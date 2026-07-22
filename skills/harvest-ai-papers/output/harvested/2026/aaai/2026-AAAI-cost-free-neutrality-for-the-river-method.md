---
title: "Cost-Free Neutrality for the River Method"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38728
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38728/42690
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Cost-Free Neutrality for the River Method

<!-- Page 1 -->

Cost-Free Neutrality for the River Method

Michelle D¨oring1, Jannes Malanowski1, Stefan Neubert1

## 1 Hasso Plattner Institute, University of Potsdam,

Germany michelle.doering@hpi.de, jannes.malanowski@student.hpi.de, stefan.neubert@hpi.de

## Abstract

Recently, the River Method was introduced as novel refinement of the Split Cycle voting rule. The decision-making process of River is closely related to the well established Ranked Pairs Method. Both methods consider a margin graph computed from the voters’ preferences and eliminate majority cycles in that graph to choose a winner. As ties can occur in the margin graph, a tiebreaker is required along with the preferences. While such a tiebreaker makes the computation efficient, it compromises the fundamental property of neutrality: the voting rule should not favor alternatives in advance. One way to reintroduce neutrality is to use Parallel-Universe Tiebreaking (PUT), where each alternative is a winner if it wins according to any possible tiebreaker. Unfortunately, computing the winners selected by Ranked Pairs with PUT is NP-complete. Given the similarity of River to Ranked Pairs, one might expect River to suffer from the same complexity. Surprisingly, we show the opposite: We present a polynomialtime algorithm for computing River winners with PUT, highlighting significant structural advantages of River over Ranked Pairs. Our Fused-Universe (FUN) algorithm simulates River for every possible tiebreaking in one pass. From the resulting FUN diagram one can then directly read off both the set of winners and, for each winner, a certificate that explains how this alternative dominates the others.

## Introduction

and Related Work

A common interest in theoretical computer science, economics, and political science is the design and analysis of social choice functions-mechanisms that aggregate individual preferences to make a collective decision. Clearly, such decision-making is an integral part of democratic processes. Beyond political contexts, social choice functions have become increasingly relevant in artificial intelligence, particularly for aligning AI systems with diverse human preferences (F¨urnkranz and H¨ullermeier 2003; K¨opf et al. 2024). As language models and other AI systems interact with feedback from a wide range of users, aggregating that feedback ‘socially acceptably’ becomes a key challenge. Recent work argues that social choice theory should guide AI alignment in addressing this diversity (Conitzer et al. 2024).

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

There is extensive research on properties of social choice functions, their trade-offs, and the often high complexity of computing them (see (Brandt et al. 2016) for an overview).

A core task of computational social choice is to design rules that satisfy reasonable fairness criteria while also being computationally tractable. In this work, we show how to efficiently compute the winners of the recently suggested River Method (D¨oring, Brill, and Heitzig 2025).

River is part of a family of margin-based social choice functions – methods that decide an election based on pairwise comparisons between alternatives and the margin of victory in each such comparison. A common approach to social choice is to select an alternative that wins all pairwise comparisons; the so-called Condorcet winner. However, there are cases where there is no such alternative. Margin-based rules resolve this by not just considering who wins in a pairwise comparison, but also by how much.

The margin of x over y is the difference between the number of voters who prefer x over y and those who prefer y over x. This information is represented as a margin graph – a complete, weighted, antisymmetric, directed graph over the set of alternatives, where each edge (x, y) is weighted by the margin between x and y (Brandt et al. 2016). If there is no Condorcet winner, the margin graph contains cycles of pairwise victories, such as alternatives x, y, z where x wins against y, which wins against z, which wins against x.

One way of resolving such cycles is to focus on the notion of immunity to majority complaints: an alternative x is immune if for every alternative z that beats x in direct comparison, there exists a path of at least as strong pairwise victories leading from x to z. This path does not only serve to define a winner, but also to defend the choice of x against claims such as “a majority prefers z over x, thus x should not win”.

In every election exists at least one immune alternative (Holliday and Pacuit 2023). Several voting rules are designed to select those alternatives, each fulfilling different fairness axioms. Split Cycle (Holliday and Pacuit 2023) selects all immune alternatives by removing the weakest link in each majority cycle, making all other immune-based functions refinements of it. However, this typically results in multiple winners. To guarantee a unique winner, Ranked Pairs (Tideman 1987) incrementally locks in pairwise victories in order of decreasing margin, as long as doing so does not create a cycle. It satisfies numerous desirable

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16838

<!-- Page 2 -->

