---
title: "Reward Model Evaluation via Automatically-Ranked Policy Alignment"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39815
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39815/43776
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Reward Model Evaluation via Automatically-Ranked Policy Alignment

<!-- Page 1 -->

Reward Model Evaluation via Automatically-Ranked Policy Alignment

Aoran Wang, Lei Ou, Yang Yu, Zongzhang Zhang*

National Key Laboratory for Novel Software Technology, Nanjing University, Nanjing 210023, China

School of Artificial Intelligence, Nanjing University, Nanjing 210023, China

{wangar, oul}@lamda.nju.edu.cn, {yuy, zhangzz}@nju.edu.cn

## Abstract

Evaluating reward models is a fundamental challenge in Reinforcement Learning (RL), particularly in settings where the reward model is learned or manually designed. The standard paradigm for Reward Model Evaluation (RME) involves training an optimal policy via RL on the given reward model and assessing model quality through the performance of the resulting policy. However, this approach conflates the quality of the reward model with the effectiveness of RL training, and is computationally expensive due to the need for policy optimization. Recent RME methods attempt to circumvent this issue by evaluating reward models directly, without RL, but often rely on impractical assumptions such as access to a ground-truth reward or fail to utilize available supervision in a fine-grained manner. To overcome these limitations, we propose the Policy Preference Alignment Coefficient (PPAC), a novel metric for RME that requires neither RL training nor ground-truth rewards. PPAC first generates a sequence of automatically ranked policy preferences that guarantee monotonic improvement in the policy value, and then quantifies the alignment between these generated preferences and those implied by the candidate reward model. Experimental results across gridworld and continuous control task demonstrate that PPAC yields preference sequences with consistently increasing policy values and outperforms existing metrics in evaluating reward model quality.

## Introduction

In Reinforcement Learning (RL), the Reward Model (RM) plays a central role in shaping the behavior of the learned policy (Sutton and Barto 1998). In many real-world applications—such as autonomous driving (Codevilla et al. 2018) and language model alignment (Ouyang et al. 2022)—the ground-truth reward is unavailable, making it necessary to construct a surrogate reward model. This can be achieved through expert-crafted heuristics, language model-assisted design (Chen et al. 2024), or data-driven methods such as inverse reinforcement learning (Ng and Russell 2000) and preference-based learning (Christiano et al. 2017; Bai et al. 2022). However, the absence of a ground-truth reward gives

*Zongzhang Zhang is the corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

rise to a fundamental challenge: how can we evaluate the quality of a learned or designed reward model? This question highlights the need for effective and practical Reward Model Evaluation (RME) techniques.

A prevalent RME paradigm assesses a reward model by training an optimal policy via RL under the given reward and measuring the performance of the resulting policy through metrics such as cumulative return or task success rate (Booth et al. 2023). Under this paradigm, reward models are deemed superior if they induce higher-performing policies. However, this evaluation strategy conflates reward model quality with the effectiveness of RL training. For example, a high-quality reward model might appear poor due to unstable RL optimization—caused by algorithmic brittleness, suboptimal hyperparameters, or stochasticity in training (Engstrom et al. 2019)—while a flawed reward model might appear strong due to reward hacking (Skalse et al. 2022), where the agent exploits reward artifacts to achieve high returns. Moreover, this approach is computationally expensive, as it requires retraining policies for each candidate RM. This cost becomes prohibitive in large-scale settings, such as Reinforcement Learning from Human Feedback (RLHF) for large language models (Ouyang et al. 2022; Shao et al. 2024), or when evaluating a large ensemble of reward models.

To mitigate these challenges, recent RME works explore RL-free methods that disentangle RME from policy optimization. One line of research proposes discrepancy-based metrics that directly compare the canonicalized candidate reward model against a known ground-truth reward (Gleave et al. 2021; Wulfe et al. 2022; Skalse et al. 2024). These methods often employ shaping-invariant metrics, offering theoretically sound comparisons. However, their reliance on the access to the ground-truth reward—what is unavailable in most practical scenarios—limits their applicability.

Another class of methods evaluates reward models directly against available supervision signals, such as expert demonstrations or trajectory preferences (Brown et al. 2021; Muslimani et al. 2025). These approaches are more practical, as such supervision is often accessible in real-world settings. For instance, the Trajectory Alignment Consistency (TAC) (Muslimani et al. 2025) assesses a reward model by comparing the pairwise preferences it induces with those present in the data. While TAC avoids the high cost of RL training, its reliance on pairwise comparison alone fails to

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

26124

<!-- Page 2 -->

capture finer distinctions in reward quality (Zhu, Jordan, and Jiao 2023; Choi et al. 2024). In particular, methods limited to binary preferences may struggle to differentiate high-quality reward models from moderately good ones.

To address the limitations of existing RME approaches, we propose the Policy Preference Alignment Coefficient (PPAC), a novel RME metric that enables fine-grained evaluation of reward models using only trajectory comparisons. Unlike prior methods, PPAC does not rely on RL training or access to ground-truth rewards, making it practical for realworld applications with RME demand such as preferencebased RL and human feedback alignment.

Contribution At the core of PPAC is our proposed policy improvement criterion Demonstration-Guided Policy Improvement (DGPI). DGPI iteratively generates a sequence of policies with monotonically increasing value under the unknown ground-truth reward by leveraging expert-preferred trajectories. This is achieved by estimating a surrogate advantage function based on the expert’s state-value function, allowing each policy update to move toward expert-like behavior without explicitly recovering the reward. The resulting policy sequence forms an automatically-ranked ordering that reflects increasing alignment with expert preferences.

