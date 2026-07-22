---
title: "Generalized Gradient Norm Clipping & Non-Euclidean $(L_0,L_1)$-Smoothness"
source_url: https://neurips.cc/virtual/2025/oral/115789
paper_pdf_url: https://arxiv.org/pdf/2506.01913v3
venue: NeurIPS
year: 2025
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Generalized Gradient Norm Clipping & Non-Euclidean $(L_0,L_1)$-Smoothness

<!-- Page 1 -->

Generalized Gradient Norm Clipping & Non-Euclidean (L0, L1)-Smoothness

Thomas Pethick∗

EPFL (LIONS) thomas.pethick@epfl.ch

Wanyun Xie∗ EPFL (LIONS) wanyun.xie@epfl.ch

Mete Erdogan EPFL (LIONS) mete.erdogan@epfl.ch

Kimon Antonakopoulos

EPFL (LIONS) kimon.antonakopoulos@epfl.ch

Antonio Silveti-Falls Université Paris-Saclay (CVN)

tonys.falls@gmail.com

Volkan Cevher

EPFL (LIONS) volkan.cevher@epfl.ch

## Abstract

This work introduces a hybrid non-Euclidean optimization method which generalizes gradient norm clipping by combining steepest descent and conditional gradient approaches. The method achieves the best of both worlds by establishing a descent property under a generalized notion of (L0,L1)-smoothness. Weight decay is incorporated in a principled manner by identifying a connection to the Frank-Wolfe short step. In the stochastic case, we show an order optimal O(n−1/4) convergence rate by leveraging a momentum based gradient estimator. We discuss how to instantiate the algorithms for deep learning, which we dub Clipped Scion, and demonstrate their properties on image classification and language modeling. The code is available at https://github.com/LIONS-EPFL/ClippedScion.

## Introduction

Recent work [Pethick et al., 2025] has shown that conditional gradient methods2, traditionally used for constrained optimization, can also solve unconstrained problems—offering an alternative to steepest descent. From their analysis it becomes apparent that the two methods have distinct properties: whereas steepest descent requires the stepsize γ for L-smooth objectives to be taken as γ < 2/L, conditional gradient methods have no such requirement, thus allowing for large stepsizes, while remaining stable.

The price to pay for the stability is that conditional gradient based methods are not descent methods and thus eventually needs a diminishing stepsize to converge, even in the deterministic case. The problem becomes very apparent if the iterates are close to the solution, since the iterates always move by a fixed magnitude and are thus pushed away from the solution. Steepest descent does not suffer from the same problem since the effective stepsize automatically becomes smaller as the iterates approach a solution. This observation naturally raises the following question:

∗Equal contribution. 2By conditional gradient based methods, we mean those methods which leverage a linear minimization oracle lmo(d) = arg min x∈D

⟨d, x⟩when updating their parameters with an open-loop stepsize.

39th Conference on Neural Information Processing Systems (NeurIPS 2025).

arXiv:2506.01913v3 [cs.LG] 4 Feb 2026

<!-- Page 2 -->

**Table 1.** Special instantiations of Algorithm 1 according to different choices of norm. Control on the norm of the parameters is guaranteed by the constrained variant of the method (Algorithm 2).

## Method

Norm type Norm ball lmo(d) ∥d∥∗ Reference

Clipped GD Vector Euclidean ∥· ∥2-ball −d

∥d∥2 ∥d∥2 [Mikolov et al., 2012] Clipped Sign Vector Max-norm ∥· ∥∞-ball −sign(d) ∥d∥1 This paper Clipped Spectral Matrix Spectral norm ∥· ∥S∞-ball −UV⊤1 −tr(lmo(d)⊤d) This paper Clipped Scion (Algorithms 3 and 4) Product Max-norm ball over layers {rl lmo∥·∥Wl (dl)}l∈[D] −P l ⟨rl lmo(dl), dl⟩ This paper 1 The reduced SVD is given as d = U diag(σ)V⊤.

Can we combine the two methods and get the best of both worlds? That is, does a stable method exist which takes large steps initially but adapts the stepsize when near a solution?

In this paper we answer the above in the affirmative by considering a hybrid method that combines a conditional gradient method with steepest descent. The proposed method generalizes gradient norm clipping [Mikolov et al., 2012] beyond the Euclidean case. In practice, gradient norm clipping has been widely adopted to stabilize training of recurrent neural networks (RNNs), Transformers and diffusion models, especially in large-scale settings. Theoretically, a precise characterization of the benefits has emerged under the (L0, L1)-smoothness assumption [Zhang et al., 2019, 2020, Koloskova et al., 2023]. Expanding on this, we show that these benefits of clipping can be made compatible with non-Euclidean methods. Besides clipping, we provide a novel analysis of conditional gradient methods without clipping under these same smoothness assumptions.

Concretely, we make the following contributions:

(i) We introduce a hybrid method between a conditional gradient method and steepest descent

(Algorithm 1), which in the Euclidean case recovers gradient norm clipping. The benefit of the hybrid method is made precise by showing a descent property under a generalized (L0, L1)-smoothness condition.

(ii) In the stochastic case we show an order optimal O(n−1/4) rate by leveraging a momentum estimator. Convergence for a clipped algorithm with stochastic feedback appears to be new even in the Euclidean case.

(iii) We establish a connection between clipping and the short step from the Frank-Wolfe literature, which similarly enjoys a descent property. The connection enables us to combine clipping with weight decay in a principled manner that maintains convergence guarantees. We propose a stochastic variant of the short step (Algorithm 2) and establish a O(n−1/4) rate.

(iv) We explicitly instantiate the algorithms for deep learning through a product norm over layers (Algorithms 3 and 4) and demonstrate their properties through experiments on image classification and language modeling.

## Preliminaries

Given a continuously differentiable objective function f: X →R, the classical gradient descent method (GD) with a stepsize γ > 0 can be written as xk+1 = arg min x∈X γ⟨∇f(xk), x⟩+ 1

2∥x −xk∥2 2 = xk −γ∇f(xk). (GD)

The normalized gradient descent method with radius ρ > 0 is, in comparison, defined as follows xk+1 = arg min

∥x−xk∥2≤ρ γ⟨∇f(xk), x⟩= xk + ρ arg min

∥x∥2≤1 γ⟨∇f(xk), x⟩= xk −γ ρ ∇f(xk)

∥∇f(xk)∥2

. (Normalized GD)

A hybrid variant is much more popular in practice, xk+1 = arg min

∥x−xk∥2≤ρ γ⟨∇f(xk), x⟩+ 1

2∥x −xk∥2 2 = xk −γ min{1, ρ ∥∇f(xk)∥2 }∇f(xk), (Clipped GD)

which we notice can be rewritten by combining GD and Normalized GD. Indeed, all three of these algorithms correspond to minimizing γ⟨∇f(xk), x⟩+ R(x)

<!-- Page 3 -->

for different choices of R. For GD, R(x) = 1

2∥x −xk∥2 2 while for Normalized GD, R(x) = ιρD(x −xk), the indicator function for Euclidean ball D = {x: ∥x∥2 ≤1} scaled by the radius ρ; Clipped GD combines both by taking R(x) = 1

2∥x −xk∥2 2 + ιρD(x −xk). This results in the iterates of Clipped GD being generated by the update in Normalized GD if ∥∇f(xk)∥2 is large, but reducing to the update in GD when ∥∇f(xk)∥2 is small enough.

Observation I Our first observation is that both GD and Normalized GD can be generalized to the non-Euclidean case. Define the sharp-operator [Nesterov, 2012, Kelner et al., 2014], d♯∈arg max x∈X

{⟨d, x⟩−1

2∥x∥2}.

Then, we can write the (possibly non-Euclidean) steepest descent method (SD) as follows xk+1 = xk −γ[∇f(xk)]♯ (SD)

Observe that we recover GD when choosing the Euclidean ℓ2 norm.

Generalizing Normalized GD to non-Euclidean norms is possible by noticing that the normalization can be written in terms of the linear minimization oracle (lmo)

lmo(d) ∈arg min x∈D

⟨d, x⟩ where the constraint is a (now assumed to be non-Euclidean) norm-ball D:= {x | ∥x∥≤1}. By choosing the ℓ2-norm ball, Normalized GD can be seen as an instance of the so-called unconstrained conditional gradient method (uCG) [Pethick et al., 2025], xk+1 = xk + γρ lmo(∇f(xk)). (uCG)

Observation II Our second central observation is that uCG can in general be considered a normalized version of steepest descent. This relationship follows from noticing that the sharp operator and lmo can be defined in terms of each other. Specifically, we have that lmo(d) = −d♯

∥d∥∗ or, equivalently, d♯= −∥d∥∗lmo(d). (1)

In the following section we use this observation to generalize Clipped GD to the non-Euclidean case.

## Method

We propose the generalized gradient norm clipping method (GGNC)

xk+1 = xk −γτk[dk]♯ with τk:= min{1, ρ ∥dk∥∗}. (GGNC)

There is freedom in how to compute the dual norm ∥dk∥∗due to the following equivalence property for the sharp operator, ∥s∥2

∗= ∥s♯∥2 = ⟨s, s♯⟩. This form is useful, e.g., in the Euclidean case where the sharp-operator is readily available, since then [dk]♯= dk.

For norm choices where the lmo is more naturally available we can equivalently write GGNC as xk+1 = xk + γηk lmo(dk) with ηk:= min{ρ, ∥dk∥∗}.

We have that ∥dk∥∗= −⟨dk, lmo(dk)⟩due to the definition of the dual norm and the optimality of lmo(dk). So, provided that lmo has been computed, we can obtain ∥dk∥∗with very little overhead. From this rewriting we also see that ρ can also be interpreted as the radius of the norm-ball constraint over which we compute the lmo.

The GGNC update rule can be seen as the solution to the following optimization problem:

xk+1 ∈arg min

∥x−xk∥≤ρ γ ⟨dk, x −xk⟩+ 1

2∥x −xk∥2

The objective is the same quadratic approximation that gives rise to SD, but the iterates are further constrained to a trust-region of radius ρ in the chosen norm, as in uCG.

<!-- Page 4 -->

## Algorithm

## 1 Generalized Gradient Norm Clipping (GGNC) Input:

Horizon n, init. x1 ∈X, d0 = 0, momentum αk ∈(0, 1], stepsize γ ∈(0, 1)

1: for k = 1,..., n do 2: Sample ξk ∼P 3: dk ←αk∇f(xk, ξk) + (1 −αk)dk−1

4: vk ←−lmo(dk) 5: ηk ←min{ρ, ⟨dk, vk⟩} 6: xk+1 ←xk −γηkvk

7: Choose ¯xn uniformly at random from {x1,..., xn} Return ¯xn

Equivalently to step 4-6: xk+1 ←xk −γτkvk with τk = min{1, ρ ⟨dk,vk⟩1/2 } and vk = [dk]♯.

## Algorithm

## 2 Stochastic Short Step Conditional Gradient (S3CG) Input:

Horizon n, init. x1 ∈βD = {x ∈X: ∥x∥≤β}, d0 = 0, momentum αk ∈(0, 1], stepsize γ ∈(0, 1], ball radius β > 0

1: for k = 1,..., n do 2: Sample ξk ∼P 3: dk ←αk∇f(xk, ξk) + (1 −αk)dk−1

4: vk ←xk −β lmo(dk)

5: Variant 1: ηk ←min{ρ, ⟨dk,vk⟩

∥vk∥2 }

6: Variant 2: ηk ←min{ρ, ⟨dk,vk⟩

4β2 }

7: xk+1 ←xk −γηkvk

8: Choose ¯xn uniformly at random from {x1,..., xn} Return ¯xn

Stochastic case In the deterministic case we can simply take the direction to be dk = ∇f(xk). In the stochastic case, one has to proceed with more care, since lmo(dk) can be biased even when dk is unbiased, due to its potential nonlinearity. With αk ∈(0, 1], we define the momentum based gradient estimator dk = (1 −αk)dk−1 + αk∇f(xk, ξk).

The final algorithm involving the momentum based gradient estimator is presented in Algorithm 1.

Weight decay & constrained problems Weight decay is a very popular technique, both as a regularizer to avoid overfitting and for ensuring numerical stability. A precise characterization exists for weight decay when combined with the conditional gradient based schemes like uCG, since the resulting update reduces to the classical conditional gradient method (a.k.a. Frank-Wolfe) designed for solving constrained problems [Chen et al., 2023, D’Angelo et al., 2023, Xie and Li, 2024, Pethick et al., 2025], xk+1 = (1 −γk)xk + γkβ lmo(∇f(xk)), (CG)

where β > 0 is the radius of norm-ball constraint and γk > 0 is some stepsize to be defined. The simplicial combination ensures that the iterates remain within the constraint set βD and, as a result, ensure that ∥xk∥≤β for all k.

The CG method is not necessarily a descent method. For the classical open-loop stepsize choice γk = 2/k+2, it is possible to step too far in the direction given by the lmo, since the stepsize does not decrease near a critical point. Naively adopting the adaptive stepsize choice from GGNC does not seem appropriate in the constrained case, since ∥dk∥∗might not necessarily be zero at a solution. Instead, we will argue that the correct analog of clipping in the constrained setting corresponds to a clipped version of the Frank-Wolfe short step. Like GGNC, this stepsize ensures an analogous descent property.

<!-- Page 5 -->

The short step is almost an immediate consequence of the L-smoothness descent lemma, from which we have f(xk+1) ≤f(xk) −γk ⟨∇f(xk), xk −β lmo(∇f(xk))⟩+ γ2 k

