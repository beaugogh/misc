---
title: "Model Counting for Dependency Quantified Boolean Formulas"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38437
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38437/42399
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Model Counting for Dependency Quantified Boolean Formulas

<!-- Page 1 -->

## Model

Counting for Dependency Quantified Boolean Formulas

Long-Hin Fung1, Che Cheng2, Jie-Hong Roland Jiang2, Friedrich Slivovsky3, Tony Tan3

1Department of Computer Science and Information Engineering, National Taiwan University 2Graduate Institute of Electronics Engineering, National Taiwan University 3School of Computer Science and Informatics, University of Liverpool r12922017@csie.ntu.edu.tw, {f11943097,jhjiang}@ntu.edu.tw, {F.Slivovsky,tonytan}@liverpool.ac.uk

## Abstract

Dependency Quantified Boolean Formulas (DQBF) generalize QBF by explicitly specifying which universal variables each existential variable depends on, instead of relying on a linear quantifier order. The satisfiability problem of DQBF is NEXP-complete, and many hard problems can be succinctly encoded as DQBF. Recent work has revealed a strong analogy between DQBF and SAT: k-DQBF (with k existential variables) is a succinct form of k-SAT, and satisfiability is NEXP-complete for 3-DQBF but PSPACE-complete for 2- DQBF, mirroring the complexity gap between 3-SAT (NPcomplete) and 2-SAT (NL-complete). Motivated by this analogy, we study the model counting problem for DQBF, denoted #DQBF. Our main theoretical result is that #2-DQBF is #EXP-complete, where #EXP is the exponential-time analogue of #P. This parallels Valiant’s classical theorem stating that #2-SAT is #P-complete. As a direct application, we show that first-order model counting (FOMC) remains #EXP-complete even when restricted to a PSPACE-decidable fragment of first-order logic and domain size two. Building on recent successes in reducing 2-DQBF satisfiability to symbolic model checking, we develop a dedicated 2-DQBF model counter. Using a diverse set of crafted instances, we experimentally evaluated it against a baseline that expands 2-DQBF formulas into propositional formulas and applies propositional model counting. While the baseline worked well when each existential variable depends on few variables, our implementation scaled significantly better to larger dependency sets.

Code and benchmarks — https://github.com/Sat-DQBF/sharp2DQR Extended version — https://arxiv.org/abs/2511.07337

## Introduction

There has been tremendous progress in SAT solving over the past few decades, enabling widespread applications across many areas of computing, including reasoning tasks in AI (Biere et al. 2009, 2023; Fichte et al. 2023). However, certain problems in hardware verification and synthesis are unlikely to admit succinct encodings in propo-

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

sitional logic, prompting research into automated reasoning in more expressive logics (Jiang 2009; Balabanov and Jiang 2015; Scholl and Becker 2001; Gitina et al. 2013a; Bloem, K¨onighofer, and Seidl 2014; Chatterjee et al. 2013; Kuehlmann et al. 2002; Ge-Ernst et al. 2022).

A natural candidate for such applications is the logic of Dependency Quantified Boolean Formulas (DQBF), an extension of Quantified Boolean Formulas (QBF) with Henkin quantifiers that annotate each existential variable with a set of universal variables it depends on (Balabanov, Chiang, and Jiang 2014). A model of a DQBF consists of Skolem functions that map each existential variable to a truth value based on an assignment to its universal dependencies. The finegrained control over variable dependencies allows DQBF to naturally express problems such as constrained program synthesis (Golia, Roy, and Meel 2021) and equivalence checking of partially specified circuits (Gitina et al. 2013b). This has led to active research over the past decade and the development of several solvers (Fr¨ohlich et al. 2014; Tentrup and Rabe 2019; Gitina et al. 2015; Wimmer et al. 2017; S´ıc and Strejcek 2021; Reichl, Slivovsky, and Szeider 2021; Reichl and Slivovsky 2022; Golia, Roy, and Meel 2023), as well as the inclusion of a dedicated DQBF track in recent QBF evaluations (Pulina and Seidl 2019).

While satisfiability is the central question in DQBF, many synthesis and verification tasks benefit from knowing how many solutions exist. Counting models can help debug and refine specifications: for instance, an unexpectedly large number of Skolem functions may suggest that the specification admits unintended behaviour. Model counters have been developed for QBF with one quantifier alternation (Plank, M¨ohle, and Seidl 2024) as well as Boolean synthesis (Shaw, Juba, and Meel 2024), and more recently, for general QBF (Capelli et al. 2024).

In this paper, we consider the model counting problem for DQBF, denoted #DQBF. This is a formidable problem, since even deciding whether a DQBF has a model is NEXP-complete (Peterson and Reif 1979; Chen et al. 2022; Cheng et al. 2025). Moreover, because DQBF allows arbitrary and potentially incomparable dependency sets, existing techniques for #QBF that rely on a linear order of quantifiers cannot be applied.

To support the intuition that #DQBF is a particularly difficult problem, we first prove that even the model count-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

14234

<!-- Page 2 -->

ing problem for DQBF with just two existential variables, denoted #2-DQBF, is #EXP-complete. This is despite the fact that satisfiability of 2-DQBF is “only” PSPACEcomplete (Fung and Tan 2023). Our proof builds on a recent result on 2-DNF model counting (Bannach et al. 2025) and uses the close correspondence between k-DQBF and k-SAT (Fung and Tan 2023). This hardness result is analogous to the well-known hardness of #2-SAT: while 2-SAT is solvable in polynomial time, counting its models is #Pcomplete (Valiant 1979a,b).

Note that functions in #EXP may output doubly exponential numbers, which require exponentially many bits. Thus, the standard polynomial time Turing reductions for establishing #P-hardness, as in the case of #2-SAT in (Valiant 1979a,b), are not appropriate for the class #EXP. To circumvent this issue, we introduce a new kind of polynomialtime reduction, called a poly-monious reduction (see Section 2 for the definition), which lies between classical parsimonious reductions and polynomial-time Turing reductions. Under poly-monious reductions, #2-SAT is still #Pcomplete (Bannach et al. 2025).

