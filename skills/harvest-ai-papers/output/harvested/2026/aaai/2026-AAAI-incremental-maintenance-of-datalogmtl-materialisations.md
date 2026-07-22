---
title: "Incremental Maintenance of DatalogMTL Materialisations"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39025
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39025/42987
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Incremental Maintenance of DatalogMTL Materialisations

<!-- Page 1 -->

Incremental Maintenance of DatalogMTL Materialisations

Kaiyue Zhao1*, Dingqi Chen1*, Shaoyu Wang1, 2*, Pan Hu1†

1School of Computer Science, Shanghai Jiao Tong University, China 2Department of Computer Science, University of Oxford, UK

## Abstract

DatalogMTL extends the classical Datalog language with metric temporal logic (MTL), enabling expressive reasoning over temporal data. While existing reasoning approaches, such as materialisation-based and automata-based methods, offer soundness and completeness, they lack support for handling efﬁcient dynamic updates—a crucial requirement for real-world applications that involve frequent data updates. In this work, we propose DRedMTL, an incremental reasoning algorithm for DatalogMTL with bounded intervals. Our algorithm builds upon the classical Delete/Rederive (DRed) algorithm, which incrementally updates the materialisation of a Datalog program. Unlike a Datalog materialisation which is in essence a ﬁnite set of facts, a DatalogMTL materialisation has to be represented as a ﬁnite set of facts plus periodic intervals indicating how the full materialisation can be constructed through unfolding. To cope with this, our algorithm is equipped with speciﬁcally designed operators to efﬁciently handle such periodic representations of DatalogMTL materialisations. We have implemented this approach and tested it on several publicly available datasets. Experimental results show that DRedMTL often signiﬁcantly outperforms rematerialisation, sometimes by orders of magnitude.

Code, datasets and instructions — github.com/Horizon12275/DREDmtl-for-DatalogMTL Extended version with full proof — arxiv.org/abs/2511.12169

## Introduction

DatalogMTL extends the well-known rule language Datalog (Ceri, Gottlob, and Tanca 1989) with metric temporal logic (MTL) (Koymans 1990). It has found applications in various domains, including ontology-based query answering (Brandt et al. 2018; Güzel Kalayci et al. 2018), stream reasoning (Wał˛ega et al. 2023; Wałe¸ga, Kaminski, and Cuenca Grau 2019), and temporal reasoning in the ﬁnancial sector (Colombo et al. 2023; Nissl and Sallinger 2022; Mori et al. 2022), among others. To showcase the capabilities of DatalogMTL, consider an industrial application scenario in which DatalogMTL has

*These authors contributed equally. †Corresponding author Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

been applied by our research group to automatically detect anomaly of power transformers. More concretely, gas concentration data is ﬁrst collected in real time using existing gas-in-oil sensors and then fed into a DatalogMTL rule engine, which ﬁres alarms whenever appropriate. As an example, the following rule shows how oil thermal faults can be detected:

OTF(x) ←HasEthylene(x,y)

∧HasEthane(x,z) ∧x[0,10]AboveThirty(y)

∧x[0,10]AboveSeventy(z)

(1)

This rule states that at any time point t, if ethylene and ethane have both been detected in the transformer oil, and their gas concentration values surpassed 30 ppm and 70 ppm at any time point in the past ten minutes, respectively, then an oil thermal fault (OTF) is detected.

Reasoning in DatalogMTL can be implemented using top-down or bottom-up approaches, or a combination of the two. One typical top-down approach is based on Büchi automata: it ensures correctness but incurs high reasoning costs. Therefore, efforts have been made to devise ef- ﬁcient bottom-up (or materialisation-based) approach for DatalogMTL reasoning. The vadalog system (Bellomarini, Nissl, and Sallinger 2022) implements such an approach, but it may not terminate due to recursion. The MeTeoR system (Wang et al. 2022) combines bottom-up and top-down approaches, but only resorts to the top-down approach when necessary. More recently, magic set rewriting, which simulates top-down evaluation via bottom-up reasoning, has been extended to support DatalogMTL reasoning (Wang et al. 2025). While materialisation-based approaches are popular for DatalogMTL reasoning, to the best of our knowledge, no incremental maintenance algorithm for DatalogMTL reasoning has been developed: when the set of explict facts change, the above systems have no choice but to recompute the materialisation from scratch.

For plain Datalog, many incremental materialisation maintenance algorithms have been developed, including Delete/Rederive (DRed) and its variants (Gupta, Mumick, and Subrahmanian 1993; Staudt and Jarke 1996; Ren and Pan 2011; Urbani et al. 2013; Hu, Motik, and Horrocks 2018), Backward/Forward (B/F) (Motik et al. 2015),

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19467

<!-- Page 2 -->

FBF (Motik et al. 2019), among others. However, adapting an incremental materialisation maintenance algorithm for Datalog to support DatalogMTL reasoning is nontrivial. Unlike Datalog, DatalogMTL supports recursion over time, which easily leads to unbounded time intervals, making termination problematic. As a result, changes to the dataset may not only affect immediate derivations but also propagate across time through periodic patterns. Although it is known that under certain restrictions, materialisations in DatalogMTL exhibit repeating structures that can be ﬁnitely represented, how to correctly update such repeating structures is still highly challenging, especially due to the complex interplay between consequence propagation and termination condition checks.

In this paper, building upon the well-known DRed algorithm, we propose DRedMTL. It replaces standard Datalog materialisation maintenance with a novel set of operations over ﬁnite representations of DatalogMTL materialisations called periodic materialisations. Periodic materialisations compactly encode inﬁnite sets of temporal facts by capturing their recurring periodic patterns, which allows us to reason over inﬁnite time domains using ﬁnite representations.

To facilitate reasoning over periodic materialisations, we devised a novel seminaïve evaluation operator speciﬁcally designed to efﬁciently handle the propagation of facts in the new DatalogMTL setting. In addition, we developed a new period identiﬁcation algorithm that effectively and correctly guarantees termination. Our experimental evaluation demonstrates that, compared to rematerialisation from scratch, our approach achieves signiﬁcant performance improvements, especially for small updates.

## Preliminaries

In this section, we ﬁrst brieﬂy recapitulate the syntax and semantics of DatalogMTL. We focus on DatalogMTL with bounded intervals, as this restriction enables materialisationbased reasoning. Then, we brieﬂy discuss how the materialisation of a DatalogMTL program can be ﬁnitely represented: our incremental maintenance algorithm will have to incrementally update such ﬁnite representations in response to changes in the explicitly given data.

