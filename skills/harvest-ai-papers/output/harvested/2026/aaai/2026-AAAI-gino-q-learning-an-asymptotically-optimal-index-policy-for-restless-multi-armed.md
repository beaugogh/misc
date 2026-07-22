---
title: "GINO-Q: Learning an Asymptotically Optimal Index Policy for Restless Multi-armed Bandits"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39088
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39088/43050
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# GINO-Q: Learning an Asymptotically Optimal Index Policy for Restless Multi-armed Bandits

<!-- Page 1 -->

GINO-Q: Learning an Asymptotically Optimal Index Policy for Restless Multi-armed Bandits

Gongpu Chen1*, Soung Chang Liew2, Deniz G¨und¨uz1

1Department of Electrical and Electronic Engineering, Imperial College London, London SW7 2AZ, U.K. 2Department of Information Engineering, The Chinese University of Hong Kong, Shatin, Hong Kong. gongpu.chen@imperial.ac.uk, soung@ie.cuhk.edu.hk, d.gunduz@imperial.ac.uk

## Abstract

The restless multi-armed bandit (RMAB) framework is a popular model with applications across a wide variety of fields. However, its solution is hindered by the exponentially growing state space (with respect to the number of arms) and the combinatorial action space, making traditional reinforcement learning methods infeasible for large-scale instances. In this paper, we propose GINO-Q, a three-timescale stochastic approximation algorithm designed to learn an asymptotically optimal index policy for RMABs. GINO-Q mitigates the curse of dimensionality by decomposing the RMAB into a series of subproblems, each with the same dimension as a single arm, ensuring that complexity increases linearly with the number of arms. Unlike recently developed Whittle-indexbased algorithms, GINO-Q does not require RMABs to be indexable, enhancing its flexibility and applicability. Our experimental results demonstrate that GINO-Q consistently learns near-optimal policies, even for non-indexable RMABs where Whittle-index-based algorithms perform poorly, and it converges significantly faster than existing baselines.

## Introduction

A restless multi-armed bandit (RMAB) models a sequential decision-making problem, in which a set of resources must be allocated to N out of M (1 ≤N < M) arms at each discrete time step. Here, each arm represents a dynamic process that, depending on whether it is selected, generates a reward and may transition to a new state. These arms evolve independently except for simultaneously being subject to the resource constraint. The objective is to find an optimal policy that selects arms at each time step to maximize the expected reward. RMABs find applications in diverse fields, including network resource allocation (Wang et al. 2019), opportunistic scheduling (Wang and Chen 2021), public health interventions (Mate et al. 2022), and many more.

This paper investigates the design of an efficient reinforcement learning (RL) algorithm for RMABs. As we know, the curse of dimensionality is a central challenge in solving dynamic programs. Unfortunately, this problem is particularly severe in RMABs due to the exponential growth of RMAB’s dimension with the number of arms. In fact,

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

it is known that RMABs are PSPACE hard even when full system knowledge is available (Papadimitriou and Tsitsiklis 1999). As a result, directly treating RMABs as Markov decision processes (MDPs) and applying RL algorithms is inefficient, and, in many cases, computationally infeasible—particularly for large-scale RMABs. For instance, consider a moderate-scale RMAB with M = 100 and N = 25. Suppose each arm exhibits 10 states. Then the RMAB encompasses an astronomical 10100 possible states, along with 100

25

≈2.4 × 1023 valid actions. Such complexity presents a great challenge for conventional RL algorithms.

To address this challenge, recent studies have drawn inspiration from the well-known Whittle index policy (Whittle 1988), a planning algorithm for RMABs with full system knowledge. This approach decouples the RMAB into individual arms, computes an index for each, and schedules based on these indices. Despite its efficiency, the Whittle index policy is fundamentally limited by its reliance on the indexability property—a condition that does not naturally hold for all RMABs. While several sufficient conditions for indexability have been studied (Ni˜no-Mora 2001, 2007; Glazebrook, Ruiz-Hernandez, and Kirkbride 2006), they are often stringent and apply only to a narrow class of RMABs. In general, verifying indexability requires full knowledge of the system and considerable analytical effort (Chen, Liew, and Shao 2022; Liu and Zhao 2010; Villar 2016), making it infeasible in most scenarios where full knowledge of the system is unavailable. As will be shown in our experiments, applying the Whittle index policy to a non-indexable RMAB can result in arbitrarily poor performance. This underscores a significant limitation of Whittle-index-based learning algorithms: without indexability guarantees, their application can be unreliable and potentially detrimental.

In this paper, we propose an RL algorithm for general RMABs that does not require indexability. Our method is inspired by a recently developed planning algorithm for RMABs known as the gain index policy (Chen and Liew 2024). This method has been shown to achieve asymptotic optimality as the number of arms grows large, given a fixed selection ratio. However, computing gain indices remains computationally demanding—even when full system parameters are known. We propose GINO-Q learning, a threetimescale stochastic approximation algorithm designed to efficiently approximate the gain index policy in model-free

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

20032

<!-- Page 2 -->

