---
title: "Is the Information Bottleneck Robust Enough? Towards Label-Noise Resistant Information Bottleneck Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39363
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39363/43324
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Is the Information Bottleneck Robust Enough? Towards Label-Noise Resistant Information Bottleneck Learning

<!-- Page 1 -->

Is the Information Bottleneck Robust Enough? Towards Label-Noise Resistant Information Bottleneck Learning

Yi Huang1, Qingyun Sun1*, Yisen Gao2, Haonan Yuan1, Xingcheng Fu3, Jianxin Li1

1SKLCCSE, School of Computer Science and Engineering, Beihang University, Beijing, China 2Department of Computer Science and Engineering, HKUST, Hong Kong, China 3Key Lab of Education Blockchain and Intelligent Technology, Ministry of Education, Guangxi Normal University, China {yihuang, sunqy, yuanhn, lijx}@buaa.edu.cn, ygaodi@cse.ust.hk, fuxc@gxnu.edu.cn

## Abstract

The Information Bottleneck (IB) principle facilitates effective representation learning by preserving label-relevant information while compressing irrelevant information. However, its strong reliance on accurate labels makes it inherently vulnerable to label noise, prevalent in real-world scenarios, resulting in significant performance degradation and overfitting. To address this issue, we propose LaT-IB, a novel Label-Noise ResistanT Information Bottleneck method which introduces a “Minimal-Sufficient-Clean” (MSC) criterion. Instantiated as a mutual information regularizer to retain task-relevant information while discarding noise, MSC addresses standard IB’s vulnerability to noisy label supervision. To achieve this, LaT- IB employs a noise-aware latent disentanglement that decomposes the latent representation into components aligned with to the clean label space and the noise space. Theoretically, we first derive mutual information bounds for each component of our objective including prediction, compression, and disentanglement, and moreover prove that optimizing it encourages representations invariant to input noise and separates clean and noisy label information. Furthermore, we design a three-phase training framework: Warmup, Knowledge Injection and Robust Training, to progressively guide the model toward noise-resistant representations. Extensive experiments demonstrate that LaT-IB achieves superior robustness and efficiency under label noise, significantly enhancing robustness and applicability in real-world scenarios with label noise.

## Introduction

The Information Bottleneck (IB) principle (Tishby, Pereira, and Bialek 2000) provides a fundamental theoretical framework for balancing compression and relevance in representation learning. Rooted in information theory, it has increasingly influenced the development of deep learning (Hu et al. 2024). IB encourages representations Z that retain only taskrelevant information while discarding irrelevant or redundant input features using Mutual Information (MI) I(·; ·):

min −I(Y; Z) + βI(X; Z). (1)

IB-based methods aim to extract “Minimal-Sufficient” representations, inherently filtering out input noise and spurious correlations. This selective encoding mechanism contributes

*Corresponding Author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

CIFAR10 40% asym noise 50% sym noise

ResNet34 77.78% 79.4% VIB (β = 0.01) 73.80% 10.0%

Cora (40% noise) Epoch: 0 →20 Epoch: 20 →100

GIB 22.9% →69.5% 69.5% →55.1% steady increase ↑ steady decline ↓

**Table 1.** Performance of IB methods under noise conditions.

to their notable robustness under noisy or adversarial input perturbations (Shamir, Sabato, and Tishby 2010).

However, input noise rarely eliminates all useful information, allowing IB to extract meaningful features from Y. In contrast, label noise corrupts the supervisory signal, causing I(Y; Z) to mislead Z to fit incorrect labels, thereby reducing robustness. This vulnerability is critical in real-world settings, where label noise is common and can severely harm performance, as real graphs are often disturbed by noise and unexpected factors. (Li et al. 2025). To address this, Label- Noise Representation Learning (LNRL) (Song et al. 2022) aims to extract robust features despite label corruption.

To empirically test the hypothesis that IB is inherently vulnerable to label noise, we conduct preliminary experiments on two tasks: image classification in computer vision and node classification in graph learning. We evaluate two representative IB-based methods: VIB (Alemi et al. 2017) and GIB (Wu et al. 2020). As shown in Table 1, VIB suffers performance drops and even training collapse, while GIB exhibits degraded accuracy. See Appendix E.3 for details.

To mitigate this, a simple remedy is to denoise the labels prior to applying IB. However, this two-stage pipeline is inherently suboptimal in both theory and practice.

Theorem 1.1 (Cumulative Degradation). In the two-stage approach, f1 is used to modify the labels Y ′ = f1(D), and f2 is responsible for extracting valid information from D while approximating the prediction result to f1(D). For one-stage model g(D), it extracts the relevant information while removing noise. If the denoising abilities of f1 and g are the same, the following inequality holds:

P(f2(D)̸ = g(D)) ≥H(Y ′|D) −1 log(|Y| −1), (2)

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22084

<!-- Page 2 -->

Noise Misleading Information.

MSC Information.

Minimal-Sufficient-Clean

Noisy Information. 

𝑌 𝒟

Clean Information. ☺

IB = + LaT-IB =

**Figure 1.** Comparison between LaT-IB and IB Principle.

where Y denotes the support of Y, and |Y| denotes the number of elements in Y. The two models perform identically iff f2 achieves the error lower bound and H(Y ′|D) = 0.

The proof of Theorem 1.1 is given in Appendix C.1. It demonstrates that cascading a denoising model f1 with an IB learner f2 leads to cumulative information loss compared with a unified model g, due to the extended information path. This phenomenon is further validated by empirical results, which show a clear degradation in the denoising effect when models are cascaded. See Appendix E.3 for detailed results.

