---
title: "Differentially Private Linear Programming: Reduced Sub-Optimality and Guaranteed Constraint Satisfaction"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39051
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39051/43013
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Differentially Private Linear Programming: Reduced Sub-Optimality and Guaranteed Constraint Satisfaction

<!-- Page 1 -->

Differentially Private Linear Programming: Reduced Sub-Optimality and Guaranteed Constraint Satisfaction

Alexander Benvenuti1, Brendan Bialy2, Miriam Dennis2, Matthew Hale1

1School of Electrical and Computer Engineering, Georgia Institute of Technology, Atlanta, GA, USA 2Munitions Directorate, Air Force Research Laboratory, Eglin Air Force Base, FL, USA abenvenuti3@gatech.edu, brendan.bialy@us.af.mil, miriam.dennis.1@us.af.mil, mhale30@gatech.edu

## Abstract

Linear programming is a fundamental tool in a wide range of decision systems. However, without privacy protections, sharing the solution to a linear program may reveal information about the underlying data used to formulate it, which may be sensitive. Therefore, in this paper we introduce an approach for protecting sensitive data while formulating and solving a linear program. First, we prove that this method perturbs objectives and constraints in a way that makes them differentially private. Then, we show that (i) privatized problems always have solutions, and (ii) their solutions satisfy the constraints in their corresponding original, non-private problems. The latter result solves an open problem in the literature. Next, we analytically bound the expected sub-optimality of solutions that is induced by privacy. Numerical simulations show that, under a typical privacy setup, the solution produced by our method yields a 65% reduction in suboptimality compared to the state of the art.

Technical Appendix — https://arxiv.org/abs/2501.19315

## Introduction

Linear programming is used in a wide range of settings, including resource allocation, power systems, and transportation systems. In many modern systems, user data plays an increasing role in formulating such optimization problems. Sensitive information such as investor data, home power consumption, and travel routes may be use used to formulate these problems (Markowitz 1952; Stott, Marinho, and Alsac 1979), though sharing the solution to an optimization problem may leak this sensitive data (Hsu et al. 2014b). As a result, interest has arisen in solving linear programs while both (i) preserving the privacy of the data used in the problem formulation and (ii) ensuring constraint satisfaction.

In this paper we solve the open problem posed in (Munoz et al. 2021), namely, the privatization of data that is used to generate constraints when solving linear programs, while also maintaining feasibility of solutions with respect to the original, non-private constraints. For a problem with linear constraints Ax ≤b and cost cT x, the work in (Munoz et al. 2021) privatized the data that is used to generate b while also ensuring feasibility with respect to the original constraints.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Then (Munoz et al. 2021) named it as an open problem to simultaneously privatize the data that produces A and ensure satisfaction of the original, non-private constraints. We not only solve this open problem, but in fact go one step further by simultaneously privatizing the data that produces all three — A, b, and c — with guaranteed satisfaction of the original constraints.

To produce a private linear program, we use differential privacy. Differential privacy is a statistical notion of privacy originally developed to protect entries in databases (Dwork et al. 2006), and it has seen wide use in the controls (Le Ny and Pappas 2013; Cort´es et al. 2016; Hawkins and Hale 2020; Yazdani et al. 2022), planning (Chen et al. 2023; Benvenuti et al. 2024b), and federated learning (Geyer, Klein, and Nabi 2017; Agarwal, Kairouz, and Liu 2021; Chen et al. 2022; Noble, Bellet, and Dieuleveut 2022) communities for the strong guarantees that it provides.

We use differential privacy in this work partly because of its immunity to post-processing (Dwork and Roth 2014), namely that arbitrary computations on private data do not weaken differential privacy. We consider linear programs in which the cost cT x and constraint terms A and b can all depend on user data, and we use differential privacy to perturb each of these terms in order to protect the data that is used to generate them. The result is a privacy-preserving linear program. We then solve this optimization problem, which is simply a way of post-processing the privacy-preserving problem. Thus, the solution to the private problem preserves the privacy of the data used to formulate the problem, as do any downstream computations that use that solution.

As noted in (Benvenuti et al. 2024a) and (Munoz et al. 2021), common privacy mechanisms such as the Gaussian and Laplace mechanisms (Dwork and Roth 2014) add noise with unbounded support. Such mechanisms can perturb constraints by arbitrarily large amounts, which can therefore cause the solution to a privatized problem to be infeasible with respect to the original constraints. Motivated by this challenge, we develop a new matrix truncated Laplace mechanism to privatize the data that produces A, and we use the truncated Laplace mechanism developed in (Munoz et al. 2021; Geng et al. 2020) to privatize the data that produces b. This approach allows us to privatize the constraints such that they only become tighter, thereby ensuring that the solution to the private problem always satisfies the original, non-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19702

<!-- Page 2 -->

(Hsu et al. 2014b) (Cummings et al. 2015) (Dvorkin et al. 2020) (Munoz et al. 2021) (Benvenuti et al. 2024a) This work Privatize A ✓ ✓ ✓ ✓ Privatize b ✓ ✓ ✓ ✓ ✓ Privatize c ✓ ✓ ✓ Satisfy Constraints ✓ ✓ ✓

**Table 1.** Comparison of differentially private linear programming approaches in the literature.

private constraints. Since the cost does not affect feasibility, we use the unbounded Laplace mechanism in (Dwork and Roth 2014) to provide privacy for the cost. We then bound the accuracy of our method, which provides users with a tool to calibrate privacy based on its tradeoff with performance. To summarize, our contributions are:

