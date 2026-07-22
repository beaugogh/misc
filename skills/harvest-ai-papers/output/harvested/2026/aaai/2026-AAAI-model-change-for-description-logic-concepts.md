---
title: "Model Change for Description Logic Concepts"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39008
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39008/42970
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Model Change for Description Logic Concepts

<!-- Page 1 -->

## Model

Change for Description Logic Concepts

Ana Ozaki1, Jandson S. Ribeiro 2

1University of Oslo, Norway 2Cardiff University, UK ana.ozaki@uib.no, ribeiroj@cardiff.ac.uk

## Abstract

We consider the problem of modifying a description logic concept in light of models represented as pointed interpretations. We call this setting model change, and distinguish three main kinds of changes: eviction, which consists of only removing models; reception, which incorporates models; and revision, which combines removal with incorporation of models in a single operation. We introduce a formal notion of revision and argue that it does not reduce to a simple combination of eviction and reception, contrary to intuition. We provide positive and negative results on the compatibility of eviction and reception for EL and ALC description logic concepts and on the compatibility of revision for ALC concepts.

## Introduction

Keeping beliefs updated is a central problem in knowledge representation, that has been investigated in the context of different logics and applications. In the main streams of belief change research, the belief base is finite and the pieces of information expressing how to modify it are expressed as sets of formulae in the underlying logic (Hansson 1999; G¨ardenfors 1988; Alchourr´on, G¨ardenfors, and Makinson 1985). In many scenarios, however, using sets of models to specify the observed change is more suitable than using formulae. This is well studied in the context of learning from interpretations (De Raedt 1997), where the goal is to find a concise formula that is consistent with models labelled as positive or negative. In the context of description logic (DL), the process of building an ontology usually goes through stages where the person creating it studies possible models of world, discarding models when they are proven false and adding new models previously not considered. The next examples illustrate model change operations for DL concepts.

Example 1. Araci is visiting a zoo in Australia and knows little about Australian animals. She knows that a platypus is a mammal that lays eggs, so her belief on platypus is

Platypus ≡Mammal⊓(∃lays.Egg).

She sees a platypus ‘d’ but knows nothing about their diet. So, she entertains the two following possible worlds (I1,d)

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

and (I2,d) with {d,e} ⊆∆I1 = ∆I2:

I1 ∶ d ∈MammalI1 d /∈HerbivoreI1

(d,e) ∈laysI1 e ∈EggI1

I2 ∶ d ∈MammalI2 d ∈HerbivoreI2

(d,e) ∈laysI2 e ∈EggI2

She catches the platypus eating a small insect, which makes Araci retract the pointed interpretation (I2,d). So, she changes her conceptual beliefs about platypuses to

Platypus ≡Mammal⊓(∃lays.Egg)⊓¬Herbivore.

Ex. 1 illustrates the process of removing a model from the concept, producing a concept closer to the real world. This change operation is called eviction (Guimar˜aes, Ozaki, and Ribeiro 2023), and should minimally modify the concept. The next example illustrates its dual: the process of adding a model, called reception. Example 2. Araci knows that kangaroos and koalas are marsupials, but knows little about Tasmanian devils. So, her beliefs about marsupials are Marsupial ≡Koala⊔Kangaroo. In the Tasmanian devils section, she sees a devil ‘d′’ and reads a sign with the information that tasmanian devils are marsupials. So, she now admits a world (I3,d′) where

I3 ∶d′ ∈TasDevilI3, d′ ∈CarnivoreI3, d′ ∈MarsupialI3

She changes her conceptual beliefs to comply with (I3,d′):

Marsupial ≡Koala⊔Kangaroo⊔TasDevil.

In both examples, Araci minimally modified her concepts. For platypus, she modified only concepts related to the diet, while for the Tasmanian devil, she modified only concepts related to marsupials and devils; no further changes relate to kangaroos or koalas were carried out. Ensuring minimal change in this setting is a challenge, as it is not always possible to retract or incorporate the single input model (Guimar˜aes, Ozaki, and Ribeiro 2023). A third and more complex kind of operation is illustrated in Ex. 3, where one must add and remove models in a single step. Example 3. Araci believes that koalas are marsupial mammals that are not placental. So her concept on koalas is:

Koala ≡Mammal⊓Marsupial⊓¬Placental.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19321

<!-- Page 2 -->

She sees a koala ‘d′′’ in the zoo, so she considers the model (I4,d′′) possible, but not (I5,d′′).

I4 ∶d′′ ∈MammalI4 d′′ ∈MarsupialI4 d′′ ∉PlacentalI4

I5 ∶d′′ ∈MammalI5 d′′ ∈MarsupialI5 d′′ ∈PlacentalI5

She reads a sign informing that koalas are actually placental. So she is compelled to comply with (I5,d′′), whereas retracting (I4,d′′). Therefore, she changes her belief to

Koala ≡Mammal⊓Marsupial⊓Placental.

In Ex. 3, the model (I4,d′′) had to be removed, while (I5,d′′) is added. We call this more complex operation a revision. After providing preliminaries (Sec. 2) and recalling eviction and reception (Sec. 3), we present our main contributions in this paper, which are:

• a theoretical study on eviction and reception for DL concepts in ALC and EL (Sec. 4); and • the introduction of the notion of model revision (Sec. 5), with some results for DL concepts (Sec. 6). Contrary to intuition, revision does not correspond to a serial combination of eviction and reception, as we show in this paper. In general, it may well be impossible to add and remove exactly and only the models of the input.

## Related Work

