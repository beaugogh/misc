---
title: "Enhancing DPSGD via Per-Sample Momentum and Low-Pass Filtering"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39951
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39951/43912
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Enhancing DPSGD via Per-Sample Momentum and Low-Pass Filtering

<!-- Page 1 -->

Enhancing DPSGD via Per-Sample Momentum and Low-Pass Filtering

Xincheng Xu1, Thilina Ranbaduge2, Qing Wang1, Thierry Rakotoarivelo2, David Smith2

1School of Computing, Australian National University, Australia 2Data 61, CSIRO, Australia {xincheng.xu, qing.wang}@anu.edu.au, {thilina.ranbaduge, thierry.rakotoarivelo, david.smith}@data61.csiro.au

## Abstract

Differentially Private Stochastic Gradient Descent (DPSGD) is widely used to train deep neural networks with formal privacy guarantees. However, the addition of differential privacy (DP) often degrades model accuracy by introducing both noise and bias. Existing techniques typically address only one of these issues, as reducing DP noise can exacerbate clipping bias and vice-versa. In this paper, we propose a novel method, DP-PMLF, which integrates per-sample momentum with a low-pass filtering strategy to simultaneously mitigate DP noise and clipping bias. Our approach uses per-sample momentum to smooth gradient estimates prior to clipping, thereby reducing sampling variance. It further employs a post-processing low-pass filter to attenuate highfrequency DP noise without consuming additional privacy budget. We provide a theoretical analysis demonstrating an improved convergence rate under rigorous DP guarantees, and our empirical evaluations reveal that DP-PMLF significantly enhances the privacy-utility trade-off compared to several state-of-the-art DPSGD variants.

Code — https://github.com/CharlieX001/DPPMLF Extended version — https://arxiv.org/abs/2511.08841

## Introduction

Deep learning has achieved remarkable success in various domains, such as medical diagnosis (Aggarwal et al. 2021; Chen et al. 2022), recommendation systems (Chen et al. 2023b; Fu, Niu, and Maher 2023), and autonomous driving (Bachute and Subhedar 2021). However, training deep models often requires large amounts of sensitive data, raising privacy concerns. Recent research has shown that trained models not only could reveal the presence of individuals in a dataset (Choquette-Choo et al. 2021; Olatunji, Nejdl, and Khosla 2021), but are also vulnerable to model inversion or reconstruction attacks (Zhao et al. 2021; Wang et al. 2021a; Nguyen et al. 2023).

Differential Privacy (DP) (Dwork, Roth et al. 2014) has become the de facto standard for privacy-preserving deep learning (Tanuwidjaja et al. 2020; Boulemtafes, Derhab, and Challal 2020), offering formal privacy guarantees for training data. Among various DP training algorithms, Differentially Private Stochastic Gradient Descent (DPSGD) (Abadi

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

et al. 2016) is widely used for training deep neural networks with privacy guarantees. DPSGD enforces (ϵ,δ)-DP through two key mechanisms: (1) gradient clipping, which bounds the ℓ2 norm of individual gradients to limit the influence of any single training sample, and (2) noise injection, where DP noise calibrated to the privacy budget ϵ and failure factor δ is added to the aggregated gradients. However, DPSGD faces a challenging privacy-utility trade-off: per-sample gradient clipping can impede convergence, and the added noise can significantly degrade model performance (Fang et al. 2023).

To improve the utility of DPSGD, recent works have proposed various strategies, such as adaptively adjusting the clipping threshold (Andrew et al. 2021; Bu et al. 2024; Xia et al. 2023), dynamically allocating the privacy budget (Lee and Kifer 2018; Yu et al. 2019; Chen et al. 2023a), projecting gradients into low-dimensional spaces (Zhou, Wu, and Banerjee 2021; Yu et al. 2021a; Asi et al. 2021; Yu et al. 2022), designing models less sensitive to DP noise (Papernot et al. 2021; Wang et al. 2021b; Shamsabadi and Papernot 2023), and incorporating public data (Li et al. 2022; Amid et al. 2022; Golatkar et al. 2022). Despite these advances, these methods face practical challenges: some lack rigorous theoretical guarantees, others are limited to specific model architectures, or require access to public data, all of which hinder the feasibility of DPSGD in real-world applications.

Beyond these practical challenges, a key theoretical concern is the convergence behavior of DPSGD, which is influenced by two factors: DP noise and clipping bias. Generally, selecting a smaller clipping threshold reduces injected DP noise, minimizing its scale but increasing the clipping bias. Conversely, a larger clipping threshold lowers clipping bias but requires injecting more DP noise to maintain privacy guarantees, which potentially leads to significant performance degradation.

Existing methods attempt to mitigate one effect at the expense of the other. Zhang et al. (Zhang et al. 2024a) applies a low-pass filter to separate DP noise from the true gradient signal, but introduces an additional bias term in the convergence rate. DiceSGD (Zhang et al. 2024b) utilizes an errorfeedback mechanism to correct bias but needs additional DP noise to protect the residual gradient information. Recent studies (Koloskova, Hendrikx, and Stich 2023; Xiao et al. 2023) suggest that clipping bias is not strictly related to clipping threshold, but is also influenced by sampling variance

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27341

<!-- Page 2 -->

σSGD. This insight inspired our work where we try to simultaneously reduce both DP noise and clipping bias, thereby enhancing the overall utility of DPSGD.

In this work, we propose a novel method, DP-PMLF, which mitigates both clipping bias and DP noise in DPSGD by integrating per-sample momentum and a low-pass filter. First, per-sample momentum is employed to average historical gradients, thereby reducing the sampling variance and bias introduced by gradient clipping. Second, a lowpass filter is applied as a post-processing step to suppress high-frequency DP noise while preserving the essential lowfrequency gradient signal. Our theoretical analysis illustrates an improved convergence guarantee compared to DPSGD under some assumptions, while providing strong privacy guarantees. Empirical results demonstrate our method outperforms resent state-of-the-art techniques. Our main contributions are threefold:

