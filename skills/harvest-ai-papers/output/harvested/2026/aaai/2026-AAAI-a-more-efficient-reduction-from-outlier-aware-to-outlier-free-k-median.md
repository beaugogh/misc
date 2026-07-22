---
title: "A More Efficient Reduction from Outlier-Aware to Outlier-Free k-Median"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40090
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40090/44051
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# A More Efficient Reduction from Outlier-Aware to Outlier-Free k-Median

<!-- Page 1 -->

A More Efﬁcient Reduction from Outlier-Aware to Outlier-Free k-Median

Zhen Zhang1,2, Han Peng1,2∗, Limei Liu1,2, Junyu Huang3, Xiaolong Li1,2*, Qilong Feng3

1School of Advanced Interdisciplinary Studies, Hunan University of Technology and Business, China 2Xiangjiang Laboratory, China 3School of Computer Science and Engineering, Central South University, China {zz, Han.Peng, seagullm, lxl}@hutb.edu.cn, junyuhuangcsu@foxmail.com, csufeng@mail.csu.edu.cn

## Abstract

Given a non-negative integer ℓ, the k-median with outliers problem extends the standard k-median problem by allowing the removal of up to ℓpoints and minimizing the clustering cost over the remaining ones. Algorithmic development in this setting remains an active area of research due to its relevance in processing noisy data. In this paper, we present a sampling-based reduction from the k-median with outliers problem to its outlier-free counterpart. The reduction incurs a multiplicative overhead of (kℓ−1 + ε−1)O(ℓ)

in the running time: it yields (kℓ−1 + ε−1)O(ℓ) outlier-free instances, a solution to one of which can be directly transformed into a solution to the original instance with an arbitrarily small loss in the approximation ratio. This improves upon the previously known reduction with an overhead of ((k + ℓ)ε−1)O(ℓ). As applications, we obtain faster ﬁxedparameter tractable (FPT) algorithms with tight approximation guarantees for the k-median with outliers problem under various metric spaces. Furthermore, our approach naturally generalizes to constrained variants of the problem where additional constraints are imposed on the cluster sizes, and yields similar improvements in their FPT approximations.

## Introduction

Center-based clustering problems are ubiquitous in various ﬁelds involving data analysis and processing. Given a set of points in a metric space and a positive integer k, the goal of these problems is to identify at most k centers and assign each point to its nearest center so as to minimize a speci- ﬁed objective function that quantiﬁes the clustering quality. Among such problems, the k-median (k-MED) problem is one of the most widely studied, which minimizes the sum of distances between points and their corresponding centers. Solving the k-MED problem facilitates the identiﬁcation of underlying data distributions and the extraction of representative prototypes. As a result, algorithms for this problem have been extensively investigated and have become fundamental tools in a wide range of applications; see, e.g., (Cohen-Addad et al. 2019, 2023; Gowda et al. 2023).

Despite its popularity, the k-MED problem is inherently sensitive to noise, as a small number of outliers located far

*Corresponding author Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

from the bulk of the data can substantially affect the value of its objective function. Allowing the removal of such outliers can often enhance the robustness of the clustering process. Motivated by this, there has been considerable interest in the k-MED with outliers (k-MEDOUT) problem. Given a non-negative integer ℓ, this problem is designed to discard at most ℓpoints (regarded as outliers) and minimize the clustering cost of the remaining points. The problem can be formally deﬁned as follows.

Deﬁnition 1 (k-MEDOUT) An instance ((X, d), P, F, ℓ, k) of the k-MEDOUT problem is speciﬁed by a metric d over a set X of points, a subset P ⊆X consisting of the points to be clustered, a subset F ⊆X consisting of permissible locations for centers, and integers ℓ∈[0, |P|] and k ∈[1, |F|]. A feasible solution (O, C) to the instance is deﬁned by a subset O ⊆P of no more than ℓoutliers and a subset C ⊆F of no more than k centers. The cost of the solution is P p∈P\O minc∈C d(p, c). The objective is to ﬁnd a feasible solution that minimizes this cost.

Solving the k-MEDOUT problem enables a more justiﬁable identiﬁcation of outliers, as it is guided by the underlying cluster structure. This, in turn, leads to the formation of more cohesive clusters. Due to its effectiveness in handling noisy data, the problem has attracted considerable attention from both theoretical and practical perspectives. In particular, the development of its approximation algorithms remains a highly active line of research. The current bestknown polynomial-time approximation guarantee for the k- MEDOUT problem is the iterative rounding-based ratio of 6.994 + ε (Gupta, Moseley, and Zhou 2021). There has also been work on developing bi-criteria approximation algorithms for the problem, which permit limited violations of the upper bound on the number of centers or outliers in exchange for real-world applicability (Huang, Liu, and Ding 2024) or better approximation guarantees (Charikar et al. 2001; Friggstad et al. 2019; Cohen-Addad, Feldmann, and Saulpic 2021; Wu et al. 2024).

A frequently adopted approach to simplifying the k- MEDOUT problem is to restrict attention to instances where the maximum numbers of centers and outliers (i.e., k and ℓ) are signiﬁcantly smaller than the input size. In this context, ﬁxed-parameter tractable (FPT) approximation algorithms, parameterized by k and ℓ, become viable. Such al-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

28591

<!-- Page 2 -->

Approx. Time Tech. Ref.

O(1) (k + ℓ)O(k+ℓ)n log n Coreset construction (Feldman and Schulman 2012) 3 + ε

(k + ℓ)ε−1 O(k) n Sampling (Goyal, Jaiswal, and Kumar 2020; Chen et al. 2023) 1 + 2e−1 + ε (k + ℓ)O(ℓ)kO(k)ε−O(k+ℓ)nO(1) Reduction to k-MED (Agrawal et al. 2023; Jaiswal and Kumar 2023) 1 + 2e−1 + ε kO(k)ε−O(k+ℓ)nO(1) Reduction to k-MED This work

