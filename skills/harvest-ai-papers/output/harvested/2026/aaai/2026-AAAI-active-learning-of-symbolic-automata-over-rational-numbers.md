---
title: "Active Learning of Symbolic Automata over Rational Numbers"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38982
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38982/42944
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Active Learning of Symbolic Automata over Rational Numbers

<!-- Page 1 -->

Active Learning of Symbolic Automata Over Rational Numbers

Sebasti´an Hagedorn1, Mart´ın Mu˜noz1, 2, 3, Cristian Riveros1, 2, Rodrigo Toro Icarte1, 4

1Department of Computer Science, Pontificia Universidad Cat´olica de Chile, Santiago, Chile 2Instituto Milenio Fundamentos de los Datos (IMFD), Santiago, Chile 3Univ. Artois, CNRS, UMR 8188, Centre de Recherche en Informatique de Lens (CRIL), F-62300 Lens, France 4Centro Nacional de Inteligencia Artificial (CENIA), Santiago, Chile

## Abstract

Automata learning has many applications in artificial intelligence and software engineering. Central to these applications is the L∗algorithm, introduced by Angluin (1987). The L∗ algorithm learns deterministic finite-state automata (DFAs) in polynomial time when provided with a minimally adequate teacher. Unfortunately, the L∗algorithm can only learn DFAs over finite alphabets, which limits its applicability. In this paper, we extend L∗to learn symbolic automata whose transitions use predicates over rational numbers, i.e., over infinite and dense alphabets. Our result makes the L∗algorithm applicable to new settings like (real) RGX, and time series. Furthermore, our proposed algorithm for learning each predicate is optimal in the sense that it asks a number of queries to the teacher that is at most linear with respect to the size of their representation.

## Introduction

Automata learning has powered numerous advances in artificial intelligence and software engineering. Its applications range from interpretable sequence classification (e.g., Shvo et al. 2021; Katzouris and Paliouras 2022; Roy et al. 2023) to reinforcement learning (e.g., Hasanbeig et al. 2021; Corazza, Gavran, and Neider 2022; Toro Icarte et al. 2023). Key to these advances is the L∗algorithm (Angluin 1987).

Learning the smallest automaton consistent with a fixed set of examples is a well-known NP-hard problem (Gold 1967; Angluin 1980). However, Angluin (1987) showed that minimal automata can be learned in polynomial time under an active learning framework. In this setting, the learner interacts with a minimally adequate teacher (MAT), which can answer two types of queries: membership queries, which return the correct classification of a given string, and equivalence queries, which verify whether a proposed automaton correctly represents the target language. If the hypothesis is incorrect, the teacher provides a counterexample. Under these assumptions, the L∗algorithm can efficiently learn a minimal DFA in polynomial time, assuming constant-time responses to both query types.

The L∗algorithm has had a significant and lasting influence on the field of automata learning, shaping both theoretical developments and practical applications (Vaandrager

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

et al. 2022). However, it is limited to learning deterministic finite automata (DFA), which can only capture temporal behaviors over finite alphabets. This limitation restricts their use in domains involving infinite or dense input spaces, such as complex event recognition (Giatrakos et al. 2020) and time series learning (Hamilton 2020).

To address these limitations, van Noord and Gerdemann (2001) and Veanes et al. (2012) introduced the concept of symbolic automata, which generalize classical automata by allowing transitions to be labeled with predicates over rich alphabet theories, while preserving many of the desirable properties of traditional automata. The learnability and practical applications of symbolic automata have been extensively explored (Drews and D’Antoni 2017; Mens and Maler 2015; Pitt and Warmuth 1993). However, existing approaches for learning symbolic automata assume that the MAT provides lexicographically minimal counterexamples. Without this assumption, it remains an open question whether such automata can be learned efficiently.

In this paper, we extend the L∗algorithm to enable the learning of symbolic automata over the rational numbers. Our approach can learn any symbolic automaton whose predicates operate over a single rational-valued variable, without imposing any constraints on the form of counterexamples provided by the teacher. Furthermore, our method is query-efficient, requiring only a polynomial number of queries relative to the size of the target automaton. To achieve this, we first introduce a technique for learning finite piecewise functions over the rational numbers using a MAT. This is accomplished through a search procedure over a number-theoretic structure known as the Stern–Brocot tree. Interestingly, our learning algorithm is efficient in the sense that it needs a linear number of queries concerning the function size and does not depend on the worst-case size counterexample. We then integrate this learning strategy into the L∗framework to support the learning of symbolic automata over rational numbers. Finally, we prove that our method can learn any such automaton in polynomial time under standard assumptions. Given space restrictions, an extended version of this article can be found in (Hagedorn et al. 2025).

## 2 Preliminaries

We begin by recalling the learning setting that we will use throughout the paper. We present the general definition here

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19091

<!-- Page 2 -->

to later instantiate it for finite piecewise functions in Section 3 and for symbolic automata in Section 4.

Learning domain. Let D be an infinite domain (e.g., sequences) and Σ a finite domain (e.g., {0, 1}). A concept over D is a function γ: D 7→Σ. A representation r over D is a finite object (i.e., given by some syntax and semantics) that encodes a function r: D 7→Σ. We denote by size(r) the size of r, namely, the number of bits to store r. We say that r is a representation of a concept γ, denoted by r = γ, if r(d) = γ(d) for every d ∈D. We usually use C and R to denote a class of concepts and a class of representations, respectively. We assume that every concept C has some representation in R, namely, for every γ ∈C there exists r ∈R such that r = γ. Finally, we denote by size(γ) = minr:r=γ size(r) the size of the minimum representation in R of γ ∈C.