L 2∥xk −β lmo(∇f(xk)∥2 (2)

≤f(xk) −γk ⟨∇f(xk), xk −β lmo(∇f(xk))⟩+ 2γ2 kLβ2. (3)

By optimizing this bound with respect to γk, we arrive at two variants of the short step γk

(2)= min{1, ⟨∇f(xk),xk−β lmo(∇f(xk))⟩

L∥xk−β lmo(∇f(xk)∥2 } or γk

(3)= min{1, ⟨∇f(xk),xk−β lmo(∇f(xk))⟩

4Lβ2 }

where the second variant is useful when the norm ∥· ∥is expensive to compute. What is particularly noteworthy of these stepsize choices is that they lead to descent, i.e., f(xk+1) ≤f(xk), by construction. We extend these stepsize choices to the stochastic case with Algorithm 2, where we propose a slightly different parameterization given by ηk = min{ρ, ⟨dk,xk−β lmo(dk)⟩

∥xk−β lmo(dk)∥2 } or ηk = min{ρ, ⟨dk,xk−β lmo(dk)⟩

4β2 }.

A careful reader might have noticed the similarity between the short step in Algorithm 2 and gradient clipping in Algorithm 1. These schemes are indeed equivalent when vk is appropriately modified in Algorithm 2 to be −β lmo(dk). This connection motivates our parameterization of the updates in Algorithm 2, which are scaled by βγηk, so that the following holds βγηk = βγ min{ρ, −⟨dk,β lmo(dk)⟩

∥β lmo(dk)∥2 } = βγ min{ρ, β∥dk∥∗ ∥β lmo(dk)∥2 } = βγ min{ρ, β∥dk∥∗ β2 } = γ min{ρ, ∥dk∥∗}.

The modified Step 7 of Algorithm 2 then becomes xk+1 = xk + γ min{ρ, ∥dk∥∗} lmo(dk)

which is exactly what is used in GGNC.

## 3.1 Norm choices

## Algorithm

1 and Algorithm 2 crucially generalize beyond the Euclidean case of Clipped GD. The following section focuses on the unconstrained variant (Algorithm 1) for simplicity, but its constrained counterpart follows in a straightforward way through Algorithm 2. Sign A simple non-Euclidean example is the ℓ∞vector norm for which GGNC reduces to a sign-based update xk+1 = xk −γηk sign(dk) (Clipped Sign) where ηk:= min{ρ, ∥dk∥1}. The update is dense in the sense that each coordinate undergoes the same magnitude change. Spectral The matrix analog of the ℓ∞norm is the Schatten-∞matrix norm, a.k.a. the spectral norm, which induces the following update xk+1 = xk −γηkUk(Vk)⊤ (Clipped Spectral)

where the reduced singular value decomposition (SVD) is given as dk = Uk diag(σk)(Vk)⊤. The dual norm can be computed given the lmo as ∥σk∥1 = ∥dk∥S1 = −⟨dk, lmo(dk)⟩= −tr(lmo(dk)⊤dk) = −flatten(lmo(dk))⊤flatten(dk), where ∥· ∥S1 is the Schatten-1 norm, a.k.a. the nuclear norm. This scheme is a clipped variant of the stochastic spectral descent method [Carlson et al., 2015b,a]. Product norm The neural networks in deep learning consist of multiple layers and it will therefore be useful to consider what we will call a product norm. Consider x = (W1,..., WD). A norm of x can be composed using norms on {Wl}l∈[D]:

∥x∥= ∥(1 r1 ∥W1∥W1,..., 1 rD ∥WD∥WD)∥X for radius parameters rl > 0. Notable choices of ∥· ∥X include the ℓ1-norm [Flynn, 2017] and the ℓ∞-norm choice made by the modular norm [Large et al., 2024]. Interestingly, if ∥·∥X is the max-norm, ∥· ∥X = ∥· ∥∞, then:

(i) The lmos can be computed separately as lmoX(x) = {r1 lmoW1(W1),..., rD lmoWD(WD)}

(ii) The dual norm requires summing over all l elements, i.e., ∥x∥∗= PD l=1

1 rl ∥Wl∥Wl,∗.

<!-- Page 6 -->

As a particular example, consider the LARS optimizer [You et al., 2017], which performs normalized SGD layer-wise. The update rule can be written in terms of the lmo-based scheme uCG with the norm choice ∥x∥= maxl ∥Wl∥F. Writing the analog sharp-operator based scheme (i.e., SD), we see that it does not correspond to simply removing the normalization as for the ℓ2 norm. Instead, using the relationship (1), we see that the correct form for the hybrid GGNC method is

Wk+1 l = Wk l −γ min{ρ, P i ∥dk i ∥F)}

dk l ∥dk l ∥F ∀l ∈[D]

where dk = {dk

1,..., dk D} and γ > 0 is the stepsize. Through this duality, we see that while the lmo only requires local information, the dual norm computation (and consequently also the sharp-operator in SD) requires global information.

In Algorithms 3 and 4 of the appendix we specialize Algorithms 1 and 2 to the particular case where ∥· ∥X is the max-norm. The resulting algorithms can be seen as clipped variants of the (unconstrained) Scion algorithm [Pethick et al., 2025] so we refer to them as (unconstrained) ClippedScion.

## 4 Analysis

Why might it be useful to consider a hybrid of SD and uCG? As we will see, the convergence properties of the two methods are complementary.

One can show for SD under L-smoothness that f(xk+1) ≤f(xk) −γ(1 −γL/2)∥∇f(xk)∥2

∗.

In other words, SD is a descent method in the sense that it decreases the function value f(xk) at every iteration. The price we pay for this descent is that the stepsize needs to be taken sufficiently small, specifically as γ < 2/L.

On the other hand, under the same L-smoothness assumption, uCG instead satisfies f(xk+1) ≤f(xk) −γρ∥∇f(xk)∥∗+ Lγ2ρ2

2.

Notice that this is not a descent method, due to the positive contribution of Lγ2ρ2

2. However, there are no restrictions on the stepsize, and we can in fact show a fast rate of O(1/k) for the norm of the gradient with a constant stepsize (as opposed to O(1/

√ k) of SD), albeit only to a neighborhood whose radius is proportional to γρ, as we formalize in the following result. Proposition 4.1. Suppose f is L-smooth with respect to ∥· ∥∗and denote f ⋆= infx∈X f(x). Then, the iterates {xk}k∈N∗of uCG satisfy, for all n ∈N∗, min 1≤k≤n ∥∇f(xk)∥∗≤1 n

Pn k=1 ∥∇f(xk)∥∗≤f(x1)−f ⋆ γρn + Lγρ

2.

Recall that GGNC reduces to uCG when the gradient norm is large, so we can expect in the early phase GGNC will converge rapidly to a neighborhood of size Lγρ

2. If the gradient norm is small in this region, then GGNC reduces to SD, which converges to an exact critical point even with constant stepsize and which can adapt to the loss landscape through the gradient norm.

We can make this intuition precise by analyzing these algorithms under the following generalization of (L0, L1)-smoothness to arbitrary norms. Assumption 4.2. The gradient ∇f is said to be (L0,L1)-smooth with L0, L1 ∈[0, ∞) if, for all x, y ∈X with ∥x −y∥≤ 1 L1, it holds

∥∇f(x) −∇f(y)∥∗≤(L0 + L1∥∇f(x)∥∗)∥x −y∥. (4)

## 4.1 Deterministic case

We now proceed to generalizing Koloskova et al. [2023, Thm. 2.1] in the deterministic case. The main argument relies on establishing that GGNC (Algorithm 1) is a descent method even under the generalized (L0, L1)-smoothness assumption, which enables the scheme to converge even for a fixed, horizon-independent stepsize γ. For the remainder of the paper, we will always denote f ⋆:= infx∈X f(x) (where it is understood this infimum is taken over βD for constrained problems) and ∆:= f(x1) −f ⋆.

<!-- Page 7 -->

Theorem 4.3. Suppose Theorem 4.2 holds and let n ∈N∗. Consider {xk}1≤k≤n generated by GGNC with dk = ∇f(xk), and γ ≤1/(L0+ρL1). Then, the following holds min 1≤k≤n ∥∇f(xk)∥∗≤ q

∆ γn + 2∆ γρn.

Specifically, with ρ = L0

L1 and γ = 1 L0, we have min 1≤k≤n ∥∇f(xk)∥∗≤ q

L0∆ n + 2L1∆ n.

Remark 4.4. Note that the condition ∥xk −xk+1∥≤1/L1 of Theorem 4.2 required in the proof is always satisfied, since γρ ≤1/L1 holds for any ρ. We note that descent can also be established for SD with an adaptive stepsize γk = 1/L0+L1∥∇f(xk)∥∗(see e.g., Balles et al. [2020, C.2.2], which uses a definition of (L0, L1)-smoothness based on the Hessian).

In contrast with GGNC, uCG is not a descent method and requires a diminishing stepsize to converge as suggested by the following theorem. The uCG method trades off the descent property with being agnostic to the Lipschitz constant L0. Theorem 4.5. Suppose Theorem 4.2 holds and let n ∈N∗. Consider {xk}1≤k≤n generated by uCG with γρ < 1/2L1. Then, the following holds min 1≤k≤n ∥∇f(xk)∥∗≤2∆ γρn + 2L0γρ.

Remark 4.6. The assumption that γρ ≤1/2L1 can be relaxed to γρ < 1/L1 while still ensuring convergence, modulo a different constant in the convergence rate.

Let us now turn to the constrained case. The following theorem establishes a convergence rate for Algorithm 2 in the deterministic setting, i.e., with dk = ∇f(xk). The convergence rate is established for a quantity called the Wolfe-gap, max u∈βD⟨∇f(x), x −u⟩, which, when equal to 0, certifies that x is a critical point for the constrained problem. It is the equivalent of the dual norm of the gradient but for constrained problems, since the gradient might not vanish at a critical point in the constrained setting. The theorem also includes an assumption that f is L-smooth rather than (L0, L1)-smooth. Because the iterates of Algorithm 2 are guaranteed to never leave the compact set βD, L-smoothness is implied by (L0, L1)-smoothness here. Theorem 4.7. Suppose f is L-smooth and let n ∈N∗. Consider {xk}1≤k≤n generated by Algorithm 2 with dk = ∇f(xk), γ ≤1

L, and ρ ≤L so that γρ ≤1. Then, for all u ∈βD, the following holds min 1≤k≤n⟨∇f(xk), xk −u⟩≤2β q

∆ γn + 2∆ γρn.

## 4.2 Stochastic case

We consider the following standard assumption about the bias and variance of the stochastic oracle. Assumption 4.8. For the stochastic gradient estimator ∇f(·, ξ): X →Rd the following holds.

(i) Unbiased: Eξ

∇f(x, ξ) = ∇f(x) ∀x ∈X.

(ii) Bounded variance: Eξ h

∥∇f(x, ξ) −∇f(x)∥2

2 i

≤σ2 ∀x ∈X, σ ≥0.

In order to establish convergence in what follows, an important quantity to introduce is the error produced by the stochastic estimator dk, which we denote by λk:= dk −∇f(xk).

We establish the following order optimal convergence guarantee for GGNC under (L0, L1)-smoothness using a momentum-based estimator. These convergence results for clipping with momentum appear to be new, even in the Euclidean case. Theorem 4.9. Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 1 with a constant stepsize γ ≤1/L0 and γρ ≤1/2L1. Then,

E[∥∇f(¯xn)∥∗] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ

<!-- Page 8 -->

where ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 O( q

E[∥λk∥2

2] + E[∥λk∥2 2]).

Furthermore, assuming f is L-smooth3 and taking α = 1/√n, γ = 1/√nL0 and ρ = L0/2n1/4L1 such that γρ = 1/2n3/4L1 we have that

E[∥∇f(¯xn)∥∗] ≤O 1 n1/4

. Remark 4.10. For ease of exposition, the guarantee is presented with horizon-dependent parameter choices, but the result can be extended to an any time guarantee in a straightforward manner by choosing the parameters as a function of k instead of n and modifying the proofs accordingly.

In the constrained case, we have the following convergence guarantee for SCG with a clipped short step (Algorithm 2) using a momentum-based estimator. To the best of our knowledge, this is the first convergence proof using the short step in the stochastic setting. Theorem 4.11. Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 2 (Variant 1) with a constant stepsize γ ≤1/L √n and ρ ≤1/n1/4. Then, for all u ∈βD,

E[⟨∇f(¯xn), ¯xn −u⟩] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ where ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 O( q

E∥λk∥2

2 + E∥λk∥2 2).

Furthermore, taking α = 1/√n, γ = 1/(L √n) and ρ = 1/n1/4 such that γρ = 1/(Ln3/4) we have that

E[⟨∇f(¯xn), ¯xn −u⟩] ≤O 1 n1/4

.

We additionally provide an identical guarantee for Algorithm 2 (Variant 2) in the appendix.

## 5 Related work

(L0, L1)-smoothness An (L0, L1)-smoothness condition was introduced based on the Hessian in [Zhang et al., 2019] and later generalized to the first-order notion that we extend to the non-Euclidean case [Zhang et al., 2020]. (L0,L1)-smoothness was used to analyze signSGD under heavy-tailed noise assumptions in Kornilov et al. [2025]. A coordinate-wise (L0,L1)-smoothness condition has also been considered for analyzing a generalized version of signSGD [Crawshaw et al., 2022].

In the Euclidean case, a descent property under (L0, L1)-smoothness was shown for both gradient clipping [Zhang et al., 2020, Koloskova et al., 2023] and gradient descent with an appropriate adaptive stepsize as studied in the two concurrent works Gorbunov et al. [2024] and Vankov et al. [2024].

Parameter-agnostic In the deterministic case, gradient descent with backtracking line-search was shown to converge under (L0, L1)-smoothness without knowledge of the Lipschitz constants [Hübler et al., 2024]. For (star)-convex problems, an interesting connection was established between gradient norm clipping and the Polyak stepsize in Takezawa et al. [2024] and further analyzed in Gorbunov et al. [2024] and Vankov et al. [2024]. The adaptive stepsize removes the need for knowing both L0 and L1. Unfortunately, the Polyak stepsize is deeply tied to the Euclidean and (star)-convex structure and thus does not seem to be directly extendable to our more general setting.

In the stochastic case, the current best known parameter-agnostic method introduces an undesirable exponential dependency on L1 in the complexity [Hübler et al., 2024]. However, knowledge of L0 can be removed without such issues through either an AdaGrad type stepsize [Wang et al., 2023, Faw et al., 2023] or normalized gradient descent with momentum [Cutkosky and Mehta, 2020] as shown in Hübler et al. [2024]. This mirrors results from the online learning community where both AdaGrad and gradient normalization are known to adapt to Hölder smoothness [Orabona, 2023].

Short step In contrast with gradient descent, the Frank-Wolfe algorithm [Frank et al., 1956] does not ensure descent with an open-loop stepsize even in the deterministic setting. Descent can be ensured by an adaptive stepsize known as the short step, originally introduced by Frank & Wolfe [Frank et al., 1956] and extended by Rubinov & Dem’yanov [Dem’yanov and Rubinov, 1968]. See Pokutta [2024] for an expository treatment.

3Only local Lipschitz is needed in the sense that the condition only needs to hold for (x, y) satisfying ∥x −y∥≤1/L1. It is also possible to replace L with Ln:= maxk≤n L0 + L1∥f(xk)∥∗, e.g., as is done in [Koloskova et al., 2023, Thm. 2.3].

<!-- Page 9 -->

Spectral norm methods Clipped Spectral can be viewed as a hybrid method between the stochastic spectral descent [Carlson et al., 2015b] and the Muon optimizer [Jordan et al., 2024b], with some crucial differences.

Muon builds the gradient estimator dk differently. Specifically they take dk = ∇f(xk, ξk) + βdk−1 if Nesterov momentum is disabled. This is equivalent to our choice dk = α∇f(xk, ξk) + (1 −α)dk−1 for LMO-based schemes, since the LMO is scale-invariant (i.e., lmo(a · s) = lmo(s) for a > 0) [Pethick et al., 2025]. However, for SD this equivalence no longer holds (in fact we have [a · s]♯= a[s]♯for a ∈R). The appropriate choice of dk, which generalizes to SD and GGNC, turns out to be the convex combination.

Stochastic spectral descent [Carlson et al., 2015b] does not construct a gradient estimator and instead takes dk = ∇f(xk, ξk). This restricts their convergence result to the case of (mild) relative noise.

In this sense, Clipped Spectral could just as well be called Clipped Muon (not to be confused with the unrelated MuonClip [Team et al., 2025]) but we prefer Clipped Spectral as the algorithm itself is not tied to momentum nor to Newton-Schulz, as the name Muon fundamentally is.

Tuddenham et al. [2022] also studied an optimization algorithm focused on orthogonalization, however they orthogonalize before doing the momentum step. Pethick et al. [2025] analyzed a more general algorithm called Averaged LMO Directional Descent which admits as a special case the algorithm studied in Tuddenham et al. [2022]; their empirical and theoretical findings found this algorithm to be worse than orthogonalization after the momentum step, e.g., the Scion family of algorithms [Pethick et al., 2025].

We note that many works have recently analyzed the convergence behavior of algorithms using spectral LMOs like Muon and Scion, starting first with Pethick et al. [2025], Li and Hong [2025] and then Kovalev [2025], Sfyraki and Wang [2025], but always under L-smoothness assumptions, in contrast to this work.

Modular norm [Large et al., 2024] introduced a norm choice for neural networks and established a smoothness condition for a given neural network provided the parameter remains bounded. The dual norm computation needed in GGNC is particularly easy to implement in the accompanying Modula software package since ∥d∥∗:= −flatten(lmo(d))⊤flatten(d), which in Modula code reads as dual_norm=-sum(model.dualize(d)*d).

Weight decay Weight decay [Pratt, 1992] is a crucial component in deep learning and has become standard in training modern neural networks through its integration with Adam [Loshchilov and Hutter, 2017]. When combined with LMO based updates such as sign descent and the normalized gradient descent the resulting methods can be seen as instantiations of the conditional gradient method for constrained optimization problems [Chen et al., 2023, D’Angelo et al., 2023, Xie and Li, 2024, Pethick et al., 2025]. Our adaptive stepsize in Algorithm 2 effectively scales the weight decay as well as the update. This is similar to scheduled weight decay [Xie et al., 2023] which uses the adaptive stepsize in Adam to also scale the weight decay parameter.

## 6 Experiments

For the norm choice of Scion and ClippedScion we use the (Sign →Spectral →Sign) and (Spectral →Spectral →Sign) configurations for language modeling and image classication respectively (see Pethick et al. [2025, Tbl. 2-4] for the associated scaling factors). To compute the spectral lmo we use the efficient implementation provided in Jordan et al. [2024b] of the Newton-Schultz iteration proposed in Bernstein and Newhouse [2024]. There have been recent efforts to move beyond the “N” (Newton-Schulz) in Muon, the most popular algorithm computing the spectral LMO, through alternative subroutines; our algorithm is compatible with these alternatives, like the optimized PolarExpress routine [Amsel et al., 2025] or power iterations [Ahn et al., 2025, Vogels et al., 2019], although we do not explore them here.

Image classification We test on a convolutional neural network (CNN) on the CIFAR10 dataset. Hyperparameters can be found in Table 2 in Section C. We consider both a fixed stepsize setting and stepsize scheduling using linear rampdown to investigate if the theoretical results are predictive of practice. We report the experimental results in Figure 1 where mean and standard deviation are computed over 5 independent runs.

<!-- Page 10 -->

0 20 30 40 50 60 70 80 Epoch

0.5

0.6

0.7

0.8

0.9

Test Accuracy

Adam Unconstrained Scion Unconstrained ClippedScion

0 250 500 750 Iteration k

0

500

Gradient norm dk

Unconstrained ClippedScion Clipping threshold

**Figure 1.** For CIFAR10 experiments with fixed stepsize clipping leads to a substantial improvement.

## 0 Iteration k

3.0

3.1

3.2

3.3

3.4

3.5

3.6

Validation Loss

Adam Unconstrained Scion Unconstrained ClippedScion

10% speedup

Iteration k

Gradient norm dk

Unconstrained ClippedScion Clipping threshold

**Figure 2.** For fixed stepsize comparison clipping improves over Scion by more than a 10% speedup on NanoGPT (1B). We observe similar gains on the smaller 124M parameter model size (cf. Section C).

We find that clipping can substantially improve the test accuracy in the fixed stepsize setting, when the gradient norm (i.e. ∥dk∥∗= ⟨dk, vk⟩) is decreasing. This separation is in agreement with the theoretical separation between Theorem 4.3 and Theorem 4.5 on fixed stepsizes. In the constrained case (Algorithm 2) we surprisingly find that ⟨dk, vk⟩is increasing (cf. Figure 6 in Section C) which requires further investigation. With stepsize scheduling we observe that clipping (i.e., Unconstrained ClippedScion) and normalization (i.e., Unconstrained Scion) achieve similar performance, which aligns with the matching theoretical rates of GGNC (Theorem 4.9) and uSCG (Pethick et al. [2025, Thm. 5.4]) in the stochastic case when stepsizes are taken decreasing.

We also evaluate the unconstrained case (Algorithm 1) using Vision Transformers (ViT) on the ImageNet dataset. We train a DeiT-base model using the DeiT codebase [Touvron et al., 2021] with replacing LayerNorm by RMS norm following [Pethick et al., 2025]. Table 3 in Section C contains the hyperparameter details. As shown in Figure 7 (Section C), Unconstrained ClippedScion achieves an 11% speedup over Unconstrained Scion, even though its gradient norm (∥dk∥∗) is increasing. This observation requires further exploration.

NanoGPT We additionally test on NanoGPT Karpathy [2023] in Figure 2 with modernizations following [Jordan et al., 2024a]: rotary embeddings are used instead of positional embeddings, RMS norm is used instead of LayerNorm, and the ReLU2 [So et al., 2021] instead of GELU activation function. All methods are trained for 5100 iterations with a batchsize of 512 and context length of 1024 on the FineWeb dataset (see Table 4 Section C for further details). The empirical observations matches those for CIFAR10 experiments.

## 7 Conclusion

We have shown that clipping can be extended to non-Euclidean settings and even constrained problems by establishing a precise connection to the Frank-Wolfe short step. A descent property was established under a generalized notion of (L0, L1)-smoothness, which opens up a range of interesting directions:

The descent property both in the unconstrained and constrained case enables integration with adaptive stepsize choices such as AdaGrad and backtracking line-search.

The non-Euclidean notion of (L0, L1)-smoothness we introduce might be a suitable condition to study for neural networks. Large et al. [2024] showed that neural networks are smooth in the modular norm provided that the parameters are constrained. However, in practice, violating the constraints seem to be unproblematic for optimization, which suggests that a looser smoothness assumption might hold such as Theorem 4.2.

<!-- Page 11 -->

## Acknowledgment

This work was supported as part of the Swiss AI Initiative by a grant from the Swiss National Supercomputing Centre (CSCS) under project ID a06 on Alps. This work was supported by the Swiss National Science Foundation (SNSF) under grant number 200021_205011. This work was supported by Hasler Foundation Program: Hasler Responsible AI (project number 21043). Research was sponsored by the Army Research Office and was accomplished under Grant Number W911NF- 24-1-0048.

## References

Kwangjun Ahn, Byron Xu, Natalie Abreu, Ying Fan, Gagik Magakyan, Pratyusha Sharma,

Zheng Zhan, and John Langford. Dion: Distributed orthonormalized updates. arXiv preprint arXiv:2504.05295, 2025.

Noah Amsel, David Persson, Christopher Musco, and Robert M Gower. The polar express: Optimal matrix sign methods and their application to the muon algorithm. arXiv preprint arXiv:2505.16932, 2025.

Lukas Balles, Fabian Pedregosa, and Nicolas Le Roux. The geometry of sign gradient descent. arXiv preprint arXiv:2002.08056, 2020.

Jeremy Bernstein and Laker Newhouse. Old optimizer, new norm: An anthology. arXiv preprint arXiv:2409.20325, 2024.

David Carlson, Volkan Cevher, and Lawrence Carin. Stochastic spectral descent for restricted boltzmann machines. In Artificial Intelligence and Statistics, pages 111–119. PMLR, 2015a.

David Carlson, Ya-Ping Hsieh, Edo Collins, Lawrence Carin, and Volkan Cevher. Stochastic spectral descent for discrete graphical models. IEEE Journal of Selected Topics in Signal Processing, 10 (2):296–311, 2015b.

Lizhang Chen, Bo Liu, Kaizhao Liang, and Qiang Liu. Lion secretly solves constrained optimization:

As lyapunov predicts. arXiv preprint arXiv:2310.05898, 2023.

Michael Crawshaw, Mingrui Liu, Francesco Orabona, Wei Zhang, and Zhenxun Zhuang. Robustness to unbounded smoothness of generalized signsgd. Advances in neural information processing systems, 35:9955–9968, 2022.

Ashok Cutkosky and Harsh Mehta. Momentum improves normalized sgd. In International conference on machine learning, pages 2260–2268. PMLR, 2020.

Francesco D’Angelo, Maksym Andriushchenko, Aditya Varre, and Nicolas Flammarion. Why do we need weight decay in modern deep learning? arXiv preprint arXiv:2310.04415, 2023.

VF Dem’yanov and AM Rubinov. Minimization of functionals in normed spaces. SIAM Journal on

Control, 6(1):73–88, 1968.

Matthew Faw, Litu Rout, Constantine Caramanis, and Sanjay Shakkottai. Beyond uniform smooth- ness: A stopped analysis of adaptive sgd. In The Thirty Sixth Annual Conference on Learning Theory, pages 89–160. PMLR, 2023.

Thomas Flynn. The duality structure gradient descent algorithm: analysis and applications to neural networks. arXiv preprint arXiv:1708.00523, 2017.

Marguerite Frank, Philip Wolfe, et al. An algorithm for quadratic programming. Naval research logistics quarterly, 3(1-2):95–110, 1956.

Eduard Gorbunov, Nazarii Tupitsa, Sayantan Choudhury, Alen Aliev, Peter Richtárik, Samuel Horváth, and Martin Takáˇc. Methods for convex (l_0, l_1)-smooth optimization: Clipping, acceleration, and adaptivity. arXiv preprint arXiv:2409.14989, 2024.

<!-- Page 12 -->

Florian Hübler, Junchi Yang, Xiang Li, and Niao He. Parameter-agnostic optimization under relaxed smoothness. In International Conference on Artificial Intelligence and Statistics, pages 4861–4869. PMLR, 2024.

Keller Jordan. Cifar-10 airbench, 2024. URL https://github.com/KellerJordan/ cifar10-airbench.

Keller Jordan, Jeremy Bernstein, Brendan Rappazzo, @fernbear.bsky.social, Boza Vlado, You

Jiacheng, Franz Cesista, Braden Koszarsky, and @Grad62304977. modded-nanogpt: Speedrunning the nanogpt baseline, 2024a. URL https://github.com/KellerJordan/modded-nanogpt.

Keller Jordan, Yuchen Jin, Vlado Boza, You Jiacheng, Franz Cecista, Laker Newhouse, and Jeremy

Bernstein. Muon: An optimizer for hidden layers in neural networks, 2024b. URL https: //kellerjordan.github.io/posts/muon/.

Andrej Karpathy. nanoGPT. https://github.com/karpathy/nanoGPT, 2023. Accessed: 2025-

01-25.

Jonathan A Kelner, Yin Tat Lee, Lorenzo Orecchia, and Aaron Sidford. An almost-linear-time algorithm for approximate max flow in undirected graphs, and its multicommodity generalizations. In Proceedings of the twenty-fifth annual ACM-SIAM symposium on Discrete algorithms, pages 217–226. SIAM, 2014.

Anastasia Koloskova, Hadrien Hendrikx, and Sebastian U Stich. Revisiting gradient clipping:

Stochastic bias and tight convergence guarantees. In International Conference on Machine Learning, pages 17343–17363. PMLR, 2023.

Nikita Kornilov, Philip Zmushko, Andrei Semenov, Mark Ikonnikov, Alexander Gasnikov, and

Alexander Beznosikov. Sign operator for coping with heavy-tailed noise in non-convex optimization: High probability bounds under (l_0, l_1)-smoothness. arXiv preprint arXiv:2502.07923, 2025.

Dmitry Kovalev. Understanding gradient orthogonalization for deep learning via non-euclidean trust-region optimization. arXiv preprint arXiv:2503.12645, 2025.

Tim Large, Yang Liu, Minyoung Huh, Hyojin Bahng, Phillip Isola, and Jeremy Bernstein. Scalable optimization in the modular norm. arXiv preprint arXiv:2405.14813, 2024.

Jiaxiang Li and Mingyi Hong. A note on the convergence of muon and further. arXiv e-prints, pages arXiv–2502, 2025.

Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.

Tomáš Mikolov et al. Statistical language models based on neural networks. 2012.

Aryan Mokhtari, Hamed Hassani, and Amin Karbasi. Stochastic conditional gradient methods: From convex minimization to submodular maximization. Journal of machine learning research, 21(105): 1–49, 2020.

Yu Nesterov. Efficiency of coordinate descent methods on huge-scale optimization problems. SIAM

Journal on Optimization, 22(2):341–362, 2012.

Francesco Orabona. Normalized gradients for all. arXiv preprint arXiv:2308.05621, 2023.

Thomas Pethick, Wanyun Xie, Kimon Antonakopoulos, Zhenyu Zhu, Antonio Silveti-Falls, and

Volkan Cevher. Training deep learning models with norm-constrained lmos. arXiv preprint arXiv:2502.07529, 2025.

Sebastian Pokutta. The frank-wolfe algorithm: a short introduction. Jahresbericht der Deutschen

Mathematiker-Vereinigung, 126(1):3–35, 2024.

Lorien Y Pratt. Non-literal transfer among neural network learners. Colorado School of Mines:

MCS-92-04, 1992.

<!-- Page 13 -->

Maria-Eleni Sfyraki and Jun-Kun Wang. Lions and muons: Optimization via stochastic frank-wolfe.

arXiv preprint arXiv:2506.04192, 2025.

David So, Wojciech Ma´nke, Hanxiao Liu, Zihang Dai, Noam Shazeer, and Quoc V Le. Searching for efficient transformers for language modeling. Advances in neural information processing systems, 34:6010–6022, 2021.

Yuki Takezawa, Han Bao, Ryoma Sato, Kenta Niwa, and Makoto Yamada. Polyak meets parameter- free clipped gradient descent. arXiv preprint arXiv:2405.15010, 2024.

Kimi Team, Yifan Bai, Yiping Bao, Guanduo Chen, Jiahao Chen, Ningxin Chen, Ruijue Chen, Yanru

Chen, Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. arXiv preprint arXiv:2507.20534, 2025.

Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre Sablayrolles, and Hervé

Jégou. Training data-efficient image transformers & distillation through attention. In International conference on machine learning, pages 10347–10357. PMLR, 2021.

Mark Tuddenham, Adam Prügel-Bennett, and Jonathan Hare. Orthogonalising gradients to speed up neural network optimisation. arXiv preprint arXiv:2202.07052, 2022.

Daniil Vankov, Anton Rodomanov, Angelia Nedich, Lalitha Sankar, and Sebastian U Stich. Op- timizing (l_0, l_1)-smooth functions by gradient methods. arXiv preprint arXiv:2410.10800, 2024.

Thijs Vogels, Sai Praneeth Karimireddy, and Martin Jaggi. Powersgd: Practical low-rank gradient compression for distributed optimization. Advances in Neural Information Processing Systems, 32, 2019.

Bohan Wang, Huishuai Zhang, Zhiming Ma, and Wei Chen. Convergence of adagrad for non-convex objectives: Simple proofs and relaxed assumptions. In The Thirty Sixth Annual Conference on Learning Theory, pages 161–190. PMLR, 2023.

Shuo Xie and Zhiyuan Li. Implicit bias of AdamW: ℓ∞norm constrained optimization. arXiv preprint arXiv:2404.04454, 2024.

Zeke Xie, Zhiqiang Xu, Jingzhao Zhang, Issei Sato, and Masashi Sugiyama. On the overlooked pitfalls of weight decay and how to mitigate them: A gradient-norm perspective. Advances in Neural Information Processing Systems, 36:1208–1228, 2023.

Yang You, Igor Gitman, and Boris Ginsburg. Large batch training of convolutional networks. arXiv preprint arXiv:1708.03888, 2017.

Bohang Zhang, Jikai Jin, Cong Fang, and Liwei Wang. Improved analysis of clipping algorithms for non-convex optimization. Advances in Neural Information Processing Systems, 33:15511–15521, 2020.

Jingzhao Zhang, Tianxing He, Suvrit Sra, and Ali Jadbabaie. Why gradient clipping accelerates training: A theoretical justification for adaptivity. arXiv preprint arXiv:1905.11881, 2019.

<!-- Page 14 -->

## Appendix

Table of Contents

A Preliminaries 15

B Proofs for Section 4 (Analysis) 15

C Experiments 29

<!-- Page 15 -->

## Algorithm

## 3 Unconstrained ClippedScion Input:

Horizon n, init. x1 = (W1

1,..., W1 D), d0 = 0, momentum αk ∈(0, 1], stepsize γ ∈(0, 1), radii rl ∈R+, and ρ > 0.

1: for k = 1,..., n −1 do 2: Sample ξk ∼P 3: dk ←αk∇f(xk, ξk) + (1 −αk)dk−1

4: vk l ←−rl lmo∥·∥Wl (dk l) ∀1 ≤l ≤D

5: ηk ←min{ρ, PD l=1 ⟨dk l, vk l ⟩} 6: xk+1 ←xk −γηkvk

7: Choose ¯xn uniformly at random from {x1,..., xn} Return ¯xn

## Algorithm

## 4 ClippedScion Input:

Horizon n, init. x1 = (W1

1,..., W1 D) ∈r1D1 × · · · × rDDD, d0 = 0, stepsize γ ∈(0, 1), momentum αk ∈(0, 1]

1: for k = 1,..., n do 2: Sample ξk ∼P 3: dk ←αk∇f(xk, ξk) + (1 −αk)dk−1

4: vk l ←xk l −rl lmo∥·∥Wl (dk l) ∀1 ≤l ≤D

5: Variant 1: ηk ←min{ρ,

PD l=1⟨dk l,vk l ⟩ maxD l=1 ∥vk l ∥2

Wl

}

6: Variant 2: ηk ←min{ρ,

PD l=1⟨dk l,vk l ⟩ 4 } 7: xk+1 ←xk −γηkvk

8: Choose ¯xn uniformly at random from {x1,..., xn} Return ¯xn

A Preliminaries

Throughout, L-smoothness is defined as follows. Definition A.1. A gradient mapping ∇f: X →Rd is said to be L-smooth with L ∈(0, ∞) if for all x, y ∈X it holds that,

∥∇f(x) −∇f(y)∥∗≤L∥x −y∥. (5)

The sharp operator has the following properties

⟨s, s♯⟩= ∥s♯∥2 = ∥s∥2

∗ (6)

See Kelner et al. [2014, App. A.1] for the proof.

B Proofs for Section 4 (Analysis)

Proposition 4.1. Suppose f is L-smooth with respect to ∥· ∥∗and denote f ⋆= infx∈X f(x). Then, the iterates {xk}k∈N∗of uCG satisfy, for all n ∈N∗, min 1≤k≤n ∥∇f(xk)∥∗≤1 n

Pn k=1 ∥∇f(xk)∥∗≤f(x1)−f ⋆ γρn + Lγρ

2.

Proof. By the descent lemma for L-smooth functions applied at the points xk and xk+1 and the definition of xk+1 we have, for all k ≥1, f(xk+1) ≤f(xk) −γρ∥∇f(xk)∥∗+ L

2γ2ρ2.

Summing from k = 1 to k = n, and dividing by n gives

1 n

Pn k=1 ∥∇f(xk)∥∗≤f(x1)−f ⋆ γρn + Lγρ

2.

Remarking that the minimum summand is smaller than the average completes the proof. □

<!-- Page 16 -->

B.1 Deterministic case

Recall the notation ∆:= f(x1) −f ⋆. Theorem 4.3. Suppose Theorem 4.2 holds and let n ∈N∗. Consider {xk}1≤k≤n generated by GGNC with dk = ∇f(xk), and γ ≤1/(L0+ρL1). Then, the following holds min 1≤k≤n ∥∇f(xk)∥∗≤ q

∆ γn + 2∆ γρn.

Specifically, with ρ = L0

L1 and γ = 1 L0, we have min 1≤k≤n ∥∇f(xk)∥∗≤ q

L0∆ n + 2L1∆ n.

Proof. For each 1 ≤k ≤n, we can write the formula for xk+1 as follows xk+1 = xk −γτk[∇f(xk)]♯ with τk = min{1, ρ ∥∇f(xk)∥∗}.

From (L0, L1)-smoothness and properties of the sharp-operator ⟨s, s♯⟩= ∥s♯∥2 = ∥s∥2

∗, we have f(xk+1) ≤f(xk) + ⟨∇f(xk), −γτk∇f(xk)⟩+ L0+∥∇f(xk)∥∗L1

2 (γτk∥∇f(xk)∥∗)2

= f(xk) −γτk∥∇f(xk)∥2

∗+ γ2τ2 k 2 (L0 + ∥∇f(xk)∥∗L1)∥∇f(xk)∥2 ∗.

A useful observation is that by definition of τk we have τk∥∇f(xk)∥∗≤ρ, since if ∥∇f(xk)∥∗> ρ then τk = ρ/∥∇f(xk)∥∗, and if ∥∇f(xk)∥∗≤ρ then τk = 1. Thus we can upper-bound the term τk∥∇f(xk)∥∗L1 by ρL1 in the quadratic part, yielding f(xk+1) ≤f(xk) −γτk∥∇f(xk)∥2

∗+ γ2τk

2 (τkL0 + ρL1)∥∇f(xk)∥2 ∗ ≤f(xk) −γτk(1 −γ

2(L0 + ρL1))∥∇f(xk)∥2 ∗ ≤f(xk) −γτk

2 ∥∇f(xk)∥2 ∗.

where the middle inequality uses that τ2 ≤τ since τ ≤1 and the last inequality uses the stepsize choice γ ≤ 1 L0+ρL1.

There are now two cases to consider.

Case I Clipping Active (∥∇f(xk)∥∗> ρ).

Here, we have τk = ρ ∥∇f(xk)∥∗so τk∥∇f(xk)∥2

∗= ρ∥∇f(xk)∥∗. Therefore, the descent inequality in this case reads f(xk+1) ≤f(xk) −ργ

2 ∥∇f(xk)∥∗.

Case II No Clipping (∥∇f(xk)∥∗≤ρ).

In this regime, τk = 1, so the inequality becomes f(xk+1) ≤f(xk) −γ

2∥∇f(xk)∥2 ∗.

This is the familiar descent guaranty for the classical steepest descent method with smooth functions.

By combining the two cases and summing over all k = 1 until n we obtain γ 2 ρ P k∈A ∥∇f(xk)∥∗+ P k<A ∥∇f(xk)∥2

∗

≤f(x1) −f ⋆ where A is the set of indices where clipping is active (Case I). Since each sum is nonnegative, we can conclude that

1 n

P k<A ∥∇f(xk)∥2

∗≤2(f(x1)−f ⋆)

γn and 1 n

P k∈A ∥∇f(xk)∥∗≤2(f(x1)−f ⋆)

γρn. (7)

<!-- Page 17 -->

Recall the following inequality for real numbers: for all a, b > 0, a2 ≥2ab −b2. Applying this with a = ∥∇f(xk)∥∗and b > 0 gives

1 n

P k<A ∥∇f(xk)∥2

∗≥1 n

P k<A(2b∥∇f(xk)∥∗−b2) = 2b n

P k<A ∥∇f(xk)∥∗

−b2(n−|A|)

n.

Substituting this estimate into (7) and using the fact that |A| ≤n gives

2b n

P k<A ∥∇f(xk)∥∗

−b2(n−|A|)

n ≤2(f(x1)−f ⋆)

γn =⇒ 1 n

P k<A ∥∇f(xk)∥∗≤1

2 f(x1)−f ⋆ bγn + b

.

Then, choosing b = q f(x1)−f ⋆ γn simplifies the above to

1 n

P k<A ∥∇f(xk)∥∗≤ q f(x1)−f ⋆ γn.

Now, we can combine both cases to bound the sum over 1 ≤k ≤n as

1 n

Pn k=1 ∥∇f(xk)∥∗≤ q f(x1)−f ⋆ γn + 2(f(x1)−f ⋆)

γρn

Taking the minimum of the summand over 1 ≤k ≤n on the left hand side gives the final result. □

Theorem 4.5. Suppose Theorem 4.2 holds and let n ∈N∗. Consider {xk}1≤k≤n generated by uCG with γρ < 1/2L1. Then, the following holds min 1≤k≤n ∥∇f(xk)∥∗≤2∆ γρn + 2L0γρ.

Proof. We begin by invoking the descent lemma for (L0, L1)-smooth functions at the points xk+1 and xk, which is justified since ∥xk+1 −xk∥= γρ ≤ 1 2L1. Then, applying the definition of xk+1 we get, for all 1 ≤k ≤n, f(xk+1) ≤f(xk) + γρ⟨∇f(xk), vk⟩+ γ2ρ2(L0 + L1∥∇f(xk)∥∗)∥vk∥2

∗ = f(xk) −γρ∥∇f(xk)∥∗+ γ2ρ2(L0 + L1∥∇f(xk)∥∗)

= f(xk) + L0γ2ρ2 + (L1γρ −1)γρ∥∇f(xk)∥∗.

Rearranging the above yields

1 2∥∇f(xk)∥∗≤(1 −L1γρ)∥∇f(xk)∥∗≤f(xk)−f(xk+1) γρ + L0γρ where we have used the assumption that γρ ≤ 1 2L1 in the first inequality above. The desired claim immediately follows. □

Theorem 4.7. Suppose f is L-smooth and let n ∈N∗. Consider {xk}1≤k≤n generated by Algorithm 2 with dk = ∇f(xk), γ ≤1

L, and ρ ≤L so that γρ ≤1. Then, for all u ∈βD, the following holds min 1≤k≤n⟨∇f(xk), xk −u⟩≤2β q

∆ γn + 2∆ γρn.

Proof. We start by applying the descent lemma for L-smooth functions at the points xk+1 and xk to get, for all 1 ≤k ≤n, f(xk+1) ≤f(xk) −γηk⟨∇f(xk), vk⟩+ L

2 γ2η2 k∥vk∥2.

Now, we divide the analysis into two cases depending on whether or not clipping is active.

<!-- Page 18 -->

Case I Clipping active (⟨∇f(xk),vk⟩

∥vk∥2 ≥ρ; ηk = ρ).

In this case, we can use the fact that ⟨∇f(xk), vk⟩≥ρ∥vk∥2 to get f(xk+1) ≤f(xk) −γηk⟨∇f(xk), vk⟩+ L

2 γ2η2 k∥vk∥2

= f(xk) −γρ⟨∇f(xk), vk⟩+ L

2 γ2ρ2∥vk∥2

≤f(xk) −γρ⟨∇f(xk), vk⟩+ L

2 γ2ρ⟨∇f(xk), vk⟩

≤f(xk) −1

2γρ⟨∇f(xk), vk⟩ where the final inequality is due to the assumption that γ ≤1

L. Rearranging this gives γρ

2 ⟨∇f(xk), vk⟩≤f(xk) −f(xk+1).

Case II No clipping (⟨∇f(xk),vk⟩

∥vk∥2 ≤ρ; ηk = ⟨∇f(xk),vk⟩

∥vk∥2).

When clipping is not active, ηk acts like a short step which gives f(xk+1) ≤f(xk) −γηk⟨∇f(xk), vk⟩+ L

2 γ2η2 k∥vk∥2

≤f(xk) −γ⟨∇f(xk), vk⟩2

∥vk∥2 + L

2 γ2 ⟨∇f(xk), vk⟩2

∥vk∥2

≤f(xk) −γ⟨∇f(xk), vk⟩2

∥vk∥2 where the last inequality follows from the assumption that γ ≤1

L. Rearranging this gives γ 4β2 ⟨∇f(xk), vk⟩2 ≤f(xk) −f(xk+1).

Combining both cases Denoting A the set of indices where clipping is active and summing from k = 1 to n we find

X k∈A γρ

2 ⟨∇f(xk), vk⟩+ X k<A γ 4β2 ⟨∇f(xk), vk⟩2 ≤f(x1) −f ⋆ which, since each summand is nonnegative, implies that

1 n

X k∈A

⟨∇f(xk), vk⟩≤2(f(x1) −f ⋆)

γρn and 1 n

X k<A

⟨∇f(xk), vk⟩2 ≤4β2(f(x1) −f ⋆)

γn. (8)

Recall the following inequality for real numbers: for all a, b > 0, a2 ≥2ab −b2. Applying this with a = ⟨∇f(xk), vk⟩and b > 0 gives

1 n

X k<A

⟨∇f(xk), vk⟩2 ≥1 n

X k<A

(2b⟨∇f(xk), vk⟩−b2) = 2b n



X k<A

⟨∇f(xk), vk⟩

−b2(n −|A|)

n.

Substituting this estimate into (8) and using the fact that |A| ≤n gives

2b n



X k<A

⟨∇f(xk), vk⟩

−b2(n −|A|)

n ≤4β2(f(x1) −f ⋆)

γn which implies that

1 n

X k<A

⟨∇f(xk), vk⟩≤1

2

4β2(f(x1) −f ⋆)

bγn + b

!

.

<!-- Page 19 -->

Thus, choosing b = q

4β2(f(x1)−f ⋆) γn simplifies the above to

1 n

X k<A

⟨∇f(xk), vk⟩≤ s

4β2(f(x1) −f ⋆) γn = 2β s f(x1) −f ⋆ γn

Now, we can combine both cases to bound the sum over 1 ≤k ≤n as

1 n n X k=1

⟨∇f(xk), vk⟩≤2β s f(x1) −f ⋆ γn + 2(f(x1) −f ⋆)

γρn

Finally, by lower bounding the left hand side by the minimal summand over 1 ≤k ≤n and using the definition of vk we arrive, for all u ∈βD, at min 1≤k≤n⟨∇f(xk), xk −u⟩≤2

β p f(x1) −f ⋆

√γn + f(x1) −f ⋆ γρn

.

□

B.2 Stochastic case

B.2.1 Convergence Analysis of uSCG

We now generalize the error control lemma Mokhtari et al. [2020, Lem. 6] to the (L0, L1)-smooth case and modify it for the clipped algorithm Algorithm 1.

Lemma B.1 (Linear recursive inequality for E λk 2

2 for GGNC). Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 1. Then, for all k ∈{1,..., n}, it holds

E[ λk 2

2] ≤

1 −αk 2

E[ λk−1 2

2] + α2 kσ2 +

4γ2ζ2 ∗ρ2L2

0 αk +

4γ2ζ2 ∗ρ2L2

1 αk ∥∇f(xk)∥2

∗, where ζ∗:= maxx∈X

∥x∥2 ∥x∥∗.

Proof. The proof is a straightforward adaptation of the arguments laid out in Mokhtari et al. [2020, Lem. 6], which in fact do not depend on convexity nor on the choice of stepsize. Let n ∈N∗and k ∈{2,..., n}, then λk 2

2 = ∇f(xk) −dk 2

2 =

∇f(xk) −αk∇f(xk, ξk) −(1 −αk)dk−1 2

2

= αk

∇f(xk) −∇f(xk, ξk)

+ (1 −αk)

∇f(xk) −∇f(xk−1)

−(1 −αk)

dk−1 −∇f(xk−1)

2

2 = α2 k

∇f(xk) −∇f(xk, ξk)

2

2 + (1 −αk)2 ∇f(xk) −∇f(xk−1) 2

2 + (1 −αk)2 ∇f(xk−1) −dk−1 2

2 + 2αk(1 −αk)⟨∇f(xk−1) −∇f(xk−1, ξk−1), ∇f(xk) −∇f(xk−1)⟩

+ 2αk(1 −αk)⟨∇f(xk) −∇f(xk, ξk), ∇f(xk−1) −dk−1⟩

+ 2(1 −αk)2⟨∇f(xk) −∇f(xk−1), ∇f(xk−1) −dk−1⟩.

Taking the expectation conditioned on the filtration Fk generated by the iterates until k, i.e., the sigma algebra generated by {x1,..., xk}, which we denote using Ek[·], and using the unbiased property in Theorem 4.8, we get,

Ek[ λk 2

2] = α2 kEk[

∇f(xk) −∇f(xk, ξk)

2

2] + (1 −αk)2 ∇f(xk) −∇f(xk−1) 2

2 + (1 −αk)2 λk−1 2

2 + 2(1 −αk)2⟨∇f(xk) −∇f(xk−1), λk−1⟩.

<!-- Page 20 -->

For brevity define Lk:= L0 + L1∥∇f(xk)∥∗. From the above expression we can estimate,

Ek[ λk 2

2] (a)

≤α2 kσ2 + (1 −αk)2 ∇f(xk) −∇f(xk−1)

2

2 + (1 −αk)2 λk−1 2 2 + 2(1 −αk)2⟨∇f(xk) −∇f(xk−1), λk−1⟩

(b)

≤α2 kσ2 + (1 −αk)2 ∇f(xk) −∇f(xk−1)

2

2 + (1 −αk)2 λk−1 2 2

+ (1 −αk)2 αk

2 ∇f(xk) −∇f(xk−1)

2

2 + 2 αk λk−1 2

2

(c)

≤α2 kσ2 + (1 −αk)2ζ2

∗

∇f(xk) −∇f(xk−1)

2 + (1 −αk)2 λk−1 2

2

+ (1 −αk)2 αk

2 ζ2 ∗

∇f(xk) −∇f(xk−1)

2 + 2 αk λk−1 2

2

(d)

≤α2 kσ2 + (1 −αk)2ζ2

∗L2 k xk −xk−1 2 + (1 −αk)2 λk−1 2

2

+ (1 −αk)2

(αk

2)ζ∗L2 k xk −xk−1 2 + 2 αk λk−1 2

2

(e)

≤α2 kσ2 + (1 −αk)2L2 kζ2

∗γ2η2 k + (1 −αk)2 λk−1 2

2 + (1 −αk)2 (αk

2)L2 kζ2

∗γ2η2 k + 2 αk λk−1 2

2

(f) ≤α2 kσ2 + (1 + αk

2)(1 −αk)ζ2 ∗L2 kγ2η2 k + (1 + 2 αk)(1 −αk)

λk−1 2

2 (g)

≤α2 kσ2 + 2(1 + αk

2)(1 −αk)ζ2 ∗γ2ρ2(L2

0 + L2 1∥∇f(xk)∥2 ∗) + (1 + 2 αk)(1 −αk)

λk−1 2

2, using the bounded variance property from Theorem 4.8 for (a), Young’s inequality with parameter αk/2 > 0 for (b), ζ∗:= maxx∈X

∥x∥2 ∥x∥∗for (c), Theorem 4.2 for (d), the definition of xk from Algorithm 1 for (e), the fact that 1 −αk < 1 for (f), and ηk ≤ρ and Young’s inequality on L2 k for (g). To complete the proof, we note that, for all k ∈{1,..., n}, it holds

(1 + 2 αk)(1 −αk) ≤ 2 αk and (1 −αk)(1 + αk

2) ≤1 −αk 2 which, applied to the previous inequality and taking total expectations, yields

E[ λk 2

2] ≤

1 −αk 2

E[ λk−1 2

2] + α2 kσ2 + 4γ2ζ2

∗ρ2 αk

(L2

0 + L2 1∥∇f(xk)∥2 ∗).

□

Lemma B.2 (Bound on E∥λk∥2

2 with horizon-dependent α for GGNC). Suppose Theorems 4.2 and 4.8 hold, f is L-smooth, and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 1 with a stepsize γρ satisfying γρ < 1 2n3/4L1. (9)

Moreover, consider a momentum αk = α = 1√n for all k ∈{1,..., n}. Then, for all k ∈{1,..., n} the following holds

E[ λk 2

2] ≤ 2(σ2+ζ2∗L2/L2 1) √n. (10)

Proof. Let k ∈{1,..., n}. We start from the recursive inequality obtained in Theorem B.1 for E[ λk 2

2]. Since we are now assuming that f is L-smooth, this inequality is satisfied with L0 = L and L1 = 0, which gives

E[ λk 2

2] ≤

1 −α 2

E[ λk−1 2

2] + α2σ2 + 4γ2ρ2ζ2 ∗L2 α. (11)

Now, we substitute the specific choice α = 1√n of momentum to find

E[ λk 2

2] ≤ 1 − 1 2 √n E[ λk−1 2

2] + σ2 n + 4ζ2

∗L2ρ2γ2 √n. (12)

Using the particular choice of γρ, we have

E[ λk 2

2] ≤ 1 − 1 2 √n E[ λk−1 2

2] + 1 n(σ2 + ζ2

∗L2

L2

1).

<!-- Page 21 -->

Let uk = E[ λk 2

2], a = 1 2 √n, and b = 1 n(σ2+ ζ2

∗L2

L2

1). Unrolling the recurrence relation uk ≤(1−a)uk−1+b, we have uk ≤(1 −a)ku0 + b Pk−1 i=0 (1 −a)i = b Pk−1 i=0 (1 −a)i = b 1−(1−a)k

1−(1−a) = b 1−(1−a)k a.

Since 0 < a < 1, we have 0 < (1 −a)k < 1 for k ≥1. Thus, 1 −(1 −a)k < 1. Therefore, uk ≤b/a. (13)

Substituting the values for a and b, we have

E[ λk 2

2] ≤ 2(σ2+ζ2∗L2/L2 1) √n. (14)

This concludes the proof. □

Theorem 4.9. Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 1 with a constant stepsize γ ≤1/L0 and γρ ≤1/2L1. Then,

E[∥∇f(¯xn)∥∗] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ where ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 O( q

E[∥λk∥2

2] + E[∥λk∥2 2]).

Furthermore, assuming f is L-smooth4 and taking α = 1/√n, γ = 1/√nL0 and ρ = L0/2n1/4L1 such that γρ = 1/2n3/4L1 we have that

E[∥∇f(¯xn)∥∗] ≤O 1 n1/4

.

Proof. Given that ∥xk −xk+1∥≤1/L1, which we will ensure by choice of the stepsize γηk and radius ρ, we have from Theorem 4.2 that

0 ≤f(xk) −f(xk+1) + ⟨∇f(xk), xk+1 −xk⟩+ L0+L1∥∇f(xk)∥∗ 2 ∥xk+1 −xk∥2

= f(xk) −f(xk+1) + γηk⟨∇f(xk), lmo(dk)⟩+ L0

2 γ2η2 k∥lmo(dk)∥2 + L1

2 γ2η2 k∥∇f(xk)∥∗∥lmo(dk)∥2

= f(xk) −f(xk+1) + γηk⟨∇f(xk), lmo(dk)⟩+ L0

2 γ2η2 k + L1

2 γ2η2 k∥∇f(xk)∥∗ where we recall that ηk = min{ρ, ∥dk∥∗}.

To treat the inner product we introduce the error λk:= dk −∇f(xk) and proceed as follows

⟨∇f(xk), lmo(dk)⟩= ⟨∇f(xk) −dk, lmo(dk)⟩+ ⟨dk, lmo(dk)⟩

≤⟨∇f(xk) −dk, lmo(dk)⟩−∥dk∥∗ = ⟨∇f(xk) −dk, lmo(dk)⟩−1

2∥dk∥∗−1 2∥dk∥∗

(Triangle ineq.) ≤⟨∇f(xk) −dk, lmo(dk)⟩−1

2∥dk∥∗−1 2∥∇f(xk)∥∗+ 1 2∥λk∥∗

(Cauchy-Schwarz) ≤∥λk∥∗−1

2∥dk∥∗−1 2∥∇f(xk)∥∗+ 1 2∥λk∥∗ ≤3

2ζ∥λk∥2 −1 2∥dk∥∗−1 2∥∇f(xk)∥∗ where ζ:= maxx∈X

∥x∥∗ ∥x∥2 is the norm equivalence constant.

Combining the two inequalities we have

0 ≤f(xk) −f(xk+1) + γηk 3 2ζ∥λk∥2 −γηk 1 2∥dk∥∗−γηk 1 2∥∇f(xk)∥∗+ L0 2 γ2η2 k + L1

2 γ2η2 k∥∇f(xk)∥∗ = f(xk) −f(xk+1) + γηk 3

2ζ∥λk∥2 −γηk 1 2(∥dk∥∗−L0γηk) −γηk 1 2(1 −L1γηk)∥∇f(xk)∥∗

Case I Clipping Active (ρ < ∥dk∥∗).

In this case we have that ηk = ρ, so

0 ≤f(xk) −f(xk+1) + γkρ 3 2ζ∥λk∥2 −γkη2 k

1 2(1 −L0γk) −γkρ 1 2(1 −L1γkρ)∥∇f(xk)∥∗ ≤f(xk) −f(xk+1) + γkρ 3

2ζ∥λk∥2 −γkρ 1 2(1 −L1γkρ)∥∇f(xk)∥∗ where we have used γk ≤ 1 L0.

4Only local Lipschitz is needed in the sense that the condition only needs to hold for (x, y) satisfying ∥x −y∥≤1/L1. It is also possible to replace L with Ln:= maxk≤n L0 + L1∥f(xk)∥∗, e.g., as is done in [Koloskova et al., 2023, Thm. 2.3].

<!-- Page 22 -->

Case II No Clipping (ρ ≥∥dk∥∗).

Here we have that ηk = ∥dk∥∗, so

0 ≤f(xk) −f(xk+1) + γkρ 3 2ζ∥λk∥2 −γkη2 k

1 2(1 −L0γk) −γk 1 2(1 −L1γkρ)∥dk∥∗∥∇f(xk)∥∗

Focusing on the last term, we have

∥dk∥∗∥∇f(xk)∥∗= ∥dk −∇f(xk) + ∇f(xk)∥∗∥∇f(xk)∥∗

(Triangle ineq.) ≥(∥∇f(xk)∥∗−∥λk∥∗)∥∇f(xk)∥∗

= ∥∇f(xk)∥2

∗−∥λk∥∗∥∇f(xk)∥∗.

For the last term, using the triangle inequality, we have

∥λk∥∗∥∇f(xk)∥∗≤∥λk∥∗(∥∇f(xk) −dk∥∗+ ∥dk∥∗)

= ∥λk∥2

∗+ ∥λk∥∗∥dk∥∗ ≤∥λk∥2

∗+ ∥λk∥∗ρ

≤ζ∥λk∥2

2 + ζ∥λk∥2ρ.

By combining, we have

0 ≤f(xk) −f(xk+1) −γkη2 k

1 2(1 −L0γk) −γk 1 2(1 −L1γkρ)∥∇f(xk)∥2 ∗ + γkρ 3

2ζ∥λk∥2 + γk 1 2ζ(1 −L1γkρ)(∥λk∥2 2 + ∥λk∥2ρ)

= f(xk) −f(xk+1) −γkη2 k

1 2(1 −L0γk) −γk 1 2(1 −L1γkρ)∥∇f(xk)∥2 ∗ + γkρζ(2 −1

2L1γkρ)∥λk∥2 + γk 1 2ζ(1 −L1γkρ)∥λk∥2 2 ≤f(xk) −f(xk+1) −γk 1

2(1 −L1γkρ)∥∇f(xk)∥2 ∗ + γkρζ(2 −1

2L1γkρ)∥λk∥2 + γk 1 2ζ(1 −L1γkρ)∥λk∥2 2 where the last inequality uses γk ≤ 1 L0.

Combining both cases Introducing the set of iterates where clipping is active, A:= {k ∈[n] | ρ < ∥dk∥∗}, we can take the expectation of both sides and sum the two cases to find

1 2γ(1 −L1γρ)(ρ P k∈A E[∥∇f(xk)∥∗] + P k<A E[∥∇f(xk)∥2

∗])

≤f(x1) −f ⋆+ P k∈A γρζ 3

2E[∥λk∥2] + P k<A γρζ(2 −1

2L1γρ)E[∥λk∥2] + γ 1 2ζ(1 −L1γρ)E[∥λk∥2 2]

≤f(x1) −f ⋆+ P k∈A γρζ 3

2 q

E[∥λk∥2

2] + P k<A γρζ(2 −1

2L1γρ) q

E[∥λk∥2

2] + γ 1 2ζ(1 −L1γρ)E[∥λk∥2 2]

≤f(x1) −f ⋆+ Pn k=1 γρζ(2 −1

2L1γρ) q

E[∥λk∥2

2] + γ 1 2ζ(1 −L1γρ)E[∥λk∥2 2]

where the second to last inequality is due to Jensen’s inequality and the last inequality uses that γ ≤1/ρL1. Using the stronger requirement that γ ≤1/2ρL1 it follows that

1 4γ ρ P k∈A E[∥∇f(xk)∥∗] + P k<A E[∥∇f(xk)∥2

∗]

≤∆+ γϵn with ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 ρζ 7

4 q

E[∥λk∥2

2] + 1 4ζE[∥λk∥2 2]. By nonnegativity of the summands, it follows that

1 n

P k∈A E[∥∇f(xk)∥∗] ≤4∆ γρn + 4ϵn ρ, (15)

corresponding to the indices from Case I. Using Jensen’s inequality, we similarly have

1 n

P k<A E[∥∇f(xk)∥∗]2 ≤1 n

P k<A E[∥∇f(xk)∥2

∗] ≤4∆ γn + 4ϵn =: A (16)

corresponding to the indices from Case II. We will now use that 2az −a2 ≤z2 for any a, z > 0. Pick z = E[∥∇f(xk)∥∗], then we have that

1 n

P k<A z ≤1 n

P k<A z2 2a + a 2

(16) ≤A

2a + 1 n

P k<A a 2 ≤A 2a + a 2

<!-- Page 23 -->

Choosing a =

√

A and using the triangle inequality we have

1 n

P k<A E[∥∇f(xk)∥∗] ≤

√

A ≤2

√

∆ √n + 2 √ϵn. (17)

Summing the two cases, (15) and (17), we have

1 n

Pn k=1 E[∥∇f(xk)∥∗] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ.

What remains is to bound the error ϵn that is due to the stochastic estimator. With the choice γ ≤1/√nL0, γρ ≤1/2n3/4L1 and αk = 1/√n, invoke Theorem B.2 from which we have

E[ λk 2

2] ≤ 2(σ2+ζ2∗L2/L2 1) √n =: B.

It follows that ϵn ≤ρζ 7

4 √

B + 1

4ζB and in turn the inequality B.2.1 simplifies

1 n

Pn k=1 E[∥∇f(xk)∥∗] ≤O(

√

∆ √γn + ∆ γρn + q ρζ

√

B + ζB + ρζ

√

B+ζB ρ)

≤O(

√

∆ √γn + ∆ γρn + p ρζB1/4 + p ζB + ζ

√

B + ζB ρ)

where we have used the triangle inequality in the second inequality. Letting b:= 2(σ2 + ζ2

∗L2/L2

1) we have with the choice γ = 1/√nL0 and ρ = L0/2n1/4L1 that

1 n

Pn k=1 E[∥∇f(xk)∥∗] ≤O

1 n1/4 p

∆L0 + ∆L1 +

√ζL0b1/4

√L1 + p ζb + ζ

√ b + ζbL1

L0

≤O

1 n1/4 p

∆L0 + ∆L1 +

√ζL0(σ2+ζ2∗L2/L2

1)1/4 √L1

+ (ζ + p ζ)

q

(σ2 + ζ2

∗L2/L2

1) + ζ(σ2+ζ2∗L2/L2

1)L1 L0

≤O

1 n1/4 p

∆L0 + ∆L1 +

√ζL0(√σ+√ ζ∗L/L1) √L1

+ (ζ + p ζ)(σ + ζ∗L/L1) + ζ(σ2+ζ2∗L2/L2

1)L1 L0

Noting that E[∥∇f(¯xn)∥∗] = 1 n

Pn k=1 E[∥∇f(xk)∥∗] completes the proof. □

B.2.2 Convergence analysis of S3CG

Following the same outline as the convergence analysis for Algorithm 1 given in the previous subsection, we start with an error control lemma in the vein of [Mokhtari et al., 2020, Lem. 6] that is compatible with our adaptive stepsize.

Lemma B.3 (Linear recursive inequality for E λk 2

2 for S3CG). Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 2 with stepsize γηk ≤ρ. Then, for all k ∈{1,..., n},

E[ λk 2

2] ≤

1 −α 2

E[ λk−1 2

2] + α2σ2 + 8ζ2 ∗L2βγ2ρ2 α where ζ∗:= maxx∈X

∥x∥2 ∥x∥∗.

Proof. The proof is a straightforward adaptation of the arguments laid out in Mokhtari et al. [2020, Lem. 6], which in fact do not depend on convexity of the function f nor on the choice of stepsize

<!-- Page 24 -->

γηk, as long as it is in [0, 1]. Let n ∈N∗and k ∈{1,..., n}, then λk 2

2 = ∇f(xk) −dk 2

2 =

∇f(xk) −α∇f(xk, ξk) −(1 −α)dk−1 2

2

= α

∇f(xk) −∇f(xk, ξk)

+ (1 −α)

∇f(xk) −∇f(xk−1)

−(1 −α)

dk−1 −∇f(xk−1)

2

2 = α2 ∇f(xk) −∇f(xk, ξk)

2

2 + (1 −α)2 ∇f(xk) −∇f(xk−1) 2

2 + (1 −α)2 ∇f(xk−1) −dk−1 2

2 + 2α(1 −α)⟨∇f(xk−1) −∇f(xk−1, ξk−1), ∇f(xk) −∇f(xk−1)⟩

+ 2α(1 −α)⟨∇f(xk) −∇f(xk, ξk), ∇f(xk−1) −dk−1⟩

+ 2(1 −α)2⟨∇f(xk) −∇f(xk−1), ∇f(xk−1) −dk−1⟩.

Taking the expectation conditioned on the filtration Fk generated by the iterates until k, i.e., the sigma algebra generated by {x1,..., xk}, which we denote using Ek[·], and using the unbiased property in Theorem 4.8, we get,

Ek[ λk 2

2] = α2Ek[ ∇f(xk) −∇f(xk, ξk)

2

2] + (1 −α)2 ∇f(xk) −∇f(xk−1) 2

2 + (1 −α)2 λk−1 2

2 + 2(1 −α)2⟨∇f(xk) −∇f(xk−1), λk−1⟩.

From the above expression we can estimate,

Ek[ λk 2

2] (a)

≤α2σ2 + (1 −α)2 ∇f(xk) −∇f(xk−1)

2

2 + (1 −α)2 λk−1 2 2 + 2(1 −α)2⟨∇f(xk) −∇f(xk−1), λk−1⟩

(b)

≤α2σ2 + (1 −α)2 ∇f(xk) −∇f(xk−1)

2

2 + (1 −α)2 λk−1 2 2

+ (1 −α)2 α 2 ∇f(xk) −∇f(xk−1)

2

2 + 2 α λk−1 2

2

(c)

≤α2σ2 + (1 −α)2ζ2

∗

∇f(xk) −∇f(xk−1)

2 + (1 −α)2 λk−1 2

2

+ (1 −α)2 α 2 ζ2 ∗

∇f(xk) −∇f(xk−1)

2 + 2 α λk−1 2

2

(d)

≤α2σ2 + (1 −α)2ζ2

∗L2 xk −xk−1 2 + (1 −α)2 λk−1 2

2

+ (1 −α)2

(α

2)ζ∗L2 xk −xk−1 2 + 2 α λk−1 2

2

(e)

≤α2σ2 + 4(1 −α)2ζ2

∗L2β2γ2η2 k + (1 −α)2 λk−1 2

2 + (1 −α)2 2αζ2 ∗L2β2γ2η2 k + 2 α λk−1 2

2

(f) ≤α2σ2 + 4(1 + α

2)(1 −α)ζ2 ∗L2β2γ2η2 k + (1 + 2 α)(1 −α)

λk−1 2

2 (g)

≤α2σ2 + 4(1 + α

2)(1 −α)ζ2 ∗L2β2γ2ρ2 + (1 + 2 α)(1 −α)

λk−1 2

2, using the bounded variance property from Theorem 4.8 for (a), Young’s inequality with parameter α/2 > 0 for (b), ζ∗:= maxx∈X

∥x∥2 ∥x∥∗for (c), Theorem 4.2 for (d), the definition of xk from Algorithm 2 for (e), the fact that 1 −α < 1 for (f), and ηk ≤ρ and for (g). To complete the proof, we note that

(1 + 2 α)(1 −α) ≤(1 −α

2) and (1 −α)(1 + α

2) ≤2 α which, applied to the previous inequality and taking total expectations, yields

E[ λk 2

2] ≤

1 −α 2

E[ λk−1 2

2] + α2σ2 + 8ζ2 ∗L2β2γ2ρ2 α.

□

Lemma B.4 (Bound on the gradient error with horizon-dependent α for S3CG). Suppose Theorem 4.8 holds, f is L-smooth with respect to ∥· ∥∗, and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 2 with a stepsize γρ satisfying γρ < 1 Ln3/4. (18)

<!-- Page 25 -->

Moreover, consider a constant momentum αk = α = 1√n for all k ∈{1,..., n}. Then, for all k ∈{1,..., n} the following holds

E[ λk 2

2] ≤2σ2+16ζ2 ∗β2 √n. (19)

Proof. Let n ∈N∗and k ∈{1,..., n}. We start from the recursive inequality obtained in Theorem B.3 for E[ λk 2

2] with L the Lipschitz constant of the gradient over the compact set D to get

E[ λk 2

2] ≤

1 −α 2

E[ λk−1 2

2] + α2σ2 + 8ζ2 ∗L2β2γ2ρ2 α. (20)

Now, we substitute the specific choice α = 1√n:

E[ λk 2

2] ≤

1 − 1 2 √n

!

E[ λk−1 2

2] + σ2 n + 8ζ2

∗L2β2γ2ρ2 √n. (21)

Using the particular choice of γρ specified in the statement of the lemma, we have

E[ λk 2

2] ≤

1 − 1 2 √n

!

E[ λk−1 2

2] + 1 n(σ2 + 8ζ2

∗β2)

Let uk = E[ λk 2

2], a = 1 2 √n, and b = 1 n(σ2 + 8ζ2

∗β2). Unrolling the recurrence relation uk ≤ (1 −a)uk−1 + b, we have uk ≤(1 −a)ku0 + b Pk−1 i=0 (1 −a)i = b Pk−1 i=0 (1 −a)i = b 1−(1−a)k

1−(1−a) = b 1−(1−a)k a

Since 0 < a < 1, we have 0 < (1 −a)k < 1 for k ≥1. Thus, 1 −(1 −a)k < 1. Therefore, uk ≤b/a. (22)

Substituting the values for a and b, we have

E[ λk 2

2] ≤2σ2+16ζ2 ∗β2 √n. (23)

This concludes the proof. □

Theorem 4.11. Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 2 (Variant 1) with a constant stepsize γ ≤1/L √n and ρ ≤1/n1/4. Then, for all u ∈βD,

E[⟨∇f(¯xn), ¯xn −u⟩] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ where ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 O( q

E∥λk∥2

2 + E∥λk∥2 2).

Furthermore, taking α = 1/√n, γ = 1/(L √n) and ρ = 1/n1/4 such that γρ = 1/(Ln3/4) we have that

E[⟨∇f(¯xn), ¯xn −u⟩] ≤O 1 n1/4

.

Proof. Note that, since f is continuously differentiable and D is compact, f must be Lipschitz-smooth on the scaled ball βD with respect to the norm ∥· ∥; call the Lipschitz constant L > 0. We can therefore start with the descent lemma for f at the points xk+1 and xk to find

0 ≤f(xk) −f(xk+1) + ⟨∇f(xk), xk+1 −xk⟩+ L 2 ∥xk+1 −xk∥2

≤f(xk) −f(xk+1) −γηk⟨∇f(xk), vk⟩+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) −γηk

