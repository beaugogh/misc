---
title: "Foundations of Formal Reasoning over Knowledge Bases Combining Symbolic and Sub-Symbolic Knowledge"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38971
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38971/42933
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Foundations of Formal Reasoning over Knowledge Bases Combining Symbolic and Sub-Symbolic Knowledge

<!-- Page 1 -->

Foundations of Formal Reasoning over Knowledge Bases

Combining Symbolic and Sub-Symbolic Knowledge

Gianluca Cima, Marco Console, Laura Papi

Sapienza University of Rome {cima, console, papi}@diag.uniroma1.it

## Abstract

More and more organizations are relying on Machine Learning (ML) models to support internal decision-making processes. To better support such processes, it would be highly beneficial to contextualize the inductively acquired knowledge encoded in these models and enable formal reasoning over it. Despite significant progress in Neuro-Symbolic AI, this specific challenge remains largely under-explored. We propose a framework that allows to integrate the knowledge induced by ML classifiers with the knowledge specified by logic-based formalisms. The framework is based on the novel notion of Hybrid Knowledge Base (HKB), consisting of two components: an ontology and a set of ML binary classifiers. As usual, the ontology provides an intensional representation of the modeled domain through logic-based axioms, while the binary classifiers implicitly encode the extensional knowledge. Specifically, a HKB associates to each concept and role mentioned in the ontology a classifier based on a set of features deemed to be relevant for the application domain, thereby virtually populating the concepts and roles with the instances and pairs of instances from the feature space. Besides the definition of the new framework, as a more technical contribution we show how to reason in this framework by studying query answering over HKBs. In particular, we investigate the computational complexity of query answering in a rich language over HKBs in which the ontology is specified in (the Description Logic counterpart of) RDFS, while the binary classifiers are represented by Multi-Layer Perceptrons.

## Introduction

In recent years, information represented by Machine Learning (ML) models (Bishop 2007; Hastie, Tibshirani, and Friedman 2009) is increasingly prominent in Information Systems (Chen, Chiang, and Storey 2012). Techniques leveraging such information are regularly employed in the most diverse application domains, such as finance, healthcare, and law, and have demonstrated strong empirical success in a variety of concrete tasks (Jiang et al. 2017; Bahoo et al. 2023).

Despite their remarkable successes, ML models still exhibit significant limitations that hinder their adoption in mission-critical settings (Thames and Sun 2024). A key limitation lies in the restricted form of interaction they offer. At

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

a high level, an ML model is (the representation of) a function M: A →B, and typically, the only query that a user can pose to M is value computation, i.e. given a ∈A, return the output M(a) ∈B. While such point-wise (local) access underpins many successful stories of ML-based techniques, numerous crucial tasks implicitly demand a global view of the information encoded by M, which remains difficult to access (K¨onig et al. 2024). In general, it would be very useful to put the inductively acquired knowledge contained in these models into context and formally reason over it, ideally by combining such knowledge with a logical specification of the domain of interest over which these ML models operate. Despite the great effort in recent years on Neural Symbolic AI systems, this specific problem remains under-explored.

In this paper, we propose a novel logical framework that enables the integration of knowledge induced by ML classifiers with knowledge specified by logic-based formalisms. Our framework falls under the general category of Ontology-Driven Knowledge Bases. The core principle of this paradigm is to represent knowledge via two complementary components: an intensional part and an extensional part. The intensional part, specified through an ontology (also referred to as TBox), comprises the vocabulary, i.e. the involved concepts and roles, and a set of axioms expressed in some formal language that constrain their interrelations, providing a semantically rich intensional representation of the modeled domain. The extensional part refers to the actual data, specifying which objects (resp. pairs of objects) are instances of concepts (resp. roles). Depending on the use case, the extensional component of an Ontology-Driven Knowledge Base methodology can take different forms. For example, in Ontology-Mediated Query Answering setting (Bienvenu and Ortiz 2015), it is realized as an ABox, whereas in the Virtual Knowledge Graph (VKG) paradigm (Xiao et al. 2019) (originally termed Ontology-Based Data Access (OBDA) (Poggi et al. 2008)) it consists of a relational database together with mappings that link the underlying database schema to the concepts and roles in the ontology.

In our novel framework, we introduce a further method to define the extensional component, which leverages ML models. We consider the typical scenario in which an application domain has a set of relevant features over which ML models operate. The framework is based on the notion of a Hybrid Knowledge Base (HKB), consisting of two compo-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

18994

<!-- Page 2 -->

nents: an ontology and a set of ML binary classifiers. The former conceptualizes the application domain, while the latter assigns to each concept (resp. role) in the ontology vocabulary a classifier (resp. classifiers over pairs) trained on the relevant features of the domain, thereby virtually specifying the extension of concepts (resp. roles) with feature space elements (resp. pairs of feature space elements).

Example 1. Consider a medical scenario exploiting classifiers to determine whether a patient is diabetic (classifier κD), male (κM), or pregnant (κP), as well as whether a pair of patients are compatible blood donors (classifier over pairs λcD) or share a compatible blood type (λcB).

In our framework, we can place this inductively obtained knowledge within a semantic context. Specifically, we model the above scenario through an ontology O, and by assigning to each concept and role in the ontology’s vocabulary its corresponding classifier. The vocabulary of O consists of the atomic concepts D, M, and P for diabetics, males, and pregnant patients, respectively, and the atomic roles cD and cB for pairs of patients that are compatible donors and pairs of patients with compatible blood types, respectively. The background knowledge of O sanctions that pregnant patients cannot be male (P ⊑¬M). Finally, the HKB is composed by O and the set of classifiers described above, where κC is assigned to the atomic concept C (for C ∈{D, M, P}) and λR is assigned to the atomic role R (for R ∈{cD, cB}).

As in a VKG system, the extensional knowledge of a HKB is defined implicitly. In particular, it is encoded in the classifiers assigned to the concepts and roles of the ontology, whose extensions are fully determined by these classifiers.

We provide a model-theoretic semantics for HKBs. An interpretation for a HKB K is a pair (I, f), where I is a standard first-order interpretation over the ontology vocabulary, and f is a function that maps each feature space element (i.e. each input to the classifiers) to a (possibly empty) set of objects from the domain ∆I of I. This reflects the assumption that each feature space element ¯a either corresponds to a combination of attribute values that no real-world entity can exhibit (f(¯a) = ∅) or corresponds to one or more entities sharing exactly those characteristics. The models of a HKB K are those interpretations (I, f) such that I satisfies the ontology axioms, and the extension of each concept and role in the ontology vocabulary exactly follows the classification defined by the corresponding classifier via the mapping f.

