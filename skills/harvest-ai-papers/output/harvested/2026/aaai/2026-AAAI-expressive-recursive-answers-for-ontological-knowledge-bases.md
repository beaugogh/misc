---
title: "Expressive Recursive Answers for Ontological Knowledge Bases"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38963
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38963/42925
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Expressive Recursive Answers for Ontological Knowledge Bases

<!-- Page 1 -->

Expressive Recursive Answers for Ontological Knowledge Bases

Luca Andolfi, Gianluca Cima, Marco Console, Maurizio Lenzerini

Sapienza University of Rome {andolfi, cima, console, lenzerini}@diag.uniroma1.it

## Abstract

A fundamental use of knowledge bases (KBs) is query answering, i.e., retrieving the information entailed by the KB in response to a user query. When both the KB and the query are specified as logical formulae, the standard form of answer provided to users is certain answers (CAs): tuples of constants that satisfy the query in every model of the KB. Despite their wide adoption, CAs are known to be just a lossy representation of the information that a KB and a query provide. However, while several alternative forms of answers have been proposed, no general consensus has emerged on the most suitable approach to answer queries over ontological KBs. In this paper, we introduce Regularly Recurrent Answers (RRAs), a novel form of answer for queries over ontological KBs. RRAs support the representation of infinite sets of tuples via a generation mechanism based on regular expressions. Such a simple mechanism allows RRAs to represent a fundamental fragment of the certain information entailed by Unions of Conjunctive Queries over DL-Lite KBs. The contribution of this paper includes the formal definition of RRAs, a formal characterization of their informativeness, and a study of their computational characteristics.

## Introduction

A knowledge base (KB) is a symbolic representation of a domain of interest, formulated in a formal language and equipped with semantics (i.e., a set of mathematical objects representing its meaning). One of the most important tasks performed with a KB is, arguably, query answering (Calvanese et al. 2007; Bienvenu and Ortiz 2015). At the most general level, query answering amounts to extracting from a KB the information requested by a user (a query) and constructing a suitable syntactic object (an answer) that represents that information. In fact, one can view query answers simply as representations of the information required by a query and, as such, they come with their own syntax and semantics (i.e., an answer language). Depending on the answer language adopted, a query answering system can provide more or less accurate answers to a query.

Hereinafter, we adopt the logical approach to KBs (Reiter 1980; Levesque and Lakemeyer 2001) in which information

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

is represented by a logical theory, and the models of this theory constitute the semantics of the KB. In this approach, a query is defined by a logical formula, and answers consist of (a representation of) the individuals that satisfy this formula in the models of the KB. When the KB has only a single finite model (e.g., in the case of relational databases (Abiteboul, Hull, and Vianu 1995)), it is customary to answer a query by returning the set of all tuples of constants that satisfy it in that model. Such a simple answer language (i.e., finite sets of tuples of constants) usually suffices to convey all the information requested by the queries.