axioms like monotonicity and clone independence. River (D¨oring, Brill, and Heitzig 2025) extends this process by additionally rejecting edges which would lead to two incoming edges, yielding a tree structure that satisfies Independence of Pareto-Dominated Alternatives, a strong resistance to agenda manipulation not shared by other known refinements. For formal definitions, axiomatic analyses, and further immune-based voting rules, see (Holliday and Pacuit 2023; D¨oring, Brill, and Heitzig 2025). Ranked Pairs and River both process edges by decreasing margin and require a total order to break ties between equally strong edges. However, such tiebreakers typically violate neutrality: no alternative should be favored a priori. See (Brill and Fischer 2012; Freeman, Brill, and Conitzer 2015; Wang et al. 2019; Zavist and Tideman 1989) for a discussion of tiebreaking rules and their implications. To restore neutrality, one can apply Parallel-Universe Tiebreaking (PUT), which considers all possible tiebreaking orders and returns the union of winners. However, deciding whether a given alternative is a PUT winner under Ranked Pairs is known to be NP-complete (Brill and Fischer 2012).

## 1.1 Our Contribution We study the computational complexity of applying Parallel-Universe Tiebreaking (PUT) to

River. Although River closely resembles Ranked Pairs, we show that the winners under PUT can be computed in polynomial time.

For this, we exploit the more restricted rule set of River: like Ranked Pairs, it processes the edges of the margin graph in order of decreasing margin and discards those that would create a cycle; River additionally enforces that each alternative has at most one incoming edge. As a result, River always produces a directed tree rooted at the winner, whereas Ranked Pairs only guarantees to return an acyclic subgraph.

This difference enables us to simultaneously simulate River for all possible tiebreakers in one pass. Our Fused- Universe (FUN) algorithm to determine all PUT winners for River can be summarized as follows: 1. Compute the Fused-Universe diagram: a subgraph of the margin graph, which includes all margin edges that appear in the River diagram of at least one universe. 2. During that same process, track and update for each alternative whether it remains undefeated in all universes, is defeated in some, or is defeated in all universes. 3. Derive the set of winners from these vertex states. After formally defining River in Section 2, we describe our algorithm in detail in Section 3, where we also explain how it can be computed in polynomial time. In Section 4 we prove that the algorithm correctly determines the set of RV-PUT winners. We first show that every alternative not selected by our algorithm is defeated in every universe. For the other direction, we construct, for each selected winner, a tiebreaker under which it wins in River. This tiebreaker not only proves correctness but also serves as a constructive certificate that the alternative is immune. We conclude in Section 6 with open questions and suggestions for future work on River and Parallel-Universe Tiebreaking.

Proofs of statements marked with ⋆are in the full version.

## Preliminaries

We consider n ≥1 voters expressing preferences over a set A of alternatives. The preferences of each voter i are represented by a linear order ≻i over A, and the (preference) profile P = (≻1,..., ≻n) collects these preferences for all voters. Let [n] = {1,..., n}. The margin of alternative x over y according to P is mP(x, y) = |{ i ∈[n] | x ≻i y }|− |{ i ∈[n] | y ≻i x }|. The margin graph M(P) of P is a weighted directed graph with vertex set A and edge set { (x, y) ∈A × A | mP(x, y) ≥0 }, where each edge (x, y) is assigned weight mP(x, y) ≥0. In any graph with vertex set A, we say that vertex y is dominated by the edge (x, y) or by vertex x, if y has an incoming edge from x. We omit the preference profile P when it is clear from the context.

A (majority) path from x to y in M is a sequence Pxy = (x = p1,..., pℓ= y) of distinct alternatives such that m(pi, pi+1) > 0 for all i ∈[ℓ−1]. The strength of such a path is the value of its lowest margin, i. e., strength(Pxy) = min{ m(pi, pi+1) | i ∈[ℓ−1] }. Analogously, majority cycles in M are closed paths (xℓ= x1) such that m(xi, xi+1) > 0 for all consecutive pairs, and their strength is defined as the lowest margin on the cycle.

Winners and Ties A Condorcet winner x is an alternative for which m(x, y) > 0 for all y ∈A \ {x}. In the absence of a Condorcet winner, every alternative faces at least one majority defeat. Some alternatives can be justified as winners despite these defeats by the existence of equally strong majority paths leading from the alternative to each alternative defeating it. This is called immunity (Holliday and Pacuit 2023): An alternative x is immune (against majority complaints) if, for every alternative y with m(y, x) > 0, there is a majority path Pxy with strength(Pxy) ≥m(y, x).

A social choice function maps a preference profile to a non-empty set of winning alternatives. For margin graphs where at least two edges have the same margin, Stable Voting, Ranked Pairs, and River require a tiebreaker to compute their winning set. A tiebreaker is a descending linear ordering τ = (e1,..., e|E|) of the margin edges E by decreasing margin, i. e., m(ei) ≥m(ej) for all 1 ≤i < j ≤|E| (Zavist and Tideman 1989; Brill and Fischer 2012). We refer to the set of all descending linear orderings by L.

The River Method River (D¨oring, Brill, and Heitzig 2025) is a social choice function which eliminates majority cycles in the margin graph by greedily constructing a subtree of M based on a fixed tiebreaker. Formally, given a preference profile P and a tiebreaker τ ∈L, let M = (A, E) denote the corresponding margin graph. River constructs the River diagram MRV(P, τ), and selects a unique winner RV(P, τ) as follows: 1. Initialize MRV(P, τ) as (A, ∅). 2. Iterate over the edges in order of τ and add (x, y) to the diagram unless it is rejected by one of two conditions: branching condition: y already has an incoming edge; cycle condition: adding the edge would create a cycle. 3. Return the unique alternative without incoming edges in MRV(P, τ) as winner RV(P, τ).

