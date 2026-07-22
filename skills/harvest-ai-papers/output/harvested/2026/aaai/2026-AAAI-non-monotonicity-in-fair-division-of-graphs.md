---
title: "Non-Monotonicity in Fair Division of Graphs"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38754
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38754/42716
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Non-Monotonicity in Fair Division of Graphs

<!-- Page 1 -->

Non-Monotonicity in Fair Division of Graphs

Hadi Hosseini1, Shraddha Pathak1, Yu Zhou2,*

1Penn State University 2Beijing Normal University hadi@psu.edu, ssp5547@psu.edu, yu.zhou@bnu.edu.cn

## Abstract

We consider the problem of fairly allocating the vertices of a graph among n agents, where the value of a bundle is determined by its cut value—the number of edges with exactly one endpoint in the bundle. This model naturally captures applications such as team formation and network partitioning, where valuations are inherently non-monotonic: the marginal values may be positive, negative, or zero depending on the composition of the bundle. We focus on the fairness notion of envy-freeness up to one item (EF1) and explore its compatibility with several efficiency concepts such as Transfer Stability (TS) that prohibits single-item transfers that benefit one agent without making the other worse-off. For general graphs, our results uncover a non-monotonic relationship between the number of agents n and the existence of allocations satisfying EF1 and transfer stability (TS): such allocations always exist for n = 2, may fail to exist for n = 3, but exist again for all n ≥4. We further show that existence can be guaranteed for any n by slightly weakening the efficiency requirement or by restricting the graph to forests. All of our positive results are achieved via efficient algorithms.

Extended version — https://arxiv.org/pdf/2511.03629

## Introduction

Fair division of indivisible items is a fundamental problem in multiagent systems and computational social choice. A central goal in fair division is to allocate a set of indivisible, non-shareable items among (potentially heterogeneous) agents in a manner that is both fair and efficient, guided by well-established axiomatic principles. However, much of the existing literature assumes that agents have additive, or otherwise monotonic valuations. These assumptions often fail to capture more realistic scenarios where the value of an item is non-monotonic and may depend on the composition of the bundle it belongs to.

In this paper, we initiate a formal study of non-monotonic bundle-dependent valuations, where the marginal value of an item may vary—potentially becoming negative— depending on the current bundle held by the agent. For instance, in settings such as team formation or committee selection with diverse expertise, the value of an additional

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

member, such as a goalkeeper, may vary significantly depending on the existing composition: they may be essential for a team lacking a substitute, but redundant or even burdensome for a fully staffed team due to added financial cost.

We focus on a specific class of bundle-dependent preferences based on cut-valuations defined over undirected graphs. In this model, items correspond to vertices of a graph G = (V, E), and an agent’s value for a bundle is determined by the number of edges that are cut, i.e. edges with exactly one endpoint in the bundle. Thus, the marginal value of an item is positive for bundle S if it has less neighbors inside S than outside S, otherwise it is zero or negative. This yields valuations that are inherently non-monotonic: adding an item can increase or decrease an agent’s utility depending on the underlying structure of the bundle.

We are interested in allocating vertices of the graph (corresponding to items) in a fair way while guaranteeing some notion of economic efficiency among the agents. Cutvaluations naturally model the aforementioned team formation problems that value fairness and diversity, where vertices represent individuals in a social or similarity graph and edges capture social ties or overlapping expertise. These non-monotonic valuations can also be seen as a soft relaxation of conflict constraints commonly studied in fair division (Hummel and Hetland 2022; Chiarelli et al. 2020; Li, Li, and Zhang 2021). Such interplay between constraintbased models and their valuation-based counterparts have been previously considered for matroids (Biswas and Barman 2019; Cookson, Ebadian, and Shah 2025; Barman and Verma 2020), as well as cardinality constraints and level valuations (Biswas and Barman 2018; Christodoulou and Christoforidis 2024).

## 1.1 Our Contributions

We consider the problem of partitioning general graphs, as well as forests, with a focus on simultaneously achieving fairness and economic efficiency. For fairness, we consider envy-freeness (EF), which informally requires that no agent strictly prefers another agents’ bundle; we also consider its well-studied relaxation, envy-freeness up to one (EF1), which requires that any pairwise envy is eliminated by removal of a single item. Under cut-valuations, allocating all vertices to a single agent is vacuously envy-free: all agents receive a value of zero. To avoid such degenerate outcomes,

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17059

<!-- Page 2 -->

we study fairness in conjunction with efficiency, including: (i) social optimality (SO), which maximizes total utility; (ii) Pareto optimality (PO), where no agent can be made better off without harming another. We also propose two natural and desirable efficiency notions: (iii) transfer stability (TS), prohibiting single-item transfers that benefit one agent without making the other worse-off; and (iv) weak transfer stability (WTS), forbidding transfers that strictly benefit both agents involved.1

General graphs. Our first set of results reveal an axiomatic non-monotonic relationship between existence guarantees for EF1+TS allocation and the number of agents n under cut-valuations: They exist for n = 2 (Proposition 1), may fail to exist for n = 3 (Theorem 1), but exist again for all n ≥4 (Theorem 2). The n = 3 counter-example also shows the incompatibility of EF1 with PO and SO. In contrast, the existence of EF1 and SO allocations follows a monotonic pattern: They always exist for n = 2, but may not exist when n ≥3 (see Theorem 5 in the extended version).

This raises a natural question: Is there an efficiency notion that is always compatible with EF1, regardless of n? We show that a slight relaxation of TS (WTS) is the strongest efficiency notion which can always be guaranteed alongside EF1, irrespective of n (Theorem 3). Moreover, such allocations can be computed in polynomial time. We also show that allocations that are 1

