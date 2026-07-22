---
title: "PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA"
source_url: https://icml.cc/virtual/2026/oral/71157
paper_pdf_url: https://arxiv.org/pdf/2606.00944v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

<!-- Page 1 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Shihao Wang 1 Xueru Zhang 1

## Abstract

Applying differential privacy (DP) via DP-SGD to Low-Rank Adaptation (LoRA) is a natural approach for privacy-preserving fine-tuning. However, LoRA’s low-rank parameterization poses a fundamental challenge. In LoRA, each trainable update is represented as a low-rank matrix Z = AB⊤, but this factorization is inherently nonidentifiable: many factor pairs (A, B) represent the same update Z. As a result, applying DP-SGD directly to the factors induces gauge-dependent perturbations on Z, and we show that this naive DP-LoRA can lead to unbounded noise amplification. We propose PRISM, an intrinsic DP mechanism for LoRA that is gauge invariant by construction, avoids bilinear noise amplification, and admits an efficient low-dimensional noise sampler. Moreover, PRISM yields a closed-form characterization of the effective intrinsic noise induced on Z, enabling stable privacy–utility tradeoffs through bounded, gauge-invariant perturbations. We establish standard (ε, δ)-DP guarantees for PRISM and introduce a DP-aware, gaugeinvariant adaptive update rule that prevents adaptive optimization from amplifying injected privacy noise, improving numerical stability in practice.

## 1. Introduction

Foundation models are routinely adapted to domain-specific tasks using private corpora. Because full-model fine-tuning is costly, practitioners often adopt parameter-efficient finetuning (PEFT) methods, which update only a small subset of parameters while keeping the backbone frozen. Common methods include adapters (Houlsby et al., 2019; Hu et al., 2023), prefix/prompt tuning (Li & Liang, 2021; Lester et al., 2021), bias-only updates (Ben Zaken et al., 2022), and

1Department of Computer Science and Engineering, The Ohio State University, Columbus, OH, USA. Correspondence to: Shihao Wang <wang.17571@osu.edu>, Xueru Zhang <zhang.12807@osu.edu>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

lightweight reparameterizations (Liu et al., 2022). Among these, Low-Rank Adaptation (LoRA) (Hu et al., 2022) has emerged as a dominant method due to its drop-in compatibility with existing linear layers, strong performance under low-precision training with a quantized backbone (Dettmers et al., 2023; Li et al., 2024), and the non-identifiability induced by its low-rank parameterization. Formally, LoRA adapts a frozen pretrained weight matrix W0 ∈Rm×n by adding a low-rank update Z:

W = W0 + Z, Z = AB⊤ (1)

where A ∈Rm×r, B ∈Rn×r with rank r ≪min{m, n}. Rather than updating W0 directly, optimization proceeds over (A, B), which implicitly define the intrinsic update Z applied to the backbone. This low-rank factorization substantially reduces the number of trainable parameters.

Despite its efficiency, PEFT on sensitive data raises significant privacy concerns. Prior work has shown that trained models can leak information about training data through membership, inversion, or extraction attacks (Fredrikson et al., 2015; Shokri et al., 2017; Ganju et al., 2018; Carlini et al., 2019; 2021). These risks are often exacerbated in PEFT settings, where fine-tuning datasets are small, domainspecific, and contain rare or uniquely identifying records.

Various approaches have been proposed to mitigate privacy risks in large models (Bourtoule et al., 2021). We focus on differential privacy (DP) (Dwork et al., 2006; Dwork & Roth, 2014), which provides an attack-agnostic, ex ante guarantee by bounding the influence of any individual record and remaining robust to arbitrary post-processing. In practice, DP is most commonly instantiated via DP-SGD (Abadi et al., 2016), which clips per-example gradients and injects calibrated Gaussian noise before each update.

A natural approach to obtaining DP in LoRA fine-tuning is to apply DP-SGD directly to the low-rank factors (A, B) (Yu et al., 2022; Liu et al., 2025; Xu et al., 2025). Some variants further freeze one of the two factors to improve numerical stability (Sun et al., 2024). While straightforward, this strategy is fundamentally misaligned with the structure of LoRA and leads to ill-defined private updates.

The core issue is that DP-SGD is defined relative to a parameterization, whereas in LoRA the factors (A, B) are only an auxiliary representation of the intrinsic update applied to arXiv:2606.00944v1 [cs.LG] 31 May 2026

<!-- Page 2 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

**Table 1.** Comparison with other DP-LoRA design choices. We

evaluate each variant against three desiderata: (a) gauge-invariant randomized mechanism, (b) additive perturbations on Z (i.e., no bilinear DP term), and (c) LoRA-scale efficiency. The naive factorspace variant violates (a) and (b), yielding unbounded effective intrinsic noise EZ. The one-sided variant, which updates B only while freezing A, satisfies (b) and (c) but not (a). PRISM satisfies all three and admits a closed-form expression for EZ.

METHOD PARAMS EZ (a) (b) (c)

DP-LORA (m+n)r UNBOUNDED ✗ ✗ ✓ ONE-SIDE nr (σC/b)√n ∥A∥F ✗ ✓ ✓ PRISM (m+n)r (σC/b)

p r(m+n−r) ✓ ✓ ✓ the frozen backbone. It is the effective update Z = AB⊤, rather than the factors themselves, that ultimately determines model behavior. As a consequence, naively applying DP-SGD in factor space (i) induces gauge-dependent perturbations on the intrinsic update Z, meaning that different factor pairs corresponding to the same intrinsic update can induce significantly different clipping and noise effects; (ii) introduces spurious higher-order noise terms caused by independently noising the two factors, resulting in quadratic noise effects that do not arise in standard DP-SGD on linear parameters; and (iii) interacts poorly with optimization dynamics, where adaptive preconditioning can amplify stochasticity and lead to numerical instability. We discuss these issues in detail in Section 2.

These issues motivate a key design principle: the randomized DP mechanism should operate on the space of intrinsic model updates, rather than on a gauge-redundant factorization. Based on this, we propose the Projected Riemannian Invariant Subspace Mechanism (PRISM), which performs DP-SGD directly on the rank-r manifold of LoRA updates. Specifically, PRISM projects per-example gradients to the tangent space ∆Z ∈TZMr, applies global Frobeniusnorm clipping and isotropic tangent Gaussian noise in this intrinsic space, and retracts back to rank r. By aligning the DP mechanism with the intrinsic update Z, PRISM ensures that the effective intrinsic noise on Z is deterministic and independent of the particular factorization (A, B). Moreover, operating in intrinsic coordinates keeps updates additive and avoids the spurious bilinear second-order noise terms induced by independently noising the factors. Importantly, PRISM achieves these guarantees with LoRA-scale computational cost. Table 1 compares PRISM with existing DP-LoRA design choices.

Our contributions can be summarized below.

• We identify issues with factor-space DP-LoRA and show that they can lead to (i) gauge-dependent clipping and noise injection, (ii) unbounded amplification of intrinsic noise, and (iii) spurious bilinear second-order noise terms arising from independently noising the two factors.

• We propose PRISM, a gauge-invariant DP mechanism that projects per-example gradients on rank-r tangent space, applies global intrinsic clipping across all LoRA modules, injects isotropic tangent noise using an O((m + n)r2) sampler, and retracts updates back to rank r. • We develop a DP-aware gauge-invariant adaptive update rule that floors rank-space preconditioners based on the DP noise level, mitigating optimizer-induced noise amplification while preserving LoRA-scale efficiency. • We provide theoretical guarantees showing that PRISM produces gauge-invariant updates and noise distributions, satisfies (ε, δ)-DP under subsampled Gaussian accounting, and injects tangent noise with gauge-invariant covariance and energy proportional to r(m + n −r). The project code is available at github.com/osu-srml/PRISM-DP-LoRA.

## 2. Problem Formulation

We study differentially private (DP) parameter-efficient finetuning using LoRA. Given a frozen weight matrix W0 ∈ Rm×n, LoRA learns a rank-r update Z such that W = W0 + Z with Z = AB⊤(Eq. (1)), by minimizing the empirical risk over a private dataset D = {xi}N i=1:

min F(A, B) ≜1

N

PN i=1 ℓi(W0 + AB⊤).

Our goal is to design a randomized training procedure whose released adapter Z satisfies (ε, δ)-DP (Dwork & Roth, 2014) with respect to D, while preserving the utility of LoRA.

Formally, an algorithm M satisfies (ε, δ)-DP if, for any adjacent datasets D, D′ and any measurable event S,

Pr[M(D) ∈S] ≤eε Pr[M(D′) ∈S] + δ, (2)

A standard approach for achieving DP in model training is DP-SGD (Abadi et al., 2016). At each iteration, DP- SGD computes per-example gradients gi = ∇ℓi, clips them to a prescribed norm C and aggregates them with added Gaussian noise ξ ∼N(0, I):

˜gi = gi max{1, ∥gi∥2/C}, bg = 1 b b X i=1

˜gi + σC b ξ (3)

where b denotes the batch size and σ is the noise multiplier. The noisy bg is then used to perform an optimizer update.

A dominant approach in DP-LoRA applies DP-SGD directly to the factor parameters (A, B) (Yu et al., 2022; Liu et al., 2025; Xu et al., 2025). Specifically, let gA,i, gB,i denote the per-example gradients with respect to A and B, respectively. This approach applies (3) to the concatenated gradient gi = (gA,i, gB,i) with ∥gi∥2

2 = ∥gA,i∥2 F + ∥gB,i∥2

F. Some works further consider variants with one-sided training that updates

<!-- Page 3 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA only one LoRA factor while freezing the other (Sun et al., 2024). However, enforcing DP on the factors (A, B) is fundamentally misaligned with the effective update Z = AB⊤that governs model behavior, as we detail below.

Issue I: Factor-space DP violates LoRA gauge symmetry. LoRA factorization is non-identifiable (Hu et al., 2022): for any invertible R ∈GL(r), the factor pairs (A, B) and (AR, BR−⊤) induce the same intrinsic update Z. Under such a gauge transformation (A, B) 7→(AR, BR−⊤), the corresponding per-example gradients transform as g′

A,i = gA,iR−⊤, g′

B,i = gB,iR.

As a result, the clipping norm, and hence the clipping coefficient, used in DP-SGD depend on the particular factorization chosen to represent Z. For example, under the simple rescaling gauge (A, B) 7→(cA, c−1B),

∥g′

A,i∥2

F + ∥g′

B,i∥2

F = c−2∥gA,i∥2

F + c2∥gB,i∥2

F. (4)

which can vary arbitrarily with c. Consequently, the distribution of the clipped-and-noised update produced in factor space is gauge dependent, and the induced intrinsic update is not determined by Z alone (Appendix A.21).

This gauge dependence propagates from gradient clipping to the resulting update increments. Even when a per-example increment (∆Ai, ∆Bi) represents a fixed intrinsic direction ∆Zi = ∆AiB⊤+ A∆B⊤ i, the same intrinsic direction admits gauge-related representatives (∆A′ i, ∆B′ i) = (∆AiR, ∆BiR−⊤) for any R ∈GL(r). In general,

∥∆A′ i∥2

F + ∥∆B′ i∥2

F̸ = ∥∆Ai∥2

F + ∥∆Bi∥2

F, (5)

so any mechanism that clips and perturbs based on the Euclidean norms in factor space is inherently gauge dependent.

Formally, let ∆Zfac(A, B) denote the intrinsic update induced by a single factor-space DP-SGD step. A gaugerespecting mechanism would require

∆Zfac(A, B)

d= ∆Zfac(AR, BR−⊤), ∀R ∈GL(r), (6)

a condition already violated by Eq. (4). Importantly, this issue is distinct from, and not resolved by, deterministic transformation-invariant optimizers for LoRA (Yen et al., 2025), as DP requires invariance of the randomized clipping and noising procedure itself.

Issue II: Noising both factors injects bilinear and gaugeamplified intrinsic noise. When DP noise is injected into both factors, the intrinsic update inevitably contains a second-order noise term. Consider a single update step

1Throughout the paper, we state the main claims in the main text and defer detailed analysis and proofs to the appendix, with explicit appendix references provided after each claim.

(A, B) ←(A, B) + (∆A, ∆B), and let ξA, ξB denote the

Gaussian perturbations added by DP-SGD, scaled by the step size η. The induced intrinsic update then satisfies

Z+ = (A + ∆A + ηξA) (B + ∆B + ηξB)⊤

= Z + ∆Z + η ξAB⊤+ Aξ⊤

B

+ η2 ξAξ⊤

B. (7)

The final term η2ξAξ⊤

B arises from multiplying independently noised factors and cannot be produced by any additive noise mechanism applied directly to Z (Appendix A.3).

Even if this second-order term is ignored, the first-order intrinsic noise remains problematic, as its magnitude depends on the norms of the factors (see Proposition 2.2, Eq. (8)). Under rescaling gauge (A, B) 7→(cA, c−1B), Eq. (8) becomes τ 2 mc−2∥B∥2

F + nc2∥A∥2

F

, which can grow without bound as c →0 or c →∞. One-sided variants that freeze one LoRA factor (Sun et al., 2024) can suppress parts of Eq. (7), but do not eliminate the dependence of intrinsic noise energy on a representation-dependent scale, since the frozen factor still determines ∥A∥F or ∥B∥F. This motivates enforcing DP directly in the intrinsic space of Z (or its tangent space), rather than in factor coordinates.

To formalize the scale of randomized perturbations on Z, we introduce the following notion.

Definition 2.1 (Effective intrinsic noise). For a random intrinsic perturbation NZ, define EZ ≜ p

E∥NZ∥2

F.

Proposition 2.2 (Intrinsic noise energy under factor noising). Let ξA ∈Rm×r and ξB ∈Rn×r be independent with i.i.d. entries N(0, τ 2), and define NZ = ξAB⊤+ Aξ⊤

B + ξAξ⊤

B. Then the first-order term N (1)

Z ≜ξAB⊤+ Aξ⊤

B satisfies

E∥N (1)

Z ∥2

F = τ 2 m∥B∥2

F + n∥A∥2

F

, (8)

while the bilinear term N (2)

Z ≜ξAξ⊤

B satisfies

E∥N (2)

Z ∥2

F = mnr τ 4. (9)

Proposition 2.2 reveals that factor-space noising induces intrinsic noise whose first-order component scales with ∥A∥F, ∥B∥F and whose second-order bilinear component scales as mnr τ 4, leading to gauge-dependent amplification and an unavoidable η2 noise term.

Corollary 2.3 (Unbounded gauge amplification). Fix Z = AB⊤̸ = 0 and τ 2 > 0. Along the scalar gauge family (Ac, Bc) = (cA, c−1B), the first-order effective intrinsic noise EZ defined in Eq. (8) is unbounded over c > 0 even though AcB⊤ c = Z is constant.

See Appendix A.4-A.5 for derivations. Corollary 2.3 shows that factor-space DP induces gauge-dependent and potentially unbounded intrinsic noise, even when the effective update Z is fixed.

<!-- Page 4 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Issue III: Adaptive preconditioning magnifies DP noise and stresses low-rank numerics. Private PEFT methods typically rely on adaptive optimizers such as Adam and AdamW to maintain utility under noisy gradients (Kingma & Ba, 2015; Loshchilov & Hutter, 2019), and recent LoRAspecific invariant optimizers extend the same principle (Yen et al., 2025). Conceptually, these methods apply a (possibly low-dimensional) preconditioner to the DP gradient:

θ+ = θ −η P−1/2bg, bg = g + ξ (10)

where ξ ∼N(0, Σξ) denotes the injected DP noise. The resulting update noise is therefore η P−1/2ξ with covariance η2 P−1/2ΣξP−1/2. Because the preconditioner P is estimated from noisy gradients, adaptive optimizers inevitably adapt to the injected DP noise. When DP noise dominates the true gradient signal, the preconditioner is largely determined by noise statistics, yielding P ≈E[ξξ⊤] = Σξ. In this regime, the update noise covariance becomes η2 P−1/2ΣξP−1/2 ≈η2I, i.e., adaptive preconditioning can normalize/reshape the injected DP noise so that the effective update noise is no longer scaled in a simple way by the base DP-SGD noise level. This noisy-moment-driven behavior is known to undermine the benefits of black-box combinations of DP with adaptive optimizers, and has motivated several DP-aware adaptive variants (e.g., leveraging side information, delayed/stale preconditioners, or biascorrected moment estimation) (Li et al., 2022; 2023; Tang et al., 2024).

These issues are further exacerbated in LoRA setting. Adaptive and invariant LoRA optimizers often involve operations on small r × r Gram matrices such as M = A⊤A and N = B⊤B (e.g., via inverses, pseudoinverses, or inverse square roots). DP noise and gauge drift can drive these matrices to- ward ill-conditioning, where ∥M †/2 ∥2 = 1/ q λ+ min(M) becomes large. This both amplifies noise in the update and destabilizes numerical routines such as eigendecompositions. Consequently, a practical DP-LoRA mechanism must control not only intrinsic sensitivity and noise injection, but also the interaction between privacy noise and adaptive preconditioning under low-rank numerical constraints.

Design target. We aim to develop a DP-LoRA procedure whose randomized update of the intrinsic parameter is (i) gauge invariant in distribution, (ii) additive in an intrinsic (tangent) representation, thereby avoiding bilinear noise, and (iii) stable under adaptive optimization and preconditioning, without magnifying DP noise or destabilizing low-rank numerical operations.

## 3. Proposed Method: PRISM

To address the issues in Section 2, we propose the Projected Riemannian Invariant Subspace Mechanism (PRISM), a

## Algorithm

## 1 One PRISM update across all

LoRA modules

