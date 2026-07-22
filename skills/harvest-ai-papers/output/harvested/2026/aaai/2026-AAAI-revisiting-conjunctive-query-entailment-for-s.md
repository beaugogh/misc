---
title: "Revisiting Conjunctive Query Entailment for S"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38989
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38989/42951
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Revisiting Conjunctive Query Entailment for S

<!-- Page 1 -->

Revisiting Conjunctive Query Entailment for S

Yazm´ın Ib´a˜nez-Garc´ıa1, Jean Christoph Jung2, Vincent Michielini3, Filip Murlak4

1Cardiff University 2TU Dortmund University 3University of Bordeaux 4University of Warsaw ibanezgarciay@cardiff.ac.uk, jean.jung@tu-dortmund.de, vincent.michielini@u-bordeaux.fr, f.murlak@uw.edu.pl

## Abstract

We clarify the complexity of answering unions of conjunctive queries over knowledge bases formulated in the description logic S, the extension of ALC with transitive roles. Contrary to what existing partial results suggested, we show that the problem is in fact 2EXPTIME-complete; hardness already holds in the presence of two transitive roles and for Boolean conjunctive queries. We complement this result by showing that the problem remains in CONEXPTIME when the input query is rooted or is restricted to use at most one transitive role (but may use arbitrarily many non-transitive roles).

## Introduction

In this paper, we aim to complete the complexity landscape for the problem of query answering over knowledge bases expressed in expressive description logics (DLs), that is, logics extending the basic DL ALC. As is common in such endeavor, we focus on the associated decision problem known as query entailment: given a DL knowledge base (KB) consisting of an ABox and a TBox, a query, and a tuple of individuals, the goal is to determine whether the query returns this tuple in every model of the given KB. As query languages we consider unions of conjunctive queries (UCQs) and fragments thereof. This problem has been heavily studied and is well understood. Existing results suggest a dichotomy:

• The problem is EXPTIME-complete for ALC and its extensions with role hierarchies (H) or qualified number restrictions (Q) (Lutz 2008; Ortiz, Simkus, and Eiter 2008). • The problem is 2EXPTIME-complete for the extension ALCself of ALC with the self-constructor (Bednarczyk and Rudolph 2023), and for every extension that allows either inverse roles (I) or both H and transitive roles (S), as long as it remains inside the DL SHIQ, which combines the extensions S, H, I, Q (Eiter et al. 2009; Glimm, Horrocks, and Sattler 2008).

Often, the restriction to rooted queries, that is, connected queries with answer variables, leads to lower complexity. This is the case for ALCself (Bednarczyk 2024) and all DLs between ALCI and SHIQ, where rooted query entailment is CONEXPTIME-complete as long as transitive role names

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

are disallowed in queries (Lutz 2008). Without inverses and self, the complexity is even lower: entailment of (rooted or not) queries without transitive roles is EXPTIME-complete for all DLs between ALC and SHQ (Lutz 2008). Working with rooted queries does not necessarily help if transitive roles are allowed in queries: analyzing the 2EXPTIME-hardness proof for query entailment in SH from (Eiter et al. 2009) shows that rooted query entailment remains 2EXPTIME-complete.

A notable gap remains for S without any extensions. For S the problem has been proven to be CONEXPTIME-complete when KBs and queries are allowed to use a single transitive role (and no other roles). The lower bound comes from (Eiter et al. 2009) and the upper one from (Bienvenu et al. 2010). A 2EXPTIME-upper bound for the general case follows from the mentioned result for SH (Eiter et al. 2009). In the same paper, Eiter et al. also claim an EXPTIME upper bound for the case where the ABox is tree-shaped. These results have been regarded as a strong indication that the whole problem may be CONEXPTIME-complete, challenging the apparent dichotomy (Bienvenu et al. 2010). The complexity for rooted query entailment was open until now, but a CONEXPTIMElower bound follows from (Eiter et al. 2009).

The aim of this paper is to revisit the query entailment problem for S and close the mentioned gaps. Our first main result is that, surprisingly, when at least two transitive roles are allowed in the query, the problem is 2EXPTIME-hard already for S (without role hierarchies), and hence 2EXP- TIME-complete. Importantly, our lower bound works with a tree-shaped ABox and thus contradicts the mentioned EXP- TIME upper bound for that case (Eiter et al. 2009). Indeed, in their argument, Eiter et al. compile input conjunctive queries (CQs) to so-called pseudo-tree queries (PTQs), designed to capture the behavior of CQs over tree-like interpretations, which is sufficient due to the tree-like model property of S. The error seems to arise from a subtle mismatch between the formal definition of PTQs used in the compilation process, and their intuitive understanding as trees of clusters, on which the later algorithmic treatment relies.

Besides the presence of two transitive roles in the query, our 2EXPTIME-hardness proof relies on the availability of non-rooted queries. We complement our lower bound by showing that both conditions are necessary: UCQ entailment remains in CONEXPTIME if at most one transitive role is allowed in the query or if the query is rooted.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19152

<!-- Page 2 -->

We develop the two proofs in parallel, using common terminology and data structures whenever possible. At the core, we show a small witness property in the following sense: the query is not entailed iff there is a small structure witnessing that. Note that this structure cannot be simply a countermodel since UCQ entailment for S is not finitely controllable (Rosati 2011). The NEXPTIME-algorithm for non-entailment can then just guess a small structure and verify that it is indeed a witness. Our argument is divided into three steps. Step 1. Reduce UCQ entailment to a special case with trivial

