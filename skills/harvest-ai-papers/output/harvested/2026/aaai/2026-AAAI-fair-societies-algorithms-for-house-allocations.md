---
title: "Fair Societies: Algorithms for House Allocations"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38753
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38753/42715
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Fair Societies: Algorithms for House Allocations

<!-- Page 1 -->

Fair Societies: Algorithms for House Allocation

Hadi Hosseini1, Sanjukta Roy2, Aditi Sethia3

1Pennsylvania State University, USA 2Indian Statistical Institute, Kolkata 3Indian Institute of Science, Bangalore hadi@psu.edu, sanjukta@isical.ac.in, aditisethia@iisc.ac.in

## Abstract

House allocations concern with matchings involving onesided preferences, where houses serve as a proxy encoding valuable indivisible resources (e.g. organs, course seats, subsidized public housing units) to be allocated among the agents. Every agent must receive exactly one resource. We study algorithmic approaches towards ensuring fairness in such settings. Minimizing the number of envious agents is known to be computationally hard. We present two tractable approaches to deal with the hardness. When the agents are presented with an initial allocation of houses, we aim to refine this allocation by reallocating a bounded number of houses to reduce the number of envious agents. We show an efficient algorithm when the agents express preference for a bounded number of houses and houses are accepted by a bounded number of agents. Next, we consider single peaked preference domain and present a polynomial time algorithm for finding an allocation that minimize the number of envious agents. We further extend it to satisfy Pareto efficiency. Our former algorithm works for other measures of envy such as total envy, or maximum envy, with suitable modifications. Finally, we present an empirical analysis recording the fairness-welfare trade-off of our algorithms.

Code — https://github.com/anonymous1203/FairSocieties

## Introduction

The problem of house allocation comprises of a set H of m houses to be allocated to a set N of n agents with preferences (cardinal utilities or rankings) such that every agent gets exactly one house. Such one-sided matching problems appear in a wide range of domains, from economic housing markets (Shapley and Scarf 1974) and logistical tasks such as dormitory or course-seat allocations among students (Budish 2011) to critical healthcare domains like allocating donor kidneys among patients (Caragiannis, Filos-Ratsikas, and Procaccia 2015). The rapid integration of automated decision-making processes has made the question of fairness in one-sided matching problems more relevant than ever.

The gold standard of fairness is envy-freeness, where no agent envies the houses allocated to any other agent. In particular, they prefer their allocated house more than any

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

other allocated house. Gan, Suksompong, and Voudouris (2019) demonstrated that if such an envy-free allocation exists, it can be computed efficiently. However, such allocations may not even exist, making it imperative to minimize the unavoidable envy. A few objectives of interest that are studied in the literature (see Aigner-Horev and Segal- Halevi (2021); Kamiyama, Manurangsi, and Suksompong (2021); Madathil, Misra, and Sethia (2025)) are as follows: minimizing the sum of envy experienced by all the agents (TotalEnvy), the number of envious agents (Envy), and the maximum envy experienced by any agent (MaxEnvy). Interestingly, the latter two are known to be NP-hard1 to compute even for binary valuations (Kamiyama, Manurangsi, and Suksompong 2021) and for weak ordinal preferences (Madathil, Misra, and Sethia 2025), while the complexity of the former is not known in general.

## 1.1 Our Contributions

In this work, we focus on minimizing the number of envious agents (Envy). The computational question of minimizing the number of envious agents is notoriously hard. It is hard to approximate to within a factor of n1−γ for any constant γ > 0 where n is the number of agents (Kamiyama, Manurangsi, and Suksompong 2021), and the exact computation is W[1]-hard with respect to the minimum number of envious agents, even for binary preferences of length three or ordinal preferences (Madathil, Misra, and Sethia 2025). Towards tractability, we ask: “given an allocation, is it possible to modify it in order to move closer to a fair allocation minimizing Envy?” Hosseini, Kumar, and Roy (2024) proposed to focus on finding fair solutions within the space of all efficient solutions; these are primarily tractable, however, they can be far from optimal fair solutions. To reach closer to an optimal allocation, we propose an approach that focuses on refining a given allocation via reallocating houses to achieve fairness, by sequentially expanding the search space. The benefits are (i) to the best of our knowledge, it is the first tractable approach in the general setting (ii) it allows control over how much reallocation is required or desirable.

Fixed Parameter Tractability. Given an allocation, we propose a generic refinement framework via reallocations that enables computation of fairer allocations. To this end,

1If m ≤n, the problems are easy (Hosseini et al. 2024).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17050

<!-- Page 2 -->

we design a fixed-parameter tractable (FPT)2 algorithm for the following decision problem: given an allocation ˆA and non-negative integers k and q, can ˆA be refined to an allocation A such that Envy reduces by at least k with at most q reallocations (Theorem 1). The parameter is q + d, where d is the maximum degree of any vertex in the associated preference graph. It is relevant to note that our framework is measure-oblivious, and works for any measure of envy – Envy, TotalEnvy or MaxEnvy (Theorem 2).

In a housing market with a large number of houses (i.e., m is large), it is likely that d is small as it is infeasible for an agent to express its preference over all the houses. Agents’ approvals of houses are also restricted by locations. A house in upstate wouldn’t be approved by all those who want to live in Manhattan, while a house in Manhattan won’t be liked by someone looking for a peaceful, cheaper, and bigger residence. Additionally, certain markets, such as Singapore’s Housing Development Board, also impose quota constraints, wherein each housing project must hold a certain percentage of every major ethnic group (Benabbou et al. 2018, 2020). Consequently, a Chinese applicant may rank a flat in an 87% Chinese neighborhood lower, recognizing that the ethnic quota renders her ineligible for it. Also, implementing a large number of reallocations can be practically challenging, thereby, justifying the choice of our parameters.

