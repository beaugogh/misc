---
title: "Can You Tell the Difference? Contrastive Explanations for ABox Entailments"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38993
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38993/42955
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Can You Tell the Difference? Contrastive Explanations for ABox Entailments

<!-- Page 1 -->

Can You Tell the Difference? Contrastive Explanations for ABox Entailments

Patrick Koopmann1, Yasir Mahmood2, Axel-Cyrille Ngonga Ngomo2, Balram Tiwari2

1Knowledge in Artificial Intelligence, Vrije Universiteit Amsterdam, The Netherlands 2Data Science Group, Heinz Nixdorf Institute, Paderborn University, Germany p.k.koopmann@vu.nl, {yasir.mahmood, axel.ngonga, balram.tiwari}@uni-paderborn.de,

## Abstract

We introduce the notion of contrastive ABox explanations to answer questions of the type “Why is a an instance of C, but b is not?”. While there are various approaches for explaining positive entailments (why is C(a) entailed by the knowledge base) as well as missing entailments (why is C(b) not entailed) in isolation, contrastive explanations consider both at the same time, which allows them to focus on the relevant commonalities and differences between a and b. We develop an appropriate notion of contrastive explanations for the special case of ABox reasoning with description logic ontologies, and analyze the computational complexity for different variants under different optimality criteria, considering lightweight as well as more expressive description logics. We implemented a first method for computing one variant of contrastive explanations, and evaluated it on generated problems for realistic knowledge bases.

Code — https://doi.org/10.5281/zenodo.17603219 Extended version — https://arxiv.org/abs/2511.11281

## Introduction

A key advantage of knowledge representation systems is that they enable transparent and explainable decision-making. For example, with an ontology formalized in a description logic (DL) (Baader et al. 2017; Hitzler, Kr¨otzsch, and Rudolph 2010) we can infer implicit information from data (then called an ABox) through logical reasoning, and all inferences are based on explicit statements in the ontology and data. However, due to the expressive power of DLs and the complexity of realistic ontologies, inferences obtained through reasoning may not always be immediately understandable. Consequently, in recent years, significant attention has been devoted to explaining why or why not something is entailed by a DL knowledge base (KB). The why question is typically answered through justifications (Schlobach, Cornet et al. 2003; Horridge 2011). For a KB K (consisting of ontology and ABox statements) and an entailed axiom α, a justification is a subset minimal J ⊆K such that J |= α. Other techniques for explaining why questions include proofs (Alrabbaa et al. 2022b) and Craig interpolants (Schlobach 2004). To answer a why not question,

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

we can use abductive reasoning to determine what is missing in K to derive α (Elsenbroich, Kutz, and Sattler 2006; Peirce 1878). Research in this area for DLs encompasses ABox abduction (Del-Pinto and Schmidt 2019; Koopmann 2021), TBox abduction (Wei-Kleiner, Dragisic, and Lambrix 2014; Du, Wan, and Ma 2017; Haifani et al. 2022), KB abduction (Elsenbroich, Kutz, and Sattler 2006; Koopmann et al. 2020) and concept abduction (Bienvenu 2008), depending on the type of entailment to be explained.

If we query a KB for a set of objects, we may wonder why some object occurs in the answer but another does not. In this context, addressing the why and why not questions jointly can provide more clarity than considering them in isolation. To illustrate this, consider a simplified KB for a hiring process that determines which candidates are considered for a job interview. The KB uses a TBox with axioms

(a) Qualified ⊓∃publishedAt.Journal ⊑Interviewed,

(b) ∃leads.Group ⊔∃hasFunding.⊤⊑Qualified, (c) PostDoc ⊓∃leads.Group ⊑⊥ stating that (a) someone who is qualified and has published at a journal gets interviewed, (b) someone who leads a group or has funding is qualified and (c) postdocs cannot lead groups. Further, we have an ABox with assertions

(1) publishedAt(alice, aij), (2) publishedAt(bob, aaai), (3) Journal(aij), (4) leads(alice, kr), (5) Group(kr), (6) hasFunding(alice, nsf), (7) PostDoc(bob)

stating that (1) Alice published at AIJ, (2) Bob published at AAAI, (3) AIJ is a journal, (4–5) Alice leads the group KR, and (6) receives funding from the NSF, and (7) Bob is a Postdoc. This knowledge base entails Interviewed(alice), but not Interviewed(bob). We can explain why Alice was interviewed with an ABox justification, e.g. {(1), (3), (4), (5)} (“She published at the journal AIJ and leads the KR group”). To explain why Bob is not interviewed, we may use ABox abduction and obtain an answer with a fresh individual e:

{ Journal(aaai), hasFunding(bob, e) }

(“If AAAI was a journal, and Bob received funding, he would have been interviewed.”) For the question “Why was Alice interviewed, but not Bob?”, those explanations are not

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19189

<!-- Page 2 -->

ideal, since they consider different reasons for being qualified (funding vs. leading a group). A better contrastive explanation would be: “Alice’s publication is at a journal and Bob’s is not, and only Alice receives funding.”

Formally, a contrastive explanation problem consists of a concept (Interviewed), a fact individual that is an instance of the concept (alice), and a foil individual that is not an instance (bob). Such contrastive ABox explanation problems are also motivated in the context of concept learning (Lehmann and Hitzler 2010; Funk et al. 2019; Heindorf et al. 2022), where the aim is to learn a concept from positive and negative examples. Contrastive explanations allow to explain the learned concepts in the light of a positive and a negative example.

The notion of contrastive explanations appears first in the work of Lipton (1990). The main theme of Lipton’s work is to express an inquirer’s preference or reflect their demand regarding the context in which an explanation is requested (e.g., explain why Bob was not interviewed in the context of Alice, who was interviewed). Contrastive explanations have since been considered for answer set programming (Eiter, Geibinger, and Oetsch 2023) with aim of explaining why some atoms are in an answer set instead of others. The idea has also been used to explain classification results of machine learning models (Dhurandhar et al. 2018; Ignatiev et al. 2020; Stepin et al. 2021; Miller 2021; Marques-Silva and Ignatiev 2022). A related concept are counter-factual explanations used in machine learning (Verma, Dickerson, and Hines 2020; Dandl et al. 2020). What these approaches have in common is that they look at similarities and differences at the same time, and use syntactic patterns to highlight the differences. We use a similar idea in the context of ABox reasoning by using ABox patterns which are instantiated differently for the fact and the foil.

