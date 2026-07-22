---
title: "Rademacher Complexity for Distributionally Robust Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40147
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40147/44108
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Rademacher Complexity for Distributionally Robust Learning

<!-- Page 1 -->

Rademacher Complexity for Distributionally Robust Learning

Zhengyu Zhou, Weiwei Liu*

School of Computer Science,

Wuhan University, China {zzysince1999, liuweiwei863}@gmail.com

## Abstract

The goal of distributionally robust learning is to learn models capable of performing well against distributional shifts, such as latent heterogeneous subpopulations, unknown covariate shifts, or unmodeled temporal effects. Recently, Duchi and Namkoong (2021) have proven an upper bound for the excess risk of distributionally robust learning through the lens of covering number argument. However, there are situations where the covering argument fails. This motivates us to study the generalization bound through the lens of Rademacher complexity. More specifically, we consider the Cressie-Read divergence (Cressie and Read 1984), fk(t) ∝tk −1. Our theoretical results indicate that the excess risk is of the order OP (n− 2k∗), where k∗= k k−1. The decay rate of the excess risk increases with increasing k. As illustrative examples, we consider three learning settings: 1) linear classifier; 2) Gaussian reproducing kernel Hilbert space; 3) one-hiddenlayer networks. The empirical results validate our theoretical findings.

## Introduction

In safety- and fairness- critical systems (Knight 2002), the goal is to learn machine learning models that achieve uniformly good performance over all input values. Examples include medical diagnosis, autonomous vehicles, criminal justice and credit evaluations, where poor performance on the tails of the inputs leads to high-cost system failures. By contrast, methods that optimize average performance, often produce models that suffer low performance on the “hard” instances of the population. For example, recent works (Blodgett, Green, and O’Connor 2016; Hashimoto et al. 2018) have demonstrated that models with low average error still fail on particular groups of data points. In light of this, various approaches have attempted to reduce the worstgroup training loss through Distributionally Robust Learning (DRL) or by simply upweighting the minority groups.

In addition to latent heterogeneity in the population, distributional shifts in covariates (Shimodaira 2000; Ben-David et al. 2006) or unobserved confounding variables (Hand 2006) can contribute to changes in the data generating distribution. The performance of machine learning models de-

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

grades significantly on domains that are different from what the model is trained on (Hand 2006; Blitzer, McDonald, and Pereira 2006; Saenko et al. 2010; Torralba and Efros 2011).

To mitigate these challenges, some works have developed a DRL framework that is explicitly robust to local changes in the data-generating distribution. Concretely, let Z be the instance space, P be the data-generating distribution on the instance space Z, Z be a random element of Z, and H be a class of measurable functions h: Z 7→R+, each of which quantifies the loss of a certain decision rule applied to instances z ∈Z. So, with a slight abuse of terminology, we will refer H as the hypothesis class. Rather than minimizing the average loss EP [h(Z)], we study the distributionally robust problem:

min h∈H

Rf(P, h):= sup

Q≪P

{EQ[h(Z)]: Df(Q∥P) ≤ρ}

,

(1) where Q is a distribution over Z, Q ≪P indicates that Q is absolutely continuous with respect to P, and the hyperparameter ρ > 0 modulates the distributional shift. Here,

Df(Q∥P):=

Z f dQ dP dP is the f-divergence between Q and P, where f: R 7→R+ = R+ ∪{∞} is a convex function satisfying f(1) = 0 and f(t) = +∞for any t < 0.

The worst-case risk (1) upweights the regions of Z with high losses h(z); thus (1) optimizes the tail performance, which is measured by the loss of “hard” examples. As long as the alternative distribution Q remains ρ-close to the datagenerating distribution P, the hypothesis h∗∈H that minimizes (1) evidently guarantees that EQ[h∗(Z)] ≤Rf(P, h∗) and provides the smallest such bound, which is equivalent to controlling the tail-performance under P. Let Pn denote the empirical distribution on Z1,..., Zn i.i.d. ∼ P; accordingly, we minimize the following empirical counterpart of (1):

ˆh ∈argmin h∈H

{Rf(Pn, h):= sup Q≪Pn

{EQ[h(Z)]: Df(Q∥Pn) ≤ρ}

.

(2)

Duchi and Namkoong (2021) have addressed the generalization problem in distributionally robust setting based on the

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

29098

<!-- Page 2 -->

covering number with respect to L∞-norm. However, there are situations where the covering number argument fails, e.g., 1) large model classes for whom the covering numbers are prohibitively large; 2) finite VC classes for whom the covering numbers with respect to L∞-norm are infinite (e.g., class of intervals in R).

