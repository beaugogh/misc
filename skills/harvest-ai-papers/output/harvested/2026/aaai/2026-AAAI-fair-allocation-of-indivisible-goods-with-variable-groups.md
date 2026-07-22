---
title: "Fair Allocation of Indivisible Goods with Variable Groups"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38742
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38742/42704
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Fair Allocation of Indivisible Goods with Variable Groups

<!-- Page 1 -->

Fair Allocation of Indivisible Goods with Variable Groups

Paul G¨olz1, Ayumi Igarashi2, Pasin Manurangsi3, Warut Suksompong4

1Cornell University, USA 2University of Tokyo, Japan 3Google Research, Thailand 4National University of Singapore, Singapore

## Abstract

We study the fair allocation of indivisible goods with variable groups. In this model, the goal is to partition the agents into groups of given sizes and allocate the goods to the groups in a fair manner. We show that for any number of groups and corresponding sizes, there always exists an envy-free up to one good (EF1) outcome, thereby generalizing an important result from the individual setting. Our result holds for arbitrary monotonic utilities and comes with an efficient algorithm. We also prove that an EF1 outcome is guaranteed to exist even when the goods lie on a path and each group must receive a connected bundle. In addition, we consider a probabilistic model where the utilities are additive and drawn randomly from a distribution. We show that if there are n agents, the number of goods m is divisible by the number of groups k, and all groups have the same size, then an envy-free outcome exists with high probability if m = ω(log n), and this bound is tight. On the other hand, if m is not divisible by k, then an envy-free outcome is unlikely to exist as long as m = o(√n).

## Introduction

Fairly allocating limited resources is a fundamental societal challenge, with applications ranging from dividing household supplies among families to distributing personnel among schools or other public institutions. The problem of fair division has accordingly received interest in several disciplines, including in computational social choice and multi-agent systems (Bouveret, Chevaleyre, and Maudet 2016; Markakis 2017; Aziz 2020; Walsh 2020). Most of the work in fair division assumes that each recipient of a bundle of resources is an individual agent, represented by a single preference. However, when distributing resources among families, schools, or institutions, each recipient in fact consists of multiple agents. Although these agents share the same set of resources and derive full value from the resources in their set, they may have differing preferences over the resources. This has motivated several researchers to study the (fixed-)group model, where the agents are partitioned into groups and the aim is to allocate the resources in a fair manner among the groups (Manurangsi and Suksompong 2017, 2025; Ghodsi et al. 2018; Segal- Halevi and Nitzan 2019; Caragiannis, Larsen, and Shyam

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

2025; G¨olz and Yaghoubizade 2026). For instance, Manurangsi and Suksompong (2022) investigated the notion of envy-freeness up to c goods (EFc). This means that no agent would prefer another group’s bundle over her own group’s if some set of at most c goods were removed from the other group’s bundle. Manurangsi and Suksompong proved that when the number of groups is constant, there exists an EFc allocation for c = O(√n), where n denotes the total number of agents, and this bound is also asymptotically tight.

The fixed-group model is appropriate when membership in the groups is predetermined, as in the allocation among families or countries. In other applications, however, the resource allocator can select the partition of agents into groups alongside the allocation. This is the case, for example, when dividing workers in an organization into teams and assigning resources to these teams. In light of this, Kyropoulou, Suksompong, and Voudouris (2020, Sec. 5) proposed a variablegroup model, in which a partition of the agents into groups can be chosen along with an allocation of the resources.1

When the resources consist of divisible items such as time, Segal-Halevi and Suksompong (2021) proved that an envy-free outcome always exists in the variable-group model. On the other hand, if the resources contain indivisible items such as books or gym equipment, Kyropoulou, Suksompong, and Voudouris (2020) showed that an EF1 outcome can be ensured in the case of two groups, and an outcome satisfying a relaxation of proportionality—which is fundamentally weaker than EF1—can be satisfied for any number of groups. This differs from the fixed-group model, where even for two groups, the optimal EFc guarantee deteriorates as the number of agents grows.

In this paper, we expand and deepen our understanding of fairness, particularly envy-freeness, when allocating indivisible goods in the variable-group model. For instance, we study the following question: does an EF1 outcome exist for any number of groups and any corresponding sizes, or is it sometimes necessary to relax the notion to EFc for some (possibly non-constant) c? As we shall see, the flexibility provided by this model enables remarkably strong fairness guarantees to be made.

1For further motivation of the variable-group model, we refer to the papers by Kyropoulou, Suksompong, and Voudouris (2020) and Segal-Halevi and Suksompong (2021).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16954

<!-- Page 2 -->

## 1.1 Our Results

In Section 3, we answer the question above in the positive: for any desired group sizes, an EF1 outcome exists and, moreover, can be computed efficiently (Theorem 1). This result holds even for arbitrary monotonic utilities, and significantly generalizes the well-known result by Lipton et al. (2004) that EF1 allocations always exist in the individual setting where each group has size one. Our algorithm is a careful extension of Lipton et al.’s classic envy cycle elimination algorithm. This positive result stands in contrast to the fixed-group setting, where c = Ω(√n) is required to guarantee the existence of an EFc allocation (Manurangsi and Suksompong 2022).