**Table 1.** FPT approximation algorithms for the k-MEDOUT problem.

gorithms run in time f(k, ℓ, ε)nO(1), where f() is an arbitrary computable function, n denotes the number of input points, and ε is an arbitrary constant in (0, 1). By leveraging the small values of ℓand k, FPT approximation algorithms that achieve much better approximation ratios than polynomial-time algorithms have been developed (Feldman and Schulman 2012; Goyal, Jaiswal, and Kumar 2020; Chen et al. 2023; Agrawal et al. 2023; Jaiswal and Kumar 2023), as summarized in Table 1.

The best-known FPT approximation algorithm for the k- MEDOUT problem, given in (Agrawal et al. 2023; Jaiswal and Kumar 2023), is obtained by reducing the problem to its outlier-free counterpart (namely, the standard k-MED problem) with an arbitrarily small loss in approximation guarantees. Speciﬁcally, Agrawal et al. (2023) performed such an approximation-preserving reduction by constructing ((k+ℓ)ε−1)O(ℓ)nO(1) outlier-free instances, and showed that an α-approximation solution to one of them implies an α(1 + ε)-approximation solution to the original instance. Consequently, the reduction in (Agrawal et al. 2023) incurs multiplicative overheads of ((k +ℓ)ε−1)O(ℓ)nO(1) and 1+ε in the running time and approximation ratio of the considered outlier-free algorithm, respectively. The overhead in the running time was later improved to ((k + ℓ)ε−1)O(ℓ) by Jaiswal and Kumar (2023). When combined with existing FPT approximation algorithm for the k-MED problem (Cohen-Addad et al. 2019), these reductions yield a (1 + 2e−1 + ε)-approximation for the k-MEDOUT problem, matching the known lower bound on the approximation ratios achievable by FPT algorithms for the problem (Cohen- Addad et al. 2019).

Our Results

When parameterized by k and ℓ, the reduction from the max k-coverage problem presented in (Cohen-Addad et al. 2019) implies that, under the gap-exponential time hypothesis (Chalermsook et al. 2020), no FPT algorithm can achieve an approximation ratio better than 1 + 2e−1 for the k- MEDOUT problem, even in the case where ℓ= 0. This hardness result suggests that further improving the approximation ratios of FPT algorithms for the k-MEDOUT problem is unlikely. Nevertheless, reducing the running time required to achieve such tight approximations, for example by optimizing the parameter-dependent term f(k, ℓ, ε), remains an open possibility. This motivates our work, in which we improve the approximation-preserving reductions given in (Agrawal et al. 2023; Jaiswal and Kumar 2023) to develop a faster tight FPT approximation algorithm.

Our main technical contribution is a sampling-based method for identifying a set of points close to the outliers in an optimal solution, which serve as anchor points for locating the outliers. Leveraging these anchor points, we identify and remove the outliers, and thereby reduce the k-MEDOUT problem to its outlier-free counterpart with a multiplicative overhead of (kℓ−1 + ε−1)O(ℓ) in the running time, as given in Table 2 and Theorem 1.

Theorem 1 Given an instance I = ((X, d), P, F, ℓ, k) of the k-MEDOUT problem satisfying |P ∪F| = n and ℓ> 0, an α-approximation algorithm for the k-MED problem that runs in time T(n −ℓ, k) on instances with n −ℓpoints and at most k centers, and a constant ε ∈(0, 1), there exists an α(1 + ε)-approximation algorithm for I with running time τ · T(n −ℓ, k) + τ(kℓε−1)O(1) + O(n(k + ℓε−1)), where τ = (kℓ−1 + ε−1)O(ℓ).

Theorem 1 suggests that any FPT or polynomial-time approximation algorithm for the k-MED problem can be transformed into an FPT approximation algorithm with a nearly identical approximation ratio for the k-MEDOUT problem. In particular, by combining Theorem 1 with the (1+2e−1 + ε)-approximation algorithm for the k-MED problem running in (kε−1)O(k)nO(1) time given in (Cohen-Addad et al. 2019), and incorporating a simple symbolic analysis of the overhead introduced by our reduction, we obtain a tight FPT approximation algorithm for the k-MEDOUT problem, which runs in kO(k)ε−O(k+ℓ)nO(1) time. As shown in Table 1 and Corollary 1, this algorithm improves upon the previously known results with the same approximation guatantees given in (Agrawal et al. 2023; Jaiswal and Kumar 2023), saving a factor of (k + ℓ)O(ℓ) in the running time.

Corollary 1 Given an instance I = ((X, d), P, F, ℓ, k) of the k-MEDOUT problem satisfying |P ∪F| = n and a constant ε ∈(0, 1), there exists a (1+2e−1 +ε)-approximation algorithm for I with running time kO(k)ε−O(k+ℓ)nO(1).

In addition to its applicability to general metric spaces, our reduction, in line with previously known reductions (Agrawal et al. 2023; Jaiswal and Kumar 2023), can also be combined with approximation algorithms for the k-MED problem under specialized metrics, including the (1 + ε)-approximation algorithms under metrics with constant doubling dimensions (Cohen-Addad, Feldmann, and Saulpic 2021), Euclidean metrics (Huang, Li, and Wu 2024), bounded-treewidth metrics (Cohen-Addad, Saulpic, and Schwiegelshohn 2021), and minor-free metrics (Cohen- Addad, Saulpic, and Schwiegelshohn 2021), as well as

28592

<!-- Page 3 -->

Overhead Ref.

O(nℓ) Folklore (brute force)

(k + ℓ)ε−1 O(ℓ) nO(1) (Agrawal et al. 2023)