Our contribution is closest to the work by (Guimar˜aes, Ozaki, and Ribeiro 2023), with the main differences being that they neither consider revision nor DL concepts. Although their results on eviction and reception of DL ontologies inspired some of our proofs, the settings are considerably different, with the DL concept case that we present here being arguably more natural to the process of modelling concepts, which is fundamental for building ontologies. In this line, there has been work on computing least common subsumers, which generalize a set of concepts with minimal change (Baader, Sertkaya, and Turhan 2007). Recent work considered learnability of DL concept expressions with pointed interpretations labelled as positive and negative (ten Cate, Koudijs, and Ozaki 2024). One can see the positive and negative pointed interpretations in their work as the sets of models to be added and removed in our setting. The difference from their work to ours is that here we focus on the existence of operators following minimal change rationality postulates, while they focus on the existence of sets of labelled models that characterize a DL concept, that is, that can be used to distinguish a particular concept from all the others in a DL language for concepts. Ontology learning from interpretations has been investigated by (Klarman and Britz 2015). Other works investigated learnability of DL concepts in a data retrieval setting (Funk, Jung, and Lutz 2021; Funk et al. 2019), using inductive logic programming (Lehmann 2009; Fanizzi, d’Amato, and Esposito 2008; Lehmann and Haase 2009; Lehmann and Hitzler 2010), and with counterfactuals (Iannone, Palmisano, and Fanizzi 2007). We also point out works relating learning, epistemic logic, and belief revision (Baltag, Gierasimczuk, and Smets 2019; Baltag et al. 2019; Ozaki and Troquard 2019; Schwind et al. 2025).

## Preliminaries

The power set of a set A is denoted by ℘(A), while the set of all finite subsets of A is denoted by ℘f(A). Given a preorder ⩽⊆D ×D on a domain D, and a set A ⊆D, the set of all maximal and minimal elements of A w.r.t. ⩽are respectively max⩽(A) = {x ∈A ∣for all y ∈A if x ⩽y, then y ⩽x}, and min⩽(A) = {x ∈A ∣for all y ∈A if y ⩽x, then x ⩽y}. We write ℘∗(A) to denote the non-empty subsets of A. Following Aiguier et al. (2018); Delgrande, Peppas, and Woltran (2018), and Guimar˜aes, Ozaki, and Ribeiro (2023), we use satisfaction systems to define logics. A satisfaction system is a triple Λ = (L,M,⊧), where L is a non-empty (possibly countably infinite) language, M is a set of models, and ⊧⊆M×℘(L) is a relation, called the satisfaction relation, which relates models to subsets of the language. We use the infix notation M ⊧B as a shorthand for (M,B) ∈⊧and say that M satisfies B. Every subset of L is called a base (which can be finite or infinite), denoted B. We denote by modΛ(B) the set {M ∈M ∣M ⊧B}. We write mod(B) when the satisfaction system is clear from the context. Satisfaction systems facilitate the generalisation of some results that do not depend on certain properties of the consequence relation of the logic. A set of models M ⊆M within Λ is finitely representable iff there is B ∈℘f(L) such that mod(B) = M. Let FR(Λ) denote all finitely representable sets of models in Λ, i.e.,

FR(Λ) = {M ⊆M ∣∃B ∈℘f(L) ∶mod(B) = M}.

Given a set M of models, the greatest finitely-representable subsets of M and the least finitely-representable supersets of M are given respectively by

MaxFRSubs(M,Λ) = max⊆({M′ ∈FR(Λ) ∣M′ ⊆M}),

MinFRSups(M,Λ) = min⊆({M′ ∈FR(Λ) ∣M ⊆M′}).

We say that a set of formulae B ⊆L is finitely representable iff there is B′ ∈℘f(L) with mod(B) = mod(B′). We write × for the Cartesian product of two sets. Also, we denote the logical closure of a base in a satisfaction system Λ by CnΛ, omitting the subscript when clear from the context.

DL Concepts Let NC and NR be countable and pairwise disjoint sets of concept names and role names, respectively. In this work, NC and NR can be finite or infinite. We explicitly indicate when these sets, called signature, are finite (otherwise, they are assumed to be infinite). EL concepts are built according to the rule: C,D ∶∶= ⊺∣A ∣(C⊓D) ∣(∃r.C), where A ∈NC and r ∈NR. EL concepts extend EL by allowing (interpreted as the empty set). ALC concepts extend EL concepts with the rule ¬C (recall that C⊓¬C is equivalent to, so ALC extends EL). We may write ∃rn.⊺, with n ∈N, as a shorthand for the nesting of n existential quantifiers (that is, ∃rn+1.⊺= ∃r.(∃rn.⊺)) and ∃r0.⊺= ⊺.

Semantics The semantics of EL, EL, and ALC concepts is defined using pointed interpretations (Baader et al. 2017; Agi et al. 2003). An interpretation I is a pair (∆I,⋅I), where ∆I is a non-empty set, called the domain, and ⋅I is a function that maps every A ∈NC to a subset of ∆I and every r ∈NR to a subset of ∆I ×∆I. It is finite if ∆I is finite. A pointed

19322

<!-- Page 3 -->

interpretation is a pair (I,d) where I = (⋅I,∆I) is an interpretation and d ∈∆I. A pointed interpretation (I,d) satisfies a concept C iff d ∈CI. We define tree-shaped pointed interpretations using the notion of unfolding (Dummett and Lemmon 1959) (see also (Konev et al. 2016)). We say that a concept C entails a concept D if for all pointed interpretations (I,d) (over the signature), d ∈CI implies d ∈DI. Two concepts C,D are equivalent, written C ≡D, iff C entails D and D entails C. Given a fixed but arbitrary r ∈NR, we define Mn = (N,⋅Mn) where rMn = {(i,i+1) ∣i ∈N,0 ≤i < n} and similarly M∞= (N,⋅M∞) where rM∞= {(i,i+1) ∣i ∈N}.

