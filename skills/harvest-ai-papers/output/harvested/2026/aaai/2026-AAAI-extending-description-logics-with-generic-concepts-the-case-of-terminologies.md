---
title: "Extending Description Logics with Generic Concepts – the Case of Terminologies"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38988
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38988/42950
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Extending Description Logics with Generic Concepts – the Case of Terminologies

<!-- Page 1 -->

Extending Description Logics with Generic Concepts – the Case of Terminologies

Joshua Hirschbrunn1, Yevgeny Kazakov1

1University of Ulm, James-Franck-Ring, 89081 Ulm, Germany joshua.hirschbrunn@uni-ulm.de, yevgeny.kazakov@uni-ulm.de

## Abstract

We propose an extension of Description Logics (DLs) with generic concepts and conditional axioms. Inspired by objectoriented languages, generic concepts allow a compact definition of concepts with similar structures. For example, one can define a generic concept Owner[X] to describe objects that own another object from X, and later use a specific replacement of the parameter X, such as Owner[Pet] representing pet owners. Conditional axioms can be used to set bounds on the values that replace the generic parameters. For example, we could restrict replacements of X in a concept Keeper[X] to only subconcepts of Pet. As the set of possible parameter replacements can be infinite and even uncountable, the generic extensions are, in general, undecidable. To identify decidable generic DLs, we focus on the case of terminologies, requiring that variables are only used in definitions of generic concepts. We formulate restrictions that allow a reduction of generic entailment to classical entailment and further conditions that ensure decidability.

## Introduction

Many large Description Logics (DLs) ontologies exhibit regularities in their syntactic structure (Mikroyannidi et al. 2011, 2012), and there have been several proposals to model such regularities within the languages so that ontologies are easier to maintain (Gangemi and Presutti 2009; He, Zheng, and Lin 2015; Skjæveland et al. 2018; Krieg-Br¨uckner, Mossakowski, and Neuhaus 2019; Skjæveland et al. 2017; Borgida et al. 2012; Kindermann, Parsia, and Sattler 2019; Kindermann et al. 2018, 2024). One proposal is to apply the principles of generic programming for object-oriented languages (Garcia et al. 2003) to ontologies. Generic DLs (Hirschbrunn and Kazakov 2024) extend classical DLs with two new features: concept variables and parametrized concepts. Concept variables are placeholders that can be replaced with (ordinary) concepts. For example, a generic concept ∃owns.X uses a concept variable X, which could be replaced with (ordinary) concepts like Pet or Car resulting in (ordinary) concepts ∃owns.Pet and ∃owns.Car. Parameterized concepts are a generalized form of atomic concepts, whose meaning may depend on other concepts. For example, a parameterized concept Owner[X] can be used to de-

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

scribe owners of objects from X, and could be defined using a generic axiom Owner[X] ≡∃owns.X. Thus, Owner[Pet] and Owner[Car] describe two different kinds of owners.

Generic axioms can be interpreted in two ways: using the schema semantics and using the second-order semantics (Hirschbrunn and Kazakov 2024). Under the schema semantics, the axiom Owner[X] ≡∃owns.X is regarded literally as an abbreviation of (countably many) axioms Owner[C] ≡ ∃owns.C obtained by replacing the concept variable X with all possible concepts C from the language. Under the second-order semantics, concept variables can be replaced with arbitrary subsets of the interpretation domain. Secondorder semantics is, generally, stronger than the schema semantics because not every subset of a domain is an interpretation of some concept of the language. However, entailment under the schema semantics can be computed using standard DL algorithms by treating instances of parametrized concepts such as Owner[Pet] and Owner[Car] as distinct atomic concepts. Schema entailment, however, may depend on the language in which the replacement concepts C are constructed: replacing with EL concepts may result in fewer entailments than replacing with ALC concepts (and fewer than for the second-order entailment). Therefore, a central question for generic DLs is, when both semantics result in the same entailments.

The previous work on generic DLs (Hirschbrunn and Kazakov 2024) shows that it is possible to ensure that second-order entailment coincides with the schema entailment by limiting the base language to the DL EL and applying further syntactic restrictions. In this paper, we use a different approach: Instead of restricting the type of concept constructors that can be used in ontologies, we restrict the shape of axioms. Specifically, we allow definitions of (generic) atomic concepts of the form A[X1,..., Xn] ≡C where the left-hand side is a parametrized concept and the right-hand side C is an arbitrary (SROIQ) concept containing only the variables Xi (1 ≤i ≤n) present on the left. A terminology is a set of such concept definitions in which every concept is defined at most once. We can also allow partial concept definitions of the form A[X1,..., Xn] ⊑C, where the partially defined atomic concept may appear in several such partial definitions, because they can be rewritten to concept definitions using concept conjunction and fresh atomic concepts. We also allow the ontology to con-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19143

<!-- Page 2 -->

tain any number of ground axioms, i.e., axioms that do not contain concept variables.

Sometimes, it is useful to further restrict (partial) definitions by limiting the scope of parameters for which they can be used. For this purpose, we introduce a new type of axiom called conditional axiom. Similar to bounds in generic programming (Garcia et al. 2003), conditional axioms allow for restricting the concepts/domain-subsets that are considered for concept variables. A conditional axiom consists of a range of conditions and a target axiom: {γ1,..., γn} ⇒β, the conditions, as well as the target axiom, are classical axioms (potentially using generic concepts). For example, this allows us to specify different kinds of contents: X ⊑File ⇒Contents[X] ⊑Data, X ⊑ Food ⇒Contents[X] ⊑Nutrients, X ⊑Law ⇒ Contents[X] ⊑Paragraphs. If a parameterized concept is applied to an argument that is not satisfied by the conditions, we consider it to be undefined, and it can be interpreted arbitrarily, which aligns with the idea of partial definitions. The terminological part of ontologies that we specify can also be cyclic. For example, our DL extension is able to capture recursive data definitions such as a node of a tree-structure: Node[X] ≡∀hasSuccessor. Node[X] ⊓∃hasValue.X

