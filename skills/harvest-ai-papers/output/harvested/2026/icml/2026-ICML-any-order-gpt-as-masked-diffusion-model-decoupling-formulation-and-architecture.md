---
title: "Any-Order GPT as Masked Diffusion Model: Decoupling Formulation and Architecture"
source_url: https://icml.cc/virtual/2026/oral/71083
paper_pdf_url: https://arxiv.org/pdf/2506.19935v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Any-Order GPT as Masked Diffusion Model: Decoupling Formulation and Architecture

<!-- Page 1 -->

arXiv:2506.19935v1 [cs.LG] 24 Jun 2025

Any-Order GPT as Masked Diffusion Model:

Decoupling Formulation and Architecture

Shuchen Xue1,2†, Tianyu Xie3, Tianyang Hu4‡, Zijin Feng5

Jiacheng Sun5‡, Kenji Kawaguchi4, Zhenguo Li5, Zhi-Ming Ma1,2

## 1 University of Chinese Academy of Sciences 2 Academy of Mathematics and Systems Science, Chinese Academy of Sciences 3

School of Mathematical Sciences, Peking University 4 National University of Singapore 5 Huawei Noah’s Ark Lab

## Abstract

Large language models (LLMs) predominantly use autoregressive (AR) approaches, but masked diffusion models (MDMs) are emerging as viable alternatives. A key challenge in comparing AR and MDM paradigms is their typical architectural difference: AR models are often decoder-only, while MDMs have largely been encoder-only. This practice of changing both the modeling paradigm and architecture simultaneously makes direct comparisons unfair, as it’s hard to distinguish whether observed differences stem from the paradigm itself or the architectural shift. This research evaluates MDMs within a decoder-only framework to: (1) equitably compare MDM (as Any-Order AR, or AO-AR) and standard AR paradigms. Our investigation suggests that the standard AO-AR objective, which averages over all token permutations, may benefit from refinement, as many permutations appear less informative compared to the language’s inherent left-to-right structure. (2) Investigate architectural influences (decoder-only vs. encoder-only) within MDMs. We demonstrate that while encoder-only MDMs model a simpler conditional probability space, decoder-only MDMs can achieve dramatic generation speedups (∼25×) and comparable perplexity with temperature annealing despite modeling a vastly larger space, highlighting key trade-offs. This work thus decouples core paradigm differences from architectural influences, offering insights for future model design. Code is available at https://github.com/scxue/AO-GPT-MDM.

Autoregressive

+ Causal Attention

Masked Diffusion Model

+ Full Attention

Unfair!

Masked Diffusion Model

+ Causal Attention

Formulation Architecture

## Introduction

The pursuit of more powerful and efficient foundation models drives continuous exploration beyond dominant autoregressive (AR) methods for language modeling. The remarkable success of diffusion

†Email: xueshuchen17@mails.ucas.edu.cn ‡Corresponding Authors

Preprint. Under review.

