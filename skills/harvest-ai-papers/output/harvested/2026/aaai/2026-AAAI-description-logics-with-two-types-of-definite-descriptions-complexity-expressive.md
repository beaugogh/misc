---
title: "Description Logics with Two Types of Definite Descriptions: Complexity, Expressiveness, and Automated Deduction"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39014
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39014/42976
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Description Logics with Two Types of Definite Descriptions: Complexity, Expressiveness, and Automated Deduction

<!-- Page 1 -->

Description Logics with Two Types of Definite Descriptions:

Complexity, Expressiveness, and Automated Deduction

Michał Socha´nski*1, Przemysław Andrzej Wał˛ega*1,2, Michał Zawidzki*1

1Department of Logic, University of Łód´z, Poland 2School of Electronic Engineering and Computer Science, Queen Mary University of London, United Kingdom {michal.sochanski,przemyslaw.walega,michal.zawidzki}@filhist.uni.lodz.pl, p.walega@qmul.ac.uk

## Abstract

Definite descriptions are expressions of the form “the unique x satisfying property C,” which allow reference to objects through their distinguishing characteristics. They play a crucial role in ontology and query languages, offering an alternative to proper names (IDs), which lack semantic content and serve merely as placeholders. In this paper, we introduce two extensions of the well-known description logic ALC with local and global definite descriptions, denoted ALCιL and ALCιG, respectively. We define appropriate bisimulation notions for these logics, enabling an analysis of their expressiveness. We show that although both logics share the same tight ExpTime complexity bounds for concept and ontology satisfiability, ALCιG is strictly more expressive than ALCιL. Moreover, we present tableau-based decision procedures for satisfiability in both logics, provide their implementation, and report on a series of experiments. The empirical results demonstrate the practical utility of the implementation and reveal interesting correlations between performance and structural properties of the input formulas.

## Introduction

Definite descriptions (DDs)—expressions of the form “the unique x satisfying property C”—serve as complex terms identifying individuals via uniquely characterising properties. Their study originates in philosophical logic, where the main focus has been on semantics (Russell 1905; Pelletier and Linsky 2005; Hilbert and Bernays 1968; Rosser 1978; Lambert 2001). In recent decades, DDs have drawn renewed interest in formal logic, including classical, intuitionistic, and temporal systems (Fitting and Mendelsohn 2023; Indrzejczak 2023a,b; Indrzejczak and Kürbis 2023; Indrzejczak and Petrukhin 2024; Indrzejczak and Zawidzki 2021, 2023a,b; Kürbis 2019a,b; Kürbis 2025; Orlandelli 2021). This line of research has also led to reasoning systems supporting DDs, including KeYamera X (Bohrer, Fernández, and Platzer 2019), PROVER9 (Oppenheimer and and 2011), and Isabelle/HOL (Benzmüller and Scott 2020).

Of particular relevance is the application of DDs in Knowledge Representation and Reasoning (KRR), where

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

they enable precise identification of individuals while encoding structural constraints—a capability surpassing that of non-descriptive names such as opaque IDs (Borgida, Toman, and Weddell 2016a,b, 2017; Toman and Weddell 2016, 2018, 2019a,b). Within description logics (DLs), this has motivated the introduction of DD operators into the logical language (Areces, Koller, and Striegnitz 2008; Ren, van Deemter, and Pan 2010; Neuhaus, Kutz, and Righetti 2020; Toman and Weddell 2019a). In particular, Artale et al. (2021) introduced concepts {ιC}, denoting the singleton containing the unique individual satisfying concept C, or the empty set if no such individual exists. This allows for succinct representation of concepts such as:

{ι(building ⊓∀tallThan.¬building)}, which captures the expression “the tallest building.” We refer to such constructs as local DDs.

We contrast local DDs with newly introduced global DDs of the form ιC.D, expressing that “the individual satisfying C also satisfies D.” For example, the concept ι(building ⊓∀tallThan.¬building).∃locIn.{Dubai} formalises the statement “the tallest building is located in Dubai.” This type of DDs builds on recent developments in modal and hybrid logics (Wał˛ega and Zawidzki 2023; Wał˛ega 2024; Indrzejczak and Zawidzki 2023a).

Despite growing interest in DDs within DLs, key foundational questions have remained open. In particular, the computational complexity, expressive power, and reasoning procedures for ALC extended with local or global DDs have not been systematically studied. While the complexity analysis proves relatively straightforward, characterising expressive power is significantly more challenging. Notably, devising suitable bisimulations for such logics is non-trivial. Existing bisimulations are for local DDs only and assume the presence of nominals and the universal role—features that simplify the task (Artale et al. 2021). To the best of our knowledge, bisimulations for ALC with DDs alone have not been proposed. Moreover, no existing DL reasoning system appears to support DDs, despite their practical motivation.

This paper aims to address these gaps. Our main contributions are as follows:

• We introduce three extensions of ALC with definite descriptions: ALCιL (local), ALCιG (global), and ALCι (both). These are formalised in Section 2.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19371

<!-- Page 2 -->

• To analyse expressivity, we define bisimulations for each logic in Section 3. They rely on novel, non-trivial conditions, which we show can be reduced to standard ALC bisimulation checks. We also provide algorithms for this reduction.

• Using these bisimulations, we study expressivity via equivalence-preserving concept translations. We show that ALCιL is strictly less expressive than ALCιG, while ALCιG and ALCι are equally expressive. All three are ExpTime-complete for concept and ontology satisfiability.

• In Section 4, we present tableau-based decision procedures for all three logics. Despite differing semantics of the two DD types, similar tableau rules suffice to handle both.

• We implement these procedures and evaluate them on custom benchmarks (Section 5). Results confirm their viability and show links between structural features of DDs and reasoning performance.

Description Logics with Definite

Descriptions Syntax Let NC, NR, and NI be countably infinite, pairwise disjoint sets of atomic concept names, role names, and individual names, respectively. ALCι concepts C are defined by the following grammar:

C:= A | ¬C | (C ⊓C) | ∃r.C | {ιC} | ιC.C, where A ∈NC and r ∈NR. Standard abbreviations are used for other logical constructs: ⊥:= A ⊓¬A, ⊤:= ¬⊥, C ⊔D:= ¬(¬C ⊓¬D), and ∀r.C:= ¬∃r.¬C. An ALCι concept inclusion (CI) is a formula of the form C ⊑D, where C and D are ALCι concepts. We write C ≡D as shorthand for C ⊑D and D ⊑C. An assertion is either a: C or r: (a1, a2), where a, a1, a2 ∈NI, C is a concept, and r ∈NR. An ABox A is a finite set of assertions; a TBox T is a finite set of concept inclusions. An ontology O consists of a TBox and an ABox. Where clear from context, we refer simply to atomic concepts, roles and individuals without mentioning names explicitly.

The description logic ALCιL is the fragment of ALCι that includes local definite descriptions {ιC} but excludes global definite descriptions ιC.D. Conversely, ALCιG includes only global descriptions.

Semantics An interpretation is a pair I = (∆I, ·I) consisting of a non-empty domain ∆I and a function that maps: (i) atomic concepts A ∈NC to subsets of ∆I, (ii) roles r ∈NR to subsets of ∆I × ∆I, (iii) individuals a ∈NI to elements of ∆I. This function extends to complex concepts:

(¬C)I:= ∆I \ CI, (C ⊓D)I:= CI ∩DI,

(∃r.C)I:= {d ∈∆I | (d, e) ∈rI for some e ∈CI},

({ιC})I:=

{d}, if CI = {d} for some d ∈∆I, ∅, otherwise,

(ιC.D)I:=

∆I, if CI = {d} ⊆DI for some d ∈∆I, ∅, otherwise.

A concept C is satisfied in I if CI̸ = ∅, and satisfiable if such I exists. A pointed interpretation is a pair (I, d) with d ∈∆I. We write (I, d) ≡L (J, e) if for every concept C from a logic L, we have d ∈CI iff e ∈CJ. Satisfaction of axioms of ontology O in I, written I |= α, is defined as:

I |= C ⊑D iff CI ⊆DI,

I |= a: C iff aI ∈CI,

I |= r: (a1, a2) iff (aI

1, aI 2) ∈rI. Interpretation I is a model of an ontology O (written I |= O) if I |= α for all α ∈O. An ontology is satisfiable if it has a model, and a concept C is satisfiable w.r.t. an ontology O if C is satisfied in a model of O.

We compare the expressive power of description logics via equivalence-preserving translations between their concepts. A logic L is not more expressive than L′, denoted L ≤L′, if every L-concept has an equivalent L′-concept. It is strictly less expressive if L ≤L′ but L′̸ ≤L, and equally expressive if both L ≤L′ and L′ ≤L.

## 3 Expressiveness and Complexity

We analyse and compare the logics ALCιL, ALCιG, and ALCι. Although their expressive power differs, all three have the same computational complexity. Theorem 1. In ALCιL, ALCιG, and ALCι, both concept and ontology satisfiability are ExpTime-complete.

Proof sketch. For upper bounds, we reduce ALCι ontology satisfiability to that of ALCOι u, which is ExpTimecomplete (Artale et al. 2021, Thm. 2). Local DDs {ιC} are allowed in ALCOι u, and each global DD {ιC.D} is replaced with ∃u.({ιC}⊓D), where u is the universal role. This polynomial reduction constructs an equivalent ontology.

For lower bounds, it suffices to show ExpTime-hardness for concept satisfiability in ALCιL and ALCιG. We give logspace reductions from satisfiability of an ALC concept C w.r.t. a TBox T, known to be ExpTime-complete (Baader 2003, Thm. 3.27). For ALCιL, we construct C′ as:

C ⊓d

(D⊑E)∈T ((¬D ⊔E) ⊓{ι (¬(¬D ⊔E) ⊔AD⊑E)}), where each AD⊑E is a fresh atomic concept. Then C′ is satisfiable iff C is satisfiable w.r.t. T. For ALCιG, we replace the above local definite descriptions with the following: AD⊑E ⊓ι (¬(¬D ⊔E) ⊔AD⊑E).⊤.

Despite having the same complexity, the logics differ in expressive power. We first observe that local descriptions can be encoded using global ones: Proposition 2. There is an exponential translation of ALCιL concepts into equivalent ALCιG concepts, and a polynomial translation of ALCιL ontologies into conservative extensions in ALCιG.

Proof sketch. The exponential translation replaces {ιC} with C ⊓ιC.⊤. The polynomial version replaces {ιC} with AC ⊓ιAC.⊤and adds axioms AC ≡C.

We conclude that ALCιL ≤ALCιG = ALCι. Next, we will introduce bisimulations and show that ALCιL < ALCιG. For this, we will exploit the following notion of names of individuals in an interpretation:

19372

<!-- Page 3 -->

a b c d e

A

I J

Z

**Figure 1.** Maximal ALCιL bisimulation between I and J

Definition 3. Let ∆′ ⊆∆I. The set Names(∆′, I) consists of all ALC concepts C, with CI = {d} for some d ∈∆′.

Example 4. Let ∆I = {a, b} with AI = ∅, and ∆J = {c, d, e} with AJ = {e} (see Figure 1). Then Names({a, b}, I) = Names({c, d}, J) = ∅, since no ALC concept uniquely identifies an individual in either set. However, Names({c, d, e}, J) is non-empty, as it contains for example A, ¬¬A, and A ⊔∃r.⊤.

We now define bisimulations for ALCιL and ALCιG. Note that by Proposition 2, a separate definition for ALCι is unnecessary.