• We propose a novel DPSGD method that simultaneously addresses DP noise and clipping bias through the integration of per-sample momentum and low-pass filtering. To the best of our knowledge, our approach is the first to consider reducing the effect of DP noise and clipping bias simultaneously. • We theoretically prove DP-PMLF achieves faster convergence compared to the vanilla DPSGD, while maintaining a mathematically proven privacy guarantee. • Empirical results on different benchmarks demonstrate that our approach achieves a better privacy-utility tradeoff compared to various existing state-of-art DPSGD variants across different models and privacy levels.

## Related Work

Existing variants on DPSGD can be categorized into two directions: DP noise reduction and clipping bias reduction.

DP Noise Reduction: To mitigate the effect of DP noise, existing approaches commonly use the following techniques: adaptive clipping threshold (Andrew et al. 2021; Bu et al. 2024; Xia et al. 2023), privacy budget allocation (Lee and Kifer 2018; Yu et al. 2019; Chen et al. 2023a), low-rank projection (Zhou, Wu, and Banerjee 2021; Yu et al. 2021a,b; Asi et al. 2021; Yu et al. 2022), specific model design (Papernot et al. 2021; Wang et al. 2021b; Shamsabadi and Papernot 2023), public data assistant (Li et al. 2022; Amid et al. 2022; Golatkar et al. 2022).

However, these methods often lack theoretical guarantees, have limited applicability to specific model architectures, or require access to public data for training. To solve these limitations, Zhang et al. (Zhang et al. 2024a) proposed the introduction of a low-pass filter as a post-processing step in DP optimizers. They demonstrated that low-pass filtering effectively suppresses high-frequency DP noise while preserving essential gradient information.

Clipping Bias Reduction: Koloskova et al. (Koloskova, Hendrikx, and Stich 2023) demonstrated that DPSGD converges with a constant bias term, irrespective of the chosen clipping threshold or the learning rate. Chen et al. (Chen, Wu, and Hong 2020) also proposed a geometric analysis framework that quantifies gradient clipping bias by measuring the disparity between gradient distributions and symmetric distributions, and a technique to add Gaussian noise to gradients before the clipping operation when gradients are highly asymmetric.

Xiao et al. (Xiao et al. 2023) found that the clipping bias is proportional to the sampling variance σSGD. The authors proposed to reduce the clipping bias using inner-outer momentum, enhanced network normalization, batch clipping with public data, and data pre-processing. Zhang et al. (Zhang et al. 2024b) introduced an errorfeedback mechanism, DiceSGD, to accumulate the difference between clipped and unclipped gradients but requires more DP noise than vanilla DPSGD. To avoid clipping operation, Bethune et al. (B´ethune et al. 2024) proposed Clipless DPSGD. This method utilizes Lipschitz-constrained neural networks, which analytically compute gradient sensitivity bounds using projection operations and gradient normpreserving networks with orthogonal weights. However, Clipless DPSGD relies on specific model architectures which limit its practical deployment.

## Preliminaries

We begin by outlining the Empirical Risk Minimization (ERM) problem along with its standard assumptions, and then provide an overview of DP.

Empirical Risk Minimization (ERM):

In this paper, we focus on differentially private optimization developed within the Empirical Risk Minimization (ERM) framework, which forms the basis for supervised deep learning. Let D be a dataset of n samples, where each sample ξ is drawn from some underlying distribution. In empirical risk minimization (ERM), we seek a parameter vector x ∈Rd that minimizes the average loss:

min x∈Rd f(x) with f(x) = 1 n

X ξ∈D f(x, ξ), (1)

where f(x, ξ) is the loss incurred on sample ξ.

For clarity, we denote by ∇f (ξ)(x) ≡∇xf(x, ξ) the gradient with respect to x computed on a single sample ξ, ∥· ∥ denotes the Euclidean norm on Rd, and T denote the total number of iterations of the optimization algorithm. We then introduce the following assumptions used in our work:

Assumption 1 (L-Smoothness). A differentiable function f: Rd →R is said to be L-smooth if it satisfies, for all x, y ∈Rd:

∥∇f(x) −∇f(y)∥≤L∥x −y∥.

Assumption 2 (Bounded Variance). The per-sample gradient has bounded variance, i.e.,

E h

∥∇f (ξ)(x) −∇f(x)∥2i

≤σ2

SGD, ∀x ∈Rd.

Here, the expectation is taken with respect to the sampling of ξ and σSGD is a constant representing the variance bound.

27342

<!-- Page 3 -->

Assumption 3 (Bounded Gradient). The per-sample gradient has a bounded norm, i.e.,

∥∇f (ξ)(x)∥≤G, ∀x ∈Rd, ξ ∈D, where G is a positive constant. Assumption 4 (Gradient Auto-Correlation). For all t ∈ {0,..., T −1}, there exist sequences {cr} and {c−r} with cr ≥0, and ∀r ≥0, such that ⟨∇f(xt), ∇f(xt−r)⟩≥cr∥∇f(xt)∥2 + c−r∥∇f(xt−r)∥2.

Assumption 5 (Independent Sampling Noise). Let ζ(ξ)

i = ∇f (ξ)(xi) −∇f(xi) represent the sampling noise from the sample ξ in the i-th iteration. If i̸ = j, then the following condition holds:

E ζ(ξ)

i

T ζ(ξ)

j

= 0.

Assumption 1 is a widely adopted smoothness condition in non-convex optimization (Zaheer et al. 2018). Assumption 2 is standard in the analysis of gradient clipping (Gorbunov, Danilova, and Gasnikov 2020). Assumption 3 is commonly used in the DPSGD setting to control the additional bias introduced by clipping (Zhang et al. 2024b). Assumptions 4 and 5 are proposed and validated in (Zhang et al. 2024a) and (Xiao et al. 2023), respectively.

Differential Privacy (DP) DP (Dwork, Roth et al. 2014) provides a privacy guarantee such that the outputs of a mechanism cannot be distinguished by the inclusion or exclusion of any single record in a dataset. Formally, DP is defined as follows: Definition 1 (Differential Privacy (DP) (Dwork et al. 2006)). A randomized algorithm M: D →Rd is (ϵ, δ)-DP if for all neighboring datasets D and D′, and for any output set S ⊆Rd, we have

Pr[M(D) ∈S] ≤eϵPr[M(D′) ∈S] + δ, (2) where δ ∈[0, 1] denotes a failure probability.

