---
title: "Probing EFX via PMMS: (Non-)Existence Results in Discrete Fair Division"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38716
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38716/42678
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Probing EFX via PMMS: (Non-)Existence Results in Discrete Fair Division

<!-- Page 1 -->

Probing EFX via PMMS: (Non-)Existence Results in Discrete Fair Division

Jarosław Byrka1, Franciszek Malinka1, Tomasz Ponitka2

1University of Wrocław 2Tel Aviv University

## Abstract

We study the fair division of indivisible items and provide new insights into the EFX problem, which is widely regarded as the central open question in fair division, and the PMMS problem, a strictly stronger variant of EFX. Our first result constructs a three-agent instance with two monotone valuations and one additive valuation in which no PMMS allocation exists. Since EFX allocations are known to exist under these assumptions, this establishes a formal separation between EFX and PMMS. We prove existence of fair allocations for three important special cases. We show that EFX allocations exist for personalized bivalued valuations, where for each agent i there exist values ai > bi such that agent i assigns value vi({g}) ∈ {ai, bi} to each good g. We establish an analogous existence result for PMMS allocations when ai is divisible by bi. We also prove that PMMS allocations exist for binary-valued MMS-feasible valuations, where each bundle S has value vi(S) ∈{0, 1}. Notably, this result holds even without assuming monotonicity of valuations and thus applies to the fair division of chores and mixed manna. Finally, we study a class of valuations called pair-demand valuations, which extend the well-studied unit-demand valuations to the case where each agent derives value from at most two items, and we show that PMMS allocations exist in this setting. Our proofs are constructive, and we provide polynomial-time algorithms for all three existence results.

Extended version — https://arxiv.org/abs/2507.14957

## Introduction

The fair division problem involves allocating a set of resources among a group of agents to meet certain fairness criteria. When there are only two agents, the standard fair division protocol is the cut-and-choose method—where one agent proposes a division of the resources into two parts, and the other selects the preferred part—a practice that dates back to the story of Abraham and Lot in the Book of Genesis. The fair division literature, beginning with Steinhaus (1948), explores the fairness guarantees that can be achieved for more than two agents.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

The initial focus of this literature has been on the cakecutting scenario, where the resources to be allocated are assumed to be infinitely divisible. A key property of cut-andchoose in cake-cutting scenarios with two agents, formalized by Foley (1967), is envy-freeness: no agent prefers another agent’s allocation to their own. A central achievement of the cake-cutting literature is that this guarantee can be extended to any number of agents, under mild assumptions (Stromquist 1980).

This work focuses on the discrete fair division problem, where the goods are indivisible. Specifically, we consider a setting with n agents and m items, where each agent i ∈N has a valuation function vi: 2M →R≥0 that assigns a nonnegative value to each subset of the items. The goal is to compute a fair partition (X1,..., Xn) such that Xi∩Xj = ∅ for all i̸ = j and X1 ∪· · · ∪Xn = M. It is easy to see that even for two agents, an envy-free allocation may not exist—for instance, when there is only one item. EFX. A key property of cut-and-choose in discrete settings with two agents, identified by Caragiannis et al. (2019), is envy-freeness up to any good (EFX): no agent prefers another’s allocation after the removal of any single item from that bundle, i.e., for all i, j ∈N, it holds that vi(Xi) ≥ vi(Xj \{g}) for all g ∈Xj. Extending the existence of EFX allocations to an arbitrary number of agents—analogous to the existence of envy-free allocations in cake cutting— remains a major open problem, even for additive valuations; notably, no counterexamples are known, even with arbitrary monotone valuations.

Nevertheless, significant progress has been made on the EFX problem for various special cases. Amanatidis et al. (2021) addressed the case of bivalued valuations, where each agent assigns one of two values to each item, i.e., there are a, b ≥0 such that vi({g}) ∈{a, b} for all i ∈N and g ∈M, and vi(S) = P g∈S vi({g}) for all S ⊆M. They provided two distinct proofs of the existence of EFX allocations for bivalued valuations: (1) an existential proof based on maximizing Nash welfare (i.e., the product of agents’ valuations), and (2) a constructive proof via the Match-and- Freeze algorithm. Both proofs crucially rely on the parameters a and b being fixed across all agents’ valuations.

Furthermore, Chaudhury, Garg, and Mehlhorn (2024); Akrami et al. (2025) established the existence of EFX allocations for three agents where two agents have arbitrary

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16735

<!-- Page 2 -->

monotone valuations and the third agent’s valuation satisfies a natural condition known as MMS-feasibility, which covers important classes of valuations, including additive; see Definition 2.6. See also the extended version for additional discussion on the EFX problem. PMMS. While EFX and its relaxations have received significant attention in the fair division literature, Caragiannis et al. (2019) also formalized another compelling fairness criterion known as the pairwise maximin share (PMMS), a natural generalization of the guarantees of cut-and-choose. Specifically, for any pair of agents i and j, it requires that agent i receives at least as much value as they would in the maximin partition of their combined items, i.e., the partition (A, B) of Xi ∪Xj that maximizes min{vi(A), vi(B)}. This corresponds to the value one could guarantee as the cutter in the cut-and-choose protocol.