Definition 5. An ALCιL bisimulation between interpretations I and J is a relation Z ⊆∆I × ∆J such that Z = ∅ or, for all (d, e) ∈Z, every atomic concept A, and role r:

Atom d ∈AI iff e ∈AJ, Forth if (d, d′) ∈rI, then there exists e′ such that (e, e′) ∈ rJ and (d′, e′) ∈Z, Back if (e, e′) ∈rJ, then there exists d′ such that (d, d′) ∈ rI and (d′, e′) ∈Z, NamesL Names(Dom(Z), I) = Names(Rng(Z), J).

An ALCιG bisimulation is defined identically, except that NamesL is replaced with:

NamesG Names(∆I, I) = Names(∆J, J).

We write (I, d) ∼L (J, e) if (d, e) ∈Z for some Lbisimulation Z, where L ∈{ALCιL, ALCιG}.

Figure 1, presents the maximal ALCιL bisimulation Z between I and J It satisfies NamesL, as Names(∆I, I) = Names(∆J, J) = ∅. However, there is no ALCιG bisimulation betwee I and J, as NamesG fails: A ∈ Names(∆J, J) but A /∈Names(∆I, I).

It is worth observing that our bisimulations differ from those used for ALCOι u by Artale et al. (2021), which rely on totality and “counting up to one” via the universal role and nominals. These conditions are too strong for ALCιL, as illustrated in Figure 1. While our NamesL and NamesG conditions are non-standard and appear to require quantification over all concepts, we show in Algorithms 1 and 2 how they can be verified procedurally. Before that, we prove that our bisimulations preserve concept satisfiability, and that the converse holds for ω-saturated1 interpretations.

Theorem 6. For all pointed interpretations (I, d) and (J, e), and both L ∈{ALCιL, ALCιG} the following hold:

1. if (I, d) ∼L (J, e), then (I, d) ≡L (J, e),

1See, e.g., Chang and Keisler (1992) for the definition.

2. if (I, d) ≡L (J, e) and I, J are ω-saturated, then (I, d) ∼L (J, e).

Proof sketch. We first prove Statement 1 by induction on the structure of L-concepts C, showing d ∈CI if and only if e ∈CJ. If C is atomic, or of the form ¬D, D ⊓E, or ∃r.D, the result follows from conditions Atom, Forth, and Back, as in the standard ALC case (Baader et al. 2017). If C = {ιD} and d ∈CI, then DI = {d}, so D ∈Names(Dom(Z), I). By the inductive hypothesis, e ∈DJ, and by NamesL, D ∈Names(Rng(Z), J), hence DJ = {e}, and e ∈({ιD})J. The converse direction is analogous. If C = ιD.E and d ∈CI, then {D, D ⊓E} ⊆Names(∆I, I). By NamesG, these concepts are also in Names(∆J, J), implying e ∈(ιD.E)J. The converse again is similar.

For Statement 2, we begin with L = ALCιG. Since (I, d) ≡ALCιG (J, e) implies (I, d) ≡ALC (J, e), and I, J are ω-saturated, standard results for ALC (Baader et al. 2017) imply that there exists an ALC-bisimulation Z with (d, e) ∈Z. To show that Z is an ALCιG-bisimulation, it remains to prove NamesG. If C ∈Names(∆I, I), then d ∈(ιC.⊤)I, hence e ∈(ιC.⊤)J, so C ∈Names(∆J, J). The reverse direction is symmetric. For L = ALCιL, we define Z:= {(k, l) ∈∆I × ∆J | (I, k) ≡ALCιL (J, l)}, so (d, e) ∈Z. Conditions Atom, Forth, and Back hold by standard arguments for ALC bisimulations, extended with a translation of ALCιL into first-order logic. To show NamesL, assume C ∈Names(Dom(Z), I). Then some d′ ∈Dom(Z) satisfies d′ ∈({ιC})I. Since (d′, e′) ∈ Z for some e′ ∈∆J, we conclude e′ ∈({ιC})J, so C ∈Names(Rng(Z), J). Thus, Names(Dom(Z), I) ⊆ Names(Rng(Z), J). The reverse inclusion follows analogously, proving equality.

We now apply our bisimulations to show that ALCιL < ALCιG. Combined with Proposition 2, this yields the following expressiveness result.

Theorem 7. The following expressive power relations hold: ALCιL < ALCιG = ALCι.

Proof. By Proposition 2, it suffices to show ALCιG̸ ≤ ALCιL. Assume, for contradiction, that ιA.⊤is equivalent to some ALCιL concept C. Consider the interpretations I and J from Example 4, with the maximal ALCιL bisimulation Z shown in Figure 1. Since (I, a) ∼ALCιL (J, c), Theorem 6 gives a ∈CI iff c ∈CJ. However, by construction, I̸ |= ιA.⊤(a) and J |= ιA.⊤(c), i.e., a /∈CI and c ∈CJ —a contradiction.

While our bisimulations accurately characterise concept equivalence, we have not yet addressed how to decide bisimilarity between two pointed interpretations. We now present an algorithm for computing the maximal bisimulation between two finite interpretations, identifying all bisimilar pairs. The following notion plays a central role:

Definition 8. Let ∆′ ⊆∆I. The set NamedInd(∆′, I) of named individuals comprises all d ∈∆′ such that d ∈CI for some C ∈Names(∆′, I).

19373

<!-- Page 4 -->

For instance, in the interpretations I and J from Example 4, we have NamedInd(∆I, I) = ∅and NamedInd(∆J, J) = {e}.

In contrast to computing names, identifying named individuals is straightforward: they are exactly those not ALCbisimilar to any other individual in the interpretation. The next theorem links named individuals to names, showing that once the named individuals are known, one can determine whether two interpretations have the same names. Below, we call relation Z total if it is both left- and right-total.

