---
title: "Universal Learning of Stochastic Dynamics for Exact Belief Propagation Using Bernstein Normalizing Flows"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40984
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40984/44945
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Universal Learning of Stochastic Dynamics for Exact Belief Propagation Using Bernstein Normalizing Flows

<!-- Page 1 -->

Universal Learning of Stochastic Dynamics for Exact Belief Propagation Using

Bernstein Normalizing Flows

Peter Amorese and Morteza Lahijanian

Deptartment of Aerospace Engineering Sciences, University of Colorado Boulder, USA

Peter.Amorese@colorado.edu, Morteza.Lahijanian@colorado.edu

## Abstract

Predicting the distribution of future states in a stochastic system, known as belief propagation, is fundamental to reasoning under uncertainty. However, nonlinear dynamics often make analytical belief propagation intractable, requiring approximate methods. When the system model is unknown and must be learned from data, a key question arises: can we learn a model that (i) universally approximates general nonlinear stochastic dynamics, and (ii) supports analytical belief propagation? This paper establishes the theoretical foundations for a class of models that satisfy both properties. The proposed approach combines the expressiveness of normalizing flows for density estimation with the analytical tractability of Bernstein polynomials. Empirical results show the efficacy of our learned model over state-of-the-art data-driven methods for belief propagation, especially for highly non-linear systems with non-additive, non-Gaussian noise.

Code — https:

//github.com/peteramorese/BernsteinFlow/tree/anony-zip Extended version — https://arxiv.org/abs/2509.15533

## Introduction

At the heart of intelligent reasoning under uncertainty is the ability to predict future random outcomes. Prediction accuracy has profound implications for the safety and effectiveness of real-world systems. Achieving accurate and informative predictions requires both a representative model of the underlying stochastic process and a principled method for reasoning with that model. When the model is known but nonlinear (or non-Gaussian), reasoning, specifically predicting the future state distribution, known as belief propagation, becomes analytically intractable and typically necessitates approximation. When the underlying dynamics are unknown, machine learning provides a data-driven means to model them. However, the choice of learning model should not only aim for expressive power but also support the type of reasoning required. In the case of belief propagation, this leads to a central question: Can we learn a model that (i) universally approximates general nonlinear stochastic dynamics, and (ii) supports analytical belief propagation?

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

This work focuses on the above question and lays the theoretical groundwork for a class of general nonlinear models capable of learning complex stochastic systems while supporting analytical belief propagation. The key insight is that, under a Bayesian (Markov chain) framework, belief propagation reduces to two fundamental operations, multiplication and integration, over two functions: the prior and the conditional probability density functions (PDFs). If these functions are represented as polynomials, these operations remain exact, since polynomials are closed under both multiplication and integration. This eliminates the need for approximation during propagation. Building on this observation, we develop a learning framework in which polynomials are trained to soundly represent true PDFs, i.e., non-negative functions that integrate to one over their domain. Specifically, in our approach, dubbed Bernstein Normalizing Flows (BNFs), the underlying PDFs are modeled using Bernstein polynomials, which offer both favorable analytical properties and universal approximation capabilities. However, polynomials alone are ill-suited for modeling PDFs over unbounded state spaces. To overcome this limitation, we leverage insights from normalizing flows (Papamakarios et al. 2021) to enable proper universal density estimation with polynomials. Hence, by embedding Bernstein polynomials in the normalizing flow architecture, we obtain models that can approximate arbitrary nonlinear stochastic systems while supporting efficient and exact belief propagation.

To the best of our knowledge, the proposed BNF framework is the first class of general nonlinear Markov chain models that simultaneously support universal approximation of stochastic dynamics and exact analytical belief propagation. Beyond the introduction of BNFs, this work makes three key contributions: (i) an explicit-constraint-free training procedure for learning valid PDFs, (ii) a method for enhancing model expressiveness without increasing the number of parameters, and (iii) empirical validation demonstrating the effectiveness of BNFs for belief propagation in comparison with state-of-the-art data-driven approaches.

## Related Work

Belief propagation in nonlinear stochastic systems is a fundamental challenge in probabilistic reasoning and control. A variety of approximate methods have been developed to handle this task, particularly in the contexts of filtering, density estimation, and probabilistic modeling.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

36610

<!-- Page 2 -->

These approaches vary in their trade-offs between accuracy, tractability, and the ability to provide formal guarantees.

Approximate belief propagation has been extensively studied in the context of nonlinear filtering (Schei 1997; Julier and Uhlmann 2004). Gaussian Mixture Models (GMMs) are commonly used to represent multimodal beliefs (Alspach and Sorenson 2003) while preserving some analytical tractability, such as efficient sampling and region-based integration, features valuable for planning. However, linearization-based methods like the Extended Kalman Filter (EKF) (Jazwinski 2013) introduce significant error under nonlinear dynamics. Component splitting techniques (Kulik and LeGrand 2024) mitigate this by recursively subdividing GMM components, but the resulting exponential growth in components renders long-horizon prediction intractable. These filtering approaches also typically assume additive Gaussian noise, making Gaussian Process (GP) regression a common choice for learning system dynamics (Deisenroth et al. 2011).

