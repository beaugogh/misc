---
title: "TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning"
source_url: https://iclr.cc/virtual/2026/oral/10009367
paper_pdf_url: https://arxiv.org/pdf/2510.00739v1
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning

<!-- Page 1 -->

TD-JEPA: Latent-predictive Representations for

Zero-Shot Reinforcement Learning

Marco Bagatella1,2,3,∗, Matteo Pirotta1, Ahmed Touati1, Alessandro Lazaric1, Andrea Tirinzoni1

1FAIR at Meta, 2ETH Zurich, 3Max Planck Institute for Intelligent Systems, Tübingen ∗Work done at Meta

Latent prediction–where agents learn by predicting their own latents–has emerged as a powerful paradigm for training general representations in machine learning. In reinforcement learning (RL), this approach has been explored to define auxiliary losses for a variety of settings, including reward-based and unsupervised RL, behavior cloning, and world modeling. While existing methods are typically limited to single-task learning, one-step prediction, or on-policy trajectory data, we show that temporal difference (TD) learning enables learning representations predictive of long-term latent dynamics across multiple policies from offline, reward-free transitions. Building on this, we introduce TD-JEPA, which leverages TD-based latent-predictive representations into unsupervised RL. TD-JEPA trains explicit state and task encoders, a policy-conditioned multi-step predictor, and a set of parameterized policies directly in latent space. This enables zero-shot optimization of any reward function at test time. Theoretically, we show that an idealized variant of TD-JEPA avoids collapse with proper initialization, and learns encoders that capture a low-rank factorization of long-term policy dynamics, while the predictor recovers their successor features in latent space. Empirically, TD-JEPA matches or outperforms state-of-the-art baselines on locomotion, navigation, and manipulation tasks across 13 datasets in ExoRL and OGBench, especially in the challenging setting of zero-shot RL from pixels.

Date: October 2, 2025

Correspondence: tirinzoni@meta.com

## Introduction

Learning effective state representations is a core challenge in reinforcement learning (RL). Useful representations should capture the dynamics of the environment in a way that supports efficient value estimation and policy optimization across tasks (Watter et al., 2015; Silver et al., 2018; Hafner et al., 2019; Gelada et al., 2019). A promising line of work is latent-predictive (a.k.a. self-predictive) representation learning (Schwarzer et al., 2021; Grill et al., 2020; Guo et al., 2020; Tang et al., 2023), an instance of the joint-embedding predictive architecture (LeCun, 2022, JEPA) paradigm. These algorithms jointly learn a state encoder ϕ(s) and a predictor P, i.e., a latent dynamics model estimating the representation of a future state s′: P(ϕ(s)) ≃ϕ(s′). Latent-predictive methods thus perform self-supervised learning entirely in latent space without any reward or reconstruction of (possibly high-dimensional) states.

Several RL methods leverage latent prediction as an auxiliary loss to improve sample efficiency and generalization in reward-based learning (Schwarzer et al., 2021; Guo et al., 2020; Hansen et al., 2024), behavior cloning (Lawson et al., 2025), and curiosity-driven exploration (Guo et al., 2022). As latent-predictive losses do not require any reward, they have been recently used for unsupervised RL: Assran et al. (2025), Zhou et al. (2025) and Sobal et al. (2025) learn latent world models that can solve goal-reaching tasks via test-time planning, whereas Jajoo et al. (2025) learn a state encoder from trajectory data to define the space of tasks used to optimize zero-shot unsupervised policies.

This paper proposes a novel way to instantiate latent-predictive representations for unsupervised RL. While previous methods have largely focused on either one-step dynamics, single-task/single-policy training, or relied on on-policy data, we introduce a policy-conditioned, multi-step formulation based on a novel off-policy temporal-difference loss. This objective encourages representations that are predictive not only of immediate transitions, but also of long-term features relevant for value estimation across multiple policies. This property arXiv:2510.00739v1 [cs.LG] 1 Oct 2025

<!-- Page 2 -->

...

**Figure 1.** TD-JEPA trains policies πz parameterized by latents z. The predictor, conditioned on z, predicts the representations of future states visited by πz (left). When trained via TD, the predictor (arrows on the right) approximates successor features for each policy, i.e., the weighted barycenter (stars) of representations of visited states (circles).

makes such representations and the associated predictors particularly well-suited for integration with off-policy, successor-feature based approaches to zero-shot unsupervised RL (Touati and Ollivier, 2021; Touati et al., 2023; Park et al., 2024).

We thus instantiate temporal difference latent-predictive representation learning into TD-JEPA, a zero-shot unsupervised RL algorithm which pre-trains four components: a state encoder, a policy-conditioned multi-step predictor, a task encoder, and a set of parameterized policies, all of which are learned end-to-end from offline, reward-free transitions. Departing from previous approaches, latent prediction is not merely an auxiliary loss, but rather the core objective that enables TD-JEPA to learn all the components needed to distill zero-shot policies. In fact, the predictor may be leveraged as an approximation of successor features (see Figure 1) to extract policies mapping encoded observations to optimal actions for all reward functions in the span of the learned features. This enables TD-JEPA to perform zero-shot policy optimization for any downstream reward, entirely in latent space.

Theoretically, for an idealized version of TD-JEPA with linear predictors, we show that 1) the representations do not collapse with a suitable initialization; 2) they recover a low-rank factorization of the successor measures of the trained policies, while the predictor approximates successor features in latent space; 3) they minimize an upper bound on the policy evaluation error for any reward, thus making zero-shot optimization possible. These results build on a novel “gradient matching” argument that extends and generalizes existing theoretical analyses of latent-predictive representations, and connect TD-JEPA with other unsupervised RL methods such as forward-backward (Touati and Ollivier, 2021) and intention-conditioned value functions (Ghosh et al., 2023).

Empirically, we evaluate TD-JEPA on 65 tasks across 13 datasets from ExoRL (Yarats et al., 2022a) and OGBench (Park et al., 2025a), covering locomotion, navigation, and manipulation with both proprioceptive and pixel-based observations. TD-JEPA matches or outperforms state-of-the-art zero-shot baselines across these settings, in particular when learning from pixels, which has proven to be one of the most challenging settings for unsupervised RL so far. Moreover, we ablate several dimensions of the algorithm, demonstrating the importance of learning representations that are predictive of multi-step policy-dependent dynamics, and the advantage of training distinct state and task encoders. Finally, we show that learned representations can be easily reused for offline or online RL, improving over zero-shot policies and learning from scratch.

## Preliminaries

We consider a reward-free Markov Decision Process M = (S, A, P, γ), where S and A are state and action spaces, P is the probability measure over next states when taking action a in state s as P(ds′ | s, a), and γ ∈[0, 1) is a discount factor. Executing a Markov policy π: S →Prob(A) induces an unnormalized distribution over visited states, which is referred to as the successor measure:

M π(X | s, a) =

∞ X t=0 γtPr(st+1 ∈X|s, a, π) ∀X ⊆S. (1)

![Figure extracted from page 2](2026-ICLR-td-jepa-latent-predictive-representations-for-zero-shot-reinforcement-learning/page-002-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

Given a reward function r: S →R and a policy π, the action-value function Qπ r (s, a) measures the cumulative discounted reward obtained by the policy over an infinite horizon, i.e., Qπ r (s, a) = E

P∞ t=0 γtr(st+1) | s, a, π

. Action-value functions are connected to successor measures via

Qπ r (s, a) =

Z s+∈S

M π(ds+ | s, a)r(s′) = Es+∼M π(·|s,a)

r(s+)

, (2)

which shows a convenient linear decomposition of Qπ r into the reward function and the dynamics induced by π. Standard RL agents aim at finding reward-maximizing policies π⋆ r(s) ∈arg maxa∈A Q⋆ r(s, a), where Q⋆ r(s, a):= maxπ Qπ r (s, a).

Latent-predictive representations. In high-dimensional settings, state encoders ϕ: S →Rdϕ may be learned to ease the estimation of action-value functions. For instance, if an encoder ϕ is such that Qπ r (s, a) = ϕ(s)⊤wπ a,r for some vector wπ a,r ∈Rdϕ, then the RL process reduces to learning vectors in Rdϕ rather than high-dimensional functions Qπ r (s, a). Latent-predictive learning has been shown to be an effective approach for this problem. In the simplest formulation, latent-predictive representations capture the one-step latent dynamics of a policy π by minimizing the loss

Lone-step(ϕ, T) = Es∼ρ,a∼π(·|s),s′∼P (·|s,a)

∥T(ϕ(s)) −ϕ(s′)∥2

, (3)

where T: Rdϕ →Rdϕ is a (possibly non-linear) predictor of the latent one-step dynamics induced by ϕ and policy π, and ϕ denotes stop-gradient. Notably, optimizing for this loss does not require any decoding or reconstruction, and it only relies on an unsupervised dataset D = {(s, a, s′)}. Different instantiations of this approach have been shown both empirically and theoretically to produce representations that accurately approximate action-value functions or policies (Guo et al., 2022; Tang et al., 2023; Voelcker et al., 2024; Lawson et al., 2025; Fujimoto et al., 2025).

Successor-features and zero-shot unsupervised RL. Considering a state encoder ψ: S →Rdψ and the associated space of linear rewards Rψ = {r(s) = ψ(s)⊤z | z ∈Rdψ}, Q-values for any reward function r(s) = ψ(s)⊤zr ∈Rψ can be written as

Qπ r (s, a) =

Z s+∈S

M π(ds+ | s, a)ψ(s+)⊤zr = Es+∼M π(·|s,a)

ψ(s+)

⊤zr:= F π ψ (s, a)⊤zr, (4)

where F π ψ (s, a) ∈Rdψ captures the successor features of π (Barreto et al., 2017). The majority of unsupervised zero-shot RL methods (Touati and Ollivier, 2021; Park et al., 2024; Agarwal et al., 2025; Jajoo et al., 2025) learn successor features F(s, a; z) ≈F πz ψ (s, a) for a set of parameterized policies {πz(s)}z∈Z, with Z ⊆Rd, that are trained to be optimal for all rewards in Rψ, i.e., πz(s) ≈arg maxa F(s, a; z)⊤z, where F(s, a; z)⊤z is an approximation of Q⋆ r(s, a) for r(s) = ψ(s)⊤z. At test time, given a reward function r, a vector zr ∈Rdψ is first obtained by projecting r onto Rψ, and the associated policy πzr is then returned.

Given the role played by ψ in defining the space of tasks of interest, with an abuse of terminology, we will refer to ψ as a task encoder. On the other hand, we shall call state encoder a map ϕ: S →Rdϕ that is used to embed states before feeding them into different networks (e.g., we will train successor features F π ψ (ϕ(s), a) and policies π(ϕ(s)) in the latent space given by ϕ). While the zero-shot methods cited so far train the task encoder ψ in different ways, and do not train any explicit state encoder ϕ, the next section will show how multi-step policy-dependent latent-predictive learning can be used to train both simultaneously.

Latent-Predictive Temporal-Difference Representations

We begin by showing how the latent-predictive loss of Eq. 3 can model multi-step and policy-dependent dynamics, and how temporal difference (TD) learning allows learning from offline transition data. We will then expand this idea to learn separate state and task embeddings, and finally show how it can be instantiated as a zero-shot unsupervised RL method.

<!-- Page 4 -->

## 3.1 Multi-step policy-conditioned latent prediction

Let {πz}z∈Z be a family of policies parameterized by z ∈Z, and D = {(s, a, s′)} be a dataset of transitions. We train a state encoder ϕ: S →Rdϕ and a policy-dependent predictor Tϕ: Rdϕ × A × Z →Rdϕ to be latent-predictive of the long-term dynamics of the policies {πz}, i.e.,

LMC-JEPA(ϕ, Tϕ) = E(s,a)∼D,z∼Z,s+∼M πz (·|s,a)

∥Tϕ(ϕ(s), a, z) −ϕ(s+)∥2

, (5)

where MC-JEPA stands for Monte-Carlo (MC) JEPA loss, as on-policy samples s+ ∼M πz(·|s, a) are needed for all policies of interest. Intuitively, Tϕ(ϕ(s), a, z) tries to predict future latent states visited by the policy πz. More formally, predictors trained via minimization of LMC-JEPA(ϕ, Tϕ) approximate the successor features of ϕ in the latent space induced by ϕ itself.

Proposition 1. For any ϕ and Tϕ, we have the following equivalence

LMC-JEPA(ϕ, Tϕ) = E(s,a)∼D,z∼Z

∥Tϕ(ϕ(s), a, z) −F πz ϕ (s, a)∥2

+ const. (6)

Given the connection between Q-functions and successor features (Eq. 4), this result crucially relates multi-step latent prediction with value estimation across multiple policies. More precisely, it implies that the predictor enables policy evaluation and optimization of rewards in the span of ϕ, as we detail at the end of this section. Since F πz ϕ is the successor features of ϕ, with the terminology introduced in Sec. 2, ϕ is used both as a state encoder, i.e., to embed states passed to the predictor, and as a task encoder, i.e., defining a space of reward functions.

Unfortunately, this loss cannot be estimated on off-policy data since it requires sampling from the successor measures of the given policies. We can however leverage the previous result and the fact that successor features admit a Bellman equation F πz ϕ (s, a) = Es′∼P (·|s,a),a′∼πz(s′)[ϕ(s′) + γF πz ϕ (s′, a′)] (Barreto et al., 2017) to define a temporal-difference version of the previous loss:

LTD-JEPA(ϕ, Tϕ) = E(s,a,s′)∼D,z∼Z,a′∼πz(·|s′)

∥Tϕ(ϕ(s), a, z) −ϕ(s′) −γTϕ(ϕ(s′), a′, z)∥2

. (7)

Unlike the Monte Carlo loss of Eq. 5, LTD-JEPA only requires sampling one-step transitions and actions from the given policies, and it can thus be estimated from off-policy, offline datasets.

## 3.2 Training separate state and task representations

While in Eq. 5 and 7 the same encoder ϕ is used for both state and task representations, these need not be the same in practice. Consider, for instance, a robot navigating a building: useful state representations may capture low-level dynamical information critical for control (e.g., joint positions and velocities), while task representations could abstract higher-level contextual features, such as the building’s topology. In this case, a single representation might be either too complex, or too abstract: having flexibility over the dimensionality and content of each representation would be desirable. We thus now introduce an asymmetric variant that trains a distinct encoder ψ: S →Rdψ to define the set of reward functions of interest (i.e., as a task encoder). We first redefine the predictor as Tϕ: Rdϕ × A × Z →Rdψ and the latent-predictive Monte-Carlo loss to train ϕ and Tϕ as

LMC-JEPA(ϕ, Tϕ, ψ) = E(s,a)∼D,z∼Z,s+∼M πz (·|s,a)

∥Tϕ(ϕ(s), a, z) −ψ(s+)∥2

, (8)

such that Tϕ maps states encoded through ϕ to the long-term dynamics of a policy πz in the latent space induced, this time, by ψ. Similar to Prop. 1, Tϕ approximates the successor features F πz ψ (s, a) of ψ in the latent space induced by ϕ. Symmetrically, we train ψ together with an additional predictor Tψ: Rdψ × A × Z →Rdϕ. To do so, we follow existing literature – according to which joint representations should be predictive of each other (Guo et al., 2020; Tang et al., 2023) – and train ψ and Tψ through the same latent-predictive loss with the roles of ϕ and ψ inverted, i.e., LMC-JEPA(ψ, Tψ, ϕ).1 As before, we can then design an off-policy TD

1While some existing works use forward-in-time sampling to train one representation and backward-in-time for the other, we use two forward-in-time losses. We further discuss this difference in App. C.

<!-- Page 5 -->

## Algorithm

1 TD-JEPA for zero-shot RL

Inputs: Dataset D, batch size B, regularization coefficient λ, networks π, Tϕ, ϕ, Tψ, ψ Initialize target networks: T − ϕ ←Tϕ, ϕ−←ϕ, T − ψ ←Tψ, ψ−←ψ while not converged do

▷Sample training batch {(si, ai, s′ i)}B i=1 ∼D, {zi}B i=1 ∼Z, {a′ i}B i=1 ∼{π(ϕ−(s′ i), zi)}B i=1

▷Compute latent-predictive losses b LTD-JEPA(ϕ, Tϕ, ψ) = 1 2B P i

Tϕ(ϕ(si), ai, zi) −ψ−(s′ i) −γT − ϕ (ϕ−(s′ i), a′ i, zi)

2 b LTD-JEPA(ψ, Tψ, ϕ) = 1 2B P i

Tψ(ψ(si), ai, zi) −ϕ−(s′ i) −γT − ψ (ψ−(s′ i), a′ i, zi)

2

▷Compute orthonormality regularization losses b LREG(ϕ) = 1 2B(B−1) P i̸=j(ϕ(si)⊤ϕ(sj))2 −1

B

P i ϕ(si)⊤ϕ(si) b LREG(ψ) = 1 2B(B−1) P i̸=j(ψ(si)⊤ψ(sj))2 −1

B

P i ψ(si)⊤ψ(si)

▷Compute actor loss {ˆai}B i=1 ∼{π(ϕ(si), zi)}B i=1 b Lactor(π) = −1

B

PB i=1 Tϕ(ϕ(si), ˆai, zi)Tzi

Update ϕ, Tϕ to minimize b LTD-JEPA(ϕ, Tϕ, ψ) + λ b LREG(ϕ) Update ψ, Tψ to minimize b LTD-JEPA(ψ, Tψ, ϕ) + λ b LREG(ψ) Update π to minimize b Lactor(π) Update target networks ϕ−, T − ϕ, ψ−, T − ψ via EMA of ϕ, Tϕ, ψ, Tψ variant of this loss,

LTD-JEPA(ϕ, Tϕ, ψ) = E (s,a,s′)∼D z∼Z,a′∼πz(·|s′)

∥Tϕ(ϕ(s), a, z) −ψ(s′) −γTϕ(ϕ(s′), a′, z)∥2

, (9)

so that ϕ and Tϕ are optimized via LTD-JEPA(ϕ, Tϕ, ψ), while ψ and Tψ via LTD-JEPA(ψ, Tψ, ϕ).

## 3.3 TD-JEPA representations for zero-shot RL

The relationship between the learned predictors and successor features suggests a seamless instantiation of TD-JEPA as a zero-shot unsupervised RL algorithm. Redefining the policy parameter space Z as the task embedding space (i.e., Z ⊆Rdψ), we train latent policies such that πz(ϕ(s)) = argmaxa Tϕ(ϕ(s), z, a)⊤z for all z ∈Z2. Since Tϕ(ϕ(s), z, a) ≃F πz ψ (s, a) (Proposition 1), this produces optimal policies for all rewards in the span of ψ, learned directly from state representations ϕ(·). At test time, given an inference dataset of rewarded samples Drwd = {(s, r)}, the optimal policy πzr can be retrieved by computing zr through linear regression, e.g. through the closed-form solution zr = argminz E(s,r)∼Drwd[(r −ψ(s)⊤z)2] = Es∼Drwd[ψ(s)ψ(s)T]−1E(s,r)∼Drwd[ψ(s)r(s)]. Alg. 1 describes TD-JEPA, which combines LTD-JEPA with stabilization strategies, e.g. target networks and covariance regularization. We remark that latent prediction is not auxiliary: it is the core objective that trains encoders and predictors, from which zero-shot policies can be directly distilled.

## 4 Theoretical Analysis

We now provide some theoretical arguments showing how latent-predictive temporal difference representations capture the long-term dynamics of a given set of policies in a way that makes them amenable to zero-shot RL. Following Tang et al. (2023), we consider a simplified tabular setting with linear predictors. We view the representation ϕ (resp. ψ) as a S × dϕ (resp. S × dψ) matrix, and consider action-free predictors Tϕ,z (resp. Tψ,z) as dϕ × dψ (resp. dψ × dϕ) matrices for all z. The expression Tϕ(ϕ(s), a, z) in Eq. 8 and 9 thus reduces to T T ϕ,zϕ(s), while M π(s′|s, a) and P(s′|s, a) are replaced by M πz(s′|s) = M πz(s′|s, πz(s)) and P πz(s′|s) = P(s′|s, πz(s)).

2This decision additionally grounds ψ as task encoder, and breaks the symmetry that could arise from the two encoders ϕ and ψ being trained through similar latent-predictive objectives.

<!-- Page 6 -->

## 4.1 Monte-Carlo losses

We define a (non-latent-predictive) successor measure approximation loss

LSM(ϕ, {Tz}z, ψ): = 1

2Ez∼Z∥ϕTzψT −M πz∥2 F. (10)

Minimizing LSM is equivalent to finding the best multilinear approximation to the successor measures M πz. We prove the following connection with the Monte Carlo latent-predictive loss of Eq. 8.

Theorem 1. For fixed ϕ and ψ, let T ⋆ z, T ⋆ ϕ,z, T ⋆ ψ,z be the optimal predictors for LSM(ϕ, Tz, ψ) (Eq. 10), LMC-JEPA(ϕ, Tϕ,z, ψ), LMC-JEPA(ψ, Tψ,z, ϕ) (Eq. 8), respectively. If (A1) ϕTϕ = ψTψ = I, (A2) the state distribution is uniform, and (A3) for all z ∈Z, the matrix P πz is symmetric, then

1. for all z, ϕT ⋆ z = ϕT ⋆ ϕ,z = ΠϕM πzψ and ψT ⋆ ψ,z = ψ(T ⋆ z)T = ΠψM πzϕ, where Πϕ (resp. Πψ) is an orthogonal projection on the span of ϕ (resp. ψ);

2. ∇ϕLMC-JEPA(ϕ, Tz, ψ) = ∇ϕLSM(ϕ, Tz, ψ) and ∇ψLMC-JEPA(ψ, Tz, ϕ) = ∇ψLSM(ϕ, T T z, ψ).

This result reveals that 1) the optimal predictors for the successor measure loss LSM and the latent-predictive loss LMC-JEPA match, and yield an orthogonal projection of the successor features M πzψ onto the ϕ space; 2) the gradients w.r.t. the representations ϕ and ψ, when evaluated at any predictor, match among these two losses, showing that gradient descent on LMC-JEPA would update representations in the direction that reduces LSM, hence improving the approximation of the successor measures. This result follows as a special case of a novel theorem (see App. C) generalizing and implying all previous guarantees for latent-predictive representations (Tang et al., 2023; Khetarpal et al., 2025; Voelcker et al., 2024; Lawson et al., 2025), which we believe is of independent interest. Finally, we remark that, while the assumptions A1-A3 have been considered in all these related works, they can be relaxed, at the price of more involved proofs and notation, as shown in App. C.