⟨dk, vk⟩+ ⟨∇f(xk) −dk, vk⟩

+ L

2 γ2η2 k∥vk∥2.

Now we can proceed case-by-case depending on whether clipping is active or not.

<!-- Page 26 -->

Case I Clipping Active (γηk = γρ; ⟨dk,vk⟩

∥vk∥2 ≥ρ).

For all u ∈βD it holds,

0 ≤f(xk) −f(xk+1) −γηk

⟨dk, vk⟩+ ⟨∇f(xk) −dk, vk⟩

+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) −γηk

1

2⟨dk, vk⟩+ 1 2⟨∇f(xk), xk −u⟩+ 1 2⟨dk −∇f(xk), xk −u⟩+ ⟨∇f(xk) −dk, vk⟩!

+ L

2 γ2η2 k∥vk∥2

(a)

≤f(xk) −f(xk+1) −γηk

1

2⟨dk, vk⟩+ 1 2⟨∇f(xk), xk −u⟩−1 2∥λk∥2∥xk −u∥2 −∥λk∥2∥vk∥2

!

+ L

2 γ2η2 k∥vk∥2

(b)

≤f(xk) −f(xk+1) + γηk

L

2 γηk∥vk∥2 −1 2⟨dk, vk⟩!

−γηk

1 2⟨∇f(xk), xk −u⟩+ γηk 3 2∥λk∥2D2

