---
title: "Convergent Semantics for Weighted Bipolar Argumentation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39019
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39019/42981
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Convergent Semantics for Weighted Bipolar Argumentation

<!-- Page 1 -->

Convergent Semantics for Weighted Bipolar Argumentation

Zongshun Wang, Yuping Shen

Institute of Logic and Cognition

Department of Philosophy Sun Yat-sen University, P.R. China wangzsh27@mail.sysu.edu.cn, shyping@mail.sysu.edu.cn

## Abstract

Establishing convergent semantics for weighted argumentation graphs is a long-standing fundamental issue. Particularly, it is challenging to develop convergent semantics for weighted bipolar argumentation graphs (wBAG), which include both support and attack relations on weighted arguments. Existing semantics in the literature are not general enough in the sense that they only apply to acyclic graphs or special cyclic cases. In this paper, we provide an elegant solution to this issue by adopting the so-called bilateral gradual semantics, so that the strength of arguments can be defined as the limits of iterative functions that always converge for any wBAG including cyclic ones. A preliminary experimental analysis shows that our semantics appear quite efficient in calculating argument strength. Overall, this paper offers a solid and promising foundation for weighted bipolar argumentation in theoretical and practical aspects.

## Introduction

An argumentation graph is a computational model for reasoning and decision-making in complex environments (Dung 1995; Amgoud and Prade 2009; Atkinson et al. 2017). In recent years, establishing convergent semantics has emerged as a compelling and influential approach for evaluating weighted arguments (Gabbay and Rodrigues 2015; Amgoud, Doder, and Vesic 2022; Besnard and Hunter 2001; Prakken 2024). The basic idea is to introduce iterative functions that take graphs as inputs and produce sequences of values that eventually converge. The final value assigned to arguments is called the strength or acceptability degree. This approach has numerous applications such as belief revision (da Costa Pereira, Tettamanzi, and Villata 2011), social network (Leite and Martins 2011), explainability (Potyka 2021), etc.

Weighted bipolar argumentation graphs (wBAG) consider both support and attack relations on weighted arguments. Such bipolar graphs have received extensive attention due to their versatile expressive power (Amgoud et al. 2008; Cayrol and Lagasquie-Schiex 2005; Polberg and Hunter 2018), with applications spanning engineering design (Baroni et al. 2015), polling (Rago and Toni 2017),

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

review aggregation (Rago et al. 2025), etc. However, developing convergent semantics for wBAG has long been challenging. Most semantics in the literature fail to converge in cyclic graphs (Evripidou and Toni 2014; Baroni et al. 2015; Rago et al. 2016; Amgoud and Ben-Naim 2018b; Potyka 2021; Doder, Vesic, and Croitoru 2021; Rago et al. 2024). The only exception (Mossakowski and Neuhaus 2018) introduces a restricted semantics that considers only the strongest supporter and attacker, which is less open-minded (Potyka 2019a,b). As pointed out in (Amgoud and Ben-Naim 2018b; Potyka 2018; Potyka and Booth 2024b; Yin, Potyka, and Toni 2024), an urgent task is to define semantics that are capable of dealing with any typology of graphs including cyclic ones.

To address this issue, we adopt the so-called bilateral gradual semantics (Wang and Shen 2024) for wBAG, where each argument is assigned two degrees—acceptability and rejectability—to capture both the positive and negative strength, reflecting a common cognitive evaluation process (Cacioppo, Gardner, and Berntson 1997). Naturally, the support and attack relations are separately measured through the acceptability and rejectability degrees in wBAG. This philosophy robustly leads to convergent semantics through iterative functions, laying a solid foundation for well-behaved wBAG semantics.

Towards this end, we first investigate the principles for well-behaved wBAG semantics. We incorporate widelyadopted principles from unipolar support graphs (Amgoud and Ben-Naim 2016), unipolar attack graphs (Amgoud et al. 2017), and bipolar graphs (Amgoud and Ben-Naim 2018b). Particularly, we include three notable principles—Quality Precedence, Cardinality Precedence and Compensation— which are known for developing semantics for unipolar graphs, yet to the best of our knowledge, have never been studied for bipolar graphs. Accordingly, we propose three convergent semantics, each defined as the limit of iterative functions that always converge for any wBAG including cyclic ones. Each semantics corresponds to one of the above three notable principles and satisfies most widely adopted principles. A preliminary experimental analysis shows that the performance of our semantics appears quite efficient concerning the number of iterations and the running time for calculating argument strength.

This paper is organized as follows. We first introduce

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19415

<!-- Page 2 -->

basic concepts concerning wBAG and bilateral gradual semantics. Next, we illustrate desirable principles for wBAG semantics and study their interrelation. Then we present our main contribution, i.e., three wBAG semantics that converge for arbitrary graphs including cyclic ones. Satisfied principles are summarized in Table 2 and preliminary experimental results are depicted in Figure 1. The paper ends with a discussion and conclusion.

## Preliminaries

A weighted bipolar argumentation graph consists of support and attack relations on a set of arguments. Each argument is assigned a basic weight from the real interval [0, 1]. Definition 1 (wBAG). A weighted bipolar argumentation graph (wBAG) is a quadruple G = ⟨A, w, S, R⟩, where A is a non-empty finite set of arguments, w is a function from A to [0, 1], S ⊆A × A and R ⊆A × A.

Given two arguments a, b ∈A, (a, b) ∈S means a supports b and (a, b) ∈R means a attacks b. By w(a) we denote the basic weight of a, which may represent various measures such as trustworthiness (da Costa Pereira, Tettamanzi, and Villata 2011), votes (Leite and Martins 2011), probability of beliefs (Hunter 2013), etc.

