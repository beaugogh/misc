---
title: "Efficient Verification and Falsification of ReLU Neural Barrier Certificates"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40890
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40890/44851
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Efficient Verification and Falsification of ReLU Neural Barrier Certificates

<!-- Page 1 -->

Efficient Verification and Falsification of ReLU Neural Barrier Certificates

Dejin Ren1, 2*, Yiling Xue1, 2, 3*, Taoran Wu1, 2, and Bai Xue1, 2, 3†

## 1 Key laboratory of System Software (Chinese Academy of Sciences) and State Key Laboratory of Computer Sciences,

Institute of Software, Chinese Academy of Sciences, Beijing, China 2 University of Chinese Academy of Sciences, Beijing, China 3 School of Advanced Interdisciplinary Sciences, University of Chinese Academy of Sciences, Beijing, China {rendj,xueyl,wutr,xuebai}@ios.ac.cn

## Abstract

Barrier certificates play an important role in verifying the safety of continuous-time systems, including autonomous driving, robotic manipulators and other critical applications. Recently, ReLU neural barrier certificates—barrier certificates represented by the ReLU neural networks—have attracted significant attention in the safe control community due to their promising performance. However, because of the approximate nature of neural networks, rigorous verification methods are required to ensure the correctness of these certificates. This paper presents a necessary and sufficient condition for verifying the correctness of ReLU neural barrier certificates. The proposed condition can be encoded as either a Satisfiability Modulo Theories (SMT) or optimization problem, enabling both verification and falsification. To the best of our knowledge, this is the first approach capable of falsifying ReLU neural barrier certificates. Numerical experiments demonstrate the validity and effectiveness of the proposed method in both verifying and falsifying such certificates.

Code — https://github.com/YilingXue/evf-rnbc Extended version — https://arxiv.org/abs/2511.10015

## Introduction

Safety is a crucial property for continuous-time systems, including autonomous driving, robotic manipulators and other vital applications. Formally, a system is safe if every trajectory starting from the initial set never enters the unsafe set. In practice, a barrier certificate offers a theoretical guarantee of safety. The 0-superlevel (or sublevel) set of a barrier certificate defines a positive invariant set — meaning that trajectories starting within it remain there indefinitely. If this positive invariant set contains the initial set and does not intersect the unsafe set, the safety of the system is ensured.

In recent years, the sum-of-squares (SOS) technique has been widely used to synthesize polynomial barrier certificates for certifying positive invariance (Ames et al. 2019; Clark 2021). However, SOS methods are restricted to polynomial systems and limit the expressive power of the resulting certificates. To address these limitations, barrier certificates

*These authors contributed equally. †Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

defined by neural networks—known as neural barrier certificates—have been introduced (Dawson, Gao, and Fan 2023; Zhao et al. 2020; Qin et al. 2021; Abate et al. 2021; Zhao et al. 2021a; Liu, Liu, and Dolan 2023). Leveraging their universal approximation capability, neural barrier certificates have demonstrated promising performance in applications such as robot control (Dawson et al. 2022; Xiao et al. 2023). Nonetheless, due to the approximate nature of neural networks, they may fail to guarantee positive invariance. Therefore, verification methods are essential to certify the correctness of learned neural barrier certificates.

This paper focuses on the verification and falsification of neural barrier certificates using Rectified Linear Unit (ReLU) activation functions, due to their widespread use in the safe control community (Dawson, Gao, and Fan 2023; Zhao et al. 2021b; Mathiesen, Calvert, and Laurenti 2022). However, ReLU neural barrier certificates are not differentiable, making traditional methods that rely on Lie derivative conditions inapplicable (Dai et al. 2017; Ames et al. 2019). Under the assumption that the derivative of the ReLU activation function is the Heaviside step function (an assumption that lacks mathematical rigor for verifying positive invariance; see the appendix for details), some works (Zhao et al. 2022; Hu et al. 2024) over-approximate the possible values of the Lie derivative and then verify the Lie derivative condition over these over-approximations, leveraging either mixed integer programming (Zhao et al. 2022) or symbolic bound propagation (Hu et al. 2024).

Recently, (Zhang et al. 2023) proposed a necessary and sufficient condition for verifying positive invariance based on the Bouligand tangent cone, which was further used to synthesize ReLU neural barrier certificates in (Zhang et al. 2024). Their condition avoids assuming that the derivative of the ReLU activation is the Heaviside step function. However, the most computationally intensive step in their method is enumerating all possible intersection combinations of linear regions intersecting the boundary of the 0-superlevel set of the ReLU neural barrier certificate. This enumeration procedure has exponential complexity with respect to the number of linear regions containing boundary points (see Remark 2). Additionally, the Bouligand tangent cone condition cannot be encoded exactly as optimization problems due to the presence of strict inequalities (see Remark 4). As a result, the condition must be relaxed to a sufficient one to enable its

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

35767

<!-- Page 2 -->

incorporation into optimization formulations.

