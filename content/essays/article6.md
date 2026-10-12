---
title: "Understanding Multi-Head Attention Mechanism"
date: "2026-09-06"
summary: "Understanding Multi-Head Attention Mechanism"
---

## Introduction 
In 2017, a paper named “Attention Is All You Need”[^1] was published, and it quickly became one of the most influential paper in modern deep learning. It introduced a novel architecture called the Transformer; an architecture entirely reliant on the self attention mechanism.

Before this paper was introduced, attention mechanisms were already used, but only as a secondary layer built on top of Recurrent Neural Networks (RNN) or Convolutional Neural Networks (CNN). Fast forward to 2019, GPT-2 was released; by then all language models and pretty much every language model that’s released to this day has adopted the transformer architecture.

![The paper that started it all.](/images/attention/attention-is-all-you-need.png)

To clarify, the self-attention mechanism is a mathematical mechanism that simulates context aware intelligence. The Transformer is the complete deep learning architecture that combines attention with other key components within the deep learning model such as Feed Forward Network, Layer Normalization, Residuals, and Embeddings. Here we will dive into the attention mechanism since it is the underlying component that powers modern language models. 

![Transformer on the left, attention mechanism on the right.](/images/attention/attention-architecture.png "full")

### Tokenization

Diving into a Language model, when a input prompt is given it generates an output response. The main driving question that we are trying to answer throughout this article is how does a model make sense of the input text. More precisely, what is the underlying mechanism that makes Transformers so effective at generating coherent texts?

The first step starts with breaking down the input text into smaller pieces called tokens. Each token represents the smallest unit of text that's processed by the language model. After breaking down the text into tokens, each token is assigned with an integer value based on a dictionary that associates a integer value to a unique text. So far, each token is assigned with a unique ID, however each token does not capture the semantic meaning of the word that it represents.

![Tokenization on input text](/images/attention/tokenization.png)

### Token Embedding 

To embed semantic meaning into a token, we have to create a d-dimensional vector for each token. A high-dimensional vectors allows each token to eventually capture the rich meaning associated to each token. Tokens with similar meaning will eventually have embeddings that are close to each other within the high-dimensional space. 

![Token embedding: an ID becomes a d-dimensional vector, and similar words sit close together.](/images/attention/token-embedding.png)

One thing the embedding does not carry is order. The vanilla Transformer adds a positional encoding to each embedded vector, a second d-dimensional vector that depends only on where the token sits in the sequence, so that the vector going into attention says both what the token means and which position it occupies.

```latex
X = E + P, \qquad X \in \mathbb{R}^{n \times d}
```

Now that we have established how each token can be expressed with its corresponding semantic meaning, tokens together still lack the ability to change its semantic meaning based on the context. For example, “There are so many bats I can choose at the baseball store.” and “I love to study bats that lives inside a cave.” The word, "bats" can mean different things based on the context the word is presented in. This is where the attention mechanism comes in.

### Single-Head Attention 

Before we dive straight into the full multi-head attention mechanism, we will break it down and start with the single-head attention and build a mental model of the single-head attention so that we can reasonably tackle the multi-head attention. The attention mechanism allows the model to gather contextual information between each input tokens within the input sequence. At a high level, the self-attention mechanism contains three weight matrices $W_Q$, $W_K$, $W_V$. These weights determine how much attention should be allocated to each token when making sense of the input text.

But to be precise, these weight matrices are learned linear projections that transform general input token representations into specialized representations used to decide which other tokens other than itself is relevant and what information should be gathered from them. 

Each matrices have different roles:

- $W_Q$ (Weight Query): Transforms the token into a query, which describes what this token is "looking for."
- $W_K$ (Weight Key): Transforms the token into a key, which describes what this token can be matched on.
- $W_V$ (Weight Value): Transforms the token into a value, which describes the information this token contributes if its attended to. 

![Embedded vectors stacked into the input matrix X, one row per token.](/images/attention/input-matrix.png)

Typically, the model would process batches instead of a single embedded vector at a time. Therefore you would stack embedded vectors into matrices and pass it through the Query and Key matrices.

The next mechanical step within the attention-mechanism it to multiply the input matrix X, comprised of embedded vectors, against the weight matrices. It projects the input X into weight matrices $W_Q$, $W_K$, $W_V$ which results in the outputs matrices $Q$, $K$, $V$. In single-head attention there is exactly one of each. 