![Figure extracted from page 1](2026-ICML-any-order-gpt-as-masked-diffusion-model-decoupling-formulation-and-architecture/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-ICML-any-order-gpt-as-masked-diffusion-model-decoupling-formulation-and-architecture/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

models [1–3] in continuous domains has naturally spurred investigation into the viability and potential benefits of discrete diffusion models [4–6] for language modeling. Among the strategies emerging within the discrete diffusion framework, masked (absorbing state) diffusion models (MDMs) have captured considerable attention. Recent works such as LLaDA [7] and Dream [8] have successfully scaled these masked diffusion models to 7B parameters, achieving compelling results that challenge the sole dominance of AR methods.

Yet, in comparisons between AR and MDM paradigms, a fundamental architectural difference is often overlooked: the former typically operates within a causal attention, decoder-only setting, whereas the latter commonly employs full attention within an encoder-only setup. Beyond the high-level paradigm, the choice between causal and full attention dictates significant differences in training, density estimation, and generation efficiencies. Intriguingly, recent studies such as ENTP [9] and MAR [10] provide evidence hinting that full attention, despite its typical association with non-causal tasks, might hold inherent theoretical advantages and achieve superior empirical results even in contexts aiming for sequential, AR-like generation. This highlights the need to decouple the effects of the theoretical formulations (AR vs. MDM) from the underlying attention mechanism.

Building upon this observation, we propose and evaluate MDMs (as Any-Order AR) implemented within a decoder-only framework, a deliberate choice to enable a more equitable comparison against conventional autoregressive models. This setup allows us to isolate variables and answer the following two questions:

1. Within decoder-only architecture, what are the differences in modeling capabilities and empirical performance when using AR versus MDM formulation for language tasks? 2. Within the MDM framework for language tasks, what are the theoretical and empirical differences when selecting an encoder-only versus a decoder-only architecture?

To answer these questions, we specifically design AO-GPT3, a decoder-only architecture capable of modeling any-order sequences, with the potential to unify AR and MDM in a single model. We then conduct a series of carefully designed experiments. In Section 3, we delve into the first question by systematically investigating the impact of varying the distribution over token prediction orders during training, while keeping the decoder-only architecture constant. Our analysis in this section, leading to Findings 1-3, aims to clarify some intrinsic characteristics of language data, convergence properties, and the influence of different orderings. Subsequently, Section 4 addresses the second question by conducting a comparative analysis of encoder-only versus decoder-only architectures when implementing the MDM formulation. This investigation examines fundamental theoretical differences in how these architectures model conditional probabilities, their empirical performance on perplexity benchmarks, and crucial practical aspects such as generation efficiency, including computational complexity and inference speed. The insights from this section, encapsulated in Findings 4-7, are intended to clearly delineate the respective strengths, weaknesses, and trade-offs associated with each architectural choice for MDMs. Details of our AO-GPT, its special design, significance, and potential are provided in Section 5.

By looking closely at these aspects, this work aims to help better understand how different modeling approaches (AR vs. MDM) and model structures (decoder-only vs. encoder-only) work together. We think these findings will be helpful for both communities, for guiding future research and development in discrete diffusion and language modeling.

Preliminary

## 2.1 Background

Autoregressive (AR) Models. AR models factorize the data’s likelihood using the chain rule from left to right:

−log pθ (x) = − n X i=1 log pθ (xi|x<i):= LAR. (1)

3In this paper, AO-AR refers to the generative formulation, which can be implemented with either encoderonly or decoder-only architectures. In contrast, AO-GPT specifically denotes our model that combines the AO-AR objective with a decoder-only architecture.

<!-- Page 3 -->

Any-Order Autoregressive (AO-AR) Models. Unlike standard AR models which rely on a fixed factorization order, AO-AR models aim to model the likelihood of averaging or marginalizing over all possible n! permutations of the data sequence. Prominent examples include NADE [11], XL-Net [12], Autoregressive Diffusion Models [13], and σ-GPT [14]. The log-likelihood can be expressed as:

−log pθ (x) = −log Eσ∼U(Sn)pθ (x|σ)

≤Eσ∼U(Sn)

"

− n X i=1 log pθ (xσi|xσ<i)

#

:= LAO-AR. (2)

Discrete Diffusion Models. Early explorations into diffusion models for discrete data were conducted by [1] and [15]. Building on this, D3PM [4] introduced a more generalized framework. D3PM defines the forward noising process using a discrete-state Markov chain with specific transition matrices Qt and learns the reverse process pθ(x0|xt) by maximizing the Evidence Lower Bound (ELBO). Campbell et al. [5] further extended D3PM to continuous time, formalizing it as a continuous-time Markov Chain (CTMC). Separately, SEDD [6] takes a different approach by parameterizing the likelihood ratio pt(y)

pt(x) to learn the reverse process and employs Denoising Score Entropy for training this ratio. Among the various approaches within the discrete diffusion framework, MDMs (also known as absorbing state diffusion models) have gained significant attention. These models define a forward noising process where tokens are progressively masked:

qt|0 (xt|x0) = n Y i=1 qt|0 xi t|xi

0

= n Y i=1

Cat xi t; (1 −t)δxi

0 + tδ[MASK]

. (3)

Here, t ∈[0, 1] represents the diffusion time or masking level, interpolating between the original data x0 (t = 0) and a fully masked sequence (t = 1). More recently, for MDMs, studies by MDLM [16–18] and RADD [19] have demonstrated that different parameterizations are equivalent. These studies also show that the training objective can be simplified or directly derived from the likelihood, leading to the following objective function, which is an ELBO on the data likelihood:

−log pθ (x) ≤

Z 1

0

1 t Eqt|0(xt|x0)



 X i:xi

0=[MASK] −log pθ(xi

0|xt)



dt:= LMDM. (4)

LMDM and LAO-AR are equivalent through simple derivations using techniques in NADE [11] and RADD [19]. In the remainder of the paper, we will use the terms "Masked Diffusion Models (MDMs)" and "Any-Order Autoregressive Models (AO-AR)" interchangeably, as they are equivalent.

## 2.2 Decoupling Formulation and Architecture

Training Efficiency Decoder-only models leverage almost every token for prediction, offering high signal density. Encoder-only MDMs, while predicting more tokens (on average, 50%) than traditional BERT [20] (15% ∼25%), still typically utilize fewer tokens per example than their AR counterparts.

Density Estimation Efficiency To evaluate the joint density of a sequence under a given order (e.g., left-to-right), a decoder-only model computes the sequence likelihood in a single pass, achieving O(n) complexity4. In contrast, an encoder-only model requires n separate network evaluations, resulting in O(n2) complexity. Notably, estimating the AO-AR loss with an encoder-only model necessitates O(T · n) complexity, where T represents the number of Monte Carlo samples.

Generation Efficiency Inference procedures also differ markedly. Standard decoder-only AR models generate n tokens through n sequential forward passes; efficient Key-Value (KV) caching makes the total complexity approximately O(n). In contrast, encoder-only MDMs require T iterative refinement steps. With each step processing the full sequence via full attention (O(n) per step), their total complexity is around O(T · n). Notably, T (the number of steps) is often comparable to n, partly due to conditional independence assumptions when generating multiple tokens simultaneously [22, 23]. For comparison, decoder-only masked diffusion models can also achieve O(n) complexity.

4For simplicity, our complexity analysis assumes the context length nctx is relatively small compared to 12 · dmodel, leading to a linear scaling with the number of tokens, as discussed in [21].

<!-- Page 4 -->

10 20 30 40 50 Steps (k)

3.0

3.5

4.0

4.5

Loss

Left-to-Right

10 20 30 40 50 Steps (k)

3.0

3.5

4.0

4.5

Loss

Any-Order

GPT2-Small AO-GPT-Small

**Figure 1.** Training loss curves comparing a standard AR GPT against an AO-GPT. Both models employ an identical decoder-only architecture, with AO-GPT demonstrating slower initial convergence.

These fundamental differences in training, density estimation, and inference characteristics across architectures highlight the critical need to decouple the generative formulation (AR vs. MDM/AO-AR) from architectural choices (causal-attention decoder vs. full-attention encoder). Without such decoupling, comparing a standard decoder-only AR model to an encoder-only MDM inevitably conflates these two variables, obscuring a fair assessment of each paradigm.

## 2.3 Experiment Setting

Our approach trains MDMs using a decoder-only AR framework. A fundamental requirement for this is enabling the model to predict tokens in an arbitrary, non-sequential order, a departure from standard left-to-right autoregression. To achieve this any-order capability, we build upon the σ-GPT architecture [14], which integrates explicit target position information to guide predictions. We selected σ-GPT as our foundation over alternatives like XL-Net [12] due to its architectural alignment with contemporary decoder-only large language models.

Building on this baseline, our AO-GPT incorporates several key enhancements. We explore and refine methods for injecting target position information more effectively within the Transformer blocks and investigate the impact of training techniques such as Exponential Moving Average (EMA) to improve stability and performance. A comprehensive exposition of the AO-GPT architecture, its training paradigm, the specific design choices and ablations (including target position injection strategies and EMA), and the inference procedure is detailed in Section 5.

Following SEDD, we train our models on the OpenWebText dataset [24], as the original WebText dataset is not publicly available. For evaluation, we test on a suite of standard benchmarks: LAMBADA [25], WikiText2 [26], PTB [27], WikiText103 [26], and the One Billion Words dataset [28]. A context length of 1024 tokens is utilized for all experiments. For data splits and processing, we exactly follow the methodologies outlined in SEDD [6], which includes techniques such as packing sentences to generate uniform-length input blocks.

3 Standard AR vs. Any-Order AR (MDM): A Decoder-Only Comparison

As established in the preliminaries and further elaborated by NADE [11] and recent analyses such as RADD [19], the training objective for MDMs (LMDM) is equivalent to that of Any-Order AR models (LAO-AR). This equivalence can be formally expressed as:

LMDM =

Z 1

0

1 t Eqt|0(xt|x0)



 X i:xi

0=[MASK] −log pθ(xi

0|xt)



dt

[19] = n · El∼U(1,...,n)

1 n −l + 1Eσ∼U(Sn)

n X r=l

−log pθ(xσr|xσ<l)

[11] = Eσ∼U(Sn)

" n X i=1

−log pθ (xσi|xσ<i)

#

= LAO-AR

(5)

<!-- Page 5 -->

This mathematical equivalence is pivotal. It implies that when MDMs (via their AO-AR formulation) and standard AR models are implemented using the same decoder-only architecture, the fundamental difference in their training objectives lies in the distribution over token orders. Standard AR models adhere to a fixed, left-to-right order (i.e., the permutation σ is the identity, σ = id), while AO-AR models (and thus MDMs) effectively learn by averaging over all possible n! permutations (σ ∼U(Sn)). Therefore, the central goal of this section is to investigate the following key question:

Question 1: Within decoder-only architecture, what are the differences in modeling capabilities and empirical performance when using AR versus MDM formulation for language tasks?

To address Question 1, we first examine the training dynamics of these two approaches when implemented within an identical decoder-only architecture, specifically focusing on their convergence behavior. We train a standard left-to-right AR model and an AO-AR model on the same OpenWebText [24] dataset, with exactly the same architecture and model size (standard GPT-2 Small size), and observe their loss progression. Specifically, we simultaneously compare the AR loss eq. (1) and AO-AR loss eq. (2). In the figure, these are labeled ‘Left-to-Right’ and ‘Any-Order’, respectively. Our initial experiments, illustrated in Figure 1, reveal a notable difference in training progression:

Finding 1: Any-Order GPT converges significantly slower in the initial training stages compared to its standard GPT counterpart when both utilize the same architecture.

This initial observation (Finding 1) suggests that the any-order objective (σ ∼U(Sn)), despite its flexibility, might slow initial learning due to increased task complexity compared to the fixed left-to-right (σ = id) order. The slower AO-AR convergence could arise from two main factors: (1). Weight Sharing Burden: learning representations effective across n! permutations is demanding. (2).

Prevalence of Less Informative Orders: many permutations in U(Sn) might be uninformative.

To further probe the effect of prediction order, we next evaluate model training under conditions where a single, predetermined order is maintained throughout. We compare models trained on: a) conventional left-to-right (σ = id), b) a singular, randomly sampled permutation (σrand ∈Sn) that remains fixed for the entirety of the training phase, and c) a block-wise permutation strategy, serving as an intermediate approach motivated by Block Diffusion [29]. Globally, this method processes blocks of tokens sequentially from left to right. However, within each block, tokens are processed according to a fixed, non-left-to-right permutation. For example, if the sequence is divided into 4-token blocks, the first block of tokens (indices 0,1,2,3) would be processed in the order 0 →2 →3 →1. The next block (indices 4,5,6,7) would then be processed as 4 →6 →7 →5. This specific intra-block permutation remains constant throughout training. Figure 2(a) presents these results. The comparison in Figure 2(a) leads to our second finding:

Finding 2.1: Even when both are trained on only one fixed order, the standard Left-to-Right order converges much faster than an arbitrary, randomly selected fixed order from Sn. Finding 2.2: Fixed block-wise random serves as an interpolation between Left-to-Right and purely random order in terms of convergence speed.

Remark 1 (Identical Loss Lower Bound). The minimum achievable cross-entropy loss for any autoregressive factorization is the true entropy of the data, H(x). By the chain rule, H(x) = Pn i=1 H(xσi|xσ<i) for any permutation σ ∈Sn. Thus, the optimal loss value is identical regardless of the chosen generation order (e.g., left-to-right, any fixed random order, or averaged over all orders as in AO-AR). Differences in convergence or final empirical loss values therefore reflect practical learning challenges and inductive biases under different ordering schemes, not a difference in the achievable target for a perfect model. This ensures the fairness of our loss comparisons.

This underscores language’s intrinsic left-to-right structure. While order-agnosticism (and thus MDMs) offers flexibility, averaging over all permutations may be less optimal. Given the observed slower convergence of purely Any-Order models (Finding 1) and the apparent advantage of the L2R order (Finding 2), a natural question arises: can we retain the flexibility of AO-GPT while mitigating its convergence drawbacks, perhaps by guiding it with some explicit L2R signal?

To explore this, we investigate the effect of incorporating a small fraction of standard Left-to-Right (L2R) ordered data directly into the training process of an AO-GPT. Specifically, we modify the sampling of generation orders σ such that 90% of training instances use an order sampled uniformly

<!-- Page 6 -->

0 5 10 15 Steps (k)

3.00

3.25

3.50

3.75

4.00

4.25

4.50

Loss

Fixed Order

Left-to-Right

1st Random order 2nd Random order

3rd Random order Block-wise Random Order (size 4)

10 20 30 40 50 Steps (k)

3.5

4.0

4.5

Loss

Left-to-Right

10 20 30 40 50 Steps (k)

3.5

3.6

3.7

3.8

3.9

4.0

Loss

Any-Order

