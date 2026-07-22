---
title: "Variance Reduction via Resampling and Experience Replay"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39304
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39304/43265
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Variance Reduction via Resampling and Experience Replay

<!-- Page 1 -->

Variance Reduction via Resampling and Experience Replay

Jiale Han, Xiaowu Dai*, Yuhua Zhu*

Department of Statistics and Data Science, UCLA

{jialehan, daix, yuhuazhu}@ucla.edu

## Abstract

Experience replay is a foundational technique in reinforcement learning that enhances learning stability by storing past experiences in a replay buffer and reusing them during training. Despite its practical success, its theoretical properties remain underexplored. In this paper, we present a theoretical framework that models experience replay using resampled Uand V -statistics, providing rigorous variance reduction guarantees. We apply this framework to policy evaluation tasks using the Least-Squares Temporal Difference (LSTD) algorithm and a Partial Differential Equation (PDE)-based modelfree algorithm, demonstrating significant improvements in stability and efficiency, particularly in data-scarce scenarios. Beyond policy evaluation, we extend the framework to kernel ridge regression, showing that the experience replay-based method reduces the computational cost from the traditional cubic time to quadratic time in the sample size, while also reducing variance. Extensive numerical experiments validate our theoretical findings, demonstrating the broad applicability and effectiveness of experience replay in diverse machine learning tasks.

Code — https://github.com/JialeHan22/Variance-

Reduction-via-Resampling-and-Experience-Replay Extended version — https://arxiv.org/pdf/2502.00520

## Introduction

Experience replay is widely recognized for enhancing learning stability by storing past experiences in a memory buffer and reusing them during training (Lin 1992; Mnih et al. 2015). Rather than processing each experience only once, experience replay randomly samples batches of experiences to update learning targets, increasing sample efficiency and improving model performance. This approach has become a key component in modern reinforcement learning (RL), driving breakthroughs in applications such as Atari games (Mnih et al. 2015) and AlphaGo (Silver et al. 2016). However, despite its widespread success, the theoretical understanding of experience replay remains limited, often requiring extensive trial and error for effective application (Zhang and Sutton 2017; Fedus et al. 2020). To address this gap,

*Co-corresponding authors Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

we propose a theoretical framework that connects experience replay to resampled U- and V - statistics (Frees 1989; Shieh 1994). This framework establishes rigorous variance reduction guarantees, providing a deeper understanding of how experience replay enhances learning stability.

Building on prior work on U- and V - statistics (Zhou, Mentch, and Hooker 2021; Peng, Coleman, and Mentch 2022), which primarily focused on decision-tree-based methods like random forests, we extend this framework to encompass a broader class of learning functions. We derive the asymptotic variance of learned estimators, demonstrating that estimators employing experience replay achieve asymptotically lower variance compared to their original methods. To validate our framework, we analyze variance reduction through experience replay in two important machine-learning problems: policy evaluation in RL and supervised learning in reproducing kernel Hilbert space (RKHS).

(a) LSTD approach. (b) PDE-based approach.

**Figure 1.** Variance reduction achieved by experience replay in policy evaluation using two approaches. U- and V statistics methods incorporate experience replay without and with replacement, respectively, into the original method. The solid lines represent the mean estimates, and the shaded areas denote the 95% confidence intervals (CIs), calculated from 50 data replications.

Policy evaluation is a critical component of RL, where the goal is to estimate the value function representing the expected cumulative reward under a given policy. Stable and accurate policy evaluation significantly impacts the overall

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

21558

