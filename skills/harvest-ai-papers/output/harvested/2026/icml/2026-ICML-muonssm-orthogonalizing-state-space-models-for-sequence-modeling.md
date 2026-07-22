---
title: "MuonSSM: Orthogonalizing State Space Models for Sequence Modeling"
source_url: https://icml.cc/virtual/2026/oral/71058
paper_pdf_url: https://arxiv.org/pdf/2606.30461v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

<!-- Page 1 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Thai-Khanh Nguyen * 1 Ngoc-Bich-Uyen Vo * 2 Thieu N. Vo † 3 Tan M. Nguyen † 4 Cuong Pham † 2

## Abstract

State space models (SSMs) have emerged as efficient linear-time alternatives to attention for longsequence modeling. However, existing SSMs often suffer from instability and memory degradation over extended horizons due to poorly conditioned first-order updates and unbalanced update geometry. We introduce MuonSSM, a general framework that stabilizes SSM training by explicitly conditioning the geometry of memory updates rather than the recurrent transition matrix. MuonSSM augments SSMs with a momentumbased pathway and a lightweight Newton–Schulz transformation on low-rank input injections, yielding bounded and spectrally conditioned updates while preserving parallel scan complexity. Theory shows that MuonSSM improves gradient propagation, mitigates spectral amplification, and enriches memory representations over long horizons. Extensive experiments across language, vision, and time-series benchmarks show consistent gains in accuracy, robustness, and long-context performance when integrated into diverse SSM backbones. These results establish geometric conditioning of updates as a principled pathway to stable, scalable sequence modeling.

## 1. Introduction

Modeling sequences efficiently and reliably remains a central challenge in modern machine learning. Transformerbased architectures have achieved strong empirical success (Vaswani et al., 2017), but their quadratic complexity in sequence length limits scalability as contexts grow (Tay

∗Equal contribution †Co-last authors 1Faculty of Information Technology, Dainam University, Hanoi University of Science and Technology, Hanoi 10000, Vietnam 2Faculty of Artificial Intelligence, Posts and Telecommunications Institute of Technology, Hanoi 10000, Vietnam 3Department of Computer Science, University of Bath, Bath BA2 7AY, UK 4Departments of Mathematics, National University of Singapore, Singapore 119076, Singapore. Correspondence to: Tan M. Nguyen <tanmn@nus.edu.sg>, Cuong Pham <cuongpv@ptit.edu.vn>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

et al., 2020). This has renewed interest in state space models (SSMs), which offer linear-time alternatives based on recurrent or scan-based dynamics. Starting from S4 (Gu et al., 2021; 2020) and followed by architectures H3 (Fu et al., 2022), S5 (Smith et al., 2022), and Mamba (Gu & Dao, 2024), modern SSMs combine strong performance with hardware-efficient selective scans, making them a promising replacement for attention-based models on long sequences. Despite their efficiency, scan-friendly SSMs can degrade over long horizons and deep stacks: common inputdependent affine updates remain fundamentally first-order and can suffer from poor long-range signal propagation and optimization instability (Dao & Gu, 2024; Pascanu et al., 2013). Recent variants mitigate this mainly via gating/normalization or input-dependent scaling (Liu et al., 2024; Yang et al., 2024a;b), which helps control magnitudes but does not introduce temporal inertia nor explicitly condition the geometry of accumulated updates. In this work, we propose MuonSSM1, a framework for stabilizing state space memory by augmenting SSMs with explicit momentum in their update dynamics. Our core insight is that memory updates in SSMs can be viewed through an online learning lens (Behrouz et al., 2025b; 2024): just as momentum methods improve optimization by accumulating gradient directions over time, introducing temporal inertia into state updates can improve long-horizon information propagation (Nguyen et al., 2020; Ma et al., 2022). Muon- SSM incorporates a lightweight momentum pathway to accumulate update directions across timesteps, together with a parallelizable normalization of input-dependent updates to maintain well-conditioned memory evolution. Importantly, these modifications preserve the affine structure required for efficient parallel scans and do not increase asymptotic computational complexity. Contributions. Our contributions are threefold: (i) We introduce MuonSSM, a family of SSMs that integrate momentum-based second-order dynamics and implicit spectral conditioning into scan-based recurrence;

1The name MuonSSM reflects conceptual inspiration from the Muon optimizer (Jordan et al., 2024), which demonstrated the practical effectiveness of geometric conditioning for stabilizing optimization. Unlike Muon, which acts on parameter gradients, MuonSSM applies this principle directly within state space memory updates.

arXiv:2606.30461v1 [cs.LG] 29 Jun 2026

<!-- Page 2 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Table 1.** Special cases of recent SSMs recovered from the general associative memory update in Eq. (1).

## Model

αt βt η Update Rule

Mamba (Gu & Dao, 2024) αt 1 0 St = αtSt−1 + vtk⊤ t

DeltaNet (Yang et al., 2024b) 1 βt 1 St = St−1(I −βtktk⊤ t) + βtvtk⊤ t

Gated DeltaNet (Yang et al., 2024a) αt βt 1 St = St−1 αt(I −βtktk⊤ t)

+ βtvtk⊤ t

LongHorn (Liu et al., 2024) 1 βt 1+βtk⊤ t kt 1 St = St−1

I − βt 1+βtk⊤ t kt ktk⊤ t

+ βt 1+βtk⊤ t kt vtk⊤ t

(ii) We provide a theoretical analysis showing that MuonSSM-style updates preserve parallelizability while improving gradient propagation; and (iii) We demonstrate empirically that MuonSSM variants consistently improve accuracy, robustness, and length generalization across a wide range of modalities and SSM backbones, including language, vision, and time-series tasks. Organization. We introduce the MuonSSM architecture in Section 2. Theoretical analysis regarding parallel associative structure and gradient propagation follows in Section 3, with detailed proofs deferred to the appendix. Section 4 presents experimental evaluations across language, vision, and timeseries benchmarks, with additional empirical analysis in Section 5. Finally, Section 6 reviews related work, and Section 7 concludes the paper.

## 2. Methodology: MuonSSM

## 2.1 Background: State Space Models as Associative Memory

Following recent works providing a unified view of SSMs as online associative memory mechanisms (Yang et al., 2024a; Behrouz et al., 2025b), we adopt the framework where at each timestep t, the model maintains a memory matrix St ∈ Rd×m and receives a key-value pair (kt, vt) ∈Rm × Rd. The memory state is updated as

St = St−1 αt(Im −βtηktk⊤ t)

+ βtvtk⊤ t, (1)

where αt ∈(0, 1] controls memory retention, βt > 0 determines the update magnitude, η modulates recall correction, and Im ∈Rm×m is the identity matrix. This formulation shows that recent SSM variants (Mamba, DeltaNet, Gated DeltaNet, LongHorn) primarily differ in their choices of scalar gates αt, βt, and η (see Table 1).

## 2.2 Limitations of First-Order Updates All updates derived from

Eq. (1) remain inherently firstorder. The change in memory is a rank-one modification:

∆St ∝(vt −αtηSt−1kt)k⊤ t, (2)

which is structurally confined to the span of the current key kt. Over long sequences, repeated rank-one updates can induce:

## 1 Spectral anisotropy:

Singular values become highly non-uniform.

## 2. Gradient degradation: Vanishing gradients through Qt

n=T Dn where Dn = αn(Im −βnηknk⊤ n).

## 3 Memory interference:

New updates can overwrite previous information.

Current SSMs address these issues only indirectly through scalar gating, normalization, or transition-matrix parameterization, such as HiPPO-inspired and diagonal SSM parameterizations (Gu et al., 2020; 2022b;a). In contrast, Muon- SSM explicitly conditions the geometry of input-dependent memory updates while also introducing an additional momentum pathway for gradient propagation.

## 2.3 MuonSSM: Orthogonalizing State Space Models

To mitigate these limitations while preserving parallel scan efficiency, we propose MuonSSM. The key idea is to augment the memory dynamics with two simple components: a momentum pathway that accumulates update directions across timesteps, and a lightweight Newton–Schulz (NS) normalization applied to each low-rank input injection. These components condition memory updates while retaining the affine structure required for efficient parallel scans. Theoretical justification is provided in Section 3.

## 2.3.1 MOMENTUM-AUGMENTED DYNAMICS MuonSSM maintains an auxiliary momentum matrix

Mt ∈ Rd×m, updated as

Mt = γMt−1 + NS τβtvtk⊤ t

, (3)

St = St−1 αt(Im −βtηktk⊤ t)

+ Mt, (4)

where γ ∈(0, 1] is the momentum decay coefficient and τ > 0 scales the normalized update. The operator NS(·) is defined below.

2.3.2. SINGLE-ITERATION NEWTON–SCHULZ Each input injection Xt = τβtvtk⊤ t is a rank-1 matrix whose sole nonzero singular value σt = τβt∥vt∥∥kt∥

<!-- Page 3 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Figure 1.** The MuonSSM architecture. At each timestep, the model forms a low-rank input injection τβtvtk⊤

t, applies a lightweight Newton–Schulz normalization, accumulates the normalized update through a momentum state Mt, and updates the memory state St through an input-dependent transition. The output is computed as yt = Stqt.

varies arbitrarily across timesteps, producing spectrally unbalanced updates if left unnormalized. We apply a singlestep Newton–Schulz iteration to each injection, which bounds singular values, preserves rank, and keeps per-step cost minimal without requiring an explicit SVD.

Definition 2.1 (Single-iteration Newton–Schulz (NS)). For X ∈Rd×m, define:

NS(X) = a + b ˜X ˜X⊤+ c

˜X ˜X⊤ 2

˜X (5)

where ˜X = X max(∥X∥F, δ) (6)

Here (a, b, c) = (3.4445, −4.7750, 2.0315) (Jordan et al., 2024), and δ > 0 is a small constant to prevent division by zero.

The spectral properties of this operator and its backwardpass Jacobian geometry, which differs structurally from Frobenius normalization and drives rank enrichment in Mt, are analyzed formally in Section 3.3.

