---
title: "Which Algorithms Can Graph Neural Networks Learn?"
source_url: https://icml.cc/virtual/2026/oral/71194
paper_pdf_url: https://arxiv.org/pdf/2602.13106v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Which Algorithms Can Graph Neural Networks Learn?

<!-- Page 1 -->

Which Algorithms Can Graph Neural

Networks Learn?

Solveig Wittig∗1, Antonis Vasileiou∗1, Robert R. Nerem∗2, Timo Stoll1,

Floris Geerts3, Yusu Wang2, and Christopher Morris1

1RWTH Aachen University 2University of California San Diego 3University of Antwerp

In recent years, there has been growing interest in understanding neural architectures’ ability to learn to execute discrete algorithms, a line of work often referred to as neural algorithmic reasoning. The goal is to integrate algorithmic reasoning capabilities into larger neural pipelines. Many such architectures are based on (message-passing) graph neural networks (MPNNs), owing to their permutation equivariance and ability to deal with sparsity and variable-sized inputs. However, existing work is either largely empirical and lacks formal guarantees or it focuses solely on expressivity, leaving open the question of when and how such architectures generalize beyond a finite training set. In this work, we propose a general theoretical framework that characterizes the sufficient conditions under which MPNNs can learn an algorithm from a training set of small instances and provably approximate its behavior on inputs of arbitrary size. Our framework applies to a broad class of algorithms, including single-source shortest paths, minimum spanning trees, and general dynamic programming problems, such as the 0-1 knapsack problem. In addition, we establish impossibility results for a wide range of algorithmic tasks, showing that standard MPNNs cannot learn them, and we derive more expressive MPNN-like architectures that overcome these limitations. Finally, we refine our analysis for the Bellman–Ford algorithm, yielding a substantially smaller required training set and significantly extending the recent work of Nerem et al. [2025] by allowing for a differentiable regularization loss. Empirical results largely support our theoretical findings.

Contents

1. Introduction 2 1.1. Related work..................................... 3

∗These authors contributed equally.

arXiv:2602.13106v1 [cs.LG] 13 Feb 2026

<!-- Page 2 -->

2. Background 6 2.1. Metric spaces and covering numbers........................ 7 2.2. Message-passing graph neural networks...................... 8 2.3. The 1-dimensional Weisfeiler–Leman algorithm and variants........... 9 2.4. Separation and approximation abilities of MPNNs................ 10 2.5. Feedforward neural networks............................ 11 2.6. Considered graph problems............................. 12

3. What and how can GNNs learn 13 3.1. Regularization-induced extrapolation........................ 13 3.2. Finite Lipschitzness in MPNNs........................... 15 3.2.1. Algorithms within a finite Lipschitz class................. 16 3.3. Improved learning guarantees for SSSPs algorithms................ 17

4. What GNNs cannot learn 18 4.1. Expressivity limitations............................... 18 4.2. Expressible but (possibly) not learnable invariants................ 19

## 5. Limitations and future directions 19

## 6. Experimental study 20

## 7. Conclusion 22

## Bibliography

22

## Appendix

30

## 1. Introduction

Graph neural networks (GNNs), and in particular message-passing graph neural networks (MPNNs), constitute a versatile and expressive class of neural architectures for learning over graph-structured data [Gilmer et al., 2017, Scarselli et al., 2009]. Their permutation equivariance and ability to operate on sparse and variable-sized inputs have made them a central tool across a wide range of applications, spanning drug design [Wong et al., 2023], global medium-range weather forecasting [Lam et al., 2023], and combinatorial optimization [Cappart et al., 2023, Gasse et al., 2019, Qian et al., 2024, Scavuzzo et al., 2024].

Recently, MPNNs have played a central role in neural algorithmic reasoning (NAR), a research direction that seeks to bridge classical algorithm design and neural computation [Cappart et al., 2023, Velickovic and Blundell, 2021, Xu et al., 2020]. The goal of NAR is to enable neural networks to learn, execute, and generalize discrete algorithms, thereby seamlessly integrating algorithmic reasoning into end-to-end trainable neural pipelines. Due to their close correspondence with iterative, local graph computation, MPNNs have emerged as a natural architectural backbone for learning graph algorithms such as shortest paths, minimum spanning trees, and dynamic programming procedures [Velickovic et al., 2020].

Despite substantial empirical progress, existing results on neural algorithmic reasoning remain theoretically limited. Most prior work is either purely empirical, demonstrating performance on benchmark instances without formal guarantees, or focuses on existential expressivity questions,

<!-- Page 3 -->

characterizing which algorithms can in principle be represented by a given architecture, e.g., Azizian and Lelarge [2021], Chen et al. [2020], He and Vitercik [2025], Loukas [2020], Morris et al. [2019], Pellizzoni et al. [2025], Xu et al. [2019], with a recent focus on transformer architectures, e.g., de Luca and Fountoulakis [2024], de Luca et al. [2025], Merrill and Sabharwal [2025], Sanford et al. [2024,], Yehudai et al. [2025], Zhou et al. [2024]. Such analyses typically abstract away the learning process and provide little insight into sample efficiency or generalization beyond the training distribution. As a consequence, they do not explain when learned models provably generalize to larger or structurally different graphs, a property that is essential for meaningful algorithmic deployment.

A notable recent exception is the work of Nerem et al. [2025], which provides theoretical guarantees for learning graph algorithms with MPNNs. However, their analysis is restricted to a single algorithm (i.e., Bellman–Ford) and enforces correctness via a non-differentiable regularization term. These assumptions limit the applicability of the results to broader classes of algorithms and to standard gradient-based learning pipelines.

Present work In this work, we develop a general theoretical framework for learning algorithms with MPNNs that addresses these limitations. We characterize sufficient conditions under which an MPNN trained on a small set of instances can provably generalize to inputs of arbitrary size, covering a broad class of graph algorithms while remaining compatible with fully differentiable training objectives. Our framework clarifies which algorithms MPNNs can learn from finite data and which they cannot learn. Concretely, our contributions are as follows.

1. We introduce a theoretical framework characterizing when standard MPNNs (or more expressive MPNNs) can learn the cost function of graph algorithms, uniformly over graphs of arbitrary size, from finite data by minimizing an empirical loss; see Section 3.

2. Using this framework, we identify conditions under which GNNs can learn standard graph algorithms, including single-source shortest-path, minimum spanning tree, and dynamic programming algorithms.

3. For single-source shortest-path, we propose a differentiable ℓ1-regularization term that reduces required training data by balancing empirical risk minimization with regularization to enforce a sparsity pattern; see Section 3.3.

4. We empirically validate that these insights translate into practice, underscoring the role of training data and the proposed regularization; see Section 6.

Taken together, our framework provides a precise characterization of which algorithms standard and more expressive MPNNs can learn, enabling a more principled understanding of the capabilities and limitations of MPNN-based, data-driven algorithmic design.

## 1.1. Related work

In the following, we discuss related work.

MPNNs MPNNs [Gilmer et al., 2017, Scarselli et al., 2009] have emerged as the most prominent graph machine learning architecture. Notable instances of this architecture include, e.g., Duvenaud et al. [2015], Hamilton et al. [2017], Kipf and Welling [2017] and Veličković et al. [2018], which can be subsumed under the message-passing framework introduced in Gilmer et al.

<!-- Page 4 -->

[2017]. In parallel, approaches based on spectral information were introduced in, e.g., Bruna et al. [2014], Defferrard et al. [2016], Gama et al. [2019], Kipf and Welling [2017], Levie et al. [2019], and Monti et al. [2017]—all of which descend from early work in Baskin et al. [1997], Goller and Küchler [1996], Kireev [1995], Merkwirth and Lengauer [2005], Micheli and Sestito [2005], Micheli [2009], Scarselli et al. [2009], and Sperduti and Starita [1997].

Expressivity of MPNNs The expressivity of an MPNN is the architecture’s ability to express or approximate different functions over a set of graphs. High expressivity means the neural network can represent many functions over this domain. In the literature, the expressivity of MPNNs is modeled mathematically using two main approaches, i.e., separation power compared to graph isomorphism test Morris [2021] and universal approximation theorems Azizian and Lelarge [2021], Geerts and Reutter [2022]. Works following the first approach study if an MPNN, by choosing appropriate parameters, can distinguish the same pairs of non-isomorphic graphs with a given graph isomorphism test. The most commonly used graph isomorphism test for analyzing the expressive power of MPNNs is the 1-dimensional Weisfeiler–Leman algorithm (1-WL), a well-studied heuristic for the graph isomorphism problem, and its more expressive variants [Cai et al., 1992, Weisfeiler and Leman, 1968, Weisfeiler, 1976]. Here, an MPNN distinguishes two non-isomorphic graphs if it can compute different vectorial representations for the two graphs. Specifically, Morris et al. [2019] and Xu et al. [2019] showed that the 1-WL limits the expressive power of any possible MPNN architecture in distinguishing non-isomorphic graphs. In turn, these results have been generalized to the k-dimensional Weisfeiler–Leman algorithm, e.g., Azizian and Lelarge [2021], Geerts [2020], Maron et al. [2019], Morris et al. [2019, 2020, 2022] and (ordered) subgraph GNNs Bevilacqua et al. [2022], Cotta et al. [2021], Li et al. [2020], Qian et al. [2022], Zhang et al. [2023]. Works following the second approach study, which functions can be approximated over the set of graphs arbitrarily closely by an MPNN [Azizian and Lelarge, 2021, Böker et al., 2023, Chen et al., 2019, Geerts and Reutter, 2022, Maehara and NT, 2019].

Generalization abilities of MPNNs Early work by Scarselli et al. [2018], building on classical learning theory [Karpinski and Macintyre, 1997, Vapnik, 1995], bounded the Vapnik– Chervonenkis theory dimension of MPNNs with piecewise polynomial activations on fixed graphs by O(P 2n log n), where P is the number of parameters and n the graph’s order; see also Hammer [2001]. However, their MPNN model differs from modern architectures [Gilmer et al., 2017, D’Inverno et al., 2024]. Garg et al. [2020] bounded the empirical Rademacher complexity of a simple sum-aggregation MPNN in terms of graph degree, depth, Lipschitz constants, and parameter norms, assuming weight sharing. This line was extended to E(n)-equivariant MPNNs by Karczewski et al. [2024] and refined via PAC-Bayesian analyses by Liao et al. [2021], Ju et al. [2023]; see also Lee et al. [2024] for knowledge graphs. Morris et al. [2023] connected MPNNs’ expressivity and generalization via the Vapnik–Chervonenkis theory, showing that VC dimension depends on the number of 1-WL equivalence classes, logarithmically on the number of colors, and polynomially on the number of parameters. Their discrete pseudo-metric assumption was extended by Pellizzoni et al. [2024], who studied vertex-individualized MPNNs using covering numbers, though without explicit metric bounds. Related refinements include VC lower bounds for restricted MPNNs [Daniëls and Geerts, 2024], margin-based analyses [Franks et al., 2024, Li et al., 2024, Chuang et al., 2021], and more expressive MPNNs [Franks et al., 2024, Maskey et al., 2025]. Several works analyze generalization under structural assumptions.

<!-- Page 5 -->

Maskey et al. [2022, 2024], Wang et al. [2025] considered random graph models, while Levie [2023], Rauchwerger et al. [2024], Vasileiou et al. [2024] derived bounds using covering numbers. Transductive generalization was studied via algorithmic stability [Verma and Zhang, 2019] and Rademacher complexity under stochastic block models [Esser et al., 2021, Tang and Liu, 2023]. For semi-supervised vertex classification, Baranwal et al. [2021] analyzed MPNNs on mixtures of Gaussians over stochastic block models. Importantly, the above work analyzed MPNNs’ generalization ability in the classical uniform convergence regime. In contrast, the present work examines the generalization of a single function to larger graphs than those seen during training. Yehudai et al. [2021] derived negative generalization results for larger graphs than those seen in the training set, while Levin et al. [2025] derived necessary conditions of generalization to larger graphs. See Vasileiou et al. [2024] for a survey on generalization analyses of MPNNs and related architectures.

Empirical work on NAR on graphs A large body of empirical work studies NAR for graphs problems [Velickovic and Blundell, 2021, Cappart et al., 2023]. Early empirical studies demonstrated that neural architectures can imitate algorithmic execution when trained on intermediate computation traces [Velickovic et al., 2020]. MPNNs have emerged as a particularly effective backbone for NAR on graph-structured problems due to their close correspondence with local, iterative graph computations [Cappart et al., 2023]. Empirical results show that MPNNs can learn graph algorithms such as single-source shortest paths, breadth-first search, minimum spanning trees, and dynamic programming [Pándy et al., 2022, Velickovic et al., 2020, Yonetani et al., 2021]. Subsequent work investigated architectural refinements and training strategies to improve stability and generalization, e.g., [Grötschla et al., 2022, Ibarz et al., 2022, Jain et al., 2023, Jürß et al., 2023, Numeroso et al., 2023, Rodionov and Prokhorenkova, 2025, Xhonneux et al., 2021]. Surveys [Cappart et al., 2023] and benchmark studies [Velickovic et al., 2022] further systematized these empirical findings and highlighted both the potential and limitations of machine-learning enhanced approaches to algorithmic reasoning and combinatorial optimization.

Theoretical work on algorithmic reasoning on graphs There is a substantial body of work studying the expressive capabilities of message-passing neural networks (MPNNs) and related architectures for representing graph algorithms. For example, Loukas [2020] studied the depth and width requirements of MPNNs for solving problems such as minimum vertex cover, leveraging results from distributed computing. Xu et al. [2019], Morris et al. [2019] showed that MPNNs are inherently limited by the 1-WLin their ability to distinguish non-isomorphic graphs. Qian et al. [2024] demonstrated that MPNNs can express each step of the primal–dual interiorpoint method for solving linear optimization problems, while Yau et al. [2024] investigated their ability to represent approximation algorithms for hard combinatorial problems such as maximum cut and minimum vertex cover; see also Sato et al. [2019]. Dudzik and Velickovic [2022] used category-theoretic tools to establish a connection between MPNNs and dynamic programming. Hertrich and Skutella [2023], Hertrich and Sering [2025] studied the size requirements of recurrent neural networks for solving knapsack and maximum-flow problems. More recently, Rosenbluth and Grohe [2025] devised a general framework for understanding the ability of recurrent MPNNs to simulate algorithms on arbitrarily large instances, and He and Vitercik [2025] showed that MPNNs can simulate classical primal–dual approximation schemes. In addition, several works have begun to study the ability of transformer architectures to simulate (graph) algorithms,

<!-- Page 6 -->

e.g., de Luca and Fountoulakis [2024], de Luca et al. [2025], Merrill and Sabharwal [2025], Sanford et al. [2024,], Yehudai et al. [2025], Zhou et al. [2024]. Overall, these works primarily focus on expressivity, largely ignoring questions related to learning and optimization.

Xu et al. [2020] addressed this gap by proposing PAC-style sample-complexity bounds for learning common (graph) algorithms with MPNNs, showing how architectural alignment with the target algorithm can improve sample efficiency. Nerem et al. [2025] demonstrated that MPNNs trained on small datasets, equipped with a regularization term, and optimized to a sufficiently small loss can execute the Bellman–Ford algorithm on arbitrarily large graphs. However, their analysis crucially relies on a non-differentiable regularization term.

## 2. Background

In the following sections, we introduce the notation and provide the necessary background.

Basic notations Let N:= {1,2,... }, N0:= N ∪{0}, R+ denote the non-negative reals, and R>0 the positive reals. For n ∈N, let [n]:= {1,..., n} and [n]0:= {0,1,..., n}. We use {{...}} to denote multisets. For non-empty sets X, Y, let Y X be the set of functions X →Y. For A ⊂X, let 1A: X →{0,1} be the indicator function. For a matrix M ∈Rn×m, Mi,· and M·,j denote its ith row and jth column. The symbol 0 denotes an all-zero vector of appropriate dimension. Functions are applied to sets, multisets, and matrices element-wise. For x ∈Rn, define ∥x∥2:= (Pn i=1 x2 i)1/2 and ∥x∥∞:= maxi∈[n] |xi|. For M ∈Rn×m, define the Frobenius norm ∥M∥F:= (P i,j M2 ij)1/2, the operator norm ∥M∥2:= supx̸=0 ∥Mx∥2/∥x∥2, and ∥M∥∞:= maxi∈[n]

Pm j=1 |Mij|.

Graphs An (undirected) graph G is a pair (V (G), E(G)) with finite sets of vertices V (G) and edges E(G) ⊆{{u, v} ⊆V (G) | u̸ = v}. vertices or vertices V (G) and edges E(G) ⊆ {{u, v} ⊆V (G) | u̸ = v}. The order of a graph G is its number |V (G)| of vertices. We call G an n-order graph if G has order n. In a directed graph, we define E(G) ⊆V (G)2, where each edge (u, v) has a direction from u to v. Given a directed graph G and vertices u, v ∈V (G), we say that v is a child of u if (u, v) ∈E(G). For a graph G and an edge e ∈E(G), we denote by G \ e the graph induced by removing the edge e from G. For an n-order graph G, assuming V (G) = [n], we denote its adjacency matrix by A(G) ∈{0,1}n×n, where A(G)vw = 1 if, and only, if {v, w} ∈E(G). The neighborhood of a vertex v ∈V (G) is denoted by NG(v):= {u ∈V (G) | {v, u} ∈E(G)}, where we usually omit the subscript for ease of notation.

An attributed graph is a pair (G, aG) with a graph G = (V (G), E(G)) and a (vertex-)attribute function aG: V (G) →Rd, for d > 0. The attribute or feature of v ∈V (G) is aG(v). Similarly, we consider graphs equipped with edge features. An edge-featured graph is a pair (G, wG), where G = (V (G), E(G)) is a graph and wG: E(G) →Rd assigns a (possibly vector-valued) feature to each edge. For an edge e ∈E(G), the vector wG(e) is referred to as the edge feature of e. The special case p = 1 with wG(e) ∈R+ for all e ∈E(G) corresponds to an edge-weighted graph, in which case wG(e) is called the (edge) weight of e. When the underlying graph is clear from the context, we simply write w(e) or we to denote the edge feature of e ∈E(G).

For a graph G without edge features, the degree of a vertex u ∈V (G) is defined as degG(u):= |NG(u)|. For an edge-weighted graph (G, wG), the weighted degree of u ∈V (G) is given by

<!-- Page 7 -->

degG(u):= P v∈NG(u) wG(u, v). When the underlying graph is clear from the context, we omit the subscript G and simply write degree(u).

Let G be graph, a path P on G of length k is a sequence of vertices (v0, v1, v2,..., vk) such that for i ∈[k], it holds that (vi−1, vi) ∈E(G). We denote the set of paths between vertices v, w ∈V (G) by PG(v, w). A graph is connected if P(v, w)̸ = ∅, for all v, w ∈V (G). A graph G is a tree if it is connected, but G \ e is disconnected for any e ∈E(G). A tree or a disjoint collection of trees is known as a forest.

A rooted tree (G, r) is a tree where a specific vertex r is marked as the root. For a rooted (undirected) tree, we can define an implicit direction on all edges as pointing away from the root; thus, when we refer to the children of a vertex u in a rooted tree, we implicitly consider this directed structure. For S ⊆V (G), the graph G[S]:= (S, ES) is the subgraph induced by S, where ES:= {(u, v) ∈E(G) | u, v ∈S}. A (vertex-)labeled graph is a pair (G, ℓG) with a graph G = (V (G), E(G)) and a (vertex-)label function ℓG: V (G) →Σ, where Σ is an arbitrary countable label set. For a vertex v ∈V (G), ℓG(v) denotes its label.

Two graphs G and H are isomorphic if there exists a bijection φ: V (G) →V (H) that preserves adjacency, i.e., (u, v) ∈E(G) if and only if (φ(u), φ(v)) ∈E(H). The bijection φ is called an isomorphism. In the case of attributed graphs, we additionally require aG(v) = aH(φ(v)), for v ∈V (G), and similarly for edge-labeled graphs.

For a graph class G and k ∈N, let Vk(G):= {(G, v) | G ∈G, v ∈V (G)k}, and set V0(G):= G. Then, for k ≥1, and (G, v), (H, w) ∈Vk(G), we say that (G, v), and (H, w) are isomorphic if there exists an isomorphism φ: V (G) →V (H) with φ(v) = w, applied componentwisely.

Given two graphs G and H with disjoint vertex sets, we denote their disjoint union by G ˙∪H.

Invariants Let G be a set of graphs, a graph-level invariant (regarding G) is a function h: G →Rd, d > 0 such that h(G) = h(H), for G and H being isomorphic. In addition, for k > 0, a k-tuple invariant is a function h: Vk(G) →Rd, such that h(G, v) = h(H, w) whenever (G, v) and (H, w) are isomorphic. For k = 0, this recovers the notion of a graph invariant.

## 2.1. Metric spaces and covering numbers

Here, we define pseudo-metric spaces, continuity assumptions, covering numbers, and partitions, which play an essential role in the following.

Metric spaces In the remainder of the paper, “distances” between graphs play an essential role, which we make precise by defining a pseudo-metric (on the set of graphs). Let X be a set equipped with a pseudo-metric d: X × X →R+, i.e., d is a function satisfying d(x, x) = 0 and d(x, y) = d(y, x) for x, y ∈X, and d(x, y) ≤d(x, z) + d(z, y), for x, y, z ∈X. The latter property is called the triangle inequality. The pair (X, d) is called a pseudo-metric space. For (X, d) to be a metric space, d additionally needs to satisfy d(x, y) = 0 ⇒x = y, for x, y ∈X.1

Lipschitz continuity on metric spaces Let (X, dX) and (Y, dY) be two pseudo-metric spaces. A function f: X →Y is called cf-Lipschitz continuous, for cf ∈R>0, if, for x, x′ ∈X, dY(f(x), f(x′)) ≤cf · dX (x, x′).

1Observe that computing a metric on the set of graphs G up to isomorphism is at least as hard as solving the graph isomorphism problem on G.

<!-- Page 8 -->

Covering numbers Let (X, d) be a pseudo-metric space. Given an ε > 0, an ε-cover of X is a subset C ⊆X such that for all elements x ∈X there is an element y ∈C such that d(x, y) ≤ε. Given ε > 0 and a pseudo-metric d on the set X, we define the covering number of X,

N(X, d, ε):= min{m | ∃an ε-cover of X of cardinality m}, i.e., the smallest number m such that there exists a ε-cover of cardinality m of the set X with regard to the pseudo-metric d.

## 2.2. Message-passing graph neural networks

One particular, well-known class of graph machine learning architectures is MPNNs. MPNNs learn a d-dimensional real-valued vector of each vertex in a graph by aggregating information from neighboring vertices. Following Gilmer et al. [2017], let (G, aG, wG) be an attributed, edge-weighted graph with initial vertex feature h(0)

v:= aG(v) ∈Rd0, d0 ∈N, for v ∈V (G). An L-layer MPNN architecture consists of a composition of L neural network layers for some L > 0. In each layer, t ∈N, we compute a vertex feature h(t)

v:= UPD(t)

ut h(t−1)

v, AGG(t)

at

{{(h(t−1)

v, h(t−1)

u, wG(v, u)) | u ∈N(v)}}

∈Rdt, (1)

dt ∈N, for v ∈V (G), where UPD(t)

ut and AGG(t)

at are functions, parameterized by ut ∈Ut and at ∈At, e.g., neural networks, with Ut and At being sets of parameters, e.g., Rd. In the case of graph-level tasks, e.g., graph classification, one also uses a readout, where hG:= READOUTr

{{h(L)

v | v ∈V (G)}}

∈Rd, (2)

to compute a single vectorial representation based on learned vertex features after iteration L. Again, READOUTr is a a parameterized function, for r in some parameter set R. Throughout the paper, we consider a variety of MPNN architectures; all of them can be viewed as special cases of the general MPNN formulation introduced above. We distinguish between vertex- and graph-level MPNNs, i.e., the former compute a feature for each vertex in a given graph while the latter compute a single feature for the whole graph.

Vertex-level and graph-level MPNN classes Since Equation (1) and Equation (2) are parametrized functions, we can define function classes of MPNNs that operate at the vertex and graph levels. Let Gn be a set of n-order graphs, and let L > 0, d > 0. Furthermore, let SL:= (UPD(1)

·, AGG(1)

·,..., UPD(L)

·, AGG(L)

·) be a sequence of parameterized functions following Equation (1) and PL:= (U1, A1,..., UL, AL) be a corresponding sets of parameters. We then define

MPNNPL

(SL,d,n)(Gn):= n h: V1(Gn) →Rn×d h(G)v = h(t)

v, G ∈X, where ut ∈Ut, at ∈At o

.

We call such a set of functions a vertex-level MPNN class. Similarly, let TL:= (UPD(1)

·, AGG(1)

·,..., UPD(L)

·, AGG(L)

·, READOUT·) be a sequence of parameterized functions following Equations (1) and (2) and QL:= (U1, A1,..., UL, AL, R) be a corresponding set of parameters. We then define

MPNNQL

(TL,d)(Gn):= n h: Gn →R h(G):= hG, G ∈Gn, where ut ∈Ut, at ∈At, and r ∈R o

.

We call such a set of functions a graph-level MPNN class. We call a concrete choice of parameters, e.g., ((ut, at)t∈[L], r) of an graph-level MPNN architecture parametrization.

<!-- Page 9 -->

## 2.3 The 1-dimensional

Weisfeiler–Leman algorithm and variants

Here, we introduce the 1-dimensional Weisfeiler–Leman algorithm and some variants.

The 1-dimensional Weisfeiler–Leman algorithm The 1-dimensional Weisfeiler–Leman algorithm (1-WL) or color refinement is a well-studied heuristic for the graph isomorphism problem, originally proposed by Weisfeiler and Leman [1968].2 Intuitively, the algorithm determines if two graphs are non-isomorphic by iteratively coloring or labeling vertices. Given an initial coloring or labeling of the vertices of both graphs, e.g., their degree or application-specific information, in each iteration, two vertices with the same label get different labels if the number of identically labeled neighbors is unequal. These labels induce a vertex partition, and the algorithm terminates when, after some iteration, the algorithm does not refine the current partition, i.e., when a stable coloring or stable partition is obtained. Then, if the number of vertices with a specific label differs between the two graphs, we can conclude that the graphs are not isomorphic. It is easy to see that the algorithm cannot distinguish all non-isomorphic graphs [Cai et al., 1992]. However, it is a powerful heuristic that can successfully decide isomorphism for a broad class of graphs [Arvind et al., 2015, Babai and Kucera, 1979].

In the following, we formally describe a variant of the 1-WL that also considers edge weights. Formally, let (G, ℓG) be a labeled graph and let wG: E(G) →R be an edge-weight function for G. In each iteration, t > 0, the 1-WL computes a vertex coloring C1 t: V (G) →N, depending on the coloring of the neighbors and the weights of the incident edges. That is, in iteration t > 0, we set

C1 t (v):= RELABEL

C1 t−1(v), {{(C1 t−1(u), wG(u, v)) | u ∈N(v)}}

, for vertex v ∈V (G), where RELABEL injectively maps the above pair to a unique natural number, which has not been used in previous iterations. In iteration 0, the coloring C1

0:= ℓG is used.3 To test whether two graphs G and H are non-isomorphic, we run the above algorithm in “parallel” on both graphs. If the two graphs have a different number of vertices colored c ∈N at some iteration, the 1-WL distinguishes the graphs as non-isomorphic. Moreover, if the number of colors between two iterations, t and (t + 1), does not change, i.e., the cardinalities of the images of C1 t and C1 i+t are equal, or, equivalently,

C1 t (v) = C1 t (w) ⇐⇒C1 t+1(v) = C1 t+1(w), for all vertices v, w ∈V (G ˙∪H), then the algorithm terminates. For such t, we define the stable coloring C1

∞(v) = C1 t (v), for v ∈V (G ˙∪H). The stable coloring is reached after at most max{|V (G)|, |V (H)|} iterations [Grohe, 2017].

It is straightforward to show that the 1-WL has limited expressivity in distinguishing pairs of non-isomorphic graphs. Hence, in the following, we derive two more expressive variants that allow us to characterize the needed expressivity to capture well-known graph algorithms.

The 1-dimensional Weisfeiler–Leman algorithm on individualized graphs We consider the 1-WL on individualized graphs, i.e., graphs equipped with a distinguished vertex. Intuitively,

2Strictly speaking, the 1-WL and color refinement are two different algorithms. That is, the 1-WL considers neighbors and non-neighbors to update the coloring, resulting in a slightly higher expressive power when distinguishing vertices in a given graph; see Grohe [2021] for details. Following the conventions in the machine learning literature, we treat both algorithms as equivalent.

3Here, we implicitly assume an injective function from Σ to N.

<!-- Page 10 -->

given a root vertex r, we individualize r by assigning it a unique initial label and then run the 1-WL. Formally, let (G, wG) be an edge-weighted graph with uniform vertex labels ℓG, and let r ∈V (G). We define initial labels by setting ℓG(r):= [∗], where [∗] is a label not used for any other vertex. Then, for each iteration t > 0, the algorithm computes a coloring C1,r t: V (G) →N by the usual 1-WL update rule, i.e., C1,r t is obtained from C1,r t−1 by aggregating the multiset of neighbor colors together with the incident edge weights, exactly as in Section 2. Equivalently, C1,r

0 is the coloring induced by ℓG with r labeled [∗]. For two edge-weighted graphs (G, wG) and (H, wH) with individualized vertices v ∈V (G) and w ∈V (H), we say that 1-WL distinguishes the (individualized) graphs (G, v) and (H, w) if, when running the above refinement in parallel on (G, v) and (H, w), the resulting color multisets differ at some iteration (analogously to the usual 1-WL notion of distinction). We write 1-iWL when 1-WL is used on individualized graphs.

The 1.1-dimensional Weisfeiler–Leman algorithm The 1.1-dimensional Weisfeiler–Leman algorithm ((1,1)-WL) [Rattan and Seppelt, 2023, Qian et al., 2024] can be seen as an extension of the 1-iWL, which tries every possible placement for the unique label [∗] and runs the 1-iWL in parallel on the disjoint union of these individualized graphs. Formally, the (1,1)-WL does not distinguish a pair of graphs (G, H) if there exists a bijection π: V (G) →V (H) such that, for v ∈V (G), running the 1-iWL in “parallel” on G, with v individualized, and H, with π(v) individualized, does not distinguish between the two graphs.

Observe that we can define 1-tuple or graph-level invariants based on these 1-WL variants.

## 2.4. Separation and approximation abilities of MPNNs

Morris et al. [2019] and Xu et al. [2019] established that the graph-distinguishing power of any MPNN architecture is upper bounded by the 1-WL. Moreover, for MPNNs with sum aggregation, Morris et al. [2019] showed that, on any finite set of graphs, suitable parameter choices yield expressivity matching that of 1-WL; see Grohe [2021] and Morris et al. [2023] for further discussion. Analogous statements can be lifted to the 1-iWL and (1,1)-WL settings.

To formalize distinguishability, following Azizian and Lelarge [2021] we express the ability of a function class to distinguish graphs via an induced equivalence relation. Let G be a set of graphs, and let F be a class of functions f: G →D for some domain D. We define the equivalence relation ρG(F) on G by

(G, H) ∈ρG(F) ⇐⇒f(G) = f(H), for all f ∈F.

In case (G, H) ∈ρG(F), we say that F cannot distinguish G and H. If F = {f} is a singleton, we write ρ(f) instead of ρ({f}).

We extend the definition to k-tuple invariants as follows. For a given k ∈N and for a class F of functions f: Vk(G) →D, for some domain D, define the equivalence relation ρVk(G)(F) on Vk(G) by

(G, v, H, w) ∈ρVk(G)(F) ⇐⇒f(G, v) = f(H, w) for all f ∈F

We can now rephrase the various notions of distinguishability from Section 2.3, as follows. Let

<!-- Page 11 -->

G be a set of graphs, then ρV1(G)(1-WL):=

(G, v, H, w) ∈(V1(G))2 | C1

∞(v) = C1

∞(w)

, ρG(1-WL):=

(G, H) ∈G2 | ∃π: V (G) →V (H),

∀v ∈V (G): (G, v, H, π(v)) ∈ρV1(G)(1-WL)

, ρV2(G)(1-iWL):=

(G, (r, v), H, (s, w)) ∈(V2(G))2 | C1.5,r

∞ (v) = C1.5,s

∞ (w)

, ρV1(G)(1-iWL):=

(G, r, H, s) ∈(V1(G))2 | ∃π: V (G) →V (H), ∀v ∈V (G),

(G, (r, v), H, (s, π(v))) ∈ρV2(G)(1-iWL)

, ρG((1,1)-WL):=

(G, H) ∈G2 | ∃π: V (G) →V (H), ∀v ∈V (G), (G, v, H, π(v)) ∈ρV1(G)(1-iWL)

, where π: V (G) →V (H) denotes a bijection. We remark that for 1-iWL, we interpret an element (G, v) ∈V1(G) as graphs G ∈G in which v is individualized.