![Figure extracted from page 1](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

performance of RL algorithms. We demonstrate the effectiveness of experience replay in two policy evaluation algorithms: (i) the Least-Squares Temporal Difference (LSTD) algorithm for Markov Decision Process (MDP) (Bradtke and Barto 1996), and (ii) the PDE-based algorithm for environments with continuous-time state dynamics (Zhu 2024). LSTD is a widely used data-efficient policy evaluation method that approximates value functions within a linear space by solving a least-squares problem derived from the Bellman equation (Bradtke and Barto 1996). The PDEbased approach is a novel method that employs a PDE framework to approximate the continuous-time value function and is tailored for environments where the state variable evolves continuously over time, which is a common scenario in applications such as autonomous driving (Kong et al. 2015) and robotics (Kober, Bagnell, and Peters 2013), where discrete-time models like MDP may fail to capture the complexity of the environment. Incorporating experience replay into these algorithms significantly enhances their stability by reducing variance, as illustrated in Figure 1. Rather than the original method which uses the entire dataset at once, the experience replay method resamples subsets, either without or with replacement, from the original dataset. These subsets are used to generate predictions, which are then averaged using resampled U- or V -statistics to produce the final prediction. This resampling approach enables data duplication, mitigates variability in predictions due to changes in the dataset, and enhances stability through the averaging process. This improvement is particularly important in practice, as the numerical results in Zhu (2024) indicate that the original RL algorithm solution can exhibit substantial instability.

While experience replay methods have been extensively validated empirically in RL, our contribution lies in providing a theoretical framework that explains why experience replay is effective in practice, particularly for policy evaluation. The experience replay technique can be further improved by incorporating extensions such as prioritized experience replay based on importance sampling (Schaul 2015). Our theoretical framework can also be extended to analyze these variants.

Besides RL, we apply our framework to supervised learning tasks using kernel ridge regression, where each regression sample is treated as an experience. Kernel ridge regression enhances modeling flexibility by leveraging reproducing kernel methods to map data into RKHS (Wahba 1990; Shawe-Taylor and Cristianini 2004). Unlike existing divideand-conquer strategies that partition datasets into disjoint subsets to reduce computational costs (Zhang, Duchi, and Wainwright 2013), our approach employs experience replay to repeatedly draw random subsamples, providing a novel strategy to improve computational efficiency. With appropriate parameter choices, our method reduces the computational cost of kernel ridge regression from the traditional O(n3) to O(n2). At the same time, our theoretical results guarantee that the variance of the predictions is lower than that of the original kernel ridge regression method. Hence, incorporating experience replay leads to more stable and faster predictions in supervised learning tasks.

We validate the effectiveness of our proposed framework through extensive experiments. The results consistently demonstrate that experience replay significantly reduces the variance of predictions compared to methods without it, highlighting its ability to enhance stability in both reinforcement learning and supervised learning tasks. Additionally, it reduces the computational cost in kernel ridge regression with an appropriate choice of parameters. Notably, experience replay generally leads to both reduced variance and lower mean squared error in predictions.

The rest of the paper is organized as follows. Section 2 introduces the background of experience replay and its connection to resampled U- or V -statistics. Section 3 defines the resampled estimators, establishes their variance reduction guarantees, and discusses applications in policy evaluation and supervised learning tasks. Section 4 presents numerical experiments to validate the theoretical findings. Section 5 concludes the paper with potential future directions. All technical proofs are included in the Appendix presented in the extended version of the paper.

## Background

Experience Replay. Experience replay stores past data in a replay buffer, denoted as Dn = {Z1,...,Zn}, where n represents the sample size, commonly referred to as the replay capacity in the context of experience replay (Lin 1992). The replay ratio B ≥1 denotes the number of batches sampled from the buffer during each update step. In practice, uniform sampling is the most common strategy for selecting data from the replay buffer, although more computationally expensive alternatives, such as prioritized experience replay, are also used (Zhang and Sutton 2017; Schaul 2015). This paper establishes theoretical guarantees for replay-based methods under uniform sampling. The proposed framework, however, can be extended to non-uniform (importance) sampling, as discussed in Appendix A.

At each update step, we sample B subsets of data points, {b1,...,bB}, where each subset bi (i = 1,...,B) contains k ≤n data points. The learning method is represented by a function hk, which takes k data points as input. The response with experience replay is then computed as the average over these B subsets: 1 B ∑ i hk(bi). (1)

In experience replay for Q-learning, each data point in the replay buffer Dn corresponds to a single transition, and k = 1 (Fedus et al. 2020). This paper studies algorithms such as LSTD, where k could increase with n. LSTD is a foundational and actively studied RL algorithm for policy evaluation (e.g., Tu and Recht 2018; Duan, Wang, and Wainwright 2024), which serves as an essential step to theoretically understand experience replay in other RL methods, such as Qlearning.

Connection to Resampled Statistics. To analyze the properties of experience replay (1), we consider, for clarity of exposition, a setting where the replay buffer Dn contains n i.i.d. observations drawn from an underlying distribution FZ over the space Z. The i.i.d. assumption can be relaxed in

21559

<!-- Page 3 -->

various ways without affecting our results (see Appendix B). We allow B and k to depend on n, with k increasing in n. This ensures that the function hk can use more information as the data size grows.

When the sampling strategy is uniform sampling without replacement, the computation in (1) takes the form of an incomplete, infinite order (or resampled) U-statistics (Frees 1989; Zhou, Mentch, and Hooker 2021), defined as:

Un,k,B = 1

B ∑ i hk(Zi1,...,Zik). (2)

where infinite order means that k and B depend on the value of n, and {Zi1,...,Zik} are drawn without replacement from {Z1,...,Zn}. In contrast, with uniform sampling with replacement, the computation in (1) follows the form of an incomplete, infinite order (or resampled) V -statistics (Shieh 1994; Zhou, Mentch, and Hooker 2021), given by:

Vn,k,B = 1

B ∑ i hk(Zi1,...,Zik), (3)

where k and B again depend on n, and the B subsets are drawn with replacement from all size-k permutations of {1,...,n}.

Under appropriate regularity conditions, both resampled U-statistics and V -statistics are asymptotically normal (Mentch and Hooker 2016; Zhou, Mentch, and Hooker 2021). The variances of these statistics can be expressed as a linear combination of k2 n ζ1,k and 1 B ζk,k. For a given c, 1 ≤c ≤k, the variance components ζc,k are defined as

Cov(hk(Z1,...,Zk),hk(Z1,...,Zc,Z

′ c+1,...,Z

′ k)), where Z

′ c+1,...,Z

′ k are i.i.d. copies from FZ, independent of the original data set Dn.

Learning Target. We focus on estimating the quantity defined as, θ = [E[g(Z)]]

−1[E[f(Z)]] ∈Rq, (4)

where g(⋅) ∶Z →Rq×q is a function returning an invertible matrix, and f(⋅) ∶Z →Rq. The target θ arises in various machine learning applications, including policy evaluation algorithms in reinforcement learning (Bradtke and Barto 1996; Zhu 2024), and supervised learning with kernel ridge regression (Wahba 1990; Rahimi and Recht 2007). We will discuss the application of experience replay to these methods in Section 3.2.

To estimate θ in (4), we use a function hk based on k ≤n data points Z∗

1,Z∗ 2,...,Z∗ k for any Z∗ i ∈Dn, i = 1,...,k, where hk in (1) is defined as:

hk(Z∗

1,...,Z∗ k) ∶= [ k ∑ i=1 g(Z∗ i)]

−1

[ k ∑ i=1 f(Z∗ i)] ∈Rq. (5)

The learning function in (5) provides a unified framework that applies to several algorithms, including the LSTD algorithm in reinforcement learning and kernel ridge regression in supervised learning. We will theoretically show that incorporating the experience replay approach (1) reduces the variance of the estimate of θ and thus improves stability.

## Algorithm

1 Estimating θ via Different Methods

1: Input: Replay buffer Dn = {Z1,...,Zn}; Functions f and g; Replay ratio (number of subsamples) B; Subsample size k. 2: Original Estimator: Compute ˜θn using (6). 3: Resampled Estimators Based on U(V)-statistics: 4: for i = 1 to B do 5: Randomly drawn k samples {Zi1,...,Zik} without (for U-statistics) or with replacement (for V -statistics). 6: end for 7: Compute ˆθU or ˆθV using (7) or (8), respectively. 8: Output: Estimators ˜θn, ˆθU, and ˆθV.

Main Results 3.1 Theoretical Guarantees Estimators without Experience Replay. When the experience replay approach is not used, and each data point in the replay buffer Dn is used only once, a plug-in estimator for θ in (5) is:

˜θn ∶= [ n ∑ i=1 g(Zi)]

−1

[ n ∑ i=1 f(Zi)]. (6)

The asymptotic property of ˜θn is described in the following lemma. The proof relies on the central limit theorem and the delta method.

Lemma 1 Let Z1,Z2,...,Zn iid∼FZ and ˜θn defined in (6), we have that √n[˜θn −θ]

dÐ→N(0,Σ), where Σ is a constant matrix given by

G(Var(f(Z)) Cov(f(Z),vec(g(Z))) Cov(f(Z),vec(g(Z))) Var(vec(g(Z)))G⊺, with G = ([E[g(Z)]]−1,−θ⊺⊗[E[g(Z)]]−1), where ⊗denotes the Kronecker product, and vec(A) reshapes a matrix A into a column vector by stacking its columns sequentially.

Estimators with Experience Replay. Using the experience replay approach, we propose two new estimators for θ that leverage resampling methods based on U- and V statistics. These estimators are constructed using the learning method hk defined in (5),

ˆθU ∶= Un,k,B = 1

B ∑ i hk(Zi1,...,Zik), (7)

ˆθV ∶= Vn,k,B = 1

B ∑ i hk(Zi1,...,Zik), (8)

where Un,k,B and Vn,k,B are resampled U- and V -statistics defined in (2) and (3), respectively. Algorithm 1 outlines the procedure for computing these estimators. The following theorem establishes that the U-statistics-based estimators achieve lower variances than the original estimator under general conditions.

Theorem 1 (Variance Reduction for U-Statistics) Let Z1,Z2,...,Zn iid∼FZ, and define ˆθU as in (7) and ˜θn as in

21560

<!-- Page 4 -->

(6). Under the assumption that limn→∞1 nζk,k[ζ1,k]−1 →0 and limn→∞n/(Bk) →0, we have liminf n→∞[Var(˜θn) −Var(ˆθU)] ≥0.

The assumption limn→∞1 nζk,k[ζ1,k]−1 →0 used by Peng, Coleman, and Mentch (2022), ensures the asymptotic normality of the resampled U-statistics. As noted in their work, this condition is typically satisfied if 1 kζk,k[ζ1,k]−1 remains bounded, with k = o(n) being sufficient. Additionally, the theorem requires n/Bk to be small, which can be achieved by selecting a large replay ratio B.

To analyze the variance reduction for V -statistics-based estimators, we define the following class of functions H = {hk ∶ sup k

∣∣E[hk(Zi1,...,Zik)hk(Zi1,...,Zik)⊺]∣∣∞ <

∞}, where (i1,...,ik) are indices selected with replacement from {1,...,k}. This condition, used by Zhou, Mentch, and Hooker (2021), ensures the boundedness of the expected outer product of hk.

Theorem 2 (Variance Reduction for V -Statistics) Let Z1,Z2,...,Zn iid∼FZ, and define ˆθV as in (8) and ˜θn as in (6), with hk ∈H. Under the assumptions k = o(n1/4), limn→∞k2ζ1,k > 0, and limn→∞n/(Bk) →0, we have liminf n→∞[Var(˜θn) −Var(ˆθV)] ≥0.

The condition limn→∞k2ζ1,k > 0, which is satisfied by many base learners and has been used in prior work (Song, Chen, and Kato 2019; Zhou, Mentch, and Hooker 2021), is further discussed in Appendix C, where we show that it holds in our framework.

Theorems 1 and 2 show that incorporating experience replay via resampled U- and V -statistics asymptotically reduces variance compared to the original estimator, enhancing the stability of parameter estimation. Our results remain valid under more general data-generating processes beyond the i.i.d. setting, including dependent sequences such as stationary ergodic Markov chains, β-mixing processes with summable coefficients, and m-dependent sequences; see Appendix B for details.

## 3.2 Applications to Machine Learning Problems

Policy Evaluation for MDP. Consider a MDP defined by the tuple (S,A,γ,r, P) (Sutton and Barto 2018). Here s ∈S denotes the state space, a ∈A represents the action space, γ ∈(0,1) is a given discounted factor, r ∶S × A →R is the reward function, and P ∶S × A →∆(S) denotes the probability distribution of the next state given the current state and action. The goal of MDP is to find the optimal policy π∗(s) that maximizes the value function. Here the policy is a mapping from the state space S to action space A, while the value function V π

∗(s) measures the expected cumulative reward of an agent over the long run, defined as:

V π

∗(s) = E

⎡⎢⎢⎢⎣

∞ ∑ j=0 γjrπ

∗(sj)∣s0 = s

⎤⎥⎥⎥⎦

, (9)

where s0 = s is the initial state, rπ

∗(s) = r(s,π(s)) is a known reward function under the current policy, and the state at time step j + 1 follows the transition distribution under the policy π, sj+1 ∼P π(⋅∣sj) = P(⋅∣sj,π(sj)). In RL, one usually divides the RL problem into two parts, one is policy evaluation, which is given a policy π(s), calculates the value function V π

∗(s); Another is policy improvement, that improves the policy according to gradient ascent or policy iteration.

The focus of this paper is policy evaluation, which is one of the most fundamental RL problems. In the setting of RL, one does not have access to the transition distribution. Instead, the agent applies an action aj = π(sj) according to the policy at each time step j, and observes the next step sj+1, receives a numerical reward rπ

∗(sj+1). Due to the finite length of the trajectory data, it is usually impossible to compute the value function directly according to the cumulative sum (9). Note that the value function V π

∗(s) also satisfies the following Bellman equation (BE),

V π

∗(s) = rπ

∗(s) + γEsj+1∼P π(s′∣s0)[V π

∗(sj+1)∣s0 = s]. (10)

Therefore, the goal of the policy evaluation problem is to find the value function that solves BE (10) given a set of trajectory data,

Dn = {(sl

0,sl 1,...,sl L)}n l=1. (11)

Here the data set contains n independent trajectories and each contains L + 1 data points. The initial state sl

0 of each trajectory is sampled from a distribution ρπ

0(s). Our method also extends to settings with dependent data and variablelength trajectories (see Appendix B).

LSTD (Bradtke and Barto 1996) is a popular RL algorithm for linear approximation and can be directly used to estimate V π

∗(s) using the trajectory data. LSTD approximates the value function V π

∗(s) = Φ(s)⊺θ in the space expanded by q given bases {ϕi(s)}q i=1, where θ ∈Rq is a unknown parameter and Φ(s) = (ϕ1(s),⋯,ϕq(s))⊺. By projecting the value function into the finite bases, LSTD solves the parameter θ in the form of

[Es[Φ(s)(Φ(s) −γE[Φ(s1)∣s0 = s])⊺]]

−1 Es[rπ

∗(s)Φ(s)].

(12) Using any trajectory data subset with k ≤n data points {(s l(1) j)L j=0,..., (s l(k) j)L j=0} for any (s l(i) j)L j=0 ∈Dn, i = 1,...,k, the estimator of θ is

[ k ∑ i=1 g((s l(i) j)L j=0)]

−1

[ k ∑ i=1 f((s l(i) j)L j=0)], corresponds to the structure of (5), where g((s l(i) j)L j=0) =

L−1

∑ j=0

Φ(s l(i) j)[Φ(s l(i) j) −γΦ(s l(i) (j+1))]⊺, f((s l(i) j)L j=0) =

L−1

∑ j=0 rπ

∗(s l(i) j)Φ(s l(i) j). (13)

This setup aligns with our framework, where Zi = (si j)L j=0 for i = 1,...,n, θ is defined in (12), and the functions g and f are defined in (13).

21561

<!-- Page 5 -->

Our theories also help explain prior empirical findings on experience replay in Q-learning (Zhang and Sutton 2017; Fedus et al. 2020); see Appendix D for details.

Policy Evaluation for Continuous-Time RL. In the second application, we aim to solve the policy evaluation problem for continuous-time RL (e.g., Zhu 2024). Given a policy π(s), unlike the MDP where the value function is a cumulative sum over discrete time steps defined as (9), the value function in continuous-time RL is an expected integral over continuous time,

V π(s) = E[∫

∞

0 e−βtrπ(st)dt∣s0 = s]. (14)

Here β > 0 is a given discounted coefficient, rπ(s) ∈R is a known reward function under the current policy. When the state st ∈S ⊂Rd is driven by the stochastic differential equation (SDE), dst = µ(st)dt + σ(st)dBt, (15)

by Feynman–Kac theorem (Stroock and Varadhan 1997), the value function V (s) satisfies the equation βV π(s) = rπ(s) + Lµ,ΣV π(s), where Lµ,Σ = µ(s) ⋅∇+ 1

2Σ ∶∇2 with Σ = σσ⊺, and Σ ∶∇2 = ∑i,j Σij∂si∂sj. Similar to the classical RL setting, one does not have access to the drift function µ(s) ∈Rd and diffusion function σ(s) ∈Rd×d. Therefore, one cannot solve the above equation directly. The goal of continuous-time policy evaluation is to find the value function satisfying (15) with a set of trajectory data Dn defined in (11). Here the data at time step j are collected at time j∆t with a given time interval ∆t.

Zhu (2024) introduced an algorithm to approximate the value function by solving a Physics-informed Bellman equation (PhiBE) defined as follows β ¯V π α (s) −Lˆµα,ˆΣα ¯V π α (s) = rπ(s), α = 1,2 (16)

where ˆµα(s) = 1 ∆t ∑α j=1 Esj [a(α)

j (sj −s0)∣s0 = s], ˆΣα(s) = 1 ∆t ∑α j=1 Esj [a(α)

j (sj −s0)(sj −s0)⊺∣s0 = s] and α = 1 ∶a(1)

1 = 1; α = 2 ∶a(2)

1 = 2, a(2)

2 = −1

2. (17)

Here ¯V π α (s) serves as α-th order approximation to the continuous-time value function V π(s), where α ∈{1,2}.

Similar to (12), if one approximates the solution ¯V (s) = Φ(s)⊺θ to the PhiBE (16) in the linear function space spanned by Φ(s), one ends up solving for the parameter θ in the following form

[Es[(βΦ(s)⊺−Lˆµα,ˆΣαΦ(s)⊺)Φ(s)]]

−1

Es[rπ(s)Φ(s)].

(18) Zhu (2024) gives the model-free algorithm to estimate the θ using only trajectory data. Specifically, for the α-th order case, using any data subset with k ≤n data points {(s l(1) j)L j=0,..., (s l(k) j)L j=0} for any (s l(i) j)L j=0 ∈Dn, i = 1,...,k, the estimator of θ is

[ k ∑ i=1 g((s l(i) j)L j=0)]

−1

[ k ∑ i=1 f((s l(i) j)L j=0)], corresponds to the structure of (5), where g((s l(i) j)L j=0) =

L−α

∑ j=0

Φ(s l(i) j)[βΦ(s l(i) j) −L¯µα,¯ΣαΦ(s l(i) j)]

⊺

, f((s l(i) j)L j=0) =

L−α

∑ j=0 rπ(s l(i) j)Φ(s l(i) j), (19)

and the estimators of µ(s) and σ(s) are defined as ¯µα(sl j) =

1 ∆t ∑α k=1 a(α)

k (sl

(j+k)−sl j), ¯Σα(sl j) = 1 ∆t ∑α k=1 a(α)

k (sl

(j+k)− sl j)(sl

(j+k) −sl j)⊺with a(α) defined as (17). Compared to LSTD, the second-order PDE-based algorithm with α = 2 incorporates two future steps, resulting in improved accuracy, as illustrated in Figure 1. This setup aligns with our framework with Zi = (si j)L j=0, i = 1,...,n and θ defined in (18), and functions g and f defined in (19).

For both LSTD and the PDE-based approach, once we obtain ˜θn, ˆθU, and ˆθV by applying Algorithm 1, the corresponding estimations of the value function at a test point s are defined as ˜V (s) = Φ(s)⊺˜θn, ˆVU(s) = Φ(s)⊺ˆθU, and ˆVV (s) = Φ(s)⊺ˆθV, where the superscript π is omitted. The variances are, Var(˜V (s)) = Φ(s)⊺Var(˜θn)Φ(s), Var(ˆVU(s)) = Φ(s)⊺Var(ˆθU)Φ(s), and Var(ˆVV (s)) = Φ(s)⊺Var(ˆθV)Φ(s). Thus the reduction of the variance of estimators of θ could be directly evaluated by the reduction in the variance of these estimations.

Kernel Ridge Regression. In the third application, we consider a supervised learning framework where Dn = {(X1,Y1),..., (Xn,Yn)} consists of i.i.d. samples drawn from a distribution FZ. Our goal is to predict the outcome Y ∈R based on the predictors X ∈Rp using kernel methods in an RKHS (Wahba 1990). Let K(⋅,⋅) ∶Rp × Rp →R be a reproducing kernel function. We consider the model Y = f(X) + ϵ, where f belongs to the RKHS defined by K, and ϵ represents random error independent of X. Following Rahimi and Recht (2007) and Dai, Lyu, and Li (2023), the kernel function K(Xi,Xj) can be approximated as ϕ(Xi)⊺ϕ(Xj) using a feature mapping ϕ ∶Rp →Rq, and f(X) can be approximated as ϕ(X)⊺θ, where θ ∈Rq is a parameter vector, defined as θ = [E[ϕ(X)ϕ(X)⊺]]

−1 E[ϕ(X)Y ]. (20)

Using any k data points {(X∗

1,Y ∗ 1),..., (X∗ k,Y ∗ k)} resampled from Dn, the kernel ridge regression estimator of θ is obtained by solving the following optimization problem for a given λ ≥0, argmin θ∈Rq { k ∑ i=1

[Y ∗ i −ϕ(X∗ i)⊺θ]2 + λ∣∣θ∣∣2

2}.

The solution takes the form of

[ k ∑ i=1 g(X∗ i,Y ∗ i) + λIp]

−1

[ k ∑ i=1 f(X∗ i,Y ∗ i)], (21)

where g(X∗ i,Y ∗ i) = ϕ(X∗ i)ϕ(X∗ i)⊺and f(X∗ i,Y ∗ i) = ϕ(X∗ i)Y ∗ i. The setup in (20) and (21) aligns with our framework in (4) and (5), with an added regularization term λIp. This term does not impact the derivation of our main results.

21562

<!-- Page 6 -->

**Figure 2.** Variance differences among the predicted policy values using the LSTD algorithm with m = 50, M = 50, and k/n = 0.3, evaluated across various values of n and B. ˜V (s∗

j) represents the results without experience replay, while ˆVU(s∗ j) and ˆVV (s∗ j) represent the results with experience replay. The red line represents the baseline where the variance difference is 0.

The standard computational cost of the kernel ridge regression with n data points is O(n3) in time (Wahba 1990). The divide-and-conquer algorithm (Zhang, Duchi, and Wainwright 2013) reduces this cost by dividing the dataset into m < n disjoint subsets, each of n/m, and averaging the local solutions across these subsets to construct a global predictor. This approach achieves a trade-off between computational cost and estimation error. In contrast, our approach, which incorporates the experience replay method, also averages over subsets but differs fundamentally in how the subsets are constructed. Instead of partitioning the dataset into non-overlapping subsets, we repeatedly draw B random subsamples, each containing k data points. This resampling allows for overlapping subsets and potential duplication of data points, resulting in a total computational cost of O(Bkq2 + Bq3) in time. Theorems 1 ensures that the conditions limn→∞n/(Bk) →0 and k = o(n) are sufficient for variance reduction. By carefully choosing B and k, our approach achieves both computational savings and variance reduction, offering a practical and efficient alternative to traditional kernel ridge regression, especially for large-scale problems. For instance, setting B = O(n13/8),k = O(n1/8), q = O(n1/8), satisfies the conditions of Theorems 1 and reduces the variance. In this setup, the computational cost is further reduced to O(n2) in time. Additional discussion and examples are provided in Appendix E.

## 4 Numerical

## Experiments

## 4.1 Experiments of Policy Evaluation Using LSTD Algorithm

Firstly, we present the experimental results obtained using LSTD with functions g and f defined in (13). We conduct the experiments in a similar setting as described in Zhu (2024), where the state space S = [−π,π], and the state under policy π is driven by the transition distribution P π(sj+1∣sj) following the normal distribution with expectation seλ/10, variance σ2

2λ(eλ/5−1), where λ = 0.05 and σ = 1. The reward function is set to be rπ

∗(s) = 0.1 ∗[cos3(s) − λs(−3cos2(s)sin(s))−1

2σ2(6cos(s)sin2(s)−3cos3(s))] and the discounted factor γ is set to be e−0.1. We use periodic bases {ϕn(s)}2I+1 k=1 = 1 √π{ 1 √

2,cos(is),sin(is)}I i=1 with I = 4. We consider the case L = 2, where each trajectory has three data points and the state sl j in Dn (11) is sampled at time j/10 for j = 0,...,L and l = 1,...,n. In each experiment, we draw n independent trajectories Dn with the initial state sl

0 of each trajectory sampled from a truncated normal distribution over S with mean 0 and standard deviation 0.1.

We check the performance of the three prediction models on m = 50 test points evenly selected in S, denoted by Stest = {s∗ j}m j=1 with s∗ j = −π+2(j −1)∗π/(m−1). The experiment is conducted M = 50 times, and the variance of the estimated outcome for each test state s∗ j, where j = 1,...,m, is approximated using the sample variance. Three different estimators are used, resulting in approximate variances denoted by Var(˜V (s∗ j)), Var(ˆVU(s∗ j)) and Var(ˆVV (s∗ j)). To assess the variance reduction property, we compare these three variances across all test states.

**Figure 2.** compares the variances using standard boxplots that display the quartile breakdown of the differences {Var(˜V (s∗

j))−Var(ˆVU(s∗ j))}m j=1 and {Var(˜V (s∗ j))− Var(ˆVV (s∗ j))}m j=1, with n ∈{500,1000,2500,5000}, B = {100,500,1000}, and k/n = 0.3. The results clearly demonstrate that for all of the different parameters, the variance differences across all test data points are consistently greater than 0 for both U- and V -statistics-based experience replay methods, particularly in data-scarce settings. As n increases, the variance differences become small as all estimation methods exhibit reduced variance; nonetheless, the variance reduction remains substantial. To illustrate this, we consider the case where n = 5000, B = 1000, and k/n = 0.3, as shown in Figure 1a. From the figure, we observe that the resampled methods demonstrate a significant improvement in variance in this large n scenario. Additional experiments with varying choices of k/n are provided in Appendix G.1, further confirming the robustness of the approach.

## 4.2 Experiments of Policy Evaluation Using PDE-Based Algorithm

Secondly, we present the experimental results obtained using the second-order PDE-based algorithm with functions g and f defined in (19) with α = 2. Similar to Zhu (2024), we consider an experimental setting where the state dynam-

21563

![Figure extracted from page 6](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

**Figure 3.** Variance differences among the predicted policy values using the second-order PDE-based algorithm with m = 50, M = 50, and k/n = 0.3, evaluated across various values of n and B. ˜V (s∗

j) represents the results without experience replay, while ˆVU(s∗ j) and ˆVV (s∗ j) represent the results with experience replay. The red line represents the baseline where the variance difference is 0.

ics are governed by the Ornstein–Uhlenbeck (OU) process ds(t) = λsdt +σdBt with λ = 0.05,σ = 1. The reward function is set to be rπ(s) = β cos3(s)−λs(−3cos2(s)sin(s))− 0.5σ2(6cos(s)sin2(s)−3cos3(s)) with the discounted coefficient β = 0.1. For the OU process, the transition distribution P π(s′∣s) from time t to t + ∆t follows a normal distribution with mean seλ∆t and variance σ2

2λ(e2λ∆t −1). We set ∆t = 0.1, and under this setting, Dn in Section 4.1 follows the same transition distribution, allowing us to use the same simulated trajectory data. Additionally, we employ the same periodic basis functions as described in Section 4.1. The true value function V π(s) then can be exactly obtained from (14), V π(s) = cos3(s).

Note that the experiments using LSTD in Section 4.1 can be considered as a way for estimating V π(s) by discretizing it as a MDP. This approach uses the relationships rπ

∗(s) = rπ(s)∆t and γ = e−β∆t, which hold in the given setting. However, as observed in Figure 1, when the original methods are used, the PDE-based approach generally shows greater accuracy with narrower confidence bands.

We evaluate the performance of the three prediction models using the same way as in Section 4.1. Figure 3 clearly demonstrates that for all of the different parameters, the variance differences across all test data points are consistently greater than 0 for both U- and V -statistics-based experience replay methods. Figure 1b illustrates the large n case where n = 5000, B = 500, and k/n = 0.3.

We present additional experiments with different choices of k/n, along with first-order results in Appendix G.1. With the use of experience replay, the second-order method achieves a greater percentage reduction in variance compared to the LSTD method. Intuitively, the second-order method accounts for two future steps, introducing more stochasticity, which provides greater potential for variance reduction. Moreover, we compare the root mean squared error (RMSE) of the proposed methods with the original method over the m test points across all M experiments for both the LSTD and PDE-based methods in Appendix H.1. The results demonstrate that the combination of experience replay, regardless of the specific resampling method used, not only reduces variance but also tends to achieve smaller prediction errors, further highlighting its effectiveness.

## 4.3 Experiments of Kernel Ridge Regression

Thirdly, we consider a regression setting where for each (X,Y) ∼FZ, the predictor X = (X(1),X(2)) ∈R2 is generated with X(1),X(2) ∼Unif(0,1), and the response is given by Y = e10(−(X(1)−0.25)2−(X(2)−0.25)2) +0.5⋅ e14(−(X(1)−0.7)2−(X(2)−0.7)2) +ϵ, where ϵ ∼N(0,0.25) is independent of X. This setting is widely used in the study of kernel ridge regression and generalized regression models (see, Hainmueller and Hazlett 2014; Wood 2003).

For each experiment, we independently draw n data points from FZ to form the training dataset Dn. We use the krls function in R to fit the kernel ridge regression model with a Gaussian kernel. The λ is chosen as n−2/3. We evaluate the performance of these models on m = 100 test points independently drawn from FZ, denoted by Dtest = {(xj,yj)}m j=1. The experiment is repeated M = 100 times, and the variances of the predicted outcomes ˜yj, ˆyj,U, and ˆyj,V for each test predictor xj, where j = 1,...,m, are approximated using the sample variances, denoted by Var(˜yj), Var(ˆyj,U), and Var(ˆyj,V). As stated in Dai, Lyu, and Li (2023), the predictions ˜yj, ˆyj,U, and ˆyj,V are approximately equal to ϕ(xj)⊺˜θn, ϕ(xj)⊺ˆθU, and ϕ(xj)⊺ˆθV when q is large. Consequently, Var(˜yj), Var(ˆyj,U), and Var(ˆyj,V) serve as estimates for ϕ(xj)⊺Var(˜θn)ϕ(xj), ϕ(xj)⊺Var(ˆθU)ϕ(xj), and ϕ(xj)⊺Var(ˆθV)ϕ(xj), respectively. Therefore, the reduction in the variance of the estimators of θ can be directly assessed by evaluating the reduction in the variance of these predictions. We compare the variances Var(˜yj), Var(ˆyj,U), and Var(ˆyj,V) across all test points.

**Figure 4.** shows the variance differences across test points by plotting the standard quartile breakdown boxplots of {Var(˜yj)−Var(ˆyj,U)}m

j=1 and {Var(˜yj)−Var(ˆyj,V)}m j=1 with B = 50, n ∈{100,150,200,250}, and k ∈{10,15,20}. The results confirm that the variance reduction property holds across all settings for both U- and V -statistics-based experience replay methods. Appendix G.2 includes additional experiments with different B values and evaluations on a real-world dataset from the U.S. Census Bureau on Boston housing, further demonstrating effectiveness.

**Table 1.** presents the time cost reduction achieved by the

21564

![Figure extracted from page 7](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

**Figure 4.** Variance differences in predicted outcomes using kernel ridge regression on the simulated data with M = 100,m = 100 and B = 50, evaluated across various values of n and k. ˜y represents the results without experience replay, while ˆyU and ˆyV represent the results with experience replay. The red line represents the baseline where the variance difference is 0.

k = 10 k = 15 k = 20 n t −tU t −tV t −tU t −tV t −tU t −tV 200 0.369 0.323 0.335 0.272 0.108 0.110 250 3.005 2.905 2.850 2.804 2.954 2.848

**Table 1.** Time cost reduction achieved by experience replay methods (measured in seconds) with B = 50 for different values of k and n.

experience replay methods with B = 50, k ∈{10,15,20}, and n ∈{200,250}. Here, t represents the total time cost across all experiments without experience replay, while tU and tV represent the total time costs with experience replay based on resampled U- and V -statistics, respectively. Time cost was measured as wall-clock time on a single core without parallelization on a laptop with an Apple M2 Pro and 16 GB of RAM. The results demonstrate that, for a fixed B, the experience replay method reduces the computational cost in time, particularly when k is small and n is large. We also compare the RMSE of the proposed methods with the original method in Appendix H.2. The results indicate that incorporating experience replay, regardless of the specific resampling method used, not only reduces variance and time cost but also decreases prediction errors for all settings, especially in data-scarce scenarios.

While our theoretical results apply to both U- and V statistics, empirical results show no major differences between them. In practice, V -statistics are often preferable due to their GPU-friendliness, ease of parallelization, and compatibility with modern machine learning frameworks.

## 5 Conclusion

Experience replay improves stability and efficiency in reinforcement learning, but its theoretical properties are still underexplored. This paper presents a theoretical framework that models experience replay using resampled U- and V statistics, enabling us to establish variance reduction guarantees across policy evaluation and supervised learning tasks. We applied this framework to two policy evaluation algorithms—the LSTD method and a PDE-based model-free algorithm—demonstrating notable improvements in stability and accuracy, particularly in data-scarce settings. Addition- ally, we applied the framework to kernel ridge regression, achieving both significant computational savings and variance reduction. Future research could extend experience replay to federated and active learning settings. For example, using replay to improve communication efficiency and model personalization in federated learning, or selecting informative data subsets for replay in active learning, may address distributed data challenges.

## Acknowledgments

We would like to thank the area chair, senior program committee, and five anonymous referees for constructive suggestions that improve the paper. Dai’s research was supported in part by NIH grant R01DK142026, a Merck Research Award, and a Hellman Fellowship Award. Zhu’s research was supported in part by NSF grant DMS-2529107 and a Hellman Fellowship Award.

## References

Bradtke, S. J.; and Barto, A. G. 1996. Linear leastsquares algorithms for temporal difference learning. Machine Learning, 22(1): 33–57. Dai, X.; Lyu, X.; and Li, L. 2023. Kernel knockoffs selection for nonparametric additive models. Journal of the American Statistical Association, 118(543): 2158–2170. Duan, Y.; Wang, M.; and Wainwright, M. J. 2024. Optimal policy evaluation using kernel-based temporal difference methods. The Annals of Statistics, 52(5): 1927–1952. Fedus, W.; Ramachandran, P.; Agarwal, R.; Bengio, Y.; Larochelle, H.; Rowland, M.; and Dabney, W. 2020. Revisiting fundamentals of experience replay. In International Conference on Machine Learning, 3061–3071. PMLR. Frees, E. W. 1989. Infinite order U-statistics. Scandinavian Journal of Statistics, 29–45. Hainmueller, J.; and Hazlett, C. 2014. Kernel regularized least squares: Reducing misspecification bias with a flexible and interpretable machine learning approach. Political Analysis, 22(2): 143–168. Kober, J.; Bagnell, J. A.; and Peters, J. 2013. Reinforcement learning in robotics: A survey. The International Journal of Robotics Research, 32(11): 1238–1274.

21565

![Figure extracted from page 8](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-AAAI-variance-reduction-via-resampling-and-experience-replay/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Kong, J.; Pfeiffer, M.; Schildbach, G.; and Borrelli, F. 2015. Kinematic and dynamic vehicle models for autonomous driving control design. In 2015 IEEE Intelligent Vehicles Symposium (IV), 1094–1099. IEEE. Lin, L.-J. 1992. Self-improving reactive agents based on reinforcement learning, planning and teaching. Machine Learning, 8: 293–321. Mentch, L.; and Hooker, G. 2016. Quantifying uncertainty in random forests via confidence intervals and hypothesis tests. Journal of Machine Learning Research, 17(26): 1–41. Mnih, V.; Kavukcuoglu, K.; Silver, D.; Rusu, A. A.; Veness, J.; Bellemare, M. G.; Graves, A.; Riedmiller, M.; Fidjeland, A. K.; Ostrovski, G.; et al. 2015. Human-level control through deep reinforcement learning. Nature, 518(7540): 529–533. Peng, W.; Coleman, T.; and Mentch, L. 2022. Rates of convergence for random forests via generalized U-statistics. Electronic Journal of Statistics, 16(1): 232–292. Rahimi, A.; and Recht, B. 2007. Random features for largescale kernel machines. Advances in Neural Information Processing Systems, 20. Schaul, T. 2015. Prioritized Experience Replay. arXiv preprint arXiv:1511.05952. Shawe-Taylor, J.; and Cristianini, N. 2004. Kernel methods for pattern analysis. Cambridge University Press. Shieh, G. S. 1994. Infinite order V-statistics. Statistics & Probability Letters, 20(1): 75–80. Silver, D.; Huang, A.; Maddison, C. J.; Guez, A.; Sifre, L.; Van Den Driessche, G.; Schrittwieser, J.; Antonoglou, I.; Panneershelvam, V.; Lanctot, M.; et al. 2016. Mastering the game of Go with deep neural networks and tree search. Nature, 529(7587): 484–489. Song, Y.; Chen, X.; and Kato, K. 2019. Approximating high-dimensional infinite-order U-statistics: Statistical and computational guarantees. Electronic Journal of Statistics, 13(2). Stroock, D. W.; and Varadhan, S. S. 1997. Multidimensional diffusion processes, volume 233. Springer Science & Business Media. Sutton, R. S.; and Barto, A. G. 2018. Reinforcement learning: An introduction. MIT press. Tu, S.; and Recht, B. 2018. Least-squares temporal difference learning for the linear quadratic regulator. In International Conference on Machine Learning, 5005–5014. PMLR. Wahba, G. 1990. Spline models for observational data. SIAM. Wood, S. N. 2003. Thin plate regression splines. Journal of the Royal Statistical Society Series B: Statistical Methodology, 65(1): 95–114. Zhang, S.; and Sutton, R. S. 2017. A deeper look at experience replay. arXiv preprint arXiv:1712.01275. Zhang, Y.; Duchi, J.; and Wainwright, M. 2013. Divide and conquer kernel ridge regression. In Conference on Learning Theory, 592–617. PMLR.

Zhou, Z.; Mentch, L.; and Hooker, G. 2021. V-statistics and variance estimation. Journal of Machine Learning Research, 22(287): 1–48. Zhu, Y. 2024. PhiBE: A PDE-based Bellman Equation for Continuous Time Policy Evaluation. arXiv preprint arXiv:2405.12535.

21566