DL concepts in Satisfaction Systems In a satisfaction system, we use the term ‘base’ for a subset of formulas in a logic language. We treat a set of concepts and a concept formed by the conjunction of the elements of the set interchangeably. So we may refer to a base as a concept or as a finite set of concepts (in the latter, we mean the concept formed by the conjunction). The notion of a ‘model’ in a satisfaction system corresponds to the notion of a pointed interpretation.

## Model

Reception and Eviction This section addresses the problem of modifying a finite base in light of a set of models, as illustrated in Ex. 1 and Ex. 2. We call such kinds of operators model change operators. Guimar˜aes, Ozaki, and Ribeiro (2023) distinguished two main primitive kinds of model change operators:

eviction: remove a set M of models from a base B, that is, turn B into a base B′ whose models are not in M; reception: incorporate all models from the set M into a base

B, that is, turn B into a base B′ such that all models in M satisfy B′. In some scenarios, not all sets of models need to be taken into account. For instance, some DLs have the finite model property or the tree-shaped property. So, it makes sense to also consider model change operators that only take into account such classes of models. Formally, a class of models on a satisfaction system Λ = (L,M,⊧) is a set C ⊆℘(M) with sets of interpretations. Model change operators are, therefore, defined on a given class of models.

Definition 4. A model change operator in a class C of models is a function ○∶℘f(L)×C →℘f(L), mapping each finite base B into a finite base B′ in light of a set of models.

For conciseness, we may omit the reference to the class C of models if C is clear from the context. The main challenge of model change operators is to guarantee the finiteness of the new base, which presents two main hurdles: 1. some sets of models cannot be uniquely added/removed to/from some bases, as Ex. 5 below illustrates. 2. the simple addition/removal of a set of models might not be finitely representable. This occurs because the language of logic is not expressive enough to distinguish all the models in a set from those which are not in the set. This issue is illustrated at Ex. 6. Example 5. Consider the EL concept ∃r3.⊺, with NC = ∅, NR = {r}, and the pointed models (I1,d1) and (I2,d1) with domains ∆I1 = {d1,d2} and ∆I2 = {d1,d2,d3}, where

I1 ∶rI1 = {(d1,d2)} I2 ∶rI2 = {(d1,d2),(d2,d3)}

Neither (I1,d1) nor (I2,d1) are models of ∃r3.⊺. Suppose that we want to add (I1,d1) to the models of ∃r3.⊺. In EL, however, every concept satisfied by (I1,d1) and mod(∃r3.⊺) is also satisfied by (I2,d1). There is no concept separating (I2,d1) from mod(∃r3.⊺)∪{(I1,d1)}. Example 6. Let B = {∃r.⊺} be an EL concept and let the signature be NC = {A},NR = {r}. We want to evict the pointed model (I,d) with ∆I = {d}, rI = {(d,d)}, and AI = ∅. We have that (I,d) satisfies B. The removal of (I,d) from mod(B) yields the base B′ = {∃r.A,∃r2.A,⋯,∃rn.A,⋯}, which is not finitely representable.

On both cases 1 and 2, as illustrated respectively on Ex. 5 and Ex. 6, extra models must be added/removed to achieve a finite base. Such addition/removal should be minimised, so only models that do contribute to reaching finiteness are considered. In this case, a “closest” finite base is produced. Such minimality criteria are properly addressed in the form of rationality postulates. The appropriate class of all eviction/reception operators abiding by such postulates are identified. We show that in several classes of models, the minimality principles cannot be guaranteed, which is due to the non-existence of a “closest” finite base, known as the compatibility problem (Guimar˜aes, Ozaki, and Ribeiro 2023). We briefly review reception and eviction, respectively, on Sec. 3.1 and Sec. 3.2.

## 3.1 Reception

We denote belief change operators related to reception as rcp. Guimar˜aes, Ozaki, and Ribeiro (2023) proposed the following rationality postulates to govern reception

(success) M ⊆mod(rcp(B,M)) (persistence) mod(B) ⊆mod(rcp(B,M)) (finite temperance) M′ /∈FR(Λ), if mod(B)∪M ⊆M′ and M′ ⊂mod(rcp(B,M)) (uniformity) mod(rcp(B,M)) = mod(rcp(B′,M′)), if MinFRSups(mod(B) ∪M,Λ) = MinFRSups(mod(B′) ∪ M′,Λ).

Success ensures that each model from M must be incorporated. The purpose of reception is to accommodate new models. Persistence ensures that no model is removed in the process. Finite temperance ensures that the addition of extra models is minimized, adding only models that contribute to reaching a finite base. Uniformity ensures that reception is neither syntax sensitive nor sensitive to model structure. For instance, in Ex. 5, the pointed interpretation (I1,d1) cannot be separated from (I2,d1) in the presence of the models of B, so reception, on B, of the sets {(I1,d1)} and {(I1,d1),(I2,d1)} must coincide.

A reception operator on a class C of models is a model change operator rcp ∶℘f(L)×C →℘f(L) that satisfies success. A reception operator satisfying all rationality postulates is called rational. When there is no finite base for mod(B)∪M, some further models must be added in favor of finiteness.

19323

<!-- Page 4 -->

Such extra removal must be minimized as finite-temperance demands. This corresponds to picking a least finitely representable superset of mod(B)∪M, that is, picking a set from MinFRSups(mod(B) ∪M,Λ). However, for some classes of models, such a least finitely representable superset does not exists, that is, MinFRSups(mod(B) ∪M,Λ) is empty. In such cases, therefore, finite-temperance cannot be satisfied, which implies in the inexistence of rational reception operators. Classes of models in which such least finitely representable supersets exist are called reception-compatible. Definition 7. A class C of models on a satisfaction system Λ, is reception-compatible iff for all M ∈C and base B ∈℘f(L), MinFRSups(mod(B)∪M,Λ) ≠∅.