While PMMS allocations may not exist for arbitrary monotone valuations (see Proposition 3.1), it remains an open question whether they exist under MMS-feasible valuations, including additive ones. Notably, under mild assumptions, any PMMS allocation is also EFX, so proving the existence of PMMS allocations would simultaneously resolve the EFX problem; see the extended version for more details. However, PMMS is significantly less understood, and little is known about its existence in special cases.

An important advantage of PMMS over EFX is that its definition naturally extends to the fair division of chores, where agents have negative valuations that decrease as the number of items increases. In contrast, the definition of EFX must be adapted for chores by requiring that vi(Xi \ {g}) ≥ vi(Xj) for all g ∈Xi. Moreover, Christoforidis and Santorinaios (2024) recently showed that EFX for chores does not exist when there are three agents with arbitrary monotonically decreasing valuations; notably, these valuations violate MMS-feasibility.

The goal of this work is to advance our understanding of the existence of both EFX and PMMS allocations in key special cases of discrete fair division.

Our Contribution In this work, we provide new insights into the existence of EFX and PMMS allocations, including one non-existence result and three existence results.

We begin by presenting our negative result for PMMS in the case of three agents.

Theorem 1 (Separation between EFX and PMMS for Three Agents). There exists an instance with three agents, one with an additive valuation and two with arbitrary monotone valuations, for which no PMMS allocation exists.

This result establishes a formal separation between the existence of EFX and PMMS allocations for the case of three agents. Akrami et al. (2025) have shown that EFX is always guaranteed under the assumptions of the theorem. In contrast, we show that PMMS may fail to exist. This indicates that proving the existence of PMMS for the case of three agents might require fundamentally different techniques.

Our first positive result concerns the existence of EFX in the important case of personalized bivalued valuations (e.g.,

Aziz et al. 2023; Bu et al. 2023; Amanatidis et al. 2025), where each agent i ∈N has values ai, bi ≥0 such that vi({g}) ∈{ai, bi} for all g ∈M. We also consider the existence of PMMS allocations under factored personalized bivalued valuations (e.g., Ebadian, Peters, and Shah 2022; Akrami et al. 2022), where each ai is an integer multiple of bi. We establish the following theorem for this setting.

Theorem 2 (Personalized Bivalued Valuations). For any instance with personalized bivalued valuations, there exists an allocation that satisfies EFX. Moreover, if the valuations are also factored, then this allocation is guaranteed to satisfy PMMS.

This generalizes the result of Amanatidis et al. (2021) in two ways. First, we consider the more general setting of personalized bivalued valuations. Second, we also establish the existence of a PMMS allocation under an additional assumption, rather than just an EFX allocation.

Our result is obtained by adapting the Match-and-Freeze algorithm to the setting of personalized bivalued valuations (see Algorithm 1). Notably, we also show that the argument based on maximizing Nash welfare does not extend to this setting (see Proposition 4.6).

We note that the existence of EFX allocations for personalized bivalued valuations has also been independently discovered by Jin and Tao (2025).

Our second positive result addresses the natural class of binary-valued valuations, where each bundle of items is either desirable or non-desirable to an agent; i.e., vi(S) ∈ {0, 1} for all i ∈N and S ⊆M. Binary-valued valuations are sometimes referred to as dichotomous preferences in the literature (e.g. Bogomolnaia and Moulin 2004; Bogomolnaia, Moulin, and Stong 2005; Kurokawa, Procaccia, and Shah 2018). We prove the following:

Theorem 3 (Binary-Valued Valuations). For any instance with binary-valued MMS-feasible valuations, there exists a PMMS allocation.

To prove our result, we introduce a novel Cut-and- Choose-Graph procedure (see Algorithm 2), inspired by the Envy-Graph procedure of Lipton et al. (2004).

A key feature of our proof is that it does not rely on the monotonicity of valuations. Therefore, it applies not only to instances involving goods, but also to those involving chores or mixed manna, i.e., a combination of goods and chores.

Finally, we study the class of pair-demand valuations, where each agent desires to receive at most two items. This class naturally generalizes unit-demand valuations and is a special case of the broader and well-studied class of kdemand (or multi-demand) valuations (e.g., Berger, Eden, and Feldman 2020; Zhang and Conitzer 2020; Deligkas, Melissourgos, and Spirakis 2021), with k = 2. We establish the following theorem for this setting.

Theorem 4 (Pair-Demand Valuations). For any instance with pair-demand valuations, there exists a PMMS allocation.

All of our positive results are not only existential but also constructive: every algorithm presented in this work runs in polynomial time (see Corollaries 4.5, 5.3 and 6.1).

16736

<!-- Page 3 -->

## 2 Preliminaries

In this work we consider instances of the fair division problem where N is a set of n agents, N = {1,..., n}, and M is a set of m indivisible items, M = {1,..., m}. Each agent i ∈N has a valuation function vi: 2M →R.

Unless stated otherwise, we assume that each agent i’s valuation is normalized, so that vi(∅) = 0, and monotone, so that vi(S) ≤vi(T) for any S ⊆T ⊆M. Notably, we do not make these assumptions in Section 5.