(c)

≤f(xk) −f(xk+1) + γρ

L

2 γρ∥vk∥2 −1 2ρ∥vk∥2!

−γρ1

2⟨∇f(xk), xk −u⟩+ γρ3 2∥λk∥2D2

(d)

≤f(xk) −f(xk+1) + γρ3

2∥λk∥2D2 −γρ1 2⟨∇f(xk), xk −u⟩ where D2 = max x,y∈βD ∥x −y∥2 is the diameter of the set βD in the Euclidean norm. The inequality (a)

follows by Cauchy-Schwarz, (b) follows by using the diameter of βD, (c) follows since clipping is active, and (d) follows since Lγ ≤1. Finally, rearranging gives γρ⟨∇f(xk), xk −u⟩≤2 f(xk) −f(xk+1)

+ 3D2γρ∥λk∥2. (24)

Case II No Clipping (γηk = γ ⟨dk,vk⟩

∥vk∥2; ⟨dk,vk⟩

∥vk∥2 ≤ρ).

In this case, our stepsize acts like the short step. Starting with the previous inequality from the descent lemma we have, for all u ∈βD,

0 ≤f(xk) −f(xk+1) −γ⟨dk, vk⟩ ∥vk∥2 ⟨dk, vk⟩−γηk⟨∇f(xk) −dk, vk⟩+ L