A scenario where covering number argument fails Consider the binary classification problem, where the input space is X = R and the label space is Y = {0, 1}. We choose the hypothesis class as H = {I[a,b](·): a < b}. We define the loss function as ℓ(h, (x, y)):= I[h(x)̸ = y] for h ∈H. We also consider the loss function class L = {I[h(x)̸ = y]: h ∈H}. Duchi and Namkoong (2021) use covering number of the loss function class with respect to L∞-norm to provide learning guarantees. We next show the covering number of L with respect to L∞-norm is infinite. Given two different hypothese h1 and h2, there exists x, such that h1(x)̸ = h2(x). Therefore, we have supx,y |I[h1(x)̸ = y]−I[h2(x)̸ = y]| = 1. The L∞-distance between two functions implies the δ-packing number of L is infinite for any δ < 1/2. The relation between the covering number and the packing number (Wainwright 2019, Lemma 5.5) implies that the δ/2-covering number of L with respect to L∞-norm is infinite, for any δ < 1.

In this paper, we try to fill this gap by providing learning guarantees through the lens of Rademacher complexity. Our contributions can be summarized as follows:

• We solve the distributionally robust generalization problem based on f-divergence using the Rademacher complexity and derive a data-dependent upper bound on generalization error. • We provide a general analysis of the excess risk of locally minimax ERM via the Rademacher complexity procedure under f-divergence, which can provide nonvacuous bound in situations where the covering number argument fails. Our generalization error bounds exhibit dependence on the choice of fk. • As illustrative examples, we derive the excess risk bound for linear classifier, Gaussian reproducing kernel Hilbert space and one-hidden-layer neural networks. Furthermore, the experimental results show that l2 regularization is able to reduce the distributionally robust generalization error, while the generalization gap increases with increasing dimension of the feature space, which validate our theoretical results.

## Preliminaries

The uncertainty region is defined as follows:

UP:= {Q: Df(Q∥P) ≤ρ},

The likelihood ratio L(x):= dQ(x)/dP(x) can be used to reformulate our distributionally robust problem (1) as follows:

Rf(P, h) = sup{EQ[h(Z)]: Q ∈UP }

= sup

L≥0

{EP [L(Z)h(Z)]: EP [L(Z)] = 1,

EP [f(L(Z))] ≤ρ},

(3)

where the supremum is over measurable functions. Let Z1,..., Zn be an n-tuple of independent and identically distributed (i.i.d.) training examples drawn from P, while Pn is the empirical distribution on Z1,..., Zn. In the next section, we analyze the performance of the local minimax ERM:

ˆh:= argmin h∈H

Rf(Pn, h). (4)

The generalization error denoted by Rf(P, ˆh) and the excess risk denoted by Rf(P, ˆh) −infh′∈H Rf(P, h′) are the key quantities to measure the generalization ability of distributionally robust learning. To study these two quantities, we define the empirical Rademacher complexity of H for a given sample Z1,..., Zn as follows:

ˆRn(H):= Eε

" sup h∈H

1 n n X i=1 εih(Zi)

#

, where ε = (ε1,..., εn) is a vector of i.i.d. Rademacher variables. The Rademacher complexity of H, Rn(H) is defined as the expectation of this quantity: Rn(H):= E(Z1,...,Zn)∼P n h

ˆRn(H)

i

. Moreover, f ∗(s):= supt{st −f(t)} is denoted as the Fenchel conjugate, and the dual reformulation of (3) is provided by Shapiro (2017). Lemma 1. For any probability P on Z, k ∈(1, ∞), k∗= k/(k −1), any ρ > 0, and ck(ρ):= (1 + k(k −1)ρ)

1 k, for all h ∈H, we have

Rf(P, h) = inf λ≥0,η∈R

EP λf ∗ h(Z) −η λ

+ λρ + η

.

(5) Divergence families: Much of our work centers on two families of divergence. The R´enyi α-divergence (van Erven and Harremo¨es 2014) between distribution P and Q is as follows:

Dα(P∥Q):= 1 α −1log

Z dP dQ α dQ, (6)

where the limit satisfies D1(P∥Q) = Dkl(P∥Q):= R log dP dQ dP as α goes to 1. For analytical reasons, we also use the equivalent Cressie-Read family of f-divergence (Cressie and Read 1984):

fk(t):= tk −kt + k −1 k(k −1), so f ∗ k(s):= 1 k h

((k −1)s + 1)k∗

+ −1 i

,

(7)

where k ∈(1, +∞), k∗= k k−1 and t+ = max{0, t}. Let fk(t) = +∞for t < 0; we further define f1 and f0 as their respective limit as k goes to 0 and 1. The family of divergence (7) includes χ2-divergence (k = 2), empirical likelihood f0(t) = −log t + t −1, and KL-divergence f1(t) = t log t −t + 1, and we frequently employ the following shorthand:

Rk(P, h):= sup

Q≪P

{EQ[h(Z)]: Dfk(Q∥P) ≤ρ}. (8)

29099

<!-- Page 3 -->

For ease of exposition, we here focus on k ∈(1, ∞). By minimizing (5) over λ ≥0, we obtain a simplified dual formulation for the Cressie-Read family (7), which is used to protect against worst-case distributional shifts.

Lemma 2. For any probability P on Z,k ∈(1, ∞), k∗= k/(k −1), any ρ > 0, and ck(ρ):= (1 + k(k −1)ρ)

1 k, for all h ∈H, we have:

Rk(P, h) = inf η∈R ck(ρ)EP h