Using this sequence, PPAC evaluates a candidate reward model by comparing its induced policy preference ranking to the DGPI-generated ranking. Specifically, PPAC computes the Spearman’s rank correlation coefficient between the two rankings, capturing the alignment between the candidate reward model and the expert-guided preferences.

We validate PPAC on grid-world navigation and continuous control task. Experimental results show that PPAC more accurately reflects the underlying quality of candidate reward models compared to existing baselines, providing an efficient tool for direct RME from trajectory comparisons.

## Preliminaries

Notations We consider the Markov Decision Process (MDP) (Sutton and Barto 1998) formalized as a tuple ⟨S, A, P, d0, r, γ⟩, where S is the state space, A is the action space, P: S × A × S →[0, 1] is the transition probability function, d0 is the initial state distribution, r: S × A →R is the reward function, and γ ∈(0, 1] is the discount factor.

Given a stationary stochastic policy π: S × A →[0, 1], the discounted state distribution is defined as: dπ(s) = (1 −γ) P∞ t=0 γtPπ(st = s), which reflects the discounted visitation frequency of state s under policy π. The occupancy measure of π is defined as: ρπ(s, a) = (1 − γ) P∞ t=0 γtPπ(st = s, at = a) = dπ(s) · π(a | s), which gives the joint discounted visitation frequency of state-action pairs. For simplicity, we denote expectations over this distribution as Eπ[·]:= E(s,a)∼ρπ[·] throughout the paper.

The expected return of policy π under reward function r is defined as the expected discounted sum of rewards:

J(r, π) = Eπ [r (s, a)].

The RL objective is to find an optimal policy π∗in the policy space Π that maximizes the expected return J(r, π):

π∗= arg max π∈Π

J(r, π).

The state-action value function Qπ and the state value function V π of a policy π are defined as

Qπ(s, a) = r(s, a) + γEs′∼P(·|s,a) [V π (s′)],

V π(s) = Ea∼π(·|s) [Qπ(s, a)].

The advantage function of π is given by:

Aπ(s, a) = Qπ(s, a) −V π(s).

Problem Statement We assume access to a preference dataset D = {(τ + i, τ − i)}N i=1 consisting of N trajectory comparisons. In each comparison pair, τ + i denotes the preferred (or better) trajectory and τ − i the rejected (or worse) trajectory. The two trajectories in each comparison pair share the same initial state. We make two key assumptions:

• All preferred trajectories τ + i = (si

0, ai 0, si 1,..., si T) are generated by a common stationary stochastic policy π+ in a latent MDP ⟨S, A, P, d0, rgt, γ⟩, and all rejected τ − i are generated similarly by another policy π−. • The policy π+ corresponds to an expert policy πE that is optimal under the unknown ground-truth reward rgt.

These assumptions are plausible in practice, as {τ + i }N i=1 typically represents the full set of demonstrations of desirable behavior, and in the absence of further supervision, we treat them as approximating the expert behavior. Conversely, {τ − i }N i=1 represents the suboptimal alternatives. The goal of this paper is to define a metric M(reval, D) that evaluates the quality of a candidate reward model reval using only the preference dataset D. As motivated in Section 1, we aim for the metric that avoids RL training on reval, and exploits the implicit supervision embedded in trajectory preferences, beyond merely classifying τ + i vs. τ − i.

## 3 Method

We introduce our proposed RME framework based on the automatically-ranked policy preferences derived from trajectory comparisons. This section is structured as follows:

• We define policy preferences based on expected state value under initial state distribution, extending prior formulations (Bowling et al. 2023; Muslimani et al. 2025). • We propose Demonstration-Guided Policy Improvement (DGPI), a policy update criterion that guarantees monotonic improvements in policy value. • We describe the process of generating automaticallyranked policy sequences with DGPI and computing the Policy Preference Alignment Coefficient (PPAC). An overview of the complete PPAC computation pipeline is illustrated in Figure 1. Detailed derivations and proofs in this section are deferred to Appendix A 1. Policy Preference Let the discounted state visitation probability from an initial state s be defined as: Pt(s′) = (1 − γ) P∞ t=0 γtPπ(st = s′|s0 = s). Then considering following the policy π from s, the state value function V π(s) under the ground-truth reward rgt is given by:

V π(s) = Est∼Pt,at∼π(·|st) [rgt (st, at)]. (1)

1https://www.lamda.nju.edu.cn/wangar/PPAC supp.pdf

26125

<!-- Page 3 -->

Chosen Trajectories

Rejected Trajectories

Expert Q-value

Learning

Behavior

Cloning

Demonstration-Guided Policy Improvement

(DGPI)

Oracle Policy Ranking

Estimated Policy Ranking

Ranking

Correlation

Policy Preference Policy Preference

Trajectory Comparisons Policy Preference Alignment Coefficient

(PPAC)

**Figure 1.** Overview of PPAC computation from trajectory comparison supervision. DGPI generates an automatically-ranked sequence of policies using the expert Q-value learned from the preferred trajectories. PPAC evaluates the quality of a candidate reward model by measuring the alignment between its induced policy rankings and the oracle ranking produced by DGPI.

We further define the support set of initial state distribution Sinit ⊆S as the following set of states,

Sinit = {s ∈S | d0(s) > 0}. (2)

