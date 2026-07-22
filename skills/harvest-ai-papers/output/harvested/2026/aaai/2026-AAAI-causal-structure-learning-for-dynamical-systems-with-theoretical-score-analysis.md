---
title: "Causal Structure Learning for Dynamical Systems with Theoretical Score Analysis"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40999
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40999/44960
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Causal Structure Learning for Dynamical Systems with Theoretical Score Analysis

<!-- Page 1 -->

Causal Structure Learning for Dynamical Systems with Theoretical Score Analysis

Nicholas Tagliapietra1,2, Katharina Ensinger1, Christoph Zimmer3, Osman Mian4

1Bosch Center for Artificial Intelligence, Renningen, Germany 2Computer Science Department, TU Darmstadt, Germany 3Baden-Wuerttemberg Cooperative State University Mannheim, Germany 4Institute for AI in medicine IKIM, Germany tagliapietra.nicholas@gmail.com

## Abstract

Real world systems evolve in continuous-time according to their underlying causal relationships, yet their dynamics are often unknown. Existing approaches to learning such dynamics typically either discretize time —leading to poor performance on irregularly sampled data— or ignore the underlying causality. We propose CADYT, a novel method for causal discovery on dynamical systems addressing both these challenges. In contrast to state-of-the-art causal discovery methods that model the problem using discrete-time Dynamic Bayesian networks, our formulation is grounded in Difference-based causal models, which allow milder assumptions for modeling the continuous nature of the system. CADYT leverages exact Gaussian Process inference for modeling the continuous-time dynamics which is more aligned with the underlying dynamical process. We propose a practical instantiation that identifies the causal structure via a greedy search guided by the Algorithmic Markov Condition and Minimum Description Length principle. Our experiments show that CADYT outperforms state-of-the-art methods on both regularly and irregularly-sampled data, discovering causal networks closer to the true underlying dynamics.

## Introduction

Real-world physical systems are fundamentally governed by continuous-time dynamics (Strogatz 2000) with intrinsic causal mechanisms. For instance, in a mass-spring system as shown in Figure n:1, the position of each mass (Si) induces a force influencing its own velocity (Vi) and the velocities of other masses connected to it with a spring. The position of each mass, however, depends only on its own velocity. This example remarks the importance of incorporating the directionality of causal relationships to achieve physical plausiblity in learned models. While differential equations are the de facto standard for modeling dynamical systems, inferring them from data remains challenging. Moreover, when leveraging data-driven approaches such as neural networks or Gaussian processes to learn these models, there are rarely guarantees that the true underlying dynamics will include causality, and spurious correlations might be incorporated by accident. These challenges highlight the need for a causal discovery framework for learning systems in continuous time.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** CADYT discovers the unknown causal structure (Top-right) using trajectories sampled from a continuoustime dynamical system (e.g. n-mass spring system). Our learned continuous-time model adapts to arbitrary timelines, including irregularly sampled ones.

Existing state-of-the-art for causal discovery on timeseries focuses on learning the causal structure, but rarely captures the underlying continuous dynamics. Indeed, most methods learn a discretized version of the true dynamics (Hyv¨arinen et al. 2010; Peters, Janzing, and Sch¨olkopf 2013; Runge 2020; Pamfil et al. 2020) while assuming regular sampling, and are not designed for irregularly-sampled data. Dynamic-systems modeling, on the other hand, solve this issue, and current approaches adapt to irregularlysampled data by learning a continuous-time model (Chen et al. 2019; Hedge et al. 2022). These methods, however, ignore causality and do not guarantee the generalization capabilities of causal models.

In this work, we tackle both challenges: we propose a novel approach capable of performing causal discovery on dynamical systems in a continuous-time fashion, relaxing the regular sampling assumption. We review the conditions under which dynamics can be modeled with Dynamic Structural Causal Models (Mooij, Janzing, and Sch¨olkopf 2013), and build our method around those conditions. Our approach, CADYT, leverages the Gaussian Process-based framework developed by Ensinger et al. (2024) to learn a continuous-time model of the dynamics. We incorporate those in our novel score, that leverages the Algorithmic Markov Condition (AMC) postulate (Janzing and Sch¨olkopf 2010). AMC allows us to identify the causes of a target variable as the ones providing the simplest description, in terms of Kolmogorov complexity. Our score upper bounds the,

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

36740

