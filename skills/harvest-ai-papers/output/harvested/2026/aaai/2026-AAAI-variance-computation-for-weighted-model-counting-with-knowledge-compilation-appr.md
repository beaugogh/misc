---
title: "Variance Computation for Weighted Model Counting with Knowledge Compilation Approach"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39007
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39007/42969
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Variance Computation for Weighted Model Counting with Knowledge Compilation Approach

<!-- Page 1 -->

Variance Computation for Weighted Model Counting with Knowledge Compilation Approach

Kengo Nakamura, Masaaki Nishino, Norihito Yasuda

Communication Science Laboratories, NTT, Inc., Kyoto, Japan

{kengo.nakamura,masaaki.nishino,norihito.yasuda}@ntt.com

## Abstract

One of the most important queries in knowledge compilation is weighted model counting (WMC), which has been applied to probabilistic inference on various models, such as Bayesian networks. In practical situations on inference tasks, the model’s parameters have uncertainty because they are often learned from data, and thus we want to compute the degree of uncertainty in the inference outcome. One possible approach is to regard the inference outcome as a random variable by introducing distributions for the parameters and evaluate the variance of the outcome. Unfortunately, the tractability of computing such a variance is hardly known. Motivated by this, we consider the problem of computing the variance of WMC and investigate this problem’s tractability. First, we derive a polynomial time algorithm to evaluate the WMC variance when the input is given as a structured d-DNNF. Second, we prove the hardness of this problem for structured DNNFs, d-DNNFs, and FBDDs, which is intriguing because the latter two allow polynomial time WMC algorithms. Finally, we show an application that measures the uncertainty in the inference of Bayesian networks. We empirically show that our algorithm can evaluate the variance of the marginal probability on real-world Bayesian networks and analyze the impact of the variances of parameters on the variance of the marginal.

Code — https://github.com/nttcslab/variance-wmc

## Introduction

Knowledge compilation is a technique that represents a propositional formula, a.k.a., a Boolean function, as a compressed and tractable form. Once Boolean functions are compiled into certain representations, we can solve various queries in polynomial time in the sizes of the representations (Darwiche and Marquis 2002). Among various queries, the most prominent one is weighted model counting (WMC), which is the problem of counting the (weighted) number of satisfying assignments of a Boolean function. WMC has been applied to various probabilistic inference tasks on, e.g., Bayesian networks (Chavira and Darwiche 2008; Dilkas and Belle 2021), factor graphs (Choi, Kisa, and Darwiche 2013), and probabilistic programming (Fierens et al. 2011; Holtzen, Van den Broeck, and Millstein 2020).

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

(a) A B

(b)

A yes no

0.7 0.3 A\B yes no yes 0.8 0.2 no 0.1 0.9 ⇒Pr(B =yes)=0.59

(c)A yes no p1 1−p1

A\B yes no yes p2 1−p2 no p3 1−p3 E[p1]=0.7, V[p1]=0.1 E[p2]=0.8, V[p2]=0.05 E[p3]=0.1, V[p3]=0.01 ⇒E[Pr(B =yes)]=0.59 ⇒V[Pr(B =yes)]=0.0804

**Figure 1.** (a) A Bayesian network. (b) Example of ordinal inference, where parameters are fixed. (c) Example of our situation where parameters have variances.

In practical situations, the parameters of such probabilistic models are often obtained by learning from data (Cozman 2000; Heckerman 2008). When we lack sufficient data, they may suffer from uncertainty. Perhaps such an uncertainty leads to unreliable inference results. However, ordinal inference methods (including methods using WMC) disregard uncertainty in parameters. Thus, we want to compute the degree of uncertainty in the inference outcome when the parameters are imprecise. A Bayesian statistical approach regards the inference outcome as a random variable by considering the distributions for the parameters and computes the variance of the outcome. For example, for the Bayesian network in Fig. 1(a), we consider the variance of the outcome when parameters follow distributions, as in Fig. 1(c). By introducing the expectation and variance of parameters, the outcome’s expectation equals the marginal, and we can also obtain its variance. The computed variance affects the decision-making that depends on the inference outcome; when the computed variance is too large, we should regard the inference result as unreliable. However, the tractability of computing the variance of the inference outcome remains unknown; although the variance computation is expected to be at least as difficult as the ordinal inference, we do not know the extent of its difficulty.

In the applications of inference, the WMC value typically equals the inference outcome. Thus, motivated by the variance computation of the inference outcome, we consider the query of computing the variance of WMC value when the weights associated with Boolean variables have variances. As explained later, a previous study (Nakamura et al. 2022) treated the variance of WMC value with knowledge compilation in a special case of network analysis. However, this work is specialized to network analysis and does not con-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19312

<!-- Page 2 -->

sider general WMC tasks. Moreover, it only uses ordered binary decision diagrams (OBDDs) (Bryant 1986), one of the most restricted representations in knowledge compilation. Therefore, this work hardly reveals the tractability of variance computation including inference tasks. Thus, we formalize variance computation query for the WMC of general Boolean function and investigate the tractability of it with various knowledge compilation representations.

Our contributions are three-fold. First, we propose a polynomial time algorithm that computes the variance of WMC of a Boolean function represented as a structured d- DNNF (Pipatsrisawat and Darwiche 2008). This result is meaningful since structured d-DNNFs subsume sentential decision diagrams (SDDs) (Darwiche 2011), which have been widely used in many applications, as a subset. Second, we prove that we cannot compute the WMC’s variance in polynomial time unless P=NP when the Boolean function is represented as a structured DNNF, a d-DNNF (Darwiche 2001), or an FBDD (Gergov and Meinel 1994), all of which are strict supersets of structured d-DNNFs. The results for d-DNNFs and FBDDs are interesting because the WMC itself can be computed in polynomial time for these representations. Third, we present an application for the inference of Bayesian networks and show that the variance of the marginal probability can be obtained in polynomial time for a Bayesian network with a constant treewidth. We also empirically demonstrate the tractability of the proposed algorithm with real-world Bayesian networks and showcase an example of uncertainty analysis on Bayesian networks with variance computation. Particularly, we demonstrated that we can find parameters of a Bayesian network whose variances have greater impact on the variance of the marginal probability, a useful result for the additional learning of parameters that effectively reduce the uncertainty of the inference.

The URL of the full version of this paper is announced on https://github.com/nttcslab/variance-wmc.

## Related Work