Given any alg ∈{1-WL,1-iWL,(1,1)-WL} and class of functions F: Vk(G) →D for some k ∈N and domain D, we say that F is alg-simulating if and only if ρVk(G)(F) = ρVk(G)(alg).

That is, the distinguishing power of F is precisely that of alg. With this notation, the expressiveness result from Morris et al. [2019] can be stated as ρG(MPNN) = ρG(1-WL) and ρV1(G)(MPNN) = ρV1(G)(1-WL), where we abuse notation and let MPNN denote both the class of all graph-level MPNNs (for ρG(MPNN)) and the class of all vertex-level MPNNs (for ρV1(G)(MPNN)), see also Section 2.2. As noted above, one can similarly verify the existence of MPNN variants that are 1-iWL-simulating (at rooted/tuple-level) and (1,1)-WL-simulating (at graph-level).

Finally, Azizian and Lelarge [2021] and Geerts and Reutter [2022] showed that, under mild regularity assumptions, separation entails approximation. We remark that these approximations require fixing the order of the underlying graphs and restricting the features to a compact domain.

Proposition 1. Let G be the set of attributed graphs with n vertices and vertex/edge attributes taking values in a compact set of Rd. Let alg ∈{1-WL,1-iWL,(1,1)-WL}, and let g: Vk(G) →R be a k-tuple invariant such that ρVk(G)(alg) ⊆ρVk(G)(g). Assuming standard technical conditions on a class of MPNNs that simulates ρVk(G)(alg), for every ϵ > 0, there exists an MPNN m such that sup (G,v)∈Vk(G)

|g(G, v) −m(G, v)| < ϵ.

In other words, whenever an invariant alg has enough information to distinguish everything that matters for the function g of interest, an alg-simulating class of MPNNs can approximate g arbitrarily well. We refer to Section F.1 for details.

## 2.5. Feedforward neural networks

In the following, we formally introduce feed-forward neural networks. Let J ∈N and (d0,..., dJ) ∈NJ+1. Given weights W = (W 1,..., W J) ∈QJ i=1 Rdi×di−1 =: ΘW, biases

<!-- Page 12 -->

B = (b1,..., bJ) ∈QJ i=1 Rdi =: Θb, and j ∈[J]0 define a feed-forward neural network (FNN) with parameters (W, B) up to layer j, as the map FNN(J)

j (W, B): Rd0 →Rdj such that

FNN(J)

j (W, B)(x):= σ

W (j) · · · σ

W (2)σ

W (1)x + b(1)

+ b(2)

· · · + b(j) ∈Rdj, for x ∈Rd0. Here, the function σ: R →R is an activation function, applied componentwisely, e.g., a rectified linear unit (ReLU), where σ(x):= max(0, x). Further we will write θ:= (W, B) ∈Θ:= ΘW × Θb to denote the whole parameter set. In case j = J, we denote the J-layer feed-forward neural network by

FNN(J)(θ)(x):= FNN(J)

J (θ)(x).

## 2.6. Considered graph problems

In the following, we formally introduce the studied graph problems, namely, the single-source shortest path (SSSP) problem, the minimum spanning tree (MST) problem, and the knapsack problem.

Solving the SSSP problem, given an edge-weighted graph (G, wG) and a source vertex s ∈V (G), amounts to finding the shortest path from the source vertex s to all other vertices in the graph G. That is, for a vertex v ∈V (G), we aim to find a path

P ∗

G(s, v):= arg min P∈PG(s,v)

X e∈P wG(e).

The cost costG(P) of a (shortest) path P is P e∈P wG(e). Given an edge-weighted graph (G, wG), determining the cost of the SSSP problem amounts to determining the cost of a shortest path

P ∗

G(s, v) from the source vertex s to v, for all v ∈V (G).

Solving the MST problem, given an edge-weighted graph (G, wG), amounts to finding a tree over all vertices in the graph G with minimum overall edge weight, the minimum spanning tree. That is, we aim to find a tree

T ∗

G:= arg min V (T)=V (G)

T is a tree.

X e∈E(T)

wG(e).

The cost cost(T) of a (minimum) spanning tree T is P e∈T(E) wG(e). Given an edge-weighted graph (G, wG), determining the cost of the MST amounts to determining the cost of a minimum spanning tree.

Finally, we consider the (0/1) knapsack problem. Given a finite set of items I = {1,..., n}, each item i ∈I is associated with a value vi ∈R>0 and a weight wi ∈R>0. Given a capacity C ∈R>0, the knapsack problem consists of selecting a subset of items whose total weight does not exceed C and whose total value is maximized. Formally, we aim to find a subset

S∗:= arg max

S⊆I P i∈S wi≤C

X i∈S vi.

The cost (or value) of a solution S is given by P i∈S vi. Given ({(vi, wi)}i∈I, C), determining the cost of the knapsack problem amounts to determining the maximum achievable total value under the capacity constraint. While the knapsack problem is not a graph problem in its standard formulation, it admits a classical reduction to a shortest-path problem on a suitably constructed directed graph; see Section 3.2.1.

<!-- Page 13 -->

## 3. What and how can GNNs learn

Based on the definition of invariants in Section 2, we can view algorithms as invariant mappings from graphs (or their vertices) to scalars or real-valued vectors. Given a hypothesis class, we can compare its distinguishability with that of an algorithm via their induced equivalence relations, closely related to uniform approximation; see Proposition 1. However, these results do not explain how to choose a function in the hypothesis class that approximates a given algorithm, and, moreover, the notion of approximation is non-uniform, applying only to graphs of fixed size. Consequently, it does not, by itself, imply learnability, particularly for larger instances. In this section, we address these limitations by deriving suitable loss functions and finite datasets; training under these settings yields guarantees on how well MPNNs can learn to approximate algorithms uniformly across graph sizes.

We distinguish between learning algorithms that are graph-level invariants, e.g., the cost of the minimum spanning tree, and k-tuple invariants, e.g., the shortest-path distance from a source vertex to all other vertices in a graph.

## 3.1. Regularization-induced extrapolation

Here, we develop a general theoretical framework showing that, with suitable regularization and carefully chosen datasets, a learning algorithm can extrapolate beyond the training range, provided the input features lie in a compact set with an appropriate topology. In particular, our results apply to extrapolation to arbitrarily large domains. We establish this theory in a general learning setting by proving basic learnability properties of Lipschitz functions on compact sets. In Section 3.2, we specialize the analysis to MPNNs with different architectures, yielding our main extrapolation (size generalization) results.

We begin by defining the notion of a finite Lipschitz class, i.e., a set of parameterized functions over a bounded domain for which the parameters control the Lipschitz constant.

Definition 2. Let X be a non-empty set. Given a hypothesis class FΘ:= {fθ: θ ∈Θ} with fθ: X →R and Θ being a set of parameters. We say that FΘ is a finite Lipschitz class if there exists a (pseudo-)metric dX on X such that for every θ ∈Θ, fθ is Lipschitz with minimal Lipschitz constant4 Mθ < ∞, and the covering number N(X, d, ε) is finite for all ε > 0.

In what follows, we assume that whenever the above definition is satisfied, one can compute an upper bound Bθ ∈R>0 such that Mθ ≤Bθ, for all θ ∈Θ, which we call a Lipschitz certificate. A target function f∗is approximable with respect to FΘ with certificate Bf∗if for all ε > 0, there exists θ ∈Θ such that |fθ(x) −f∗(x)| < ε, for x ∈X.

Let N ∈N and FΘ be a finite Lipschitz class, let f∗: X →R be a target function, and let X:= {x1,..., xN} ⊆X. For the dataset {(xi, yi)}N i=1 with yi:= f∗(xi), the empirical loss of a hypothesis fθ ∈FΘ is

Lemp

X (fθ):= 1

N

N X i=1

|fθ(xi) −yi|, and its regularized loss is

LX(fθ):= Lemp

X (fθ) + Lreg(fθ),

4The infimum is used if the minimum does not exist.

<!-- Page 14 -->

V1(G) TIDM

X x11 x7 x6 x4 x8 x1 x5

2ε x12 x14 x13 x3 x9 x10 x2

|fθ(x5) −f∗(x5)| ≤ε fθ

Lemp

X (fθ) ≤ε′

Lreg(fθ) ≤ε′

Dataset(X) {x1, x2, x3, x4}

f1 f2 f3 f4 f5 f∗

FΘ

10

10

40

11

10

10 v TIDM

40

11

10

10 10 10 10 v

**Figure 1.** An illustration of the learnability result in Theorem 3, applied to MPNNs by first

mapping the space V1(G) to a pseudometric space (via IDMs or computation trees; see Section I.1), satisfying Definition 2 and then applying Theorem 3. A computation-tree construction is shown on the right.

where Lreg: FΘ →R+ is a regularization term which, in practice, depends on the certificate Bθ described above. Such regularizers typically depend on the norms of the trainable weights; a concrete example is given below.

Example of finite Lipschitz class and certificates A common example a finite Lipschitz class is given by standard feedforward neural networks of the form x 7→WLσ(WL−1σ(· · · σ(W1x) · · ·)) with 1-Lipschitz nonlinearities, for which one may take Bθ = QL ℓ=1 ∥Wℓ∥2 with respect to the induced Euclidean metric and assume inputs x in a closed Euclidean ball. More generally, certificates for compositions are obtained by multiplying per-layer or operator bounds, and many architectures (including constrained residual or normalized variants) admit similarly computable certificates. Likewise, we assume we have a known upper bound Bf∗∈R>0 such that the target f∗is Lipschitz regarding dX with minimal Lipschitz constant at most Bf∗.

The following result shows that for a finite Lipschitz class, controlling the Lipschitz certificate of that class, and the Lipschitz continuity of the target class imply that a target function can be learned from finite data; see Figure 1 for an illustration.

Theorem 3 (Informal). Let FΘ be a finite Lipschitz class on (X, dX) with certificates Bθ, and let f∗be a Lipschitz target that is approximable with certificate Bf∗. Then, defining the regularization term as

Lreg(fθ) = η ReLU(Bθ −Bf∗), for some η > 0, it follows that for any ε > 0, there exist ε′(ε), r(ε) > 0, and a dataset X ⊂X with cardinality

X = N(X, dX, r(ε)) such that if the regularized loss on X is smaller than ε′(ε), then sup x∈X

|fθ(x) −f∗(x)| < ε.

On the Bf∗certificate assumption The key assumption in Theorem 3 is not that the true Lipschitz constant stays controlled while approximating the target, but that the Lipschitz certificate Bθ does. That is, we can approximate f∗arbitrarily well by functions fθ whose computable bounds Bθ do not blow up. Since Bθ is directly computable from the parameters (e.g., via operator-norm or other parameter-norm bounds), it can be used in training even when the true Lipschitz constant Mθ is intractable. This yields a practical regularizer that controls Bθ.

<!-- Page 15 -->

The bound for Bf∗is trivial if the target function lies in the hypothesis class, but often f∗/∈FΘ and must be approximated. For standard FNNs, obtaining a nontrivial bound on Bf∗is difficult. However, fully expressive FNN alternatives have been proposed for adversarial robustness [Anil et al., 2019]; their Lipschitz constants can be bounded via parameter constraints, and the resulting function class is dense in the Lipschitz functions, so they can meet the theorem’s conditions. Similarly, 1-Lipschitz residual networks are dense in the set of scalar 1-Lipschitz functions on any compact domain [Murari et al., 2025], with Lipschitz constants bounded through parameter constraints.

A more general theorem in Section B addresses cases where functions cannot be approximated with a bounded certificate, including non-Lipschitz targets.

Connection to distinguishability If the conclusion of Theorem 3 holds, then a necessary condition is that, whenever FΘ cannot distinguish two inputs, f∗must also assign them the same value. This observation is particularly relevant for hypothesis classes with limited distinguishing power, such as MPNNs. In that case, uniform learnability is restricted to targets f∗whose distinguishability does not exceed that of the model class.

## 3.2. Finite Lipschitzness in MPNNs

Below, we study MPNNs that satisfy the finite Lipschitz learning property of Definition 2, which suffices for the learnability guarantee in Theorem 3. Throughout, the input space consists of pairs (G, u) with a graph G and vertex u ∈V (G), i.e., V1(G) for a graph class G.

We equip V1(G) with a pseudo-metric that controls the Lipschitz behavior of MPNNs. Our analysis covers (i) normalized sum aggregation, (ii) mean aggregation, and (iii) max/min aggregation; see Section G for formal definitions. These are special cases of the general MPNN formulation in Equation (1) and capture many classical graph algorithms.

We first establish finite Lipschitzness for normalized sum aggregation and extend it to mean aggregation. While inspired by work on iterated degree measures and computation trees (e.g., Grebík and Rocha [2022], Böker et al. [2023], Rauchwerger et al. [2024]), our approach does not require compactness of the input space, i.e., Definition 2 only assumes finite covering numbers, simplifying the construction (see Section I).

Crucially, we also show that max/min aggregation—essential for many algorithmic invariants— satisfies finite Lipschitzness. Here, the analysis proceeds on Hausdorff spaces with the Hausdorff distance; see Section J. To our knowledge, these are the first explicit Lipschitzness guarantees for max- and min-aggregation MPNNs, despite widespread use of related stability arguments [Levie, 2023, Böker et al., 2023, Rauchwerger et al., 2024, Vasileiou et al., 2024]. These architectures cover a range of common graph algorithms (see Section 3.2.1). Precise assumptions, conditions, and constants appear in Section G; we state the main result informally next.

Theorem 4 (Informal). The hypothesis class FΘ induced by MPNNs using normalized sum aggregation, mean aggregation, or max (or min) aggregation satisfies Definition 2.

See Theorem 104 and Theorem 108 for the formal statements and proofs. In the following, we identify graph invariants expressible by these MPNN architectures, and hence learnable from finite data by Theorem 4.

<!-- Page 16 -->

## 3.2.1. Algorithms within a finite Lipschitz class

Here, we outline examples of algorithms that are contained in finite Lipschitz classes, following Definition 2, there exists a (pseudo-)metric with finite covering number, and the algorithm is Lipschitz with respect to this (pseudo-)metric.

Normalized-sum aggregation In particular, normalized-sum aggregation is of special interest, as on graphs with a fixed number of vertices it allows MPNNs to represent any graph invariant with distinguishing power equivalent to the 1-WL. However, as we will see in Section 4.2, this learnability property cannot be maintained without restricting attention to graphs of fixed order.

Truncated PageRank We now show that a mean-aggregation MPNN learning truncated PageRank satisfies Theorem 3. Let (G, wG) be an edge-weighted graph, u ∈V (G), ξ ∈(0,1) a damping factor, and K ∈N a truncation depth. The K-truncated weighted PageRank value r(K)

u is defined recursively for t ∈[K] as r(t)

u:= (1 −ξ) + ξ deg(u)

X v∈N(u)

wuv r(t−1)

v, (3)

where r(0)

u:= 1, deg(u) denotes the weighted degree of u, and wuv:= wG(u, v). This generalizes standard PageRank [Page et al., 1998] to edge-weighted graphs; the unweighted case has wuv = 1 for all (u, v) ∈E(G).

This algorithm is represented exactly by a K-layer mean-aggregation MPNN (Equation (22)). Set h(0)

u:= 1 and define ϕt(x, y):= (1 −ξ) + ξy for t ∈[K]. Then the MPNN update h(t)

u:= ϕt h(t−1)

u, 1 deg(u)

X v∈N(u)

wuv h(t−1)

v matches Equation (3), yielding h(t)

u = r(t)

u for t ∈[K]. Since PageRank does not use self-loops, ϕt ignores its first argument. Lipschitz continuity of truncated PageRank follows from Theorem 4, as it lies in the hypothesis class of mean-aggregation MPNNs, which satisfies Definition 2. A key property is that the truncation depth K needed for error ε > 0 depends only on ε and ξ, not on |V (G)|. Since PageRank is a contraction with factor ξ, we have |r(K)

u −r(∞)

u | ≤ξK, where r(∞)

u is full PageRank. Thus, choosing K ≥⌈logξ(ε)⌉guarantees error at most ε regardless of graph size. Therefore, by Theorem 3, a finite training set with regularization suffices to train an MPNN to learn truncated PageRank and extrapolate to graphs of arbitrary size. Moreover, since truncation error is size-independent, the trained model approximates full PageRank to the same error across all graphs, despite being trained on finite data.

Bellman–Ford The Bellman–Ford algorithm for single-source shortest paths provides another example fitting into the framework. For an edge-weighted graph (G, wG) with source vertex r ∈V (G), the K-step Bellman–Ford algorithm computes shortest path distances x(K)

v from the root vertex r to each vertex v via the recurrence x(0)

r:= 0, x(0)

v:= β for v̸ = r, where β is a large constant, and x(t)

v:= min{x(t−1)

u + wG(u, v) | u ∈N(v) ∪{v}}, for t ∈[K]. This can be represented exactly by an MPNN with min aggregation (see Equation (23)) using K layers,

<!-- Page 17 -->

where the update function ϕt implements the identity and the aggregation function Mt computes Mt(xu, wG(u, v)):= xu + wG(u, v), for u ∈N(v). By Theorem 4, MPNNs with min aggregation satisfy Definition 2, and since the number of iterations K needed to compute shortest paths is at most the graph diameter, which is independent of graph size for bounded-diameter graph families, it follows from Theorem 3 that a finite training set with regularization can be used to train an MPNN to learn Bellman–Ford, enabling learning from a finite number of training examples that will extrapolate to graphs of arbitrary size. In Section 3.3, we adopt an approach specifically designed for this setting to derive a small training set that guarantees extrapolation. More generally, Zhu et al. [2021] showed that a generalized Bellman–Ford algorithm, based on path formulations, captures invariants such as the Katz index, widest path, and most reliable path. These can likewise be represented by MPNNs with mean and max aggregation and thus fall into a finite Lipschitz hypothesis class.

Dynamic programming It is well-known that many problems that can be solved by dynamic programming can be cast as a shortest-path problem on a transformed graph [Frieze, 1976]. Using the 0-1 knapsack problem as an illustration, for n ∈N, given items i ∈[n] with integer weights si and values vi, and a capacity S, consider the directed acyclic graph with vertices (i, j), for i ∈[n]0 and j ∈[S]0, where (i, j) represents having considered the first i items and accumulated total weight j. Now, we add edges ((i −1, j), (i, j)) of weight 0 (“do not choose item i”) and, whenever j + si ≤S, edges ((i −1, j), (i, j + si)) of weight −vi (“choose item i”); finally, connect each vertex (n, j) to a sink t by a zero-weight edge. Then every s-t path (with s:= (0,0)) encodes a feasible subset and has total weight equal to minus its total value, so the shortest-path distance to t equals −OPT. Moreover, the standard knapsack recurrence is exactly the shortest-path relaxation on this graph, i.e., initializing x(0)

s:= 0 and x(0)

u:= β, for u̸ = s, one has, for i ∈[n] and j ∈[S]0, x(i)

(i,j):= min n x(i−1)

(i−1,j), x(i−1)

(i−1,j−si) −vi o

, where the second term is omitted when j < si, and x(n)

t:= minj≤S x(n)

(n,j). As in the Bellman– Ford example, this computation can be represented exactly by a min-aggregation MPNN with K = n layers by taking ϕt to be the identity and Mt(xu, w(u, v)):= xu + w(u, v); thus, by Theorem 4 the hypothesis class satisfies Definition 2, and for families in which the number of stages n is bounded (so K is independent of the size of the transformed graph, which grows with S), Definition 2 implies learnability from a finite training set with regularization and extrapolation to arbitrarily large capacities. We note that the same reasoning applies to a large class of problems that can be cast as dynamic programs, e.g., the longest increasing subsequence or edit distances between strings.

## 3.3. Improved learning guarantees for SSSPs algorithms

While the above results demonstrate the existence of a finite training set for learning various algorithms, they do not explicitly show how to construct this training set or bound its size. Hence, the following result shows that we can explicitly construct a constant-size training set and a differentiable regularization term such that a small loss on the training set implies approximating the Bellman–Ford algorithm for arbitrarily large graphs. Consider learning Ksteps of Bellman–Ford using a min-aggregation MPNN with K layers and m-layer feed-forward neural networks. We train the MPNN by minimizing a loss function L(θ) that contains a

<!-- Page 18 -->

weighted variant of ℓ1-regularization. In particular, Lreg(θ) is a weighted sum over the ℓ1 norms of the weight matrices and bias vectors, with layer-dependent weights.

Theorem 5 (Informal). There exists a training set X of size K + 1 such that, for appropriate choice of regularization parameter η, if a K-layer min-aggregation MPNN achieves a loss LX(θ) within ε < 1/2 of its global minimum, then for any SSSP instance, the MPNN approximates every K-step shortest path distance x(K) within additive error ε(x(K) + 1).

A detailed statement of the theorem is given in Theorem 17 in the appendix. The theorem differs from the main theorem of Nerem et al. [2025] in several ways. On the positive side, our result uses a smaller training set, namely K + 1 path instances, and replaces their nondifferentiable ℓ0 penalty with a differentiable ℓ1 regularizer with layer-specific weights. This differentiability allows our loss to be optimized directly. On the other hand, our analysis assumes a somewhat more restricted model, i.e, the depth is fixed to exactly K message-passing layers (matching K Bellman–Ford steps), and the aggregation dimension is assumed to be 1. These choices are made to simplify the analysis. Furthermore, in our result, the regularization parameter η and the edge weights in the training set both scale exponentially in K, which may be prohibitive in some settings. However, in Section D.2 we outline ways to circumvent these limitations.

## 4. What GNNs cannot learn

In the previous section, we identified sufficient conditions under which a hypothesis class admits learnability guarantees via regularized empirical risk minimization. In particular, when a class of MPNNs forms a finite Lipschitz class with respect to a suitable (pseudo)metric on the input space, invariant algorithms that can be uniformly approximated within this class are learnable from finite samples. In this section, we turn to the complementary question, i.e., which invariant algorithms cannot be learned by MPNN hypothesis classes? We first show cases of invariants that are not expressible by any MPNN of the general form Equation (1). Then we show that even for invariants that are expressible by MPNNs, Theorem 3 may not be applied since Definition 2 is not satisfied by these types of MPNNs.

## 4.1. Expressivity limitations

Here, we show that MPNNs are often insufficient to learn simple graph algorithms. To that end, we first show that standard MPNNs, as defined in Equation (1), are not expressive enough to determine the costs of the SSSP and MST.

Formally, let G denote the class of edge-weighted graphs. Given an edge-weighted graph (G, wG) and a source vertex s ∈V (G), we view the costs for the SSSP problem as a 2-tuple invariant SSSP: V2(G) →R such that SSSP(G, (s, v)):= costG(PG(s, v)), for v ∈V (G), where PG(s, v) denotes a shortest path from s to v in G. Similarly, we view the cost of the MST problem as a graph-level invariant MST: G →R such that MST(G):= P e∈E(T) wG(e), for a minimal spanning tree T of G.

The following results highlight limitations of MPNN architectures in approximating classical graph algorithmic invariants. In particular, no MPNN architecture can approximate the SSSP cost or the MST cost arbitrarily well. Moreover, this limitation persists for MST even when considering 1-iWL-simulating MPNNs; see Section 2.4. Formal statements and proofs are deferred to Section E.

<!-- Page 19 -->

Proposition 6 (Informal). There does not exist an MPNN architecture that can approximate the invariants SSSP and MST. In contrast, there exist 1-iWL- and (1,1)-WL-expressive MPNN architectures that can approximate the invariants SSSP and MST, respectively.

Here, 1-iWL and (1,1)-WL refer to MPNN architectures that simulate individualized variants of the 1-WL, as introduced in Section 2.3.

## 4.2. Expressible but (possibly) not learnable invariants

Beyond expressivity limitations, there exist invariant algorithms that are representable by MPNNs but for which our sufficient conditions for learnability do not apply. In such cases, the obstruction is not a lack of expressive power, but rather the absence of a metric structure on the input space that yields finite covering numbers, as required by Definition 2.

As a simple example, consider a variant of the MPNN architecture in which the aggregation operator in Equation (1) is replaced by an unnormalized sum. Restricting to graphs without vertex or edge features (or, equivalently, to graphs with constant vertex and edge features across all vertices and edges) and to one-layer architectures, the resulting hypothesis class clearly contains the degree invariant (G, u) 7→degG(u), since vertex degrees are computed exactly by summing over neighbors.

However, if we don’t restrict our space to graphs with bounded maximum degree, this expressivity already prevents the hypothesis class from being a finite Lipschitz class. Indeed, for any (pseudo-)metric under which the degree map is Lipschitz with a finite constant, the induced metric space necessarily has infinite covering number (for sufficiently small radius) as shown next.

Lemma 7 (Informal). Let K be the family of all complete graphs. Let d be any (pseudo-)metric on V1(K) such that the degree invariant deg: V1(K) →N is L-Lipschitz for some L ∈R>0. Then, for every ε ∈(0, 1

L), N(V1(K), d, ε) = ∞. Consequently, no hypothesis class containing the degree invariant can satisfy Definition 2 on any graph space containing V1(K).

A similar obstruction applies to any invariant equivalent to the 1-WL, since its first iteration already captures the degree invariant. Thus, any hypothesis class expressive enough to represent all 1-WL invariants inherits the same covering-number pathology on graph spaces with unbounded degrees.

## 5. Limitations and future directions

While our framework provides the first general, provable learning guarantees for a broad class of graph algorithms with MPNNs, it relies on several structural assumptions that limit its scope. In particular, our theory assumes access to carefully constructed training datasets that form suitable covers of the underlying graph space. Although such datasets are essential for establishing our guarantees, they may not arise naturally in practice, so it is necessary to develop high-probability, sampling-based methods for constructing informative training sets. Moreover, our results are formulated in terms of achieving sufficiently small regularized training

<!-- Page 20 -->

**Table 1.** Test score results for Q2 with a standard and 1-iWL-equivalent MPNNs. All results

were obtained across three seeds, and test scores are averaged. The number in brackets indicates the number of vertices for the test graphs.

Dataset

Task (Test score ↓) ER-constdeg ER General

1-WL (64) 0.9725 ± 0.0001 0.9725 ± 0.0001 0.8393 ± 0.0001 1-iWL (64) 0.0035 ± 0.0002 0.0034 ± 0.0004 0.0032 ± 0.0002

1-WL (256) 0.9896 ± 0.0006 0.9765 ± 0.0001 0.8368 ± 0.0010 1-iWL (256) 0.0033 ± 0.0002 0.0037 ± 0.0001 0.0033 ± 0.0002

1-WL (1024) 0.9948 ± 0.0005 0.9645 ± 0.0001 0.8217 ± 0.0010 1-iWL (1024) 0.0030 ± 0.0001 0.0038 ± 0.0002 0.0033 ± 0.0002 loss. Yet, we do not provide guarantees that standard gradient-based optimization methods will reliably converge to parameter settings that generalize.

Hence, looking forward, bridging our learning-theoretic analysis with convergence results for gradient descent, therefore, remains an important direction for future work. Finally, our current analysis is restricted to polynomial-time algorithms; extending the framework to approximation algorithms for computationally hard problems and studying whether exploiting the data distribution can yield approximation ratios beyond worst-case guarantees constitutes another promising avenue for future research.

## 6. Experimental study

In the following, we investigate to what extent our theoretical results translate into practice. Specifically, we answer the following questions.

Q1 Does gradient descent converge to parameter assignments that allow for size generalization?

Q2 Do the more expressive MPNN architectures of Section 4 lead to improved predictive performance in practice?

Q3 Does the differentiable regularization term from Section 3.3 leads to improved generalization errors compared to p-norm based regularization term?

We use an MPNN aligned with the theoretical results observed in Section 3.3. Due to the explicit construction of the training set, we conduct the experiments on the SSSP problem outlined in Section 3.3. For this, we generate synthetic training and test datasets based on Erdős–Rényi graphs and path graphs derived from Theorem 5. We then train a two-layer MPNN to predict two steps of the Bellman–Ford algorithm. See Section L for details on dataset construction, experimental settings, and additional results. The source code of all methods and evaluation procedures is available at https://github.com/Timo-SH/exact_nar.

## Results

and discussion In the following, we address Q1 to Q3. Regarding Q1, Section 6 shows size generalization properties for 64 and 1024 vertices on test graphs. The underlying MPNNs were trained on the same training dataset with a fixed edge weight for the path graphs outlined in Section 3.3. In addition, weights were uniformly sampled for test set edges. To demonstrate size generalization, we provide three test sets with increasing graph diversity. Throughout all test sets, the test error does not increase with vertex count in each graph. Furthermore,

<!-- Page 21 -->

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score 64 nodes Test score 1024 nodes Training loss

**Figure 2.** Training error and test score (lower is better) for size generalization experiments in

Q1 using test datasets with 64 and 1024 vertices, respectively. Values were smoothed using Gaussian smoothing with σ = 1. The gray region indicates the loss values for which Theorem 5 guarantees extrapolation.

**Table 2.** Comparison of regularization between our ℓ1 based method (here named ℓreg), ℓ1 and

ℓ2 regularization terms. Across all experiments, η = 0.1 holds, and the MPNN from Q1 was used. Furthermore, the general dataset as outlined in Section L is used for all experiments. Results are obtained across three seeds.

vertices

Reg. (↓) 64 128 256 512 ℓ1 0.0061 ± 0.0010 0.0053 ± 0.0011 0.0054 ± 0.0010 0.0060 ± 0.0009 0.0056 ± 0.0009 ℓ2 0.0336 ± 0.0503 0.0336 ± 0.0500 0.0343 ± 0.0510 0.0133 ± 0.0123 0.0369 ± 0.0557 ℓreg 0.0032 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0003 0.0033 ± 0.0002 the average vertex degree, as shown between the degree-bound ER-constdeg dataset and the unbounded ER dataset, does not affect test set performance. For the construction of the datasets, the behavior of the weight parameter, and further results, see Section L.

Regarding Q2, Table 1 shows the inability of a standard MPNN to generalize to unseen graphs in the test set at all. In addition, compared to the 1-iWL-equivalent MPNN, we observe a significantly higher training loss.

Regarding Q3, as seen in Table 2, replacing the proposed differentiable regularization term with a p-norm based regularization leads to similar results using ℓ1 regularization. While ℓ1 and ℓ2 norms allow for sufficient training and generalization results, size generalization improves with the proposed regularization term across graph sizes. Furthermore, with ℓ2 regularization, training is noticeably less stable and yields slightly worse test set performance. These results align with Theorem 5, highlighting the application of a differentiable regularization term to the SSSP problem, opposed to a non-differentiable regularization previously required.

<!-- Page 22 -->

## 7. Conclusion

We developed a general theoretical framework for learning graph algorithms with GNNs. Our framework characterizes the conditions under which an MPNN, or more expressive variants, can be trained on a finite set of instances and provably generalize to inputs of arbitrary size by minimizing a supervised, regularized loss. By connecting algorithmic learning to notions of metric structure, covering numbers, and regularization-induced extrapolation, we move beyond purely expressivity-based analyses and provide learning-theoretic guarantees for neural algorithmic reasoning on graphs. Building on this framework, we identified broad classes of graph algorithms, ranging from shortest paths to dynamic programming problems, that suitably expressive GNNs can learn, and we also identified fundamental limitations of standard MPNNs. For the single-source shortest-path problem, we further showed how a differentiable p-normbased regularization significantly reduces the size of the required training set. In summary, our results provide a precise characterization of which algorithms GNNs can learn from finite data and which they cannot, thereby enabling a more principled understanding of data-driven algorithmic design and its potential for reliable generalization beyond the training regime.

## References

[1] C. Anil, J. Lucas, and R. Grosse. Sorting out lipschitz function approximation. In ICML,

2019. 15

[2] V. Arvind, J. Köbler, G. Rattan, and O. Verbitsky. On the power of color refinement. In

International Symposium on Fundamentals of Computation Theory, 2015. 9

[3] W. Azizian and M. Lelarge. Characterizing the expressive power of invariant and equivariant graph neural networks. In ICLR, 2021. 3, 4, 10, 11, 70

[4] L. Babai and L. Kucera. Canonical labelling of graphs in linear average time. In Symposium on Foundations of Computer Science, 1979. 9

[5] A. Baranwal, K. Fountoulakis, and A. Jagannath. Graph convolution for semi-supervised classification: Improved linear separability and out-of-distribution generalization. In ICML, 2021. 5

[6] I. I. Baskin, V. A. Palyulin, and N. S. Zefirov. A neural device for searching direct correlations between structures and properties of chemical compounds. Journal of Chemical Information and Computer Sciences, 37(4):715–721, 1997. 4

[7] B. Bevilacqua, F. Frasca, D. Lim, B. Srinivasan, C. Cai, G. Balamurugan, M. M. Bronstein, and H. Maron. Equivariant subgraph aggregation networks. In ICLR, 2022. 4

[8] V. I. Bogachev. Measure Theory. Springer Monographs in Mathematics. Springer Science

& Business Media, 2007. 79