1: Input: LoRA factors {(Aℓ, Bℓ)}L ℓ=1, minibatch {xi}b i=1, clip C, noise multiplier σ, learning rate η. 2: Per-example intrinsic norms: 3: for i = 1 to b do 4: For each module ℓ, compute lifted tangent gradient (∆Ai,ℓ, ∆Bi,ℓ) via Eq. (14). 5: Compute ∥∆Zi,ℓ∥2

F via Eq. (15), and si via Eq. (16). 6: Set clipping coefficient αi = min{1, C/si}. 7: end for 8: Module-wise DP tangent update: 9: for each module ℓdo 10: ¯∆Aℓ= 1 b

P i αi∆Ai,ℓ, ¯∆Bℓ= 1 b

P i αi∆Bi,ℓ. 11: Sample tangent noise (ΞA,ℓ, ΞB,ℓ) via Eq. (19).

12: ∆Adp ℓ = ¯∆Aℓ+ σC b ΞA,ℓ, ∆Bdp ℓ = ¯∆Bℓ+ σC b ΞB,ℓ. 13: Compute DP-aware invariant adaptive direction (UA,ℓ, UB,ℓ) using Eqs. (24)–(26). 14: Retract via Eq. (22): (Aℓ, Bℓ) ←Retrr

Aℓ, Bℓ; −ηUA,ℓ, −ηUB,ℓ

. 15: end for 16: Output: updated LoRA factors.

DP-LoRA procedure that applies DP-SGD in the intrinsic geometry of low-rank updates. For simplicity, we previously described LoRA for a single weight matrix W = W0 + AB⊤; in practice, LoRA is applied to multiple layers of a model. We therefore consider a LoRA model with L LoRA modules (i.e., LoRA-augmented layers), indexed by ℓ(Hu et al., 2022). Each module ℓhas factor parameters (Aℓ, Bℓ) and an intrinsic update Zℓ= AℓB⊤ ℓ. For each training example i, we denote the intrinsic gradient Gi,ℓ≜∇Zℓℓi. By the chain rule, the corresponding factor gradients satisfy gA,i,ℓ= Gi,ℓBℓand gB,i,ℓ= G⊤ i,ℓAℓ.

Overview. Algorithm 1 summarizes one PRISM update applied across all LoRA modules. Rather than directly perturbing the non-identifiable factors, it performs DP-SGD on the intrinsic parameters {Zℓ} by operating on tangent directions of the fixed-rank manifold Mr. For each sample i and module ℓ, PRISM computes a lifted tangent gradient (∆Ai,ℓ, ∆Bi,ℓ) (line 4), which is a factor-space representa- tion of an intrinsic tangent matrix ∆Zi,ℓ∈TZℓMr satisfying ∆Zi,ℓ= ∆Ai,ℓB⊤ ℓ+ Aℓ∆B⊤ i,ℓ. Using these intrinsic tangent matrices, PRISM computes a per-example intrinsic norm aggregated across all modules and applies a single global clipping coefficient αi (lines 3-7), yielding a unified sensitivity bound for the entire LoRA update.

PRISM then proceeds module-wise: it averages the clipped lifted tangents over the minibatch (line 10) and adds isotropic tangent Gaussian noise to form the DP tangent update (∆Adp ℓ, ∆Bdp ℓ) (lines 11–12). It applies a DP-aware, gauge-invariant adaptive transform to obtain (UA,ℓ, UB,ℓ)

<!-- Page 5 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

(line 13), and retracts back to rank r to update (Aℓ, Bℓ) (line 14). The remainder of this section details these components and explains how they address Issues I–III.

## 3.1. Tackle Issue I: Gauge-Invariant Tangent Projection

To eliminate the gauge dependence of factor-space updates, we treat the intrinsic update Zℓ= AℓB⊤ ℓas a point on the fixed-rank manifold Mr and operate directly in its tangent space. For full-column-rank Aℓ, Bℓ, the tangent space at Zℓ admits the characterization (Appendix A.6)

TZℓMr = {∆Zℓ= ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ}, (11)

where ∆Aℓ∈Rm×r and ∆Bℓ∈Rn×r. We refer to any pair (∆Aℓ, ∆Bℓ) satisfying this relation as a (factor-space) lift of the intrinsic tangent matrix ∆Zℓ. While such lifts are not unique, the induced matrix ∆Zℓdepends only on Zℓ (Appendix A.7).

To define a gauge-invariant intrinsic gradient, we introduce the orthogonal projectors onto the column spaces of factors,

ΠAℓ≜Aℓ(A⊤ ℓAℓ)†A⊤ ℓ, ΠBℓ≜Bℓ(B⊤ ℓBℓ)†B⊤ ℓ. (12)

Given a per-example intrinsic gradient Gi,ℓ∈Rm×n, we project it onto the tangent space via

PAℓ,Bℓ(Gi,ℓ) ≜Gi,ℓ−(I −ΠAℓ) Gi,ℓ(I −ΠBℓ) (13)

= ΠAℓGi,ℓ+ Gi,ℓΠBℓ−ΠAℓGi,ℓΠBℓ.

which depends only on ΠAℓ, ΠBℓ, and hence is invariant to the gauge transformation. As a result, the projected tangent direction PAℓ,Bℓ(Gi,ℓ) represents an intrinsic update of Zℓthat is independent of the chosen factorization (Appendix A.8).

To obtain a concrete factor-space representation, we adopt a canonical horizontal lift that maps the intrinsic tangent direction back to factor space in a gauge-consistent manner. Let gA,i,ℓ= Gi,ℓBℓ, gB,i,ℓ= G⊤ i,ℓAℓ, and define Mℓ= A⊤ ℓAℓ, Nℓ= B⊤ ℓBℓ. We set

∆Ai,ℓ= gA,i,ℓN † ℓ−1

2ΠAℓ gA,i,ℓN † ℓ

,

∆Bi,ℓ= gB,i,ℓM † ℓ−1

2ΠBℓ gB,i,ℓM † ℓ

.

(14)

which satisfies ∆Ai,ℓB⊤ ℓ+ Aℓ∆B⊤ i,ℓ= PAℓ,Bℓ(Gi,ℓ) (Appendix A.9).

## 3.2. Tackle Issue II: Global Intrinsic DP Mechanism

We next design a DP mechanism that operates directly on intrinsic tangent updates, thereby avoiding amplified noise inherent to factor-space perturbations. Given lifted tangent directions (∆Ai,ℓ, ∆Bi,ℓ) obtained from Eq. (14), we measure the magnitude of tangent directions using the Frobenius norm ∥∆Zi,ℓ∥2

F = ∥∆Ai,ℓB⊤ ℓ+ Aℓ∆B⊤ i,ℓ∥2

F, which can be computed efficiently (Appendix A.10):

∥∆Zi,ℓ∥2

F = tr

∆A⊤ i,ℓ∆Ai,ℓNℓ

+ tr

∆B⊤ i,ℓ∆Bi,ℓMℓ

+ 2 tr

(A⊤ ℓ∆Ai,ℓ)(B⊤ ℓ∆Bi,ℓ)

. (15)

In the common per-example gradient setting, Eq. (15) further simplifies (Appendix A.11).

To control sensitivity across all LoRA modules, we aggregate intrinsic norms and define the global intrinsic norm si ≜

PL ℓ=1 ∥∆Zi,ℓ∥2

F

1/2

(16)

We then compute per-example clipping coefficients αi ≜ min{1, C/si}. Each module aggregates the clipped lifts as

¯∆Aℓ= 1 b

P i αi∆Ai,ℓand ¯∆Bℓ= 1 b

P i αi∆Bi,ℓ. This mirrors DP-SGD sensitivity control (Eq. (3)), but crucially operates in the intrinsic geometry of LoRA.

Isotropic tangent noise. For each module ℓ, PRISM adds Gaussian noise directly in the tangent space,

(∆Adp ℓ, ∆Bdp ℓ) = (¯∆Aℓ, ¯∆Bℓ)+ σC b (ΞA,ℓ, ΞB,ℓ), (17)

where the random pair (ΞA,ℓ, ΞB,ℓ) is constructed so that ΞA,ℓB⊤ ℓ+ AℓΞ⊤

B,ℓ∼PAℓ,Bℓ(Ξℓ) for Ξℓ∼N(0, Imℓ×nℓ) (Appendix A.12). PRISM uses factor-space lifts for efficiency, but the released update is intrinsic and invariant to the factor lift; hence it admits an equivalent lift-free form:

d ∆Zℓ= 1 b b X i=1 αi ∆Zi,ℓ+ σC b PAℓ,Bℓ(Ξℓ), (18)

where ∆Zi,ℓ= PAℓ,Bℓ(Gi,ℓ) ∈TZℓMr. This intrinsic form is convenient for stating gauge invariance and privacy guarantees; in implementation, to sample PAℓ,Bℓ(Ξℓ) efficiently, we avoid drawing a full mℓ× nℓGaussian matrix and instead use a low-dimensional factor sampler (Appendix A.13-A.15):

ΞA,ℓ= (I −ΠAℓ)ΩA,ℓN

−1

2 ℓ, ΞB,ℓ= ΩB,ℓM

−1

2 ℓ. (19)

with ΩA,ℓ∼N(0, Imℓ×r) and ΩB,ℓ∼N(0, Inℓ×r).

Theorem 3.1 (Isotropic tangent noise and closed-form intrinsic energy). Let Ξℓ∈Rmℓ×nℓhave i.i.d. N(0, 1) entries. Then PAℓ,Bℓ(Ξℓ) is an isotropic Gaussian supported on TZℓMr and

E∥PAℓ,Bℓ(Ξℓ)∥2

F = r(mℓ+ nℓ−r). (20)

Therefore, the effective intrinsic noise of PRISM perturba- tion N PRISM

Zℓ = σC b PAℓ,Bℓ(Ξℓ) is

EPRISM

Zℓ = σC b p r(mℓ+ nℓ−r). (21)

<!-- Page 6 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

See Appendix A.16 for the proof, with supporting results in Appendix A.17-A.18 and concentration bounds in Appendix A.19. Theorem 3.1 shows that projecting a dense Gaussian matrix onto the rank-r tangent space yields an isotropic Gaussian supported on that subspace with expected squared norm r(m + n −r). Consequently, PRISM induces intrinsic noise on Z whose magnitude depends only on (σ, C, b) and layer dimensions, and is independent of gauge-dependent quantities ∥A∥F, ∥B∥F.

Retraction without bilinear noise. Given the noisy tangent direction, PRISM updates the intrinsic parameter via a retraction onto the fixed-rank manifold Mr,

Z+ ℓ = Retrr

Zℓ−η(∆Adp ℓB⊤ ℓ+ Aℓ(∆Bdp ℓ)⊤)

, (22)

where Retrr(·) denotes the best rank-r approximation in Frobenius norm (Appendix A.20). Because (22) is additive in the intrinsic tangent perturbation, this step avoids the bilinear second-order noise term η2ξA,ℓξ⊤

B,ℓthat arises when independently noising both factors (Eq. (7); Appendix A.21). Consequently, the effective intrinsic noise induced by PRISM admits a closed-form characterization (Eq. (21)), and retraction introduces only second-order distortion through the lifted factor-product residual.

Proposition 3.2 (Retraction distortion is second order). Let Z = AB⊤∈Mr, with A, B full column rank, and let ∆Z = ∆AB⊤+ A∆B⊤∈TZMr be a lifted tangent perturbation. For the truncated-SVD retraction Retrr and any η ≥0,

∥Retrr(Z −η∆Z) −(Z −η∆Z)∥F ≤η2∥∆A∆B⊤∥F.

(23) Since ∥∆A∆B⊤∥F ≤∥∆A∥F ∥∆B∥F, the distortion is O(η2) for fixed ∆A, ∆B; equivalently, Retrr(Z−η∆Z) = Z −η∆Z + O(η2) as η →0.

Proposition 3.2 shows that retraction is first-order exact for the lifted tangent step used by PRISM. Thus, the DP perturbation remains additive to first order; the only discrepancy is the second-order residual in Eq. (23), rather than an explicit factor-space bilinear noise term.

Theorem 3.3 (Gauge invariance of PRISM). Fix (σ, C, b) and consider one PRISM step at intrinsic state Zℓ= AℓB⊤ ℓ. For any R ∈GL(r) and gauge-equivalent factors (A′ ℓ, B′ ℓ) = (AℓR, BℓR−⊤), the distribution of the intrinsic DP increment in Eq. (18) is invariant:

d ∆Zℓ(Aℓ, Bℓ)

d= d ∆Zℓ(A′ ℓ, B′ ℓ).

Since retraction in Eq. (22) is deterministic post-processing, Z+ ℓis also gauge invariant in distribution.

Theorem 3.3 implies that PRISM is a well-defined randomized mechanism on the rank-r manifold: the law of the clipped-and-noised increment is determined by Zℓ alone, not by the particular factor gauge (Aℓ, Bℓ). See Appendix A.22 for the proof.

Privacy guarantee. Eq. (18) is a (subsampled) Gaussian mechanism on a linear space, and all subsequent operations—adaptive post-processing, factorization, alignment, and retraction—are DP-preserving by post-processing (Appendix A.23 and Appendix A.24). Theorem 3.4 (DP guarantee of PRISM). Assume Poisson subsampling with rate q = b/N and per-example intrinsic clipping at threshold C (Eq. (16)). Each PRISM iteration is a subsampled Gaussian mechanism with noise multiplier σ. Consequently, for any target δ ∈(0, 1), after T iterations PRISM satisfies (ε, δ)-DP, where ε is determined by composing T subsampled Gaussian mechanisms and can be computed numerically using the privacy loss random variable (PRV) accountant (Gopi et al., 2021; Yousefpour et al., 2022; Opacus Contributors, 2026).

Theorem 3.4 shows that each PRISM iteration is a subsampled Gaussian mechanism on intrinsic tangent updates; the remaining operations are DP-preserving post-processing. Hence, standard DP-SGD accounting applies; see Appendix A.25 for the composition analysis.

## 3.3. Tackle Issue III: DP-Aware Gauge-Invariant Adaptivity and Numerical Stability

The mechanism in Eq. (17) produces a DP-sanitized tangent direction; by the post-processing property of DP, any subsequent transformation preserves the DP guarantee. We leverage this property to design a gauge-invariant adaptive update that is robust to privacy noise. For clarity, we describe the computation for a single LoRA module ℓ.

Right-invariant preconditioning in rank space. For each module ℓ, we track first moments mA,ℓ, mB,ℓand rank-space second moments VA,ℓ, VB,ℓ∈Rr×r defined as, mA,ℓ←β1mA,ℓ+ (1 −β1) ∆Adp ℓ,

VA,ℓ←β2VA,ℓ+ (1 −β2) (∆Adp ℓ)⊤∆Adp ℓ mℓ

.

(24)

with analogous updates for mB,ℓ, VB,ℓ(replacing mℓby nℓ). We precondition on the right by inverse square roots and set the adaptive direction

UA,ℓ= mA,ℓ(VA,ℓ+ λA,ℓI)−1/2,

UB,ℓ= mB,ℓ(VB,ℓ+ λB,ℓI)−1/2. (25)

Under a gauge action (Aℓ, Bℓ) 7→(AℓR, BℓR−⊤), VA,ℓ and VB,ℓtransform by congruence and (25) yields the same intrinsic update UA,ℓB⊤ ℓ+ AℓU ⊤

B,ℓ.

DP-aware floors and conditioning control. Adaptive preconditioners can amplify DP noise when VA,ℓor VB,ℓ

<!-- Page 7 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

**Table 2.** Utility on GLUE8 and Math-10K (higher is better). “Non-DP” uses the same setup without DP clipping/noise; ε ∈{6, 3}

uses DP-SGD with δ = 10−5. Avg is the unweighted mean over the 12 tasks; bold is best per column. Takeaway: Under DP, PRISM attains the best Avg and wins most tasks, especially on multi-step reasoning (GSM8K/MAWPS/SVAMP).

SETTING METHOD GLUE8 MATH-10K AVG

COLA SST-2 MRPC STS-B QQP MNLI QNLI RTE GSM8K AQUA MAWPS SVAMP

NON-DP

FFA 0.456 0.935 0.759 0.821 0.713 0.736 0.809 0.809 0.513 0.476 0.836 0.678 0.712 RITE 0.515 0.947 0.883 0.873 0.821 0.846 0.889 0.895 0.595 0.488 0.899 0.736 0.782 ADAMW 0.504 0.954 0.831 0.863 0.766 0.813 0.846 0.848 0.561 0.476 0.870 0.698 0.752 LORA+ 0.578 0.950 0.840 0.862 0.807 0.845 0.851 0.838 0.592 0.465 0.891 0.712 0.769 LAMB 0.468 0.939 0.860 0.872 0.776 0.842 0.868 0.856 0.559 0.449 0.878 0.708 0.756 PRISM 0.392 0.921 0.857 0.822 0.797 0.814 0.834 0.798 0.552 0.472 0.895 0.693 0.737 ϵ = 6

FFA 0.355 0.907 0.738 0.465 0.479 0.579 0.684 0.755 0.375 0.390 0.735 0.611 0.589 RITE 0.235 0.787 0.635 0.268 0.500 0.482 0.562 0.657 0.282 0.366 0.597 0.503 0.490 ADAMW 0.407 0.915 0.770 0.659 0.493 0.651 0.716 0.798 0.441 0.465 0.761 0.615 0.641 LORA+ 0.436 0.897 0.787 0.691 0.739 0.721 0.747 0.823 0.446 0.409 0.786 0.611 0.674 LAMB 0.414 0.920 0.756 0.544 0.521 0.602 0.709 0.776 0.425 0.437 0.761 0.592 0.621 PRISM 0.444 0.919 0.798 0.718 0.770 0.707 0.776 0.791 0.469 0.445 0.819 0.626 0.690 ϵ = 3