• We develop a differential privacy mechanism that simultaneously privatizes all terms in a linear program (Theorem 3.9).

• We prove that a privatized problem produces a solution that is feasible with respect the constraints in the original, non-private problem (Theorem 3.10), which solves an open problem in the literature.

• We bound the accuracy of our method, namely the increase/decrease in optimal cost, in terms of privacy parameters (Theorem 4.1).

• We empirically compare the performance of our method to the state of the art and show that the solution produced by our method yields a 65% reduction in sub-optimality relative to existing work (Section 5).

## 1.1 Related Work

There exists substantial previous work on differential privacy in optimization, specifically looking at privacy for objective functions in distributed optimization (Huang, Mitra, and Vaidya 2015; Wang et al. 2016; Han, Topcu, and Pappas 2016; Nozari, Tallapragada, and Cort´es 2016; Dobbe et al. 2018; Lv, Yang, and Shi 2020). We differ from these works because we consider the constraints to also be sensitive, not just objectives. Privacy for optimization with linear constraints has been previously investigated in (Hsu et al. 2014b; Cummings et al. 2015; Dvorkin et al. 2020; Munoz et al. 2021; Benvenuti et al. 2024a; Kaplan et al. 2024). Both (Hsu et al. 2014b) and (Cummings et al. 2015) consider differential privacy for both the costs and constraints, but they allow for constraints to be violated, which is unacceptable in many applications, e.g., if constraints encode safety. The authors in (Dvorkin et al. 2020) analyze privacy for the constant vector in equality constraints by reformulating their optimization problem as a stochastic chanceconstrained optimization problem. The authors in (Kaplan et al. 2024) consider privacy for all the constraints with a focus on maximizing the number of constraints satisfied. However, both of these works still allow for constraint violation. Both (Munoz et al. 2021) and (Benvenuti et al. 2024a) address the problem of privately solving convex optimization problems with linear constraints with guaranteed constraint satisfaction, but (Munoz et al. 2021) only privatizes b and (Benvenuti et al. 2024a) only privatizes A. We differ because we consider privacy for all components of an LP simultaneously. Moreover, (Benvenuti et al. 2024a) privatizes the entries of A themselves, though here we consider the more general setting of allowing A and b to be functions of user data, and we privatize that user data, not the entries of A and b. Table 1 summarizes our place in the literature.

## 1.2 Notation

For N ∈N, we use [N]:= {1, 2,..., N}. We use | · | to denote the cardinality of a set and A ⊖B to denote the symmetric difference between two sets A and B. We use E [X] to denote the expectation of a random variable X and L(σ) to be a zero-mean Laplace distribution with scale parameter σ. We use Mi,j to denote the ithjth entry of a matrix. Additionally, we use ∥M∥1,1 = Pm i=1

Pn j=1 |Mi,j| to denote the (1, 1)-norm of a matrix. We use 1m×n to be an m × n matrix of all ones and [−s1m×n, s1m×n] to be an mn-fold Cartesian product of the interval [−s, s]. We use A ◦B as the Hadamard product between matrices A and B. We write diam(S) = sups1,s2∈S ∥s1 −s2∥2 for the diameter of a set S.

## Preliminaries

and Problem Formulation 2.1 Linear Programming We consider linear programs (LPs) formed from a database D ∈D taking the form maximize x c(D)T x subject to A(D)x ≤b(D), x ≥0,

(P)

where D is the set of all possible realizations of the database D, c(D) ∈Rn is the “cost vector”, A(D) ∈Rm×n is the “constraint coefficient matrix”, and b(D) ∈Rm is the “constraint vector”. We also use the sets A to denote the set of all realizations of A(D) and B and b(D) for all D ∈D. We define the feasible region of the LP for a database realization D as

F(D) = {x ∈Rn: A(D)x ≤b(D)}. (1)

Remark 2.1. We include the constraint x ≥0 without loss of generality since the constraints in a problem may be reformulated to shift the feasible region to the non-negative orthant without changing the problem. We do this because having strictly positive decision variables allows us have insight into how the feasible region changes when perturbing the constraints, which plays a key role in our feasibility analysis in Section 3.

Assumption 2.2. For every D ∈D, Problem (P) satisfies Slater’s condition.

19703

<!-- Page 3 -->

Remark 2.3. Assumption 2.2 is common in the optimization literature. Slater’s condition says that for the constraints Ax ≤b there exists a point ¯x such that A¯x −b < 0, and thus Assumption 2.2 states that such a point must exist for each realization of the database D. Satisfying Slater’s condition implies that the feasible region F(D) defined by (1) has non-empty interior for all D ∈D. If F(D) has empty interior, then any perturbation to the constraints can produce a private problem whose solution is automatically infeasible with respect to the original, non-private constraints. Thus, such constraints are fundamentally incompatible with privacy. We enforce Assumption 2.2 in order to only consider problems where it is at least possible to attain both privacy and feasibility simultaneously, though we still must determine how to do so.

Assumption 2.4. The set D is bounded and the bounds are publicly available.

Assumption 2.4 is quite mild since user data may represent physical quantities that do not exceed certain bounds, e.g., with voltages in a power grid, and these can be publicly known without revealing any sensitive user data.

Problem (P) admits an equivalent dual problem of the form minimize µ µT b(D)

subject to µT A(D) ≤c(D)T, µ ≥0.

