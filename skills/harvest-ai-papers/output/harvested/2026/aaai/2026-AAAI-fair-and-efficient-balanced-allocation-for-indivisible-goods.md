---
title: "Fair and Efficient Balanced Allocation for Indivisible Goods"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38755
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38755/42717
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Fair and Efficient Balanced Allocation for Indivisible Goods

<!-- Page 1 -->

Fair and Efﬁcient Balanced Allocation for Indivisible Goods

Yasushi Kawase1,2, Ryoga Mahara1

1The University of Tokyo, Tokyo, Japan 2RIKEN Center for Advanced Intelligence Project, Tokyo, Japan kawase@mist.i.u-tokyo.ac.jp, mahara@mist.i.u-tokyo.ac.jp

## Abstract

We study the problem of allocating indivisible goods among agents with additive valuation functions to achieve both fairness and efﬁciency under the constraint that each agent receives exactly the same number of goods (the balanced constraint). While this constraint is common in real-world scenarios such as team drafts or asset division, it signiﬁcantly complicates the search for allocations that are both fair and efﬁcient. Envy-freeness up to one good (EF1) is a well-established fairness notion for indivisible goods. Pareto optimality (PO) and its stronger variant, fractional Pareto optimality (fPO), are widely accepted efﬁciency criteria. Our main contribution establishes both the existence and polynomial-time computability of allocations that are simultaneously EF1 and fPO under balanced constraints in two fundamental cases: (1) when agents have at most two distinct types of valuation functions, and (2) when each agent has a personalized bivalued valuation. Our algorithms leverage novel applications of maximum-weight matching in bipartite graphs and duality theory, providing the ﬁrst polynomial-time solutions for these cases and offering new insights for constrained fair division problems.

## Introduction

The fair division of indivisible goods is an important problem that has been widely studied in mathematics, economics, and computer science (Brams and Taylor 1996; Brandt et al. 2016). In recent years, this topic has attracted even more interest (see surveys (Amanatidis et al. 2023; Aziz et al. 2022b; Guo, Li, and Deng 2023)). Many previous studies have discussed fairness and efﬁciency under the assumption that there are no constraints on allocation. However, in real-world problems, it is often necessary to make allocations under various constraints. Motivated by this, recent works have studied fair division problems under a variety of constraints (see the survey (Suksompong 2021)).

For instance, in team sports drafts, new players are assigned to teams, and it is typical for each team to receive the same number of new players to prevent any team from having a numerical advantage. Another example is the division of indivisible assets, such as inherited jewelry or artwork, among family members. Siblings often agree to take

Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

the same number of items, but differences in market value or personal signiﬁcance may still lead to envy. These examples highlight the importance of considering allocations that maintain balanced quantities while also satisfying fairness and efﬁciency.

In this paper, we study the problem of ﬁnding fair and efﬁcient allocations under the constraint that each agent receives the same number of goods (the balanced constraint), assuming that the total number of goods is a multiple of the number of agents. We also assume that each agent has an additive valuation function.

To formalize notions of fairness in such settings, several criteria have been introduced in the literature. Envyfreeness (EF) (Foley 1966) is one of the most fundamental fairness concepts. It requires that no agent prefers someone else’s bundle over their own. However, with indivisible items, achieving EF can be impossible even in very simple scenarios, such as when there are only two agents and a single item. To address this issue, various relaxed notions of fairness have been proposed. The most prominent among these is envy-freeness up to one item (EF1) introduced by Budish (2011). EF1 requires that each agent prefers their own bundle to that of any other agent after removing at most one item from the other agent’s bundle. It is known that an EF1 allocation always exists and can be computed in polynomial time (Lipton et al. 2004). Moreover, even under the balanced constraint, an EF1 allocation can be found using the round-robin algorithm (Caragiannis et al. 2019).

On the efﬁciency side, Pareto optimality (PO) is a standard benchmark. An allocation is PO if no agent can be made strictly better off without making someone else worse off. A stronger concept, known as fractional Pareto optimality (fPO), extends this notion to fractional allocations. It is known that maximizing utilitarian welfare yields an fPO allocation, and thus also a PO allocation. Consequently, such an allocation always exists and can be computed in polynomial time.

While ﬁnding allocations that are either EF1 or PO individually is relatively straightforward, the problem becomes considerably more complex when both fairness and efﬁciency must be achieved at the same time. In what follows, we examine the main challenges in satisfying both criteria simultaneously and review previous progress on addressing this issue.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17067

<!-- Page 2 -->

For the unconstrained case, Caragiannis et al. (2019) established the novel result that maximizing the Nash social welfare (Nash 1950; Kaneko and Nakamura 1979), deﬁned as the geometric mean of the agents’ valuations, yields an allocation that is both EF1 and PO (but may not be fPO). However, since maximizing Nash social welfare is NPhard (Nguyen et al. 2014) and even APX-hard (Lee 2017), this approach does not directly yield an efﬁcient algorithm. Barman, Krishnamurthy, and Vaish (2018) addressed this computational limitation by proposing a pseudo-polynomial time algorithm that computes an EF1 and PO allocation and proved the existence of an EF1 and fPO allocation. Subsequently, Mahara (2024b) developed a polynomial-time algorithm to compute an EF1 and fPO allocation when the number of agents is constant. The existence of a polynomial-time algorithm for ﬁnding an EF1 and PO (or fPO) allocation in general case remains an important open question.

There is growing interest in fair and efﬁcient allocation under various practical constraints that extend beyond the unconstrained setting. When such constraints are present, achieving both EF1 and PO1 becomes more challenging than in the unconstrained case. A natural ﬁrst approach is to maximize Nash social welfare among allocations that satisfy the constraints, but in general, such an approach does not lead to an EF1 allocation. Furthermore, under general constraints, there may not exist any allocation that is both EF1 and PO (Wu, Li, and Gan 2021; Cookson, Ebadian, and Shah 2025). To date, the only known result guaranteeing the existence of an allocation that is both EF1 and PO under constraints is due to Shoshan, Hazon, and Segal-Halevi (2023), who studied fair division under category constraints and developed a polynomial-time algorithm to ﬁnd such an allocation for the case of two agents.

Our Results In this paper, we study the problem of fair division of indivisible goods among agents with additive valuation functions under the balanced constraints.