2 γ2 ⟨dk, vk⟩

∥vk∥2

!2

∥vk∥2

≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

∥vk∥2 −γηk⟨∇f(xk) −dk, vk⟩+ Lγ2 ⟨dk, vk⟩2

2∥vk∥2

≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

2∥vk∥2 −γηk⟨∇f(xk) −dk, vk⟩

(25)

where in the last inequality we have used that γ ≤1

L. Rearranging, we can estimate

0 ≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

2∥vk∥2 −γηk⟨∇f(xk) −dk, vk⟩

(a)

≤f(xk) −f(xk+1) − 1 2∥vk∥2 γ

2⟨∇f(xk), xk −u⟩2 −2γ⟨∇f(xk) −dk, xk −u⟩2 −γηk⟨∇f(xk) −dk, vk⟩

= f(xk) −f(xk+1) − γ 4∥vk∥2 ⟨∇f(xk), xk −u⟩2 + γ ∥vk∥2 ⟨∇f(xk) −dk, xk −u⟩2 −γηk⟨∇f(xk) −dk, vk⟩

(b)

≤f(xk) −f(xk+1) − γ 4∥vk∥2 ⟨∇f(xk), xk −u⟩2 + D2 2γ ∥vk∥2 ∥λk∥2

2 + D2γρ∥λk∥2