In this paper, arguments are evaluated through the bilateral gradual semantics which assigns each argument an acceptability degree and a rejectability degree. Definition 2 (Bilateral gradual semantics). A bilateral gradual semantics is a function S transforming G = ⟨A, w, S, R⟩to a function DegS

G defined from A to [0, 1] × [0, 1]. For any a ∈A, DegS

G(a) = (σ+

G(a), σ−

G(a)) where σ+

G(a) and σ−

G(a) represent the acceptability and rejectability degrees of a respectively.

When the context is clear, we simply write Deg (resp. σ+, σ−) instead of DegS

G (resp. σ+

G, σ−

G). Below, we present some notations used in the paper. Let G = ⟨A, w, S, R⟩and a ∈A. SupG(a) denotes the set of all supporters of a, i.e., SupG(a) = {b ∈A | (b, a) ∈S}. AttG(a) denotes the set of all attackers of a, i.e., AttG(a) = {b ∈A | (b, a) ∈R}. We say that a is non-supported if SupG(a) = ∅and nonattacked if AttG(a) = ∅. We may abbreviate AttG(a) as Att(a) and SupG(a) as Sup(a). For G = ⟨A, w, S, R⟩and G′ = ⟨A′, w′, S′, R′⟩s.t. A∩A′ = ∅, we define G⊕G′ = ⟨A ∪A′, w∗, S ∪S′, R ∪R′⟩where for any a ∈A (resp. a ∈A′), w∗(a) = w(a) (resp. w∗(a) = w′(a)).

Principles Principles represent a set of desirable properties that semantics usually need to satisfy in practical applications, serving as a guideline for exploring semantics. Numerous studies have investigated the principles that consider only the acceptability degree (Amgoud and Ben-Naim 2018a; Baroni, Rago, and Toni 2018, 2019; Amgoud, Doder, and Vesic 2022; Bonzon et al. 2016). Principles for bilateral gradual semantics in unipolar attack graphs were proposed in (Wang and Shen 2024). Based on this bilateral philosophy, we study the principles that simultaneously take into account the acceptability and rejectability degrees in wBAG.

We provide a total of 23 principles, which integrate and adapt the well-established principles from unipolar support graphs (Amgoud and Ben-Naim 2016), unipolar attack graphs (Amgoud et al. 2017), and bipolar graphs (Amgoud and Ben-Naim 2018b). Some principles are basic ones, e.g., Anonymity, Resilience, Proportionality. There is also a set of symmetric principles that consider how supporters and attackers respectively influence the acceptability and rejectability degrees of arguments, e.g., A-Counting, R-Counting, A-Reinforcement, R-Reinforcement. We also incorporate three notable principles—Quality Precedence, Cardinality Precedence and Compensation—which serve as strategies for defining semantics in unipolar graphs, yet have never been studied in bipolar graphs.

**Table 1.** illustrates the sources of acceptability and rejectability degrees. Intuitively, the former is determined by supporters and basic weight, while the latter is solely determined by attackers. Such a bilateral and non-reciprocal setting originates from (Wang and Shen 2024) for unipolar graphs. Here we lift the idea for bipolar graphs, and this turns out to be a cornerstone for developing convergent semantics.

Degree Source

• basic weight acceptability • acceptability degree of supporters • rejectability degree of supporters rejectability • acceptability degree of attackers • rejectability degree of attackers

**Table 1.** Sources of acceptability and rejectability degrees

The notions of Isomorphism and Path will be used to establish principles.

Definition 3 (Isomorphism). Consider G = ⟨A, w, S, R⟩ and G′ = ⟨A′, w′, S′, R′⟩. An isomorphism from G to G′ is a bijective function f from A to A′ s.t. (i) ∀a ∈A, w(a) = w′(f(a)), (ii) ∀a, b ∈A, (a, b) ∈S iff (f(a), f(b)) ∈S′, (iii) ∀a, b ∈A, (a, b) ∈R iff (f(a), f(b)) ∈R′.

Definition 4 (Path). We say that there is a path from a1 to an iff there is a sequence consisting of {a1,..., an} s.t. (ai, ai+1) ∈R ∪S for any i ∈{1,..., n −1}.

Anonymity. The acceptability and rejectability degrees of an argument are independent of its identity. Formally: (1) For any G = ⟨A, w, S, R⟩and G′ = ⟨A′, w′, S′, R′⟩, for any isomorphism f from G to G′, we have ∀a ∈A, σ+

G(a) = σ+

G′(f(a)), σ−

G(a) = σ−

G′(f(a)). Independence. The acceptability and rejectability degrees of an argument should be independent of any argument that is not connected to it. (2) For any G = ⟨A, w, S, R⟩and G′ = ⟨A′, w′, S′, R′⟩ s.t. A ∩A′ = ∅, we have ∀a ∈A, σ+

G(a) = σ+

G′⊕G(a), σ−

G(a) = σ−

G′⊕G(a). Directionality. The acceptability and rejectability degrees of an argument a depend on argument b only if there is a path from b to a.

19416

<!-- Page 3 -->

(3) For any G = ⟨A, w, S, R⟩and G′ = ⟨A, w, S′, R′⟩s.t. S ⊆S′, R ⊆R′, R′ ∪S′ = R ∪S ∪{(a, b)}, ∀x ∈ A, if there is no path from b to x, then σ+

G(x) = σ+

G′(x), σ−

G(x) = σ−

G′(x).

Equivalence. The acceptability degree of an argument only depends on the acceptability and rejectability degrees of its supporters, as well as its basic weight; (ii) The rejectability degree only depends on the acceptability and rejectability degrees of its attackers. (4) For any G = ⟨A, w, S, R⟩, ∀a, b ∈A,

• if w(a) = w(b), and there exists a bijective function f from Sup(a) to Sup(b) s.t. ∀x ∈Sup(a), σ+(x) = σ+(f(x)), σ−(x) = σ−(f(x)), then σ+