Core Issue: How can the IB principle be effectively applied to real-world scenarios with complex and unknown label noise, in order to learn representations that are both “Minimal-Sufficient” and robust to noisy supervision?

Due to unknown label noise and the difficulty of integrating denoising with Information Bottleneck, applying IB in practice requires confronting the following key challenges:

• How to formulate the IB objective under label noise to learn clean representation. (▷Section 4.1) • How to optimize MI under label noise that distorts taskrelevant representation learning. (▷Section 4.2) • How to effectively disentangle clean and noisy representations without knowing noisy samples. (▷Section 4.3) Present work. To address the core issue and tackle the key challenges, we propose a Label-Noise ResistanT Information Bottleneck (LaT-IB) method. Centered on the idea of disentangling representations into clean and noisy label spaces, we formulate an IB training objective tailored for noisy supervision and theoretically justify its effectiveness through upper and lower bound analysis. To this end, we design a three-phase training framework: Warmup, Knowledge Injection and Robust Training, which gradually guides the model to learn “Minimal-Sufficient-Clean” (MSC) representations. A comparison between LaT-IB and standard IB principle is illustrated in Figure 1. Our contributions are:

• We identify the inherent vulnerability of IB to label noise and prove that denoising before IB is suboptimal. • We propose a LaT-IB method that introduces MSC criterion of representations to enhance IB’s robustness to label noise while maintaining its essential characteristics. • We provide theoretical upper and lower bounds for LaT- IB, showing how disentangling clean and noise features enables robust representation learning. Based on this, we design a principled model and training framework. • Extensive experiments evaluate LaT-IB’s robustness and efficiency, outperforming baselines under label noise and adversarial attacks across diverse tasks and domains.

## Related Work

## 2.1 Information Bottleneck for Robustness The IB (Tishby, Pereira, and

Bialek 2000) framework introduces a feature learning paradigm grounded in information theory. Works such as VIB (Alemi et al. 2017) and GIB (Wu et al. 2020) have advanced its practical use. Considering robustness, methods like DisenIB (Pan et al. 2021) and DGIB (Yuan et al. 2024) show reasonable robustness to input features, with studies (Xie et al. 2023; Pensia, Jog, and Loh 2020) further improving resilience to input noise.

Considering the presence of label noise, RGIB (Zhou et al. 2023) explores structural noise in GNNs to improve link prediction robustness. However, comprehensive studies on the vulnerability of IB to label noise still remain lacking.

## 2.2 Label-Noise Representation Learning

The LNRL aims to improve model robustness and representation quality under noisy label conditions. Existing approaches for learning with noisy labels include sample selection (Patel and Sastry 2023; Wei et al. 2020), which filters out likely noisy samples; robust loss functions (Zhang and Sabuncu 2018; Wang et al. 2019), which modify loss terms to reduce sensitivity to incorrect labels; noise-robust architectures (Liu et al. 2020), which use regularization to avoid overfitting noise; and data augmentation, such as mixupbased methods (Zhang et al. 2018; Harris et al. 2020), which interpolates samples to improve generalization.

However, most methods ignore representation-level constraints, making it hard to learn task-relevant and noiseinvariant features under severe noise or distribution shifts.

## 3 Preliminary Analysis

Notation. We primarily define the input data D. For vision tasks, D = X, where X ∈RN×C×P ×Q denotes N samples with C channels and spatial size P × Q (e.g., height × width). For graph learning tasks, D = G = (X, A), where X ∈RN×d denotes d-dimensional features for N nodes and A ∈RN×N represents the adjacency matrix. Each sample ξi ∈D has a label yi ∈Y, which may be corrupted by noise during the labeling process. We denote Yc and Yn as the clean and noisy counterparts of Y respectively.

## Analysis

of IB Theory with Label Noise. In the traditional IB, I(X; Z) encourages minimal representations by compressing the input, while I(Y; Z) ensures sufficiency by preserving task-relevant information. However, when the label Y is corrupted by noise, maximizing I(Y; Z) is equivalent to maximizing I(Yc, Yn; Z), which inadvertently causes the learned representation Z to capture noise Yn, thus compromising robustness and degrading performance.

In this study, we aim to mitigate the negative impact of label noise on model performance while preserving the “Minimal-Sufficient” property of the IB method. Ideally, we consider a robust IB method MIB that, given a dataset (D, Y) where Y consists of both clean labels yi ∈Yc and noisy labels yj ∈Yn, aims to satisfy the following objective:

min −I(Z; Yc) + βI(Z; D)

s.t. Z = MIB(D, Y). (3)

22085

<!-- Page 3 -->

𝜇ௌ 𝜎ௌ 𝜇் 𝜎்

ොݕௌ ොݕ்

𝑌𝑐 𝑌ܵܶ

𝐷𝐽ௌ

𝐷𝐽ௌ: Reveal the difference in noise capacity݁݊ܿ

݋݀݁ ݎܵ݁݊ܿ ݋݀݁ ݎܶܵ

∼ݍሺݏ|ݔሻ →𝑁ሺ𝜇ௌ, 𝜎ௌሻܶ

∼ݍሺݐ|ݔሻ →𝑁ሺ𝜇், 𝜎்ሻ݀݁ܿ

݋݀݁ ݎ

Training Path Inference Path

ሺ𝓓, 𝒀ሻ

Clean Sample 𝑦= 𝑦𝑐

Noisy Sample 𝑦= 𝑦𝑛

Label-Noise Resistant Information Bottleneck (LaT-IB)

Sufficient Minimal Clean min 𝐼𝑌;ܵ,ܶ + ߚ𝐼𝒟;ܵ,ܶ + ߛ𝐼ܵ;ܶ 𝑌 s.t. max 𝐼𝑌𝑛;ܵ, 𝐼𝑌𝑐;ܶ ≤𝐾