Monte Carlo methods (Djuric et al. 2003) offer a flexible alternative by representing beliefs with particle sets. Propagation is straightforward if state transitions can be sampled, but obtaining a usable PDF requires post-hoc density estimation. These methods are also prone to inaccuracies in low-sample regions and lack formal error bounds. In contrast to the approximate methods, our approach performs analytical belief propagation. Similar to GP regression with GMM propagation, our model can evaluate probabilistic future events, and easily draw samples from the current belief.

Several works have aimed to provide formal error bounds on belief propagation. For instance, Polymenakos et al. (2020) derive bounds for GP models, while grid-based techniques generalize formal GMM propagation to broader nonlinear systems (Figueiredo et al. 2024), albeit under restrictive assumptions (e.g., diagonal-covariance GMM approximations). Moment-based propagation methods also exist (Jasour, Wang, and Williams 2021), but moments alone are often insufficient to fully recover the underlying distribution (Akhiezer 2020). Unlike these methods, our approach does not assume a given model; instead, we focus on learning a model that supports exact belief propagation, eliminating the need for bounding the approximation error entirely.

Polynomials have long been used for density estimation (Yu and Loskot 2023) due to their normalization convenience. Bernstein polynomials, in particular, have been applied to smooth approximations of empirical distributions and in nonparametric settings (Babu, Canty, and Chaubey 2002; Belalia, Bouezmarni, and Leblanc 2017), though often via kernelbased methods. Sampling from general multivariate polynomial densities remains a challenge. Our work addresses this by embedding Bernstein polynomials within a normalizing flow architecture. Univariate Bernstein polynomials have been used in normalizing flows in conjunction with neural networks for robustness and interpretability (Ramasinghe et al. 2022; Arpogaus et al. 2025). However, due to the neural network, the modeled density is not a polynomial. In contrast, our proposed model is entirely polynomial, enabling efficient sampling, maintaining model sparsity, and supporting exact belief propagation.

Notation Throughout the paper, bold symbols denote vectors, e.g., x = [x1,..., xn] ∈Rn, and polynomial functions are denoted as π(x). Given a random variable x, its probability density function (PDF), which we also refer to as density, is denoted p(x), and the probability of x being in region R ⊆Rn is denoted P(x ∈ R). Multivariate polynomials (e.g., in the monomial-basis) π(x) = Pd1 j1=0 · · · Pdn jn=0 cj1,···,jnxj1

1 · · · xjn n are denoted with multi-indices π(x) = Pd j=0 cjxj, and the set of corresponding coefficients is denoted in bold as c. The set of all degree-d polynomials is denoted Πd[x]. For a vector-valued function f(x), the i-th component is denoted fi(x). If f depends only on the first l ≤n components of x, we denote this by writing f(x≤l). If f depends only on the i-th component of x, we use f(xi). Finally, the image of region R via mapping f is denoted f(R):= {f(x) | x ∈R}.

## Problem Formulation

Consider a discrete-time, non-linear stochastic dynamical system of the form xk+1 = f(xk, vk) (1) where xk ∈X ⊆Rn is the state, and vk ∼p(v) is a stochastic process noise variable. We assume function f is continuous and differentiable, and the initial state x0 ∼p(x0) is random. This work considers a state space X that is either unbounded, i.e., X = Rn, or bounded hyperrectangular, i.e., X = Śn i=1 Ii for some closed intervals Ii ⊂R. The dynamics of System (1) can be equivalently represented by the state-transition distribution p(xk | xk−1) = f(xk−1, ·)#p(v) (2) where # denotes the push-forward operator. This representation, which implicitly captures the non-linear dependence of f on xk and vk, may be very complex for highly non-linear systems. For ease of presentation, we denote this distribution as p(x′ | x). Hence, the stochastic evolution of the system (1) from the initial distribution p(x0) is captured by a continuousstate Markov chain Mf = (X, p(x0), p(x′ | x)).

We consider a scenario where both the dynamics f and the initial state distribution (belief) p(x0) are unknown and must be learned from data. Specifically, we assume data is provided in the form of state input-output pairs Dx′ = {(ˆx, ˆx′)i}N i=1, where ˆx ∈X is a point and ˆx′ = f(ˆx, v) for a realization of v, and initial states Dx0 = {(ˆx0)i}N0 i=1 for N, N0 ∈N. We are interested in belief propagation, i.e., representing the (marginal) state distribution p(xK), also referred to as the belief of the state at some future time K ∈N, and probabilistic reachability of a region of interest R ⊂X at time step K, i.e., P(xK ∈R), subject to starting at the initial belief p(x0). Using the Markov chain Mf, the belief can be propagated recursively for k = 1,..., K, using:

p(xk) =