An allocation X = ⟨X1,..., Xn⟩is a partition of the items among the agents, where each item is assigned to exactly one agent. Formally, we require that X1 ∪· · · ∪Xn = M and Xi ∩Xj = ∅for all i̸ = j.

Fairness Notions We now formally define the EFX condition. Definition 2.1 (EFX Allocations). We say that an allocation X is envy-free up to any good (EFX) if, for every pair of agents i and j, and for every item g ∈Xj, we have vi(Xi) ≥ vi(Xj \ {g}). Otherwise, if there exists some item g ∈Xj such that vi(Xi) < vi(Xj \ {g}), we say that agent i EFXenvies agent j.

To introduce the notion of PMMS, we first define the fair share function µi. Definition 2.2 (Fair Share). Let k ∈{2,..., n}. The fair share of agent i for a bundle S ⊆M divided among k agents is defined as µi(S, k) = max X1,...,Xk partition of S min{vi(X1),..., vi(Xk)}.

We refer to any partition X1,..., Xk that achieves the maximum above as a maximin partition. If only a single agent is being considered and it is clear from context, we omit the subscript and write µ instead of µi. Similarly, when k = 2, we omit the parameter and write µi(S) to denote µi(S, 2).

Using the notion of fair shares, we define PMMS, first introduced by Caragiannis et al. (2019). Definition 2.3 (PMMS Allocations). An allocation X is pairwise maximin share fair (PMMS) if, for every pair of agents i and j, it holds that vi(Xi) ≥µi(Xi ∪Xj). Otherwise, if vi(Xi) < µi(Xi ∪Xj), we say that agent i PMMSenvies agent j.

We also study the related concept of MMS, and compare it to PMMS in Section 3. Definition 2.4 (MMS Allocations). An allocation X is maximin share fair (MMS) if, for every agent i, it holds that vi(Xi) ≥µi(M, n).

Valuation Classes An important class of valuations is the class of additive valuations, where for every S ⊆M and any g ∈M \ S, we have v(S ∪{g}) = v(S) + v({g}).

We now formally define personalized bivalued valuations. Definition 2.5 (Personalized Bivalued Valuations). Agent i’s valuation is said to be personalized bivalued if vi is additive and there exist values ai > bi ≥0 such that vi({g}) ∈{ai, bi} for every item g ∈M. Furthermore, a personalized bivalued valuation is called factored if either ai is divisible by bi, or bi = 0.

Whenever we write ai/bi and bi = 0, we interpret this fraction as a sufficiently large number K.

We also define the class of MMS-feasible valuations, following the definition of Akrami et al. (2025).

Definition 2.6 (MMS-Feasible Valuations). Agent i’s valuation is MMS-feasible if, for every subset S ⊆M and for any two partitions (X1, X2) and (Y1, Y2) of S such that X1 ∪X2 = Y1 ∪Y2 = S and X1 ∩X2 = Y1 ∩Y2 = ∅, it holds that max{vi(X1), vi(X2)} ≥min{vi(Y1), vi(Y2)}.

We define binary-valued valuations as follows.

Definition 2.7 (Binary-Valued Valuations). Agent i’s valuation is binary if for every subset S ⊆M, it holds that vi(S) ∈{0, 1}.

Finally, we define the class of pair-demand valuations.

Definition 2.8 (Pair-Demand Valuations). Agent i’s valuation is called pair-demand if there exist non-negative values vi,1,..., vi,m ≥0 such that, for every subset S ⊆M, it holds that:

vi(S) = max T ⊆S,|T |≤2

X j∈T vi,j.

Implications of PMMS We note that, although PMMS does not imply EFX in general, it does imply a slightly weaker variant of EFX. Moreover, PMMS implies the full EFX condition if all valuations are non-degenerate; i.e., if vi(S)̸ = vi(T) for all S̸ = T and i. These implications are discussed in more detail in the extended version.

Non-Existence of PMMS In this section, we examine the conditions necessary for the existence of PMMS allocations. We begin by discussing the two-agent case and then proceed to the case of three agents.

In the case of two agents, the PMMS condition is equivalent to MMS (Definition 2.4). It has been noted by Akrami et al. (2025) that MMS allocations for two agent exist when one agent has an MMS-feasible valuation and the other has an arbitrary valuation. This condition is necessary, as an MMS allocation may not exist for two agents if both valuations are arbitrary.

While one might expect that a non-existence result for two agents would automatically extend to settings with three or more agents, this extension is not immediate. For example, simply adding a dummy agent who values every subset at 0 to the two-agent counterexample is not sufficient. Intuitively, adding such a dummy agent is equivalent to allowing some items to go to charity, as considered by Caragiannis, Gravin, and Huang (2019). We present a non-trivial extension of the non-existence result beyond the two-agent case. To the best of our knowledge, this is the first known construction demonstrating the non-existence of a PMMS allocation for more than two agents.

16737

<!-- Page 4 -->

Proposition 3.1 (Non-Existence of PMMS). For any n ≥2, there exists an instance with n agents, each with monotone valuations, and n + O(log n) items, in which no PMMS allocation exists. Moreover, an MMS allocation exists in this instance.

