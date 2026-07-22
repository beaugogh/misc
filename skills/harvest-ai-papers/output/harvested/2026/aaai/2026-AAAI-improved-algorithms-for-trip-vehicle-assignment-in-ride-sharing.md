---
title: "Improved Algorithms for Trip-Vehicle Assignment in Ride-Sharing"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40978
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40978/44939
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Improved Algorithms for Trip-Vehicle Assignment in Ride-Sharing

<!-- Page 1 -->

Improved Algorithms for Trip-Vehicle Assignment in Ride-Sharing

Jingyang Zhao1,2, Mingyu Xiao1*, Yonghang Su1

1University of Electronic Science and Technology of China 2Kyung Hee University, Yongin-si, South Korea jingyangzhao1020@gmail.com, myxiao@uestc.edu.cn, suyh 123@163.com

## Abstract

The RIDE-SHARING ASSIGNMENT PROBLEM (AAAI 2018) is a fundamental problem in intelligent transportation systems, urban mobility, and algorithmic decision-making. Given a set of m vehicles with initial locations and n requests (n ≤mk), each with a specified origin and destination, the goal is to assign at most k requests to each vehicle and compute corresponding routes that minimize the total travel distance. The algorithmic approach depends on whether n = mk or n < mk. In this paper, we present algorithms with provable approximation guarantees for both cases. When n = mk, we design a min{O(

√ k), O(p n k)}-approximation algorithm, whereas previously the ratio O(

√ k) was only proved for k being a power of 2. When n < mk, we achieve an approximation ratio of O(

√ k log max{n, m}), breaking the natural O(k) barrier. We also conduct experiments to evaluate the empirical performance of our algorithms. The results show that our solutions consistently outperform those produced by the previous existing algorithm.

Code — https://github.com/Serryh1/RSAP

## Introduction

As urbanization accelerates and private car ownership becomes increasingly unsustainable in densely populated areas (Clewlow and Mishra 2017), ride-sharing has emerged as a promising alternative, with the potential to alleviate traffic congestion, improve travel efficiency, and reduce environmental impact (Ho et al. 2018).

In recent years, many platforms, such as Uber, Lyft, and Didi Chuxing, have enabled passengers to share rides with others traveling in a similar direction (Wang and Yang 2019). The concept has also extended to long-distance travel, with services like BlaBlaCar facilitating intercity and even international carpooling (Shaheen, Stocker, and Mundler 2017). Moreover, ride-sharing has gained traction in corporate transportation and campus shuttle systems (Knopp, Biesinger, and Prandtstetter 2021; AlQuhtani 2022), offering cost-effective and resource-efficient alternatives for group transit.

*Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

The benefits of ride-sharing are well-documented. Passengers can reduce travel costs, and service providers can increase revenue by combining multiple requests into shared trips (Zeng, Tong, and Chen 2019; Luo and Spieksma 2022). Additionally, shared rides reduce total vehicle mileage, leading to lower fuel consumption and fewer carbon emissions (Coulombel et al. 2019; Cai et al. 2019; Yu et al. 2017).

However, realizing these benefits in practice hinges on the ability to efficiently match passengers with vehicles and plan feasible routes under real-world constraints. This core challenge gives rise to computationally complex optimization problems (Bei and Zhang 2018; Luo and Spieksma 2022).

In this paper, we study the RIDE-SHARING ASSIGN- MENT PROBLEM (RSAP) (Bei and Zhang 2018), which formalizes this fundamental decision task: how to assign a set of transportation requests, each with pickup and drop-off locations, to a fleet of vehicles in a way that respects capacity constraints and minimizes total travel cost.

Formally, we are given a set of n requests R = {(si, ti): i = 1,..., n}, where each request involves transporting an agent (or object) from source si to destination ti. There is also a set of m vehicles U = {u1,..., um}, each starting at location ui (used to represent the vehicle itself). The objective is to assign requests to vehicles such that:

• Each vehicle serves at most k requests;

• Each request is served by exactly one vehicle;

• The total distance traveled by all vehicles is minimized.

That is, we seek a partition of requests into m disjoint groups R = {Ru ⊆R: u ∈U} with |Ru| ≤k for each Ru ∈R, and a feasible route Iu for each vehicle to serve the requests in Ru. A solution is represented by the pair (R, I), where I = {Iu: u ∈U} denotes the set of routes. Vehicles are not required to return to their starting locations, and feasibility requires that n ≤mk.

As in prior work (Bei and Zhang 2018; Li, Li, and Lee 2020; Luo and Spieksma 2020, 2022; Luo et al. 2022), we focus on non-preemptive routes: once a vehicle picks up an object, it must deliver it directly to its destination without intermediate drop-offs.

We aim to design approximation algorithms for the RSAP. For minimization problems, a ρ-approximation algorithm is one that runs in polynomial time and returns a solution with

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

36556

<!-- Page 2 -->

objective value at most ρ times the optimal, where ρ ≥1 is called the approximation ratio.

## Related Work

Bei and Zhang (2018) initiated the study of the RSAP, showing that the problem is NP-hard even for k = 2. They presented a 2.5-approximation algorithm for the case k = 2 and n = 2m. Li, Li, and Lee (2020) extended this result by giving a 2.5-approximation for k = 2 and n < 2m.

Using techniques from an assignment problem (Goossens et al. 2012), Luo and Spieksma (2020, 2022) improved the approximation to 2 for k = 2 and n = 2m. They also showed that the RSAP is APX-hard for any k ≥2, and gave a simple (2k −1)-approximation algorithm for general k.