![Figure extracted from page 1](2026-AAAI-causal-structure-learning-for-dynamical-systems-with-theoretical-score-analysis/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

otherwise uncomputable, Kolmogorov complexity via the Minimum Description Length principle (Gr¨unwald 2007). We then minimize this score via structure search for the underlying causal structure. Our contributions are as follows:

• We propose a novel approach for causal discovery in continuous-time dynamical systems that addresses both irregular sampling and causal structure identification—two challenges previously tackled in isolation. • We leverage the Gaussian Process framework for exact inference in continuous time, enabling nonparametric modeling of system dynamics. • We develop an end-to-end algorithm, Causal Discovery for Dynamic Timeseries (CADYT), combining Gaussian Process dynamical system modeling methods for continuous-time inference with structure search, enabling exact evaluation of dynamics while recovering true causal mechanisms.

## Background

In this section we introduce the basic formalism for dynamical systems described by differential equations, and how they are typically learned. Next, we provide a causal interpretation of dynamical systems through dynamic structural causal models (DSCM). We end this section by explaining how we can use the Algorithmic framework of Janzing and Sch¨olkopf (2010) to perform causal discovery over such dynamical systems defined using DSCMs.

Dynamical Systems We consider a multivariate real-valued stochastic process X(t) = {X(t)

1,..., X(t) D } on a compact time interval, i.e. t ∈[0, T] and each X(·)

i ∈R. We characterize the evolution of the system’s states through the framework of dynamical systems (Strogatz 2000), where its dynamics are governed by a defined set of rules that control state transitions. In the continuous-time setting relevant to our work, the dynamics are typically formalized using systems of autonomous Ordinary Differential Equations (ODE) of the form

˙X(t) = F(X(t)) with F: RD →RD, (1)

where ˙X(t) is the time derivative of X(t) representing its rate of change at time t, and F = (F0,..., FD) is the vector field describing the system’s dynamics. A trajectory of a dynamical system is the path traced starting from an initial condition X(0) for which Eq.(1) holds. The system of ODEs induces causal dependencies between components of the dynamics (and/or trajectories) describing if and how each one influences another, called local dependency. Bellot, Branson, and van der Schaar (2022) provide the following formalization Definition 1 (Local dependency). Two components Xi and Xj are locally dependent given any other processes iff Xi appears in the differential equation of Xj i.e. |∂iFj|̸ = 0.

Essentially, a component Xj is locally dependent on component Xi if Xi directly influences Xj in Eq.(1), and independent otherwise. These dependencies entail an associated directed (potentially cyclic) graph, G, where the components

Xi ∈X are the nodes and there is a directed edge from Xi →Xj if and only if Xj is locally dependent on Xi.

Dynamics Model Learning: In the field of Dynamics Model Learning, we aim at learning an approximation of the dynamics F from discrete-time trajectory data. Since observations are discrete while the underlying dynamics are continuous, we must first discretize the ODE using a numerical integrator. This discretization enables matching continuous dynamics to discrete observations. In this work, we use multi-step integrators (Hairer, Nørsett, and Wanner 2008) since they allow for exact GP inference. They approximate a point in the trajectory X(n+s) by using a weighted sum of the last s −1 points ¯X[n:n+s−1] = { ¯X(n),..., ¯X(n+s−1)} and are of the form s X j=0 ajn ¯X(n+j) = s X j=0 bjnF(¯X(n+j)), (2)

where ajn and bjn are integrator-specific coefficients (e.g., Adams-Bashforth or Adams-Moulton methods). The number of stages is determined by s and often corresponds to the order of convergence (Hairer, Nørsett, and Wanner 2008).

Gaussian Processes Gaussian Processes (GPs) (Rasmussen and Williams 2005) are a class of probabilistic models which describe a random function F: RD →R. They are a generalization of multivariate normal distributions, and analogously, are fully described by their mean function m(x) and covariance function kθ(x, y), where θ denotes the trainable parameters such as lengthscales. Further, the covariance function k(·, ·): RD →RD can be a kernel such as the Radial Basis Function (RBF) kernel, or the Polynomial kernel. Here, we assume a zero-mean Gaussian process prior F ∼N(0, kθ(x, y)). Further, a GP conditioned on a number of test points X = {X(1),..., X(N)} and their associated observations Y = {Y (1),..., Y (N)} still follows (by definition) a multivariate Gaussian distribution, with mean µ(X∗) and variance Σ(X∗) derived as µ(X∗) = k(X∗)T (K + λI)−1Y, (3)

Σ(X∗) = k(X∗, X∗) −k(X∗)T (K + λI)−1k(X∗), (4)

where K ∈RN×N is the covariance matrix evaluated at points X[1:N] i.e. Kij = k(X(i), X(j)). This conditioning operation is called Gaussian Process Regression (GPR).

When applied to Dynamics Model Learning, different variants of GPR are used for approximating the dynamics function F in Eq.1 by conditioning the GP on measured trajectory points. Following Ensinger et al. (2024), multi-step integrators (Hairer, Nørsett, and Wanner 2008) enable exact GP inference and make it possible to evaluate the learned F conditioned on observations. To do so, Ensinger et al. (2024) derived kernels leveraging multi-step integrators as,

K(¯X(n), ¯X(m)) = b⊤ n k(¯X[n:n+s], ¯X[m:m+s]) bm, k(¯X∗) = b⊤ n k(¯X∗, ¯X[n:n+s]),

(5)

where bn ∈Rs is the n-th column of the matrix B ∈Rs×N containing the integration coefficients, and k(¯X[i:j], ¯X[k:l])

36741

<!-- Page 3 -->

is a block matrix obtained after evaluating the chosen kernel between ¯X[i:j] and ¯X[k:l]. In essence, given N (potentially irregularly sampled) trajectory points, X[t1,...,tN] we can evaluate the dynamics at any point ¯X∗by performing the GPR in Eq.(3),(4) using the kernels in Eq. (5)

FD(X⋆|Xt1:tN) ∼N(µpost(X⋆), Σpost(X⋆)), (6)

where the equations for mean and covariance depend on the chosen multi-step integrators. The advantage of using multistep integrators within GPR is that, depending on their order, they permit a better representation of the continuous dynamics F and allow for evaluations of F at any test point X∗.

Most dynamics model learning methods discussed above ignore the causal structure and fail to preserve local dependencies. This could lead to inaccurate predictions of a component Xj when an independent, unrelated component Xi undergoes a distribution shift. In the following we show how to equip these methods to take causal relations into account.

Dynamic Structural Causal Models

The system of ODEs shown in Eq.(1) induces different local dependencies (Def. 1) between stochastic processes. This dependency can be thought of as modularization of the system. The set of individual component trajectories is called modular if the admitted trajectories of the entire system can be detached into trajectories of individual components (Mooij, Janzing, and Sch¨olkopf 2013). Under the dynamical stability assumption, which states that asymptotic dynamics of the system of ODE’s converge to a unique element irrespective of the initial conditions, a system of ODE can be converted to a Dynamic Structural Causal Model (DSCM) (Rubenstein et al. 2016), defined as follows.

Definition 2 (Rubenstein et al. 2016). Let DYNi be the trajectory for component Xi, and let DYN = S

Xi∈X DYNi be a modular set of trajectories. A deterministic Dynamic Structural Causal Model (DSCM) on time indexed variables X taking values in DYN is a collection of equations.

S: {Xi = Fi(Pai), Xi ∈X}, (7)

where Pai ⊆X\{Xi} and each Fi is a map that outputs the trajectory of the effect variable Xi in terms of the trajectory of its direct causes Pai.

In the above definition, the parents Pai should be interpreted as direct causes of Xi, and the function Fi as causal mechanism that maps the direct causes to the effect. Further, self-loops in the causal graph are allowed, although they do not explicitly appear in Def.2, which describes instead the stationary asymptotic behavior of the system. In essence in a DSCM, we explicitly decompose Eq. (1) into multiple simpler sub-equations, one for each component, as a direct consequence of local consistency. Rubenstein et al. (2016) proves that it is possible to derive a DSCM that allows us to reason about the asymptotic dynamics of the underlying ODE if the dynamic stability assumption holds, and impossible otherwise. Hence going forward, we assume dynamic stability. We adopt the instantaneous gradient assumption, meaning that causal relationships are encoded in the time derivatives of X. This assumption is more aligned with the ODE structure and milder than the instantaneous-effect assumption, which requires instantaneous dependencies between variables. Consequently, our proposal is more aligned with Difference-based Causal Models (DBCM) (Voortman, Dash, and Druzdzel 2010) as opposed to the Dynamic Bayesian Networks.

Let trajectory T ∈RN×D be a sequence of observations of X sampled from a DSCM over time-steps {t1,..., tN} and denoted by T = {X(1),..., X(N)}, we aim to find the underlying directed graph G of process interactions entailed by the DSCM and learn the dynamics of each variable using only its causal parents. Doing so is impossible unless we make assumptions on how T was generated (Pearl 2009). To that end, we assume causal sufficiency, i.e. for each component Xi there are no unobserved components that influence Xi. In addition we assume G is µ-Markovian with respect to T which implies that local independencies of the underlying DSCM are reflected in T. Conversly we assume T is µ-faithful with respect to G which implies that all local independencies that we find in T also hold in G. Together these assumptions ensure that independence statements derived from T can be interpreted as absence of edges in G, thereby letting us deduce local independencies (Mogensen and Hansen 2020). Let ϕmax be the highest frequency present among all the components within S and define ∆max = max(ti+1 −ti) for 1 ≤i< N, we assume that ∆max ∈(0, 1 2ϕmax), meaning that T has been sampled at a rate finer than its critical frequency. Next, we explain how to learn the underlying causal structure entailed by a DSCM.

Information Theoretic Causal Discovery Information theoretic causal discovery relies on the algorithmic Markov condition (AMC) (Janzing and Sch¨olkopf 2010), and is grounded in Kolmogorov complexity. The Kolmogorov complexity of a binary string x is the length of the shortest binary program p∗that outputs x and halts on a universal Turing machine U (Kolmogorov 1965; Vereshchagin and Vit´anyi 2004). For a probability distribution P, this complexity K(P) is the length of the shortest program that outputs P(x) to within precision q on input ⟨x, q⟩. Formally,

K(P) = min p∈{0,1}∗

||p||: |U(p, x, q) −P(x)| ≤1 q

The AMC states that a graph G over X, with joint distribution P, is an admissible causal graph only if the shortest description of P factorizes as K(P(X1,..., XD)) = PD j=1 K(P(Xj | Paj))+O(1). Thus, the true causal graph minimizes Kolmogorov complexity i.e. each Paj provides the tersest description of its causal child.

While Kolmogorov complexity is not computable due to the halting problem, it can be bounded from above in a statistically well-founded way using the Minimum Description Length (MDL) principle (Grunwald 2004). Marx and Vreeken (2021) show that for sample sizes approaching infinity, the true causal graph can be identified by minimizing an appropriate lossless MDL-score.

36742

<!-- Page 4 -->

Given a model class M, the MDL principle selects the optimal model M ∈M for data D by minimizing the total description length: L(D, M) = L(M) + L(D | M), where L(M) represents the number of bits required to describe the model M, and L(D | M) is the number of bits needed to describe the data D once the model M is known. Existing methods have already used this algorithmic model to discover causal graphs for non-timeseries data with reasonable success (Kaltenpoth and Vreeken 2019; Mian, Marx, and Vreeken 2021; Mameche, Kaltenpoth, and Vreeken 2023).

## 3 MDL for Dynamical Systems

To use information theoretic causal discovery with dynamical systems, we need to build a suitable MDL score for timeseries trajectories sampled from a DSCM. We will do so for the well known case of Additive Noise Models (Hoyer et al. 2009) and assume that we have

X(t)

i = ˆX(t)

i + ν(t)

i, (8)

with ˆX(t)

i following the dynamical system defined in Eq. (1) for t ∈[0, T] and ν(t)

i ∼N(0, σ2 i) being independent gaussian noise terms such that νi ⊥⊥Xi ∀i and νi ⊥⊥νj ∀i, j. This setup can be interpreted as a noisy observation model in dynamical systems, where a deterministic process is perturbed by independent additive noise. Given a trajectory T of size N for (possibly irregular) time steps {t1,..., tN}, we want to find the model such that

M ∗= argmin

M∈M

L(T, M), (9)

= argmin

M∈M

L(M) +

D X i=1

L(X[t1:tN]

i |Pai, Fi)

!

, (10)

= argmin

M∈M

L(M) +

D X i=1

L(νi)

!

, (11)

where we use the notation X[a:b]

i to denote the values for Xi from time-steps a to b included. The summation term in Eq.(10) follows from Eq.(7) and measures compression of each component given its causal parents and the parametrization enforced by M. We simplify this in Eq.(11) to show that encoding a component given the model reduces to encoding the noise terms. To be able to use MDL as a practical stand-in for Kolmogorov complexity inside AMC, we need to define a model class and an encoding scheme measuring the complexity of the class resp. data under that model class. This we do next.

Encoding the Model The model cost L(M) consists of a global cost Lglobal(M) plus the sum of the local model costs for each individual variable Xi, i.e. PD i=1 L(Mi). For a prespecified integrator of step-size s, the global cost measures the complexity of storing the initial s samples of a given trajectory T. Formally,

Lglobal(M) = log N + rd · D · s, (12) where we encode the integrator stepsize s using log N bits and first s samples of the trajectory. We assign a fixed cost of rd bits to each component value X(t)

i ∈T [t1:ts].

For each Xi, we define a local model Mi where we store its causal parents and the parameters of the structural equation Fi in Eq. (7). We encode Mi as

L(Mi) = LN(||Pai||) + ||Pai|| log D + LF (Fi), (13)

where LN encodes the number of parents using the MDLoptimal encoding for integers z ≥0 (Rissanen 1983). It is defined as LN(z) = log∗z + log c0, where log∗z = log z + log log z +... and only positive terms are considered. Further, c0 is a normalization constant to ensure the Kraft-inequality holds (Kraft 1949). Next, we identify those ||Pai|| variables and encode the function Fi over them.

Encoding the Functions To compute each local model Mi, we learn a continuous dynamics function Fi for each Xi by using the GPR scheme developed by Ensinger et al. (2024). We do so due to two main reasons namely 1) they offer a natural fit for modeling systems of ODEs by learning a continuous model and not a discrete one and are therefore capable of handling irregularly sampled trajectories and, 2) their non-parametric modeling-nature saves us from imposing parametric assumptions on Fi. Each model Mi regresses the dynamics related to variable Xi from its causal parents Pai. In essence, we learn a GP as defined in Eq.(6) using the kernels in Eq.(5), yielding an estimator in the form