In this paper, we present the following results. First, we show that reasoning under classical ontologies extended with (only) conditional axioms can be reduced to reasoning with classical ontologies allowing for negated axioms (Section 4). Second, using the conditional axioms, we show a reduction of reasoning with ground generic ontologies to reasoning with classical ontologies (with conditional axioms) (Section 5). Third, we show that we can reduce reasoning with a non-ground generic terminology to reasoning with a ground generic ontology using a fixpoint approach; this approach allows us to extend a model of the ground part of a generic terminology to a model of the whole ontology (Section 6). Finally, we also explain how the semantic restrictions from Section 6 can be achieved syntactically in practice (Section 7).

## Related Work

As mentioned in the introduction, our work is based on the existing generic extension of description logics proposed earlier (Hirschbrunn and Kazakov 2024). We differ from that work in the way we restrict the usage of generic features to keep decidability. Instead of restricting the generic DL to a fragment of the extension of EL, we work with the extension of DLs up to SROIQ, but require that axioms with variables are part of a terminology where each parameterized concept is defined at most once (multiple partial definitions are also allowed). Additionally, we introduce a new feature of the generic extension in this paper, namely, conditional axioms that allow us to restrict the range of concept variables using classical axioms.

Apart from generic extensions, our approach is related to several other areas. Ontology parts of similar syntactic structure are primarily studied in the field of Ontology Design Patterns (ODPs) (Gangemi and Presutti 2009; He, Zheng, and Lin 2015; Skjæveland et al. 2018; Krieg-Br¨uckner,

Mossakowski, and Neuhaus 2019; Skjæveland et al. 2017; Borgida et al. 2012; Kindermann, Parsia, and Sattler 2019). Similar to our reduction of second-order to classical reasoning, this method employs variables to create axiom templates for deriving standard axioms tailored to particular applications. The key distinction from our approach is that ODPs lack true generic concepts like Owner[X] and do not possess model-theoretic semantics. Rather, ODPs are generally a preliminary stage, substituting variables with concepts from predetermined sets of candidates to form a classical ontology that can subsequently be used in the standard way. There are also works in this area that are primarily concerned with finding repeating structures in ontologies (usually with the goal of testing and defining new ODPs) (Mikroyannidi et al. 2011, 2012; Lawrynowicz et al. 2018).

A related but different concept are the Generators introduced by Kindermann et al. (Kindermann et al. 2018). Those are a kind of rule language on top of DLs, consisting of rules called generators that have axiom templates as conditions and targets. If a certain replacement of variables in the conditions results in an axiom that is entailed by the ontology, then the target is added as an axiom to the ontology for the same variable replacement. This is somewhat similar to our conditional axioms, with the most important difference being that usage of these generators requires the (manual) specification of a language of replacement concepts, while in our case, the second-order semantics considers arbitrary subsets of the domain as replacements of the concept variables.

Additionally, in the broader context of DL research, the idea of making axioms depend on other axioms in the DL itself, like we do with conditional axioms, is also not completely new. One example are so-called context description logics (Klarman and Guti´errez-Basulto 2010), which allow axioms to be dependent on a concrete context, which is itself also formulated as a DL axiom. They differ from conditional axioms in that contexts are defined outside the ontology in a special context ontology; there is no direct connection between elements of the context axiom and the classical axiom targeted, as we can establish by sharing variables; and finally, context DLs are a kind of multi-modal DL allowing to formulate a form of possibility and necessity on contexts, which we do not support. We also differ from DL rules (e.g., (Kr¨otzsch, Rudolph, and Hitzler 2008)) because we do not leave the DL language to formulate rules in First-Order Logic (FOL), but formulate conditional axioms directly in the DL of the ontology itself and we quantify over concept variables, not variables for individuals.

## 3 Generic Extension

We start by formally defining the syntax of generic DLs with parameterized concepts, concept variables, and conditional axioms.

Definition 1 (Syntax, extended from (Hirschbrunn and Kazakov 2024)). The syntax of generic DLs consists of disjoint and countably infinite sets NC of concept names, each with an assigned arity ar(A) ∈N (A ∈NC), NR of role names, and NX of concept variables. Given a base DL L

19144

<!-- Page 3 -->

that is a fragment of SROIQ, we define by LX its corresponding generic extension, adding parameterized (atomic) concepts, concept variables, and conditional axioms. Specifically, the set of LX-concepts is the smallest set containing concept variables X ∈NX, classical atomic concepts A ∈NC with ar(A) = 0, concept terms A[C1,..., Cn], where A ∈NC, n = ar(A) ≥1 and C1,..., Cn are LX-concepts, and which is closed under the concept constructors of L. The set of LX-axioms is the smallest set containing all axioms built from LX-concepts using the axiom constructors of L, as well as axioms of the form Γ ⇒β (conditional axioms), where β is a non-conditional LX axiom and Γ is a set of such axioms. An LX-ontology is a (possibly infinite) set K of LX-axioms.

For a conditional axiom α = (Γ ⇒β), we call all elements γ ∈Γ conditions of α and β the target of α. All axioms that are not conditional, i.e., Γ is empty, we call unit axioms. Note that all conditions and the target can only be unit axioms; conditional axioms can not be nested.1 We introduce a range of special notations to facilitate the discussion about LX concepts and axioms.

Definition 2 (Adapted from (Hirschbrunn and Kazakov 2024)). Let the expression ex be either a LX-concept, a LX-axiom, or a LX-ontology. We denote by sub(ex) (all) subconcepts of ex, i.e., substrings of the expression that are valid concepts. For LX-concepts and LX-axioms (that are not using ⇒), we split sub(ex) into sub+(ex) and sub−(ex) the set of concepts that occur positively, respectively negatively, in ex, sub(ex) = sub+(ex)∪sub−(ex).2 We denote by vars(ex) = sub(ex) ∩NX the set of concept variables occurring in ex. We say that ex is ground if vars(ex) = ∅.

