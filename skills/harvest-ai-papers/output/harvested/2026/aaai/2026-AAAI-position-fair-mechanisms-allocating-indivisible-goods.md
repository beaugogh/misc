---
title: "Position Fair Mechanisms Allocating Indivisible Goods"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38763
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38763/42725
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Position Fair Mechanisms Allocating Indivisible Goods

<!-- Page 1 -->

Position Fair Mechanisms Allocating Indivisible Goods

Ryoga Mahara1, Ryuhei Mizutani2, Taihei Oki3,4, Tomohiko Yokoyama1

1The University of Tokyo, Japan 2Keio Univeristy, Japan 3Hokkaido Univeristy, Japan 4RIKEN, Japan {mahara, tomohiko yokoyama}@mist.u-tokyo.ne.jp, mizutani@math.keio.ac.jp, oki@icredd.hokudai.ac.jp

## Abstract

Fair division mechanisms for indivisible goods require agent orderings to deterministically select one allocation when running the algorithm in practice. We introduce position envyfreeness up to one good (PEF1) as a fairness criterion for mechanisms: a mechanism is said to satisfy PEF1 if for any pair of agent orderings, no agent prefers their bundle determined under one ordering to that under another ordering by more than the utility of a single good. First, we propose a scale-invariant, polynomial-time mechanism that satisfies PEF1 and yields an envy-freeness up to one good (EF1) allocation. For the case of two agents, we establish that any mechanism producing a maximum Nash welfare allocation eliminates envy based on positions by removing one good, provided that utilities are positive. Additionally, we present a polynomial-time mechanism based on the adjusted winner procedure, which satisfies PEF1 and produces an EF1 and Pareto optimal allocation for two agents. In contrast, we demonstrate that well-known mechanisms such as roundrobin and envy-cycle elimination do not generally satisfy PEF1.

## Introduction

Fair division of indivisible goods among agents is a fundamental problem in economics and computer science with significant practical importance. Applications range from course allocation in universities (Budish et al. 2016) and inheritance division (Goldman and Procaccia 2015) to various other real-world settings (Igarashi and Yokoyama 2023; Han and Suksompong 2024). For surveys, see (Walsh 2020; Aziz et al. 2022b; Amanatidis et al. 2023). In fair division, agents are typically assumed to have additive utilities over bundles of goods, and the challenge is to find an allocation that meets certain fairness criteria. One well-studied criterion is envyfreeness (Foley 1967), which requires an allocation to satisfy that no agent prefers another agent’s bundle to their own.

In this paper, we consider fairness properties not of allocations but of mechanisms, which have received little attention in existing work. Particularly, we deal with fairness regarding an input order of agents. To illustrate this, consider a situation where two agents have identical utilities for one good, requiring mechanisms to establish clear rules for

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

determining which agent receives it. Namely, mechanisms must incorporate an ordering among the agents.

We formalize mechanisms as follows (see Section 2.2 and Figure 1 for formal definitions). The input of a mechanism is a tuple of utilities arranged by an agent ordering. The mechanism prioritizes agents based on their positions in the agent ordering, and outputs an allocation. Under this framework, utilities that agents obtain by the mechanism can vary substantially depending on their positions in the agent ordering.

Previous work by Manabe and Okamoto (2012) introduced a fairness concept for mechanisms in the divisible goods setting, based on agent orderings. This concept, called meta-envy-freeness, requires a mechanism to ensure that each agent obtains the same utility regardless of the agent ordering. A meta-envy-free mechanism always exists for divisible goods since divisible goods can be split equally among agents. Specifically, when n agents desire a single good, each can simply receive 1/n of the good, obtaining identical utilities.

In contrast, for indivisible goods, the situation differs significantly. A meta-envy-free mechanism cannot exist even with two agents and a single good, as only the agent in the higher priority position can receive the good.

A similar difficulty arises for envy-freeness in the indivisible goods setting, where envy-free allocations do not always exist. This motivated the development of relaxations such as envy-freeness up to one good (EF1) (Budish 2011). An allocation is said to be EF1 if any agent’s envy toward another agent can be eliminated by removing a single good from the envied agent’s bundle. Importantly, an EF1 allocation always exists for agents with additive utilities (Lipton et al. 2004; Caragiannis et al. 2019).

Inspired by EF1 and the concept of meta-envy-freeness, we introduce position envy-freeness up to one good (PEF1)1 as a fairness criterion for mechanisms with respect to agent orderings. A mechanism is said to satisfy PEF1 if for any agent and two agent orderings, their envy towards a bundle under one ordering over that under another ordering can be eliminated by removing a single good from the envied bundle.

Since PEF1 is a property of mechanisms concerning dif-

1We use the term “position envy-free” instead of “meta-envyfree” to clarify the meaning of “meta.”

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17137

<!-- Page 2 -->

ferent agent orderings, a PEF1 mechanism may not produce a fair allocation. This raises a fundamental question: can we design a mechanism that satisfies PEF1 and is guaranteed to produce an EF1 allocation?

Our Results First, we answer the above question affirmatively by presenting a PEF1 mechanism that always produces an EF1 allocation (Theorem 3). The mechanism employs a maximum-weight matching to determine a bundle for agents in each round. Notably, the mechanism runs in polynomial time.

Second, for two agents, we establish that any mechanism that maximizes the Nash welfare (i.e., the geometric mean of agents’ utilities) satisfies PEF1. Since a maximum Nash welfare (MNW) allocation is both EF1 and Pareto optimal (PO, i.e., no allocation makes some agent better off without making another agent worse off) (Caragiannis et al. 2019), this mechanism outputs an allocation that satisfies both EF1 and PO. While computing a MNW allocation is NP-hard (Nguyen et al. 2014) and even APX-hard (Lee 2017), we present a modified version of the adjusted winner mechanism (Brams and Taylor 1996; Aziz et al. 2015, 2022a) that is PEF1, runs in polynomial time, and produces an EF1 and PO allocation for the case of two agents.

