---
title: "EFX and PO Allocation Exists for Two Types of Goods"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38723
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38723/42685
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# EFX and PO Allocation Exists for Two Types of Goods

<!-- Page 1 -->

EFX and PO Allocation Exists for Two Types of Goods

Vladimir Davidiuk2, Yuriy Dementiev1, Artur Ignatiev1, Danil Sagunov1

1ITMO University 2St. Petersburg State University

## Abstract

We study the problem of fairly and efficiently allocating indivisible goods among agents with additive valuations. We focus on envy-freeness up to any good (EFX) — an important fairness notion in fair division of indivisible goods. A central open question in this field is whether EFX allocations always exist for any number of agents. While recent results have established EFX existence for settings with at most three distinct valuations and for two types of goods, the general case remains unresolved. In this paper, we extend the existent knowledge by proving that EFX allocations satisfying Pareto optimality (PO) always exist and can be computed in quasiliniear time when there are two types of goods, given that the valuations are positive. Our findings demonstrate a fairly simple and efficient algorithm constructing an EFX+PO allocation.

## Introduction

Fair division of indivisible goods is a core research area in algorithmic game theory and computational social choice, focusing on the equitable allocation of discrete items—such as property, licenses, or humanitarian aid—among agents with heterogeneous preferences. The online platform Spliddit (spliddit.org) offers practical implementations of fair division algorithms, addressing real-world allocation challenges including rent distribution among roommates, taxi fare splitting, and fair assignment of goods between individuals. A central goal is to achieve fairness and effectiveness guarantees that balance efficiency and equity, even when exact solutions are theoretically or computationally out of reach.

The gold standard of fairness, envy-freeness (EF) (Foley 1966), ensures no agent prefers another’s allocation over their own. Yet, EF allocations often fail to exist for indivisible goods, and even when they do, identifying them is NP-complete as shown by (Lipton et al. 2004) even with two agents. This limitation has spurred the study of meaningful relaxations. The initial relaxation of envy-freeness is the concept of envy-freeness up to one good (EF1), which was informally introduced by (Lipton et al. 2004) and later formally defined by (Budish 2011). Under EF1, an agent i may envy agent j, provided there is at least one good in j’s

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

bundle such that, if removed, i’s envy toward j would disappear. EF1 allocations always exist for indivisible goods under additive valuations and can be computed in polynomial time using algorithms like the envy cycle elimination method (Lipton et al. 2004). (Caragiannis et al. 2019) proved that Round-Robin algorithms leads to an EF1 allocation. As proven by (Caragiannis et al. 2019), allocations maximizing the Nash Social Welfare (MNW) are necessarily Paretoefficient and envy-free up to one good. Among these, envyfreeness up to any good (EFX), introduced by (Caragiannis et al. 2019), has emerged as a compelling alternative. EFX softens the strictness of EF: while an agent may envy another’s bundle, this envy vanishes upon the removal of any single good from the envied bundle. The existence of EFX is still open for n agents with arbitrary additive valuations.

Recent years have seen significant progress in answering this question, though a general solution remains elusive. The first positive existence result was shown by (Plaut and Roughgarden 2020) for when the agents have identical valuations, they showed that the lexicographic minimal (lexmin) solution guarantees EFX in this case. For two agents, (Plaut and Roughgarden 2020) showed that the cut and choose algorithm guarantees EFX. (Chaudhury, Garg, and Mehlhorn 2024) extended this result to three agents, while (Mahara 2023) and (Prakash HV et al. 2025) proved existence for settings with two and three types of agents, respectively. On the other side, (Gorantla, Marwaha, and Velusamy 2023) demonstrated that EFX allocations exist when goods belong to just two distinct types, even providing a partial characterization of when exact envy-freeness (EF) is achievable in such cases. A previous paper established the existence of EFX and PO allocations under lexicographic preferences (Hosseini et al. 2021). Moreover, (Garg and Murhekar 2023) proved that an EFX and fPO allocation exists and can be computed in polynomial time for bivalued instances.

Pareto optimality is a fundamental efficiency concept in fair division, ensuring no agent can improve their allocation without harming others. (Amanatidis et al. 2021) showed that when goods take on at most two possible values, the Maximum Nash Welfare (MNW) solution guarantees EFX and Pareto optimality (PO), also they show a polynomialtime algorithm for EFX based on matching. However, (Plaut and Roughgarden 2020) also revealed a sobering limitation: if agents can assign zero value to goods, EFX and PO may

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16795

<!-- Page 2 -->

be incompatible. This leaves an open problem: Does an EFX and PO allocation always exist when all valuations are positive?

Our Contribution. We significantly advance the understanding of fair and efficient allocations for two types of goods. First, we prove that EFX+PO allocation always exist when all agents have positive utilities, while demonstrating that the stronger EFX+fPO combination remains impossible. This improves upon (Gorantla, Marwaha, and Velusamy 2023), who established EFX existence without Pareto optimality.

We provide an efficient algorithmic solution: our approach computes such an allocation in O(n log n + log m) time for n agents and m goods. It works as fast as O(log n+ log m) time, if the agents are ordered by their relative valuations of good types. Additionally, we introduce a class of proper allocations and prove that every proper allocation is Pareto optimal, offering new structural insights into the interplay between fairness and efficiency.