AO-GPT-Small AO-GPT-Small-10% left to right

**Figure 2.** (a) Convergence speed with different fixed prediction orders: left-to-right, fixed random, and fixed block-wise random. (b) Impact of adding 10% left-to-right (L2R) data to AO-GPT training on its L2R and any-order loss.

from Sn (i.e., σ ∼U(Sn)), while the remaining 10% of instances use the fixed L2R order (σ = id). The impact of this hybrid approach on training dynamics and performance is illustrated in Figure 2(b). Also, as shown in Table 1 under the "Left-to-Right" evaluation, our AO-GPT model incorporating this 10% L2R data achieves significantly lower zero-shot validation perplexity compared to a purely any-order one, underscoring the substantial improvement in final loss achieved by this hybrid approach. This experiment yields two significant observations:

Finding 3.1: Incorporating a small fraction (10%) of explicitly Left-to-Right ordered data into the training of an AO-GPT drastically improves its performance (both convergence speed and final loss) when evaluated on standard Left-to-Right.

This result, while perhaps not entirely unexpected given the inherent structure of language, is starkly illustrated when comparing final performance metrics. More surprisingly, this hybrid training strategy also benefits the model’s any-order capabilities:

Finding 3.2: A small fraction (10%) of Left-to-Right data can even improve the model performance on Any-Order data.

Finding 3.2 is particularly intriguing. It suggests that highly structured L2R patterns provide a beneficial inductive bias or a more stable learning signal, helping the model learn fundamental linguistic structures more effectively. This, in turn, appears to enhance generalization across arbitrary permutations, rather than being a mere data trade-off. This phenomenon itself warrants dedicated investigation beyond our initial exploration, as a comprehensive understanding of this benefit is a promising direction for future work.

## 4 Comparing Encoder-Only and Decoder-Only for Masked Diffusion Models

Building on the insights from comparing AR and AO-AR within a decoder-only framework, we now turn our attention to the impact of the architectural choice itself when implementing an Any-Order Autoregressive (or Masked Diffusion Model) formulation. This leads to our second question:

Question 2: Within the MDM framework for language tasks, what are the theoretical and empirical differences when selecting an encoder-only versus a decoder-only architecture?

To address Question 2, we analyze how encoder-only and decoder-only architectures differ in modeling the univariate conditional probabilities p(xj|xE) that underpin AO-AR or MDM, where j is the index of the target token and E ⊂{1,..., n}\{j} is the index set of observed context tokens xE.

## 4.1 Modeling Univariate Conditional Probabilities

Order-Invariant Formulation: For encoder-only AO-AR, the computed conditional probability pθ(xj|xE) is order-invariant. Provided that each token in xE is correctly paired with its positional

<!-- Page 7 -->

encoding, the permutation of these token-position pairs within the input does not alter the output probability for xj.

Order-Dependent Formulation: For decoder-only AO-AR, the inherent asymmetry in causal attention means the prediction pθ(xj|xE, σE) is order-dependent even each token in xE is correctly paired with its positional encoding. The probability explicitly depends on the sequence σE in which the context tokens xE are presented to the model.

Henceforth, we refer to pθ(xj|xE) as an order-invariant conditional probability and pθ(xj|xE, σE) as an order-dependent conditional probability. The distinction between order-invariant and order-dependent modeling leads to different counts of the effective conditional probability space covered by each architecture.

Finding 4: Encoder-only AO-AR models n · 2n−1 order-invariant univariate conditional probability while decoder-only AO-AR models approximately e · n! order-dependent univariate conditional probability.

Encoder-only AO-AR: This architecture models the probability of predicting any token xj (n possibilities) given any subset xE of the other n−1 tokens. Since the order of xE does not matter, we count the number of distinct pairs (j, E). For each target j, there are 2n−1 possible subsets E. Therefore, the model represents n · 2n−1 unique order-invariant conditional probabilities. This quantity can be derived combinatorially: summing over all possible context sizes k (from 0 to n−1), we choose k context tokens ( n k ways) and have n−k possible target tokens. The total is Pn−1 k=0 n k

(n−k) = n·2n−1.

Decoder-only AO-AR: This architecture models order-dependent probabilities. While it can potentially generate samples according to any of the n! permutations, the fundamental units are pθ(xj|xE, σE). To count the number of distinct such terms, we again sum over context size k. For a fixed context set E of size k and a fixed target j, there are k! possible orderings σE. Therefore, the total number of distinct order-dependent probabilities is:

Nordered = n−1 X k=0 n k

|{z} Choose context

(n −k) | {z }

Choose target k! |{z}

Order context

= n−1 X k=0 n! k!(n −k)!(n −k)k! = n!

n−1 X i=0

1 i! (6)

As n →∞, this sum quickly converges to e · n!. This significantly larger number compared to the encoder-only case reflects the decoder’s sensitivity to the permutation of the context. The core difference highlighted by these counts is whether the model’s prediction p(xj|...) is conditioned on the context as an unordered set xE (encoder) or as an ordered sequence (xσE(1),..., xσE(k)) (decoder).

## 4.2 Ensemble on Context Order

As shown in Figure 3 (Ensemble Times = 1), decoder-only AO-AR models exhibit higher zero-shot perplexity than their encoder-only counterparts. We hypothesize this performance gap is due to the inherently harder task faced by decoders: they must learn to represent approximately e · n! distinct order-dependent conditional probabilities, a vastly larger space than the n · 2n−1 order-invariant conditionals modeled by encoders. To verify this, given that the increased number is completely due to the order of context tokens xσ<i, we introduce an ensembling technique for evaluating LAO-AR = Eσ∼U(Sn) [Pn i=1 −log pθ (xσi|xσ<i)]. For each individual conditional probability pθ (xσi|xσ<i), we generate M random permutations of the context sequence xσ<i. The probability used for the loss calculation, pens(xσi|xσ<i), is obtained by averaging the model’s predictions across M permutations of the context xσ<i:

pens(xσi|xσ<i) = 1

M

M X j=1 pθ xσi|xpermj(σ<i), permj(σ<i)

. (7)

Here, permj signifies the j-th permutation of the context sequence. (We always include the identity permutation among the M permutations in practice.) Crucially, while the order of the input sequence fed to the model is permuted, each token remains associated with its original positional encoding. This averaging process approximates the order-invariance of an encoder by marginalizing over the context order. The results in Figure 3 show that the ensemble on order context fills the gap.

<!-- Page 8 -->

**Table 1.** Zero-shot validation perplexity(↓) on a variety of datasets on GPT-2-medium sized models (∼350M). †Model reproduced by the authors. ‡Model trained with an additional 10% left-to-right ordered data.

## Model

LAMBADA WikiText2 PTB WikiText103 1BW

Left-to-Right

Encoder-only Models

SEDD 39.19 30.29 88.18 30.05 53.54 RADD 38.60 29.71 76.00 29.96 52.36 Decoder-only Models

GPT-2 35.66 31.80 123.14 31.39 55.72 σ-GPT† 61.05 44.80 121.48 43.68 76.74 AO-GPT‡ 42.44 31.52 87.56 30.86 50.23

Any-Order

Encoder-only Models

SEDD 42.77 31.04 87.12 29.98 61.19 RADD 41.96 29.96 79.06 28.51 57.07 Decoder-only Models σ-GPT† 57.27 43.28 126.11 41.80 74.81 AO-GPT‡ 49.79 33.73 101.01 32.38 65.90 AO-GPT‡ + Ensembles (8 times) 45.08 30.63 87.74 29.46 59.11 AO-GPT‡ + Ensembles (64 times) 44.31 30.16 85.75 28.98 58.18

1 2 4 16 32 64 Ensemble Times

42.5

45.0

47.5

50.0

52.5

55.0

57.5

60.0

Perplexity

LAMBADA

1 2 4 16 32 64 Ensemble Times

30.0

32.5

35.0

37.5

40.0

42.5

45.0

WikiText2

1 2 4 16 32 64 Ensemble Times

90

100

110

120

130

140

PTB

1 2 4 16 32 64 Ensemble Times

30.0

32.5

35.0

37.5

40.0

42.5

## 45.0 WikiText103

1 2 4 16 32 64 Ensemble Times

60

65

70

75

80

85 1BW

AO-GPT-Small AO-GPT-Medium SEDD-Small SEDD-Medium

**Figure 3.** Zero-shot unconditional perplexity (↓) for varying ensemble sizes. An ensemble size of 1 represents the baseline model without ensembling.

Finding 5: Decoder-only AO-AR falls short of their Encoder-only counterpart, while ensemble on order context fills the gap.

This observation validates our initial hypothesis. The dramatic reduction in perplexity, which brings the decoder’s performance nearly in line with the encoder-only models, confirms that this sensitivity to context order is the dominant reason for the initial performance gap.

## 4.3 Generation Computational Complexity

The reverse process in MDMs iteratively recovers masked tokens as follows:

qs|t = n−1 Y i=0 qs|t(xi s|xt), where qs|t(xi s|xt) =

 



