---
title: "Policy Zooming: Adaptive Discretization-based Infinite-Horizon Average-Reward Reinforcement Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39412
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39412/43373
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Policy Zooming: Adaptive Discretization-based Infinite-Horizon Average-Reward Reinforcement Learning

<!-- Page 1 -->

Policy Zooming: Adaptive Discretization-based Infinite-Horizon Average-Reward

Reinforcement Learning

Avik Kar1, Rahul Singh1

1Indian Institute of Science avikkar@iisc.ac.in, rahulsingh0188@gmail.com

## Abstract

We study infinite-horizon average-reward reinforcement learning for continuous space Lipschitz Markov decision processes (MDPs) in which an agent can play policies from a given set Φ. The proposed algorithms efficiently explore the policy space by “zooming” into the “promising regions” of Φ, thereby achieving adaptivity gains in the performance. We upper bound the regret as ˜O

T 1−d−1 eff.

, where deff. = dΦ z + 2 for our model-free algorithm PZRL-MF and deff. = 2dS +dΦ z +3 for our model-based algorithm PZRL-MB. Here, dS is the dimension of the state space, and dΦ z is the zooming dimension given a set of policies Φ. dΦ z is an alternative measure of the complexity of the problem, and it depends on the underlying MDP as well as on Φ. Hence, the proposed algorithms exhibit low regret in case the problem instance is benign and/or the agent competes against a low-complexity Φ (that has a small dΦ z). When specialized to the case of finite-dimensional policy space, we obtain that deff. scales as the dimension of this space under mild technical conditions; and also obtain deff. = 2, or equivalently ˜O(

√

T) regret for PZRL-MF, under a curvature condition on the average reward function that is commonly used in the multi-armed bandit (MAB) literature.

Code — https://github.com/avik-kar/Policy_zooming Extended version — https://arxiv.org/pdf/2405.18793

## Introduction

Reinforcement Learning (RL) (Sutton and Barto 2018) is a popular framework in which an agent repeatedly interacts with an unknown environment modeled by an MDP (Puterman 2014) and the goal is to choose actions sequentially in order to maximize the cumulative rewards earned by the agent. We study infinite-horizon average reward MDPs in continuous state and action spaces endowed with a metric, in which the transition kernel and reward functions are Lipschitz (Assumption 2.1). The class of Lipschitz MDPs covers a broad class of problems, such as the class of linear MDPs (Jin et al. 2020), RKHS MDPs (Chowdhury and Gopalan 2019), linear mixture models, RKHS approximation, and the nonlinear function approximation framework considered in Osband and Van Roy (2014) and Kakade et al. (2020). See Maran et al. (2024a,b) for more details, or refer to Figure 1. Even though

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Lipschitz

Strongly Smooth

Kernelized

Linear

LQR

**Figure 1.** Relations among families of continuous space RL problems. LQR stands for Linear Quadratic Regulator (Abbasi-Yadkori and Szepesvári 2011). Our assumptions correspond to the green set. Diagram is taken from Maran et al. (2024a).

discrete and linear MDPs have been extensively studied in the literature, they might not be suitable for many real-world applications since it is becoming increasingly common to deploy RL and control algorithms in systems that are nonlinear and continuous (Nair et al. 2023; Kumar et al. 2021).

Let dS and dA denote the dimensions of the state and action spaces, respectively, and define d:= dS + dA. For episodic Lipschitz MDPs, the regret scales as ˜O

K1−d−1 eff. 1, where K is the number of episodes and deff. is the effective dimension, which depends on both the underlying MDP and the algorithm. For instance, using a fixed discretization yields deff. = d + 2 (Song and Sun 2019). In contrast, adaptive algorithms can exploit MDP structure to reduce deff.. Prior works (Cao and Krishnamurthy 2020; Sinclair, Banerjee, and Yu 2023) employ adaptive discretization and a technique called “zooming,” which reduces deff. to dz + 2, where dz is the zooming dimension. However, this notion of dz, designed for episodic settings, fails to capture adaptivity in average reward problems. Specifically, as the horizon grows, dz →d, making adaptive methods no better than fixed discretization. To address this, Kar and Singh (2025) introduced a new definition of zooming dimension tailored for average reward RL, and achieved deff. = 2dS + dz + 3, with dz ≤d. However, their methods assume compactness of the stateaction space and focus solely on the complexity of the MDP.

In this work, we propose adaptive discretization-based al-

1 ˜O suppresses poly-logarithmic dependence in K or T.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22527

<!-- Page 2 -->

1 3 Parameter 1

−1.00

−0.01

Parameter 2

0.19

0.69

0.55

0.19

0.7 0.66 0.37

0.19

0.59

0.54

0.21

(a) PZRL-MF

1 3 Parameter 1

−1.00

−0.01

Parameter 2

0.59

0.67

0.71

0.47

0.19

0.71

0.68

0.5

0.2

0.19

0.64

0.51

0.28

0.19

0.19

0.52

0.33

0.2

0.19

0.19

0.38

0.25

0.19

0.19

0.19

(b) Policy UCB

**Figure 2.** We show the policies activated by different algorithms for one single trajectory of the transmission scheduling example (See Section 5). The radius of the balls around an active policy is proportional to its average reward. Uniform discretization-based algorithms waste resources to learn a larger number of policies, whereas adaptive algorithms activate more policies from the near-optimal regions.

gorithms that (i) handle non-compact spaces and (ii) apply to the setups efficiently where the performance is to be compared against a known class of policies. Specifically, we propose the zooming dimension given a policy class Φ, denoted by dΦ z, that captures the joint complexity of the MDP and the comparator policy class. Thus, we refine the idea of dz to depend on a policy class as well. If the optimal policy belongs to a “simple” class, this refinement enables significantly smaller dΦ z, yielding dΦ z ≪d. We analyze regret with respect to a given policy class Φ (1), a widely accepted approach in complex systems (Hazan and Singh 2022; Rakhlin and Sridharan 2014). Our model-free algorithm PZRL-MF and model-based algorithm PZRL-MB achieve regret bounds with effective dimensions deff. = dΦ z +2 and deff. = 2dS +dΦ z +3, respectively. It turns out that our algorithms activate policies from the given policy class in an efficient way as compared to an algorithm that uses a uniform grid for policy search. Figure 2 depicts that PZRL-MF activates fewer policies from suboptimal regions and more from near-optimal regions as compared to a naive uniform discretization.