𝐾= max 𝐼ܵ;ܶ, 𝜀 2ܵ

Clean Label

Spaceܶ

Noisy Label

Space

Preserve

Disentangle

Compress

Progressive Representation

Disentanglement

𝑃

𝑌 𝑦𝑐 𝑦𝑛

𝑃

𝑌 𝑦𝑐 𝑦𝑛

𝑃

𝑌 𝑦𝑐 𝑦𝑛

## 1. Warmup

## 3. Robust Training

𝒟ܵ ො𝑦ௌ 𝑌

## 2. Knowledge Injection

𝒟ܵ

ො𝑦ௌ𝑌′ܶ ො𝑦்

InfoJS

Selector

𝒟ܵ

ො𝑦ௌ 𝑌ܶ ො𝑦்

ො𝑦

MSC Representation

Data Pipeline Method

Period1,2 Period3

𝑌 𝒟

**Figure 2.** Left: The overall LaT-IB model architecture with dual encoders for extracting features from clean (S) and noisy (T) label spaces, and a shared decoder. Right: An illustration of the LaT-IB method, which disentangles representations to extract “Minimal-Sufficient-Clean” features. Specifically, its pipeline consists of three period: Warmup, Knowledge Injection and Robust Training, which transform Eq. (8) from a theoretical formulation into a practical training procedure.

Compared to the traditional IB objective, the goal of Eq. (3) is to maximize the MI between the learned representation and the clean labels Yc, rather than with all observed labels Y. However, whether each label is clean or noisy is unknown. In the next section, we introduce a concrete solution to mitigate IB’s vulnerability to label noise.

## 4 Methodology In this paper, we propose Label-Noise Resistant Information

Bottleneck (LaT-IB), along with theoretical formulation, model architecture and a tailored training framework, as illustrated in Figure 2. We begin by presenting the formal objective of LaT-IB and interpreting its theoretical implications. To enable efficient optimization, we derive upper and lower bounds that simplify the objective, effectively bridging the gap between theory and practice. Finally, drawing on key insights, we design a three-phase training framework: Warmup, Knowledge Injection and Robust Training, clarify the role of each phase and facilitate the progressive disentanglement of clean and noise-related representations.

## 4.1 Label-Noise Resistant Information Bottleneck

In real-world datasets, each training sample may have either a clean or a corrupted label, and sometimes both possibilities coexist probabilistically. Using a unified representation for all samples under such ambiguity can cause conflicting features and hurt downstream tasks. To mitigate this, we disentangle the representation into two parts: S under the clean label space, and T under the noise space. Under this disentanglement, the objective in Eq. (3) can be reformulated as:

min −I(S; Yc) + I(D; S, T). (4)

Since only Y are available in the dataset, we implicitly associate it with the joint representation of S and T, where disentanglement is encouraged by min I(S; T|Y). A successful disentanglement implies that S and T encode conditionally independent given Y, capturing distinct semantics. With β and γ as balancing factors, the LaT-IB is formulated as:

min −I(Y; S, T) | {z } prediction term

+β I(D; S, T) | {z } compression term

+γ I(S; T|Y) | {z } disentanglement term

, (5)

However, Eq. (5) still cannot map S to clean features and T to noise features. To address this and further explore its representational meaning, we introduce two lemmas below.

Lemma 4.1 (Nuisance Invariance). Taking the part of D that does not contribute to Y as Dn (Dn is independent of Y), and considering the Markov chain (Y, Dn) →D → (S, T), the following inequality holds:

I(Dn; S, T) ≤−I(Y; S, T) + I(D; S, T). (6)

Lemma 4.2 (Feature Convergence). Assuming that Y can potentially contain all information about Yc and Yn, the following inequality holds when max(I(Yn; S), I(Yc; T)) ≤ max(I(S; T), ε)/2 = K, ε > 0, ε ∈R is satisfied:

−I(Yc; S)−I(Yn; T)−ε ≤−I(Y; S, T)+I(S; T|Y). (7)

The detailed proofs of these lemmas can be found in Appendix C.2. Lemma 4.1 demonstrates that optimizing min −I(Y; S, T)+I(D; S, T) in Eq. (5) (β = 1) essentially reduces the model’s tendency to learn features irrelevant to Y (denoted as Dn). Lemma 4.2 further indicates that, when the MI terms I(Yn, S) and I(Yc, T) are sufficiently small, optimizing min −I(Y; S, T)+I(S, T|Y) in Eq. (5) (γ = 1) effectively strengthens the mapping relationships S →Yc and T →Yn. Based on these insights, we can first ensure the conditions in Lemma 4.2 then optimize the main objective in Eq. (5) as a form of progressive representation disentanglement. This enables the model to separate clean and noisy features while avoiding learning irrelevant noise Dn.

By combining Lemma 4.1 and Lemma 4.2, we obtain a principled training objective that integrates sufficiency, com-

22086