Theorem 9. Let I and J be finite interpretations and let ∆′ ⊆∆I and ∆′′ ⊆∆J. If Names(∆′, I)̸ = ∅̸ = Names(∆′′, J), then Names(∆′, I) = Names(∆′′, J) if and only if the maximal ALC-bisimulation Z between I and J is a total relation and the restriction of Z to NamedInd(∆′, I) × NamedInd(∆′′, J) is also total.

Proof sketch. Assume that Names(∆′, I) = Names(∆′′, J)̸ = ∅. To show that the restriction of Z to NamedInd(∆′, I) × NamedInd(∆′′, J) is total, suppose for contradiction that some d ∈NamedInd(∆′, I) has no Zrelated counterpart in NamedInd(∆′′, J). Then there exists C ∈Names(∆′, I) such that CI = {d} and CJ = {e} for some e ∈∆′′. Since (d, e) /∈Z, there exists an ALC concept D with d ∈DI but e /∈DJ, so C⊓D ∈Names(∆′, I) but C ⊓D /∈Names(∆′′, J)—a contradiction. To show that Z is total, suppose some d ∈∆I \ NamedInd(∆′, I) has no Z-related individual in ∆J. As Names(∆′′, J)̸ = ∅, there exists e∗∈NamedInd(∆′′, J) with CJ = {e∗} for some C. For each e ∈∆J \ {e∗}, choose Ce with e ∈CJ e and d /∈CI e, and let D = C ⊔d e̸=e∗¬Ce. Then DJ = {e∗}, so D ∈Names(∆′′, J) = Names(∆′, I), and since d ∈DI, we get d ∈NamedInd(∆′, I)—a contradiction.

Assume Z and its restriction are total. Suppose, for contradiction, that C ∈Names(∆′, I) but C /∈Names(∆′′, J). Then CI = {d} for some d ∈NamedInd(∆′, I), and there exists e ∈NamedInd(∆′′, J) with (d, e) ∈Z and e ∈CJ. Since C /∈Names(∆′′, J), there is e′̸ = e with e′ ∈CJ. By totality, there exists d′ ∈∆I with (d′, e′) ∈Z. If d′̸ = d, then {d, d′} ⊆CI contradicts uniqueness. If d′ = d, and for D ∈Names(∆′′, J), DJ = {e}, then d ∈DI but e /∈DJ, so (d, e′) ∈Z contradicts that Z is a bisimulation.

In Algorithm 1, we use Theorem 9 to compute the maximal ALCι bisimulation between finite interpretations I and J. The algorithm first computes three maximal ALC bisimulations: Z, ZI, and ZJ, which are used to determine the sets NI = NamedInd(∆I, I) and NJ = NamedInd(∆J, J), as well as N Z

I = NamedInd(Dom(Z), I) and N Z

J = NamedInd(Rng(Z), J). If both N Z

I and N Z

J are empty, then NamesL holds and the algorithm returns Z. If only one is empty, then NamesL fails, and the algorithm returns ∅. Otherwise, Theorem 9 provides an equivalent condition for NamesL: if it holds, the algorithm returns Z; otherwise, it returns ∅. For example, when applied to I and J from Figure 1, the algorithm returns the bisimulation Z shown therein.

## Algorithm

1: Maximal ALCιL-bisimulation

Input: interpretations I and J Output: maximal ALCιL bisimulation for I and J

1 Z:= MAXBSIMALC(I, J);

2 ZI:= MAXBSIMALC(I, I);

3 ZJ:= MAXBSIMALC(J, J);

4 NI:= {d ∈∆I | (d, e)̸ ∈ZI for all e̸ = d in ∆I};

5 NJ:={d ∈∆J |(d, e)̸ ∈ZJ for all e̸ = d in ∆J };

6 N Z I:= NI ∩Dom(Z);

7 N Z J:= NJ ∩Rng(Z);

8 if N Z I = ∅= N Z

J then return Z;

9 if N Z I = ∅̸ = N Z

J or N Z

I̸ = ∅= N Z

J then return ∅;

10 if Z is total over ∆I × ∆J and Z ∩(N Z I × N Z

J) is total over N Z

I × N Z

J then return Z;

11 else return ∅;

To compute the maximal ALCι bisimulation, we introduce Algorithm 2 which modifies Algorithm 1 by replacing Lines 6 and 7 with the following:

6 N Z I:= NI; 7 N Z J:= NJ;

We can show that both algorithms are correct:

Theorem 10. Algorithms 1 and 2 return, respectively, the maximal ALCιL and ALCι bisimulations for I and J.

Proof. The argumentation exploits Theorem 9, which provides the necessary condition for the bisimulation checks. What remains is to justify that NI = NamedInd(∆I, I) and NJ = NamedInd(∆J, J). This follows from the Hennessy-Milner property for ALC bisimulations and the finiteness of I and J. Specifically, if d ∈NI, then for every e̸ = d, there exists an ALC concept Ce such that d ∈CI e and e /∈CI e. Let D = d e̸=d Ce; then DI = {d}, so d ∈NamedInd(∆I, I). Conversely, if d /∈NI, then there exists e̸ = d such that (I, d) ∼ALC (I, e), and thus d satisfies exactly the same ALC concepts as e, implying d /∈NamedInd(∆I, I). The argument for NJ = NamedInd(∆J, J) is analogous.

Tableaux Systems In this section, we present tableau calculi TABALCιL, TABALCιG, and TABALCι, for all three logics. The first two share rules for common constructs, but differ in handling local and global definite descriptions, whereas TABALCι combines these systems.

Rules Given a concept C (optionally with ontology O), our calculi return sat if C is satisfiable (w.r.t. O), and unsat otherwise. Rules are applied to assertions to incrementally build a tableau tree. The root contains a: C, where a is fresh and does not occur in O. A branch B is a path from root to leaf; if B′ extends B, we write B ⊆B′. If it does not lead to confusion, we treat branches as sets of assertions. For an individual a and branch B, the theory of a, written ThB(a), is {C | a: C ∈B}; we say a satisfies C on