Contributions Our notion of contrastive ABox explanations (CEs) is quite general, and even allows for contradictions with the KB. We distinguish between a syntactic and a semantic version, consider different optimality criteria and analyze them theoretically for different DLs ranging from light-weight EL to the more expressive ALCI (see Table 1 for an overview). Our contributions are three fold:

1. We introduce contrastive ABox explanations along with several variants and optimality criteria. 2. We characterize the complexity for various reasoning problems spanning five dimensions: variants, preference measures, types of optimality, DLs, and concept types. 3. We implemented a first practical method and evaluated it on realistic ontologies.

Description Logics

We recall the relevant DLs (Baader et al. 2017). Let NI, NC, and NR denote countably infinite, mutually disjoint sets of individual, concept and role names, respectively. ALCI concepts are concept names or built following the syntax rules in Table 2, where R stands for a role name r ∈NR or its inverse r−. We define further concepts as syntactic optimality fresh ind. EL⊥ ALC, ALCI ⊆/ ≤ ⊆/ ≤ diff-min ≤PT11 / CONP-cT12 EXPTIME-cT11,T12 conf-min yes EXPTIME-cT17 CONEXPTIME-cT17 no CONP-cT18 EXPTIME-cT18 com-max open /CONP-cT19 EXPTIME-cT19

**Table 1.** Complexity results for verifying minimality of CEs.

Construct Syntax Semantics

Conjunction C ⊓D CI ∩DI

Existential restriction ∃R.C {x | ∃y ∈CI, ⟨x, y⟩∈RI} Negation ¬C ∆I \ CI

**Table 2.** Syntax and semantics for ALCI concepts.

sugar: top ⊤= A ⊔¬A, bottom ⊥= A ⊓¬A, disjunction C ⊔D = ¬(¬C ⊓¬D) and value restriction ∀r.C = ¬∃r.¬C. An concept without inverse roles is in ALC, if it furthermore only uses ⊤, ⊓, ∃and ⊥it is in EL⊥, and without ⊥it is in EL.

A general concept inclusion (GCI) is an expression of the form C ⊑D for concepts C, D. A TBox is a finite set of GCIs. An assertion is an expression of the form A(a) (concept assertion) or r(a, b) (role assertion), where a, b ∈NI, A ∈NC and r ∈NR. An ABox is a finite set of assertions. A KB is a tuple ⟨T, A⟩of a TBox T and an ABox A, treated as T ∪A. GCIs and assertions are called axioms. A TBox/KB is in ALCI/ALC/EL⊥/EL if all concepts in it are.

The semantics of ALCI is defined in terms of interpretations. An interpretation I is a tuple I = (∆I, ·I), where ∆I is a non-empty set called the domain of I, and ·I is the interpretation function that maps every individual name a ∈NI to an element aI ∈∆I, every concept name C ∈NC to a set CI ⊆∆I, and every role name r ∈NR to a binary relation rI ⊆∆I × ∆I. The interpretation function is extended to inverse roles using (r−)I = {⟨x, y⟩| ⟨y, x⟩∈rI} and to concepts following Table 2.

Let C ⊑D be a GCI and I be an interpretation. Then, I satisfies C ⊑D (denoted by I |= C ⊑D), if CI ⊆DI. Similarly, I satisfies a concept assertion A(a) if aI ∈AI and a role assertion r(a, b) if ⟨aI, bI⟩∈rI. I is a model of K (I |= K), if I satisfies every axiom in K. Finally, K entails α (K |= α) if I |= α for every model I of K. If K |= C(a), we call a an instance of C.

Contrastive Explanations We are interested in contrastive ABox explanation problems (CPs), which are formally defined as tuples P = ⟨K, C, a, b⟩ consisting of a KB K, a concept C and two individual names a, b, s.t. K |= C(a) and K̸ |= C(b). Intuitively, a CP reads as “Why is a an instance of C and b is not?”. If K and C are expressed in a DL L, we call P an L CP. We call a (or more generally C(a)) the fact and b (C(b)) the foil of the CP. Note that, because K̸ |= C(b), K is always consistent.

Building upon the framework of Lipton (1990), we aim

19190

<!-- Page 3 -->

to contrast a and b by highlighting the differences between the assertions that support C(a) and the missing assertions that would support C(b). Since different individuals may be related to a than to b, we abstract away from concrete individual names and instead use ABox patterns. An ABox pattern is a set q(⃗x) of assertions that uses variables from⃗ x instead of individual names. Given a vector⃗c of individual names with the same length as⃗x, q(⃗c) then denotes the assertions obtained after replacing variables following xi 7→ci. We want to highlight the difference between a and b using an ABox pattern qdiff(⃗x), paired with two vectors⃗c and⃗d such that qdiff(⃗c) is entailed by the KB, and adding qdiff(⃗d) would entail C(b). In our example, qdiff(x, y, z) = {Journal(y), hasFunding(x, z)} would be such a pattern, where for the fact alice we have⃗c = ⟨alice, aij, nsf⟩, and for the foil bob we could use ⟨bob, aaai, e⟩, where e is fresh.

To fully explain the entailment, we also need to include other facts that are relevant to the entailment, and which fact and foil have in common. In our example, the explanation only makes sense together with the commonality qcom(x, y, z) = {publishedAt(x, y)}. Specifically, our contrastive explanations use ABox patterns q(⃗x) = qcom(⃗x) ∪ qdiff(⃗x), with qcom(⃗x) stating what holds for both instantiations, and qdiff(⃗x) what holds only for the fact. To avoid irrelevant assertions in q(⃗x), we furthermore require that q(⃗c) is an ABox justification in the classical sense.

A final aspect regards how to deal with contradictions. Assume that in our example, instead of Axiom (b), we used (b′) ∃leads.Group ⊑Qualified. Most notions of abduction require the hypothesis to be consistent with the KB, which in the present case, due to Axiom (c), is impossible if we want to entail Interviewed(bob). For the present example, we might however still want to provide an explanation, for instance: “If AAAI was a journal and Bob lead the KR group, he would have been interviewed, but he cannot lead a group since he is a postdoc”. This results in the following components in the contrastive explanation:

q′ com = { publishedAt(x, y), Group(z) }, q′ diff = { Journal(y), leads(x, z) },⃗ c′ = ⟨alice, aij, kr⟩,⃗ d′ = {bob, aaai, kr} To point out the issue with this explanation, we add a final component, the conflict set C, which in this case would be {PostDoc(bob)}. Removing conflicts from the KB results in an alternative scenario consistent with the proposed explanation. This aligns with what are commonly called counterfactual accounts (Eiter, Geibinger, and Oetsch 2023). Intuitively, we would want to avoid conflicts if possible, but we will see later that this is not always desirable.

We can now formalise our new notion of explanations. Definition 1. Let P = ⟨K, C, a, b⟩be a CP where K = ⟨T, A⟩. A solution to P (the contrastive ABox explanation/CE) is a tuple

⟨qcom(⃗x), qdiff(⃗x),⃗c,⃗d, C⟩ of ABox patterns qcom(⃗x), qdiff(⃗x), vectors⃗c and⃗d of individual names, and a set C of assertions, which for q(⃗x) = qcom(⃗x) ∪qdiff(⃗x) satisfies the following conditions:

C1 T, q(⃗c) |= C(a) and T, q(⃗d) |= C(b), C2 K |= q(⃗c), C3 K |= qcom(⃗d), C4 q(⃗c) is a ⊆-minimal set satisfying C1+C2, C5 C ⊆A is ⊆-minimal such that T, (A \ C) ∪q(⃗d)̸ |= ⊥.

We call⃗c the fact evidence and⃗d the foil evidence. The patterns qcom(⃗x) and qdiff(⃗x) will be called commonality and difference. Intuitively, q(⃗x) describes a pattern that is responsible for a being an instance of C, with qcom(⃗x) describing what a and b have in common, and qdiff(⃗x) what b is lacking. By instantiating⃗x with⃗c we obtain a set of entailed assertions that entail C(a) (C1 and C2), and by instantiating it with⃗d, we obtain a set of assertions that entails C(b) (C1), where qcom(⃗d) is already provided by the present ABox (C3), and qdiff(⃗d) is missing. Since qdiff(⃗d) can be inconsistent with the KB, C presents the conflicts and (A \ C) ∪q(⃗d) depicts an alternative consistent scenario in which C(b) is entailed (C5). To avoid unrelated assertions in q or C, we require them to be minimal (C4 and C5). Example 2. For our example, the CP is ⟨K, Interviewed, alice, bob⟩. A CE for this CP is

E1 = ⟨qcom(x, y, z), qdiff(x, y, z),⃗c,⃗d, ∅⟩, where⃗c = ⟨alice, aij, nsf⟩,⃗d = ⟨bob, aaai, e⟩, qcom(x, y, z) ={ publishedAt(x, y) }, and qdiff(x, y, z) ={ Journal(y), hasFunding(x, z) }.

Another CE would be

E2 = ⟨q′ com, q′ diff,⃗c′,⃗d′, {PostDoc(bob)}⟩, with q′ com and q′ diff,⃗c′ and⃗d′ as described above. ◁

Syntactic and Semantic CEs In the example, our definition also allows for the following trivial CE that has limited explanatory value:

Et = ⟨∅, {Interviewed(x)}, ⟨alice⟩, ⟨bob⟩, ∅⟩.

A natural restriction to avoid this are syntactic CEs: Definition 3 (Syntactic and Semantic CEs). Let P = ⟨K, C, a, b⟩be a CP where K = ⟨T, A⟩. A CE

E = ⟨qcom(⃗x), qdiff(⃗x),⃗c,⃗d, C⟩ for P is called syntactic if qcom(⃗c), qdiff(⃗c), qcom(⃗d) ⊆A, and otherwise semantic.

Syntactic explanations can only refer to what is explicit in the ABox. Semantic explanations can additionally refer to implicit information that is entailed. Example 4. Consider the KB K = ⟨T, A⟩with

T ={ Prof ⊑Qualified, Qualified ⊓Nominee ⊑Offered } A ={ Prof(alice), Nominee(alice), Qualified(bob) }

A syntactic explanation for ⟨K, Offered, a, b⟩is

E3 = ⟨∅, {Prof(x), Nominee(x)}, ⟨alice⟩, ⟨bob⟩, ∅⟩.

19191

<!-- Page 4 -->

A semantic explanation can highlight the commonality:

E4 = ⟨{Qualified(x)}, {Nominee(x)}, ⟨alice⟩, ⟨bob⟩, ∅⟩ and thus give a more precise explanation for why Bob was not offered the job. (He didn’t need to be a professor.) ◁

If the CP contains a concept name as concept, a semantic explanation can always be obtained by simply using that concept as difference, which is why this case is more interesting for complex concepts. Moreover, we can reduce semantic CEs to syntactic ones:

Lemma 5. Let P = ⟨⟨T, A⟩, C, a, b⟩be an L CP. Then, one can compute in polynomial time, with access to an oracle that decides entailment for L, an ABox Ae such that every semantic CE for P is a syntactic CE for P ′ = ⟨⟨T, Ae⟩, C, a, b⟩and vice versa.

Proof. We simply need to add all entailed assertions of the form A(a)/r(a, b) where A, r, a and b occur in the input.

Because of Lemma 5, we focus on syntactic CEs for most of the paper. Furthermore, some reasoning problems with semantic CEs are trivial for CPs involving concept names but intractable when complex concepts are considered.

Optimality Criteria The minimality required in C4 and C5 is necessary to avoid unrelated assertions in the CE. Even with these restrictions in place, there can be many CEs for a given CP. The idea of CEs is to choose the ABox pattern so that the difference is as small as possible, and the commonality as large as possible. Also, while we allow for conflicts, having less seems intuitively better. There are therefore different components one may want to optimize, and optimization may be done locally (wrt. the subset relation) or globally (wrt. cardinality).

Definition 6 (Preferred CEs). Let P be a CP and E = ⟨qcom(⃗x), qdiff(⃗x),⃗c,⃗d, C⟩a CE for P. Then,