## 4.2 Temporal-difference losses

We first derive a non-collapse guarantee. While a similar result was originally proved by Tang et al. (2023)

for the one-step loss (Eq. 3), our case is more complex since TD latent-prediction can be seen as “doubly latent-predictive” (cf. Eq. 9): T T ϕ,zϕ(s) is optimized to match a representation being learned – ψ(s+) – plus a bootstrapped version of itself – T T ϕ,zϕ(s+).

Theorem 2. Let ϕt and ψt be the representations learned under a continuous-time relaxation of Eq. 9 where, at each step t, the optimal predictors for (ϕt, ψt) are first computed and then a gradient step on (ϕt, ψt) is taken (see App. B.3 for the explicit formulation). Then, the covariance matrices ϕT t ϕt and ψT t ψt are constant over time, i.e., ϕT t ϕt = ϕT

0 ϕ0 and ψT t ψt = ψT

0 ψ0 for all t ≥0.

This result suggests that, if predictors are trained at a faster rate than representations, the overall dynamics preserve their covariance, thus preventing ϕ and ψ from collapsing to trivial solutions (e.g., ϕ = ψ = 0) when properly initialized, e.g., with unitary covariance.

As done for MC objectives (Th. 1), we now show that the latent-predictive loss of TD-JEPA is related to forward and backward TD losses for approximating the successor measure (Blier et al., 2021).

Theorem 3. Consider the following TD losses for approximating the successor measure

Lfw(ϕ, Tz, ψ):= 1

2Ez∼Z h

∥ϕTzψT −P πz −γP πzϕTzψT∥2

F i

, (11)

Lbw(ϕ, Tz, ψ):= 1

2Ez∼Z h

∥ψTzϕT −(P πz)T −γ(P πz)TψTzϕT∥2

F i

. (12)

For fixed (ϕ, ψ), let T ⋆ z,fw, T ⋆ z,bw, T ⋆ ϕ,z, T ⋆ ψ,z respectively be the optimal predictors for Lfw(ϕ, Tz, ψ), Lbw(ϕ, Tz, ψ), LTD-JEPA(ϕ, Tz, ψ), LTD-JEPA(ψ, Tz, ϕ). Under the same assumptions as Th. 1,

<!-- Page 7 -->

1. for all z, ϕT ⋆ ϕ,z = ϕT ⋆ z,fw = ˜Πϕ,zM πzψ and ψT ⋆ ψ,z = ψT ⋆ z,bw = ˜Πψ,zM πzϕ, where ˜Πϕ,z (resp. ˜Πψ,z) is an oblique projection on the span of ϕ (resp. ψ);

2. ∇ϕLTD-JEPA(ϕ, Tz, ψ) = ∇ϕLfw(ϕ, Tz, ψ) and ∇ψLTD-JEPA(ψ, Tz, ϕ) = ∇ψLfw(ϕ, Tz, ψ).

Similar to Th. 1, the optimal predictors and gradients of TD-JEPA match those of the non-latent-predictive TD losses of Eq. 11 and 12, which are known to recover an approximation of the successor measure for bilinear parameterizations of the form F T z B (Blier et al., 2021). Unlike in the Monte Carlo case, here the optimal predictors solve a least-squares TD problem (Boyan, 1999; Precup et al., 2001), yielding the fixed point of a projected Bellman operator whose closed-form expression is an oblique projection (Scherrer, 2010).

## 4.3 Policy evaluation and zero-shot RL

Finally, the following result motivates the significance of optimizing the successor measure losses of Eq. 10, 11, and 12.

Theorem 4. Let ϕ, ψ have identity covariance matrices. For any reward function r, let ωr:= (ψTψ)−1ψTr be the linear regression weight for representation ψ. Then, for any Tz, max r∈RS:∥r∥2≤1 Ez∈Z

"X s∈S

V πz r (s) −ϕ(s)TTzωr

2

#

≤2LSM(ϕ, Tz, ψ).

Moreover, LSM(ϕ, Tz, ψ) ≤cLfw(ϕ, Tz, ψ) and LSM(ϕ, Tz, ψ) ≤cLbw(ϕ, Tz, ψ) for some c.

Paraphrasing, the policy evaluation error of the technique in Section 3.3 (i.e., embed r into a vector ω through linear regression on ψ, and compute Tϕ(ϕ(s), z)Tω) is bounded by the successor measure approximation loss and the corresponding TD errors. Both these quantities are indirectly optimized by TD-JEPA (Th. 1, 3), which is thus a sound approach for zero-shot policy evaluation. Moreover, Th. 4 leads to a zero-shot optimality result analogous to Theorem 2 of (Touati and Ollivier, 2021): if the approximation of M πz is perfect (i.e., M πz = ϕTzψT for all z or, equivalently, the TD errors in Eq. 11 and 12 are zero) and the policies πz are optimal for all linear rewards in ψ, then the inference procedure above recovers optimal policies for any (even non-linear) reward function.

## 5 Experiments

We benchmark zero-shot performance across a diverse set of problems, including 4 locomotion/navigation domains from ExoRL/DMC (Tassa et al., 2018; Yarats et al., 2022a), as well as 9 navigation/manipulation domains from OGBench (Park et al., 2025a). The former suite involves reward-based tasks and highcoverage data, while the latter evaluates goal-reaching and provides low-coverage datasets3. We consider both proprioceptive and pixel-based variants of all domains, and report expected returns/success rates across a set of tasks (4-8 depending on the domain) as main evaluation metric. In DMC, we often normalize returns by the maximum achievable (1000).

We structure our evaluation in four parts: (i) a comprehensive evaluation of TD-JEPA with respect to existing zero-shot methods; (ii) an ablation over the prediction target, measuring the impact of multi-step, policy-aware dynamics modeling; (iii) a comparison of TD-JEPA to its symmetric variant that learns a shared state-task encoder ϕ; and (iv) a demonstration of fast adaptation from pre-trained state representations. Further results are presented in App. D, and implementation details in App. E.

5.1 How does TD-JEPA compare to zero-shot RL algorithms?

We first compare TD-JEPA to three groups of successor-feature-based zero-shot RL baselines:4

3We additionally apply BC regularization in OGBench based on Park et al. (2025b), as detailed in App. E.6 4Notice that only Laplacian, HILP, FB and RLDP are standard zero-shot unsupervised RL algorithms, while BYOL, BYOL-γ, and ICVF (henceforth marked with a ∗) are representation learning methods: their instantiation in a zero-shot framework is novel and designed to investigate the impact of different representations.

<!-- Page 8 -->

Laplacian ICVF* HILP FB RLDP BYOL* BYOL-γ* TD-JEPA

DMCRGB (avg) 293.1 ± 15.1 438.7 ± 14.9 391.2 ± 23.8 456.2 ± 8.6 525.7 ± 13.3 513.8 ± 11.6 582.4 ± 9.8 628.8 ± 5.5 walker 309.4 ± 50.0 534.9 ± 61.3 422.8 ± 32.5 324.4 ± 16.6 576.1 ± 35.3 595.2 ± 9.0 648.3 ± 36.5 738.9 ± 3.5 cheetah 242.4 ± 29.6 394.9 ± 30.1 333.0 ± 86.6 622.4 ± 23.1 605.3 ± 23.5 468.0 ± 46.7 679.8 ± 17.1 706.0 ± 4.1 quadruped 430.1 ± 32.3 583.3 ± 17.2 513.9 ± 10.8 475.4 ± 16.7 551.1 ± 23.4 581.8 ± 16.6 570.0 ± 6.6 626.7 ± 13.6 pointmass 190.4 ± 12.4 241.6 ± 35.6 294.9 ± 33.4 402.8 ± 16.8 370.3 ± 12.0 410.3 ± 8.5 431.6 ± 17.4 443.7 ± 10.9

DMC (avg) 591.1 ± 10.7 619.3 ± 10.3 620.1 ± 8.4 648.2 ± 4.1 610.2 ± 13.5 618.6 ± 10.5 645.4 ± 10.5 661.2 ± 6.3 walker 769.7 ± 4.7 727.0 ± 16.2 796.4 ± 7.7 811.5 ± 5.9 723.9 ± 18.3 746.8 ± 11.0 786.1 ± 9.6 785.2 ± 6.7 cheetah 614.5 ± 18.9 606.3 ± 16.8 618.3 ± 5.8 672.7 ± 4.9 575.6 ± 44.9 622.8 ± 23.9 647.2 ± 9.0 688.7 ± 6.7 quadruped 635.0 ± 38.7 708.5 ± 14.2 694.8 ± 11.0 595.6 ± 9.1 665.0 ± 13.9 611.8 ± 28.1 683.1 ± 26.1 691.4 ± 5.0 pointmass 345.1 ± 22.4 435.5 ± 11.1 371.0 ± 37.1 513.0 ± 20.0 476.3 ± 39.4 493.0 ± 41.3 465.1 ± 17.6 479.3 ± 23.6

