---
title: "Tractable Weighted First-Order Model Counting with Bounded Treewidth Binary Evidence"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38994
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38994/42956
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Tractable Weighted First-Order Model Counting with Bounded Treewidth Binary Evidence

<!-- Page 1 -->

Tractable Weighted First-Order Model Counting with Bounded Treewidth Binary Evidence

V´aclav K˚ula1, Qipeng Kuang2, Yuyi Wang3, Yuanhong Wang4, Ondˇrej Kuˇzelka1

1Faculty of Electrical Engineering, Czech Technical University in Prague, Prague, Czech Republic 2The University of Hong Kong, Hong Kong, China 3CRRC Zhuzhou Institute, Zhuzhou, China 4Jilin University, Changchun, China kulavacl@fel.cvut.cz, kuangqipeng@connect.hku.hk, yuyiwang920@gmail.com, lucienwang@jlu.edu.cn, ondrej.kuzelka@fel.cvut.cz

## Abstract

The Weighted First-Order Model Counting Problem (WFOMC) asks to compute the weighted sum of models of a given first-order logic sentence over a given domain. Conditioning WFOMC on evidence—fixing the truth values of a set of ground literals—has been shown impossible in time polynomial in the domain size (unless #P ⊆FP) even for fragments of logic that are otherwise tractable for WFOMC without evidence. In this work, we address the barrier by restricting the binary evidence to the case where the underlying Gaifman graph has bounded treewidth. We present a polynomial-time algorithm in the domain size for computing WFOMC for the two-variable fragments FO2 and C2 conditioned on such binary evidence. Furthermore, we show the applicability of our algorithm in combinatorial problems by solving the stable seating arrangement problem on bounded-treewidth graphs of bounded degree, which was an open problem. We also conducted experiments to show the scalability of our algorithm compared to the existing model counting solvers.

Code — https://github.com/kulavacl/WFOMC---binary-evidence

## Introduction

The Weighted First-Order Model Counting Problem (WFOMC) asks to compute the weighted sum of models for a given first-order logic sentence over a specified domain, alongside a pair of weighting functions that assign a weight to each model of the sentence. WFOMC serves as a fundamental problem in Statistical Relational Learning (Getoor and Taskar 2007) where applications such as Markov Logic Networks (Van den Broeck 2011), parfactor graphs (Poole 2003), probabilistic logic programs (Van den Broeck, Meert, and Darwiche 2014) and probabilistic databases (Van den Broeck 2013) can be reduced to WFOMC. Recent work also reveals the potential of WFOMC to contribute to enumerative combinatorics by providing a general framework for encoding counting problems (Malhotra, Bizzaro, and Serafini 2025), integer sequences (Svatos et al. 2023), and computing graph polynomials on specific graphs (Kuang et al. 2024).

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

In WFOMC we usually measure the time complexity in terms of the domain size. The fragments enjoying polynomial time complexity in the domain size are called domainliftable (Van den Broeck 2011). Previous results have shown that the two-variable fragment (FO2) possibly with counting quantifiers (C2) and cardinality constraints is domainliftable (Van den Broeck 2011; Van den Broeck, Meert, and Darwiche 2014; Kuzelka 2021).

We consider the task of computing WFOMC for FO2 and C2 with evidence, the interpretation of certain predicates. For example, consider the sentence

Ψ = ∀x∀y: E(x, y) →(¬I(x) ∨¬I(y)) (1)

over the domain ∆ = {1, 2, 3, 4}. An evidence can be the specification that E(1, 2), E(1, 3), E(2, 3), E(1, 4) and their reverse atoms are true and other atoms of E are false. In this case, each model is an assignment of I(1), · · ·, I(4) satisfying Ψ, which represents an independent set of the graph with vertices {1, 2, 3, 4} and undirected edges (1, 2), (1, 3), (2, 3), (1, 4). The WFOMC of Ψ with the above evidence over ∆with unit weight for each model equals to the number of independent sets on the graph.

It has been shown that FO2 and C2 remain domain-liftable when conditioned on unary evidence (i.e., interpretation of unary predicates) (Van den Broeck and Davis 2012; Wang et al. 2024). In the contrary, conditioning on binary evidence (i.e., interpretation of binary predicates) is #P-hard, even for the universally quantified FO2 sentences (Van den Broeck and Davis 2012). An intuition of this phenomenon is that the binary evidence breaks the symmetry of domain elements. Without binary evidence, domain elements can be partitioned into a fixed number of classes, where elements within the same class are indistinguishable. For example, for the sentence in Eq. (1) conjuncted with ∀x: ¬E(x, x), elements can be classified based on whether I(x) holds. This symmetry is crucial for current algorithms computing WFOMC of domain-liftable fragments. Unary evidence does not break the symmetry of elements, as they can be eliminated using the technique proposed by Wang et al. (2024, Appendix A), allowing WFOMC to be computed on a first-order sentence without unary evidence.

Little progress has been made to deal with the binary evidence. Van den Broeck and Darwiche (2013) showed that

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19198

<!-- Page 2 -->

if the binary evidence can be represented by a binary matrix with low boolean rank, then a boolean matrix factorization (Miettinen 2009) transfers the binary evidence to unary evidence. However, as stated by the authors, real-world binary matrices are likely to have large boolean rank, thus the use of this approach is limited in reality.

## 1.1 Our Contributions

We propose an algorithm to compute WFOMC for an FO2 or C2 sentence with cardinality constraints, unary evidence and binary evidence whose Gaifman graph, the undirected graph with vertices corresponding to domain elements in which two vertices a and b are connected if and only if there is a binary predicate P such that the truth value of P(a, b) or P(b, a) is specified in the binary evidence, is of bounded treewidth. The algorithm runs in time polynomial in the domain size. This offers a new approach to overcome the symmetry limitation in lifted inference, and expands the expressive power and applicability of WFOMC. The key idea of our algorithm is the dynamic programming for computing WFOMC for the universally quantified FO2 sentence with evidence on the tree decomposition of the underlying Gaifman graph. Existing techniques help to extend the result to FO2 and C2 with cardinality constraints.

## Experiments

are conducted to test the performance of our algorithm compared to two existing model counters on two problems, the friends and smokers problem and the inference on Watts-Strogatz graphs. Results indicate the efficiency and scalability of our algorithm.

Finally, our approach applies to combinatorial problems on bounded treewidth graphs by solving an open problem (Berriaud, Constantinescu, and Wattenhofer 2023): the stable seating arrangement problem of fixed number of classes on graphs of bounded treewidth and bounded degree. We show that counting the number of stable seating arrangements in such case is in time polynomial in the number of agents. Remark 1.1. A similar result is Courcelle’s theorem (Courcelle 1990) which states that the model checking problem of monadic second order logic on a bounded treewidth graph is in polynomial time. We remark that our result and Courcelle’s theorem are incomparable. First, as Courcelle’s theorem works with monadic second order logic of graphs, it is required that the interpretation to all but unary predicates should be given. In contrast, we allow binary predicates to remain uninterpreted. Second, our result is restricted to the two-variable fragment, which is a necessary consequence of the negative result showing intractability of WFOMC for FO3 (Beame et al. 2015), while Courcelle’s theorem can involve arbitrary number of variables because it works in a different setting.

## Preliminaries

## 2.1 First-Order

Logic

We work with the function-free fragments of first-order logic (FOL). Let P be the vocabulary of predicates (also called relations). An atom has the form P(t1, t2, · · ·, tk) where

P ∈P is a predicate and ti is a logical variable or a constant. A literal is an atom or its negation. A formula is a literal, or created by connecting formulas using negation, conjunction or disjunction, or by quantifying a formula using a universal quantifier ∀x or an existential quantifier ∃x where x is a logical variable. A ground formula is a formula containing no variables. A variable in a formula is called free if there is no quantification over that variable. A sentence is a formula with no free variables.

A possible world ω interprets each relation in a sentence over a finite domain, represented by a set of ground literals. We write ω |= α to denote that the formula α is true in ω following the standard FOL semantics. The possible world ω is a model of a sentence Ψ if ω |= Ψ. We denote the set of all models of a sentence Ψ over the domain ∆by MΨ,∆.

In this paper, we are specially interested in the following syntactic fragments of FOL. A sentence with at most two logical variables is called an FO2 sentence. An FO2 sentence with only universal quantifiers is called a UFO2 sentence. An FO2 sentence with counting quantifiers ∃=k, ∃≤k and ∃≥k is called a C2 sentence, restricting that the number of assignments of the quantified variable satisfying the subsequent formula is exactly k, at most k or at least k, respectively. A sentence can be possibly augmented with cardinality constraints, which are expressions of the form of |P| ▷◁k where P is a predicate and ▷◁is a comparison operator {<, ≤, =, ≥, >}. We view cardinality constraints as atomic formulas that are satisfied if the number of true ground atoms of P in a possible world meets the constraint.

## 2.2 Weighted First-Order Model Counting

The weighted first-order model counting (WFOMC) problem takes the input consisting of a first-order sentence Ψ, a domain ∆of size n, and a pair of weighting functions (w, w) that both map P to real weights. Given a set L of literals whose relations are in Ψ, the weight of L is defined as

W(L, w, w):=

Y l∈LT w(pred (l)) ·

Y l∈LF w(pred (l)), where LT (resp. LF) denotes the set of positive (resp. negative) literals in L, and pred (l) maps a literal l to its corresponding relation name. We omit the symbols w, w and write W(L) in short when the weighting functions are clear in the text. Example 2.1. Let P = {R, S}. Consider the weighting functions w(R) = 2, w(S) = 3, w(R) = w(S) = 1. The weight of the literal set

L = {R(1), ¬R(2), S(1, 1), ¬S(1, 2), S(2, 1), S(2, 2)}

is w(R) · (w(S))3 · w(R) · w(S) = 54.

Definition 2.1 (Weighted First Order Model Counting). The WFOMC of a first-order sentence Ψ over a finite domain ∆ under weighting functions w, w is

WFOMC(Ψ, ∆, w, w):=

X µ∈MΨ,∆

W(µ, w, w).

19199

<!-- Page 3 -->

We remark that as the weighting functions are defined in terms of relations, all positive ground literals of the same relation get the same weights, and so do all negative ground literals of the same relation, i.e., the weights are symmetric w.r.t. domain elements. The symmetries of weights are crucial for efficient model counting as we shown later. For asymmetric WFOMC where each ground literal can have its own weight, we refer the reader to Beame et al. (2015), where it was shown that asymmetric WFOMC is #P-hard even for UFO2 sentences. Example 2.2. Consider the sentence Ψ = ∀x∀y: R(x) ∨ S(x, y) and the weighting functions in Example 2.1 over the domain ∆= {1, 2, · · ·, n}. Then

WFOMC(Ψ, ∆, w, w) =

22n+1 + 3n n.

In fact, for each domain element i ∈∆, either R(i) is true S(i, j) is not limited for any j ∈∆which contributes weight 2 · (3 + 1)n, or R(i) is false and S(i, j) is true for all j ∈ ∆which contributes weight 3n. Multiplying the contributed weight of each element, we get the above value.

2.3 1-Types and 2-Tables We will need the following notions to describe the algorithms.

A set of literals is maximally consistent if it does not contain both an atom and its negation at the same time, and cannot be extended to a larger consistent set. Definition 2.2 (1-Type). A 1-type of a first-order sentence Ψ is a maximally consistent set of literals formed from predicates in Ψ where each literal contains a single variable x. Definition 2.3 (2-Table). A 2-table of a first-order sentence Ψ is a maximally consistent set of literals formed from predicates in Ψ where each literal uses both the variables x, y.

We alternatively write a 1-type (and a 2-table) as a conjunction of literals that it contains. For example, Ψ = ∀x∀y: S(x, y) ∨R(y) has four 1-types: S(x, x) ∧R(x), S(x, x) ∧¬R(x), ¬S(x, x) ∧R(x) and ¬S(x, x) ∧¬R(x), and four 2-tables: S(x, y) ∧S(y, x), S(x, y) ∧¬S(y, x), ¬S(x, y) ∧S(y, x) and ¬S(x, y) ∧¬S(y, x). Intuitively, a 1-type interprets unary and reflexive binary relations for a single domain element, and a 2-table interprets binary relations for a pair of distinct domain elements. Definition 2.4 (1-Type Configuration). Let C = {C1, C2, · · ·, Cp} be the set of possible 1-types of a sentence Ψ.1 A 1-type configuration w.r.t. Ψ is a vector ζ(∆) = (ζ1, · · ·, ζp) indicating the number of elements partitioned to each 1-type over the domain ∆.

We often omit ∆for simplicity if it is clear in the context.

## 2.4 Data Complexity of WFOMC

We consider the data complexity, which measures the runtime of WFOMC in terms of the size of the domain, regarding the sentence and the weighting functions as fixed. The

1We call a 1-type possible in Ψ if it can be instantiated in some model of Ψ, which was also called valid in literatures (van Bremen and Kuzelka 2021; T´oth and Kuzelka 2024).

fragments whose WFOMC have polynomial time data complexity are called domain-liftable.

The fragment UFO2 was shown to be domain-liftable by Van den Broeck (2011) and Beame et al. (2015). We briefly introduce the latter algorithm whose notations will be used in the rest of the paper.

Consider WFOMC(Ψ, ∆, w, w) for a UFO2 sentence in the prenex normal form Ψ = ∀x∀y ψ(x, y) where ψ(x, y) is a quantifier-free FO2 sentence. Suppose that ∆= {1, 2, · · ·, n}. Let ψref(x, y) = ψ(x, y) ∧ψ(y, x). Then Ψ can be expanded as conjunction of ground formulae over ∆:

Ψ =

^ i∈∆ ψ(i, i)

!

∧



 ^ i,j∈∆:i<j ψref(i, j)



. (2)

Let C = {C1, C2, · · ·, Cp} be the set of possible 1-types of Ψ. Suppose that the 1-type of element i is determined as τi (τi ∈C). After substituting unary and reflexive binary literals in ψref(i, j) with true or false according to τi and τj, the formula for a pair of elements (i, j) does not have common ground literals with any other pair, hence the 2-tables between each pair of elements can be selected independently. Let D be the set of 2-tables of Ψ, and define Ds,t = {π ∈D: s(a) ∧t(b) ∧π(a, b) |= ψref(a, b)} for each s, t ∈C. The WFOMC can be computed as:

X τ1,...,τn∈C

Y i∈∆

W(τi)

Y i,j∈∆:i<j rτi,τj, (3)

where rs,t =

X π∈Ds,t

W(π). (4)

Furthermore, from Eq. (3) we know that the computation of WFOMC(Ψ, ∆, w, w) only depends on the numbers of elements assigned to each 1-type. Therefore, we compute Eq. (3) in time polynomial in n by enumerating the 1-type configuration instead of the 1-types for each element:

WFOMC(Ψ, ∆, w, w) =

X ζ1+···+ζp=n n! ζ1! · · · ζp!

· p Y i=1

(W(Ci))ζi (ri,i)( ζi

2) Y

1≤i<j≤p (ri,j)ζiζj

!

.

(5)

Recently, T´oth and Kuzelka (2023) proposed a dynamic programming version of this approach, which partially inspires our dynamic programming algorithm.

## 2.5 Evidence

In real-world applications, we often care about WFOMC conditioned on some set of ground literals, called evidence. Evidence can be in either the open-world or the closedworld form. Definition 2.5 (Open-World Evidence). The open-world evidence is a consistent set of ground literals E, where the truth of each ground atom is restricted by its positivity or negativity in E. Ground atoms not in E are considered unknown (i.e., the truth is not restricted).

19200

<!-- Page 4 -->

Definition 2.6 (Closed-World Evidence). The closed-world evidence of a set of predicates P′ ⊆P is a set of ground atoms E formed from P′. Ground atoms of the predicates in P′ appearing in E are supposed to be true, while those not appearing in E are supposed to be false. Remark 2.1. The closed-world notion differs from the closed-world assumption in probabilistic databases (Suciu 2018), where all ground atoms not appearing in the database are assumed to be false. In our case, only the ground atoms of the predicates in the evidence are assumed to be false, while those of other predicates are not restricted.

The two forms of the evidence can be transformed to each other. Transforming the closed-world representation to the open-world representation is straightforward by adding the default negative ground literals to the evidence set. For instance, the closed-world evidence E = {R(1, 2), R(2, 2)} of the predicate set P′ = {R} over the domain ∆= {1, 2} corresponds to the open-world evidence E′ = {¬R(1, 1), R(1, 2), ¬R(2, 1), R(2, 2)}. On the other hand, for example, consider the open-world evidence E = {R(1, 2), R(2, 3), ¬R(3, 4)}. To transform E to the closed-world form, we introduce two fresh binary predicates R⊤and R⊥, add the sentence ∀x∀y: (R⊤(x, y) →R(x, y)) ∧(R⊥(x, y) →¬R(x, y)) and write E′ = {R⊤(1, 2), R⊤(2, 3), R⊥(3, 4)} which is in the closed-world form.

The data complexity of WFOMC is extended to the case with evidence, where the evidence is treated as another input (besides the domain size) of the problem. Note that the number of ground literals in the evidence is polynomial in the domain size. Given a class E of evidence, we say that a firstorder fragment L with E is domain-liftable if the WFOMC conditioned on any evidence in E, i.e., WFOMC of Ψ ∧E for every Ψ ∈L and every E ∈E, can be computed in time polynomial in the domain size.

Unary and binary evidence are two particular classes of evidence, where unary evidence consists of ground literals (or atoms) containing a single element in the domain, and binary evidence consists of ground literals (or atoms) containing two distinct elements. For example, unary evidence can contain R(1, 1) though R is a binary predicate.

In this paper, we push the boundaries of data-liftability to the case where the underlying Gaifman graph of the binary evidence has bounded treewidth. Definition 2.7 (Gaifman Graph). The Gaifman graph with respect to the domain ∆and the closed-world binary evidence E is an undirected graph G∆,E of n vertices, in which there is an edge between a and b if and only if E contains P(a, b) or P(b, a) for some P ∈P.

**Figure 1.** shows an example of the Gaifman graph of the closed-world binary evidence {R(a, b), R(a, c), R(b, c), R(c, d), R(c, e), R(d, g), R(e, g)}.

For ease of presentation, we will alternatively write the evidence E as a conjunction of ground literals according to its semantics, i.e., E = V l∈E l for open-world evidence and E = V l∈E l ∧V l/∈E:pred(l)∈P′ ¬l for closed-world evidence, where pred(l) maps a literal l to its corresponding relation name.

𝑎 𝑏 𝑐 𝑑 𝑒 𝑔 𝑎 𝑎𝑏 𝑎𝑏𝑐 𝑏𝑐 𝑐 𝑑 𝑑𝑔 𝑑𝑒𝑔 𝑑𝑒 𝑐𝑑𝑒 𝑐𝑑 𝑐𝑑𝑒 𝑐𝑑𝑒 …

**Figure 1.** An example of the Gaifman graph (top) of closedworld binary evidence and its nice tree decomposition (bottom). The leaf, introduce, forget and join nodes are colored in white, blue, green and orange respectively. The last forget nodes are omitted for simplicity.

## 2.6 Treewidth and Tree Decompositions

We refer to the common definition of tree decomposition (e.g., Cygan et al. 2015).

Definition 2.8 (Tree Decomposition). A tree decomposition of a graph G(VG, EG) is a tree T(VT, ET) where each node u ∈VT holds a bag Bu ⊆VG and the tree satisfies the following conditions:

• S u∈VT Bu = VG. • For each edge (a, b) ∈EG, there is a tree node u ∈VT such that a, b ∈Bu. • For each vertex a ∈VG, the nodes u’s with a ∈Bu form a connected component in T.

The width of a tree decomposition is maxu∈T {|Bu|} −1. The treewidth of a graph G is the lowest width among its possible tree decompositions.

The following form of tree decomposition will be used to simplify the description of the algorithm.

Definition 2.9 (Nice Tree Decomposition). For a graph of treewidth k, its tree decomposition T(VT, ET) of width k is nice if a root node root ∈VT can be chosen such that the tree rooted at root satisfies:

• Each node has at most two children. • Broot = ∅and Bl = ∅for every leaf l. • Each non-leaf node is of one of the following three types: – An introduce node u has exactly one child v such that

Bu = Bv ∪{a} for some a /∈Bv. – A forget node u has exactly one child v such that Bu =

Bv \ {a} for some a ∈Bv. – A join node u has exactly two children v1, v2 such that

Bu = Bv1 = Bv2.

An example of the nice tree decomposition is shown in Figure 1, where the treewidth is 2. Together with Bodlaender’s work (1993), it was shown that such a tree decomposition can be computed efficiently.

Lemma 2.1. (Cygan et al. 2015; Bodlaender 1993) For a graph G(VG, EG) of treewidth k, its nice tree decomposition of size O(k · |VG|) can be computed in time linear in |VG|.

19201

<!-- Page 5 -->

## 2.7 Markov Logic Networks Markov Logic Networks (MLNs) (Richardson and

Domingos 2006) is a model used in the area of statistical relational learning. We will use MLNs to encode the Watts-Strogatz model later in the experiments.