Knowledge compilation is regarded as a key technique for tackling computationally difficult propositional reasoning tasks. Thus, as well as the succinctness of representations, the tractability for various operations is the central research subject. Knowledge compilation map (Darwiche and Marquis 2002), which summarizes the succinctness and tractability of various representations, have been extended by subsequent studies. For example, the tractability of standard operations has been studied for recently proposed representations (Illner 2025; Onaka et al. 2025) and the tractability of the generalization of WMC such as algebraic model counting (AMC) and two-level AMC (2AMC) was recently investigated (Kiesel, Totis, and Kimmig 2022; Wang et al. 2024). Our study broadens the application of knowledge compilation by proposing a new query related to probabilistic inference, which is a major application of knowledge compilation, and investigating this query’s position on the knowledge compilation map.

In probabilistic inference, it is crucial to deal with uncertainty in parameters. A typical approach to incorporate uncertainty is a fully Bayesian approach, where we regard every parameter as drawn from a distribution, as in the Introduction. However, to the best of our knowledge, no study has considered the variance of the marginal in a Bayesian network with this approach. Another line of research for incorporating uncertainty in Bayesian networks is credal networks (Cozman 2000), where imprecise probabilities are modeled as sets of distributions called credal sets. Credal networks enable robust inferences by computing the bounds of the marginal probability when the parameters have fluctuated within given bounds. However, marginal inference for credal networks is NP-hard even for networks with constant treewidth (De Campos and Cozman 2005). In contrast, our approach can compute the variance of the marginal in polynomial time for networks with constant treewidth.

WMC has also been applied to the reliability analysis on communication networks where links are stochastically failed (Duenas-Osorio et al. 2017). For this purpose, Boolean function f ′, which indicates the connectivity in sub-networks, is considered and the reliability equals the WMC of f ′ (Hardy, Lucet, and Limnios 2007). Nakamura et al. (2022) proposed an algorithm that computes the variance of reliability in polynomial time in the size of the OBDD (Bryant 1986) representing f ′ when the existential probability of each link in the network has variance. We extend their problem setting and algorithm to handle WMC’s variance computation of a general Boolean function. Moreover, we extended their algorithm to work on structured d- DNNFs, a strict superset of OBDDs; here, our algorithm’s key technical difference is its management of variable sets and variable decompositions guided by a vtree, as described later. As a byproduct, we can prove that the variance of network reliability on networks with constant treewidth can be computed in polynomial time. This theoretically improves the previous result (Nakamura et al. 2022) stating that it can be computed in polynomial time for networks with constant pathwidth, since the treewidth subsumes the pathwidth but not vice versa; details are in the full version.

There exist studies to represent a probability distribution of a random variable X as a tractable circuit in a spirit of knowledge compilation: probabilistic circuits (Choi, Vergari, and Van den Broeck 2020) represent probability mass functions, while probabilistic generating circuits (Zhang, Juba, and Van den Broeck 2021) and characteristic circuits (Yu, Trapp, and Kersting 2023) represent probability generating and characteristic functions. These circuits admit polytime moment computation, including the variance, of the random variable X under certain structural restrictions. In contrast, our work regards the probability Pr(X = a) as a random variable and computes the variance of it, where X is a random variable appearing in, e.g., Bayesian networks. To derive the variance of the inference outcome, our work is needed because we currently have no approach to compute the variance of the probability value seen as a random variable with probabilistic circuits.

## Preliminaries

A Boolean function takes a set of Boolean variables each valued true or false as an input and outputs either true or false. An assignment a on variable set V is a mapping V →

19313

<!-- Page 3 -->

{true, false}. Assignment a is called a model of Boolean function f if f is evaluated to true under a.

A rooted directed acyclic graph is called a negation normal form (NNF) if the leaf nodes are labeled with true, false, x, or ¬x, where x is a Boolean variable, and the internal nodes are labeled with either ∧or ∨. The size of the NNF is defined as the number of arcs. For node α of an NNF, Boolean function fα represented by α is defined as follows. For leaf node α, fα = α; true and false stand for identity functions that always evaluate to true and false. For internal node α, let α1,..., αk be the child nodes of α. If α is a ∧node, fα = V j fαj. If α is a ∨-node, fα = W j fαj. The Boolean function represented by an NNF is that represented by its root node. We often abuse a symbol for NNF node α to represent the whole NNF rooted at α.

Next, we define several restrictions on NNFs, which induce subsets of NNFs. For NNF node α, let Var(α) be the set of Boolean variables that appear as the labels of the descendant nodes of α, called the scope of α. In the following, let α1,..., αk be the child nodes of internal node α. Definition 1. An NNF is called decomposable if every ∧node α satisfies Var(αi) ∩Var(αj) = ∅for any i̸ = j. An NNF is called deterministic if every ∨-node α satisfies fαi ∧ fαj = false for any i̸ = j. An NNF is called decision if every ∨-node only appears in the form: (x ∧α) ∨(¬x ∧β), where x, ¬x are leaf nodes.

A d-DNNF is a decomposable and deterministic NNF, and FBDD is a decomposable and decision NNF with the following additional restriction; for every ∨-node, α, β in the decision property must be either a leaf node or a ∨-node. We also define structured decomposability as follows. Definition 2. A vtree T on variable set V is a rooted binary tree, where each leaf node is labeled with a Boolean variable in V and each internal node v has exactly two child nodes vl, vr. Here, any Boolean variable x ∈V must appear as a label exactly once. To distinguish them from NNF nodes, we call the nodes of a vtree a vnode. The scope Var(v) of vnode v is the set of the labels of the descendants of v. For NNF node α, its decomposition vnode d(α) of vtree T is the deepest vnode v in T satisfying Var(α) ⊆Var(v). Definition 3. We say an NNF respects vtree T if every ∧node α has exactly two child nodes αl, αr and they satisfy Var(αl) ⊆Var(vl) and Var(αr) ⊆Var(vr) for some vnode v of T. An NNF is called structured decomposable if it respects some vtree.

A structured DNNF (st-DNNF) is a structured decomposable NNF. A structured d-DNNF (st-d-DNNF) is a structured decomposable and deterministic NNF. Example 4. Let f = (¬a ∧b ∧¬c ∧d) ∨(a ∧b ∧¬c ∧d) ∨ (a ∧b ∧c ∧¬d). Fig. 2(a) depicts an st-d-DNNF of f and the respected vtree. Fig. 2(b) is a d-DNNF of f; however, it is not structured decomposable because the left child of the root decomposes the variables into {a, d} and {b, c} while the right child decomposes them into {a, b} and {c, d}.