Our construction consists of an instance with n −2 star items and O(log n) common items. By carefully designing the valuation functions, we ensure that any PMMS allocation must assign exactly one star item to n−2 agents and partition the common items among the remaining two agents. Furthermore, by appropriately setting the valuations over the common items, we ensure that no pair of agents can partition these items among themselves and satisfy the PMMS condition. The full proof appears in the extended version.

The construction in the proof of Proposition 3.1 uses n+O(log n) items. An interesting open problem is to determine the minimal number of items required for such a construction; specifically, whether the result can be improved to include only n + O(1) items.

As shown by Akrami et al. (2025), an EFX allocation always exists for three agents if at least one of them has an MMS-feasible valuation and the other two have monotone valuations. We show that these assumptions are not sufficient to guarantee the existence of a PMMS allocation. Specifically, we present an example with two agents having monotone valuations and one agent with an additive (hence MMS-feasible) valuation, where no PMMS allocation exists. This establishes a separation between the two fairness notions and suggests that the proof technique used to establish the existence of EFX allocations for three agents does not extend to PMMS. The proof of the following theorem is deferred to the extended version.

Theorem 1 (Separation between EFX and PMMS for Three Agents). There exists an instance with three agents, one with an additive valuation and two with arbitrary monotone valuations, for which no PMMS allocation exists.

The instance used in the proof of Theorem 1 was discovered through a computational search over the space of possible valuations. Considerable effort was devoted to simplifying the counterexample, as the initial instances had complex and unintuitive structure. The counterexample presented here is notably simpler, using few distinct values and elegantly handling uneven bundle sizes.

Personalized Bivalued Valuations In this section, we analyze the case of personalized bivalued valuations, where the valuations are additive and, for each agent i, there exist some ai > bi ≥0 such that vi({g}) ∈ {ai, bi} for all items g. Our main theorem for this setting is as follows.

Theorem 2 (Personalized Bivalued Valuations). For any instance with personalized bivalued valuations, there exists an allocation that satisfies EFX. Moreover, if the valuations are also factored, then this allocation is guaranteed to satisfy PMMS.

The rest of this section is devoted to proving Theorem 2. We show that Algorithm 1 produces an EFX allocation for

## Algorithm

1: Personalized Match-and-Freeze Alg.

Input: A personalized bivalued instance ⟨N, M, V⟩ Output: An EFX allocation X = ⟨X1,..., Xn⟩

1 Set P ←M

2 Set wi ←0 for i ∈{1,..., n}

## 3 Set

Lr ←N for r ∈{1,..., m}

## 4 Set

Xi ←∅for i ∈{1,..., n}

5 while P̸ = ∅do

## 6 Set r to be the current round (iteration) number

## 7 Construct a weighted bipartite graph G between

Lr and P

8 for each i ∈Lr and g ∈P with vi({g}) = ai do

## 9 Add an edge from i to g with weight ai/bi

## 10 Find a maximal (in terms of size) matching in G

that maximizes the total weight

11 for each matched pair (i, g) do

## 12 Add g to Xi 13 Remove g from P

14 for each connected component C of G do

## 15 Let U be the set of unmatched agents in C

16 if U̸ = ∅then

17 Let t be the maximum of ai/bi for i ∈U

## 18 Remove all matched agents of C from

Lr+j for j ∈{1,..., ⌊t −1⌋}

19 wi ←r for each matched i in C

20 for each unmatched agent i in increasing wi do

## 21 Add any remaining good g to Xi 22 Remove g from P

23 return X = ⟨X1,..., Xn⟩ any personalized bivalued instance, and a PMMS allocation if the instance is factored. Algorithm 1 is a modified version of the Match-and-Freeze algorithm proposed by Amanatidis et al. (2021), which was designed to compute EFX allocations for non-personalized bivalued valuations. See Table 1 for an example of the execution of Algorithm 1.

We begin by stating the following property of the allocation produced by the algorithm; see the extended version for a proof.

Lemma 4.1. Consider an execution of Algorithm 1, and fix a round r. Let C be any connected component of the graph G constructed during round r. If the set U of unmatched agents in C is nonempty and U̸ = C, then it holds that:

max{ai/bi: i ∈U} ≤min{ai/bi: i ∈C \ U}.

Next, we use Lemma 4.1 to derive the following technical lemma, which plays a key role in our analysis. The lemma and its proof are similar to the analysis of the Match-and- Freeze algorithm for non-personalized bivalued valuations, as presented by Amanatidis et al. (2021, Lemma 4.2). The proof is deferred to the extended version.

Lemma 4.2. Consider an execution of Algorithm 1, and fix an agent i. Let ri denote the last round in which an item g with vi({g}) = ai was allocated to some agent. Let Xi,r

16738

<!-- Page 5 -->

Agents Round 1 Round 2 Round 3 Round 4 Round 5 Round 6

Agent 1 (a1 = 2.5) 1 1 1 1 1 1

Agent 2 (a2 = 3) 3 — 1 1 1

Agent 3 (a3 = 4) 1 1 1 1 1 1

