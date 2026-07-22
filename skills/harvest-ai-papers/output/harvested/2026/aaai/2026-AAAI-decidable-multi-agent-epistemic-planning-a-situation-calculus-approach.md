---
title: "Decidable Multi-agent Epistemic Planning: A Situation Calculus Approach"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38979
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38979/42941
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Decidable Multi-agent Epistemic Planning: A Situation Calculus Approach

<!-- Page 1 -->

Decidable Multi-agent Epistemic Planning: A Situation Calculus Approach

Qihui Feng, Gerhard Lakemeyer

Knowledge-Based Systems Group, RWTH Aachen University, Germany

{feng, gerhard}@kbsg.rwth-aachen.de

## Abstract

Multi-agent epistemic planning (MEP) is the task of generating action sequences that achieve goals speciﬁed over both the physical world and agents’ mental states. It plays an important role in research domains such as game theory, computational economics, and cognitive science. While dynamic epistemic logic (DEL) provides an expressive framework for MEP, it requires complete, model-based speciﬁcations of the initial state and action effects, and suffers from undecidability due to the unbounded nesting of beliefs. In this work, we propose a modal variant of the situation calculus that captures much of the expressive power of the DEL approach. Inspired by the cognitive concept Theory of Mind (ToM), we introduce action theories with hierarchical structures, allowing agents to reason about other agents’ action theories up to bounded depths. We develop a regression method that reduces reasoning about future states to reasoning about the initial state. By preserving bounded-order ToM throughout the regression process, our approach ensures the decidability of the planning problem. Finally, we propose an algorithm to ﬁnd the optimal solution, namely, to ﬁnd the shortest action sequence that achieves the goal.

## Introduction

Multi-agent epistemic planning (MEP) refers to the task of generating action sequences to achieve goals formulated not only in terms of the world state but also the mental states of agents. Unlike classical planning, epistemic planning explicitly characterizes and tracks how knowledge and beliefs evolve through actions. This capability enables planning in nondeterministic, partially observable, and multi-agent domains, where agents may reason about others’ knowledge and beliefs. MEP plays important roles in applications such as games (De Giacomo et al. 2016), human-agent interaction (Baral et al. 2017), and cognitive science (Pietarinen 2003). Most existing approaches for MEP are based on Dynamic Epistemic Logic (DEL). In the DEL approach, both the epistemic states and actions (events) are represented using pointed Kripke models, and state transitions with respect to actions are computed through the product update, which integrates the epistemic model with the event model (Bolander and Andersen 2011). The DEL approach offers several

Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

advantages for modeling MEP: it provides high expressivity for representing epistemic concepts such as nested beliefs and common knowledge, and it allows capturing complex epistemic dynamics arising from diverse action types and effects. In addition, the product update offers a uniform mathematical method for computing how agents’ knowledge evolves in response to actions.

However, despite its expressiveness, the DEL approach faces several limitations. As a semantic approach, it requires a complete and explicit construction of both the initial model and the event model, which often demands expertise in modal logic. In complex domains, the automatic generation of these models is challenging. Moreover, it has been shown that MEP in DEL is undecidable, mainly due to the potential for unbounded growth of nested knowledge (Bolander and Andersen 2011). While decidable fragments exist, such as planning with propositional actions or pure epistemic actions (L¨owe, Pacuit, and Witzel 2011; Yu, Wen, and Liu 2013; Bolander, Jensen, and Schwarzentruber 2015), strong restrictions are imposed that limit the expressivity.

To address the drawbacks of the semantic-based DEL approach, alternative syntactic approaches have also been explored. (Aucher 2011, 2012) investigates epistemic planning using DEL-sequent calculus and projection. Unlike the DEL approach, these works do not explicitly consider action sequences but instead produce a formal speciﬁcation that the transition must fulﬁll. Situation Calculus (McCarthy and Hayes 1981; Reiter 2001), which is a ﬁrst-order logical framework originally designed for physical actions, is used for relevant tasks such as belief change or progression (Fang and Liu 2013; Fang, Liu, and Wen 2015). However, to express knowledge and beliefs in the original design of the situation calculus requires second-order quantiﬁcation, which makes it difﬁcult to design a general planner but still preserve decidability. Via a modal variant of the epistemic situation calculus, (Belle and Lakemeyer 2014) presents a regression framework for multi-agent scenarios, which reduces queries after actions to the initial state so that tools for theorem proving can be applied. However, their approach does not handle MEP directly, and also suffers from limited expressivity, as it can only represent actions with objective pre- and postconditions, and cannot express announcements or nondeterministic actions.

To further extend the prior works and overcome the re-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19064

<!-- Page 2 -->

striction on action theories, we investigate the cognitivescience concept Theory of Mind (ToM) - the cognitive mechanism by which one predicts other people’s actions by inferring their perceptions, beliefs, and desires (Ho, Saxe, and Cushman 2022). Higher-order ToM typically corresponds to more sophisticated cognitive and reasoning abilities, involving recursive mental-state attribution (Peloquin 2023). Inspired by the hierarchical structure of ToM, we propose a formalism of collective action theories, where each agent has an individual action theory that amounts to ToM of a certain order, and beliefs about other agents’ theories, which amount to lower-order ToMs. By preserving bounded-order ToM (BoToM) throughout the regression, our framework ensures the decidability of MEP represented within this formalism.

The rest of the paper is organized as follows. We begin by formalizing the logic for multi-agent epistemic reasoning in dynamic systems. Next, Section 3 introduces our hierarchical formalism for collective theories. We then discuss the various action types that can be represented within our framework. Subsequently, we present the regression approach in Section 5. Section 6 provides examples to demonstrate the expressiveness of our framework. In Section 7, we deﬁne MEP problems via logical entailment and prove their decidability. We propose an algorithm which solves MEPs and returns optimal solutions.

The Logic MS