2-EF1, a multiplicative approximation of EF1, can co-exist alongside PO for arbitrary n (see Proposition 2 in the extended version).

We note that our EF1+WTS result (Theorem 3) also improves upon prior guarantees for equitable graph cut. Specifically, we show that the vertices of a graph can be partitioned into n parts such that the absolute difference between the cut-values of any two parts is bounded by the maximum degree ∆in the graph (Corollary 1). This improves on the previous bound of 5∆+ 1 by Barman and Verma (2025).

Forests. When the underlying graph is a forest (i.e. acyclic), we show that EF1 and SO allocations always exist and can be computed in polynomial time (Theorem 4). Interestingly, the standard techniques from the monotone settings—iteratively building toward an EF1 allocation where, on assigning each new item, EF1 is maintained as an invariant—do not apply to such special cases either. While our algorithm also iteratively builds towards an EF1 allocation, there are situations where we temporarily break intermediate EF1 guarantees, but ensure that such violations can be ‘caught-up’ through subsequent assignments.

Finally, we note that the negative counter-example we construct for showing the incompatibility of EF1 alongside various fairness notions under general graphs is in fact a complete bipartite graph with treewidth 2. This highlights that while strong existence and algorithmic guarantees hold for forests (bipartite graphs; treewidth 1), they break even for graphs that are only slightly different.

1In Appendix A of the extended version of the paper, we demonstrate that techniques developed for monotone valuations fail to extend to the cut-valuation setting.

All omitted material is available in the extended version of this paper.

## 1.2 Related works Fair Division under Non-monotone Valuations

Early works on non-monotone valuations focus on doubly monotone (often additive) valuations, where each item is either always a good (positive value) or a chore (negative value) for an agent, regardless of the bundle. In such settings, EF1 allocations always exist (Aziz et al. 2022; Bhaskar, Sricharan, and Vaish 2020). The existence of EF1+PO allocations remains open, even in the simple additive case (Liu et al. 2024). While such allocations are known for (additive) goods-only instances (Caragiannis et al. 2019), their existence in chores-only settings was only recently established (Mahara 2025). Recent work either relaxes EF1 (Barman et al. 2025) or focuses on specific valuations (Hosseini, Mammadov, and W ˛as 2023). More general non-monotone settings—where items act as goods or chores depending on the bundle—have been recently explored under special classes such as subadditive, non-negative valuations2, identical trilean, and separable single-peaked (Barman and Verma 2025; Bilò, Loebl, and Vinci 2025; Bhaskar et al. 2025).

Fair Division of Graphs Graphs appear in fair division both as feasibility constraints (e.g. conflicting or connectivity (Hummel and Hetland 2022; Chiarelli et al. 2020; Li, Li, and Zhang 2021; Kumar et al. 2024; Igarashi, Manurangsi, and Yoneda 2025; Bouveret et al. 2017; Bei et al. 2022; Bilò et al. 2022)), and to define agents’ valuations (e.g. from graphical structures such as shortest paths (Hosseini, Narang, and W ˛as 2025; Hosseini and Schierreich 2025), minimum vertex cover (Wang and Li 2024), or edge-based models where each item (an edge) is valued by exactly two agents (the incident vertices) (Christodoulou et al. 2023; Deligkas et al. 2024; Zhou et al. 2024)). A related line of research considers partitioning of friends into groups that are balanced and fair (Li et al. 2023; Deligkas et al. 2025). Here, an agents utilities are monotone and based on intragroup connections. In contrast, our model captures nonmonotonic, bundle-dependent preferences, arising in problems where inter-group connections are valued.

## Preliminaries

Given any j, k ∈N such that j ≤k, let [k]:= {1,..., k}, and [j, k]:= {j, j + 1,..., k}.

An instance of the cut-valuation problem is denoted by ⟨N, G, v⟩, where N = {1, 2,..., n} is the set of n agents, G = (V, E) is an undirected graph with |V | = m vertices and |E| edges, and a cut-valuation v. The vertex set V corresponds to the set of items to be distributed among the agents; throughout the paper, we use items and vertices interchangeably. The edge between any two adjacent vertices o, o′ is denoted by e = (o, o′). The neighbors of o within the set S is denoted by NS(o):= {o′ ∈S: (o, o′) ∈E}. The degree of o, denoted by deg(o):= |NV (o)|, is the number of its

2We note that cut-valuations studied in this paper are a subclass of non-negative and were discussed in (Barman and Verma 2025).

17060

<!-- Page 3 -->

o1 o2 o3 o4 o5 o6 o7 o8

S

T

U

W

**Figure 1.** Graph with 8 items (vertices).

neighbors in G. A graph is a forest if it is acyclic. Note that a graph may contain multiple disconnected components.

Cut-Valuations. The cut-valuation v: 2V →R defines the cardinal preferences of the agents for any subset of items in V. Specifically, the cut-value of any subset S is v(S):= |{(o, o′) ∈E: o ∈S and o′ ∈V \ S}|, which is the number of edges that have one endpoint in S and the other endpoint in V \ S. Crucially, the cut-valuation represents a subclass of non-monotone valuations, where an item o has a positive marginal value for a bundle S if and only if o has more neighbors outside of S than in S, i.e. |NS(o)| < |NV \S(o)|. Otherwise, o may have a negative or non-positive marginal value. For the ease of exposition, we refer to an item with positive marginal value (with respect to a subset) as a good, otherwise it is called a chore (with respect to the subset). Without loss of generality, we assume (i) |V | > n, and (ii) G has no singleton components because such vertices have zero value and can be assigned arbitrarily.

