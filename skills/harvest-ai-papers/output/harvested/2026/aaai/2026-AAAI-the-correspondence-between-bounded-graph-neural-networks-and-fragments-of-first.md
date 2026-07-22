---
title: "The Correspondence Between Bounded Graph Neural Networks and Fragments of First-Order Logic"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38987
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38987/42949
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# The Correspondence Between Bounded Graph Neural Networks and Fragments of First-Order Logic

<!-- Page 1 -->

The Correspondence Between Bounded Graph Neural Networks and Fragments of First-Order Logic

Bernardo Cuenca Grau1, Eva Feng1, Przemysław Andrzej Wał,ega2

## 1 Department of Computer Science, University of Oxford 2 School of Electronic Engineering and Computer Science, Queen Mary

University of London bernardo.grau@cs.ox.ac.uk, eva.feng@cs.ox.ac.uk, p.walega@qmul.ac.uk

## Abstract

Graph Neural Networks (GNNs) address two key challenges in applying deep learning to graph-structured data: they handle varying size input graphs and ensure invariance under graph isomorphism. While GNNs have demonstrated broad applicability, understanding their expressive power remains an important question. In this paper, we propose GNN architectures that correspond precisely to prominent fragments of first-order logic (FO), including various modal logics as well as more expressive two-variable fragments. To establish these results, we apply methods from finite model theory of firstorder and modal logics to the domain of graph representation learning. Our results provide a unifying framework for understanding the logical expressiveness of GNNs within FO.

Extended version — https://arxiv.org/abs/2505.08021

## Introduction

Learning on graphs or relational structures presents two fundamental challenges. First, neural networks require fixed size inputs, making them ill-suited for graphs of varying size. Second, predictions about graphs should not depend on how the graph is represented, i.e., they should be invariant under isomorphism (Hamilton 2020).

Graph Neural Networks (GNNs) (Gilmer et al. 2017) overcome these limitations by operating natively on graphstructured data, inherently handling variable sizes and ensuring representation invariance. The flagship aggregatecombine (AC) architecture can be viewed as a layered network operating over an input graph. Each node maintains a state (a real-valued vector) and, in each layer, a node’s state is updated based on its current state and that of its neighbours. This update mechanism is specified by an aggregation function that takes the current states of the neighbours and aggregates them into a vector, and a combination function that takes the aggregate value from the neighbours and the current state of the node and computes the updated state. Their aggregate-combine-readout (ACR) extension includes an additional readout function which aggregates states across all nodes in the graph, rather than just local neighbours (Barcel´o et al. 2020). GNNs have been widely applied. They drive recommendation systems (Ying

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

et al. 2018), predict molecular properties (Besharatifard and Vafaee 2024), enhance traffic navigation (Derrow-Pinion et al. 2021), interpret scenes in computer vision (Chen et al. 2022), and enable reasoning over incomplete knowledge graphs (Tena Cucala et al. 2022; Zhang and Chen 2018; Huang et al. 2024).

GNNs encompass many architectures and a central question is understanding their expressive power—i.e., the classes of functions they can compute. This has been addressed from multiple angles. Early works studied the discriminative power of GNNs: given two graphs, can a GNN from a given family yield distinct outputs for them? By design, no GNN can separate isomorphic graphs, but more subtly, certain non-isomorphic graphs may remain indistinguishable. In particular, if two graphs cannot be distinguished by the 1-dimensional Weisfeiler-Leman (WL) graph isomorphism test, then no GNN can differentiate them either (Morris et al. 2019; Xu et al. 2019). Generalised k-dimensional GNNs, which handle higher-order graph structures, have also been connected to the WL hierarchy of increasingly powerful isomorphism tests (Morris et al. 2019). Through the correspondence between WL and finite-variable logics (Cai, F¨urer, and Immerman 1992), the limitation extends to logical distinguishability.

The expressiveness of GNNs has also been studied through the lenses of database query languages. As node classifiers, GNNs compute a unary query—an isomorphisminvariant function mapping each graph and node to a truth value. For a family of GNN classifiers, what is the logic expressing these unary queries? This is the logical expressiveness (or uniform expressiveness) of GNNs. The expressiveness of GNNs goes beyond first-order logic (FO) since aggregation can only be captured using extensions such as counting terms (Grohe 2024; Huang et al. 2023), Presburger quantifiers (Benedikt et al. 2024), or linear programming (Nunn et al. 2024). Other GNN variants, such as recursive GNNs (Ahvonen et al. 2024; Pflueger, Cucala, and Kostylev 2024) require fixpoint operators. A connection between GNNs and FO fragments has also been established (Barcel´o et al. 2020). Graded modal logic (GML) formulas, a.k.a. concepts in the description logic ALCQ (Baader et al. 2003), can be captured by GNNs without readout functions, just as FO formulas with two variables and counting quantifiers (C2) can be realised by a

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19135

<!-- Page 2 -->

FO

GNNAC+ b ≡C2

GNNAC+ s

≡

FO2

GNNACR b

≡

GMLC GNNAC b

≡

GML

GNNACR s

≡

ML(E)

GNNAC s

≡

ML

**Figure 1.** The landscape of our expressive power results

GNNs with readouts. This relationship is, however, asymmetric: while any GML classifier can be expressed by an AC GNN, the converse requires an assumption of FO expressibility, and in the case of case of ACR GNNs and C2 the converse does not hold even with this assumption (Hauke and Wał,ega 2025). The conditions ensuring FO expressibility of a GNN remain largely unexplored: the only sufficient condition known to us is that monotonic GNNs with max aggregation precisely match unions of tree-shaped conjunctive queries (Tena Cucala et al. 2023).

Contributions We introduce bounded GNNs with kbounded aggregation, where multiplicities greater than k in a multiset are capped at k. If k = 1, the multiplicities do not matter, and we speak of set-based aggregation. As we show, bounded GNNs correspond to modal and two-variable FO fragments as depicted in Figure 1.