Syntax of DatalogMTL Throughout the paper, we assume that the timeline consists of rational numbers. A time interval is a set of continuous time points ϱ of the form ⟨t1,t2⟩, where t1 ∈Q ∪{−∞}, t2 ∈Q ∪{∞}, ⟨is [ or (and likewise ⟩is ] or). An interval is bounded if both of its endpoints are rational numbers, i.e., neither ∞nor −∞. When it is clear from the context, we may abuse the distinction between intervals (i.e. sets of time points) and their representation ⟨t1,t2⟩. If ϱ = ⟨t1,t2⟩, let ϱ−= t1 and ϱ+ = t2.

A term is either a variable or a constant. A relational atom is an expression R(t), where R is a predicate and t is a tuple of terms of arity matching that of R. Metric atoms extend relational atoms by allowing operators from metric temporal logic (MTL), namely ⊞ϱ, ⊟ϱ, |ϱ, xϱ, Uϱ, and Sϱ, where ϱ is an interval. Formally, metric atoms, M, are generated by

I,t ⊧⊺ for every t ∈Q

I,t ⊧ for no t ∈Q

I,t ⊧⊞ϱM iff I,t1 ⊧M for all t1 s.t. t1 −t ∈ϱ

I,t ⊧⊟ϱM iff I,t1 ⊧M for all t1 s.t. t −t1 ∈ϱ

I,t ⊧|ϱM iff I,t1 ⊧M for some t1 s.t. t1 −t ∈ϱ

I,t ⊧xϱM iff I,t1 ⊧M for some t1 s.t. t −t1 ∈ϱ

I,t ⊧M2UϱM1 iff I,t1 ⊧M1 for some t1 s.t. t1 −t ∈ϱ, and I,t2 ⊧M2 for all t2 ∈(t,t1)

I,t ⊧M2SϱM1 iff I,t1 ⊧M1 for some t1 s.t. t −t1 ∈ϱ, and I,t2 ⊧M2 for all t2 ∈(t1,t)

**Table 1.** Semantics for ground metric atoms

the grammar

M ∶∶= ∣⊺∣R(t) ∣⊞ϱM ∣⊟ϱM ∣|ϱM ∣xϱM ∣

MUϱM ∣MSϱM, where ⊺and are the constants representing truth and falsehood, respectively, and ϱ is any arbitrary interval containing only nonnegative rationals. A DatalogMTL rule, r, is of the form

M ′ ←M1 ∧M2 ∧⋅⋅⋅∧Mn, for n ≥1, where each Mi is a metric atom and M ′ is a metric atom not mentioning, |, x, U, and S. Metric atom M ′ and the set {Mi ∣i ∈{1,...,n}} are the head and body of r, denoted as head(r) and body(r), respectively.

A rule r is safe if each variable in its head appears also in its body. A program Π is a ﬁnite set of safe rules. A substitution σ is a mapping of ﬁnitely many variables to constants. For α an expression (e.g., an atom, a rule, or a program thereof), ασ is the result of replacing each occurrence of a variable x in α with σ(x), if the latter is deﬁned. An expression is ground if it mentions no variable. A fact is of the form R(t)@ϱ, where R(t) is a ground relational atom, ϱ is an interval, and @ indicates that the preceding atom holds over the time interval that follows. A dataset D is a ﬁnite set of facts. If all the intervals a dataset (resp., a program) mentions are bounded, then the dataset (resp., the program) is bounded. Our work focuses on bounded datasets and programs.

Semantics of DatalogMTL A DatalogMTL interpretation I is a function that maps each time point t ∈Q to a set of ground relational atoms (essentially to atoms that hold at t). For a time point t ∈Q, if R(t) belongs to this set, we write I,t ⊧R(t). This extends to the ground metric atoms as presented in Table 1.

An interpretation I satisﬁes a fact R(t)@ϱ, denoted as I ⊧R(t)@ϱ, if I,t ⊧R(t) for each t ∈ϱ. An interpretation I is a model of a dataset D, written I ⊧D, if it satis- ﬁes every fact in D. An interpretation I satisﬁes a ground rule r0 if I,t ⊧body(r0) implies I,t ⊧head(r0) for each t ∈Q. A ground rule r0 is an instance of a rule r if there

19468

<!-- Page 3 -->

is a substitution σ such that r0 = rσ. An interpretation I satisﬁes a rule r, if it satisﬁes all ground instances of r, and it is a model of a program Π, if it satisﬁes all rules in Π. I is a model of a pair (Π,D) if I is both a model of D and a model of Π. A program-dataset pair (Π,D) entails a fact R(t)@ϱ, written (Π,D) ⊧R(t)@ϱ, if all models of (Π,D) satisfy R(t)@ϱ. An interpretation I contains another interpretation I′, written I′ ⊆I, if I,t ⊧R(t) implies I′,t ⊧R(t) for each ground relational atom R(t) and each t ∈Q; moreover, I = I′ if they contain each other. An interpretation I is the least in a set of interpretations I, if I ∈I, and ∀I′ ∈I, I ⊆I′. Similarly, I is the greatest in I, if I ∈I, and ∀I′ ∈I, I′ ⊆I. Each dataset D has a unique least interpretation ID such that ID is the least in the set of all models of D. For interpretations I1, I2, and I3, we write I3 = I1 ∪I2 if I3 is the least in {I ∣I1 ⊆I and I2 ⊆I}, and we write I3 = I1 ∩I2, if I3 is the greatest in {I ∣I ⊆I1 and I ⊆I2}. The empty interpretation I∅maps t to ∅for each t ∈Q, and it is contained by any interpretation. Finally, we write I3 = I1 −I2, if I3 is the greatest in {I ∣I ⊆I1,I ∩I2 = I∅}.

Materialisation for DatalogMTL We now brieﬂy discuss how materialisation-based reasoning works for DatalogMTL with bounded intervals. To this end, we ﬁrst introduce a few additional notations that will facilitate our discussion. For D a dataset, t−

D and t+

D denote the minimal and maximal interval endpoints appearing in D, respectively, and t−

D = t+

D = 0 if D mentions no numbers. Moreover, the depth of a rule r, written depth(r), is deﬁned as the sum of right endpoints of all intervals appearing in the operators of r, and depth(r) = 0 if r mentions no intervals; for Π a program, depth(Π) is the maximum depth of its rules.

The immediate consequence operator TΠ for a program Π is the function that maps an interpretation I to the least interpretation TΠ(I) containing I and satisfying the following: for each r0 a ground rule instance of a rule in Π and each t a time point, I,t ⊧body(r0) implies I,t ⊧head(r0). For a program Π and a dataset D, a transﬁnite sequence of interpretations T α

Π(ID) can be deﬁned for ordinals α by successively applying TΠ, the immediate consequence operator for Π, to ID, the unique least model for D, as follows: (i) T 0