(c)

≤16β2 f(xk) −f(xk+1)

−γ⟨∇f(xk), xk −u⟩2 + 4D2

2γ∥λk∥2 2 + 16D2β2γρ∥λk∥2 (26) where (a) is due to Young’s inequality, (b) is due to Cauchy-Schwarz and the definition of D2 as the diameter of βD in the Euclidean norm, and (c) follows by multiplying everything by 4∥vk∥2 and estimating. We can rearrange this to finally arrive at γ⟨∇f(xk), xk −u⟩2 ≤16β2 f(xk) −f(xk+1)

+ 4D2

2γ∥λk∥2 2 + 16D2β2γρ∥λk∥2.

Combining Both Cases Let M = max{16β2, 2} and M′ = max{16D2β2, 3D2} and let A ⊂ {1, 2,..., n} denote the indices where clipping is active. Let n ∈N∗and denote ϵn:= 1 n n X k=1

M′ρE[∥λk∥2] + 1 n n X k=1

4D2 2E[∥λk∥2 2].

<!-- Page 27 -->

Then, taking expectations, adding from k = 1 to n, and dividing by n gives

1 n

X k∈A γρE[⟨∇f(xk), xk −u⟩] + 1 n

X k<A γE[⟨∇f(xk), xk −u⟩2] ≤M n f(x1) −f ⋆