G(a) = σ+

G(b);

• if there exists a bijective function f ′ from Att(a) to Att(b) s.t. ∀x ∈Att(a), σ+(x) = σ+(f ′(x)), σ−(x) = σ−(f ′(x)), then σ−

G(a) = σ−

G(b).

Resilience. If the basic weight of an argument lies in (0, 1), then its acceptability degree also lies in (0, 1). (5) If 0 < w(a) < 1, then 0 < σ+(a) < 1.

Proportionality. The higher the basic weight of an argument, the higher its acceptability degree. (6) If (i) w(a) < w(b), (ii) σ+(a) < 1 or σ+(b) < 1, and (iii) Sup(a) = Sup(b), then σ+(a) < σ+(b).

The following principles consider how supporters and attackers respectively determine the acceptability and rejectability degrees of arguments. We say an argument a is worthless if σ+(a) = 0 and alive if σ+(a) > 0. A-Neutrality. A worthless supporter has no impact on the acceptability degree of the supported argument. (7) If (i) w(a) = w(b), (ii) Sup(a) = Sup(b) \ {x} with x ∈Sup(b), (iii) σ+(x) = 0, then σ+(a) = σ+(b).

R-Neutrality. A worthless attacker has no impact on the rejectability degree of the attacked argument. (8) If (i) Att(a) = Att(b) \ {x} with x ∈Att(b), (ii) σ+(x) = 0, then σ−(a) = σ−(b).

A-Stability. The acceptability degree of a non-supported argument is equal to its basic weight. (9) If Sup(a) = ∅, then σ+

G(a) = w(a).

R-Stability. The rejectability degree of a non-attacked argument is 0. (10) If Att(a) = ∅, then σ−

G(a) = 0.

A-Strengthening. An alive supporter strengthens the acceptability degree of an argument to be greater than its basic weight. (11) If w(a) < 1 and ∃b ∈Sup(a) s.t. σ+(b) > 0, then σ+(a) > w(a).

R-Strengthening. An alive attacker strengthens the rejectability degree of an argument to be greater than 0. (12) If ∃b ∈Att(a) s.t. σ+(b) > 0, then σ−(a) > 0.

Example 1. A wBAG where dashed arrows represent supports and solid arrows represent attacks. Arguments x, a, y are assigned with basic weights 0.6, 0.5, 0.8 respectively.

a: 0.5 x: 0.6 y: 0.8

Assume a semantics satisfies A-Stability and R-Stability. Then σ+(x) = 0.6, σ+(y) = 0.8, and σ−(x) = σ−(y) = 0. By A-Strengthening and R-Strengthening, we have σ+(a) > 0.5 and σ−(a) > 0.

A-Strengthening Soundness. Alive supporters are the only source of obtaining the acceptability degree. (13) If w(a) < 1 and σ+(a) > w(a), then ∃b ∈Sup(a) s.t. σ+(b) > 0. R-Strengthening Soundness. Alive attackers are the only source of obtaining the rejectability degree. (14) If σ−(a) > 0, then ∃b ∈Att(a) s.t. σ+(b) > 0.

The following two principles claim that each alive argument has an impact on the arguments it attacks or supports. A-Counting. Adding an alive supporter leads to an increase in the acceptability degree of the supported argument. (15) If (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) Sup(a) = Sup(b) \ {x} with x ∈Sup(b), (iv) σ+(x) > 0, then σ+(a) < σ+(b). R-Counting. Adding an alive attacker leads to an increase in the rejectability degree of the attacked argument. (16) If (i) σ−(a) < 1 or σ−(b) < 1, (ii) Att(a) = Att(b) \ {x} with x ∈Att(b), (iii) σ+(x) > 0, then σ−(a) < σ−(b).

Intuitively, the higher the acceptability degree, the stronger the impact of the argument. A-Reinforcement. Increasing a supporter’s acceptability degree leads to an increase in the acceptability degree of the supported argument. (17) If (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) Sup(a) \ {x} = Sup(b) \ {y} with x ∈Sup(a) and y ∈Sup(b), (iv) σ+(x) < σ+(y) and σ−(x) = σ−(y), then σ+(a) < σ+(b). R-Reinforcement. Increasing an attacker’s acceptability degree leads to an increase in the rejectability degree of the attacked argument. (18) If (i) σ−(a) < 1 or σ−(b) < 1, (ii) Att(a) \ {x} = Att(b)\{y} with x ∈Att(a) and y ∈Att(b), (iii) σ+(x) < σ+(y) and σ−(x) = σ−(y), then σ−(a) < σ−(b).

Naturally, the higher the rejectability degree, the weaker the impact of the argument. A-Weakened Defense. Increasing a supporter’s rejectability degree leads to a decrease in the acceptability degree of the supported argument. (19) If (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) Sup(a) \ {x} = Sup(b) \ {y} with x ∈Sup(a) and y ∈Sup(b), (iv) σ−(x) < σ−(y) and σ+(x) = σ+(y) > 0, then σ+(a) > σ+(b). R-Weakened Defense. Increasing an attacker’s rejectability degree leads to a decrease in the rejectability degree of the attacked argument. (20) If (i) σ−(a) < 1 or σ−(b) < 1, (ii) Att(a) \ {x} = Att(b)\{y} with x ∈Att(a) and y ∈Att(b), (iii) σ−(x) < σ−(y) and σ+(x) = σ+(y) > 0, then σ−(a) > σ−(b).

19417

<!-- Page 4 -->

