---
title: "Improving the Convergence Rate of Ray Search Optimization for Query-Efficient Hard-Label Attacks"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38127
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38127/42089
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Improving the Convergence Rate of Ray Search Optimization for Query-Efficient Hard-Label Attacks

<!-- Page 1 -->

Improving the Convergence Rate of Ray Search Optimization for

Query-Efficient Hard-Label Attacks

Xinjie Xu1, Shuyu Cheng2, Dongwei Xu1, Qi Xuan1,3, Chen Ma1,3*

1Institute of Cyberspace Security, Zhejiang University of Technology, Hangzhou 310023, China 2JQ Investments, Shanghai 200122, China 3Binjiang Institute of Artificial Intelligence, ZJUT, Hangzhou 310056, China xxj1018@foxmail.com, csy530216@126.com, {dongweixu, xuanqi, machen}@zjut.edu.cn

## Abstract

In hard-label black-box adversarial attacks, where only the top-1 predicted label is accessible, the prohibitive query complexity poses a major obstacle to practical deployment. In this paper, we focus on optimizing a representative class of attacks that search for the optimal ray direction yielding the minimum ℓ2-norm perturbation required to move a benign image into the adversarial region. Inspired by Nesterov’s Accelerated Gradient (NAG), we propose a momentum-based algorithm, ARS-OPT, which proactively estimates the gradient with respect to a future ray direction inferred from accumulated momentum. We provide a theoretical analysis of its convergence behavior, showing that ARS-OPT enables more accurate directional updates and achieves faster, more stable optimization. To further accelerate convergence, we incorporate surrogatemodel priors into ARS-OPT’s gradient estimation, resulting in PARS-OPT with enhanced performance. The superiority of our approach is supported by theoretical guarantees under standard assumptions. Extensive experiments on ImageNet and CIFAR-10 demonstrate that our method surpasses 13 state-ofthe-art approaches in query efficiency.

Code — https://github.com/machanic/hard_label_attacks Extended version — https://arxiv.org/abs/2512.21241

## Introduction

We focus on hard-label adversarial attacks. Considered among the most practical and challenging black-box attacks, hard-label attacks operate under strict information constraints. While white-box attacks (Goodfellow, Shlens, and Szegedy 2015; Madry et al. 2018) leverage model parameters and gradients, and score-based attacks (Ma, Chen, and Yong 2021) exploit confidence scores, hard-label attacks rely solely on top-1 predicted labels. This makes the efficient generation of adversarial examples substantially more difficult while enhancing their practical applicability.

Why study query-based black-box adversarial attacks under the hard-label setting? Real-world machine-learning services such as cloud vision APIs and biometric recognizers often reveal nothing more than the final predicted decision (i.e., the top-1 label) to external users. With gradients and

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

confidence scores stripped away, an attacker is forced to treat the model as a hard-label black box to probe its decision boundary. This stringent setting accurately reflects the limited feedback of deployed services and raises three key challenges. (1) Minimal feedback: Each query yields only a hardlabel response, demanding efficient exploration strategies. (2) Practical relevance: It closely mirrors restricted commercial platforms where probability scores and internal details are deliberately hidden. (3) Security-critical: Hard-label attacks reveal vulnerabilities in “security-through-obscurity” systems and underscore the urgent need for defenses against adversaries with minimal information. Consequently, designing query-efficient attacks based solely on hard-label feedback is essential for vulnerability assessment and robust defenses.

Why are hard-label attacks challenging? Because a model’s predicted label typically changes only when an input moves across or near its decision boundary, hard-label attacks must restrict their search to this narrow region, making the optimization especially challenging. Early hard-label attacks like Boundary Attack (BA) (Brendel, Rauber, and Bethge 2018) and Biased BA (Brunner et al. 2019) initialize from a sample already in the adversarial region and progressively reduce the perturbation by stepping toward the original image while exploring directions on the decision boundary via randomly sampled spherical vectors. However, these approaches remain highly inefficient in terms of query cost: they rely almost entirely on random sampling and neglect valuable information from past queries, which impedes effective perturbation reduction. To address this challenge, recent studies have adopted zeroth-order (ZO) optimization techniques, which leverage boundary information more effectively to identify adversarial examples. Existing ZO-based attacks—such as HopSkipJumpAttack (HSJA) (Chen, Jordan, and Wainwright 2020), OPT (Cheng et al. 2019), Sign- OPT (Cheng et al. 2020), and Prior-OPT (Ma et al. 2025)— primarily focus on improving gradient estimation through finite differences. However, their optimization strategies rely on vanilla gradient descent, overlooking well-established acceleration methods such as momentum and Nesterov’s accelerated gradient, which can enhance convergence rates even when the gradient estimation quality remains unchanged. To address these limitations, we propose ARS-OPT, a novel ZO optimization algorithm incorporating accelerated random search (ARS) (Nesterov and Spokoiny 2017). Our theoretical

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

11451

<!-- Page 2 -->

analysis demonstrates that the update of ARS-OPT can be interpreted as implicitly incorporating second-order curvature information without explicit Hessian estimation, and establishes a bound on the expected gap between the objective value at iteration T and the optimum value. Building on this, we introduce PARS-OPT, which integrates transfer-based priors to improve gradient estimation. PARS-OPT further extends to combine priors from multiple surrogate models, delivering additional gains in attack performance. Extensive experiments on ImageNet, CIFAR-10, and a CLIP-based model demonstrate that our framework, consisting of ARS- OPT and its prior-enhanced variant PARS-OPT, outperforms 13 state-of-the-art methods with superior query efficiency. Our main contributions are summarized as follows.

• Novelty in hard-label attacks. We present ARS-OPT, a novel hard-label attack that accelerates convergence by estimating gradients along an interpolated “lookahead” direction, combining the search trajectory with accumulated momentum. We further introduce PARS-OPT, which integrates transfer-based priors from surrogate models to improve gradient estimation and enhance attack efficiency. • Novelty in theoretical analysis. We establish an O(1/T 2) convergence rate under standard assumptions, supported by the construction of an unbiased estimator of the true gradient that is essential for ensuring this rate. The theoretical analysis provides a principled explanation for the acceleration behavior of our approach and clarifies its underlying optimization dynamics. • SOTA performance. Experimental results show our approach outperforms 13 state-of-the-art attacks on ImageNet and CIFAR-10 across classifiers, including CLIP.

