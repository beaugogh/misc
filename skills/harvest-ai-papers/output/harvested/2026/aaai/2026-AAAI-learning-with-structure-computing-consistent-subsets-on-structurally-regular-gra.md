---
title: "Learning with Structure: Computing Consistent Subsets on Structurally-Regular Graphs"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38427
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38427/42389
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Learning with Structure: Computing Consistent Subsets on Structurally-Regular Graphs

<!-- Page 1 -->

Learning with Structure: Computing Consistent Subsets on Structurally-Regular Graphs

Aritra Banik1, Mano Prakash Parthasarathi2, Venkatesh Raman3, Diya Roy1, Abhishek Sahu1

1National Institute of Science, Education and Research, An OCC of Homi Bhabha National Institute, Bhubaneswar, India 2North Carolina State University, Raleigh, NC, USA 3(Retd) The Institute of Mathematical Sciences, HBNI, Chennai, India aritra@niser.ac.in, mpartha@ncsu.edu, vraman@imsc.res.in, diya.roy@niser.ac.in, abhisheksahu@niser.ac.in

## Abstract

The Minimum Consistent Subset (MCS) problem arises naturally in the context of supervised clustering and instance selection. In supervised clustering, one aims to infer a meaningful partitioning of data using a small labeled subset. However, the sheer volume of training data in modern applications poses a significant computational challenge. The MCS problem formalizes this goal: given a labeled dataset X in a metric space, the task is to compute a smallest subset S of X such that every point in X shares its label with at least one of its nearest neighbors in S. Recently, the MCS problem has been extended to graph metrics, where distances are defined by shortest paths. Prior work has shown that MCS remains NP-hard even on simple graph classes like trees, and presented an fixed-parameter tractable (FPT) algorithm parameterized by the number of colors for MCS on trees. This raises the challenge of identifying graph classes that admit algorithms efficient in both input size (n) and the number of colors (c). In this work, we study the Minimum Consistent Subset problem on graphs, focusing on two well-established measures: the vertex cover number (vc) and the neighborhood diversity (nd). Specifically, we design efficient algorithms for graphs exhibiting small vc or small nd, which frequently arise in realworld domains characterized by local sparsity or repetitive structure. These parameters are particularly relevant because they capture structural properties that often correlate with the tractability of otherwise hard problems. Graphs with small vertex cover sizes are ”almost independent sets”, representing sparse interactions, while graphs with small neighborhood diversity exhibit a high degree of symmetry and regularity. Importantly, small neighborhood diversity can occur even in dense graphs, a property frequently observed in domains such as social networks with modular communities or knowledge graphs with repeated relational patterns. Thus, algorithms designed to work efficiently for graphs with small neighborhood diversity are capable of efficiently solving MCS in complex settings where small vertex covers may not exist. We show that MCS is FPT when parameterized by the vertex cover number and by neighborhood diversity. In each case, we present an algorithm whose running time is polynomial in n and c, and the non-polynomial part depends solely on the chosen parameter. Notably, our algorithms remain efficient for arbitrarily many colors, as their complexity is polynomially dependent on the number of colors.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Extended version — https://arxiv.org/abs/2512.12860

## Introduction

Clustering lies at the heart of numerous tasks in computer science and machine learning. In its essence, given a set of points in a metric space (P, d), the objective is to partition them such that “proximate” points reside within the same cluster. While various unsupervised approaches exist, supervised learning offers a powerful paradigm for achieving “most appropriate” clustering.

In supervised clustering, a labeled training dataset i.e., a subset of points P ′ ⊂P endowed with a coloring function C: P ′ →[c] (where each color denotes a class/cluster) is provided to distill underlying patterns. Usually, given the training dataset, a learning algorithm outputs a set of cluster centers C = {c1,..., cr}. Subsequently, an unlabeled point q is assigned the color C(ci) where ci = NN(q, C), with NN(q, C) representing the nearest neighbors of q in C.

However, the ever-increasing volume of modern datasets poses significant computational challenges for learning algorithms. Large datasets, while information-rich, often lead to protracted learning times. This has motivated a rich line of work on instance selection, where the goal is to extract a small, yet representative, subset of the training data that preserves classification behavior. A classical formulation of this idea is the Minimum Consistent Subset (MCS) problem, introduced in 1968 (Hart 1968). Given a colored training dataset T, the MCS problem seeks a minimum cardinality subset S ⊆T such that for every point t ∈T, the color of t is same as the color of at least one of its nearest neighbors in S. Despite its apparent simplicity, the MCS problem poses significant computational hurdles and is known to be computationally hard in Euclidean spaces (Wilfong 1991; Khodamoradi, Krishnamurti, and Roy 2018), and also hard to approximate in general settings (Chitnis 2022).

The MCS problem has recently been extended to graph metrics, motivated by applications where similarity is naturally modeled by graphs, such as social or knowledge networks. In the Consistent Subset Problem on Graphs (CSPG), we are given a graph G = (V, E) with a vertex coloring C: V →[c]. The distance metric is defined as the shortest path distance in G, denoted by d(u, v). For a vertex v ∈V and a subset U ⊆V, let d(v, U) = minu∈U d(v, u). The set

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