settings. Our approach integrates Q-learning, SARSA, and stochastic gradient descent (SGD), operating on distinct timescales to effectively learn gain indices without relying on system knowledge. Specifically, we begin by decomposing the RMAB across arms through a relaxation of the hard constraint, applying the Lagrange multiplier method to formulate M unconstrained single-arm subproblems. For each subproblem, Q-learning is used to estimate the Q-function, while SARSA is employed to approximate the gradient of the average reward with respect to the Lagrange multiplier. The Lagrange multiplier itself is then updated via SGD. By appropriately designing the learning rates for the three updates, the algorithm naturally operates on three distinct timescales, enabling efficient and stable learning of the gain index policy. The key advantages of GINO-Q are twofold:

## 1 Scalability:

By decomposing the RMAB into a collection of subproblems, GINO-Q only needs to solve problems with the same dimension as a single arm. This decomposition circumvents the exponential growth of the joint state and action spaces, ensuring that computational complexity scales linearly with the number of arms M. As a result, GINO-Q achieves strong performance even in large-scale RMABs, where conventional RL algorithms are computationally infeasible. 2. Applicability: GINO-Q does not require the RMAB to be indexable, thereby significantly broadening its applicability. Our experiments show that Whittle-index-based learning algorithms can perform poorly in non-indexable settings. In contrast, GINO-Q consistently learns nearoptimal policies—even in non-indexable RMABs.

We evaluate the performance of GINO-Q through extensive experiments, which show that it consistently outperforms existing algorithms across all tested settings.

## Related Work

The success of deep RL has attracted considerable research interest in its application to practical problems that can be modeled as RMABs. Notable examples include wireless sensor scheduling (Leong et al. 2020), dynamic multichannel access (Wang et al. 2018; Demirel et al. 2018), intelligent building management (Wei, Wang, and Zhu 2017). However, a common limitation across these studies is the poor scalability of deep RL in RMABs. The experimental results presented in these papers are typically restricted to small-scale scenarios, with the number of arms limited to M < 10.

In the planning scenario, where the system knowledge is known, the Whittle index policy (Whittle 1988) is recognized as one of the most efficient heuristic algorithms for addressing RMAB problems. This has inspired a series of studies focused on applying RL algorithms to learn Whittle indices. For example, the work in (Fu et al. 2019) studied a Q-learning algorithm to learn the Whittle indices; however, their experiments revealed that the proposed algorithm struggles to accurately learn the Whittle indices. Subsequently, Avrachenkov and Borkar (2022) introduced Whittle-Index-Based Q-learning (WIBQ), a two-timescale stochastic approximation algorithm designed to learn the

Whittle indices. They proved theoretically that WIBQ converges to the Whittle indices for indexable RMABs. Further advancing this work, Xiong and Li (2023) enhanced WIBQ to handle arms with large state spaces by coupling WIBQ with neural network function approximator. Additionally, Nakhleh et al. (2021) converted the computation of Whittle indices to an optimal control problem and proposed a neural network-based approach for computing Whittle indices.

In practical applications, Whittle-index-based learning algorithms have been employed in adaptive video streaming (Xiong et al. 2022), wireless edge caching (Xiong et al. 2024), and preventive healthcare (Biswas et al. 2021). Moreover, the Whittle index policy has also inspired studies on online learning for RMABs (Wang et al. 2023; Xiong, Wang, and Li 2022; Xiong, Li, and Singh 2022).

All of these studies rely on the indexability condition that makes the Whittle index policy applicable. However, as we will show through a concrete example, not all RMABs satisfy this condition. Fortunately, a gain index policy that does not require indexability was recently proposed by Chen and Liew (2024), who also introduced a gradient-based approach to compute the gain indices with full knowledge of system parameters. To the best of our knowledge, our proposed GINO-Q algorithm is the first RL method designed to learn the gain index policy in a model-free setting.

Notations. For any positive integer M, we will use [M] to denote the set of positive integers between 1 and M, i.e., [M] = {1, 2, · · ·, M}. E[·] denotes the expectation.

Problem Statement and Preliminaries An RMAB consists of M arms {Bi: i ∈[M]}. Each arm Bi is an MDP represented by a tuple (Si, Ai, ri, pi), where Si is the state space, Ai is the action space, ri: Si × Ai →R is the reward function, and pi is the transition kernel. Let st i and at i denote the state and action of Bi at time t. In particular, we have Ai = {0, 1} for all i ∈[M]. We will say that arm Bi is activated at time t if at i = 1. At any time step, all arms evolve independently based on their actions; that is, P(st+1

1, · · ·, st+1

M |st

1, · · ·, st M, at

1, · · ·, at M) = QM i=1 pi(st+1 i |st i, at i). However, there is a constraint on the actions that weakly couples all the arms. Specifically, at each time step, only N arms can be activated (1 ≤N < M). That is, PM i=1 at i = N for all t. The objective is to identify an optimal policy that maximizes the cumulative reward obtained from all the arms. Mathematically, an RMAB is a constrained optimization problem defined as follows:

max {at i:i∈[M],t≥1} lim T →∞

## 1 T E

" T X t=1

M X i=1 ri st i, at i

#

(1)

subject to

M X i=1 at i = N, ∀t. (2)

We assume that all arms are unichain MDPs. As a result, the objective function (1) is independent of the initial state.

The Gain Index Policy. An RMAB can be viewed as an MDP with a joint state space S1 ×S2 ×· · ·×SM and action

20033

<!-- Page 3 -->

space {0, 1}M. However, the size of the state spaces grows exponentially with M, and the set of feasible actions forms a combinatorial space of size

M

N