Luo et al. (2022) later proposed a matching-based algorithm for the case n = mk, achieving an O(

√ k) approximation when k is a power of 2. However, their analysis is incomplete for general k, and we provide an instance (see details in the full version) where the algorithm fails to achieve any constant-factor approximation for k = 3. Thus, for non-power-of-2 values of k, the best known ratio remains 2k −1 (Luo and Spieksma 2022). It is worth noting that ride-sharing has also been studied under different objectives, such as maximizing revenue (Tong et al. 2018a; Jacob and Roet-Green 2021; Zheng, Chen, and Ye 2018), minimizing maximum vehicle distance (Zeng, Tong, and Chen 2019), and designing truthful mechanisms (Shen, Lopes, and Crandall 2016; Kleiner, Nebel, and Ziparo 2011; Protopapas et al. 2024).

Our Contributions We introduce new approximation algorithms for the RSAP that significantly improve upon previous results for both cases n = mk and n < mk (see Table 1). Our main contributions are summarized below:

1. Case n = mk. We propose two new algorithms:

• ALG.1 achieves an approximation ratio of O(√ k), which is O(√n) in the worst case. • ALG.2 achieves an approximation ratio of O(p n k). Taking the better of the two, we obtain an approximation ratio of min{O(

√ k), O(p n k)}, which is at most O(4√n) in the worst case. Previously, the best ratio was O(

√ k) when k is a power of 2, and 2k −1 otherwise. 2. Case n < mk. We present the first non-trivial approximation algorithm, ALG.3, which achieves an approximation ratio of O(

√ k log max{n, m}), breaking the natural O(k) barrier for the first time. 3. Experimental Results. We implemented our algorithms for the n = mk case. The results show that our methods outperform the algorithm in (Luo et al. 2022), especially when k is not a power of 2. Due to its complexity, we did not implement the algorithm for the n < mk case, which may require further engineering effort to be practical.

Due to limited space, the proofs of lemmas marked with “*” were omitted, and they can be found in the full version of this paper.

n Approximation Ratio Reference n = mk

2k −1 Luo and Spieksma (2022) O(

√ k) under k = 2, 4, 8,... Luo et al. (2022) min{O(

√ k), O(p n k)} This Paper n < mk 2k −1 Luo and Spieksma (2022) O(

√ k log max{n, m}) This Paper

**Table 1.** A summary of previous approximation algorithms and our approximation algorithms for the RSAP.

Notation

Let G = (V = U ∪S ∪T, E, w) denote the input complete graph, where U = {u1,..., um} denotes the initial locations of the m vehicles, S = {s1,..., sn} (resp., T = {t1,..., tn}) denotes the origins (resp., destinations) of the n requests, and w is a non-negative weight function defined on the edges in E. For convenience, we assume that V consists of m+2n distinct vertices and that w is a metric satisfying w(a, a) = 0, w(a, b) = w(b, a), and the triangle inequality w(a, b) ≤ w(a, c) + w(c, b) for all a, b, c ∈V.

We let R = {(si, ti)}n i=1 denote the set of n requests. Throughout the paper, we work with multi-edge sets, and the union of any two edge sets is taken with multiplicities. Given a subgraph S of G, we let V (S) (resp., E(S)) denote its vertex (resp., edge) set.

A walk in a graph, denoted by W = v1v2...vl, is a sequence of vertices, where one vertex may appear more than once and each consecutive pair of vertices is connected by an edge. We denote the edge set of W by E(W) = {v1v2,..., vl−1vl}. A path in a graph is a walk where no vertex appears more than once, and a path on l distinct vertices is referred to as an l-path, whose order is l. Given a walk W, one can skip some vertices on the walk to obtain a new walk W ′, and such an operation is called shortcutting. For example, if W = v1v3v2v3v4, by shortcutting the vertices v3 and v4, we obtain a new walk W ′ = v1v2. If the edge weight function w satisfies the triangle inequality, we have w(W ′) ≤w(W).

In a graph G′ = (V ′, E′, w′), an l-path partition P is a set of |V ′| l vertex-disjoint l-paths that together cover all vertices in V ′. Note that there exists an l-path partition in G′ only if |V ′| is divisible by l. For any vertex v ∈V ′, the degree of v in G′ is the number of edges in E′ incident to v. If G′ is connected and the number of odd-degree vertices in V ′ is either 0 or 2, then a walk W with E′(W) = E′ can be found in O(|E′|) time (Schrijver 2003). Note that when there are exactly two odd-degree vertices, the walk W starts and ends at those two vertices, respectively.

For any integer t > 0, we denote the set {1,..., t} by [t]. A route of a vehicle u that satisfies the requests in {(si, ti)}k i=1 is a walk starting from u that visits all vertices in {si, ti}k i=1, such that for each i ∈[k], si appears before ti on the walk.

For the RSAP, we fix an optimal solution (R∗, I∗), where we let R∗= {R∗ u | u ∈U} and I∗= {I∗ u | u ∈U}. That is, for each vehicle u ∈U, R∗ u denotes the set of requests assigned to u, and I∗denotes the corresponding route. We let OPT = P

I∈I∗w(I) denote the total weight of the routes in this optimal solution.

36557

<!-- Page 3 -->

## Algorithm

1: ALG.1 Input: An instance G = (V = U ∪S ∪T, E, w). Output: A feasible solution.

1: Construct a complete graph H = (VH, EH, ˆw), where VH = [n] and ˆw(i, j):= w(si, sj) + 3