Due to the presence of ontology axioms, there will be feature space elements discarded by HKB models. For instance, consider the axiom P ⊑¬M in Example 1, and let ¯a be a feature space element simultaneously classified positively by κP and κM (i.e. κP(¯a) = κM(¯a) = 1). In this case, every model of the HKB must discard ¯a, i.e. set f(¯a) = ∅. Clearly, it is desirable to discard feature space elements only when necessary, so as to maximize coverage of the feature space and, consequently, preserve as much information as possible from the application of the employed ML classifiers to the sub-symbolic data. For this reason, we introduce the notion of minimally-discarding models, which are models that discard a ⊆-minimal set of feature space elements.

Importantly, our model-theoretic semantics enables the possibility to formally reason over the combination of symbolic and sub-symbolic knowledge within a HKB. It provides a foundation for studying classical reasoning tasks from the Knowledge Representation and Reasoning tradition over knowledge acquired through symbolic and inductive techniques, with users interacting via the ontology layer, as is typical of any ontology-driven methodology. In this paper, we focus on two reasoning tasks: non-trivial consistency checking and query answering. The former checks whether there exists a model that does not discard all elements of the feature space, which is a key reasoning task for assessing whether the ML classifiers contribute any meaningful information, assuming, as usual, that the ontology is flawless and error-free. The latter is arguably one of the most studied tasks in symbolic reasoning, serving as a mechanism to extract information from the various (preferred) models of the knowledge encoded within an application domain.

Besides the novel framework, the other main contribution of this paper is a thorough computational complexity analysis of the aforementioned reasoning tasks over HKBs in a meaningful setting. We consider the Description Logic (DL) DL-Lite¬

RDFS as the ontology language and unions of conjunctive queries with inequalities (UCQ̸=s) as the query language. This setting has been the subject of recent thorough investigations in the ontology-mediated query answering literature (see (Cima, Lenzerini, and Poggi 2020; Cima et al. 2025)). The DL DL-Lite¬ RDFS corresponds to the DL counterpart of RDFS (often called DL-LiteRDFS (Cuenca Grau 2004; Rosati 2007)) extended with disjointness axioms, while the query language is the well-known union of conjunctive queries extended with inequality atoms. For the classifiers, we consider Multi-Layer Perceptrons (MLPs), a widely used class for classification tasks over structured data.

Similarly to the so-called data complexity which assumes that both the ontology and the query (if applicable) are fixed, we focus on the classifiers complexity, i.e. the complexity in which only the set of classifiers is regarded as the input. We show that non-trivial consistency checking is NP-complete, whereas query answering is significantly more intractable, and more specifically CONEXPTIME-complete. Due to this latter negative result, we explore both a restricted setting and an alternative semantics for query answering. The restricted setting forbids the use of roles in ontology axioms, resulting in the fragment H¬ of DL-Lite¬

RDFS. In this restricted setting, we prove that both tasks are NP-complete. As for the alternative semantics, we define a semantics for query answering based on the “When In Doubt Throw It Out” principle from belief revision, which restricts reasoning to those feature space elements never discarded by any minimally-discarding model. We prove that query answering under this alternative semantics becomes Σp

2-complete, while it remains NP-complete in the restricted setting. Interestingly, for the results related to query answering, all the lower bounds already hold for conjunctive queries.

The remainder of this paper is organized as follows. In Section 2, we discuss some related works. In Section 3, we introduce the necessary background on ontologies and classifiers. In Section 4, we present our novel notion of HKB, including the semantics of queries. In Section 5, we provide

18995

<!-- Page 3 -->

the computational complexity analysis discussed above. Finally, in Section 6, we conclude and outline future work.

## 2 Related Work

The idea of integrating ML techniques and symbolic reasoning is at the core of the field of Neuro-Symbolic Artificial Intelligence (NSAI) (Hitzler and Sarker 2022). Many approaches proposed in NSAI prescribe the use of some formal language to interact with the information encoded within ML models. However, to the best of our knowledge, no previous work allows to fully integrate the information encoded into a set of ML models with the axioms of an ontology and perform logical reasoning. In the remainder of this section, we survey some of the most relevant related works and identify the main differences in our approach.

A prominent approach to integrate logical formalisms and ML models consists in using the former to express constraints over the latter (see (Giunchiglia, Stoian, and Lukasiewicz 2022) for an interesting survey). This gives rise to a family of ML models that we can call Logically Constrained (LCML). The behavior of an LCML model m is restricted using a set of logical constraints T expressed by encoding T into m at training time. This is achieved either by encoding the constraints into the loss-functions used by the learning algorithms (Xu et al. 2018) or by modifying the structure of m altogether (Giunchiglia et al. 2024). While the framework of LCML models may seem akin to the notion of HKBs, there are several crucial differences. Firstly, the aim of the LCML is to define models that comply with a specification: no form of logical reasoning over the knowledge stored in the model is allowed as is the case of HKBs. Secondly, constraints are expressed over one single model using the attributes of the data. Thus, there is no form of integration and contextualization across distinct models. Finally, LCML models do not provide any mechanism for information extraction other than value computation while one of the core features of HKBs is query answering.

Information extraction via logical formalisms is another important trend of NSAI, especially in the context of knowledge graph embeddings (KGE) (Wang et al. 2017). This line of work advocates the use of logics to express queries directly over a KGE in such a way to consider edges and entities that were not explicitly present in the original graph but labeled as possible in the embedding (see, e.g. (Hamilton et al. 2018; Fischer et al. 2019; Arakelyan et al. 2021)). A similar approach has been investigated for general ML models, not necessarily in the KGE framework (Fischer et al. 2019). These approaches lack some of the distinctive features of HKBs. Firstly, they are based on a very simple form of semantics (grounded on the likelihood of edges and entities in the embedding) and cannot capture the subtle nuances of a full-fledged logical formalism. Secondly, since there is no external ontology defining a shared vocabulary, they cannot integrate the information coming from multiple ML models in any meaningful way. Finally, there is no tool to express logical constraints (as the case of LCML models above), thus answers are subject to the characteristic uncertainty of ML models despite their rigorous logical definition.