+ γϵn. (27)

We can lower bound the left hand side by the sum over A and divide by γρ to get

1 n

X k∈A

E[⟨∇f(xk), xk −u⟩] ≤M∆ γρn + ϵn ρ. (28)

Similarly, lower bounding the left hand side by the sum over the complement of A and dividing by γ, we get by Jensen’s inequality

1 n

X k<A

E[⟨∇f(xk), xk −u⟩]2 ≤1 n

X k<A

E[⟨∇f(xk), xk −u⟩2] ≤M∆ γn + ϵn. (29)

We use the fact that 2az −a2 ≤z2 for any a, z > 0. Picking z = E[⟨∇f(xk), xk −u⟩], it follows that

1 n

X k<A z ≤1 n

X k<A z2

2a + a 2 ≤A 2a + 1 n

X k<A a 2 ≤A 2a + a 2 (30)

where A:= M∆ γn + ϵn. Choosing a =

√

A and replacing z by E[⟨∇f(xk), xk −u⟩] we get

1 n

X k<A

E[⟨∇f(xk), xk −u⟩] ≤

√

A =

√

M∆ √γn + √ϵn. (31)

Adding both of these we get

1 n n X k=1

E[⟨∇f(xk), xk −u⟩] ≤

√

M∆ √γn + √ϵn + M∆ γρn + ϵn ρ. (32)

Let Λ2 n:= 2σ2+16ζ2

∗β2 √n. By theorem B.4, Λ2 n ≥E[∥λk∥2

2] for all k ≤n.

Next, we can estimate ϵn ≤M′ρΛn + 4D2

2Λ2 n √ϵn ≤ p

M′ρΛn + 2D2Λn ϵn ρ ≤M′Λn + 4 ρD2

2Λ2 n.

Substituting in the definition of Λn, γ, and ρ while also noting the definition of ¯xn, we get

E[⟨∇f(¯xn), ¯xn −u⟩] ≤

√

M∆ √γn + √ϵn + M∆ γρn + ϵn ρ

≤

√

M∆ √γn + p

M′ρΛn + 2D2Λn + M∆ γρn + M′Λn + 4 ρD2

2Λ2 n

≤

√

LM∆ n1/4 + q

M′

2σ2 + 16ζ2∗β2 n1/4 + 2D2 p

2σ2 + 16ζ2∗β2 n1/4

+ LM∆ n1/4 + M′ p

2σ2 + 16ζ2∗β2 n1/4 +

4D2 2

2σ2 + 16ζ2 ∗β2 n1/4 which gives a big O rate

E[⟨∇f(¯xn, ¯xn −u⟩] ≤O

1 n1/4

!

.

□

<!-- Page 28 -->

Theorem B.5. Suppose Theorems 4.2 and 4.8 hold and let n ∈N∗. Consider the iterates {xk}1≤k≤n generated by Algorithm 2 (Variant 2) with a constant stepsize γ ≤1/L √n and ρ ≤1/n1/4. Then, for all u ∈D,

E[⟨∇f(¯xn), ¯xn −u⟩] ≤4

√

∆ √γn + 8∆ γρn + 4 √ϵn + 8ϵn ρ where ∆:= f(x1) −f ⋆and ϵn:= 1 n

Pn k=1 O( q

E∥λk∥2

2 + E∥λk∥2 2).

Furthermore, taking α = 1/√n, γ = 1/(L √n) and ρ = 1/n1/4 such that γρ = 1/(Ln3/4) we have that

E[⟨∇f(¯xn), ¯xn −u⟩] ≤O 1 n1/4

.

Proof. Note that, since f is continuously differentiable and D is compact, f must be Lipschitz-smooth on the scaled ball βD with respect to the norm ∥· ∥; call the Lipschitz constant L. We can therefore start with the descent lemma for f at the points xk+1 and xk to find

0 ≤f(xk) −f(xk+1) + ⟨∇f(xk), xk+1 −xk⟩+ L 2 ∥xk+1 −xk∥2

≤f(xk) −f(xk+1) −γηk⟨∇f(xk), vk⟩+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) −γηk