To illustrate the intuition behind zooming, we revisit its origin in the simpler setting of Lipschitz MABs (Kleinberg, Slivkins, and Upfal 2008).

Lipschitz MABs: The Zooming Algorithm. The agent maintains a set of “active arms,” and their “confidence balls” whose radii are equal to the confidence radii associated with the corresponding arm’s estimated reward. Thanks to Lipschitz continuity, rewards of nearby arms can be inferred from the active ones.2 New arms are activated only if not covered by existing confidence balls. The agent selects the arm with the highest upper confidence bound (UCB) index. Because the confidence radius shrinks with the number of plays, the algorithm “zooms in” on promising regions, those with a high UCB index. This adaptive behavior yields an effective dimension of dz + 2. A similar idea has been explored in (Bubeck et al. 2011).

2Let a be an active arm with confidence radius η and empirical mean ˆµa. Then, for any arm a′ in its confidence ball, the mean reward lies in [ˆµa −(1+L)η, ˆµa +(1+L)η] with high probability.

## 1.1 Challenges

For MABs, the zooming algorithm plays only from amongst the active arms since the UCB index of an active arm turns out to be an optimistic estimate of the mean reward of each arm lying inside its confidence ball. For policies, however, rewards are not unbiased estimates of the long-term average unless the controlled Markov process (CMP) is at stationarity, making confidence radius design and optimism proofs more involved. Moreover, to our knowledge, model-free UCB indices have not been explored for average reward RL, not even in tabular MDPs. Another challenge lies in selecting an appropriate norm for measuring distances between policies (note that since the policy space is not finite-dimensional, all norms are not equivalent).

1.2 Contributions 1. To the best of our knowledge, this is the first work to provide finite-time regret bounds for average reward RL in general state-action space MDPs with d > 1. Prior works (Ortner and Ryabko 2012; Qian et al. 2019; Wei et al. 2021; He, Zhong, and Yang 2023) are either limited to finite action spaces or assume dS = 1.

2. We develop two algorithms, PZRL-MF (model-free) and PZRL-MB (model-based), that use policy-based zooming and UCB methods (Lattimore and Szepesvári 2020). Our main novelty is a new complexity measure for average reward RL: the zooming dimension dΦ z, defined via policy covers of Φ. We show regret bounds of ˜O

T 1−d−1 eff.

with deff. = dΦ z + 2 for PZRL-MF, and deff. = 2dS + dΦ z + 3 for PZRL- MB. Importantly, a small dΦ z does not imply the MDP belongs to nice class of MDPs, such as linear MDPs or tabular MDPs. When Φ is parameterized over W ⊂Rdw, we show dΦ z ≤dw under mild assumptions. For MDPs with bi-Lipschitz average reward functions, we get deff. = 2 and hence an O(

√

T) regret for PZRL-MF.

3. Along the way, we prove a novel sensitivity result (Theorem 4.1) for Markov processes on general state spaces (Meyn and Tweedie 2012). We bound the distance between the stationary distributions of Markov chains in terms of a weighted distance measure (13) between the transition kernels, improving over the existing results (Mitrophanov 2005; Mouhoubi 2021) that bounds the same quantity in terms of the sup distance between the transition kernels.

4. Existing algorithms for general state spaces are often computationally intractable without linearity (Ayoub et al. 2020) or deterministic dynamics (Wu et al. 2024). In contrast, our methods are efficient, and in fact, PZRL-MF has the same computational complexity as zooming for MABs.

5. In Section 5, we demonstrate the applicability of our framework via a transmission scheduling problem. This MDP is neither tabular nor linear; however, the optimal policy is known to belong to a known class of policies that can be described by finitely many parameters. Simulation results show the practical relevance of our algorithms.

## 1.3 Past Works Lipschitz episodic MDPs:

Domingues et al. (2021) uses smoothing kernels to estimate the transition kernel, and ob-

22528

<!-- Page 3 -->

tains a regret upper bound with deff. = 2d + 1. Cao and Krishnamurthy (2020) performs adaptive discretization and zooming and achieves regret upper bound with deff. = dz +2, where dz is the zooming dimension defined specifically for the episodic case. Sinclair, Banerjee, and Yu (2023) also obtains adaptivity gains with deff. = dz + dS for a model-based algorithm. The same work also shows a regret lower bound of Ω(K1−(dz+2)−1). This lower bound is worse than the O(

√

K) dependence that is achievable for the tabular case or the function approximation techniques. This is not surprising since Lipschitz MDPs are a broader class of MDPs (Maran et al. 2024a,b); See Figure 1. Even though function approximation techniques yield an O(

√

K) regret, this comes at the expense of a larger prefactor in the regret bound as compared to Lipschitz MDPs. Moreover, function approximation techniques are computationally inefficient unless the underlying MDP is linear, and the feature maps are known. The knowledge of feature maps seems to be a restrictive assumption since learning features efficiently is an active topic in itself (Modi et al. 2024).

Average reward RL: Tabular MDPs are well-studied by now, and popular algorithms with a tight ˜O(

√

DSAT) regret bound exist (Jaksch, Ortner, and Auer 2010; Tossou, Basu, and Dimitrakakis 2019); where D is the MDP diameter. In contrast, continuous MDPs have only recently gained attention. Wei et al. (2021) uses function approximation, in which the relative value function is a linear function of the features, and obtains a ˜O(

√

T) regret. He, Zhong, and Yang (2023) uses function approximation techniques and obtains a regret bound of ˜O(poly(dE, B)√dF T), where B is the span of the relative value function. When the transition kernel of the underlying MDP is α-Hölder continuous and infinitely often smoothly differentiable, then Ortner and Ryabko (2012) obtains a regret upper bound with deff. = (2d+2α)/α. Kar and Singh (2025) performs adaptive discretization and zooming and achieves regret upper-bound with deff. = 2dS + dz + 3 for Lipschitz MDPs with compact state-action spaces.