Finally, we analyze the round-robin mechanism, which produces an EF1 allocation (Caragiannis et al. 2019). We show that the mechanism satisfies PEF1 for the case of at most three agents and it lacks PEF1 when the number of agents is at least four. In addition, we show that the envycycle mechanism, which returns an EF1 allocation when agents have monotone utility functions (Lipton et al. 2004), also fails to satisfy PEF1 in general.

We remark that all mechanisms proposed in this paper are scale-invariant; namely, scaling an agent’s utility by any positive constant does not affect the output.

Further Related Work A mechanism is said to be anonymous if for any agent ordering, the outcome allocation of the mechanism remains unchanged (Gibbard 1973; Satterthwaite 1975). In this paper, we distinguish between anonymity and position (meta-)envy-freeness. Position envy-freeness ensures that the utilities that agents receive do not change, while the allocation produced by the mechanism may vary depending on the agent ordering.

The equal-treatment-of-equals (ETE) is also a fairness concept for mechanisms (Moulin 2004). A mechanism satisfies ETE if agents with identical preferences receive the same bundle of goods.

Similar to position envy-freeness, both anonymity and ETE are impossible to achieve for indivisible goods. For divisible goods, the compatibility of anonymity and ETE with fairness and efficiency properties has been extensively studied (Shapley and Scarf 1974; Zhou 1990; Bogomolnaia and Moulin 2001; Roth, S¨onmez, and ¨Unver 2005; Bei, Huzhang, and Suksompong 2020).

Our work also relates to a fairness concept in allocation rules. An allocation rule is a map from utility profiles to sets of allocations satisfying specified criteria (S¨onmez 1999). An allocation rule is essentially-single-valued if for any utility profile and any two allocations in its output set, each agent receives equal utility from these allocations (S¨onmez 1999). If a mechanism always selects its output from allocations determined by an essentially-single-valued allocation rule, then the mechanism is meta-envy-free. It is known that the MNW allocation rule, defined as a mapping to all MNW allocations, is essentially-single-valued for agents with continuous utility functions over divisible goods (Dubins and Spanier 1961; Segal-Halevi and Sziklai 2019).

## Preliminaries

## 2.1 Fair Division Model

Let M be the set of m goods and N be the set of n agents. A subset of M is termed a bundle. Each agent a ∈N has a non-negative utility function ua: 2M →R≥0. For simplicity, we denote ua(g) as ua({g}) for each g ∈M. We assume that ua is additive, that is, we have ua(S) = P g∈S ua(g) for any S ⊆M. A family u = {ua}a∈N of the utility functions of all agents is called a profile. Let U≥0 denote the set of all profiles. An allocation A = {Aa}a∈N is a partition of M into n bundles, where Aa denotes the bundle of agent a ∈N.

We now introduce a fairness concept of an allocation. An allocation A is said to be envy-free if no agent envies any other agent, i.e., ua(Aa) ≥ua(Aa′) for all a, a′ ∈N. An allocation A is called envy-free up to one good (EF1) if for all a, a′ ∈N with Aa′̸ = ∅, there exists a good g ∈Aa′ such that ua(Aa) ≥ua(Aa′ \ {g}).

Next, we define an efficiency concept. An allocation A is said to Pareto dominate another allocation A′ if ua(Aa) ≥ ua(A′ a) for all a ∈N and ua′(Aa′) > ua′(A′ a′) for some a′ ∈N. An allocation A is called Pareto optimal (PO) if there is no allocation that Pareto dominates A.

## 2.2 Mechanism and Position Fairness

We now introduce several notions related to agent orderings. An agent ordering is defined as a bijection from N to [n] = {1, 2,..., n}. We call π(a) the position of agent a under π. Let Π denote the set of all agent orderings. An ordered profile u = (u1, u2,..., un) is an ordered ntuple of utility functions. Given an agent ordering π, let uπ be an ordered profile generated from an original profile u = {ua}a∈N by mapping utility functions according to π, i.e., (uπ)i = uπ−1(i) for each i ∈[n]. An ordered allocation A = (A1, A2,..., An) is a partition of M into n bundles indexed from 1 to n.

A mechanism M is defined as a map from ordered profiles to ordered allocations. More precisely, an input of a mechanism is an ordered profile uπ generated from a profile u and an agent ordering π, and the mechanism cannot access u and π; in other words, the mechanism is ignorant of the correspondence between agents and their positions in π. Then, M(uπ) means the ordered allocation returned by M when the input is uπ. See Figure 1 for an illustration.

We now define a fairness concept of a mechanism concerning agent orderings, called position envy-freeness. This concept means that no agent envies the bundle under one agent ordering π compared to that under another agent ordering π′.

17138

<!-- Page 3 -->

Profile u = {ua}a∈N

Ordered profile uπ Ordered profile uπ′ π π′

Ordered allocation M(uπ)

Ordered allocation M(uπ′)

M M

Allocation {M(uπ)π(a)}a∈N

Allocation {M(uπ′)π′(a)}a∈N

PEF1

**Figure 1.** An illustration of a mechanism M and fairness concepts.

Definition 1. A mechanism M satisfies position envyfreeness with respect to U≥0 if for any profile u ∈U≥0, for any agent orderings π, π′ ∈Π, and for any agent a ∈N, ua

M(uπ)π(a)