ABoxes and UCQs of special shape. Step 2. Reduce the special case of entailment to the exis- tence of structures called mosaics, which are collections of interpretations called tiles that respect certain compatibility requirements. Step 3. Show that both the size of all tiles in a mosaic and their number can be bounded exponentially. While the overall strategy is familiar, the steps are subtle. Steps 1–2 for the single transitive role case rely on a careful refinement of Eiter et al.’s PTQs, which ensures correctness of the algorithmic treatment, but makes the compilation process significantly harder. The crux of Step 3 is to show that UCQ entailment is finitely controllable as long as the set of used role names consists of a single transitive role name and queries are acyclic. Going beyond existing results (Bienvenu et al. 2010), we show that the size of the countermodel can be bounded independently from the query.

The structure of the paper is as follows. We give the necessary preliminaries in Section 2. Section 3 contains the proof of the 2EXPTIME-lower bound. Section 4 focuses on the case of a single transitive role and acyclic queries, needed for Step 3. In Section 5 we revise the notion of PTQs. In Section 6 we implement the three steps and obtain both upper bounds. We conclude in Section 7.

Proofs for all statements in the paper are available in the full version (Ib´a˜nez-Garc´ıa et al. 2025).

## Preliminaries

TBoxes, ABoxes, and Knowledge Bases. We fix countably infinite sets NI of individual names, NC of concept names, and NR of role names, partitioned into non-transitive role names Nnt

R and transitive role names Nt

R. Concepts C of the description logic S are defined by the grammar:

C::= A | ¬C | C1 ⊔C2 | ∃r. C.

A concept inclusion (CI) is an expression of the form C ⊑D for concepts C, D. A TBox is a finite set of concept inclusions. An ABox is a finite set of concept assertions A(a) and role assertions r(a, b) for A ∈NC, r ∈NR, and a, b ∈NI. A knowledge base (KB) is a pair K = ⟨T, A⟩consisting of a TBox T and an ABox A. We write NC(T), NI(A), etc. for the finite sets of concept names, individual names, etc. that occur in a particular TBox T or ABox A.

Interpretations. The semantics of concepts, TBoxes, and ABoxes are defined as usual based on interpretations. An interpretation is a pair I = ⟨∆I, ·I⟩where ∆I is the domain of I; and ·I assigns a subset AI ⊆∆I of the domain to every concept name A ∈NC, a binary relation rI ⊆∆I × ∆I to every role name r ∈NR, and an element aI ∈∆I to every individual name a ∈NI (Baader et al. 2017). The interpretation of complex concepts is standard:

(¬C)I = ∆I \ CI, (C ⊔D)I = CI ∪DI,

(∃r. C)I = {d ∈∆I | ⟨d, e⟩∈rI for some e ∈CI}.

An interpretation I is a model of a TBox T, written I |= T, if tI is a transitive relation for all t ∈Nt

R, and CI ⊆DI for every concept inclusion C ⊑D in T. For ABoxes, we adopt the standard name assumption; that is, we assume aI = a for all a ∈NI(A). Then, I is a model of ABox A, written I ⊨A, if a ∈AI for every assertion A(a) ∈A and ⟨a, b⟩∈rI for every assertion r(a, b) ∈A. Finally, I is a model of a KB K = ⟨T, A⟩if I |= T and I |= A.

For a domain element d ∈∆I, the type of d in I is defined as tp(I, d) = {A ∈NC | d ∈AI}.

The transitive closure of an interpretation I is the interpretation I+ that coincides with I except that, for every t ∈Nt

R, tI+ is the transitive closure of tI.

A tree is a directed acyclic graph in which exactly one node (the root) has no incoming edges, and each other node has exactly one incoming edge (originating in the parent of the node). With an interpretation I we associate a directed multigraph GI in which nodes are the domain elements and edges are obtained by taking the disjoint union of the interpretations of all role names. We call I tree-shaped if GI is a tree (in particular, it has no parallel edges). We call I a transitive-tree interpretation if it is the transitive closure of a tree-shaped interpretation I0. The root of I is the root of I0.

Conjunctive Queries. Let NV be a countably infinite set of variables. A conjunctive query (CQ) is an expression of the form q(¯x) where q is a finite set of atoms of the form A(x) or r(x, y) where x, y ∈NV, A ∈NC, and r ∈NR, and ¯x is a tuple of variables occurring in the atoms of q. We call ¯x the answer variables of q(¯x). We write var(q) for the set of all variables occurring in q. A union of conjunctive queries (UCQ) Q(¯x) is a finite set of CQs with the same answer variables ¯x, which we call the answer variables of Q. A (U)CQ is Boolean if its tuple of answer variables is empty, and unary if it is a singleton. We identify a Boolean CQ q with its set of atoms.

A match of a CQ q(¯x) in an interpretation I is a function δ: var(q) →∆I such that δ(x) ∈AI for each A(x) ∈q, and ⟨δ(x), δ(y)⟩∈rI for each r(x, y) ∈q. For a tuple ¯d of domain elements from ∆I, we write ⟨I, ¯d⟩|= q(¯x) if there is a match δ of q in I with δ(¯x) = ¯d. For UCQs, we write ⟨I, ¯d⟩|= Q(¯x) if ⟨I, ¯d⟩|= q(¯x) for some q(¯x) ∈Q(¯x). In the Boolean case, we write I |= q if there is a match of q in I, and I |= Q if I |= q for some q ∈Q.

To any CQ q one can associate a directed multigraph Gq, where nodes represent variables and edges are formed by binary atoms. If atoms share the same pair of variables, this creates parallel edges in Gq. A query q(¯x) is called acyclic or connected if Gq is acyclic or connected, respectively. A query is said to be rooted if it is connected and not Boolean. These definitions extend to UCQs: a UCQ Q is acyclic, connected,