One last line of work that we deem close to ours is the formal verification of ML models. In this line of work, the compliance of an ML model on a set of constraints is tested using automated reasoning techniques (see (K¨onig et al. 2024) for a thorough survey). We believe that HKBs could help experts in the verification of ML models by providing a conceptual language for specifying properties of interest, i.e. ontologies and queries for HKBs.

## Preliminaries

We assume the reader is familiar with function-free firstorder logic with equality (FOL). We define ΣC, ΣR, and Var to be the pairwise disjoint, countably infinite sets of atomic concepts, atomic roles, and variables, respectively.

Ontologies. Similarly to (Xiao et al. 2019), in this paper an ontology O consists of a finite set of declarations of concepts and roles from ΣC and ΣR, respectively, and a finite set of FOL axioms. We let sig(O), called the signature of O, be the set of declared atomic concepts and atomic roles. We impose that axioms in O use symbols from sig(O) ∪{=} for predicate names and symbols from Var for terms.

We are interested in DL-Lite¬

RDFS ontologies (Cima et al. 2025) in the technical sections. The axioms in a DL-Lite¬ RDFS ontology take the following forms (we use the DL notation):

B ⊑C P1 ⊑P2 (concept/role inclusion) B1 ⊑¬B2 P1 ⊑¬P2 (concept/role disjointness), where C ∈ΣC and for i = 1 and i = 2 (i) Pi is a basic role, i.e. either an atomic role R ∈ΣR or the inverse of an atomic role R ∈ΣR, which we denoted by R−, and (ii) Bi is a basic concept, i.e. either an atomic concept C ∈ΣC or an expression of the form ∃P with P a basic role.

Interpretations. Given an ontology O, an interpretation for O is a pair I = (∆I, ·I), where ∆I is a non-empty set of objects, called interpretation domain, and the interpretation function ·I assigns (i) a set CI ⊆∆I to each atomic concept C ∈sig(O) and (ii) a set RI ⊆∆I × ∆I to each atomic role R ∈sig(O). We denote by I |= O the fact that I satisfies all the axioms in O, i.e. I |= α for each α ∈O.

Given a DL-Lite¬

RDFS ontology O and an interpretation I = (∆I, ·I) for O, the interpretation function ·I extends to basic concepts and roles as follows: (∃R)I = {o | ∃o′.(o, o′) ∈RI}, (R−)I = {(o, o′) | (o′, o) ∈RI}, and (∃R−)I = {o | ∃o′.(o′, o) ∈RI}. Then, we say that I satisfies a concept inclusion B ⊑C (resp. role inclusion P1 ⊑P2) if BI ⊆CI (resp. P I

1 ⊆P I

2) and satisfies a concept disjointness B1 ⊑¬B2 (resp. role disjointness P1 ⊑¬P2) if BI

1 ∩BI 2 = ∅(resp. P I 1 ∩P I 2 = ∅).

Queries. Given an ontology O, a FOL query q over O is an expression of the form q = {¯x | φ(¯x)}, where ¯x = (x1,..., xm) is a tuple of variables from Var (m is the arity of q), and φ(¯x) is a FOL formula with the variables in ¯x as the free variables, predicate names from sig(O) ∪{=}, and terms from Var. For a FOL query q = {¯x | φ(¯x)} over an ontology O with ¯x = (x1,..., xm), an interpretation I for O, and a tuple of objects ¯o = (o1,..., om) from ∆I, we denote by I |= φ(¯x/¯o) the fact that I satisfies the FOL

18996

<!-- Page 4 -->

sentence φ(¯x/¯o) obtained by replacing each occurrence of the free variable xi with the domain object oi, for i ∈[m].

We consider two query languages: conjunctive queries (CQ) and unions of conjunctive queries with inequalities (UCQ̸=). A union of conjunctive queries with inequalities (UCQ̸=) q over an ontology O takes the form q = {¯x | ∃¯y1. ϕ1(¯x, ¯y1)∧ξ1(¯x, ¯y1)∨...∨∃¯yp. ϕp(¯x, ¯yp)∧ξp(¯x, ¯yp)}, where for each i ∈[p]: (i) ¯yi is a tuple of variables from Var with ¯x∩¯yi = ∅, (ii) ϕi(¯x, ¯yi) is a conjunction of atoms with predicate names from sig(O) and terms from ¯x∪¯yi, and (iii) ξi(¯x, ¯yi) is a conjunction of inequality atoms (i.e. an atom of the form t1̸ = t2 with t1, t2 ∈¯x∪¯yi). We say that q is a conjunctive query (CQ) if p = 1 and ξ1(¯x, ¯y1) is empty.

Classifiers. We fix a countably infinite set A of symbols for attributes. To each A ∈A, we associate an attribute domain DA, consisting of the non-empty set of possible values for the attribute A (e.g. DA can be a finite set of categories, the natural numbers N, or even the reals R). Given a tuple A = (A1,..., An) of attributes from A, we denote by F(A) the feature space of A, defined as F(A) = DA1 ×...×DAn.

Given a tuple A = (A1,..., An) of attributes from A, a binary classifier based on A (when A is clear from the context, a binary classifier) is a function κ: F(A) →{0, 1} assigning to each vector of values for the attributes in A a label in {0, 1}, with the usual meaning that the label 1 (resp. 0) corresponds to the positive (resp. negative) class. We also make use of the notion of a binary classifier over pairs based on A (when A is clear from the context, a binary classifier over pairs), which is a function λ: F(A) × F(A) →{0, 1}.

A Formal Framework for HKBs We assume that the extensional part of a Knowledge Base is defined via a set of binary classifiers, one for each atomic concept mentioned in the ontology, and a set of binary classifiers over pairs, one for each atomic role mentioned in the ontology. This leads us to the following formal definition.

Definition 1. A Hybrid Knowledge Base (HKB) K is a pair K = (O, Ψ), where O is an ontology and Ψ is a set of classifiers based on a tuple A of attributes from A (and we let sig(Ψ) = A). More precisely, Ψ contains:

• a binary classifier κC, for each C ∈sig(O); • a binary classifier over pairs λR, for each R ∈sig(O).

Note that the classifiers in Ψ operate over a tuple A of attributes. As such, A conveys the information from an Information System deemed relevant for supporting the decisionmaking processes of an organization. It can be thought of as the result of a feature selection process.