FFA 0.337 0.890 0.730 0.406 0.466 0.561 0.662 0.740 0.350 0.374 0.718 0.598 0.569 RITE 0.221 0.713 0.636 0.260 0.485 0.463 0.548 0.606 0.255 0.362 0.525 0.474 0.462 ADAMW 0.410 0.903 0.778 0.622 0.555 0.633 0.718 0.812 0.446 0.413 0.731 0.591 0.634 LORA+ 0.434 0.906 0.798 0.668 0.730 0.708 0.740 0.812 0.419 0.386 0.765 0.609 0.665 LAMB 0.396 0.909 0.759 0.517 0.486 0.586 0.708 0.783 0.393 0.425 0.744 0.608 0.609 PRISM 0.406 0.884 0.784 0.729 0.770 0.732 0.791 0.780 0.456 0.406 0.807 0.614 0.680 has small or ill-conditioned eigenvalues. To mitigate this, PRISM introduces DP-aware floors λA,ℓ, λB,ℓ, scaled according to the known DP noise level σC b

2 and the geometry of the current LoRA module. For isotropic tangent noise, the rank-space noise covariances satisfy E[Ξ⊤

A,ℓΞA,ℓ/mℓ] = mℓ−r mℓN −1 ℓ and E[Ξ⊤

B,ℓΞB,ℓ/nℓ] = M −1 ℓ (Appendix A.26). Small eigenvalues of Mℓor Nℓtherefore simultaneously increase DP noise seen by the preconditioner and degrade numerical stability. Motivated by this, we set λA,ℓ≍ σC b

2 tr(N −1 ℓ) r, λB,ℓ≍ σC b

2 tr(M −1 ℓ) r. (26)

These operations yield a uniform bound on DP noise amplification under the adaptive post-processing.

Theorem 3.5 (Bounding DP noise amplification under adaptive preconditioning). Let V ⪰0 and λ > 0, and define P = V + λI. Then ∥P−1/2∥2 ≤λ−1/2 and for any matrix X,

∥XP−1/2∥2

F ≤λ−1∥X∥2

F. (27)

Theorem 3.5 formalizes Issue III (Eq. (10)): DP-noise amplification under inverse-square-root right-preconditioning is governed by the preconditioner’s spectral gain g(P) ≜

∥P−1/2∥2 = 1/ q λ+ min(P). A floor P = V + λI forces g(P) ≤1/

√ λ, hence the Frobenius energy of any perturbation can increase by at most 1/λ.

In PRISM, Eq. (17) injects DP noise into (∆Adp ℓ, ∆Bdp ℓ), and Eq. (25) post-processes it by (VA,ℓ+ λA,ℓI)−1/2 and

(VB,ℓ+ λB,ℓI)−1/2. The DP-aware floors in Eq. (26) keep λA,ℓ, λB,ℓfrom collapsing when VA,ℓ, VB,ℓ(or Mℓ, Nℓ) are ill-conditioned, so Eq. (27) yields controlled DP-noise amplification (bounded by 1/λA,ℓand 1/λB,ℓ), and intrinsic clipping caps the final step size (Appendix A.27).

## 4. Experiments

We benchmark PRISM for private LoRA fine-tuning on two multi-task instruction suites: GLUE8 (NLU) and Math- 10K (multi-step numerical reasoning), spanning diverse linguistic phenomena and compositional reasoning tasks to assess robustness across settings.

Setup. We fine-tune the Gemma-3-4B-pt backbone (Gemma Team et al., 2025) with LoRA (Hu et al., 2022). Our implementation follows LLM-Adapters (Hu et al., 2023; AGI-Edgerunners, 2023): Math-10K is used in its original form, while GLUE8 is constructed from GLUE (Wang et al., 2018) in the same instruction-format interface. We report both non-private results and (ε, δ)-DP results using DP- SGD (Abadi et al., 2016) with ε ∈{3, 6} and δ = 10−5. We use Opacus (Yousefpour et al., 2022; Opacus Contributors, 2026) with the default PRV accountant (Gopi et al., 2021). Full details are provided in Appendix B.1.

Datasets and metrics. GLUE8 consists of eight GLUE tasks (excluding WNLI) (Wang et al., 2018). We evaluate on the official validation splits using standard GLUE metrics. Math-10K combines GSM8K (Cobbe et al., 2021), AQuA (Ling et al., 2017), MAWPS (Koncel-Kedziorski

<!-- Page 8 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

**Table 3.** Math-10K results on Gemma-3-4B-pt, Gemma-2-9B, and Gemma-3-12B-pt under DP (r = 16, ε = 6, δ = 10−5). The “Type” column indicates the backbone family; all experiments use text-only inputs. Bold indicates the best result within each backbone.

Backbone Type Method GSM8K AQuA MAWPS SVAMP Avg

Gemma-3-4B-pt Multimodal AdamW 0.441 0.465 0.761 0.615 0.571 LoRA+ 0.446 0.409 0.786 0.611 0.563 PRISM 0.469 0.445 0.819 0.626 0.590

Gemma-2-9B Text-only AdamW 0.6473 0.4979 0.8093 0.7570 0.6779 LoRA+ 0.6293 0.4409 0.8067 0.6970 0.6435 PRISM 0.6603 0.5197 0.8487 0.7790 0.7019

Gemma-3-12B-pt Multimodal AdamW 0.5807 0.4764 0.7311 0.6870 0.6188 LoRA+ 0.6346 0.5039 0.8193 0.7460 0.6760 PRISM 0.6535 0.5315 0.8193 0.7820 0.6966 et al., 2016), and SVAMP (Patel et al., 2021) via LLM- Adapters (Hu et al., 2023). Performance is measured by exact answer accuracy using the LLM-Adapters protocol.

Baselines. We compare PRISM against FFA (Sun et al., 2024), LoRA-RITE (Yen et al., 2025), AdamW (Kingma & Ba, 2015; Loshchilov & Hutter, 2019), LoRA+ (Hayou et al., 2024), and LAMB (You et al., 2020).

Main Results and Interpretation. Table 2 reports utility under non-private training and DP training with ε ∈{6, 3}. Without DP, LoRA-RITE achieves the best average performance, which is expected since PRISM is designed to address DP-specific issues rather than to improve non-private optimization. Under DP, PRISM achieves the best average performance at both privacy budgets (0.690 at ε = 6; 0.680 at ε = 3) and wins the majority of tasks (8/12 and 7/12, respectively). PRISM is not best on every task (e.g., SST-2, RTE, and AQuA). This is expected because GLUE8 and Math-10K are trained as task suites with shared hyperparameters, while individual tasks have different convergence rates and sensitivities to DP noise.

The mechanism-level distinction is where the DP perturbation is applied. Factor-space DP perturbs the factors (A, B); after multiplication, the effective perturbation on Z = AB⊤ is scaled by the current factor norms and therefore depends on the chosen gauge. Thus, under the same nominal privacy budget, factor-space DP can induce uneven intrinsic noise across layers and tasks, causing some components to be over-noised. PRISM instead clips and noises the gaugeinvariant tangent update of Z, so the induced intrinsic noise is bounded and independent of the factorization. This makes the private updates more stable across heterogeneous task suites and improves the average DP utility, even when another optimizer is best on a few individual tasks.

Additional Scaling and Overhead Results. To assess robustness beyond the main setting, we further evaluate PRISM on larger backbones, across varying LoRA ranks, and with explicit runtime and memory profiling. For the backbone type, Gemma-2-9B is a text- only language model (Gemma Team et al., 2024), while Gemma-3-4B-pt and Gemma-3-12B-pt belong to the multimodal Gemma 3 family (Gemma Team et al., 2025); all benchmark inputs in our experiments are text-only.

**Table 3.** shows that PRISM’s advantage persists on both Gemma-2-9B and Gemma-3-12B-pt. Table 4 shows that PRISM remains consistently the best method across ranks r ∈{8, 16, 32} on Gemma-3-4B-pt. Finally, Table 5 shows that PRISM’s overhead is primarily in runtime rather than memory usage, consistent with its additional geometry-aware computations.

**Table 4.** Rank sensitivity on Gemma-3-4B-pt under DP (ε = 6,

δ = 10−5; text-only inputs). Avg is the unweighted mean over all 12 tasks. PRISM is best across all tested ranks.

Rank Method GLUE8 Avg Math Avg Avg r = 8 AdamW 0.659 0.522 0.614 LoRA+ 0.704 0.543 0.650 PRISM 0.744 0.565 0.684 r = 16 AdamW 0.676 0.571 0.641 LoRA+ 0.730 0.563 0.674 PRISM 0.740 0.590 0.690 r = 32 AdamW 0.682 0.542 0.636 LoRA+ 0.721 0.516 0.653 PRISM 0.740 0.566 0.682

**Table 5.** Runtime and memory profiling on Gemma-3-4B-pt for

Math-10K (r = 16, ε = 6). Measurements use a single A100- 40GB GPU with 10 warmup updates and 30 measured updates. PRISM roughly doubles step time in the current implementation, while peak memory is essentially unchanged.

## Method

Step time (s) Peak memory (MB)

LoRA+ 9.32 20961.1 AdamW 9.37 20961.1 PRISM 18.64 20964.3

Mechanism Diagnostics (Three Issues). We next analyze how DP clipping and noise injection propagate to the intrinsic update Z during Math-10K training (300 steps), and

<!-- Page 9 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA relate these effects to the three issues identified earlier. Figure 1 illustrates systematic amplification of intrinsic noise in factor-space DP compared to PRISM.

Issue I: gauge sensitivity. We perform DP training from gauge-rescaled initializations (A, B) 7→(cA, c−1B) with c ∈{0.25, 0.5, 1, 2, 4}. Figure 2 shows that factor-space DP remains sensitive to this benign reparameterization (Eq. (4)), whereas PRISM quickly reduces this variability to near zero after warm-up (Appendix C.1).

0 50 100 150 200 250 300 Update step

1.25

1.50

1.75

2.00

2.25

Amplification

Amplification (raw) Amplification MA (w=25)

**Figure 1.** Intrinsic DP-noise amplification during training (Math-10K). We plot the per-step ratio ∥NZ∥fac

F /∥NZ∥PRISM

F, where ∥NZ∥F is the Frobenius norm of the effective DP noise on the merged LoRA update Z. The blue curve reports the raw per-step ratio, and the orange curve reports its moving average (MA) with window size w = 25 updates. Values > 1 indicate that applying DP-SGD in factor space (A, B) injects a larger intrinsic perturbation into Z than PRISM under the same privacy budget.

0 50 100 150 200 250 300 Update step

10−1

100

Range(‖ΔZ‖F)

Baseline PRISM

**Figure 2.** Gauge sensitivity under DP (Math-10K). At step t we compute ρt = maxc ∥∆Zt∥F −minc ∥∆Zt∥F across gaugerescaled runs; smaller is better and ρt ≈0 indicates practical gauge invariance. PRISM drives ρt near zero, whereas factorspace DP exhibits persistently large ρt.

Issue II: gauge-dependent intrinsic noise. Proposition 2.2 predicts E∥NZ∥2

F = τ 2St for factor-space DP, where St = P ℓ(mℓ∥Bℓ∥2

F +nℓ∥Aℓ∥2

F) varies under gauge rescaling. Figure 3 confirms this linear scaling behavior for the baseline, while PRISM remains substantially lower and nearly invariant to St (Eq. (21)). Appendix C.2 further fixes Z and varies c to reproduce Corollary 2.3.

Issue III: DP under adaptive preconditioning. Figure 4 sweeps the DP noise multiplier σ and measures the resulting

5.500 5.525 5.550 5.575 5.600 5.625 5.650 5.675 5.700 St = ∑(m‖B‖2

F + n‖A‖2

F) 1e7

Measured ‖NZ‖2

F

Baseline (measured)

Baseline fit: R2=0.999

PRISM (measured)

**Figure 3.** Gauge-dependent intrinsic DP noise (Math-10K). We

plot the measured intrinsic noise energy ∥NZ∥2

F against the gaugedependent statistic St. A strong linear trend indicates that the amount of DP noise injected into Z depends on the factorization; PRISM largely removes this dependence and keeps ∥NZ∥2

F low.

preconditioned intrinsic noise magnitude (Eq. (10)). Factorspace DP-AdamW exhibits a “noise-normalization” effect (Proposition A.29), whereas PRISM with DP-aware floors (Eq. (26)) consistently reduces the perturbation across all σ, which aligns with Theorem 3.5 (Appendix C.3).

0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 Noise multiplier (σ)

Measured (μ ± σseed)

Baseline PRISM

**Figure 4.** Preconditioned intrinsic DP noise vs. σ (Math-10K). We report E∥P−1/2

t ξintr∥F; lower means the optimizer applies less stochastic perturbation after preconditioning. Factor-space DP becomes nearly σ-invariant, while PRISM keeps the preconditioned noise smaller via DP-aware floors.

Limitations. PRISM is tailored to LoRA-style fixed-rank updates; extending it to other PEFT methods requires deriving the corresponding intrinsic geometry. Its main practical cost is runtime overhead from geometry-aware operations, while peak memory remains nearly unchanged.

## Acknowledgements

This work was funded in part by the National Science Foundation under award number IIS2202699, IIS-2416895, IIS- 2301599, CMMI2301601, and DMS-2529302.

Impact Statement

This work develops a differentially private method for LoRA fine-tuning. We expect it to reduce privacy risks when adapt-

<!-- Page 10 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA ing models on sensitive data; we do not foresee additional negative societal impacts beyond those typical of deploying ML systems.

## References

Abadi, M., Chu, A., Goodfellow, I., McMahan, H. B.,

Mironov, I., Talwar, K., and Zhang, L. Deep learning with differential privacy. In Proceedings of the 2016 ACM SIGSAC conference on computer and communications security, pp. 308–318, 2016.

AGI-Edgerunners. LLM-Adapters: Official implementation.

https://github.com/AGI-Edgerunners/ LLM-Adapters, 2023.

Ben Zaken, E., Goldberg, Y., and Ravfogel, S. BitFit: Simple parameter-efficient fine-tuning for transformerbased masked language-models. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pp. 1–9. Association for Computational Linguistics, 2022. doi: 10.18653/v1/2022.acl-short.1. URL https:// aclanthology.org/2022.acl-short.1/.

Bourtoule, L., Chandrasekaran, V., Choquette-Choo, C. A.,

Jia, H., Travers, A., Zhang, B., Lie, D., and Papernot, N. Machine unlearning. In 2021 IEEE Symposium on Security and Privacy (SP), pp. 141–159, 2021. doi: 10. 1109/SP40001.2021.00019.

Carlini, N., Liu, C., Erlingsson, ´U., Kos, J., and Song, D. The secret sharer: Evaluating and testing unintended memorization in neural networks. In 28th USENIX Security Symposium (USENIX Security 19), pp. 267–284. USENIX Association, 2019. URL https://www.usenix.org/conference/ usenixsecurity19/presentation/carlini.

Carlini, N., Tram`er, F., Wallace, E., Jagielski, M.,

Herbert-Voss, A., Lee, K., Roberts, A., Brown, T., Song, D., Erlingsson, ´U., Oprea, A., and Raffel, C. Extracting training data from large language models. In 30th USENIX Security Symposium (USENIX Security 21), pp. 2633–2650. USENIX As- sociation, 2021. URL https://www.usenix. org/conference/usenixsecurity21/ presentation/carlini-extracting.

Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,

Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., and Schulman, J. Training verifiers to solve math word problems, 2021. URL https://arxiv. org/abs/2110.14168.

Dettmers, T., Pagnoni, A., Holtzman, A., and Zettlemoyer,

L. QLoRA: Efficient finetuning of quantized LLMs. In

Thirty-seventh Conference on Neural Information Pro- cessing Systems, 2023. URL https://openreview. net/forum?id=OUIFPHEgJU.

Dwork, C. and Roth, A. The algorithmic foundations of differential privacy. Foundations and Trends in Theoretical Computer Science, 9(3–4):211–407, 2014. doi: 10.1561/0400000042. URL https://doi.org/10. 1561/0400000042.

Dwork, C., McSherry, F., Nissim, K., and Smith, A. Calibrat- ing noise to sensitivity in private data analysis. In Theory of cryptography conference, pp. 265–284. Springer, 2006.

Eckart, C. and Young, G. The approximation of one matrix by another of lower rank. Psychometrika, 1(3):211–218, 1936. doi: 10.1007/BF02288367. URL https://doi. org/10.1007/BF02288367.

Edelman, A., Arias, T. A., and Smith, S. T. The geometry of algorithms with orthogonality constraints. SIAM Journal on Matrix Analysis and Applications, 20(2):303–353, 1998. doi: 10.1137/S0895479895290954. URL https: //doi.org/10.1137/S0895479895290954.

Fredrikson, M., Jha, S., and Ristenpart, T. Model inversion attacks that exploit confidence information and basic countermeasures. In Proceedings of the 22nd ACM SIGSAC Conference on Computer and Commu- nications Security, CCS ’15, pp. 1322–1333. Association for Computing Machinery, 2015. doi: 10.1145/ 2810103.2813677. URL https://doi.org/10. 1145/2810103.2813677.

Ganju, K., Wang, Q., Yang, W., Gunter, C. A., and Borisov,

N. Property inference attacks on fully connected neural networks using permutation invariant representations. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, CCS ’18, pp. 619–633. Association for Computing Machinery, 2018. doi: 10.1145/3243734.3243834. URL https://doi. org/10.1145/3243734.3243834.

Gemma Team, Riviere, M., Pathak, S., Sessa, P. G., Hardin,

C., Bhupatiraju, S., Hussenot, L., Mesnard, T., Shahriari, B., Ram´e, A., et al. Gemma 2: Improving open language models at a practical size. arXiv preprint arXiv:2408.00118, 2024. doi: 10.48550/arXiv.2408. 00118. URL https://arxiv.org/abs/2408. 00118.

Gemma Team, Kamath, A., Ferret, J., Pathak, S., Vieil- lard, N., Merhej, R., Perrin, S., Matejovicova, T., Ram´e, A., Rivi`ere, M., et al. Gemma 3 technical report. arXiv preprint arXiv:2503.19786, 2025. doi: 10.48550/arXiv.2503.19786. URL https://arxiv. org/abs/2503.19786.