Fi(Xt⋆ i |Pa[t1:t⋆)

i) ∼N µpost(Xt⋆ i), Σpost(Xt⋆ i)

, (14)

where we can estimate the dynamics of a Xi at an arbitrary point t⋆using the history of Pa[t1:t⋆)

i up to this point. Once a GP is trained, X(t)

i can be estimated by numerically integrating the dynamics Fi(·) learned by the GP over an arbitrary timeline. We formally score Fi(·) as,

LF (Fi)=log

1 rλ

N(N −1)

2 +Lϕ([αi, βi, Λi]). (15)

The components of Fi comprise the kernel matrix Ki and the corresponding length-scale and noise-variance parameters αi and βi, computed from Pai. Since the integrator coefficients are deterministically obtained from αi, βi, Ki, and the initial trajectory in Eq. (12), they need not be stored. To store Ki efficiently, we apply Singular Value Decomposition Ki = ViΛiV ⊤ i, where Vi and Λi denote the orthonormal eigenvector and diagonal eigenvalue matrices, respectively. The orthonormal matrix Vi ∈RN×N can be represented using at most N(N −1)/2 rotation angles at a predefined precision rλ. Finally, the length scales αi, variances βi, and eigenvalues in Λi are encoded using Lp.

Encoding the Parameters To encode the length-scale resp. eigenvalues obtained from the SVD, we use the score proposed by Marx and Vreeken (2019) for encoding parameters up to a user-specified precision p. We have