Several classes of all models are not reception-compatible, as we show in Sec. 4. For instance, in the DL EL, the class of all its models is not reception compatible, as Ex. 8 illustrates. Example 8. Consider the concept in EL and a signature with NR = {r}. Suppose M+ = {(M∞,0)} (see def. in Sec. 2). We would like to include an interpretation pointed at an infinite chain but we are not asking the finite chains Mn to be included. There is no EL concept that best represents adding this set to. Given a concept ∃rn.⊺one can always create another concept ∃rn+1.⊺that includes M+ but has strictly less models: mod(∃r.⊺) ⊃mod(∃r2.⊺) ⊃⋯⊃mod(∃rn.⊺) ⊃⋯.

Ex. 9 illustrates a reception operation. Example 9. (continued from Ex. 5). Recall we want the reception of ∃r3.⊺with (I1,d1). Both ∃r2.⊺and ∃r.⊺. are more general than ∃r3.⊺. From these, the closest that contains (I1,d1) is ∃r.⊺. So, rcp({∃r3.⊺},{(I1,d1)}) = {∃r.⊺}.

On reception-compatible classes of models, Guimar˜aes, Ozaki, and Ribeiro (2023) have proposed the family of maxichoice reception operators, which chooses one finitely representable base from MinFRSups. Maxichoice reception operators coincide with all rational reception operators.

## 3.2 Eviction

Eviction operators, denoted by evc, are governed by the following postulates: (success) M∩mod(evc(B,M)) = ∅. (inclusion) mod(evc(B,M)) ⊆mod(B). (finite retainment) M′ /∈FR(Λ), if mod(evc(B,M)) ⊂M′ and M′ ⊆mod(B)∖M. (uniformity) mod(evc(B,M)) = mod(evc(B′,M′)), if MaxFRSubs(mod(B) ∖M,Λ) = MaxFRSubs(mod(B′) ∖ M′,Λ)

Success ensures that each model from M must be relinquished. As the purpose of eviction is to remove models, inclusion ensures that no models are added. Uniformity, as for reception, guarantees that eviction is neither syntax sensitive nor sensitive to model structure. Finite retainment ensures that the removal of extra models is minimized, retracting only models that contribute to reaching a finite base. An eviction operator on a class C of models is a model change operator evc ∶℘f(L)×C →℘f(L) that satisfies success.

An eviction operator satisfying all rationality postulates is called rational. In the best scenario, to evict a set of models

M from a finite base B, one would simply identify a base for the set mod(B)∖M. However, as not all sets of models are finitely representable, some further models must be minimally removed in favour of finiteness, as finite-retainment demands. This corresponds to picking a greatest finitely representable subset from mod(B) ∖M, that is, picking a set from MaxFRSubs(mod(B)∖M,Λ). This set, in general, is not a singleton, and a choice must be made among the most plausible candidates. The choice, as for reception, is realised by a choice function. Similarly to reception, depending on the underlying class C of models, MaxFRSubs(mod(B)∖M,Λ) might be empty. In such a case, finite retainment cannot be satisfied, which means that in such classes rational eviction operators do not exist. Classes of models in which the greatest finitely representable subsets exist are called evictioncompatible. Definition 10. A class C of models, on a satisfaction system Λ, is eviction-compatible iff for all M ∈C and base B ∈℘f(L), MaxFRSubs(mod(B)∖M,Λ) ≠∅.

On eviction-compatible classes of models, Guimar˜aes, Ozaki, and Ribeiro (2023) have proposed the family of maxichoice eviction operators, which chooses one finitely representable base from FR. Maxihoicde reception operators are characterised by all rationality postulates of reception.

Eviction and Reception: DL Concepts Here we investigate eviction and reception on DL concepts, focusing on the prototypical DLs ALC and EL. In the following, we denote by Λ(EL concepts) and Λ(ALCconcepts) the satisfaction systems for EL and ALC concepts with pointed interpretations as models. Table 1 summarises our results.

Sat. System Eviction Reception

Λ(EL con.) yes (Thm. 11) no (Thm. 13) Λ(EL con.)† yes (Thm. 11) yes (Thm. 14)

Λ(ALCcon.) no (Thm. 12) no (Thm. 13) Λ(ALCcon.)‡ yes (Thm. 16) yes (Thm. 16)

**Table 1.** Eviction and reception-compatibility for DL concepts. † is for the case pointed interpretations can only be tree-shaped and ‡ is for the case they can only be tree-shaped, over finite signatures, and sets of models can only be finite.

Theorem 11. Λ(EL concepts) is eviction-compatible.

Theorem 11 does not hold for EL (without) as any language that cannot express inconsistencies is not evictioncompatible (Guimar˜aes, Ozaki, and Ribeiro 2023). We also do not have eviction-compatibility for ALC. Theorem 12. Λ(ALCconcepts) is not eviction-compatible.

The next theorem establishes that reception-compatibility neither holds for EL nor for ALC concepts. Theorem 13. Λ(EL concepts) and Λ(ALCconcepts) are not reception-compatible. This holds even if we restrict to the class of (possibly infinite) sets of (possibly infinite) treeshaped pointed interpretations or if we restrict to the class of sets of pointed interpretations over a unique finite signature.

19324

<!-- Page 5 -->

We now concentrate on finding a restricted class of concepts where reception-compatibility holds.

Theorem 14. Λ(EL concepts) is reception-compatible in the class of (possibly infinite) sets of finite tree-shaped pointed interpretations (over a possibly infinite signature).