(k + ℓ)ε−1 O(ℓ) (Jaiswal and Kumar 2023) (kℓ−1 + ε−1)O(ℓ) This work

**Table 2.** Multiplicative overheads in the running time incurred by reductions to the k-MED problem.

the 1.999-approximation algorithm under the Ulam metric (Chakraborty, Das, and Krauthgamer 2023). As in the general setting, the resulting algorithms preserve the approximation guarantees of their outlier-free counterparts and, due to the efﬁciency of our reduction, are notably faster than those derived from previously known reductions (Agrawal et al. 2023; Jaiswal and Kumar 2023).

Our approach accommodates arbitrary selections of outliers and therefore applies to instances where additional constraints preclude straightforwardly designating the farthest points from the centers as outliers. We show that this approach can be easily extended to yield approximationpreserving reductions for constrained generalizations of the k-MEDOUT problem, in which additional constraints are imposed on the size of each cluster. Notably, similar reductions for these constrained variants have also been proposed in (Jaiswal and Kumar 2023; Dabas, Gupta, and Inamdar 2025). However, as in the unconstrained setting, our reductions are more efﬁcient, yielding algorithms that save a factor of (k + ℓ)O(ℓ) in the running time.

Comparison with Earlier Work

The added complexity of identifying outliers makes the k- MEDOUT problem more challenging than its outlier-free counterpart, which motivates research on reducing the former to the latter. A natural approach is to enumerate all subsets of size ℓfrom the input, treat each as a candidate set of outliers, and solve the outlier-free clustering problem on the remaining points. This entails solving O(nℓ) outlierfree instances and thus incurs a multiplicative overhead of O(nℓ) in the running time. Ideas for improving upon this brute-force approach have been proposed, as summarized in Table 2. Agrawal et al. (2023) constructed the reduction for k-MEDOUT based on a solution to an outlier-free instance with k + ℓcenters. They deﬁned a set of concentric rings around each center, and sampled ((k + ℓ)ε−1 log n)2 points within the rings. These points form a coreset that closely approximates the set of points to be clustered, ensuring that the multiplicative overhead in the running time, incurred by enumerating all subsets of size ℓfor outlier identiﬁcation, is bounded by ((k + ℓ)ε−1)O(ℓ)nO(1). In a similar vein, Jaiswal and Kumar (2023) sampled ε−O(1)ℓO(1) points with probabilities weighted according to their distance to the nearest of the k + ℓcenters derived from the outlierfree instance, and showed that a near-optimal set of outliers can be found by enumerating subsets of a set comprising the sampled points and the neighboring points of the cen- ters. This implies an approximation-preserving reduction for the k-MEDOUT problem with a multiplicative overhead of ((k + ℓ)ε−1)O(ℓ) in the running time.

In this paper, we aim to further improve the efﬁciency of approximation-preserving reduction for the k-MEDOUT problem. We obtain O(k + ℓ) centers by solving an outlierfree instance (as in (Agrawal et al. 2023; Jaiswal and Kumar 2023)) and use them to initialize D-sampling. Speciﬁcally, the algorithm iteratively selects points with probability proportional to their distance to the nearest point among the centers and previously sampled points. While sharing algorithmic similarities with the reductions in (Agrawal et al. 2023; Jaiswal and Kumar 2023) (which also sample points based on a (k + ℓ)-center solution), our approach no longer relies on sampling to identify candidate outliers. Instead, it samples to ﬁnd anchor points, namely, points sufﬁciently close to the outliers in an optimal solution that can serve as anchors to locate them. This idea enables us to further reduce the required sampling size to linear in ℓ. Guided by these anchor points, we give an approximation-preserving reduction for the k-MEDOUT problem that incurs a multiplicative overhead of (kℓ−1 + ε−1)O(ℓ) in the running time, which is signiﬁcantly smaller than the overheads of the previous reductions (Agrawal et al. 2023; Jaiswal and Kumar 2023). As a result, our reduction yields a faster FPT approximation algorithm with a tight approximation guarantee, as previously pointed out.

## Preliminaries

We consider a metric space (X, d) with distance function d. Given a point a ∈X and a subset B ⊆X, let d(a, B) = minb∈B d(a, b) denote the distance from a to its nearest point in B. Given a positive integer k and two subsets B1, B2 ⊆X with min{|B1|, |B2|} ≥k, let optk(B1, B2) = minC⊆B2 ∧|C|=k

P b∈B1 d(b, C) denote the minimum k-clustering cost of B1 using centers selected from B2. Given a positive integer i, deﬁne [i] = {1, · · ·, i}.

The following result, known as Chernoff bound, provides an upper bound on the probability that the sum of independent binary random variables deviates signiﬁcantly below its expectation. Lemma 1 (Chernoff (1952)) Given two real numbers p, λ ∈(0, 1) and t independent binary random variables v1,..., vt with Pr[vi = 1] = p for each i ∈[t], we have Pr[Pt i=1 vi < (1 −λ)pt] < e−λ2pt/2.

The k-MEDOUT problem reduces to the k-MED problem when ℓ= 0. In this outlier-free setting, we can construct constant-factor bi-criteria approximation solutions in linear time, as described in the following lemma. Lemma 2 (Chen (2009); Wei (2016)) Given an instance ((X, d), P, F, 0, k) of the k-MEDOUT problem, a bicriteria approximation solution (∅, C) with |C| = O(k) and P p∈P d(p, C) = O(optk(P, F)) can be found in O(|P ∪ F| · k) time.

Given a set of anchor points for locating the outliers, the goal is to select, for each anchor point, a prescribed number of nearby points as outliers in the approximation solution,

28593

<!-- Page 4 -->

## Algorithm