4w(ti, tj) for any i, j ∈[n]. 2: Compute a 4(1 −1 k)-approximate k-path partition P in H using GW.1 in (Goemans and Williamson 1995). 3: Obtain a set of m pairwise disjoint groups R, w.r.t. P, where each group contains exactly k requests. 4: Construct a complete bipartite graph B = (U ∪R, EB, c), where, for any u ∈U and R ∈R, set the cost of the edge between them as c(u, R):= min(si,ti)∈R(w(u, si)+w(si, ti)). 5: Compute a minimum cost perfect matching M ∗in B using Edmonds’ blossom algorithm (Schrijver 2003). 6: for each (u, Ru) ∈M ∗do 7: Assign all requests in Ru to vehicle u. 8: Obtain two k-paths P s u = sσ1...sσk and P t u = tσ1...tσk in G, assuming that the k-path w.r.t. Ru in P is Pu = σ1...σk. 9: Set Eu:= E(P s u) ∪E(P s u) ∪E(P t u) ∪{usσi, sσitσi}, assuming that c(u, Ru) = w(u, sσi) + w(sσi, tσi). 10: Let Eu:= Eu ∪{tσ1tσi} if w(tσ1, tσi) ≤w(tσi, tσk), and Eu:= Eu ∪{tσitσk} otherwise. 11: Compute a walk Wu in G[Eu] that traverses all edges in Eu (Schrijver 2003). 12: Construct a route Iu by shortcutting Wu. 13: end for 14: return (R, I), where I = {Iu | u ∈U}.

Algorithms for Case n = mk In this section, we introduce two new algorithms (ALG.1 and ALG.2) for the case n = mk.

The First Algorithm ALG.1 is based on the well-known 4(1 −1 k)-approximation algorithm, denoted as GW.1, for the k-path partition problem (Goemans and Williamson 1995).

The main idea of ALG.1 is to use GW.1 to partition all n requests in R into a set of m groups R with each containing exactly k requests. However, since each request consists of two locations, we cannot directly apply GW.1 to the original graph G to obtain the desired partition. To address this, we construct a complete graph H = (VH, EH, ˆw), where VH = [n] and ˆw(i, j):= w(si, sj) + 3

4w(ti, tj) for any i, j ∈[n]. Note that ˆw remains a metric. Then, we apply GW.1 to H to compute a k-path partition P, where each k-path P ∈P corresponds to a group of k requests. Therefore, based on P, we obtain the desired set of m groups R.

To assign the groups in R to the m vehicles, we use Edmonds’ blossom algorithm (Schrijver 2003) to compute a minimum cost bipartite perfect matching M ∗between the groups in R and the vehicles in U, where, for any u ∈U and R ∈R, the cost of the edge between them is defined as c(u, R):= min(si,ti)∈R(w(u, si) + w(si, ti)).

Finally, for each pair (u, Ru) ∈M ∗, we design a route Iu for vehicle u to serve all requests in Ru, based on the use of the corresponding k-path Pu ∈P in H.

The details of ALG.1 are presented in Algorithm 1. Lemma 1. For the RSAP with n = mk, ALG.1 computes in O(n3) time a solution (R, I) with w(I) ≤2 ˆw(P)+c(M ∗).

**Figure 1.** An illustration of the graph G[Eu], where we assume that w(tσ1, tσi) ≤w(tσi, tσk). In this case, we also know that Wu = usσi...sσitσi...tσk.

Proof. Since I = {Iu | u ∈U}, to prove w(I) ≤2 ˆw(P) + c(M ∗), it suffices to prove that, for each pair (u, Ru) ∈M ∗, the inequality w(Iu) ≤2 ˆw(Pu)+c(u, Ru) holds, where Pu is the k-path in P w.r.t. Ru. We begin by analyzing w(Eu).

By Lines 8 and 9, we have Pu = σ1...σk, P s u = sσ1...sσk, P t u = tσ1...tσk, and c(u, Ru) = w(u, sσi) + w(sσi, tσi). By Lines 9 and 10, we have w(Eu) = 2w(P s u) + w(P t u) + c(u, Ru) + Z, (1)

where Z = min{w(tσ1, tσi), w(tσi, tσk)} ≤1

2w(tσ1, tσi)+ 1 2w(tσi, tσk). An illustration of G[Eu] is shown in Figure 1. Since w(tσ1, tσi) + w(tσi, tσk) ≤w(P t u) by the triangle inequality, we have w(Eu) ≤2w(P s u) + 3

2w(P t u) + c(u, Ru)

= 2 ˆw(Pu) + c(u, Ru),

(2)

where the first inequality follows from (1), and the equality follows from the definition of ˆw (see Line 1).

Next, we prove that Iu is a feasible route for vehicle u and its weight satisfies that w(Iu) ≤w(Eu).

Note that G[Eu] is a connected graph with exactly 2 odddegree vertices: u and tσk if w(tσ1, tσi) ≤w(tσi, tσk), and u and tσ1 otherwise (see Figure 1). Hence, a walk Wu with w(Wu) = w(Eu) can be computed in Line 11. Note that for each j ∈[k], sσj appears before tσj in Wu. Thus, by Line 12, Iu is a feasible route for vehicle u that satisfies all requests in Ru. Moreover, by the triangle inequality, we have w(Iu) ≤w(Wu), and then we obtain w(Iu) ≤w(Eu).

Since P is a k-path partition in H, we have S

R∈R R = R. Then, since for each Ru ∈R, there is a route Iu ∈I for vehicle u that satisfies all requests in Ru, we know (R, I) is a feasible solution for the RSAP.

For the running time of ALG.1, GW.1 in Line 2 runs in O(n2 log n) time (Goemans and Williamson 1995), the minimum cost perfect matching in Line 5 can be computed in O(m3) time (Schrijver 2003), and the walk in Line 11 can be computed in O(k) time (Schrijver 2003). Therefore, ALG.1 takes O(n3) time.

Remark 1. In a bipartite graph with n vertices, a minimum cost perfect matching can be computed in O(n2+ε)-time for any ε > 0 (Chen et al. 2022). As O(n2 log n) ⊆O(n2+ε), the running time of ALG.1 can be improved to O(n2+ε).

To prove the approximation ratio of ALG.1, by Lemma 1, we need to provide upper bounds for ˆw(P) and c(M ∗).

We first consider ˆw(P). We use the following key result.

36558