Example: EFX and fPO are not always compatible. Consider a simple example with two types of goods (croissant and coffee) and two agents (Alice (1) and Bob (2)). There are two croissants (a) and two coffees (b), with valuations v1(a) = v2(a) = 1 and v1(b) = 10 and v2(b) = 9. In the unique EFX allocation, each agent receives one croissant and one coffee. While this allocation is envy-free up to any good, it fails to be fractionally Pareto optimal (fPO): a fractional allocation where Alice gets 1.1 coffee and Bob gets 0.9 coffee plus two croissant would strictly improve the allocation, Alice has the same utility, but Bob increases his utility (11 for Alice and 10.1 for Bob). However, in the indivisible setting, this EFX allocation is Pareto optimal (PO), as no discrete reallocation can improve one agent’s utility without harming the other. This demonstrates that there may not be allocations that satisfy EFX and fPO simultaneously. In our turn, we show that an EFX+PO allocation always exists.

1

1 1

1 10 10

9 9

**Table 1.** Example with two types of goods.

Additional Related Work. The fair division of indivisible goods has witnessed remarkable theoretical and algorithmic progress in recent years, as documented in several comprehensive surveys (Amanatidis et al. 2023; Aziz et al. 2022; Nguyen and Rothe 2023). One promising direction involves EFX relaxation by allowing a small subset of goods to remain unassigned—often interpreted as charitable donations—while maintaining fairness guarantees. While trivially satisfying envy-freeness by leaving all goods unallocated is meaningless, meaningful progress has been made in bounding both the number of discarded items and their welfare impact. (Caragiannis, Gravin, and Huang 2019) demonstrated that an EFX allocation exists for a subset of goods while preserving at least half of the Maximum Nash Welfare. (Chaudhury et al. 2021) developed an algorithm for computing partial EFX allocations where: (i) at most n −1 goods remain unassigned, and (ii) no agent strictly prefers the set of unallocated goods to their own bundle, while (Berger et al. 2022) and (Mahara 2024) later reduced this to n −2 goods in general and just one good for four agent instances. (Ghosal et al. 2025) generalized these results, proving that for agents with at most k distinct valuations, EFX allocations exist with k −2 unassigned goods.

Approximate EFX notions have also gained attention, where an allocation is α-EFX if no agent envies another after scaling the other’s bundle without any good by α, formally if for every pair of agents i and j: vi(Xi) ≥α · vi(Xj \ g) for any g ∈Xj. (Plaut and Roughgarden 2020) established the existence of 0.5-EFX allocations, and this bound was later improved to 0.618 by (Amanatidis, Markakis, and Ntokos 2020). Most recently, (Amanatidis, Filos-Ratsikas, and Sgouritsa 2024) showed that 2

3-EFX allocations exist for up to seven agents or when agents have no more than three distinct valuations.

Setting. The setting consists of a set of n agents N = [n] = {1,..., n}, and a multiset M of indivisible goods that contains copies of two different goods: g1 with multiplicity m1 and g2 with multiplicity m2. Each agent i ∈N has a valuation function vi: 2M →R>0, which quantifies the utility that i derives from any subset of goods. We focus on additive valuations, meaning the value of a subset of goods is simply the sum of the values of its individual items. Formally, for any subset S ⊆M, the valuation function satisfies vi(S) = P g∈S vi(g). An allocation X = (X1, X2,..., Xn) is a partition of M into n disjoint subsets, called bundles, where each agent i receives the bundle Xi. We match allocation X with the multiplicity of goods in each agent’s bundle {(xi,1, xi,2) | i ∈[n]}, so we can assume that agents utility equals vi(Xi) = xi,1·vi,1+xi,2·vi,2, where vi,j = vi({gj}) for each i ∈[n], j ∈[2]. Definition 1 (EFX). An allocation X is envy-free up to any good (EFX) if, for every pair of agents i, j ∈N, it holds that vi(Xi) + vi(g) ≥vi(Xj) for any g ∈Xj.

We say that agent i envies agent j up any good if vi(Xi)+ ming∈Xj vi(g) < vi(Xj). Definition 2 (PO). An allocation X is Pareto optimal (PO) if there is no allocation Y such that vi(Yi) ≥vi(Xi) for all i ∈N and vj(Yj) > vj(Xj) for some j ∈N. Equivalently, we will say that such an allocation is not Pareto dominated by any other allocation.

The Setup To show our main result, we have to define several crucial concepts. In this section, we give necessary definitions and formulate fundamental properties of our allocation structures. They serve as a backbone of our algorithm.

Most of the properties in this section are given without proofs to ease the understanding of the construction and

16796

