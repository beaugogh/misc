---
title: "Linear Time Algorithms for Individually Fair k-means via Multi-Swap Local Search"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39202
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39202/43163
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Linear Time Algorithms for Individually Fair k-means via Multi-Swap Local Search

<!-- Page 1 -->

Linear Time Algorithms for Individually Fair k-means via Multi-Swap Local

Search

Beirong Cui, Qilong Feng*, Junyu Huang

School of Computer Sciencd and Engineering, Central South University, Changsha 410083, China

## Abstract

Fair clustering has attracted increased attention in recent years. In this work, we study the individually fair clustering problem in Euclidean space. While single-swap local search methods have achieved near-linear running time and constant approximation guarantees, their performance often depends on the aspect ratio of the dataset (the ratio between the diameter and the minimum interpoint distance of the dataset). How to apply multi-swap local search while obtaining linear running time with better approximation ratio is still a challenging task. To address this, we introduce a collaborative initialization framework for that integrates greedy with sampling techniques. This framework eliminates the dependence on the aspect ratio and produces a constant-factor bicriteria approximation in linear time. In contrast to the current state-of-the-art near-linear time algorithm, which requires a restrictive assumption about the relationship between optimal centers and cluster centroids, we propose a multi-swap local search algorithm that provides an improved approximation guarantee. Our method runs in linear time with high probability and does not rely on the aforementioned assumption. We validate our theoretical results through extensive experiments on both real-world and synthetic datasets, including largescale benchmarks with up to 100 million points. Our empirical evaluation demonstrates superior performance in terms of clustering quality and computational efficiency, along with scalability under varying parameter settings.

## Introduction

Clustering is a fundamental problem in unsupervised learning and has been extensively studied for decades. Among various clustering objectives, k-means is one of the most widely used in practice. Given a dataset P ⊆Rd, the kmeans problem seeks to find at most k centers C ⊆Rd that minimize the sum of squared Euclidean distances from each point to its nearest center.

The standard k-means problem has been extensively studied over the past decades, leading to numerous algorithmic advances and practical solutions (Arthur and Vassilvitskii 2006; Bahmani et al. 2012; Cohen-Addad et al. 2022). A significant line of work focuses on developing constant-factor approximation algorithms with linear or near-linear runtime

*Corresponding author: csufeng@mail.csu.edu.cn Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

in the data size (Aggarwal, Deshpande, and Kannan 2009; Arthur and Vassilvitskii 2006; Beretta et al. 2023; Huang et al. 2024; Lattanzi and Sohler 2019). However, in many real-world applications optimizing clustering cost alone is insufficient. Fairness has become a key concern in how data points are assigned to clusters. For instance, in placing public facilities such as hospitals (Vakilian and Yalciner 2022), it is important to ensure that no individual is too far from their nearest facility. In such scenarios, individual fairness becomes crucial: it guarantees that every person has reasonable access to a nearby center, thereby preventing systemic inequities that may arise under standard clustering objectives. Incorporating such fairness constraints not only promotes equity but also enhances the ethical and societal reliability of algorithmic systems.

Motivated by individual fairness, (Mahabadi and Vakilian 2020) introduced the individually fair k-clustering problem. Given a dataset P of n points in a metric space, each point p ∈P is associated with a fair radius δ(p), defined as the smallest radius such that the ball of radius δ(p) centered at p contains at least n/k points from P. This definition captures the idea that every individual should have a cluster center within a distance that reflects the local density of the data. The goal of individually fair clustering is to select at most k centers such that every point is assigned to a center within its fair radius. In this setting, (Jung, Kannan, and Lutz 2020) established a fundamental hardness result: in Euclidean spaces of dimension d > 1, no algorithm can achieve a fairness approximation ratio better than

√

2, highlighting the intrinsic difficulty of satisfying fairness constraints exactly. To enable approximation algorithms, (Mahabadi and Vakilian 2020) formulated individually fair clustering as a bi-objective optimization problem, aiming to simultaneously minimize the clustering cost while satisfying individual fairness constraints. (Negahbani and Chakrabarty 2021) addressed the k-means setting with a polynomial-time (8, 4)-bicriteria approximation algorithm that combines linear programming relaxation with randomized rounding techniques. A more general framework was introduced in (Vakilian and Yalciner 2022), achieving a (16p+ε, 3)-bicriteria approximation for fair k-clustering in polynomial time, where p is a parameter determined by the clustering objective. Using a multi-swap local search strategy, (Mahabadi and Vakilian 2020) proposed a (84, 7)-bicriteria approximation algo-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

20650

<!-- Page 2 -->

rithm for the individually fair k-median problem. However, this algorithm relies on enumeration to construct swap pairs at each local search step, which results in a high polynomial runtime of O(n5k5d log(n∆)), which limits scalability for large datasets. Building on this line of work, (Bateni et al. 2024) introduced a single-swap local search algorithm (SSLS), achieving an (O(1), O(1))-bicriteria approximation in O(ndk2 log(n∆)) time. While this represents a step toward efficiency, several limitations remain:

**Figure 1.** Failure of the Centroid Assumption