• E is difference-minimal if no explanation E′ has difference q′ diff(⃗x′) and foil evidence⃗d′, s.t. q′ diff(⃗d′) ⊂qdiff(⃗d). • E is conflict-minimal if there is no CE E′ with a conflict set C′ ⊂C. • E is commonality-maximal if no CE E′ has commonality q′ com(⃗x′) and foil evidence⃗d′, s.t. qcom(⃗d) ⊂q′ com(⃗d′).

We define each of the aforementioned optimality also w.r.t. the cardinality of given sets.

Minimizing differences aligns with the general aim of CEs—the smaller the difference, the easier to understand the explanation. Minimizing conflicts allows to deprioritize farfetched explanations that contradict much of what is known about the foil—if possible, we would want to provide a CE without conflicts. From a practical viewpoint, difference minimality allows the smallest factual change and conflict minimality limits CEs whose difference conflicts with the known data about foil. Commonality-maximality is similarly motivated, and allows to force the CE to be even more focussed. With commonality-maximality, we obtain interesting semantic CEs even when the concept in the CP is a concept name: in Example 4, both E4 and the trivial CE using qdiff = {Offered(x)} are difference-minimal, but E4 is also commonality-maximal and explains the CP better.

In Example 2, E1 is conflict-minimal and E2 is commonality-maximal, whereas both are differenceminimal. The trivial Et is conflict- and difference-minimal, but not commonality-maximal.

Decision Problems For any CP, we can always construct an arbitrary CE based on an ABox justification for the fact, where for the foil evidence, we simply replace a by b. Finding CEs that are also good wrt. our optimality criteria is less trivial. As usual, it is more convenient to look at decision problems rather than at the computation problem, in particular at the verification problem: Given a CP P with CE E, is E optimal wrt. a given criterion? Table 1 gives the complexity for these problems for different DLs. The global versions reduce to bounded versions of the existence problem: is there an E with a conflict/difference/commonality that has at most/least n elements? EXPTIME-hardness for ALC follows in all cases by a reduction to entailment (see full version). We discuss the other results in the following sections.

Difference-Minimal Explanations The challenge in computing and verifying differenceminimal CEs is that we cannot fix the other components: it is possible that the difference can only be made smaller by completely changing the other components. To deal with this, we define a maximal structure that intuitively contains all possible CEs, on which we then minimize the different components one after the other, starting with the difference. What it means for a structure to “contain” a CE is captured formally by the following definition. We call ⟨qcom(⃗x), qdiff(⃗x),⃗c,⃗d, C⟩a candidate CE if it satisfies Definition 1 except for C4 and C5.

Definition 7. Let Ep = ⟨pcom(⃗x), pdiff(⃗x),⃗cp,⃗dp, Cp⟩and Eq = ⟨qcom(⃗y), qdiff(⃗y),⃗cq,⃗dq, Cq⟩be two candidate CEs for a CP P = ⟨K, C, a, b⟩. A homomorphism from Ep to Eq is a mapping σ:⃗x →⃗y that ensures pcom(σ(⃗x)) ⊆qcom(⃗y) and pdiff(σ(⃗x)) ⊆qdiff(⃗y). We say that Ep embeds into Eq if there is such a homomorphism and additionally Cp ⊆Cq.

Fix a CP P = ⟨K, C, a, b⟩. We define the CE superstructure Em = ⟨qcom(⃗xm), qdiff(⃗xm),⃗cm,⃗dm, A⟩for P as follows:

•⃗xm contains one variable xa′,b′ for every ⟨a′, b′⟩∈ NI(A) × NI(A), •⃗cm contains a′ for every xa′,b′ in⃗x,

•⃗dm contains b′ for every xa′,b′ in⃗x, • qcom(⃗xm) = {A(xa′,b′) | A(a′), A(b′) ∈ A} ∪{r(xa0,b0, xa1,b1) | r(a0, a1), r(b0, b1) ∈A}, • qdiff(⃗xm) = {A(xa′,b′) | A(a′) ∈A, b′ ∈NI(A), A(b′)̸ ∈A} ∪{r(xa0,b0, xa1,b1) | r(a0, a1) ∈A, b0, b1 ∈NI(A), r(b0, b1)̸ ∈A} We set qm = qcom ∪qdiff. The variables⃗xm contain all possible combinations of mapping to an individual for the foil and for the fact, which is why they correspond to pairs of

19192

<!-- Page 5 -->

individual names. qcom and qdiff are then constructed based on the set of all assertions we can build over these variables. Em indeed captures all syntactic CEs for P that are defined over the signature of the input. Lemma 8. Every syntactic CE for P without fresh individual names embeds into Em.

Em is polynomial in size, and is almost a CE, modulo the minimality of q(⃗c) (C4) and of Cm (C5). Moreover, to satisfy C5, we also need qm(⃗dm) to be consistent with T, which may not be the case. To obtain a differenceminimal CE, we need to remove elements from qm to make T, qm(⃗dm) consistent and q2(⃗dm) subset-minimal without violating T, qm(⃗dm) |= C(b). The following lemma states how to safely remove elements from qm(⃗dm). For⃗x ⊆⃗xm, denote by qm|⃗x(⃗xm) the restriction of qm(⃗xm) to atoms that only use variables from⃗x. Lemma 9. Let⃗x ⊆⃗xm be s.t 1) xa,b ∈⃗x, and 2) for every xa′,b′ in⃗xm, we have some xa′′,b′′ ∈⃗x with a′ = a′′. Then, K, qdiff|⃗x(⃗dm) |= C(b).

Lemma 9 tells us which atoms we should keep if we want to make sure the foil remains entailed. The following lemma tells us how to make qm(⃗dm) consistent with T: Lemma 10. Let⃗x ⊆⃗xm be s.t. for every xa1,b1, xa2,b2 ∈⃗x, a1̸ = a2 implies b1̸ = b2. Then, T, qm|⃗x(⃗dm)̸ |= ⊥.

Importantly, the conditions in Lemma 9 and 10 are compatible: we can always find a vector⃗x that is safe in the sense that it satisfies the conditions in both lemmas, and thus ensures both consistency with T and entailment of C(b). This can be used as follows to compute difference-minimal CEs, starting from the super-structure Em.