An MLN Φ is a set of weighted quantifier-free first-order logic formulas α1, · · ·, αk with weights w1, · · ·, wk taking on values from the real domain or infinity:

Φ = {(w1, α1), (w2, α2), · · ·, (wk, αk)}.

Given a domain ∆, the MLN defines a probability distribution over possible worlds such that

PΦ,∆(ω) =

( exp

P

(wi,αi)∈ΦR wi·N(αi,ω)

Z, if ω |= Φ∞ 0, otherwise where ΦR denote the real-valued (soft) weight-formula pairs, Φ∞the ∞-valued (hard) weight-formula pairs, Z is the normalization constant ensuring valid probability values, and N(αi, ω) is the number of substitutions for variables in αi by constants that produce a ground formula satisfied in the world ω. The distribution formula is equivalent to the one of a Markov Random Field (Koller and Friedman 2009). Hence, an MLN, along with a domain, defines a probabilistic graphical model, and inference in the MLN is thus inference over that model.

Inference (and also learning) in MLNs is reducible to WFOMC (Van den Broeck, Meert, and Darwiche 2014). For each (wi, αi(xi)) ∈ΦR, where xi is the free variables, introduce a new formula ∀xi: ξi(xi) ↔αi(xi), where ξi is a fresh predicate, w(ξi) = exp(wi) and w(ξi) = 1. Let w(Q) = w(Q) = 1 for all other predicates Q. Consider sentence Γ created by the above procedure, with hard formulas added to Γ as they are. We can then compute the probability of a query ϕ as PΦ,∆(ϕ) = WFOMC(Γ∧ϕ,∆,w,w)

WFOMC(Γ,∆,w,w), where ϕ is a set of constraints that can be both hard and soft.

## 3 Approach

We describe a novel algorithm that given a sentence Ψ in the two-variable fragment, a finite domain ∆of size n, the weighting functions w, w, the closed-world unary evidence U and binary evidence E whose Gaifman graph G∆,E has treewidth k for some constant k (which we refer to as bounded-treewidth binary evidence), it computes WFOMC(Ψ ∧U ∧E, ∆, w, w) in time polynomial in n. The open-world evidence is handled by transforming it to the closed-world form as described in Section 2.5.

We start by providing an algorithm for the universally quantified two-variable fragment UFO2. At the end of the section, we use existing reduction techniques to extend the result to FO2 and C2 with cardinality constraints.

We assume that the nice tree decomposition T(VT, ET) of the Gaifman graph G∆,E is given, which has a root root ∈VT and size O(kn). By Lemma 2.1, such a tree decomposition can be computed in time linear in n.

Let C = {C1, C2, · · ·, Cp} be the set of possible 1-types of Ψ, and let D be the set of 2-tables of Ψ. Define Ds,t for each s, t ∈C as in Section 2.4. When we talk about the satisfaction of evidence with respect to a subset ∆′ ⊆∆, we only consider the truth of ground atoms that only contain constants in ∆′.

## 3.1 The Recursion Framework In this subsection, we present the algorithm for the UFO2

fragment with unary evidence U and binary evidence E.

For a node u ∈VT, Bu ⊆∆is the set of elements in the bag of u. Let B∗ u denote the union of Bv for all nodes v in the subtree rooted at u, and let Su denote B∗ u \ Bu. Given the 1types τ = V a∈Bu τa of elements in Bu satisfying U and the 1-type configuration ζ = ζ(Su) for elements in Su, define a partial model of u as a set of ground literals consisting of the followings:

• The model of Ψ over Su satisfying U and E and consistent with ζ (i.e., there are ζi elements having the 1-type Ci for each 1 ≤i ≤p), and • The 2-tables between Bu and Su satisfying E. Let Lu,τ,ζ be the set of possible partial models of u with respect to τ, ζ. Define f(u, τ, ζ) as the sum of weights of partial models in Lu,τ,ζ, i.e., f(u, τ, ζ) = P

L∈Lu,τ,ζ W(L). Then our target is to compute

WFOMC(Ψ∧U ∧E, ∆, w, w) =

X ζ1+···+ζp=n f(root, ⊤, ζ).

This is because Broot = ∅and Sroot = ∆, in which it holds that S ζ1+···+ζp=n Lroot,⊤,ζ = MΨ∧U∧E,∆. Next we compute f(u, τ, ζ) by recursion on the tree decomposition. The computation depends on the type of u. Recall that in Section 2.4 we write Ψ as ∀x∀y ψ(x, y) for some quantifier-free formula ψ and write ψref(x, y) = ψ(x, y) ∧ψ(y, x). As E is in the close-world representation w.r.t. a set of predicates P′, all atoms of P′ not in E are supposed to be false. We refine the definition of rs,t in Eq. (4) to align with E for element pairs not in E, i.e., rs,t =

X π∈Ds,t: π(a,b)|=V p∈P′ ¬p(a,b)∧¬p(b,a)

W(π)

for every pair of 1-types s, t ∈C. The original definition of rs,t in Eq. (4) can be regarded as in the case of P′ = ∅. The Leaf Node. If u is a leaf, we have Bu = ∅by Definition 2.9. In this case, the only valid pair of (τ, ζ) is (⊤, 0). We assign 1 to the f value:

f(u, ⊤, 0) = 1. (6)

The Introduce Node. Let v be the child node of u, and a be the unique element in Bu \ Bv. Each partial model L ∈ Lu,τ,ζ can be decomposed to the following three parts:

• A model µ ∈MΨ∧U∧E,Su consistent with ζ; • The 2-tables π1 between Bu \ {a} and Su; • The 2-tables π2 between a and Su. Let τa be the 1-type of a. Since Su = Sv, µ∧π1 is a partial model L′ ∈Lv, τ\τa, ζ where τ \ τa means τ removing τa. Therefore, each L ∈Lu,τ,ζ where a has 1-type τa can be

19202

<!-- Page 6 -->

regarded as augmenting π2 to a partial model in Lv, τ\τa, ζ. We then have f(u, τ, ζ) = p Y i=1

(rτa,Ci)ζi

!

· f(v, τ \ τa, ζ). (7)

Here, we use the property that a does not connect to any element in Su in the Gaifman graph, i.e., all ground atoms containing a and elements in Su should be false in the evidence E. For example, the element d in the introduce node cd in Figure 1 does not connect to any element in Scd = {a, b}, hence R(a, d), R(d, a), R(b, d), R(d, b) are all false in the evidence. The Forget Node. Let v be the child node of u, and a be the unique element in Bv \ Bu. Note that Su = Sv ∪{a}. Each partial model L ∈Lu,τ,ζ can be decomposed to the following five parts:

• The 1-type τa of a satisfying U; • A model µ ∈MΨ∧U∧E,Sv consistent with ζ−τa, where ζ−τa means ζ subtracting 1 at the position of τa; • The 2-tables π1 between a and Sv; • The 2-tables π2 between Bu and a; • The 2-tables π3 between Bu and Sv. As Bv = Bu ∪{a}, we know that µ ∧π1 ∧π3 is a partial model L′ ∈Lv, τ∧τa, ζ−τa. Therefore, each L ∈Lu,τ,ζ where a has 1-type τa can be regarded as augmenting τa and π2 to a partial model in Lv, τ∧τa, ζ−τa. Let Bu = {b1, · · ·, bm}. We can then compute f(u, τ, ζ) as follows:

f(u, τ, ζ) =

X τa∈C:τa|=U

X πb1∈Da,b1,τa,τb1

· · · X πbm∈Da,bm,τa,τbm

W(τa) ·

Y b∈Bu

W(πb)

!

· f(v, τ ∧τa, ζ−τa),

(8) where Da,b,s,t is the set of the 2-tables between the elements a and b having the 1-types s and t, respectively that satisfy E, i.e., Da,b,s,t = {π ∈Ds,t: π(a, b) |= E}. The Join Node. Let v1, v2 be the children nodes of u. Note that Su = Sv1 ∪Sv2. For each L ∈Lu,τ,ζ, it can be decomposed to the following three parts:

• A partial model L1 ∈Lv1,τ,z1; • A partial model L2 ∈Lv2,τ,z2 where (z1)i + (z2)i = ζi for each 1 ≤i ≤p; • The 2-tables between Sv1 and Sv2. Therefore, we have f(u, τ, ζ) =

X z1+z2=ζ f(v1, τ, z1) · f(v2, τ, z2)

· p Y i=1 p Y j=1 rCi,Cj

(z1)i·(z2)j,

(9)

where z1 + z2 denotes the element-wise addition of the two vectors. In the above equation, we use the same idea as handing the introduce node to compute the weights of 2-tables between Sv1 and Sv2.

Remark 3.1. In the computation of Eqs. (6) to (9) we might encounter invalid tuples of (u, τ, ζ), e.g., τ not satisfying U or the tuples where Pp i=1 ζi̸ = |Su|. The f-values of these tuples are set to 0 and thus do not affect the computation with valid tuples.

## 3.2 Time Complexity We show that computing the recursion of f by

Eqs. (6) to (9) takes time polynomial in n. Let p be the number of 1-types of Ψ and q be the number of 2-tables of Ψ. Recall that by Definition 2.8, for every node u ∈VT, we have |Bu| ≤k+1.

• For a leaf node, it takes O(1) time since there is only one valid tuple of (τ, ζ). • For a non-leaf node, the number of valid tuples of (τ, ζ) is O pk+1 · np

. The time of computing Eqs. (7) to (9) is as follows: – For an introduce node, computing the weights of 2- tables between a and Su takes O(p) time, so the total time on the node is O pk+2 · np

. – For a forget node, enumerating τa and πa,b for all b ∈

Bu takes O p · qk+1 time and the computation after the enumeration takes O(k) time, so the total time on the node is O pk+2 · qk+1 · k · np

. – For a join node, enumerating z1, z2 takes O(np) time and computing the weights of 2-tables between Sv1 and Sv2 takes O(p2) times, so the total time on the node is O pk+3 · n2p

.

By Lemma 2.1, the number of nodes on a tree is O(kn) and the tree can be computed in time O(n). Therefore, the total time is O(n+kn·pk+3 ·qk+1 ·k·n2p). As the sentence Ψ is fixed when we consider data complexity, p and q are also fixed. We then obtain the following theorem. Theorem 3.1. UFO2 with unary evidence and boundedtreewidth binary evidence is domain-liftable.

## 3.3 Implications of the Result

Beside UFO2, our algorithm also works for other domainliftable two-variable fragments which have a modular transformation to UFO2 defined by Van den Broeck, Meert, and Darwiche (2014). The property says that for any sentence in such fragment, its WFOMC can be obtained from the WFOMC of a UFO2 sentence over any finite domain. It was shown that there are modular transformations to UFO2 for FO2 (Van den Broeck, Meert, and Darwiche 2014) and C2

(Kuzelka 2021, Theorem 4) possibly with cardinality constraints (Kuzelka 2021, Proposition 5), hence we obtain the following theorem: Theorem 3.2. FO2 and C2, possibly with cardinality constraints, unary evidence and bounded-treewidth binary evidence are domain-liftable.

## 3.4 Asymmetric Weights for Binary Predicates

Recall that for symmetric weights, we compute the weight of a set of literals as W(L, w, w):= Q l∈LT w(pred (l)) · Q l∈LF w(pred (l)). Suppose that there is a set of literals La

19203

<!-- Page 7 -->

with asymmetric weights wa: La →R and wa: La →R that may differ from w(pred (l)) or w(pred (l)). We can now compute the weight of a set of literals as

W(L, w, w) =

Y l̸∈La,l∈LT w(pred (l)) ·

Y l̸∈La,l∈LF w(pred (l))

· Y l∈La,l∈LT wa(l) ·

Y l∈La,l∈LF wa(l).

To ensure that our algorithm works with this modification correctly, we need to add an edge (i, j) to the Gaifman graph for each literal P(i, j) ∈La or ¬P(i, j) ∈La, if the edge does not exist originally.

Then we can use the same techniques as in the symmetric case to compute asymmetric WFOMC. The data complexity is still polynomial in the domain size, as long as the Gaifman graph of La has bounded treewidth.

## 4 Experiments

We evaluated the performance of our algorithm on several examples and compared it with two other model counting algorithms, d4 (Jean-Marie 2017), Forclift (Van den Broeck et al. 2017), and Crane2 (Dilkas, Kidambi, and Singh 2025). d4 is a propositional model counter that compiles a formula in conjunctive normal form to deterministic decomposable negation normal form (d-DNNF). It generally performs well when compared to other model counters, but it cannot leverage lifted methods. Forclift is a model counter similarly to our algorithm that computes lifted inference and accepts binary evidence. Crane2 is a model counter based on Forclift, which performs very well on a limited set of problems, but does not support full range of FO2 sentences yet. For this reason, Crane2 is only used for friends and smokers experiments. All experiments were run on a laptop with Intel i7- 10510U CPU and 32GB of RAM.

## 4.1 Friends and Smokers

The first problem we chose is a variant of the often used friends and smokers problem with the following sentence:

∀x: ¬friends(x, x) ∧∀x∀y: friends(x, y) →friends(y, x) ∧∀x∀y: (smokes(x) ∧friends(x, y)) →smokes(y).

In our experiments, we provide open-world evidence that corresponds to the persons coming in cliques of 3 (i.e., due to the open-world nature of the evidence, they may also have other friends beyond the cliques), and suppose |∆| = 3 · k (k ≥1). We compared the runtime of our algorithm (labeled TD-WFOMC), d4, Forclift, and Crane2. Figure 2 shows that our algorithm runs significantly faster than the other three, and scales well to large domain size. We forgo the symmetry of friendships for Crane2 as symmetry is not supported. In Figure 3, we report the runtime of our algorithm for fixed domain size of 60 while varying the sizes of friend cliques.

## 4.2 Watts-Strogatz Model Another interesting problem we can tackle using WFOMC is performing inference on

Watts-Strogatz (WS) model (Watts

0 50 100 150 200 250 300 Domain Size

10−1

100

101

102

103

Time [s]

Forclift d4 TD-WFOMC Crane2

**Figure 2.** Time to compute the model count of friends and smokers problem with binary evidence

5 10 15 20 25 Clique Size

10−1

100

101

102

103

Time [s]

TD-WFOMC

**Figure 3.** Time to count models of friends and smokers problem with fixed |∆| = 60 for varying size of friend cliques.

and Strogatz 1998), which is a random graph model widely used in network science to generate small-world networks. The generation process of a random graph starts with a regular ring lattice with N nodes, where each node is connected to exactly K other nodes (assuming K is an even integer), K/2 on each side, warping over the end. To generate the random graph, each edge (i, j) is rewired with probability β in some order, meaning that edge (i, j) is replaced with edge (i, k) (i̸ = k) such that edge (i, k) does not exist already. The Watts-Strogatz model can be encoded as an MLN Ψ:

∞, ∀x: ¬WiredEdge(x, x) ∞, ∀x∀y: ¬WiredEdge(x, y) ∨¬WiredEdge(y, x) ∞, ∀x∃=K/2y: WiredEdge(x, y)

w1, WiredEdge(x, y) ∧¬EvidenceEdge(x, y) w2, WiredEdge(x, y) ∧EvidenceEdge(x, y) ∞, ∀x∀y: Edge(x, y) ↔ (WiredEdge(x, y) ∨WiredEdge(y, x)), where EvidenceEdge is interpreted as the starting regular ring lattice with binary evidence (in which each vertex has outgoing edges to only its right neighbors), Edge(x, y) represents the rewired edges, and w1 and w2 depend on β. We use wired edge to keep track of what edges are kept the same and what edges were changed, as well as to enforce that each node has degree ≥K/2, which holds in the Watts-Strogatz model.

Our algorithm can also handle random graphs created by

19204

<!-- Page 8 -->

101 102

Domain Size

10−1

100

101

102

Time [s]

Simplified Model

3 4 6 10 12 Domain Size

10−1 100 101 102

Regular Model

Inference on Watts Strogatz Graphs

TD-WFOMC cycles TD-WFOMC cliques d4 cycles d4 cliques

Forclift cycles Forclift cliques

**Figure 4.** Inference times on Watts-Strogatz model, K = 2 and the simplified model, K = 2 and M = ⌊|∆|+1

2 ⌋. We use full line for a ring lattice starting graph and dashed line for cliques starting graph.

this procedure regardless of what the starting graph is, as long as all the vertices share the same degree d (which is also expected in the original model) and the starting graph has bounded treewidth, i.e., the Gaifman graph of binary evidence of EvidenceEdge has bounded treewidth. In our experiments, we show this by considering the starting graph, where each node belongs to exactly one clique of size 3. This also requires us to modify the rewiring procedure, which we change accordingly.

We then build the MLN used in our experiments by adding the following weighted formulas to Ψ:

∞, ∀x∀y: friends(x, y) ↔Edge(x, y) w, smokes(x) ∧friend(x, y) →smokes(y), (10)

where the wired edges in the Watts-Strogatz model forms a friendship network.

We also consider a simplified version of the Watts- Strogatz model, where we start with a ring lattice (or a different graph as above) and instead of rewiring edges, we introduce M new edges, creating shortcuts in the graph. Its MLN is

∞, ∀x∀y: ¬WiredEdge(x, y) ∨¬WiredEdge(y, x) ∞, EvidenceEdge(x, y) →WiredEdge(x, y)

with the cardinality constraint |WiredEdge| = 2·|∆|+M.

The results of our experiments can be seen in Figure 4.

## 5 New Results on the Stable Seating

Arrangement Problem In the stable seating arrangement problem we have a group of agents A = [n] and a seating graph G = (VG, EG). In this and the following section, we use [n] as a shorthand for {1, · · ·, n}. Let d be the maximum degree of G. We use NG(v) to denote the neighborhood of v ∈VG. Each agent needs to be assigned a different seat (a vertex of graph G) and we assume n = |VG|.

Each agent a ∈A has a preference pa: A \ {a} 7→R of all other agents. The preference pa(b) represents how much utility agent a gets by sitting next to agent b. A preference profile is a collection of agent preferences, denoted by P = (pa)a∈A. A class of agents is a subset of agents K ⊆A such that all agents in it share a common preference function pK: A 7→R and no agent distinguishes between others in the class. A preference profile P is k-class if it can be partitioned into k classes K1, K2,..., Kk such that A = K1 ∪K2 ∪· · ·∪Kk. We denote the set of all classes by K = {Ki|i ∈[k]}. We also use the notation K∗= K∪K0, where K0 is a special class such that it holds that pKi(K0) = 0 for all i ∈[k]. We use class K0 to mark missing neighbors for seats in the seating graph that have fewer than d neighbors.

An arrangement is a bijection π: A 7→VG which assigns each agent a seat in the seating graph G. Given an arrangement π, the utility of each agent a ∈A is Ua(π) = P v∈NG(π(a)) pa(π−1(v)). An agent a envies another agent b if Ua(π) < Ua(π′) where π′ is obtained from π by swapping the positions of agents a and b. An arrangement is called envy-free if no agent envies another agent, and called stable if no two agents envy each other.

Definition 5.1 (Stable and Envy-Free Seating Arrangements). A k-class stable dinner seating arrangement problem SSA(A, P, G, K) is a problem of finding a stable seating arrangement π. #SSA(A, P, G, K) is the corresponding problem of counting the number of stable arrangements of SSA(A, P, G, K).

#EFSA(A, P, G, K) is defined analogously with respect to envy-free seating arrangements.

The complexity of finding stable seating arrangements in various settings has been studied (Bullinger and Suksompong 2023; Bodlaender et al. 2020; Berriaud, Constantinescu, and Wattenhofer 2023). Berriaud, Constantinescu, and Wattenhofer (2023) uses the notion of k-class stable seating arrangement, where each agent belongs to one of k classes, and each class is a group of agents that share the same utility function and are also indistinguishable to each other in the group. As established by Berriaud, Constantinescu, and Wattenhofer (2023), finding a stable or envy-free seating arrangement for cyclic or path-shaped tables is solvable in polynomial time when the number of classes is fixed.

In Theorem 5.1 below, we extend this positive result to counting problems and more complex table configurations. Specifically, we show that counting the number of stable seating arrangements is tractable on seating graphs of bounded treewidth and bounded degree—conditions that include cycles and paths—provided the number of classes is fixed. This result also answers the open question posed in (Berriaud, Constantinescu, and Wattenhofer 2023) concerning the 2 × n grid table, whose seating graph has treewidth 2, and further generalizes the tractability to a broader class of table structures.

Theorem 5.1. Counting the number of stable (or envy-free) seating arrangements is in time polynomial in the number of agents, if the problem is k-class and the seating graph has bounded treewidth and degree.

Proof. Let #SSA(A, P, G, K) and #EFSA(A, P, G, K) be the counting version of the stable and envy-free seat-

19205

<!-- Page 9 -->

ing arrangements problems respectively. We first show that there is an FO2 sentence Ψ, unary evidence U, binary evidence E, and a set of cardinality constraints C, such that #SSA(A, P, G, K) can be obtained from WFOMC(Ψ∧U∧ E ∧C, VG, w, w) in time polynomial in |VG|.

For a predicate P, we use P/k to indicate that the arity of P is k. The predicates in the formula Ψ are:

• neighbor i/2 (i ∈[d]), which are used to encode the seating graph. The neighbor i predicates are fully specified using closed-world evidence. For each vertex u ∈ VG, we arbitrarily label all its outgoing edges so that no two edges share the same label i. This is useful when we later distinguish the individual neighbors of u. • class s/1 (s ∈K), where class s(x) indicates that the class of the agent sitting at vertex x is s. • neighbor i is s/1 (i ∈ [d], s ∈ K∗), where neighbor i is s(x) denotes that the i-th neighbor of the vertex x is of class s. Recall that K∗= K ∪K0 where K0 is a special class such that ps(K0) = 0 for all s ∈K. We use neighbor i is K0(x) in case the degree da of x is less than the maximum degree d of G. • envies/2, where envies(x, y) indicates that the agent at seat x envies the agent at seat y.

We encode the seating graph to closed-world binary evidence E. Let

E =

[ a∈VG

{neighbor i(a, bi) | i ∈[da], (a, bi) ∈EG}, where da is the degree of a. Recall that we label the outgoing edges of a in such a way that a is connected to each of its neighbors using a differently labeled edge. The unary evidence U is only necessary for seating graphs with at least one vertex a with degree da < d. In such case, we define

U =

[ a∈VG

{neighbor i is K0(a) | da < i ≤d}.

Let Φ be a first-order sentence

Φ =∀x:

_ s∈K class s(x) (11)

∧∀x:

^ s∈K,t∈K,s̸=t

¬class s(x) ∨¬class t(x) (12)

∧∀x:

d^ i=1

_ s∈K∗ neighbor i is s(x) (13)

∧∀x:

d^ i=1

^ s,t∈K∗,s̸=t

¬neighbor i is s(x)

∨¬neighbor i is t(x)

(14)

∧

^ i∈[d],s∈K

∀x∀y: (class s(y) ∧neighbor i(x, y))

→neighbor i is s(x). (15)

Let C =

|class s| = |s| s ∈K be a set of cardinality constraints and let w(P) = w(P) = 1 for all predicates P in Φ. Then WFOMC(Φ ∧U ∧E ∧C, VG, w, w) · Q s∈K |s|! counts the number of possible seating arrangements (possibly unstable or not envy-free) for the set of agents A at a table given by the seating graph G. Here, the term Q s∈K |s|! counts for each class the number of arrangements of the agents to the vertices of the class.

Next, let

F = n class s(x) ∧

^ i∈[d],ti∈K∗ neighbor i is ti(x)

∧

^ i∈[d],ui∈K∗ neighbor i is ui(y)

s ∈K,

X i∈[d]

ps(ti) <

X i∈[d]

ps(ui)

o and

Γ = ∀x∀y: ¬envies(x, y) ∨¬envies(x, y)

∧∀x∀y: envies(x, y) ↔



_ f∈F f(x, y)



.

Since Γ filters out all unstable seating arrangements, we can see that if Ψ = Φ ∧Γ, then

#SSA(A, P, G, K)

=WFOMC(Ψ ∧U ∧E ∧C, VG, w, w) ·

Y s∈K

|s|!.

Since the formula Ψ is fixed and depends only on the number of classes and the maximum degree of the seating graph, we can say that due to results in Section 3.2, we prove that #SSA(A, P, G, K) can be computed in time polynomial in the number of agents if the maximum degree d of the seating graph G and the treewidth t of G are fixed.

We can use the same proof for computing the number of envy-free seating arrangements #EFSA(A, P, G, K) if instead of ∀x∀y: ¬envies(x, y) ∨¬envies(y, x) we require only ∀x∀y: ¬envies(x, y).

## 6 Conclusion

We provide a novel approach to tackle the symmetry limitation in WFOMC by introducing an algorithm to compute WFOMC of FO2 and C2 with cardinality constraints, unary evidence and binary evidence where the underlying Gaifman graph is of bounded treewidth in time polynomial in the domain size. The algorithm applies to the counting problem in combinatorics that can be encoded by WFOMC of such fragment, e.g., the stable seating arrangement problem. We hope this work inspires further advances to asymmetric lifted inference, and establishes a general counting method on bounded-treewidth graphs.

## Acknowledgements

V´aclav K˚ula is supported by the Central Europe Leuven Strategic Alliance (CELSA) project Towards Scalable Algorithms for Neuro-Symbolic AI. Yuanhong Wang is supported by National Natural Science Foundation of China

19206

<!-- Page 10 -->

(No.62506141). Ondˇrej Kuˇzelka is supported by the Czech Science Foundation project 23-07299S (Statistical Relational Learning in Dynamic Domains).

## References

Beame, P.; Van den Broeck, G.; Gribkoff, E.; and Suciu, D. 2015. Symmetric Weighted First-Order Model Counting. In PODS, 313–328. ACM. Berriaud, D.; Constantinescu, A.; and Wattenhofer, R. 2023. Stable Dinner Party Seating Arrangements. In WINE, volume 14413 of Lecture Notes in Computer Science, 3–20. Springer. Bodlaender, H. L. 1993. A linear time algorithm for finding tree-decompositions of small treewidth. In STOC, 226–234. ACM. Bodlaender, H. L.; Hanaka, T.; Jaffke, L.; Ono, H.; Otachi, Y.; and van der Zanden, T. C. 2020. Hedonic Seat Arrangement Problems. In AAMAS, 1777–1779. International Foundation for Autonomous Agents and Multiagent Systems. Bullinger, M.; and Suksompong, W. 2023. Topological Distance Games. In AAAI, 5549–5556. AAAI Press. Courcelle, B. 1990. The Monadic Second-Order Logic of Graphs. I. Recognizable Sets of Finite Graphs. Inf. Comput., 85(1): 12–75. Cygan, M.; Fomin, F. V.; Kowalik, L.; Lokshtanov, D.; Marx, D.; Pilipczuk, M.; Pilipczuk, M.; and Saurabh, S. 2015. Parameterized Algorithms. Springer. Dilkas, P.; Kidambi, A. K.; and Singh, G. 2025. Crane. https: //github.com/dilkas/crane. Accessed: 2025-06-01. Getoor, L.; and Taskar, B. 2007. Introduction to statistical relational learning, volume 1. MIT press Cambridge. Jean-Marie, L. 2017. d4. https://github.com/crillab/d4. Accessed: 2017-07-09. Koller, D.; and Friedman, N. 2009. Probabilistic Graphical Models - Principles and Techniques. MIT Press. Kuang, Q.; Kuzelka, O.; Wang, Y.; and Wang, Y. 2024. Bridging Weighted First Order Model Counting and Graph Polynomials. arXiv:2407.11877. Kuzelka, O. 2021. Weighted First-Order Model Counting in the Two-Variable Fragment With Counting Quantifiers. J. Artif. Intell. Res., 70: 1281–1307. Malhotra, S.; Bizzaro, D.; and Serafini, L. 2025. Lifted inference beyond first-order logic. Artif. Intell., 342: 104310. Miettinen, P. 2009. Matrix Decomposition Methods for Data Mining: Computational Complexity and Algorithms. Ph.D. thesis, University of Helsinki. Poole, D. 2003. First-order probabilistic inference. In IJCAI, 985–991. Morgan Kaufmann. Richardson, M.; and Domingos, P. M. 2006. Markov logic networks. Mach. Learn., 62(1-2): 107–136. Suciu, D. 2018. Probabilistic Databases. In Encyclopedia of Database Systems (2nd ed.). Springer. Svatos, M.; Jung, P.; T´oth, J.; Wang, Y.; and Kuzelka, O. 2023. On Discovering Interesting Combinatorial Integer Sequences. In IJCAI, 3338–3346. ijcai.org.

T´oth, J.; and Kuzelka, O. 2023. Lifted Inference with Linear Order Axiom. In AAAI, 12295–12304. AAAI Press. T´oth, J.; and Kuzelka, O. 2024. Complexity of Weighted First-Order Model Counting in the Two-Variable Fragment with Counting Quantifiers: A Bound to Beat. In KR. van Bremen, T.; and Kuzelka, O. 2021. Faster lifting for two-variable logic using cell graphs. In UAI, volume 161 of Proceedings of Machine Learning Research, 1393–1402. AUAI Press. Van den Broeck, G. 2011. On the Completeness of First- Order Knowledge Compilation for Lifted Probabilistic Inference. In NIPS, 1386–1394. Van den Broeck, G. 2013. Lifted Inference and Learning in Statistical Relational Models (Eerste-orde inferentie en leren in statistische relationele modellen). Ph.D. thesis, Katholieke Universiteit Leuven, Belgium. Van den Broeck, G.; and Darwiche, A. 2013. On the Complexity and Approximation of Binary Evidence in Lifted Inference. In NIPS, 2868–2876. Van den Broeck, G.; and Davis, J. 2012. Conditioning in First-Order Knowledge Compilation and Lifted Probabilistic Inference. In AAAI, 1961–1967. AAAI Press. Van den Broeck, G.; Meert, W.; and Darwiche, A. 2014. Skolemization for Weighted First-Order Model Counting. In KR. AAAI Press. Van den Broeck, G.; Meert, W.; Davis, J.; and Van Haaren, J. 2017. Forclift. https://github.com/UCLA-StarAI/Forclift. Accessed: 2017-06-14. Wang, Y.; Pu, J.; Wang, Y.; and Kuzelka, O. 2024. Lifted algorithms for symmetric weighted first-order model sampling. Artif. Intell., 331: 104114. Watts, D. J.; and Strogatz, S. H. 1998. Collective dynamics of ‘small-world’ networks. Nature, 393(6684): 440–442.

19207