<!-- Page 11 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Gopi, S., Lee, Y. T., and Wutschitz, L. Numerical composition of differential privacy. In Advances in Neural Information Processing Systems, volume 34, pp. 11631–11642. Curran Associates, Inc., 2021. URL https://proceedings.neurips. cc/paper_files/paper/2021/file/ 6097d8f3714205740f30debe1166744e-Paper. pdf.

Hayou, S., Ghosh, N., and Yu, B. LoRA+: Efficient low rank adaptation of large models. In Proceedings of the 41st International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research, pp. 17783–17806. PMLR, 2024. URL https://proceedings.mlr.press/ v235/hayou24a.html.

Houlsby, N., Giurgiu, A., Jastrzebski, S., Morrone, B.,

De Laroussilhe, Q., Gesmundo, A., Attariyan, M., and Gelly, S. Parameter-efficient transfer learning for NLP. In Proceedings of the 36th International Conference on Machine Learning, volume 97 of Proceedings of Machine Learning Research, pp. 2790–2799. PMLR, 2019. URL https://proceedings.mlr.press/v97/ houlsby19a.html.

Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,

S., Wang, L., and Chen, W. LoRA: Low-rank adaptation of large language models. In International Conference on Learning Representations, 2022. URL https:// openreview.net/forum?id=nZeVKeeFYf9.

Hu, Z., Wang, L., Lan, Y., Xu, W., Lim, E.-P., Bing, L., Xu,

X., Poria, S., and Lee, R. LLM-Adapters: An adapter family for parameter-efficient fine-tuning of large language models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 5254–5276, Singapore, 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main. 319. URL https://aclanthology.org/2023. emnlp-main.319/.

Kingma, D. P. and Ba, J. Adam: A method for stochastic optimization. In International Conference on Learning Representations (ICLR), 2015. URL https://arxiv. org/abs/1412.6980.

Koncel-Kedziorski, R., Roy, S., Amini, A., Kushman, N., and Hajishirzi, H. MAWPS: A math word problem repository. In Knight, K., Nenkova, A., and Rambow, O. (eds.), Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 1152–1157, San Diego, California, June 2016. Association for Computational Linguistics. doi: 10.18653/v1/N16-1136. URL https://aclanthology.org/N16-1136/.

Lester, B., Al-Rfou, R., and Constant, N. The power of scale for parameter-efficient prompt tuning. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pp. 3045–3059. Association for Computational Linguistics, 2021. doi: 10.18653/v1/2021. emnlp-main.243. URL https://aclanthology. org/2021.emnlp-main.243/.

Li, T., Zaheer, M., Reddi, S., and Smith, V. Private adaptive optimization with side information. In Proceedings of the 39th International Conference on Machine Learning, volume 162 of Proceedings of Machine Learning Research, pp. 13086–13105. PMLR, 2022. URL https:// proceedings.mlr.press/v162/li22x.html.

Li, T., Zaheer, M., Liu, K., Reddi, S. J., McMahan, H. B., and Smith, V. Differentially private adaptive optimization with delayed preconditioners. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum? id=j1zQGmQQOX1.

Li, X. L. and Liang, P. Prefix-Tuning: Optimizing con- tinuous prompts for generation. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pp. 4582–4597. Association for Computational Linguistics, 2021. doi: 10.18653/v1/2021.acl-long. 353. URL https://aclanthology.org/2021. acl-long.353/.

Li, Y., Yu, Y., Liang, C., Karampatziakis, N., He, P.,

Chen, W., and Zhao, T. LoftQ: LoRA-fine-tuning-aware quantization for large language models. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum? id=LzPWWPAdY4.

Ling, W., Yogatama, D., Dyer, C., and Blunsom, P. Pro- gram induction by rationale generation: Learning to solve and explain algebraic word problems. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 158–167. Association for Computational Linguistics, 2017. doi: 10.18653/v1/P17-1015. URL https://aclanthology.org/P17-1015/.

Liu, H., Tam, D., Muqeeth, M., Mohta, J., Huang, T., Bansal,

M., and Raffel, C. Few-shot parameter-efficient finetuning is better and cheaper than in-context learning. In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), Advances in Neural Information Processing Systems, volume 35, pp. 1950–1965. Curran Associates, Inc., 2022.

<!-- Page 12 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Liu, X.-Y., Zhu, R., Zha, D., Gao, J., Zhong, S., White, M., and Qiu, M. Differentially private low-rank adaptation of large language model using federated learning. ACM Transactions on Management Information Systems, 16 (2), 2025. doi: 10.1145/3682068. URL https://doi. org/10.1145/3682068.

Loshchilov, I. and Hutter, F. Decoupled weight decay reg- ularization. In International Conference on Learning Representations, 2019. URL https://openreview. net/forum?id=Bkg6RiCqY7.

Mirsky, L. Symmetric gauge functions and unitarily in- variant norms. The Quarterly Journal of Mathematics, 11(1):50–59, 1960. doi: 10.1093/qmath/11.1.50. URL https://doi.org/10.1093/qmath/11.1.50.

Mishra, B., Meyer, G., Bonnabel, S., and Sepulchre, R.

Fixed-rank matrix factorizations and Riemannian lowrank optimization. Computational Statistics, 29:591–621, 2014. doi: 10.1007/s00180-013-0464-z. URL https: //doi.org/10.1007/s00180-013-0464-z.

Opacus Contributors. Opacus PrivacyEngine API reference. https://opacus.ai/api/privacy_ engine.html, 2026.

Patel, A., Bhattamishra, S., and Goyal, N. Are NLP models really able to solve simple math word problems? In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 2080–2094, Online, 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.naacl-main. 168. URL https://aclanthology.org/2021. naacl-main.168/.

Shokri, R., Stronati, M., Song, C., and Shmatikov, V. Mem- bership inference attacks against machine learning models. In 2017 IEEE Symposium on Security and Privacy (SP), pp. 3–18. IEEE Computer Society, 2017. doi: 10.1109/SP.2017.41. URL https://doi.org/10. 1109/SP.2017.41.

Sun, Y., Li, Z., Li, Y., and Ding, B. Improving LoRA in privacy-preserving federated learning. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum? id=NLPzL6HWNl.

Tang, Q., Shpilevskiy, F., and L´ecuyer, M. DP- AdamBC: Your DP-Adam is actually DP-SGD (unless you apply bias correction). Proceedings of the AAAI Conference on Artificial Intelligence, 38 (14):15276–15283, 2024. doi: 10.1609/aaai.v38i14. 29451. URL https://ojs.aaai.org/index. php/AAAI/article/view/29451.

Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., and

Bowman, S. R. GLUE: A multi-task benchmark and analysis platform for natural language understanding. In Proceedings of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP, pp. 353–355, Brussels, Belgium, 2018. Association for Computational Linguistics. doi: 10.18653/v1/ W18-5446. URL https://aclanthology.org/ W18-5446/.

Xu, H., Shrestha, S., Chen, W., Li, Z., and Cai, Z. DP-

FedLoRA: Privacy-enhanced federated fine-tuning for on-device large language models. In 2025 IEEE International Conference on Data Mining (ICDM), pp. 813– 822. IEEE, 2025. doi: 10.1109/ICDM65498.2025.00089. URL https://doi.org/10.1109/ICDM65498. 2025.00089.

Yen, J.-N., Si, S., Meng, Z., Yu, F., Duvvuri, S. S., Dhillon,

I. S., Hsieh, C.-J., and Kumar, S. LoRA Done RITE: Robust invariant transformation equilibration for LoRA optimization. In The Thirteenth International Conference on Learning Representations, 2025. URL https:// openreview.net/forum?id=VpWki1v2P8.

You, Y., Li, J., Reddi, S., Hseu, J., Kumar, S., Bho- janapalli, S., Song, X., Demmel, J., Keutzer, K., and Hsieh, C.-J. Large batch optimization for deep learning: Training BERT in 76 minutes. In International Conference on Learning Representations, 2020. URL https: //openreview.net/forum?id=Syx4wnEtvH.

Yousefpour, A., Shilov, I., Sablayrolles, A., Testuggine, D.,

Prasad, K., Malek, M., Nguyen, J., Ghosh, S., Bharadwaj, A., Zhao, J., Cormode, G., and Mironov, I. Opacus: Userfriendly differential privacy library in PyTorch, 2022. URL https://arxiv.org/abs/2109.12298.

Yu, D., Naik, S., Backurs, A., Gopi, S., Inan, H. A., Kamath,

G., Kulkarni, J., Lee, Y. T., Manoel, A., Wutschitz, L., Yekhanin, S., and Zhang, H. Differentially private fine- tuning of language models. In International Conference on Learning Representations, 2022. URL https:// openreview.net/forum?id=Q42f0dfjECO.

<!-- Page 13 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

## Appendix

Roadmap

## Appendix

A: Theory and proofs. A1 Quotient geometry / gauge quotient................................................................................p. 13 A2 General gauge amplification...................................................................................... p. 14 A3 Second-order term concentration.................................................................................. p. 14 A4 Naive factor-space DP amplification............................................................................... p. 15 A5 Effective noise range under rescaling.............................................................................. p. 16 A6 Tangent space projector properties.................................................................................p. 16 A7 Gauge freedom in tangent lifts.................................................................................... p. 17 A8 Projector gauge invariance........................................................................................p. 18 A9 Canonical factor lift construction.................................................................................. p. 18 A10 Tangent update Frobenius norm................................................................................... p. 19 A11 Rank-1 specialization............................................................................................ p. 19 A12 Factorized tangent noise equivalence.............................................................................. p. 19 A13 Low-dimensional noise sampler................................................................................... p. 20 A14 Stable projector / basis computation............................................................................... p. 20 A15 Noise-sampler gauge invariance...................................................................................p. 20 A16 Proof of Thm. 3.1................................................................................................p. 21 A17 Isotropy of projected Gaussian.................................................................................... p. 21 A18 Covariance and intrinsic dimension................................................................................p. 22 A19 Noise concentration bounds...................................................................................... p. 22 A20 Retraction / rank-r approximation................................................................................. p. 22 A21 No bilinear DP term in PRISM....................................................................................p. 23 A22 Proof of Thm. 3.3................................................................................................p. 23 A23 Gaussian mechanism on subspace................................................................................. p. 23 A24 Procrustes alignment as gauge.................................................................................... p. 23 A25 DP guarantee details............................................................................................. p. 24 A26 Rank-space noise moments....................................................................................... p. 24 A27 Adaptive preconditioning analysis.................................................................................p. 24

## Appendix

B: Experimental setup. B1 Datasets, hyperparameters, and compute........................................................................... p. 25

## Appendix

C: Additional diagnostics and analysis. C1 Issue I: gauge sensitivity diagnostics.............................................................................. p. 26 C2 Issue II: gauge sweep at fixed Z...................................................................................p. 29 C3 Issue III: preconditioning/noise amplification diagnostics............................................................ p. 31

A. Theory and Proofs

This appendix provides proofs and additional derivations. We use ⟨X, Y ⟩= tr(X⊤Y), ∥· ∥F for the Frobenius norm, vec(·) for vectorization, and ⊗for the Kronecker product. For a symmetric positive semidefinite matrix X, X† denotes the Moore–Penrose pseudoinverse.

A.1. Quotient geometry: rank-r matrices as a gauge quotient

The non-identifiability (Aℓ, Bℓ) ∼(AℓR, BℓR−⊤) can be formalized as a smooth group action. Let ˜ M ≜Rm×r

∗ × Rn×r

∗ be the total space of full-column-rank factors and let GL(r) act on ˜ M by

(Aℓ, Bℓ) · R = (AℓR, BℓR−⊤), R ∈GL(r). (28)

The map π: ˜ M →Mr given by π(Aℓ, Bℓ) = AℓB⊤ ℓis constant along orbits of this action. Under mild regularity conditions, the rank-r manifold is the quotient Mr ∼= ˜ M/GL(r), and intrinsic quantities on Zℓare precisely those that are invariant under (28).

Vertical and horizontal spaces. Differentiating the action (28) at the identity R = Ir yields the vertical space (tangent to the gauge orbit) at (Aℓ, Bℓ):

V(Aℓ,Bℓ) = {(AℓΩ, −BℓΩ⊤): Ω∈Rr×r}. (29)

<!-- Page 14 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

A complementary horizontal space H(Aℓ,Bℓ) selects one representative lift of each intrinsic tangent direction. With the Frobenius metric on ˜ M, the orthogonal complement of (29) is characterized by

H(Aℓ,Bℓ) = n

(∆Aℓ, ∆Bℓ): A⊤ ℓ∆Aℓ= (B⊤ ℓ∆Bℓ)⊤o

, (30)

This is exactly the gauge-fixing constraint enforced by our canonical lift (14).

Lemma A.1 (Orthogonality to the gauge orbit). A pair (∆Aℓ, ∆Bℓ) satisfies (30) if and only if it is orthogonal to every vertical direction under the Frobenius inner product on ˜ M:

⟨(∆Aℓ, ∆Bℓ), (AℓΩ, −BℓΩ⊤)⟩= tr(∆A⊤ ℓAℓΩ) −tr(∆B⊤ ℓBℓΩ⊤) = 0, ∀Ω.

Proof. The stated inner product equals tr(ΩA⊤ ℓ∆Aℓ) −tr(Ω(B⊤ ℓ∆Bℓ)⊤) = tr(Ω(A⊤ ℓ∆Aℓ−(B⊤ ℓ∆Bℓ)⊤)). Since this vanishes for all Ωif and only if A⊤ ℓ∆Aℓ= (B⊤ ℓ∆Bℓ)⊤, we obtain (30).

Why this matters for DP. Clipping and adding noise in factor coordinates implicitly chooses a metric on ˜ M, not on the quotient Mr. As a result, the induced intrinsic perturbation can depend on the chosen representative (i.e., the gauge), which is the source of the amplification phenomena in Section 2. PRISM instead clips and perturbs horizontal (gauge-orthogonal) directions and interprets the Gaussian mechanism intrinsically in the quotient geometry. This is why the effective intrinsic noise EZℓis a fixed, controllable scalar in PRISM (Corollary A.2).

Corollary A.2 (Effective intrinsic DP noise of PRISM). Let N PRISM

Zℓ = σC b PAℓ,Bℓ(Ξℓ) with Ξℓ∼N(0, Im×n). Then EZℓ= σC b p r(m + n −r), independent of the factor gauge.

Proposition A.3 (Orthogonal tangent projection). For Zℓ= AℓB⊤ ℓ ∈Mr, the linear map PAℓ,Bℓin Eq. (13) is the orthogonal projector onto TZℓMr: for all G ∈Rm×n, PAℓ,Bℓ(G) ∈TZℓMr and G −PAℓ,Bℓ(G) ∈(TZℓMr)⊥. Equivalently, PAℓ,Bℓis symmetric and idempotent.

Proof of Proposition A.3. By Lemma A.9, any G ∈Rm×n decomposes orthogonally as

G = (G −Π⊥

AℓGΠ⊥

Bℓ) | {z } ∈TZℓMr

+ Π⊥

AℓGΠ⊥

Bℓ | {z } ∈(TZℓMr)⊥

.

Therefore the orthogonal projector onto TZℓMr is PAℓ,Bℓ(G) = G −Π⊥

AℓGΠ⊥

Bℓ= ΠAℓG + GΠBℓ−ΠAℓGΠBℓ.

A.2. General gauge amplification for arbitrary basis changes

Corollary 2.3 considered the scalar rescaling gauge (Aℓ, Bℓ) 7→(cAℓ, c−1Bℓ). Here we record the corresponding expression for a general invertible basis change.

Proposition A.4 (Gauge-dependent noise energy under general R). Let (A′ ℓ, B′ ℓ) = (AℓR, BℓR−⊤) for invertible R ∈ GL(r) and let ξA,ℓ, ξB,ℓbe i.i.d. Gaussian as in Proposition 2.2. Then

E

∥ξA,ℓB′ ℓ

⊤∥2

F

= mτ 2∥BℓR−⊤∥2

F, E

∥A′ ℓξ⊤

B,ℓ∥2

F

= nτ 2∥AℓR∥2

F.

Consequently, for any nonzero Zℓ= AℓB⊤ ℓ, there exist gauge matrices R with arbitrarily large condition number such that the first-order noise energy on Zℓbecomes arbitrarily large, even though Zℓis unchanged.

Proof. The expressions follow by the same calculation as Proposition 2.2, with Bℓreplaced by BℓR−⊤and Aℓreplaced by AℓR. For the final statement, take an R that scales one singular direction of Aℓ(and inversely scales the corresponding direction of Bℓ) by a large factor; the scalar rescaling case is recovered by R = cI.

A.3. Second-order term magnitude and concentration

Proposition 2.2 quantifies the expected Frobenius energy of the bilinear term N (2)

Zℓ= ξA,ℓξ⊤