The last three notable principles correspond to three strategies to deal with the precedence of the quality, quantity or compromise of supporters and attackers. Quality Precedence (QP) prioritizes the quality of supporters and attackers. It focuses on the strongest supporter and attacker, which have both the highest acceptability and lowest rejectability degree. In words: (i) the stronger the strongest supporter of an argument, the higher its acceptability, and (ii) the stronger the strongest attacker of an argument, the higher its rejectability. (21) For any G = ⟨A, w, S, R⟩, ∀a, b ∈A,

• if (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) ∃y ∈Sup(b) s.t. ∀x ∈Sup(a), σ+(x) < σ+(y) and σ−(x) > σ−(y), then σ+(a) < σ+(b); • if (i) σ−(a) < 1 or σ−(b) < 1, (ii) ∃y ∈Att(b) s.t. ∀x ∈Att(a), σ+(x) < σ+(y) and σ−(x) > σ−(y), then σ−(a) < σ−(b).

Cardinality Precedence (CP) prioritizes the quantity of supporters and attackers. In words: (i) the greater the number of alive supporters of an argument, the higher its acceptability, and (ii) the greater the number of alive attackers of an argument, the higher its rejectability. (22) For any G = ⟨A, w, S, R⟩, ∀a, b ∈A,

• if (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) |{x ∈Sup(a)| σ+(x) > 0}| < |{y ∈Sup(b)| σ+(y) > 0}|, then σ+(a) < σ+(b); • if (i) σ−(a) < 1 or σ−(b) < 1, (ii) |{x ∈ Att(a)| σ+(x) > 0}| < |{y ∈Att(b)| σ+(y) > 0}|, then σ−(a) < σ−(b).

Compensation is a kind of compromise that considers both the quality and quantity of attackers and supporters. It says that several weak supporters/attackers may compensate one strong supporter/attacker. (23) There exists a wBAG G = ⟨A, w, S, R⟩such that

• ∃a, b ∈A s.t. (i) w(a) = w(b), (ii) σ+(a) < 1 or σ+(b) < 1, (iii) ∃y ∈Sup(b) s.t. ∀x ∈Sup(a), σ+(x) < σ+(y) and σ−(x) > σ−(y), (iv) |{x ∈ Sup(a)| σ+(x) > 0}| > |{y ∈Sup(b)| σ+(y) > 0}|, (v) σ+(a) = σ+(b); • ∃a, b ∈A s.t. (i) σ−(a) < 1 or σ−(b) < 1, (ii) ∃y ∈Att(b) s.t. ∀x ∈Att(a), σ+(x) < σ+(y) and σ−(x) > σ−(y), (iii) |{x ∈Att(a)| σ+(x) > 0}| > |{y ∈Att(b)| σ+(y) > 0}|, (iv) σ−(a) = σ−(b).

Formal Analysis of Principles

In this section, we provide a formal analysis of principles. We first present some links between principles.

Proposition 1. The following properties hold:

1. A-Stability, R-Stability, R-Strengthening, QP and CP are incompatible. 2. Compensation is not compatible with QP or CP. 3. CP (resp. Compensation) is compatible with principles (1)-(20).

Proposition 2. Let S be a semantics which satisfies Independence, Directionality and Equivalence. Then:

## 1 If S satisfies A-Stability, A-Neutrality, then it also satisfies A-Strengthening

Soundness. 2. If S satisfies R-Stability, R-Neutrality, then it also satisfies R-Strengthening Soundness. 3. If S satisfies A-Stability, A-Neutrality, A-Reinforcement, then it also satisfies A-Counting and A-Strengthening. 4. If S satisfies A-Stability, R-Neutrality, R-Reinforcement, then it also satisfies R-Counting and R-Strengthening.

Next, we study the behavior of semantics under some specified principles. To begin, we show that a set of arguments that are not supported or attacked by any other arguments keeps their acceptability and rejectability degrees unchanged in any graph, whenever the semantics satisfies Independence and Directionality.

Proposition 3. If a semantics S satisfies Independence and Directionality, then for any G = ⟨A, w, S, R⟩and G′ = ⟨A′, w′, S′, R′⟩such that A ⊆A′, w(a) = w′(a) for all a ∈A, S′ ∩(A′ × A) = S and R′ ∩(A′ × A) = R, it follows that σ+

G(a) = σ+

G′(a) and σ−

G(a) = σ−

G′(a) for all a ∈A.

If an argument is only supported by worthless arguments, then its acceptability degree equals its basic weight, whenever the semantics satisfies Independence, Directionality, Equivalence, A-Stability and A-Neutrality.

Proposition 4. Let S be a semantics which satisfies Independence, Directionality, Equivalence, A-Stability and A- Neutrality. Then for any G = ⟨A, w, S, R⟩, ∀a ∈A, if for any x ∈Sup(a), σ+(x) = 0, then σ+(a) = w(a).

If an argument is only attacked by worthless arguments, then its rejectability degree is 0, whenever the semantics satisfies Independence, Directionality, Equivalence, R-Stability and R-Neutrality.

Proposition 5. Let S be a semantics which satisfies Independence, Directionality, Equivalence, R-Stability and R- Neutrality. Then for any G = ⟨A, w, S, R⟩, ∀a ∈A, if for any x ∈Att(a), σ+(x) = 0, then σ−(a) = 0.

If a semantics satisfies Independence, Directionality, Equivalence, Proportionality, A-Neutrality, A-Stability and A-Strengthening, then the lower bound of the acceptability degree is equal to the basic weight.

Proposition 6. Let S be a semantics which satisfies Independence, Directionality, Equivalence, Proportionality, A- Neutrality, A-Stability and A-Strengthening. Then for any G = ⟨A, w, S, R⟩, ∀a ∈A, σ+(a) ∈[w(a), 1].