(1) The number of local search iterations in SSLS (Bateni et al. 2024) depends heavily on the initial solution. Since initialization relies on the aspect ratio ∆, the runtime has a logarithmic dependence on ∆, leading to O(ndk2 log(n∆)) running time. In worst-case instances, ∆can be as large as 2no(1) (Cohen-Addad, Mirrokni, and Zhong 2022), potentially making SSLS polynomial in time and limiting scalability. Moreover, ∆may be arbitrarily large in practice (Huang et al. 2023; Nguyen, Nguyen, and Jones 2022). To the best of our knowledge, no existing algorithm for individually fair k-means achieves an O(1)-approximation in near-linear or linear time while maintaining fairness. Thus, designing efficient methods for computing high-quality initial solutions in linear time remains a key challenge.

(2) Under individual fairness constraints, a key structural as- sumption in the analysis of SSLS no longer holds. Specifically, the cost decomposition identity cost(P ∗, c) = |P ∗| · ρ2(c, c∗) + cost(P ∗, c∗) (see Section 2 for notation) for an optimal cluster P ∗, any point c, and its optimal center c∗, depends on c∗coinciding with the centroid µ(P ∗). This condition is generally violated under individual fairness. To illustrate, consider the example in Figure 1, where P = {a, b, c, d} and k = 2. Assume ∆1 ≫∆2 ≫ρ(b, c). The optimal clustering assigns a to one cluster and A = {b, c, d} to the other, with the optimal center c∗

A placed at the intersection of fairnessenforced balls rather than near µ(A). As ∆2 grows, the separation between c∗

A and µ(A) increases, breaking the centroid-based cost decomposition. This breaks a core analytical tool of SSLS, undermining its performance and limiting its applicability in fair clustering settings.

(3) The approximation guarantees of SSLS involve large hid- den constants, with at least 2000 for the clustering cost and at least 6 for the fairness violation (relying on the assumption). Multi-swap approach (Mahabadi and Vakilian 2020) has so far lacked comparable runtime performance despite their better approximation ratios. Bridging this gap by achieving both strong theoretical guarantees and linear running time remains a challenge in the development of scalable fair clustering algorithms.

To address these challenges, we propose a novel multiswap local search framework that achieves a (62, 7)bicriteria approximation in linear time.

Firstly, as shown in (Mahabadi and Vakilian 2020), the cost of a worst-case k-means solution can reach n∆2, which introduces a log(n∆) factor in the runtime. To remove this dependence, we propose a collaborative initialization framework that combines greedy selection with sampling. This approach achieves an (O(1), 4)-bicriteria approximation in linear time O(ndk +poly(k)), independent of the aspect ratio ∆. As a result, it provides stronger theoretical guarantees and significantly improves practical efficiency.

Secondly, since the cost decomposition identity does not generally hold under individual fairness constraints, we generalize it to an inequality that applies to any set P ⊆Rd and any two points c1, c2 ∈Rd: cost(P, c1) ⩽2|P|·ρ2(c1, c2)+ 2 cost(P, c2). This minor relaxation allows our algorithm to be applied in general Euclidean settings, thereby enhancing its applicability and generalization.

Finally, performing multi-swap local search under individual fairness requires a sampling-based approach, as enumeration is computationally prohibitive. However, sampling raises two challenges: how to select valid swap pairs that include points near optimal centers while satisfying fairness constraints, and how to combine multiple pairs to achieve improvements beyond single swaps. To address the first, we introduce a greedy construction of anchor points and a novel center adjustment mechanism that replaces unfair candidate centers with suitable anchors, preserving fairness while reducing cost. For the second, we design an efficient algorithm that generates a small set of candidate multi-swap pairs from the sampled points, with size independent of n. We further demonstrate that, under certain conditions, this set contains at least one valid multi-swap that improves the solution in each iteration.

Our contributions are summarized as follows:

• We propose a collaborative initialization framework for individually k-means problem that combines greedy and sampling methods, achieving an (O(1), 4)-bicriteria approximation in O(ndk + poly(k)) time.

• We propose a linear-time multi-swap local search algorithm for individually fair k-means, achieving a (62, 7)-bicriteria approximation in O(nd · poly(k)) time with constant probability. The algorithm removes a key assumption in SSLS and outperforms its (2000, 6)-bicriteria approximation, which requires O(ndk2 log(n∆)) time.

• Extensive performance tests and parameter sensitivity analyses demonstrate the effectiveness of our proposed algorithms on both real-world and synthetic datasets.

20651