B,ℓ. Here we record a simple high-probability bound that complements (9) and illustrates why the bilinear term can dominate when the learning rate is not extremely small.

<!-- Page 15 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Lemma A.5 (High-probability bound for the bilinear term). Let ξA,ℓ∈Rm×r and ξB,ℓ∈Rn×r have i.i.d. N(0, τ 2) entries. Then for any δ ∈(0, 1), with probability at least 1 −2δ,

∥ξA,ℓξ⊤

B,ℓ∥F ≤τ 2 r mr + 2 p mr log(1/δ) + 2 log(1/δ)

nr + 2 p nr log(1/δ) + 2 log(1/δ)

. (31)

In particular, the typical scale is ∥ξA,ℓξ⊤

B,ℓ∥F = Θ(τ 2 r√mn) up to logarithmic factors.

Proof. Use ∥XY ⊤∥F ≤∥X∥F ∥Y ∥F. Since ∥ξA,ℓ∥2

F /τ 2 ∼χ2 mr and ∥ξB,ℓ∥2

F /τ 2 ∼χ2 nr, applying the chi-square tail bound used in Proposition A.24 to each and taking a union bound yields (31).

Implication for DP-LoRA. When both factors are randomized, the intrinsic parameter update contains the extra term η2ξA,ℓξ⊤

B,ℓ(Eq. (7)). Lemma A.5 implies this term has magnitude on the order of η2τ 2r√mn, which is not controlled by the intrinsic clipping threshold on the first-order tangent update. PRISM avoids this term altogether (Lemma A.26).

A.4. Noise amplification under naive factor-space DP

Proof of Proposition 2.2. Consider the first-order intrinsic perturbation N (1)

Zℓ= ξA,ℓB⊤ ℓ+Aℓξ⊤

B,ℓ. Expanding the Frobenius norm,

∥N (1)

Zℓ∥2

F = ∥ξA,ℓB⊤ ℓ∥2

F + ∥Aℓξ⊤

B,ℓ∥2

F + 2⟨ξA,ℓB⊤ ℓ, Aℓξ⊤

B,ℓ⟩.

The cross term has zero expectation because ξA,ℓand ξB,ℓare independent and centered:

E⟨ξA,ℓB⊤ ℓ, Aℓξ⊤

B,ℓ⟩= Etr

(ξA,ℓB⊤ ℓ)⊤(Aℓξ⊤

B,ℓ)

= Etr(Bℓξ⊤

A,ℓAℓξ⊤

B,ℓ) = EξA,ℓtr

Bℓξ⊤

A,ℓAℓEξB,ℓ[ξ⊤

B,ℓ]

= 0.

For the remaining terms,

E∥ξA,ℓB⊤ ℓ∥2

F = Etr(Bℓξ⊤

A,ℓξA,ℓB⊤ ℓ) = tr

BℓE[ξ⊤

A,ℓξA,ℓ] B⊤ ℓ

.

Since ξA,ℓhas i.i.d. N(0, τ 2) entries, E[ξ⊤

A,ℓξA,ℓ] = mτ 2 Ir, yielding mτ 2∥Bℓ∥2

F. Similarly,

E∥Aℓξ⊤

B,ℓ∥2

F = Etr(ξB,ℓA⊤ ℓAℓξ⊤

B,ℓ) = tr

A⊤ ℓAℓE[ξ⊤

B,ℓξB,ℓ]

= nτ 2∥Aℓ∥2

F, because E[ξ⊤

B,ℓξB,ℓ] = nτ 2 Ir. Summing proves (8).

For the bilinear term, each entry of ξA,ℓξ⊤

B,ℓis a sum of r independent products of mean-zero Gaussians; its variance is rτ 4. Summing variances over mn entries yields E∥ξA,ℓξ⊤

B,ℓ∥2

F = mnr τ 4, proving (9).

Proposition A.6 (One-sided factor noise). Let ξA,ℓ∈Rm×r and ξB,ℓ∈Rn×r have i.i.d. entries N(0, τ 2). For Zℓ= AℓB⊤ ℓ, consider the intrinsic perturbations obtained by noising only one factor: N (A)

Zℓ ≜ξA,ℓB⊤ ℓand N (B)

Zℓ ≜Aℓξ⊤

B,ℓ. Then

E∥N (A)

Zℓ∥2

F = τ 2 m∥Bℓ∥2

F, E∥N (B)

Zℓ∥2

F = τ 2 n∥Aℓ∥2

F. (32)

Proof of Proposition A.6. If Aℓis frozen and only Bℓis perturbed by ξB,ℓwith i.i.d. N(0, τ 2) entries, then the induced intrinsic perturbation is NZℓ= Aℓξ⊤

B,ℓ. Therefore

E∥NZℓ∥2

F = Etr(ξB,ℓA⊤ ℓAℓξ⊤

B,ℓ) = tr

A⊤ ℓAℓE[ξ⊤

B,ℓξB,ℓ]

= nτ 2∥Aℓ∥2

F, which is (32). If instead Bℓis frozen and only Aℓis perturbed, the same calculation gives E∥NZℓ∥2

F = mτ 2∥Bℓ∥2

F. In either case there is no bilinear term because only one factor is randomized.

<!-- Page 16 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

A.5. Range of effective intrinsic noise under scalar gauge rescaling

Corollary 2.3 shows that naive factor-space DP can make the effective intrinsic noise arbitrarily large under the scalar gauge (Aℓ, Bℓ) 7→(cAℓ, c−1Bℓ). For completeness, we record the entire range of the first-order effective noise over this one-parameter family.

Proposition A.7 (Range over scalar gauges). Let Zℓ= AℓB⊤ ℓ̸ = 0 and consider the scalar gauge family (Ac, Bc) = (cAℓ, c−1Bℓ) for c > 0. Let ξA,ℓ, ξB,ℓhave i.i.d. N(0, τ 2) entries as in Proposition 2.2, and define the first-order perturbation N (1)

Z,c ≜ξA,ℓB⊤ c + Acξ⊤

B,ℓ. Then

E

∥N (1)

Z,c∥2

F

= τ 2 m c2 ∥Bℓ∥2

F + nc2∥Aℓ∥2

F

. (33)

The minimizing gauge is c⋆= m∥Bℓ∥2

F n∥Aℓ∥2

F

1/4

, (34)

and the minimum value is min c>0 E

∥N (1)

Z,c∥2

F

= 2τ 2 √mn ∥Aℓ∥F ∥Bℓ∥F. (35)

Moreover, supc>0 E[∥N (1)

Z,c∥2

F ] = ∞.

Proof. Equation (33) follows directly from (8) after substituting Ac = cAℓand Bc = c−1Bℓ. The objective in c is strictly convex in log c and differentiating (33) yields −2m∥Bℓ∥2

F /c3 + 2nc∥Aℓ∥2

F = 0, giving (34). Substituting c⋆into (33) yields (35). The divergence as c →0 or c →∞gives the supremum.

Interpretation. Even if one tunes the gauge once to reduce EZℓ, the optimizer can still drift to a different implicit scaling of (Aℓ, Bℓ) over time. Therefore, under factor-space DP the effective intrinsic noise is not a fixed function of the intrinsic parameter Zℓand is not directly controlled by (σ, C, b) alone. PRISM removes this degree of freedom by defining the DP mechanism intrinsically on TZℓMr (Corollary A.2).

A.6. Tangent space orthogonal complement and orthogonal projection

Lemma A.8 (Tangent space characterization). Assume Aℓ∈Rm×r and Bℓ∈Rn×r have full column rank and Zℓ= AℓB⊤ ℓ. Then the tangent space of Mr at Zℓis

TZℓMr = {∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ: ∆Aℓ∈Rm×r, ∆Bℓ∈Rn×r}, (36)

which is Eq. (11) in the main text.

Proof. Consider the smooth factorization map ϕ: Rm×r

∗ ×Rn×r

∗ →Mr defined by ϕ(A, B) = AB⊤. For any perturbations (∆A, ∆B), the directional derivative at (Aℓ, Bℓ) is

Dϕ(Aℓ,Bℓ)[∆A, ∆B] = ∆A B⊤ ℓ+ Aℓ∆B⊤.

Thus every matrix of the form ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓarises as the derivative of the curve t 7→(Aℓ+ t∆Aℓ)(Bℓ+ t∆Bℓ)⊤at t = 0, and hence lies in TZℓMr.

Conversely, any tangent vector ∆Z ∈TZℓMr is the derivative of a smooth curve t 7→Z(t) ∈Mr with Z(0) = Zℓ. Because Aℓand Bℓare full column rank, rank-r matrices near Zℓadmit factorizations Z(t) = A(t)B(t)⊤with A(t), B(t) smooth in t. Differentiating at t = 0 yields ∆Z = ˙A(0)B⊤ ℓ+ Aℓ˙B(0)⊤, proving (36).

Lemma A.9 (Tangent space orthogonal complement). Let Zℓ= AℓB⊤ ℓwith ΠAℓ, ΠBℓas in (12). Then

(TZℓMr)⊥= {X ∈Rm×n: ΠAℓX = 0 and XΠBℓ= 0} = {Π⊥

AℓY Π⊥

Bℓ: Y ∈Rm×n}. (37)

<!-- Page 17 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Proof. Let X ∈(TZℓMr)⊥. For all ∆Aℓ, ∆Bℓ,

0 = ⟨X, ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ⟩= ⟨XBℓ, ∆Aℓ⟩+ ⟨X⊤Aℓ, ∆Bℓ⟩.

Hence XBℓ= 0 and X⊤Aℓ= 0. Since ΠBℓprojects onto col(Bℓ), XBℓ= 0 is equivalent to XΠBℓ= 0; similarly X⊤Aℓ= 0 is equivalent to ΠAℓX = 0. Conversely, if ΠAℓX = 0 and XΠBℓ= 0, the inner product above vanishes for all ∆Aℓ, ∆Bℓ. Finally, XΠBℓ= 0 implies X = XΠ⊥

Bℓand ΠAℓX = 0 implies X = Π⊥

AℓX, hence X = Π⊥

AℓY Π⊥

Bℓfor Y = X.

A.7. Gauge freedom in factor lifts and minimum-factor-norm representatives

The representation of an intrinsic tangent update ∆Zℓ∈TZℓMr in factor space is not unique. This non-uniqueness is the differential analogue of the gauge symmetry (Aℓ, Bℓ) ∼(AℓR, BℓR−⊤). We record the basic “lift gauge” degrees of freedom and a canonical choice based on minimum factor norm.

Lemma A.10 (Gauge degrees of freedom in factor lifts). Let Zℓ= AℓB⊤ ℓand fix an intrinsic tangent matrix ∆Zℓ∈TZℓMr. If (∆Aℓ, ∆Bℓ) is any pair satisfying ∆Zℓ= ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ, then for any Ω∈Rr×r,

(∆Aℓ, ∆Bℓ) 7→(∆Aℓ+ AℓΩ, ∆Bℓ−BℓΩ⊤) (38)

produces another valid lift of the same intrinsic update ∆Zℓ. In particular, the induced matrix ∆Zℓdepends only on the intrinsic point Zℓand not on the chosen factor lift.

Proof. For any Ω,

(∆Aℓ+ AℓΩ)B⊤ ℓ+ Aℓ(∆Bℓ−BℓΩ⊤)⊤= ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ+ AℓΩB⊤ ℓ−AℓΩB⊤ ℓ= ∆Zℓ.

Equation (38) shows that there are infinitely many factor pairs that realize the same intrinsic tangent update. This is the differential version of the gauge symmetry (28). Depending on the optimizer implementation, it can be useful to pick a canonical representative of this equivalence class. One natural choice is the minimum-factor-norm lift, which can be computed by solving a small Sylvester equation of size r × r.

Proposition A.11 (Minimum-norm representative in a gauge class). Assume Aℓand Bℓhave full column rank so that M = A⊤ ℓAℓ≻0 and N = B⊤ ℓBℓ≻0. Fix any lift (∆A0, ∆B0) that realizes a given ∆Zℓ. Consider the gauge family

∆Aℓ(Ω) = ∆A0 + AℓΩ, ∆Bℓ(Ω) = ∆B0 −BℓΩ⊤.

Then the unique minimizer of f(Ω) ≜∥∆Aℓ(Ω)∥2

F + ∥∆Bℓ(Ω)∥2

F is obtained by the unique solution Ω⋆to the Sylvester equation

MΩ+ ΩN = B⊤ ℓ∆B0 −A⊤ ℓ∆A0. (39)

The corresponding (∆Aℓ(Ω⋆), ∆Bℓ(Ω⋆)) is the minimum-factor-norm lift of ∆Zℓ.

Proof. Expand the quadratic objective:

f(Ω) = ∥∆A0 + AℓΩ∥2

F + ∥∆B0 −BℓΩ⊤∥2

F = ∥∆A0∥2

F + ∥∆B0∥2

F + 2 tr(Ω⊤A⊤ ℓ∆A0) −2 tr(Ω⊤∆B⊤

0 Bℓ)

+ tr(Ω⊤MΩ) + tr(ΩNΩ⊤), where we used ∥AℓΩ∥2

F = tr(Ω⊤MΩ) and ∥BℓΩ⊤∥2

F = tr(ΩNΩ⊤). Taking the derivative and setting it to zero gives the first-order optimality condition

MΩ+ ΩN = B⊤ ℓ∆B0 −A⊤ ℓ∆A0, which is (39). Since M and N are positive definite, f is strictly convex in Ωand the Sylvester equation has a unique solution, hence the minimizer is unique.

<!-- Page 18 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Relation to “horizontal” conditions. The optimality condition (39) is equivalent to orthogonality of the minimizer to the gauge (kernel) directions of the map (∆Aℓ, ∆Bℓ) 7→∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓunder the Euclidean metric on factors. This is the standard minimum-norm property of least-squares solutions and is closely related to horizontal lifts in quotient-geometry treatments (Mishra et al., 2014).

A.8. Gauge invariance of subspace projectors

Lemma A.12 (Projectors are gauge invariant). Let (A′ ℓ, B′ ℓ) = (AℓR, BℓR−⊤) for any invertible R ∈Rr×r. Then ΠA′ ℓ= ΠAℓand ΠB′ ℓ= ΠBℓ.

Proof. We prove the statement for ΠAℓ; the argument for ΠBℓis identical. Let A′ ℓ= AℓR. Then A′ ℓ

⊤A′ ℓ= R⊤(Aℓ

⊤Aℓ)R. By Lemma A.13,

(A′ ℓ

⊤A′ ℓ)

† =

R⊤(A⊤ ℓAℓ)R

†

= R−1(A⊤ ℓAℓ)

†R−⊤.

Therefore

ΠA′ ℓ= A′ ℓ

A′ ℓ

⊤A′ ℓ

†

A′ ℓ

⊤

= AℓR

R−1(A⊤ ℓAℓ)

†R−⊤

R⊤A⊤ ℓ

= Aℓ(A⊤ ℓAℓ)

†A⊤ ℓ = ΠAℓ.

Lemma A.13 (Pseudoinverse under congruence). Let X ⪰0 and let R be invertible. Then (R⊤XR)† = R−1X†R−⊤.

Proof. Let Y = R⊤XR and define Y ∗≜R−1X†R−⊤. We verify the Moore–Penrose conditions: Y Y ∗Y = Y, Y ∗Y Y ∗= Y ∗, and both Y Y ∗and Y ∗Y are symmetric. All follow from substituting the definition of Y and Y ∗, using RR−1 = I and the Moore–Penrose conditions for X and X†.

A.9. A canonical factor lift of the tangent projection

This subsection verifies that the explicit lift defined in Eq. (14) indeed reproduces the orthogonal tangent projection (13). Non-uniqueness of factor lifts (and a minimum-norm choice) is discussed separately in Appendix A.7.

Lemma A.14 (A convenient factor lift of the tangent projection). Let Zℓ= AℓB⊤ ℓand let Gi,ℓ≜∇Zℓℓi with factor gradients gA,i,ℓ= Gi,ℓBℓand gB,i,ℓ= G⊤ i,ℓAℓ. Define ∆Ai,ℓ, ∆Bi,ℓby (14). Then the induced matrix update

∆Zi,ℓ≜∆Ai,ℓB⊤ ℓ+ Aℓ∆B⊤ i,ℓ (40)

equals the tangent projection PAℓ,Bℓ(Gi,ℓ).

Proof. Step 1 (matching the matrix update). Using BℓN †B⊤ ℓ= ΠBℓand AℓM †A⊤ ℓ= ΠAℓ, gA,i,ℓN † = Gi,ℓ(BℓN †) = Gi,ℓΠBℓ, gB,i,ℓM † = G⊤ i,ℓ(AℓM †) = G⊤ i,ℓΠAℓ.

Hence

∆Ai,ℓB⊤ ℓ=

Gi,ℓΠBℓ−1

2ΠAℓ(Gi,ℓΠBℓ)

B⊤ ℓ= Gi,ℓΠBℓ−1

2ΠAℓGi,ℓΠBℓ,

Aℓ∆B⊤ i,ℓ= Aℓ

G⊤ i,ℓΠAℓ−1

2ΠBℓ(G⊤ i,ℓΠAℓ)

⊤= ΠAℓGi,ℓ−1

2ΠAℓGi,ℓΠBℓ.

Summing yields ∆Zi,ℓ= ΠAℓGi,ℓ+ Gi,ℓΠBℓ−ΠAℓGi,ℓΠBℓ= PAℓ,Bℓ(Gi,ℓ).

<!-- Page 19 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

A.10. Frobenius norm formula for tangent updates

Proposition A.15 (Frobenius norm of a factorized update). Let Zℓ= AℓB⊤ ℓand let ∆Zℓ= ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓfor arbitrary ∆Aℓ∈Rm×r and ∆Bℓ∈Rn×r. With M = A⊤ ℓAℓand N = B⊤ ℓBℓ,