Example 2. Recall Example 1, and suppose the classifiers are based on the tuple A = (age, bmi, ant, a1c, hb) of patient attributes, where age is the patient age, with Dage = {0, 1, 2} (0 corresponds to young, 1 to middle-aged, and 2 to senior); bmi is the body mass index, with Dbmi = {0, 1, 2} (0 corresponds to low BMI, 1 medium, and 2 high); ant is the number of ABO blood group antigens, with Dant = {0, 1, 2} (0 corresponds to blood type O, 1 to either A or B, and 2 to AB); a1c indicates the value of blood glucose, with

Da1c = {0, 1, 2} (0 corresponds to low glucose level, 1 medium, and 2 high); and hb contains the hemoglobin levels according to blood tests, with Dhb = {0, 1, 2} (0 corresponds to low hemoglobin level, 1 medium, and 2 high). Suppose the classifiers in Ψ are defined as follows:

• For each ¯a = (a1, a2, a3, a4, a5) ∈F(A), we have: – κD(¯a) = 1 if and only if a2 + a3 −3 ≥0; – κM(¯a) = 1 if and only if 3a2 + a5 −5 ≥0; – κP(¯a) = 1 if and only if −a2 + 1

2a3 + a4 −5 2 ≥0

• For each pair (¯a,¯b) ∈F(A) × F(A), where ¯a = (a1, a2, a3, a4, a5) and ¯b = (b1, b2, b3, b4, b5), we have: – λcD(¯a,¯b) = 1 if and only if −a3−a4+b3+b4−1 ≥0; – λcB(¯a,¯b) = 1 if and only if a3 −b3 ≥0.

The HKB K for the medical scenario is then defined as the pair K = (O, Ψ), where O is the ontology with sig(O) = {D, M, P, cB, cD} and which states the set {P ⊑¬M} of axioms, while Ψ = {κD, κM, κP, λcD, λcB}.

We now turn to describe the semantics of HKBs, which we formalize in logical terms through first-order interpretations. Before proceeding, a few clarifications are in order. As previously noted, the data deemed relevant is conveyed by the set A of attributes over which the classifiers of a HKB operate, and, more specifically, is captured by the feature space F(A). Note that each element (a1,..., an) ∈F(A) either does not correspond to any real-world entity (i.e. no actual entity can exhibit its combination of attribute values) or represents one or more real entities sharing exactly those characteristics. With this observation in mind, we are now ready to define the notion of interpretation for a HKB.

Definition 2. Given a HKB K = (O, Ψ) with sig(Ψ) = A, an interpretation for K is a pair I = (I, f), where

• I = (∆I, ·I) is an interpretation for O; • f: F(A) →P(∆I) associates to each element ¯a ∈ F(A) a (possibly empty) set f(¯a) of objects from ∆I; • f(¯a) ∩f(¯b) = ∅holds for every pair (¯a,¯b) ∈F(A) × F(A) such that ¯a̸ = ¯b.

Note that f acts as a bridge from the raw input vectors, which constitute the sub-symbolic representation of data, to the symbolic representation embodied by the objects in the interpretation domain. The third bullet point ensures that distinct elements of the feature space are mapped to distinct objects of the interpretation domain (similarly to the Unique Name Assumption). Also, the definition allows modeling situations in which a combination of attribute values ¯a ∈F(A) is infeasible, expressible by setting f(¯a) = ∅, capturing the fact that no real-world entity exhibits such attributes according to the considered interpretation.

In what follows, for I = (I, f), we denote by disc(I) the set of I-discarded elements, i.e. disc(I) = {¯a ∈F(A) | f(¯a) = ∅}. We also say that I is trivial if disc(I) coincides with the feature space F(A), i.e. if disc(I) = F(A). We are now ready to define the notion of model for a HKB.

Definition 3. Let K = (O, Ψ) be a HKB with sig(Ψ) = A, and let I = (I, f) be an interpretation for K. We say that I is a model of K if I |= O and the next conditions hold:

18997

<!-- Page 5 -->

1. for each atomic concept C ∈sig(O): CI = {o | ∃¯a. κC(¯a) = 1 and o ∈f(¯a)}; 2. for each atomic role R ∈sig(O): RI = {(o, o′) | ∃¯a,¯b. λR(¯a,¯b) = 1 and o ∈f(¯a) and o′ ∈f(¯b)}.

When both conditions 1 and 2 hold, we write I |= Ψ.

In other words, an interpretation I = (I, f) for a HKB K = (O, Ψ) is a model of K if both I |= O and I |= Ψ. As for the condition I |= O, we require that I satisfies all the FOL axioms in O. As for I |= Ψ, once the universe of discourse ∆I and the function f are fixed, we treat the classifiers in Ψ as exact mappings, requiring that the extension of atomic concepts and roles faithfully follows the classifiers in Ψ. So we do not actually have any incomplete information about predicate extensions, since Ψ fully determines them. Thus, like the disjointness axioms in the ontology, the inclusions axioms also act as constraints in a given HKB.

Example 3. Recall Example 2. Let I be an interpretation for O such that ∆I = {o¯a | κP(¯a) = 0 ∨κM(¯a) = 0}, DI = {o¯a | κD(¯a) = 1}, PI = {o¯a | κP(¯a) = 1}, MI = {o¯a | κM(¯a) = 1}, cDI = {(o¯a, o¯b) | λcD(¯a,¯b) = 1}, and cBI = {(o¯a, o¯b) | λcB(¯a,¯b) = 1}. Let f: F(A) → P(∆I) be the function such that f(¯a) = ∅if both κP(¯a) = 1 and κM(¯a) = 1; otherwise, f(¯a) = {o¯a}. Consider now the interpretation I = (I, f) for K. By construction, we have I |= Ψ. Furthermore, since I discards all feature space elements classified positively by both κP and κM, we can conclude that I |= O. It follows that I is a model of K.

We say that a HKB is consistent if it has at least one model and inconsistent otherwise. Inconsistency can arise due to an unsatisfiable set of axioms (e.g. O = {∀x. (C(x)∧ ¬C(x))}) or due to the classifiers being incompatible with the ontology axioms (e.g. O = {∃x. C(x)} but κC(¯a) = 0, for each ¯a ∈F(A)). Although consistent, the next example shows that a HKB may admit only trivial models.