19153

<!-- Page 3 -->

or rooted if each CQ in Q is. We call tree query (TQ) any unary CQ q(x) such that Gq is a directed tree (in particular, it has no parallel edges), x being its root. A union of tree queries (UTQ) is a UCQ that contains only TQs.

For a CQ q(¯x), a variable z ∈var(q) is initial in q if z has no incoming edges in Gq. For instance, if q(x) is a TQ, then x is initial in q(x).

Query Entailment. Let K = ⟨T, A⟩be a KB, Q(¯x) be a UCQ and ¯a be a tuple of individuals from NI(A). We say that K entails Q(¯a), written K |= Q(¯a), if ⟨I, ¯a⟩⊨Q for every model I of K. We study the reasoning problems of UCQ entailment and rooted UCQ entailment. UCQ entailment asks, given a KB K and a Boolean UCQ Q, whether K |= Q; and rooted UCQ entailment asks, given a KB K, a rooted UCQ Q(¯x), and a tuple ¯a from NI(A), whether K |= Q(¯a). We also consider the variant over a single transitive role t which means that the only role that occurs in T and Q is t. More general query answering problems, for example, for UCQs with constants, can be reduced to the above using standard methods (Glimm et al. 2008).

Throughout the paper, we assume that TBoxes T be in normal form which means that each concept inclusion in T has one of the following shapes:

d i Ai ⊑F j Bj, A ⊑∃r.B, A ⊑∀r.B, where A, Ai ∈NC ∪{⊤}, B ∈NC, Bj ∈NC ∪{⊥}; ⊥, ⊤, ⊓, and ∀are part of the syntax, with standard semantics. It is routine to show that this is without loss of generality for the considered entailment problems.

When stating complexity bounds, we write ∥T ∥and ∥Q∥ for the size of T and Q, respectively, represented as a word over a suitable alphabet.

Two Transitive Roles In this section, we show that UCQ entailment in S is 2EXP- TIME complete when the query involves at least two transitive roles. The 2EXPTIME-upper bound follows from several previous works, e.g., (Glimm et al. 2008; Calvanese, Eiter, and Ortiz 2014; Guti´errez-Basulto et al. 2023; Gottlob, Pieris, and Tendera 2013). We focus on the hardness of the problem.

Theorem 1. UCQ Entailment in S is 2EXPTIME-complete. It is 2EXPTIME-hard already for CQs and ABoxes of the form {A(a)}, if at least two transitive roles are available.

Our proof closely follows the 2EXPTIME-hardness proof for CQ entailment in SH provided in (Eiter et al. 2009). Since a simple reduction from this problem seems impossible, we give a direct argument. Here we sketch 2EXPTIME-hardness for unions of CQs, which is significantly easier than for CQs.

We reduce from the word problem for exponential-space alternating Turing machines. We encode runs of such machines as interpretations of the form shown in Figure 1, where edges labeled by α represent paths of length 2, consisting of a t1-edge followed by a t2-edge for t1, t2 ∈Nt

R. Each gray triangle represents a configuration: existential ones have one successor, and universal two. Each of these triangles is a full binary tree of height n, built from α-edges, whose 2n leaves correspond to tape cells. A tape cell is encoded using the blue

R

...

...

α α α α α α α α α α α α α config. tree u v w t1 t2 t1 t1 t2

...

**Figure 1.** Encoding runs of alternating Turing machines.

x1

B1 y1

B1 z1

Yσ y Zτ z αn+1 αn+3 xn

Bn yn Bn zn

...

αn+1 αn+3 x x′ t1 t1 t2 t2 t1

**Figure 2.** Detecting copying errors.

gadget on the left. The content of the cell is stored in node w: the current using concept names Yσ and the previous one with Zσ where σ ranges over possible cell contents. Nodes u and v encode the number of the cell in binary using concept names B1,..., Bn. Each Bi is present in exactly one of the nodes u and v: in u if the ith bit is 0, and in v if it is 1.

With a bit of effort one can define a TBox (using additional concept names to propagate information) that ensures that the interpretation correctly encodes a run of the machine, provided that previous tape content (along with the state annotation) is correctly copied from the previous configuration. The latter is ensured by the query, which is the union of CQs qσ,τ for σ, τ ranging over pairs of different cell contents. Each qσ,τ detects a copying error where σ was replaced by τ. It is shown in Figure 2, with the dashed edges representing the path on the right, directed from x to x′.

Variables y and z can only match in consecutive configurations, in the w nodes of some cell gadgets, say wσ and wτ. Then, yi can match only in uσ or vσ, and zi only in uτ or vτ. Moreover, owing to the rigidity of the paths αn+1 and αn+3, yi matches in uσ iff zi matches in uτ. Hence, y and z can only match in the same cell of two consecutive configurations. They do if and only if this cell was copied incorrectly.

## 4 Acyclic Queries, Single Transitive Role

We now focus on the special case of acyclic queries over a single transitive role, which is the crux of the problem. We prove an exponential countermodel property. Theorem 2. Consider an acyclic Boolean UCQ Q and a TBox T, both of which use a single role name t, which is transitive. Then, for every transitive-tree interpretation I over t with root d0 such that both I |= T and I̸ |= Q, there exists an interpretation J satisfying the following:

19154

<!-- Page 4 -->

• ∆J ⊆∆I and tp(J, d) = tp(I, d) for each d ∈∆J; • J is finite and |∆J | ≤(|NC(T)| + 1)!; • d0 ∈∆J, J |= T, and J̸ |= Q.