(h(Z) −η)k∗

+ i 1 k∗+ η

. (9)

Proof of Lemma 2. Invoking Lemma 25 in the Appendix, we have the Fenchel conjugate of fk:

f ∗ k(s) = 1 k ((k −1)s + 1)k∗

+ −1 k

Substituting this into the dual formulation (5), we arrive at sup Q≪P

{EQ[Z]: Dfk(Q∥P) ≤ρ}

= inf λ≥0,η λEP f ∗ k

Z −η λ

+ λρ + η

= inf λ≥0,η

(

(k −1)k∗ k λ1−k∗EP

"

Z −η + λ k −1 k∗

+

#

+λ(ρ −1 k) + η

= inf λ≥0,˜η n

(k −1)k∗k−1EP h

(Z −˜η)k∗

+ i λ1−k∗

+ ρ + 1 k(k −1)

λ + ˜η

, where the last line is followed by setting ˜η:= η − λ k−1. Taking derivative of λ to minimize the preceding expression, we have (noting that (k∗−1)/k∗= 1/k):

λ = (k −1)(k(k −1)ρ + 1)−1 k∗

EP h

(Z −˜η)k∗

+ i 1 k∗.

By substituting it into the preceding expression, we find that the supremum is inf

˜η (k(k −1)ρ + 1)

1 k

EP h

(Z −˜η)k∗

+ i 1/k∗

+ ˜η, which concludes our proof.

To illustrate that the simplified dual form (9) is equivalent to optimizing the tail-performance of a model, we introduce a risk-averse loss, namely conditional value-at-risk (CVaR) (Rockafellar, Uryas’ev et al. 2000). Krokhmal (2007) shows that the dual form (9) is a higher-order generalization of the classical CVaR (Rockafellar, Uryas’ev et al. 2000), which corresponds to Rk(P, h) with k = ∞(or k∗=1).

Case k = ∞. Example 1. For 0 < α ≤1, the conditional value-at-risk is

CVaRα(P, h):= inf η∈R α−1EP

(h(Z) −η)+

+ η

.

(10)

(10) corresponds to an uncertainty set arising out of limiting f−divergence or R´enyi divergence. Recalling the R´enyi divergence (6), we have D∞(Q∥P):= limα→∞Dα(P∥Q):= limα→∞ 1 α−1log

R dP dQ α dQ = ess sup log dQ dP. If we define f∞,c = 0 for 0 ≤t ≤c and +∞otherwise, then the uncertainty region can be expressed via the following calculation (Shapiro, Dentcheva, and Ruszczynski 2014, Example 6.19):

UP:=

Q: D∞(Q∥P) ≤log 1 α

= n

Q: Df∞,α−1 (Q∥P) ≤1 o

= {Q: there exists Q′, β ∈[α, 1], s.t. P = βQ + (1 −β)Q′}.

It can be readily observed that the optimal η of (10) is the α-quantile of h(Z), which is defined as below.

q(α):= inf q {P[h(Z) > q] ≤α}.

The dual form (10) shows that CVaR minimizes the expected risk on the worst α portion of the training data.

To study the relation between the distributionally robust risk Rk(P, h) and the expected loss of hypothesis h, we consider the case of k = 2.

Case k = 2. We derive a bound of the distributionally robust loss in terms of the expected loss and variance of hypothesis h for χ2-divergence. In the interests of conciseness, we first introduce a shorthand notation for the loss variance of a hypothesis h ∈H.

σ(h):= p

EP [(h(Z) −E[h(Z)])2].

Proposition 3. For any function h: H →R with finite first and second moment under distribution P,

E[h(Z)] ≤R2(P, h) ≤E[h(Z)] +

√

2ρ1/2σ(h).

Remark 4. In light of this proposition, we suggest that in the χ2-divergence case, introducing the variance of the hypothesis as a regularizer can improve the distributional robustness, which is measured by R2(P, h).

Learning Guarantees for DRL When no ambiguity exists, we use φη,h(z) and ck to denote h(z) −η and ck(ρ), respectively. This section will be structured as follows: first, §3.1 provides an upper bound of the generalization error via entropy integral. §3.2 derives an upper bound of the excess risk through the lens of Rademacher complexity, and further bounds the Rademacher complexity with entropy integral. Finally, we establish the expected loss guarantee for the empirical DRL minimizer in §3.3. The proofs of the main results in this paper can be found in the Appendix.

## 3.1 Data-Dependent Bound on Generalization Error

We begin by imposing standard regularity assumptions which enable us to invoke concentration-of-measure results for empirical processes.

29100

<!-- Page 4 -->

Assumption 5. The instance space Z is bounded as follows:

diam(Z):= sup z,z′∈Z

∥z′ −z∥2 < ∞.

Assumption 6. The functions in H are upper semicontinuous and uniformly bounded as follows: 0 ≤h(z) ≤M < ∞for all h ∈H and z ∈Z.

We use the entropy integral (Talagrand 2014) to measure the complexity of the hypothesis class H:

C(H) =

Z ∞

0 p log N(H, ∥· ∥∞, u)du, where N(H, ∥· ∥∞, u) denotes the covering number of H in the uniform metric ∥f −f ′∥∞= supz∈Z |f(z) −f ′(z)| with radius u.

Before introducing our main theoretical results, we first present a useful lemma. For ease of notation, for any fixed h ∈H, let gk(η, P):= ck

EP h

(h(Z) −η)k∗

+ i 1 k∗

+ η.

We have Rk(P, h) = infη gk(η, P) from Lemma 2. Lemma 7. If h(Z) ∈[0, M], then for any distribution P:

inf η∈R gk(η, P) = inf η gk(η, P): η ∈

− 1 ck −1M, M

.

Remark 8. The above lemma restricts the domain of η to a compact set, which is crucial to our uniform concentration result. Theorem 9. Under Assumptions 5-6 and for any t > 0,

P

∃h ∈H: Rk(P, h) > min η≥0

(

EPn[(φη,h)k∗

+ ]

1 k∗+ η + 1

+ ck t √nC1(k, ρ, M) + r log(η + 1)

n C1(k, ρ, M)

+ 24 √nC2(k, ρ, M)C(H)

1 k∗

)!

≤2 exp

−2t2 and

P

∃h ∈H: Rk(Pn, h) > min η≥0

(

EP [(φη,h)k∗

+ ]

1 k∗+ η + 1

+ ck t √nC1(k, ρ, M) + r log(η + 1)

n C1(k, ρ, M)

+ 24 √nC2(k, ρ, M)C(H)

1 k∗

)!

≤2 exp

−2t2 where ck and k∗ are defined in Lemma 1 and C1(k, ρ, M), C2(k, ρ, M) are constants. More specif- ically, C1(k, ρ, M) = ckM ck−1 k∗ and C2(k, ρ, M) = k∗ ckM ck−1 k∗−1

.

## 3.2 Excess Risk Bounds

Theorem 10. Under Assumptions 5-6, for any h ∈H, the following holds with probability of at least 1 −δ:

Rk(P, ˆh) −Rk(P, h) ≤2ck

Rn(ψ ◦Φ)

1 k∗

+ 3C3(k, ρ, M)

log(2/δ)

2n

1 2k∗,

(11)

where

Φ = φη,h: h ∈H, η ∈

− 1 ck −1M, M

, ψ(t) = tk∗

+, ψ ◦Φ:= {ψ ◦φ: φ ∈Φ} and C3(k, ρ, M) = c2 kM ck−1. In particular, if we take h = argmin h′∈H

Rk(P, h′), the left-hand side represents the excess risk.

Remark 11. Note that we bound the excess risk with the Rademacher complexity of the function class ψ ◦Φ, which can be bounded by the Dudley’s entropy integral (Talagrand 2014). We next invoke an important lemma, which is useful for bounding the Rademacher complexity of ψ ◦Φ and can be found in (Mohri, Rostamizadeh, and Talwalkar 2012, Lemma 4.2).

Lemma 12 (Talagrand’s contraction inequality). Let ψ be a ρ-Lipschitz function. For any function class H, we have

Rn(ψ ◦H) ≤ρRn(H).

Remark 13. Note that the function t 7→tk∗

+ is not Lipschitz on the entire domain; however, the function class is bounded. By a truncation argument (Wainwright 2019, Example 5.29), the invoked lemma can be made applicable to our cases.

Proposition 14.

Rn(ψ ◦Φ) ≤ 1 √n

C4(k, ρ, M)C(H) + C5(k, ρ, M)

, where C4(k, ρ, M) = 24k∗ ckM ck−1 k∗−1

, C5(k, ρ, M) =

24k∗ ckM ck−1 k∗

.

Remark 15. The Rademacher complexity of the function class ψ ◦Φ can be bounded by the Dudley entropy integral of the original function class H.

## 3.3 Expected Loss Guarantee

To establish expected loss guarantees for the locally minimax ERM, we present the following inequality, which relates the expected loss to the distributionally robust loss.

Proposition 16. Under Assumption 2, we have

EP [h(Z)] ≤Rk(P, h) ≤ck(ρ)M

1 k EP [h(Z)]1−1 k.

29101

<!-- Page 5 -->

Remark 17. Note that, for fixed ρ, when k approaches infinity, the right-hand side converges to EP [h(Z)], which coincides with our intuition: the uncertainty set UP shrinks as k increases. Theorem 18. Under Assumptions 1-2, the following holds with probability of at least 1 −δ:

EP h

ˆh(Z)

i

≤ckM

1 k EP h∗ avg(Z)

1−1 k

+ 2ck (Rn(ψ ◦Φ))

1 k∗

+ 3C3(k, ρ, M)

log(2/δ)

2n

1 2k∗, where ˆh denotes the locally minimax ERM, and h∗ avg:= argminh∈HEP [h(Z)]. Remark 19. Theorem 18 shows that when k approaches in- finity, ck and M

1 k converge to 1 and E h∗ avg(Z)

1−1 k converges to E h∗ avg(Z)

. Therefore, given sufficient samples, the expected loss of locally minimax ERM is close to the optimal expected loss, which is in line with Hu et al. (2018, Theorem 2).

Proof sketch. Using the left half of Proposition 16 and Theorem 10,

EP h

ˆh(Z)

i

≤Rk(P, ˆh) ≤Rk(P, h∗ avg)

+ 2ck (Rn(ψ ◦Φ))

1 k∗

+ 3C3(k, ρ, M)

log(2/δ)

2n

1 2k∗.

We can then bound Rk(P, h∗ avg) using the right half of Proposition 16, and thereby obtain the desired result.

## 4 Example Bounds In this section, we illustrate the use of

Theorem 10. Let the instance space X be a subset of the d-dimensional Euclidean space, namely Rd. Z is equipped with the following Euclidean distance:

dZ(z, z′) = q

∥x −x′∥2

2 + |y −y′|2. (12)

We use metric entropy to bound the Rademacher complexity, and accordingly require the following estimate of the covering number of balls in some metric spaces (Wainwright 2019, Lemma 5.7). The following lemma relates the metric entropy to the socalled volume ratio. It involves the Minkowski sum A+B:= {a + b: a ∈A, b ∈B}, and the volume of the unit ball based on the Lebesgue measure is denoted by vol(B):= R

I{x ∈B}dx. Lemma 20 (Volume ratios and metric entropy). Consider a pair of norms ∥·∥and ∥·∥′ on Rd, and let B and B′ be their corresponding unit balls (i.e., B = θ ∈Rd|∥θ∥≤1

, with B′ similarily defined). Then the δ-covering number of B in the ∥· ∥′-norm therefore obeys the bounds

1 δ d vol(B)

vol(B)′ ≤N(δ, B, ∥· ∥′)

(a)

≤vol(2 δ B + B′) vol(B′).

Whenever B′ ⊆B, the upper bound (a) may be simplified by observing that vol

2 δ B + B′

≤vol

2 δ + 1

B

=

2 δ + 1 d vol(B).

## 4.1 Linear Classifier in Binary Classification

We begin here with binary linear classifiers. In this setting, we define X = {x ∈Rd: ∥x∥2 ≤r0}, Y = {−1, +1}, and let the hypothesis class F ⊆RX be a set of linear functions of x ∈X. More specifically, we define fw(x) = ⟨w, x⟩and consider prediction vector w with l2 norm constraint, i.e.,

F = {fw(x): ∥w∥2 ≤W}.

Here we consider the hinge loss, i.e., ℓ(fw(x), y) = ϕ(y⟨w, x⟩) = max{0, 1 −y⟨w, x⟩}. Thanks to Proposition 14, it is sufficient to bound the entropy integral of

HL:= {(x, y) 7→ϕ(y⟨w, x⟩): ∥w∥2 ≤W}.

Corollary 21. For any distribution P on Z, with probability of at least 1 −δ,

Rk(P, ˆh) −R∗ k(P, HL)

≤2ckn− 1 2k∗

C4(k, ρ, 1 + Wr0)( p d log 3 + 3Wr0

√ d/2)

+ C5(k, ρ, 1 + Wr0)

1 2k∗

+ 3C3(k, ρ, 1 + Wr0)

log(2/δ)

2n

1 2k∗,

(13) where R∗ k(P, HL):= infh′∈HL Rk(P, h′).

## 4.2 Gaussian Reproducing Kernel Hilbert Space

In this case, we consider the instance space X = {x ∈X: ∥x∥≤r0)} and label space Y = [−B, B] for some value of r0, B > 0, and equip Z with the Euclidean metric (12).

