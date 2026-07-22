---
title: "How Do Transformers Learn to Associate Tokens: Gradient Leading Terms Bring Mechanistic Interpretability"
source_url: https://iclr.cc/virtual/2026/oral/10011067
paper_pdf_url: https://arxiv.org/pdf/2601.19208v2
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# How Do Transformers Learn to Associate Tokens: Gradient Leading Terms Bring Mechanistic Interpretability

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

HOW DO TRANSFORMERS LEARN TO ASSOCIATE TOKENS: GRADIENT LEADING TERMS BRING MECHANISTIC INTERPRETABILITY

Shawn Im1, Changdae Oh1, Zhen Fang2, Sharon Li1

1University of Wisconsin–Madison 2University of Technology Sydney {shawnim,changdae,sharonli}@cs.wisc.edu, zhen.fang@uts.edu.au

## ABSTRACT

Semantic associations such as the link between “bird” and “flew” are foundational for language modeling as they enable models to go beyond memorization and instead generalize and generate coherent text. Understanding how these associations are learned and represented in language models is essential for connecting deep learning with linguistic theory and developing a mechanistic foundation for large language models. In this work, we analyze how these associations emerge from natural language data in attention-based language models through the lens of training dynamics. By leveraging a leading-term approximation of the gradients, we develop closed-form expressions for the weights at early stages of training that explain how semantic associations first take shape. Through our analysis, we reveal that each set of weights of the transformer has closed-form expressions as simple compositions of three basis functions–bigram, token-interchangeability, and context mappings–reflecting the statistics of the text corpus and uncovering how each component of the transformer captures semantic associations based on these compositions. Experiments on real-world LLMs demonstrate that our theoretical weight characterizations closely match the learned weights, and qualitative analyses further show how our theorem shines light on interpreting the learned associations in transformers.

## INTRODUCTION

Large language models (LLMs) based on self-attention have shown strong capabilities in capturing both factual knowledge and qualitative aspects of the human world (Grattafiori et al., 2024; Yang et al., 2025; Team et al., 2024; Achiam et al., 2023). This progress has sparked growing interest in understanding why these models work so well and, in particular, what kinds of internal structures emerge during training (Engels et al., 2024; Li et al., 2023a; Meng et al., 2022; Cunningham et al., 2023). Among these structures, semantic associations are especially foundational to language modeling (Harris, 1954; Firth, 1957; Miller & Charles, 1991), as they enable models to connect words and concepts in ways that support generalization and coherent text generation. While recent studies have identified specific mechanisms such as induction heads (Olsson et al., 2022), linear semantic relations (Nanda et al., 2023), and topic clustering (Li et al., 2023b), we still lack a principled account of how semantic associations arise during the training of attention-based transformers.

By semantic associations, we mean the statistical and functional relationships between tokens that encode meaning—for example, the link between “bird” and “flew”, the interchangeability of “car” and “truck” in adjectival contexts, or the coupling of “country” and “capital”. These associations have long been recognized in linguistics under the lens of distributional semantics (Harris, 1954). In modern transformers, such associations are not explicitly programmed but instead emerge through gradient-based optimization over large corpora. Understanding how these structures crystallize during training is therefore essential not only for connecting deep learning with linguistic theory but also for developing a mechanistic foundation of representation learning in large language models.

In this work, we develop a theory for the emergence of semantic associations in attention-based language models trained on natural language data, through the lens of training dynamics. A formal arXiv:2601.19208v2 [cs.CL] 12 May 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026

**Figure 1.** To understand the emergence of associative features, we analyze the training dynamics of Transformers by focusing on the gradient leading terms for weights, which allows us to identify interpretable basis functions that characterize each weight by their compositions. Empirical validation confirms that our weight characterizations match the actual ones learned in practical transformers.

analysis of training dynamics is attractive as it allows us to rigorously discuss how modern language models learn features and capabilities. Unfortunately, the training dynamics of transformers are highly complex, which has led prior work to adopt unrealistic assumptions that diverge from practice: (1) synthetic structured language (Li et al., 2023b; Yang et al., 2024), (2) simplified model architectures without, e.g., positional encoding or residual connections (Tian et al., 2023; Huang et al., 2025), and (3) non-standard training, such as sequential component-wise training or partially frozen weights (Bietti et al., 2023; Li et al., 2023b). While these prior works provide valuable theoretical insights, their departures from realistic conditions raise concerns about the generalizability of their insights to LLMs used in practice. In contrast, we ground our study in a more realistic setting by focusing on naturalistic text distributions and attention-based transformers with positional encodings, optimized with a standard training procedure (Brown et al., 2020). This is essential to minimize the gap between our theory and practical use.

Our key technical innovation is to analyze training dynamics of the transformer at an early stage, through the leading term of an expansion of the gradients for each set of weights. In particular, transformers are known to acquire many core behaviors early in training–including semantic relations– and persist through convergence (Olsson et al., 2022; Elhage et al., 2021; Nanda et al., 2023). This makes the early phase not only empirically important but also analytically tractable. During this stage, gradient updates admit a closed-form approximation: the leading term dominates parameter updates before higher-order corrections accumulate. Leveraging this, we show that the learned weight matrices (including the output matrix, value matrices, query-key matrices) can be expressed as simple compositions of three basis functions: a bigram mapping, which captures next token dependencies; an interchangeability mapping, which reflects functional similarity across tokens (e.g., synonyms or shared grammatical roles); and a context mapping, which encodes longer-range prefix–suffix co-occurrence.

Through experiments on a natural language dataset, we verify that the learned weights in an attention-based transformer model closely match our theoretical closed-form expressions, and further demonstrate that this holds even beyond the early stage. We also show rich qualitative examples of how each weight component of the transformer captures the actual word-wise semantic associations characterized by our theorem. Furthermore, we verify that our theoretically characterized features are correlated with the behavior of real-world language model. Figure 1 depicts an overview of our analysis, and we summarize our contributions as follows:

1. We present the first explicit characterization of weights in attention-based transformers trained on real-world text corpora under the next-token prediction loss;

2. We interpret the features learned in weights as compositions of bi-gram, interchangeability, and context mappings, and then show how these basis functions capture semantic association across words;

