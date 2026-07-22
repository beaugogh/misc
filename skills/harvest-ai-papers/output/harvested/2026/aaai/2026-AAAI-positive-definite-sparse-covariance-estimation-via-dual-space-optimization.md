---
title: "Positive Definite Sparse Covariance Estimation via Dual Space Optimization"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39453
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39453/43414
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Positive Definite Sparse Covariance Estimation via Dual Space Optimization

<!-- Page 1 -->

Positive Deﬁnite Sparse Covariance Estimation via Dual Space Optimization

Fengpei Li*, Wenfu Xia*, Ziping Zhao†

ShanghaiTech University {fengpeili, wenfuxia, zipingzhao}@shanghaitech.edu.cn

## Abstract

Covariance matrix estimation in high dimensions is a fundamental problem in machine learning and signal processing. A common structural assumption used to mitigate the challenges posed by high dimensionality is sparsity, which posits that most variable pairs exhibit negligible correlations. In this paper, we revisit the classical problem of positive definite sparse covariance estimation (PDSCE) introduced by Rothman (2012). Unlike many earlier approaches, this formulation incorporates a logarithmic barrier, which guarantees that the resulting covariance estimator is positive deﬁnite and thereby ensures the well-posedness of the estimation problem. However, the inclusion of the logarithmic barrier also leads to nontrivial optimization difﬁculties. To overcome these difﬁculties, we propose a dual proximal gradient method (DPGM) for solving the PDSCE problem. In contrast to existing primal-space approaches, DPGM operates directly in the dual space. This dual perspective provides several key advantages. First, DPGM signiﬁcantly reduces computational costs, because positive deﬁniteness is preserved automatically and no iterative subproblem solvers are required. Second, compared with primal optimization algorithms, DPGM offers stronger theoretical guarantees, including principled step size selection and improved iteration complexity. Extensive numerical experiments demonstrate that DPGM consistently outperforms existing methods, which conﬁrms its effectiveness and scalability for high-dimensional sparse covariance estimation.

## Introduction

The estimation of covariance matrices lies at the core of numerous fundamental problems in modern multivariate data analysis, with broad applications in machine learning (Jolliffe 2002), ﬁnance (Ledoit and Wolf 2003), and biology (Sch¨afer and Strimmer 2005). For example, in machine learning, they are prerequisites for dimensionality reduction methods such as principal component analysis (Jolliffe 2002) and for classiﬁcation techniques like linear and quadratic discriminant analysis (Witten and Tibshirani 2009; Xiong et al. 2018); in ﬁnance, covariance matrices are essential for portfolio optimization to manage risk and al-

*These authors contributed equally. †Corresponding author. Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

locate assets (Markowitz 1952; Zhao and Palomar 2018; Zhao, Zhou, and Palomar 2019); in biology, covariance matrices are used to infer large-scale gene association networks (Faust and Raes 2012). However, in high-dimensional settings where the problem dimension far exceeds the sample size, covariance matrix estimation becomes particularly challenging. A commonly used estimator is the sample covariance matrix. However, when the problem dimension and the sample size grow proportionally, or even when the dimensionality exceeds the number of samples, the sample covariance matrix is no longer a consistent estimator of the population covariance matrix. As a result, reliance on the sample covariance matrix can severely degrade the performance of downstream tasks. For instance, in principal component analysis, it may overestimate the importance of certain components due to inaccurate eigenvalue estimates (Karoui 2008b). These limitations have spurred intense research interest in high-dimensional covariance estimation in recent years (Zhao and Liu 2013; Fan, Liao, and Liu 2016; Donoho, Gavish, and Johnstone 2018; Yan, Yang, and Zhao 2025). To effectively estimate high-dimensional covariance matrices, a widely adopted strategy is to impose structural assumptions. Sparsity is one of the most commonly used approaches, wherein many of the entries are assumed to be zero (Bickel and Levina 2008). This reduces the effective number of parameters and improves statistical convergence rates. A common method for sparse covariance estimation is thresholding, where small entries of the sample covariance matrix are set to zero (Karoui 2008a; Rothman, Levina, and Zhu 2009). Despite possessing desirable theoretical properties, including minimax optimality and fast statistical convergence rates, these estimators generally lack guaranteed positive deﬁniteness. To simultaneously enforce positive deﬁniteness and sparsity, many estimation problems have been proposed. In this paper, we revisit the positive deﬁnite sparse covariance estimation (PDSCE) problem in Rothman (2012):

min Σ∈Sd

++

2 ∥Σ −S∥2 F −τ log det Σ + ∥W ◦Σ∥1, (1)

where S is the sample covariance matrix, −τ log det (·) is the logarithmic barrier with parameter τ ≥0, and ∥W ◦·∥1 is the weighted ℓ1-norm with W being a nonnegative weight

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22896