P1 Obtain a query q(0) = q(0)

com ∪q(0)

diff from qm by remov- ing atoms until T, q(0)(⃗dm)̸ |= ⊥. By doing so, ensure that for some safe vector⃗x, we have qm|⃗x ⊆q(0). By Lemma 9, we then also have K, q(0)

diff (⃗dm) |= C(b).

P2 Compute a minimal subset qdiff(⃗xm) of q(0)

diff (⃗xm) s.t.

T, q(0)

com(⃗dm) ∪qdiff(⃗dm) |= C(b). This can be done in polynomial time by checking each axiom in turn. P3 To satisfy C4, compute a minimal subset qcom(⃗xm) of q(0)

com(⃗xm) s.t. T, qcom(⃗cm) ∪qdiff(⃗cm) |= C(a). This also takes polynomial time by checking each axiom in turn. P4 To satisfy C5, minimize Cm in the same way. We obtain the following theorem. Theorem 11. For any DL L-CPs, given an oracle that decides entailment in L, we can 1) compute a differenceminimal syntactic CE, and 2) decide difference-minimality of a given syntactic CE in polynomial time.

To see why 2) holds, let E be a syntactic CE. We may assume that E contains no fresh individuals, since we can always add occurrences of individuals to the KB in a way that does not affect relevant entailments. By Lemma 8, E then embeds in Em. We now apply P1 in the above procedure with the additional requirement that the pattern from

E is also contained in q(0), and in P2, we try to construct a subset of the difference of E.

This establishes our results in Table 1 for local difference minimality. When minimizing the difference globally, we lose tractability, Indeed, it is NP-complete to decide whether a CE exists with the cardinality of the difference bounded by some n ∈N. This allows us to prove the following theorem.

Theorem 12. Deciding whether a given syntactic or semantic CE for a given CP is difference-minimal w.r.t cardinality is CONP-complete for EL and EL⊥, and EXPTIMEcomplete for ALC.

Conflict-Minimal Explanations

It seems natural to favor explanations with an empty or minimal conflict set. Unfortunately, it turns out that this makes computing CEs significantly harder, and may lead to explanations that are overall much more complex. The reason is that avoiding conflicts may require fresh individuals in the foil evidence:

Example 13. Consider P = ⟨⟨T, A⟩, C, a, b⟩with

T ={ ∃r.∃r.A ⊑C, B ⊑¬A ⊓∀r.¬A }, A ={ A(a), r(a, a), B(b) }

A conflict-free syntactic CE for P is

⟨∅, { r(x, y), r(y, z), A(z) }, ⟨a, a, a⟩, ⟨b, c, a⟩, ∅⟩

We need the fresh individual c since b cannot satisfy A nor have a as successor without creating a conflict. ◁

Indeed, we may even need exponentially many of such individual names. To show this, we reduce a problem to conflict-minimality that has been studied under the names instance query emptiness (Baader et al. 2016) and flat signature-based ABox abduction (Koopmann 2021). We reduce from the abduction problem as it simplifies transferring size bounds.

Definition 14. A signature-based (flat) ABox abduction problem is a tuple ⟨K, α, Σ⟩of a KB K, an axiom α (the observation) and a set Σ of concept and role names. A hypothesis for this problem is a set H of assertions that uses only names from Σ, and for which K ∪H̸ |= ⊥and K ∪H |= α.

Lemma 15. For L ∈ {EL⊥, ALC, ALCI}, let A = ⟨T, C(b), Σ⟩be a signature-based ABox abduction problem with an L TBox T. Then, one can construct in polynomial time an L-CP s.t. from every syntactic CE with empty conflict set, one can construct in polynomial time a subsetminimal hypothesis for A and vice versa.

Proof sketch. We give the idea for ALCI while the other reductions can be found in our technical report (Koopmann et al. 2025). We construct a new TBox T ′ that contains for every CI C ⊑D ∈T the CI C ⊑D ⊔A⊥, where A⊥is fresh. In addition, T ′ contains ∃r.A⊥⊑A⊥and A⊥⊑∀r.A⊥for every role r occurring in T, and the axiom B⊥⊓A⊥⊑⊥, where B⊥is also fresh. For any ABox A′ not containing any of the fresh names, (I) T ′, A′̸ |= ⊥and

19193

<!-- Page 6 -->

(II) T, A′ |= ⊥iff for some individual name b, T ′ ∪A′ |= A⊥(b). We further define

A ={A(a), r(a, a) | A ∈NC ∩Σ, r ∈NR ∩Σ}

∪{A⊥(a), B⊥(b)}.

The CP is now defined as P = ⟨⟨T ′, A⟩, C ⊔A⊥, a, b⟩.

Lemma 15 also allows us to reduce the abduction problem to the problem of computing conflict-minimal syntactic CEs. The reason is that it is easy to extend a given CP ⟨K, C, a, b⟩so that it has a syntactic CE with a non-empty conflict set: Simply add to K the following axioms, where A∗and B∗are fresh: A∗(a), B∗(b), A∗⊑C, A∗⊓B∗⊑⊥. Now a syntactic CE can be obtained by setting qcom(⃗x) = ∅, qdiff(⃗x) = {A∗(x)} and C = {B∗(b)}. Consequently, we can decide the existence of a hypothesis for a given abduction problem by computing a conflict-minimal CE and checking whether its conflict set is empty. This now allows us to import a range of complexity results from (Koopmann 2021). To obtain matching upper bounds, we extend the construction of the CE super-structure to now work on possible types of individuals in the foil evidence. Fix a CE with difference qdiff and foil evidence⃗d. Let I be a model of K ∪qdiff(⃗d), and let S be the set of (sub-)concepts occurring in K and C. We assign to every d ∈∆I its type defined as tpI(d) = a if d = aI with a an individual that occurs in K or P, and otherwise as tpI(d) = {C ∈S | d ∈CI}. We can use the types for an arbitrary model I of the KB to bound the number of fresh individuals in any given CE without introducing new conflicts. The resulting CE contains a variable xc,t for every individual c occurring in A and type t occurring in the range of tpI. Together with the corresponding lower bound from the abduction problem, we obtain: Theorem 16. There exists a family of EL⊥-CPs in s.t. the size of their conflict-minimal syntactic CEs is exponential in the size of the CP. At the same time, every ALCI-CP has a subset and a cardinality conflict-minimal syntactic CE whose size is at most exponential in the size of the CP.