## 2.2 Differential Privacy

We will provide differential privacy to a database D by perturbing each component of the LP that it produces, namely A(D), b(D), and c(D). The goal of differential privacy is to make “similar” pieces of data appear approximately indistinguishable, and the notion of “similar” is defined by an adjacency relation (Dwork and Roth 2014).

Definition 2.5 (Adjacency). Two databases D and D′ are said to be “adjacent” if they differ in at most one entry. If two databases D and D′ are adjacent, we say Adj(D, D′) = 1; otherwise we write Adj(D, D′) = 0.

To make adjacent pieces of data appear approximately indistinguishable, we implement differential privacy, which is done using a randomized map called a “mechanism”. In its general form, differential privacy protects a sensitive piece of data y by randomizing some function of it, say f(y). In the case of linear programming, we privatize three functions of the sensitive data D, namely A(D), b(D), and c(D).

Definition 2.6 (Differential Privacy; (Dwork and Roth 2014)). Fix a probability space (Ω, F, P). Let ϵ > 0 and δ ∈ [0, 1

2) be given. A mechanism M: Rm×n × Ω→Rm×n is (ϵ, δ)-differentially private if for all V (D), W(D) ∈Rm×n that are adjacent in the sense of Definition 2.5, we have P[M (V) ∈T] ≤eϵP[M (W) ∈T] + δ for all Borel measurable sets T ⊆Rm×n.

Since all three components of Problem (P) require privacy, next we state a lemma on how composing private mechanisms affects privacy.

Lemma 2.7 (Sequential Composition of Private Mechanisms (Dwork and Roth 2014)). For i ∈[N], fix αi ≥ 0 such that PN i=1 αi = 1. Let Mi: D → Ri for i ∈[N] be an (αiϵ, αiδ)-differentially private mechanism. If M[N]: D →QN i=1 Ri is defined to be M[N](D) = (M1(D),..., MN(D)) then M[N] is (ϵ, δ)-differentially private.

We refer to the αi’s as the “privacy budget allocation”, since they divide ϵ and δ among the privacy mechanisms. Lemma 2.7 implies that an algorithm containing individual privatizations of A(D), b(D), and c(D) is itself differentially private with parameters equal to the sum of the privacy parameters from each individual privatization. This property allows us to form a linear program composed of each privatized quantity and ensure that forming that program is differentially private. Next we state a lemma that solving such an optimization problem also preserves the privacy of the underlying database D. Lemma 2.8 (Immunity to Post-Processing; (Dwork and Roth 2014)). Let M: Rm×n × Ω→Rm×n be an (ϵ, δ)differentially private mechanism. Let h: Rm×n →Rp×q be an arbitrary mapping. Then the composition h ◦M: Rm×n →Rp×q is (ϵ, δ)-differentially private.

Since solving an optimization problem is a form of postprocessing, Lemma 2.8 implies that the solution to an (ϵ, δ)differentially private optimization problem is also (ϵ, δ)differentially private, allowing the solution to a privatized form of Problem (P) to be shared without harming the privacy of D.

## 2.3 Problem Statements Consider

Problem (P). Computing x∗without any protections depends on the underlying sensitive database D, and thus computing and using x∗can reveal information about D. Therefore, we seek to develop a framework for solving problems in the form of Problem (P) that preserves the privacy of D while still satisfying the constraints in Problem (P). This will be done by solving the following problems. Problem 1. Develop a privacy mechanism to privatize D when computing each component of a linear program (namely, A(D), b(D), and c(D)). Problem 2. Prove that a solution to the privately generated optimization problem also satisfies the constraints of the original, non-private problem. Problem 3. Bound the sub-optimality in solutions that is induced by the privacy mechanism in terms of the privacy parameters ϵ and δ.

Private Constraints In this section, we solve Problems 1 and 2. Specifically, we perturb the matrix A(D), the vector b(D), and the vector c(D) in order to privatize D. Since A(D), b(D), and c(D) all have different properties and requirements to preserve feasibility, we use separate privacy mechanisms for each. We begin with privacy for the matrix A(D). The

19704

<!-- Page 4 -->

proofs for all new technical results may be found in the Technical Appendix Section B.

## 3.1 Privacy for A(D)

Definition 3.1. The L1,1-sensitivity of a function f: D → Rm×n is

∆1,1f = sup D,D′:Adj(D,D′)=1

∥f(D) −f(D′)∥1,1.

Next, we extend the definition of the Truncated Laplace Distribution in (Munoz et al. 2021) to matrix-valued draws. Lemma 3.2 (Matrix-Variate Truncated Laplace Mechanism). Let privacy parameters ϵ > 0 and δ ∈(0, 1

2] and sensitivity ∆1,1A be given. The Matrix-Variate Truncated Laplace Mechanism takes a matrix-valued function of sensitive data F(y) ∈Rm×n as input and outputs the private approximation of F(y), denoted ˜F(y) = F(y) + Z ∈ Rm×n, where Zi,j ∼LT (σA, SA) for all i ∈[m] and j ∈ [n]. Here, LT (σA, SA) is the scalar truncated Laplace distribution with density f(Zi,j) = 1 ζ exp

−1 σA |Zi,j|

, where SA:= [−sA, sA] and the values of sA and −sA are bounds on the private outputs such that Zi,j ∈SA. We define ζ = P(Zi,j ≤|sA|), and σA is the scale parameter of the distribution. The Matrix-Variate Truncated Laplace Mechanism is (ϵ, δ)-differentially private if σA ≥∆1,1A ϵ and sA = ∆1,1A ϵ log mn(exp(ϵ)−1)

