---
title: "Data Complexity of Querying Description Logic Knowledge Bases Under Cost-Based Semantics"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38966
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38966/42928
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Data Complexity of Querying Description Logic Knowledge Bases Under Cost-Based Semantics

<!-- Page 1 -->

Data Complexity of Querying Description Logic

Knowledge Bases under Cost-Based Semantics

Meghyn Bienvenu1, Quentin Mani`ere2, 3

1Universit´e de Bordeaux, CNRS, Bordeaux INP, LaBRI, UMR 5800, Talence, France 2Department of Computer Science, Leipzig University, Germany 3Center for Scalable Data Analytics and Artificial Intelligence (ScaDS.AI), Dresden/Leipzig, Germany meghyn.bienvenu@labri.fr, quentin.maniere@uni-leipzig.de

## Abstract

In this paper, we study the data complexity of querying inconsistent weighted description logic (DL) knowledge bases under recently-introduced cost-based semantics. In a nutshell, the idea is to assign each interpretation a cost based upon the weights of the violated axioms and assertions, and certain and possible query answers are determined by considering all (resp. some) interpretations having optimal or bounded cost. Whereas the initial study of cost-based semantics focused on DLs between EL⊥and ALCO, we consider DLs that may contain inverse roles and role inclusions, thus covering prominent DL-Lite dialects. Our data complexity analysis goes significantly beyond existing results by sharpening several lower bounds and pinpointing the precise complexity of optimal-cost certain answer semantics (no non-trivial upper bound was known). Moreover, while all existing results show the intractability of cost-based semantics, our most challenging and surprising result establishes that if we consider DL-LiteH bool ontologies and a fixed cost bound, certain answers for instance queries and possible answers for conjunctive queries can be computed using first-order rewriting and thus enjoy the lowest possible data complexity (AC0).

Extended version — http://arxiv.org/abs/2511.07095

## Introduction

Ontology-mediated query answering (OMQA) has been extensively studied within the KR and database communities as a means of improving data access by exploiting semantic information provided by an ontology (Poggi et al. 2008; Bienvenu and Ortiz 2015; Xiao et al. 2018). Ontologies are typically formulated in decidable fragments of first-order logic (FO), with description logics (DLs) being a popular choice (Baader et al. 2017). Given an ontology (or TBox in DL parlance) T, a dataset (or ABox) A, and a query q(⃗x), the OMQA task boils down to finding the certain answers, i.e. tuples of constants⃗a for which the instantiated query q(⃗a) is entailed from the knowledge base (KB) (T, A). Observe that if the input KB is inconsistent, every answer tuple is trivially a certain answer, so OMQA trivializes.

A prominent approach to tackling this issue is to adopt alternative inconsistency-tolerant semantics in order to be

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

able to extract meaningful information from inconsistent KBs, cf. (Lembo et al. 2010) and surveys (Bienvenu and Bourgaux 2016; Bienvenu 2020). Many of these semantics are based upon repairs, defined as inclusion-maximal consistent subsets of the ABox. For example, the AR semantics considers the query answers that hold in all repairs, while the brave semantics returns those answers holding in at least one repair. Note that the line of work on repairbased semantics targets scenarios in which the TBox axioms are deemed fully reliable, so inconsistencies derive solely from errors in the ABox. However, in practice, it can be useful to allow for TBox axioms which typically hold but may admit rare exceptions. Such ‘soft’ ontology axioms can be addressed qualitatively, using generalized notions of repair that have been proposed for existential rule ontologies (Eiter, Lukasiewicz, and Predoiu 2016), or employing nonmonotonic extensions of DLs that support defeasible axioms cf. (Bonatti, Lutz, and Wolter 2009; Giordano et al. 2013; Britz et al. 2021). Another option is to adopt a quantitative approach, using the recently proposed cost-based semantics for DL KBs (Bienvenu, Bourgaux, and Jean 2024), henceforth referred to as (BBJ 2024) for succinctness.

In a nutshell, the idea is to annotate axioms and assertions with (possibly infinite) weights, which are used to assign a cost to each interpretation based upon the weights of the violated axioms and assertions (and taking into account also the number of violations of each TBox axiom). To query the KB, we may choose either to consider the set of interpretations achieving the optimal cost, or we may fix a cost bound k and consider all interpretations having cost at most k. We can then define the sets of certain and possible answers as those answers that hold respectively in all or some interpretation of optimal cost or bounded cost. As noted in (BBJ 2024), the optimal-cost certain answer semantics generalizes both the classical certain answer semantics and the AR semantics based upon weighted ABox repairs. Increasing the cost bound k beyond the optimal cost allows one to identify answers that are robust in the sense that they hold not only for the optimal-cost interpretations. Optimal- and bounded-cost possible answers generalize query satisfiability and can serve to compare candidate answers based upon their incompatibility with the KB.

The computational complexity of querying inconsistent weighted KBs under cost-based semantics was investigated

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

18953

<!-- Page 2 -->

in (BBJ 2024). Five central decision problems were considered: bounded-cost satisfiability (does there exist an interpretation with cost at most k?) plus query entailment under the four cost-based semantics. The complexity analysis was fairly comprehensive, considering both combined and data complexity, conjunctive and instance queries, and DLs ranging from the lightweight DL EL⊥to the expressive DL ALCO. One important question that was left open, however, was the data complexity of optimal-cost certain semantics (arguably the most useful of the semantics), for which no non-trivial upper bound was provided. Moreover, as the considered DLs allow neither inverse roles nor role inclusions, they do not yield any results for DLs of the DL-Lite family (Calvanese et al. 2007), which are the most commonly utilized in the context of OMQA.

The preceding considerations motivate us to embark on a more detailed data complexity analysis of cost-based semantics, considering various DL-Lite dialects and expressive DLs up to ALCHIO. The results of our study are summarized in Table 1. A first major contribution, detailed in Section 4, is to provide a ∆p

2 upper bound for the optimalcost certain and possible semantics, matching an existing lower bound for EL⊥and a new lower bound we show for DL-Litecore. This result is obtained by using an intricate quotient construction to establish a small interpretation property, which crucially does not depend on the considered cost. In Section 5, we strengthen a number of existing lower bounds for the bounded-cost semantics by showing that they hold even when for cost bound k = 1, as well as providing some new lower bounds for DL-Litecore. Finally, our most challenging and surprising technical result (presented in Section 6) is to show that if we consider DL-LiteH bool ontologies and a fixed cost bound, then certain answers for instance queries and possible answers for conjunctive queries can be computed using first-order rewriting and thus enjoy the lowest possible data complexity (AC0). Detailed proofs can be found in the appendix of the extended version.

## Preliminaries

We recall the syntax & semantics of description logics (DLs) and refer readers to (Baader et al. 2017) for further details.

Description logic knowledge bases We consider countably infinite sets NC, NR, and NI of concept names, role names, and individual names. An inverse role has the form r−, with r ∈NR. A role is either a role name or inverse role. We use N±

R = NR ∪{r−| r ∈NR} for the set of roles. If r = s−is an inverse role, then r−denotes s.

An ALCIO concept C is built according to the grammar C, D::= ⊤| ⊥| A | {a} | ¬C | C⊓D | ∃r.D where A ∈NC, r ∈N±

R, and a ∈NI. A concept {a} is called a nominal. An ALCI concept is a nominal-free ALCIO concept. An EL concept is an ALCI concept that uses neither negation, nor ⊥, nor inverse roles (EL⊥concepts may additionally use ⊥).

An ALCHIO TBox is a finite set of concept inclusions (CIs) C ⊑D, where C, D are ALCIO concepts, and role inclusions (RIs) r ⊑s, where r, s ∈N±

R. An EL TBox consists only of CIs between EL concepts. An ABox is a finite set of concept assertions A(a) and role assertions r(a, b) where

A ∈NC, r ∈NR, and a, b ∈NI. We use Ind(A) for the set of individual names used in A, and NC(T) (resp. NR(T)) for the set of concept (resp. role) names used in T. An ALCHIO knowledge base (KB) takes the form K = (T, A) with T an ALCHIO TBox and A an ABox.

We next introduce the syntax of some DLs of the DL-Lite family. A basic concept has the form A or ∃r, with A ∈NC and r ∈N±

R. A DL-LiteH core TBox is a finite set of CIs of the forms C ⊑D and C ⊓D ⊑⊥, with C, D basic concepts, and RIs r ⊑s, with r, s ∈N±

R. We drop superscript ·H if no role inclusions are admitted, and replace ·core by ·bool to indicate that C, D may be built from basic concepts using ¬, ⊓, ⊔.

The semantics of DL KBs is defined as usual in terms of interpretations I = (∆I, ·I) with ∆I the non-empty domain and ·I the interpretation function. An interpretation satisfies a CI C ⊑D if CI ⊆DI and likewise for RIs. It satisfies an assertion A(a) if a ∈AI and r(a, b) if (a, b) ∈rI. This notably requires ABox individuals to be interpreted as themselves, thus enforcing the standard names assumption (SNA) for the ABox individuals. The interpretation IA associated with an ABox A has domain Ind(A) and interprets concept and role names according to the assertions of A:

AIA:= {a | A(a) ∈A} rIA:= {(a, b) | r(a, b) ∈A}. Given any interpretation I, we use I|∆to denote the restriction of I to a subdomain ∆⊆∆I.

Queries First-order queries are given by formulas in firstorder logic with equality. Since we wish to query DL KBs, we consider queries whose relational atoms can be either concept atoms A(t) or role atoms r(t, t′), where A ∈NC, r ∈NR, and t, t′ are terms (variables or individuals). We mostly focus on conjunctive queries (CQs) which have the form ∃⃗yψ, where ψ is a conjunction of concept and role atoms, and⃗y a tuple of variables from ψ. Instances queries (IQs) are CQs with a single atom. We also consider acyclic and connected CQs, meaning that the associated undirected graph (containing an edge {t, t′} for each role atom r(t, t′)) has these properties. A Boolean CQ (BCQ) is a CQ that has no free variables. We write I |= q to indicate that an interpretation I satisfies a BCQ q.

Complexity classes For any syntactic object O such as a TBox, ABox, or query, we use |O| to denote the size of O, meaning the encoding of O as a word over a suitable alphabet. Our complexity results concern the well-known complexity classes NP and coNP as well as ∆p

2 (deterministic polynomial time with access to an NP oracle) and AC0. We omit the formal definition of AC0, which is based upon circuits, as to understand our results, it suffices to know that it is in AC0 (in data complexity) to test whether a Boolean first-order query is satisfied in a finite interpretation.

## 3 Cost-Based Semantics for Weighted KBs

In this section, we recall the definition of cost-based semantics from (BBJ 2024) and introduce the associated reasoning tasks. We also recall and prove some basic properties used in later sections.

Throughout the paper, we work with weighted KBs, whose assertions and axioms are annotated with weights:

18954

<!-- Page 3 -->

BCSk, IQAk p, CQAk p IQAk c CQAk c BCS, IQAp, CQAp IQAc, CQAc IQAopt p,c, CQAopt p,c

EL⊥/ ALCHIO NP ‡

Thm. 1, 3 coNP ‡

Thm. 1, 4 coNP ‡

Thm. 1, 4 NP †

Thm. 1 coNP †

Thm. 1 ∆p

2 †

Thm. 2 DL-Litecore / DL-LiteH bool in AC0

Thm. 8 in AC0

Thm. 8 coNP

Thm. 1, 7 NP Thm. 1, 5 coNP

Thm. 1, 5 ∆p

2 Thm. 2, 6

**Table 1.** All results are completeness results, unless stated otherwise. †: lower bound from (BBJ 2024). ‡: lower bound for k ≥3 from (BBJ 2024), improved to k ≥1 in the present paper. For CQA, lower bounds already hold for connected acyclic BCQs. Results hold both for binary and unary encoding of weights, except for ∆p

2-hardness (only for binary encoding).

Definition 1. A weighted knowledge base (WKB) Kω = (T, A)ω consists of a knowledge base (T, A) and a weight function ω: T ∪A 7→N>0 ∪{∞}. We can similarly define weighted TBoxes (Tω) and weighted ABoxes (Aω).

Intuitively, these weights can be viewed as the penalties incurred for violating assertions and axioms: those having cost 1 are the least reliable, while those assigned maximal weight ∞should definitely be satisfied.

Interpretations will then be assigned costs based upon the sets of violations of the TBox axioms and ABox assertions. Note that differently from prior work, we also define violations of role inclusions, given by pairs of domain elements. Definition 2. Given an interpretation I, the set of violations of a concept inclusion B ⊑C in I is vioB⊑C(I) = BI \ CI, the set of violations of a role inclusion r ⊑s in I is vior⊑s(I) = rI \ sI, and the violations of an ABox A in I are vioA(I) = {α ∈A | I̸ |= α}. Definition 3. Let Kω = (T, A)ω be a WKB. The cost of an interpretation I w.r.t. Kω is defined by:

ω(I) =

X τ∈T ω(τ)|vioτ(I)| +

X α∈vioA(I)

ω(α)

The optimal cost of Kω is optc(Kω) = minI(ω(I)). A WKB Kω is k-satisfiable if ω(I) ≤k for some interpretation I.

We recall next the four cost-based semantics proposed in (BBJ 2024), which depend on whether one considers interpretations whose cost is less than a provided bound, or the interpretations having optimal cost, and whether the query is required to hold in all or at least one such interpretation. Definition 4. Let q be a BCQ, Kω = (T, A)ω a WKB, and k an integer. We say that q is entailed by Kω under

• k-cost bounded certain semantics, written Kω |=k c q, if I |= q for every interpretation I with ω(I) ≤k; • k-cost bounded possible semantics, written Kω |=k p q, if I |= q for some interpretation I with ω(I) ≤k; • opt-cost certain semantics, written Kω |=opt c q, if I |= q for every interpretation I with ω(I) = optc(Kω); • opt-cost possible semantics, written Kω |=opt p q, if I |= q for some interpretation I with ω(I) = optc(Kω). These semantics extend to non-Boolean CQs in the expected way, e.g. the opt-cost certain answers to a CQ q(⃗x) w.r.t. (T, A)ω are the tuples⃗a from Ind(A) s.t. Kω |=opt c q(⃗a). If the underlying KB is satisfiable, then the certain and possible optimal-cost semantics coincide with query entailment and query satisfiability (or with classical notions of certain and possible answers, in the case of non-Boolean queries). These semantics are thus intended to be used when the underlying KB is inconsistent. The opt-cost certain answers identifies those answers that hold in the interpretations deemed most likely and have been shown to generalize previously considered weight-based repair semantics (BBJ 2024). By considering values of k beyond optc(Kω), we can use the k-cost bounded certain semantics to identify ‘robust’ answers which hold not only in the optimal-cost interpretations but also in those with close-to-optimal cost. By contrast, the opt-cost and k-cost bounded possible answers can serve to rank candidate answers based upon their degree of incompatibility with the WKB.

We now formalize the decision problems for cost-based semantics investigated in this paper, which differ depending on which cost bound is used and whether it is given as input:

• Bounded cost satisfiability (BCS) takes as input a WKB Kω = (T, A)ω and an integer k and decides whether there exists an interpretation I with ω(I) ≤k. • k-cost satisfiability (BCSk) takes as input a WKB Kω = (T, A)ω and decides whether there exists an interpretation I with ω(I) ≤k. • Bounded-cost certain (resp. possible) BCQ entailment (CQAc / CQAp) takes as input a WKB Kω = (T, A)ω, a BCQ q and an integer k and decides whether Kω |=k c q (resp. Kω |=k p q). • k-cost certain (resp. possible) BCQ entailment (CQAk c / CQAk p) takes as input a WKB Kω = (T, A)ω and a BCQ q and decides whether Kω |=k c q (resp. Kω |=k p q). • Optimal-cost certain (resp. possible) BCQ entailment (CQAopt c / CQAopt p) takes as input a WKB Kω = (T, A)ω and a BCQ q and decides if Kω |=opt c q (resp. Kω |=opt p q). We will also consider the restrictions of the BCQ entailment problems to the case of instance queries, denoted by IQAc, IQAp, IQAk c, IQAk p, IQAopt c and IQAopt p respectively. We shall study the data complexity of the preceding reasoning tasks. For the fixed-cost and optimal-cost decision problems, data complexity is measured with respect to the size of the input weighted ABox, while the size of the weighted TBox and query (if present) are treated as constants. For the bounded-cost problems, we measure complexity w.r.t. the weighted ABox and the input integer. Both the ABox weights and the input integer (if present) are assumed to be encoded in binary.

We conclude the section with some easy lemmas, which establish useful reductions between the decision problems.

18955

<!-- Page 4 -->

Lemma 1. BCSk for DL-Litecore (resp. EL⊥) reduces to IQAk p for DL-Litecore (resp. EL⊥). In particular, the same holds for BCS and IQAp.

Lemma 2. IQAk p for DL-Litecore (resp. EL⊥) reduces to the complement of IQAk+1 c for DL-Litecore (resp. EL⊥). In particular, IQAp reduces to the complement of IQAc.

Lemma 3. For every k ≥0, IQAk p for DL-Litecore (resp. EL⊥) reduces to IQAk+1 p for DL-Litecore (resp. EL⊥) WKBs.

An Upper Bound for the General Case The aim of this section is to establish the next two theorems: Theorem 1. CQAp (resp. CQAc) for ALCHIO is in NP (resp. in coNP). Theorem 2. CQAopt p and CQAopt c for ALCHIO are in ∆p

2. Starting from an interpretation I that satisfies (or does not satisfy) the query q of interest, the main technical ingredient is the construction of another interpretation J that behaves as I w.r.t. q, whose cost is at most the cost of I, and whose domain has a size polynomially bounded by the size of the input ABox A. This is fairly easy if query satisfaction is to be preserved, that is, for CQAp: one can brutally collapse elements together according to their type using the well-known filtration technique (Baader et al. 2017). Lemma 4. Let K = (T, A)ω be an ALCHIO WKB, k an integer, and q a BCQ. If there exists an interpretation I such that ω(I) ≤k and I |= q, then there is an interpretation J such that ω(J) ≤k and J |= q, and whose domain ∆J has cardinality bounded polynomially in |A|, with |T | and |q| treated as constants, and independently from k.

It becomes more challenging if query non-satisfaction is the property to preserve, that is, to address CQAc. In particular, the solution adopted in (BBJ 2024, Proposition 8) for ALCO WKBs yields a polynomial bound that depends on the bounded cost k. This makes their technique adequate when the cost is fixed, that is, for CQAk c, or if the encoding of k is given in unary, but otherwise does not provide a polynomial upper bound w.r.t. data complexity. We deeply rework the approach, not only to support ALCHIO WKBs, but also to obtain a cost-independent bound as follows. Lemma 5. Let K = (T, A)ω be an ALCHIO WKB, k an integer, and q a BCQ. If there exists an interpretation I such that ω(I) ≤k and I̸ |= q, then there is an interpretation J such that ω(J) ≤k and J̸ |= q, and whose domain ∆J has cardinality that is bounded polynomially in |A|, with |T | and |q| treated as constants, and independently from k.

With Lemmas 4 and 5, we obtain the NP and coNP upper bounds in Theorem 1 with standard guess-and-check procedures. For Theorem 2, the ∆p

2 algorithms proceed similarly but first identify the optimal cost via a binary search, using an exponential bound on the optimal cost (whenever finite).

Now, to prove Lemma 5, we rely on the adaptation of a quotient construction from (Mani`ere 2022, Theorem 8) defined to answer counting conjunctive queries over ALCHI KBs. This construction was already reused by (BBJ 2024) for ALCO WKBs, and it is not too difficult to handle inverse roles and role inclusions by sticking closer to the original version. From the starting interpretation I, our adaptation differs from theirs as it also takes as a parameter a subset V ⊆T of the considered TBox T. In the constructed interpretation, we violate axioms of V exactly as in the original interpretation I. Intuitively, one can think of these axioms in V as so expensive to violate that one cannot do better than in I, while potential violations of axioms from T \ V can be handled in a more systematic and structured manner. Violations of ABox assertions are easier to control and are preserved exactly as in the original interpretation I. For an interpretation J, we denote vioV(J):= S τ∈V vioτ(J). Adapting the quotient technique yields the following: Lemma 6. Let K = (T, A) be an ALCHIO KB and q a BCQ. Let V ⊆T be a subset of T and I an interpretation such that I̸ |= q. There exists a polynomial p independent of A, and an interpretation J satisfying the following: 1. J̸ |= q; 2. vioA(J) = vioA(I); 3. ∀τ ∈V, vioτ(J) ⊆vioτ(I); 4. ∆J ≤p(|A| + |vioV(I)|). We now explain how to obtain Lemma 5, with an approach inspired from (Lutz and Mani`ere 2024), where our Lemmas 5 and 6 respectively play the role of their Proposition 2 and Lemma 1. Let Kω = (T, A)ω be an ALCHIO WKB, q a BCQ, k an integer, and I an interpretation such that I̸ |= q. For a given V ⊆T, we use JV to denote the interpretation obtained by applying Lemma 6 with V the input set of axioms. We prove that there exists a subset V ⊆T such that (i) the size of vioV(I) is bounded by a polynomial in |A| independent of k; and (ii) ω(JV) ≤k. To do so, we construct a sequence V0 ⊊V1 ⊊· · · ⊊Vn ⊆T of V’s that all satisfy item (i) and with Vn also satisfying item (ii). Note that JVn is then the desired interpretation for Lemma 5: item (i) plus Point 4 from Lemma 6 gives the polynomial bound on the size of Jn, while item (ii) and Point 1 in Lemma 6 ensure the desired properties w.r.t. the cost and query. Initialization. Set V0:= ∅, which trivially satisfies item (i). Induction step. Assume that, for some i ≥0, we have successfully constructed Vi satisfying item (i); thus we have a polynomial pi independent of k such that |vioV(I)| ≤ pi(|A|). If Vi also satisfies item (ii), then we are done. Otherwise ω(JVi) > k, and since ω(I) ≤k, there exists an assertion or axiom τ from K that is violated at least once more in JVi than in I, i.e. |vioτ(JVi)| > |vioτ(I)|. Note that due to Point 2 in Lemma 6, it is then clear that τ /∈A. Similarly, due to Point 3 in Lemma 6, we have τ /∈Vi. Therefore τ ∈T \ Vi. We set Vi+1:= Vi ∪{τ}. It remains to verify that Vi+1 satisfies item (i). Note that vioVi+1(I) = vioVi(I) ∪vioτ(I). The size of vioVi(I) is bounded adequately by pi(|A|). For the size of vioτ(I), recall that by choice of τ we have |vioτ(I)| < |vioτ(JVi)|. We brutally bound |vioτ(JVi)| by

∆JVi 2. By Point 4 in Lemma 6, ∆JVi has size bounded by p(|A| + |vioVi(I)|), thus by p(|A|+pi(|A|)). Overall, the size of vioVi+1(I) is bounded by pi+1(|A|) where pi+1(x):= pi(x) + (p(x + pi(x)))2 is the desired polynomial independent of k.

Note that this procedure is guaranteed to terminate in at most |T | steps, which concludes the proof.

18956

<!-- Page 5 -->

Lower Bounds We first refine some existing lower bounds for the fixed-cost decision problems in EL⊥, then prove the lower bounds for DL-Lite listed in Table 1.

## 5.1 Lower Bounds in

Extensions of EL⊥ We begin with two lower bounds showing that even if the cost k is fixed to 1, all considered reasoning tasks are NPcomplete (or coNP-complete, depending on the task) already for EL⊥WKBs. These results notably improve those from (BBJ 2024), where the cost was fixed to 3. Lemma 3 lifts our hardness proof to any fixed k ≥1, and since the case of fixed k = 0 coincides with the usual semantics of EL KBs, the complexity w.r.t. fixed cost is now well understood. Theorem 3. For every k ≥1, BCSk, IQAk p and CQAk p for EL⊥are NP-hard.

Proof sketch. The reduction is from 3-SAT. Given a 3-CNF formula ϕ:= Vℓ i=1

W3 j=1 li,j, where each li,j is a literal over v1,..., vn, we construct a WKB (T, Aϕ)ω. The ABox Aϕ contains False(a), Bool(a), and the additional assertions:

Var(vk) for 1 ≤k ≤n clause(a, ci) for 1 ≤i ≤ℓ posj(ci, vk) for li,j = vk negj(ci, vk) for li,j = ¬vk The TBox T has the following axioms:

Bool ⊑True True ⊓False ⊑⊥ ∃clause.False ⊑True Var ⊑∃val.Bool ∃val.True ⊑True ∃val.False ⊑False ∃pos1.False ⊓∃pos2.False ⊓∃pos3.False ⊑False

(the six other combinations...) ∃neg1.True ⊓∃neg2.True ⊓∃neg3.True ⊑False

The function ω assigns ∞to all axioms and assertions, except for Bool ⊑True, which has weight 1. One can verify that ϕ is satisfiable iff (T, Aϕ)ω is 1-satisfiable.

For the case of IQAk c, we could use Lemma 2 to directly obtain a coNP-hardness proof for k ≥2. We instead re-adapt the above proof to strengthen the result to every k ≥1. Note that concept disjointness axioms are not even needed here. Theorem 4. For every k ≥1, IQAk c and CQAk c for EL are coNP-hard.

## 5.2 Lower Bounds in the DL-Lite Family We now turn to the DL-Lite family, which inherits the upper bounds from

Theorems 1 and 2. We begin with a proof that, when k is allowed to vary, all considered reasoning tasks are NP-hard (resp. coNP-hard) already for DL-Litecore WKBs. Theorem 5. BCS, IQAp and CQAp for DL-Litecore are NPhard. IQAc and CQAc for DL-Litecore WKBs are coNP-hard.

Note that, by virtue of Lemmas 1 and 2, it suffices to prove that BCS for DL-Litecore is NP-hard.

Proof sketch. We reduce from 3-COL, that is deciding whether a given graph G = (V, E) is 3-colourable. All axioms of T are given infinite weight by ω and are as follows:

∃si ⊓∃tj ⊑⊥for s, t ∈{r, g, b}, s̸ = t, and i, j ∈{1, 2} ∃s−

1 ⊓∃s− 2 ⊑⊥for s ∈{r, g, b}

We choose an orientation E′ of E: for each {u, v} ∈E, we add either (u, v) or (v, u) in E′. For each e = (u, v) ∈E′ and each s ∈{r, g, b}, we add s1(u, e) and s2(v, e) in the ABox AG. Assertions in AG are given weight 1 by ω. It can be verified that G ∈3-COL iff (T, AG)ω is 4|E|-satisfiable.

For optimal cost semantics, we establish a matching ∆p

2 lower bound. The proof adapts an existing construction from (Bourgaux 2016, Proposition 6.2.4) that establishes ∆p

2-hardness of query entailment for DL-Lite KBs under preferred repair semantics, by reduction from deciding if a given variable is true in the lexicographically maximum truth assignment satisfying a given satisfiable CNF. We point out that, unlike the other lower bounds listed in Table 1, this result crucially relies upon a binary encoding of weights, intuitively because exponentially large weights are needed to perform lexicographic comparison of satisfying valuations. Theorem 6. IQAopt p, IQAopt c, CQAopt p, and CQAopt c for DL-Litecore are ∆p

2-hard. We now move to the case in which k is fixed. Notice indeed that the lower bound from Theorem 5 strongly relies on a varying k. For the certain semantics, we show that coNPhardness holds even if k is fixed to 1, if we consider CQs. The proof is strongly inspired by the one of Theorem 4, especially with how to simulate the truth value assignment. The main difference is that we use acyclic CQs to circumvent the lack of nested concepts in DL-Litecore. Theorem 7. For every k ≥1, CQAk c for DL-Litecore is coNP-hard. This holds already for connected acyclic BCQs and without concept disjointness axioms.

## 6 Positive Results in the DL-Lite Family

In light of the lower bounds established in the previous section, we can only hope to achieve tractability for the DL-Lite family under a fixed cost (see Theorem 5). Furthermore, under the certain semantics, we established that CQAk c answering is coNP-hard (Theorem 7) already for DL-Litecore and k = 1. This leaves us with two promising settings to explore: CQAk p and IQAk c for DL-Litecore. This section establishes that both reasoning tasks enjoy the lowest possible complexity, that is, AC0. Furthermore, we can even push this positive result to one of the most expressive logics of the DL-Lite family, namely DL-LiteH bool.

Theorem 8. For every integer k ≥1, CQAk p and IQAk c for DL-LiteH bool are in AC0. Our approach is based on first-order (FO) rewriting: given the weighted TBox TωT, query q and cost k, we construct an FO-query q′ such that for every weighted ABox AωA, the following, here stated for CQAk p, holds:

(T, A)ωT ∪ωA |=k p q iff IAωA |= q′.

To make this formulation fully precise, we need to define the FO-interpretation IAωA associated with a weighted ABox AωA, over which the rewritten query q′ is evaluated. We argue that AωA can be seen as a usual ABox augmented with extra assertions about the weights. We denote by AωA k the

18957

<!-- Page 6 -->

extension of A with special concept and role assertions that encapsulate the relevant information about weights w.r.t. the fixed cost bound k: if a concept assertion ωA(A(a)) = n, then we add the assertion Wn

A(a) if n ≤k, or assertion W∞

A (a) if n > k. We proceed similarly for each role assertion r(a, b), adding respectively wn r (a, b) or w∞ r (a, b). Notice that we only need to introduce (k+1)(NC(A)+NR(A)) fresh predicates and that computing AωA k from any reasonable representation of AωA can be seen as a pre-processing step achieved by an AC0 transducer. As AωA k is a usual ABox, its corresponding interpretation IA ωA k is well defined and can serve as the desired interpretation IAωA.

Before explaining how to construct q′, we sketch the main argument that allows for such a rewriting to exist and that ensures completeness of the claim (i.e. the ⇒direction in the formulation above). It relies on a (very!) small interpretation property: if an interpretation witnesses the desired behaviour w.r.t. the query and within the fixed cost, then there exists one that is completely trivial except on a small domain whose size is bounded by a constant w.r.t. the input weighted ABox. The different possibilities to interpret such a constant-size domain can thus all be encapsulated in the rewritten query q′. To facilitate the understanding of the rewriting, we first present this small interpretation property.

## 6.1 A (Very) Small Interpretation Property

Consider a WKB K = (T, A)ω, a fixed cost k and a BCQ q. We introduce two distinct notions of types. The first is the usual one in DLs: a 1-type t is a subset of NC(T) ∪{∃r | r ∈N±

R (T)}. The 1-type of an element e ∈∆I is tpI(e):= {A | e ∈AI} ∪{∃r | e ∈(∃r)I, r ∈N±

R }. This notion of 1-type captures the basic DL-Lite concepts, and thus, if two elements d and e have the same 1-type, then they violate exactly the same DL-Litebool CIs.

The second notion of type is intended to capture the concepts that hold due to the ABox assertions. We define the ABox type tpA(a) of a ∈Ind(A) as:

tpA(a):= tpIA(a) ∪{∃>kr | A |= ∃>kr, r ∈N±

R (T)}, where A |= ∃>kr means that there exists (at least) k + 1 distinct individuals b1,..., bk+1 ∈NI such that r(a, b1),..., r(a, bk+1) ∈A (or r(b1, a),..., r(bk+1, a) ∈ A if r is an inverse role). Notice that there are at most 2|NC(T)|+2|NR(T)| possible 1-types, and at most 2|NC(T)|+4|NR(T)| possible ABox types. We write r ⊑T s if (r, s) is in the transitive closure of {(p, p) | p ∈N±

R } ∪{(p, q) ∈N±

R × N±

R | p ⊑q ∈ T }. The following observation motivates the extension of 1-types into ABox types when a fixed cost k is considered: Lemma 7. Consider an interpretation I whose cost is ≤k. For every individual a and role r ∈N±

R, if ∃>kr ∈tpA(a), then ∃s ∈tpI(a) for every role s ∈N±

R such that r ⊑T s. We now prove that, if there exists an interpretation I whose cost is ≤k, then we find an interpretation J that behaves as I w.r.t. the query q, and whose cost is also ≤k, with all violations concentrated in a predictable portion of its domain. This portion of the domain of J is of course small, since the maximum number of violations is k, thus involving at most 2k distinct elements. By ‘predictable’, we mean that these violations take place among a small number of special individuals (constant number with respect to k) that can easily be identified, and on a small set of additional domain elements. To identify these special individuals, we rely on the following intuition: if an ABox type t is realized more than 2k times in A, then there is a way to complete t without any ‘local’ violation. Indeed, if it was impossible to do so, then t being realized more than 2k times would always result in more than k violations and thus in a cost exceeding k, contradicting the very existence of I. Therefore, only individuals with a rare ABox type may require a special treatment to keep the cost less than k. Formally, we say that an ABox type t is rare in A if #{a ∈Ind(A) | tpA(a) = t} ≤2k, and we use RT(A) for the set of rare ABox types in A.

Now, when we start from an interpretation I with cost ≤k and attempt to build J, we preserve the interpretation of concepts and roles from I on those special individuals that have a rare ABox type. For J to behave like I with respect to the query q, we also preserve the interpretation on individuals occurring in q. We define the pre-core pc(A) as the set of individuals from A that have a rare ABox type, plus those query-related individuals, that is:

pc(A):= {a | tpA(a) ∈RT(A)} ∪Ind(q). Unfortunately, the pre-core does not contain all the individuals that may be forced to participate in violations. As the following example illustrates, elements ‘close’ to the precore may also be forced to do so. Example 1. Consider the fixed cost k:= 3 and the ABox A:= {A(a0)}∪S7 i=0{r(ai, bi), t(bi, ci)}. The ABox type of a0 is rare, others are not. Consider the TBox T with axioms:

A ⊑∃u ⊓¬∃s ∃u−⊑∃r−⊓¬∃s− ∃t ⊑∃s− r ⊑s and assign cost 1 to all t assertions, cost 2 to axiom r ⊑ s, and infinite cost to other assertions and axioms. Every interpretation with cost ≤3 violates the assertion t(b0, c0), which is somewhat surprising as both involved individuals have ABox types that can otherwise be instantiated in a way that does not violate anything. However, b0 and c0 happen to be ‘close’, i.e. at distance less than k = 3, to a0. The rare type of a0 can then impact b0 and c0 as seen above.

To capture those individuals that may be affected by elements from the pre-core, we essentially explore the neighbourhood of the latter. For a, b ∈Ind(A), we write a ⇝1 b if there exists a role r ∈N±

R and an assertion r(a, b) in A and ∃>kr /∈tpA(a). When exploring neighbours, the reason we exclude roles r such that ∃>kr ∈tpA(a) comes from Lemma 7: it guarantees that element a satisfies ∃r, so the potential violations on a do not impact the r-edges to b. We then denote a ⇝i+1 c if there exists b such that a ⇝i b and b ⇝1 c. The core of A, denoted core(A), is now defined as:

core(A):= pc(A) ∪{b | a ⇝i b, a ∈pc(A), i ≤k + 1}. Notice that we stop the exploration of the neighbourhood of pc(A) at depth k + 1. This is simply because the special behaviour of a pre-core element can only “cascade” to neighbours by enforcing a violation at each layer; thus, impacted elements cannot be further than (k + 1)-away.

18958

<!-- Page 7 -->

We can now state our key technical lemma. Note that Points 5p and 5c are used respectively to handle the possible and certain semantics. Recall that Theorem 7 established coNP-hardness for CQAk c, which is why Point 5c only concerns the case where q is an IQ. Lemma 8. Let K = (T, A)ω be a WKB, q a BCQ, and k a fixed cost. If there exists an interpretation I with cost ≤k, then there exists an interpretation J such that:

1. ∆J = Ind(A) ∪W for some W ⊆{wt | t is a 1-type}; 2. J |pc(A) = I|pc(A); 3. ω(J) = ω(J |core(A)∪W); 4. ω(J) ≤k; 5p. If I |= q, then J |core(A)∪W |= q (and thus J |= q); 5c. If q is an IQ and I̸ |= q, then J̸ |= q.

## 6.2 Construction of the FO-Rewriting

Consider a DL-LiteH bool TBox T, a weight function ωT for T, fixed cost k, and BCQ q. We now proceed to the actual construction of the rewritten query q′. Notice that the pre-core always has size at most P0:= 2k×2|NC(T)|+4|NR(T)|+|q| (at most 2k copies of each rare ABox type, plus the individuals in q). For each individual a, there exist at most 2k|NR(T)| distinct individuals b such that a ⇝1 b. Therefore, the size of every core, regardless of the specific ABox, is bounded by P0 ×(2k|NR(T)|)k. We let MT,q,k be the above quantity plus the number of possible 1-types, that is:

MT,q,k:= P0 × (2k|NR(T)|)k + 2|NC(T)|+2|NR(T)|

The number MT,q,k gives an upper bound on the maximal size of the domain core(A)∪W involved in the construction of interpretation J in Lemma 8. Note that Points 3, 5p and 5c also guarantee that core(A) ∪W contains all the relevant information regarding violations and query satisfaction.

The rewritten query q′ considers each relevant interpretation M, up to isomorphism, whose domain ∆M has size at most MT,q,k and tries to match the ‘individual part’ of M (that is, the core(A) part, as opposed to the W part) in the input AωA. The rewriting must also check that each remaining individual from AωA can be interpreted in a manner that is compatible w.r.t. the considered M, in the sense that it shall not introduce any violations (nor satisfy the query, in the case of the certain semantics). To achieve this, we specify along with M its intended individual part as a subdomain Γ ⊆∆M and the allowed ABox violations as a weighted ABox Vν. We call such a triple (M, Γ, Vν) a strategy for (TωT, q, k) if Ind(V) ⊆Γ and ωT (M) + P α∈V ν(α) ≤k. We differentiate between p-strategies, used for CQAk p, and c-strategies, used for IQAk c. A p-strategy is a strategy (M, Γ, Vν) that additionally satisfies M |= q. An ABox type t is p-safe for a p-strategy σ = (M, Γ, Vν) if there exists a 1-type t′ such that: 1. for every A ∈NC(T), if A ∈t, then A ∈t′; 2. for every r ∈N± R (T), if ∃r ∈t, then ∃r ∈t′; 3. t′ does not violate any CIs from T; 4. for every r ∈N± R (T), if ∃r ∈t′, then ∃s ∈t′ for every s ∈N±

R (T) with r ⊑T s;

5. for every r ∈N± R (T), if ∃r ∈t′, then there exists d ∈∆M such that for every s ∈N±

R (T) with r ⊑T s, we have ∃s−∈tpM(d). Recall that we need only to define c-strategies for the case where q is an IQ. We may assume w.l.o.g. that q is a concept IQ1. A c-strategy for (TωT, q, k) is a strategy σ = (M, Γ, Vν) such that Ind(q) ⊆Γ and M̸ |= q, and an ABox type t is c-safe for σ if there exists a 1-type t′ that satisfies Conditions 1–5 of p-safe types, plus the following condition: 6. if q = ∃y A(y), then A /∈t′. The rewritten FO-query q′ is now obtained as the disjunction of subqueries qσ, where each σ is a p-strategy (resp. cstrategy) for (TωT, q, k). Now, for a given σ:= (M, Γ, Vν), the subquery qσ uses one existentially quantified variable vd for each d ∈Γ, and attempts to identify a subpart of the input weighted ABox AωA that could be interpreted as M|Γ, up to the violations described in Vν. For example, if d /∈AM and A(d) ∈V, then qσ contains the following subquery A(vd) →Wν(A(d))

A (vd), enforcing that variable vd can only be mapped on an individual a such that A(a) ∈A if ωA and ν agree on the cost of the assertion A(a). Using a universally quantified variable, qσ also makes sure that all other individuals in A have an ABox type that is p-safe (resp. c-safe) w.r.t. σ. It is indeed clear, examining the very local requirements defining safe types that ‘having a safe p- (or c-) type’ can be verified using an appropriate FO-subquery.

In this manner, we can construct FO-queries q′ p and q′ c, respectively based on p- and c-strategies, such that the following properties hold, concluding the proof of Theorem 8: Lemma 9. Let TωT be a weighted DL-LiteH bool TBox, k an integer, and q a BCQ. For every weighted ABox AωA:

(T, A)ωT ∪ωA |=k p q iff IAωA |= q′ p. Furthermore, if q is an IQ, then:

(T, A)ωT ∪ωA̸ |=k c q iff IAωA |= q′ c.

## Conclusion

Our results significantly improve our understanding of the data complexity of query entailment under recently introduced cost-based semantics. In particular, we have proved a ∆p

2 upper bound for the optimal-cost certain and possible semantics, yielding tight complexity bounds for a wide range of lightweight and expressive DLs, up to ALCHIO and covering also prominent DL-Lite dialects. Moreover, we obtained surprising tractability results, showing that fixed-cost possible semantics (for CQs) and certain semantics (for IQs) in DL-LiteH bool enjoy the same low AC0 complexity as classical CQ answering in DL-Lite. We expect our upper bounds can be adapted to also handle negative role inclusions (to cover also DL-LiteR). For DLs with functionality or number restrictions, it does not suffice to work with finite interpretations, so wholly different methods are required. Developing a practical implementation of the FO-rewritings for the identified tractable cases is another interesting direction.

1IQs of the form ∃y r(a, y) (resp. ∃xy r(x, y)) can be handled by adding infinite-weight CIs ∃r ⊑B, B ⊑∃r for a fresh concept name B, and using the IQ B(a) (resp. ∃x.B(x)) instead.

18959

<!-- Page 8 -->

## Acknowledgments

The authors acknowledge the financial support of the ANR AI Chair INTENDED (ANR-19-CHIA-0014) and the Federal Ministry of Research, Technology and Space of Germany and by S¨achsische Staatsministerium f¨ur Wissenschaft, Kultur und Tourismus in the programme Center of Excellence for AI-research “Center for Scalable Data Analytics and Artificial Intelligence Dresden/Leipzig”, project identification number: ScaDS.AI.

## References

Baader, F.; Horrocks, I.; Lutz, C.; and Sattler, U. 2017. An Introduction to Description Logic. Cambridge University Press. Bienvenu, M. 2020. A Short Survey on Inconsistency Handling in Ontology-Mediated Query Answering. K¨unstliche Intell., 34(4): 443–451. Bienvenu, M.; and Bourgaux, C. 2016. Inconsistency- Tolerant Querying of Description Logic Knowledge Bases. In Reasoning Web Tutorial Lectures. Bienvenu, M.; Bourgaux, C.; and Jean, R. 2024. Cost-Based Semantics for Querying Inconsistent Weighted Knowledge Bases. In Proceedings of KR. Bienvenu, M.; and Ortiz, M. 2015. Ontology-Mediated Query Answering with Data-Tractable Description Logics. In Reasoning Web Tutorial Lectures. Bonatti, P. A.; Lutz, C.; and Wolter, F. 2009. The Complexity of Circumscription in DLs. J. Artif. Intell. Res., 35: 717–773. Bourgaux, C. 2016. Inconsistency handling in ontologymediated query answering. (Gestion des incoh´erences pour l’acc`es aux donn´ees en pr´esence d’ontologies). Ph.D. thesis, University of Paris-Saclay, France. Britz, K.; Casini, G.; Meyer, T.; Moodley, K.; Sattler, U.; and Varzinczak, I. 2021. Principles of KLM-style Defeasible Description Logics. ACM Trans. Comput. Log., 22(1): 1:1– 1:46. Calvanese, D.; De Giacomo, G.; Lembo, D.; Lenzerini, M.; and Rosati, R. 2007. Tractable Reasoning and Efficient Query Answering in Description Logics: The DL-Lite Family. Journal of Automated Reasoning (JAR). Eiter, T.; Lukasiewicz, T.; and Predoiu, L. 2016. Generalized Consistent Query Answering under Existential Rules. In Proceedings of KR. Giordano, L.; Gliozzi, V.; Olivetti, N.; and Pozzato, G. L. 2013. A non-monotonic Description Logic for reasoning about typicality. Artif. Intell., 195: 165–202. Lembo, D.; Lenzerini, M.; Rosati, R.; Ruzzi, M.; and Savo, D. F. 2010. Inconsistency-Tolerant Semantics for Description Logics. In Proceedings of RR. Lutz, C.; and Mani`ere, Q. 2024. Adding Circumscription to Decidable Fragments of First-Order Logic: A Complexity Rollercoaster. In Proceedings of KR, 531–541. Mani`ere, Q. 2022. Counting queries in ontology-based data access. (Requˆetes de comptage pour l’acc`es aux donn´ees en pr´esence d’ontologies). Ph.D. thesis, University of Bordeaux, France. Poggi, A.; Lembo, D.; Calvanese, D.; De Giacomo, G.; Lenzerini, M.; and Rosati, R. 2008. Linking Data to Ontologies. Journal of Data Semantics, 10: 133–173. Xiao, G.; Calvanese, D.; Kontchakov, R.; Lembo, D.; Poggi, A.; Rosati, R.; and Zakharyaschev, M. 2018. Ontology- Based Data Access: A Survey. In Proceedings of IJCAI.

18960