![Figure extracted from page 2](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

3. We finally validate our theoretical interpretation on both self-attention models and practical LLM, demonstrating the generality and relevance of our theorems.

## 2 RELATED WORKS

Understanding emergence of features in Transformers. Many works have considered the training dynamics of transformers under controlled settings to interpret their feature learning (Tian et al., 2023; Bietti et al., 2023; Nichani et al., 2024; Kim & Suzuki, 2024). A line of them investigates how low-level associative features, such as bigram structure (Bietti et al., 2023), cyclic structure (Huang et al., 2025), and co-occurrence (Tian et al., 2023; Yang et al., 2024), are learned from data. There are also multiple works that analyze how high-level capabilities, such as chain-of-thought (Kim & Suzuki, 2025), topic clustering (Li et al., 2023b; Jiang et al., 2024), reasoning or memorization (Yao et al., 2025), and in-context learning capability (Nichani et al., 2024; Bietti et al., 2023; Wang et al., 2024a; Kim & Suzuki, 2024; Edelman et al., 2024), are obtained during training. Although insightful, they often assume structured or abstract language data (Li et al., 2023b; Nichani et al., 2024; Yang et al., 2024), unrealistic model architecture (Tian et al., 2023; Cui et al., 2024; Troiani et al., 2025), and adjusted training strategies far from practice (Bietti et al., 2023; Kim & Suzuki, 2024; Huang et al., 2025), which depart from reality. In contrast, our theoretical analysis is grounded in natural language data, realistic architecture, and a standard training strategy. As a result, our theory substantially reduces the gap between formal analysis and practical use, which is further corroborated by our empirical validations.

Understanding feature learning beyond Transformers. Recent work has also explored how models learn data-dependent features through dynamics for non-transformer models as well (Dandi et al., 2023; Ba et al., 2022; Mousavi-Hosseini et al., 2023). However, this line of work similarly considers abstractions of language, such as Gaussian data (Ba et al., 2022), single or multi-index models (Damian et al., 2024; Dandi et al., 2023), or spiked models (Wang et al., 2024b; Mousavi- Hosseini et al., 2023), and considers measures of data complexity with Hermite expansions (Bietti et al., 2022; Damian et al., 2024; Lee et al., 2024). On the contrary, we adopt a realistic theoretical setup to analyze features in transformers, which remains the dominant architecture in practice.

PRELIMINARY

## 3.1 PROBLEM STATEMENT

Semantic associations are foundational for language models: they enable models to go beyond memorizing sequences and instead generalize across contexts (Hinton, 1984), infer latent structure (Wu et al., 2018), and generate coherent text. Despite their importance, the mechanisms by which transformers acquire these associations during training remain poorly understood. Towards a mechanistic and theory-grounded interpretation of LLMs in a more realistic setup, we pose the question:

How do semantic associations emerge during the training of attention-based language models on natural language data?

It is worth noting that we focus here on general natural language data, rather than synthetically structured or abstractive language, which has been considered in previous works (Yang et al., 2024; Nichani et al., 2024; Huang et al., 2025). This is essential to minimize the gap between our theory and practical use, since real-world text is highly diverse and is not restricted to a specific structure. In addition, prior studies (Olsson et al., 2022; Elhage et al., 2021; Nanda et al., 2023) have shown that critical semantic and reasoning abilities, such as induction heads and linear semantic relations, can already emerge in the early stage and be preserved through convergence. This makes the early stage of training a natural and necessary focus for theoretical analysis, which we now develop.

## 3.2 MODEL ARCHITECTURE

Prior works have analyzed the training dynamics of attention-based models under simplifying assumptions, such as restricting attention to low rank (Cui et al., 2024), removing causal masking (Tian et al., 2023; Yang et al., 2024), without positional encodings (Bietti et al., 2023) or residual

<!-- Page 4 -->

Published as a conference paper at ICLR 2026 streams (Huang et al., 2025). In line with Nichani et al. (2024), we study an attention-based architecture that retains these components: positional encodings, causal masking, and residual streams. To further align with practice, we employ a relative positional encoding scheme, as in T5 (Raffel et al., 2020), rather than augmenting embeddings with absolute position vectors. We begin by introducing the necessary notation before formally defining the transformer computation.

Let V = {e1,..., ej,..., e|V|} denote the set of vocabulary. For an input sequence of length T, we represent the input as a matrix X ∈RT ×|V|, where each row of X is the one-hot encoding of the t-th token in the sequence. In an L-layer transformer, the parameters associated with self-attention are given by {W(l), P(l), V(l)}L l=1 together with WO, where W(l) ∈R|V|×|V| is the key–query matrix of layer l, V(l) ∈R|V|×|V| is the value matrix, P(l) ∈RT is the learned relative positional encoding, and WO ∈R|V|×|V| is the output matrix. The model with input X is defined as follows.

Definition 3.1 (Attention-Based Transformer). Given an input matrix X ∈RT ×|V|, the L-layer attention-based transformer with parameters Θ = {W(l), P(l), V(l)}L l=1 ∪{WO} is defined as

FΘ(X) = h(L)WO, (1)

where hL is defined by the recurrence relation, i.e., h(l) = h(l−1) + S(Mask(h(l−1)W(l)h(l−1)⊤+ DM(P(l))))h(l−1)V(l) and h(0) = X, (2)

where S(·) represents the softmax function, DM(v) maps the ith element of v to the (−i+1)th subdiagonal, and Mask(·) denotes the operator of attention mask. This architecture is in line with Nichani et al. (2024), and recent work shows that self-attention–only models can match the performance of architectures with MLP layers (Wang et al., 2025).

## 3.3 TRAINING SETUP

Learning objective. To align with standard language modeling practice and ensure comparability with prior works (Huang et al., 2025; Nichani et al., 2024), we adopt the standard cross-entropy objective: given N input matrices X1,..., XN with sequence length T and corresponding output matrices Y1,..., YN, where Yi ∈RT ×|V|, the objective function is defined as

L(Θ) = −1

NT

N X i=1

T X t=1 log S(Fθ(Xi)[t])Y[t]⊤ i, (3)

where M[t] denotes the t-th row of a matrix M and Y[t]

i corresponds to the one-hot embedding for the t + 1-th token of the sequence corresponding to Xi.

Gradient descent. We analyze the evolution of the parameters under full-batch gradient descent with a constant learning rate η. Under gradient descent, the parameters are updated as follows:

Θ(t) = Θ(t −1) −η∇ΘL(Θ). (4)

Due to the nonlinear complexities of the gradient, deriving an exact form for even one of the weight matrices after t steps is challenging. We address this challenge by considering a leading-order approximation technique, allowing for a closed-form expression of the gradients and weights while yielding a tight approximation of the full gradient.

THEORETICAL ANALYSIS

In Section 4.1, we provide theorems demonstrating that the weights of attention-based transformers remain close to their gradient leading terms for O(1/η) steps under both zero and Gaussian initializations. Then, Section 4.2 uncovers how three basis functions, which are crucial to express token associations and language structure, are encapsulated in those gradient leading terms, and how these three functions are compounded to shape the desiderata of the transformers’ weight matrices.

## 4.1 MAIN THEOREMS

Under the setup described in Sec. 3, we obtain the following results for attention-based transformers.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

**Figure 2.** Illustration of theoretical results. We characterize weight matrices of the attention-only transformer as compositions of three basis functions: bigram mapping, interchangeability mapping, and context mappings. We illustrate how these mappings are composed across weight matrices to learn semantic associations between a given query token and its surrounding text.

Theorem 4.1. (Informal) Given an attention-based transformer (Def. 3.1) under sufficiently small Gaussian initialization, with L ≤

√

T/4, after s gradient descent steps with learning rate η ≥1

T, if s ≤η−1 min(8 √

T, 1 12L), then for all layers l = 1,..., L, WO −sη ¯B

F ≤3s2η2, (5) V(l) − s

2 η2 ¯Φ⊤¯B⊤

F

≤12s3η3, (6) W(l) −

3 s

4

+ 2 s

3 η4 ¯Q

F

≤13s5η5T, (7) P(l) −

3 s

4

+ 2 s

3 η4∆

F

≤13s5η5T, (8)

where ∥· ∥F is the Frobenius norm, ¯B corresponds to a bigram statistic, ¯Φ corresponds to a context co-occurrence statistic, ¯Q corresponds to a token-to-token correlation based on a composition of ¯B and ¯Φ, and ∆corresponds to a relative position correlation based on the same feature as ¯Q.

The above Theorem shows that any finite-depth L-layer attention-based transformer (Def. 3.1) has the same characterization for its weights uniformly across all layers under a zero-initialization (Theorem D.10) and a small Gaussian initialization (Theorem 4.1), suggesting that all layers of the model capture common associative features from natural language as a starting point before evolving differently as training progresses (Figure 6). As seen in Figure 2, compositions of these features form the leading terms of the output matrix (¯B), value matrix (¯Φ⊤¯B⊤), and query-key matrix (¯Q). We walk through these matrices in Section 4.2.1 and how they form the weights of the model in Section 4.2.2. The formal theorem and proofs are in Appendix D.

## 4.2 INTERPRETATION OF THEOREMS

In the previous section, we showed that the model parameters can be approximated by key corpus statistics ¯B, ¯Φ, ¯Q and ∆. Now, we discuss the definitions of these statistics by first introducing three basis functions and explaining how their composition characterizes the model’s behavior.

## 4.2.1 THREE BASIS FUNCTIONS SHAPING ASSOCIATIVE FEATURES

(1) Bigram mapping ¯B. The (i, j)-th element in ¯Bij corresponds to a correlation between token ei and token ej based on how likely ei is to be directly followed by ej as a bigram. More precisely,

¯Bij = Pt(ei)Pt(ej|ei) −Pt(ei)/|V|, (9)

where Pt(ei) is the relative frequency of ei over all tokens in the dataset X1,..., XN and Pt(ej|ei) is the relative frequency of ej given that the previous token was ei. The product between Pt(ei) and Pt(ej|ei) forms an estimate of the likelihood of ei followed by ej appearing as a bigram and the second term −Pt(ei)/|V| simply acts as a centering term such that each row sums to 0.

![Figure extracted from page 5](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

Published as a conference paper at ICLR 2026

(2) Interchangeability mapping Σ¯B. We study Σ¯B = ¯B⊤¯B, the correlation matrix of ¯B, which captures correlations between pairs of tokens based on a frequency-weighted similarity of their previous-token distributions. From Eq. (9), neglecting the centering terms, the (i, j)-th element of Σ¯B can be represented as

Pt(ei)Pt(ej) | {z } Frequency weighting

|V| X k=1

Pt(e← k |ei)Pt(e← k |ej) | {z } Previous token similarity

. (10)

In essence, Eq. (10) shows that Σ¯B captures a symmetric relationship between tokens based on how similar of a function or role they play across different contexts. Specifically, in Eq. (10), we can see that the corresponding row, which acts as a feature for token ei captures its associations with interchangeable tokens captured by the previous token similarity factor and frequent tokens captured by the frequency weights. Similarities in previous token distributions are an indicator of functional similarities or interchangeability, as this captures structural patterns such as nouns being preceded by articles or adjectives and objects being preceded by common descriptors. This interchangeability map, Σ¯B, acts a building block of characterizations for the weights W(l) and P(l) as illustrated in Figure 2. We depict a simple example of a word-wise correlation captured by Σ¯B in Figure 1.

(3) Context mapping ¯Φ. The (i, j)-th element of ¯Φ corresponds to a correlation between token ei and ej based on how likely ej is to appear as a prefix of ei. This can be written as

1 T

T X k=1

1 k k X m=1

Pt(the k + 1 -th token is ei, the m -th token is ej) −µj, (11)

the pond contains fish

7 24

4

**Figure 3.** An example of ¯Φ with arrows pointing to prefix tokens for “fish” with context summary scores on edges. Larger values indicate the token appears more frequently in the context of “fish”.

where µj centers the columns of ¯Φ to be 0. Considering each row as an embedding for a token ei, which represents an average of the tokens that appear in its context, i.e., smoothed context.

More precisely, the strength of the association from token ei to ej is determined by the average probability that ej appears in the context of ei over possible positions of ei and ej. This matrix can be interpreted as assigning a representation to a token based on a summary of the possible contexts that token ei appears in. This allows for learning associations between words that capture richer semantic relationships than bigram features. For example, we could expect to see correlations between animal and habitat, country and capital, or emotions and facial expressions (See Figure 3). This context mapping ¯Φ is a core building block of the gradients for the query-key attention W(l)

and value V(l) matrices as shown in Figure 2.

## 4.2.2 COMPOSITION OF BASIS FUNCTIONS FOR SEMANTIC ASSOCIATION

We now show how these three basis functions, bigram mapping ¯B, interchangeability mapping Σ¯B, and context mapping ¯Φ, are compounded to characterize four classes of weight matrices of the transformer.

(1) Output matrix WO. As shown in Eq. (5), ¯B is the leading term of WO, and thus the mapping from embedding vectors to output predictions can be understood by examining the matrix product ei ¯B for a token embedding ei. The j-th element of the resulting output vector is ¯Bij, and each ¯Bij includes a factor of Pt(ei). This implies that tokens are scored according to how frequently they occur in the average next-token distribution of ei, and explain how models at early stages effectively learn bigram-like patterns.

(2) Value matrix V(l). The leading term of the value matrix V(l) can be expressed as ¯Φ⊤¯B⊤as noted in Eq. (6), which acts as a composition of a context summary and bigram mapping. Because

<!-- Page 7 -->

Published as a conference paper at ICLR 2026

¯Φ⊤captures longer-term dependencies and ¯B⊤captures only bigram statistics, the resulting embedding from V(1) still endows the original token representations with semantic properties similar to those of ¯Φ⊤as seen in Figure 2.

(3) Attention matrix W(l). Theorem 4.1 characterizes the attention weight (a shared query-key matrix) as ¯Q, which is constructed as a composition of Σ¯B, ¯Φ, the input matrix Xi, the output matrix Yi, etc. We note that this compound feature captures a token-to-token correlation determined by how predictive one token is of the other’s next-token distribution based on the context and interchangeability mappings. We walk through an overview of the construction of ¯Q in three steps (See Appendix A for details).

1. Input-output matching scoring in context. As a preliminary step, we first define a composed feature Σ¯B ¯Φ by multiplying the interchangeability mapping Σ¯B with the context mapping

¯Φ. This composition utilizes local interchangeability to map a token to a class of similar tokens and utilizes the context mapping to capture longer-range semantic correlations shared by the set of similar tokens. Using this feature, for each sample, we assign scores between each input and output token. 2. Masking and centering. The auto-regressive constraint is enforced by masking future tokens, keeping only scores from input tokens that precede the output token. Then, the resulting scores for each output token are centered and normalized based on its position. 3. Next-to-query shift and averaging. The scores between each input and output token are then shifted so that the same score is assigned instead to be between the input token and the token directly preceding the output token. Then, the scores are averaged across all samples.

(4) Positional encoding P(l). The closed-form characterization ∆of the positional encoding P(l) follows a very similar composition to ¯Q, with the main difference being that the correlations are mapped to positional differences rather than to the vocabulary-space differences (See Lemma D.1).

## 4.2.3 HOW THE WEIGHTS COOPERATE

To illustrate how the weights work together and provide further context on the role of each of the weights as functions, we consider the leading-term computation of a single-layer attention-based model. Dropping constant factors to focus on the interactions between features, the leading terms of the entire model computation can be written as

S

Mask

X¯QX⊤+ DM(∆)

X¯Φ⊤¯B⊤+ X

¯B. (12)

We can further decompose this into XWO and the computation from the self-attention block is:

S

Mask

X¯QX⊤+ DM(∆)

X¯Φ⊤Σ¯B. (13)

¯Q and ∆capture correlations between two tokens or two positions based on how predictive the first token/position is of the next-token distribution of the second token/position according to (¯Φ⊤Σ¯B)⊤. Notice that the attended tokens are mapped to the output space by ¯Φ⊤Σ¯B, the same feature that determines the correlations for attention. As a result, the self-attention block effectively attends to tokens that, under the value and output matrix projection, lead to better next-token prediction. Thus, we find that while the residual stream XWO provides an average prediction of the next token, ¯Q enables the model to refine this prediction by selectively focusing on tokens most indicative of the next-token given its current parameters, those capturing corpus association statistics.

Implication. By considering an end-to-end analysis of the model under simultaneous training of layers and by decomposing the weights, we obtain a clear interpretation of how different components collaborate to form semantic representations and can rigorously contextualize the function of each component in the full computation of attention-based transformers. While these features only yield small changes in the actual text output, they provide important insight into how the model’s behavior develops during training. For example, if early training already associates fish with pond (as in Figure 3), we expect such relationships to be a useful anchor for later training, allowing the model to complete more complex sentences, e.g., “A pond in the garden was filled with colorful fish that sparkled in the sunlight”, coherently with learned semantic associations.

<!-- Page 8 -->

Published as a conference paper at ICLR 2026

## 5 EXPERIMENTS

5.1 3-LAYER ATTENTION-BASED TRANSFORMER

We begin with an experimental setting designed to closely mirror our theory, enabling direct verification of results and analysis of the semantic relationships embedded in the learned weights. For clearer interpretability, we use the TinyStories dataset (Eldan & Li, 2023), truncated to the 3,000 most frequently occurring words, which also defines the model’s vocabulary. A 3-layer self-attention model defined in Definition 3.1 is then trained with sequence length T = 200.

**Table 1.** Minimum cosine similarities between theoretical and actually learned weights across all epochs. Results from a 3-layer attention-based model trained on TinyStories (small η).

Weights Min. Cosine

Attention 0.999496 Value 0.999169 Output 0.998486

0 20 40 60 80 100 Epoch

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

Cosine Similarities Large LR

Attention (range across layers)

Value (range across layers) Output (range across layers)

**Figure 4.** Cosine similarity between theoretical and learned weights. Results from a 3-layer transformer model trained on TinyStories.

Verification of theory. To verify Theorem 4.1, we measure the cosine similarity between the learned weights and their corresponding leading terms at checkpoints over the first 100 epochs of SGD using a batch size of 2048 for computational tractability with a learning rate of 0.005. We also consider the cosine similarity between the learned weights and their leading terms when using a larger learning rate of 0.05 to understand how features evolve at later stages with respect to the leading term gradients. We provide results for both settings in Table 1 and Figure 4. The results show that the learned weights maintain strong agreement with the theoretical predictions: even after 30 epochs, all weights achieve a cosine similarity of at least 0.9. Moreover, all parameter matrices have a cosine similarity above 0.7, even after 100 epochs, where the loss had dropped from 8.00 to 5.35. These findings suggest that the features predicted by the theorem not only characterize the model dynamics during the early stage, but also remain informative well beyond it. We provide results for a BPE tokenization and for a causal analysis in Appendix B, and we elaborate experimental details for the TinyStories experiments in Appendix C.

the park little bird ball dog big tree man box red ball car dress balloon truck blocks apples shirt hat to the play go be help see her make do

(a) Examples for ¯B they she they he it one lily timmy tom her happy happy sad excited scared proud angry nice curious surprised wanted saw had wanted asked went loved ran looked took

(b) Examples for Σ¯ B fish fish big small pond lake water catch sea boat flower beautiful yellow butterfly hose garden bloom pretty daisy field birds bird tree up park nest flowers tweety sky flew

(c) Examples for ¯Φ

**Figure 5.** Selected tokens from the top 30 correlated tokens under different basis features from TinyStories. The characterized features actually capture both grammatical and semantic structures.

Semantic structure. To validate our interpretation of associative features, we collect for each token the top 30 most correlated tokens under each of the basis functions: the bigram mapping (¯B), interchangeability mapping (Σ¯B), and context matrix (¯Φ), constructed from the TinyStories corpus. We provide examples of tokens where the expected semantic relationships can be observed in Figure 5. Under ¯B, we see that the word “red” is correlated with common objects such as “truck”

<!-- Page 9 -->

Published as a conference paper at ICLR 2026 that would be described by the word “red”. Under ¯Φ, we can see that the word “fish” is correlated with common settings where fish would appear, such as “pond” or “lake”.

## 5.2 TRANSFORMERS IN PRACTICE

Setup. To evaluate how well our theoretical results extend to practical LLMs, we analyze token relationships learned from OpenWebText (Gokaslan et al., 2019), a real-world large-scale dataset with text from millions of webpages, in Pythia-1.4B (Biderman et al., 2023) and compare them with our theoretical predictions, examining how these relationships evolve across layers on datasets and models reflecting real-world complexities. We choose the Pythia model family, as they are opensourced and uniquely provide access to intermediate checkpoints, enabling fine-grained analysis of training dynamics and interpretability (Marks et al., 2024; Gallego-Feliciano et al., 2025). Unlike our theoretical setting, Pythia includes additional components such as MLP and multi-head attention, making it impossible to directly read off average token correlations from the weights. In order to interpret the layer-wise representations in terms of token-token correlations, we perform the analysis through the following steps:

1. We pass in each token ei as the input to the transformer.

2. For each token and from each layer l, we collect the following embeddings: the input to layer l hi,l,pre, the output of the l-th layer hi,l,post, and the output of the l-th layer without the MLP component hi,l,attn.1

## 3 The embeddings hi,l,pre form the rows of

El,pre ∈R|V|×d which represents a mapping from the input embeddings of layer l to tokens. Similarly, the embeddings hi,l,post and hi,l,attn form the rows of El,post ∈R|V|×d and El,attn ∈R|V|×d respectively.

Attention correlations. To analyze the correlations captured by the attention weights at each layer, we compute the product of the key and query mappings for each head and average these products, which we will call Al,emb ∈Rd×d. We then multiply the mapping El,pre on both sides of Al,emb to convert the average attention mapping into a token-basis attention weight matrix Al,tok. Finally, we consider token correlations captured by Al,tok by using its covariance matrix, which we compare with the covariance matrix of ¯Q, the leading-order attention mapping term from our theorem.

Embedding correlations. To analyze the correlations captured by the value mapping and the MLP, we consider the token-token correlations captured by the output of each layer. Utilizing the covariance matrix of El,post allows for direct comparison with the covariance matrix of the leading value matrix term ¯Φ⊤¯B⊤, since the matrices themselves have different dimensions. Furthermore, this enables us to control for shifts in the embedding space.

Comparison methodology. We compute the leading term matrices using 100K samples from OpenWebText. To control for differences in model architecture, we normalize each row of the leading term weights to have unit norm. Then, we compute cosine similarities between the corresponding covariance matrices across layers and across checkpoints. We perform the same analysis on the FineWeb (Penedo et al., 2024) dataset and provide results in Appendix B. More details on the experimental setup are in Appendix C.

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

Layer Number

Attention Mapping Cosine Similarity

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

Layer Number

No MLP Embedding Cosine Similarity

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

Layer Number

Embedding Mapping Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

Cosine Similarity Across Checkpoints

**Figure 6.** Cosine similarity between covariance matrices for Pythia-1.4B attention weights and embeddings and the corresponding leading term features based on OpenWebText.

1We remind the reader of each layer’s structure in the Pythia model. The input is normalized and then passed into the attention block and the MLP block in parallel. Then the outputs of each are added to the original input.

![Figure extracted from page 9](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-009-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-009-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-009-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 10 -->

Published as a conference paper at ICLR 2026

Results. We provide a visualization of results in Figure 6, where we can see that, at the early stage of training, there is very strong agreement between the Pythia embeddings and our leading-term features. We can see that for the embedding mapping, the token representations strongly match our theoretical analysis across all layers, and similarly for the attention weights, excluding only the first layer. We can see that as the model continues training, the weights gradually drift from fixed associative features to represent richer knowledge beyond association, starting with the earlier layers. However, it still maintains these features to a large extent for relatively longer steps. This suggests that our analysis on attention-based models generalizes with the addition of multi-head attention or MLP and acts as a starting point for a finer-grained analysis of full training dynamics.

MLP ablation. We perform an ablation at each layer by performing the embedding correlation analysis using El,attn, which is based on only the output of the attention block and excludes the MLP component. The results for this analysis can be seen in the middle plot of Figure 6. We can see that the correlations captured by embeddings with and without the MLP are similar except at the first layer. This suggests that at the first layer, the MLP maps tokens to embeddings with structures similar to that of the leading-order value matrix term and maintains a similar structure at later layers. Based on these initial results, one possible hypothesis is that the MLP at early stages functions similarly to the leading-term value mapping.

Individual attention heads. In order to capture a fine-grained understanding of the attention block, we perform the analysis on attention correlations using individual attention heads. We perform this analysis at an early (Layer 2), middle (Layer 13), and late layer (Layer 24) to also understand how heads may evolve differently at different stages of the model. In Figure 7, we find that different layers evolve differently with respect to the gradient leading-term for attention mappings. The earlier layers learn the leading-term features at a slower rate, as seen by the high similarity (red) appearing at later steps, especially for layer 2. We can also see that layer 13 exhibits faster specialization of attention heads than the other layers, as seen by the high variance in each column at later steps for layer 13. This provides insight into the rate of specialization of attention heads and suggests that intermediate layers are where specialization initially occurs.

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 11 12 13 14 15 16

Head Index

Layer 2

0

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 11 12 13 14 15 16

Head Index

Layer 13

1

2

4

8

16

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 11 12 13 14 15 16

Head Index

Layer 24

0.2

0.3

0.4

0.5

0.6

0.7

0.8

Cosine Similarity

Per-Head Attention Cosine Similarity Across Training Steps

**Figure 7.** Cosine similarity between covariance matrices for Pythia-1.4B individual attention head weights and the corresponding leading term features based on OpenWebText.

## 6 CONCLUSION

We present new theoretical results on the emergence of semantic associations in self-attention models learned from a natural language dataset. Our gradient leading term analysis for each model weight illuminates how the core basis functions that shape the associative features, i.e., bigram mapping, interchangeability mapping, and context mapping, develop from the training corpus. We show that transformer weights have closed-form expressions as compositions of those basis functions to represent semantic associations across natural language tokens. The extensive analyses on the weight matrices’ characterizations grounded by empirical supports from toy transformers and real-world LLMs contribute to the theoretical foundations of representation learning in transformers while also opening pathways for interpretability research: discovering common factors that allow weight matrices across components to be decomposed into simple functions of those shared factors; leveraging theory to formulate broad hypotheses about how concepts arise in models, extending beyond individual mechanisms or specific behaviors to complex characteristics.

![Figure extracted from page 10](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-010-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-010-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-010-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-010-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

ETHICS STATEMENT

We provide a novel theorem that characterizes the roles of weights in the transformer model, which is a de facto standard building block of modern LLMs. We try to uphold high standards of scientific excellence by making minimal assumptions for theoretical analysis while providing practical implications on mechanistic interpretability. The new insights on emerging features we presented contribute to a better understanding and diagnosis of the representation learning of transformers, which makes a big step towards transparent and reliable AI. As our study considers a setup of training from scratch on public datasets, there is no direct privacy issue and harm. The authors also acknowledge and respect the ethics of confidentiality and fairness, and confirmed that there are no identified violations of them.

REPRODUCIBILITY STATEMENT

All the theoretical analyses in this work are accompanied by full proofs with detailed step-by-step explanations (in the Appendix) for verification, reproduction, and reuse. We elaborate on the details of our setup in the main body of the paper for all empirical validations, and the code is available here. In addition, our choice of models pursues maximum reproducibility and accessibility, given its simple and fully open-sourced configurations.

## ACKNOWLEDGMENTS

The authors would like to thank James Oldfield, Wendi Li, and Jimmy Di for their valuable feedback. The work is supported in part by the AFOSR Young Investigator Program under award number FA9550-23-1-0184, National Science Foundation under awards IIS-2237037 and IIS-2331669, Office of Naval Research under grant number N00014-23- 1-2643, Schmidt Sciences Foundation, Open Philanthropy, Alfred P. Sloan Fellowship, and gifts from Google and Amazon. Zhen Fang was funded by the Australian Government through the Australian Research Council (ARC) under grant number DE250100363. Shawn Im is also supported by the National Science Foundation Graduate Research Fellowship Program under Grant No. 2137424. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation. Support was also provided by the Graduate School and the Office of the Vice Chancellor for Research at the University of Wisconsin-Madison with funding from the Wisconsin Alumni Research Foundation.

## REFERENCES

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Ale- man, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Jimmy Ba, Murat A Erdogdu, Taiji Suzuki, Zhichao Wang, Denny Wu, and Greg Yang. High- dimensional asymptotics of feature learning: How one gradient step improves the representation. Advances in Neural Information Processing Systems, 35:37932–37946, 2022.

Stella Biderman, Hailey Schoelkopf, Quentin Gregory Anthony, Herbie Bradley, Kyle O’Brien, Eric

Hallahan, Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, et al. Pythia: A suite for analyzing large language models across training and scaling. In International Conference on Machine Learning, pp. 2397–2430. PMLR, 2023.

Alberto Bietti, Joan Bruna, Clayton Sanford, and Min Jae Song. Learning single-index models with shallow neural networks. Advances in neural information processing systems, 35:9768–9783, 2022.

Alberto Bietti, Vivien Cabannes, Diane Bouchacourt, Herve Jegou, and Leon Bottou. Birth of a transformer: A memory viewpoint. Advances in Neural Information Processing Systems, 36: 1560–1588, 2023.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,

Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. Advances in neural information processing systems, 33:1877–1901, 2020.

Hugo Cui, Freya Behrens, Florent Krzakala, and Lenka Zdeborov´a. A phase transition between positional and semantic learning in a solvable model of dot-product attention. Advances in Neural Information Processing Systems, 37:36342–36389, 2024.

Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert Huben, and Lee Sharkey. Sparse autoen- coders find highly interpretable features in language models. arXiv preprint arXiv:2309.08600, 2023.

Alex Damian, Loucas Pillaud-Vivien, Jason D Lee, and Joan Bruna. The computational complexity of learning gaussian single-index models. arXiv preprint arXiv:2403.05529, 7, 2024.

Yatin Dandi, Florent Krzakala, Bruno Loureiro, Luca Pesce, and Ludovic Stephan. How two-layer neural networks learn, one (giant) step at a time. arXiv preprint arXiv:2305.18270, 2023.

Ezra Edelman, Nikolaos Tsilivis, Benjamin Edelman, Eran Malach, and Surbhi Goel. The evolution of statistical induction heads: In-context learning markov chains. Advances in Neural Information Processing Systems, 37:64273–64311, 2024.

Ronen Eldan and Yuanzhi Li. Tinystories: How small can language models be and still speak coherent english? arXiv preprint arXiv:2305.07759, 2023.

Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann,

Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, et al. A mathematical framework for transformer circuits. Transformer Circuits Thread, 1(1):12, 2021.

Joshua Engels, Eric J Michaud, Isaac Liao, Wes Gurnee, and Max Tegmark. Not all language model features are one-dimensionally linear. arXiv preprint arXiv:2405.14860, 2024.

John Rupert Firth. Papers in Linguistics 1934–1951. Oxford University Press, London, 1957.

Jorge Gallego-Feliciano, S Aaron McClendon, Juan Morinelli, Stavros Zervoudakis, and Antonios

Saravanos. Hidden dynamics of massive activations in transformer training. arXiv preprint arXiv:2508.03616, 2025.

Aaron Gokaslan, Vanya Cohen, Ellie Pavlick, and Stefanie Tellex. Openwebtext corpus. http:

//Skylion007.github.io/OpenWebTextCorpus, 2019.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad

Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.

Zellig S Harris. Distributional structure. Word, 10(2-3):146–162, 1954.

Geoffrey E Hinton. Distributed representations. 1984.

Ruiquan Huang, Yingbin Liang, and Jing Yang. Non-asymptotic convergence of training transform- ers for next-token prediction. Advances in Neural Information Processing Systems, 37:80634– 80673, 2025.

Yibo Jiang, Goutham Rajendran, Pradeep Ravikumar, Bryon Aragam, and Victor Veitch. On the origins of linear representations in large language models. In Proceedings of the 41st International Conference on Machine Learning, pp. 21879–21911, 2024.

Juno Kim and Taiji Suzuki. Transformers learn nonlinear features in context: nonconvex mean-field dynamics on the attention landscape. In Proceedings of the 41st International Conference on Machine Learning, pp. 24527–24561, 2024.

Juno Kim and Taiji Suzuki. Transformers provably solve parity efficiently with chain of thought. In

The Thirteenth International Conference on Learning Representations, 2025.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Beatrice Laurent and Pascal Massart. Adaptive estimation of a quadratic functional by model selec- tion. Annals of statistics, pp. 1302–1338, 2000.

Jason D Lee, Kazusato Oko, Taiji Suzuki, and Denny Wu. Neural network learns low-dimensional polynomials with sgd near the information-theoretic limit. Advances in Neural Information Processing Systems, 37:58716–58756, 2024.

Kenneth Li, Oam Patel, Fernanda Vi´egas, Hanspeter Pfister, and Martin Wattenberg. Inference-time intervention: Eliciting truthful answers from a language model. Advances in Neural Information Processing Systems, 36:41451–41530, 2023a.

Yuchen Li, Yuanzhi Li, and Andrej Risteski. How do transformers learn topic structure: Towards a mechanistic understanding. In Proceedings of the 40th International Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research, pp. 19689–19729. PMLR, 23–29 Jul 2023b.

Samuel Marks, Can Rager, Eric J Michaud, Yonatan Belinkov, David Bau, and Aaron Mueller.

Sparse feature circuits: Discovering and editing interpretable causal graphs in language models. arXiv preprint arXiv:2403.19647, 2024.

Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, and David Bau. Mass-editing memory in a transformer. arXiv preprint arXiv:2210.07229, 2022.

George A. Miller and Walter G. Charles. Contextual correlates of semantic similarity. Language and Cognitive Processes, 6(1):1–28, 1991.

Alireza Mousavi-Hosseini, Denny Wu, Taiji Suzuki, and Murat A Erdogdu. Gradient-based feature learning under structured data. Advances in Neural Information Processing Systems, 36:71449– 71485, 2023.

Neel Nanda, Lawrence Chan, Tom Lieberum, Jess Smith, and Jacob Steinhardt. Progress measures for grokking via mechanistic interpretability. arXiv preprint arXiv:2301.05217, 2023.

Eshaan Nichani, Alex Damian, and Jason D Lee. How transformers learn causal structure with gradient descent. In Proceedings of the 41st International Conference on Machine Learning, pp. 38018–38070, 2024.

Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom Henighan,

Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, et al. In-context learning and induction heads. arXiv preprint arXiv:2209.11895, 2022.

Guilherme Penedo, Hynek Kydl´ıˇcek, Loubna Ben allal, Anton Lozhkov, Margaret Mitchell, Colin

Raffel, Leandro Von Werra, and Thomas Wolf. The fineweb datasets: Decanting the web for the finest text data at scale. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2024. URL https://openreview.net/forum? id=n6SCkn2QaG.

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi

Zhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of machine learning research, 21(140):1–67, 2020.

Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhu- patiraju, L´eonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ram´e, et al. Gemma 2: Improving open language models at a practical size. arXiv preprint arXiv:2408.00118, 2024.

Yuandong Tian, Yiping Wang, Beidi Chen, and Simon S Du. Scan and snap: Understanding training dynamics and token composition in 1-layer transformer. Advances in neural information processing systems, 36:71911–71947, 2023.

Emanuele Troiani, Hugo Cui, Yatin Dandi, Florent Krzakala, and Lenka Zdeborov´a. Fundamental limits of learning in sequence multi-index models and deep attention networks: High-dimensional asymptotics and sharp thresholds. arXiv preprint arXiv:2502.00901, 2025.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Mingze Wang, Ruoxi Yu, Lei Wu, et al. How transformers implement induction heads: Approxima- tion and optimization analysis. arXiv preprint arXiv:2410.11474, 2024a.

Peng Wang, Yifu Lu, Yaodong Yu, Druv Pai, Qing Qu, and Yi Ma. Attention-only transformers via unrolled subspace denoising. arXiv preprint arXiv:2506.03790, 2025.

Zhichao Wang, Denny Wu, and Zhou Fan. Nonlinear spiked covariance matrices and signal propa- gation in deep neural networks. In The Thirty Seventh Annual Conference on Learning Theory, pp. 4891–4957. PMLR, 2024b.

Yiling Wu, Shuhui Wang, and Qingming Huang. Learning semantic structure-preserved embeddings for cross-modal retrieval. In Proceedings of the 26th ACM International Conference on Multimedia, MM ’18, pp. 825–833, New York, NY, USA, 2018. Association for Computing Machinery. ISBN 9781450356657.

An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,

Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025.

Hongru Yang, Bhavya Kailkhura, Zhangyang Wang, Yingbin Liang, et al. Training dynamics of transformers to recognize word co-occurrence via gradient flow analysis. Advances in Neural Information Processing Systems, 37:46047–46117, 2024.

Junjie Yao, Zhongwang Zhang, and Zhi-Qin John Xu. An analysis for reasoning bias of language models with small initialization. arXiv preprint arXiv:2502.04375, 2025.

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

A DETAILED DESCRIPTION ON WEIGHT CHARACTERIZATION

The token-to-token correlation captured by ¯Q is determined by how strongly correlated one token is with the other’s next-token distribution. These correlations are captured by Qi where each element Qijk of Qi measures for Xi, the correlation between the token at position j and the token at position k + 1. This correlation between the token at position j and position k + 1 gets mapped back to a correlation between the tokens at positions j and k through X⊤ i QiXi. let Qi given in Eq. (16) be the per-example correlation matrix computed from input–output token pairs in ith input,

¯Q = 1 NT

N X i=1

X⊤ i QiXi. (14)

We walk through an overview of the construction of Qi in four steps and provide the detailed computation in Appendix A.

Feature composition. As a preliminary step, we first define a composed feature Σ¯B ¯Φ by multiplying the interchangeability mapping Σ¯B with the context mapping ¯Φ. Each entry corresponds to the average product of path weights from token ei to ej with one step on Σ¯B and one step on ¯Φ. This composition utilizes local interchangeability to map a token to its more general functional class and utilizes the context-summary to capture longer-range semantic correlations shared by tokens in the functional class. We will refer to the resulting feature as the composed feature for simplicity in the remaining steps.

Scoring input–output pairs. For each input Xi and its corresponding output Yi, we utilize the composed feature, Σ¯B ¯Φ, to compute correlation scores between input and output tokens as seen in Figure 2.

(Yi −UO)Σ¯B ¯ΦX⊤ i, (15)

where UO is a baseline matrix with all elements set to 1/|V|. This assigns a correlation score to each input–output token pair according the composed feature.

Masking and centering. The auto-regressive constraint is enforced by masking future tokens, keeping only scores from input tokens that precede the output token. The resulting scores for each output token are centered and normalized based on its position. The matrix is then centered so that the scores for each output token sum to zero, yielding the per-example matrix Qi.

Qi = eintjk, tk→tj

Ji, (Yi −UO)Σ¯B ¯ΦX⊤ i

, (16)

where Ji is the masking operator and ein denotes an Einstein summation.

Next to Query Mapping. Lastly, the scores between each input and output token are then mapped to be the correlation between the input token and the token preceding the output token. In this way, the model learns to attend to the input token when it expects the next token to be the output token.

Aggregation across the dataset. Finally, we map per-example correlations back to the vocabulary space and average over all N inputs and T tokens per input:

¯Q = 1 NT

N X i=1

X⊤ i QiXi. (17)

In this way, each token is associated with the average correlations to other tokens across the dataset.

B ADDITIONAL EXPERIMENTS

BPE tokenization. We train a 3-layer attention-based model on TinyStories as in Section 5.1 using a BPE tokenization with vocabulary size of 10,000. We train the model for 10 epochs with a learning rate of 0.005 and measure the cosine similarity between the theoretical and actual weights. We report the minimum over the 10 epochs in Table 2.

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

Weights Min. Cosine

Attention 0.999914 Value 0.998800 Output 0.997891

**Table 2.** Minimum cosine similarities between theoretical and actually learned weights across all epochs. Results from a 3-layer attention-based model trained on TinyStories and with a BPE tokenization.

Causal intervention. We aim to understand how the model output changes when removing the leading terms from each of the weights. We perform this analysis on the 3-layer attention-based transformers trained on TinyStories with a learning rate of 0.05. Unlike most causal intervention settings, the features considered have a general function rather than a specific function applicable to a narrower setting, and therefore, we expect removing the leading terms to result in performance degradation across the dataset. As a result, we choose to focus on the extent to which the output distribution changes when the leading term component is removed for each weight matrix. For each weight matrix, we remove the projection of the weight matrix onto its corresponding leading term. After removing this projection, we compute the loss of the resulting model on the dataset. We provide the results of this intervention in Table 3. We can see that the output layer has the largest effect on the loss, while the attention weights have the least. This behavior is predicted by the theory as the output layer has the largest order update, while the attention weights have the smallest order updates.

Weights Loss

Original 5.349 Attention Layer 0 5.350 Attention Layer 1 5.352 Attention Layer 2 5.361 Value Layer 0 6.192 Value Layer 1 6.526 Value Layer 2 6.520 Output 8.287

**Table 3.** Loss of the attention-based model on TinyStories after the leading term component from each weight matrix is removed. The first row corresponds to the original model.

Validation on additional dataset. We perform the analysis in Section 5.2 on the token-token correlations captured by embeddings in Pythia-1.4B except instead of using OpenWebText, we use FineWeb (Penedo et al., 2024). We provide the results in Figure 8 where we see very similar results as with OpenWebText.

1

2

4

8

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 19 20 21 22 23 24

Layer Number

Attention Mapping Cosine Similarity

1

2

4

8

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 19 20 21 22 23 24

Layer Number

No MLP Embedding Cosine Similarity

1

2

4

8

32

64

128

256

512

Training Step

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 19 20 21 22 23 24

Layer Number

Embedding Mapping Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

0.0

0.2

0.4

0.6

0.8

1.0

Cosine Similarity

Cosine Similarity Across Checkpoints (FineWeb)

**Figure 8.** Cosine similarity between covariance matrices for Pythia-1.4B attention weights and embeddings and the corresponding leading term features based on FineWeb.

![Figure extracted from page 16](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-016-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-016-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICLR-how-do-transformers-learn-to-associate-tokens-gradient-leading-terms-bring-mecha/page-016-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 17 -->

Published as a conference paper at ICLR 2026

C EXPERIMENTAL DETAILS

TinyStories Experiments We collect the vocabulary from TinyStories treating each word, punctuation mark, or number as a token and use the 3000 most common tokens. We then filter out samples that include tokens outside of the set of 3000. For training, we use 65536 of the filtered samples with sequence length at least 201 and truncate all sequences to 201 tokens for training and computing theoretical leading terms. For the BPE tokenization, we tokenize the dataset using a vocabulary size of 10,000, and for training, we use samples with sequence length at least 201 and truncate all sequences to 201 tokens for training and computing theoretical leading terms. We compute the theoretical matrices using the first batch.

Pythia Experiments We use the first 100k samples of OpenWebText/FineWeb with length at least 512 characters to perform the analysis.

We utilize 4 A100 GPUs with 80GB of memory. These experiments can be performed with less compute by reducing batch size or sequence length.

D PROOFS

∥·∥will be the operator norm unless denoted otherwise.

D.1 PROOF OF 1-LAYER THEOREM

Lemma D.1 (General Gradient Form). Under the setting described, we have that

∂L ∂WO

= −1

NT

N X i=1 h(1)⊤ i Ri (18)

∂L ∂V (1) = −1

NT

N X i=1

X⊤ i A(1)⊤ i RiW ⊤

O (19)

∂L ∂W (1) = −1

NT

N X i=1

X⊤ i eintjk,tk→tj(Ji, (RiW ⊤

O V (1)⊤X⊤ i))Xi (20)

∂L ∂P (1) = −1

NT eintjk,jk→t

D,

N X i=1 eintjk,tk→tj(Ji, (RiW ⊤

O V (1)⊤X⊤ i))

!

(21)

where A(1)

i = S(Mask(XiW (1)X⊤ i + DM(P (1)))), Ri = Yi −S(Fθ(Xi)), Ji ∈RT ×T ×T with Ji,t = Diag(A(1)[t]

i) −A(1)[t]⊤ i A(1)[t]

i being the Jacobian of the softmax function for the tth token in the sequence, D ∈RT ×T ×T with Dt being a matrix with ones along the (−t + 1)th sub-diagonal and zeros elsewhere, and ein is used to denote an Einstein summation.

Proof. We start by considering the derivative of the loss with respect to Fθ(Xi)[t] which is

Y [t]

i −S(Fθ(Xi)[t]) (22)

and derivative of Fθ(Xi)[t] with respect to WO is h(1)[t]

i. Then it follows that

∂L ∂WO

= −1

NT

N X i=1 h(1)⊤ i Ri (23)

Now, we consider the gradient with respect to V (1) using the chain rule which gives

∂L ∂V (1) = −1

NT

N X i=1

X⊤ i A(1)⊤ i RiW ⊤

O (24)

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

Now, we consider the gradient with respect to A(1)

i as an intermediate step towards the gradient with respect to W (1), P (1). Using the chain rule as before, we have

∂L

∂A(1)

i

= −1

NT RiW ⊤

O V (1)⊤X⊤ i. (25)

Letting B(1)

i = XiW (1)X⊤ i + DM(P (1)), we have that the derivative of A(1)[t]

i with respect to B(1)[t]

i is

Ji,t = Diag(A(1)[t]

i) −A(1)[t]⊤ i A(1)[t]

i (26)

Then, in order to get the gradient of the loss with respect to B(1)

i, we need to consider the contribution from each t resulting in the Einstein summation

∂L

∂B(1)

i

= −1

NT eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i) (27)

From the chain rule, we can derive the gradient with respect to both W (1) and P (1).

∂L ∂W (1) = −1

NT

N X i=1

X⊤ i eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)Xi (28)

∂L ∂P (1) = −1

NT eintjk,jk→t

D,

N X i=1 eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)

!

(29)

where Dt has ones along the (−t + 1)th sub-diagonal and zeros elsewhere. This completes the proof.

Lemma D.2 (Local softmax Jacobian bound). Let S denote the softmax map. Then for every z ∈Rd,

∥∇S(z)∥≤max

1≤j≤d S(z)j ≤exp(range(z)) d, where range(z):= max j zj −min j zj.

For any z such that range(z) ≤r

S(z) −1 d1

≤er d ∥z∥.

Proof. Let p = S(z). The Jacobian of softmax is

∇S(z) = Diag(p) −pp⊤.

For any x ∈Rd, x⊤∇S(z)x = d X j=1 pjx2 j −



 d X j=1 pjxj





2

.

The second term is nonnegative, so x⊤∇S(z)x ≤ d X j=1 pjx2 j ≤ max j pj

∥x∥2

2.

Since ∇S(z) is symmetric positive semidefinite, this implies

∥∇S(z)∥2→2 ≤max j pj.

It remains to bound maxj pj. Let M = maxj zj and m = minj zj. Then for every j, pj = ezj Pd k=1 ezk ≤eM dem = eM−m d = erange(z)

d.

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

Therefore

∥∇S(z)∥2→2 ≤erange(z)

d.

Now let γ(τ) = z′ + τ(z −z′) for τ ∈[0, 1]. By the fundamental theorem of calculus,

S(z) −S(z′) =

Z 1

0 ∇S(γ(τ))(z −z′) dτ.

If range(γ(τ)) ≤r for all τ ∈[0, 1], then

∥S(z) −S(z′)∥2 ≤

Z 1

0 ∥∇S(γ(τ))∥2→2 dτ ∥z −z′∥2 ≤er d ∥z −z′∥2.

Taking z′ = 0 gives the final claim, since S(0) = 1 d1 and range(τz) = τ range(z) ≤range(z).

Corollary D.3 (Local softmax bound from an ℓ∞bound). Let S: Rd →∆d−1 denote the softmax map. If ∥z∥∞≤R, then S(z) −1 d1

2 ≤e2R d ∥z∥2.

In particular, if ∥z∥∞≤1

2, then S(z) −1 d1

2 ≤e d∥z∥2.

Proof. If ∥z∥∞≤R, then range(z) = max j zj −min j zj ≤2∥z∥∞≤2R.

Applying Lemma D.2 with r = 2R gives

S(z) −1 d1

2 ≤e2R d ∥z∥2.

The final claim follows by taking R = 1

2.

Lemma D.4 (First Gradient Step). Under the setting described, after one gradient step, we have that

WO = η(¯B) (30)

W (1), V (1), P (1) = 0 (31)

where ¯B a |V | × |V | matrix where the jth row is the average next-token distribution of the jth token in the vocabulary weighted by the relative frequency of token j across the dataset and centered to have the row sum be 0.

Proof. From Lemma D.1, as the parameters are initially zero, we can see that W (1), V (1), P (1) all have gradients of zero and therefore remain as 0. For WO, as the value matrix is initially zero, h(1)

i = Xi and as WO is zero, the output distribution for every token is the uniform distribution. Let UO ∈RT ×|V | represent the resulting output with each element 1/|V |. Then, we have that

∂L ∂WO

= −1

NT

N X i=1

X⊤ i (Yi −UO) (32)

We consider the sum of each of the terms X⊤ i Yi and X⊤ i UO. First, we consider the sum of X⊤ i Yi. The jth row of X⊤ i Yi is a |V |-dimensional vector with each element being the number of times the corresponding token appears after each occurrence of the jth token in the vocabulary in Xi. Then,

<!-- Page 20 -->

Published as a conference paper at ICLR 2026 summing over all i and dividing by NT results in each row mapping to the average next-token distribution weighted by the frequency of the token corresponding to the row. We can write this as

B = 1 NT

N X i=1

X⊤ i Yi =



 α1P1 α2P2

... α|V |P|V |



 (33)

where αj is the relative frequency of the jth token in the dataset and Pj is the average next-token distribution for token j. For the sum X⊤ i UO divided by NT, we simply get that every row is αj times the uniform distribution over the vocabulary, and we will denote this matrix by U. Then, we have that

∂L ∂WO

= −(B −U) (34)

and therefore after the first step,

WO = η(B −U) (35)

Then, as ¯B = B −U, this completes the proof.

Lemma D.5 (Second Gradient Step). Under the setting described, and with η ≤1, |V | ≥8, after two gradient steps, we have that

WO −2η ¯B

F ≤ η2 p

|V |

(36)

V (1) −η2 ¯Φ⊤¯B⊤

F ≤ 2η3 p

|V |

(37)

W (1), P (1) = 0 (38)

where ¯B is as defined in the previous lemma and ¯Φ is given by

¯Φjk = P(ek →ej) −µΦ,k (39)

where P(ek →ej) corresponds to the empirical probability that ej is the current token and ek is in its prefix and µΦ,k is the value that sets each column sum to 0.

Proof. First, as V (1) remains at zero after the first step, we have that the gradients for W (1), P (1) are zero and therefore, they remain at zero after the second step. We now consider the forward pass after the first gradient step. As the value matrix remains as zero, we have that

Fθ(Xi) = ηXi ¯B (40)

For each row t, let fi,t = Fθ(Xi)[t,:]. Since Fθ(Xi) = ηXi ¯B, each row fi,t is equal to η times a row of ¯B. Since each row of ¯B is a frequency-weighted centered probability vector, it has a range of at most 1. Hence range(fi,t) ≤η ≤1.

By Lemma D.2, applied rowwise,

S(fi,t) −1

|V |1

≤ e |V |∥fi,t∥.

Summing over rows gives

∥S(Fθ(Xi)) −UO∥F ≤ e |V | ∥Fθ(Xi)∥F = eη

|V |

Xi ¯B

F ≤eη

√

T |V |. (41)

Then, as |V | ≥8, we have that

∥Ri −(Yi −UO)∥F ≤η

√

T p

|V |

(42)

<!-- Page 21 -->

Published as a conference paper at ICLR 2026 and by Lemma D.1 and that ∥Xi∥≤

√

T, we have

∂L ∂WO

+ ¯B

F

≤ 1 NT

N X i=1 ηT p

|V |

= η p

|V |

(43)

Then, it follows that after the second gradient step,

WO −2η ¯B

F ≤ η2 p

|V |

(44)

Now, we consider the gradient with respect to V (1). By Lemma D.1, we have that

∂L ∂V (1) = −1

NT

N X i=1 ηX⊤ i A(1)⊤ i (Yi −S(Fθ(Xi))) ¯B⊤ (45)

and since W (1), P (1) = 0, A(1)

i = A0 where the tth row of A0 has the first t elements equal to 1/t and the rest equal to 0. Then, by equation 41, we have that ηX⊤ i A⊤

0 (Yi −S(Fθ(Xi))) ¯B⊤−ηX⊤ i A⊤

0 (Yi −UO) ¯B⊤ F ≤η2T p

|V |

∥A0∥ (46)

Then, using the discrete Hardy’s inequality with p = 2, we have that ∥A0∥≤2 and

∂L ∂V (1) + 1 NT

N X i=1 ηX⊤ i A⊤

0 (Yi −UO) ¯B⊤

F

≤ 2η2 p

|V |

(47)

Now, we will analyze

1 NT

N X i=1 ηX⊤ i A⊤

0 (Yi −UO) ¯B⊤ (48)

Since η ¯B is independent of i, we can move it outside the sum and we can analyze

1 NT

N X i=1

X⊤ i A⊤

0 (Yi −UO) (49)

We start by considering the form of X⊤ i A⊤

0. Since the tth row of A0 has 1/t as the first t elements and zeros for all other elements, we have that the jth element of the tth column of X⊤ i A⊤

0 is γi(ej, t)

t (50)

where ej represents the jth token in the vocabulary and γi(ej, t) is the number of occurrences of ej in the first t tokens of Xi. Letting Φ′ = 1 NT

PN i=1 X⊤ i A⊤

## 0 Yi, we have that

Φ′ jk = 1 NT

N X i=1

T X t=1

1(X[t+1] i = ek)γi(ej, t)

t (51)

Swapping the order of the sums, we have

Φ′ jk = 1 NT

T X t=1

1 t

N X i=1

1(X[t+1] i = ek)γi(ej, t) (52)

Then, as γi(ej, t) = Pt m=1 1(X[m]

i = ej), we have that

Φ′ jk = 1

T

T X t=1

1 t t X m=1

1 N

N X i=1

1(X[t+1] i = ek, X[m]

i = ej) (53)

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

Then, as 1 N

PN i=1 corresponds to an average over the dataset, the average over N corresponds to the empirical probability of having a sequence with the t + 1th token equal to ek and the mth token equal to ej, which we will denote as P(xt+1 = ek, xm = ej). Then, this gives

Φ′ jk = 1

T

T X t=1

1 t t X m=1

P(xt+1 = ek, xm = ej) (54)

Then, we have an average over m ∈[t] which results in the average probability that the t+1th token is ek and ej is in the first t tokens. We will denote this as P(ej ∈x1:t, xt+1 = ek). This gives

Φ′ jk = 1

T

T X t=1

P(ej ∈x1:t, xt+1 = ek) (55)

This probability of ej being in the prefix of xt+1 = ek is averaged over the different positions of ek to get an average probability that ej is in the prefix given that ek is the current token, which we will denote as P(ej →ek) and

Φ′ jk = P(ej →ek) (56)

Now, we consider UP = 1 NT

PN i=1 X⊤ i A⊤

0 UO. Then, we have that

UPjk = 1 NT

N X i=1

T X t=1 γi(ej, t)

|V |t (57)

Rearranging the sum and decomposing γi, we get

UPjk = 1

T

T X t=1

1 t|V | t X m=1

P(xm = ej) (58)

Then, if we consider the average over positions m and t, we get the average probability that ej is in the first t tokens over all t multiplied by 1/|V |. We can notice that the sum of the jth row of UP and Φ′ are the same. Then, setting

¯Φ′ = Φ′ −UP (59)

we have

∂L ∂V (1) + η¯Φ′ ¯B⊤

F

≤ 2η2 p

|V |

(60)

Then, it follows that after two gradient steps,

V (1) −η2 ¯Φ′ ¯B⊤

F ≤ 2η3 p

|V |

(61)

Defining ¯Φ = ¯Φ′⊤, we have V (1) −η2 ¯Φ⊤¯B⊤

F ≤ 2η3 p

|V |

(62)

This completes the proof.

Lemma D.6 (Third Gradient Step). Under the setting described, and with η ≤1/8, |V | ≥500, after three gradient steps with η, we have that

WO −3η ¯B

F ≤3η2 (63) V (1) −3η2 ¯Φ⊤¯B⊤

F ≤2η3 (64) W (1) −2η4 ¯Q

F ≤2η5T (65) P (1) −2η4∆

F ≤2η5T (66)

<!-- Page 23 -->

Published as a conference paper at ICLR 2026

Proof. First, we start with bounding the norm of WO, V (1), A0. We have that

∥WO∥F ≤2η + η2 p

|V |

(67)

V (1) ≤

2η2 + 2η3 p

|V |

!

(68)

∥A0∥≤2 (69)

Now, we consider the deviation of the output from the uniform distribution. We start by bounding the norm of Xi + A0XiV (1)

Xi + A0XiV (1) ≤

1 + 5η2 √ T (70)

Then, we can upper bound the norm of Fθ(Xi) as

∥Fθ(Xi)∥F ≤5η

2

1 + 5η2 √ T ≤4η

√

T, (71)

where the last inequality uses η ≤1/8. Let

Hi = Xi + A0XiV (1).

For each row t, write fi,t = Fθ(Xi)[t,:] = H[t,:]

i WO. Using the bounds above, H[t,:]

i

≤1 + 5η2, ∥WO∥≤∥WO∥F ≤5η

2.

Therefore

∥fi,t∥2 ≤5η

2 (1 + 5η2).

Hence, since η ≤1/8, range(fi,t) ≤2 ∥fi,t∥2 ≤1.

By Lemma D.2, applied rowwise,

S(fi,t) −1

|V |1

≤ e |V | ∥fi,t∥.

Summing over rows gives

∥S(Fθ(Xi)) −UO∥F ≤ e |V | ∥Fθ(Xi)∥F ≤4eη

√

T |V | ≤4η

√

T p

|V |

, (72)

where the last inequality uses |V | ≥8. Then, it follows that

∂L ∂WO

+ ¯B

F

≤ 1 NT

N X i=1

8ηT p

|V |

+ 5η2T

!

≤2η (73)

and

WO −3η ¯B

F ≤ η2 p

|V |

+ 2η2 ≤3η2 (74)

Now, we consider the gradient with respect to V (1). Since ∥Yi −S(Fθ(Xi))∥≤

√

2T, we have that

∂L ∂V (1) + 2η¯Φ⊤¯B⊤

F

≤2

4η p

|V |

5η 2 + η2 p

|V |

!

≤22η2 p

|V |

≤η2 (75)

Then, we have that after the third step,

V (1) −3η2 ¯Φ⊤¯B⊤

F ≤2η3 (76)

<!-- Page 24 -->

Published as a conference paper at ICLR 2026

Now, we consider the gradient with respect to W (1), P (1) which according to Lemma 1.1 are

∂L ∂W (1) = −1

NT

N X i=1

X⊤ i eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)Xi (77)

∂L ∂P (1) = −1

NT eintjk,jk→t

D,

N X i=1 eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)