Unexpectedly, yet crucially, the bound does not depend on the query at all, unlike in (Bienvenu et al. 2010). Moreover, it depends only on the number of concept names mentioned in T, rather than all concept names occurring in I.

The rest of the section is devoted to the proof of Theorem 2. Let us fix Q, T, I, and d0 as in the statement. While I may well be infinite, the extracted interpretation J will be finite, but not necessarily a transitive-tree interpretation. For d ∈∆I, define tI(d) = e ∈∆I ⟨d, e⟩∈tI and let Id be the subinterpretation of I induced by {d} ∪tI(d).

Let m = |Q|. We define a function ¯q that assigns to each d ∈∆I an m-tuple ¯qd = ⟨qd,1,..., qd,m⟩of acyclic Boolean CQs that are forbidden in Id, in the sense that

Id̸ |= {qd,i | 1 ≤i ≤m} for each d ∈∆I. (1)

The function ¯q is defined by induction. First, we set ¯qd0 as any m-tuple listing all CQs from Q. We then proceed topdown, maintaining the invariant. Suppose that ¯qd is already defined for some d ∈∆I; we shall define ¯qe for all direct t-successors e of d in I: elements e ∈tI(d) such that there is no f ∈tI(d) with e ∈tI(f). For each i ≤m, let Xd,i ⊆ var(qd,i) be the set of initial variables of qd,i that can be matched in d; that is, it contains an initial variable x of qd,i iff d ∈AI for each atom A(x) in qd,i. Consider the query q′ obtained from qd,i by dropping all atoms involving a variable from Xd,i, and let us look at its connected components. If each connected component of q′ admitted a match in a (strict) subtree of Id then by merging these matches and mapping each variable from Xd,i to d, we would get a match of qd,i in Id, contradicting the assumption. Hence, there must be a connected component q′ d,i of q′ that does not admit such a match. (Notice that q′ d,i = qd,i iff Xd,i = ∅.) We let qe,i = q′ d,i for each direct t-successor e of d in I. Crucially, ¯q is anti-monotone: ¯qe ⪯¯qd for each ⟨d, e⟩∈tI, where ¯qe ⪯¯qd iff qe,i is a subquery of qd,i for each i.

For our construction of J, we also formalize the notion of ‘visible concepts’ of an element in the tree. For each d ∈∆I, we define VCI t (d) as the set

{A ∈NC(T) | e ∈AI for some e ∈tI(d)}.

Because of the transitivity of tI, the function VCI t is also anti-monotone: VCI t (e) ⊆VCI t (d) for every ⟨d, e⟩∈tI. Now that we defined the functions ¯q and VCI t, we can finally use them to construct, for each d ∈∆I, a finite interpretation Jd with the following properties:

• d ∈∆Jd ⊆∆I, • tp(Jd, e) = tp(I, e) for all e ∈∆Jd,

• VCI t (e) = VC

J + d t (e) for all e ∈∆Jd,

• J + d̸ |= {qd,i | i ≤m}, and

• |∆Jd| ≤(|VCI t (d)| + 1)!.

d

Jf1 Jf2 · · · Jfℓ t t t d e1 e2

...

ek t t t t t

Jd1 Jd2 · · · Jdℓ t t t

**Figure 3.** Interpretation Jd in the two cases.

The second and third condition together immediately give J + d |= T, because T is in normal form and only uses the role name t. The fourth states that J + d satisfies the same invariant (1) as Id. In consequence, defining J as J + d0 will complete the proof of Theorem 2.

We construct Jd for d ∈∆I by induction over the set M = VCI t (d) ⊆NC(T). There are two cases, depending on the set αM = e ∈∆Id | VCI t (e) = M

. The first case is conceptually simpler and serves also as the induction base.

1. There exists e ∈αM such that αM ∩tI(e) = ∅. Hence, VCI t (e) = M but VCI t (f) ⊊M for all f ∈tI(b). Then, we can select elements f1,..., fℓ∈tI(e), ℓ≤|M|, such that for each A ∈M, there exists j with fj ∈AI. We build Ja by taking the disjoint union of interpretations Jfj, that exist by the induction hypothesis, and adding element d with unary type inherited from I along with t-edges from d to fj for all j, as shown in Figure 3 (left). Note that in the induction base, where M = ∅, Jd has domain {d} and no edges.

2. For all e ∈αM, αM ∩tI(e)̸ = ∅. Then, because ⪯is a well-founded partial order, there is some e0 ∈αM and a ⪯minimal m-tuple ¯q such that ¯qe = ¯q for all e ∈tI(e0) ∩αM. Since e0 ∈αM, we can, as in the first case, select elements f1,..., fm ∈tI(b0), m ≤|M|, such that for each A ∈M, there is some j with fj ∈AI. We partition f1,..., fm in two sequences, depending on VCI t:

• d1..., dℓcontains all those fi with VCI t (fi) ⊊M, and

• e1,..., ek contains all those fi with VCI t (fi) = M.

To build Ja, we first arrange a, e1, e2,..., ek (with unary types inherited from I) into a simple path with t-edges. Next, we turn it into a cycle by adding a t-edge from ek to e1. Finally, we add the disjoint union of interpretations Jd1,..., Jdℓ, along with a t-edge from ek to dj for all j ≤ℓ. See Figure 3 (right) for an illustration of the constructed Jd.

Verifying that Jd has the desired properties is easy, except for J + d̸ |= {qd,i | i ≤m} which subtly relies on the choice of e0 and the anti-monotonicity of ⪯.

19155

<!-- Page 5 -->

