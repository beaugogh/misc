---
title: "Non-Monotonic S4F Standpoint Logic"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38986
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38986/42948
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Non-Monotonic S4F Standpoint Logic

<!-- Page 1 -->

Non-Monotonic S4F Standpoint Logic

Piotr Gorczyca1, Hannes Strass1, 2

1Computational Logic Group, Faculty of Computer Science, TUD Dresden University of Technology, Germany 2ScaDS.AI Center for Scalable Data Analytics and Artificial Intelligence, Dresden/Leipzig, Germany firstname.lastname@tu-dresden.de

## Abstract

Standpoint logics offer unified modal logic-based formalisms for representing multiple heterogeneous viewpoints. At the same time, many non-monotonic reasoning frameworks can be naturally captured using modal logics – in particular using the modal logic S4F. In this work, we propose a novel formalism called S4F Standpoint Logic, which generalises both S4F and propositional standpoint logic and is therefore capable of expressing multi-viewpoint, non-monotonic semantic commitments. We define its syntax and semantics and analyze its computational complexity, obtaining the result that S4F Standpoint Logic is not computationally harder than its constituent logics, whether in monotonic or non-monotonic form. We also outline mechanisms for credulous and sceptical acceptance and illustrate the framework with an example.

Code — https://github.com/cl-tud/nm-s4fsl-asp Extended version — https://arxiv.org/abs/2511.10449

## Introduction

Standpoint logic is a modal logic-based formalism for representing multiple diverse (and potentially conflicting) viewpoints within a single framework. Its main appeal derives from its conceptual simplicity and its attractive properties: In the presence of conflicting information, standpoint logic sacrifices neither consistency nor logical conclusions about the shared understanding of common vocabulary (G´omez

´Alvarez and Rudolph 2021). The underlying idea is to start from a base logic (originally propositional logic; G´omez

´Alvarez and Rudolph 2021) and to enhance it with two modalities pertaining to what holds according to certain standpoints. There, a standpoint is a specific point of view that an agent or other entity can take, and that has a bearing on how the entity understands and employs a given logical vocabulary (that may at the same time be used by other entities with a potentially different understanding). The two modalities are, respectively: □sϕ, expressing “it is unequivocal [from the point of view s] that ϕ”; and its dual ♢sϕ, where “it is conceivable [from the point of view s] that ϕ”.

Standpoint logic escapes global inconsistency by keeping conflicting pieces of knowledge separate, yet avoids duplication of vocabulary and in this way conveniently keeps

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

portions of common understanding readily available. It has historic roots within the philosophical theory of supervaluationism (Bennett 2011), which explains semantic variability “by the fact that natural language can be interpreted in many different yet equally acceptable ways, commonly referred to as precisifications” (G´omez ´Alvarez and Rudolph 2021).

In our work, such semantic commitments can be made on the basis of incomplete knowledge using a form of default reasoning. Consequently, in our logic each standpoint embodies a consistent (but possibly partial) point of view, potentially using non-monotonic reasoning (NMR) to arrive there. This entails that the overall formalism becomes nonmonotonic with respect to its logical conclusions.

Several non-monotonic formalisms that could be employed for default reasoning within standpoints come to mind, and obvious criteria for selection among the candidates are not immediate. We choose to employ the nonmonotonic modal logic S4F (Segerberg 1971; Schwarz and Truszczy´nski 1994), which is a very general formalism that subsumes several other NMR languages, decidedly allowing the possibility for later specialisation via restricting to proper fragments. In this way, we obtain standpoint versions of default logic (Reiter 1980) (see also Example 1 below), answer set programming (Gelfond and Lifschitz 1991), and abstract argumentation (Dung 1995), all as corollaries of our general approach. The usefulness of non-monotonic S4F for knowledge representation and especially non-monotonic reasoning has been aptly demonstrated by Schwarz and Truszczy´nski (1994) (among others), but seems to be underappreciated in the literature to this day.

We illustrate the logic we propose by showcasing a worked example in standpoint default logic, a standpoint variant of Reiter’s default logic (1980), where defaults and definite knowledge can be annotated with standpoint modalities. In Example 1, defaults are of the standard form, namely ϕ: ψ1,..., ψn/ξ where (as usual) if the prerequisite ϕ is established and there is no evidence to the contrary of the justifications ψ1,..., ψn, then the consequence ξ is concluded. An extension is a deductively closed set of formulas representing one possible belief set derived by maximally applying the defaults. A sentence follows credulously if some extension entails it, and sceptically if all extensions do. Example 1. Ovulation disorders are among the leading causes of female infertility. Their origins and diagnostics

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19126

<!-- Page 2 -->

vary, and medical communities do not agree on a unified diagnosis or treatment. For example, community D1 typically attributes ovulation disorders to polycystic ovary syndrome (PCOS), while community D2 often sees functional hypothalamic amenorrhea (FHA) as their main source (unless the patient is pregnant, Preg). The initial treatment for PCOS, as generally accepted in the overall medical community M – including its subcommunities D1 and D2 – involves hormone therapy (Horm); however, this should be avoided in FHA, as it may be ineffective and could mask the underlying issue.1 This can be formalised as a standpoint default theory:

DO:=

□D1(OvuDis: PCOS/PCOS), D1 ≼M,

□D2(OvuDis: ¬Preg, FHA/FHA), D2 ≼M,

□M(PCOS →Horm), □M(FHA →¬Horm)

Now assume a patient is diagnosed with ovulation disorders, DO

1:= DO ∪{□∗OvuDis}. The unique standpoint extension of DO

1 yields □D1(PCOS∧Horm) and □D2(FHA∧¬Horm), so these conclusions follow sceptically. The patient or physician may choose a treatment based on the reputation and trust attributed to the community from which the conclusion derives. If it is later learned that the patient is in fact pregnant – DO

2:= DO 1 ∪{□∗Preg} – then, □D2(FHA ∧¬Horm) is withdrawn, whereas □D1(PCOS ∧Horm) remains.

Compare this with related logics: A plain default theory is obtained by dropping the standpoint modalities. It yields two extensions corresponding to the previous conclusions, which follow credulously but not sceptically. Additionally, the information about which standpoint each conclusion derives from is lost. Alternatively, propositional standpoint logic with strict implications – e.g., □D1(OvuDis →PCOS) and □D2((OvuDis ∧¬Preg) →FHA) – does not support default reasoning, as it lacks means of expressing non-monotonicity.

In this work, we introduce syntax and semantics of S4F standpoint logic, a combination of S4F and standpoint logic that generalises both, including a non-monotonic semantics for default reasoning. We study the computational complexity of the logic and observe that the extension of unimodal S4F to multiple standpoint modalities does not incur any additional computational cost. We conclude with an implementation of our logic in disjunctive answer set programming and a discussion of avenues for future work.