The MAT learning setting. Let C and R be a class of concepts and representations, respectively, over D. In general, given some concept γ ∈C, the learning task consists of finding some r ∈R such that r = γ. For this task, we follow the active learning setting introduced by (Angluin 1987) called Minimally Adequate Teacher (MAT): the Learner has to infer the behavior of an unknown concept γ ∈C by having access to two functions, called membership and equivalence oracles, provided by the Teacher who knows γ beforehand. Specifically, a membership oracle MQ of γ answers the following query: given an input d ∈D, return the output γ(d). An equivalence oracle EQ of γ receives a representation r ∈R and returns either the pair (true, ⊥), meaning that r = γ, or the pair (false, d∗) where d∗∈D, meaning that r̸ = γ and d∗is a counterexample (i.e., r(d∗)̸ = γ(d∗)). For any pair of functions f, g: N →N, we say that an algorithm Λ learns R using a MAT with f(n) membership queries and g(n) equivalence queries if, given a membership oracle MQ and an equivalence oracle EQ of some unknown concept γ ∈C, Λ finds a representation r ∈R such that r = γ after making at most O(f(n)) membership queries and O(g(n)) equivalence queries with size(γ) = n. As it is common in the literature, for measuring the efficiency of Λ, we are interested in bounding the number of calls that Λ makes to the oracles with respect to size(γ) and, also, to the length of the longest counterexample provided by EQ.

## 3 Learning Finite Piecewise Functions

In this section, we address the problem of active learning finite piecewise functions over the rational numbers. We start by introducing some basic notation regarding rationals and intervals that we will use throughout the paper to then define the learning problem. We end this section by presenting the main technical result of the paper.

Rationals and intervals Let N = {0, 1,...} be the set of natural numbers, Z the set of integers, Q the set of rational numbers, and Q∞= Q ∪{∞, −∞} where −∞< q < ∞ for every q ∈Q. We will use a, b, c,... to denote elements in N or Z, and p, q, r,... for elements in Q. Further, we represent any q ∈Q∞as a fraction q = a b where a ∈Z and b ∈N. We note that this includes the fractions a

0 = ∞and

−a

0 = −∞for any a ∈N. We say that a b is irreducible if there is no natural number c > 1 such that c divides both a and b. In the sequel, we will always assume that a b is irreducible, where ∞= 1

0 and −∞= −1 0. For q = a b ∈Q with a̸ = 0, we define size(q) = log(|a|) + log(b) where log(·) is in base 2, namely, the number of bits to represent q as a fraction; and when a = 0, size(q) = 1.

A subset I ⊆Q is an interval if I is non-empty, and for every p, q ∈I and r ∈Q, if p < r < q, then r ∈I. As usual, we represent intervals as pairs ⟨p, q⟩where ⟨∈ { [, (} and ⟩∈{ ],) }. In addition, when p = −∞then ⟨= (, and when q = ∞, then ⟩=) (i.e., −∞or ∞are never included). Further, we always write these p and q as irreducible fractions in Q∞. For example:

(−1

2, 3 1] = {p ∈Q | −1

2 < p ≤3} and 7

1, 1 0

= {p ∈Q | 7 ≤p < ∞}

are intervals over Q under this notation. For I = ⟨p, q⟩we define size(I) = size(p) + size(q).

For two intervals I1, I2, we write I1 < I2 iff p < q for every p ∈I1 and q ∈I2. We say that a sequence of intervals I1I2... Ik is an interval partition of Q iff I1 < I2 <... < Ik and Q = Sk j=1 Ij. For instance, −1

0, −2 3 −2

3, 1 1

2, 3 3

2, 1 0 is an interval partition of Q.

Finite piecewise functions. Let Σ be a finite set of labels. We will use A, B,... for denoting labels in Σ. The class C of concepts are all functions over the rationals γ: Q 7→Σ. Further, we restrict ourselves to the class of finite piecewise functions, namely, functions γ that can be represented by a finite number of intervals. Formally, we say that an interval I is monochromatic with respect to γ if γ(p) = γ(q) for every pair p, q ∈I. If I is monochromatic with respect to γ, we define γ(I) = γ(q) where q is any element in I. As an example, consider a function γ1: Q →{A, B}:

γ1(q) =

A, if −2

3 ≤q ≤1 2 or 3 2 < q, B, otherwise.

One can check that interval (1

2, 3 2] is monochromatic with respect to γ1, and that γ1((1

2, 3 2]) = B. We say that γ is a finite piecewise function if there exists an interval partition I1I2... Ik of Q such that each Ij is monochromatic with respect to γ. If this is the case, we can represent γ as the sequence of pairs:

r = (I1, γ(I1)) (I2, γ(I2))... (Ik, γ(Ik)). (†)

We will write r = γ to denote that r represents γ and write r(q) to denote the label γ(q) for every q ∈Q. We define the class R of all representations r like (†) of finite piecewise functions. We define the size of r as size(r) = P j size(Ij). Note that a representation of a finite piecewise function γ is not unique. For example, ((−1

0, 1 1), A)([ 1 1, 1 0), A) and ((−1

0, 1 0), A) represent the same concept γ where γ(q) = A for every q ∈Q. For this reason, we say that a representation like (†) is the canonical representation of γ if, in addition,

19092

<!-- Page 3 -->