≥ua

M(uπ′)π′(a)

. As mentioned in Section 1, this concept is already known as meta-envy-freeness (Manabe and Okamoto 2012) in fair division for divisible goods.

Unfortunately, a position envy-free mechanism may not exist for indivisible goods. Consider a setting with two agents and a single good, where both agents have identical utility functions. The input of a mechanism is an ordered tuple of the same two utility functions. Without knowing the correspondence between agents and their positions, the mechanism must allocate the good consistently to a fixed position (e.g., position 1). This leads to a violation of position envy-freeness since they receive the good when assigned to position 1 but not when assigned to position 2.

Following the spirit of EF1, we introduce a relaxation of the position envy-freeness, called position envy-freeness up to one good (PEF1). This relaxation allows for some degree of position-based disparity, bounded by the utility of at most one good. See also Figure 1. Definition 2. A mechanism M satisfies position envyfreeness up to one good (PEF1) with respect to U≥0 if for any profile u ∈U≥0, agent orderings π, π′ ∈Π, and agent a ∈N with M(uπ′)π′(a)̸ = ∅, there exists a good g ∈M(uπ′)π′(a) such that ua

M(uπ)π(a)

≥ua

M(uπ′)π′(a) \ {g}

. When we write PEF1 without further specification, we mean PEF1 with respect to U≥0.

Additionally, we define the scale-invariance of mechanisms. For a profile u and a tuple of positive real numbers α = (αa)a∈N ∈Rn

>0 indexed by agents in N, let αu denote the profile defined as (αu)a(S) = αa · ua(S) for every a ∈N and S ⊆M. A mechanism M is called scaleinvariant if M(uπ) = M((αu)π) for every profile u, tuple α ∈Rn

>0, and agent ordering π ∈Π.

## Algorithm

1: Round-Robin Mechanism

Input: Ordered profile (u1, u2,..., un) Output: Ordered allocation (A1, A2,..., An)

1: Fix indices of goods. 2: Ai ←∅for all i ∈[n] 3: i ←1 4: while A1 ∪A2 ∪· · · ∪An ⊊M do 5: Take g ∈argmaxg′∈M\(A1∪A2∪···∪An) ui(g′) 6: Ai ←Ai ∪{g} 7: i ←(i mod n) + 1 8: return (A1, A2,..., An)

To explain these concepts, we present the round-robin mechanism (Caragiannis et al. 2019) described in Algorithm 1. The mechanism first gives a total order of the goods for tie breaking. Then it operates by having agents sequentially select their most preferred remaining good, following the order specified by π−1(1) to π−1(n). Ties are broken by choosing the good with the smallest order. This process continues until all goods are allocated. The round-robin mechanism possesses two important properties: it is scale-invariant and outputs EF1 allocation for any profile and agent ordering (Caragiannis et al. 2019).

While the round-robin mechanism gives an EF1 allocation, it does not satisfy PEF1. To illustrate this, consider an instance with four agents, five goods, and a profile u as shown in Table 1 with positive values x > y > z > 0. Consider two agent orderings π, π′ ∈Π such that π(ai) = i and π′(ai) = 5−i for each i ∈{1, 2, 3, 4}. Let M be the roundrobin mechanism and let A = M(uπ) and B = M(uπ′). Under π, agent a1 receives Aπ(a1) = {g1, g5}, while under π′, agent a1 receives Bπ′(a1) = {g4}. For any g ∈Aπ(a1), we have ua1(Aπ(a1) \ {g}) > z = ua1(Bπ′(a1)), which violates PEF1.

g1 g2 g3 g4 g5 Agent a1 x 0 0 z y Agent a2 0 x 0 0 y Agent a3 x 0 y 0 0 Agent a4 0 x z y 0

**Table 1.** An example utility profile where the round-robin mechanism violates PEF1.

More generally, for the round-robin mechanism M, if ⌈m n ⌉≥⌊log2 n⌋, there exist a profile u and agent orderings π, π′ such that even after removing any ⌊log2 n⌋−1 goods from M(uπ), the agent still prefers M(uπ′) (Theorem 10). Further discussion of the round-robin mechanism can be found in Section 5.

Existence of a Scale-Invariant PEF1 Mechanism Producing an EF1 Allocation

In this section, we present our main result.

17139

<!-- Page 4 -->

## Algorithm

2: A Scale-Invariant and PEF1 Mechanism Producing an EF1 Allocation

Input: Ordered profile (u1, u2,..., un) Output: Ordered allocation (A1, A2,..., An)

1: Fix indices of goods as M = {g1, g2,..., gm}. 2: Add dummy goods until m is divisible by n. 3: Ai ←∅for all i ∈[n] and I ←M 4: for r = 1 to ⌈m n ⌉do 5: Compute a maximum-weight matching µr with respect to w defined by the equation (1) in Gr = ([n] ∪I, Er). 6: Let µr(i) denote the good in I matched with i ∈[n] under µr. 7: for i = 1 to n do 8: Ai ←Ai ∪{µr(i)} 9: I ←I \ {µr(i)} 10: return (A1, A2,..., An)

Theorem 3. There exists a scale-invariant, PEF1 mechanism that always produces an EF1 allocation in polynomial time.

We will prove Theorem 3 by presenting Algorithm 2, which constructs a maximum-weight matching iteratively. This mechanism is similar to one proposed by Brustle et al. (2020) in the context of fair division with subsidy. Our mechanism is distinguished by its scale invariance and the tie-breaking method.

In the mechanism, we first give an arbitrary total order of the goods M. Let g1,..., gm be the goods aligned according to this order. We then ensure that m is divisible by n by adding dummy goods valued at zero by all agents if necessary. Initially, set Ai = ∅for every position i ∈[n], and let I be a set of all unallocated goods.