In Section 4, we strengthen the previous result by showing that, if the goods lie on a path, EF1 allocations exist even when each group must receive a connected bundle (Theorem 2). The connectivity requirement is natural when the goods correspond to time slots or offices along a corridor, and has been studied in several papers (Bouveret et al. 2017; Bei et al. 2022; Bil`o et al. 2022; Igarashi 2023). This existence result also holds for monotonic utilities, and generalizes results from the individual setting by Bil`o et al. (2022) and Igarashi (2023). However, like in the individual setting, the result does not come with an efficient algorithm.

Finally, in Section 5, we consider a probabilistic model where the utilities are additive and each agent’s utility for each good is drawn independently at random from a nonatomic distribution.2 We are interested in when an envy-free3 outcome exists with high probability (that is, with probability approaching 1 as the number of agents n grows), assuming that the number of groups k is fixed and all groups have the same size. Interestingly, we show that the existence depends on whether the number of goods m is divisible by k. On the one hand, if m is divisible by k, the transition occurs at merely Θ(log n): an envy-free outcome is unlikely to exist if m = o(log n) (Theorem 3), but likely to exist if m = ω(log n) (Theorem 4). On the other hand, if m is not divisible by k, such an outcome is unlikely to exist as long as m = o(√n) (Theorem 5).4

## 1.2 Further Related Work

As mentioned earlier, a number of authors have investigated fair division among groups, mostly focusing on the fixedgroup model. Besides envy-freeness, Manurangsi and Suksompong (2022) also obtained bounds on proportionality as well as consensus 1/k-division—the latter is even more stringent than envy-freeness, as it requires agents to value all bundles of goods equally. While these bounds were already tight in terms of n, Caragiannis, Larsen, and Shyam (2025) and Manurangsi and Meka (2026) recently improved their

2A distribution is called non-atomic if it does not put a positive probability on any single point.

3Envy-freeness corresponds to EFc for c = 0. An envy-free outcome does not always exist, e.g., when there are two groups and only one valuable good.

4In contrast, a result in the fixed-group setting by Manurangsi and Suksompong (2017) implies that an envy-free outcome is likely to exist when m = Ω(n log n).

dependence on k. Bu et al. (2023), Barman et al. (2025), as well as Kawase, Roy, and Sanpui (2025) studied settings that can be interpreted as special cases of the fixed-group model. For example, Bu et al.’s setting corresponds to the fixed-group model when each group has size two.

The probabilistic model we consider in Section 5 falls under the framework of asymptotic fair division. This framework was introduced by Dickerson et al. (2014) and subsequently studied in several papers (Kurokawa, Procaccia, and Wang 2016; Suksompong 2016; Manurangsi and Suksompong 2020, 2021; Bai and G¨olz 2022; Bai et al. 2022; Benad`e et al. 2024; Yokoyama and Igarashi 2025). The motivation is that, since an allocation satisfying envy-freeness (or some other fairness notion) does not always exist, it is natural to ask when an envy-free allocation is likely to exist if the utilities are drawn at random. We highlight two relations between our results and known results from this line of work. Firstly, Manurangsi and Suksompong (2017) examined the fixed-group model and showed that an envy-free allocation is unlikely to exist unless m = Ω(n). This contrasts with our results, which show that existence is already likely in the variable-group model when m = ω(log n). Secondly, in the individual setting, Manurangsi and Suksompong (2020, 2021) proved that the threshold for the existence of envyfree allocations differs according to whether m is divisible by n. However, the (multiplicative) gap in their case is only logarithmic (i.e., Θ(n) vs. Θ(n log n/ log log n)), whereas our gap is much larger (i.e., Θ(log n) vs. Ω(√n)).

## Preliminaries

For any positive integer t, let [t]:= {1, 2,..., t}. Let k ≥2 and n1,..., nk be positive integers, N = [n] be a set of n = n1 + · · · + nk agents, and M = [m] be a set of m goods. A bundle refers to a (possibly empty) set of goods. Each agent a ∈N has a utility function ua over the sets of goods in M; for a single good g ∈M, we sometimes write ua(g) instead of ua({g}). We assume that the utilities are monotonic, meaning that ua(M ′) ≤ua(M ′′) for any a ∈N and M ′ ⊆M ′′ ⊆M, and normalized, i.e., ua(∅) = 0. The utilities are called additive if ua(M ′) = P g∈M ′ ua(g). When utilities are non-additive, we assume that an algorithm can query any agent’s utility for any set of goods in constant time. An instance in the variable-group model consists of the set of agents N, the set of goods M, the agents’ utility functions, and the desired group sizes n1,..., nk.

We would like to partition the n agents into k groups C1,..., Ck of sizes n1,..., nk, respectively, and allocate the m goods among these groups. We write C = (C1,..., Ck). An allocation A = (A1,..., Ak) consists of k disjoint bundles, where bundle Ai is allocated to the i-th group; it is called complete if A1 ∪· · · ∪Ak = M. An outcome consists of a partition of agents C along with a complete allocation of goods A. An outcome (C, A) is

• envy-free up to c goods (EFc), for a given non-negative integer c, if for every i, j ∈[k] and every agent a ∈ Ci, there exists a set B ⊆Aj with |B| ≤c such that ua(Ai) ≥ua(Aj \ B); • envy-free if it is EF0.

16955

<!-- Page 3 -->

The individual setting refers to a special case of this model where n1 = · · · = nk = 1 (and therefore k = n).

EF1: Existence and Computation

Recall that in the individual setting, a classic result of Lipton et al. (2004) states that for any instance with arbitrary monotonic utilities, an EF1 allocation exists. Moreover, such an allocation can be found in time O(mn3) via the envy cycle elimination algorithm. Intuitively, this algorithm allocates one good at a time in an arbitrary order. The algorithm maintains an “envy graph”, which is a directed graph that captures the envy relations among the agents. In particular, the vertices represent the agents, and there is an edge from one agent to another agent if and only if the former agent envies the latter agent. Hence, an agent is unenvied exactly when the corresponding vertex has no incoming edge. Each good is assigned to an unenvied agent, and if the assignment causes a cycle to be formed in the envy graph, the cycle is eliminated by giving each agent’s bundle to the preceding agent on the cycle. Once all cycles have been eliminated, the next good can be assigned to an unenvied agent, and EF1 is maintained throughout the algorithm.

A priori, it may appear that the envy cycle elimination algorithm is not well-suited for the group setting. Indeed, it is unclear when a group should be considered to “envy” another group, as different agents in the same group may have differing opinions about the groups’ bundles. Nevertheless, we show that adopting an alternative perspective on the algorithm allows for its generalization to the group setting. Specifically, instead of moving the bundles as in the typical interpretation, we can reinterpret the envy cycle elimination step as moving the agents along the cycles instead. This interpretation enables a generalization of the algorithm to accommodate groups, as it permits the reassignment of individual agents according to their envy relations while preserving group sizes, thereby leveraging the flexibility of the variable-group model. In addition to extending the seminal result of Lipton et al. (2004), the following theorem also strengthens a variable-group guarantee due to Kyropoulou, Suksompong, and Voudouris (2020, Thm. 5.6), which holds under additive utilities for a much weaker notion than EF1.

Theorem 1. For any instance with arbitrary monotonic utilities, there exists an EF1 outcome. Moreover, such an outcome can be computed in time O(mn3).

Proof. We use the following generalization of the envy cycle elimination algorithm.

1. Let C be an arbitrary partition of the n agents into groups of sizes n1,..., nk, and let A be an empty allocation. 2. Construct an envy graph, which is a directed graph with the k groups as the vertices; this graph will be updated as the algorithm proceeds. For each agent, add an edge from the agent’s group to another group if the agent envies the latter group. (Thus, the graph initially contains no edges.) In particular, there can be multiple edges from one vertex to another vertex.

3. Take an arbitrary unallocated good, and allocate it to any group with no incoming edge in the envy graph. Update the envy graph. 4. If there is at least one directed cycle in the envy graph, consider an arbitrary cycle. For each edge in the cycle, move the agent associated with this edge to the group that the agent envies. Update the envy graph. If there is still a directed cycle in the envy graph, repeat this step. 5. If there is still an unallocated good, go back to Step 3. Otherwise, output the current outcome (C, A).

We first show that the algorithm outputs a valid outcome. To this end, we prove that each time we eliminate a cycle in Step 4, the number of edges in the envy graph decreases. For each agent not associated with an edge in the cycle, the agent’s own bundle as well as all other bundles remain the same, so the number of envy edges from the agent also remains the same. On the other hand, for each agent associated with an edge in the cycle, the agent is assigned to a better bundle in her view among the k bundles, so the number of envy edges from the agent decreases by at least one. Hence, the total number of envy edges decreases, which means that the process of eliminating cycles must terminate. When the envy graph contains no cycle, there must exist a vertex with no incoming edge, and we can allocate the next good to the corresponding group. It follows that all goods are allocated. Moreover, the sizes of the k groups remain n1,..., nk throughout, so the algorithm outputs a valid outcome.

Next, we show that the outcome returned by the algorithm is EF1. Specifically, we prove that at every point during the execution of the algorithm, the partition C and the (possibly incomplete) allocation A together yield EF1. This is true at the beginning of the algorithm, as the allocation is empty. When a good is allocated, it is allocated to a group with no incoming edge, so any envy towards the group can be eliminated by removing this good. Moreover, when a cycle is eliminated, for each agent not associated with an edge in the cycle, the agent’s own bundle as well as all other bundles remain the same, so the EF1 invariant is maintained. On the other hand, for each agent associated with an edge in the cycle, the agent is assigned to a better bundle in her view among the k bundles. Since any envy that the agent has towards another bundle can be eliminated by removing a good from the bundle before, the same remains true afterwards, and the EF1 invariant is again maintained.

Finally, we analyze the running time of the algorithm. There are m allocated goods, and each allocated good increases the number of envy edges by at most n. Finding and eliminating a directed cycle can be done in time O(k2), and the elimination decreases the number of envy edges by at least one. As the algorithm can query any agent’s utility for any set of goods in constant time, updating the envy graph takes time O(nk). Since k ≤n, the algorithm runs in time O(mn3).

## 4 EF1: Adding Connectivity Constraints

Having established the general existence of EF1 outcomes, in this section, we impose an additional requirement in the form of connectivity. Specifically, we assume that the goods

16956

<!-- Page 4 -->

lie on a path 1, 2,..., m. An allocation A is said to be connected if Aj forms an interval on the path for each j ∈[k]. An outcome (C, A) is called connected if A is connected.

In the individual setting, Igarashi (2023) proved that a connected EF1 allocation is guaranteed to exist, thereby strengthening an earlier result of Bil`o et al. (2022), which holds for EF2. For their proofs, Bil`o et al. and Igarashi developed a discretization approach using Sperner’s lemma (Sperner 1928). This idea was originally due to Su (1999), who provided an elegant proof that an envy-free allocation of a cake (i.e., a heterogeneous divisible good) always exists. Su’s proof encodes possible divisions as points in the standard simplex and employs a triangulation of the simplex along with a coloring of each vertex of the triangulation. By applying Sperner’s lemma, Su showed the existence of an elementary simplex (i.e., a simplex not composed of smaller simplices in the triangulation) whose vertices correspond to allocations that are similar to one another, where each allocation ensures that a different agent is envy-free. An infinite sequence of such simplices, with their sizes progressively shrinking, converges to an envy-free allocation.

Our main result of this section generalizes the results of Bil`o et al. (2022) and Igarashi (2023) to the group setting. The result is formally stated as follows.

Theorem 2. For any instance with arbitrary monotonic utilities such that the goods lie on a path, there exists a connected EF1 outcome.

Note that unlike Theorem 1, this theorem does not come with efficient computation. Indeed, the question of whether a connected EF1 allocation can be computed efficiently is open even in the individual setting (Igarashi 2023).

We start by recalling some basic notions of combinatorial topology. For any positive integer k, a (k −1)-simplex S is the convex hull of k main vertices x1, x2,..., xk. We use the notation S = ⟨x1, x2,..., xk⟩. The (k −1)-standard simplex ∆k−1 is the (k −1)-simplex whose main vertices are given by the j-th unit vectors ej ∈{0, 1}k for j ∈[k], where ej h = 1 if h = j and ej h = 0 otherwise. A triangulation T of a (k−1)-simplex S is a collection of smaller (k −1)-simplices S1, S2,..., Sh such that the union of simplices Sj for j ∈[h] is S, and for each i̸ = j, the intersection Si ∩Sj is either empty or a face common to Si and Sj. We call S1, S2,..., Sh elementary simplices, and write V (T) for the set of vertices of a triangulation T.

For a triangulation T of a (k −1)-simplex S, a coloring is a mapping λ: V (T) →[k] that assigns a color in [k] to each vertex x ∈V (T). A coloring λ is called proper if we can write S = ⟨x1, x2,..., xk⟩in such a way that if a vertex x ∈V (T) is colored with color j (i.e., j = λ(x)), then xj is a vertex of the minimal face containing x. For example, if k = 3, then a (k −1)-simplex can be viewed as a triangle. In a proper coloring of the simplex, the three main vertices x1, x2, x3 are colored 1, 2, 3, respectively, and each vertex x on an edge between xi and xj is colored either i or j.

In our proof, the space of connected allocations is encoded by the positions of k −1 “knives”. Like Bil`o et al. (2022) and Igarashi (2023), we consider a triangulation of this space, where each knife is at either a vertex or an edge of the path. More precisely, consider the following simplex:

Sm:= x ∈Rk−1

1 2 ≤x1 ≤· · · ≤xk−1 ≤m + 1 2

.

Let Thalf be a Kuhn’s triangulation of Sm (Deng, Qi, and Saberi 2012; Bil`o et al. 2022; Igarashi 2023). The vertices of this triangulation are given by

V (Thalf) = x ∈Sm xi ∈

1

2, 1,..., m + 1 2

, ∀i

, where each elementary simplex S = ⟨x1, x2,..., xk⟩of Thalf satisfies the property that there exists a permutation ϕ: [k] →[k] such that xϕ(i+1) = xϕ(i)+ 1

2eϕ(i) for each i ∈ [k −1]. Each vertex x ∈V (Thalf) yields a partial allocation A(x) = (A1(x), A2(x),..., Ak(x)) such that for each j ∈[k], the j-th bundle is given by

Aj(x) = {y ∈[m] | xj−1 < y < xj}, with x0 = 1

2 and xk = m + 1 2. With appropriate coloring and rounding, Igarashi (2023) demonstrated that a desired elementary simplex, guaranteed by Sperner’s lemma, can be rounded to produce a connected EF1 allocation. The proof relies on the notion of a virtual utility, ˆua(x, j), defined for each vertex x of the triangulation and each index j ∈[k]. This virtual utility determines agent a’s most preferred bundle in a partial allocation corresponding to the vertex x; in particular, ˆua(x, j) = 0 if Aj(x) = ∅, and ˆua(x, j) ≥0 otherwise. Igarashi (2023, Alg. 1) presented an algorithm that, given an elementary simplex S = ⟨x1, x2,..., xk⟩of Thalf, produces an allocation A = (A1, A2,..., Ak) with the following property: each agent’s estimate of the j-th bundle based on the virtual utility is upper-bounded by her true utility of Aj and lower-bounded by the her “up-to-one utility” of Aj, as defined next. For any connected subset of goods I, the up-toone utility u− a (I) of agent a is defined as u− a (I):=

 



0 if I = ∅; min ua(I \ {g}) | g ∈I such that I \ {g} is connected if I̸ = ∅.

The following lemma is stated as Lemma 3.2 in the work of Igarashi (2023).5

Lemma 1 (Igarashi 2023). Consider the triangulation Thalf of Sm. There exists an algorithm that, given any elementary simplex S = ⟨x1, x2,..., xk⟩of Thalf, returns a connected allocation (A1, A2,..., Ak) such that for every agent a ∈ N and every pair of indices i, j ∈[k], we have ua(Aj) ≥

ˆua(xi, j) ≥u− a (Aj). Our main lemma of this section is as follows. Lemma 2. Let λ1,..., λn: V (Thalf) →[k] be any proper colorings. Then, there exist an elementary simplex S∗= ⟨x∗

1, x∗ 2,..., x∗ k⟩of Thalf and π: N →[k] such that 1. |π−1(i)| = ni for each i ∈[k], and

5Although Igarashi’s Lemma 3.2 is stated for the case k = n, the same proof also works when k̸ = n.

16957

<!-- Page 5 -->

2. π(a) ∈{λa(x∗ h) | h ∈[k]} for each a ∈N.

The proof of Lemma 2 involves applying the averaging technique, originally introduced by Gale (1984) and recently applied to cake cutting (Asada et al. 2018; Igarashi and Meunier 2025). It considers the average preference of the agents and derives a desired assignment using a network flow argument. The details are deferred to the full version of our paper (G¨olz et al. 2025).

We now show how to use the lemma to prove Theorem 2.

Proof of Theorem 2. Based on the virtual utilities, define a coloring λa: V (Thalf) →[k] for each a ∈N such that λa(x) ∈argmax{ˆua(x, j) | j ∈[k] such that Aj(x)̸ = ∅}.

These colorings were shown to be proper by Igarashi (2023).

Lemma 2 then yields an elementary simplex S∗ = ⟨x∗

1, x∗ 2,..., x∗ k⟩of Thalf and π: N →[k] that satisfy the two conditions of the lemma. Let Ci = π−1(i) for each i ∈ [k]; the first condition of the lemma ensures that |Ci| = ni. Next, we construct the allocation A∗= (A∗

1,..., A∗ k) by invoking Lemma 1 on S∗. We claim that (C, A∗) is an EF1 outcome. To see this, consider any agent a ∈N (belonging to Cπ(a)) and any j ∈[k]. By the second condition of Lemma 2, π(a) = λa(x∗ h) for some h ∈[k]. We thus have ua(A∗ π(a)) ≥ˆua(x∗ h, π(a)) (by Lemma 1)

≥ˆua(x∗ h, j) (since π(a) = λa(x∗ h))

≥u− a (A∗ j) (by Lemma 1).

Hence, (C, A∗) is an EF1 outcome, as desired.

Envy-Freeness: Asymptotic Existence

In this section, we turn our attention to the asymptotic existence of envy-free outcomes. Specifically, we consider a setting where the utilities are additive and, for each a ∈N and g ∈M, the utility ua(g) is drawn independently from a given distribution D. This distribution is assumed to be nonatomic (i.e., does not put a positive probability on any single point) and has a support contained in the interval6 [0, 1]. We also assume throughout this section that all groups have the same size, that is, n1 = · · · = nk = n/k—in particular, n is divisible by k. We fix k and investigate the asymptotic (non-)existence of EF outcomes as n grows. We say that an event occurs with high probability if the probability that it occurs approaches 1 as n →∞.

## 5.1 Divisible Case

We first consider the case where the number of goods m is divisible by k. Intuitively, this is an “easier” case, as it is possible to give every group the same number of goods. For this case, we show that the phase transition occurs at m = Θ(log n), as stated in the following two theorems.

Theorem 3. For any fixed k ≥2, if m ≤ ln n

4, then with high probability, no envy-free outcome exists.

6If the support is contained in [0, t] for some t > 1, we can scale down all utilities by t.

Theorem 4. For any fixed k ≥2, utility distribution D, and β ∈(0, 1), there exists a constant Ck,β,D such that, for any sufficiently large n and any m ≥Ck,β,D · ln n with the property that m is divisible by k, there is a polynomial-time algorithm that computes an envy-free outcome with probability at least 1 −β.

To facilitate the proofs, we introduce some definitions.

• Let A denote the set of all allocations. • An allocation A = (A1,..., Ak) ∈A is called balanced if |A1| = · · · = |Ak| = m/k. Let Abal be the set of all balanced allocations. • For A ∈A and a ∈N, let i∗ a(A) = argmaxi∈[k]ua(Ai), ties broken arbitrarily. For each i ∈[k], let pA i = Pr[i∗ a(A) = i], where the probability is taken over the randomness of the utilities. Let pA = (pA

1,..., pA k).

• Let CEF,A be the partition of N where each agent a ∈N is assigned to i∗ a(A). Note that the outcome (CEF,A, A) is always envy-free. • Let P(N) denote the set of all partitions (C1,..., Ck) of N such that |C1| = · · · = |Ck| = n/k. • For A ∈A, let EA denote the event that CEF,A ∈P(N).

Since D is non-atomic, a tie in utilities (i.e., ua(B) = ua(B′) for some agent a and distinct bundles B, B′) occurs with probability zero. We thus have the following.

Observation 1. The probability that an envy-free outcome exists is equal to Pr[W

A∈A EA].

We continue with further preliminaries on probabilities.

• For a distribution P, we write supp(P) to denote its support. For Λ ⊆supp(P), we write P(Λ) as a shorthand for the measure (i.e., probability) of Λ under P. When Λ = {λ} has size one, we simply write P(λ). • For Σ ∈Rd×d, we write N(0, Σ) to denote the centered (multivariate) Gaussian distribution supported on Rd with covariance Σ. • Let ∆k−1 n denote the discrete (k−1)-simplex {x ∈Zk

≥0 | P i∈[k] xi = n}.

• For n ∈N and p ∈∆k−1, the multinomial distribution Mult (n, p) is a distribution supported on ∆k−1 n where Mult (n, p) {x}:= n x

Q i∈[k] pxi i for each x ∈∆k−1 n.

Due to space constraints, all missing proofs can be found in the full version of our paper (G¨olz et al. 2025).

Non-Existence via First Moment Method. We begin by proving the non-existence result (Theorem 3) via the first moment method. Specifically, in light of Observation 1, we compute Pr[EA] for any allocation A and apply the union bound. We start with a simple formula.

Observation 2. For any allocation A, we have Pr[EA] = Mult n, pA n k · 1

.

Proof. Since the agents’ utilities are independent, the distribution of the number of agents in CEF,A is Mult n, pA

. The formula follows from the definition of EA.

16958

<!-- Page 6 -->

A standard bound on Mult n, pA n k · 1 then yields the following lemma.

Lemma 3. For any A ∈A, we have Pr[EA] ≤ kk/2

(2πn)

k−1

2.

Moreover, for any A ∈Abal, Pr[EA] ≥ 1 ek2/n · kk/2

(2πn)

k−1

2.

We can now prove Theorem 3 by taking the union bound.

Proof of Theorem 3. Using Observation 1 and Lemma 3 and taking the union bound over all A ∈A, we find that the probability that an envy-free outcome exists is at most km · kk/2

(2πn)

k−1

2 ≤n ln k

4 · kk/2 n k−1

2 = kk/2 n

2k−ln k−2 4, where we use the assumption that m ≤ln n

4. The last quantity is o(1) for any fixed k ≥2.

Existence via Second Moment Method. Next, we turn to the existence result (Theorem 4). Recall that we have estimated the first moment Pr[EA] in Lemma 3. One might expect that when the sum of Pr[EA] over all A ∈A far exceeds 1, our desired event W

A∈A EA occurs with high probability. However, this is not necessarily true for dependent events. To overcome this issue, we employ the second moment method, which leverages the fact that if the events are nearly independent, in the sense that Pr[EA ∧EA′] ≤ (1 + o(1)) Pr[EA] · Pr[EA′], then we can reach the desired conclusion. Unfortunately, such an inequality need not hold for all pairs of allocations A, A′. Indeed, when A and A′ are “close”, EA and EA′ can be highly correlated. Therefore, we will only apply the second-moment method on a set of allocations that are “far away” from one another. The exact definition of “far away” that we use is given below in Definition 1. Observe that if A, A′ are drawn independently at random from Abal, then E[|Ai ∩A′ j|] = m/k2 for any i, j ∈[k]. Thus, the condition in Definition 1 requires that |Ai ∩A′ j| is close to its expectation.

Definition 1. For δ ∈[0, 1], two balanced allocations A = (A1,..., Ak) and A′ = (A′

1,..., A′ k) are said to be δ-intersection balanced (δ-IB) if m(1−δ)

k2 ≤|Ai ∩A′ j| ≤ m(1+δ)

k2 for all i, j ∈[k]. We say that balanced allocations A(1),..., A(D) are δ-IB if every pair among them is δ-IB.

A standard concentration argument shows that if m ≥ Θk,δ(log n), then n2k random balanced allocations satisfy δ-IB with high probability, as stated below.

Lemma 4. For any δ ∈(0, 1) and any m ≥4k4 δ2 · ln n such that m is divisible by k, let A(1),..., A(n2k) be balanced allocations drawn uniformly and independently at random. Then, with high probability, these allocations are δ-IB.

The remainder of this section is largely devoted to bounding the second moment as stated in the following lemma, where σ2 > 0 is the variance of D.

Lemma 5. For any fixed β ∈(0, 1), if δ ≤ β 12k4 and m ≥

48000k13 β2σ6, then for any pair of δ-IB balanced allocations A and A′, we have

Pr[EA′ | EA] ≤ 1 1 −β/2 −o(1) · kk/2

(2πn)

k−1

2.

Before we prove Lemma 5, let us sketch how to use it to establish Theorem 4. Let Ck,β,D = max n

4k4 δ2, 1920000k13 β2σ6 o

, where δ = β 12k4. The algorithm works as follows.

• Choose balanced allocations A(1),..., A(n2k) independently and uniformly at random.7

• For w ∈[n2k], check whether CEF,A(w) ∈P(N). If so, output (CEF,A(w), A(w)).

The algorithm runs in time nO(k) · m. To bound its success probability, note that by Lemma 4, A(1),..., A(n2k) are δ-IB with high probability. We condition on this event henceforth. Our algorithm succeeds when the event W w∈[n2k] EA(w) occurs. Using the second moment method, we can lowerbound the probability of this event by 1−β/2−o(1), which is at least 1 −β for any sufficiently large n.

We now proceed to prove Lemma 5. Fix two balanced allocations A, A′ that are δ-IB. For i, i′ ∈[k], we let8 p(i,i′) = Pr[i∗ a(A) = i ∧i∗ a(A′) = i′]. We will use the following lemma.

Lemma 6. For each a ∈N, let Xa be a random variable on {e1,..., ek} such that Pr[Xa = ei′] = k · p(⌈ka/n⌉,i′) for each i′ ∈[k]. Then, Pr[EA′ | EA] = Pr

X1 + · · · + Xn = n k · 1

.

The rest of the proof of Lemma 5 can be divided into two parts: (i) showing that the values p(i,i′) are all close to 1/k2, and (ii) bounding Pr

X1 + · · · + Xn = n k · 1

.

Part (i): Bounding p(i,i′). We need the following multivariate generalization of the Berry–Esseen theorem, which is stated as Theorem 1.1 in the work of Raiˇc (2019).9

Lemma 7 (Raiˇc 2019). Let W 1,..., W T be independent random variables in Rd with mean zero, H:= W 1 + · · · + W T, and Σ:= Cov[H] ∈ Rd×d be the covariance matrix of H. For any convex Λ ⊆ Rd, it holds that |Pr[H ∈Λ] −N(0, Σ){Λ}| ≤ 60d1/4 P i∈[T ] E[∥Σ−1

2 W i∥3 2].

Let us now give the proof overview for this part. We let d = k2 and implicitly associate10 tuples (j, j′) ∈[k]2 with elements in [k2] when writing the indices for readability.

7For example, we can take a random permutation of the goods, and let each block of m/k goods form a bundle.

8p(i,i′) is the same for every agent a, so we omit a from the notation.

9The version stated here follows from Theorem 1.1 of Raiˇc (2019) by letting Xi = Σ−1

2 W i, so that PT i=1 Var(Xi) = Id. Also, we use the term 60d1/4, which is weaker than the one used by Raiˇc (2019).

10For example, (j, j′) can be associated with k(j −1) + j′.

16959

<!-- Page 7 -->

Let µ denote the mean of D. For each g ∈M, we define the random variable W g ∈Rd such that

W g

(j,j′) =

(

(ua(g) −µ) · k σ√m if g ∈Aj ∩A′ j′; 0 otherwise for all j, j′ ∈[k]; note that this distribution is the same regardless of a. Then, let H = P g∈M W g. Moreover, for all i, i′ ∈[k], let Λi,i′ ⊆Rd be the set of all vectors v ∈Rd that satisfy the following constraints:

X ℓ∈[k]

v(i,ℓ) ≥

X ℓ∈[k]

v(j,ℓ) ∀j ∈[k];

X ℓ∈[k]

v(ℓ,i′) ≥

X ℓ∈[k]

v(ℓ,j′) ∀j′ ∈[k].

One can check that when there are no ties in utilities, i∗ a(A) = i and i∗ a(A′) = i′ if and only if H ∈Λi,i′. In other words, Pr[H ∈Λi,i′] is exactly p(i,i′). Since Λi,i′ is convex, Lemma 7 implies that p(i,i′) is close to N(0, Σ){Λi,i′} for Σ = Cov[H]. Using the fact that A, A′ are δ-IB and balanced, we can show that Σ is also close to the identity matrix Id. By applying a standard total variation distance bound between Gaussians, this also implies that N(0, Σ){Λi,i′} and N(0, Id){Λi,i′} are close. Due to symmetry, the latter is simply 1 k2. Thus, we can conclude that p(i,i′) itself is close to 1 k2, as stated more formally below. Lemma 8. Let γ ∈(0, 1). Suppose that δ ≤ γ 3k and m ≥

30000k7 γ2σ6. Then, for all i, i′ ∈[k], we have p(i,i′) −1 k2

≤γ.

Part (ii): Bounding Pr

X1 + · · · + Xn = n k · 1

. We reinterpret Xi so that it is a mixture distribution between the uniform distribution on {e1,..., ek} and a “leftover” distribution. In other words, for each Xi, we can toss a (biased) coin and, based on the outcome, sample Xi either from the uniform distribution or from the leftover distribution. By a concentration bound, we show that Xi is drawn from the uniform distribution for most indices i. For these Xi, their sum exactly follows the multinomial distribution, which we have a very good estimate on. From this, we can derive the following bound.

Lemma 9. Let ζ ∈ (0, 0.5) and ˜X1,..., ˜Xn be any independent random variables on {e1,..., ek} such that | Pr[ ˜Xa = ei] −1 k| ≤ ζ k for all a ∈N and i ∈[k]. If n ≥ k 1−2ζ, then Pr h

˜X1 + · · · + ˜Xn = n k · 1 i is at most exp

−2ζ2n

+ kk/2

(2π(1 −2ζ)n)

k−1

2.

Finally, combining Lemmas 6, 8, and 9 yields Lemma 5.

## 5.2 Non-Divisible Case

Next, we consider the case where m is not divisible by k. For this case, we prove that an envy-free outcome cannot exist with high probability unless m = Ω(√n). This differs markedly from the divisible case, where m = ω(log n) suffices for existence.

Theorem 5. For any fixed k ≥2, if m = o(√n) and m is not divisible by k, then with high probability, no envy-free outcome exists.

The proof of this non-existence result, like the divisible case (Theorem 3), uses the first moment method. The key distinguishing property between the two cases is encapsulated in the lemma below, which states that for any allocation A, there exists i ∈[k] such that pA i is noticeably smaller than 1 k; in particular, we may take i corresponding to a bundle with the smallest size. This is in contrast to the divisible case, where a balanced allocation gives pA i = 1 k for all i. Lemma 10. If m is not divisible by k, then for any A ∈A, there exists i ∈[k] such that pA i ≤1 k − α k2√m, where α > 0 is a constant depending only on D.

Lemma 10 implies the following upper bound on Pr[EA]. Lemma 11. If m is not divisible by k, then for any A ∈A, we have Pr[EA] ≤

√ k · exp

−α2 k4 · n m

, where α is the constant from Lemma 10.

We now finish the proof in a similar manner as Theorem 3.

Proof of Theorem 5. Using Observation 1 and Lemma 11 and taking the union bound over all A ∈A, the probability that an envy-free outcome exists is at most km ·

√ k · exp

−α2 k4 · n m

, which is o(1) because m = o(n/m).

When m = Ω(n log n), an envy-free outcome exists with high probability due to the result in the fixed-group setting by Manurangsi and Suksompong (2017). Tightening the gap between o(√n) and Ω(n log n) is an interesting question.

## 6 Conclusion

In this paper, we have studied fairness in the allocation of indivisible goods with variable groups, where a partition of the agents into groups can be chosen along with an allocation of the goods. We demonstrated that the flexibility afforded by this model allows strong envy-freeness guarantees to be made in both worst-case and average-case scenarios.

Besides closing the asymptotic gap in the non-divisible case (Section 5.2) and extending the asymptotic analysis in Section 5 to the case where groups may have differing sizes, an intriguing direction for future work is to make connections between the variable-group model and the setting of hedonic games (Aziz and Savani 2016). Specifically, in hedonic games, agents derive utilities from other agents assigned to the same group, and the objective is to find a desirable partition of the agents into groups; variants where the group sizes are fixed have also been considered (Bil`o, Monaco, and Moscardelli 2022; Li et al. 2023). A generalization of both models would therefore be to permit preferences both over agents as well as over goods—this can reflect, e.g., group projects where resources are assigned to each group.11 It would be interesting to investigate fairness guarantees that can be made in this general setting.

11A similar model has been studied under the name generalized group activity selection problem (Bil`o et al. 2019; Flammini and Varricchio 2022).

16960

<!-- Page 8 -->

## Acknowledgments

This work was partially supported by the Singapore Ministry of Education under grant number MOE-T2EP20221- 0001, by JST FOREST Grant Number JPMJFR226O, and by an NUS Start-up Grant. We would like to thank Erel Segal-Halevi for helpful discussions at the early stage, and the anonymous reviewers for their valuable comments.

## References

Asada, M.; Frick, F.; Pisharody, V.; Polevy, M.; Stoner, D.; Tsang, L. H.; and Wellner, Z. 2018. Fair division and generalizations of Sperner- and KKM-type results. SIAM Journal on Discrete Mathematics, 32(1): 591–610. Aziz, H. 2020. Developments in multi-agent fair allocation. In Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI), 13563–13568. Aziz, H.; and Savani, R. 2016. Hedonic games. In Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D., eds., Handbook of Computational Social Choice, chapter 15, 356–376. Cambridge University Press. Bai, Y.; Feige, U.; G¨olz, P.; and Procaccia, A. D. 2022. Fair allocations for smoothed utilities. In Proceedings of the 23rd ACM Conference on Economics and Computation (EC), 436–465. Bai, Y.; and G¨olz, P. 2022. Envy-free and Pareto-optimal allocations for agents with asymmetric random valuations. In Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI), 53–59. Barman, S.; Ebadian, S.; Latifian, M.; and Shah, N. 2025. Fair division with market values. In Proceedings of the 39th AAAI Conference on Artificial Intelligence (AAAI), 13589– 13596. Bei, X.; Igarashi, A.; Lu, X.; and Suksompong, W. 2022. The price of connectivity in fair division. SIAM Journal on Discrete Mathematics, 36(2): 1156–1186. Benad`e, G.; Halpern, D.; Psomas, A.; and Verma, P. 2024. On the existence of envy-free allocations beyond additive valuations. In Proceedings of the 25th ACM Conference on Economics and Computation (EC), 1287. Bil`o, V.; Caragiannis, I.; Flammini, M.; Igarashi, A.; Monaco, G.; Peters, D.; Vinci, C.; and Zwicker, W. S. 2022. Almost envy-free allocations with connected bundles. Games and Economic Behavior, 131: 197–221. Bil`o, V.; Fanelli, A.; Flammini, M.; Monaco, G.; and Moscardelli, L. 2019. Optimality and Nash stability in additive separable generalized group activity selection problems. In Proceedings of the 28th International Joint Conference on Artificial Intelligence (IJCAI), 102–108. Bil`o, V.; Monaco, G.; and Moscardelli, L. 2022. Hedonic games with fixed-size coalitions. In Proceedings of the 36th AAAI Conference on Artificial Intelligence (AAAI), 9287– 9295. Bouveret, S.; Cechl´arov´a, K.; Elkind, E.; Igarashi, A.; and Peters, D. 2017. Fair division of a graph. In Proceedings of the 26th International Joint Conference on Artificial Intelligence (IJCAI), 135–141.