∥∆Zℓ∥2

F = tr(∆A⊤ ℓ∆AℓN) + tr(∆B⊤ ℓ∆BℓM) + 2 tr

(A⊤ ℓ∆Aℓ)(B⊤ ℓ∆Bℓ)

. (41)

Proof of Proposition A.15. Expand ∥∆Zℓ∥2

F = ⟨∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ, ∆AℓB⊤ ℓ+ Aℓ∆B⊤ ℓ⟩and use cyclicity of trace:

∥∆AℓB⊤ ℓ∥2

F = tr(∆A⊤ ℓ∆AℓB⊤ ℓBℓ) = tr(∆A⊤ ℓ∆AℓN), ∥Aℓ∆B⊤ ℓ∥2

F = tr(∆B⊤ ℓ∆BℓA⊤ ℓAℓ) = tr(∆B⊤ ℓ∆BℓM), and ⟨∆AℓB⊤ ℓ, Aℓ∆B⊤ ℓ⟩= tr((A⊤ ℓ∆Aℓ)(B⊤ ℓ∆Bℓ)). Summing yields (41).

A.11. Specialization to rank-1 per-example gradients

Lemma A.16 (Norm for rank-1 gradients). Let Gi,ℓ= uv⊤and let ∆Zi,ℓ= PAℓ,Bℓ(Gi,ℓ). Define bu = ΠAℓu and bv = ΠBℓv. Then

∥∆Zi,ℓ∥2

F = ∥bu∥2

2 ∥v∥2 2 + ∥u∥2 2 ∥bv∥2 2 −∥bu∥2 2 ∥bv∥2 2. (42)

Proof. Use ∆Zi,ℓ= buv⊤+ubv⊤−bubv⊤and the identities ∥ab⊤∥2

F = ∥a∥2

2∥b∥2 2 and ⟨ab⊤, cd⊤⟩= (a⊤c)(b⊤d). Expanding and simplifying yields (42).

A.12. Factorized tangent noise equals a projected dense Gaussian

For convenience, define the whitened factors bAℓ≜AℓM −1/2, bBℓ≜BℓN −1/2, (43)

so that bA⊤ ℓbAℓ= bB⊤ ℓbBℓ= Ir and ΠAℓ= bAℓbA⊤ ℓ, ΠBℓ= bBℓbB⊤ ℓwhen Aℓ, Bℓhave full column rank.

Lemma A.17 (Distributional equivalence of the sampler). Let U ∈Rm×r and V ∈Rn×r have i.i.d. standard normal entries and define bAℓ, bBℓas in (43). Then

(I −ΠAℓ) U bB⊤ ℓ+ bAℓV ⊤ d= PAℓ,Bℓ(Ξℓ), where Ξℓhas i.i.d. N(0, 1) entries.

Proof. We show that vec(∆Znoise) is a zero-mean Gaussian with covariance equal to (46). Using the identity vec(XY ⊤) = (Y ⊗I)vec(X), we have vec

(I −ΠAℓ)U bB⊤ ℓ

= (bBℓ⊗(I −ΠAℓ)) vec(U), vec(bAℓV ⊤) = (I ⊗bAℓ) vec(V).

Since vec(U) and vec(V) are independent standard Gaussians, their images under fixed linear maps are independent Gaussians and the covariances add:

Cov vec(∆Znoise)

= (bBℓbB⊤ ℓ⊗(I −ΠAℓ)) + (I ⊗bAℓbA⊤ ℓ).

Substituting bBℓbB⊤ ℓ= ΠBℓand bAℓbA⊤ ℓ= ΠAℓyields

Cov vec(∆Znoise)

= (ΠBℓ⊗I) −(ΠBℓ⊗ΠAℓ) + (I ⊗ΠAℓ), which matches (46). Therefore ∆Znoise d= PAℓ,Bℓ(Ξℓ).

<!-- Page 20 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

A.13. Low-dimensional noise sampler

The intrinsic PRISM noise for module ℓis NZℓ= τ PAℓ,Bℓ(Ξℓ) with Ξℓ∼N(0, Im×n) and τ = σC/b (Theorem 3.1). Directly sampling the dense matrix Ξℓis unnecessary.

Let U ∈Rm×r and V ∈Rn×r have i.i.d. N(0, 1) entries, and define

ΞA,ℓ= (I −ΠAℓ) U N −1/2, ΞB,ℓ= V M −1/2, where M = A⊤ ℓAℓand N = B⊤ ℓBℓ. Then the intrinsic perturbation induced by these factor noises is

ΞA,ℓB⊤ ℓ+ AℓΞ⊤

B,ℓ, which matches the low-dimensional sampler in Eq. (19) (with (U, V) corresponding to (ΩA,ℓ, ΩB,ℓ)). By Lemma A.17 (Appendix A.12), this intrinsic perturbation is distributed exactly as PAℓ,Bℓ(Ξℓ).

Computationally, this reduces random number generation from O(mn) to O((m + n)r) per module. Stable computation of ΠAℓ, ΠBℓand the inverse square roots M −1/2, N −1/2 is discussed in Appendix A.14. The resulting intrinsic noise distribution is also invariant to the choice of factorization, as formalized in Appendix A.15.

A.14. Stable computation of projectors and orthonormal bases

For numerical stability, it is often preferable to compute the projectors ΠAℓ, ΠBℓand orthonormal bases of col(Aℓ) and col(Bℓ) without forming Gram-matrix inverses explicitly. We record simple equivalences.

Lemma A.18 (Projector from a thin QR factorization). Assume Aℓ∈Rm×r has full column rank and let Aℓ= QARA be a thin QR factorization with Q⊤

AQA = Ir and RA invertible. Then the orthogonal projector onto col(Aℓ) satisfies ΠAℓ= QAQ⊤

A. An analogous statement holds for Bℓ.

Proof. Since A⊤ ℓAℓ= R⊤

ARA, we have

ΠAℓ= Aℓ(A⊤ ℓAℓ)−1A⊤ ℓ= QARA(R⊤

ARA)−1R⊤

AQ⊤

A = QAQ⊤

A, because RA(R⊤

ARA)−1R⊤

A = Ir when RA is invertible.

Lemma A.19 (Noise sampling is invariant to the choice of orthonormal bases). Let QA, Q′

A ∈Rm×r be orthonormal bases of the same subspace col(Aℓ) and let QB, Q′

B ∈Rn×r be orthonormal bases of col(Bℓ). Define ΠAℓ= QAQ⊤

A = Q′

AQ′⊤

A and ΠBℓ= QBQ⊤

B = Q′

BQ′⊤

B. If U ∈Rm×r and V ∈Rn×r have i.i.d. N(0, 1) entries, then

(I −ΠAℓ) U Q⊤

B + QAV ⊤ d= (I −ΠAℓ) U Q′⊤

B + Q′

AV ⊤.

Proof. Because QA and Q′

A are orthonormal bases of the same subspace, there exists an orthogonal matrix OA ∈Rr×r such that Q′

A = QAOA. Similarly, Q′

B = QBOB for some orthogonal OB. Then

(I −ΠAℓ)UQ′⊤

B + Q′

AV ⊤= (I −ΠAℓ)UO⊤

BQ⊤

B + QAOAV ⊤.

Since U and V are i.i.d. standard Gaussian matrices, UO⊤

B d= U and OAV d= V. The claim follows.

Regularization. When Gram matrices are nearly singular, one can obtain stable orthonormal bases via QR/SVD and use Lemma A.18 to form ΠAℓ, ΠBℓ. If one instead regularizes Gram inverses directly (e.g., spectral truncation or damping), the resulting operators are still deterministic functions of (Aℓ, Bℓ) and therefore DP-safe by post-processing, but may not preserve exact gauge invariance unless the regularization is itself defined in a gauge-consistent way.

A.15. Gauge invariance of the factorized noise sampler

We recall the factorized sampler used to generate the tangent noise lifts in Eq. (18):

∆Anoise = (I −ΠAℓ) U N −1/2, ∆Bnoise = V M −1/2, (44)

<!-- Page 21 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA where U ∈Rm×r and V ∈Rn×r have i.i.d. N(0, 1) entries, and M = A⊤ ℓAℓ, N = B⊤ ℓBℓ. The induced intrinsic perturbation is ∆Znoise = ∆AnoiseB⊤ ℓ+ Aℓ∆B⊤ noise.

The intrinsic mechanism (18) is gauge invariant by construction. Here we make explicit that the implementation-level sampler (44) inherits the same invariance: regardless of which factorization of Zℓis used internally, the induced distribution on the intrinsic noise ∆Znoise is unchanged. Proposition A.20 (Sampler invariance under gauge transforms). Let (A′ ℓ, B′ ℓ) = (AℓR, BℓR−⊤) for some R ∈GL(r). Construct ∆Anoise and ∆Bnoise from (Aℓ, Bℓ) via (44), and construct ∆A′ ℓ,noise and ∆B′ ℓ,noise from (A′ ℓ, B′ ℓ) via the same formula (with the corresponding projectors and Gram matrices). Then the induced intrinsic noises

∆Znoise = ∆AnoiseB⊤ ℓ+ Aℓ(∆Bnoise)⊤, ∆Z′ noise = ∆A′ ℓ,noise(B′ ℓ)⊤+ A′ ℓ(∆B′ ℓ,noise)⊤.

have the same distribution.

Proof. By Lemma A.17, both ∆Znoise and ∆Z′ noise are distributed as PAℓ,Bℓ(Ξℓ) and PA′,B′(Ξℓ), respectively, for a dense standard Gaussian Ξℓ. By Lemma A.12, the subspace projectors are gauge invariant and thus PA′,B′ = PAℓ,Bℓ. Therefore PA′,B′(Ξℓ) and PAℓ,Bℓ(Ξℓ) have identical distributions.

Contrast with naive factor noise. If one instead adds i.i.d. Gaussian noise directly to ∆Aℓand ∆Bℓwithout the whitening and projection factors in (44), the induced intrinsic perturbation depends on the chosen gauge through ∥Aℓ∥F and ∥Bℓ∥F (Proposition 2.2). The role of M −1/2 and N −1/2 in (44) is precisely to compensate for this coordinate dependence and yield an isotropic Gaussian in the intrinsic tangent space.

A.16. Proof of Theorem 3.1

Proof of Theorem 3.1. Let Ξℓ∼N(0, Im×n) be a dense standard Gaussian and write NZℓ= τ PAℓ,Bℓ(Ξℓ) with τ = σC/b.

Gaussianity and support. Vectorizing gives vec(Ξℓ) ∼N(0, Imn) and vec(PAℓ,Bℓ(Ξℓ)) = P vec(Ξℓ), where P is the matrix representation of the orthogonal projector PAℓ,Bℓunder vec(·). Since P is linear, symmetric, and idempotent, P vec(Ξℓ) is Gaussian with covariance P and is supported on range(P), which corresponds to the tangent subspace TZℓMr (Eq. (13)).

Isotropy on the tangent space. Because the covariance equals the orthogonal projector onto TZℓMr, the distribution is isotropic within that subspace; a self-contained verification is given in Lemma A.21 (Appendix A.17).

Expected energy. Using ∥X∥2

F = ∥vec(X)∥2

2 and E∥G∥2 2 = tr(Cov[G]) for a zero-mean Gaussian vector G, we obtain

E

PAℓ,Bℓ(Ξℓ)

2

F = E

Pvec(Ξℓ)

2

2 = tr(P) = rank(P) = dim(TZℓMr) = r(m + n −r), which is Eq. (20). Multiplying by τ 2 yields E∥NZℓ∥2

F = τ 2r(m + n −r) and thus Eq. (21).

Gauge invariance. Finally, PAℓ,Bℓdepends only on ΠAℓand ΠBℓ(Eq. (13)), and these projectors are invariant under the gauge transform (Aℓ, Bℓ) 7→(AℓR, BℓR−⊤) by Lemma A.12 (Appendix A.8).

A.17. Isotropy of the projected Gaussian on the tangent space

Lemma A.21 (Isotropy within TZℓMr). Let Ξℓ∈Rm×n have i.i.d. N(0, 1) entries and let PAℓ,Bℓbe the orthogonal projector onto TZℓMr. For any U, V ∈TZℓMr,

E

⟨U, PAℓ,Bℓ(Ξℓ)⟩⟨V, PAℓ,Bℓ(Ξℓ)⟩

= ⟨U, V ⟩. (45)

Equivalently, PAℓ,Bℓ(Ξℓ) is an isotropic Gaussian in the tangent space under the Frobenius inner product.

Proof. Because PAℓ,Bℓis an orthogonal projector, it is self-adjoint: ⟨U, PAℓ,Bℓ(X)⟩= ⟨PAℓ,Bℓ(U), X⟩for all U, X. For U ∈TZℓMr, PAℓ,Bℓ(U) = U. Therefore ⟨U, PAℓ,Bℓ(Ξℓ)⟩= ⟨U, Ξℓ⟩and similarly for V. Since Ξℓhas i.i.d. standard normal entries, ⟨U, Ξℓ⟩is a centered Gaussian with variance ∥U∥2

F, and

E[⟨U, Ξℓ⟩⟨V, Ξℓ⟩] = ⟨U, V ⟩.

<!-- Page 22 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

A.18. Projected Gaussian covariance and intrinsic dimension

Lemma A.22 (Covariance of a projected dense Gaussian). Let Ξℓ∈Rm×n have i.i.d. N(0, 1) entries and let Zℓ= AℓB⊤ ℓ∈Mr. Then PAℓ,Bℓ(Ξℓ) is a centered Gaussian supported on TZℓMr with vectorized covariance

Cov vec

PAℓ,Bℓ(Ξℓ)

= (In ⊗ΠAℓ) + (ΠBℓ⊗Im) −(ΠBℓ⊗ΠAℓ). (46)

If Aℓand Bℓhave full column rank, the covariance operator in Eq. (46) is an orthogonal projector of rank r(m + n −r), which implies E∥PAℓ,Bℓ(Ξℓ)∥2

F = r(m + n −r) (Eq. (20)).

Proof of Lemma A.22. Write P(Ξℓ) = ΠAℓΞℓ+ ΞℓΠBℓ−ΠAℓΞℓΠBℓand apply vectorization: vec(ΠAℓΞℓ) = (I ⊗ ΠAℓ)vec(Ξℓ), vec(ΞℓΠBℓ) = (ΠBℓ⊗I)vec(Ξℓ), vec(ΠAℓΞℓΠBℓ) = (ΠBℓ⊗ΠAℓ)vec(Ξℓ). Thus vec(P(Ξℓ)) =

I ⊗ΠAℓ+ ΠBℓ⊗I −ΠBℓ⊗ΠAℓ vec(Ξℓ).

Since vec(Ξℓ) ∼N(0, I), the covariance is (46). When Aℓ, Bℓare full column rank, this covariance is an orthogonal projector with rank r(m + n −r) (Edelman et al., 1998). The expected squared norm equals the trace, giving (20).

A.19. Concentration of the effective intrinsic noise in PRISM

Because PAℓ,Bℓ(Ξℓ) is an isotropic Gaussian in the tangent space (Lemma A.21), its Frobenius norm concentrates sharply. This provides high-probability control beyond the expectation in (20).

Lemma A.23 (Chi-square form). Assume Aℓand Bℓare full column rank and let d ≜dim(TZℓMr) = r(m + n −r). Let Ξℓ∈Rm×n have i.i.d. N(0, 1) entries and set G = PAℓ,Bℓ(Ξℓ). Then ∥G∥2

F has a chi-square distribution with d degrees of freedom:

∥G∥2

F ∼χ2 d. (47)

Proof. Let {E1,..., Ed} be any orthonormal basis of TZℓMr under ⟨·, ·⟩. Since PAℓ,Bℓis the orthogonal projector onto TZℓMr, we may write G = Pd k=1⟨Ξℓ, Ek⟩Ek. By orthonormality and independence of Gaussian linear functionals, the coefficients {⟨Ξℓ, Ek⟩}d k=1 are i.i.d. N(0, 1). Therefore ∥G∥2

F = Pd k=1⟨Ξℓ, Ek⟩2 is chi-square with d degrees of freedom.

Proposition A.24 (High-probability bound for PRISM noise). Let NZℓ= σC b PAℓ,Bℓ(Ξℓ) be the intrinsic Gaussian perturbation in DP-PRISM. Let d = r(m + n −r). Then for any δ ∈(0, 1),

Pr

∥NZℓ∥F ≤σC b q d + 2 p d log(1/δ) + 2 log(1/δ)

≥1 −δ. (48)

Proof. By Lemma A.23, ∥NZℓ∥2

F = (σC/b)2X where X ∼χ2 d. A standard chi-square concentration inequality gives Pr(X −d ≥2

√ dt + 2t) ≤e−t for all t ≥0. Setting t = log(1/δ) yields (48).

Remark. Proposition A.24 shows that the realized intrinsic noise magnitude in PRISM concentrates around its mean EZℓ with relative fluctuations O(1/

√ d). This is useful when interpreting the privacy–utility trade-off in large layers, where d = r(m + n −r) is large.

A.20. Retraction and rank-r approximation

We justify Proposition 3.2 and record standard facts about truncated SVD retractions.

Lemma A.25 (Eckart–Young–Mirsky theorem). Let X ∈Rm×n have singular values s1 ≥· · · ≥smin(m,n). Let Xr be the truncated SVD keeping the top r singular values. Then Xr is a best rank-r approximation in Frobenius norm:

Xr ∈arg min rank(Y)≤r ∥X −Y ∥F, ∥X −Xr∥2