δ + 1

.

We apply Lemma 3.2 to the entire constraint matrix A(D) to produce a differentially private constraint matrix ¯A. If some entry A(D)i,j is identically zero for all D ∈D, then that zero entry may represent that there is no physical relationship between a decision variable and a constraint. For example, in a smart power grid system, one home’s power consumption may not influence its neighbor’s power consumption. Given their practical relevance, we wish to preserve such properties when privacy is implemented. To ensure that identically zero-valued entries in A(D) (which we refer to as “non-sensitive” entries) remain unchanged by privacy, we set

¯A = A(D) + (sA1m×n + Z) ◦I {A(D)̸ = 0}, (2)

where I {A(D)̸ = 0} ∈Rm×n is a matrix of ones and zeros where I {A(D)̸ = 0}i,j = 1 if there exists some D ∈ D such that A(D)i,j̸ = 0 and I {A(D)̸ = 0}i,j = 0 if A(D)i,j = 0 for all D ∈D. We add sA1m×n in (2) to ensure that the coefficients in ¯A can only become larger than they were in A(D), thus tightening the constraints to promote feasibility of private solutions with respect to the original, non-private constraints.

## 3.2 Privacy for b(D)

To enforce privacy for b(D), we leverage the approach used in (Munoz et al. 2021), which we restate here for completeness. We begin by defining the sensitivity of a vector-valued function. Definition 3.3. The ℓ1-sensitivity of a function f: D → Rm is ∆1f = supD,D′:Adj(D,D′)=1 ∥f(D) −f(D′)∥1.

We use the multivariate Truncated Laplace Mechanism to enforce privacy for the constraint vector b(D). Lemma 3.4 (Multivariate Truncated Laplace Mechanism (Munoz et al. 2021; Geng et al. 2020)). Let privacy parameters ϵ > 0 and δ ∈(0, 1

2] and sensitivity ∆1b be given. The Truncated Laplace Mechanism takes a function of sensitive data f(y) ∈Rm as input and outputs a private approximation of f(y), denoted ˜f(y) = f(y) + z ∈Rm, where zi ∈Sb, with Sb:= [−sb, sb], and zi ∼LT (σb, Sb) for all i ∈[m]. The multivariate truncated Laplace mechanism is (ϵ, δ)-differentially private if σb ≥∆1b ϵ and sb =

∆1b ϵ log m(exp(ϵ)−1)

δ + 1

.

We apply Lemma 3.4 to b(D) to obtain

¯b = b(D) −sb1m + zb (3)

as the privatized constraint vector, where zb is the noise added to enforce privacy from Lemma 3.4. By subtracting sb1m, we ensure that each entry in the constraint vector becomes smaller, thereby tightening each constraint to promote feasibility.

## 3.3 Privacy for c(D) To enforce privacy for c(D), we use the standard

Laplace mechanism, which we define next. Lemma 3.5 (Laplace Mechanism; (Dwork and Roth 2014)). Let ∆1f > 0 and ϵ > 0 be given, and fix the adjacency relation from Definition 2.5. The Laplace mechanism takes sensitive data f(y) ∈Rn as input and outputs private data

˜f(y) = f(y)+z, where z ∼L(σ). The Laplace mechanism is (ϵ, 0)-differentially private if σ ≥∆1f ϵ. Similar to the identically zero entries of A(D), an identically zero, or non-sensitive zero, entry in c(D) encodes the fact that a decision variable does not impact the cost, and thus to preserve that structure we privatize only the nonsensitive zero elements in c(D). Let c(D)0 denote the vector of sensitive entries of c(D). To produce a private cost function, we compute ˜c0 = c(D)0 + zc, where zc ∼L(σc) is the noise added using Lemma 3.5 to enforce privacy. We then form ˜c by replacing the sensitive entries in c(D) with the corresponding private entries of ˜c0. Since changing the cost function does not impact feasibility, ˜c0 requires no postprocessing and may be used as-is.

## 3.4 Guaranteeing Feasibility

Along with privacy, we must also enforce feasibility. In order for the privately obtained solution ˜x∗to satisfy the constraints of the non-private problem (namely Problem (P)), it is clear that the two problems must have at least one feasible point in common. Ensuring that this is always true thus leads to the following assumption. Assumption 3.6 (Perturbed Feasibility). The set S = T

D⊆D {x: A(D)x ≤b(D)} is not empty.

In words, Assumption 3.6 says that there must exist at least one point that satisfies the constraints produced by every realization of the database D. With Assumption 3.6, we

19705

<!-- Page 5 -->

## Algorithm

1: Privately Solving Linear Programs

1: Inputs: Problem (P), ϵ, δ, ∆1,1A, ∆1b, ∆1c, αA, αb,αc 2: Outputs: Privacy-preserving solution ˜x∗

3: Set σA = ∆1,1A αAϵ 4: Set σb = ∆1b αbϵ 5: Set σc = ∆1c αcϵ 6: Compute the support for the constraint coefficient matrix sA = ∆1,1A αAϵ log

2nm(exp(αAϵ)−1) δ + 1

7: Compute the support for the constraint vector sb =

∆1b αbϵ log

2m(exp(αbϵ)−1) δ + 1