Allocation. An allocation A = (A1,..., An) is a partition of vertices (items) into n pairwise disjoint subsets of V, i.e., for every Ai, Aj ⊆V, Ai ∩Aj = ∅. Each part Ai contains a bundle of items assigned to agent i ∈N. Note that the items in Ai may not be adjacent. An allocation may be partial when ∪i∈NAi ⊊V, or complete when ∪i∈NAi = V.

Let us review the cut-valuations and potential allocations using Example 1.

Example 1 (Allocations and cut-valuations). Consider the graph in Figure 1. The cut-value of the set S = {o1} is v(S) = 4. However, the set T that is obtained by adding an item o3 to S reduces the cut-value to v(T) = 3. In other words, o3 is a chore for the set S. However, o3 is a good for set W = {o2} since addition of o3 to W results in the set U that has a cut-value of v(U) = 2, whereas v(W) = 1.

Remark 1 (Relation to Graph Partitions). In graph theory, a k-partition of a graph G = (V, E) is a division of V into k disjoint subsets V = V1 ∪· · · ∪Vk, where Vi ∩Vj = ∅for all i̸ = j, where Vi may be subject to additional structural constraints such as being connected subgraphs or forming independent sets. In our model, an allocation corresponds to a complete partition of V into n bundles (A1,..., An), one for each agent. Our framework does not impose a connectivity constraint, i.e. multiple disconnected components may be allocated as a bundle (say Ai) to an agent.

Fairness. An allocation A = (A1,..., An) is envy-free (EF) if every agent values their own bundle at least as much as that of any other agent’s bundle, i.e., v(Ai) ≥v(Aj) for every two agents i, j ∈N. An allocation A is envy-free up to one item (EF1) if for every pair of agents i, j ∈N where v(Aj) > v(Ai), there exists an item oj ∈Aj such that v(Ai) ≥v(Aj \ {oj})3 (Lipton et al. 2004; Budish 2011).

In Example 1, although v(T) > v(W), the (hypothetical) removal of o1 ∈T eliminates the envy. Note that in this setting, the existence of an EF1 allocation is particularly delicate due to the non-monotonicity of valuations since removing a single item (vertex) may sometimes increase the agent’s value. In this example, the removal of o3 ∈T in fact increases the value of T from 3 to 4.

Efficiency. In our setting, fairness alone may not be sufficient to rule out undesirable allocations. For instance, allocating all vertices to a single agent is envy-free, however, all agents receive a value of zero. Thus, we consider non-empty allocations wherein each agent receives at least one item and define several plausible efficiency notions.

An allocation, A, is Social Optimal (SO) if it maximizes the utilitarian social welfare, i.e., A ∈ arg maxX∈Πn(V)

P i∈N v(Xi), where Πn(V) denotes the set of all n-partitions of V. An allocation A is Pareto Optimal (PO) if it is not Pareto dominated by another allocation, that is, no other allocation B exists such that v(Bi) ≥v(Ai) for every i ∈N with at least one inequality being strict.

An allocation, A = (A1,..., An), is Transfer Stable (TS) if, for every i, j ∈N, there does not exist an item o ∈Ai such that v(Ai \ {o}) ≥v(Ai) and v(Aj ∪{o}) ≥ v(Aj) with at least one inequality being strict. Allocation A is Weak Transfer Stable (WTS) if, for every i, j ∈N, there does not exist an item o ∈Ai such that v(Ai \{o}) > v(Ai) and v(Aj ∪{o}) > v(Aj). Informally, a TS allocation requires that no single item can be transferred from an agent to another without making either agent worse-off while increasing the value of at least one of the two agents. It is WTS if no such transfer exists that necessarily makes both agents strictly better-off. It is easy to see that SO =⇒PO =⇒ TS =⇒ WTS while the converse directions do not hold. For an example that illustrates these notions, we refer the reader to Example 2 in the extended version.

General Graphs In this section, we study general graphs that may contain cycles. Our first set of results reveal a non-monotonic relationship between existence guarantees for EF1+TS allocation and the number of agents under cut-valuations: They exist for n = 2, may fail to exist for n = 3, but exist again for all n ≥4. Interestingly, this non-monotonic dependence is not present for SO. In Appendix B of the extended version, we provide a family of instances for every n ≥3 agents such that no allocation is simultaneously EF1 and SO.

## 3.1 Two Agents: Existence

To warm up, we start by considering the case of n = 2, and give an existence guarantee for EF and SO: Since the cut function of a graph G is symmetric, i.e. v(S) = v(V \ S)

3We refer the reader to Appendix A in the extended version for a discussion on alternative definitions of EF1 used in the literature.

17061

<!-- Page 4 -->

oa ob oc1 oc2 ocd−1 ocd · · ·

**Figure 2.** An example showing the incompatibility of EF1 and transfer stability (TS) for n = 3.

for any S ⊆V, any partition between two agents is EF. Moreover, an allocation is SO if and only if it is PO, because the cut-values are symmetric and an increase in the value of one agent leads to an increase in value for both. Proposition 1. When n = 2, an allocation satisfying EF and SO always exists, but computing such an allocation is NP-HARD. Moreover, an allocation satisfying EF and TS always exists and can be computed in polynomial time.

