---
title: "Structural Approach to Guiding a Present-Biased Agent"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38708
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38708/42670
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Structural Approach to Guiding a Present-Biased Agent

<!-- Page 1 -->

Structural Approach to Guiding a Present-Biased Agent

Tatiana Belova1, Yuriy Dementiev1, Artur Ignatiev1, Danil Sagunov1

1ITMO University

## Abstract

Time-inconsistent behavior, such as procrastination or abandonment of long-term goals, arises when agents evaluate immediate outcomes disproportionately higher than future ones. This leads to globally suboptimal behavior, where plans are frequently revised or abandoned entirely. In the influential model of Kleinberg and Oren (2014) such behavior is modeled by a present-biased agent navigating a task graph toward a goal, making locally optimal decisions at each step based on discounted future costs. As a result, the agent may repeatedly deviate from initially intended plans. Recent work by Belova et al. (2024) introduced a two-agent extension of this model, where a fully-aware principal attempts to guide the present-biased agent through a specific set of critical tasks without causing abandonment. This captures a rich class of principal–agent dynamics in behavioral settings. In this paper, we provide a comprehensive algorithmic characterization of this problem. We analyze its computational complexity through the framework of parameterized algorithms, focusing on graph parameters that naturally emerge in this setting, such as treewidth, vertex cover, and feedback vertex set. Our main result is a fixed-parameter tractable algorithm when parameterized by the treewidth of the task graph and the number of distinct (v, t)-path costs. Our algorithm encaptures several input settings, such as bounded edge costs and restricted task graph structure. We demonstrate that our main result yields efficient algorithms for a number of such configurations. We complement this with tight hardness results, that highlight the extreme difficulty of the problem even on simplest graphs with bounded number of nodes and constant parameter values, and motivate our choice of parameters. We delineate tractable and intractable regions of the problem landscape, which include answers to open questions of Belova et al. (2024).

## Introduction

Present bias—the tendency to overvalue immediate outcomes relative to future ones—is a well-studied phenomenon in behavioral economics (Laibson 1997; Frederick, Loewenstein, and O’Donoghue 2002). It explains why

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

individuals often abandon long-term beneficial plans in favor of short-term ease, leading to suboptimal results in domains such as health, finance, education, and productivity.

(Kleinberg and Oren 2014) introduced a graph-theoretic model to formalize such behavior in sequential decisionmaking. In their model, a time-inconsistent agent with present bias navigates a directed acyclic graph (DAG) of tasks, choosing each step based on a discounted evaluation of future costs. The agent may abandon the plan before reaching the goal if their perceived cost exceeds the discounted reward. This model provides a powerful abstraction for reasoning about procrastination and dynamic decisionmaking in complex systems.

A natural extension of this framework, described in (Belova et al. 2024), involves a principal (e.g., a teacher, system designer, or platform) who can intervene by modifying the graph to guide the agent toward desired outcomes. Such interventions may involve removing distracting tasks or adding helpful shortcuts. Our work focuses on this setting, where the principal seeks to ensure that a present-biased agent completes a sequence of important tasks and reaches the final goal.

Problem Setting. We study intervention strategies in the Kleinberg–Oren model, where an agent operates on a timeinconsistent planning model M = (G, w, s, t, β, r):

• G = (V, E) is a directed acyclic graph with parallel arcs representing the task structure, • w: E →N0 assigns costs to arcs, • s and t are the start and goal vertices, • β ∈(0, 1] is the present-bias factor, • r is the reward obtained upon reaching t.

When located at vertex v, the agent evaluates all v-t paths and selects the one P = e1e2... ek that minimizes the perceived cost ζM(P) = w(e1) + β · k X i=2 w(ei).

If ζM(P) > β · r, the agent abandons the task entirely. Otherwise, he commits to the first arc e1 = (v, u) and moves to vertex u, where the decision process is repeated recursively. If several paths have a minimum perceived cost, the agent

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16664

<!-- Page 2 -->

selects one of them deterministically, according to a given lexicographic order on the arcs.

Recent work by (Belova et al. 2024) initiated the study of principal-agent problems, where a principal aims to ensure that the agent follows a path from s to t that includes a designated set of critical arcs T ⊆E(G), using limited graph modifications. Two types of interventions were considered:

• T -PATH-DELETION: Can we delete at most k arcs from G so that the agent follows a path from s to t that includes all of T? • T -PATH-ADDITION: Given a set of auxiliary weighted arcs A, can we add at most k arcs from A (without creating cycles) so that the agent follows a path from s to t that includes all of T? In this work, we unify these two problems into a single general formulation:

T -PATH-EDITING Input: A time-inconsistent planning model M = (G, w, s, t, β, r), a set of additional arcs A such that G + A is acyclic and w maps w maps E(G) ∪A into N0, and a set of critical arcs T ⊆E(G). Task: Compute the minimum number of arc edits (deletions from E(G) or additions from A) needed so that the agent follows an s–t path (path in G from s to t) that traverses all arcs in T.

Throughout this paper, we say that the agent follows a path P if the agent, acting according to the Kleinberg–Oren model, traverses every arc of P without abandoning the task at any intermediate vertex.

Notably, unlike the previous formulations that fix a budget k, the optimization version allows a more global view of tractability.