Example 4. Consider a HKB K′ = (O′, Ψ′) of a university scenario, where sig(O′) contains the atomic concepts AP, FP, FL, F, and L for associate professors, full professors, foreign lab coordinators, foreigners, and lab coordinators, respectively. The set of axioms in O′ is {AP ⊑¬FP, FL ⊑ L, FL ⊑F}. The set Ψ′ = {κAP, κFP, κFL, κF, κL} of classifiers is such that sig(Ψ′) = A′ = {A1, A2}, with DA1 = DA2 = {0, 1}. Furthermore, for each ¯a = (a1, a2) ∈ F(A′), we have κAP(¯a) = 1 if and only if a1 −1 ≥0; κFP(¯a) = 1 if and only if a1 + a2 −1 ≥0; κFL(¯a) = 1 if and only if −a1 −a2 + 1 ≥0; κF(¯a) = 1 if and only if a2 −1 ≥0; and κL(¯a) = 1 if and only if −a2 ≥0.

One can easily verify that each ¯a ∈F(A′) is such that either (i) κAP(¯a) = 1 ∧κFP(¯a) = 1 or (ii) κFL(¯a) = 1. Consider now an element ¯a ∈F(A′). If ¯a satisfies (i), then it should be discarded due to AP ⊑¬FP. If ¯a satisfies (ii), then one can see that either κL(¯a) = 0 or κF(¯a) = 0, and therefore it should be discarded due to FL ⊑L or FL ⊑F, respectively. Thus, we get that K′ admits only trivial models.

Trivial models inherently suppress the information inferred from the classifiers in Ψ, as they discard all the feature space elements. It is thus natural to focus only on non-trivial models, provided they exist. More generally, rather than considering all models of a HKB, it is reasonable to restrict the attention to those that retain maximal information from the application of the classifiers over the sub-symbolic data. In this paper, we focus on models that discard feature space elements in a minimal fashion, according to set inclusion.

Definition 4. Given a HKB K = (O, Ψ) and an interpretation I = (I, f) for K, we say that I is a minimallydiscarding model of K if (i) I is a model of K and (ii) there is no model I′ = (I′, f ′) of K such that disc(I′) ⊊disc(I).

Given a HKB K, we denote by MinDisc(K) the set of minimally-discarding models of K.

Interestingly, a HKB may admit minimally-discarding models that discard different subsets of the feature space.

Example 5. Recall Example 2. Let K′′ = (O′′, Ψ) be the HKB obtained from K by adding to O the axiom: cD ⊑cB. Consider ¯a = (1, 1, 1, 2, 0) and ¯b = (1, 0, 2, 2, 1). Note that (i) λcD(¯a,¯b) = 1 and λcB(¯a,¯b) = 0, and (ii) κM(¯a) = κM(¯b) = 0 and λcB(¯a, ¯a) = λcB(¯b,¯b) = 1. Due to (i), we derive that there can be no model I of K′′ such that both ¯a̸ ∈disc(I) and ¯b̸ ∈disc(I). Due to (ii), we derive that there can be models I of K′′ such that ¯a̸ ∈disc(I) and models I′ of K′′ such that ¯b̸ ∈disc(I′). As a result, there exist at least two distinct minimally-discarding models of K′′ that discard different subsets of the feature space.

The notion of minimally-discarding model shares similar characteristics with the notion of repair, widely studied in the literature on consistent query answering. To draw such a correspondence, we associate to each tuple A of attributes with a finite domain a set of facts DA = {s(c¯a) | ¯a ∈ F(A)}, where s ∈ΣC is an atomic concept assumed to be never mentioned in any ontology O and c¯a is a constant associated with element ¯a. To each HKB K = (O, Ψ) with sig(Ψ) being a tuple A of attributes with finite domains, we associate a knowledge base (KB) BK = (ΣK, DA), where ΣK is a set of axioms that includes the axioms in O together with the following set of axioms: {s(c¯a) →C(c¯a) | C ∈ sig(O) is an atomic concept and κC(¯a) = 1} ∪{s(c¯a) ∧ s(c¯b) →R(c¯a, c¯b) | R ∈sig(O) is an atomic role and λR(¯a,¯b) = 1}. A repair of a KB B = (Σ, D) formed by a set of facts D and a set of axioms Σ is a ⊆-maximal set of facts R ⊆D such that B′ = (Σ, R) is consistent. Given a HKB K = (O, Ψ) with sig(Ψ) being a tuple A of attributes with finite domains, a set of facts R ⊆DA, and a model I of K such that disc(I) = {¯a | s(c¯a) ∈DA \R}, one can verify that R is a repair of BK if and only if I ∈MinDisc(K).

## 4.1 Reasoning Tasks over HKBs In any Ontology-Driven Knowledge

Base framework, the typical form of interaction to extract information consists in posing queries over the vocabulary of the ontology. We adopt the same interaction model in our framework, and formally define the notion of answers to queries over HKBs.

Definition 5. Let K = (O, Ψ) be a HKB, let q = {¯x | φ(¯x)} be a FOL query over O of arity m, and let ¯t = (¯a1,..., ¯am) be an m-tuple of elements from F(A), i.e. ¯t ∈F(A)m. We say that ¯t is a skeptical-answer to q over K if, for every I =

18998

<!-- Page 6 -->

(I, f) ∈MinDisc(K), the following condition holds: there exists an m-tuple ¯o = (o1,..., om) of objects from ∆I such that I |= φ(¯x/¯o) and oi ∈f(¯ai), for each i ∈[m].

For a HKB K = (O, Ψ) and a FOL query q over O, we let Sans(q, K) be the set of skeptical-answers to q over K.

In other words, in the absence of a principled criterion to single out a unique “correct” minimally-discarding model, we adopt a cautious approach by considering only those answers obtainable by all minimally-discarding models. This form of reasoning is reminiscent of classical skeptical reasoning over all repairs of a KB, a common strategy for handling query answering with respect to inconsistent KBs (Lembo et al. 2010; Bienvenu and Bourgaux 2016).

Example 6. Recall Example 3, and consider the UCQ̸= q = {(x, y) | cD(x, y) ∧x̸ = y ∧(P(x) ∧P(y)) ∨(D(x) ∧ D(y))} over O, asking for pairs of distinct patients that are compatible blood donors and are either both pregnant or both diabetic. Consider now ¯a = (1, 2, 1, 0, 2) and ¯b = (0, 2, 1, 1, 2). It is not hard to verify that (¯a,¯b) ∈Sans(q, K).

In what follows, we say that a HKB K = (O, Ψ) is an (LO, LC)-HKB if (i) O is specified in the fragment LO of FOL and (ii) each classifier in Ψ belongs to the class LC of classifiers. Given the general framework presented so far, it is natural to consider the following reasoning tasks, for specific FOL fragments LO of ontology languages, classes LC of classifiers, and FOL fragments LQ of query languages:

• (non-trivial) consistency: given a (LO, LC)-HKB K, check whether K admits a (non-trivial) model; • skeptical entailment: given a (LO, LC)-HKB K, a query q ∈LQ, and a tuple ¯t, check whether ¯t ∈Sans(q, K).

We are interested in the classifiers complexity variant of the above decision problems, which is the complexity where only the set Ψ of classifiers is regarded as the input, while the ontology and the query (if applicable) are assumed to be fixed. This complexity measure is analogous to the widely studied data complexity (Vardi 1982) measure of reasoning tasks over KBs, where the input is only the set of facts.

## 5 Computational Complexity Analysis

We now provide a detailed computational complexity analysis of the decision problems defined in the previous section. In this first investigation, we focus on the setting in which LO = DL-Lite¬

RDFS, LQ is either CQ or UCQ̸=, and the classifiers operate on tuples of attributes having a finite domain. More specifically, similarly to other theoretical works that study reasoning tasks over ML models (Barcel´o et al. 2020a; Arenas et al. 2021; Alfano et al. 2025), we let the domain of each attribute be {0, 1}. This is only for the sake of presentation, and we observe that all our results can be easily extended to the case in which the domains are finite sets of arbitrary size. We further assume that each binary classifier over pairs λR: {0, 1}n × {0, 1}n →{0, 1} is treated as a standard classifier κR: {0, 1}2n →{0, 1} operating on concatenated input pairs, i.e. λR(x, x′) = 1 if and only if κR(x∥x′) = 1. Within this context, we consider the class of Multi-Layer Perceptron (MLP), i.e. LC = MLP.

As defined in (Barcel´o et al. 2020a), an MLP M is a function M: {0, 1}l →{0, 1} defined by a sequence of weight matrices W(1),..., W(k), bias vectors b(1),..., b(k), and activation functions a(1),..., a(k), where k is the number of layers of M. Given ¯a ∈{0, 1}l, for i ∈[k], assuming that h(0) = ¯a, we inductively define h(i) = a(i)(h(i−1)W(i) + b(i)). The output of M on ¯a is defined as M(¯a) = h(k). We assume all weights and biases to be rational numbers from Q. That is, we assume that there exists a sequence of positive integers d0,..., dk such that W(i) ∈Qdi−1×di and b(i) ∈Qdi, for i ∈[k]. Given that we are interested in binary classifiers, we assume that dk = 1. The size of an MLP is the total size of its weights and biases, in which the size of a rational number p q is log2(p) + log2(q) (with the convention that log2(0) = 1). We focus on MLPs in which all internal functions a(1),..., a(k−1) are the ReLU function relu(x) = max(0, x). Usually, MLP binary classifiers are trained using the sigmoid as the output function a(k). Nevertheless, when an MLP classifies an input (after training), it takes decisions by simply using the preactivations, also called logits. Based on this and on the fact that we only consider already trained MLPs, we can assume without loss of generality that the output function a(k) is the binary step function step(x) = 1 if x ≥0 and step(x) = 0 otherwise.

For instance, the HKB K′ defined in Example 4 is a (DL-Lite¬

RDFS, MLP)-HKB. It is straightforward to verify that a (DL-Lite¬

RDFS, MLP)-HKB always admit trivial models. So, in our setting, while the consistency problem becomes trivial, we now characterize the complexity of verifying whether a given (DL-Lite¬

RDFS, MLP)-HKB admit non-trivial models.

Theorem 1. For DL-Lite¬

RDFS ontologies and MLP classifiers, the non-trivial consistency problem is NP-complete in classifiers complexity.

The result comes from the observation that a non-trivial model exists if and only if there exists a non self-conflicting feature space element, which can be guessed in nondeterministic polynomial time. Intuitively, a self-conflicting feature space element is an element discarded by all models.

We now turn to the query answering problem over HKBs. Unfortunately, the following result proves that this problem is highly intractable, even in classifiers complexity and for the query language LQ = CQ. The upper bound is from a simple guess-and-check procedure, i.e. guess the (in general exponentially large) model that serves as a counterexample to query entailment, while the lower bound is from the complement of the 3-colorability problem for succinct graphs, a NEXPTIME-complete problem (Papadimitriou and Yannakakis 1986). The lower bound exploits the fact that from a Boolean circuit it is possible to obtain in polynomial time an equivalent MLP (Barcel´o et al. 2020b, Lemma 13).

Theorem 2. For DL-Lite¬

RDFS ontologies, MLP classifiers, and queries in UCQ̸=, the skeptical entailment problem is CONEXPTIME-complete in classifiers complexity. The hardness holds already for queries in CQ.

In light of the above negative result, we further investigate the query answering problem over HKBs by considering a

18999

<!-- Page 7 -->

fragment of the ontology language DL-Lite¬

RDFS as well as an alternative semantics for query answers that avoid skeptically reasoning over all the minimally-discarding models.

We point out that in Theorem 2 the main source of complexity comes from the usage of axioms involving atomic roles. This naturally leads us to consider the fragment H¬ of DL-Lite¬

RDFS which forbids the presence of atomic roles in axioms. Note that H¬ remains a useful ontology language, as it allows to express taxonomies (i.e. hierarchy of atomic concepts) as well as disjointness between atomic concepts. For instance, the ontologies O and O′ illustrated, respectively, in Example 2 and Example 4 are H¬ ontologies.

Interestingly, while for non-trivial consistency the lower bound provided in Theorem 1 already applies to LO = H¬, we now show that the complexity of the query answering problem significantly decreases for (H¬, MLP)-HKBs.

Theorem 3. For H¬ ontologies, MLP classifiers, and queries in UCQ̸=, the skeptical entailment problem becomes NP-complete in classifiers complexity. The hardness holds already for queries in CQ.

The complexity decreases are due to the fact that each minimally-discarding model of a (H¬, MLP)-HKB K discards only the self-conflicting feature space elements.

## 5.1 Alternative Semantics for Query Answering

We now consider a sound approximation of the query answering semantics provided in Definition 5. This semantics is inspired by the well-behaved IAR semantics adopted for query answering over inconsistent KBs (Lembo et al. 2015), which follows the WIDTIO (When In Doubt Throw It Out) approach of the belief revision and update research area.