1: Identifying anchor points via sampling Input: A real number ϵ ∈(0, 1) and an instance I = ((X, d), P, F, ℓ, k) of the k-MEDOUT problem with ℓ> 0. Output: A subset A ⊆P ∪F

1: Construct a bi-criteria approximation solution (∅, A) to instance ((X, d), P, F ∪P, 0, k + ℓ) using Lemma 2, and let β be the ratio of its cost to the optimum. 2: for i ←1 to ⌈2ℓβϵ−1⌉do 3: Sample a point p ∈P with probability proportional to d(p, A). 4: A ←A ∪{p} 5: return A.

while ensuring that no point is selected more than once. This selection task is modeled via the unit-supply transportation problem, which is deﬁned as follows. Deﬁnition 2 (Unit-Supply Transportation) An instance (S, D, µ, d) of the unit-supply transportation problem is speciﬁed by a set S of supply points, a set D of demand points, a demand function µ: D →Z≥0, and a distance function d: S × D →R≥0. A feasible solution to the instance is a transportation mapping φ: S →D satisfying |φ−1(a)| = µ(a) for each a ∈D. The cost of the solution is P b∈S d(b, φ(b)). The objective is to ﬁnd a feasible solution of minimum cost.

It is well known that the unit-supply transportation problem can be solved in polynomial time, based on the total unimodularity of the constraint matrix in its linear programming formulation. Lemma 3 (Schrijver (1998)) An instance (S, D, µ, d) of the unit-supply transportation problem can be exactly solved in (|S| · |D|)O(1) time.

The Algorithm for Identifying Anchor Points In this section we describe how to identify the anchor points used to locate the outliers, as outlined in Algorithm 1. The algorithm takes as input a real number ϵ ∈(0, 1) and an instance I = ((X, d), P, F, ℓ, k) of the k-MEDOUT problem, where ℓ> 0. It constructs a set A by combining the centers obtained from a β-approximation solution to the outlier-free instance ((X, d), P, F ∪P, 0, k + ℓ) with ⌈2ℓβϵ−1⌉additional points sampled from P. This section establishes that A contains the desired anchor points lying sufﬁciently close to the outliers.

Intuitively, Lemma 2 provides an upper bound on the total distance from all points in P, including the outliers, to their nearest centers in the solution to the outlier-free instance ((X, d), P, F∪P, 0, k+ℓ). Accordingly, Algorithm 1 includes these centers as anchor points. However, this bound alone is insufﬁcient to support an approximation-preserving reduction with an arbitrarily small loss in the approximation ratio. To remedy this, the algorithm additionally samples ⌈2ℓβϵ−1⌉anchor points from P, where each is selected with probability proportional to its distance from the current set of anchor points. This ensures that the outliers not well covered by the initial O(k + ℓ) centers are likely to be close to at least one of the anchor points. These insights lead to the proof of the following lemma, where we consider O as the set of outliers.

Lemma 4 Given a subset O ⊆P with |O| ≤ℓ, inequality P o∈O d(o, A) ≤ϵ · optk(P\O, F) holds with probability at least 1 −e−1/4.

Proof We prove the lemma by showing that points near the outliers not well covered by the set of centers obtained in step 1 of Algorithm 1 can be sampled in step 3 with high probability. Let A0 denote this center set. For each i ∈[⌈2ℓβϵ−1⌉], let Ai be the union of A0 and the points sampled in the ﬁrst i iterations of the algorithm. The approximation ratio of the solution (∅, A0) to the outlier-free instance considered in step 1 suggests that its cost is close to optk(P\O, F), as stated in the following claim.

Claim 1 P p∈P d(p, A0) ≤β · optk(P\O, F).

We break the analysis into the following two cases:

(1) There exists an integer i ∈[0, ⌈2ℓβϵ−1⌉−1] satisfying

X o∈O d(o, Ai) ≤ϵ β

X p∈P d(p, Ai);

(2) For each integer i ∈[0, ⌈2ℓβϵ−1⌉−1], it holds that

X o∈O d(o, Ai) > ϵ β

X p∈P d(p, Ai).

For case (1), let i be the smallest integer that satisﬁes the condition. We have

X o∈O d(o, A) ≤

X o∈O d(o, Ai)

≤ϵ β

X p∈P d(p, Ai)

≤ϵ β

X p∈P d(p, A0)

≤ϵ · optk(P\O, F), where the ﬁrst and third steps follow from the fact that A0 ⊆ Ai ⊆A, and the last step is due to Claim 1. This completes the proof of Lemma 4 for case (1).

We now focus on case (2), where the outliers in O\Ai remain far from the points in Ai for each i ∈[0, ⌈2ℓβϵ−1⌉− 1]. In each such iteration, Algorithm 1 samples a point p ∈ P with probability proportional to d(p, Ai), and adds it to Ai to form Ai+1. This suggests that inequality |Ai ∩O| < |Ai+1 ∩O| holds with probability

P o∈O\Ai d(o, Ai) P p∈P d(p, Ai) =

P o∈O d(o, Ai) P p∈P d(p, Ai) > ϵ β. (1)

We consider ⌈2ℓβϵ−1⌉independent binary random variables v0,..., v⌈2ℓβϵ−1⌉−1 with Pr[vi = 1] = ϵβ−1 for each i ∈ [0, ⌈2ℓβϵ−1⌉−1]. It can be shown that

Pr[|A ∩O| < |O|] ≤Pr[|A ∩O| −|A0 ∩O| < ℓ]

28594

<!-- Page 5 -->

## Algorithm

2: The algorithm for the k-MEDOUT problem Input: A real number ϵ ∈ (0, 1), an instance I = ((X, d), P, F, ℓ, k) of the k-MEDOUT problem with ℓ> 0, and an algorithm Clustering applicable only when ℓ= 0 Output: A solution (O†, C†) to I