When δ = 0, the mechanism M is said to satisfy pure DP; if δ > 0, it satisfies approximate DP.

The Gaussian mechanism is widely used to achieve the DP guarantee. The definition of global sensitivity and the Gaussian mechanism are defined as follows: Definition 2 (Global Sensitivity). Let H: D →Rd be a function that maps datasets to d-dimensional vectors. The global sensitivity of H is defined as:

∆H = max

D∼D′ ∥H(D) −H(D′)∥.

Definition 3 (Gaussian Mechanism (Dwork, Roth et al. 2014)). For a function H: D →Rd with ℓ2 global sensitivity ∆H, the Gaussian mechanism is defined as

M(D) = H(D) + N(0, σ2

DP Id), where N(0, σ2

DP Id) denotes the d-dimensional multivariate Gaussian distribution with mean zero and covariance matrix σ2

DP Id. The noise parameter is set to σDP = ∆H p

2 ln(1.25/δ) ϵ, which ensures that M satisfies (ϵ, δ)-DP.

0 20 40 60 80 100 Epoch

25

35

45

55

65

Test Accuracy (%)

LP-DPSGD DPSGD

(a) DPSGD and LP-DPSGD with ϵ = 8.

0 20 40 60 80 100 Epoch

20

25

30

35

40

Test Accuracy (%)

InnerOuter DPSGD

(b) DPSGD and InnerOuter with ϵ = 1.

**Figure 1.** Test accuracy (%) comparison of DPSGD and two existing methods on CIFAR-10 with a 5-Layer CNN over 100 epochs under different privacy budgets (ϵ).

Our approach is also built upon post-processing, one fundamental DP properties:

Lemma 1 (Post-Processing (Dwork et al. 2006)). Let M: D →Rd be an (ϵ, δ)-DP mechanism and let H: Rd → Rd be any deterministic or randomized function. Then the composition H ◦M satisfies (ϵ, δ)-DP.

Motivation

Reducing DP Noise. As mentioned in Section, different works have been proposed to mitigate the effects of DP noise. The state-of-the-art work by Zhang et al. (Zhang et al. 2024a), named LP-DPSGD, was proposed to preserve the integrity of the true gradient signals while mitigating the impact of DP noise. LP-DPSGD employs a low-pass filter to process gradients, effectively retaining low-frequency gradient signals while suppressing high-frequency noise, there by improving the signal-to-noise ratio of the gradients.

Although LP-DPSGD reduces the impact of DP noise, it introduces an increased bias as a trade-off. As shown by Koloskova et al. (Koloskova, Hendrikx, and Stich 2023), if the true gradient is sufficiently large, it can offset the sampling variance σSGD, thus preventing clipping bias. However, when incorporating a low-pass filter, this clipping bias cannot be eliminated, as the true gradients from different training iterations could be (negatively) correlated or even completely uncorrelated.

As can be seen in Figure 1 (a), the performance of LP- DPSGD is even worse than that of vanilla DPSGD. This is because the impact of clipping bias outweighs that of DP noise in this scenario. As a result, while LP-DPSGD effectively suppresses DP noise, the additional bias introduced by the low-pass filter undermines the overall performance. Further details on our analysis are provided in Section.

27343

<!-- Page 4 -->

Mitigating Clipping Bias. Xiao et al. (Xiao et al. 2023) found that the clipping bias term is proportional to the sampling variance σSGD. The authors proposed the DPSGD with Inner-Outer Momentum (abbreviated to InnerOuter for simplicity) approach as a way of reducing clipping bias. The inner momentum smooths the gradients at the sample level by averaging the gradients in the previous training iterations before clipping, effectively reducing the impact of sampling noise. The outer momentum aggregates the clipped gradients of all samples in a batch, adds DP noise, and applies a second round of smoothing at the batch level.

However, InnerOuter does not perform well when the DP noise is large. The accumulation of historical gradients through the outer momentum operation cannot separate the true gradient and DP noise signals. This accumulates more DP noise which leads to inaccurate gradient estimates in training iterations. As seen in Figure 1 (b), InnerOuter is not effective where DP noise dominates the signal. Furthermore, the authors did not provide theoretical proofs leaving Inner- Outer’s convergence insufficiently validated.

Our Proposed Approach

Now we provide details of DP-PMLF. Our approach is built on two complementary ideas. (1) Per-sample Momentum: By maintaining a momentum term for each sample, we average historical gradients over a window of k iterations. This per-sample momentum reduces sampling variance and mitigates clipping bias by smoothing out fluctuations before the clipping step. (2) Low-pass Filter: DP noise is evenly distributed among all frequency components, while true gradient signals concentrate in low frequencies. By applying a linear low-pass filter to the aggregated noisy momentum, we suppress high-frequency noise while preserving the true low-frequency components.

Together, these ideas balance the trade-off between reducing noise and controlling clipping bias. The per-sample momentum provides a more stable gradient estimate prior to clipping, and the low-pass filter further cleans the aggregated signal without consuming additional privacy budget.

Our proposed method is outlined in Algorithm 1. The algorithm proceeds as follows: Per-sample Momentum Calculation (lines 1 and 5): For each sample ξ, we compute a momentum term by averaging its gradients over the previous k iterations using exponential decay weights. The momentum term v(ξ)

t = t X i=t−k+1

ˆβ t−i∇f (ξ)(xi).

Here, ˆβ t−i = βt−i cβ and cβ = Pt i=t−k+1 βt−i. cβ is the normalization constant that ensures that the momentum coefficients sum to one, preventing excessive accumulation of DP noise. Momentum Clipping and Noise Addition (lines 6 and 8): Each sample’s momentum v(ξ)

t is clipped to a threshold C, which bounds the global sensitivity ˜v(ξ)

t = clip(v(ξ)

t, C). The aggregated momentum is then computed and Gaussian

## Algorithm

1: DP-PMLF

Require: dataset D, initial model parameters x0, learning rate η, momentum length k, filter parameters {ar}na r=1, {br}nb r=0, clipping threshold C, noise scale σDP, batch size B, iteration number T, per-sample momentum factor β 1: cβ = sum(Pt i=t−k+1 βt−i) 2: for t = 0 to T −1 do 3: Sample minibatch Bt of size B from D 4: for ξ ∈Bt do 5: v(ξ)