Lp(θ) = 2||θ|| +

||θ|| X i=1

LN(|ρi|) + LN(⌈θi · 10ρi⌉), (16)

with ρi being the smallest integer such that |θi|·10ρi ≥10p. To simplify, p = 2 implies that we consider first two digits of the parameter. We need two bits to store the signs of ρi and the parameter, then we encode the shift ρi and the shifted parameter θi.

36743

<!-- Page 5 -->

Encoding Data Given Model As a final step in constructing a lossless score, we encode the residual noise that remains after our the model has encoded the underlying causal structure and data-generating process. As our goal is to minimize the variance of the residuals across the timeseries trajectory, we encode each νi as zero mean Gaussian noise using the encoding provided by Grunwald (2004), formally

L(νi) = N

2

1 ln 2 + log 2πˆσ2 i

, (17)

where ˆσ2 i is the empirical estimate of residual noise variance. Combining the above, we obtain a lossless MDL score for a timeseries trajectory modeled using a causal graph.

Theoretical Analysis

While lack of computability of Kolmogorov complexity impedes us from directly providing identifiability guarantees using the Algorithmic Markov Condition (AMC), we can still independently prove that our score acts as a valid regularized log-likelihood score with an upperbound asymptotically similar to the BIC score (Schwarz 1978). Doing so however necessitates two additional assumptions.

Assumption 1 (Finite dimensions). K is finite-dimensional.

Assumption 2 (Bounded hyperparameters and precision). The length scale parameters αi, the variance parameters βi are upper bounded. All precisions |ρi| are upper bounded.

Kernel classes satisfying Assm. (1) include, Polynomial kernels, Wendland kernels (Wendland 1995), Buhmann kernels (Martin, Buhmann, and Ablowitz 2003), Truncated resp. Random Fourier kernels (Rahimi and Recht 2007), and Nystr¨om Approximated kernels (Williams and Seeger 2000). Intuitively, Assms. 1 and 2 ensure that the cost of storing the eigenvalues in Eq. (15) scales sub-linearly with the number of trajectory points, which is necessary to provide theoretical guarantees. Let C = log

1 rλ

· N(N−1) 2 +

2||θ|| + N 2 1 ln 2 + log(2π)

, we show the following.