Agent 4 (a4 = 5) — — — 1

**Table 1.** An example execution of Algorithm 1 is presented for an instance with 4 agents and 18 items. The agents have bivalued valuations with a1 = 2.5, a2 = 3, a3 = 4, a4 = 5, and bi = 1 for i ∈{1, 2, 3, 4}. The items are x, y, z1,..., z16. Agents 1 and 2 assign the higher value to item x and no other item, while agents 3 and 4 assign the higher value to item y and no other item. Each cell represents the value of the item that a given agent received in a particular round. Cells with a circled value indicate rounds in which an agent received a high-value item. Cells corresponding to rounds in which an agent is frozen contain a dash, and cells for rounds after the last item has been allocated are left empty.

denote the singleton set allocated to agent i in round r, or the empty set if agent i does not receive any item in that round. Let Fi denote the set of rounds during which agent i is not active. Then:

(i) We have vi(Xi,r) = ai for all r ∈{1, 2,..., ri −1}. (ii) If Fi̸ = ∅, then vi(Xi,ri) = ai and Fi ⊆{ri +

1,..., ri + ⌊ai/bi −1⌋}. (iii) If vi(Xi,ri) = ai and vi(Xj,ri) = ai for some agent j, then Fi = Fj. The proof of Theorem 2 also relies on the following claim, proved in the extended version. Lemma 4.3. Let X be an allocation, and let i and j be any agents. Suppose that vi(Xi) ≥vi(Xj) −bi. Then agent i does not EFX-envy agent j. Moreover, if agent i’s valuation is factored, then agent i also does not PMMS-envy agent j.

We now present a simplified version of the proof of the main theorem, under the additional assumption that the considered agent has received a low-value item. For the full proof, see the extended version.

Simplified Proof of Theorem 2. Consider an execution of Algorithm 1, and fix two agents i and j. Let R denote the index of the last round, and let ri ≤R denote the last round in which an item g with vi({g}) = ai was allocated to any agent. Let Xi,r denote the singleton set allocated to agent i in round r, or the empty set if agent i does not receive any item in that round. Similarly, let Xj,r denote the set allocated to agent j in round r. Let Fi ⊆{1,..., R} denote the set of rounds during which agent i is inactive.

Our goal is to prove that i does not EFX-envy j, and if the valuation is factored, then i also does not PMMSenvy j. In the simplified version of the proof, we assume that vi(Xi,ri) = bi. By Lemma 4.3, it suffices to show that vi(Xi) ≥vi(Xj) −bi. We use this observation to complete the proof in most of the cases considered in our analysis.

By Lemma 4.2, we know that vi(Xi,r) = ai for all r ∈{1,..., ri −1}, and vi(Xi,r) ≥bi for all r ∈ {ri + 1,..., R −1}. Moreover, vi(Xj,r) ≤ai for all r ∈ {1,..., ri−1} and vi(Xj,r) ≤bi for all r ∈{ri+1,..., R}.

First, suppose that vi(Xj,ri) = bi. In this case, by Lemma 4.2, we have Fi = ∅, and:

vi(Xi) ≥(ri −1) · ai + (R −ri) · bi ≥vi(Xj) −bi.

Next, suppose that vi(Xj,ri) = ai. In this case, by Lemma 4.2, we know that agent i was not matched during round ri, and thus Fi = ∅. Moreover, agent j must have been matched to item Xj,ri during round ri. Indeed, it cannot be that agent j received item Xj,ri through the operation in Line 21, because if that were the case, then agent i would have been matched to item Xj,ri during round ri. Therefore, during round ri, agents i and j belong to the same connected component, as they both have an edge to item Xj,ri. Furthermore, by the choice of freezing time in Line 17, we have vi(Xj,r) = 0 for all r ∈{ri + 1,..., ri + ⌊ai/bi −1⌋}, since agent i remains unmatched during round ri.

First, suppose that R > ri + ⌊ai/bi −1⌋. Since agent j becomes frozen, her priority is updated in Line 18, so that agent i always chooses an item before agent j. Hence, vi(Xi,R) ≥vi(Xj,R). It follows that:

vi(Xi) = (ri −1) · ai + (R −ri) · bi + vi(Xi,R)

= ri · ai + (R −ai/bi −ri) · bi + vi(Xi,R) ≥ri · ai + (R −1 −⌊ai/bi⌋−ri) · bi + vi(Xj,R) ≥vi(Xj) −bi.

Now, suppose that R ≤ri + ⌊ai/bi −1⌋. In this case, Xj consists of exactly ri items, and Xi consists of at least ri −1 high-value items and possibly some low-value items. The EFX condition holds since vi(Xi) ≥(ri −1) · ai ≥ vi(Xj \ {g}) for any g ∈Xj. For the PMMS condition, observe that the total value of low-value items in Xi is at most (⌊ai/bi −1⌋+ 1) · bi ≤ai, and therefore:

µi(Xi ∪Xj) ≤(ri −1) · ai + (|Xi| −ri + 1) · bi = vi(Xi).

This completes the simplified proof of the theorem.