We can construct the set of possible types for a given CP using a type-elimination structure, giving us a set of possible tuples for the CE in deterministic exponential time. Based on this, we can modify our method for computing differenceminimal CEs to also construct conflict-minimal CEs. For ALC, using an oracle for entailment would yield membership in 2EXPTIME. To improve this, we observe that even in models for the constructed CP, the number of possible types is still exponentially bounded. Theorem 17. Deciding whether a given syntactic CE for a CP is (subset or cardinality) conflict-minimal, is

• EXPTIME-complete for EL⊥-CPs, • CONEXPTIME-complete for ALC- and ALCI-CPs, where the complexity only depends on the size of the CP.

A straight-forward solution to this exponential explosion is to bound the number of individuals or to disallow fresh individuals altogether. This immediately yields a CONP-upper bound for the verification, but cannot regain tractability.

Theorem 18. Deciding whether a given syntactic explanation without fresh individuals is (subset or cardinality) conflict-minimal is CONP-complete for EL⊥, but EXP- TIME-complete for ALC and ALCI.

Commonality-Maximal Explanations

As illustrated in the extreme by the case of semantic CPs with concept names as concept, sometimes minimizing differences and conflicts is not sufficient, and we want to maximize the commonality instead to obtain a more focussed CE. This gives us an idea on how close the foil can get to the fact. For EL, we prove that it is NP-complete to decide the existence of an explanation with commonality above a given threshold n ∈N. Proving the lower bound requires a different reduction as for Theorem 12.

Theorem 19. Deciding whether a given syntactic CE for a CP is commonality-maximal is CONP-complete for EL/EL⊥, but EXPTIME-complete for ALC/ALCI.

## Evaluation

of a First Prototype

To understand how to compute CEs in practice, we implemented a first prototype for one of the variants.Theorem 11 shows that difference-minimal syntactic contrastive explanations can be computed in polynomial time, with an oracle for deciding entailment, while the other criteria are not tractable. Semantic explanations can be reduced to syntactic ones by computing all entailed concept assertions (Lemma 5), which is a standard functionality of OWL reasoning systems. Based on these observations, we developed a prototype to compute difference-minimal syntactic CEs.

A Practical Method for Computing CEs

To make our method for computing difference-minimal CEs practical, we refine the definition of the super structure. Fix a CP P = ⟨⟨T, A⟩, C, a, b⟩. Our construction is now based on a subset A′ ⊆A, and a set I ⊆NI of individuals to be used for the foil. We define Em = ⟨qcom(⃗x), qdiff(⃗x),⃗cm,⃗dm, Cm⟩, where now

•⃗x contains a variable xc,d for every ⟨c, d⟩∈NI(A′) × I, •⃗cm uses c for every xc,d in⃗x,

•⃗dm uses d for every xc,d in⃗x, • qcom(⃗x) = {A(xc,d) | A(c) ∈A′, d ∈I, A(d) ∈A}∪ {r(xc,d, xc′,d′) | r(c, c′) ∈A′, d, d′ ∈I, r(d, d′) ∈A}, • qdiff(⃗x) = {A(xc,d) | A(c) ∈A′, d ∈I, A(d)̸ ∈A}∪ {r(xc,d, xc′,d′) | r(c, c′) ∈A′, d, d′ ∈I, r(d, d′)̸ ∈A}.

For A′ = A and I = NI(A), Em is identical to the maximal CE defined before, but too large. Instead, for A′ we compute the union of all justifications of C(a) with an optimized implementation. In I, we include individuals that are “sufficiently close” to the foil, as well as some fresh individuals, using Lemma 9 and 10 to ensure that I is sufficiently large. To apply P1–P4 efficiently, we modified the implementation of the justification algorithm presented in (Kalyanpur et al. 2007) to compute justifications with a fixed component:

19194

<!-- Page 7 -->

Corpus Signature Size Number of Individuals TBox size ABox size avg. med. range avg. med. range avg. med. range avg. med. range

EL⊥ 2,013 728 167 – 7,217 781 417 48 – 3,608 1,478 390 105 – 5,653 1,254 482 103 – 8,234 ALCI 1,764 606 54 – 7,355 490 185 0 – 5,473 1,603 498 94 – 5,286 1,207 494 101 – 9,284

**Table 3.** Some details about the two corpora.

Corpus #CPs Commonality Difference Conflict Fresh Individuals Duration (sec.) average range average range average range average range average range average range

EL⊥ 35.1 4 – 50 0.45 0 – 4 1.42 1 – 6 0.0 0 – 0 0.34 0 – 3 2.84 0.08 – 386.9 ALCI 34.7 1 – 50 0.34 0 – 7 1.29 1 – 5 0.36 0 – 9 0.25 0 – 5 8.81 0.06 – 493.6

**Table 4.** Results for the two corpora. “#CP” states the number of CPs answered (out of 50) within the timeout (10 mins).

.

Definition 20. Let K be a KB, K′ ⊆K and α an axiom s.t. K |= α. A justification for K |= α with fixed component K′ is a subset-minimal J ⊆(K \ K′) s.t. K′ ∪J |= α.

In each step, we compute such justifications where we fix the TBox and the components that are currently not modified, which allows to speed up the computation significantly.

Our implementation uses different optimizations for ALCI and for EL⊥. We implemented it in Java 8, using the OWL API 5.1.20 (Horridge and Bechhofer 2011), reasoning systems ELK (Kazakov, Kr¨otzsch, and Simancik 2014) and HERMIT (Glimm et al. 2014), as well as the explanation library EVEE-LIB 0.3 (Alrabbaa et al. 2022a), which helped us in computing unions of justifications for EL⊥.