Another notion of hardness for the counting problem requires the reduction to be parsimonious (Ladner 1989). However, since 2-SAT is NL-complete, #2-SAT is not #Phard under parsimonious reduction, unless NL = NP. We believe that the notion of poly-monious reduction is wellsuited for establishing #EXP-hardness, as it strikes a balance between parsimonious reductions and polynomial-time Turing reductions in terms of strength.

As an application of the hardness of #2-DQBF, we show that the combined complexity of first-order model counting (FOMC)—a central problem in statistical relational AI—is #EXP-complete (over varying vocabulary). FOMC is defined as given FO sentence Ψ and a number N in unary, compute the number of models of Ψ with domain {1,..., N}. The combined complexity of FOMC is the complexity measured in terms of both the sentence Ψ and the number N. While the #EXP-hardness of FOMC can already be inferred from classical results in logic (Lewis 1980),1 we obtain a stronger result: FOMC is #EXP-hard even when the domain size is restricted to 2 and the base logic is a PSPACE-decidable fragment of FO.2 This may help explain why scalable FO model counters have remained elusive despite intensive research efforts for over a decade.

Motivated by our result that #DQBF remains hard even for just two existential variables, we explore the viability of solving #2-DQBF in practice. Due to the doubleexponential number of possible Skolem functions, direct enumeration is infeasible. Similarly, expanding a DQBF into a propositional formula leads to an exponential blow-up, rendering state-of-the-art #SAT solvers impractical.

Instead, we build on a recent success in reducing 2-DQBF

1A close inspection of the proof in (Lewis 1980) shows polymonious reductions from languages in NEXP to the Bernays- Sch¨onfinkel-Ramsey fragment of FO, whose satisfiability problem is known to be NEXP-complete.

2In general, the satisfiability problem for FO is undecidable (Trakhtenbrot 1950).

satisfiability to model checking (Fung et al. 2024) and interpret 2-DQBF instances as succinctly represented implication graphs. Based on this idea, we propose a model counting algorithm that proceeds in two main phases. In the first phase, it constructs a Binary Decision Diagram (BDD) representing reachability in the implication graph. This phase benefits from mature tools developed by the formal methods community, including the IC3 algorithm, the CUDD package for BDD manipulation, and ABC’s implementation of exact reachability (Bradley and Manna 2007; Bradley 2011; E´en, Mishchenko, and Brayton 2011; Somenzi 2009; Brayton and Mishchenko 2010). In the second phase, our algorithm counts Skolem functions by analysing each weakly connected component separately—similar in spirit to component-based decomposition in propositional model counters (Gomes, Sabharwal, and Selman 2021). Within each component, it suffices to enumerate Skolem functions for just one existential variable. We further restrict attention to partial Skolem functions defined only on the variables local to each component. This avoids explicit enumeration and enables us to handle instances with up to 2264 Skolem functions. The techniques used in this phase combine new ideas with existing methods (Reichl, Slivovsky, and Szeider 2021; Fung et al. 2024).

We evaluate our implementation on a diverse set of crafted benchmarks. As a baseline, we use a pipeline that expands a DQBF to a propositional formula and applies the #SAT solver Ganak (Sharma et al. 2019). While Ganak performs well on some smaller instances, its reliance on explicit expansion becomes a bottleneck as dependency sets grow. In contrast, our solver scales gracefully and consistently outperforms the baseline on DQBF with larger dependency sets.

We also performed experiments with state-of-the-art FO model counters. While our approach can only be applied to FOMC with binary relations, this is enough to encode problems such as counting the number of independent sets in highly symmetric graphs. In some cases, our implementation was able to handle instances with more than 2127 solutions, far beyond the practical reach of current FO model counters. This indicates that an analogue of our component decomposition technique for #2-DQBF may improve FO model counters in restricted, highly symmetric settings.

Related work. FOMC is often studied in the data complexity setting, i.e., the FO sentence is fixed and the complexity is measured only in terms of the domain size. It is shown in (Beame et al. 2015) that there is an FO3 sentence such that the data complexity of its FOMC is #P1-complete. For the two-variable fragment, the data complexity drops to PTIME (T´oth and Kuzelka 2024; van Bremen and Kuzelka 2023; Beame et al. 2015). The combined complexity is #Pcomplete, but assuming that the vocabulary is fixed (Beame et al. 2015). A tightly related problem to FOMC is query evaluation on probabilistic databases, whose combined complexity is #P-complete (Dalvi and Suciu 2004), but again, under the assumption of fixed vocabulary.

The notion of combined and data complexity was introduced in (Vardi 1982) in the context of database query evaluation, to better understand which component (the query/the

14235

<!-- Page 3 -->

data/both) contributes more to the complexity of query evaluation. Since then, as hinted in the previous paragraph, it has become the standard notion for establishing fine-grained complexity results for problems involving a few parameters.

## 2 Preliminaries

Notation. Let B = {⊥, ⊤}, where ⊥and ⊤denote the Boolean false and true values. A literal is either a Boolean variable or its negation. We write x⊤to denote the literal x and x⊥to denote ¬x. The sign of the literal xb is the bit b.

We use the symbols a, b, c to denote elements in B, and the bar version ¯a,¯b, ¯c to denote strings in B∗with |¯a| denoting the length of ¯a. Boolean variables are denoted by x, y, z, u, v and the bar version ¯x, ¯y, ¯z, ¯u, ¯v denote vectors of Boolean variables with |¯x| denoting the length of ¯x. We insist that in a vector ¯x there is no variable occurring more than once. Abusing the notation, we write ¯z ⊆¯x to denote that every variable in ¯z also occurs in ¯x.

As usual, φ(¯x) denotes a Boolean formula with variables ¯x. When it is clear from the context, we simply write φ. For ¯z ⊆¯x and ¯a ∈B∗where |¯a| = |¯z|, φ[¯z/¯a] denotes the formula obtained from φ by assigning the values in ¯a to ¯z. Obviously, if ¯z = ¯x, then φ[¯z/¯a] is either ⊥or ⊤.

Poly-monious reductions. Let Σ be a finite alphabet. A poly-monious reduction from a function F: Σ∗→N to another function G: Σ∗→N is a polynomial-time deterministic Turing machine M together with a polynomial p(s1,..., st) such that on input word w, M outputs t strings v1,..., vt where F(w) = p(G(v1),..., G(vt)).