![Figure extracted from page 2](2026-AAAI-efx-and-po-allocation-exists-for-two-types-of-goods/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-efx-and-po-allocation-exists-for-two-types-of-goods/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-efx-and-po-allocation-exists-for-two-types-of-goods/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-efx-and-po-allocation-exists-for-two-types-of-goods/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

the algorithm itself. Complete proofs of such properties and claims can be found in subsequent sections or the supplementary materials of this paper. We mark all statements, the proof of which can be found in the appendix, with a star (⋆).

Input preprocessing. Our first goal is to make the input data much more convenient and reflecting the actual allocation properties.

By n we denote the number of agents, by m1 and m2 we denote the total quantities of items of first and second types respectively. We naturally assume that n ≥1 and m1, m2 ≥ 1. Agents are identified with integer numbers in [n]. For i ∈ [n], j ∈[2], let vi,j denote the utility of an item of type j as estimated by agent i.

We then divide the agents in two groups, the first group consists of agents i that have vi,2 ≤vi,1 (agents that prefer a good of type 1 to a good of type 2 or value them equally), the second consists of agents i that have vi,2 ≥vi,11. Note that there may be several ways to divide the agents, choose any of them arbitrarily. Let n1, n2 denote the obtained group sizes. If it appears that m1 n1 < m2 n2, we interchange the good types and the groups (that is why we defined the groups symetrically). Then the inequality m1 n1 ≥m2 n2 holds. If n2 = 0, we consider that m2 n2 = ∞. This means, in particular, that n2 > 0.

We assume that vi,j > 0 for each i ∈[n], j ∈[2], as motivated in the introduction. Then, we normalize the agent utilities: we replace (vi,1, vi,2) with (1, vi,2/vi,1) for each agent i ∈[n]. Finally, we re-enumerate the agents in the way that vi,2 ≤vi+1,2 holds for each i ∈[n−1]. By definition of n1 and n2, we have that ∀i ∈[n1]: vi,2 ≤1 and vn1+1,2 ≥ 1. The other thing crucial to our further constructions is that the total number of goods is at least the number of agents. Observation 1 (⋆). If m1 + m2 ≤n, give one good of the first type to each agent i with i ≤m1. Give one good of the second type to each agent i with i ≥n −m2 + 1. This allocation is EFX+PO.

We are ready to summarize our restrictions on the input, that all hold true after the input is preprocessed. We provide them below.

Preprocessed input restrictions

• For each i ∈[n], vi,1 = 1 and vi,2 > 0; • For each i ∈[n −1], vi,2 ≤vi+1,2; • n1 + n2 = n and vn1,2 ≤1 and vn1+1,2 ≥1; • m1/n1 ≥m2/n2 and m2 > 0 and n2 > 0; • m1 + m2 ≥n. Thoughout the rest of the paper, we always assume that the input satisfies the above constraints. Our results might not hold true if these constraints are not satisfied.

Proper allocations. In our work, the Pareto-optimality is achieved in all of the constructed allocations, both intermediate ones (that might not be EFX) and the resulting one (that is necessary EFX). All of our allocations fall under the notion given below.

1We do not use vi,2 > vi,1 here for purpose.

Definition 3 (Proper allocation). An allocation of goods {(xi,1, xi,2)} is proper, if there exists t ∈[n] such that

• for each i ∈[t −1], xi,2 = 0, and • for each i ∈[t + 1, n], xi,1 < vt,2. For example, the allocation in Observation 1 is proper (choose t = m1). As announced above, we will prove that all proper allocations are PO, as formulated below. Theorem 1. If allocation is proper, then it is Pareto-optimal.

Prioritized equitable allocations. The following notion is basic to our allocation constructions. It formally defines the process of dividing the identical goods between specific agents in (almost) equal parts, where some specific agents should receive the greater part.

The notion below defines this process formally. Note that we use it for partial allocation of goods, while complete allocations are formed via performing several partial allocations consecutively. Definition 4 (Prioritized equitable allocation, PEA). For integers c ∈[2], q ∈[mt], s ∈[n], and a sequence of distinct agents a1, a2,..., as ∈[n], we say that we give q goods of type c equitably prioritized to the agents a1, a2,..., as, if

• for each i ∈[s], agent ai receives either ⌊q/s⌋or ⌈q/s⌉ goods of type c; • for each 1 ≤i < j ≤s, agent aj receives at least as many goods of type c as ai. Equivalently, if we give q goods of type c to s agents a1, a2,..., as equitably prioritized, and r is the remainder of division of q by s, then agents a1, a2,..., as−r receive ⌊q/s⌋goods each, and agents as−r+1,..., as receive ⌈q/s⌉ goods each.

Split allocations. We move on to the central allocation construction of our algorithm, the split allocations. Simply speaking, in a split allocation, only a specified agent t (the “split point”) can receive goods of both types simultaneously. Agents i < t or agents i > t receive only goods of the first type or the second type respectively.

A split allocation is uniquely identified by two integers: t ∈[n] and k ∈[m2] — the number of goods of the second type given to agent t. These integers should fit under specific constraints. We define all valid pairs of integers T ⊂[n] × [m2]:

T =

(t, k): vt,2 ≥1, t < n, k ≤ m2 n −t + 1

∪{(n, m2)}.

Note that T is not empty since n2 > 0 and m2 > 0. We now give formal definition to split allocations. Definition 5 (Split allocations). For (t, k) ∈T, the (t, k)split-allocation is defined by 1. Give k goods of the second type to agent t. 2. Give (m2 −k) remaining goods of the second type equitably prioritized to agents t + 1, t + 2,..., n. 3. Let p = ⌈k · vt,2⌉. Give min{p(t −1), m1} goods of the first type equitably prioritized to agents 1, 2,..., t −1. 4. Give remaining max{0, m1 −p(t−1)} goods of the first type equitably prioritized to agents 1, 2,..., t.

16797

<!-- Page 4 -->

(t, k)-split-allocation as PEA sum Type

(c)

Quantity

(q)

Agent seq. (a1,..., as) 2 k t 2 m2 −k t + 1,..., n 1 min{m1, ⌈kvt,2⌉· (t −1)} 1,..., t −1 1 max{m1 −⌈kvt,2⌉· (t −1)} 1,..., t

**Table 2.** Expessing (t, k)-split-allocation as a series of prioritized equitable allocations.

We summarize that the (t, k)-split-allocation is expressed as a sequence of four prioritized equitable allocations in Table 2. Note that the agent t can receive 0 goods of the first type, as demonstrated in Table 3.

1... t −1 t t + 1... n 1 ⌊m1 t−1⌋... ⌈m1 t−1⌉ 0 0... 0 2 0... 0 k ⌊m2−k n−t ⌋... ⌈m2−k n−t ⌉

**Table 3.** Structure of (t, k)-split-allocations with m1 ≤ p(t −1). The number in ith column and jth row equals xi,j, the number of goods of type j given to agent i.

The following simple observation explains why split allocations are PO.

Observation 2. For each (t, k) ∈ T, the (t, k)-splitallocation is proper.

Envy direction. Our algorithm will encounter several split allocations. If at least one of split allocations it encounters is EFX, the algorithm will be fine.

But if the (t, k)-split-allocation is not EFX for (t, k) ∈T, what can we say about the envy? We will show that our design of split allocations is such that it is not possible that agent i < t is envious and agent j > t is envious simultaneously in the (t, k)-split-allocation. We proceed to formal notions.

Definition 6 (Left-envious (LE) and right-envious (RE) allocations). We say that an allocation X is left-envious, or LE (right-envious, or RE), if X is not EFX, and there exists i, j such that agent j envies (up to any item) agent i for i < j (i > j).

We will prove that no (t, k)-split-allocation can have envy in both directions.

Theorem 2. For each (t, k) ∈T, the (t, k)-split-allocation cannot be LE and RE simultaneously.

There are two natural “extremal” cases of split allocations. One case is the (n, m2)-split-allocation, where all goods of the second type are given to agent n. This allocation maximizes the total utility provided by goods of the second type. The other case is when goods of the second type receive the leftmost positions possible for a split allocation. This case is the (t, ⌊m2/(n −t + 1)⌋)-split-allocation, where t ∈[n] minimum possible such that vt,2 ≥1 and m2 ≥n −t + 1 (there can be no (t′, k′) ∈T with t′ < t). Following this logic, we define orderings of split allocations.

(t, k)-reallocation as PEA sum Type

(c)

Quantity

(q)

Agent seq. (a1,..., as) 2 k t 2 m2 −k t + 1,..., n 1 ⌈dvt,2⌉· (t −1) 1,..., t −1 1 ⌈dvt,2⌉−p t

1 m1 −⌈dvt,2⌉· t + p

1,..., ℓ or 1,..., t −1, t + 1,..., ℓ, t

**Table 4.** Expressing (t, k)-reallocation as a series of prioritized equitable allocations.

Definition 7 (Complete ordering of split allocations). A complete linear ordering ≺on the set T is defined by

(t1, k1) ≺(t2, k2)

if and only if t1 < t2 or t1 = t2 and k1 > k2.

The two split allocations described above are naturally maximal and minimal elements in T with respect to ≺. Our second result on envy directions uncovers that these two extremal allocations have specific envy directions (if they are not EFX). Theorem 3 (⋆). Let (tL, kL) be the minimum element in T with respect to ≺. Let (tR, kR) be the maximum element in T with respect to ≺. Both of the following is true: 1. The (tL, kL)-split-allocation is either EFX or LE, 2. The (tR, kR)-split-allocation is either EFX or RE.

Reallocation. To get intuition behind the final concept, assume that none of the split allocations is EFX. Then Theorem 3 guarantees that the (tL, kL)-split-allocation and the (tR, kR)-split-allocation are left-envious and right-envious respectively. Since all split allocations are either LE or RE, there should be (t, k) ∈T such that the (t, k)-splitallocation is LE, while for its immediate successor (w.r.t. ≺) (t′, k′) ∈T, the (t′, k′)-split-allocation is RE. That is, (t, k) and (t′, k′) form a point where the “envy direction changes”.

This can be, for example, (t, k) ∈T for t < n and k ≥2, and (t, k −1) ∈T, such that the (t, k)-split-allocation is LE and the (t, k −1)-split-allocation is RE.

Our final allocation construction slightly transforms such (t, k)-split-allocations by redistributing some goods of the first type from agents to the left of t to agents to the right of t. We now define this construction formally (see also Table 4). Definition 8 ((t, k)-reallocation). For (t, k) ∈T such that t < n and the (t, k)-split-allocation X satisfies m1 ≥⌈d · vt,2⌉· t −p, where p = ⌈kvt,2⌉and d = xt+1,2 = ⌊(m2 −k)/(n −t)⌋, the (t, k)-reallocation is obtained by

1. Start from X, but take away all items of the first type from each agent. 2. Let ℓ∈[n] be maximum possible such that xℓ,2 = d. 3. Give ⌈d · vt,2⌉items of the first type to each agent in [t −1].

16798

<!-- Page 5 -->

4. Give ⌈d · vt,2⌉−p first-type items to agent t. 5. Give the remaining m1 −⌈d · vt,2⌉+ p items of the first type equitably prioritized to:

• Agents 1, 2,..., ℓ, in case ⌈dvt,2⌉−p > (d−k)·vt,2; • Agents 1, 2,..., t −1, t + 1,..., ℓ, t, otherwise.

Note that the definition of (t, k)-reallocations forces additional constraints on (t, k). We will prove the following lemma, that guarantees that (t, k) satisfies these (and other) constraints, if it corresponds to the point of “envy direction change”. Lemma 1 (⋆). Let (t, k), (t′, k′) ∈T be such that the (t, k)split-allocation is left-envious, but (t′, k′)-split-allocation is right-envious. Moreover, there is no (t′′, k′′) ∈T that satisfies (t, k) ≺(t′′, k′′) ≺(t′, k′). Then t < n and

⌈xt+1,2 · vt,2⌉· t −⌈kvt,2⌉+ 1 ≤m1 ≤

⌈xt+1,2 · vt,2⌉· t −⌈(k −1)vt,2⌉.

The final of our results is the following theorem. If combined with Lemma 1, it grants an EFX+PO allocation. Theorem 4 (⋆). Let X be the (t, k)-reallocation for some (t, k) ∈T. If m1 ≤⌈xt+1,2 · vt,2⌉· t −⌈(k −1) · vt,2⌉, then X is EFX+PO.

As discussed before in this section, the Pareto-optimality will follow from the fact that any (t, k)-reallocation is proper. We will prove this fact as a part of the proof of Theorem 4.

The Algorithm We summarize the constructions and properties of the previous section into an algorithm that constructs the desired allocation. It proves, in particular, that EFX+PO allocations always exist for two types of goods, given that all agents’ utilities are positive. Theorem 5. Given preprocessed input, an EFX+PO allocation can be found in O(log n + log m) time.

Proof. We present an algorithm that is based on envy directions of split allocations. Its pseudocode can be found in Algorithm 1, and we will refer to its lines throughout the proof.

We have to clarify first why the algorithm is able to work in logarithmic time, given that even just outputting an allocation (2n integers) takes linear time. In the following claim, we explain why this is possible; moreover, we can even determine whether a split allocation is EFX in constant time.

Claim 1. Given (t, k) ∈T, we can determine in O(1) time whether the (t, k)-split-allocation is EFX, left-envious or right-envious.

Proof of Claim 1. By definition of split allocations, there are b ≤5 distinct bundles that agents receive in the (t, k)split-allocation X. Additionally, there are b contiguous segments of agent numbers [a1, a2−1], [a2, a3−1],..., [ab, n], where a1 = 1 and a1 < a2 <... < ab. Agents within the

## Algorithm

1: The algorithm constructing EFX+PO allocation on preprocessed inputs.

1 tL ←smallest integer in [n] with (tL, ∗) ∈T;

2 XL ←the (tL, ⌊ m2 n−tL+1⌋)-split-allocation;

3 if XL is EFX then return XL;

4 tR ←n;

5 XR ←the (tR, m2)-split-allocation;

6 if XR is EFX then return XR; /* binary search to find t */

7 while tR −tL > 1 do

8 tM ←⌊(tL + tR)/2⌋;

9 XM ←the (tM, ⌊ m2 n−tM+1⌋)-split-allocation;

10 if XM is EFX then return XM;

11 if XM is LE then tL ←tM else tR ←tM;

12 t ←tL and kL ←⌊ m2 n−t+1⌋and kR ←1;

13 if (t, kR)-split-allocation is RE then /* binary search to find k */

14 while kL −kR > 1 do

15 kM ←⌊(kL + kR)/2⌋;

16 XM ←the (t, kM)-split-allocation;

17 if XM is EFX then return XM;

18 if XM is LE then kL ←kM else kR ←kM;

19 k ←kL;

20 else

21 XR ←the (t, kR)-split-allocation;

22 if XR is EFX then return XR; /* LE changes to RE between (t, kR)

and (t + 1, ⌊m2/(n −t)⌋) */

23 k ←kR;

24 return the (t, k)-reallocation.

same segment receive exactly the same bundle. Note that b and a1, a2,..., ab are easily computable in O(1) time from (t, k) following Definition 5, as well as the bundles themselves.

Moreover, if there is envy (up to any item) from agent i to agent j, and agents i −1, i, i + 1 receive exactly the same bundle, then there is necessary envy (up to any item) from agent i −1 to agent j or from agent i + 1 to agent j.

To see the last paragraph, assume agent i envies agent j up to any item. Equivalently, there is a choice of integers z1, z2 ∈{0, 1} such that z1 + z2 = 1 and zc ≤xj,c, and xi,1 + xi,2 · vi,2 < (xj,1 −z1) + (xj,2 −z2) · vi,2, or, equivalently, xi,1 −xj,1 + z1 < (xj,2 −xi,2 −z2) · vi,2. (1)

Since vi−1,2 ≤vi,2 ≤vi+1,2 and xi−1,c = xi,c = xi+1,c for each c ∈[2], we have that (1) holds if we replace i with either i + 1 (if the right part is non-negative), or i −1 (if the right part is negative). Equivalently, either agent i + 1 or agent i −1 envies agent j up to any item.

It follows that there is no need to check whether an agent i with as < i < as+1 −1 envies (up to any item) any other agent. The only agents we have to check are the agents with

16799

<!-- Page 6 -->

numbers in {a1, a2−1, a2,..., ab−1, ab, n}. There are b distinct bundles in X, so for each agent we have to make b −1 comparisons (whether an agent i envies an agent with this specific bundle).

In total, one should make only a total of 2b(b−1) comparisons between agents and bundles. Each comparison is done in constant time. ⌟

We move on to the description of the algorithm itself. The algorithm first evaluates tL from the statement of Theorem 3 (Line 1). Since tL = max{min{t ∈[n]: vt,2 ≥1}, n −m2 + 1}, tL is evaluated in O(log n) time via lower bound binary search over (v1,2, v2,2,..., vn,2).

The other integers from the statement of Theorem 3 are computable in O(1) time, and the algorithm checks whether the (tL, kL)- or the (tR, kR)-split-allocation is EFX (Lines 2-5). If the algorithm does not return here, from Theorem 3 we know that the allocations are LE and RE respectively.

The algorithm then aims to find (t, k) ∈T satisfying Lemma 1. This is done via two binary searches. In the first binary search, the algorithm finds t, and in the second one — the algorithm finds k (given that t is known). During these searches, the algorithm might encounter a split allocation that is EFX. If this happens, the algorithm returns such allocation as its final answer.

We move on to discussion of the first binary search. To perform this search, the algorithm treats tL and tR as binary search bounds and modify them correspondingly, until it reaches tR −tL = 1. It keeps the following invariant: the (tL, ⌊m2/(n −tL + 1)⌋)-split-allocation is LE, and the (tR, ⌊m2/(n −tR + 1)⌋)-split-allocation is RE. In a single iteration of the binary search, the algorithm takes tM in the middle between tL and tR, checks whether the (tM, ⌊m2/(n −tM + 1)⌋)-split-allocation is EFX, LE, or RE, and returns the correct allocation, puts tL equal to tM, or puts tR equal to tM correspondingly (Lines 8-11).

After the binary search, the algorithm puts t:= tL. We know that the desired “envy direction change” point has form (t, k) for some integer k between ⌊m2/(n−t+1)⌋and 1 (because the successor of (t, 1) w.r.t. to ≺is RE). If (t, 1) is right-envious allocation, then the algorithm performs binary search over k starting with kL = ⌊m2/(n−t+1)⌋and kR = 1 in exactly the same way as in the first binary search (Line 14-18). An only little difference from the first binary search is that kL > kR (instead of kL < kR), as imposed by definition of ≺.

If the (t, 1)-split-allocation is not left-envious, then its either EFX (and forms the correct solution), or k = 1 is viable choice for Lemma 1 (Lines 21-23).

In either of the two cases, the algorithm finds (t, k) viable for Lemma 1 (or encounters an EFX split allocation and returns before). The algorithm constructs the (t, k)reallocation and returns it as a final solution (Line 24). This allocation is EFX+PO by Theorem 4.

Similarly to split allocations, the (t, k)-reallocation is found in O(1) time, since there is at most a constant number of bundles given to contiguous segments of agents.

Envy Directions in Split Allocations This section is devoted to properties of envy (up to any item) and envy directions in split allocations. Our main goal is to prove Theorem 2 and Theorem 3, that are fundamental to our algorithm.

Before proceeding, we fomulate split allocations numerically for referencing throughout the proof.

Definition 9 (Numerical definition of split allocations). For (t, k) ∈T, the (t, k)-split-allocation {(xi,1, xi,2)} is given by xi,2 =

   

  

0, if i < t, k, if i = t, q2, if t < i < n −r2, q2 + 1, if i > n −r2, where m2 −k = q2(n −t) + r2 for 0 ≤r2 < n −t, and, for p = ⌈k · vt,2⌉, (a) in case of m1 < p(t −1), xi,1 =

 



0, if i ≥t, q1, if i ≤t −1 −r1, q1 + 1, if i ∈[t −r1, t −1], where m1 = q1 · (t −1) + r1 for 0 ≤r1 < (t −1), (b) in case of m1 ≥p(t −1), xi,1 =

      

     

0, if i > t, q1, if i = t and r1 = 0, q1 + 1, if i = t and r1 > 0, p + q1, if i ≤min{t −r1, t −1}, p + q1 + 1, if i ∈[t −r1 + 1, t −1], where m1 −p(t −1) = q1 · t + r1 for 0 ≤r1 < t.

We start with a series of lemmas. The first simple lemma demonstrates that there can be no envy between agents that go before t or between two agents that go after t in a (t, k)split-allocation.

Lemma 2 (⋆). Let X be a (t, k)-split-allocation for (t, k) ∈ T. If there is envy (up to any item) between agents i < j in X for i, j ∈[n], then i ≤t and j ≥t.

The next lemma restricts any left-envious (LE) split allocation to the case (b) from Definition 9 of split allocations.

Lemma 3 (⋆). Let X be the (t, k)-split-allocation for (t, k) ∈T. If X is LE, then m1 ≥p · (t −1), where p = ⌈k · vt,2⌉.

The final lemma in the series explains that m1 ≥p(t −1) also rules out envies between any agent i < t and agent t.

Lemma 4 (⋆). Let X be the (t, k)-split-allocation for (t, k) ∈T, and let p = ⌈k · vt,2⌉. If m1 ≥p · (t −1), then for each i ∈[t −1] there is no envy (up to any item) between agent i and agent t in X.

We are ready to prove our main result on envy directions in split allocations, Theorem 2. For convenience of the reader, we restate it here first.

16800

<!-- Page 7 -->

Theorem 2. For each (t, k) ∈T, the (t, k)-split-allocation cannot be LE and RE simultaneously.

Proof. Targeting towards a contradiction, assume that there exists (t, k) ∈T such that the (t, k)-split-allocation X = {(xi,1, xi,2)} is LE and RE simultaneously.

By Lemma 3, we know that m1 ≥p · (t −1) holds for p = ⌈xt,2 · vt,2⌉. In particular, X comes from case (b) of Definition 9. Then, by Lemma 4 we have that there is no envy (up to any item) between any agent i ∈[t−1] and agent t in X. Consequently, if there is an envy between agent i and agent j in X, where i < j, then i ≤t and j > t necessarily holds.

Under the initial assumption that X is LE and RE simultaneously, we prove two contraversary claims. Recall that q1 and r1 from Definition 9 of split allocations are non-negative integers satisfying m1 = q1·(t−1)+r1. Similarly, q2 and r2 are two positive integers that satisfy m2−k = q2·(n−t)+r2.

The first claim comes from X being right-envious.

Claim 2. Both of the following is true:

• If r1 > 0, then p + q1 < q2 · vt,2. • If r1 = 0, then vt,2 · xt,2 + q1 < q2 · vt,2.

Proof of Claim 2. Since X is right-envious, there is an agent i ∈[t] that envies (up to any item) some agent j ∈[t+1, n]. There are two cases depending on whether i < t or i = t.

If i < t, then agent i has no items of the second type, and agent j has no items of the first type. The envy from agent i to agent j is equivalent to xi,1 + 1 · vi,2 < xj,2 · vi,2. From Definition 9 we have that xi,1 ≥p + q1 and xj,2 ≤q2 + 1. Consequently, p + q1 + vi,2 < (q2 + 1) · vi,2. It follows p + q1 < q2 · vi,2 ≤q2 · vt,2, since vi,2 ≤vt,2.

We have that if i < t, then p + q1 < q2 · vt,2. Since p ≥ k ·vt,2 = xt,2 ·vt,2, it also follows vt,2 ·xt,2 +q1 < q2 ·vt,2. Therefore, both parts of the claim follow if i < t.

We now consider the case when agent t envies (up to any item) agent j > t. The envy is equivalent to xt,1 + (xt,2 + 1) · vt,2 < xj,2 · vt,2.

Recall that xj,2 ≤q2 + 1 and rewrite the above as xt,1 + xt,2 · vt,2 < q2 · vt,2. (2)

If r1 = 0, then xt,1 = q1, and (2) becomes xt,2 · vt,2 + q1 ≤q2 · vt,2, as required by the first part of the claim statement.

If r1 > 0, then xt,1 = q1 + 1. Then, by p < xt,2 · vt,2 + 1 and (2) obtain p + q1 < xt,2 · vt,2 + 1 + q1 ≤xt,1 + xt,2 · vt,2 < q2 · vt,2.

This proves the second part of the claim statement. This concludes the proof of the claim. ⌟

The second claim comes from X being left-envious.

Claim 3. Both of the following is true:

• If r1 > 0, then p + q1 > q2 · vt,2. • If r1 = 0, then vt,2 · xt,2 + q1 > q2 · vt,2.

Proof of Claim 3. Since X is left-envious, there is an agent j > t that envies some agent i ∈[t]. There are two cases depending on whether i < t or i = t.

Consider first the case when i < t. The envy from agent j to agent i is then equivalent to 1 + xj,2 · vj,2 < xi,1. We have that xj,2 ≥q2 from definition of X, and vj,2 ≥vt,2 since j > t. Combining the inequalities, obtain q2 · vt,2 < xi,1 −1. (3)

If r1 > 0, then xi,1 ≤p + q1 + 1. Then (3) gives q2 · vt,2 < p + q1 + 1 −1, which is essentially the first part of the claim. If r1 = 0, then xi,1 = p + q1. Combining this, (3) and vt,2 · xt,2 > p −1 gives q2 · vt,2 < (p −1) + q1 < vt,2 · xt,2 + q1.

The second part is also proved for case i < t.

We move on to the remaining case i = t. The envy from agent j to agent t is then expressed as 1 + xj,2 · vj,2 < xt,1 + xt,2 · vt,2. Similarly to the previous case, rewrite this as q2 · vt,2 < (xt,1 −1) + xt,2 · vt,2. (4)

If r1 > 0, xt,1 = q1 + 1. Combining this, (4) and p ≥ xt,2 · vt,2 gives the first part of the claim. If r1 = 0, then xt,1 = q1. Combining (4) with xt,1 = q1 gives q2 · vt,2 < q1 −1 + xt,2 · vt,2 < q1 + xt,2 · vt,2.

The proof of the case i = t and the whole claim is complete. ⌟

Clearly, Claim 2 and Claim 3 are controversial statements that are both true under the initial assumption. The obtained contradiction proves the theorem.

While Theorem 2 is fundamental to our split allocation approach, Theorem 3 is pivotal to the binary search over T. The proof of Theorem 3 is omitted due to the space constraints and can be found in the appendix.

## Conclusion

In this work, we have made progress in understanding the existence and computability of EFX+PO allocations, establishing that such allocations always exist for two types of goods with positive utilities and developing an efficient O(n log n + log m)-time algorithm. We are interested in whether these results can be extended to several simple independent cases of a more general open question. It represents critical next steps in the broader research aimed at characterizing when EFX and EFX+PO allocations are guaranteed to exist.

Open Question 1. Does an EFX allocation always exist? Does an EFX+PO allocation always exists when all utilities are positive? At least in two settings:

(a) utility matrix has rank 2, (b) three types of goods.

16801

<!-- Page 8 -->

## Acknowledgments

Yuriy Dementiev, Artur Ignatiev and Danil Sagunov: This work was supported by the Ministry of Economic Development of the Russian Federation (IGK 000000C313925P4C0002), agreement №139-15-2025-010.

## References

Amanatidis, G.; Aziz, H.; Birmpas, G.; Filos-Ratsikas, A.; Li, B.; Moulin, H.; Voudouris, A. A.; and Wu, X. 2023. Fair division of indivisible goods: Recent progress and open questions. Artificial Intelligence, 322: 103965. Amanatidis, G.; Birmpas, G.; Filos-Ratsikas, A.; Hollender, A.; and Voudouris, A. A. 2021. Maximum Nash welfare and other stories about EFX. Theoretical Computer Science, 863: 69–85. Amanatidis, G.; Filos-Ratsikas, A.; and Sgouritsa, A. 2024. Pushing the Frontier on Approximate EFX Allocations. In Bergemann, D.; Kleinberg, R.; and Sab´an, D., eds., Proceedings of the 25th ACM Conference on Economics and Computation, EC 2024, New Haven, CT, USA, July 8-11, 2024, 1268–1286. ACM. Amanatidis, G.; Markakis, E.; and Ntokos, A. 2020. Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle elimination. Theor. Comput. Sci., 841: 94– 109. Aziz, H.; Li, B.; Moulin, H.; and Wu, X. 2022. Algorithmic fair allocation of indivisible items: a survey and new questions. SIGecom Exch., 20(1): 24–40. Berger, B.; Cohen, A.; Feldman, M.; and Fiat, A. 2022. Almost Full EFX Exists for Four Agents. In Thirty-Sixth AAAI Conference on Artificial Intelligence, AAAI 2022, Thirty- Fourth Conference on Innovative Applications of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022, 4826–4833. AAAI Press. Budish, E. 2011. The Combinatorial Assignment Problem: Approximate Competitive Equilibrium from Equal Incomes. Journal of Political Economy, 119(6): 1061 – 1103. Caragiannis, I.; Gravin, N.; and Huang, X. 2019. Envy- Freeness Up to Any Item with High Nash Welfare: The Virtue of Donating Items. In Karlin, A. R.; Immorlica, N.; and Johari, R., eds., Proceedings of the 2019 ACM Conference on Economics and Computation, EC 2019, Phoenix, AZ, USA, June 24-28, 2019, 527–545. ACM. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A.; Shah, N.; and Wang, J. 2019. The Unreasonable Fairness of Maximum Nash Welfare. ACM Transactions on Economics and Computation, 7: 1–32. Chaudhury, B. R.; Garg, J.; and Mehlhorn, K. 2024. EFX Exists for Three Agents. J. ACM, 71(1): 4:1–4:27. Chaudhury, B. R.; Kavitha, T.; Mehlhorn, K.; and Sgouritsa, A. 2021. A Little Charity Guarantees Almost Envy- Freeness. SIAM J. Comput., 50(4): 1336–1358. Foley, D. K. 1966. Resource allocation and the public sector. Yale University.

Garg, J.; and Murhekar, A. 2023. Computing fair and efficient allocations with few utility values. Theoretical Computer Science, 962: 113932. Ghosal, P.; HV, V. P.; Nimbhorkar, P.; and Varma, N. 2025. (Almost Full) EFX for Three (and More) Types of Agents. In Walsh, T.; Shah, J.; and Kolter, Z., eds., AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA, 13889–13896. AAAI Press. Gorantla, P.; Marwaha, K.; and Velusamy, S. 2023. Fair allocation of a multiset of indivisible items. In Bansal, N.; and Nagarajan, V., eds., Proceedings of the 2023 ACM-SIAM Symposium on Discrete Algorithms, SODA 2023, Florence, Italy, January 22-25, 2023, 304–331. SIAM. Hosseini, H.; Sikdar, S.; Vaish, R.; and Xia, L. 2021. Fair and Efficient Allocations under Lexicographic Preferences. In Thirty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2021, Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021, The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI 2021, Virtual Event, February 2-9, 2021, 5472–5480. AAAI Press. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On Approximately Fair Allocations of Indivisible Goods. In Proceedings of the 5th ACM Conference on Electronic Commerce, EC ’04, 125–131. New York, NY, USA: Association for Computing Machinery. ISBN 1581137710. Mahara, R. 2023. Existence of EFX for two additive valuations. Discrete Applied Mathematics, 340: 115–122. Mahara, R. 2024. Extension of Additive Valuations to General Valuations on the Existence of EFX. Math. Oper. Res., 49(2): 1263–1277. Nguyen, T. T.; and Rothe, J. 2023. Complexity Results and Exact Algorithms for Fair Division of Indivisible Items: A Survey. In Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, IJCAI 2023, 19th-25th August 2023, Macao, SAR, China, 6732– 6740. ijcai.org. Plaut, B.; and Roughgarden, T. 2020. Almost Envy-Freeness with General Valuations. SIAM J. Discret. Math., 34(2): 1039–1068. Prakash HV, V.; Ghosal, P.; Nimbhorkar, P.; and Varma, N. 2025. EFX Exists for Three Types of Agents. In Ashlagi, I.; and Roth, A., eds., Proceedings of the 26th ACM Conference on Economics and Computation, EC 2025, Stanford University, Stanford, CA, USA, July 7-10, 2025, 101–128. ACM.

16802