Convergent Semantics and their Properties In this section, we propose three convergent semantics for wBAG, each corresponding to one of QP, CP and Compensation. We develop semantics based on the well-studied hcategorizer function family (Besnard and Hunter 2001; Pu et al. 2014; Amgoud, Doder, and Vesic 2022). The resulting functions produce iterative sequences that always converge for any wBAG including cyclic ones.

19418

<!-- Page 5 -->

Quality-Based Semantics The quality-based semantics (QBS) prioritizes the quality of supporters and attackers, i.e., satisfies Quality Precedence. Definition 5. Let G = ⟨A, w, S, R⟩. For any a ∈A, the iterative sequence {F i(a)}i∈N is defined by F i(a) = (f i(a), gi(a)) where f i, gi: A →[0, 1] are:

f 0(a) = w(a), g0(a) = 0;

For any i ≥0, f i+1(a) = w(a) + (1 −w(a))

max b∈Sup(a) hi(b)

1 + max b∈Sup(a) hi(b)

gi+1(a) = max b∈Att(a) hi(b)

1 + max b∈Att(a) hi(b) with hi(b) = f i(b) 1 + gi(b).

By convention, maxb∈Sup(a) hi(b) = 0 if Sup(a) = ∅and maxb∈Att(a) hi(b) = 0 if Att(a) = ∅. Theorem 1 (QBS Convergence). For any a ∈A, the sequence {F i(a)}i∈N converges as i approaches infinity.

The quality-based semantics is defined through the limit of the above iterative sequence. Definition 6 (QBS). The quality-based semantics is a function QBS transforming any G = ⟨A, w, S, R⟩into a function DegQBS

G defined from A to [0, 1] × [0, 1] s.t. ∀a ∈A, DegQBS

G (a) = (σ+(a), σ−(a)) where σ+(a) = lim i→∞f i(a), σ−(a) = lim i→∞gi(a).

Theorem 2 states that the acceptability and rejectability degrees assigned by QBS can be nicely described by the following equations. Theorem 2. Let G = ⟨A, w, S, R⟩. Then for any a ∈A under QBS, we have:

σ+(a) = w(a) + (1 −w(a))

max b∈Sup(a) h(b)

1 + max b∈Sup(a) h(b)

σ−(a) = max b∈Att(a) h(b)

1 + max b∈Att(a) h(b) with h(b) = σ+(b) 1 + σ−(b).

Theorem 3 states that QBS is the unique function that satisfies the above equations. Theorem 3. Let G = ⟨A, w, S, R⟩and D: A → [0, 1] × [0, 1] be a function. If for any a ∈A, D(a) = (D+(a), D−(a)) satisfies

D+(a) = w(a) + (1 −w(a))

max b∈Sup(a) h′(b)

1 + max b∈Sup(a) h′(b)

D−(a) = max b∈Att(a) h′(b)

1 + max b∈Att(a) h′(b) with h′(b) = D+(b) 1 + D−(b), then D = DegQBS

G.

Since QBS focuses on the strongest supporter and attacker, it violates A-Counting, R-Counting, A- Reinforcement, R-Reinforcement, A-Weakened Defense, and R-Weakened Defense. In fact, it satisfies the rest principles that are compatible with QP.

Theorem 4. QBS violates A-Counting, R-Counting, A- Reinforcement, R-Reinforcement, A-Weakened Defense, R- Weakened Defense, CP and Compensation. It satisfies all the remaining principles.

Cardinality-Based Semantics

The cardinality-based semantics (CBS) prioritizes the quantity of supporters and attackers, i.e., satisfies Cardinality Precedence. The iterative function below considers only the founded supporters/attackers whose previous values of the function f are greater than 0.

Definition 7. Let G = ⟨A, w, S, R⟩. For any a ∈A, the iterative sequence {F i(a)}i∈N is defined by F i(a) = (f i(a), gi(a)) where f i, gi: A →[0, 1] are:

f 0(a) = w(a), g0(a) = 0;

For any i ≥0, f i+1(a) = w(a) + (1 −w(a))

| FSi(a)| +

P b∈FSi(a)

hi(b)

| FSi(a)|

1 + | FSi(a)| +

P b∈FSi(a)

hi(b)

| FSi(a)| gi+1(a) =

| FAi(a)| +

P b∈FAi(a)

hi(b)

| FAi(a)|

1 + | FAi(a)| +

P b∈FAi(a)

hi(b)

| FAi(a)|

, in which hi(b) = f i(b) 1+gi(b), FSi(a) = {b ∈Sup(a)|f i(b) >

0} and FAi(a) = {b ∈Att(a)|f i(b) > 0}. We stipulate that P b∈FSi(a) hi(b)

| FSi(a)| = 0 if FSi(a) = ∅and

P b∈FAi(a) hi(b)

| FAi(a)| = 0 if FAi(a) = ∅.

Intuitively, FSi(a) (resp. FAi(a)) denotes the set of founded supporters (resp. attackers) in the i-th iteration.

Theorem 5 (CBS Convergence). For any a ∈A, the sequence {F i(a)}i∈N converges as i approaches infinity.

The cardinality-based semantics is defined through the limit of the above iterative sequence.

Definition 8 (CBS). The cardinality-based semantics is a function CBS transforming any wBAG G = ⟨A, w, S, R⟩ into a function DegCBS

G defined from A to [0, 1] × [0, 1] s.t. ∀a ∈A, DegCBS

G (a) = (σ+(a), σ−(a)) where σ+(a) = lim i→∞f i(a), σ−(a) = lim i→∞gi(a).

Theorem 6 states that the acceptability and rejectability degrees assigned by CBS can be nicely described by the following equations.

19419

<!-- Page 6 -->

Theorem 6. Let G = ⟨A, w, S, R⟩. Then for any a ∈A under CBS, we have:

σ+(a) = w(a) + (1 −w(a))

| FS(a)| +