We can now define the preference between policies, i.e., the policy preference, based on Eq. 1 and Eq. 2. Definition 3.1 (Policy Preference). In an infinite-horizon MDP ⟨S, A, P, d0, rgt, γ⟩, we define the preference ordering over stationary stochastic policies as follows:

πA ≻ (rgt,γ) πB ⇐⇒V πA(s0) > V πB(s0), for all s0 ∈Sinit.

That is, policy πA is preferred over policy πB if and only if starting from every possible initial state, the expected return of the trajectories following πA is larger than the expected return of the trajectories following πB.

The subscript (rgt, γ) emphasizes that this policy preference ordering is with respect to the reward rgt and the discount factor γ. In the rest of the paper, we simplify this policy preference w.r.t. (rgt, γ) as ≻when there is no ambiguity. Since π+ is assumed to be optimal under the reward rgt, it follows directly that π+ is preferred over π−, i.e., π+ ≻π−. Demonstration-Guided Policy Improvement (DGPI) We now introduce DGPI, a novel policy improvement rule guided by expert demonstrations that ensures monotonic improvements in the policy value, even in the absence of rgt.

We begin with a classic result from (Kakade and Langford 2002) that measures the expected value difference. Lemma 3.2. Given an initial state distribution d0, for any two policies ˜π and π,

Es∼d0

V ˜π(s)

−Es∼d0 [V π(s)] = 1 1 −γ E˜π [Aπ(s, a)].

(3) To improve from π within the trust-region constraint (Schulman et al. 2015), we consider the following optimization objective that maximizes the right-hand side of Eq. 3 with a KL-divergence regularization:

arg max

˜π∈Π

E˜π [Aπ(s, a)] −αDd˜π

KL(˜π ∥π), (4)

where Dd˜π

KL (˜π∥π) = Es∼d˜π[DKL(˜π(·|s)∥π(·|s))] is the expected KL-divergence between ˜π(·|s) and π(·|s) under the state distribution d˜π. The maximization in Eq. 4 admits an analytical solution (Azar, G´omez, and Kappen 2012):

˜π(a | s) = 1 Z(s)π(a | s) exp

1 αAπ(s, a)

, (5)

where the state-dependent function Z(s) is the normalizer to ensure that ˜π(a|s) sums up to 1 on all actions for each s.

Proposition 1 in (Wang et al. 2018) indicates that the updated policy ˜π in Eq. 5 ensures: for any state s ∈S, V ˜π(s) > V π(s) before convergence. In other words, updating π with Eq. 5 naturally yields a policy preference ˜π ≻π.

However, we can not thus construct automatically-ranked policy preferences π−= π1 ≺π2 ≺· · · ≺πK = π+ by iteratively updating with Eq. 5. The main challenge is that without knowing rgt, we can not estimate the advantage function Aπ(s, a). In fact, recovering the exact ground-truth reward from demonstration supervision remains an open and ill-posed problem (Lazzati and Metelli 2025).

Despite the inaccessibility of exact rgt, recent work has shown that it is possible to estimate the optimal state-action value function QπE(s, a) corresponding to the expert policy πE, purely from the expert demonstrations (Garg et al. 2021; Sikchi et al. 2024; Moulin, Neu, and Viano 2025). This observation opens a promising pathway for policy improvement without the ground-truth reward recovery. One representative approach is Inverse soft-Q Learning (IQ-Learn) (Garg et al. 2021), which formulates a non-adversarial method to recover QπE(s, a). However, IQ-Learn inherently depends on entropy regularization and assumes the policy is implicitly shaped by a regularized reward, which is not aligned with our unregularized setup. In contrast, Saddle- Point Offline Imitation Learning (SPOIL) learns QπE(s, a)

26126

<!-- Page 4 -->

## Algorithm

1: SPOIL (Moulin, Neu, and Viano 2025) Input: Expert trajectories τE, learning rate η > 0, and numbers of iteration T

1: Initialize Q-function Q0, uniform policy π0. 2: for step t = 1, 2,..., T do 3: πt(a | s) ∝πt−1(a | s) exp(η · Qt−1(s, a)). 4: Train Qt(s, a) by solving the following maximization arg max

Q

EπE

Q(s, a) −Ea′∼πt[Q(s, a′)]

.

5: end for 6: return QT by alternating between Q-value estimation and policy optimization in the following formulation without any regularization on policy or reward model:

Qk(s, a) ∈arg max

Q

EπE

Q(s, a) −Ea′∼πk[Q(s, a′)]

, πk+1(a | s) = πk(a | s) exp η · Qk(s, a)

P a′∈A πk(a′ | s) exp η · Qk(s, a′)

, where η > 0 is the learning rate controlling the update strength. As shown in prior works (Ho and Ermon 2016; Garg et al. 2021), this iterative scheme converges to the optimal state-action value function Q∗= QπE(s, a).

In our framework, SPOIL is used as a subroutine to recover QπE(s, a) from the expert trajectories {τ + i }N i=1. The SPOIL algorithm is summarized in Algorithm 1, and more details on it are deferred to Appendix B.

Being able to obtain QπE(s, a), we define the surrogate value function ˆV π(s) and surrogate advantage function

ˆAπ(s, a) with respect to the policy π as follows:

ˆV π(s) = Ea∼π(·|s) [QπE(s, a)], ˆAπ(s, a) = QπE(s, a) −ˆV π(s).

(6)

Intuitively, ˆV π(s) represents the expected return of executing policy π for one step from the state s, then following πE thereafter. The surrogate advantage ˆAπ(s, a) reflects the benefit of consistently following πE from the state s instead of taking an action a ∼π(·|s) at the first step.