Related Work. Several monotonic logics have been “standpointified” so far: Apart from propositional logic in the original work of G´omez ´Alvarez and Rudolph (2021), also first-order logic and several description logics (G´omez

´Alvarez, Rudolph, and Strass 2022, 2023b, 2023a), the temporal logic LTL (Gigante, G´omez ´Alvarez, and Lyon 2023; Demri and Wałega 2024; Aghamov et al. 2025), and most recently even monodic fragments of first-order logic with counting (G´omez ´Alvarez and Rudolph 2024, 2025).

In previous, preliminary work (2024), we introduced a different, more restrictive non-monotonic standpoint logic

1We show a simplified example of a real-world case where different bodies define PCOS by the presence or absence of certain symptoms (Teede, Deeks, and Moran 2010, Table 1), showcasing the standpoint non-monotonic reasoning captured by our logic.

framework: a two-dimensional modal logic, a product logic (Kurucz et al. 2003) of standpoint logic with S4F, however only considering a fragment of the language (where all formulas are of the form □sϕ or ♢sϕ with ϕ not containing further standpoint modalities). Leisegang, Meyer, and Rudolph (2024) integrated standpoint modalities into KLM propositional logics (Kraus, Lehmann, and Magidor 1990) in a restricted setting (disallowing negation or disjunction of formulas with modalites). Leisegang, Meyer, and Varzinczak (2025) proposed a slightly different KLM-based defeasible standpoint logic offering standpoint modalities and sharpenings that can both be defeasible, but where logical entailment is still monotonic and defeasible implication is among propositional formulas only. Regarding nonmonotonic multi-modal logics, Rosati (2006) generalised the logic of GK (Lin and Shoham 1992) to the multi-agent case, however with an explicit focus on epistemic interpretations of modalities and resulting introspection capabilities.

## Background

All languages we henceforth consider build upon propositional logic, denoted L, built from a set A of atoms according to φ::= p | ¬φ | φ ∧φ where p ∈A, allowing the usual notational shorthands φ∨ψ and φ →ψ. Its model-theoretic semantics is given by valuations E ⊆A containing exactly the true atoms. We denote satisfaction of a formula φ by a valuation E as E ⊩φ and entailment of a formula φ by a set T ⊆L of formulas as T |= φ. By Sub(φ) we denote the set of all subformulas of φ (also for logics introduced later and similarly for theories T). For functions f: A →B, we denote f(C):= {f(a) | a ∈C} for C ⊆A.

Standpoint Logic Standpoint logic (SL) was introduced as a modal logic-based formalism for representing multiple (potentially contradictory) perspectives in a single framework (G´omez ´Alvarez and Rudolph 2021). Building upon propositional logic, in addition to a set A of propositional atoms, it uses a set S of standpoint names, where a standpoint represents a point of view an agent or other entity can take, with ∗∈S being the universal standpoint. Formally, the syntax of propositional standpoint logic is given by φ::= ⊥|p|¬φ|φ∧φ|□sφ|s ≼u where p ∈A, and s, u ∈S. An expression s ≼u is called a sharpening statement and states that all semantic commitments of standpoint u are inherited by standpoint s.

The semantics of standpoint logic is given by standpoint structures N = (Π, σ, γ), where Π is a non-empty set of precisifications (i.e. worlds), σ: S →2Π assigns a set of precisifications to each standpoint name (with σ(∗) = Π fixed), and γ: Π →2A assigns a propositional valuation E ⊆A to each precisification. The satisfiaction relation N, π ⊩φ for π ∈Π is defined by structural induction as follows:

N, π ⊩p:⇐⇒p ∈γ(π) N, π ⊩¬φ:⇐⇒N, π̸ ⊩φ N, π ⊩φ1 ∧φ2:⇐⇒N, π ⊩φ1 and N, π ⊩φ2 N, π ⊩□sφ:⇐⇒N, π′ ⊩φ for all π′ ∈σ(s) N, π ⊩s ≼u:⇐⇒σ(s) ⊆σ(u)

19127

<!-- Page 3 -->

Standpoint structures can be regarded as a restricted form of ordinary (multi-modal) Kripke structures

Π, {Rs}s∈S, γ

, where the worlds are the precisifications Π, the evaluation function of worlds is γ, and the reachability relation for a standpoint name (i.e. modality) s ∈S is Rs = Π × σ(s).

Modal Logic S4F The modal logic S4F is a unimodal logic extending the logic S4 (characterised by axioms K, T, and 4) by axiom schema

(φ ∧¬K¬Kψ) →K(¬K¬φ ∨ψ) (F) and was studied in depth by Segerberg (1971). We are chiefly interested in its non-monotonic semantics and thus approach the logic from its (more accessible) model theory. The syntax of S4F LK is given by φ::= p | ¬φ | φ ∧φ | Kφ with p ∈A. The semantics of S4F is given by S4F structures, tuples M = (V, W, ξ) where V and W are disjoint sets of worlds with W̸ = ∅, and ξ: V ∪W →2A assigns to each world w a valuation ξ(w) ⊆A. The satisfaction relation M, w ⊩φ for w ∈V ∪W is then defined by induction:

M, w ⊩p:⇐⇒p ∈ξ(w) M, w ⊩¬φ:⇐⇒M, w̸ ⊩φ M, w ⊩φ1 ∧φ2:⇐⇒M, w ⊩φ1 and M, w ⊩φ2 M, w ⊩Kφ:⇐⇒ M, v ⊩φ for all v ∈V ∪W if w ∈V, M, v ⊩φ for all v ∈W otherwise. An S4F structure M = (V, W, ξ) is a model of a formula φ ∈LK (theory A ⊆LK), written M ⊩φ (M ⊩A) iff for all w ∈V ∪W, we have M, w ⊩φ (for each φ ∈A). A theory A ⊆LK is satisfiable iff there is an S4F structure F such that F ⊩A. A formula φ ∈LK is entailed by a theory A, written A |=S4F φ, iff every model of A is a model of φ.

S4F structures can also be seen as a restricted form of Kripke structures (V ∪W, R, ξ) with reachability relation R:= (V ×V) ∪(V ×W) ∪(W ×W), comprising two clusters of worlds: outer worlds V and inner worlds W. Intuitively, for an S4F structure (V, W, ξ) all worlds V ∪W are globally possible, but there is an important distinction whether this possibility is known: All inner worlds are known to be possible in any world, while this does not necessarily hold for the outer worlds. Thus V can possibly affect what is known overall, but not what is known in W. S4F has a small model property; its satisfiability problem is NP-complete (Schwarz and Truszczy´nski 1993), entailment “A |=S4F φ?” is coNP-complete. An S4F structure (V, W, ξ) with V = ∅is called an S5 structure and just denoted (W, ξ).

Non-Monotonic S4F A non-monotonic logic is obtained by restricting attention to models where what is known is minimal (Schwarz and Truszczy´nski 1994): Given an S5 structure X = (X, χ), an S4F structure M = (V, W, ξ) is strictly preferred over X iff W = X, ξ|W = χ, and there is a w ∈V with ξ(w) /∈χ(X) (in other words ξ(V)̸ ⊆χ(X)). An S5 structure X = (X, χ) is a minimal model of a theory A ⊆LK iff X is a model for A and there is no S4F structure M that is strictly preferred to X with M a model for A. Intuitively, if M is strictly preferred to X then in M we know strictly less and the knowledge of X is thus not minimal.