We first establish that AC GNNs with set-based aggregation (GNNAC s) correspond to basic modal logic (ML) and thus to concepts in the description logic ALC. This extends to GNNs using bounded aggregation (GNNAC b), which correspond to graded modal logic (GML), that is, concepts of ALCQ. Readouts enable global quantification: GNNs with set-based aggregation and readout (GNNACR s) capture modal logic with the global modality (ML(E)), which corresponds to ALC with the universal role (Baader et al. 2003), while those with bounded aggregation and readouts (GNNACR b) match graded modal logic with counting (GMLC), which corresponds to ALCQ equipped with the universal role. While bounded readouts enable global quantification, they cannot express certain first-order properties like “nodes with exactly k non-neighbours”. To overcome this limitation, we introduce GNNAC+ b: a family of bounded GNNs augmented with an aggregation function over non-neighbours. We prove that GNNAC+ b captures C2 (two-variable FO with counting), while its set-based variant GNNAC+ s corresponds to the twovariable FO fragment FO2.

Graphs and Classifiers Graphs We consider (finite, undirected, simple, and nodelabelled) graphs G = (V, E, λ), where V is a finite set of nodes, E a set of undirected edges with no self-loops, and λ: V →{0, 1}d assigns to each node a binary vector1 of dimension d. The dimension d of all vectors in G is the same, and we refer to it as the dimension of G. A pointed graph is a pair (G, v) of a graph and one of its nodes. Node Classifiers A node classifier is a function mapping pointed graphs to true or false. The classifier accepts the input if it returns true and it rejects if it returns false. Two classifiers are equivalent if they compute the same function. A family F of classifiers is at most as expressive as F′, written F ≤F′, if each classifier in F has an equivalent one in F′. If F ≤F′ and F′ ≤F, we write F ≡F′, and say that F and F′ have the same expressiveness. Such uniform expressiveness contrasts with other notions such as discriminative power (Morris et al. 2019; Wang and Zhang 2022) and non-uniform expressiveness (Grohe 2024). GNN Classifiers We consider standard GNNs with aggregate-combine (AC) and aggregate-combine-readout (ACR) layers (Benedikt et al. 2024; Barcel´o et al. 2020), and propose also extended aggregate-combine (AC+) layers equipped with one aggregation over neighbours and another over non-neighbours. An AC layer is a pair (agg, comb), an ACR layer is a triple (agg, comb, read) and an AC+ layer is a triple (agg, agg, comb), where agg and agg are aggregation functions and read is a readout function, all mapping multisets of vectors into single vectors, whereas comb is a combination function mapping vectors to vectors. An application of a layer to a graph G = (V, E, λ) yields a graph G′ = (V, E, λ′) with the same nodes and edges, but with an updated labelling function λ′. For an AC layer, vector λ′(v) is defined as follows for each node v, where NG(v) = {w | {u, w} ∈E} is the set of neighbours of v and N G(v) = {w | {u, w}̸ ∈E}\{v} is the set of nonneighbours of v excluding v itself (note that the graphs we consider have no self loops).

comb λ(v), agg({|λ(w)|}w∈NG(v))

. (1)

For an ACR layer, vector λ′(v) is defined as comb λ(v),agg({|λ(w)|}w∈NG(v)), read({|λ(w)|}w∈V)

.

(2)

In turn, for an AC+ layer, vector λ′(v) is defined as comb λ(v),agg({|λ(w)|}w∈NG(v)), agg({|λ(w)|}w∈N G(v))

.

(3)

Each agg, agg, comb, and read has domain and range of some fixed dimension (but each can have a different dimension), which we refer to as input and output dimensions. For

1The assumption that node labels are binary, i.e., nodes are coloured, is standard when studying logical characterisation of GNNs (Barcel´o et al. 2020; Benedikt et al. 2024; Nunn et al. 2024)

19136

<!-- Page 3 -->

layer application to be meaningful, these dimensions need to match: if in an AC layer agg has input dimension d and output dimension d′, then the input dimension of comb is d + d′; in an ACR layer, if agg has dimensions d and d′, and read has dimensions d and d′′ (note that input dimensions of agg and read need to match), the input dimension of comb is d + d′ + d′′; if in an AC+ layer, agg has input dimension d and output dimension d′, and agg has dimensions d and d′′, then the input dimension of comb is d + d′ + d′′. A GNN classifier N of dimension d consists of L layers and a classification function cls from vectors to truth values. The input dimension of the first layer is d and consecutive layers have matching dimensions: the output dimension of layer i matches the input dimension of layer i + 1. We write λ(v)(ℓ) for the vector of node v upon application of layer ℓ; λ(v)(0) is the initial label of v, and λ(v)(L) is its final label. The application of N to (G, v) is the truth value N(G, v) = cls(λ(v)(L)).

Logic Classifiers We consider formulas over finite signatures consisting of a set PROP of propositions (unary predicates) p1, p2,... for node colours. Formulas of the graded modal logic of counting (GMLC) are defined as follows:

φ:= p | ¬φ | φ ∧φ | ♢kφ | ∃kφ, where p ∈PROP and, for each k ∈N, ♢k and ∃k are the k-graded modality and the k-counting modality, respectively. The formula ♢kφ expresses that at least k accessible worlds satisfy φ, while ∃kφ states that at least k worlds in total satisfy φ. Graded modal logic (GML) is obtained from GMLC by disallowing counting modalities. Modal logic with the global modality (ML(E)) is obtained from GMLC by restricting both counting and graded modalities to k = 1. Basic modal logic (ML) further restricts ML(E) by disallowing counting modalities entirely. We also consider the two-variable fragment of first-order logic with counting quantifiers (C2), where ∃k denotes counting quantifiers.2 The classical two-variable fragment (FO2) is obtained from C2 by restricting counting quantifiers to k = 1.