1, xi t̸ = [MASK], xi s = xi t s t, xi t = [MASK], xi s = [MASK] t−s t q0|t(xi s|xt), xi t = [MASK], xi s̸ = [MASK].

(8) Here, q0|t(xi s|xt) (when xi t = [MASK]) represents a distribution over the vocabulary for predicting a non-[MASK] token. Sampling xs from qs|t(xs|xt) involves sampling each xi s independently. For positions i where xi t̸ = [MASK], xi s is deterministically set to xi t. For positions where xi t = [MASK], a more efficient two-stage sampling procedure can be employed, as stated in Lemma 1.

Lemma 1 (Efficient Sampling Algorithm). For sampling xi s from qs|t(xi s|xt) as defined in Equation (8) when xi t = [MASK], an equivalent sampling procedure is:

1. Sample a binary variable b ∼Bernoulli s t

.

<!-- Page 9 -->

64 128 256 512 Steps

2.0

5.0

10

20

50

100

200

500

Time (s)

AO-GPT is ~25x faster than SEDD

Generation Time vs. Steps

SEDD-Medium AO-GPT-Medium

**Figure 4.** Generation time versus number of generation steps with sequence length 1024 and batch size= 32 for decoder-only AO-AR models (with KV-cache and Lemma 1) and their encoder-only counterparts (SEDD).

2. If b = 1, set xi s = [MASK].

3. If b = 0, sample xi s from the distribution q0|t(·|xt). It reduces computational cost by only requiring the evaluation of q0|t(·|xt) when b = 0. The proof of equivalence and a detailed discussion of the computational benefits are provided in Appendix C.

Leveraging both the KV-cache mechanism and the efficient sampling technique from Lemma 1, decoder-only AO-AR models significantly reduce per-step computational costs. At each generation step, the KV-cache obviates recomputing context tokens, while efficient sampling (Lemma 1) restricts computation to only those tokens designated for unmasking. This synergy reduces the computational complexity of each step to O(1), a marked advantage over their encoder-only counterparts. Our findings are summarized as follows:

Finding 6: The total computational complexity of generating a length n sequence using an encoder-only AO-AR is O(n2); with both KV-cache and Lemma 1, a decoder-only AO-AR’s computational complexity is O(n).

The O(n) total complexity for decoder-only AO-AR models (Finding 7) translates directly into tangible performance gains. This theoretical advantage is empirically validated by the significant generation speedups visualized in Figure 4. Beyond speed, we also evaluated the unconditional generation perplexity. To ensure a fair comparison and address the observation by [18] that float32 Gumbel noise (as used in SEDD [6]) can lower effective temperature, we utilized float64. We then compared AO-GPT and SEDD under three distinct annealing configurations: 1) no annealing (Top-p 1.0, Temperature 1.0), 2) mild annealing (Top-p 0.95, Temperature 0.9), and 3) appropriate annealing (Top-p 0.95, Temperature 0.7). The detailed results of generation perplexity are in Table 2, with the main conclusions summarized in Findings 8.1 and 8.2.

Finding 7.1: AO-GPT can achieve 25× speedup on generation compared with SEDD. Finding 7.2: AO-GPT exhibits higher generation perplexity without logit annealing, while appropriate annealing brings its perplexity to a comparable level.

The observed perplexity difference, particularly without annealing (Finding 8.2), can be attributed to AO-GPT’s lower modeling likelihood compared to SEDD when considered in non-ensembled configurations. Thus, while SEDD might achieve better perplexity for models of comparable size, AO-GPT’s striking 25x speed advantage (Finding 8.1) presents a compelling trade-off between generation quality and practical inference speed. The findings in this section illuminate the significant distinctions between encoder-centric and decoder-centric approaches, suggesting that exploring how to synergistically combine their respective advantages is a crucial direction for future work.

<!-- Page 10 -->

**Table 2.** Generation Perplexity measured by GPT-2-Large of AO-GPT-Medium and SEDD-Medium across different generation steps and sampling settings (Top-p and Temperature). Lower values are better.

Sampling Setting Steps

Top-p Temperature Model 64 128 256 512

1.0, 1.0 AO-GPT 194.588 154.837 148.006 140.369 136.406 SEDD 121.574 100.014 86.428 87.666 81.689

0.95, 0.9 AO-GPT 33.528 29.359 27.378 27.020 26.952 SEDD 25.414 22.034 19.481 19.022 19.311

0.95, 0.7 AO-GPT 6.105 5.615 5.507 5.095 4.611 SEDD 6.400 6.042 5.201 4.979 5.051

## 5 AO-GPT: a Decoder-only Model with the Potential to Unify AR and MDM

## 5.1 Significance and Future Potential

We highlight here its broader significance and future potential. The development of efficient and effective decoder-only MDMs like AO-GPT is crucial for several reasons:

Broader Scope: Firstly, the strong left-to-right sequentiality inherent in natural language, which often favors standard autoregressive (AR) models, may not be as pronounced in other discrete data modalities. For domains such as biological sequences, symbolic music, or certain structured code representations, the inherent flexibility of an any-order AR approach could be more naturally suited. Implementing such models within a decoder-only architecture, as AO-GPT proposes, could offer substantial advantages over rigidly ordered AR models, potentially leading to more effective modeling and generation in these diverse fields.

Efficiency: Secondly, within the realm of language modeling itself, the pursuit of decoder-only MDMs is driven by a compelling trade-off between modeling paradigms and computational efficiency. Decoder-only AO-AR offers significant theoretical and empirical advantages in density estimation and generation in terms of theoretical computational complexity and empirical generation speed (as discussed in Section 2.2, 4 and indicated by Finding 7, 8.1).

Flexibility: Thirdly, decoder-only AO-AR frameworks like AO-GPT exhibit superior flexibility in controlling the distribution over token generation orders. While encoder-only AO-AR models can vary the distribution of the number of masked tokens, they cannot easily specialize to a strict, fixed-order autoregressive model (e.g., left-to-right). In contrast, decoder-only AO-AR models can directly learn from any permutation distribution P(Sn). This allows them to instantiate a standard left-to-right AR model by simply using the identity permutation (σ = id), or to train on hybrid order distributions (as shown in Section 3). This adaptability uniquely positions them to interpolate between, and potentially unify, autoregressive and masked diffusion paradigms within a single architecture.

## 5.2 Injecting Target Position Information

In this section, we will give a comprehensive description of the modeling details, training, and inference of masked diffusion models using a decoder-only architecture. To train autoregressive models on sequences in any order with a decoder-only model, a key architectural modification is necessary compared to standard GPT: adding explicit target position information. In a traditional AR model setup (like GPT), the model implicitly predicts the token immediately succeeding the current one; the target position is always the next index in the sequence.

However, when processing sequences in a shuffled order according to a permutation σ = (σ1,..., σn), the token at step t in the shuffled sequence is xσt, and the target token to predict at step t is xσt+1. The original position σt+1 is not fixed relative to the current step t, but varies depending on the specific permutation. Therefore, at step t, to predict xσt+1, the model should access the information of the input representation for tokens xσ≤t, its position in the original sequence (σ≤t), and crucially, the original position σt+1 of the next token to be predicted in the shuffled sequence. This is necessary

<!-- Page 11 -->

order of words matter order of words matter 1 2 3 4 order of words matter 1 2 3 4

Causal Transformer

## 1 Tokens

Layer Norm

Layer Norm

Attention

MLP

2 4

MLP

Token-wise Gating

Token-wise Scale, Shift

Token-wise Scale, Shift

Token-wise Gating

AdaLN Target Positional Encoding

## 1 Tokens

Layer Norm

Layer Norm

Attention

MLP

2 4 1 Tokens

Layer Norm

Layer Norm

Attention

MLP

2 4

Same Target Positional

Encoding Per Layer

Different Target Positional

Encoding Per Layer

(a) (b) (c) (d)

Shuffle

Add Positional

Encoding

Input Tokens

1 2 4

Input Target Positional Encoding

**Figure 5.** Target position injection strategies for decoder-only AO-AR model.

0 10 20 30 40 Steps (k)

3.6

3.8

4.0

4.2

Loss

Left-to-Right

0 10 20 30 40 Steps (k)

3.6

3.8

4.0

4.2

Loss

Order-Agnostic

Vanilla PE Same PE every layer

Different PE every layer AdaLN every layer

(a) Ablation on Target Position Injection

0 10 20 30 40 Steps (k)

3.6

3.8

4.0

4.2

Loss

Left-to-Right

0 10 20 30 40 Steps (k)

3.6

3.8

4.0

4.2

Loss

Order-Agnostic

No EMA EMA=0.99

EMA=0.999 EMA=0.9999

(b) Ablation on Exponential Moving Average (EMA)

**Figure 6.** Ablation studies for AO-GPT: target positional encoding and exponential moving average.

because transformers need the explicit target original position (σt+1) to identify which specific original position’s token it should predict next, a requirement absent in fixed-order prediction.