Note that poly-monious reductions are a slight generalization of the classical parsimonious and c-monious reductions, but weaker than polynomial time Turing reductions. Parsimonious reduction is a poly-monious reduction with the identity polynomial p(s) = s. The c-monious reduction (Bannach et al. 2025) is a poly-monious reduction with the polynomial p(s) = cs. When restricted to functions in #P, a poly-monious reduction with polynomial p(s1,..., st) is a special case of polynomial time Turing reduction in the sense that the number of calls to the oracle is fixed to t, which does not depend on the input word.

#EXP-complete functions. A function F: Σ∗→N is in #EXP, if there is a non-deterministic exponential time Turing machine M such that for every word w ∈Σ∗, F(w) is the number of accepting runs of M on w. It is #EXP-hard, if for every function G ∈#EXP, there is a poly-monious reduction from G to F. Finally, it is #EXP-complete, if it is in #EXP and #EXP-hard.

Dependency Quantified Boolean Formulas (DQBF). A dependency quantified Boolean formula (DQBF) in prenex normal form is a formula of the form:

Ψ:= ∀¯x ∃y1(¯z1) · · · ∃yk(¯zk) ψ (1)

where ¯x = (x1,..., xn), each ¯zi ⊆¯x and ψ, called the matrix, is a quantifier-free Boolean formula using variables in ¯x ∪{y1,..., yk}. We call ¯x the universal variables, y1,..., yk the existential variables, and each ¯zi the dependency set of yi. A k-DQBF is a DQBF with k existential variables. For convenience, we sometimes write ∃yi(¯zi) as ∃yi(Ii) where Ii is the set of indices of the variables in ¯zi.

A DQBF Ψ as in (1) is satisfiable if there is a tuple (f1,..., fk), called Skolem functions, such that, for every 1 ≤i ≤k, fi is a formula using only variables in ¯zi, and by replacing each yi with fi, the matrix ψ becomes a tautology. We call the tuple (f1,..., fk) a solution or model of Ψ and write (f1,..., fk) |= Ψ. We refer to Ψ as a uniform DQBF if for every model (f1,..., fk) |= Ψ, f1,..., fk represent the same Boolean function, i.e., |¯z1| = · · · = |¯zk| = m and for every ¯a ∈Bm, f1(¯a) = · · · = fk(¯a). We write #Ψ to denote the number of Skolem functions of Ψ.

The model counting problem for DQBF, denoted #DQBF, is to compute #Ψ for a given DQBF Ψ. Its restriction to k-DQBF is denoted by #k-DQBF.

DQBF expansion. We first recall the definition of the expansion of a DQBF from (Fung and Tan 2023), which shows that a DQBF represents an exponentially large CNF formula. We will need an additional notation. For ¯z ⊆¯x and ¯a ∈Σ|¯x|, we write ¯a

¯x↓¯z to denote the projection of ¯a to the components in ¯z according to the order of the variables in ¯x. For example, if ¯x = (x1,..., x5) and ¯z = (x1, x2, x5), then ⊥⊥⊤⊥⊤

¯x↓¯z is ⊥⊥⊤, i.e., the projection of ⊥⊥⊤⊥⊤to its 1st, 2nd and 5th bits.

Let Ψ be as in Eq. (1). For each 1 ≤i ≤k and for each ¯c ∈B|¯zi|, let Xi,¯c be a variable. For each (¯a,¯b) ∈Bn × Bk, where ¯a = (a1,..., an) and ¯b = (b1,..., bk), define the clause C¯a,¯b:= X¬b1

1,¯c1 ∨· · · ∨X¬bk k,¯ck, where ¯ci = ¯a

¯x↓¯zi, for each 1 ≤i ≤k. The expansion of Ψ, denoted by exp(Ψ), is the following k-CNF formula.

exp(Ψ):=

^

(¯a,¯b) s.t. ψ[(¯x,¯y)/(¯a,¯b)]=⊥

C¯a,¯b (2)

It is known that Ψ is satisfiable if and only if its expansion exp(Ψ) is satisfiable (cf. Fung and Tan 2023). More precisely, a solution (f1,..., fk) |= Φ corresponds uniquely to a satisfying assignment of exp(Φ), where Xi,¯c = fi(¯c) for every 1 ≤i ≤k and ¯c ∈B|¯zi|.

Complexity of #DQBF In this section, we will analyse the complexity of #DQBF, starting with #3-DQBF. It is straightforward that #3-DQBF is in #EXP. It is #EXP-hard since every language in NEXP can be reduced parsimoniously in polynomial time to 3- DQBF (Fung and Tan 2023). This gives us the following theorem. Theorem 1. #3-DQBF is #EXP-complete.

Theorem 1 is not surprising, given that the satisfiability problem for 3-DQBF is already NEXP-complete. We will strengthen it by showing that #EXP-hardness already holds for 2-DQBF, whose satisfiability problem is PSPACEcomplete.

Before we can prove this, we need to introduce some further terminology. First, we recall the notion of succinct representation of graphs introduced in (Galperin and Wigderson 1983). In such a representation, instead of being given

14236

<!-- Page 4 -->

the list of edges in a graph, we are given a Boolean circuit C(¯x, ¯y), where ¯x, ¯y are vectors of Boolean variables of length n. The circuit C represents a graph GC where the set of vertices is Bn and there is an edge oriented from ¯a to ¯b, denoted ¯a →¯b, iff C(¯a,¯b) = ⊤.

We will interpret a 2-CNF formula F as a directed graph, called the implication graph of F, where each clause (ℓ1 ∨ ℓ2) represents two edges (¬ℓ1 →ℓ2) and (¬ℓ2 →ℓ1). If n is the number of variables in F, each literal can be encoded as a binary string a0a1 · · · alog n ∈B1+log n, where a0 is the sign and a1 · · · alog n is the name of the variable.

Finally, we need the notion of projection introduced in (Skyum and Valiant 1985). Intuitively, a projection is a special kind of polynomial-time reduction where each bit j in the output is determined either by the length of the input or by bit i in the input, where the index i can be computed efficiently from index j and the length of the input.