t = Pt i=t−k+1 ˆβt−i∇f (ξ)(xi), where ˆβt−i = βt−i cβ 6: ˜v(ξ)

t = clip(v(ξ)

t, C) 7: end for 8: ¯vt = 1 B

P ξ∈Bt ˜v(ξ)

t + wt, where wt ∼N(0, σ2

DP Id) 9: mt = −Pna r=1 armt−r + Pnb r=0 br¯vt−r 10: cb,t = 1, cm,t = −Pna r=1 arcm,t−r + Pnb r=0 brcb,t−r 11: ˆmt = mt/cm,t 12: xt+1 = xt −η ˆmt 13: end for 14: return xT noise with scale σDP is added to each dimension of the average clipped momentum to satisfy DP guarantees:

¯vt = 1

B

X ξ∈Bt

˜v(ξ)

t + wt, with wt ∼N(0, σ2

DP Id).

Low-pass Filtering and Bias Correction (lines 9 - 11): We apply a linear low-pass filter with coefficients {ar}na r=1 and {br}nb r=0 to the aggregated noisy momentum:

mt = − na X r=1 ar mt−r + nb X r=0 br ¯vt−r, where mt is the filtered output at time t, ¯vt−r represents the aggregated noisy momentum at time t −r, {ar} and {br} are the filter coefficients and na and nb determine the filter order. To ensure that after filtering the mean of the signal remains unchanged (Winder 2002), the design of the filter coefficients should satisfy the following constraint:

− na X r=1 ar + nb X r=0 br = 1. (3)

We calculate an initialization bias correction term via cm,t = − na X r=1 ar cm,t−r + nb X r=0 brcb,t−r.

We normalize mt to correct the initialization bias for the filter’s effect ˆmt = mt/cm,t. This step smooths the signal, suppressing high-frequency DP noise while retaining the low-frequency, true momentum components. Model Update (line 12): Finally, the model parameters are updated using the corrected momentum xt+1 = xt −η ˆmt.

Theoretical Analysis We now present key lemmas that underpin our convergence analysis.

27344

<!-- Page 5 -->

Lemma 2 (Effectiveness of Low-pass Filter).

ˆmt = t X r=0

ˆκr ¯vt−r, with

ˆκr = κr Pt r=0 κr and κr = min(nb,r) X r2=0 br2 na X r1=1 za,r1 (pa,r1)r−r2.

We begin by analyzing how the low-pass filter aggregates historical momentum information while attenuating highfrequency DP noise. This is crucial because, as shown in Section 3.3, the true gradient signal concentrates in the lowfrequency regime while DP noise is spectrally flat. Thus, the low-pass filter suppresses the high-frequency components, as indicated by the decay properties of {ˆκr}. The proof of this lemma is available in the appendix. Lemma 3 (Bounded Momentum Variance). Under Assumptions 1, 2, and 5, if the step size satisfies η ≤ s σ2

SGD L2k3(C2 + dσ2

DP), then

E h

∥v(ξ)

t −∇f(xt)∥2i

≤O σ2

SGD ρ2

, where ρ = s

(1 + β)(1 −βk) (1 −β)(1 + βk).

Proof Sketch. We decompose the error into the variance of the sampling noise E

∥∇f (ξ)(xi) −∇f(xi)∥2

, and the error due to the drift between ∇f(xi) and ∇f(xt). The former is directly controlled by Assumption 2 and the independence in Assumption 5, while the latter is bounded via the L-smoothness condition (Assumption 1). The weighted averaging in the per-sample momentum reduces the overall variance by the factor ρ2. Detailed derivations are provided in the appendix. □ Remark. The factor ρ2 increases with both the per-sample momentum factor β and the momentum length k. When β reaches its maximum value of 1, the exponential decay reduces to an equal-weight average, and ρ2 approaches k. Theoretically, larger values of β and k are preferable; however, in practice, a large β may cause training to rely overly on historical information, potentially slowing convergence. Convergence Analysis We now combine the above lemmas to establish the convergence rate of Algorithm 1. The analysis builds on a standard descent lemma for L-smooth functions and is augmented by our representation of the low-pass filtered momentum and the variance reduction effect. Step 1: Descent Lemma. By L-smoothness from Assumption 1, we have

E [f(xt+1) −f(xt)] ≤−η E [⟨∇f(xt), ˆmt⟩]+ Lη2

2 E

∥ˆmt∥2

.

Step 2: Decomposition of Gradient. Using the representation from Lemma 2, we write

⟨∇f(xt), ˆmt⟩= t X r=0

ˆκr ⟨∇f(xt), ¯vt−r⟩.

We decompose each inner product into two parts:

## 1 The correlation between the current gradient and the historical (unclipped) momentum, which under

Assumption 4 can be bounded in terms of ∥∇f(xt)∥2 and ∥∇f(xt−r)∥2. 2. A bias term arising from clipping, i.e., the difference E[˜v(ξ)

t−r −v(ξ)

t−r], which is bounded by O

G + σSGD ρ using Assumption 3 and Lemma 3. Step 3: Final Convergence Bound. After careful estimation of the descent term and the term E

∥ˆmt∥2

(which also incorporates the effect of the DP noise with variance d σ2

DP), telescoping over T iterations and taking averages yields the following convergence guarantee: Theorem 1 (Convergence Bound). Under Assumptions 1–5, if Algorithm 1 is running for T iterations with step size η ≤ s σ2

SGD L2k3(C2 + d σ2

DP), then E

∥∇f(xt)∥2 is upper bounded by

O f(x0) −f ∗ ηT + LηC2 + Lη ΓDP d σ2

DP +

G2

ΓSGD

+ σ2

SGD ρ2 ΓSGD

!!

, where ˆcr = Pt−r i=t−r−k+1 ˆβt−r−ict−i, ρ = q

(1+β)(1−βk) (1−β)(1+βk), and f ∗ = minxf(x). ΓDP =

PT −1 t=0

Pt r=0 ˆκrˆcr PT −1 t=0

Pt r=0 ˆκ2 r and

ΓSGD =

PT −1 t=0

Pt r=0 ˆκrˆcr PT −1 t=0

Pt r=0