The core of the mechanism consists of m n rounds (the for loop of Lines 4-9). Let G = ([n] ∪M, E) denote a complete bipartite graph with two disjoint vertex sets [n] and M, where E = {{i, g} | i ∈[n], g ∈M}. In each round r, we consider the remaining subgraph Gr = ([n] ∪I, Er), where Er = {{i, g} | i ∈[n], g ∈I}.

The mechanism utilizes a weight function w: [n]×M → R≥0 on E defined by w(i, g) = 2m+1nw1(i, g) + w2(i, g) (1)

for each edge {i, g} ∈E. Here, two weight functions w1 and w2 are defined as follows.

The first weight function w1 is based on utilities. For each good g and the agent in each position i, we define rank R(i, g) as follows: R(i, g) = k if g has the kth highest utility among all goods in M for the agent in position i. If multiple goods have the same utility, they are assigned the same rank, and the next rank is assigned as if no ties occurred. For example, if four goods g1, g2, g3, g4 have utilities 10, 10, 8, and 7, respectively, then R(i, g1) = R(i, g2) = 1, R(i, g3) = 2, and R(i, g4) = 3. For each i ∈[n] and g ∈M, we define w1(i, g) = m −R(i, g).

The second weight function w2 is based on the total order of the goods: for each i ∈[n] and ℓ∈[m], we define w2(i, gℓ) = 2m−ℓ.

Additionally, recall the fundamental concept from matching theory. A subset of edges is a matching if no two edges in the subset share a common vertex. For a matching µ, let w(µ) denote the total weight of the matching with respect to w. Let µ(i) denote the good matched with i under µ.

In each rth round, the mechanism computes a maximumweight matching µr with respect to w in Gr (Line 5). While there may be multiple maximum-weight matchings, any such matching can be selected. Then, according to µ, goods are allocated to each position. As we will show in Lemma 4, maximizing w ensures that we first maximize w1, then w2 among matchings maximizing w1.

To illustrate the behavior of Algorithm 2, we apply it to the same instance from Table 1. Recall the profile with four agents and five goods with utilities satisfying x > y > z > 0. For this profile, the edge weights of the bipartite graph are given as in Table 2.

g1 g2 g3 g4 g5 Agent a1 264 260 514 769 Agent a2 528 516 514 769 Agent a3 520 772 514 513 Agent a4 272 516 770 257

**Table 2.** Edge weights for the bipartite graph in Algorithm 2.

For any agent ordering π, in the bipartite graph, there exists a unique maximum-weight matching {(π(a1), g1), (π(a2), g2), (π(a3), g3), (π(a4), g4)}. This means that regardless of which agent ordering is chosen, each agent receives the same good in round 1. In the second round, only good g5 remains unallocated. Here, the maximum-weight matchings between the remaining good and agents are {(π(a1), g5)} and {(π(a2), g5)}. The algorithm selects either maximum-weight matching. For instance, we can choose to prioritize the agent with the smaller position value under π. Although agent a1 experiences position envy between different orderings, this envy is bounded by at most one good, satisfying PEF1.

## 3.1 Proof of Theorem 3

The following lemma shows that a single weight function can achieve lexicographical maximization. Lemma 4. A maximum-weight matching of Gr with respect to w maximizes w1 first, and among all such matchings, maximizes w2.

Proof. Let µ and ν be any two matchings, and let wi(µ) and wi(ν) denote the total weights of µ and ν with respect to wi for i ∈{1, 2}. Since each matching contains at most n edges, and w2(e) ≤2m for all e ∈E, we have w2(µ) − w2(ν) ≥−2mn. If w1(µ) > w1(ν), then we get w1(µ) − w1(ν) ≥1 and w(µ) −w(ν)

17140

<!-- Page 5 -->

= 2m+1n(w1(µ) −w1(ν)) + (w2(µ) −w2(ν))

≥2m+1n −2mn > 0. This implies that a maximum-weight matching with respect to w must maximize w1. If w1(µ) = w1(ν) and w2(µ) > w2(ν), then w(µ) > w(ν). Thus, among matchings maximizing w1, a maximum-weight matching with respect to w must maximize w2.

For each agent ordering π ∈ Π and each r ∈ {1, 2,..., ⌈m n ⌉}, let µπ,r denote a maximum-weight matching in Gr with respect to w computed in rth round when the input is uπ. Let Γπ,r be the set of goods matched by µπ,r. For agent a ∈N, we denote by gπ,r,a the good matched with position π(a) under µπ,r. By the definition of w2, we can show that the set Γπ,r is determined independently of the agent ordering π. Lemma 5. For every round r ∈{1, 2,..., ⌈m n ⌉} and any pair of agent orderings π, π′ ∈Π, we have Γπ,r = Γπ′,r.

Proof. We prove the lemma by induction on r. Fix any ordering π and, for r = 1, suppose there exist two maximumweight matchings µπ,1 and µ′ π,1 with respect to w. By the definition of w, these matchings must have the same w2 weight sum. Since w2 uses powers of 2 based on the goods’ indices, this equality implies that µ and µ′ match the same set of goods. Thus, Γπ,1 is unique. Moreover, since w2 does not depend on positions, Γπ,1 is independent of π. The same argument applies inductively for each subsequent round r > 1, completing the proof.

Finally, we prove Theorem 3.