γ(Ij)̸ = γ(Ij+1) for every j < k. One can easily check that every concept γ has a unique canonical representation. Finally, for any concept γ with canonical representation r we define size(γ) = size(r). Continuing the example, γ1 can be seen to be a finite piecewise function. Its canonical representation is shown in Figure 2.

Main technical result. Herein lies the problem of learning an unknown finite piecewise function γ ∈C that can be finitely represented by some r ∈R. In this work, we present an MAT learning algorithm that does this efficiently, focusing on finding each labeled interval (I, γ(I)) in time O(size(I)). Specifically, we get the following technical result on learning finite piecewise functions. Theorem 1. For the class C of finite piecewise functions, there exists a learning algorithm that learns an unknown concept γ ∈C using MAT with a linear number of membership and equivalence queries over size(γ).

In other words, no matter the concept γ, the number of calls to the oracles is proportional to the size of the canonical representation of γ, where rational numbers are represented in a binary encoding. Arguably, this MAT learning algorithm is asymptotically optimal in the sense that one cannot take less than size(γ). Furthermore, the learning guarantee does not depend on the size of the longest counterexample as other MAT algorithms do (see Theorem 2 in the next section).

We prove Theorem 1 in Sections 5 and 6. Next, we show how to apply this result on learning symbolic automata.

## 4 Learning Symbolic Automata

Symbolic finite state automata (SFA) are an extension of classical finite state automata in which the transitions are replaced by predicates instead of the symbols from a finite alphabet. They were first introduced in (van Noord and Gerdemann 2001) with natural language processing motivations and have been studied in recent decades because they enable applications over real-life scenarios that usually consider large or even infinite alphabets (Veanes 2013; Argyros and D’Antoni 2018; Drews and D’Antoni 2017).

This paper addresses the learning of SFAs with onedimensional predicates on Q, built out of inequalities. In this section, we formally define SFAs with inequality formulas. Then, we present some applications of SFAs in practice. After this, we show how to apply Theorem 1 to MAT learning of SFAs and discuss how it is compared with similar works.

Inequality formulas. Let x be a fixed variable. An inequality formula has the following syntax:

φ:= x < q | x > q | x ≤q | x ≥q | φ ∨φ | φ ∧φ with q ∈Q. We say that a value p ∈Q satisfies φ if one can replace every appearance of x in φ by p and obtain a binary formula that evaluates to true. We denote this by p |= φ. An inequality formula φ naturally defines a function JφK: Q 7→{0, 1} (also called a predicate) such that JφK(p) = 1 if, and only if, p |= φ. Two inequality formulas φ and ψ are equivalent if JφK = JψK. As an example, consider:

φ =

−2

3 ≤x ∧x ≤1

∨

2 < x which defines JφK = [ −2

3, 1 3] ∪(3 2, −∞) (similar to γ1). We write true or false as a shorthand for two fix formulas that are always 1 or 0, respectively. Further, for ∼1, ∼2 ∈ {<, ≤}, we write q1 ∼1 x ∼2 q2 as a shorthand for q1 ∼1 x ∧x ∼2 q2. One can easily check that for every interval I, there exists a formula φI that defines it (e.g., if I = [ −2

3, 1 3] then φI:= −2

3 ≤x ≤1 3). We call the rational numbers that appear in φ the coefficients of φ. We define the size of φ, denoted by size(φ), as the sum of the sizes of the coefficients and symbols appearing in φ. Finally, we denote the set of all inequality formulas as F.

Symbolic Automata. We introduce a subset of Symbolic Finite state Automata (SFA) that carry predicates that are represented by inequality formulas. The difference between SFA and classical finite automata is that finite automata have transitions of the form s1 a−→s2 with s1, s2 states and a a symbol in some finite alphabet; whereas SFA have transitions of the form s1 φ−→s2 with s1, s2 states and φ an inequality formula. Consequently, there is (possibly) an infinite number of values that can satisfy φ. Hence these type of transitions enable finite state automata to handle an infinite alphabet such as the set of rational numbers.

Formally, a (non-deterministic) Symbolic Finite state Automata with inequality predicates (SFA) is a tuple:

A = (S, ∆, s0, F) (∗)

where S is a finite set of states, ∆⊆S × F × S is a finite relation, s0 ∈S is the initial state, and F ⊆S is the set of final states. We say that ∆is the transition relation of A and (s1, φ, s2) ∈∆is a transition of A that we usually write as s1 φ−→s2. A run of A over a string w = q1q2... qn ∈Q∗is a sequence of transitions:

ρ:= s0 φ1 −→s1 φ2 −→...

φn −−→sn such that (si−1, φi, si) ∈∆and qi |= φi for every i ∈ {1,..., n}. A run is accepting if sn ∈F. The language accepted by A is defined as L(A) = {w ∈Q∗| A accepts w}. We define size(A) = |S| + |∆| + P

(s1,φ,s2)∈∆size(φ) as the size of A.

An SFA A of the form (∗) is deterministic if, for all pairs of transitions (s, φ, s1), (s, ψ, s2) ∈∆, if JφK ∩JψK̸ = ∅, then φ = ψ and s1 = s2. In (D’Antoni and Veanes 2014), it was shown that for every SFA there exists an equivalent deterministic SFA of at most exponential size. As it is standard in the MAT learning setting of finite automata (Angluin 1987; Drews and D’Antoni 2017), in the sequel we assume that all SFAs are deterministic.

In the following, we present two examples of how to use SFAs in practice that motivate their learning problem.