OGBenchRGB (avg) 30.58 ± 0.81 25.22 ± 0.55 32.56 ± 0.92 39.89 ± 0.47 39.09 ± 0.59 40.33 ± 0.52 41.58 ± 0.64 41.34 ± 0.45 antmaze-mn 92.20 ± 2.91 85.80 ± 3.02 84.60 ± 3.59 96.80 ± 0.74 97.60 ± 0.50 94.40 ± 1.48 98.00 ± 0.73 96.67 ± 1.11 antmaze-ln 35.40 ± 2.97 42.60 ± 2.84 47.00 ± 4.04 76.80 ± 2.33 63.60 ± 3.89 62.20 ± 3.42 68.80 ± 2.70 74.60 ± 3.35 antmaze-ms 60.20 ± 3.88 46.20 ± 2.74 71.80 ± 2.22 86.20 ± 2.05 90.60 ± 1.91 90.40 ± 1.97 86.00 ± 3.10 84.40 ± 3.85 antmaze-ls 7.20 ± 1.98 7.20 ± 1.20 23.60 ± 1.83 27.40 ± 2.78 21.80 ± 1.01 26.60 ± 2.23 28.60 ± 1.71 28.80 ± 2.50 antmaze-me 0.00 ± 0.00 0.00 ± 0.00 0.20 ± 0.20 1.80 ± 1.09 0.80 ± 0.44 1.20 ± 1.00 3.20 ± 1.98 0.20 ± 0.20 cube-single 73.80 ± 3.53 34.80 ± 7.03 56.40 ± 3.82 62.00 ± 2.27 63.20 ± 3.91 75.40 ± 2.58 76.40 ± 3.24 67.80 ± 3.67 cube-double 1.60 ± 0.72 0.80 ± 0.44 1.60 ± 0.58 1.20 ± 0.61 2.20 ± 1.31 2.40 ± 0.65 1.40 ± 0.67 3.00 ± 0.91 scene 2.80 ± 1.12 8.40 ± 1.45 5.40 ± 1.63 4.20 ± 0.87 9.40 ± 1.33 8.80 ± 1.64 11.20 ± 1.82 14.20 ± 2.22 puzzle-3x3 2.00 ± 1.40 1.20 ± 0.44 2.44 ± 0.99 2.60 ± 0.79 2.60 ± 0.79 1.60 ± 0.40 0.60 ± 0.31 2.40 ± 0.83

OGBench (avg) 14.81 ± 1.32 30.87 ± 0.58 37.98 ± 1.11 39.04 ± 0.66 27.07 ± 0.83 26.42 ± 0.83 30.42 ± 0.94 37.98 ± 0.77 antmaze-mn 50.00 ± 4.94 79.80 ± 2.62 83.60 ± 2.63 73.00 ± 2.72 74.60 ± 4.15 58.40 ± 2.00 51.40 ± 1.55 70.40 ± 3.72 antmaze-ln 21.60 ± 3.90 58.40 ± 1.90 52.60 ± 3.86 36.80 ± 4.28 36.40 ± 4.66 26.60 ± 3.03 21.80 ± 3.57 57.20 ± 4.25 antmaze-ms 21.40 ± 4.32 39.00 ± 3.30 50.60 ± 2.46 70.40 ± 3.95 58.40 ± 3.29 60.60 ± 5.07 45.60 ± 2.84 61.56 ± 4.53 antmaze-ls 11.80 ± 1.47 13.20 ± 1.64 12.20 ± 1.75 49.80 ± 5.64 19.60 ± 2.73 25.80 ± 4.28 20.20 ± 1.80 40.60 ± 2.51 antmaze-me 0.80 ± 0.61 0.00 ± 0.00 2.00 ± 0.84 51.60 ± 2.65 4.80 ± 2.35 11.40 ± 2.29 19.60 ± 2.53 20.20 ± 2.39 cube-single 15.11 ± 1.49 20.40 ± 1.93 74.20 ± 3.53 49.60 ± 3.83 19.80 ± 2.41 22.00 ± 3.16 79.40 ± 2.83 34.20 ± 2.88 cube-double 2.00 ± 0.42 5.00 ± 0.80 20.00 ± 2.72 2.60 ± 0.43 3.80 ± 0.76 4.40 ± 0.72 2.60 ± 0.67 3.60 ± 0.78 scene 7.80 ± 1.28 45.40 ± 2.29 43.80 ± 1.90 12.80 ± 1.61 11.60 ± 1.57 15.40 ± 1.37 14.40 ± 2.32 38.44 ± 1.37 puzzle-3x3 2.80 ± 0.68 16.60 ± 0.73 2.80 ± 0.68 4.80 ± 0.68 14.60 ± 0.90 13.20 ± 1.91 18.80 ± 0.44 15.60 ± 1.11

**Table 1.** Performance of zero-shot algorithms for DMC (reward) and OGBench (success rate) with either proprioception or RGB inputs. We report means and standard errors across seeds. Numbers are bold for top algorithms if confidence intervals overlap.

• Laplacian (Wu et al., 2019), HILP (Park et al., 2024), and FB (Touati and Ollivier, 2021) are established zero-shot methods that train a task encoder ψ, without specific learning objectives for a state encoder.

• BYOL⋆(Grill et al., 2020), BYOL-γ⋆(Lawson et al., 2025) and RLDP (Jajoo et al., 2025) learn a state encoder ϕ via latent-predictive learning, which we then use as a task encoder for successor features (learned through a contrastive loss in the case of RLDP).

• ICVF⋆(Ghosh et al., 2023) learns a multilinear decomposition of the successor measure via expectile regression, yielding both state and task encoders on top of which we train successor features.

For a fair comparison, each method is tuned over comparable hyperparameter grids and adopts the same architecture: in particular, the state input is always passed through an explicit state encoder before being fed into, e.g., the successor features estimator F(s, a; z)5. We find that this protocol results in significant improvements in zero-shot performances, even for existing methods (e.g., 1.3× and 2.4× higher than overlapping pixel-based results for the methods presented in Park et al. (2024) and Jajoo et al. (2025), respectively), as displayed in Tab 1. When considering suite-aggregated performance, we find that TD-JEPA is on par or better than the best performing baseline in each suite. Given the diverse nature of suites (proprioception vs pixels), domains (locomotion, navigation, manipulation) and datasets (high- vs low-coverage), many algorithms unsurprisingly achieve strong performance in some configurations while under-performing in others. We thus additionally measure how consistently well each algorithm performs by computing the probability of improvement (Agarwal et al., 2021) across all domains in Fig. 2. We find that TD-JEPA is consistently among the top performing algorithms, whereas most baselines perform well on a narrow subset of problems. For instance, while TD-JEPA is only slightly preferable to FB and HILP from proprioception, it is significantly better than them in visual domains. Similarly, BYOL-γ is slightly better than TD-JEPA in OGBenchRGB, but it is significantly worse in DMCRGB and OGBench. Finally, we note that latent-predictive methods tend to be generally preferrable in pixel-based domains.

5On average, explicit state encoders actually improve the performance for existing methods, see App. D.1.

<!-- Page 9 -->

TD-JEPA

BYOL- *

BYOL*

RLDP

FB

HILP

ICVF*

Laplacian

Y

TD-JEPA BYOL- *

BYOL*

RLDP

FB HILP ICVF* Laplacian

X

50±0 62±7 67±5 70±5 70±4 81±3 87±4 82±3

38±7 50±0 59±4 64±4 67±5 81±5 79±6 83±5

33±5 41±4 50±0 52±6 57±5 77±5 78±6 82±5

30±5 36±4 48±6 50±0 55±5 74±3 77±4 80±3

30±4 33±5 43±5 45±5 50±0 64±7 69±3 73±6

19±3 19±5 23±5 26±3 36±7 50±0 56±5 67±6

13±4 21±6 22±6 23±4 31±3 44±5 50±0 58±5

18±3 17±5 18±5 20±3 27±6 33±6 42±5 50±0

P(X>Y) - RGB

TD-JEPA

BYOL- *

BYOL*

RLDP

FB

HILP

ICVF*

Laplacian

Y

50±0 65±7 77±5 76±5 55±5 57±6 65±4 93±4

35±7 50±0 54±6 58±7 37±3 49±7 57±8 79±5

23±5 46±6 50±0 53±7 33±4 39±6 48±6 73±6

24±5 42±7 47±7 50±0 37±5 38±5 43±9 71±7

45±5 63±3 67±4 63±5 50±0 52±4 57±2 85±4

43±6 51±7 61±6 62±5 48±4 50±0 56±5 81±6

35±4 43±8 52±6 57±9 43±2 44±5 50±0 76±6

7±4 21±5 27±6 29±7 15±4 19±6 24±6 50±0

P(X>Y) - Proprioception

**Figure 2.** Probabilities of improvement: how lixely is method X to outperform method Y on a random domain? We report symmetrized 95% simple bootstrap confidence intervals. Dotted lines surround matches in which the improvement is statistically significant.

DMCRGB DMC OGBenchRGBOGBench 0.0

0.2

0.4

0.6

Normalized performance

BYOL* BYOL-γ* TD-JEPA

0.0 0.1 antmaze-ln cube-single antmaze-me puzzle-3x3 antmaze-mn quadruped cube-double cheetah antmaze-ms pointmass walker scene antmaze-ls

RGB

-0.1 0.0 0.1

Normalized performance difference

Proprioception

**Figure 3.** Left: normalized zero-shot performance for latent-predictive methods. Right: difference in normalized performance between TD-JEPA and its symmetric variant. Error bars represent standard errors on normalized performance or its differences, respectively.

5.2 Which dynamics should latent-predictive zero-shot algorithms model?

The baselines based on BYOL and BYOL-γ are algorithmically closest to TD-JEPA, and allow a precise investigation on the dynamics to model. While BYOL⋆and BYOL-γ⋆approximate one-step and multi-step transitions of the behavioral policy, respectively, TD-JEPA models multi-step transitions of the zero-shot policies. While approximating the behavioral dynamics can be effective for expert-like data (i.e., in OGBench), we observe a general pattern suggesting that directly modeling policy-conditional successor measures is on average beneficial, as reported in Fig. 3 (left).

5.3 Should state and task representations differ?

TD-JEPA trains separate state and task encoders: while this may grant a better approximation of successor measures, sharing state and task representations while optimizing a single objective (see Section 3.1) may in practice be more efficient. We measure the difference in per-task normalized performance between TD-JEPA and a symmetric variant in Figure 3 (right): we observe that this variant performs comparatively rather well, while relying on a single predictor-encoder pair. However, using distinct state and task embeddings tends to improve empirical performance more often than not.

<!-- Page 10 -->

0K 200K 400K

Steps

0.0

0.2

0.4

Normalized Performance walker

0K 200K 400K

Steps

0.00

0.25

0.50 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Offline

0K 200K 400K

Steps

0.00

0.25

0.50

Normalized Performance walker

0K 200K 400K

Steps

0.00

0.25

0.50 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Online

TD-JEPA TD-JEPA (frozen) FB FB (frozen) Scratch

**Figure 4.** Normalized performance of zero-shot policies when fine-tuned offline (top) or online (bottom). Initializing the agent to zero-shot solutions (blue and yellow lines) results in sample-efficient learning; frozen representations (dashed) are often expressive enough to enable fast adaptation.

5.4 Are state representations beneficial for fast adaptation?

While the previous evaluations have focused on aggregated zero-shot performance, we now investigate an additional benefit of explicit state representations: fast adaptation at test-time. Given a pixel-based task, we initialize the agent with the zero-shot policy πz and critic learned at pre-training, and we either fine-tune the whole model via TD3 (Fujimoto et al., 2018) or keep the pre-trained state encoder frozen. We consider two RL adaptation protocols (i) Offline: a transition-reward dataset is provided Drew = {(s, a, s′, r)} and TD3 updates are applied offline; (ii) Online: an online buffer is additionally collected over time and batches are sampled by mixing it with the offline buffer mentioned above (following the unsupervised-to-online protocol of Kim et al. (2024)). Figure 4 reports results for each DMC domain for the task in which the gap between online and zero-shot algorithms is largest; we consider TD-JEPA and FB as strong, representative algorithms among self-predictive and contrastive methods. We first observe that fine-tuning pre-trained agents leads to large gains in sample efficiency w.r.t. training from scratch, and reaches the asymptotic performance of TD3. More interestingly, frozen representations are often sufficient for downstream learning, and do not need further fine-tuning. We refer to App. D.3 and App. E.7 for further results and details, respectively.

## 6 Conclusion

Through the introduction of a novel temporal-difference latent-predictive loss, we presented a zero-shot unsupervised RL method that operates entirely in latent space and can be shown to recover a factorization of the successor measures of multiple policies. Empirically, we found that TD-JEPA matches the best zero-shot methods when learning from proprioception, and exceeds them when learning from pixels, while also retrieving state representations that allow fast downstream adaptation. As formal guarantees rely on an assumption of symmetry, one exciting direction for future work may study learning objectives that are compatible with asymmetric successor measures, yet remain amenable to practical optimization. On a practical note, we believe that benchmarking latent-predictive zero-shot objectives on large-scale, real robotic dataset can shed further light on opportunities and limitations of this promising framework.

<!-- Page 11 -->

## References

Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron C Courville, and Marc Bellemare. Deep reinforcement learning at the edge of the statistical precipice. NeurIPS, 2021.

Siddhant Agarwal, Harshit Sikchi, Peter Stone, and Amy Zhang. Proto successor measure: Representing the behavior space of an rl agent. ICML, 2025.

Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba, Komeili, Matthew Muckley, Ammar

Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, and Nicolas Ballas. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985, 2025.

André Barreto, Will Dabney, Rémi Munos, Jonathan J Hunt, Tom Schaul, Hado P van Hasselt, and David Silver.

Successor features for transfer in reinforcement learning. NeurIPS, 2017.

Chethan Bhateja, Derek Guo, Dibya Ghosh, Anikait Singh, Manan Tomar, Quan Vuong, Yevgen Chebotar, Sergey

Levine, and Aviral Kumar. Robotic offline rl from internet videos via value-function pre-training. arXiv preprint arXiv:2309.13041, 2023.

Léonard Blier, Corentin Tallec, and Yann Ollivier. Learning successor states and goal-dependent values: A mathematical viewpoint. arXiv preprint arXiv:2101.07123, 2021.

Maksim Bobrin, Ilya Zisman, Alexander Nikulin, Vladislav Kurenkov, and Dmitry Dylov. Zero-shot adaptation of behavioral foundation models to unseen dynamics. arXiv preprint arXiv:2505.13150, 2025.

Justin A Boyan. Least-squares temporal difference learning. ICML, 1999.

Lasse Espeholt, Hubert Soyer, Remi Munos, Karen Simonyan, Vlad Mnih, Tom Ward, Yotam Doron, Vlad Firoiu,

Tim Harley, Iain Dunning, et al. Impala: Scalable distributed deep-rl with importance weighted actor-learner architectures. ICML, 2018.

Scott Fujimoto, Herke Hoof, and David Meger. Addressing function approximation error in actor-critic methods.

ICML, 2018.

Scott Fujimoto, Pierluca D’Oro, Amy Zhang, Yuandong Tian, and Michael Rabbat. Towards general-purpose model-free reinforcement learning. ICLR, 2025.

Carles Gelada, Saurabh Kumar, Jacob Buckman, Ofir Nachum, and Marc G Bellemare. Deepmdp: Learning continuous latent space models for representation learning. ICML, 2019.

Dibya Ghosh, Chethan Anand Bhateja, and Sergey Levine. Reinforcement learning from passive data via latent intentions. ICML, 2023.

Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre Richemond, Elena Buchatskaya, Carl Doersch,

Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, et al. Bootstrap your own latent-a new approach to self-supervised learning. NeurIPS, 2020.