We ﬁrst observe that maximizing Nash social welfare over balanced allocations does not necessarily guarantee EF1 (see Example 1). We then give a characterization that an allocation is fPO if and only if it maximizes a weighted utilitarian social welfare (Proposition 1). We also show that checking whether a given balanced allocation satisﬁes fPO and EF1 is polynomial-time solvable, whereas checking PO is coNP-complete. Additionally, we provide a reduction from the problem of ﬁnding an EF1 and fPO allocation under unconstrained case to balanced constraint case.

We establish both the existence and polynomial-time computability of balanced allocations that are simultaneously EF1 and fPO in two important cases: when there are

1In the constrained case, we consider PO and fPO only with respect to feasible allocations (i.e., constrained PO and constrained fPO). It is not difﬁcult to see that PO (or fPO) with respect to all allocations may not exist. For example, suppose there are two agents and two goods, and one agent values both goods positively while the other agent assigns zero value to both. Then, the PO allocation with respect to all allocations must assign both goods to the agent who values them, but such an allocation is not balanced.

at most two types of agents, and when each agent has a personalized bivalued valuation, i.e., each agent i assigns two distinct values ai, bi (ai > bi ≥0) to the goods.

In the personalized bivalued case, we show that maximizing the weighted utilitarian social welfare with appropriately chosen weights yields an EF1 and fPO allocation.

In the two types case, we provide an algorithm that maintains primal and dual optimal solutions for the linear program that maximizes weighted social welfare. The algorithm searches for an EF1 allocation by gradually changing the weights. In this procedure, we exploit a characterization of dual optimal solutions for maximum-weight perfect matchings in bipartite graphs using the shortest path distances. It is worth mentioning that our result for the two types case implies the result for the unconstrained case.

It is worth noting that the balanced constraints are a special case of the category constraints studied in (Shoshan, Hazon, and Segal-Halevi 2023; Igarashi and Meunier 2025) and the matroid constraints considered in (Kawase and Sumita 2020; Kawase, Sumita, and Yokoi 2023; Cookson, Ebadian, and Shah 2025). Moreover, both cases analyzed in this paper have been widely studied in the recent fair division literature (see Related Work).

Due to space limitations, we omit most of the proofs, which can be found in the full paper.

## Related Work

Fair and efﬁcient allocation for divisible items The Fisher market framework, originally introduced by Irving Fisher (see (Brainard and Scarf 2005)), has long been a central object of study in both economics and computer science. This model with divisible goods is well known for exhibiting strong notions of fairness and efﬁciency. In particular, Varian (1974) showed that when all agents have equal budgets, the equilibrium allocation achieved in a Fisher market is both EF and PO. It is established that such market equilibria can be computed in polynomial time under additive valuation functions (Devanur et al. 2008; Orlin 2010; V´egh 2012). For the constrained case, an EF and PO allocation still exists if each agent has an identical constraint (Cole and Tao 2021), but ﬁnding it is PPAD-complete even in the balanced setting where each agent receives exactly one good (Tr¨obst and Vazirani 2024; Caragiannis, Hansen, and Rathi 2024). Moreover, there exists an allocation that is both SD-EF (which is a stronger notion than EF and balancedness) and ordinally efﬁcient (which is slightly weaker notion than PO) (Kojima 2009); however, such an allocation may not exist even under category constraint (Kawase, Sumita, and Yokoi 2023).

Fair and efﬁcient allocation for indivisible chores For indivisible chores, the existence of EF1 and fPO (or PO) allocations was previously known for a few restricted cases: instances with two agents (Aziz et al. 2022a); instances with bivalued valuations for each agent (Ebadian, Peters, and Shah 2022; Garg, Murhekar, and Qin 2022); instances with two types of chores (Aziz et al. 2023); instances with three agents (Garg, Murhekar, and Qin 2023); and instances with three types of valuation functions (Garg, Murhekar, and Qin 2024). In a signiﬁcant breakthrough, Mahara (2025) recently

17068

<!-- Page 3 -->

showed the existence of EF1 and fPO allocations for general additive valuations.

Fair and efﬁcient allocation under constraints Shoshan, Hazon, and Segal-Halevi (2023) proposed a polynomialtime algorithm for fair division under category constraints with two agents, which ﬁnds an EF1 and PO allocation when each category consists of only goods or only chores. If goods and chores are mixed, the algorithm ﬁnds an EF[1,1] (envy-free up to one good and one chore) and PO allocation. Igarashi and Meunier (2025) extended this result to general settings with n agents, proving the existence of a PO allocation in which each agent can be made envy-free by reallocating at most n(n −1) items.

For budget constraints, Wu, Li, and Gan (2021) showed that any budget-feasible allocation that maximizes the Nash social welfare achieves a 1/4-EF1 and PO allocation for goods. They also showed that there exists an instance in which there is no (1/2 + ε)-EF1 and PO allocation for any ε > 0. Here, α-EF1 is an approximate relaxation of EF1, which requires that each agent prefers their own bundle to α times the bundle of any other agent after the removal of at most one item from that other agent’s bundle. Cookson, Ebadian, and Shah (2025) investigated fair division under matroid constraints, showing that maximizing the Nash social welfare yields a 1/2-EF1 and PO allocation for goods.

For a broader overview of fair division under various constraints, see the survey by Suksompong (2021).

Bivalued and two-type instances For bivalued instances2, Amanatidis et al. (2021) showed that an EFX allocation can be computed in polynomial time for goods. Here, EFX (envy-freeness up to any good) is a stronger fairness concept than EF1. Garg and Murhekar (2023) further showed that both EFX and PO allocations can be computed in polynomial time for goods. In the context of chores, Garg, Murhekar, and Qin (2022) and Ebadian, Peters, and Shah (2022) proved that EF1 and PO allocations can be computed in polynomial time. Additionally, Garg, Murhekar, and Qin (2023) showed that EFX and PO allocations can be computed in polynomial time for chores when there are three agents. Akrami et al. (2022) established that maximizing the Nash social welfare is polynomial-time computable when the two values are multiples of each other, but becomes NPhard when they are coprime.

For instances with two types of valuations, Mahara (2023, 2024a) showed that an EFX allocation always exists for goods under additive valuations, and even under more general monotone valuations. In addition, Garg, Murhekar, and Qin (2023) showed that EF1 and PO allocations can be computed in polynomial time for both goods and chores.