Pseudo-Tree Queries Differently To prepare for multi-role queries, we revise the notion of pseudo-tree queries (PTQs). The key property missing in (Eiter et al. 2009) is global undirected acyclicity, which we build into our definition. Intuitively, we define a PTQ as a connected CQ whose set of binary atoms can be partitioned into disjoint connected acyclic sets of atoms over the same role name, called clusters, that are arranged into a tree. The latter condition ensures global undirected acyclicity. Let us make this precise. Definition 3. Let q(¯x) be a CQ. For a non-transitive role name r, an r-cluster of q(¯x) is a nonempty maximal subset Cr of q of the form {r(x, y1), r(x, y2),..., r(x, yk)} with k > 0. For a transitive role name t, a t-cluster of q(¯x) is a nonempty maximal connected set Ct of t-atoms of q(¯x).

The clusters of a CQ constitute a partition of the set of its binary atoms. We treat clusters as (Boolean) conjunctive queries. In particular, we speak of initial variables in clusters. For instance, Figure 4 (left) shows an example of a query with one t-cluster and three s-clusters; cluster C4 has two initial variables, x and u; variables y and z are not initial in C4, but they are initial in C2 and C3, respectively. Definition 4. A cluster tree for a CQ q(¯x) is a tree having for its set of nodes the set of clusters of q(¯x), and such that:

(a) two clusters can only share variables if they are siblings or if one is a child of the other; (b) two siblings can only share a variable if they also share it with their parent; (c) each non-root cluster C shares with its parent exactly one variable, called the entry variable of C, and this variable must be initial in C (the root cluster has no entry variable).

**Figure 4.** (middle) shows a cluster tree for the query on the left. Intuitively, a cluster tree reflects which clusters must be matched below each other, when the query is matched in a transitive-tree interpretation. However, this intuition breaks down as soon as the entry variable of a child cluster is initial in the parent cluster (as for C1 and C4 in Figure 4): then, the child cluster need not be matched below the parent cluster.

For similar reasons, cluster trees are not unique: the root of a cluster tree may be swapped for any of its children whose entry variable is initial in the current root. In Figure 4, an alternative cluster tree is obtained by making C4 a child of C1. Once we fix the root, the cluster tree is unique: all clusters sharing a variable with the root become its children, etc. By a root cluster in q(¯x) we mean any cluster that is the root of some cluster tree for q(¯x). In Figure 4, C1 and C4 are root clusters, while C2 and C3 are not. Definition 5. A Boolean pseudo-tree query (Boolean PTQ) is a connected Boolean CQ q such that 1. there is a cluster tree for q; 2. for each transitive t, every t-cluster of q is acyclic. A unary pseudo-tree query (unary PTQ) is a unary CQ q(x)

such that q is a Boolean PTQ, and x is initial and belongs to a single, root cluster in q. A Boolean/unary UPTQ is a UCQ that contains only Boolean/unary PTQs.

x u y z

C1

C2

C3

C4 s t t t t s s

C4

C1 C2 C3

Ap1(x)

Ap2(y)

Ap3(z)

t t t t

**Figure 4.** A Boolean PTQ over a transitive role t and nontransitive role s, its cluster tree, and a query corresponding to its root cluster.

B

A

C D s s t t t t s s

B D A C s s t t

A

B D C s t s s t

**Figure 5.** A naughty query using transitive roles s, t.

Coming back to the example in Figure 4, the query q shown on the left is a Boolean PTQ and q(u) is a unary PTQ, whereas q(x), q(y), and q(z) are not. Moreover, any TQ whose answer variable occurs in at most one binary atom (as in Theorem 8 below) is a unary PTQ. On the other hand, the query in Figure 5 (left) does not admit a cluster tree. Yet, it was classified as a PTQ in (Eiter et al. 2009).

The raison d’ˆetre of PTQs is to semantically capture CQs over transitive-tree interpretations, as stated in Lemma 6 below. Crucially, this is possible only if at most one transitive role is allowed.

Lemma 6. Let T be the class of transitive-tree interpretations. The following can be done in polynomial time for CQs using at most one transitive role:

• Given a connected Boolean CQ q, decide if I |= q for some I ∈T, and if so, output a Boolean PTQ ˆq such that I |= q iff I |= ˆq for all I ∈T. • Given a connected unary CQ q(x), decide if ⟨I, d⟩|= q(x) for some I ∈T with root d, and if so, output unary PTQs

ˆq1(x),..., ˆqk(x) such that for all I ∈T with root d, ⟨I, d⟩|= q(x) iff ⟨I, d⟩|= ˆqi(x) for all i.

The existence of ˆq and ˆq1(x),..., ˆqk(x) in Lemma 6 relies on the input query using at most one transitive role. For instance, the query q in Figure 5 (left) admits a match in a transitive-tree interpretation, but one can check that it is not captured by a single PTQ. Intuitively, this is because q is entailed by both queries in Figure 5 (right), despite their radically different structure. In the unary case, we need multiple (but polynomially many) PTQs, because the answer variable cannot belong to multiple clusters. For instance, for q in Figure 4, q(x) requires two unary PTQs: one consists of cluster C1 and the other consists of clusters C2, C3, and C4.

We close the section by defining subPTQs, which are to PTQs what subtrees are to TQs. A subPTQ of a Boolean PTQ q is a unary subquery of q induced by a proper subtree

19156

<!-- Page 6 -->

of a cluster tree for q. It consists of all binary atoms in the subtree along with all unary atoms of q over variables used in the subtree, and its answer variable is the entry variable of the root of the subtree. A subPTQ of a unary PTQ q(x) is defined analogously, except that we are limited to the (unique) cluster tree of q(x) such that x belongs to the root cluster. For instance, the query q in Figure 4 has 4 subPTQs. Three are induced by the subtrees of the cluster tree in the figure, rooted at C1, C2, and C3, and their answer variables are x, y, and z, respectively. The last one is induced by the subtree rooted at C4 of the alternative cluster tree whose root is C1, and its answer variable is x. Of those 4 queries, only the first 3 are subPTQs of the unary PTQ q(u).

