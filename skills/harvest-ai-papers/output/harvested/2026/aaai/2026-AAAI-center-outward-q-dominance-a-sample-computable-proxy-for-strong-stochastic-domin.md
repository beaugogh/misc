---
title: "Center-Outward q-Dominance: A Sample-Computable Proxy for Strong Stochastic Dominance in Stochastic Multi-Objective Optimisation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39805
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39805/43766
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Center-Outward q-Dominance: A Sample-Computable Proxy for Strong Stochastic Dominance in Stochastic Multi-Objective Optimisation

<!-- Page 1 -->

Center-Outward q-Dominance: A Sample-Computable Proxy for Strong

Stochastic Dominance in Stochastic Multi-Objective Optimisation

Robin van der Laag1, Hao Wang1, Thomas B¨ack1, Yingjie Fan1

1LIACS, Leiden University {r.p.van.der.laag, h.wang, t.h.w.baeck, y.fan}@liacs.leidenuniv.nl

## Abstract

Stochastic multi-objective optimization (SMOOP) requires ranking multivariate distributions; yet, most empirical studies perform scalarization, which loses information and is unreliable. Based on the optimal transport theory, we introduce the center-outward q-dominance relation and prove it implies strong first-order stochastic dominance (FSD). Also, we develop an empirical test procedure based on q-dominance, and derive an explicit sample size threshold, n∗(δ), to control the Type I error. We verify the usefulness of our approach in two scenarios: (1) as a ranking method in hyperparameter tuning; (2) as a selection method in multi-objective optimization algorithms. For the former, we analyze the final stochastic Pareto sets of seven multi-objective hyperparameter tuners on the YAHPO-MO benchmark tasks with qdominance, which allows us to compare these tuners when the expected hypervolume indicator (HVI, the most common performance metric) of the Pareto sets becomes indistinguishable. For the latter, we replace the mean value-based selection in the NSGA-II algorithm with q-dominance, which shows a superior convergence rate on noise-augmented ZDT benchmark problems. These results establish center-outward q-dominance as a principled, tractable foundation for seeking truly stochastically dominant solutions for SMOOPs.

Code — https://github.com/RvdLaag/qDominance Extended version — https://arxiv.org/abs/2511.12545

## Introduction

Decision-making often involves balancing conflicting objectives under stochasticity. Hyperparameter optimization (HPO) is a typical example, where each run of an algorithm produces a vector of random outcomes (validation accuracy, training time, memory footprint, etc.) whose joint distribution reflects noise in the data and the learning procedure itself. More generally, each candidate solution of a stochastic multi-objective optimization problem (SMOOP) is associated with a distribution of multi-objective performance. Comparing different solutions, therefore, requires ranking these distributions rather than comparing single deterministic points.

Studies on SMOOPs have typically resorted to one of the following pragmatic strategies:

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

• Scalarization: turns the problem into a single-objective stochastic optimization problem by applying some predetermined scalarization function to the objectives (Caballero et al. 2004; Abdelaziz 2012; Drugan and Now´e 2013; Trappler, Helbert, and Riche 2025); • Single-sample iterations: solving the optimization problem by evaluating candidate solutions using a single Monte-Carlo draw per iteration (Jin and Branke 2005); • Moment surrogates: replacing each random objective by a summary statistic, such as the mean (Fliege and Xu 2011), variance, (C)VaR (Daulton et al. 2022), or its worst-case scenario, e.g., minimax robustness (Ehrgott, Ide, and Sch¨obel 2014), multi-objective multi-armed bandits (Lu et al. 2019; Xu and Klabjan 2023), thereby converting the problem into a deterministic one; • Weak stochastic dominance testing: comparing the empirical cumulative distribution functions (CDF) of the candidate solutions (Teich 2001);

While these strategies ease computation, they also discard some parts of the distributional structure and can lead to suboptimal solutions.

A principled alternative to compare distributions is strong first-order stochastic dominance (FSD): a distribution A is preferred to B if every non-decreasing utility considers samples from A at least as good as samples from B in expectation. Strong FSD is attractive; it preserves distributional information and imposes no arbitrary scalarization. Section 2 contains the necessary background on (stochastic) multiobjective optimization problems and stochastic dominance.

Testing for strong FSD through samples can be computationally difficult in higher dimensions. Recent work by Rioux et al., 2025 proposes a statistic that assesses multivariate almost stochastic dominance by constructing an optimal coupling between two distributions.

In this paper, we take a different route. We introduce center-outward q-dominance (formalized in Section 4): utilizing center-outward distributions and quantile functions (Hallin 2017), which we cover in Section 3, we construct maps from each distribution to the same uniform distribution Ud on the unit ball. With this construction, all pairwise comparisons reuse a single common reference frame; we thus only compare samples with identical center-outward rank and sign, ruling out the possibility of incoherent cou-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

26037

<!-- Page 2 -->