14149

<!-- Page 2 -->

of nearest neighbors of v in U is denoted by NN(v, U) = {u ∈U: d(v, u) = d(v, U)}.

A subset of vertices S ⊆V (G) is called a consistent subset for (G, C) if, for every vertex v ∈V (G), the color of v is present among the colors of its nearest neighbors in S, i.e., C(v) ∈C(NN(v, S)).

CONSISTENT SUBSET PROBLEM ON GRAPHS (CSPG)

Input: A graph G and a coloring function C: V (G) → [c]. Question: Compute a minimum consistent subset for (G, C).

This graph-theoretic version of the MCS problem (i.e., CSPG) has recently drawn attention for both its theoretical appeal and practical relevance. Polynomial-time algorithms have been discovered for certain special graph classes, such as paths, spiders, and caterpillars (Dey, Maheshwari, and Nandy 2023), and later for bi-colored trees (Dey, Maheshwari, and Nandy 2021) and for k-colored trees (for fixed k) (Arimura et al. 2023). For more related works, we refer to (Manna 2024a,b; Biniaz and Khamsepour 2024). Although results were known for bi-colored and k-colored trees, the status for the problem when the underlying graph is a general tree was open for a long time. In a recent breakthrough, (Banik et al. 2024) the authors systematically investigated CSPG and resolved this question. Their work led to two major contributions:

• They established that CSPG is NP-complete on trees, resolving a key open question. This result is particularly striking, as many hard graph problems become tractable when restricted to trees. • They designed a fixed-parameter tractable (FPT) algorithm, i.e., an algorithm running in time f(k) · nO(1), where k is a chosen parameter and f is a computable function independent of the input size, for trees, with a running time of O(26c · n6), where c is the number of colors (chosen as the parameter) and n is the number of vertices. This significantly improves upon earlier bruteforce approaches with super-exponential dependence on c.

The hardness of CSPG on trees, where the minimum feedback vertex set (FVS) is empty set, has significant implications: it precludes the existence of an FPT algorithm parameterized solely by FVS. This calls for stronger structural parameters to recover tractability. In this work, we take this challenge head-on and present FPT algorithms for MCS parameterized by two natural and well-studied graph parameters:

• Vertex Cover Number (vc), which measures the minimum number of vertices needed to cover all edges of the graph. • Neighborhood Diversity (nd), which bounds the number of types of neighborhoods across the graph and is strictly stronger than vertex cover in dense graphs.

A formal definition for both parameters is presented in the next section. Our key contribution is that our algorithms are independent of the number of colors c, in stark contrast to prior work where the exponential dependence on c was unavoidable. Specifically, we show:

• MCS admits an FPT algorithm parameterized by vertex cover size, with running time kO(k) · poly(n, c), where f is color-independent and k is the size of the vertex cover. • MCS also admits an FPT algorithm parameterized by neighborhood diversity, again avoiding any exponential dependence on the number of colors.

In particular, we want to bring to the reader’s attention that while designing an FPT algorithm with dependence on both neighborhood diversity (r) and the number of colors (c) is straightforward, due to Claim 1.10, removing the dependence on the number of colors is highly non-trivial. This is because when the number of colors is large, the number of possible combinations becomes prohibitively high, resulting in a running time that is no longer FPT in r. However, our key insight is that the interaction of a small number of important or responsible colors with the solution is sufficient to determine the interaction of all other colors. While we may not be able to explicitly identify these responsible colors in advance, once we know how they interact with the solution, we can use a color-coding technique to probabilistically isolate and identify a most suitable set of such colors. This allows us to reduce the problem to a collection of independent subproblems, each of which can be solved separately using a greedy algorithm. The solutions to these subproblems can then be combined to obtain a solution to the original instance. To achieve this, we exploit structural properties arising from both the neighborhood diversity of the graph and the specific characteristics of the problem.

At a high level, our algorithmic technique departs from the conventional use of color coding. Typically, color coding is employed to mark objects or structural features of a problem instance in a way that enables their independent resolution. In contrast, our approach involves color coding the elements themselves (in our case, the colors), with the goal of ensuring that a greedily selected subset of solution elements remains well separated under the resulting color distribution. We believe that this perspective introduces a novel and potentially widely applicable direction for color coding, with possible extensions to a broader class of combinatorial problems beyond the specific context addressed in this work.

The parameter neighborhood diversity (nd) is particularly relevant in the context of AI and machine learning applications on graphs. While vertex cover captures a notion of ”sparseness” around edges, neighborhood diversity provides a finer-grained measure of structural regularity. Graphs with small neighborhood diversity are those where most vertices have neighborhoods that are structurally similar, even if the graph is dense. Such structures appear in various real-world networks, including social networks with distinct community structures, or knowledge graphs where entities often share common relational patterns. An FPT algorithm parameterized by nd is significant because it indicates tractability not just for sparse graphs (like those with small vertex

14150

<!-- Page 3 -->

cover), but also for certain types of dense graphs that exhibit high regularity in their local connectivity patterns, a characteristic often observed in complex systems modeled as graphs in AI. This allows for efficient solutions in scenarios where a small vertex cover might not exist, but the underlying structure still permits algorithmic leverage.