8: Generate ¯A using (2) 9: Generate ¯b using (3) 10: Post-process ¯A using (4) 11: Post-process ¯b using (5) 12: Compute ˜c0 = c(D)0 + zc 13: Form ˜c by replacing each non-zero entry in c with its corresponding entry of ˜c0

14: Solve Problem (DP-P) (via any algorithm) to find ˜x∗ post-process ¯A from (2) and ¯b from (3) according to

˜Ai,j = min n

¯Ai,j, sup

D∈D

A(D)i,j o for all i∈[m],j ∈[n] (4)

and

˜bi = max n

¯bi, inf

D∈D b(D)i o for all i ∈[m]. (5)

For ˜Ai,j, we do so for each (i, j) such that Ai,j is non-zero. For ˜bi, we do so for all i. The outputs of these computations are the private constraint coefficient matrix ˜A and private constraint vector ˜b. Remark 3.7. Taking the minimum in (4) ensures that each entry in ˜A appears in some A ∈A and taking the maximum in (5) ensures that each entry in ˜b appears in some b ∈B. The supremum and infumum are finite since D is bounded, and computing them maintains privacy since D does not depend on sensitive information according to Assumption 2.4.

With this privacy implementation, we will solve the optimization problem maximize x ˜cT x subject to ˜Ax ≤˜b, x ≥0.

(DP-P)

## Algorithm

1 provides a unified overview of our approach. Note that Problem (DP-P) may be solved via any algorithm, and thus Algorithm 1 does not introduce any additional computational complexity compared to solving Problem (P). Remark 3.8. Algorithm 1 presents our approach in the case where every component of the LP depends on the sensitive database; however, one can amend Algorithm 1 if only a subset of these components depends on the sensitive database. For example, if only A(D) and c(D) depend on the database, and the constraint vector b does not, then one can omit steps 4, 7, 9, and 11 from Algorithm 1, and choose αA > 0 and αc > 0 such that αA + αc = 1. Doing so will yield a more accurate result while still guaranteeing privacy for the database-dependent quantities.

## 3.5 Characterizing Privacy

Next we prove that Algorithm 1 is differentially private.

Theorem 3.9 (Solution to Problem 1). Let privacy parameters ϵ > 0 and δ ∈(0, 1

2], sensitivities ∆1,1A, ∆1b, and ∆1c, and privacy budget allocations αi for i ∈{A, b, c} be given. Let Assumptions 2.2, 2.4, and 3.6 hold. Then Algorithm 1 keeps the database D (ϵ, δ)-differentially private.

Theorem 3.9 allows us to privatize each component of the linear program individually to generate an overall (ϵ, δ)differentially private LP. The solution generated by solving (DP-P) then can be shared without harming privacy.

Theorem 3.10 (Solution to Problem 2). Let privacy parameters ϵ > 0 and δ ∈[0, 1

2) be given, and let Assumptions 2.2, 2.4, and 3.6 hold. Then Problem (DP-P) is guaranteed to have a solution, and that solution is guaranteed to satisfy the original, non-privatized constraints in Problem (P).

Theorem 3.10 guarantees that Algorithm 1 produces a feasible LP. Since all of the constraints are tightened by privacy, and the solution to Problem (DP-P) always exists, that solution is guaranteed to satisfy the original, non-private constraints. The conclusion of (Munoz et al. 2021) identifies the privatization of A(D) with guaranteed constraint satisfaction as an open problem, and thus Theorems 3.9 and 3.10 not only solve this open problem but present, to the best of the authors’ knowledge, the only private linear programming approach which can simultaneously privatize A(D) and b(D) while guaranteeing satisfaction of the original, non-private constraints.

## 4 Accuracy

In this section, we solve Problem 3 and bound the expected sub-optimality that is induced by privacy. This bound depends on (i) the largest feasible solution and the largest possible norm of a dual variable, whether it is a solution or not, (ii) the realization of the LP components at the boundary of D, and (iii) the “closeness” of the private and non-private optimization problems in a way that we make precise.

For (i) and (ii), we define the following quantities:

χ = max D∈D,j∈[N] ¯x(D)∗ j

Λ = max

D∈D c(D)T η −c(D)T ω min j∈[m] −A(D)jη + b(D)j

ˆA = sup D∈D

A(D)i,j i∈[m],j∈[n]

ˆb = sup D∈D b(D)i i∈[m]

,

19706

<!-- Page 6 -->

ρ =

              

             

2m

∆1b αbϵ

2

+ ms2 b + 2sbχ Pm i=1 n0 i sA

+ Λ2

2

∆1b αbϵ

2

+ s2 b

+ χ2 Pm i=1

2n0 i

∆1,1A αAϵ

2

+ (n0 i sA)2

+ 2n0,c

∆1c αcϵ

2

+ mΛ2 Pn j=1

2m0 j

∆1,1A αAϵ

2

+ (m0 jsA)2

+ 2χ2n0,c

∆1c αcϵ

2 1

2 if ˜Ai,j = A(D)i,j + (sA + Zi,j)I {A̸ = 0}i,j and ˜bi = b(D)i −sb + zbi for all i, j





√n∥(A(D) −ˆA)∥F χ √m∥(A(D) −ˆA)T ∥F Λ

2√n ∆1c αcϵ χ





2

+





∥(b(D) −ˆb)∥2

2 ∆1c αcϵ √m∥b(D) −ˆb∥2Λ





2 otherwise

(6)