!

(78)

We start by analyzing RiW ⊤

O V (1)⊤X⊤ i. First, We will use that ∥Yi −UO∥≤

√

T and ¯Φ

≤1

T max i ∥Xi∥∥A0∥∥Yi −UO∥≤2

T T = 2 (79)

We know by the previous lemma and the bound on the deviation of the output that

RiW ⊤

O V (1)⊤X⊤ i −2η3(Yi −UO) ¯B⊤¯B ¯ΦX⊤ i

F ≤25η4T p

|V |

+ 5Tη4

2 p

|V |

+ 4η4T p

|V |

≤3η4T

2 (80)

We start by considering the structure of Yi ¯B⊤¯B ¯ΦX⊤ i. We first consider the simpler multiplication of ej ¯B⊤¯B ¯Φe⊤ k. First, we define Σ ¯ B = ¯B⊤¯B which has Σ ¯ Bmn = P|V | l=1 α2 l ¯Plm ¯Pln where αl is the relative frequency of token l and ¯Pl is the average next-token distribution of token el centered at 0. This corresponds to a similarity measure of the previous tokens of em and en with common tokens more heavily weighted. Then, we have that ejΣ ¯ B ¯Φe⊤ k =

|V | X m=1

Σ ¯ Bjm ¯P(em →ek) (81)