19374

<!-- Page 5 -->

ABox rules:

(ABoxI) a: C ∈ABox a: C (ABoxr) r(a, a′) ∈ABox r(a, a′)

TBox rule:

(T Box) C ⊑D ∈T Box, a: E a: ¬(C ⊓¬D)

Clash rule:

(⊥) a: C, a: ¬C

⊥

Propositional rules:

(¬¬) a: ¬¬C a: C (⊓) a: C ⊓D a: C, a: D (¬⊓) a: ¬(C ⊓D) a: ¬C | a: ¬D

Role rules:

(∃r) a: ∃r.C b: C, r: (a, b) (¬∃r) a: ¬∃r.C, r: (a, a′)

a′: ¬C

Global definite description rules:

(ιg

1) a: ιC.D b: C, b: D (ιg

2) a: ιC.D, a′: C, a′′: C, a′: E a′′: E

(¬ιg) a: ¬ιC.D, a′: E a′: ¬C | a′: ¬D | b: C, b: Ag

C, b′: C, b′: ¬Ag

C

(cutg ι) a: ιC.D, a′: E a′: C | a′: ¬C

Local definite description rules:

(ιℓ

1) a: {ιC} a: C (ιℓ

2) a: {ιC}, a′: C, a′′: C, a′: D a′′: D

(¬ιℓ) a: ¬{ιC} a: ¬C | a: ¬AC, b: C, b: AC

(cutℓ ι) a: {ιC}, a′: D a′: C | a′: ¬C

∗b, b′ occurring in the conclusion of a rule are fresh.

**Figure 2.** Rules of TABALCι

B if a: C ∈B. A rule has the form Pr Con1|···|Conm, with m the branching factor. Rules are deterministic if m = 1, and branching otherwise. The calculus’s branching factor is the largest m among its rules. A rule (r) applies to premise Pr if (i) it is not blocked, (ii) no conclusion already appears on the branch, and (iii) the branch is open. A branch is closed if a clash occurs; otherwise, it is open. It is saturated if open and no rules are applicable.

**Figure 2.** lists the rules of TABALCι. Those for standard ALC constructs are omitted here. We highlight the handling of DDs and the blocking condition for (∃r). Blocking. Rule (∃r) is blocked for a: ∃r.C if:

(block∃) There exists an individual a′ on B such that a′:

C ∈B and a′: ¬D ∈B for all D with a: ¬∃r.D ∈B.

In that case, a′ serves as a proxy r-successor of a. Blocking can be lifted if new a: ¬∃r.E assertions are added such that a′: E /∈B. This is known as pattern-based blocking (Kaminski and Smolka 2009). Global DDs. Rule (ιg

1) introduces a fresh individual satisfying both C and D, unless an existing one already satisfies C, in which case only D is propagated (to the least such individual w.r.t. lexicographic order, if needed). Rule (ιg

2) ensures uniqueness by merging the theories of any two individuals satisfying C. Rule (¬ιg) enforces non-uniqueness: for each individual a′, at least one of the following holds: (i) a′: ¬C, (ii) a′: ¬D, or (iii) two distinct individuals satisfy C. In the third case, further applications to a′: ¬ιC.E are blocked. Rule (cutg ι) ensures decisiveness: every individual satisfies either C or ¬C for any positive DD ιC.D. The rule is crucial for the completeness of TABALCι. For example, the tableau for the unsatisfiable concept (ι¬(C ⊓D).⊤) ⊓(ιC.¬D) ⊓(ιD.¬C) fails to close without (cutg ι). Local DDs. Local DDs are handled similarly, except for negation. While ¬ιC.D enforces non-uniqueness globally, ¬ιC does so locally, i.e., relative to the current individual. Rule (¬ιℓ) ensures either the current individual does not satisfy C or some other individual does. The right branch does not introduce new individuals when (¬ιℓ) is applied to a′: ¬{ιC}—only a′: ¬AC is added in the right conclusion. In both negated-DD rules, Ag

C or AC is a fresh atom (not in the input) determined by C. Priorities and Confluence. Rules are applied in fixed order: (⊥) has the highest, (∃) the lowest priority. As formulas are never removed, the calculus is cumulative; all rules are invertible, ensuring confluence: rule order may affect derivation length but not outcome.

Correctness We prove that TABALCι—and so also TABALCιG and TABALCιL—is sound, complete, and terminating. Recall that TABALCι is sound if, for any ALCιconcept C (and ontology O), it returns unsat only if C is unsatisfiable (w.r.t. O). It is complete if, whenever it returns sat, C is indeed satisfiable (w.r.t. O). To establish soundness, we show that rules of TABALCι preserve satisfiability:

Lemma 11. Let (r) be a rule of TABALCι applied to a branch B, and let B1,..., Bn ⊇B be the resulting branches. If B is satisfiable, then so is some Bi for i ∈{1,..., n}.

Proof sketch. The proof proceeds by case analysis on the rules. We illustrate it using the most complex case, (¬ιg). Let Pr = {a: ¬ιC.D, a′: E} be satisfiable. Then a ∈(¬ιC.D)I and a′ ∈EI, meaning no unique individual satisfies both C and D. We have three cases: (i) a′ /∈CI, so a′ ∈(¬C)I and Pr ∪{a′: ¬C} is satisfiable. (ii) a′ /∈DI, so a′ ∈(¬D)I and Pr ∪{a′: ¬D} is satisfiable. (iii) a′ ∈CI ∩DI, and there exists b′ ∈∆I, b′̸ = a′, such that b′ ∈CI. Extend I to I′ so that (Ag

C)I′ = {a′}. Then a′ ∈(Ag

C)I′, b′ ∈(¬Ag

C)I′, hence Pr ∪{b: C, b: Ag

C, b′: C, b′: ¬Ag

C} is satisfiable.