We recall the following lemma from (Fung and Tan 2023), which is inspired by the result in (Papadimitriou and Yannakakis 1986). Lemma 2. (Fung and Tan 2023) Suppose there is a projection A that takes as input a CNF formula and outputs a graph. Then, there is a polynomial-time algorithm that transforms a DQBF instance Ψ to a circuit C that succinctly represents the graph A(exp(Ψ)).

Using Lemma 2, we can prove the following. Lemma 3. Suppose there is a projection A that takes as input a CNF formula and outputs a 2-CNF formula. Then, there is a polynomial time algorithm B that transforms a DQBF instance Ψ to a 2-DQBF instance Φ such that #Φ = #A(exp(Ψ)).

Proof. Viewing 2-CNF formula as a graph and applying Lemma 2, there is a polynomial time algorithm A∗that transforms a DQBF Ψ to a circuit C that succinctly represents the implication graph of A(exp(Ψ)).

The desired algorithm B works as follows. Let Ψ be the input DQBF. First, run A∗on Ψ to obtain the circuit C(u, ¯x, u′, ¯x′), where ¯x, ¯x′ encode the names of variables and u, u′ represent the signs of literals. Then, output the 2- DQBF Φ:= ∀¯x∀¯x′ ∃y1(¯x)∃y2(¯x′) α ∧β, where α:= (¯x = ¯x′) →(y1 = y2)

β:=

^ b,b′∈B

C(b, ¯x, b′, ¯x′) ↔(yb

1 →yb′ 2)

Intuitively, α states that Φ is a uniform DQBF and β states that the implication graph of the expansion must have the same edges as GC.

We claim that #Φ = #A(exp(Ψ)), i.e., #Φ is precisely the number of solutions of the 2-CNF formula represented by the circuit C. By the definition of β, (b, ¯a) →(b′, ¯a′) is an edge in the graph GC iff a clause Xb

1,¯a →Xb′ 2,¯a′ is in exp(Φ). Since α states that Skolem functions for y1, y2 must be the same, the indices 1 and 2 in the literals Xb

1,¯a and Xb′

2,¯a′ can be dropped. It is equivalent to saying that (b, ¯a) → (b′, ¯a′) is an edge in the graph GC iff a clause Xb

1,¯a →Xb′ 1,¯a′ is in exp(Φ). Therefore, #Φ = #A(exp(Ψ)).

Lemma 4. There is a polynomial-time reduction that transforms a DQBF Ψ into two 2-DQBFs Φ1 and Φ2 such that #Ψ = #Φ1 −#Φ2.

Proof. It is shown in (Bannach et al. 2025) that there is a polynomial-time reduction that takes as input a CNF formula F and outputs two 2-CNF formulas F1 and F2 such that #F = #F1 −#F2. We observe that their reduction is in fact a projection. Using Lemma 3, we obtain the desired reduction.

The proof of Lemma 4 is non-constructive. We can strengthen it by giving an explicit reduction that runs in almost linear time, as stated in Lemma 5. The run time is quadratic in the number of existential variables and linear in the length of the matrix.

Lemma 5. There is a reduction that transforms a DQBF Ψ into two 2-DQBF Φ1 and Φ2 such that #Ψ = #Φ1 −#Φ2. The reduction runs in time O(k2|ψ|), where k is the number of existential variables in Ψ and ψ is the matrix of Ψ.

Using Lemma 4 or Lemma 5, we obtain the following theorem.

Theorem 6. #2-DQBF is #EXP-complete.

We can also show that every k-DQBF can be reduced parsimoniously to a uniform k-DQBF, which gives us the following corollary.

Corollary 7. For every k ≥2, #k-DQBF is #EXPcomplete, even when restricted to uniform k-DQBF.

First-order Model Counting (FOMC) In this section, we show a tight connection between #DQBF and FOMC. Recall that FOMC is defined as given FO sentence Ψ and a number N in unary, compute the number of models of Ψ with domain {1,..., N}. We denote by FOMCbin when the number N is given in binary.

It is implicit in (Chen et al. 2022) that FOMCbin can be reduced to #DQBF and that the reduction is parsimonious. We will describe the idea here with an example. Consider the well-known smoker-friend example for Markov Logic Networks (Richardson and Domingos 2006):

Ψ:= ∀u∀v stress(u) →smoke(u)

∧friend(u, v) ∧smoke(u) →smoke(v)

For every n, we will show how to construct a DQBF Φn such that #Φn is exactly the number of models of Ψ of size 2n.

The idea is to represent each of the predicates stress, smoke, and friend with a Skolem function. We have 2n universal variables ¯x1, ¯x2 in Φn. The first block of n variables ¯x1 corresponds to u and the second block ¯x2 corresponds to v. It has 4 existential variables, y1, y2, y3, y4, corresponding to 4 atoms stress(u), smoke(u), friend(u, v) and smoke(v). The dependency sets are ¯x1, ¯x1, ¯x1 ∪¯x2 and ¯x2, respectively. The matrix of Φn is obtained by replacing each atom in Ψ with its corresponding existential variable. Formally,

Φn:= ∀¯x1∀¯x2 ∃y1(¯x1)∃y2(¯x1)∃y3(¯x1, ¯x2)∃y4(¯x2) ϕ,

14237

<!-- Page 5 -->

where ϕ:= (y1 →y2) ∧(y3 ∧y2 →y4) ∧(¯x1 = ¯x2 →y2 = y4).

The first two conjuncts correspond to the quantifier-free parts in Ψ. The last conjunct states that y2 and y4 must be the same function, since they are intended to represent the same predicate smoke. It is not difficult to show that #Φn is precisely the number of models of Ψ with size 2n.

Next, we show that FOMC is already hard even when the domain size is fixed to 2. Theorem 8. FOMC is #EXP-hard even when the domain size is fixed to 2.