![Figure extracted from page 2](2026-AAAI-linear-time-algorithms-for-individually-fair-k-means-via-multi-swap-local-search/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

## Preliminaries

In this paper, we consider a dataset P ⊆Rd of size n, where d denotes the dimensionality of the space. We let k and t denote the number of clusters and the size of swap pairs, respectively. For any two points p, q ∈Rd, we define their Euclidean distance as ρ(p, q). This definition extends to sets as follows: the distance between two sets P, Q ⊆Rd is given by ρ(P, Q):= infx∈P,y∈Q ρ(x, y). For any positive integer l, we write [l] to denote the set {1, 2, · · ·, l}. The centroid of a set P is defined as µ(P) = 1 |P |

P p∈P p. Given a set of clustering centers C ⊆Rd with |C| = k, the clustering cost is defined as cost(P, C):= P p∈P minc∈C ρ2(p, c). To formalize the notion of individual fairness in k-means clustering, we proceed by defining the fair radius and the concept of fairness violation approximation.

Definition 1 (Fair Radius). The fair radius function δ: Rd → R+ is defined as δ(a) = min r ∈R+: |B(a, r) ∩P| ⩾ n k

, where B(a, r) = {x ∈Rd: ρ(x, a) ⩽r} denotes the closed ball of radius r centered at a. We refer to δ(a) as the fair radius of point a.

Definition 2 (α-Fairness). Given a parameter α > 0, a set of centers C ⊆Rd is said to be α-fair if for every point p ∈P, ρ(p, C) ⩽α · δ(p).

According to (Jung, Kannan, and Lutz 2020), in Euclidean spaces of dimension d > 1, there exists a point set P such that for any center set C, there is at least one point p ∈P satisfying ρ(p, C) ⩾

√

2 δ(p). Moreover, determining the optimal fairness parameter α for a given point set and number of clusters k is NP-hard. This suggests that, for the individually fair k-means problem, the most viable approach is to seek a bicriteria approximation that trades off between fairness violation and clustering cost. In the following, we assume α is a predefined parameter, and we assume there exists at least one center set C ⊆Rd that is α-fair.

Definition 3 ((β, η)-Bicriteria Approximation). An algorithm is a (β, η)-bicriteria approximation for the individually fair k-means problem if, for any dataset P ⊆Rd, the solution CALG (a set of k clustering centers) satisfies the following two properties:

## 1 Cost

Approximation: cost(P, CALG) ⩽ β · cost(P, COPT), where COPT denotes the optimal center set minimizing the k-means cost; 2. Fairness Relaxation: CALG is (η · α)-fair, meaning ρ(p, CALG) ⩽η · α · δ(p) for all p ∈P.

For brevity, we define ALG = cost(P, CALG) and OPT = cost(P, COPT).

Let P∗= {P ∗

1, P ∗ 2, · · ·, P ∗ k } denote the optimal clustering partition of P, with corresponding optimal centers C∗= {c∗

1, c∗ 2, · · ·, c∗ k}. Let C = {c1, c2, · · ·, ck} be a set of centers produced by an algorithm, inducing a partition P = {P1, P2, · · ·, Pk}, where each Pi consists of all points in P assigned to center ci under the k-means clustering. To facilitate analysis, we define two mappings: M: ci 7→ Pi and M∗: c∗ i 7→P ∗ i, for i = 1, 2,..., k. We refer to these as Mc and M∗ c∗, respectively, when emphasizing the center being mapped. For subsets I ⊆C and O ⊆C∗, we denote M∗

I = S c∗∈O M∗ c∗as the union of optimal clusters corresponding to centers in O, and MI = S c∈I Mc as the union of clusters from centers in I.

The following lemma is a well-known decomposition of the k-means cost and is standard in clustering analysis:

Lemma 1. For any point set P ⊆Rd and any point c ∈Rd, cost(P, c) = |P| · ρ2(c, µ(P)) + cost(P, µ(P)).

Multi-Swap Local Search Algorithm In this section, we present a multi-swap local search algorithm for the individually fair k-means problem that achieves a (62, 7)-bicriteria approximation. A key challenge is sampling valid multi-swap pairs that reduce clustering cost while preserving individual fairness. Traditional approaches, such as D2-sampling (Lattanzi and Sohler 2019), ignore fairness and thus result in fairness violations. In multi-swap settings, interactions between center replacements and cluster reassignments grow more complex. Critically, even if individual swaps are fairness-preserving in isolation, their simultaneous execution may violate fairness for certain points. Therefore, a valid multi-swap must be carefully designed to ensure that the combined effect of all center replacements does not violate fairness constraints for any point. To address these challenges, we propose a center adjustment mechanism, which ensures that each iteration improves the clustering cost while maintaining bounded fairness violation.

The full multi-swap local search procedure is formalized in Algorithm 1, which proceeds in three stages. In the first stage (Steps 1–2), we construct an anchor set S0 using a greedy strategy (Algorithm 2) that selects centers with minimal fair radii, ensuring the initial center set C satisfies individual fairness. In the second stage (Steps 4–7), we apply D2-sampling to generate a candidate set Q0, prioritizing locations near optimal centers to achieve significant cost reductions. However, since D2-sampling depends only on distance, incorporating these points directly may violate fairness. To resolve this, the third stage (Steps 8–11, Algorithm 3) introduces a center adjustment mechanism: using S0 and Q0, it constructs a candidate set F of valid multiswap operations, which includes at least one multi-swap that simultaneously reduces clustering cost and preserves fairness. As a result, each iteration reduces the cost by a multiplicative factor of Θ(1 −1/k) with constant probability, leading to a (62, 7)-bicriteria approximation.

In classical k-means, the optimal center of a cluster P ∗ is equal to its centroid, i.e., c∗= µ(P ∗). However, under individual fairness constraints, centers may deviate from the centroid to ensure every point lies within its fair radius. This misalignment invalidates centroid-based assumption. To strengthen the theoretical foundation of our algorithm, we extend Lemma 1 using the following inequality:

Lemma 2. For any point set P ⊆Rd and any c1, c2 ∈Rd, cost(P, c1) ⩽2|P| · ρ2(c1, c2) + 2 · cost(P, c2).

This inequality supports the definition of a key construct the core, which consists of points close to a near-optimal

20652

<!-- Page 4 -->

## Algorithm

1: Individually Fair Multi-Swap Local Search (IFMSLS)

Input: A dataset P ⊆Rd, number of clusters k, rounds parameter T, swap pair size t, parameters ε, θ, α. Output: A θ-feasible center set C ⊆Rd with |C| ⩽k.

1: Initialize S0 ←GAS(P, k, α, 2). 2: Initialize centers C ←S0, then randomly select k−|S0| points from P and add to C. 3: for i = 1: T do 4: Initialize Q0 ←∅. 5: for j = 1: t do 6: Sample p ∈P with probability cost(p,C)

cost(P,C) and add p to Q0. 7: for (Q, O) ∈2Q0 × 2C s.t. |Q| = |O| ⩾1 do 8: F ←CA((Q, O), S0, θ, C). 9: for (Q′, O) ∈F do 10: if cost(P, C \ O ∪Q′) ⩽

1 −ε k

· cost(P, C) then 11: C ←C \ O ∪Q′. 12: return C.

## Algorithm

2: Greedy Anchor Selection (GAS)

Input: Dataset P ⊆Rd, number of clusters k, fairness pa- rameter α, coverage expansion factor γ. Output: Anchor set S0 ⊆P with individual fairness guar- antees. 1: Initialize anchor set: S0 ←∅ 2: Initialize covered points: Z ←∅ 3: while Z̸ = P do 4: c ←arg minp∈P \Z δ(p) 5: S0 ←S0 ∪{c} 6: Z ←Z ∪{p ∈P: ρ(p, c) ⩽γα · δ(p)} 7: return S0 center and can be efficiently sampled using D2-sampling (Step 6 in Algorithm 1). Definition 4 (Core). For a set E ⊆Rd, a point c, and β ⩾ 1, the core of E with respect to c is core(E, c, β) = E ∩

B (c, Rβ(E, c)), where Rβ(E, c) = q β · cost(E,c)

|E|.

The following lemma provides a critical sampling guarantee: if the current cost of an optimal cluster P ∗accounts for a significant fraction of the optimal cost, a large fraction of this cost is concentrated in its core. This ensures that D2sampling selects points from the core with high probability. Lemma 3. Let P ∗∈P∗be an optimal cluster with center c∗. If cost(P ∗, C) ⩾2(2 + 4ε) · cost(P ∗, c∗), then the cost of the β′-core of P ∗under C, where β′ = (1 + ε)2, satisfies cost(core(P ∗, c∗, β′), C) ∈Ω(ε3) · cost(P ∗, C∗).

To leverage the core structure effectively, we introduce a framework for constructing valid multi-swap pairs based on the relationship between the current center set C and a anchor set S0. Each a ∈S0 is an anchor point, with an associated anchor zone B(a, θα · δ(a)), where θ is a parameter

## Algorithm

3: Center Adjustment (CA)

Input: Candidate swap pair (Q, O), anchor set S0, fairness slack parameter θ, current center set C, Output: Set of θ-feasible refined swap pairs F.

1: Initialize feasible swap set: F ←∅ 2: A ←{a ∈S0: (C \ O ∪Q) ∩B(a, θα · δ(a)) = ∅} 3: for each Q′ ⊆(Q ∪A) such that |Q′| = |Q| do 4: if C \ O ∪Q′ is θ-feasible then 5: F ←F ∪{(Q′, O)} 6: return F specified in the algorithm. We say that the center set C is θfeasible with respect to S0 if, for every anchor point a ∈S0, the intersection C ∩B(a, θα · δ(a)) is non-empty. That is, each anchor zone contains at least one center from C. This condition is maintained as an invariant in our local search, guaranteeing that no anchor point is left poorly covered. The following lemma formalizes the term “anchor”, shows that feasibility with respect to S0 serves as both a necessary and sufficient condition for fairness, up to constant factors. Lemma 4. Let C be a set of k centers and S0 ⊆P be an anchor set constructed by Algorithm 2. Then: 1. If C is θ-feasible, then C is ((θ + γ) · α)-fair. 2. Conversely, if C is (θα)-fair, then C is θ-feasible. 3. Moreover, if γ ⩾2, there exists an anchor set S0 of size at most k such that the above implications hold. The lemma suggests a simple construction for γ-fair centers: when γ ⩾2, the anchor set S0 can be extended to a full set of k centers by adding k −|S0| random points from P, yielding an initial γ-fair solution. To improve clustering quality, we use D2-sampling (Step 6) to select candidate centers near optimal centers. However, directly swapping in these points may lead to severe fairness violations, as traditional nearest-point-based swap constructions fail to satisfy individual fairness constraints. To address the risk of fairness violations during center updates, we revise the standard capture relationship between optimal centers and the current solution by incorporating the anchor zone structure. This ensures that swaps preserve θ-feasibility, thereby maintaining individual fairness throughout the local search process. We begin by classifying optimal centers based on their relationship to the anchor set S0 as follows. Definition 5 (Anchor and Unconstrained Optimal Centers). A point c∗∈C∗is an anchor optimal center if it is the closest center in C∗to some point a ∈S0. In this case, we write ac∗= a and say c∗is anchored at a. The set of all such centers is denoted A∗. The remaining optimal centers, U ∗= C∗\ A∗, are called unconstrained optimal centers.

This restricted rule incorporates the relationship between centers and anchor points. We now construct the multi-swap pairs intuitively, with full formal details provided in the full version. Since optimal clusters contributing little to the current cost are unlikely to be sampled effectively via D2sampling, to avoid ineffective swaps, we focus on optimal clusters with cost at least ε · ALG/k. The candidate multiswap set H is built in two steps. First, for each current cen-

20653

<!-- Page 5 -->

ter capturing between one and t such optimal centers, we let I be those centers and O be |I| lonely centers, i.e., centers capturing none, and add (I, O) to H. Second, for each center that captures more than t optimal centers, we process each captured c∗by selecting one unused center c0 and adding the swap ({c∗}, {c0}) to H. All such pairs (I, O) form the swap set H.

To guide the selection of effective swaps from the candidate set H, we classify each (I, O) ∈H as good or bad based on its potential cost reduction.

Definition 6 (Good and Bad Swap Pairs). A multi-swap pair (I, O) ∈H is good if cost(M∗

I, C) > (4 + ε) · cost(M∗

I, C∗) + Reassign(I, O) + ε k · cost(P, C), and bad otherwise, where Reassign(I, O) = cost(MO\M∗

I, C\O)− cost(MO \ M∗

I, C).

The intuition is that a good swap targets optimal clusters I whose current cost under C is significantly higher than their optimal cost, justifying the swap. For any good swap pair (I, O), we can show that replacing O with I leads to a substantial decrease in total cost: cost(P, C \ O ∪I) <

1 −ε k

· cost(P, C) −(3 + ε) · cost(M∗ I, C∗). This ensures a cost reduction of at least a factor of 1−ε/k. The additional term (3 + ε) · cost(M∗

I, C∗) allows us to select points from the β′-core of each optimal cluster, rather than requiring exact optimal centers, which occur with zero probability under D2-sampling. This relaxation is essential for achieving a non-trivial success probability while still guaranteeing significant cost improvement. The following theorem formalizes this guarantee.

Theorem 1. Let (I, O) be a good swap pair, where I = {c∗

1, c∗ 2, · · ·, c∗ l } with l ⩽t. For any strongly improving set Q = {q1, q2, · · ·, ql}, defined by qi ∈core(M∗ c∗ i, c∗ i, β′) for i = 1, 2, · · ·, l, we have cost(P, C \ O ∪Q) ⩽

1 −ε k

· cost(P, C).

While a strongly improving set Q of candidate centers can significantly reduce clustering cost, directly replacing O with Q may violate individual fairness. To preserve fairness, we introduce a center adjustment mechanism (Algorithm 3) that transforms Q into a new set Q′ such that: |Q′| = |Q|, C \O∪Q′ is θ-feasible (and thus ((θ+γ)α)-fair by Lemma 4), and the cost reduction is preserved.

Let A ⊆S0 be the anchor points whose anchor zones become empty after removing O (Step 2 in Algorithm 3). Our goal is to construct a set Q′ ⊆Q ∪A of size |Q| that preserves θ-feasibility. The following proposition shows that, under mild conditions, candidate points from cores are compatible with anchor zones:

Proposition 1. Let θ ⩾2, and let c∗∈A∗that is anchored by ac∗. If ac∗/∈core(M∗ c∗, c∗, β′), then core(M∗ c∗, c∗, β′) ⊆B(ac∗, θα · δ(ac∗)).

Intuitively, when θ ⩾2, the core lies within the anchor zone unless the anchor itself is in the core. Thus, sampling from the core ensures the new center lies in the anchor zone, preserving θ-feasibility. If instead ac∗is in the core, we can explicitly include it in Q′ via enumeration. In both cases, the resulting swap achieves a cost reduction by a factor of at least 1 −ε/k while maintaining θ-feasibility, and hence ((θ +γ)α)-fairness by Lemma 4. A full proof and extension to multi-swap settings are given in the full version. Combining all components, we obtain the following theorem, which establishes the correctness and effectiveness of the center adjustment mechanism (Algorithm 3). Theorem 2. Let C be a θ-feasible set of centers with θ ⩾2. For every good swap pair (I, O) ∈H, there exists a set Q′ ⊆Q ∪A such that |Q′| = |O| and: 1. C \ O ∪Q′ is θ-feasible, 2. cost(P, C \ O ∪Q′) ⩽

1 −ε k

· cost(P, C). We now analyze the overall performance of Algorithm 1. The initial center set C, constructed in Step 2, may have cost as high as n∆2. However, each successful iteration reduces the cost by a factor of 1 −ε/k. By Theorem 2, this process maintains θ-feasibility throughout. With careful parameter selection and analysis, we arrive at the main result: Theorem 3. Algorithm 1 solves the individually fair kmeans problem with constant probability, producing a solution C that is: 1. a (62, 7)-bicriteria approximation, i.e., cost(P, C) ⩽ 62 · OPT and C is 7α-fair, 2. computable in O(nd · poly(k) · log(n∆)) time.

Fast Initialization Independent of Aspect Ratio In the previous section, we presented a greedy initialization algorithm that achieves a constant-factor approximation in near-linear time, O(nd · poly(k) · log(n∆)), even from an arbitrarily poor initial solution. While efficient in n and d, this runtime depends logarithmically on the aspect ratio ∆, which can be large in practice. As shown in Lemma 4, Algorithm 2 produces a γα-fair solution but provides no cost guarantee. In contrast, D2-oversampling (Aggarwal, Deshpande, and Kannan 2009) yields O(k) centers with constant expected approximation ratio, but without fairness bounds. A naive combination would result in O(k) centers, which is incompatible with the requirement of selecting exactly k centers in individually fair k-means.

To overcome the limitations of existing initialization methods, we propose a collaborative initialization framework (Algorithm 4) with three stages. First, we build a candidate set P0 of size O(k) by combining centers from (Steps 1-3): the anchor-based fair selection (Algorithm 2), ensuring γα-fairness, and D2-oversampling (Algorithm 5), providing a constant-factor cost approximation in expectation. This set P0 simultaneously satisfies the fairness constraint and captures low-cost structure. Second, we reduce P to a weighted instance (P0, ω) by assigning each point to its nearest center in P0 (Steps 4-5), which enables clustering in time independent of n and ∆. Finally, we show that P0 contains subset of size k that is both γα-fair and achieves a constant-factor cost approximation (Step 6), and that such a subset can be found in O(poly(k)) time. This yields an (O(1), 4)-bicriteria approximation, effectively balancing fairness, clustering quality, and efficiency. The following lemma, based on the analysis of D2-sampling in (Aggarwal, Deshpande, and Kannan

20654

<!-- Page 6 -->

## Algorithm

4: Collaborative Initialization Framework (CIF)

Input: A dataset P ⊆Rd, number of clusters k, parameters α, γ, a weighted algorithm B that outputs a 1-feasible solution C with O(1) clustering quality approximation. Output: An initial center set C0 with (O(1), 4)-bicriteria approximation. 1: S0 ←GAS(P, k, α, 2). 2: S1 ←DOS(P, k). 3: P0 ←S0 ∪S1. 4: Let σ(p) ∈P0 be the nearest point to p in P0. 5: For each p0 ∈P0, let ω(p0) denotes the number of points in P assigned to p0, that is, ω(p0) = |σ−1(p0)|. 6: C0 ←B(P0, ω, S0, k). 7: return C0.

## Algorithm

5: D2-Oversampling (DOS)

Input: A dataset P ⊆Rd, number of clusters k. Output: An sample set S1 of size O(k).

1: Initialize S1 ←∅. 2: Randomly select a point p from P and add it to S1. 3: for i = 1: O(k) do

4: Sample a point p ∈P with probability cost(p,S1)

cost(P,S1).

5: S1 ←S1 ∪{p}. 6: return S1.

2009), establishes that Algorithm 5 produces a candidate set S1 with a constant-factor approximation to the optimal kmeans cost, with constant probability.

Lemma 5. (Aggarwal, Deshpande, and Kannan 2009) Let S1 ⊆P be the set of O(k) points selected in Algorithm 5. Then, with probability at least 0.03, cost(P, S1) ⩽20 · OPT∞, where OPT∞denotes the optimal k-means clustering cost. Furthermore, Algorithm 5 runs in O(ndk) time.

Since the standard k-means problem is a relaxation of the individually fair variant, we have OPT∞⩽OPT. Thus, with constant probability, cost(P, P0) ⩽cost(P, S1) ⩽20 · OPT∞⩽20·OPT. After constructing the candidate set P0 with size O(k), we reduce the problem to clustering within P0 by assigning each point in P to its nearest center in P0. This instance compression enables all subsequent steps to run in time independent of n, effectively eliminating dataset size from the overall time complexity. The following lemma justifies this strategy by showing that P0 contains a subset of exactly k centers that forms a constant-factor approximation to the optimal fair clustering cost.

Lemma 6. For each c∗ i ∈ C∗, let c′ i ∈ P0 be the closest point in P0 to c∗ i, and C′ = {c′

1, · · ·, c′ k}. Then cost(P, C′) ⩽O(1) · OPT.

We now analyze the fairness of C′. Each anchor a ∈S0 defines an anchor zone B(a, θα · δ(a)), and for any optimal center c∗assigned to a, we have c∗∈B(a, α·δ(a)). Let c′ ∈ C′ be the closest point in P0 to c∗. By the triangle inequality, ρ(c′, a) ⩽ρ(c′, c∗) + ρ(c∗, a) ⩽ρ(c′, c∗) + α · δ(a) ⩽2α · δ(a), which implies c′ ∈B(a, 2α·δ(a)), so C′ is 2-feasible.

By Lemma 4, 2-feasibility implies 4α-individual fairness. Combined with Lemma 6, this yields an (O(1), 4)-bicriteria approximation. Having established the existence of such a solution within P0, the final step is to efficiently compute a k-center subset C0 ⊆P0 that is 4α-fair and achieves a constant-factor approximation on the weighted instance.

The following lemma, adapted from (Vakilian and Yalciner 2022), provides a key tool for extracting a high-quality fair solution from the candidate set. Lemma 7. (Vakilian and Yalciner 2022) Let C∗

0 be the optimal 1-feasible solution for the weighted k-means problem on P0, with cost costω(P0, C):= P p∈P0 ω(p) · ρ2(p, C), where ω(p) is the weight of p ∈P0 (assigned in Step 5 of Algorithm 4). Then there exists an algorithm that computes a 1-feasible solution C0 ⊆P0 runs in poly(k) time such that costω(P0, C0) ∈O(1) · costω(P0, C∗

0). Since C∗

0 is optimal and C′ is feasible, we have costω(P0, C0) ∈O(1) · costω(P0, C′). We now state the main theorem for the collaborative initialization framework: Theorem 4. With constant probability, Algorithm 4 computes an (O(1), 4)-bicriteria approximate solution to the individually fair k-means problem in O(ndk + poly(k)) time.

We now revisit Algorithm 1. By replacing the initial center set, which is originally constructed in Step 2 using a method that depends on log(n∆), with the output of Algorithm 4, we eliminate the dependence on the aspect ratio ∆. Since the new initialization runs in O(ndk + poly(k)) time, we obtain the following improved guarantee: Theorem 5. With constant probability, Algorithm 1, when initialized with Algorithm 4, computes a (62, 7)-bicriteria approximate solution to the individually fair k-means problem in O(nd · poly(k)) time.

## Experiment

In this section, we present empirical results of our algorithms on real-world and synthetic datasets, evaluated on a server with 72 Intel Xeon Gold 6230 CPUs and 500 GB RAM.

Datasets. We evaluate on diverse benchmark datasets used in prior work (Mahabadi and Vakilian 2020; Negahbani and Chakrabarty 2021; Bateni et al. 2024): Adult (n = 32, 561, d = 6), Bank (n = 45, 211, d = 3), Diabetes (n = 101, 766, d = 2), Gowalla (n = 100, 000, d = 2), Skin (n = 245, 054, d = 4), Shuttle (n = 58, 000, d = 9), and Covtype (n = 581, 012, d = 54). To assess scalability, we include two large-scale datasets: HIGGS (n = 107, d = 18) and Learn (n = 108, d = 128) (J´egou et al. 2011; Bateni et al. 2024). All datasets are standard normalized following (Bateni et al. 2024).

Metrics. We evaluate performance using three key metrics: the clustering cost defined as P p∈P ρ2(p, C), the maximum bound ratio which measures fairness violation as maxp∈P ρ2(p,C)

δ(p) where lower values indicate better fairness, and the running time in seconds to assess efficiency.

Baselines. We compare against: EMSLS (Mahabadi and Vakilian 2020) (enumeration-based local search), LP (Negahbani and Chakrabarty 2021) and its efficient variant

20655

<!-- Page 7 -->

Dataset Method Cost Fairness Time bank

EMSLS 3.234E+03 1.52 2428.3 LP 4.514E+03 1.18 22880.90 LPS 4.838E+03 1.16 37.69 SSLS 3.289E+03 1.61 6.83 MSLS-G 3.127E+03 1.44 1.82 MSLS-W 3.028E+03 1.53 4.18 adult

EMSLS 8.984E+03 1.26 2762.54 LP 9.973E+03 1.15 25517.47 LPS 9.782E+03 1.19 280.98 SSLS 8.629E+03 1.31 23.21 MSLS-G 8.686E+03 1.37 1.76 MSLS-W 8.620E+03 1.28 2.89 gowalla

EMSLS 7.395E+02 1.47 2128.54 LP 9.334E+02 1.17 11367.70 LPS 9.990E+02 1.15 9.78 SSLS 7.938E+02 2.33 18.20 MSLS-G 7.178E+02 1.69 1.63 MSLS-W 7.107E+02 1.87 3.60

Dataset Method Cost Fairness Time diabetes

EMSLS 1.485E+03 1.05 2013.24 LP 1.575E+03 1.29 291.99 LPS 1.471E+03 1.29 3.01 SSLS 1.733E+03 2.00 3.60 MSLS-G 1.440E+03 1.14 1.70 MSLS-W 1.423E+03 1.18 2.71 shuttle

EMSLS 1.097E+04 1.80 2720.54 LP 1.975E+04 1.14 13160.33 LPS 1.963E+04 1.12 45.66 SSLS 1.677E+04 1.95 4.89 MSLS-G 1.088E+04 1.72 1.66 MSLS-W 1.059E+04 1.98 3.20 skin

EMSLS 1.682E+03 1.60 2187.42 LP 1.808E+03 1.02 4493.82 LPS 2.060E+03 1.13 9.26 SSLS 1.695E+03 2.23 10.08 MSLS-G 1.518E+03 1.75 1.79 MSLS-W 1.516E+03 1.85 3.14

**Table 1.** Comparison on different datasets, with 5000 points sampled from each dataset

Dataset Method Cost Fairness Time

HIGGS

EMSLS - - > 24h LP - - > 24h LPS - - > 24h SSLS - - > 24h MSLS-G 3.0322E+08 1.10 3396.12 MSLS-W 2.9966E+08 1.09 3783.84

Dataset Method Cost Fairness Time

Learn

EMSLS - - > 24h LP - - > 24h LPS - - > 24h SSLS - - > 24h MSLS-G 1.2816E+10 1.00 63147.94 MSLS-W 1.2703E+10 1.01 75122.80

**Table 2.** Comparison on large scale datasets

LPS (linear programming), SSLS (Bateni et al. 2024) (single-swap local search), and two variants of our method: MSLS-G (greedy initialization, Algorithm 2) and MSLS-W (weighted instance initialization, Algorithm 4).

Experimental Setup. Following the experimental setting in (Bateni et al. 2024), we execute all algorithms on each dataset 10 times, fix the number of clusters at k = 10, and set the parameters ε, θ and γ as ε = 1/100 and θ = γ = 2. The swap pair size is set to t = 2 for better scalability. For local search algorithms (SSLS, MSLS-G, and MSLS-W), we set the number of local search iterations to T = 500. To further accelerate our algorithms, we propose a distancepreserving structure that stores distances to the t + 1 nearest centers each after center updates. This structure enables efficient computation of clustering cost after swap without requiring full dataset enumeration.

100 200 500 1000 2000 5000 Dimensionality

0

2

4

6

8

Difference (%)

Relative Cost Difference (%)

100 200 500 1000 2000 5000 Dimensionality

101

102

103

Time (log scale)

Time (Log Scale)

EMSLS SSLS MSLS-W MSLS-G

**Figure 2.** Comparison results with varying dimensions

Results. As shown in Table 1, our algorithms achieve superior performance in both clustering cost and running time. MSLS-W consistently delivers the best clustering quality across most datasets, while MSLS-G is the fastest in terms of runtime. Both MSLS-G and MSLS-W achieve fairness guarantees comparable to the best baselines, with MSLS-W offering significant improvements in efficiency. MSLS-G and MSLS-W achieving higher clustering quality and substantially reduced runtimes compare to SSLS. Notably, MSLS- G not only runs the fastest but also improves clustering cost over all baselines. On average, MSLS-W reduces clustering cost by 5.3%, 23.8%, 25.7%, and 14.0% compared to EM- SLS, LP, LPS, and SSLS, respectively. Moreover, MSLS-G is 6.5 times faster than SSLS on average.

On large-scale instances, the results in Table 2 demonstrate that MSLS-G and MSLS-W successfully complete within 24 hours on HIGGS (n = 10, 000, 000) and Learn (n = 100, 000, 000), while SSLS fails to finish within the time limit. Additionally, Figure 2 illustrates performance in high-dimensional settings from 100 to 5000 dimensions on synthetic dataset SYN (n = 5, 000). Our methods exhibit solid scalability as dimensionality increases, confirming their scalability in demanding scenarios.

## Conclusion

This paper proposes an effective collaborative initialization framework for individually fair k-means, which enables a linear-time multi-swap local search algorithm. Our approach removes a key assumption from prior work and achieves better solutions both theoretically and in practice. Extensive experiments demonstrate its effectiveness. A promising direction for future work is to design linear-time algorithms that further reduce fairness violations, bringing practical performance closer to theoretical optima.

20656

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Natural Science Foundation of China (Nos. 62432016, 62172446) and the Central South University Research Program of Advanced Interdisciplinary Studies(No.20230YJC023). This work was also carried out in part using computing resources at the High Performance Computing Center of Central South University.

## References

Aggarwal, A.; Deshpande, A.; and Kannan, R. 2009. Adaptive sampling for k-means clustering. In International Workshop on Approximation Algorithms for Combinatorial Optimization, 15–28. Springer. Arthur, D.; and Vassilvitskii, S. 2006. k-means++: The advantages of careful seeding. Technical report, Stanford. Bahmani, B.; Moseley, B.; Vattani, A.; Kumar, R.; and Vassilvitskii, S. 2012. Scalable k-means++. arXiv preprint arXiv:1203.6402. Bateni, M.; Cohen-Addad, V.; Epasto, A.; and Lattanzi, S. 2024. A Scalable Algorithm for Individually Fair k-means Clustering. In International Conference on Artificial Intelligence and Statistics, 3151–3159. PMLR. Beretta, L.; Cohen-Addad, V.; Lattanzi, S.; and Parotsidis, N. 2023. Multi-swap k-means++. Advances in Neural Information Processing Systems, 36: 26069–26091. Cohen-Addad, V.; Green Larsen, K.; Saulpic, D.; Schwiegelshohn, C.; and Sheikh-Omar, O. A. 2022. Improved Coresets for Euclidean k-Means. Advances in Neural Information Processing Systems, 35: 2679–2694. Cohen-Addad, V.; Mirrokni, V.; and Zhong, P. 2022. Massively Parallel k-Means Clustering for Perturbation Resilient Instances. In International Conference on Machine Learning, 4180–4201. PMLR. Huang, J.; Feng, Q.; Huang, Z.; Xu, J.; and Wang, J. 2023. Fast algorithms for distributed k-clustering with outliers. In International Conference on Machine Learning, 13845– 13868. PMLR. Huang, J.; Feng, Q.; Huang, Z.; Xu, J.; and Wang, J. 2024. Linear time algorithms for k-means with multi-swap local search. Advances in Neural Information Processing Systems, 36. J´egou, H.; Tavenard, R.; Douze, M.; and Amsaleg, L. 2011. Searching in one billion vectors: re-rank with source coding. In 2011 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 861–864. IEEE. Jung, C.; Kannan, S.; and Lutz, N. 2020. Service in your neighborhood: Fairness in center location. Foundations of Responsible Computing (FORC). Lattanzi, S.; and Sohler, C. 2019. A better k-means++ algorithm via local search. In International Conference on Machine Learning, 3662–3671. PMLR. Mahabadi, S.; and Vakilian, A. 2020. Individual fairness for k-clustering. In International conference on machine learning, 6586–6596. PMLR.

Negahbani, M.; and Chakrabarty, D. 2021. Better Algorithms for Individually Fair k-Clustering. Advances in Neural Information Processing Systems, 34: 13340–13351. Nguyen, H. L.; Nguyen, T.; and Jones, M. 2022. Fair range k-center. arXiv preprint arXiv:2207.11337. Vakilian, A.; and Yalciner, M. 2022. Improved approximation algorithms for individually fair clustering. In Proceeding of the 25th International Conference on Artificial Intelligence and Statistics, 8758–8779.

20657