## Model

For each natural number ℓ, we denote [ℓ] = {1,..., ℓ}.

2In a bivalued instance, each agent i assigns one of two ﬁxed values, a > b > 0, to the goods. This setting is a special case of the personalized bivalued instance, where each agent may assign their own pair of distinct values.

An instance of our problem is a tuple (N, M, (vi)i∈N), where N = [n] represents the (non-empty) set of agents and M = [m] represents the (non-empty) set of indivisible goods. Each agent i has a valuation function, denoted as vi: M →R+, where R+ represents the set of nonnegative real numbers. We assume that each agent’s valuation is additive, and write vi(X):= P j∈X vij to denote the utility of agent i when i receives a subset of goods X ⊆M. A valuation function vi is called personalized bivalued if there exist ai, bi ∈R+ with ai > bi such that vij ∈{ai, bi} for all j ∈M.

Throughout this paper, we assume that m is a multiple of n, and deﬁne k:= m/n. An (integral) allocation is an ordered partition A = (A1,..., An) of M, i.e., S i∈N Ai = M and Ai ∩Ai′ = ∅for any distinct i, i′ ∈N. Each Ai is the bundle allocated to agent i. An allocation A is called balanced if |Ai| = k for all i ∈N. We sometimes represent a balanced allocation A by a matrix x ∈{0, 1}N×M, where xij = 1 if good j is allocated to agent i (i.e., j ∈Ai), and xij = 0 otherwise. A balanced fractional allocation is a matrix x ∈RN×M

+ such that P j∈M xij = k for all i ∈N and P i∈N xij = 1 for all j ∈M. By the property of the total unimodularity, the set of balanced fractional allocations forms the convex full of the balanced (integral) allocations (see, e.g., (Schrijver 2003, Sec. 21.2)). Thus, a balanced fractional allocation can be interpreted as a lottery over balanced allocations.

An allocation A is called envy-free up to one good (EF1) if, for all i, i′ ∈N, either Ai′ = ∅, or there exists a good j ∈Ai′ such that vi(Ai) ≥vi(Ai′ \ {j}). A balanced (fractional) allocation x ∈RN×M

+ Pareto-dominates a balanced (fractional) allocation x′ ∈RN×M

+ if (i) P j∈M vijx′ ij ≤ P j∈M vijxij for all i ∈N, and (ii) P j∈M vijx′ ij < P j∈M vijxij for some i ∈N. A balanced allocation is called Pareto optimal (PO) or fractionally Pareto optimal (fPO) if it cannot be Pareto-dominated by any other balanced integral or fractional allocation, respectively.

Observe that the set of achievable valuation vectors (P j∈M v1jx1j,..., P j∈M vnjxnj) arising from balanced fractional allocation x forms a polytope, which is precisely the convex full of the set of valuation vectors (v1(A1),..., vn(An)) corresponding to balanced allocations A. Thus, the fPO allocations can be characterized within the framework of multi-objective linear programming (see, e.g., (Ehrgott 2005)).

Proposition 1. A balanced allocation A is fPO if and only if it maximizes the weighted sum (weighted utilitarian social welfare) P i∈N αivi(Ai) for some positive weight vector α ∈RN

++.

Note that, for any given strictly positive weight vector α, the maximum value P i∈N αi·vi(Ai) taken over all balanced allocations A can be computed by the following linear pro-

17069

<!-- Page 4 -->

gramming (LP):

max P i∈N

P j∈M αivijxij s.t. P i∈N xij = 1 ∀j ∈M, P j∈M xij = k ∀i ∈N, xij ≥0 ∀i ∈N, ∀j ∈M.

(1)

To illustrate the above concepts, we present a concrete example.

Example 1. Consider an instance with N = {1, 2}, M = {1, 2, 3, 4}, and the valuations are

(v11, v12, v13, v14) = (10, 10, 21, 22), and (v21, v22, v23, v24) = (0, 1, 6, 8).

The possible valuation vectors for balanced allocations are visualized in Figure 1. This instance has a unique EF1 and fPO allocation: ({1, 3}, {2, 4}). Note that the allocation ({1, 4}, {2, 3}) is PO but not fPO. Among the balanced allocations, ({1, 2}, {3, 4}) maximizes the Nash social welfare, but it is not EF1. Moreover, in this instance, no EF fractional allocation (i.e., ex ante EF) can be represented as a lottery over EF1 and fPO allocations (i.e., ex post EF1 and fPO).

v1(A1)

v2(A2)

({3, 4}, {1, 2})

({2, 4}, {1, 3})

({2, 3}, {1, 4})

({1, 4}, {2, 3})

({1, 3}, {2, 4})

A = ({1, 2}, {3, 4})

20 25 30 35 40

5

10

**Figure 1.** Possible valuation vectors for balanced allocations in Example 1. Square markers indicate fPO allocations and red markers denote EF1 allocations. The blue region represents the set of possible valuation vectors for fractional balanced allocations.

Properties of EF1 and fPO Allocations In this section, we provide some properties of EF1 and fPO that will be used in subsequent discussions.

It is well known that an EF1 balanced allocation can be computed by the following round-robin procedure (Caragiannis et al. 2019): First, an ordering of the agents is ﬁxed. Then, according to this ordering, the agents take turns sequentially to choose their favorite available good (breaking ties arbitrarily). This process is repeated in multiple rounds until all goods have been allocated. We call the outcome of the round-robin procedure the round-robin allocation.

For a balanced allocation A = (A1,..., An) and a weight vector α ∈RN

++, deﬁne a weighted directed graph G(α)

A = (N ˙∪M ˙∪{r}; −→ E ∪←− E ∪E+, w(α)), where −→ E = N × M, ←− E = {(j, i) ∈M × N | j ∈Ai}, E+ = {r} × M, w(α)(i, j) = −αivij for all (i, j) ∈−→ E, w(α)(j, i) = αivij for all (j, i) ∈←− E, and w(α)(r, j) = 0 for all j ∈M. It is not difﬁcult to see that A maximizes P i∈N αivi(Ai) over all balanced allocations if and only if G(α)

A contains no negative-weight directed cycles. Next, we characterize the optimal solution of LP (1). Its dual is given by:

min k · P i∈N qi + P j∈M pj s.t. qi + pj ≥αivij ∀i ∈N, ∀j ∈M. (2)

We call the dual variables (q, p) the potentials and p the price vector. By the complementary slackness theorem, a feasible pair x and (q, p) forms optimal solutions to the primal and dual LPs if and only if, for all i ∈N and j ∈M, either xij = 0 or qi + pj = αivij.

Let A be a balanced fPO allocation that maximizes the value P i∈N αivi(Ai) for some α ∈RN

++. Then, we can construct an optimal dual solution as follows (see, e.g., Schrijver (2003, Sec. 17.4)). Lemma 1 (folklore). Let A be a balanced allocation that maximizes P i∈N αivi(Ai) for some α ∈RN

++. Then, an optimal dual solution (q, p) to (2) can be obtained by setting qi as the shortest length of r–i path for each i ∈N and −pj as the shortest length of r–j path in G(α)

A. Here, the solution is nonnegative, i.e., (q, p) ∈RN

+ × RM

+. Moreover, the potentials computed in this way do not depend on the choice of A.

We introduce price envy-freeness up to one good (p-EF1), which is a key concept introduced by Barman, Krishnamurthy, and Vaish (2018). This notion has been widely used in the literature for computing EF1 and PO allocations (Barman, Krishnamurthy, and Vaish 2018; Ebadian, Peters, and Shah 2022; Mahara 2024b; Garg, Murhekar, and Qin 2022, 2023, 2024; Mahara 2025). Deﬁnition 1 (p-EF1). Let (q, p) be potentials. For any nonempty set of goods X ⊆M, deﬁne p(X):= P j∈X pj and ˆp(X):= p(X) −maxj∈X pj. An allocation A is called p- EF1 if p(Ai) ≥ˆp(Ai′) for any pair of agents i, i′ ∈N.

For an appropriate choice of prices p, p-EF1 implies EF1. Lemma 2. Given a weight vector α ∈RN

++, let A be an optimal balanced allocation of LP (1), and let (q, p) be an optimal solution of the dual LP (2) such that qi ≥0 for all i ∈N. If A is p-EF1, then it is also EF1.

By the LP formulation, we can check whether a given balanced allocation A is fPO in polynomial time. Theorem 1. Given a balanced allocation A, whether it satisﬁes EF1 and fPO can be checked in polynomial time.

Next, we demonstrate that any instance of the unconstrained problem can be transformed into an equivalent instance with balanced constraint. This is achieved by introducing a set of “dummy” goods that have no value to any agent, allowing for a direct correspondence between the properties of allocations in the two settings. This equivalence is formalized in the following theorem. Theorem 2. For an unconstrained fair allocation instance (N, M, (vi)i∈N), let M ′ be a set of dummy goods of size

17070

<!-- Page 5 -->

|N| · (|M| −1) and let v′ i(X) = vi(X ∩M) for each i ∈N and X ⊆M ∪M ′. The following equivalences hold:

• If an allocation A is PO (resp., fPO, EF1) in the unconstrained instance, then a balanced allocation (A1 ∪ D1,..., An ∪Dn) where (D1,..., Dn) is an ordered partition of M ′ is PO (resp., fPO, EF1) in the balanced instance. • If a balanced allocation A′ is PO (resp., fPO, EF1) in the balanced instance, then an allocation (A1∩M,..., An∩ M) is PO (resp., fPO, EF1) in the unconstrained instance. This theorem implies that if we construct a polynomialtime algorithm to ﬁnd an EF1 and fPO balanced allocation for a speciﬁc setting, then it can also be used to ﬁnd an EF1 and fPO allocation for the corresponding unconstrained setting. This result has immediate algorithmic implications. For instance, our polynomial-time algorithm for the two-types case under the balanced constraint can be directly applied to the two-types case in the unconstrained setting. This is because, after the addition of dummy goods, the agent types remain unchanged, ensuring that the resulting balanced instance continues to fall within the two-types framework.

It is known that, in the unconstrained setting, the problem of deciding whether a given allocation is PO is coNPcomplete (De Keijzer et al. 2009). By combining this with Theorem 2, we obtain the following corollary. Corollary 1. The problem of deciding whether a given balanced allocation is PO is coNP-complete.

Personalized Bivalued Valuations Case In this section, we consider the case of personalized bivalued valuations, where each agent i ∈N assigns to every good j ∈M a value vij ∈{ai, bi} for some ai > bi ≥0. We show that a balanced allocation that is both EF1 and fPO always exists, and that such an allocation can be computed in polynomial time. Theorem 3. When each agent has a personalized bivalued valuation, there always exists a balanced allocation that is both EF1 and fPO. Moreover, such an allocation can be found in polynomial time.

Our algorithm prepare k slots for each agent, and consider perfect matching between slots and goods as a balanced allocation. We set ε = 1/(nk(k + 1)) and the weight of each edge between sth slot of agent i and good j ∈M as w

(i, s), j

= ai/(ai −bi) + s · ε if vij = ai, bi/(ai −bi) if vij = bi.

Our algorithm outputs a balanced allocation A∗corresponding to a maximum weight perfect matching X∗in this weighted bipartite graph. Intuitively, the weights without the s · ε term are chosen so that the objective function increases by the same amount regardless of which agent receives a high-value good. The s · ε term is included to ensure that high-value goods are distributed as evenly as possible among the agents.

In the personalized bivalued setting, fPO allocations can be characterized by a speciﬁc weight vector α such that αi = 1/(ai −bi) for each i ∈N. This motivates the choice of this particular weight vector. Proposition 2. For agents with personalized bivalued valuations, a balanced allocation A is fPO if and only if it maximizes the value P i∈N vi(A′ i)/(ai −bi) over all balanced allocations.

We show that A∗computed in our algorithm satisﬁes both EF1 and fPO. Lemma 3. A∗is EF1 and fPO.

Now we are ready to prove Theorem 3.

Proof of Theorem 3. We can compute the maximum-weight perfect matching X∗in the bipartite graph in polynomial time by the Hungarian algorithm, which runs in polynomial time (Schrijver 2003). From this matching, we construct the balanced allocation A∗deﬁned by A∗ i = { j ∈ M | ((i, s), j) ∈X∗}, which can also be obtained in polynomial time. By Lemma 3, this allocation satisﬁes both EF1 and fPO. Therefore, for agents with personalized bivalued valuations, a balanced allocation that is simultaneously EF1 and fPO always exists and can be computed in polynomial time.