Proof. The reduction is from uniform 2-DQBF, which is #EXP-hard, by Corollary 7. We fix a uniform 2-DQBF Φ:= ∀¯x∃y1(I)∃y2(J)ϕ, where ¯x = (x1,..., xn), I = {i1,..., im} and J = {j1,..., jm}. Let S be a predicate symbol with arity m and U be a unary predicate. Define the FO sentence Ψ:= ∃u0∃u1∀v1 · · · ∀vn U(u1)∧¬U(u0)∧ψ, where ψ is the formula obtained from ϕ by replacing each xi in ϕ with U(vi) for every 1 ≤i ≤n; and y1 and y2 with S(vi1,..., vim) and S(vj1,..., vjm), respectively. The intention is that ⊤and ⊥are represented with membership in the predicate U and a Skolem function f: Bm →B is represented by the relation S. We can show that #Φ is half the number of models of Ψ with domain {1, 2}.

We further show that the logic required for #EXPhardness has satisfiability problem decidable in PSPACE, which gives us the following corollary. Corollary 9. There is a fragment L of FO of which the satisfiability problem is in PSPACE, but its corresponding FOMC is #EXP-complete even when the domain size is restricted to 2.

## Algorithm

for #2-DQBF In this section, we present an algorithm for #2-DQBF that builds on recent advances in 2-DQBF satisfiability checking using symbolic reachability (Fung et al. 2024). The key idea is to interpret the matrix of a 2-DQBF as a succinct encoding of the implication graph induced by its expansion. Our algorithm symbolically decomposes this graph into its weakly connected components and computes the model count by processing each component independently.

We fix the input 2-DQBF Φ:= ∀¯x∃y1(¯z1)∃y2(¯z2) φ. Instead of computing #Φ directly, we will compute # exp(Φ). There is a difference because a variable Xi,¯c may not even occur in exp(Φ), indicating that the Skolem function of yi is completely unconstrained at assignment ¯c. We call a variable Xi,¯c a support variable if it appears in exp(Φ); otherwise, it is called non-support. Since non-support variables can be assigned arbitrarily, it is sufficient to compute the number of solutions that assign non-support variables to a fixed value, say, ⊥. We call such solutions essential solutions.

Counting non-support variables. #Φ can be recovered from the number of essential solutions by multiplying it with 2m, where m is the number of non-support variables. The set of support/non-support variables can be characterised with Boolean formulas as follows.

## Algorithm

1: Count the number of essential solutions for Φ

1: Transform Φ to a symbolic reachability instance (I, T) using the transformation in (Fung et al. 2024) 2: if Φ is unsatisfiable then 3: return 0 4: R ←the set of all support variables 5: N ←1 6: while R̸ = ∅do 7: Pick an arbitrary variable Xi,¯c from R 8: C ←the connected component in eGΦ that contain Xi,¯c 9: NC ←the number of assignments on the variables in C that respect the implications in C 10: Remove all the variables in C from R 11: N ←N × NC 12: return N

Lemma 10. Let S1:= {¯c: ¬φ[¯z1/¯c] is satisfiable} and S2:= {¯c: ¬φ[¯z2/¯c] is satisfiable}. The set of support variables in exp(Φ) is {X1,¯c: ¯c ∈S1} ∪{X2,¯c: ¯c ∈S2}. Moreover, the number of support and non-support variables is |S1|+|S2| and (2|¯z1| −|S1|)+(2|¯z2| −|S2|), respectively.

Given a BDD for the negated matrix ¬φ, Lemma 10 can be used to efficiently compute the number of support variables |Si| by projecting out variables not in ¯zi and counting satisfying assignments.

Overview of the algorithm. In the following, let GΦ be the implication graph of exp(Φ). Let eGΦ be the undirected graph obtained from GΦ by ignoring the edge orientation and adding an edge between a literal and its negation, for every literal in exp(Φ). The connected components of eGΦ correspond to a partition of the clauses in exp(Φ) where no two components share common variables.

High-level pseudocode is shown as Algorithm 1. First, using the reduction in (Fung et al. 2024), we convert Φ to a transition system (I, T), where I is the formula for the initial states and T is the formula for the transition relation. A brief summary of this transformation can be found in the extended version. From (I, T), we can deduce whether Φ is satisfiable by constructing a formula φtr that represents the transitive closure of GΦ via BDD-based reachability. If it is not satisfiable, the algorithm immediately returns 0.

Now, suppose Φ is satisfiable. From φtr, we can also construct the formula for eGΦ. Algorithm 1 iterates through every connected component C in eGΦ that contains only the support variables. In each iteration, it computes NC, the number of assignments on the variables in C that respect the implications in C. For example, if there is an edge ℓ1 →ℓ2 in GΦ, when ℓ1 is assigned to ⊤, ℓ2 must also be assigned to ⊤. If there are k connected components C1, C2,..., Ck (that contains only support variables), then the number of essential solutions is the product Q

1≤i≤k NCi, since no two components share the same variable.

Counting over a component. This is the most technical part of the algorithm. We start with the following lemma on efficient model counting for 1-DQBF.

Lemma 11. Let Υ:= ∀¯u∃y(¯v) φ be a satisfiable 1-DQBF.

14238

<!-- Page 6 -->

• The number of Skolem functions for Υ is 2m, where m = 2|¯v| −|{¯c: ¬φ[¯v/¯c] is satisfiable}|. • In particular, for a set S ⊆B|¯v|, the number of Skolem functions for Υ that differ on S is 2m, where m = |S| − |{¯c: ¬φ[¯v/¯c] ∧(¯c ∈S) is satisfiable}|. Lemma 11 tells us that if we have a candidate Skolem function f for y1, by substituting y1 with f, we obtain a 1-DQBF instance Φ′ of which the number of Skolem functions restricted to a component can be computed efficiently via Lemma 11. We perform this for every candidate Skolem function for y1 to compute the number NC.

The main challenge is to enumerate all possible Skolem functions for y1. To do so, we combine the candidate Skolem function enumeration technique in (Reichl, Slivovsky, and Szeider 2021) and the Skolem function extraction in (Fung et al. 2024). Suppose we already have a list of Skolem functions F = {f (1),..., f (t)} for y1, where each f (i) is given as a Boolean formula. To find a Skolem function different from all functions in this list, it must differ from each f (i) at some ¯vi. Let A be a Boolean formula, over variables ¯v1,..., ¯vt where each |¯vi| = |¯z1|, maintained throughout the enumeration process. We will use A to represent the assignments we can choose to differ from each f (i). The intuition is that if M is a satisfying assignment for A, we want to find a function f with f(M(¯vi)) = ¬f (i)(M(¯vi)) for every 1 ≤i ≤t. How can we construct the Boolean formula that defines the function f? Here we employ the technique from (Fung et al. 2024). First, we “force” the variable X1,M(¯vi) to be assigned with ¬f (i)(M(¯vi)) by adding the edge