where η is a solution to Problem (P) and ω is a Slater point for Problem (P). For (iii), we use Corollary 3.1 from (Robinson 1973), which we state formally in the Technical Appendix, Section A as Lemma A.1. Lemma A.1 then forms the basis for our accuracy result, which we state next.

Theorem 4.1 (Solution to Problem 3). Fix privacy parameters ϵ > 0 and δ ∈[0, 1

2), and let the sensitivities ∆1,1A, ∆1b, and ∆1c, and privacy budget allocations αi for i ∈{A, b, c} be given. Let Assumptions 2.2, 2.4, and 3.6 hold. Let x∗be the solution to Problem (P) and let ˜x∗be the solution to Problem (DP-P). Let H(G, C) be the Hoffman constant, as defined in (Robinson 1973), associated with Problem (P). Then E c(D)T x∗−c(D)T ˜x∗

≤ ∥c(D)∥2 H(G, C)ρ, where ρ is defined in (6).

Remark 4.2. Given an LP in the form of Problem (P), the Hoffman constant H(G, C) is well-defined and always exists. Computing exact Hoffman constants is known to be NP-Hard (Pena, Vera, and Zuluaga 2018), though a variety of upper bounds and efficient approximation algorithms for them exist, and any one of them can be used in conjunction with Theorem 4.1. A full exposition is beyond the scope of this article, and we refer the reader to (Pena, Vera, and Zuluaga 2018, 2021; Hoffman 1952) and references therein for an extended discussion.

The accuracy guarantee of Theorem 4.1 enables users to trade off the worst-case average sub-optimality induced by privacy in order to design the parameters ϵ and δ. Additionally, we find that the order of ρ is O(log(1 δ)ϵ−1

2) in terms of the privacy parameters and O(nm) in terms of the problem parameters, which implies linear growth of the error in terms of the privacy parameters in the worst case. However, in practice, we find virtually no increase in error with increasing problem size, which is shown empirically in Section 5. Next, we bound the magnitude of the fluctuations around the mean.

Theorem 4.3. Let the conditions of Theorem 4.1 hold. Let R = ∥x∗−˜x∗∥2. Then,

P

R −E [R] ≥diam(F(D))

p log(1/t)/2

≥1 −t.

Theorem 4.3 indicates that the fluctuations of the error about the mean error depends on the size of the original, non-private feasible region.

## 5 Numerical Simulation

In this section, we present simulations on the internet advertising setting described in (Munoz et al. 2021), which we restate here for completeness. See Technical Appendix C.2 for additional simulations. In this setting, the pages of a website are partitioned into N groups, and group i ∈[N] receives ni unique visitors. The database D is the confidential business information from advertisers, such as market research on the products being advertised. For a group of M advertisers, for each j ∈[M], advertiser j lists a price pij(D) that they are willing to pay per unique visit, and a budget b(D)j that that they are willing to spend on advertising. This setting yields the optimization problem maximize x≥0

X i∈[N]

X j∈[M]

pij(D)xij subject to

X j∈[M]

xij ≤ni for i ∈[N]

X i∈[N]

pij(D)xij ≤b(D)j for j ∈[M].

We consider two scenarios: (i) where only pij(D) requires privacy for all i, j and (ii) where both pij(D) and b(D) require privacy. For both scenarios, αi = 1/3 for all i. See Technical Appendix C.1 for results with varying αi.

For case (i), we utilize Algorithm 1 modified in the manner detailed in Remark 3.8 to provide privacy for just pij(D), and we compare the quality of the solution (i.e., the loss in revenue) and the fraction of the constraints violated (i.e., how often advertisers go over budget) to that of (Hsu et al. 2014b). We note that (Hsu et al. 2014b) has known issues with privacy leakages, as pointed out in (Munoz et al. 2021). Specifically, (Hsu et al. 2014b) recommends scaling the problem by the ℓ1 norm of the optimal solution, though doing so will alter the sensitivity of the problem, and no analysis is provided on how to compute the scaled problem’s sensitivity. Additionally, the multiplicative weights algorithm used by (Hsu et al. 2014a) in problems with private constraints, such as in their Algorithm 5, may fail to converge in practice when noise draws with strong privacy are too large. Knowing these issues, (Hsu et al. 2014b) still presents the closest work to ours.

In case (i), we analyze sub-optimality, E

(c(D)T x∗−c(D)T ˜x∗)/(c(D)T x∗)

under varying levels of privacy. We set N = 10 and M = 5. Each pij(D)

19707

<!-- Page 7 -->

0.5 1 1.5 2

0% 20% 40% 60% 80%

Privacy Strength, ϵ

Sub-Optimality

Remark 3.8 (Case (i)) Algorithm 1 (Case (ii)) (Hsu et al. 2014b) (Munoz et al. 2021)

**Figure 1.** Performance loss with varying privacy strength. Combining Algorithm 5 with a privatized objective from (Hsu et al. 2014b) leads to constraint violation for all ϵ ∈[0.25, 2]. High constraint violation allows the solution to give the appearance of superior performance; however, such a solution leads to significant violation of some advertisers’ budgets, which is unacceptable. Even when allowing this constraint violation, the solution produced by (Hsu et al. 2014b) still yields worse performance than that of Remark 3.8 and Algorithm 1. We also compare to (Munoz et al. 2021), and we emphasize that Munoz incurs lower suboptimality because it privatizes only b(D) in the constraints, while Algorithm 1 is used to privatize both A(D) and b(D). The approach in (Munoz et al. 2021) only incurs 0.5% suboptimality at ϵ = 2, while the approach in Algorithm 1 incurs roughly 20% sub-optimality, which indicates that privacy for A(D) induces 19.5% additional sub-optimality.