Thm. 12 and Thm. 13 compel us to investigate more restricted classes of models to obtain a positive result for ALC. There are two natural ways of restricting this class: restricting to finite sets of finite tree-shaped interpretations or to finite tree-shaped interpretations with finite signature. The next theorem establishes that these restrictions alone are not sufficient ALC reception-compatibility.

Theorem 15. Λ(ALCconcepts) is neither receptioncompatible in the class of finite sets of finite tree-shaped pointed interpretations over a (possibly infinite) signature; nor in the class of (possibly infinite) sets of finite tree-shaped pointed interpretations over a (unique) finite signature.

Theorem 16. Λ(ALCconcepts) is reception-compatible and eviction-compatible in the class of finite sets of finite treeshaped pointed interpretations over any finite signature.

## Model

Revision In this section, we introduce a new kind of model change operation, which we call model revision. Model revision incorporates a set of models while also guaranteeing that another set of models is removed. For instance, in Ex. 3, (I4,d′′) had to be removed, while (I5,d′′) had to be added. Revision cannot be defined by assembling reception and eviction, as reception can add models required to be evicted and vice versa. For revision, we consider change operators defined on a class C ⊆℘(M)×℘(M) of pairs of models. A class of pairs of models is called a binary class.

Example 17. Let B = {∃r.⊺} be an EL concept on the signature NC = {A} and NR = {r}. Let (I1,d1) and (I2,d1) be pointed models with ∆I1 = {d1,d2},∆I2 = {d1,d2,d3} and

I1 ∶AI1 = {d2},rI1 = {(d1,d2)}

I2 ∶AI2 = {d1},rI2 = {(d1,d2),(d2,d3)}

We want to revise B with ({(I1,d1)},{(I2,d1)}), that is, re- ceive (I1,d1) and evict (I2,d1). Combining rational eviction with rational reception, in any order, is not strong enough to achieve revision. A rational eviction of B with (I2,d1) is B′ = {∃r3.⊺}. However, incorporating (I1,d1) to it yields the base {∃r.⊺} again, which contains (I2,d1). On the other hand, reception of B with (I1,d1) does not change B, as (I1,d1) is a model of ∃r.⊺. Eviction of B with (I2,d1) gives ∃r3.⊺, which does not contain (I1,d1).

Definition 18. A revision operator, on a binary class C, is function rev ∶℘f(L)×C →℘f(L) which satisfies the postulate success M−∩mod(rev(B,M+,M−)) = ∅and M+ ⊆ mod(rev(B,M+,M−)).

For clarity, we denote M−as the set of models to be removed, while M+ denotes the set of models to be added.

Success guarantees that all models in M−are removed while all models in M+ are added. Clearly, one cannot demand to add and remove the same model. Success cannot be satisfied for (B,M+,M−), if M+ and M−are not disjoint. Unfortunately, the possibility of success goes beyond identifying whether or not M+ and M−are disjoint. It depends on the logic’s underlying satisfaction system. For example, for ALC concepts, models are closed under bisimulation (Goranko and Otto 2007; Blackburn, van Benthem, and Wolter 2007), which means that some distinct but bisimilar pointed interpretations (I1,d1) and (I2,d2) satisfy precisely the same formulae. Thus, a revision that demands incorporation of (I1,d1) and removal of (I2,d2) cannot occur. For success, revision must at least be defined on classes of pairs of models in which incorporating M+ does not conflict with eliminating M−. We call such classes revision-realisable. Definition 19. A binary class of models C is revisionrealisable iff for all (M+,M−) ∈C, there is a finitely representable set M of models such that M+ ⊆M and M−∩M = ∅.

For conciseness, unless otherwise explicitly stated, we assume that all binary classes of models are revision-realisable. Success alone is not enough to bring rationality to revision. We introduce other rationality postulates to capture the minimal change principle for revision. We start with vacuous-expansion: if M+ ⊆ mod (B) then mod(rev(B,M+,M−)) ⊆mod (B), vacuous-removal: if M−∩mod (B) = ∅then mod (B) ⊆ mod(rev(B,M+,M−)).

If all models of M+ are models of B, one should only evict M−(vacuous expansion). On the other hand, if none of the models in M−satisfy B (vacuous removal), all we need to do is to add models. If all models in M+ satisfy B, and none of M−violate B, the base B should be left untouched. We call this lethargy.

lethargy: if M+ ⊆mod(B) and M−∩mod(B) = ∅, then rev(B,M+,M−) = mod(B).

Proposition 20. If a revision operator satisfies vacuousexpansion and vacuous-removal then it satisfies lethargy.

These three postulates capture the most fundamental features of revision. Yet, such postulates are not enough, as they allow for drastic removal and addition of models. For example, if some of the models in M+ does not satisfy B and some model in M−violates B then vacuous-expansion and vacuous-removal allow the removal of all models of B. However, ideally, changes should be minimised.

In the case that the trivial removal of M−and the trivial addition of M+ reach a finitely representable set M, the revision should correspond to M as finiteness is trivially obtained. However, if finiteness is not reached in this way, then one must remove and add some extra interpretations in favour of finiteness. Such additions and removals must be minimised. Such a minimal change principle is conceptualised in the form of the circumspection postulate.

circumspection: if X+,X−∈C are disjoint sets and condi- tions (1) to (3) below are jointly satisfied, then condition (4) is satisfied:

19325

<!-- Page 6 -->