Zhaohan Guo, Shantanu Thakoor, Miruna Pîslar, Bernardo Avila Pires, Florent Altché, Corentin Tallec, Alaa Saade,

Daniele Calandriello, Jean-Bastien Grill, Yunhao Tang, et al. Byol-explore: Exploration by bootstrapped prediction. NeurIPS, 2022.

Zhaohan Daniel Guo, Bernardo Avila Pires, Bilal Piot, Jean-Bastien Grill, Florent Altché, Rémi Munos, and Moham- mad Gheshlaghi Azar. Bootstrap latent-predictive representations for multitask reinforcement learning. ICML, 2020.

Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. ICML, 2019.

Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. ICLR, 2020.

Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. ICLR,

2024.

<!-- Page 12 -->

Pranaya Jajoo, Harshit Sikchi, Siddhant Agarwal, Amy Zhang, Scott Niekum, and Martha White. Regularized latent dynamics prediction is a strong baseline for behavioral foundation models. Workshop on Reinforcement Learning Beyond Rewards @ RLC 2025, 2025.

Scott Jeen, Tom Bewley, and Jonathan Cullen. Zero-shot reinforcement learning from low quality data. NeurIPS, 2024.

Khimya Khetarpal, Zhaohan Daniel Guo, Bernardo Avila Pires, Yunhao Tang, Clare Lyle, Mark Rowland, Nicolas

Heess, Diana Borsa, Arthur Guez, and Will Dabney. A unifying framework for action-conditional self-predictive reinforcement learning. AISTATS, 2025.

Junsu Kim, Seohong Park, and Sergey Levine. Unsupervised-to-online reinforcement learning. arXiv preprint arXiv:2408.14785, 2024.

Diederik P Kingma. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.

Aviral Kumar, Aurick Zhou, George Tucker, and Sergey Levine. Conservative q-learning for offline reinforcement learning. NeurIPS, 2020.

Charline Le Lan, Stephen Tu, Mark Rowland, Anna Harutyunyan, Rishabh Agarwal, Marc G Bellemare, and Will

Dabney. Bootstrapped representations in reinforcement learning. arXiv preprint arXiv:2306.10171, 2023.

Daniel Lawson, Adriana Hugessen, Charlotte Cloutier, Glen Berseth, and Khimya Khetarpal. Self-predictive represen- tations for combinatorial generalization in behavioral cloning. arXiv preprint arXiv:2506.10137, 2025.

Yann LeCun. A path towards autonomous machine intelligence. Open Review, 2022.

Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip:

Towards universal visual reward and representation via value-implicit pre-training. ICLR, 2023.

Sridhar Mahadevan and Mauro Maggioni. Proto-value functions: A laplacian framework for learning representation and control in markov decision processes. JMLR, 2007.

Arjun Majumdar, Karmesh Yadav, Sergio Arnaud, Jason Ma, Claire Chen, Sneha Silwal, Aryan Jain, Vincent-Pierre

Berges, Tingfan Wu, Jay Vakil, et al. Where are we in the search for an artificial visual cortex for embodied intelligence? NeurIPS, 2023.

Robert McCarthy, Daniel CH Tan, Dominik Schmidt, Fernando Acero, Nathan Herr, Yilun Du, Thomas G Thuruthel, and Zhibin Li. Towards generalist robot learning from internet video: A survey. Journal of Artificial Intelligence Research, 83, 2025.

Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. CORL, 2022.

Simone Parisi, Aravind Rajeswaran, Senthil Purushwalkam, and Abhinav Gupta. The unsurprising effectiveness of pre-trained vision models for control. In international conference on machine learning, pages 17359–17371. PMLR, 2022.

Seohong Park, Tobias Kreiman, and Sergey Levine. Foundation policies with hilbert representations. ICML, 2024.

Seohong Park, Kevin Frans, Benjamin Eysenbach, and Sergey Levine. Ogbench: Benchmarking offline goal-conditioned

RL. ICLR, 2025a.

Seohong Park, Qiyang Li, and Sergey Levine. Flow q-learning. ICML, 2025b.

Matteo Pirotta, Andrea Tirinzoni, Ahmed Touati, Alessandro Lazaric, and Yann Ollivier. Fast imitation via behavior foundation models. ICLR, 2024.

Doina Precup, Richard S Sutton, and Sanjoy Dasgupta. Off-policy temporal-difference learning with function approximation. ICML, 2001.

Bruno Scherrer. Should one compute the temporal difference fix point or minimize the bellman residual? the unified oblique projection view. ICML, 2010.

Moritz Schneider, Robert Krug, Narunas Vaskevicius, Luigi Palmieri, and Joschka Boedecker. The surprising ineffectiveness of pre-trained visual representations for model-based reinforcement learning. Advances in Neural Information Processing Systems, 37:32916–32946, 2024.

Max Schwarzer, Ankesh Anand, Rishab Goel, R Devon Hjelm, Aaron Courville, and Philip Bachman. Data-efficient reinforcement learning with self-predictive representations. ICLR, 2021.

<!-- Page 13 -->

Harshit Sikchi, Andrea Tirinzoni, Ahmed Touati, Yingchen Xu, Anssi Kanervisto, Scott Niekum, Amy Zhang,

Alessandro Lazaric, and Matteo Pirotta. Fast adaptation with behavioral foundation models. RLC, 2025.

David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot,

Laurent Sifre, Dharshan Kumaran, Thore Graepel, et al. A general reinforcement learning algorithm that masters chess, shogi, and go through self-play. Science, 2018.

Sneha Silwal, Karmesh Yadav, Tingfan Wu, Jay Vakil, Arjun Majumdar, Sergio Arnaud, Claire Chen, Vincent-Pierre

Berges, Dhruv Batra, Aravind Rajeswaran, et al. What do we learn from a large-scale study of pre-trained visual representations in sim and real environments? In 2024 IEEE International Conference on Robotics and Automation (ICRA), pages 17515–17521. IEEE, 2024.

Vlad Sobal, Wancong Zhang, Kyunghyun Cho, Randall Balestriero, Tim GJ Rudner, and Yann LeCun. Learning from reward-free offline data: A case for planning with latent dynamics models. arXiv preprint arXiv:2502.14819, 2025.

Yunhao Tang, Zhaohan Daniel Guo, Pierre Harvey Richemond, Bernardo Avila Pires, Yash Chandak, Rémi Munos,

Mark Rowland, Mohammad Gheshlaghi Azar, Charline Le Lan, Clare Lyle, et al. Understanding self-predictive learning for reinforcement learning. ICML, 2023.

Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas

Abdolmaleki, Josh Merel, Andrew Lefrancq, et al. Deepmind control suite. arXiv preprint arXiv:1801.00690, 2018.

Andrea Tirinzoni, Ahmed Touati, Jesse Farebrother, Mateusz Guzek, Anssi Kanervisto, Yingchen Xu, Alessandro

Lazaric, and Matteo Pirotta. Zero-shot whole-body humanoid control via behavioral foundation models. ICLR, 2025.

Ahmed Touati and Yann Ollivier. Learning one representation to optimize all rewards. NeurIPS, 2021.

Ahmed Touati, Jérémy Rapin, and Yann Ollivier. Does zero-shot reinforcement learning exist? ICLR, 2023.

Nikolaos Tsagkas, Andreas Sochopoulos, Duolikun Danier, Sethu Vijayakumar, Chris Xiaoxuan Lu, and Oisin

Mac Aodha. When pre-trained visual representations fall short: Limitations in visuo-motor robot learning. arXiv preprint arXiv:2502.03270, 2025.

Núria Armengol Urpí, Marin Vlastelica, Georg Martius, and Stelian Coros. Epistemically-guided forward-backward exploration. RLC, 2025.

Claas Voelcker, Tyler Kastner, Igor Gilitschenski, and Amir-massoud Farahmand. When does self-prediction help?

understanding auxiliary tasks in reinforcement learning. RLC, 2024.

Manuel Watter, Jost Springenberg, Joschka Boedecker, and Martin Riedmiller. Embed to control: A locally linear latent dynamics model for control from raw images. NeurIPS, 2015.

Yifan Wu, George Tucker, and Ofir Nachum. The laplacian in rl: Learning representations with efficient approximations.

ICLR, 2019.

Denis Yarats, David Brandfonbrener, Hao Liu, Michael Laskin, Pieter Abbeel, Alessandro Lazaric, and Lerrel Pinto.

Don’t change the algorithm, change the data: Exploratory data for offline reinforcement learning. Generalizable Policy Learning in the Physical World Workshop @ ICLR 2022, 2022a.

Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. ICLR, 2022b.

Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning. arXiv preprint arXiv:2411.04983, 2024.

Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning. ICML, 2025.

<!-- Page 14 -->

## Appendix

A Extended Related Work 15

B Proofs 16

B.1 Proof of Proposition 1........................................ 16

B.2 Proof of Theorem 1.......................................... 17

B.3 Proof of Theorem 2.......................................... 18

B.4 Proof of Theorem 3.......................................... 18

B.5 Proof of Theorem 4.......................................... 20

C Theoretical Analysis under Relaxed Assumptions 20

C.1 Reduction from latent-predictive to density-based losses..................... 21

C.2 Generalizing existing results..................................... 22

C.3 TD-JEPA with forward-backward-in-time sampling........................ 22

D Additional Results 23

D.1 Explicit state encoders for zero-shot baselines........................... 23

D.2 Contrastive variant of symmetric TD-JEPA............................ 24

D.3 Additional fast adaptation results.................................. 24

D.4 Architectural ablations........................................ 27

D.5 Visualization of TD-JEPA representations............................. 27

D.6 Numerical results for performance difference plots......................... 28

E Implementation Details 28

E.1 Environments............................................. 28

E.2 Learning from pixels......................................... 28

E.3 Architectures............................................. 30

E.4 Training hyperparameters...................................... 30

E.5 Method-specific details........................................ 30

E.6 Offline correction........................................... 32

E.7 Evaluation: zero-shot and fast adaptation............................. 32

E.8 Pseudocode for TD-JEPA...................................... 33

<!-- Page 15 -->

A Extended Related Work

As TD-JEPA bridges zero-shot reinforcement learning and latent-predictive representation learning, we reserve this section to building connections to several related works in both areas beyond what was discussed in Sec. 1.

Zero-shot RL algorithms These methods aim at pre-training agents on unsupervised data to enable solving a wide range of downstream tasks specified via reward functions in a zero-shot fashion, i.e., without additional test-time learning or planning. So far they have achieved impressive results, yielding so-called behavioral foundation models (Pirotta et al., 2024; Tirinzoni et al., 2025). The forward-backward algorithm (FB, Touati and Ollivier (2021); Touati et al. (2023)) is an established method in this class, and perhaps the most related to TD-JEPA. FB learns a task encoder and estimates its successor features, essentially finding a bilinear decomposition of policy-conditional successor measures (e.g., M πz ≈FzBT). On the other hand, TD-JEPA uses the parameterization M πz ≈ϕTzψT, which thus explicitly trains shared (across tasks) state representations and enforces more structure in the predictor. On top of the difference in parameterization, FB adopts a contrastive loss, which computes pairwise dot products across each training batch. This is not necessary for the objective of TD-JEPA, which is latent-predictive at its core. FB has further been shown capable of zero-shot imitation (Pirotta et al., 2024) and extended to several settings, including online training regularized by expert data (Tirinzoni et al., 2025), offline training on low-quality data (Jeen et al., 2024), training on environments with different dynamics (Bobrin et al., 2025), online fine-tuning (Sikchi et al., 2025) and pure exploration (Urpí et al., 2025).

Other methods, like HILP, PSM, and RLDP, can also be seen as training a task encoder ψ plus successor features on top. HILP (Park et al., 2024) trains ψ through a “goal-reaching” loss that preserves temporal distance from true to latent state space. PSM (Agarwal et al., 2025) does so by learning an affine decomposition of the successor measure for a discrete codebook of policies. Finally, RLDP (Jajoo et al., 2025) trains ϕ using a chained multi-step latent-predictive loss similar to the one used by TD-MPC (Hansen et al., 2024). Jajoo et al. (2025) also observe that regularizing the representation to be orthonormal is crucial to avoid collapse and obtain good performance, which we also observe in TD-JEPA (see Alg. 1).

Latent-predictive methods As discussed in Section 1, these methods have mostly been applied to define auxiliary losses for a variety of RL settings. Schwarzer et al. (2021) use a latent-predictive loss to enhance state representations learned through a deep Q network. Guo et al. (2020) use latent prediction in the context of POMDPs to embed observations and histories. Their method trains two representations to be self-predictive of each other, hence connecting to the asymmetric variant of TD-JEPA and the method explained in Appendix C. Hansen et al. (2024) uses latent prediction to train a latent dynamics model that, combined with TD3, enables mixing model-free and model-based reinforcement learning, e.g., by test time planning to improve the pre-trained policy. Sobal et al. (2025), on the other hand, learn latent dynamics models on purely unsupervised data and show they can solve goal-reaching tasks via test-time planning.

BYOL-γ (Lawson et al., 2025) is a recent, closely related method for representation learning. At its core, BYOL-γ predicts discounted future representations of states visited by the behavior policy, while TD-JEPA extends this objective to policy-conditional prediction. As a result, BYOL-γ may be seen as an unconditional, Monte Carlo version of TD-JEPA, with a strict requirement in terms of on-policy data. On the other hand, the on-policy nature of the algorithm enables Lawson et al. (2025) to implement a bi-directional update of asymmetric representations. TD-JEPA can also recover an asymmetric parameterization, but its practical objective is not bi-directional (i.e., it only implements forward TD prediction, cf. Appendix C.3 for a formal definition of the bi-directional latent-predictive objective). Crucially, BYOL-γ is not proposed as a zero-shot method: the version evaluated in this work is a novel instantiation in a successor feature framework.

Theory of latent-predictive representations The theory of latent-predictive or self-predictive representations has been previously studied in several works (Tang et al., 2023; Voelcker et al., 2024; Khetarpal et al., 2025; Lawson et al., 2025), with a particular focus on single-policy, single-step prediction (potentially, bidirectional). Our analysis of MC-JEPA (Section 4) largely takes place in a multi-policy setting, with generic transition kernels over states; as such, it subsumes and expands on several existing results (see Appendix C.2). On the other hand, representation learning through temporal difference losses, as in TD-JEPA, is largely

<!-- Page 16 -->

understudied. The closest studies are by Blier et al. (2021) and Lan et al. (2023) which show that, under certain parameterizations and assumptions, TD representation learning can recover low-rank decompositions of the successor measure, in the sense that they optimize the corresponding approximation loss. These works crucially rely on having a single policy, and it remains an open questions whether such results extend to multiple policies. In this direction, we provide a first result which connects latent-predictive TD learning with TD learning over the successor measure for multiple polies.

Other representation learning methods for RL Beyond latent-predictive methods, ICVF (Ghosh et al., 2023; Bhateja et al., 2023) has also been proposed as a multi-policy, multi-step representation learning objective. By relying on an implicit, value-based loss, this method may be applied to off-policy, action-free, transition-based data to recover a decomposition of policy-dependent successor measures. This decomposition is multi-linear, but, unlike TD-JEPA, it is restricted to linear predictors; its practical implementation moreover forces the same dimensionality across state and task embeddings. As BYOL-γ, ICVF does not natively support zero-shot RL: we thus integrate it into a successor-features-based zero-shot policy optimization scheme.

VIP (Ma et al., 2023) also works in a similar setting as ICVF. It casts representation learning as an offline goal-conditioned reinforcement learning problem. This can be seen related to approximating the successor measure of several goal-reaching policies. On the other hand, TD-JEPA does so for all reward-maximing policies, hence encompassing the goal-reaching ones.