where ¯P(em →ek) is the probability that em is in the prefix of ek centered at 0. We can then interpret the each element (Σ ¯ B ¯Φ)jk as a measure of assocation between token j and k based on a two-step chain of (interchangeability mapping, suffix token mapping). Essentially, how often does token ek succeed token ej and similar tokens. We will let ¯G = Σ ¯ B ¯Φ. Now, we can consider 2η3Yi ¯GX⊤ i. This results in a T × T matrix where the jk-th element is ˜P(X[k]

i →2 X[j+1]

i) and we will denote this as gijk. Then, 2η3(Yi −UO) ¯GX⊤ i will have elements centered to have row sums of 0 and we will let the centered elements be ¯gijk. Then, we consider the einsum of J and 2η3(Yi −UO) ¯GX⊤ i. The tth column of the resulting matrix will the be product of Jt and the tth column of 2η3(Yi −UO) ¯GX⊤ i. This results in the tth row having the form

2η3



       





¯gi1t t... ¯gitt t0... 0





−



 µg,it t... µg,it t0... 0







       

⊤

(82)

The tth row is 2η3¯gijt for 1 ≤j ≤t weighted by 1/t and centered to have a row sum of 0 and we will refer to the centered and weighted elements 2η3qijt and the resulting matrix Qi. Letting