Polynomial Time Algorithms. Given that minimizing Envy is hard even for weak ordinal rankings, in search for tractability, we explore single-peaked and single-dipped preferences. These constitute an important preference domain in decision-making problems, which not only model many real-world settings including house allocations and matching markets (Bade 2019; Beynier et al. 2021; Tamura 2023) but also serve as a tractable realm for many hard problems, albeit not always (Faliszewski et al. 2009). In many cases agents’ housing preferences are influenced by availability of facilities. For example, elderly individuals may prioritize houses near a hospital, while couples with children might prefer houses closer to a school. The value they assign to a house decreases as its distance from their preferred location increases, producing single peaked preferences. We show that for single-peaked/dipped preferences, an allocation with minimum Envy can be found in polynomial time (Theorems 3 and 4). Focusing on efficiency, we observe that, although, a Pareto optimal (PO) allocation may not be compatible with minimizing Envy, we can decide the existence in polynomial time. We also present structural properties for single-peaked and single-dipped preferences.

Experiments. Our empirical analysis is done on synthetic data with cardinal preferences. It shows the effects of reallocations on welfare loss and Envy, and how quickly we can converge (based on the values of q) to an optimal allocation given various initial allocations with welfare guarantees such as Nash (geometric mean of agents’ utilities) or egalitarian (minimum utility of any agent) welfare. We average

2An FPT algorithm with respect to a parameter ℓruns in time f(ℓ)(n + m)O(1) for a computable function f.

over 100 instances with 6 agents and 11 houses and record (i) the loss in welfare and (ii) the decrease in Envy as we increment the number of reallocations q from 1 to n. We also implement our algorithms for single-peaked/dipped preferences and observe that the welfare loss due to minimizing Envy is insignificant when cardinal preferences conform to these structures.

## 1.2 Additional Related Work

House allocations have been studied since early 1970s with various models: existing tenants (Shapley and Scarf 1974), and new applicants (Hylland and Zeckhauser 1979; Abdulkadiro˘glu and S¨onmez 1999). The concept of fairness in house allocations is more recent and was first explored by Beynier et al. (2019); Kamiyama, Manurangsi, and Suksompong (2021); Madathil, Misra, and Sethia (2025); Hosseini, Kumar, and Roy (2024). Aigner-Horev and Segal-Halevi (2021) looked into a relaxed variant where each agent receives at most one house and developed an efficient algorithm to find an envy-free matching of maximum cardinality under binary utilities. Shende and Purohit (2020) examined the interplay between envy-freeness and strategy-proofness. Minimization of various envy measures across all edges in an underlying graph on agents has also been looked at (Hosseini et al. 2023, 2024; Dey et al. 2025). Choo et al. (2024) discussed envy-free house allocations in relation to subsidies. Adjusting a given allocation for achieving fairness was studied by He et al. (2019); Friedman, Psomas, and Vardi (2015, 2017) for online fair division settings. Single-peaked preferences were first formalized by Black (1948). A significant literature in social choice has also focused on characterizing single-peaked preferences (Ballester and Haeringer 2011; Elkind, Faliszewski, and Skowron 2020; Puppe 2018) and they have been studied for domains like voting and electorates (Conitzer 2007; Faliszewski et al. 2009; Sprumont 1991) among others. For more details, we refer the reader to the survey of preference restrictions in social choice (Elkind, Lackner, and Peters 2022).

## Preliminaries

We denote the set of integers {1,..., t} by [t]. An instance of the house allocation problem with ordinal preferences is given by I = (N, H, ⪰), where N is a set of n agents, H is a set of m houses, and ⪰= {⪰i |i ∈N} is the ranking profile with ⪰i being the ranking of agent i over (possibly, a subset of) houses H. We assume m > n. We use h ⪰i h′ to denote agent i prefers houses h and h′ equally, otherwise we use h ≻h′.

Allocations. An allocation A: N →H is an injective mapping from the set N of agents to the set H of houses where each agent gets exactly one house. The house allocated to agent i under the allocation A is denoted by A(i). For two allocations A and A′, we use A∆A′ to denote their symmetric difference.

Fairness. Given an allocation A, we say that agent i envies agent j if i ranks j′s house better than its own house, i.e., A(j) ≻i A(i). The pairwise envy is defined as

17051

<!-- Page 3 -->

envyi,j(A):= I[A(j) ≻i A(i)] where I denotes the indicator function which is one if the condition is satisfied and zero otherwise. The amount of envy experienced by i is given by envyi(A):= P j̸=i envyi,j(A). An allocation A is envyfree (EF) if for every agent i ∈N we have envyi(A) = 0. Given an allocation A, we denote by E(A) the set of all envious agents. That is, E(A) = {i ∈N|envyi(A) > 0}. We consider the problem of minimizing the number of envious agents (Envy) in an allocation A. Formally, Envy(A):= |E(A)|. The total envy of an allocation A is defined as the sum of the amount of envy experienced by all the agents: TotalEnvy(A):= P i∈E(A) envyi(A). Likewise, the maximum envy of an allocation A is the maximum envy experienced by any agent: MaxEnvy(A):= maxi∈E(A) envyi(A).