Definition 6. Let K = (O, Ψ) with sig(Ψ) = A be a (DL-Lite¬

RDFS, MLP)-HKB, and let I be a model of K. We say that I is a minimally-discarding WIDTIO-model of K if, for every ¯a ∈F(A), the following holds: ¯a ∈disc(I) if and only if there exists a I′ ∈MinDisc(K) such that ¯a ∈disc(I′).

Let now q = {¯x | φ(¯x)} be a UCQ̸= query over O of arity m and ¯t = (¯a1,..., ¯am) be an m-tuple of elements from F(A). We say that ¯t is a WIDTIO-answer to q over K if, for every minimally-discarding WIDTIO-model I of K: there exists an m-tuple ¯o = (o1,..., om) of objects from ∆I such that I |= φ(¯x/¯o) and oi ∈f(¯ai), for each i ∈[m].

For a (DL-Lite¬

RDFS, MLP)-HKB K = (O, Ψ) and a UCQ̸= query q over O, we denote by Wans(q, K) the set of WIDTIO-answers to q over K.

In other words, a WIDTIO-model implements the WID- TIO approach by discarding all and only the feature space elements discarded by at least one minimally-discarding model. Thus, the evaluation of a query under the WIDTIO semantics reasons only on those feature space elements that belong to every possible minimally-discarding model.

It is not hard to see that a minimally-discarding WIDTIOmodel of a (DL-Lite¬

RDFS, MLP)-HKB K always exists (at worst, it will be a trivial model). Furthermore, this semantics is a sound approximation of the previously studied semantics, in the sense that Wans(q, K) ⊆Sans(q, K) holds for every (DL-Lite¬

RDFS, MLP)-HKB K = (O, Ψ) and UCQ̸= query q over O. Actually, the next example shows that there are cases in which the subset relation can even be strict. Example 7. Consider the (DL-Lite¬

RDFS, MLP)-HKB K = (O, Ψ), where sig(O) contains the atomic roles B, P, and F, and O states the axiom P ⊑¬F. The set Ψ = {λB, λP, λF} of classifiers is such that sig(Ψ) = A = {A1, A2}, and for each pair (¯a,¯b) ∈F(A) × F(A) such that ¯a = (a1, a2) and ¯b = (b1, b2), we have: λB(¯a,¯b) = κB(¯a||¯b) = 1 if and only if 2(a1+a2)−b1−b2−3 ≥0; λF(¯a,¯b) = κF(¯a||¯b) = 1 if and only if a1 +b2 −3(a2 +b1) ≥0; λP(¯a,¯b) = κP(¯a||¯b) = 1 if and only if −a1 −b2 −2(a2 + b1) + 2 ≥0. Let ¯a = (1, 1), ¯b = (1, 0), ¯c = (0, 1), and ¯d = (0, 0). Since (¯b, ¯c), (¯d, ¯c), (¯b, ¯d), and (¯d, ¯d) are the pairs (x, x′) such that κP(x||x′) = κF(x||x′) = 1, we derive that every I ∈MinDisc(K) is such that either disc(I) = { ¯d,¯b} or disc(I) = { ¯d, ¯c}. Consider now the CQ q = {(x) | ∃y.B(x, y)} over O. Since (¯a, ¯d), (¯a,¯b), and (¯a, ¯c) are the pairs (x, x′) such that κB(x||x′) = 1, we get that Sans(q, K) = {¯a} while Wans(q, K) = ∅. We now study the WIDTIO-entailment problem, for LO ∈ {DL-Lite¬

RDFS, H¬} and LQ = {CQ, UCQ̸=}, defined as the problem of deciding, given a (LO, MLP)-HKB K, a query q ∈LQ, and a tuple ¯t, whether ¯t ∈Wans(q, K). We start with LO = H¬, and prove that the two query answering semantics actually coincide in this setting (in fact, this is an immediate consequence of the next result). Proposition 1. Let K be a (H¬, MLP)-HKB and let I be an interpretation for K. We have that I ∈MinDisc(K) if and only if I is a WIDTIO-model of K.

It immediately follows that the complexity results derived in Theorem 3 also apply to the WIDTIO-entailment problem. We conclude this section by analyzing the remaining case of the complexity of query answering over (DL-Lite¬

RDFS, MLP)-HKBs under the WIDTIO semantics. Theorem 4. For DL-Lite¬

RDFS ontologies, MLP classifiers, and queries in UCQ̸=, the WIDTIO entailment problem is Σp

2-complete in classifiers complexity. The hardness holds already for queries in CQ.

For the upper bound, it is enough to guess an assignment to the variables that makes the query true, and check whether the guessed assignment involves only feature space elements that are never discarded in minimally-discarding models.

## 6 Conclusion and Future Work

We presented a novel framework that provides semantic context for the knowledge induced by ML models. This framework allows us to define formal reasoning tasks over the knowledge derived from both symbolic (i.e. ontologies) and sub-symbolic (i.e. classifiers) representations. Finally, we studied the complexity of two fundamental reasoning tasks in this context: consistency checking and query answering.

Directions for future work are many. Firstly, we would like to extend HKBs to account for the probabilistic nature of ML outputs. Secondly, we would like to study the complexity of other reasoning tasks connected to HKBs. Finally, it would be valuable to provide an ASP encoding for the query answering problem (under the WIDTIO approach) and validate it empirically with a thorough experimental evaluation.

19000

<!-- Page 8 -->

## Acknowledgments

This work has been supported by MUR under the PNRR project FAIR (PE0000013).

## References