ˆκr ˆcr are two ratios introduce by low- pass filtering. Remark. The first term represents the optimization error decreasing with the number of iterations. The second term LηC2 reflects the error introduced by gradient clipping. The third term captures the impact of the DP noise, where the aggregated effect is modulated by the filter coefficients. The final term aggregates the residual bias due to low-pass filtering and the reduced clipping bias from per-sample momentum. Our approach reduces the clipping bias term by introducing the variance reduction factor ρ. Corollary 1. If the per-sample gradient norm is bounded by G = O σSGD ρ

, then the bound in Theorem 1 simplifies to

O f(x0) −f ∗ ηT + LηC2 + Lη d σ2

DP ΓDP

+ σ2

SGD ρ2 ΓSGD

.

Remark. A careful inspection of our convergence bound reveals that, by choosing β, k, and low-pass filter coefficients appropriately, our approach reduces the clipping bias term by introducing the variance reduction factor ρ and mitigates the effect of DP noise via the low-pass filter compared to vanilla DPSGD (Abadi et al. 2016). Privacy Analysis We establish that our approach satisfies (ϵ, δ)-differential privacy. Theorem 2 (Differential Privacy Guarantee). There exist absolute constants c1 and c2 such that, given sampling probability q = B/n and T iterations, for any ϵ < c1q2T, Algorithm 1 is (ϵ, δ)-differentially private for any δ > 0 if the noise scale (σDP) satisfies σDP ≥c2 q p

T log(1/δ)

ϵ.

27345

<!-- Page 6 -->

## Method

MNIST Fashion-MNIST CIFAR-10 CIFAR-100 ϵ=1 ϵ=8 ϵ=1 ϵ=8 ϵ=1 ϵ=8 ϵ=1 ϵ=8 DPSGD 89.00 ± 0.06 88.95 ± 0.01 78.96 ± 0.05 79.04 ± 0.04 35.74 ± 0.26 47.74 ± 1.20 7.52 ± 0.49 18.27 ± 0.48 LP-DPSGD 88.99 ± 0.06 88.96 ± 0.01 79.03 ± 0.10 79.02 ± 0.10 35.84 ± 0.63 48.37 ± 0.36 7.55 ± 0.26 18.52 ± 0.27 InnerOuter 92.15 ± 0.15 92.43 ± 0.06 80.50 ±2.28 81.18 ± 1.56 11.55 ± 1.07 33.53 ± 0.52 1.13 ± 0.20 13.93 ± 0.40 DP-PMLF 92.16 ± 0.05 92.39 ± 0.07 80.65 ± 1.17 81.93 ± 0.83 40.96 ± 1.18 51.47 ± 0.33 11.40 ± 0.21 23.15 ± 0.52

**Table 1.** Test accuracy (%) comparison across datasets on ViT with fixed epoch (Epoch = 25 for MNIST and Fashion-MNIST, Epoch = 50 for CIFAR-10 and CIFAR-100) and different privacy budgets ϵ = 1 and 8.

0 50 100 Epoch

10

20

30

40

50

60

Test Accuracy (%)

(a) CNN-5

0 50 100 Epoch

0

10

20

30

40

50

(b) ResNet-18

0 50 100 Epoch

0

10

20

30

40

50

(c) ViT

DP-PMLF InnerOuter LP-DPSGD DPSGD

**Figure 2.** Test accuracy (%) comparison across different models on CIFAR-10 with fixed privacy budget ϵ = 1.

Proof. Let D and D′ be any two neighbouring datasets where D′ contains exactly one additional sample ξ compared to D. The global sensitivity of the clipped persample momentum satisfies ∥clip(v(ξ)

t, C)∥≤C. Thus, by utilizing the Gaussian mechanism in Definition 3 and privacy amplification by subsampling (Balle, Barthe, and Gaboardi 2018), ¯vt in each training iteration is protected by (O(q/σDP), δ/T)-DP. Given that the subsequent low-pass filter is applied as a post-processing step (Lemma 1) in each training iteration, ˆmt is also protected by (O(q/σDP), δ/T)-DP. The moments accountant method (Abadi et al. 2016) then implies that, over T iterations, the overall privacy guarantee is (ϵ, δ)-DP provided if the stated condition on σDP holds.

## Experiments

Next we evaluate DP-PMLF through comprehensive experiments. Due to page limitation, details of the experimental setting and additional results are given in the appendix.

## Experiment

Setting

Dataset. We evaluate our approach on four image classification datasets, including MNIST (Deng 2012), Fashion-MNIST (Xiao, Rasul, and Vollgraf 2017), CIFAR-10 (Krizhevsky and Hinton 2009), and CIFAR- 100 (Krizhevsky and Hinton 2009), and four sentence classification datasets, including MNLI, QNLI, QQP, and SST-2 from the GLUE benchmark (Wang et al. 2018). Baselines. We compare the test accuracy of DP-PMLF with vanilla DPSGD (Abadi et al. 2016) and two state-of-the-art methods introduced in Section: LP-DPSGD (Zhang et al. 2024a) and InnerOuter (Xiao et al. 2023).

Models. We utilized three models for image classification tasks: a 5-layer CNN (Zhang et al. 2024a), ResNet-18 (He et al. 2016), and the Vision Transformer (ViT) (Dosovitskiy et al. 2021). These models are initialized with random weights without pretraining. For sentence classification tasks, we fine-tune a pre-trained RoBERTa-base model (Liu et al. 2019). Hyper-parameters. The parameter choices are detailed in the appendix and based on settings commonly used in the literature. All experiments are repeated five times, with the mean and standard deviation reported.

Privacy-Utility Trade-off Image Classification We compare the performance of our method against baselines across different models and datasets with varying privacy budgets ϵ. We report the test accuracy for ϵ = 1 and ϵ = 8 for the ViT model in Table 1. As can be seen, DP-PMLF maintains its leading performance. For instance, on Fashion-MNIST, it achieves accuracies of about 80.65% at ϵ = 1 and 81.93% at ϵ = 8. On CIFAR-100, our approach maintains a 4–5% margin over the next-best baselines across both privacy budgets.