Xf (i)(M(¯vi))

1,M(¯vi) →X¬f (i)(M(¯vi))

1,M(¯vi)

into the transition relation T, for every 1 ≤i ≤t. We then check whether in the transition relation T there is a cycle that contains contradicting literals. If there is such a cycle, we move to the next satisfying assignment of A by “blocking” the assignment M in A. If there is no such cycle, we extract the function f for y1 by employing the technique from (Fung et al. 2024), add f into F, and update A by conjoining it with C1[¯z1/¯vt+1], where ¯vt+1 are fresh variables, and C1 is a Boolean formula extracted from C that specifies only the literals associated with y1.

Without additional constraints, we would enumerate many satisfying assignments M of A which do not lead to a Skolem function. For instance, if M(¯vi) = M(¯vj) = ¯a, but fi(¯a)̸ = fj(¯a), there clearly is no function ft+1 such that both ft+1(¯a)̸ = fi(¯a) and ft+1(¯a)̸ = fj(¯a). Such cases, and many more, can be excluded by conjoining A with

^

1≤i≤t ¬φtr

X

¬f(t+1)(¯vt+1) 1,¯vt+1, X f(j)(¯vj) 1,¯vj

. (3)

Recall that φtr is a formula that represents the edges of the transitive closure of the implication graph. The formula φtr

X¬f (i)(¯z(i))

1,¯z(i), Xf (j)(¯z(j))

1,¯z(j)

represents the formula obtained by substituting the variable representing the two liter- als in φtr with X¬f (i)(¯z(i))

1,¯z(i), Xf (j)(¯z(j))

1,¯z(j).

## Algorithm

2: Counting NC

1: Let C1, C2 be the literals in C associated with y1, y2, resp. 2: F, A, n ←∅, ⊤, 0 3: T ′ ←T ▷T is the transition relation constructed from Φ 4: while A is satisfiable do 5: Let M be a satisfying assignment of A ▷Force the candidate to be different from the previous ones 6: T ′ ←T ′ ∧FORCEASSIGNMENT(M, F) ▷Check if such assignments lead to no Skolem functions 7: E′ ←COMPUTEREACHABLE(E, T ′) 8: if CHECKBADCYCLE(E′) then 9: A ←A ∧BLOCKASSIGNMENT(M) 10: continue ▷Count the number of Skolem functions and update A 11: f ←COMPUTEVALIDCANDIDATE(T ′) 12: n ←n + COUNT1DQBFONCOMPONENT(f) 13: F ←F ∪{f} 14: UPDATE(A) 15: return n ▷n is the number NC

The intended meaning of Eq. (3) is as follows. The conjunct C1[¯z1/¯vt+1] states that the place ¯v where the next Skolem function differs from f must be in component C1.

Each conjunct ¬φtr

X¬f (i)(¯z(i))

1,¯z(i), Xf (j)(¯z(j))

1,¯z(j)

ensures that the edge X¬f (i)(¯z(i))

1,¯z(i) →Xf (j)(¯z(j))

1,¯z(j) is not in the transitive closure of GΦ. Otherwise, if such an edge is present, when we force X1,M(¯vi) to be ¬f (i)(M(¯vi)) and X1,M(¯vj) to be ¬f (j)(M(¯vj)), we will find a bad cycle and there will be no solutions.

We present the algorithm to compute NC formally as Algorithm 2. We first split C into two sets C1 and C2 that contain the literals associated with y1 and y2, respectively.

In Line 8, we force the assignment by adding into T the edge Xf (i)(M(¯vi))

1,M(¯vi) →X¬f (i)(M(¯vi))

1,M(¯vi), for every 1 ≤i ≤t. In Line 9 we run the command reach from ABC to check whether there is a cycle containing contradicting literals. If there is such a cycle, the assignment M is blocked in Line 11. In Line 13 we extract a Skolem function using the technique from (Fung et al. 2024). In Line 14, we count the number of solutions for the 1-DQBF instance after substituting y1 with the new Skolem function f. Finally, in Line 16 we update the formula A by conjoining it with the conjunction in Eq. (3).

## Experiments

We implemented the algorithm from the previous section in a tool called sharp2DQR. Formulas such as R, GΦ, φtr, S1 and S2 are represented as BDDs using cudd (Somenzi 2009). This offers several advantages. For example, the formula φtr can be computed using BDD-based reachability as implemented in ABC’s reach command (Brayton and Mishchenko 2010). The number of support/non-support variables can also be computed easily by constructing the BDD for S1 and S2 from ¬φ with existential quantification.

To evaluate our model counter, we generated a diverse family of benchmarks, which we divided into three batches of instances.

14239

<!-- Page 7 -->

0 100 200 300 400 500 600 Time

0

50

100

150

200

## of solved instances

PEC_small

0 100 200 300 400 500 600 Time

0

100

200

300

400

## of solved instances

PEC_opt

0 25 50 75 100 125 # of bits

10 3

10 2

10 1

100

101

102

103

Time

2_colorability sharp2DQR Exp+ganak (z3) Exp+ganak (cm)

**Figure 1.** The two figures on the left show the performance of the solvers on the PEC instances, the horizontal axis corresponds to the running time (s), and the vertical axis to the number of solved instances. The figure on the right shows the performance of the solvers on the 2-colorability instances; the horizontal axis corresponds to the number of bits of the graph in the instance, and the vertical axis to the running time (s).

• PEC opt: These are instances with a dependency set size of 10 to 50. They are generated in a similar manner as in (Fung et al. 2024). There are 370 instances in this batch. One third of these have 0 non-support variables. • PEC small: These are instances generated from the IS- CAS89 instances with a dependency set size of 3 to 10 variables. There are 192 instances in this batch. • 2 colorability: These are the 2 colorability instances as in (Fung et al. 2024). These are succinctly represented graphs with 2 to 127 bits, each of them contains exactly two Skolem functions.