⟨dk, vk⟩+ ⟨∇f(xk) −dk, vk⟩

+ L

2 γ2η2 k∥vk∥2.

(33)

Now we can proceed case-by-case depending on whether clipping is active or not.

Case I Clipping Active (γηk = γρ; ⟨dk,vk⟩

4β2 ≥ρ).

0 ≤f(xk) −f(xk+1) −γηk

⟨dk, vk⟩+ ⟨∇f(xk) −dk, vk⟩

+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) −γηk

1

2⟨dk, vk⟩+ 1 2⟨∇f(xk), xk −u⟩+ 1 2⟨dk −∇f(xk), xk −u⟩+ ⟨∇f(xk) −dk, vk⟩!

+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) −γηk

1

2⟨dk, vk⟩+ 1 2⟨∇f(xk), xk −u⟩−1 2∥λk∥2∥xk −u∥2 −∥λk∥2∥vk∥2

!

+ L

2 γ2η2 k∥vk∥2

≤f(xk) −f(xk+1) + γηk

L

2 γηk∥vk∥2 −1 2⟨dk, vk⟩!

−γηk

1 2⟨∇f(xk), xk −u⟩+ γηk 3 2∥λk∥2D2

≤f(xk) −f(xk+1) + γρ

2Lγρβ2 −2ρβ2 −γρ1

2⟨∇f(xk), xk −u⟩+ γρ3 2∥λk∥2D2

≤f(xk) −f(xk+1) + γρ3

2∥λk∥2D2 −γρ1 2⟨∇f(xk), xk −u⟩ (34) in the second inequality we have used the fact that ∥vk∥2 ≤2∥xk∥2 + 2∥β lmo(dk)∥2 ≤4β2 and the fact that ∥vk∥2 ≤D2. Finally, rearranging gives γρ⟨∇f(xk), xk −u⟩≤2 f(xk) −f(xk+1)

+ 3D2γρ∥λk∥2. (35)

Case II No Clipping (γηk = γ ⟨dk,vk⟩

4β2; ⟨dk,vk⟩ 4β2 ≤ρ).

0 ≤f(xk) −f(xk+1) −γ⟨dk, vk⟩ 4β2 ⟨dk, vk⟩−γηk⟨∇f(xk) −dk, vk⟩+ L

2 γ2 ⟨dk, vk⟩

4β2

!2

∥vk∥2

≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

4β2 −γηk⟨∇f(xk) −dk, vk⟩+ Lγ2 ⟨dk, vk⟩2

8β2

≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

8β2 −γηk⟨∇f(xk) −dk, vk⟩

(36)

<!-- Page 29 -->

where in the last inequality we have used that γ ≤1

L. Rearranging,

0 ≤f(xk) −f(xk+1) −γ⟨dk, vk⟩2

8β2 −γηk⟨∇f(xk) −dk, vk⟩

≤f(xk) −f(xk+1) −1

8β2 γ

2⟨∇f(xk), xk −u⟩2 −2γ⟨∇f(xk) −dk, xk −u⟩2 −γηk⟨∇f(xk) −dk, vk⟩

≤f(xk) −f(xk+1) −1

8β2 γ

2⟨∇f(xk), xk −u⟩2 + γ

4β2 ⟨∇f(xk) −dk, xk −u⟩2 −γηk⟨∇f(xk) −dk, vk⟩

≤f(xk) −f(xk+1) − γ 16β2 ⟨∇f(xk), xk −u⟩2 + γ 4β2 ⟨∇f(xk) −dk, xk −u⟩2 −γηk⟨∇f(xk) −dk, vk⟩

≤f(xk) −f(xk+1) − γ 16β2 ⟨∇f(xk), xk −u⟩2 + D2 2γ 4β2 ∥λk∥2 2 + D2γρ∥λk∥2

≤16β2 f(xk) −f(xk+1)

−γ⟨∇f(xk), xk −u⟩2 + 4D2

2γ∥λk∥2 2 + 16D2β2γρ∥λk∥2. (37)

The rest of the proof is exactly the same as it was for Variant 1, so we omit it. □

C Experiments

Our implementations follow Unconstrained ClippedScion and ClippedScion Algorithm 3 and Algorithm 4 (Variant 2), respectively. For simplicity, we absorb the latter’s factor of 4 into the clipping threshold ρ, so both algorithms directly clip PD l=1 ⟨dk l, vk l ⟩at ρ.

CIFAR10 experiments are run on a single A100 NVIDIA GPU, NanoGPT runs are run on 4 × H100 NVIDIA GPUs, and ViT experiments use 16 × GH200 NVIDIA GPUs. Hyperparameters are provided in Tables 2 to 4.

-8 -7 -6 -5 -4 -3 -2 -1 log2 Learning Rate x rho

No Clip 800 rho

90.6 91.4 92.2 92.4 91.8 88.6 82.9 44.0

90.2 91.3 91.9 92.8 93.0 94.1 94.2 85.2

90.6 91.2 92.2 93.5 93.7 94.2 94.2 93.8

90.5 91.3 92.6 93.3 93.7 93.9 94.0 93.8

90.4 91.4 92.6 93.3 93.6 93.9 94.0 93.9

90.5 91.4 92.5 93.2 93.6 93.7 93.7 94.0

90.4 91.2 92.7 93.0 93.4 93.8 93.8 93.9

90.5 91.4 92.5 93.0 93.4 93.7 93.9 93.7

90.2 91.5 92.3 92.9 93.4 93.6 93.9 93.9

Unconstrained ClippedScion Test Accuracy Heatmap

50

60

70

80

90

-7 -6 -5 -4 -3 -2 -1 0 log2 Learning Rate x rho

No Clip 800 rho

91.3 92.2 93.3 93.7 94.1 94.5 94.5 10.0

91.4 92.3 93.2 93.8 94.1 94.4 94.5 10.0

91.3 92.3 93.2 93.8 94.1 94.3 94.3 10.0

91.3 92.2 93.1 93.7 94.0 94.0 94.1 76.6

91.4 92.2 93.1 93.6 93.9 94.0 94.1 93.7

91.3 92.3 93.1 93.5 93.9 93.9 94.0 93.8

91.4 92.3 93.0 93.5 93.8 93.8 94.1 93.9

91.1 92.2 93.0 93.4 93.8 93.9 94.0 94.0

91.1 92.1 92.8 93.3 93.7 93.9 93.9 94.0

Unconstrained ClippedScion Test Accuracy Heatmap

10

20

30

40

50

60

70

80

90

**Figure 3.** The optimal hyperparameters for Unconstrained ClippedScion on CIFAR10 for 80 epochs, (left) no stepsize decay (right) with stepsize decay. (indicated in red). The first row indicated with "No Clip" corresponds to Unconstrained Scion.

-10 -9 -8 -7 -6 -5 -4 -3 log2 Learning Rate x rho

No Clip

12800.0

25600.0

38400.0

51200.0

64000.0

76800.0

89600.0

102400.0 rho

90.0 91.1 91.2 90.1 87.6 80.1 68.2 49.9

89.2 90.9 91.4 90.4 88.4 81.3 69.3 51.6

84.5 90.6 91.1 90.3 85.9 81.6 70.9 58.7

59.7 89.6 90.9 89.6 87.6 85.5 80.0 72.5

53.2 85.0 90.7 90.6 87.7 84.9 80.4 73.6

46.2 65.7 90.2 91.0 88.8 86.5 83.9 77.1

42.4 59.9 89.4 88.8 88.4 84.9 84.9 78.0

37.0 56.1 88.6 89.6 87.2 89.4 85.3 79.4

33.0 53.7 85.3 89.2 89.6 88.1 85.2 81.8

ClippedScion Test Accuracy Heatmap

40

50

60

70

80

90

**Figure 4.** The optimal hyperparameters for ClippedScion on CIFAR10 for 80 epochs, no stepsize decay (indicated in red). The first row indicated with "No Clip" corresponds to Scion.

![Figure extracted from page 29](2025-NEURIPS-generalized-gradient-norm-clipping-non-euclidean-l-0-l-1-smoothness/page-029-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 29](2025-NEURIPS-generalized-gradient-norm-clipping-non-euclidean-l-0-l-1-smoothness/page-029-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 29](2025-NEURIPS-generalized-gradient-norm-clipping-non-euclidean-l-0-l-1-smoothness/page-029-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 30 -->

0 10 20 40 50 60 70 80 Epoch

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8

0.9

Test Accuracy

Adam Unconstrained Scion Unconstrained ClippedScion

0 250 500 750 Iteration k

0

500

Gradient norm dk

Unconstrained ClippedScion Clipping threshold

**Figure 5.** For CIFAR10 experiments with stepsize decay; Unconstrained Scion and Unconstrained ClippedScion achieve similar performance as expected.

0 10 20 40 50 60 70 80 Epoch

0.3

0.4

0.5

0.6

0.7

0.8

0.9

Test Accuracy

Scion ClippedScion

0 250 500 750 Iteration k

2x104

4x104

6x104

8x104

1x105 vk, dk

ClippedScion Clipping threshold

**Figure 6.** For CIFAR10 experiments for constrained variant of the algorithms without stepsize decay; clipping is less effective due to the surprising increase of ⟨vk, dk⟩. We observe that even the (deterministic) Wolfe gap is increasing, which is otherwise expected to go to zero.

0 25 50 75 100 125 150 175 200 Epoch

0.70

0.72

0.74

0.76

0.78

0.80

Test Accuracy

Unconstrained Scion Unconstrained ClippedScion

11% speedup

0 25 50 75 100 125 150 175 200 Epoch

Gradient norm dk

Unconstrained ClippedScion Clipping threshold

**Figure 7.** Clipping improves over Scion by a 11% speedup on DeiT-base. Cosine learning rate schedule is used.

## 0 Iteration k

3.3

3.4

3.5

3.6

3.7

3.8

3.9

Validation Loss

Adam Unconstrained Scion Unconstrained ClippedScion

10% speedup

Iteration k

0

200

400

600

800

Gradient norm dk

Unconstrained ClippedScion Clipping threshold

**Figure 8.** For fixed stepsize comparison clipping improves over Scion by more than a 10% speedup on NanoGPT (124M).

<!-- Page 31 -->

## 0 Iteration k

3.2

3.3

3.4

3.5

3.6

3.7

3.8

Validation Loss

Unconstrained Scion Unconstrained ClippedScion

**Figure 9.** NanoGPT (124M) with stepsize decay. Unconstrained Scion and Unconstrained Clipped- Scion similar performance for the final iterate as expected under stepsize decay.

## 0 Iteration k

3.2

3.3

3.4

3.5

3.6

3.7

3.8

Validation Loss

Scion ClippedScion

Iteration k

400

500

600

700

800

900 vk, dk

ClippedScion Clipping threshold

**Figure 10.** NanoGPT (124M) for constrained variants of the algorithm with stepsize decay. An interesting observation, which requires further investigation, is that ⟨vk, dk⟩surprisingly increases during the linear stepsize decay.

0 400 500 600 700 800

3.3550

3.3575

3.3600

3.3625

3.3650

3.3675

3.3700

Validation Loss

**Figure 11.** NanoGPT (124M) for Unconstrained ClippedScion with ρ sweeping. The sweep range is set according to the gradient norm from Figure 8 (right). Both steepest descent (ρ = ∞) and conditional gradient (ρ →0) perform worse than clipping.

<!-- Page 32 -->

**Table 2.** Hyperparameters for the CIFAR10 experiments building on airbench [Jordan, 2024].

Hyperparameter Adam (Clipped)Scion Unconst. Scion Unconst. ClippedScion Block size (b1, b2, b3) width factor × (64, 256, 256) Activation function GELU Dataset CIFAR10 (50000 training examples) batch size Epochs 80 Stepsize schedule Linear decay γk = γ · (1 −k/n) Averaging parameter α 0.9 0.5 Stepsize γ 1e-3 2−8 2−5 2−2

Initial stepsize γ for decay 2e-3 - 2−1 2−1 Clipping parameter ρ - 12800 - Radius r1 / rℓ/ rD - 1 / 5 / 2000 1 / 5 / 200 1 / 5 / 200

**Table 3.** DeiT-base hyperparameters following the tuned hyperparameters of Pethick et al. [2025]

Hyperparameter Unconstrained Scion Unconstrained ClippedScion Layers 12 Head dim 64 Activation function

√

2· GELU (scaled to preserve variance) Normalization function RMSNorm Sequence Length 197 Dataset ImageNet-1k Stepsize schedule Cosine decay Max lr 0.00024 Warmup epochs 0 End lr 10−7 Batch size Epochs 200 Averaging parameter α 0.1 Radius ρ1 / ρℓ/ ρL 25 / 25 / 500 Clipping parameter ρ -

**Table 4.** NanoGPT hyperparameters following the tuned hyperparameters of Pethick et al. [2025].

Hyperparameter AdamW (Unconstrained) Scion (Unconstrained) ClippedScion Layers 12 Head dim 128 Activation function 2 · ReLU(x)2 Vocabulary size 50304 Dataset FineWeb batch size 512 block size Iterations n Warmdown 28.5% or 0%

Stepsize schedule Constant then linear decay γk =

(γ if k < n −m γ · (n−k m) if k ≥n −m Warmup 5% 0 Gradient clipping Yes No Momentum β1 / β2 0.9 / 0.95 - Averaging parameter α - 0.1 Stepsize γρ 0.0018 0.00036 Clipping parameter ρ - 600 for 124M model and 6000 for 1B model Radius r1 / rℓ/ rD - - /50 / 3000