In summary, all existing methods for verifying ReLU neural barrier certificates rely on derivative assumption or sufficient conditions, which can be overly conservative and lead to false negatives in practical applications. Moreover, none of these methods can be used for falsification, leaving a critical gap in real-world deployment. In this paper, we propose a novel necessary and sufficient condition for certifying the positive invariance of 0-superlevel sets of continuous piecewise linear functions (CPLFs) under continuous-time systems. This condition is applicable not only to ReLU neural barrier certificates but also to other networks with piecewise linear activation functions, such as leaky ReLU (Maas et al. 2013) and PReLU (He et al. 2015), since these networks are inherently CPLFs. Our proposed condition states that the 0-superlevel set of a CPLF is positively invariant if and only if, in each valid linear region (see Definition 5), the inner product between the region’s linear coefficient vector and the vector field is non-negative. Compared to the condition in (Zhang et al. 2023), our condition requires verification in significantly fewer regions, as it avoids enumerating all possible intersection combinations of linear regions that intersect boundary. This reduction makes the proposed condition more efficient and practical for real-world applications.

We propose a verification algorithm based on our necessary and sufficient condition. The algorithm begins by identifying an initial valid linear region using the Interval Bound Propagation (IBP) technique. Once such a region is found, a boundary propagation algorithm is employed to enumerate all neighboring valid linear regions. By iteratively applying this propagation step, the algorithm ensures that all valid linear regions are covered. For each valid linear region, we can translate the proposed condition into Satisfiability Modulo Theories (SMT) and optimization problems for verifying and falsifying the ReLU neural barrier certificate. Finally, numerical experiments demonstrate the validity and effectiveness of our method in both verification and falsification. The main contributions of this paper are summarized as follows.

• We propose a necessary and sufficient condition for certifying the positive invariance of 0-superlevel sets of CPLFs under continuous-time systems. Unlike (Zhao et al. 2022; Hu et al. 2024), our condition does not rely on the assumption that the derivative of the ReLU activation is the Heaviside step function. Besides, compared to the condition in (Zhang et al. 2023), it significantly reduces the computational complexity of implementation. • The proposed condition can be encoded as SMT and optimization problems, enabling both verification and falsification of ReLU neural barrier certificates. To the best of our knowledge, this is the first method capable of falsifying such certificates.

## Preliminaries

## 2.1 Notation

Rn represents n-dimensional real space; Rm×n represents space of m × n real matrices; N[m,n] represents the nonnegative integers in [m, n]. Vectors and matrices are denoted as boldface lowercase and uppercase respectively. For a vector x, x(i) represents its i-th entry; ∥x∥represents its norm. x · y represents inner product of vectors x and y. For a matrix M, M(i) represents its i-th row vector; rows(M) and cols(M) denote the number of its rows and columns respectively; rank(M) represents the rank of M; [M; x⊤] represents adding x to the last row of M. 0 (or 1) represents the vector (or matrix) whose entries are all zero (or one) with appropriate dimensions in the context. For a set S, its complement, interior, closure, boundary, cardinality and power set are denoted by Sc, Int S, S, ∂S, |S| and 2S, respectively. For two sets S1, S2, S1 \ S2 represents the set {s: s ∈S1∧s /∈S2}. B(x, δ) = {x′ ∈Rn: ∥x′−x∥≤δ} represents the closed δ-ball around the vector x.

## 2.2 ReLU Neural Network

We introduce notations to describe a neural network (NN) with L hidden layers, where the i-th layer contains Mi neurons. Let x ∈Rn denote the input to the network, zij the output of the j-th neuron in the i-th layer, and y the onedimensional network output. We use zi to represent the vector of neuron outputs in the i-th layer. The outputs are computed as zij = σ w⊤ ijx + bij

, i = 1 σ w⊤ ijzi−1 + bij

, 2 ≤i ≤L y = ω⊤zL + ϕ where σ: R →R is the activation function. The input to σ is the pre-activation value to the neuron: for the j-th neuron in the first layer, this value is given by w⊤

1jx + b1j; for the j-th neuron in the i-th hidden layer (i > 1), it is given by w⊤ ijzi−1 + bij. Here, wij ∈Rn when i = 1, and wij ∈RMi−1 when i > 1. Throughout this paper, we assume σ is the ReLU function σ(z) = max{0, z}. The final output of the network is given by y = ω⊤zL + ϕ, where ω ∈RML and ϕ ∈R. A neuron is said to be activated by an input x if its pre-activation value is non-negative, and inactivated if it is non-positive. If the pre-activation value is exactly zero, the neuron is considered both activated and inactivated.

An activation indicator is an L-tuple C = ⟨s1, s2,..., sL⟩, where each si = (si1, si2,..., siMi)⊤is a binary vector of length Mi. Each entry sij ∈{0, 1} indicates whether the j-th neuron in the i-th layer is inactivated (0) or activated (1).

For a given activation indicator C, if an input x activates C, the pre-activation values of all neurons, as well as the overall network output, are affine functions of x. The corresponding affine mapping is determined by C as follows. For the first layer, we define:

¯w1j(C) = w1j, s1j = 1 0, s1j = 0 ¯b1j(C) = b1j, s1j = 1 0, s1j = 0

Then, the output of the j-th neuron in the first layer is given by ¯w1j(C)⊤x + ¯b1j(C). We recursively define ¯wij(C) and ¯bij(C) for i > 1 by letting W i(C) be the matrix whose

35768

<!-- Page 3 -->

columns are ¯wi1(C),..., ¯wiMi(C), and setting:

¯wij(C) =

W i−1(C)wij, sij = 1 0, sij = 0