Benchmark Ontologies. We used KBs from the OWL Reasoner Competition ORE 2015 (Parsia et al. 2017), namely from the tracks Materialization tracks for OWL DL and OWL EL, restricted respectively to ALCI and EL⊥. Those tracks focus on ABox reasoning, and contain KBs of varying shapes. Some KBs contained all entailed assertions, which limits their use for explanations. Therefore, we step-wisely removed from each KB all entailed assertions. KBs with more than 10,000 axioms were discared. The resulting corpora contained 46 (EL⊥) and 100 (ALCI) KBs (see Table 3).

CPs. For each KB in the corpus, we performed 5 runs and constructed 10 CPs for each run. For each CP, we generated a random EL concept C of maximum size 5 using a random walk on the ABox starting from a randomly selected fact individual a. For this, we also considered entailed assertions. For the foil, we selected a random individual b that is not an instance of C and shares at least one concept with a.

## Evaluation

## Results

Some of the KBs in our corpus had to be excluded: in the EL⊥/ALCI corpus, 13 were inconsistent, for 21/17 no problems could be generated under our constraints. Two more KBs from the ALCI corpus where removed because HERMIT threw an exception on those. Of the remaining KBs, 10/13 KBs did not allow to produce interesting CEs: for those KBs, every CE had an empty commonality and conflict, and exactly one axiom in the difference. The reason was the simple structure of the ABox, which simply allowed for no more contrasting entailments, e.g. because no role assertions were used. We exclude those KBs in the following evaluation, and focus on the remaining 14/67 ones.

## Experiments

were conducted on a server with 2× Intel Xeon E5-2630 v4 20 cores, 2.2GHz CPUs, along with 189 GB of available RAM running Debian 11 (Bullseye). The Java runtime environment was OpenJDK 11.0.28. The results are shown in Table 4. In general, the computed CEs tended to be simple, even though the concepts to be explained were of size up to 5. This can be explained with the simplicity of some ABoxes: if an individual has only one successor, even a complex concept of size 5 can only refer to those two individuals, and consequently the CP may use only one fact. Nonetheless, we see that every component of a CE is used, sometimes with several assertions, and also fresh individuals appear. We also see that conflicts are a relatively rare occasion, not happening at all in the EL⊥corpus, which may indicate that computing conflict-free CEs could still be feasible in practice. What our evaluation also shows is that our current prototype takes surprisingly long to compute the answers. Reasons include our approach for making q(⃗x) consistent, selection of individuals, and that our construction often results in very large super-structures. This shows potential for more dedicated methods in the future.

## Conclusion and Future Work

We introduced contrastive explanation problems and proposed CEs as a way to answer them. It turns out that minimizing difference is tractable and feasible in practice, while minimzing conflicts may lead to an exponential explosion. At the same time, conflicts do not seem to happen often for realistic ontologies. In the future we want to investigate dedicated algorithms for computing CEs more efficiently. We are also exploring a variant of CEs which use quantified variables in the fact and foil vectors. Moreover, one can address the counting and enumeration complexity for CEs. To conclude, we propose CEs as a tool to contrast positive and negative query answers in ontology mediated query answering.

19195

<!-- Page 8 -->

## Acknowledgments

We thank all anonymous reviewers for their valuable feedback. Research was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation), grant TRR 318/1 2021 – 438445824 and the Ministry of Culture and Science of North Rhine-Westphalia (MKW NRW) within projects WHALE (LFN 1-04) funded under the Lamarr Fellow Network programme and project SAIL, grant NW21-059D.

## References

Alrabbaa, C.; Borgwardt, S.; Friese, T.; Koopmann, P.; M´endez, J.; and Popovic, A. 2022a. On the Eve of True Explainability for OWL Ontologies: Description Logic Proofs with Evee and Evonne. In Arieli, O.; Homola, M.; Jung, J. C.; and Mugnier, M., eds., Proceedings of the 35th International Workshop on Description Logics (DL 2022) colocated with Federated Logic Conference (FLoC 2022), Haifa, Israel, August 7th to 10th, 2022, volume 3263 of CEUR Workshop Proceedings. CEUR-WS.org. Alrabbaa, C.; Borgwardt, S.; Koopmann, P.; and Kovtunova, A. 2022b. Explaining ontology-mediated query answers using proofs over universal models. In International Joint Conference on Rules and Reasoning, 167–182. Springer. Baader, F.; Bienvenu, M.; Lutz, C.; and Wolter, F. 2016. Query and Predicate Emptiness in Ontology-Based Data Access. J. Artif. Intell. Res., 56: 1–59. Baader, F.; Horrocks, I.; Lutz, C.; and Sattler, U. 2017. An Introduction to Description Logic. Cambridge University Press. ISBN 978-0-521-69542-8. Bienvenu, M. 2008. Complexity of Abduction in the EL Family of Lightweight Description Logics. In Brewka, G.; and Lang, J., eds., Principles of Knowledge Representation and Reasoning: Proceedings of the Eleventh International Conference, KR 2008, Sydney, Australia, September 16-19, 2008, 220–230. AAAI Press. Dandl, S.; Molnar, C.; Binder, M.; and Bischl, B. 2020. Multi-objective counterfactual explanations. In International conference on parallel problem solving from nature, 448–469. Springer. Del-Pinto, W.; and Schmidt, R. A. 2019. ABox Abduction via Forgetting in ALC. In The Thirty-Third AAAI Conference on Artificial Intelligence, AAAI 2019, The Thirty- First Innovative Applications of Artificial Intelligence Conference, IAAI 2019, The Ninth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2019, 2768– 2775. Dhurandhar, A.; Chen, P.-Y.; Luss, R.; Tu, C.-C.; Ting, P.; Shanmugam, K.; and Das, P. 2018. Explanations based on the missing: Towards contrastive explanations with pertinent negatives. Advances in neural information processing systems, 31. Du, J.; Wan, H.; and Ma, H. 2017. Practical TBox Abduction Based on Justification Patterns. In Proceedings of the Thirty- First AAAI Conference on Artificial Intelligence, February 4-9, 2017, San Francisco, California, USA, 1100–1106.