Proof of Theorem 3. Let M denote Algorithm 2. We first prove that M satisfies PEF1. To this end, we compare any pair of two agent orderings π, π′ ∈Π. By Lemma 5, Γπ,r = Γπ′,r for all r = 1, 2,..., ⌈m n ⌉. This implies that gπ,r+1,a /∈ Sr r′=1 Γπ,r′ = Sr r′=1 Γπ′,r′ for any r = 1, 2,..., ⌈m n ⌉−1 and any agent a ∈N. By Lemma 4, matching µπ′,r is a maximum-weight matching with respect to w1. Thus, for any agent a ∈N, we obtain w1(π(a), gπ,r+1,a) ≤ w1(π′(a), gπ′,r,a) since otherwise good gπ,r+1,a is included in the maximum-weight matching µπ′,r. By the definition of w1, this implies ua gπ,r+1,a

≤ua gπ′,r,a

. This leads that ua

M(uπ′)π′(a)

=

⌈m n ⌉ X r=1 ua gπ′,r,a

≥

⌈m n ⌉−1 X r=1 ua gπ′,r,a

≥

⌈m n ⌉ X r=2 ua gπ,r,a

= ua

M(uπ)π(a) \ {gπ,1,a}

, which implies that the mechanism is PEF1.

Next, we show that the mechanism always produces an EF1 allocation. Fix any agent ordering π. Since we choose a maximum-weight matching with respect to w1, we have ua gπ,r+1,a′

≤ua gπ,r,a for any two agents a, a′ ∈N and r = 1, 2,..., ⌈m n ⌉−1. Then, for all a, a′ ∈N, we have ua

M(uπ)π(a)

=

⌈m n ⌉ X r=1 ua gπ,r,a

≥

⌈m n ⌉−1 X r=1 ua gπ,r,a

≥

⌈m n ⌉ X r=2 ua gπ,r,a′

= ua

M(uπ)π(a′) \ {gπ,1,a′}

.

We finally consider the time complexity and scaleinvariance of the mechanism. In each round, we can find a maximum-weight matching with respect to w in polynomial time (Lov´asz and Plummer 2009). Thus, the mechanism runs in polynomial time. Furthermore, the weight function w is unchanged if the profile is multiplied by a tuple of positive reals. Therefore, the mechanism is scale-invariant.

## 4 The Case of Two Agents

In this section, we focus on the case of two agents.

## 4.1 Maximize Nash Welfare The

Nash welfare of an allocation A = {Aa}a∈N is defined as NW(A) =

Q a∈N ua(Aa)

1/n. An allocation A is said to be maximum Nash welfare (MNW) if it maximizes NW(A) among all allocations. Let U>0 be the class of profiles where ua: 2M →R>0 for all agents a ∈N.

We will show that PEF1 can be achieved by a mechanism that maximizes the Nash welfare for two agents. To this end, we first prove the following theorem. Theorem 6. When n = 2, for any u ∈U>0, any two MNW allocations A and B, and any agent a ∈N, if Ba̸ = ∅, then there exists g ∈Ba such that ua(Aa) ≥ua(Ba \ {g}).

Proof. Let N = {a1, a2} denote the set of two agents. Let A = {Aa1, Aa2} and B = {Ba1, Ba2} be two distinct MNW allocations.

We show that for agent a1, if Ba1̸ = ∅, there exists some good g ∈Ba1 such that ua1(Aa1) ≥ua1(Ba1 \g). The same argument can be applied to a2. Without loss of generality, we can assume that Ba1 \ Aa1̸ = ∅. Suppose, towards a contradiction, that ua1(Aa1) < ua1(Ba1\{g}) for every g ∈ Ba1 \ Aa1. Take a good h ∈Ba1 \ Aa1 (note that h ∈Aa2). Consider allocations A′ and B′ where A′ a1 = Aa1 ∪{h}, A′ a2 = Aa2 \{h}, B′ a1 = Ba1 \{h}, and B′ a2 = Ba2 ∪{h}. We will show that NW(A′)NW(B′) > NW(A)NW(B), contradicting the optimality of A and B. Observe that

NW(A′)2

NW(A)2 · NW(B′)2

NW(B)2

= ua1(A′ a1) ua1(Aa1) · ua2(A′ a2) ua2(Aa2) · ua1(B′ a1) ua1(Ba1) · ua2(B′ a2) ua2(Ba2)

=

1 + ua1(h)(ua1(Ba1) −ua1(Aa1) −ua1(h)) ua1(Aa1)ua1(Ba1)

·

1 + ua2(h)(ua2(Aa2) −ua2(Ba2) −ua2(h)) ua2(Aa2)ua2(Ba2)

.

By our assumption, ua1(Aa1) < ua1(Ba1 \ {h}). This implies that the first term in the product on the right-hand side is strictly greater than 1.

Since A is MNW, NW(A) ≥ NW(B′), implying ua1(Aa1)ua2(Aa2) ≥ua1(Ba1 \ {h})ua2(Ba2 ∪{h}). Combined with ua1(Aa1) < ua1(Ba1 \ {h}), we obtain ua2(Aa2) ≥ ua2(Ba2 ∪{h}). Thus, the second

17141

<!-- Page 6 -->

## Algorithm

3: Adjusted Winner Mechanism

Input: Ordered profile (u1, u2) Output: Ordered allocation (A1, A2)

1: Fix total order of the goods. 2: Normalize utilities. 3: Let A1 = {g ∈M | u1(g) ≥0 ∧u2(g) = 0} and A2 = {g ∈M | u1(g) = 0 ∧u2(g) > 0}. 4: Let M + = {g ∈M | u1(g) > 0 ∧u2(g) > 0}. 5: if M +̸ = ∅then 6: Arrange the goods in M + in non-increasing order based on their utility ratios: u1(g1)