The depth of formula φ the maximum nesting of modal operators (♢k and ∃k) or quantifiers in it. The counting rank, rk#(φ), is the maximal among numbers k occurring in its graded and counting modalities (♢k and ∃k) or in counting quantifiers, or 0 if the formula does not mention any modalities or quantifiers. For L any of the logics defined above, we denote as Lℓ,c the set of all L formulas of depth at most ℓ and counting rank at most c.

Formulas are evaluated over pointed models (MG, v), each corresponding to a pair of a (coloured) graph G = (V, E, λ) of some dimension d and a node v ∈V. In the case of modal logics, model MG = (V, E, ν) has V as the set of modal worlds, E as the symmetric accessibility relation, and the valuation function ν maps each pi ∈PROP to the subset of nodes in V whose vectors have 1 on the i-th

2We use the symbols ∃k for both counting quantifiers and counting modalities.

position. Valuation ν extends to all modal formulas:

ν(¬φ):= V \ ν(φ), ν(φ1 ∧φ2):= ν(φ1) ∩ν(φ2), ν(♢kφ):= {v | k ≤|{w | {v, w} ∈E and w ∈ν(φ)}|}, ν(∃kφ):= V if k ≤|ν(φ)|, and ∅otherwise.

A pointed model (M, v), satisfies a formula φ, denoted (M, v) |= φ, if v ∈ν(φ). In the case of C2 formulas, we treat MG as the corresponding FO structure, and evaluate formulas using the standard FO semantics.

For a logic L, we write (M, w) ≡L (M′, w′) if (M, w) and (M′, w′) satisfy the same formulas of L. A logic classifier of dimension d is a formula φ with at most d propositions (unary predicates) p1,..., pd. The application of φ to (G, v) is true if (MG, v) |= φ and false otherwise. By convention, we use the same symbol for a logic and its associated classifier family.

Bounded GNN Classifiers We next introduce bounded GNNs, which generalise max GNNs (Tena Cucala and Cuenca Grau 2024) and max-sum GNNs (Tena Cucala et al. 2023). Bounded GNNs restrict aggregation and readout by requiring existence of a bound k such that all multiplicities k′ > k in an input multiset are replaced with k. Thus, multiplicities greater than k do not affect the output of a k-bounded function. Set-based functions ignore multiplicities altogether.

Definition 1. An aggregation (or readout) function f is kbounded, for k ∈N, if f(M) = f(Mk) for each multiset M in the domain of f, where Mk is the multiset obtained from M by replacing all multiplicities greater than k with k. Function f is set-based if it is 1-bounded, and it is bounded if it is k-bounded for some k ∈N.

Example 2. Consider the example functions below.

• The aggregation in max GNNs (Tena Cucala and Cuenca Grau 2024) is set-based. It maps a multiset of vectors to a vector being their componentwise maximum, for instance {|(3, 2), (2, 4), (2, 4)|} 7→(3, 4). • The aggregation in max-k-sum GNNs (Tena Cucala et al. 2023) is k-bounded. It maps M to a vector whose ith component is the sum of the k largest ith components in M; if k = 2, {|(3, 2), (2, 4), (2, 4)|} 7→(5, 8). • Examples of unbounded functions include componentwise sum {|(3, 2), (2, 4), (2, 4)|} 7→(7, 10) and the average mapping {|(3, 2), (2, 4), (2, 4)|} 7→(7

3, 10 3).

Equipped with the notion of bounded aggregation and readout functions, we are ready to define bounded GNNs.

Definition 3. We consider families of GNN classifiers, GNNY

X, where X ∈{s, b, m} indicates the type of aggregation and readout: set-based (s), bounded (b), or arbitrary— also called multiset—(m), whereas Y ∈{AC, ACR, AC+} indicates whether the GNN uses only AC, ACR, or AC+ layers. Bounded GNN classifiers are those with bounded aggregation and readout functions.

All GNNY

X classifiers, with X ∈{s, b}, are bounded. Family GNNAC m corresponds to aggregate-combine GNNs,

19137

<!-- Page 4 -->

GNNACR m to aggregate-combine-readout GNNs (Barcel´o et al. 2020), GNNAC b contains monotonic max-sum GNNs (Tena Cucala et al. 2023), and GNNAC s contains max GNNs (Tena Cucala and Cuenca Grau 2024).

As shown later, the expressiveness of bounded GNN classifiers falls within FO. This is intuitively so, because bounded GNNs have finite spectra, as defined below. Definition 4. (Benedikt et al. 2024) The spectrum, sp(N), of a GNN classifier N (of dimension d), is the set of all vectors that can occur as node labels in any layer of N application (to graphs of dimension d). For L the number of layers of N and ℓ≤L, we let sp(N, ℓ) be the subset of the spectrum consisting of the vectors that can occur upon application of layer ℓ. By convention, we let sp(N, 0) be the set of Boolean vectors of the classifier’s dimension.

Since sp(N, 0) is always finite and bounded functions applied to multisets with a bounded number of vectors yield finitely many possible outcomes, the spectra of bounded GNN classifiers are bounded. Using combinatorial arguments we can obtain explicit bounds as below. Proposition 5. Each bounded GNN classifier N has a finite spectrum. In particular, if N has dimension d, L layers, and k is the largest bound of its aggregation and readout functions, then |sp(N, 0)| = 2d and |sp(N, ℓ+ 1)|, for each 0 ≤ℓ≤L −1, is bounded by the following values:

|sp(N, ℓ)| · (k + 1)|sp(N,ℓ)|, if N ∈GNNAC b,

|sp(N, ℓ)| · (k + 1)2|sp(N,ℓ)|, if N ∈{GNNACR b, GNNAC+ b }.

Overview and Technical Approach In what follows, we systematically establish the correspondences between bounded GNNs and logic classifiers depicted in Figure 1. In Section 5, we show that bounded aggregate-combine GNNs correspond precisely to the modal logics without global counting (ML and GML). Next, in Section 6, we show that bounded aggregate-combinereadout GNNs capture the expressive power of modal logics with global counting (ML(E) and GMLC). Finally, in Section 7, we prove that extended aggregate-combine GNNs are equivalent in expressive power to two-variable logics (C2 and FO2).