We consider a propositional variant of the logic ESn(Belle and Lakemeyer 2014): Given ﬁnite sets of agents Ag, actions Ac and atomic propositions Ap, the logic MS(Ag, Ac, Ap) includes the following formulae:1 ϕ: = p | ¬ϕ | ϕ ∧ψ | Kiϕ | [a]ϕ | □ϕ, (1)

where p ∈Ap. Other connectives like ∨, →, ≡are used as the usual abbreviations. Kiϕ means “agent i knows/believes ϕ”,2 [a]ϕ is read as “ϕ holds after action a” and □ϕ means “ϕ holds after any sequence of actions”. For G ⊆Ag, we use EGϕ as the abbreviation of ∧i∈GKiϕ and Ek

Gϕ means EG(· · · (EGϕ)) with k nested EG. When G = Ag, we write Eϕ and Ekϕ. Note that ESn is a ﬁrst-order logic with a countably inﬁnite set of objects and actions. We restrict our language to a propositional fragment for decidable MEP. A ﬁrst-order extension is certainly possible, but we leave it for future work. In addition, we include two “predicates”:

• Poss(a): a is executable (in an agents’ mind); • I(a, a′): a′ is indistinguishable from a (for an agent).

Essentially, these predicates are interpreted as propositions in Ap, e.g., Poss(move) as poss move. Let Z denote the set of ﬁnite action sequences, i.e. Z = Ac∗. We use ⟨⟩to denote the empty one. A formula is bounded if it does not mention □, and it is static if it does not mention □or any [a]. We say a formula is objective if it mentions no K operators and a formula is subjective if every proposition occurs

1When the context is clear, we simply write MS. 2“Knowledge” and “belief” are used interchangeably.

in the scope of a K operator. A formula is i-objective if every occurrence of Ki is in the scope of a Kj where j̸ = i, and a formula is i-subjective if every occurrence of propositions or Kj for j̸ = i is in the scope of a Ki. In addition, we use ⊤and ⊥to represent tautologies and falsities. For z = a1 · · · am, we write [z]ϕ instead of [a1] · · · [am]ϕ. Executability of sequence Exec(z) is recursively deﬁned as

• Exec(⟨⟩):= ⊤; • For z = a · σ, Exec(z):= Poss(a) ∧[a]Exec(σ).

To evaluate the depth of a formula, we follow (Feng et al. 2025) and deﬁne:

Deﬁnition 1 (i-depth). For i ∈Ag, the i-depth of a formula α, written as dep[α, i], is recursively deﬁned as

• dep[p, i] = 0 for p ∈Ap; • dep[¬α, i] = dep[α, i]; • dep[α ∧β, i] = max(dep[α, i], dep[β, i]); • dep[[a]α, i] = dep[α, i] for a ∈Ac; • dep[□α, i] = dep[α, i]; • dep[Kiα, i] = max(max{dep[α, j] | j̸ = i} + 1, dep[α, i]); • dep[Kjα, i] = 0 for j̸ = i.

Intuitively, dep[α, i] measures the degree of nesting of agent i’s mental state. For example, a formula p∧KA¬KBp has A-depth 2 and B-depth 0, as it involves what A believes that B believes, but not the actual beliefs of B. The depth of a formula α is deﬁned as the maximal i-depth, i.e. dep[α] = maxi∈Ag dep[α, i].

The semantics of the logic involves several terms: world, structure, and epistemic state. Similar notions are in (Belle and Lakemeyer 2014, 2015; Feng et al. 2025). A world is deﬁned as a mapping w: Z →2Ap. We use W to denote the set of all worlds. Let |Ag| = n, for k ≥0, we inductively deﬁne the epistemic states and structures as follows:

• E0 = {{∅}} • Sk+1 = {(w, e1,... en−1) | w ∈W, ej ∈Ek for all j}

• Ek+1 = ℘(Sk+1), i.e. Ek+1 is the power set of Sk+1

We call sk ∈Sk a k-structure and ek ∈Ek a kstate. We call k the depth of sk and ek. Intuitively, a structure consists of what an agent considers possible about the world and about other agents’ beliefs. When the context is clear, we omit the superscript k. By a model, we mean a tuple (w, e1,... en) (also written as (w,⃗e)), where w is a world and ei is the state of agent i. Note the difference between structures and models: a structure consists of n −1 states of the same depth, while a model consists of n states whose depths can be different. For state ˆe and structure s = (w, e1,... en−1), we use s ∪i ˆe to denote the model obtained by inserting ˆe at the i-th position, i.e. (w, e1,... ei−1, ˆe, ei,... en−1). The satisfaction relation is deﬁned as follows:

• (w,⃗e) |= p iff p ∈w[⟨⟩] • (w,⃗e) |= ¬α iff it is not the case that (w,⃗e) |= α • (w,⃗e) |= α ∧β iff (w,⃗e) |= α and (w,⃗e) |= β • (w,⃗e) |= Kiα iff s ∪i ei |= α for all s ∈ei

19065

<!-- Page 3 -->

We introduce the following notions. Essentially, they extend the semantics of Poss and I to sequences:

Deﬁnition 2. We deﬁne Πw ⊆Z and ∼w⊆Z × Z as:

• ⟨⟩∈Πw. For z = σ · a, z ∈Πw iff σ ∈Πw and Poss(a) ∈w[σ]. • ⟨⟩∼w z iff z = ⟨⟩. For z = σ·a and z′ = σ′·a′, z ∼w z′ iff σ ∼w σ′ and I(a, a′) ∈w[σ′].

To characterize the situation after actions, we extend the world/state progression (Claßen 2013; Liu and Feng 2023) to multi-agent cases:

Deﬁnition 3. For w ∈W and z ∈Z, the progression of w wrt z, written as wz, is deﬁned as the world w′ such that for all z′ ∈Z, w[z·z′] = w′[z′]. For epistemic state e ∈Ek, the progression of e wrt z, written as ez, is deﬁned as follows:

• When k = 1, i.e. e is a state of depth 1, ez = {(wσ, {∅},... {∅}) | (w, {∅},... {∅}) ∈e, σ ∈Πw, z ∼w σ} • When k > 1, i.e. e is a state deeper than 1, ez = {(wσ, e′

1,σ,... e′ n−1,σ) | (w, e′

1,... e′ n−1) ∈e, σ ∈Πw and z ∼w σ} Where e′ j,σ is the progression of e′ j wrt σ.

Now we can consider formulae with action modalities:

• (w,⃗e) |= [a]ϕ iff (wa,⃗ea) |= ϕ

• (w,⃗e) |= □α iff (wz,⃗ez) |= α for all z ∈Z

We say a model and a formula α is compatible if, for all i ∈Ag, the i-depth of α is not deeper than the epistemic state of agent i. Given a ﬁnite set Σ ⊆MS,3 α ∈MS, we say Σ entails α (written as Σ |= α) iff for every model (w,⃗e) compatible with each formula in Σ ∪{α}, if (w,⃗e) |= ϕ for all ϕ ∈Σ, then (w,⃗e) |= α. We say α is valid (written as |= α) iff {} |= α. We say a formula α is satisﬁable if there is a compatible model (w,⃗e) s.t. (w,⃗e) |= α. When α is objective, we write w |= α instead of (w,⃗e) |= α. When α is i-subjective, we write ei |= α. Note that MS cannot handle formulae of unbounded depth. When Σ is an inﬁnite set of formulae with unbounded depth, i.e. for all k it exists ψ ∈Σ s.t. dep[ψ] > k, then Σ |= α is not well-deﬁned.

The logic satisﬁes the K45n properties after any actions.

Theorem 1. For any α, β ∈MS and i ∈Ag:

• (Prop) |= □Kiα if α is a (propositional) tautology; • (Dist)|= □Kiα ∧Ki(α →β) →Kiβ;4

• (4)|= □Kiα →KiKiα; • (5)|= □¬Kiα →Ki¬Kiα.

The static entailment amounts to K45n theorem proving.

Theorem 2. Given static Σ and α, Σ |= α iff α is derivable from Σ under the K45n axiom system.

3Σ can also be an inﬁnite set, provided that the depth of formulae is bounded, i.e. it exists k ∈N s.t. dep[ϕ] ≤k for all ϕ ∈Σ.

4Throughout the paper, we assume that the modality □always has the lowest precedence among all operators.

It is proven by constructing a bisimulation between MS models and K45n Kripke models. We refer to (Feng et al. 2025) for the proof. With the syntax and semantics of the logic MS, we now turn to multi-agent action theories, which specify the transition of not only the world but also agents’ mental states.

Multi-Agent Action Theories The proposed action theories are inspired by the BHL framework (Bacchus, Halpern, and Levesque 1999). As in BHL, a theory includes precondition axioms, successor-state axioms (SSAs), which describe the effect of actions, and observation-indistinguishability (OI) axioms, which distinguish the action actually being executed from those likely being executed. In addition, we include axioms on other agents’ knowledge of actions. Deﬁnition 4 (Individual Action Theory). For i ∈Ag and k ∈N, We deﬁne the k-order individual action theory (IAT) of agent i, denoted as Σi,k, as the following axioms:

• Σi,k pre: For each action a ∈Ac,

□Poss(a) ≡πa (2)

• Σi,k ssa: For each a ∈Ac and p ∈Ap,5

□[a]p ≡γp,a (3)

• Σi,k oi: For each a, a′ ∈Ac,

□I(a, a′) ≡φa,a′ (4)

• Σi,k iat: For each j̸ = i, j’s knowledge of actions KjΣj,k−1 is included. When k = 0, Σj,k−1:= ⊤. When k > 0, Σj,k−1 is an IAT of order k −1, where πa, γp,a and φa,a′ are static formulae with a depth at most k. Note that for k > 1, Σj,k−1 includes other agents’ knowledge about actions. The nesting continues until k = 0. Hence, a hierarchical structure is formed. Based on the IAT of each agent, we deﬁne the collective action theory (CAT): Deﬁnition 5 (Collective Action Theory). For k ∈N, a korder CAT, written as Γ, is deﬁned as

Γ:= Γpre ∪Γssa ∪Γoi ∪