Bouveret, S.; Chevaleyre, Y.; and Maudet, N. 2016. Fair allocation of indivisible goods. In Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D., eds., Handbook of Computational Social Choice, chapter 12, 284–310. Cambridge University Press. Bu, X.; Li, Z.; Liu, S.; Song, J.; and Tao, B. 2023. Fair division with allocator’s preference. In Proceedings of the 19th International Conference on Web and Internet Economics (WINE), 77–94. Caragiannis, I.; Larsen, K. G.; and Shyam, S. 2025. A new lower bound for multi-color discrepancy with applications to fair division. In Proceedings of the 18th International Symposium on Algorithmic Game Theory (SAGT), 228–246. Deng, X.; Qi, Q.; and Saberi, A. 2012. Algorithmic solutions for envy-free cake cutting. Operations Research, 60(6): 1461–1476. Dickerson, J. P.; Goldman, J.; Karp, J.; Procaccia, A. D.; and Sandholm, T. 2014. The computational rise and fall of fairness. In Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI), 1405–1411. Flammini, M.; and Varricchio, G. 2022. Approximate strategyproof mechanisms for the additively separable group activity selection problem. In Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI), 300–306. Gale, D. 1984. Equilibrium in a discrete exchange economy with money. International Journal of Game Theory, 13(1): 61–64. Ghodsi, M.; Latifian, M.; Mohammadi, A.; Moradian, S.; and Seddighin, M. 2018. Rent division among groups. In Proceedings of the 12th International Conference on Combinatorial Optimization and Applications (COCOA), 577– 591. G¨olz, P.; Igarashi, A.; Manurangsi, P.; and Suksompong, W. 2025. Fair allocation of indivisible goods with variable groups. CoRR, abs/2511.06218. G¨olz, P.; and Yaghoubizade, H. 2026. Fair division among couples and small groups. In Proceedings of the 40th AAAI Conference on Artificial Intelligence (AAAI). Forthcoming. Igarashi, A. 2023. How to cut a discrete cake fairly. In Proceedings of the 37th AAAI Conference on Artificial Intelligence (AAAI), 5681–5688. Igarashi, A.; and Meunier, F. 2025. Envy-free division of multilayered cakes. Mathematics of Operations Research, 50(3): 2261–2286. Kawase, Y.; Roy, B.; and Sanpui, M. A. 2025. Simultaneously fair allocation of indivisible items across multiple dimensions. In Proceedings of the 45th IARCS Annual Conference on Foundations of Software Technology and Theoretical Computer Science (FSTTCS). Forthcoming. Kurokawa, D.; Procaccia, A. D.; and Wang, J. 2016. When can the maximin share guarantee be guaranteed? In Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI), 523–529. Kyropoulou, M.; Suksompong, W.; and Voudouris, A. A. 2020. Almost envy-freeness in group resource allocation. Theoretical Computer Science, 841: 110–123.