A (concept variable) substitution is a partial mapping θ = [X1/C1,..., Xn/Cn] that assigns concepts Ci to concept variables Xi (1 ≤i ≤n). We denote by θ(ex) the result of applying the substitution to ex, defined in the usual way.

In the remainder of the paper, we differentiate between different versions of a DL as follows: If concepts, axioms, and ontologies include concept terms, conditional axioms, and concept variables, we call them generic. If this is not the case, we call these classical.

As described in Section 1, we adapt the existing secondorder semantics for generic extensions (Hirschbrunn and Kazakov 2024) for usage with conditional axioms:

Definition 3 (Second-Order Semantics, adapted from (Hirschbrunn and Kazakov 2024)). A (second-order) interpretation for a LX is a pair I = (∆I, ·I), where ∆I is a nonempty set called the domain of I and ·I is an interpretation function, which assigns to every A ∈NC with arity

1If conditional axioms were allowed to be nested, we would be able to express all boolean combinations over axioms.

2For less expressive DLs occurring positively (negatively) usually simply corresponds to occurring on the right side of the axiom under an even (odd) number of nested negations or on the left side under an odd (even) number of nested negations, for more expressive DLs this can be more difficult, see e.g., (Simancik 2012) for SROIQ.

n = ar(A) a function AI: (2∆I)n →2∆I and to every r ∈NR a relation rI ⊆∆I × ∆I. A valuation for I (also called a variable assignment) is a mapping η that assigns to every variable X ∈NX a subset η(X) ⊆∆I.

The interpretation of LX-concepts CI,η ⊆∆I is recursively defined by XI,η = η(X) for X ∈ NX, A[C1,..., Cn]I,η = AI(CI,η

1,..., CI,η n), and is extended to other LX-concepts in the usual way. Satisfaction of unit axioms I |=2 η β under I and η is determined from the interpretation of LX-concepts in β in the standard way. For example, I |=2 η C ⊑D iff CI,η ⊆DI,η. The interpretation of conditional axioms follows naturally, i.e., I |=2 η Γ ⇒β, iff ∃γ ∈Γ: I̸ |=2 η γ or I |=2 η β. We write I |=2 α if I |=2 η α for every valuation η. Finally, for an ontology K, we write I |=2 K if I |=2 α for every α ∈K, and we write K |=2 α if I |=2 K implies I |=2 α.

We add a few remarks about this definition: First, for a classical ontology, every second-order model is a classical model and vice versa, as the second-order interpretation only differs from a classical interpretation in its treatment of atomic concepts as functions, which is not relevant if we only have atomic concepts with zero arity, as in the case of classical ontologies. Second, notice that for our conditional axioms, the same η is considered for the conditions, as for the target, i.e., the ∀η quantification is outside the implication. This is important as we want conditions to restrict the choice of subsets of the domain that are considered for the variables in the target axiom. For example, all usages of X in {X ⊑Pet} ⇒Keeper[X] ≡∃owns.X ⊓∃feeds.X, must be the same, and describe some kind of pet. Finally, we can easily reduce the entailment of a ground axiom Γ ⇒β, i.e., K |= Γ ⇒β, to the unsatisfiability of K extended with Γ and the conditional axiom {β} ⇒⊤⊑⊥: Clearly, K |= Γ ⇒β iff K ∪Γ |= β and if K ∪{{β} ⇒⊤⊑⊥} is unsatisfiable, then I |= β holds for every model I of K, therefore K |= Γ ⇒β iff K ∪Γ ∪{{β} ⇒⊤⊑⊥} is unsatisfiable.

In the remainder of the paper, we sometimes use the following ordering on (second-order) interpretations: For two interpretations I1 and I2 over the same domain ∆(∆I1 = ∆I2 = ∆), we define: I1 ⪯I2 iff ∀r ∈NR: rI1 = rI2 and ∀A ∈NC, ∀M1,..., Mn ⊆∆: A(M1,..., Mn)I1 ⊆ A(M1,..., Mn)I2.

## 4 Conditional Axioms

We start our analysis by considering the new feature introduced in this paper, i.e., conditional axioms, on their own. That is, we consider the extension of classical DLs (only) with conditional axioms (not yet concept terms or concept variables). For example, we allow axioms such as {A ⊑B, A ⊑C} ⇒∃r.A ⊑⊤. The classical satisfaction relation can easily be extended to these conditional axioms with classical concepts: I |= Γ ⇒β, iff ∃γ ∈Γ: I̸ |= γ or I |= β.

Reasoning with a classical ontology with conditional axioms can be nondeterministically reduced to reasoning with negated axioms by choosing for each conditional axiom either the target axiom or the negation of some condition ax-

19145

<!-- Page 4 -->

iom. Then the satisfiability of our ontology with conditions coincides with the satisfiability of (at least) one of these constructed ontologies.

Theorem 1. There is a non-deterministic algorithm that reduces in polynomial time the satisfiability of a classical ontology with conditional axioms to the satisfiability of an ontology potentially including negated axioms.

Proof. Let K be a classical ontology with conditional axioms. Let K′ be obtained from K by adding (1) all unit axioms to K′ and (2) for each (conditional) axiom {γ1,..., γn} ⇒β ∈K, adding non-deterministically either β or one of ¬γi for some 1 ≤i ≤n. If K is satisfiable, then for some of these choices K′ is satisfiable.

Given I |= K, we can construct one such K′ by doing for each α ∈K the following: If α is a unit axiom, then α ∈K′ otherwise α = {γ1,..., γn} ⇒β, and as I |= α either ∃j(1 ≤j ≤n): I̸ |= γj and we add ¬γj to K′ or I |= β, and we add β to K′. Then I |= K′ and because K′ contains the non-conditional axioms of K and for each conditional axiom, either one of the negated conditions or the target is in K′, K′ fulfills the construction described above.