## 2 Problem Setup

Notation. N denotes the set of natural numbers. Let (Ω, F) be a measurable space, and let µ: F 7→R be a signed measure, then we denote total variation norm (Folland 2013) of µ by ∥µ∥T V, i.e., ∥µ∥T V:= sup{P i |µ(Bi)|: {Bi}i ⊂F partitions Ω}. For B ⊆S, diam (B):= sups,s′∈B ρ(s, s′). We denote a ∧b the minimum, and a ∨b the maximum of a, b ∈R. ⌈a⌉denotes the smallest integer that is larger than a for a ∈R. In general, we use a superscript (f) ((b)) to indicate that an object is associated with algorithm PZRL-MF (PZRL-MB).

Let M = (S, A, p, r) be an MDP, where the dimensions of the state-space S and action-space A are dS and dA, respectively. The spaces S, A are endowed with metrics ρS and ρA, respectively. The space S × A is endowed with a metric ρ that is sub-additive, i.e., we have, ρ ((s, a), (s′, a′)) ≤ ρS(s, s′) + ρA(a, a′), for all (s, a), (s′, a′) ∈S × A. We let S be endowed with Borel σ-algebra BS. The state and the action taken at time t are denoted by st, at, respectively. The transition kernel is p: S × A × BS →[0, 1], i.e., P (st+1 ∈B|st = s, at = a) = p(s, a, B), a.s., for all (s, a, B) ∈S × A × BS, t ∈{0} ∪N, and is not known to the agent. The reward function r: S × A →[0, 1] is a measurable map, and the reward earned by the agent at time t is equal to r(st, at). A stationary deterministic policy is a measurable map ϕ: S →A that implements the action ϕ(s) when the system state is s. Let ΦSD be the set of all such policies. The infinite horizon average reward for the MDP M under a policy ϕ is denoted by JM(ϕ), and is defined as,

JM(ϕ):= lim inf t→∞

## 1 T E

"T −1 X t=0 r(st, ϕ(st))

#

.

The maximum average reward attainable with a set of policies Φ ⊆ΦSD is denoted by J⋆

M,Φ. The regret of a learning algorithm ψ w.r.t. a class of comparator policies Φ until T is defined as (Rakhlin and Sridharan 2014),

RΦ(T; ψ):= TJ⋆

M,Φ −

T −1 X t=0 r(st, at). (1)

The current work derives an upper bound on RΦ(T; ψ) in terms of the zooming dimension, a joint complexity measure of class Φ and the MDP M when the algorithms are only allowed to play policies from Φ. Note that if Φ contains an optimal policy, then RΦ(T; ψ) is the usual regret. An MDP is Lipschitz if it satisfies the following properties. Assumption 2.1 (Lipschitz continuity). (i) The reward function r is Lr-Lipschitz, i.e., ∀s, s′ ∈S, a, a′ ∈A,

|r(s, a) −r(s′, a′)| ≤Lrρ ((s, a), (s′, a′)).

(ii) The transition kernel p is Lp-Lipschitz, i.e., ∀s, s′ ∈

S, a, a′ ∈A,

∥p(s, a, ·) −p(s′, a′, ·)∥T V ≤Lpρ ((s, a), (s′, a′)).

While studying infinite-horizon average reward MDPs, some sort of ergodicity assumption is required. In fact, uniform ergodicity is the weakest known sufficient condition that ensures efficient computation of an optimal policy even when the MDP is known (Arapostathis et al. 1993). Assumption 2.2 (Ergodicity). Let Φ ⊆ΦSD be the comparator class of policies. The CMP {st}t that is induced by transition kernel p under application of any ϕ ∈Φ is uniformly ergodic (Douc et al. 2018), that is, there exist two constants, C ∈(0, ∞) and α ∈(0, 1) and for every ϕ ∈Φ, there exists a unique distribution µ(∞)

ϕ,p such that µ(t)

ϕ,p,s −µ(∞)

ϕ,p

T V ≤Cαt, ∀s ∈S, t ∈{0} ∪N, (2)

where µ(t)

ϕ,p,s denotes the distribution of st given s0 = s.

We call µ(∞)

ϕ,p as the stationary distribution of the CMP induced by p under the application of policy ϕ. We need Φ to be endowed with an appropriate metric ρΦ such that Φ is bounded and JM is a Lipschitz function on Φ. In fact, under Assumption 2.1 and Assumption 2.2, JM is Lipschitz w.r.t. the metric ρΦ set equal to the metric induced by ∞norm.

22529

<!-- Page 4 -->

Further, JM is Lipschitz w.r.t. a weighted distance measure too under a mild technical condition. We show these two results in Theorem 4.1. For a discussion on the metric spaces, see Appendix C of the extended version. We next define the zooming dimension dΦ z, a joint complexity measure for the problem instance and the comparator policy class Φ.

Zooming dimension. Suboptimality of a policy ϕ w.r.t. Φ is defined as ∆Φ(ϕ):= J⋆

M,Φ −JM(ϕ). Define the sets of policies Φγ:= {ϕ ∈Φ | ∆Φ(ϕ) ∈(γ, 2γ]}, and Φ≤γ:= {ϕ ∈Φ | ∆Φ(ϕ) ≤γ}. Then, the zooming dimension of the problem given the policy space Φ is defined as dΦ z:= inf n d′ > 0 | N γ cz (Φγ) ≤cz1γ−d′, and

N γ cz (Φ≤γ) ≤cz2γ−d′, ∀γ ≥0 o

, (3)

where Nγ (Φ′) denotes the γ-covering number of Φ′ ⊆Φ w.r.t. metric ρΦ, cz1 and cz2 are problem-dependent constants, cz:= 2(max {2, Cub} + LJ). Cub is a problem-dependent constant. Remark 2.3. We note that even if the policy class is highdimensional, the zooming dimension could be small, as it is a measure of the size of the set of near-optimal policies.

## 3 Algorithm