Notations and Definitions Graph Notations and Definitions: Let G be a graph. We use V (G) and E(G) to denote the set of vertices and edges of G, respectively. For a set of vertices S, by G\S we mean G[V (G) \ S], i.e., the subgraph of G induced on V \ S. For a vertex v, N(v) denotes the set of neighbors of v in G and N[v] = N(v) ∪{v} denotes the closed neighborhood of v. We call a graph G a complete graph if every pair of vertices in G is adjacent. A clique in G is an induced subgraph that is complete. In contrast, a set I ⊆V (G) is an independent set if no two vertices in I are adjacent in G. A set M ⊆V (G) is a vertex cover if for every edge in G, at least one of its endpoints lies in M.

Two vertices u and v are of the same type if N(v)\{u} = N(u) \ {v}. Note that, this defines an equivalence relation on V (G) (Matsumoto, Kurita, and Kiyomi 2025). A neighborhood decomposition of a graph G is a partition C = {C1, C2,..., Cw} of V (G) such that all vertices in each Ci are of same type. Each Ci is a neighborhood class, and w is the size of the decomposition. The neighborhood diversity, ND(G), is the minimum size of a neighborhood decomposition of G.

Observation 0.1. Given a graph G, ND(G) can be computed in polynomial time (Lampis 2012).

We define the set of vertices at distance ℓfrom a vertex v by N ℓ(v) = {u ∈V: d(u, v) = ℓ} and the set of vertices at distance ℓfrom a vertex v of color a by N ℓ a(v) = {u ∈ V: d(u, v) = ℓand C(u) = a}. For any vertex v, let Na(v) denotes the set of neighbors of v, with color a. For X ⊆ V (G), we define N(X) to be the neighbors of vertices in X. Most of the symbols and notations of graph theory used are standard and taken from (Diestel 2012). Parameterized Complexity: Parameterized complexity offers a framework for solving NP-hard problems more efficiently by isolating the combinatorial explosion to a parameter that is small in practice. A problem is fixed-parameter tractable (FPT) if it can be solved in time f(ℓ) · |I|O(1), where ℓis the parameter, |I| is the input size, and f is a computable function. Safe reduction rules are polynomialtime preprocessing steps that simplify the instance without changing its answer. For a detailed background, readers can refer to (Cygan et al. 2015). Hitting Set: Given a set system (U, F), we say that H ⊆U is a hitting set for (U, F) if ∀F ∈F, H ∩F̸ = ∅and a set of subsets F′ ⊆F is called a set cover for (U, F) if S

F ∈F′ F = U. From (Cygan et al. 2015)[Theorem 6.1], we have the following proposition.

Proposition 1. Given a hitting set instance HS(U, F), a hitting set of minimum size can be found in time 2|F|(|U| + |F|)O(1).

The O∗notation suppresses polynomial factors in the input size. Specifically, O∗(f(n)) = O(f(n)·poly(n)), where polynomial factors are omitted for clarity when they are not the focus of the analysis.

FPT Algorithm Parameterized by Vertex

Cover Size

In this section, we present a fixed-parameter tractable (FPT) algorithm for the MCS problem parameterized by the size of the vertex cover. For completeness, we begin with a formal definition of the problem.

CONSISTENT SUBSET PROBLEM PARAMETERIZED BY VERTEX COVER SIZE

Input: A graph G = (V = M ⊔I, E) where |M| = k and G[I] is an independent set, along with a coloring function C: V (G) →[c]. Question: Compute a minimum consistent subset (MCS) S for (G, C). Parameter: k

It is well-known that the VERTEX COVER problem is FPT when parameterized by the solution size k (Cygan et al. 2015). Let k be the size of the minimum vertex cover. As a preprocessing step, we compute a vertex cover M of size k. We define I = V (G) \ M. Observe that the induced subgraph G[I] is edgeless.

Observation 1.1. For any two vertices u and v in G, 0 ≤ d(u, v) ≤2k. In particular, if at least one of u, v ∈M, then 0 ≤d(u, v) ≤(2k −1).

Proof. Let P be a shortest path between vertices u and v. Since I is an independent set, no two consecutive vertices on P can belong to I. Thus, between any two vertices from I, there must be at least one vertex from M.

The path P can contain at most k vertices from M, as |M| = k. Therefore, the number of vertices from I on P is at most k+1. This gives an upper bound on the total number of vertices in P as k + (k + 1) = 2k + 1.

In the case where either u ∈M or v ∈M, the number of vertices from I on P can be at most k, and thus the total number of vertices in P is at most 2k. Therefore, the observation follows.

Next, we make two guesses with respect to a minimum consistent subset S and attempt to find a solution that respects the guesses.

Guess 1: We guess the distances from each vertex ui in

M to S. More specifically, we assume that an array D = [d1, d2, · · · dk] is given where di denote the distance between ui and S. By Observation 1.1, each entry di can take a value between 0 and (2k −1). Thus, the total number of guesses for D is bounded by (2k)k. Guess 2: We guess the set of vertices M1 ⊆M, which con- sists of the neighbors of the vertices S ∩I. Formally, M1 = {u | u ∈N(S ∩I) \ (S ∩M)}. The number of choices is bounded by 2k.