Π(ID) = ID, (ii) T α+1

Π (ID) = TΠ(T α

Π(ID)) for α an ordinal, and (iii) T α

Π(ID) = ⋃β<α T β

Π(ID) for α a limit ordinal; the canonical model CΠ,D of Π and D is the interpretation T ω1

Π (ID) with ω1 the ﬁrst uncountable ordinal. In fact, CΠ,D is the least model of Π and D (Brandt et al. 2017).

For an interpretation I and an interval ϱ, the projection I ∣ϱ of I over ϱ is the interpretation that coincides with I on ϱ and maps all relational atoms to false outside ϱ. Moreover, an interpretation I is a shift of another interpretation I′, if there is a rational number s such that for each R(t) a ground relational atom and each t a time point, I′,t ⊧R(t) implies I,t + s ⊧R(t), and vice versa. Finally, for a given program Π and a dataset D, we are not interested in dealing with arbitrary rational number time points on the time line; instead, it is sufﬁcient to handle time points that are somewhat related to those appearing in Π and D. This is formalised by the notion of (Π,D)-ruler. Concretely, (Π,D)-ruler is the set of time points of the value t+i×div(Π), where t is an endpoint mentioned in D and i is an integer, and div(Π) = 1/k, with k being the product of all denominators in the rational endpoints mentioned in Π; for generality, k = 1 and div(Π) = 1 if Π has no mention of rational endpoints.

We are now ready to deﬁne the notions of saturated interpretation and unfolding, which are key components for ﬁnitely representing the materialisation of a bounded program-dataset pair.

Deﬁnition 1. For a program Π and a dataset D, interpretation Tk

Π(ID) is saturated if there exist closed intervals ϱ1,ϱ2,ϱ3 and ϱ4 of length 2depth(Π), whose endpoints are located on the (Π,D)-ruler and satisfy ϱ+

1 < ϱ+ 2 < t− D and t+

D < ϱ−

3 < ϱ− 4, and such that the following properties hold:

• Tk Π(ID) satisﬁes Π in [ϱ−

1,ϱ+ 4]; • Tk Π(ID) ∣ϱ1 and Tk

Π(ID) ∣ϱ3 are shifts of Tk

Π(ID) ∣ϱ2 and Tk

Π(ID) ∣ϱ4,respectively.

[ϱ−

1,ϱ− 2) and (ϱ+ 3,ϱ+ 4] are often referred to as the left period, written ϱleft, and the right period, written ϱright, of the interpretation Tk

Π(ID), respectively.

Deﬁnition 2. The (ϱleft,ϱright)-unfolding of a saturated interpretation Tk

Π(ID) with periods (ϱleft,ϱright) is the interpretation C such that:

• C ∣[ϱ− left,ϱ+ right]= Tk

Π(ID) ∣[ϱ− left,ϱ+ right],

• C ∣ϱleft−n⋅∣ϱleft∣is a shift of Tk Π(ID) ∣ϱleft, for any n ∈N,

• C ∣ϱright+n⋅∣ϱright∣is a shift of Tk Π(ID) ∣ϱright, for any n ∈N.

It has been shown that for an arbitrary pair of bounded program and dataset (Π,D), there exists k ∈N and intervals ϱleft and ϱright such that Tk

Π(ID) is a saturated interpretation with periods (ϱleft,ϱright), and the (ϱleft,ϱright)-unfolding of Tk

Π(ID) coincides with CΠ,D, the canonical model of Π and D (Wałe¸ga et al. 2023). Intuitively speaking, a saturated interpretation ﬁnitely represents the canonical model of a program and a dataset. The goal of this work is to incrementally update a saturated interpretation in response to changes in the explicitly given dataset D.

The Delete/Rederive Algorithm To incrementally update saturated interpretations for DatalogMTL, we draw inspirations from the Delete/Rederive (DRed) algorithm (Gupta, Mumick, and Subrahmanian 1993; Staudt and Jarke 1996), a well-known technique for maintaining Datalog materialisations. Given a Datalog program, a set of explicitly given facts, the original materialisation, and sets of facts to remove from and to add to the given facts, the DRed algorithm updates the materialisation to reﬂect changes in the explicitly given facts, without recomputing it from scratch. More speciﬁcally, the algorithm operates in three stages: in the overdeletion stage, the algorithm eagerly identiﬁes all facts that depend on the set of deleted facts; it then enters the rederivation stage, in which it recognises which of the overdeleted facts can be rederived in one step; ﬁnally, during insertion, the algorithm computes the consequences of both the rederived facts and the newly inserted ones.

19469

<!-- Page 4 -->

Motivation Before we present the technical details of our incrmental update approach for DatalogMTL, in this section, we discuss at a high level challenges that need to be addressed in devising such an incremental update approach. We also provide key insights behind our incremental update algorithm. Finally, we provide a concrete example that highlights the beneﬁts of applying our incremental maintenance algorithm for DatalogMTL reasoning compared with recomputing the materialisation from scratch.

In extending DRed for Datalog to support DatalogMTL reasoning, two major challenges arise. First, DRed relies on the seminaïve evaluation strategy applied in both the overdeletion and the insertion stages to be efﬁcient in dealing with updates. More speciﬁcally, in each round of rule application, at least one body atom is required to be evaluated in the set of facts deleted/inserted in the previous round; this strategy ensures that only consequences dependent on the deleted/inserted facts are considered. Although seminaïve evaluation has been considered for DatalogMTL materialisation, its interplay with the construction of saturated interpretations in the context of DatalogMTL reasoning has not been studied, let alone the application of seminaïve evaluation strategy in DatalogMTL materialisation maintenance. Second, for the Datalog setting, the bulk of the work is devoted to iterative rule application, so it is sufﬁcient to make rule application process ‘incremental’ in order to obtain an algorithm that is efﬁcient for updates; however, in the DatalogMTL setting, a signiﬁcant amount of time needs to be dedicated to periods identiﬁcation (i.e., termination checks). Intuitively, after each round of rule application, the period identiﬁcation procedure enumerates all pairs of intervals of a certain length, and then it compares pairwisely the facts in these intervals to detect the presence of a repeating pattern. Once two intervals coincide in their content, a period is identiﬁed. As such, the cost of this procedure naturally depends on the number of facts inside these intervals. Therefore, it is essential that the periods identiﬁcation process is also designed to be somewhat ‘incremental’, so that the overall processing time aligns with the size of the updates rather than the size of the entire materialisation; this would require thorough understanding and careful treatment of the periodic structure of DatalogMTL materialisations.