[9] J. Bruna, W. Zaremba, A. Szlam, and Y. LeCun. Spectral networks and deep locally connected networks on graphs. In ICLR, 2014. 4

[10] J. Böker, R. Levie, N. Huang, S. Villar, and C. Morris. Fine-grained expressivity of graph neural networks. In NeurIPS, 2023. 4, 15, 74, 90

<!-- Page 23 -->

[11] J. Cai, M. Fürer, and N. Immerman. An optimal lower bound on the number of variables for graph identifications. Combinatorica, 12(4):389–410, 1992. 4, 9

[12] Q. Cappart, D. Chételat, E. Khalil, A. Lodi, C. Morris, and P. Veličković. Combinatorial optimization and reasoning with graph neural networks. Journal of Machine Learning Research, 24:130:1–130:61, 2023. 2, 5

[13] Z. Chen, S. Villar, L. Chen, and J. Bruna. On the equivalence between graph isomorphism testing and function approximation with GNNs. In NeurIPS, 2019. 4

[14] Z. Chen, L. Chen, S. Villar, and J. Bruna. Can graph neural networks count substructures?

In NeurIPS, 2020. 3

[15] C. Chuang and S. Jegelka. Tree mover’s distance: Bridging graph metrics and stability of graph neural networks. In NeurIPS, 2022. 79

[16] C.-Y. Chuang, Y. Mroueh, K. Greenewald, A. Torralba, and S. Jegelka. Measuring generalization with optimal transport. In NeurIPS, 2021. 4

[17] L. Cotta, C. Morris, and B. Ribeiro. Reconstruction for powerful graph representations.

In NeurIPS, 2021. 4

[18] N. Daniëls and F. Geerts. A note on the VC dimension of 1-dimensional GNNs. arXiv preprint, 2024. 4

[19] A. B. de Luca and K. Fountoulakis. Simulation of graph algorithms with looped trans- formers. In ICML, 2024. 3, 6

[20] A. B. de Luca, G. Giapitzakis, S. Yang, P. Velickovic, and K. Fountoulakis. Positional attention: Expressivity and learnability of algorithmic computation. In ICML, 2025. 3, 6

[21] M. Defferrard, X. Bresson, and P. Vandergheynst. Convolutional neural networks on graphs with fast localized spectral filtering. In NeurIPS, 2016. 4

[22] G. A. D’Inverno, M. Bianchini, and F. Scarselli. VC dimension of graph neural networks with pfaffian activation functions. arXiv preprint, 2024. 4

[23] A. J. Dudzik and P. Velickovic. Graph neural networks are dynamic programmers. In

NeurIPS, 2022. 5

[24] D. Duvenaud, D. Maclaurin, J. Aguilera-Iparraguirre, R. Gómez-Bombarelli, T. Hirzel,

A. Aspuru-Guzik, and R. P. Adams. Convolutional networks on graphs for learning molecular fingerprints. In NeurIPS, 2015. 3

[25] P. M. Esser, L. C. Vankadara, and D. Ghoshdastidar. Learning theory can (sometimes)

explain generalisation in graph neural networks. In NeurIPS, 2021. 5

[26] B. J. Franks, C. Morris, A. Velingker, and F. Geerts. Weisfeiler-leman at the margin:

When more expressivity matters. In ICML, 2024. 4

[27] A. M. Frieze. Shortest path algorithms for knapsack type problems. Mathematical

Programming, 11:150–157, 1976. 17

<!-- Page 24 -->

[28] F. Gama, A. G. Marques, G. Leus, and A. Ribeiro. Convolutional neural network architectures for signals supported on graphs. IEEE Transactions on Signal Processing, 67(4):1034–1049, 2019. 4

[29] V. K. Garg, S. Jegelka, and T. S. Jaakkola. Generalization and representational limits of graph neural networks. In ICML, 2020. 4

[30] M. Gasse, D. Chételat, N. Ferroni, L. Charlin, and A. Lodi. Exact combinatorial optimization with graph convolutional neural networks. In NeurIPS, 2019. 2

[31] F. Geerts. The expressive power of kth-order invariant graph networks. arXiv preprint,

2020. 4

[32] F. Geerts and J. L. Reutter. Expressiveness and approximation properties of graph neural networks. In ICLR, 2022. 4, 11, 70

[33] J. Gilmer, S. S. Schoenholz, P. F. Riley, O. Vinyals, and G. E. Dahl. Neural message passing for quantum chemistry. In ICML, 2017. 2, 3, 4, 8

[34] C. Goller and A. Küchler. Learning task-dependent distributed representations by backpropagation through structure. In International Conference on Neural Networks, 1996. 4

[35] J. Grebík and I. Rocha. Fractional isomorphism of graphons. Combinatorica, 42(3):

365–404, 2022. 15, 74, 90

[36] M. Grohe. Descriptive Complexity, Canonisation, and Definable Graph Structure Theory.

Cambridge University Press, 2017. 9

[37] M. Grohe. The logic of graph neural networks. In Symposium on Logic in Computer

Science, 2021. 9, 10

[38] F. Grötschla, J. Mathys, and R. Wattenhofer. Learning graph algorithms with recurrent graph neural networks. arXiv preprint, 2022. 5

[39] A. A. Hagberg, D. A. Schult, and P. J. Swart. Exploring network structure, dynamics, and function using networkx. In Proceedings of the 7th Python in Science Conference, pages 11 – 15, 2008. 91

[40] W. L. Hamilton, Z. Ying, and J. Leskovec. Inductive representation learning on large graphs. In NeurIPS, 2017. 3

[41] B. Hammer. Generalization ability of folding networks. IEEE Transactions on Knowledge and Data Engineering, 13(2):196–206, 2001. 4

[42] Y. He and E. Vitercik. Primal-dual neural algorithmic reasoning. In ICML, 2025. 3, 5

[43] C. Hertrich and L. Sering. Relu neural networks of polynomial size for exact maximum flow computation. Mathematical Programming, 210(1):377–406, 2025. 5

[44] C. Hertrich and M. Skutella. Provably good solutions to the knapsack problem via neural networks of bounded size. INFORMS J. Comput., 35(5):1079–1097, 2023. 5

<!-- Page 25 -->

[45] B. Ibarz, V. Kurin, G. Papamakarios, K. Nikiforou, M. Bennani, R. Csordás, A. J. Dudzik,

M. Bosnjak, A. Vitvitskyi, Y. Rubanova, A. Deac, B. Bevilacqua, Y. Ganin, C. Blundell, and P. Velickovic. A generalist neural algorithmic learner. In B. Rieck and R. Pascanu, editors, LoG, 2022. 5

[46] R. Jain, P. Velickovic, and P. Liò. Neural priority queues for graph neural networks.

arXiv preprint, 2023. 5

[47] H. Ju, D. Li, A. Sharma, and H. R. Zhang. Generalization in graph neural networks:

Improved PAC-Bayesian bounds on graph diffusion. arXiv preprint, 2023. 4

[48] J. Jürß, D. H. Jayalath, and P. Velickovic. Recursive algorithmic reasoning. In S. Villar and B. Chamberlain, editors, LoG, 2023. 5

[49] R. Karczewski, A. Souza, and V. Garg. On the generalization of equivariant graph neural networks. In ICML, 2024. 4

[50] M. Karpinski and A. Macintyre. Polynomial bounds for VC dimension of sigmoidal and general Pfaffian neural networks. Journal of Computer and System Sciences, 54(1): 169–176, 1997. 4

[51] A. S. Kechris. Classical Descriptive Set Theory, volume 156 of Graduate Texts in Mathematics. Springer, New York, 2012. 78

[52] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. In ICLR, 2015.

92

[53] T. N. Kipf and M. Welling. Semi-supervised classification with graph convolutional networks. In ICLR, 2017. 3, 4

[54] D. B. Kireev. Chemnet: A novel neural network based method for graph/property mapping. Journal of Chemical Information and Computer Sciences, 35(2):175–180, 1995. 4

[55] R. Lam, A. Sanchez-Gonzalez, M. Willson, P. Wirnsberger, M. Fortunato, F. Alet,

S. Ravuri, T. Ewalds, Z. Eaton-Rosen, W. Hu, A. Merose, S. Hoyer, G. Holland, O. Vinyals, J. Stott, A. Pritzel, S. Mohamed, and P. Battaglia. Learning skillful medium-range global weather forecasting. Science, 382(6677):1416–1421, 2023. 2

[56] J. Lee, M. Hwang, and J. J. Whang. PAC-Bayesian generalization bounds for knowledge graph representation learning. In ICML, 2024. 4

[57] R. Levie. A graphon-signal analysis of graph neural networks. In NeurIPS, 2023. 5, 15

[58] R. Levie, F. Monti, X. Bresson, and M. M. Bronstein. Cayleynets: Graph convolutional neural networks with complex rational spectral filters. IEEE Transactions on Signal Processing, 67(1):97–109, 2019. 4

[59] E. Levin, Y. Ma, M. Díaz, and S. Villar. On transferring transferability: Towards a theory for size generalization. In NeurIPS, 2025. 5

[60] P. Li, Y. Wang, H. Wang, and J. Leskovec. Distance encoding: Design provably more powerful neural networks for graph representation learning. In NeurIPS, 2020. 4

<!-- Page 26 -->

[61] S. Li, F. Geerts, D. Kim, and Q. Wang. Towards bridging generalization and expressivity of graph neural networks. arXiv preprint, 2024. 4

[62] R. Liao, R. Urtasun, and R. S. Zemel. A PAC-Bayesian approach to generalization bounds for graph neural networks. In ICLR, 2021. 4

[63] A. Loukas. What graph neural networks cannot learn: depth vs width. In ICLR, 2020. 3,

5

[64] T. Maehara and H. NT. A simple proof of the universality of invariant/equivariant graph neural networks. arXiv preprint, 2019. 4

[65] H. Maron, H. Ben-Hamu, H. Serviansky, and Y. Lipman. Provably powerful graph networks. In NeurIPS, 2019. 4

[66] S. Maskey, Y. Lee, R. Levie, and G. Kutyniok. Generalization analysis of message passing neural networks on large random graphs. In NeurIPS, 2022. 5

[67] S. Maskey, G. Kutyniok, and R. Levie. Generalization bounds for message passing networks on mixture of graphons. arXiv preprint, 2024. 5

[68] S. Maskey, R. Paolino, F. Jogl, G. Kutyniok, and J. F. Lutzeyer. Graph representational learning: When does more expressivity hurt generalization? arXiv preprint, 2025. 4

[69] C. Merkwirth and T. Lengauer. Automatic generation of complementary descriptors with molecular graph networks. Journal of Chemical Information and Modeling, 45(5): 1159–1168, 2005. 4

[70] W. Merrill and A. Sabharwal. A little depth goes a long way: The expressive power of log-depth transformers. arXiv preprint, 2025. 3, 6

[71] A. Micheli. Neural network for graphs: A contextual constructive approach. IEEE

Transactions on Neural Networks, 20(3):498–511, 2009. 4

[72] A. Micheli and A. S. Sestito. A new neural network model for contextual processing of graphs. In Italian Workshop on Neural Nets Neural Nets and International Workshop on Natural and Artificial Immune Systems, 2005. 4

[73] F. Monti, D. Boscaini, J. Masci, E. Rodolà, J. Svoboda, and M. M. Bronstein. Geometric deep learning on graphs and manifolds using mixture model CNNs. In IEEE Conference on Computer Vision and Pattern Recognition, 2017. 4

[74] C. Morris. The power of the Weisfeiler-Leman algorithm for machine learning with graphs.

In International Joint Conference on Artificial Intelligence, 2021. 4

[75] C. Morris, M. Ritzert, M. Fey, W. L. Hamilton, J. E. Lenssen, G. Rattan, and M. Grohe.

Weisfeiler and Leman go neural: Higher-order graph neural networks. In AAAI, 2019. 3, 4, 5, 10, 11, 67, 68

[76] C. Morris, N. M. Kriege, F. Bause, K. Kersting, P. Mutzel, and M. Neumann. TUDataset:

A collection of benchmark datasets for learning with graphs. arXiv preprint, 2020. 71

<!-- Page 27 -->

[77] C. Morris, G. Rattan, and P. Mutzel. Weisfeiler and Leman go sparse: Towards higher- order graph embeddings. In NeurIPS, 2020. 4

[78] C. Morris, G. Rattan, S. Kiefer, and S. Ravanbakhsh. SpeqNets: Sparsity-aware permutation-equivariant graph networks. In ICML, 2022. 4

[79] C. Morris, F. Geerts, J. Tönshoff, and M. Grohe. WL meet VC. In ICML, 2023. 4

[80] C. Morris, Y. L., H. Maron, B. Rieck, N. M. Kriege, M. Grohe, M. Fey, and K. Borgwardt.

Weisfeiler and Leman go machine learning: The story so far. Journal of Machine Learning Research, 24:333:1–333:59, 2023. 10

[81] D. Murari, T. Furuya, and C.-B. Schönlieb. Approximation theory for 1-Lipschitz ResNets.

arXiv preprint, 2025. 15

[82] R. R. Nerem, S. Chen, S. Dasgupta, and Y. Wang. Graph neural networks extrapolate out-of-distribution for shortest paths. arXiv preprint, 2025. 1, 3, 6, 18, 34, 38

[83] D. Numeroso, D. Bacciu, and P. Velickovic. Dual algorithmic reasoning. In ICLR, 2023. 5

[84] L. Page, S. Brin, R. Motwani, and T. Winograd. The PageRank citation ranking: Bringing order to the web. Technical Report 1999-66, Stanford InfoLab, 1998. 16

[85] M. Pándy, W. Qiu, G. Corso, P. Velickovic, Z. Ying, J. Leskovec, and P. Liò. Learning graph search heuristics. In LoG, 2022. 5

[86] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin,

N. Gimelshein, L. Antiga, A. Desmaison, A. Köpf, E. Z. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala. Pytorch: An imperative style, high-performance deep learning library. In NeurIPS, 2019. 92

[87] P. Pellizzoni, T. Schulz, D. Chen, and K. M. Borgwardt. On the expressivity and sample complexity of node-individualized graph neural networks. In NeurIPS, 2024. 4

[88] P. Pellizzoni, T. H. Schulz, and K. M. Borgwardt. Graph neural networks can (often)

count substructures. In ICLR, 2025. 3

[89] C. Qian, G. Rattan, F. Geerts, C. Morris, and M. Niepert. Ordered subgraph aggregation networks. In NeurIPS, 2022. 4

[90] C. Qian, D. Chételat, and C. Morris. Exploring the power of graph neural networks in solving linear optimization problems. In AISTATS, 2024. 5

[91] C. Qian, A. Manolache, K. Ahmed, Z. Zeng, G. V. den Broeck, M. Niepert, and C. Morris.

Probabilistically rewired message-passing neural networks. In ICLR, 2024. 2, 10

[92] G. Rattan and T. Seppelt. Weisfeiler-leman and graph spectra. In SODA, 2023. 10, 69,

73

[93] L. Rauchwerger, S. Jegelka, and R. Levie. Generalization, expressivity, and universality of graph neural networks on attributed graphs. arXiv preprint, 2024. 5, 15, 74

<!-- Page 28 -->

[94] G. Rodionov and L. Prokhorenkova. Discrete neural algorithmic reasoning. In ICML,

2025. 5

[95] E. Rosenbluth and M. Grohe. Repetition makes perfect: Recurrent sum-gnns match message passing limit. arXiv preprint, 2025. 5

[96] C. Sanford, B. Fatemi, E. Hall, A. Tsitsulin, M. Kazemi, J. Halcrow, B. Perozzi, and

V. Mirrokni. Understanding transformer reasoning capabilities via graph algorithms. In NeurIPS, 2024. 3, 6

[97] C. Sanford, D. Hsu, and M. Telgarsky. Transformers, parallel computation, and logarithmic depth. In ICML, 2024. 3, 6

[98] R. Sato, M. Yamada, and H. Kashima. Approximation ratios of graph neural networks for combinatorial problems. In NeurIPS, 2019. 5

[99] F. Scarselli, M. Gori, A. C. Tsoi, M. Hagenbuchner, and G. Monfardini. The graph neural network model. IEEE Transactions on Neural Networks, 20(1):61–80, 2009. 2, 3, 4

[100] F. Scarselli, A. C. Tsoi, and M. Hagenbuchner. The Vapnik-Chervonenkis dimension of graph and recursive neural networks. Neural Networks, pages 248–259, 2018. 4

[101] L. Scavuzzo, K. I. Aardal, A. Lodi, and N. Yorke-Smith. Machine learning augmented branch and bound for mixed integer linear programming. arXiv preprint, 2024. 2

[102] R. Schneider. Convex Bodies: The Brunn–Minkowski Theory, volume 44 of Encyclopedia of Mathematics and its Applications. Cambridge University Press, Cambridge, 1993. 80

[103] A. Sperduti and A. Starita. Supervised neural networks for the classification of structures.

IEEE Transactions on Neural Networks, 8(3):714–35, 1997. 4

[104] H. Tang and Y. Liu. Towards understanding generalization of graph neural networks. In

ICML, 2023. 5

[105] V. Timofte. Stone–Weierstrass theorems revisited. Journal of Approximation Theory, 136

(1):45–59, 2005. 70

[106] V. N. Vapnik. The Nature of Statistical Learning Theory. Springer, 1995. 4

[107] A. Vasileiou, B. Finkelshtein, F. Geerts, R. Levie, and C. Morris. Covered forest: Fine- grained generalization analysis of graph neural networks. In ICML, 2024. 5, 15

[108] A. Vasileiou, S. Jegelka, R. Levie, and C. Morris. Survey on generalization theory for graph neural networks. arXiv preprint, 2024. 5

[109] P. Velickovic and C. Blundell. Neural algorithmic reasoning. Patterns, 2(7):100273, 2021.

2, 5

[110] P. Velickovic, R. Ying, M. Padovano, R. Hadsell, and C. Blundell. Neural execution of graph algorithms. In ICLR, 2020. 2, 5

[111] P. Velickovic, A. P. Badia, D. Budden, R. Pascanu, A. Banino, M. Dashevskiy, R. Hadsell, and C. Blundell. The CLRS algorithmic reasoning benchmark. In ICML, 2022. 5

<!-- Page 29 -->

[112] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, and Y. Bengio. Graph attention networks. In ICLR, 2018. 3

[113] S. Verma and Z. Zhang. Stability and generalization of graph convolutional neural networks. In International Conference on Knowledge Discovery & Data Mining, 2019. 5

[114] Z. Wang, J. Cerviño, and A. Ribeiro. A manifold perspective on the statistical general- ization of graph neural networks. In ICML, 2025. 5

[115] B. Weisfeiler. On Construction and Identification of Graphs. Springer, 1976. 4

[116] B. Weisfeiler and A. Leman. The reduction of a graph to canonical form and the algebra which appears therein. Nauchno-Technicheskaya Informatsia, 2(9):12–16, 1968. 4, 9

[117] F. Wong, E. J. Zheng, J. A. Valeri, N. M. Donghia, M. N. Anahtar, S. Omori, A. Li,

A. Cubillos-Ruiz, A. Krishnan, W. Jin, A. L. Manson, J. Friedrichs, R. Helbig, B. Hajian, D. K. Fiejtek, F. F. Wagner, H. H. Soutter, A. M. Earl, J. M. Stokes, L. D. Renner, and J. J. Collins. Discovery of a structural class of antibiotics with explainable deep learning. Nature, 2023. 2

[118] L. A. C. Xhonneux, A. Deac, P. Velickovic, and J. Tang. How to transfer algorithmic reasoning knowledge to learn new algorithms? In NeurIPS, 2021. 5

[119] K. Xu, W. Hu, J. Leskovec, and S. Jegelka. How powerful are graph neural networks? In

ICLR, 2019. 3, 4, 5, 10

[120] K. Xu, J. Li, M. Zhang, S. S. Du, K. Kawarabayashi, and S. Jegelka. What can neural networks reason about? In ICLR, 2020. 2, 6

[121] M. Yau, N. Karalias, E. Lu, J. Xu, and S. Jegelka. Are graph neural networks optimal approximation algorithms? In NeurIPS, 2024. 5

[122] G. Yehudai, E. Fetaya, E. A. Meirom, G. Chechik, and H. Maron. From local structures to size generalization in graph neural networks. In ICML, 2021. 5

[123] G. Yehudai, C. Sanford, M. Bechler-Speicher, O. Fischer, R. Gilad-Bachrach, and

A. Globerson. Depth-width tradeoffs in algorithmic reasoning of graph tasks with transformers. arXiv preprint, 2025. 3, 6

[124] R. Yonetani, T. Taniai, M. Barekatain, M. Nishimura, and A. Kanezaki. Path planning using neural a* search. In M. Meila and T. Zhang, editors, ICML, 2021. 5

[125] B. Zhang, G. Feng, Y. Du, D. He, and L. Wang. A complete expressiveness hierarchy for subgraph gnns via subgraph Weisfeiler-Lehman tests. arXiv preprint, 2023. 4

[126] H. Zhou, A. Bradley, E. Littwin, N. Razin, O. Saremi, J. M. Susskind, S. Bengio, and

P. Nakkiran. What algorithms can transformers learn? a study in length generalization. In ICLR, 2024. 3, 6

[127] Z. Zhu, Z. Zhang, L. A. C. Xhonneux, and J. Tang. Neural bellman-ford networks: A general graph neural network framework for link prediction. In NeurIPS, 2021. 17

<!-- Page 30 -->

A. Proof of Theorem 3

In this appendix, we prove Theorem 3. We begin with a lemma showing that, for finite Lipschitz classes equipped with certificates, one can control the deviation from a given Lipschitz-continuous target function.

Lemma 8. Let X be a non-empty set. Consider a hypothesis class FΘ ⊂RX and a target function f∗∈RX. Assume f∗is Lipschitz continuous with respect to dX with Lipschitz constant Bf∗. Let r > 0, ε > 0 and assume FΘ is a finite Lipschitz class with certificates {Bθ}θ∈Θ and (pseudo-)metric dX. Consider the regularized loss LX(fθ) with regularization term Lreg(fθ).

Let X:= {xi}n i=1 be an r-cover of X of minimum cardinality, i.e., n = N(X, dX, r). If the regularized loss satisfies LX(fθ) ≤ε, then

∥fθ −f∗∥∞≤(Bθ + Bf∗)r + N(X, dX, r) ε.

Proof. Since LX(fθ) ≤ε and Lemp

X (fθ) ≥0, we have Lreg(fθ) ≤LX(fθ) ≤ε. Since X is an r-cover of X, for any x ∈X there exists xi ∈X with dX (x, xi) ≤r. By the triangle inequality and Lipschitz continuity, we that that

|fθ(x) −f∗(x)| ≤|fθ(x) −fθ(xi)| + |fθ(xi) −f∗(xi)| + |f∗(xi) −f∗(x)|

≤Bθ · dX (x, xi) + |fθ(xi) −f∗(xi)| + Bf∗· dX (x, xi)

≤(Bθ + Bf∗) · r + |fθ(xi) −f∗(xi)|.

By definition of yi, we have

1 N

N X i=1

|fθ(xi) −f∗(xi)| = Lemp

X (fθ) ≤LX(fθ) ≤ε.

Thus, max 1≤j≤N |fθ(xj) −f∗(xj)| ≤

N X j=1

|fθ(xj) −f∗(xj)| ≤Nε.

Therefore, for the xi with dX (x, xi) ≤r, we have |fθ(xi) −f∗(xi)| ≤Nε, and

|fθ(x) −f∗(x)| ≤(Bθ + Bf∗)r + Nε, for all x ∈X.

We are now ready to prove the main theorem. For completeness, we restate it below in a formal form.

Theorem 9 (Theorem 3 in the main text). Let X be a non-empty set, let FΘ be a finite Lipschitz class through the (pseudo)metric dX, and let f∗be a target function. Assume there is a constant Bf∗∈R+ such that f∗is Lipschitz continuous regarding dX with Lipschitz constant

Bf∗. Moreover, suppose that, for every δ > 0, there exists θ satisfying supx∈X |fθ(x)−f∗(x)| < δ and the certificate Bθ ≤Bf∗.

For X:= {x1,..., xn} ⊂X and given dataset {(xi, f∗(xi))}n i=1, and η > 0, consider the regularized loss LX(fθ) with Lreg

X (fθ) = ηReLU(Bθ −Bf∗), which satisfies infθ∈Θ{LX(fθ)} = 0.

<!-- Page 31 -->

Then, for ε ∈(0,1), there exists r > 0 and ε′ > 0 such that if we take a dataset X that is an r-cover of minimum cardinality with |X| = Kr = N(X, dX, r), then

LX(fθ) < ε′, implies

|fθ(x) −f∗(x)| < ε, for all x ∈X.

In particular, the above conclusion holds for r = ε 6(1+Bf∗) and any ε′ < min n ε 3N(X,d,r), εη 6(1+Bf∗)

o

; in this case, the required number of samples is Kr = N(X, dX, r).

Proof. We recall that we assume that, for every δ > 0, there exists θ satisfying supx∈X |fθ(x) − f∗(x)| < δ and the certificate Bθ ≤Bf∗. This implies that there exists a sequence fθk such that ∥fθk −f∗∥∞→0 and Bθk ≤Bf∗.

Note

Lreg(fθ) = ηReLU(Bθ −Bf∗) ≤B, implies

Bθ ≤1 ηB + Bf∗.

Choose r = ε 6(1+Bf∗), let Kr = N(X, dX, r), and choose ε′ < min n ε 3Kr, εη 6(1+Bf∗)

o

. By the assumption on Fθ, there exists an r-cover X with |X| = Kr.

Let L:= infθ∈Θ{LX(fθ)}. We claim that L = 0. Indeed, consider the sequence {fk} and {Bθk} mentioned earlier. Then Bθk ≤Bf∗and thus Lreg(fθk) = 0. Further Lemp

X (fθk) ≤ ∥f∗−fθk∥∞→0. Therefore

L = inf θ∈Θ{LX(fθ)} ≤lim k→∞LX(fθk) = 0.

Now we apply Lemma 8 to the set X = {xi}Kr i=1, which is an r-cover by construction. We consider the dataset {(xi, f∗(xi))}Kr i=1. By assumption, LX(fθ) < ε′. Hence, we have ηReLU(Bθ −Bf∗) < ε′, which implies Bθ < Bf∗+ ε′ η ≤Bf∗+ ε 6(1+Bf∗). Thus by Lemma 8,

∥fθ −f∗∥∞≤(Bθ + Bf∗)r + Krε′

≤

Bf∗+ ε 6(1 + Bf∗) + Bf∗

!

· ε 6(1 + Bf∗) + Kr · ε 3Kr

=

2Bf∗+ ε 6(1 + Bf∗)

!

· ε 6(1 + Bf∗) + ε 3

= 2Bf∗ε 6(1 + Bf∗) + ε2

36(1 + Bf∗)2 + ε 3.

<!-- Page 32 -->

We now assume ε < 1 so that ε2 36(1+Bf∗)2 ≤ ε 36, and observe that Bf∗ 1+Bf∗< 1. From these inequalities, it follows that

∥fθ −f∗∥∞< ε

3 · Bf∗ 1 + Bf∗+ ε 3 + ε 36

< ε

3 + ε 3 + ε 36

= 2ε

3 + ε 36

= 24ε

36 + ε 36 = 25ε 36 < ε.

The required number of samples is Kr = N(X, dX, r) where r = ε 6(1+Bf∗).

B. Learning non-realizable functions

This appendix records a variant of Theorem 3 that applies to a larger class of target functions, particularly functions that cannot be approximated with a bounded Lipschitz constant. The approximation properties of the target are summarized by a certificate profile, which captures how large a certificate budget is required to approximate the target to a given accuracy.

Certificate profile Let (X, dX) be a pseudo-metric space and let FΘ = {fθ: X →R | θ ∈Θ} be a hypothesis class. Assume that for each θ ∈Θ we can compute a certificate Bθ ∈R+ such that fθ is Bθ-Lipschitz with respect to dX. For a target function f∗: X →R and ε > 0, define eBf∗(ε):= inf n

B ≥0

∃θ ∈Θ: ∥fθ −f∗∥∞≤ε and Bθ ≤B o

. (4)

Note that eBf∗(ε) may be finite even if f∗/∈FΘ.

Lemma 10. Let f∗: X →R be a target and fix ε ∈(0,1), η > 0, and ε′ > 0. Set r:= ε

4 1 + 2 eBf∗(ε/4) + ε′/η

. (5)

Let X = {x1,..., xK} ⊂X be a minimum-cardinality r-cover (so K = N(X, dX, r)) and set yi:= f∗(xi). For fθ ∈FΘ, define

LX(fθ):= 1 K

K X i=1

|fθ(xi) −yi| + η ReLU(Bθ −eBf∗(ε/4)). (6)

If LX(fθ) ≤ε′ and ε′ ≤ ε 4K, (7)

then ∥fθ −f∗∥∞≤ε. In particular, taking B = eBf∗(ε/4) yields the sample size

K(ε, η, ε′) = N

X, dX, ε