We propose a model-free algorithm PZRL-MF and a modelbased algorithm PZRL-MB. Both the algorithms combine policy-based zooming with the principle of optimism in the face of uncertainty (Lattimore and Szepesvári 2020). They maintain a set of active policies, compute their UCB indices, and then play an active policy with the highest UCB index in the current episode. Its zooming component zooms in and activates only those policies from Φ, for which it is not possible to generate a good estimate of its performance using the performance estimates of nearby active policies. However, they differ in the way in which they compute UCB indices and activate new policies and hence are discussed separately. The algorithms are summarized in Algorithm 1.

## 3.1 PZRL-MF Policy

Diameter. Diameter at time t is defined as, diam(f)

t (ϕ):=

C 1 −α



 s c(f)

d log

T δ

1 ∨Nt(ϕ) + 1 + Kt(ϕ) 1 ∨Nt(ϕ)



, ϕ ∈Φ, (4)

where Nt(ϕ) is the number of plays of the policy ϕ until time t, Kt(ϕ) is the number of episodes that began before time t, and in which ϕ was played, while c(f)

d is an appropriate constant.

Active Policies. Φact.

t denotes the set of policies active at time t. Define the following ball in the policy space,

Bϕ,t:= n ϕ′ ∈Φ: ρΦ(ϕ′, ϕ) ≤diam(f)

t (ϕ)

o

. (5)

Since the confidence ball associated with a policy shrinks when it is played, in the possible event that ∪ϕ∈Φact.

t Bt(ϕ)

## Algorithm

1: Policy Zooming for RL (PZRL-MF/PZRL-MB)

Input Horizon T, confidence parameter δ, ergodicity coefficient α and policy class Φ Initialize h = 0, k = 0, Φact.

0 = {}. for t = 0 to T −1 do if h ≥Hk then k ←k + 1, h ←0 Update the set of active policies Φact.

t ⊂Φ For every ϕ ∈Φact.

t compute Indext(ϕ), where Indext(ϕ) = Index(f)

t (ϕ) (6) if PZRL-MF, Indext(ϕ) = Index(b)

t (ϕ) (12) if PZRL-MB. Choose ϕ(k) ∈arg maxϕ∈Φact.

t Indext(ϕ). Hk = 1 ∨Nt(ϕ(k)) end if h ←h + 1 Play at = ϕ(k)(st), observe st+1 and receive r(st, at). end for does not cover the set Φ anymore, the proposed algorithm activates a new policy to ensure that the union of confidence balls of the active policies covers Φ. Thus, PZRL-MF possesses the covering invariance property, i.e., ∪ϕ∈Φact.

t Bϕ,t covers Φ at all times.

Model-free UCB Index. Let ϕt denote the policy played at time t. The UCB index at time t is defined as

Index(f)

t (ϕ):= 1 Nt(ϕ)

t−1 X i=0

I{ϕi=ϕ}r(si, ϕ(si))

+ (1 + LJ) diam(f)

t (ϕ), ϕ ∈Φact.

t, (6)

where LJ is the Lipschitz constant associated with JM.

## 3.2 PZRL-MB

We assume S to be bounded for PZRL-MB. PZRL-MB maintains an adaptive partition of the state space S for each active policy. We use Pϕ,t to denote the state partition corresponding to policy ϕ at time t; see Appendix A.1 in the extended version for more details on the procedure to create these partitions. Loosely speaking, as time progresses, Pϕ,t is finer in those regions of S that have been visited relatively more number of times while playing ϕ. Pϕ,t consists of a certain type of subsets of S called cells. The cells comprising Pϕ,t are called active cells at time t corresponding to policy ϕ. Let q−1 ϕ,t(s) be the active cell corresponding to ϕ at time t that contains the state s. Policy Diameter. The model-based policy diameter for ϕ ∈ Φ is defined as follows:

diam(b)

t (ϕ):=

Z

S diam q−1 ϕ,t(s)

µ(∞)

ϕ,p (ds). (7)

Policy balls for PZRL-MB are defined similar to (5), replacing diam(f)

t (ϕ) with diam(b)

t (ϕ). Similar to PZRL-MF, PZRL- MB maintains a set of active policies, Φact.

t that satisfies the covering invariance property.

Approximate Diameter: The agent cannot compute diam(b)

t (ϕ) since it does not know µ(∞)

ϕ,p. However, the agent

22530

<!-- Page 5 -->

can compute a “tight” lower bound of diam(b)

t (ϕ), which can then be used in (5) in lieu of diam(b)

t (ϕ). This approximation causes the regret upper bound to increase only by a constant factor (See Appendix A.3 and A.6 in the extended version).

Model-based UCB Index. PZRL-MB evaluates the UCB indices of the active policies by using an estimate of the transition kernel. The algorithm constructs a set of plausible discretized transition kernels using its estimate (10). A curated bias term is added to the discretized reward function in order to overcome the discretization error. Then, the UCB indices are computed using an iterative algorithm (11), similar to the policy evaluation algorithm. Computation of the UCB index involves the following three steps:

(i) Estimating the Transition Kernel: Denote Sϕ,t to be the set of representative points of the cells in Pϕ,t, and denote

¯Sϕ,t to be the set of representative points of all the cells of size of the smallest cell in Pϕ,t. At time t, for every active policy ϕ, PZRL-MB constructs the empirical transition distribution,

ˆp(d)

ϕ,t(s, ·) with the width of the bins set equal to the diameter of q−1 ϕ,t(s) for every s ∈Sϕ,t. Then a continuous extension of

ˆp(d)

ϕ,t, ˆpϕ,t is computed. ˆpϕ,t is again discretized with the width of the bins set equal to the diameter of the smallest active cell. This discrete estimate is denoted by ℘Sϕ,t→¯Sϕ,t,ˆpϕ,t. For a detailed discussion on the estimation of the transition kernel, see Appendix A.2 in the extended version of the paper.

(ii) Confidence Ball: For a policy ϕ and a representative state s ∈Sϕ,t, the confidence radius associated with the estimate ℘Sϕ,t→¯Sϕ,t,ˆpϕ,t is defined as follows, ηϕ,t(s):=3



  c(b)