Our incremental maintenance technique addresses both of these two challenges. For the ﬁrst challenge, we devise a novel seminaïve evaluation operator that is tailored for incremental updates in the DatalogMTL setting: compared with the existing seminaïve operator, our new operator identiﬁes more accurately the consequences affected by the update and also facilitates period identiﬁcation. To tackle the second challenge, our algorithm is designed to identify periods in the updated facts and their consequences, rather than in the entire materialisation. Typically, deletions and insertions are small compared with the entire materialisation. As such, computing periods over the updated facts tend to be less costly than doing so for the entire materialisation; thus, our approach has the potential to signiﬁcantly reduce redundant computations, especially in scenarios where updates only affect a limited portion of the materialisation. We use the following example to highlight the beneﬁts of our approach; throughout the technical section, this example will be expanded to illustrate key operations in our algorithm.

Example 1. Let program Π consist of a single rule (2), and let E, E−, and E+ be the original dataset, the set of facts to remove from E, and set of facts to add to E, respectively. Now consider the materialisation of Π over E. According to the deﬁnition of depth(Π) and Deﬁnition 1, it is easy to verify that depth(Π) = 11, and that when k = 4, interpretation Tk

Π(IE) is saturated, with ϱleft = [−24,−23) and ϱright = [24,34) being possible left and right periods, respectively. To arrive at the conclusion that ϱright = [24,34), the materialisation procedure needs to verify that Tk

Π(IE) ∣[2,24] is a shift of Tk

Π(IE) ∣[12,34], and this clearly requires comparing O(n) facts. To summarise, the materialisation procedure requires O(n) time.

⊞[0,1]R(x) ←⊟[9,10]R(x) (2)

E = {R(ai)@[0,1] ∣0 < i < n}

E−= {R(a1)@[0,1]}

E+ = {R(an)@[0,1]}

Now consider the removal of E−and the insertion of E+. If we recompute the materialisation from scratch over the entire set (E ∖E−) ∪E+, the procedure again requires O(n) time. In contrast, our incremental update approach restricts the attention to only the updated facts and their consequences. For deletion, our approach tries to identify periodic structure only among facts of the form R(a1)@ϱ. In our example, after a constant number of rule application, our algorithm will be able to identify the relevant left and right periods by only comparing O(1) facts instead of O(n) facts. In other words, (over)deletion requires only O(1) time. Insertion follows the same principle, and so we omit the details.

DRed for DatalogMTL

Before we present the details of our algorithm, we ﬁrst introduce the notion of periodic materialisations, which are ﬁnite representations of possibly unbounded models of DatalogMTL programs. Our update algorithm will have to incrementally maintain periodic materialisations in response to changes in the explicitly given data.

Deﬁnition 3. For (Π,E) a bounded DatalogMTL programdataset pair, a periodic materialisation of (Π,E) is a triple I of the form ⟨I,ϱL,ϱR⟩, where I is a saturated interpretation of Π and E, and ϱL and ϱR are periods of this saturated interpretation; moreover, the unfolding of I, written unfold(I), is deﬁned as the (ϱL,ϱR)-unfolding of I.

By Deﬁnition 3 and properties already discussed in the Preliminary Section, if I is a periodic materialisation of a program-dataset pair (Π,E), then unfold(I) coincides with CΠ,E, the canonical model of Π and E. Note that I can capture the interpretation of a bounded dataset I, in which case I = ⟨I,ϱL,ϱR⟩such that I ∣ϱL= I ∣ϱR= I∅, and unfold(I) = I.

19470

<!-- Page 5 -->

## Algorithm

1: DREDMT L(Π,E,I,E−,E+)

Input: program Π, original dataset E, periodic materialisation I of (Π,E), dataset to remove E−, dataset to insert E+

1 D ∶= R ∶= A ∶= ∅, E−∶= (E−∩E)∖E+, E+ ∶= E+∖E

## 2 OVERDELETE

## 3 REDERIVE

## 4 INSERT

5 procedure OVERDELETE

6 ND ∶= E−

7 loop

8 ∆D ∶= ND ∖D

9 (ϱD

L, ϱD

R) ∶= PDS(Π,E,I.ϱL,I.ϱR,D, ∆D)

10 if (ϱD

L, ϱD

R) ≠(∅,∅) then break

11 ND ∶= Π⟨unfold(I) ∖D ⋮∆D⟩

12 D ∶= D ∪∆D

13 D ∶= ⟨D,ϱD

L,ϱD

R ⟩, I ∶= I ∖∖D

14 procedure REDERIVE

15 NR ∶= ∅, k = 1

16 loop

17 tL = (I.ϱL)+ −k × max(2depth(Π),∣I.ϱL∣)

18 tR = (I.ϱR)−+ k × max(2depth(Π),∣I.ϱR∣)

19 NR ∶= NR ∪(unfd(D)∣[tL,tR] ∩TΠ(unfd(I)))

20 ∆R ∶= NR ∖R

21 (ϱR

L,ϱR

R) ∶= PDS(Π,E,I.ϱL,I.ϱR,R,∆R)

22 if (ϱR

L, ϱR

R) ≠(∅,∅) then break

23 R ∶= R ∪∆R, k ∶= k + 1

24 NR ∶= Π⟨unfold(I) ∪R ⋮∆R⟩

25 R ∶= ⟨R,ϱR

L,ϱR

R ⟩, I ∶= I ⋓R

26 procedure INSERT

27 NA ∶= E+, E = (E ∖E−) ∪E+

28 loop

29 ∆A ∶= NA ∖(unfold(I) ∪A)

30 (ϱA

L,ϱA

R) ∶= PDS(Π,E,I.ϱL,I.ϱR,A,∆A)

31 if (ϱA

L, ϱA

R) ≠(∅,∅) then break

32 A ∶= A ∪∆A 33 NA ∶= Π⟨unfold(I) ∪A ⋮∆A⟩

34 A ∶= ⟨A,ϱA

L,ϱA

R ⟩, I ∶= I ⋓A

## Algorithm

Overview Our incremental materialisation maintenance algorithm for DatalogMTL is formalised in Algorithm 1. The algorithm takes as input a program Π, a dataset E, a periodic materialisation I of (Π,E), a dataset E−to be removed from E, and a dataset E+ to be added to E, and it updates I such that after the execution of the algorithm, I becomes a periodic materialisation of (Π,(E ∖E−) ∪E+), and this is achieved without recomputing the periodic materialisation from scratch. Similar to the DRed algorithm for plain Datalog, Algorithm 1 consists of three stages, which we outline below.