Here, we assume that, for any ∧-node α of an st-d-DNNF with child nodes αl, αr, Var(αl)̸ = ∅and Var(αr)̸ = ∅. We can easily transform an st-d-DNNF to satisfy the above a b c d

(a) ∨ ∧ ∧

∨ ∧ ∧ ∧ ∧

¬a b ¬c d a b c ¬d

(b) ∨ ∧ ∧ ∧ ∨ ∧

∧ ∧ ∧ ¬a d b ¬c a b

¬c d c ¬d

**Figure 2.** (a) A vtree and an st-d-DNNF. (b) A d-DNNF that is not structured decomposable.

assumption. If Var(αl) = ∅, fαl is either true or false. When fαl = true, we can replace α with αr; i.e., we eliminate α and redirect the incoming arcs of α to αr. Otherwise, we can replace α with false. We can perform the same transformation when Var(αr) = ∅. Under this assumption, the vnode v appeared in Definition 3 is determined as v = d(α). This can be proved as follows. We have Var(α) = Var(αl) ∪Var(αr) ⊆Var(vl) ∪Var(vr) = Var(v). Also, we have Var(α) ⊈Var(vl) following from Var(α) \ Var(vl) = Var(αr)̸ = ∅. Similarly, Var(α) ⊈Var(vr). Therefore, v is the deepest vnode such that Var(α) ⊆Var(v).

Variance of Weighted Model Counting We first define the WMC. We denote the set of models of f on variable set V by AV f. For each variable x in variable set V, we assign positive weight Px and negative weight Nx. Then we define the WMC W V f of f on variable set V by

W V f:=

X a∈AV f

W V a, W V a:=

Y x∈V a(x)=true

Px ·

Y x∈V a(x)=false

Nx. (1)

Note that the value of W V f changes by modifying V. Thus, when considering the WMC, we must care about the variable set. If V is clear from the context, we omit the superscripts.

In existing studies, Px and Nx are given as real values without uncertainty. In this paper, for every variable x ∈V, Px and Nx are regarded as random variables with bounded expectation and variance. Then, WMC Wf, defined by (1), is also a random variable with bounded expectation and variance. This virtually considers the variance of the inference outcome in the applications since the WMC value typically equals the outcome, as described in Introduction.

We assume that (Px, Nx) and (Py, Ny) are independent for x̸ = y, while Px and Nx for the same x are not necessarily independent. Then the expectation E[Wf] is equivalent to the ordinal WMC: E[W V f ] = P a∈AV f E[W V a ] = P a∈AV f

Q x∈V:a(x)=true E[Px] · Q x∈V:a(x)=false E[Nx]. This assumption is reasonable for some applications, and later we slightly relax it for a specific application; see the Application section. Now we formally define the variance computation queries. Problem 5. We are given expectations µPx, µNx and variances σ2

Px, σ2

Nx of Px, Nx and covariance σPxNx of Px and Nx for every x ∈V. We define variance computation query VC as the computation of variance V[W V f ] of WMC of input Boolean function f. As a related one, we define covariance computation query CVC as the computation of covariance Cov[W V f, W V g ] of WMCs of input Boolean functions f, g.

19314

<!-- Page 4 -->

We have Cov[Wf, Wg] = P a∈Af

P b∈Ag Cov[Wa, Wb], each term of which can be computed in O(|V|) time. Thus, if the models of Boolean functions are explicitly enumerated, we can compute V[Wf] = Cov[Wf, Wf] in O(|V||Af|2) time and Cov[Wf, Wg] in O(|V||Af||Ag|) time. Example 6. Let f be the Boolean function in Example 4. Let µPx = µ, µNx = 1 −µ, σ2

Px = σ2

Nx = σ2, and σPxNx = −σ2 for any x ∈V = {a, b, c, d}. Then Wf = NaPbNcPd + PaPbNcPd + PaPbPcNd, and thus E[Wf] = µ2 −µ4. Similarly, V[Wf] = (2µ2 −2µ3 −2µ4 + 4µ6)σ2 + (1 −2µ + 2µ2 + 6µ4)σ4 + (2 + 4µ2)σ6 + σ8. However, since |Af| and |Ag| are generally exponential in |V|, this solution causes a prohibitively long running time. Therefore, we consider how to solve these queries when Boolean functions are represented as NNFs.

Tractability Results The goal of this section is to prove the following theorem. Theorem 7. When f, g are given as st-d-DNNFs α, β respecting the same vtree, CVC can be solved in O(|α||β| + |V|2) time. Thus, when f is given as an st-d-DNNF α, VC can be solved in O(|α|2 + |V|2) time.

We first introduce some fundamental formulas that are frequently used. Given random variables A, B, C, X, Y, suppose that (A, B) and (X, Y) are independent. Then,

Cov[A + B, C] = Cov[A, C] + Cov[B, C], (2) Cov[AX, BY ] = Cov[A, B]Cov[X, Y ]

+Cov[A, B]E[X]E[Y ] + E[A]E[B]Cov[X, Y ]. (3)

Eq. (2) is a well-known formula derived from the linearity of covariances. Eq. (3) is analogous to the formula for the variance of the product of independent random variables; the proof of (3) can be found in (Nakamura et al. 2022).

Using these formulas, we design an algorithm to compute Cov[Wfα, Wfβ] for given st-d-DNNFs α, β respecting the same vtree. The proposed algorithm computes Cov[Wfα, Wfβ] by recursively decomposing it into the sums and products of Cov[Wfα′, Wfβ′ ]s, where α′, β′ are the child nodes of α, β. To avoid redundant recursive calls, the value of Cov[Wfα′, Wfβ′] is cached once it is computed. However, since WMC value W V f is altered by changing variable set V, we must track the variable set in decomposing the covariance. We manage the variable set by fully using the vtree. More specifically, let anc = LCA(d(α), d(β)) be the lowest common ancestor (LCA) of d(α) and d(β), which is the deepest vnode v such that it is the ancestor of both d(α) and d(β). Our algorithm recursively computes Cov[W V fα, W V fβ], where V = Var(anc). In the following, for convenience, we define d(true) = d(false) = ⊥, which is an imaginary vnode satisfying Var(⊥) = ∅, LCA(⊥, ⊥) = ⊥, and LCA(v, ⊥) = v for any other vnode v. In other words, ⊥is a vnode that is a descendant of any other vnodes.

Decomposition Lemmas To derive the algorithm, we must determine how the covariance is decomposed into the covariances of child nodes.