We identify two existing decoder-only architectures for training order-agnostic autoregressive models: XL-Net [12] and σ-GPT [14]. XL-Net incorporates the target position using two-stream attention, a mechanism that differs significantly from mainstream decoder architectures. Therefore, we do not adopt this approach. In contrast, σ-GPT incorporates the target position through an additional target positional encoding on a standard GPT architecture as Figure 5(a). Thus, we choose to adopt σ-GPT as a baseline method.

## 5.3 Design Space of AO-GPT

## 5.3.1 Target Position Injections

We observe slow convergence in σ-GPT, particularly during its initial training stages. Beyond the factors analyzed in Section 3, we hypothesize that the semantic requirements imposed by the target position significantly influence the predicted token, potentially more so than a simple target position encoding can adequately capture. For instance, in the sentence She put the _ in the _, the first blank typically requires a noun representing a movable object (e.g., book, key, food), while the second necessitates a noun denoting a container or location (e.g., box, drawer, fridge). The distinct lexical distributions for these two positions suggest that a single, undifferentiated target position encoding applied after the token embedding may be insufficient to model these nuanced, position-dependent semantic constraints.

To address this potential limitation, we propose and ablate three distinct strategies for incorporating richer target position information, all designed to incur negligible additional computational cost: (1) Figure 5(c) re-applying the same target positional encoding at the input of each Transformer block; (2) Figure 5(d) utilizing distinct, learnable target positional encodings for each Transformer block; and (3) Figure 5(b) conditioning the LayerNorm parameters [30, 31] within each Transformer block on the target position. As shown in Figure 6, the former two ways demonstrate some early training acceleration compared to the baseline, but their advantages diminish in later stages, eventually performing nearly identically to the baseline. In contrast, the adaptive LayerNorm (adaLN) approach shows consistent improvements throughout the entire training process. This suggests that

<!-- Page 12 -->

0 10 20 30 40 Steps (k)

3.5

3.6

3.7

3.8

3.9

4.0

Loss

Left-to-Right

0 10 20 30 40 Steps (k)

3.5

3.6

3.7

3.8

3.9

4.0

Loss

Any-Order

-GPT + AdaLN + AdaLN + EMA=0.9999

**Figure 7.** Combined impact of adaptive layerNorm (AdaLN) and exponential moving average (EMA) on AO-GPT training. Loss curves compare the baseline σ-GPT, σ-GPT with AdaLN, and σ-GPT with both AdaLN and EMA (decay 0.9999) for Left-to-Right (left) and Any-Order (right) objectives.

**Table 3.** Zero-shot validation perplexity(↓) on a variety of datasets on GPT-2-medium sized models (∼350M). †Model reproduced by the authors. ‡Model trained with an additional 10% left-to-right ordered data.

## Model

LAMBADA WikiText2 PTB WikiText103 1BW

Left-to-Right σ-GPT† 61.05 44.80 121.48 43.68 76.74 AO-GPT‡ 42.44 31.52 87.56 30.86 50.23

Any-Order σ-GPT† 57.27 43.28 126.11 41.80 74.81 AO-GPT‡ 49.79 33.73 101.01 32.38 65.90 dynamically modulating LayerNorm parameters based on target position provides a more effective and stable way to incorporate positional information, likely because it allows for finer-grained, context-dependent normalization at each transformer block.

## 5.3.2 Exponential Moving Average

While Exponential Moving Average (EMA) of model weights is a less common technique in the pre-training of standard autoregressive language models, it is a widely adopted practice in the training of both continuous and current discrete diffusion models, where it often contributes to improved sample quality and training stability. Given the potential for EMA to smooth the training trajectory, and potentially to help smooth out noise, allowing the optimization to converge to the target loss more efficiently, we conducted an ablation study to assess its impact on OA-GPT. We experimented with several EMA decay rates: 0.99, 0.999, and 0.9999, comparing these against a baseline model trained without EMA. Our results indicate a clear benefit to employing EMA. All tested EMA configurations outperformed the baseline model (no EMA). Notably, an EMA decay rate of 0.9999 yielded the best performance among the values tested.

Having established the individual benefits of adaptive layerNorm (adaLN) for target position injection and exponential moving average (EMA) for training, we investigate their combined effect on AO-GPT. Figure 7 illustrates the training loss progression for both Left-to-Right and Any-Order objectives when integrating both adaLN and EMA (with a decay of 0.9999) into the σ-GPT baseline. The results demonstrate that these two enhancements are largely orthogonal, with their combination leading to significantly improved convergence and lower final loss values compared to the baseline σ-GPT and models with only one of the improvements. This synergistic effect is further corroborated by the zero-shot perplexity scores presented in Table 3, where the fully enhanced

<!-- Page 13 -->

-inf

The small black cat sat on the big blue mat Original Sentence

: tokens generated at last step:tokens predicted this step

Generation Order

The

1

4 cat

4

2 small

2

5

2

5 sat

5

9 blue

9

8 big

8

3 the the black

-inf

-inf -inf

3

7 black

3

7 7

7 6

10 the the

7 7

6 10

:KV-cache -inf:attention mask

1 4:position:target position

Query

Key

: tokens previously generated

1 2 3 4 5 6 7 8 9 10

The small black cat sat on the big blue mat

1 2 3 4 5 6 7 8 9 10

The small black cat sat _ the big blue _

**Figure 8.** Attention mask for simultaneous prediction of multiple tokens in AO-GPT.

AO-GPT (incorporating adaLN, EMA, and 10% L2R data) substantially outperforms the reproduced σ-GPT baseline across all evaluated datasets for both Left-to-Right and Any-Order evaluations.

## 5.4 Parallel Generation Attention Mask

The reverse process in MDMs iteratively recovers masked tokens as follows:

qs|t = n−1 Y i=0 qs|t(xi s|xt), where qs|t(xi s|xt) =

 



1, xi t̸ = [MASK], xi s = xi t s t, xi t = [MASK], xi s = [MASK] t−s t q0|t(xi s|xt), xi t = [MASK], xi s̸ = [MASK].

(9) Here, q0|t(xi s|xt) (when xi t = [MASK]) represents a distribution over the vocabulary for predicting a non-[MASK] token, provided by the model. Sampling xs from qs|t(xs|xt) involves sampling each xi s independently. Crucially, AO-GPT, equipped with the specialized attention mask depicted in Figure 8, can compute these probabilities q0|t(xi s|xt) for different i in a single forward pass. This mask ensures that the prediction for each masked token xi s is conditioned only on the unmasked tokens present in xt and its own position, without attending to other concurrently predicted masked tokens. Consequently, this parallel prediction scheme for multiple masked tokens introduces no training/inference mismatch for the individual q0|t(xi s|xt) distributions, as each is generated under conditions consistent with the model’s training.

## 6 Related Work