Two Types Case In this section, we consider instances in which agents are partitioned into at most two types, referred to as type-1 and type-2 agents. This structure serves as a tractable intermediate case between the setting of identical agents and fully heterogeneous populations.

We begin by revisiting the simplest case, where all agents belong to a single type; that is, every agent shares the same valuation function (vi = u for all i ∈N). In this setting, the round-robin allocation is not only guaranteed to be EF1, but it also trivially satisﬁes fPO. This is because, with identical valuations, every complete allocation maximizes utilitarian social welfare.

We now turn to the case with two types. For each type t ∈{1, 2}, let Nt denote the set of agents of type t, with nt = |Nt| and n = n1 + n2 the total number of agents. Without loss of generality, we assume N1 = {1,..., n1} and N2 = {n1+1,..., n}. All agents of the same type share an identical valuation function: for each i ∈Nt, vi = ut.

Our main result in this section is the following. Theorem 4. When the number of agent types is at most two, there always exists a balanced allocation that is both EF1 and fPO. Moreover, such an allocation can be found in polynomial time.

To obtain such an fPO balanced allocation, we only consider weight vectors α ∈RN

++ such that αi = 1 for all i ∈N1 and αi = γ for all i ∈N2, where γ ∈R++.

Without loss of generality, we may assume utj̸ = utj′ for some t ∈{1, 2} and j, j′ ∈M. Otherwise, the problem is trivial since every balanced allocation is both EF and fPO. We denote δ:= mint∈{1,2}, j,j′∈M: utj̸=utj′ |utj −utj′|

1 + maxt∈{1,2} maxj∈M utj (> 0).

17071

<!-- Page 6 -->

We search γ for which the resulting balanced allocation A is EF1. Recall that a balanced allocation A maximizes P i∈N αivi(Ai) if and only if G(α)

A contains no negativeweight directed cycles. In what follows, we write G(γ)

A instead of G(α)

A for α = (1,..., 1, γ,..., γ). Deﬁne

C = {γ1, γ2,..., γL}

= n u1j−u1j′ u2j−u2j′ j, j′ ∈M, u1j > u1j′, u2j > u2j′ o to be the set of critical values of γ, where δ < γ1 < γ2 < · · · < γL < 1/δ. Intuitively, a critical value γ represents a point at which a zero cycle appears in G(γ)

A. Note that L = O(m2) since there are at most O(m2) pairs of goods (j, j′). We deﬁne the intervals between these critical values as I1 = [δ, γ1], I2 = [γ1, γ2],..., IL+1 = [γL, 1/δ]. We will denote γ0:= δ and γL+1:= 1/δ. If C = ∅, we deﬁne L = 0. Lemma 4. For each ℓ ∈ [L + 1], if A maximizes P i∈N1 u1(Ai) + P i∈N2 γu2(Ai) for some γ ∈(γℓ−1, γℓ), then it also maximizes the value for any γ ∈[γℓ−1, γℓ] = Iℓ.

For each interval Iℓ, let A(ℓ) be a balanced allocation that maximizes P i∈N1 u1(Ai) + P i∈N2 γu2(Ai) for all γ ∈Iℓ.

Let S(ℓ):= S i∈N1 A(ℓ)

i and T (ℓ):= S i∈N2 A(ℓ)

i. For each interval Iℓand for each γ ∈Iℓ, we determine the potentials (q(γ), p(γ)) ∈RN

+ × RM

+ according to the procedure described in Lemma 1. Here, we do not need to specify ℓsince the potentials do not depend on the choice of the allocation. Since agents of the same type have identical valuations and identical weights, there exists a path of length 0 in G(γ)

A(ℓ) between any two agents of the same type. Thus, we have q(γ)

i = q(γ)

i′ for any i, i′ ∈N1 and q(γ)

i = q(γ)

i′ for any i, i′ ∈N2. We redistribute the goods in S(ℓ) among the type- 1 agents, and those in T (ℓ) among the type-2 agents, using the round-robin procedure with respect to the price vector p(γ). Let (X(ℓ,γ)

1,..., X(ℓ,γ)

n1) and (Y (ℓ,γ)

1,..., Y (ℓ,γ)

n2) denote the resulting allocations for type-1 and type-2 agents, respectively. We assume that the round-robin is applied in the order of indices. Then, we have the following relations. Lemma 5. For any ℓ∈[L + 1] and γ ∈Iℓwe have p(γ)(X(ℓ,γ)

1) ≥· · · ≥p(γ)(X(ℓ,γ)

n1)

≥ˆp(γ)(X(ℓ,γ)

1) ≥· · · ≥ˆp(γ)(X(ℓ,γ)

n1), and p(γ)(Y (ℓ,γ)

1) ≥· · · ≥p(γ)(Y (ℓ,γ)

n2)

≥ˆp(γ)(Y (ℓ,γ)

1) ≥· · · ≥ˆp(γ)(Y (ℓ,γ)

n2).

Let ˆ A(ℓ,γ) = (X(ℓ,γ)

1,..., X(ℓ,γ)

n1, Y (ℓ,γ)

1,..., Y (ℓ,γ)

n2). We will omit the superscripts (γ), (ℓ) and (ℓ, γ) when they are clear from the context.

For each interval Iℓ, we ﬁrst check whether ˆ A(ℓ,γ) is EF1 for γ = γℓ−1 and γ = γℓ. If either allocation is EF1, we immediately return it as an EF1 and fPO balanced allocation. If not, we examine the following two conditions for each ℓ∈[L + 1] and γ ∈{γℓ−1, γℓ}:

(a) p(γ)(X(ℓ,γ)

n1) ≥ˆp(γ)(Y (ℓ,γ)

1),

(b) p(γ)(Y (ℓ,γ)

n2) ≥ˆp(γ)(X(ℓ,γ)

1).