14151

<!-- Page 4 -->

Let I OUT(D) be the set of vertices in I that are at a distance at most di −1 from some vertex ui ∈M. For any choice of (D, M1), we say that a set of vertices X ⊆V (G) respects the choice (D, M1), if ∀ui ∈M, d(ui, X) = di and N(X ∩I) = M1. Therefore, given (D, M1), our aim is to find a minimum cardinality consistent subset S ⊆V (G) that respects the choice (D, M1). Observation 1.2. For any minimal consistent subset S respecting (D, M1), S ∩I OUT(D) = ∅.

Proof. Assume, for the sake of contradiction, that there exists a vertex v ∈S ∩I OUT(D). By the definition of I OUT(D), there exists a vertex ui ∈M such that d(ui, v) ≤di −1, where di = d(ui, S) by definition. Since v ∈S, it follows that d(ui, S) ≤d(ui, v) = di −1, which is a contradiction to di = d(ui, S) as defined in D. Therefore, our assumption is false, and hence we conclude that S ∩I OUT(D) = ∅.

We define M0 = S ∩M, i.e. M0 = {ui ∈M | di = 0} and Mx = M \ (M0 ∪M1). Recall, for any vertex v, we denote the set of vertices at distance d from v by N d(v), the set of vertices of color a in the neighbor of v by Na(v) and the set of vertices of color a at distance d from v by N d a(v). We extend the scope of D and define di for the vertices ui in I as follows. Let dmin ui be the minimum distance in D among the set of vertices N(ui), i.e. dmin ui = minuj∈N(ui) dj. Note that all the neighbors of ui are in M and hence di = dmin ui + 1 is well defined. For any vertex ui ∈I, we define Ci to be the set of colors of all those vertices that are at distance di from ui and do not belong to the set (Mx ∪M1), i.e. Ci = {C(uj) | uj ∈ N di(ui) \ (Mx ∪M1 ∪I OUT(D))}. Let I IN ⊆I be the set of vertices ui such that C(ui) /∈Ci. Observation 1.3. For any consistent subset S respecting (D, M1), I IN(D) ⊆S.

Proof. Suppose not. Let ui ∈I IN(D) but ui /∈S. Also, let x be the closest vertex in S from ui such that C(x) = C(ui). Consider P as the shortest path between ui and x, also let uj ∈M be the vertex next to ui in path P. Observe that, d(uj, x) < (dmin ui + 1) −1 = dmin ui ≤dj, which contradicts the assumption that S respects the choice D.

Observation 1.4. Given D, in polynomial time, we can find out the set of vertices in I IN(D) and I OUT(D).

Proof. For a given choice of D, both I OUT(D) and I IN(D) can be constructed in polynomial time using shortest path algorithms.

We have established that for any consistent subset S respecting D, I IN(D) ⊆S and I OUT(D) ∩S = ∅. If I IN(D) ∩I OUT(D)̸ = ∅, then we simply discard the guess D.

We denote a vertex ui to be satisfied if ∃a vertex v ∈ N di(ui)∩(M0∪I IN(D)) such that C(ui) = C(v). If a vertex is not satisfied, we call it unsatisfied and let U denote the set of all unsatisfied vertices. For any color a, let U a ⊆U denote the subset of vertices in U that are colored a.

Let S be any solution that respects (D, M1). For each color a, define Sa ⊆S \ (I IN(D) ∪M0) to be the set of vertices in S of color a, excluding those in I IN(D) and M0. Let S′ a ⊆I \ I OUT(D) be any set of vertices of color a such that for every vertex ui ∈U a, d(ui, S′ a) ≤di. Lemma 1.5. The set S′ = (S\Sa)∪S′ a is a consistent subset respecting (D, M1), when S is consistent with (D, M1).

Proof. For the sake of contradiction, suppose that the set S′ is not consistent. Then, by the definition, there exists at least one vertex ui ∈V (G) such that C(ui) /∈C(NN(ui, S′)). Note that ui ∈U. Now, if ui /∈U a i.e., C(ui) = b (say). In this case, as S is a consistent subset and by the construction of S′, ∃a vertex uj ∈S′ of color b such that d(ui, uj) = di. Hence, ui ∈U a and by the definition of S′ a, there exists a vertex uj of color C(ui) such that d(ui, uj) ≤di. Hence, we have d′ i = d(ui, S′) < di. Observe that ui ∈I; otherwise, the fact that d(ui, S′) < di would imply that S′ does not respect Guess 1. Let ub be any vertex in NN(ui, S′). Let uc ∈M be the neighbor of ui in M lying on the path from ui to ub. Then, d(uc, ub) < di −1.

We know that di = dmin ui + 1 and dc ≥(dmin ui + 1) −1 = di−1 > d(uc, ub). Hence, S′ a contains a vertex at distance at most dc −1. Thus S′ a contains a vertex from I OUT(D), which contradicts the definition of S′ a, completing the proof.