d log

Tδ−1

Pt−1 i=0 In si∈q−1 ϕ,t(s)i o



 

1 dS +2

+ (3(1 + Lϕ)Lp + Cp) diam q−1 ϕ,t(s)

, (8)

where c(b)

d > 0 is a constant that is discussed in Lemma D.2 in the extended version, Cp is as described in Assumption 4.3, and Lϕ is the Lipschitz constant associated with ϕ, i.e., for all s, s′ ∈S, ρA(ϕ(s), ϕ(s′)) ≤LϕρS(s, s′). It follows from the rule used for activating a new cell that we have, ηϕ,t(s) ≤Cη,ϕ diam q−1 ϕ,t(s)

, (9)

for every s ∈Sϕ,t, where Cη,ϕ:= 3 (1 + (1 + Lϕ)Lp) + Cp. Let Θϕ,t denote the set of all possible discretized transition kernels that describe outgoing transition probabilities from points in ¯Sϕ,t, with a support on the discrete state space

¯Sϕ,t. We define a set of transition probability kernels associated with ℘Sϕ,t→¯Sϕ,t,ˆpϕ,t as follows,

Cϕ,t:= θ ∈Θϕ,t | θ(¯s, ·) −℘Sϕ,t→¯Sϕ,t,ˆpϕ,t(s, ·)

1 ≤ηϕ,t(s) for every s ∈Sϕ,t, ¯s ∈¯Sϕ,t ∩q−1 t (s)

, (10)

(iii) Computing the UCB Indices of Active Policies: Let us fix a time t. To obtain the UCB index of a policy ϕ ∈Φ, we perform the following iterations,

V ϕ,t

0 (s) = 0,

V ϕ,t i+1(s) = r(s, ϕ(s)) + (1 + Lϕ)Lr diam q−1 ϕ,t(s)

+ max θ∈Cϕ,t

X s′∈¯Sϕ,t θ(s, s′)V ϕ,t i (s′), (11)

s ∈¯Sϕ,t, i ∈Z+. The difference of two consecutive iterates of (11) is shown to converge in Lemma A.4 in the extended version. We define the UCB indices as follows,

Index(b)

t (ϕ):= lim i→∞

V ϕ,t i+1(s) −V ϕ,t i (s)

+ LJ diam(b)

t (ϕ), (12)

for any s ∈¯Sϕ,t. Remark 3.1. Similar to the zooming algorithm for bandits (Kleinberg, Slivkins, and Upfal 2019), we assume access to an oracle that takes as input a finite collection of open balls, and then either declares that they cover Φ, or outputs a point that is uncovered. In general, such an oracle may not be computationally efficient. However, when Φ has a finite-dimensional parameterization, we can perform a grid search.

## 4 Regret Analysis In this section, we present our main results,

Theorem 4.2 and Theorem 4.5, that yield upper bounds on the regret of PZRL- MF and PZRL-MB, respectively. Before presenting these, we first show that the average reward function JM(·) is a Lipschitz function of the policies w.r.t. the sup-norm distance. Furthermore, under a mild assumption, it is also a Lipschitz function of the policies w.r.t. a weighted distance measure. This result provides an important insight into selecting an appropriate norm for defining the zooming dimension. Define ρΦ,∞(ϕ, ϕ′):= sup s∈S ρA(ϕ(s), ϕ′(s)), ∀ϕ, ϕ′ ∈Φ.

Consider a probability measure ν on (S, BS). Define the metric, ρΦ,ν(ϕ, ϕ′):=

Z

S ρA(ϕ(s), ϕ′(s)) dν(s), (13)

Theorem 4.1. Let the MDP M satisfy Assumption 2.1 and 2.2. (i) Then, the infinite horizon average reward is LJ,∞- Lipschitz w.r.t. the metric ρΦ,∞, i.e., for ϕ, ϕ′ ∈Φ we have,

|JM(ϕ) −JM(ϕ′)| ≤LJ,∞ρΦ,∞(ϕ, ϕ′), where,

LJ,∞:= Lr + Lp 2(1 −α)

l log 1 α (C)

m

+ 1

. (14)

(ii) Furthermore, if µ(∞)

ϕ,p (ξ) ≤κν(ξ), ∀ξ ∈BS, ϕ ∈Φ, for some probability measure ν and a constant κ > 0, then JM(·) is LJ,ν-Lipschitz w.r.t. the metric ρΦ,ν, i.e., for ϕ, ϕ′ ∈ Φ we have,

|JM(ϕ) −JM(ϕ′)| ≤LJ,νρΦ,ν(ϕ, ϕ′), where, LJ,ν:= κLJ,∞.

22531

<!-- Page 6 -->

The above theorem is proved in Appendix B of the extended version. The next two theorems are the main results of this work, and bound the regrets of PZRL-MF and PZRL-MB. Theorem 4.2. If the MDP M satisfies Assumptions 2.1 and 2.2, then with a probability at least 1 −δ, the regret of PZRL-MF, i.e. RΦ(T; PZRL-MF), is bounded above as

˜O(T 1−d−1 eff.) where deff. = dΦ z + 2. The following assumptions are required for the analysis of PZRL-MB. Assumption 4.3 (Bounded Radon-Nikodym derivative). The probability measures {p(s, ϕ(s), ·)}s are absolutelycontinuous w.r.t. the Lebesgue measure on (S, BS), with density functions given by {fϕ,s}s for every ϕ ∈Φ. These densities satisfy

∂fϕ,s(s+)

∂s+(i)

∞

≤Cp, ∀s ∈S, i = 1, 2,..., dS, where s+ = (s+(1), s+(2), · · ·, s+(dS)). Assumption 4.4. There exists κ′ > 0 such that for every ζ ⊆BS, µ(∞)

ϕ,p (ζ) ≥κ′λ(ζ), where λ is the Lebesgue measure (Billingsley 2017) on (S, BS).