P b∈FS(a)

h(b)

| FS(a)|

1 + | FS(a)| +

P b∈FS(a)

h(b)

| FS(a)| σ−(a) =

| FA(a)| +

P b∈FA(a)

h(b)

| FA(a)|

1 + | FA(a)| +

P b∈FA(a)

h(b)

| FA(a)| with h(b) = σ+(b) 1 + σ−(b),

FS(a) = {b ∈Sup(a)| σ+(b) > 0} and FA(a) = {b ∈ Att(a)| σ+(b) > 0}.

Similar to Theorem 3, Theorem 7 states that CBS is the unique function satisfying the above equations.

Theorem 7. Let G = ⟨A, w, S, R⟩and D: A → [0, 1] × [0, 1] be a function. If for any a ∈ A, D(a) = (D+(a), D−(a)) satisfies the corresponding equations presented in Theorem 6. Then D = DegCBS

G.

CBS satisfies all the principles that are compatible with CP, stated as below.

Theorem 8. CBS satisfies all the principles except QP and Compensation.

Hybrid-Based Semantics The hybrid-based semantics (HBS) satisfies Compensation, taking both the quality and quantity into account.

Definition 9. Let G = ⟨A, w, S, R⟩. For any a ∈A, the iterative sequence {F i(a)}i∈N is defined by F i(a) = (f i(a), gi(a)) where f i, gi: A →[0, 1] are as follows:

f 0(a) = w(a), g0(a) = 0;

For any i ≥0, f i+1(a) = w(a) + (1 −w(a))

| FSi(a)| + P b∈FSi(a)

hi(b)

1 + | FSi(a)| + P b∈FSi(a)

hi(b)

gi+1(a) =

| FAi(a)| + P b∈FAi(a)

hi(b)

1 + | FAi(a)| + P b∈FAi(a)

hi(b), in which hi(b) = f i(b) 1+gi(b), FSi(a) = {b ∈Sup(a)|f i(b) >

0} and FAi(a) = {b ∈Att(a)|f i(b) > 0}. We stipulate that P b∈FSi(a) hi(b) = 0 if FSi(a) = ∅and P b∈FAi(a) hi(b) = 0 if FAi(a) = ∅.

Theorem 9 (HBS Convergence). For any a ∈A, the sequence {F i(a)}i∈N converges as i approaches infinity.

The hybrid-based semantics is defined through the limit of the above iterative sequence.

Definition 10 (HBS). The hybrid-based semantics is a function HBS transforming any wBAG G = ⟨A, w, S, R⟩into a function DegHBS

G defined from A to [0, 1]×[0, 1] s.t. ∀a ∈A, DegHBS

G (a) = (σ+(a), σ−(a)) where σ+(a) = lim i→∞f i(a), σ−(a) = lim i→∞gi(a).

Theorem 10 states that the acceptability and rejectability degrees assigned by HBS can be nicely described by the following equations. Theorem 10. Let G = ⟨A, w, S, R⟩. Then for any a ∈A under HBS, we have:

σ+(a) = w(a) + (1 −w(a))

| FS(a)| + P b∈FS(a)

h(b)

1 + | FS(a)| + P b∈FS(a)

h(b)

σ−(a) =

| FA(a)| + P b∈FA(a)

h(b)

1 + | FA(a)| + P b∈FA(a)

h(b) with h(b) = σ+(b) 1 + σ−(b),

FS(a) = {b ∈Sup(a)| σ+(b) > 0} and FA(a) = {b ∈ Att(a)| σ+(b) > 0}.

Similar to Theorem 3 and Theorem 7, Theorem 11 states that HBS is the unique function that satisfies the above equations. Theorem 11. Let G = ⟨A, w, S, R⟩and D: A → [0, 1] × [0, 1] be a function. If for any a ∈ A, D(a) = (D+(a), D−(a)) satisfies the corresponding equations presented in Theorem 10, then D = DegHBS

G. HBS satisfies all the principles that are compatible with Compensation, stated as below. Theorem 12. HBS satisfies all the principles except QP and CP.

Comparisons for principles under QBS, CBS and HBS are summarized in Table 2.

QBS CBS HBS Principles (1)-(14) • • • A-Counting – • • R-Counting – • • A-Reinforcement – • • R-Reinforcement – • • A-Weakened Defense – • • R-Weakened Defense – • • Quality Precedence • – – Cardinality Precedence – • – Compensation – – •

**Table 2.** Principles under QBS, CBS and HBS

Example 2. Consider the wBAG G depicted below.

a: 0.5 x: 0.8 y: 1.0 p: 0.8 q: 1.0

19420

<!-- Page 7 -->

The strength of the argument a converges approximately as follows: DegQBS

G (a) ≈(0.750, 0.424), DegCBS

G (a) ≈ (0.874, 0.720), and DegHBS

G (a) ≈(0.899, 0.757).

Preliminary Experimental Analysis We implemented our three novel semantics in Python and conducted preliminary experiments on the wBAG benchmark from (Potyka 2018). The benchmark1 consists of 30 randomly generated (RG) datasets, each containing 100 graphs. The number of dataset arguments (i.e., graph size) ranges from 100 to 3000, increasing by 100.

The experiments were run on a Windows 11 x64 laptop with an Intel i7-11800H CPU (8 cores, 4.6 GHz) and 32 GB of memory. Our evaluation criteria include the total running time of a dataset and its minimal/maximal iterations. The algorithm stops when the difference of values between successive iterations < 0.0001 for each argument. All empirical results are summarized in Figure 1.