¯Q = 1 NT

PN i=1 X⊤ i QiXi, we have that

∂L ∂W (1) + 2η3 ¯Q

F

≤2η4T (83)

where we have used that the squared Frobenius norm of the einsum is the sum of the norms of each column and that ∥Jt∥= 1/t. Then, it follows that

W (1) −2η4 ¯Q

F ≤2η5T (84)

Now, we consider the gradient with respect to each element of P (1)

∂L

∂P (1)

m

+ 2η3

NT

N X i=1

Tr(D−mQi)

F

≤2η4√

T (85)

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

Since the trace is a linear function, we let ∆m = Tr(D−m 1 NT

PN i=1 Qi) and let ∆be the vector consisting of ∆m, and we have

∂L ∂P (1) + 2η3∆

F

≤2η4T (86)

and it follows that P (1) −2η4∆

F ≤2η5T (87)

This completes the proof.

Theorem D.7 (Early Stage Features). Under the setting described, for s ≤η−1 3 8T 3/8, for T ≥ 3, |V | ≥500, we have that after s gradient descent steps with learning rate η, WO −sη ¯B

F ≤3s2η2 (88) V (1) − s

2 η2 ¯Φ⊤¯B⊤

F

≤4s3η3 (89) W (1) −

3 s

4

+ 2 s