The above two assumptions are not restrictive. See Remark 4.7 in the extended version for more details on this. We use ΦLip. to denote the class of Lipschitz policies. Theorem 4.5. Let Φ ⊆ΦLip.. If the MDP M satisfies Assumption 2.1, 2.2, 4.3 and 4.4, then with a probability at least 1 −δ, the regret of PZRL-MB, i.e. RΦ(T; PZRL-MB), is upper-bounded as ˜O(T 1−d−1 eff.) where deff. = 2dS +dΦ z +3.

Refer to Appendix G in the extended version for detailed proofs of the above two results. Here, we provide a generic proof sketch.

Proof sketch. We decompose the regret as follows,

RΦ(T; ψ) =

K(T) X k=1 τk+1−1 X t=τk

J⋆

M,Φ −JM(ϕ(k))

| {z } (a)

+

K(T) X k=1 τk+1−1 X t=τk

JM(ϕ(k)) −r(st, ϕ(k)(st))

| {z } (b)

, where ϕ(k) denotes the policy played in the k-th episode, τk denotes the time when the k-th episode starts, and K(T) denotes the total number of episodes till time T. We bound the terms (a) and (b) separately.

Bounding (a): This term is further decomposed into the sum of the regrets arising due to playing policies from the sets Φγ, where γ assumes the values 2−i, i = 1, 2,..., ⌈log (1/ϵ)⌉, and ϵ = T −d−1 eff.. Cumulative regret arising from playing policies not in the set ∪⌈log(1/ϵ)⌉ i=1 Φ2−i is bounded by ϵT. Regret due to playing policies from Φγ is bounded in the following three steps:

(1) First, we derive a condition under which a γ-suboptimal policy is no longer played.

(2) Then, we deduce an upper bound of the number of plays of a policy ϕ in terms of its suboptimality gap by concluding that the condition stated in (1) holds when ϕ has been played sufficiently many times.

(3) Then, we establish an upper bound on the number of policies that are activated by the algorithms from Φγ.

The product of two upper bounds discussed in (2) and (3), when multiplied with 2γ, yields regret from playing policies in Φγ. We then add these regret terms corresponding to different sets Φγ, where γ = 2−i and i = 1, 2,..., ⌈log (1/ϵ)⌉; to this we add the regret arising due to playing policies with suboptimality less than ϵ, which is bounded by ϵT.

Bounding (b): We show that term (b) is bounded as O(K(T)) using uniform ergodicity. Then we show that the total number of episodes for PZRL-MF as well as PZRL- MB are bounded above by O

T dΦ z /deff.

, where deff. = dΦ z +2 and deff. = 2dS + dΦ z + 3, respectively. We obtain the desired regret bound after summing the upper bounds on (a) and (b).

Remark 4.6 (Discontinuous Policies). The regret analysis of PZRL-MB extends to policies with discontinuities, provided all discontinuities lie on the boundaries of active cells. This condition can be enforced by redefining the cells (Definition A.1 in the extended version) accordingly. For simplicity, we define the cells using dyadic cubes.

The next result quantifies an upper bound on deff. for an important class of policies; See Appendix C in the extended version for the proof. Corollary 4.7 (Finite parameterization). We now consider a set Φ that consists of policies that have been parameterized by finitely many parameters from the set W ⊂RdW. For each w ∈W, let ϕ(·; w): S →A be the pol- icy parameterized by w. Assume that the policies satisfy LW ρΦ(ϕ(·; w), ϕ(·; w′)) ≥∥w −w′∥2 for all w, w′ ∈W. We have deff. ≤dW +2 for PZRL-MF and deff. ≤2dS +dW +

3 for PZRL-MB. Corollary 4.8 (Bi-Lipschitz MDPs). Consider a bi-Lipschitz MDP, i.e., the average reward function JM: Φ →R satisfies the following properties: there exist two constants ¯L ≥L > 0 such that for every ϕ, ϕ′

LρΦ(ϕ, ϕ′) ≤|JM(ϕ) −JM(ϕ′)| ≤¯LρΦ(ϕ, ϕ′).

Then, the regret of PZRL-MF w.r.t. the policy class scales as

˜O(

√

T) on a high probability set. We note that the assumption made in Corollary 4.8 commonly made in continuum bandits literature such as Cope (2009); Yu and Mannor (2011); Combes, Proutière, and Fauquette (2020).

## 5 Simulations

We evaluate the proposed algorithms on the following two systems.

Transmission scheduling for remote estimation of a stochastic dynamic process. Consider a process {xt} that

22532

<!-- Page 7 -->

evolves as xt+1 = βxt + wt, where |β| < 1 and {wt} is i.i.d., wt ∼N(0, 1) for all t. A sensor observes {xt}, encodes it into data packets, and transmits them to a remote estimator across an unreliable wireless channel. ct ∈{0, 1} denotes the channel state at time t. ct = 1 (0) denotes that the channel state is good (bad). {ct} is a Markov process with transition probabilities pij:= P(ct+1 = j | ct = i), i, j ∈{0, 1}, where p01, p11 > 0. at ∈{0, 1} denotes the decision made by the sensor regarding whether or not a packet transmission is attempted at time t; at = 1 denotes that transmission is attempted. The estimator state ˆxt evolves as

ˆxt+1 = xt+1ctat +(1−ctat)βˆxt. The estimation error {et} evolves as et+1 = (βet + wt) −βctatet. The agent’s estimate of ct, denoted by bt can be updated recursively. The actions {at} are to be chosen so as to minimize the error with a minimal amount of transmission power. The agent earns a reward rt:= −e2 t −λat, where λ > 0 is the number of units of resource required for transmission. Dutta and Singh (2023) shows that a threshold policy is optimal in this setup, one which transmits only when bt exceeds a certain threshold (that is allowed to depend upon et). Hence, the optimal policy can be described by specifying the threshold curve, which in turn can be approximated by a curve with finitely many parameters. This problem does not fit into the class of Linear MDPs or Tabular MDPs. However, it can be shown that the average reward function is Lipschitz when the comparator policy class consists only of stable policies, and hence fits within our framework. We compare the empirical performance of the proposed algorithms, PZRL-MF and PZRL-MB (Algorithm 1) with that of a heuristic algorithm Policy UCB (Algorithm 2 in the extended version), which discretizes the policy space uniformly at time t = 0 and plays the policy with the highest model-free UCB index from the set of finite set of policies in every episode. For both PZRL-MF and PZRL-MB, we use the following parameterization: ϕ(s; w) = I{w(1)+w(2)et<bt}, w = (w(1), w(2)) ∈[1, 3]×[−1, −0.01]. We plot the cumulative reward minus the average performance of the policy that suggests transmission irrespective of the system state, averaged over 50 runs in Figure 3(a). Both PZRL-MF and PZRL-MB outperform the fixed discretization-based algorithm, Policy UCB.