<!-- Page 2 -->

matrix and ◦denoting the element-wise product. Alternative approaches, such as those proposed by Xue, Ma, and Zou (2012) and Liu, Wang, and Zhao (2014), enforce positive deﬁniteness through explicit eigenvalue constraints. However, these formulations introduce two nonsmooth terms, making them less compelling than Problem (1) from an optimization standpoint.

To solve the PDSCE problem, several algorithms have been proposed. Rothman (2012) introduced a row-by-row block coordinate minimization method (BCM) that exploits the structure of symmetric positive deﬁnite matrices by updating one row (and the corresponding column) at a time. However, each subproblem requires solving a Lasso problem (Tibshirani 1996) via an inner loop, resulting in a computationally expensive double-loop algorithm. A further limitation of BCM is that it does not necessarily guarantee the iterates remain positive deﬁnite unless the algorithm converges. In addition, the iteration complexity of BCM scales linearly with the problem dimension d, requiring O(d log 1/ϵ) iterations to reach an ϵ-stationary point, which becomes prohibitively slow in high-dimensional settings (Li et al. 2018). Kyrillidis et al. (2014) proposed an inexact proximal Newton method (PNM) that leverages local Hessian information and achieves a local quadratic convergence rate. While theoretically appealing, PNM suffers from two major practical drawbacks. First, it requires damped proximal Newton steps to ensure positive deﬁniteness and to compensate for the lack of global Lipschitz smoothness, which often leads to overly conservative updates. Second, like BCM, it adopts a double-loop structure that necessitates solving a Lasso problem. These computational bottlenecks signiﬁcantly limit its practical efﬁciency.

Recently, Wei and Zhao (2023) developed a proximal gradient method (PGM) for the PDSCE problem, which requires careful step-size selection to ensure positive deﬁniteness. However, checking positive deﬁniteness in each line search relies on the Cholesky decomposition, which incurs substantial computational overhead. Furthermore, this work does not provide further convergence analysis. To bridge this gap, in this paper, we ﬁrst provide a complete analysis of the PGM algorithm, offering guidelines for step-size selection to ensure positive deﬁniteness and establishing its iteration complexity. However, the theoretical step size is overly conservative, which signiﬁcantly hinders the practical efﬁciency of PGM.

Motivated by the limitations of the algorithms discussed above, we develop an efﬁcient algorithm for the PDSCE problem. The core innovation of our approach lies in applying the proximal gradient method to the dual formulation of Problem (1). The proposed algorithm offers several distinct advantages over existing methods. Its computational cost is lower than that of current algorithms, as it naturally generates positive deﬁnite iterates of Σ at each iteration without additional overhead, and no subproblems need to be solved iteratively. In addition, the method provides theoretical beneﬁts through an effective step size that eliminates the need for backtracking line searches. We conduct extensive experiments on both synthetic and real-world datasets, which demonstrate the superior efﬁciency of our algorithm com- pared to state-of-the-art methods and conﬁrm its effectiveness for high-dimensional problems.

## Preliminaries

Notations Given a d-dimensional symmetric matrix X, its eigendecomposition is X = V ΛV ⊤, where Λ is a diagonal matrix with ordered eigenvalues λ1 (X) = Λ1,1 ≥· · · ≥ λd (X) = Λd,d and V is an orthogonal matrix of eigen- vectors. We deﬁne ∥X∥F = qP i,j X2 ij as the Frobenius norm, ∥X∥1 = P ij |Xij| as the element-wise ℓ1-norm, and ∥X∥∞= maxij |Xij| as the element-wise ℓ∞-norm. We denote by I the identity matrix, by ⊗the Kronecker product, and by ◦the Hadamard product. Sd

++ denotes the set of symmetric positive deﬁnite matrices of dimension d, Sd denotes the set of symmetric matrices of dimension d, and R denotes the set of real numbers.

Lipschitz smoothness and strong convexity A differentiable convex function f is called L-Lipschitz smooth if, for all X, Y, f(Y) ≤f(X) + ⟨∇f(X), Y −X⟩+ L

2 ∥X −Y ∥2 F, and is called µ-strongly convex if f(Y) ≥f(X) + ⟨∇f(X), Y −X⟩+ µ

2 ∥X −Y ∥2 F.

## 3 Eigenvalue bounds for the PDSCE solution

We ﬁrst establish eigenvalue bounds for the solution to the PDSCE problem (1) in the following theorem.

Theorem 1. The solution to the PDSCE problem (1), bΣ, is unique and satisﬁes αI ⪯bΣ ⪯βI, where the universal constants α and β are deﬁned as α = λd (S) −∥W ∥∞d + q