## 3. Theoretical Analysis

We establish the key theoretical properties of MuonSSM: parallelizability, gradient stability, spectral conditioning, and rank enrichment. Together, these properties explain how MuonSSM mitigates the limitations of first-order SSMs while preserving computational efficiency.

## 3.1 Parallelizability

To enable parallel training, we cast the coupled memory and momentum updates (3)–(4) as a single block-affine recurrence, which admits efficient parallel associative scans.

Proposition 3.1 (Block-Affine Recurrence). Define the augmented state by horizontally concatenating the memory and momentum matrices:

Zt =

St Mt

∈Rd×2m.

The coupled dynamics satisfy the linear recurrence:

Zt = Zt−1Φt + Ψt, (7)

where the transition matrix Φt ∈R2m×2m and input Ψt ∈ Rd×2m are defined as:

Φt =

Dt 0 γIm γIm

, Ψt =

Ut Ut

(8)

with Dt = αt(Im −βtηktk⊤ t) and Ut = NS(τβtvtk⊤ t).

Remark 3.2 (Parallel Training Efficiency). The block-affine recurrence (7) enables parallel associative scans (Blelloch, 1990) with operator (Φi, Ψi) ⊕(Φj, Ψj) = (ΦiΦj, ΨiΦj +Ψj). This reduces the recurrent depth from

O(L) to O(log L) while keeping total work linear in L. The NS pre-computation in Step 1 of Algorithm 1 is local to each timestep and adds only a constant-factor overhead.

## Algorithm

1 summarizes the full parallel training procedure based on Proposition 3.1.

## 3.2 Gradient Stability

We next examine how the augmented dynamics affect gradient propagation through time. While standard SSMs suffer from repeated contraction induced by input-dependent transition matrices, the momentum pathway introduces an additional channel for gradient flow.