Conversely, if K′ is satisfiable then K is satisfiable in the same interpretation: Take I such that I |= K′, we show that I |= K. Take α ∈K either α is non-conditional and α ∈K′ or α = {γ1,..., γn} ⇒β and either ∃γj: I |= ¬γj then I |= α or I |= β and I |= α.

This gives us a non-deterministic polynomial-time reduction.

The reduction described in Theorem 1 can be used for DLs, which can express negation of the axioms appearing as conditions. For example, negations of concept inclusion axioms C ⊑D can be expressed as {C(a), (¬D)(a)} with a a fresh individual. Of course, for a less expressive DL like EL, this raises the complexity of reasoning, as effectively we are using ALC reasoning.

## 5 Ground Ontologies

The approach described in the previous section allows us to remove conditional axioms from ontologies to get back to the classical case. With this result, only two features still make it difficult to consider a generic ontology under standard classical interpretations. The first are variables, the second are concept terms. We can leave variables aside for now by considering only ground generic ontologies. To deal with concept terms, a naive way to interpret them under classical interpretations is to simply consider them as new atomic concept names.3 Unfortunately, this has the side effect that we do not account for equivalent axioms anymore, i.e., using classical interpretations in this way for an ontology such as {C ≡D} we do not get A[C] ≡A[D] as a consequence because A[C] and A[D] are two independent atomic concepts. On the other hand, clearly, for second-order semantics, we get A[C] ≡A[D] as the function AJ applied to the same set M = CI = DI twice, gives the same result. To still be able

3This was done in the existing work on generic extensions, leading to syntactic restrictions (Hirschbrunn and Kazakov 2024).

to reduce second-order entailment to classical entailment using this approach, we transform the given ontology using a closure that moves this treatment of equal concepts from the semantics to explicit (conditional) axioms in the ontology:

Definition 4 (Congruence Closure). A congruence axiom is a (conditional) axiom of the form: Vn i=1 Ci ≡Di ⇒ A[C1,..., Cn] ≡A[D1,..., Dn] where n = ar(A) and Ci, Di, LX-concepts (1 ≤i ≤n). The congruence closure of a ground ontology K is the extension of K with all congruence axioms for which A[C1,..., Cn] ∈sub(K) and A[D1,..., Dn] ∈sub(K).

Clearly, all congruence axioms are tautologies under the second-order semantics:

Lemma 2. Let α be a congruence axiom and I a secondorder interpretation. Then I |=2 α.

Proof. Let α be a congruence axiom (Definition 4), I a second-order interpretation, and η a variable assignment. If CI,η i̸ = DI,η i for some i (1 ≤ i ≤ n), then, trivially, I |=2 η α. Otherwise (A[C1,..., Cn])I,η = AI(CI,η

1,..., CI,η n) = AI(DI,η

1,..., DI,η n) = A[D1,..., Dn])I,η, which, likewise, implies I |=2 η α. Since η was arbitrary, we proved I |=2 α.

Lemma 3. Let K be a ground ontology and K′ the congruence closure of K (see Definition 4). Then K is satisfiable under second-order semantics iff K′ is (classically) satisfiable.

Proof. (⇒) Let I = (∆I, ·I) be a second-order interpretation such that I |=2 K. Define the classical interpretation J = (∆J, ·J) with ∆J = ∆I and A[C1,..., Cn]J = AI(CI

1,..., CI n) for every A ∈NC, n = ar(A) and Ci ground LX-concepts (1 ≤i ≤n), and rJ = rI for every r ∈NR. Note that this definition implies that DJ = DI for every ground LX-concept since the extension of interpretation under concept constructors is defined in I and J in the same way. Likewise, I |=2 α iff J |= α for every ground LX-axiom α. Hence, from I |=2 K, we obtain J |= K. Further, by Lemma 2, I |=2 α for every congruence axiom α ∈K′. Hence J |= K′.

(⇐) Let J be a classical interpretation such that J |= K′. Define the second-order interpretation I = (∆I, ·I) with ∆I = ∆J, AI(M1,..., Mn) = A[C1,..., Cn]J if A[C1,..., Cn] ∈sub(K) and Mi = CJ i (1 ≤i ≤n), and AI(M1,..., Mn) = ∅in the remaining cases, and rI = rJ for every r ∈NR. Notice that the interpretation of AJ (M1,..., Mn) is well-defined, i.e., it does not depend on the choice of the atom A[C1,..., Cn] ∈sub(K) such that CI i = Mi (1 ≤i ≤n). Indeed, for every other choice A[D1,..., Dn] ∈sub(K) such that DJ i = Mi (1 ≤i ≤n), by Definition 4, the congruence axiom belongs to K′, and since J |= K′ and CJ i = DJ i (1 ≤ i ≤n), we obtain A[C1,..., Cn]J = A[D1,..., Dn]J. Since A[C1,..., Cn]J = AI(CI

1,..., CI n) for every A[C1,..., Cn] ∈sub(K), similarly like in the case (⇒),

19146

<!-- Page 5 -->

it follows that I |=2 α iff J |= α for every α ∈K. Since J |= K′ and K ⊆K′, it follows that I |=2 K.

Note that K′ can be computed in polynomial time in the size of K since the number of atoms A[C1,..., Cn] ∈ sub(K) is linear in K. Therefore, we get the following result.

Theorem 4. Second-order satisfiability of ground ontologies with conditional axioms can be reduced in polynomial time to the satisfiability of ground ontologies with conditional axioms under classical semantics.

Proof. Let K be a ground ontology with conditional axioms, and K′ its congruence closure according to Definition 4. Note that K′ can be computed in polynomial time in the size of K since the number of atoms A[C1,..., Cn] ∈sub(K) is linear in K. The statement of the theorem now follows directly from Lemma 3.

## 6 Terminologies

Following the results regarding ground ontologies, in this section, we extend our results to the non-ground case. The goal of this section is to reduce the (second-order) satisfiability of generic non-ground ontologies to the (second-order) satisfiability of generic ground ontologies. With the results from the previous sections, this gives us the ability to reduce reasoning with generic ontologies to classical reasoning (with negated axioms).