We derive decomposition formulas by conducting a comprehensive case analysis: (I) d(α) and d(β) have no ancestordescendant relation, (II) d(α) is an ancestor of d(β) and α is a ∨-node, and (III) d(α) is an ancestor of d(β) and α is a ∧-node. Here, (II) and (III) allow d(α) = d(β). Note that when d(β) is an ancestor of d(α), we can swap α and β to satisfy (II) or (III). In the following, we derive decomposition formulas for each case.

In case (I), i.e., both anc̸ = d(α) and anc̸ = d(β) hold, the following decomposition holds by considering how fα and fβ can be represented on variable set Var(anc). Lemma 8. In case (I), by letting V:= Var(anc), Vl:= Var(ancl), and Vr:= Var(ancr), we have

Cov[W V fα, W V fβ] = Cov[W Vl fα, W Vl true]Cov[W Vr true, W Vr fβ ]

+ Cov[W Vl fα, W Vl true]E[W Vr true]E[W Vr fβ ] (4)

+ E[W Vl fα ]E[W Vl true]Cov[W Vr true, W Vr fβ ].

Proof. Since Var(α) ⊆Vl, Vl ∪Vr = V, and Vl ∩Vr = ∅, fα on variable set V can be represented as fα ∧trueVr, where trueVr is a true function on variable set Vr. Thus, we have W V fα = W Vl fα W Vr true. Similarly, W V fβ = W Vl trueW Vr fβ.

Since (W Vl fα, W Vl true) and (W Vr true, W Vr fβ) are independent, the lemma follows from (3).

In case (II), we have the following decomposition. Lemma 9. In case (II), by letting V:= Var(anc) and α1,..., αk be the child nodes of α, we have

Cov[W V fα, W V fβ] = Pk j=1 Cov[W V fαj, W V fβ]. (5)

Proof. By determinism of fα = Wk j=1 fαj, we have W V fα = Pk j=1W V fαj. Eq. (5) follows by recursively applying (2).

In case (III), two child nodes αl, αr satisfy Var(αl) ⊆ Var(ancl) and Var(αr) ⊆Var(ancr) by structured decomposability. This leads to the following decomposition. Lemma 10. In case (III), suppose fβ can be decomposed as f ′ β ∧f ′′ β, where Var(f ′ β) ⊆Var(ancl) =: Vl and Var(f ′′ β) ⊆ Var(ancr) =: Vr. Then, by letting V:= Var(anc),

Cov[W V fα, W V fβ] = Cov[W Vl fαl, W Vl f ′ β ]Cov[W Vr fαr, W Vr f ′′ β ]

+ Cov[W Vl fαl, W Vl f ′ β ]E[W Vr fαr ]E[W Vr f ′′ β ] (6)

+ E[W Vl fαl ]E[W Vl f ′ β ]Cov[W Vr fαr, W Vr f ′′ β ].

Proof. We have W V fα = W Vl fαl W Vr fαr and W V fβ = W Vl f ′ β W Vr f ′′ β, where (W Vl fαl, W Vl f ′ β) and (W Vr fαr, W Vr f ′′ β) are independent. The lemma follows from (3).

We can decompose fβ = f ′ β ∧f ′′ β for the following cases. If anc̸ = d(β), either Var(d(β)) ⊆Vl or Var(d(β)) ⊆Vr holds. We can take (f ′ β, f ′′ β) = (fβ, true) for the former and (f ′ β, f ′′ β) = (true, fβ) for the latter. If anc = d(β) and β is a ∧-node, child nodes βl, βr satisfy Var(βl) ⊆Vl and Var(βr) ⊆Vr by structured decomposability.

19315

<!-- Page 5 -->

Procedure and Complexity

We can recursively decompose Cov[Wfα, Wfβ] into the covariances and expectations of the WMCs of child nodes with Lemmas 8–10. The base cases of the recursion, e.g., the case where both are literals with the same Boolean variable, can be resolved using the input (co)variances σ2

Px, σ2

Nx, σPxNx of weights. Also, we pre-compute E[Wfγ] for every node γ in st-d-DNNFs α, β. Since this procedure is identical to a standard one for computing WMC with st-d-DNNFs, the details of computing expectations are in the full version.

## Algorithm

1 is the proposed covariance computation algorithm. This algorithm outputs a pair (anc, Cov[W V fα, W V fβ]), where V = Var(anc). We cache the output for Cov[α, β] in c[α, β] once computed. e[γ] stores a pair of v = d(γ) and E[W Var(v)

fγ ]. As stated above, these can be pre-computed with a standard WMC algorithm; we defer the details to the full version. Lines 3 and 4 deal with the base cases and lines 5– 10 use Lemma 8. Lines 11–16 deal with the remaining base cases involving literals. Lines 19 and 20 use Lemma 9 and lines 21–31 use Lemma 10. To ensure that fβ can be decomposed into f ′ β ∧f ′′ β as in Lemma 10, α, β are swapped in line 18, if needed.

We must care about the variable set during the computation. For this purpose, we implement two auxiliary functions ADJEXP and ADJCOV. ADJEXP receives vnode w and e[α′], where Var(d(α′)) ⊆Var(w), and returns E[W Var(w)

fα′ ]. ADJCOV receives vnode w, the output of COV(α′, β′), e[α′], and e[β′], where Var(LCA(d(α′), d(β′))) ⊆Var(w), and returns Cov[W Var(w)

fα′, W Var(w)

fβ′ ]. Using these functions, we adjust the variable sets. With a preprocessing taking O(|V|2) time, these functions can be computed in constant time; see the full version. The correctness of Algorithm 1, i.e., that COV(α, β) returns Cov[W V fα, W V fβ], follows from the fact that cases (I), (II), and (III) are comprehensive and recursive decomposition follows Lemmas 8–10 for each case. We now move to the proof of Theorem 7.

Proof of Theorem 7. Preprocessing requires O(|V|2) time, and computing expectations takes O(|α| + |β|) time. Computing the LCA (line 2) needs O(1) time with a data structure that is built in O(|V|) time (Bender and Farach-Colton 2000). Thus, other than recursion, COV(α′, β′) requires at most O(kα′kβ′) time, where kα′, kβ′ are the number of child nodes of α′, β′. Since the answer is cached in c[α′, β′] once COV(α′, β′) is computed, the overall complexity of COV(α, β) is bounded by O(|α||β|).

We finally give a brief note on the assumption that two std-DNNFs share the same vtree in solving CVC query. Such an assumption is also imposed on some queries that take multiple st-d-DNNFs as an input (Pipatsrisawat and Darwiche 2008); e.g., sentential entailment and bounded conjunction defined in (Darwiche and Marquis 2002). Although we do not prove the tractability of CVC for the case where two st-d-DNNFs do not respect the same vtree, we believe it is intractable because st-d-DNNFs do not admit polytime sentential entailment unless P=NP when they do not share