Z xk−1 p(xk | xk−1)p(xk−1)dxk−1. (3)

Once p(xK) is constructed, then, the probabilistic reachability is given by

P(xK ∈R) =

Z

R p(xK)dxK. (4)

36611

<!-- Page 3 -->

We refer to (4) as belief evaluation.

Challenges The analytical feasibility of the integral operations described by (3) and (4) is critically dependent on the coupling between the functional form of both distributions p(xk) and p(x′ | x). In fact, for most known systems that have non-linear dynamics, or even linear f but non-Gaussian p(v), propagation via (3) is analytically infeasible, necessitating approximation.

Since both p(x0) and p(x′ | x) are unknown and must be learned, the following question arises: Is there a functional form for p(xk) and p(xk | xk−1) that can model general non-linear stochastic dynamics such that (3) and (4) become analytically tractable? To rigorously differentiate such desireable models from linear-Gaussian models, or even non-linear models that assume additive-Gaussian noise, we define a universal distribution approximator.

Definition 1 (Universal Distribution Approximator). Let P be the set of all continuous PDFs supported on a compact bounded support X ⊂Rn, i.e., p(x) > 0 for all p ∈P, x ∈X. Let Pθ be a family of distributions parameterized by a set of parameters θ where |θ| < ∞. Then, under any probability divergence D(·||·), pθ ∈Pθ is said to be universal if for any p ∈P and ϵ > 0, if there exists a θ such that D(p||pθ) < ϵ.

Definition 1 can be easily extended to describe universal conditional PDF approximators by asserting that pθ(x | y) is universal for all y in a compact bounded region Y.

This work tackles the challenge of choosing a functional form for learning an arbitrary Markov chain Mf subject to:

C1. pθ(x0) and pθ(xk | xk−1) are universal, C2. pθ(xk) can be computed exactly via (3), and C3. P(xk ∈R) can be computed exactly via (4) for any

. hyper-rectangle R ⊂X.

Hence, the belief propagation and evaluation problem that we consider is as follows.

Problem 1. Given datasets Dx0 and Dx′ generated from the stochastic System (1) and a time horizon K ∈N, learn a Markov chain Mf that adheres to conditions C1-C3, and compute the distribution p(xK).

## Approach

Overview Ensuring that all three constraints hold poses a challenging functional representation problem. Recall that the recursive operation in (3) involves multiplication and marginalization, while (4) requires definite integration. Among common function classes, polynomials are one of the few that are closed under these operations and are also known for their strong approximation capabilities. We leverage these properties to address Problem 1.

In the remainder of the paper, all probability densities pθ(·) assumed to be parameterized models. For notational simplicity, we omit the subscript θ. All proofs are provided in the extended version.

## Preliminaries

Our approach builds on two existing concepts, normalizing flows and Bernstein polynomials, which we review here.

Normalizing Flow Normalizing flows (Papamakarios et al. 2021) are a powerful and expressive parametric form for distribution modeling. In essence, a normalizing flow consists of two parts: i) a diffeomorphism (invertible and differential map) g: X →Z which maps from a “feature” space X to a “latent” space Z that is homeomorphic to X, and ii) a simple distribution pz(z) (often the standard Gaussian) over the latent space Z. In essence, g−1 transforms pz(z) into a arbitrary density px(x) in the feature space X, and g “reverses” the transformation, allowing px(x) to be expressed using the differential change in volume, i.e., px(x) = pz(g(x)) | det(Jg(x))|, (5)

where det(Jg) is the determinant of the Jacobian of g.

For density estimation or generative modeling, g is typically parameterized with a universal invertible function approximator. In order to make g invertible and have a tractable Jacobian determinant, triangular maps are often used, i.e., gi(x) = gi(x≤i), simplifying (5) to px(x) = pz(g(x))

n Y i=1

∂gi ∂xi

(x≤i)

. (6)

To ensure that the triangular map is invertible, gi must be monotonic along the i-th dimension, i.e., ∂gi

∂xi (x≤i) > 0 for all x≤i ∈Ri. Importantly, under mild conditions (Papamakarios et al. 2021), (6) can approximate any arbitrary feature distribution px as long as gi can approximate any monotonic function along i.

Bernstein Polynomials Any multivariate polynomial π(x) of degree d can be equivalently expressed in the Bernstein basis as π(x) = Pd j=0 bjϕd j (x), where ϕd j (x) = Qn i=1 di ji xji i (1 −xi)di−ji are the Bernstein basis polynomials, and bj are the coefficients. A coefficient set in the Bernstein basis is denoted with b. The Bernstein basis allows one to easily bound the polynomial using its coefficients. We take advantage of this property in order to construct valid polynomial distribution models.

## 4 Polynomial Distribution Modeling

In this section, we present our modeling framework for p(x0) and p(xk|xk−1). We aim to express both density functions as multivariate polynomials to preserve the feasibility of (3) and satisfy conditions C2 and C3. However, polynomials inherently cannot represent PDFs supported over unbounded domains such as Rn, since a valid PDF must be a non-negative function that integrates to one over its domain, whereas any non-negative polynomial π(x) yields