In many application scenarios, however, KBs have multiple (and sometimes infinite) models. This is the case, e.g., for incomplete databases (Abiteboul, Hull, and Vianu 1995), data integration and exchange (Lenzerini 2002), and ontology-based data access and ontology-mediated query answering (Calvanese et al. 2007; Cal`ı, Gottlob, and Kifer 2008; Bienvenu and Ortiz 2015). In all these settings, the literature often focuses on Boolean queries and, essentially, reduces query answering to logical entailment. In concrete applications, however, users are often interested in more than just yes/no answers. To solve these cases, a prominent approach is to use the same tuple-based answer language and return certain answers (CAs), i.e., sets of tuples of constants that satisfy the query in every model of the KB. Introduced in the late 1970s (Lipski 1979), CAs have become the de facto standard for query answering over KBs across different domains. Example 1. Consider the Description Logic KB K = ⟨T, A⟩, where A = {hS(Ava, Bea)} and T is defined as

(1) E ⊑∃hS (2) ∃hS−⊑S (3) S ⊑E

Informally, K states that each employee is assigned to a supervisor (1), every supervisor is an employee (2) −(3), and Bea is the supervisor of Ava (A).

To retrieve the information about employees and their supervisors, we could issue the query q = {(x, y) | hS(x, y)}. The CAs for q over K is the set CA(q, K) = {(Ava, Bea)}.

Despite their wide adoption, CAs are far from ideal for KBs with multiple models (Libkin 2016). Since the answer language used is too simple, CAs can represent only a small portion of the information that a query actually requires. To see this, consider again Example 1 and observe that the information that someone supervises Bea is certain in K (i.e.,

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

18928

<!-- Page 2 -->

true in all its models). Clearly, one would expect such information in the answer for q, but there is no mention of it in CA(q, K). Upon inspecting such an answer, users could be even tempted to conclude that Bea has no supervisor, effectively subverting the meaning of the theory and the query.

## Limitations

of CAs are well known in the literature and have been studied extensively in the context of databases (Console et al. 2020), but they have been left largely unexplored for more complex KBs with only a few notable exceptions. The work in (Borgida, Toman, and Weddell 2016) introduces referring expressions (RefExp): an answer language that uses Description Logic (DL) constructs to describe unnamed individuals. While RefExp provide more intuitive (and therefore usable) answers to users, issues arise when one wants to use them to capture more information coming from the query (see Section 3 for additional details). Specifically, to obtain a full answer, one may need to return infinitely many and often redundant such descriptors (Toman and Weddell 2019). While this issue can be partially mitigated via regular expressions, the case of Unions of Conjunctive Queries (UCQs) and DL languages with role inclusions has not been treated in full.

Inspired by the standard approach of answer-tuples with nulls for incomplete databases (Imielinski and Lipski 1984), the works in (Lutz and Przybylko 2022, 2023) introduce minimal partial answers with multi-wildcards (MPAW), a tuple-based answer language that allows both constants and special symbols (wildcards) to represent unnamed individuals. While such symbols can partially mitigate the information loss in CAs, their expressive power remains limited due to necessary syntactic restrictions.

A more systematic study of the informativeness of answer languages for ontological KBs is presented in (Andolfi et al. 2024) where a formal framework for this purpose is introduced. This framework is based on the simple observation that, in general, the behavior of a query q over a KB K is fully determined by the collection q(K) of sets of tuples of individuals obtained by evaluating q over all the models of K (see, e.g., (Lipski 1979; Imielinski and Lipski 1984) for an early use of this idea). Using q(K), one can define the certain knowledge C entailed by q and K as the set of all formulae (in a given language) that are satisfied by every element of q(K). A good answer for q over K, in terms of certain knowledge, is any symbolic representation that satisfies (i.e., preserves) all the formulae in C. The paper also shows that both CAs and MPAW fail to preserve even a very simple language and propose certain n-answers (CnA, with n ∈N), a novel answer language that mitigates this issue.

Example 2. The set of all MPAW for q over K is {(Ava, Bea), (Bea, ⋆)}. Similarly, the set of all C2A to q over K is {(Ava, Bea), (Bea, ⋆1), (⋆1, ⋆2)}. The semantics of both answers is straightforward: the ⋆-symbols represent tuples of individuals (named or unnamed) that certainly satisfy q. The set of MPAW preserves the information that Bea is supervised by some individual ⋆but not that ⋆is themselves supervised. This additional information is preserved by the set of C2A, where, however, the information that the supervisor ⋆2 of ⋆1 is themselves supervised is lost.

As one may easily deduce from Example 2, none of the previously discussed languages are able to preserve the certain knowledge entailed by q and K that can be expressed in the existential positive fragment of first-order logic (∃Pos). This is a consequence of a more general result from (Andolfi et al. 2024), which shows that no answer language based on finite sets of tuples can preserve such information. This limitation holds even when considering CQs and DL-LiteR KBs.

In light of these observations, we propose a novel answer language that we call regularly recurrent answers (RRAs). The goal of RRAs is to provide a simple yet effective way to represent the infinite sets of tuples required to properly answer UCQs over ontological KBs. To achieve this goal, RRAs employ a mechanism based on regular expressions. We chose regular expressions as the basis for RRAs because they provide a simple, intuitive, and widely accepted mechanism for generating new tuples whose computational properties are well understood. More specifically, each RRA consists of a finite set of regularly recurrent tuples (RRTs): pairs of the form ⟨¯a, ρ⟩, where ¯a is a tuple of terms and ρ is a (set of) regular expression(s) that specifies how to generate other tuples of terms starting from ¯a.

Example 3. Consider again Example 1. An RRA R for q over K consists of RRTs t1 = ⟨(Ava, Bea), ∅⟩and t2 = ⟨(x, s(x)), {[x, ⟨s∗, Bea⟩]}⟩. The semantics of t1 is the set {(Ava, Bea)} while that of t2 is the set of tuples

(Bea, s(Bea)), (s(Bea), s(s(Bea))),...

. The semantics of R is simply the union of the semantics of t1 and t2 and it is easy to observe that R preserves the certain knowledge entailed by q and K that can be expressed in ∃Pos.

The main contribution of this paper is the presentation of an answer language of the kind defined in Example 3 and the study of its computational characteristics. Specifically, our contribution is the following: we introduce RRAs, our novel answer language; we show that, for every UCQ q and DL-LiteR KB K, there always exists an RRA, that we call canonical, whose semantics can be isomorphically mapped into the answers that q obtains over a canonical model of K; we show that canonical RRAs preserve the certain knowledge entailed by q and K that can be expressed in ∃Pos (as defined in (Andolfi et al. 2024)). Finally, we show that computing canonical RRAs is in PTIME in data complexity in the aforementioned scenario.

It is important to emphasize that RRAs are intended as a foundational theoretical contribution to the study of expressive answer languages. We are aware that, in their current form, RRAs are not yet suited for direct interaction with end users: raw regular expressions are unlikely to align with the expectations and needs of non-experts. Nonetheless, establishing the expressive power required to represent answers provides a solid theoretical basis for further research in this area. In particular, future studies on usability can build on this foundation and draw from the extensive literature on the visual presentation of regular languages (Beck et al. 2017).

Organization Section 2 introduces preliminary notions and provides a concise overview of the framework for informativeness presented in (Andolfi et al. 2024). RRAs are presented in Section 3 where we also compare them to other

18929

<!-- Page 3 -->

languages from the literature. Then Section 4 is devoted to proving informativeness of RRAs for UCQs over DL-LiteR KBs while Section 5 studies the computational properties of relevant problems. In Section 6 we conclude.

## 2 Preliminaries

We fix three countably infinite and pairwise disjoint sets of symbols ΣC, ΣV, and ΣF, for constants, variables, and unary functions, respectively. The set ΣT of terms is defined inductively as follows: (i) every t ∈ΣC ∪ΣV is in ΣT; (ii) for every t ∈ΣT and f ∈ΣF, f(t) ∈ΣF.

We will often write a term f1(f2(... (fk(c))...)) simply as f1f2... fk(c) (dropping parenthesis); abbreviate a sequence of function symbols f1f2... fk as ¯f; and use ¯g ¯f(t) for the term defined by the composition of the sequences of function symbols ¯g and ¯f applied to the term t. Additionally, given a term t = f1f2... fk(k), with k ∈ΣC ∪ΣV, we call f1 the leading function symbol of t, the sequence f1f2... fk of function symbols of t the word of t, and c the base of t. Finally, given a function µ: ΣV →ΣV ∪ΣC and a term t = ¯g(k), with k ∈ΣV ∪ΣC, µ(t) is the term ¯g(µ(k)), if k is a variable, and t itself, if k is a constant.

Regular Expressions. A regular expression χ over ΣF (regex) is defined by the syntax: χ::= ∅| f | χ1χ2 | (χ1 + χ2) | χ∗, where f ∈ΣF. The language L(χ) defined by a regex χ is the subset of Σ∗

F defined as customary.

First-order Logic A predicate symbol P is a symbol not in ΣC ∪ΣV ∪ΣF with an associated integer ar(P) ≥0 called its arity. For a set of predicate symbols S, FO(S) denotes the set of all function-free first-order formulae built using symbols of S, ΣC, and ΣV. We will use ∃Pos(S) for the sub-language of FO(S) without free variables (sentences) of the form W i ∃¯xi.φi(¯xi), where each φi(¯xi) is a conjunction of atomic formulae using constants from ΣC and variables from ¯xi. A first-order interpretation for a set of predicate symbols S (simply, interpretation for S or interpretation) is a pair I = ⟨ΣT, ·I⟩where ·I is a function s.t. cI = c, for each c ∈ΣC, and P I ⊆Σn

T, for each P ∈S with ar(P) = n. Interpretations do not consider functions in ΣF and enforce the standard names assumption over constants (Levesque and Lakemeyer 2001). An interpretation I = ⟨ΣT, ·I⟩for S and a mapping µ: ΣV →ΣT satisfy φ ∈FO(S) (written I, µ |= φ) in the usual sense. If φ is a sentence, I |= φ denotes I, µ |= φ, for each µ: ΣV →ΣT.

Morphisms Given interpretations I, J for S, a homomorphism from I to J is a mapping h: ΣT →ΣT s.t., h(¯a) ∈RJ, for each ¯a ∈RI and R ∈S. A homomorphism h is constant-preserving if it is the identity over ΣC and an isomorphism if it is bijective and h−1 is a homomorphism.

Queries A n-ary query q for a set of predicates S is an expression of the form q(¯x) = {¯x | φ(¯x)}, where ¯x ∈Σn

V and φ(¯x) ∈FO(S) is a formula whose free variables occur in ¯x. We use ΣV(q) for the set of all variables occuring in φ(¯x). Given an interpretation I for S, an answer tuple for q over I is a tuple µ(¯x) such that I, µ |= φ(¯x). A query language Q is a collection of queries, and conjunctive queries (CQs)

and their unions (UCQs) are languages defined as customary in the literature. Additionally, we will use connected CQs (CCQs), i.e, CQs for which the Gaifman graph of the defining formula is connected. It is well known that ¯a is an answer tuple for a UCQ q(¯x) over an interpretation I if there exists a homomorphism from (the canonical interpretation of) of a disjunct of q(¯x) into I that maps ¯x into ¯a. We call such homomorphisms the supports of ¯a and q over I.

Knowledge Bases (KBs) We assume the reader is familiar with Description Logics KBs and refer to (Calvanese et al. 2007) for additional details on DL-LiteR. Let ΣP be a countably infinite set of predicate symbols partitioned into the disjoint sets ΣA of atomic concepts (unary predicates) and ΣR of atomic roles (binary predicates). A KB is a pair ⟨T, A⟩ where T (TBox) is a finite set of TBox axioms using predicates in ΣP, and A (ABox) is a finite set of ABox axioms using predicates in ΣP and constants in ΣC. Additionally, we define the query languages CCQ, CQ, and UCQ, respectively, as those CCQs, CQs, and UCQs using only predicates in ΣP. Semantics for KBs is given as customary using interpretations: we define a model of a KB K as an interpretation I for ΣP that satisfies all the axioms of K (written I |= K), and use mod(K) for the set of all models of K.

## 2.1 A Framework for Informativeness

We now briefly recall the framework presented in (Andolfi et al. 2024) for analyzing the informativeness of query answers. At a high level, the framework is grounded on a simple intuition: given a query q and a KB K, the collection q(K) of all sets of answers that q yields over the models of K (Imielinski and Lipski 1984) describes all the information that q can possibly retrieve from K. Given a Query Answering System (i.e., a formal model of a concrete query answering mechanism), we ask what portion of the information in q(K) is actually returned by it.

Next, we define the collection q(K) formally. To this end, we define semantics for logical queries using interpretations. Let Σans be the countably infinite set of predicates S∞ i=0{ansi} where each ansi has arity i and does not occur in ΣP. Given an n-ary query q and a KB interpretation I, the complete answer for q over I is the interpretation for Σans q(I) = ⟨ΣT, ·q(I)⟩such that: (i) ansq(I)

n is the set of all the answer tuples for q over I; and (ii) ansq(I)

j = ∅, for each j̸ = n. Given a KB K, the complete answer for q over K is defined as q(K) = {q(I) | I ∈mod(K)}. Intuitively, q(K) contains all the information that q can retrieve form K.

In principle, to be maximally informative, a query answering mechanism should return the whole q(K). This is, however, impossible since such a collection may easily become infinite. In these cases, query answering mechanisms return a representation of q(K) in some language. Next, we provide a general model of such representations. An answer domain is a pair D = ⟨D, |=D⟩such that D is a set of syntactic objects (abstract answers) and |=D⊆D × FO(Σans) is a satisfaction relation over D. Intuitively, D contains all the answers that a query answering mechanism using D may provide, i.e., the answer language, while |=D provides semantics for such objects in terms of the alphabet used for

18930

<!-- Page 4 -->

q(K). The next definition provides a formal model of query answering mechanisms.

Definition 1. Let Q be a query language, K a KB language, and D = ⟨D, |=D⟩an answer domain. A query answering system (QAS) for Q over K with answers in D is a tuple ⟨Q, K, D, eval⟩where eval is a function from Q × K to D.

Intuitively, eval (evaluation function) characterizes the answers that the query answering mechanism modeled by a QAS provides for every pair of query and KB.

Definition 2. Let S be the QAS ⟨Q, K, ⟨D, |=D⟩, eval⟩and let F ⊆FO(Σans). We say that S preserves the certain knowledge definable in F if, for each q ∈Q, K ∈K, and φ ∈F, the following holds: eval(q, K) |=D φ if and only if A |= φ, for each A ∈q(K).

We can now formally state our main goal. Specifically, in what follows we present a QAS for UCQ over DL-LiteR that preserves the certain knowledge of ∃Pos(Σans).

## 3 Regularly Recurrent Answers

We now introduce our novel answer language and use it to define a family of QAS for UCQ over DL-LiteR KBs that preserve the certain knowledge definable in ∃Pos(Σans). Firstly, we define suitable objects for the answer domain.

Definition 3. A term expression τ is an expression of the form ⟨χ, c⟩where c ∈ΣC and χ is a regular expression over ΣF. The semantics JτK of τ is the set of all terms t ∈ΣT such that the base of t is c and the word of t belongs to L(ρ).

Example 4. Let τ = ⟨(c + s)∗, Ava⟩with c, s ∈ΣF and Ava ∈ΣC. The semantics of τ is the set JτK of all terms f1(... (fk(Ava))...) s.t. fi ∈{c, s}, for each i ∈[k].

Our goal is to use term expressions to represent sets of tuples whose terms are defined by their semantics. To formalize this intuition, we need to introduce additional notation.

A substitution rule ρ is an expression of the form ρ = [x, τ] where x ∈ΣV and τ is a term expression, and a substitution set is a finite set of substitution rules with distinct variables. Given a substitution set S, a substitution function for S is a function f: ΣV →ΣT such that f(x) ∈JτK, for each x ∈ΣV for which [x, τ] ∈S. The following definition introduces the basic building block of our answer language.

Definition 4. A regularly recurrent tuple (RRT) is an expression of the form ⟨¯a, S⟩where ¯a is a tuple of terms and S is a substitution set such that, for every variable x in ¯a, there is a substitution rule [x, τ] in S.

Additionally, we define the arity of an RRT r = ⟨¯a, S⟩ as the arity of ¯a. Intuitively, r acts as a placeholder for the tuples of terms that can be obtained by applying S over ¯a.

Definition 5. Let r = ⟨(t1,..., tn), S⟩be an RRT. The semantics JrK of r is the following set of tuples: { f(t1),..., f(tn)

| f is a substitution function for S}.

It should be clear that J⟨¯a, S⟩K contains no variables since each variable in ¯a has an associated substitution rule in S.

Example 5. Let r = ⟨¯a, {ρ}⟩, where ¯a = (x, s(x), d(x)) and ρ = [x, τ] with τ as in Example 4. The semantics

JrK of r is the set of all the tuples (t1, t2, t3) such that, for some n ∈N and f1,..., fn ∈{c, s} we have: t1 = f1(... (fn(Ava))...), t2 = s(t1), t3 = d(t1).

We will call a finite set of RRTs of the same arity a regularly recurrent answer (RRA), and define the arity ar(R) of an RRA R as the arity of its elements. The following definition provides a formal semantics to RRAs. Definition 6. The semantics JRK of an RRA R is the interpretation ⟨ΣT, ·R⟩for Σans such that ansR i = S r∈RJrK, for i = ar(R), and ansR i = ∅, for every i̸ = ar(R). RRAs will be the answer domain of the family of QASs we are constructing. To this end, we need a suitable satisfaction relation: an RRA R satisfies a formula φ ∈FO(Σans) if JRK |= φ. We use |=RRA for the satisfaction relation we just introduced, and we define the answer domain RRA = ⟨R, |=RRA⟩, where R is the family of all RRAs. Example 6. Consider the RRA R = {r}, where r is defined as in Example 5. Then, R̸ |=RRA φ1 and R |=RRA φ2 where φ1 = ∃x1, x2.Ans3(x1, x2, x2) and φ2 = ∃x1, x2, x3, x4.Ans3(Ava, x1, x2) ∧Ans3(x1, x3, x4).

With our answer domain in place, we are now ready to define a query evaluation function for our QAS. To this end, we define a special family of RRAs that we call canonical. Definition 7. Let q be a query and K a KB. An RRA R is canonical for q over K if the following conditions hold: 1. for every I ∈mod(K), there is a constant-preserving homomorphism from JRK to q(I); and 2. there exists I ∈mod(K) such that JRK = q(I). Example 7. Consider the ABox A′ = {E(Ava)} and the TBox T ′ that extends T from Example 1 with the following:

(4) E ⊑∃hC (5) ∃hC−⊑E (6)E ⊑∃hD The additional axioms state that every employee has as coach (4) that is an employee (5), and every employee belongs to a department (6). The following query asks for all the employees with their supervisors and departments:

q(x, y, z) = {(x, y, z) | E(x) ∧hS(x, y) ∧hD(x, z)} One can show that R from Example 7 is a canonical RRA for q over ⟨T ′, A′⟩. Intuitively, this is because, in every model of the KB, there is an employee (Ava), their supervisor (s(Ava)), their department (d(Ava)), and all the other pairs induced by the axioms in T.

If we add E(Bea) to A′, R is not canonical anymore. This is because, in every model I of the new KB, q(I) will contain also the information relative to Bea. To obtain a canonical RRA for the new KB, one could add to R the RRT ⟨(y, s(y), d(y)), ⟨y, τ⟩⟩with τ = ⟨(c + s)∗, Bea⟩.

In general, there is no guarantee that a canonical RRA for a given pair of query and KB exists due to the finiteness requirements we impose. A QAS ⟨Q, K, RRA, eval⟩is called RRA-canonical if eval(q, K) is a canonical RRA for q over K, for every pair of q ∈Q and K ∈K. The following claim follows from the definition of canonical RRAs. Theorem 1. Every RRA-canonical QAS preserves the certain knowledge definable in ∃Pos(Σans).

The goal of Section 4 will be to show that an RRAcanonical QAS for UCQ over satisfiable DL-LiteR exists.

18931

<!-- Page 5 -->

## 3.1 RRAs and Other Answer Languages

Before concluding this section, we compare RRAs with other answer languages from the literature. As we pointed out in the introduction, results in (Andolfi et al. 2024) show that a QAS for UCQ over DL-LiteR whose answers can be represented as finite interpretations for Σans cannot preserve the certain information definable in ∃Pos(Σans). In turn, Theorem 1 implies that an RRA-canonical QAS is strictly more expressive than those based on certain n-answers or minimal partial answers with multi-wildcards.

An answer language that is close in spirit to RRAs are Referring Expressions (RefExpr) as defined in (Toman and Weddell 2019). Indeed, following the construction from that work, one can obtain a QAS for Conjunctive Queries (CQs) over ALC ontologies which preserves the certain information definable in ∃Pos(Σans). However, RefExprs present issues that make them unsuitable for our context. Firstly, the singularity requirement of Definition 5 from (Toman and Weddell 2019) is easily violated if role inclusion assertions are allowed in the TBox. As a result, in these cases one may easily end up with no RefExprs for unnamed individuals in the answers. Secondly, the same unnamed individual may satisfy more than one RefExpr. To avoid redundant information, one needs to compute ABox closures, which is usually expensive in terms of space and time.

Finally, the information provided by an RRA cannot, in general, be reconstructed by computing the CAs of finitely many Boolean queries to the KB. For simplicity, consider the KB in Example 1. To discover that Ava’s supervisor has a supervisor, one could issue the Boolean query ∃x, y.hS(Ava, x) ∧hS(x, y) and, upon receiving a nonempty answers, conclude that such an individual certainly exists. However, if the user is interested in ascending the chain of supervisors further, they would need to issue additional queries. If the ontology is unknown to them, there seems to be no straightforward way to conclude that such a chain is infinite. On the contrary, it is easy to observe that a canonical RRA {⟨(x, s(x)), {[x, ⟨s∗, Ava⟩]}⟩} for the query {(x, y) | hS(x, y)} conveys such information.

## 4 RRA-Canonical QAS for UCQ in DL-LiteR

This section is devoted to the proof of the following theorem.

Theorem 2. There exists an RRA-canonical QAS for UCQ over the language of satisfiable DL-LiteR KBs.

Theorem 2 and Theorem 1 together prove our main result: there exists a QAS for UCQ over DL-LiteR KBs that preserves the certain knowledge definable in ∃Pos(Σans). To construct such a QAS, we rely on the notion of canonical model of a DL-LiteR KB. In this work, a canonical model for a DL-LiteR KB K is an interpretation C = ⟨ΣT, ·C⟩for ΣP s.t. C ∈mod(K), and, for every I ∈mod(K), there exists a constant-preserving homomorphism from C to I.

Lemma 1. Let K be a DL-LiteR KB, C a canonical model for K, and q ∈UCQ. If an RRA R is such that JRK = q(C), then R is canonical for q over K.

To prove Theorem 2, we rely on Lemma 1 in the following way. Given a DL-LiteR KB K, we construct a specific type of forest-like canonical model C for K and show that C admits a finite representation highlighting its recurrent patterns. Then, given q ∈UCQ, we construct an RRA R that represents all those recurrent patterns of C that satisfy q and show that indeed JRK = q(C).

The remainder of this section is split in two parts: Section 4.1 presents our construction that yields a canonical model. While the construction is rather standard, we provide the main details that are needed to understand the rest of the proof. Then, in Section 4.2, we construct the desired RRA and present its properties.

## 4.1 Forest-Like Canonical Models

Our construction makes use of the set Σ+

P of extended predicates consisting of the following: all symbols in ΣP; all symbols R−, where R is an atomic role; and all symbols ∃P, where P is an atomic role or its inverse. Intuitively, the set of extended predicates contains all the DL-LiteR symbols that can be generated using ΣP.

Next, we introduce graphs of facts (GoF), a convenient family of graphs that we use as a scaffolding for our canonical models. In what follows, a GoF G = {V, E, l} is simply an edge-labeled directed graph whose nodes are terms in ΣT and whose edges are labeled by sets of symbols in Σ+

P. Sometimes we will treat l as a set of pairs and write l′ = l ∪{(e, t)}, with e ∈E and t ∈Σ+

P, for the labeling function such that l′(e) = l(e) ∪{(e, t)}, and l′(e′) = l(e′), for every e̸ = e′ ∈E. Given a graph of facts G, one can construct an equivalent interpretation I(G) as follows.

Definition 8. The interpretation I(G) = ⟨ΣT, ·I(G)⟩associated to a GoF G = (V, E, l) is an interpretation for ΣP s.t CI(G) = {t | e = (t, t) ∈E and C ∈l(e)}, for each atomic concept C ∈ΣP, and RI(G) = {(t1, t2) | e = (t1, t2) ∈ E and R ∈l(e)} ∪{(t2, t1) | e = (t1, t2) ∈E and R−∈ l(e)}, for each atomic role R ∈ΣP.

Similarly, given a DL-LiteR KB K = ⟨T, A⟩, one can construct a GoF G(A) that represents A as follows. The nodes of G(A) are all the constants occurring in A; for each constant c occurring in A, G(A) has an edge (c, c) whose label consists of all P ∈ΣP such that P(c) ∈A, all symbols R ∈ΣP such that R(c, c) ∈A, all symbols ∃R ∈Σ+

P, such that R(c, d) ∈A, and all symbols ∃R−∈Σ+

P, such that R(d, c) ∈A; for each pair of distinct constants c, b occurring in A, G(A) has an edge (c, b) whose label consists of all symbols P ∈ΣP such that P(c, b) ∈A.

Given a DL-LiteR KB K = ⟨T, A⟩, our goal is now to construct a GoF GK from G(A) such that I(GK) is a canonical model of K. To this end, we use the notion of unraveling, a specialization of the Skolem chase (Calvanese et al. 2007; Marnette 2009) for graphs of facts.

Let T be a DL-LiteR TBox T. To each axiom γ ∈T, we associate a distinct function symbol sγ ∈ΣF and an unraveling rule ργ. An unraveling rule is an expression of the form α ⇝β where both α and β are of the form X[t1, t2], X is a symbol from Σ+

P, t1, t2 are (not necessarily distinct) terms in ΣT, and all variables in β also occur in α. Unraveling

18932

<!-- Page 6 -->

γ ργ A ⊑B A[x, x] ⇝B[x, x] A ⊑∃R A[x, x] ⇝R[x, sγ(x)] A ⊑∃R− A[x, x] ⇝R−[x, sγ(x)] ∃R ⊑A ∃R[x, x] ⇝A[x, x] ∃R ⊑∃S ∃R[x, x] ⇝S[x, sγ(x)] ∃R ⊑∃S− ∃R[x, x] ⇝S−[x, sγ(x)] ∃R−⊑A ∃R−[x, x] ⇝A[x, x] ∃R−⊑∃S ∃R−[x, x] ⇝S[x, sγ(x)] ∃R−⊑∃S− ∃R−[x, x] ⇝S−[x, sγ(x)] R ⊑S R[x, y] ⇝S[x, y] R ⊑S− R[x, y] ⇝S−[x, y] R−⊑S R−[x, y] ⇝S[x, y] R−⊑S− R−[x, y] ⇝S−[x, y]

**Table 1.** Unraveling Rules

rules for DL-LiteR are given in Table 1, where x, y ∈ΣV, A, B are atomic concepts, and R, S are atomic roles.

Next, we define how unraveling rules are applied. For X ∈Σ+

P, the inverse of X (denoted by inv(X)) is defined as follows: inv(X) = X, if X is an atomic concept; inv(X) = X−, if X is an atomic role; inv(X) = ∃R−, if X = ∃R and R is an atomic role; inv(X) = R, if X = R−; and inv(X) = ∃R, if X = ∃R−. Similarly, the existential qualification of X (ex(X)) is defined as ex(X) = ∃X, if X is an atomic role or its inverse, and ex(X) = P, otherwise.

Let now ρ = P[t1, t2] ⇝Q[t3, t4] be an unraveling rule with t1, t2, t3, t4 not necessarily distinct. A trigger τ for ρ in a GoF G = ⟨V, E, l⟩is a mapping τ: ΣV →V s.t. either (i) (τ(t1), τ(t2)) ∈E and P ∈l((τ(t1), τ(t2))) or (ii) (τ(t2), τ(t1)) ∈E and inv(P) ∈l((τ(t2), τ(t1))). Definition 9. Let τ be a trigger for the unraveling rule ρ = P[t1, t2] ⇝Q[t3, t4] in a GoF G = ⟨V, E, l⟩. The application of τ to G (written τ(G)) is the GoF G′ = ⟨V ′, E′, l′⟩ defined as follows:

• V ′ = {τ(t3), τ(t4)} ∪V; • E′ = {(τ(t3), τ(t4)), (τ(t3), τ(t3)), (τ(t4), τ(t4))}∪E; • l′ = {⟨(τ(t3), τ(t4)), Q⟩}∪{⟨(τ(t3), τ(t3)), ex(Q)⟩} ∪{⟨(τ(t4), τ(t4)), ex(inv(Q)))⟩} ∪l. We can extend the notion of application of a trigger to a whole DL-LiteR TBox T in the natural way: given a GoF G, T (G) is the graph obtained by applying all the triggers for T in G. Clearly, T (G) defines a monotone operator and, thus, we can naturally talk about the least fix point unravel(T, G) of T over a GoF G. Additionally, given a DL-LiteR KB K = ⟨T, A⟩, we use unravel(K) for the GoF unravel(T, G(A)). One can show that unravel(K) yields a canonical model of K as the following lemma shows. Lemma 2. Let K be a satisfiable DL-LiteR KB. Then, I(unravel(K)) is a canonical model for K.

We now argue about the topology of unravel(K). A TBox axiom is non-generative if its unraveling rule contains no function symbols. The T -closure of A is AT = unravel(T0, A), where T0 denotes the set of non-generative axioms in T. The roots of K (R(K)) is the collection of all sub-graphs of AT induced by one of the constants in A.

Lemma 3. Let K = ⟨T, A⟩be a DL-LiteR KB. Then unravel(K) = AT ∪S g′′∈R(K) unravel(T, g′′) and, for every g, g′ ∈R(K) we have: 1. unravel(T, g) is an arborescence (removing self-loops); 2. unravel(T, g) and unravel(T, g′) share no vertexes; 3. For every t, t′ ∈ΣT s.t. there is a path in unravel(T, g) from t to t′, there is a sequence of function symbols ¯g in ΣF for which t′ = ¯g(t).

## 4.2 Answering Queries with Unravelling We are now ready to provide a constructive proof of

Theorem 2. Specifically, we show that, for a DL-LiteR KB K and q ∈ UCQ, there exists an RRA R such that JRK = q(I(unravel(K))). The proof is based on the fact that unravel(K) consists of a collection of isomorphic sub-trees. To identify these sub-trees, we use the notion of replica. Definition 10. Let K be a DL-LiteR KB and let t, t′̸ ∈ΣC be nodes in unravel(K). Then, t′ is a replica of t in K if (i) there exists a path from t to t′ in unravel(K); (ii) the leading function symbol of t and t′ coincide; (iii) and t̸ = t′.

One can easily show that, if t′, t′′ are both replicas of t, then the sub-trees of unravel(K) rooted in the three terms are all isomorphic. This is due to the fact that t, t′, and t′′ are all generated by an application of the same unraveling rule defined by T and, thus, one can show inductively that the same unraveling steps are applied to all of them.

The next step of our construction is to define a replicaaware version of unravel(K). The root of a term t of unravel(K) (denoted by R(t)) is the unique g ∈R(K) such that t occurs in unravel(T, g). We use Anc(t) for the set of vertexes in the unique loop-free path in G = unravel(T, R(t)) from the root of G to t. The replica-level of a term t in K (denoted by lvK(t)) is defined as:

maxt′∈Anc(t)|{t′′ ∈Anc(t′) | t′′ is a replica of t′ in K}|

Definition 11. Let K be a DL-LiteR KB and n ∈N. The nth replica-level of unravel(K) = ⟨V, E, l⟩(unravelr=n(K)) is the sub-graph induced by {v ∈V | lvK(v) ≤n}.

It is easy to observe that, for every g ∈R(K) and n ∈N, unravelr=n(T, g) is a finite arborescence when self-loops are removed. Next, we proceed to identify two distinct types of answers for UCQs over I(unravel(K)). Given an n-ary q ∈UCQ and ¯a ∈Σn

T, a near support of ¯a and q is a support µ of ¯a and q over I(unravel(K)) such that µ(x) occurs in unravelr=0(K), for some x ∈ΣV(q). We use near supports to partition the set of answers for a UCQ in two collections. Definition 12. Let K be a DL-LiteR KB and let q be an n-ary query in UCQ. A tuple ¯a ∈Σn

T is a near answer to q over K if there exists a near support for ¯a and q over I(unravel(K)). Otherwise, ¯a is a far answer to q over K.

It is clear that every ¯a ∈q(I(unravel(K))) is either near or far, depending on the existence of an associated near support. We now show that there exists an RRA whose semantics consists of both. In what follows, we focus on CCQs and discuss the general UCQs at the end of the section. Lemma 4. Let K be a satisfiable DL-LiteR KB, and let q ∈ CCQ with |ΣV(q)| ≤n. Then, ¯a is a near answer to q over

18933

<!-- Page 7 -->

K if and only if there exists a near support µ for ¯a and q over I(unravelr=n(T, A)).

A near RRT for q over K is an RRT r = ⟨¯a, ∅⟩such that there exists a near support for ¯a and q over unravelr=n(K). Next, we turn our attention to far answers. Definition 13. A generator for a DL-LiteR KB K is a term t ∈ΣT for which there exists a term t′ ∈ΣT such that (i) t, t′ appear in unravelr=1(T, A), and (ii) t′ is a replica of t.

From what we said above, a generator marks the beginning of a repeating sub-tree of unravel(K). Characterizing these repetitions is crucial for our proofs. Recall that, if t′ is a replica of t, then t′ = ¯g(t), for some sequence of functions symbols ¯g in ΣF (Item 3 of Lemma 3). Definition 14. Let t = f¯g(c) with c ∈ΣC be a generator in unravel(K) and let f¯g1f¯g(c),..., f¯gkf¯g(c) be its replicas in unravelr=1(T, A). The replica expression of t is the regular expression e(t) = (f¯g1 +... + f¯gn).

Intuitively, the regular expression e(t)f¯g generates the word of every replica of t = f¯g(c) and, thus, it captures some of the terms of unravel(K) that are generated by the axiom that generated t. However, other “copies” of t could be generated by the generators preceding it. To obtain a regular expression for all such terms, we need the following.

Let t be a generator in unravel(K). The generator sequence of t is the sequence ⟨g1,..., gn⟩of generators in the unique path from the root of unravel(R(t)) to t in reverse order w.r.t. how they occur in that path and g1 = t. Observe now that, for each i < j, there is a path from gj to gi in unravel(K). Due to Item 3 of Lemma 3 then, the word of gi is equal to s′ isj, where sj is the word of gj and s′ i is a sub-expression of the word of gi. The word decomposition of t is the sequence of strings ⟨s1,..., sn⟩such that, for each i ∈[n], sisi+1... sn is the word gi, i.e., the i-th term in the generator sequence of t. We are finally ready to provide a regular expression that defines the roots of all sub-trees of unravel(K) generated by the axioms that generated t. Definition 15. Let t be a generator whose base is c ∈ΣC. The generation rule ρ(t) of t is the term expression ⟨e, c⟩, where e is the regex e(¯g1)∗(s1)e(¯g2)∗(s2)... e(¯gn)∗(sn) and si and gi are, respectively, the i-th elements of the word decomposition and the generator sequence of t.

We are finally ready to construct the desired RRA. Let t be a generator for K, the generator graph Gt of t is the sub-graph of unravelr=1(T, A) induced by t. Let now q be a CCQ with |ΣV(q)| = n. A generator RRT for q over K is an RRT ⟨¯a, {σ}⟩for which there exists a generator t for K and ¯c ∈q(I(unravelr=n(T, Gt))) such that σ = ⟨x, ρ(t)⟩ and ¯c is obtained from ¯a bt substituting x with t. Lemma 5. Let K be a satisfiable DL-LiteR KB and q(¯x) a CCQ. If a tuple ¯c is a far answer to q over K, then there is a generator RRT r for q over K such that ¯c ∈JrK.

Let now evalR be the function that maps every pair of CCQ q and satisfiable DL-LiteR KB K into the finite RRA consisting of all the near RRTs and all the (unique up to variable renaming) generator RRTs for q over K. Using Lemma 4 and 5, one can show the following.

Lemma 6. For every satisfiable DL-LiteR KB K and q ∈ UCQ, JevalR(q, K)K = q(I(unravel(q, K))

To prove the existence of a canonical RRA in the case of general CQs, we observe the following. Given a q ∈CQ, one can split it into its connected components, apply the construction above to obtain canonical RRAs for each of these components, and then return the Cartesian product of the results. To handle UCQs, one can simply return the union of the results of each of its disjuncts. These observations allow one to easily obtain Theorem 2.

## 5 Computational Aspects

We now study two computational problems related to the QAS defined in Section 4. The first problem is query answering, i.e., computing evalR(q, K), for a given satisfiable DL-LiteR KB K and q ∈UCQ. We are interested in the so called data complexity of the problem, i.e., the complexity that depends on the size of the input ABox alone. By inspecting the proof in Section 4, it is easy to observe that one can compute unravelr=n(K) in PTIME w.r.t. the size of A. This automatically yields a polynomial upper bound for the aforementioned problem. Interestingly, one can show that it is possible to obtain an even tighter upper bound by constructing a suitable FOL formula (independent from A) to be evaluated over A. The latter yields the following result.

Theorem 3. Let ⟨T, A⟩be a satisfiable DL-LiteR KB and let q ∈UCQ. Computing evalR(q, ⟨T, A⟩) can be done with logarithmic space overhead w.r.t. the size of A.

The results stated in Theorem 3 are in line with classical query answering using CAs and, thus, provide a strong motivation for using RRAs in practice.

The second problem we study is checking whether a formula φ ∈∃Pos(Σans) is satisfied by an RRA R. This problem refers to the possibility of using RRAs effectively as views over the original KB. Here we are interested in the complexity coming only from the input RRA, and the complexity of the whole problem.

Theorem 4. For a given RRA R and φ ∈∃Pos(Σans), checking whether R |=R φ is PSPACE-Complete, and can be done in PTIME w.r.t. the size of R.

It is still open whether the aforementioned problem is PTIME-complete w.r.t. the size of the RRA R.

## 6 Conclusions

In this paper, we presented a novel answer language for KBs (RRAs) and used it to define a query answering mechanism for UCQs over DL-LiteR KBs that is provably more informative than others in the literature. Additionally, we studied the complexity of related decision problems.

Future work includes using RRAs with different query and KB languages, possibly beyond the DL family. Moreover, one could study QAS that preserve languages more expressive than ∃Pos(Σans). Finally, we would like to use RRAs as the theoretical foundation of concrete software systems to visualize query answering results.

18934

<!-- Page 8 -->

## Acknowledgments

This work has been supported by MUR under the PNRR project FAIR (PE0000013). Additionally, the authors would like to thank the anonymous referees for their insightful comments.

## References

Abiteboul, S.; Hull, R.; and Vianu, V. 1995. Foundations of Databases. Addison Wesley Publishing Company.

Andolfi, L.; Cima, G.; Console, M.; and Lenzerini, M. 2024. What Does a Query Answer Tell You? Informativeness of Query Answers for Knowledge Bases. In Proceedings of the Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI 24), 10442–10449.

Beck, F.; Burch, M.; Diehl, S.; and Weiskopf, D. 2017. A taxonomy and survey of dynamic graph visualization. In Computer graphics forum, 1, 133–159. Wiley Online Library.

Bienvenu, M.; and Ortiz, M. 2015. Ontology-Mediated Query Answering with Data-Tractable Description Logics. In Reasoning Web. Semantic Technologies for Intelligent Data Access – Eleventh International Summer School Tutorial Lectures (RW 2015), volume 9203 of Lecture Notes in Computer Science, 218–307.

Borgida, A.; Toman, D.; and Weddell, G. E. 2016. On Referring Expressions in Query Answering over First Order Knowledge Bases. In Proceedings of the Fifteenth International Conference on the Principles of Knowledge Representation and Reasoning (KR 2016), 319–328.

Cal`ı, A.; Gottlob, G.; and Kifer, M. 2008. Taming the Infinite Chase: Query Answering under Expressive Relational Constraints. In Proceedings of the Eleventh International Conference on the Principles of Knowledge Representation and Reasoning (KR 2008), 70–80.

Calvanese, D.; De Giacomo, G.; Lembo, D.; Lenzerini, M.; and Rosati, R. 2007. Tractable Reasoning and Efficient Query Answering in Description Logics: The DL-Lite Family. Journal of Automated Reasoning, 39(3): 385–429.

Console, M.; Guagliardo, P.; Libkin, L.; and Toussaint, E. 2020. Coping with Incomplete Data: Recent Advances. In Proceedings of the 39th ACM SIGMOD-SIGACT-SIGAI Symposium on Principles of Database Systems, PODS, 33– 47. ACM.

Imielinski, T.; and Lipski, W., Jr. 1984. Incomplete Information in Relational Databases. Journal of the ACM, 31(4): 761–791.

Lenzerini, M. 2002. Data Integration: A Theoretical Perspective. In Proceedings of the Twenty-First ACM SIGACT SIGMOD SIGART Symposium on Principles of Database Systems (PODS 2002), 233–246.

Levesque, H. J.; and Lakemeyer, G. 2001. The Logic of Knowledge Bases. The MIT Press.

Libkin, L. 2016. Certain answers as objects and knowledge. Artificial Intelligence, 232: 1–19.

Lipski, W. 1979. On Semantic Issues Connected with Incomplete Information Databases. ACM Trans. Database Syst., 4(3): 262–296. Lutz, C.; and Przybylko, M. 2022. Efficiently Enumerating Answers to Ontology-Mediated Queries. In Proceedings of the Forty-First ACM SIGMOD-SIGACT-SIGAI Symposium on Principles of Database Systems (PODS 2022), 277–289. Lutz, C.; and Przybylko, M. 2023. Efficient Answer Enumeration in Description Logics with Functional Roles. In Proceedings of the Thirty-Seventh AAAI Conference on Artificial Intelligence (AAAI 2023), 6483–6490. Marnette, B. 2009. Generalized Schema-Mappings: from Termination to Tractability. In Proceedings of the Twentyeighth ACM SIGACT SIGMOD SIGART Symposium on Principles of Database Systems (PODS 2009), 13–22. Reiter, R. 1980. Data Bases: A Logical Perspective. In Proc. of the Workshop on Data Abstraction, Databases and Conceptual Modelling, 174–176. Toman, D.; and Weddell, G. E. 2019. Finding ALL Answers to OBDA Queries Using Referring Expressions. In Liu, J.; and Bailey, J., eds., AI 2019: Advances in Artificial Intelligence - 32nd Australasian Joint Conference, Adelaide, SA, Australia, December 2-5, 2019, Proceedings, volume 11919 of Lecture Notes in Computer Science, 117–129. Springer.

18935