4 1 + 2(eBf∗(ε/4) + ε′/η

!

.

<!-- Page 33 -->

Proof. By the definition of eBf∗(ε/4) there exists θ∗∈Θ such that

∥fθ∗−f∗∥∞≤ε/4 and Bθ∗≤B. (8)

If LX(fθ) ≤ε′, then the regularizer term in (6) satisfies η ReLU(Bθ −eBf∗(ε/4)) ≤ε′, hence ReLU(Bθ −eBf∗(ε/4)) ≤ε′/η and therefore

Bθ ≤eBf∗(ε/4) + ε′/η. (9)

Since yi = f∗(xi), we have

1 K

K X i=1

|fθ(xi) −f∗(xi)| ≤LX(fθ) ≤ε′.

Hence, max 1≤i≤K |fθ(xi) −f∗(xi)| ≤

K X i=1

|fθ(xi) −f∗(xi)| ≤K ε′. (10)

Fix x ∈X and choose xi ∈X with dX (x, xi) ≤r. Using the triangle inequality,

|fθ(x) −f∗(x)| ≤|fθ(x) −fθ∗(x)| + |fθ∗(x) −f∗(x)|.

The second term is at most ε/4 by (8). For the first term, Lipschitz continuity of fθ and fθ∗ yields

|fθ(x) −fθ∗(x)| ≤|fθ(x) −fθ(xi)| + |fθ(xi) −fθ∗(xi)| + |fθ∗(xi) −fθ∗(x)|

≤(Bθ + Bθ∗) d(x, xi) + |fθ(xi) −fθ∗(xi)|

≤(Bθ + Bθ∗) r + |fθ(xi) −f∗(xi)| + |f∗(xi) −fθ∗(xi)|.

By (9) and (8), Bθ + Bθ∗≤(B + ε′/η) + B, and by (10) and (8),

|fθ(xi) −f∗(xi)| ≤Kε′, |f∗(xi) −fθ∗(xi)| ≤ε/4.

Combining these bounds gives

|fθ(x) −f∗(x)| ≤(Bθ + Bθ∗) r + Kε′ + ε/2. (11)

By the choice of r in (5),

(Bθ + Bθ∗) r ≤ (Bθ + Bθ∗)ε

4(1 + 2 eBf∗(ε/4) + ε′/η) ≤ε/4, and by (7), Kε′ ≤ε/4. Substituting into (11) yields |fθ(x) −f∗(x)| ≤ε. Since x ∈X was arbitrary, ∥fθ −f∗∥∞≤ε.

Remark 11. The dependence on η and the tolerance ε′ appears through the term ε′/η in (5): weaker regularization (smaller η) permits larger certificates Bθ ≤eBf∗(ε/4)+ε′/η, which shrinks the admissible cover radius and increases the sample size N(X, dX, r). Conversely, stronger regularization tightens certificate control, but may increase the achievable regularized loss when an accurate approximation requires larger budgets (as captured by eBf∗(·)).

<!-- Page 34 -->

C. Improved learning guarantees for SSSPs algorithms

While the above sections derive conditions under which a finite training dataset exists, and the algorithm can be learned, here we derive a concrete, small training dataset for learning the Bellman–Ford algorithm for the SSSP problem. Our analysis significantly extends the analysis of Nerem et al. [82] by deriving a simpler training dataset and, unlike the former work, a differentiable regularization term.

In the following, we formalize the Bellman–Ford update, which corresponds exactly to the update performed by the Bellman–Ford algorithm at each iteration on all vertices of a graph. Our objective is to learn the K-fold application of this update.

Definition 12 (Bellman–Ford instance, update, and distance). An attributed, edge-weighted graph G is called a Bellman–Ford instance (BF instance) if both its vertex labels aG(v) ≥0, for all v ∈V (G), and its edge weights wG(e) ≥0, for all e ∈E(G), are non-negative real-valued functions. For notational convenience, we additionally assume that

NG(v):= NG(v) ∪{v}, wG(v, v) = 0, for all v ∈V (G).

We denote by GBF the set of all BF instances. We further define the map Γ: GBF →GBF to be the operator that maps a BF instance G to the BF instance Γ(G) with the same vertices, edges, and edge weights as G, but whose vertex labels are updated according to aΓ(G)(v):= min{aG(u) + wG(u, v): u ∈NG(v)}, for v ∈V (G).

We refer to Γ as the Bellman–Ford update. Note that Γ(G) ∈GBF, for G ∈GBF.

Given G ∈GBF, we define the t-step Bellman–Ford distance of a vertex v as x(t)

v:= aΓ t(G)(v), where Γ t denotes the t-fold composition of Γ.

Consequently, the learning task studied in this work is to approximate the vertex-level mapping induced by Γ K using an MPNN.

C.1. Employed MPNN architecture

Consider G ∈GBF. Let K ∈N denote the number of iterations of the Bellman–Ford Update we wish to learn. We want to employ MPNNs as defined in Section 2.2 with minimum aggregation and m-layer ReLU FNNs, where m ∈N, as update and aggregation functions. We initialize the vertex representations by setting h(0)

v:= aG(v) ∈R≥0, for v ∈V (G),

More precisely, we define the update and aggregation functions through h(t)

v:= UPD(t)

ut h(t−1)

v, AGG(t)

at n

{{ h(t−1)

v, h(t−1)

u, wG(v, u)

| u ∈N(v)}}

o

:= FNN(m) θ(t)

UPD min u∈N(v) FNN(m) θ(t)

AGG h(t−1)

u wG(v,u)

!

,

<!-- Page 35 -->

where t ∈[K], v ∈V (G), and θ(t)

UPD:= (W (UPD,t,1), b(UPD,t,1),..., W (UPD,t,m), b(UPD,t,m)), θ(t)

AGG:= (W (AGG,t,1), b(AGG,t,1),..., W (AGG,t,m), b(AGG,t,m)), are parameter sets, each consisting of m weight matrices and bias vectors of appropriately chosen dimension, which we will specify below. Finally, we denote the output of the MPNN after K message-passing steps for vertex v ∈V (G) by h(K)

v.

Global indexing and hidden dimensions Note that in the above, each weight matrix and bias vector is indexed depending on whether they belong to an update or aggregation FNN, the index t ∈[K] of the aggregation layer, and the layer index within the FNN. We now introduce an alternative global indexing, where each weight matrix and bias vector is labeled by its global position within the MPNN, from innermost to outermost. More precisely, let J:= 2mK be the number of total layers. Then define a bijection ϕ: [J]0 →{(0)} ∪{(f, t, l) | t ∈[K], l ∈[m], f ∈{AGG, UPD}}

such that

(ϕ(0), ϕ(1), ϕ(2),..., ϕ(J)):= (0, (AGG, 1,1),..., (AGG, 1, m), (UPD, 1,1),...,

(UPD, 1, m), (AGG, 2,1),..., (UPD, K, m)).

If the context allows it, we will abuse notation and write j = ϕ(j). With both indices at hand, we now want to specify the dimensions of the hidden features and, by extension, those of the parameters. Let dϕ(j) = dj ∈N denote the dimension of the feature vector of the j-th global layer. Further let dϕ(0) = d0 = 1 denote the input dimension. We then require bj ∈Rdj, W j ∈

(

Rdj×(dj−1+1) ϕ(j) ∈{(AGG, t,1) | t ∈[K]} Rdj×dj−1 otherwise, where for each edge inserting layer, i.e., a layer of the type (AGG, t,1), t ∈[K], the input dimension is given by the sum of the feature dimension of the previous layer and the dimension of edge weights (which is equal to 1). For our purposes, we will choose d0 = dJ = 1. Further, we will choose all hidden dimensions to be equal to some fixed d ∈R, except for j such that ϕ(j) ∈{(AGG, t, m) | t ∈[K]} where we let dj = 1.

In the following proofs, we will primarily use the global indexing. To identify aggregation layers, we define, for each k ∈[K], an index ak ∈[J] such that ϕ(ak) = (AGG, k, m), i.e., ak is the last layer of the k-th aggregation FNN. Similarly, to identify edge-inserting layers, we define, for each k ∈[K], an index jk ∈[J] such that ϕ(jk) = (AGG, k, 1), i.e., jk is the first layer of the k-th aggregation FNN. For convenience, we additionally set j0:= 0.

Further, we want to split the weight matrices of the edge-inserting layers into a component that acts on hidden vertex features and a component that acts on the inserted edge weights. To this end, we define

˜ W jk:=

W jk

−,1... W jk

−,d(jk−1)

∈Rdj×dj−1, Ck:=

W jk

−,d(jk−1)+1

∈Rdj×1

<!-- Page 36 -->

such that

W jk h(k−1)

u wG(v, u)

!

= ˜ W jkh(k−1)

u + CkwG(v, u).

Finally to avoid unnecessary case distinctions we redefine W jk:= ˜ W jk.

Parameter sets We define B:= (b(1),..., b(J)) ∈Q j∈[J] Rdj =: Θb as the vector of biases, C:= (C(1),..., C(K)) ∈Q k∈[K] Rdjk×1 =: ΘC as the vector of edge inserting weight matrices and W:= (W (1),..., W (J)) ∈Q j∈[J] Rdj×dj−1 =: ΘW as the vector of weight matrices acting on vertex features. Further we define θ:= (W, C, B) to denote the collection of all parameters and ΘBF:= ΘW × ΘC × Θb to denote the parameter space such that θ ∈ΘBF.

C.2. Loss function

Following Section 2.4, let

X ⊂X:= V1(GBF) = {(G, v): G ∈GBF, v ∈V (G)}

denote the training set used to learn a vertex-level invariant, and let N:= |X| be its cardinality.

For notational convenience, we identify each vertex v ∈V (G) with the pair (G, v), and write

X = {v: G ∈GBF, v ∈V (G)}

to simplify expressions in the remainder of the section.

We define the loss function acting on parameter configurations θ ∈ΘBF as the sum of the MAE loss and some weighted ℓ1-norm as regularization. More precisely, we let

L(θ):= Lemp(θ) + ηLreg(θ), for some fixed η > 0, where

Lemp(θ):= 1

N

X v∈X h(K)

v −x(K)

v

, where h(K)

v denotes the final output of the MPNN and x(K)

v is the targeted K-step BF-distance, and

Lreg(θ):=

K X k=0

J X j>jk

∥W j∥1 +

X k∈[K]

∥Ck∥1 +

J X j=1

∥bj∥1.

Remark 13. Using layer-wise indexing, one can show that the regularization rewrites as

Lreg(θ) =

X k∈[K]

m X l=2 k∥W (AGG,k,l)∥1 +

X i∈[d(UPD,k−1,m)]

k∥W (AGG,k,m)

−,i ∥1 + ∥W (AGG,k,m)

−,d(UPD,k−1,m)+1∥1

+

X k∈[K]

X l∈[m]

(k + 1)∥W (UPD,k,l)∥1 + ∥b(AGG,k,l)∥1 + ∥b(UPD,k,l)∥1

, i.e., all weight matrices acting on feature vectors of the k-th aggregation layer are weighted with k, all weight matrices acting on edge components and all bias vectors are weighted with 1, and all weight matrices of the k-th update layer are weighted with k + 1. Intuitively, the weight matrices are weighted depending on their importance for the network, which will become clearer during the proof.

<!-- Page 37 -->

C.3. Construction of the training set for learning Bellman–Ford algorithm

In the following, we outline the construction of the training set for training an MPNN to execute the K-fold Bellman–Ford update.

Definition 14 (Path graphs). Let K > 0, let w ∈RK+1

≥0, and β > 0, we now define vertexattributed, edge-weighted paths where the edge-weights are given by the entries of a real-valued vector. That is, let P(w):= Pβ(w) ∈GBF be the path graph such that

V (P(w)):= {vw

0, vw 1,..., vw K}:= {v0, v1,..., vK}

with labels aP(w)(v0) = w0, aP(w)(vi) = β, for all i ∈[K], and

E(P(w)):= {(vi−1, vi) | i ∈[K]}, where the edge-weight function wP(w): E(P(w)) →R≥0 is defined as (vi−1, vi) 7→wi, for i ∈[K].

Remark 15. Consider a graph Pβ(w) such that β > ∥w∥1. Then one can easily verify that the

K-step BF-distance of vw

K in Pβ(w) is given by x(K)

vK w = ∥w∥1.

Definition 16 (Bellman–Ford path training set). Let x ∈R≥0, and define

Sx,K:= {xe(K+1)

k | k ∈[K]0}, where {eK+1 ℓ }K ℓ=0 denotes the canonical unit-length basis of RK+1. That is, Sx,K contains scaled versions of the canonical unit-length basis vectors.

We now use these scaled vectors to define the edge weights in our training set, which consists of paths. Let K > 0, β = β(x, N) ≥2(N + x + 1) and let Pβ(w) denote an edge-weighted path as in Definition 14. We then define the Bellman–Ford path training set, parameterized by x ∈R≥0, as

TSx,K:= {vw

K | w ∈Sx,K, vw

K ∈Pβ(w)}.

C.4. Theorem

We can now state our main result for learning SSSP.

Theorem 17. Let K ∈N, assume we want to learn K-steps of Bellman–Ford, i.e., the function Γ K, using the min-aggregation MPNN architecture with K layers and m-layer FNN as update and aggregation functions as described above in Section C.1. In addition, assume that the regularization parameter η satisfies η ≥2K exp(m(K2 + 3K)), and for the edge weight scaler x of the training set TSx,K it holds x ≥4mKNη, where N is the cardinality of the training set X. Then if the Bellman–Ford path training set is contained in the training set, i.e., TSx,K ⊂X, and the loss L(θ) is within ε ≤1

2 of its global minimum, then, for any Bellman–Ford instance G ∈GBF and any v ∈V (G), h(K)

v −x(K)

v

≤ε(x(K)

v + 1), where h(K)

v is the feature representation output by the MPNN and x(K)

v is the targeted K-step BF-distance of the vertex v.

<!-- Page 38 -->

General Path Graph: K ∈N, w ∈RK+1 w1 w2 w3 wk w0 β β β β β v0 v1 v2 v3 vk−1 vk

(a) Path graph

Training set TSx,K, given x ∈R≥0, K ∈N w = xeK+1

0

0 0 0 0 x β β β β β v0 v1 v2 v3 vk−1 vk w = xeK+1

1 x 0 0 0 0 β β β β β v0 v1 v2 v3 vk−1 vk w = xeK+1

2

0 x 0 0 0 β β β β β v0 v1 v2 v3 vk−1 vk

...

w = xeK+1

K

0 0 0 x 0 β β β β β v0 v1 v2 v3 vk−1 vk

(b) Training set

**Figure 3.** Bellman–Ford training graphs. Dots indicate omitted intermediate vertices, and edge

weights are shown on the edges. (a) General path graph associated with w ∈RK+1 as in Definition 14. The initial vertex is labeled a(v0) = w0, while all other vertices have label β ≫0. The path has length K with edge weights w1,..., wK. (b) Bellman– Ford training set for arbitrary K as defined in Definition 16, consisting of K + 1 path graphs corresponding to the scaled unit vectors xeK+1

0,..., xeK+1

K. Each path contains K + 1 vertices v0,..., vK. The root vertex satisfies a(v0) = x if k = 0 and a(v0) = 0 otherwise, while all other vertices have label β. Exactly one edge per path has weight x, and all remaining edges have weight 0.

This theorem differs from the main theorem of Nerem et al. [82] in several ways. On the positive side, our result uses a smaller training set, namely K + 1 path instances from TSx,K, and replaces their non-differentiable ℓ0 penalty with a differentiable ℓ1 regularizer that has layer-specific weights w(k). This differentiability allows our loss to be optimized directly. On the other hand, our analysis assumes a more restricted model: the depth is fixed to exactly K message-passing layers (matching K Bellman–Ford steps), and the aggregation dimension is 1. These choices are made to simplify the analysis. Furthermore, unlike Nerem et al. [82], the regularization parameter η and the training weight scale x both scale exponentially in K, which may be prohibitive in some settings.

D. Proof of Theorem 17

We begin with a proof outline that highlights the main lemmas and ideas underlying the argument.

<!-- Page 39 -->

D.1. Proof outline

Here, we outline the high-level idea of the proof, broken down into its key aspects.

Section D.3: Properties of FNNs The aim of this section is to develop algebraic properties of FNNs that are needed to handle the ReLU nonlinearity and to investigate the dependence of the network output on its weights and biases. Later, we will see that the features produced by the MPNN can be upper-bounded by the output of a single FNN of depth J (the total number of global layers of the MPNN), which is where the results derived in this section will be applied.

The main results include linearity of FNNs in the regime where all parameters are nonnegative, as well as monotonicity with respect to both the network parameters and the input. The key ingredient is that, for non-negative inputs, the ReLU activation acts as the identity. In addition, we prove the following corollary.

Corollary 18. Let W ∈ΘW and B, BC ∈Θb. Then for any y ∈Rd0

≥0 it holds

FNN(J)(W, B + BC)(y) −FNN(J)(W+, B+

C)(y)

≤G(W, BC)(y) + FNN(J)(|W|, |B|)(0).

The RHS consists of two terms, each capturing a distinct source of deviation. The second term, FNN(J)(|W|, |B|)(0), can be interpreted as the maximal influence that non-zero biases may exert on the network output. In particular, once we establish that the biases are small, this term becomes negligible.

The first term, G(W, BC)(y), is defined as a sum of auxiliary FNNs and quantifies the maximal contribution of negative weights. After proving that all negative weights must be close to zero near optimality, this term is likewise small. Consequently, the entire RHS provides a controlled error term.

Interpreting the LHS in the MPNN setting, B represents the collection of biases of the MPNN, while BC has the same structure and encodes the contribution of edge features along a path to a node v in the training set. Thus, the LHS measures the difference between the output of the MPNN with parameters (W, C, B) (cf. Section C.1) and that of the MPNN with parameters (W+, C+, 0), i.e., where all weights are replaced by their positive parts and all biases are set to zero.

The latter parameter configuration is significantly easier to analyze, since the effects of the ReLU nonlinearity and the biases vanish. Hence, this corollary allows us to replace the original MPNN features by those of the simplified network up to an error controlled by the RHS.

Section D.4: FNNs along computation trees In this section, we define the set of computation trees T K

G (v) that encodes all possible choices during aggregation. We then define the FNN along a computation tree t ∈T K

G (v), denoted by H(k)(θ)(t). Intuitively, this quantity represents the feature that the MPNN would output if the aggregation followed the computation tree t.

This framework allows us to define the set of minimum-aggregation trees T k

G,θ(v), i.e., the computation trees selected by the min-aggregation. In particular, the feature of the MPNN can be written as an FNN evaluated along a minimum-aggregation tree.

Lemma 19. Let G ∈GBF, v ∈V (G), and θ ∈ΘBF. Then for any k ∈[K]0 and any τ k v ∈T k

G,θ(v), h(k)

v = H(k)(θ)(τ k v).

<!-- Page 40 -->

The main purpose of introducing FNNs along computation trees is to enable comparisons between the MPNN output and the output obtained from alternative computation trees. In particular, this allows us to upper-bound the MPNN features by FNNs evaluated along trees that are not chosen by the MPNN itself.

This idea is formalized in the next lemma, which shows that although the MPNN performs a layer-wise, “greedy” minimization, the resulting computation tree τ k v ∈T K

G,θ(v) minimizes the feature globally, up to the effect of negative weights.

Lemma 20. Let G ∈GBF, v ∈V (G), and θ ∈ΘBF. Then for any k ∈[K]0, τ k v ∈T k

G,θ(v), and tk v ∈T k

G(v) it holds

H(k)(θ)(τ k v) ≤H(k)(θ+)(tk v)

element-wise.

This is the point where the use of min-aggregation becomes crucial.

Section D.5: walk-lifted FNNs In this section, we define the walk-lifted FNN Hwl(θ)(z), where z ∈RK+1

≥0, which can be represented as an FNN with suitably chosen biases. As a consequence, it inherits all properties derived in Section D.3. In particular, Corollary 18 translates directly into the following corollary for walk-lifted FNNs.

Corollary 21. For all z ∈RK+1

≥0 and parameters (W, C, B) ∈ΘBF, it holds Hwl(W, C, B)(z) −Hwl(W+, C+, 0)(z)

≤G

W, B(z, C)

(z) + Hwl(|W|, |C|, |B|)(0).

Here, B(z, C) represents the effective bias induced by the edge features encoded in z and the parameters C. As before, the right-hand side compares the walk-lifted FNN with arbitrary parameters to the corresponding object with non-negative weights and vanishing biases.

We further show that the walk-lifted FNN coincides with the FNN along a computation tree whenever the computation tree is essentially a walk.

Lemma 22. Let G ∈GBF and (W, C, B) = θ ∈ΘBF. Then for any v ∈V (G) and any p ∈PK

G (v) it holds

Hwl(θ)(zp) = H(k)(θ)(tK(p)).

Here, p should be interpreted as a walk in the graph G, tK(p) as its corresponding computation tree representation, and zp as a vector encoding the edge weights along p.

Combining the three lemmas above, we obtain the following result, which allows us to replace the MPNN features with walk-lifted FNN features.

Lemma 23. Let θ ∈ΘBF and G ∈GBF. Then for any v ∈V (G) and any p ∈PK

G (v) it holds h(K)

v ≤Hwl(θ+)(zp), and h(K)

v = Hwl(θ)(zp), if tK(p) ∈T K

G,θ(v).

Here, tK(p) denotes the computation tree associated with p. The condition tK(p) ∈T K

G,θ(v) means that the successive minimum-aggregations in the MPNN select exactly the nodes along the path p, that is, in each layer the aggregation chooses the next vertex on p. In the subsequent sections, this lemma will serve as the key ingredient for replacing MPNN features with an object that is significantly easier to control and analyze.

<!-- Page 41 -->

Section D.6: Small empirical loss and structure of parameters The goal of this section is to show that if the loss is close to its global minimum and if the parameters η and x are chosen sufficiently large, then the network parameters must exhibit a highly constrained structure. More precisely, we prove that

• all biases are close to zero, i.e. B ≈0,

• all weights are either positive or close to zero, i.e. W−≈0,

• the factors multiplying edge weights are approximately equal to 1 or larger,

• the empirical loss is small, i.e. Lemp ≤2ε.

The key idea underlying this analysis is that the parameters are subject to two competing forces.

• Regularization, which pushes all parameters toward zero, and

• Empirical loss, which pushes those parameters necessary to fit the targets toward 1.

We begin by introducing a constant L ∈R>0 and show that ηL is an upper bound on the global minimum of the loss, i.e., min θ∈ΘBF L(θ) ≤ηL.

In fact, ηL is the global minimum, which we establish implicitly at the end of the section.

Next, we derive coarse a priori bounds on the effect that non-zero biases and negative weights can have on the MPNN output, uniformly over all seen and unseen inputs.

Corollary 24. Let θ ∈ΘBF and 0 ≤ε ≤ηL. Assume that L(θ) lies within ε of its global minimum. Then

Hwl(|W|, |C|, |B|)(0) ≤exp(L)

J X j=1

∥bj∥1,

G(W, B(z, C))(z) ≤exp(L)

J X l=1

∥(W l)−∥1 +

K X k=1

∥(Ck)−∥1

∥z∥1, z ∈RK+1

≥0.

Here, Hwl(|W|, |C|, |B|)(0) = P l∈[J]

Q j>l

W j bl represents the maximal deviation that the biases B = (b1,..., bJ) can induce in the MPNN output. Similarly, G(W, B(z, C))(z) bounds the maximal contribution of negative weights.

Controlling both quantities is crucial, since their sum appears on the right-hand side of Corollary 21 and thus governs the error incurred when replacing the original parameters (W, C, B) by the simplified configuration (W+, C+, 0). The exponential dependence on L arises from bounding products of the form Q j>l

W j solely in terms of P j>l∥W j∥1 ≤L(θ) ≤2ηL. We then introduce a reduced set of transformed parameters together with a modified loss function. The key idea is that this new loss depends on fewer variables while still capturing the essential behavior of the original optimization problem.

Definition 25 (Modified loss function). Given θ = (W, C, B) ∈ΘBF, we define the transformed parameters

˜θ:= (γ0,..., γK, B, w−) ∈RK+3

≥0.

<!-- Page 42 -->

To avoid case distinctions, we introduce C0:= 1. We then set γk:=

J Y j=jk+1

(W j)+(Ck)+, k ∈{0,..., K},

B:= ∥B∥1, w−:=

J X l=1

∥(W l)−∥1 +

K X k=1

∥(Ck)−∥1.

We define the modified loss

˜L(˜θ):= ˜Lemp(˜θ) + η ˜Lreg(˜θ), where

˜Lemp(˜θ):= 1

N

K X k=0 σ

(1 −γk)x −exp(L)B

,

˜Lreg(˜θ):= B +

K X k=0 lkγ1/lk k + w−.

Up to negative parameters, γk represents the factor by which the k-th edge weight along an aggregation path is multiplied, while B and w−capture the total magnitude of biases and negative weights, respectively. Our objective is therefore to show that B ≈0, w−≈0, and γk ≈1.

To justify working with ˜L instead of L, we show that near-optimality of the original loss implies near-optimality of the modified loss. Since the regularization terms are chosen such that both losses attain the same global minimum ηL, it suffices to prove that ˜L(˜θ) ≤L(θ).

In fact, we prove the following.

Lemma 26. Let θ = (W, C, B) ∈ΘBF and let ˜θ denote its transformed parameter vector. Assume TSx,K ⊂X and that L(θ) lies within ε ≤ηL of its global minimum. Then

Lemp(θ) ≥˜Lemp(˜θ), Lreg(θ) ≥˜Lreg(˜θ).

To prove the empirical-loss inequality Lemp(θ) ≥˜Lemp(˜θ), we upper bound the MPNN features h(K)

v using Lemma 23. and the a priori bound from Corollary 24, to obtain h(K)

v ≤

K X k=0 γkzk + exp(L)B, where z ∈RK+1 denotes the edge weights along a shortest path to v. By the choice of training samples TSx,K, we have PK k=0 γkzk = γkx, for some k ∈[K]. Consequently, x(K)

v −h(K)

v

≥σ x −γkx −exp(L)B

.

Summing over all samples in TSx,K yields Lemp(θ) ≥˜Lemp(˜θ).

<!-- Page 43 -->

To establish Lreg(θ) ≥˜Lreg(˜θ), we exploit the specific structure of the regularizer. For each k ∈[K]0 and each weight matrix appearing in γk =

J Y j=jk+1

(W j)+(Ck)+, there exists exactly one corresponding normalized term in the regularization. A variational argument, combined with a separation of biases and negative weights from the remaining terms, yields the claimed bound.

Based on this lemma, we now characterize parameter configurations whose loss is close to the global minimum.

Lemma 27 (Parameter characterization near the global minimum). Let θ ∈ΘBF. Assume TSx,K ⊂X and that L(θ) lies within 0 ≤ε ≤ηL of its global minimum. Further assume η ≥2K exp(L) and x ≥2NηJ.

Then the following estimates hold:

Hwl(|W|, |C|, |B|)(0) ≤ε, (12)

γk ≥1 −ε ηJ, k ∈[K]0, (13)

and, for any z ∈RK+1

≥0, Hwl(W, C, B)(z) −Hwl(W+, C+, 0)(z)

≤

1

2∥z∥1 + 1 ε. (14)

Moreover,

Lemp(θ) ≤2ε.

The estimate (12) implies that the effect of the biases on the MPNN output is negligible, i.e. B ≈0. The bound (13) shows that the factors multiplying the edge weights are close to one (or larger). Inequality (14) allows us to replace MPNN features along a path by the simpler expression Hwl(W+, C+, 0)(z), and the final inequality ensures that the empirical loss is small.

The key idea in the proof is that the previous lemma allows us to analyze the modified loss ˜L instead of L. The modified loss removes couplings between the factors γk and eliminates ReLU nonlinearities between layers, thereby isolating the two competing forces acting on the parameters. The regularization drives B, the negative weights w−, and the factors γk, k ∈[K]0, toward zero, while the empirical loss pushes B and the γk’s away from zero. This implies w−≈0. Since exp(L) < η by assumption, the regularization force on B dominates, yielding B ≈0. Finally, for sufficiently large x, the loss is minimized when γk ≈1, which implies that the regularization loss is approximately L and hence that the empirical loss is small.

Section D.7: Upper and lower nound In this section, we additionally assume that the hidden dimension before each minimum aggregation is equal to 1. Intuitively, this restriction ensures that the minimum aggregation cannot decrease hidden features on graphs that contain more branching than simple path graphs, which provide strictly fewer aggregation options. As a result, path graphs represent the worst case for the minimum operator.

Formally, this assumption implies that the MPNN features can be expressed via a walk-lifted FNN along any computation path. This allows us to apply the parameter characterization from Lemma 27 and deduce the following lower bound.

<!-- Page 44 -->

Corollary 28 (Lower bound). Let θ ∈ΘBF, η ≥2K exp(L), and x ≥2NηJ. Assume TSx,K ⊂X and that L(θ) lies within 0 ≤ε ≤ηL of its global minimum. Then for any G ∈GBF, v ∈V (G), and t ∈T J θ (v), h(K)

v ≥(1 −ε) ∥zt∥1 −ε.

In particular, h(K)

v ≥(1 −ε) x(K)

v −ε, where x(K)

v denotes the Bellman–Ford distance.

The first inequality shows that the MPNN features can be bounded from below by approximately the length of any min-aggregation computation path. Since, by definition, the Bellman–Ford distance x(K)

v is the minimal length among all paths ending at v ∈V (G), this immediately implies the claimed lower bound.

We next establish the corresponding upper bound. Here, an additional difficulty arises, i.e., although the modified loss is minimized at γk = 1, it does not provide a tight a priori upper bound on γk, since the additional regularization cost incurred by choosing γk > 1 is relatively small. We therefore first show that excessively large values of γk necessarily lead to overly large MPNN features and hence to an empirical loss that is too large. This observation allows us to control γk from above and, in combination with Lemma 23, to derive the desired upper bound.

Theorem 29 (Upper bound). Let θ ∈ΘBF, η ≥2K exp(L), and x ≥2NηJ. Assume TSx,K ⊂X and that L(θ) lies within 0 < ε < 1

2 of its global minimum. Then, for any G ∈GBF and any v ∈V (G), h(K)

v ≤(1 + ε) x(K)

v + ε.

Combining the lower and upper bounds yields the claimed theorem.

D.2. Outlook

In this subsection, we outline several directions in which the results of this paper can be strengthened and extended.

Removing the exponential dependence on η without biases We first observe that if all biases are set to zero, the proofs reveal that the exponential lower bound on the regularization parameter η is no longer necessary. In this setting, the arguments can be repeated with only minor modifications, yielding the following result.

Theorem 30. Let K ∈N and suppose we aim to learn K steps of the Bellman–Ford algorithm, i.e. the function Γ K, using a min-aggregation MPNN with K layers and m-layer feedforward neural networks as update and aggregation functions, as described in Section C.1, but without any biases. Assume that the Bellman–Ford path training set is contained in the training set, i.e. TSx,K ⊂X, and that the edge-weight scaling satisfies x ≥4mKNη, where N:= |X| is the cardinality of the training set.

Then there exists a constant C > 0 such that if L(θ) lies within 0 ≤ε < min{η2mK(K+3), 1

2} of its global minimum, then for any Bellman–Ford instance G ∈GBF and any v ∈V (G), h(K)

v −x(K)

v

≤ε C x(K)

v, where h(K)

v denotes the MPNN feature representation and x(K)

v the target K-step Bellman–Ford distance.

<!-- Page 45 -->

Edge case graph G(x, K) for K = 4 x x x x x

0 0 0 0

0 0 0

0 0

0

0

0

0

0 v−1 v0 p1,0 p2,0 p3,0 p4,0 v1 p2,1 p3,1 p4,1 v2 p3,2 p4,2 v3 p4,3 v4

**Figure 4.** Edge case graph from Definition 31 for learning the K-fold Bellman–Ford update with

higher aggregation dimension. The root vertex is v−1. Shown here is the instance for K = 4. At each vertex vi, i ∈[K], the network can choose between multiple paths of equal total weight x.

Removing the exponential dependence with biases The exponential lower bound on η can also be removed without eliminating biases by including the Bellman–Ford path training set twice with different edge-weight scalings, for example, by assuming that TSx,K, TS2x,K ⊂X. By comparing feature values obtained from identical path graphs with different scalings, we can eliminate the bias terms in a first step and show that Lemp(θ) ≤2ε and B ≤ε/η without any restriction on η. In a second step, bounds analogous to those in Lemma 27 can be derived. The proofs of the upper and lower bounds then remain unchanged.

Extension to ℓ1-regularization We further aim to generalize our analysis to standard ℓ1regularization. From a theoretical perspective, we conjecture that size generalization results as in Theorem 17 continue to hold in this setting, though potentially with weaker error bounds and increased optimization difficulty.

Removing the one-dimensional aggregation assumption Finally, we seek to remove the assumption that the hidden dimension before each aggregation equals one, i.e. to extend the theory to dak > 1. This assumption is only used in Section D.7. For higher aggregation dimensions, the minimum operator may exploit additional degrees of freedom and produce feature values that are significantly smaller than the true shortest-path distance, thereby breaking generalization. We conjecture that this issue can be resolved by augmenting the training set with a carefully designed edge case graph that forces the MPNN to confront the most extreme configurations of shortest paths.

Definition 31 (Edge case graph). Let x > 0 and K ∈N. We define the edge case graph G(x, K) = (V, E) as follows.

<!-- Page 46 -->

First, add a path with vertices v−1, v0,..., vK ∈V and edges (vi−1, vi) ∈E for i ∈[K]0, with edge weights w(v−1, v0) = x and w(vi−1, vi) = 0 for all i ∈[K].

Next, for each i ∈[K], add a path of length i + 1 from v−1 to vi whose edge weights are zero except for the final edge, which has weight x. More precisely, for each i ∈[K] we introduce vertices pi,j ∈V for j ∈[i −1]0 and edges

{v−1, pi,0}, {pi,0, pi,1},..., {pi,i−2, pi,i−1}, {pi,i−1, vi} ∈E, with weights w({v−1, pi,0}) = w({pi,0, pi,1}) = · · · = w({pi,i−2, pi,i−1}) = 0, w({pi,i−1, vi}) = x.

Finally, we assign vertex features corresponding to the one-step Bellman–Ford distances with root vertex v−1. Specifically, we set a(v−1) = a(pi,0) = 0 for all i ∈[K], a(v0) = x, and a(v) = β for all remaining vertices v ∈V \ {v−1, p1,0,..., pK,0, v0}, where β > 0 is chosen sufficiently large.

We conjecture that augmenting the training set with the edge case graph G(x, K) suffices to restore size generalization guarantees with a constant aggregation dimension, and that, in this regime, the performance gap between The tailored loss used in this work and the standard ℓ1-loss vanish.

D.3. Properties of FNNs

In the following, let J ∈N and (d0,..., dJ) ∈NJ+1 be fixed.

Remark 32. By definition of the feedforward neural network (see Section 2.2), for any parameters θ = (W, B) ∈Θ and any input x ∈Rd0, we have

FNNJ

0 (θ)(x) = x, and for all j ≥1,

FNNJ j (θ)(x) = σ

W (j) FNNJ j−1(θ)(x) + b(j).

We will repeatedly use this recursive representation in inductive arguments.

Remark 33. We regard W ∈ΘW, B ∈Θb, and θ ∈Θ as vectors in their respective parameter spaces. Accordingly, element-wise operations on W, B, or θ are defined componentwise on the matrices W (j) and vectors b(j), j ∈[J]. For example,

B+:=

(b(1))+,..., (b(J))+, and operations such as B + B′ for B, B′ ∈Θb are well defined.

Lemma 34 (Linearity). Let θ:= (W, B) ∈Θ and assume that all parameters of θ are (element-wise) non-negative. Then for all j ∈[J]0 and y ∈Rd0

≥0 it holds that

FNN(J)

j (W, B)(y) = j X l=1 jY s=l+1

W s b l + jY s=1

W s

(y).

<!-- Page 47 -->

Lemma 35. Let j ∈[J]0, y1, y2 ∈Rd0

≥0, and θ1:= (W1, B1), θ2:= (W2, B2) ∈Θ. Assume that y1 ≤y2, θ1 ≤θ2 and W2 ≥0 element-wise. Then it holds that

FNN(J)

j (W1, B1)(y1) ≤FNN(J)

j (W2, B2)(y2), element-wise.

Proof. Let Wi = (W 1 i,..., W J i) and Bi = (b1 i,..., bJ i) for i ∈[2]. We argue by induction on j ∈[J]0.

Base case (j = 0) It holds

FNN(J)

j (W1, B1)(y1) = y1 ≤y2 = FNN(J)

j (W2, B2)(y2).

Induction step Assume the statement holds for j −1, then we obtain

FNN(J)

j (W1, B1)(y1) = σ

W j

1 FNN(J) j−1(W1, B1)(y1) + bj

1 (since FNN(J)

j−1(W1, B1)(y1) ≥0)

≤σ

W j

2 FNN(J) j−1(W1, B1)(y1) + bj

2 (since W j

2 ≥W j 1, bj 2 ≥bj 1)

≤σ

W j

2 FNN(J) j−1(W2, B2)(y2) + bj

2 (induction hypothesis and W j

2 ≥0)

= FNN(J)

j (W2, B2)(y2).

Thus, the inequality holds for j, completing the proof.

Lemma 36 (Lipschitz–type inequality). Let j ∈[J]0, y1, y2 ∈Rd0, W ∈ΘW, and B1, B2 ∈Θb. Then, the following holds

FNN(J)

j (W, B1)(y1) −FNN(J)

j (W, B2)(y2)

≤FNN(J)

j (|W|, |B1 −B2|)(|y1 −y2|), element-wise.

Recall that |W| denotes the vector or collection of biases where the absolute value is applied point-wise to all parameters, i.e. |W|:= (

W 1,...,

W J) where (|W |j)l,k =

(W j)l,k for all j ∈[J] and indexes l, k.

Proof. As before, we let Bi = (b1 i,..., bJ i) for i = 1,2. We proceed by induction on j ∈[J]0.

Base case (j = 0) It holds

FNN(J)

0 (W, B1)(y1) −FNN(J) 0 (W, B2)(y2) = |y1 −y2| = FNN(J)

0 (|W|, |B1 −B2|)(|y1 −y2|).

Induction step Assume the statement holds for j −1. Since ReLU satisfies |σ(a) −σ(a′)| ≤|a −a′|, we obtain

FNN(J)

j (W, B1)(y1) −FNN(J)

j (W, B2)(y2)

≤|W j|

FNN(J)

j−1(W, B1)(y1) −FNN(J)

j−1(W, B2)(y2)

+ |bj

1 −bj 2|.

<!-- Page 48 -->

By the induction hypothesis,

FNN(J)

j−1(W, B1)(y1) −FNN(J)

j−1(W, B2)(y2)

≤FNN(J)

j−1(|W|, |B1 −B2|)(|y1 −y2|).

Substituting gives

FNN(J)

j (W, B1)(y1) −FNN(J)

j (W, B2)(y2)

≤|W j| FNN(J)

j−1(|W|, |B1 −B2|)(|y1 −y2|) + |bj

1 −bj 2|

= FNN(J)

j (|W|, |B1 −B2|)(|y1 −y2|).

This completes the induction.

Next, we study how negative parameters affect the outputs of FNNs.

Definition 37. Let W ∈ΘW, and B ∈Θb. For l ∈[J] define

Bl:= (b1, b2,..., bl−1, 0,...) ∈Θb and

Wl:= ((W 1)+,..., (W l−1)+, (W l)−, (W l+1)+,..., (W J)+) ∈ΘW

Definition 38. Let W ∈ΘW, and B1, B2, B ∈Θb. For j ∈[J]0, define

Gj(W, B1, B2)(y):= j X l=1

FNN(J)

j (Wl, Bl

1)(y) + FNN(J) j (W+, B2)(0), and

G(W, B)(y):= GJ(W, B+, B−)(y).

Remark 39 (Intuition for G). We see that in the case of G(W, B)(y), all parameters of all FNNs that are being summed over in the above definition are positive. Thus we can apply Lemma 34 to see that, for any y ∈Rd0

≥0,

G(W, B)(y) =

X l∈[J]0 l−1 X l′=0

(W J)+... (W l+1)+(W l)−(W l−1)+... (W l′+1)+(bl′)+

+

X l′∈[J]0

J Y s=l′+1

(W s)+

(bl′)−,

(15)

where we let b0:= y for notational convenience.

Note that the right-hand side can be interpreted as follows: it corresponds to evaluating FNNJ j (W, B)(y) after replacing all weight matrices and bias vectors by their positive parts, except for exactly one of them, which is replaced by its negative part, and then summing over all such choices.

For the estimates that follow, we aim to bound the difference between the output of the MPNN with parameters (W, C, B) (cf. Section C.1) and that of the MPNN with parameters (W+, C+, 0), i.e., where all weights are replaced by their positive parts and all biases are set to zero.

The next lemma provides a first step toward such a bound using the function G. It has the flavor of an inclusion–exclusion lower bound and formalizes the idea of swapping a single weight matrix or bias vector with its negative part.

<!-- Page 49 -->

Remark 40 (Upper bound on G). When deriving error bounds on the loss and parameters in

Section D.6 we will need to bound G(W, B)(y). We will do this through

∥G(W, B)(b0)∥1 ≤

X l∈[J]0 l−1 X l′=0

J Y s=l′+1 s̸=l

∥(W s)+∥1

∥(W l)+∥1∥(bl′)+∥1 +

X l′∈[J]0

J Y s=l′+1

∥(W s)+∥1

∥(bl′)−∥1, where ∥W j∥1 = P k∈[dj]

P l∈[dj−1]

W j k,l denotes the 1-norm of matrices, which is not to be understood as a point-wise application in contrast to the absolute value |·| and the positive part (·)+. Note that this is a direct consequence of Equation (15).

Lemma 41. Let W ∈ΘW, and B1, B2, B ∈Θb such that B1 −B2 = B, and B1, B2 ≥0. Then for any y ∈Rd0

≥0 it holds

FNN(J)

j (W, B)(y) ≥FNN(J)

j (W+, B1)(y) −Gj(W, B1, B2)(y).

Proof. We argue by induction over j.

Base case j = 0 Since G0(W, B1, B2)(y) = 0,

FNN(J)

0 (W, B)(y) = y = FNN(J) 0 (W+, B1)(y) −G0(W, B1, B2)(y).

Inductive step In the following, we omit the argument (y) whenever it is clear from the context. Let j > 0 and assume the claim holds for j −1. Using W j = (W j)+ −(W j)−, the induction hypothesis and Lemma 35

FNN(J)

j (W, B) = σ

W jFNN(J)

j−1(W, B) −bj

= σ

(W j)+FNN(J)

j−1(W, B) −(W j)−FNN(J)

j−1(W, B) + bj

1 −bj 2

≥(W j)+ FNN(J)

j−1(W+, B1) −Gj−1(W, B1, B2)

−(W j)−FNN(J)

j−1(W+, B) + bj

1 −bj 2

=

(W j)+FNN(J)

j−1(W+, B1) + bj

1

−

(W j)+Gj−1(W, B1, B2) + (W j)−FNN(J)

j−1(W+, B) + bj

2

.

Since FNN(J)

j−1(W+, B) is only dependent on the first j −1 bias vectors we note that

FNN(J)

j−1(W+, B) = FNN(J)

j−1(W+, Bj) by definition of Bj (cf. Definition 37). By using the definition of G and that B2 ≥0 we obtain that

(W j)+Gj−1(W, B1, B2) + (W j)−FNN(J)

j−1(W+, B) + bj

2

= (W j)+ j−1 X l=i+1

FNN(J)

j−1(Wl, Bl

1) + (W j)−FNN(J) j−1(W+, Bj

1) + (W j)+FNN(J) j−1(W+, B2)(0) + bj

2

= j−1 X l=i+1 σ

(W j)+FNN(J)

j−1(Wl, Bl

1) + σ

(W j)−FNN(J)

j−1(W+, Bj

1) + σ

(W j)+FNN(J)

j−1(W+, B2)(0) + bj

2

= j X l=i+1

FNN(J)

j (Wl, Bl

1) + FNN(J) j (W+, B2)(0) = Gj(W, B1, B2)

Inserting this into the above equation gives

FNN(J)

j (W, B) ≥

(W j)+FNN(J)

j−1(W+, B1)(y) + bj

1

−Gj(W, B1, B2)

= FNN(J)

j (W+, B1) −Gj(W, B1, B2)

and the result follows.

<!-- Page 50 -->

The next lemma finally establishes the bound we will later use to bound the difference between the output of the MPNN with parameters (W, C, B) and that of the MPNN with parameters (W+, C+, 0).

Corollary 42. Let W ∈ΘW, and B, BC ∈Θb. Then for any y ∈Rd0

≥0 it holds

FNN(J)(W, B + BC)(y) −FNN(J)(W+, B+

C)(y)

≤G(W, BC)(y) + FNN(J)(|W|, |B|)(0).

Proof. By Lemma 35 and Lemma 34, we obtain the upper bound:

FNN(J)(W, B + BC)(y) ≤FNN(J)(W+, B+ + B+

C)(y)

≤FNN(J)(W+, B+)(0) + FNN(J)(W+, B+

C)(y) ≤FNN(J)(|W|, |B|)(0) + FNN(J)(W+, B+

C)(y).

We also obtain a lower bound by applying Lemma 36:

FNN(J)(W, B + BC)(y) ≥FNN(J)(W, BC)(y) −FNN(J)(|W|, |B|)(0).

Furthermore, by letting B1 = B+

C and B2 = B−

C in Lemma 41 we arrive at

FNN(J)(W, B + BC)(y) ≥FNN(J)(W, BC)(y) −FNN(J)(|W|, |B|)(0)

≥FNN(J)(W+, B+

C)(y) −G(W, BC)(y) −FNN(J)(|W|, |B|)(0)

Combining the upper and lower bounds yields the claimed estimate.

D.4. FNNs along computation trees

To avoid analyzing the layers of the MPNN one by one, we aim to express the entire MPNN in terms of an object that can be defined similarly to the FNN in the previous section. Unfortunately, in general, no choice of bias and weight vectors in FNN(J)(W, B)(y) can capture the full expressivity of the aggregation operation. To address this, we introduce FNNs along computation paths in this section. For an appropriate choice of the underlying tree, these networks coincide with the MPNN output.

Recall that each layer of the MPNN is given by h(t)

v:= FNN(m) θ(t)

UPD min u∈N(v) FNN(m) θ(t)

AGG h(t−1)

u wG(v,u)

!

.

For ease of notation, we write fUPD,k θ:= FNN(m) θ(k)

UPD

, fAGG,k θ:= FNN(m) θ(k)

AGG

, and use this shorthand throughout. Further, recall that we index global layers by j ∈[J], where {jk: k ∈[K]} denote the edge-inserting layers and {ak: k ∈[K]} the aggregation layers. The output dimension of the j-th global layer is denoted by dj ∈N. Parameter configurations are written as θ = (W, C, B) ∈ΘBF (see Section C.1).

Definition 43 (Rooted tree with indexed children). Let T denote the set of vertex-attributed, edge-weighted rooted trees, and let G be an edge-weighted graph. Given v ∈V (G), neighbors u1,..., ud ∈NG(v), and trees t1,..., td ∈T, we define

Tv(t1,..., td) = T ∈T

<!-- Page 51 -->

to be the rooted tree with root r labeled v, and children 1,..., d, where for each i ∈[d] the subtree rooted at i is ti and edge-weights wT (r, i):= wG(v, ui).

For t ∈T, we denote the label of its root by root(t).

Definition 44 (Set of computation trees). Let G ∈G denote a graph. We define T k

G(v), the set of computation trees of G rooted in v ∈V (G) of length k ∈[K]0 recursively as follows.

For k = 0, let T 0

G(v) be the set that contains the tree t0 v given by a single vertex r with the vertex-label at0v(r) = aG(v). For k > 0, we define

T k

G(v):= {Tv(t1,..., tdak): ui ∈NG(v), ti ∈T k−1

G (ui), i ∈[dak]}, where dak is the output dimension of the k-th aggregation.

Definition 45 (FNN along computation tree). Let G ∈GBF, and θ ∈ΘBF. We define the FNN of G and parameters θ along tk v ∈T k

G(v) recursively as follows. For k = 0 and t0 v ∈T 0

G(v) with root(t0 v) = r let

H(0)(θ)(t0 v):= at0v(r) = aG(v).

Further for k > 0 and tk v = Tv(t1,..., tdak) ∈T k

G(v) with root(tk v) = r define

H(k)(θ)(tk v):= fUPD,k θ fAGG,k θ

H(k−1)(θ)(ti)

wtkv (i,r)

i∈[dak]

!

= fUPD,k θ fAGG,k θ

H(k−1)(θ)(ti) wG(v,root(ti))

i∈[dak]

!

.

Definition 46 (Min-aggregation computation trees). Let G ∈GBF, and θ ∈ΘBF. We define T k

G,θ(v), the set of min-aggregation computation trees of G and a network θ rooted in v ∈V (G) of length k ∈[K]0 recursively as follows. For k = 0 let T 0

G,θ(v):= T 0

G(v) be the set that contains the tree given by the single vertex labeled aG(v).

For k > 0 we define

T k

G,θ(v):= n

Tv(τ1,..., τdak)

∀i ∈[dak]: τi ∈arg min τ∈Sk−1 θ (v)

fAGG,k θ

H(k−1)(θ)(τ)

wG v,root(τ)

i o

, where

Sk−1 θ (v):=

[ u∈NG(v)

T k−1

G,θ (u).

The next lemma establishes that the FNN along a min-aggregation tree rooted in v ∈V (G) is equal to the feature of v.

Lemma 47. Let G ∈GBF, v ∈V (G) and θ ∈ΘBF. Then for any k ∈[K]0 and τ k v ∈T k

G,θ(v)

h(k)

v = H(k)(θ)(τ k v)

Proof. Fix G ∈GBF, and θ ∈ΘBF. We prove the claim by induction on k ∈[K]0.

<!-- Page 52 -->

Base case k = 0 For any τ 0 v ∈T 0

G,θ(v), h(0)

v = aG(v) = H(0)(θ)(τ 0 v).

Induction step Fix v ∈V (G) and τ k v ∈T k

G,θ(v) such that τ k v = Tv(τ1,..., τdak) where τi ∈Sk−1 θ (v) for i ∈[dak]. Assume the claim holds for k −1. Then for every τ ∈Sk−1 θ (v) with root labeled u ∈NG(v) it holds h(k−1)

u = H(k−1)(θ)(τ). Thus for every i ∈[dak]

min τ∈Sk−1 θ (v)

fAGG,k θ

H(k−1)(θ)(τi) wG(v, root(τi))

!

i = min u∈N(v)

fAGG,k θ h(k−1)

u wG(v, u))

!

i and hence

H(k)(θ)(τ k v) = fUPD,k θ fAGG,k θ

H(k−1)(θ)(τi) wG(v,root(τi))

i∈[dak]

!

= fUPD,k θ min τ∈Sk−1 θ (v)

fAGG,k θ

H(k−1)(θ)(τ) wG(v,root(τ))

!

= fUPD,k θ min u∈N(v) fAGG,k θ h(k−1)

u wG(v,u))

!

= h(k)

v, where the minimum is taken element-wise.

The next lemma shows that even though the MPNN minimizes features somewhat “greedily” layer by layer, the chosen computation tree of the MPNN τ J v ∈T J

G,θ(v) minimizes the feature “globally” up to negative weights.

Lemma 48. Let G ∈GBF, v ∈V (G) and θ ∈ΘBF. Then for any k ∈[K]0, τ k v ∈T k

G,θ(v) and tk v ∈T k

G(v) it holds

H(k)(θ)(τ k v) ≤H(k)(θ+)(tk v)

element-wise.

Proof. We prove the statement by induction on k ∈[K]0.

Base case (j = 0) Let v ∈V (G), τ 0 v ∈T 0

G,θ(v) and t0 v ∈T 0

G(v), then

H(0)(θ)(τ 0 v) = aG(v) = H(0)(θ+, G)(t0 v).

Inductive step Assume the hypothesis holds for k −1. Let u ∈V (G), τ ∈T k−1

G,θ (u) and t ∈T k−1

G (u). Applying the monotonicity result Lemma 35 and the induction hypothesis gives fAGG,k θ

H(k−1)(θ)(τ) wG(v, root(τ))

!

≤fAGG,k θ+

H(k−1)(θ+, G)(t)

wG(v, root(t))).