In the overdeletion stage, the dataset D is extended with all facts that depend on the deleted facts. The algorithm then applies the rules of Π iteratively (line 11) until a pair of periods are found (line 9–10). Line 11 makes use of our newly devised seminaïve evaluation operator Π⟨I ⋮∆⟩, which computes the union of all facts derived by (rσ,t)⟨I ⋮∆⟩, where rσ is a ground rule instance with r a rule in Π and σ a substitution mapping each variable appearing in r to a constant appearing in I, and t is a rational time point; operator (r′,t)⟨I ⋮∆⟩where r′ is a ground rule instance and t is a rational time point is in turn deﬁned as the minimal set of punctual facts N such that II,t ⊧body(r′), II∖∆,t /⊧body(r′), and IN,t ⊧head(r′). When I and ∆are ﬁnite, Π⟨I ⋮∆⟩can be efﬁciently evaluated by instantiating the query from facts inside ∆, which is typically much smaller than I. However, in line 21, by slight abuse of notation, we use unfold(I) ∖D as an operand of the operator: this does not mean that we have to compute the entire unfolding of I prior to the execution of the operator. In contrast, the evaluation is still instantiated from from facts in ∆, while interpretation I can be unfolded lazily as required.

In the rederivation stage, the algorithm recovers the facts that were overdeleted but should actually still hold after the update. It should be noted that overdeleted facts may span the entire timeline, and so it may not be sufﬁcient to recover facts within a ﬁxed interval. Lines 17–19 address this issue, in each round of the loop of lines 16–24, we extend the interval of interest [tL,tR] so that overdeleted facts inside this interval could be successfully recovered (line 19); this is done in parallel to the propagation of already recovered facts (line 24). The loop terminates when a pair of periods are successfully identiﬁed (lines 21–22), and the periodic materialisation I is updated in line 25.

Insertion is analogous to deletion: the dataset A is populated with new facts that are derivable from E+. In parallel to consequence propagation, the algorithm tries to detect the periodic structure within the dataset A. Ultimately, the algorithm updates the periodic materialisation in line 34 to incorporate the inserted facts and their consequences.

Period Identiﬁcation The PDS procedure formalised in Algorithm 2 identiﬁes the repeating patterns within a dataset being populated during iterative application of rules. More speciﬁcally, it takes as input a program Π, a dataset E, intervals ϱL and ϱR, the dataset being popuplated D, and a set of new facts ∆D that are to be integrated into D after period detection. The procedure ﬁrst examines facts in ∆D: if there is a fact in ∆D that overlaps with the interval [t−

E,t+

E], it means facts inside this interval have not stabilised, and so the procedure terminates. Otherwise, u and v will be computed separately (lines 5–6) such that [u,v] is largest interval containing [t−

E,t+

E] and does not contain a fact satis- ﬁed by I∆D. Now if [u,v] is nonempty, we search for the left and right periods with endpoints on the (Π,E)−ruler in γL = (u,ϱ+

L + 2depth(Π)] and γR = [ϱ− right −2depth(Π),v), respectively (lines 9–16). The procedure returns the pair of periods (ϱ′

L,ϱ′

R), or (∅,∅) if no valid period is detected at either end (lines 17–18). Intuitively, the algorithm requires ϱ1,ϱ2 (resp., ϱ3,ϱ4) to be a multiple of ∣ϱL∣(resp., ∣ϱR∣) apart so that it would be convenient align the new periods with the given ones.

19471

<!-- Page 6 -->

## Algorithm

2: PDS(Π,E,ϱL,ϱR,D, ∆D)

Input: program Π, dataset E, intervals ϱL and ϱR, dataset D of facts derived so far, and dataset ∆D of facts derived in the last round

1 ϱ′ L ∶= ϱ′

R ∶= ∅, P ∶= (Π,E)-ruler

2 foreach Mσ@ϱ ∈∆D do

3 if ϱ ∩[t−

E,t+

E] ≠∅then

4 return (∅,∅)

5 u = max({x < t− E ∣∃y,M@⟨y,x⟩∈∆D} ∪{−∞})

6 v = min({x > t+ E ∣∃y,M@⟨x,y⟩∈∆D} ∪{∞})

7 γL ∶= (u, ϱ+

L + 2depth(Π)]

8 γR ∶= [ϱ− R −2depth(Π), v)

9 foreach ϱ1,ϱ2 ⊆γL with ∣ϱ1∣= ∣ϱ2∣= 2depth(Π) do

10 if ϱ−

1 < ϱ− 2,ϱ− 1 ∈P and ϱ− 2 ≡ϱ− 1 mod ∣ϱL∣then

11 if ID ∣ϱ1 is a shift of ID ∣ϱ2 then

12 ϱ′

L ∶= [ϱ−

1,ϱ− 2)

13 foreach ϱ3,ϱ4 ⊆γR with ∣ϱ3∣= ∣ϱ4∣= 2depth(Π) do

14 if ϱ+

3 < ϱ+ 4,ϱ+ 3 ∈P and ϱ+ 3 ≡ϱ+ 4 mod ∣ϱR∣then

15 if ID ∣ϱ3 is a shift of ID ∣ϱ4 then

16 ϱ′

R ∶= (ϱ+

3,ϱ+ 4]

17 if ϱ′ L = ∅or ϱ′

R = ∅then return (∅,∅)

18 else return (ϱ′ L,ϱ′

R)

## Algorithm

3: Implementation of Periodic Minus

Input: Two periodic materialisations D1 and D2

1 if D2.ϱL then

2 (D1,D2) ∶= Ext(D1,D2,L)

3 (D1,D2,ϱL) ∶= Aln(D1,D2,L)

4 else ϱL ∶= D1.ϱL 5 if D2.ϱR then

(D1,D2) ∶= Ext(D1,D2,R)

7 (D1,D2,ϱR) ∶= Aln(D1,D2,R)

8 else ϱR ∶= D1.ϱR 9 I ∶= D1.I ∖D2.I

10 return ⟨I,ϱL,ϱR⟩

Implementation of Periodic Operators Algorithm 1 has made frequent use of operators ∖∖and ⋓, which are responsible for taking the difference and union of two periodic materialisations, respectively. In practice, these two operators can be implemented arbitrarily, so long as unfold(D1) −unfold(D2) = unfold(D1 ∖∖D2) and unfold(D1) ∪unfold(D2) = unfold(D1 ⋓D2). Next we describe our implementation of these operators, which utilises two auxiliary functions, Ext and Aln, responsible for extending and aligning periodic materialisations, respectively.

Consider two periodic materialisations D1 and D2, and let end ∈{L,R} denote which end of the periodic materialisation to operate on (either left or right). Given periodic materialisations D1 and D2 which both have valid (but potentially different) periods ϱend, function Ext computes a pair of periodic materialisations (D′

1,D′ 2) = Ext(D1,D2,end) such that the periodic regions are extended to have the same