S4F in Knowledge Representation The logic S4F is immensely useful for knowledge representation purposes (Schwarz and Truszczy´nski 1993, 1994), as it allows to naturally embed several important logics and formalisms for non-monotonic reasoning, including, but not limited to: Default Logic. For a general default ϕ: ψ1,..., ψm/ξ (Reiter 1980), the corresponding S4F formula is given by (Kϕ ∧K¬K¬ψ1 ∧... ∧K¬K¬ψm) →Kξ. Logic Programs. A given normal logic program rule p0 ←p1,..., pm, ∼pm+1,..., ∼pm+n is translated into (Kp1∧...∧Kpm∧K¬Kpm+1∧...∧K¬Kpm+n) →Kp0, and similar translation results exist for extended and disjunctive logic programs (Schwarz and Truszczy´nski 1994). Argumentation Frameworks. An AF F = (A, R) (under stable semantics) is translated into the S4F theory TF:= {K¬K¬a →Ka | a ∈A} ∪{Ka →K¬b | (a, b) ∈R}, which follows from Dung’s translation of AFs into normal logic programs [Dung, 1995, Section 5; Strass, 2013].

The above formalisms can be modularly (piece by piece, without looking at the entire theory) and faithfully (preserving the semantics one-to-one) embedded into S4F. Further S4F embeddings are possible: e.g. the (bimodal) logic of GK by Lin and Shoham (1992) as well as the (bimodal) logic of MKNF by Lifschitz (1994), all with S4F being unimodal and thus arguably offering a simpler semantics.

Among the non-monotonic modal logics capable of faithfully embedding the above formalisms, S4F stands out as a prominent candidate for several reasons, including (but not limited to) its intuitive model theory and its relative computational easiness compared to other logics (e.g. S4, for which satisfiability is PSpace-complete; Halpern and Moses 1992). Furthermore, other logics need not guarantee modularity (e.g. KD45; Gottlob 1995; Moore 1985) or have issues with explicit definitions (Schwarz and Truszczy´nski 1994).

Complexity of Non-Monotonic S4F The decision problems associated with non-monotonic S4F were found to reside on the second level of the polynomial hierarchy (Schwarz and Truszczy´nski 1993). As we later generalise it, below we sketch the procedure for deciding whether a given S4F theory A ⊆LK has a minimal model. The actual minimal model X cannot always be explicitly constructed due to potentially containing exponentially many worlds (w.r.t. A), thus a “smaller” representation is required. The idea for this – going back to Shvarts (1990) – is to represent X by giving all subformulas Kϕ of A with X ⊩Kϕ.

More technically, denote AK:= {φ | Kφ ∈Sub(A)}; a partition (Φ, Ψ) of AK then intuitively represents an S5 structure X in which all formulas in Ψ are known and all formulas in Φ are not known. Surprisingly, it can be decided whether X is a minimal model of A by consulting only (Φ, Ψ): Formally, Schwarz and Truszczy´nski (1993) define

Θ:= A ∪{¬Kφ | φ ∈Φ} ∪{Kψ | ψ ∈Ψ} ∪Ψ which is read as a theory of propositional logic with subformulas Kϕ regarded as atoms that are independent of ϕ. Now the pair (Φ, Ψ) corresponds to a minimal S4F model X of A iff (a) Θ is satisfiable in propositional logic, (b) for each ϕ ∈Φ, we have Θ̸ |= ϕ, and (c) for each ψ ∈Ψ, we

19128

<!-- Page 4 -->

have A ∪{¬Kϕ | ϕ ∈Φ} |=S4F ψ. Since the number of NP oracle calls to verify (a–c) is polynomial (actually linear) in AK, we get containment in ΣP

2 (Schwarz and Truszczy´nski 1993). A matching lower bound follows from the faithful embedding of default logic (Reiter 1980) into S4F (Schwarz and Truszczy´nski 1994) and Gottlob’s result on the complexity of extension existence in default logic (1992).

Non-Monotonic S4F Standpoint Logic

Herein, we propose non-monotonic multi-modal S4F with modalities restricted as in standpoint logic. We proceed to show that the combination of the two logics exhibits all “nice” properties of the constituents. The syntax of the new logic is almost the same as ordinary standpoint logic; we just disallow to nest sharpening statements into formulas.2

Definition 2. The language L≼

S of S4F standpoint logic over atoms A and standpoint names S contains expressions φ that are either sharpening statements s ≼u or formulas ψ of propositional multi-modal logic with modalities S, i.e., φ::= s ≼u | ψ with ψ::= p | ¬ψ | ψ1 ∧ψ2 | □sψ where p ∈A and s, u ∈S. A theory is a subset T ⊆L≼

S.

As usual, we require the universal standpoint ∗∈S. By LS we denote the proper fragment that contains formulas only.

Thus in the actual syntax of our logic, a standpoint-annotated default □s(ϕ: ψ1,..., ψn/ξ) is syntactic sugar for a formula (□sϕ ∧□s¬□s¬ψ1 ∧... ∧□s¬□s¬ψn) →□sξ. For instance, □M(OvuDis: PCOS/PCOS) of Example 1 stands for (□MOvuDis ∧□M¬□M¬PCOS) →□MPCOS.

The major novel aspects of our logic are the new monotonic and non-monotonic semantics. We start with introducing the structures that are used in both model theories.

Definition 3. Let A be a set of propositional atoms and S be a set of standpoint names. An S4F standpoint structure (over A and S) is a tuple F = (Π, σ, τ, γ) where

• Π is a non-empty set of precisifications, • σ, τ: S →2Π are functions such that σ(∗) ∪τ(∗) = Π and for all s, u ∈S: σ(s)̸ = ∅and σ(s) ∩τ(u) = ∅; • γ: Π →2A maps every precisification π ∈Π to a propositional valuation E ⊆A.

S4F standpoint structures thus mainly comprise precisifications π ∈Π that each have a propositional valuation γ(π) attached as before. Additionally, each standpoint s distinguishes inner precisifications σ(s) and outer precisifications τ(s) that are disjoint across all standpoints, with ∗still being universal. Intuitively, every standpoint s ∈S has “its own” associated S4F structure (τ(s), σ(s), γ). This insight motivates the following definition of the satisfaction relation.

Definition 4. Let F = (Π, σ, τ, γ) be an S4F standpoint structure and φ ∈L≼

S. For π ∈Π, the (pointed) satisfaction relation F, π ⊩φ is defined by structural induction:

2This is not a severe restriction; several standpoint logics or precursors have similar conditions, with no known issues (G´omez

´Alvarez 2019; G´omez ´Alvarez, Rudolph, and Strass 2023b,a).