Generally speaking, the total running time appears to grow linearly in graph size and all semantics perform quite efficiently. The average time for computing a graph of 3000 arguments under QBS/HBS/CBS ≈0.11s/0.10s/0.09s. Concerning the number of min/max iterations in the experiment, we observe that QBS usually takes more iterations to converge than HBS and CBS. Even so, QBS only uses 13 steps to converge in the worst case. Interestingly, the number of min/max iterations under HBS, CBS and QBS seems to be constant in graph size. A similar phenomenon is also mentioned in (Amgoud, Doder, and Vesic 2022). In addition, the min/max iterations of HBS and CBS appear to largely overlap. To sum up, the preliminary experiments suggest that our semantics perform rather efficiently and have potential for real-world applications.

**Figure 1.** Total Runtime and Min/Max Iterations on RG

1https://www.researchgate.net/publication/326557254

## Discussion

and Conclusion The study of gradual semantics in wBAG has received extensive attention in the literature. Particularly, developing convergent semantics for cyclic wBAG is challenging. Most existing semantics are restricted to acyclic graphs, e.g., ES- AAF (Evripidou and Toni 2014), QuAD (Baroni et al. 2015), DF-QuAD (Rago et al. 2016), Euler (Amgoud and Ben- Naim 2018b), MLP (Potyka 2021), and NPE (Doder, Vesic, and Croitoru 2021). The only exception is the Max Eulerbased semantics (Mossakowski and Neuhaus 2018), which simply focuses on the strongest supporter and attacker while ignoring other arguments. This violates the so-called openmindedness (Potyka 2019a), i.e., the strength of arguments cannot be far from their basic weights. In contrast, under our CBS and HBS, adding sufficient supporters (resp. attackers) leads to σ+ →1 (resp. σ−→1), which illustrates a form of open-mindedness.

The investigation of convergence behavior is of significant interest. Some special cyclic cases have been proven to converge under various semantics, typically by imposing constraints on the indegrees or basic weights of arguments (Mossakowski and Neuhaus 2018; Potyka 2021, 2019a; Potyka and Booth 2024a). Moreover, continuization has emerged as a technique to improve the convergence behavior of semantics (Potyka 2018, 2019a; Potyka and Booth 2024b). This approach associates update functions with a system of differential functions, and empirical studies have shown that continuized semantics are effective in resolving many divergence cases. However, their theoretical convergence behavior remains largely unknown.

The existing methodologies to aggregate the strength of supporters and attackers make it inherently difficult to obtain convergent semantics, as their aggregation operators do not always behave well during iterations. Particularly, in computing cyclic graphs with intricate interactions, argument values may vary drastically, resulting in divergent behavior (Amgoud and Ben-Naim 2018b; Potyka 2019a; Mossakowski and Neuhaus 2018; Potyka and Booth 2024a).

The paper elegantly addresses the challenge by adopting the bilateral gradual semantics, which offers a novel perspective to separately evaluate supporters and attackers through the acceptability and rejectability degrees. We first presented a set of principles for well-behaved wBAG semantics, and studied their relationships and properties. Then we proposed three convergent semantics that conform to the above principles. These semantics are defined through the limits of the iterative functions that always converge for any wBAG including cyclic ones, and perform efficiently on the benchmark from the literature.

Future work can be considered in several directions. We can investigate the computational complexity of convergent functions and conduct more experiments to check scalability. Additional desirable wBAG principles, such as monotonicity (Baroni, Rago, and Toni 2019), duality (Potyka 2020) can be discussed. It would also be interesting to aggregate σ+ and σ−to an overall strength for specific applications. Finally, applying wBAG to practical scenarios involving cycles of supports and attacks—such as social media debates and explainable AI—is a desirable endeavour.

19421

<!-- Page 8 -->

## Acknowledgements

This work was supported by the National Social Science Found of China (25BZX071).

## References

Amgoud, L.; and Ben-Naim, J. 2016. Evaluation of arguments from support relations: Axioms and semantics. In Proceedings of the 25th International Joint Conference on Artificial Intelligence, IJCAI, 900–906. Amgoud, L.; and Ben-Naim, J. 2018a. Evaluation of arguments in weighted bipolar graphs. International Journal of Approximate Reasoning, 99: 39–55. Amgoud, L.; and Ben-Naim, J. 2018b. Weighted Bipolar Argumentation Graphs: Axioms and Semantics. In Proceedings of the 27th International Joint Conference on Artificial Intelligence, IJCAI, 5194–5198. Amgoud, L.; Ben-Naim, J.; Doder, D.; and Vesic, S. 2017. Acceptability Semantics for Weighted Argumentation Frameworks. In Proceedings of the 26th International Joint Conference on Artificial Intelligence, IJCAI, 56–62. Amgoud, L.; Cayrol, C.; Lagasquie-Schiex, M.; and Livet, P. 2008. On bipolarity in argumentation frameworks. International Journal of Intelligent Systems, 23(10): 1062–1093. Amgoud, L.; Doder, D.; and Vesic, S. 2022. Evaluation of argument strength in attack graphs: Foundations and semantics. Artificial Intelligence, 302: 103607. Amgoud, L.; and Prade, H. 2009. Using arguments for making and explaining decisions. Artificial Intelligence, 173(3- 4): 413–436. Atkinson, K.; Baroni, P.; Giacomin, M.; Hunter, A.; Prakken, H.; Reed, C.; Simari, G.; Thimm, M.; and Villata, S. 2017. Towards artificial argumentation. AI Magazine, 38(3): 25–36. Baroni, P.; Rago, A.; and Toni, F. 2018. How many properties do we need for gradual argumentation? In Proceedings of the 32nd AAAI Conference on Artificial Intelligence, AAAI, 126–139. Baroni, P.; Rago, A.; and Toni, F. 2019. From fine-grained properties to broad principles for gradual argumentation: a principled spectrum. International Journal of Approximate Reasoning, 105: 252–286. Baroni, P.; Romano, M.; Toni, F.; Aurisicchio, M.; and Bertanza, G. 2015. Automatic evaluation of design alternatives with quantitative argumentation. Argument & Computation, 6(1): 24–49. Besnard, P.; and Hunter, A. 2001. A logic-based theory of deductive arguments. Artificial Intelligence, 128(1/2): 203– 235. Bonzon, E.; Delobelle, J.; Konieczny, S.; and Maudet, N. 2016. A comparative study of ranking-based semantics for abstract argumentation. In Proceedings of the 30th AAAI Conference on Artificial Intelligence, AAAI, 914–920. Cacioppo, J.; Gardner, W.; and Berntson, G. 1997. Beyond bipolar conceptualizations and measures: The case of attitudes and evaluative space. Personality and Social Psychology Review, 1(1): 3–25.