RGX. In practice, regular expressions (RGX) process text documents where symbols are encoded in Unicode, where each symbol is an integer in the range from 0 to 1.114.111 written in hexadecimal as U+0000 to U+10FFFF. For instance, the digits {0, 1,..., 9} run from 48 (U+0030) to 57 (U+0039), the latin alphabet in uppercase {A,..., Z} runs from 65 (U+0041) to 90 (U+005A), and the latin alphabet in lowercase {a,..., z} runs from 97 (U+0061) to

19093

<!-- Page 4 -->

s0 (1) s1 s2 65 ≤x ≤90 97 ≤x ≤122 true true s0 (2) s1 q2

13 2 < x ≤23 3 13 1 < x true true true

**Figure 1.** Two SFA with inequality formulas. (1) is the SFA of a RGX and (2) is the SFA of a time series pattern.

122 (U+007A). Therefore, a text document in practice can be seen as a sequence of integers q1... qn ∈N∗(note that although SFA and our results used Q, they also applied to N given that N ⊆Q). For a simple example, suppose that we want to check an uppercase letter directly followed by a lowercase letter in the Latin alphabet. This pattern can be defined by a RGX1 (in PCRE or Perl syntax) as:

[A-Z][a-z]

where [A-Z] and [a-z] are called char classes denoting any symbol from A to Z (i.e. interval [65, 90]) and from a to z (i.e. interval [97, 122]). In Figure 1 (1), we show how to represent this RGX with an SFA by using inequalities. Note that this pattern can be defined with standard finite state automata; however, we will need a large number of transitions between states to encode the inequality formulas.

Time series. Consider a scenario where a sensor measures the temperature of the environment. More precisely, consider that the sensor emits a signal in the form of a sequence q1q2... qn ∈Q∗where each qi ∈Q is a temperature measured in degrees Celsius and where the order represents the time (i.e., q1 was measured before q2, and so on).

Consider that a user is interested in detecting the following pattern of the sensor signals:

13 2 < t1 ≤23 3; t2 > 13 1 which means that it wants to see a temperature t1 in the range (13

2, 23 3 ] followed by a temperature t2 over 13. We use; to denote that two events occur sequentially, but not necessarily consecutively. One can check that the SFA illustrated in Figure 1 (2) detects the previously defined pattern.

The two previous examples are simplified cases to showcase the use of SFA with inequality formulas in practice. This setting can easily be extended to more complex scenarios, for example, where data symbols can be a tuple of the form (a, q) where a is a label and q is a rational number. For the sake of presentation, we prefer to present SFA and their examples only over rational numbers, but one can easily extend them to other scenarios.

1Notice that, in practice, RGX are unanchored, namely, they start the evaluation in any part of the document.

Learning SFAs using MAT. The following result2 presented in (Argyros and D’Antoni 2018) is crucial for deriving our result regarding MAT learning SFAs.

Theorem 2 (Theorem 1 in (Argyros and D’Antoni 2018)). Let Λ be an algorithm that learns F using MAT with f(n) membership queries and g(n) equivalence queries. Then SFA can be learned using MAT with n2 · f(n) + n2 · g(n)·log(m) membership queries and n2 ·g(n) equivalence queries where m is the length of the longest counterexample.

In other words, a good MAT learning algorithm for the class of inequality formulas F implies a good MAT learning algorithm for SFA with inequality predicates. One can easily note that inequality formulas are a special case of finite piecewise functions. Indeed, we already noticed that a formula φ ∈F defines a function JφK: Q 7→Σ where Σ = {0, 1}. Furthermore, JφK is a finite piecewise function and, if JφK has a canonical representation of the form (†):

φ∗:=

_ j:JφK(Ij)=1 φIj where φI is the formula representing the interval I. Then, size(φ∗) ∈O(size(JφK)), that is, the minimum size of a representation in F for φ is proportional to the size of the canonical representation of JφK. Then, by applying Theorem 1 for learning finite piecewise functions with Theorem 2 for learning SFAs we get the following corollary.

Corollary 1. An SFA of size n can be learned using MAT with n3 · log(m) membership queries and n3 equivalence queries where m is the length of the longest counterexample.

It is important to note that previous works like (Drews and D’Antoni 2017; Argyros and D’Antoni 2018; Mens and Maler 2015) settled the basis on MAT learning SFAs (e.g., Theorem 2); however, their results rely on simple predicates (e.g., equality predicates) or strong assumptions over the teacher (e.g., the equivalence query always returns the minimal counterexample). Instead, to the best of our knowledge, Corollary 1 is the first result that shows fully MAT learning of SFA over non-trivial predicates. Furthermore, it is efficient in the sense that Theorem 1 is the best that one could achieve for combining it with Theorem 2.

## 5 The Stern-Brocot Tree and Break Links

In this section, we present the Stern-Brocot tree of rational numbers and some of its properties. Then we introduce the concept of a break link and its connection with convergent fractions, which will be fundamental in supporting the efficient learning algorithm of finite piecewise functions.

The Stern-Brocot tree. The Stern-Brocot tree (TSB) is a construction to represent the set of positive rational numbers presented by (Stern 1858; Brocot 1861). In this paper we consider an extended version of this tree that contains the

2(Argyros and D’Antoni 2018) presents Theorem 2 with more details regarding the exact complexity of its MAT learning algorithm. Here, we oversimplified the upper bound on the size of the representation, which better fits our purposes.

19094

<!-- Page 5 -->

0 1

−1

1

−2

1

−3

1

−4

1 −5

2

−3

2

−5

3 −4

3

−1

2

−2

3

−3

4 −3

−1

3

−2

−1

4

1 1

1 2

1 3

1 4 2