Lemma 1. Given a DSCM S, let T be a trajectory generated from S and let ¯L(T, Mj) = L(Mj) + L(νj) −C. If Assms. 1,2 hold, it holds asymptotically

¯L(T, Mj) ≤c0 · N · log(ˆσ2 j) + c(j)

1 log(N) + c(j) 2.

with constants c0, c(j)

1, c(j) 2 independent of N.

Theorem 2. Given a DSCM S, let T be a trajectory generated from S and let ¯L(T, M) = PD i=1 ¯L(T, Mi). If Assms. 1,2 hold, it holds asymptotically.

¯L(T, M) ≤c0 · N · log(ˆσ2) + c1log(N) + c2.

with constants c0, c1, and c2 independent of N and ¯L(T, M) asymptotically is a valid regularized log-likelihood score according to Definition A.2.

Corollary 3. Model selection using L(T, M) is equivalent to model selection using ¯L(T, M).

We provide the proof in Appendix A. Intuitively, our proof shows that the upper bound of L(T, M) behaves like sum of component-wise regularized log-likelihood scores (such as the BIC). These guarantees, however, only hold if we score all graphs over T. This is an intractable bruteforce approach because the search space grows superexponentially in the number of variables. To nevertheless have a practical instantiation for minimizing L(T, M), we use a general greedy structure search algorithm which we describe next.

## 4 The CADYT Algorithm We present the score-based method Causal Discovery for Dynamic

Timeseries (CADYT) for discovering causal graphs of multivariate continuous-valued dynamical systems. We incorporate our proposed score into a common three-step search procedure (Mian, Marx, and Vreeken 2021; Mameche, Kaltenpoth, and Vreeken 2023) namely, edge scoring, forward and backward search. This is the next best alternative to exhaustive search for our case. The well known Greedy Equivalence Search (Chickering 2002) is not built for timeseries and methods for topological search (Wang et al. 2017; Xu, Mameche, and Vreeken 2025) do not directly apply to cyclic systems. We provide full pseudocode in Appendix E.

We start with the edge-ranking phase that computes the gain for all pairwise causal connections. The gain Γij, between each pair Xi and Xj, is given by

Γij = L(T, M) −L(T, M⊕ij), (18)

where M⊕ij implies model M with edge Xi →Xj included. Intuitively, the higher the Γij, the more confident we are that this is the correct causal edge. The edge scoring phase returns a priority queue of tuples (Γij, (Xi, Xj)) ordered by decreasing gain.

The forward search iteratively adds the highest-scoring edge from the priority queue. After adding an edge Xi → Xj, all incoming edges to Xj are re-evaluated using Eq. (18) and updated in the queue. Before inclusion, each edge is tested for statistical significance using the nohypercompression inequality (Gr¨unwald 2007). The search terminates when no further additions improve the score. The subsequent backward phase prunes redundant edges by removing any whose deletion increases L(T, M), continuing until no such edges remain. We then return the final graph.

CADYT has overall computational complexity of O(N 3D3 log D) where N 3 derives from our choice of nonparametric regression functions (GPs) for LF. In Appendix C we give a detailed derivation on the computational complexity and show how it is at least on-par with existing methods. CADYT, moreover, can be inherently parallelized, and we implement it as such, resulting in a fast runtime.

## Related Work

GPs for time-series modeling Most works in this field address discrete-time dynamics (Deisenroth and Rasmussen 2011; Wang, Fleet, and Hertzmann 2005) while we aim to learn GP dynamics models in continuous time. However,

36744

<!-- Page 6 -->

**Figure 2.** [Lower is better, NSHD ] for random graphs of sizes D ∈{5, 10, 15} for regularly sampled data (left) and irregularly sampled data (right). CADYT finds graphs closer to the ground truth resulting in a lower NSHD.

there is also work that addresses continuous-time modeling (Heinonen et al. 2018; Hedge et al. 2022; Ridderbusch, Ober-Bl¨obaum, and Goulart 2023). Glass, Ensinger, and Zimmer (2024) apply the inference scheme (Hedge et al. 2022) to active learning. We leverage the method proposed by Ensinger et al. (2024) due to the beneficial properties of exact inference even under irregular sampling. None of the mentioned approaches, as opposed to our work, can discover the underlying causality in dynamical systems.

Causal models for time-series Causal discovery from time-series data has received active research interest over the past decade. Early methods focused on Granger-causality (G-causality) (Granger 1969), which implies that Xi Gcauses Xj if including past of Xi helps in predicting the present of Xj. Methods have been designed for both linear (Geweke 1982; Barrett, Barnett, and Seth 2010) and non-linear (Nauta, Bucur, and Seifert 2019) causal models. Methods that are not explicitly based on G-causality lie in the category of constraint-based methods (Chu, Glymour, and Ridgeway 2008; Sun, Taylor, and Bollt 2015; Runge 2020), score-based methods (Pamfil et al. 2020) or noisebased methods (Hyv¨arinen et al. 2010; Peters, Janzing, and Sch¨olkopf 2013). These methods assume regularly sampled discrete trajectories and overlook the continuous-time structure of time series and the conditions required to reliably learn the underlying dynamics.

Voortman, Dash, and Druzdzel (2010) were among the first ones to study under which conditions dynamical systems allow for a causal interpretation, and proposed Difference-based causal models (DBCM). DBCM differ from well known dynamic Bayesian networks in that they force all causation to go through derivatives. This idea was extended by Mooij, Janzing, and Sch¨olkopf (2013) to show that (D)SCMs can model the asymptotic behavior of systems of ODEs with limitations on the possible interventions under DBCM. Those limitations are addressed in recent works (Blom, Bongers, and Mooij 2020; Cinquini et al. 2025).