Alfano, G.; Greco, S.; Mandaglio, D.; Parisi, F.; Shahbazian, R.; and Trubitsyna, I. 2025. Even-if Explanations: Formal Foundations, Priorities and Complexity. In Proceedings of the Thirty-Ninth AAAI Conference on Artificial Intelligence (AAAI 25), 15347–15355. Arakelyan, E.; Daza, D.; Minervini, P.; and Cochez, M. 2021. Complex Query Answering with Neural Link Predictors. In Proceedings of the Ninth International Conference on Learning Representations (ICLR 2021). Arenas, M.; B´aez, D.; Barcel´o, P.; P´erez, J.; and Subercaseaux, B. 2021. Foundations of Symbolic Languages for Model Interpretability. In Proceedings of the Thirty-Fourth Annual Conference on Neural Information Processing Systems (NeurIPS 2021), 11690–11701. Bahoo, S.; Cucculelli, M.; Goga, X.; and Mondolo, J. 2023. Artificial intelligence in Finance: a comprehensive review through bibliometric and content analysis. SN Business & Economics, 4(23). Barcel´o, P.; Monet, M.; P´erez, J.; and Subercaseaux, B. 2020a. Model Interpretability through the lens of Computational Complexity. In Proceedings of the Thirty-Third Annual Conference on Neural Information Processing Systems (NeurIPS 2020). Barcel´o, P.; Monet, M.; P´erez, J.; and Subercaseaux, B. 2020b. Model Interpretability through the Lens of Computational Complexity. CoRR, abs/2010.12265. Bienvenu, M.; and Bourgaux, C. 2016. Inconsistency- Tolerant Querying of Description Logic Knowledge Bases. In Pan, J. Z.; Calvanese, D.; Eiter, T.; Horrocks, I.; Kifer, M.; Lin, F.; and Zhao, Y., eds., Proceedings of the Twelfth International Summer School on Reasoning Web: Logical Foundation of Knowledge Graph Construction and Query Answering (RW 2016), volume 9885 of Lecture Notes in Computer Science, 156–202. Springer. Bienvenu, M.; and Ortiz, M. 2015. Ontology-Mediated Query Answering with Data-Tractable Description Logics. In Proceedings of the Eleventh International Summer School Tutorial Lectures (RW 2015), 218–307. Bishop, C. M. 2007. Pattern recognition and machine learning, 5th Edition. Information science and statistics. Springer. Chen, H.; Chiang, R. H. L.; and Storey, V. C. 2012. Business Intelligence and Analytics: From Big Data to Big Impact. MIS Quarterly, 36(4): 1165–1188. Cima, G.; Console, M.; Delfino, R. M.; Lenzerini, M.; and Poggi, A. 2025. Answering Conjunctive Queries with Safe Negation and Inequalities over RDFS Knowledge Bases. In Proceedings of the Thirty-Ninth AAAI Conference on Artificial Intelligence (AAAI 25), 14824–14831. Cima, G.; Lenzerini, M.; and Poggi, A. 2020. Answering Conjunctive Queries with Inequalities in DL-LiteR. In Proceedings of the Thirty-Fourth AAAI Conference on Artificial Intelligence (AAAI 2020), 2782–2789.

Cuenca Grau, B. 2004. A possible simplification of the semantic web architecture. In Proceedings of the Thirteenth International World Wide Web Conference (WWW 2004), 704–713.

Fischer, M.; Balunovic, M.; Drachsler-Cohen, D.; Gehr, T.; Zhang, C.; and Vechev, M. T. 2019. DL2: Training and Querying Neural Networks with Logic. In Proceedings of the Thirty-Sixth International Conference on Machine Learning (ICML 2019), 1931–1941.

Giunchiglia, E.; Stoian, M. C.; and Lukasiewicz, T. 2022. Deep Learning with Logical Constraints. In Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence (IJCAI 2022), 5478–5485.

Giunchiglia, E.; Tatomir, A.; Stoian, M. C.; and Lukasiewicz, T. 2024. CCN+: A neuro-symbolic framework for deep learning with requirements. International Journal of Approximate Reasoning, 171: 109124.

Hamilton, W. L.; Bajaj, P.; Zitnik, M.; Jurafsky, D.; and Leskovec, J. 2018. Embedding Logical Queries on Knowledge Graphs. In Proceedings of the Thirty-First Annual Conference on Advances in Neural Information Processing Systems (NeurIPS 2018), 2030–2041.

Hastie, T.; Tibshirani, R.; and Friedman, J. H. 2009. The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd Edition. Springer.

Hitzler, P.; and Sarker, M. K. 2022. Neuro-symbolic artificial intelligence: The state of the art. IOS press.

Jiang, F.; Jiang, Y.; Zhi, H.; Dong, Y.; Li, H.; Ma, S.; Wang, Y.; Dong, Q.; Shen, H.; and Wang, Y. 2017. Artificial intelligence in healthcare: past, present and future. Stroke and Vascular Neurology, 2(4).

K¨onig, M.; Bosman, A. W.; Hoos, H. H.; and van Rijn, J. N. 2024. Critically Assessing the State of the Art in Neural Network Verification. Journal of Machine Learning Research, 25: 12:1–12:53.

Lembo, D.; Lenzerini, M.; Rosati, R.; Ruzzi, M.; and Savo, D. F. 2010. Inconsistency-tolerant Semantics for Description Logics. In Proceedings of the Fourth International Conference on Web Reasoning and Rule Systems (RR 2010), 103–117.

Lembo, D.; Lenzerini, M.; Rosati, R.; Ruzzi, M.; and Savo, D. F. 2015. Inconsistency-tolerant query answering in ontology-based data access. Journal of Web Semantics, 33: 3–29.

Papadimitriou, C. H.; and Yannakakis, M. 1986. A Note on Succinct Representations of Graphs. Information and Control, 71(3): 181–185.

Poggi, A.; Lembo, D.; Calvanese, D.; De Giacomo, G.; Lenzerini, M.; and Rosati, R. 2008. Linking Data to Ontologies. Journal on Data Semantics, X: 133–173.

Rosati, R. 2007. The Limits of Querying Ontologies. In Proceedings of the Eleventh International Conference on Database Theory (ICDT 2007), volume 4353 of Lecture Notes in Computer Science, 164–178. Springer.

19001

<!-- Page 9 -->

Thames, C.; and Sun, Y. 2024. A Survey of Artificial Intelligence Approaches to Safety and Mission-Critical Systems. In 2024 Integrated Communications, Navigation and Surveillance Conference (ICNS), 1–12. Vardi, M. Y. 1982. The Complexity of Relational Query Languages (Extended Abstract). In Proceedings of the Fourteenth Annual ACM Symposium on Theory of Computing (STOC 1982), 137–146. Wang, Q.; Mao, Z.; Wang, B.; and Guo, L. 2017. Knowledge graph embedding: A survey of approaches and applications. IEEE transactions on knowledge and data engineering, 29(12): 2724–2743. Xiao, G.; Ding, L.; Cogrel, B.; and Calvanese, D. 2019. Virtual Knowledge Graphs: An Overview of Systems and Use Cases. Data Intelligence, 1(3): 201–223. Xu, J.; Zhang, Z.; Friedman, T.; Liang, Y.; and den Broeck, G. V. 2018. A Semantic Loss Function for Deep Learning with Symbolic Knowledge. In Proceedings of the Thirty-Fifth International Conference on Machine Learning (ICML 2018), 5498–5507.

19002