Continuous RiverSwim. We modify the RiverSwim MDP (Strehl and Littman 2008) to obtain its continuous version. The state st describes the location of the agent in the river and evolves as follows upon the application of action at at time t:

st+1 =

  

 

(0 ∨(st −1

2(1 + wt 2))) ∧6 w.p. 2(1−at)

5 st w.p. 0.2 (0 ∨(st + 1

2(1 + wt 2))) ∧6 w.p. 2(1+at)

5, where {wt} is i.i.d. and wt ∼N(0, 0.5), and t ∈{0} ∪N. Here, S = [0, 6] and A = [0, 1]. The reward function is given by r(s, a) = 0.005(((s −6)/6)4 + ((a −1)/2)4) + 0.5((s/6)4 +((a+1)/2)4). Note that the policy that chooses the action 1 at all times, irrespective of the current state, is optimal. For both PZRL-MF and PZRL-MB, we use the following parameterizations:

0 10000 Time

Cumulative reward w.r.t. a stable policy

PZRL-MF PZRL-MB Policy-UCB

(a) Transmission Scheduling

0 10000 Time

1

2

3

4

5

6

8 log(Regret)

PZRL-MF (dw = 1)

PZRL-MF (dw = 2)

PZRL-MF (dw = 3)

PZRL-MB (dw = 1)

PZRL-MB (dw = 2)

PZRL-MB (dw = 3)

UCRL2 ZoRL TSDE

(b) Continuous RiverSwim

**Figure 3.** Simulation results.

1. 1 parameter: ϕ(s; w) = w, w ∈[−1, 1]. 2. 2 parameters: ϕ(s; w) = w(1) + w(2)s, w = (w(1), w(2)) ∈[−1, 1] × [−0.5, 0.5]. 3. 3 parameters: ϕ(s; w) = w(1) + w(2)s + w(3)s2, w = (w(1), w(2), w(3)) ∈[−1, 1] × [−0.5, 0.5]2. We compare the empirical performance of PZRL-MF and PZRL-MB (Algorithm 1) with that of ZoRL (Kar and Singh 2025), UCRL2 (Jaksch, Ortner, and Auer 2010) and TSDE (Ouyang et al. 2017). Since these competitor policies are designed for finite state-action spaces, we apply them on a uniform discretization of S × A. We plot the logarithm of the cumulative regret averaged over 50 runs for the Continuous RiverSwim environment in Figure 3(b), and observe that PZRL-MF and PZRL-MB outperforms every other algorithm, and amongst PZRL-MF and PZRL-MB, PZRL-MB has the edge over PZRL-MF. Policy classes with 2 and 3 parameters outperform the single-parameter policy class for both proposed algorithms.

## 6 Conclusion

The central idea of zooming-based algorithms is to capitalize on its adaptive nature. The adaptivity is captured via the zooming dimension. We identify the absence of policy class dependence in the existing definition of the zooming dimension. To rectify this, we define the zooming dimension in terms of coverings of the policy space, allowing it to depend on the comparator policy class. We propose zooming-based algorithms PZRL-MF and PZRL-MB, and prove that their regret can be bounded as ˜O(T 1−d−1 eff.) where deff. = dΦ z + 2 and deff. = 2dS + dΦ z + 3, respectively. Simulation results support our theoretical findings.

22533

<!-- Page 8 -->

## References

Abbasi-Yadkori, Y.; and Szepesvári, C. 2011. Regret bounds for the adaptive control of linear quadratic systems. In Proceedings of the 24th Annual Conference on Learning Theory, 1–26. JMLR Workshop and Conference Proceedings. Arapostathis, A.; Borkar, V. S.; Fernández-Gaucherand, E.; Ghosh, M. K.; and Marcus, S. I. 1993. Discrete-time controlled Markov processes with average cost criterion: a survey. SIAM Journal on Control and Optimization, 31(2): 282–344. Ayoub, A.; Jia, Z.; Szepesvari, C.; Wang, M.; and Yang, L. 2020. Model-based reinforcement learning with valuetargeted regression. In International Conference on Machine Learning, 463–474. PMLR. Billingsley, P. 2017. Probability and measure. John Wiley & Sons. Bubeck, S.; Munos, R.; Stoltz, G.; and Szepesvári, C. 2011. X-Armed Bandits. Journal of Machine Learning Research, 12(5). Cao, T.; and Krishnamurthy, A. 2020. Provably adaptive reinforcement learning in metric spaces. Advances in Neural Information Processing Systems, 33: 9736–9744. Chowdhury, S. R.; and Gopalan, A. 2019. Online learning in kernelized Markov decision processes. In The 22nd International Conference on Artificial Intelligence and Statistics, 3197–3205. PMLR. Combes, R.; Proutière, A.; and Fauquette, A. 2020. Unimodal bandits with continuous arms: Order-optimal regret without smoothness. Proceedings of the ACM on Measurement and Analysis of Computing Systems, 4(1): 1–28.

Cope, E. W. 2009. Regret and convergence bounds for a class of continuum-armed bandit problems. IEEE Transactions on Automatic Control, 54(6): 1243–1253.