![Figure extracted from page 3](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Lemma 2 (*). There exists a k-path partition P∗in the graph H such that ˆw(P∗) ≤7(k−1)√k−1 k · OPT.

Since P is a 4(1 −1 k)-approximate k-path partition in H, by Lemma 2, we obtain the following result.

Lemma 3. We have ˆw(P) ≤28(k−1)2√k−1 k2 · OPT.

Then, we consider c(M ∗), which can be bounded by using the famous Hall’s Marriage theorem (Schrijver 2003).

Lemma 4. We have c(M ∗) ≤OPT.

Proof. First, we use the optimal solution (R∗, I∗) and the set of groups R in ALG.1 to construct a k-regular bipartite graph B′ = (U ∪R, EB′, c).

Initially, EB′:= ∅. Recall that for each vehicle u ∈U, the assigned requests to u in the optimal solution is R∗ u ∈R∗. Then, for any vehicle u ∈U and any request (si, ti) ∈R∗ u, we add an edge (u, R) to EB′, where (si, ti) ∈R ∈R. Note that this is always possible since S

R∈R R = R by ALG.1. Moreover, since w(Iu) ≥w(u, si)+w(si, ti) by the triangle inequality and c(u, R) = min(si,ti)∈R(w(u, si) + w(si, ti)) by definition, we have w(Iu) ≥c(u, R). Therefore, we have c(EB′) =

X u∈U

X

(u,R)∈EB′ c(u, R)

≤

X u∈U k · w(Iu) = k · OPT.

(3)

Since exactly k requests are assigned to each vehicle u ∈U in the optimal solution, there are exactly k edges incident to u in B′. Moreover, since each R ∈R consists of k requests, there are also exactly k edges incident to R in B′. Hence, B′ forms a k-regular bipartite graph.

By Hall’s Marriage theorem (Schrijver 2003), the edges in EB′ can be decomposed into k perfect matchings in B′ (see details in the full version). Thus, by (3), there exists a perfect matching M in B′ with c(M) ≤1 k c(EB′) ≤OPT. (4)

Note that M is also a perfect matching in the graph B.

Since M ∗is a minimum cost perfect matching in B, by (4), we have c(M ∗) ≤c(M) ≤OPT.

By Lemmas 1, 3, and 4, we obtain the following theorem.

Theorem 1. For the RSAP with n = mk, ALG.1 achieves an approximation ratio of 56(k−1)2√k−1 k2 + 1.

The Second Algorithm ALG.2 is based on the use of a constrained spanning forest, which is a spanning forest in the graph G[S ∪T]. Moreover, it requires that for any request (si, ti) ∈R, both si and ti lie in the same tree of the forest; and for any tree of the forest, the number of vertices it contains is divisible by 2k. We remark that the weight of an optimal constrained spanning forest naturally provides a lower bound for OPT. We will show that a 2-approximate constrained spanning forest F can be computed in O(n2 log n) time using the primal-dual algorithm, denoted as GW.2, for the general constrained spanning forest problem (Goemans and Williamson 1995).

By definition, each tree F ∈F contains a set of requests RF ⊆R. By doubling all edges in E(F) and shortcutting all ti (resp., si), we can obtain a path P s

F (resp., P t

F). Here, the paths P s

F and P t

F are called consistent, i.e., the set of requests whose origins lie in V (P s

F) is the same as the set of requests whose destinations lie in V (P t

F). ALG.2 aims to use the forest F to find two consistent kpath partitions Ps in G[S] and Pt in G[T] such that for every path P s ∈Ps, which consists of the origins of a set of k requests R, there is a corresponding path P t ∈Pt consisting of the destinations of all requests in R, and vice versa. Thus, they correspond to a set of m groups R, where each group contains exactly k requests. Then, similar to ALG.1, ALG.2 computes a minimum cost bipartite perfect matching M ∗that assigns the groups in R to the vehicles in U. For each pair (u, Ru) ∈M ∗, it designs a route Iu for vehicle u to serve all requests in Ru, based on the corresponding k-paths P s u ∈Ps and P t u ∈Pt. To find the consistent k-path partitions Ps and Pt, ALG.2 first uses the forest F to obtain two consistent sets of paths Ps

F = {P s

F | F ∈F} and Pt

F = {P t

F | F ∈F}. If every path in Ps

F ∪Pt

F has length k, then Ps

F and Pt

F are the desired k-path partitions. Otherwise, there must exist two consistent l′k-paths P s ∈Ps

F and P t ∈Pt

F for some l′ > 1. In this case, ALG.2 invokes a subroutine, called SPLIT, to ‘split’ these two paths into two consistent sets of k-paths, Ps k and Pt k, such that V (P s) = S

P s k ∈Ps k V (P s k) and V (P t) = S

P t k∈Pt k V (P t k). By repeatedly applying this process, ALG.2 constructs the desired consistent k-path partitions.

The details of ALG.2 are presented in Algorithm 2, and its subroutine SPLIT is described in Algorithm 3. Note that SPLIT can be regarded as a divide-and-conquer algorithm.

Lemma 5. In ALG.2, a 2-approximate constrained spanning forest F in G[S ∪T] can be found in O(n2 log n) time.

Proof. Let G′ = (V ′, E′, w) denote the graph G[S ∪T]. The integer program of the minimum general constrained spanning forest problem in (Goemans and Williamson 1995) can be formalized as follows:

minimize

X e∈E′ w(e) · xe (IP)

X e∈δ(S)

xe ≥f(S), ∀∅̸ = S ⊂V ′, xe ∈{0, 1}, ∀e ∈E′, where δ(S) denotes the set of edges with one vertex in S and one vertex in V ′ \ S.

Goemans and Williamson (1995) proved that if the function f is a proper function, the minimum general constrained spanning forest problem w.r.t. f admits a 2-approximation algorithm with a running time of O(n2 log n).

In our constrained spanning forest problem, the spanning forest must satisfy that for any request (si, ti) ∈R, both si and ti lie in the same tree; and for any tree, the number of

36559

<!-- Page 5 -->

## Algorithm

2: ALG.2 Input: An instance G = (V = U ∪S ∪T, E, w). Output: A feasible solution.

1: Compute a 2-approximate constrained spanning forest F in G[S ∪T] using GW.2 in (Goemans and Williamson 1995). 2: Initialize Ps F:= ∅and Pt

F:= ∅. 3: for each F ∈F do 4: Construct a path P s

F (resp., P t

F) by doubling all edges in E(F) and shortcutting all ti (resp., si) in V [F]. 5: Update Ps

F:= Ps

F ∪{P s

F } and Pt

F:= Pt

F ∪{P t

F }. 6: end for 7: Initialize Ps:= Ps F and Pt:= Pt

F. 8: while there exists an lk-path P s ∈Ps with l > 1 do 9: Let the consistent lk-path in Pt be P t. 10: Call SPLIT on P s and P t to obtain k-path sets Ps k and Pt k. 11: Update Ps:= Ps\{P s}∪Ps k and Pt:= Pt\{P t}∪Pt k. 12: end while 13: Obtain a set of m pairwise disjoint groups R from Ps and Pt, where each group contains exactly k requests. 14: Compute a minimum cost perfect matching M ∗using Lines 4- 5 of ALG.1. 15: for each (u, Ru) ∈M ∗do 16: Assign all requests in Ru to vehicle u. 17: Let P s u = sσ′

1...sσ′ k and P t u = tσ1...tσk be the corresponding k-paths from Ps and Pt, respectively. 18: Construct a route Iu using Lines 9-12 of ALG.1. 19: end for 20: return (R, I), where I = {Iu | u ∈U}.

vertices it contains is divisible by 2k. Hence, the integer program of our problem can be formalized into the (IP), where the function f satisfies that for any S ⊆V ′, f(S) ∈{0, 1}, and f(S) = 0 if and only if

• |S| mod 2k = 0, and • |S ∩{si, ti}|̸ = 1 for all (si, ti) ∈R.

It can be verified that f forms a valid proper function (see details in the full version).

Therefore, a 2-approximate constrained spanning forest in the graph G[S ∪T] can be found in O(n2 log n) time.

Similar to Lemma 1, we have the following result.

Lemma 6 (*). For the RSAP with n = mk, ALG.2 computes in O(n3) time a solution (R, I) with w(I) ≤2w(Ps) + 2w(Pt) + c(M ∗).

Similar to Remark 1, the running time of ALG.2 can also be improved to O(n2+ε) for any constant ε > 0.

Lemma 7 (*). We have w(Ps) + w(Pt) ≤ p

72n/k · OPT.

By Lemmas 4, 6, and 7, we have the following result.

Theorem 2. For the RSAP with n = mk, ALG.2 achieves an approximation ratio of p

288n/k + 1.

By Theorems 1 and 2, we obtain the following theorem.

Theorem 3. For the RSAP with n = mk, there exists a min{O(

√ k), O(p n k)}-approximation algorithm.

Note that the ratio in Theorem 3 is at most O(4√n).

## Algorithm

3: SPLIT

Input: Two consistent lk-paths P s and P t, where l > 1. Output: Two consistent sets of k-paths Ps k and Pt k with V (P s) = S

P s k ∈Ps k V (P s k) and V (P t) = S

P t k∈Pt k V (P t k).

1: Initialize Ps k:= {P s} and Pt k:= {P t}. 2: while there exists an l′k-path P s ∈Ps k with l′ > 3 do 3: Let the consistent path in Pt k w.r.t. P s be P t. 4: Assume that P s = sσ1...sσl′k, and let h = ⌈l′

2 ⌉. 5: Obtain two paths P s

1 and P s 2 by deleting the middle edge sσhksσhk+1 from P s, i.e., P s

1 = sσ1...sσhk, and P s

2 = sσhk+1...sσl′k. 6: Obtain two paths P t

1 and P t 2, which are consistent with P s 1 and P s

2 respectively, by shortcutting P t. 7: Assume that P t

1 = tσ′ 1...tσ′ hk, and P t

2 = tσ′ hk+1...tσ′ l′k.

8: Obtain two paths P t

11 and P t 12 by deleting the middle edge tσ′

⌈h

2 ⌉ktσ′ ⌈h

2 ⌉k+1 from P t 1.

9: Obtain two paths P s

11 and P s 12, which are consistent with P t

11 and P t 12 respectively, by shortcutting P s 1. 10: Analogously, obtain two paths P t

21 and P t 22 by deleting the middle edge tσ′

⌈h+l′

2 ⌉k tσ′

⌈h+l′

2 ⌉k+1 from P t

## 2. Then, obtain two

paths P s

21 and P s 22, which are consistent with P t 21 and P t 22 respectively, by shortcutting P s

2. 11: Let Ps k:= Ps k \ {P s} ∪{P s

11, P s 12, P s 21, P s 22} and Pt k:= Pt k \ {P t} ∪{P t

11, P t 12, P t 21, P t 22}. 12: end while 13: while there exists an l′k-path P s ∈Ps k with 2 ≤l′ ≤3 do 14: Let the consistent path w.r.t. P s in Pt k be P t. 15: Assume that P s = sσ1...sσl′k. 16: Obtain a set of l′ k-paths Ps = {P s

1,..., P s l′}, where P s i = sσik−k+1...sσik for each i ∈[l′]. 17: Obtain a set of l′ consistent k-paths Pt = {P t

1,..., P t l′} by shortcutting P t according to each corresponding P s i ∈Ps. 18: Update Ps k:= Ps k \{P s}∪Ps and Pt k:= Pt k \{P t}∪Pt. 19: end while 20: return Ps k and Pt k.

An Algorithm for Case n < mk

In this section, we introduce our third algorithm (ALG.3) that works for the case n < mk.

Similar to ALG.1, ALG.3 begins by obtaining a complete graph H = (VH, EH, ˆw), where VH = U∪[n]. The function

ˆw is defined as follows: ˆw(i, j) = w(si, sj) + w(ti, tj) for any i, j ∈[n], ˆw(ui, j) = w(ui, sj)+w(ui, tj) for any ui ∈ U and j ∈[n], and ˆw(ui, uj) = 2w(ui, uj) for any ui, uj ∈ U. Note that ˆw remains a metric. Next, ALG.3 finds a forest F with possibly minimized ˆw(F) in the graph H such that each tree contains exactly one distinct vehicle uF ∈U and at most k vertices in [n]. We remark that each tree F ∈F in H corresponds to a tree F ′ with w(F ′) = ˆw(F) in G such that F ′ contains the vehicle uF and the origins and the destinations of at most k requests. Moreover, by doubling all edges in E(F ′) and then shortcutting, a feasible route IuF can be obtained with w(IuF) ≤2w(F ′) = 2 ˆw(F).

It remains to show how to compute the forest F with minimized ˆw(F) in the graph H. This problem is in fact a special case of the airport and railway problem (ARP) (Salavatipour and Tian 2025). In the ARP, we are given a metric graph

36560

<!-- Page 6 -->

m: #vehicles k: vehicle capacity c: #centers 2: covariance

**Figure 2.** Experimental results on the datasets. Each row corresponds to one objective (from top to bottom): solution quality and running time. Each column corresponds to varying one parameter (from left to right): m, k, c, and σ2. The results of ALG.1 (ours), ALG.2 (ours), and LADG (previous) are shown as blue, green, and red curves, respectively. Each point represents the average result over 10 instances, while the vertical line segment at each point indicates the minimum and maximum values.

## Algorithm

4: ALG.3 Input: An instance G = (V = U ∪S ∪T, E, w). Output: A feasible solution.

1: Construct a complete graph H = (VH, EH, ˆw), where VH = U ∪[n]. Define ˆw(i, j) = w(si, sj) + w(ti, tj) for any i, j ∈ [n], ˆw(ui, j) = w(ui, sj) + w(ui, tj) for any ui ∈U and j ∈[n], and ˆw(ui, uj) = 2w(ui, uj) for any ui, uj ∈U. 2: Compute an O(log max{n, m})-approximate forest F in H using the algorithm in (Salavatipour and Tian 2025). 3: for each F ∈F do 4: Assume that the vehicle in F is uF. 5: Obtain the corresponding tree F ′ w.r.t. F in the graph G. 6: Let RF denote the set of requests covered by F ′. 7: Assign all requests in RF to vehicle uF. 8: Construct a route IuF by doubling all edges in E(F ′) and then shortcutting. 9: end for 10: return (R, I), where I = {IuF | F ∈F}.

along with a parameter k ∈N+, where each edge has a weight and each vertex has a non-negative opening cost. The goal is to find a forest to cover all vertices, where each tree contains at least one opened vertex and has at most k+1 vertices. The objective is to minimize the total edge weight of the forest plus the total opening cost of the opened vertices.

To see why the problem of computing the forest F with minimized ˆw(F) is a special case of the ARP, consider the graph H with the opening cost of each vertex in U set to 0, and each vertex in [n] set to ∞. Then, any optimal (or approximate) solution to the ARP must be a forest in which each tree contains exactly one vehicle from U and at most k vertices from [n]. (Note that if a tree contains multiple dis- tinct vehicles from U, one can always delete an edge on the unique path between any two of them to split the tree, repeating this process until each tree contains exactly one vehicle.) Since the ARP admits an O(log |V (H)|)-approximation algorithm and |V (H)| = O(n + m), an O(log max{n, m})approximate forest F can be obtained in polynomial time.

The details of ALG.3 are shown in Algorithm 4. First, we analyze the solution weight of ALG.3.

Lemma 8 (*). For the RSAP with n < mk, ALG.3 computes in O(n4 + m4) time a solution (R, I) with w(I) ≤2 ˆw(F).

By slightly modifying the proof of Lemma 2, we obtain

Lemma 9 (*). There exists a forest F∗in the graph H such that ˆw(F∗) ≤8k

√ k k+1 · OPT, where each tree in F∗contains only one vertex from U and at most k vertices from [n].

Since F is an O(log max{n, m})-approximate forest in the graph H, by Lemma 9, we have the following result.

Lemma 10. ˆw(F) ≤O(

√ k log max{n, m}) · OPT.

By Lemmas 8 and 10, we have the following theorem.

Theorem 4. For the RSAP with n < mk, ALG.3 achieves an approximation ratio of O(

√ k log max{n, m}).

## Experiments

We evaluate our algorithms for the case n = mk and compare our proposed algorithms, ALG.1 and ALG.2, with the LADG algorithm from (Luo et al. 2022). Notably, LADG has demonstrated strong empirical performance, outperforming several baselines—including adaptations of dial-a-ride algorithms (Tong et al. 2018b; Zeng, Tong, and Chen 2019) and a greedy heuristic—within the RSAP setting, as reported

36561

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-improved-algorithms-for-trip-vehicle-assignment-in-ride-sharing/page-006-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

m: #vehicles 100 150 200 250 300 350 400 k: vehicle capacity 2 3 · · · 18 · · · 33 34 c: #centers 10 15 20 25 30 35 40 σ2: covariance 40 60 80 100 120 140 160

**Table 2.** Parameter settings for dataset generation. Bold values indicate fixed settings when varying the others.

in (Luo et al. 2022). We do not compare our algorithms with the previous best (2k −1)-approximation algorithm (Luo and Spieksma 2022) for non-power-of-2 values of k, as this algorithm is relatively simple and was also not included in the experimental evaluation of (Luo et al. 2022).

Implementation. Both ALG.1 and ALG.2 run in O(n3) time, while LADG runs in O(n3 log n) time (Luo et al. 2022). Since LADG frequently requires computing minimum weight perfect matchings (Luo et al. 2022), we employ an optimized implementation of Edmonds’ blossom algorithm (Schrijver 2003) to improve its efficiency.

In our implementation, we make a minor modification to the route selection step: when routing a vehicle u to serve its assigned requests Ru, instead of using the fixed edge pair {usσi, sσitσi} yielding c(u, Ru) = w(u, sσi) + w(sσi, tσi) (as in Line 9 of ALG.1), we evaluate all k such edge pairs (sσi, tσi) ∈Ru and choose the one with the minimum weight. This modification does not affect the theoretical approximation ratio and incurs negligible runtime overhead.

All algorithms are implemented in C++, compiled with g++ -O3, and executed on a server with an Intel Xeon Gold 6226R CPU @ 2.90GHz, 512 GB RAM, running Ubuntu Server 20.04 LTS.

Instances. To generate RSAP instances with m vehicles and n = mk requests, we follow the approach in (Bei and Zhang 2018; Luo et al. 2022) within a 4000 × 4000 Euclidean square region ρ = [0, 4000]2.

We first sample c cluster centers {µ1,..., µc} uniformly from ρ. Then, for each vertex v ∈V, we select a center µi uniformly at random and draw v from the 2D Gaussian distribution N(µi, σ2I), where σ2 is the variance and I is the 2 × 2 identity matrix. All sampling steps are independent. Previously, both works (Bei and Zhang 2018; Luo et al. 2022) adopt an instance generation method characterized by four parameters: the number of vehicles m, the vehicle capacity k, the number of centers c, and the covariance σ2. We adopt the same method, and our parameter settings are summarized in Table 2. When varying one parameter, the others are fixed to the boldface values. For each configuration (m, k, c, σ2), we generate 10 independent instances and report average performance.

Results. Figure 2 summarizes our experimental results. Rows correspond to performance metrics (solution quality and running time), while columns reflect variations in each parameter: m, k, c, and σ2. Note that the solution quality refers to the solution weight.

We observe that variations in c and σ2 have a limited effect on performance, which is consistent with the findings of previous experiments (Bei and Zhang 2018; Luo et al. 2022). Hence, we focus our discussion on the impact of m and k.

Solution quality. ALG.1 consistently achieves the best solution quality, which aligns with its theoretical guarantee of outperforming ALG.2 for small values of k. In contrast, LADG performs the worst, even when k is a power of 2.

When varying k, the performance of ALG.1 and ALG.2 remains stable, whereas LADG exhibits pronounced fluctuations: its quality improves significantly when k is a power of 2 but deteriorates sharply when k = 2r −1 for some integer r > 0. These highlight why LADG cannot guarantee a good approximation ratio when k is not a power of 2.

In particular, LADG’s performance tends to degrade when the binary representation of k contains many ones, as this may prevent it from finding perfect matchings during each round of its forward phase (see details of LADG). The worst performance is observed when k = 2r −1 for some integer r > 0, where the binary representation of k consists entirely of ones.

Running time. When varying m or k, ALG.1 and LADG have comparable running times, whereas ALG.2 is the slowest. This is because ALG.1 runs GW.1 on the graph H of size |VH| = n, whereas ALG.2 runs GW.2 on G[S ∪T] with |S ∪T| = 2n. Since both subroutines run in O(n2 log n) time, the runtime of ALG.2 is expected to be roughly four times that of ALG.1.

Given that LADG has a time complexity of O(n3 log n), we believe that optimizing the implementations of GW.1 and GW.2 can further speed up both ALG.1 and ALG.2.

Summary. ALG.1 not only outperforms LADG in solution quality but also runs faster. ALG.2 likewise achieves better solution quality than LADG, albeit with a slightly longer running time. Moreover, the running time of ALG.2 is roughly four times that of ALG.1.

## Conclusion

and Discussion

In this paper, we propose three novel algorithms for the RSAP, significantly improving the best-known approximation ratios for both n = mk and n < mk. Experimental results for the case n = mk demonstrate the strong empirical performance of our algorithms, consistently outperforming the previously best-known algorithm from (Luo et al. 2022).

From a technical perspective, our algorithms employ fundamentally different techniques compared to previous approximation approaches. These techniques show promise for adaptation to related problems, such as the dial-a-ride problem, opening up avenues for future development.

We did not implement ALG.3 for the case n < mk in our experiments. This is because achieving the desired approximation ratio requires invoking the algorithm from (Salavatipour and Tian 2025), which is complex and hard to implement. ALG.3 is primarily designed to establish a theoretical approximation guarantee. For practical deployment, it may be necessary to design more efficient components or simplify certain intricate procedures to ensure scalability and performance in real-world applications. These aspects deserve further investigation.

36562

<!-- Page 8 -->

## Acknowledgments

The work is supported by the National Natural Science Foundation of China under the grants 62502078 and 62372095, and by the Postdoctoral Fellowship Program of CPSF under Grant Number GZC20251102.

## References

AlQuhtani, S. 2022. Ridesharing as a potential sustainable transportation alternative in suburban universities: the case of Najran University, Saudi Arabia. Sustainability, 14(8): 4392.

Bei, X.; and Zhang, S. 2018. Algorithms for Trip-Vehicle Assignment in Ride-Sharing. In AAAI 2018, 3–9. AAAI Press.

Cai, H.; Wang, X.; Adriaens, P.; and Xu, M. 2019. Environmental benefits of taxi ride sharing in Beijing. Energy, 174: 503–508.

Chen, L.; Kyng, R.; Liu, Y. P.; Peng, R.; Gutenberg, M. P.; and Sachdeva, S. 2022. Maximum Flow and Minimum-Cost Flow in Almost-Linear Time. In 63rd IEEE Annual Symposium on Foundations of Computer Science, FOCS 2022, 612–623. IEEE.

Clewlow, R. R.; and Mishra, G. S. 2017. Disruptive transportation: The adoption, utilization, and impacts of ridehailing in the United States. Research Report UCD-ITS-RR- 17-07, University of California, Davis, Institute of Transportation Studies, Davis, CA.

Coulombel, N.; Boutueil, V.; Liu, L.; Viguie, V.; and Yin, B. 2019. Substantial rebound effects in urban ridesharing: Simulating travel decisions in Paris, France. Transportation Research Part D: Transport and Environment, 71: 110–126.

Goemans, M. X.; and Williamson, D. P. 1995. A General Approximation Technique for Constrained Forest Problems. SIAM J. Comput., 24(2): 296–317.

Goossens, D.; Polyakovskiy, S.; Spieksma, F. C.; and Woeginger, G. J. 2012. Between a rock and a hard place: the two-to-one assignment problem. Mathematical methods of operations research, 76(2): 223–237.

Ho, S. C.; Szeto, W. Y.; Kuo, Y.-H.; Leung, J. M.; Petering, M.; and Tou, T. W. 2018. A survey of dial-a-ride problems: Literature review and recent developments. Transportation Research Part B: Methodological, 111: 395–421.

Jacob, J.; and Roet-Green, R. 2021. Ride solo or pool: Designing price-service menus for a ride-sharing platform. Eur. J. Oper. Res., 295(3): 1008–1024.

Kleiner, A.; Nebel, B.; and Ziparo, V. A. 2011. A Mechanism for Dynamic Ride Sharing Based on Parallel Auctions. In Walsh, T., ed., IJCAI 2011, Proceedings of the 22nd International Joint Conference on Artificial Intelligence, Barcelona, Catalonia, Spain, July 16-22, 2011, 266– 272. IJCAI/AAAI.

Knopp, S.; Biesinger, B.; and Prandtstetter, M. 2021. Mobility offer allocations in corporate settings. EURO Journal on Computational Optimization, 9: 100010.

Li, S.; Li, M.; and Lee, V. C. S. 2020. Trip-Vehicle Assignment Algorithms for Ride-Sharing. In COCOA 2020, volume 12577 of Lecture Notes in Computer Science, 681– 696. Springer. Luo, K.; Agarwal, C.; Das, S.; and Guo, X. 2022. The Multivehicle Ride-Sharing Problem. In Candan, K. S.; Liu, H.; Akoglu, L.; Dong, X. L.; and Tang, J., eds., WSDM ’22: The Fifteenth ACM International Conference on Web Search and Data Mining, Virtual Event / Tempe, AZ, USA, February 21 - 25, 2022, 628–637. ACM. Luo, K.; and Spieksma, F. C. 2022. Minimizing Travel Time and Latency in Multi-Capacity Ride-Sharing Problems. Algorithms, 15(2): 30. Luo, K.; and Spieksma, F. C. R. 2020. Approximation Algorithms for Car-Sharing Problems. In Kim, D.; Uma, R. N.; Cai, Z.; and Lee, D. H., eds., Computing and Combinatorics - 26th International Conference, COCOON 2020, Atlanta, GA, USA, August 29-31, 2020, Proceedings, volume 12273 of Lecture Notes in Computer Science, 262–273. Springer. Protopapas, N.; Yazdanpanah, V.; Gerding, E. H.; and Stein, S. 2024. Online Decentralised Mechanisms for Dynamic Ridesharing. In AAMAS 2024, 1602–1610. International Foundation for Autonomous Agents and Multiagent Systems / ACM. Salavatipour, M. R.; and Tian, L. 2025. Approximation algorithms for the airport and railway problem. J. Comb. Optim., 49(1): 8. Schrijver, A. 2003. Combinatorial optimization: polyhedra and efficiency, volume 24. Springer. Shaheen, S.; Stocker, A.; and Mundler, M. 2017. Online and app-based carpooling in France: Analyzing users and practices—A study of BlaBlaCar. Springer. Shen, W.; Lopes, C. V.; and Crandall, J. W. 2016. An Online Mechanism for Ridesharing in Autonomous Mobilityon-Demand Systems. In Kambhampati, S., ed., Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence, IJCAI 2016, New York, NY, USA, 9-15 July 2016, 475–481. IJCAI/AAAI Press. Tong, Y.; Zeng, Y.; Zhou, Z.; Chen, L.; Ye, J.; and Xu, K. 2018a. A Unified Approach to Route Planning for Shared Mobility. Proc. VLDB Endow., 11(11): 1633–1646. Tong, Y.; Zeng, Y.; Zhou, Z.; Chen, L.; Ye, J.; and Xu, K. 2018b. A unified approach to route planning for shared mobility. Proceedings of the VLDB Endowment, 11(11): 1633. Wang, H.; and Yang, H. 2019. Ridesourcing systems: A framework and review. Transportation Research Part B: Methodological, 129: 122–155. Yu, B.; Ma, Y.; Xue, M.; Tang, B.; Wang, B.; Yan, J.; and Wei, Y.-M. 2017. Environmental benefits from ridesharing: A case of Beijing. Applied Energy, 191: 141–152. Zeng, Y.; Tong, Y.; and Chen, L. 2019. Last-Mile Delivery Made Practical: An Efficient Route Planning Framework with Theoretical Guarantees. Proc. VLDB Endow., 13(3): 320–333. Zheng, L.; Chen, L.; and Ye, J. 2018. Order Dispatch in Price-aware Ridesharing. Proc. VLDB Endow., 11(8): 853– 865.

36563