τO(∗) τO(M) τO(D2) τO(D1) π3: {O, Pr, F}

π4: {O, Pr}

π1: {O, Pr, H, P, F} π2: {O, Pr, H, F}

σO(∗) σO(M) σO(D2) σO(D1)

π8: {O, Pr, H, P} π7: {O, Pr, H}

π5: {O, Pr, P} π6: {O, Pr, P, F}

**Figure 1.** An S4F standpoint structure FO = (ΠO, σO, τO, γO) that is a model of theory DO

2 from Example 1. Precisifications ΠO = {π1,..., π8} within a box belong to the outer (upper) or inner (lower) set of precisifications of the standpoint labelling the box, e.g. π8 ∈σO(D1) ⊆σO(D2). (Satisfaction FO ⊩D1 ≼D2 is coincidental and not required by DO

2.) Precisification π’s valuation is shown as a set γO(π) of atoms below π. Atoms are abbreviated thus: OvuDis (O), Preg (Pr), Horm (H), PCOS (P), and FHA (F). For example, FO ⊩□∗(Pr ∧O) (as FO, π ⊩Pr ∧O for all π ∈ΠO) and FO, π5 ⊩□MH (since FO, π ⊩H for all π ∈σO(M)), while FO, π1̸ ⊩□MH (as FO, π3̸ ⊩H with π3 ∈τO(M)), whence FO, π1 ⊩♢M¬H. Intuitively, from the medical standpoint M, ¬H is conceivable at π1, whereas H is unequivocal at π5.

F, π ⊩p:⇐⇒p ∈γ(π) F, π ⊩¬ψ:⇐⇒F, π̸ ⊩ψ F, π ⊩ψ1 ∧ψ2:⇐⇒F, π ⊩ψ1 and F, π ⊩ψ2 F, π ⊩□sψ:⇐⇒ F, π′ ⊩ψ for all π′ ∈σ(s) if π ∈σ(∗), F, π′ ⊩ψ for all π′ ∈σ(s) ∪τ(s) otherwise.

F, π ⊩s ≼u:⇐⇒σ(s) ⊆σ(u) and τ(s) ⊆τ(u) F ⊩φ:⇐⇒F, π ⊩φ for all π ∈Π

As usual, a structure F is a model of a theory T ⊆L≼

S iff F ⊩φ for all φ ∈T; a theory T ⊆L≼

S is satisfiable iff there exists a structure F such that F ⊩T; a formula φ ∈L≼

S is entailed by a theory T ⊆L≼

S, denoted T |=S φ, iff every model of T is a model of φ. Again, S4F standpoint structures can be recast as ordinary (multi-modal) Kripke structures (Π, {Rs}s∈S, γ) where each s ∈S has reachability relation Rs:= τ(∗) × τ(s) ∪τ(∗) × σ(s) ∪σ(∗) × σ(s). For illustration, Figure 1 graphically depicts an S4F standpoint structure for Example 1 along with some satisfied formulas.

The sharpening statements of a theory T form a hierarchy of standpoints (with ∗at the top) that we sometimes need. Definition 5. Let T ⊆L≼

S be a theory over standpoint names S. For s, u ∈S we say that s sharpens u and write T ⊢S s ≼u, which is defined by induction as follows:

• T ⊢S s ≼u if s ≼u ∈T or u = ∗or s = u; (base cases) • T ⊢S s ≼u if there is some t ∈S such that s ≼t ∈T and T ⊢S t ≼u. (inductive case)

19129

<!-- Page 5 -->

It is clear that for finite T ⊆L≼

S and s, u ∈S, the question whether T ⊢S s ≼u can be decided in deterministic polynomial time by checking reachability in the directed graph (S, {(s, u) | s ≼u ∈T} ∪S × {∗}). Furthermore, all sharpening statements that we can establish via reachability are correct with respect to the model theory, as this result shows. Lemma 6. For any theory T ⊆L≼

S and s, u ∈S, 1. T ⊢S s ≼u implies T |=S s ≼u, and 2. if T is satisfiable, then T ⊢S s ≼u iff T |=S s ≼u.

Non-Monotonic Semantics In uni-modal S4F, the non-monotonic semantics seeks to minimise the amount of knowledge contained in a structure X. Similarly, in the non-monotonic semantics of S4F standpoint logic we seek to minimise the amount of determination contained in the structure of each standpoint. Intuitively, this leads to standpoints making semantic commitments only insofar it is absolutely necessitated by a given theory. To this end, we firstly introduce a preference ordering on structures. Definition 7. Consider the S4F standpoint structures F1 = (Π1, σ1, τ1, γ1) and F2 = (Π2, σ2, τ2, γ2) over standpoint names S and s ∈S. We define the following orderings:

F1 ⊴s F2:⇐⇒γ2(σ2(s)) = γ1(σ1(s)) and γ2(τ2(s)) ⊆γ1(σ1(s) ∪τ1(s)) F1 ⊴F2:⇐⇒F1 ⊴s F2 for all s ∈S F1 ◁F2:⇐⇒F1 ⊴F2 and F2̸ ⊴F1 F1 ≃F2:⇐⇒F1 ⊴F2 and F2 ⊴F1 Intuitively, F1 ⊴F2 expresses that for all standpoints, F2 is at least as determined as F1, with respect to the structures’ semantic commitments. In our non-monotonic semantics, we are interested in structures where such commitments are minimal (subject to still satisfying a given theory). We call an S4F standpoint structure an S5 standpoint structure whenever for all s ∈S we have τ(s) = ∅.

Definition 8. Let T ⊆L≼

S. An S5 standpoint structure F is a minimal model of T iff (1) F ⊩T and (2) for all S4F standpoint structures F′ ⊴F with F′ ⊩T, we find F′ ≃F. As usual, an expression φ ∈L≼

S is credulously (sceptically) entailed by a theory T ⊆L≼

S, denoted T |≈cred φ (T |≈scep φ), iff F ⊩φ for some (all) minimal model(s) F of T. E.g. a minimal model F′

O = (Π′

O, σ′

O, τ ′

O, γ′

O) of theory DO

2 from Example 1 is obtained from FO (see Figure 1) by moving all outer precisifications into their respective inner sets (yielding e.g. σ′

O(D2) = τO(D2) ∪σO(D2)) thus emptying the outer sets.

We observe that S4F standpoint logic generalises both propositional standpoint logic (G´omez ´Alvarez and Rudolph 2021) (via S5 standpoint structures; only atomic sharpening statements) as well as unimodal S4F (Schwarz and Truszczy´nski 1994) (via S = {∗} and replacing every occurrence of K in a theory T by □∗, denoted T[K/□∗]). Proposition 9. 1. For any theory T of propositional stand- point logic such that sharpening statements occur in T as atoms only, there is a bijection between the set of standpoint structures N that satisfy T and the set of S5 standpoint structures F that satisfy T.