## Related Work

Hard-label attacks, also known as decision-based black-box attacks, are among the most challenging adversarial scenarios. They rely solely on the target model’s top-1 predicted label without access to internal structure or confidence scores, and craft perturbations by querying and exploiting information near the decision boundary. Boundary Attack (BA) (Brendel, Rauber, and Bethge 2018) was one of the earliest methods, performing random walks on the boundary to minimize perturbations, but suffers from low query efficiency. Biased BA (BBA) (Brunner et al. 2019) improves BA via three biases: (1) low-frequency Perlin noise, (2) regional masking, and (3) surrogate-model gradients. The Evolutionary Attack (abbreviated as Evolutionary) (Dong et al. 2019) adopts random sampling with adaptive covariance, while AHA (Li et al. 2021) exploits historical queries to guide the search. HopSkipJumpAttack (HSJA) (Chen, Jordan, and Wainwright 2020) refines adversarial examples via (1) gradient approximation at the boundary and (2) binary search projection onto the boundary toward the benign image. SQBA (Park, Miller, and McLaughlin 2024) combines surrogate-model gradients with HSJA’s gradient estimation to improve query efficiency. QEBA (Li et al. 2020) lowers HSJA’s query cost using subspaces derived from spatial transformations, low-frequency components, and intrinsic features. GeoDA (Rahmati et al. 2020) leverages the boundary’s low curvature via local linearization to estimate gradients and reduce queries. Triangle Attack (Wang et al. 2022) applies the law of sines in a low-frequency subspace, removing boundary projections and gradient estimation. Tangent Attack (TA) (Ma et al. 2021) locates an optimal tangent point to minimize perturbations, while SurFree (Maho, Furon, and Le Merrer 2021) uses geometry-driven directional trials without gradient estimation. CGBA and its variant CGBA- H (Reza et al. 2023) search along a semicircular path on a restricted 2D plane to find boundary points. Another direction formulates hard-label attacks as continuous optimization problems. OPT (Cheng et al. 2019) employs zeroth-order (ZO) optimization based on random-direction finite differences. Sign-OPT (Cheng et al. 2020) reduces queries by using directional derivative signs but sacrifices gradient precision. Prior-OPT (Ma et al. 2025) integrates transfer-based priors into the ray-search optimization, while RayS (Chen and Gu 2020) removes gradient estimation entirely by using hierarchical search, but is limited to untargeted ℓ∞-norm attacks. QE-DBA (Zhang, Ahmed, and Yu 2024) applies Bayesian optimization to explore the perturbation space, effectively addressing hard-label ZO optimization problems. However, existing methods overlook established acceleration strategies—such as momentum and Nesterov’s accelerated gradient—that can greatly improve convergence rates without requiring better gradient estimates. In this work, we address this gap by integrating acceleration techniques to enhance query efficiency. Moreover, our framework can further boost efficiency by incorporating transfer-based priors.

## 3 Problem Statement of Hard-Label Attacks

Given a classifier ψ: Rd →RC designed for a C-class classification task, and a correctly classified input image x ∈[0, 1]d, where d is the dimension of the input image, the adversary seeks to generate an adversarial example xadv by crafting a minimal perturbation such that the classifier’s prediction for xadv becomes incorrect. This adversarial objective can be formally expressed as:

min xadv ∥xadv −x∥p s.t. Φ(xadv) = 1, (1)

where ∥xadv−x∥p is the p-norm distortion, and the constraint Φ(xadv) is defined as an attack success indicator:

Φ(xadv):=

  

 

1 if ˆy = yadv in a targeted attack, or ˆy̸ = y in an untargeted attack, 0 otherwise.

(2)

Here, ˆy = arg maxi∈{1,...,C} ψ(xadv)i denotes the top-1 predicted label by classifier ψ, y is the true label of x, and yadv is the target label in a targeted attack scenario.

Following the ray-search methods (Cheng et al. 2019, 2020; Ma et al. 2025), we reformulate the optimization problem in Eq. (1) as finding the optimal ray direction θ∗from x that yields the minimal distance f(θ) to the boundary of the adversarial region. This can be formulated as:

min θ∈Rd\{0} f(θ), where f(θ):= inf n λ > 0: Φ x + λ θ

∥θ∥

= 1 o

.

(3)

By convention, f(θ) = +∞if the set is empty. Consequently, the resulting adversarial example is constructed as

11452

<!-- Page 3 -->

adversarial region g1(˜θt)

g2(˜θt)

E[g2(˜θt)] = ∇f(˜θt)

non-adversarial region f(θt+1)

θt ˜θt θt+1 mt mt+1 f(θt)

f(˜θt)

f(θt+1)

−1

ˆ L g1(˜θt)

−ζt αt g2(˜θt) In ARS-OPT, g1(˜θt) and g2(˜θt) are collinear, but this does not hold in PARS-OPT.

The circle represents the unit-norm constraint. original image

**Figure 1.** Illustration of a three-step update: first, compute the perturbation direction ˜θt = (1−αt)θt +αtmt; then estimate gradients at ˜θt using a biased g1(˜θt) and an unbiased g2(˜θt); finally, update θt+1 and mt+1 via a gradient descent step.

x∗= x + f(θ∗) θ∗

∥θ∗∥, where θ∗is the optimal solution obtained from the minimization problem defined in Eq. (3).

## 4 The Proposed Approach

Previous works (Cheng et al. 2019, 2020; Ma et al. 2025) focus on efficient gradient estimation to optimize the direction θ, with step size typically determined by line search. However, they do not explore any optimization acceleration techniques beyond gradient estimation. Next, we present an overview of ARS-OPT and its prior-enhanced variant PARS- OPT, both equipped with theoretical convergence guarantees.