Upper Bounds Our proof of 2EXPTIME-hardness of CQ entailment in S crucially relies on the availability of (a) two transitive roles and (b) Boolean CQs. We now show that entailment becomes easier if we forbid either of these. In this sense our hardness result is optimal. Theorem 7. The query entailment problem in S is

CONEXPTIME-complete for rooted UCQs and for UCQs that use at most one transitive role name.

The CONEXPTIME-hardness for UCQs using at most one transitive role was established by (Eiter et al. 2009). While the proof is formulated using Boolean CQs, it does not rely on this and can be adjusted easily to the case of rooted CQs.

We focus on the upper bounds. The proofs have a common three-step structure described in the introduction and ultimately establish a small witness property based on Theorem 2. We implement Steps 1–3 for both upper bounds in parallel in Sections 6.1–6.3 and we put them together in Section 6.4, where the proof of Theorem 7 is finalized.

## 6.1 Eliminating ABoxes and Simplifying Queries

The first step eliminates the ABox and simplifies the queries. For the rooted case, this is routine. We reduce our main entailment problem to a variant where the input consists of a TBox T, a set τ ⊆NC(T), and a unary UCQ Q1: the task is to decide whether for each model I of T and every d ∈∆I with tp(I, d) ∩NC(T) = τ, we have ⟨I, a⟩|= Q1. We write this condition as ⟨T, τ⟩|= Q1. The reduction is provided by the following theorem. Note that this is a non-deterministic reduction, similar to the one introduced in (Adleman and Manders 1977). Theorem 8. There is a NEXPTIME algorithm that, given a KB ⟨T, A⟩, a rooted UCQ Q(¯x), and a tuple ¯a of individuals from NI(A), computes for each a ∈NI(A) a set τa ⊆NC(T) and a UTQ Q1 a such that • ⟨T, A⟩̸ |= Q(¯a) iff there is a run of the algorithm such that ⟨T, τa⟩̸ |= Q1 a for all a ∈NI(A); • for each run of the algorithm and each a ∈NI(A), the size of each TQ in Q1 a is linear in ∥Q∥and its answer variable occurs in at most one binary atom. Next, we handle the single transitive role case. We obtain stronger size guarantees (needed later) at the cost of relaxing tree queries (TQs) to pseudo-tree queries (PTQs). Similarly to the rooted case, we reduce entailment of UCQs using a single transitive role to a variant of entailment for UPTQs. This time, given a TBox T, a set τ ⊆NC(T), a Boolean UPTQ Q0, and a unary UPTQ Q1, one has to decide whether for each model I of T and each d ∈∆I with tp(I, d) ∩NC(T) = τ, we have I |= Q0 or ⟨I, d⟩|= Q1. We write the condition to be decided as ⟨T, τ⟩|= Q0 ∨Q1. The following theorem provides the reduction; it relies on Lemma 6 to transform CQs into PTQs equivalent over transitive-tree interpretations. Theorem 9. There is a NEXPTIME algorithm that, given a KB ⟨T, A⟩and a Boolean UCQ Q using at most one transitive role, computes for each a ∈NI(A) a set τa ⊆NC(T), a Boolean UPTQ Q0 a, and a unary UPTQ Q1 a such that • ⟨T, A⟩̸ |= Q iff there is a run of the algorithm such that ⟨T, τa⟩̸ |= Q0 a ∨Q1 a for all a ∈NI(A); • for each run of the algorithm and each a ∈NI(A), ∥Q0 a∥ is linear in ∥Q∥, each PTQ in Q1 a is linear in ∥Q∥, and the total number of subPTQs of PTQs from Q1 a is polynomial in ∥Q∥. Compared to Theorem 8, Theorem 9 yields queries from a broader class (UPTQs, rather than UTQs), but offers stronger size guarantees: the total number of subPTQs of PTQs in Q1 a is polynomial. This is a substitute for a polynomial bound on ∥Q1 a∥, which cannot be ensured. Importantly, the variant of entailment used in Theorem 8 is a special case of the one in Theorem 9: Q0 a = ∅and UTQs with answer variables used in at most one binary atom instead of UPTQs. This enables us to treat the two cases in parallel in what follows.

## 6.2 From Entailment to Existence of Mosaics Our goal now is to reduce the variant of UPTQ entailment introduced in

Section 6.1 to the special case where only one role is used in the input. Our reduction relies on tiles, which are interpretations using only one role name, consistent with the TBox. We show that countermodels can be represented using mosaics, which are collections of such tiles.

Below, Tr is the restriction of T to CIs that do not mention any role names other than r, and ⟨I, d0⟩⊨Tr means that d0 ∈CI implies d0 ∈DI for each CI C ⊑D from Tr. Definition 10. A tile for a TBox T is a triple ⟨I, d0, r⟩where I is an interpretation, d0 ∈∆I, and r ∈NR, such that sI = ∅for all s ∈NR −{r} and 1. if r is transitive, then I ⊨Tr (and, in particular, I+ = I); 2. if r is non-transitive, then ⟨I, d0⟩⊨Tr. Tiles are meant to be assembled to form a countermodel to ⟨T, τ⟩⊨Q0 ∨Q1. To facilitate this, we introduce a family of fresh auxiliary concept names of the form Ap(x), where p(x) is a subPTQ of a PTQ from Q0 or from Q1. Intuitively, Ap(x) will be used to propagate the constraint that p(x) must not be matched. To prevent the entire CQ from being satisfied, we recursively partition it into clusters (as described in the next paragraph) and ensure that each tile violates suitable clusters, augmented with atoms of the form Ap(x)(x). Crucially, if Q0 and Q1 are Q0 a and Q1 a from Theorem 9 for some Q, then the number of auxiliary concept names is polynomial in ∥Q∥.