## Algorithm

4: Implementation of Periodic Union

Input: Two periodic materialisations D1 and D2

1 ϱL ∶= ϱR ∶= ∅

2 if D1.ϱL and D2.ϱL then

3 (D1,D2) ∶= Ext(D1,D2,L)

4 if D1.ϱL or D2.ϱL then

5 (D1,D2,ϱL) ∶= Aln(D1,D2,L)

6 if D1.ϱR and D2.ϱR then

7 (D1,D2) ∶= Ext(D1,D2,R)

8 if D1.ϱR or D2.ϱR then

9 (D1,D2,ϱR) ∶= Aln(D1,D2,R)

10 I ∶= D1.I ∪D2.I

11 return ⟨I,ϱL,ϱR⟩ length, which is the least common multiple (LCM) of the two; this can be easily achieved by copying the relevant periodic segments of the timeline. In contrast, function Aln tries to align the start and end points of periodic intervals of the two periodic materialisations at the target end, again through facts copying. If only one of the two periodic operators has a valid ϱend, an empty period is introduced for the other periodic materialisation so that alignment can still be performed. It should be noted that both Ext and Aln operations preserve the semantics of the interpretations: they do not change which facts hold at any time point but only alters the ﬁnite representations of the input periodic materialisations.

Theorem 1 states that Algorithms 3 and 4 correctly implement operators ∖∖and ⋓, respectively; Theorem 2 states that Algorithm 1 is correct. The full proofs for these theorems are lengthy, so we only provide proof sketches; the full proofs are given in the online technical report. Theorem 1. If given input D1,D2, Algorithm 3 and 4 output Dm and Du, respectively, then unfold(D1) −unfold(D2) = unfold(Dm) and unfold(D1) ∪unfold(D2) = unfold(Du)

Proof Sketch. For minus, we show that the equation holds by leveraging that the periods of unfold(D1) and unfold(D2) can be extended and aligned to form a new pair of periods, and their difference also abides by the new periods. The case for union is similar.

Theorem 2. For a bounded DatalogMTL program Π, a bounded dataset E, a bounded deleting dataset E−, a bounded inserting dataset E+, a periodic materialisation I such that unfold(I) = CΠ,E, let E′ = E∖E−∪E+, then after calling DREDMT L(Π,E,E−,E+,I), we have unfold(I) = CΠ,E′

Proof Sketch. We ﬁrst show that unfold(D) computed by the OVERDELETE contains CΠ,E −CΠ,E∖E−∪E+, which means every fact that no longer holds because of deleting E−will be removed, and then we show that the union of unfold(R),unfold(A) computed by the REDERIVE,INSERT and unfold(I) after deletion equals CΠ,E∖E−∪E+, which involves proving mistakenly deleted facts are rederived and every new fact that holds because of E+ are inserted.

19472

<!-- Page 7 -->

## Evaluation

We implemented the proposed DRedMTL algorithm based on an efﬁcient DatalogMTL reasoner MeTeoR (Wang et al. 2022) and empirically tested the performance of our implementation on three publicly available datasets. We chose MeTeoR as its latest version supports materialisation for DatalogMTL with bounded intervals (Wałe¸ga et al. 2023), which allows us to directly compare the performance of DRedMTL with rematerialisation from scratch. The source code of our implementation, the benchmarks we used, as well as an extended technical report containing all detailed proofs, are available online.

Benchmarks LUBMt (Wang et al. 2022) is a temporal version of the well-known LUBM benchmark (Guo, Pan, and Heﬂin 2005). It has a recursive program consisting of 85 rules, of which 29 have temporal operators in them (denoted as ∣Πmtl∣) and 56 do not (denoted as ∣Πno_mtl∣). The iTemporal dataset is generated from a temporal benchmark generator developed by Bellomarini, Nissl, and Sallinger (2022). Its program is highly recursive and consists of 12 rules. Finally, the Meteorological dataset (Maurer et al. 2002) contains long-term meteorological observations. It has a nonrecursive program consisting of four rules, of which two contain temporal operators. These datasets were collected and made publicly available by Wang et al. (2025), and we used them without any modiﬁcation. The statistics of these datasets is given in Table 2, where ∣E∣and ∣I∣are the number of explicitly given facts and the number of facts in the saturated interpretation, respectively. The ratio between ∣I∣ and ∣E∣is usually a good indicator of the recursiveness of the corresponding rule set: the larger the ratio is, the more recursive and complex the rule set is and the more likely it is to generate a greater number of facts. Indeed, our choice of benchmarks is a nice mixture of highly recursive (iTemporal), mildly recursive (LUBMt) and nonrecursive datasets, which allows us to test the potential of our reasoning algorithm in different possible application scenarios.

Test Settings We conducted our experiment on a server with 256GB RAM and an Intel Xeon Platinum 8269CL 2.50GHz CPU, running Fedora Linux 40, kernel version Linux 6.10.10-200.fc40.x86_64. Our evaluation primarily examines the capabilities of DRedMTL in handling both deletions and insertions. Table 3 summarises the performance

LUBMt iTemporal Meteorological

∣Πmtl∣ 29 3 2

∣Πno_mtl∣ 56 8 2

∣Π∣ 85 11 4

Recursive Yes Yes No

∣E∣ 630.5k 46.41k 62.01M

∣I∣ 1.426M 30.62M 62.48M

**Table 2.** Dataset Statistics

comparison of our algorithm against rematerialisation. For our approach, we record the wall-clock time of running Algorithm 1 to handle the updates. For the baseline, we record the wall-clock time that MeTeoR spends on computing the canonical representation over the updated set of explicitly given facts from scratch. In addition to the time metrics, to better reﬂect the workload of DRedMTL, we also record the number of facts derived in the three stages of our algorithm, i.e., overdeletion (∣D∣), rederivation (∣R∣) and insertion (∣A∣). Note that for insertion, the sets of overdeleted and rederived facts are always empty, so we only record the number of inserted facts, ∣A∣.

Our evaluation considers both small-scale and large-scale updates. For small-scale update tests, we randomly selected 100 facts and ran DRedMTL to deal with the deletion; then we added these facts back and recorded the time DRedMTL took to handle the insertion. Large-scale tests were performed in a similar fashion, except that 10% of the original dataset were removed and added back; the exact numbers of deleted facts are shown in Table 3. For each test case, three test runs with different (randomly selected) updates were performed; the results showed no signiﬁcant variation in terms of running time. Therefore, for the ease of presentation we only reported the results of one run for each test case. Finally, for each test run, we made sure that the periodic materialisation produced by DRedMTL (I1) is equivalent to that produced by rematerialisation (I2): this is achieved by verifying that both I1 ∖∖I2 and I2 ∖∖I1 are empty.