1: Let A be the set returned by Algorithm 1 with (ϵ, I) as input. 2: Let S ⊆P be the union of the ℓnearest neighbors (self included) in P of each point in A. 3: Let v be a virtual point with d(v, p) = 0 for each p ∈S. 4: H ←∅. 5: for each function µ: A ∪{v} →Z≥0 that satisﬁes P a∈A µ(a) = ℓand µ(v) = |S| −ℓdo 6: Solve the instance (S, A ∪{v}, µ, d) of the unitsupply transportation problem using Lemma 3, and let φ: S →A ∪{v} be the solution. 7: O ←S a∈A φ−1(a). 8: Use Clustering to construct a solution (∅, C) to instance ((X, d), P\O, F, 0, k). 9: H ←H ∪{(O, C)}.

10: return (O†, C†) ←arg min (O,C)∈H

P p∈P\O d(p, C).

< Pr





⌈2ℓβϵ−1⌉−1 X i=0 vi < ℓ





<e−1/4, where the ﬁrst step is due to the fact that |O| ≤ℓ, the second step follows from the fact that

Pr[|Ai ∩O| < |Ai+1 ∩O|] > ϵβ−1 = Pr[vi = 1]

for each i ∈[0, ⌈2ℓβϵ−1⌉−1] (due to inequality (1)), and the third step follows from Lemma 1 (with λ = 1/2). Therefore, with probability at least 1 −e−1/4, we have |A ∩O| = |O|, which implies that O ⊆A and hence P o∈O d(o, A) = 0. This establishes the validity of Lemma 4 for case (2). □

The Anchor Points-Based Algorithm for the k-MEDOUT Problem

In this section we solve the k-MEDOUT problem based on the anchor points. Our approach is presented in Algorithm 2 and illustrated in Figure 1, which considers a real number ϵ ∈(0, 1), an instance I = ((X, d), P, F, ℓ, k) with |P ∪F| = n and ℓ> 0, and an algorithm Clustering applicable only to the case where ℓ= 0. The algorithm constructs a set A of anchor points using Algorithm 1, and forms the candidate set S ⊆P of outliers as the union of the ℓnearest neighbors of each anchor point. To identify a subset of this candidate set that is close to an optimal set of outliers, the algorithm iterates over all |A|-tuples (µ1, · · ·, µ|A|) of non-negative integers satisfying P|A| i=1 µi = ℓ, which correspond to guesses of the number of outliers captured by each anchor point. For each such tuple, it maps the corresponding number of candidate outliers to each anchor v

A S

(b) (a)

**Figure 1.** (a): The ℓnearest neighbors of each anchor point in A (anchor points are shown in black) are collected into the set S of candidates for outliers; (b): An instance of the unitsupply transportation problem is constructed on a bipartite graph formed by the points in A ∪S ∪{v}, and is solved to select outliers from S.

point by solving an instance of the unit-supply transportation problem. Speciﬁcally, it introduces a demand point v with µ(v) = |S| −ℓand d(v, p) = 0 for each p ∈S in the instance, and considers the candidates in S not mapped to v in the corresponding solution as outliers. Given the identiﬁed outliers, the algorithm removes them from P and executes algorithm Clustering on the remaining points to obtain the k centers. Based on these iterations, Algorithm 2 constructs a candidate set H of solutions and ﬁnally returns the solution (O†, C†) ∈H that minimizes the cost for I.

The following lemma ensures that Algorithm 2 can capture a subset of ℓpoints close to the outliers, regardless of how the outliers are distributed.

Lemma 5 Given a subset O ⊆P with |O| = ℓ, the following event occurs with probability at least 1 −e−1/4: There exists a solution (O′, C′) ∈H such that a bijection γ: O\O′ →O′\O satisfying P o∈O\O′ d(o, γ(o)) ≤ 2ϵ · optk(P\O, F) can be constructed.

Proof For each anchor point a ∈A, let O(a) = {o ∈ O: arg mina′∈A d(a′, o) = a} denote the subset of outliers in O captured by a. Let (O′, C′) be the solution added to H in the iteration where each value |O(a)| is correctly guessed (namely µ(a) = |O(a)| for each a ∈A) and the instance I′ = (S, A ∪{v}, µ, d) of the unit-supply transportation problem is constructed with the desired setting of the demand function. Let φ: S →A∪{v} denote the corresponding solution to I′. By constructing a bijection between O(a) and φ−1(a) for each a ∈A, we can obtain a tight bijection between O and O′ with high probability, as stated in the following claim.

Claim 2 With probability at least 1 −e−1/4, there exists a bijection ˜γ: O →O′ with P o∈O d(o, ˜γ(o)) ≤2ϵ · optk(P\O, F).

We map each o ∈O \ O′ to O′ \ O by iteratively applying the bijection ˜γ stated in Claim 2 until the image lies in O′ \ O. We deﬁne a sequence (˜γ0(o), ˜γ1(o), ˜γ2(o), · · ·) where ˜γ0(o) = o and ˜γi(o) = ˜γ(˜γi−1(o)) for each i ≥1. Given that |O \ O′| = |O′ \ O| and ˜γ: O →O′ is a bijection, this process is guaranteed to terminate at some index t

28595

<!-- Page 6 -->

satisfying ˜γt(o) ∈O′ \O. We then deﬁne γ(o) = ˜γt(o), and denote this index by t(o) = t. It can be shown that

X o∈O\O′ d(o, γ(o)) ≤