Proof. For two agents, every allocation is EF due to symmetry of cut-valuations. Thus, the problem reduces to finding an SO partition. The symmetry of valuations means that the partition corresponding to the maximum cut is SO. That is, a MAX-CUT results in EF+SO; however, since computing a MAX-CUT is NP-HARD (Garey, Johnson, and Stockmeyer 1974), the hardness follows. Focusing on TS, we devise a simple greedy algorithm as follows: Start with an arbitrary 2-partition of the graph, say A = (V, ∅), and iteratively transfer an item from one bundle to the other such that the value of the bundles increases. The value can increase at most O(m2) times since, the value increases by at least 1 in each round and for any set S, v(S) ≤|E| where |E| ∈O(m2) for simple graphs. Again, by symmetry of cut-valuations for 2-partitions, the final allocation after the greedy process is also EF.

## 3.2 Three Agents: Non-existence

While for n = 2, EF+TS always admits a polynomial-time solution, we show that for n = 3, even EF1—a strictly weaker notion than EF—is incompatible with TS (and thus, with PO and SO as well). Theorem 1 (Non-existence of EF1+TS allocations). There exists a cut-valuation instance with n = 3 agents where no EF1 allocation is TS (and thus PO and SO).

Proof. Consider the instance with 3 agents and d + 2 items, oa, ob and oct where t ∈[d] as shown in Figure 2. Suppose d ≥3 and that d is odd. In any EF1 allocation, oa and ob must be allocated to different agents; if not, i.e., if A1 = {oa, ob}, then one of the remaining two agents will receive a value of at most 2 d

2

< d = v(A1 \ {oa}) = v(A1 \ {ob}), which violates EF1. Thus, oa is allocated to agent 1 (red) and ob to agent 2 (blue).

After allocating d

2 of the remaining items to the third agent (yellow), no new item can be allocated to A3 without breaking EF1 because each item has marginal value of two for agent 3, and on addition of any new item o ∈

{o⌈d

2⌉+1,..., ocd}, we have v(A3 ∪{o} \ {o′}) = 2⌈d 2⌉> d = v(A1) = v(A2) for any o′ ∈A3 ∪{o}. Thus, all the remaining items must be (wastefully) allocated to either agent 1 or 2 in order to maintain EF1. In Figure 2, they are arbitrarily allocated to agent 1 (red). But the marginal values of these items are 0 for both agents 1 and 2; thus, to maintain TS these items should be transferred to agent 3, which whereas violates EF1.

While Theorem 1 shows the incompatibility of EF1 with TS, PO, and SO, the EF1 allocation marked in Figure 2 satisfies the weaker WTS condition. In fact, as we show in Section 3.4, allocations that are both EF1 and WTS always exist and can be computed in polynomial time.

## 3.3 Four or More Agents: Existence

Surprisingly, when n ≥4, EF1 and TS allocations always exist and can be computed in polynomial time.

Theorem 2 (EF1+TS allocations when n ≥4). When n ≥4, a complete allocation satisfying EF1 and TS always exists and can be computed in polynomial time.

Before presenting the main algorithm for our constructive proof, we observe that, under identical valuations, if the allocation is ordered from the least to the highest valued bundle, then the allocation is EF1 if and only if the agent with the least-valued bundle is not involved in any EF1 violation; we refer the readers to the extended version for the proof. This lemma enables us to restrict attention to EF1 violations involving only the agent with the least-valued bundle.

Lemma 1. Given an instance with identical valuations and allocation A = (A1,..., An) such that v(A1) ≤... ≤ v(An), A is EF1 if and only if, for every j ∈N with v(Aj) > v(A1), there exists an item oj ∈Aj s.t. v(A1) ≥ v(Aj \ {oj}).

## Algorithm

1 operates over the space of complete allocations and performs local search to eliminate EF1 violations. A subroutine (Algorithm 2) is repeatedly invoked to enforce TS by reassigning items whose marginal value to the current holder is weakly negative.

## Algorithm

Description. Algorithm 1 starts with any arbitrary complete allocation. Since agents have identical valuation functions, any bundle can be assigned to any agent. Thus, throughout the algorithm, the bundles are sorted in non-decreasing order of value i.e. v(A1) ≤v(A2) ≤... ≤ v(An). The algorithm proceeds by iteratively resolving pairwise EF1 violations in two cases: In Case I, we run a local search repeatedly to find a bundle, say Ai, such that i) Ai violates EF1 with respect to the lowest valued bundle A1, and ii) there exists an item o ∈Ai with strictly positive marginal value for agent 1, i.e. v(A1 ∪{o}) > v(A1). In this case, we transfer the item to A1, update the labels, and repeat. Otherwise, we are in the case (Case II) where agent 1’s violation of EF1 towards another bundle, say Ai∗, cannot be remedied by transferring an item from Ai∗to A1 since all items in Ai∗are of a non-positive marginal value for agent 1. In this case, the algorithm transfers an item o′ ∈Ai∗to another

17062

<!-- Page 5 -->

## Algorithm

1: Computing EF1 + TS allocations on general graphs when n ≥4

1: Initialize A = (A1,..., An) arbitrarily with any complete allocation. 2: Relabel bundles s.t. v(A1) ≤· · · ≤v(An). 3: A ←TS-SUBROUTINE(None; A) 4: while (∃EF1 violation from agent 1 to some other agent) do

▷Case I (Lines 5–9): When there exists an item in an EF1violator’s bundle with positive marginal value for A1.

5: while (there exists EF1 violation towards an agent i, s.t. v(A1 ∪{o}) > v(A1) for some o ∈Ai) do 6: Transfer item o to A1 7: Relabel bundles s.t. v(A1) ≤· · · ≤v(An) 8: A ←TS-SUBROUTINE(None; A) 9: end while

▷Case II (Lines 10–14): When all items in the EF1-violator’s bundle have non-positive marginal value for A1.