In the following remark, we explain the importance of the order in which unmatched agents receive items in Line 20 of Algorithm 1.

Remark 4.4. Consider the example described in Table 1. In the final round, only two items remain, and all agents are active. Therefore, two agents must be left without an item in this round. According to the priority ordering w, the items are given to agents 1 and 3, as they were not matched at any point during the execution of the algorithm.

16739

<!-- Page 6 -->

If, instead, an item were allocated to agent 2 rather than agent 1, then agent 1 would EFX-envy agent 2. In that case, agent 1 would receive five low-value items, yielding a value of 5, while agent 2 would receive one high-value item and four low-value items. Agent 1’s valuation for agent 2’s bundle, even after removing one low-value item, would be 5.5, violating EFX.

We also observe that Algorithm 1 allocates at least one item in each round, ensuring that it runs in polynomial time (in n and m), as a maximum-weight maximal matching can be computed in polynomial time (Kuhn 1955). This leads to the following corollary.

Corollary 4.5. For any instance with personalized bivalued valuations, an EFX allocation can be computed in polynomial time. Furthermore, for any instance with factored personalized bivalued valuations, a PMMS allocation can also be computed in polynomial time.

Finally, we note that Amanatidis et al. (2021) also showed that for non-personalized bivalued valuations, an EFX allocation can be achieved by maximizing the Nash welfare (i.e., the geometric mean of agents’ utilities, (Q i∈N vi(Xi))1/n). In sharp contrast, in the extended version, we show that this result does not extend to personalized bivalued valuations, as demonstrated by the following proposition.

Proposition 4.6. There exists an instance with personalized bivalued valuations where none of the allocations maximizing Nash welfare satisfies EFX.

## 5 Binary-Valued Valuations

In this section, we consider the class of binary-valued valuations, where all possible bundles are classified as either desirable or non-desirable; see Definition 2.7 for a formal definition. Importantly, we do not assume that these valuations are monotone or normalized, we only assume that they satisfy the MMS-feasibility condition (Definition 2.6). We now proceed to state our main theorem.

Theorem 3 (Binary-Valued Valuations). For any instance with binary-valued MMS-feasible valuations, there exists a PMMS allocation.

The proof of Theorem 3 is based on the notion of the cutand-choose graph, which is formally defined in the following definition. This notion is inspired by the envy graph introduced by Lipton et al. (2004).

Definition 5.1 (Cut-and-Choose Graph). For a fixed allocation (X1,..., Xn) and a fixed agent s ∈N, we define the cut-and-choose graph as follows. The set of vertices is the set of agents N. For every agent i ∈N, we add an edge to precisely one agent π(i) ∈N. If vi(Xs) ≥µi(Xs ∪Xj) for all j ∈N, then we set π(i) = s. Otherwise, we set π(i) = j for some j ∈N such that vi(Xs) < µi(Xs ∪Xj).

We use the following key properties of the cut-and-choose graph.

Lemma 5.2. Fix an allocation (X1,..., Xn) and an agent s ∈N, and consider the cut-and-choose graph. Then, for every agent i ∈N, the following holds:

## Algorithm

2: Cut-and-Choose-Graph Procedure

Input: A binary-valued MMS-feasible ⟨N, M, V⟩ Output: A PMMS allocation X = ⟨X1,..., Xn⟩

1 Let X = {X1,..., Xn} be an arbitrary allocation

2 while X is not PMMS do

3 Choose s ∈[n] s.t. ∃j∈N vs(Xs) < µs(Xs ∪Xj)

4 Let π be the cut-and-choose graph for X and s

5 Set i0 ←s

Set k ←0

7 while π(ik) /∈{i0,..., ik} do

8 Set ik+1 ←π(ik)

9 Set k ←k + 1

10 if π(ik) = i0 then

## 11 Set

Xi ←Xπ(i) for all i ∈{i0,..., ik}

12 else

13 Let w be such that π(ik) = iw 14 Let (A, B) be a maximin partition of

Xi0 ∪Xiw by vik 15 if viw−1(A) < viw−1(B) then

## 16 Swap A and B

## 17 Set

Xi ←Xπ(i) for all i ∈{i0,..., iw−2} ∪{iw,..., ik−1}

## 18 Set

Xiw−1 ←A

## 19 Set

Xik ←B

20 return X = ⟨X1,..., Xn⟩

(i) If π(i) = s, then either vi(Xs) = 1, or µi(Xs ∪Xj) = 0 for all j ∈N. (ii) If π(i) = j for some j̸ = s, then vi(Xj) = 1 and µi(Xs∪

Xj) = 1.

We use Lemma 5.2 to prove Theorem 3. The proof relies on Algorithm 2, and Figure 1 illustrates the operations performed by the algorithm.

We present a simplified version of the proof of Theorem 3, under the assumption that the if-condition in Line 10 is not satisfied. For the full proof, see the extended version.

Simplified Proof of Theorem 3. By the while-loop condition in Line 2, it is clear that the output of Algorithm 2 satisfies the PMMS condition. Hence, to prove Theorem 3, it suffices to show that Algorithm 2 terminates for any input.