We will show in Lemma 7 that at least one of these two conditions holds for any (ℓ, γ). Furthermore, if both conditions hold for some (ℓ, γ), then ˆ A(ℓ,γ) is EF1 (Lemma 6). Since we have assumed that neither endpoint allocation is EF1, exactly one of the two conditions holds at each endpoint. Additionally, we will show in Lemma 8 that condition (a) holds at (ℓ, γ) = (1, δ) and condition (b) holds at (ℓ, γ) = (L + 1, 1/δ). Therefore, as we move through the intervals, at least one of the following two situations must occur:

• Case 1: For some ℓ∈[L + 1], condition (a) holds at (ℓ, γℓ−1) and condition (b) holds at (ℓ, γℓ). • Case 2: For some ℓ∈[L], condition (a) holds at (ℓ, γℓ) and condition (b) holds at (ℓ+ 1, γℓ).

We can ﬁnd such an ℓin polynomial time by checking the conditions for each ℓ∈[L + 1] and γ ∈{γℓ−1, γℓ}.

If we encounter Case 1, there exists γ∗∈Iℓsuch that ˆ A(ℓ,γ∗) satisﬁes both conditions (a) and (b) (Lemma 10). Therefore, ˆ A(ℓ,γ∗) is EF1 and fPO by Lemma 6. We search for such a γ∗by tracking the changes as we continuously increase γ within the interval Iℓ. Since all agents of the same type share the same q(γ)

i, there is a shortest path from the root r to each node in N ∪M that uses at most four edges in GA(ℓ). There are at most O(m2) such paths. The length of each path is a linear function of γ, so each −q(γ)

i and p(γ)

j can be represented as the minimum of O(m2) linear functions in γ. Thus, −q(γ)

i and p(γ)

j are piecewise linear functions with at most O(m2) segments. This structure allows us to efﬁciently track the changes in the potentials as γ varies, enabling us to ﬁnd a suitable γ∗that satisﬁes both conditions (a) and (b) in polynomial time.

If we encounter Case 2, we construct a sequence of allocations by successively exchanging one good from a type-1 agent with one good from a type-2 agent at each step, transitioning from ˆ A(ℓ,γℓ) to ˆ A(ℓ+1,γℓ). Speciﬁcally, at each step, we select a pair of goods (j1, j2) with j1 assigned to a type- 1 agent and j2 assigned to a type-2 agent, and swap their assignments. Then, we redistribute the goods among type-1 agents and those among type-2 agents using the round-robin procedure with respect to the price vector p(γℓ). By repeating such single-good exchanges, we can transform ˆ A(ℓ,γℓ)

into ˆ A(ℓ+1,γℓ). We will show that during this process, we reach an allocation that satisﬁes both conditions (a) and (b), thus yielding an EF1 and fPO balanced allocation (Lemmas 11 and 12).

We now proceed to the proofs. We ﬁrst show that if ˆ A satisﬁes the conditions (a) and (b), then it is EF1.

Lemma 6. Let ℓ∈[L + 1] and γ ∈Iℓ. If p(γ)(X(ℓ,γ)

n1) ≥ ˆp(γ)(Y (ℓ,γ)

1), then the envy from a type-1 agent to a type-2 agent can be eliminated by removing one good. Similarly, if p(γ)(Y (ℓ,γ)

n2) ≥ˆp(γ)(X(ℓ,γ)

1), then the envy from a type-2 agent to a type-1 agent can be eliminated by removing one

17072

<!-- Page 7 -->

good. In addition, if both conditions hold, then the allocation is EF1.

Next, we show that at least one of the conditions (a) or (b) holds for any ℓ∈[L + 1] and γ ∈Iℓ. Lemma 7. For any ℓ∈[L + 1] and γ ∈Iℓ, at least one of p(γ)(X(ℓ,γ)

n1) ≥ˆp(γ)(Y (ℓ,γ)

1) or p(γ)(Y (ℓ,γ)

n2) ≥ˆp(γ)(X(ℓ,γ)

1) holds.

We show that if ˆ A(1,δ) is not EF1, then condition (a) holds for (ℓ, γ) = (1, δ), and if ˆ A(L+1,1/δ) is not EF1, then condition (b) holds for (ℓ, γ) = (L + 1, 1/δ).

Lemma 8. If ˆ A(1,δ) is not EF1, then p(δ)(X(1,δ)

n1) ≥ ˆp(δ)(Y (1,δ)

1). Also, if ˆ A(L+1,1/δ) is not EF1, then p(1/δ)(Y (L+1,1/δ)

n2) ≥ˆp(1/δ)(X(L+1,1/δ)

1). We establish the existence of the desired γ∗in Case 1. As a preliminary step, we show the continuity of the prices received by each agent. Lemma 9. For each ℓ∈[L + 1], i ∈N1, and i′ ∈ N2, the values p(γ)(X(ℓ,γ)

i), ˆp(γ)(X(ℓ,γ)

i), p(γ)(Y (ℓ,γ)

i′), and ˆp(γ)(Y (ℓ,γ)

i′) are continuous with respect to γ over Iℓ. Now we can prove the existence of γ∗in Case 1. Lemma 10. Take any ℓin [L + 1]. Consider the case where p(γℓ−1)(X(ℓ,γℓ−1)

n1) ≥ˆp(γℓ−1)(Y (ℓ,γℓ−1)

1) and p(γℓ)(Y (ℓ,γℓ)

n2) ≥ˆp(γℓ)(X(ℓ,γℓ)

1). Then, there exists γ∗∈ Iℓ such that p(γ∗)(X(ℓ,γ∗)

n1) ≥ ˆp(γ∗)(Y (ℓ,γ∗)

1) and p(γ∗)(Y (ℓ,γ∗)

n2) ≥ˆp(γ∗)(X(ℓ,γ∗)

1). Moreover, such a γ∗can be computed in polynomial time.

We next show that, if we encounter Case 2, then we can ﬁnd an EF1 and fPO balanced allocation by successively exchanging one good from a type-1 agent with one good from a type-2 agent. Let ℓbe the index chosen in the algorithm. Since both A(ℓ) and A(ℓ+1) maximize P i∈N1 u1(Ai) + γℓ

P i∈N2 u2(Ai), we have q(γℓ)

i +p(γℓ)

j = u1j for all i ∈N1 and j ∈S(ℓ) ∪S(ℓ+1), and q(γℓ)

i + p(γℓ)