Under a high DP noise regime (ϵ = 1), as shown in Table 1, the InnerOuter method shows a degradation in performance. This is because the InnerOuter method lacks normalization and suffers from excessive noise accumulation. In contrast, DP-PMLF utilizes both normalization and a lowpass filter allowing our approach to better control and filter DP noise, thereby achieving superior results.

**Figure 2.** presents the test accuracy on CIFAR-10 under ϵ = 1 for three model architectures: CNN-5, Resnet-18, and ViT. In all cases, DP-PMLF consistently surpasses the baseline methods. For example, with CNN-5, DP-PMLF attains

27346

<!-- Page 7 -->

## Method

MNLI QNLI QQP SST-2 ϵ=1 ϵ=8 ϵ=1 ϵ=8 ϵ=1 ϵ=8 ϵ=1 ϵ=8 DPSGD 51.36 ± 0.66 72.00 ± 0.23 65.59 ± 0.66 85.47 ± 0.78 71.20 ± 0.97 80.38 ± 0.37 76.19 ± 1.15 90.83 ± 0.38 LP-DPSGD 52.75 ± 0.62 71.48 ± 0.23 66.34 ± 0.94 85.44 ± 0.45 71.61 ± 0.71 80.55 ± 0.40 76.46 ± 0.24 89.24 ± 0.66 InnerOuter 48.45 ± 0.89 70.35 ± 0.38 69.46 ± 0.87 86.07 ± 0.58 70.27 ± 0.64 83.18 ± 0.34 76.49 ± 0.63 89.08 ± 0.43 DP-PMLF 56.81 ± 0.74 75.56 ± 0.42 72.38 ± 0.62 86.96 ± 0.69 75.55 ± 1.16 83.42 ± 0.52 78.07 ± 0.96 90.39 ± 1.03

**Table 2.** Test accuracy (%) comparison across GLUE benchmark subsets with different privacy budgets ϵ = 1, 8.

1 2 3 4 5 6 8 Privacy Budget

88

89

90

91

92

93

Test Accuracy (%)

(a) MNIST (CNN-5)

1 2 3 4 5 6 8 Privacy Budget

88

89

90

91

92

93

(b) MNIST (ResNet-18)

1 2 3 4 5 6 8 Privacy Budget

45

50

55

60

65

70

(c) CIFAR-10 (CNN-5)

1 2 3 4 5 6 8 Privacy Budget

40

45

50

55

60

65

(d) CIFAR-10 (ResNet-18)

DP-PMLF DP-PMLF (w/o PM) DP-PMLF (w/o LF)

**Figure 3.** Test accuracy (%) for DP-PMLF and its two variants, which are DP-PMLF without Per-sample Momentum (DP- PMLF (w/o PM)) and DP-PMLF without Low-pass Filter (DP-PMLF (w/o LF)).

approximately 47% accuracy, exceeding the best baseline by around 9%. Similarly, with ResNet-18, DP-PMLF reaches nearly 50%, which is 1–2% higher than the strongest competitor. Finally, when using ViT, DP-PMLF achieves about 31% accuracy, compared to only 23% for the best baseline.

Sentence Classification To further assess the performance of our approach, we extend our evaluation to sentence classification tasks using four datasets from the GLUE benchmark, with results presented in Table 2. These experiments further demonstrate the effectiveness of DP-PMLF, which consistently shows a significant performance improvement over other baselines. When ϵ = 1, our method surpasses the baselines by over 4% on MNLI and nearly 3% on QNLI. Although the performance gap decreases under a more relaxed privacy budget of ϵ = 8, DP-PMLF still outperforms or remains highly competitive with the baseline methods. These results show the effectiveness of our approach for sentence classification tasks in a differential privacy setting.

Ablation Studies

We evaluated on two core components of DP-PMLF: persample momentum and the low-pass filter. Specifically, we denote DP-PMLF without per-sample momentum as DP- PMLF (w/o PM) and DP-PMLF without the low-pass filter as DP-PMLF (w/o LF). We used MNIST and CIFAR-10 on the CNN-5 and Resnet-18 models with different privacy budget (ϵ) values ranging from 1 to 8. Figure 3 shows that DP-PMLF consistently outperforms DP-PMLF (w/o PM) for different ϵ values. This is because per-sample momentum effectively reduces clipping bias and thus narrows the neighborhood around the optimal convergence point.

Further, compared to DP-PMLF (w/o LF), our approach exhibits superior performance on MNIST by leveraging historical gradients. This refines the gradient descent direction and potentially accelerates convergence. For CIFAR-10, we adopt more complicated filter coefficients to enhance gradient signal smoothing and mitigate DP noise. This is advantageous when DP noise is large, e.g., when ϵ ≤6. However, when DP noise is relatively small (ϵ > 6), excessive smoothing may lead to the loss of true gradient information, causing DP-PMLF to perform slightly worse than DP-PMLF (w/o LF). This is evident in Figure 3(c) where our approach is achieving approximately 0.5–0.7% less test accuracy than DP-PMLF (w/o LF) when ϵ > 6.

## Conclusion and Future Work

In this work, we propose a novel DPSGD variant that incorporates per-sample momentum and a low-pass filter to simultaneously reduce the effect of DP noise and clipping bias. We provide a theoretical proof of an improved convergence rate associated with a formal DP guarantee. Our experimental results show that our approach achieves higher utility in image and sentence classifications compared to the state-of-the-art DPSGD variants. In future work, we will investigate how to analyze our approach under some general assumptions such as non-convex Polyak-Łojasiewicz conditions (Karimi, Nutini, and Schmidt 2016), and (L0, L1)smoothness (Zhang et al. 2020). Furthermore, we will develop an adaptive method to optimize the selection of the hyper-parameters in per-sample momentum and low-pass filtering. Finally, we will investigate how to apply this method to different domain applications, such as natural language processing tasks and reinforcement learning.

27347

<!-- Page 8 -->

## Acknowledgments

This research is supported by CSIRO Data61 Scholarship Program.

## References