u2(g1) ≥· · · ≥u1(gℓ)

u2(gℓ).

7: Find P1 = {g1,..., gk−1}, P2 = {gk+1,..., gℓ} and gk with λ1 and λ2 (where λ1 + λ2 = 1 and λ1, λ2 ≥ 0) such that 1 u1(M +) (u1(P1) + λ1u1(gk)) =

1 u2(M +) (u2(P2) + λ2u2(gk)). 8: if λ1 ≥λ2 then 9: A1 ←A1 ∪P1 ∪{gk} and A2 ←A2 ∪P2 10: else 11: A1 ←A1 ∪P1 and A2 ←A2 ∪P2 ∪{gk} 12: return (A1, A2)

term is at least 1. This yields NW(A′)2NW(B′)2 > NW(A)2NW(B)2, a contradiction.

Consider a mechanism that returns an MNW allocation, breaking ties according to agents’ positions. This mechanism is scale-invariant by the definition of Nash welfare. Furthermore, the resulting allocation satisfies EF1 and PO (Caragiannis et al. 2019). By Theorem 6, we obtain the following theorem.

Theorem 7. When n = 2, any mechanism that returns an MNW allocation is scale-invariant and satisfies PEF1 with respect to U>0. Moreover, such allocations are EF1 and PO.

## 4.2 Adjusted Winner Mechanism

For two agents, we prove the existence of a scale-invariant and PEF1 mechanism that always produces EF1 and PO in polynomial time by considering the adjusted winner mechanism (Brams and Taylor 1996; Aziz et al. 2015, 2022a).

Theorem 8. When n = 2, there exists a scale-invariant, PEF1 mechanism that always returns an EF1 and PO allocation in polynomial time.

See Algorithm 3. The mechanism first fixes a total order of goods and partitions the goods into three sets: A1 containing goods valued only by position 1, A2 containing goods valued only by position 2, and M + containing goods positively valued by both agents. We then arrange goods in M + in non-increasing order of utility ratios u1(g)

u2(g), breaking ties by the indices of goods. We denote the sequence by g1, g2,..., gℓwhere ℓ= |M +|.

We consider dividing fractionally these ordered goods using a boundary line: goods to the left of the boundary are allocated to agent in position 1, and goods to the right are allocated to agent in position 2. Formally, as we move a boundary from left to right, there exists a unique k ∈[ℓ] and parameters λ1, λ2 where allocating bundle P1 = {g1, g2,..., gk−1} to agent in position 1, bundle P2 = {gk+1, gk+2,..., gℓ} to agent in position 2, and splitting good gk in proportions λ1, λ2 gives equal utility to both agents. Specifically, 1 u1(S) (u1(P1) + λ1u1(gk)) =

1 u2(S) (u2(P2) + λ2u2(gk)). Based on the comparison of λ1 and λ2, we allocate the boundary good gk entirely to one of the agents (see Lines 8 and 10 in Algorithm 3).

From Section 3 of (Aziz et al. 2015), we have the following lemma.

Lemma 9 (Aziz et al. (2015)). For every pair of positions i, j ∈{1, 2}, ui(Pi)+λiui(gk) ≥ui(Pj)+λjui(gk). Moreover, no partition of M + between the two agents can make one agent better off without making the other agent worse off compared to either (P1 ∪{gk}, P2) or (P1, P2 ∪{gk}).

Using this lemma, we prove Theorem 8.

Proof of Theorem 8. Let N = {a1, a2} be the set of two agents. For each a ∈N, let Ma = {g ∈M | ua(g) > 0 ∧ua′(g) = 0} be the set of goods valued only by agent a where a′ denotes the other agent, and let M0 = {g ∈M | ua1(g) = ua2(g) = 0}.

We first prove that the mechanism is PEF1. The boundary line and the proportions λ1, λ2 are determined solely by the utility ratios, independently of agent orderings. Bundles P1 and P2 are determined by the boundary line, which is independent of positions. For any agent a ∈N and agent orderings π and π′, we denote by Pa the fixed set Pπ(a) = Pπ′(a) of goods in M +. Under ordering π, agent a in position π(a) receives either Ma ∪Pa, Ma ∪M0 ∪Pa, Ma ∪Pa ∪{gk}, or Ma ∪M0 ∪Pa ∪{gk}. Since ua(M0) = 0, agent a’s utility equals either ua(Ma ∪Pa) or ua(Ma ∪Pa ∪{gk}), establishing PEF1.

We now show that the mechanism always returns an EF1 allocation. Fix an agent ordering π. Without loss of generality, we assume that π(a1) = 1 and π(a2) = 2. When λ1 ≥λ2, we have ua1(M(uπ)π(a1)) = ua1(Ma1 ∪Pa1) + ua1(gk)

≥ua1(Ma2 ∪Pa2) + λ2ua1(gk) + (1 −λ1)ua1(gk) ≥ua1(Ma2 ∪Pa2) = ua1(M(uπ)π(a2)), where we use Lemma 9 for the first inequality, and ua2(M(uπ)π(a2)) = ua2(Ma2 ∪Pa2)

≥ua2(Ma1 ∪Pa1) + λ1ua2(gk) −λ2ua2(gk) ≥ua2(Ma1 ∪Pa1) = ua2(M(uπ)π(a1) \ {gk}), where we use Lemma 9 for the first inequality, and λ1 ≥λ2 for the second inequality. When λ1 < λ2, the resulting allocation can be proven to be EF1 by an analogous argument to the case of λ1 ≥λ2.

