---
title: "How does the attention mechanism work?"
date: "2026-09-06"
summary: "Understanding multi-head attention mechanism"
---

## Introduction 
In 2017, a paper named “Attention Is All You Need”[^1] was published, and it quickly became one of the most influential paper in modern deep learning. It introduced a novel architecture called the Transformer; an architecture entirely reliant on the self attention mechanism.

Before this paper was introduced, attention mechanisms were already used, but only as a secondary layer built on top of Recurrent Neural Networks (RNN) or Convolutional Neural Networks (CNN). Fast forward to 2019, GPT-2 was released; by then all language models and pretty much every language model that’s released to this day has adopted the transformer architecture.

![The paper that started it all.](/images/attention/attention-is-all-you-need.png)

To clarify, the self-attention mechanism is a mathematical mechanism that simulates context aware intelligence. The Transformer is the complete deep learning architecture that combines attention with other key components within the deep learning model such as Feed Forward Network, Layer Normalization, Residuals, and Embeddings. Here we will dive into the attention mechanism since it is the underlying component that powers modern language models. 

![The Transformer on the left, encoder stack beside decoder stack. Every block in it is either an attention layer, a feed forward network, or an Add & Norm, and the whole stack repeats N times; the encoder's output crosses over into the decoder as K and V, which is the cross attention. The decoder's first attention layer is masked so a position can only look at positions before it. On the right, one multi-head attention block: Q, K and V are each projected h times into smaller subspaces, every head runs scaled dot-product attention on its own projection, and the h outputs are concatenated and projected once more.](/images/attention/attention-architecture.png "full")


### Tokenization

Diving into a Language model, when a input prompt is given it generates an output response. The main driving question that we are trying to answer throughout this article is how does a model make sense of the input text, and what is the underlying mechanism that powers it all?

The first step starts with breaking down the input text into smaller pieces called tokens. Each piece usually represents a word; but within the context of LLM each piece is referred to as a token. Each token is assigned with an integer value based on a dictionary. So far each token is assigned with a unique ID, however, each token does not capture the semantic meaning of the word that it represents.

![Tokenization on input text](/images/attention/tokenization.png)


### Token Embedding 

To embed semantic meaning into a token, we have to create a d-dimensional vector for each token. Tokens with similar meaning will have embeddings that are close to each other within the high-dimensional space.

Now that each token can be expressed with its corresponding semantic meaning, it still lacks the ability to change its semantic meaning based on the context.

For example, “There are so many bats I can choose at the baseball store.” and “I love to study bats that lives inside a cave.”

The word bats can mean different things based on the context the word is presented in. This is where the attention mechanism comes in.

### Attention Mechanism

The attention mechanism allows the model to gather contextual information between each input tokens within the input sequence. At a high level, the weight matrices $W_Q$, $W_K$, $W_V$ determine how much attention should be allocated to each token when making sense of the input text.

But to be precise, these weight matrices are learned linear projections that transform general input token representations into specialized representations for dyanmic routing.

- Q (Query): What each token is "looking for."
- K (Key): The informational "label" each token provides.
- V (Value): The actual semantic value content passed along. 

> Typically, the model would process batches instead of a single embedded vector at a time. Therefore you would stack embedded vectors into matrices and pass it through the Query and Key matrices.

By multiplying the input matrix X comprised of embedded vectors against the weight matrices, it projects the input X into Q, K, V matrices. However this begs the question, why do we need these $Q$, $K$,$V$, projections if its just a linear transformation. 

Assume that you didn’t multiply the input into the weight matrices, when computing the similarity score between a token against every other token, it would result in the similarity score or attention being identical.

[insert image], Attention(x_i, x_j) =Attention(x_j, x_i)

If token i were to pay the same amount of attention to j, just as j would pay the same amount of attention to i, there would be no contextual meaning. While tokens can pay the same amount of attention, this is not always the case.

By calculating the dot-product between the embedded vectors and the weight matrices, we can get the similarity scores between the two and find asymmetric attention between each tokens, thus providing richer context within the input text.







![Token Embedding](/images/attention/token-embedding.png "full")

[^1]: [Attention Is All You Need - Vaswani et al., 2017](https://arxiv.org/pdf/1706.03762)