## Algorithm

1: COV(α, β): computing Cov[Wfα, Wfβ]

Input: Two st-d-DNNFs α, β respecting the same vtree Output: Pair of anc = LCA(d(α), d(β)) and

Cov[W V fα, W V fβ] (V = Var(anc))

1 if c[α, β]̸ = null then return c[α, β] // Cache for COV(α, β)

2 anc ←LCA(d(α), d(β))

3 if α = false or β = false then return (anc, 0)

4 if α = true and β = true then return (⊥, 0)

5 if anc̸ = d(α) and anc̸ = d(β) then // Let Var(α) ⊆Var(ancl) and Var(β) ⊆Var(ancr)

6 el ←ADJEXP(ancl, e[α]) · ADJEXP(ancl, e[true])

7 er ←ADJEXP(ancr, e[true]) · ADJEXP(ancr, e[β])

8 cl ←ADJCOV(ancl, COV(α, true), e[α], e[true])

9 cr ←ADJCOV(ancr, COV(true, β), e[true], e[β])

10 r ←cl · cr + cl · er + el · cr // Eq. (4)

11 else if α, β are both leaf nodes then

12 if (α, β) = (true, x), (x, true) then r ←σ2

Px + σPxNx

13 else if (α, β)=(true, ¬x), (¬x, true) then r←σ2

Nx +σPxNx

14 else if α = β = x then r ←σ2

Px 15 else if α = β = ¬x then r ←σ2

Nx 16 else r ←σPxNx // (α, β) = (x, ¬x), (¬x, x)

17 else

18 Swap α, β if (i) anc = d(β)̸ = d(α) or (ii) d(α) = d(β) and only β is a ∨-node

19 if α is a ∨-node then // α1,..., αk: the child nodes of α

20 r←Pk j=1 ADJCOV(anc, COV(αi, β), e[αi], e[β]) // Eq. (5)

21 else // α is a ∧-node

22 αl, αr ←(child nodes of α) s.t. Var(αl) ⊆Var(ancl) and

Var(αr) ⊆Var(ancr)

23 if Var(d(β)) ⊆Var(ancl) then βl ←β, βr ←true

24 else if Var(d(β)) ⊆Var(ancr) then βl ←true, βr ←β

25 else // d(α) = d(β); thus β is a ∧-node due to line 18

26 βl, βr ←(child nodes of β) s.t. Var(βl) ⊆Var(ancl)

and Var(βr) ⊆Var(ancr)

27 el ←ADJEXP(ancl, e[αl]) · ADJEXP(ancl, e[βl])

28 er ←ADJEXP(ancr, e[αr]) · ADJEXP(ancr, e[βr])

29 cl ←ADJCOV(ancl, COV(αl, βl), e[αl], e[βl])

30 cr ←ADJCOV(ancr, COV(αr, βr), e[αr], e[βr])

31 r ←cl · cr + cl · er + el · cr // Eq. (6)

32 return c[α, β] ←(anc, r)

the vtree. Note that, for VC, such an assumption is not imposed because we have a single input st-d-DNNF for VC.

Intractability Results The goal of this section is to prove the following result.

Theorem 11. When f, g are given as st-DNNFs, d-DNNFs, or FBDDs, CVC is intractable, i.e., it cannot be solved in polynomial time unless P=NP. When f is given as an st- DNNF, a d-DNNF, or an FBDD, VC is intractable.

We prove this by first introducing some queries from the knowledge compilation map (Darwiche and Marquis 2002).

Problem 12. Given Boolean function f, model counting query CT computes the number of models of f, i.e., |AV f |. Given Boolean functions f, g, sentential entailment query SE asks whether f |= g, i.e., AV f ⊆AV g.

19316

<!-- Page 6 -->

We now show a polynomial time reduction from the CT and SE queries to the VC and CVC queries. It is known that CT is intractable when f is given as an st-DNNF (Pipatsrisawat and Darwiche 2008). It is also known that SE is intractable when f, g are given as d-DNNFs or FB- DDs (Darwiche and Marquis 2002). Thus, the existence of the above reduction indicates the intractability of VC and CVC queries with such representations.

Let n:= |V|. The key lemmas are as follows. Lemma 13. Let µPx = µNx = 1, σ2

Px = σ2

Nx = 3, and σPxNx = −1 for every variable x ∈V. Then, for any assignment a of V, V[Wa] = 4n −1. In addition, for any assignments a, b (a̸ = b) of V, Cov[Wa, Wb] = −1.

Proof. We can decompose W V a = Qa xW V\{x}

a, where Qa x = Px if a(x) = true or Qa x = Nx otherwise. Similar decomposition can be derived for W V b. Thus, by (3),

Cov[W V a, W V b ] =

(Cov[Qa x, Qb x] + E[Qa x]E[Qb x])Cov[W V\{x}

a, W V\{x}

b ]

+ Cov[Qa x, Qb x]E[W V\{v}

a ]E[W V\{x}

b ]. (7)

Here, E[Qa x] = E[Qb x] = E[W V\{x}

a ] = E[W V\{x}

b ] = 1 because µPx = µNx = 1 for any x ∈V. When a = b, (7) becomes V[W V a ] = 4V[W V\{x}

a ] + 3 because V[Qa x] = 3 regardless of whether Qa x equals Px or Nx. By applying this formula recursively for every Boolean variable x, we have V[W V a ] = 3(1 + 4 + · · · + 4n−1) = 4n −1. When a̸ = b, by letting x be a Boolean variable satisfying a(x)̸ = b(x), we have Cov[Qa x, Qb x] = Cov[Px, Nx] = −1. By substituting Cov[Qa x, Qb x] in (7), Cov[W V a, W V b ] = −1.

Lemma 14. Let f, g be Boolean functions on variable set V. Then, under identical settings of expectations and (co)variances as Lemma 13, |AV f | = ⌈V[W V f ]/(4n −1)⌉ and |AV f∧g| = ⌈Cov[W V f, W V g ]/(4n −1)⌉.

Proof. By recursively applying (2), we have

Cov[W V f, W V g ] = P a∈AV f

P b∈AV g Cov[W V a, W V b ]

= P a∈AV f ∩AV g V[W V a ]

+ P

(a,b)∈AV f ×AV g:a̸=b Cov[W V a, W V b ],