To characterise a family of GNN classifiers F via a logic L we establish a bidirectional correspondence. We first show that every formula of L can be simulated by a GNN in F. We then show the converse: every GNN classifier in F admits an equivalent L-classifier.

The second step builds on finite model theory characterisations of L-equivalence through model comparison games (independent of GNNs). The existence of a winning strategy induces an equivalence relation ∼on pointed models, which extends to pointed coloured graphs: (G, v) ∼(G′, v′) holds precisely when (MG, v) ∼(MG′, v′). By limiting games to a fixed number of rounds and bounded grading, and by considering finite signatures, we ensure that ∼-invariant classes of models can be represented as a finite disjunction of characteristic formulas of L (Otto 2019; Libkin 2004). Specifically, for modal logics and two-variable fragments we use suitable variants of bisimulation and 2-pebble games, respectively.

The final requirement to establish the connection to GNNs is to show that each GNN classifier N in F is invariant under ∼, i.e., (G1, v1) ∼(G2, v2) implies N(G1, v1) = N(G2, v2), for all pointed graphs (G1, v1) and (G2, v2).

## 5 Modal Logics Without Global Counting

We first study bounded aggregate-combine GNNs, and start by showing that GML and ML formulas can be captured by GNNAC b and GNNAC s classifiers, respectively. For this, we adapt the construction simulating GML formulas with GNNs which uses unbounded summation (Barcel´o et al. 2020). For GML, our GNN construction uses max-k-sum aggregation, and for ML it uses max aggregation (which coincides with max-k-sum, for k = 1).

Theorem 6. GML ≤GNNAC b and ML ≤GNNAC s.

Proof Sketch. Let φ ∈GML be a logic classifier of dimension d with subformulas φ1,..., φL, such that k ≤ℓ if φk is a subformula of φℓ. We construct Nφ with layers 0,..., L and a classification function that maps a vector to true iff its last element is 1. Layer 0 multiplies input vectors by a matrix D ∈Rd×L, namely λ(v)(1) = λ(v)(0)D, where Dkℓ= 1 if the kth position of the input vectors corresponds to a proposition φℓ; other entries of D are 0. All other layers are AC layers of dimension L using max-nsum, for n the counting rank of φ. The combination function is comb(x, y) = σ(xC + yA + b), where σ(x) = min(max(0, x), 1) is the truncated ReLU and where entries of matrices A, C ∈RL×L and bias vector b ∈RL depend on the subformulas of φ as follows: (i) if φℓis a proposition, Cℓℓ= 1, (ii) if φℓ= φj ∧φk, then Cjℓ= Ckℓ= 1 and bℓ= −1; (iii) if φℓ= ¬φk, then Ckℓ= −1 and bℓ= 1, and (iv) if φℓ= ♢cφk, then Akℓ= 1 and bℓ= −c + 1. All other entries are zero. Note that if φ ∈ML, then Nφ ∈GNNAC s, as required.

We next show that every classifier in GNNAC b admits an equivalent GML classifier whereas each GNNAC s classifier admits an equivalent ML classifier. To this end, we first discuss the game-theoretic characterisations of logical indistinguishability for GML and ML.

The ℓ-round c-graded bisimulation game (Otto 2019) is played by Spoiler (him) and Duplicator (her) on finite pointed models (M, v) and (M′, v′). A configuration is a tuple (M, w, M′, w′), stating that one pebble is placed on world w in M, and the other on w′ in M′. The initial configuration is (M, v, M′, v′). Each round proceeds in the following two steps, leading to the next configuration. (1) Spoiler selects a pebble and a set U1̸ = ∅of at most c neighbours of the world marked by this pebble. Duplicator responds with a set U2 of neighbours of the world marked by the other pebble, such that |U1| = |U2|. (2) Spoiler selects a world in U2 and Duplicator responds with a world in U1. If a player cannot pick an appropriate set (U1 or U2), they lose. If in some configuration worlds marked by pebbles do not satisfy the same propositions, Duplicator loses. Hence, Duplicator wins

19138

<!-- Page 5 -->

if she has responses for all ℓmoves of Spoiler, or if Spoiler cannot make a move in some round. Spoiler wins if Duplicator loses. We write (M, v) ∼ℓ,c (M′, v′) if Duplicator has a winning strategy starting from configuration (M, v, M′, v′). Importantly, ∼ℓ,c determines indistinguishability of pointed models in GMLℓ,c and any class of pointed models closed under ∼ℓ,c is definable by a GMLℓ,c formula. Theorem 7. (Otto 2019) For any pointed models (M, v) and (M′, v′), and any ℓ, c ∈N: (M, v) ∼ℓ,c (M′, v′) iff (M, v) ≡GMLℓ,c (M′, v′) iff (M′, v′) |= φℓ,c

[M,v].

Here, the characteristic formula φℓ,c

[M,v] is defined inductively on n ≥0 as follows, for p ∈PROP and U n v,w the set of worlds u such that {v, u} ∈E and (M, u) ∼n,c (M, w).

φ0,c

[M,v]:=

^

{p: (M, v) |= p} ∧

^

{¬p: (M, v)̸ |= p}, φn+1,c

[M,v]:= φ0,c

[M,v] ∧ ^

♢kφn,c [M,w]: {v, w} ∈E, k ≤min(|U n v,w|, c)

∧ ^

¬♢kφn,c

[M,w]: {v, w} ∈E and |U n v,w| < k ≤c

∧

¬♢1

^

{v,w}∈E

¬φn,c

[M,w].

Moreover, any ∼ℓ,c-closed class C of pointed models is definable by the formula W

(M,v)∈C φℓ,c

[M,v].