```latex
Q = X W_Q, \qquad K = X W_K, \qquad V = X W_V
```

```latex
W_Q \in \mathbb{R}^{d \times d_k}, \quad W_K \in \mathbb{R}^{d \times d_k}, \quad W_V \in \mathbb{R}^{d \times d_v}
```

This begs the question, what is the purpose of this operation if the projections is just a linear transformation. To answer this, the purpose of the linear projections is not to make the output tokens more complex, but instead, re-express them into a learned space that's specialized for different role in attention. 

Single-head self-attention calculates the relevance of each token against every other token to encode contextual relationships within the input sequence. This is done by performing a matrix multiplication between the extracted query matrices.

```latex
S = Q K^{T}, \qquad S_{ij} = q_i \cdot k_j, \qquad S \in \mathbb{R}^{n \times n}
```

![Q multiplied by K transposed gives the n x n score matrix S; S[love, bats] and S[bats, love] differ.](/images/attention/attention-scores.png "large")

If token `i` were to pay the same amount of attention to token `j`, just as `j` would pay the same amount of attention to `i`, then there would be no contextual meaning between the two tokens. While tokens can pay the same amount of attention to each other, this is not always the case. There are times when the relevance of each token to another is disproportional, so by computing the dot-product between the two tokens you are able to find the asymmetric attention between one another. 

At scale this process is done by computing a matrix multiplication between the extracted vectors that make up the matrices $Q$ and $K$. The resulting output is the contextual information within a input sequence. And since the model generates text one token at a time, or in other words in an autoregressive manner, we will only consider the similarity score between the token itself and every other tokens that came before.

```latex
S_{ij} =
\begin{cases}
q_i \cdot k_j & j \le i \\
-\infty & j > i
\end{cases}
```

![Causal attention: each query row only keeps the keys at or before it, a staircase from the top-left to the bottom-right of the score matrix.](/images/attention/causal-attention.png "large")

Between the dot-products of the extracted $Q$ and $K$ vectors, the relevance or similarity scores can be negative or positive and skew heavily in either directions. Before the softmax, the vanilla Transformer divides every score by $\sqrt{d_k}$. The dot-products grow with the length of the vectors, and without the scaling a large $d_k$ pushes the softmax toward putting all of its weight on a single token. We would apply a softmax function to convert the raw scores into a normalized probability distribution such that all scores ranges between 0 and 1. These result values are referred as the attention scores; representing how much inference each token should have. 

```latex
A = \operatorname{softmax}\!\left(\frac{S}{\sqrt{d_k}}\right), \qquad A_{ij} = \frac{e^{S_{ij}/\sqrt{d_k}}}{\sum_{m} e^{S_{im}/\sqrt{d_k}}}, \qquad \sum_{j} A_{ij} = 1
```

We then multiply the attention scores to the $V$ matrix which helps extract the contextual information within the input sequence. The resulting output would be a output matrix, $O$. 

![Attention scores A multiplied by V give the output matrix O.](/images/attention/attention-av.png)

For a single head, $d_v = d$, so $O$ is already $n \times d$. At this point the dimension of output matrix should be in the exact shape as the input embedding matrix $X$, however this matrix $W_O$ is needed to mix features across different attention heads. We have not introduced multi-head attention, but we will dive into it very shortly. Just know that the single-head attention mechanism consists of one set of weights and one pass through the mechanism, while the multi-head attention which runs several of these operations in parallel which will be explained after.

```latex
O = A V, \qquad O \in \mathbb{R}^{n \times d_v}
```

```latex
\operatorname{Attention}(Q, K, V) = \operatorname{softmax}\!\left(\frac{Q K^{T}}{\sqrt{d_k}}\right) V
```

![O multiplied by W_O gives the output at the embedding width d.](/images/attention/attention-wo.png)

At a scale, this is what all of the self-attention components look like together. Starting from the input sequence, into the $QKV$ Weights, to computing the attention logits, processing it into attention scores, then finally getting it to its final form, output matrix O. 

![Single-head attention end to end: X projected into Q, K, V; the causal scores S and softmaxed A; O = A V; and W_O back to the embedding width.](/images/attention/single-head-overview.png "large")