R

Rn π(x)dx = ∞. To address this, we first map the unbounded support Rn to a bounded domain and then define the polynomial PDF over this transformed space.

Transforming the State Space Let Un:= (0, 1)n be the ndimensional open unit box. To enable the use of polynomial density functions, we employ a mapping Ω: X →Un to transform the original state space X into the unit box Un. As long as Ωis a diffeomorphism and diagonal, i.e., Ωi(x) =

36612

<!-- Page 4 -->

Ωi(xi), densities over X can be equivalently expressed over Un using (5) as follows.

px(x) = pu(Ω(x)) | det JΩ(x)| (7a)

= pu(Ω(x))

n Y i=1 dΩi dxi

(xi)

. (7b)

In fact, a valid choice for each component Ωi of Ωis a univariate cumulative distribution function (CDF) of a continuous distribution supported on R, e.g., the Gaussian CDF, since the CDFs are monotonic and continuous, i.e., they are diffeomorphisms. The properties of the proposed models do not depend on the specific choice of Ω; however, certain choices of Ωmay allow the model to learn more accurate representations of the underlying Markov chain (see the extended version for details on how to choose Ω).

The properties of Ωpreserve the integration property

Z

Ii px(x)dxi =

Z

Ω(Ii)

pu(u)dui, (8)

over any interval Ii of an axis of X. By extension, marginalizing or integrating px(x) over hyper-rectangular regions R ⊆X is equivalent to marginalizing or integrating over its image Ω(R) in Un. Note that Ω(R) is guaranteed to also be hyper-rectangular since Ωis diagonal and monotone.

This allows us to express a polynomial density pu(u) = π(u), such that marginalizing over ui reduces to simply integrating the polynomial π(u) over the interval [0, 1]. Additionally, it is easy to verify that the product of any two Un-polynomial densities of different random variables, e.g., p(uk|uk−1)p(uk−1), as in (3), results in a polynomial and remains integrable. For the remainder of the paper, we drop the subscript when denoting densities, e.g., pu(u) = p(u).

Since both multiplication and marginalization operations in (3) (including integration in (4)) become simple polynomial operations of the equivalent Un-polynomial densities, we can learn the Markov chain Mf directly in Un without imposing any restrictions on the generality of the underlying systems or state distributions. Therefore, all that remains is to specify the polynomial model parametric form for learning p(u0) and p(uk|uk−1).

Polynomial Density Estimation Density estimation is a functional optimization problem with two constraints over the support: i) the integral of the function over the support must be 1, and ii) the function must be non-negative. Regarding (i), the class of all polynomials of a fixed degree d that sum to 1 over Un, can be easily characterized as a linear constraint over coefficients (Yu and Loskot 2023).

Enforcing constraint (ii), however, is more challenging since even checking if a polynomial is non-negative over Un is known to be NP-hard (Murty and Kabadi 1985). To address this, we employ the Bernstein polynomial basis, which provides a relaxation, i.e., a sufficient (but not necessary) condition for bounding a polynomial (and its derivatives) over Un. We embed this relaxation within a normalizing flow architecture to ensure the necessary invertibility conditions for synthesizing valid polynomial densities.

Bernstein Normalizing Flow We propose the Bernstein Normalizing Flow (BNF) for density estimation, particularly for learning p(u0). Recall, triangular-map normalizing flows are an expressive parametric form for universal density estimation, which can be easily extended to universal conditional density estimation.

We aim to formulate a polynomial distribution over Un via the diffeomorphism g: Un →Un where the latent space is also the unit box. In order to ensure that g is a diffeomorphism, it suffices to show that gi is monotonic in ui and spans the full range, i.e., for all u = (u1,..., un) ∈Un, gi(u) = 0 if ui = 0, and gi(u) = 1 if ui = 1.

Suppose each component gi is a multivariate Bernstein polynomial gi(u) = πi g(u≤i) of degree d. By making the latent density uniform over Un, the normalizing flow density (5) simplifies to p(u) = n Y i=1

∂πi g ∂ui

(u≤i), (9)

which is simply a product of multivariate polynomials.

Hence, the two invertibility conditions of g, i.e., monotonicity and coverage of the full range, can be expressed in differential form as

∂gi ∂ui

(u≤i) > 0 (10a) Z 1

0

∂gi ∂ui

(u≤i)dui = 1 (10b)

for all u≤i ∈Ui. To enforce these conditions on the Bernstein polynomial πi g(u≤i), we can directly parameterize the partial derivative πi

∂g(u≤i) = (∂πi g/∂ui)(u≤i) and enforce constraints (10) on the coefficients via the following lemmas:

Lemma 1 (Bernstein Relaxation (Lorentz 2012)). A Bernstein polynomial π(u) with coefficients bj is bounded on Un by the extrema of its coefficients, i.e., π(u) > minj bj and π(u) < maxj bj for all u ∈Un.