In analogy to Lemma 3.2, we establish that the surrogate advantage estimates above yield valid improvement signals:

Lemma 3.3. For any two policies ˜π and π,

Es∼d˜π h

ˆV ˜π(s)

i

−Es∼d˜π h

ˆV π(s)

i

= 1 1 −γ E˜π h

ˆAπ(s, a)

i

.

(7)

We use this result to derive a surrogate policy update rule analogous to Eq. (5), replacing the true advantage with its surrogate counterpart. To obtain a policy ˜π that maximally improves over π, we maximize the right-hand side of Eq. 8 with KL-regularization Dd˜π

KL(˜π ∥π), yielding the following closed-form solution:

˜π(a | s) = 1 Z′(s)π(a | s) exp

1 α

ˆAπ(s, a)

, (8)

where ˆAπ(s, a) is the surrogate advantage function in Eq. 6, and Z′(s) is the normalizer that ensures ˜π(a|s) forms a valid probability distribution. Our proposed Demonstration- Guided Policy Improvement (DGPI) adopts this surrogateadvantage-weighted updating as its core mechanism.

The following proposition confirms that DGPI enjoys the same monotonic improvement guarantee as the update in Eq. 5, despite using surrogate advantage estimates: Proposition 3.4 (Monotonic Improvement). Let ˜π be obtained from π via Eq. 8. Then:

V ˜π(s) > V π(s), for all s ∈S.

That is, ˜π ≻π w.r.t. the rgt and the discounted factor γ.

Moreover, repeated application of exact DGPI from any initial policy π1 yields a sequence of strictly improving policies π1, π2,..., eventually converging to expert policy πE: Proposition 3.5. Let {πt}t≥1 denote the sequence produced by iteratively applying exact DGPI. Then for some T, we have πT = πE, and π1 ≺π2 ≺· · · ≺πT.

These properties of DGPI enable us to automatically generate a preference chain of policies π−= π1 ≺π2 ≺· · · ≺ πK = π+ purely from trajectory preference data, laying the foundation for our proposed PPAC metric. Policy Preference Alignment Coefficient (PPAC) We now describe how to use DGPI to generate a sequence of automatically-ranked policy preferences from the preference dataset D = {(τ + i, τ − i)}N i=1, and how to compute our proposed evaluation metric—Policy Preference Alignment Coefficient (PPAC)—based on the alignment between this policy sequence and a candidate reward model.

Motivated by recent findings that listwise comparisons provide richer supervision than pairwise preferences for reward learning (Zhu, Jordan, and Jiao 2023; Choi et al. 2024), we hypothesize that enforcing consistency with a listwise ordering over policies enables finer-grained evaluation of reward model quality, compared with a pairwise ordering.

To construct such a listwise ordering, we begin by initializing the policy sequence from the rejected policy π1 = π−, which we approximate using Behavior Cloning (BC) (Pomerleau 1991) on the set of rejected trajectories {τ − i }N i=1 Then, we apply DGPI iteratively to obtain the subsequent policies π1, π2,..., πK, where each update is given by:

˜π(a | s) = 1 Z′(s)πk(a | s) exp

1 α

ˆAπk(s, a)

. (9)

In practice, we fit the parameterized πk+1 by minimizing the KL-divergence between the DGPI target ˜π and πk+1:

arg min πk+1∈Π

D dπk KL (˜π∥πk+1)

= arg max πk+1∈Π

X s dπk(s)

X a

˜π(a | s) log πk+1(a | s)

≈arg max πk+1∈Π

Eπk exp

1 α

ˆAπk(s, a)

log πk+1(a | s)

,

(10) which is equivalent to a weighted behavior cloning objective where samples are reweighted by exp

1 α ˆAπk(s, a)

.

26127

<!-- Page 5 -->

We repeat this DGPI process in Eq. 10 to convergence. According to Proposition 3.5, we obtain a strictly ordered sequence of policy preferences:

π1 = π−≺π2 ≺· · · ≺πK = π+, which—by construction—satisfies a monotonic increase in their values under the ground-truth reward rgt and starting from any possible initial state s in D:

V π1(s) < · · · < V πK(s).

This ranking of policy values provides a supervision signal at the level of policy preference, which we refer to as the oracle policy ranking Rgt. To evaluate a candidate reward model reval, we assess whether its induced preferences over the policies {π1,..., πK} aligns with the oracle ranking.

For each comparison pair (τ + i, τ − i) ∈D, we first identify the shared initial state si, and sample M trajectories from each policy πk starting at si. The empirical value V πk(si) of each policy under reval is estimated as:

V πk(si) = 1

M

M X m=1

Tm−1 X t=0 γtreval(sm t, am t), (11)

where (sm t, am t) denotes the t-th transition in the m-th trajectory sampled by πk with horizon Tm. We denote the ranking over these estimated values as Ri eval. If reval functions as good as rgt, the rankings Ri eval and Rgt should exactly match. On the contrary, the worse reval is than rgt, the more severely the rankings Ri eval and Rgt should differ. To quantify their alignment, we use Spearman’s rank correlation coefficient:

C(Ri eval, Rgt) = cov(Ri eval, Rgt) σRi eval · σRgt

, (12)

where cov(Ri eval, Rgt) denotes the covariance of these two rank variables, and σRi eval, σRgt are the standard deviations. The Policy Preference Alignment Coefficient (PPAC) is then defined as the average Spearman’s rank correlation across all N comparison pairs in D, i.e.,