Efficiency. An allocation A is said to be Pareto dominated by another allocation A′ if at least one agent gets a strictly better house and no agent gets worse-off under A′. A Pareto optimal allocation is not Pareto dominated by any allocation. All the missing proofs are deferred to the full version (Hosseini, Roy, and Sethia 2025).

Refining Fairness: A Parameterized

## Algorithm

Kamiyama, Manurangsi, and Suksompong (2021) showed that we cannot design a polynomial time algorithm to find a minimum Envy allocation for binary preferences, unless P = NP. Furthermore, it cannot have an FPT algorithm with respect to the number of envious agents k even for weak ordinal preferences, (Madathil, Misra, and Sethia 2025). We design a FPT algorithm that, given an initial allocation ˆA, computes the “best” allocation that is at most q reallocations away from ˆA, parameterized by q and the degree of the preference graph. We first state the main result of this section.

Theorem 1. Given an instance I = (N, H, ⪰) of house allocation, a complete allocation ˆA, and two positive integers k and q, deciding if there is an allocation A such that Envy(A) ≤Envy(ˆA) −k and |A ∆ˆA| ≤q admits an algorithm that runs in time O∗(33q(d+1)) (randomized) or O∗(8qd log(3q(d+1)) (deterministic), where d is the maximum degree of any vertex in the associated preference graph G.

Intuition and Challenges. Our algorithm starts with an allocation ˆA. To find an allocation with reduced Envy from an initial allocation, arguably, the most employed technique is to iteratively eliminate envy cycles. An envy cycle is a directed cycle of agents where each agent envies its outneighbor. To eliminate a cycle, each agent gives her house to the previous agent (who envies her) on the cycle. Envy can be further reduced by unallocating some houses and reallocating their occupants to currently unallocated houses. These reallocations can be systematically done using ˆAalternating paths. An ˆA-alternating path starts at an unallocated house, continues with a sequence of allocated agenthouse pairs, and ends at an allocated house. Thus, changing the allocation along an alternating path unallocates one house and reallocates all the agents on the path. In order to make an envious agent envy-free, we may need to unallocate multiple houses simultaneously (see Example 1). The challenge is to identify the paths and the subset of houses to be allocated (a minimal improvement set as in Definition 2). If we need to identify multiple paths that reallocate some q ∈[n] agents on the paths, a brute-force algorithm takes time mO(q) to find the agents and another O(qd) to identify the houses on the paths, where d is the maximum number of houses in an agent’s preference list. We design an algorithm that finds the minimum Envy that can be achieved by at most q reallocations from ˆA, and runs in time 3O(qd) which is significantly better when m is large (note m > n, more discussion deferred to the full version). If a few agents require reallocation in ˆA, then we can converge to an optimal allocation faster (for small q).

Notations. The preference graph G is the bipartite graph between agents and houses, i.e., G = (N ∪H, E) where E = {(i, h): agent i ranks house h}. Let A be an allocation. Then A is a matching in G. An A-alternating path P is a path in G whose edges alternate between allocated and non-allocated edges. We call it an A-alternating cycle if it starts and ends at the same vertex. Then, for an A-alternating path/cycle P, we define A ⊕P as the allocation obtained from A by removing the edges that appear in both A and P, and adding the edges in P that do not appear in A. If X = {P1,... Ps} is a collection of s alternating paths and cycles, then A ⊕X = A ⊕P1 ⊕... ⊕Ps. Suppose that X induces a component C in G. Then, we slightly abuse the notation to write A ⊕C instead of A ⊕X. On the other hand, given two allocations A and ˆA, the symmetric difference, denoted by A ∆ˆA is a set of ˆA-alternating path(s) and cycle(s) in G (that are also A-alternating path(s) and cycle(s), respectively in G). See Example 1.

Example 1. Consider the following instance with 5 agents and 8 houses. The allocation ˆA = {(iz, hz)|z ∈[5]} is a complete allocation. Note that Envy(ˆA) = 5. There are no envy cycles. Three ˆA-alternating paths are P1 = (h8, i1, h1, i2, h2), P2 = (h7, i3, h3, i4, h4), and P3 = (h6, i5, h5). Furthermore, for each Pz, z ∈[3], it holds that Envy(ˆA ⊕Pz) = Envy(ˆA) = 5. Let A = ˆA ⊕ P1 ⊕P2 ⊕P3. Then, A∆ˆA = {P1, P2, P3}, and A = {(i1, h8), (i2, h1), (i3, h7), (i4, h3), (i5, h6)}. Surprisingly, Envy(A) = 0.

i1: h5 ⪰h2 ⪰h4 ≻h8 ≻h1 i2: h5 ⪰h4 ≻h2 ≻h1 ≻h8 i3: h5 ⪰h2 ≻h4 ≻h7 ≻h3 i4: h5 ⪰h2 ≻h4 ≻h3 ≻h7 i5: h2 ⪰h4 ≻h5 ≻h6 ≻h1

Therefore, we conclude that

Envy(A) < Envy(ˆA) +

X i=1

Envy-drop(ˆA, Pi).

where Envy-drop(ˆA, Pi) = Envy(ˆA) −Envy(ˆA ⊕Pi) denotes the decrease in number of envious agents in ˆA ⊕Pi compared to ˆA.

17052

<!-- Page 4 -->

## Algorithm

1: Reduce Envy by k with at most q reallocations

Input: (N, H, ⪰), an allocation ˆA, k, q ∈Z≥0 Output: An allocation A with Envy(A) = Envy(ˆA) −k and |A ∆ˆA| ≤q. 1: Construct a bipartite graph G = (N ∪H, E) where (i, h) ∈E if i ranks h for i ∈N and h ∈H. 2: Let χ be a coloring of the vertices and edges of G with three colors red, green, and blue uniformly at random. 3: Let EB = {e ∈E|χ(e) = blue}, and C be the connected components of G −EB. 4: for C ∈C do 5: if C is not feasible, then delete C 6: end for 7: for C ∈C do 8: rC:= Envy(ˆA) −Envy(ˆA ⊕C) 9: nC:= number of agents in C 10: end for 11: Using knapsack algorithm find a subset X of C such that P

C∈X rC ≥k and P

C∈X nC ≤q

12: return A = ˆA ⊕X

Overview of Algorithm 1. Our algorithm works in two phases. In the first phase, we identify a class C of subsets of ˆA-alternating paths and cycles (via randomized coloring or universal set family) such that we can reach the desired allocation using some subsets from C. In the second phase, we begin by deleting the components in C that are not feasible (Definition 3). Then, we identify minimal improvement sets, (Definition 2) of C such that the number of envious agents decreases by k and no more than q agents’ allocations are changed. Towards this, let C ∈C be a feasible component. Then, C contains a set of ˆA-alternating paths and cycles. We denote the decrease in the number of envious agents Envy(ˆA) −Envy(ˆA ⊕C) as rC. Note that rC can be negative if the number of envious agents in ˆA ⊕C is more than that of ˆA. Additionally, nC denotes the number of reallocated agents in ˆA⊕C. Finally, we solve a knapsack on C using rC as profit and nC as cost to obtain a desired allocation. We begin with some definitions.

Definition 1 (Dependent Set). Let ˆA be a complete allocation. A subset T = {T1, T2,... Tt} of ˆA-alternating paths/cycles is said to be dependent if Envy(ˆA ⊕T1 ⊕... ⊕Tt)̸ = Envy(ˆA) −P ℓ∈[t](Envy(ˆA) −Envy(ˆA ⊕Tℓ)).

Definition 2 (Minimal Improvement Set). Let T be a set of pairwise disjoint ˆA-alternating paths/cycles. A subset S ⊆T is an improvement set for ˆA if there exists a positive integer k such that for each subset S′ ⊆T \S and some integer k′, it holds that (i) Envy(ˆA⊕S) = Envy(ˆA)−k, (ii) Envy(ˆA⊕S′) = Envy(ˆA)−k′, and (iii) Envy(ˆA⊕S⊕S′) = Envy(ˆA)−(k+k′). Further, subset S ⊆T is a minimal improvement set if no subset of S is an improvement set.

In Example 1, set {P1, P2, P3} is the only improvement set and thus it is minimal. In Observation 1-Lemma 4, we prove properties of a minimal improvement set that will be helpful in our proof. Observation 1 follows from the definition.

Observation 1. Let S be a minimal improvement set for

ˆA. Then, every path/cycle in S is dependent on at least one other path/cycle in S.

We show that if Envy(ˆA) is not minimum, then an improvement set exists for the allocation ˆA.

Lemma 1. Let A and ˆA be two allocations. Then, Envy(ˆA) −k = Envy(A) for some k > 0 if and only if S is an improvement set, where S is the set of alternating paths and cycles in A ∆ˆA.

Next, we prove some properties of an improvement set relating it to the preference graph G.

Lemma 2. For any minimal improvement set S for an allocation ˆA, the graph G[V (S)] is connected.3

Separation of Paths / Cycles. A coloring χ: V (G) ∪ E(G) →{red, green, blue} is a good coloring if the following events hold true.

1. Each agent i, house h, and the edge (i, h) that appears in a path or cycle in A ∆ˆA is colored red. That is, if (i, h) is in T, it is colored red. We have, χ(i) = χ(h) = χ(i, h) = red ∀i, h, (i, h) ∈E(T). 2. Let S be a minimal improvement set. Then each edge (i, h) in G incident to two vertices of S such that (i, h) /∈ T is colored green. That is, χ(i, h) = green ∀(i, h) /∈ T, i ∈S, h ∈S. 3. Let S be a minimal improvement set. Each edge (i, h) in G where either agent i or house h is in S but not both i and h are in S, is colored blue. That is, χ(i, h) = blue ∀i ∈S, h /∈S or i /∈S, h ∈S. The edges in G that is colored blue is denoted by EB.

Lemma 3. Given a coloring χ, the probability that χ is a good coloring is at least 3−3q(d+1).

Thus, we get a good coloring with high probability if we repeat the above algorithm 33q(d+1) times.

Definition 3 (Feasible Components). We say that a component C ∈C is not feasible if any of the following holds true. (1) There exists a green or blue vertex in C. (2) The graph induced by the red vertices and edges in C is not a disjoint union of ˆA-alternating paths/cycles. (3) There exists an edge in G between two vertices of C that is colored blue. (4) component C is dependent, that is, there exists another component C′ ∈C such that Envy(ˆA⊕C)−Envy(ˆA) = k1, Envy(ˆA ⊕C′) −Envy(ˆA) = k2, and Envy(ˆA ⊕C ⊕C′) − Envy(ˆA) < k1 + k2. A component C is feasible otherwise.

Equipped with the definitions of good coloring and feasible component, we finally prove that each minimal improvement set in A ∆ˆA is a feasible connected component in C.

3G[V (S)] is the preference graph on V (S) (vertices of S).

17053

<!-- Page 5 -->

Lemma 4. Let S be any minimal improvement set in A ∆ˆA. Then, in a good coloring, the graph G[V (S)] is a single component in C. Moreover, it is a feasible component.

We are now ready to argue the correctness of Theorem 1.

Proof Sketch of Theorem 1. Suppose that we have a good coloring χ for the graph G. Then, Lemma 4 ensures that every minimal improvement set is a connected and feasible component in C. We show that once we have the feasible components in C, we need to choose a collection C′ ⊆C of components such that P

C∈C′ rC ≥k and P

C∈C′ nC ≤q. Note that this is exactly the classical knapsack problem with q as the maximum admissible weight and k as the minimum required profit. In particular, the input to the knapsack problem is ⟨C, r1, r2,..., r|C|, n1, n2,... n|C|, q, k⟩and goal is to decide if there is a subset X ⊆C such that P

C∈X nC ≤q and P

C∈X rC ≥k. We defer the proof of equivalence to the full version. The knapsack problem can be solved in time O(|C|q) = O(nq) (Kellerer, Pferschy, and Pisinger 2004). For the randomized algorithm, a good coloring is obtained with high probability by repeating the step 33q(d+1) times. Thus, total time taken is O((n + m)2 · 33q(d+1)). A derandomization of Algorithm 1 and its run time analysis is presented in the full version.

We now show that Algorithm 1 is oblivious to the measure of envy under consideration. It can be suitably adapted for total envy or maximum envy of an allocation. In fact, it works for “cardinal preferences” as well by only modifying Line 1 of Algorithm 1 to define the edge set of preference graph G as follows: (i, h) ∈E if agent i has a non-zero, positive value for house h for i ∈N and h ∈H.

Theorem 2. Given an instance I = (N, H, V) of house allocation, a complete allocation ˆA, and two positive integers k and q, deciding if there is an allocation A such that TotalEnvy(A) ≤TotalEnvy(ˆA) −k (or MaxEnvy(A) ≤ MaxEnvy(ˆA) −k) and |A ∆ˆA| ≤q admits a fixedparameter tractable algorithm parameterized by q and d, where d is the maximum degree of any vertex in the associated preference graph G.

## 4 Restricted Domain: Efficient Algorithms

In this section, we present efficient algorithms for minimizing Envy when the rankings over H are complete, strict, and single-peaked/dipped. We first present the definitions. We say h is a peak house for agent i, denoted as peak(i) if h is the first-ranked house for i. That is, h ≻i h′ for each h′̸ = h.

Definition 4 (Single-Peaked Preferences). A preference ranking ≻i is single-peaked with respect to an ordering ✄ of houses H if for every pair of houses h, h′ ∈H, we have that if h ✄h′ ✄peak(i) or peak(i) ✄h′ ✄h, then h′ ≻i h. A preference profile ≻is single-peaked if there exists an ordering ✄over H such that ≻i is single-peaked with respect to ✄for every agent i ∈N (see Figure 1).

Intuitively, in single-peaked preferences, as an agent moves away from his favorite house peak(i) in the ordering ✄in any direction, left or right, the houses become less preferable for her. Likewise, under single-dipped preferences, there is an ordering ✄on the houses such that for any agent i, there is a least preferred house h, called a dip(i), and she prefers the houses better as she moves away from h in either direction with respect to the ordering ✄. Formally,

Definition 5 (Single-Dipped Preferences). A preference ranking ≻i is single-dipped with respect to an ordering ✄ of houses H if for every pair of houses h, h′ ∈H, h ✄h′ ✄ dip(i) or h ✄h′ ✄dip(i), implies h ≺i h′. A preference profile ≻is single-dipped if there exists an ordering ✄over H such that ≻i is single-dipped with respect to ✄for every i ∈N.

We now state the main result of this section, and set the notations that will be helpful in the proof.

Theorem 3. Given a single-peaked instance I = (N, H, ≻, ✄), minimizing the number of envious agents admits a polynomial time algorithm with run time O(|H|2).

Notations. For a house h, we denote the set of agents who prefer it to all other houses as base(h). That is, base(h) = {i ∈N | h ≻i h′ for all h′̸ = h} = {i ∈N | h = peak(i)}. Suppose that the set of rankings ≻are single-peaked with respect to the ordering ▷over the houses (h1 ▷h2 ▷... ▷hm). The interval [hi, hj) denotes the set of houses hi ▷... ▷hj−1. We say that a house h is a shared peak if it is the most preferred house of more than one agent, that is, |base(h)| > 1. Otherwise, if base(h) = 1, we say it is an individual peak. We say that a house h is non-wastefully allocated if it is allocated to an agent in base(h), otherwise it is allocated wastefully. We define the span of a peak house h, denoted by span(h), as the set of houses that are identically ranked by all the agents in base(h), starting from their first ranked house. If a house h is an individual peak, then we say span(h) = ∅.

Example 2. Consider the instance in Figure 1 with four agents and the following rankings.

i1: h2 ≻h1 ≻h3 ≻h4 ≻h5 ≻h6 ≻h7 i2: h4 ≻h5 ≻h6 ≻h3 ≻h2 ≻h1 ≻h7 i3: h4 ≻h5 ≻h6 ≻h3 ≻h7 ≻h2 ≻h1 i4: h4 ≻h5 ≻h6 ≻h7 ≻h3 ≻h2 ≻h1

It is a single-peaked instance with respect to the ordering ✄:= h1 ✄h2 ✄h3 ✄h4 ✄h5 ✄h6 ✄h7. The house h4 is a shared peak, and h2 is an individual peak. Notice that peak(i1) = h2 and peak(i2) = peak(i3) = peak(i4) = h4. Consequently, base(h4) = {i2, i3, i4}. Note that |span(h4)| = |{h4, h5, h6}| = 3, as these are the top houses identically ranked by all the agents in base(h4). Also, |span(h1)| = 0. An important and helpful observation is the following. If at least two agents from {i2, i3, i4} were to be envy-free in any allocation, then not only the peak house h4 would have to remain unallocated, but all the houses in span(h4) must also remain unallocated under any

17054

<!-- Page 6 -->

h1 h2 h3 h4 h5 h6 h7 i1 i2 i3 i4

**Figure 1.** Single-Peaked preferences

complete allocation. The allocation of h2, h3, h1, and h7 to the four agents, respectively, is the one minimizing Envy with exactly one envious agent, namely, i3.

We now present a series of structural results. If a shared peak h is assigned to one agent, it leads to envy among the other agents, with at least |base(h)| −1 envious agents. On the other hand, we show by the following claim that even if h is not assigned, at least |base(h)| −2 agents are bound to be envious under any allocation.

Lemma 5. Let h be a shared peak. Then, at most 2 agents from the set base(h) can be envy-free under any allocation.

Proof. Consider an allocation A. If the house h is allocated wastefully, then all the base(h) agents are envious, no matter which house they receive in A. If h is allocated nonwastefully to an agent, say i, then i is always envy-free in any completion of this allocation, as she receives her firstranked house. But, all other |base(h)|−1 agents are envious of i. If house h is not allocated in A, then we prove at most two agents in base(h) are envy-free. Let a single-peaked axis for the preferences be denoted by ▷= h1 ▷· · · ▷hm. Consider three agents i1, i2, and i3 from base(h). Then, at least 2 of these agents are allocated to houses from the interval either [h1, h) or (h, hm] on the axis ▷. WLOG, we assume that A(i1) = hj and A(i2) = hl such that {hj, hl} ∈ [h1, h) and l < j. Then, since h is a peak for both i1 and i2, by the structure of the rankings, it holds that both agents i1 and i2 have the (partial) ranking h1 ≺hl ≺hi ≺h. Then, agent i2 envies i1. Thus, at most one envy-free agent can be assigned to each interval [h1, h) and (h, hm]. Therefore, at most two agents can be envy-free from the set base(h). Furthermore, the houses allocated to the two agents lies on either side of h in a single peaked axis.

We now proceed to show another interesting structural claim that helps us to allocate the individual peaks non-wastefully.

Lemma 6. There exists an allocation with the minimum number of envious agents where all individual peaks are allocated, and they are allocated non-wastefully.

## Algorithm

2: Minimize Envy for Single-Peaked Preferences

Input: (N, H, ≻) and a single-peak axis ▷ Output: Allocation A that minimizes Envy

Base cases: 1: for h ∈pI do A(base(h)) = h 2: end for 3: for hj, hl s.t. hj ∈span(hl) and hl ∈span(hj) do A(i) = hj, A(i′) = hl s.t. i ∈base(hj), i′ ∈base(hl) 4: end for 5: for hj, hl s.t. hj ∈span(hl) but hl /∈span(hj) do A(i) = hl for some i ∈base(hl) 6: end for Greedy resolve: 7: S ←Set of remaining unallocated shared peaks. 8: Order the houses in S as h ⪯h′ if |span(h)| ≤ |span(h′)| Say, {hz1, hz2,... hz|S|} is the ordering. 9: for j ∈[S] do m′, n′ = number of unallocated houses & agents under A 10: if m′ −|span(hzj)| ≥n′ then Resolve hzj & U ← span(hzj) 11: else Allocate {hzj, hzj+1,... hzS} non-wastefully. 12: end if 13: end for 14: Each remaining agent, in a fixed order, chooses its favorite house among the remaining houses, except U. 15: Output A.

Let the number of individual and shared peaks be pI and pS respectively. Then any allocation can have at least pI + pS envy-free agents, just by allocating the peaks non-wastefully and completing the allocation in an arbitrary manner. Moreover, by Lemma 5, no allocation can have more than pI +2· pS envy-free agents. This establishes the following result.

Lemma 7. Let |EF(A⋆)| be the number of envy-free agents under any optimal allocation A⋆. Then, pI + pS ≤ |EF(A⋆)| ≤pI + 2 · pS.

The following is a generalization of Lemma 5.

Lemma 8. Let {h1, h2,... hk} be the set of k shared peaks such that span(hj) ∩span(hl)̸ = ∅for any j, l ∈[k]. Then at least k and at most k + 1 agents from the set S j∈[k] base(hj) are envy-free under any optimal allocation.

A shared peak h is said to be resolved under an allocation A if span(h) remains unallocated and as a result exactly two agents from the set base(h) become envy-free under A, specifically, the agents from base(h) who get their span(h) + 1 ranked house (Lemma 5).

Overview of Algorithm 2. In the light of Lemma 6, we first allocate all the individual peaks non-wastefully. For a pair of shared peaks hj and hl such that hj ∈span(hl) and hl ∈span(hj), we allocate hj and hl non-wastefully. Otherwise if hj ∈span(hl) but hl /∈span(hj), then in the light of Lemma 8, at most 3 agents from base(hj)∪base(hl) can be envy-free, and to that end, we allocate hl non-wastefully. Now what remains are the shared peaks, possibly with over-

17055

<!-- Page 7 -->

**Figure 2.** Welfare loss incurred starting from a Nash (blue) and Egalitarian (green) welfare-maximizing allocation and performing at most q reallocations, where 1 ≤q ≤n.

lapping spans. We resolve these remaining peaks in a greedy manner, by choosing a peak with the minimum span size in each step. In each step, we resolve a peak and set some unassigned houses as unavailable. We resolve the peaks as long as the number of unallocated agents is less than the number of available unallocated houses. Finally, we complete the allocation by letting the remaining unallocated agents choose an available unallocated house, one by one.

Proof Idea of Theorem 3. Let EF(A) denote the set of envy-free agents in an allocation A. Let A be the output of Algorithm 2 and A∗be an optimal allocation. Clearly, |EF(A∗)| ≥|EF(A)|. To prove the correctness of Algorithm 2, we show that |EF(A∗)| = |EF(A)|. To this end, we show that |EF(A∗)\EF(A)| = |EF(A)\EF(A∗)| by a case analysis.

Theorem 4. Given a single-dipped instance I = (N, H, ≻, ✄) of house allocation, minimizing the number of envious agents admits a linear time algorithm with runtime O(m).

The proof depends on a structural claim that at most 2 agents can be envy-free under any allocation. It is relevant to note that, unlike Algorithm 1, Algorithm 2 does not extend to other envy measures like TotalEnvy. This is because the structural claim of Lemma 5 is specific to Envy.

## 5 Experiments

We experimentally evaluated our algorithms with synthetic house allocation instances. We construct instances with n = 6 agents and 6 ≤m ≤11 houses. Every agent values a house between an integer between 0 and 10 chosen uniformly at random. The results are averaged over 100 instances for each (n, m) pair. For each instance, our algo- rithm (Algorithm 1) is initialized with a welfare-maximizing allocation. We compare the welfare of the allocations obtained as the numbers of reallocations aimed at minimizing Envy increases 1 ≤q ≤n. Figure 2 shows that the welfare loss as we increase the number of reallocations starting from a Nash and an Egalitarian welfare-maximizing allocation. We also show (deferred to the full version) the reduction in Envy as we increase the number of reallocations. These plots suggest that welfare loss and the drop in Envy starts flattening after 3 reallocations. That is, a small number of reallocations, specifically around 3, are sufficient to significantly reduce envy while maintaining high welfare. Thus, starting from a welfare-maximizing allocation, just a few targeted changes can move the system close to a minimum envy state without substantial sacrifice in welfare. We defer additional experiments to the full version.

## 6 Conclusion

We present a general framework that enables tractable computations for finding fairer solutions in house allocations. Given the known hardness and inapproximability of minimizing envy in this context, unless P=NP, we cannot get a tractable algorithm parameterized by maximum envy k and d, even for binary preferences, making a framework like ours essential to achieve any tractability. The properties that are necessary for our algorithm are: the connectivity of minimal improvement sets, and being able to compute the decrease in envy (rC) due to an improvement set. Thus, the algorithm may extend for weighted envy (Dai et al. 2024) but would not directly work for concepts like local envy (Hosseini et al. 2023; Beynier et al. 2019) where the envy depends on factors other than the structure of the preferences. Extending our algorithms for single-peaked preferences with ties and other envy measures is an interesting direction.

17056

![Figure extracted from page 7](2026-AAAI-fair-societies-algorithms-for-house-allocations/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

HH acknowledges the support from the National Science Foundation (NSF) through CAREER Award IIS-2144413 and Award IIS-2107173. SR is supported by the Start-Up project grant of Indian Statistical Institute. AS is supported by Walmart Center for Tech Excellence (CSR WMGT-23- 0001).

## References

Abdulkadiro˘glu, A.; and S¨onmez, T. 1999. House Allocation with Existing Tenants. Journal of Economic Theory, 88(2): 233–260. Aigner-Horev, E.; and Segal-Halevi, E. 2021. Envy-free Matchings in Bipartite Graphs and their Applications to Fair Division. Information Sciences. Bade, S. 2019. Matching with single-peaked preferences. Journal of Economic Theory, 180: 81–99. Ballester, M. A.; and Haeringer, G. 2011. A characterization of the single-peaked domain. Social Choice and Welfare, 36(2): 305–322. Benabbou, N.; Chakraborty, M.; Ho, X.-V.; Sliwinski, J.; and Zick, Y. 2018. Diversity Constraints in Public Housing Allocation. In Proceedings of the 17th International Conference on Autonomous Agents and MultiAgent Systems, AA- MAS ’18, 973–981. Richland, SC: International Foundation for Autonomous Agents and Multiagent Systems. Benabbou, N.; Chakraborty, M.; Ho, X.-V.; Sliwinski, J.; and Zick, Y. 2020. The price of quota-based diversity in assignment problems. ACM Transactions on Economics and Computation (TEAC), 8(3): 1–32. Beynier, A.; Chevaleyre, Y.; Gourv`es, L.; Harutyunyan, A.; Lesca, J.; Maudet, N.; and Wilczynski, A. 2019. Local Envy-Freeness in House Allocation Problems. Autonomous Agents and Multi-Agent Systems, 33(5): 591–627. Beynier, A.; Maudet, N.; Rey, S.; and Shams, P. 2021. Swap dynamics in single-peaked housing markets. Autonomous Agents and Multi-Agent Systems, 35(2): 20. Black, D. 1948. On the Rationale of Group Decisionmaking. Journal of Political Economy, 56(1): 23–34. Budish, E. 2011. The combinatorial assignment problem: Approximate competitive equilibrium from equal incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Filos-Ratsikas, A.; and Procaccia, A. D. 2015. An improved 2-agent kidney exchange mechanism. Theoretical Computer Science, 589: 53–60. Choo, D.; Ling, Y. H.; Suksompong, W.; Teh, N.; and Zhang, J. 2024. Envy-free house allocation with minimum subsidy. Operations Research Letters, 54: 107103. Conitzer, V. 2007. Eliciting single-peaked preferences using comparison queries. In Proceedings of the 6th international joint conference on Autonomous agents and multiagent systems, 1–8. Dai, S.; Chen, Y.; Wu, X.; Xu, Y.; and Zhang, Y. 2024. Weighted Envy-Freeness in House Allocation. arXiv preprint arXiv:2408.12523.

Dey, P.; Dhar, A.; Hota, A.; and Kolay, S. 2025. The Complexity of Minimum-Envy House Allocation Over Graphs. arXiv:2505.00296. Elkind, E.; Faliszewski, P.; and Skowron, P. 2020. A characterization of the single-peaked single-crossing domain. Social Choice and Welfare, 54(1): 167–181. Elkind, E.; Lackner, M.; and Peters, D. 2022. Preference Restrictions in Computational Social Choice: A Survey. arXiv:2205.09092. Faliszewski, P.; Hemaspaandra, E.; Hemaspaandra, L. A.; and Rothe, J. 2009. The shield that never was: societies with single-peaked preferences are more open to manipulation and control. In Proceedings of the 12th Conference on Theoretical Aspects of Rationality and Knowledge, TARK ’09, 118–127. New York, NY, USA: Association for Computing Machinery. ISBN 9781605585604. Friedman, E.; Psomas, C.-A.; and Vardi, S. 2015. Dynamic fair division with minimal disruptions. In Proceedings of the sixteenth ACM conference on Economics and Computation, 697–713. Friedman, E.; Psomas, C.-A.; and Vardi, S. 2017. Controlled dynamic fair division. In Proceedings of the 2017 ACM Conference on Economics and Computation, 461–478. Gan, J.; Suksompong, W.; and Voudouris, A. A. 2019. Envyfreeness in house allocation problems. Mathematical Social Sciences, 101: 104–106. He, J.; Procaccia, A. D.; Psomas, A.; and Zeng, D. 2019. Achieving a fairer future by changing the past. In Proceedings of the 28th International Joint Conference on Artificial Intelligence, IJCAI’19, 343–349. AAAI Press. ISBN 9780999241141. Hosseini, H.; Kumar, M.; and Roy, S. 2024. The Degree of Fairness in Efficient House Allocation. In ECAI 2024 - 27th European Conference on Artificial Intelligence, Including 13th Conference on Prestigious Applications of Intelligent Systems, PAIS 2024, Proceedings, 3636–3643. IOS Press BV. Hosseini, H.; McGregor, A.; Sengupta, R.; Vaish, R.; and Viswanathan, V. 2024. Tight Approximations for Graphical House Allocation. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems, AAMAS ’24, 825–833. Richland, SC: International Foundation for Autonomous Agents and Multiagent Systems. ISBN 9798400704864. Hosseini, H.; Payan, J.; Sengupta, R.; Vaish, R.; and Viswanathan, V. 2023. Graphical House Allocation. In 22nd International Conference on Autonomous Agents and Multiagent Systems, AAMAS. Hosseini, H.; Roy, S.; and Sethia, A. 2025. Fair Societies: Algorithms for House Allocations. arXiv:2511.07022. Hylland, A.; and Zeckhauser, R. 1979. The efficient allocation of individuals to positions. Journal of Political Economy, 87(2): 293–314. Kamiyama, N.; Manurangsi, P.; and Suksompong, W. 2021. On the Complexity of Fair House Allocation. Operations Research Letters, 49(4): 572–577.

17057

<!-- Page 9 -->

Kellerer, H.; Pferschy, U.; and Pisinger, D. 2004. Knapsack problems. Springer. Madathil, J.; Misra, N.; and Sethia, A. 2025. The Cost and Complexity of Minimizing Envy in House Allocation. Journal of Autonomous Agents and Multi-Agent Systems, 39(2): 29. Puppe, C. 2018. The single-peaked domain revisited: A simple global characterization. Journal of Economic Theory, 176: 55–80. Shapley, L.; and Scarf, H. 1974. On cores and indivisibility. Journal of Mathematical Economics, 1(1): 23–37. Shende, P.; and Purohit, M. 2020. Strategy-proof and envyfree mechanisms for house allocation. J. Econ. Theory, 213: 105712. Sprumont, Y. 1991. The division problem with singlepeaked preferences: a characterization of the uniform allocation rule. Econometrica: Journal of the Econometric Society, 509–519. Tamura, Y. 2023. Object reallocation problems with singledipped preferences. Games and Economic Behavior, 140: 181–196.

17058