Problem Motivation. In emerging computational systems involving human or autonomous agents, effective task delegation and coordination increasingly rely on explicit modeling of agent behavior. Modern multi-agent architectures often follow hierarchical paradigms, where higher-level entities (principals, mediators) interact with time- or resourceconstrained agents to ensure alignment with overarching objectives.

Agents in such systems may exhibit irrationalities, including time inconsistency or locally myopic behavior. Understanding how and when such agents can be steered toward desired behaviors—especially under minimal interventions—forms a key building block in the design of robust, interpretable, and strategically aligned agent systems. The T -PATH-EDITING problem formalizes one such scenario, capturing goal-aligned influence via constrained structural modifications.

## Model

Example. To illustrate our framework, consider a scenario in which Bob, an AI engineer at a large tech company, is tasked with developing a production-ready LLMbased agent for enterprise document analysis. His ultimate goal is to deploy the agent after thorough benchmarking on realistic tasks (vertex t). There are multiple possible strategies to reach this goal, each composed of subtasks such as data preprocessing, model fine-tuning, prompt engineering, integration, and evaluation. These subtasks form a directed acyclic graph (see Figure 1), where each arc represents an action, and its weight corresponds to the estimated engineering effort or time cost.

However, Bob exhibits present-biased behavior: when evaluating a future plan, he gives full weight to the immediate next task, but discounts the remaining effort by a factor β = 1/2. Starting at node s, he considers several possible execution paths:

• P1 = sbet, P2 = scft: thorough and reliable pipelines involving data cleaning, fine-tuning, and full evaluation: ζM(P1) = ζM(P2) = 10 + 10+10

= 20; • P3 = sadt: a simplified path using default weights and partial testing: ζM(P3) = 10 + 8+8

= 18; • P4 = sbft: a shortcut based on prompt-only adaptation with minimal validation: ζM(P4) = 10 + 2+10

= 16. Bob chooses the path P4 that minimizes the perceived cost, and it is easy to see that at each next vertex he will continue to choose this path, and will eventually follow sbft.

Now consider the role of Alice, Bob’s team lead and project owner. Her priority is to ensure that the critical evaluation step (arc (b, e)) is completed, as it directly affects the model’s reliability and regulatory compliance. Alice provides Bob with a promised reward of r = 36 upon successful deployment. However, due to Bob’s present bias, he perceives this as only β · r = 18 at each decision point.

Suppose Alice simply disables the prompt-only shortcut by removing arc (b, f), hoping to block the path P4, the perceived cost at s becomes 10 + 8+8

= 18 = β · r, which achieve only on path P3. Bob would follow the arc (s, a). In contrast, the path P1 = sbet, which only includes the crucial arc (b, e), has a perceived cost of 20—too high for Bob to choose under present bias.

To resolve this, Alice applies a strategic edit: she introduces a new auxiliary arc (a, b), allowing Bob to access path P = sabet. This new path includes the critical task (b, e), and thanks to the adjusted structure, it has a lower perceived cost 1 + 10+10

= 11 at key decision point a. As a result, Bob follows P = sabet, completing all required stages and aligning his behavior with Alice’s objectives.

s c f t a d b e r = 36 10

10

10 10

8 10

10

10 β = 1/2

8

1

Alice

Bob

**Figure 1.** Example: T = {(b, e)}, A = {(a, b)}. For initial graph G, the agent follows the path sbft. After deletion (b, f)—path sadt. And after adding (a, b)—T-path sabet.

Why Graph Parameters Matter. In real-world planning graphs modeling behavioral agents—such as workflows in education, research, digital assistants, or financial

16665