Our proposal aims to model a DBCM rather than a dynamic Bayesian network. In contrast to the existing work, our work is uniquely positioned at the intersection of dynamical system learning and causal discovery as it provides a theory-backed approach to modeling the former, while allowing for learning the laws of the process via the latter.

**Figure 3.** [Higher is better, F1 score (top) and AUPRC (bottom)] for random graphs of sizes D ∈{5, 10, 15} for regularly (left) resp. irregularly sampled data (right). CADYT improves over baselines in terms of F1. CADYT having high AUPRC indicates higher confidence about the correct causal edges as opposed to spurious ones.

## Experiments

Setup We instantiate CADYT using parallelized greedy search. We perform our experiments with GPs with RBF- Kernel leveraging explicit Adams-Bashforth (AB) integrators of order s ∈{1, 2, 3}. Even though Thm. 1 applies to finite-dimensional Kernels, our choice is motivated by RBF-Kernel’s exact-inference capabilities. Even with overregularization that could result due to the use of RBF- Kernel, we find that we still outperform the competition. We include the results for CADYT using Polynomial kernels in the supplementary material. We compare CADYT with a variety of baselines: The constraint-based PCMCI+ (Runge 2020) using non-parametric Kernelized independence test, the score-based DYNOTEARS (Pamfil et al. 2020), and the noise-based VARLINGAM (Hyv¨arinen et al. 2010).

We generate synthetic data using Diamond structure (4 variables) and Erd˝os–R´enyi random graphs with and without cycles for D ∈{5, 10, 15} for both regular and irregular timelines. To evaluate the predicted structures we measure the Structural Hamming Distance (SHD) (Tsamardinos, Brown, and Aliferis 2006) which counts the edge mismatch in true and predicted structures. For comparability across structures of different sizes, we normalize SHD between 0 and 1 by dividing with D2 and call this NSHD. To evaluate precision and recall over predicted edges we use the F1 metric, and use Area Under Precision Recall Curve (AUPRC) to assess how correct each method is on the edges it is most confident about. We repeat all experiments 20 times with different seeds and report the mean. We report results for the more challenging setting of Erd˝os–R´enyi graphs with both regular and irregular sampling in the manuscript and postpone full experimental details to Appendix B.

36745