The first term is (4n −1)|AV f∧g| and the second term is −|{(a, b) ∈AV f × AV g | a̸ = b}| by Lemma 13. The latter can be lower bounded by −|{(a, b) ∈AV true × AV true | a̸ = b}| = −2n(2n −1) = −(4n −2n) > −(4n −1). Thus, we have

(4n−1)(|AV f∧g|−1) < Cov[W V f, W V g ] ≤(4n−1)|AV f∧g|, indicating |AV f∧g| = ⌈Cov[W V f, W V g ]/(4n −1)⌉. By setting g = f, we have |AV f | = ⌈V[W V f ]/(4n −1)⌉.

Lemma 14 indicates the reductions from CT to VC and from SE to CVC. Given Boolean function f, we can answer CT by computing V[Wf] under the settings of Lemma 13.

Query st-d-DNNF st-DNNF d-DNNF FBDD

VC ✓(Thm. 7) ◦(Thm. 11) ◦(Thm. 11) ◦(Thm. 11) CVC ✓∗(Thm. 7) ◦(Thm. 11) ◦(Thm. 11) ◦(Thm. 11) CT ✓ ◦ ✓ ✓ SE ✓∗ ◦ ◦ ◦ ∗Assuming that two st-d-DNNFs respect the same vtree.

**Table 1.** Tractability of queries. ✓indicates that this query can be answered in polynomial time in the sizes of NNFs, and ◦indicates that it cannot be answered in polynomial time unless P=NP.

Given Boolean functions f, g, we can answer SE as follows. We compute V[Wf] and Cov[Wf, Wg] under the settings of Lemma 13 and obtain |AV f | and |AV f∧g| by Lemma 14. Then f |= g if and only if |AV f | = |AV f∧g|. Combined with the intractability results of CT and SE, the intractability of VC for st-DNNFs and that of CVC for d-DNNFs and FBDDs follow. Note that CVC is also intractable for st-DNNFs since VC can be reduced to CVC with g = f.

The remaining is to show the intractability of VC for d- DNNFs and FBDDs. We use the following lemma.

Lemma 15. Let f, g be Boolean functions on variable set V, z /∈V be a Boolean variable, and h = (z ∧f)∨(¬z ∧g). We set µPz = µNz = 1 and σ2

Pz = σ2

Nz = −σPzNz = 3, and Nx and Px (x ∈V) have identical settings as Lemma 13. Then, Cov[W V f, W V g ] = V[W V f ] + V[W V g ] −

V[W V∪{z}

h ]/4 + 3(E[W V f ] −E[W V g ])2/4.

Proof. Since W V∪{z}

h = PzW V f + NzW V g, V[W V∪{z}

h ] = V[PzW V f ] + V[NzW V g ] +2Cov[PzW V f, NzW V g ] by (2). We have V[PzW V f ] = 4V[W V f ] + 3(E[W V f ])2, V[NzW V g ] = 4V[W V g ] + 3E[W V g ]2, and Cov[PzW V f, NzW V g ] = −2Cov[W V f, W V g ] −3E[W V f ]E[W V g ] by using (3). Substituting each term leads to the equation in Lemma 15.

Lemma 15 demonstrates that we can obtain Cov[Wf, Wg] by computing the variances of Wf,Wg, and Wh and the expectations of Wf and Wg. If f, g are given as FBDDs, we can easily construct the FBDD of h by simply adding decision node ∨at the root: (z ∧f) ∨(¬z ∧g), which does not break the restrictions of FBDDs. This construction is also valid for d-DNNFs when f, g are given as d-DNNFs. Thus, CVC can be answered by solving VC when f, g are given as d-DNNFs or FBDDs; they also admit the expectation computation because it amounts to ordinal WMC. This indicates the intractability of VC for d-DNNFs and FBDDs, proving Theorem 11. Table 1 summarizes the tractability of the queries.

Application for Bayesian Networks We introduce an application that considers the uncertainty in the inference of Bayesian networks. A discrete Bayesian network represents a joint distribution over categorical random variables X:= {X1,..., Xn}, where the range of Xi is

19317

<!-- Page 7 -->

{xi1,..., xiki}. Each random variable Xi has parents Ui ⊆ X, and the dependence structure is assumed to be acyclic. The joint probability that Xi takes value xi for i = 1,..., n is described as Pr(x1,..., xn) = Qn i=1 Pr(xi|ui), where ui:= {ui1,..., uiℓi} is the set of values of parent variables Ui. A marginal inference for a Bayesian network is to compute the marginal probability of partial assignments that are the values of some random variables.

In an ordinal setting, every conditional distribution is characterized by a set of fixed parameters. More specifically, distribution Pr(xi|ui) for given parent values ui is a Bernoulli (for a binary-valued Xi) or a categorical (for a general Xi) distribution with fixed parameters. Since these parameters are often learned from data, they may have uncertainty. As explained in the Introduction, a Bayesian statistical approach to model the uncertainty is to introduce distributions, e.g., beta or Dirichlet distributions, for the parameters and regard the marginal probability as a random variable. With our method, we can compute the variance of the marginal probability. Our main result here is as follows.

Theorem 16. Given a Bayesian network with a constant treewidth, we can compute the variance of a marginal probability in polynomial time.

This theorem can be proved by using the existing WMC encoding of Bayesian networks (Chavira and Darwiche 2008) and then compute the marginal probability’s variance by our proposed algorithm. Since the method for the general case is complicated, as it requires the slight relaxation of the independence assumption, we defer the details of the general method and the proof of Theorem 16 to the full version. Instead, we here explain a simpler method for the case where every random variable is binary-valued, i.e., ki = 2 for every Xi. We use the encoding of Sang, Bearne, and Kautz (2005), referred to as ENC2 by Chavira and Darwiche (2008).

Before incorporating uncertainty, we explain the method for ordinal marginal inference. For every random variable Xi, we prepare indicator variables λxi1, λxi2; λxij = true when Xi = xij. We set the following clauses:

λxi1 ∨λxi2, ¬λxi1 ∨¬λxi2. (8)

We also prepare parameter variable ρxi1|ui for every pattern on parent values ui and set the following clauses:

λui1 ∧· · · ∧λuiℓi ∧ρxi1|ui =⇒λxi1, λui1 ∧· · · ∧λuiℓi ∧¬ρxi1|ui =⇒λxi2. (9)