Eiter, T.; Geibinger, T.; and Oetsch, J. 2023. Contrastive Explanations for Answer-Set Programs. In European Conference on Logics in Artificial Intelligence, 73–89. Springer. Elsenbroich, C.; Kutz, O.; and Sattler, U. 2006. A case for abductive reasoning over ontologies. In Proceedings of the OWLED 2006 Workshop on OWL: Experiences and Directions, Athens, Georgia, USA, November 10-11, 2006, volume 216, 1–12. CEUR. Funk, M.; Jung, J. C.; Lutz, C.; Pulcini, H.; and Wolter, F. 2019. Learning Description Logic Concepts: When can Positive and Negative Examples be Separated? In Kraus, S., ed., Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, Macao, China, August 10-16, 2019, 1682–1688. ijcai.org. Glimm, B.; Horrocks, I.; Motik, B.; Stoilos, G.; and Wang, Z. 2014. HermiT: An OWL 2 Reasoner. J. Autom. Reason., 53(3): 245–269. Haifani, F.; Koopmann, P.; Tourret, S.; and Weidenbach, C. 2022. Connection-Minimal Abduction in EL via Translation to FOL. In Blanchette, J.; Kov´acs, L.; and Pattinson, D., eds., Automated Reasoning - 11th International Joint Conference, IJCAR 2022, volume 13385 of Lecture Notes in Computer Science, 188–207. Springer. Heindorf, S.; Bl¨ubaum, L.; D¨usterhus, N.; Werner, T.; Golani, V. N.; Demir, C.; and Ngomo, A. N. 2022. EvoLearner: Learning Description Logics with Evolutionary Algorithms. In Laforest, F.; Troncy, R.; Simperl, E.; Agarwal, D.; Gionis, A.; Herman, I.; and M´edini, L., eds., WWW ’22: The ACM Web Conference 2022, Virtual Event, Lyon, France, April 25 - 29, 2022, 818–828. ACM. Hitzler, P.; Kr¨otzsch, M.; and Rudolph, S. 2010. Foundations of Semantic Web Technologies. Chapman and Hall/CRC Press. ISBN 9781420090505. Horridge, M. 2011. Justification based explanation in ontologies. The University of Manchester (United Kingdom). Horridge, M.; and Bechhofer, S. 2011. The OWL API: A Java API for OWL ontologies. Semantic Web, 2(1): 11–21. Ignatiev, A.; Narodytska, N.; Asher, N.; and Marques-Silva, J. 2020. From Contrastive to Abductive Explanations and Back Again. In AIxIA 2020 - Advances in Artificial Intelligence: XIX Int. Conf. of the Italian Association for AI, volume 12414, 335–355. Springer. Kalyanpur, A.; Parsia, B.; Horridge, M.; and Sirin, E. 2007. Finding All Justifications of OWL DL Entailments. In Aberer, K.; Choi, K.; Noy, N. F.; Allemang, D.; Lee, K.; Nixon, L. J. B.; Golbeck, J.; Mika, P.; Maynard, D.; Mizoguchi, R.; Schreiber, G.; and Cudr´e-Mauroux, P., eds., The Semantic Web, 6th International Semantic Web Conference, 2nd Asian Semantic Web Conference, ISWC 2007 + ASWC 2007, Busan, Korea, November 11-15, 2007, volume 4825 of Lecture Notes in Computer Science, 267–280. Springer. Kazakov, Y.; Kr¨otzsch, M.; and Simancik, F. 2014. The Incredible ELK — From Polynomial Procedures to Efficient Reasoning with EL Ontologies. J. Autom. Reason., 53(1): 1–61. Koopmann, P. 2021. Signature-Based Abduction with Fresh Individuals and Complex Concepts for Description Logics.

19196

<!-- Page 9 -->

In Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI 2021, 1929–1935. Koopmann, P.; Del-Pinto, W.; Tourret, S.; and Schmidt, R. A. 2020. Signature-Based Abduction for Expressive Description Logics. In Calvanese, D.; Erdem, E.; and Thielscher, M., eds., Proceedings of the 17th International Conference on Principles of Knowledge Representation and Reasoning, KR 2020, Rhodes, Greece, September 12-18, 2020, 592–602. Koopmann, P.; Mahmood, Y.; Ngomo, A.-C. N.; and Tiwari, B. 2025. Can You Tell the Difference? Contrastive Explanations for ABox Entailments. arXiv:2511.11281. Lehmann, J.; and Hitzler, P. 2010. Concept learning in description logics using refinement operators. Mach. Learn., 78(1-2): 203–250. Lipton, P. 1990. Contrastive explanation. Royal Institute of Philosophy Supplements, 27: 247–266. Marques-Silva, J.; and Ignatiev, A. 2022. Delivering Trustworthy AI through Formal XAI. In Thirty-Sixth AAAI Conference on Artificial Intelligence, 12342–12350. AAAI Press. Miller, T. 2021. Contrastive explanation: a structural-model approach. The Knowledge Engineering Review, 36: e14. Parsia, B.; Matentzoglu, N.; Gonc¸alves, R. S.; Glimm, B.; and Steigmiller, A. 2017. The OWL Reasoner Evaluation (ORE) 2015 Competition Report. J. Autom. Reason., 59(4): 455–482. Peirce, C. 1878. Deduction, induction and hypothesis: Popular Science Monthly, v. 13. Schlobach, S. 2004. Explaining Subsumption by Optimal Interpolation. In Alferes, J. J.; and Leite, J. A., eds., Logics in Artificial Intelligence, 9th European Conference, JELIA 2004, Lisbon, Portugal, September 27-30, 2004, Proceedings, volume 3229 of Lecture Notes in Computer Science, 413–425. Springer. Schlobach, S.; Cornet, R.; et al. 2003. Non-standard reasoning services for the debugging of description logic terminologies. In Ijcai, volume 3, 355–362. Stepin, I.; Alonso, J. M.; Catala, A.; and Pereira-Fari˜na, M. 2021. A survey of contrastive and counterfactual explanation generation methods for explainable artificial intelligence. IEEE Access, 9: 11974–12001. Verma, S.; Dickerson, J.; and Hines, K. 2020. Counterfactual explanations for machine learning: A review. arXiv preprint arXiv:2010.10596, 2(1): 1. Wei-Kleiner, F.; Dragisic, Z.; and Lambrix, P. 2014. Abduction framework for repairing incomplete EL ontologies: Complexity results and algorithms. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 28.

19197