2. For any theory T ⊆LK of S4F, there is a bijection between the set of S4F structures M that satisfy T and the set of S4F standpoint structures F that satisfy T[K/□∗].

Expansions Historically, the semantics of non-monotonic reasoning formalisms was not formulated in terms of minimal models from the start. A more common formulation employed deductively closed sets where non-monotonic inferences have been maximally applied. For example, Reiter (1980) defined the semantics of default logic via so-called extensions; Mc- Dermott and Doyle (1980) devised a scheme for obtaining non-monotonic modal logics (of which unimodal S4F is an instance) and defined the semantics based on expansions; Moore (1985) gave an equally named concept for autoepistemic logic (a logic that can actually be cast into the scheme of McDermott and Doyle as non-monotonic modal logic KD45; Shvarts 1990). Our definition below is a generalisation of these notions to the multi-modal (standpoint) case.

Definition 10. Let T ⊆LS. A set U ⊆LS is an expansion of T iff U ={ψ ∈LS | T ∪{¬□sϕ | □sϕ ∈LS\U} |=S ψ}.

Intuitively, a theory U is an expansion of T if, by only using the original theory T and negative introspection (w.r.t. U), the expansion U can be reproduced exactly.

We can show that expansions are an alternative, but equivalent way to define the non-monotonic semantics of S4F standpoint logic. The fundamental insight that expansions in the scheme of McDermott and Doyle (1980) can be equivalently formulated in terms of S5 structures goes back to Schwarz (1992); Marek, Shvarts, and Truszczynski (1993) later extensively studied such correspondences for various (non-monotonic) modal logics. Our main result on this topic shows that the correspondence can be lifted from unimodal to multi-modal non-monotonic (standpoint) logics.

Theorem 11. Let T ⊆LS be a theory. An S5 standpoint structure F is a minimal model of T iff the theory of F, the set Th(F):= {ψ ∈LS | F ⊩ψ}, is an expansion of T.

S4F Standpoint Logic: Complexity Analysis Complexity of Monotonic S4F Standpoint Logic Reasoning within monotonic S4F standpoint logic is interesting in its own right, but also relevant for reasoning with the non-monotonic minimal-model semantics. We start out with model checking, that is, given a formula ψ (finite theory T) and a structure F = (Π, σ, τ, γ) (and possibly a precisification π ∈Π), does F, π ⊩ψ (respectively F ⊩T) hold?

Proposition 12. The model checking problem for S4F standpoint logic (formulas and finite theories) is in P. Proof (Sketch). We can check F, π ⊩ψ bottom-up by considering all subformulas in order of increasing size. There are linearly many such checks, and each check in the worst case (of □∗ξ) involves all (linearly many) precisifications.□

As is the case for other standpoint logics (G´omez ´Alvarez, Rudolph, and Strass 2022), one useful aspect of (monotonic) S4F standpoint logic is that satisfiable theories always have small models, where “small” here means linear

19130

<!-- Page 6 -->

in the size of the theory. The size of a (finite) theory T is ∥T∥:= P φ∈T ∥φ∥with the size of a formula φ defined as the number of its subformulas, ∥φ∥:= |Sub(φ)|, and the size of a sharpening statement being ∥s ≼u∥:= 2.

Theorem 13. Let T ⊆L≼

S be finite. If T is satisfiable, then there exists a model of T with at most ∥T∥precisifications. Proof (Sketch). We employ a standard idea (Halpern and Moses 1992; Schwarz and Truszczy´nski 1993; G´omez

´Alvarez, Rudolph, and Strass 2022): Each □uξ ∈Sub(T) with F̸ ⊩□uξ has a witness precisification π ∈σ(u) ∪τ(u) with F, π̸ ⊩ξ. We keep one such witness for each dissatisfied □uξ ∈Sub(T) to obtain a model of size at most ∥T∥.□

We next address the satisfiability problem of S4F standpoint logic, that is, given a finite theory T ⊆L≼

S, does there exist a structure F that is a model of T? To decide it, we use the small model property as expected. The proposition below generalises the known results on unimodal S4F (Schwarz and Truszczy´nski 1993) and multi-modal propositional standpoint logic (G´omez ´Alvarez and Rudolph 2021). Proposition 14. The satisfiability problem for S4F standpoint logic is NP-complete. Proof. NP-hardness carries over from the proper fragment of propositional logic, so it remains to show membership. Given a theory T ⊆LS, we guess an S4F standpoint structure F with at most ∥T∥many precisifications and then check whether F ⊩φ for all φ ∈T. The latter check can be done in deterministic polynomial time by Proposition 12. □

Note that theory satisfiability cannot be reduced to formula satisfiability, as formulas lack sharpening statements.

Characterising Minimal Models In this section, we show how the minimal models of a theory T ⊆L≼

S can be parsimoniously represented, which paves the way for subsequent complexity analyses. For the purposes of our constructions, we consider (w.l.o.g.) the vocabulary A of T to consist only of those atoms that actually occur in T.

The main idea of our syntactic characterisation of minimal models follows Shvarts (1990) in that we reduce to propositional logic over the extended vocabulary A± ⊇A where subformulas of the form □sξ (and sharpening statements) are regarded as propositional atoms. The major novelty of our construction is the incorporation of sharpening statements via the hierarchy of standpoints. For brevity, we sometimes denote ¬Φ:= {¬φ | φ ∈Φ} for a set Φ ⊆L≼

S.

Definition 15. Let T ⊆L≼

S be an S4F standpoint theory and denote T □:= {□sϕ | □sϕ ∈Sub(T) for some s ∈S}. For a partition (Φ, Ψ) of T □we define the following conditions: (C1) For every s ∈S, the theory Θs:= T ∪¬Φ ∪Ψ ∪Ψs is satisfiable in propositional logic, where we define Ψs:= {ψ | □uψ ∈Ψ for some u ∈S with T ⊢S s ≼u}. (C2) For every s ∈S and □uϕ ∈Φ for some u ∈S with

T ⊢S u ≼s, the theory Θs ∪{¬ϕ} is satisfiable in propositional logic. (C3) For every s ∈S and □sψ ∈Ψ, T ∪¬Φ |=S □sψ.

Whenever a partition Ξ(T) = (Φ, Ψ) satisfies (C1), we can construct an S5 standpoint structure from it.

Definition 16. Given a partition Ξ(T) = (Φ, Ψ) satisfying (C1), define S5 standpoint structure FΞ(T) = (Π, σ, τ, γ) where for s ∈S, σ(s):= {F ∩A | F ⊆A± with F ⊩Θs} and τ(s):= ∅, and Π:= σ(∗) with γ(π):= π for all π ∈Π.

Clearly, if Ξ(T) satisfies (C1), then FΞ(T) is well-defined because σ(s)̸ = ∅for any s ∈S. Our subsequent main results show that the construction is correct and partitions therefore provide a valid way of characterising (minimal) models for theories. We start with soundness.

Theorem 17. Let T ⊆L≼

S and Ξ(T) = (Φ, Ψ) be a partition of T □such that Ξ(T) satisfies (C1).