Lemma 2. Let π(u) be a Bernstein polynomial of degree d = (d1,..., dn) with coefficients bj = (bj1,..., bjn). Then,

Z 1

0 π(u)dui = 1 ⇐⇒ di X ji=0 bji = di + 1 ∀ji. (11)

Let ˜bi be the coefficients of πi

∂g, which has degree ˜di = (d1,..., di −1,... dn). Then, condition (10a) can be easily enforced by constraining ˜bi j ≥0 for all 0 ≤j ≤˜di, and condition (10b) can be enforced by ensuring that all ˜bi j sum to di along the i-th axis. With both constraints, polynomials πi g correctly parameterize a diffeomorphism, and therefore p(u) is a valid density.

Remark 1. To achieve more expressivity, multiple diffeomorphism “layers” g can be composed. Doing so, however, raises the degree multiplicatively of the fully-expanded polynomial (which is necessary for belief propagation and evaluation).

36613

<!-- Page 5 -->

Conditional Density Estimation To parameterize a conditional distribution p(u | w) for w ∈ Un, we can construct a flow function h: Un × Un →Un, such that given any w, h(u, w) is a diffeomorphism in u. The differential constraints (10a) and (10b) can be modified accordingly by adding w as a parameter. Making each component hi of h a polynomial hi(u, w) = πi h(u≤i, w) of degree D = (d1,..., dn, d1,..., dn), yields a polynomial conditional distribution of the form p(u | w) = n Y i=1

∂πi h ∂ui

(u≤i, w). (12)

By ensuring that the coefficients of each πi h are all nonnegative, and sum to di −1 along the i-th axes, (12) is a valid conditional distribution.

Theorem 1. The conditional Bernstein normalizing flow is a universal conditional distribution approximator.

Belief Propagation By modeling p(u0) as a BNF and p(u′ | u) as a conditional BNF, the operations in (3) and (4) can be carried out exactly using tensor operations on the coefficients of each model. Additionally, both multiplication and integration operations can be carried out in the Bernstein basis, improving the numerical stability of each prediction (Farouki and Rajan 1987). Since belief propagation is exact with respect to the model, all prediction error can be attributed to modeling/learning error (and floating-point numerical inaccuracies).

The following theorem states another crucial consequence of using BNF to model Mf for belief propagation.

Theorem 2. Given a state-transition conditional-BNF p(u′ | u) that is of degree d′ in u′, starting from any valid polynomial belief p(u0), p(uk) ∈Πd′[u] for every k ∈N.

Theorem 2 has computational implications for longhorizon prediction. Namely, in each propagation recursion (3), the amount of memory needed to store each belief p(uk) does not grow in time, unlike methods such as GMM-splitting (Kulik and LeGrand 2024). Additionally, the computation needed for p(uk) is O(k). Note that number of parameters in BNF scales with the number of coefficients in a degree-d 2n-variate (for u and u′) Bernstein polynomial, i.e. O(d2n), which is memory intensive for large n. For scalability purposes, we recognize sparse models as valuable future work.

The proposed BNF methods are not limited to just belief propagation and can be trivially extended to other applications as discussed in the following remark.

Remark 2 (Bayesian Belief Update Analog). The proposed methods can be employed for exact Bayesian belief updating with learned likelihood and prior models, i.e., p(α | β) = pθ(β | α)pθ(α)/p(β). Computing the normalization constant p(β) needed to calculate the posterior belief p(α | β) often results in an infeasible integral for complex likelihood models. Nonetheless, the multiplication-normalization operation sequence closely parallels the propagation operation described in (3), and thus the models presented in this paper can be readily applied to exact Bayesian Belief updating.

Remark 3. The normalizing flow structure allows one to easily sample from both of the learned distributions. A latent state ˆz is sampled uniformly over Un, then mapped through the inverse of g or h, i.e., ˆu = g−1(ˆz) or ˆu = g−1(z; w).

Training Procedure In this section, we outline the procedure for training each piece of the Markov chain. Specifically, we show how the Bernstein relaxation constraints described in Sec. 4 can be enforced during training. Additionally, we describe a procedure that can be implemented during training to tighten the relaxations and increase the expressivity of the the model without increasing the number of parameters.

Constrained Log-Likelihood Optimization Maximum Likelihood Estimation (MLE) is a well established objective for density estimation (Pan and Fang 2002). We aim to maximize the likelihood BNF given state space data Dx′ and Dx0. MLE of a x-density with x-data is equivalent to MLE of a u-density against the data mapped to Un via Ω. The constrained MLE optimization problem over the parameters of each BNF model for learning p(u0) is:

arg max

˜b∈˜B

Eu0∼p⋆(u0)

log p(u0)

(13a)

subject to ˜bi ≥0 (13b)

di−1 X ji=0

˜bi = di ∀1 ≤i ≤n (13c)