F =

X k>r s2 k.

Proof. See (Eckart & Young, 1936; Mirsky, 1960).

<!-- Page 23 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Proof of Proposition 3.2. Let Xη = Z −η∆Z. Define

Yη = (A −η∆A)(B −η∆B)⊤.

Then rank(Yη) ≤r, and

Yη = Z −η(∆AB⊤+ A∆B⊤) + η2∆A∆B⊤= Xη + η2∆A∆B⊤.

By Lemma A.25, Retrr(Xη) is a best rank-r approximation to Xη. Since Yη is a rank-r candidate,

∥Xη −Retrr(Xη)∥F ≤∥Xη −Yη∥F = η2∥∆A∆B⊤∥F.

This proves Eq. (23). Finally, ∥∆A∆B⊤∥F ≤∥∆A∥F ∥∆B∥F, giving the stated second-order distortion bound.

A.21. Absence of bilinear second-order DP noise in PRISM

Lemma A.26 (PRISM noise is additive in the intrinsic parameter). Consider one PRISM iteration for a single LoRA module. Conditioned on the minibatch and on the Gaussian randomness used in (18), the update takes the intrinsic additive form

Z+ ℓ= Retrr

Zℓ−η

¯ ∆Zℓ+ σC b PAℓ,Bℓ(Ξℓ)

, where ¯ ∆Zℓis the clipped mean tangent update. In particular, the only randomness in the intrinsic update is the linear Gaussian term PAℓ,Bℓ(Ξℓ); there is no bilinear product of independent noises analogous to ξA,ℓξ⊤

B,ℓin (7).

Proof. This is immediate from the definition of PRISM in (18)–(22) and the linearity of PAℓ,Bℓ. Retraction Retrr and any subsequent factorization/gauge alignment are deterministic post-processing steps.

A.22. Proof of Theorem 3.3

Proof of Theorem 3.3. Part (i) is Lemma A.12. Part (ii) follows from Proposition A.3 since PAℓ,Bℓdepends only on (ΠAℓ, ΠBℓ). For (iii), PAℓ,Bℓ(Ξℓ) is a measurable function of (ΠAℓ, ΠBℓ, Ξℓ) and (ΠAℓ, ΠBℓ) are unchanged under gauge transformations, hence the induced distribution is unchanged. Retraction, refactorization, and gauge alignment are deterministic maps of the intrinsic quantities, so they preserve gauge invariance.

A.23. Gaussian mechanism on a linear subspace

DP analyses are often stated for outputs in Rd with full-dimensional Gaussian noise. PRISM adds Gaussian noise supported on the tangent subspace TZℓMr. This is still a standard Gaussian mechanism once the output space is identified with the subspace.

Lemma A.27 (Gaussian mechanism restricted to a subspace). Let S ⊆Rd be a linear subspace with orthogonal projector ΠS. Let f: D 7→S be a function with ℓ2 sensitivity at most ∆: ∥f(D) −f(D′)∥2 ≤∆for all adjacent D, D′. Let g ∼N(0, Id) and define the mechanism

M(D) ≜f(D) + σ∆ΠSg.

Then M is (ε, δ)-DP for the same (ε, δ) guarantee as the standard Gaussian mechanism in dimension dim(S) (with noise multiplier σ).

Proof. Let k = dim(S) and let U ∈Rd×k have orthonormal columns spanning S so that ΠS = UU ⊤. Write f(D) =

Uα(D) for some α(D) ∈Rk. Then ΠSg = UU ⊤g d= Uh where h ∼N(0, Ik). Therefore M(D)

d= U(α(D) + σ∆h). Since U is an isometry on S, the DP guarantee for α(D) + σ∆h (a standard Gaussian mechanism in Rk) transfers directly to M.

A.24. Procrustes alignment is a gauge transform

Lemma A.28 (Orthogonal alignment is gauge preserving). Let Zℓ= AℓB⊤ ℓwith Aℓ, Bℓfull column rank and let Q be orthogonal. Then (A′ ℓ, B′ ℓ) = (AℓQ, BℓQ) satisfies A′ ℓB′ ℓ

⊤= Zℓand leaves ΠAℓ, ΠBℓunchanged.

<!-- Page 24 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Proof. A′ ℓB′ ℓ

⊤= (AℓQ)(BℓQ)⊤= AℓQQ⊤B⊤ ℓ= AℓB⊤ ℓ. For the projector,

A′ ℓ

(A′ ℓ)⊤A′ ℓ

†

(A′ ℓ)⊤= AℓQ

Q⊤A⊤ ℓAℓQ

†

Q⊤A⊤ ℓ= Aℓ(A⊤ ℓAℓ)

†A⊤ ℓ= ΠAℓ, because

Q⊤XQ

†

= Q⊤X

†Q for orthogonal Q.

A.25. DP guarantee details

We provide a proof of Theorem 3.4.

Proof of Theorem 3.4. Write the per-example intrinsic tangent update (concatenated across all LoRA modules) as ∆Zℓi ∈T, where T denotes the direct-sum tangent space equipped with the Frobenius inner product. PRISM applies intrinsic clipping (Eq. (16)) to obtain ˜ ∆Zℓi = αi ∆Zℓi with ∥˜ ∆Zℓi∥F ≤C. Hence the ℓ2 sensitivity of the minibatch average is bounded by

1 b b X i=1

˜ ∆Zℓi(D) −1 b b X i=1

˜ ∆Zℓi(D′)

F

≤C b for any adjacent datasets D, D′.

Next, PRISM adds Gaussian noise of standard deviation σC/b in T. Concretely, each module samples a dense Gaussian matrix and applies the orthogonal tangent projector (Eq. (13)), so the resulting noise is a Gaussian restricted to a linear subspace. By Lemma A.27, the released vector d ∆Zℓ= 1 b b X i=1

˜ ∆Zℓi + σC b G, G ∼N(0, ΠT), is an instance of the Gaussian mechanism with sensitivity C/b.

Finally, under Poisson subsampling with rate q = b/N, each iteration is a subsampled Gaussian mechanism. The overall (ε, δ) guarantee after T steps follows from standard privacy-loss composition for subsampled Gaussian mechanisms, and

PRISM uses the PRV accountant implemented in Opacus to compute ε for a target δ (Gopi et al., 2021; Yousefpour et al., 2022; Opacus Contributors, 2026). All subsequent operations (adaptive post-processing, factorization, alignment, and retraction) are deterministic post-processing and therefore do not weaken DP.

A.26. Rank-space moments of isotropic tangent noise

This section derives the rank-space second moments of the isotropic tangent noise used by PRISM (Eq. (19)), which motivates the DP-aware floors in Eq. (26). Let U ∼N(0, Im×r) and V ∼N(0, In×r), and define ΞA,ℓ= (I −ΠAℓ)U N −1/2 and ΞB,ℓ= V M −1/2 with M = A⊤ ℓAℓand N = B⊤ ℓBℓ. Then

E[Ξ⊤

A,ℓΞA,ℓ] = N −1/2 E[U ⊤(I −ΠAℓ)U] N −1/2, E[Ξ⊤

B,ℓΞB,ℓ] = M −1/2 E[V ⊤V ] M −1/2. (49)

Since U has i.i.d. standard normal entries and (I −ΠAℓ) is an orthogonal projector of rank tr(I −ΠAℓ) = m −r, we have E[U ⊤(I −ΠAℓ)U] = (m −r)Ir. Similarly, E[V ⊤V ] = nIr. Substituting into (49) yields

E hΞ⊤

A,ℓΞA,ℓ m i

= m −r m N −1, E hΞ⊤

B,ℓΞB,ℓ n i

= M −1. (50)

Thus the typical eigenvalues of the rank-space noise covariance scale with M −1 and N −1, explaining why inverse-squareroot preconditioning can explode when M or N is ill-conditioned. PRISM’s floors in Eq. (26) are gauge invariant because tr(M −1) and tr(N −1) are invariant under (Aℓ, Bℓ) 7→(AℓR, BℓR−⊤).

A.27. Adaptive preconditioning and DP noise amplification

This subsection complements Section 3 and proves Theorem 3.5. We also record a simple identity showing how rank-space normalization can “cancel” the DP noise scale when the second moment is dominated by noise.

<!-- Page 25 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

Proof of Theorem 3.5. Since V ⪰0, write its eigendecomposition V = UΛU ⊤with Λ = diag(λ1,..., λr) and λi ≥0. Then P = V + λI = U(Λ + λI)U ⊤and thus P−1/2 = U(Λ + λI)−1/2U ⊤.

∥P−1/2∥2 = max i (λi + λ)−1/2 ≤λ−1/2.

For any X, submultiplicativity of the Frobenius norm gives ∥XP−1/2∥F ≤∥X∥F ∥P−1/2∥2 ≤λ−1/2∥X∥F. Squaring yields Eq. (27).

Proposition A.29 (Noise normalization under naive rank-space preconditioning). Let G ∈Rm×r have i.i.d. N(0, 1) entries and define the (uncentered) second moment V ≜1 mG⊤G. Then the preconditioned matrix Q ≜GV −1/2 satisfies

Q⊤Q = mIr and hence ∥Q∥2

F = mr.

Equivalently, if bm = τG for any τ > 0 and V = 1 m bm⊤bm, then bm V −1/2 has Frobenius norm √mr independent of τ.

Proof. By definition, Q⊤Q = V −1/2G⊤GV −1/2 = V −1/2(mV)V −1/2 = mIr. Taking traces gives ∥Q∥2

F = tr(Q⊤Q) = mr. The final claim follows from V = τ 2(1 mG⊤G), which implies bmV −1/2 = G(1 mG⊤G)−1/2 = Q.

Proposition A.29 explains the issue in Issue III: when an adaptive method forms V directly from a DP-sanitized gradient whose energy is dominated by DP noise, the right-multiplication by V −1/2 can make the stochastic component insensitive to the DP noise scale. PRISM avoids this via (i) DP-aware floors and condition-number clamping (Eq. (26)), which bound ∥V −1/2∥2 and prevent ill-conditioned amplification, and (ii) debiasing of the second moment by subtracting the known DP noise covariance in rank space (Appendix A.26).

Lemma A.30 (Orthogonal gauge equivariance of rank-space preconditioning). Let R ∈Rr×r be orthogonal and consider the restricted gauge transform (Aℓ, Bℓ) 7→(AℓR, BℓR). If bmA, bmB transform as bm′

A = bmAR and bm′

B = bmBR, and the second moments transform as V ′

A = R⊤VAR and V ′

B = R⊤VBR, then the preconditioned directions from Eq. (25) satisfy U ′

A = UAR and U ′

B = UBR, and therefore the intrinsic update UAB⊤ ℓ+ AℓU ⊤

B is invariant.

Proof. For orthogonal R, similarity equivariance of matrix functions yields (V ′

A + λI)−1/2 = (R⊤(VA + λI)R)−1/2 = R⊤(VA + λI)−1/2R. Thus U ′

A = bm′

A(V ′

A + λI)−1/2 = bmAR R⊤(VA + λI)−1/2R = UAR, and similarly U ′

B = UBR. Finally, with A′ ℓ= AℓR and B′ ℓ= BℓR we have

U ′

A(B′ ℓ)⊤+ A′ ℓ(U ′

B)⊤= (UAR)(BℓR)⊤+ (AℓR)(UBR)⊤

= (UAR)(R⊤B⊤ ℓ) + (AℓR)(R⊤U ⊤

B)

= UA(RR⊤)B⊤ ℓ+ Aℓ(RR⊤)U ⊤

B = UAB⊤ ℓ+ AℓU ⊤

B,

B. Experimental Setup

B.1. Experimental Details

This section reports dataset split sizes, hyperparameters, and the hardware/software environment used in our experiments.

Compute. All experiments were run on a single NVIDIA A100-PCIE-40GB GPU.

Datasets and splits. Table 6 reports the training sizes we used and evaluation split sizes. GLUE8 is derived from GLUE (Wang et al., 2018) (excluding WNLI), converted to an instruction-format JSON dataset, and sub-sampled with a fixed number of training examples per task. Math-10K is the LLM-Adapters mixture (Hu et al., 2023; AGI-Edgerunners, 2023) and is evaluated on the standard test splits of its component datasets.

Common fine-tuning hyperparameters. Unless otherwise stated, all methods share the same backbone, LoRA configuration, and DP settings in Table 7. For DP runs, the noise multiplier is calibrated with Opacus make private with epsilon using the default PRV accountant (Gopi et al., 2021; Opacus Contributors, 2026).

<!-- Page 26 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

**Table 6.** Dataset splits used in our experiments.

DATASET / SPLIT TRAIN EVAL

GLUE8 COLA 1,250 1,043 SST-2 1,250 872 MRPC 1,250 408 STS-B 1,250 1,500 QQP 1,250 40,430 MNLI (MATCHED / MISMATCHED) 1,250 9,815 / 9,832 QNLI 1,250 5,463 RTE 1,250 277

GLUE8 TOTAL 10,000 –

MATH-10K MATH-10K TRAIN (MIXTURE) 9,919 – GSM8K TEST – 1,319 AQUA TEST – 254 MAWPS TEST – 238 SVAMP TEST – 1,000

**Table 7.** Common hyperparameters shared across methods.

SETTING GLUE8 MATH-10K

BACKBONE MODEL GOOGLE/GEMMA-3-4B-PT (GEMMA TEAM ET AL., 2025) SAME LORA RANK r 16 16 LORA SCALING αLoRA 16 16 LORA DROPOUT 0.05 0.05 TARGET MODULES {Q PROJ,K PROJ,V PROJ,UP PROJ,DOWN PROJ} SAME UPDATE STEPS 500 300 EFFECTIVE BATCH SIZE 64 64 MICRO-BATCH SIZE 4 4 MAX SEQUENCE LENGTH 384 256 TRAIN ON INPUTS FALSE TRUE RANDOM SEED 42 42 DP BUDGETS ε ∈{3, 6}, δ = 10−5 SAME CLIPPING NORM C 1.0 1.0 DP GRAD-SAMPLE BACKEND FUNCTORCH (FALLBACK TO HOOKS) SAME DP ACCOUNTANT PRV (OPACUS DEFAULT) (GOPI ET AL., 2021; OPACUS CONTRIBUTORS, 2026) SAME

C. Additional Diagnostics and Analysis

C.1. Additional diagnostics for Issue I

Diagnostic protocol and hyperparameters. We evaluate gauge sensitivity by running DP training under multiple equivalent LoRA factorizations of the same intrinsic update Zℓ= AℓB⊤ ℓ. For each gauge c, we apply the reparameterization (Aℓ, Bℓ) ←(cAℓ, c−1Bℓ), which leaves Zℓunchanged but alters factor-space norms. We train for T = 300 update steps on

Math-10K and log (i) clipping fraction dp clip frac, (ii) mean clipping coefficient dp coef mean, and (iii) realized intrinsic step magnitude ∥∆Zt∥F, where ∆Zt ≡Zt+1 −Zt is computed from the actual parameter update (not a formula-level proxy). Gauges: c ∈{0.25, 0.5, 1.0, 2.0, 4.0}.

Metrics and theoretical link. In baseline factor-space DP-SGD, per-example clipping uses the factor norm sfact i = p

∥gA,i∥2

F + ∥gB,i∥2

F and αi = min{1, Cfact/sfact i } (cf. (3)). Under gauge rescaling, the norm transforms as (4), so αi and the induced intrinsic update distribution depend on c (Issue-I). PRISM instead forms intrinsic directions via the tangent construction and projectors (e.g., (13), (14)), clips using the intrinsic norm (16), and adds isotropic tangent noise (17); these operations are designed to depend on Zℓrather than on a particular factorization, so gauge dependence should be strongly reduced (up to stochastic variability from DP noise).

Interpretation (Figure 5). This plot summarizes how the clipping coefficients vary across gauges during training. For

<!-- Page 27 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

**Table 8.** Method-specific hyperparameters.

METHOD OPTIMIZER LR (GLUE8) LR (MATH) SUPPLEMENTARY

ADAMW ADAMW (KINGMA & BA, 2015; LOSHCHILOV & HUT- TER, 2019)

2×10−4 3×10−4 –

FFA ADAMW + FREEZE Aℓ(SUN ET AL., 2024)

2×10−4 3×10−4 –

RITE LORA-RITE (YEN ET AL., 2025) 2×10−4 3×10−4 –

LORA+ ADAMW SPLIT LRS (HAYOU ET AL., 2024)

2×10−4 3×10−4 RATIO ρ = 6.0.

LAMB LAMB (YOU ET AL., 2020) 5×10−3 5×10−3 – PRISM PRISM (OURS) 2×10−4 3×10−4 –

0 50 100 150 200 250 300 Update step

0.0

0.2

0.4

0.6

0.8

1.0

Mean DP coefficient

Baseline PRISM

**Figure 5.** Over-time bands of dp coef mean across gauges (mean with IQR band; min/max lines).

baseline, the spread between min/max (and the IQR band) remains wide for most of training, indicating that the same DP configuration produces materially different clipping behavior depending on (Aℓ, Bℓ)’s gauge. This matches the mechanism in (4): changing c reweights ∥gA,i∥F versus ∥gB,i∥F, hence changes sfact i and pushes different gauges into different clipping regimes (larger/smaller αi). For PRISM, dp coef mean concentrates near 1 after the transient, and the across-gauge dispersion shrinks, consistent with clipping being controlled by the intrinsic norm si in (16), which depends on ∆Zi,ℓrather than on factor scaling. Importantly, the remaining non-zero dispersion is expected in finite runs because DP noise makes αi and ∆Zℓstochastic, but PRISM’s variability is markedly smaller than baseline’s.