Our approach works under the assumption that a given generic ontology consists of two parts: a ground part containing arbitrary ground axioms and a terminological part consisting of generic concept definitions. Our main result shows that, under certain semantic conditions, an arbitrary model of the ground part can be extended to a model of the terminological part by using a fixpoint operator reminiscent of defining the least fixpoint semantics for (cyclic) EL terminologies (Baader 2003).

Definition 5 (Generic Terminology). A (generic) concept definition is a conditional axiom α of the form Γ ⇒ A[X1,..., Xn] ≡D (called a complete concept definition) or Γ ⇒A[X1,..., Xn] ⊑D (called a partial concept definition), where n = ar(A) ≥1, X1,..., Xn are distinct variables and vars(Γ) ∪vars(D) ⊆{X1,..., Xn}. We say that α defines A (completely or partially, respectively), call A the defined concept name of α and D its description. A (generic) terminology is a set T of concept definitions, such that a concept is either defined in one complete definition or in one or more partial definitions, but not both.

For a given generic terminology T, we denote completely defined concept names as ΣT def, and partially defined concept names as ΣT part. All other concept names occurring in the terminology are called primitive concept names, denoted ΣT prim. It should be noted that we permit cyclic dependencies among the defined concept names. We do not consider an axiom as a proper concept definition if a variable occurs in the conditional axiom, but not as an argument of the defined concept name. In this case, the definition would be ambiguous; for example, A[X] ≡X ⊓∃r.Y does not clearly define how A[C] should be interpreted.

As said above, we want to take a model of the ground part of an ontology and extend it to a model of the whole ontology (including the non-ground but terminological part). This means that given a model of the non-ground part I, we can only change the interpretation of parameterized concepts for arguments that do not occur in the ground part, e.g., if A[C] is a concept in the ground ontology, we may not change the interpretation of AI(M) for the argument M = CI in order to ensure that our resulting interpretation still is a model. What we can change is the interpretation for “unknown” Ms. We formalize these allowed changes in the following definition.

Definition 6 (Terminological Expansions). Let G be a ground generic ontology, T a generic terminology, and I a model of G, i.e., I |= G. We call a set M ⊆∆I known if there is a C ∈sub(G) such that CI = M, otherwise it is unknown. A subset of P(∆I) is unknown if at least one member is unknown. Then a terminological expansion of I is an interpretation J = (∆J, ·J), such that ∆J = ∆I, ∀r ∈ NR: rJ = rI, ∀C ∈sub(G): CJ = CI, for A ∈ΣT part and M1,..., Mn ⊆∆I unknown, A(M1,..., Mn)J = ∅, and ∀B ∈ΣT prim: BJ = BI. By TxG,T (I) we denote the set of all terminological expansions of I. We omit G and T if they are irrelevant or clear from the context.

Note that, for the concepts appearing in T and G, a J ∈TxG,T (I) differs from I only in the interpretation of defined concept names when those are applied to unknown arguments, i.e., to subsets of the domain that are not “represented” by any concept that occurs in G. This makes sure that for all concepts in G, J and I coincide, i.e., J |=2 G.

We choose to interpret concept terms using partially defined concept names applied to unknown arguments as the empty set in the expansions. The advantage of this is that we immediately know that their definition is entailed by every J ∈TxG,T (I).

Definition 7. An LX-ontology K is said to be admissible if K = G ∪T, where:

A1. G is a ground ontology, A2. T is a (generic) terminology, A3. If A is defined by some α ∈ T with arguments X1,..., Xn, then for every substitution θ such that θ(A[X1,..., Xn]) ∈sub(G) it holds that G |=2 θ(α), A4. If D is the description of some completely defined con- cept name in T, I a model of G and J1, J2 ∈TxG,T (I) such that J1 ⪯J2, then DJ1,η ⊆DJ2,η for every valuation η, i.e., D behaves monotonically.

The notion of an admissible ontology ensures that an extension of a model of the ground part to a model of the terminological part is always possible. Condition 3 prevents a clash of the knowledge of the ground and the terminological parts, e.g., having an axiom ⊤⊑A[B] in G and an axiom A[X] ≡⊥in T violates this condition. Furthermore, Condition 3 ensures that for known arguments, definitions in T are entailed by every J ∈TxG,T (I). This means we do

19147

<!-- Page 6 -->

only need to choose a J ∈TxG,T (I) that also entails complete definitions for unknown arguments to get a model of K. To find this J, we use an approach that (starting from I) changes the interpretation of completely defined concept names step-by-step to get closer to their definition, until a fixpoint is reached.

For such a fixpoint to exist, we need to make sure that the interpretation only increases from step to step. Because we allow defined concept names in the descriptions in T, this can only be ensured if descriptions are always upward monotonic in all concept terms using fully defined concept names. For example, if we had A[X] ≡¬B[X], this would not hold, as if we assume that B[X] increases with every step of our expansion, then A[X] would at the same time decrease. Indeed, if this monotonicity were not required, we would be able to express General Concept Inclusions (GCIs) in our terminology. The reason for this is similar to absorption (Horrocks and Tobies 2000): We can express a GCI C[X] ⊑D[X] as ⊤≡¬C[X] ⊔D[X] and, because this is not allowed as a terminological axiom (as ⊤is not a parameterized concept), we use A[X] ≡¬A[X] ⊓¬B[X] to be able to use B[X] ≡¬C[X] ⊔D[X] instead of ⊤. To prevent such cases, we use Condition 4 in Definition 7.

Definition 8 (One Step Expansion). Let K = G ∪T be an admissible ontology according to Definition 7 and I a model of G. The one-step expansion is a function 1ExpK,I: TxG,T (I) →TxG,T (I) such that 1ExpK,I(J) is the interpretation J ′ ∈TxG,T (I) defined by changing the interpretation of completely defined concept names in the following way: Let A ∈ΣT def, M1,..., Mn ⊆∆I unknown, if A is defined by Γ ⇒A[X1,..., Xn] ≡D ∈T then for η = {X1/M1,..., Xn/Mn}: AJ ′(M1,..., Mn) = DJ,η.