Theorem 12. For any ALCι-concept C (and ontology O), if TABALCι returns unsat, then C is unsatisfiable (w.r.t. O).

Proof. If TABALCι returns unsat, then all branches of the constructed tableau are closed—i.e., the clash rule has been applied to each, indicating unsatisfiability. Since every assertion in the tableau (except the root) results from rule applications, the contrapositive of Lemma 11 ensures that unsatisfiability propagates upward through the tableau, ultimately reaching a: C at the root. This implies that C is unsatisfiable (w.r.t. O if ABox or TBox rules were applied).

For completeness, we show that if TABALCι constructs a tableau with an open and saturated branch B for input concept C (and ontology O), then C is satisfiable (w.r.t. O),

19375

<!-- Page 6 -->

as B provides sufficient information to construct a model IB = (∆IB, ·IB) of C (and O).

Let DD(B) = {C | a: ιC.D ∈B or a: ιC ∈B} denote the set of concepts that must have singleton extensions in IB. For each individual a on B, let the representative of a, rep(a), be the least (w.r.t. lexicographic order) individual a′ such that both a and a′ satisfy some C ∈DD(B) on B, or a itself if no such C exists. If the application of (∃r) to an assertion a: ∃r.C ∈B was blocked (and never unblocked), then any individual a′ on B satisfying {C} ∪{¬D | a: ¬∃r.D ∈B} ⊆ThB(a′) is called an (r, D)-proxy successor of a. We define IB = (∆IB, ·IB) as follows:

• ∆IB = {rep(a) | a occurs on B}, • aIB = rep(a) for each individual a on B, • CIB = {rep(a) | a: C ∈B} for each concept C on B, • rIB = {(rep(a), rep(a′)) | r: (a, a′) ∈B or a′ is an (r, D)-proxy successor of a for some D} for each role r. Lemma 13. For any assertion a: C ∈B, rep(a) ∈CIB.

Proof sketch. By structural induction on C. We illustrate the case C = ∃r.D. Assume a: ∃r.D ∈B. Since B is saturated, two cases arise: (i) If (∃r) was applied, then B contains b: D and r: (a, b). Thus (rep(a), rep(b)) ∈rIB, and by the induction hypothesis, rep(b) ∈DIB, hence rep(a) ∈(∃r.D)IB. (ii) If (∃r) was blocked, then (block∃) must be satisfied. Then there exists an (r, D)-proxy successor of a on B, say a′. By definition, a′: D ∈B. Thus (rep(a), rep(a′)) ∈rIB and by the induction hypothesis, rep(a′) ∈DIB, so rep(a) ∈(∃r.D)IB.

Theorem 14. If TABALCι returns sat for input C (and O), then C is satisfiable (w.r.t. O).

Proof. A sat output implies the existence of an open, saturated branch B. By Lemma 13, the constructed interpretation IB satisfies all a: D ∈B. Since a: C ∈B for some a, we have rep(a) ∈CIB, so C is satisfiable. If O is part of the input, saturation ensures all ABox rules were applied, so IB satisfies all ABox assertions. For TBox axioms C ⊑D, exhaustive application of (TBox) and Lemma 13 assure that rep(a) ∈CIB implies rep(a) ∈DIB for each individual a on B. Hence, IB satisfies O, and C is satisfiable w.r.t. O.

To prove that TABALCι terminates, we show that for any input concept C (and ontology O), the tableau T constructed by applying the TABALCι rules is finite. Each concept appearing in T is of one of the forms D, ¬D, Ag

E, ¬Ag

E, AF, or ¬AF, where D, ιE.G (for some concept G), and ιF are subconcepts of C or of concepts in O. Hence, the number of distinct concepts in T is bounded by 4 · |C| (or 4 · (|C| + |O|)), where |C| denotes the number of symbols in C (excluding parentheses), and |O| the total number of symbols in the concepts from O (also excluding parentheses). Consequently, each individual on a branch B of T can satisfy at most 4 · |C| (or 4 · (|C| + |O|)) distinct concepts. Lemma 15. Let T be a tableau for input C (and O), and let B be a branch of T. Then the number of distinct individuals on B is bounded by 24·|C| (or 24·(|C|+|O|) + k, where k is the number of individuals occurring in the ABox).

Proof sketch. New individuals may be introduced by the rules (ABoxI), (ABoxr), (∃r), (ιg

1), (¬ιg), and (¬ιℓ). Every non-root individual must be introduced by one of these rules. Define a function f that maps each individual a not introduced by any of the ABox rules to a set of concepts:

• {D}, if a is the root individual; • {D, E}, if a is introduced by (ιg 1) on a′: ιD.E; • {D, ±Ag D}, if introduced by (¬ιg) on a′: ¬ιD.E and a: ±Ag

D ∈B; • {D, AD}, if introduced by (¬ιℓ) on a′: ¬{ιD}; • {D} ∪{¬E | a′: ¬∃r.E ∈B when a was introduced}, if introduced by (∃r) on a′: ∃r.D;

where ±Ag

E denotes either Ag

E or ¬Ag

E. By construction, f(a) ⊆ThB(a). Thus, the range of f is a subset of the power set of the set of concepts on B, bounded by 24·|C| (or 24·(|C|+|O|)). We can show that f is injective, so the bound on the number of non-ABox individuals follows. Adding the k individuals from the ABox yields the claimed result.

The bound in Lemma 15 allows us to prove termination:

Theorem 16. The tableau system TABALCι is terminating.

Proof. Let T be the tableau for C (and O). Each branch B of T has at most 24·|C| (or 24·(|C|+|O|) +k, for k the number of individuals in ABox) individuals, each satisfying at most 4 · |C| (or 4 · (|C| + |O|)) concepts. Each rule application (except (ABoxr)) adds at least one concept to some individual’s theory. (ABoxr) applies at most as many times as there are role assertions in the ABox, say n. Thus the length of B is at most 4·|C|·24·|C| (or 4·(|C|+|O|)·(24·(|C|+|O|)+k)+n). As the branching factor of TABALCι is also finite, T is finite, so TABALCι terminates.