We note two important observations regarding Theorem 7. First, our construction of characteristic formulas corrects an error of Otto (2019), by including a final conjunct that is necessary for the theorem to hold. Second, we observe that the ℓ-round 1-graded bisimulation games coincide with ℓ-round bisimulation games for ML (Goranko and Otto 2007), and that the characteristic formulas φℓ,1

[M,v] are characteristic formulas of ML.

We can now shift our attention to GNNs and show that classifiers in GNNAC b and GNNAC s are invariant under the bisimulation games for GML and ML, respectively. Theorem 8. The following hold:

1. GNNAC b classifiers with L layers and k-bounded aggregation are ∼L,k-invariant; 2. GNNAC s classifiers with L layers are ∼L,1-invariant.

Proof Sketch. We show by induction on ℓ≤L that, for any pointed graphs satisfying (G1, v1) ∼ℓ,k (G2, v2), the execution of a k-bounded GNN N ∈GNNAC b satisfies λ1(v1)(ℓ) = λ2(v2)(ℓ), and thus N(G1, v1) = N(G2, v2).

If ℓ= 0, (G1, v1) ∼0,k (G2, v2) implies that v1 and v2 satisfy the same propositions, so λ1(v1)(0) = λ2(v2)(0). For ℓ≥1, (G1, v1) ∼ℓ,k (G2, v2) implies (G1, v1) ∼ℓ−1,k (G2, v2), so λ1(v1)(ℓ−1) = λ2(v2)(ℓ−1) by induction. It remains to show that agg({|λ1(w)(ℓ−1)|}w∈NG1(v1)) equals agg({|λ2(w)(ℓ−1)|}w∈NG2(v2)), which subsequently implies λ1(v1)(ℓ) = λ2(v2)(ℓ) by Equation (1). Suppose for the sake of contradiction, and without loss of generality, that there is a neighbour w2 of v2 such that λ2(w2)(ℓ−1) occurs k2 < k times in {|λ2(w)(ℓ−1)|}w∈NG2(v2) and k1 > k2 times in

{|λ(ℓ−1)

1 (w)|}w∈NG1(v1). The strategy for Spoiler is to select a set U1 of min(k, k1) elements of w ∈NG1(v1) satisfying λ1(w)(ℓ−1) = λ1(w1)(ℓ−1). Duplicator must respond with a subset U2 of neighbours of v2 in G2 of the same cardinality. Any such U2 must contain w2 such that λ2(w2)(ℓ−1)̸ = λ1(w1)(ℓ−1). In the second part of the round, Spoiler chooses w2; then, whichever element w′

1 in U1 Duplicator chooses, we have λ1(w′

1)(ℓ−1)̸ = λ(ℓ−1) 2 (w2). Hence, by the inductive hypothesis, (G1, w′

1)̸ ∼ℓ−1,k (G2, w2) and hence (G1, v1)̸ ∼ℓ,k (G2, v2), raising a contradiction. The proof for N ∈GNNAC s is a particular case, where k = 1.

By Theorem 7, invariance under bisimulation games implies that graphs accepted by a GNN can be characterised by a disjunction of characteristic formulas.

Corollary 9. Let N be a GNN with L layers and C the pointed models (M, v) accepted by N. If N ∈GNNAC b with k-bounded aggregations, it is equivalent to the GML formula W

(M,v)∈C φL,k

[M,v]. If N ∈GNNAC s, it is equivalent to the ML formula W

(M,v)∈C φL,1

[M,v].

Therefore, GML ≥GNNAC b and ML ≥GNNAC s. By combining these results with Theorem 6 we obtain the following exact correspondence.

Corollary 10. GML ≡GNNAC b and ML ≡GNNAC s.

## 6 Modal Logics with Global Counting

We now consider bounded GNNs with readouts. We first show that GMLC is captured by GNNACR b using max-k-sum as aggregation, whereas ML(E) is captured by GNNACR s using componentwise maximum aggregation.

Theorem 11. GMLC ≤GNNACR b and ML(E)≤GNNACR s.

Proof Sketch. Let φ ∈GMLC; we will construct a GNN by modifying the construction from the proof of Theorem 6. We now use ACR layers with comb(x, y, z) = σ(xC + yA + zR+b), where R simulates global modalities. In particular, for subformulas φℓ= ∃cφk, we set Rkℓ= 1 and bℓ= −c + 1, whereas other entries are set to zeros. Moreover, we let read (and agg) be the max-n-sum function where n is the counting rank of φ. The remaining components are as in the proof of Theorem 6. The construction for ML(E) is obtained as a particular case by taking c = 1 and noting the max-1-sum function corresponds to max aggregation.

We next show that GNNACR b and GNNACR s classifiers admit equivalent GMLC and ML(E) classifiers, respectively. As a first step, our approach involves developing a new game-theoretic characterisation of GMLC that naturally covers ML(E) as a special case.

To this end, we introduce ℓ-round c-graded global bisimulation games, by extending the games from Section 5. In each round, Spoiler can now choose to play either a standard (local) round as before, or a global round. Each global round proceeds by Spoiler selecting a non-empty set U1 of worlds

19139

<!-- Page 6 -->

of size bounded by c in one of the models, and Duplicator subsequently picking a set U2 of worlds of the same size in the other model; Spoiler then places a pebble in a world u in U2 and Duplicator responds by placing a pebble on a world u′ in U1, leading to a new configuration (M, u, M′, u′). We write (M, v) ∼∃ ℓ,c (M′, v′) if Duplicator has a winning strategy in the ℓ-round c-graded global bisimulation game starting at (M, v, M′, v′). Similarly as in the case of non-global games (Theorem 7), we can show the following characterisation result.

Theorem 12. For any pointed models (M, v) and (M′, v′) and ℓ, c ∈N, (M, v) ∼∃ ℓ,c (M′, v′) iff (M, v) ≡GMLCℓ,c (M′, v′) iff (M′, v′) |= φℓ,c

∃[M,v]. Here, the characteristic formulas are defined inductively on n ≥0 as follow, where U n v,w is the set of all u with {v, u} ∈E and (M, u) ∼∃ n,c (M, w), and Jn w is the set of all u ∈V with (M, u) ∼∃ n,c (M, w).