Any-Order Density Estimation Neural Autoregressive Distribution Estimation (NADE) [11] initially leveraged implicit position awareness within its MLP architecture, parameterizing conditionals p(xod|p(xo<d) for an arbitrary ordering o using a weight-sharing scheme inspired by RBMs. Masked Autoencoder for Distribution Estimation (MADE) [32] adapted standard autoencoders by carefully masking connections to enforce autoregressive properties for arbitrary orders. Autoregressive Diffusion Models (ARDMs) [13] integrated principles from diffusion processes, training a shared network on masked modeling objective. Arbitrary Conditional Distributions with Energy (ACE) [33] utilizes energy-based models to estimate arbitrary conditionals p(xi|xS). Training and inference on any-order autoregressive models the right way [34] addresses model redundancy and training inefficiency. They propose training on a smaller set of univariate conditionals p(xi|xS) and upweighting the training loss for conditionals expected to be frequent during inference, leading to improved likelihoods without sacrificing tractable inference for arbitrary conditional queries. In- DIGO [35] introduces a novel insertion-based decoding algorithm for Transformers, enabling flexible sequence generation in arbitrary orders. While InDIGO demonstrates adaptive generation, our work further investigates the implications of such order-agnostic capabilities within the discrete diffusion framework and its architectural consequences for likelihood modeling. Train for the Worst, Plan for the Best [36] focuses on the trade-off between MDM’s training complexity and its inference flexibility, while our paper focuses on decoupling the generative formulation from the underlying architecture.

Existing Decoder-only Any-Order Model Adapting decoder-only Transformers for any-order tasks has led to distinct approaches. XLNet [12] trained the model to predict tokens in all possible factorization orders to capture bidirectional context. It incorporates the target position zt using

<!-- Page 14 -->

a two-stream self-attention mechanism (content stream hzt and query stream gzt), a mechanism that differs significantly from mainstream decoder architectures. σ-GPT [14] enables any-order generation in a standard GPT architecture by incorporating the target position through an additional concatenated target positional encoding. Specifically, to predict token xσ(t+1), the model receives the current token xσ(t), its original position σ(t), and the original position of the target token σ(t + 1), allowing any generation order.

Randomized Image Generation Randomized Autoregressive modeling (RAR) [37] followed σ-GPT [14] and trained a standard autoregressive model with an additional target position encoding on permuted image tokens with annealing during training. Rand-AR [38] is a decoder-only visual model trained on randomly permuted image tokens, using an explicit position instruction token (which doubles the token length) before each image token to specify the spatial location of the next token to be predicted. While RAR and Rand-AR both explored training on permuted sequences, they primarily focused on the visual domain and differ from our work in several key aspects. (1) these methods operate exclusively on image tokens. The statistical properties and inherent structures of image tokens (e.g., local spatial correlations) are substantially different from those of language tokens, which exhibit more complex, long-range semantic and grammatical dependencies. (2) their approach to generation and the theoretical framework varies. RAR, despite training with permutations, ultimately anneals towards and generates images using a conventional raster scan order. Rand-AR does consider parallel decoding by predicting tokens for specified positions; however, it does not explicitly investigate or establish the connection between its order-agnostic generation and the principles of discrete diffusion models, a central aspect of our study. (3) the evaluation focus of these vision-centric works is predominantly on generative quality metrics such as Fréchet Inception Distance (FID) and Inception Score (IS). In contrast, our research places a strong emphasis on understanding the fundamental differences in likelihood modeling capabilities (e.g., perplexity) between standard autoregressive and order-agnostic/masked diffusion paradigms, particularly when controlling for architectural choices.

## 7 Conclusion and Limitation

In this work, we conducted a systematic investigation to decouple the effects of modeling paradigms (AR vs. MDM) from their commonly associated architectural choices (decoder-only vs. encoderonly). By implementing MDMs (as AO-AR) within a decoder-only framework, we facilitated a more equitable comparison and explored architectural influences within the MDM paradigm itself. Our comparison of autoregressive (AR) and masked diffusion models (MDMs) within a decoder-only framework revealed that MDM’s uniform order-agnosticism may be suboptimal for language, given its inherent left-to-right structure. This suggests future MDM research could benefit from exploring non-uniform order distributions, balancing modeling power with data alignment and efficiency. Furthermore, contrasting encoder-only and decoder-only MDMs highlighted decoders’ significantly lower generation complexity (e.g., linear vs. quadratic), though encoders offer unique advantages like bidirectional attention and context order invariance. These insights underscore the need to consider architectural impacts beyond formulation when comparing models, and affirm the strong potential of decoder-based MDMs as an efficient direction for future exploration.

Our experiments were conducted on models of up to medium size (e.g., 350M parameters). Whether these observations generalize to significantly larger computational scales remains an open question. Furthermore, this work focused on language; the applicability of our findings to other discrete data modalities is uncertain, especially as many such modalities may not possess the strong left-to-right sequential structure inherent in natural language.

## References

[1] J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, and S. Ganguli, “Deep unsupervised learning using nonequilibrium thermodynamics,” in International conference on machine learning, pp. 2256–2265, pmlr, 2015.

[2] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” Advances in neural information processing systems, vol. 33, pp. 6840–6851, 2020.

<!-- Page 15 -->

[3] Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole, “Score-based gen- erative modeling through stochastic differential equations,” arXiv preprint arXiv:2011.13456, 2020.

[4] J. Austin, D. D. Johnson, J. Ho, D. Tarlow, and R. Van Den Berg, “Structured denoising diffusion models in discrete state-spaces,” Advances in neural information processing systems, vol. 34, pp. 17981–17993, 2021.

[5] A. Campbell, J. Benton, V. De Bortoli, T. Rainforth, G. Deligiannidis, and A. Doucet, “A continuous time framework for discrete denoising models,” Advances in Neural Information Processing Systems, vol. 35, pp. 28266–28279, 2022.

[6] A. Lou, C. Meng, and S. Ermon, “Discrete diffusion modeling by estimating the ratios of the data distribution,” arXiv preprint arXiv:2310.16834, 2023.

[7] S. Nie, F. Zhu, Z. You, X. Zhang, J. Ou, J. Hu, J. Zhou, Y. Lin, J.-R. Wen, and C. Li, “Large language diffusion models,” arXiv preprint arXiv:2502.09992, 2025.

[8] J. Ye, Z. Xie, L. Zheng, J. Gao, Z. Wu, X. Jiang, Z. Li, and L. Kong, “Dream 7b,” 2025.

[9] E. Ewer, D. Chae, T. Zeng, J. Kim, and K. Lee, “Entp: Encoder-only next token prediction,” arXiv preprint arXiv:2410.01600, 2024.

[10] T. Li, Y. Tian, H. Li, M. Deng, and K. He, “Autoregressive image generation without vector quan- tization,” Advances in Neural Information Processing Systems, vol. 37, pp. 56424–56445, 2024.

[11] B. Uria, M.-A. Côté, K. Gregor, I. Murray, and H. Larochelle, “Neural autoregressive distri- bution estimation,” Journal of Machine Learning Research, vol. 17, no. 205, pp. 1–37, 2016.

[12] Z. Yang, Z. Dai, Y. Yang, J. Carbonell, R. R. Salakhutdinov, and Q. V. Le, “Xlnet: Generalized autoregressive pretraining for language understanding,” Advances in neural information processing systems, vol. 32, 2019.

[13] E. Hoogeboom, A. A. Gritsenko, J. Bastings, B. Poole, R. v. d. Berg, and T. Salimans,

“Autoregressive diffusion models,” arXiv preprint arXiv:2110.02037, 2021.

[14] A. Pannatier, E. Courdier, and F. Fleuret, “σ-gpts: A new approach to autoregressive models,” in Joint European Conference on Machine Learning and Knowledge Discovery in Databases, pp. 143–159, Springer, 2024.

[15] E. Hoogeboom, D. Nielsen, P. Jaini, P. Forré, and M. Welling, “Argmax flows and multinomial diffusion: Learning categorical distributions,” Advances in neural information processing systems, vol. 34, pp. 12454–12465, 2021.

[16] J. Shi, K. Han, Z. Wang, A. Doucet, and M. Titsias, “Simplified and generalized masked diffusion for discrete data,” Advances in neural information processing systems, vol. 37, pp. 103131–103167, 2024.

[17] S. Sahoo, M. Arriola, Y. Schiff, A. Gokaslan, E. Marroquin, J. Chiu, A. Rush, and V. Kuleshov,

“Simple and effective masked diffusion language models,” Advances in Neural Information

Processing Systems, vol. 37, pp. 130136–130184, 2024.

[18] K. Zheng, Y. Chen, H. Mao, M.-Y. Liu, J. Zhu, and Q. Zhang, “Masked diffusion models are secretly time-agnostic masked models and exploit inaccurate categorical sampling,” arXiv preprint arXiv:2409.02908, 2024.

[19] J. Ou, S. Nie, K. Xue, F. Zhu, J. Sun, Z. Li, and C. Li, “Your absorbing discrete diffusion secretly models the conditional distributions of clean data,” arXiv preprint arXiv:2406.03736, 2024.

[20] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers), pp. 4171–4186, 2019.

<!-- Page 16 -->

[21] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Rad- ford, J. Wu, and D. Amodei, “Scaling laws for neural language models,” arXiv preprint arXiv:2001.08361, 2020.

[22] A. Liu, O. Broadrick, M. Niepert, and G. V. d. Broeck, “Discrete copula diffusion,” arXiv preprint arXiv:2410.01949, 2024.

[23] M. Xu, T. Geffner, K. Kreis, W. Nie, Y. Xu, J. Leskovec, S. Ermon, and A. Vahdat, “Energy- based diffusion language models for text generation,” arXiv preprint arXiv:2410.21357, 2024.

[24] A. Gokaslan and V. Cohen, “Openwebtext corpus.” http://Skylion007.github.io/

OpenWebTextCorpus, 2019.

[25] D. Paperno, G. Kruszewski, A. Lazaridou, Q. N. Pham, R. Bernardi, S. Pezzelle, M. Baroni,

G. Boleda, and R. Fernández, “The lambada dataset: Word prediction requiring a broad discourse context,” arXiv preprint arXiv:1606.06031, 2016.

[26] S. Merity, C. Xiong, J. Bradbury, and R. Socher, “Pointer sentinel mixture models,” 2016.

[27] M. Marcus, B. Santorini, and M. A. Marcinkiewicz, “Building a large annotated corpus of english: The penn treebank,” Computational linguistics, vol. 19, no. 2, pp. 313–330, 1993.

[28] C. Chelba, T. Mikolov, M. Schuster, Q. Ge, T. Brants, P. Koehn, and T. Robinson, “One billion word benchmark for measuring progress in statistical language modeling,” arXiv preprint arXiv:1312.3005, 2013.

[29] M. Arriola, A. Gokaslan, J. T. Chiu, Z. Yang, Z. Qi, J. Han, S. S. Sahoo, and V. Kuleshov,

“Block diffusion: Interpolating between autoregressive and diffusion language models,” arXiv preprint arXiv:2503.09573, 2025.