j = γℓu2j for all i ∈N2 and j ∈T (ℓ) ∪T (ℓ+1). We observe that ˆ A obtained during the process of Case 2 is always fPO.

Lemma 11. Fix ℓ∈[L + 1] and let (q, p) = (q(γℓ), p(γℓ)). Suppose M is partitioned into S and T with S ⊆ S(ℓ) ∪S(ℓ+1) and T ⊆ T (ℓ) ∪T (ℓ+1). Let ˆ A = (X1,..., Xn1, Y1,..., Yn2) be the balanced allocation obtained by the round-robin procedure with respect to p, assigning goods in S to type-1 agents and goods in T to type-2 agents. Then, ˆ A is fPO.

Next, we show that if ˆ A does not satisfy condition (b) at some step, then ˆ A at the next step satisﬁes condition (a). Lemma 12. Let (S, T) be a partition of M and p ∈RN

+. Let ˆ A = (X1,..., Xn1, Y1,..., Yn2) be the balanced allocation obtained by the round-robin procedure with respect to p, assigning goods in S to type-1 agents and goods in T to type-2 agents. Suppose j1 ∈S and j2 ∈T, and consider the new partition (S′, T ′) = (S \{j1}∪{j2}, T \{j2}∪{j1}), and let ˆ A′ = (X′

1,..., X′ n1, Y ′

1,..., Y ′ n2) be the balanced allocation obtained by round-robin with respect to (S′, T ′) and p. Then, if p(Yn2) < ˆp(X1), we have p(X′ n1) ≥ˆp(Y ′

1).

This lemma implies that if we encounter Case 2, we can ﬁnd an EF1 and fPO balanced allocation by successively exchanging goods between type-1 and type-2 agents until conditions (a) and (b) are satisﬁed. This is because ˆ A = ˆ A(ℓ,γℓ) at the ﬁrst step satisﬁes condition (a), and at the end we will have ˆ A = ˆ A(ℓ+1,γℓ) and it satisﬁes condition (b). If an allocation satisﬁes both conditions (a) and (b), then it is EF1 by Lemma 6.

Now, we are ready to prove Theorem 4.

Proof of Theorem 4. If ˆ A(ℓ,γ) is EF1 for some ℓ∈[L + 1] and γ ∈{γℓ−1, γℓ}, then the algorithm returns it as an EF1 and fPO balanced allocation. Otherwise, the algorithm ﬁnds an EF1 and fPO balanced allocation via Case 1 or Case 2, depending on which situation occurs. For Case 1, it ﬁnds γ∗∈Iℓsuch that ˆ A(ℓ,γ∗) satisﬁes both conditions (a) and (b), and returns it as an EF1 and fPO balanced allocation by Lemma 10. For Case 2, it ﬁnds an EF1 and fPO balanced allocation by Lemma 11 and Lemma 12. Thus, the algorithm always ﬁnds an EF1 and fPO balanced allocation.

For each ℓ∈[L + 1], the allocation A(ℓ) can be computed in polynomial time by the Hungarian algorithm. For each ℓ∈[L + 1] and γ ∈Iℓ, we can compute the potential (q(γ), p(γ)) in polynomial time by the Bellman–Ford algorithm by Lemma 1. We can then compute the allocation ˆ A(ℓ,γ) in polynomial time since the round-robin redistribution of goods takes O(m) time. Since L = O(m2) and the critical values can be computed in O(m2) time, we can check whether ˆ A(ℓ,γ) is EF1 for each ℓ∈[L + 1] and γ ∈{γℓ−1, γℓ} in polynomial time. For Case 1, we can ﬁnd a desired γ in polynomial time by Lemma 10. Hence, the total time complexity for Case 1 is polynomial. For Case 2, we can ﬁnd an EF1 and fPO balanced allocation in polynomial time since we only need to perform a sequence of single-good exchanges, and the number of such exchanges is at most O(m).

## Conclusion

In this paper, we addressed the problem of ﬁnding a fair and efﬁcient allocation of indivisible goods under the balanced constraint, where each agent receives the same number of goods. Our main contribution is to afﬁrmatively resolve the existence and polynomial-time computability of allocations that are simultaneously EF1 and fPO in two important cases: when agents have personalized bivalued valuations and when there are at most two types of agents. We developed novel polynomial-time algorithms for both scenarios, leveraging techniques from maximum-weight perfect matching.

A natural next step is to extend our results beyond two types of agents to the general case of three or more types, but this becomes much more complex.

17073

<!-- Page 8 -->

## Acknowledgments

This work was partially supported by the joint project of Kyoto University and Toyota Motor Corporation, titled “Advanced Mathematical Science for Mobility Society” and supported by JST ERATO Grant Number JPMJER2301, JST PRESTO Grant Number JPMJPR2122, JSPS KAKENHI Grant Numbers JP23K19956 and JP25K00137, Japan.

## References