plings when comparing more than two distributions, such as Xi ↔Yj, Xi ↔Zk, but not Yj ↔Zk. Consequently, we only need to compute one coupling per distribution, independent of the number of distributions we wish to compare, in contrast to the method in (Rioux et al. 2025), which requires the computation of a coupling for each order pair of distributions. We show that if q-dominance holds for all quantiles, we obtain strong FSD; if it only holds up to some quantile, we get a natural relaxation. Because the centeroutward ranks are computed once, the entire set of relaxations is obtained at no extra cost. Rioux et al. can similarly vary their threshold ε0 for free once an entropic-OT coupling is fixed, but exploring different regularization levels λ or functions h still requires a new coupling to be obtained, whereas our method has no tunable hyperparameters. Furthermore, our finite-sample test admits an explicit minimum sample size threshold n∗(δ) that guarantees a user-specified Type-I error δ. Lastly, we propose a sorting procedure that enables practical ranking of solutions through pairwise qdominance and its relaxation.

We verify the usefulness of our approach with two complementary experiments in Section 5. Firstly, we re-analyze the final stochastic Pareto sets of seven multi-objective HPO methods on the YAHPO-MO benchmark tasks (Pfisterer et al. 2022) with q-dominance, as opposed to the expected Hypervolume Indicator (HVI). We find that, with qdominance, we can still meaningfully compare the different methods even when the expected HVI of the Pareto sets becomes indistinguishable. Secondly, we apply q-dominance to the well-known NSGA-II algorithm (Deb et al. 2002) for multi-objective optimization, where q-dominance is used to compare different solutions under uncertainty of the objectives. Compared to the default mean value-based or singlesample-based selection, q-dominance enables the algorithm to converge significantly faster on noise-augmented ZDT benchmark problems (Zitzler, Deb, and Thiele 2000).

## Background

In this section, we will provide an introduction to the background of multi-objective optimization and stochastic dominance.

## 2.1 Multi-Objective Optimization Problems

A multi-objective optimization problem (MOOP) is typically formulated as max x (f1(x),..., fm(x))

subject to x ∈X,

(1)

where X ⊆Rd is the solution space, and f: X →Rm, with m ≥2, the vector-valued objective function.

Definition 1. A feasible solution x ∈X is said to Pareto dominate another solution y ∈X, if

(i) For all i ∈{1,..., m}, fi(x) ≥fi(y), and (ii) There exists an i ∈{1,..., m}, such that fi(x) > fi(y).

A solution x∗∈X along with its image point f(x∗) is called Pareto optimal if there does not exist another solution that dominates it. The set of Pareto optimal points is called the Pareto front.

Assume a probability space (Ω, A, P). Stochastic multiobjective optimization problems (SMOOP) arise when the objective function is stochastic, i.e., f: X ×Ω→Rm. With ω ∈Ω, an SMOOP can be written as max x (f1(x, ω),..., fm(x, ω))

subject to x ∈X,

(2)

Notably, the Pareto optimal solution to an SMOOP depends on the realization ω. Two typical approaches to interpret the maximization, and thus the comparison, of random vectors are the multi-objective method and the stochastic method (Abdelaziz 2012).

The multi-objective method defines, for each component of the objective function fi, a vector (F(1)

i (fi(x, ω)),..., F(ri)

i (fi(x, ω))) of one or more statistical functionals F(j)

i of the random variable fi(x, ω), common functionals are the expectation and the variance. With this, we reformulate the SMOOP (2) as an MOOP with the r1 + · · · + rm functionals as the deterministic objectives.

The stochastic method scalarizes the random objectives f1(x, ω),..., fm(x, ω) using a function u: Rm →R, and reformulates SMOOP (2) as a single-objective stochastic optimization problem.

Both of these methods have obvious downsides. The multi-objective method reduces the joint distribution of the objectives to a finite set of summary statistics (the functionals), losing information about the distribution in the process, particularly because the dependency between the random objectives is not taken into account. The stochastic method does not lose this dependency between objectives; however, it does require that the scalarization function is known, and the solution does not generalize to other scalarization functions.

A different approach is to utilize the concept of multivariate stochastic dominance, which allows us to compare random vectors directly without losing any information.

## 2.2 Stochastic Dominance

Firstly, let us introduce the concepts of first-order stochastic dominance (FSD) in the scalar case. Definition 2. Let X and Y be real-valued random variables with cumulative distribution functions FX and FY. We say that X first-order stochastically dominates Y, written X ⪰1 Y, if and only if any (and hence all) of the following equivalent conditions hold:

(i) FX(z) ≤FY (z) for all z ∈R; (ii) E[u(X)] ≥E[u(Y)] for all non-decreasing utility functions u: R →R. A natural first step is to lift Definition 2 to Rd by replacing the scalar CDF with the joint CDF

FX(z) = P(X1 ≤z1,..., Xd ≤zd)

26038

<!-- Page 3 -->

and by letting the test set be all non-decreasing utility functions u: Rd →R. Crucially, in dimension d > 1, these two characterizations diverge, giving rise to the weak (via CDFs) and strong (via utility functions) notions of multivariate FSD.

Definition 3 (Weak FSD). Let X, Y ∈Rd be real-valued random vectors with joint CDFs FX and FY. We say that X weakly stochastically dominates Y, written X ⪰w Y, if and only if

FX(z) ≤FY(z), ∀z ∈Rd.

Definition 4 (Strong FSD). We say that X strongly stochastically dominates Y, written X ⪰1 Y, if and only if

E[u(X)] ≥E[u(Y)], for all non-decreasing utility functions u: Rd →R.