![Figure extracted from page 3](2026-AAAI-is-the-information-bottleneck-robust-enough-towards-label-noise-resistant-inform/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-is-the-information-bottleneck-robust-enough-towards-label-noise-resistant-inform/page-003-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

pression, and clean-noise disentanglement:

min −I(Y; S, T) | {z } Sufficient

+β I(D; S, T) | {z } Minimal

+γ I(S; T|Y) | {z } Clean s.t. max(I(Yn; S), I(Yc; T)) ≤K | {z } Clean

. (8)

## 4.2 Bound Analysis and Implementation

Building on the formulation introduced in the previous section, we now turn to the optimization of the proposed objective in Eq. (8). Since directly optimizing the multivariate MI is intractable, we first simplify the original objective by analyzing upper and lower bounds of MI, and then present the implementation strategy for each term. All proposition proofs are provided in the Appendix C.3. Proposition 4.1 (The upper bound of −I(Y; S, T)). Given the label Y and the variable S, T that learns the characteristics of the clean label space and the noisy label space respectively, we have:

−I(Y; S, T) ≤−max (I(Y; S), I(Y; T)). (9) Intuitively, Eq. (9) encourages encoders to focus on learning its own knowledge, ensuring consistency in the learned representation. Further, since MI terms are intractable, each I(Y, Z) with Z ∈{S, T} is lower-bounded by the crossentropy loss using a variational approximation qθ(y|z):

I(Y; Z) ≥Ep(y,z) (log(qθ(y|z))):= −LCE(Z, Y), (10)

Proposition 4.2 (The upper bound of I(D; S, T)). Let D, S, T be random variables. Assume the probabilistic mapping p(D, S, T) follows the Markov chain S ↔D ↔T. Then:

I(D; S, T) ≤I(D; S) + I(D; T). (11) The implementation of each term I(D; ·) remains consistent with that in VIB (Alemi et al. 2017) and GIB (Wu et al. 2020), achieved by minimizing the KL divergence between the variational posterior q(·|D) and the prior p(·). Proposition 4.3 (Reformulation of I(S, T|Y)). Given the label Y and the variable S, T, minimizing I(S; T|Y) is equivalent to minimize I(S, Y; T, Y).

The Proposition 4.3 achieves the tractable transformation of conditional MI theoretically. However, minimizing the term I(S, Y; T, Y) = DKL q(S, T, Y)||q(S, Y)q(T, Y)

is intractable since both distributions involve mixtures with many components. Therefore, we use the density-ratio trick (Sugiyama, Suzuki, and Kanamori 2012) by introducing a discriminator d, that learns to distinguish between samples from the joint distribution q(s, t, y) and those from the product of marginals q(s, y)q(t, y). In particular, we sample negative pairs ((s, y), (t, y′)) from q(s, y)q(t, y), where (s, y) and (t, y′) are drawn independently, and positive pairs ((s, y), (t, y)) from the joint distribution q(s, t, y), where both s and t correspond to the same sample. The discriminator d((s, y), (t, y′)) is trained to output the probability that a given pair comes from the joint distribution, and the objective is to minimize the MI by solving the following problem:

min q max d Eq(s,y)q(t,y) log d((s, y), (t, y′))

+Eq(s,t,y) log(1 −d((s, y), (t, y))).

(12)

When the discriminator cannot distinguish between joint and independent samples, the MI is effectively minimized. Proposition 4.4 (Reformulation of the condition in Eq. (8): max(I(Yn; S), I(Yc; T)) ≤K). Minimizing I(Yc; T) and I(Yn; S) is equivalent to maximize I(Yn; T) and I(Yc; S).

Proposition 4.4 relaxes the condition in Eq. (8). Since the original MI calculation is mismatched and thus intractable, the relaxed formulation provides a tractable alternative that can be optimized efficiently, as described in Eq. (10).

## 4.3 Principle to Practice: LaT-IB Framework

Based on the theoretical analysis above, this section introduces the practical implementation of LaT-IB. To optimize the objective in Eq. (8), we adopt a three-phase training framework to progressively disentangle the representation. Specifically, we first introduce a Warmup period to provide the model with initial discriminative ability. Building on this, a Knowledge Injection period enforces the constraint by applying InfoJS selector, guiding the learning of encoderS/T via selected samples. Finally the Robust Training period focuses on optimizing the complete objective with prior knowledge, refining the model’s robustness.

Feature-Decomposed Dual Encoder Architecture Design. Based on the Observation 4.1, we adopt the Jensen- Shannon (JS) divergence as a metric to evaluate the noise retention capacity of the two encoders. Observation 4.1. With the decoder kept fixed, we train the encoder using datasets that share the same input X but differ in the level of label noise in Y. As the noise gap between the two datasets increases, the divergence between the resulting encodings from the encoder also becomes larger.

Accordingly, Figure 2 illustrates the overall architecture of the LaT-IB: the model is designed with a dual-encoder, single-decoder framework, where the two encoders extract features S and T, respectively. Each encoder maps the input features to a high-dimensional Gaussian distribution, and the embeddings are sampled using the reparameterization trick.

Phase 1: Warmup with Discriminative Learning under Noise. To address the problem of noise memorization during training, we introduce a Warmup phase where the model builds basic discriminative ability. Specifically, we pretrain the clean encoder encoderS using the full dataset, providing a foundation for more effective separation of clean and noisy samples in subsequent stages. The loss function in Warmup period is defined based on prediction ˆyS:

LW armup = LCE(decoder(S), Y) = LCE(ˆyS, y). (13) Noise-Aware Sample Selection. Since the variables Yc and Yn are unobservable, we approximate the constraint max(I(Yn; S), I(Yc; T)) ≤K in Eq. (8) by selecting a partial set of confident samples to act as proxies for clean and noisy labels. Samples are then grouped into three categories for training: Clean Set, Noise Set, and Uncertain Set. Observation 4.2. For two different encoders, samples with more consistent predictions after passing through the decoder tend to have smaller divergence between their embeddings. In contrast, samples with inconsistent predictions correspond to larger embedding divergence.

22087

<!-- Page 5 -->

Observation 4.2 suggests that the divergence between encoders can be used to identify clean samples. Moreover, prior studies (Arpit et al. 2017; Song et al. 2019) have shown that models tend to fit clean samples earlier. Based on these insights, we designed the InfoJS selector as detailed in Algorithm B.2, which identifies clean (noisy) samples as those with MI between S and Y being in the top δ% (bottom δ%) and JS divergence between S and T in the bottom δ% (top δ%), respectively. Unselected samples are treated as the uncertain set. Labels are assigned as follows: y′ = y for Clean and Noise Sets, and y′ = g(ˆyS)/g(ˆyT) for Uncertain Set when training the encoderS/T, where g denotes either a debiasing function (Menon et al. 2020) or one-hot mapping.

However, the InfoJS selector performs selection based on relative feature scores. To improve the quality of each set, we further enrich the sample composition by incorporating predicted confidence scores as an absolute criterion.

Phase 2: Knowledge Injection to Disentangle Representations. Once the model has acquired basic discriminative ability, we proceed to optimize the objective in Eq. (8). Given the condition and its reformulated form:

max(I(Yn; S), I(Yc; T)) ≤K | {z } The original constraint in Eq. (8) ⇒max(I(Yn; T)), max(I(Yc; S)) | {z } The reformulated constraint in Proposition 4.4

, (14)

to satisfy the constraint, we introduce a Knowledge Injection phase to encourage the encoderS,T to learn disentangled representations. Furthermore, to enforce difference in noise representation between the two encoders, we incorporate the JS divergence DJS based on Observation 4.1:   

 

LClean = LCE(ˆyS, y′) −DJS(s ∥t),

LUncertain = LCE(ˆyS, y′) + LCE(ˆyT, y′) + DJS(s ∥t),

LNoise = LCE(ˆyT, y′) −DJS(s ∥t),

(15) For Clean and Noise Sets, divergence is maximized to increase encoder discrepancy; and for the Uncertain set, divergence is minimized to guide T towards meaningful patterns. It is worth noting that the Uncertain set is much smaller, thus has limited influence on the encoders’ training process.

Empirically, minimizing the I(D; S, T) helps to leading to a more robust encoding space. To progressively disentangle the representation and achieve a minimal representation, we introduce a regularization term LMinimal that approximates the min I(D; S, T) term base on Proposition 4.2, and incorporate it into the loss function during the Knowledge Injection period to learn a compact representation:

LInjection = LClean + LUncertain + LNoise + LMinimal.

(16) This facilitates a smoother transition to the third Robust Training stage. The implementation details of LMinimal are provided in the Appendix D.1.

Phase 3: Robust Training for Representation Consistency. The Warmup stage establishes initial discriminative ability, while Knowledge Injection realized constraint to guide the model toward informative and reliable samples. To further disentangle and enhance representation robustness under label noise, this period focuses on optimizing the full objective in Eq. (5): min −I(Y; S, T) + I(D; S, T) + I(S; T|Y), aiming to learn noise consistent representations.

Section 4.2 has introduced the implementation of each objective term. Among them we propose LConCE to optimize the term I(Y; S, T) based Eq. (9) and (10):

LConCE ←

X min(LCE(ˆyS, y), LCE(ˆyT, y)), (17)

encouraging consistency between encoders and clean/noisy labels. Detailed formulations are provided in Appendix B.1.

The loss function for the Robust Training period is:

LRobust = 1

|B|

B X i=1

[ LConCE(ˆyS, ˆyT, y) | {z } Eq. (17)

+β LMinimal | {z } Eq. (11)

−γ log d(si, yi; ti, yi) | {z } Proposition 4.3, Eq. (12)

],

(18) where B denotes a training batch. In addition, we alternately update the discriminator d based on Eq. (12), using a random permutation π to approximate the marginal distribution:

Ld = 1

|B|

B X i=1

−log(1 −d(si, yi; tπ(i), yπ(i)))

−log d(si, yi; ti, yi).

(19)

## Experiment

In this section, we conduct extensive experiments to evaluate the robustness and efficiency of the LaT-IB under diverse tasks and various types of noise, including real-world and synthetic label noise, as well as adversarial perturbation. 1

## 5.1 Experimental Settings

Datasets. We evaluate the proposed LaT-IB method on multiple datasets. For image classification, we utilize the CI- FARN (Wei et al. 2022), Animal-10N (Song, Kim, and Lee 2019) and CIFAR (Krizhevsky, Hinton et al. 2009) datasets. For node classification tasks, we evaluate on Cora, Citeseer, Pubmed (Sen et al. 2008), and DBLP (Pan et al. 2016). More descriptions about datasets are provided in Appendix E.1.

Baselines. We compare our LaT-IB with four categories, 16 baselines in two scenarios: ①Classic IB methods; ②IB with robust loss functions; ③Improved IB variants; ④Twostage denoising + IB methods. They comprehensively evaluate our LaT-IB’s performance from multiple perspectives.

Label Noise Settings. To evaluate the robustness of LaT- IB and baselines against label noise, we conduct experiments in both image and graph classification tasks. For image classification, we evaluate on both real-world noisy datasets and synthetic settings with symmetric and asymmetric label noise, simulated using custom transition matrices as described in (Xiao et al. 2023). For node classification, we follow the protocol in (Wang et al. 2024) to inject uniform and pairwise label noise into graph labels.

1Code available at: https://github.com/RingBDStack/LaT-IB

22088

<!-- Page 6 -->

## Method

## Model

CIFAR-10N CIFAR-100N Animal

-10N aggre rand1 rand2 rand3 worst noisy100

Classic

IB

VIB 86.11±0.34 83.69±0.50 83.69±0.46 83.76±0.29 73.80±0.59 53.29±0.09 76.28±0.51 NIB 85.21±0.44 84.03±1.43 81.98±0.68 82.39±0.43 73.51±0.82 48.11±0.40 75.62±0.64

Robust

Loss

VIB (LGCE) 85.70±0.08 84.32±0.50 83.97±0.38 84.25±0.68 78.88±0.27 — 81.72±1.77 VIB (LSCE) 83.95±0.10 82.65±0.25 82.84±0.31 82.50±0.24 73.81±1.54 50.71±0.14 77.17±0.44

Improved

IB

SIB 89.99±0.08 84.75±1.04 85.07±0.72 85.39±0.50 70.58±0.50 50.82±0.41 83.95±0.14 DT-JSCC 85.46±0.44 81.85±0.66 81.14±0.55 81.03±0.34 69.73±1.15 43.61±0.19 78.98±0.23

Deniose

+ IB

JoCoR+VIB 86.39±0.18 86.45±0.02 86.53±0.29 86.60±0.11 81.65±0.15 54.24±0.18 75.45±0.27 (ELR+)+VIB 92.65±0.27 92.09±0.25 92.01±0.20 91.93±0.15 86.68±0.25 61.06±0.34 85.87±0.15 Promix+VIB 92.35±0.38 92.59±0.40 92.42±0.17 92.54±0.21 91.24±0.28 63.91±0.19 85.47±0.51

Ours LaT-IB 94.17±0.12 93.25±0.11 93.19±0.09 93.03±0.11 87.95±0.22 63.59±0.67 88.49±0.11

**Table 2.** Classification accuracy (%) on the CIFAR-10N/100N and Animal-10N dataset. All the best results are highlighted in bold, and the second-best results are underlined.

## Method

## Model

Clean Uniform Noise Pair Noise

10% 20% 30% 40% 10% 20% 30% 40%

Classic GIB 71.57±1.18 70.50±1.85 64.30±6.45 63.90±3.51 62.67±1.35 68.67±3.47 61.30±14.57 67.53±4.77 55.57±14.33

Robust

Loss

GIB (LGCE) 69.93±0.69 67.43±3.21 61.67±7.19 47.80±18.62 43.47±14.50 50.93±0.52 55.33±11.23 62.37±6.99 36.90±15.23 GIB (LSCE) 72.53±0.12 70.17±2.10 71.63±2.05 62.90±8.09 51.87±6.03 69.30±1.66 68.23±3.41 65.13±5.02 51.13±11.30

Improv- ed IB

CurvGIB 64.63±5.28 65.67±5.85 54.67±10.09 54.00±2.41 54.97±2.78 59.97±9.00 62.07±5.15 66.63±1.94 54.57±1.25 IS-GIB 71.00±1.22 69.97±1.41 64.30±2.30 59.77±3.70 53.77±4.41 64.83±2.34 62.50±1.51 62.50±1.31 55.40±4.74

Denoise

+ IB

RNCGLN+GIB 70.57±0.99 69.50±0.86 63.43±5.90 62.83±4.15 53.27±14.47 69.90±1.69 68.20±2.14 66.47±3.21 56.77±15.11 CGNN+GIB 71.87±1.99 68.97±3.09 65.47±4.77 64.93±2.46 48.83±6.48 59.03±12.67 69.77±1.77 68.50±2.83 53.93±13.85

Ours LaT-IB 74.97±0.68 74.90±2.09 73.40±2.62 70.50±3.86 72.20±4.22 75.63±0.46 73.03±1.77 70.07±3.20 68.77±2.29

**Table 3.** Classification accuracy (%) on the Pubmed dataset under different noise types and noise rates. All the best results are highlighted in bold, and the second-best results are underlined.

Adversarial Attack Settings. As discussed in Appendix D.1, the implementation of I(D; S, T) in our LaT-IB framework aligns with prior work VIB and GIB, thereby theoretically inheriting their robustness properties. To empirically verify this claim, we evaluate LaT-IB’s performance under adversarial perturbations in the image classification setting. Specifically, we adopt the FGSM (Goodfellow, Shlens, and Szegedy 2015) attack to perturb input images with ε ∈ {0.05, 0.1, 0.2}, controlling the perturbation strength. Combined with noisy labels during training, this setup evaluate the robustness of model under compound noise conditions.

## 5.2 Robustness Against Label Noise

In this section, we evaluate the representation capability of our proposed method under various label noise conditions. Specifically, we investigate whether the LaT-IB model can effectively learn robust representations when trained on data corrupted by different types and levels of label noise.

Results. In most scenarios, our proposed LaT-IB method outperforms other baseline approaches as shown in Table 2 and 3. In certain cases, however, methods that first perform denoising and then apply IB achieve better results, likely due to the strong denoising capacity of those models. Nev- ertheless, such two-stage methods involve longer training pipelines and are more vulnerable to adversarial attacks, as will be demonstrated in the next section. Additional experimental results on label noise are shown in Appendix E.

## 5.3 Robustness Against Adversarial Perturbations

In this section, to further validate the “Minimal-Sufficient” property in MSC of the proposed LaT-IB method, we apply perturbations to the input data D. The perturbed data is then fed into models trained under noisy label settings. This setup enables a comprehensive evaluation of model robustness against diverse noise, including inputs and labels.

Results. The results demonstrate that the LaT-IB method exhibits strong robustness against adversarial attacks, significantly outperforming other approaches, as shown in Table 4. Notably, two-stage methods suffer a substantial performance drop under attack due to the increased number of vulnerable components, further highlighting their limitations.

## 5.4 Ablation Study In this section, we analyze the effectiveness of different training stages in the

LaT-IB framework. To investigate the

22089

<!-- Page 7 -->

## Model

CIFAR-10N (aggre) CIFAR-10N (worst)

No attack ε = 0.05 ε = 0.1 ε = 0.2 No attack ε = 0.05 ε = 0.1 ε = 0.2

VIB 86.11±0.34 52.33±1.55 43.18±2.10 36.63±1.10 73.80±0.59 43.29±2.36 36.56±3.28 32.17±3.27 VIB (LGCE) 85.70±0.08 54.15±1.85 44.84±3.00 34.72±2.43 78.88±0.27 43.27±1.56 31.24±1.42 24.23±1.45 SIB 89.99±0.08 56.48±2.50 46.62±2.41 38.14±2.37 70.58±0.50 43.39±2.83 33.40±2.87 27.89±2.93 (ELR+)+VIB 92.65±0.27 39.88±0.74 23.16±0.40 14.60±0.39 86.68±0.25 42.72±0.24 26.44±0.64 14.70±0.70 Promix+VIB 92.35±0.38 51.27±1.53 36.43±0.65 20.49±1.79 91.24±0.28 52.88±1.46 36.05±0.68 23.79±0.14 LaT-IB 94.17±0.12 69.38±1.23 60.66±2.03 49.64±2.27 87.95±0.22 64.36±1.67 54.18±2.53 43.91±3.05

**Table 4.** Classification accuracy (%) on CIFAR-10N (aggre and worst) under different adversarial perturbation levels. For Denoise + IB methods, adversarial attacks are applied in both stages: the VIB model is trained using the output of a denoising model that has itself been attacked. All the best results are highlighted in bold, and the second-best results are underlined.

rand1

CIFAR10N worst sym-0.2

CIFAR100 noisy100 55 60 65 70 75 80 85 90 95

Accuracy (%)

LaT-IB LaT-IB w/o KI LaT-IB w/o RT uni-0.2

DBLP pair-0.2 uni-0.4 pair-0.4 45 50 55 60 65 70 75 80

Accuracy (%)

LaT-IB LaT-IB w/o KI LaT-IB w/o RT

Pubmed

**Figure 3.** Ablation study.

role of each phase in enhancing model robustness, we design two ablated variants:

• LaT-IB (w/o KI): We remove the Knowledge Injection period, thus max(I(Yn; S), I(Yc; T)) ≤K is not satisfied. weakening the ability to map S →Yc and T →Yn. • LaT-IB (w/o RT): We remove the Robust Training period, meaning no further enhancement is applied to the representations from S, T. The LaT-IB model can only gain partial information from the three subsets. Note that we do not design an ablation variant without the Warmup period, as it is essential for establishing basic classification capability and stable later training.

Results. Overall, the full LaT-IB method achieves the best performance under all noisy label settings as shown in Figure 3, demonstrating the importance of different periods in the framework. For image classification tasks (with larger samples), the Robust Training stage is particularly critical, while for graph-based tasks (with fewer samples), the Knowledge Injection stage proves more influential. These findings highlight the necessity of each training stage in achieving robust representations under noisy supervision.

## 5.5 Hyperparameter Sensitivity Analysis

We analyze the sensitivity of the model to the hyperparameter β, γ and δ. The coefficient β controls the feature compression term I(D; S, T), which encourages the model to learn noise invariant features. The coefficient γ controls the feature separation term I(S; T|Y), which encourages the encoderS,T to capture clean and noisy representations respectively. δ regulates how much information the encoderS,T learns during the Knowledge Injection phase.

1e-1 1e-2 1e-3 1e-4 1e-5 β

0

20

40

60

80

Accuracy (%)

CIFAR-10N (worst) CIFAR-100 (sym 0.5)

1e0 1e-1 1e-2 1e-3 1e-4 γ

65

70

75

80

85

Accuracy (%)

CIFAR-10N (worst) CIFAR-100 (sym 0.5)

**Figure 4.** The influence of β and γ.

Results. We observe that a large β can dominate training and cause collapse as shown in Figure 4, indicating that I(D; S, T) partially limits the model’s expressiveness. However, our method is more tolerant to β than the original VIB, which fails to train on CIFAR-10 with 50% symmetric noise at β = 0.01. In contrast, our model performs better as β decreases because the input compression level is reduced.

We also observe that the model’s sensitivity to γ varies across noisy settings, highlighting the importance of the separation term I(S; T|Y) under different types of noise.

For δ, a too-small δ limits the encoder’s training data exposure, while a too-large δ causes the encoders to converge, reducing their ability to separate clean and noisy information. More detailed results in Appendix E.6.

## 6 Conclusion

In this work, we propose LaT-IB, a novel yet principled IB framework that enables robust representation learning under label noise while preserving the principle of learning minimally sufficient representations. We disentangle features into representations related to clean and noisy label spaces, and theoretically demonstrate the noise-separating effect of our method through upper and lower bounds analysis. Furthermore, we design a three-phase training framework comprising Warmup, Knowledge Injection and Robust Training, that facilitates the extraction of “Minimal-Sufficient-Clean” representations. Extensive experiments across diverse noisy environments validate the superior performance of LaT-IB compared to existing IB-based methods, highlighting its potential to efficiently advance the practical application of IB theory in real-world learning scenarios with label noise.

22090

<!-- Page 8 -->

## Acknowledgments

The corresponding author is Qingyun Sun. This work is supported by NSFC under grants No.62427808 and No.62225202, and by the Fundamental Research Funds for the Central Universities. We extend our sincere thanks to all reviewers for their valuable efforts.

## References

Alemi, A. A.; Fischer, I.; Dillon, J. V.; and Murphy, K. 2017. Deep Variational Information Bottleneck. In ICLR. Arpit, D.; Jastrzebski, S.; Ballas, N.; Krueger, D.; Bengio, E.; Kanwal, M. S.; Maharaj, T.; Fischer, A.; Courville, A.; Bengio, Y.; et al. 2017. A closer look at memorization in deep networks. In ICML, 233–242. Goodfellow, I. J.; Shlens, J.; and Szegedy, C. 2015. Explaining and Harnessing Adversarial Examples. In ICLR. Harris, E.; Marcu, A.; Painter, M.; Niranjan, M.; Pr¨ugel- Bennett, A.; and Hare, J. 2020. Fmix: Enhancing mixed sample data augmentation. arXiv preprint arXiv:2002.12047. Hu, S.; Lou, Z.; Yan, X.; and Ye, Y. 2024. A survey on information bottleneck. IEEE Transactions on Pattern Analysis and Machine Intelligence. Krizhevsky, A.; Hinton, G.; et al. 2009. Learning multiple layers of features from tiny images. Li, B.; Xie, X.; Lei, H.; Fang, R.; and Kang, Z. 2025. Simplified PCNet with robustness. Neural Networks, 184: 107099. Liu, S.; Niles-Weed, J.; Razavian, N.; and Fernandez- Granda, C. 2020. Early-learning regularization prevents memorization of noisy labels. NeurIPS, 33: 20331–20342. Menon, A. K.; Jayasumana, S.; Rawat, A. S.; Jain, H.; Veit, A.; and Kumar, S. 2020. Long-tail learning via logit adjustment. arXiv preprint arXiv:2007.07314. Pan, S.; Wu, J.; Zhu, X.; Zhang, C.; and Wang, Y. 2016. Triparty deep network representation. In IJCAI, 1895–1901. Pan, Z.; Niu, L.; Zhang, J.; and Zhang, L. 2021. Disentangled information bottleneck. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, 9285– 9293. Patel, D.; and Sastry, P. 2023. Adaptive sample selection for robust learning under label noise. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 3932–3942. Pensia, A.; Jog, V.; and Loh, P.-L. 2020. Extracting robust and accurate features via a robust information bottleneck. IEEE Journal on Selected Areas in Information Theory, 1(1): 131–144. Sen, P.; Namata, G.; Bilgic, M.; Getoor, L.; Galligher, B.; and Eliassi-Rad, T. 2008. Collective classification in network data. AI magazine, 29(3): 93–93. Shamir, O.; Sabato, S.; and Tishby, N. 2010. Learning and generalization with the information bottleneck. Theoretical Computer Science, 411(29-30): 2696–2711. Song, H.; Kim, M.; and Lee, J.-G. 2019. Selfie: Refurbishing unclean samples for robust deep learning. In ICML, 5907– 5915.

Song, H.; Kim, M.; Park, D.; and Lee, J.-G. 2019. How does early stopping help generalization against label noise? arXiv preprint arXiv:1911.08059. Song, H.; Kim, M.; Park, D.; Shin, Y.; and Lee, J.-G. 2022. Learning from noisy labels with deep neural networks: A survey. IEEE transactions on neural networks and learning systems, 34(11): 8135–8153. Sugiyama, M.; Suzuki, T.; and Kanamori, T. 2012. Densityratio matching under the bregman divergence: a unified framework of density-ratio estimation. Annals of the Institute of Statistical Mathematics, 64: 1009–1044. Tishby, N.; Pereira, F. C.; and Bialek, W. 2000. The information bottleneck method. arXiv preprint physics/0004057. Wang, Y.; Ma, X.; Chen, Z.; Luo, Y.; Yi, J.; and Bailey, J. 2019. Symmetric cross entropy for robust learning with noisy labels. In Proceedings of the IEEE/CVF international conference on computer vision, 322–330. Wang, Z.; Sun, D.; Zhou, S.; Wang, H.; Fan, J.; Huang, L.; and Bu, J. 2024. NoisyGL: A Comprehensive Benchmark for Graph Neural Networks under Label Noise. arXiv preprint arXiv:2406.04299. Wei, H.; Feng, L.; Chen, X.; and An, B. 2020. Combating noisy labels by agreement: A joint training method with coregularization. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 13726–13735. Wei, J.; Zhu, Z.; Cheng, H.; Liu, T.; Niu, G.; and Liu, Y. 2022. Learning with Noisy Labels Revisited: A Study Using Real-World Human Annotations. In ICLR. Wu, T.; Ren, H.; Li, P.; and Leskovec, J. 2020. Graph information bottleneck. NeurIPS, 33: 20437–20448. Xiao, R.; Dong, Y.; Wang, H.; Feng, L.; Wu, R.; Chen, G.; and Zhao, J. 2023. ProMix: combating label noise via maximizing clean sample utility. In Proceedings of the Thirty- Second IJCAI, 4442–4450. Xie, S.; Ma, S.; Ding, M.; Shi, Y.; Tang, M.; and Wu, Y. 2023. Robust information bottleneck for task-oriented communication with digital modulation. IEEE Journal on Selected Areas in Communications, 41(8): 2577–2591. Yuan, H.; Sun, Q.; Fu, X.; Ji, C.; and Li, J. 2024. Dynamic graph information bottleneck. In Proceedings of the ACM Web Conference 2024, 469–480. Zhang, H.; Cisse, M.; Dauphin, Y. N.; and Lopez-Paz, D. 2018. mixup: Beyond Empirical Risk Minimization. In ICLR. Zhang, Z.; and Sabuncu, M. 2018. Generalized cross entropy loss for training deep neural networks with noisy labels. NeurIPS, 31. Zhou, Z.; Yao, J.; Liu, J.; Guo, X.; Yao, Q.; He, L.; Wang, L.; Zheng, B.; and Han, B. 2023. Combating bilateral edge noise for robust link prediction. NeurIPS, 36: 21368–21414.

22091