3 η4 ¯Q

F

≤6s5η5T (90) P (1) −

3 s

4

+ 2 s

3 η4∆

F

≤6s5η5T (91)

Proof. We will prove the result by induction. The previous lemmas form the base case. The first phase will be bounding the deviation of the output from the uniform distribution after s gradient steps. To start, we bound the norm of Ai, the resulting attention mapping for Xi. For the tth row, define zi,t:= (XiW (1)X⊤ i + DM(P (1)))[t,: t].

By the inductive hypotheses for W (1) and P (1),

∥zi,t∥∞≤

6 s

4

+ 4 s

3 η4 + 12s5η5T.

Using 6 s

4

+ 4 s

3

≤2s4 and sη ≤3/(8T 3/8), the right-hand side is bounded by an absolute constant smaller than 1/2. Hence range(zi,t) ≤2∥zi,t∥∞≤1.

By Lemma D.2,

∥(Ai −A0)[t,:]∥≤e t ∥zi,t∥.

Moreover,

∥zi,t∥≤

√ t

6 s

4

+ 4 s

3 η4 + 12s5η5T

.

Therefore

∥(Ai −A0)[t,:]∥≤e

6 s

4

+ 4 s

3 η4 + 12e s5η5T √ t.

Then, summing the upper bounds on the squared norms of each row, and using that Pr q=1 1/q ≤ 1 + log r we have

∥Ai −A0∥F ≤e

6 s

4

+ 4 s

3 η4√

T + 12es5η5T p

1 + log T (92)

Then, we have that

A(1)

i

≤2 + e

6 s

4

+ 4 s

3 η4√

T + 12es5η5T p

1 + log T (93)

Then, upper bounding 6 s

4

+ 4 s

3 by 2s4, we have A(1)

i

≤2 + 2es4η4√

T + 12es5η5T p

1 + log T (94)

<!-- Page 26 -->

Published as a conference paper at ICLR 2026

Now, using that sη ≤ 3 8T 3/8, we have that

2es4η4√ T + 12es5η5T p

1 + log T ≤2sη (95)

and A(1)

i

≤2 + 2sη (96)

Now, we bound the norm of V (1) which by the inductive hypothesis we have is at most s

2 η22

√

2 + 4s3η3 (97)

which is at most s2η2√

2 + 4s3η3 (98)

and since sη ≤1

3, V (1)

F ≤4s2η2 (99)

Then, we have that Xi + A(1)

i XiV (1)

F ≤

√

T

1 + 16s2η2 (100)

Since sη ≤ 3 8T 3/8 and by the inductive hypothesis we have that

∥Fθ(Xi)∥F ≤2

√

T sη + 3s2η2

(101)

Since sη ≤ 3 8T 3/8, we have ∥Fθ(Xi)∥F ≤4sη

√

T (102)

Let

Hi:= Xi + A(1)

i XiV (1).

For each row t, write fi,t:= Fθ(Xi)[t,:] = H[t,:]

i WO.

Since A(1)

i [t,:]Xi is a convex combination of one-hot vectors,

H[t,:]

i

≤1 +

V (1) ≤1 + 4s2η2.

Also, by the inductive hypothesis and

¯B

F ≤1,

∥WO∥≤∥WO∥F ≤sη + 3s2η2.

Thus

∥fi,t∥≤(1 + 4s2η2)(sη + 3s2η2).

Using sη ≤3/(8T 3/8) and T ≥3, this is bounded by 1, and hence range(fi,t) ≤2 ∥fi,t∥≤2.

By Lemma D.2, applied row-wise,

S(fi,t) −1

|V |1

≤e2

|V | ∥fi,t∥.

Summing over rows gives

∥S(Fθ(Xi)) −UO∥F ≤e2

|V | ∥Fθ(Xi)∥F ≤4e2sη

√

T |V |.

Since |V | ≥500, we have e2/ p

|V | ≤1, and therefore

∥S(Fθ(Xi)) −UO∥F ≤4sη s

T |V |.

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

Now, we will utilize the bound on the deviation of the output from the uniform distribution as well to perform the inductive step for WO. We have based on the bound that after the (s + 1)th step

∂L ∂WO

+ ¯B

F

≤ 8sη p

|V |

+ 12s2η2 ≤6sη (103)

Then, after (s + 1) steps, we have that

WO −(s + 1)η ¯B

F ≤3η2s2 + 6sη2 ≤3η2(s + 1)2 (104)

Now, we perform the inductive step for V (1) using the bound on the deviation of the attention pattern and on the output deviation. We have that after the (s + 1)th step

∂L ∂V (1) + sη¯Φ⊤¯B⊤

F

≤∥Ri −(Yi −UO)∥F

A(1)

i

∥Xi∥∥WO∥

+ ∥(Yi −UO)∥

A(1)

i −A0

F ∥Xi∥∥WO∥

+ ∥(Yi −UO)∥∥A0∥∥Xi∥

WO −sη ¯B

F (105)

Applying upper bounds and using that |V | ≥500, we have

∂L ∂V (1) + sη¯Φ⊤¯B⊤

F

≤1

T

24sη p

|V |

Tηs + 4Ts2η2 + 6Ts2η2

!

≤12s2η2 (106)

Then, after (s + 1) steps, we have that

V (1) − s + 1

2 η2 ¯Φ⊤¯B⊤

F

≤4s3η3 + 12s2η3 ≤4(s + 1)3η3 (107)

Now, we perform the inductive step for W (1) utilizing the earlier bounds on the output and attention pattern deviations. We start by bounding the deviation between s3−s2

2 η3Σ ¯ B ¯Φ and W ⊤

O V (1)⊤. By the inductive hypothesis and 2 ≤ p

|V |, we have that W ⊤

O V (1)⊤−s3 −s2

2 η3Σ ¯ B ¯Φ

F

≤8s4η4 + 3

√

2s4η4 ≤13s4η4 (108)

Then, for each RiW ⊤

O V (1)⊤X⊤ i since |V | ≥500, we have that RiW ⊤

O V (1)⊤X⊤ i −s3 −s2

2 η3(Yi −UO)Σ ¯ B ¯ΦX⊤ i

F

≤20s4η4T p

|V |

+ 13s4η4T ≤14s4η4T

(109) Now, in order to consider the deviation of the einsum of J and s3−s2

2 η3(Yi −UO)Σ ¯ B ¯ΦX⊤ i, we need to first bound the deviation of the Jacobian of the current attention pattern from J. We do so by considering the deviation for each Jt. As proven earlier, we have that

∥(Ai −A0)[t,:]∥≤e

6 s

4

+ 4 s

3 η4 + 12es5η5T √ t (110)

Then, we have that for the current Jacobian for the sample Xi corresponding to the tth row which will call Jt,i

Jt,i −Jt = Diag(Ai[t,:] −A0[t,:]) −A0[t,:](Ai[t,:] −A0[t,:])⊤−(Ai[t,:] −A0[t,:])A0[t,:]⊤

−(Ai[t,:] −A0[t,:])(Ai[t,:] −A0[t,:])⊤ (111)

and it follows then that for t ≥2

∥Jt,i −Jt∥2 ≤∥Ai[t,:] −A0[t,:]∥∞+ 2 √ t ∥Ai[t,:] −A0[t,:]∥2 + ∥Ai[t,:] −A0[t,:]∥2

2 (112)

Then, as

∥Ai[t,:] −A0[t,:]∥∞≤∥Ai[t,:] −A0[t,:]∥2 (113)

<!-- Page 28 -->

Published as a conference paper at ICLR 2026 we have that

∥Jt,i −Jt∥2 ≤ e

6 s

4

+ 4 s

3 η4 + 12es5η5T √ t

1 + 2 √ t +

6 s

4

+ 4 s

3 η4 + 12s5η5T √ t

(114)

Since J1,i is always all zeros, we can ignore this term and for t ≥2, we have that as sη ≤ 3 8T 3/8,

∥Jt,i −Jt∥2 ≤5s2η2 (115)

Then, we have that s3 −s2

2 η3Qi −eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)

F

≤∥Ji −J∥2 s3 −s2

2 η3(Yi −UO)Σ ¯ B ¯ΦX⊤ i

F

+ ∥Ji∥2

RiW ⊤

O V (1)⊤X⊤ i −s3 −s2

2 η3(Yi −UO)Σ ¯ B ¯ΦX⊤ i

F

(116)

Then, as ∥Jt∥2 = 1 t, ∥Ji∥2 ≤3

2 + 5s2η2√ T ≤2, and sη ≤ 3 8T 3/8, we have that s3 −s2

2 η3Qi −eintjk,tk→tj(Ji, RiW ⊤

O V (1)⊤X⊤ i)

F

≤5

√

2s5η5T +28s4η4T ≤30s4η4T

(117)

Then, we have that

∂L ∂W (1) + s3 −s2

2 η3 ¯Q

F

≤30s4η4T (118)

Then, we have that after (s + 1) steps,

W (1) −

3 s + 1

4

+ 2 s + 1

3 η4 ¯Q

F

≤6s5η5T + 30s4η5T ≤6(s + 1)5η5T (119)

Finally, as we have the bound on the deviation from Qi, we have that for P (1),

∂L ∂P (1) + s3 −s2

2 η3∆

F

≤30s4η4T (120)

and that after (s + 1) steps,

P (1) −

3 s + 1

4

+ 2 s + 1

3 η4∆

F

≤6s5η5T + 30s4η5T ≤6(s + 1)5η5T (121)

D.2 PROOF OF MULTI-LAYER THEOREM

Lemma D.8 (General Gradient Form). Under the setting described, defining

S(l)

i = eintjk, tk→tj

J(l)

i, G(l)

i V (l)⊤h(l−1)⊤ i

, (122)

G(l−1)

i = G(l)

i + A(l)⊤ i G(l)

i V (l)⊤+ S(l)

i h(l−1)

i W (l)⊤+ S(l)⊤ i h(l−1)

i W (l), (123) with

G(L)

i = RiW ⊤

O (124) we have that

∂L ∂WO

= −1

NT

N X i=1 h(L)⊤ i Ri, (125)

<!-- Page 29 -->

Published as a conference paper at ICLR 2026

∂L ∂V (l) = −1

NT

N X i=1 h(l−1)⊤ i A(l)⊤ i G(l)

i, (126)

∂L ∂W (l) = −1

NT

N X i=1 h(l−1)⊤ i S(l)

i h(l−1)

i, (127)

∂L ∂P (l) = −1

NT eintjk, jk→t

D,

N X i=1

S(l)

i

!

, (128)

where A(l)

i = S(Mask(h(l−1)

i W (l)h(l−1)⊤ i + Dm(P (l)))), Ri = Yi −S(Fθ(Xi)), J(l)

i ∈RT ×T ×T with J(l)

i,t = Diag(A(l)[t]

i) −A(l)[t]⊤ i A(l)[t]

i being the Jacobian of the softmax function at the lth attention layer for the tth token in the sequence, D ∈RT ×T ×T with Dt being a matrix with ones along the (−t + 1)th sub-diagonal and zeros elsewhere, and ein denotes an Einstein summation.

Proof. Throughout the proof, we factor out the global multiplier −1/(NT) and define G(l)

i to be the resulting backpropagated residual at layer l. Thus the actual gradient with respect to h(l)

i is

∂L

∂h(l)

i

= −1

NT G(l)

i.

We begin by considering the derivative of the loss with respect to Fθ(Xi)[t], which is

∂L ∂Fθ(Xi)[t] = S(Fθ(Xi)[t]) −Y [t]

