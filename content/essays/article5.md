---
title: "How does the attention mechanism work?"
date: "2026-09-06"
summary: "Understanding multi-head attention mechanism"
---

## Introduction 

At a high level, when a LLM is given an input prompt it generates an output response. The main driving question that we are trying to answer is how does a model make sense of the input text and what is the mechanism that powers everything?

### Tokenization

The first step is to break down the text into pieces called tokens. Each piece is a word, but within the context of LLM each piece is referred to as a  token. Each token  is assigned with an integer value based on a dictionary. While each token is assigned with a unique ID,  each token does not capture the semantic meaning of the words.


### Token Embedding 

To embed semantic meaning into a token, we have to create a d-dimensional vector for each token. Tokens with similar meaning will have embeddings that are close to each other within the high-dimensional space.

Now that each token can be expressed with its corresponding semantic meaning, it still lacks the ability to change its semantic meaning based on the context.

For example, “There are so many bats I can choose at the baseball store.” and “I love to study bats that lives inside a cave.”

The word bats can mean different things based on the context the word is presented in. This is where the attention mechanism comes in.