Let (HK, ∥· ∥K) be the Gaussian reproducing kernel Hilbert space (RKHS) with the kernel K(x1, x2) = exp(−∥x1 −x2∥2

2/σ2) for some σ > 0, and let Br:= {h ∈HK: ∥h∥≤r} be the radius-r ball in HK. Let H be the class of all functions of the form h(z) = (y −f0(x))2, where the predictor f0: X 7→R belongs to IK(Br). Here, IK(Br) denotes an embedding of Br into the space C(X) of continuous real-valued functions on X equipped with the sup norm ∥f∥X:= supx∈X |f(x)|.

Using the covering number estimates drawn from the work of Cucker and Ding Xuan (2007), we can prove the generalization bound for Gaussian RKHS.

Proposition 22. For compact X ⊂Rd, the following holds for all u ∈(0, r/2]:

log N(IK(Br), ∥· ∥X, u)

≤d

32 + 640d(diam(X))2 σ2 d+1 log r u d+1

.

29102

<!-- Page 6 -->

Corollary 23. For any distribution P on Z, with probability of at least 1 −δ,

Rk(P, ˆh) −R∗ k(P, H)

≤2ckn− 1 2k∗

C4(k, ρ, 2B2 + 2r2)K1

+ C5(k, ρ, 2(B2 + r2))