## Results

Our evaluation shows that DRedMTL consistently outperforms rematerialisation for all small deletions and insertions. As shown in Table 3, on LUBMt, DRedMTL is 69.4 times faster than the baseline for small deletion, and 121.3 times faster for small insertion. On the nonrecursive Meteorological dataset, DRedMTL achieves similar performance improvement for small updates. On iTemporal, the performance improvement is more modest: the speedup is around six times. This is so since the program of iTemporal is highly recursive, making incremental maintenance especially challenging: as one can see, deleting only 100 facts leads to the overdeletion of over 244 thousand facts.

For large updates, DRedMTL achieved a signiﬁcant performance boost on the LUBMt and iTemporal datasets. When deleting 10% of the data, DRedMTL is 13.2 times faster on LUBMt and 4.2 times faster on iTemporal. For large insertion, the improvements are 43.8 and 4.2 times, respectively. Interestingly, on the Meteorological dataset, DRedMTL is slower than rematerialisation in dealing with large updates. Notice that for this dataset, the ratio between ∣I∣and ∣E∣is rather small, as depicted in Table 2, indicating that only a small fraction of the materialisation are inferred facts; moreover, the program is nonrecursive, so no effort is required for identifying the repeating pattern inside the materialisation. As such, for large updates on this dataset, DRedMTL, which is based on efﬁcient seminaive reasoning and period identiﬁcation, losts its advantage.

To further analyse the performance of the proposed algorithm, we proﬁled our system on the deletion test cases and reported the runtime breakdown (by stage of reason-

19473

<!-- Page 8 -->

‘Remat’ stands for Rematerialisation from the updated set of explicitly given facts.

Dataset ∣E±∣

Deletion Insertion DREDMT L Remat DREDMT L Remat Time(s) ∣D∣ ∣R∣ ∣A∣ Time(s) Time(s) ∣A∣ Time(s)

LUBMt 100 0.7k 11.5k 1.5k 11.4k 48.6k 0.4k 0.2k 48.5k 63.1k 3.4k 372.1k 143.5k 251.9k 45.0k 1.1k 190.2k 48.2k iTemporal 100 8.1k 244.5k 274.0k 274.4k 52.7k 8.7k 231.2k 52.8k 4.6k 12.6k 8.963M 1.286M 1.288M 52.3k 12.4k 7.829M 52.6k

Meteorological 100 10 102 1 1 0.7k 11 101 0.7k 6.201M 1.4k 6.271M 0.7k 1.2k 6.270M 0.7k

**Table 3.** Evaluation Results

Dataset ∣E−∣ Overdeletion Rederivation Insertion

LUBMt 100 59.0% 2.4% 38.6% 63.1k 15.7% 67.9% 16.4% iTemporal 100 70.5% 10.6% 18.9% 4.6k 64.2% 29.9% 5.9%

Meteorological 100 62.8% 21.8% 15.4% 6.201M 92.2% 7.7% 0.1%

**Table 4.** Deletion Test Runtime Breakdown

ing) in Table 4. It could be readily observed that in most cases, overdeletion is the most time consuming step of the algorithm. This is so since overdeletion produces the largest number of facts across the three stages. The only exception is the case of large deletion for LUBMt: rederivation consumes more time than overdeletion and insertion combined. Indeed, although rederivation produces less facts than overdeletion, it involves evaluating rules ‘backwards’ from head to body, which, as observed by Hu, Motik, and Horrocks (2018), could be more expensive than the seminaïve evaluation taking place in overdeletion and insertion. In the Datalog setting, enhancing rederivation with counting could help alleviate this issue, but extending the counting technique to DatalogMTL is beyond the scope of this paper.

Overall our test results suggest that the proposed algorithm improves substantially and consistently over rematerialisation, for both small and large updates. In some test cases, the running time decreased from several hours to several minutes, or from an hour to a few seconds, demonstrating the potential of deploying the proposed approach in industrial applications where short service response time is highly desirable.

## Conclusion and Future Work

In this paper, we have introduced a new technique for incrementally updating DatalogMTL materialisations. Compared with recomputing the materialisation from scratch, our technique achieves signiﬁcant performance improvements, especially when the updates are small.

We see many exciting future research directions. From a practical perspective, it would be interesting to see how well the proposed approach works in industrial scenarios such as IoT anomaly detection (Zhang et al. 2024): in typical such applications, DatalogMTL can be used to model anomaly detection rules that are triggered by streams composed of timestamped sensor data; the ability to reason incrementally offered by our method is crucial for ensuring efﬁcient and reliable fault alerts. Moreover, we shall consider comparing the performance of our system with well-established stream reasoning frameworks such as C-SPARQL (Barbieri et al. 2009) and CQELS (Phuoc et al. 2011). While the underlying languages are quite different, it should be possible to transform our reasoning workload (at least the nonrecursive cases) to a C-SPARQL or CQELS workload, and test it on the corresponding engine. Last but not least, DRed is not the only incremental update algorithm for Datalog materialisations; algorithms such as B/F, FBF, and DRedc are popular alternatives of DRed and sometimes offer superior performance. It would thus be useful to consider extending these incremental maintenance algorithms for Datalog to support DatalogMTL reasoning, and to compare the performance of the adapted algorithms with that of ours.

## Acknowledgements

This work was generously funded by National Science and Technology Major Project of China under grant number 2025ZD1600800 and National Natural Science Foundation of China under grant number 62206169. We thank the anonymous reviewers for their constructive comments that helped greatly in shaping the ﬁnal version of this paper.

19474

<!-- Page 9 -->

## References