MR.Q (Fujimoto et al., 2025) learns model-based representations that approximately linearize value functions for reward-based RL. This is achieved by combining reward prediction with a single-step latent dynamics loss similar to the one of BYOL, yielding state encoders on top of which value functions and policies are trained. TD-JEPA also aims at linearizing value functions, but does so with a multi-step policy-dependent loss and, most importantly, in a reward-free manner.

More broadly, several recent works evaluate visual representations pre-trained from large-scale data (e.g., internet videos) in control problems (Parisi et al., 2022; Majumdar et al., 2023; Silwal et al., 2024; Schneider et al., 2024; Zhou et al., 2024; McCarthy et al., 2025; Tsagkas et al., 2025). While there is no “best” method overall, as performance are problem and data dependent (Majumdar et al., 2023), representations pre-trained or fine-tuned with RL-related objectives, like time and task awareness (Ma et al., 2023; Bhateja et al., 2023; Tsagkas et al., 2025), perform well in general. TD-JEPA aligns with this view, as it shows that visual representations pre-trained with multi-step and policy-dependent objectives are suitable for value estimation and optimization across multiple tasks.

B Proofs

B.1 Proof of Proposition 1

For any z, s, a, s+, the term inside the expectation in Eq. 5 can be rewritten as

∥Tϕ(ϕ(s), a, z) −ϕ(s+)∥2 = ∥Tϕ(ϕ(s), a, z) ± F πz ϕ (s, a) −ϕ(s+)∥2

= ∥Tϕ(ϕ(s), a, z) −F πz ϕ (s, a)∥2 + ∥F πz ϕ (s, a) −ϕ(s+)∥2

−(Tϕ(ϕ(s), a, z) −F πz ϕ (s, a))T(F πz ϕ (s, a) −ϕ(s+)).

Taking the expectation w.r.t. s+ ∼M πz(·|s, a), it is easy to see that the last term is zero since F πz ϕ (s, a):= Es+∼M πz (·|s,a)[ϕ(s+)], while the second term is a constant. This concludes the proof.

□

Remark 1. By replacing the target ϕ(s+) above with ψ(s+) and F πz ϕ (s, a) with F πz ψ (s, a), this proof generalizes to the Monte Carlo loss with asymmetric representations (Eq. 8).

<!-- Page 17 -->

B.2 Proof of Theorem 1

We begin by rewriting the MC-JEPA loss of Eq. 8 with the notation of Sec. 4 as

LMC-JEPA(ϕ, Tϕ,z, ψ):= 1

2Ez∼Z,s∼ρ,s+∼M πz (·|s)

T T ϕ,zϕ(s) −ψ(s+)

2

2

, (13)

where ρ denotes the state distribution. Proposition 1 implies that LMC-JEPA has the same gradients as

Lmc(ϕ, Tϕ,z, ψ):= 1

2Ez∼Z,s∼ρ

T T ϕ,zϕ(s) −Es+∼M πz (·|s)

ψ(s+)

2

2

.

Let Dρ ∈RS×S be a diagonal matrix containing ρ(s) for all states s ∈S on its diagonal. Using that Dρ = I by Assumption A2,6

Lmc(ϕ, Tz, ψ):= 1

2Ez∼Z h

∥D1/2 ρ (ϕTz −M πzψ)∥2

F i

= 1

2Ez∼Z

∥ϕTz −M πzψ∥2

F

. (14)

We now prove all statements for Lmc, as gradient equivalence with Eq. 13 implies they also hold for LMC-JEPA.

Statement 1 Let us first compute the optimal predictors. For any z ∈Z, the gradient of Lmc(ϕ, Tz, ψ) w.r.t. Tz is

∇TzLmc(ϕ, Tz, ψ) = p(z)ϕT(ϕTz −M πzψ) = p(z)(Tz −ϕTM πzψ), where p(z) is the probability to sample z7, while the second equality uses that ϕTϕ = I by Assumption A1. This yields T ⋆ ϕ,z = ϕTM πzψ. Moreover, by simply inverting the roles of ϕ and ψ, we find that ∇TzLmc(ψ, Tz, ϕ) = p(z)(Tz −ψTM πzϕ) and, thus, T ⋆ ψ,z = ψTM πzϕ.

The gradient of LSM(ϕ, Tz, ψ) w.r.t. Tz is

∇TzLSM(ϕ, Tz, ψ) = p(z)ϕT(ϕTzψT −M πz)ψ = p(z)(Tz −ϕTM πzψ), where we used again Assumption A1. Hence, T ⋆ z = ϕTM πzψ. Therefore, we clearly have that T ⋆ z = T ⋆ ϕ,z. Moreover, since P πz is symmetric by Assumption A3, M πz is symmetric too, and

T ⋆ ψ,z = (ϕT(M πz)Tψ)T = (ϕTM πzψ)T = (T ⋆ z)T.

Finally, it is easy to see that ϕT ⋆ ϕ,z and ψT ⋆ ψ,z satisfy the stated expressions for Πϕ:= ϕϕT and Πψ:= ψψT, respectively. Moreover, Πϕ and Πψ are symmetric and idempotent (ΠϕΠϕ = Πϕ), hence they are orthogonal projection matrices. This proves the first part of the statement.

Statement 2 Let us now fix any Tz for all z ∈Z and compute the gradients w.r.t. ϕ and ψ.

∇ϕLmc(ϕ, Tz, ψ) = Ez∼Z

(ϕTz −M πzψ)T T z

,

∇ψLmc(ψ, Tz, ϕ) = Ez∼Z

(ψTz −M πzϕ)T T z

,

∇ϕLSM(ϕ, Tz, ψ) = Ez∼Z

(ϕTzψT −M πz)ψT T z

= Ez∼Z

(ϕTz −M πzψ)T T z

,

∇ψLSM(ϕ, T T z, ψ) = Ez∼Z

(ψTzϕT −(M πz)T)ϕT T z

= Ez∼Z

(ψTz −(M πz)Tϕ)T T z

, where we used Assumption A1 to simplify the last two expressions. Given that P πz and, thus, M πz are symmetric by Assumption A3, these gradients match as stated.

□

6We ignore the 1/S scaling that only multiplies the loss by a constant. 7Without loss of generality, we also assume that p(z) > 0 for all z. If this is not the case, any z with p(z) = 0 can be removed from the loss.

<!-- Page 18 -->

B.3 Proof of Theorem 2

We begin by rewriting the TD-JEPA loss of Eq. 9 with the notation of Sec. 4 as

LTD-JEPA(ϕ, Tz, ψ):= 1

2Ez∼Z,s∼ρ,s+∼P πz (·|s)

T T ϕ,zϕ(s) −ψ(s+) −γT T ϕ,zϕ(s+)

2

2

. (15)

Following the proof of Theorem 1, we can put this in matrix form as

Ltd(ϕ, Tz, ψ):= 1

2Ez∼Z

D1/2 ρ (ϕTz −Uz)

2

F

, (16)

where Uz:= P πzψ −γP πzϕTz. As we only brought expectations inside the norm, Eq. 16 has the same gradients as Eq. 15. Hence, we define a continuous-time relaxation of gradient descend dynamics for Eq. 16 (equiv. Eq. 15) by the following ordinary differental equation (ODE) system:

    

   

Tϕ,z,t ∈arg minTz Ltd(ϕt, Tz, ψt) Tψ,z,t ∈arg minTz Ltd(ψt, Tz, ϕt)

˙ϕt = −∇ϕtLtd(ϕt, Tϕ,z,t, ψt)

˙ψt = −∇ψtLtd(ψt, Tψ,z,t, ϕt)

(17)

This implicitly assumes that predictors are optimized at a much faster rate than representations – an important property used in Theorem 1 of Tang et al. (2023) to show constant covariance and, thus, no collapse. We now prove this by following similar steps as in the proof of Tang et al. (2023), adapted to our setting. In particular, we prove it for the representations ϕ only. Given the symmetry of the losses, the same result can trivially be proven for ψ as well.

We need to prove that d dt(ϕT t ϕt) = 0. Since d dt(ϕT t ϕt) = (ϕT t ˙ϕt)T + ϕT t ˙ϕt, it is enough to show that ϕT t ˙ϕt = 0. Simple algebra yields

∇ϕLtd(ϕ, Tz, ψ) = Ez

Dρ (ϕTz −Uz) T T z

,

∇TzLtd(ϕ, Tz, ψ) = p(z)ϕTDρ (ϕTz −Uz).

Therefore, ϕT t ˙ϕt = −ϕT t ∇ϕtLtd(ϕt, Tϕ,z,t, ψt)

= −ϕT t Ez

Dρ (ϕtTϕ,z,t −Uz) T T ϕ,z,t

= −

X z∈Z p(z)ϕT t Dρ (ϕtTϕ,z,t −Uz) T T ϕ,z,t

= −

X z∈Z

∇Tϕ,z,tLtd(ϕt, Tϕ,z,t, ψt)T T ϕ,z,t

= 0, where the last equation holds since the gradient w.r.t. the predictor is zero at every step (first order optimality conditions from Eq. 17).

B.4 Proof of Theorem 3

We begin by rewriting the TD-JEPA loss of Eq. 9 with the notation of Sec. 4 as

LTD-JEPA(ϕ, Tz, ψ):= 1

2Ez∼Z,s∼ρ,s+∼P πz (·|s)

T T ϕ,zϕ(s) −ψ(s+) −γT T ϕ,zϕ(s+)

2

2

. (18)

Following the proof of Theorem 1, we can put this in matrix form as

Ltd(ϕ, Tz, ψ):= 1

2Ez∼Z

D1/2 ρ ϕTz −P πzψ −γP πzϕTz

2

F

. (19)

As we only brought expectations inside the norm, Eq. 19 has the same gradients as Eq. 18, so we can focus on it to prove the results. Moreover, we can set Dρ = I by Assumption A2.

<!-- Page 19 -->

Statement 1 We start by computing the gradients of Ltd and Lfw w.r.t. Tz. Up to a multiplicative constant p(z) (which doesn’t change the results), we have

∇TzLtd(ϕ, Tz, ψ) = ϕT (ϕTz −P πzψ −γP πzϕTz) = Tz −ϕTP πzψ −γϕTP πzϕTz, where we used Assumption A1 to set ϕTϕ = I. Further using that ψTψ = I,

∇TzLfw(ϕ, Tz, ψ) = ϕT(ϕTzψT −P πz −γP πzϕTzψT)ψ

= Tz −ϕTP πzψ −γϕTP πzϕTz = ∇TzLtd(ϕ, Tz, ψ).

Therefore, the gradients w.r.t. Tz of the two losses match, which means that the stationary points (i.e., optimal predictors) are also the same. Setting these gradients to zero we thus find that

T ⋆ ϕ,z = T ⋆ z,fw = (ϕT(I −γP πz)ϕ)−1ϕTP πzψ.

Note that matrix ϕT(I −γP πz)ϕ is positive definite and, thus, invertible. This is because I −γP πz is positive definite and ϕTϕ = I. Using that M πz = (I −γP πz)−1P πz, ϕT ⋆ ϕ,z = ϕT ⋆ z,fw = ϕ(ϕT(I −γP πz)ϕ)−1ϕT(I −γP πz) | {z } ˜Πϕ,z

M πzψ, where it is easy to verify that ˜Πϕ,z is idempotent (˜Πϕ,z ˜Πϕ,z = ˜Πϕ,z) but not necessarily symmetric, hence an oblique projection as stated.

For the other result in Statement 1, we proceed analogously by first showing that

∇TzLtd(ψ, Tz, ϕ) = Tz −ψTP πzϕ −γψTP πzψTz,

∇TzLbw(ϕ, Tz, ψ) = Tz −ψT(P πz)Tϕ −γψT(P πz)TψTz = ∇TzLtd(ψ, Tz, ϕ), where the last equality is true since P πz is symmetric. Then the result follows as before after equating the gradients to zero, solving for T ⋆ ψ,z, and expressing ψT ⋆ ψ,z as a function of ˜Πψ,z.

Statement 2 We show that the gradients w.r.t. ϕ and ψ match for any predictor Tz

∇ϕLtd(ϕ, Tz, ψ) = (ϕTz −P πzψ −γP πzϕTz) T T z,

∇ϕLfw(ϕ, Tz, ψ) = ϕTzψT −P πz −γP πzϕTzψT ψT T z = ∇ϕLtd(ϕ, Tz, ψ), where we used that ψTψ = I. Similarly,

∇ψLtd(ψ, Tz, ϕ) = (ψTz −P πzϕ −γP πzψTz) T T z,

∇ψLbw(ϕ, Tz, ψ) = ψTzϕT −(P πz)T −γ(P πz)TψTzϕT ϕT T z = ∇ψLtd(ψ, Tz, ϕ), where we used that ϕTϕ = I and (P πz)T = P πz. This proves the statement.

□

<!-- Page 20 -->

B.5 Proof of Theorem 4

Let us start from the first inequality. Defining V πz r ∈RS as a vector containing V πz r (s) for all states s ∈S, we can write the left-hand side for any r ∈RS as

Ez∈Z

"X s∈S

V πz r (s) −ϕ(s)TTzωr

2

#

= Ez∈Z∥V πz r −ϕTzωr∥2

2.

Since V πz r = M πzr and, by Assumption A1, ωr = ψTr,

Ez∈Z∥V πz r −ϕTzωr∥2

2 = Ez∈Z∥M πzr −ϕTzψTr∥2 2 ≤Ez∈Z∥M πz −ϕTzψT∥2

F ∥r∥2

2 = 2LSM(ϕ, Tz, ψ)∥r∥2

2.

The inequality is thus obtained by maximizing both sides over rewards with norm bounded by 1.

Let us now prove the bounds of LSM in terms of the Bellman errors Lfw and Lbw. Let us fix z ∈Z and recall that M πz admits both a “forward” Bellman equation, M πz = P πz + γP πzM πz, and a “backward” one, M πz = P πz + γM πzP πz (Blier et al., 2021). This implies that M πz = (I −γP πz)−1P πz = P πz(I −γP πz)−1. Then, for any matrix M ∈RS×S,

M −M πz = (I −γP πz)−1 ((I −γP πz)M −P πz) = (I −γP πz)−1 (M −P πz −γP πzM),

M −M πz = (M(I −γP πz) −P πz) (I −γP πz)−1 = (M −P πz −γMP πz) (I −γP πz)−1.

Using the first set of equalities with M = ϕTzψT, we can easily bound

LSM(ϕ, Tz, ψ) = 1

2Ez∼Z

∥ϕTzψT −M πz∥2

F

≤1

2Ez∼Z

∥(I −γP πz)−1∥2

2∥ϕTzψT −P πz −γP πzϕTzψT∥2 F

, where we used the inequality ∥XY ∥2

F ≤∥X∥2

2∥Y ∥2 F with ∥· ∥2

2 denoting the operator norm and ∥· ∥2 F the frobenius norm. Moreover,

∥(I −γP πz)−1∥2

2 = 1 (1 −γ)2 ∥(1 −γ)(I −γP πz)−1∥2

2 ≤ S (1 −γ)2, where the last inequality holds since (1 −γ)(I −γP πz)−1 is a stochastic matrix. Hence,

LSM(ϕ, Tz, ψ) ≤ S (1 −γ)2 Lfw(ϕ, Tz, ψ), which proves the first inequality with c = S (1−γ)2. The second one can be proved analogously.

□

C Theoretical Analysis under Relaxed Assumptions

This section describes how the main assumptions used in Section 4 can be removed, namely the uniform state distribution (A1), identity covariances (A2), and symmetric kernels P πz or M πz (A3). We shall derive similar results Th. 1 and Th. 3, but at the price of more complex proofs and notation. We do so through a novel “gradient matching” argument that reduces a general latent-predictive loss to density approximation. As we shall see, this encompasses not only MC-JEPA and TD-JEPA, but also existing methods (Tang et al., 2023; Khetarpal et al., 2025; Lawson et al., 2025).