!

<!-- Page 53 -->

Now fix v ∈V (G) and define Sk−1(v):= ∪u∈N(v)T k−1

G (u). Then the above implies min τ∈Sk−1 θ (v)

fAGG,k θ

H(k−1)(θ)(τ) wG(v, root(τ))

!

= min u∈N(v) min τ∈T k−1

G,θ (u)

fAGG,k θ

H(k−1)(θ)(τ) wG(v, root(τ))

!

≤min u∈N(v) min t∈T k−1

G (u)

fAGG,k θ+

H(k−1)(θ+, G)(t)

wG(v, root(t))).

!

= min t∈Sk−1(v) fAGG,k θ+

H(k−1)(θ+, G)(t)

wG(v, root(t)))

!

.

Further fix τ k v ∈T k

G,θ(v) and tk v ∈T k

G(v). W.l.o.g. assume that tk v = Tv(t1,..., tdak) and τ k v = Tv(τ1,..., τdak) where ti ∈Sk−1(v) and τi ∈Sk−1 θ (v) for all i ∈[dak]. Applying the monotonicity result 35 on fUPD,k θ together with the above gives

H(k)(θ)(τ k v) = fUPD,k θ fAGG,k θ

H(k−1)(θ)(τi) wG(v,root(τi))

i∈[dak]

!

= fUPD,k θ min τ∈Sk−1 θ (v)

fAGG,k θ

H(k−1)(θ)(τ) wG(v,root(τ))

!

≤fUPD,k θ+ min t∈Sk−1(v) fAGG,k θ+

H(k−1)(θ+,G)(t)

wG(v,root(t))

!

≤fUPD,k θ+ fAGG,k θ+

H(k−1)(θ+,G)(ti)

wG(v,root(ti))

i∈[dak]

!

= H(k)(θ+)(tk v)

which concludes the induction step.

D.5. Application to walk-lifted FNNs

In this section, we introduce a third and final parametrized FNN, the walk-lifted FNN, to easily access all relevant parameters. We will see that the walk-lifted FNN inherits all of the properties of the simple FNN as shown in Section D.3. Moreover, we show that when the aggregation indeed follows a single path, the MPNN can be expressed by the walk-lifted FNN.

Definition 49 (Set of walks). Let G ∈GBF denote a graph and vK ∈V (G). We define

PK

G (vK):= {(v0,..., vK) ∈V (G)K+1: (vk−1, vk) ∈E(G) for all k ∈[K]}

as the set of walks of length K ∈N in G and ending in vK. Let p:= (v0,..., vK) ∈PK

G (vK). We define the weight vector of p as the sequence of weights zp:= (aG(v0), wG(v0, v1),..., wG(vK−1, vK)) ∈RK+1

≥0, recalling that by definition BF-graphs have non-negative real-valued vertex and edge features aG, wG ≥0. Further, we define the tree tk(p) of p of length k ∈[K]0 recursively as follows. For k = 0, let t0(p) ∈T 0

G(v0) denote the tree with a single vertex with vertex label aG(v0). For k > 0, we define tk(p):= Tvk(tk−1(p),..., tk−1(p)) ∈T k

G(vk)

by attaching dak copies of the tree tk−1(p) underneath a root vertex with label vk (where dak denotes the output dimension of the k-th aggregation layer).

<!-- Page 54 -->

Remark 50 (BF-distance). Let G ∈GBF and v ∈V (G). Then the K-step BF-distance (see

Definition 12) is given by x(K)

v = min{∥zp∥1: p ∈PK

G (v)}.

Remark 51 (Path vector of path graphs). Let w ∈RK+1 and recall that the path graph P(w) was defined by V (P(w)):= {v0, v1,..., vK} with vertex-labels given by aG(v0) = w0 and aG(vi) = β for all i ∈[K] and E(P(w)):= {(vi−1, vi) | i ∈[K]}, where the edge-weight function wP(w): E(P(w)) →R+ is defined as (vi−1, vi) 7→wi, for i ∈[K]0. If we let p = (v0,..., vK) ∈PK

G (vK). Then the above implies that zp = (aG(v0), wG(v0, v1),..., wG(vK−1, vK)) = w.

Hence for any training sample vK ∈V (Pβ(w)), where w ∈Sx,K it holds for the path p as above that zp = w which we will make use of later on.

Remark 52 (1D aggregation). If dak = 1 for all k ∈[K]. then any tree in T K

G (v) is in fact a walk, and we can identify

T K

G (v) ≡PK

G (v).

In this case we write zt for t ∈T K

G (v), meaning zp where p ∈PK

G (v) is such that tK(p) = t.

Next, we define the walk-lifted FNN, which is a simple FNN as in Section D.3, but with a very specifically chosen bias vector. Intuitively, we choose the bias vector such that each edge weight along a given walk is added in the corresponding edge-insertion layer. In general, the walk-lifted FNN does not capture the same expressivity as a FNN along a tree, and thus is not powerful enough to express any possible feature of the MPNN. In case any minimum aggregation tree is essentially a walk, we will see that the walk-lifted FNN is in fact equal to the feature of the MPNN.

Definition 53 (Bias of weight vector and walk-lifted FNN). Let C ∈ΘC and z = (z0,..., zK) ∈ RK+1

≥0 we define the bias of a weight vector as

B(z, C):= (b1(z, C),..., bJ(z, C))

where bj(z, C):=