Next, we prove that the mechanism produces Pareto optimal allocations. Let {Aa1, Aa2} be the allocation induced from the ordered allocation produced by the mechanism. By Lemma 9, since goods in Ma are valued only by agent a for each a ∈N, and goods in M0 are valued by neither agent, any allocation that differs from {Aa1, Aa2} would

17142

<!-- Page 7 -->

make at least one agent worse off. Finally, the mechanism clearly runs in polynomial time, and its scale-invariance follows from the normalization step.

## 5 Further Analysis for Round-Robin

Mechanism We now investigate the round-robin mechanism (recall Algorithm 1). We refer to each iteration of the while loop in Algorithm 1 as a round, in which agents select their most preferred good from the remaining goods according to a fixed agent ordering. As mentioned in Section 2, for the roundrobin mechanism, more goods need to be removed to eliminate position-based envy as n increases.

Theorem 10. When ⌈m/n⌉≥⌊log2 n⌋, for the round-robin mechanism, there exists a profile and two agent orderings π, π′ where even after removing any ⌊log2 n⌋−1 goods from their bundle under π, an agent prefers keeping their remaining bundle to receiving their bundle under π′.

We prove the theorem by constructing a specific profile. The detailed proof is deferred to the full version of our paper (Mahara et al. 2025).

Proof Sketch. Consider two agent orderings π, π′ ∈Π such that π(ai) = i and π′(ai) = n + 1 −i for each i ∈[n]. The key idea is to construct utilities where agent a1’s first ⌊log2 n⌋choices under π have significantly higher value (value C) than the remaining choices, while carefully setting the utilities of other agents to ensure that under π′, agent a1 cannot obtain any of these highly valued goods. This construction ensures that even after removing any ⌊log2 n⌋−1 goods from agent a1’s bundle under π, at least one good of value C remains, making this bundle more valuable than their bundle under π′.

Theorem 10 shows that the round-robin mechanism is not PEF1 when n ≥4 and m ≥n + 1. When m ≤n, each agent receives at most one good, ensuring PEF1. Moreover, we prove that the round-robin mechanism is PEF1 for two or three agents. We defer the proof to the full version of our paper (Mahara et al. 2025).

Theorem 11. When n ∈{2, 3}, the round-robin mechanism is PEF1.

## 6 Envy-Cycle Mechanism

Next, we study the envy-cycle mechanism, which always produces an EF1 allocation when agents have monotone utility functions (Lipton et al. 2004). We say that ua is monotone if ua(S) ≤ua(T) for any S ⊆T ⊆M. We will show the mechanism may not satisfy PEF1. All proofs are presented in the full version (Mahara et al. 2025).

To describe the mechanism, we define several concepts. We say that P = (P1, P2,..., Pn) is an ordered partial allocation if S i∈[n] Pi ⊆M and Pi ∩Pi′ = ∅for all i̸ = i′ ∈[n]. For an ordered profile u and a partial allocation P = (P1, P2,..., Pn), envy graph is defined as a directed graph GP = ([n], E), where the vertex set is [n] and the edge set is E = {(i, i′) | i, i′ ∈[n], i̸ = i′, ui(Pi) <

## Algorithm

4: Envy-Cycle Mechanism

Input: Ordered profile (u1, u2,..., un) Output: Ordered allocation (A1, A2,..., An)

1: Fix indices of goods as M = {g1, g2,..., gm}. 2: Set Ai ←∅for all i ∈[n]. 3: for j = 1, 2,..., m do 4: For partial allocation A = {Ai}i∈[n], construct the envy graph GA. 5: while there exists an envy cycle in GA do 6: Resolve the envy cycle by transferring bundles in the opposite direction of the cycle. 7: Let i ∈[n] be the vertex of in-degree 0 in GA with the smallest index. 8: Set Ai ←Ai ∪{gj}. 9: return (A1, A2,..., An)

ui(Pi′)}. An envy cycle is a directed cycle in the envy graph, that is, a sequence of positions (i1, i2,..., iℓ) such that (ik, ik+1) ∈E for all k ∈[ℓ], where iℓ+1 = i1.

In the envy-cycle mechanism (Algorithm 4), we first order the goods arbitrarily. For each good, we first eliminate all envy cycles in the partial allocation and then allocate it to an unenvied position. Specifically, while there exists an envy cycle in the current allocation, we resolve it by transferring bundles in the opposite direction of the cycle. After eliminating all cycles, we allocate the current good to a position not envied by any other. If multiple such positions exist, we choose the one with the smallest index.

Similar to the round-robin mechanism, the envy-cycle mechanism does not satisfy PEF1 in general. Theorem 12. When n ≥2, for the envy-cycle mechanism, there exists a profile and two agent orderings π, π′ where even after removing any m − m n

−1 goods from their bundle under π, an agent prefers keeping their remaining bundle to receiving their bundle under π′.

Theorem 12 implies that if the envy-cycle mechanism is PEF1, then m − m n

≤1. Moreover, we establish that this condition is also sufficient for PEF1. Theorem 13. The envy-cycle mechanism is PEF1 if m − m n

≤1.

## Discussion

This paper introduces a new fairness notion, PEF1, for mechanisms. We demonstrate a PEF1 mechanism producing an EF1 allocation for agents with additive utilities. For the case of two agents, we prove the existence of a scaleinvariant, PEF1 mechanism that outputs an EF1 and PO allocation.

Several questions remain open for future research. While we have shown in Theorem 6 that for n = 2, the utility difference between any pair of MNW allocations is bounded by some good’s utility for each agent, the result for n > 2 remains unknown. We conjecture this bound holds for any n. Additionally, the existence of a PEF1 mechanism producing an EF1 and PO allocation for any n remains an open question.

17143

<!-- Page 8 -->