<!-- Page 21 -->

C.1 Reduction from latent-predictive to density-based losses

Let Z be a finite set. For z ∈Z, let Ξz ∈RS×S be a generic kernel. For instance, Ξz may be the successor measure M πz or the one-step kernel P πz, but it is not important at this point. Using the same notation as Section 4 and Appendix B, consider the following density-based loss:

Ldens(ϕ, Tz, ψ): = 1

2Ez∼Z,s∼ρ,s+∼ρ

" ϕ(s)TTzψ(s+) −Ξz(s+|s)

ρ(s+)

2#

= 1

2Ez∼Z h

∥D1/2 ρ (ϕTzψT −ΞzD−1 ρ)D1/2 ρ ∥2

F i

. (20)

Minimizing this loss over representations ϕ, ψ and a collection of predictors {Tz}z∈Z is equivalent to finding the best multilinear approximation to the densities of the Ξz w.r.t. the state distribution ρ. Note that this is a well-defined loss (i.e., it does not involve stop-gradient operations) and the prediction targets ΞzD−1 ρ are not a function of the representations being learned. Our goal is to show that certain latent-predictive dynamics optimize this density-based loss.

For didactic purpose, let us consider two abstract latent-predictive losses Lϕ(ϕ, Tϕ,z, ψ) and Lψ(ψ, Tψ,z, ϕ). We shall specify what these are later. Lϕ(ϕ, Tϕ,z, ψ) is optimized over ϕ and Tϕ,z for all z, while Lψ(ψ, Tψ,z, ϕ)

is optimized over ψ and Tψ,z for all z. As common in the literature, we study a continuous-time relaxation of gradient descend dynamics by assuming that predictors are optimized at a much faster rate than representations – an important property to ensure that the latter ones do not collapse (Tang et al., 2023). This process can be described by the following ordinary differental equation (ODE) system:

    

   

Tϕ,z,t ∈arg minTz Lϕ(ϕt, Tz, ψt) Tψ,z,t ∈arg minTz Lψ(ψt, Tz, ϕt)

˙ϕt = −∇ϕtLϕ(ϕt, Tϕ,z,t, ψt)

˙ψt = −∇ψtLψ(ψt, Tψ,z,t, ϕt)

(21)

We now ask the question: how should Lϕ and Lψ be defined for the dynamics of Eq. 21 to optimize the density-based loss of Eq. 20? The following result provides and answer.

Theorem 5. Suppose that the gradients of Ldens, Lϕ, and Lψ match for all ϕ, ψ, Tz, i.e.,

1. ∇TzLdens(ϕ, Tz, ψ) = ∇TzLϕ(ϕ, Tz, ψ)

2. ∇TzLdens(ϕ, T T z, ψ) = ∇TzLψ(ψ, Tz, ϕ)

3. ∇ϕLdens(ϕ, Tz, ψ) = ∇ϕLϕ(ϕ, Tz, ψ)

4. ∇ψLdens(ϕ, T T z, ψ) = ∇ψLψ(ψ, Tz, ϕ)

Then, Ldens is a Lyapunov function for the ODE of Eq. 21.

Proof. Let Tz,t ∈arg minTz Ldens(ϕt, Tz, ψt) be the optimal predictor for the density-based loss given (ϕt, ψt) and define L(t):= Ldens(ϕt, Tz,t, ψt). We verify that a L(t), and thus Ldens, is a Lyapunov function for the ODE of Eq. 21. First note that Ldens is continuous and has continuous first derivates. By the chain rule, d dtL(t) = ∇ϕLdens(ϕt, Tz,t, ψt) · ˙ϕt + ∇ψLdens(ϕt, Tz,t, ψt) · ˙ψt, where the · operation is the dot product of the vectorized matrices. By Eq. 21, ˙ϕt = −∇ϕLϕ(ϕt, Tϕ,z,t, ψt) and ˙ψt = −∇ψLψ(ψt, Tψ,z,t, ϕt). Moreover, assumptions 1 and 2 directly yield Tϕ,z,t = Tz,t and Tψ,z,t = T T z,t. Plugging these into ˙ϕt and ˙ψt and using assumptions 3 and 4,

˙ϕt = −∇ϕLϕ(ϕt, Tz,t, ψt) = −∇ϕLdens(ϕt, Tz,t, ψt), ˙ψt = −∇ψLψ(ψt, T T z,t, ϕt) = −∇ψLdens(ϕt, Tz,t, ψt).

<!-- Page 22 -->

Thus, d dtL(t) = −∥∇ϕLdens(ϕt, Tz,t, ψt)∥2

F −∥∇ψLdens(ϕt, Tz,t, ψt)∥2

F ≤0,

Moreover, we clearly have d dtL(t) < 0 if (ϕt, ψt) is not a stationary point of the ODE, which proves the statement.

Therefore, if the gradients of Ldens, Lϕ, and Lψ match, the gradient dynamics of Eq. 21 monotonically improve the density-based loss over time. We remark that this does not imply convergence to the global minimum as Ldens is not convex. Th. 5 thus suggests a simple trick for designing the right latent-predictive dynamics to optimize a given density-based loss: just find Lϕ and Lψ whose gradients match those of Ldens. Latent predictive losses that satisfy this property are derived in the next result.

Proposition 2. Consider the following latent-predictive losses

Lϕ(ϕ, Tz, ψ):= 1

2Ez∼Z∥D1/2 ρ (ϕTz −ΞzψΣ−1 ψ)∥2

Σψ, (22)

Lψ(ψ, Tz, ϕ):= 1

2Ez∼Z∥D1/2 ρ (ψTz −Ξ∗zϕΣ−1 ϕ)∥2

Σϕ, (23)

where ∥X∥W = ∥XW 1/2∥F, Σϕ:= ϕTDρϕ, Σψ:= ψTDρψ, and Ξ∗ z:= D−1 ρ ΞT z Dρ is the ρ-adjoint of Ξz. Then, Lϕ and Lψ satisfy the gradient matching conditions for Ldens stated in Th. 5.

Proof. This can be directly obtained through simple linear algebra.

Note that, while the latent-predictive losses of Eq. 22 and 23 are expressed in expectation w.r.t. the kernels Ξz and Ξ∗ z, sample-based estimators for both are possible. In particular, while Eq. 22 involves sampling from the kernel Ξz, Eq. 23 involves a “backward” sampling operation given by the adjoint of Ξz.

C.2 Generalizing existing results

Through the right assumptions and choice of Ξz, Proposition 2 and Theorem 5 yield several existing results. First, with Ξz = M πz, we note that Eq. 22 and 23 are equivalent to MC-JEPA (cf. Eq. 8) with additional covariance weighting and a backward-in-time sampling in the loss for ψ. Assuming that Dρ = I (A1), Σϕ = Σψ = I (A2), and P πz is symmetric for all z (A3), this mismatch is resolved and we recover Th. 1 under its same assumptions. On the other hand, Proposition 2 and Theorem 5 show what happens when such assumptions are relaxed: if only A3 holds8, then Th. 1 still holds up to covariance transformations, while if A3 is further removed then MC-JEPA needs to be modified with backward sampling in the loss of ψ to guarantee optimization of the successor measure approximation loss.

Several analyses in related works, which all assume A1-A3, are also recovered by proper choice of Ξz. For instance, for a single policy π (i.e., |Z| = 1), we obtain Theorem 6 of Tang et al. (2023) by setting Ξz = P π and Theorem 4.1 of Lawson et al. (2025) by setting Ξz = M π. By letting Z correspond to the action space A, we recover Theorem 2 of Khetarpal et al. (2025) by setting Ξa = P π a for all actions a, with Pa the matrix containing P(s′|s, a) for all (s, s′).

C.3 TD-JEPA with forward-backward-in-time sampling

In the previous section, we have seen that MC-JEPA requires a backward-in-time sampling operation in the loss for ψ to provably optimize the successor measure approximation loss. In this section, we derive the TD dynamics corresponding to this process.

We thus start from Ldens, Lϕ, and Lψ with Ξz = M πz and replace the latter with the one-step kernel P πz plus the bootstrapped parameterization M πz ≃ϕTzψTDρ. For Ldens, similarly to Th. 3, we derive density-based

8To be precise, here we need the density MπzD−1 ρ to be symmetric, which implies that (Mπz)∗= Mπz.

<!-- Page 23 -->

forward and backward TD losses, respectively based on the application of the forward and backward Bellman operator. For the first one, we use that M πz = P πz + γP πzM πz ≃P πz + γP πzϕTzψTDρ and write

Lfw(ϕ, Tz, ψ):= 1

2Ez∼Z h

∥D1/2 ρ (ϕTzψT −P πzD−1 ρ −γP πzϕTzψT)D1/2 ρ ∥2

F i

. (24)

For the second one, we rewrite the backward Bellman equation in terms of the adjoint of M πz as

(M πz)∗= (P πz)∗+ γ(M πzP πz)∗

= (P πz)∗+ γD−1 ρ (P πz)T(M πz)TDρ

≃(P πz)∗+ γD−1 ρ (P πz)TDρψT T z ϕTDρ

= (P πz)∗+ γ(P πz)∗ψT T z ϕTDρ.

This yields

Lbw(ϕ, Tz, ψ):= 1

2Ez∼Z h

∥D1/2 ρ (ψTzϕT −(P πz)∗D−1 ρ −γ(P πz)∗ψTzϕT)D1/2 ρ ∥2

F i

. (25)

We then use the same bootstrapping for the latent-predictive losses of Eq. 22 and 23, thus obtaining

Lϕ(ϕ, Tz, ψ):= 1

2Ez∼Z∥D1/2 ρ (ϕTz −P πzψΣ−1 ψ −γP πzϕTz)∥2

Σψ, (26)

Lψ(ψ, Tz, ϕ):= 1

2Ez∼Z∥D1/2 ρ (ψTz −(P πz)∗ϕΣ−1 ϕ −γ(P πz)∗ψTz)∥2

Σϕ. (27)

As for MC-JEPA, this is the counterpart of TD-JEPA with additional covariance weighting and backwardin-time sampling in the loss of ψ. Through simple algebra, it is not difficult to check that Lϕ and Lψ have matching gradients (as in Th. 5) w.r.t. Lfw and Lbw, respectively. This implies that Th. 3 holds for this modified algorithm without assumptions A1-A3.

Unfortunately, differently from the original TD-JEPA, this variant is not easy to be optimized off-policy. In fact, while for Eq. 26 we can simply replace the on-policy kernel P πz with P(s′|s, a) and condition the predictor on actions, the same trick cannot be used for the adjoint (P πz)∗in Eq. 27. This is because there is no action-conditioned backward Bellman equation. We leave the study of practical learning dynamics for this theoretically sound variant of TD-JEPA for future work.

D Additional Results

This section reports additional experiments, as well as detailed numerical results for plots in the main part of the paper.

D.1 Explicit state encoders for zero-shot baselines

As mentioned in Section 5, existing zero-shot methods do not necessarily learn explicit state embeddings Wu et al. (2019); Touati and Ollivier (2021); Park et al. (2024). Nevertheless, we find that introducing a state encoder tends to improve average zero-shot performance, even in the absence of a specific representation learning objective. We consider three established zero-shot baselines (Laplacian (Wu et al., 2019), FB (Touati and Ollivier, 2021) and HILP (Park et al., 2025a)), and compare their performance without an explicit state encoder (i.e., successor features are trained on raw states), to those attained when introducing a state encoder (either shallow or deep). Note that, in this case, the state encoder is trained through gradient flowing from the original loss, and is not coupled to an ad-hoc objective. Results are summarized in Tab. 2, which only considers proprioceptive domains as a state encoder is necessary when learning from pixels. We observe that, while having an explicit state encoder may be detrimental in few specific domains, it remains beneficial on average, and crucial to obtain better performance in some domains. The optimal depth of the encoder is however domain-specific: OGBench domains generally prefer a deeper encoder, while DMC domains can be solved with a shallow encoder, or no explicit encoder at all. In order to maximize performance of the baselines, we thus evaluate them coupled with a deep encoder in OGBench, and with a shallow one in DMC (e.g., in Tab. 1). We additionally summarize performance differences induced by this choice of encoders in Fig. 5 (left).

<!-- Page 24 -->

FB FBshallow FBdeep HILP HILPshallow HILPdeep Laplacian Laplacianshallow Laplaciandeep

DMC (avg) 648.9 ± 7.5 648.2 ± 4.1 632.0 ± 4.4 659.4 ± 4.1 620.1 ± 8.4 603.2 ± 5.8 585.6 ± 8.9 591.1 ± 10.7 598.8 ± 7.5 walker 788.7 ± 4.3 811.5 ± 5.9 812.4 ± 12.9 783.6 ± 8.4 796.4 ± 7.7 785.0 ± 9.1 754.6 ± 16.7 769.7 ± 4.7 762.1 ± 7.8 cheetah 662.8 ± 5.7 672.7 ± 4.9 635.7 ± 22.3 635.2 ± 9.4 618.3 ± 5.8 612.3 ± 12.2 640.5 ± 9.1 614.5 ± 18.9 630.7 ± 17.9 quadruped 574.1 ± 11.3 595.6 ± 9.1 590.6 ± 10.6 695.8 ± 13.5 694.8 ± 11.0 681.1 ± 16.2 590.6 ± 31.0 635.0 ± 38.7 651.5 ± 12.7 pointmass 570.0 ± 22.6 513.0 ± 20.0 489.3 ± 14.8 522.8 ± 18.9 371.0 ± 37.1 334.5 ± 27.9 356.7 ± 24.0 345.1 ± 22.4 351.0 ± 28.5

OGBench (avg) 19.07 ± 0.65 21.96 ± 0.81 39.04 ± 0.66 30.51 ± 1.20 35.02 ± 0.92 37.98 ± 1.11 9.07 ± 0.71 9.29 ± 0.59 14.81 ± 1.32 antmaze-mn 45.20 ± 2.05 49.00 ± 2.13 73.00 ± 2.72 62.20 ± 2.39 60.22 ± 2.57 83.60 ± 2.63 17.00 ± 2.72 25.80 ± 3.48 50.00 ± 4.94 antmaze-ln 19.80 ± 2.62 15.60 ± 2.54 36.80 ± 4.28 34.00 ± 2.86 27.40 ± 4.00 52.60 ± 3.86 13.60 ± 2.68 10.60 ± 2.46 21.60 ± 3.90 antmaze-ms 20.60 ± 5.38 32.40 ± 3.18 70.40 ± 3.95 12.00 ± 3.88 43.60 ± 5.12 50.60 ± 2.46 14.20 ± 3.24 12.60 ± 3.31 21.40 ± 4.32 antmaze-ls 8.00 ± 2.65 15.80 ± 1.05 49.80 ± 5.64 4.20 ± 2.05 11.20 ± 1.04 12.20 ± 1.75 4.44 ± 2.30 4.00 ± 1.58 11.80 ± 1.47 antmaze-me 23.00 ± 3.20 25.80 ± 1.65 51.60 ± 2.65 6.67 ± 2.16 8.60 ± 1.33 2.00 ± 0.84 0.40 ± 0.40 1.00 ± 0.68 0.80 ± 0.61 cube-single 21.00 ± 2.52 26.80 ± 2.62 49.60 ± 3.83 84.00 ± 2.76 88.00 ± 2.49 74.20 ± 3.53 19.20 ± 2.11 18.20 ± 2.14 15.11 ± 1.49 cube-double 4.20 ± 0.96 4.00 ± 0.79 2.60 ± 0.43 27.11 ± 3.02 29.20 ± 2.83 20.00 ± 2.72 2.80 ± 0.53 3.40 ± 0.85 2.00 ± 0.42 scene 23.80 ± 2.28 22.00 ± 2.29 12.80 ± 1.61 42.20 ± 1.75 45.00 ± 2.88 43.80 ± 1.90 7.80 ± 1.31 5.80 ± 0.96 7.80 ± 1.28 puzzle-3x3 6.00 ± 0.84 6.22 ± 0.97 4.80 ± 0.68 2.20 ± 0.55 2.00 ± 0.52 2.80 ± 0.68 2.20 ± 0.63 2.20 ± 0.63 2.80 ± 0.68