Conceptual Sketch and Overview Nesterov and Spokoiny (2017) propose an Accelerated Random Search (ARS) method for ZO optimization, which rigorously establishes explicit non-asymptotic convergence rates under various convexity and smoothness assumptions by introducing an accelerated ZO framework. In the score-based setting, Cheng et al. (2021) extend ARS to score-based attacks and provide an analysis of the convergence rate. However, in hard-label attacks, obtaining function values requires extensive binary searches, significantly reducing the query efficiency of gradient estimation based on finite differences.

To address these limitations, we introduce ARS-OPT, a novel ZO optimization framework that can be seamlessly augmented with transfer-based priors to further boost query efficiency. The primary challenge is accelerating convergence in gradient descent when only poorly estimated gradients are available. At iteration t, we employ the following three-step update process for θt (Fig. 1):

1 Compute the perturbation direction ˜θt ←(1 −αt)θt + αtmt, where m0 is initialized to θ0. 2 At ˜θt, we use multiple queries to estimate gradients g1(˜θt) (biased estimator, e.g., Sign-OPT or Prior-OPT method) and g2(˜θt) (unbiased estimator of ∇f(˜θt)). 3 Update both parameters by gradient descent: θt+1 ← ˜θt −1

ˆLg1(˜θt), mt+1 ←mt −ζt αt g2(˜θt).

Inspired by Nesterov’s accelerated gradient method, our approach dynamically tracks two sequences, i.e., the direction θt and the momentum vector mt, and then computes a lookahead vector ˜θt by linearly interpolating between θt and mt, controlled by an interpolation coefficient αt. At

˜θt, we estimate two gradients, g1(˜θt) and g2(˜θt), to compute the updates of θt+1 and mt+1, respectively. Although we adopt the same estimation procedure for g1(˜θt) as in Prior-OPT, our algorithm converges substantially faster, as demonstrated by our experiments. The convergence guarantee of our approach relies on two technical assumptions: (1) g2(˜θt) serves as an unbiased estimator of ∇f(˜θt), and (2) ζt ≤Et h

(∇f(˜θt)⊤vt)2i

/

ˆL · Et h

∥g2(˜θt)∥2i

, with the full derivation given in the Appendix. We also note that our framework can incorporate various gradient estimation techniques, such as prior-guided estimation, to further improve performance. Our approach can be intuitively understood through the analogy of a walker descending a valley: rather than relying solely on the current slope, the walker looks ahead to anticipate the upcoming terrain and adjust the direction of motion accordingly, thereby achieving smoother and faster progress toward the minimum.

ARS-OPT Our framework, spanning from Step 1 to Step 3, is compatible with various gradient estimation techniques, enabling flexible algorithmic implementations. In this section, we provide a detailed introduction to the fundamental algorithm, ARS-OPT. In Step 1, unlike standard gradient descent, the gradient is not computed at the current direction θt. Instead, the algorithm predicts a candidate ray direction ˜θt by interpolating between the momentum vector mt and the current direction θt. The sequences of θt and mt are referred to as the main sequence and the auxiliary sequence, respectively.

˜θt is referred to as the lookahead position of θt, and is computed via interpolation: ˜θt ←(1 −αt)θt + αtmt, where αt ∈[0, 1] is the interpolation coefficient. The value of αt is defined as the positive root of the equation α2 t = ζtγt(1−αt), where γt is a scalar determined in Algorithm 1, and ζt =

2(q−1)+π dπ

/

ˆL dπ 2(q−1)+π

. This expression is derived from the convergence analysis of ARS-OPT. This choice of αt is critical to establishing the algorithm’s theoretical convergence guarantees. For detailed derivations, we refer readers to Appendix A. To maintain two sequences—the optimization variable θt and the auxiliary variable mt (which accumulates historical momentum to capture global optimization trends)—we employ two gradient estimates, g1(˜θt) and g2(˜θt), to update θt and mt, respectively:

g1(˜θt):= ∇f(˜θt)⊤vt · vt ≈f(˜θt + ϵvt) −f(˜θt)

ϵ · vt, (4)

g2(˜θt):= d 2 π (q −1) + 1∇f(˜θt)⊤vt · vt (5)

≈ d f(˜θt + ϵvt) −f(˜θt)

2ϵ π (q −1) + ϵ · vt, (6)

where d is the dimension of the input image, q is the number of vectors in gradient estimation, and vt is the sign-based gradient estimate (Cheng et al. 2020) as vt:=

1 √q

Pq i=1 sign(f(˜θt + ϵui) −f(˜θt))ui, which calculates the

11453

<!-- Page 4 -->

Original

Image x θt mt

˜θt = (1 −αt)θt + αtmt

Step 1

Initialization θ0, m0

Step 2

Gradient

Estimation g1(˜θt) = 1 ϵ f(˜θt+ϵvt) −f(˜θt)

vt

+ Ps i=1

1 ϵ f(˜θt+ϵpt,i) −f(˜θt)

pt,i g2(˜θt) = (d−s)π 2ϵ(q−s−1) + πϵ f(˜θt+ϵvt) −f(˜θt)

vt

+ Ps i=1

1 ϵ f(˜θt+ϵpt,i) −f(˜θt)

pt,i g1(˜θt)

g2(˜θt) ˜θt f(˜θt)

vt = 1 √q−s q−s X i=1 sign f(˜θt+ϵui)−f(˜θt)

| {z } only a single query (Eq. (7))

ui

˜θt ϵu1 ϵu2 ϵu3 ϵu4 ϵu5 vt u1 u2 u3 uq−s

... pt,1

...

pt,s x

˜θt Sample q −s random vectors, take s priors, then orthogonalize via Gram–Schmidt.

Step 3 Update θt+1 = ˜θt −1/ˆL · g1(˜θt) mt+1 = mt −ζt/αt · g2(˜θt)

g1(˜θt)

g2(˜θt)

˜θt {ui}q−s i=1 {pt,i}s i=1

**Figure 2.** Illustration of one iteration in PARS-OPT. We first form a lookahead point ˜θt by linearly interpolating between the current direction θt and the momentum term mt (with m0 = θ0). Next, we estimate vt via a sign-based procedure over a set of randomly sampled orthonormal basis vectors. Finally, we use vt to compute the biased gradient estimate g1(˜θt) and the unbiased estimate g2(˜θt), which are then used to update θt and mt, yielding θt+1 and mt+1 for the next iteration.