2 3

3 3 4

2 1

3 2

4 3 3

3 1

2 4 1 r1 =

(−1

0, −2 3), B

[ −2

3, 1 2], A

(1

2, 3 2], B

(3

2, 1 0), A

**Figure 2.** Top: The finite piecewise function γ1 (see Section 3) shown in a Stern–Brocot tree up to depth 4. Nodes q for which γ(q) = A (resp. B) are represented by gray (resp. white) blocks. Bottom: The canonical representation of γ1.

whole set of rational numbers Q. The theory for the Stern- Brocot tree is well-studied, so we present here the main definitions that are important for our algorithmic result (see Graham, Knuth, and Patashnik (1994) for further details).

The Stern-Brocot tree is a directed rooted tree TSB = (V (TSB), E(TSB)) such that TSB is an infinite complete binary tree where V (TSB) = Q are the set of vertices (written as irreducible fractions), E(TSB) = {(u, left(u)), (u, right(u)) | u ∈V (TSB)} is the set of edges, and 0

1 is the root. Figure 2 illustrates the structure of the Stern-Brocot tree up to depth 4. Every vertex u in V (TSB) has exactly two children, the left child left(u) and the right child right(u), which are placed from left to right, following the left-to-right order of their children.

The construction of TSB is as follows: we define the boundary relation B ⊆Q∞×Q×Q∞as the smallest set that satisfies that (−1

0, 0 1, 1 0) ∈B, and that if (c1 d1, a b, c2 d2) ∈B, then (c1 d1, c1+a d1+b, a b) ∈B and (a b, a+c2 b+d2, c2 d2) ∈B. It can be shown that every irreducible fraction, except −1

0 and 1 0, appears as the middle component of some triple in B exactly once. With the relation B, we define the functions left, right: Q →Q of TSB by:

left a b

= a + c1 b + d1 and right a b

= a + c2 b + d2

, for every a b ∈Q such that (c1 d1, a b, c2 d2) ∈B. One can check that this relation holds in Figure 2.

Since TSB forms a binary tree and every a b ∈Q is uniquely represented as a vertex in V (TSB), then there is a unique path from the root 0

1 to a b. We can encode this path as a string in {L, R}∗of the left-child (L) and right-child (R) moves from 0

1 to a b. For instance, one can check in Figure 2 that LRL represents −2

3 and RLL represents 1 3. In particular, negative numbers starts with L, positive numbers with R, and 0

1 is represented by the empty string. Furthermore, we can succinctly encode a string in {L, R}∗by its run-length encoding of the contiguous sequences of R an L symbols. For example, the string RLLLLRLLRRRL (which represents 23 108) can be grouped as R1L4R1L2R3L1. In general, for every q ∈Q we can define its SB-encoding:

encSB (q) = ∼[a1,..., an]

where ∼∈{+, −}, n ≥1, and ai ≥1 such that:

• if ∼= + and n is even, then S = Ra1La2... Ran−1Lan; • if ∼= + and n is odd, then S = Ra1La2... Lan−1Ran; • if ∼= −and n is even, then S = La1Ra2... Lan−1Ran; • if ∼= −and n is odd, then S = La1Ra2... Ran−1Lan; and S is the path from 0

1 to q in TSB. In particular, we define the empty array as the SB-encoding of 0

## 1. For example, from Figure 2 one can check that encSB

−2

3

= −[1, 1, 1] and encSB

1

3

= +[1, 2]. It is worth noticing that the SBencoding is directly related to the continuous fraction representation of rational numbers (see Graham, Knuth, and Patashnik (1994))—yet we will present the notion solely as the path of left- and right-child moves in TSB, as this suits our purposes better.

An important property of the SB-encoding of rational numbers is that its size its not much bigger than the irreducible representation of the number. Proposition 1. Given any rational number q = a b and its corresponding SB-encoding ∼[a1,..., an], it holds that Pn i=1 log(1 + ai) ∈O(size(q)). Notice that every array ∼[a1,..., an] uniquely represents a rational number in TSB. For every q ∈Q with encSB (q) = ∼[a1,..., an] we call the rational number pm with encSB (pm) = ∼[a1,..., am] (for 1 ≤m ≤n) the m-th convergent fraction of q. In addition, we say that pm is a strict convergent fraction of q if m < n. For instance,

−1

1 and −1 2 are strict convergent fractions of −2 3 and 1 1 is the only strict convergent fraction of 1

3. One can think of the convergent fractions of a rational number q as the nodes at the turning points in the path to q from the root in TSB. Convergent fractions will be key to our main characterization.

Break links. For learning an unknown finite piecewise function γ with canonical representation r of the form (†), the objective is to identify every interval Ij and the corresponding value γ(Ij). In the next section, we present a learning algorithm that, using the Stern-Brocot tree, constructs r by finding the convergent fractions of each endpoint of the intervals in r. In this subsection, we introduce a notion inside the Stern-Brocot tree, called break links, that we will use as a proxy to find all the values that appear in r.

Formally, given an interval I = ⟨p, q⟩, we denote by bounds(I) = {p, q}, namely, the lower and upper bounds of I. For a finite piecewise function γ with canonical representation r like (†), we define bounds(γ) = {bounds(Ij) | j ≤k}\{−∞, ∞}. That is, bounds(γ) contains the bounding values inside γ except −∞and ∞. Therefore, the main goal in our learning algorithm will be to find all the values in bounds(γ) for γ.