[ i∈Ag

KiΣi,ki (5)

where Γpre, Γssa and Γoi are respectively of the form (2-4) and the corresponding πa, γp,a and φa,a′ are static formulae of depth at most k. Σi,ki is the IAT of agent i. We use Ord(Γ, i):= ki to denote the order of agent i’s action theory. Ord(Γ) denotes the maximal order of Γ. By a Γ-model, we mean a model (w,⃗e) compatible with Γ, and (w,⃗e) |= Γ.

Essentially, a k-order IAT corresponds to the mind of an agent with k-order ToM. There are two reasons for having such a hierarchy: The ﬁrst is to distinguish an agent’s IAT from what other agents believe to be his or her IAT, and the second is for the hierarchical nature of ToM: A child with 1-order ToM could accurately reason about others’ beliefs about the world state, and can distinguish what is believed

5Propositions about Poss or I, e.g. poss move, are excluded.

19066

<!-- Page 4 -->

by others from what is true. When two children with 1-order ToM share their rationale behind actions, can they accurately model the knowledge about the mental state transition of the other? The answer is no. A k-order agent cannot reason about the knowledge of another k-order agent, as representing others’ perspectives consumes one level of nesting.

Deﬁnition 6. Given theory Γ which includes KiΣi,k and Σi,k of the form Σi,k pre ∪Σi,k ssa ∪Σi,k oi ∪S j̸=i KjΣj,k−1, the slice of Γ wrt agent i, written as Γi, is a CAT deﬁned as

Γi:= Σi,k pre ∪Σi,k ssa ∪Σi,k oi ∪KiΣi,k ∪

[ j̸=i

KjΣj,k−1 i.e. the precondition axioms, SSAs and OI axioms of Γi are the corresponding parts in Σi,k.

Γi is a CAT reconstructed via agent i’s IAT in Γ. It is not difﬁcult to prove (Γi)i = Γi.

Now we consider the existence of Γ-models: For any model (w,⃗e), since Γ only regulates the state transition but not the initial state, one can construct a Γ-model wrt (w,⃗e) which satisﬁes the same static formulae:

Theorem 3. Given theory Γ and model (w,⃗e) compatible with Γ, there exists a Γ-model (wΓ, e1,Γ,..., en,Γ) (also written as (wΓ,⃗eΓ)) of the same depth such that for each compatible static formula ϕ:

(w,⃗e) |= ϕ iff (wΓ,⃗eΓ) |= ϕ (6)

Proof. Given (w,⃗e), we recursively construct (wΓ,⃗eΓ) such that for all p ∈Ap, z ∈Z and a, a′ ∈Ac,

• wΓ[⟨⟩] = w[⟨⟩]; • p ∈wΓ[z · a] iff (wΓ,⃗eΓ) |= [z]γΓ p,a;

• Poss(a) ∈wΓ[z] iff (wΓ,⃗eΓ) |= [z]πΓ a; • I(a, a′) ∈wΓ[z] iff (wΓ,⃗eΓ) |= [z]φΓ a,a′;

• For any i ∈Ag, ei,Γ = {sΓi | s ∈ei}, where For s = (w, e1,... ei−1, ei+1,... en), sΓi = (wΓi, e1,Γi,... ei−1,Γi, ei+1,Γi,... en,Γi).

Here γΓ p,a, πΓ a and φΓ a,a′ are respectively the right-hand side of Γpre, Γssa and Γoi. For all ej and w, we construct ej,Γi and wΓi in a similar way but wrt Γi instead of Γ. We prove Eq. 6 via a double-induction: The outer induction is on the order of Γ and the inner induction is on the construction of formula ϕ. Base case 1: For a zero-order CAT, it reduces to the singleagent cases with objective ϕ. We refer to (Lakemeyer and Levesque 2011) for the proof details. I.H.1: Suppose that Eq.(6) holds for all Γ′ which satisﬁes Ord(Γ′) < k, formula ϕ, and (w,⃗e) compatible with Γ′. Base case 2: For any Γ with Ord(Γ) = k, It is trivial that (w,⃗e) |= p iff (wΓ,⃗eΓ) |= p. I.H.2: Suppose that (w,⃗e) |= α iff (wΓ′,⃗eΓ′) |= α for all Γ′ with Ord(Γ′) = k and (w,⃗e) compatible with Γ′. Now we consider a ﬁxed Γ. Induction on Boolean operators is trivial.

For induction on the modality Ki,

(w,⃗e) |= Kiα ⇔f.a. s ∈ei, s ∪i ei |= α (Semantics) ⇔f.a. s ∈ei, sΓi ∪i ei,Γi |= α (#)

⇔f.a. s′ ∈ei,Γ, s′ ∪i ei,Γ |= α (ei,Γ = ei,Γi) ⇔ei,Γ |= Kiα ⇔(wΓ,⃗eΓ) |= Kiα

There are two cases for (#): When Ord(Γi) < k, then I.H.1 is applied. Otherwise, we apply I.H. 2 as Ord(Γi) = k.

To prove that (wΓ,⃗eΓ) is indeed a Γ-model, we check each entry of Γ. For the precondition, SSAs and OI axioms, the proof applies simply the semantics and the deﬁnition of (wΓ,⃗eΓ). For the IAT of each agent i:

(wΓ,⃗eΓ) |= KiΣi,ki

⇔s′ ∪i ei,Γ |= Σi,ki f.a. s′ ∈ei,Γ ⇔s′ ∪i ei,Γ |= Σi,ki ∧KiΣi,ki f.a. s′ ∈ei,Γ ⇔s′ ∪i ei,Γ |= Γi f.a. s′ ∈ei,Γ ⇔sΓi ∪i ei,Γi |= Γi f.a. s ∈ei It is equivalent to prove that for each s ∈ei, sΓi ∪i ei,Γi is a Γi-model, which can be proved via induction.

We deﬁne a knowledge base with bounded-order ToM (BoToM-KB) as follows: Deﬁnition 7 (BoToM-KB). A ﬁnite set of formulae Σ0 ∪Γ forms a BoToM-KB, if there is k ∈N such that Σ0 is a static formula of depth at most k, and Γ is a k-order CAT.

Σ0 can be seen as the initial state in the DEL approach, and to some extent, Γ corresponds to the DEL statetransition system. However, to represent the ToM hierarchy in DEL, the event models and product update need to be modiﬁed such that the depths of the Kripke states are considered. So far, no one has investigated such modiﬁcation.

Action Types Three types of action are usually considered in multi-agent domains: ontic actions, sensing, and announcements. We show how these actions can be modeled in our framework.

Ontic actions have actual effects on the world state. Given a theory Γ, an action a is ontic if there is a p ∈Ap such that Γ does not entail □γp,a ≡p. Our framework can represent ontic action with uncertain or unexpected effects. Uncertain effects, either caused by the partial observability of the agent or the non-deterministic nature of the world, can be modeled in the sense that φa,a′ of a ﬁxed a holds for more than one a′. Unexpected effects are modeled in the sense that the action which actually happens is considered impossible, i.e. φa,a does not hold.

In contrast to ontic actions, sensing and announcements do not change the actual world but only what agents believe. Thus, these actions only have trivial SSAs with γp,a ≡p. Let see h be sensing the tossing result Head, then a precise sensing can be represented by

□Poss(see h) ≡Hd; □I(see h, see h) ≡⊤;

□I(see h, a′) ≡⊥for a′̸ = see h

19067

<!-- Page 5 -->

Let Σi include these axioms, then KiΣi |= [see h]KiHd. Our framework supports announcement to any group of agents. Let G!Hd denote the announcement to G ⊆Ag that the coin shows head. For each i ∈G, let Σi,k include

□Poss(G!Hd) ≡Hd; □I(G!Hd, G!Hd) ≡⊤;

□I(G!Hd, a′) ≡⊥for a′̸ = G!Hd.

Let Γ include KiΣi,k for each i ∈G, then

Γ |= [G!Hd]El

GHd for any l up to the order of theory Γ. Other forms of actions, such as noisy sensing or deceptive announcements, will be demonstrated by examples in a later section.

In fact, the notion of “actions” here is similar to “events” in the DEL approach, as the executor of an action is not speciﬁed. While complex constructs such as action proﬁles (multiple agents simultaneously choose actions) can naturally be expressed within our framework, we focus on the general formalism and do not elaborate on these constructs.

Regression For the action theories mentioned above, we introduce the regression method, which transforms epistemic queries on a future situation to those on the current situation. Deﬁnition 8 (Regressable). We call a formula ϕ regressable wrt Γ iff ϕ is bounded, and dep[ϕ, i] ≤Ord(Γ, i) for all i. Deﬁnition 9 (Regression function). For z ∈Z and k-order collective theory Γ, we recursively deﬁne R[Γ, z, α]:

• R[Γ, ⟨⟩, p]:= p for p not mentioning Poss or I; • R[Γ, σ · a, p]:= R[Γ, σ, γΓ p,a]; • R[Γ, σ, Poss(a)]:= R[Γ, σ, πΓ a]; • R[Γ, σ, I(a, a′)]:= R[Γ, σ, φΓ a,a′]; • R[Γ, z, α ∧β]:= R[Γ, z, α] ∧R[Γ, z, β]; • R[Γ, z, ¬α]:= ¬R[Γ, z, α]; • R[Γ, z, [a]α]:= R[Γ, z · a, α]; • R[Γ, ⟨⟩, Kiϕ]:= Ki

R[Γi, ⟨⟩, ϕ]

; • R[Γ, σ · a, Kiϕ]:= R[Γ, σ, Ki

V a′

(Poss(a′) ∧I(a, a′)) →[a′]ϕ

] The regression always terminates and returns a static formula of size O(|ϕ| · |Γ| · |Ac|k·m), where k is the order of Γ and m is the action length of [z]ϕ. When the second argument is an empty sequence, we write R[Γ, α] instead of R[Γ, ⟨⟩, α].

The main motivation for introducing hierarchical structures and descending orders of action theories is to limit the depth of regression results. Via induction, we prove that Theorem 4. For any theory Γ, ϕ regressable wrt Γ, dep[R[Γ, z, ϕ], i] ≤dep[Γ, i] for all z and i ∈Ag.

Namely, the regression never results in a formula deeper than the order of Γ. The regression is correct in the sense that any Γ-model satisﬁes α after sequence z if and only if the model satisﬁes the initial condition R[Γ, z, α]: Lemma 1. Given action theory Γ, for all Γ-model (w,⃗e), z ∈Z and static formula α regressable wrt Γ,

(w,⃗e) |= [z]α iff (w,⃗e) |= R[Γ, z, α] (7)

Proof sketch: We proceed with a triple-induction: The outer-induction is on the order of the theory Γ, the midinduction is on the length of the action sequence z, and the inner-induction is on the construction of formula α.

The lemma can be easily extended to regression on arbitrary bounded formulae: Theorem 5. Given action theory Γ, for all Γ-model (w,⃗e), z ∈Z and bounded formula α regressable wrt Γ,

(w,⃗e) |= [z]α iff (w,⃗e) |= R[Γ, z, α] (8)

Now we are ready for the regression theorem: Theorem 6 (Regression). Given BoToM-KB Σ0 ∪Γ, for all z ∈Z, and formula α regressable wrt Γ,

Σ0 ∪Γ |= [z]α iff Σ0 |= R[Γ, z, α] (9)

Proof. It sufﬁces to prove the equivalence of the statements:

F.a. (w,⃗e) |= Γ, if (w,⃗e) |= Σ0, then (w,⃗e) |= [z]α (10) F.a. (w,⃗e), if (w,⃗e) |= Σ0, then (w,⃗e) |= R[Γ, z, α] (11)

(10)⇒(11): For any model (w,⃗e):

(w,⃗e) |= Σ0 ⇒(wΓ,⃗eΓ) |= Σ0 (Thm. 3) ⇒(wΓ,⃗eΓ) |= [z]α (Eq. 10) ⇒(wΓ,⃗eΓ) |= R[Γ, z, α] (Thm. 5) ⇒(w,⃗e) |= R[Γ, z, α] (Thm. 3)

(10)⇐(11): For any Γ-model (wΓ,⃗eΓ),

(wΓ,⃗eΓ) |= Σ0 ⇒(wΓ,⃗eΓ) |= R[Γ, z, α] (Eq. 11) ⇒(wΓ,⃗eΓ) |= [z]α (Thm. 5)

By Thm. 5 we proved the following result, which will later be used in the planning task. Corollary 1. For z ∈Z, and any ϕ, ψ regressable wrt. Γ,

• if |= ϕ ≡ψ, then |= R[Γ, z, ϕ] ≡R[Γ, z, ψ] • if |= R[Γ, ϕ] ≡R[Γ, ψ], then |= R[Γ, z, ϕ] ≡R[Γ, z, ψ]

## 6 Examples We formalize action theories for two examples: Sally-Anne Test (Wimmer and Perner 1983) and Die

Rolling. Due to the space limit, we only present the key entries of the theories that are relevant to regression. In particular, we consider the dynamics of four actions:

• move: To move the marble. We consider the unexpected effect of the action, or as described in (Baral et al. 2022), an agent is oblivious of the actions’ occurrence. • roll: To roll a die. A non-deterministic action. • show2: An agent saw that the die showed two. We model noisy sensing, namely, a distracted agent might misread the number. •!bob 3: Bob announces that the die shows three (even if it does not). An example of deceptive announcements. Example 1 (Sally-Anne Test). Initially, Sally’s marble is in a basket (and everyone knows that), then Anne (secretly) moves the marble into a box. In a test, the child will be asked “Will Sally look in the box for her marble?”

19068

<!-- Page 6 -->

The test is a classic psychological experiment used to assess the order of ToM: If the participant believes that Sally will not look in the box, it indicates that the child has developed ﬁrst-order ToM and can understand another person’s beliefs, even if they are false. Otherwise, the child has at most zero-order ToM. We show how different orders of ToM can be characterized:

• Ag = {S, C0, C1}, which respectively stands for Sally, Child with 0-order ToM and with 1-order ToM. • Ap = {InBt, InBx} The marble is in the Basket / in the Box. • Ac = {move, void, look bx}, void for nothing happens, look bx for “look in the box for the marble”

We consider a collective theory Γ which includes

• KC0ΣC0, i.e. a 0-order IAT for child C0, and • KC1ΣC1, a 1-order IAT for child C1.

ΣC0 includes

• □Poss(look bx) ≡InBx, • □[move]InBx ≡⊤, □[move]InBt ≡⊥, and • □I(a, a) ≡⊤, □I(a, a′) ≡⊥for all a̸ = a′.

ΣC1 differs from ΣC0 by

• □Poss(look bx) ≡KSInBx, i.e. Sally will look in the box only when she believes that the marble is in the box.

• ΣC1 includes KSΣS,0 where ΣS,0 oi includes □I(move, void) ≡⊤, □I(move, move) ≡⊥. Namely, Sally is oblivious to the move.

Let Σ0 be the initial state. We encode the children’s answers to the test as their knowledge about the possibility of action look bx. By regression, we prove that

Σ0 ∪Γ |= KC0([move]Poss(look bx)) ⇔Σ0 |= R[Γ, KC0([move]Poss(look bx))]

⇔Σ0 |= KC0(R[ΓC0, move, Poss(look bx)])

⇔Σ0 |= KC0(R[ΓC0, move, ⊤]) ⇔Σ0 |= ⊤

Namely, in any initial case, C0 believes that Sally will look in the box for the marble. In contrast, child C1 does not believe that Sally will look in the box. By regression,

Σ0 ∪Γ |= ¬KC1([move]Poss(look bx))

⇔Σ0 |= ¬KC1(R[ΓC1, move, KSInBx])

⇔Σ0 |= ¬KC1KS(R[ΓS, void, InBx]) ⇔Σ0 |= ¬KC1KS(InBx)

According to the example, the child knows that Sally knows that initially, the marble is in the basket instead of the box.

Example 2 (Die Rolling). Alice and Bob roll a die. The result can be shown to them, but when Alice is distracted, she may misread the number. In addition, Bob can announce the number, even if it is wrong, and Alice will believe it anyhow.

• Ag = {A, B}, i.e. two agents Alice and Bob.

• Ac = {roll, roll2, show2,!bob 3,...} roll is a nominal action and roll1 to roll6 are factual actions with the resulting number. show2 and!bob 3 are, respectively, the noisy sensing and announcement mentioned at the beginning of this section. • Ap = {N1,... N6, Dt}. Dt means Alice is distracted, Nx stands for the number that the die shows.

We consider the collective theory Γ which includes KAΣA and KBΣB. Alice’s individual theory ΣA consists of

• □Poss(show2) ≡(Dt →(N2 ∨N3)) ∧(¬Dt →N2) Alice may misread 3 as 2 when she is distracted. • □Poss(!bob 3) ≡N3 ∧¬N1 ∧· · · ∧¬N6 Alice always believes the truth of Bob’s announcement. • □[roll2]N2 ≡⊤and □[roll2]Nx ≡⊥for x̸ = 2. • □I(roll, rollx) ≡⊤for x ∈{1,... 6}

Bob’s theory ΣB differs from Alice’s by

• □Poss(show2) ≡N2, i.e. Bob never misreads. • □Poss(!bob 3) ≡⊤, i.e. Bob can always announce that the number is 3, as long as he wants to do so.

After rolling the die and showing the result 2, to achieve a state where Alice does not know that the die shows 2, by regression we prove that the initial situation must fulﬁll

Σ0 ∪Γ |= [roll][show2]¬KAN2 ⇔Σ0 |= ¬KA¬Dt

Namely, Alice cannot conﬁrm that she stays focused. Lastly, we show how Bob can make a false announcement and manipulate Alice’s beliefs:

Σ0 ∪Γ |= [!bob 3](KAN3) ⇔Σ0 |= ⊤

Namely, Alice will always believe Bob’s announcement.

## 7 Multi-agent Epistemic Planning

Multi-agent epistemic planning amounts to ﬁnding an action sequence such that, after taking the actions, a given goal is fulﬁlled. In the DEL approach, MEP is known to be robustly undecidable mainly because agents can reason with an arbitrary nesting of beliefs (Aucher and Bolander 2013). With the bounded-order hierarchy of the action theories, we restrict the degree of nesting and thus preserve decidability.

Deﬁnition 10 (BoToM-MEP). Given a BoToM-KB Σ0 ∪Γ and a goal α regressable wrt Γ, the BoToM-MEP problem is to decide whether a ﬁnite sequence z exists such that

Σ0 ∪Γ |= Exec(z) ∧[z]α (12)

A sequence z which fulﬁlls (12) is called a solution of the MEP wrt Σ0, Γ and α. Note that the DEL approach deﬁnes MEP based on the satisfaction of a single model and therefore requires complete speciﬁcation of the initial state; and our deﬁnition is based on logical entailment, where multiple, even inﬁnitely many models are involved. Thus, we accept incomplete speciﬁcation.

Theorem 7. For σ1, σ2 ∈Z s.t. R[Γ, Exec(σ1) ∧[σ1]α] and R[Γ, Exec(σ2)∧[σ2]α] are logically equivalent, if z·σ1 is a solution of the problem, then z · σ2 is also a solution.

19069

<!-- Page 7 -->

Proof. Suppose that z · σ1 is a solution,

Σ0 ∪Γ |= Exec(z · σ1) ∧[z · σ1]α ⇐⇒Σ0 ∪Γ |= Exec(z) ∧[z]Exec(σ1) ∧[z · σ1]α ⇐⇒Σ0 ∪Γ |= R[Γ, Exec(z)]

∧R[Γ, z, Exec(σ1) ∧[σ1]α] (Thm. 6) ⇐⇒Σ0 ∪Γ |= R[Γ, Exec(z)]

∧R[Γ, z, Exec(σ2) ∧[σ2]α] (Cor. 1) ⇐⇒Σ0 ∪Γ |= R[Γ, Exec(z) ∧[z]Exec(σ2) ∧[z · σ2]α] ⇐⇒Σ0 ∪Γ |= Exec(z · σ2) ∧[z · σ2]α

Proposition 1. For z = a · σ, Σ0 |= R[Γ, Exec(z) ∧[z]α] if and only if Σ0 |= Poss(a) ∧R[Γ, a, R[Exec(σ) ∧[σ]α]]

With the above theorem and proposition, we are ready to prove the most important result of this work: Theorem 8. BoToM-MEP is decidable.

Proof. Given a k-order theory Γ and α regressable wrt Γ. By Thm. 6, to decide Eq. 12 amounts to decide

Σ0 |= R[Γ, Exec(z) ∧[z]α] (13)

Since both Σ0 and the regression are static, it is reduced to K45n reasoning. By Thm. 4, the regression function always returns a formula with depth bounded by k. As pointed out in (Halpern 1995), for a ﬁxed k and ﬁnite Ap, there are only ﬁnitely many inequivalent static formulae. Let the number of such formulae be N. By Thm. 7 and the Pigeonhole Principle, if (12) has a solution, there must be a solution z of length at most N. Since Ac is also ﬁnite, by enumerating all action sequences up to length N, one can decide if a solution exists.

In fact, it is not needed to enumerate all sequences or to compute the exact number of N. It can be solved more efﬁciently by Algorithm 1: A queue of action sequence candidates Cand is maintained and initialized with the empty one. A dictionary State, which maps action sequences to MS formulae, is maintained and initialized as {⟨⟩: α}. In each iteration of the while-loop, the algorithm pops out the ﬁrst sequence z in Cand, generates a longer sequence a · z for each a ∈Ac, and tests whether Σ0 entails the regression.6 Line 13 tests if the regression is equivalent to a formula in State.7 If the regression wrt a · z is equivalent to one wrt an explored sequence z′, by Thm. 7 the shortest solution expanded from a·z will not be shorter as those expanded from z′. Hence, we can prune a · z. Since the size of State will be at most N, either a solution is found, or eventually every regression can be found in State, then every sequence in Cand will be pruned and it terminates when the queue is empty. Theorem 9. Algorithm 1 terminates and returns FALSE if the BoToM-MEP has no solution. When a solution exists, the algorithm returns a solution z such that for any other solution z′, |z| ≤|z′|.

6By Prop.1 it sufﬁces to perform a single step of regression. 7Though State could be huge, equivalence check can be efﬁcient with proper knowledge compilation methods (Halpern 1995).

## Algorithm

1: Breadth-First BoToM-MEP Search

1: function botommep(Σ0, Γ, α): 2: Cand ←[⟨⟩] 3: State[⟨⟩] ←α 4: if Σ0 |= R[Γ, α] then 5: return ⟨⟩ 6: end if 7: while Cand not empty do 8: z ←POP(Cand) 9: ϕ ←State[z] 10: for a ∈Ac do 11: if Σ0 |= R[Γ, Poss(a) ∧[a]ϕ] then 12: return a · z 13: else if R[Γ, Exec(a) ∧[a]ϕ] /∈State then 14: State[a · z] ←R[Γ, Poss(a) ∧[a]ϕ] 15: PUSH(Cand, a · z) 16: end if 17: end for 18: end while 19: return FALSE 20: end function

## 8 Conclusion

Our work is the ﬁrst attempt to solve MEP in the situation calculus. Compared with the de facto standard approach via DEL model update, our syntactic method avoids the manual construction of semantic models and enables incomplete speciﬁcations. With the price of not being able to deal with common knowledge or arbitrary depth of belief nesting,8 we preserve most of the expressiveness of the DEL approach and have decidable planning. To our knowledge, no existing framework can express all the action types we mentioned, while MEP remains decidable.

This framework brings many future directions: Strategy reasoning and epistemic protocol synthesis generate (group) strategies to ensure temporal goals (Xiong and Liu 2016; Aucher, Maubert, and Pinchinat 2014). In our framework, strategies and protocols can be characterized by additional preconditions. With a probabilistic extension, one can represent the likelihood of non-deterministic actions and measure an agent’s degree of belief (Bacchus, Halpern, and Levesque 1999; Liu and Feng 2023; Feng and Lakemeyer 2024). It is also interesting to implement an actual epistemic planner (Wan, Fang, and Liu 2021; Liu and Liu 2018; Ware and Siler 2021a,b; Muise et al. 2022), or to build a connection with epistemic game theory and description languages for games (Thielscher 2017).

## Acknowledgments

We thank Yongmei Liu (Sun Yat-sen University) for helpful discussions and suggestions regarding related work. This work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) 2236/2 ‘UnRAVeL’ and the EU ICT-48 2020 project TAILOR (No. 952215).

8We treat agents as bounded reasoners with ﬁnite-order ToMs.

19070

<!-- Page 8 -->

## References

Aucher, G. 2011. DEL-sequents for progression. Journal of Applied Non-Classical Logics, 21(3-4): 289–321. Aucher, G. 2012. DEL-sequents for regression and epistemic planning. Journal of Applied Non-Classical Logics, 22(4): 337–367. Aucher, G.; and Bolander, T. 2013. Undecidability in epistemic planning. Ph.D. thesis, INRIA. Aucher, G.; Maubert, B.; and Pinchinat, S. 2014. Automata techniques for epistemic protocol synthesis. arXiv preprint arXiv:1404.0844. Bacchus, F.; Halpern, J. Y.; and Levesque, H. J. 1999. Reasoning about noisy sensors and effectors in the situation calculus. Artiﬁcial Intelligence, 111(1-2): 171–208. Baral, C.; Bolander, T.; van Ditmarsch, H.; and McIlrath, S. 2017. Epistemic planning (Dagstuhl seminar 17231). Dagstuhl Reports, 7(6): 1–47. Baral, C.; Gelfond, G.; Pontelli, E.; and Son, T. C. 2022. An action language for multi-agent domains. Artiﬁcial Intelligence, 302: 103601. Belle, V.; and Lakemeyer, G. 2014. Multiagent only knowing in dynamic systems. Journal of Artiﬁcial Intelligence Research, 49: 363–402. Belle, V.; and Lakemeyer, G. 2015. Semantical considerations on multiagent only knowing. Artiﬁcial Intelligence, 223: 1–26. Bolander, T.; and Andersen, M. B. 2011. Epistemic planning for single-and multi-agent systems. Journal of Applied Non- Classical Logics, 21(1): 9–34. Bolander, T.; Jensen, M. H.; and Schwarzentruber, F. 2015. Complexity results in epistemic planning. In 24th International Joint Conference on Artiﬁcial Intelligence, 2791– 2797. AAAI Press. Claßen, J. 2013. Planning and veriﬁcation in the agent language Golog. Ph.D. thesis, Aachen, Techn. Hochsch., Diss., 2013. De Giacomo, G.; Murano, A.; Rubin, S.; Di Stasio, A.; et al. 2016. Imperfect-Information Games and Generalized Planning. In IJCAI, 1037–1043. Fang, L.; and Liu, Y. 2013. Multiagent knowledge and belief change in the situation calculus. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 27, 304–312. Fang, L.; Liu, Y.; and Wen, X. 2015. On the Progression of Knowledge and Belief for Nondeterministic Actions in the Situation Calculus. In IJCAI, 2955–2963. Feng, Q.; and Lakemeyer, G. 2024. Probabilistic Multiagent Only-Believing. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems, 571–579. Feng, Q.; Wilk, H.; Khan, S. M.; and Lakemeyer, G. 2025. Translating Multi-Agent Modal Logics of Knowledge and Belief into Decidable First-Order Fragments. In Proc. of the 24th International Conference on Autonomous Agents and Multiagent Systems, 740–748.

Halpern, J. Y. 1995. The effect of bounding the number of primitive propositions and the depth of nesting on the complexity of modal logic. Artiﬁcial Intelligence, 75(2): 361– 372. Ho, M. K.; Saxe, R.; and Cushman, F. 2022. Planning with theory of mind. Trends in Cognitive Sciences, 26(11): 959– 971. Lakemeyer, G.; and Levesque, H. J. 2011. A semantic characterization of a useful fragment of the situation calculus with knowledge. Artiﬁcial Intelligence, 175(1): 142–164. Liu, D.; and Feng, Q. 2023. On the progression of belief. Artiﬁcial Intelligence, 322: 103947. Liu, Q.; and Liu, Y. 2018. Multi-agent Epistemic Planning with Common Knowledge. In IJCAI, 1912–1920. L¨owe, B.; Pacuit, E.; and Witzel, A. 2011. DEL planning and some tractable cases. In Logic, Rationality, and Interaction: Third International Workshop, LORI 2011, Guangzhou, China, October 10-13, 2011. Proceedings 3, 179–192. Springer. McCarthy, J.; and Hayes, P. J. 1981. Some philosophical problems from the standpoint of artiﬁcial intelligence. In Readings in artiﬁcial intelligence, 431–450. Elsevier. Muise, C.; Belle, V.; Felli, P.; McIlraith, S.; Miller, T.; Pearce, A. R.; and Sonenberg, L. 2022. Efﬁcient multi-agent epistemic planning: Teaching planners about nested belief. Artiﬁcial Intelligence, 302: 103605. Peloquin, C. 2023. Representing Minds Representing Minds: An Examination of the Association between Recursive Mental State Attributions and Executive Processes. Ph.D. thesis, Open Access Te Herenga Waka-Victoria University of Wellington. Pietarinen, A.-V. 2003. What do epistemic logic and cognitive science have to do with each other? Cognitive systems research, 4(3): 169–190. Reiter, R. 2001. Knowledge in action: logical foundations for specifying and implementing dynamical systems. MIT press. Thielscher, M. 2017. GDL-III: A Description Language for Epistemic General Game Playing. In IJCAI, 1276–1282. Wan, H.; Fang, B.; and Liu, Y. 2021. A general multi-agent epistemic planner based on higher-order belief change. Artiﬁcial Intelligence, 301: 103562. Ware, S. G.; and Siler, C. 2021a. Sabre: A narrative planner supporting intention and deep theory of mind. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence and Interactive Digital Entertainment, volume 17, 99–106. Ware, S. G.; and Siler, C. 2021b. The sabre narrative planner: multi-agent coordination with intentions and beliefs. In AAMAS Conference proceedings. Wimmer, H.; and Perner, J. 1983. Beliefs about beliefs: Representation and constraining function of wrong beliefs in young children’s understanding of deception. Cognition, 13(1): 103–128. Xiong, L.; and Liu, Y. 2016. Strategy Representation and Reasoning for Incomplete Information Concurrent Games in the Situation Calculus. In IJCAI, 1322–1329.

19071

<!-- Page 9 -->

Yu, Q.; Wen, X.; and Liu, Y. 2013. Multi-Agent Epistemic Explanatory Diagnosis via Reasoning about Actions. In IJ- CAI, 1183–1190.

19072