Interpretation (Figure 6). This figure measures the actual intrinsic update applied to Zℓat each step (computed from Zt+1 −Zt), thus directly reflecting the DP perturbation that matters in the intrinsic space. Baseline exhibits a persistent and relatively wide band across gauges: some gauges yield substantially larger ∥∆Zt∥F than others. This is the operational manifestation of Issue-I: once αi is gauge-dependent via (4), the clipped-and-noised factor update implies a gaugedependent induced update on Zℓ, so ∥∆Zt∥F cannot be predicted from Zℓalone. PRISM shows a transient early phase (optimizer/moment warm-up plus DP stochasticity) and then stabilizes to a smaller, tighter band; this is consistent with intrinsic clipping (16) and tangent noise (17) controlling the intrinsic step directly. The remaining oscillations are natural: even a gauge-invariant distribution will yield non-identical single-run trajectories under DP noise, but PRISM suppresses the systematic gauge effect visible in baseline.

Interpretation (Figure 7). We compress the multi-gauge experiment into a single diagnostic: rangec(dp coef mean) = maxc dp coef mean(c) −minc dp coef mean(c). A gauge-invariant DP mechanism should make this range small (up to stochastic fluctuations). Baseline remains high throughout training, directly supporting the theoretical failure mode: factor-space clipping depends on c because of (4), so the average clipping coefficient changes substantially across equivalent parameterizations. PRISM yields a much smaller range after the initial transient, consistent with using the intrinsic norm

<!-- Page 28 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

0 50 100 150 200 250 300 Update step

10−1

100

‖ΔZ‖F per step

Baseline PRISM

**Figure 6.** Over-time bands of realized intrinsic step magnitude ∥∆Zt∥F across gauges (mean with IQR band; min/max lines).

0 50 100 150 200 250 300 Update step

0.0

0.2

0.4

0.6

0.8

1.0

Range of mean DP coefficient

Baseline PRISM

**Figure 7.** Gauge-sensitivity index for clipping: rangec(dp coef mean) over time.

(16) and tangent construction ((13), (14)) to decouple DP sensitivity control from gauge.

Interpretation (Figure 8). This is the most direct “mechanism check” for Issue-I: the x-axis varies only the gauge c, while all intrinsic quantities are initially identical. At step 1, baseline’s clipping fraction moves from almost fully clipped (small c) to almost never clipped (large c), i.e., a qualitative regime change triggered purely by reparameterization. This matches (4): for small c the c−2∥gA,i∥2

F term can dominate, inflating norms and forcing αi ≪1; for larger c the norm shrinks and clipping disengages. PRISM is approximately flat across gauges, aligning with intrinsic clipping (16): the clipping decision depends on ∥∆Zi,ℓ∥F rather than on factor scaling.

Interpretation (Figure 9). The mean clipping coefficient dp coef mean is a smoother counterpart of Figure 8: it directly measures the average shrinkage induced by DP clipping, αi = min{1, C/si}. Baseline increases monotonically with c at step 1, showing that the same DP algorithm injects different effective shrinkage (hence different intrinsic update distributions) purely due to gauge, as predicted by (4). PRISM remains roughly constant across gauges, consistent with controlling sensitivity in intrinsic space (16) and therefore avoiding this reparameterization artifact.

Interpretation (Figure 10). By step 300, baseline’s dp clip frac is close to 1 for all gauges, indicating a clipping-saturated regime in factor space: most examples are clipped regardless of c. This supports (but also partially limits) diagnostic interpretability: once clipping saturates, the mechanism becomes less sensitive to further changes in the factor norms, so a flatter curve here does not imply gauge invariance. In contrast, PRISM shows a near-zero clipping fraction at step 300 for all gauges, suggesting that (under the intrinsic threshold Cint) optimization has entered a stable region where intrinsic

<!-- Page 29 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

−0.6 −0.4 −0.2 0.0 0.2 0.4 0.6 log10 (gauge c)

0.0

0.2

0.4

0.6

0.8

1.0

Clipping fraction

Baseline PRISM

**Figure 8.** Discrete gauge sweep of dp clip frac at step 1.

−0.6 −0.4 −0.2 0.0 0.2 0.4 0.6 log10 (gauge c)

0.0

0.2

0.4

0.6

0.8

1.0

Mean DP coefficient

Baseline PRISM

**Figure 9.** Discrete gauge sweep of dp coef mean at step 1.

per-example norms mostly lie below the clip bound in (16). Thus, the step-300 sweep is best viewed as confirming that late training can enter a stable/saturated regime, rather than as the primary evidence for Issue-I (which is better captured at step 1 and by Figures 2 and 7).

Interpretation (Figure 11). Consistent with Figure 10, baseline’s dp coef mean still varies with gauge at step 300, but the variability is reduced relative to step 1 because clipping is already heavily engaged for all gauges (many αi < 1). This illustrates a subtle but important point: Issue-I is fundamentally about the mechanism’s dependence on reparameterization (here seen sharply at step 1), and saturation can mask that dependence by collapsing the algorithm into an always-clipped regime. PRISM’s dp coef mean concentrates near 1 across gauges at step 300, consistent with intrinsic clipping being mostly inactive and the DP perturbation being governed primarily by tangent noise (17) rather than by gauge-dependent shrinkage. Together with the intrinsic step sensitivity in Figure 2, these late-step diagnostics suggest PRISM’s intrinsic control yields a more stable intrinsic update distribution across equivalent factorizations.

C.2. Additional diagnostics for Issue II

Gauge sweep protocol. We snapshot the LoRA layer with the largest St at the end of training and sweep the gauge (Aℓ, Bℓ) 7→(cAℓ, c−1Bℓ), which keeps Zℓ= AℓB⊤ ℓfixed. We evaluate log10 c ∈linspace(−3, 3, 61) and draw 64 Monte-Carlo samples per c; we plot the median and the 10–90% band.

<!-- Page 30 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

−0.6 −0.4 −0.2 0.0 0.2 0.4 0.6 log10 (gauge c)

0.0

0.2

0.4

0.6

0.8

1.0

Clipping fraction

Baseline PRISM

**Figure 10.** Discrete gauge sweep of dp clip frac at step 300.

−0.6 −0.4 −0.2 0.0 0.2 0.4 0.6 log10 (gauge c)

0.0

0.2

0.4

0.6

0.8

1.0

Mean DP coefficient

Baseline PRISM

**Figure 11.** Discrete gauge sweep of dp coef mean at step 300.

What Figure 12 tests. Issue II predicts that factor-space DP can inject a gauge-dependent intrinsic noise even when the intrinsic parameter Zℓ= AℓB⊤ ℓ(and thus the model function) is held fixed. From Eq. (8), the first-order intrinsic noise satisfies

E∥ξA,ℓB⊤ ℓ+ Aℓξ⊤

B,ℓ∥2

F = τ 2 m∥Bℓ∥2

F + n∥Aℓ∥2

F

, so under (Aℓ, Bℓ) 7→(cAℓ, c−1Bℓ) the coefficient becomes S(c) = mc−2∥Bℓ∥2

F + nc2∥Aℓ∥2

F, which is minimized at cth = m∥Bℓ∥2

F n∥Aℓ∥2

F

1/4 and diverges as c →0 or c →∞. PRISM instead samples isotropic tangent noise PAℓ,Bℓ(Ξℓ), whose distribution depends only on the tangent projector, and whose energy is controlled by the intrinsic dimension (cf. EZℓ= (σC/b)

p r(m + n −r) in the main text). Empirically, Figure 12 matches this dichotomy: the baseline (factor-space DP) curve varies by orders of magnitude across c despite fixed Zℓ, while PRISM remains essentially flat up to Monte- Carlo variability. The baseline “bilinear” component (from the η ξA,ℓξ⊤

B,ℓterm in Eq. (7)) is comparatively small and gauge-invariant, indicating that the dominant instability here comes from the linear term’s gauge dependence.

Amplification factors. Figure 13 converts the sweep into an explicit amplification ratio. Because PRISM’s intrinsic noise is gauge-invariant, the ratio inherits the V-shaped dependence of S(c): even benign reparameterizations that leave Zℓ unchanged can inflate factor-space intrinsic DP noise by large factors. This complements the training-time observation in Figure 1: during optimization, the implicit gauge chosen by the optimizer already yields a consistent > 1 amplification, and the controlled gauge sweep shows that, in principle, the same model state (same Zℓ) admits much larger effective intrinsic noise under factor-space DP. Together with Figure 3, these results empirically validate Issue II’s core claim: factor-space

<!-- Page 31 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

10−3 10−2 10−1 100 101 102 103

Gauge scale c in A →cA, B →c−1B

100

101

102

103

104

Intrinsic noise norm

Baseline linear (median) Baseline bilinear (median) PRISM (median)

c * ≈1.3 (empirical)

c * th ≈1.4

**Figure 12.** Gauge sweep at fixed Zℓ: intrinsic-noise medians with 10–90% band.

10−3 10−2 10−1 100 101 102 103

Gauge scale c in A →cA, B →c−1B

101

102

103

Factor

Amplification (Baseline/PRISM)

**Figure 13.** Gauge sweep: amplification factor (median baseline / median PRISM) vs. c.

DP produces gauge-dependent, potentially highly amplified intrinsic noise, while PRISM keeps the intrinsic DP noise scale controlled and gauge-invariant.

C.3. Additional Issue III diagnostics

Protocols. (Sigma sweep.) For Figures 4, 14 and 15, we sweep ϵ ∈{1.5, 3, 6, 12} at fixed (C, δ), run 120 optimizer steps, discard the first 10 steps as burn-in, and report means over the remaining steps. The x-axis uses the realized noise multiplier σ returned by the privacy engine. (Step-wise diagnostics.) For Figures 16 to 20, we run 300 steps at ϵ = 3 (hence σ ≈0.62 in this setup).

## Analysis

(raw noise scaling). For clipped DP-SGD-style noise, the injected intrinsic noise satisfies ξintr ∼N

0, (σC/b)2I

(up to the intrinsic parameterization), so E∥ξintr∥F should grow approximately linearly with σ at fixed clipping norm C and batch size b. Figure 14 matches this expectation for both methods, serving as a sanity check that (i) the privacy engine responds correctly to the ϵ sweep and (ii) our measurement pipeline is consistent. Notably, PRISM exhibits a larger raw intrinsic noise norm than factor-space DP-AdamW; this is expected because PRISM injects noise directly in the intrinsic update space, whereas factor-space perturbations are first applied to the LoRA factors and then mapped into the intrinsic update, which can reduce the resulting ∥ξintr∥F via the low-rank geometry.

## Analysis

(noise normalization + reduced amplification). Define the amplification factor a(σ) ≡ E

∥P−1/2ξintr∥F /∥ξintr∥F

, which isolates how much the preconditioner scales DP noise in Eq. (10). A key predic-

<!-- Page 32 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 Noise multiplier (σ)

101

2 × 101

3 × 101

4 × 101

6 × 101

Measured (μ ± σseed)

Baseline PRISM

**Figure 14.** Mean raw intrinsic DP noise ∥ξintr∥F vs. σ.

0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 Noise multiplier (σ)

102

Measured (μ ± σseed)

Baseline PRISM

**Figure 15.** Mean amplification ∥P−1/2ξ∥F /∥ξ∥F vs. σ.

tion of Issue III is noise normalization: when the second-moment estimator is dominated by DP noise, V ∝σ2 so (V + λI)−1/2 ∝1/σ, and the preconditioned noise becomes nearly σ-invariant (Prop. A.29). This is exactly what Figure 4 shows; combining it with the near-linear growth of raw noise in Figure 14 implies a(σ) should decrease roughly as 1/σ, which is what Figure 15 exhibits. Crucially, PRISM’s amplification is much smaller across σ (roughly 18–50 vs. 90–275 for DP-AdamW), supporting the claim that DP-aware floors (Eq. (26)) and the bound in Eq. (27) control worst-case scaling of DP noise under adaptive preconditioning.

## Analysis

(why amplification can be large). Figure 16 plots a “max scaling” proxy for preconditioning strength, roughly corresponding to the largest coordinate-wise scaling (e.g., maxi(bvi + ϵadam)−1/2 for Adam-like diagonals, and an operatornorm proxy for low-rank preconditioners). This quantity upper-bounds how much a preconditioner can magnify any input vector, and thus should track amplification of DP noise. DP-AdamW begins with extremely large aggressiveness (orders of magnitude larger than PRISM) and only gradually decays, which is consistent with Issue III: early noisy second-moment estimates can have very small entries/eigenvalues, yielding very large inverse-square-root scaling. PRISM stays in a much tighter range (tens to ∼100), consistent with explicitly enforcing a noise-calibrated floor (Eq. (26)), which prevents the smallest eigenvalues from collapsing and keeps the effective scaling bounded as suggested by Eq. (27).

## Analysis

(ill-conditioning in the low-rank core). Issue III also has a numerical face: when preconditioning is implemented through low-rank structure, stability is controlled by the smallest eigenvalues of the relevant Gram/second-moment objects. Let M denote the (measured) Gram proxy in the low-rank core; then ∥M−1/2∥2 = 1/ p λmin(M), so large values indicate severe ill-conditioning and stress both optimization and numerics. Figure 17 shows DP-AdamW exhibits substantially

<!-- Page 33 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

0 50 100 150 200 250 300 Update step

102

Max preconditioner scaling (proxy)

Baseline PRISM

**Figure 16.** Preconditioner aggressiveness (proxy) over training steps.

0 50 100 150 200 250 300 Update step

101 max 1/√λmin

Baseline PRISM

**Figure 17.** Low-rank numerics stress: max ∥M−1/2∥2 (Gram proxy).

higher stress (large inverse-square-root operator norms) throughout training, whereas PRISM remains in a low-stress regime. This supports the theoretical motivation behind DP-aware floors and condition-number control: by preventing near-singular directions in the low-rank core, PRISM reduces the regimes in which Eq. (27) would otherwise allow very large scaling (small effective λ).

## Analysis

(direct evidence for Issue III and PRISM mitigation). Figure 18 tracks the realized amplification ∥P−1/2 t ξt,intr∥F /∥ξt,intr∥F during training. Under adaptive preconditioning, this factor can be large when (i) the secondmoment (or Gram) has tiny eigenvalues and/or (ii) the preconditioner becomes overly aggressive, precisely the failure mode summarized by Issue III. Empirically, DP-AdamW sits near a large constant amplification (∼102) over the entire run, which explains why its effective update noise (after preconditioning) can remain large even when the raw intrinsic noise is comparatively small (Figure 14). PRISM’s amplification is materially smaller (tens rather than hundreds) and evolves smoothly, consistent with a preconditioner whose smallest eigenvalues are protected by noise-aware floors (Eq. (26)) and whose worst-case scaling is constrained in the sense of Eq. (27). Together with Figures 16 and 17, this plot provides direct empirical support that PRISM mitigates the amplification aspect of Issue III.

## Analysis

(mechanism: amplification is controlled by scaling). Figure 19 relates amplification to the max-scaling proxy. In general, for any linear preconditioner Hℓ, ∥Hℓξ∥/∥ξ∥concentrates between the singular values of Hℓ; Thus a max-scaling (operator-norm) proxy should strongly correlate with realized amplification. PRISM exhibits this expected monotonic relationship: as the preconditioner becomes more aggressive over training (larger x), the measured amplification (y) rises accordingly, and the color gradient shows this evolution over steps. DP-AdamW, in contrast, occupies a regime with much

<!-- Page 34 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

0 50 100 150 200 250 300 Update step

102

2 × 101

3 × 101

4 × 101

6 × 101

‖P−1/2ξ‖intr/‖ξ‖intr

Baseline PRISM

**Figure 18.** Amplification over training steps: ∥P−1/2ξ∥/∥ξ∥.

102

Preconditioner aggressiveness (max‖P−1/2‖, log)

102

2 × 101

3 × 101

4 × 101

6 × 101

Noise amplification (‖P−1/2ξ‖/‖ξ‖, log)

Baseline PRISM

50

100

150

200

250

300

Training step

**Figure 19.** Amplification vs. aggressiveness (color = step).

larger aggressiveness yet saturates at a high amplification level, suggesting the run spends most of its time near a hard constraint (e.g., clipping/conditioning caps) rather than smoothly trading off scaling. This plot supports the interpretation that PRISM’s improvements are driven by controlling the preconditioner’s effective scaling, exactly the control knob targeted by Eq. (26) and bounded by Eq. (27).

## Analysis

(mechanism: PRISM de-couples amplification from ill-conditioning). Figure 20 links amplification to low-rank ill-conditioning via the Gram proxy stress ∥M−1/2∥2. Without safeguards, increasing stress (smaller λmin(M)) would typically increase amplification because inverse-square-root operations magnify components in near-null directions. DP- AdamW concentrates in a high-stress regime, consistent with Figure 17, while maintaining a high amplification level. PRISM stays in a low-stress regime and, importantly, shows that when stress grows, amplification does not explode; rather, amplification can even decrease as safeguards activate (floors/clamps effectively reduce the preconditioner’s usable gain in ill-conditioned regimes). This is the intended behavior of Issue III mitigation: the algorithm should avoid coupling worst-case scaling to unstable low-rank directions, in line with the floor-based control in Eq. (26) and the bound in Eq. (27).

<!-- Page 35 -->

PRISM: Gauge-Invariant Tangent-Space Differentially Private LoRA

101

Low-rank stress (max‖M−1/2‖, log)

102

2 × 101

3 × 101

4 × 101

6 × 101

Noise amplification (‖P−1/2ξ‖/‖ξ‖, log)

Baseline PRISM

**Figure 20.** Amplification vs. low-rank stress (Gram proxy).