In the following, we denote the unordered interval of two rational numbers p, q as: ⌊p, q⌉= [min(p, q), max(p, q)]. Let γ be a finite piecewise function and (p, q) be an edge in TSB. We say that (p, q) is a break link of γ if p is 0

1 or ⌊p, q⌉ is not monochromatic with respect to γ, meaning that there

19095

<!-- Page 6 -->

exist x, y ∈⌊p, q⌉, such that γ(x)̸ = γ(y). In Figure 2, we show the Stern-Brocot tree up to depth 4 along with the finite piecewise function γ1 introduced in Section 3 where nodes q for which γ(q) = A (resp. B) are represented by gray (resp. white) blocks. One can check that (0

1, 1 1) and (1 2, 2 3) are break links of γ1 but (−1

1, −2 1) and (1 2, 1 3) are not. Next, we present the relation between break links and the convergent fractions of the bounds in a piecewise function γ.

Proposition 2. Given a finite piecewise function γ, (1) for every convergent fraction q of a bound in bounds(γ), there exists a break link (p1, p2) of γ such that q ∈{p1, p2}; and (2) for every break link (p1, p2) of γ at least one among p1 and p2 is a convergent fraction of some bound in bounds(γ).

The previous proposition is crucial for our learning algorithm to find the endpoints in γ. Given that every value in Q is a convergent fraction of itself, (1) implies that, if we find all break links of γ in TSB, then we will have all the elements in bounds(γ). Furthermore, by (2) and Propositions 1 the number of break links of γ will not be bigger than size(γ). In the next section, we will show how to use this connection to learn any finite piecewise function γ.

The Learning Algorithm The goal of this section is to present the learning algorithm that, given a membership oracle MQ and an equivalence oracle EQ of an unknown finite piecewise function γ, computes its representation r of the form (†). The algorithm works by incrementally adding break links of γ until every break link has been discovered by the algorithm. Then, from the break links we construct the final hypothesis. We will start the section by describing the data structure and an algorithm to build a representation from the collected data. Then, we present the learning algorithm and prove its correctness.

Building a consistent representation. As already mentioned, the main strategy of the algorithm is to find all break links (p, q) of γ. Instead of keeping pairs (p, q), we will maintain the points p and q in a list D of the form:

D = (q1, A1), (q2, A2),..., (qm, Am) (‡)

where qi ∈Q and γ(qi) = Ai for every i ≤m, and q1 < q2 <... < qm. Furthermore, every qi is part of a break link of γ, namely, qi ∈{p, q} for some break link (p, q) of γ. We call D the data structure of our learning algorithm.

Our first task for the learning algorithm is to show how to construct a representation r from a given data structure D. Specifically, we say that a representation r is consistent with a data structure D like (‡) if r(qi) = Ai for every i ≤m. For a finite piecewise function γ with canonical representation r like (†), we say that q ∈bounds(γ) is a left-bound (rightbound) of γ if q ∈Ij and q = inf(Ij) (resp. q = sup(Ij)) for some j ≤k. In other words, Ij is of the form [q, p⟩(resp. ⟨p, q]) for some p ∈Q∞. Note that every q ∈bounds(γ) is either a left- or a right-bound of γ or both (e.g., Ij = [q, q]).

So, how do we build a consistent representation r from D? We use a strategy to determine which of the values in D are endpoints in bounds(γ) and, additionally, which are left- or right-bounds (or both). Intuitively, if qi−1 is a descendant of

## Algorithm

1: Construct a representation r from D

Input: A data structure D like (‡). Output: A representation r consistent with D.

1: Procedure ConstructRepresentation(D) 2: r ←∅ 3: ⟨←(, leftBnd ←−∞, currLabel ←A1 4: for i ∈{1,..., m} do 5: if qi−1 is descendant of qi and Ai−1̸ = Ai then 6: r ←r ∪(⟨leftBnd, qi), currLabel) 7: ⟨←[, leftBnd ←qi, currLabel ←Ai 8: if qi is an ancestor of qi+1 and Ai̸ = Ai+1 then 9: r ←r ∪(⟨leftBnd, qi], currLabel) 10: ⟨←(, leftBnd ←qi, currLabel ←Ai+1 11: r ←r ∪(⟨leftBnd, ∞), Am) 12: return r qi in TSB and γ(qi−1)̸ = γ(qi) for some i > 1, then this is evidence that qi ∈bounds(γ) and, furthermore, qi is a leftbound of γ. Similarly, if qi is an ancestor of qi+1 and γ(qi)̸ = γ(qi+1) for some i < m, then qi is a right-bound of γ. This intuition, in fact, is guaranteed to completely characterize bounds(γ) when D contains all break links of γ. Proposition 3. Assume that D like (‡) contains all break links of γ. Then (1) qi is a left-bound of γ iff qi−1 is a descendant of qi and Ai−1̸ = Ai, and (2) qi is a right-bound of γ iff qi is an ancestor of qi+1 and Ai̸ = Ai+1.

In Algorithm 1, we implement this strategy for constructing a representation from D where lines 5-7 encode (1) and lines 8-10 encode (2) plus the border cases (i.e., −∞and ∞) which we resolve in lines 3 and 11. Notice that before D has all break links, ConstructRepresentation(D) will not necessarily produce the correct representation for γ. Nevertheless, as the following result shows, it always produces a consistent representation of D. Theorem 3. Algorithm 1 outputs a representation r that is consistent with D. Moreover, if D contains all break links of γ, then r = γ.

By the previous result, we know that the representation r is always consistent with D and, moreover, if we aim to find all break links, then eventually we will have that r = γ.