1 2k∗

+ 3C3(k, ρ, 2(B2 + r2))

log(2/δ)

2n

1 2k∗,

(14)

where R∗ k(P, H):= infh′∈H Rk(P, h′) and

K1 =

√ d

2Γ d + 3

2, log 2

+ (log 2)

d+1

2

32 + 2560dr2 0 σ2 d+1

2 r2 + Br

.

## 4.3 One-Hidden-Layer Neural Network

Here, we consider the loss class H = {(x, y) 7→max{0, 1− y Pm j=1 ujs(αT j x)}: ∥u∥1 ≤Λ, ∥αj∥2 ≤Ω, for j = 1,..., m}, where u = (u1,..., um), αj ∈Rm for j = 1,..., m and s(·) is the ReLU activation. Corollary 24. For any distribution P on Z, with probability of at least 1 −δ,

Rk(P, ˆh) −R∗ k(P, H)

≤2ckn− 1 2k∗

C4(k, ρ, 1 + ΩΛr0)K2

+C5(k, ρ, 1 + ΩΛr0)

1 2k∗

+ 3C3(k, ρ, 1 + ΩΛr0)

log(2/δ)

2n

1 2k∗,

(15)

where R∗ k(P, H):= infh′∈H Rk(P, h′) and K2 = 3d 1 2 m 3 2 ΛΩr0 + 3Λd 1 2.