[30] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “Film: Visual reasoning with a general conditioning layer,” in Proceedings of the AAAI conference on artificial intelligence, vol. 32, 2018.

[31] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in Proceedings of the

IEEE/CVF international conference on computer vision, pp. 4195–4205, 2023.

[32] M. Germain, K. Gregor, I. Murray, and H. Larochelle, “Made: Masked autoencoder for distribu- tion estimation,” in International conference on machine learning, pp. 881–889, PMLR, 2015.

[33] R. Strauss and J. B. Oliva, “Arbitrary conditional distributions with energy,” Advances in Neural

Information Processing Systems, vol. 34, pp. 752–763, 2021.

[34] A. Shih, D. Sadigh, and S. Ermon, “Training and inference on any-order autoregressive models the right way,” Advances in Neural Information Processing Systems, vol. 35, pp. 2762–2775, 2022.

[35] J. Gu, Q. Liu, and K. Cho, “Insertion-based decoding with automatically inferred generation order,” Transactions of the Association for Computational Linguistics, vol. 7, pp. 661–676, 2019.

[36] J. Kim, K. Shah, V. Kontonis, S. Kakade, and S. Chen, “Train for the worst, plan for the best:

Understanding token ordering in masked diffusions,” arXiv preprint arXiv:2502.06768, 2025.

[37] Q. Yu, J. He, X. Deng, X. Shen, and L.-C. Chen, “Randomized autoregressive visual generation,” arXiv preprint arXiv:2411.00776, 2024.

[38] Z. Pang, T. Zhang, F. Luan, Y. Man, H. Tan, K. Zhang, W. T. Freeman, and Y.-X. Wang,

“Randar: Decoder-only autoregressive visual generation in random orders,” arXiv preprint arXiv:2412.01827, 2024.

<!-- Page 17 -->

**Table 4.** AO-GPT Model Specifications Parameter Small Medium

nlayers 12 24 dmodel 768 nheads 12 16 dhead 64 64 Batch Size (tokens) 0.5M 0.5M Learning Rate 6.0 × 10−4 3.0 × 10−4 Weight Decay 0.05 0.05 Adam β1 0.9 0.9 Adam β2 0.95 0.95 EMA 0.9999 0.9999

A Additional Experiment Details and Results

A.1 Model Details

The AO-GPT models were trained with several common hyperparameters. Specifically, both Small and Medium models used a dhead of 64, a batch size of 0.5M tokens, a weight decay of 0.05, Adam optimizer parameters β1 = 0.9 and β2 = 0.95, and an Exponential Moving Average (EMA) decay of 0.9999. The learning rate was 6.0 × 10−4 for the Small model and 3.0 × 10−4 for the Medium model. Architectural details like nlayers, dmodel, and nheads are the same with the GPT-2 specific to each model size as detailed in Table 4. We trained AO-GPT on nodes of 8 H800 80GB. For the input adaptive layer norm, we use a target positional encoding of 128 hidden dimensions to minimize its impact on increased parameters.

A.2 Additional Results

**Table 5.** presents zero-shot validation perplexity scores on the same suite of datasets, but for models of a smaller scale (GPT-2-small size, ∼125M parameters). This allows for an examination of how the different approaches (SEDD, RADD, GPT-2, σ-GPT, and our AO-GPT with its enhancements) compare at different model sizes. Furthermore, to offer a qualitative assessment of AO-GPT’s generative capabilities, we provide unconditional text samples generated by our AO-GPT Medium model. Figures 9, 10, and 11 showcase these generated passages under different sampling configurations (varying top-p and temperature settings). These examples illustrate the model’s ability to produce coherent and contextually relevant text.

B Broader Impact

This research contributes to the development of text generation models with potentially enhanced controllability. This work explores diverse pathways for language modeling without inherently aiming to escalate the raw generative power beyond current systems, thereby promoting responsible exploration of AI techniques.

C Proof and Discussion for Lemma 1

Lemma 1 states that for sampling xi s from qs|t(xi s|xt) (Equation (8) in the main text) when xi t = [MASK], an equivalent two-stage sampling procedure can be used which reduces computational cost. We provide the proof of equivalence and discuss the computational advantages here.

Proof. When xi t = [MASK], the original distribution qs|t(xi s|xt) is defined as:

• P(xi s = [MASK]|xt) = s t

• P(xi s = v|xt) = t−s t q0|t(v|xt), for any token v̸ = [MASK].

<!-- Page 18 -->

**Table 5.** Zero-shot validation perplexity(↓) on a variety of datasets on GPT-2-small sized models (∼125M). †Model reproduced in this work. ‡Model trained with an additional 10% left-to-right ordered data.

## Model

LAMBADA WikiText2 PTB WikiText103 1BW

Left-to-right

Encoder-only Models

SEDD 49.41 41.19 118.74 41.70 72.60 RADD 49.09 38.26 107.78 38.41 63.33 Decoder-only Models

GPT-2 45.04 42.43 138.43 41.60 75.20 σ-GPT† 68.61 57.66 146.87 55.54 90.98 AO-GPT‡ 52.46 42.10 135.96 40.97 71.73

Order-agnostic

Encoder-only Models

SEDD 50.92 41.84 114.24 40.62 79.29 RADD 50.27 38.26 110.38 35.90 74.28 Decoder-only Models σ-GPT† 65.83 53.08 138.61 50.75 87.71 AO-GPT‡ 59.93 46.33 141.92 45.44 84.36 AO-GPT‡ + Ensembles (8 times) 55.62 42.77 126.08 42.02 77.62 AO-GPT‡ + Ensembles (64 times) 54.92 42.24 123.49 41.51 76.73

Here q0|t(v|xt) is the probability of token v given by the model’s predictive distribution for the masked position. The proposed procedure for xi t = [MASK] is:

Stage 1: Bernoulli Trial. Sample a binary variable b ∼Bernoulli s t

.

Stage 2: Determine xi s.

• If b = 1 (occurs with probability s t), set xi s = [MASK].

• If b = 0 (occurs with probability 1 −s t = t−s t), then sample xi s from the distribution q0|t(·|xt).

We demonstrate that this two-stage procedure generates samples with probabilities identical to the original definition of qs|t(xi s|xt) when xi t = [MASK].

Probability of sampling xi s = [MASK] with the new procedure: This event occurs if and only if the Bernoulli trial in Stage 1 yields b = 1. Pnew(xi s = [MASK]|xt) = P(b = 1) = s t. This matches the probability P(xi s = [MASK]|xt) from the original definition.

Probability of sampling xi s = v (where v̸ = [MASK]) with the new procedure: This event occurs if and only if the Bernoulli trial in Stage 1 yields b = 0, AND xi s is subsequently sampled as v from q0|t(·|xt) in Stage 2. The probability is:

Pnew(xi s = v|xt) = P(b = 0 and xi s is sampled as v from q0|t)

= P(b = 0) × P(sample v from q0|t|b = 0)

=

1 −s t

× q0|t(v|xt)

= t −s t q0|t(v|xt)

This also matches the probability P(xi s = v|xt) from the original definition for v̸ = [MASK]. Since the probabilities for all possible outcomes of xi s (either [MASK] or any v̸ = [MASK]) are identical under both the original definition and the two-stage sampling procedure, the two methods are mathematically equivalent.

<!-- Page 19 -->