i = −R[t]

i (129)

Since

∂Fθ(Xi)[t]

∂WO

= h(L)[t]

i (130)

it follows that

∂L ∂WO

= −1

NT

N X i=1 h(L)⊤ i Ri (131)

We now consider the gradient through each attention layer in terms of the current and previous layer embeddings h(l−1)

i, h(l)

i. Let h = h(l−1)

i, A = A(l)

i, G = G(l)

i, and V = V (l). The residual contribution to the gradient with respect to V (l) is

(Ah)⊤G = h⊤A⊤G.

Therefore, after restoring the global factor and summing over i,

∂L ∂V (l) = −1

NT

N X i=1 h(l−1)⊤ i A(l)⊤ i G(l)

i.

The gradient for M = Ah is δM = GV (l)⊤, δA = δMh⊤, δ(1)

h = A⊤δM. Next, through the row-wise softmax, each row Jacobian is

J(l)

i,t = Diag(A(l)[t]

i) −A(l)[t]⊤ i A(l)[t]

i (132)

Stacking these gives a tensor J(l)

i. Applying it row-wise to δA gives

S(l)

i = eintjk, tk→tj

J(l)

i, G(l)

i V (l)⊤h(l−1)⊤ i

(133)

Finally, back-propagating through ˜A = hW (l)h⊤+ DM(P (l)), the residual contributions are h⊤S(l)

i h for W (l) and eintjk, jk→t(D, S(l)

i)

<!-- Page 30 -->

Published as a conference paper at ICLR 2026 for P (l). Summing over i and normalizing,

∂L ∂W (l) = −1

NT

N X i=1 h(l−1)⊤ i S(l)

i h(l−1)

i (134)

∂L ∂P (l) = −1

NT eintjk, jk→t

D,

N X i=1

S(l)

i

!

(135)

Collecting all contributions to h(l−1)

i gives

G(l−1)

i = G(l)

i + A(l)⊤ i G(l)

i V (l)⊤+ S(l)

i h(l−1)

i W (l)⊤+ S(l)⊤ i h(l−1)

i W (l) (136) Since

∂L ∂Fθ(Xi) = S(Fθ(Xi)) −Yi = −Ri, after factoring out −1/(NT), the residual at the last layer is

G(L)

i = RiW ⊤

O. We can inductively apply the recurrence and collecting the per-layer parameter derivatives gives the desired expressions for ∂L/∂WO, ∂L/∂V (l), ∂L/∂W (l), and ∂L/∂P (l).

Lemma D.9 (First Step, Multi-Layer Zero-Initialization). Under the setting described, after one gradient step, we have that

WO = η(¯B) (137)

W (l), V (l), P (l) = 0 (138) for 1 ≤l ≤L where ¯B is a |V |×|V | matrix where the jth row is the average next-token distribution of the jth token in the vocabulary weighted by the relative frequency of token j across the dataset and centered to have the row sum be 0.

Proof. By Lemma D.8,

∂L ∂WO

= −1

NT

N X i=1 h(L)⊤ i Ri = −1

NT

N X i=1

X⊤ i (Yi −UO) = −(B −U) ≡−¯B (139)

where B and U are defined the same as in the one-layer case. A single gradient step gives

WO = −η ∂L

∂WO

= η ¯B (140)

At initialization WO = 0, so by Lemma D.8 the upstream gradient from layer L is

G(L)

i = RiW ⊤

O = 0 (141) Using the recurrence (Lemma D.8),

G(l−1)

i = G(l)

i + A(l)⊤ i G(l)

i V (l)⊤+ S(l)

i h(l−1)

i W (l)⊤+ S(l)⊤ i h(l−1)

i W (l) (142)

Since G(L)

i = 0 and W (l), V (l) = 0 for all l, we inductively get G(l)

i = 0 for every l.

Now, the layerwise gradients are (Lemma D.8)

∂L ∂V (l) = −1

NT

N X i=1 h(l−1)⊤ i A(l)⊤ i G(l)

i = 0 (143)

and with S(l)

i = eintjk, tk→tj

J(l)

i, G(l)

i V (l)⊤h(l−1)⊤ i we also have S(l)

i = 0 (because G(l)

i = 0 or V (l,0) = 0), hence

∂L ∂W (l) = −1

NT

N X i=1 h(l−1)⊤ i S(l)

i h(l−1)

i = 0 (144)

∂L ∂P (l) = −1

NT eintjk,jk→t

D,

N X i=1

S(l)

i

!

= 0 (145)

Therefore a single gradient step leaves W (l), V (l), P (l) = 0 for 1 ≤l ≤L.

<!-- Page 31 -->

Published as a conference paper at ICLR 2026

Theorem D.10 (Early Stage Features, Multi-Layer). Fix a depth L ≤

√

T 4 and assume zero initial- ization for all parameters. Under the setting described, for s ≤η−1 min

1 12L, 5 8 √

T with T ≥60 and |V | ≥500, after s gradient descent steps with learning rate η we have, uniformly for every layer 1 ≤l ≤L, WO −sη ¯B

F ≤3s2η2 (146) V (l) − s

2 η2 ¯Φ⊤¯B⊤

F

≤12s3η3 (147) W (l) −

3 s

4

+ 2 s

3 η4 ¯Q

F

≤13s5η5T (148) P (l) −

3 s

4

+ 2 s

3 η4∆

F

≤13s5η5T (149)

where ¯B, ¯Φ, ¯Q, and ∆are as in the one-layer analysis (row-centered bigram matrix, centered prefix-statistics operator, and the third-step structures, respectively).

Proof. We prove the bounds simultaneously for all layers with induction.

By the previous lemma, with zero initialization and one step, WO = η ¯B, W (l) = 0, V (l) = 0, P (l) = 0 for 1 ≤l ≤L. This gives the base case.

Now we prove the inductive step. Assume the four bounds hold after s steps, with (s + 1)η ≤ min

1 12L, 5 8 √

T

. We derive bounds on the deviations in the attention patterns, activations, and outputs in the forward pass after s steps.

Now, we start with a bound on the deviations in the activations from Xi at each row. Since, each row of A(l)

i sums to 1, we have that h(l)

i [t,:] −Xi[t,:]

≤ h(l−1)

i [t,:] −Xi[t,:]

+ max q≤T h(l−1)

i [q,:]

V (l). (150)

and h(l)

i [t,:]

≤(1 +

V (l))

h(l−1)

i [t,:]

(151)

Then, by the inductive hypothesis and sη ≤ 1 12L, we have that V (l)

F ≤2s2η2. Using this and that h(0)

i = Xi which has unit norm, we have that across all layers and rows h(l)

i [t,:]

≤

1 + 2s2η2 L (152)

Since sη ≤1/(12L), we have

2Ls2η2 ≤sη 6.

Thus

1 + 2s2η2 L ≤exp(2Ls2η2) ≤1 + sη 4, where the last inequality uses 2Ls2η2 ≤1/72. Therefore h(l)

i [t,:]

≤1 + sη

4.

Using this and again that h(0)

i = Xi, we have that for all rows and layers, h(l)

i [t,:] −Xi[t,:]

≤L

1 + sη 4

2s2η2 ≤sη 4, again using sη ≤1/(12L).

Let A0 be the uniform causal attention with the tth row having the first t elements equal to 1/t and the remaining elements equal to 0. For each layer l and row t, define the unmasked attention-logit vector z(l)

i,t:= h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:]

[: t].

<!-- Page 32 -->

Published as a conference paper at ICLR 2026

Then

A(l)

i [t,: t] = S(z(l)

i,t), A0[t,: t] = 1 t 1.

Decomposing h(l−1)

i [t,:] as Xi[t,:]+(h(l−1)

i [t,:]−Xi[t,:]), we get by the inductive hypothesis and that maxkm | ¯Qkm|, maxm |∆m| ≤1 as shown in the one-layer case that

MASK(h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:])

≤

6 s

4

+ 4 s

3 η4√ t + 26s5η5T

+ 2 h(l−1)

i [t,:] −Xi[t,:]

6 s

4

+ 4 s

3 η4√

T

+ h(l−1)

i [t,:] −Xi[t,:]

2 6 s

4

+ 4 s

3 η4√

T

(153)

By our earlier bounds, we have then

MASK(h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:])

≤s4η4√ t + 26s5η5T + sη

2 s4η4√ T + s2η2

16 s4η4√ T

(154)

which we can upper bound by

MASK(h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:])

≤s4η4√ t + 21

2 s3η3 (155)

and we have z(l)

i,t

≤s4η4√ t + 21

2 s3η3. (156)

Moreover, since ∥z(l)

i,t ∥∞≤∥z(l)

i,t ∥, the preceding bound and the assumptions sη ≤5/(8

√

T) and T ≥60 imply

∥z(l)

i,t ∥∞≤1

2.

Hence range(z(l)

i,t) ≤2∥z(l)

i,t ∥∞≤1.

By Lemma D.2, applied to the softmax on the first t coordinates,

(A(l)

i −A0)[t,:]

≤e t z(l)

i,t

.

Therefore (A(l)

i −A0)[t,:]

≤es4η4

√ t + 21e

2 s3η3 t.

For t = 1, both A(l)

i [1,:] and A0[1,:] are point masses, so the left-hand side is zero. For t ≥2, the assumptions sη ≤5/(8

√

T) and T ≥60 imply es4η4

√ t + 21e

2 s3η3 t ≤sη √

T

.

Thus, for all t, (A(l)

i −A0)[t,:]

≤sη √

T

. (157)

Consequently, A(l)

i −A0

F ≤sη. (158)

From the deviation bounds on the activations and the inductive control of WO,

∥Fθ(Xi)∥F = ∥h(L)

i WO∥F ≤∥h(L)

i ∥F ∥WO∥≤(1 + sη

4) √

T (sη + 3s2η2) ≤2sη

√

T (159)

<!-- Page 33 -->

Published as a conference paper at ICLR 2026

For each row t, let fi,t:= Fθ(Xi)[t,:] = h(L)

i [t,:]WO.

Using the activation bound and the inductive hypothesis for WO,

∥fi,t∥≤

1 + sη 4

(sη + 3s2η2).

Since sη ≤5/(8

√

T) and T ≥60, the right-hand side is at most 1. Hence range(fi,t) ≤2 ∥fi,t∥≤2.

By Lemma D.2, applied row-wise,

S(fi,t) −1

|V |1

≤e2

|V | ∥fi,t∥.

Summing over rows gives

∥S(Fθ(Xi)) −UO∥F ≤e2

|V | ∥Fθ(Xi)∥F ≤2e2sη

√

T |V |.

Since |V | ≥500, we have e2/ p

|V | ≤1, and therefore

∥S(Fθ(Xi)) −UO∥F ≤2sη s

T |V |. (160)

Then as in the one-layer case but using equation 160 and accounting for deviations in the hidden state from Xi,

∂L ∂WO

+ ¯B

F

≤ 4sη p

|V |

+ 4sη ≤5sη (161)

Then, after s + 1 steps, we have

WO −(s + 1)η ¯B

F ≤3s2η2 + 5sη2 ≤3(s + 1)2η2 (162)

From Lemma D.8,

∂L ∂V (l) = −1

NT

X i h(l−1)⊤ i A(l)⊤ i RiW ⊤

O (163)

Considering the deviation from each of the terms, we have

∂L ∂V (l) + sη¯Φ⊤¯B⊤

F

≤36s2η2 (164)

Then, we have that after s + 1 steps,

V (l) − s + 1

2 η2 ¯Φ⊤¯B⊤

F

≤12s3η3 + 36s2η3 ≤12(s + 1)3η3

From Lemma D.8,

∂L ∂W (l) = −1

NT

X i h(l−1)⊤ i S(l)

i h(l−1)

i (165)

∂L ∂P (l) = −1

NT eintjk, jk→t

D,

X i

S(l)

i

(166)

with S(l)

i = ein

J(l)

i, G(l)

i V (l)⊤h(l−1)⊤ i

. As in the one-layer bound, we can use the bound on the attention pattern to control J(l)

i. We have that for t ≥2

∥Jt,i −Jt∥2 ≤

1 + 2 √ t

∥Ai[t,:] −A0[t,:]∥2 + ∥Ai[t,:] −A0[t,:]∥2

2 (167)

<!-- Page 34 -->

Published as a conference paper at ICLR 2026

Then, as we have that

∥Ai[t,:] −A0[t,:]∥2 ≤sη √

T

(168)

it follows that

∥Jt,i −Jt∥2 ≤10sη √

T

(169)

Since J1,i is always all zeros, we can ignore this term and for t ≥2, we have that as sη ≤ 5 8 √

T,

∥Jt,i −Jt∥2 ≤10sη √

T

(170)

Now, we bound the deviation of G(l)

i from sη(Yi −UO) ¯B⊤. Starting from layer L, we have

G(L)

i −sη(Yi −UO) ¯B⊤

F ≤2sη s

T |V |(2sη) +

√

T(3s2η2) ≤4s2η2√

T (171)

We will let the bound on the deviation at layer l be DG,l. Now, we consider the bound for each layer l,

G(l−1)

i −sη(Yi −UO) ¯B⊤

F ≤DG,l + 4s2η2 G(l)

i

+ 2

S(l)

i

(2

√

T)(2s4η4T) (172)

Since we also need the norm of S(l)

i to iterate through layers, we bound the norm of S(l)

i, S(l)

i

F ≤

J(l)

i

G(l)

i

V (l)

h(l−1)

i

F

≤5

2

G(l)

i

(2s2η2)(2

√

T)

≤10s2η2 G(l)

i

√

T