In addition, we set Pρ = 1 −Nρ = Pr(xi1|ui) for every ρ = ρxi1|ui. Let f be a Boolean function that is a conjunction of all the clauses in (8) and (9). Then the marginal probability given partial assignment x can be obtained in two ways: (i) To prepare Boolean function gx, which is a conjunction of indicator variables corresponding to x, and compute the WMC of f ∧gx with Pλ = Nλ = 1 for every λ = λij. (ii) To set Pλ = 0 for λ = λxij such that x contains xij′ (j′̸ = j), set all the other weights of the indicator variables to 1, and then compute the WMC of f. For example, when x = {x11, x32}, method (i) prepares gx = λx11∧λx32, while method (ii) sets Pλ = 0 for λ = λx12, λx31.

To incorporate uncertainty, we regard Px and Nx as random variables. Expectations µPx, µNx are set to the original weight values. Since the weights of indicator variables λ = λxij are determined regardless of the probability values, we set σ2

Pλ = σ2

Nλ = σPλNλ = 0. For parameter variables ρ = ρxi1|ui, we consider variance σ2 xi1|ui of probability parameter Pr(xi1|ui). Since Pρ + Nρ = 1, we set σ2

Pρ = σ2

Nρ = −σPρNρ = σ2 xi1|ui. By computing the variance of the WMC under this setting, we can compute the variance of the marginal. Note that we here assume that each parameter is independent of the others because (Px, Nx) and (Py, Ny) (x̸ = y) are independent, which is justified by the widely-adopted parameter independence assumption (Spiegelhalter and Lauritzen 1990) when parameters are learned from data; see also (Heckerman 2008). In the following experiments, we empirically validate the tractability of the proposed algorithm and showcase the usage of variance computation with this encoding.

We finally mention that the variance of the conditional probability of a Bayesian network can be approximately obtained by using the CVC query. The conditional probability of x given condition c equals Wh′/Wh with h′ = f ∧gx ∧gc and h = f ∧gc using method (i), i.e., to prepare Boolean function gx. Although we cannot precisely determine V[Wh′/Wh], by Taylor expansion (van Kempen and van Vliet 2000) we have V[Wh′/Wh] ≈ V[Wh′]/{E[Wh]}2 −2Cov[Wh′, Wh]E[Wh′]/{E[Wh]}3 + V[Wh]{E[Wh′]}2/{E[Wh]}4.

## Experiments