. As a result, the problem becomes challenging to solve when M is large. Since the arms are weakly coupled only via constraint (2), a common approach to mitigate the complexity is to decompose the RMAB into single-arm problems by relaxing the constraint. Building on this concept, Chen and Liew (2024) introduced the gain index policy and proved its asymptotic optimality.

In particular, we relax constraint (2) of the RMAB problem to the following:

lim T →∞

## 1 T E

" T X t=1

M X i=1 at i

#

= N. (3)

Replacing (2) by (3) leads to a relaxed RMAB. By applying the Lagrange multiplier method and invoking strong duality, the relaxed problem can be equivalently reformulated as the following inf-max problem:

inf λ max

{at i} lim T →∞

## 1 T E

" T X t=1

M X i=1 ri st i, at i

−λat i

#

+ Nλ,

(4) where λ ∈R is the Lagrange multiplier. For any fixed λ, (4) can be decoupled into M subproblems:

Ji(λ): max {at i:t≥1} lim T →∞

## 1 T E

" T X t=1 ri st i, at i

−λat i

#

, (5)

where i ∈[M]. We refer to each Ji(λ) as a single-arm problem. Note that Ji(λ) is an MDP associated with Bi: they share the same state space Si, action space Ai, and transition kernel pi. However, there is a distinction between them in terms of their reward functions. The reward function of Ji(λ) is defined as ri(s, a) −λa, where λ can be interpreted as the cost of action a = 1. If we denote the optimal value of problem Ji(λ) by gi(λ), it can be determined by the Bellman equation as follows (Puterman 2014):

Vi(s, λ) + gi(λ) = max a∈{0,1} {Qi(s, a, λ)}, s ∈Si, (6)

where Vi(s, λ) is the state value function and Qi(s, a, λ) is the state-action value function:

Qi(s, a, λ) ≜ri(s, a) −λa +

X s′∈Si pi(s′|s, a)Vi(s′, λ).

Here, we express Vi and Qi as functions of λ to highlight their dependence on λ. Now, (4) reduces to inf λ f(λ) ≜

M X i=1 gi(λ) + Nλ. (7)

Denoting by λ∗the optimal solution to problem (7), then the gain index policy is defined as follows: Definition 1 (Gain index policy). For each arm i ∈[M] and each state s ∈Si, a gain index is defined as:

Wi(s) ≜Qi(s, 1, λ∗) −Qi(s, 0, λ∗). (8) Then the gain index of the i-th arm at time t is given by Wi(st i). The gain index policy activates the N arms with the largest N gain indices, with ties broken arbitrarily.

1 4

2 6 5