(λd (S) −∥W ∥∞d)2 + 4τ

, β = λ1 (S) + ∥W ∥∞d + q

(λ1 (S) + ∥W ∥∞d)2 + 4τ

.

To the best of our knowledge, Theorem 1 presents a new spectral characterization that has not been documented in existing literature, and it will serve as a cornerstone of the following algorithm analysis.

## 4 Existing Algorithms for PDSCE

Before introducing our proposed method, we review three representative algorithms, namely BCM, PNM, and PGM, for solving the PDSCE problem (1), with a focus on their algorithmic structures and limitations. BCM was introduced in the seminal work (Rothman 2012) and exhibits several critical limitations that make it unsuitable for large-scale problems. First, it does not guarantee the positive deﬁniteness of the iterates, which is essential for producing a valid covariance matrix. Second, its iteration complexity scales linearly

22897

<!-- Page 3 -->

## Method

Reference Iteration Complexity Single Loop Positive Deﬁniteness Guarantee

BCM Rothman (2012) O(dL2µ−2 log(1/ϵ)) % % prior to convergence PNM Kyrillidis et al. (2014) O(log log(1/ϵ)) (local) %! via damped step size PGM Wei and Zhao (2023) O

L (β+

√ d(α+β))2

(β+

√ d(α+β))2+τ log(1/ϵ)

!! via line-search step size

DPGM This Paper O(Lµ−1 log(1/ϵ))!! naturally

We deﬁne L = α2+τ α2 and µ = β2+τ β2 as the locally smooth and strongly convex parameters of Problem (1).

**Table 1.** Comparison of existing optimization methods for the PDSCE problem.

with the ambient dimension d. Third, its double-loop architecture incurs substantial computational overhead in highdimensional settings. A summary of these properties is provided in Table 1.

In what follows, we primarily introduce the PNM (Kyrillidis et al. 2014) and PGM (Tran-Dinh, Kyrillidis, and Cevher 2015; Wei and Zhao 2023) methods for the PDSCE problem. Both methods exploit the composite structure of the objective function, which consists of a smooth term f and a non-smooth term g. We deﬁne the functions f, g: Sd

++ →R by f(Σ):= 1 2 ∥Σ −S∥2 F −τ log det Σ and g(Σ) = ∥W ◦Σ∥1. Speciﬁcally, at the (t + 1)-th iteration, the updates of both methods can be formulated as the solution to the following subproblem:

Σt+1 = arg min

Σ∈Sd

++

{u(Σ, Σt) + g(Σ)}, (2)

where u(Σ, Σt) is the quadratic approximation of f(Σ) at Σt, deﬁned by u(Σ, Σt):= f(Σt) + ⟨∇f(Σt), Σ −Σt⟩

+ 1

2 ⟨vec (Σ −Σt), M t vec (Σ −Σt)⟩, where ∇f (Σt) = Σt −S −τΣ−1 t and M t is a symmetric positive semideﬁnite matrix that determines the secondorder information of the surrogate.

Proximal Newton Method PNM (Kyrillidis et al. 2014) incorporates second-order information through the Hessian matrix:

M t = ∇2f(Σt) = I + τΣ−1 t ⊗Σ−1 t.

Since f is not globally Lipschitz smooth, and to ensure positive deﬁniteness of Σt+1, Kyrillidis et al. (2014) proposed a damped update scheme consisting of two phases. First, an intermediate solution is computed by solving the following problem:

Σt+ 1

2 = arg min Σ∈Sd

++

{u(Σ, Σt) + g(Σ)}. (3)

Then, a damped update is performed using the rule

Σt+1 = (1 −γt) Σt + γtΣt+ 1

2, (4)

where γt ∈(0, 1) is a relaxation parameter adaptively determined based on both Σt+ 1

2 and Σt.

In practice, the overall performance often falls short of expectations due to several key factors. First, the surrogate problem (3) lacks a closed-form solution and must be solved using iterative methods such as FISTA (Beck and Teboulle 2009), resulting in a double-loop algorithmic structure. Second, the damped update often leads to overly conservative step sizes: when Σt+ 1

2 deviates signiﬁcantly from Σt, the relaxation parameter γt becomes very small, causing Σt+1 to remain close to Σt. Third, although Kyrillidis et al. (2014) established the convergence rate of PNM without assuming global Lipschitz smoothness by utilizing the self-concordance property of f, the locally quadratic convergence rate is typically attained only within a small unknown region of the optimum.