In our experiment, we first confirmed the practical tractability of the proposed algorithm for st-d-DNNFs with an application for computing the variance of the marginal of Bayesian networks. We used Bayesian networks from bn- Rep (Leonelli 2025), which collects networks from recent academic literature in various areas. We retrieved all 70 binary Bayesian networks from bnRep. The number of random variables ranges from 3 to 122. We derived the CNF of f with ENC2 by Ace v3.0 (http://reasoning.cs.ucla.edu/ace/) and compiled every CNF into a SDD, which is a subset of an st-d-DNNF, by the SDD package (Choi and Darwiche 2013). Given p = Pr(xi1|ui) in the data, we set σ2 xi1|ui = p(1 −p)/θ, which virtually considered Pr(xi1|ui) follows Beta((θ −1)p, (θ −1)(1 −p)). We set θ = 10; note that the value of θ does not affect the computational time. For parameters where p = 0 or 1, we set σ2 xi1|ui = 0 because Pr(xi1|ui) should take a value within [0, 1], and thus the variance must be 0 when the expectation is 0 or 1. We chose one random variable from a Bayesian network as a partial assignment and computed the variance of the marginal by method (ii). Note that the choices of the partial assignment and the expectations and (co)variances of weights do not affect the computational time since the size of the SDD representing f remains unchanged. The proposed method was implemented in C++ and compiled with g++-11.4.0. All experiments were performed on a single thread of a Linux server with AMD EPYC 7763 CPU and 2048 GB RAM;

19318

<!-- Page 8 -->

Name #rv |SDD| Compile (s) Variance (s)

projectmanagement 26 0.500 0.025 GDIpathway2 28 0.784 0.021 grounding 36 2.387 0.017 engines 12 0.240 0.011 windturbine 122 1.380 0.009

**Table 2.** Top-5 (out of 70) time-consuming networks. “#rv” is the number of random variables. “|SDD|” is the size of compiled SDD. “Compile” and “Variance” indicate the time required to compile SDD and compute variance.

C

Chl_a DO

N

P

Te

Tu pH

**Figure 3.** The “algalactivity2” network.

Parameter Variance

DO|pH0, Te0 0.002887 Chl a|C1, DO0, N0, Te1 0.003532 Te|P0 0.003554 pH|Te0 0.003592 Chl a|C1, DO1, N1, Te0 0.003674

(none) 0.003904

**Table 3.** Variance of Pr(Chl a = 0) when one parameter’s variance is reduced to one-tenth. Top-5 parameters in ascending order of variance was exhibited.

note that we used less than 4 GB of memory during the experiments. We reported the average consumed time for SDD compilation and variance computation over 10 runs for each network.

As a result, after the SDD was compiled, the variance computation only took 0.025 sec at maximum, recorded for “projectmanagement” network whose SDD size was 3,888. Even if the SDD compilation is added to the computational time, it took only 10 sec to process the most time-consuming “propellant” network. Table 2 shows the top-5 networks in descending order of the variance computation times. This indicates the practical tractability of the proposed algorithm. More detailed results can be found in the full version.

Next, we showcased the usage of variance computations with the “algalactivity2” network from bnRep (Fig. 3). Each random variable in Fig. 3 is valued either 0 or 1. With the same setting as the above experiment, the mean and variance of Pr(Chl a=0) are computed as 0.5281 and 0.003904. Since the standard deviation is 0.06248, the variance will affect the decision-making that depends on, e.g., whether Pr(Chl a = 0) ≤0.55. To conduct more robust decisionmaking, we want to reduce the variance of the marginal. One approach is to decrease the variance of the parameters by collecting more observations (data). However, since it is costly to collect observations corresponding to all the parameters, we want to find parameters that are effective for reducing the variance of the marginal. Thus, we additionally demonstrated how much the variance of this marginal is decreased by reducing the variance of one parameter to one-tenth. We conducted the above demonstration for each of the 43 parameters in the network. Table 3 shows the top-5 parameters in the reduction of the variance of Pr(Chl a=0). In other words, it shows the top-5 parameters having greater impact on the variance of the marginal. Here, RVj stands for RV = j; e.g., DO|pH0, Te0 denotes parameter Pr(DO|pH = 0, Te=0). It is notable that, among the 43 parameters, those having greater impact on the variance of Pr(Chl a = 0) are not only the conditional probabilities of Chl a but also those of the other random variables. We realized that reducing the variance of the parameters in Table 3 efficiently decreased the variance of the marginal. These results suggest us that we cannot reveal what parameters have greater impact on the variance of the inference result without actually computing the variance. We give more examples of the variance computation in the full version.

## Conclusion

We defined a query for computing the WMC’s variance. We proved that this query is tractable for st-d-DNNFs and intractable for st-DNNFs, d-DNNFs, and FBDDs; the tractability was shown by presenting an algorithm to solve the query. We also showed an application for quantifying the uncertainty in the inference on Bayesian networks. Future directions include the computation of more involved WMC statistics, such as higher-order moments. We should also investigate the tractability of VC and CVC queries for emerging classes of representations, such as and-sum circuits (Onaka et al. 2025).

## References

Bender, M. A.; and Farach-Colton, M. 2000. The LCA problem revisited. In Proc. of the 4th Latin American Symposium on Theoretical Informatics (LATIN’00), 88–94.

Bryant, R. E. 1986. Graph-based algorithms for Boolean function manipulation. IEEE Transactions on Computers, C-35(8): 677–691.

Chavira, M.; and Darwiche, A. 2008. On probabilistic inference by weighted model counting. Artificial Intelligence, 172(6–7): 772–799.

Choi, A.; and Darwiche, A. 2013. Dynamic minimization of sentential decision diagrams. In Proc. of the 27th AAAI Conference on Artificial Intelligence (AAAI’13), 187–194.

Choi, A.; Kisa, D.; and Darwiche, A. 2013. Compiling probabilistic graphical models using sentential decision diagrams. In Proc. of the 12th European Conference on Symbolic and Quantiative Approaches to Resoning with Uncertainty (ECSQARU’13), 121–132.

Choi, Y.; Vergari, A.; and Van den Broeck, G. 2020. Probabilistic circuits: A unifying framework for tractable probabilistic models. Technical report, UCLA.

Cozman, F. G. 2000. Credal networks. Artificial Intelligence, 120(2): 199–233.

Darwiche, A. 2001. On the tractable counting of theory models and its application to truth maintenance and belief revision. Journal of Applied Non-Classical Logics, 11(1-2): 11–34.

19319

<!-- Page 9 -->

Darwiche, A. 2011. SDD: A new canonical representation of propositional knowledge bases. In Proc. of the 22nd international Joint Conference on Artifical Intelligence (IJCAI’11), 819–826. Darwiche, A.; and Marquis, P. 2002. A knowledge compilation map. Journal of Artificial Intelligence Research, 17(1): 229–264. De Campos, C. P.; and Cozman, F. G. 2005. The inferential complexity of Bayesian and credal networks. In Proc. of the 19th International Joint Conference on Artificial Intelligence (IJCAI’05), 1313–1318. Dilkas, P.; and Belle, V. 2021. Weighted model counting with conditional weights for Bayesian networks. In Proc. of the 37th Conference on Uncertainty in Artificial Intelligence (UAI’21), 386–396. Duenas-Osorio, L.; Meel, K. S.; Paredes, R.; and Vardi, M. Y. 2017. Counting-based reliability estimation for power-transmission grids. In Proc. of the 31st AAAI Conference on Artificial Intelligence (AAAI’17), 4488–4494. Fierens, D.; Van den Broeck, G.; Thon, I.; Gutmann, B.; and Raedt, L. D. 2011. Inference in probabilistic logic programs using weighted CNF’s. In Proc. of the 27th Conference on Uncertainty in Artificial Intelligence (UAI’11), 211–220. Gergov, J.; and Meinel, C. 1994. Efficient Boolean manipulation with OBDD’s can be extended to FBDD’s. IEEE Transactions on Computers, 43(10): 1197–1209. Hardy, G.; Lucet, C.; and Limnios, N. 2007. K-terminal network reliability measures with binary decision diagrams. IEEE Transactions on Reliability, 56(3): 506–515. Heckerman, D. 2008. A Tutorial on Learning with Bayesian Networks, 33–82. Springer Berlin Heidelberg. Holtzen, S.; Van den Broeck, G.; and Millstein, T. 2020. Scaling exact inference for discrete probabilistic programs. Proc. of the ACM on Programming Languages, 4(OOP- SLA): 1–31. Illner, P. 2025. New compilation languages based on restricted weak decomposability. In Proc. of the 39th AAAI Conference on Artificial Intelligence (AAAI’25), 14987– 14996. Kiesel, R.; Totis, P.; and Kimmig, A. 2022. Efficient knowledge compilation beyond weighted model counting. Theory and Practice of Logic Programming, 22(4): 505–522. Leonelli, M. 2025. bnRep: A repository of Bayesian networks from the academic literature. Neurocomputing, 624: 129502. Nakamura, K.; Inoue, T.; Nishino, M.; and Yasuda, N. 2022. Impact of link availability uncertainty on network reliability: analyses with variances. In Proc. of the 2022 IEEE International Conference on Communications (ICC’22), 2713– 2719. Onaka, R.; Nakamura, K.; Nishino, M.; and Yasuda, N. 2025. An and-sum circuit with signed edges that is more succinct than SDD. In Proc. of the 39th AAAI Conference on Artificial Intelligence (AAAI’25), 15100–15108. Pipatsrisawat, K.; and Darwiche, A. 2008. New compilation languages based on structured decomposability. In Proc.

of the 23rd National Conference on Artificial Intelligence (AAAI’08), 517–522. Sang, T.; Bearne, P.; and Kautz, H. 2005. Performing Bayesian inference by weighted model counting. In Proc. of the 20th National Conference on Artificial Intelligence (AAAI’05), 475–481. Spiegelhalter, D. J.; and Lauritzen, S. L. 1990. Sequential updating of conditional probabilities on directed graphical structures. Networks, 20(5): 579–605. van Kempen, G.; and van Vliet, L. 2000. Mean and variance of ratio estimators used in fluorescence ratio imaging. Cytometry Part A - The Journal of Quantitative Cell Science, 39(4): 300–305. Wang, B.; Mau´a, D. D.; den Broeck, G. V.; and Choi, Y. 2024. A compositional atlas for algebraic circuits. In Proc. of the 38th Annual Conference on Neural Information Processing Systems (NeurIPS’24). Yu, Z.; Trapp, M.; and Kersting, K. 2023. Characteristic circuits. In Proc. of the 37th Annual Conference on Neural Information Processing Systems (NeurIPS’23). Zhang, H.; Juba, B.; and Van den Broeck, G. 2021. Probabilistic generating circuits. In Proc. of the 38th International Conference on Machine Learning (ICML’21), 12447– 12457.

19320