!(#!|#, 0)

!(#!|#, 1)

1 1

1

1

0.6

0.4 0.6

0.8 0.4

0.2

**Figure 1.** Transition probabilities of a non-indexable arm. Except for state 1, each of the remaining states has identical transition probabilities for both actions. For simplicity, we only plot the transitions of action 0 for those states.

Intuitively, the gain index Wi(s) evaluates the “gain” of activating arm Bi when it is in state s. Under some mild conditions (Chen and Liew 2024), the gain index policy is asymptotically optimal in the following sense:

lim M→∞

## 1 M Gind

M = lim

M→∞

## 1 M Gopt

M, (9)

where Gind

M and Gopt

M denote the total time-averaged reward across all arms under the gain index policy and the optimal policy, respectively.

Whittle Index Policy and Indexability. Whittle index policy (Whittle 1988) is a classic approach for RMABs. It shares the same asymptotic optimality as described in (9) (Weber and Weiss 1990). Similar to the gain index policy, the Whittle index policy assigns an index to each state of each arm and selects at each time the top N arms with the highest indices for activation. Whittle’s index for state s of arm Bi is defined as the infimum value of λ that ensures equal optimality between taking action 0 and action 1 in state s within the single-arm problem Ji(λ). That is,

WIi(s) = inf{λ: Qi(s, 1, λ) = Qi(s, 0, λ)}. (10)

The Whittle index policy is only applicable to indexable RMABs. Specifically, we denote by Ei(λ) the set of states in which action 0 is optimal for problem Ji(λ).

Definition 2 (Indexability). An arm Bi is considered indexable if Ei(λ) expands monotonically from the empty set to the entire state space Si as λ increases from −∞to ∞. An RMAB is indexable if all its arms are indexable.

Recall that λ can be interpreted as the cost of taking action a = 1. If an arm Bi is indexable, then the optimal action for this arm in state s is a = 1 if the cost λ ≤WIi(s); otherwise, the optimal action is a = 0. Therefore, WIi(s) can be interpreted as the “value” of taking action a = 1 in state s. However, in the absence of indexability, this property no longer holds—rendering WIi(s) an invalid metric for prioritization. As a result, the Whittle index policy is well-defined only for indexable RMABs.

To illustrate that the indexability does not always hold, we construct a non-indexable arm as a counterexample.

Example 1 (A Non-indexable Arm). Consider an arm Bi with 6 states and transition probabilities illustrated in Fig. 1. The reward function is defined as ri(1, 1) = −10, ri(1, 0) =

20034

<!-- Page 4 -->

−4, ri(2, 1) = ri(2, 0) = 4 and ri(s, 1) = 0, ri(s, 0) = −2 for s ∈{3, 4, 5, 6}. It can be verified that state 1 ∈Ei(λ) for −4 ≤λ ≤2 and 1 /∈Ei(λ) for λ < −4 and λ > 2. Hence the set Ei(λ) does not expand monotonically as λ increases, implying that the arm is not indexable.

Nevertheless, the quantity defined by (10) remains welldefined, even for non-indexable arms. This raises a natural question: what happens if the Whittle index policy is applied to a non-indexable RMAB? Moreover, in existing Whittleindex-based algorithms such as WIBQ (Avrachenkov and Borkar 2022) and Neurwin (Nakhleh et al. 2021), the Whittle index is typically determined by learning a value of λ that satisfies the condition Qi(s, 1, λ) = Qi(s, 0, λ). However, in Example 1, both −4 and 2 satisfy this condition. As a result, the algorithm may converge to one of these values arbitrarily, or even oscillate if multiple such solutions are close in value. How do Whittle-index-based algorithms perform under such ambiguity?

As demonstrated by our experiments, applying the Whittle index policy to an RMAB with arms as defined in Example 1 can lead to arbitrarily poor performance. This underscores the fragility of Whittle-index-based learning algorithms in the absence of indexability guarantees and highlights the importance of the gain index policy, which operates without such assumptions. These considerations motivate the development of GINO-Q, which aims to learn the gain index policy efficiently in model-free settings.

Gain-Index-Oriented Q Learning With asymptotic optimality and no reliance on indexability, learning the gain index policy offers a promising solution for RMABs without system knowledge, particularly for largescale problems. This section presents the GINO-Q learning algorithm for RMABs. Our approach involves decomposing the RMAB into single-arm problems and learning the gain indices for each arm.

By definition, the gain indices of an arm are determined by the Q-function of the corresponding single-arm problem under the optimal activation cost λ∗. While learning the Qfunction for a fixed λ reduces to a standard Q-learning task, jointly learning λ∗introduces additional complexity due to the coupling between the dual variable λ and the value functions. Specifically, in the absence of system knowledge, the gradient required to update λ cannot be computed directly— and, moreover, it cannot be estimated directly during the Qlearning process.

To overcome this challenge, we propose a three-timescale stochastic approximation algorithm. The algorithm updates the Q-function of Ji(λ) and the dual variable λ on medium and slow timescales, respectively. A third, faster timescale is employed to estimate the derivative of gi(λ) with respect to λ, which plays a critical role in guiding the update of λ.

Useful Properties. We begin by introducing some useful definitions and establishing key properties of the optimization problem (7), which form the basis of our method. We first define an auxiliary MDP for each arm as follows: Definition 3 (Auxiliary MDP). The auxiliary MDP associated with arm Bi is defined as Mi = (Si, Ai, c, pi), where the state space Si, action space Ai, and transition kernel pi are identical to those of Bi. The cost function is given by c(s, a) = a for all s ∈Si and a ∈Ai.

Since Bi is a unichain MDP, so is Mi. As a result, the average cost of Mi under any stationary policy π is independent of the initial state s. We denote this average cost by hπ i ≜lim

T →∞

1 T Eπ hPT t=1 at i i

. Let Dπ i (s, a) denote the state- action value function of Mi under policy π, and π(a′|s′) the probability of taking action a′ in state s′. Then we have

Dπ i (s, a) + hπ i = a +

X s′,a′ pi(s′|s, a)π(a′|s′)Dπ i (s′, a′).

Clearly, Ji(λ) and Mi share the same policy space. Let π be a policy for the single-arm problem Ji(λ), and V π i (s) and gπ i be the associated value function and long-term average reward, respectively. It is easy to see that, for any policy π, dgπ i dλ = −hπ i, ∀i ∈[M]. (11)

Let πλ i denote the optimal policy for problem Ji(λ), then the derivative of function f(λ) is given by f ′(λ) =

M X i=1 dgi(λ)

dλ + N = N −

M X i=1 hπλ i i. (12)

Drawing from these concepts, we can establish the existence of a bounded optimal solution λ∗, which supports the practical feasibility of learning λ∗. Lemma 1. For any RMAB with bounded reward functions {ri}i∈[M], f(λ) is a piecewise linear and convex function. In addition, there always exist a bounded λ∗that achieves the minimum value of f(λ).

GINO-Q learning algorithm. Our objective is to learn the optimal dual variable λ∗and the corresponding Qfunctions for the single-arm problems Ji(λ∗), for all i ∈ [M]. To this end, we propose a simple yet effective algorithm that simultaneously updates λ and learns the associated Q-functions, thereby enabling the computation of gain indices for all arms. We refer to this approach as Gain-Index- Oriented Q-learning (GINO-Q).

In particular, we fix a stepsize sequence {θt: t ≥1}, and employ the stochastic gradient-descent method to update λ:

λt+1 = λt −θt ˆf ′(λt), (13)

where ˆf ′(λt) is an estimator of f ′(λt), to be detailed later. Meanwhile, we use the standard relative value iteration (RVI) Q-learning algorithm (Abounadi, Bertsekas, and Borkar 2001) to learn the Q-function of every single-arm problem Ji(λt) for the current λt. That is, ∀i ∈[M]:

Qt+1 i (st i, at i) =Qt i(st i, at i) + βt i[ri(st i, at i) −λtat i+ max a Qt i(st+1 i, a) −Qt i(st i, at i) −gt i], (14)

where {βt i: t ≥1} is a predefined stepsize sequence. While gt i can be estimated in various ways (Abounadi, Bertsekas, and Borkar 2001), one of the most widely used methods is:

gt i = 1 2|S|

X s∈Si

X a∈Ai

Qt i(s, a). (15)

20035

<!-- Page 5 -->

We proceed by constructing the estimator ˆf ′(λ) according to (12). Given any λ, the optimal policy πλ i for Ji(λ) selects actions greedily according to the optimal Q-function of Ji(λ), denoted by Qi. At time step t, Qt i serves as an estimate of Qi. Hence, the policy that selects actions greedily according to Qt i can be regarded as an estimate of πλ i. To learn the average cost of this policy for the auxiliary MDP Mi, we employ the SARSA algorithm (Sutton and Barto 2018):

Dt+1 i (st i, at i) = Dt i(st i, at i) + αt i[at i + Dt i(st+1 i, at+1 i)−

Dt i(st i, at i) −ht i], (16)

where {αt i: t ≥1} is the stepsize sequence, action at+1 i = arg maxa Qt i(st+1 i, a) is selected greedily based on Qt i. The average cost of Mi is estimated by the well-known method from (Abounadi, Bertsekas, and Borkar 2001):

ht i = max a Dt i(si, a), (17)

where si ∈Si is an arbitrary but fixed reference state. We then estimate f ′(λt) by ˆf ′(λt) = N −PM i=1 ht i. The stepsize schedules of the three coupled iterates play a critical role in learning both λ∗and the corresponding Qfunctions. As shown in equation (12), for any given λ, the derivative f ′(λ) depends on the optimal policy πλ i for the single-arm problem Ji(λ). Therefore, the update of the sequence {λt} must proceed more slowly than that of Qt i, allowing Q-learning to sufficiently approximate Qi. Conversely, since SARSA aims to estimate the state-action value function of Mi under the greedy policy induced by Qt i, its updates should operate at a faster timescale than Q-learning.

We define the stepsize sequences of the three coupled iterates properly so that they form a three-timescale stochastic approximation algorithm, with updates (13), (14), and (16) operating in the slow, medium, and fast timescales, respectively. In particular, define1 αt i = C1 t, βt i = C2 t√log t, θt = C3 t log t1{t(mod C4) = 0}, where {Ck} are constants, 1{·} is the indicator function, {αt i} and {βt i} are invariant across i ∈[M]. It is easy to verify that P∞ t=1 xt = ∞and P∞ t=1(xt)2 < ∞for x = αi, βi or θ. Update (16) is faster than (14) because βt i = o(αt i). For the same reason, update (14) is faster than (13).

The GINO-Q algorithm is summarized in Algorithm 1. A detail to note is line 14, where λt is updated only if the estimated derivative is decreased in absolute value. Since f(λ) is piecewise linear and convex, this strategy helps mitigate erroneous updates caused by noise in the estimation of f ′(λ). While this may slightly slow convergence near λ∗, it improves stability and robustness during learning.

Remark: If the learner has knowledge of the arm classification (but not the specific parameters of arms), updates (14) and (16) do not need to be performed for each individual arm. Instead, it is sufficient to maintain a pair of (Qt i, Dt i) for each class. This is because arms within the same class

1In practice, t in the expressions of αt i and βt i can be replaced by n(st i, at i), the number of occurrences of (st i, at i) up to time t.

## Algorithm

1: GINO-Q Learning

Input: Integer T, learning rates {αt i}, {βt i}, and {θt} Initialization: Let t = 1, λ1 = 0, y0 = M. Reset the

RMAB and receive the initial arm states {s1 i } Output: Gain indices of all arms while t ≤T do for i = 1, 2, · · ·, M do

Select action at i according to Qt i (e.g., ϵ-greedy) Apply action at i to the i-th arm, observe reward rt i and the new state st+1 i Compute gt i using equation (15) δt i = rt i −λtat i + maxa Qt i(st+1 i, a) −Qt i(st i, at i) Qt+1 i (st i, at i) = Qt i(st i, at i) + βt i(δt i −gt i) Compute ht i using equation (17) bt+1 i = arg maxa Qt i(st+1 i, a) σt i = at i + Dt i(st+1 i, bt+1 i) −Dt i(st i, at i) −ht i Dt+1 i (st i, at i) = Dt i(st i, at i) + αt iσt i end for yt = N −PM i=1 ht i λt+1 = λt −θt1{|yt| < |yt−1|}yt t ←t + 1 end while for i = 1, 2 · · ·, M do for s ∈Si do

Wi(s) = QT i (s, 1) −QT i (s, 0) // gain index end for end for share the same Q and D functions. As a result, the complexity of GINO-Q increases linearly with respect to the number of classes K. If the arm classification is unknown, then the complexity scales linearly with respect to the number of arms M, which still represents a significant reduction compared to the exponential growth of the state space.

Robustness. The definition of gain indices is dependent on λ∗, and our GINO-Q learning aims to learn λ∗and the corresponding Q function of every single-arm problem Ji(λ∗). This part discusses the robustness of GINO-Q learning with respect to the value of λ∗. Remarkably, we show that the asymptotic optimality of the gain index policy is assured as long as the sequence {λt} converges to a neighbourhood of λ∗—not necessarily converging precisely to λ∗. This implies that convergence to a neighbourhood of λ∗is sufficient to induce a near-optimal index policy.

Formally, for any λ and any arm Bi, define

W λ i (s) ≜Qi(s, 1, λ) −Qi(s, 0, λ), ∀s ∈Si.

Then the gain index is Wi(s) = W λ∗ i (s). Learning the values of {W λ i (s)} for a given λ constitutes a well-studied RL task. However, a practical concern arises: how does the performance of the index policy get affected by inaccuracies in estimating λ∗? The following lemma partially addresses this question by showing that the policy remains asymptotically optimal to a certain degree of estimation error in λ∗.

20036

<!-- Page 6 -->

0 iteration

2

0

2

4

Gain indices

GI(1) GI(2) GI(3)

True GI(1) True GI(2) True GI(3)

(a) Gain index over training.

0 500 iteration

4

2

0

Reward

Upper bound GINO-Q WIBQ(-4) WIBQ(2) DQN Random

(b) Reward over training (M = 10, N = 7).

0 500 iteration

80

60

40

20

0

Reward

Neurwin GINO-Q WIBQ Upper bound Random

(c) M = 100, N = 70.

**Figure 2.** Performances of the GINO-Q and baseline algorithms in a non-indexable RMAB problem. In (a), GI(s) denotes the gain index of state s. States 3 to 6 share the same gain index, hence we only plot GI(3) and omit the others. In (b), WIBQ(x) corresponds to the result of a single run where the Whittle index of state 1 learned by WIBQ is x ∈{−4, 2}. In (c), the results represent the average of 20 independent runs, with the shaded areas indicating confidence bounds.

Lemma 2. There exists a non-empty interval (λl, λu) that contains λ∗, such that the gain index policy with indices {W λ i (s)} is asymptotically optimal for any λ ∈(λl, λu).

As demonstrated in the proof (see Appendix), (λl, λu) is the interval where f ′(λ) = 0, whenever such an interval exists. If no such interval exists, (λl, λu) corresponds to the range of the two segments connected to λ∗. In this latter case, the non-smoothness of f(λ) may pose a challenge when searching for λ∗using gradient decent methods. Specifically, the sequence {λt} may oscillate around λ∗instead of converging to it precisely because |f ′(λ)| is bounded away from 0 for λ in the neighborhood of λ∗. Fortunately, according to Lemma 2, this situation will not affect the asymptotic optimality of the resulting index policy. This property makes GINO-Q particularly well-suited for largescale RMABs—when M is large, GINO-Q can learn a nearoptimal policy and remains robust to the inaccuracies in λ∗.

## Experiments

This section showcases the performance of GINO-Q by evaluating it across three distinct RMABs. For each problem, we explore various settings characterized by different pairs of (M, N) values. The baseline algorithms include the conventional RL method DQN (Mnih et al. 2015), as well as recently developed Whittle-index-based approaches: WIBQ (Avrachenkov and Borkar 2022) and Neurwin (Nakhleh et al. 2021). Among these, DQN models the entire RMAB as a single MDP, resulting in a state space growing exponentially in M, and a combinatorial action space of size

M

N

. As M increases, the problem quickly becomes intractable for DQN. Therefore, we only evaluate DQN in small-scale problems. On the other hand, WIBQ and Neurwin are stateof-the-art algorithms specifically designed for RMABs, with a focus on learning the Whittle index policy. They serve as our primary baselines for comparison. Additional details of the experiments can be found in the appendix.

Non-indexable RMAB. We begin with comparing GINO- Q with the Whittle-index-based learning algorithms in a non-indexable RMAB. Both WIBQ and Neurwin assume that the given RMAB is indexable because the Whittle index policy is only defined for indexable RMABs. However, indexability is rarely guaranteed in practical learning scenarios. To explore the consequences of applying a Whittlebased algorithm to a non-indexable problem, we constructed an RMAB using the arm model from Example 1 and evaluated the performance of GINO-Q and WIBQ in this setting.

We first consider the setting with M = 10 and N = 7. Fig. 2a demonstrates that GINO-Q effectively acquires the gain indices. It is important to note that the key point of the gain index policy is the relative ordering of states by their gain indices. Consequently, the performance of GINO- Q stabilizes once this order is established (compare Fig. 2a with 2b). As discussed in Example 1, there are two values of λ (i.e., −4 and 2) that satisfy the condition Qi(1, 1, λ) = Qi(1, 0, λ). As a result, both can be recognized by the WIBQ algorithm as valid Whittle indices for state 1. In contrast, each of the remaining states admits a unique Whittle index. In our experiments, WIBQ consistently learned the true Whittle indices for states 2 to 6. However, for state 1, the Whittle index converged to −4 in some runs and to 2 in others. State 1 has the highest priority with index 2 and the lowest priority with index −4, resulting in significantly different performances, as shown in Fig. 2b. For benchmarking purposes, we also evaluated the performance of DQN and the random policy (i.e., selecting N arms randomly at each step). Notably, WIBQ performs even worse than the random policy when the Whittle index of state 1 converges to 2, highlighting the risk of applying Whittle-index-based learning to non-indexable RMABs. For simplicity, the results of Neurwin are not plotted in this setting as WIBQ already learned the true Whittle indices.

We also compared the algorithms in the setting of (M, N) = (100, 70), as depicted in Fig. 2c. The low average of WIBQ suggests that it is more likely to converge to 2 than −4. While Neurwin generally outperforms WIBQ in this RMAB, it similarly faces a high risk of learning a very poor index policy. In contrast, GINO-Q consistently learns a nearoptimal index policy. Moreover, we computed upper bounds

20037

<!-- Page 7 -->

0 iteration

30

25

20

15

10

5

Reward

M=4, N=2

Neurwin Upper bound GINO-Q WIBQ DQN

0 iteration

80

60

40

20

Reward

M=10, N=4

Neurwin Upper bound GINO-Q WIBQ DQN

0 iteration

800

600

400

Reward

M=100, N=20

Neurwin Upper bound GINO-Q WIBQ

**Figure 3.** Performance comparisons between GINO-Q and baseline algorithms in the channel allocation problem.

0 iteration

0.5

0.0

0.5

1.0

1.5

Reward

M=6, N=2

Neurwin GINO-Q WIBQ DQN

0 iteration

0

1

2

3

4

Reward

M=10, N=4

Neurwin GINO-Q WIBQ DQN

0 iteration

10

0

10

20

Reward

M=100, N=30

Neurwin GINO-Q WIBQ

**Figure 4.** Performance comparisons between GINO-Q and baseline algorithms in the patrol scheduling problem.

for both settings, provided by the optimal value of the relaxed RMAB. Fig. 2c shows that when M is large, GINO-Q closely approaches the upper bound, providing strong evidence of its asymptotic optimality.

Channel Allocation. Channel allocation in communication networks involves strategically assigning communication channels to users to optimize the overall system performance. In a simple scenario, a network possesses a finite number of channels, each of which can be allocated to a single user at any time step. A recent research topic is channel allocation aimed at minimizing the average age of information (AoI), a metric that measures information freshness. Tripathi and Modiano (2019) formulated this problem as an RMAB and proved that this RMAB is indexable. See the Appendix for a detailed description of the problem.

We evaluated the GINO-Q and baseline algorithms across three different scales of M and N. The reported results represent averages from 20 independent runs, as presented in Fig. 3. It can be observed that GINO-Q consistently achieves the best performance across all settings. While Neurwin is capable of learning a Whittle index policy comparable to the gain index policy, it converges at a significantly slower rate. Additionally, compared to Neurwin and WIBQ, GINO- Q exhibits very low variance, as indicated by their confidence bounds.

Patrol Scheduling. We also assess the algorithms in a patrol scheduling problem, another application that is often formulated as an RMAB (Xu et al. 2021). The performances of GINO-Q and the baseline algorithms in this problem are reported in Fig. 4. Unfortunately, the upper bounds obtained from the relaxed RMAB appear to be loose for these settings, so they are not plotted here. Nevertheless, once again, GINO-Q outperforms all benchmark algorithms across all settings. In the small-scale setting (M = 6), DQN performs as well as GINO-Q. However, as M increases to 10, DQN’s policy becomes less effective than both the gain and Whittle index policies due to the curse of dimensionality. When M = 100, the RMAB exhibits enormous state and action spaces that DQN cannot handle. In contrast, GINO-Q is able to learn a near-optimal index policy quickly, even for largescale RMABs. Its convergence speed is not affected by the increase in M, as long as the number of classes is fixed.

## Conclusion

In this paper, we introduced GINO-Q, a novel threetimescale stochastic approximation algorithm designed to address the challenges posed by RMABs. Our approach effectively tackles the curse of dimensionality by decomposing the RMAB into manageable single-arm problems, ensuring that the computational complexity grows linearly with the number of arms. Unlike existing Whittle-index-based learning algorithms, GINO-Q does not require RMABs to be indexable, significantly broadening its applicability. We showed experimentally that Whittle-index-based learning algorithms can perform poorly in non-indexable RMABs. In contrast, GINO-Q consistently learns near-optimal policies across all experimental RMABs, including non-indexable ones, and shows great efficiency by converging significantly faster than existing baselines.

20038

<!-- Page 8 -->

## Acknowledgements

The work of G. Chen and D. G¨und¨uz was supported in part by the UKRI for the Project AI-R (ERC Consolidator) under Grant EP/X030806/1, and by INFORMED-AI under Grant EP/Y028732/1. The work of S. C. Liew was supported in part by the General Research Funds (Project No. 14200221) established under the University Grant Committee of the Hong Kong Special Administrative Region, China.

## References

Abounadi, J.; Bertsekas, D.; and Borkar, V. S. 2001. Learning algorithms for Markov decision processes with average cost. SIAM Journal on Control and Optimization, 40(3): 681–698.

Avrachenkov, K. E.; and Borkar, V. S. 2022. Whittle index based Q-learning for restless bandits with average reward. Automatica, 139: 110186.

Biswas, A.; Aggarwal, G.; Varakantham, P.; and Tambe, M. 2021. Learn to Intervene: An Adaptive Learning Policy for Restless Bandits in Application to Preventive Healthcare. In Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI-21, 4039–4046.

Chen, G.; and Liew, S. C. 2024. An Index Policy for Minimizing the Uncertainty-of-Information of Markov Sources. IEEE Transactions on Information Theory, 70(1): 698–721.

Chen, G.; Liew, S. C.; and Shao, Y. 2022. Uncertaintyof-Information Scheduling: A Restless Multiarmed Bandit Framework. IEEE Transactions on Information Theory, 68(9): 6151–6173.

Demirel, B.; Ramaswamy, A.; Quevedo, D. E.; and Karl, H. 2018. DeepCAS: A Deep Reinforcement Learning Algorithm for Control-Aware Scheduling. IEEE Control Systems Letters, 2(4): 737–742.

Fu, J.; Nazarathy, Y.; Moka, S.; and Taylor, P. G. 2019. Towards Q-learning the Whittle Index for Restless Bandits. In 2019 Australian & New Zealand Control Conference (ANZCC), 249–254.

Glazebrook, K. D.; Ruiz-Hernandez, D.; and Kirkbride, C. 2006. Some Indexable Families of Restless Bandit Problems. Advances in Applied Probability, 38(3): 643–672.

Leong, A. S.; Ramaswamy, A.; Quevedo, D. E.; Karl, H.; and Shi, L. 2020. Deep reinforcement learning for wireless sensor scheduling in cyber–physical systems. Automatica, 113: 108759.

Liu, K.; and Zhao, Q. 2010. Indexability of restless bandit problems and optimality of whittle index for dynamic multichannel access. IEEE Transactions on Information Theory, 56(11): 5547–5567.

Mate, A.; Madaan, L.; Taneja, A.; Madhiwalla, N.; Verma, S.; Singh, G.; Hegde, A.; Varakantham, P.; and Tambe, M. 2022. Field study in deploying restless multi-armed bandits: Assisting non-profits in improving maternal and child health. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, 12017–12025.

Mnih, V.; Kavukcuoglu, K.; Silver, D.; Rusu, A. A.; Veness, J.; Bellemare, M. G.; Graves, A.; Riedmiller, M.; Fidjeland, A. K.; Ostrovski, G.; et al. 2015. Human-level control through deep reinforcement learning. nature, 518(7540): 529–533. Nakhleh, K.; Ganji, S.; Hsieh, P.-C.; Hou, I.; Shakkottai, S.; et al. 2021. NeurWIN: Neural Whittle index network for restless bandits via deep RL. Advances in Neural Information Processing Systems, 34: 828–839. Ni˜no-Mora, J. 2001. Restless bandits, partial conservation laws and indexability. Advances in Applied Probability, 33(1): 76–98. Ni˜no-Mora, J. 2007. Dynamic priority allocation via restless bandit marginal productivity indices. Top, 15(2): 161–198. Papadimitriou, C. H.; and Tsitsiklis, J. N. 1999. The Complexity of Optimal Queuing Network Control. Mathematics of Operations Research, 24(2): 293–305. Puterman, M. L. 2014. Markov decision processes: discrete stochastic dynamic programming. John Wiley & Sons. Sutton, R. S.; and Barto, A. G. 2018. Reinforcement learning: An introduction. MIT press. Tripathi, V.; and Modiano, E. 2019. A whittle index approach to minimizing functions of age of information. In 2019 57th Annual Allerton Conference on Communication, Control, and Computing (Allerton), 1160–1167. IEEE. Villar, S. S. 2016. Indexability and optimal index policies for a class of reinitialising restless bandits. Probability in the engineering and informational sciences, 30(1): 1–23. Wang, J.; Ren, X.; Mo, Y.; and Shi, L. 2019. Whittle index policy for dynamic multichannel allocation in remote state estimation. IEEE Transactions on Automatic Control, 65(2): 591–603. Wang, K.; and Chen, L. 2021. Restless Multi-Armed Bandit in Opportunistic Scheduling. Springer. Wang, K.; Xu, L.; Taneja, A.; and Tambe, M. 2023. Optimistic whittle index policy: Online learning for restless bandits. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 10131–10139. Wang, S.; Liu, H.; Gomes, P. H.; and Krishnamachari, B. 2018. Deep reinforcement learning for dynamic multichannel access in wireless networks. IEEE transactions on cognitive communications and networking, 4(2): 257–265. Weber, R. R.; and Weiss, G. 1990. On an index policy for restless bandits. Journal of applied probability, 27(3): 637– 648. Wei, T.; Wang, Y.; and Zhu, Q. 2017. Deep reinforcement learning for building HVAC control. In Proceedings of the 54th annual design automation conference 2017, 1–6. Whittle, P. 1988. Restless Bandits: Activity Allocation in a Changing World. Journal of Applied Probability, 25: 287– 298. Xiong, G.; and Li, J. 2023. Finite-time analysis of whittle index based Q-learning for restless multi-armed bandits with neural network function approximation. In Advances in Neural Information Processing Systems, volume 36, 29048– 29073.

20039

<!-- Page 9 -->

Xiong, G.; Li, J.; and Singh, R. 2022. Reinforcement learning augmented asymptotically optimal index policy for finite-horizon restless bandits. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, 8726– 8734. Xiong, G.; Qin, X.; Li, B.; Singh, R.; and Li, J. 2022. Indexaware reinforcement learning for adaptive video streaming at the wireless edge. In Proceedings of the Twenty-Third International Symposium on Theory, Algorithmic Foundations, and Protocol Design for Mobile Networks and Mobile Computing, 81–90. Xiong, G.; Wang, S.; and Li, J. 2022. Learning infinitehorizon average-reward restless multi-action bandits via index awareness. Advances in Neural Information Processing Systems, 35: 17911–17925. Xiong, G.; Wang, S.; Li, J.; and Singh, R. 2024. Whittle Index-Based Q-Learning for Wireless Edge Caching With Linear Function Approximation. IEEE/ACM Transactions on Networking. Xu, L.; Bondi, E.; Fang, F.; Perrault, A.; Wang, K.; and Tambe, M. 2021. Dual-mandate patrols: Multi-armed bandits for green security. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, 14974–14982.

20040