Consider the tuple ⟨W, E⟩, where W = P i∈N vi(Xi) and E is the number of agents for whom the PMMS condition holds. We will show that in each iteration, either W strictly increases, or W remains the same and E strictly increases. Since W ∈{0, 1,..., n} and E ∈{0, 1,..., n}, the algorithm must terminate after at most n2 iterations.

To prove this claim, fix an iteration of the while-loop. Let X be the allocation at the beginning of the iteration and let Y be the allocation at the end.

In the simplified version of the proof, we suppose the ifcondition in Line 10 is not satisfied. By Lemma 5.2(ii), we have vi(Yi) = vi(Xπ(i)) = 1 for all i ∈{i0,..., ik} \ {iw−1, ik}. Also, from the same lemma, we know that µiw−1(Xiw ∪Xi0) = 1 and µik(Xiw ∪Xi0) = 1.

16740

<!-- Page 7 -->

s i1 i2 ik... i3

(i) Case 1: Cycle.

s... iw−1 iw...

ik ik−1

(ii) Case 2: Lollipop.

**Figure 1.** An illustration of the operations performed by the Cut-and-Choose-Graph Procedure (Algorithm 2). The nodes represent agents, and the arrows depict the cut-and-choose graph. Subfigure (i) illustrates Case (1), where the if-condition in Line 10 holds, and the new allocation is obtained by assigning each agent i in the cycle the bundle of the agent to whom i points. Subfigure (ii) illustrates Case (2), where the if-condition in Line 10 does not hold. In this case, the new allocation is obtained by giving all agents in the cycle—except for agents iw−1 and ik—the bundles they are pointing to, and having agents iw−1 and ik divide the two bundles Xs and Xiw between themselves using the cut-and-choose method.

Since (A, B) is set to be a maximin partition of Xiw ∪Xi0 by vik in Line 14, we have vik(B) = 1 since µik(Xiw ∪ Xi0) = 1. Finally, by the swap operation in Line 16 and the MMS-feasibility of viw−1, we have viw−1(Yiw−1) = viw−1(A) = max{viw−1(A), viw−1(B)}

≥µiw−1(A ∪B) = 1.

Therefore, W strictly increases in this case. This proves the claim, and consequently, completes the simplified proof of the theorem.

As noted in the proof of Theorem 3, the tuple ⟨W, E⟩ increases lexicographically with every iteration of Algorithm 2. Since there are only n2 possible values for this tuple, Algorithm 2 runs in polynomial time (in n and m). This leads to the following corollary. Corollary 5.3. For instances with binary-valued valuations, PMMS allocations can be computed in polynomial time.

## 6 Pair-Demand Valuations

In this section, we analyze the natural class of pair-demand valuations, where each agent desires at most two items; see Definition 2.8. This class generalizes unit-demand valuations, in which every agent wants only one item. While EFX and PMMS are straightforward to guarantee under unit-demand valuations, they become non-trivial in the pairdemand setting. Our main result is the following theorem. Theorem 4 (Pair-Demand Valuations). For any instance with pair-demand valuations, there exists a PMMS allocation.

We remark that we do not establish the existence of EFX allocations for pair-demand valuations, which we leave as an open problem. In particular, PMMS does not imply EFX, as valuations may be degenerate. Achieving EFX may require allocating only a single item to one agent and more than two items to another. For example, consider an instance with two identical agents, one high-value item, and three lowvalue items. Here, one agent must receive the high-value item, while the other receives all three low-value items, even though the third low-value item no longer increases the second agent’s value and could instead benefit the first agent.

## Algorithm

3: Reversed Round-Robin Algorithm

Input: A pair-demand ⟨N, M, V⟩with |M| ≥2|N| Output: A PMMS allocation X = ⟨X1,..., Xn⟩

## 1 Set

Xi ←∅for i ∈{1,..., n}

2 Set P ←M

3 for i ∈N in increasing order of indices do

4 Let gi ∈arg maxg∈P vi({g})

## 5 Add gi to Xi 6 Remove gi from P

7 for i ∈N in decreasing order of indices do

8 Let hi ∈arg maxh∈P vi({h})

## 9 Add hi to Xi 10 Remove hi from P

## 11 Allocate all items left in P to any player

12 return X = ⟨X1,..., Xn⟩

As we show below, it is possible to obtain a PMMS allocation while giving each agent exactly two items, provided there are at least 2n items in total.

Our proof is based on a two-stage round-robin algorithm (Algorithm 3) in which agents select items according to a fixed order in the first stage, and then in the reversed order in the second stage. The idea of reversing the order in round-robin algorithms has been explored in the literature; for instance, in ABBA picking sequences (Brams and Taylor 2000), the Double Round-Robin algorithm (Aziz et al. 2022), and as part of the Draft-and-Eliminate algorithm (Amanatidis, Markakis, and Ntokos 2020). We defer the proof to the extended version.

Since Algorithm 3 runs in polynomial time (in n and m), we obtain the following corollary. Corollary 6.1. For instances with pair-demand valuations, PMMS allocations can be computed in polynomial time.

## Conclusion

Our work has provided several new insights into the existence of EFX and PMMS allocations. In the extended version, we additionally highlight several open problems that arise from our findings.