That is the whole of single-head attention. Note that the matrix that comes out of $W_O$ is not a new representation of the sequence, but instead it is the "correction" to the old one; a new representation that is context rich. 

The output matrix $O$ has the same shape as the input matrix $X$. The follow step is to take one each row per token and add it back onto the input matrix $X$ through a residual connection, followed by a layer normalization: $X' = \text{LayerNorm}(X + O W_O)$. Each row of $X'$ is the token's original embedding plus whatever context attention gathered for it.

```latex
X' = \operatorname{LayerNorm}\left(X + O W_O\right), \qquad W_O \in \mathbb{R}^{d_v \times d}
```

Lastly, $X'$ is then passed through a feed forward network consists of two linear layers with a non-linearity between them, applied to each row on its own, with the same residual and normalization around it. Attention is the only step where tokens exchange information; the feed forward network processes each token independently. 

```latex
\operatorname{FFN}(x) = \max(0,\ x W_1 + b_1)\, W_2 + b_2, \qquad X'' = \operatorname{LayerNorm}\left(X' + \operatorname{FFN}(X')\right)
```

<!-- Check Point -->
### Multi-Head Attention

The single-head attention with a single query, key, and value matrix has one issue, it just isn't enough to capture the complex relationships between tokens. To address this, we have multiple sets of the query, key, and value matrices. This enables the model to "learn and represent diverse types of relationships between tokens"[^2]. This is achieved by extending the dimensions of the $Q$, $K$, $V$, and its respective weights by introducing a new variable h. $h$ represents the number of heads. To further capture all of the information, the paper would extend the model even further by adding layers such that there are multiple layers of multi-head attention. In the diagram we will show 4 heads and 3 layers, but in the "Attention is all you need paper" note that there were 8 heads and 6 layers within the transformer architecture.

![Multi-head attention: one layer holds h heads, each running single-head attention on a d/h slice of X, concatenated and mixed by W_O; N such layers are stacked.](/images/attention/multi-head.png "full")

```latex
\operatorname{MultiHead}(X) = \operatorname{Concat}\left(\text{head}_1, \dots, \text{head}_h\right) W_O, \qquad \text{head}_i = \operatorname{Attention}\left(X W_Q^{(i)},\ X W_K^{(i)},\ X W_V^{(i)}\right)
```

```latex
\textcolor{#e03131}{W_Q} \in \mathbb{R}^{d \times (d_k \times h)}, \quad \textcolor{#2f9e44}{W_K} \in \mathbb{R}^{d \times (d_k \times h)}, \quad \textcolor{#e67700}{W_V} \in \mathbb{R}^{d \times (d_v \times h)}, \quad \textcolor{#0c8599}{W_O} \in \mathbb{R}^{(d_v \times h) \times d}
```

```latex
X^{(\ell)} = \operatorname{Layer}\left(X^{(\ell-1)}\right), \qquad \ell = 1, \dots, N
```

Within each layer, the multihead attention will generate an output matrix across all heads with the same dimensions. We then add all the output matrices side by side in the same layer. Now within each layer, it takes the output of $l-1$ as its input. Nothing is concatenated unlike the mutli-head attention. The matrix stays in the same `n` x `d` dimension the whole as the output matrices passes through each layer. 

As the matrix flows through the transformer architecture, it'll eventually reach an end where the model is now ready to form a prediction. A prediciton is made by one more linear layer that multiplies an embedding projhect matrix $W_vocab$ to map hidden features into unformalized log-probabilities across the entire vocabulary, and then feed it into one more softmax to convert the vocabulary logits into actual probabilities. In the original paper this matrix is not a new set of weights, it is the transpose of the token-embedding matrix from the start of the model, $W_{vocab} = E^{T}$, so the logit for each word is the dot product between the final hidden row and that word's embedding.

![The last row of X^(N) times W_vocab gives logits over the vocabulary; a softmax turns them into next-token probabilities.](/images/attention/next-token.png "large")


[^1]: [Attention Is All You Need - Vaswani et al., 2017](https://arxiv.org/pdf/1706.03762)
[^2]: [How Attention Got So Efficient](https://www.youtube.com/watch?v=Y-o545eYjXM&t=182s)