**Table 2.** Ablation over encoder depth on proprioceptive DMC and OGBench domains for zero-shot baselines. Each method is evaluated in three variants: a baseline without explicit state encoder, one with a shallow (i.e., linear) state encoder, one with a deep one (2 or 4 hidden layers for DMC and OGBench, respectively, see Tab. 4.) We report mean performance and standard error. Results for each variant are bold if their confidence intervals overlap with the best variant of the same method.

## Algorithm

2 Symmetric TD-JEPA for zero-shot RL (latent-predictive and contrastive variants)

Inputs: Dataset D, batch size B, regularization coefficient λ, networks π, Tϕ, ϕ Initialize target networks: T − ϕ ←Tϕ, ϕ−←ϕ while not converged do

▷Sample training batch {(si, ai, s′ i)}B i=1 ∼D, {zi}B i=1 ∼Z, {a′ i}B i=1 ∼{π(ϕ−(s′ i), zi)}B i=1

▷Compute latent-predictive/contrastive loss b L(ϕ, Tϕ) = 1 2B P i

Tϕ(ϕ(si), ai, zi) −ϕ−(s′ i) −γT − ϕ (ϕ−(s′ i), a′ i, zi)

2 b L(ϕ, Tϕ) = 1 2B(B−1) P i̸=j

Tϕ(ϕ(si), ai, zi)⊤ϕ(s′ j) −γTϕ(ϕ(s′ i), a′ i, zi)⊤ϕ(s′ j)

2

−1

B

P i Tϕ(ϕ(si), ai, zi)⊤ϕ(s′ i)

▷Compute orthonormality regularization loss b LREG(ϕ) = 1 2B(B−1) P i̸=j(ϕ(si)⊤ϕ(sj))2 −1

B

P i ϕ(si)⊤ϕ(si)

▷Compute actor loss {ˆai}B i=1 ∼{π(ϕ(si), zi)}B i=1 b Lactor(π) = −1

B

PB i=1 Tϕ(ϕ(si), ˆai, zi)Tzi

Update ϕ, Tϕ to minimize b L(ϕ, T ϕ) + λ b LREG(ϕ) Update π to minimize b Lactor(π) Update target networks ϕ−, T − ϕ via EMA of ϕ, Tϕ

D.2 Contrastive variant of symmetric TD-JEPA

In order to further isolate the effect of different objectives on zero-shot performance, we instantiate the symmetric variant of TD-JEPA described by Eq. 7, where a single representation is used both as state and task encoder, as well as its contrastive counterpart, which uses an objective similar to that in Touati and Ollivier (2021). These algorithms are described in Alg. 2, where blue and yellow lines are exclusive to the latent-predictive and contrastive variants, respectively. Intuitively, the contrastive variant can be seen as a specific, symmetric instantiation of FB (Touati and Ollivier, 2021), and the comparison to the symmetric variant parallels that between TD-JEPA and FB. We report performance differences between the symmetric variant of TD-JEPA and the symmetric-contrastive variant in Fig. 5 (right). Similarly to results from Fig. 2, we observe that gaps in performance between self-predictive and contrastive methods grow larger when learning directly from pixels. For a numerical comparison, see Tab. 3.

D.3 Additional fast adaptation results

We extend the empirical evaluation on fast adaptation in Section 5 through Fig. 6. In the top part, we repeat the evaluation of Fig. 4, while only initializing encoders to pre-trained weights. The remaining components

<!-- Page 25 -->

0.0 0.2 pointmass cube-double scene cheetah puzzle-3x3 walker quadruped cube-single antmaze-me antmaze-ln antmaze-ls antmaze-mn antmaze-ms

Laplacian

-0.2 0.0 0.2

Normalized performance difference

HILP

0.0 0.5

FB

0.0 0.2 antmaze-me cube-double puzzle-3x3 antmaze-mn pointmass scene cube-single antmaze-ln antmaze-ls cheetah quadruped antmaze-ms walker

RGB

0.0 0.2

Normalized performance difference

Proprioception

**Figure 5.** Difference in normalized performance between zero-shot baselines with and without an explicit encoder (left); normalized performance difference between symmetric TD-JEPA and its contrastive variant (right). Error bars

represent standard errors on normalized performance differences.

of actor and critic need to be learned from scratch. These experiments thus recall the standard setting in which pre-trained visual representations are evaluated (Nair et al., 2022; Ma et al., 2023; Majumdar et al., 2023). We observe that, while initial performance is near-zero for all methods, pre-trained representations maintain their effectiveness in terms of sample efficiency. In the middle row, we again repeat the evaluation from Fig. 4, but only freeze convolutional weights for the variants represented by a dashed line. We observe that this causes the performance gap to full fine-tuning to shrink significantly, suggesting that convolutional filters extract suitable representations for both TD-JEPA and FB. Finally, we extend our empirical evaluation to OGBench in the bottom part of Figure 6, in which we present results for the most challenging tasks in three representative domains. This evaluation differs from the previous ones, as we found it to require strong BC regularization, even during fine-tuning. We confirm that pre-trained representations remain beneficial in terms of sample efficient adaptation. Interestingly, we find that frozen representations pre-trained may outperform full fine-tuning in antmaze-ls, while they remained a bottleneck in DMC.

<!-- Page 26 -->

0K 200K 400K

Steps

0.0

0.2

0.4

Normalized Performance walker

0K 200K 400K

Steps

0.0

0.2

0.4 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Offline

0K 200K 400K

Steps

0.00

0.25

0.50

Normalized Performance walker

0K 200K 400K

Steps

0.00

0.25

0.50 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Online

0K 200K 400K

Steps

0.0

0.2

0.4

Normalized Performance walker

0K 200K 400K

Steps

0.00

0.25

0.50 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Offline

0K 200K 400K

Steps

0.00

0.25

0.50

Normalized Performance walker

0K 200K 400K

Steps

0.00

0.25

0.50 cheetah

0K 200K 400K

Steps

0.0

0.2

0.4 quadruped

0K 200K 400K

Steps

0.0

0.5 pointmass

Online

0K 200K 400K

Steps

0.0

0.5

Normalized Performance antmaze-ln

0K 200K 400K

Steps

0.0

0.2

0.4 antmaze-ls

0K 200K 400K

Steps

0.0

0.5 cube-single

Offline

0K 200K 400K

Steps

0.0

0.5

Normalized Performance antmaze-ln

0K 200K 400K

Steps

0.0

0.2

0.4 antmaze-ls

0K 200K 400K

Steps

0.00

0.25

0.50 cube-single

Online

TD-JEPA TD-JEPA (frozen) FB FB (frozen) Scratch

**Figure 6.** Additional fast adaptation results, obtained when only loading encoder’s weights (top), when only freezing convolutional layers (middle) and in OGBench (bottom).

<!-- Page 27 -->

0 1 2 4

0

1

2

4

State encoder depth

4±2 16±4 17±5 19±5

2±1 18±5 22±4 30±5

3±1 25±7 32±4 27±3

2±1 44±5 38±9 38±10

Predictor depth: 1

0 1 2 4

0

1

2

4

0±0 21±2 15±4 18±3

1±0 24±3 17±4 20±2

3±1 26±5 22±7 22±4

0±0 37±6 32±5 32±11

Predictor depth: 2

0 1 2 4

0

1

2

4

4±2 26±5 11±3 18±4

2±1 26±5 12±3 17±2

1±1 32±3 10±3 21±2

4±1 46±3 22±3 30±3

Predictor depth: 4 antmaze-ln

0 1 2 4

Task encoder depth

0

1

2

4

State encoder depth

0±0 14±3 2±1 7±2

1±0 14±0 6±2 18±4

0±0 12±3 20±3 24±2

0±0 16±3 26±3 31±5

0 1 2 4

Task encoder depth

0

1

2

4

1±1 12±2 6±2 11±3

0±0 11±3 8±3 15±5

0±0 18±1 15±2 24±4

0±0 16±2 18±3 29±2

0 1 2 4

Task encoder depth

0

1

2

4

0±0 13±5 3±2 14±2

0±0 14±2 8±3 16±4

0±0 17±0 12±3 22±1

0±0 18±2 15±1 24±3 antmaze-ls

**Figure 7.** Zero-shot performance of TD-JEPA in antmaze-ln (top) and antmaze-ls (bottom) as the number of hidden layers in the encoders and predictors varies (from 0 to 4 and from 1 to 4, respectively).

D.4 Architectural ablations

Architectural choices are often crucial for self-predictive learning, and capacity is usually carefully distributed between encoder and predictor (Guo et al., 2022). This section ablates the width of the three main components in TD-JEPA in a controlled setting, namely in two visual OGBench tasks (antmaze-ln and antmaze-ls), which were chosen due to their complexity, and the fact that they often reward different approaches (see Tab. 1). We measure zero-shot performance as widths change in Fig. 7. In general, we observe that the state encoder (on the y axis) should be as deep as possible (although this trend is not present in DMC, see Table 2). Instead, the task encoder (on the x axis) should only be as deep as needed: at least 1 layer in antmaze-ln and closer to 4 for antmaze-ls. Finally, we observe that the predictor may be shallow, as long as the encoders have sufficient capacity. This result matches the general conjecture that latent-predictive representations should capture the key aspects of the input, to the extent that a prediction problem, e.g. predicting successor features, may be solved with limited capacity.

D.5 Visualization of TD-JEPA representations

Given a state-action pair (s, a) and a further state g, one may easily evaluate the successor measure in g of the policy that tries to reach g from s: for instance, in the case of TD-JEPA, M πϕ(g)(g | s, a) ≈T ϕ(ϕ(s), a, zg)⊤ψ(g), where zg = Es∼Drwd[ψ(s)ψ(s)T]−1ψ(g). Intuitively, this is connected to how quickly the policy may reach the goal, and should reflect the dynamics of the MDP. As often done in the literature (Lawson et al., 2025), we consider the methods evaluated in Tab. 1 and visualize these estimates for visual antmaze-ln in Fig. 8, highlighting how representations reflect temporal distances in the environment. While all plots reveal a similar pattern (which is not surprising as successor features are temporally-consistent representations by definition), some methods show inconsistent temporal distances. For instance, BYOL, RLDP, and HILP have latents of few states far from the goal with higher similarity to the latter than closer states. This is a sign of poor performance, as the predictor would be optimistic in predicting the number of steps to reach those goals.

<!-- Page 28 -->

**Figure 8.** Cosine similarities between successor features and features (e.g., ⟨T ϕ(ϕ(·), a, zg), ψ(g)⟩for TD-JEPA) projected over xy position of the agent’s center of mass. The red star marks g. Similarities reflect shortest-path distances in the MDP.

D.6 Numerical results for performance difference plots

We supplement the performance difference plot in Fig. 3 (right) and Fig. 5 (right) with Tab. 3, detailing numerical results.

E Implementation Details

We organize the discussion of implementation details in several subsections.

E.1 Environments

Zero-shot results in Section 5 consider the standard Deepmind Control Suite (DMC, Tassa et al. (2018)) evaluation over four domains from (Touati et al., 2023): walker, cheetah, quadruped and maze. The first three define several locomotion tasks (e.g. walk, run, flip), while the latter evaluates both goal- and rewardbased tasks. We additionally extend the zero-shot evaluation to the more recent OGBench suite (Park et al., 2024), which focuses exclusively on goal reaching. For computational reasons, we consider nine representative domains. We thus evaluate navigation across five antmaze datasets (medium-{navigate, stitch, explore} and large-{navigate, stitch}) 9, and manipulation through cube-{single, double}, scene and puzzle-3x3. In each domain we consider the five default tasks; for consistency with DMC, we carry out zero-shot evaluation through the standard reward inference procedure, and thus define each task through its reward function. During inference, we shift each reward by +1, which we found to significantly improve zero-shot performance.

E.2 Learning from pixels

In visual experiments, environment return states as 64×64 RGB images. In order to alleviate non-Markovianity, states are composed by stacking 3 frames. Each image is scaled to [−0.5, 0.5] and undergoes random shifts with a maximum intensity of 2 pixels, which is slightly milder than common strategies (Yarats et al., 2022b). The images are passed through convolutional encoders before being processed by further networks. Namely, we instantiate two convolutional encoders: one for the state encoder, and one for the task encoder (except for the symmetric variant of TD-JEPA, which only uses one). We however found that using a single, shared convolutional encoder does not significantly impact performance, and do not exclude that further specialization of the encoder might improve it. Each convolutional encoder uses the DrQ-v2 architecture introduced in Yarats et al. (2022b); we briefly experimented with IMPALA- (Espeholt et al., 2018) and Dreamer-like (Hafner et al., 2020) architectures, and we found them to achieve similar results when well-tuned.

9For compactness, we use mn, ms, me, ln, ln as dataset abbreviations, respectively.