Let q be Boolean PTQ from Q0 or the Boolean PTQ underlying a subPTQ q(x) of a PTQ from Q0 or from Q1. Consider

19157

<!-- Page 7 -->

a root cluster C of q, and the corresponding cluster tree for q with C in the root. We define qC as the Boolean PTQ obtained by replacing each direct subtree of the cluster tree with a single unary atom using a suitable auxiliary concept name. (Recall that a direct subtree is one rooted at a child of the whole tree’s root.) More precisely, qC contains all binary atoms from C along with all unary atoms of q over variables used in C, and for each child C′ of C, sharing a variable x with C, qC contains the atom Ap(x)(x) where p(x) is the subPTQ corresponding to the cluster subtree rooted at C′.

For instance, if q is the query in Figure 4 (left), then qC4(x) is the query shown on the right. Concept names Ap1(x), Ap2(y), and Ap3(z) used in qC4(x) replace the subPTQs of q induced by C1, C2, and C3, respectively.

We now define a mosaic as a compatible collection of tiles that correctly propagates information about subPTQs. Definition 11. Consider a TBox T, a type τ, a Boolean UPTQ Q0, and a unary UPTQ Q1. A mosaic for T and τ, and against Q0 and Q1, is a set M of tiles for T such that: 1. for each ⟨I, d0, r⟩∈M, q ∈Q0, and root r-cluster C of q, we have I ⊭qC; 2. for each ⟨I, d0, r⟩∈M, d ∈∆I, auxiliary Ap(x), and root r-cluster C of p that contains x, if d /∈AI p(x) then ⟨I, d⟩⊭pC(x); 3. there is a family of tiles ⟨Ir, dr, r⟩∈M with tp(Ir, dr) ∩NC(T) = τ, for r ranging over NR(T), such that for each q(x) ∈Q1, ⟨Ir, dr⟩⊭qC(x) for some r ∈NR(T) and root r-cluster C of q that contains x; 4. for each ⟨I, d0, r⟩∈M, d ∈∆I, and s ∈NR(T) such that either s̸ = r or both r is non-transitive and d̸ = d0, there is ⟨J, e0, s⟩∈M such that tp(I, d) = tp(J, e0). As promised, our variant of the entailment problem for UPTQs reduces to the existence of mosaics. Theorem 12. For any TBox T, τ ⊆NC(T), Boolean UPTQ Q0, and unary UPTQ Q1, ⟨T, τ⟩⊭Q0 ∨Q1 iff there is a mosaic M for T and τ, and against Q0 and Q1.

The proof of Theorem 12 is technical yet relatively standard. It remains to see that the existence of suitable mosaics can be decided in NEXPTIME. Towards this end, we prove in the following subsection that tiles and mosaics of singly exponential size are sufficient.

## 6.3 Bounding the Sizes of Tiles and Mosaics We know from

Theorem 12 that the entailment problem reduces to the existence of a mosaic. Now, using Theorem 2 in Section 4, we can show that we can assume each tile of the mosaic to be of exponential size. Lemma 13. Consider a TBox T, τ ⊆NC(T), a Boolean UPTQ Q0, and a unary UPTQ Q1. For every mosaic M for T and τ, and against Q0 and Q1, there is a mosaic M′ for T and τ against Q0 and Q1 such that |∆I| ≤(|NC(T)| + 1)! for each tile ⟨I, a0, r⟩∈M′.

It remains to see that the number of tiles in a mosaic can be bounded as well. Here, the arguments diverge.

In the single transitive role case, we rely on the number of auxiliary concept names, determined by the number of subPTQs of PTQs from Q0 and Q1, being polynomial. As one tile per type is enough, we get the following.

Lemma 14. If there is a mosaic for T and τ, and against a Boolean UPTQ Q0 and a unary UPTQ Q1, with tiles of size at most M, then there is one with at most n + n · 2n+m tiles, all of size at most M, where n = ∥T ∥and m is the total number of subPTQs of PTQs from Q0 and Q1.

In the rooted case, the number of auxiliary concepts is exponential, but we observe that in a countermodel built from tiles, a rooted query can traverse only a linear number of tiles from the initial element. Because a tile of size M requires at most M · ∥T ∥witnesses, a singly exponential number of tiles is sufficient to build the part of the countermodel within linear distance from the initial element. Further away, we do not care about matching the query anymore, so we only need one tile for each τ ⊆NC(T).

Lemma 15. If there is a mosaic for T and τ against Q0 = ∅ and unary UTQ Q1 with tiles of size at most M, then there is one with at most n · ((Mn)m+1 + 2n) tiles, all of size at most M, where n = ∥T ∥and m is the maximal number of variables of a TQ in Q1.

## 6.4 Wrapping Up

Combining Theorems 8 and 9 (Step 1), Theorem 12 (Step 2), and Lemmas 13–15 (Step 3), we obtain the following.