PPAC(reval, D) = 1

N

N X i=1

C(Ri eval, Rgt).

In practice, we monitor the surrogate state value ˆV πk to select a set of K policies that are approximately evenly spaced in the value range, ensuring diverse preference supervision throughout the DGPI process. We show the process of computing PPAC from D = {τ + i, τ − i }N i=1 in Algorithm 2. By construction, A PPAC value near 1 indicates a strong agreement between the estimated and oracle rankings, reflecting high reward model fidelity. A PPAC value near −1 indicates a reverse alignment. Moreover, PPAC is designed to be invariant to common reward transformations, ensuring that it evaluates only the policy preference structure encoded by the reward model, rather than its numeric value. Proposition 3.6. When evaluated under the same preference dataset D, if the reward models r and r′ differ by a positive scaling transformation r′(s, a) = β1 · r(s, a) + β2,

## Algorithm

2: Computing the PPAC Input: Candidate reward model reval, trajectory comparisons dataset D = {τ + i, τ − i }N i=1, and granularity control parameter K

1: Estimate QπE from {τ + i }N i=1 with SPOIL. (Alg. 1) 2: Train policy π1 from {τ − i }N i=1 with BC. 3: Generate ranked policies π1 ≺· · · ≺πK in DGPI updating from π1. (Eq. 10) 4: for i = 1 to N do 5: Let si ←initial state of (τ + i, τ − i). 6: for k = 1 to K do 7: Sample trajectories starting from πk starting at si. 8: Estimate V πk(si) under reval. (Eq. 11) 9: end for 10: Compute C(Ri eval, Rgt) between the estimated ranking Ri eval and the oracle ranking Ri gt. (Eq. 12) 11: end for 12: return PPAC(reval, D) = 1 N

PN i=1 C(Ri eval, Rgt).

where β1 > 0, β2 are constants, or a potential-based reward shaping transformation (Ng, Harada, and Russell 1999)

r′(s, a) = r(s, a) + γEs′∼P(·|s,a)Φ(s′) −Φ(s), where Φ: S →R is a potential function, then

PPAC(r, D) = PPAC(r′, D).

## 4 Experiment

In this section, we evaluate PPAC against several baseline methods for RME. We begin with a summary of the experimental setup, followed by main results. Additional implementation details and analysis are provided in Appendix C. Benchmarks To assess whether PPAC serves as an effective RME metric, we evaluate it on two standard tasks:

• MiniGrid-DoorKey-8×8 (Chevalier-Boisvert et al. 2023): a goal-oriented navigation task in a 2D grid world with image-based observations and a discrete action space. The agent must first pick up a key and then open a door to reach the goal. The ground-truth reward is defined as 1−0.9∗(step count/max steps) if the agent successfully reaches the goal, and 0 otherwise. We randomize 10 different instances of this task for experiment. • HalfCheetah (MuJoCo) (Todorov, Erez, and Tassa 2012): a control task with feature-based observations and a continuous action space. The agent is rewarded for accelerating forward, with a penalty for excessive control inputs. Baselines We compare PPAC with the following baselines:

• STAndardised Reward Comparison (STARC) (Skalse et al. 2024): STARC measures the discrepancy between a canonicalized candidate reward model and the groundtruth reward. It generalizes previous discrepancy-based metrics (Gleave et al. 2021; Wulfe et al. 2022), so we use its best-performing specification as the representative. • TAC (Muslimani et al. 2025): TAC compares the pairwise preferences over trajectory distributions induced by the candidate reward and the supervision data.

26128

<!-- Page 6 -->

Reward Model NegativeSTARC TAC PPAC-BC PPAC-AIL PPAC

GroundTruth 0.0000 1.0000 0.8300 0.9400 0.9800 PotentialShaped -1.3232 1.0000 0.9100 0.9100 0.9800 SecondGoal-Slight -1.6591 1.0000 0.9100 0.8300 0.6400 SecondGoal-Intense -1.7303 1.0000 0.8100 0.6220 0.4800 Constant -1.6024 -1.0000 -0.9100 -0.9400 -0.9400

**Table 1.** RME results on the MiniGrid-DoorKey-8×8 task. Each value represents the average RME score across 10 randomized task instances. Higher values indicate candidate reward models of higher quality.

Reward Model NegativeSTARC TAC PPAC-BC PPAC-AIL PPAC

GroundTruth 0.0000 1.0000 0.9353 0.9774 0.9873 PotentialShaped -0.6745 1.0000 0.9353 0.9774 0.9873 SecondGoal-Slight -0.2489 1.0000 0.8346 0.9774 0.7549 SecondGoal-Intense -0.8099 1.0000 0.6060 0.9549 0.5203 Random -1.8873 -1.0000 -0.9489 -0.9489 -0.9293

**Table 2.** RME results on the HalfCheetah task. Higher values indicate candidate reward models of higher quality.

• PPAC with noisy-injected Behavior Cloning (PPAC-BC): A variant of PPAC that replaces DGPI with noisy perturbations of the BC policy, inspired by Disturbancebased Reward Extrapolation (D-REX) (Brown, Goo, and Niekum 2020). Intermediate policies are generated by injecting increasing Gaussian noise into a BC policy trained on the chosen trajectories. • PPAC with Adversarial Imitation Learning (PPAC-AIL): A variant of PPAC inspired by Automated Preference generation with Enhanced Coverage (APEC) (Zhang et al. 2025), whose intermediate policies are checkpoints in Adversarial Imitation Learning (AIL) training with the chosen trajectories serving as expert demonstrations. For STARC, the ground-truth reward is exposed during evaluation as required. For PPAC-BC and PPAC-AIL, only the chosen trajectories are used as expert demonstrations. TAC and PPAC make full use of the comparison dataset.