To relate the two orders, we first recall an equivalent characterization of strong FSD from (Sriboonchita et al. 2009) that replaces utilities by probabilities on so-called upper sets.

Proposition 1. For random vectors X, Y ∈Rd the following are equivalent:

(i) X ⪰1 Y (Definition 4). (ii) For every upper set M ⊆Rd,

P(X ∈M) ≥P(Y ∈M).

Here an upper set is any M ⊆Rd such that for any z, w ∈Rd with w ≥z we have that w ∈M whenever z ∈M.

Proof. We refer to (Sriboonchita et al. 2009).

The upper set view makes the hierarchy between the two orders apparent, yielding the following result.

Theorem 1. For every dimension d ≥1 and every pair of random vectors X, Y ∈Rd,

X ⪰1 Y =⇒X ⪰w Y.

Proof. For m = (m1,..., md) ∈Rd we have that 1 − FX(m) = P(X ≥m) = P(X ∈[m1, ∞)×· · ·×[md, ∞)) and similarly for Y. The set [m1, ∞) × · · · × [md, ∞) is an upper set in Rd, thus if P(X ∈M) ≥P(Y ∈M) for all upper sets M ∈M, then it also holds for the special form above. This gives us that 1 −F(m) ≥1 −G(m), implying X ⪰w Y.

The converse does not hold for dimensions d > 1, as the next counterexample from (Kopa and Petrov´a 2018) demonstrates.

Example 1. Consider the two random vectors

X =

(0, 1), w.p. 1/2, (1, 0), w.p. 1/2. Y =

(0, 0), w.p. 1/2, (1, 1), w.p. 1/2.

Then FX(z) ≤FY(z) for all z ∈R2 and thus X ⪰w Y. Consider the upper set M = {m ∈R2: m1 + m2 ≥3

2}, then 0 = P(X ∈M) < P(Y ∈M) = 1

2, and thus X̸ ⪰1 Y.

Example 1 makes the dilemma explicit: in dimensions d > 1 weak FSD can be too permissive, declaring X ⪰w Y even though strong FSD rejects that claim, i.e. X̸ ⪰1 Y. Equivalently, there exists a non-decreasing utility u—for instance u(x1, x2) = exp(x1 + x2)—for which E[u(X)] < E[u(Y)].

As noted in the introduction, testing for strong FSD can be computationally difficult without full knowledge of the joint distribution. Rioux et al. use the following theorem from (Shaked and Shanthikumar 2007) for their optimal transport approach.

Theorem 2. The random vectors X, Y satisfy X ⪰1 Y, if and only if there exists a coupling (bX, bY) of (X, Y) satisfying P(bX ≥bY) = 1.

Rioux et al. then provides the following lemma, casting this theorem into the context of optimal transport.

Lemma 3. Let PX, PY denote the distributions of the random vectors X and Y, respectively. Then X ⪰1 Y if inf π∈Π(PX,PY)

Z c dπ = 0, where c: Rd × Rd →R+ is the cost function c(x, y) = 1{x≤y} and Π(PX, PY) denotes the set of all couplings of (PX, PY).

When more than two distributions P1, P2,... must be compared, this method requires solving an optimal transport problem for every ordered pair (Pi, Pj). Because each coupling is optimized in isolation a sample X ∼P1 that is matched to Y ∼P2 under π1,2 and to Z ∼P3 under π1,3 need not have Y matched to Z under π2,3. The resulting family of couplings, therefore, lacks a common reference frame and is difficult to interpret jointly.

In the next section, we introduce center-outward ranks and signs, providing the missing common reference frame that underpins our definition of q-dominance.

Center-Outward Ranks and Signs In this section, we define the center-outward distribution and quantile function, which are rooted in the main result of (McCann 1995) and further developed in (Hallin 2017) and (Hallin et al. 2021).

Throughout this section, we make use of the following notation. Let µd denote the Lebesgue measure over Rd equipped with its Borel σ-field Bd. Furthermore, denote by Pd the family of Lebesgue-absolutely continuous distributions over (Rd, Bd). We use the notation T#P1 = P2 for the distribution P2 of T(X), where X ∼P1, and say that T is pushing P1 forward to P2. Lastly, let Sd−1, Sd, and Sd denote the unit sphere, the open unit ball, and the closed unit ball in Rd, respectively.

## 3.1 Theoretical Definition

We restate the main result of (McCann 1995).

Theorem 4 (McCann 1995). For two distributions P1, P2 ∈ Pd the following statements hold:

26039

<!-- Page 4 -->

(i) the class of functions