Intuitively, the one-step expansion 1Exp(J) is the result of updating the interpretation of completely defined concept names (when applied to unknown arguments) by using their description. Note that the conditions of Definition 5 ensure that one-step expansion of J is well-defined. In particular, the definition is unambiguous because every concept name is completely defined in T at most once, and all concept variables appearing in this definition must be parameters of this concept name. In this procedure, we do not take the conditions Γ into consideration, because if we make sure that in the extended model the definition A[X1,..., Xn] ≡D holds for every choice of Xi, then it also holds in the cases where Γ is also entailed. Disregarding Γ can also not lead to contradictions: A contradiction with another axiom in T is not possible, because every concept name is only completely defined once (regardless of whether conditions are present or not); And a contradiction with G is not possible because we only change the interpretation for unknown arguments.

We are now ready to show the final result of this section. We use here that the one-step expansion we defined is a monotonic function on the set of terminological expansions, giving us the guaranteed existence of a fixpoint. This fixpoint is our new model of the whole ontology K.

Theorem 5. Let K = G∪T be an admissible ontology and G second-order satisfiable, then K is second-order satisfiable.

Proof. Given a model I = (∆I, ·I) of G, we show that a fixpoint of 1ExpK,I exists such that it is a model of K.

We start by showing the monotonicity of the one-step expansion, i.e., for J1, J2 ∈TxG,T (I), J1 ⪯J2 implies 1Exp(J1) ⪯1Exp(J2). By Definition 8, we need to show A1Exp(J1)(M1,..., Mn) ⊆A1Exp(J2)(M1,..., Mn) for all unknown M1,..., Mn ⊆∆I. Let η = {Xi → Mi} then by Definition 7 Case A4, DJ1,η ⊆ DJ2,η and A(M1,..., Mn)1Exp(J1) = DJ1,η ⊆ DJ2,η = A1Exp(J2)(M1,..., Mn).

One can easily see that ⪯is a complete lattice on Tx(I). Then by Tarski’s Fixpoint Theorem (Lloyd 1987), 1ExpK,I has a fixpoint, let J denote such a fixpoint. As J ∈ TxG,T (I) we know J |=2 G.

We now show that J |=2 T. Take Γ ⇒β ∈T and some η, we show that J |=2 η Γ ⇒β. Assume that β defines A for arguments X1,..., Xn. Case 1: If we have A[C1,..., Cn] ∈ sub(G) and η(Xi) = CJ i (1 ≤i ≤n), then by Definition 7 Case A3, G |=2 [X1/C1,..., Xn/Cn](Γ ⇒β) and as J |=2 G, we get J |=2 η Γ ⇒β. Case 2: Assume that J̸ |=2 η Γ, then trivially J |=2 η Γ ⇒β, therefore in the remainder we assume that J |=2 η Γ and proof J |=2 η β. Case 3: Assume that β = A[X1,..., Xn] ⊑D, then by Definition 6, A[X1,..., Xn]J,η = ∅and therefore J |=2 β. Case 4: Assume that β = A[X1,..., Xn] ≡D, then because J is a fixpoint of the one-step expansion, we know that applying the one-step expansion to J does not change the interpretation of β. Then we know that for the interpretation of A[X1,..., Xn] this means that A[X1,..., Xn]J,η = DJ,η and J |=2 η β. Therefore, we have shown that there is a model J such that J |= K.

## 7 Ensuring Admissibility

In the previous section, we have shown that the satisfiability of a generic ontology with an arbitrary ground part and a terminological non-ground part can be reduced to the satisfiability of the ground part only. The requirement for this result is, that the given ontology is admissible (Definition 7), i.e., fulfills certain restrictions: First, for a defined concept name, the definition must already be entailed for known arguments by the ground part (A3), second, the descriptions of complete concept definitions need to be (upward) monotonic in the contained concept terms using completely defined concept names, i.e., increase if the interpretation of subterms increases (A4). These are both semantic restrictions; in this section, we discuss how these restrictions can be achieved in practice, i.e., turned into the following syntactic restrictions. Definition 9. An LX-ontology K is said to be practically admissible if K = G ∪T, where: B1. G is a ground ontology, B2. T is a (generic) terminology, B3. If D is a description in T, and A[C1,..., Cn] ∈sub(D)

then C1,..., Cn are variables or 0-ary atomic concepts. B4. For each A[X1,..., Xn] ≡D ∈T: If B[C1,..., Cm] ∈ sub(D) such that B[X1,..., Xm] ≡D′ ∈T, then B[C1,..., Cm] ∈sub+(D).

19148

<!-- Page 7 -->

Definition 10 (Ground Expansion). Given a generic ontology K, consisting of a ground part G and a generic terminology T, i.e. K = G ∪T, we define the ground expansion Exp(G) as the set of axioms achieved in the following way: All axioms in G are in Exp(G). Then we repeatedly check if for A[C1,..., Cn] ∈sub(Exp(G)) such that A is defined by α in T, we have θ(α) ∈Exp(G) for θ = {X1/C1,..., Xn/Cn}. If this is not the case, we add θ(α) to Exp(G). We repeat this until no new axioms are added to Exp(G).

To get from condition A3 to B3, we use the ground expansion procedure. This procedure does not terminate in every case. To achieve termination, it is important that there do not occur complex concepts or concept terms as arguments (of concept terms) in T. If this were the case and we additionally have a cyclic dependency (which we allow), we could get non-termination: Consider, e.g. A[X] ≡ A[B[X]] ∈T, then any replacement of X with a concept C from A[C] ∈sub(Exp(G)) results in a new concept A[B[C]] ∈sub(Exp(G)), which again results in a new concept A[B[B[C]]] ∈sub(Exp(G)) and so on. This would result in an infinite Exp(G). If we do not have complex concepts or concept terms as arguments, calculating the expansion of G takes at most exponential time (even in the presence of cycles). This is because, in the worst case, we have to ground every terminological axiom with every set of concepts occurring as arguments of concept terms in K.