All metrics except STARC yield scores between [−1, 1], with higher values indicating better reward models. Since STARC is unbounded and higher values indicate worse performance, we report the negative STARC (i.e., NegativeSTARC) to maintain consistency in interpretation. Experimental Design For each benchmark, we construct five reward models of descending quality:

• GroundTruth: the ground-truth RM, the best RM of all. • PotentialShaped: the ground-truth RM transformed by potential-based shaping. This transformation preserves the optimal policy and should yield close RME score. • SecondGoal-Slight: the ground-truth RM with an additional small bonus for achieving a secondary and orthogonal objective. In MiniGrid, this corresponds to reaching a distractor grid cell; in HalfCheetah, it incentivizes the agent maintaining a specific height. • SecondGoal-Intense: the same as above but with a large bonus for the secondary goal, substantially diverting the agent’s behavior in both MiniGrid and HalfCheetah.

• Constant (or Random): an uninformative reward, either randomly generated (or constant) across all transitions.

These five reward models above represent a quality spectrum from ideal to poor. An effective RME metric should assign similar scores to GroundTruth and PotentialShaped, and progressively lower scores to SecondGoal-Slight, SecondGoal- Intense, and Random at clear intervals. Results We conduct experiments on 10 randomly generated DoorKey tasks. For each DoorKey task, we train a Proximal Policy Optimization agent (Schulman et al. 2017) under its ground-truth reward until it consistently reaches the goal, designating it as the latent chosen policy. A mediumperformance checkpoint from the same training run—prior to convergence—is selected as the rejected policy. We collect N = 5 trajectories from each of these policies per task as supervision to compute TAC, PPAC-BC, PPAC-AIL, and PPAC. For PPAC-based methods, we set the ranking granularity to K = 5. For the HalfCheetah task, we train a Soft Actor-Critic agent (Haarnoja et al. 2018) that achieves a performance of approximately 12,000 as the chosen policy, and similarly select an intermediate policy of medium performance as the rejected one. We collect N = 50 trajectories from each policy and use a higher granularity with K = 20.

The RME results for DoorKey and HalfCheetah are reported in Table 1 and Table 2, respectively. We observe several key findings: NegativeSTARC, due to its unbounded scale, lacks interpretability to reward quality as an absolute metric. More critically, it fails to correctly recognize that PotentialShaped is as good as the GroundTruth, contradicting its theoretical invariance intention. TAC demonstrates limited discriminative power, failing to distinguish between all but the most degenerate reward model (Constant/Random). This supports our motivation that pairwise preference signals are insufficient for fine-grained RME. PPAC-BC performs reasonably well on HalfCheetah, correctly ordering most reward models. However, in DoorKey it incorrectly ranks PotentialShaped above both GroundTruth

26129

<!-- Page 7 -->

and SecondGoal-Slight. Additionally, the low magnitude of PPAC-BC for GroundTruth suggests that the noise-injected policies used in this method do not consistently degrade in performance. This reflects the inherent instability in D- REX-style perturbations, where high-noise policies behave nearly randomly and fail to preserve performance ordering. PPAC-AIL successfully ranks reward models in DoorKey, but fails to do so in HalfCheetah by assigning similar scores to models of differing quality. This suggests that AIL-generated policy sequences lack sufficient value separation in high-dimensional continuous control settings. In contrast, PPAC consistently produces scores close to 1 for GroundTruth, correctly identifies PotentialShaped as equivalent to GroundTruth and clearly separates reward models across both tasks. These results indicate that PPAC generates more reliably ordered policy preferences, and provides more discriminative RME than existing baselines.

## 5 Related Work Reward Model Evaluating

Traditional RME relies on indirect evaluation, where the quality of a reward model is inferred from the performance of the optimal policy trained under it. In this paradigm, a reward model is considered superior if the policy trained via RL under that model achieves higher returns or task success rates. In contrast, PPAC provides a form of direct reward evaluation, decoupling reward model quality from the RL training dynamics. This separation is crucial, as it avoids confounding RME with RL instability, sensitivity to hyperparameters, or suboptimal policy convergence. Moreover, PPAC is highly efficient when multiple reward models must be evaluated, since DGPI is executed only once on the supervision dataset rather than requiring separate RL training for each reward candidate.

A number of prior works have proposed direct evaluation metrics that assess reward models without training policies. For example, Equivalent-Policy Invariant Comparison (EPIC) (Gleave et al. 2021) canonicalizes reward models by removing potential-based shaping and computes similarity using correlation over a fixed transition distribution. Dynamics-Aware Reward Distance (DARD) (Wulfe et al. 2022) extends EPIC by evaluating only on realizable transitions using known dynamics. STARC (Skalse et al. 2024) further generalizes EPIC and DARD into a unified framework with improved theoretical guarantees. However, all of these methods require access to the ground-truth reward, which is often unavailable in real-world tasks—the very reason why reward model learning is needed. In contrast, PPAC leverages trajectory comparisons, a form of supervision that is far more accessible in practice, especially in preferencebased reward learning settings (Christiano et al. 2017).