![Figure extracted from page 28](2026-ICLR-td-jepa-latent-predictive-representations-for-zero-shot-reinforcement-learning/page-028-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 29 -->

C-TD-JEPAsym TD-JEPAsym TD-JEPA

DMCRGB (avg) 437.2 ± 9.8 598.1 ± 5.9 628.8 ± 5.5 walker 413.2 ± 16.1 685.9 ± 14.8 738.9 ± 3.5 cheetah 517.9 ± 31.3 688.0 ± 7.2 706.0 ± 4.1 quadruped 428.3 ± 21.6 606.7 ± 20.1 626.7 ± 13.6 pointmass 389.5 ± 17.2 411.6 ± 13.9 443.7 ± 10.9

DMC (avg) 586.3 ± 14.6 657.5 ± 3.6 661.2 ± 6.3 walker 757.8 ± 12.4 800.7 ± 4.7 785.2 ± 6.7 cheetah 583.3 ± 23.3 618.1 ± 11.3 688.7 ± 6.7 quadruped 565.5 ± 14.4 731.7 ± 17.3 691.4 ± 5.0 pointmass 438.8 ± 24.5 479.6 ± 11.1 479.3 ± 23.6

OGBenchRGB (avg) 33.93 ± 0.67 39.74 ± 0.64 41.34 ± 0.45 antmaze-mn 93.80 ± 1.05 95.80 ± 1.09 96.67 ± 1.11 antmaze-ln 68.00 ± 3.46 77.80 ± 4.22 74.60 ± 3.35 antmaze-ms 61.20 ± 3.00 82.20 ± 1.80 84.40 ± 3.85 antmaze-ls 8.80 ± 0.90 20.60 ± 1.03 28.80 ± 2.50 antmaze-me 1.40 ± 0.52 0.60 ± 0.31 0.20 ± 0.20 cube-single 64.00 ± 5.70 69.00 ± 2.62 67.80 ± 3.67 cube-double 2.00 ± 0.67 1.40 ± 0.60 3.00 ± 0.91 scene 4.00 ± 0.79 8.00 ± 1.94 14.20 ± 2.22 puzzle-3x3 2.20 ± 0.76 2.22 ± 0.78 2.40 ± 0.83

OGBench (avg) 35.58 ± 0.97 35.20 ± 0.49 37.98 ± 0.77 antmaze-mn 82.20 ± 2.87 76.40 ± 2.65 70.40 ± 3.72 antmaze-ln 57.20 ± 4.47 43.60 ± 2.44 57.20 ± 4.25 antmaze-ms 74.00 ± 2.27 62.80 ± 3.59 61.56 ± 4.53 antmaze-ls 43.20 ± 3.16 41.40 ± 3.82 40.60 ± 2.51 antmaze-me 21.80 ± 3.30 17.00 ± 2.65 20.20 ± 2.39 cube-single 16.80 ± 2.15 20.00 ± 2.17 34.20 ± 2.88 cube-double 3.60 ± 1.07 2.40 ± 0.78 3.60 ± 0.78 scene 16.80 ± 1.31 39.40 ± 2.17 38.44 ± 1.37 puzzle-3x3 4.60 ± 1.19 13.80 ± 1.47 15.60 ± 1.11

**Table 3.** Performance of TD-JEPA and symmetric variants (contrastive and latent-predictive) in DMC (returns) and OGBench (success rate) with either proprioception or RGB inputs. We report means and standard errors across seeds. Numbers are bold for top algorithms if confidence intervals overlap.

Input Embedding

LayerNorm + TanH

Linear + ReLU

Linear

Convolutional Encoder

Flatten

Conv + ReLU x4

Linear

Predictor

Linear + ReLU

Input Emb Input Emb

Linear

Actor

Linear + ReLU

Input Emb Input Emb Convolutional Encoder

Linear State Encoder

Linear + Norm

LayerNorm + TanH

Convolutional Encoder

Task Encoder

Linear + ReLU

Linear

Linear + Norm

**Figure 9.** Overview of the architectures used by TD-JEPA in DMCRGB. We refer to Tab. 4 for the different instantiations in other domains.

<!-- Page 30 -->

DMCRGB DMC OGBenchRGB OGBench

SFs: Tϕ, Tψ, F - hidden layers 3 3 4 4 SFs: Tϕ, Tψ, F - hidden width 512 512 State Encoder: ϕ - hidden layers 0 0 0 4 State Encoder: ϕ - hidden width 256 256 512 512 State Encoder: ϕ - output dimension dϕ 256 256 256 256 Task Encoder: ψ - hidden layers 2 2 4 4 Task Encoder: ψ - hidden witdh 256 256 512 512 Task Encoder: ψ - output dimension dψ 50 50 50 50 Actor: π - hidden layers 3 3 4 4 Actor: π - hidden witdh 256 256 512 512

Discount factor γ 0.98 0.98 0.99 0.99 Total gradient steps 2M 2M 1M 1M Batch size B 512 256 256 Default learning rate 10−4 10−4 10−4 10−4

Default regularization coefficient λ 1.0 1.0 1.0 1.0 EMA coefficient 0.001 0.001 0.005 0.005 pgoal 0.5 0.5 0.5 0.5

**Table 4.** Architectural (top) and training (bottom) hyperparameters.

E.3 Architectures

All algorithms rely on three types of networks, each of which is instantiated to the standard architectures from (Touati et al., 2023): (i) successor feature estimators, predictors and F-networks are MLPs with two layer-normalized embedding layers, (ii) state/task encoders and B-networks are standard MLPs with L2-normalized output and (iii) actor networks are Gaussian MLPs with a similar architecture to predictors, and fixed standard deviation of 0.2. All networks use ReLU activations, except for embedding layers, which use TanH. The number and width of layers in DMC closely follow those described in Touati et al. (2023), while we utilize deeper, narrower networks in OGBench, in order to better align with the implementation of benchmarked methods in Park et al. (2025a). An overview of the architectures used for TD-JEPA in DMCRGB is depicted in Fig. 9; further architectural hyperparameters describing depth and width of these networks are reported in the first half of Table 4. We remark that the state encoder’s depth in proprioception was found to be quite impactful, and was tuned according to baseline performance, as shown in Table 2.

E.4 Training hyperparameters

The second part of Table 4 describes hyperparameters used for training, and is complemented by the following discussion of further details. We again closely follow the default hyperparameters from Touati et al. (2023) and Park et al. (2025a) whenever possible; the batch size is reduced in visual domains to meet computational limitations. All networks are optimized through Adam (Kingma, 2014). TD-targets and value estimates for SVG-like policy updates are computed as the mean of twin networks; latents z ∈Z are representations of random uniform states from the dataset ψ(s) with probability pgoal, and are sampled from the hypersphere (i.e., Z) otherwise (Touati et al., 2023).

E.5 Method-specific details

The baselines’ implementation closely follows the public codebases, when available.

Our implementation of FB builds upon the one released in Tirinzoni et al. (2025), which is in turn aligned with the code released by Touati et al. (2023).

As described in Jajoo et al. (2025), RLDP is implemented in the same framework, but the latent dynamics model and the task encoder are trained in parallel with the remaining components; gradients from the contrastive FB objective are not backpropagated through the task encoder. As in the original work, we found that multi-step

<!-- Page 31 -->

prediction results in better performance, and we similarly adopt a prediction horizon of H = 5. Given a batch of trajectories {(si

0, ai 0,..., si H)}B−1 i=0, a task encoder ψ and latent predictor TRLDP: Rdψ × A →Rdψ, the loss for training task representations is thus:

bLRLDP(TRLDP, ψ) = 1 2B

B−1 X i=0

H−1 X t=0 hi t −ψ−(si t)

2, (28)

where hi

0 = ψ(si 0), hi t = TRLDP(hi t−1, ai t−1), and ψ−is a target network. The latent predictor is instantiated with the hyperparameters presented for the SFs architecture described in Tab. 4.

Laplacian (Mahadevan and Maggioni, 2007), HILP (Park et al., 2024), BYOL⋆(Grill et al., 2020), BYOL-γ⋆

(Lawson et al., 2025) and ICVF⋆(Ghosh et al., 2023) are all implemented in a successor-feature framework:

the losses proposed in the original publications are optimized to retrieve a task encoder ψ. Considering a batch of transitions {(si, ai, s′ i)}B−1 i=0, the feature learning objectives for Laplacian, BYOL⋆and BYOL-γ⋆are, respectively:

bLLaplacian(ψ) = 1 2B

B−1 X i=0

∥ψ(si) −ψ(s′ i)∥2, (29)

bLBYOL(TBYOL, ψ) = 1 2B

B−1 X i=0

TBYOL(ψ(si), a) −ψ−(s′ i)

2, (30)

bLBYOL−γ(TBYOL, ψ) = 1 2B

B−1 X i=0

TBYOL(ψ(si), a) −ψ−(s+ i)

2, (31)

(32)

where TBYOL: Rdψ × A →Rdψ is a jointly trained latent predictor, s+ i ∼M πβ(·|si, ai), πβ is the behavioral policy, and the minus sign (−) denotes target networks. HILP and ICVF instead train representations through bLHILP(ψ) = 1 2B

B−1 X i=0 ℓ2 τ(−1si̸=gi −γ∥ψ−(s′) −ψ−(g)∥+ ∥ψ(s) −ψ(g)∥), (33)

bLICVF(TICVF, ϕ, ψ) = 1 2B

B−1 X i=0

|τ −1Ai<0|

V (si, gi, yi) −1si=gi −γV−(s′ i, gi, yi)

2, (34)

where ℓ2 τ(x) = |τ −1x<0|x2 is an expectile regression loss with expectile τ, gi and yi are goals (or intents) sampled from a mixture of future and random states as described in Ghosh et al. (2023), V (x, y, z) = ϕ(x)⊤TICVF(ψ(z))ψ(y), TICVF: Rdψ →Rdψ×dψ is a matrix predictor and Ai = 1si=yi + γV (s′ i, yi, yi) − V (si, yi, yi). In an unified way across baselines, universal successor feature estimators Fψ: Rdϕ ×A×Z →Rdψ (and state encoders ϕ: S →Rdϕ) are then trained through standard TD-learning over features ψ by optimizing:

bLSF(Fψ, ϕ) = 1 2B

B−1 X i=0

Fψ(ϕ(si), ai; zi) −ψ−(s′ i) −γFψ,−(ϕ−(s′ i), a′ i; zi)

2, (35)

where a′ i ∼π(ϕ(s′ i), zi). The latent dynamics model in BYOL⋆and BYOL-γ⋆, as well as the intent-conditioned predictor from ICVF⋆(Ghosh et al., 2023), share the architecture of SFs, as described in Table 4, potentially dropping the subnetworks that receive states, actions or latents z as necessary. The state encoder in ICVF⋆ receives gradients from both the ICVF loss, and the successor feature prediction, which we found to slightly improve performance compared to only propagating gradients in either direction.

We found all zero-shot algorithms to be sensitive to certain hyperparameters, such as the strength of orthonormal regularization λ. For a fair comparison, we evaluate all algorithms over a small hyperparameter grid (6 configurations in DMC, and 4 in OGBench), and report performances for the best performing configuration for each domain. For all algorithms, we sweep over two values for the learning rate of the task encoder ψ: [10−4, 10−5]. A second important hyperparameter is the orthonormal regularization coefficient λ,

<!-- Page 32 -->

Laplacian FB RLDP BYOL* BYOL-γ* TD-JEPA

DMCRGB [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] DMC [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] [0.01, 0.1, 1] OGBenchRGB (nav) [0, 1] [100, 1000] [100, 1000] [0.001, 0.01] [0.001, 0.01] [0.1, 1] OGBench (nav) [0, 1] [100, 1000] [100, 1000] [0.001, 0.01] [0.001, 0.01] [0.1, 1] OGBenchRGB (man) [0, 1] [100, 1000] [100, 1000] [0.01, 0.1] [0.01, 0.1] [1, 10] OGBench (man) [0, 1] [100, 1000] [100, 1000] [0.01, 0.1] [0.01, 0.1] [1, 10]

**Table 5.** Orthonormal regularization ranges for each algorithm. (nav) and (man) indicate navigation and manipulation domains, respectively.

for which optimal ranges strongly differ across algorithms. In order to avoid an excessively large sweep, the ranges were thus tuned for each algorithm on a representative subset of domains, and are reported in Table 5. In general, we observe that contrastive methods prefer very strong regularization, while self-predictive methods can learn with weaker regularization in certain domains. For algorithms that do not leverage orthonormal regularization (HILP, ICVF⋆), we instead sweep over the likelihood of sampling random goals/intents in [0.375, 0.5].

E.6 Offline correction

The standard zero-shot evaluation pipeline (Touati et al., 2023) has traditionally relied on high-coverage datasets (Yarats et al., 2022a). OGBench (Park et al., 2025a) represents an interesting challenge in this sense, as most datasets are expert-like, and the incomplete support over actions induces well-known offline issues (Kumar et al., 2020). While these problems have been previously studied in the context of zero-shot RL (Jeen et al., 2024), we find that a novel instantiation of regularization techniques for single-task RL works well in this setting. In particular, we rely on a FlowQ-like regularization scheme (Park et al., 2025b): we train a flow model to estimate the behavioral policy, and replace the Gaussian policy with a noise-conditioned, one-step policy. This policy is regularized to samples generated by the flow model through 10 integration steps. The resulting behavior cloning loss term is normalized by the mean absolute Q-value in the batch, and scaled by a regularization coefficient α: we use α = 3 and α = 0.3 for manipulation and navigation tasks, respectively. Both networks are instantiated with the architectural hyperparameters described for π in Table 4. Finally, in order to be able to track BC targets, the policy is trained directly over the state space (or on the output of convolutional encoders in visual domain), instead of acting over state representations produced by state encoders ϕ(·).

E.7 Evaluation: zero-shot and fast adaptation

While zero-shot evaluation is averaged over all tasks (4-7, depending on the domain), fast adaptation is only evaluated on the hardest task per domain, estimated through average zero-shot performance of TD-JEPA and FB. This corresponds to run in walker, cheetah, quadruped and square in maze; we evaluate task 2 in antmaze domains and task 4 in cube-single. Fast adaptation methods that rely on pre-trained weights are initialized from the best performing zero-shot run. Behavior cloning regularization is carried over from pre-training if present, but orthonormal regularization is no longer applied. For online adaptation, the Update-to-Data ratio is fixed to 1, and 5000 initial transitions are collected by the policy before fine-tuning. Batches are sampled from a 50-50 mixture of the relabeled pre-training dataset, and a replay buffer containing the most recent 2 · 105 transitions.

The procedure to extract an actor and critic that are trainable through TD3 (Fujimoto et al., 2018) from zero-shot agents is rather direct. First, the relabeled dataset is used to infer the optimal latent zr through linear regression. Then, the critic network may then be derived from successor feature estimates: in the case of FB (Touati and Ollivier, 2021), Q(s, a) ≈F(ϕ(s), a, zr)⊤zr; in the case of TD-JEPA the same holds as soon as F is replaced by Tϕ. Although adaptation schemes over Z are possible (Sikchi et al., 2025), zr can be kept frozen. In order to match the output of the critic to the scale of rewards, zr is scaled such that its squared L2 norm matches the maximum reward over the dataset. Finally, the actor π(s) can be directly extracted from zero-shot policies as soon as they are conditioned on zr.

<!-- Page 33 -->

All evaluation metrics are averaged over 10 episodes in OGBench, and 20 in DMC, and computed over 10 random seeds for OGBench and 5 for DMC.

E.8 Pseudocode for TD-JEPA

1 def t r a i n (s e l f):

2 # sample training batch

3 obs, action, next_obs = s e l f. replay_buffer. sample ()

4 z = s e l f. sample_z (obs)

5

6 # compute targets

7 next_phi = s e l f. target_phi_encoder (next_obs)

8 next_psi = s e l f. target_psi_encoder (next_obs)

9 next_action = s e l f. actor (next_phi). sample ()

10 target_phi = next_psi + discount * s e l f. target_phi_predictor (next_phi, z, next_action)

11 target_psi = next_phi + discount * s e l f. target_psi_predictor (next_psi, z, next_action)

12 # compute predictions

13 phi = s e l f. phi_encoder (obs)

14 p s i = s e l f. psi_encoder (obs)

15 pred_phi = s e l f. phi_predictor (phi, z, action)

16 pred_psi = s e l f. psi_predictor (psi, z, action)

17 jepa_loss = mse(pred_phi target_phi. detach ()) + mse(pred_psi target_psi. detach ())

18 # regularize

19 phi_cov = torch. matmul(phi, phi.T)

20 phi_ortho_loss = phi_cov. diag (). mean () + 0.5 * phi_cov. off_diag (). pow (2). mean ()

21 psi_cov = torch. matmul(psi, p s i.T)

22 psi_ortho_loss = psi_cov. diag (). mean () + 0.5 * psi_cov. off_diag (). pow (2). mean ()

23

24 # compute actor loss

25 actor_action = s e l f. actor (phi. detach (), z). sample ()

26 actor_pred = s e l f. phi_predictor (phi. detach (), z, actor_action)

27 actor_loss = (actor_pred * z). sum (- 1). mean ()

28

29 # aggregate losses and optimize

30 l o s s = jepa_loss + s e l f. lambda_phi * phi_ortho_loss + s e l f. lambda_psi * psi_ortho_loss

31 l o s s += actor_loss

32 s e l f. optimizer. zero_grad ()

l o s s. backward ()

34 s e l f. optimizer. step ()

35 # update target networks

36 update_target (s e l f. target_phi_encoder, s e l f. phi_encoder)

37 update_target (s e l f. target_psi_encoder, s e l f. psi_encoder)

38 update_target (s e l f. target_phi_predictor, s e l f. phi_predictor)

39 update_target (s e l f. target_psi_predictor, s e l f. psi_predictor)

Listing 1 Python-like pseudocode for TD-JEPA (simplified).

Pseudocode for the default variant of TD-JEPA is shown in Listing 1; the output of predictors is assumed to be averaged across twin networks.