![Figure extracted from page 3](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Proposition 3.3 (Gradient Propagation in MuonSSM). Let the augmented state Zt =

St Mt evolve according to the affine recurrence

Zt = Zt−1Φt + Ψt, Φt =

Dt 0 γIm γIm

.

Then the gradient of the loss L with respect to Zt−1 propa- gates backwards via the transposed transition matrices:

∂L ∂Zt−1

= ∂L

∂ZT tY n=T

Φ⊤ n, which expands into the upper-triangular block form

∂L ∂Zt−1

= ∂L

∂ZT



 tY n=T

D⊤ n

T X k=t k+1 Y j=T

D⊤ j

!

(γIm)k−t+1

0 (γIm)T −t+1



 with the convention that any empty product equals Im.

Remark 3.4 (Gradient Preservation via Scalar Momentum). When γ ≈1, the momentum pathway (γIm)T −t+1 introduces a scalar eigenvalue close to unity into the Jacobian product Qt n=T Φ⊤ n. Although the memory pathway Qt n=T D⊤ n may contract due to input-dependent attenuation, a non-vanishing gradient component is preserved through the momentum state Mt, mitigating exponential decay and enabling stable long-range credit assignment.

We emphasize that this analysis assumes a linear recurrence; additional nonlinearities and deep stacking in practice introduce interactions beyond the closed-form Jacobian of Proposition 3.3. Empirical support is provided in Appendix C and Figure 7, where gradient norm heatmaps confirm substantially more uniform long-range propagation.

## 3.3 Spectral Conditioning and

Newton–Schulz Geometry Beyond gradient flow, stable training requires controlling the spectral magnitude of memory updates. We analyze the NS operator in two complementary ways: its effect on singular values in the forward pass, and its distinct Jacobian geometry in the backward pass.

Corollary 3.5 (Spectral Conditioning of Updates). Let ρ(σ) = aσ + bσ3 + cσ5. Since ∥˜X∥F ≤1, all singular values of ˜X lie in [0, 1], and the NS map sends each singular value σ to ρ(σ). Hence, for any input matrix X, σmax(NS(X)) ≤sup σ∈[0,1]

|ρ(σ)| = 1 + εu. (9)

For (a, b, c) = (3.4445, −4.7750, 2.0315), we have ρ(σ) ≥

0 on [0, 1] and supσ∈[0,1] ρ(σ) ≈1.2. Moreover, since ρ(σ) > 0 for all σ > 0, NS preserves the rank of any nonzero input, and thus preserves the rank-one structure of each nonzero injection.

Beyond the forward-pass bound of Corollary 3.5, the NS operator exerts a structurally distinct backward geometry that drives rank enrichment beyond what Frobenius normalization achieves. Proposition 3.6 (Backward Geometry of Newton–Schulz Normalization). Let X0 = uw⊤∈Rd×m be rank-one with ∥u∥2 = ∥w∥2 = 1. Denote by u⊥and w⊥ any vectors orthogonal to u and w respectively, so that {uw⊤, u⊥w⊤, uw⊤

⊥, u⊥w⊤

⊥} partitions Rd×m into four orthogonal subspaces of dimensions 1, d −1, m −1, and (d −1)(m −1), respectively.

The Jacobian DGX0 of NS(X) (Definition 2.1) has the fol- lowing eigenvalue families:

λ =

  

 

0 direction uw⊤ a + b + c directions u⊥w⊤, uw⊤

⊥ a directions u⊥w⊤

⊥

(10)

The total dimension of each family is 1, d + m −2, and (d −1)(m −1), respectively. For (a, b, c) = (3.4445, −4.7750, 2.0315), these evaluate to 0, a + b + c ≈

0.701, a ≈3.4445. In contrast, Frobenius normalization X 7→X/∥X∥F has eigenvalue 0 in the radial direction uw⊤and eigenvalue 1 in every other direction. Remark 3.7 (Implication for Rank Enrichment). Proposition 3.6 shows that NS and Frobenius normalization have different backward geometries. While both remove the radial direction uw⊤, Frobenius normalization leaves all tangent directions unchanged, whereas NS amplifies the fully orthogonal subspace u⊥w⊤

⊥by a factor a ≈3.4445 and scales the mixed directions by a + b + c ≈0.701. Thus, NS biases the backward signal toward directions orthogonal to the current rank-one write. When accumulated through the momentum recurrence, this provides a mechanism for producing less collinear updates and increasing the effective rank of Mt, consistent with the ablation results in Appendix C.

## 3.4 Rank Enrichment

Finally, we analyze how momentum accumulation affects the representational capacity of the memory state. While each individual update is rank-1, their exponentially weighted accumulation leads to a progressively richer memory structure. Proposition 3.8 (Rank Enrichment via Momentum Accumulation). Assume M0 = 0. The momentum state at time t admits the expansion

Mt = t X s=1 γt−s NS τβsvsk⊤ s

. (11)

Consequently, rank(Mt) ≤min(t, d, m). (12)

<!-- Page 5 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Moreover, this upper bound is attainable and generically tight: under non-degenerate updates (τ > 0, βs > 0, vs̸ = 0, ks̸ = 0), the set of direction pairs {(vs, ks)}t s=1 for which rank(Mt) < min(t, d, m) has measure zero with respect to the product surface measure on (Sd−1 × Sm−1)t.

While momentum accumulation allows the memory to reach a rank up to min(t, d, m), rank alone is insufficient to characterize representational capacity. We therefore consider the effective rank reff(Mt) =

P i σi(Mt)

2 P i σi(Mt)2, (13)

which measures how uniformly the singular values of Mt are distributed. A higher effective rank indicates that the momentum state uses more independent representational directions, reducing the risk that repeated rank-one writes collapse into a small subspace. Together with Proposition 3.6, this suggests that the backward geometry of NS can encourage less collinear future writes, while momentum accumulation integrates these writes over time. This mechanism is consistent with the three-way ablation in Appendix C, where replacing NS with Frobenius normalization reduces the effective rank and downstream accuracy. We defer all proofs to Appendix A.

## 4. Experiments

We present a comprehensive empirical evaluation of Muon- SSM across three distinct modalities: language, vision, and time series. Our primary objective is to assess whether the proposed memory-update mechanism translates into tangible performance gains and improved robustness across diverse data distributions. We benchmark MuonSSM against representative state-of-the-art SSM baselines, including Mamba, LongHorn, and Gated DeltaNet. To ensure a controlled comparison, we maintain identical parameter counts, architectural hyperparameters, and training budgets across all experiments, thereby isolating the effect of the Muon- SSM update mechanism. All experiments are conducted on four NVIDIA H100 GPUs.

## 4.1 Language Modeling and Long-Context Retrieval

Setup. We investigate the capability of MuonSSM to handle discrete sequential data requiring both common-sense reasoning and precise long-range information retrieval. We adopt a 170M parameter configuration to conduct a controlled study on algorithmic efficiency in the small-scale regime. All models are pre-trained from scratch on the FineWeb-Edu 10B dataset (Lozhkov et al., 2024), a highquality educational corpus chosen to evaluate the model’s ability to acquire reasoning capabilities and linguistic structure efficiently under a controlled compute budget. Following pre-training, we perform supervised fine-tuning on the Alpaca-52K dataset (Taori et al., 2023) to unlock instruction- following capabilities. Crucially, the SFT stage is conducted with a maximum sequence length of 2048 tokens. This constraint allows us to explicitly test the model’s ability to extrapolate to longer contexts during evaluation, assessing whether the spectral properties of MuonSSM facilitate length generalization beyond the training horizon.

Results. As summarized in Tables 2 and 3, MuonSSM demonstrates superior performance compared to standard SSMs. On common-sense reasoning benchmarks derived from the FineWeb-Edu pre-training, the model achieves lower perplexity, suggesting that spectrally balanced updates facilitate better knowledge compression. More importantly, in the Single Needle in Haystack (S-NIAH) evaluation, MuonSSM maintains high retrieval accuracy across PassKey (PK), Number (N), and UUID tasks up to context lengths of 8K tokens. This result is particularly significant given that the instruction tuning was limited to 2048 tokens. Unlike baseline models which typically exhibit rapid performance degradation when extrapolating beyond their training context window, MuonSSM mitigates long-range gradient attenuation by introducing a momentum pathway and conditioning the geometry of input-dependent memory updates, thereby improving length generalization.

## 4.2 Vision Spatial Modeling and Robustness

Setup. Following the MambaVision framework (Hatamizadeh & Kautz, 2025), we evaluate MuonSSM as a drop-in replacement for visual state-space modeling. The architecture employs a hierarchical design where images are processed by a convolutional stem followed by stacked SSM mixers. We replace the standard Mamba mixers with MuonSSM blocks while keeping the hybrid attention layers and patch embedding strategies invariant. We utilize Tiny model variants to strictly control the computational budget. We assess performance on three standard tiers of visual understanding: image classification on ImageNet-1K (IN-1K) (Deng et al., 2009), object detection on MS COCO (Lin et al., 2015), and semantic segmentation on ADE20K (Zhou et al., 2017). Furthermore, to strictly evaluate the resilience of learned representations against distribution shifts and corruptions, we extend our evaluation to three challenging robustness benchmarks: ImageNet Corruption (IN-C) (Hendrycks & Dietterich, 2019), ImageNet Rendition (IN-R) (Hendrycks et al., 2021a), and ImageNet Adversarial (IN-A) (Hendrycks et al., 2021b). All experiments follow the same training schedules and evaluation protocols as in prior MambaVision work.

Results. Tables 4 and 5 summarize the results, where MuonSSM yields consistent improvements over the MambaVision baseline across standard classification and dense prediction tasks. Crucially, in the robustness evaluation, MuonSSM demonstrates a significant reduction in Mean Corruption Error on IN-C and higher accuracy on IN-A and

<!-- Page 6 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Table 2.** Zero-shot performance on common sense reasoning and language modeling tasks. All models are pretrained on FineWeb-Edu10B

tokens. We compare original SSM backbones with our Muon-integrated versions. ↓: Lower is better, ↑: Higher is better. Bold indicates the best result per architecture.

Architecture Memory Wiki. LMB. LMB. PIQA Hella. Wino. ARC-e ARC-c SIQA BoolQ Avg. Algorithm ppl ↓ ppl ↓ acc ↑ acc ↑ acc n ↑ acc ↑ acc ↑ acc n ↑ acc ↑ acc ↑ acc ↑

Mamba Original 42.17 102.51 20.57 63.81 30.10 51.11 52.39 21.75 37.41 59.87 42.13 + Muon (Ours) 40.83 89.17 22.84 63.47 33.19 53.36 53.21 25.58 38.33 63.82 44.23

LongHorn Original 43.06 96.80 22.16 62.79 29.87 52.25 50.34 21.24 36.18 55.02 41.23 + Muon (Ours) 41.71 80.98 24.00 62.02 32.85 54.38 51.17 25.12 37.15 59.44 43.27

Gated DeltaNet Original 39.58 97.92 21.36 62.45 30.02 51.30 51.85 21.42 36.90 55.23 41.32 + Muon (Ours) 38.12 83.47 23.91 62.88 33.51 53.76 52.74 23.13 38.02 56.85 43.10

**Table 3.** Needle-in-a-Haystack retrieval performance under vary-

ing context lengths. We evaluate three variants: PassKey (PK), Number (N), and UUID. Higher values indicate better accuracy.

Architecture Memory S-NIAH-PK S-NIAH-N S-NIAH-UUID

## Algorithm

2K 4K 8K 2K 4K 8K 2K 4K 8K

Mamba Original 29.3 16.4 8.8 18.6 14.3 4.1 48.6 32.9 25.0 + Muon 32.1 20.5 15.8 22.4 19.1 10.2 53.8 38.2 31.5

LongHorn Original 67.9 52.1 20.0 70.7 55.7 35.6 46.4 30.7 19.3 + Muon 66.7 55.9 39.3 75.1 71.4 36.8 52.9 37.9 28.6

GatedDeltaNet Original 61.4 43.6 25.7 69.3 43.6 27.1 52.1 35.0 24.3 + Muon 63.2 48.9 44.5 74.1 57.8 29.4 58.3 42.6 33.1

IN-R. This enhanced resilience indicates that the spectral whitening effect of MuonSSM prevents the model from overfitting to superficial high-frequency statistics or texture biases common in standard training. Instead, the optimization dynamics encourage the learning of invariant features robust to distribution shifts, proving beneficial for out-ofdistribution generalization.

**Table 4.** Comparison of SSMs with and without the proposed Muon

framework. Bold indicates the best performance per architecture.

Architecture Memory IN-1K IN-R IN-A IN-C

## Algorithm

Top-1 ↑Top-5 ↑Top-1 ↑Top-1 ↑Top-1 ↑mCE ↓

Mamba Original 81.08 95.32 42.35 20.57 12.31 112.84 + Muon 81.19 95.36 42.61 20.50 12.57 112.52

LongHorn Original 81.63 95.82 45.44 23.76 13.12 111.68 + Muon 82.01 95.90 46.28 25.27 13.53 111.24

GatedDeltaNet Original 79.92 95.24 41.55 19.92 11.85 114.12 + Muon 80.31 95.35 42.18 20.47 12.33 113.56

**Table 5.** Downstream task performance on COCO2017 (Object

Detection & Instance Segmentation) and ADE20K (Semantic Segmentation). We compare the original backbones against our Muonintegrated versions across different model scales.

Architecture Memory Object Detection Instance Seg. Sem. Seg.

## Algorithm

APbox APbox

## 50 APbox 75 APmask APmask 50 APmask

75 mIoU

Mamba Original 50.8 69.5 55.2 44.1 67.0 47.9 43.9 + Muon 51.1 69.9 55.4 44.3 67.4 48.2 45.2

LongHorn Original 50.6 69.3 55.3 44.0 66.7 47.6 44.2 + Muon 51.0 69.8 55.4 44.1 67.1 47.6 45.7

GatedDeltaNet Original 49.5 68.1 53.8 43.4 67.2 46.8 41.2 + Muon 50.1 68.8 54.5 43.8 67.8 47.3 41.8

## 4.3. Time-Series for Human Activity Recognition

**Table 6.** Comparison of different architectures with Memory Algo-

rithm column added

Architecture Memory Algorithm

Accuracy

(%)

Precision

(%)

Recall

(%)

F1-score

(%)

MuWiGes

Mamba Original 96.25 96.31 96.24 96.25 + Muon 97.64 97.47 97.44 97.45

LongHorn Original 97.23 97.44 97.27 97.35 + Muon 97.95 97.98 97.95 97.96

GatedDeltaNet Original 96.88 96.90 96.87 96.87 + Muon 97.73 97.75 97.72 97.73

UESTC-MMEA-CL

Mamba Original 87.74 88.38 89.46 88.91 + Muon 91.62 91.41 90.95 90.96

LongHorn Original 89.06 89.88 89.44 89.43 + Muon 91.56 90.94 91.12 91.02

GatedDeltaNet Original 86.09 87.20 86.16 85.92 + Muon 87.97 88.35 87.82 87.81

MMAct

Mamba Original 71.46 71.82 71.56 71.68 + Muon 74.65 78.16 74.06 74.25

LongHorn Original 72.47 75.68 74.12 73.76 + Muon 74.40 79.25 76.47 76.43

GatedDeltaNet Original 66.39 73.23 68.28 67.75 + Muon 66.61 74.11 69.09 68.73

Setup. We adopt a simple architecture consisting of a Conv1D front-end for local feature extraction, followed by stacked state space blocks and a classification head. Within this architecture, standard SSM blocks are replaced with MuonSSM blocks, while all other components remain unchanged. This design ensures that any observed differences can be attributed to the memory update dynamics introduced by MuonSSM. We evaluate on three widely used benchmarks: MuWiGes (Nguyen et al., 2023) with 12 finegrained hand gestures, UESTC-MMEA-CL (Xu et al., 2024) with 32 daily activities, and MMAct (Kong et al., 2019) with 37 complex actions with high sensor noise, covering diverse levels of activity granularity and temporal complexity.

Results. As shown in Table 6, MuonSSM outperforms baselines on all three datasets, with the margin of im-

<!-- Page 7 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling provement widening as dataset complexity increases from MuWiGes to MMAct, which involve greater inter-class similarity and motion variability. Notably, these improvements arise despite the fact that the input sequences are not extremely long, suggesting that MuonSSM benefits temporal modeling by stabilizing update dynamics and reducing sensitivity to high-frequency noise, rather than solely by extending effective context length.

## 5. Empirical Analysis

## 5.1 Spectral Conditioning and Stability

Our core hypothesis is that standard first-order SSM updates suffer from spectral degradation over time, leading to ill-conditioned optimization landscapes. To verify this, we visualize the distribution of singular values of the state transition matrix (dstate = 64) for a Mamba backbone trained on the Human Activity Recognition task.

**Figure 2.** Singular value spectrum of the recurrent state matrix. Standard SSM updates (red) exhibit spectral collapse and a high condition number, while MuonSSM (green) maintains a near-isometric, well-conditioned spectrum via Newton–Schulz normalization.

As shown in Figure 2, the baseline Mamba model (red) exhibits a severe spectral collapse, where a few dominant singular values absorb most of the energy, while the majority decay towards zero. This results in an extremely high condition number (κ ≈2.2 × 106), indicating a brittle optimization landscape prone to vanishing gradients. In contrast, applying MuonSSM with Newton–Schulz iteration (green) effectively flattens the spectrum, pushing smaller singular values towards unity. This reduces the condition number by approximately 18× (from κ ≈2.2 × 106 to κ ≈1.2 × 105). This empirical evidence confirms that our lightweight orthogonalization acts as an effective preconditioner, maintaining a healthy effective rank throughout training without the cost of exact SVD.

## 5.2 Optimization Dynamics and Computational Scalability Convergence

Speed. Figure 3a compares the pre-training loss on FineWeb-Edu 10B for the baseline LongHorn and our MuonSSM. The results are striking, LongHorn with Muon not only achieves a lower final perplexity but also demonstrates a significantly steeper initial learning trajec-

(a) Pre-training dynamics on FineWeb-Edu 10B tokens

(b) Training time per epoch vs. sequence length.

**Figure 3.** (a) MuonSSM accelerates convergence 1.3× faster,

achieves lower validation loss and perplexity compared to the baseline. (b) The parallel trend lines indicate that MuonSSM preserves the asymptotic linear complexity of the baseline, adding only a constant-factor overhead due to the projection step.

tory. This suggests that the geometry-aware updates allow the optimizer to escape saddle points more efficiently and navigate the loss landscape with greater stability, effectively accelerating convergence by approximately 1.3× in terms of training steps. Computational Scalability. Integrating Newton–Schulz iterations introduces additional matrix multiplications, which may affect throughput. To assess this cost, we measure the training time per epoch across varying sequence lengths on the MMAct dataset. As illustrated in Figure 3b, LongHorn with Muon incurs a modest constant-factor overhead compared to the baseline LongHorn, while exhibiting a similar scaling trend as sequence length increases. This indicates that MuonSSM preserves the scan-compatible structure of the underlying SSM backbone: the recurrence can still be evaluated with O(log L) parallel depth and O(L) total work over the sequence. Although the per-step computation is slightly higher, the faster convergence rate means that MuonSSM can reach target performance targets in fewer total steps, making it a highly efficient strategy overall.

5.3. Capacity vs. Geometric Conditioning The augmented state Zt = [St Mt] ∈Rd×2m (Proposition 3.1) effectively doubles the memory dimension, raising the question of whether the observed gains can be attributed

![Figure extracted from page 7](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling solely to increased capacity. To isolate this effect, we construct 2×dstate baselines for both LongHorn and Mamba by doubling the state dimension while keeping all other components unchanged. All models are trained on MMAct over 5 independent runs. Table 7 reports accuracy, precision, recall, and F1 scores for these variants. Doubling dstate yields only modest improvements over the base models (+0.41% for LongHorn, +1.05% for Mamba). In contrast, Muon variants outperform their respective 2× baselines by a substantial margin (+1.52% and +2.13%), indicating that increased capacity alone is insufficient to explain the gains. These results support our hypothesis that the primary benefit of MuonSSM arises from improved optimization geometry, rather than from a simple expansion of the state dimension.

## 5.4 Ablation Studies: Impact of

Newton–Schulz Iterations. A critical design choice in MuonSSM is the number of Newton–Schulz iterations. In Figure 4, we compare Mamba baselines against MuonSSM variants with different settings on the MMAct dataset: Momentum Only (No NS), Newton– Schulz one iteration, and Newton–Schulz five iterations. This suggests that enforcing strict via more iterations may be overly rigid, potentially hindering the model’s ability to capture necessary non-orthogonal correlations in the data. Based on these results, we adopt Newton–Schulz with one iteration as the default setting, balancing performance with computational efficiency.

**Figure 4.** Ablation of Iterations on MMAct dataset

## 5.5 Robustness and Inductive Bias Finally, we investigate what features

MuonSSM learns compared to standard models. We employ GradCAM (Gildenblat & contributors, 2021) to visualize the focus regions of MambaVision-Tiny models on the IN-R dataset, which contains out-of-distribution examples like art, sketches, and cartoons. Figure 5 reveals a striking difference in inductive bias. Texture vs. Shape Bias. The baseline MambaVision (left) often misclassifies objects based on texture cues. For in- stance, it misidentifies a sketch of a Hammerhead Shark as a Great White Shark, likely due to texture ambiguity, and mistakes a stylized Goldfish for an Old English Sheepdog. Invariant Representation. MuonSSM (right) correctly classifies both instances. The activation maps show that MuonSSM focuses more precisely on the structural shape of the distinct head of the hammerhead shark rather than background noise or texture. This suggests that the spectral orthogonalization in MuonSSM encourages the learning of more disentangled and shape-invariant features, leading to the superior robustness observed in our main experiments.

**Figure 5.** GradCAM visualizations show that standard MambaV-

ision (left) is prone to texture bias and confusion under domain shift. MuonSSM (right) demonstrates stronger shape bias, correctly identifying the Goldfish and Hammerhead Shark by focusing on relevant structural features despite the artistic rendition.

## 6. Related Work

MuonSSM relates to prior work on state space sequence models, associative memory mechanisms, momentumbased recurrent dynamics, and orthogonalized updates. Unlike approaches that modify the recurrent transition operator, MuonSSM conditions the geometry of input-dependent memory updates while preserving scan-based parallel computation. State Space Models. SSMs have emerged as scalable alternatives to attention for long-sequence modeling, beginning with structured models such as S4 (Gu et al., 2021) and extending to H3 (Fu et al., 2022), S5 (Smith et al., 2022), and Mamba (Gu & Dao, 2024; Dao & Gu, 2024). Their foundations are closely related to HiPPO-based memory compression (Gu et al., 2020; 2022b) and subsequent diagonal or parameterized SSM variants (Gu et al., 2022a). Related linear-time architectures combine recurrence with limited attention or alternative sequence mixing mechanisms, including Mega (Ma et al., 2022), Griffin (De et al., 2024), Jamba (Lenz et al., 2025), RWKV (Peng et al., 2023), Ret- Net (Sun et al., 2023), and Hyena (Poli et al., 2023). Across these models, efficiency is typically achieved by structuring

![Figure extracted from page 8](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Table 7.** Comparison with doubled state-dimension baselines on MMAct (5 independent runs, mean ± std). Best results are in bold.

Architecture Accuracy (%) Precision (%) Recall (%) F1 (%)

LongHorn 72.47 ± 0.19 75.68 ± 0.30 74.12 ± 0.17 73.76 ± 0.24 LongHorn 2×dstate 72.88 ± 0.27 78.62 ± 0.34 74.67 ± 0.25 74.90 ± 0.23 MuonLongHorn (Ours) 74.40 ± 0.21 79.25 ± 0.26 76.47 ± 0.27 76.43 ± 0.36

Mamba 71.47 ± 0.25 71.82 ± 0.38 71.56 ± 0.28 71.68 ± 0.33 Mamba 2×dstate 72.52 ± 0.22 76.98 ± 0.34 73.80 ± 0.25 73.40 ± 0.18 MuonMamba (Ours) 74.65 ± 0.34 78.16 ± 0.29 74.06 ± 0.41 74.25 ± 0.35 the recurrence for parallel scan primitives (Blelloch, 1990). Recent work further connects SSMs, linear attention, and recurrent computation through low-rank associative memory updates (Katharopoulos et al., 2020; Orvieto et al., 2023; Behrouz et al., 2025b). Several models interpret state updates as associative memory rules or online learning dynamics (Yang et al., 2024b;a; Liu et al., 2024; Behrouz et al., 2025a; Ba et al., 2016; Ramsauer et al., 2020; Schlag et al., 2021), but largely retain first-order update mechanisms. Beyond this regime, LinOSS (Rusch & Rus, 2024) derives stable second-order dynamics from forced harmonic oscillators, yielding a linear time-invariant formulation. In contrast, MuonSSM targets selective, input-dependent SSMs, where transitions vary across timesteps and stability is addressed through per-step spectral conditioning of low-rank memory injections. Momentum in Sequence Models. Momentum is a classical mechanism for stabilizing optimization and accelerating convergence (Polyak, 1964). It has also been explored in recurrent architectures as a way to extend effective memory and improve stability (Nguyen et al., 2020; Ma et al., 2022; Teo & Nguyen, 2024). Related perspectives connect recurrent computation with online optimization and test-time memory updates (Zinkevich, 2003; Behrouz et al., 2025b; 2024). MuonSSM builds on these ideas by incorporating momentum directly into scan-compatible SSM updates, yielding an additional pathway for information and gradient propagation without breaking the affine recurrence structure. Orthogonalization and Spectral Conditioning. Another line of work stabilizes recurrent or deep networks through spectral constraints, unitary or orthogonal parameterizations, and normalization-based control of singular values (Pascanu et al., 2013; Arjovsky et al., 2016; Henaff et al., 2016; Vorontsov et al., 2017; Wisdom et al., 2016; Helfrich et al., 2018; Miyato et al., 2018). Exact orthogonalization is often costly, motivating lightweight alternatives based on Newton– Schulz iterations and related approximate normalization schemes (Song et al., 2022; Bernstein & Newhouse, 2024; Jordan et al., 2024).Recent optimizers such as Muon (Jordan et al., 2024) and Dion (Ahn et al., 2025) demonstrate the practical value of orthonormalized update directions for large-scale training. MuonSSM differs from these optimizerlevel methods: it applies lightweight Newton–Schulz-style conditioning directly to input-dependent low-rank memory injections inside scan-based SSMs, rather than orthogonalizing parameter gradients or imposing global constraints on the recurrent transition operator.

## 7. Concluding Remarks

In this work, we presented MuonSSM, a family of SSMs that stabilizes sequence modeling by conditioning memory updates rather than constraining recurrent transitions. Muon- SSM combines a momentum pathway with a lightweight single-step Newton–Schulz transformation on low-rank input injections, yielding bounded and better-conditioned updates while preserving parallel scan complexity. Our analysis shows that this design provides an additional gradient pathway, controls spectral amplification, and encourages richer memory representations. Experiments across language, vision, and time-series tasks demonstrate consistent gains across multiple SSM backbones. While our study focuses on moderate-scale models and fixed conditioning hyperparameters, the results suggest that geometric conditioning of update dynamics is a simple and effective mechanism for stable sequence modeling. Future work will explore larger-scale pretraining, hybrid attention–SSM architectures, and adaptive conditioning strategies.

<!-- Page 10 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here.

## Acknowledgements

This research is supported by the National Research Foundation Singapore under the AI Singapore Programme (AISG Award No: AISG2-TC-2023-012-SGIL). This research is also supported by the Ministry of Education, Singapore, under the Academic Research Fund Tier 1 (FY2023) (A- 8002040-00-00, A-8002039-00-00), the NUS Presidential Young Professorship Award (A-0009807-01-00), the NUS Artificial Intelligence Institute–Seed Funding (A-8003062- 00-00), and the Cross Faculty Grant 2025, CFG25-012 (A- 8004460-00-00).

## References

Ahn, K., Xu, B., Abreu, N., Fan, Y., Magakyan, G., Sharma,

P., Zhan, Z., and Langford, J. Dion: Distributed orthonormalized updates. arXiv preprint arXiv:2504.05295, 2025.

Arjovsky, M., Shah, A., and Bengio, Y. Unitary evolution recurrent neural networks. In International conference on machine learning, pp. 1120–1128. PMLR, 2016.

Ba, J., Hinton, G. E., Mnih, V., Leibo, J. Z., and Ionescu, C.

Using fast weights to attend to the recent past. Advances in neural information processing systems, 29, 2016.

Behrouz, A., Zhong, P., and Mirrokni, V. Titans: Learning to memorize at test time. arXiv preprint arXiv:2501.00663, 2024.

Behrouz, A., Razaviyayn, M., Zhong, P., and Mirrokni, V.

Nested learning: The illusion of deep learning architectures. arXiv preprint arXiv:2512.24695, 2025a.

Behrouz, A., Razaviyayn, M., Zhong, P., and Mirrokni, V. S.

It’s all connected: A journey through test-time memorization, attentional bias, retention, and online optimization. ArXiv, abs/2504.13173, 2025b.

Bernstein, J. and Newhouse, L. Old optimizer, new norm:

An anthology. arXiv preprint arXiv:2409.20325, 2024.

Blelloch, G. E. Prefix sums and their applications. 1990.

Dao, T. and Gu, A. Transformers are ssms: Generalized models and efficient algorithms through structured state space duality. arXiv preprint arXiv:2405.21060, 2024.

De, S., Smith, S. L., Fernando, A., Botev, A., Cristian-

Muraru, G., Gu, A., Haroun, R., Berrada, L., Chen, Y.,

Srinivasan, S., et al. Griffin: Mixing gated linear recurrences with local attention for efficient language models. arXiv preprint arXiv:2402.19427, 2024.

Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and

Fei-Fei, L. Imagenet: A large-scale hierarchical image database. In 2009 IEEE Conference on Computer Vision and Pattern Recognition, pp. 248–255, 2009. doi: 10.1109/CVPR.2009.5206848.

Fu, D. Y., Dao, T., Saab, K. K., Thomas, A. W., Rudra,

A., and R´e, C. Hungry hungry hippos: Towards language modeling with state space models. arXiv preprint arXiv:2212.14052, 2022.

Gildenblat, J. and contributors. Pytorch library for cam methods. https://github.com/jacobgil/ pytorch-grad-cam, 2021.

Gu, A. and Dao, T. Mamba: Linear-time sequence mod- eling with selective state spaces. In First conference on language modeling, 2024.

Gu, A., Dao, T., Ermon, S., Rudra, A., and R´e, C. Hippo:

Recurrent memory with optimal polynomial projections. Advances in neural information processing systems, 33: 1474–1487, 2020.

Gu, A., Goel, K., and R´e, C. Efficiently modeling long sequences with structured state spaces. arXiv preprint arXiv:2111.00396, 2021.

Gu, A., Goel, K., Gupta, A., and R´e, C. On the parameteri- zation and initialization of diagonal state space models. Advances in neural information processing systems, 35:

35971–35983, 2022a.

Gu, A., Johnson, I., Timalsina, A., Rudra, A., and R´e, C.

How to train your hippo: State space models with generalized orthogonal basis projections. arXiv preprint arXiv:2206.12037, 2022b.

Hatamizadeh, A. and Kautz, J. MambaVision: A Hybrid Mamba-Transformer Vision Backbone. In 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 25261–25270, Los Alamitos, CA, USA, 2025. IEEE Computer Society. doi: 10.1109/CVPR52734.2025.02352.

Helfrich, K., Willmott, D., and Ye, Q. Orthogonal recurrent neural networks with scaled cayley transform. In International Conference on Machine Learning, pp. 1969–1978. PMLR, 2018.

Henaff, M., Szlam, A., and LeCun, Y. Recurrent orthogonal networks and long-memory tasks. In International Conference on Machine Learning, pp. 2034–2042. PMLR, 2016.

<!-- Page 11 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Hendrycks, D. and Dietterich, T. Benchmarking neural network robustness to common corruptions and perturbations. Proceedings of the International Conference on Learning Representations, 2019.

Hendrycks, D., Basart, S., Mu, N., Kadavath, S., Wang, F.,

Dorundo, E., Desai, R., Zhu, T., Parajuli, S., Guo, M., Song, D., Steinhardt, J., and Gilmer, J. The many faces of robustness: A critical analysis of out-of-distribution generalization. ICCV, 2021a.

Hendrycks, D., Zhao, K., Basart, S., Steinhardt, J., and

Song, D. Natural adversarial examples. CVPR, 2021b.

Jordan, K., Jin, Y., Boza, V., You, J., Cesista, F., New- house, L., and Bernstein, J. Muon: An optimizer for hidden layers in neural networks, 2024. URL https: //kellerjordan.github.io/posts/muon/.

Katharopoulos, A., Vyas, A., Pappas, N., and Fleuret, F.

Transformers are rnns: Fast autoregressive transformers with linear attention. In International conference on machine learning, pp. 5156–5165. PMLR, 2020.

Kong, Q., Wu, Z., Deng, Z., Klinkigt, M., Tong, B., and

Murakami, T. Mmact: A large-scale dataset for cross modal human action understanding. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 8658–8667, 2019.

Lenz, B., Lieber, O., Arazi, A., Bergman, A., Manevich, A.,

Peleg, B., Aviram, B., Almagor, C., Fridman, C., Padnos, D., et al. Jamba: Hybrid transformer-mamba language models. In The Thirteenth International Conference on Learning Representations, 2025.

Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick,

R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L., and Doll´ar, P. Microsoft coco: Common objects in context, 2015.

Liu, B., Wang, R., Wu, L., Feng, Y., Stone, P., and Liu,

Q. Longhorn: State space models are amortized online learners. ArXiv, abs/2407.14207, 2024.

Lozhkov, A., Ben Allal, L., von Werra, L., and Wolf,

T. Fineweb-edu: the finest collection of educational content, 2024. URL https://huggingface.co/ datasets/HuggingFaceFW/fineweb-edu.

Ma, X., Zhou, C., Kong, X., He, J., Gui, L., Neubig, G., May,

J., and Zettlemoyer, L. Mega: Moving average equipped gated attention. arXiv preprint arXiv:2209.10655, 2022.

Miyato, T., Kataoka, T., Koyama, M., and Yoshida, Y. Spec- tral normalization for generative adversarial networks. arXiv preprint arXiv:1802.05957, 2018.

Nguyen, H.-Q., Le, T.-H., Tran, T.-K., Tran, H.-N., Tran,

T.-H., Le, T.-L., Vu, H., Pham, C., Nguyen, T. P., and Nguyen, H. T. Hand gesture recognition from wrist-worn camera for human–machine interaction. IEEE Access, 11: 53262–53274, 2023.

Nguyen, T., Baraniuk, R., Bertozzi, A., Osher, S., and Wang,

B. Momentumrnn: Integrating momentum into recurrent neural networks. Advances in neural information processing systems, 33:1924–1936, 2020.

Orvieto, A., Smith, S. L., Gu, A., Fernando, A., Gulcehre,

C., Pascanu, R., and De, S. Resurrecting recurrent neural networks for long sequences. In International Conference on Machine Learning, pp. 26670–26698. PMLR, 2023.

Pascanu, R., Mikolov, T., and Bengio, Y. On the difficulty of training recurrent neural networks. In International conference on machine learning, pp. 1310–1318. Pmlr, 2013.

Peng, B., Alcaide, E., Anthony, Q., Albalak, A., Arcadinho,

S., Biderman, S., Cao, H., Cheng, X., Chung, M., Grella, M., et al. Rwkv: Reinventing rnns for the transformer era. arXiv preprint arXiv:2305.13048, 2023.

Poli, M., Massaroli, S., Nguyen, E., Fu, D. Y., Dao, T.,

Baccus, S., Bengio, Y., Ermon, S., and R´e, C. Hyena hierarchy: Towards larger convolutional language models. In International Conference on Machine Learning, pp. 28043–28078. PMLR, 2023.

Polyak, B. T. Some methods of speeding up the convergence of iteration methods. Ussr computational mathematics and mathematical physics, 4(5):1–17, 1964.

Ramsauer, H., Sch¨afl, B., Lehner, J., Seidl, P., Widrich,

M., Adler, T., Gruber, L., Holzleitner, M., Pavlovi´c, M., Sandve, G. K., et al. Hopfield networks is all you need. arXiv preprint arXiv:2008.02217, 2020.

Rusch, T. K. and Rus, D. Oscillatory state-space models.

arXiv preprint arXiv:2410.03943, 2024.

Schlag, I., Irie, K., and Schmidhuber, J. Linear transformers are secretly fast weight programmers. In International conference on machine learning, pp. 9355–9366. PMLR, 2021.

Smith, J. T., Warrington, A., and Linderman, S. W. Sim- plified state space layers for sequence modeling. arXiv preprint arXiv:2208.04933, 2022.

Song, Y., Sebe, N., and Wang, W. Fast differentiable matrix square root. arXiv preprint arXiv:2201.08663, 2022.

Sun, Y., Dong, L., Huang, S., Ma, S., Xia, Y., Xue, J.,

Wang, J., and Wei, F. Retentive network: A successor to

<!-- Page 12 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling transformer for large language models. arXiv preprint arXiv:2307.08621, 2023.

Taori, R., Gulrajani, I., Zhang, T., Dubois, Y., Li,

X., Guestrin, C., Liang, P., and Hashimoto, T. B. Stanford alpaca: An instruction-following llama model. https://github.com/tatsu-lab/ stanford_alpaca, 2023.

Tay, Y., Dehghani, M., Abnar, S., Shen, Y., Bahri, D., Pham,

P., Rao, J., Yang, L., Ruder, S., and Metzler, D. Long range arena: A benchmark for efficient transformers. arXiv preprint arXiv:2011.04006, 2020.

Teo, R. S. and Nguyen, T. M. Momentumsmoe: Integrating momentum into sparse mixture of experts. Advances in Neural Information Processing Systems, 37:28965– 29000, 2024.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones,

L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. Advances in neural information processing systems, 30, 2017.

Vorontsov, E., Trabelsi, C., Kadoury, S., and Pal, C. On orthogonality and learning recurrent networks with long term dependencies. In International Conference on Machine Learning, pp. 3570–3578. PMLR, 2017.

Wisdom, S., Powers, T., Hershey, J., Le Roux, J., and At- las, L. Full-capacity unitary recurrent neural networks. Advances in neural information processing systems, 29,

2016.

Xu, L., Wu, Q., Pan, L., Meng, F., Li, H., He, C., Wang,

H., Cheng, S., and Dai, Y. Towards continual egocentric activity recognition: A multi-modal egocentric activity dataset for continual learning. IEEE Transactions on Multimedia, 26:2430–2443, 2024. ISSN 1941-0077. doi: 10.1109/tmm.2023.3295899.

Yang, S., Kautz, J., and Hatamizadeh, A. Gated delta networks: Improving mamba2 with delta rule. ArXiv, abs/2412.06464, 2024a.

Yang, S., Wang, B., Zhang, Y., Shen, Y., and Kim, Y. Par- allelizing linear transformers with the delta rule over sequence length. ArXiv, abs/2406.06484, 2024b.

Zhou, B., Zhao, H., Puig, X., Fidler, S., Barriuso, A., and

Torralba, A. Scene parsing through ade20k dataset. In 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 5122–5130, 2017. doi: 10.1109/ CVPR.2017.544.

Zinkevich, M. Online convex programming and generalized infinitesimal gradient ascent. In Proceedings of the 20th international conference on machine learning (icml-03), pp. 928–936, 2003.

<!-- Page 13 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Supplement to “MuonSSM: Orthogonalizing State Space Models for Sequence

Modeling”

## Appendix

A: Proofs of Theoretical Results

In this appendix, we provide detailed proofs for all theoretical results stated in Section 3, along with additional lemmas and technical details.

A.1. Proof of Proposition 3.1 and Remark 3.2: Parallelizability Proof. To establish the parallelizability of MuonSSM, we provide a two-part proof. First, we verify that the proposed block-affine recurrence exactly recovers the coupled memory and momentum dynamics. Second, we prove the associativity of the transition operator, which is the sufficient condition for applying parallel associative scans.

## 1 Recovery of Coupled

Dynamics. Given the augmented state Zt =

St Mt

, the block-affine recurrence Zt = Zt−1Φt + Ψt can be expanded using the definitions of Φt and Ψt:

St Mt

=

St−1 Mt−1

Dt 0 γI γI

+

Ut Ut

. (14)

Performing the block matrix multiplication yields the following two coupled equations:

St = St−1Dt + γMt−1 + Ut, (15)

Mt = γMt−1 + Ut. (16)

Substituting Eq. (16) into Eq. (15), we obtain:

St = St−1Dt + Mt. (17)

This confirms that the block-affine formulation exactly matches the intended MuonSSM momentum-augmented memory update.

## 2 Associativity and Parallel

Complexity. For a sequence of affine transformations ft(Z) = ZΦt + Ψt, the composition of two successive steps fj(fi(Z)) is:

fj(fi(Z)) = (ZΦi + Ψi)Φj + Ψj

= Z(ΦiΦj) + (ΨiΦj + Ψj).

This composition defines the operator ⊕:

(Φi, Ψi) ⊕(Φj, Ψj) = (ΦiΦj, ΨiΦj + Ψj).

To show that ⊕is associative, we consider three elements a, b, c where a = (Φ1, Ψ1), b = (Φ2, Ψ2), and c = (Φ3, Ψ3). Evaluating (a ⊕b) ⊕c:

(a ⊕b) ⊕c = (Φ1Φ2, Ψ1Φ2 + Ψ2) ⊕(Φ3, Ψ3)

= ((Φ1Φ2)Φ3, (Ψ1Φ2 + Ψ2)Φ3 + Ψ3)

= (Φ1Φ2Φ3, Ψ1Φ2Φ3 + Ψ2Φ3 + Ψ3).

Evaluating a ⊕(b ⊕c):

a ⊕(b ⊕c) = (Φ1, Ψ1) ⊕(Φ2Φ3, Ψ2Φ3 + Ψ3)

= (Φ1(Φ2Φ3), Ψ1(Φ2Φ3) + (Ψ2Φ3 + Ψ3))

= (Φ1Φ2Φ3, Ψ1Φ2Φ3 + Ψ2Φ3 + Ψ3).

Since (a⊕b)⊕c = a⊕(b⊕c), the operator is associative. By the property of associative scans, any sequence of L elements can be reduced in O(log L) time using a binary tree structure. Given that the Newton–Schulz step for Ut is local to each timestep, the entire sequence Z1:L is computable in O(log L) parallel depth.

<!-- Page 14 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

A.2. Proof of Proposition 3.3: Gradient Stability Proof. The result is derived by applying the chain rule to the backpropagation through time dynamics. Given the state evolution in row-vector convention Zt = Zt−1Φt + Ψt, we evaluate the gradient of the total loss L with respect to the state at time t −1. Following the standard convention, the gradient relates to the final state at time T via the product of transposed transition matrices:

∂L ∂Zt−1

= ∂L

∂ZT tY n=T

∂Zn ∂Zn−1

!

= ∂L

∂ZT

T Y n=t

Φn

!⊤

| {z } J ⊤

(t−1)→T

, (18)

where ∂Zn ∂Zn−1 = Φ⊤ n. Recalling the block structure from A.1, the transposed matrix is:

Φ⊤ n =

Dn 0 γI γI

⊤

=

D⊤ n γI 0 γI

.

The product J ⊤

(t−1)→T involves multiplying these upper-triangular matrices. Let J ⊤

(t−1)→T =

A B 0 C

, where the blocks are determined by induction over the sequence length T −t + 1:

## 1 Diagonal Blocks:

The top-left block A accumulates the sequence of memory transitions: A = Qt n=T D⊤ n. The bottom-right block C represents the persistent momentum decay: C = Qt n=T γI = (γI)T −t+1.

## 2 Off-diagonal Momentum Block:

The block B captures the cross-propagation from the momentum pathway into the memory state. Expanding the product, the top-right block accumulates terms where each momentum injection γI at step k is subsequently transformed by the memory transitions D⊤ j. This yields:

B =

T X k=t



 k+1 Y j=T

D⊤ j



(γI)k−t+1.

As γ →1, the bottom-right block C approaches the identity matrix, ensuring that a non-vanishing component of the gradient ∂L ∂MT is preserved and propagated back to Mt−1, regardless of the contractive nature of the memory transitions Dn. Substituting these blocks back into J ⊤

(t−1)→T completes the proof.

A.3. Proof of Corollary 3.5: Spectral Conditioning Proof. 1. Spectral Transformation. Let ˜X = X/ max(∥X∥F, δ), so ∥˜X∥F ≤1. By the standard inequality ∥·∥2 ≤∥·∥F, all singular values of ˜X satisfy σi ∈[0, 1]. Let ˜X = UΣV⊤be the SVD. Since ˜X ˜X⊤= UΣ2U⊤, the NS update satisfies:

NS(X) = a + b ˜X ˜X⊤+ c (˜X ˜X⊤)2 ˜X = U (aΣ + bΣ3 + cΣ5) | {z } = ρ(Σ)

V⊤, where ρ(σ) = aσ + bσ3 + cσ5 is applied entry-wise. Thus σmax(NS(X)) = maxi ρ(σi) ≤supσ∈[0,1] ρ(σ), and it suffices to analyze ρ on [0, 1]. 2. Global Extremum on [0, 1]. The derivative is:

ρ′(σ) = 3.4445 −14.325 σ2 + 10.1575 σ4.

Setting ρ′(σ) = 0 and substituting u = σ2 yields:

10.1575 u2 −14.325 u + 3.4445 = 0, ∆= 14.3252 −4(10.1575)(3.4445) ≈65.26 > 0.

The two roots are:

u1,2 = 14.325 ±

√

65.26 2 × 10.1575 ≈{0.3075, 1.1028}.

<!-- Page 15 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

Only u1 ≈0.3075 lies in [0, 1], giving the unique interior critical point σ∗= √u1 ≈0.5545. Since ρ′′(σ∗) = −28.65 σ∗+ 40.63 (σ∗)3 ≈−8.9593 < 0, this is a local maximum. Evaluating ρ at all candidates:

ρ(0) = 0, ρ(σ∗) = 3.4445(0.5545) −4.7750(0.5545)3 + 2.0315(0.5545)5 ≈1.2, ρ(1) = 3.4445 −4.7750 + 2.0315 = 0.701

Therefore:

sup σ∈[0,1]

ρ(σ) = ρ(σ∗) ≈1.2, which gives σmax(NS(X)) ≲1.2 = 1 + εu 3. Preservation of rank-1 structure. Factoring ρ(σ) = σ · q(σ2) where q(u) = cu2 + bu + a. The discriminant of q:

∆q = b2 −4ac = (4.7750)2 −4(3.4445)(2.0315) = 22.801 −27.985 = −5.189 < 0.

Since ∆q < 0 and c > 0, we have q(u) > 0 for all u ∈R. Therefore:

ρ(σ) > 0 ∀σ > 0, ρ(0) = 0.

It follows that rank(NS(X)) = rank(e X) = rank(X), preserving rank-1 structure.

A.4. Proof of Proposition 3.6: Backward Geometry of Newton–Schulz Normalization Proof. We prove the result for the normalized Newton–Schulz map in Definition 2.1, viewed as a function of the raw input X. Since ∥X0∥F = 1, and in practice δ < 1, the normalization is locally given by eX = X/∥X∥F around X0. Write

G(X) = P(eX) eX, P(Z) = aId + bZZ⊤+ c(ZZ⊤)2.

Let X0 = uw⊤with ∥u∥2 = ∥w∥2 = 1.

## 1 Differential of the

Frobenius normalization. For a perturbation H ∈Rd×m, the differential of eX = X/∥X∥F at X0 is d eX[H] = H −⟨X0, H⟩F X0 = H −(u⊤Hw)uw⊤. (19)

Define αH:= u⊤Hw, K:= d eX[H] = H −αHuw⊤.

Then u⊤Kw = αH −αH = 0.

2. Differential of the polynomial part. At X0 = uw⊤, we have eX0 eX⊤

0 = uu⊤, (eX0 eX⊤

0)2 = uu⊤.

Thus

P(eX0) = aId + (b + c)uu⊤.

Let

A = eX eX⊤.

The differential of A at eX0 in the direction K is dA[K] = Kwu⊤+ u(Kw)⊤.

Using u⊤Kw = 0, the differential of A2 is d(A2)[K] = dA[K]uu⊤+ uu⊤dA[K]

= Kwu⊤+ u(Kw)⊤.

Therefore, dP[K] = (b + c)

Kwu⊤+ u(Kw)⊤

.

<!-- Page 16 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

## 3 Full

Jacobian. By the product rule,

DGX0[H] = dP[K] eX0 + P(eX0)K

= (b + c)

Kwu⊤+ u(Kw)⊤ uw⊤+ aK + (b + c)uu⊤K. (20)

Since

(Kw)⊤u = u⊤Kw = 0, the term u(Kw)⊤uw⊤vanishes. Hence

DGX0[H] = (b + c)Kww⊤+ aK + (b + c)uu⊤K. (21)

Substituting K = H −αHuw⊤into Eq. (21) gives

DGX0[H] = aH + (b + c)Hww⊤+ (b + c)uu⊤H − a + 2(b + c)

αHuw⊤. (22)

4. Eigenvalue families. We evaluate Eq. (22) on the four orthogonal subspaces induced by u and w. Radial direction. Let H = uw⊤. Then αH = 1, Hww⊤= H, and uu⊤H = H. Therefore,

DGX0[H] = a + (b + c) + (b + c) −a −2(b + c)

H = 0.

Thus uw⊤has eigenvalue 0. Directions u⊥w⊤. Let H = pw⊤with p ⊥u. Then αH = 0, Hww⊤= H, and uu⊤H = 0. Hence

DGX0[H] = (a + b + c)H.

Thus these directions have eigenvalue a + b + c. Directions uw⊤

⊥. Let H = uq⊤with q ⊥w. Then αH = 0, Hww⊤= 0, and uu⊤H = H. Hence

DGX0[H] = (a + b + c)H.

Thus these directions also have eigenvalue a + b + c. Directions u⊥w⊤

⊥. Let H = pq⊤with p ⊥u and q ⊥w. Then αH = 0, Hww⊤= 0, and uu⊤H = 0. Hence

DGX0[H] = aH.

Thus these directions have eigenvalue a. The dimensions of the three eigenvalue families are respectively 1, (d −1) + (m −1) = d + m −2, and (d −1)(m −1), matching the statement of the proposition. Finally, for Frobenius normalization, Eq. (19) shows that the radial direction uw⊤is mapped to zero, while every direction orthogonal to uw⊤is unchanged. Therefore its eigenvalues are 0 in the radial direction and 1 on all tangent directions.

A.5. Proof of Proposition 3.8: Rank Enrichment Proof. We prove each part separately.

## 1 Momentum

Expansion. Expanding the recurrence

Mt = γMt−1 + NS(τβtvtk⊤ t)

with initial condition M0 = 0 gives

M1 = NS(τβ1v1k⊤

1),

M2 = γM1 + NS(τβ2v2k⊤

2)

= γNS(τβ1v1k⊤

1) + NS(τβ2v2k⊤ 2),

M3 = γM2 + NS(τβ3v3k⊤

3)

= γ2NS(τβ1v1k⊤

1) + γNS(τβ2v2k⊤ 2) + NS(τβ3v3k⊤ 3).

Continuing this expansion, or equivalently by induction, we obtain

Mt = t X s=1 γt−sNS(τβsvsk⊤ s).

This proves Eq. (11).

<!-- Page 17 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

## 2 Rank Upper

Bound. Each input injection

Xs = τβsvsk⊤ s has rank at most one. Moreover, the Newton–Schulz map in Definition 2.1 acts on the singular values of Xs while preserving its singular directions. Hence rank

NS(Xs)

≤rank(Xs) ≤1.

Using the sub-additivity of matrix rank, rank(Mt) ≤ t X s=1 rank

NS(τβsvsk⊤ s)

≤t.

Since Mt ∈Rd×m, its rank is also bounded by min(d, m). Therefore, rank(Mt) ≤min(t, d, m).

This proves Eq. (12).

## 3 Direction-Preserving Form of NS on Rank-1

Inputs. We next make explicit how the Newton–Schulz operator acts on each rank-1 update. Under the non-degeneracy assumptions τ > 0, βs > 0, vs̸ = 0, ks̸ = 0, define

ˆvs = vs ∥vs∥2

, ˆks = ks ∥ks∥2

, and

ˆσs = τβs∥vs∥2∥ks∥2 max(τβs∥vs∥2∥ks∥2, δ) ∈(0, 1].

Then the normalized input satisfies eXs = ˆσsˆvsˆk⊤ s.

Since this matrix is rank-1, we have eXs eX⊤ s = ˆσ2 s ˆvsˆv⊤ s, eXs eX⊤ s

2

= ˆσ4 s ˆvsˆv⊤ s.

Substituting these identities into Definition 2.1 gives

NS(Xs) = aId + bˆσ2 s ˆvsˆv⊤ s + cˆσ4 s ˆvsˆv⊤ s

ˆσsˆvsˆk⊤ s = aˆσs + bˆσ3 s + cˆσ5 s

ˆvsˆk⊤ s = ρ(ˆσs)ˆvsˆk⊤ s, where ρ(σ) = aσ + bσ3 + cσ5.

For the coefficients used in Definition 2.1, we have ρ(σ) > 0 for all σ > 0. Therefore, each non-degenerate NS-normalized update is a positive scalar multiple of the same rank-1 direction ˆvsˆk⊤ s. Consequently, the momentum state can be written as

Mt = t X s=1 λsˆvsˆk⊤ s, λs:= γt−sρ(ˆσs) > 0. (23)

<!-- Page 18 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

## 4 Attainability of the Upper

Bound. Let r = min(t, d, m).

We construct one explicit configuration for which rank(Mt) = r. Choose ˆv1,..., ˆvr to be orthonormal vectors in Rd and

ˆk1,..., ˆkr to be orthonormal vectors in Rm. If t > r, choose the remaining directions as

ˆvs = ˆv1, ˆks = ˆk1, s = r + 1,..., t.

Then Eq. (23) becomes

Mt = µ1ˆv1ˆk⊤

1 + r X s=2 λsˆvsˆk⊤ s, where µ1 = λ1 + t X s=r+1 λs > 0.

Equivalently,

Mt = AΛ′B⊤, where

A = [ˆv1,..., ˆvr] ∈Rd×r, B = [ˆk1,..., ˆkr] ∈Rm×r, and

Λ′ = diag(µ1, λ2,..., λr).

The matrices A and B have full column rank r, and Λ′ is invertible. Hence rank(Mt) = rank(AΛ′B⊤) = r = min(t, d, m).

Therefore, the upper bound is attainable.

## 5 Generic

Tightness. It remains to show that the rank-deficient case is non-generic. For fixed positive coefficients λ1,..., λt, the entries of

Mt = t X s=1 λsˆvsˆk⊤ s are polynomial functions of the direction coordinates {(ˆvs)i, (ˆks)j}s,i,j. The condition rank(Mt) < r is equivalent to the simultaneous vanishing of all r × r minors of Mt. Each such minor is a polynomial in the direction coordinates. The construction in Paragraph 4 shows that at least one r × r minor is not identically zero. Hence the set of direction pairs for which all r × r minors vanish is a proper algebraic subset of

(Sd−1 × Sm−1)t.

Such a proper algebraic subset has measure zero with respect to the product surface measure on the direction space. Therefore, under non-degenerate updates, the set of direction pairs {(vs, ks)}t s=1 for which rank(Mt) < min(t, d, m)

has measure zero. This proves that the upper bound is generically tight.

## Appendix

B: Training Details

In this appendix, we provide the parallel training algorithm for MuonSSM, followed by comprehensive details regarding the model architectures, training hyperparameters, and optimization settings used in our experiments across language, vision, and time-series modalities. All experiments were conducted on a single NVIDIA H100 GPU.

<!-- Page 19 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

## Algorithm

## 1 MuonSSM: Parallel

Mode (Training)

Input: K ∈RL×m, V ∈RL×d, Q ∈RL×m

Gates: α, β ∈RL

Params: δ, γ, τ, η // 1. Parallel Pre-computation for t = 1 to L in parallel do

Xt ←τβtvtk⊤ t Ut ←NS(Xt) Dt ←αt(Im −βtηktk⊤ t) end for // 2. Construct Associative Operators for t = 1 to L in parallel do

Φt ←

Dt 0m×m γIm γIm

∈R2m×2m

Ψt ←

Ut Ut

∈Rd×2m end for // 3. Parallel Associative Scan {Zt}L t=1 ←Scan({(Φt, Ψt)}L t=1, ⊕) 2

// 4. Extract Memory States S1:L ←[Z1[:,: m],..., ZL[:,: m]] // 5. Compute Outputs for t = 1 to L in parallel do yt ←Stqt end for Return {yt}L t=1

B.1. Parallel Training Algorithm Algorithm 1 provides the parallel training procedure for MuonSSM. The key observation is that the coupled memory– momentum dynamics can be written as a block-affine recurrence, allowing the sequence to be evaluated using an associative scan. The Newton–Schulz normalization is applied locally at each timestep and therefore does not affect the asymptotic scan complexity.

B.2. Language Modeling We base our language modeling experiments on the Gated DeltaNet architecture, replacing the standard Delta layers with our proposed MuonSSM blocks. The model configuration follows a standard small-scale setting (170M parameters) suitable for rigorous ablation. The specific architectural parameters are detailed in Table 8. Models are pre-trained on the FineWeb-Edu 10B token dataset using a causal language modeling objective. We utilize the AdamW optimizer with a cosine learning rate decay schedule. To ensure stability, we employ gradient clipping and a warmup period. The full training configuration is provided in Table 9.

B.3. Vision Spatial Modeling For visual representation learning, we adopt the training and evaluation protocols from MambaVision. We evaluate MuonSSM on three downstream tasks: Image Classification (ImageNet-1K), Object Detection (COCO), and Semantic Segmentation (ADE20K). We use the Tiny variant of the hierarchical architecture, replacing the spatial SSM mixers with MuonSSM layers. For object detection, we utilize the Mask R-CNN framework. For semantic segmentation, we employ the UperNet framework. Table 10 summarizes the specific hyperparameters used for each task.

B.4. Time-Series: Human Activity Recognition We evaluate MuonSSM on the Multi-Modal Activity (MMA) benchmarks. The experimental setup strictly controls for data preprocessing and model size to isolate algorithmic improvements. Data Preprocessing. Raw inertial signals (tri-axial accelerometer and gyroscope) are resampled and segmented into fixed-length windows of L = 512 with a 50% overlap. Each channel is standardized to zero mean and unit variance using training set statistics. The resulting segments are formatted as tensors X ∈RB×L×6, where B denotes the batch size.

<!-- Page 20 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Table 8.** Language model architecture configuration based on

Gated DeltaNet specifications.

Hyperparameter Value

Layers (N) 10 Heads (H) 12 Model Dimension (D) 672 Intermediate Dimension Context Length Vocab Size 32000

Local Window Size MuonSSM per Layer 1 Rotary Percentage 1.0 (100%) Normalization FusedRMSNorm (ϵ = 1e −5) MLP Type LLaMA MLP Precision bf16-mixed

**Table 9.** Language model training hyperparameters for pre-training

on FineWeb-Edu 10B.

Hyperparameter Value

Data & Batching Total Tokens 10B (1 × 1010) Global Batch Size 512 sequences Sequence Length

Optimization (AdamW) Peak Learning Rate 1 × 10−3

Min Learning Rate 1 × 10−4

Weight Decay 0.1 Betas (β1, β2) (0.9, 0.95) Gradient Clipping 1.0 Warmup Tokens 100M (1% of total)

**Table 10.** Vision Training Hyperparameters. Settings for Classification, Object Detection, and Semantic Segmentation.

Parameter Classification Object Detection Semantic Seg.

Dataset ImageNet-1K MS COCO ADE20K Framework - Mask R-CNN UperNet Optimizer LAMB AdamW AdamW Learning Rate (LR) 5e-3 / 1e-4 1e-4 5e-5 Weight Decay 0.05 0.05 0.01 Stochastic Depth 0.2 0.2 0.3 Batch Size 256 8 8 Training Duration 310 epochs 36 epochs 160K iters

## Model

Configuration. The backbone consists of a lightweight Conv1D front-end (kernel size 3, stride 1) for local feature extraction, followed by N = 2 stacked MuonSSM layers with a hidden dimension dmodel = 128. A global average pooling layer and a compact linear classification head produce the final predictions. Dropout with p = 0.1 is applied after the encoder and before the classification head. Training Setup. All models are trained end-to-end using categorical cross-entropy loss. We use the Adam optimizer with the following schedule: Initial Learning Rate: 1 × 10−3, Weight Decay: 1 × 10−4, Scheduler: Cosine annealing without restarts, Batch Size 16, Epochs: 50 with Early Stopping, patience = 10, Gradient Clipping: Global norm set to 1.0 to stabilize training dynamics.

B.5. Sensitivity Analysis and Robustness To evaluate the robustness of MuonSSM and its sensitivity to hyperparameter choices, we performed a comprehensive post-hoc analysis over two key parameters: the momentum coefficient γ ∈{0.0, 0.5, 0.8, 0.9, 0.95, 0.99} and the input scaling factor τ ∈{0.4, 0.5, 0.6, 0.8, 1.0, 1.2}. Model Selection Protocol. We emphasize that primary model selection was conducted strictly using validation sets. The results presented in Figure 6 serve as a post-hoc sensitivity analysis to demonstrate the stability of MuonSSM across diverse data distributions. Results and Discussion. As illustrated in the heatmaps, MuonSSM exhibits consistent performance gains over the baseline across a wide, principled range of hyperparameters. Specifically, within the recommended range of γ ∈[0.8, 0.99] and τ ∈[0.6, 0.8, 1.0] (12 configurations), the standard deviation in test accuracy remains minimal (e.g., ±0.27% for MuWiGes, ±0.63% for UESTC-MMEA-CL, and ±0.72% for MMAct). Table 11 provides a quantitative summary of these 12 configurations compared to the standard LongHorn baseline: This stability is theoretically grounded in our use of Newton–Schulz iteration, which bounds the singular values of updates (σmax ≤1), preventing uncontrolled amplification regardless of the specific scaling factor τ. These results suggest that MuonSSM can be reliably deployed with a default configuration (e.g., γ = 0.9, τ = 0.6) without the need for extensive per-dataset tuning.

<!-- Page 21 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Figure 6.** Post-hoc sensitivity analysis: Heatmap showing test accuracy (%) across different combinations of momentum tau (τ) and

momentum gamma (γ) parameters.

Dataset Baseline Min (in range) Max (in range) % configs ≥Base

MuWiGes 97.23 97.05 97.95 67% (8/12) UESTC-MMEA-CL 89.06 89.22 91.56 100% (12/12) MMAct 72.47 71.55 74.40 83% (10/12)

**Table 11.** Quantitative robustness summary across the principled hyperparameter range.

## Appendix

C: Additional Empirical Analyses

C.1. Empirical Evidence for NS-Induced Rank Enrichment Remark 3.7 suggests that the backward geometry of Newton–Schulz (NS) normalization biases the learning signal toward directions less aligned with the current rank-one write. When accumulated through the momentum recurrence, these less collinear writes are expected to increase the effective rank of the momentum state Mt. We empirically examine this mechanism using two complementary diagnostics.

1. Three-way normalization ablation. We compare three variants of the same backbone on MMAct under the same training setup: momentum alone, momentum with Frobenius normalization, and momentum with NS normalization. For each variant, we measure validation accuracy and the effective rank reff(Mt) = (P i σi(Mt))2 P i σ2 i (Mt). (24)

A higher effective rank indicates that the singular values of Mt are more evenly distributed, and hence that the momentum state uses more independent representational directions. Frobenius normalization provides only a small improvement over momentum alone, increasing the effective rank from 12.98 to 13.34. In contrast, NS increases the effective rank to 16.62 and improves validation accuracy by 2.14 percentage points over Frobenius normalization. This suggests that NS contributes more than magnitude normalization: its backward geometry encourages less redundant update directions when accumulated in Mt.

2. Rank truncation intervention. We further test whether the additional rank is functionally useful. After training a deep MuonSSM model, we apply SVD to the internal SSM representations and retain only the top-k singular components at inference time, while keeping all model parameters fixed. The results show a clear accuracy drop in the low-rank regime, indicating that the additional singular directions preserved by MuonSSM contribute to downstream prediction.

Interpretation. Together, these diagnostics support the mechanism described in Remark 3.7. Momentum accumulation can increase the nominal rank by summing rank-one writes, but repeated writes may still remain highly collinear. Frobenius normalization controls the scale of each write, whereas NS changes the backward geometry by emphasizing directions orthogonal to the current write. Empirically, this leads to higher effective rank and better downstream accuracy, consistent with the proposed rank-enrichment mechanism.

![Figure extracted from page 21](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-021-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 22 -->

MuonSSM: Orthogonalizing State Space Models for Sequence Modeling

**Table 12.** Three-way ablation isolating the role of NS in rank enrichment on MMAct. NS yields both higher effective rank and better validation accuracy than momentum alone and momentum with Frobenius normalization.

Variant Val. Acc. ↑ Effective Rank ↑

Momentum only 72.04 ± 0.58 12.98 ± 0.81 Momentum + Frobenius 72.53 ± 0.82 13.34 ± 0.43 Momentum + Newton–Schulz 74.67 ± 0.46 16.62 ± 0.57

**Figure 7.** Gradient norm heatmaps over timesteps and training iterations. Each value is ∥∂L/∂hn∥2. Compared with Mamba,

MuonMamba shows more uniform gradient propagation across long contexts, supporting the structural gradient-preservation mechanism in Proposition 3.3.

C.2. Gradient Propagation Heatmaps Proposition 3.3 shows that the momentum pathway provides an additional route for gradient propagation through the (γIm)T −t+1 block. Since practical models include nonlinearities, gating, normalization, and deep stacking, we complement this linear analysis with an empirical gradient-propagation diagnostic. We compare Mamba and MuonMamba under the same language modeling setup with sequence length 2048 over approximately 60K training iterations. At selected iterations, we record the gradient norm with respect to the hidden state at each timestep:

g(n) =

∂L ∂hn

2.

**Figure 7.** visualizes these values as heatmaps over timesteps and training iterations. Vanilla Mamba exhibits a clear gradient decay pattern, with much smaller gradient norms for earlier tokens. In contrast, MuonMamba maintains a more uniform gradient profile across the sequence. This supports the interpretation that the momentum pathway mitigates long-range gradient attenuation in realistic nonlinear training, although it does not constitute a strict non-vanishing gradient guarantee.

![Figure extracted from page 22](2026-ICML-muonssm-orthogonalizing-state-space-models-for-sequence-modeling/page-022-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