Finding all break links. The learning algorithm is presented in Algorithm 2. It receives as input a membership oracle MQ and an equivalence oracle EQ, both compatible with an unknown finite piecewise function γ in C. Its goal is to construct a representation r for γ of the form (†) after a finite number of iterations. This is done by maintaining a data structure D that stores all the break links of γ that have been found up to the current iteration. Since γ is a finite piecewise function, the interval partition I1, I2,..., Ik of Q must be finite and, furthermore, every endpoint q in bounds(γ) has a finite encoding encSB (q). Therefore, by Proposition 2 and Theorem 3, the number of break links of γ must be finite, and, after collecting all of them in D, we can construct a representation r of γ.

## Algorithm

2 works by first adding a pair (0, γ(0)) into D (line 1), and then, at each iteration, adding the components

19096

<!-- Page 7 -->

## Algorithm

2: The Learning Algorithm

Input: A Membership Oracle MQ and an Equivalence Or- acle EQ compatible with some finite p.w. function γ. Output: A representation r equivalent to γ.

1: D ←{(0 1, MQ(0 1))} 2: while true do 3: r ←ConstructRepresentation(D) 4: (ans, q∗) ←EQ(r) 5: if ans = true then 6: return r 7: r ←FindClosestAncestor(q∗, D) 8: (p, q) ←FindBreakLink(r, q∗, D) 9: D ←D ∪{(p, MQ(p)), (q, MQ(q))}

## Algorithm

3: Find a break link of γ from a node in TSB Input: An origin node r, counterexample q∗and array D. Output: A break link (p, q) of γ not present in D.

1: Procedure FindBreakLink(r, q∗, D) 2: if q∗< r then 3: (p, q) ←SearchLeft(r, q∗, D) 4: else 5: (p, q) ←SearchRight(r, q∗, D) 6: return (p, q)

p and q of a new break link (p, q) of γ into D, along with the labels γ(p) and γ(q) (line 9). Each iteration does the following: First, it constructs a representation r using Algorithm 1 and the array D (line 3). Then, it asks the equivalence oracle EQ whether r = γ; if it is true, the algorithm ends (lines 4– 6). If not, this means that we are missing some break link in D and, then, in lines 7–8 the algorithm searches the new break link for γ in TSB. Finally, in line 9, it adds the information of the new break link into D, maintaining the array ordered, and avoiding adding any existing tuple again. By Theorem 3, we know that if the equivalence oracle returns a counterexample q∗, then D is missing some break link of γ. Thus, if we prove that Algorithm 2 always adds a new break link in lines 7–9, then its correctness will follow.

The question that remains to answer is where to find a new break link given the counterexample q∗. Towards this goal, Algorithm 2 first computes the closest ancestor of q∗in D (line 7), namely, the element r ∈{q1,..., qm} that is the closest ancestor to q∗in TSB assuming that D has form (‡). One can show that one can compute method FindClosestAncestor(q∗, D) in time O(|D|) and without calling MQ or EQ. To this end, we show that, if D is missing a break link, then one can be found in the left branch or right branch that stems from r, depending on whether q∗< r or q∗> r, respectively. The case q∗= r would never happen since D is assumed to be consistent with γ.

Proposition 4. Assume that r̸ = γ in line 5 of Algorithm 2 and r is the closest ancestor of q∗in D. Then there is a missing break link in the left branch of r when q∗< r, or in the right branch when q∗> r.

The method FindBreakLink(r, q∗, D) in Algorithm 3 ex- ploits Proposition 4 to find a break link. Specifically, it works as follows: given an origin node r, a counterexample q∗and array D, it searches over the left branch or right branch that stem from r using two subroutines searchLeft and searchRight, respectively (see (Hagedorn et al. 2025) for the implementation of both methods). Each subroutine uses galloping search (Bentley and Yao 1976) and membership queries to efficiently find a break link over the branches. If the distance from r to an undiscovered break link of γ is k, then the number of membership queries it takes to find this break link is in O(log(k)). Theorem 4. Assume that r̸ = γ in line 5 of Algorithm 2 and r is the closest ancestor of q∗that appears in D. The method FindBreakLink(r, q∗, D) returns an undiscovered break link (p, q) of γ not present in D making at most O(log(k)) membership queries to MQ where k is the distance in TSB between r and p.

Finally, let us analyze the number of membership and equivalence queries needed to learn an unknown finite piecewise function γ using Algorithm 2. The number of membership queries is the total of queries to MQ made in all calls to FindBreakLink. We see that each q ∈bounds(γ) with SB-encoding ∼[a1,..., an], by Proposition 2 and Theorem 4, contributes O(log(1 + ai)) calls to find the break link at ai. Thus, the total number of membership queries is in O(Pn i=1 log(1 + ai)) for q and, by Proposition 1, we find that the number of membership queries is in O(size(γ)).

The number of equivalence queries used in Algorithm 2 is bounded by the number of iterations, which is equal to the number of break links for γ. As we reasoned above, this number is in O(size(γ)) by Proposition 1. Theorem 5. Algorithm 2 returns the canonical representation r of a finite piecewise function γ using no more than O(size(γ)) membership queries and no more than O(size(γ)) equivalence queries.

Conclusions and Future Work We presented a MAT learning algorithm for finite piecewise functions that directly applies to the learning of symbolic automata with interval formulas. Furthermore, this algorithm is efficient in the sense that it takes at most a linear number of queries to the Teacher concerning the size of the concept.