## Acknowledgments

This work was partially supported by JST ERATO Grant Number JPMJER2301. Ryoga Mahara acknowledges additional support from JSPS KAKENHI Grant Number JP23K19956. Ryuhei Mizutani acknowledges additional support from JSPS KAKENHI Grant Number JP23KJ0379 and JST SPRING Grant Number JPMJSP2108. Taihei Oki acknowledges additional support from JST FOREST Grant Number JPMJFR232L. We thank the anonymous AAAI 2026 reviewers for their valuable feedback.

## References

Amanatidis, G.; Aziz, H.; Birmpas, G.; Filos-Ratsikas, A.; Li, B.; Moulin, H.; Voudouris, A. A.; and Wu, X. 2023. Fair division of indivisible goods: Recent progress and open questions. Artificial Intelligence, 322: 103965. Aziz, H.; Brˆanzei, S.; Filos-Ratsikas, A.; Kristoffer, S.; and Frederiksen, S. 2015. The adjusted winner procedure: Characterizations and equilibria. In Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJ- CAI), 454–460. Aziz, H.; Caragiannis, I.; Igarashi, A.; and Walsh, T. 2022a. Fair allocation of indivisible goods and chores. Autonomous Agents and Multi-Agent Systems, 36: 1–21. Aziz, H.; Li, B.; Moulin, H.; and Wu, X. 2022b. Algorithmic fair allocation of indivisible items: A survey and new questions. ACM SIGecom Exchanges, 20(1): 24–40. Bei, X.; Huzhang, G.; and Suksompong, W. 2020. Truthful fair division without free disposal. Social Choice and Welfare, 55: 523–545. Bogomolnaia, A.; and Moulin, H. 2001. A new solution to the random assignment problem. Journal of Economic Theory, 100(2): 295–328. Brams, S. J.; and Taylor, A. D. 1996. Fair Division: From Cake-Cutting to Dispute Resolution. Cambridge University Press. Brustle, J.; Dippel, J.; Narayan, V. V.; Suzuki, M.; and Vetta, A. 2020. One dollar each eliminates envy. In Proceedings of the 21st ACM Conference on Economics and Computation (EC), 23–39. Budish, E. 2011. The combinatorial assignment problem: Approximate competitive equilibrium from equal incomes. Journal of Political Economy, 119(4): 1061–1103. Budish, E.; Cachon, G. P.; Kessler, J. B.; and Othman, A. 2016. Course match: A large-scale implementation of approximate competitive equilibrium from equal incomes for combinatorial allocation. Operations Research, 65(2): 314– 336. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The unreasonable fairness of maximum Nash welfare. ACM Transactions on Economics and Computation, 7(3): 1–12. Dubins, L. E.; and Spanier, E. H. 1961. How to cut a cake fairly. The American Mathematical Monthly, 68(1): 1–17. Foley, D. K. 1967. Resource allocation and the public sector. Yale Economic Essays, 7: 45–98.

Gibbard, A. 1973. Manipulation of voting schemes: A general result. Econometrica, 41(4): 587–601. Goldman, J.; and Procaccia, A. D. 2015. Spliddit: Unleashing fair division algorithms. ACM SIGecomm Exchanges, 13(2): 41–46. Han, J.; and Suksompong, W. 2024. Fast & fair: A collaborative platform for fair division applications. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), 23796–23798. Igarashi, A.; and Yokoyama, T. 2023. Kajibuntan: A house chore division app. In Proceedings of the 37th AAAI Conference on Artificial Intelligence (AAAI), 16449–16451. Lee, E. 2017. APX-hardness of maximizing Nash social welfare with indivisible items. Information Processing Letters, 122: 17–20. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In Proceedings of the 5th ACM Conference on Electronic Commerce (EC), 125–131. Lov´asz, L.; and Plummer, M. D. 2009. Matching Theory. American Mathematical Society. Mahara, R.; Mizutani, R.; Oki, T.; and Yokoyama, T. 2025. Position fair mechanisms allocating indivisible goods. CoRR, abs/2409.06423. Manabe, Y.; and Okamoto, T. 2012. Meta-envy-free cakecutting and pie-cutting protocols. Journal of Information Processing, 20(3): 686–693. Moulin, H. 2004. Fair Division and Collective Welfare. MIT press. Nguyen, N.-T.; Nguyen, T. T.; Roos, M.; and Rothe, J. 2014. Computational complexity and approximability of social welfare optimization in multiagent resource allocation. Autonomous Agents and Multi-Agent Systems, 28(2): 256– 289. Roth, A. E.; S¨onmez, T.; and ¨Unver, M. U. 2005. Pairwise kidney exchange. Journal of Economic Theory, 125(2): 151–188. Satterthwaite, M. A. 1975. Strategy-proofness and Arrow’s conditions: Existence and correspondence theorems for voting procedures and social welfare functions. Journal of Economic Theory, 10(2): 187–217. Segal-Halevi, E.; and Sziklai, B. R. 2019. Monotonicity and competitive equilibrium in cake-cutting. Economic Theory, 68(2): 363–401. Shapley, L.; and Scarf, H. 1974. On cores and indivisibility. Journal of Mathematical Economics, 1(1): 23–37. S¨onmez, T. 1999. Strategy-proofness and essentially singlevalued cores. Econometrica, 67(3): 677–689. Walsh, T. 2020. Fair division: The computer scientist’s perspective. In Proceedings of the 29th International Joint Conference on Artificial Intelligence (IJCAI), 4966–4972. Zhou, L. 1990. On a conjecture by Gale about one-sided matching problems. Journal of Economic Theory, 52(1): 123–135.

17144