where p⋆(·) denotes the true distribution, and ˜B ∋b denotes the parameter space. Expectations with respect to p⋆ are empirically evaluated over the data in Dx0. A similar optimization problem can be formulated for training the transition distribution by using the empirical expectation of log p(u′|u) over the data u′, u ∼p⋆(u′, u) where p⋆(u′, u) denotes the true joint distribution that generated Dx′. Note that, even though the constraints (13b) and (13c) are linear, the objective (13a) is non-linear and non-convex. Thus, we leverage stochastic gradient descent (SGD) for optimization.

In order to avoid explicitly constraining the parameter space, we can define a differentiable function Ψ: Θ →˜Bfeas where Θ represents an “unconstrained” parameter space, and

˜Bfeas ⊂˜B is the set of feasible parameters, i.e., the set of all ˜b that satisfy (13b) and (13c). With Ψ, SGD can be performed in Θ instead of B, enforcing the constraints implicitly. We can define Ψ for a given coefficient tensor bi as the composition of two operations: 1) map each vector to be positive, and 2) normalize the coefficients to sum to di along dimension i. Formally, we can construct Ψ as ˜bi = Ψi(θi) = (σ ◦δ)(θi), where δ is a positive-range element-wise function (e.g., softplus) and σ is the normalizing function σ(θi) = θi/ di−1 X ji=0 θi j. (14)

Each operation is differentiable; thus, models parameterized by θ0,..., θdτ −1 can be trained with standard SGD are guaranteed to satisfy the constraints.

36614

<!-- Page 6 -->

Tightening the Relaxation

We have thus far ignored an important aspect inherent to the BNF that can significantly affect the models’ expressiveness: the tightness of the Bernstein relaxation in Lemma 1. Constraining coefficients b > 0 is only a sufficient (but not necessary) condition for πi

∂g ≥0. Thus, ˜Bfeas inner-approximates the set of all degree-d polynomial diffeomorphisms, and limits the expressiveness of the model. Increasing the degree of each πi g improves the expressiveness, at the cost of adding many more parameters to the model. We propose an alternative method to tighten the relaxation during the training procedure without adding any parameters to the model.

The proposed procedure lifts a given Bernstein polynomial to a higher degree to reason over feasibility. Any Bernstein polynomial of degree d can be equivalently expressed in a Bernstein basis of a higher degree d+ ≥d (Lorentz 2012). For simplicity of presentation, we describe the following assuming a one-dimensional Bernstein polynomial; however, all operations readily extend to the multivariate case. A Bernstein basis polynomial ϕd j(x) can be written as a linear combination of higher-degree basis polynomials:

ϕd j(x) = d + 1 −j d + 1 ϕd+1 j (x) + j + 1 d + 1ϕd+1 j+1(x). (15)

One can apply (15) recursively d+ −d times to build a linear transformation of the original coefficients, in the form b+ = Md+ d b where b+ is the degree-d+ coefficient vector of the same polynomial represented by b, and Md+ d is a (d+ +1)× (d + 1) tall matrix.

Theorem 3 ((Garloff 1985)). Given a Bernstein polynomial π(u) of degree d, let π = infu∈Un π(u) and b = minj b. Then, for d+ ≥d, b ≤π ≤b + O(d−1) and b converges to π monotonically.

Theorem 3 illustrates the convergence of the Bernstein relaxation as the raised-degree is increased.

Constraining degree-d polynomials by the degree d+ representation inherently captures more non-negative degree-d polynomials, and as d+ →∞, the raised degree constraint captures all non-negative polynomials. In other words, there may exist a non-negative degree-d polynomial with coefficients b that minimizes (13a), but violates constraint (13b) due to the conservatism of the relaxation.

Employing degree-raising during training is not as straightforward as using implicit constraints, as discussed in the previous section. To illustrate the challenge, consider the following sequence of operations within a single SGD iteration: 1) Raise the degree of the current (unconstrained) parameters via b+ = Md+ d b. 2) Replace all negative entries with zero. 3) Project the rectified parameters back down to the degree-d representation. 4) Normalize the parameters using (14). Unfortunately, even though the rectified b+ ≥0 after step 2, the projection does not necessarily preserve this property.

To address this issue, we train the model with a softconstraint violation penalty. Then, using an iterative projection, the parameters are moved into the feasible region. The constraint violation penalty loss can be formulated as

P j max(0, b+), which is easily calculated with matrix multiplication. Then, to apply a hard constraint to the resulting parameters b, we iteratively repeat the projection steps 1-3 until b+ ≥0. This training procedure avoids cumbersome feasible-set projections during optimization, while still yielding a feasible solution.

Evaluations

This section evaluates the efficacy of learned BNF Markov chain models for uncertainty propagation and the effect of the choice of degree on the models’ expressiveness. Full details on system parameters, experimental setup, and additional visualizations are provided in the extended version.