The techniques developed in this paper could have the potential to work in other problems regarding MAT learning. One open problem is to learn a finite piecewise function over Qk (i.e., k-dimensions) where a finite number of square regions specify the function. This problem also has applications in symbolic automata, where, for example, time series are sequences of data tuples (e.g., the sensor measures temperature and humidity together). Further, the techniques proposed in this paper could have application in learning timed automata (An et al. 2020), where clock conditions can be seen as a special case of finite piecewise functions.

19097

<!-- Page 8 -->

## Acknowledgements

The work of Mu˜noz and Riveros was supported by ANID – Millennium Science Initiative Program – Code ICN17 002. Riveros was also supported by ANID Fondecyt project 1230935. The work of Toro Icarte was supported by the National Center for Artificial Intelligence CENIA FB210017 (Basal ANID) and Fondecyt project 11230762.

## References

An, J.; Chen, M.; Zhan, B.; Zhan, N.; and Zhang, M. 2020. Learning One-Clock Timed Automata. In Biere, A.; and Parker, D., eds., Tools and Algorithms for the Construction and Analysis of Systems, 444–462. Cham: Springer International Publishing. ISBN 978-3-030-45190-5. Angluin, D. 1980. Inductive inference of formal languages from positive data. Information and Control, 45(2): 117– 135. Angluin, D. 1987. Learning regular sets from queries and counterexamples. Information and Computation, 75(2): 87– 106. Argyros, G.; and D’Antoni, L. 2018. The Learnability of Symbolic Automata. In Chockler, H.; and Weissenbacher, G., eds., Computer Aided Verification, 427–445. Cham: Springer International Publishing. ISBN 978-3-319-96145- 3. Bentley, J. L.; and Yao, A. C. 1976. An Almost Optimal Algorithm for Unbounded Searching. Inf. Process. Lett., 5(3): 82–87. Brocot, A. 1861. Calcul des rouages par approximation, nouvelle m´ethode, Revue chronom´etrique. Journal des horlogers, scientifique et pratique, 186–194. Corazza, J.; Gavran, I.; and Neider, D. 2022. Reinforcement learning with stochastic reward machines. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, 6429–6436. D’Antoni, L.; and Veanes, M. 2014. Minimization of Symbolic Automata. volume 49, 541–553. Drews, S.; and D’Antoni, L. 2017. Learning Symbolic Automata. In Legay, A.; and Margaria, T., eds., Tools and Algorithms for the Construction and Analysis of Systems, 173– 189. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-662-54577-5. Giatrakos, N.; Alevizos, E.; Artikis, A.; Deligiannakis, A.; and Garofalakis, M. 2020. Complex event recognition in the big data era: a survey. The VLDB Journal, 29(1): 313–352. Gold, E. M. 1967. Language identification in the limit. Information and Control, 10(5): 447–474. Graham, R. L.; Knuth, D. E.; and Patashnik, O. 1994. Concrete Mathematics: A Foundation for Computer Science. Reading, MA: Addison-Wesley, second edition. ISBN 0201558025 9780201558029 0201580438 9780201580433 0201142368 9780201142365. Hagedorn, S.; Mu˜noz, M.; Riveros, C.; and Toro Icarte, R. 2025. Active learning of symbolic automata over rational numbers. CoRR.

Hamilton, J. D. 2020. Time series analysis. Princeton university press. Hasanbeig, M.; Jeppu, N. Y.; Abate, A.; Melham, T.; and Kroening, D. 2021. Deepsynth: Automata synthesis for automatic task segmentation in deep reinforcement learning. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 7647–7656. Katzouris, N.; and Paliouras, G. 2022. Learning Automata- Based Complex Event Patterns in Answer Set Programming. In International Conference on Inductive Logic Programming, 52–68. Springer. Mens, I.-E.; and Maler, O. 2015. Learning Regular Languages over Large Ordered Alphabets. Logical Methods in Computer Science, Volume 11, Issue 3. Pitt, L.; and Warmuth, M. K. 1993. The minimum consistent DFA problem cannot be approximated within any polynomial. J. ACM, 40(1): 95–142. Roy, R.; Gaglione, J.-R.; Baharisangari, N.; Neider, D.; Xu, Z.; and Topcu, U. 2023. Learning interpretable temporal properties from positive examples only. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 6507–6515. Shvo, M.; Li, A. C.; Icarte, R. T.; and McIlraith, S. A. 2021. Interpretable sequence classification via discrete optimization. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 9647–9656. Stern, M. 1858. Ueber eine zahlentheoretische Funktion. Journal f¨ur die reine und angewandte Mathematik, 55: 193– 220. Toro Icarte, R.; Klassen, T. Q.; Valenzano, R.; Castro, M. P.; Waldie, E.; and McIlraith, S. A. 2023. Learning reward machines: A study in partially observable reinforcement learning. Artificial Intelligence, 323: 103989. Vaandrager, F.; Garhewal, B.; Rot, J.; and Wißmann, T. 2022. A new approach for active automata learning based on apartness. In International Conference on Tools and Algorithms for the Construction and Analysis of Systems, 223– 243. Springer. van Noord, G.; and Gerdemann, D. 2001. Finite State Transducers with Predicates and Identities. Grammars, 4. Veanes, M. 2013. Applications of Symbolic Finite Automata. In Konstantinidis, S., ed., Implementation and Application of Automata, 16–23. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-642-39274-0. Veanes, M.; Hooimeijer, P.; Livshits, B.; Molnar, D.; and Bjorner, N. 2012. Symbolic finite state transducers: Algorithms and applications. In Proceedings of the 39th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages, 137–150.

19098