is 0 with probability 0.2 and is drawn uniformly from [0, 1] with probability 0.8. We also set bi = 107 for all i ∈[N] and nj = 107 for all j ∈[M]. The performance loss for case (i) is shown in Figure 1 for ϵ ∈[0.25, 2] and δ = 0.1. Our work maintains zero constraint violation, as guaranteed by Theorem 3.10, while (Hsu et al. 2014b) violates constraints at every value of ϵ, up to 51% of constraints at ϵ = 0.25.

For case (ii), we use Algorithm 1 without any modifications using the same problem parameters as case (i). There is no other work to the authors’ knowledge that can keep both pij(D) and b(D) private simultaneously. However, we still present comparisons to (Munoz et al. 2021). The work in (Munoz et al. 2021) can only keep b(D) private in the constraints, which means that it leaks private information about pij(D) by not keeping A(D) private, but we include this comparison to quantify how performance is affected by providing privacy to A(D) in addition to c(D) and b(D).

The performance loss for case (ii) is shown in Figure 1. In case (ii), when more quantities are kept private, i.e., both pij(D) and b(D), Algorithm 1 still out-performs (Hsu et al. 2014b), which highlights our method’s improvement over the state of the art. In addition, we see at most a 6% difference in the performance of our method between cases (i) and (ii) (which occurs when ϵ = 2), indicating only minor performance loss with additional private quantities in an LP. Similarly, we find a 20% increase in sub-optimality between Algorithm 1 and (Munoz et al. 2021) at ϵ = 2, indicating modest increases in sup-optimality when privatiz-

0 20 40 60 80 100

20%

40%

60%

80%

Number of Sensitive Constraints, M

Sub-Optimality

Remark 3.8 Algorithm 1 (Hsu et al. 2014b) (Munoz et al. 2021)

**Figure 2.** Performance loss with varying M. As the number of variables increases, Algorithm 5 in (Hsu et al. 2014b) allows their solver to run for more iterations, leading to improvement in accuracy, though this leads to a dramatic increase in computation time. In Algorithm 1, we see only an 11% decrease in optimal revenue with a 10× increase in problem size, going from 13.3% sub-optimality with M = 10 to 24% sub-optimality at M = 100. Performance remains roughly constant with increasing number of constraints for Algorithm 1 and (Munoz et al. 2021), while Algorithm 5 in (Hsu et al. 2014b) steadily improves in performance but still has much higher sub-optimality.

ing both pij(D) and b(D) in the constraints as opposed to only b(D).

Next, we analyze how performance varies with increasing problem size, namely increasing M shown in Figure 2. We note that increasing M increases both the number of variables and the number of sensitive constraints. Since we have shown that our mechanism never violates the constraints while the work in (Hsu et al. 2014b) does, we instead focus our comparisons on performance. We fix ϵ = 1, δ = 0.1, N = 20, and a randomly drawn pij(D), where pij(D) is 0 with probability 0.2 and is drawn uniformly from [0, 1] with probability 0.8. We simulate 100 samples for each M ∈{5, 6,..., 100}. Since Algorithm 5 in (Hsu et al. 2014b) runs for more iterations on problems with more decision variables, they see an increase in solution quality with increasing M, though in exchange for a significant increase in computation time. We see only a 10% increase sub-optimality for a 10 fold increase in M without any change in computational complexity due to privacy, highlighting the scalability of our work. Additionally when privatizing b(D) with increasing M, the performance of Algorithm 1 is virtually identical to that of the method from (Munoz et al. 2021), which highlights both methods’ ability to perform at scale.

## 6 Conclusion

We presented a method for simultaneously keeping the constraints and costs private in linear programming. We showed that this method is differentially private and that it always produces a feasible solution with respect to the original, non-private constraints. Future work will focus on guaranteed constraint satisfaction while privatizing nonlinear and stochastic constraints.

19708

<!-- Page 8 -->

## Acknowledgements

This work was partially supported by AFRL under grant FA8651-23-F-A008, NSF under CAREER grant 2422260 and Graduate Research Fellowship under grant DGE-2039655, ONR under grant N00014-24-1-2432, and AFOSR under grant FA9550-19-1-0169. Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of sponsoring agencies.

## References