Cayrol, C.; and Lagasquie-Schiex, M. 2005. On the acceptability of arguments in bipolar argumentation frameworks. In Proceedings of the 8th European Conference on Symbolic and Quantitative Approaches to Reasoning with Uncertainty, ECSQARU, 378–389. da Costa Pereira, C.; Tettamanzi, A.; and Villata, S. 2011. Changing one’s mind: Erase or rewind? Possibilistic belief revision with fuzzy argumentation based on trust. In Proceedings of the 22nd International Joint Conference on Artificial Intelligence, IJCAI, 164–171. Doder, D.; Vesic, S.; and Croitoru, M. 2021. Ranking semantics for argumentation systems with necessities. In Proceedings of the 29th International Joint Conference on Artificial Intelligence, IJCAI, 1912–1918. Dung, P. 1995. On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games. Artificial Intelligence, 77(2): 321–357. Evripidou, V.; and Toni, F. 2014. Quaestio-it.com: a social intelligent debating platform. Journal of Decision Systems, 23(3): 333–349. Gabbay, D.; and Rodrigues, O. 2015. Equilibrium states in numerical argumentation networks. Logica Universalis, 9(4): 411–473. Hunter, A. 2013. A probabilistic approach to modelling uncertain logical arguments. International Journal of Approximate Reasoning, 54(1): 47–81. Leite, J.; and Martins, J. 2011. Social abstract argumentation. In Proceedings of the 22nd International Joint Conference on Artificial Intelligence, IJCAI, 2287–2292. Mossakowski, T.; and Neuhaus, F. 2018. Modular semantics and characteristics for bipolar weighted argumentation graphs. arXiv preprint arXiv:1807.06685. Polberg, S.; and Hunter, A. 2018. Empirical evaluation of abstract argumentation: Supporting the need for bipolar and probabilistic approaches. International Journal of Approximate Reasoning, 93: 487–543. Potyka, N. 2018. Continuous dynamical systems for weighted bipolar argumentation. In Proceedings of the 16th International Conference on Principles of Knowledge Representation and Reasoning, KR, 148–157. Potyka, N. 2019a. Extending Modular Semantics for Bipolar Weighted Argumentation. In Proceedings of the 18th International Conference on Autonomous Agents and Multiagent Systems, AAMAS, 1722–1730. Potyka, N. 2019b. Open-mindedness of gradual argumentation semantics. In Proceedings of the 13th International Conference on Scalable Uncertainty Management, SUM, 236–249. Potyka, N. 2020. Bipolar abstract argumentation with dual attacks and supports. In Proceedings of the 17th International Conference on Principles of Knowledge Representation and Reasoning, KR, 677–686. Potyka, N. 2021. Interpreting neural networks as quantitative argumentation frameworks. In Proceedings of the 35th AAAI Conference on Artificial Intelligence, AAAI, 6463– 6470.

19422

<!-- Page 9 -->

Potyka, N.; and Booth, R. 2024a. Balancing openmindedness and conservativeness in quantitative bipolar argumentation (and how to prove semantical from functional properties). In Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning, KR, 597–607. Potyka, N.; and Booth, R. 2024b. An empirical study of quantitative bipolar argumentation frameworks for truth discovery. In Proceedings of the 10th International Conference on Computational Models of Argument, COMMA, 205–216. IOS Press. Prakken, H. 2024. An abstract and structured account of dialectical argument strength. Artificial Intelligence, 335: 104193. Pu, F.; Luo, J.; Zhang, Y.; and Luo, G. 2014. Argument ranking with categoriser function. In Proceedings of the Knowledge Science, Engineering and Management: 7th International Conference, KSEM, 290–301. Rago, A.; Cocarascu, O.; Oksanen, J.; and Toni, F. 2025. Argumentative review aggregation and dialogical explanations. Artificial Intelligence, 340: 104291. Rago, A.; and Toni, F. 2017. Quantitative argumentation debates with votes for opinion polling. In Proceedings of the 20th International Conference on Principles and Practice of Multi-Agent Systems, PRIMA, 369–385. Rago, A.; Toni, F.; Aurisicchio, M.; and Baroni, P. 2016. Discontinuity-Free Decision Support with Quantitative Argumentation Debates. In Proceedings of the 15th International Conference on Principles of Knowledge Representation and Reasoning, KR, 63–73. Rago, A.; Vasileiou, S.; Toni, F.; Son, T.; and Yeoh, W. 2024. A Methodology for Gradual Semantics for Structured Argumentation under Incomplete Information. arXiv preprint arXiv:2410.22209. Wang, Z.; and Shen, Y. 2024. Bilateral Gradual Semantics for Weighted Argumentation. In Proceedings of the 38th AAAI Conference on Artificial Intelligence, AAAI, 10732– 10739. Yin, X.; Potyka, N.; and Toni, F. 2024. CE-QArg: Counterfactual Explanations for Quantitative Bipolar Argumentation Frameworks. In Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning, KR, 697–707.

19423