Proximal Gradient Method The earliest use of the PGM to solve the PDSCE problem appears in Tran-Dinh, Kyrillidis, and Cevher (2015), where the two updates in (3) and (4) are retained, except that the matrix M t is set to M t = 1 ηt I, with ηt being a step size. However, the damped-type update in (4) often leads to performance degradation in practice. Recently, Wei and Zhao (2023) proposed an alternative PGM method that eliminates the relaxation step (4). The step size ηt is selected via backtracking line search to ensure both the sufﬁcient decrease condition f(Σt+1) ≤u(Σt+1, Σt), and the positive deﬁniteness of Σt+1. This algorithm has been shown to achieve better empirical performance compared to the method in Tran-Dinh, Kyrillidis, and Cevher (2015). In this paper, we establish the convergence of the PGM algorithm proposed in Wei and Zhao (2023). As a preliminary step, the following lemma shows that while f is neither globally Lipschitz smooth nor strongly convex over Sd

++, both properties hold locally over any compact subset.

Lemma 2. The function f(Σ) is (1 + τ a2)-smooth and (1 + τ b2)-strongly convex over the set

CΣ(a, b) =

Σ ∈Sd

++ aI ⪯Σ ⪯bI

, where 0 < a < b. Speciﬁcally, for any Σ1, Σ2 ∈CΣ(a, b), the following inequalities hold:

∥∇f(Σ1) −∇f(Σ2)∥F ≤

1 + τ a2

∥Σ1 −Σ2∥F,

∥∇f(Σ1) −∇f(Σ2)∥F ≥

1 + τ b2

∥Σ1 −Σ2∥F.

22898

<!-- Page 4 -->

To establish the iteration complexity of the PGM algorithm, we select parameters a and b such that Σt ∈ CΣ(a, b) for all iterations t. This ensures that the Lipschitz smoothness and strong convexity properties of f remain well-controlled throughout the optimization process. Furthermore, Theorem 1 guarantees that the optimal solution satisﬁes bΣ ∈CΣ(α, β), which necessitates the condition CΣ(α, β) ⊆CΣ(a, b) to ensure consistency between the iterates and the optimal solution. We are now ready to present the convergence result.

Theorem 3. Let α and β be the constants deﬁned in Theorem 1. Suppose the step size satisﬁes ηt ≤ α2 τ+α2. Then all iterates generated by PGM remain within the set CΣ(α, β + √ d(α + β)). Moreover, for any t ≥0, let Σt and Σt+1 be two successive iterates generated by the update in (2), we have:

Σt+1 −bΣ

F ≤ s

1 − α2 α2 + τ · (β +

√ d(α + β))2 + τ (β +

√ d(α + β))2

· Σt −bΣ

F, with ηt = α2 τ+α2, leading to an iteration complexity of

O α2 + τ α2 · (β +

√ d(α + β))2

(β +

√ d(α + β))2 + τ

· log 1 ϵ

!

.

Theorem 3 establishes the existence of a step size that guarantees positive deﬁniteness and allows the derivation of the corresponding iteration complexity. In practice, however, this step size is overly conservative. Using this step size in PGM results in very slow convergence.

## 5 Proposed Method: DPGM

In this section, we propose a new method for solving the PDSCE problem (1), which is based on applying the PGM in the dual space. We begin by deriving the dual formulation of Problem (1). To this end, we introduce an auxiliary variable Ψ and reformulate the original problem into the following linearly constrained convex program:

min Σ∈Sd

++, Ψ∈Sd f (Σ) + g (Ψ)

s. t. Σ = Ψ.

(5)

The Lagrangian associated with the reformulated problem is given by

L(Σ, Ψ, Γ) = f (Σ) + g (Ψ) + ⟨Γ, Σ −Ψ⟩.

where Γ ∈Sd denotes the Lagrange multiplier associated with the constraint Σ = Ψ.

To derive the dual function, we minimize L with respect to the primal variables Σ and Ψ. The minimization over Σ admits the following solution arg min

Σ∈Sd

++

{f(Σ) + ⟨Γ, Σ⟩} = V Jτ (Λ) V ⊤,

## Algorithm

1: DPGM for PDSCE Problem

Input: S, W

1 Initialize Σ0 = diag(S), Γ 0 = Σ0 −S −τΣ−1 0 2 while not converged do

3 Compute gradient ∇h (Γ t) via (7)

Select ηt via backtracking line search or as given in Theorem 5

5 Update dual variable Γ t+1 via (8)

6 end Output: Γ t+1, Σt+1 = ∇h(Γ t+1)

where V and Λ come from the eigendecomposition S−Γ = V ΛV ⊤and Jτ(·) is the proximal operator of −τ log det(·) with

[Jτ (Λ)]i,j =