Agarwal, N.; Kairouz, P.; and Liu, Z. 2021. The skellam mechanism for differentially private federated learning. Advances in Neural Information Processing Systems, 34: 5052–5064. Benvenuti, A.; Bialy, B.; Dennis, M.; and Hale, M. 2024a. Guaranteed Feasibility in Differentially Private Linearly Constrained Convex Optimization. IEEE Control Systems Letters, 8: 2745–2750. Benvenuti, A.; Hawkins, C.; Fallin, B.; Chen, B.; Bialy, B.; Dennis, M.; and Hale, M. 2024b. Differentially Private Reward Functions for Markov Decision Processes. In 2024 IEEE Conference on Control Technology and Applications (CCTA), 631–636. IEEE. Chen, B.; Hawkins, C.; Karabag, M. O.; Neary, C.; Hale, M.; and Topcu, U. 2023. Differential privacy in cooperative multiagent planning. In Uncertainty in Artificial Intelligence, 347–357. PMLR. Chen, W.-N.; Choo, C. A. C.; Kairouz, P.; and Suresh, A. T. 2022. The fundamental price of secure aggregation in differentially private federated learning. In International Conference on Machine Learning, 3056–3089. PMLR. Cort´es, J.; Dullerud, G. E.; Han, S.; Le Ny, J.; Mitra, S.; and Pappas, G. J. 2016. Differential privacy in control and network systems. In 55th IEEE Conference on Decision and Control (CDC), 4252–4272. Cummings, R.; Kearns, M.; Roth, A.; and Wu, Z. S. 2015. Privacy and truthful equilibrium selection for aggregative games. In Web and Internet Economics: 11th International Conference, 286–299. Dobbe, R.; Pu, Y.; Zhu, J.; Ramchandran, K.; and Tomlin, C. 2018. Customized local differential privacy for multi-agent distributed optimization. arXiv preprint arXiv:1806.06035. Dvorkin, V.; Fioretto, F.; Van Hentenryck, P.; Kazempour, J.; and Pinson, P. 2020. Differentially private convex optimization with feasibility guarantees. arXiv preprint arXiv:2006.12338. Dwork, C.; McSherry, F.; Nissim, K.; and Smith, A. 2006. Calibrating noise to sensitivity in private data analysis. In Theory of cryptography conference, 265–284. Springer. Dwork, C.; and Roth, A. 2014. The algorithmic foundations of differential privacy. Foundations and Trends in Theoretical Computer Science, 9(3–4): 211–407. Geng, Q.; Ding, W.; Guo, R.; and Kumar, S. 2020. Tight analysis of privacy and utility tradeoff in approximate differential privacy. In International Conference on Artificial Intelligence and Statistics, 89–99. PMLR.

Geyer, R. C.; Klein, T.; and Nabi, M. 2017. Differentially private federated learning: A client level perspective. arXiv preprint arXiv:1712.07557. Han, S.; Topcu, U.; and Pappas, G. J. 2016. Differentially private distributed constrained optimization. IEEE Transactions on Automatic Control, 62(1): 50–64. Hawkins, C.; and Hale, M. 2020. Differentially private formation control. In 2020 59th IEEE Conference on Decision and Control (CDC), 6260–6265. IEEE. Hoffman, A. J. 1952. On Approximate Solutions of Systems of Linear Inequalities. Journal of Research of the National Bureau of Standards, 49(4). Hsu, J.; Gaboardi, M.; Haeberlen, A.; Khanna, S.; Narayan, A.; Pierce, B. C.; and Roth, A. 2014a. Differential privacy: An economic method for choosing epsilon. In 2014 IEEE 27th Computer Security Foundations Symposium, 398–410. IEEE. Hsu, J.; Roth, A.; Roughgarden, T.; and Ullman, J. 2014b. Privately solving linear programs. In Automata, Languages, and Programming: 41st International Colloquium, 612– 624. Springer. Huang, Z.; Mitra, S.; and Vaidya, N. 2015. Differentially private distributed optimization. In Proceedings of the 16th International Conference on Distributed Computing and Networking, 1–10. Kaplan, H.; Mansour, Y.; Moran, S.; Stemmer, U.; and Tur, N. 2024. On Differentially Private Linear Algebra. arXiv preprint arXiv:2411.03087. Le Ny, J.; and Pappas, G. J. 2013. Differentially private filtering. IEEE Transactions on Automatic Control, 59(2): 341–354. Lv, Y.-W.; Yang, G.-H.; and Shi, C.-X. 2020. Differentially private distributed optimization for multi-agent systems via the augmented lagrangian algorithm. Information Sciences, 538: 39–53. Markowitz, H. 1952. Portfolio Selection. The Journal of Finance, 7(1): 77–91. Munoz, A.; Syed, U.; Vassilvtiskii, S.; and Vitercik, E. 2021. Private optimization without constraint violations. In International Conference on Artificial Intelligence and Statistics, 2557–2565. PMLR. Noble, M.; Bellet, A.; and Dieuleveut, A. 2022. Differentially private federated learning on heterogeneous data. In International Conference on Artificial Intelligence and Statistics, 10110–10145. PMLR. Nozari, E.; Tallapragada, P.; and Cort´es, J. 2016. Differentially private distributed convex optimization via objective perturbation. In 2016 American control conference (ACC), 2061–2066. IEEE. Pena, J.; Vera, J.; and Zuluaga, L. 2018. An algorithm to compute the Hoffman constant of a system of linear constraints. arXiv preprint arXiv:1804.08418. Pena, J.; Vera, J. C.; and Zuluaga, L. F. 2021. New characterizations of Hoffman constants for systems of linear constraints. Mathematical Programming, 187: 79–109.

19709

<!-- Page 9 -->

Robinson, S. M. 1973. Bounds for error in the solution set of a perturbed linear program. Linear Algebra and its applications, 6: 69–81. Stott, B.; Marinho, J.; and Alsac, O. 1979. Review of linear programming applied to power system rescheduling. In Proceedings of the Power Industry Computer Applications Conference, 142–154. Wang, Y.; Hale, M.; Egerstedt, M.; and Dullerud, G. E. 2016. Differentially private objective functions in distributed cloud-based optimization. In 2016 IEEE 55th Conference on Decision and Control (CDC), 3688–3694. IEEE. Yazdani, K.; Jones, A.; Leahy, K.; and Hale, M. 2022. Differentially private LQ control. IEEE Transactions on Automatic Control.

19710