## 5 Numerical Study

In this section, we validate three theoretical findings for linear classifiers, as follows: (i) verifying that the decay rate of distributionally robust generalization is dependent on k; (ii) establishing that there is a dimension dependence in distributionally robust generalization, i.e., that distributionally robust generalization is more difficult when the dimension of the feature space is higher; (iii) verifying that controlling the l2 norm of the model parameter can reduce distributionally robust generalization.

We investigate distributionally robust generalization via a binary classification experiment using hinge loss l(w, (x, y)) = (1 −yxT w)+, where y ∈{+1, −1} and x ∈Rd. We select a vector w∗

0 ∈Rd uniformly on the unit sphere and generate data as follows:

X i.i.d. ∼N(0, Id) and

Y |X =

( sign(XT w∗

0) w.p. 0.9

−sign(XT w∗

0) w.p. 0.1

(a)

(b)

(c)

**Figure 1.** (a) Linear classifier. Test loss under different sample sizes n and parameters k; (b) Linear classifier. Test loss under different perturbations ρ and feature space dimensions d; (c) Linear classifier. Excess risk under different perturbations ρ and regularization coefficients λ.

where N(0, Id) denotes the normal distribution with mean

29103

![Figure extracted from page 6](2026-AAAI-rademacher-complexity-for-distributionally-robust-learning/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-rademacher-complexity-for-distributionally-robust-learning/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-rademacher-complexity-for-distributionally-robust-learning/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

0 and covariance matrix Id, and sign(x) =

 



1, if x > 0 0, if x = 0 −1, if x < 0

We train the binary linear classifier using the following objective function:

min w sup Q≪Pn

{EQ[l(fw(x), y)]:Dfk(Q∥Pn) ≤ρ}+λ∥w∥2

2,

(16) where l(·) is the hinge loss and fw(x):= ⟨w, x⟩. With the aid of the duality formulation, we can transfer the mini-max problem (16) to a min-min problem:

min w,η ck(ρ)EPn h

(l(fw(x), y)−η)k∗

+ i 1 k∗+η+λ∥w∥2

2

.

Thus, we can jointly minimize the distributionally robust risk via gradient descent.

In our first experiment, we set d = 5, λ = 0 and vary the values of k and sample size n. For each (n, k) pair, we run the training algorithm; in each run, we sample n training data independently. In Figure 1(a), we plot the test risk as a function of n and k. As we can see from Figure 1(a), the decay rate of the test risk increases with the increasing k, which is in line with our Theorem 10: the test risk has an Op(n− 1 2k∗) rate, where k∗= k k−1. However, we can also observe that at a lower number of training samples, the generalization error increases with the increasing k. This phenomenon is explicable; in our theoretical result Corollary 21, when k increases, the constants C3(k, ρ, 1 + Wr0) and C4(k, ρ, 1 + Wr0) also increase.

In our second experiment, we choose λ = 0, k = 2, and study the dependence of distributional generalization error on the dimension of the feature space. We construct two additional synthetic datasets with d = 15 and d = 20, respectively. To facilitate fair comparison, we generate the data in a similar way to the first experiment,

X i.i.d. ∼N(0, Id/d).

Moreover, we keep the distribution of Y conditioned on X, in the same way as in the first experiment. This construction ensures that the l2 norm of every single data point is kept in the same order across the three datasets. The distributional generalization error gap is plotted in Figure 1(b). From Figure 1(b), we can observe that the generalization gap increases as the dimension d increases.

In our third experiment, we fix k = 2 and vary the values of ρ and λ. We run the training algorithm for each (ρ, λ) pair; in each run we sample 100 points of training data independently. In Figure 1(c), we plot the distributional generalization error gap as a function of ρ and λ. From Figure 1(c), we can observe that the generalization gap decreases with increasing λ. Accordingly, we conclude that l2 regularization is helpful for reducing the distributionally generalization error.

## 6 Related Work

Distributional shifts arise in many guises across the fields of statistics, machine learning, applied probability, simulation and optimization. We here provide a necessarily abridged survey of the strands of work in this area, along with their respective foci. Domain adaptation seeks models that are trained on data from one domain, and performs well on a specified target domain. A typical approach of this kind aims to reweight the distribution P to make it “closer” to the known target distribution Ptarget (Shimodaira 2000; Huang et al. 2006; Bickel, Br¨uckner, and Scheffer 2007; Sugiyama, Krauledat, and M¨uller 2007; Sugiyama et al. 2007).

In the optimization literature, a substantial body of work focuses on distributionally robust optimization problems. Several authors investigate worst-case regions arising out of moment conditions on the data vector X (Delage and Ye 2010; Jiang and Guan 2016). Other works (Ben-Tal et al. 2013; Duchi, Glynn, and Namkoong 2021; Namkoong and Duchi 2017; Lam 2016; Lam and Zhou 2017; Zhou and Liu 2023) studies a scenario similar to our f-divergence formulation (1).

An alternative to our f-divergence based sets {Q: Df(Q∥P) ≤ρ} is Wasserstein balls (Wozabal 2012; Shafieezadeh-Abadeh, Esfahani, and Kuhn 2015; Blanchet and Murthy 2019; Blanchet, Kang, and M. 2019; Rui and Kleywegt 2016; Esfahani and Kuhn 2018; Sinha, Namkoong, and Duchi 2017). Wasserstein ball allows worst-case distributions with different support from the data-generating distribution P. This property, however, means that tractable reformulations are only available under restrictive scenarios (Shafieezadeh-Abadeh, Esfahani, and Kuhn 2015; Esfahani and Kuhn 2018; Sinha, Namkoong, and Duchi 2017) and that they remain computationally challenging. In comparison, our f-divergence formulation is computationally efficient to solve.

## Conclusion

In this work, we present the theoretical guarantees for distributionally robust learning (Theorems 9 and 10). Our results are derived through the lens of Rademacher complexity, which has not previously been applied before. We prove an OP (n− 1 2k∗(log(2/δ))

1 2k∗) convergence rate with probability of at least 1 −δ. The empirical results verify our theoretical findings.

## Acknowledgments

This work is supported by the Key R&D Program of Hubei Province under Grant 2024BAB038, the National Key R&D Program of China under Grant 2023YFC3604702, the Fundamental Research Funds for the Central Universities under Grant 2042025kf0045.

## References

Ben-David, S.; Blitzer, J.; Crammer, K.; and Pereira, F. 2006. Analysis of Representations for Domain Adaptation. In NeurIPS, 137–144.

29104

<!-- Page 8 -->

Ben-Tal, A.; den Hertog, D.; Waegenaere, A. D.; Melenberg, B.; and Rennen, G. 2013. Robust Solutions of Optimization Problems Affected by Uncertain Probabilities. Management Science, 59(2): 341–357. Bickel, S.; Br¨uckner, M.; and Scheffer, T. 2007. Discriminative learning for differing training and test distributions. In ICML, volume 227, 81–88. Blanchet, J. H.; Kang, Y.; and M., K. R. A. 2019. Robust Wasserstein profile inference and applications to machine learning. Journal of Applied Probability, 56(3): 830–857. Blanchet, J. H.; and Murthy, K. R. A. 2019. Quantifying Distributional Model Risk via Optimal Transport. Mathematical Operation Research, 44(2): 565–600. Blitzer, J.; McDonald, R. T.; and Pereira, F. 2006. Domain Adaptation with Structural Correspondence Learning. In EMNLP, 120–128. Blodgett, S. L.; Green, L.; and O’Connor, B. T. 2016. Demographic Dialectal Variation in Social Media: A Case Study of African-American English. In EMNLP, 1119–1130. Cressie, N.; and Read, T. R. C. 1984. Multinomial Goodness-of-Fit Tests. Journal of the Royal Statistical Society, 46(3): 440–464. Cucker, F.; and Ding Xuan, Z. 2007. Learning theory: An approximation theory viewpoint, volume 24. Delage, E.; and Ye, Y. 2010. Distributionally Robust Optimization Under Moment Uncertainty with Application to Data-Driven Problems. Operation Research, 58(3): 595– 612. Duchi, J. C.; Glynn, P. W.; and Namkoong, H. 2021. Statistics of Robust Optimization: A Generalized Empirical Likelihood Approach. Mathematics of Operations Research, 46(3): 946–969. Duchi, J. C.; and Namkoong, H. 2021. Learning Models with Uniform Performance via Distributionally Robust Optimization. The Annals of Statistics, 49(3): 1378–1406. Esfahani, P. M.; and Kuhn, D. 2018. Data-driven distributionally robust optimization using the Wasserstein metric: Performance guarantees and tractable reformulations. Mathematical Programming, 171(1-2): 115–166. Gong, X.; Yuan, D.; and Bao, W. 2021a. Discriminative metric learning for partial label learning. IEEE Transactions on Neural Networks and Learning Systems, 34(8): 4428–4439. Gong, X.; Yuan, D.; and Bao, W. 2021b. Understanding partial multi-label learning via mutual information. In NeurIPS. Gong, X.; Yuan, D.; and Bao, W. 2022. Partial label learning via label influence function. In ICML. Gong, X.; Yuan, D.; Bao, W.; and Luo, F. 2022. A unifying probabilistic framework for partially labeled data learning. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(7): 8036–8048. Hand, D. J. 2006. Classifier technology and the illusion of progress. Statistical Science, 21(1): 1–14. Hashimoto, T. B.; Srivastava, M.; Namkoong, H.; and Liang, P. 2018. Fairness Without Demographics in Repeated Loss Minimization. In ICML, volume 80, 1934–1943.

Hu, W.; Niu, G.; Sato, I.; and Sugiyama, M. 2018. Does Distributionally Robust Supervised Learning Give Robust Classifiers? In ICML, volume 80, 2034–2042. Huang, J.; Smola, A. J.; Gretton, A.; Borgwardt, K. M.; and Sch¨olkopf, B. 2006. Correcting Sample Selection Bias by Unlabeled Data. In In NeurIPS, 601–608. Jiang, R.; and Guan, Y. 2016. Data-driven chance constrained stochastic program. Mathematical Programming, 158(1-2): 291–327. Knight, J. C. 2002. Safety critical systems: Challenges and directions. In ICSE, 547–550. Krokhmal, P. A. 2007. Higher moment coherent risk measures. Lam, H. 2016. Robust Sensitivity Analysis for Stochastic Systems. Mathematics of Operations Research, 41(4): 1248–1275. Lam, H.; and Zhou, E. 2017. The empirical likelihood approach to quantifying uncertainty in sample average approximation. Operations Research Letters, 45(4): 301–307. Mohri, M.; Rostamizadeh, A.; and Talwalkar, A. 2012. Foundations of Machine Learning. Namkoong, H.; and Duchi, J. C. 2017. Variance-based Regularization with Convex Objectives. In NeurIPS, 2971– 2980. Rockafellar, R. T.; Uryas’ev, S.; et al. 2000. Optimization of conditional value-at-risk. Journal of Risk, 2: 21–42. Rui, G.; and Kleywegt, A. J. 2016. Distributionally robust stochastic optimization with Wasserstein distance. arXiv preprint arXiv:1604.02199. Saenko, K.; Kulis, B.; Fritz, M.; and Darrell, T. 2010. Adapting Visual Category Models to New Domains. In ECCV, volume 6314, 213–226. Shafieezadeh-Abadeh, S.; Esfahani, P. M.; and Kuhn, D. 2015. Distributionally Robust Logistic Regression. In NeurIPS, 1576–1584. Shapiro, A. 2017. Distributionally Robust Stochastic Programming. SIAM Journal on Optimization, 27(4): 2258– 2275. Shapiro, A.; Dentcheva, D.; and Ruszczynski, A. 2014. Lectures on stochastic programming: Modeling and theory. Shimodaira, H. 2000. Improving predictive inference under covariate shift by weighting the log-likelihood function. Journal of Statistical Planning and Inference, 90(2): 227– 244. Sinha, A.; Namkoong, H.; and Duchi, J. C. 2017. Certifiable Distributional Robustness with Principled Adversarial Training. CoRR, abs/1710.10571. Sugiyama, M.; Krauledat, M.; and M¨uller, K. 2007. Covariate Shift Adaptation by Importance Weighted Cross Validation. Journal of Machine Learning Research, 8: 985–1005. Sugiyama, M.; Nakajima, S.; Kashima, H.; von B¨unau, P.; and Kawanabe, M. 2007. Direct Importance Estimation with Model Selection and Its Application to Covariate Shift Adaptation. In NeurIPS, 1433–1440.

29105

<!-- Page 9 -->

Talagrand, M. 2014. Upper and lower bounds for stochastic processes: modern methods and classical problems, volume 60. Torralba, A.; and Efros, A. A. 2011. Unbiased look at dataset bias. In CVPR, 1521–1528. van Erven, T.; and Harremo¨es, P. 2014. R´enyi Divergence and Kullback-Leibler Divergence. IEEE Transactions on Information Theory, 60(7): 3797–3820. Wainwright, M. J. 2019. High-dimensional statistics: A nonasymptotic viewpoint, volume 48. Wozabal, D. 2012. A framework for optimization under ambiguity. Annals of Operations Research, 193(1): 21–47. Zheng, C.; Shi, Z.; Miao, R.; Liu, W.; Yang, T.; Cui, B.; and Uhlig, S. 2025. Answering Subset Query Over Multi- Attribute Data Streams Using Hyper-USS. IEEE Transactions on Knowledge and Data Engineering. Zhou, Z.; and Liu, W. 2023. Sample complexity for distributionally robust learning under chi-square divergence. Journal of Machine Learning Research.

29106