10: while (there exists EF1 violation from agent 1 to special agent i∗and v(A1) ≥v(A1 ∪{o}) for every o ∈Ai∗) do 11: Transfer any such item o to another agent, k̸ = i∗, s.t. v(Ak ∪{o}) > v(Ak) 12: end while 13: Relabel bundles s.t. v(A1) ≤· · · ≤v(An). 14: A ←TS-SUBROUTINE(i∗; A) 15: end while bundle, say Ak, for whom v(Ak ∪{o′}) > v(Ak). This process repeats until there is no EF1 violations from agent 1 to i∗. The key observation is that when the algorithm is in Case II, there is an EF1 violation with respect to only a single agent (see Claim 2 below); thus, it suffices to consider only a single special agent i∗. Note that to maintain efficiency, after each transfer, the algorithm invokes the TS subroutine (Algorithm 2) described next.

Maintaining Efficiency TS-Subroutine. This subroutine (Algorithm 2) takes as input a complete allocation and a designated special agent (call it i∗), and returns a TS allocation in which no agent is worse-off compared to the input allocation. The special agent is used solely to ensure that, in certain cases, its bundle remains unchanged; which becomes critical when arguing the convergence of the algorithm (see the next paragraph). The subroutine iteratively identifies an agent holding an item with non-positive marginal value and transfers that item as follows: If the agent with the nonpositive marginal value item is the one with the least-valued bundle (aka agent 1), the item is transferred to any bundle (excluding the special agent i∗) where it has strictly positive marginal value; otherwise, it is transferred to the least-valued bundle i.e., A1, if it provides strictly positive marginal value there; if not, it is transferred to any agent (excluding the special agent i∗) for whom the item has strictly positive marginal value. This process continues until no such item remains, yielding a TS allocation.

## Algorithm

2: Transfer Stability (TS-SUBROUTINE) Input: Special agent i∗and a complete allocation A = (A1,..., An) s.t. v(A1) ≤· · · ≤v(An) Output: A TS allocation s.t. v(A1) ≤· · · ≤v(An)