![Figure extracted from page 6](2026-AAAI-causal-structure-learning-for-dynamical-systems-with-theoretical-score-analysis/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-causal-structure-learning-for-dynamical-systems-with-theoretical-score-analysis/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

**Figure 4.** [NSHD (left) Lower is better, AUPRC (right) Higher is better] for Adams-Bashforth integrator of order s ∈{1, 2, 3} for irregularly sampled data. CADYT shows gradual improvement with higher order integrators.

## Results

We perform a sanity check and assess the robustness of CADYT to false-positives. We generated 10 graphs made of 4 independent ODEs. CADYT with AB3 never discovered a single spurious edge. Surprisingly, baselines report causal edges for independent data. VARLINGAM found spurious edges 30% of times, whereas PCMCI+ and DYNOTEARS 60% and 100% respectively.

Next we sample random dynamical systems and evaluate how well the methods can discover the underlying causal structure. We sample cyclic and acyclic dynamical systems with equal probability and report the results. We report NSHD in Figure n: 2 where we observe that CADYT consistently outperforms all baselines by a clear margin. Both DYNOTEARS and PCMCI+ demonstrate a high false positive rate which worsens the NSHD. Overall, all methods worsen slightly on irregularly-sampled data, but CADYT still remains best by a visible margin.

To evaluate how well we perform in-terms of precision and recall, we report the F1 score in Figure n: 3. We see that CADYT is on-par with the baselines for variable sizes 5, and continues to be robust to false-positives by maintaining a high precision as network size increases. Competing methods on the other hand have very low precision as they tend to predict spurious edges quite frequently.

While NSHD and F1 score could give us a summarized picture of how well the methods perform, we are also interested in how correct are the methods on the causal relationships that they are most confident about. To that end, we calculate the AUPRC metric by ordering the predicted edges of each algorithm in decreasing confidence. For CADYT this confidence is computed using Eq. (18), For PCMCI+ we use the p-values associated with each edge whereas for DYNOTEARS resp. VARLINGAM we use the strength of the causal edge as present in the predicted adjacency matrix. Looking at the results in Figure n: 3 we see that CADYT again performs well across benchmarks. A high AUPRC indicates that CADYT is mostly correct about high-confidence edges.

Effect of Integration Order To study the effect of the integration scheme, we conduct an ablation study whose result we report in Figure n:4. We compare integrators on irregular timelines and see that higher-order integrators (AB2/AB3) generally outperform AB1. This is consistent with the domain knowledge that higher-order integration schemes approximate the underlying continuous-time dynamics better.

## Method

DblMass DblLinear R¨ossler DYNOTEARS 0.22 0.59 0.34 PCMCI+ 0.24 0.30 0.22 VARLINGAM 0.39 0.44 0.30 CADYT (ours) 0.79 0.79 0.55

**Table 1.** [Higher is better, AUPRC ] for the simulated 2-mass spring system (DblMass), for the real double-linear system (DblLinear), and for the R¨ossler Oscillator (R¨ossler).

We observed that addition of cycles into the datagenerating process affects the methods differently. We find CADYT tends to improve with the order of integration, where versions leveraging higher-order schemes (AB2 and AB3) stay robust or even improve, whereas the lower-order AB1 variant deteriorates.

Oscillators and Chaotic Systems We further test on the simulated 2-mass spring system, its analogous real-world counterpart (Schmidt and Lipson 2009), and the hyperchaotic R¨ossler Oscillator. To stay fair to the baselines, we use regular sampling. We report results averaged over 10 runs in Table n: 1 which shows that CADYT outperforms the competing methods and finds causal structures closer to the underlying dynamics (lower SHD), while denoting high confidence about true edges (high AUPRC).

## Discussion

and Conclusions

We proposed CADYT, a method for uncovering causal structure in continuous-time dynamics from discrete trajectory data. Our approach combines the exact inference framework of Ensinger et al. (2024) with the Algorithmic Markov Condition (Janzing and Sch¨olkopf 2010). We proved that our score is a valid regularized log-likelihood score (Def.A.2) with an upper-bound asymptotically similar to the BIC, and demonstrated empirically that our score outperforms existing methods. Going forward we see potential lines of improvements as future work.

First, we used greedy graph search and the Adams- Bashforth integrators as the two main components for CADYT. We do not, however, claim that these to be optimal choices. It is possible that alternate search strategies resp. integrators yield better performance and we aim to investigate such alternative approaches. Second, while using the proposal of Ensinger et al. (2024) allowed us to naturally work with both regular and irregular-sampled trajectories, it has been known to be sensitive to high amount of noise. We conjecture that we could further improve the results by evolving the machinery to be robust to noise. Third, we could extend CADYT to relax the causal sufficiency assumption by searching for instantaneous edges such that both edge directions give a high score, post backward search. This could potentially point to a hidden confounder. Last, currently CADYT assumes ODEs can be well-modeled by a GP regression under noisy observation model. A recently proposed extension of DSCMS to chaotic models (Boeken and Mooij 2024) could allow us to relax this assumption further and is a potentially rewarding line of future work.

36746

![Figure extracted from page 7](2026-AAAI-causal-structure-learning-for-dynamical-systems-with-theoretical-score-analysis/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

Nicholas Tagliapietra and Katharina Ensinger are supported by Robert Bosch GmbH. Osman Mian is supported by the German Federal Ministry of Research, Technology and Space (DECIPHER-M, 01KD2420C).

## References

Barrett, A. B.; Barnett, L.; and Seth, A. K. 2010. Multivariate Granger causality and generalized variance. Physical Review E—Statistical, Nonlinear, and Soft Matter Physics, 81(4). Bellot, A.; Branson, K.; and van der Schaar, M. 2022. Neural graphical modelling in continuous-time: consistency guarantees and algorithms. arXiv:2105.02522. Blom, T.; Bongers, S.; and Mooij, J. M. 2020. Beyond Structural Causal Models: Causal Constraints Models. In Adams, R. P.; and Gogate, V., eds., Proceedings of The 35th Uncertainty in Artificial Intelligence Conference, volume 115 of PMLR, 585–594. PMLR. Boeken, P.; and Mooij, J. M. 2024. Dynamic Structural Causal Models. arXiv:2406.01161. Chen, R. T. Q.; Rubanova, Y.; Bettencourt, J.; and Duvenaud, D. 2019. Neural Ordinary Differential Equations. arXiv:1806.07366. Chickering, D. M. 2002. Optimal structure identification with greedy search. JMLR, 3. Chu, T.; Glymour, C.; and Ridgeway, G. 2008. Search for Additive Nonlinear Time Series Causal Models. Journal of Machine Learning Research, 9(5). Cinquini, M.; Beretta, I.; Ruggieri, S.; and Valera, I. 2025. A Practical Approach to Causal Inference over Time. Proceedings of the AAAI Conference on Artificial Intelligence, 39: 14832–14839. Deisenroth, M. P.; and Rasmussen, C. E. 2011. PILCO: a model-based and data-efficient approach to policy search. In Proceedings of the 28th ICML, ICML’11. Omnipress. Ensinger, K.; Tagliapietra, N.; Ziesche, S.; and Trimpe, S. 2024. Exact inference for continuous-time Gaussian process dynamics. In Proceedings of the Thirty-Eighth AAAI Conference on Artificial Intelligence and Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence and Fourteenth Symposium on Educational Advances in Artificial Intelligence, AAAI’24/IAAI’24/EAAI’24. AAAI Press. Geweke, J. 1982. Measurement of linear dependence and feedback between multiple time series. Journal of the American statistical association, 77(378). Glass, L.; Ensinger, K.; and Zimmer, C. 2024. Safe Active Learning for Gaussian Differential Equations. arXiv:2412.09053. Granger, C. W. J. 1969. Investigating Causal Relations by Econometric Models and Cross-spectral Methods. Econometrica, 37(3): 424–438. Grunwald, P. 2004. A tutorial introduction to the minimum description length principle. arXiv:math/0406077.

Gr¨unwald, P. D. 2007. The minimum description length principle. MIT press. Hairer, E.; Nørsett, S.; and Wanner, G. 2008. Solving Ordinary Differential Equations I: Nonstiff Problems. Springer Series in Computational Mathematics. Springer Berlin Heidelberg. ISBN 9783540566700. Hedge, P.; Yildiz, C.; L¨ahdesm¨aki, H.; Kaski, S.; and Heinonen, M. 2022. Variational multiple shooting for Bayesian ODEs with Gaussian processes. In Proceedings of the 38th Conference on Uncertainty in Artificial Intelligence (UAI 2022), PMLR, Proceedings of Machine Learning Research, 790–799. United States: JMLR. Conference on Uncertainty in Artificial Intelligence, UAI; Conference date: 01-08-2022 Through 05-08-2022. Heinonen, M.; Yildiz, C.; Mannerstr¨om, H.; Intosalmi, J.; and L¨ahdesm¨aki, H. 2018. Learning unknown ODE models with Gaussian processes. In Proceedings of the 35th ICML, ICML 2018, volume 5 of PMLR, 3120–3132. United States: International Machine Learning Society. Hoyer, P.; Janzing, D.; Mooij, J. M.; Peters, J.; and Sch¨olkopf, B. 2009. Nonlinear causal discovery with additive noise models. In NeurIPS, volume 21. Curran. Hyv¨arinen, A.; Zhang, K.; Shimizu, S.; and Hoyer, P. O. 2010. Estimation of a structural vector autoregression model using non-Gaussianity. Journal of Machine Learning Research, 11(5). Janzing, D.; and Sch¨olkopf, B. 2010. Causal inference using the Algorithmic Markov Condition. IEEETPAMI, 56: 5168– 5194. Kaltenpoth, D.; and Vreeken, J. 2019. We Are Not Your Real Parents: Telling Causal from Confounded by MDL. In SDM. SIAM. Kolmogorov, A. N. 1965. Three approaches to the quantitative definition ofinformation’. Problems of information transmission, 1(1). Kraft, L. G. 1949. A device for quantizing, grouping, and coding amplitude-modulated pulses. Ph.D. thesis, Massachusetts Institute of Technology. Mameche, S.; Kaltenpoth, D.; and Vreeken, J. 2023. Learning Causal Models under Independent Changes. In Oh, A.; Naumann, T.; Globerson, A.; Saenko, K.; Hardt, M.; and Levine, S., eds., Advances in Neural Information Processing Systems, volume 36, 75595–75622. Curran Associates, Inc. Martin, B.; Buhmann, M.; and Ablowitz, J. 2003. Radial basis functions: theory and implementations. Cambridge University (ISBN: 0-521-63338-9.). Marx, A.; and Vreeken, J. 2019. Telling cause from effect by local and global regression. KAIS, 60(3): 1277–1305. Marx, A.; and Vreeken, J. 2021. Formally Justifying MDLbased Inference of Cause and Effect. arXiv:2105.01902. Mian, O.; Marx, A.; and Vreeken, J. 2021. Discovering Fully Oriented Causal Networks. In AAAI. Mogensen, S. W.; and Hansen, N. R. 2020. Markov equivalence of marginalized local independence graphs. The Annals of Statistics, 48(1).

36747

<!-- Page 9 -->

Mooij, J. M.; Janzing, D.; and Sch¨olkopf, B. 2013. From ordinary differential equations to structural causal models: the deterministic case. arXiv preprint arXiv:1304.7920. Nauta, M.; Bucur, D.; and Seifert, C. 2019. Causal discovery with attention-based convolutional neural networks. Machine Learning and Knowledge Extraction, 1(1). Pamfil, R.; Sriwattanaworachai, N.; Desai, S.; Pilgerstorfer, P.; Georgatzis, K.; Beaumont, P.; and Aragam, B. 2020. Dynotears: Structure learning from time-series data. In International Conference on Artificial Intelligence and Statistics. Pmlr. Pearl, J. 2009. Causality. Cambridge university press. Peters, J.; Janzing, D.; and Sch¨olkopf, B. 2013. Causal inference on time series using restricted structural equation models. Advances in neural information processing systems, 26. Rahimi, A.; and Recht, B. 2007. Random features for largescale kernel machines. Advances in neural information processing systems, 20. Rasmussen, C. E.; and Williams, C. K. I. 2005. Gaussian Processes for Machine Learning (Adaptive Computation and Machine Learning). The MIT Press. Ridderbusch, S.; Ober-Bl¨obaum, S.; and Goulart, P. 2023. The past does matter: correlation of subsequent states in trajectory predictions of Gaussian Process models. In Uncertainty in Artificial Intelligence, UAI 2023, July 31 - 4 August 2023, Pittsburgh, PA, USA, volume 216, 1752–1761. PMLR. Rissanen, J. 1983. A Universal Prior for Integers and Estimation by Minimum Description Length. AnnalsStatistics, 11(2): 416–431. Rubenstein, P. K.; Bongers, S.; Sch¨olkopf, B.; and Mooij, J. M. 2016. From deterministic ODEs to dynamic structural causal models. arXiv preprint arXiv:1608.08028. Runge, J. 2020. Discovering contemporaneous and lagged causal relations in autocorrelated nonlinear time series datasets. In Conference on uncertainty in artificial intelligence. Pmlr. Schmidt, M.; and Lipson, H. 2009. Distilling Free-Form Natural Laws from Experimental Data. Science, 324(5923). Schwarz, G. 1978. Estimating the dimension of a model. The annals of statistics. Strogatz, S. H. 2000. Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry and Engineering. Westview Press. Sun, J.; Taylor, D.; and Bollt, E. M. 2015. Causal network inference by optimal causation entropy. SIAM Journal on Applied Dynamical Systems, 14(1). Tsamardinos, I.; Brown, L. E.; and Aliferis, C. F. 2006. The max-min hill-climbing Bayesian network structure learning algorithm. Machine Learning, 65. Vereshchagin, N. K.; and Vit´anyi, P. M. 2004. Kolmogorov’s structure functions and model selection. IEEETIT, 50(12). Voortman, M.; Dash, D.; and Druzdzel, M. J. 2010. Learning causal models that make correct manipulation predictions with time series data. In Causality: Objectives and Assessment. PMLR.

Wang, J. M.; Fleet, D. J.; and Hertzmann, A. 2005. Gaussian Process Dynamical Models. In NeurIPS 2005. Cambridge, MA, USA: MIT Press. Wang, Y.; Solus, L.; Yang, K. D.; and Uhler, C. 2017. Permutation-based Causal Inference Algorithms with Interventions. In NIPS. Wendland, H. 1995. Piecewise polynomial, positive definite and compactly supported radial functions of minimal degree. Advances in computational Mathematics, 4(1). Williams, C.; and Seeger, M. 2000. Using the Nystr¨om method to speed up kernel machines. Advances in neural information processing systems, 13. Xu, S.; Mameche, S.; and Vreeken, J. 2025. Information- Theoretic Causal Discovery in Topological Order. In AIS- TATS 2025.

36748