(

Ckzk j = jk, k ∈[K] 0 else ∈Rdj, j ∈[J].

Further let W ∈ΘW and B ∈Θb. We define the walk-lifted FNN as

Hwl(W, C, B)(z):= FNN(J)(W, B + B(z, C))(z0), z ∈RK+1

≥0.

The next lemma establishes the connection between the FNN of a computation tree and the walk-lifted FNN in case the tree is essentially a walk.

Lemma 54. Let G ∈GBF and (W, C, B) = θ ∈ΘBF. Then for any v ∈V (G) and p ∈PK

G (v) it holds

Hwl(θ)(zp) = H(k)(θ)(tK(p)).

<!-- Page 55 -->

Proof. We extend the above definition to k ∈[K]0 as follows, using the equivalent global indexing

H(k)

wl (W, C, B)(z):= FNN(J)

(UPD,k,m)(W, B + B(z, C))(z0), z ∈RK+1

≥0.

We now prove

H(k)

wl (θ)(zp) = H(k)(θ)(tk(p))

by induction on k ∈[K]0. Once proven, this concludes the lemma.

Base case (j = 0) It follows from the above definitions and the fact that t0(p) ∈T 0

G(v0)

H(0)

wl (θ)(zp) = FNN(J)

0 (W, B + B(z, C))(zt 0) = zt 0 = aG(v0) = H(0)(θ)(t0(p)).

Induction step Assuming the claim holds for k −1, we find

H(k)(θ)(tk(p)) = fUPD,k θ fAGG,k θ

H(k−1)(θ)(tk−1(p))

wG(vk,root(tk−1(p)))

!

= fUPD,k θ fAGG,k θ

H(k−1)

wl (θ)(zp) zp k

!

= σ(W (UPD,k,m)... σ(W (AGG,k,1)H(k−1)

wl (θ)(zp) + Ckzp k + b(AGG,k,1)) · · · + b(UPD,k,m))

= H(k)

wl (θ)(zp)

which proves the induction step.

The following lemmas are all immediate consequences of the above and the properties derived in the last two sections. Combined, they will serve as the basis for all feature estimations in the two following sections.

Lemma 55 (Linearity). Let θ = (W, C, B) ∈ΘBF and assume that all parameters of θ are (element-wise) non-negative. Then for all z ∈RK+1

≥0,

Hwl(W, C, B)(z) =

J X l=1

J Y s=l+1

W s b l +

J Y s=1

W s z0 +

X k∈[K]

J Y s=jk+1

W s

Ckzk.

Moreover, the walk-lifted FNN is linear in z, i.e.,

Hwl(W, C, B)(z) =

K X k=0 zk Hwl(W, C, 0)(eK+1 k) + Hwl(W, C, B)(0)

where {eK+1 l }K l=0 denotes the canonical unit-length basis of RK+1.

Proof. Combining Lemma 34 and Definition 53 of B(z, C).

Lemma 56. Let z1, z2 ∈RK+1

≥0, and θ1 = (W1, C1, B1), θ2 = (W2, C2, B2) ∈ΘBF. Assume that z1 ≤z2, θ1 ≤θ2 and W2, C2 ≥0, element-wise. Then

Hwl(θ1)(z1) ≤Hwl(θ2)(z2), element-wise.

<!-- Page 56 -->

Proof. Note that by assumption B1 + B(z2, C1) ≤B2 + B(z2, C2). Thus the lemma follows by Lemma 35.

Corollary 57. For all z ∈RK+1

≥0 and parameter (W, C, B) ∈ΘBF,

Hwl(W, C, B)(z) −Hwl(W+, C+,0)(z)

≤G(W, B(z, C))(z) + Hwl(|W|, |C|, |B|)(0).

Proof. The statement follows by choosing BC = B(z, C) and B = B in Corollary 42.

Lemma 58. Let θ ∈ΘBF, and G ∈GBF. Then for any v ∈V (G) and p ∈PK

G (v) it holds h(K)(v) ≤Hwl(θ+)(zp), and h(K)(v) = Hwl(θ)(zp).

if tK(p) ∈T K

G,θ(v)

Proof. By Lemma 47, h(K)

v = H(k)(θ)(τ K v) for any τ K v ∈T K

G,θ(v). Thus if tK(p) ∈T K

G,θ(v) it must be h(K)

v = H(k)(θ)(tK(p)) = Hwl(θ)(zp)

by Lemma 54. Similarly, choosing tK v = tK(p) ∈T K

G (v) in Lemma 48 and applying Lemma 54 gives h(K)

v = H(k)(θ)(τ K v) ≤H(k)(θ+)(tK(p)) = Hwl(θ+)(zp).

In the preceding sections, we introduced and analyzed three objects: FNNs, FNNs along computation trees, and walk-lifted FNNs.

We first introduced FNNs as a simple setting in which we could derive fundamental structural properties. These properties were then applied in the subsequent sections to the aggregation and update functions of the MPNN, as well as to walk-lifted FNNs. Next, FNNs along computation trees enabled us to express MPNN features in closed form, allowing us to compare the MPNN output with that obtained when aggregation follows a computation tree other than the min-aggregation tree.

The walk-lifted FNN is the main object we will work with from now on. As shown above, it inherits the relevant properties of simple FNNs while explicitly revealing its dependence on the network parameters and the edge weights along a given path. This explicit structure makes it particularly convenient to analyze. Moreover, as established in the previous lemma, the walk-lifted FNN can be used to express or bound the features of the MPNN.

We will use these results as follows. In the next section, we derive bounds on the network parameters under the assumption that the loss is close to its global minimum. To this end, we apply the previous lemma to obtain a lower bound on the empirical loss by removing the ReLU nonlinearity and replacing the MPNN feature hK v with the walk-lifted FNN Hwl(θ+)(zp). Finally, in the last section, we show that for the path training samples TSx,K, the minaggregation computation tree must follow the path and is therefore essentially a walk. In this case as well, the MPNN feature can be replaced by the walk-lifted FNN, allowing us to work entirely within this framework.

<!-- Page 57 -->

D.6. Small empirical loss and structure of parameters

For the remainder of this section, we will consider the MPNN and its parameters as defined in Section C.

Definition 59. For each k ∈[K]0, we define lk:=

{ j ∈[J]: j > jk }

+ 1k̸=0 = J −jk + 1k̸=0 where jk is the k-th edge-inserting layer (c.f. Section C.1). Further let

L:=

K X k=0 lk.

Remark 60. We will see that lk is the number of weight matrices the k-th edge-weight on a given walk is multiplied by. This will be crucial for lower-bounding the regularization term. Further explicit computation gives L = mK(K + 3).

Definition 61 (Bellman–Ford implementing parameters). We define the Bellman–Ford (BF) parameter configuration ψ ∈ΘBF as follows. For each layer j ∈[J], let the bias vector be given by bj ψ:= 0 dj, and define the weight matrix W j ψ ∈Rdj×dj−1 by

W j ψ:=



    

1 0 · · · 0 0 0 · · · 0............ 0 0 · · · 0



    

, i.e., the matrix whose only nonzero entry is a single “1” in the top-left corner. Further for each k ∈[K], let

Ck ψ:= (1,0,...,0)⊤∈Rdjk×1, the vector with a single nonzero entry in the first coordinate. We call the resulting parameter tuple ψ =

(W j ψ)J j=1, (Ck ψ)K k=1, (bj ψ)J j=1

∈ΘBF the BF parameter configuration.

Lemma 62. For L defined as above, it holds that min θ∈ΘBF L(θ) ≤η L.

Proof. Let ψ denote the BF configuration from Definition 61. First note that the BF parameters exactly implement the Bellman–Ford algorithm and hence Lemp(ψ) = 0. Thus by definition of L, and using bj ψ = 0 dj, we have

L(ψ) = ηL(ψ)reg = η





K X k=0

X j>jk

∥W j ψ∥1 +

X k∈[K]

∥Ck ψ∥1



.

<!-- Page 58 -->

Since each W j ψ, j ∈[J] and each Ck ψ, k ∈[K] contains exactly one nonzero entry,

∥W j ψ∥1 = 1, ∥Ck ψ∥1 = 1.

Hence

L(ψ) = η

K X k=0

J −jk + 1k̸=0

!

= η

K X k=0 lk = ηL.

Since ψ ∈ΘBF, we obtain min θ∈ΘBF L(θ) ≤L(ψ) = ηL.

Lemma 63. Let C ∈R, T denote some index set and t:= |T|. Then the solution to min v∈Rt

X l∈T

|vl| s.t.

Y l∈T vl = C is given by vl = C

1 t, for all l ∈T.

Proof. Because of the symmetry of the absolute value, it suffices to consider v ∈Rt

≥0. We then see from the inequality of arithmetic and geometric means that

1 t

X l∈T

|vl| ≥

Y l∈T vl

1 t = C

1 t.

Thus 1 t

P l∈T |vl| is minimal in case of equality which is exactly the case if vl = C

1 t.

Lemma 64. Let M ∈R≥0. Then

M x x ≤exp

M e

, for all x ∈R>0.

Proof. We want to bound the maximum of the function f: R>0 →R>0, f(x):= (M x)x. To this end, we compute its extreme points as

0 = f′(x) = exp ((ln (M) −ln (x))x)′ = (−1 xx + ln (M) −ln (x)) exp ((ln (M) −ln (x))x)

= (−1 + ln (M) −ln (x))f(x).

Since f(x)̸ = 0, we conclude that the extreme point is given by

−1 + ln (M) = ln (x) =⇒ x = exp (−1 + ln (M)) = M e.

Further it holds f(M e) = exp (M e)

lim x→∞f(x) ≤lim x→∞

1 2 x = 0 ≤exp (M e)

lim x→0 f(x) = lim x→∞f(1 x) = lim x→∞exp (ln (Mx)

x) = 1 ≤exp (M e)

and thus

M x x ≤exp

M e

, for all x ∈R>0.

<!-- Page 59 -->

To prove Theorem 17, we begin by deriving basic bounds on the effect that nonzero biases and negative entries in the weight matrices can have on the output of the MPNN.

Lemma 65. Let θ ∈ΘBF and 0 ≤ε ≤ηL. Assume that L(θ) is within ε of its global minimum. Then the following holds.

1. For any T ⊂[J], Y j∈T

∥W j∥1 ≤exp(L).

2. For any k ∈[K] and T ⊂{jk + 1,..., J}, Y j∈T

∥W j∥1 ∥Ck∥1 ≤exp(L).

Proof. We prove the first statement; the second is analogous.

Let t:= |T| and C:= Q j∈T ∥W j∥1. By Lemma 63, tC1/t ≤

X j∈T

∥W j∥1.

Applying Lemma 62 gives η

X j∈T

∥W j∥1 ≤L(θ) ≤ηL + ε ≤2ηL, and therefore

C1/t ≤2L t ⇒ C ≤

2L t t

.

Finally, by Lemma 64, C ≤

2L t t ≤exp(2L/e) ≤exp(L), which proves the claim.

Corollary 66. Let θ ∈ΘBF and 0 ≤ε ≤ηL. Assume that L(θ) is within ε of its global minimum. Then,

Hwl(|W|, |C|, |B|)(0) ≤exp(L)

J X j=1

∥bj∥1,

G(W, B(z, C))(z0) ≤exp(L)

J X l=1

∥(W l)−∥1 +

K X k=1

∥(Ck)−∥1

∥z∥1, z ∈RK+1

≥0.

Proof. First note that since dJ = 1, it holds that Hwl(|W|, |C|, |B|)(0) and G(W, B(z, C))(z0) belong to R≥0. Using Lemmas 55 and 65, we obtain

Hwl(|W|, |C|, |B|)(0) ≤

J X j=1

J Y l=j+1

∥W l∥1∥bj∥1 ≤ max j∈[J]

J Y l=j+1

∥W l∥1

J X j=1

∥bj∥1 ≤exp(L)

J X j=1

∥bj∥1.

Recall that by Remark 40, it holds for general biases ˜B that

∥G(W, ˜B)(˜b0)∥1

≤

X l∈[J]0 l−1 X l′=0

J Y s=l′+1 s̸=l

∥(W s)+∥1

∥(W l)−∥1∥(˜bl′)+∥1 +

X l′∈[J]0

J Y s=l′+1

∥(W s)+∥1

∥(˜bl′)−∥1

<!-- Page 60 -->

For our purposes we choose ˜B = B(z, C) and ˜b0 = z0. Further we let C0 = 1 for ease of notation. Noting that bl′(z, C) = P k∈[K]0 δl′,jkCkzk for l′ ∈[J] we find

∥G(W, B(z, C))(z0)∥1

≤

X l∈[J]0 l−1 X l′=0

J Y s=l′+1 s̸=l

∥(W s)+∥1

∥(W l)−∥1

X k∈[K]0 δl′,jk∥(Ck)+∥1zk

+

X l′∈[J]0

J Y s=l′+1

∥(W s)+∥1

X k∈[K]0 δl′,jk∥(Ck)−∥1zk

65 ≤

X l∈[J]0 l−1 X l′=0

∥(W l)−∥1

X k∈[K]0 δl′,jkzk +

X l′∈[J]0

X k∈[K]0 δl′,jk∥(Ck)−∥1zk exp (L)

=

X l∈[J]0

∥(W l)−∥1

X k∈[K]0 l−1 X l′=0 δl′,jk zk +

X k∈[K]0

X l′∈[J]0 δl′,jk

∥(Ck)−∥1zk

!

exp (L)

≤

X l∈[J]0

∥(W l)−∥1

X k∈[K]0 zk +

X k∈[K]0

∥(Ck)−∥1zk exp (L)

≤

X l∈[J]0

∥(W l)−∥1∥z∥1 +

X k∈[K]0

∥(Ck)−∥1∥z∥1 exp (L)

≤exp (L)

X l∈[J]0

∥(W l)−∥1 +

X k∈[K]0

∥(Ck)−∥1

∥z∥1 applying lemma Lemma 65 with appropriate choice for T in each considered summand.

To simplify the analysis of the loss function and highlight the main forces acting on the parameters, we introduce a modified loss function.

Definition 67 (Modified loss function). We begin by defining a transformation of the neural network parameters. Given θ = (W, C, B) ∈ΘBF, we define the transformed parameters

˜θ:= (γ0,..., γK, B, w−) ∈RK+3

≥0 as follows. To avoid a case distinction, we introduce C0:= 1 as a fixed parameter. Then we set γk:=

J Y j=jk+1

(W j)+(Ck)+ ∈R≥0, k ∈{0,..., K},

B:= ∥B∥1 ∈R≥0, w−:=

J X l=1

∥(W l)−∥1 +

K X k=1

∥(Ck)−∥1 ∈R≥0.

Next, we define a new loss function ˜L on the transformed parameters. As before, we separate the loss into an empirical term and a regularization term:

˜L(˜θ):= ˜Lemp(˜θ) + η ˜Lreg(˜θ),

<!-- Page 61 -->

where

˜Lemp(˜θ):= 1

N

K X k=0 σ

(1 −γk)x −exp(L)B

,

˜Lreg(˜θ):= B +

K X k=0 lkγ

1 lk k + w−, where x ∈R≥0 is the scale of the weights in the training set TSx,K.

Remark 68. Applying Lemma 55 and the definition of γk, k ∈[K]0 we see that

Hwl(W+, C+,0)(z) =

K X k=0

J Y s=jk+1

(W s)+

(Ck)+zk =

K X k=0 γk zk for any z ∈RK+1. Thus up to biases and negative weights γk is the factor that the k-th edge weight zk is multiplied with, in case the aggregation follows the path p such that zp = z.

The next lemma establishes the key connection between the original and modified loss functions. It shows that the modified loss lower-bounds the contributions of the original parameters, allowing us to analyze ˜L in place of L.

Lemma 69. Let θ = (W, C, B) ∈ΘBF and let ˜θ be its transformed parameter vector. Further, assume TSx,K ⊂X and that L(θ) is within ε ≤ηL of its global minimum. Then

Lemp(θ) ≥˜Lemp(˜θ), and Lreg(θ) ≥˜Lreg(˜θ).

Proof. We first prove Lemp(θ) ≥˜Lemp(˜θ). Fix w ∈Sx,K and consider the corresponding path graph used for training G:= P(w) with vertices vw

0,..., vw K. Let pw = (vw

0,..., vw K) ∈P K

G (vK) be the walk that starts in vw

0 and ends in vw K. Then it holds zpw = w (see Remark 51). Thus, Lemma 58 implies h(K)

vw

K ≤Hwl(θ+)(zpw) = Hwl(W+, C+, B+)(w).

Further since the last vertex vw

K of the path graph P(w) is part of the training set, e.g. {vw

K: w ∈Sx,K} = TSx,K ⊂X and for the corresponding target it holds x(K)

vw

K = ∥w∥1 (c.f. Remark 15) we have

Lemp(θ) = 1

N

X v∈X h(K)

v −x(K)

v

≥1

N

X w∈Sx,K h(K)

vw

K −∥w∥1

.

<!-- Page 62 -->

Combining the above, using Lemma 55, Lemma 56, Corollary 66 and Remark 68, we obtain

N Lemp(θ) ≥

X w∈Sx,K

|∥w∥1 −h(K)

vw

K | ≥

X w∈Sx,K σ

∥w∥1 −Hwl(W+, C+, B+)(w)

≥

X w∈Sx,K σ

∥w∥1 −Hwl(W+, C+,0)(w) −Hwl(|W|, |C|, |B|)(0)

≥

X w∈Sx,K σ

∥w∥1 −Hwl(W+, C+,0)(w) −exp(L)B

=

X w∈Sx,K σ

K X k=0

(1 −γk)wk −exp(L)B

!

≥

K X k=0 σ((1 −γk)x −exp(L)B) = N ˜Lemp(˜θ), where in the last inequality we used that Sx,K = {xeK+1 k: k ∈[K]0}.

Next we prove Lreg(θ) ≥˜Lreg(˜θ). Observe that, γ0 ≤

J Y j>j0

∥(W j)+∥1, γk ≤

J Y j>jk

∥(W j)+∥1 ∥(Ck)+∥1, k ∈[K].

Thus for each k ∈[K]0, by Lemma 63 and the definition of lk (see Definition 59)

lk γ1/lk k ≤

J X j>jk

∥W j∥1 + 1k̸=0∥Ck∥1.

Therefore,

Lreg(θ) =

K X k=0



X j>jk

∥W j∥1 + 1k̸=0∥Ck∥1



+ B

≥

K X k=0



X j>jk

∥(W j)+∥1 + 1k̸=0∥(Ck)+∥1



+ B +

J X j=1

∥(W j)−∥1 +

K X k=1

∥(Ck)−∥1

≥

K X k=0 lkγ1/lk k + B + w−= ˜Lreg(˜θ).

Based on the previous lemma, which allows us to analyze the modified loss ˜L in place of the original loss L, the next result identifies the key structural properties that any parameter set must satisfy when it lies close to the global minimum. There are essentially two main advantages to working with ˜L.

First, the feature contribution is replaced by a simpler upper bound that no longer depends on the ReLU’s intricate behaviour. An immediate consequence is that non-zero biases or negative entries in the weight matrices can only increase the modified loss, rather than interact in more complicated ways as in the original formulation. Secondly, the parameters appearing

<!-- Page 63 -->

in different summands of the modified empirical loss become independent of one another. In particular, increasing γk1 for some k1 does not decrease the term σ

(1 −γk2)x −exp(L)B associated with any k2̸ = k1. These simplifications eliminate several sources of coupling and nonlinearity present in the original loss and thereby make the subsequent analysis considerably more tractable.

Lemma 70 (Parameter characterization near the global minimum). Let θ ∈ΘBF. Assume TSx,K ⊂X and that L(θ) lies within 0 ≤ε ≤ηL of its global minimum. Further assume η ≥2K exp(L) and x ≥2NηJ.

Then the following estimates hold:

Hwl(|W|, |C|, |B|)(0) ≤ε, (16)

γk ≥1 −ε ηJ, k ∈[K]0, (17)

and, for any z ∈RK+1

≥0,

|Hwl(W, C, B)(z) −Hwl(W+, C+,0)(z)| ≤

1

2∥z∥1 + 1 ε. (18)

Moreover,

Lemp(θ) ≤2ε.

Note that both η and x must be chosen sufficiently large. A large value of η ensures that the influence of the biases on the empirical loss is small compared to their contribution to the regularization term, so that any non-zero bias is strongly penalized overall. Likewise, taking x much larger than η guarantees that the empirical loss dominates the regularizer, so that deviations in the feature values have a significantly stronger impact on the total loss than variations in the regularization cost.

Proof. Starting from the definition of ˜L, we compute

˜L(˜θ) −ηL −ηw−= 1

N

K X k=0 σ((1 −γk)x −exp(L)B) + ηB + η

K X k′=0 lk′(γ1/lk′ k′ −1)

≥1

N

X k: γk≤1

(1 −γk)x −exp(L)B

+ ηB + η

X k′: γk′≤1 lk′(γ1/lk′ k′ −1)

≥1

N

X k: γk≤1

(1 −γk)x + ηlk(γk −1)

+ η −K exp(L)

B

≥ x

N −ηJ

X k: γk≤1

(1 −γk) + 1

2ηB

≥ηJ

X k: γk≤1

(1 −γk) + 1

2ηB, where we used that γ1/lk′ k′ ≥γk′ if γk′ ≤1 and lk ≤J. Using Lemma 69 and Lemma 62 we obtain ηJ

X k: γk≤1

(1 −γk) + 1

2ηB + ηw−≤˜L(˜θ) −ηL ≤L(θ) −ηL ≤ε. (19)

With (19) at hand, we can now derive the estimates as claimed.

<!-- Page 64 -->

Proof of (16) and (18) From (19),

1 2ηB ≤ε, ηw−≤ε.

Using Corollary 66 and η ≥2 exp(L) by assumption on η, this yields

Hwl(|W|, |C|, |B|)(0) ≤exp(L)B ≤exp(L)2ε η ≤exp(L) 2ε 2 exp(L) = ε,

G(W, B(z, C))(z0) ≤exp(L)w−∥z∥1 ≤exp(L)ε η∥z∥1 ≤1

2ε∥z∥1.

Thus (16) holds, and by Corollary 57,

|Hwl(W+, C+,0)(z) −Hwl(W, C, B)(z)|

≤G(W, B(z, C))(z0) + Hwl(|W|, |C|, |B|)(0) ≤

1

2∥z∥1 + 1 ε, proving (18).

Lower bound on γk From (19), for any k ∈[K]0 ηJ(1 −γk) ≤ε ⇒ γk ≥1 −ε ηJ, which gives (17).

Estimate for the empirical loss From (19),

X k: γk≤1

(1 −γk) ≤ ε ηJ and hence,

˜Lreg(˜θ) ≥

K X k=0 lk γ1/lk k = L −

K X k=0 lk (1 −γ1/lk k) ≥L −J

K X k: γk≤1

(1 −γk) ≥L −ε η.

Therefore, using Lemma 69 and Lemma 62

Lemp(θ) = L(θ) −ηLreg(θ) ≤L(θ) −η ˜Lreg(˜θ) ≤ε + ηL − ηL −ε

≤2ε which completes the proof.

D.7. Upper and Lower bound

In this section, we assume that the dimension of aggregation is 1, i.e. dak = 1, for all k ∈[K]. Then any computation tree is in fact a path, and thus, zt is well-defined for any t ∈T J

G (v), where G ∈GBF and v ∈V (G) (c.f. Remark 52).

Corollary 71 (Lower bound). Let θ ∈ΘBF, η ≥2K exp(L) and x ≥2NηJ. Assume TSx,K ⊂X and that L(θ) lies within 0 ≤ε ≤ηL of its global minimum. Then for any G ∈GBF, v ∈V (G), and t ∈T J θ (v)

h(K)

v ≥(1 −ε) ∥zt∥1 −ε.

In particular, h(K)

v ≥(1 −ε) x(K)

v −ε where x(K)

v denotes the Bellman–Ford distance.

<!-- Page 65 -->

Proof. Let G ∈GBF. Fix v ∈V (G) and τ ∈T K

G,θ(v). Applying Lemma 58, and (18) from Lemma 70 and Remark 68 gives h(K)

v = Hwl(W, C, B)(zτ) ≥Hwl(W+, C+,0)(zτ) −

1 2∥zτ∥1 + 1 ε

=

K X k=0 γk zτ k −

1 2∥zτ∥1 + 1 ε.

Using γk ≥1 − ε ηJ (by (17) from Lemma 70), η ≥2 and J ≥1, we obtain

K X k=0 γk zτ k ≥

1 −ε ηJ

∥zτ∥1 ≥

1 −ε 2

∥zτ∥1.

Combining this with the previous estimate gives h(K)

v ≥(1 −ε) ∥zτ∥−ε.

Finally, note that by definition of the BF-distance x(K)

v it holds ∥zt∥1 ≥x(K)

v for any t ∈ T K

G (v) ≡PK

G (v) (see Remark 50). Therefore, h(K)

v ≥(1 −ε) x(K)

v −ε, which completes the proof.

The next lemma helps to derive tighter upper bounds on the features.

Lemma 72. Let θ ∈ΘBF, η ≥2K exp(L) and x ≥2NηJ. Assume TSx,K ⊂X and that L(θ) lies within 0 < ε < 1/2 (≤ηL) of its global minimum. Then for any z ∈RK+1

≥0,

Hwl(W+, C+,0)(z) −∥z∥1

≤ε ∥z∥1.

Proof. Let w ∈Sx,K and τ ∈T J

G,θ(vw

K) where vw

K denotes the last vertex of the graph G:= Pβ(w) from the training set. Further let pBF:= (vw

0,..., vw K) ∈PK

G (vw

K) and pAGG ∈PK

G (vw

K) denote the path of τ, i.e. tK(pAGG) = τ.

Assume for contradiction that the aggregation does not follow pBF, i.e. pBF̸ = pAGG. Then the first vertex on pAGG is not v0 and hence zpAGG

0 = aG(v0) = β (c.f. Remark 51). Since ε ≤1

2, and by Lemma 70 and Corollary 71, we have

N ≥2Nε ≥NLemp(θ) ≥|h(K)

vw

K −∥w∥1| ≥h(K)

vw

K −∥w∥1

≥(1 −ε)∥zτ∥1 −ε −∥w∥1 ≥(1 −ε)β −ε −x ≥1

2(β −1) −x ≥N + 1 2 where in the last inequality we use β ≥2(N + x + 1), which is a contradiction. Hence, it must be pBF = pAGG and thus w = zpBF = zτ (c.f. Remark 51). Therefore by Lemma 58 h(K)

vw = Hwl(W, C, B)(zτ) = Hwl(W, C, B)(w).

<!-- Page 66 -->

Applying Lemma 70, we obtain

2Nε ≥NLemp(θ) ≥|h(K) vw

K −∥w∥1| = |Hwl(W, C, B)(w) −∥w∥1|

≥|Hwl(W+, C+,0)(w) −∥w∥1| −|Hwl(W, C, B)(w) −Hwl(W+, C+,0)(w)|

≥|Hwl(W+, C+,0)(w) −∥w∥1| −

1 2∥w∥1 + 1 ε.

For w = xeK+1 k ∈Sx,K, this gives

|Hwl(W+, C+,0)(xeK+1 k) −x| = |Hwl(W+, C+,0)(w) −∥w∥1| ≤(2N + 1

2x + 1)ε ≤εx, where the last inequality follows from our assumptions on x and η:

2N + 1 1 2x ≤22N + 1

2Nη ≤ 2N + 1 2NK exp(L) ≤2N + 1 4N ≤1.

Finally, by the linearity of the walk-lifted FNN for positive parameter we get for any z ∈RK+1

≥0:

|Hwl(W+, C+,0)(z) −∥z∥1| ≤

X k∈[K]0 zk x |Hwl(W+, C+,0)(xeK+1 k) −x| ≤

X k∈[K]0 zk x εx ≤ε∥z∥1.

Theorem 73 (Upper bound). Let θ ∈ΘBF, η ≥2K exp(L) and x ≥2NηJ. Assume TSx,K ⊂X and that L(θ) lies within 0 < ε < 1

2 of its global minimum. Then, for any G ∈GBF and any v ∈V (G), h(K)

v ≤(1 + ε)x(K)

v + ε.

Proof. Fix G ∈GBF and let p ∈PK

G (v). Using Lemma 58, Lemma 55, Lemma 72 and (16) from Lemma 70 h(K)

v ≤Hwl(W+, C+, B+)(zp) ≤Hwl(W+, C+,0)(zp) + Hwl(W+, C+, B+)(0) ≤(1 + ε)∥zp∥+ ε and thus by definition of the BF-distance (see Remark 50)

h(K)

v ≤ min p∈PK

G (v)(1 + ε)∥zp∥+ ε = (1 + ε)xK v + ε.

E. What MPNN cannot learn

This appendix provides additional details for Section 4. In particular, Section E.1 contains further details related to Section 4.1, including a formal statement and proof of Proposition 6, while Section E.2 contains the proof of Lemma 7 from Section 4.2.

<!-- Page 67 -->

E.1. Expressivity limitations

We begin by formally stating and proving the negative result of Proposition 6, namely that standard MPNN architectures cannot approximate the SSSP and MST invariants.

Proposition 74 (Proposition 6 (negative result) in the main text). The following holds.

1. For n ≥6, there exists an edge-weighted graph G of order n and vertices s, t1, t2 ∈V (G) such that, for the class of vertex-level MPNNPL

(SL,d,n)({G}), for any number of layers L ≥0, d > 0, set of parameters PL, and sequence of parameterized functions SL, it holds that for all m ∈MPNNPL

(SL,d,n)({G}),

|SSSP(G, (s, t1)) −SSSP(G, (s, t2))| ≥1 but m(t1) = m(t2).

2. For n ≥6, there exist edge-weighted graphs G, H of order n such that, for the class of graphlevel MPNNQL

(TL,d)({G, H}), for any number of layers L ≥0, d > 0, set of parameters QL, and sequence of parameterized functions TL, it holds that for all m ∈MPNNQL

(TL,d)({G, H}),

|MST(G) −MST(H)| ≥1 but m(G) = m(H).

3. For n ≥14, there exist edge-weighted graphs G, H of order n such that, for the class of graph-level 1-iWL-simulating MPNNQL

(TL,d)({G, H}), for any number of layers L ≥0, d > 0, set of parameters QL, and sequence of parameterized functions TL, it holds that for all m ∈MPNNQL

(TL,d)({G, H}),

|MST(G) −MST(H)| ≥1 but m(G) = m(H).

Proof. For (1) it suffices to consider the edge-weighted graph (G, wG) with V (G):= [6] and edge set E(G):= {(1,2), (1,3), (2,3), (3,4), (4,5), (4,6), (5,6)}, with edge weights wG(1,2):= 3, wG(1,3):= 1, wG(2,3):= 1, wG(3,4):= 5, wG(4,5):= 1, wG(4,6):= 1, and wG(5,6):= 3. Hence, the graph G consists of two triangles connected by an edge with a large weight. Let s = 1, t1 = 2, and t2 = 5. Then, the shortest path from s to t1 has cost 2 via vertices 1,3,2, whereas the shortest path from s to t2 has cost 7 via vertices 1,3,4,5. Hence |SSSP(G, (s, t1)) −SSSP(G, (s, t2))| = 5 ≥1. For (2) we consider an additional edge-weighted graph (H, wH), also of order six with V (H):= [6]. The graphs G and H have different costs for minimal spanning trees, yet they are indistinguishable by 1-WL. The edge set of H is E(H):= {(1,2), (2,4), (4,6), (6,5), (5,3), (3,1), (3,4)}, with edge weights wH(1,2):= 3, wH(2,4):= 1, wH(4,6):= 1, wH(6,5):= 3, wH(5,3):= 1, wH(3,1):= 1, and wH(3,4):= 5. Hence, the graph H consists of a 6-cycle with a chord of large weight. Observe that MST(G) = 9. However, in H, because we do not have to include the heavy chord in an MST, we get MST(H) = 7.

We now observe that 1-WL, taking edge weights into account, cannot distinguish the graphs G and H, and it also cannot distinguish t1 and t2 in G. Indeed, in view of the characterization of 1- WL-distinguishability in terms of unrollings (see Lemma 81), one can verify that unr(G, t1, L) = unr(G, t2, L) for all L. Similarly, there is a bijection π: V (G) →V (H) such that for all v ∈V (G), unr(G, v, L) = unr(H, π(v), L) for all L. Hence, by Morris et al. [75, Theorem 1], no vertex-level MPNN can separate t1 from t2 on G, and no graph-level MPNN can separate G from H, implying (1) and (2).

<!-- Page 68 -->

For (3), we exhibit two connected graphs G and H such that 1-iWL does not distinguish them (regarding a suitable choice of roots), yet MST(G)̸ = MST(H). In both graphs, the vertex set is V (G) = V (H):= [14], where 7 and 8 are two bridge endpoints and both graphs contain the edge (7,8). The edge sets are

E(G):= {(1,2), (1,3), (2,3)} ∪{(4,5), (4,6), (5,6)} ∪{(3,4)}

∪{(9,10), (9,11), (10,11)} ∪{(12,13), (12,14), (13,14)} ∪{(11,12)}

∪{(7, i) | i ∈[6]} ∪{(8, j) | j ∈{9,10,11,12,13,14}} ∪{(7,8)}, and

E(H):= {(1,2), (2,4), (4,6), (6,5), (5,3), (3,1), (3,4)}

∪{(9,10), (10,12), (12,14), (14,13), (13,11), (11,9), (11,12)}

∪{(7, i) | i ∈[6]} ∪{(8, j) | j ∈{9,10,11,12,13,14}} ∪{(7,8)}.

The weights are defined by wG(3,4) = wG(11,12):= 5, wG(7, i):= 10 for i ∈[6], wG(8, j):= 10 for j ∈{9,...,14}, and wG(e):= 1 for all other e ∈E(G) (in particular wG(7,8) = 1); analogously, wH(3,4) = wH(11,12):= 5, wH(7, i):= 10 for i ∈[6], wH(8, j):= 10 for j ∈ {9,...,14}, and wH(e):= 1 for all other e ∈E(H) (again wH(7,8) = 1). It is readily verified that MST(G) = 39 and MST(H) = 31.

Let v and w be vertex 1 in G and H, respectively. Then G and H are 1-iWL-indistinguishable regarding v and w. Indeed, this follows from the corresponding characterization in terms of unrollings (see Lemma 81) and the existence of a bijection π: V (G) →V (H) such that for all v′ ∈V (G), unr(G, v′, L, v) = unr(H, π(v′), L, w). Hence, by the same argument as Morris et al. [75, Theorem 1], no 1-iWL-simulating graph-level MPNN can separate G from H, which implies (3).

Now, the following result shows that 1-iWL- and (1,1)-WL-simulating MPNNs can arbitrarily well approximate the costs of SSSP and MST, respectively. We remark that these approximation results require fixing the order of graphs.

Proposition 75. Let n > 0, let C ⊆R be compact, and let Gn,C be a set of edge-weighted n-order graphs with edge weights from C. Then the following holds.

1. For n ≥1 and ε > 0, there exists a class of 1-iWL-simulating vertex-level MPNNs Fε and an f ∈Fε such that sup G∈Gn,C, s,t∈V (G)

f(G, (s, t)) −SSSP(G, (s, t))

< ε.

2. For n ≥1 and ε > 0, there exists a class of (1,1)-WL-simulating graph-level MPNNs Fε and an f ∈Fε such that sup G∈Gn,C f(G) −MST(G)

< ε.

Proof. For simplicity, we assume that all graphs are connected. We rely on Proposition 1 and show below, in Lemma 76, that ρ2(1-iWL) ⊆ρ2(SSSP), and in Lemma 77 that ρ((1,1)-WL) ⊆ ρ(MST). The approximation statements then follow from Proposition 1 and form that we consider simulating MPNNs.

<!-- Page 69 -->

The following results state that 1-iWL determines shortest-path distances and that (1,1)-WL determines the cost of an MST.

Lemma 76 (Proposition 6 (positve result regarding SSSP) in the main text). Let (G, wG) and (H, wH) be two connected edge-weighted graphs, and let s, v ∈V (G) and t, w ∈V (H). If

C1,s

∞(v) = C1,t

∞(w), then SSSP(G, (s, v)) = SSSP(H, (t, w)).

Proof. We argue by contradiction. Assume that SSSP(G, (s, v))̸ = SSSP(H, (t, w)). Then, for L large enough, the rooted unrollings satisfy unr(G, v, L, s)̸ = unr(H, w, L, t). By the characterization of 1-iWL in terms of rooted unrollings (see Lemma 81), this implies C1,s

∞(v)̸ = C1,t

∞(w), contradicting the assumption. We refer to Section F.2 for details.

Lemma 77 (Proposition 6 (positve result regarding MST) in the main text). Let (G, wG) and (H, wH) be two connected edge-weighted graphs that are (1,1)-WL-indistinguishable. Then

MST(G) = MST(H).

Proof. We reduce the cost computation for a minimal spanning tree to counting the number of connected components in weight-pruned subgraphs. Since (1,1)-WL determines the number of connected components [92], the claim follows. We refer to Section F.2 for details.

E.2. Proof of Lemma 7

This appendix contains the formal statement and proof of Lemma 7.

Lemma 78 (Lemma 7 in the main text). Let K be the family of all complete graphs, i.e.,

K:= {G | V (G) = [n], E(G) = {{i, j} | i, j ∈[n], i̸ = j}, for some n ∈N}.

Let d be any (pseudo-)metric on V1(K) such that the degree invariant deg: V1(K) →N is L-Lipschitz for some L < ∞. Then, for every ε ∈(0, 1

L), N(V1(K), d, ε) = ∞. Consequently, no hypothesis class containing the degree invariant can satisfy Definition 2 on any graph space containing V1(K).

Proof. Fix ε ∈(0,1/L) and set q:= ⌈Lε⌉+ 1. For each k ∈N, let K1+kq ∈K denote the complete graph on 1 + kq vertices, choose an arbitrary uk ∈V (K1+kq), and define xk:= (K1+kq, uk) ∈V1(K). Then deg(xk) = kq, and for k̸ = ℓ, d(xk, xℓ) ≥| deg(xk) −deg(xℓ)|

L ≥q

L > ε.

Thus {xk}k∈N is an infinite ε-separated subset of (V1(K), d) (i.e., d(xk, xℓ) > ε for all k̸ = ℓ), implying N(V1(K), d, ε) = ∞.

F. Expressivity limitations

This appendix provides additional technical background for Section E.1, including the formal proofs of Lemma 76 and Lemma 77.

<!-- Page 70 -->

F.1. Separation and approximation

We briefly recall known connections between discrete separation power and continuous approximation power, following Azizian and Lelarge [3] and Geerts and Reutter [32].

Let C ⊆R be compact. For n ∈N, let Gn,C denote the set of edge-weighted n-order graphs with edge weights in C. One can represent elements in Gn,C by their weighted adjacency matrices in Cn×n. Then, equipped with the product topology, Gn,C is compact.

Let k ∈N and let F be a class of continuous functions on Vk(Gn,C) of the form f: Vk(Gn,C) → Rℓf for some ℓf ∈N that may depend on f. We write F for the closure of F using the sup norm. That is, a function h: Vk(Gn,C) →Rℓh is in F if there exists a sequence (fi)i≥1 ⊆F with fi: Vk(Gn,C) →Rℓh such that

∥fi −h∥∞:= sup (G,v)∈Vk(Gn,C)

∥fi(G, v) −h(G, v)∥2 →0.

We assume F satisfies the following natural assumptions:

## 1 Concatenation-closed: if f1:

Vk(Gn,C) →Rd and f2: Vk(Gn,C) →Rp are in F, then G 7→(f1(G), f2(G)) ∈Rd+p is in F.

2. Function/FNN-closed for ℓ: if f: Vk(Gn,C) →Rp is in F and g: Rp →Rℓis continuous or is an FNN, then g ◦f ∈F.

For such F we denote by Fℓthe subset of functions in F of the form Vk(Gn,C) →Rℓ, i.e., with output dimension fixed to ℓ.

Based on a generalized Stone–Weierstrass theorem [105], Geerts and Reutter [32, Theorem 6.1] and Azizian and Lelarge [3, Lemma 32] combined prove the following characterization.

Theorem 79. Let C ⊆R be compact, and let n, m, k, ℓ∈N. Let F be a class of functions on Vk(Gn,C) that is concatenation-closed and function/FNN-closed for ℓ. Then

Fℓ= f: k(Gn,C) →Rℓ ρVk(Gn,c)(F) ⊆ρVk(Gn,C)(f)

.

Let us fix L ∈N and consider

F:=

[ p

MPNNQL

(TL,p)(Gn,C), i.e., the class of all L-layer graph-level MPNNs as defined in Section 2.2, with TL implemented by FNNs. Fix ℓ∈N. As the class F of MPNNs is easily verified to be concatenation-closed and FNN-closed for ℓ, Theorem 79 applies.

Corollary 80. Let g: Gn,C →Rℓbe a continuous graph invariant such that g cannot separate more graphs than the class F of L-layer graph-level MPNNs. Then, for any ϵ > 0, there is an

L-layer graph-level MPNN f in MPNNQL

(TL,p)(Gn,ℓ) satisfying sup G∈Gn,C

∥g(G) −f(G)∥2 ≤ϵ.

One can obtain similar statements for invariants g: V1(Gn,C) →Rℓand the class F of vertexlevel L-layer MPNNs, g: V2(Gn,c) →Rℓand the class F of vertex-level L-layer MPNNs where each (G, (r, v)) ∈V2(Gn,C) as a vertex v in G in which r is individualized.

<!-- Page 71 -->

In particular, given any alg ∈{1-WL,1-iWL,(1,1)-WL} and class of MPNNs that are algsimulating, the Corollary implies that this class of MPNNs can arbitrarily approximate any invariant g that is upper bounded in expressive power by alg, resulting in Proposition 1 in the main paper.

In the following, we will use the above result to shed some light on the abilities of MPNNs to approximate or not be able to approximate invariants corresponding to well-known graph problems.

F.2. Additional details for Section 4.1

We first recall the unrolling-tree characterization of 1-WL for vertex-labeled, edge-weighted graphs [76] and then adapt it to characterize 1-iWL as well.

Given a connected vertex-labeled and edge-weighted graph (G, ℓG, wG), we define the unrolling tree of depth L ∈N0 rooted at a vertex u ∈V (G), denoted unr(G, u, L), inductively as follows.

1. For L = 0, unr(G, u,0) is the single-vertex tree whose root is labeled ℓG(u).

2. For L > 0, unr(G, u, L) has a root labeled ℓG(u) and, for each neighbor v ∈N(u), it has a child subtree isomorphic to unr(G, v, L −1), connected to the root by an edge of weight wG(u, v).

We now extend this notion to incorporate the distinguished root vertex used in 1-iWL. Given a connected vertex-labeled and edge-weighted graph (G, ℓG, wG) and a fixed vertex r ∈V (G), we mark r by setting ℓG(r):= [∗]. The unrolling tree regarding r of depth L ∈N0 rooted at u ∈V (G), denoted unr(G, u, L, r), is defined inductively as follows.

1. For L = 0, unr(G, u,0, r) is the single-vertex tree whose root is labeled ℓG(u).

2. For L > 0, unr(G, u, L, r) has a root labeled ℓG(u) and, for each neighbor v ∈N(u), it has a child subtree isomorphic to unr(G, v, L −1, r), connected to the root by an edge of weight wG(u, v).

The following lemma is immediate.

Lemma 81 (Follows from Morris et al. [76, Lemma 12]). The following characterizations hold.

1. For L ∈N0, given a connected vertex-labeled, edge-weighted graph (G, ℓG, wG) and vertices u, v ∈V (G), the following are equivalent.

• The vertices u and v have the same color after L iterations of 1-WL.

• The unrolling trees unr(G, u, L) and unr(G, v, L) are isomorphic (as rooted, labeled, edge-weighted trees).

2. For L ∈N0, given a connected vertex-labeled, edge-weighted graph (G, ℓG, wG), a fixed vertex r ∈V (G) with ℓG(r) = [∗], and vertices u, v ∈V (G), the following are equivalent.

• The vertices u and v have the same color after L iterations of 1-iWL, for individualized r.

• The unrolling trees unr(G, u, L, r) and unr(G, v, L, r) are isomorphic (as rooted, labeled, edge-weighted trees).

<!-- Page 72 -->

F.2.1. Proof of Lemma 76

Let (G, wG) and (H, wH) be two connected edge-weighted graphs, and let s, v ∈V (G) and t, w ∈ V (H). We need to show that if C1.5,s

∞ (v) = C1.5,t

∞ (w), then SSSP(G, (s, v)) = SSSP(H, (t, w)).

Assume for contradiction that SSSP(G, (s, v))̸ = SSSP(H, (t, w)). Fix L large enough so that the (unique) marked vertices s in unr(G, v, L, s) and t in unr(H, w, L, t) appear within depth L along all shortest root-to-marked paths. In unr(G, v, L, s), the cost of the shortest path from the root v to the unique vertex labeled [∗] equals SSSP(G, (s, v)), and analogously, in unr(H, w, L, t) the cost of the shortest path from the root w to the unique vertex labeled [∗] equals SSSP(H, (t, w)). If SSSP(G, (s, v))̸ = SSSP(H, (t, w)), then the two rooted, vertex-labeled, edge-weighted trees unr(G, v, L, s) and unr(H, w, L, t) cannot be isomorphic, contradicting the unrolling-tree characterization of 1-iWL (see Lemma 81) together with the assumption C1,s

∞(v) = C1,t

∞(w).

F.2.2. Proof of Lemma 77

Let (G, wG) and (H, wH) be two connected edge-weighted graphs that are (1,1)-WL-indistinguishable. We need to show that MST(G) = MST(H).

We prove this by showing that the cost of a minimal spanning tree is determined by the number of connected components in threshold subgraphs that only hold edges with weights below a certain threshold. Lemma 76 then follows from the fact that (1,1)-WL determines the number of connected components. We detail the argument at the end of this subsection.

For a graph X we write cc(X) for its set of connected components and #cc(X) for the number of connected components. Let (G, wG) be an (undirected) edge-weighted graph and let W(G):= {wG(e) | e ∈E(G)} be its set of edge weights. Let the distinct weights be w1 < w2 < · · · < wm, and set wm+1:= +∞. For any w ∈R>0 we define the (unweighted) threshold subgraph

G<w:=

V (G), {e ∈E(G) | wG(e) < w}

.

For each j ∈[m + 1] define κj:= #cc(G<wj). Note that κm+1 = #cc(G).

Let MSF(G) be the minimum spanning forest cost, i.e., the total weight of a minimum spanning forest of G. If G is connected, then we denote MSF(G) by MST(G).

Lemma 82. For any edge-weighted graph (G, wG) with distinct weights w1 < · · · < wm,

MSF(G) = m X j=1

(κj −κj+1) wj.

Proof. For j ∈[m], set Gj:= G<wj+1. Then E(Gj) = {e ∈E(G) | wG(e) ≤wj} and #cc(Gj) = κj+1.

We prove by induction on j that

MSF(Gj) = j X i=1

(κi −κi+1) wi. (20)

<!-- Page 73 -->

Taking j = m yields the claim since Gm = G. Base case j = 1 We have G1 = G<w2, hence every edge in G1 has weight w1. Any spanning forest of G1 has exactly |V (G)| −κ2 edges, so

MSF(G1) = (|V (G)| −κ2) w1 = (κ1 −κ2) w1, since G<w1 has no edges and thus κ1 = #cc(G<w1) = |V (G)|. Induction step Assume (20) holds for j −1. Let H:= Gj−1 = G<wj, so #cc(H) = κj and all edges in H have weight < wj.

Upper bound Let F be a minimum spanning forest of H, so MSF(H) = P e∈E(F) wG(e) and F has κj components. Since Gj has κj+1 connected components, there exists a set S ⊆E(Gj) of exactly κj −κj+1 edges of weight wj that connect components of F without creating cycles. Then F ∪S is a spanning forest of Gj, and therefore

MSF(Gj) ≤

X e∈E(F∪S)

wG(e) = MSF(H) + (κj −κj+1) wj.

Lower bound Let T be any spanning forest of Gj. Removing all edges of weight wj from T leaves a forest T<wj ⊆E(H), so T<wj has at least κj components. Each edge of weight wj in T can reduce the number of components by at most 1, hence T must contain at least κj −κj+1 edges of weight wj. Thus

X e∈E(T)

wG(e) ≥

X e∈E(T<wj)

wG(e) + (κj −κj+1) wj ≥MSF(H) + (κj −κj+1) wj.

Taking the minimum over all such T yields

MSF(Gj) ≥MSF(H) + (κj −κj+1) wj.

Combining the bounds gives MSF(Gj) = MSF(H) + (κj −κj+1) wj, and substituting the induction hypothesis for MSF(H) = MSF(Gj−1) proves (20).

Claim 83. Let (G, wG) and (H, wH) be edge-weighted graphs that are (1,1)-WL indistinguishable. Then W(G) = W(H). Assume that W(G) = {w1,..., wm} with w1 < w2 < · · · < wm. Then for every j ∈[m],

#cc(G<wj) = #cc(H<wj) and #cc(G) = #cc(H).

Proof. By (1,1)-WL-indistinguishability there exists a bijection π: V (G) →V (H) such that for all v ∈V (G), (G, v, H, π(v)) are 1-iWL-indistinguishable regarding v and π(v). In particular, unr(G, v,1, v) and unr(H, π(v),1, π(v)) are isomorphic, for all v ∈V (G). These unrolling trees contain all edge weights in the respective graphs. Hence, W(G) = W(H).

Fix j ∈[m]. Consider the unweighted graphs G<wj and H<wj. It is readily verified by unrolling tree characterization that G<wj and H<wj are also (1,1)-WL-equivalent. Hence, by the spectral characterization of (1,1)-WL via equitable matrix maps, the Laplacian spectra of G<wj and H<wj coincide [92]. The multiplicity of eigenvalue 0 of the Laplacian equals the number of connected components, hence #cc(G<wj) = #cc(H<wj). The same argument yields #cc(G) = #cc(H).

We are now finally ready to formally prove Lemma 76. Indeed, if (G, wG) and (H, wH) are (1,1)-WL-indistinguishable, then by the previous claim, #cc(G<wj) = #cc(H<wj) and #cc(G) = #cc(H). Applying Lemma 82 the suffices to conclude MST(G) = MST(H), as desired.

<!-- Page 74 -->

G. MPNN classes satisfying finite Lipschitzness

(a) Small graph s v

10

40

10

11

10 10

(b) Tree at v Tv v s s

(c) Large graph s v

10

40

10

41

10

10

11

12

10

10

10

(d) Tree at v Tv v s s s s

(e) Compact tree space

T (compact)

Tsmall

Tlarge

**Figure 5.** A compact space of computation trees enables algorithmic generalization. Under

an appropriate metric on T, the computation trees Tsmall and Tlarge are close, so regularization-induced Lipschitz continuity of the model implies that good performance on the training instance Tsmall transfers to good performance on the nearby instance Tlarge. Occurrences of v in the computation tree other than the root are omitted for simplicity.

Below, we describe hypothesis classes for graph learning models—which capture many wellknown graph algorithms—that satisfy the finite Lipschitz learning property introduced in Definition 2 and, consequently, Theorem 3. Throughout, the input space X consists of pairs of graphs and vertices belonging to these graphs. The parameter space Θ is a subset of RP for some P ∈N, which will be specified later. We equip the input space with a suitable pseudo-metric such that the conditions of Definition 2 are satisfied. More precisely, we first establish this property for message passing neural networks (MPNNs) with normalized sum aggregation. This result largely follows existing work (see, e.g., [93, 35, 10]) based on iterated degree measure spaces, a continuous counter part of computation trees (see Section K), endowed with the Kantorovich distance (see Section H), but with important simplifications. In particular, in our setting, it is not necessary to show compactness of the input space, since Definition 2 requires only a weaker condition, namely finiteness of the covering number. We then extend the result to MPNNs with mean aggregation.

Finally, using similar tools but working on different topological spaces—namely, Hausdorff spaces instead of measure spaces, equipped with the Hausdorff distance—we show that MPNNs with max and min aggregation satisfy the finite Lipschitz learning property. These architectures capture many commonly used graph algorithms, including shortest-path algorithms, minimum spanning tree problems, and related tasks. Below, we present the precise architectures and

<!-- Page 75 -->

state the main result.

Overall, we get the following results.

Assumptions Let Gr,p0 denote the space of undirected attributed and edge-weighted graphs (G, aG, wG), without isolated vertices,5 with vertex features aG(u) ∈Br,p0:= {x ∈Rp0 | ∥x∥2 ≤ r} for all u ∈V (G), where p0 ∈N and r > 0, and edge-weights wG(e) ∈E ⊆R>0 for some compact set E, for all e ∈E(G). Also, let V1(Gr,p0) denote the space consisting of pairs of graphs in Gr,p0 and their vertices (i.e., V1(Gr,p0) = {(G, u) | G ∈Gr,p0, u ∈V (G)}).

Let L ∈N and let pt ∈N. Let ϕ1: Br,p0 × Br,p0 →Rp1, and ϕt: Rpt−1 × Rpt−1 →Rpt (t > 1), Mt: Rpt−1 × R →Rpt−1 (t ≥1).

We assume that for each t ∈[L] there exist constants C(t)

ϕ,1, C(t)

ϕ,2, C(t)

M,1, C(t)

M,2 > 0 such that

∥ϕt(x, y) −ϕt(x′, y′)∥2 ≤C(t)

ϕ,1∥x −x′∥2 + C(t)

ϕ,2∥y −y′∥2, ∀x, y, x′, y′ ∈Rpt−1.

∥Mt(x, y) −Mt(x′, y′)∥2 ≤C(t)

M,1∥x −x′∥2 + C(t)

M,2∥y −y′∥2, ∀(x, y), (x′, y′) ∈Rpt−1 × R.

Moreover, we assume bounded offsets, i.e., ∥ϕt(0,0)∥2 ≤B(0)

t, for some Bt > 0. Finally, for graph level predictions let ψ: RpL →Rd be a Lipschitz function with respect to the ∥· ∥2 norm.

Based on these assumptions on {ϕt}t∈[L] and ψ, we define three specific MPNN architectures, each of which is an instance of the general MPNN framework introduced in Equation (1).

Normalized sum aggregation Let (G, u) ∈V1(Gr,p0), define h(0)

u = aG(u) ∈Br,p0 and recursively h(t)

u = ϕt



h(t−1)

u, 1 |V (G)|

X v∈N(u)

wuv h(t−1)

v



, t ∈[L]. (21)

For graph-level tasks, the final d-dimensional representation is given by hG = ψ



 1 |V (G)|

X u∈V (G)

h(L)

u



.

A particular instance of such a hypothesis class is given by

FΘ:= n f: V1(Gr,p0) →RpL f(G, u) = h(L)

u, ϕt(x, y) = σ

W (t)

1 x + W (t) 2 y

,

W (t)

1, W (t) 2 ∈Rpt×pt−1, t ∈[L]

o

, where σ denotes the element-wise ReLU activation, or more generally any Lipschitz function (e.g., Leaky ReLU). For this class, the Lipschitz constants are C(t)

ϕ,1 = ∥W (t)

1 ∥2 and C(t) ϕ,2 = ∥W (t)

2 ∥2, while the offset bounds satisfy B(0)

t = 0. The parameter space Θ consists of all matrices {W (t)

1, W (t) 2 }t∈[L]. Although ϕt is defined here as a single-layer feed-forward network, the same construction extends to arbitrary-depth feed-forward networks with ReLU (or any other 1-Lipschitz) activations; in that case, C(t) ϕ,1 and C(t)

ϕ,2 are given by the products of the spectral norms of the corresponding weight matrices.

5We consider non-isolated vertices to avoid division by zero for mean aggregation and empty sets for max aggregation in Section J.1.

<!-- Page 76 -->

Mean aggregation Let (G, u) ∈V1(Gr,p0), define h

(0) u = aG(u) ∈Br,p0 and recursively:

h

(t) u = ϕt



h

(t−1) u, 1 deg(u)

X v∈N(u)

wuv h

(t−1) v



, t ∈[L]. (22)

For graph-level tasks, we again define hG = ψ



 1 |V (G)|

X u∈V (G)

h

(L) u



.

A special case of such a hypothesis class can be derived similarly to normalized sum aggregation MPNNs by replacing ϕt, with FNNs.

Max-min aggregation Let (G, u) ∈V1(Gr,p0), define ˆh(0)

u:= xu and, recursively:

ˆh(t)

u = ϕt

ˆh(t−1)

u, maxv∈N(u) Mt

ˆh(t−1)

v, wuv

, (23)

where The maximum in Equation (23) is taken coordinatewise in Rpt−1. Note that similarly we can define MPNNs based on min aggregation by replacing the max operator with min.

A special case of such a hypothesis class can be derived similarly to normalized sum aggregation MPNNs by replacing ϕt and Mt with FNNs.

The following result shows that all the above-defined families of MPNNs satisfied the finite Lipschitz property from Definition 2.

Theorem 84 (Theorem 4 in the main text). The hypothesis class FΘ induced by MPNNs using any one of the following aggregation schemes, normalized sum aggregation (Equation (21)), mean aggregation (Equation (22)), or max (or min) aggregation (Equation (23)), satisfies Definition 2.

Proof. see Section I, Section J.

Remark The above result extends directly to graph-level representations. Indeed, if the readout function ψ is Lipschitz, then the composition of the vertex-level MPNN with ψ remains Lipschitz with respect to the induced graph-level pseudo-metric. Consequently, the finite Lipschitz learning property continues to hold for graph-level prediction tasks.

Extensions to mixed aggregation architectures The exclusivity of the aggregation choices in Theorem 4 reflects a technical limitation of the proof strategy, i.e., the pseudometrics introduced in Sections I and J are tailored to individual aggregation mechanisms and do not suffice to establish the result simultaneously for all of them, nor for architectures that combine multiple aggregation operators.

Nevertheless, the proof techniques developed in Sections I and J extend beyond the specific aggregation schemes considered there. By equipping the relevant input spaces with product topologies endowed with summed metrics, one can naturally combine different aggregation mechanisms, such as mean or normalized sum, together with max (or min), within a single GNN architecture. More generally, the arguments can be unified by considering a generic aggregation operator and defining suitable pseudometrics on the associated iterated neighborhood spaces, such as the Kantorovich–Rubinshtein distance on spaces of iterated degree measures or the Hausdorff distance on spaces of iterated neighborhood sets. With these choices, the input space remains compact, and both aggregation and update maps remain Lipschitz with respect to the resulting metrics.

<!-- Page 77 -->

H. Topological, measure-theoretic, and geometric background

This appendix collects all background material required for the proof of Theorem 4. The central objective is to construct suitable metric spaces for vertex and neighborhood representations induced by message passing neural networks, and to show that these spaces are compact. Compactness will later imply the finiteness of covering numbers, which is the key condition in Definition 2.

The appendix is organized as follows. Section H.1 recalls basic notions from topology and metric geometry. Section H.2 reviews measure-theoretic preliminaries and weak∗convergence. Section H.3 introduces iterated degree measures and the Kantorovich–Rubinshtein metric, which underpins the analysis of sum and mean aggregation. Section H.4 develops the hyperspace and Hausdorff-metric framework needed for max (and min) aggregation.

H.1. Topological background

We begin by recalling standard definitions from topology, emphasizing compactness and product constructions, which will be repeatedly used in later proofs.

Definition 85 (Topological space). A topological space is a pair (X, τ), where X is a set and τ is a collection of subsets of X containing the empty set and X, closed under arbitrary unions and finite intersections. The elements of τ are called open sets.

Let (X, τX) and (Y, τY) be topological spaces. A map f: X →Y is said to be continuous if for every open set U ⊆Y, the preimage f−1(U) is an open subset of X.

Let τ1 and τ2 be two topologies on the same set X. We say that τ1 is coarser than τ2 if τ1 ⊆τ2.

Definition 86 (Product topology). Let {(Xi, τi)}i∈I be a family of topological spaces. The product topology on Q i∈I Xi is the coarsest topology for which all coordinate projections are continuous.

Definition 87 (Compact space). A topological space (X, τ) is compact if every open cover of X admits a finite subcover.

Theorem 88 (Tychonoff). The product of compact topological spaces is compact with respect to the product topology.

Definition 89 (Metric space and induced topology). Let X be a set. A function d: X × X → [0, +∞) is a metric on X if, for all x, y, z ∈X, d(x, y) = 0 ⇐⇒x = y, d(x, y) = d(y, x), d(x, z) ≤d(x, y) + d(y, z).

The pair (X, d) is called a metric space. The metric d induces a topology on X whose open sets are those U ⊂X such that for every x ∈U there exists ε > 0 with Bd(x, ε) ⊂U.

Definition 90 (Metrizable topology). A topological space (X, τ) is said to be metrizable if there exists a metric d on X such that the topology induced by d coincides with τ.

<!-- Page 78 -->

H.2. Measure-theoretic background

We next recall basic measure-theoretic notions that will be used to model neighborhood aggregation by averaging or summation.

Let X be a set. A collection A ⊆2X is a σ-algebra if X ∈A, A is closed under complements, and under countable unions.

Definition 91 (Measure). Let (X, A) be a measurable space. A measure on (X, A) is a map µ: A →[0, ∞] such that µ(∅) = 0 and µ



[ i∈N

Ai



=

X i∈N µ(Ai)

for every countable collection of pairwise disjoint sets.

Given a collection S ⊆2X, we denote by σ(S) the smallest σ-algebra containing S. Given a topological space (X, τ), we denote by B(X) = σ(τ) the Borel σ-algebra on X, by M≤1(X) the space of finite Borel measures with total mass at most 1, and by P(X) the space of finite Borel measures with total mass exactly 1 (i.e., probability measures).

Definition 92 (Weak∗topology). Let (X, τ) be a topological space. The weak∗topology on M≤1(X) (or similarly on P(X)) is the coarsest topology such that, for every bounded continuous function f: X →R, the map µ 7→

Z

X f dµ is continuous.

Theorem 93 ([51], Theorem 17.22). If (X, τ) is a compact metrizable space, then the space M≤1(X) (similarly P(X)), endowed with the weak∗topology, are also compact and metrizable.

H.3. Iterated degree measures and Kantorovich–Rubinshtein metric

This subsection develops the measure-valued representation spaces used for normalized-sum and mean aggregation. We recall that Br,p0:= {x ∈Rp0 | ∥x∥2 ≤r}.

Definition 94 (Iterated degree measures). Let L ∈N. We define recursively a sequence of spaces {Mℓ}L ℓ=0 and {Hℓ}L ℓ=0 as follows.

• Set M0:= Br,p0, H0:= M0.

• For each ℓ≥0, define

Mℓ+1:= M≤1(Hℓ), Hℓ+1:= ℓ+1 Y j=0

Mj.

Note that, an element of Mℓis a (sub-)probability measure on the space Hℓ−1, whereas an element of Hℓis a tuple

(h0, h1,..., hℓ), hj ∈Mj for each j ≤ℓ.

In particular, for ℓ≥1, the space Hℓcollects the iterated degree measures up to level ℓ, while Mℓ+1 consists of measures supported on such tuples.

<!-- Page 79 -->

Definition 95 (Kantorovich–Rubinshtein distance). Let (X, d) be a metric space and let µ, ν ∈M≤1(X). Define

Lip1(X, R):= {f: X →R | |f(x) −f(x′)| ≤d(x, x′) ∀x, x′ ∈X}.

The Kantorovich–Rubinshtein distance is

K(µ, ν):= sup f∈Lip1(X,R)

∥f∥∞≤1

Z

X f dµ −

Z

X f dν

.

Remark 96. When µ and ν are probability measures on X, the Kantorovich–Rubinshtein distance coincides with the 1-Wasserstein distance and admits an equivalent formulation as an optimal transportation problem (see [15]). The restriction to bounded test functions in the supremum is essential for well-definedness when considering finite (sub-probability) measures. Indeed, without imposing a bound on f, every constant function f ≡c is 1-Lipschitz and if µ(X)̸ = ν(X), then

R

X f dµ −

R

X f dν = c µ(X) −ν(X)

, which can be made arbitrarily large in absolute value by letting |c| →∞. Consequently, the supremum would be infinite.

Kantorovich–Rubinshtein recursive metric We define a metric dK,t on HL, for t ∈N recursively as follows. For x, y ∈H0, recall H0 = M0 = Br,p0, and set d0(x, y) = ∥x −y∥2. For t ≥1, let x = (η, µ) and x′ = (η′, µ′) be elements of Ht, where η, η′ ∈Ht−1 and µ, µ′ ∈Mt. Define dt(x, x′):= dt−1(η, η′) + K(µ, µ′).

Theorem 97. For every L ∈N, (HL, dL) is a compact metric space.

Proof. We prove the theorem by induction on t. We begin by stating four claims that will be used throughout the proof.

Claim 1. If (X, d) is a compact metric space, then M≤1(X) is compact with respect to the weak∗topology. This follows from Theorem 93.

Claim 2. If (X, d) is a compact metric space, then the Kantorovich–Rubinstein metric K defined in Definition 95 metrizes the weak∗topology on M≤1(X). This follows from Bogachev [8][Theorem 8.3.2].

Claim 3. If A and B are compact topological spaces, then A × B is compact with respect to the product topology. This is a direct consequence of Tychonoff’s theorem (Theorem 88).

Claim 4. Let (A, dA) and (B, dB) be metric spaces, and define the sum metric d on A × B by d

(a, b), (a′, b′)

:= dA(a, a′) + dB(b, b′).

Then d metrizes the product topology induced by dA and dB. Indeed, for any ε > 0,

BdA a, ε/2

× BdB b, ε/2

⊆Bd

(a, b), ε

⊆BdA(a, ε) × BdB(b, ε), where for a metric space (X, d) and ε > 0 we write

Bd(x, ε) = {y ∈X | d(x, y) ≤ε}.

<!-- Page 80 -->

We now proceed with the proof. For the base case t = 0, we have H0 = Br,p0 with dK,0(x, y) =

∥x −y∥2. Since Br,p0 is closed and bounded in Rp0, it is compact. Hence (H0, dK,0) is compact.

For the induction step, assume that (Ht−1, dK,t−1) is a compact metric space for some t ≥1. We show that (Ht, dK,t) is compact. By the induction hypothesis and Claim 1, M≤1(Ht−1) = Mt is compact in the weak∗topology. By Claim 2, the metric K metrizes this topology, so (Mt, K) is a compact metric space. Since Ht = Ht−1 × Mt and both Ht−1 and Mt are compact, Claim 3 implies that Ht is compact with respect to the product topology. Finally, by Claim 4, the topology induced by dK,t coincides with the product topology induced by dK,t−1 on Ht−1 and K on Mt. Therefore, (Ht, dK,t) is compact, completing the induction.

H.4. Hyperspaces and Hausdorff metrics for max aggregation

We now turn to max (and min) aggregation, where neighborhoods are encoded as compact sets rather than measures.

Hyperspace and Hausdorff metric Let (X, d) be a metric space and denote by

Haus(X):= {A ⊆X | A̸ = ∅, A is compact}.

the hyperspace of nonempty compact subsets of X. The Hausdorff metric on Haus(X) induced by d is denoted by Hd and is defined as

Hd(A, B) = max n sup a∈A inf b∈B d(a, b), sup b∈B inf a∈A d(a, b)

o

.

The following result is a corollary of the Blaschke Selection Theorem [102][Thm. 1.8.4].

Theorem 98. Let (X, d) be compact. Then (Haus(X), Hd) is compact.

Iterated neighborhood set spaces Let E ⊂Re be compact. Define recursively

• Smax 0 = Br,p0, Hmax

0 = Smax

0.

• Y max t = Hmax t × E, Smax t+1 = Haus(Y max t), Hmax t+1 = Hmax t × Smax t+1.

Hausdorff recursive metric We define a metric dH,t on Hmax t recursively. For x, y ∈Hmax

0, set dH,0(x, y):= ∥x −y∥2.

Equip Y max t−1 = Hmax t−1 × E with the product metric dY,t−1

(η, e), (η′, e′)

:= dH,t−1(η, η′) + ∥e −e′∥2.

Let Ht−1 denote the Hausdorff metric on Haus(Y max t−1) induced by dY,t−1. For t ≥1 and x = (η, A), x′ = (η′, A′) in Hmax t = Hmax t−1 × Smax t, define dH,t(x, x′):= dH,t−1(η, η′) + Ht−1(A, A′).

Theorem 99 (Compactness of (Hmax t, dH,t)). For every t ∈N, the space (Hmax t, dH,t) is a compact metric space.

<!-- Page 81 -->

Proof. We prove the theorem by induction on t. For t = 0, by definition, Hmax

0 = Br,p0 and dH,0(x, y) = ∥x −y∥2, hence (Hmax

0, dH,0) is compact. Assume that (Hmax t−1, dH,t−1) is compact for some t ≥1. We show that (Hmax t, dH,t) is compact. By the induction hypothesis and the compactness of the edge-feature space E, the product space Y max t−1 = Hmax t−1 × E is compact with respect to the sum metric dY,t−1 (see Claim 4 in the proof of Theorem 97). By Theorem 98, the hyperspace Haus(Y max t−1) endowed with the Hausdorff metric Ht−1 is compact. Hence the neighborhood set space Smax t is compact. Since Hmax t = Hmax t−1 × Smax t is a finite product of compact spaces, it is compact in the product topology (Theorem 88). Finally, by construction, the metric dH,t

(η, A), (η′, A′)

= dH,t−1(η, η′) + Ht−1(A, A′)

metrizes the product topology (again see Claim 4 in Theorem 97). Therefore (Hmax t, dH,t) is compact.

I. Proof of Theorem 4 for sum/mean-aggregation

This section proves Theorem 4 for the normalized-sum and mean aggregation schemes. The overall strategy is to construct, for each (G, u) ∈Gr,p0 ⊗V, a canonical iterated degree measure (IDM) representation in the compact metric space (HL, dK,L) from Appendix H. This allows us to endow Gr,p0 ⊗V with a pseudo-metric induced by dK,L and to deduce finiteness of covering numbers from compactness. We then show that the MPNN maps are Lipschitz with respect to these pseudo-metrics, completing the verification of Definition 2 for the two aggregation schemes.

Roadmap We proceed in three steps:

1. In Section I.1, we define the induced IDM maps and the corresponding pseudo-metrics on V1(Gr,p0).

2. In Section I.2, we prove Lipschitz continuity of the normalized-sum and mean MPNNs with respect to the induced pseudo-metrics (via the equivalent IDM formulations).

3. In Section I.3, we state the main conclusion (Theorem 5 in the main paper) and explain how it follows immediately from the Lipschitz bounds and compactness/covering arguments.

Normalized-sum and mean-aggregation MPNNs We recall the normalized-sum and meanaggregation schemes defined in Equation (21) and Equation (22). Fix L ∈N. For (G, u) ∈ V1(Gr,p0), set h(0)

u = h

(0) u:= xu and, for t ∈[L], define h(t)

u = ϕt



h(t−1)

u, 1 |V (G)|

X v∈N(u)

wuv h(t−1)

v



 h

(t) u = ϕt



h

(t−1) u, 1 deg(u)

X v∈N(u)

wuv h

(t−1) v



 where deg(u):= P v∈N(u) wuv. For each t ∈[L], we assume that the update map ϕt: Rpt−1 ×

Rpt−1 →Rpt is Lipschitz, i.e., there exist constants C(t)

ϕ,1, C(t)

ϕ,2 > 0 such that

∥ϕt(x, y) −ϕt(x′, y′)∥2 ≤C(t)

ϕ,1∥x −x′∥2 + C(t)

ϕ,2∥y −y′∥2, ∀x, x′, y, y′ ∈Rpt−1.

<!-- Page 82 -->

I.1. Induced IDMs and pseudo-metrics

In this subsection, we construct mappings from the space V1(Gr,p0) to the space of iterated degree measures (IDMs) HL. This allows us to endow V1(Gr,p0) with a pseudo-metric defined as the recursive Kantorovich–Rubinshtein metric on HL, evaluated on the induced elements. Using the compactness result proved in Appendix H (in particular, Theorem 97), we will later deduce finiteness of the covering number of V1(Gr,p0) with respect to this pseudo-metric. Moreover, we aim to construct these mappings in such a way that message passing neural networks (MPNNs) are Lipschitz continuous with respect to the induced pseudo-metric. For this reason, we introduce different mappings from V1(Gr,p0) to HL, depending on the aggregation scheme under consideration (normalized-sum or mean). We therefore define below two different induced IDMs, one for each aggregation scheme. For this section, without loss of generality we assume that for all G ∈Gr,p0, the edge weights wuv ∈E(0,1] for all {u, v} ∈E(G) (i.e., E ⊂(0,1] compact).

Normalized-sum induced IDMs Let (G, u) ∈V1(Gr,p0). We define the normalized-sum induced IDM of order t, denoted by η(t)

u, recursively as follows. Set η(0)

u = xu, where xu denotes the initial vertex features of the vertex u ∈V (G). For t ≥0, we define η(t+1)

u = η(t)

u, µ(t+1)

u

∈Ht × Mt+1 = Ht+1, where µ(t+1)

u = 1 |V (G)|

X v∈N(u)

wuv δη(t)

v.

Here, δη denotes the Dirac measure concentrated at the point η ∈Ht, that is, for any measurable set A ⊂Ht, δη(A) =

(

1, if η ∈A, 0, otherwise.

Mean induced IDMs Let (G, u) ∈V1(Gr,p0). We define the mean induced IDM of order t, denoted by η(t)

u, recursively as follows. Let deg(u) =

X v∈N(u)

wuv > 0.

The positivity of deg(u) holds since, by definition, graphs in Gr,p0 do not contain isolated vertices. We set η(0)

u = aG(u).

For t ≥0, we define η(t+1)

u = η(t)

u, π(t+1)

u

∈Ht × Mt+1 = Ht+1, where π(t+1)

u = 1 deg(u)

X v∈N(u)

wuv δη(t)

v.

<!-- Page 83 -->

Induced pseudo metric on V1(Gr,p0) Since dK,L is a well-defined metric on HL, the following pseudo-metrics on V1(Gr,p0) are well defined for (G, u), (G′, u′) ∈V1(Gr,p0):

(i) the normalized-sum pseudo-metric dsum,L

(G, u), (G′, u′)

:= dK,L η(L)

u, η(L)

u′

,

(ii) the mean-aggregation pseudo-metric dmean,L

(G, u), (G′, u′)

:= dK,L η(L)

u, η(L)

u′

.

Below, we derive equivalent expressions of the MPNNs defined in Equation (21) and Equation (22) through their induced IDMs. These formulations will be used later to prove the Lipschitz property with respect to the corresponding pseudo-metrics in Propositions 102 and 103.

Lemma 100. For (G, u) ∈V1(Gr,p0), let h(t)

u, and h

(t) u be as defined in Equation (21), and Equation (22), respectively. Let η(t)

u, and η(t)

u, denote the corresponding induced IDMs defined above. Then, for all t ∈N, the following identities hold:

(i) h(t)

u = g(t)

sum(η(t)

u):= ϕt g(t−1)

sum η(t−1)

u

,

R g(t−1)

sum (z) dµ(t)

u (z)

,

(ii) h

(t) u = g(t)

mean(η(t)

u):= ϕt g(t−1)

mean η(t−1)

u

,

R g(t−1)

mean (z) dπ(t)

u (z)

.

where h(0)

u = g(0)

sum(η(0)

u) = g(0)

mean(η(0)

u):= η(0)

u = aG(u) for all (G, u) ∈V1(Gr,p0).

Proof. The proof proceeds by induction on t. By direct application of the definition of IDMs, we obtain Z g(t)(z) dµ(t+1)(z) = 1 |V (G)|

X v∈N(u)

wuvg(t)

η(t)

v

.

The claim then follows by applying the induction hypothesis.

The following lemma reduces differences of vector-valued integrals to scalar-valued ones, allowing us to apply the Kantorovich–Rubinshtein distance later.

Lemma 101. Let (X, A) be a measurable space, let µ, µ′ be finite measures on (X, A), and let G: X →Rm be integrable with respect to both µ and µ′. Then

Z

X

G dµ −

Z

X

G dµ′

2 = sup ∥a∥2≤1

Z

X

⟨a, G(x)⟩dµ(x) −

Z

X

⟨a, G(x)⟩dµ′(x)

.

Proof. Set v:=

Z

X

G dµ −

Z

X

G dµ′ ∈Rm.

By the dual characterization of the Euclidean norm,

∥v∥2 = sup ∥a∥2≤1

⟨a, v⟩= sup ∥a∥2≤1

|⟨a, v⟩|.

Using linearity of the integral and the inner product, for each a ∈Rm we have

⟨a, v⟩= a,

Z

X

G dµ −

Z

X

G dµ′

=

Z

X

⟨a, G(x)⟩dµ(x) −

Z

X

⟨a, G(x)⟩dµ′(x).

Substituting into the previous yields the claimed identity.

<!-- Page 84 -->

I.2. Lipschitzness of sum/mean MPNNs

We now establish Lipschitz continuity of the normalized-sum and mean MPNN maps with respect to the induced pseudo-metrics. This is the key analytic step that connects the recursive representation space geometry to the stability of message passing.

Proposition 102 (Lipschitzness of normalized-sum MPNNs). Fix L ∈N and consider the normalized-sum MPNN in Equation (21). Let g(t)

sum: Ht →Rpt be defined as in Lemma 100, i.e., h(t)

u = g(t)

sum(η(t)

u) for all (G, u) ∈V1(Gr,p0). Then for each t ∈[L], the map g(t) is Lipschitz with respect to dK,t. In particular, the function fsum: V1(Gr,p0) →RpL defined by fsum(G, u):= h(L)

u is Lipschitz with respect to dsum,L, i.e., there exists Csum,L > 0 such that

∥fsum(G, u) −fsum(G′, u′)∥2 ≤Csum,L dsum,L

(G, u), (G′, u′)

, ∀(G, u), (G′, u′) ∈V1(Gr,p0).

Proof. We prove by induction on t that there exist constants Ct, bt > 0 such that, for all x, x′ ∈Ht,

∥g(t)

sum(x) −g(t)

sum(x′)∥2 ≤Ct dK,t(x, x′) and sup x∈Ht

∥g(t)(x)∥2 ≤Bt.

We have H0 = Br,p0, g(0)

sum(η) = η, and dK,0(η, η′) = ∥η −η′∥2. Hence C0 = 1 and B0 = r. Assume the claim holds for t −1, with constants Ct−1 and Mt−1. Let x = (η, µ) and x′ = (η′, µ′) in Ht, where η, η′ ∈Ht−1 and µ, µ′ ∈Mt. By Lemma 100, g(t)

sum(x) = ϕt g(t−1)

sum (η),

Z g(t−1)

sum (z) dµ(z)

, g(t)(x′) = ϕt g(t−1)

sum (η′),

Z g(t−1)

sum (z) dµ′(z)

.

Using the assumed Lipschitz property of ϕt, we obtain

∥g(t)

sum(x) −g(t)

sum(x′)∥2 ≤C(t)

ϕ,1∥g(t−1)

sum (η) −g(t−1)

sum (η′)∥2 + C(t)

ϕ,2

Z g(t−1)

sum dµ −

Z g(t−1)

sum dµ′

2.

Bounding the integral term Let G: Ht−1 →Rpt−1 denote g(t−1)

sum. For any unit vector a ∈Rpt−1 with ∥a∥2 ≤1, define the scalar function fa: Ht−1 →R as fa(z):= ⟨a, G(z)⟩. Then

∥fa∥∞≤Bt−1, Lip(fa) ≤Ct−1.

where Lip(fa) denotes the smallest Lipschitz constant of fa.

Set λt−1:= Bt−1 + Ct−1 and define efa:= fa/λt−1. Then ∥efa∥∞≤1 and Lip(efa) ≤1, so by definition of K,

Z fa dµ −

Z fa dµ′

= λt−1

Z efa dµ −

Z efa dµ′

≤λt−1 K(µ, µ′).

Taking the supremum over ∥a∥2 ≤1 and using Lemma 101 yields

Z

G dµ −

Z

G dµ′

2 ≤λt−1 K(µ, µ′).

<!-- Page 85 -->

Lipschitzess of g(t) By the induction hypothesis,

∥g(t−1)

sum (η) −g(t−1)

sum (η′)∥2 ≤Ct−1 dK,t−1(η, η′).

Combining with the previous gives

∥g(t)

sum(x) −g(t)

sum(x′)∥2 ≤C(t)

ϕ,1Ct−1 dK,t−1(η, η′) + C(t)

ϕ,2λt−1 K(µ, µ′).

Since dK,t(x, x′) = dK,t−1(η, η′) + K(µ, µ′), we obtain

∥g(t)

sum(x) −g(t)

sum(x′)∥2 ≤Ct dK,t(x, x′), Ct:= max n

C(t)

ϕ,1Ct−1, C(t)

ϕ,2(Bt−1 + Ct−1)

o

.

Boundedness of g(t) Let x = (η, µ) ∈Ht. Using the Lipschitz bound for ϕt and the offset assumption,

∥g(t)(x)∥2 ≤∥ϕt(0,0)∥2 + C(t)

ϕ,1∥g(t−1)(η)∥2 + C(t)

ϕ,2

Z g(t−1)(z) dµ(z)

2.

Since µ has total mass at most 1 in the normalized-sum case, we have

Z g(t−1)(z) dµ(z)

2 ≤

Z

∥g(t−1)(z)∥2 dµ(z) ≤Bt−1 µ(Ht−1) ≤Bt−1.

Therefore,

∥g(t)(x)∥2 ≤Bt + (C(t)

ϕ,1 + C(t)

ϕ,2)Bt−1, so it suffices to take

Bt:= B(ϕ)

t + (C(t)

ϕ,1 + C(t)

ϕ,2)Bt−1.

This completes the induction. Overall, we have that for (G, u), (G′, u′) ∈V1(Gr,p0), we have

∥h(L)

u −h(L)

u′ ∥2 = ∥g(L)(η(L)

u) −g(L)(η(L)

u′)∥2 ≤CL dK,L η(L)

u, η(L)

u′

= CL dsum,L

(G, u), (G′, u′)

.

Thus fsum is Lipschitz with Lipschitz constant Csum,L:= CL.

Proposition 103 (Lipschitzness of mean-aggregation MPNNs). Fix L ∈N and consider the mean-aggregation MPNN in Equation (22). For each t ∈{0,..., L}, let

HG t:= n η(t)

u

(G, u) ∈Gr,p0 ⊗V o

⊆Ht denote the set of mean-induced IDMs of order t. Let g(t): HG t →Rpt be defined as in Lemma 100, i.e., h

(t) u = g(t)(η(t)

u) for all (G, u) ∈V1(Gr,p0). Then, for each t ∈[L], the map g(t) is Lipschitz with respect to dK,t restricted to HG t. In particular, the function fmean: V1(Gr,p0) →RpL defined by fmean(G, u):= h

(L) u is Lipschitz with respect to dmean,L, i.e., there exists Cmean,L > 0 such that

∥fmean(G, u)−fmean(G′, u′)∥2 ≤Cmean,L dmean,L

(G, u), (G′, u′)

, ∀(G, u), (G′, u′) ∈V1(Gr,p0).

Proof. The proof follows the same argument as in Proposition 102, with the only changes that we work on the restricted domain HG t, so that mean-aggregation is well defined, and we replace the induced measures µ(t)

u by π(t)

u.

<!-- Page 86 -->

I.3. Conclusion: finite Lipschitz classes for sum/mean aggregation

We now state the main consequence for the normalized sum and mean aggregation, corresponding to Theorem 5 in the main paper, and explain how it follows directly from the Lipschitz continuity established above together with compactness (hence total boundedness) of the representation space (HL, dK,L).

Theorem 104 (Theorem 4 (sum/mean aggregation) in the main text). Fix L ∈N. Consider the hypothesis class induced by the normalized-sum MPNN Equation (21) (respectively, the mean-aggregation MPNN Equation (22)) with Lipschitz update maps {ϕt}t∈[L] as assumed in the main text. Endow V1(Gr,p0) with the pseudo-metric dsum,L (respectively, dmean,L). Then the resulting hypothesis class is a finite Lipschitz class in the sense of Definition 2.

Proof. By Proposition 102 (respectively, Proposition 103), the hypothesis map fsum(G, u) = h(L)

u (respectively fmean(G, u) = h

(L) u) is Lipschitz with respect to the induced pseudo-metric on V1(Gr,p0). By Theorem 97, the metric space (HL, dK,L) is compact, and therefore has finite covering number for every radius ε > 0. Since dsum,L and dmean,L are defined as pullbacks of dK,L through the induced IDM maps,

V1(Gr,p0), dsum,L and

V1(Gr,p0), dmean,L admit finite ε-covers for every ε > 0 as well.

Remark In the above result, the Lipschitz constant Mθ appearing in Definition 2 depends only on the Lipschitz constants {C(t)

ϕ,1, C(t)

ϕ,2}t∈[L] of the update maps {ϕt}t∈[L] and on the number of layers L, and is independent of the size or structure of the input graph. In particular, in the special case

FΘ:= n f: V1(Gr,p0) →RpL f(G, u) = h(L)

u, ϕt(x, y) = σ

W (t)

1 x + W (t) 2 y

,

W (t)

1, W (t) 2 ∈Rpt×pt−1, t ∈[L]

o

.

where σ is the ReLu function applied elementwise, the Lipschitz constant Mθ depends only on the operator 2-norms ∥W (t)

1 ∥2 and ∥W (t) 2 ∥2 of the weight matrices and on L.

J. Proof of Theorem 4 for max/min-aggregation

In this section, we prove Theorem 4 for max-aggregation MPNNs. We work in the slightly more general setting where edge weights are vectors in a compact set E ⊂Rde, for de ∈N; the result in the main paper corresponds to the special case de = 1. As in the sum/mean case, the proof proceeds by constructing a canonical representation space endowed with a compact metric and showing that the MPNN maps are Lipschitz with respect to the induced pseudo-metric on V1(Gr,p0).

Roadmap

The argument follows the same high-level structure as for sum/mean aggregation:

1. We introduce induced iterated neighborhood-set objects that encode rooted graph neighborhoods recursively.

## 2 We define an induced pseudo-metric on V1(Gr,p0) via a recursive

Hausdorff metric.

<!-- Page 87 -->

## 3 We show that max-aggregation MPNNs are

Lipschitz with respect to this pseudo-metric.

## 4 We conclude by combining Lipschitzness with compactness to verify

Definition 2.

Max-aggregation MPNNs We recall the max-aggregation scheme defined in Equation (23). Fix L ∈N. For (G, u) ∈V1(Gr,p0), define ˆh(0)

u:= xu and, for t ∈[L],

ˆh(t)

u = ϕt

ˆh(t−1)

u, maxv∈N(u) Mt

ˆh(t−1)

v, wuv

, (24)

where Mt: Rpt−1 × Rde →Rpt−1 is a message map and ϕt: Rpt−1 × Rpt−1 →Rpt is an update map. The maximum is taken coordinatewise in Rpt−1. For each t ∈[L], assume that ϕt and Mt are Lipschitz, i.e., there exist constants C(t)

ϕ,1, C(t)

ϕ,2, C(t)

M,1, C(t)

M,2 > 0 such that

∥ϕt(x, y) −ϕt(x′, y′)∥2 ≤C(t)

ϕ,1∥x −x′∥2 + C(t)

ϕ,2∥y −y′∥2, and

∥Mt(x, y) −Mt(x′, y′)∥2 ≤C(t)

M,1∥x −x′∥2 + C(t)

M,2∥y −y′∥2.

J.1. Induced iterated neighborhood-set objects

Here we represent neighborhoods as sets of feature–edge pairs. This leads to a recursive representation in terms of iterated neighborhood-set objects equipped with Hausdorff metrics. Let (G, u) ∈V1(Gr,p0). Define ηmax,(t)

u ∈Hmax t recursively by ηmax,(0)

u:= xu ∈Hmax

0 and, for t ≥0, ηmax,(t+1)

u:= ηmax,(t)

u, A(t+1)

u

∈Hmax t+1, A(t+1)

u:=

(ηmax,(t)

v, wuv): v ∈N(u)

.

Nonemptiness of A(t+1)

u follows since graphs in Gr,p0 have no isolated vertices. Let

HG,max t:= ηmax,(t)

u | (G, u) ∈V1(Gr,p0)

⊆Hmax t denote the collection of neighborhood-set objects induced by graph–vertex pairs. We define maps g(t)

max: HG,max t →Rpt recursively by g(0)

max(x) = x and, for t ∈[L], g(t)

max(η, A) = ϕt g(t−1)

max (η), max(z,w)∈A Γt(z, w)

, Γt(z, w):= Mt(g(t−1)

max (z), w), where the maximum is taken coordinatewise in Rpt−1.

Lemma 105 (Equivalent formulation for max-aggregation). For all (G, u) ∈V1(Gr,p0) and all t,

ˆh(t)

u = g(t)

max ηmax,(t)

u

.

Proof. We prove by induction on t.

For t = 0, ηmax,(0)

u = xu and ˆh(0)

u = xu, so define g(0)

max(η):= η. Assume the claim holds at depth t −1. Fix (G, u). By construction, ηmax,(t)

u = ηmax,(t−1)

u, A(t)

u

, A(t)

u = {(ηmax,(t−1)

v, wuv): v ∈N(u)}.

<!-- Page 88 -->

Using (24) and the induction hypothesis h(t−1)

v = g(t−1)

max (ηmax,(t−1)

v),

ˆh(t)

u = ϕt g(t−1)

max (ηmax,(t−1)

u), maxv∈N(u) Mt g(t−1)

max (ηmax,(t−1)

v), wuv

.

Since A(t)

u is precisely the set of pairs (ηmax,(t−1)

v, wuv), the maximum equals max(z,e)∈A(t)

u Γt(z, e)

with Γt(z, e):= Mt(g(t−1)

max (z), e). Define g(t)

max on induced elements by the stated recursion; then h(t)

u = g(t)

max(ηmax,(t)

u), completing the induction.

J.2. Induced pseudo-metric

Since (Hmax

L, dH,L) is a compact metric space (see Theorem 99), we may pull back its metric to obtain a pseudo-metric on rooted graphs. Define dmax,L

(G, u), (G′, u′)

:= dH,L ηmax,(L)

u, ηmax,(L)

u′

, (G, u), (G′, u′) ∈V1(Gr,p0). (25)

J.3. Lipschitzness of max-aggregation MPNNs

The next lemma shows that the coordinatewise maximum over a compact set is stable under perturbations measured by the Hausdorff distance.

Lemma 106. Let (X, d) be a metric space and let f: X →R be Lipschitz with constant Lf. Define

F(A):= max x∈A f(x), A ∈Haus(X).

Then F is Lf-Lipschitz with respect to Hd.

Proof. Fix A, B ∈Haus(X). Let x ∈A be such that f(x) = maxa∈A f(a). By definition of the Hausdorff distance Hd(A, B), there exists y ∈B such that d(x, y) ≤Hd(A, B).

Then

F(A) −F(B) = max a∈A f(a) −max b∈B f(b) ≤f(x) −f(y) ≤Lf d(x, y) ≤Lf Hd(A, B).

Similarly, for the difference F(B) −F(A).

We are now ready to establish the Lipschitz continuity of max-aggregation MPNNs with respect to the induced pseudo-metric.

Proposition 107 (Lipschitzness of max-aggregation MPNNs). Fix L ∈N and consider the max-aggregation MPNN defined in Equation (24). Then for each t ∈[L], the function fmax: V1(Gr,p0) →RpL, fmax(G, u):= ˆh(L)

u, is Lipschitz with respect to the induced pseudo-metric dmax,L (Equation (25)).

Proof. We prove by induction on t that there exist constants Ct, Bt > 0 such that for all x, x′ ∈HG,max t,

∥g(t)

max(x) −g(t)

max(x′)∥2 ≤Ct dH,t(x, x′), then the result follows directly by Lemma 105.

<!-- Page 89 -->

For t = 0, g(0)

max(η) = η, hence C0 = 1. Assume the claim holds for t −1. Let x = (η, A) and x′ = (η′, A′) in HG,max t. By Lemma 105, g(t)

max(x) = ϕt g(t−1)

max (η), max(z,e)∈AΓt(z, e)

, Γt(z, e) = Mt(g(t−1)

max (z), e), and similarly for x′.

Using the Lipschitz property of ϕt,

∥g(t)

max(x) −g(t)

max(x′)∥2 ≤C(t)

ϕ,1∥g(t−1)

max (η) −g(t−1)

max (η′)∥2 + C(t)

ϕ,2∥maxAΓt −maxA′Γt∥2, where maxAΓt abbreviates max(z,e)∈AΓt(z, e).

The first term is bounded by C(t)

ϕ,1Ct−1 dmax,t−1(η, η′) by the induction hypothesis. For the max term, fix a unit direction a ∈Rpt−1 with ∥a∥2 ≤1 and consider the scalar functional fa(z, e):= ⟨a, Γt(z, e)⟩on Y max t−1 = Hmax t−1 × E. By Lipschitzness of Mt and the induction hypothesis, fa is Lipschitz on (Y max t−1, dY,t−1) with constant at most C(t)

M Ct−1, uniformly in ∥a∥2 ≤1, C(t)

M:= max{C(t)

M,1, C(t)

M,2} Applying Lemma 106 on (Haus(Y max t−1), Ht−1) yields max(z,e)∈Afa(z, e) −max(z,e)∈A′fa(z, e)

≤C(t)

M Ct−1 Ht−1(A, A′).

Taking the supremum over ∥a∥2 ≤1 and using an argument identical to Lemma 101, gives

∥maxAΓt −maxA′Γt∥2 ≤C(t)

M Ct−1 Ht−1(A, A′).

Combining the bounds and recalling dH,t(x, x′) = dH,t−1(η, η′) + Ht−1(A, A′) yields a recursion of the form

∥g(t)

max(x) −g(t)

max(x′)∥2 ≤Ct dH,t(x, x′), Ct:= max n

C(t)

ϕ,1Ct−1, C(t)

ϕ,2C(t)

M Ct−1 o

.

J.4. Conclusion: finite Lipschitz class for max aggregation

We now state the final consequence for max aggregation, completing the proof of Theorem 4.

Theorem 108 (Theorem 4 (max/min aggregation) in the main text). Fix L ∈N. Consider the hypothesis class induced by the max-aggregation MPNN Equation (24). Endow V1(Gr,p0) with the pseudo-metric dmax,L. Then the resulting hypothesis class is a finite Lipschitz class in the sense of Definition 2.

Proof. By Proposition 107, the hypothesis map fmax(G, u) = ˆh(L)

u is Lipschitz with respect to dmax,L. By Theorem 99, (Hmax

L, dH,L) is compact which implies finite covering numbers for every radius ε. Since dmax,L is obtained by pulling back dH,L through the induced neighborhood-set map, the space V1(Gr,p0) endowed with dmax,L also admits finite ε-covers for all ε > 0. This verifies Definition 2.

<!-- Page 90 -->

Remark The Lipschitz constant Mθ in Definition 2 depends only on the Lipschitz constants of the message maps {Mt}t∈[L], the update maps {ϕt}t∈[L], and on the number of layers L, and is independent of the size or structure of the input graph. In particular, in the special case

FΘ:= n f: V1(Gr,p0) →RpL f(G, u) = h(L)

u, ϕt(x, y) = σ

W (t)

1 x + W (t) 2 y

,

Mt(z, w) = σ

U (t)

1 z + U (t) 2 w

,

W (t)

1, W (t) 2 ∈Rpt×pt−1, U (t)

1 ∈Rqt×pt−1, U (t)

2 ∈Rqt×e, t ∈[L]

o

, where σ is the ReLu function applied elementwise, the Lipschitz constant Mθ depends only on the 2-norms ∥W (t)

1 ∥2, ∥W (t) 2 ∥2, ∥U (t) 1 ∥2, and ∥U (t) 2 ∥2 of the weight matrices and on the depth L.

The same conclusions hold for min-aggregation, since min(−·) = −max(−·) and negation preserves all Lipschitz properties.

K. Iterated degree measures as computation trees

Computation trees or unrolling trees (see Section F.2) provide a convenient way to understand how message passing neural networks (MPNNs) propagate and aggregate information across a graph. Starting from a root vertex, a computation tree records its neighbors, the neighbors of those neighbors, and so on, up to a prescribed depth. Since MPNNs update vertex representations by repeatedly aggregating information from local neighborhoods, such trees encode precisely the information required to compute vertex features layer by layer.

Iterated degree measures (IDMs) can be viewed as a measure-theoretic analogue of these computation trees. Instead of explicitly storing finite sets of neighbors, IDMs represent neighborhoods as probability measures and neighborhoods of neighborhoods as measures over measures, recursively. This abstraction is particularly natural in the setting of graphons, which are continuous objects extending finite graphs. Formally, a graphon is a measurable function W: [0,1]2 →[0,1], which can be interpreted as a weighted graph with an uncountable vertex set [0,1], where the edge weight between two vertices x, y ∈[0,1] is given by W(x, y).

In a graphon, each vertex has infinitely many neighbors, and its neighborhood cannot be described by a finite multiset. Instead, the local structure around a vertex is naturally captured by a measure encoding the distribution of its neighbors and their attributes. Since edge weights are integrable, these neighborhood measures have total mass at most one. Iterating this construction—taking measures of neighborhood measures—yields exactly the hierarchy of spaces {Mℓ}L ℓ=0 and {Hℓ}L ℓ=0 introduced above. In this sense, IDMs serve as computation trees for graphons, providing a compact, recursive representation of increasingly deep neighborhood information. This perspective aligns with recent work connecting graph neural networks applied on graphons, and measure-based representations of local structure (see, e.g., [35]). See also [10], for a definition of the 1-WL algorithm applied on graphons based on the above analysis.

L. Experimental study

In the following, we outline details related to the experimental evaluation of Q1 to Q3 in Section 6. In addition, we provide further results on size generalization and training set construction. The source code for all experiments is available in the supplementary material.

<!-- Page 91 -->

**Table 3.** Parameters for generation of Erdős–Reyni and stochastic block model (SBM) graphs

in Q1 to Q3.

Dataset/Graphs n p weight

ER-constdeg 64-1024 6.4/n Uniform(1,100) ER 64-1024 0.1 Uniform(1,100) Star graphs 64-1024 - Uniform(1,100) Complete graphs 64-1024 - Uniform(1,100)

SBM 64-1024





0.7 0.05 0.02 0.05 0.6 0.03 0.02 0.03 0.4



 Uniform(1,100)

Dataset creation To investigate Q1, we construct multiple training and test datasets. Throughout the experiments, we consider two training sets of graphs. Building on theoretical results on minimal training samples for the SSSP problem, we construct a training set of the minimum number of path graphs, as outlined in Section 4. This results in a set of three graphs for a Bellman–Ford problem with two steps. In addition, we construct an extended training set to help with training in our MPNN setting. For this, we consider additional path graphs constructed in the same way as for the minimal training set with edge weight x, but with edges scaled by 0.5 and 2. Moreover, we add a special version of the path graph, which includes multiple paths to the furthest reachable vertex. In all training datasets, the initial Bellman–Ford state and edge weights are given. Moreover, the initial starting vertex is marked with 0 unless otherwise specified. For all experiments, we set the edge weight x = 50 and the value indicating unvisited vertices to 1000. In addition, all graphs in both the training and test datasets have a self-loop edge for each vertex.

As the simplest case of size generalization, we provide a test set, which we call ER-constdeg, of 200 randomly generated Erdős–Rényi graphs with an average vertex degree of 6.4. We fix the average vertex degree and increase the number of vertices, generating one dataset for each from 64 to 1024 vertices. Furthermore, we provide a second dataset generated from Erdös–Reyni graphs, but with an unbounded average degree. For this, we set p = 0.1 as the edge probability in the graph generator provided by NetworkX [39]. We call this dataset ER. Again, we provide a test dataset for 64 to 1024 vertices each. As the most general case of the test set, we provide a set of 50 graphs, each consisting of Erdös–Reyni graphs with unbounded degree, stochastic block model graphs with probability matrices outlined in Table 3, complete graphs as well as star graphs and path graphs as shown in Figure 4. This dataset is called General. Across all test datasets, the weight distribution is uniform on [1,100] for all graphs.

For Q2 and Q3, we consider the same training and test sets as in Q1. However, we restrict our evaluation to a subset of the test datasets, since Q1 showed that the General and ER test sets are sufficient for evaluating generalization capabilities.

Neural architectures The MPNN architecture discussed in Section 4 consists of an update and aggregation function mapping vertex and edge features to an intermediate representation. The ReLU activation function is used, except for the last layer, as this resulted in unstable training behavior. Moreover, all functions in each layer are implemented using a two-layer FNN with the configurations outlined in the following paragraph.

Hyperparameters and hardware Throughout all experiments, we trained the MPNN architectures for a total of 160000 steps with a learning rate of 0.001. Table 4 showcases tuned

<!-- Page 92 -->

**Table 4.** Hyperparameter selection for each experiment in Q1 to Q3. Selected hyperparameters

are highlighted, with the tuned ones shown in brackets.

Hyperparameter Q1 Q2 Q3

Learning rate {0.0001, 0.001, 0.01} {0.0001, 0.001, 0.01} {0.0001, 0.001, 0.01} Weight decay 0 0 0 Optimzier Adam Adam Adam

Number of steps 160000 160000 160000 Batch size 1 1 1 Edge weight (x) 50 50 50 Initial vertex value 0 0 0

Hidden dim. {32,64,128} {32,64,128} {32,64,128} Number of MPNN layers 2 2 2 Number of MLP layers 2 2 2 1st layer output dim. {8,16, 32} {8,16, 32} {8,16, 32} 2nd layer output dim. 1 1 1

**Table 5.** Runtime and memory Usage for each experiment in Section 6. The first value denotes

the runtime in minutes (m) and seconds (s) of each experiment, and the second value denotes the used VRAM in MB. All results were obtained on a single computing vertex with an Nvidia L40 GPU and 120GB of RAM. For each experiment, the longest runtime was considered, obtained from test datasets with 1024 vertices.

Dataset

Task ER-constdeg ER General

Q1 18m48s/606.33 27m20s/881.06 25m3s/891.55 Q2 12m3s/573.33 14m17s/571.28 24m44s/887.95 Q3 L1 -/- -/- 23m37s/887.94 Q3 L2 -/- -/- 24m16s/887.95 parameters with selected parameters highlighted. A constant learning rate was used without a specific scheduler. Furthermore, the Adam optimizer [52] was used across all experiments.

For size generalization and regularization experiments in Q1 and Q3, we used a two-layer MPNN as outlined in Section 4. For all experiments, we used the design outlined in the theory of Section 4. In addition, we set the update and aggregation functions to two-layer MLPs with a hidden dimension of 64. The first aggregation FNN uses minimum aggregation with an output dimension of 16, while the second layer reduces the output dimension to 1. All layers are randomly initialized via the uniform initialization provided by PyTorch [86].

Furthermore, we report the runtime and memory usage of our experiments in Table 5. We provide a PyTorch Geometric implementation for each model. All our experiments were executed on a system with 12 CPU cores, an Nvidia L40 GPU, and 120GB of memory.

Experimental protocol In all experiments, we use the Bellman–Ford state of the vertices and the edge weights from the graph construction as input to our model. Furthermore, the target is given by the result obtained from Bellman–Ford after K additional steps from the starting iteration. To calculate the training loss, a combined loss consisting of an ℓ1-loss Lemp and a regularization term Lreg is given:

L = Lemp + ηLreg.

Throughout Q1, this loss is used to train the model with the regularization outlined in Section 4. For η, a value of 0.1 is used across experiments. The test score, however, is computed slightly

<!-- Page 93 -->

differently. Given the precision hv of a vertex value after K additional Bellman–Ford steps and the underlying ground truth xv the test score is computed as follows:

Ltest = 1 |Gtest|

X v∈Gtest

|hv −xv|

(xv + 1).

Therefore, a lower test score implies better generalization by the model to the unseen test dataset.

For Q2, we use slightly modified training and test sets compared to Q1 and Q3. Since the more expressive MPNN architecture from Section 4 requires a marked starting vertex for Bellman–Ford, we remove this special label from the training and test data and only provide the Bellman–Ford initialization from the execution of the algorithm. Otherwise, the parameters and training/test data remain the same as in Q1.

Finally, in Q3, we consider the regularization term introduced in Section 4 and whether it improves performance over standard ℓ1 or ℓ2 regularization. To conduct the experiment, we select the ER and General datasets outlined in Section L for evaluating both regularization terms. To provide a fair comparison, both architectures were kept the same as in Q1 and executed with the same seeds across experiments.

Additional results To supplement the results for Q1, we present detailed results in Figure 7, highlighting similar test behavior across test graph sizes. Furthermore, we provide an additional training dataset containing both random graphs and the minimum-path graphs for the training outlined in Section 4. Moreover, we provide distributions of the weight matrices for Q1. We omit showing bias value distributions, as they converge to 0 across all FNN layers. In addition, the weight matrices for update MLP layers contain singular non-zero values, with most entries remaining zero during training. Similar results can be observed for the aggregation FNN layers. Furthermore, the singular non-zero weights converge to positive values across all layers, with a maximum of 1.5 observed in the aggregation FNN of the first MPNN layer. We observe similar behavior for ℓ1 and ℓ2 regularization, but not as pronounced as in Section L.

Since size generalization experiments in Q1 were conducted only for two Bellman–Ford steps, we aim to provide additional insights into predicting future Bellman–Ford steps. Using the setup from Q1, we predict three steps of Bellman–Ford instead of two. For this, we use the same MPNN as in Q1 and highlight the results obtained in Table 7. We note that a two-layer MPNN is not sufficient to learn to predict three steps of Bellman–Ford from scratch with the given training set from Q1. However, this aligns with theoretical results, indicating that at least one layer is needed for each step of Bellman–Ford to be sufficiently predicted.

Finally, Table 8 presents additional results for Q2, highlighting differences between training and test results arising from the increased expressivity of the 1-iWL-MPNN. As shown, the training loss and test score are significantly higher for Q2 than for the MPNN in Q1. This aligns empirical results with theoretical observations on the required expressivity for the SSSP problem, as seen in Proposition 6.

<!-- Page 94 -->

**Table 6.** Additional results for the ER-constdeg and ER dataset used for size generalization

in Q1. Results are outlined for the given MPNN from Q1, with the test dataset changed accordingly. A list of hyperparameters can be found under Q1 in Table 4.

vertices

Test Set (Test score ↓) 64 128 256 512

ER-constdeg 0.0035 ± 0.0002 0.0034 ± 0.0002 0.0033±0.0002 0.0031 ± 0.0002 0.0030 ± 0.0001 ER 0.0034 ± 0.0004 0.0033 ± 0.0006 0.0037 ± 0.0001 0.0038 ± 0.0002 0.0038 ± 0.0002 General 0.0032 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0003 0.0033 ± 0.0002

0 20000 40000 60000 80000 100000 120000 140000

0.0

0.2

0.4

0.6

0.8

Weight Value

2nd MLP update layer 2

0 20000 40000 60000 80000 100000 120000 140000

0.2

0.0

0.2

0.4

0.6

0.8

2nd MLP update layer 1

0 20000 40000 60000 80000 100000 120000 140000

0.0

0.5

1.0

Weight Value

2nd MLP aggr. layer 2

0 20000 40000 60000 80000 100000 120000 140000

0.5

0.0

0.5

1.0

2nd MLP aggr. layer 1

0 20000 40000 60000 80000 100000 120000 140000

0.25

0.00

0.25

0.50

0.75

Weight Value

1st MLP update layer 2

0 20000 40000 60000 80000 100000 120000 140000

0.25

0.00

0.25

0.50

0.75

1st MLP update layer 1

0 20000 40000 60000 80000 100000 120000 140000 Training Steps

0.0

0.5

1.0

1.5

Weight Value

1st MLP aggr. layer 2

0 20000 40000 60000 80000 100000 120000 140000 Training Steps

0.5

0.0

0.5

1st MLP aggr. layer 1

**Figure 6.** Weights associated with the two MPNN layers and the corresponding MLPs for Q1

with 1024 vertices in the test set. Bias values are not shown as they converge towards 0. 1st or 2nd denotes the MPNN layer, whereas layer 1 or 2 denotes the FNN layer.

**Table 7.** Results for the application of the 2-layer MPNN from Q1 to the prediction task of

three Bellman–Ford steps. Following the same protocol as for Q1, the vertex features are given by the vertex values at the initial Bellman–Ford state. The target is given by the Bellman–Ford state after three steps.

vertices

Test Set (Test score ↓) 64 128 256 512

General 1.5381 ± 0.0057 1.5030 ± 0.0043 1.0831 ± 0.0015 0.6433 ± 0.0015 0.5721 ± 0.0039

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 94](2026-ICML-which-algorithms-can-graph-neural-networks-learn/page-094-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 95 -->

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score Training error Regularization error Training loss

(a) Results with General test set for 64 vertices

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score Training error Regularization error Training loss

(b) Results with General test set for 128 vertices

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score Training error Regularization error Training loss

(c) Results with General test set for 256 vertices

**Figure 7.** Extended results on size generalization obtained in Q1 for the General dataset.

Each plot shows training error Lemp, training loss L, regularization loss ηLreg, and test score for each of the experiments. All plots are generated from the same seed and smoothed using Gaussian smoothing with σ = 1 (continued on next page).

<!-- Page 96 -->

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score Training error Regularization error Training loss

(d) Results with General test set for 512 vertices

0 20000 40000 60000 80000 100000 120000 140000 160000

#Steps

10 2

10 1

100

101

102

Test Score/Train Err.

min. Training loss (2)

Test score Training error Regularization error Training loss

(e) Results with General test set for 1024 vertices

**Table 8.** Additional results for Q2 with size generalization properties. The same setup as in

Q1 was used in Q2, without special vertex labeling, unlike Q1.

vertices - General

Task (Score ↓) 64 128 256 512

Q2 - Training 28.4869 ± 0.0015 28.4869 ± 0.0015 28.4869 ± 0.0015 28.4869 ± 0.0015 28.4869 ± 0.0015 Q2 - Test 0.8393 ± 0.0001 0.8414 ± 0.0008 0.8368 ± 0.0010 0.8306 ± 0.0006 0.8217 ± 0.0010

Q1 - Training 2.0544 ± 0.0151 2.0544 ± 0.0151 2.0544 ± 0.0151 2.0544 ± 0.0151 2.0544 ± 0.0151 Q1 - Test 0.0032 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0002 0.0033 ± 0.0003 0.0033 ± 0.0002