Therefore, from Lemma 1.5, given D and M1, for each color a ∈C(U), our objective reduces to independently computing a minimum-size set S∗ a ⊆I \I OUT(D) of color a, such that for every vertex ui ∈U a, it holds that d(ui, S∗ a) ≤ di.

Recall, we define the set of vertices at distance ℓfrom a vertex v by N ℓ(v) = {u ∈V: d(u, v) = ℓ}.

For any vertex ui ∈U a, let M a

1 (ui) ⊆N di−1(ui) ∩M1 to be the set of vertices such that each vertex in M a

1 (ui) has at least one neighbor of color a in I \ I OUT(D). Formally,

M a

1 (ui) = {uj ∈N di−1(ui)∩M1: Na(uj)∩(I\I OUT(D))̸

= ∅}

The intuition behind the definition of M a

1 (ui) is as follows. In order to satisfy any unsatisfied vertex ui of color a, any solution must include at least one vertex u ∈I\I OUT(D) of color a where u is a neighbor of a vertex in M a

1 (ui). We define the following set system with ground set M1, Ma(D, M1) = {M a

1 (ui)}. Let X∗ a ⊆N(Sa) ∩M1 be the minimal set of vertices such that every vertex in Sa has a neighbor in X∗ a. Observation 1.6. X∗ a must be a minimal hitting set for Ma(D, M1).

Towards finding S∗ a, we make the following final guess:

Guess 3: For each color a, guess the minimal hitting set

Xa ⊆N(Sa) ∩M1. The total number of such choices is bounded by 2k.

14152

<!-- Page 5 -->

Given Xa, consider the set system (I, F(Xa)) where for each vertex ui ∈Xa we include set of vertices N(ui) ∩ (I \ (I IN(D) ∪I OUT(D))) of color a as a subset in the family F(Xa) i.e.

F(Xa) = {N(ui) ∩(I \ (I IN ∪I OUT)) ∩C−1(a): ui ∈Xa}

For any choice Xa, let S(Xa) denotes the minimum hitting set for (I, F(Xa)). Observation 1.7. (S \ Sa) ∪S(Xa) is a solution.

Proof. By construction for any vertex ui ∈U a, d(ui, Sa) ≤ di. Observe that from Lemma 1.5, we know that (S \ Sa) ∪S(Xa) is a solution. Note that Sa is a hitting set for (I, F(Xa)). This completes the proof.

Observation 1.8. Given D and M1, we can find out S∗ a ⊆ I \ I OUT(D) in time 2O(k).

Proof. Observe that there are at most 2k possible choices for Xa. For each choice of Xa, F(Xa) contains at most |Xa| ≤ k sets. Since the HITTING SET problem is solvable in time Poly(n) · 2m with n variables and m sets (By Proposition 1), S∗ a can be found in 2O(k) time.

All the sets {S∗ a | a ∈C(U)} can be found in time at most c·poly(n)·2O(k), leading to O∗(kO(k)) overall running time. Theorem 1.9. MCS is FPT parameterized by vertex cover number, admitting an algorithm running in time O∗(kO(k)), where k is the size of the vertex cover.

MCS Parameterized by Neighborhood

Diversity/Types of Vertices We are given a graph G = (V, E). Let V = F i∈[r] Ti be a neighborhood decomposition of a graph G of minimum size. Note that, ∀i ∈[r], the induced graph G[Ti] is either an independent set or a clique, and for distinct i, j ∈[r], either there is no edge between Ti and Tj (or) all possible edges exist between vertices in Ti and Tj.

CONSISTENT SUBSET PROBLEM PARAMETERIZED BY NEIGHBORHOOD DIVERSITY

Input: A graph G = (V = F i∈[r] Ti, E) where for each u, v ∈Ti, N(u) \ {v} = N(v) \ {u} along with a coloring function C: V (G) →[c]. Question: Compute a minimum consistent subset (MCS) S for (G, C). Parameter: r

We show that MCS is FPT parameterized by neighborhood diversity r. To that end, we prove the following claim, which we use in the correctness proof of our algorithm at the end of this section. Claim 1.10. (†)1 Given a graph G = (V, E) with neighborhood diversity r (i.e., V = F i∈[r] Ti), there is an MCS S for (G, C) such that for each type Ti and for each color j,

1Proofs for Theorems, Lemmas, and Claims marked with † have been moved to the extended version due to space limitations.

the set S has 0, 1 or all the vertices of color j from Ti. Formally, ∀i ∈[r] and ∀j ∈[c], we have |Ti ∩C−1(j) ∩S| ∈ {0, 1, |(Ti ∩C−1(j))|}.

The above claim essentially states that there exists a minimum consistent subset (MCS) that, for each color from any type, includes either 0, 1, or all vertices of that color. With this claim in place, we are now ready to present the first step of our algorithm.

Step 1: Identifying the Nature of Responsible Colors We start by defining partitions and sets of responsible colors with respect to a potential MCS S below. Notice that while we may guess (i.e., generate all possible) partitions required for a desired MCS, generating all sets of responsible colors may not be possible in FPT time. We use a clever approach to bypass the exhaustive generation of responsible color sets, as described at the end of these definitions. Partitions (w.r.t. an MCS S): We begin by guessing a partition T of the r types into 3 sets, namely T0, T1, and T2 with respect to a potential MCS S for (G, C) as follows:

• T0 = {Ti | i ∈[r] and Ti ∩S = ∅} • T1 = {Ti | i ∈[r] and |C(Ti ∩S)| = 1} • T2 = {Ti | i ∈[r] and |C(Ti ∩S)| > 1}

In other words, T0 is the set of types that contain no vertex from S, T1 is the set of types from which all vertices selected into S are of the same color, and T2 is the set of types from which vertices of multiple colors are selected into S. Responsible Colors (w.r.t an MCS S): Given an MCS S and a corresponding 3-partition T, a small inclusion-wiseminimal set of colors R is a set of responsible colors if and only if it satisfies the following.

• For each type Ti ∈T1, R contains the color C(Ti ∩S). • For each type in T2, the set R contains at least two distinct colors from C(Ti ∩S).

Observe that any set of responsible colors has size at most 2r, due to the minimality property. Moreover, any such set is sufficient to determine the partition T of types. And, for a given S, there may exist multiple sets of responsible colors, possibly more than polynomially (in n) many and finding one may not even be possible in FPT time. Nevertheless, let R = {c1,..., ck} denote an arbitrary set of responsible colors for S where k ≤2r. We prove the following property of a set of responsible colors which we use in the final correctness proof of our algorithms. The property is that basically for every vertex v, its closest distance to a solution vertex in S can be determined (same as) by its closest distance to a solution vertex whose color is from the set of responsible colors. Claim 1.11. For a set of responsible colors R of S and an arbitrary vertex v, d(v, S \ (S ∩C−1(C(v)))) = d(v, S ∩ (∪j∈R\C(v)C−1(j))).

Proof. Let z be a vertex in S of a color other than C(v) such that the distance from v to z is minimized over all vertices in S whose colors are different from that of v, i.e.,

14153

<!-- Page 6 -->

d(v, z) = d(v, S \ (S ∩C−1(C(v)))). If z ∈T1, then by definition of T1, we have C(z) ∈R, satisfying the claim. Otherwise, if z ∈Ti for some Ti ∈T2 and C(z) /∈R, then by the definition of responsible colors, there must exist a y ∈S∩Ti of a different color (i.e., C(y) ∈R, C(y)̸ = C(v)). But then, we have d(v, z) = d(v, y), proving the claim.

We reiterate that although we may not be able to decide on an R, we can guess whether the vertices corresponding to the colors in R are included in the solution from each type as described below. Guessing solution occurrences (nature) of colors in R: We guess the solution occurrence of each responsible color c ∈R in each type via a function occ: R →2[r], where occ(c) is the set of types that have vertices in S ∩C−1(c). A valid occurrence function occ must be consistent with the following partitioning requirements consistent with S and T.

• For each type Ti ∈T0, there is no j ∈[k] such that i ∈occ(cj). • For each type Ti ∈T1, there is precisely one j ∈[k] such that i ∈occ(cj). • For each type Ti ∈T2, there are at least two colors cj1, cj2 ∈R such that i ∈occ(cj1) ∩occ(cj2).

At the end of Step 1, we assume that we have correctly fixed a partition T (with respect to a potential MCS S), along with a consistent and valid occurrence function occ for some arbitrary set of responsible colors R (for S).

Graph G Type 1 Type 2 Type 3 Type 4

Label 1 Colors

Label 2 Colors

Label 3 Colors

Label 4 Colors

Label 5 Colors

**Figure 1.** Each disk represents a type in the graph G. Colors are grouped into labels, and each level is indicated by a distinct background color. From each label, a representative color is selected, shown as a point encircled by a circle.

Step 2: Label Coding to Identify a Most Suitable Set of Responsible Colors In this step, we apply a label-coding function that assigns each color in R a distinct label with sufficiently high probability. This allows us to break the problem into simpler subproblems, each of which is structurally easier, solvable in f(r)·nO(1) time, and independent of the others. In each subproblem, we search for the most appropriate color that can assume the role of a responsible color from R. Since the input instance already associates colors with vertices, we use the term “label coding” instead of “color coding” to avoid confusion, although the two are essentially equivalent.

Formally, this step aims to identify a set of actual colors from the input that can take on the roles of the guessed responsible colors, in a manner consistent with the guessed function occ, and compute the smallest possible consistent subset that realizes this correspondence. We proceed as follows. Label Coding: We label-code (Cygan et al. 2015) all the colors using k labels and partition the color set [c] as [c] = C1⊎· · ·⊎Ck, such that with high probability, each responsible color ci of R gets the label i. We call such an event a nice label-coding. Following a nice label-coding, our goal becomes to identify the best responsible (a choice that gives the smallest possible consistent subset) color cjs from each Ci that aligns with the guessed/chosen partitioning constraints and occ function. Caution Constraints: We select the most suitable responsible color for each Ci, where i ∈[k] in the next step. While selecting these most suitable responsible colors independently from each Ci, we impose the following caution constraints to ensure correctness. In our (desired) solution, in each Ci,