(

Λij+√

Λ2 ij+4τ 2 i = j, 0 i̸ = j. The inﬁmum over Ψ can be computed in closed form as inf Ψ∈Sd {g (Ψ) −⟨Γ, Ψ⟩} =

0 if |Γij| ≤Wij, −∞ otherwise.

which leads to the constraint |Γij| ≤Wij for all i, j in the dual space. Combining the above results, the dual formulation of the PDSCE problem (1) becomes max

Γ

1 2

V Jτ(Λ)V ⊤−S

2

F −τ log det Jτ(Λ)

+

D

Γ, V Jτ(Λ)V ⊤E s. t. |Γij| ≤Wij.

(6)

We now present our proposed DPGM approach for solving the dual PDSCE problem (6). Let h(Γ): Sd →R denote the objective function in the dual problem (6). Given the current iterate Γ t at iteration t, the gradient is computed as

∇h(Γ t) = V tJτ(Λt)V ⊤ t, (7)

where S −Γ t = V tΛtV ⊤ t is the eigendecomposition. The dual variable is then updated via the proximal gradient step:

Γ t+1 = PW (Γ t + ηt∇h(Γ t)), (8)

where ηt is the step size, and PW (·) denotes the projection onto the box constraint set {X | |Xij| ≤Wij}, deﬁned elementwise by

[PW (X)]ij = min {max {Xij, −Wij}, Wij}.

The step size ηt is selected through a backtracking line search until the following condition is satisﬁed:

h(Γ t+1) −h(Γ t) + 1

2ηt ∥Γ t+1 −Γ t∥2

F

≥⟨∇h(Γ t), Γ t+1 −Γ t⟩,

(9)

or alternatively, the theoretically optimal choice of ηt given in Theorem 5 can be adopted.

Notably, the primal solution bΣ can be recovered from the dual optimum bΓ via the strong duality: bΣ = bV Jτ(bΛ) bV

⊤,

22899

<!-- Page 5 -->

where bV and bΛ come from the eigendecomposition of S−bΓ and bΓ is the solution to Problem (6). Consequently, the proposed method simultaneously generates a sequence of primal covariance matrix iterates:

Σt = V tJτ(Λt)V ⊤ t. (10) Crucially, the positive deﬁniteness of all iterates Σt is naturally preserved by the proximal operator Jτ(·), independent of the step size ηt. The complete dual proximal gradient method is summarized in Algorithm 1.

Computation Costs We brieﬂy outline the practical computational advantages of DPGM. The inner subproblems of BCM, PNM, and PGM all entail multiple iterative operations, such as solving Lasso problems and performing Cholesky decompositions to verify positive deﬁniteness, each incurring O(d3) time complexity. In contrast, DPGM requires only a single O(d3) operation for eigendecomposition.

## 6 Convergence Analysis To demonstrate that solving

Problem (1) in the dual space offers advantages beyond the guaranteed positive deﬁniteness of Σ, we conduct a rigorous analysis of Algorithm 1. As a ﬁrst step, we characterize the strong concavity and smoothness properties of the dual objective function h.

Lemma 4. The dual objective function h(Γ) is (b2 b2+τ)- smooth and (a2 a2+τ)-strongly concave over the set CΓ (a, b) = {Γ | aI ⪯V Jτ(Λ)V ⊤⪯bI, S −Γ = V ΛV ⊤}. Speciﬁcally, for any Γ 1, Γ 2 ∈CΓ (a, b), the following inequalities hold:

∥∇h(Γ 1) −∇h(Γ 2)∥F ≤ b2 b2 + τ ∥Γ 1 −Γ 2∥F,

∥∇h(Γ 1) −∇h(Γ 2)∥F ≥ a2 a2 + τ ∥Γ 1 −Γ 2∥F.

Moreover, Algorithm 1 generates iterates satisfying Γ t ∈ CΓ (α, β) and Σt ∈CΣ(α, β) for all t ≥0.

Lemma 4 highlights the key advantages of solving the dual problem. First, the Lipschitz smoothness modulus of the dual objective h is upper bounded by b2 b2+τ < 1, which implies that a dimensional independent worst-case step size choice ηt = 1 is always valid. Second, the iterates of Algorithm 1 remain within a tighter spectral set CΣ(α, β), in contrast to CΣ(α, β +

√ d(α + β)) required for PGM. This con- ﬁnement enables stronger convergence guarantees and leads to improved iteration complexity, as formalized in the following theorem. Theorem 5. Let Γ t+1 and Γ t be iterates generated by Algorithm 1 according to (8), and let bΓ denote the optimal solution to Problem (6). Then, the following holds: Γ t+1 −bΓ

F ≤max

1 −ηt α2 α2 + τ

,

1 −ηt β2 β2 + τ

· Γ t −bΓ

F, for some step size ηt > 0. Furthermore:

1. Algorithm 1 converges linearly if the step size ηt satisﬁes

0 < max 1 −ηt · α2 α2 + τ

,

1 −ηt · β2 β2 + τ

< 1.

2. The optimal worst-case contraction is achieved when ηt = 2 · (α2 α2+τ + β2 β2+τ)−1 in which case the contraction factor becomes max

1 −ηt · α2 α2 + τ

,

1 −ηt · β2 β2 + τ

= L −µ

L + µ, where L = α2+τ α2 and µ = β2+τ β2. This leads to an iteration complexity of

O

1

4 · Lµ−1 · log 1 ϵ

.

The core of Theorem 5 lies in its provision of a simple and effective theoretical step size selection. Additionally, compared to PGM, the iteration complexity of DPGM is improved. Building on Theorem 5, the following corollary establishes the linear convergence of the corresponding primal sequence. Corollary 6. Let Σt be the primal iterate generated via (10) in Algorithm 1, and let bΣ denote the optimal solution to Problem (1). Then, for all t ≥0,

Σt −bΣ

F ≤

L −µ

L + µ t Γ 0 −bΓ

F.

## 7 Numerical Experiments

In this section, we compare the performance of the proposed DPGM algorithm with BCM, PNM, and PGM on both synthetic and real-world datasets. All methods are initialized with Σ0 = diag(S). For the proposed method, we additionally set Γ 0 = Σ0 −S −τΣ−1

0.

Synthetic Data Experiments We consider three types of covariance matrices as ground truth, all of which are guaranteed to be positive deﬁnite. 1. Block Matrix: The indices {1,..., d} are evenly partitioned into groups, with Σ⋆ ij = 0.8 if i̸ = j and i, j belong to the same group and 0 otherwise. 2. Banded Matrix: The entries are deﬁned as Σ⋆ ij = 1 − |i−j| m for |i −j| ≤m, and 0 otherwise.

## 3 Toeplitz Matrix:

The entries are Σ⋆ ij = 0.75|i−j|. We ﬁx the group size of the block matrix at 100, yielding d

100 blocks. This setting ensures that the largest and smallest eigenvalues of Σ⋆are independent of the dimensionality. For banded matrix, we set the bandwidth m = d

100 to maintain a consistent sparsity level in Σ⋆. The Toeplitz structure inherently ensures that its extremal eigenvalues are dimension-independent. Consistent with high-dimensional settings, we set n = d observations for all experiments. The parameter τ was ﬁxed at 10−4 as recommended by Rothman (2012) to obtain a stable solution.

22900

<!-- Page 6 -->

0 200 400 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(a) Banded matrix, d = 500

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(b) Banded matrix, d = 1000

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(c) Banded matrix, d = 1500

0 200 400 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(d) Block matrix, d = 500

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(e) Block matrix, d = 1000

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(f) Block matrix, d = 1500

0 200 400 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(g) Toeplitz matrix, d = 500

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(h) Toeplitz matrix, d = 1000

0 200 400 600 CPU Time (seconds)

10−8

10−6

10−4

10−2

100

|F(Σt) −F(ˆΣ)|/F(ˆΣ)

BCM PNM PGM DPGM (prop.)

(i) Toeplitz matrix, d = 1500

**Figure 1.** Relative errors of the objective values versus the computational time for dimensions ranging from 500 to 1500.

We ﬁrst investigate the performance of the algorithms under different dimensions. We evaluate three scenarios with d = 500, d = 1000, and d = 1500. The diagonal elements of W are set to zero, and the off-diagonal elements are set to ρ, where ρ is selected to minimize bΣ −Σ⋆

F through a grid search on a logarithmic scale from 10−3 to 1. Each iteration, we calculate the relative errors F (Σ)−F (b Σ) |F (b Σ)| of all algorithms, where F(Σ) = f(Σ) + g(Σ) signiﬁes the objective function of Problem (1).

As shown in Figure 1, our proposed method signiﬁcantly outperforms all state-of-the-art approaches in terms of convergence time for. In most cases, PGM is faster than BCM and PNM, likely due to the double-loop structure of the latter two algorithms. PGM exhibits smaller per-step increments, possibly because the step size must simultaneously satisfy both the positive deﬁniteness and descent conditions. We can observe that PNM exhibits local quadratic convergence. However, it is evident that this behavior occurs only when the algorithm is close to convergence.

Next, we ﬁx the dimension at d = 1000 to examine how different regularization settings affect algorithmic efﬁciency. Speciﬁcally, we test regularization parameters ρ = 0.04, 0.08, and 0.12. Table 2 presents the average runtime and number of iterations required for each algorithm. We see that the proposed algorithm outperforms every other algorithm with respect to running time on all the high-dimensional settings. At the same time, we also observe that the proposed algorithm exhibits fewer iterations compared to other algorithms.

22901

<!-- Page 7 -->

Structure Algorithm BCM PNM PGM DPGM (prop.)

ρ Time(s) Iter Time(s) Iter Time(s) Iter Time(s) Iter

Block

0.04 3607.33 34 2871.34 162 519.14 242 3.59 20

0.08* 4643.19 33 2452.51 98 151.86 91 5.89 33

0.12 6700.25 63 1934.73 76 80.77 67 12.60 52

Banded

0.04 3729.17 55 3076.28 193 276.02 165 5.84 28

0.08* 5680.03 67 2831.92 165 327.70 193 10.17 51

0.12 6012.36 86 2614.66 143 361.77 231 13.86 63

Toeplitz

0.04 3669.72 47 3162.55 178 1183.75 561 7.01 27

0.08 5622.96 68 2981.49 154 386.17 218 12.44 48

0.12* 6015.70 91 2561.77 130 182.21 149 9.46 41

S&P 500 0.01 1753.29 32 597.70 12 46.72 21 0.239 3

**Table 2.** Runtime comparisons on synthetic data with d = 1000 and S&P 500 data with d = 415. The asterisk (*) marks the conﬁguration achieving the minimal Frobenius norm error ∥bΣ −Σ⋆∥F across all three parameter settings.

Real-world Data Experiments

We conduct an experiment using real-world datasets from ﬁnancial stock markets. We collect historical daily stock prices for S&P 500 Index constituents from January 1, 2010, to December 31, 2020. After excluding missing data, we obtain daily returns for 415 stocks (d = 415). We generate 100 daily return time series datasets, each with a randomly selected start date and spanning 252 consecutive trading days. For each dataset, we estimate the covariance matrix and calculate the portfolio return risk of the global minimum variance portfolio based on these estimated covariances. Let Σ denote a generic estimator of the covariance matrix of asset returns, and w represent the allocation vector for a portfolio comprising d ﬁnancial securities. The risk of the estimated portfolio is deﬁned as:

min w∈Rd w⊤Σw s. t. w⊤1 = 1, w ≥0.

The quality of the estimated covariance matrix Σ directly affects the portfolio risk, with more accurate estimates resulting in lower risk.

We consider four types of covariance matrices as inputs: the sample covariance matrix S (SCM), and three regularized estimators based on Problem (1): the ℓ1-norm penalty, the adaptive Lasso penalty (Zou 2006), and the minimax concave penalty (MCP) (Zhang 2010). The ﬁrst two methods are equivalent to directly solving Problem (1) under different W conﬁgurations, whereas MCP involves solving a sequence of Problem (1) through iterative convexiﬁcation (Fan et al. 2018). We ﬁrst compare the runtime performance of the proposed method with other approaches when solving the ℓ1-penalized estimator using S&P 500 data, as reported in the last row of Table 2. Furthermore, Figure 2 presents a violin plot analysis of portfolio risk across different covariance estimators. It can be observed that the SCM exhibits a higher median and a wider range of volatility, indicating

SCM L1 MCP Adaptive LASSO

0.00

0.01

0.02

0.03

0.04

0.05

0.06

**Figure 2.** Violin plot of the daily volatility for different covariance estimators on stock market data.

both higher portfolio risk and greater instability, whereas using the formulation in Problem (1) signiﬁcantly reduces both risk and volatility.

## 8 Conclusion

In this paper, we have focused on the positive deﬁnite sparse covariance estimation problem. We have analyzed existing methods and identiﬁed their key limitations. To address these issues, we have proposed a novel dual proximal gradient method that inherently preserves positive deﬁniteness through its dual-space formulation. Extensive numerical experiments have demonstrated superior computational efﬁciency across various high-dimensional settings.

22902

<!-- Page 8 -->

## References

Beck, A.; and Teboulle, M. 2009. A fast iterative shrinkagethresholding algorithm for linear inverse problems. SIAM Journal on Imaging Sciences, 2(1): 183–202. Bickel, P. J.; and Levina, E. 2008. Regularized estimation of large covariance matrices. The Annals of Statistics, 36(1): 199 – 227. Donoho, D. L.; Gavish, M.; and Johnstone, I. M. 2018. Optimal shrinkage of eigenvalues in the spiked covariance model. Annals of Statistics, 46(4): 1742–1778. Fan, J.; Liao, Y.; and Liu, H. 2016. An overview of the estimation of large covariance and precision matrices. The Econometrics Journal, 19(1): C1–C32. Fan, J.; Liu, H.; Sun, Q.; and Zhang, T. 2018. I-LAMM for sparse learning: Simultaneous control of algorithmic complexity and statistical error. The Annals of Statistics, 46(2): 814–841. Faust, K.; and Raes, J. 2012. Microbial interactions: from networks to models. Nature Reviews Microbiology, 10(8): 538–550. Jolliffe, I. T. 2002. Principal Component Analysis. Springer Series in Statistics. New York, NY, USA: Springer, 2 edition. Karoui, N. E. 2008a. Operator norm consistent estimation of large-dimensional sparse covariance matrices. The Annals of Statistics, 36(6): 2717–2756. Karoui, N. E. 2008b. Spectrum estimation for large dimensional covariance matrices using random matrix theory. The Annals of Statistics, 36(6): 2757–2790. Kyrillidis, A.; Mahabadi, R. K.; Tran-Dinh, Q.; and Cevher, V. 2014. Scalable sparse covariance estimation via selfconcordance. In Proceedings of the Twenty-Eighth AAAI Conference on Artiﬁcial Intelligence, 1946–1952. Qu´ebec City, Qu´ebec, Canada: AAAI Press. Ledoit, O.; and Wolf, M. 2003. Improved estimation of the covariance matrix of stock returns with an application to portfolio selection. Journal of Empirical Finance, 10(5): 603–621. Li, X.; Zhao, T.; Arora, R.; Liu, H.; and Hong, M. 2018. On faster convergence of cyclic block coordinate descenttype methods for strongly convex minimization. Journal of Machine Learning Research, 18(184): 1–24. Liu, H.; Wang, L.; and Zhao, T. 2014. Sparse covariance matrix estimation with eigenvalue constraints. Journal of Computational and Graphical Statistics, 23(2): 439–459. Markowitz, H. 1952. Portfolio selection. The Journal of Finance, 7(1): 77–91. Rothman, A. J. 2012. Positive deﬁnite estimators of large covariance matrices. Biometrika, 99(3): 733–740. Rothman, A. J.; Levina, E.; and Zhu, J. 2009. Generalized thresholding of large covariance matrices. Journal of the American Statistical Association, 104(485): 177–186. Sch¨afer, J.; and Strimmer, K. 2005. A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics. Statistical Applications in Genetics and Molecular Biology, 4(1).

Tibshirani, R. 1996. Regression shrinkage and selection via the Lasso. Journal of the Royal Statistical Society: Series B (Methodological), 58(1): 267–288. Tran-Dinh, Q.; Kyrillidis, A.; and Cevher, V. 2015. Composite self-concordant minimization. Journal of Machine Learning Research, 16(12): 371–416. Wei, Q.; and Zhao, Z. 2023. Large covariance matrix estimation with oracle statistical rate via Majorizationminimization. IEEE Transactions on Signal Processing, 71: 3328–3342. Witten, D. M.; and Tibshirani, R. 2009. Covarianceregularized regression and classiﬁcation for high dimensional problems. Journal of the Royal Statistical Society Series B: Statistical Methodology, 71(3): 615–636. Xiong, H.; Cheng, W.; Fu, Y.; Hu, W.; Bian, J.; and Guo, Z. 2018. De-biasing covariance-regularized discriminant analysis. In Proceedings of the Twenty-Seventh International Joint Conference on Artiﬁcial Intelligence, IJCAI-18, 2889– 2897. International Joint Conferences on Artiﬁcial Intelligence Organization. Xue, L.; Ma, S.; and Zou, H. 2012. Positive-deﬁnite ℓ1penalized estimation of large covariance matrices. Journal of the American Statistical Association, 107(500): 1480– 1491. Yan, Y.; Yang, Q.; and Zhao, Z. 2025. Large covariance matrix estimation with nonnegative correlations. In Proceedings of The 28th International Conference on Artiﬁcial Intelligence and Statistics, volume 258 of Proceedings of Machine Learning Research, 3502–3510. PMLR. Zhang, C.-H. 2010. Nearly unbiased variable selection under minimax concave penalty. The Annals of Statistics, 38(2): 894–942. Zhao, T.; and Liu, H. 2013. Sparse inverse covariance estimation with calibration. In Advances in Neural Information Processing Systems, volume 26, 2274–2282. Lake Tahoe, Nevada, USA: NeurIPS. Zhao, Z.; and Palomar, D. P. 2018. Mean-reverting portfolio with budget constraint. IEEE Transactions on Signal Processing, 66(9): 2342–2357. Zhao, Z.; Zhou, R.; and Palomar, D. P. 2019. Optimal meanreverting portfolio with leverage constraint for statistical arbitrage in ﬁnance. IEEE Transactions on Signal Processing, 67(7): 1681–1695. Zou, H. 2006. The adaptive Lasso and its oracle properties. Journal of the American Statistical Association, 101(476): 1418–1429.

22903