1. If Ξ(T) also satisfies (C2), then FΞ(T) ⊩T; 2. if Ξ(T) also satisfies (C2) and (C3), then FΞ(T) is a minimal model of T.

Proof (Sketch). The key to the proof is showing that for all s ∈S, F ⊆A± with F ⊩Θs, and φ ∈Sub(T), we have F ⊩φ iff FΞ(T), F ∩A ⊩φ. With this, we can then show FΞ(T) ⊩T, where satisfaction of sharpening statements holds by construction. For minimality, we assume F ⊴FΞ(T) with F ⊩T and employ a helper result establishing that F ⊴FΞ(T) implies F ⊩

¬□uϕ

FΞ(T)̸ ⊩□uϕ

. This serves to show γ(τ(s)) ⊆γ′(σ′(s)), thus FΞ(T) ⊴F.□

This shows soundness of the characterisation; we can also show completeness, which is the more involved direction.

Theorem 18. Let T ⊆L≼

S be an S4F standpoint theory and F be an S5 standpoint structure for the vocabulary of T.

1. If F ⊩T, then T □has a partition (Φ, Ψ) that satisfies (C1) and (C2); 2. if F is a minimal model of T, then T □has a partition (Φ, Ψ) that satisfies (C1), (C2), and (C3).

Proof (Sketch). With F ⊩T, it is clear to define the partition Ξ(T, F) = (Φ, Ψ) by Ψ:=

□uϕ ∈T □ F ⊩□uϕ and Φ:= T □\ Ψ. A first helper claim then again connects the propositional and modal readings of formulas: for any s ∈S and π ∈σ(s) we define the propositional valuation Fπ:= γ(π) ∪Ψ ⊆A± for which it holds for all φ ∈Sub(T) that Fπ ⊩φ iff F, π ⊩φ. This then serves to establish another helper result by which for any s ∈S and π ∈σ(s), we have Fπ ⊩Θs; in turn, this can be used to prove (C1) and (C2). For (C3), we do a proof by contradiction and assume there is some □sψ ∈Ψ such that T ∪¬Φ̸ |=S □sψ. Then there exists an S4F standpoint structure F′ with F′ ⊩T ∪¬Φ and F′̸ ⊩□sψ. The two structures F and F′ can be combined to a third structure F′′ with F′′ ⊴F that can be shown to also be a model for T with F′′̸ ⊩□sψ (this is actually the most laborious part of the proof). But this then yields F′′ ◁F with F′′ ⊩T although F is a minimal model of T, the desired contradiction. □

In our running Example 1, the minimal model F′

O of theory DO

2 given earlier can be characterised as pair (Φ′ 2, Ψ′ 2), with {□∗O, □∗Pr, □D1P, □D1H} ⊆Ψ′

2 and {□D2F} ⊆Φ′ 2, where the latter containment intuitively expresses that ¬FHA is conceivable from standpoint D2.

19131

<!-- Page 7 -->

Complexity of Non-Monotonic S4F SL Given that each minimal model of an S4F standpoint logic theory T ⊆L≼

S can be parsimoniously represented via a partition Ξ(T) of T □, for dealing with various decision problems surrounding minimal models we can resort to computing with such representations instead of computing with actual models (that might be of worst-case exponential size).

Theorem 19. Deciding existence of a minimal model for an S4F standpoint logic theory T ⊆L≼

S is ΣP

2 -complete. Proof. The lower bound follows from unimodal S4F (Schwarz and Truszczy´nski 1993), so let us focus on containment. The general approach is clear: Given T ⊆L≼

S, we obtain T □, guess a partition Ξ(T) = (Φ, Ψ), and verify (C1), (C2), and (C3). Verifying (C1) and (C2) can be done using the NP oracle for the polynomially many satisfiability checks of propositional logic, where all involved theories are polynomial in the size of T. For (C3), we make use of Proposition 14 and employ the NP oracle to do |Ψ| ≤∥T∥many satisfiability checks of monotonic S4F standpoint logic. □

The idea for credulous and sceptical entailment is then to many-one-reduce it to minimal model existence as follows:

Theorem 20. Let T ⊆L≼

S be a theory, ξ ∈L≼

S be a formula, and assume atom z ∈A does not occur in T ∪{ξ}.

1. T |≈cred ξ iff T ξ cred has a minimal model, where

T ξ cred:= T ∪{(□∗¬□∗z ∧□∗¬□∗ξ) →□∗z} 2. T |̸≈scep ξ iff T ξ scep has a minimal model, where

T ξ scep:= T ∪{(□∗¬□∗z ∧¬□∗¬□∗ξ) →□∗z}

Proof (Sketch). Intuitively, the additional atom z and implications serve as integrity constraints that eliminate all minimal models that do (not) contain the formula ξ to be queried: A minimal model F is an S5 standpoint structure by definition, so either (a) F ⊩□∗z or (b) F ⊩¬□∗z, and in case (b) then F ⊩□∗¬□∗z due to negative introspection. It can be shown that (a) is impossible because the only reason for it requires (b); thus the other conjunct (¬)□∗¬□∗ξ in the implication’s prerequisite must be dissatisfied. For example, in credulous entailment, F̸ ⊩□∗¬□∗ξ yields F ⊩□∗ξ; the conclusion is dual for sceptical reasoning. □

Given T and ξ, the theories T ξ cred and T ξ scep can clearly be constructed in deterministic polynomial time. Thus the respective complexities follow, with lower bounds obtained from the proper fragment of default logic (Gottlob 1992).

Corollary 21. The problem “Given T and ξ, does T |≈cred ξ hold?” is ΣP

2 -complete. The problem “Given T and ξ, does T |≈scep ξ hold?” is ΠP

2 -complete.

Disjunctive ASP Encoding We provide a proof-of-concept implementation of S4F standpoint logic by developing an encoding in disjunctive answer set programming using the saturation technique (Eiter and Gottlob 1995). The main insight underlying the encoding is to equivalently reformulate the guess-andcheck approach described in the previous section as follows:

(1) We guess, independently, the following:

(a) a partition Ξ(T) = (Φ, Ψ) of T □; (b) for every standpoint name s ∈S, a propositional valu- ation Es of the extended vocabulary A± = A ∪T □; (c) for each □uξ ∈T □, a valuation E□uξ ⊆A±.

(2) We next verify (in deterministic polynomial time):

(a) Es ⊩Θs for all s ∈S; (b) for every □uϕ ∈Φ, we have that E□uϕ ⊩Θs ∪{¬ϕ}

for all s ∈S with T ⊢S u ≼s.

(3) We finally verify (using the NP oracle) that for every

□sψ ∈Ψ, we have that T ∪¬Φ |=S □sψ.