Barbieri, D. F.; Braga, D.; Ceri, S.; Della Valle, E.; and Grossniklaus, M. 2009. C-SPARQL: SPARQL for continuous querying. In Proceedings of the 18th International Conference on World Wide Web, WWW ’09, 1061–1062. New York, NY, USA: Association for Computing Machinery. ISBN 9781605584874. Bellomarini, L.; Nissl, M.; and Sallinger, E. 2022. iTemporal: An Extensible Generator of Temporal Benchmarks. In International Conference on Data Engineering, ICDE 2022, 2021–2033. Brandt, S.; Kalaycı, E. G.; Kontchakov, R.; Ryzhikov, V.; Xiao, G.; and Zakharyaschev, M. 2017. Ontology-based data access with a horn fragment of metric temporal logic. In Proceedings of the Thirty-First AAAI Conference on Artiﬁcial Intelligence, AAAI’17, 1070–1076. AAAI Press. Brandt, S.; Kalayci, E. G.; Ryzhikov, V.; Xiao, G.; and Zakharyaschev, M. 2018. Querying Log Data with Metric Temporal Logic. J. Artif. Intell. Res., 62: 829–877. Ceri, S.; Gottlob, G.; and Tanca, L. 1989. What you Always Wanted to Know About Datalog (And Never Dared to Ask). IEEE Trans. Knowl. Data Eng., 1(1): 146–166. Colombo, A.; Bellomarini, L.; Ceri, S.; and Laurenza, E. 2023. Smart Derivative Contracts in DatalogMTL. In International Conference on Extending Database Technology, EDBT, 773–781. Guo, Y.; Pan, Z.; and Heﬂin, J. 2005. LUBM: A benchmark for OWL knowledge base systems. J. Web Semant., 3(2-3): 158–182. Gupta, A.; Mumick, I. S.; and Subrahmanian, V. S. 1993. Maintaining views incrementally. In Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data, SIGMOD ’93, 157–166. New York, NY, USA: Association for Computing Machinery. ISBN 0897915925. Güzel Kalayci, E.; Xiao, G.; Ryzhikov, V.; Kalayci, T. E.; and Calvanese, D. 2018. Ontop-temporal: a tool for ontology-based query answering over temporal data. In ACM International Conference on Information and Knowledge Management, 1927–1930. Hu, P.; Motik, B.; and Horrocks, I. 2018. Optimised Maintenance of Datalog Materialisations. In McIlraith, S. A.; and Weinberger, K. Q., eds., Proceedings of the Thirty-Second AAAI Conference on Artiﬁcial Intelligence, New Orleans, Louisiana, USA, February 2-7, 2018, 1871–1879. AAAI Press. Koymans, R. 1990. Specifying Real-Time Properties with Metric Temporal Logic. Real Time Syst., 2(4): 255–299. Maurer, E. P.; Wood, A. W.; Adam, J. C.; Lettenmaier, D. P.; and Nijssen, B. 2002. A Long-Term Hydrologically Based Dataset of Land Surface Fluxes and States for the Conterminous United States. Journal of Climate, 15(22): 3237 – 3251. Mori, M.; Papotti, P.; Bellomarini, L.; and Giudice, O. 2022. Neural Machine Translation for Fact-checking Temporal Claims. In Fact Extraction and VERiﬁcation Workshop, 78– 82.

Motik, B.; Nenov, Y.; Piro, R.; and Horrocks, I. 2015. Incremental update of datalog materialisation: the backward/forward algorithm. In Proceedings of the Twenty-Ninth AAAI Conference on Artiﬁcial Intelligence, AAAI’15, 1560–1568. AAAI Press. ISBN 0262511290. Motik, B.; Nenov, Y.; Piro, R.; and Horrocks, I. 2019. Maintenance of datalog materialisations revisited. Artiﬁcial Intelligence, 269: 76–136. Nissl, M.; and Sallinger, E. 2022. Modelling Smart Contracts with DatalogMTL. In Workshops of the EDBT/ICDT, volume 3135. Phuoc, D. L.; Dao-Tran, M.; Parreira, J. X.; and Hauswirth, M. 2011. A Native and Adaptive Approach for Uniﬁed Processing of Linked Streams and Linked Data. In Aroyo, L.; Welty, C.; Alani, H.; Taylor, J.; Bernstein, A.; Kagal, L.; Noy, N. F.; and Blomqvist, E., eds., The Semantic Web - ISWC 2011 - 10th International Semantic Web Conference, Bonn, Germany, October 23-27, 2011, Proceedings, Part I, volume 7031 of Lecture Notes in Computer Science, 370– 388. Springer. Ren, Y.; and Pan, J. Z. 2011. Optimising ontology stream reasoning with truth maintenance system. In Proceedings of the 20th ACM International Conference on Information and Knowledge Management, CIKM ’11, 831–836. New York, NY, USA: Association for Computing Machinery. ISBN 9781450307178. Staudt, M.; and Jarke, M. 1996. Incremental Maintenance of Externally Materialized Views. In Proceedings of the 22th International Conference on Very Large Data Bases, VLDB ’96, 75–86. San Francisco, CA, USA: Morgan Kaufmann Publishers Inc. ISBN 1558603824. Urbani, J.; Margara, A.; Jacobs, C.; van Harmelen, F.; and Bal, H. 2013. DynamiTE: Parallel Materialization of Dynamic RDF Data. In Alani, H.; Kagal, L.; Fokoue, A.; Groth, P.; Biemann, C.; Parreira, J. X.; Aroyo, L.; Noy, N.; Welty, C.; and Janowicz, K., eds., The Semantic Web – ISWC 2013, 657–672. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-642-41335-3. Wałe¸ga, P.; Kaminski, M.; and Cuenca Grau, B. 2019. Reasoning over Streaming Data in Metric Temporal Datalog. In The Thirty-Third AAAI Conference on Artiﬁcial Intelligence, AAAI 2019, The Thirty-First Innovative Applications of Artiﬁcial Intelligence Conference, IAAI 2019, The Ninth AAAI Symposium on Educational Advances in Artiﬁcial Intelligence, EAAI 2019, Honolulu, Hawaii, USA, January 27 - February 1, 2019, 3092–3099. AAAI Press. Wałe¸ga, P. A.; Zawidzki, M.; Wang, D.; and Cuenca Grau, B. 2023. Materialisation-Based Reasoning in DatalogMTL with Bounded Intervals. In AAAI Conference on Artiﬁcial Intelligence, 6566–6574. Wał˛ega, P. A.; Kaminski, M.; Wang, D.; and Grau, B. C. 2023. Stream reasoning with DatalogMTL. Journal of Web Semantics, 76: 100776. Wang, D.; Hu, P.; Wałe¸ga, P. A.; and Cuenca Grau, B. 2022. MeTeoR: Practical Reasoning in Datalog with Metric Temporal Operators. In AAAI Conference on Artiﬁcial Intelligence, 5906–5913.

19475

<!-- Page 10 -->

Wang, S.; Zhao, K.; Wei, D.; Walega, P. A.; Wang, D.; Cai, H.; and Hu, P. 2025. Goal-Driven Reasoning in DatalogMTL with Magic Sets. In Walsh, T.; Shah, J.; and Kolter, Z., eds., The Thirty-Ninth AAAI Conference on Artiﬁcial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA, 15203–15211. AAAI Press. Zhang, F.; Hu, P.; Cai, H.; and Jiang, L. 2024. Parallel Collaborative Reasoning Approaches Based on DatalogMTL in IoT Scenarios. In 2024 27th International Conference on Computer Supported Cooperative Work in Design (CSCWD), 1055–1060.

19476