1. X−⊆(mod(B) ∖mod(rev(B,M+,M−)), and M−∩ mod(B) ⊆X−

2. M+ ∖mod(B) ⊆X+ ⊆(mod(rev(B,M+,M−)) ∖ mod(B) and 3. ((mod(B)∖X−)∪X+) ≠mod(rev(B,M+,M−)

4. ((mod(B)∖X−)∪X+) /∈FR(Λ).

In circumspection above, the set X−(condition 1) denotes the extra interpretations to be removed, while X+ (condition 2) denotes the extra interpretations to be added during revision. These extra additions and removals can only occur in favour of finiteness, and all of them must be necessary to achieve finiteness. Therefore, every smaller combination of removals or additions to form a revision candidate (condition 3) does not reach finiteness (condition 4). The postulate circumspection captures lethargy. Proposition 21. If a revision operator satisfies circumspection then it satisfies lethargy.

Defining operators capable of satisfying principles of minimal change has been proved a challenge in the field of belief change. In some logics, operators satisfying minimal change principles cannot even be defined (Flouris 2006; Ribeiro, Nayak, and Wassermann 2018; Guimar˜aes, Ozaki, and Ribeiro 2023). This occurs due to the strong semantics and properties of the logics. Guimar˜aes, Ozaki, and Ribeiro (2023) have shown that in some logics satisfaction systems, eviction and reception do not exist. For revision, this would not be different. We shall direct the effort of defining revision operators to classes of models that are compatible with such rationality postulates. Definition 22. A binary class C is revision-compatible iff there is a revision operator on C satisfying success, vacuousexpansion, vacuous-removal and circumspection.

Given that we are working on a binary class of models that is revision-compatible, we would like to know how to construct a revision operator satisfying all the rationality postulates presented so far. We will frame the precise class of operators that satisfy such postulates. For this, we need to define some auxiliary tools. Let χΛ(M+,M−) = {Y ∈FR(Λ) ∣M+ ⊆Y and M−∩Y = ∅}, be the set which contains exactly all finite bases satisfied by all models in a given set M+ but violated by all models in M−. One can regard χΛ(M+,M−) as the set of all potential candidates to revise a base with the pair (M+,M−).

Not all sets in χΛ(M+,M−), however, are suitable to revise a given base B, as some of them might add or remove more than allowed by circumspection. If we could “measure” the changes incurred on mod(B) to achieve a finite representable set of models, then we can just select the finite representable sets with the minimal incurred changes. The symmetric difference between two sets A and B provide exactly the changes necessary to turn one set into another. To turn a set A into a set B, we need only to add the elements of B that are not in A, and remove the elements in A that are not in B. We can, therefore, use the symmetric difference to “measure” changes between sets of interpretations, and choose those that minimise the changes. On each set of interpretations M, we define the relation ⪯M⊆℘(M)×℘(M), such that M1 ⪯M M2 iff (M⊕M1) ⊆(M⊕M2).

Intuitively, M1 ⩽M M2 means that turning M into M2 incurs in at least as much change as turning M into M1. This means that turning M into M1 is equally cheap or cheaper than turning M to M2. We can use this closeness relation to revise a base B by a pair (M+,M−). As the revision must minimise the changes, we choose, from χΛ(M+,M−), one of the closest options to mod(B) that is, one from min⪯mod(B)(χΛ(M+,M−)). To define a revision function using this strategy, we need the condition that for every base B and pair (M+,M−), there is at least one choice on min⪯(χΛ(M+,M−)), that is, the symmetric difference indeed minimises the distance from the base to the revision candidates. This condition follows from revision-compatibility. Theorem 23. If C is revision-compatible, then for all finite base B and (M+,M−) ∈C, min⪯mod(B)(χΛ(M+,M−)) ≠∅.

We get revision operators from symmetric difference. Definition 24. A na¨ıve relational revision operator, on a binary class of models C, is a map rev⊕∶℘f(L)×C →℘f(L) s.t. mod(rev⊕ sel(M+,M−)) ∈min⪯mod(B)(χΛ(M+,M−)).

The na¨ıve operator minimises the distance between the models of a base B′ to all bases satisfied by M+ and violated by all models in M−. Indeed, the na¨ıve revision operators is strongly connected with circumspection. Theorem 25. A revision operator satisfies circumspection iff it is a na¨ıve relational revision operator.

Although na¨ıve revision operators capture circumspection, they are too weak to satisfy vacuous-removal and vacuousexpansion, as Ex. 26 illustrates. Example 26. Let B = (B⊓C) be an EL concept and consider the interpretations Ii = (∆Ii,⋅Ii), with i ∈{1,2,3,4}, where ∆Ii = {d}, and each ⋅Ii is as follows.

AI1 = {d}

BI1 = ∅

CI1 = {d}

AI2 = ∅

BI2 = ∅

CI2 = ∅

AI3 = ∅

BI3 = ∅

CI3 = {d}

AI4 = ∅

BI4 = {d}

CI4 = {d}

By definition, (I4,d) is a model of B = (B ⊓C). Assume we want to revise B with ({(I1,d)},{(I2,d)}), that is, accommodate (I1,d) while relinquishing (I2,d). Since d /∈ (B ⊓C)I2, according to vacuous-removal, we should only add models to B. Adding only (I1,d) is not possible, because (I4,d) is a model of B and every EL concept satisfied by both (I4,d) and (I1,d) is also satisfied by (I3,d). So, every revision satisfying vacuous-removal contains the set {(I1,d),(I3,d),(I4,d)}. This corresponds to revising B = (B ⊓C) to C. If we want to avoid adding (I3,d), we could remove (I4,d), violating vacuous-removal, and staying only with (I1,d). So, a na¨ıve revision operator can output (A⊓C) as a solution for revising (B⊓C).

In Ex. 26, vacuous-removal is violated, as the operator removes further models from B when M−does not violate B. Also, when M+ satisfies B, the na¨ıve operator allows adding further models. We strengthen the na¨ıve operator.

19326

<!-- Page 7 -->

Definition 27. A symmetric-differential revision function on a binary class C of models, is a function rev ∶ ℘f(L) × C →℘f(L), such that for all (M+,M−) ∈C, mod(rev(B,M+,M−)) = M where,

(i) if M+ ⊆mod(B), then

M ∈min⪯mod(B)(χΛ(M+,M−∪(M∖mod(B))))

(ii) if M+ /⊆mod(B), but M−∩mod(B) = ∅, then

M ∈min⪯mod(B)(χΛ(M+ ∪mod(B),M−))

(iii) otherwise, M ∈min⪯mod(B)(χΛ(M+,M−)).

For case (i), when M+ satisfies the base, according to vacuous-expansion, no interpretation can be incorporated. This corresponds to enforcing all counter models of B to be removed jointly with M−. For case (ii), analogous to case (i), whenever all models of M−violate B, as per vacuousremoval, no model of B should be removed. This corresponds to enforcing all models of mod(B) to be incorporated jointly with M+. As for case (iii), the cases (i) and (ii) give enough protection to vacuous-removal and vacuousexpansion. Hence, in any other case, we can just perform a na¨ıve revision. The symmetric-differential revision operators are characterised by the rationality postulates of revision. Theorem 28. A revision operator rev satisfies success, vacuous-expansion, vacuous-removal and circumspection iff it is a symmetric differential revision operator.

Revision-compatibility is tightly connected to both reception-compatibility and eviction-compatibility. In the case that M−is empty, revising a base with (M+,M−) intuitively corresponds to performing a reception, as vacuousremoval would forbid removal of interpretations. Analogously, if M+ is empty, then revising with (M+,M−), with a non-empty M−, would correspond to evicting M−, as vacuous-expansion would forbid adding interpretations. From this perspective, we can trace an important connection between revision-compatibility with eviction-compatibility and reception-compatibility. To establish this connection, the underlying class of models must cover the cases that we can perform revision of the kind (M+,∅) and (∅,M−), that is, cover the possibility of solely adding or removing interpretations. We call such classes decomposable classes of models. Definition 29. A binary class of models C is decomposable iff for all (M+,M−) ∈C, (M+,∅) ∈C and (∅,M−) ∈C.

Given a binary class of models C, let C+ = {M+ ∈M ∣ (M+,M−) ∈C}, and, C−= {M−∈M ∣(M+,M−) ∈C}. The set C+ is the greatest subclass of C with reception candidates, whereas C−is the largest subclass with eviction candidates. Every rational revision operator induces an eviction and a reception operator. Consequently, compatibility of revision implies compatibility with both reception and eviction. Theorem 30. Let C be a decomposable revision-compatible binary class of models. The following hold for C. 1. C+ is reception-compatible and C−is eviction-compatible. 2. If evc is a eviction operator on C−, then there is a revision operator rev on C satisfying all rationality postulates such that evc(B,M−) = rev(B,∅,M−).

3. If rcp is a reception operator on C+, then there is a revision operator rev on C satisfying all rationality postulates such that rcp(B,M+) = rev(B,M+,∅).

From Thm. 30, eviction and reception are special cases of revision, whereas revision can only be performed in classes of models compatible with both reception and eviction. This connection between revision with eviction and reception allows to translate (in)compatibility results from eviction and reception to revision, as we see in Sec. 6.

## 6 Revision: DL Concepts

Here, we briefly consider the revision of DL concepts. It follows from Thm. 30 and the results in Table 1 that neither Λ(EL concepts) nor Λ(ALCconcepts) are, in general, revisioncompatible. We establish that these satisfaction systems are also not revision-compatible when we restrict to finite treeshaped pointed interpretations.

Theorem 31. Λ(EL concepts) and Λ(ALCconcepts) are not revision-compatible in the binary class of finite tree-shaped pointed interpretations. This also holds if we restrict to finite sets of models and if we restrict to a finite signature.

So we restrict the binary class of models that we consider even further. We consider the binary class of finite tree-shaped pointed interpretations for finite sets of models union their closure under bisimulation over a finite signature. We argue that this class is revision-compatible. We say that two sets of pointed interpretations are bisimulation disjoint iff there is no pointed interpretation in one of the sets that is bisimilar to a pointed interpretation in the other set.

Theorem 32. Λ(ALCconcepts) is revision-compatible in the binary class of sets of pointed interpretations which are the closure under bisimulation of finite sets of finite tree-shaped pointed interpretations over a (unique) finite signature.

Regarding the case of EL, we do not have the same expressivity we have in ALC for restricting the models that are satisfied by a concept. We leave it as an open question. From the positive results for eviction and reception for certain classes of models for EL and ALC in Table 1, we obtain the existence of the revision operators in Thm. 30.

## Conclusion

We investigated eviction and reception for DL concepts, establishing various results considering different classes of models. We find classes of models where we obtain eviction and reception compatibility for both ALC and EL concepts. It turns out that the class of models where we obtain positive results for ALC is much more restricted than the class for EL. We also introduce the notion of model revision and relate various postulates with the revision operation. Revision cannot be seen as a mere combination of eviction and reception, which is evidenced by negative results for DL concepts. As future work, it would be interesting to investigate model eviction, reception, and revision of DL concepts in a more practical setting, expand our work to more expressive DLs.

19327

<!-- Page 8 -->

## Acknowledgments

Ozaki is supported by the Research Council of Norway, project (316022, 322480). This work was also supported by the Research Council of Norway, Integreat - Norwegian Centre for knowledge-driven machine learning (332645).

## References

Agi, K.; Wolter, F.; Zakharyaschev, M.; and Gabbay, D. 2003. Many-dimensional modal logics: theory and applications. Amsterdam Boston: Elsevier North Holland. ISBN 0444508260. Aiguier, M.; Atif, J.; Bloch, I.; and Hudelot, C. 2018. Belief revision, minimal change and relaxation: A general framework based on satisfaction systems, and applications to description logics. Artificial Intelligence, 256: 160–180. Alchourr´on, C. E.; G¨ardenfors, P.; and Makinson, D. 1985. On the Logic of Theory Change: Partial Meet Contraction and Revision Functions. Journal of Symbolic Logic, 50(2): 510–530. Baader, F.; Horrocks, I.; Lutz, C.; and Sattler, U. 2017. An Introduction to Description Logic. Cambridge University Press. ISBN 978-0521695428. Baader, F.; Sertkaya, B.; and Turhan, A. 2007. Computing the least common subsumer w.r.t. a background terminology. J. Appl. Log., 5(3): 392–420. Baltag, A.; Gierasimczuk, N.; ¨Ozg¨un, A.; Sandoval, A. L. V.; and Smets, S. 2019. A dynamic logic for learning theory. J. Log. Algebraic Methods Program., 109. Baltag, A.; Gierasimczuk, N.; and Smets, S. 2019. Truth- Tracking by Belief Revision. Stud Logica, 107(5): 917–947. Blackburn, P.; van Benthem, J. F. A. K.; and Wolter, F., eds. 2007. Handbook of Modal Logic, volume 3 of Studies in logic and practical reasoning. North-Holland. ISBN 978-0- 444-51690-9. De Raedt, L. 1997. Logical settings for concept-learning. Artificial Intelligence, 95(1): 187–201.

Delgrande, J. P.; Peppas, P.; and Woltran, S. 2018. General Belief Revision. J. ACM, 65(5): 29:1–29:34. Dummett, M. A. E.; and Lemmon, E. J. 1959. Modal Logics Between S 4 and S 5. Mathematical Logic Quarterly, 5(14- 24): 250–264. Fanizzi, N.; d’Amato, C.; and Esposito, F. 2008. DL-FOIL Concept Learning in Description Logics. In Zelezn´y, F.; and Lavrac, N., eds., ILP, volume 5194 of Lecture Notes in Computer Science, 107–121. Springer. Flouris, G. 2006. On belief change in ontology evolution. AI Communications, 19(4): 395–397. Funk, M.; Jung, J. C.; and Lutz, C. 2021. Actively Learning Concepts and Conjunctive Queries under ELr-Ontologies. In Zhou, Z., ed., IJCAI, 1887–1893. ijcai.org. Funk, M.; Jung, J. C.; Lutz, C.; Pulcini, H.; and Wolter, F. 2019. Learning Description Logic Concepts: When can Positive and Negative Examples be Separated? In Kraus, S., ed., IJCAI, 1682–1688. ijcai.org.

G¨ardenfors, P. 1988. Knowledge in flux: Modeling the dynamics of epistemic states. The MIT press. Goranko, V.; and Otto, M. 2007. Model theory of modal logic. In Blackburn, P.; van Benthem, J. F. A. K.; and Wolter, F., eds., Handbook of Modal Logic, volume 3 of Studies in logic and practical reasoning, 249–329. North-Holland. Guimar˜aes, R.; Ozaki, A.; and Ribeiro, J. S. 2023. Finite Based Contraction and Expansion via Models. In AAAI, 6389–6397. Hansson, S. O. 1999. A Textbook of Belief Dynamics: Theory Change and Database Updating. Applied Logic Series. Kluwer Academic Publishers. Iannone, L.; Palmisano, I.; and Fanizzi, N. 2007. An algorithm based on counterfactuals for concept learning in the Semantic Web. Appl. Intell., 26(2): 139–159. Klarman, S.; and Britz, K. 2015. Ontology Learning from Interpretations in Lightweight Description Logics. In Inoue, K.; Ohwada, H.; and Yamamoto, A., eds., ILP, volume 9575 of Lecture Notes in Computer Science, 76–90. Springer. Konev, B.; Lutz, C.; Wolter, F.; and Zakharyaschev, M. 2016. Conservative Rewritability of Description Logic TBoxes. In Kambhampati, S., ed., IJCAI, 1153–1159. IJCAI Press. Lehmann, J. 2009. DL-Learner: Learning Concepts in Description Logics. J. Mach. Learn. Res., 10: 2639–2642. Lehmann, J.; and Haase, C. 2009. Ideal Downward Refinement in the EL Description Logic. In Raedt, L. D., ed., ILP, volume 5989 of Lecture Notes in Computer Science, 73–87. Springer. Lehmann, J.; and Hitzler, P. 2010. Concept learning in description logics using refinement operators. Mach. Learn., 78(1-2): 203–250. Ozaki, A.; and Troquard, N. 2019. Learning Ontologies with Epistemic Reasoning: The E\!L Case. In Calimeri, F.; Leone, N.; and Manna, M., eds., JELIA, volume 11468 of Lecture Notes in Computer Science, 418–433. Springer. Ribeiro, J. S.; Nayak, A.; and Wassermann, R. 2018. Towards Belief Contraction without Compactness. In KR 2018, 287– 296. AAAI Press. Schwind, N.; Inoue, K.; Konieczny, S.; and Marquis, P. 2025. Iterated Belief Change as Learning. In IJCAI, 4669–4677. ijcai.org. ten Cate, B.; Koudijs, R.; and Ozaki, A. 2024. On the Power and Limitations of Examples for Description Logic Concepts. In IJCAI, 3567–3575. ijcai.org.

19328