Our ASP encoding now guesses just like in (1) above, verifies (2) via straightforward evaluation of propositional formulas (with T ⊢S u ≼s being obtained directly via rules), and implements (3) via a saturation encoding that checks, for every □sψ ∈Ψ independently, that T ∪¬Φ ∪{¬□sψ} is unsatisfiable. Each such check makes use of the small model property of S4F standpoint logic (Theorem 13) and works by verifying that all S4F standpoint structures up to the maximal possible size are not models; technically, model candidates are disjunctively guessed and then checked off if they violate some required property. The full encoding is available at https://github.com/cl-tud/nm-s4fsl-asp.

Our implementation continues and generalises a long line of research implementing default and autoepistemic reasoning formalisms via answer set programming: Junker and Konolige (1990) implemented default and autoepistemic logics via truth maintenance systems, which are known to be equivalent to logic programs under the stable model semantics (Reinfrank, Dressler, and Brewka 1989). The system dl2asp (Chen et al. 2010) works similarly to the work of Junker and Konolige. Ji and Strass (2014) provided a disjunctive ASP encoding of default logic via the logic of GK (Lin and Shoham 1992).

## Discussion

In this paper, we introduced S4F standpoint logic, which combines and generalises propositional standpoint logic (G´omez ´Alvarez and Rudolph 2021) and (non-monotonic) S4F (Schwarz and Truszczy´nski 1994). It constitutes the first full-fledged, unrestricted non-monotonic standpoint logic covering, by corollary, standpoint default logic, standpoint answer set programming, and standpoint argumentation frameworks. We demonstrated that the addition of multiple standpoints to non-monotonic S4F comes at no additional computational cost, and based on this insight presented a disjunctive ASP encoding that implements our logic.

For future work, we are interested in simplifying our decision procedure for the proper fragments of standpoint logic programs and standpoint argumentation frameworks, as the satisfiability problems of the base languages are easier (NP-complete; Bidoit and Froidevaux 1991, Marek and Truszczy´nski 1991, LPs; Dunne and Wooldridge 2009, AFs) unless the polynomial hierarchy collapses. We also want to study strong equivalence for S4F standpoint logic; the case of unimodal S4F was studied by Truszczy´nski (2007).

19132

<!-- Page 8 -->

## Acknowledgements