¯bij(C) = w⊤ ij¯bi−1(C) + bij, sij = 1 0, sij = 0 where ¯bi(C) is the vector of bias terms ¯bij(C) for j = 1,..., Mi. We define w(C) = W L(C)ω and b(C) = ω⊤¯bL(C) + ϕ. Based on these notations, if the input x activates the activation indicator C, the output of each neuron and the final network output are given by: zij =

¯wij(C)⊤x + ¯bij(C) and y = w(C)⊤x + b(C). Next, we characterize the activated region corresponding to a given activation indicator C. Lemma 1 ((Zhang et al. 2023)). Let X(C) denote the set of inputs that activate a particular set of neurons represented by the activation indicator C. For notational consistency, we define W 0(C) as the identity matrix and ¯b0(C) as the zero vector. Then

X(C) =

L \ i=1

Mi \ j=1

{x ∈Rn: w⊤ ij

W i−1(C)⊤x

+¯bi−1

+ bij ≥0, si(j) = 1} ∩

Mi \ j=1

{x ∈Rn:

w⊤ ij

W i−1(C)⊤x + ¯bi−1

+ bij ≤0, si(j) = 0

!

.

The activated region X(C) forms a polyhedron. Let I denote the set of all possible activation indicators. With the above notations, the ReLU neural network can be expressed as a continuous piecewise linear function (CPLF):

y = w(C)⊤x + b(C), x ∈X(C), C ∈I. (1)

Note that I is a finite set, as the number of activated regions is no more than 2

PL i=1 Mi (Montufar et al. 2014).

## 2.3 Positive Invariance and Barrier Certificate In this paper we consider the continuous-time system

˙x = f(x), (2)

with x ∈Rn and f: Rn →Rn locally Lipschitz. For any initial condition x0 ∈Rn, there exists a maximal time interval of existence I(x0) = [0, τmax) such that ϕx0: I(x0) →Rn is the unique solution to system (2), where ϕx0(0) = x0 and τmax is the explosion time with limt→τmax ∥ϕx0(t)∥= +∞. Definition 1 (Positive invariance). A set C ⊆Rn is positively invariant for system (2) if for all x0 ∈C and all t ∈I(x0), the corresponding trajectory satisfies ϕx0(t) ∈C. Definition 2 (Barrier certificate). Given the system (2), let the initial set be SI = {x ∈Rn: hI(x) > 0} and the unsafe set be SU = {x ∈Rn: hU(x) > 0}, where hI, hU are continuous functions, and both SI, SU are nonempty and connected. A barrier certificate for system (2) is a continuous function h: Rn →R whose 0-superlevel set C = {x ∈Rn: h(x) ≥0} satisfies the following conditions:

1. Initial set condition: SI ⊂C. 2. Unsafe set condition: SU ∩C = ∅. 3. Positively invariant condition: C is positively invariant under system (2).

Once a barrier certificate is found, it guarantees that all trajectories starting from the initial set will never enter the unsafe set. A ReLU neural barrier certificate refers to a barrier certificate represented by a neural network with ReLU activation functions. The objective of this paper is to verify or falsify a given ReLU neural barrier certificate.

Remark 1. In fact, it suffices for a single connected component of C to satisfy the three conditions to ensure that all trajectories starting from the initial set will never enter the unsafe set. In the verification algorithm proposed in Sect.4, the boundary propagation algorithm is employed to identify the complete boundary of such a connected component of C.

Tangent Cones and Invariance Conditions Since a ReLU neural network is essentially a CPLF, this section investigates the necessary and sufficient conditions for the positively invariant condition to the 0-superlevel set defined by a CPLF. We begin by reviewing some significant theorems about positive invariance and related foundational concepts.

Definition 3 (Distance). Given a vector space X with norm ∥· ∥, the distance between two points x1, x2 ∈X is d(x1, x2) = ∥x1 −x2∥; the distance between a set S ⊂X and a point x ∈X is d(x, S) = infy∈S ∥x −y∥.

Definition 4 (Tangent cones (Clarke et al. 2008; Aubin and Frankowska 2009)). Let S be a closed subset of the Banach space X.

## 1. The Bouligand tangent cone or contingent cone to S at x, denoted T B

S (x), is defined as follows:

T B

S (x) ≜ v ∈X lim inf t→0+ d(x + tv, S)

t = 0

.

## 2. The Clarke tangent cone or circatangent cone to S at x, denoted T C

S (x), is defined as follows:

T C

S (x) ≜

( v ∈X lim t→0+,x′ S →x d(x′ + tv, S)

t = 0

)

, where x′ S→x means the convergence is in S.

(a) Bouligand tangent cone (b) Clarke tangent cone

**Figure 1.** Illustration of tangent cones at a nonsmooth boundary point.

35769

![Figure extracted from page 3](2026-AAAI-efficient-verification-and-falsification-of-relu-neural-barrier-certificates/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-efficient-verification-and-falsification-of-relu-neural-barrier-certificates/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Both tangent cones in Definition 4 are closed cones. If x ∈Int S, then T B

S (x) = T C

S (x) = X. If x ∈Sc, then T B

S (x) = T C

S (x) = ∅. Therefore, tangent cones are nontrivial only on the boundary ∂S.

The following theorem is quoted from (Clarke et al. 2008) with some modifications for the context of ordinary differential equations instead of differential inclusions.

Theorem 1 ((Clarke et al. 2008, Theorem 3.8 in Chapter 4)). Consider the system (2) and let S ⊂Rn be a closed set, then the following assertions are equivalent: a. S is positively invariant for the system (2); b. for all x ∈∂S, f(x) ∈T B

S (x);

c. for all x ∈∂S, f(x) ∈T C

S (x).

For a CPLF h: Rn →R, its expression can be written as h(x) = w⊤ i x + bi, x ∈Xi, i = 1, · · ·, N, (3)

where Xi = {x: Aix ≤di} is a polyhedron (the background of polyhedron is provided in the appendix) of full dimension, i.e., dim(Xi) = n, referred to as a linear region. The collection {Xi}N i=1 partitions the entire input space Rn, i.e., SN i=1 Xi = Rn, and for all i̸ = j, dim(Xi ∩Xj) ≤n−1. We say Xi and Xj are adjacent if dim(Xi ∩Xj) = n −1. In such a case, there exists a hyperplane H such that Xi ∩Xj ⊆ H, and H ∩Xi and H ∩Xj are facets of Xi and Xj, respectively.

In this paper, we adopt the following assumption, which is also emphasized in (Ames et al. 2016, 2019).

Assumption 1. For a candidate barrier certificate h, its 0superlevel set C = {x ∈Rn: h(x) ≥0} satisfies: ∂C = {x ∈Rn: h(x) = 0}, Int C = {x ∈Rn: h(x) > 0}; C contains interior points and is a regular closed set, i.e., Int C̸ = ∅, Int C = C.

For ease of presentation, we define valid linear regions as follows.

Definition 5 (Valid linear region). A linear region Xi is said to be valid if it is n-dimensional and, for the associated hyperplane Hi = {x ∈Rn: w⊤ i x + bi = 0}, either Hi ∩Int Xi̸ = ∅or Hi ∩Xi is a facet of Xi.

The following two propositions respectively characterize the Bouligand tangent cone and the Clarke tangent cone to the set C.

Proposition 1. Given a CPLF h as defined in (3), consider its 0-superlevel set C = {z ∈Rn: h(z) ≥0}. Under Assumption 1, the following assertions hold for any x ∈∂C:

1. if x ∈Int Xi, i = 1, · · ·, N, then

T B

C (x) = {v ∈Rn: w⊤ i v ≥0}; (4)

2. if x ∈Tm k=1 Xik and x̸ ∈Rn \ Sm k=1 Xik, i1, · · ·, im ∈ {1, 2, · · ·, N}, then

T B

C (x) = m [ k=1

{v ∈Rn:

^ j∈E

Aik(j)v ≤0 ∧w⊤ ikv ≥0},

(5)

T B

C (x) ⊃{v ∈Rn:

^ k∈I w⊤ ikv ≥0}, (6)

where the set E, I are defined as E ≜ {j ∈ {1, · · ·, rows(A)}: Aik(j)x = dik(j)}, I ≜{k ∈ {1, · · ·, m}: Xik is a valid linear region}. 3. ∂C ⊂ S l∈J Xl, where J ≜ {l ∈ {1, · · ·, N}: Xl is a valid linear region}.

Proposition 2. Given a CPLF h as defined in (3), let C = {z ∈Rn: h(z) ≥0} denote its 0-superlevel set. Under Assumption 1, the Clarke tangent cone to C at any point x ∈∂C is given by

T C

C (x) =

    

   

{v ∈Rn: w⊤ i v ≥0}, if x ∈Int Xi, i = 1, · · ·, N {v ∈Rn: V k∈I w⊤ ikv ≥0}, if x ∈Tm k=1 Xik ∧x̸ ∈Rn \ Sm k=1 Xik

(7)

where i1, · · ·, im ∈{1, 2, · · ·, N}, I = {k ∈{1, · · ·, m}: Xikis a valid linear region}.

Based on the equivalence of assertions (a) and (c) in Theorem 1, the necessary and sufficient condition for the positive invariance of the 0-superlevel set of a CPLF under system (2) is established in Theorem 2. Theorem 2. Consider the system (2) and the set C = {x ∈ Rn: h(x) ≥0}, where h is a CPLF as defined in (3). Under Assumption 1, the set C is positively invariant for the system (2) if and only if, for each valid linear region Xi, w⊤ i f(x) ≥0, ∀x ∈∂C ∩Xi. (8)

Recall that a ReLU neural network is essentially a CPLF. By applying Theorem 2 and using the notations introduced in Section 2.2, we derive the necessary and sufficient condition for the positive invariance of the 0-superlevel set represented by a ReLU neural network under system (2). Theorem 3. Consider the system (2) and the set C = {x ∈ Rn: h(x) ≥0}, where h is a ReLU neural network as described in Section 2.2. Under Assumption 1, the set C is positively invariant for system (2) if and only if, for each activation indicator C such that X(C) is a valid linear region, w(C)⊤f(x) ≥0, ∀x ∈∂C ∩X(C). (9)

Remark 2. In fact, with the equivalence of assertions (a) and (b) in Theorem 1, one can also derive a necessary and suffi- cient condition for the positive invariance of the 0-superlevel set of a ReLU neural network, as investigated in (Zhang et al. 2023). However, compared to our condition in Theorem 3, the condition in (Zhang et al. 2023) has to additionally enumerate all possible intersection combinations of activated regions X(C) that intersect the boundary ∂C, which significantly increases computational complexity. For instance, if there are n activated regions X(C1), · · ·, X(Cn) with a nonempty intersection Tn k=1 X(Ck)̸ = ∅, the total number of intersection combinations among these regions is Pn k=1 n k

= 2n −1. However, according to Definition 5, the number of valid linear regions that must be enumerated in our method is fewer than n.

35770

<!-- Page 5 -->

## 4 Verification Algorithm

In this section we present our verification algorithm based on the necessary and sufficient condition in Theorem 3. The algorithm proceeds in three steps: we first search for an initial valid linear region (Sect. 4.1); using this initial region, the boundary propagation algorithm enumerates all valid linear regions, i.e., compute A ≜{C: X(C) is a valid linear region} (Sect. 4.2); finally, for each valid activation indicator C ∈ A, we verify whether w(C)⊤f(x) ≥0 holds for all x ∈∂C ∩X(C) (Sect. 4.3). If this condition holds for every C ∈A, then C is positively invariant for system (2); otherwise, if any C ′ ∈A violates the condition, C is not positively invariant. Figure 2 illustrates the procedure of enumerating all valid linear regions.

**Figure 2.** Illustration of enumerating valid linear regions: We begin by randomly selecting two points—one from the initial set (colored in green) and one from the unsafe set (colored in red)—and iteratively shrinking the segment connecting them until an initial valid linear region is found. The boundary propagation algorithm then expands from this region to identify neighboring valid linear regions. By iteratively applying this propagation step, the algorithm eventually enumerates all valid linear regions.

## 4.1 Searching for an Initial Valid Linear Region

We use the following procedure to search for an initial valid linear region.

1. Randomly select points until two points x1, x2 are found such that h(x1)h(x2) < 0. For example, x1 can be sampled from the unsafe set and x2 from the initial set. 2. Utilize the method of the bisection to shrink the length of the line segment {tx1 + (1 −t)x2: 0 ≤t ≤1}, until ∥x1 −x2∥≤ϵ, where ϵ > 0 is a predefined threshold. Specifically, suppose initially h(x1) < 0, h(x2) > 0, if h(x1+x2

2) < 0, then x1:= x1+x2

2, else x2:= x1+x2

2. 3. Compute the interval hull IntHull({x1, x2}) of x1 and x2, and use Interval Bound Propagation (IBP) to determine the candidate activation indicator C ′. For each neuron j in layer i with input interval [l1, l2]:

– if l1 > 0, set si(j):= 1; – if l2 < 0, set si(j):= 0; – else, set si(j):= −1.

4. Generate all feasible activation indicators C from C ′ by replacing each −1 in si(j) with both 1 and 0. 5. For each feasible activation indicator C, check whether X(C) passes the Valid Test below. If a valid indicator is found, denote it by C0, and take the corresponding region X(C0) as the initial valid linear region.

Valid Test When X(C) is an n-dimensional valid linear region, it follows that dim(∂C ∩X(C)) = n −1. Therefore, the validity of X(C) can be verified by checking whether this dimensional condition holds. Note that the redundant case where ∂C ∩X(C) = X(C) can also be included, but this does not affect the correctness of our method.

Given an activated region of the form X(C) = {x ∈ Rn: Ax ≤d}, define the set P = ∂C ∩X(C) and let

˜ A = [A; w⊤(C); −w⊤(C)], ˜d = [d; −b(C); b(C)], then P = {x ∈Rn: ˜ Ax ≤˜d} is also a polyhedron. In a system of linear inequalities Ax ≤d, the inequality A(j)x ≤ d(j), j ∈{1, · · ·, rows(A)}, is called an implicit equality if A(j)x = d(j) holds for all solutions of the system Ax ≤ d. We denote by A=x ≤d= the system consisting of all implicit equalities within Ax ≤d.

To identify the implicit equalities in P = {x ∈Rn: ˜ Ax ≤˜d}, we solve the following pair of LPs for each row j = 1, · · ·, rows(˜ A):

min x

˜ A(j)x max x

˜ A(j)x s.t. ˜ Ax ≤˜d s.t. ˜ Ax ≤˜d

If the optimal values of both LPs are equal, then ˜ A(j)x ≤ ˜d(j) is an implicit equality. According to (Conforti, Cornuéjols, and Zambelli 2014, Theorem 4.17), the dimension of P satisfies dim(P) = n −rank(˜ A=). Therefore, if rank(˜ A=) = 1, then dim(P) = n −1.

## 4.2 Boundary Propagation Algorithm

Next we introduce the boundary propagation algorithm, which can enumerate all valid activation indicators, i.e., the set A ≜{C: X(C) is a valid linear region}. This algorithm proceeds as follows:

1. Initialize the set of valid activation indicators as A:= {C0} and the visited set as B:= ∅. 2. Select an activation indicator C in A \ B and add C to B. For each j = 1, · · ·, rows(A), solve the following LP feasibility problem to find the facet of X(C) which has the intersection with ∂C.

 

 w(C)⊤x + b(C) = 0 A(j)x = d(j) A(k)x ≤d(k), k ∈{1, · · ·, rows(A)} \ {j}

If the above LP feasibility problem admits a feasible solution x⋆, then enumerate all feasible activation indicators that are activated by x⋆. For each indicator that passes the Valid Test, add it to the set A. 3. The algorithm terminates when A = B, meaning all valid activation indicators have been explored and no new ones have been found.

Remark 3. When the system dimension is 2, the number of facets of X(C) that intersect ∂C is at most 4. Therefore once four such facets have been identified, it is unnecessary to examine the remaining facets.

35771

![Figure extracted from page 5](2026-AAAI-efficient-verification-and-falsification-of-relu-neural-barrier-certificates/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

For ReLU neural networks, the partitioning of the input space exhibits a special structure: every n-dimensional linear region shares a facet with each of its adjacent linear regions. This property arises from the fact that the partitioning is generated through a sequence of hyperplanes, layer by layer (Raghu et al. 2017; Serra, Tjandraatmadja, and Ramalingam 2018). Moreover, since ∂C is contained within the union of valid linear regions (see Proposition 1), if we further assume that ∂C is connected, then given an initial valid linear region, one can examine its facets to identify those intersecting the boundary. By recursively expanding to adjacent regions via these shared facets, we can enumerate all valid linear regions. The following theorem formalizes this claim.

Theorem 4. Assuming that ∂C is connected, the boundary propagation algorithm can identify all valid linear regions.

## 4.3 Verification and Falsification in Each Valid Linear Region

After enumerating all valid linear regions, we can verify or falsify the three conditions in Definition 2 within each valid linear region.

the Positively Invariant Condition The necessary and sufficient condition in Theorem 3 can be described as a quantified formula:

∀C ∈A, ∀x x ∈∂C ∩X(C) →w(C)⊤f(x) ≥0

.

(10) We can translate (10) into an SMT problem that determines whether the following quantifier-free formula with Disjunctive Normal Form (DNF) is satisfiable (SAT) or not (UNSAT).

_

C ∈A w(C)⊤x + b(C) = 0 ∧x ∈X(C)

∧w(C)⊤f(x) < 0

.

(11)

If the SMT problem (11) is proven to be UNSAT, then the Boolean value of (10) is true, implying that C is positively invariant under system (2). When the system (2) is polynomial, the SMT (11) can be solved using an SMT solver that employs Cylindrical Algebraic Decomposition (Caviness and Johnson 2012), such as Z3 (De Moura and Bjørner 2008). In this case, verification by solving (11) is both sound and complete: an UNSAT return implies positive invariance of C, while a SAT return indicates the falsification of positive invariance. When the system (2) is non-polynomial, we can use dReal (Gao, Kong, and Clarke 2013), an SMT solver that supports non-polynomial functions such as trigonometric and exponential functions. dReal employs δ-complete decision procedures, returning either UNSAT or δ-SAT, where δ is a user-specified numerical error bound. Therefore, positive invariance verification using dReal is sound: when dReal returns UNSAT for SMT (11), C is positively invariant. However, a “δ-SAT” result does not necessarily falsify positive invariance due to potential numerical errors.

The quantified formula (10) can also be described as a series of optimization problems: for each valid linear region

X(C), C ∈A, we solve the following optimization.

min x w(C)⊤f(x)

s.t.

w(C)⊤x + b(C) = 0, x ∈X(C).

(12)

If the optimal value of (12) is non-negative, the positive invariant condition is satisfied for C. When all activation indicators in A pass the verification, we can deduce that C is positively invariant for system (2); otherwise, it is not. When the system (2) is linear, the optimization is an LP. If the optimal value of (12) exists, it can be obtained by the simplex method or interior-point method. In contrast, when the system (2) is nonlinear, the optimization (12) may be nonconvex, making it challenging to obtain the optimal value. Nevertheless, we can utilize (12) to falsify the positive invariance. Specifically, if there exists a valid linear region X(C), C ∈A such that (12) yields a negative feasible value, then C is not positively invariant.

Remark 4. The condition based on the Bouligand tangent cone cannot be directly translated into a series of optimization problems, in contrast to condition derived from the Clarke tangent cone. This limitation arises from the presence of strict inequalities — specifically, the restriction “for x ∈Int Xi (Aix < di)” in the first assertion of Proposition 1 — which are not permitted in standard optimization formulations. The detailed explanation can be found in the appendix.

the Initial and Unsafe Set Conditions We can also encode the verification of the initial and unsafe set conditions as SMT and optimization problems like the positively invariant condition. To this end, we introduce the following propositions, which provide necessary and sufficient conditions.

Proposition 3. SI ⊂C if and only if SI ∩∂C = ∅and SI ∩Int C̸ = ∅.

Proposition 4. SU ∩C = ∅if and only if SU ∩∂C = ∅and SU ∩Cc̸ = ∅.

The condition SI ∩∂C = ∅can also be described as a quantified formula:

∀C ∈A, ∀x (x ∈∂C ∩X(C) →hI(x) ≤0). (13)

Similar to the positive invariant condition, the quantified formula (13) can be encoded into SMT and optimization problems. For simplicity, we present the details in the appendix.

To verify SI ∩Int C̸ = ∅, we can randomly select a point x ∈SI and check whether hI(x) > 0. If both conditions are satisfied, we conclude that SI ⊂C. Otherwise, the verification fails.

Note that the condition in Proposition 4 for verifying the unsafe set condition SU ∩C = ∅is analogous to that used for verifying the initial set condition. Therefore, a similar verification procedure can be applied to the unsafe set condition as well.

35772

<!-- Page 7 -->

## 5 Experiments

In this section, we evaluate the proposed method to demonstrate the validity and effectiveness of our verification algorithm. Specifically, we conduct experiments on four systems: Arch3, Complex, Linear4d, and Decay. Among them, Linear4d is a linear system, while the others are nonlinear. System descriptions, experimental settings, and detailed experimental results are provided in the appendix.

For linear systems, we only solve the optimization problem (12) to check the positive invariant condition, as it reduces to an LP whose optimal value can be reliably obtained when it exists. For nonlinear systems, we first solve the optimization (12). If there exists a valid linear region for which the suboptimal value is negative, then the positive invariant condition is falsified. Otherwise, if all instances of (12) yield nonnegative suboptimal values for each C ∈A, we proceed to solve the SMT problem (11) using the dReal solver (Gao, Kong, and Clarke 2013). If dReal returns UNSAT for every region, positive invariance is verified. However, if it returns δ-SAT for any region, the validity of the certificate remains inconclusive. The same procedure is applied to verify the initial set and unsafe set conditions.

We compare our method with that in (Zhang et al. 2023), as it is, to the best of our knowledge, the only method that does not rely on the Heaviside step function assumption for the derivative of the ReLU activation. Notably, our method supports both verification and falsification of barrier certificates, whereas the method in (Zhang et al. 2023) only performs verification. Consequently, if a certificate fails their test, no conclusion can be drawn about its correctness. Furthermore, the correctness guarantees in (Zhang et al. 2023) hold only if the solver returns optimal solutions for all underlying optimization problems. In practice, however, solvers often yield suboptimal results in nonlinear programming, potentially undermining the reliability of their verification.

The running time and validity of barrier certificates for each case are summarized in Table 1. Our method successfully verifies or falsifies all cases, whereas the approach in (Zhang et al. 2023) can only verify five out of seven barrier certificates in the two-dimensional system Arch3. In other cases, it either returns “unknown” or crashes due to memory exhaustion. Furthermore, their results are reliable only when all underlying optimization problems can be solved to optimality by the solvers, which is difficult to rigorously ver-

(a) (b)

**Figure 3.** Enumerated valid linear regions and the vector field of system Arch3.

Case HNN tour tZ Vour VZ

Arch3

(2-d) (nonlinear)

32 3.89 24.10 ✓ ✓ 64 28.40 141.01 ✓ ✓ 96 94.75 528.36 ✓ ✓ 128 204.78 198.17 ✗? 32-32 19.75 41.10 ✓ ✓ 64-64 215.99 283.00 ✓ ✓ 96-96 774.27 1644.60 ✗?

Complex

(3-d) (nonlinear)

32 5.29 135.22 ✓? 64 92.36 698.35 ✓? 96 469.53 1377.00 ✓? 32-32 79.57 1132.23 ✓? 64-64 500.08 − ✗ − 96-96 19686.48 − ✓ −

Linear4d

(4-d) (linear)

16 9.61 286.46 ✓? 32 88.12 1110.54 ✓? 48 9992.90 − ✓ − 8-8 7.84 212.19 ✓? 12-12 55.05 593.78 ✓? 16-16 524.73 2243.71 ✗? 24-24 22571.44 − ✗ −

Decay

(6-d) (nonlinear)

20 19842.22 − ✓ − 8-8 347.72 4381.28 ✓? 10-10 1953.08 4035.94 ✗? 12-12 31112.56 − ✗ −

**Table 1.** The first two columns list the system names and neural network architectures (HNN denotes the number of neurons per hidden layer). We report the running time and certificate validity of our method as tour and Vour, and use tZ and VZ for the results of (Zhang et al. 2023). A dash (−) indicates a program crash. A ✓denotes verification (✓ indicates verification under the assumption that all underlying optimization problems can be solved to optimality), ✗denotes falsification, and? indicates unknown validity.

ify in nonlinear programming. In terms of running time, our method consistently outperforms theirs, particularly in highdimensional systems. This improvement stems from the fact that our algorithm enumerates far fewer regions than (Zhang et al. 2023), as discussed in Remark 2. Figure 3 illustrates the valid linear regions enumerated by our boundary propagation algorithm for the first barrier certificate in system Arch3.

## 6 Conclusion

In this paper, we proposed a necessary and sufficient condition for verifying ReLU neural barrier certificates and developed a corresponding algorithm that supports both verification and falsification. To the best of our knowledge, this is the first method capable of falsifying ReLU neural barrier certificates, thereby filling a critical gap for their reliable application in safety-critical systems. Through numerical experiments, we demonstrated that our method achieves superior verification performance compared to existing approaches, particularly in high-dimensional systems.

35773

![Figure extracted from page 7](2026-AAAI-efficient-verification-and-falsification-of-relu-neural-barrier-certificates/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-verification-and-falsification-of-relu-neural-barrier-certificates/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## References

Abate, A.; Ahmed, D.; Edwards, A.; Giacobbe, M.; and Peruffo, A. 2021. FOSSIL: a software tool for the formal synthesis of lyapunov functions and barrier certificates using neural networks. In Proceedings of the 24th international conference on hybrid systems: computation and control, 1– 11. Ames, A. D.; Coogan, S.; Egerstedt, M.; Notomista, G.; Sreenath, K.; and Tabuada, P. 2019. Control barrier functions: Theory and applications. In 2019 18th European control conference (ECC), 3420–3431. IEEE. Ames, A. D.; Xu, X.; Grizzle, J. W.; and Tabuada, P. 2016. Control barrier function based quadratic programs for safety critical systems. IEEE Transactions on Automatic Control, 62(8): 3861–3876. Aubin, J.-P.; and Frankowska, H. 2009. Set-valued analysis. Springer Science & Business Media. Caviness, B. F.; and Johnson, J. R. 2012. Quantifier elimination and cylindrical algebraic decomposition. Springer Science & Business Media. Clark, A. 2021. Verification and synthesis of control barrier functions. In 2021 60th IEEE Conference on Decision and Control (CDC), 6105–6112. IEEE. Clarke, F. H.; Ledyaev, Y. S.; Stern, R. J.; and Wolenski, P. R. 2008. Nonsmooth analysis and control theory, volume 178. Springer Science & Business Media. Conforti, M.; Cornuéjols, G.; and Zambelli, G. 2014. Integer Programming. Graduate Texts in Mathematics. Springer International Publishing. ISBN 9783319110080. Dai, L.; Gan, T.; Xia, B.; and Zhan, N. 2017. Barrier certificates revisited. Journal of Symbolic Computation, 80: 62–86. Dawson, C.; Gao, S.; and Fan, C. 2023. Safe control with learned certificates: A survey of neural lyapunov, barrier, and contraction methods for robotics and control. IEEE Transactions on Robotics, 39(3): 1749–1767.

Dawson, C.; Qin, Z.; Gao, S.; and Fan, C. 2022. Safe nonlinear control using robust neural lyapunov-barrier functions. In Conference on Robot Learning, 1724–1735. PMLR. De Moura, L.; and Bjørner, N. 2008. Z3: An efficient SMT solver. In International conference on Tools and Algorithms for the Construction and Analysis of Systems, 337–340. Springer. Gao, S.; Kong, S.; and Clarke, E. M. 2013. dReal: An SMT solver for nonlinear theories over the reals. In International conference on automated deduction, 208–214. Springer. He, K.; Zhang, X.; Ren, S.; and Sun, J. 2015. Delving deep into rectifiers: Surpassing human-level performance on imagenet classification. In Proceedings of the IEEE international conference on computer vision, 1026–1034. Hu, H.; Yang, Y.; Wei, T.; and Liu, C. 2024. Verification of neural control barrier functions with symbolic derivative bounds propagation. In 8th Annual Conference on Robot Learning.

Liu, S.; Liu, C.; and Dolan, J. 2023. Safe control under input limits with neural control barrier functions. In Conference on Robot Learning, 1970–1980. PMLR. Maas, A. L.; Hannun, A. Y.; Ng, A. Y.; et al. 2013. Rectifier nonlinearities improve neural network acoustic models. In Proc. icml, volume 30, 3. Atlanta, GA. Mathiesen, F. B.; Calvert, S. C.; and Laurenti, L. 2022. Safety certification for stochastic systems via neural barrier functions. IEEE Control Systems Letters, 7: 973–978. Montufar, G. F.; Pascanu, R.; Cho, K.; and Bengio, Y. 2014. On the number of linear regions of deep neural networks. Advances in neural information processing systems, 27.

Qin, Z.; Zhang, K.; Chen, Y.; Chen, J.; and Fan, C. 2021. Learning safe multi-agent control with decentralized neural barrier certificates. arXiv preprint arXiv:2101.05436. Raghu, M.; Poole, B.; Kleinberg, J.; Ganguli, S.; and Sohl- Dickstein, J. 2017. On the expressive power of deep neural networks. In international conference on machine learning, 2847–2854. PMLR. Serra, T.; Tjandraatmadja, C.; and Ramalingam, S. 2018. Bounding and counting linear regions of deep neural networks. In International conference on machine learning, 4558–4566. PMLR. Xiao, W.; Wang, T.-H.; Hasani, R.; Chahine, M.; Amini, A.; Li, X.; and Rus, D. 2023. Barriernet: Differentiable control barrier functions for learning of safe robot control. IEEE Transactions on Robotics, 39(3): 2289–2307.

Zhang, H.; Qin, Z.; Gao, S.; and Clark, A. 2024. SEEV: Synthesis with Efficient Exact Verification for ReLU Neural Barrier Functions. arXiv preprint arXiv:2410.20326. Zhang, H.; Wu, J.; Vorobeychik, Y.; and Clark, A. 2023. Exact verification of relu neural control barrier functions. Advances in neural information processing systems, 36: 5685–

5705. Zhao, H.; Zeng, X.; Chen, T.; and Liu, Z. 2020. Synthesizing barrier certificates using neural networks. In Proceedings of the 23rd international conference on hybrid systems: Computation and control, 1–11. Zhao, H.; Zeng, X.; Chen, T.; Liu, Z.; and Woodcock, J. 2021a. Learning safe neural network controllers with barrier certificates. Formal Aspects of Computing, 33: 437–455. Zhao, Q.; Chen, X.; Zhang, Y.; Sha, M.; Yang, Z.; Lin, W.; Tang, E.; Chen, Q.; and Li, X. 2021b. Synthesizing ReLU neural networks with two hidden layers as barrier certificates for hybrid systems. In Proceedings of the 24th International Conference on Hybrid Systems: Computation and Control, 1–11. Zhao, Q.; Chen, X.; Zhao, Z.; Zhang, Y.; Tang, E.; and Li, X. 2022. Verifying neural network controlled systems using neural networks. In Proceedings of the 25th ACM International Conference on Hybrid Systems: Computation and Control, 1–11.

35774