∇ΨP1;P2:= {∇ψ | ψ: Rd →R, ∇ψ#P1 = P2}, where ψ is convex and lower semi-continuous, is nonempty; (ii) if ∇ψ′, ∇ψ′′ ∈∇ΨP1;P2, they coincide P1-a.s., that is P1 ({x | ∇ψ′(x)̸ = ∇ψ′′(x)}) = 0; (iii) if P1 and P2 have finite moments of order two, any element of ∇ΨP1;P2 is an optimal quadratic transport pushing P1 forward to P2, i.e. it is a solution to inf γ∈Π(P1,P2)

Z

Rd×Rd∥x −y∥2 dγ(x, y), where Π(P1, P2) denotes the set of joint distributions with marginals P1 and P2. Denote by Ud the uniform distribution over Sd, which is the product of the uniform over the unit sphere and the uniform over the unit interval. The center-outward distribution and quantile functions are then defined as follows. Definition 5. The center-outward quantile function Q± of P ∈Pd is the a.e. unique element ∇ψ ∈∇ΨUd;P, such that ψ satisfies ψ(u) = ∞, for ∥u∥> 1 and ψ(u) = lim inf

Sd∋v→u ψ(v), for ∥u∥= 1.

Definition 6. Call F±:= ∇ϕ the center-outward distribution function, where ϕ is defined as the Legendre transform ϕ(x):= ψ∗(x):= sup u∈Sd

(⟨u, x⟩−ψ(u)), x ∈Rd.

The following propositions from (Hallin et al. 2021) summarize the main properties of these functions. Proposition 2. Let Z ∼P ∈Pd and let F± be the centeroutward distribution function of P, then

(i) F± takes values in Sd and F±#P = Ud. Thus F± is a probability-integral transformation; (ii) ∥F±(Z)∥ is uniform over [0, 1], S(Z) = F±(Z)/∥F±(Z)∥is uniform over Sd−1, and they are mutually independent; (iii) F± entirely characterizes P;

(iv) for d = 1, F± coincides with 2F −1, where F is the tradition distribution function. Definition 7. For q ∈(0, 1) we call

C(q):= Q±(qSd−1) = {z ∈Rd | ∥F±(z)∥= q} the center-outward quantile counter, and

C(q):= Q±(qSd) = {z ∈Rd | ∥F±(z)∥≤q} the center-outward quantile region of order q. Furthermore,

C(0):=

\

0<q<1 C(q) = ∂ψ(0).

Proposition 3. Let P ∈Pd have center-outward quantile function Q±, then

(i) Q±#Ud = P, and hence Q± entirely characterizes

P; (ii) the center-outward quantile region C(q), for 0 < q <

1, has P-probability content q;

## 3.2 Empirical Estimation

We now examine how to construct empirical counterparts to F± and Q± using samples.

Denote by Z(n):= (Z1,..., Zn) an n-tuple of i.i.d. random vectors from distribution P ∈P, with density f and center-outward distribution function F±. For the empirical center-outward distribution function bF± (Hallin et al. 2021) propose the following construction.

Assume that d ≥2, and factorize n = nRnS + n0 with nR, nS, n0 ∈N and 0 ≤n0 < min{nR, nS}, such that nR →∞and nS →∞as n →∞. Next, we define a sequence of regular grids over the unit ball Sd as the intersection between

• a regular nS-tuple S(ns):= (u1,..., unS) of unit vectors, and • nR hyperspheres centered at 0, with radii n

1 nR+1,..., nR nR+1 o

, along with n0 copies of the origin. The discrete distribution with probability masses 1/n at each of the nRnS grid points and probability mass n0/n at the origin converges weakly to the uniform Ud over the ball Sd. We refer to this grid as the augmented grid.

Definition 8. The empirical center-outward distribution function is any mapping bF±: (Z1,..., Zn) 7→ bF±(Z1),..., bF±(Zn)

satisfying n X i=1

∥Zi −bF±(Zi)∥2 = min π n X i=1

∥Zπ(i) −bF±(Zi)∥2, (3)

where the set {bF±(Zi) | i = 1,..., n} consists of the n points of the augmented grid and π ranges over the n! permutations of {1, 2,..., n}.

The assignment problem in Equation (3) can be solved by, for example, the Hungarian algorithm in O(n3).

Along with the definition of the empirical center-outward distribution function bF±, we define the following concepts:

• center-outward ranks bRi:= (nR + 1)∥bF±(Zi)∥;

• empirical center-outward quantile contours bC(j nR+1):=

{Zi | bRi = j} and regions bC(j nR+1):= {Zi | bRi ≤ j}, where j/(nR + 1), j ∈{0,..., nR}, are empirical probability contents, to be interpreted as a quantile order;

• center-outward signs: bSi:= 1{bF±(Zi)̸=0}

bF±(Zi) ∥bF±(Zi)∥, and sign curves {Zi | bSi = u}, for u ∈S(nS).

In Figure 1, samples from a bi-variate distribution along with selected quantile contours and signs in the sample space R2 (left) and in the unit ball S2 (right) are shown, along with the mappings F± and Q±.

Center-Outward Dominance Relation We now introduce our main contribution: center-outward qdominance, a dominance relation between two distributions

26040

<!-- Page 5 -->

F±

Q±

**Figure 1.** Samples of a bi-variate distribution (left) and the points on the augmented grid (right). Selected centeroutward quantile contours are shown in blue and signs in red.

using their center-outward distribution and quantile functions.

Let P1, P2 ∈Pd be two probability distributions with center-outward distribution and quantile functions F±

1, Q± 1 and F±

2, Q± 2.

Definition 9 (q-dominance). For q ∈[0, 1) we say that P1 dominates P2 at quantile q, writing P1 ⪰q P2, if for every y ∈CP2(q) we have that x:= Q±

1

F±

2 (y)

≥y. (4)

When F±

2 (y) = 0 (meaning y ∈CP2(0)), we interpret Q±

1 (0) ≥y as “every x ∈CP1(0) satisfies x ≥y.”

## 4.1 Theoretical Properties Definition 9 yields three immediate consequences, which we collect below as

Corollary 1, and is connected to strong FSD, as we will show in Theorem 5.

Corollary 1. If P1 dominates P2 for a quantile q ∈[0, 1); P1 ⪰q P2, then:

(i) For any q′ ≤q we also have that P1 ⪰q′ P2, since

CPi(q′) ⊆CPi(q). (ii) For any non-decreasing utility u: Rd →R,

E[u(X) | X ∈CP1(q)] ≥E[u(Y) | Y ∈CP2(q)].

If u is bounded from above and below by constants M and m respectively, then

E[u(X)] −E[u(Y)] ≥∆q −(1 −q)(M −m), where ∆q:=

R

∥v∥≤q u(Q±

1 (v)) −u(Q± 2 (v)) dv ≥0.

(iii) There exists a coupling (bX, bY) with marginals P1, P2 such that

P(bX ≥bY) ≥q.

The bound is attained by the monotone coupling bX = Q±

1 (Z) and bY = Q± 2 (Z), with Z ∼Ud.

Theorem 5. If P1 ⪰q P2 for all q ∈[0, 1) then P1 strongly (and thus also weakly) stochastically dominates P2, i.e. P1 ⪰P2.

Proof. By Corollary 1(iii), the map Z 7→

Q±

1 (Z), Q± 2 (Z)

provides a coupling with P(X ≥Y) = 1, since P1 ⪰q P2 for all q ∈[0, 1), and Theorem 2 then yields P1 ⪰1 P2.

Thus, q-dominance can be seen as a natural relaxation of strong FSD, where we obtain strong FSD when q-dominance holds for all quantiles.

## 4.2 Empirical Test

To transform the theory into a finite-sample decision rule, we discretize (4) on the augmented grid defined in Section 3.2. Let X(n) = (X1,..., Xn) and Y(n) = (Y1,..., Yn) be n i.i.d. samples from P1 and P2 respectively, with empirical center-outward distribution and quantile functions bF±

1, bQ± 1 and bF±

2, bQ± 2.

Definition 10. For q ∈ n

0, 1 nR+1,..., nR nR+1 o

, we have that

X(n) ⪰q Y(n) if bQ±

1 (q′u) ≥bQ± 2 (q′u), for all q′ ∈ n

0, 1 nR+1,..., ⌊q(nR+1)⌋ nR+1 o and all u ∈S(nS).

When n0 ≥2 the terms bQ±

1 (0) and bQ± 2 (0) are multi-valued, in this case we interpret the defining inequality as “for every x ∈bQ±

1 (0) and y ∈bQ± 2 (0), we have that x ≥y.” In the following theorem, we prove that, once the sample size is large enough, theoretical q-dominance of the distributions P1 ⪰q P2 carries over to the empirical maps with high probability. Theorem 6. Let distributions P1 and P2 have centeroutward quantile functions Q±

1, Q± 2 that are bi-Lipschitz continuous with constants L1 and L2. Choose nR = nθ and nS = n1−θ, with θ ∈

1

2d, d+1 2d for d ≤4 and θ ∈ d−2 d2, 2d−3 d2 for d ≥5. If we assume that P1 ⪰q P2 for every q ∈[0, 1), then for every confidence level 0 < δ < 1 there exists an explicit threshold n∗(δ) such that for all n ≥n∗(δ)

X(n) ⪰q Y(n), for every q ∈ j nR + 1 nR j=0

, with probability at least 1 −δ.

A complete proof, including an explicit formula for n∗(δ), is provided in Appendix A.

Lastly, we provide a straightforward procedure, outlined in Appendix B (Algorithm 1), that ranks a collection of empirical distributions by iteratively applying center-outward q-dominance on a shared augmented grid. We first build non-dominated fronts for successively smaller q values, and then, within each front, order the remaining distributions by a measure of how close they are to being dominated.

## Experiments

To demonstrate the usefulness of q-dominance, we conduct two numerical studies: (1) to help improve the robust ranking of optimizers in multi-objective hyperparameter optimization tasks; (2) to assist the selection in multi-objective evolutionary algorithms (MOEAs) under noise.

26041

<!-- Page 6 -->

0.25 0.50 0.75 1.00

2

4

Mean Rank q-dominance

0.25 0.50 0.75 1.00

HVI

Fraction of Budget Used

Random Random x4

ParEGO SMS-EGO

EHVI MEGO

MIES

(a) Mean-rank trajectories (±1 s.d.).

1 2 3 4 5 7

MIES MEGO ParEGO SMS-EGO Random x4

EHVI Random

CD q-dominance ranks

1 2 3 4 5 7

ParEGO

MEGO Random x4

MIES SMS-EGO

EHVI Random

CD

HVI ranks

(b) Critical difference diagrams for mean ranks after 100% of budget used.

**Figure 2.** Results of YAHPO-MO benchmarks based on qdominance (left) and HVI (right).

## 5.1 Multi-Objective Hyperparameter Optimization (HPO) Rankings

Pfisterer et al. compare seven optimizers: Random Search, Random Search 4x (Random Search with quadrupled budget), ParEGO (Knowles 2006), SMS-EGO (Ponweiser et al. 2008), EHVI (Emmerich, Giannakoglou, and Naujoks 2006), MEGO (Jeong and Obayashi 2005), and MIES (Li et al. 2013) on 25 different multi-objective hyperparameter optimization problem instances with 2 to 4 objectives. They compare these optimizers by computing the normalized Hypervolume Indicator (HVI) of their found Pareto fronts after specific fractions of their budget have been used. For our approach, we sample k ≤5 points uniformly at random from the same Pareto fronts at each replication, resulting in 30k samples from the optimizer’s underlying stochastic Pareto set for each problem instance and at each considered fractional budget. With these samples, we then rank the optimizers using our q-dominance relation, by computing their empirical center-outward quantile maps and sorting them using Algorithm 1. We repeat this procedure 100 times to minimize the influence of the random sampling. More complete experimental details can be found in Appendix C.1.

In Figure 2a, we show the mean rank, based on qdominance (left) and HVI (right), of the different HPO methods as a function of the fraction of budget used. Figure 2b shows the critical difference plot, with α = 0.05, after 100% of the budget has been used.

The first difference we note is the spread of the mean

0.00 0.02 Val Accuracy

0.00

0.01

0.02

0.03

Val Cross Entropy

0.00 0.05 0.10 HVI

0

2

4

8

Count

MIES ParEGO

**Figure 3.** Left: pooled samples from the final stochastic Pareto sets for MIES and ParEGO on lcbench 167152 (marker size ∝quantile−1). Right: histogram of the HVI values for those same Pareto sets.

ranks between the optimizers after around 50% of the budget has been used. In Figure 2a (left), we see that the mean ranks, based on q-dominance, of all the methods aside from Random Search are bunched quite close together, and in Figure 2b (left), we see that none of these methods significantly outperform the others. Whilst for the mean ranks based on HVI, we have a much larger spread on the right side of Figure 2a and in Figure 2b.

Furthermore, in Figure 2b we see that, based on the qdominance ranking, only EHVI does not significantly improve on Random Search after the entire budget has been used. Contrastingly, based on the HVI ranking, in addition to EHVI, SMS-EGO and MIES also do not significantly improve on Random Search—–a notable difference, specifically for MIES, which on average performs the best according to q-dominance.

To further investigate this difference in rankings, we examine the final Pareto sets of MIES and ParEGO, the optimizers that, on average, perform best based on q-dominance and HVI, respectively, on the problem instance lcbench 167152 (See Table 1 in Appendix C.1). On this problem, MIES is preferred over ParEGO based on q-dominance, with a rank of 1.97 ± 0.26 for MIES versus 3.11 ± 0.60 for ParEGO, yet ParEGO is preferred over MIES based on HVI, where ParEGO has an HVI of 0.0399 ± 0.0025 and MIES has an HVI of 0.0400 ± 0.0045 across the 30 replications. In Figure 3, we show samples from the final Pareto sets of MIES (blue circles) and ParEGO (orange squares) in the left plot, and a histogram of the HVI values of both optimizers over the 30 replications in the right plot. From these figures, we can infer that MIES has a high probability of achieving better results than ParEGO, shown by the blue, circular points of MIES in the bottom left of the left plot in Figure 3 and the left-most bars in the right plot. However, this comes at the cost of slightly higher risk, which we can see from the points of MIES in the upper middle part of the left plot in Figure 3 and the right-most bars in the histogram on the right. By taking the expected value of the HVI, we lose this information, resulting in the HVI ranking favoring ParEGO over MIES, as ParEGO’s mean HVI value is slightly lower.

26042

<!-- Page 7 -->

0.00 0.25 0.50 0.75 1.00

1

2

3

## 4 ZDT1

0.00 0.25 0.50 0.75 1.00

2

## 4 ZDT2

0.00 0.25 0.50 0.75 1.00

1

2

3

## 4 ZDT3

0.00 0.25 0.50 0.75 1.00

200

400

ZDT4

0.00 0.25 0.50 0.75 1.00

5

6

ZDT6 q-dominance NSGA-II mean NSGA-II single

Fraction of Evaluation Budget Used

∆HV

**Figure 4.** The difference in HV (∆HV) between the deterministic Pareto front and the expected HV of the solutions at a specific budget used. ZDT5 is excluded as it is a Boolean optimization problem.

## 5.2 Noise Augmented ZDT

To assess the value of q-dominance when directly applied to SMOOPs, we augment the commonly used ZDT benchmark problems (Zitzler, Deb, and Thiele 2000) with noise in the inputs. Specifically, if f is the objective function, then we consider the optimization problem: minx f(z1,..., zk), where zi ∼N[ai,bi](xi, σ2). Here ai, bi indicate the lowerand upper-bound of the decision variable xi, such that xi ∈ [ai, bi], and N[ai,bi](xi, σ2) denotes the truncated normal distribution, with mean xi, variance σ2, and truncated to lie within the interval [ai, bi]. With this construction, our objective functions become stochastic, and the underlying deterministic functions are never evaluated outside of their domains.

We consider two simple baselines: NSGA-II with meanvalue based selection (denoted by NSGA-II mean), i.e., for each candidate solution we evaluate the objective function n times and compute the mean, and NSGA-II with single sample based selection (NSGA-II single), where we only evaluate the objective function once (Deb et al. 2002). For our method, we replace the selection with the q-dominance sorting procedure (Algorithm 1), computed on n objective function evaluations per candidate solution. All three methods have identical evaluation budgets and population sizes.

We perform 20 independent runs. Each method has a population size of 20 and proceeds for a total of 200 generations, or 200n for NSGA-II single. Our q-dominance method and the NSGA-II-mean method use n = 64 samples per candidate, where we let nR = nS = 8 for the center- outward empirical quantile maps. Lastly, for the noise, we take σ = 0.1. This choice was based on a visual inspection of the stochastic objective functions, with varied σ, evaluated at the deterministic optima. Further details, along with the plots used to determine σ, can be found in Appendix C.2.

In Figure 4 we show the difference in HV between the deterministic Pareto front and the expected HV, including the 95% confidence interval, of the approximated fronts obtained by the different methods. Plots showing the q ≈0.55 center-outward quantile regions of the final Pareto sets are shown in Appendix C.2.

We observe that for all problems, except ZDT4, the qdominance method converges significantly faster than the two baselines. For ZDT4, we note that none of the solutions are close to the deterministic front in terms of the second objective, f2, as can be seen in Figure 2 in Appendix C.2. Based on the initial inspection of the stochastic objective functions, we suspect that this is due to the sensitivity of ZDT4 to noise.

## 6 Conclusion

In this paper, we presented center-outward q-dominance, a sample-computable proxy for strong FSD, applicable to stochastic multi-objective optimization problems. Our main theoretical result establishes that q-dominance over the full range of quantiles is sufficient for strong FSD:

P1 ⪰q P2, ∀q ∈[0, 1) =⇒P1 ⪰1 P2 (strong FSD).

Because each distribution is mapped once to the common uniform reference on the unit ball, the method provides globally coherent comparisons, scales to many distributions with only one optimal transport map needing to be computed per distribution, and is free of tunable hyperparameters. The same computation yields the entire hierarchy of relaxations, for different quantiles q, at no extra cost, enabling a fast sorting procedure for stochastic multi-objective optimization, and our finite-sample analysis supplies an explicit sample size threshold n∗(δ) for any desired Type I error.

Our two empirical studies illustrated these properties by demonstrating the potential to enable stable rankings when traditional methods fail, and by providing faster convergence when directly applied to optimization problems. We emphasize that these results are intended to illustrate and validate our theoretical findings, rather than to establish new stateof-the-art performance. Accordingly, we compare only with a small set of widely used stochastic baselines. A thorough benchmarking comparison of q-dominance against a broader range of modern techniques is beyond the scope of this paper and is left for future work.

Furthermore, we plan to compare our construction theoretically to a recent work (Rioux et al. 2025), which is based on the (non-quadratic) optimal transport (OT) between two multivariate distributions, while our method uses the quadratic OT from each distribution to a common reference on the unit ball. In our method, the composition of the OTs Q±

1 ◦F± 2 is unnecessarily an OT between two distributions. Although both works imply the first-order stochastic dominance, it is unclear whether our q-dominance implies their construction, vice versa, or if they are incompatible.

26043

<!-- Page 8 -->

## Acknowledgements

This research is supported by the HyTROS project, funded out of the Dutch Growth Fund Program GroenvermogenNL (Green capacity for the Dutch economy and society) via the NWO call “NGF: Transport en opslag van waterstof Groenvermogen NL - Werkpakket 2”. This funding is further complemented with in-kind and cash funding from several of the HyTROS participants.

## References

Abdelaziz, F. 2012. Solution approaches for the multiobjective stochastic programming. European Journal of Operational Research, 216: 1–16. Caballero, R.; Cerd´a, E.; del Mar Mu˜noz, M.; and Rey, L. 2004. Stochastic approach versus multiobjective approach for obtaining efficient solutions in stochastic multiobjective programming problems. European Journal of Operational Research, 158(3): 633–648. Daulton, S.; Cakmak, S.; Balandat, M.; Osborne, M. A.; Zhou, E.; and Bakshy, E. 2022. Robust Multi-Objective Bayesian Optimization Under Input Noise. In Chaudhuri, K.; Jegelka, S.; Song, L.; Szepesv´ari, C.; Niu, G.; and Sabato, S., eds., International Conference on Machine Learning, ICML 2022, 17-23 July 2022, Baltimore, Maryland, USA, volume 162 of Proceedings of Machine Learning Research, 4831–4866. PMLR. Deb, K.; Pratap, A.; Agarwal, S.; and Meyarivan, T. 2002. A fast and elitist multiobjective genetic algorithm: NSGA- II. IEEE Transactions on Evolutionary Computation, 6(2): 182–197. Drugan, M. M.; and Now´e, A. 2013. Designing multiobjective multi-armed bandits algorithms: A study. In The 2013 International Joint Conference on Neural Networks, IJCNN 2013, Dallas, TX, USA, August 4-9, 2013, 1–8. IEEE. Ehrgott, M.; Ide, J.; and Sch¨obel, A. 2014. Minmax robustness for multi-objective optimization problems. European Journal of Operational Research, 239(1): 17–31. Emmerich, M.; Giannakoglou, K.; and Naujoks, B. 2006. Single- and multiobjective evolutionary optimization assisted by Gaussian random field metamodels. IEEE Transactions on Evolutionary Computation, 10(4): 421–439. Fliege, J.; and Xu, H. 2011. Stochastic Multiobjective Optimization: Sample Average Approximation and Applications. Journal of Optimization Theory and Applications, 151(1): 135–162. Hallin, M. 2017. On Distribution and Quantile Functions, Ranks and Signs in R d. Working Papers ECARES ECARES 2017-34, ULB – Universite Libre de Bruxelles. Hallin, M.; del Barrio, E.; Cuesta-Albertos, J.; and Matr´an, C. 2021. Distribution and quantile functions, ranks and signs in dimension d: A measure transportation approach. The Annals of Statistics, 49(2): 1139 – 1165. Jeong, S.; and Obayashi, S. 2005. Efficient global optimization (EGO) for multi-objective problem and data mining. In 2005 IEEE Congress on Evolutionary Computation, volume 3, 2138–2145 Vol. 3.

Jin, Y.; and Branke, J. 2005. Evolutionary optimization in uncertain environments-a survey. IEEE Transactions on Evolutionary Computation, 9(3): 303–317.

Knowles, J. 2006. ParEGO: a hybrid algorithm with online landscape approximation for expensive multiobjective optimization problems. IEEE Transactions on Evolutionary Computation, 10(1): 50–66.

Kopa, M.; and Petrov´a, B. 2018. Strong and Weak Multivariate First-Order Stochastic Dominance. Mathematics eJournal.

Li, R.; Emmerich, M. T.; Eggermont, J.; B¨ack, T.; Sch¨utz, M.; Dijkstra, J.; and Reiber, J. 2013. Mixed Integer Evolution Strategies for Parameter Optimization. Evolutionary Computation, 21(1): 29–64.

Lu, S.; Wang, G.; Hu, Y.; and Zhang, L. 2019. Multi- Objective Generalized Linear Bandits. In Kraus, S., ed., Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, Macao, China, August 10-16, 2019, 3080–3086. ijcai.org.

McCann, R. J. 1995. Existence and uniqueness of monotone measure-preserving maps. Duke Mathematical Journal, 80(2): 309 – 323.

Pfisterer, F.; Schneider, L.; Moosbauer, J.; Binder, M.; and Bischl, B. 2022. YAHPO Gym - An Efficient Multi- Objective Multi-Fidelity Benchmark for Hyperparameter Optimization. In Guyon, I.; Lindauer, M.; van der Schaar, M.; Hutter, F.; and Garnett, R., eds., Proceedings of the First International Conference on Automated Machine Learning, volume 188 of Proceedings of Machine Learning Research, 3/1–39. PMLR.

Ponweiser, W.; Wagner, T.; Biermann, D.; and Vincze, M. 2008. Multiobjective Optimization on a Limited Budget of Evaluations Using Model-Assisted S-Metric Selection. In Rudolph, G.; Jansen, T.; Beume, N.; Lucas, S.; and Poloni, C., eds., Parallel Problem Solving from Nature – PPSN X, 784–794. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-540-87700-4.

Rioux, G.; Nitsure, A.; Rigotti, M.; Greenewald, K.; and Mroueh, Y. 2025. Multivariate stochastic dominance via optimal transport and applications to models benchmarking. In Proceedings of the 38th International Conference on Neural Information Processing Systems, NIPS ’24. Red Hook, NY, USA: Curran Associates Inc. ISBN 9798331314385.

Shaked, M.; and Shanthikumar, J. G., eds. 2007. Multivariate Stochastic Orders, 265–322. New York, NY: Springer New York. ISBN 978-0-387-34675-5.

Sriboonchita, S.; Wong, W.-K.; Dhompongsa, S.; and Nguyen, H. T. 2009. Stochastic Dominance and Applications to Finance, Risk and Economics. Chapman and Hall/CRC. ISBN 9781420082678.

Teich, J. 2001. Pareto-Front Exploration with Uncertain Objectives. In Zitzler, E.; Thiele, L.; Deb, K.; Coello Coello, C. A.; and Corne, D., eds., Evolutionary Multi-Criterion Optimization, 314–328. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-540-44719-1.

26044

<!-- Page 9 -->

Trappler, V.; Helbert, C.; and Riche, R. L. 2025. Multiobjective Optimization under Uncertainties using Conditional Pareto Fronts. arXiv preprint arXiv:2504.04944. Xu, M.; and Klabjan, D. 2023. Pareto Regret Analyses in Multi-objective Multi-armed Bandit. In Krause, A.; Brunskill, E.; Cho, K.; Engelhardt, B.; Sabato, S.; and Scarlett, J., eds., International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA, volume 202 of Proceedings of Machine Learning Research, 38499– 38517. PMLR. Zitzler, E.; Deb, K.; and Thiele, L. 2000. Comparison of Multiobjective Evolutionary Algorithms: Empirical Results. Evolutionary Computation, 8(2): 173–195.

26045