Comparison Methods We compare BNF to three uncertainty propagation methods based on GMM belief representations: (i) first-order linearization around component means (EKF-style) (Jazwinski 2013), (ii) Whitened Spherical Average Second-Order Stretching (WSASOS) (Kulik and LeGrand 2024), and (iii) a grid-based approach from (Figueiredo et al. 2024). EKF and WSASOS assume nonlinear dynamics with additive Gaussian noise. The grid-based method assumes a diagonal-covariance GMM for p(x′|x), but lacks a procedure for constructing a formal GMM approximation from general nonlinear models, so we evaluate it assuming a single-component GMM.

All three methods rely on Gaussian assumptions, so we used GP regression to learn p(x′ | x) and expectation maximization on a GMM to learn p(x0). EKF serves as a widely used baseline, WSASOS as a state-of-the-art componentsplitting method, and the grid-based approach as a formal method with guaranteed error bounds.

## Experimental Setup

## Experiments

were performed on two highly non-linear latent stochastic systems: Van der Pol with additive Gaussian noise and a stable oscillator with multiplicative non-Gaussian noise. The latent initial state distribution is a Gaussian distribution. For each GMM method, p(x0) is learned with 10 mixture components to avoid overfitting to the initial state data. The resolution of the grid method is 20by-20. Each comparison uses a Multitask Gaussian Process Regression with a radial basis function kernel. For BNF, we used Bernstein polynomials with degrees 10, 20, and 30 for each component gi. Each method is trained with 1K initial state data points 10K state-transition data points. Prediction accuracy is evaluated using average log-likelihood (13a) on a distinct large test data set, consisting of Monte-Carlo samples from the true system. Each experiment was performed 10 times with random training seeds, and all log-likelihood results were found to have a variance below 10−3.

**Fig. 1.** shows a visual comparison of the computed beliefs at time step k = 9 for the Van der Pol system (Fig. 1a–d) and the stable oscillator (Fig. 1e–h). Figs. 2–3 present the average log-likelihood results. Overall, we observe that BNF performs comparably to the grid-based method in the additive Gaussian case and significantly outperforms all baselines under non- Gaussian noise. Additionally, performance improves with increasing polynomial degree.

36615

<!-- Page 7 -->

(a) Monte Carlo (b) EKF (c) GridGMM (d) BNF (e) Monte Carlo (f) EKF (g) GridGMM (h) BNF

**Figure 1.** Visual Comparison for the final belief propagated k = 9 timesteps into the future for the (a)-(d) Van der Pol and (e)-(h) stable oscillator systems.

2 4 6 8 Timestep

4.0

3.5

3.0

2.5

2.0

Average Log-Likelihood

Grid (learned) WSASOS (learned) EKF (learned) Grid (true) WSASOS (true) EKF (true) BNF (d=10) BNF (d=20) BNF (d=30)

**Figure 2.** Additive-Gaussian Noise - Belief accuracy

Additive Gaussian Noise System As can be seen in Fig. 2, BNF generates a more accurate prediction than EKF, however, the grid method performs the best. Since the system is additive Gaussian, GP regression learns a very accurate model. The grid method produces the least propagation error among the GMM methods, and is able to achieve a very accurate prediction. WSASOS (learned) times out after 6 time steps since the number of components in the GMM explodes exponentially.

To isolate propagation error from learning error, we compared BNF to baseline methods using the true underlying system dynamics, effectively isolating only the error accumulated via propagation. Alternatively, since BNF propagation is exact, the induced error is only learning error. As can be seen, BNF performs comparably despite starting from a more inaccurate initial distribution.

In BNF, the effect of the degree of the polynomial is most notably observed the estimate of the initial distribution. The initial distribution has relatively small covariance, thus, the polynomial must be able to attain a steep transition, which requires polynomials of higher degree.

Multiplicative Non-Gaussian Noise System Fig. 3 illustrates the universal modeling capability of BNFs. Since the true underlying system has highly non-linear non-Gaussian noise, the GP regression models become unable to truly capture the stochastic nature of the system, despite having ample data. Consequently, unlike the additive-Gaussian case, the GMM methods now incur significant propagation and learn-

2 4 6 8 Timestep

4.0

3.5

3.0

2.5

2.0

Average Log-Likelihood

Grid (learned) WSASOS (learned) EKF (learned) BNF (d=10) BNF (d=20) BNF (d=30)

**Figure 3.** Multipli. Non-Gaussian Noise - Belief accuracy

ing error. Conversely, BNF is able to more accurately capture the complex stochasticity in the true system (visually seen in Fig. 1 (f-g)). In particular, the inaccuracy in the stochastic model for GP-based collapses the belief over the stable points of the system, whereas BNF maintains a better (more uncertain) representation of the belief. BNF exhibits a consistent trend with the previous experiment when varying the degree. This experiment demonstrates the power of shifting all prediction error to only learning error: prediction accuracy is solely a function of the representational capability of the model and the methods used for training.