φ0,c

∃[M,v]:=

^

{p: (M, v) |= p} ∧

^

{¬p: (M, v)̸ |= p}, φn+1,c

∃[M,v]:= φ0,c

∃[M,v] ∧ ^

♢kφn,c ∃[M,w]: {v, w} ∈E, k ≤min(|U n v,w|, c)

∧ ^

¬♢kφn,c

∃[M,w]: {v, w} ∈E and |U n v,w| < k ≤c

∧ ^

∃kφn,c

∃[M,w]: w ∈V, k ≤|Jn w|, and k ≤c

∧ ^

{¬∃kφn,c

∃[M,w]: w ∈V and |Jn w| < k ≤c

∧

¬♢1

^

{v,w}∈E

¬φn,c

∃[M,w] ∧¬∃1

^ w∈V

¬φn,c

∃[M,w].

Moreover, any class C of pointed models closed under ∼∃ ℓ,c is definable by W

(M,v)∈C φℓ,c

∃[M,v].

We can observe that if c = 1, then characteristic formulas are in ML(E), and our games correspond to global bisimulation games developed for ML(E) (Goranko and Otto 2007, Section 5.1). We are now ready to show that classifiers in GNNACR b and GNNACR s are invariant under the bisimulation games for GMLC and ML(E), respectively.

Theorem 13. The following hold:

1. GNNACR b classifiers with L layers and k-bounded aggregations and readouts are ∼∃

L,k-invariant; 2. GNNACR s classifiers with L layers are ∼∃

L,1-invariant.

Proof Sketch. The proof has the same structure as in Theorem 8. The inductive hypothesis implies λ1(v1)(ℓ−1) = λ2(v2)(ℓ−1) and min(k, {|λ1(w)(ℓ−1)|}w∈NG1(v1))

equals min(k, {|λ2(w)(ℓ−1)|}w∈NG2(v2)). Addition- ally we can show now that read({|λ1(w)(ℓ−1)|}w∈V1) equals read({|λ2(w)(ℓ−1)|}w∈V2), which then implies that λ1(v1)(ℓ) = λ2(v2)(ℓ) by Equation (2). Indeed, if these multisets were not equal, Spoiler could find (w.l.o.g.) a node w2 ∈V2 such that λ2(w2)(ℓ−1) occurs k2 < k times in

{|λ2(w)(ℓ−1)|}w∈V2 and k1 > k2 times in {|λ(ℓ−1)

1 (w)|}w∈V1. This would allow Spoiler to play a global round that wins the game.

The proof for the set-based case can again be obtained as a particular case, with c = 1.

As before, Theorems 12 and 13 imply the following. Corollary 14. Let N be a GNN with L layers and C the pointed models (M, v) accepted by N. If N ∈GNNACR b with k-bounded aggregations, it is equivalent to the GMLC formula W

(M,v)∈C φL,k

∃[M,v]. If N ∈GNNACR s, it is equivalent to the ML(E) formula W

(M,v)∈C φL,1

∃[M,v].

Therefore, GMLC ≥GNNACR b and ML(E) ≥GNNACR s. Combining these with Theorem 11 we have the following. Corollary 15. The following equivalences hold: GMLC ≡ GNNACR b and ML(E) ≡GNNACR s.

## 7 Two-Variable Fragments

Finally, we consider bounded GNNs with non-neighbour aggregation. We show that GNNAC+ b and GNNAC+ s exactly correspond to C2 and FO2, respectively.

We first show that each C2 classifier can be expressed in GNNAC+ b using max-k-sum for neighbour and nonneighbour aggregations, whereas each FO2 classifier can be expressed in GNNAC+ s using componentwise max.

Theorem 16. C2 ≤GNNAC+ b and FO2 ≤GNNAC+ s.

Proof Sketch. Similarly to Barcel´o et al. (2020), we exploit the fact that C2 has the same expressive power as the modal logic EMLC with complex modalities (Lutz, Sattler, and Wolter 2001, Theorem 1). We can show that EMLC classifiers in normal form (Barcel´o et al. 2020, Lemma D.4) can be captured by GNNAC+ b. The construction is similar to that of Theorem 6, but using AC+ layers. We use max-n-sum aggregations where n is the counting rank of the EMLC formula. Then, comb(x, y, z) = σ(xC + yA + zA + b), with matrix and vector entries depending on the subformulas φℓ. If φℓis a proposition, conjunction, or negation, the ℓth columns of A, C, and b are as in Theorem 6, and the ℓth column of A has only 0s. For the remaining cases, the ℓth columns of A, C, A, and b are defined as in the construction of (Barcel´o et al. 2020, Theorem 5.1), except that we use combinations of bounded neighbour and non-neighbour aggregation instead of combinations of unbounded aggregation and global readouts. The proof for FO2 is a particular case, where operators in EMLC can count up to 1.

Games for two-variable logics (Libkin 2004) are similar to bisimulation games, but they are now played with two pairs of pebbles. In what follows we define a variant of the game for C2 (Gr¨adel and Otto 1999), obtained by imposing restrictions on both the number of rounds and on the possible counting. We let the 2-pebble ℓ-round c-graded game be played on two models M and M′ by Spoiler and Duplicator with two pairs of pebbles: (p1

M, p1

M′) and (p2

M, p2

M′). After each round, the pebble positions define a mapping π of two

19140

<!-- Page 7 -->

elements in M into two elements of M′. Duplicator has a winning strategy if she can ensure that, after each round, π is a partial isomorphism between the models. For node classification, we consider games in which the starting configuration has p1

M and p1

M′ placed on some elements of M and M′, respectively. Each round is played as follows: (1) Spoiler chooses a model (say, M), one of pebble pairs i ∈{1, 2}, and a non-empty subset U ⊆V with |U| ≤c. Duplicator responds with a subset U ′ ⊆V ′ such that |U ′| = |U|. (2) Spoiler places pebble pi

M′ on some u′ ∈U ′. Duplicator responds by placing pi

M on some u ∈U. We write (M, a) ∼2 ℓ,c (M′, a′) if Duplicator has a winning strategy when p1

M and p1

M′ are initially placed on elements a and a′, respectively.

As we establish next, this game variant characterises indistinguishability in the logic C2 ℓ,c. What is crucial is that we consider both bounded depth and counting rank. As a result, formulas of C2 ℓ,c have finitely many equivalence classes (with respect to the logical equivalence), and so, any class of models closed under the equivalence in C2 ℓ,c is definable by a (finite) C2 ℓ,c formula.

Theorem 17. For any pointed models (M, a) and (M′, a′) and any ℓ, c ∈N: (M, a) ∼2 ℓ,c (M′, a′) iff a in M and a′ in M′ satisfy the same C2 ℓ,c formulas with one free variable. Furthermore, any class C of pointed models closed under ∼2 ℓ,c is definable by a C2 ℓ,c formula.

Proof Sketch. To show the equivalence, we prove a stronger result, where a and a′ are vectors of length at most 2. We show each implication by induction on ℓ. For the forward implication, we show the contrapositive, namely that M |= φ(a) and M′̸ |= φ(a′), imply the existence of a winning strategy for Spoiler. For the opposite direction, we show that whenever M |= φ(a) iff M′ |= φ(a′), there is a winning strategy for Duplicator.

The above shows that (M, a) ∼2 ℓ,c (M′, a′) iff a in M and a′ in M′ satisfy the same C2 ℓ,c formulas with one free variable. Since, up to logical equivalence, there are finitely many C2 ℓ,c formulas (Cai, F¨urer, and Immerman 1992, Lemma 4.4), each ∼2 ℓ,c equivalence class can be expressed as a (finite) disjunction of (finite) C2 ℓ,c formulas.

Next, we show that bounded GNNs with non-neighbour aggregation are invariant under our variant of the 2-pebble games.

Theorem 18. The following hold:

1. GNNAC+ b classifiers with L layers and k-bounded aggregations and readout are ∼2

L,k-invariant;

2. GNNAC+ s classifiers with L layers are ∼2

L,1-invariant.

Proof Sketch. The structure of the proof follows that of Theorem 8, but now games use two pairs of pebbles and GNNs have AC+ layers—with two types of aggregation. The important part of the proof is in the inductive step, where we show that (G1, v1) ∼2 ℓ,k (G2, v2) implies that min(k, {|λ1(w)(ℓ−1)|}w∈XG1(v1))

equals min(k, {|λ2(w)(ℓ−1)|}w∈XG2(v2)), for both X ∈

{N, N}. Towards a contradiction suppose that there is u ∈ XG1(v1) such that λ1(u)(ℓ−1) appears k1 times in {|λ1(w)(ℓ−1)|}w∈XG1(v1) and k2 < k1 times in {|λ2(w)(ℓ−1)|}w∈XG2(v2), with k2 < k. The winning strategy for Spoiler is to pick a set U1 of min(k, k1) elements from {|λ1(w)(ℓ−1)|}w∈XG1(v1) with label λ1(u)(ℓ−1). This allows Spoiler to get to a configuration (MG, v1, u1, MG′, v2, u2) with λ1(u)(ℓ−1)̸ = λ2(u2)(ℓ−1) which, by the inductive hypothesis, implies (G1, v1)̸ ∼2 ℓ,k (G2, v2). The proof for the set-based case is a particular case, with k = 1.

As before, Theorem 17 implies the following.

Corollary 19. Let N be a GNN with L layers and C the pointed models (M, v) accepted by N. If N ∈GNNAC+ b it is equivalent to a C2 formula. If N ∈GNNAC+ s, it is equivalent to an FO2 formula.

Therefore, C2 ≥GNNAC+ b and FO2 ≥GNNAC+ s. Combining these with Theorem 16 we have the following.

Corollary 20. The following equivalences hold: C2 ≡ GNNAC+ b and FO2 ≡GNNAC+ s.

## 8 Conclusion and Future Work

We have introduced families of bounded GNNs, whose expressive power corresponds exactly to well-known modal logics and 2-variable first-order logics. Among others, we have showed that standard aggregate-combine GNNs with bounded aggregation have the same expressive power as the graded modal logic. This, together with the result of Barcel´o et al. (2020), implies that an aggregate-combine GNN classifier is FO-expressible if and only if it is equivalent to a bounded aggregate-combine GNN classifier. The correspondence between FO-expressibility and bounding aggregation (and readout) occurs as an interesting phenomenon to study. In particular, we find it interesting to determine for which classes of GNNs classifiers, FO-expressibility is equivalent to expressibility by bounded GNNs. Future work directions we consider include also establishing tight bounds on the size of logical formulas capturing GNNs and practical extraction of logical formulas from GNNs.

## Acknowledgements

Eva Feng is generously supported by a Google DeepMind Scholarship (CS2324 DeepMind 1594092).

## References

Ahvonen, V.; Heiman, D.; Kuusisto, A.; and Lutz, C. 2024. Logical characterizations of recurrent graph neural networks with reals and floats. In Globersons, A.; Mackey, L.; Belgrave, D.; Fan, A.; Paquet, U.; Tomczak, J. M.; and Zhang, C., eds., Proc. of NeurIPS. Baader, F.; Calvanese, D.; McGuinness, D. L.; Nardi, D.; and Patel-Schneider, P. F., eds. 2003. The Description

19141

<!-- Page 8 -->

Logic Handbook: Theory, Implementation, and Applications. Cambridge University Press. ISBN 0-521-78176-0. Barcel´o, P.; Kostylev, E. V.; Monet, M.; P´erez, J.; Reutter, J. L.; and Silva, J. P. 2020. The Logical Expressiveness of Graph Neural Networks. In Proc. of ICLR. Benedikt, M.; Lu, C.-H.; Motik, B.; and Tan, T. 2024. Decidability of Graph Neural Networks via Logical Characterizations. In Proc. of ICALP, volume 297, 127:1–127:20. Schloss Dagstuhl. Besharatifard, M.; and Vafaee, F. 2024. A review on graph neural networks for predicting synergistic drug combinations. Artif. Intell. Rev., 57(3): 49. Cai, J.-Y.; F¨urer, M.; and Immerman, N. 1992. An optimal lower bound on the number of variables for graph identification. Combinatorica, 12(4): 389–410. Chen, C.; Wu, Y.; Dai, Q.; Zhou, H.; Xu, M.; Yang, S.; Han, X.; and Yu, Y. 2022. A Survey on Graph Neural Networks and Graph Transformers in Computer Vision: A Task- Oriented Perspective. CoRR, abs/2209.13232. Derrow-Pinion, A.; She, J.; Wong, D.; Lange, O.; Hester, T.; Perez, L.; Nunkesser, M.; Lee, S.; Guo, X.; Wiltshire, B.; Battaglia, P. W.; Gupta, V.; Li, A.; Xu, Z.; Sanchez- Gonzalez, A.; Li, Y.; and Velickovic, P. 2021. ETA Prediction with Graph Neural Networks in Google Maps. In Proc. of CIKM, CIKM ’21, 3767–3776. ACM. Gilmer, J.; Schoenholz, S. S.; Riley, P. F.; Vinyals, O.; and Dahl, G. E. 2017. Neural Message Passing for Quantum Chemistry. In Proc. of ICML, volume 70, 1263–1272. Goranko, V.; and Otto, M. 2007. Model theory of modal logic. In Blackburn, P.; van Benthem, J. F. A. K.; and Wolter, F., eds., Handbook of Modal Logic, volume 3 of Studies in logic and practical reasoning, 249–329. North-Holland. Gr¨adel, E.; and Otto, M. 1999. On Logics with Two Variables. Theor. Comput. Sci., 224(1-2): 73–113. Grohe, M. 2024. The descriptive complexity of graph neural networks. TheoretiCS, 3. Hamilton, W. L. 2020. Graph Representation Learning. Synthesis Lectures on Artificial Intelligence and Machine Learning. Morgan & Claypool Publishers. ISBN 978-3-031- 00460-5. Hauke, S. P.; and Wał,ega, P. A. 2025. Aggregate-Combine- Readout GNNs Are More Expressive Than Logic C2. arXiv preprint arXiv:2508.06091. Huang, X.; Orth, M. A. R.; Barcel´o, P.; Bronstein, M. M.; and Ceylan, ˙I. ˙I. 2024. Link Prediction with Relational Hypergraphs. CoRR, abs/2402.04062. Huang, X.; Romero, M.; Ceylan, ˙I. ˙I.; and Barcel´o, P. 2023. A Theory of Link Prediction via Relational Weisfeiler- Leman on Knowledge Graphs. In Oh, A.; Naumann, T.; Globerson, A.; Saenko, K.; Hardt, M.; and Levine, S., eds., Proc. of NeurIPS. Libkin, L. 2004. Elements of Finite Model Theory. Texts in Theoretical Computer Science. An EATCS Series. Springer. Lutz, C.; Sattler, U.; and Wolter, F. 2001. Modal Logic and the Two-Variable Fragment. In Fribourg, L., ed., Proc. of

CSL, volume 2142 of Lecture Notes in Computer Science, 247–261. Springer. Morris, C.; Ritzert, M.; Fey, M.; Hamilton, W. L.; Lenssen, J. E.; Rattan, G.; and Grohe, M. 2019. Weisfeiler and leman go neural: Higher-order graph neural networks. In Proc. of AAAI, volume 33, 4602–4609. Nunn, P.; S¨alzer, M.; Schwarzentruber, F.; and Troquard, N. 2024. A Logic for Reasoning about Aggregate-Combine Graph Neural Networks. In Proc. of IJCAI, 3532–3540. ijcai.org. Otto, M. 2019. Graded modal logic and counting bisimulation. CoRR, abs/1910.00039. Pflueger, M.; Cucala, D. T.; and Kostylev, E. V. 2024. Recurrent Graph Neural Networks and Their Connections to Bisimulation and Logic. In Wooldridge, M. J.; Dy, J. G.; and Natarajan, S., eds., Proc. of AAAI, 14608–14616. AAAI Press. Tena Cucala, D.; Cuenca Grau, B.; Motik, B.; and Kostylev, E. V. 2023. On the Correspondence Between Monotonic Max-Sum GNNs and Datalog. In Marquis, P.; Son, T. C.; and Kern-Isberner, G., eds., Proc. of KR, 658–667. Tena Cucala, D. J.; and Cuenca Grau, B. 2024. Bridging Max Graph Neural Networks and Datalog with Negation. In Marquis, P.; Ortiz, M.; and Pagnucco, M., eds., Proc. of KR. Tena Cucala, D. J.; Cuenca Grau, B.; Kostylev, E. V.; and Motik, B. 2022. Explainable GNN-Based Models over Knowledge Graphs. In Proc. of ICLR. Wang, X.; and Zhang, M. 2022. How Powerful are Spectral Graph Neural Networks. In Proc. of ICML. Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2019. How Powerful are Graph Neural Networks? In Proc. of ICLR. Ying, R.; He, R.; Chen, K.; Eksombatchai, P.; Hamilton, W. L.; and Leskovec, J. 2018. Graph Convolutional Neural Networks for Web-Scale Recommender Systems. In Proc. of the 24th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD ’18, 974–983. ACM. Zhang, M.; and Chen, Y. 2018. Link Prediction Based on Graph Neural Networks. In Bengio, S.; Wallach, H. M.; Larochelle, H.; Grauman, K.; Cesa-Bianchi, N.; and Garnett, R., eds., Proc. of NeurIPS, 5171–5181.

19142