We conclude this section with a corollary following from completeness and termination of TABALCι:

Theorem 17. Let C be a satisfiable ALCι-concept. There exists a model I of C of size at most exponential in |C|.

Proof. Let T be a tableau for input C. Since TABALCι is complete and C is satisfiable, T contains an open branch B. Build an interpretation IB = (∆IB, ·IB) as in the completeness proof. By Lemma 13, rep(a) ∈CIB, where a is the root individual. The domain size is bounded by the number m of individuals on B, which by Lemma 15 is exponential in the size of C (or C and O).

## 5 Implementation and Experiments

In this section, we describe our implementation of the three tableau calculi and present their evaluation. We have implemented all three calculi in a single prover written in Python. Our implementation takes as input an ALCι concept, possibly together with an ABox and a TBox, however our preliminary experiments consider satisfiability of concepts without ontologies. The prover parses the input concept using the Python library Lark, applies the tableau procedure, and outputs information about the satisfiability of the concept. The code and instructions for using the prover

19376

<!-- Page 7 -->

No. DDs in a concept: 0.1 · k 0.3 · k 0.5 · k

Global DDs runtime avg.: 0.239s 0.750s 0.777s runtime std.dev.: 0.879s 2.16s 1.81s no. of time-outs: 21 31 42

Local DDs runtime avg.: 0.371s 0.356s 0.411s runtime std.dev.: 1.31s 0.92s 1.59s no. of time-outs: 15 32 28

**Table 1.** Runtime for concepts with only GDs and only LDs; k represents the number of binary operators in a concept

are available on https://github.com/ExtenDD/two-types-of- DDs-AAAI-2026.

The primary aim of our experiment is to compare the efficiency of the prover depending on the amount of global descriptions (GDs) and local descriptions (LDs) in the input concepts. All the experiments were run on a machine with the processor AMD Ryzen 5 PRO 7540U and 16GB RAM under Windows 11.

Generator Our generator first builds a random binary syntax tree containing a predefined number of nodes, each corresponding to a subconcept; then, atomic concepts are randomly distributed among the leaves, binary operators (including GDs) among the inner nodes, and unary operators (including LDs) among all the nodes. The generator allows to customise the number of different atoms occurring in a concept, the number of GDs, LDs, and existential restrictions, as well as the chance for each subconcept to be preceded by negation.

## Experiments

and results In all experiments, the prover was run 5 times for each concept and the minimum was recorded as runtime, with the “time-out” limit set to 10s. The reported average runtimes do not consider the “time-outs”, as well as concepts of the form ¬∃r.C, which turn out satisfiable without applying any rule. To compare runtimes for GDs and LDs we generated six datasets, each with 150 concepts containing a random number of atoms between 10 and 200. First three datasets have concepts with GDs, but with no LDs. The latter three datasest have concepts with LDs, but with no GDs. For k being the number of binary operators in a concept, the first three datasets contain 0.1 · k, 0.3 · k, and 0.5 · k GDs, respectively, whereas the next three datasets contain 0.1 · k, 0.3 · k, and 0.5 · k LDs. Other parameters are kept the same in all datasets: the number of existential restrictions is 30% of the number of subconcepts, and the number of different atoms is 50% of the number of occurrences of atoms.

The runtimes for all six datasets are presented in Table 1. We do not include the time required for concept generation and for their parsing, as our focus was on the performance of the implemented tableau procedure.2 Two observations can be made: runtime and the number of time-outs

2The runtime for parsing and concept generation grow linearly with concept size. For example, concepts with 100 atoms require approx. 0.003s to be generated and approx. 0.5s to parse and concepts with 200 atoms require 0.006s and 1s, respectively.

**Figure 3.** Runtimes for concepts with only GDs, only LDs, and without DDs; dashed lines represent average runtimes

are proportional to the number of descriptions in a concept (although this tendency is less visible for LDs), and greater for GDs than for LDs. The fact that GDs are more challenging aligns with our theoretical findings, whereas the fact that the growth of runtime is only linear, suggests practical feasibility of reasoning with DDs.

In the next experiment we analysed the scalability of the prover, by testing its performance on concepts of growing size. Recall that we identify the size of a concept with the number of symbols it uses, excluding parentheses. For this, we grouped the previously generated concepts into a set with LDs only and a set with GDs only. Additionally, we generated a set of 200 concepts without descriptions, leaving the other parameters the same as in the case of the other datasets. Results are depicted in Figure 3. We observe that in all three cases, the runtime seems to grow polynomially with concept size, even though computational complexity of the satisfiability problem is ExpTime-complete. This may be due to how we generate concepts or to insufficient data. Again, concepts with GDs have higher runtimes than those with LDs, whereas concepts without descriptions have clearly lower runtime, with only two time-outs across the whole dataset.

## 6 Conclusions

In this paper, we introduced three extensions of the standard description logic ALC: ALCιL with local definite descriptions {ιC}, ALCιG with global descriptions ιC.D, and ALCι, which supports both. We showed that all three logics are ExpTime-complete, but differ in expressive power: ALCιL < ALCιG = ALCι. This expressiveness result is established via tailored bisimulations developed and analysed in the paper. We also proposed tableau-based decision procedures for all the logics and implemented them. Experimental results show that definite descriptions increase reasoning time, with global descriptions incurring a higher cost than local ones. Nonetheless, the overhead remains manageable, confirming the practical feasibility of our extensions. In future work, our aim is to optimise both the algorithms and their implementations.

19377

