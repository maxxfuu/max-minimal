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

Diving into a Language model, when a input prompt is given it generates an output response. The main driving question that we are trying to answer throughout this article is how does a model make sense of the input text. More precisely, what is the underlying mechanism that makes Transformers so effective at gereneating coherent texts?

The first step starts with breaking down the input text into smaller pieces called tokens. Each token represents the smallest unit of text thats processed by the language model. After breaking down the text into tokens, each token is assigned with an integer value based on a dictionary that associates a integer value to a unqiue text. So far, each token is assigned with a unique ID, however each token does not capture the semantic meaning of the word that it represents.

![Tokenization on input text](/images/attention/tokenization.png)

### Token Embedding 

To embed semantic meaning into a token, we have to create a d-dimensional vector for each token. A high-dimensional vectors allows each token to eventually capture the rich meaning associated to each token. Tokens with similar meaning will eventually have embeddings that are close to each other within the high-dimensional space. 

![Token Embedding](/images/attention/token-embedding.png "full")

Now that we have established how each token can be expressed with its corresponding semantic meaning, tokens together still lack the ability to change its semantic meaning based on the context. For example, “There are so many bats I can choose at the baseball store.” and “I love to study bats that lives inside a cave.” The word, "bats" can mean different things based on the context the word is presented in. This is where the attention mechanism comes in.

### Attention Mechanism

The attention mechanism allows the model to gather contextual information between each input tokens within the input sequence. At a high level, the self-attention mechanism contains three weight matricies $W_Q$, $W_K$, $W_V$. These weights determine how much attention should be allocated to each token when making sense of the input text.

But to be precise, these weight matrices are learned linear projections that transform general input token representations into specialized representations used to decide which other tokens other than itself is relevant and what information should be gathered from them. 

Each matrices have different roles:

- $W_Q$ (Weight Query): Transforms the token into a query, which describes what this token is "looking for."
- $W_K$ (Weight Key): Transforms the token into a key, which describes what this token can be matched on.
- $W_V$ (Weight Value): Transforms the token into a value, which describes the information this token contirbutes if its attended to. 

[insert image]

> Typically, the model would process batches instead of a single embedded vector at a time. Therefore you would stack embedded vectors into matrices and pass it through the Query and Key matrices.

![Embedded vectors stacked into the input matrix X, one row per token.](/images/attention/input-matrix.png "large")

The next mechanical step within the attention-mechanism it to mulitply the input matrix X, comprised of embedded vectors, against the weight matrices. It projects the input X into weight matricies $W_Q$, $W_K$, $W_V$ which results in the outputs matricies $Q$, $K$, $V$. 

This begs the question, what is the purpose of this operation if the projections is just a linear transformation. To answer this, the purpose of the linear projections is not to make the output tokens more complex, but instead, re-express them into a learned space thats specialized for different role in attention. 

<!-- Check Point --->

The next step is to quntify the relevance of each token against every other token. This is done by performing a matrix mulitplication between the extracted query matricies.

[insert image], Attention(x_i, x_j) = Attention(x_j, x_i)

If token i were to pay the same amount of attention to j, just as j would pay the same amount of attention to i, there would be no contextual meaning. While tokens can pay the same amount of attention to each other, this is not always the case. By calculating the dot-product between the extracted vectors that make up the matrices $Q$ and $K$, we can get the similarity scores between the two tokens and find asymmetric attention between each tokens, thus providing richer context within the input text. Since the model generates text one token at a time, or in other words in an autoregressive manner, we will only consider the similarity score between the token itself and every other tokens that came before.

Between the dot-products of the extracted $Q$ and $K$ vectors, the relevance or similarity scores can be negative or positive and skew heavily in either directions. We would apply a softmax function to convert the raw scores into a normalized probability distrbution such that all scores ranges between 0 and 1. These result values are refered as the attention scores; representing how much inference each token should have. 

We then multiply the attention scores to the $V$ matrix which helps extract the contextul information within the input seqeunece. The resulting output would be a output matrix, $O$. However the dimension of output matrix would be too small so we will use an output weight matrix to convert the dimensions back to same dimensions as the token embeddings. 

[^1]: [Attention Is All You Need - Vaswani et al., 2017](https://arxiv.org/pdf/1706.03762)