These experiments illustrate the power of BNF in learning and propagating PDFs of complex, realistic systems. Unlike baseline methods, BNF maintains high predictive fidelity even under non-Gaussian noise. Given BNF’s exact propagation property, its sole error is rooted in learning, which can be mitigated using higher polynomial degrees.

## Conclusion

In this work, we introduced a Bernstein Normalizing Flows (BNFs), a novel model class that enables universal PDF approximation and exact belief propagation by combining Bernstein polynomials with normalizing flows. BNFs eliminate approximation error while supporting efficient sampling and evaluation. We provided the theoretical foundations for this approach and empirically demonstrate that BNFs are particularly effective in nonlinear, non-Gaussian settings, where state-of-the-art methods suffer.

36616

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-universal-learning-of-stochastic-dynamics-for-exact-belief-propagation-using-ber/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## References

Akhiezer, N. I. 2020. The classical moment problem and some related questions in analysis. SIAM. Alspach, D.; and Sorenson, H. 2003. Nonlinear Bayesian estimation using Gaussian sum approximations. IEEE transactions on automatic control, 17(4): 439–448. Arpogaus, M.; Kneib, T.; Nagler, T.; and R¨ugamer, D. 2025. Hybrid Bernstein Normalizing Flows for Flexible Multivariate Density Regression with Interpretable Marginals. arXiv preprint arXiv:2505.14164. Babu, G. J.; Canty, A. J.; and Chaubey, Y. P. 2002. Application of Bernstein polynomials for smooth estimation of a distribution and density function. Journal of Statistical Planning and Inference, 105(2): 377–392. Belalia, M.; Bouezmarni, T.; and Leblanc, A. 2017. Smooth conditional distribution estimators using Bernstein polynomials. Computational Statistics & Data Analysis, 111: 166–182. Deisenroth, M. P.; Turner, R. D.; Huber, M. F.; Hanebeck, U. D.; and Rasmussen, C. E. 2011. Robust filtering and smoothing with Gaussian processes. IEEE Transactions on Automatic Control, 57(7): 1865–1871.

Djuric, P. M.; Kotecha, J. H.; Zhang, J.; Huang, Y.; Ghirmai, T.; Bugallo, M. F.; and Miguez, J. 2003. Particle filtering. IEEE signal processing magazine, 20(5): 19–38. Farouki, R. T.; and Rajan, V. 1987. On the numerical condition of polynomials in Bernstein form. Computer Aided Geometric Design, 4(3): 191–216. Figueiredo, E.; Patane, A.; Lahijanian, M.; and Laurenti, L. 2024. Uncertainty propagation in stochastic systems via mixture models with error quantification. In 2024 IEEE 63rd Conference on Decision and Control (CDC), 328–335. IEEE. Garloff, J. 1985. Convergent bounds for the range of multivariate polynomials. In Int. Symp. on Interval Mathematics, 37–56. Springer. Jasour, A.; Wang, A.; and Williams, B. C. 2021. Moment-based exact uncertainty propagation through nonlinear stochastic autonomous systems. arXiv preprint arXiv:2101.12490. Jazwinski, A. H. 2013. Stochastic processes and filtering theory. Courier Corporation. Julier, S. J.; and Uhlmann, J. K. 2004. Unscented filtering and nonlinear estimation. Proceedings of the IEEE, 92(3): 401–422. Kulik, J.; and LeGrand, K. A. 2024. Nonlinearity and uncertainty informed moment-matching Gaussian mixture splitting. arXiv preprint arXiv:2412.00343. Lorentz, G. G. 2012. Bernstein polynomials. American Mathematical Soc. Murty, K. G.; and Kabadi, S. N. 1985. Some NP-complete problems in quadratic and nonlinear programming. Technical report. Pan, J.-X.; and Fang, K.-T. 2002. Maximum likelihood estimation. In Growth curve models and statistical diagnostics, 77–158. Springer.

Papamakarios, G.; Nalisnick, E.; Rezende, D. J.; Mohamed, S.; and Lakshminarayanan, B. 2021. Normalizing flows for probabilistic modeling and inference. Journal of Machine Learning Research, 22(57): 1–64. Polymenakos, K.; Laurenti, L.; Patane, A.; Calliess, J.-P.; Cardelli, L.; Kwiatkowska, M.; Abate, A.; and Roberts, S. 2020. Safety guarantees for iterative predictions with Gaussian processes. In 2020 59th IEEE Conference on Decision and Control (CDC), 3187–3193. IEEE. Ramasinghe, S.; Fernando, K.; Khan, S.; and Barnes, N. 2022. Robust normalizing flows using Bernstein-type polynomials. 33rd British Machine Vision Conference Proceedings. Schei, T. S. 1997. A finite-difference method for linearization in nonlinear estimation algorithms. Automatica, 33(11): 2053–2058. Yu, Y.; and Loskot, P. 2023. Polynomial distributions and transformations. Mathematics, 11(4): 985.

36617