Another line of work, such as TAC (Muslimani et al. 2025), also seeks to avoid RL by comparing rankings over trajectory distributions. TAC quantifies the alignment between the candidate reward model’s induced preferences and an oracle ranking. While TAC provides a useful perspective, it operates on pairwise preferences, which often lack the granularity needed to discriminate between closely competing reward models. PPAC addresses this limitation by constructing automatically-ranked listwise policy sequences using our proposed DGPI procedure, thereby offering finergrained RME. As shown in our experiments, preference misalignment is more easily captured through disorder in listwise preferences than through flips in pairwise comparisons. Ranked Preference Generation A growing body of work demonstrates that listwise supervision offers significant advantages over pairwise comparisons in both reward learning and imitation learning (Zhu, Jordan, and Jiao 2023; Choi et al. 2024; Brown, Goo, and Niekum 2020; Zhang et al. 2025). These findings motivate the development of methods that generate automatically-ranked trajectories or policies from suboptimal data without requiring extra explicit labels or access to the ground-truth reward.

D-REX (Brown, Goo, and Niekum 2020) proposes generating ranked policies by injecting Gaussian noise of increasing magnitude into a BC policy trained on suboptimal demonstrations. While D-REX proves an upper bound on the expected return of such noise-injected policies, it does not guarantee monotonic degradation in performance as noise increases. APEC (Zhang et al. 2025), on the other hand, produces ranked policies by sampling intermediate policies from the training trajectory of AIL. Although APEC provides a lower bound on value during AIL training, it likewise lacks guarantees of monotonic improvement on the performance of generated policies. To the best of our knowledge, our proposed Demonstration-Guided Policy Improvement (DGPI) is the first method that ensures monotonic improvement in policy performance without requiring access to a ground-truth reward or external preference labeling. DGPI leverages only trajectory comparisons, making it wellsuited to RME in preference-based reward learning.

While our primary focus is RME, DGPI is broadly applicable to other tasks that require generating ranked policies in the absence of the ground-truth reward. As shown in Appendix D, DGPI can be naturally extended to work under other types of supervision as well, making it a versatile tool in IL, curriculum generation, and structured exploration.

## 6 Conclusion and Limitation

We propose the PPAC, a novel RME metric without relying on RL training or access to ground-truth rewards. PPAC measures the alignment between a reward model’s induced policy ranking and an expert-guided policy ranking generated via our proposed DGPI, which ensures monotonic policy improvement without extra supervision. Experiments on grid-world and continuous control tasks demonstrate that PPAC achieves more consistent and discriminative evaluation than existing RME methods, highlighting PPAC’s capability as a practical, efficient, and theoretically grounded approach to reward model assessment.

One limitation of PPAC lies in its reliance on accurate estimation of the expert Q-function. When trajectory comparison data is limited, the unreliable estimation undermines DGPI’s monotonic improvement guarantee. Additionally, PPAC is more of a necessity indicator of reward model quality as a high PPAC score certifies adequacy only within the coverage of the provided trajectories. In future studies, we will explore more on the coverage analysis to strengthen the sufficiency of our proposed RME indicator.

26130

<!-- Page 8 -->

## Acknowledgements

This work is supported by the National Science Foundation of China (62276126, 62250069, 62495093) and Jiangsu Science Foundation (BK20243039).

## References

Azar, M. G.; G´omez, V.; and Kappen, H. J. 2012. Dynamic policy programming. Journal of Machine Learning Research (JMLR), 13: 3207–3245.

Bai, Y.; Jones, A.; Ndousse, K.; Askell, A.; Chen, A.; Das- Sarma, N.; Drain, D.; Fort, S.; Ganguli, D.; Henighan, T.; et al. 2022. Training a helpful and harmless assistant with reinforcement learning from human feedback. arXiv preprint arXiv:2204.05862.

Booth, S.; Knox, W. B.; Shah, J.; Niekum, S.; Stone, P.; and Allievi, A. 2023. The perils of trial-and-error reward design: misdesign through overfitting and invalid task specifications. In Proceedings of the 37th AAAI Conference on Artificial Intelligence (AAAI), 5920–5929.

Bowling, M.; Martin, J. D.; Abel, D.; and Dabney, W. 2023. Settling the reward hypothesis. In Proceedings of the 40th International Conference on Machine Learning (ICML), 3003–3020.

Brown, D. S.; Goo, W.; and Niekum, S. 2020. Better-thandemonstrator imitation learning via automatically-ranked demonstrations. In Proceedings of the 2020 Conference on Robot Learning (CoRL), 330–359.

Brown, D. S.; Schneider, J.; Dragan, A.; and Niekum, S. 2021. Value alignment verification. In Proceedings of the 38th International Conference on Machine Learning (ICML), 1105–1115.

Chen, X.-H.; Wang, Z.; Du, Y.; Jiang, S.; Fang, M.; Yu, Y.; and Wang, J. 2024. Policy learning from tutorial books via understanding, rehearsing and introspecting. Advances in Neural Information Processing Systems (NeuIPS), 37: 18940–18987.

Chevalier-Boisvert, M.; Dai, B.; Towers, M.; Perez-Vicente, R.; Willems, L.; Lahlou, S.; Pal, S.; and Castro, P. S. 2023. Minigrid & miniworld: Modular & customizable reinforcement learning environments for goal-oriented tasks. Advances in Neural Information Processing Systems (NeuIPS), 36: 73383–73394.