For PEC opt and PEC small, the number of Skolem functions ranges from 1 to more than 2264 and the number of connected components ranges from 1 to more than 1600.

We evaluated the performance of sharp2DQR against ganak (Sharma et al. 2019), which is used to count the number of models of the expansion as defined in Eq. (2). The expansion is computed via cryptominisat5 (Soos, Nohl, and Castelluccia 2009) or z3 (De Moura and Bjørner 2008) as follows: First, we obtain a model M of ¬φ. Then, we generate the corresponding clauses in the expansion. Then, we add a blocking clause ∧x∈¯z1∪¯z2∪{y1,y2}x̸ = M[x] to ¬φ to prevent duplicated solutions and repeat until the formula becomes unsatisfiable. This method is called Exp+ganak.

The experiments were conducted on Ubuntu 22.04.4 LTS with 48 GB of 2400MHz DDR4 memory and an i5-13400 CPU. Each solver had 600 seconds to solve each instance.

**Figure 1.** shows that sharp2DQR fell short on PEC small instances, but it is significantly better than Exp+ganak on PEC opt instances. This is because the dependency set size is larger on PEC opt instances, and since the expansion size is exponential to the dependency set size, our method, without expanding, performs better on larger instances. Most of the time spent by Exp+ganak is used on computing the expansion, and on many instances ganak finishes counting quite quickly after the expansion. sharp2DQR does not work well on small instances because sometimes BDD operations take too long, and on

the PEC small instances, the number of unsatisfying models is small enough that enumeration is not too much of a problem. We also notice that for Exp+ganak, the performance of using cryptominisat5 and z3 is similar, but cryptominisat5 is better on the PEC opt instances.

For 2 colorability, Exp+ganak was unable to solve any instances larger than 12 bits, while sharp2DQR successfully solved instances up to 127 bits. This is due to the fact that the number of clauses in the expansion is Θ(2n) for an n-bit graph, making full expansion very expensive.

More experimental results and analysis can be found in the extended version. We also compared both Exp+ganak and sharp2DQR against the latest FOMC tool WFOMC (Wang 2025), where we encode counting the number of 2-colorings and independent sets on some specific graphs. In all instances, WFOMC can only handle model sizes of up to 4, far lower than what sharp2DQR can handle, which in some instances is 2127. However, in the independent set counting instances, Exp+ganak performs better than sharp2DQR.

Concluding Remarks

We established that #2-DQBF is as hard as general #DQBF. Specifically, we proved that it is #EXP-complete by leveraging the connections between k-DQBF and k- SAT (Fung and Tan 2023) and the technique in (Bannach et al. 2025).

On the experimental front, we introduced a novel algorithm for #2-DQBF using BDD-based symbolic reachability. As a baseline, we also implemented an approach that relies on universal expansion followed by propositional model counting. While our algorithm scaled better with larger dependency sets, the expansion-based method works for general DQBF and may be worth exploring further.

To the best of our knowledge, this is the first paper investigating model counting for DQBF, and there are many avenues for future research. One natural next step is to generalize our algorithm to handle 3-DQBF.

14240

<!-- Page 8 -->

## Acknowledgements

We thank the reviewers for their detailed and constructive comments on the initial version. We acknowledge the generous support of the Royal Society International Exchange Grant no. R3\233183, the National Science and Technology Council of Taiwan grant no. 111-2923-E-002-013-MY3 and 114-2221-E-002-183-MY3, and the NTU Center of Data Intelligence: Technologies, Applications, and Systems grant no. NTU-113L900903.

## References

Balabanov, V.; Chiang, H. K.; and Jiang, J. R. 2014. Henkin quantifiers and Boolean formulae: A certification perspective of DQBF. Theor. Comput. Sci., 523: 86–100. Balabanov, V.; and Jiang, J. R. 2015. Reducing Satisfiability and Reachability to DQBF. In QBF Workshop. Bannach, M.; Demaine, E. D.; Gomez, T.; and Hecher, M. 2025. #P is Sandwiched by One and Two #2DNF Calls: Is Subtraction Stronger Than We Thought? In LICS. Beame, P.; den Broeck, G. V.; Gribkoff, E.; and Suciu, D. 2015. Symmetric Weighted First-Order Model Counting. In PODS. Biere, A.; Fleury, M.; Froleyks, N.; and Heule, M. J. H. 2023. The SAT Museum. In J¨arvisalo, M.; and Berre, D. L., eds., SAT. Biere, A.; Heule, M.; van Maaren, H.; and Walsh, T., eds. 2009. Handbook of Satisfiability. IOS Press. Bloem, R.; K¨onighofer, R.; and Seidl, M. 2014. SAT-Based Synthesis Methods for Safety Specs. In VMCAI. Bradley, A. 2011. SAT-Based Model Checking without Unrolling. In VMCAI. Bradley, A.; and Manna, Z. 2007. Checking Safety by Inductive Generalization of Counterexamples to Induction. In FMCAD. Brayton, R.; and Mishchenko, A. 2010. ABC: An Academic Industrial-Strength Verification Tool. In CAV. Capelli, F.; Lagniez, J.; Plank, A.; and Seidl, M. 2024. A Top-Down Tree Model Counter for Quantified Boolean Formulas. In IJCAI. Chatterjee, K.; Henzinger, T.; Otop, J.; and Pavlogiannis, A. 2013. Distributed Synthesis for LTL Fragments. In FMCAD. Chen, F.-H.; Huang, S.-C.; Lu, Y.-C.; and Tan, T. 2022. Reducing NEXP-complete problems to DQBF. In FMCAD. Cheng, C.; Fung, L.-H.; Jiang, J.-H. R.; Slivovsky, F.; and Tan, T. 2025. Fine-Grained Complexity Analysis of Dependency Quantified Boolean Formulas. In SAT. Dalvi, N.; and Suciu, D. 2004. Efficient Query Evaluation on Probabilistic Databases. In VLDB. De Moura, L.; and Bjørner, N. 2008. Z3: An efficient SMT solver. In TACAS. E´en, N.; Mishchenko, A.; and Brayton, R. 2011. Efficient Implementation of Property Directed Reachability. In FM- CAD.