16961

<!-- Page 9 -->

Li, L.; Micha, E.; Nikolov, A.; and Shah, N. 2023. Partitioning friends fairly. In Proceedings of the 37th AAAI Conference on Artificial Intelligence (AAAI), 5747–5754. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In Proceedings of the 5th ACM Conference on Electronic Commerce (EC), 125–131. Manurangsi, P.; and Meka, R. 2026. Tight lower bound for multicolor discrepancy. In Proceedings of the 9th SIAM Symposium on Simplicity in Algorithms (SOSA). Forthcoming. Manurangsi, P.; and Suksompong, W. 2017. Asymptotic existence of fair divisions for groups. Mathematical Social Sciences, 89: 100–108. Manurangsi, P.; and Suksompong, W. 2020. When do envyfree allocations exist? SIAM Journal on Discrete Mathematics, 34(3): 1505–1521. Manurangsi, P.; and Suksompong, W. 2021. Closing gaps in asymptotic fair division. SIAM Journal on Discrete Mathematics, 35(2): 668–706. Manurangsi, P.; and Suksompong, W. 2022. Almost envyfreeness for groups: Improved bounds via discrepancy theory. Theoretical Computer Science, 930: 179–195. Manurangsi, P.; and Suksompong, W. 2025. Ordinal maximin guarantees for group fair division. Theoretical Computer Science, 1036: 115151. Markakis, E. 2017. Approximation algorithms and hardness results for fair division. In Endriss, U., ed., Trends in Computational Social Choice, chapter 12, 231–247. AI Access. Raiˇc, M. 2019. A multivariate Berry–Esseen theorem with explicit constants. Bernoulli, 25(4A): 2824–2853. Segal-Halevi, E.; and Nitzan, S. 2019. Envy-free cakecutting among families. Social Choice and Welfare, 53(4): 709–740. Segal-Halevi, E.; and Suksompong, W. 2021. How to cut a cake fairly: a generalization to groups. American Mathematical Monthly, 128(1): 79–83. Sperner, E. 1928. Neuer Beweis f¨ur die Invarianz der Dimensionszahl und des Gebietes. Abhandlungen aus dem Mathematischen Seminar der Universit¨at Hamburg, 6: 265– 272. Su, F. E. 1999. Rental harmony: Sperner’s lemma in fair division. American Mathematical Monthly, 106(10): 930– 942. Suksompong, W. 2016. Asymptotic existence of proportionally fair allocations. Mathematical Social Sciences, 81: 62– 65. Walsh, T. 2020. Fair division: the computer scientist’s perspective. In Proceedings of the 29th International Joint Conference on Artificial Intelligence (IJCAI), 4966–4972. Yokoyama, T.; and Igarashi, A. 2025. Asymptotic existence of class envy-free matchings. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2244–2252.

16962