Corollary 16. There is a NEXPTIME algorithm that, given a KB ⟨T, A⟩and rooted UCQ Q or a Boolean UCQ Q using at most one transitive role, computes for each a ∈NI(A) a set τa ⊆NC(T), a Boolean PTQ Q0 a and a unary UPTQ Q1 a, both containing PTQs of linear size only, such that ⟨T, A⟩̸ |= Q iff there is a run of the algorithm such that for all a ∈ NI(A) there is a mosaic Ma for T and τa against Q0 a and Q1 a, of size bounded exponentially in ∥T ∥+ ∥Q∥using tiles of size bounded exponentially in ∥T ∥.

Theorem 7 now follows easily, because after computing Q0 a and Q1 a for each a ∈NI(A), the algorithm from Corollary 16 can guess a suitable mosaic Ma for each a. Verifying that Ma is indeed a mosaic for T and τa against Q0 a and Q1 a can be done in time exponential in ∥T ∥+ ∥Q∥.

Conclusions

Contrary to previous expectations, UCQ entailment in S turns out to be 2EXPTIME-complete, even when restricted to trivial ABoxes and CQs with two transitive roles. On the positive side, both entailment of rooted UCQs and entailment of UCQs using at most one transitive role are CONEXPTIMEcomplete and thus easier. We note a curious dependence of the complexity of the problem on the number of transitive roles allowed in queries: EXPTIME for 0, CONEXPTIME for 1, and 2EXPTIME for at least 2. Our results partly apply to UCQ entailment over finite interpretations. Indeed, it is easy to check that our 2EXP- TIME-hardness proof also works in the finite case. A matching upper bound follows from (Gogacz, Ib´a˜nez-Garc´ıa, and Murlak 2018). On the other hand, it is an open question if our CONEXPTIME upper bounds hold in the finite case, too.

19158

<!-- Page 8 -->

## Acknowledgments

Vincent Michielini was supported by the ERC grant INF- SYS, agreement no. 950398, held by Wojciech Czerwi´nski at the University of Warsaw. Filip Murlak was supported by Poland’s NCN grant 2018/30/E/ST6/00042.

## References

Adleman, L.; and Manders, K. 1977. Reducibility, randomness, and intractibility (Abstract). In Proceedings of the Ninth Annual ACM Symposium on Theory of Computing, STOC ’77, 151–163. New York, NY, USA: Association for Computing Machinery. ISBN 9781450374095. Baader, F.; Horrocks, I.; Lutz, C.; and Sattler, U. 2017. An Introduction to Description Logic. Cambridge University Press. ISBN 978-0-521-69542-8. Bednarczyk, B. 2024. Data Complexity in Expressive Description Logics with Path Expressions. In Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI 2024, 3241–3249. ijcai.org. Bednarczyk, B.; and Rudolph, S. 2023. How to Tell Easy from Hard: Complexities of Conjunctive Query Entailment in Extensions of ALC. J. Artif. Intell. Res., 78. Bienvenu, M.; Eiter, T.; Lutz, C.; Ortiz, M.; and Simkus, M. 2010. Query Answering in the Description Logic S. In Proceedings of the 23rd International Workshop on Description Logics (DL 2010), volume 573 of CEUR Workshop Proceedings. CEUR-WS.org. Calvanese, D.; Eiter, T.; and Ortiz, M. 2014. Answering regular path queries in expressive Description Logics via alternating tree-automata. Inf. Comput., 237: 12–55. Eiter, T.; Lutz, C.; Ortiz, M.; and Simkus, M. 2009. Query Answering in Description Logics with Transitive Roles. In Proceedings of the 21st International Joint Conference on Artificial Intelligence, IJCAI 2009, 759–764.

Glimm, B.; Horrocks, I.; and Sattler, U. 2008. Unions of Conjunctive Queries in SHOQ. In Proceedings of the 11th International Conference on Principles of Knowledge Representation and Reasoning (KR), 252–262. AAAI Press.

Glimm, B.; Lutz, C.; Horrocks, I.; and Sattler, U. 2008. Conjunctive Query Answering for the Description Logic SHIQ. J. Artif. Intell. Res., 31: 157–204. Gogacz, T.; Ib´a˜nez-Garc´ıa, Y. A.; and Murlak, F. 2018. Finite Query Answering in Expressive Description Logics with Transitive Roles. In Proceedings of the Sixteenth International Conference on Principles of Knowledge Representation and Reasoning KR 2018, 369–378. AAAI Press. Gottlob, G.; Pieris, A.; and Tendera, L. 2013. Querying the Guarded Fragment with Transitivity. In Proceedings of the 40th International Colloquium on Automata, Languages, and Programming (ICALP), volume 7966 of Lecture Notes in Computer Science, 287–298. Springer. Guti´errez-Basulto, V.; Ib´a˜nez-Garc´ıa, Y.; Jung, J. C.; and Murlak, F. 2023. Answering regular path queries mediated by unrestricted SQ ontologies. Artif. Intell., 314: 103808.

Ib´a˜nez-Garc´ıa, Y. A.; Jung, J. C.; Michielini, V.; and Murlak, F. 2025. Revisiting Conjunctive Query Entailment for S. arXiv:2511.07933. Lutz, C. 2008. The Complexity of Conjunctive Query Answering in Expressive Description Logics. In Proceedings of 4th International Joint Conference on Automated Reasoning, IJCAR 2008, volume 5195 of Lecture Notes in Computer Science, 179–193. Springer. Ortiz, M.; Simkus, M.; and Eiter, T. 2008. Worst-case Optimal Conjunctive Query Answering for an Expressive Description Logic without Inverses. In Proceedings of the Twenty- Third AAAI Conference on Artificial Intelligence, AAAI 2008,

504–510. AAAI Press. Rosati, R. 2011. On the finite controllability of conjunctive query answering in databases under open-world assumption. Journal of Computer and System Sciences, 77(3): 572–594.

19159