. That’s part of it. That’s what their challenges are. Price cuts kept going up, and regressive tax cuts used to avoid the biggest recession deficits ever. And gave Bill Clinton earlier everything that Frederick Douglass said would, and will, help provide stimulus, public goods and extraordinary discovery of opposition to Republican New Deal. Like Dewey, failed Eisenhower, Bunyan, and other story, Democratic nomination does not. I no need any of these huge votes. They don’t have nothing, because they need a party to pull. So this is going to be difficult. You can’t do more than either party got on. They can come up with a lot better than we do. They could say oboe and no sir, like Democrats do. You could say they’re going to do. We frankly don’t care about whether or not to. You know Eisenhower was a Republican and not a Democrat. Hoith in the mid-1960s, in times of consensus about present threat to the budget and health care for seniors, the Democrats were real conservatives. He more than vetoed the largest military budget everyone has now. Eisenhower, did. And that continues to stand to haunt politicians. It’s a third year defense, and Democrats should be the best defending it. Still, his big difference with government-paid premiums and deductibles and the federal commitment to keep bills slightly lower, to the point. Now Change did a little older, a lot less of aigg, delivering a public option to pay by premiums. Under his plan, seniors can subsidize your health care as it is and they won’t give you the vouchers, anything. But they would let you Congress forward using the old patterns, looking at Medicare, and making sharp adjustments. That is what we did and Eisenhower also do, and Democrats well do have an alternative to it, it’s Romney. The Health Care Act, from Clinton, provided this but, you know, Democrats have opposed it, undertaking the Social Security program until roughly three years later, not after really the final reforms made Obamacare. That leaves Medicaid completely, but not the Bill Health Insurance or WILI. Instead, these taxes will be chained for a few years. Then die, while Federal reverses itself on waiting to stop the stimulus, even now there is evidence that the American recovery, even now, has at best reached great stimulus, never zero. Oh, you just put in a few fantasy. I have yet to run the CBO score, but it’s going to keep providing two to three hundred million people, get as Census4–2008, or the amount of people who advocated to destroy those benefits. But getting rid of the lion’s taxes doesn’t mean that Republican success, or it is. And there are other options. Republican care plans want to make sure the elderly and the poor don’t pay taxes. JOINS GROUP, JIM LEE, TOM MONLE, AUSTIN ZIENCEIN, HEALTHY POLICE WOLFNEY: SIGNED RESEARCHISM CLASS, PRINCESSES VECTOR: —– "Intellect would rather have this conversation, my kids’ children, and they’re going to say how I got insurance and Medicare and we are gonna make the individuals younger, I’m saying Obama’s going to get out of the wages of most Americans. But here’s what my point of view is: It’s constitutional. No, this is a government-run health care that is our entitlement that everybody got to raise the children of their parents." It should be a state-run entitlement. But there’s a few points Republicans should pick up on. To some people, this really is an antitrust problem. He had a monopoly right. And this is one issue that Republican health reform is addressing. When you think of Obamacare, one of those things is health care clearly. Now, the antitrust of American health care is the antitrust issue. So, to us people speak to them even if it was no problem. But the plan that would win the antitrust issue would not be Obamacare. Kaplan Unio tried to allow health care firms to discriminate between insurers and consumers and charge them the best prices they can. With the nets rolled, the conservative media called any plan that took money to allow this micromanagement essentially pushed doctors from, essentially, price schemes. Counter-contradictory proposal for natural-buy new surcharge. Republicans argued that people could buy insurance after union drug provisions kind of with union money. Health insurance companies designed then still in buy in have entered discussion even saying they wouldn’t have to cover abortion care. Because it’s in a doctor’s facility, it is a product of Blackburn’s bill... It’s an association. This was the bill at the highest point. Democrats rejected. They were 96% against it.... What we wanted them to say was that

**Figure 9.** Unconditional generation result of OA-GPT Medium (top-p= 1.0, temperature= 1.0).

<!-- Page 20 -->

that young people who were vulnerable need to be protected,” the lawsuit said. “He wanted the school to be a model for people who violate our trust.” The sexual assault trial had started in January of 2014. At 17, Madsen was a popular teacher of boys at the boys’ academy, but resigned abruptly in 2010. He moved into substitute teaching and working on the force. A jury in 2013 convicted him of all 49 counts of sexual abuse for allegedly performing oral sex at the boys’ while he was a lieutenant. In a similar case last year, a jury found that the district attorney’s office covered up allegations of sexual misconduct that involves both female students and male students. “It’s been a legacy of defense and secrecy being preserved for many months,” Barbara Cappadza, the chief deputy prosecutor for the Sacramento County District Attorney’s Office, said on Thursday. [California bureaucrat signs off deal to avoid criminal charges for covering up child sex abuse after school department violence] “I was shocked, the shocking thing about the case, is that it seemed so away from the role she took in knowing the officers were involved in the case,” she said. “They said they did have a sense of familiarity with where the case was going.” The lawsuit is the first time the office has pursued civil criminal charges, it says, against Madsen, the teacher, about the abuse. This lets Cappadza, known by the Sacramento DA as a “proactive prosecutor, prosecute all alleged cases of sexual misconduct cases. “ Complaints and actions against child sex abuse are common in all investigations,” Cappadza said. “It’s possible all of the criminal cases in this case go back to 2010.”

In an interview, an attorney for the county attorney’s office and the San Francisco Department of Children and Families, said the agency had not filed criminal charges against the current officers in the case despite the fact they did not. They have not publicly admitted to any sexual misconduct, nor that any such allegations have been made in public. “The district attorney’s office still has the authority to resolve these allegations and has determined each individual involved is in a confidential and inadvertent matter in the district attorney,” Cappadza said. The lawsuit found that the county police have brought sexual misconduct allegations against the officers about 30 times. In those cases, prosecutors find there is enough evidence even against officers and they may not be brought behind bars. Charges against those who are fired are often steep and unusual. Madsen was previously fired from leading a school force of about 100 officers, according to a report filed by a police inspector in 2013 by the school district’s police union. Madsen complained that some of his officers were caught up in sexual misconduct accusations against officers around the country at this time over the years. In his conference remarks, he said that there are “a growing number” of 962 sworn officers and more than 600 in 13 of California’s 32 cities at large. Highprofile cases of alleged civil rights violations in California. Take a close look into the cover-up in the 2016 rape of 11. (The New York Post) The identity of the alleged victims could not be publicly released for the record, because prosecutors do not currently have a Madsen witness in the case. Nonetheless, they have said that they may themselves have been victims of sexual misconduct. They would concede, however, that the allegations have been or were likely made before this case. Human rights advocates say officers are hired and sanctioned by the public after lineups of the force. The American Society is investigating similar complaints against a longtime member of the county police department alleging that he’s disciplined twice in 2010 and 2011. Another officer reached just a guilty plea for reporting having sex with an underage student in a drug program in 2013; he then was fired in 2013 and then was fired in the same year for another job. The suit is an unusual one against Madsen, as well as a handful of other sexual misconduct suits. Madsen, 47, was promoted early in his tenure as the Sacramento County High School Task Force head on Jan. 21, 2010, the news outlet previously reported. He already completed three years probation after he pleaded no contest in 2012 to sexually assaulting a female student. “I went through a lot of changes. I wanted to start it, I wanted to know about it,” said Matilda Montoya,

35, who lost her sister in Honduras in the West Hills town of Telarrugada, Colombia soon after in March. “I really wanted to get started. If I could get involved, but I got stuck here. I should get back to my trip

**Figure 10.** Unconditional generation result of OA-GPT Medium (top-p= 0.95, temperature= 0.9).

<!-- Page 21 -->

just say, “I’m gonna tell you, I don’t put my name on the show, but I want to tell you what I think. And it’s not what I want to say. And I’m gonna tell the rest of you, in my campaign and, frankly, this country. And I know the people, as many people as there are, they’re going to put you on it. Because you know, you can say on the radio, “I don’t care what you think. I don’t want to be afraid of you. It’s a shame for you.” Q: Well, it’s a great shame for you. Q: Thank you. John. Trump: Like I said. Q: Thank you. Trump: Thank you. Trump: Thank you. Well, we don’t have to go on and on. Q: In the end, do you think we’re going to start to hear from listening to you. I’m going to be afraid that we’re not going to be listening to you. Trump: I think, I think, I think, that listening to the rest of the world, to the Europeans, is a danger to the world. On the other hand, I think it’s the danger, maybe, or even the peril, that the U.S. is being, right now. I think, of course, is that it has been said that we are not listening to the part of the world right now, the 1 percent of us. And the percent of people that make up 1 percent of the world, the 1 percent of Americans, and frankly, the Europeans, and the rest of the world, the rest of the rest of the world, I think that we do have the luxury of listening to the American people, in a way, listening to the Europeans, and to start listening to the world and in some ways, start to think, and think about what we’re going to do to the rest of the world. I think the United States is going to be a very powerful country, a powerful country, a very powerful military, probably the strongest military in the world, and a great power. I think that, at the end of the day, as the world’s largest economy, we’ll be known as a superpower. But our country is the superpower of today, and if we lose that, we’re not going to be the dominant power of the area, of the world, and we’re gonna be a threat to the world. We’ll be a threat to Europe, we’ll be in a threat to each other, and a major threat to each other. We’ll be a threat, we’re a threat to the other parts of the world, as the Middle East, as well, and as the Pacific, and obviously, the security world. And that’s right, but we’re gonna leave, because the United States is still on the world. And if we leave, the U.S. will be the threat to the 1 percent of the world, and of the world, of the European Union, the rest of the world, and frankly, the rest of the Western world. It’s a big danger for us. And we have to start to think, as Americans and the way we think about it, understand that this is important to us, because that’s the relationship this is that we’re going to have. We’ve got a great relationship with the U.S. — and we’re in that relationship. It’s a vital relationship. I think it’s important, I think I have to say, this don’t think is necessarily, it’s gonna be a loss of this, but it’s gonna be more than that. It’s not be like it used to be, the rest of the world, in terms of security, we’re gonna have to be smarter, I mean, and I think that we’re gonna have to understand that we’re in more of a danger now, as a country, than we were, than we were in the past, because we’ve got a system, it’s going to be more complicated, we’re going to have more ways to work with people all around the world, we’re going to be a kind of danger. In that sense, now I think we’re in a much more danger, actually. I think this is a danger, actually, to the American public, is that much more serious and more dangerous. That’

**Figure 11.** Unconditional generation result of OA-GPT Medium (top-p= 0.95, temperature= 0.7).