16839

<!-- Page 3 -->

Parallel-Universe Tiebreaking Instead of fixing one tiebreaker, Parallel-Universe Tiebreaking (PUT) selects every winner according to any possible tiebreaker. Formally,

RV-PUT(P) =

[ τ∈L

RV(P, τ).

Fusing Parallel Universes The FUN algorithm efficiently simulates the River procedure across all universes simultaneously by exploiting River’s unique branching condition: each alternative has at most one incoming edge in any River diagram. This structure enables reasoning about which edges are added or rejected across all possible tiebreakers.

Consider Figure 1. The edges (x, y), (z, y), and (d, y), with margin 10, are processed first by River. Depending on the tiebreaker, one is added, while the other is rejected by the branching condition. As a result, any edge to y with margin lower than 10 is rejected by the branching condition regardless of the tiebreaker. This allows us to reason about potential winners: once all margin-10 edges are processed, it is already certain that y cannot be a River winner in any universe. Indeed, one of (x, y), (z, y), or (d, y) will appear in every River diagram, thereby dominating y. Consequently, y cannot be an RV-PUT winner.

The FUN algorithm. Our algorithm to compute the RV-PUT winners has two main steps.

In the first step, it computes the Fused-Universe (FUN) diagram. The algorithm takes as input the margin graph and processes its edges in order of decreasing margin; edges with the same margin are considered in arbitrary order. For each edge (x, y) with margin k the algorithm checks whether the edge is clearly rejected from every possible universe because of River’s branching or cycle condition. If the algorithm has decided that (x, y) cannot be clearly rejected from every universe, it adds the edge to the FUN diagram and proceeds to compute the conditions under which this edge may appear in some universe. These conditions are represented by four possible edge states: fix, branching choice, cycle choice, or cycle-branching choice. Each alternative – represented in the diagram as a vertex – also receives a vertex state: not dominated, fixedly dominated, or cycle dominated.

In the second step, the FUN algorithm returns the set of winning alternatives, which is the set of vertices which are not dominated or cycle dominated in the FUN diagram.

We introduce the edge and vertex states in Section 3.1, followed by a detailed description of their computation in Section 3.2. Afterwards, we explain in Section 3.3 how the algorithm can be implemented to run in polynomial time.

## 3.1 Edge and Vertex States Edge States With a fixed tiebreaker, River either rejects or adds an edge to the

River diagram. Our algorithm is more nuanced about the edge states, as it considers simultaneously whether edges are rejected or added in any possible universe. An edge in the FUN diagram receives one of four edge states. Their interpretations, implications, and abbreviations are summarized in Table 1 and illustrated in Figure 1. Let (x, y) with margin k be the current edge.

y c

4

6 10 4

10

8 2

M: MFUN: 6

2

Margin Graph y c

BC

BC

CC

CBC

Fix

FUN diagram

4

6

10

8 10 10 x d z x d z not dom. fix dom.

fix dom. fix dom.

fix dom.

6

Fix

10

BC

**Figure 1.** Election with margin graph M, FUN diagram MFUN with edge/vertex states and RV-PUT winner x.

A fix edge appears in every universe. An edge is marked Fix if we are certain no other incoming edge to y has margin ≥k, and no path from y to x has strength ≥k. A simple example is a unique edge with maximum margin: since it is processed first, neither River’s branching nor cycle condition reject it and the edge is added to every River diagram.

A branching choice edge may appear in some universe but cannot appear in all. That is because there exists at least one other incoming “partner” edge (z, y) with margin k which also could be added. Which of the two edges is added to the River diagram depends on the order in the tiebreaker τ: if (x, y) is before (z, y) in τ, then (x, y) is added and (z, y) must be rejected by the branching condition. Vice versa, if (z, y) is before (x, y) in τ, then (z, y) is added and (x, y) rejected. Both edges are marked as a branching choice BC.

A cycle choice edge may appear in some but not all universes. Assume there is a path from d to c containing at least one BC edge (d, y), and let (z, y) be the partner BC (not on the path). If the tiebreaker puts (z, y) first, (d, y) is rejected by the branching condition, so adding (c, d) does not close a cycle and it is added. If (d, y) comes first instead, (c, d) would close a cycle and is rejected by the cycle condition. A simpler example would be a directed cycle (a, b, c) of equalmargin edges: depending on the tiebreaker, two edges are added and the third is rejected by the cycle condition.

A cycle branching choice edge is a branching choice that depends on the cycle choice of another edge. Assume (c, d) is a cycle choice edge because there is a path from d to c that includes a branching choice edge (d, y) with partner (z, y) (not on the path). In this case, whether (x, d) is added depends on how the cycle is resolved: if (z, y) is processed first and added, then (d, y) is rejected, (c, d) does not close a cycle and is added, and (x, d) is rejected by the branching condition. If instead (d, y) is processed and added first, then (c, d) is rejected by the cycle condition, and (x, d) is added.

Vertex States With a fixed tiebreaker, River selects a unique winner – the alternative with no incoming edge in the resulting River diagram. Our algorithm generalizes this by assigning vertex states during execution, capturing which alternatives can or cannot be winners across all universes.

These vertex states reflect what is known about a vertex y’s incoming edges in MFUN. Edges labeled Fix, BC, or CBC with margin k indicate that y is dominated by an edge

16840

<!-- Page 4 -->

short edge state interpretation implication

Fix fix added in every universe in every universe, y is dominated by (x, y) BC branching choice added in some but not all universes; there is (z, y) with m(z, y) = k which could be added instead in every universe, y is dominated by an edge with margin k CC cycle choice may be added in some but not all universes; there exists an y-x-path which could be added instead there is a universe where y is not dominated by (x, y) CBC cycle branching choice added in some but not all universes; there exists (z, y) with m(z, y) > k which is CC in every universe, y is dominated by an edge with margin at least k

**Table 1.** Overview of the possible edge states assigned to an edge (x, y) with margin k = m(x, y).

vertex state property in MFUN not dominated no incoming edge fixedly dominated either exactly one incoming edge with state Fix, or at least one incoming edge with state BC or CBC cycle dominated at least one incoming edge and all incoming edges have state CC

**Table 2.** Overview of the possible vertex states.

of margin ≥k in every universe. In contrast, CC edges do not guarantee such domination, as they may be rejected depending on the cycle structure and tiebreaker. This distinction allows us to assign each vertex one of three possible states, as summarized in Table 2 and illustrated in Figure 1.

## 3.2 Computing the Fused-Universe Diagram

Let us now go into the details on how to compute the introduced edge and vertex states for the FUN diagram. Given a margin graph M, the algorithm processes the edges in descending order of their margin, breaking ties arbitrarily. Algorithm 1 shows how each edge (x, y) with margin m(x, y) = k is then processed in two phases:

## 1 Rejection in Every

Universe (lines 4 to 8). The algorithm first decides whether the edge (x, y) must be rejected from MFUN in every tiebreaker universe. This decision is based on River’s branching and cycle conditions:

• Branching rejection: If vertex y is fixedly dominated by some edge with margin > k, then (x, y) is rejected by River’s branching condition in every universe. • Cycle rejection: If adding (x, y) forms a cycle with a path of strength > k in every universe, then in each of these universes the edge is rejected by River’s cycle condition. This is checked by the algorithm in lines 5 – 8. The condition in line 5 can be computed with a breadthfirst search (BFS) started on y that only considers edges with margin > k. Similarly, the set U in line 6 can be computed with a reverse BFS started on x that only considers edges with margin > k. To check the condition in line 7, we do the following. For every CC edge (c, d) in MFUN, run a BFS started on d that only considers edges with margin ≥m(c, d) that are not incident to y. Let E′ be the set of such edges (c, d) where this BFS reaches c – meaning there is a path from d to c in MFUN of strength ≥m(c, d) that does not include vertex y. Now the condition in line 7 can be tested by comparing U with the vertices reached by a BFS started on y that only considers edges in E \ E′ with margin > k.

## 2 Assigning the Edge

State (lines 9 to 19). If the edge is not rejected in Step 1, the algorithm will add the edge to MFUN and determine its state. A first preliminary state is derived from the current state of the target vertex y, without yet accounting for possible cycles in MFUN – resulting in one of the states Fix, BC, or CBC (lines 9 – 14). Later, the algorithm checks whether (x, y) is contained in cycles in MFUN to determine whether it (and possibly other edges of margin k) must be updated to CC (lines 16 – 19).

Note that the state of an edge is tentative until all edges of the same margin are processed. Only then it is clear which cycles this edge is contained in. For this, in lines 16 – 19, the algorithm performs the cycle update check: it updates the edges in cycles that are closed by (x, y) in MFUN. To compute C in 16, the algorithm performs two BFS in MFUN: A forward BFS from y to find all vertices Y reachable from y and a reverse BFS from x to find all vertices X reaching x. Now C is the set of edges (u, v) with u in Y and v in X.

## 3.3 Computing the RV-PUT Winners in Polynomial Time After computing the

Fused-Universe diagram MFUN, our algorithm returns the set of vertices that are cycle dominated or not dominated in MFUN as RV-PUT winners. These two steps run in polynomial time in the size of the margin graph. Theorem 3.1. The runtime of the FUN algorithm executed on a margin graph M = (A, E) is polynomial in |A|.

Proof. We assume that M is given as adjacency lists. Likewise, the algorithm constructs MFUN using adjacency lists and stores each edge state along with the respective edge.

Observe that |E| ∈Θ(|A|2) and that the following operations can be computed in polynomial time in |A| on both graphs: (1) initializing and adding edges to MFUN; (2) sorting and iterating through all edges; (3) iterating over incoming edges of a vertex; (4) determining the state of a vertex; (5) running a breadth first search (BFS); (6) transposing the graph and running a reverse BFS; (7) updating an edge state; (8) iterating over all vertices.

16841

<!-- Page 5 -->

## Algorithm

1: Computing the fused universe diagram.

Input: margin graph M(P) = (A, E) of a preference profile P with margins m Output: FUN diagram MFUN

1 MFUN ←(A, ∅)

2 foreach (x, y) ∈E in order of decreasing margin do

3 k ←m(x, y)

4 if y is fixedly dominated and ∃(z, y) ∈MFUN: m(z, y) > k then reject (x, y) and continue if there is a path from y to x of strength > k in MFUN then

6 compute the set of vertices U that have a path to x of strength > k in MFUN

7 if for all u ∈U there exists a path P ∈MFUN from y to u of strength > k, such that for every CC edge

(c, d) ∈P, all paths from d to c in MFUN of strength ≥m(c, d) include vertex y then

8 reject (x, y) and continue

9 if y is not dominated then state(x, y) ←Fix

10 else if y is cycle dominated and ∃(z, y) ∈MFUN: m(z, y) > k then state(x, y) ←CBC

11 else if y is cycle dominated and ∀(z, y) ∈MFUN: m(z, y) = k then state(x, y) ←BC

12 else

13 state(x, y) ←BC

14 update incoming Fix edge of y to BC

15 add (x, y) to MFUN

16 compute the set of edges C ⊆MFUN that form a cycle with (x, y)

17 if C̸ = ∅then

18 state(x, y) ←CC

19 foreach e ∈C with m(e) = k do state(e) ←CC

20 return MFUN

This covers all elemental operations of Algorithm 1 as well as the final pass over all vertices to determine the winner set. In Section 3.2 we explain how the complex operations (namely cycle reject check and cycle update check) reduce to running O(|E|) breadth first searches. Thus, the FUN algorithm overall runs in polynomial time in |A|.

## 4 The FUN Algorithm Returns Exactly the

RV-PUT Winners In the following two sections, we prove that one can correctly identify the RV-PUT winners using the FUN diagram.

## 4.1 Forward Direction: Fix, Branching Choice and Rejected Edges

We show the forward direction: every RV-PUT winner a is identified by the FUN algorithm. To that end, we establish a structural lemma relating the state of an edge in the FUN diagram to its presence or absence in the River diagram under any tiebreaker. We write MRV τ as a shortcut for the River diagram RV(P, τ) of P under tiebreaker τ. Lemma 4.1. For every edge (x, y) ∈M and for all tiebreakers τ ∈L it holds that state(x, y) = Fix ⇒(x, y) ∈MRV τ; (1)

state(x, y) ∈{BC, CBC} ⇒

∃(z, y) ∈MRV τ: m(z, y) ≥m(x, y); (2)

(x, y) /∈MFUN ⇒(x, y) /∈MRV τ. (3)

Proof. Let τ ∈L be an arbitrary tiebreaker. We show Equations (1) and (2) and (3) simultaneously via induction over the margin edges in order of τ.

They are trivially true for the induction base, as MFUN is initiated as an empty graph. For the induction step, consider (x, y) with m(x, y) = k. As induction hypothesis (IH) assume that Equations (1) to (3) are true for all edges processed before (x, y) according to τ.

▷Claim 4.2 (⋆). Let (x, y) ∈MFUN with m(x, y) = k be an edge with state(x, y) ∈{Fix, BC, CBC}. Then (x, y) cannot be rejected from MRV τ by River’s cycle condition.

Equation (1): state(x, y) = Fix ⇒(x, y) ∈MRV τ. By Claim 4.2, the edge (x, y) is not rejected from MRV τ by River’s cycle condition. Assume towards contradiction that it is rejected from MRV τ by River’s branching condition. Then there has to be an edge (z, y) ∈MRV τ with z̸ = x that appears in τ before (x, y). It follows from the contraposition of Equation (3) that (z, y) ∈MFUN. That means that (z, y) is added either before or after (x, y) to MFUN. If (z, y) is added before (x, y), then y is already dominated once the algorithm processes (x, y); contradicting state(x, y) = Fix. Conversely, if (z, y) is added after, then the state of (x, y) is updated to BC in 14; contradicting state(x, y) = Fix.

As a result, (x, y) is not rejected by any of River’s conditions, proving (x, y) ∈MRV τ.

16842

<!-- Page 6 -->

Equation (2): state(x, y) ∈{BC, CBC} ⇒∃(z, y) ∈ MRV τ: m(z, y) ≥k. By Claim 4.2, the edge (x, y) is not rejected from MRV τ by River’s cycle condition. Assume (x, y) is rejected by River’s branching condition. Then there has to be an edge (z, y) ∈MRV τ with m(z, y) ≥k and the claim holds. Otherwise, (x, y) is not rejected at all by River, (x, y) ∈MRV τ and the claim holds since m(x, y) = k.

Equation (3): (x, y) /∈MFUN ⇒(x, y) /∈MRV τ. Since (x, y) /∈MFUN, it was rejected from the FUN diagram – either by the branching (line 4) or cycle reject check (line 5). We show it is also rejected from the River diagram.

First, assume (x, y) was rejected by the branching reject check. Then y is fixedly dominated and there exists an incoming edge to y with margin k′ > k in MFUN. By Equations (1) and (2) of (IH), there exists an edge (z, y) ∈MRV τ with m(z, y) ≥k′. Hence, (x, y) is rejected from MRV τ by River’s branching condition.

Now, assume (x, y) was rejected by the cycle reject check. Let U be the set of vertices from which there exists a path to x in MFUN with strength > k (note that x ∈U). Then the cycle reject check condition ensures the following.

1. MFUN contains a path from y to x with strength > k. 2. For every u ∈U, there exists a path Pyu ∈MFUN from y to u with strength(Pyu) > k such that for every CC edge (c, d) ∈Pyu, all paths Pdc ∈MFUN from d to c with strength(Pdc) ≥m(c, d) > k include vertex y.

We now construct a path from y to x in MRV τ by iteratively extending backward from x, and thereby show that (x, y) must be rejected from MRV τ by the cycle condition. At each step, let s be the current starting vertex of the path. If s = y, we are done. Otherwise, s ∈U and, by assumption, there exists a path from y to s in MFUN of strength > k. Therefore, s must be fixedly or cycle dominated. In both cases, we show that s has an incoming edge (c, s) ∈MRV τ with m(c, s) > k such that c /∈P, allowing us to prepend (c, s) to the path. As y ∈U and U is finite, this backward process must eventually reach y, thereby completing the desired path from y to x in the River diagram.

Initialize P:= (x) as the partial path, and let s:= x denote the current start vertex of P.

s is fixedly dominated. By Equations (1) and (2) of (IH), there is some edge (c, s) ∈MRV τ with m(c, s) > k. Since we only follow edges from MRV τ in P and MRV τ is a tree, c /∈P as otherwise the edge (c, s) would close a cycle in MRV τ. We set P:= (c, s) ◦P and s:= c. s is cycle dominated. By definition of cycle dominated vertices, s has at least one incoming edge in MFUN and all such incoming edges are CC. Note that c ∈U for all incoming edges (c, s) ∈MFUN with m(c, s) > k and, by assumption, y has a path to c in MFUN with strength > k. As a result, there exists at least one incoming edge of s with margin > k in MFUN, and all such incoming edges are on a path from y with strength > k. If one such edge (c, s) is also in the River diagram, then c /∈P (as otherwise the edge (c, s) would close a cycle in MRV τ) and we set P:= (c, s) ◦P and s:= c. Otherwise, every such edge (c, s) ∈MFUN with margin > k is rejected from MRV τ. • If (c, s) is rejected by River’s branching condition, there is (c′, s) ∈MRV τ with m(c′, s) ≥m(c, s) > k. By the contraposition of Equation (3), (c′, s) ∈MFUN and we set P:= (c′, s) ◦P and s:= c′. • If every such edge (c, s) is rejected by River’s cycle condition, then there is a path Psc ∈MRV τ from s to c with strength ≥m(c, s) > k. By the contraposition of Equation (3), Psc ∈MFUN. Now, since (c, s) is a CC edge on a path from y to s and strength(Psc) ≥ m(c, s) > k, our assumption implies y ∈Psc. In conclusion, there exists a path Psc in the River diagram which includes y. In this case, y already has an incoming edge in the River diagram MRV τ and (x, y) is rejected from MRV τ by the branching condition.

Therefore, either (x, y) is rejected from MRV τ by Rivers’ branching condition, or there exists a path from y to x in MRV τ with strength > m(x, y), because of which (x, y) is rejected from MRV τ by River’s cycle condition. This proves the induction step for Equations (1) to (3), and therefore shows the claim.

With this, we can now prove the forward direction. Theorem 4.3 (Forward Direction of Main Theorem). For every preference profile P and every alternative a ∈A:

a ∈RV-PUT(P) ⇒a is cycle/not dominated in MFUN(P)

Proof. We show the contraposition of the claim. For that, recall that by definition every alternative that is neither cycle dominated nor not dominated, must be fixedly dominated. The contraposition can therefore be formulated as a /∈RV-PUT(P) ⇐a is fixedly dominated. Suppose a is fixedly dominated. Then, by definition, it has either an incoming edge labeled Fix, or at least one incoming edge labeled BC or CBC in MFUN. By Theorem 4.1, there exists some incoming edge to y in every universe. Therefore, a /∈RV(P, τ) and a /∈RV-PUT(P).

## 4.2 Backward Direction: Cycle Edges and a Winning Certificate

In this section, we show that every alternative a identified as an RV-PUT winner by the FUN algorithm is indeed a River winner in at least one tiebreaker universe. To that end, we present a procedure that extracts a River diagram from MFUN that certifies a as a winner. We also describe how to construct the tiebreaking order that defines this universe.

Deriving a Potential Certificate for an Alternative Recall that, for a given preference profile P and tiebreaker τ, the River Method computes a tree rooted in some alternative a. This tree certifies a as the winner by containing, for every other alternative b̸ = a, a path from a to b.

Similarly, given the Fused-Universe diagram MFUN and alternative a, we compute a tree T(MFUN, a) rooted at a. If a is an RV-PUT winner, this tree serves as a certificate: it matches the River diagram MRV(P, τ) for some

16843

<!-- Page 7 -->

tiebreaker τ under which a is the unique River winner. When MFUN is clear from the context, we write T a instead of T(MFUN, a). The algorithm computing T a is a variant of Prim’s algorithm for computing a Minimum Spanning Tree (Prim 1957), therefore named DIRECTEDMAXPRIM: 1. Initialize T = ({a}, ∅). 2. While Ec = { (u, v) ∈MFUN | u ∈T ∧v /∈T } exist, add to T an edge from Ec with maximum margin. 3. Return T a = T. An efficient implementation uses a priority queue such as Fibonacci Heaps (Fredman and Tarjan 1987) to select the edges in step 2. For a FUN diagram with |A| alternatives and |E| edges, DIRECTEDMAXPRIM has a runtime in O(|E| + |A| log |A|) (Cormen et al. 2022).

Note that since the algorithm is initialized at a and only adds edges from vertices in T to vertices outside T, the resulting T a is a (not necessarily spanning) tree rooted in a. We now state two properties of T a. The first establishes the existence of strong paths within the tree. Lemma 4.4 (⋆). If a FUN diagram MFUN contains a path Pab from a to b, then T a contains a path P ′ ab from a to b with strength(P ′ ab) ≥strength(Pab). The next explains how T a may include an edge despite a higher-margin edge to the same alternative in MFUN. Lemma 4.5 (⋆). Let MFUN be a FUN diagram with margins m. Let a be an alternative and let s, d, dL be different alternatives reachable from a in MFUN. If MFUN contains edges (d, s), (dL, s) with m(d, s) < m(dL, s) and T a contains (d, s), then T a contains a path PsdL from s to dL with strength(PsdL) ≥m(dL, s).

From the certificate tree T a, we derive a tiebreaker τ a that prioritizes the edges in T a over any other edges with the same margin that are not in T a. We will show in Theorem 4.8 that whenever a is not dominated or cycle dominated in MFUN, running River with this tiebreaker will result in a River diagram MRV(P, τ a) which exactly matches T a. Definition 4.6. Let P be a preference profile and M(P) the corresponding margin graph. A certificate tiebreaker τ a for an alternative a with certificate tree T a is an ordering of all edges in M(P) that fulfills the following two properties:

1. Edges are ordered by descending margin. 2. Among edges with identical margin, those that are in T a come before those not in T a.

Confirming RV-PUT-Winners Using the Certificate Tree Note that T a is not necessarily a spanning tree, as some alternatives may not be reachable from a in MFUN. However, if a is cycle dominated or not dominated, then the certificate tree T a is a spanning tree over all alternatives: Lemma 4.7 (⋆). If an alternative a is cycle dominated or not dominated in MFUN then the certificate tree T a is a spanning tree of M rooted in a.

The full proof can be found in the full version of the paper. In it, we show that the certificate tree T a for a is exactly the River diagram under the certificate tiebreaker τ a. Since T a is rooted in a, it follows that a is the unique River winner in that universe. The proof is by induction over the edges, following τ a, and relies on structural properties of the certificate tree established in Theorems 4.4 and 4.5. Theorem 4.8 ((⋆) Backward Direction of Main Theorem). For every preference profile P and every alternative a ∈A:

a ∈RV-PUT(P) ⇐a is cycle/not dominated in MFUN(P)

## 5 Experiments (Brief Overview)

We implemented our algorithm (Malanowski 2025) and compared its performance against the pref-voting implementations (Mattei and Walsh 2013) of (i) River and Ranked Pairs with brute-force PUT (RV-PUT, RP-PUT) and (ii) Split Cycle, Stable Voting, and Beat Path. Synthetic profiles were drawn from the normalized Mallows model with ϕ = 0.35 (Szufa et al. 2025). Timeouts: 5 minutes for polynomial-time methods (including FUN) and 30 minutes for RV-PUT/RP-PUT.

Our results are illustrated and discussed in detail in the long version of this paper; we give a brief summary.

• Scalability to PUT: For m ≥7, both RV-PUT and RP-PUT exceeded the 30-minute timeout on multiple instances, whereas FUN computed RV-PUT in under 0.1s on the same inputs. • Competitiveness vs. poly-time rules: FUN is on par with Split Cycle and Beat Path and surpasses Stable Voting for larger m; Split Cycle and Beat Path track closely due to Floyd–Warshall implementations. • Effect of voters: Runtime increases when n is small relative to m (more near-ties keep more edges in the FUN diagram). St able Voting shows higher variance than the other methods.

## 6 Conclusion We presented a polynomial-time algorithm for computing the PUT (Parallel-Universe Tiebreaking) variant of

River. Our FUN algorithm exploits River’s branching condition to maintain a compact diagram capturing all possible River outcomes across tiebreakers. This highlights the computational benefit of River’s simple decision process, especially in contrast to Ranked Pairs, whose PUT variant is NP-hard.

The FUN diagram captures all possible winner but may keep edges that never appear in any River diagram. That is, because it removes only edges which are rejected by River in all universes for the same reason (branching or cycle condition). Future work could refine this to the exact union.

As RV-PUT defines a new social choice function, an axiomatic study could be of interest. In particular in comparison to PUT-Ranked Pairs and River in terms of winning set containment and axioms such as clone independence.

Preliminary experiments indicate that FUN scales to instances where brute-force PUT fails and is competitive with well-regarded polynomial-time rules. A broader empirical study on synthetic and real data, including comparison to the optimized RP-PUT implementation by Wang et al.1, is promising future work.

1We thank an anonymous AAAI 2026 reviewer for this pointer.

16844

<!-- Page 8 -->

## Acknowledgments

The project on which this report is based was funded by the Federal Ministry of Research, Technology and Space under the funding code “KI-Servicezentrum Berlin-Brandenburg” 16IS22092. Responsibility for the content of this publication remains with the author (Michelle D¨oring).

## References

Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D. 2016. Handbook of Computational Social Choice. Cambridge University Press. ISBN 978-1-107-06043-2. Brill, M.; and Fischer, F. 2012. The Price of Neutrality for the Ranked Pairs Method. Proceedings of the AAAI Conference on Artificial Intelligence, 26(1): 1299–1305. Number: 1. Conitzer, V.; Freedman, R.; Heitzig, J.; Holliday, W. H.; Jacobs, B. M.; Lambert, N.; Moss´e, M.; Pacuit, E.; Russell, S.; Schoelkopf, H.; Tewolde, E.; and Zwicker, W. S. 2024. Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback. In Proceedings of the 41st International Conference on Machine Learning, 9346 – 9360. Vienna, Austria. ArXiv:2404.10271 [cs]. Cormen, T. H.; Leiserson, C. E.; Rivest, R. L.; and Stein, C. 2022. Introduction to Algorithms. Cambridge, Massachusetts: The MIT Press, fourth edition edition. ISBN 978-0-262-04630-5. D¨oring, M.; Brill, M.; and Heitzig, J. 2025. The River Method. Fredman, M. L.; and Tarjan, R. E. 1987. Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms. Journal of the ACM, 34(3): 596–615. Freeman, R.; Brill, M.; and Conitzer, V. 2015. General Tiebreaking Schemes for Computational Social Choice. In Proceedings of the 2015 International Conference on Autonomous Agents and Multiagent Systems, 1401–1409. F¨urnkranz, J.; and H¨ullermeier, E. 2003. Pairwise preference learning and ranking. In Machine Learning: ECML 2003, 145–156. Springer. Holliday, W. H.; and Pacuit, E. 2023. Split Cycle: a new Condorcet-consistent voting method independent of clones and immune to spoilers. Public Choice, 197(1): 1–62. K¨opf, A.; Kilcher, Y.; von R¨utte, D.; Anagnostidis, S.; Tam, Z. R.; Stevens, K.; Barhoum, A.; Nguyen, D.; Stanley, O.; Nagyfi, R.; et al. 2024. Openassistant conversationsdemocratizing large language model alignment. Advances in Neural Information Processing Systems, 36. Malanowski, J. 2025. River FUN Experiment Code. Published at https://github.com/ forUnity/RiverPutExperimentsAAAI and archived at https://archive.softwareheritage.org with SWHID swh:1:snp:27c386b81e9e5f284f13afc636b0b2cc30c9a605. Mattei, N.; and Walsh, T. 2013. PrefLib: A Library for Preferences http://www.preflib.org. In Perny, P.; Pirlot, M.; and Tsouki`as, A., eds., Algorithmic Decision Theory, 259–270. Berlin, Heidelberg: Springer. ISBN 978-3-642-41575-3.

Prim, R. C. 1957. Shortest Connection Networks and Some Generalizations. The Bell System Technical Journal, 36(6): 1389–1401. Szufa, S.; Boehmer, N.; Bredereck, R.; Faliszewski, P.; Niedermeier, R.; Skowron, P.; Slinko, A.; and Talmon, N. 2025. Drawing a map of elections. Artificial Intelligence, 343: 104332. Tideman, T. N. 1987. Independence of clones as a criterion for voting rules. Social Choice and Welfare, 4(3): 185–206. Wang, J.; Sikdar, S.; Shepherd, T.; Zhao, Z.; Jiang, C.; and Xia, L. 2019. Practical Algorithms for Multi-Stage Voting Rules with Parallel Universes Tiebreaking. Proceedings of the AAAI Conference on Artificial Intelligence, 33(01): 2189–2196. Number: 01. Zavist, T. M.; and Tideman, T. N. 1989. Complete independence of clones in the ranked pairs rule. Social Choice and Welfare, 6(2): 167–173.

16845