Clearly, if the original K is satisfiable, then the resulting Exp(G) is also satisfiable, as we only add instances of axioms in T. Furthermore, it is easy to see that now K′ = Exp(G) ∪T fulfills Condition A3. Therefore, instead of checking A3, we can instead check B3 and apply the procedure from Definition 10.

Similarly, it is possible to turn the semantic condition A4 into the syntactic condition B4. A4 requires the descriptions of complete concept definitions to behave monotonically if the interpretation of other completely defined concept names (applied to unknown arguments) is extended. (The interpretation of other concepts is already fixed in Tx(I), compare Definition 6 and Definition 7). It is well known that positive polarity of subterms results in the concept being upward monotonic in the subterm (see e.g., (Blackburn, de Rijke, and Venema 2001)). Using a suitable definition of positive polarity for SROIQ (e.g., (Simancik 2012)) this can be shown in general using induction on the structure of the concept description. In our case, a simple syntactic condition (B4) that is sufficient to achieve monotonicity, is to require that concept terms using completely defined concept names may only occur positively in a complete concept description.

Therefore, instead of checking the admissibility of an LXontology according to the semantic Definition 7, we can instead use the syntactic practical admissibility in Definition 9.

Corollary 6. If an ontology K = G ∪T is practically admissible according to Definition 9, then the ontology K′ = Exp(G) ∪T is admissible according to Definition 7 and K is second-order satisfiable iff K′ is second-order satisfiable.

Taking these remarks together with our earlier results, we obtain the following reduction as a consequence of Theo- rems 1, 4, and 5:

Corollary 7. Given a generic ontology K satisfying Definition 9, the satisfiability of K under second-order semantics can be reduced in exponential time to the satisfiability of classical ontologies with negated axioms.

## 8 Discussion and Conclusion

Generic description logics were introduced to efficiently handle collections of similar axioms in ontologies, offering advantages akin to those of generic classes in programming: A concept name’s definition can be applied in various contexts, minimizing the necessity for duplicating and altering intricate concept structures. This method supports modular ontology construction and aids in preventing mistakes that may occur during axiom refactoring. Unfortunately, existing generic extensions (Hirschbrunn and Kazakov 2024) were limited to fragments of the extension of EL.

In this paper, we lift that restriction and demonstrate the decidability of generic extensions of expressive DLs up to SROIQ. We achieve this by requiring that axioms with variables are only used to define concept names, while they can be used freely when ground. This is a reasonable restriction, as this captures the initial idea of generic concepts, namely, being a way to combine the definition of many similar concepts into one place. It also corresponds to the historic development of DLs, which also started with terminologies.

We also introduce a new feature of generic extensions, namely, conditional axioms. These allow us to formulate conditions under which an axiom should hold, while in interpretations where these conditions do not hold, the axiom can be ignored. Conditional axioms are a natural addition to generic DLs, akin to bounds in generic programming. They can be used as a check on variable replacements in concept terms, allowing to select one (or more) of potentially many partial definitions given for a concept name in an ontology. Furthermore, conditional axioms are also an advantage for complete definitions, for example, we can formulate that the definition of Keeper[X] “makes sense” only when X describes some set of pets, i.e., {X ⊑Pet} ⇒ Keeper[X] ≡∃owns.X ⊓∃feeds.X. This prevents modeling errors, where Keeper[·] is used with some wrong argument, such as Keeper[Car].

Planned future work includes implementing the approach described here, studying how existing ontologies might benefit from generic extensions, specifically, determining the extent to which inherent complexity can be reduced, and developing a tool for automatically translating existing ontologies to use the generic extension.

In summary, the findings in this paper demonstrate that it is possible to get generic extensions of expressive description logics that are still decidable, provided certain reasonable restrictions are applied. Additionally, the introduction of conditional axioms allows the use of generic concepts in a more targeted way by restricting the replacement of parameters. This is a valuable addition to the area of generic description logics, as well as to the broader research area that deals with exploiting syntactic regularities in ontologies.

19149

<!-- Page 8 -->

## References