This work was supported by funding from BMFTR (Federal Ministry of Research, Technology and Space) within projects KIMEDS (grant no. GW0552B), MEDGE (grant no. 16ME0529), SEMECO (grant no. 03ZU1210B), and SE- CAI (via DAAD project 57616814, School of Embedded Composite AI, https://secai.org/, as part of the program Konrad Zuse Schools of Excellence in Artificial Intelligence).

## References

Aghamov, R.; Baier, C.; Karimov, T.; Majumdar, R.; Ouaknine, J.; Piribauer, J.; and Spork, T. 2025. Model Checking Linear Temporal Logic with Standpoint Modalities. CoRR, abs/2502.20193. Bennett, B. 2011. Standpoint semantics: a framework for formalising the variable meaning of vague terms. Understanding Vagueness. Logical, Philosophical and Linguistic Perspectives, 261–278. Bidoit, N.; and Froidevaux, C. 1991. Negation by Default and Unstratifiable Logic Programs. Theor. Comput. Sci., 78(1): 86–112. Chen, Y.; Wan, H.; Zhang, Y.; and Zhou, Y. 2010. dl2asp: Implementing Default Logic via Answer Set Programming. In Janhunen, T.; and Niemel¨a, I., eds., Logics in Artificial Intelligence – 12th European Conference, JELIA 2010, Helsinki, Finland, September 13–15, 2010. Proceedings, volume 6341 of Lecture Notes in Computer Science, 104– 116. Springer. Demri, S.; and Wałega, P. A. 2024. Computational Complexity of Standpoint LTL. In Endriss, U.; Melo, F. S.; Bach, K.; Diz, A. J. B.; Alonso-Moral, J. M.; Barro, S.; and Heintz, F., eds., ECAI 2024 – 27th European Conference on Artificial Intelligence, 19–24 October 2024, Santiago de Compostela, Spain – Including 13th Conference on Prestigious Applications of Intelligent Systems (PAIS 2024), volume 392 of Frontiers in Artificial Intelligence and Applications, 1206–1213. IOS Press. Dung, P. M. 1995. On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games. Artif. Intell., 77(2): 321–358. Dunne, P. E.; and Wooldridge, M. 2009. Complexity of Abstract Argumentation, 85–104. Boston, MA: Springer US. ISBN 978-0-387-98197-0. Eiter, T.; and Gottlob, G. 1995. On the Computational Cost of Disjunctive Logic Programming: Propositional Case. Ann. Math. Artif. Intell., 15(3–4): 289–323. Gelfond, M.; and Lifschitz, V. 1991. Classical Negation in Logic Programs and Disjunctive Databases. New Gener. Comput., 9(3/4): 365–386. Gigante, N.; G´omez ´Alvarez, L.; and Lyon, T. S. 2023. Standpoint Linear Temporal Logic. In Marquis, P.; Son, T. C.; and Kern-Isberner, G., eds., Proceedings of the 20th International Conference on Principles of Knowledge Representation and Reasoning, KR 2023, Rhodes, Greece, September 2–8, 2023, 311–321.

Gorczyca, P.; and Strass, H. 2024. Adding Standpoint Modalities to Non-Monotonic S4F: Preliminary Results. In Gierasimczuk, N.; and Heyninck, J., eds., Proceedings of the 22nd International Workshop on Non-Monotonic Reasoning. Gottlob, G. 1992. Complexity Results for Nonmonotonic Logics. Journal of Logic and Computation, 2(3): 397–425. Gottlob, G. 1995. Translating Default Logic into Standard Autoepistemic Logic. J. ACM, 42(4): 711–740.

G´omez ´Alvarez, L. 2019. Standpoint logic: a logic for handling semantic variability, with applications to forestry information. Ph.D. thesis, University of Leeds, UK.

G´omez ´Alvarez, L.; and Rudolph, S. 2021. Standpoint Logic: Multi-Perspective Knowledge Representation. In Neuhaus, F.; and Brodaric, B., eds., Formal Ontology in Information Systems – Proceedings of the Twelfth International Conference, FOIS 2021, Bozen-Bolzano, Italy, September 11–18, 2021, volume 344 of Frontiers in Artificial Intelligence and Applications, 3–17. IOS Press.

G´omez ´Alvarez, L.; and Rudolph, S. 2024. Reasoning in SHIQ with Axiom- and Concept-Level Standpoint Modalities. In Marquis, P.; Ortiz, M.; and Pagnucco, M., eds., Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning, KR 2024, Hanoi, Vietnam. November 2–8, 2024. G´omez ´Alvarez, L.; and Rudolph, S. 2025. Putting Perspective into OWL [sic]: Complexity-Neutral Standpoint Reasoning for Ontology Languages via Monodic S5 over Counting Two-Variable First-Order Logic. In Proceedings of the 22nd International Conference on Principles of Knowledge Representation and Reasoning, 366–375.

G´omez ´Alvarez, L.; Rudolph, S.; and Strass, H. 2022. How to Agree to Disagree – Managing Ontological Perspectives using Standpoint Logic. In Sattler, U.; Hogan, A.; Keet, C. M.; Presutti, V.; Almeida, J. P. A.; Takeda, H.; Monnin, P.; Pirr`o, G.; and d’Amato, C., eds., The Semantic Web – ISWC 2022 – 21st International Semantic Web Conference, Virtual Event, October 23–27, 2022, Proceedings, volume 13489 of Lecture Notes in Computer Science, 125–141. Springer.

G´omez ´Alvarez, L.; Rudolph, S.; and Strass, H. 2023a. Pushing the Boundaries of Tractable Multiperspective Reasoning: A Deduction Calculus for Standpoint EL+. In Marquis, P.; Son, T. C.; and Kern-Isberner, G., eds., Proceedings of the 20th International Conference on Principles of Knowledge Representation and Reasoning, KR 2023, Rhodes, Greece, September 2–8, 2023, 333–343.

G´omez ´Alvarez, L.; Rudolph, S.; and Strass, H. 2023b. Tractable Diversity: Scalable Multiperspective Ontology Management via Standpoint EL. In Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, IJCAI 2023, 19th–25th August 2023, Macao, SAR, China, 3258–3267. ijcai.org. Halpern, J. Y.; and Moses, Y. 1992. A Guide to Completeness and Complexity for Modal Logics of Knowledge and Belief. Artif. Intell., 54(2): 319–379.

19133

<!-- Page 9 -->

Ji, J.; and Strass, H. 2014. From Default and Autoepistemic Logics to Disjunctive Answer Set Programs via the Logic of GK. In Schaub, T.; Friedrich, G.; and O’Sullivan, B., eds., ECAI 2014 – 21st European Conference on Artificial Intelligence, 18–22 August 2014, Prague, Czech Republic – Including Prestigious Applications of Intelligent Systems (PAIS 2014), volume 263 of Frontiers in Artificial Intelligence and Applications, 1039–1040. IOS Press. Junker, U.; and Konolige, K. 1990. Computing the Extensions of Autoepistemic and Default Logics with a Truth Maintenance System. In Shrobe, H. E.; Dietterich, T. G.; and Swartout, W. R., eds., Proceedings of the 8th National Conference on Artificial Intelligence. Boston, Massachusetts, USA, July 29 – August 3, 1990, 2 Volumes, 278–283. AAAI Press / The MIT Press. Kraus, S.; Lehmann, D.; and Magidor, M. 1990. Nonmonotonic Reasoning, Preferential Models and Cumulative Logics. Artif. Intell., 44(1–2): 167–207. Kurucz, A.; Wolter, F.; Zakharyaschev, M.; and Gabbay, D. M. 2003. Many-dimensional modal logics: Theory and applications. Elsevier. Leisegang, N.; Meyer, T.; and Rudolph, S. 2024. Towards Propositional KLM-Style Defeasible Standpoint Logics. In Gerber, A.; Maritz, J.; and Pillay, A. W., eds., Proceedings of the 5th Southern African Conference on AI Research (SACAIR’24), volume 2326 of CCIS, 459–475. Springer. Leisegang, N.; Meyer, T.; and Varzinczak, I. 2025. Extending Defeasibility for Propositional Standpoint Logics. In Logics in Artificial Intelligence: 19th European Conference, JELIA 2025, Kutaisi, Georgia, September 1–4, 2025, Proceedings, Part II, 43–57. Berlin, Heidelberg: Springer- Verlag. ISBN 978-3-032-04589-8. Lifschitz, V. 1994. Minimal Belief and Negation as Failure. Artif. Intell., 70(1–2): 53–72. Lin, F.; and Shoham, Y. 1992. A Logic of Knowledge and Justified Assumptions. Artif. Intell., 57(2–3): 271–289. Marek, V. W.; Shvarts, G. F.; and Truszczynski, M. 1993. Modal Nonmonotonic Logics: Ranges, Characterization, Computation. J. ACM, 40(4): 963–990. Marek, V. W.; and Truszczy´nski, M. 1991. Autoepistemic Logic. J. ACM, 38(3): 588–619. McDermott, D. V.; and Doyle, J. 1980. Non-Monotonic Logic I. Artif. Intell., 13(1–2): 41–72. Moore, R. C. 1985. Semantical Considerations on Nonmonotonic Logic. Artif. Intell., 25(1): 75–94. Reinfrank, M.; Dressler, O.; and Brewka, G. 1989. On the Relation Between Truth Maintenance and Autoepistemic Logic. In Sridharan, N. S., ed., Proceedings of the 11th International Joint Conference on Artificial Intelligence. Detroit, MI, USA, August 1989, 1206–1212. Morgan Kaufmann. Reiter, R. 1980. A Logic for Default Reasoning. Artif. Intell., 13(1–2): 81–132. Rosati, R. 2006. Multi-modal nonmonotonic logics of minimal knowledge. Ann. Math. Artif. Intell., 48(3-4): 169–185.

Schwarz, G. 1992. Minimal Model Semantics for Nonmonotonic Modal Logics. In Proceedings of the Seventh Annual Symposium on Logic in Computer Science (LICS ’92), Santa Cruz, California, USA, June 22–25, 1992, 34– 43. IEEE Computer Society. Schwarz, G.; and Truszczy´nski, M. 1993. Nonmonotonic Reasoning is Sometimes Simpler. In Gottlob, G.; Leitsch, A.; and Mundici, D., eds., Computational Logic and Proof Theory, Third Kurt G¨odel Colloquium, KGC’93, Brno, Czech Republic, August 24–27, 1993, Proceedings, volume 713 of Lecture Notes in Computer Science, 313– 324. Springer. Schwarz, G.; and Truszczy´nski, M. 1994. Minimal Knowledge Problem: A New Approach. Artif. Intell., 67(1): 113– 141. Segerberg, K. K. 1971. An Essay in Classical Modal Logic. Ph.D. thesis, Stanford University, Department of Philosophy. Shvarts, G. F. 1990. Autoepistemic Modal Logics. In Parikh, R., ed., Proceedings of the 3rd Conference on Theoretical Aspects of Reasoning about Knowledge, Pacific Grove, CA, USA, March 1990, 97–109. Morgan Kaufmann. Strass, H. 2013. Approximating operators and semantics for abstract dialectical frameworks. Artif. Intell., 205: 39–70. Teede, H.; Deeks, A.; and Moran, L. 2010. Polycystic ovary syndrome: a complex condition with psychological, reproductive and metabolic manifestations that impacts on health across the lifespan. BMC Medicine, 8: 41. Published online 2010-06-30. Truszczy´nski, M. 2007. The Modal Logic S4F, the Default Logic, and the Logic Here-and-There. In Proceedings of the Twenty-Second AAAI Conference on Artificial Intelligence, July 22–26, 2007, Vancouver, British Columbia, Canada, 508–514. AAAI Press.

19134