C1: There is at least one color (denoted by ci′) that has solution vertices precisely in all types of occ(ci). C2: There is exactly one color ci′ that has solution vertices from any type Tj ∈T1 where Tj ∈occ(ci). C3: There is no color ci′ that has solution vertices from any type in T0 ∪(T1 \ occ(ci)).

These caution constraints together ensure that, in the desired solution we aim to construct, the types corresponding to the selected vertices satisfy the identified (or guessed) partition T.

Step 3: Selection of a Best Responsible Color from Each Label with Caution Constraints

To determine the most suitable responsible color from each Ci and combine them to return an MCS, we crucially exploit the fact that the subproblems of selecting responsible colors from each Ci are independent. At a high level, this independence arises because the partition T, determined by the occurrence function occ over R, essentially fixes, for every vertex, the distance of closest solution vertex of a different color. This, in turn, determines the minimum number of vertices required from that particular color in the solution to ensure consistency for all vertices of the same color. Since both the partition T and the function occ are already fixed, we can compute, for each individual color, the smallest subset of vertices that must be included in a solution, as long as the occ function requirements from Ci and the caution constraints are satisfied. Below we describe the exact procedure along with a formal correctness argument for the same.

For a fixed label Ci, we go over each cj ∈Ci expecting it to be a most suitable responsible color from Ci and compute the size of a smallest set of vertices required to be in the solution for the consistency of all vertices of colors in Ci. First, from occ(ci), we determine the types from which vertices of color cj are to be selected into S. Recall from Claim 1.10, either one or all vertices of color cj for each of

14154

<!-- Page 7 -->

the types in occ(ci) are selected into a potential solution S. Let Oj be the set of all possible subsets of vertices of color cj that may appear in S in accordance with occ(ci). Thus, |Oj| ≤2r. For a fixed o ∈Oj, let n′ j,o (|o|) be the number of vertices of color cj in S and nk,o be the minimum number of vertices of color ck ∈Ci \ {ci} (again we have at most 3k such choices) one has to pick into a solution of color ck adhering to caution constraints while satisfying the consistency requirement of all vertices of color ck and of all the vertices of color cj (with respect to the choice o).

We formally check the consistency requirements as follows (in addition to caution constraints). For a choice o of color cj and any arbitrary subset o′ of color ck (at most 3k many such choices) that are to be selected into a potential solution, we must ensure that:

d(v, o′) ≤min {d(v, Ti) | Ti ∈T1 ∪T2} ∀v of color ck

(1)

d(u, o) ≤d(u, o′) ∀u of color cj. (2)

Equation (1) ensures the consistency requirement for all vertices of color ck, and Equation (2) ensures consistency of all vertices of color cj with respect to color ck. Note that we do not have to worry about the consistency requirements between two colors ck and c′ k; since ensuring that each color is consistent with respect to a responsible set of colors (in (1)) is sufficient for it to be consistent with all the colors, due to Claim 1.11. Let Si be a smallest subset of solution vertices of colors in Ci that satisfy the caution constraints along with the above mentioned consistency requirements, i.e.,

|Si| = min cj∈Ci{min o∈Oj{n′ j,o +

X ck∈Ci\{cj}

nk,o}}

We return S = S i∈k Si as the desired MCS. Before presenting our final algorithm, we provide a correctness proof of the above statement by establishing the independence of the subproblems, specifically, that the selection of the best responsible color from each Ci can be done independently. The following lemma essentially states that the smallest possible set of solution vertices of colors from Ci, satisfying the caution constraints and consistency requirements, can substitute the vertices of the same colors in an MCS without violating consistency of any vertex or increasing the solution size. Lemma 1.12. (†) For any MCS S with partition T, occ, a set of responsible colors R, and following a nice label coding [c] = C1 ⊎· · · ⊎Ck, let Si be a smallest possible set of vertices selected from all the colors in Ci with cj being the responsible color, while adhering to the caution constraints and consistency requirements. S′ = S∩(∪j /∈CiC−1(j))∪Si is also an MCS.

Lemma 1.12 ensures that one can compute each Si of minimum possible size from the corresponding label Ci, independently of the others, and combine them to obtain a desired Minimum Consistent Subset (MCS). A formal algorithm is presented in Algorithm 1. Runtime Analysis: The algorithm branches over 3r partitions (choices for T) and rO(r) possible occ functions, each

## Algorithm

1: MCS parameterized by Neighborhood Diversity

1: Generate all 3-partitions of the types into T0, T1, and T2. 2: Generate all valid occurrence functions occ. 3: for each fixed partition and valid occ do 4: Label-code the colors [c] using k labels (k ≤2r), and partition [c] = C1 ⊎· · · ⊎Ck based on the labels the colors receive. 5: for i = 1 to k do 6: for each cj ∈Ci do 7: Let cj be the responsible color in Ci. 8: for each o ∈Oj do 9: Compute n′ j,o and the corresponding set of vertices (call it S′ j,o). 10: for each ck ∈Ci \ {cj} do 11: Compute nk,o (as described in Step 3) and its vertex set S′ k,o. 12: end for 13: end for 14: Keep track of the S′ j = S′ j,o ∪ (S ck∈Ci\{cj} S′ k,o) which minimizes n′ j,o + P ck∈Ci\{cj} nk,o. 15: end for 16: Si ←arg minS′ j:cj∈Ci |S′ j|. 17: end for 18: Keep track of S ←S i∈[k] Si of minimum cardinality. 19: end for 20: return S.