Baader, F. 2003. Terminological cycles in a description logic with existential restrictions. In IJCAI, volume 3, 325–330. Blackburn, P.; de Rijke, M.; and Venema, Y. 2001. Modal Logic, volume 53 of Cambridge Tracts in Theoretical Computer Science. Cambridge University Press. ISBN 978-1- 10705088-4. Borgida, A.; Horkoff, J.; Mylopoulos, J.; and Rosati, R. 2012. Experiences in Mapping the Business Intelligence Model to Description Logics, and the Case for Parametric Concepts. In Kazakov, Y.; Lembo, D.; and Wolter, F., eds., Proceedings of the 2012 International Workshop on Description Logics, DL-2012, Rome, Italy, June 7-10, 2012, volume 846 of CEUR Workshop Proceedings. CEUR- WS.org. Gangemi, A.; and Presutti, V. 2009. Ontology Design Patterns. In Staab, S.; and Studer, R., eds., Handbook on Ontologies, 221–243. Springer Berlin Heidelberg. ISBN 978- 3-540-70999-2 978-3-540-92673-3. Garcia, R.; Jarvi, J.; Lumsdaine, A.; Siek, J. G.; and Willcock, J. 2003. A comparative study of language support for generic programming. In Proceedings of the 18th annual ACM SIGPLAN conference on Object-oriented programing, systems, languages, and applications, 115–134. He, Y.; Zheng, J.; and Lin, Y. 2015. Ontorat: Automatic generation and editing of ontology terms. In Couto, F. M.; and Hastings, J., eds., Proceedings of the International Conference on Biomedical Ontology, ICBO 2015, Lisbon, Portugal, July 27-30, 2015, volume 1515 of CEUR Workshop Proceedings. CEUR-WS.org. Hirschbrunn, J.; and Kazakov, Y. 2024. Extending Description Logics with Generic Concepts – the Tale of Two Semantics. In Marquis, P.; Ortiz, M.; and Pagnucco, M., eds., Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning, KR 2024, Hanoi, Vietnam. November 2-8, 2024. Horrocks, I.; and Tobies, S. 2000. Reasoning with Axioms: Theory and Pratice. CoRR, cs.LO/0005012. Kindermann, C.; George, A.-M.; Parsia, B.; and Sattler, U. 2024. Minimal Macro-Based Rewritings of Formal Languages: Theory and Applications in Ontology Engineering (and Beyond). In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 10581–10588. Issue: 9. Kindermann, C.; Lupp, D. P.; Sattler, U.; and Thorstensen, E. 2018. Generating Ontologies from Templates: A Rule- Based Approach for Capturing Regularity. In Ortiz, M.; and Schneider, T., eds., Proceedings of the 31st International Workshop on Description Logics co-located with 16th International Conference on Principles of Knowledge Representation and Reasoning (KR 2018), Tempe, Arizona, US, October 27th - to - 29th, 2018, volume 2211 of CEUR Workshop Proceedings. CEUR-WS.org. Kindermann, C.; Parsia, B.; and Sattler, U. 2019. Comparing Approaches for Capturing Repetitive Structures in Ontology Design Patterns. In Janowicz, K.; Krisnadhi, A. A.; Poveda- Villal´on, M.; Hammar, K.; and Shimizu, C., eds., Proceedings of the 10th Workshop on Ontology Design and Patterns

(WOP 2019) co-located with 18th International Semantic Web Conference (ISWC 2019), Auckland, New Zealand, October 27, 2019, volume 2459 of CEUR Workshop Proceedings, 17–31. CEUR-WS.org. Klarman, S.; and Guti´errez-Basulto, V. 2010. ALCALC: A Context Description Logic. In Janhunen, T.; and Niemel¨a, I., eds., Logics in Artificial Intelligence - 12th European Conference, JELIA 2010, Helsinki, Finland, September 13-15, 2010. Proceedings, volume 6341 of Lecture Notes in Computer Science, 208–220. Springer. Krieg-Br¨uckner, B.; Mossakowski, T.; and Neuhaus, F. 2019. Generic Ontology Design Patterns at Work. In Barton, A.; Sepp¨al¨a, S.; and Porello, D., eds., Proceedings of the Joint Ontology Workshops 2019 Episode V: The Styrian Autumn of Ontology, Graz, Austria, September 23- 25, 2019, volume 2518 of CEUR Workshop Proceedings. CEUR-WS.org. Kr¨otzsch, M.; Rudolph, S.; and Hitzler, P. 2008. Description Logic Rules. In Ghallab, M.; Spyropoulos, C. D.; Fakotakis, N.; and Avouris, N. M., eds., ECAI 2008 - 18th European Conference on Artificial Intelligence, Patras, Greece, July 21-25, 2008, Proceedings, volume 178 of Frontiers in Artificial Intelligence and Applications, 80–84. IOS Press. Lawrynowicz, A.; Potoniec, J.; Robaczyk, M.; and Tudorache, T. 2018. Discovery of emerging design patterns in ontologies using tree mining. Semantic Web, 9(4): 517–544. Lloyd, J. W. 1987. Foundations of logic programming. Berlin; New York: Springer-Verlag. ISBN 978-0-387- 18199-8. Mikroyannidi, E.; Iannone, L.; Stevens, R.; and Rector, A. 2011. Inspecting Regularities in Ontology Design Using Clustering. In Aroyo, L.; Welty, C.; Alani, H.; Taylor, J.; Bernstein, A.; Kagal, L.; Noy, N.; and Blomqvist, E., eds., The Semantic Web – ISWC 2011, volume 7031, 438–453. Springer Berlin Heidelberg. ISBN 978-3-642-25072-9 978- 3-642-25073-6. Series Title: Lecture Notes in Computer Science. Mikroyannidi, E.; Manaf, N. A. A.; Iannone, L.; and Stevens, R. 2012. Analysing Syntactic Regularities in Ontologies. In OWLED, volume 849. Simancik, F. 2012. Elimination of Complex RIAs without Automata. In Kazakov, Y.; Lembo, D.; and Wolter, F., eds., Proceedings of the 2012 International Workshop on Description Logics, DL-2012, Rome, Italy, June 7-10, 2012, volume 846 of CEUR Workshop Proceedings. CEUR- WS.org. Skjæveland, M. G.; Forssell, H.; Kl¨uwer, J. W.; Lupp, D. P.; Thorstensen, E.; and Waaler, A. 2017. Reasonable Ontology Templates: APIs for OWL. In Nikitina, N.; Song, D.; Fokoue, A.; and Haase, P., eds., Proceedings of the ISWC 2017 Posters & Demonstrations and Industry Tracks co-located with 16th International Semantic Web Conference (ISWC 2017), Vienna, Austria, October 23rd - to - 25th, 2017, volume 1963 of CEUR Workshop Proceedings. CEUR-WS.org. Skjæveland, M. G.; Lupp, D. P.; Karlsen, L. H.; and Forssell, H. 2018. Practical Ontology Pattern Instantiation, Discovery, and Maintenance with Reasonable Ontology Tem-

19150

<!-- Page 9 -->

plates. In Vrandecic, D.; Bontcheva, K.; Su´arez-Figueroa, M. C.; Presutti, V.; Celino, I.; Sabou, M.; Kaffee, L.; and Simperl, E., eds., The Semantic Web - ISWC 2018 - 17th International Semantic Web Conference, Monterey, CA, USA, October 8-12, 2018, Proceedings, Part I, volume 11136 of Lecture Notes in Computer Science, 477–494. Springer.

19151