sign of the directional derivative with a single query:

sign(f(θ + ϵu) −f(θ)) =

(

+1, Φ x + f(θ) θ+ϵu ∥θ+ϵu∥

̸

= 1,

−1, otherwise.

(7) Eq. (4) can be regarded as the projection of the true gradient onto vt. Eq. (5) is an unbiased estimator of ∇f(˜θt), derived from Theorem 4.11. Theorem 4.1. Let {u1, u2,..., uq} be an orthonormal set obtained by orthogonalizing q vectors independently and uniformly sampled from the unit sphere in Rd. Suppose g is a fixed vector in Rd (for example, it is the true gradient to be estimated). Let v:= Pq i=1 sign(g⊤ui)ui, and ˆg:= g⊤v ·v. Then we have

E[ˆg] = E[(g⊤v)2] · g. (8)

The proof of Theorem 4.1 is shown in Appendix A. In Eq. (8), ˆg is equal to g1(˜θt), and E[(g⊤v)2] = 1 d

2 π(q −1) + 1 based on Lemma A.5 (see Appendix A). Thus we have E[g1(˜θt)] = 1 d

2 π(q −1) + 1

· g. Consequently, the true gradient can be recovered as g = d 2 π (q−1)+1E[g1(˜θt)] = d 2 π (q−1)+1E[∇f(˜θt)⊤vt · vt], which shows that g2(˜θt) is an unbiased estimator of ∇f(˜θt).

PARS-OPT ARS-OPT relies exclusively on random orthonormal vectors to estimate the gradient, which leads to inaccurate gradient approximation and poor query efficiency. To further enhance the efficiency of the algorithm, we propose a variant algorithm named Prior-guided ARS-OPT (PARS-OPT) within our framework. An ideal prior would be the gradient of ˆf(θ)

1Throughout this paper, for any vector v, we denote v as its ℓ2-normalized vector, where v:= v ∥v∥.

derived from a surrogate model. However, since ˆf(θ) is nondifferentiable due to the binary search process, this gradient cannot be directly computed. To overcome this challenge, we employ a differentiable surrogate function h(θ, λ) in Eq. (9), following Ma et al. (2025), which ensures the gradient relationship: ∇ˆf(θ0) = c · ∇θh(θ0, λ0) for any non-zero vector θ0 ∈Rd with ˆf(θ0) < +∞. Here, ˆf(·) is defined on the surrogate model ˆψ, λ0 = ˆf(θ0) is treated as a constant scalar during differentiation, and c is a non-zero constant.

h(θ, λ):=

(ˆψy −maxj̸=y ˆψj, if untargeted attack, maxj̸=yadv ˆψj −ˆψyadv, if targeted attack, (9)

where ˆψi:= ˆψ x + λ · θ ∥θ∥ i is an abbreviation for the i-th element of the output of the surrogate model ˆψ, and x is the original image. Given s non-zero vectors kt,1,..., kt,s computed as ∇θh(θ0, λ0) from s surrogate models and q −s randomly sampled vectors r1,..., rq−s ∼N(0, I), we apply Gram–Schmidt orthogonalization to these q vectors to obtain an orthonormal set pt,1,..., pt,s, u1,..., uq−s, which are used by the gradient estimation formulas:

g1(˜θt) = ∇f(˜θt)⊤vt · vt + s X i=1

∇f(˜θt)⊤pt,i · pt,i (10)

≈f(˜θt + ϵvt) −f(˜θt)

ϵ vt + s X i=1 f(˜θt + ϵpt,i) −f(˜θt)

ϵ pt,i. (11)

g2(˜θt) = d −s

2 π (q −s −1) + 1 ∇f(˜θt)⊤vt · vt + s X i=1

∇f(˜θt)⊤pt,i · pt,i

(12)

≈

(d −s)

f(˜θt + ϵvt) −f(˜θt)

2ϵ π (q −s −1) + ϵ vt + s X i=1 f(˜θt + ϵpt,i) −f(˜θt)

ϵ pt,i,

(13)

where vt:= 1 √q−s

Pq−s i=1 sign(f(˜θt + ϵui) −f(˜θt))ui. To ensure the convergence of PARS-OPT, we still require g2(˜θt)

11454

![Figure extracted from page 4](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

## Algorithm

1: (P)ARS-OPT Attack

1: Input: L-smooth function f, ˆL ≥L, the original image x, the success indicator function Φ(·), initial ray direction θ0, number of estimation vectors q, finite-difference step size ϵ, input dimension d, number of iterations T, maximum gradient norm gmax, γ0 > 0, surrogate model set S = { ˆψ(1),..., ˆψ(s)} with s > 0 for PARS-OPT, and S = ∅for ARS-OPT. 2: Output: Adversarial example xadv. 3: m0 ←θ0, ∥ˆ∇f−1∥2 ←+∞; 4: for t = 0 to T −1 do 5: for ˆψ(i) in S do 6: λt ←BinarySearch(x, θt, ˆψ(i), Φ); 7: kt,i ←∇θh(θt, λt) on ˆψ(i) with λt treated as a constant in differentiation; ▷obtain s priors. 8: end for 9: ri ∼N(0, I) for i = 1,..., q −s; 10: pt,1,..., pt,s, u1,..., uq−s ←Gram–Schmidt– Orthogonalize({kt,1,..., kt,s, r1,..., rq−s});

11: ˆDt ←

Ps i=1(∇f(θt)⊤pt,i)2

∥ˆ∇ft−1∥2; ▷It requires extra queries.

12: ζt ←

ˆ Dt+ (2(q−s−1)+π)

(d−s)π (1−ˆ Dt) ˆL(ˆ Dt+ (d−s)π (2(q−s−1)+π) (1−ˆ Dt));

13: ˜θt ←(1 −αt)θt + αtmt, where αt ≥0 is a positive root of the equation α2 t = ζtγt(1 −αt); 14: γt+1 ←(1 −αt)γt; 15: vt ← 1 √q−s

Pq−s i=1 sign(f(˜θt + ϵui) −f(˜θt))ui;

16: ∇f(˜θt)⊤vt ←f(˜θt+ϵvt)−f(˜θt)

ϵ; ▷Directional derivative approximation by finite differences.

17: ∇f(˜θt)⊤pt,i ←f(˜θt+ϵpt,i)−f(˜θt)

ϵ, ∀i = 1,..., s;

18: Estimate g1(˜θt), g2(˜θt) by using Eq. (11) and Eq. (13); 19: g1(˜θt) ←ClipGradNorm g1(˜θt), gmax

;

20: ∥ˆ∇ft∥2 ← s P i=1

∇f(˜θt)⊤pt,i

2+ (d−s)π 2(q−s−1)+π

∇f(˜θt)⊤vt

2

;

▷This line is used only in PARS-OPT. 21: θt+1 ←˜θt −1

ˆLg1(˜θt), mt+1 ←mt −ζt αt g2(˜θt); 22: end for 23: return xadv ←x + f(θT) θT ∥θT ∥.

to be an unbiased estimator of ∇f(˜θt), whose proof is more involved than in ARS-OPT; see the Appendix for details.

## Algorithm

1 presents a unified framework covering both ARS-OPT and PARS-OPT, and Fig. 2 offers an overview of the PARS-OPT procedure. In targeted attacks, we initialize θ0 with the direction to an image ˜x from the target class in the training set. The momentum term m0 is initialized as θ0 in the first iteration. Specifically, setting s = 0 reduces Eq. (11) and Eq. (13) to their counterparts in ARS-OPT, namely Eq. (4) and Eq. (6). Note that ˆDt and ∥ˆ∇ft∥2 are estimators rather than exact values, and {∇f(θt)⊤pt,i}s i=1 in ˆDt require additional finite-difference approximations. Details are provided in Remark A.12 of Appendix A. Algorithm 1 is a practical approximation of an idealized version presented in Appendix A. Theorem 4.2 establishes the convergence guarantee for this idealized algorithm, giving an O(1/T 2) rate under smooth convex assumptions, whereas a variant of Sign-OPT only attains an O((ln T)/T) rate (Theorem A.10), implying faster convergence for the idealized PARS-OPT. Theorem 4.2. Let θ∗denote the optimal solution of Problem (3), and let θ0, θT, γ0, and ζt denote the corresponding quantities in the idealized version of Algorithm 1. Assuming that f(·) is smooth and convex, we have

E



(f(θT) −f(θ∗))

1 + √γ0

2

T −1 X t=0 p ζt

!2

≤ f(θ0) −f(θ∗) + γ0

2 ∥θ0 −θ∗∥2. (14)

The proof is given in Appendix A (Theorem A.11).

## Experiments

Experimental Setting Dataset. We evaluate the proposed method on two publicly available datasets, CIFAR-10 (Krizhevsky and Hinton 2009) and ImageNet (Deng et al. 2009), with images resized to 3 × 32 × 32 and 3 × 299 × 299, respectively. For all experiments, 1,000 images are randomly selected from each dataset as test samples for evaluation. In the case of targeted attacks, the target class is defined as yadv = (y + 1) mod C, where y denotes the true class. For the same target class, we use the same image ˜x as the initialization for all methods. Models. On the ImageNet dataset, we evaluate two target models: Inception-v4 (Szegedy et al. 2017) and Swin Transformer (Liu et al. 2021). For Inception-v4 (input resolution 299 × 299), we use Inception-ResNet-v2 (IncResV2) and Xception as surrogate models. For Swin Transformer (inputs resized to 224 × 224), the surrogate models are ResNet-50 and ConViT (D’Ascoli et al. 2021). See Appendix for details. Baseline Methods. We compare ARS-OPT and PARS-OPT against baselines, including HSJA, TA, GeoDA, Evolutionary, SurFree, AHA, QEBA, CGBA-H, SQBA, BBA, Sign- OPT, Prior-Sign-OPT and Prior-OPT. In our methods, the suffix “-S” (e.g., ARS-OPT-S) means the random vectors u1,..., uq−s for gradient estimation are drawn from a 3×56×56-dimensional subspace. AHA, QEBA, and CGBA- H also adopt subspace sampling, while SQBA, BBA, Prior- Sign-OPT, Prior-OPT, and PARS-OPT leverage surrogate models, denoted by subscripts; e.g., PARS-OPTIncResV2 uses Inception-ResNet-v2 as the surrogate model. Metrics. We report the mean ℓ2 distortion as 1 |X|

P x∈X ∥xadv −x∥2, where X denotes the test dataset. Additionally, we present the attack success rate (ASR), defined as the proportion of samples with distortions below a threshold

√

0.001 × d for a given query budget.

Experimental Results on the ImageNet Dataset Results of Attacks against Undefended Models. Tables 1 and 2 report the results of attacks against undefended models on 1,000 ImageNet images. In summary:

(1) In Table 1, PARS-OPT performs the best in untargeted attacks, while ARS-OPT-S achieves state-of-the-art performance in targeted attacks due to its stabilized optimization via the lookahead direction, reducing the risk of local minima.

11455

<!-- Page 6 -->

## Method

with Untargeted Attack Targeted Attack D.R.1 2K 4K 6K 8K 10K 2K 4K 6K 8K 10K 15K 20K

Inception-v4

HSJA × 44.53 26.31 17.92 14.19 11.65 79.00 60.90 47.25 39.19 32.95 24.55 19.52 TA × 42.23 25.86 17.80 14.17 11.69 61.99 47.07 37.16 31.51 27.11 21.08 17.32 Sign-OPT × 48.23 23.27 14.97 11.07 8.79 65.20 48.33 38.49 32.10 27.53 20.39 16.28 GeoDA × 20.12 14.33 12.49 11.01 9.69 - - - - - - - Evolutionary × 42.66 25.32 17.60 13.38 10.84 65.06 48.37 38.72 32.12 27.39 19.94 15.61 SurFree × 38.48 26.35 20.17 16.37 13.82 74.89 61.16 51.56 44.48 39.00 29.35 23.15 AHA ✓ 42.06 23.52 15.41 11.10 8.52 54.12 36.09 26.46 20.50 16.49 10.86 8.12 QEBA ✓ 16.54 8.08 5.82 4.26 3.66 58.31 37.68 28.56 21.74 18.00 12.07 9.25 CGBA-H ✓ 15.12 7.83 5.86 4.61 4.10 56.32 37.82 29.69 23.86 20.00 14.31 11.56 SQBAIncResV2 × 19.03 12.80 10.01 8.43 7.42 - - - - - - - BBAIncResV2 × 28.44 20.74 17.37 15.47 14.19 56.28 44.98 38.43 34.07 30.94 25.76 22.63 Prior-Sign-OPTIncResV2 × 42.40 17.16 10.19 7.36 5.84 55.42 37.00 28.14 22.96 19.51 14.36 11.66 Prior-Sign-OPTIncResV2&Xception × 37.10 12.57 7.10 5.19 4.20 49.37 31.34 23.67 19.32 16.70 12.82 10.77 Prior-OPTIncResV2 × 18.13 6.80 5.15 4.45 4.03 49.84 36.80 31.04 27.60 25.28 21.84 19.80 Prior-OPTIncResV2&Xception × 13.42 4.49 3.64 3.32 3.12 42.63 30.32 25.60 23.01 21.44 19.19 17.98 ARS-OPT × 46.60 24.24 15.74 11.68 9.30 65.53 46.60 35.84 28.84 24.02 16.63 12.69 PARS-OPTIncResV2 × 14.02 6.31 4.93 4.24 3.82 49.37 33.88 26.91 22.72 19.94 16.06 13.67 PARS-OPTIncResV2&Xception × 9.91 4.41 3.62 3.28 3.05 43.91 28.16 22.56 19.36 17.23 14.13 12.32 ARS-OPT-S ✓ 25.02 10.38 6.46 4.85 3.92 59.15 37.52 26.37 19.62 15.37 9.94 7.38 PARS-OPT-SIncResV2 ✓ 19.55 7.82 5.36 4.23 3.54 55.18 34.12 24.22 18.73 15.02 10.18 7.84 PARS-OPT-SIncResV2&Xception ✓ 20.52 7.25 5.02 4.05 3.45 55.28 33.30 23.70 18.64 15.31 10.78 8.33

Swin Transformer

HSJA × 45.86 27.32 17.92 13.50 10.64 50.96 39.26 30.66 25.64 21.73 16.19 12.75 TA × 46.73 27.85 18.02 13.38 10.51 40.72 31.92 25.88 22.25 19.45 15.52 12.89 Sign-OPT × 53.40 26.41 16.93 12.41 9.90 44.91 35.98 30.89 27.52 25.27 21.84 19.95 GeoDA × 36.92 28.03 24.54 21.59 19.12 - - - - - - - Evolutionary × 49.24 31.19 23.04 18.60 15.74 51.71 38.29 31.23 26.85 23.76 19.28 16.56 SurFree × 34.28 23.58 18.37 15.18 13.06 61.31 47.67 39.39 33.84 29.73 22.96 18.73 AHA ✓ 46.76 30.37 23.35 19.39 17.02 36.11 28.04 23.68 20.78 18.76 15.51 13.72 QEBA ✓ 31.11 16.99 12.07 8.46 7.02 42.99 30.31 24.38 19.40 16.52 11.58 8.91 CGBA-H ✓ 29.24 17.01 12.60 9.26 7.81 37.81 27.83 23.19 19.67 17.17 13.10 10.83 SQBAResNet50 × 20.40 13.40 10.33 8.62 7.56 - - - - - - - BBAResNet50 × 29.37 20.94 17.59 15.47 14.08 35.28 28.45 24.65 22.16 20.34 17.54 15.98 Prior-Sign-OPTResNet50 × 52.88 26.19 16.45 11.88 9.25 43.88 34.32 29.23 26.06 23.86 20.52 18.66 Prior-Sign-OPTResNet50&ConViT × 43.06 17.96 10.91 7.90 6.33 43.20 33.48 28.21 24.99 22.84 19.66 17.94 Prior-OPTResNet50 × 39.45 20.26 14.13 11.24 9.62 42.96 33.51 28.64 25.67 23.72 20.86 19.45 Prior-OPTResNet50&ConViT × 17.98 8.66 6.45 5.45 4.90 39.62 30.27 25.75 23.12 21.45 19.27 18.33 ARS-OPT × 41.91 20.04 12.76 9.26 7.21 38.85 26.14 19.70 15.67 12.99 9.10 6.96 PARS-OPTResNet50 × 29.26 12.77 8.41 6.22 5.01 38.01 25.72 19.72 15.73 13.15 9.39 7.29 PARS-OPTResNet50&ConViT × 12.73 6.11 4.56 3.73 3.23 36.53 23.60 17.98 14.50 12.20 8.61 6.90 ARS-OPT-S ✓ 23.04 10.61 6.88 5.06 3.99 34.77 20.92 14.46 10.71 8.31 5.24 3.79 PARS-OPT-SResNet50 ✓ 23.91 10.96 7.23 5.40 4.31 37.10 22.92 15.85 11.88 9.42 6.03 4.30 PARS-OPT-SResNet50&ConViT ✓ 19.84 8.74 6.09 4.68 3.85 37.06 22.56 16.26 12.26 9.83 6.54 4.80

1 D.R. denotes the use of dimension reduction technique.

**Table 1.** Mean ℓ2 distortions of different query budgets on the ImageNet dataset.

## Method

Mean ℓ2 Distortions Attack Success Rate 2K 4K 6K 8K 10K 2K 4K 6K 8K 10K

Sign-OPT 49.44 42.29 38.93 37.02 35.71 15.2% 16.3% 18.0% 19.1% 19.4% Prior-OPTResNet50 27.38 21.52 19.34 18.52 18.15 34.9% 44.9% 48.7% 50.6% 51.4% Prior-OPTConViT 21.27 16.54 15.14 14.62 14.36 43.3% 54.7% 57.5% 58.8% 58.9% Prior-OPTResNet50&ConViT 18.09 12.66 11.22 10.72 10.43 50.1% 65.6% 70.2% 72.2% 73.4% ARS-OPT 47.42 37.08 31.00 26.97 24.02 16.2% 20.2% 24.7% 28.2% 30.7% PARS-OPTResNet50 26.18 17.65 14.45 12.69 11.55 36.2% 49.8% 56.8% 62.2% 65.8% PARS-OPTConViT 20.80 14.89 12.68 11.47 10.61 43.3% 57.0% 62.0% 66.5% 69.1% PARS-OPTResNet50&ConViT 18.67 12.25 10.16 9.07 8.38 48.7% 65.1% 72.6% 76.0% 78.8%

**Table 2.** The experimental results of attacking against CLIP with the backbone of ViT-L/14.

11456

<!-- Page 7 -->

0 4K 8K 12K 16K 20K Number of Queries

5

10

15

20

25

30

35

40

45

Mean ℓ2 Distortion

TA GeoDA HSJA Sign-OPT Evolutionary SurFree AHA QEBA CGBA-H Prior-OPT ARS-OPT PARS-OPT ARS-OPT-S PARS-OPT-S

(a) ATResNet50,ϵ∞=8/255(ImageNet)

0 4K 8K 12K 16K 20K Number of Queries

5 15 25 35 45 55 65 75 85 95 105 115 125

Mean ℓ2 Distortion

TA GeoDA HSJA Sign-OPT Evolutionary SurFree AHA QEBA CGBA-H Prior-OPT ARS-OPT PARS-OPT ARS-OPT-S PARS-OPT-S

(b) MIMIRViT,ϵ∞=4/255(ImageNet)

0 4K 8K 12K 16K 20K Number of Queries

10 20 30 40 50 60 70 80 90 100

Attack Success Rate

TA GeoDA HSJA Sign-OPT Evolutionary SurFree AHA QEBA CGBA-H Prior-OPT ARS-OPT PARS-OPT ARS-OPT-S PARS-OPT-S

(c) ATResNet50,ϵ∞=8/255(ImageNet)

0 4K 8K 12K 16K 20K Number of Queries

10 20 30 40 50 60 70 80 90 100

Attack Success Rate

TA GeoDA HSJA Sign-OPT Evolutionary SurFree AHA QEBA CGBA-H Prior-OPT ARS-OPT PARS-OPT ARS-OPT-S PARS-OPT-S

(d) MIMIRViT,ϵ∞=4/255(ImageNet)

**Figure 3.** Mean distortions and attack success rates of untargeted attacks with ℓ2 norm constraint against defense models. The surrogate model of PARS-OPT and Prior-OPT is the adversarially trained ResNet-50 model (PGD, ϵℓ∞= 4/255).

0.0 0.2 0.4 0.6 0.8 1.0 ˆDt

0.00 0.05 0.10 0.15 0.20 ζt

ARS-OPT PARS-OPT

(a) Effect of prior’s quality ˆDt

0 200 400 600 800 1000 q

0.000 0.005 0.010 0.015 0.020 ζt

ARS-OPT PARS-OPT ˆDt=0.2 PARS-OPT ˆDt=0.1 PARS-OPT ˆDt=0.01

(b) Effect of number of vectors q

0 2 4 6 8 10 s

0.00 0.05 0.10 0.15 0.20 ζt

ARS-OPT PARS-OPT ¯Dt=0.1

(c) Effect of number of priors s

0 20 40 60 80 100 T 0.0

1.0

2.0

3.0

E[f(θT) −f(θ∗)]

ARS-OPT(upper bound) PARS-OPT ˆDt=0.1(upper bound)

(d) Convergence of (P)ARS-OPT

**Figure 4.** Experimental results of ablation studies.

(2) Table 2 reports untargeted attack results on CLIP (ViT- L/14). Our methods outperform the baselines (Sign-OPT and Prior-OPT) in mean ℓ2 distortion and attack success rate. Results of Attacks against Defense Models. We evaluate untargeted attacks against two types of defense models, i.e., adversarial training (AT) (Madry et al. 2018) and MIMIR (Xu et al. 2025). MIMIR achieves state-of-the-art performance on RobustBench (Croce et al. 2021). Fig. 3 shows that our methods achieve the best performance on ImageNet.

Comprehensive Understanding of (P)ARS-OPT In our ablation studies, we perform controlled experiments based on our theoretical analysis with dimensionality d = 3,072. Fig. 4a shows the relationship between ˆDt and ζt. As ˆDt increases, ζt increases accordingly, which in turn improves the convergence rate of PARS-OPT (Eq. (14)). Fig. 4b illustrates that increasing the number of vectors q used for gradient estimation leads to larger ζt and improved performance. Fig. 4c shows that when each prior has the same quality, defined as ¯Dt:= ˆDt/s, increasing the number of priors yields a larger ζt and higher attack efficiency. Fig. 4d shows that when the prior is effective, even with a small

ˆDt, PARS-OPT achieves a lower convergence bound than ARS-OPT, indicating better potential performance.

## 6 Conclusion

We propose a novel hard-label attack approach, comprising two algorithms—ARS-OPT and PARS-OPT—that accelerate convergence and improve attack success rates by leveraging Nesterov-style acceleration and transfer-based priors. We provide convergence guarantees through theoretical analysis and validate our methods with extensive experiments, demonstrating improvements over 13 state-of-the-art approaches.

11457

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-improving-the-convergence-rate-of-ray-search-optimization-for-query-efficient-ha/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was supported by Zhejiang Provincial Natural Science Foundation of China under Grant No. LMS25F020005, and by the Key R&D Program of Zhejiang Province under Grant No. 2024C01164.

## References

Brendel, W.; Rauber, J.; and Bethge, M. 2018. Decision- Based Adversarial Attacks: Reliable Attacks Against Black- Box Machine Learning Models. In International Conference on Learning Representations. Brunner, T.; Diehl, F.; Le, M. T.; and Knoll, A. 2019. Guessing Smart: Biased Sampling for Efficient Black-Box Adversarial Attacks. In IEEE/CVF International Conference on Computer Vision, 4957–4965. IEEE Computer Society. Chen, J.; and Gu, Q. 2020. RayS: A Ray Searching Method for Hard-label Adversarial Attack. In ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD ’20, 1739–1747. Association for Computing Machinery. ISBN 9781450379984. Chen, J.; Jordan, M. I.; and Wainwright, M. J. 2020. Hop- SkipJumpAttack: A Query-Efficient Decision-Based Attack. In IEEE Symposium on Security and Privacy, 1277–1294. Cheng, M.; Le, T.; Chen, P.-Y.; Zhang, H.; Yi, J.; and Hsieh, C.-J. 2019. Query-Efficient Hard-label Black-box Attack: An Optimization-based Approach. In International Conference on Learning Representations. Cheng, M.; Singh, S.; Chen, P. H.; Chen, P.-Y.; Liu, S.; and Hsieh, C.-J. 2020. Sign-OPT: A Query-Efficient Hard-label Adversarial Attack. In International Conference on Learning Representations. Cheng, S.; Wu, G.; and Zhu, J. 2021. On the Convergence of Prior-Guided Zeroth-Order Optimization Algorithms. In Advances in Neural Information Processing Systems, volume 34, 14620–14631. Curran Associates, Inc. Croce, F.; Andriushchenko, M.; Sehwag, V.; Debenedetti, E.; Flammarion, N.; Chiang, M.; Mittal, P.; and Hein, M. 2021. RobustBench: a standardized adversarial robustness benchmark. In Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks, volume 1. D’Ascoli, S.; Touvron, H.; Leavitt, M. L.; Morcos, A. S.; Biroli, G.; and Sagun, L. 2021. ConViT: Improving Vision Transformers with Soft Convolutional Inductive Biases. In International Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, 2286–2296. PMLR. Deng, J.; Dong, W.; Socher, R.; Li, L.-J.; Li, K.; and Fei- Fei, L. 2009. ImageNet: A Large-Scale Hierarchical Image Database. In IEEE Conference on Computer Vision and Pattern Recognition, 248–255. Dong, Y.; Su, H.; Wu, B.; Li, Z.; Liu, W.; Zhang, T.; and Zhu, J. 2019. Efficient Decision-Based Black-Box Adversarial Attacks on Face Recognition. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 7706–7714. Goodfellow, I. J.; Shlens, J.; and Szegedy, C. 2015. Explaining and Harnessing Adversarial Examples. In International Conference on Learning Representations.

Krizhevsky, A.; and Hinton, G. 2009. Learning Multiple Layers of Features from Tiny Images. Technical Report 0, University of Toronto. Li, H.; Xu, X.; Zhang, X.; Yang, S.; and Li, B. 2020. QEBA: Query-Efficient Boundary-Based Blackbox Attack. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1218–1227. IEEE Computer Society. Li, J.; Ji, R.; Chen, P.; Zhang, B.; Hong, X.; Zhang, R.; Li, S.; Li, J.; Huang, F.; and Wu, Y. 2021. Aha! Adaptive Historydriven Attack for Decision-based Black-box Models. In IEEE/CVF International Conference on Computer Vision, 16148–16157. IEEE Computer Society. Liu, Z.; Lin, Y.; Cao, Y.; Hu, H.; Wei, Y.; Zhang, Z.; Lin, S.; and Guo, B. 2021. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. In IEEE/CVF International Conference on Computer Vision, 9992–10002. IEEE Computer Society. Ma, C.; Chen, L.; and Yong, J.-H. 2021. Simulating Unknown Target Models for Query-Efficient Black-box Attacks. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 11830–11839. Ma, C.; Guo, X.; Chen, L.; Yong, J.-H.; and Wang, Y. 2021. Finding Optimal Tangent Points for Reducing Distortions of Hard-label Attacks. In Advances in Neural Information Processing Systems, volume 34, 19288–19300. Ma, C.; Xu, X.; Cheng, S.; and Xuan, Q. 2025. Boosting Ray Search Procedure of Hard-label Attacks with Transfer-based Priors. In International Conference on Learning Representations. Madry, A.; Makelov, A.; Schmidt, L.; Tsipras, D.; and Vladu, A. 2018. Towards Deep Learning Models Resistant to Adversarial Attacks. In International Conference on Learning Representations. Maho, T.; Furon, T.; and Le Merrer, E. 2021. SurFree: a fast surrogate-free black-box attack. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 10425–10434. IEEE Computer Society. Nesterov, Y.; and Spokoiny, V. 2017. Random Gradient- Free Minimization of Convex Functions. Foundations of Computational Mathematics, 17(2): 527–566. Park, J.; Miller, P.; and McLaughlin, N. 2024. Hardlabel based Small Query Black-box Adversarial Attack. In IEEE/CVF Winter Conference on Applications of Computer Vision, 3974–3983.

Rahmati, A.; Moosavi-Dezfooli, S.-M.; Frossard, P.; and Dai, H. 2020. GeoDA: A Geometric Framework for Black-Box Adversarial Attacks. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, 8443–8452.

Reza, M. F.; Rahmati, A.; Wu, T.; and Dai, H. 2023. CGBA: Curvature-aware Geometric Black-box Attack. In IEEE/CVF International Conference on Computer Vision, 124–133. Szegedy, C.; Ioffe, S.; Vanhoucke, V.; and Alemi, A. A. 2017. Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning. In AAAI Conference on Artificial Intelligence, AAAI’17, 4278–4284. AAAI Press.

11458

<!-- Page 9 -->

Wang, X.; Zhang, Z.; Tong, K.; Gong, D.; He, K.; Li, Z.; and Liu, W. 2022. Triangle Attack: A Query-Efficient Decision- Based Adversarial Attack. In European Conference on Computer Vision, 156–174. Springer-Verlag. ISBN 978-3-031- 20064-9. Xu, X.; Yu, S.; Liu, Z.; and Picek, S. 2025. MIMIR: Masked Image Modeling for Mutual Information-based Adversarial Robustness. arXiv:2312.04960. Zhang, Z.; Ahmed, N.; and Yu, S. 2024. QE-DBA: Query- Efficient Decision-Based Adversarial Attacks via Bayesian Optimization. In International Conference on Computing, Networking and Communications, 783–788.

11459