Abadi, M.; Chu, A.; Goodfellow, I.; McMahan, H. B.; Mironov, I.; Talwar, K.; and Zhang, L. 2016. Deep Learning with Differential Privacy. In SIGSAC Conference on Computer and Communications Security, CCS ’16, 308–318. New York, NY, USA: Association for Computing Machinery. ISBN 9781450341394. Aggarwal, R.; Sounderajah, V.; Martin, G.; Ting, D. S.; Karthikesalingam, A.; King, D.; Ashrafian, H.; and Darzi, A. 2021. Diagnostic accuracy of deep learning in medical imaging: a systematic review and meta-analysis. NPJ digital medicine, 4(1): 65. Amid, E.; Ganesh, A.; Mathews, R.; Ramaswamy, S.; Song, S.; Steinke, T.; Suriyakumar, V. M.; Thakkar, O.; and Thakurta, A. 2022. Public Data-Assisted Mirror Descent for Private Model Training. In Chaudhuri, K.; Jegelka, S.; Song, L.; Szepesv´ari, C.; Niu, G.; and Sabato, S., eds., International Conference on Machine Learning (ICML), volume 162 of Proceedings of Machine Learning Research, 517– 535. Baltimore, Maryland, USA: PMLR. Andrew, G.; Thakkar, O.; McMahan, B.; and Ramaswamy, S. 2021. Differentially private learning with adaptive clipping. Advances in Neural Information Processing Systems, 34: 17455–17466. Asi, H.; Duchi, J.; Fallah, A.; Javidbakht, O.; and Talwar, K. 2021. Private adaptive gradient methods for convex optimization. In International Conference on Machine Learning, 383–392. PMLR, Virtual: PMLR. Bachute, M. R.; and Subhedar, J. M. 2021. Autonomous driving architectures: insights of machine learning and deep learning algorithms. Machine Learning with Applications, 6: 100164. Balle, B.; Barthe, G.; and Gaboardi, M. 2018. Privacy amplification by subsampling: Tight analyses via couplings and divergences. Advances in neural information processing systems, 31. B´ethune, L.; Massena, T.; Boissin, T.; Bellet, A.; Mamalet, F.; Prudent, Y.; Friedrich, C.; Serrurier, M.; and Vigouroux, D. 2024. DP-SGD Without Clipping: The Lipschitz Neural Network Way. In International Conference on Learning Representations (ICLR). Vienna, Austria: ICLR. Boulemtafes, A.; Derhab, A.; and Challal, Y. 2020. A review of privacy-preserving techniques for deep learning. Neurocomputing, 384: 21–45. Bu, Z.; Wang, Y.-X.; Zha, S.; and Karypis, G. 2024. Automatic clipping: Differentially private deep learning made easier and stronger. Advances in Neural Information Processing Systems, 36. Chen, L.; Yue, D.; Ding, X.; Wang, Z.; Choo, K.-K. R.; and Jin, H. 2023a. Differentially private deep learning with dynamic privacy budget allocation and adaptive optimization. IEEE Transactions on Information Forensics and Security, 18(1): 4422–4435.

Chen, X.; Wang, X.; Zhang, K.; Fung, K.-M.; Thai, T. C.; Moore, K.; Mannel, R. S.; Liu, H.; Zheng, B.; and Qiu, Y. 2022. Recent advances and clinical applications of deep learning in medical image analysis. Medical image analysis, 79: 102444. Chen, X.; Wu, S. Z.; and Hong, M. 2020. Understanding gradient clipping in private sgd: A geometric perspective. Advances in Neural Information Processing Systems, 33: 13773–13782. Chen, X.; Yao, L.; McAuley, J.; Zhou, G.; and Wang, X. 2023b. Deep reinforcement learning in recommender systems: A survey and new perspectives. Knowledge-Based Systems, 264: 110335. Choquette-Choo, C. A.; Tramer, F.; Carlini, N.; and Papernot, N. 2021. Label-only membership inference attacks. In International conference on machine learning, 1964–1974. PMLR, Virtual: PMLR. Deng, L. 2012. The mnist database of handwritten digit images for machine learning research [best of the web]. IEEE signal processing magazine, 29(6): 141–142. Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; Weissenborn, D.; Zhai, X.; Unterthiner, T.; Dehghani, M.; Minderer, M.; Heigold, G.; Gelly, S.; Uszkoreit, J.; and Houlsby, N. 2021. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. In International Conference on Learning Representations. Dwork, C.; Kenthapadi, K.; McSherry, F.; Mironov, I.; and Naor, M. 2006. Our data, ourselves: Privacy via distributed noise generation. In International Conference on the Theory and Applications of Cryptographic Techniques, 486– 503. Lyon, France: Springer. Dwork, C.; Roth, A.; et al. 2014. The algorithmic foundations of differential privacy. Foundations and Trends® in Theoretical Computer Science, 9(3–4): 211–407. Fang, H.; Li, X.; Fan, C.; and Li, P. 2023. Improved convergence of differential private sgd with gradient clipping. In The Eleventh International Conference on Learning Representations. Fu, Z.; Niu, X.; and Maher, M. L. 2023. Deep learning models for serendipity recommendations: a survey and new perspectives. ACM Computing Surveys, 56(1): 1–26. Golatkar, A.; Achille, A.; Wang, Y.-X.; Roth, A.; Kearns, M.; and Soatto, S. 2022. Mixed differential privacy in computer vision. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 8376–8386. Louisiana, USA: IEEE. Gorbunov, E.; Danilova, M.; and Gasnikov, A. 2020. Stochastic optimization with heavy-tailed noise via accelerated gradient clipping. Advances in Neural Information Processing Systems, 33: 15042–15053. He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, 770–778. Karimi, H.; Nutini, J.; and Schmidt, M. 2016. Linear convergence of gradient and proximal-gradient methods under the

27348

<!-- Page 9 -->