![Figure extracted from page 7](2026-AAAI-description-logics-with-two-types-of-definite-descriptions-complexity-expressive/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

This research is funded by the European Union (ERC, ExtenDD, project number: 101054714). Views and opinions expressed are however those of the authors only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.

## References

Areces, C.; Koller, A.; and Striegnitz, K. 2008. Referring expressions as formulas of description logic. In Proc. of INLG, 42–49. Artale, A.; Mazzullo, A.; Ozaki, A.; and Wolter, F. 2021. On Free Description Logics with Definite Descriptions. In Proc. of KR, 63–73. Baader, F. 2003. The description logic handbook: Theory, implementation and applications. Cambridge: Cambridge University Press. Baader, F.; Horrocks, I.; Lutz, C.; and Sattler, U. 2017. An introduction to description logic. Cambridge University Press. Benzmüller, C.; and Scott, D. S. 2020. Automating Free Logic in HOL, with an Experimental Application in Category Theory. Journal of Automated Reasoning, 64(1): 53– 72. Bohrer, R.; Fernández, M.; and Platzer, A. 2019. dLι: Definite Descriptions in Differential Dynamic Logic. In Fontaine, P., ed., Proc. of CADE, 94–110. Borgida, A.; Toman, D.; and Weddell, G. 2016a. On referring expressions in information systems derived from conceptual modelling. In Proc. of ER, 183–197. Borgida, A.; Toman, D.; and Weddell, G. 2016b. On referring expressions in query answering over first order knowledge bases. In Proc. of KR, 319–328. Borgida, A.; Toman, D.; and Weddell, G. 2017. Concerning Referring Expressions in Query Answers. In Proc. of IJCAI- 17, 4791–4795. Chang, C. C.; and Keisler, H. J. 1992. Model theory, Third Edition, volume 73 of Studies in logic and the foundations of mathematics. North-Holland. Fitting, M.; and Mendelsohn, R. L. 2023. First-Order Modal Logic, volume 480 of Synthese Library. Cham: Springer, 2 edition. Hilbert, D.; and Bernays, P. 1968. Grundlagen der Mathematik I. Berlin, Heidelberg: Springer. Indrzejczak, A. 2023a. Russellian Definite Description Theory – a Proof Theoretic Approach. Review of Symbolic Logic, 16(2): 624–649. Indrzejczak, A. 2023b. Towards Proof-Theoretic Formulation of the General Theory of Term-Forming Operators. In Proc. of TABLEAUX, 131–149. Indrzejczak, A.; and Kürbis, N. 2023. A Cut-Free, Sound and Complete Russellian Theory of Definite Descriptions. In Proc. of TABLEAUX, 112–130.

Indrzejczak, A.; and Petrukhin, Y. I. 2024. Bisequent Calculi for Neutral Free Logic with Definite Descriptions. In Proc. of ARQNL, 48–61. Indrzejczak, A.; and Zawidzki, M. 2021. Tableaux for Free Logics with Descriptions. In Proc. of TABLEAUX, 56–73. Indrzejczak, A.; and Zawidzki, M. 2023a. Definite descriptions and hybrid tense logic. Synthese, 202(3). Article number: 98. Indrzejczak, A.; and Zawidzki, M. 2023b. When iota meets lambda. Synthese, 201(1). Article number: 72. Kaminski, M.; and Smolka, G. 2009. Hybrid Tableaux for the Difference Modality. Electronic Notes in Theoretical Computer Science, 231: 241–257. Proc of. M4M5 2007. Kürbis, N. 2019a. A Binary Quantifier for Definite Descriptions in Intuitionist Negative Free Logic: Natural Deduction and Normalisation. Bulletin of the Section of Logic, 48(2): 81–97. Kürbis, N. 2019b. Two Treatments of Definite Descriptions in Intuitionist Negative Free Logic. Bulletin of the Section of Logic, 48(4): 299–317. Kürbis, N. 2025. Normalisation for Negative Free Logics without and with Definite Descriptions. Review of Symbolic Logic, 18(1): 240–272. Lambert, K. 2001. Free Logic and Definite Descriptions. In New Essays in Free Logic, volume 23, 37–48. Neuhaus, F.; Kutz, O.; and Righetti, G. 2020. Free Description Logic for Ontologists. In Proc. of JOWO. Oppenheimer, P. E.; and and, E. N. Z. 2011. A Computationally-Discovered Simplification of the Ontological Argument. Australasian Journal of Philosophy, 89(2): 333–349. Orlandelli, E. 2021. Labelled calculi for quantified modal logics with definite descriptions. Journal of Logic and Computation, 31(3): 923–946. Pelletier, F. J.; and Linsky, B. 2005. What is Frege’s Theory of Descriptions. In On Denoting: 1905–2005, 195–250. Ren, Y.; van Deemter, K.; and Pan, J. Z. 2010. Charting the Potential of Description Logic for the Generation of Referring Expressions. In Proc. of INLG, 115–123. Rosser, J. B. 1978. Logic for Mathematicians. Dover: Dover Publications. Russell, B. 1905. On denoting. Mind, 14(56): 479–493. Toman, D.; and Weddell, G. 2016. Ontology Based Data Access with Referring Expressions for Logics with the Tree Model Property – (Extended Abstract). In Proc. of AI, 353– 361. Toman, D.; and Weddell, G. 2018. Identity Resolution in Conjunctive Querying over DL-Based Knowledge Bases. In Proc. of DL, 1–12. Toman, D.; and Weddell, G. 2019a. Finding ALL answers to OBDA queries using referring expressions. In Proc. of AI, 117–129. Toman, D.; and Weddell, G. 2019b. Identity resolution in ontology based data access to structured data sources. In Proc. of PRICAI, 473–485.

19378

<!-- Page 9 -->

Wał˛ega, P. A. 2024. Expressive Power of Definite Descriptions in Modal Logics. In Proc. of KR, 687–696. Wał˛ega, P. A.; and Zawidzki, M. 2023. Hybrid Modal Operators for Definite Descriptions. In Proc. of JELIA, 712–726.

19379