![Figure extracted from page 2](2026-AAAI-structural-approach-to-guiding-a-present-biased-agent/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-structural-approach-to-guiding-a-present-biased-agent/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-structural-approach-to-guiding-a-present-biased-agent/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-structural-approach-to-guiding-a-present-biased-agent/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

planning—the underlying structure is rarely arbitrary. Instead, it tends to reflect the limited complexity of humandesigned or human-operated systems. This makes structural graph parameters highly relevant for understanding algorithmic tractability in practice (Maniu, Senellart, and Jog 2019).

Below, we summarize the key graph parameters considered in our study. All of these parameters are undirected graph parameters. We consider them with respect to the underlying undirected graph of G + A.

The treewidth (tw) of a graph G is the minimum width among all possible tree decompositions of G, where the width of a tree decomposition is defined as the size of its largest bag minus one. Intuitively, treewidth quantifies how “tree-like” a graph is. Many real-world planning graphs exhibit low treewidth due to hierarchical structure, and dynamic programming algorithms often become efficient on graphs of bounded treewidth (Cygan et al. 2015).

The feedback vertex set number (fvs) is the size of the smallest set of vertices whose removal renders the undirected graph skeleton acyclic. This parameter captures the extent to which cyclic dependencies exist and is often small in acyclic or near-acyclic planning systems.

The vertex cover number (vc) is the size of the smallest set C ⊆V (G) such that every edge (u, v) ∈E(G) is incident to at least one vertex in C. In task graphs with a few highly connected control points or verification steps, the vertex cover tends to be small.

The path length (p) refers to the number of arcs on the longest directed path from source s to target t in the DAG. It reflects the maximum depth of planning or reasoning required by the agent.

The tree-depth (td) of a graph G is the minimum height of a rooted tree T such that G is a subgraph of the closure of T; that is, for every edge (u, v) ∈E(G), one of u or v must be an ancestor of the other in F. Equivalently, treedepth measures how “deeply nested” a graph is in terms of ancestor-descendant relations and reflects hierarchical complexity.

These parameters are not only natural from an algorithmic perspective, but also arise organically in structured task graphs. Treewidth and feedback vertex set are small in many systems where tasks are layered or hierarchically decomposed—such as curriculum maps (Stavrinides and Zuev 2023; Yang et al. 2024), multi-stage workflows, or modular design pipelines. Even when cycles are present, they are typically localized and limited in scope. Vertex cover tends to be small in graphs where dependencies are funneled through a small number of coordination or bottleneck nodes—common in multi-agent or supervisory planning setups (Cygan et al. 2015). Path length is inherently bounded in most practical systems: no realistic agent executes hundreds of sequential steps before reaching a goal. In humanfacing systems, this is constrained by attention spans, task fatigue, or real-time processing limits.

Taken together, these structural properties motivate a parameterized approach to the T -PATH-EDITING problem. By isolating parameters that remain small in realistic deployments, we identify meaningful tractable regimes where efficient intervention strategies for present-biased agents can be computed. This connection between structure and tractability bridges theoretical models with real-world applicability.

Parameterized complexity. To rigorously analyze the computational complexity of the T -PATH-EDITING problem, we rely on the framework of parameterized complexity. This framework allows us to distinguish between sources of hardness by isolating specific aspects of the input—such as structural graph parameters—as formal parameters.

Formally, a parameterized problem is a language Q ⊆ Σ∗× N, where an instance is given as a pair (I, k) consisting of the main input I and a parameter k. A problem is said to be fixed-parameter tractable (FPT) if it can be solved in time f(k) · |I|O(1) for some computable function f depending only on k. This contrasts with the broader class XP, where the running time is allowed to be |I|g(k) for some computable function g.

To classify intractable problems, the W-hierarchy provides a series of hardness classes: FPT = W[0] ⊆W[1] ⊆ W[2] ⊆· · · ⊆W[P]. It is widely believed that FPT̸ = W[1], so proving W[1]-hardness is strong evidence that no fixedparameter tractable algorithm exists. Such hardness proofs are typically obtained via parameterized reductions from known W[1]-complete problems.

In addition, we use the notion of Para-NP-hardness, which refers to parameterized problems that remain NPhard even when the parameter is fixed to a constant. This notion is useful for ruling out tractability in low-parameter regimes.

For a general reference on the theory and techniques of parameterized complexity, we refer the reader to (Cygan et al. 2015).

Our Contribution. We present algorithmic results for T - PATH-EDITING, highlighting structural and numerical conditions under which efficient interventions are possible. We comprehensively describe a complexity landscape of these problems. Our main result is an algorithm parameterized by the treewidth (tw) of the graph G + A and the diversity of path costs:

Theorem 1. T -PATH-EDITING admits an algorithm running in |L|O(tw) ·mO(1) time, where tw equals the treewidth of G + A and

L =

[ v∈V (G)

{w(P) | P is a (v, t)-path in G + A}

.

This shows that T -PATH-EDITING is fixed-parameter tractable when both the graph structure (via treewidth tw) and weight diversity are bounded. We also show:

• NP-hardness on graphs of treewidth 2, • W[1]-hardness w.r.t. the number of vertices n and the combined parameter (p, vc), • XP-algorithms with respect to feedback vertex set, vertex cover, and tree-depth, • FPT-algorithms for cost-limited instances with bounded cost diversity |{w(e)}|.

16666

<!-- Page 4 -->

Related Work. The study of present-biased behavior originates from classical economic theory. Samuelson’s discounted utility model (Samuelson 1937) laid the foundation for formal models of intertemporal choice. This was later extended into the hyperbolic and quasi-hyperbolic discounting frameworks (Laibson 1994; McClure et al. 2004), which more accurately capture behavioral inconsistencies over time. The model we adopt follows the framework introduced by Kleinberg and Oren (Kleinberg and Oren 2014, 2018), where a present-biased agent navigates a task graph by selecting paths according to discounted cost evaluations. Their model can be viewed as a discrete analogue of quasihyperbolic discounting and incorporates Akerlof’s notion of salience (Akerlof 1991).

While the Kleinberg–Oren model has strong empirical motivation, it does not capture all known psychological aspects of time-inconsistent behavior (Frederick, Loewenstein, and O’Donoghue 2002). Nevertheless, it has spurred extensive algorithmic research, including complexity and approximation analyses (Gravin et al. 2016; Kleinberg, Oren, and Raghavan 2016, 2017; Halpern and Saraf 2023; Meyer, Pomplun, and Schill 2022; Dementiev, Fomin, and Ignatiev 2022; Fomin and Strømme 2020).

Several recent works have extended the Kleinberg–Oren model in complementary directions. (Akagi, Marumo, and Kurashima 2024; Akagi, Kim, and Kurashima 2025) propose a continuous-time variant with closed-form solutions for optimal reward placement and abandonment conditions. (Belova et al. 2024) introduce the T -PATH-EDITING framework and analyze structural interventions in two-agent settings.

The principal–agent formulation we study can be seen as a natural and timely generalization of the classical motivating subgraph and P-motivating subgraph problems, where the goal is to identify a subgraph that leads a present-biased agent to the goal (through a specific path P) without abandonment. (Tang et al. 2017; Albers and Kraft 2017, 2019; Oren and Soker 2019; Fomin and Strømme 2020).

Finally, our work is also situated in the broader context of graph modification problems, a well-established domain in algorithmic graph theory. These problems aim to alter a graph’s structure—via edge or vertex deletions/additions—to satisfy desired properties. We refer the reader to surveys such as (Burzyn, Bonomo, and Dur´an 2006; Natanzon, Shamir, and Sharan 2001; Crespelle et al. 2023) for comprehensive overviews.

Polynomial Algorithm on Bounded Vertex

Cover Graphs

In this section, we prove that T -PATH-EDITING can be solved in polynomial time when vertex cover of G + A has constant size.

The first observation about graphs with bounded vertex cover is that such graphs have bounded path lengths.

Observation 1. In a DAG G, every path consists of at most 2 · vc(G) −1 arcs.

Before moving on to the main result of this section, we show an auxiliary algorithmic result. We will use it as a subroutine in our main algorithm.

Proposition 1. There is a polynomial-time algorithm that, given two disjoint sets A, B and a sequence of m pairs (a1, b1), (a2, b2),..., (am, bm) ∈A × B, and a set R ⊂ (A ∪B) finds minimum possible X ⊂(A ∪B) such that

• for each i ∈[m], {ai, bi} ∩X̸ = ∅and • X ∩R = ∅, or reports that X does not exist.

We note that Proposition 1 is folklore and is essentially a problem of finding a vertex cover of minimum cardinality in a bipartite graph. For completeness, we provide the proof with necessary references in the appendix.

We now show the XP-algorithm for T -PATH-EDITING parameterized by vc. In the following proof, our algorithm makes comparisons between perceived costs.

Theorem 2. T -PATH-EDITING admits an algorithm with running time mO(vc2), where vc is the vertex cover number of G + A.

Proof. We present an algorithm that finds an optimal solution to the given instance ((G, w, s, t, β, r), A, T) of T - PATH-EDITING. If no solution exists, the algorithm correctly reports it.

We assume without loss of generality that the algorithm is additionally given a vertex cover C or G + A with |C| ≤ 2 · vc(G + A), as such vertex cover can be found in polynomial time (see, e.g., (Papadimitriou and Steiglitz 1982) for 2-approximation of VERTEX COVER). Let G∗be the graph obtained via optimal sequence of arc edits. Speaking informally, our algorithm does not know G∗ in advance, so its goal is to guess only the relevant structure of G∗: the agent’s s-t path and important shortest paths in G∗. Since all path length are bounded in G + A, (therefore in G∗), the search space for these guesses is bounded with mO(vc2). The high-level sketch of our algorithm is the following.

1. Iterate over all s-t paths P in G + A (the guess for the agent’s path); 2. Construct a set S consisting of all vertices of C and all vertices of the path P. That is, each arc of P has both endpoints in S and each arc of G starts in S or ends in S or both; 3. For each v ∈S, iterate one path Rv from v to t in G + A (the guess for the shortest path); 4. Find a smallest possible set of arc deletions that • forces the agent to follow P, and • for each v ∈S, breaks every v-t path shorter than Rv.

We move on to the formal part of the proof. We describe the steps of the algorithm formally and supply it with correctness claims when needed.

Iterating the agent’s s-t path and critical vertices. In its outer loop, the algorithm iterates an arc set P ⊂(E(G)∪A) such that P ⊃T and P forms a simple s-t path in G + A. In particular, |P| ≤2|C| −1.

16667

<!-- Page 5 -->

Slightly abusing the notation, we refer to P both as an arc set and a path in G + A. Let d be the length of P, and let u0, u1,..., ud be the vertices on P in the natural order, so u0 = s and ud = t. For each i ∈[d], the algorithm denotes by ei the edge between ui−1 and ui in P.

The algorithm then constructs a set S:= {u0, u1,..., ud} ∪C of critical vertices.

Iterating the critical shortest paths edges. The algorithm then iterates R ⊂(E(G) ∪A) such that |R| ≤(|S| + 1) · (2|C| −1), and R ⊃P and

(R1) for each i ∈[d], w(ei) + β · distR(ui, t) ≤β · r.

Here and further in this proof, we slightly abuse the notation and denote by distR(x, y) the distance between x and y in the graph (V (G), R).

An intuition behind R is that it is (when guessed correctly) a union of all shortest paths that are required for the agent to follow P. (R1) specifically ensures that the agent does not abandon P.

Highlighting local obstructions. Having P and R both fixed, the algorithm now aims to find the minimum size subset X ⊂E(G) (the edges one has to delete) such that, for G′ = (V (G), R ∪(E(G) \ X)): (a) we do not delete any edge in R; (b) distances in G′ agree with distances in R; (c) the agent follows every edge ei ∈P in G′. Expressed formally, this becomes

(X1) X ∩R = ∅; (X2) For each v ∈S, distG′(v, t) = distR(v, t); (X3) For each i ∈[d], for each vertex v ∈V (G) and for each edge e′ ∈E(G′) that goes from ui−1 to v and e′̸ = ei, holds w(ei) + β · distG′(ui, t) ≺w(e′) + β · distG′(v, t).

Here and forth, we use ≺to indicate the comparison between perceived costs according to the agent’s behavior. That is, if the parts to the left and to the right of ≺are equal, the result of comparison is equivalent to the comparison of ei and e′ according to the ordering of edges.

We claim that these constraints are essentially equivalent to the agent following P in G′.

Claim 1. Let X ⊂E(G) satisfy (X2). Then R satisfies (R1) and X satisfies (X3) if and only the agent follows P in G′.

Proof of Claim 1. Since (X2) holds, distR(v, t) and distG′(v, t) are equivalent if v ∈S. The agent follows P in G′ if and only if:

• The agent does not abandon the task in neither of u0, u1,..., ud−1, so for each i ∈ [d] we have w(ei) + β · distG′(ui, t) ≤β · r. This is equivalent to (R1). • For each i ∈[d], the agent always prefers the edge ei when goes from ui−1, meaning taking any other edge e′ outgoing from ui−1 gives greater cost estimations (or estimations for e′ and ei are equal but e′ goes after ei in the ordering of edges). This is equivalent to (X3).

The equivalences prove the claim. ⌟

We now explain how the algorithm finds suitable X algorithmically.

Obstructions between critical vertices. The algorithm first constructs X1 by finding the arcs with critical endpoints that have to be deleted necessarily to fulfill the properties. X1 consists of all arcs e′ of G such that e′ starts in some x ∈S and ends in some y ∈S, and either

(i) distR(x, t) > w(e′) + distR(y, t), or (ii) x = ui−1 for some i ∈[d], e′̸ = ei and w(ei) + β · distR(ui, t) ≻w(e′) + β · distR(y, t).

We claim that all arcs in X1 are necessary to delete.

Claim 2. If X satisfies (X2), (X3) then X1 ⊂X.

Proof of Claim 2. Let X ⊂E(G) satisfy (X2), (X3). Targeting towards a contradiction, suppose e′ ∈X1 \ X. Denote by x, y ∈S the start and end points of e′, i.e. e′ goes from x ∈S to y ∈S.

If (i) is true, then distR(x, t) > w(e′) + distR(y, t), then by (X2) we have distG′(x, t) > w(e′) + distG′(y, t), which contradicts the definition of shortest distances, as e′ goes from x to y.

If (ii) is true, then by (X2) we have w(ei) + β · distG′(ui, t) ≻w(e′) + β · distG′(y, t), and this clearly violates (X3), since both ei and e′ start in ui−1. The obtained contradiction finishes the proof of the claim. ⌟

We will show a little later that in any optimal solution, there is no arc between vertices in S that should be deleted but does not belong to X1.

Obstructions incident to non-critical vertices. Then, for each non-critical vertex v ∈V (G) \ S, the algorithm constructs an arc pair set Xv. This is done in the following way. Consider an arc e′ that ends in v and an arc e′′ that starts in v. Let x and y be the start point of e′ and the end point of e′′ respectively. Note that x, y ∈S, since we cannot have arcs between two non-critical vertices. The pair {e′, e′′} is added to Xv if

(i) distR(x, t) > w(e′) + w(e′′) + distR(y, t), or (ii) x = ui−1 for some i ∈[d] and w(ei)+βdistR(ui, t) ≻w(e′)+β(w(e′′)+distR(y, t)).

We show that its necessary for X to hit every pair in Xv.

Claim 3. Let X ⊂E(G) satisfy (X2), (X3). Then, for each v ∈V (G) \ S and for each Y ∈Xv, we have X ∩Y̸ = ∅.

Proof of Claim 3. The proof resembles the proof of Claim 2 with a pair of edges e′, e′′ instead of a single edge e′. Targeting towards a contradiction, assume there exists v ∈ V (G) \ S and {e′, e′′} ∈Xv such that e′, e′′ /∈X.

If {e′, e′′} satisfies (i), then by (X2)

distG′(x, t) ≻w(e′) + w(e′′) + distG′(y, t),

16668

<!-- Page 6 -->

which contradicts the definition shortest distances identically to the proof of Claim 2.

The remaining case is when {e′, e′′} satisfies (ii). By (X2) and ui, y ∈S we have distR(y, t) = distG′(y, t) and distR(ui, t) = distG′(ui, t). Since e′′ goes from v to y, we have distG′(v, t) ≤w(e′′) + distG′(y, t) by definition of dist. Combining all of these with (ii) yields w(ei) + β · distG′(ui, t) ≻w(e′) + β · distG′(v, t), contradiciting (X3). The proof of the claim is complete. ⌟

Inner step of the algorithm. Having P and R fixed by the two outer loops, and X1 and Xv constructed for each v /∈S, the algorithm finds the set X of minimum cardinality that satisfies (X1) and the right parts Claim 2 and Claim 3, that is, X does not intersect R, X contains X1, and X intersects every pair in S v /∈S Xv. The algorithm might also determine that X does not exist (this would mean basically that the choice of P and R is wrong, or no solution exists at all). This happens, for instance, when X1 ∩R̸ = ∅.

Since Xv and Xv′ contains pairwise distinct arcs, the minimum possible set intersecting every pair of Xv can be done independently for each vertex v /∈S. For each v /∈S, the algorithm uses polynomial-time subroutine Proposition 1 to find minimum-size set Xv that hits every pair in Xv and does not intersect R. If the subroutine of Proposition 1 reports that Xv does not exist, the algorithm correctly determines that X does not exist and moves to the next iteration of the outer loops.

If Xv was successfully constructed for each v /∈S, the algorithm constructs X via X:= X1 ∪S v∈V (G)\S Xv. The algorithm obtains a solution of size |R ∩A| + |X|: edges in (R∩A) should be added to G, edges in X should be removed from G. The algorithm updates its best solution with this one and moves to the next choice of P and R.

The description of the algorithm is finished. We move on to proving its correctness.

The algorithm never outputs incorrect solutions. We first show that (R ∩A) ∪X is always a correct solution. Note that if we add R ∩A to G and remove X from G, we obtain exactly G′ = (V (G), R ∪(E(G) \ X). Therefore, it is enough to prove that the agent always follows P in G′.

We show that X constructed in the inner step of the algorithm satisfies (X2) and (X3).

Claim 4. If X satisfies (X1), X contains X1 and X intersects every pair of S v /∈S Xv, then X satisfies (X2) and (X3).

Combining Claim 4 and Claim 1, we obtain that the agent follows P in G′, and P traverses all arcs T by construction. Therefore, the algorithm outputs only correct solutions.

The algorithm finds a minimum-size solution. To see that the algorithm outputs a solution of minimum size, we show a valid choice of P and R that leads to the optimal answer.

To see this choice, let G∗be the graph obtained from G with the optimal edit sequence. Let P ∗be the agent’s s-t path in G∗. We have that T ⊂P ∗, and |P ∗| ≤2 vc(G + A) −1 ≤2|C| −1. Let S be the union of all vertices of P ∗ and C. For each v ∈S, let R∗ v be the edge set of the shortest path between v and t in G∗. Construct R∗as a union of P ∗ and S v∈S R∗ v, clearly

|R∗| ≤(2|C|−1)+|S|·(2|C|−1) ≤(|S|+1)·(2|C|−1), and R∗satisfies (R1) since the agent does not abandon P ∗ in G∗.

Therefore, P ∗and R∗are valid choices of P and R that the algorithm will consider in one of its iterations. Note that X∗(a sequence of arc deletions for G∗) satisfies (X1),(X2), (X3) for this choice of P and R. Hence, the algorithm will find edge deletion set X with |X| = |X∗| and update the answer with an arc edit set of size |R∗∩A| + |X∗|, which is minimum possible by definition of G∗.

Running time analysis. The inner step of the algorithm is polynomial in m, so we have to analyze the number of iteration given by its two loops. In its first loop, the algorithm iterates arc sets of size at most O(vc), and in its second loop it iterates arc sets of size O(vc2). Multiplied, this gives a total of mO(vc2) iterations.

Parameter Landscape The proof of our main algorithmic result, Theorem 1, shares its basic idea with the proof of Theorem 2: guess each distance from v to t, ensure that necessary arcs are added, and delete necessary arcs so that the resulting distances agree with the guess and the resulting agent’s path traverses each arc in T. To achieve the running time of Theorem 1, we avoid guessing the agent’s path P, as we did in Theorem 2, because this approach requires comparing arbitrary arcs of G + A lexicographically. In the proof of Theorem 1, we highly rely on that it’s enough to compare arcs of G + A only to arcs from T.

Other than that, Theorem 1 is a technical dynamic programming algorithm over a tree decomposition, common to the field of parameterized complexity (see, e.g, (Cygan et al. 2015)). The complete proof of Theorem 1 can be found in the appendix.

We now demonstrate that Theorem 1 captures several structural settings for T -PATH-EDITING, including the bounded vertex cover scenario and constant arc costs. Lemma 3. Let (G, w) be a DAG with non-negative integer arc costs w: E(G) →W. Let t be a vertex in G. Let p be a maximum number of arcs in a path in G. Then

|L| ≤min{(p + 1)|W |, 1 + p · max W} and

|L| ≤min{mp+1, m2·vc, m2td +1, m2·fvs +1}. Theorem 3 has interesting consequences. Because each of the three parameters vc, fvs, td is at least tw, the running time of the algorithm of Theorem 1 is upper-bounded by mO(vc2), mO(fvs2), mO(td ·2td). That is, in particular, Theorem 1 generalizes Theorem 2.

For constant number of distinct arc costs, the algorithm of Theorem 1 is more efficient with running time pO(tw ·|W |) · mO(1). In particular, T -PATH-EDITING is fixed-parameter tractable with respect to both fvs +|W| and td +|W|.

16669

<!-- Page 7 -->

Hardness of T -PATH-EDITING In this section we prove hardness of T -PATH-EDITING, showing that our XP-algorithms cannot be turned into FPTalgorithms without breaking FPT̸ = W[1]. Theorem 4. T -PATH-EDITING is W[1]-hard with respect to:

• n, when parallel arcs in G are allowed, • p + vc, when parallel arcs in G are forbidden.

Proof. We give a parameterized gap reduction from MOD- IFIED k-SUM (MkS), which is W[1]-hard (Dementiev, Fomin, and Ignatiev 2022). In MkS, we are given k integer sets X1,..., Xk and the target sum S. The goal is to determine whether there exists a choice of k integers, one from each of X1, X2,..., Xk, with a total sum S.

Given an instance of (X1,..., Xk, S) of MkS, we construct a corresponding T -PATH-EDITING instance as illustrated in Figure 2. For each set Xi, we create a gadget consisting of two vertices vi and vi+1 connected by multiple parallel arcs, each representing an element x ∈Xi with weight w = x. The goal is to ensure that the agent reaches vertex t via the unique T-path sabt including the critical arc (b, t).

The construction uses the following parameters: β = 1

4 + ε for arbitrary 0 < ε < 1; r = 10 · S; A = ∅; T = {(b, t)}; x = S +2. We duplicate each of the arcs of (s, c), (c, t) into z:= |X1| +... + |Xk| identical copies with the same arc cost. Breaking the path s →c →t in G uses at least z edits.

We will show that the answer to the MODIFIED k-SUM problem is “Yes” if and only if there is a solution for the T -PATH-EDITING problem of size no greater than z −k.

Suppose that the T -PATH-EDITING instance has a feasible solution of size at most z −k. Then, the only arcs removed are those between vertices v1,..., vk, t in gadgets; removing any arc from the lower part of the graph would be too costly or would block the required edge (b, t). Let G′ denote the modified graph, and let S′ be the cost of the shortest v1-t path in G′.

We now analyze possible values of S′. If S′ > x−2, then S′ ≥x −1, and the perceived cost of any path starting with s →a →... is at least β · (1 + x −1), which is worse than the perceived cost of the lower path s →c →t, that is equal to β · (x −ε). Hence, the agent would not take the s →a →b →t path. If S′ < x −2, then S′ ≤x −3, and, when he makes decision in the vertex a, the agent compares

1 + β · S′ < 0 + β · (x + 1), and prefers to go through v1 rather than directly to b.

Therefore, the only way for the agent to traverse the desired arc (b, t) is when S′ = S = x −2. This implies the existence of a sequence of arc weights corresponding to a valid solution of the original MODIFIED k-SUM instance. Conversely, any such solution induces a deletion pattern in T -PATH-EDITING with no more than z −k edits, that forces the agent to pass through the arc (b, t) as desired.

At the same time, as is evident from the proof, the only solution of another type for such T -PATH-EDITING instance— to break the path s →c →t—will have a size at least z. Which completes our reduction.

X1

⋯

Xk v1 t s v2 vk

0

0 0

1 x −ε x + 1 a b c

**Figure 2.** The construction of graph G from Theorem 4.

Note that the construction of the graph G involves only k + 5 vertices. Int the same time, this example can be easily modified into an example without parallel arcs by adding an additional vertex in the middle of each arc. In such a graph, the vertex cover number will not exceed k + 5, and the parameter p, the maximal arc length of a path in G, is equal to 2k + 2. Thus, we have obtained a parameterized reduction to T -PATH-EDITING with parameter n = k + 5 in one case, and p + vc ≤3k + 7 in the other.

This completes the reduction, establishing W[1]-hardness for both settings.

The graph in the reduction of Theorem 4 is a seriesparallel graph, and such graphs are known to have treewidth at most two (Brandst¨adt, Le, and Spinrad 1999).

Corollary 5. T -PATH-EDITING is NP-hard for tw = 2.

Note that this result is tight: when tw(G + A) = 1, the graph is a tree, and the T -PATH-EDITING problem becomes trivial. In this case, the agent has a unique s–t path, and the decision reduces to checking whether agent follow this path and whether it contains all arcs in T, with no modifications required.

On the other hand, (Belova et al. 2024) proved that the T - PATH-DELETION problem—a special case of our T -PATH- EDITING formulation—remains NP-hard even when the maximum length p of any s–t path in G is bounded by 8. This result immediately implies that T -PATH-EDITING is Para-NP-hard with respect to the parameter p.

## Conclusion

We have introduced and studied the T -PATH-EDITING problem, a general framework for designing structural interventions that guide time-inconsistent agents toward completing critical tasks. Our model extends the Kleinberg–Oren framework by formalizing the principal’s role in influencing agent behavior through minimal graph edits.

Our results delineate the tractability frontier of T -PATH- EDITING across a range of structural parameters, including treewidth, vertex cover, feedback vertex set, and path length. In particular, we demonstrate fixed-parameter tractability for combined parameters capturing graph structure and cost diversity, while also establishing lower bounds via Para-NPand W[1]-hardness.

An intriguing open question is to determine whether T -

PATH-EDITING admits an f(tw) · mg(p)-time algorithm for computable functions f and g.

16670

<!-- Page 8 -->

## Acknowledgments

This work was supported by the Ministry of Economic Development of the Russian Federation (IGK 000000C313925P4C0002), agreement №139-15-2025-010.

## References

Akagi, Y.; Kim, H.; and Kurashima, T. 2025. A Continuoustime Tractable Model for Present-biased Agents. In AAAI- 25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA, 13510–13519. AAAI Press.

Akagi, Y.; Marumo, N.; and Kurashima, T. 2024. Analytically Tractable Models for Decision Making under Present Bias. In Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February 20-27, 2024, Vancouver, Canada, 9441–9450. AAAI Press.

Akerlof, G. A. 1991. Procrastination and obedience. American Economic Review: Papers and Proceedings, 81(2): 1– 19.

Albers, S.; and Kraft, D. 2017. On the Value of Penalties in Time-Inconsistent Planning. In 44th International Colloquium on Automata, Languages, and Programming (ICALP), 10:1–10:12.

Albers, S.; and Kraft, D. 2019. Motivating Time- Inconsistent Agents: A Computational Approach. Theory Comput. Syst., 63(3): 466–487.

Belova, T.; Dementiev, Y.; Fomin, F. V.; Golovach, P. A.; and Ignatiev, A. 2024. How to Guide a Present-Biased Agent Through Prescribed Tasks? In ECAI 2024 - 27th European Conference on Artificial Intelligence, 19-24 October 2024, Santiago de Compostela, Spain - Including 13th Conference on Prestigious Applications of Intelligent Systems (PAIS 2024), volume 392 of Frontiers in Artificial Intelligence and Applications, 3461–3468. IOS Press.

Brandst¨adt, A.; Le, V. B.; and Spinrad, J. P. 1999. Graph Classes: A Survey. Society for Industrial and Applied Mathematics.

Burzyn, P.; Bonomo, F.; and Dur´an, G. 2006. NPcompleteness results for edge modification problems. Discrete Applied Mathematics, 154(13): 1824–1844.

Crespelle, C.; Drange, P. G.; Fomin, F. V.; and Golovach, P. A. 2023. A survey of parameterized algorithms and the complexity of edge modification. Comput. Sci. Rev., 48: 100556.

Cygan, M.; Fomin, F. V.; Kowalik, L.; Lokshtanov, D.; Marx, D.; Pilipczuk, M.; Pilipczuk, M.; and Saurabh, S. 2015. Parameterized Algorithms. Springer.

Dementiev, Y.; Fomin, F.; and Ignatiev, A. 2022. Inconsistent Planning: When in Doubt, Toss a Coin! Proceedings of the 36th AAAI Conference on Artificial Intelligence (AAAI), 36(9): 9724–9731.

Fomin, F. V.; and Strømme, T. J. F. 2020. Time-Inconsistent Planning: Simple Motivation Is Hard to Find. In Proceeding of the 34th AAAI Conference on Artificial Intelligence (AAAI), 9843–9850. AAAI Press. Frederick, S.; Loewenstein, G.; and O’Donoghue, T. 2002. Time Discounting and Time Preference: A Critical Review. Journal of Economic Literature, 40(2): 351–401. Gravin, N.; Immorlica, N.; Lucier, B.; and Pountourakis, E. 2016. Procrastination with Variable Present Bias. In ACM Conference on Economics and Computation (EC), 361. Halpern, J. Y.; and Saraf, A. 2023. Chunking Tasks for Present-Biased Agents. In Proceedings of the 24th ACM Conference on Economics and Computation (EC), 853–884. Kleinberg, J. M.; and Oren, S. 2014. Time-inconsistent planning: a computational problem in behavioral economics. In ACM Conference on Economics and Computation (EC), 547–564. Kleinberg, J. M.; and Oren, S. 2018. Time-inconsistent planning: a computational problem in behavioral economics. Commun. ACM, 61(3): 99–107. Kleinberg, J. M.; Oren, S.; and Raghavan, M. 2016. Planning Problems for Sophisticated Agents with Present Bias. In ACM Conference on Economics and Computation (EC), 343–360. Kleinberg, J. M.; Oren, S.; and Raghavan, M. 2017. Planning with Multiple Biases. In ACM Conference on Economics and Computation (EC), 567–584. Laibson, D. 1997. Golden Eggs and Hyperbolic Discounting*. The Quarterly Journal of Economics, 112(2): 443– 478. Laibson, D. I. 1994. Hyperbolic Discounting and Consumption. Ph.D. thesis, Massachusetts Institute of Technology, Department of Economics. Maniu, S.; Senellart, P.; and Jog, S. 2019. An Experimental Study of the Treewidth of Real-World Graph Data. In 22nd International Conference on Database Theory, ICDT 2019, March 26-28, 2019, Lisbon, Portugal, volume 127 of LIPIcs, 12:1–12:18. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. McClure, S. M.; Laibson, D. I.; Loewenstein, G.; and Cohen, J. D. 2004. Separate Neural Systems Value Immediate and Delayed Monetary Rewards. Science, 306(5695): 503–507. Meyer, S. A.; Pomplun, J.; and Schill, J. 2022. Present bias in partially sophisticated and assisted agents. Mathematical Social Sciences, 118: 36–47. Natanzon, A.; Shamir, R.; and Sharan, R. 2001. Complexity classification of some edge modification problems. Discrete Applied Mathematics, 113(1): 109–128. Oren, S.; and Soker, D. 2019. Principal-agent problems with present-biased agents. In Proceedings of the 12th International Symposium on Algorithmic Game Theory (SAGT), 237–251. Springer. Papadimitriou, C. H.; and Steiglitz, K. 1982. Combinatorial Optimization: Algorithms and Complexity. Prentice-Hall. ISBN 0-13-152462-3.

16671

<!-- Page 9 -->

Samuelson, P. A. 1937. A Note on Measurement of Utility. The Review of Economic Studies, 4(2): 155–161. Stavrinides, P.; and Zuev, K. 2023. Course-prerequisite networks for analyzing and understanding academic curricula. Applied Network Science, 8. Tang, P.; Teng, Y.; Wang, Z.; Xiao, S.; and Xu, Y. 2017. Computational issues in time-inconsistent planning. In Proceedings of the 31st Conference on Artificial Intelligence (AAAI). AAAI Press. Yang, B.; Gharebhaygloo, M.; Rondi, H.; Hortis, E.; Lostalo, E.; Huang, X.; and Ercal, G. 2024. Comparative analysis of course prerequisite networks for five Midwestern public institutions. Applied Network Science, 9.

16672