polyak-łojasiewicz condition. In Joint European conference on machine learning and knowledge discovery in databases, 795–811. Springer. Koloskova, A.; Hendrikx, H.; and Stich, S. U. 2023. Revisiting Gradient Clipping: Stochastic bias and tight convergence guarantees. In International Conference on Machine Learning, 17343–17363. PMLR, Hawai: PMLR. Krizhevsky, A.; and Hinton, G. 2009. Learning multiple layers of features from tiny images. Technical Report 0, University of Toronto, Toronto, Ontario. Lee, J.; and Kifer, D. 2018. Concentrated differentially private gradient descent with adaptive per-iteration privacy budget. In SIGKDD International Conference on Knowledge Discovery & Data Mining, 1656–1665. London, UK: ACM. Li, T.; Zaheer, M.; Reddi, S.; and Smith, V. 2022. Private adaptive optimization with side information. In International Conference on Machine Learning, 13086–13105. PMLR, Hawai: PMLR. Liu, Y.; Ott, M.; Goyal, N.; Du, J.; Joshi, M.; Chen, D.; Levy, O.; Lewis, M.; Zettlemoyer, L.; and Stoyanov, V. 2019. RoBERTa: A Robustly Optimized BERT Pretraining Approach. CoRR, abs/1907.11692. Nguyen, N.-B.; Chandrasegaran, K.; Abdollahzadeh, M.; and Cheung, N.-M. 2023. Re-thinking model inversion attacks against deep neural networks. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 16384– 16393. Vancouver, Canada: IEEE. Olatunji, I. E.; Nejdl, W.; and Khosla, M. 2021. Membership inference attack on graph neural networks. In International Conference on Trust, Privacy and Security in Intelligent Systems and Applications (TPS-ISA), 11–20. IEEE, Virtual: IEEE. Papernot, N.; Thakurta, A.; Song, S.; Chien, S.; and Erlingsson, ´U. 2021. Tempered sigmoid activations for deep learning with differential privacy. In the AAAI Conference on Artificial Intelligence, 9312–9321. Virtual: AAAI. Shamsabadi, A. S.; and Papernot, N. 2023. Losing less: A loss for differentially private deep learning. In Privacy Enhancing Technologies (PETs), 307–320. Lausanne, Switzerland: PoPETs. Tanuwidjaja, H. C.; Choi, R.; Baek, S.; and Kim, K. 2020. Privacy-preserving deep learning on machine learning as a service—a comprehensive survey. IEEE Access, 8: 167425– 167447. Wang, A.; Singh, A.; Michael, J.; Hill, F.; Levy, O.; and Bowman, S. R. 2018. GLUE: A multi-task benchmark and analysis platform for natural language understanding. arXiv preprint arXiv:1804.07461. Wang, K.-C.; Fu, Y.; Li, K.; Khisti, A.; Zemel, R.; and Makhzani, A. 2021a. Variational model inversion attacks. Advances in Neural Information Processing Systems, 34: 9706–9719. Wang, W.; Wang, T.; Wang, L.; Luo, N.; Zhou, P.; Song, D.; and Jia, R. 2021b. DPlis: Boosting Utility of Differentially Private Deep Learning via Randomized Smoothing. Privacy Enhancing Technology, 2021(4): 163–183.

Winder, S. 2002. Analog and digital filter design. Elsevier. Xia, T.; Shen, S.; Yao, S.; Fu, X.; Xu, K.; Xu, X.; and Fu, X. 2023. Differentially private learning with per-sample adaptive clipping. In the AAAI Conference on Artificial Intelligence, volume 37, 10444–10452. Washington, DC, USA: AAAI. Xiao, H.; Rasul, K.; and Vollgraf, R. 2017. Fashion-mnist: a novel image dataset for benchmarking machine learning algorithms. arXiv preprint arXiv:1708.07747, 1–6. Xiao, H.; Xiang, Z.; Wang, D.; and Devadas, S. 2023. A theory to instruct differentially-private learning via clipping bias reduction. In IEEE Symposium on Security and Privacy (SP), 2170–2189. IEEE, San Francisco, CA, USA: IEEE. Yu, D.; Naik, S.; Backurs, A.; Gopi, S.; Inan, H. A.; Kamath, G.; Kulkarni, J.; Lee, Y. T.; Manoel, A.; Wutschitz, L.; Yekhanin, S.; and Zhang, H. 2022. Differentially Private Fine-tuning of Language Models. In International Conference on Learning Representations (ICLR). Virtual: ICLR. Yu, D.; Zhang, H.; Chen, W.; and Liu, T. 2021a. Do not Let Privacy Overbill Utility: Gradient Embedding Perturbation for Private Learning. In International Conference on Learning Representations (ICLR). Virtual: ICLR. Yu, D.; Zhang, H.; Chen, W.; Yin, J.; and Liu, T.-Y. 2021b. Large scale private learning via low-rank reparametrization. In International Conference on Machine Learning, 12208– 12218. PMLR, Virtual: PMLR. Yu, L.; Liu, L.; Pu, C.; Gursoy, M. E.; and Truex, S. 2019. Differentially private model publishing for deep learning. In IEEE symposium on security and privacy (SP), 332–349. IEEE, San Francisco, CA, USA: IEEE. Zaheer, M.; Reddi, S.; Sachan, D.; Kale, S.; and Kumar, S. 2018. Adaptive methods for nonconvex optimization. Advances in neural information processing systems, 31. Zhang, J.; He, T.; Sra, S.; and Jadbabaie, A. 2020. Why Gradient Clipping Accelerates Training: A Theoretical Justification for Adaptivity. In International Conference on Learning Representations (ICLR), 1–12. Virtual: ICLR. Zhang, X.; Bu, Z.; Hong, M.; and Razaviyayn, M. 2024a. DOPPLER: Differentially Private Optimizers with Lowpass Filter for Privacy Noise Reduction. In Globersons, A.; Mackey, L.; Belgrave, D.; Fan, A.; Paquet, U.; Tomczak, J. M.; and Zhang, C., eds., Annual Conference on Neural Information Processing Systems (NeurIPS), 1–26. Vancouver, BC, Canada: Curran Associates. Zhang, X.; Bu, Z.; Wu, S.; and Hong, M. 2024b. Differentially Private SGD Without Clipping Bias: An Error- Feedback Approach. In International Conference on Learning Representations (ICLR), 1–27. Vienna, Austria: ICLR. Zhao, X.; Zhang, W.; Xiao, X.; and Lim, B. 2021. Exploiting explanations for model inversion attacks. In IEEE/CVF international conference on computer vision, 682–692. Montreal, BC, Canada: IEEE. Zhou, Y.; Wu, S.; and Banerjee, A. 2021. Bypassing the Ambient Dimension: Private SGD with Gradient Subspace Identification. In International Conference on Learning Representations (ICLR), 1–28. Virtual: ICLR.

27349