Fichte, J. K.; Berre, D. L.; Hecher, M.; and Szeider, S. 2023. The Silent (R)evolution of SAT. Commun. ACM, 66(6): 64– 72. Fr¨ohlich, A.; Kov´asznai, G.; Biere, A.; and Veith, H. 2014. iDQ: Instantiation-Based DQBF Solving. In Pragmatics of SAT Workshop (POS). Fung, L.; and Tan, T. 2023. On the Complexity of k-DQBF. In SAT. Fung, L.-H.; Cheng, C.; Fan, Y.-W.; Tan, T.; and Jiang, J.- H. R. 2024. 2-DQBF Solving and Certification via Property- Directed Reachability Analysis. In FMCAD. Galperin, H.; and Wigderson, A. 1983. Succinct Representations of Graphs. Inf. Control., 56(3): 183–198. Ge-Ernst, A.; Scholl, C.; S´ıc, J.; and Wimmer, R. 2022. Solving Dependency Quantified Boolean Formulas using Quantifier Localization. Theor. Comput. Sci., 925: 1–24. Gitina, K.; Reimer, S.; Sauer, M.; Wimmer, R.; Scholl, C.; and Becker, B. 2013a. Equivalence checking of partial designs using dependency quantified Boolean formulae. In ICCD. Gitina, K.; Reimer, S.; Sauer, M.; Wimmer, R.; Scholl, C.; and Becker, B. 2013b. Equivalence checking of partial designs using dependency quantified Boolean formulae. In ICCD. Gitina, K.; Wimmer, R.; Reimer, S.; Sauer, M.; Scholl, C.; and Becker, B. 2015. Solving DQBF through quantifier elimination. In DATE. Golia, P.; Roy, S.; and Meel, K. S. 2021. Program Synthesis as Dependency Quantified Formula Modulo Theory. In IJCAI. Golia, P.; Roy, S.; and Meel, K. S. 2023. Synthesis with Explicit Dependencies. In DATE. Gomes, C. P.; Sabharwal, A.; and Selman, B. 2021. Model Counting. In Biere, A.; Heule, M.; van Maaren, H.; and Walsh, T., eds., Handbook of Satisfiability - Second Edition. Jiang, J. R. 2009. Quantifier Elimination via Functional Composition. In CAV. Kuehlmann, A.; Paruthi, V.; Krohm, F.; and Ganai, M. 2002. Robust Boolean reasoning for equivalence checking and functional property verification. IEEE Trans. Comput. Aided Des. Integr. Circuits Syst., 21(12): 1377–1394. Ladner, R. 1989. Polynomial Space Counting Problems. SIAM J. Comput., 18(6): 1087–1097. Lewis, H. 1980. Complexity Results for Classes of Quantificational Formulas. J. Comput. Syst. Sci., 21(3): 317–353. Papadimitriou, C.; and Yannakakis, M. 1986. A Note on Succinct Representations of Graphs. Inf. Control., 71(3): 181–185. Peterson, G.; and Reif, J. 1979. Multiple-Person Alternation. In FOCS. Plank, A.; M¨ohle, S.; and Seidl, M. 2024. Counting QBF solutions at level two. Constraints, 29(1-2): 22–39. Pulina, L.; and Seidl, M. 2019. The 2016 and 2017 QBF solvers evaluations (QBFEVAL’16 and QBFEVAL’17). Artif. Intell., 274: 224–248.

14241

<!-- Page 9 -->

Reichl, F.; and Slivovsky, F. 2022. Pedant: A Certifying DQBF Solver. In SAT. Reichl, F.; Slivovsky, F.; and Szeider, S. 2021. Certified DQBF Solving by Definition Extraction. In SAT. Richardson, M.; and Domingos, P. M. 2006. Markov logic networks. Mach. Learn., 62(1-2): 107–136. Scholl, C.; and Becker, B. 2001. Checking Equivalence for Partial Implementations. In DAC. Sharma, S.; Roy, S.; Soos, M.; and Meel, K. S. 2019. GANAK: A Scalable Probabilistic Exact Model Counter. In IJCAI. Shaw, A.; Juba, B.; and Meel, K. S. 2024. An approximate skolem function counter. In AAAI. S´ıc, J.; and Strejcek, J. 2021. DQBDD: An Efficient BDD- Based DQBF Solver. In SAT. Skyum, S.; and Valiant, L. 1985. A Complexity Theory Based on Boolean Algebra. J. ACM, 32(2): 484–502. Somenzi, F. 2009. CUDD: CU decision diagram package release 2.4. 2. University of Colorado at Boulder. Soos, M.; Nohl, K.; and Castelluccia, C. 2009. Extending SAT Solvers to Cryptographic Problems. In Kullmann, O., ed., SAT. Tentrup, L.; and Rabe, M. 2019. Clausal Abstraction for DQBF. In SAT. T´oth, J.; and Kuzelka, O. 2024. Complexity of Weighted First-Order Model Counting in the Two-Variable Fragment with Counting Quantifiers: A Bound to Beat. In KR. Trakhtenbrot, B. 1950. The impossibility of an algorithm for the decidability problem on finite classes. In D. Akad. Nauk USSR, 70(1), 569–572. Valiant, L. 1979a. The Complexity of Computing the Permanent. Theor. Comput. Sci., 8: 189–201. Valiant, L. 1979b. The Complexity of Enumeration and Reliability Problems. SIAM J. Comput., 8(3): 410–421. van Bremen, T.; and Kuzelka, O. 2023. Lifted inference with tree axioms. Artif. Intell., 324: 103997. Vardi, M. Y. 1982. The Complexity of Relational Query Languages (Extended Abstract). In STOC. Wang, Y. 2025. https://github.com/yuanhong-wang/ WFOMC. Accessed: 2025-07-28. Wimmer, R.; Karrenbauer, A.; Becker, R.; Scholl, C.; and Becker, B. 2017. From DQBF to QBF by Dependency Elimination. In SAT.

14242