Akrami, H.; Chaudhury, B. R.; Hoefer, M.; Mehlhorn, K.; Schmalhofer, M.; Shahkarami, G.; Varricchio, G.; Vermande, Q.; and van Wijland, E. 2022. Maximizing Nash social welfare in 2-value instances. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence (AAAI), 4760–4767. Amanatidis, G.; Aziz, H.; Birmpas, G.; Filos-Ratsikas, A.; Li, B.; Moulin, H.; Voudouris, A. A.; and Wu, X. 2023. Fair division of indivisible goods: Recent progress and open questions. Artiﬁcial Intelligence, 322: 103965. Amanatidis, G.; Birmpas, G.; Filos-Ratsikas, A.; Hollender, A.; and Voudouris, A. A. 2021. Maximum Nash welfare and other stories about EFX. Theoretical Computer Science, 863: 69–85. Aziz, H.; Caragiannis, I.; Igarashi, A.; and Walsh, T. 2022a. Fair allocation of indivisible goods and chores. Autonomous Agents and Multi-Agent Systems, 36: 1–21. Aziz, H.; Li, B.; Moulin, H.; and Wu, X. 2022b. Algorithmic fair allocation of indivisible items: A survey and new questions. ACM SIGecom Exchanges, 20(1): 24–40. Aziz, H.; Lindsay, J.; Ritossa, A.; and Suzuki, M. 2023. Fair Allocation of Two Types of Chores. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 143–151. Barman, S.; Krishnamurthy, S. K.; and Vaish, R. 2018. Finding fair and efﬁcient allocations. In Proceedings of the 2018 ACM Conference on Economics and Computation (EC), 557–574. Brainard, W. C.; and Scarf, H. E. 2005. How to compute equilibrium prices in 1891. American Journal of Economics and Sociology, 64(1): 57–83. Brams, S. J.; and Taylor, A. D. 1996. Fair Division: From cake-cutting to dispute resolution. Cambridge University Press. Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D. 2016. Handbook of computational social choice. Cambridge University Press. Budish, E. 2011. The combinatorial assignment problem: Approximate competitive equilibrium from equal incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Hansen, K. A.; and Rathi, N. 2024. On the complexity of Pareto-optimal and envy-free lotteries. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 244– 252. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The unreasonable fairness of maximum Nash welfare. ACM Transactions on Economics and Computation, 7(3): 12:1–32. Cole, R.; and Tao, Y. 2021. On the existence of Pareto ef- ﬁcient and envy-free allocations. Journal of Economic Theory, 193: 105207. Cookson, B.; Ebadian, S.; and Shah, N. 2025. Constrained fair and efﬁcient allocations. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence (AAAI), 13718–13726. De Keijzer, B.; Bouveret, S.; Klos, T.; and Zhang, Y. 2009. On the complexity of efﬁciency and envy-freeness in fair division of indivisible goods with additive preferences. In International Conference on Algorithmic Decision Theory, 98–110. Springer. Devanur, N. R.; Papadimitriou, C. H.; Saberi, A.; and Vazirani, V. V. 2008. Market equilibrium via a primal–dual algorithm for a convex program. Journal of the ACM, 55(5): 22:1–18. Ebadian, S.; Peters, D.; and Shah, N. 2022. How to fairly allocate easy and difﬁcult chores. In Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 372–380. Ehrgott, M. 2005. Multicriteria Optimization. Berlin; New York: Springer, 2nd edition. Foley, D. K. 1966. Resource allocation and the public sector. Yale University. Garg, J.; and Murhekar, A. 2023. Computing fair and efﬁcient allocations with few utility values. Theoretical Computer Science, 962: 113932. Garg, J.; Murhekar, A.; and Qin, J. 2022. Fair and efﬁcient allocations of chores under bivalued preferences. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence (AAAI), 5043–5050. Garg, J.; Murhekar, A.; and Qin, J. 2023. New algorithms for the fair and efﬁcient allocation of indivisible chores. In Proceedings of the 32nd International Joint Conference on Artiﬁcial Intelligence (IJCAI), 2710–2718. Garg, J.; Murhekar, A.; and Qin, J. 2024. Weighted EF1 and PO allocations with few types of agents or chores. In Proceedings of the 33rd International Joint Conference on Artiﬁcial Intelligence (IJCAI), 2799–2806. Guo, H.; Li, W.; and Deng, B. 2023. A survey on fair allocation of chores. Mathematics, 11(16): 3616:1–28. Igarashi, A.; and Meunier, F. 2025. Fair and efﬁcient allocation of indivisible items under category constraints. arXiv:2503.20260. Kaneko, M.; and Nakamura, K. 1979. The Nash social welfare function. Econometrica: Journal of the Econometric Society, 423–435. Kawase, Y.; and Sumita, H. 2020. On the max-min fair stochastic allocation of indivisible goods. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, 2070–2078. Kawase, Y.; Sumita, H.; and Yokoi, Y. 2023. Random assignment of indivisible goods under constraints. In Proceedings of the 32nd International Joint Conference on Artiﬁcial Intelligence (IJCAI), 2792–2799.

17074

<!-- Page 9 -->

Kojima, F. 2009. Random assignment of multiple indivisible objects. Mathematical Social Sciences, 57(1): 134–142. Lee, E. 2017. APX-hardness of maximizing Nash social welfare with indivisible items. Information Processing Letters, 122: 17–20. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In Proceedings of the 5th ACM Conference on Electronic Commerce (EC), 125–131. Mahara, R. 2023. Existence of EFX for two additive valuations. Discrete Applied Mathematics, 340: 115–122. Mahara, R. 2024a. Extension of additive valuations to general valuations on the existence of EFX. Mathematics of operations research, 49(2): 1263–1277. Mahara, R. 2024b. A polynomial-time algorithm for fair and efﬁcient allocation with a ﬁxed number of agents. arXiv:2411.01810. Mahara, R. 2025. Existence of fair and efﬁcient allocation of indivisible chores. arXiv:2507.09544. Nash, J. F. 1950. The bargaining problem. Econometrica, 18(2): 155–162. Nguyen, N.-T.; Nguyen, T. T.; Roos, M.; and Rothe, J. 2014. Computational complexity and approximability of social welfare optimization in multiagent resource allocation. Autonomous agents and multi-agent systems, 28(2): 256–289. Orlin, J. B. 2010. Improved algorithms for computing Fisher’s market clearing prices: Computing Fisher’s market clearing prices. In Proceedings of the forty-second ACM symposium on Theory of computing (STOC), 291–300. Schrijver, A. 2003. Combinatorial Optimization: Polyhedra and Efﬁciency. Algorithms and Combinatorics. Springer. Shoshan, H.; Hazon, N.; and Segal-Halevi, E. 2023. Ef- ﬁcient nearly-fair division with capacity constraints. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 206– 214. Suksompong, W. 2021. Constraints in fair division. ACM SIGecom Exchanges, 19(2): 46–61. Tr¨obst, T.; and Vazirani, V. V. 2024. Cardinal-utility matching markets: The quest for envy-freeness, Pareto-optimality, and efﬁcient computability. arXiv:2402.08851. Varian, H. R. 1974. Equity, envy, and efﬁciency. Journal of Economic Theory, 9(1): 63–91. V´egh, L. A. 2012. Strongly polynomial algorithm for a class of minimum-cost ﬂow problems with separable convex objectives. In Proceedings of the forty-fourth annual ACM symposium on Theory of computing (STOC), 27–40. Wu, X.; Li, B.; and Gan, J. 2021. Budget-feasible maximum Nash social welfare is almost envy-free. In Proceedings of the 30th International Joint Conference on Artiﬁcial Intelligence (IJCAI), 465–471.

17075