X o∈O\O′ t(o) X i=1 d(˜γi−1(o), d(˜γi(o))

≤

X o∈O d(o, ˜γ(o))

≤2ϵ · optk(P\O, F), where the ﬁrst step follows from triangle inequality, the second step follows from the bijectivity of ˜γ, and the third step is due to Claim (2). Consequently, γ is a bijection from O\O′ to O′\O satisfying the statement of Lemma 5. □

We now analyze Algorithm 2 to show the correctness of Theorem 1. Proof (of Theorem 1) We prove the theorem by showing that Algorithm 2 returns the desired approximation solution within the claimed time bound. We ﬁrst analyze the approximation guarantee of the algorithm. Let (O∗, C∗) be an optimal solution to I, let opt = P p∈P\O∗d(p, C∗) denote the cost of (O∗, C∗), let α denote the approximation ratio of the outlier-free algorithm Clustering, and let (O′, C′) ∈H be a solution to I satisfying the statement of Lemma 5 with respect to O∗, where γ: O∗\O′ →O′\O∗ is the corresponding bijection. For each p ∈P, let c(p) be the center in C∗nearest to p. The approximation guarantee of Clustering suggests that

X p∈P\O′ d(p, C′)

≤α · optk(P\O′, F)

≤α ·

X p∈P\O′ d(p, C∗)

=α



 X p∈(P\O′)\O∗ d(p, C∗) +

X o∈O∗\O′ d(o, C∗)





≤α



 X p∈(P\O′)\O∗ d(p, C∗) +

X o∈O∗\O′ d(o, c(γ(o)))



.

(2)

Observe that X o∈O∗\O′ d(o, c(γ(o)))

≤

X o∈O∗\O′ d(o, γ(o)) +

X o∈O∗\O′ d(γ(o), C∗)

≤2ϵ · optk(P\O∗, F) +

X o∈O′\O∗ d(o, C∗)

= 2ϵ · opt +

X o∈O′\O∗ d(o, C∗), (3)

where the ﬁrst step follows from triangle inequality, and the second step follows from Lemma 5 and the fact that γ is a bijection from O∗\O′ to O′\O∗. Combining inequality (2) with inequality (3), we get

X p∈P\O′ d(p, C′)

≤α



 X p∈(P\O′)\O∗ d(p, C∗) +

X o∈O′\O∗ d(o, C∗) + 2ϵ · opt





=α



 X p∈P\O∗ d(p, C∗) + 2ϵ · opt





=α(1 + 2ϵ)opt.

This inequality implies that the approximation ratio of Algorithm 2 is α(1 + 2ϵ).

We now analyze the running time of Algorithm 2. Let T(n −ℓ, k) denote the running time of algorithm Clustering on instances with n −ℓpoints and at most k centers. The set A of anchor points consists of O(k + ℓ) centers and O(ℓϵ−1) points sampled from P. The set S of candidates for outliers is formed by collecting the ℓnearest neighbors of each anchor point. Consequently, we have |A| = O(k + ℓϵ−1) and |S| ≤O(kℓ+ ℓ2ϵ−1). Identifying the anchor points and candidates for outliers involves solving an instance of the (k + ℓ)-median problem using the linear-time algorithm in Lemma 2, and computing the distances from the anchor points to all points in P (used for determining the sampling probabilities in Algorithm 1 and ﬁnding the neighbors of the anchor points), which takes O(n(k + ℓϵ−1)) time. Let τ denote the number of iterations of steps 6–9 in Algorithm 2. In each iteration, the algorithm solves an instance of the unit-supply transportation problem based on Lemma 3 and an instance of the k-MED problem using Clustering, which takes T(n −ℓ, k) + (|A| · |S|)O(1) ≤T(n −ℓ, k) + (kℓϵ−1)O(1) time. Putting everything together, the running time of Algorithm 2 is τ ·T(n−ℓ, k)+τ(kℓϵ−1)O(1) +O(n(k +ℓϵ−1)).

It remains to analyze the value of τ, which is the number of |A|-tuples (µ1, · · ·, µ|A|) of non-negative integers satisfying P|A| i=1 µ1 = ℓ. We have τ =

|A| + ℓ−1 ℓ

< (|A| + ℓ−1)ℓ ℓ!

< e(|A| + ℓ−1)

ℓ ℓ

= (kℓ−1 + ϵ−1)O(ℓ), where we use the counting technique of stars and bars in the ﬁrst step, the third step follows from the lower bound of Stirling’s approximation, and the last step follows from the fact that |A| = O(k + ℓϵ−1).

Letting ε = ϵ/2, the discussion above implies the correctness of Theorem 1. □

28596

<!-- Page 7 -->

Extensions Under Cluster Size Constraints In real-world applications involving clustering, it is often necessary to impose constraints on cluster sizes. For example, lower bounds can be used to ensure that the clustering results satisfy the k-anonymity principle (Arutyunova and Schmidt 2021), and upper bounds can help prevent load imbalance among cluster centers. In this section, we consider the generalization of the k-MEDOUT problem incorporating such cluster size constraints, which is referred to as the sizeconstrained k-MEDOUT (SC-k-MEDOUT) problem and de- ﬁned as follows. Deﬁnition 3 (SC-k-MEDOUT) An instance ((X, d), P, F, ℓ, k) of the k-MEDOUT problem can be extended to its sizeconstrained variant ((X, d), P, F, ℓ, k, µ1, µ2) by incorporating two mappings µ1, µ2: F →Z≥0, where µ1(c) ≤ µ2(c) for each c ∈F. A feasible solution (O, C, ϕ) to the variant is speciﬁed by a subset O ⊆P of no more than ℓ outliers, a subset C ⊆F of no more than k centers, and a mapping ϕ: P\O →C with |ϕ−1(c)| ∈[µ1(c), µ2(c)] for all c ∈C. The cost of the solution is P p∈P\O d(p, ϕ(p)), and the objective is to ﬁnd a feasible solution minimizing this cost.

A key distinction between the size-constrained and unconstrained k-MEDOUT problems lies in the structural properties of their respective optimal solutions. In the unconstrained setting, each point is assigned to its nearest center in an optimal solution, and the set of outliers consists of the ℓpoints farthest from their respective nearest centers. In contrast, for the SC-k-MEDOUT problem, constructing solutions solely based on point-to-center distances may violate feasibility, and the optimal solutions no longer exhibit the aforementioned structural regularities. Encouragingly, our approach to identifying a near-optimal set of outliers makes no assumptions on the spatial distribution of outliers in optimal solutions, which allows the outliers to be arbitrary points, as established in Lemma 5. This enables us to effortlessly extend our approach from the unconstrained case to the size-constrained setting. Indeed, our algorithm for the SC-k-MEDOUT problem retains the overall structure of Algorithm 2, except that the set H of candidate solutions is constructed using a subroutine applicable to the sizeconstrained setting, and the ﬁnal solution is selected based on its cost under the cluster size constraints. Analyzing the performance of this variant of Algorithm 2 yields the following theorem. Theorem 2 Given an instance I = ((X, d), P, F, ℓ, k, µ1, µ2) of the SC-k-MEDOUT problem satisfying |P ∪ F| = n and ℓ> 0, an α-approximation algorithm for the outlier-free counterpart of the problem that runs in time T(n −ℓ, k) on instances with n −ℓpoints and at most k centers, and a constant ε ∈(0, 1), there exists an α(1 + ε)-approximation algorithm for I with running time τ · T(n −ℓ, k) + τ(kℓε−1)O(1) + O(n(k + ℓε−1)), where τ = (kℓ−1 + ε−1)O(ℓ).

Notably, the applicability of Theorem 2 hinges on the availability of a suitable approximation algorithm for solving the outlier-free counterpart of the considered instance. In the general case where each center is associated with both non-uniform lower and upper bounds, no efﬁcient approximation algorithms are currently known. However, several special cases of the problem have been studied, for which ﬁxed-parameter approximation algorithms (with parameter k) are known. These special cases include

(i) the capacitated k-MED problem, where each center is associated only with an upper bound on the cluster size (Adamczyk et al. 2019; Cohen-Addad and Li 2019; Goyal, Jaiswal, and Kumar 2020; Bandyapadhyay, Fomin, and Simonov 2024), (ii) the lower-bounded k-MED problem, where each cen- ter is associated only with a lower bound (Goyal, Jaiswal, and Kumar 2020; Bandyapadhyay, Fomin, and Simonov 2024), (iii) and the balanced k-MED problem, where all centers are associated with uniform upper and lower bounds (Ding 2020; Kong, Zhang, and Feng 2023). In each of these cases, Theorem 2 can be combined with an existing outlier-free algorithm to yield an approximation algorithm for the respective special case of the SC-k- MEDOUT problem.

Conclusions In this paper, we study the k-MEDOUT problem under the setting where the maximum numbers of outliers and centers are treated as ﬁxed parameters. By locating the outliers in an optimal solution based on a carefully chosen set of anchor points, we reduce the k-MEDOUT problem to its outlierfree counterpart. This reduction leads to a faster FPT algorithm with a tight approximation guarantee. Moreover, our approach is applicable to variants of the problem that impose additional constraints on the cluster sizes, and yields similar improvements in the FPT approximation results.

Given the known lower bound on the approximation ratios achievable by FPT algorithms for the k-MEDOUT problem (Cohen-Addad et al. 2019), further improvement from the perspective of approximation guarantees for the problem is unlikely. Nevertheless, it remains an open question whether comparable approximation guarantees can be attained through more efﬁcient algorithms. Notably, the existing inapproximability result (Cohen-Addad et al. 2019) is established in the outlier-free case, and thus does not preclude the possibility of achieving comparable approximation guarantees for the k-MEDOUT problem using FPT algorithms parameterized solely by k. This suggests a promising direction for future research in the design of more efﬁcient parameterized algorithms. Moreover, the reduction presented in this paper, along with the reductions in (Agrawal et al. 2023; Jaiswal and Kumar 2023), relies on randomized procedures and therefore introduces randomness into the resulting algorithms. Understanding whether deterministic constructions can achieve similar guarantees forms another natural direction to explore. Finally, it is worth investigating whether the anchor point-based techniques developed in this work can be extended to obtain analogous improvements under other clustering objectives, such as k-means and k-center.

28597

<!-- Page 8 -->

## Acknowledgments

This work was supported by National Natural Science Foundation of China (62202161), Open Project of Xiangjiang Laboratory (23XJ01001), National Natural Science Foundation of China (62432016, 62502545), Science and Technology Innovation Program of Hunan Province (2025RC3207), Scientiﬁc Research Fund of Hunan Provincial Education Department (23B0592), Innovation Fund of QiYuan Lab (2022-JCJQ-LA-001-088), and Key Research and Development Program of Hunan Province (2024JK2007).

## References

Adamczyk, M.; Byrka, J.; Marcinkowski, J.; Meesum, S. M.; and Wlodarczyk, M. 2019. Constant-factor FPT approximation for capacitated k-median. In Proceedings of the 27th Annual European Symposium on Algorithms (ESA), volume 144, 1:1–1:14. Agrawal, A.; Inamdar, T.; Saurabh, S.; and Xue, J. 2023. Clustering what matters: Optimal approximation for clustering with outliers. In Proceeding of the 37th AAAI Conference on Artiﬁcial Intelligence (AAAI), 6666–6674. Arutyunova, A.; and Schmidt, M. 2021. Achieving anonymity via weak lower bound constraints for k-median and k-means. In Proceedings of the 38th International Symposium on Theoretical Aspects of Computer Science (STACS), volume 187, 7:1–7:17. Bandyapadhyay, S.; Fomin, F. V.; and Simonov, K. 2024. On coresets for fair clustering in metric and Euclidean spaces and their applications. Journal of Computer and System Sciences, 142: 103506. Chakraborty, D.; Das, D.; and Krauthgamer, R. 2023. Clustering permutations: New techniques with streaming applications. In Proceedings of the 14th Innovations in Theoretical Computer Science Conference (ITCS), volume 251, 31:1–31:24. Chalermsook, P.; Cygan, M.; Kortsarz, G.; Laekhanukit, B.; Manurangsi, P.; Nanongkai, D.; and Trevisan, L. 2020. From gap-exponential time hypothesis to ﬁxed parameter tractable inapproximability: Clique, dominating set, and more. SIAM Journal on Computing, 49(4): 772–810. Charikar, M.; Khuller, S.; Mount, D. M.; and Narasimhan, G. 2001. Algorithms for facility location problems with outliers. In Proceedings of the 12th Annual Symposium on Discrete Algorithms (SODA), 642–651. Chen, K. 2009. On coresets for k-median and k-means clustering in metric and Euclidean spaces and their applications. SIAM Journal on Computing, 39(3): 923–947. Chen, X.; Han, L.; Xu, D.; Xu, Y.; and Zhang, Y. 2023. k-median/means with outliers revisited: A simple FPT Approximation. In Proceedings of the 29th International Conference on Computing and Combinatorics (COCOON), volume 14423, 295–302. Chernoff, H. 1952. A measure of asymptotic efﬁciency for tests of a hypothesis based on the sum of observations. Annals of Mathematical Statistics, 23(4): 493–507.

Cohen-Addad, V.; Feldmann, A. E.; and Saulpic, D. 2021. Near-linear time approximation schemes for clustering in doubling metrics. Journal of the ACM, 68(6): 44:1–44:34. Cohen-Addad, V.; Grandoni, F.; Lee, E.; and Schwiegelshohn, C. 2023. Breaching the 2 LMP approximation barrier for facility location with applications to k-median. In Proceedings of the 34th ACM-SIAM Symposium on Discrete Algorithms (SODA), 940–986. Cohen-Addad, V.; Gupta, A.; Kumar, A.; Lee, E.; and Li, J. 2019. Tight FPT approximations for k-median and kmeans. In Proceedings of the 46th International Colloquium on Automata, Languages, and Programming (ICALP), volume 132, 42:1–42:14. Cohen-Addad, V.; and Li, J. 2019. On the ﬁxed-parameter tractability of capacitated clustering. In Proceedings of the 46th International Colloquium on Automata, Languages, and Programming (ICALP), volume 132, 41:1–41:14. Cohen-Addad, V.; Saulpic, D.; and Schwiegelshohn, C. 2021. A new coreset framework for clustering. In Proceedings of the 53rd Annual ACM SIGACT Symposium on Theory of Computing (STOC), 169–182. Dabas, R.; Gupta, N.; and Inamdar, T. 2025. FPT approximation for capacitated clustering with outliers. Theoretical Computer Science, 1027: 115026. Ding, H. 2020. Faster balanced clusterings in high dimension. Theoretical Computer Science, 842: 28–40. Feldman, D.; and Schulman, L. J. 2012. Data reduction for weighted and outlier-resistant clustering. In Proceedings of the 23rd Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1343–1354. Friggstad, Z.; Khodamoradi, K.; Rezapour, M.; and Salavatipour, M. R. 2019. Approximation schemes for clustering with outliers. ACM Transactions on Algorithms, 15(2): 26:1–26:26. Gowda, K. N.; Pensyl, T. W.; Srinivasan, A.; and Trinh, K. 2023. Improved bi-point rounding algorithms and a golden barrier for k-median. In Proceedings of the 34th ACM-SIAM Symposium on Discrete Algorithms (SODA), 987–1011. Goyal, D.; Jaiswal, R.; and Kumar, A. 2020. FPT approximation for constrained metric k-median/means. In Proceedings of the 15th International Symposium on Parameterized and Exact Computation (IPEC), volume 180, 14:1–14:19. Gupta, A.; Moseley, B.; and Zhou, R. 2021. Structural iterative rounding for generalized k-median problems. In Proceedings of the 48th International Colloquium on Automata, Languages, and Programming (ICALP), volume 198, 77:1– 77:18. Huang, J.; Liu, W.; and Ding, H. 2024. Bi-criteria sublinear time algorithms for clustering with outliers in high dimensions. In Proceedings of the 30th International Conference on Computing and Combinatorics (COCOON), volume 15161, 91–103. Huang, L.; Li, J.; and Wu, X. 2024. On optimal coreset construction for Euclidean (k, z)-clustering. In Proceedings of the 56th Annual ACM Symposium on Theory of Computing (STOC), 1594–1604.

28598

<!-- Page 9 -->

Jaiswal, R.; and Kumar, A. 2023. Clustering what matters in constrained settings: Improved outlier to outlier-free reductions. In Proceeding of the 34th International Symposium on Algorithms and Computation (ISAAC), volume 283, 41:1–41:16. Kong, X.; Zhang, Z.; and Feng, Q. 2023. On parameterized approximation algorithms for balanced clustering. Journal of Combinatorial Optimization, 45(1): 49. Schrijver, A. 1998. Theory of linear and integer programming. Chichester, England: John Wiley & Sons. Wei, D. 2016. A constant-factor bi-criteria approximation guarantee for k-means++. In Proceedings of the 29th Annual Conference on Neural Information Processing Systems (NeurIPS), 604–612. Wu, C.; M¨ohring, R. H.; Wang, Y.; Xu, D.; and Zhang, D. 2024. Approximation algorithms for robust clustering problems using local search techniques. In Proceedings of the 18th Annual Conference on Theory and Applications of Models of Computation (TAMC), volume 14637, 197–208.

28599