16741

<!-- Page 8 -->

## Acknowledgments

This project has been partially funded by NCN grant number 2020/39/B/ST6/01641, by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation program (grant agreement No. 866132), by an Amazon Research Award, by the Israel Science Foundation Breakthrough Program (grant No. 2600/24), and by a grant from TAU Center for AI and Data Science (TAD), and by the NSF-BSF (grant number 2020788).

## References

Akrami, H.; Alon, N.; Chaudhury, B. R.; Garg, J.; Mehlhorn, K.; and Mehta, R. 2025. EFX: A Simpler Approach and an (Almost) Optimal Guarantee via Rainbow Cycle Number. Oper. Res., 73(2): 738–751. Akrami, H.; Chaudhury, B. R.; Hoefer, M.; Mehlhorn, K.; Schmalhofer, M.; Shahkarami, G.; Varricchio, G.; Vermande, Q.; and van Wijland, E. 2022. Maximizing Nash Social Welfare in 2-Value Instances. In AAAI, 4760–4767. AAAI Press. Amanatidis, G.; Birmpas, G.; Filos-Ratsikas, A.; Hollender, A.; and Voudouris, A. A. 2021. Maximum Nash welfare and other stories about EFX. Theor. Comput. Sci., 863: 69–85. Amanatidis, G.; Lolos, A.; Markakis, E.; and Turmel, V. 2025. Online Fair Division for Personalized 2-Value Instances. CoRR, abs/2505.22174. Amanatidis, G.; Markakis, E.; and Ntokos, A. 2020. Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle elimination. Theor. Comput. Sci., 841: 94– 109. Aziz, H.; Caragiannis, I.; Igarashi, A.; and Walsh, T. 2022. Fair allocation of indivisible goods and chores. Auton. Agents Multi Agent Syst., 36(1): 3. Aziz, H.; Lindsay, J.; Ritossa, A.; and Suzuki, M. 2023. Fair Allocation of Two Types of Chores. In AAMAS, 143–151. ACM. Berger, B.; Eden, A.; and Feldman, M. 2020. On the Power and Limits of Dynamic Pricing in Combinatorial Markets. In WINE, volume 12495 of Lecture Notes in Computer Science, 206–219. Springer. Bogomolnaia, A.; and Moulin, H. 2004. Random Matching Under Dichotomous Preferences. Econometrica, 72(1): 257–279. Bogomolnaia, A.; Moulin, H.; and Stong, R. 2005. Collective choice under dichotomous preferences. J. Econ. Theory, 122(2): 165–184. Brams, S.; and Taylor, A. D. 2000. The Win-Win Solution: Guaranteeing Fair Shares to Everybody. W. W. Norton & Company. Bu, X.; Li, Z.; Liu, S.; Song, J.; and Tao, B. 2023. Fair Division with Allocator’s Preference. In WINE, volume 14413 of Lecture Notes in Computer Science, 77–94. Springer. Caragiannis, I.; Gravin, N.; and Huang, X. 2019. Envy- Freeness Up to Any Item with High Nash Welfare: The Virtue of Donating Items. In EC, 527–545. ACM.

Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The Unreasonable Fairness of Maximum Nash Welfare. ACM Trans. Economics and Comput., 7(3): 12:1–12:32. Chaudhury, B. R.; Garg, J.; and Mehlhorn, K. 2024. EFX Exists for Three Agents. J. ACM, 71(1): 4:1–4:27. Christoforidis, V.; and Santorinaios, C. 2024. On the Pursuit of EFX for Chores: Non-existence and Approximations. In IJCAI, 2713–2721. ijcai.org. Deligkas, A.; Melissourgos, T.; and Spirakis, P. G. 2021. Walrasian Equilibria in Markets with Small Demands. In AAMAS, 413–419. ACM. Ebadian, S.; Peters, D.; and Shah, N. 2022. How to Fairly Allocate Easy and Difficult Chores. In AAMAS, 372–380. International Foundation for Autonomous Agents and Multiagent Systems (IFAAMAS). Foley, D. 1967. Resource Allocation and the Public Sector. Yale Economic Essays, 7(1): 45–98. Jin, J.; and Tao, B. 2025. On Pareto-Optimal and Fair Allocations with Personalized Bi-Valued Utilities. CoRR, abs/2507.18251. Kuhn, H. W. 1955. The Hungarian method for the assignment problem. Naval Research Logistics Quarterly, 2(1-2): 83–97. Kurokawa, D.; Procaccia, A. D.; and Shah, N. 2018. Leximin Allocations in the Real World. ACM Trans. Economics and Comput., 6(3-4): 11:1–11:24. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In EC, 125–131. ACM. Steinhaus, H. 1948. The problem of fair division. Econometrica, 16(1): 101–104. Stromquist, W. 1980. How to Cut a Cake Fairly. The American Mathematical Monthly, 87(8): 640–644. Zhang, H.; and Conitzer, V. 2020. Learning the Valuations of a k-demand Agent. In ICML, volume 119 of Proceedings of Machine Learning Research, 11066–11075. PMLR.

16742