≤7sη

G(l)

i

,

(173)

Using this upper bound back in the recurrence for DG,l, we have

G(l−1)

i −sη(Yi −UO) ¯B⊤

F ≤DG,l + 4s2η2 G(l)

i

+ 56s5η5T 3/2 G(l)

i

(174)

Using sη ≤ 5 8 √

T, we have

G(l−1)

i −sη(Yi −UO) ¯B⊤

F ≤DG,l + 18s2η2 G(l)

i

(175)

We can now write a recurrence for

G(l)

i as

G(l)

i

≤sη

(Yi −UO) ¯B⊤ + DG,l, we have

G(l−1)

i

≤(1 + 18s2η2)( sη(Yi −UO) ¯B⊤ + DG,l) ≤(1 + 18s2η2)(sη

√

2T + DG,l) (176)

Utilizing this with the recurrence for DG,l, we can then write a recurrence only in terms of DG,l and find that for all l, DG,l ≤12s2η2√

T as L ≤

√

T 4 and sη ≤min

1 12L, 5 8 √

T

. Then, we also have that for all l,

G(l)

i

≤sη

√

T + 12s2η2√

T ≤2sη

√

T. Then, we have that as ∥Jt∥2 = 1 t,

∥Ji∥2 ≤3

2 + 10sη √

T ≤2, and sη ≤min

1 12L, 5 8 √

T

, s3 −s2

2 η3Qi −S(l)

i

F

≤64s4η4T (177)

This produces

∂L ∂W (l) + s3 −s2

2 η3 ¯Q

F

≤64s4η4T (178)

<!-- Page 35 -->

Published as a conference paper at ICLR 2026 and similarly,

∂L ∂P (l) + s3 −s2

2 η3∆

F

≤64s4η4T (179)

and hence after (s + 1) steps

W (l) −

3 s + 1

4

+ 2 s + 1

3 η4 ¯Q

F

≤13(s + 1)5η5T (180)

P (l) −

3 s + 1

4

+ 2 s + 1

3 η4∆

F

≤13(s + 1)5η5T (181)

Lemma D.11 (Gaussian Initialization Operator Norm). Under the setting described and with all parameters initialized from N(0, v2

|V |2+2ξ) for ξ ≥0 and T ≤|V |, we have that with probability at least 1 −(3L + 1) exp

−|V |1+2ξ

4

, for all 1 ≤l ≤L,

∥WO∥,

V (l),

W (l),

P (l) ≤ 3v |V |1/2 (182)

Proof. We start with WO. Using a concentration bound on Gaussian random matrices, we have that

P

|V |1+ξ v WO

≥2 p

|V | + t

≤e−t2/2 (183)

Then, setting t = |V |1/2+ξ, we have that

P

∥WO∥≥ 3v |V |1/2

≤exp

−|V |1+2ξ

2

(184)

Then, with probability at least 1 −exp

−|V |1+2ξ

2

,

∥WO∥≤ 3v |V |1/2 (185)

We can apply the same argument for each of V (l), W (l) to derive the same bound. Since P (l) is smaller than the other matrices and has the same initialization, we can also apply the same bound. Applying a union bound on the probability of failures for each of the weights, we have that with probability at least 1 −(3L + 1) exp

−|V |1+2ξ

2

, all of WO, V (l), W (l), P (l) have operator norm at most 3v |V |1/2.

Lemma D.12 (Gaussian Initialization Frobenius Norm). Under the setting described and with all parameters initialized from N(0, v2

|V |2+2ξ) for ξ ≥0 and T ≤|V |, we have that with probability at least 1 −(3L + 1) exp

−|V |2+2ξ

4

, for all 1 ≤l ≤L,

∥WO∥F,

V (l)

F,

W (l)

F,

P (l)

F ≤2v (186)

Proof. We start with WO. Using Lemma 1 from Laurent & Massart (2000), we have that

P

∥WO∥2

F ≥ v2

|V |2+2ξ (|V |2 + 2|V |

√ t + 2t)

≤e−t (187)

Then, setting t = |V |2+2ξ

4, we have that

P

∥WO∥2

F ≥3v2

≤exp

−|V |2+2ξ

4

(188)

<!-- Page 36 -->

Published as a conference paper at ICLR 2026

Then, with probability at least 1 −exp

−|V |2+2ξ

4

,

∥WO∥F ≤2v (189)

We can apply the same argument for each of V (l), W (l) to derive the same bound. For P (l), we have

P

P (1)

2

F ≥ v2

|V |2+2ξ (T + 2

√

Tt + 2t)

≤e−t (190)

Then, setting t = |V |2+2ξ

4 and using that T ≤|V |, we have that

P

P (1)

2

F ≥3v2

≤exp

−|V |2+2ξ

4

(191)

Then, with probability at least 1 −exp

−|V |2+2ξ

4

, P (1)

F ≤2v (192)

Applying a union bound on the probability of failures for each of the weights, we have that with probability at least 1 −(3L + 1) exp

−|V |2+2ξ

4

, all of WO, V (l), W (l), P (l) have Frobenius norm at most 2v.

Theorem D.13 (Gaussian Initialization (Multi-Layer)). Assume the setting of D.10 with depth L ≤ √

T 4, all parameters initialized i.i.d. from N

0, v2

|V |2+2ξ with v ≤η2

T 2, T ≤|V |, and learning rate η ≥T −1. Then, with probability at least

1 −(3L + 1)

exp

−|V |1+2ξ

4

+ exp

−|V |2+2ξ

4 for s ≤η−1 min

1 12L, 5 8 √

T with T ≥60 and |V | ≥500, after s gradient descent steps with learning rate η we have, uniformly for every layer 1 ≤l ≤L,

WO −sη ¯B

F ≤3s2η2 (193) V (l) − s

2 η2 ¯Φ⊤¯B⊤

F

≤12s3η3 (194) W (l) −

3 s

4

+ 2 s

3 η4 ¯Q

F

≤13s5η5T (195) P (l) −

3 s

4

+ 2 s

3 η4∆

F

≤13s5η5T (196)

where ¯B, ¯Φ, ¯Q, and ∆are as in the one-layer analysis (row-centered bigram matrix, centered prefix-statistics operator, and the third-step structures, respectively).

Proof. We start by noting that as long the proof holds when v = η2

T 2 and we show that the first gradient step satisfies the inductive hypothesis used in Theorem D.10, then the proof will be complete. We will prove that the first gradient step satisfies the inductive hypothesis with v = η2

T 2.

We will condition on the event that the results of Lemmas D.11 and D.12 holds. Then, our results will hold with probability at least

1 −(3L + 1)

exp

−|V |1+2ξ

4

+ exp

−|V |2+2ξ

4 and we have that at initialization for all 1 ≤l ≤L

∥WO∥,

V (l),

W (l),

P (l) ≤ 3η2

T 2|V |1/2 (197)

<!-- Page 37 -->

Published as a conference paper at ICLR 2026 and

∥WO∥F,

V (l)

F,

W (l)

F,

P (l)

F ≤2η2

T 2 (198)

Now, we start with a bound on the deviations in the activations from Xi at each row. Since, each row of A(l)

i sums to 1, we have that h(l)

i [t,:] −Xi[t,:]

≤ h(l−1)

i [t,:] −Xi[t,:]

+ max q≤T h(l−1)

i [q,:]

V (l). (199)

and h(l)

i [t,:]

≤(1 +

V (l))

h(l−1)

i [t,:]

(200)

Using that

V (l) ≤ 3η2

T 2|V |1/2 and that h(0)

i = Xi which has unit norm, we have that across all layers and rows h(l)

i [t,:]

≤

1 + 3η2

T 2|V |1/2

L

(201)

and as η ≤ 1 12L and as (1 + c/L)L ≤1 + 2c for c ≤1, we have that h(l)

i [t,:]

≤1 + η7/2

2 (202)

Using this and again that h(0)

i = Xi, we have that for all rows and layers, h(l)

i [t,:] −Xi[t,:]

≤L

1 + η7/2

2

3η2

T 2|V |1/2 ≤η7/2

3 (203)

again using that sη ≤ 1 12L.

Let A0 be the uniform causal attention with the t-th row having the first t elements equal to 1/t and the remaining elements being 0. By our earlier bounds, we have then

MASK(h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:])

≤

1 + η7/2

2

2 3η2

T 2|V |1/2

√

T + 3η2

T 2|V |1/2 ≤6η7/2

√

T

(204)

where we have use 1

T ≤η and η ≤ 1 12L. For the tth row, define z(l)

i,t:= h(l−1)

i [t,:]W (l)h(l−1)⊤ i + DM(P (l))[t,:]

[: t].

The preceding bound gives z(l)

i,t

≤6η7/2

√

T

.

In particular, z(l)

i,t

∞≤6η7/2

√

T

≤1

2, under the assumptions on η and T. Hence range(z(l)

i,t) ≤1.

By Lemma D.2, applied to the softmax on the first t coordinates,

(A(l)

i −A0)[t,:]

≤e t z(l)

i,t

≤6eη7/2

√

T

.

Consequently, A(l)

i −A0

F ≤6eη7/2.

<!-- Page 38 -->

Published as a conference paper at ICLR 2026

From the deviation bounds on the activations and the initial bound on WO,

∥Fθ(Xi)∥F = ∥h(L)

i WO∥F ≤∥h(L)

i ∥F ∥WO∥≤(1 + η7/2

2) √

T 3η2

T 2|V |1/2 ≤4η4 (205)

For each row t, let fi,t = Fθ(Xi)[t,:].

From the preceding bound,

∥fi,t∥≤∥Fθ(Xi)∥F ≤4η4.

Thus, under the smallness assumptions on η, range(fi,t) ≤2 ∥fi,t∥≤1.

By Lemma D.2, applied row-wise,

S(fi,t) −1

|V |1

≤ e |V | ∥fi,t∥.

Summing over rows gives

∥S(Fθ(Xi)) −UO∥F ≤ e |V | ∥Fθ(Xi)∥F ≤4eη4

|V | ≤ 4η4 p

|V |

, where the last inequality uses |V | ≥500.

Then following the argument in the zero-initialization case,

∂L ∂WO

+ ¯B

F

≤ 4η4 p

|V |

+ η5/2

√

T

≤2η3 (206)

Then, after the first step,

WO −η ¯B

F ≤ 3η2

T 2|V |1/2 + 2η4 ≤3η4 ≤3η2 (207)

From Lemma D.8,

∂L ∂V (l) = −1

NT

X i h(l−1)⊤ i A(l)⊤ i RiW ⊤

O (208)

Considering the deviation from each of the terms, we have

∂L ∂V (l)

F

≤ 15η2

T 2|V |1/2 ≤15η9/2 (209)

Then, we have that after the first step

V (l)

F ≤2η2

T 2 + 15η11/2 ≤3η4 ≤12η3

From Lemma D.8,

∂L ∂W (l) = −1

NT

X i h(l−1)⊤ i S(l)

i h(l−1)

i (210)

∂L ∂P (l) = −1

NT eintjk,jk→t

D,

X i

S(l)

i

(211)

with S(l)

i = ein

J(l)

i, G(l)

i V (l)⊤h(l−1)⊤ i

. As in the zero-initialization case, we can use the bound on the attention pattern to control J(l)

i. We have that for t ≥2

∥Jt,i −Jt∥2 ≤

1 + 2 √ t

∥Ai[t,:] −A0[t,:]∥2 + ∥Ai[t,:] −A0[t,:]∥2

2 (212)

<!-- Page 39 -->

Published as a conference paper at ICLR 2026

Then, as we have that

∥Ai[t,:] −A0[t,:]∥2 ≤6eη7/2

√

T

(213)

it follows that

∥Jt,i −Jt∥2 ≤50η7/2

√

T

(214)

Since J1,i is always all zeros, we can ignore this term and for t ≥2, we have that,

∥Ji −J∥2 ≤50η7/2 (215)

Now, we bound the norm of G(l)

i. Starting from layer L, we have

G(L)

i

F ≤

√

2T 3η2

T 2|V |1/2 ≤5η4 (216)

Let DG,l denote a uniform upper bound on

G(l)

i

F. Now, we consider the bound for each layer l,

G(l−1)

i

F ≤DG,l + 5

2DG,l 3η2

T 2|V |1/2 +2

S(l)

i

√

2T 3η2

T 2|V |1/2 ≤(1+8η9/2)DG,l +9η4 S(l)

i

(217) Since we also need the norm of S(l)

i to iterate through layers, we bound the norm of S(l)

i, S(l)

i

F ≤

J(l)

i

G(l)

i

V (l)

h(l−1)

i

F ≤5

2DG,l 3η2

T 2|V |1/2

√

2T ≤8η4DG,l (218)

Using this upper bound back in the recurrence for DG,l, we have

G(l−1)

i

F ≤(1 + 8η9/2 + 72η8)DG,l (219)

Then for all l, DG,l ≤6η4 as L ≤

√

T 4 and η ≤min

1 12L, 5 8 √

T

. Then, we also have that for all l,

G(l)

i

≤6η4. Then, we have that as ∥Jt∥2 = 1 t,

J(l)

i

2 ≤ 3 2 + 50η7/2 ≤2, and sη ≤min

1 12L, 5 8 √

T

, S(l)

i

F ≤48η8 (220)

This produces

∂L ∂W (l)

F

≤48η8 (221)

and similarly,

∂L ∂P (l)

F

≤48η8 (222)

and hence after the first step

W (l)

F ≤48η9 + 3η2

T 2 ≤4η5T

P (l)

F ≤48η9 + 3η2

T 2 ≤4η5T