Domingues, O. D.; Menard, P.; Pirotta, M.; Kaufmann, E.; and Valko, M. 2021. Kernel-Based Reinforcement Learning: A Finite-Time Analysis. In Meila, M.; and Zhang, T., eds., Proceedings of the 38th International Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, 2783–2792. PMLR. Douc, R.; Moulines, E.; Priouret, P.; and Soulier, P. 2018. Markov chains: Basic definitions. Springer. Dutta, M.; and Singh, R. 2023. Optimal scheduling policies for remote estimation of autoregressive Markov processes over time-correlated fading channel. In 2023 62nd IEEE Conference on Decision and Control (CDC), 6455–6462. IEEE. Folland, G. B. 2013. Real analysis: modern techniques and their applications. John Wiley & Sons. Hazan, E.; and Singh, K. 2022. Introduction to online nonstochastic control. arXiv preprint arXiv:2211.09619. He, J.; Zhong, H.; and Yang, Z. 2023. Sample-efficient Learning of Infinite-horizon Average-reward MDPs with General Function Approximation. In The Twelfth International Conference on Learning Representations. Jaksch, T.; Ortner, R.; and Auer, P. 2010. Near-optimal regret bounds for reinforcement learning. Journal of Machine Learning Research, 11(Apr): 1563–1600.

Jin, C.; Yang, Z.; Wang, Z.; and Jordan, M. I. 2020. Provably efficient reinforcement learning with linear function approximation. In Conference on Learning Theory, 2137–2143. PMLR. Kakade, S.; Krishnamurthy, A.; Lowrey, K.; Ohnishi, M.; and Sun, W. 2020. Information theoretic regret bounds for online nonlinear control. Advances in Neural Information Processing Systems, 33: 15312–15325. Kar, A.; and Singh, R. 2025. Provably Adaptive Average Reward Reinforcement Learning for Metric Spaces. In Proceedings of the Forty-first Conference on Uncertainty in Artificial Intelligence, 1924–1964. PMLR. Kleinberg, R.; Slivkins, A.; and Upfal, E. 2008. Multi-armed bandits in metric spaces. In Proceedings of the fortieth annual ACM symposium on Theory of computing, 681–690.

Kleinberg, R.; Slivkins, A.; and Upfal, E. 2019. Bandits and experts in metric spaces. Journal of the ACM (JACM), 66(4): 1–77. Kumar, A.; Fu, Z.; Pathak, D.; and Malik, J. 2021. Rma: Rapid motor adaptation for legged robots. arXiv preprint arXiv:2107.04034. Lattimore, T.; and Szepesvári, C. 2020. Bandit Algorithms. Cambridge University Press. Maran, D.; Metelli, A. M.; Papini, M.; and Restell, M. 2024a. No-Regret Reinforcement Learning in Smooth MDPs. The Forty-first International Conference on Machine Learning.

Maran, D.; Metelli, A. M.; Papini, M.; and Restelli, M. 2024b. Projection by Convolution: Optimal Sample Complexity for Reinforcement Learning in Continuous-Space MDPs. The 37th Annual Conference on Learning Theory. Meyn, S. P.; and Tweedie, R. L. 2012. Markov chains and stochastic stability. Springer Science & Business Media. Mitrophanov, A. Y. 2005. Sensitivity and convergence of uniformly ergodic Markov chains. Journal of Applied Probability, 42(4): 1003–1014. Modi, A.; Chen, J.; Krishnamurthy, A.; Jiang, N.; and Agarwal, A. 2024. Model-free representation learning and exploration in low-rank mdps. Journal of Machine Learning Research, 25(6): 1–76. Mouhoubi, Z. 2021. Perturbation and stability bounds for ergodic general state Markov chains with respect to various norms. Le Matematiche, 76(1): 243–276. Nair, S.; Rajeswaran, A.; Kumar, V.; Finn, C.; and Gupta, A. 2023. R3m: A universal visual representation for robot manipulation. Confernce on Robot Learning. Ortner, R.; and Ryabko, D. 2012. Online regret bounds for undiscounted continuous reinforcement learning. Advances in Neural Information Processing Systems, 25. Osband, I.; and Van Roy, B. 2014. Model-based reinforcement learning and the eluder dimension. Advances in Neural Information Processing Systems, 27. Ouyang, Y.; Gagrani, M.; Nayyar, A.; and Jain, R. 2017. Learning unknown Markov decision processes: A Thompson sampling approach. In Advances in Neural Information Processing Systems, 1333–1342.

22534

<!-- Page 9 -->

Puterman, M. L. 2014. Markov decision processes: discrete stochastic dynamic programming. John Wiley & Sons. Qian, J.; Fruit, R.; Pirotta, M.; and Lazaric, A. 2019. Exploration bonus for regret minimization in discrete and continuous average reward mdps. Advances in Neural Information Processing Systems, 32. Rakhlin, A.; and Sridharan, K. 2014. Lecture notes for STAT928: Statistical Learning and Sequential Prediction. www.mit.edu/~rakhlin/courses/stat928/stat928_notes.pdf. Sinclair, S. R.; Banerjee, S.; and Yu, C. L. 2023. Adaptive discretization in online reinforcement learning. Operations Research, 71(5): 1636–1652. Song, Z.; and Sun, W. 2019. Efficient model-free reinforcement learning in metric spaces. arXiv preprint arXiv:1905.00475. Strehl, A. L.; and Littman, M. L. 2008. An analysis of model-based interval estimation for Markov decision processes. Journal of Computer and System Sciences, 74(8): 1309–1331. Sutton, R. S.; and Barto, A. G. 2018. Reinforcement learning: An introduction. MIT press.

Tossou, A.; Basu, D.; and Dimitrakakis, C. 2019. Nearoptimal optimistic reinforcement learning using empirical Bernstein inequalities. arXiv preprint arXiv:1905.12425. Wei, C.-Y.; Jahromi, M. J.; Luo, H.; and Jain, R. 2021. Learning infinite-horizon average-reward MDPs with linear function approximation. In International Conference on Artificial Intelligence and Statistics, 3007–3015. PMLR. Wu, R.; Sekhari, A.; Krishnamurthy, A.; and Sun, W. 2024. Computationally Efficient RL under Linear Bellman Completeness for Deterministic Dynamics. CoRR. Yu, J. Y.; and Mannor, S. 2011. Unimodal Bandits. In ICML, 41–48.

22535