1: while (there exists an agent i ∈N with an item o ∈Ai s.t. v(Ai) ≤v(Ai \ {o}) do 2: If i = 1 (least valued bundle), then transfer o to an agent k̸ = i∗s.t. v(Ak ∪{o}) > v(Ak); 3: Else if i̸ = 1 and v(A1 ∪{o}) > v(A1), then transfer o to A1; 4: Else transfer o to any agent k̸ = i∗s.t. v(Ak ∪{o}) > v(Ak). 5: Relabel the bundles s.t. v(A1) ≤· · · ≤v(An). 6: end while

The Importance of n ≥4 and Special Agent. The structure of cut-valuations imposes a limit on the number of agents who can view a given item as a chore (non-positive marginal value); as we show in Lemma 2, this can be at most two such agents. This means that when n ≥3, in a TS allocation, each item must be assigned to an agent who values it positively. As shown in Theorem 1, sometimes this constraint conflicts with the EF1 requirement.

When n ≥4, this bound on the number of agents guarantees the existence of multiple agents for whom an item is positively valued. This enables series of transfer to obtain EF1 when direct transfers to the least valued agent may not be possible: An item can be transferred to another agent who values it positively, and if needed, another item from their bundle can be passed to A1. To ensure polynomial-time termination, we sometimes need to treat an agent as “special” and not alter its bundle during the TS-SUBROUTINE. In such cases, we again rely on the n ≥4 condition to guarantee that there exists another agent—distinct from the special agent— who values an item positively.

Lemma 2. Given a cut-valuation instance and a (partial) allocation, any item o ∈V has non-positive marginal value for at most two agents. Moreover, when n ≥4, item o has positive marginal value for at least two agents.

While the formal proof of the lemma is relegated to the extended version, an intuition for it can be obtained from Figure 3.

o

Ai

Aj Ak

Item o has negative marginal value for at most one agent.

o

Ai

Aj

Ak

Item o has zero marginal value for at most two agents

**Figure 3.** An illustration of the characterization in Lemma 2.

Before proving Theorem 2, we first present three key technical claims. First, we show that each agent derives at least half the total value of all bundles that contain only items with non-positive marginal value to that agent.

17063

<!-- Page 6 -->

Claim 1. For an agent i ∈N, consider any set of bundles X such that for every bundle Ak ∈X, it holds that v(Ai) ≥ v(Ai ∪{o}) for every o ∈Ak. Then, we have v(Ai) ≥1

2

X

Ak∈X v(Ak).

Using this claim, it is easy to see that when Case II happens, i.e., when there is EF1 violation from agent 1 to some agent i∗but Ai∗does not have any item with positive marginal value for A1, such a violation can only be towards a single agent. Thus, all remaining bundles contain at least one item with positive marginal value. Claim 2. Let X be the set of all bundles towards which the first agent (agent with least valued bundle) has EF1 violations. If, for every bundle Ak ∈X and o ∈Ak we have v(A1) ≥v(A1 ∪{o}), then |X| ≤1. Moreover, for any other bundle Aj /∈X, there exists an item o′ ∈Aj such that v(A1 ∪{o′}) > v(A1).4

To argue about the termination of the main algorithm, Algorithm 1, we use a lexicographic improvement in the vector Φ = (v(A1), −n1), where v(A1) represents the value of the least-valued bundle and n1 represents the number of agents with this least-value. Finally, to prove that the TS- SUBROUTINE terminates in polynomial time, we again use a potential argument; in particular, we show that the social welfare strictly increases and Φ does not decrease. Claim 3. The TS-SUBROUTINE returns an allocation that is TS. Furthermore, in each iteration of Algorithm 2, the potential function Φ = (v(A1), −n1) does not decrease, and the social welfare SW(A) = P i∈N v(Ai) increases by at least 1. Therefore, Algorithm 2 terminates in O(m2) time.

We are now ready to prove Theorem 2.

Proof of Theorem 2. First, we show that if Algorithm 1 terminates, then the resulting allocation is both EF1 and TS. After that, we prove that the algorithm terminates in polynomial time. By the main while loop in Line 4, the algorithm continues until agent 1 (the agent with the least value) no longer has an EF1 violation towards any other agent. By Lemma 1, this ensures that the allocation is EF1. Next, from Claim 3, we know that the TS-SUBROUTINE guarantees that the resulting allocation is TS. Since this subroutine is called in Lines 8 and 14, the final allocation also satisfies TS.

We now prove that the algorithm terminates in polynomial time. We show that (i) in every iteration of Case I there is a lexicographic improvement in Φ = (v(A1), −n1); and (ii) in Case II, either (a) either Φ is lexicographically improved, or (b) when Φ does not change, the algorithm moves back to Case I. Since each part of the algorithm runs in polynomial time—v(A1) can increase at most O(|E|) ∈O(m2) times, n1 can decrease at most O(n) times, the while loop is Case II runs in O(m) time, and the social welfare can improve at

4Notice that the same proof also implies that if agent 1 envies (not necessarily EF1-envies) exactly one agent i and all items in Ai have non-positive value with respect to agent 1, then every other agent has an item with a positive marginal value for agent 1. This generalization helps us prove Theorem 2.

most O(m2) times (which is the potential function for the TS-SUBROUTINE; see Claim 3)—the algorithm terminates in time polynomial in n and m. Case I. Let i be an agent for whom there is an EF1 violation and let o ∈Ai be an item with positive marginal value for A1. After reallocating o to agent 1, the value of A1 strictly increases. In addition, since there was a EF1 violation towards i, we know Ai’s new value is still strictly larger than previous least value i.e. v(Ai \ {o}) > v(A1). If v(A2) = v(A1), the minimum value does not change, but the number of agents receiving the minimum value n1 decreases by 1. Otherwise, the minimum value increases by at least 1 and thus Φ lexicographically improves. Case II. First, we show that in Case II, Φ does not decrease. From Claim 2, we know that any EF1 violation must be towards a single special agent i∗and all items in Ai∗have a non-positive marginal value for A1. In this case, an arbitrary item o ∈Ai∗is transferred to an agent k̸ = i∗who has positive marginal value for o; the existence of such an agent k̸ = i∗is guaranteed via Lemma 2 when n ≥4. Note that v(A1) does not change since A1’s bundle is untouched, and no agent becomes worse than v(A1): Agent i∗is EF1envied by agent 1 so v(Ai∗\ {o}) > v(A1), and o has a positive marginal value for Ak.

Thus, for Case II, we need to show that if Φ does not lexicographically increase and the allocation is not EF1, then we must move back to Case I, i.e. there cannot be two consecutive runs of Case II unless the potential function Φ increases. To see this, notice that after the execution of the subroutine in Line 14, if the resulting allocation is not EF1+TS and v(A1) and n1 (i.e. Φ) remain unchanged, then the least valued agent remains agent 1. This is because, from Claim 3, we know that the subroutine does not make any agent worseoff. Also, since Ai∗was TS before Case II (i.e. contained no non-positive items for itself), it must be the case that i∗was not involved in any transfers during the subroutine execution. Thus, any EF1-violation must be towards a different agent since agent 1 did not EF1-envy i∗after Case II. Moreover, since the least valued agent is still agent 1 and (the new) Ai∗is still an envied bundle with no items that have a positive marginal value for A1, from Claim 2, the new EF1envied agent must have an item with positive marginal value for A1, satisfying the condition for Case I.

## 3.4 EF1 and Efficiency: A Monotonic Result

We have shown that EF1 and the efficiency notion TS exhibits non-monotonic existence. This raises a natural question: Is there an efficiency notion that is always compatible with EF1, regardless of n? We answer this question positively by showing that a slight relaxation of TS–namely WTS–is guaranteed to exist along with EF1 for any n. Theorem 3 (EF1+WTS allocations). Given a cut-valuation instance, a complete allocation satisfying EF1 and WTS always exists and can be computed in polynomial time.

Our proof is constructive: we provide an algorithm, akin to Algorithm 1, that computes such an allocation for any instance. The full algorithm and proof of Theorem 3 can be found in the extended version of the paper. Intuitively, unlike

17064

<!-- Page 7 -->

TS which requires each item to have positive marginal in its bundle, WTS permits items to have zero-marginals. This forgoes the need for multiple agents with positive value for an item, removing the need for n ≥4 (Lemma 2).

As a corollary, Theorem 3 implies that any graph with m vertices admits a non-empty n-partition of the vertex set (with n ≤m) with nearly-equitable the cut-values across parts. Notably, the bound of ∆in Corollary 1 improves on the previous best of 5∆+ 1 by Barman and Verma (2025).

Corollary 1 (Equitable graph cuts). Given a graph G = (V, E) and an integer n ≤|V |, there exists a polynomial-time computation n-partition of V into nonempty V1, V2,..., Vn̸ = ∅such that the cut-values satisfy |v(Vi) −v(Vj)| ≤∆for all i, j ∈[n], where ∆:= maxo∈V deg(o) denotes the maximum degree of G.

## 4 Forest Graphs

In this section, we provide a polynomial-time algorithm that takes as input a cut-valuation instance where the graph G = (V, E) is a forest (i.e. acyclic), and outputs an allocation that is simultaneously EF1 and socially optimal (SO). This algorithmic guarantee also shows the existence of such allocations for forest graphs. Our first observation is a characterization of SO allocations for forests: When n ≥2, no two adjacent items can be allocated to the same agent.

Proposition 2. Given a cut-valuation instance where G is a forest and n ≥2, an allocation A is SO if and only if, for every (o, o′) ∈E, we have o ∈Ai and o′ ∈Aj̸ = Ai.

This is because forests are bipartite graphs and for such graphs, a MAX-CUT partition ensures all edges in the graph contribute toward the cut-value; we refer the reader to the extended version for a formal proof of the proposition. As consequence of Proposition 2, the problem of finding an allocation that is EF1 and SO is equivalent to finding an EF1 allocation where no adjacent vertices (items) are assigned to the same agent. Under this condition, agent’s bundle forms an independent set S in the graph, with v(S) = P o∈S deg(o). This coincides with the conflict-constraints, albeit for valuations derived from cut-functions.

Note that for n = 2, the bi-partition based on the bipartite graph of the forest is both EF and SO since the cut function is symmetric, i.e. v(S) = v(V \ S) for any S ⊆V 5; thus we assume n ≥3. Interestingly, the negative example in Theorem 1 is also a bipartite graph (with treewidth = 2), but an EF1+SO allocation does not exist for it when n = 3. This highlights that while strong existence and algorithmic guarantees (EF1+SO) hold for forests (bipartite; treewidth 1), they break even for graphs that are only slightly different.

## Algorithm

Overview. We begin with an empty initial allocation and an arbitrary rooting of each tree in the forest. The algorithm proceeds iteratively: at each step, it assigns a root item (vertex) to an agent and roots the resulting subtrees at the unallocated neighbors (children) of the assigned item. We always exclusively assign root items; thus, at most one of their neighbors (the parent) may have already been

5This is true for n = 2 and any bipartite graph (not just forests).

assigned. Therefore, to satisfy the SO condition, it suffices to ensure that the assigned root item is not in the same bundle as its parent. Such a root whose parent does not belong to the bundle is a feasible root (for that bundle).

Whenever a feasible root exists for the least-valued agent (agent 1) the algorithm assigns this to A1 under CASE 1. CASES 2 and 3 handle situations where no root is feasible for A1. Here, we assign a root item to another agent, temporarily violating the EF1 condition. However, it is carefully designed to catch up on such violations through subsequent assignments. In particular, the algorithm proceeds by checking for the following three conditions sequentially:

• CASE 1: Is there a feasible root ot for the least-valued agent (agent 1)? • CASE 2: Can we allocate a feasible root ot to the second least-valued agent (agent 2) such that any resulting EF1 violation can be compensated for? • CASE 3: Is there an agent j̸ = 1, 2 who can receive a feasible root ot such that any resulting EF1 violation can be remedied? Theorem 4 (Existence of EF1 + SO allocations). Given cut-valuation instance where G = (V, E) is a forest, a complete allocation that is EF1 and SO always exists and can be computed in polynomial time.

The algorithm, by construction, always assigns feasible root items, thereby ensuring that no two adjacent items are allocated to the same agent, i.e., the returned allocation is SO. For EF1, assigning an item to agent 1 in CASE 1 preserves EF1, since on removal of the last added item, A1 was the least-valued bundle. In contrast, when an item ot is assigned to an agent j̸ = 1, each child of ot (unallocated neighbor of ot) becomes a feasible root item for agent 1, where each child has a value of at least 1. Note that ot has at least v({ot})−1 (unassigned) children (since at most one neighbor of ot, i.e. its parent has been assigned so far). Thus, agent 1 can be almost compensated for the resulting EF1violation (of at most v({ot}) toward j! CASES 2 and 3 capture cases where this EF1-violation can be fully eliminated.

It remains to show that at least one of the three CASES always holds whenever an item remains to be allocated. The proofs of these guarantees and the precise algorithm for Theorem 4 are provided in the extended version.

## 5 Concluding Remarks

We studied the compatibility of EF1 with various efficiency guarantees under cut-valuations, noting surprising non-monotonicity in existence guarantees against the number of agents. Since cut-valuations are identical, all results extend to EQ-based fairness notions. Future work includes exploring stronger notions such as EFX, or weaker fairness requirement with stronger efficiency guarantees. In the extended version, we show that a 1

2-EF1+PO allocation always exists. While the approximation factor cannot improve beyond 2

3 (Theorem 1), it remains open whether (and how far) it can be improved. Finally, understanding the complexity of deciding whether a given instance admits an EF1 allocation satisfying a target efficiency criterion X ∈{TS, PO, SO} is an interesting future direction.

17065

<!-- Page 8 -->

## Acknowledgments

This research was supported by the National Science Foundation (NSF) through CAREER Award IIS-2144413 and Award IIS-2107173. Yu Zhou is supported by Research Start-up Funds of Beijing Normal University at Zhuhai (No. 310425209505). We thank the anonymous reviewers for their fruitful comments. We are grateful to Siddharth Barman for introducing this problem, and for many helpful discussions.

## References

Aziz, H.; Caragiannis, I.; Igarashi, A.; and Walsh, T. 2022. Fair allocation of indivisible goods and chores. Auton. Agents Multi Agent Syst., 36(1): 3. Barman, S.; HV, V. P.; Sethia, A.; and Suzuki, M. 2025. Fair and Efficient Allocation of Indivisible Mixed Manna. arXiv preprint arXiv:2507.03946. Barman, S.; and Verma, P. 2020. Existence and computation of maximin fair allocations under matroid-rank valuations. arXiv preprint arXiv:2012.12710. Barman, S.; and Verma, P. 2025. Fair Division Beyond Monotone Valuations. arXiv preprint arXiv:2501.14609. Bei, X.; Igarashi, A.; Lu, X.; and Suksompong, W. 2022. The price of connectivity in fair division. SIAM journal on Discrete Mathematics, 36(2): 1156–1186. Bhaskar, U.; Kumar, G.; Pandit, Y.; and Rakshitha. 2025. Towards Envy-Freeness Relaxations for General Nonmonotone Valuations. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems, 298–306. Bhaskar, U.; Sricharan, A.; and Vaish, R. 2020. On approximate envy-freeness for indivisible chores and mixed resources. arXiv preprint arXiv:2012.06788. Bilò, V.; Caragiannis, I.; Flammini, M.; Igarashi, A.; Monaco, G.; Peters, D.; Vinci, C.; and Zwicker, W. S. 2022. Almost envy-free allocations with connected bundles. Games and Economic Behavior, 131: 197–221. Bilò, V.; Loebl, M.; and Vinci, C. 2025. On Almost Fair and Equitable Allocations of Indivisible Items for Non-monotone Valuations. arXiv preprint arXiv:2503.05695. Biswas, A.; and Barman, S. 2018. Fair Division Under Cardinality Constraints. In IJCAI, 91–97. ijcai.org. Biswas, A.; and Barman, S. 2019. Matroid Constrained Fair Allocation Problem. In AAAI, 9921–9922. AAAI Press. Bouveret, S.; Cechlárová, K.; Elkind, E.; Igarashi, A.; and Peters, D. 2017. Fair Division of a Graph. In IJCAI, 135–141. ijcai.org. Budish, E. 2011. The combinatorial assignment problem: Approximate competitive equilibrium from equal incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The unreasonable fairness of maximum Nash welfare. ACM Transactions on Economics and Computation (TEAC), 7(3): 1–32. Chiarelli, N.; Krnc, M.; Milaniˇc, M.; Pferschy, U.; Pivaˇc, N.; and Schauer, J. 2020. Fair packing of independent sets. In Combinatorial Algorithms: 31st International Workshop, IWOCA 2020, Bordeaux, France, June 8–10, 2020, Proceedings 31, 154–165. Springer. Christodoulou, G.; and Christoforidis, V. 2024. Fair and Truthful Allocations Under Leveled Valuations. arXiv preprint arXiv:2407.05891.

Christodoulou, G.; Fiat, A.; Koutsoupias, E.; and Sgouritsa, A. 2023. Fair allocation in graphs. In Proceedings of the 24th ACM Conference on Economics and Computation, 473–488. Cookson, B.; Ebadian, S.; and Shah, N. 2025. Constrained fair and efficient allocations. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 13718–13726. Deligkas, A.; Eiben, E.; Goldsmith, T.-L.; and Korchemna, V. 2024. EF1 and EFX orientations. arXiv preprint arXiv:2409.13616. Deligkas, A.; Eiben, E.; Ioannidis, S. D.; Knop, D.; and Schierreich, Š. 2025. Balanced and fair partitioning of friends. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 13754–13762. Garey, M. R.; Johnson, D. S.; and Stockmeyer, L. 1974. Some simplified NP-complete problems. In Proceedings of the sixth annual ACM symposium on Theory of computing, 47–63. Hosseini, H.; Mammadov, A.; and W ˛as, T. 2023. Fairly allocating goods and (terrible) chores. In Proceedings of the Thirty- Second International Joint Conference on Artificial Intelligence, 2738–2746. Hosseini, H.; Narang, S.; and W ˛as, T. 2025. Fair distribution of delivery orders. Artificial Intelligence, 104389.

Hosseini, H.; and Schierreich, Š. 2025. The Algorithmic Landscape of Fair and Efficient Distribution of Delivery Orders in the Gig Economy. arXiv preprint arXiv:2503.16002. Hummel, H.; and Hetland, M. L. 2022. Fair allocation of conflicting items. Auton. Agents Multi Agent Syst., 36(1): 8. Igarashi, A.; Manurangsi, P.; and Yoneda, H. 2025. Dividing Conflicting Items Fairly. arXiv preprint arXiv:2506.14149. Kumar, Y.; Equbal, S.; Gurjar, R.; Nath, S.; and Vaish, R. 2024. Fair Scheduling of Indivisible Chores. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems, 2345–2347. Li, B.; Li, M.; and Zhang, R. 2021. Fair Scheduling for Timedependent Resources. In NeurIPS, 21744–21756. Li, L.; Micha, E.; Nikolov, A.; and Shah, N. 2023. Partitioning friends fairly. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 5747–5754. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In Proceedings of the 5th ACM Conference on Electronic Commerce, 125–131. Liu, S.; Lu, X.; Suzuki, M.; and Walsh, T. 2024. Mixed fair division: A survey. Journal of Artificial Intelligence Research, 80: 1373–1406. Mahara, R. 2025. Existence of Fair and Efficient Allocation of Indivisible Chores. arXiv preprint arXiv:2507.09544. Wang, F.; and Li, B. 2024. Fair Surveillance Assignment Problem. In WWW, 178–186. ACM. Zhou, Y.; Wei, T.; Li, M.; and Li, B. 2024. A Complete Landscape of EFX Allocations on Graphs: Goods, Chores and Mixed Manna. In 33rd International Joint Conference on Artificial Intelligence (IJCAI 2024), 3049–3056. International Joint Conferences on Artificial Intelligence.

17066