Choi, H.; Jung, S.; Ahn, H.; and Moon, T. 2024. Listwise reward estimation for offline preference-based reinforcement learning. In Proceedings of the 41st International Conference on Machine Learning (ICML), 8651–8671.

Christiano, P. F.; Leike, J.; Brown, T.; Martic, M.; Legg, S.; and Amodei, D. 2017. Deep reinforcement learning from human preferences. Advances in Neural Information Processing Systems (NIPS), 4302–4310.

Codevilla, F.; M¨uller, M.; L´opez, A.; Koltun, V.; and Dosovitskiy, A. 2018. End-to-end driving via conditional imitation learning. In Proceedings of the 35th International Conference on Robotics and Automation (ICRA), 4693–4700.

Engstrom, L.; Ilyas, A.; Santurkar, S.; Tsipras, D.; Janoos, F.; Rudolph, L.; and Madry, A. 2019. Implementation matters in deep RL: A case study on PPO and TRPO. In Proceedings of the 7th International Conference on Learning Representations (ICLR). Garg, D.; Chakraborty, S.; Cundy, C.; Song, J.; and Ermon, S. 2021. IQ-Learn: Inverse soft-Q learning for imitation. Advances in Neural Information Processing Systems (NeurIPS), 34: 4028–4039. Gleave, A.; Dennis, M. D.; Legg, S.; Russell, S.; and Leike, J. 2021. Quantifying differences in reward functions. In Proceedings of the 9th International Conference on Learning Representations (ICLR). Haarnoja, T.; Zhou, A.; Abbeel, P.; and Levine, S. 2018. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In Proceedings of the 35th International Conference on Machine Learning (ICML), 1861–1870. Ho, J.; and Ermon, S. 2016. Generative adversarial imitation learning. Advances in Neural Information Processing Systems (NIPS), 29: 4565–4573. Kakade, S.; and Langford, J. 2002. Approximately optimal approximate reinforcement learning. In Proceedings of the 19th International Conference on Machine Learning (ICML), 267–274. Lazzati, F.; and Metelli, A. M. 2025. On the partial identifiability in reward learning: Choosing the best reward. arXiv preprint arXiv:2501.06376. Moulin, A.; Neu, G.; and Viano, L. 2025. Inverse Q-learning done right: Offline imitation learning in Qπ-realizable MDPs. arXiv preprint arXiv:2505.19946. Muslimani, C.; Johnstonbaugh, K.; Chandramouli, S.; Booth, S.; Knox, W. B.; and Taylor, M. E. 2025. Towards improving reward design in RL: A reward alignment metric for RL practitioners. arXiv preprint arXiv:2503.05996. Ng, A. Y.; Harada, D.; and Russell, S. 1999. Policy invariance under reward transformations: Theory and application to reward shaping. In Proceedings of the 16th International Conference on Machine Learning (ICML), 278–287. Ng, A. Y.; and Russell, S. 2000. Algorithms for inverse reinforcement learning. In Proceedings of the 17th International Conference on Machine Learning (ICML), 663–670. Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.; et al. 2022. Training language models to follow instructions with human feedback. Advances in Neural Information Processing Systems (NeuIPS), 35: 27730–27744. Pomerleau, D. A. 1991. Efficient training of artificial neural networks for autonomous navigation. Neural Computation, 3: 88–97. Schulman, J.; Levine, S.; Abbeel, P.; Jordan, M.; and Moritz, P. 2015. Trust region policy optimization. In Proceedings of the 32nd International Conference on Machine Learning (ICML), 1889–1897. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.

26131

<!-- Page 9 -->

Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.; Zhang, H.; Zhang, M.; Li, Y.; et al. 2024. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. Sikchi, H.; Zheng, Q.; Zhang, A.; and Niekum, S. 2024. Dual RL: Unification and new methods for reinforcement and imitation learning. In Proceedings of the 12th International Conference on Learning Representations (ICLR). Skalse, J.; Howe, N.; Krasheninnikov, D.; and Krueger, D. 2022. Defining and characterizing reward gaming. Advances in Neural Information Processing Systems (NeuIPS), 35: 9460–9471. Skalse, J. M. V.; Farnik, L.; Motwani, S. R.; Jenner, E.; Gleave, A.; and Abate, A. 2024. STARC: A general framework for quantifying differences between reward functions. In Proceedings of the 12th International Conference on Learning Representations (ICLR). Sutton, R. S.; and Barto, A. G. 1998. Reinforcement learning: An introduction. MIT press Cambridge. Todorov, E.; Erez, T.; and Tassa, Y. 2012. MuJoCo: A physics engine for model-based control. In Proceedings of the 25th IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 5026–5033. Wang, Q.; Xiong, J.; Han, L.; Liu, H.; Zhang, T.; et al. 2018. Exponentially weighted imitation learning for batched historical data. Advances in Neural Information Processing Systems (NeurIPS), 6288–6297. Wulfe, B.; Ellis, L. M.; Mercat, J.; McAllister, R. T.; and Gaidon, A. 2022. Dynamics-aware comparison of learned reward functions. In Proceedings of the 10th International Conference on Learning Representations (ICLR). Zhang, Z.; Xu, T.; Du, X.; Cao, X.; Sun, Y.; and Yu, Y. 2025. Improving reward model gneralization from adversarial process enhanced preferences. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 76414– 76435. Zhu, B.; Jordan, M.; and Jiao, J. 2023. Principled reinforcement learning with human feedback from pairwise or k-wise comparisons. In Proceedings of the 40th International Conference on Machine Learning (ICML), 43037–43067.

26132