verifiable in polynomial time. A random labeling yields a nice label-coding with probability at least k−k, and such codings can be enumerated in kO(k) · nO(1) time. For each component Ci and a responsible color cj, there are c ≤n choices, and at most 2r options for |Oj|. For each o ∈Oj, the value n′ j,o can be computed in polynomial time. For each of the non-responsible colors ck, values nk,o can be computed in 3r · poly(n) time by enumerating all S ∩C−1(ck). Thus, the total runtime is 3r · rO(r) · kO(k) · nO(1) · kc · 3r · nO(1) · c · 3r · nO(1) = rO(r) · nO(1), where the final bound follows from k ≤2r and c ≤n.

The randomization step (label-coding) can be derandomized with (n, k)-universal sets (Cygan et al. 2015), while maintaining the same asymptotic running time.

Theorem 1.13. MCS is FPT parameterized by neighborhood diversity, admitting an algorithm running in time O∗(rO(r)), where r is the neighborhood diversity of the input graph.

## Acknowledgments

The first author acknowledges support from the Science and Engineering Research Board (SERB) via the project MTR/2022/000253. The second author would like to thank Akanksha Agrawal (IIT Madras) for formally introducing him to the field of parameterized algorithms, a foundation that helped shape this work.

14155

<!-- Page 8 -->

## References

Arimura, H.; Gima, T.; Kobayashi, Y.; Nochide, H.; and Otachi, Y. 2023. Minimum Consistent Subset for Trees Revisited. CoRR, abs/2305.07259. Banik, A.; Das, S.; Maheshwari, A.; Manna, B.; Nandy, S. C.; M., K. P. K.; Roy, B.; Roy, S.; and Sahu, A. 2024. Minimum Consistent Subset in Trees and Interval Graphs. In Barman, S.; and Lasota, S., eds., 44th IARCS Annual Conference on Foundations of Software Technology and Theoretical Computer Science, FSTTCS 2024, December 16-18, 2024, Gandhinagar, Gujarat, India, volume 323 of LIPIcs, 7:1–7:15. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Biniaz, A.; and Khamsepour, P. 2024. The Minimum Consistent Spanning Subset Problem on Trees. J. Graph Algorithms Appl., 28(1): 81–93. Chitnis, R. 2022. Refined Lower Bounds for Nearest Neighbor Condensation. In Dasgupta, S.; and Haghtalab, N., eds., International Conference on Algorithmic Learning Theory, 29 March - 1 April 2022, Paris, France, volume 167 of Proceedings of Machine Learning Research, 262–281. Cygan, M.; Fomin, F. V.; Kowalik, L.; Lokshtanov, D.; Marx, D.; Pilipczuk, M.; Pilipczuk, M.; and Saurabh, S. 2015. Parameterized Algorithms. Springer. ISBN 978-3- 319-21274-6. Dey, S.; Maheshwari, A.; and Nandy, S. C. 2021. Minimum Consistent Subset Problem for Trees. In Bampis, E.; and Pagourtzis, A., eds., Fundamentals of Computation Theory - 23rd International Symposium, FCT 2021, Athens, Greece, September 12-15, 2021, Proceedings, volume 12867 of Lecture Notes in Computer Science, 204–216. Springer. Dey, S.; Maheshwari, A.; and Nandy, S. C. 2023. Minimum consistent subset of simple graph classes. Discret. Appl. Math., 338: 255–277. Diestel, R. 2012. Graph Theory, 4th Edition, volume 173 of Graduate texts in mathematics. Springer. ISBN 978-3-642- 14278-9. Hart, P. E. 1968. The condensed nearest neighbor rule (Corresp.). IEEE Transactions on Information Theory, 14(3): 515–516. Khodamoradi, K.; Krishnamurti, R.; and Roy, B. 2018. Consistent Subset Problem with Two Labels. In Panda, B. S.; and Goswami, P. P., eds., Algorithms and Discrete Applied Mathematics - 4th International Conference, CAL- DAM 2018, Guwahati, India, February 15-17, 2018, Proceedings, volume 10743 of Lecture Notes in Computer Science, 131–142. Springer. Lampis, M. 2012. Algorithmic Meta-theorems for Restrictions of Treewidth. Algorithmica, 64(1): 19–37. Manna, B. 2024a. Minimum Consistent Subset in Interval Graphs and Circle Graphs. CoRR, abs/2405.14493. Manna, B. 2024b. Minimum Strict Consistent Subset in Paths, Spiders, Combs and Trees. CoRR, abs/2405.18569. Matsumoto, N.; Kurita, K.; and Kiyomi, M. 2025. Space- Efficient FPT Algorithms for Degeneracy. IEICE Trans. Inf. Syst., 108(3): 208–213.

Wilfong, G. 1991. Nearest Neighbor Problems. In Proceedings of the Seventh Annual Symposium on Computational Geometry, SCG ’91, 224–233.

14156
