---
title: "Distributional Inverse Reinforcement Learning"
source_url: https://icml.cc/virtual/2026/oral/71147
paper_pdf_url: https://arxiv.org/pdf/2510.03013v4
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Distributional Inverse Reinforcement Learning

<!-- Page 1 -->

Distributional Inverse Reinforcement Learning

Feiyang Wu 1 Ye Zhao 2 Anqi Wu 1

## Abstract

We propose a distributional framework for offline Inverse Reinforcement Learning (IRL) that jointly models uncertainty over reward functions and full distributions of returns. Unlike conventional IRL approaches that recover a deterministic reward estimate or match only expected returns, our method captures richer structure in expert behavior, particularly in learning the reward distribution, by minimizing first-order stochastic dominance (FSD) violations and thus integrating distortion risk measures (DRMs) into policy learning, enabling the recovery of both reward distributions and distribution-aware policies. This formulation is well-suited for behavior analysis and riskaware imitation learning. Theoretical analysis shows that the algorithm converges with O(ε−2) iteration complexity. Empirical results on synthetic benchmarks, real-world neurobehavioral data, and MuJoCo control tasks demonstrate that our method recovers expressive reward representations and achieves state-of-the-art performance.

## 1. Introduction

Inverse Reinforcement Learning (IRL) aims to infer an expert’s underlying reward function and policy from observed trajectories collected under unknown dynamics. IRL has been successfully applied in diverse domains, including robotics (Vasquez et al., 2014; Wu et al., 2024a), animal behavior modeling (Ashwood et al., 2022; Ke et al., 2025), autonomous driving (Rosbach et al., 2019; Wu et al., 2020), and fine-tuning of large language models (Zeng et al., 2025). A pioneering work in this field, the Maximum Entropy IRL (MaxEntIRL) framework (Ziebart et al., 2008), formulates reward learning as a likelihood optimization problem and

1School of Computational Science and Engineering, Georgia Institute of Technology, Atlanta, USA 2George W. Woodruff School of Mechanical Engineering, Georgia Institute of Technology, Atlanta, USA. Correspondence to: Feiyang Wu <feiyangwu@gatech.edu>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

interprets expert policies as Boltzmann distributions over returns. Follow-up works have extended this framework to improve reward inference stability and generalization (Arora & Doshi, 2021; Garg et al., 2021; Zeng et al., 2022).

Despite these advances, most IRL methods assume that the expert’s reward function is deterministic, thereby recovering only a point estimate, i.e., r(s, a) ∈R for every state s and action a. This assumption, however, limits expressiveness in real-world settings where reward signals are inherently stochastic. For instance, in robotic manipulation tasks involving deformable or fragile objects (Yin et al., 2021), contact uncertainty introduces reward variability for identical state-action pairs–variability that directly influences the learned policy’s robustness and safety. Similarly, in neuroscience, dopaminergic activity has been shown to act as a reward-related teaching signal that shapes animal behavior via RL-like mechanisms (Markowitz et al., 2023). Yet, dopamine signals exhibit significant trial-to-trial varia- tions, suggesting that behavior may arise from an underlying stochastic reward distribution. These challenges are further amplified in offline IRL settings, where interaction with the environment is unavailable, and the algorithm must fully rely on fixed demonstrations.

These examples highlight that in many real-world scenarios, demonstrations may be generated under stochastic reward functions, i.e., r(s, a) is a random variable. This motivates the need to go beyond point estimates and instead recover the full distribution of rewards. Prior works such as Bayesian IRL (BIRL) methods infer a posterior over reward parameters using Markov chain Monte Carlo (MCMC) (Ramachandran & Amir, 2007), maximum a posteriori (MAP) estimation (Choi & Kim, 2011), or variational inference (Chan & van der Schaar, 2021), but primarily capture uncertainty over the parameters of a deterministic reward function. Their policy likelihoods or optimality models are still driven by expected-return quantities, such as soft optimal Q-values, rather than by the full reward-induced return distribution. Consequently, higher-order reward structure can be invisible to the objective: two reward distributions with the same mean can induce the same expectation-level signal while differing substantially in variance, skewness, or tail behavior.

However, it remains unclear how to effectively learn reward arXiv:2510.03013v4 [cs.LG] 27 May 2026

<!-- Page 2 -->

Distributional Inverse Reinforcement Learning distributions directly from expert demonstrations. A natural alternative is to compare return distributions using statistical distances such as Wasserstein distance. Such distances are useful for matching two distributions, but they do not by themselves encode the IRL preference relation that the expert should be better than the learner under the recovered reward. In other words, distribution matching and distributional ordering are distinct requirements. Consequently, a principled framework is needed to lift the expert-preference condition from expected returns to full return distributions while simultaneously supporting return-distribution estimation in the offline IRL setting.

To this end, we introduce Distributional Inverse Reinforcement Learning (DistIRL), a novel framework that explicitly models both the distributional nature of reward and the return. This allows us to capture stochasticity not only from transitions and policies but also from the reward function itself. Specifically, for reward learning, instead of matching expected returns as in MaxEntIRL, we propose to compare full return distributions using a First-order Stochastic Dominance (FSD) criterion. This allows us to capture not only the mean but also higher-order moments of the return distribution and thus capture the full landscape of reward distributions, leading to a richer and more faithful estimate of the underlying reward structure. To the best of our knowledge, this is the first offline IRL framework to learn full reward distributions in a principled manner while also learning distribution-aware policies.

It is important to note that while our framework incorporates risk-sensitive policy learning, risk sensitivity primarily serves as a mechanism that enables robust reward distribution learning in the offline IRL setting. The connection is explained in detail in Sec. 4.2. Our contributions in this paper are summarized as follows: (1) Reward Distribution Learning. We propose an intuitive framework for learning reward distributions in the offline IRL setting. With an FSD objective emphasizing the entire distribution, we are able to learn reward distributions beyond the first moment. (2) Distribution-aware Policy Learning. Our algorithm learns the return distribution and recovers the distributionaware policy, extending the modeling capability of IRL frameworks towards a broader range of behavior analyses and facilitating imitation learning in risk-sensitive scenarios. (3) Theoretical Analysis. We develop a convergence-rate analysis for the proposed algorithm for solving DistIRL, showing that the algorithm converges with O(ε−2) iteration complexity. (4) Empirical Validation. We demonstrate that our method recovers meaningful reward distributions on synthetic and real-world datasets, including neurobehavioral data. Our algorithm also achieves state-of-the-art performance on highdimensional robotic control tasks in offline IRL settings.

## 2. Related Work

Inverse Reinforcement Learning Traditional offline IRL algorithms recover a reward function by matching expert feature expectations or maximizing an entropy-regularized likelihood. Apprenticeship learning (Abbeel & Ng, 2004) and maximum entropy / maximum causal entropy IRL (Ziebart et al., 2008; 2010; Gleave & Toyer, 2022) infer a deterministic reward whose induced policy reproduces expert behavior in expectation. Subsequent deep IRL and imitation-learning variants incorporate neural function approximators or adversarial objectives (Ho & Ermon, 2016; Jeon et al., 2018; Wulfmeier et al., 2015; Ni et al., 2021; Garg et al., 2021; Zeng et al., 2022; Viano et al., 2021; Bloem & Bambos, 2014; Wu et al., 2024b; Zhan et al., 2026). Several of these methods require online interaction with a simulator or a learned dynamics model during training, which is undesirable or infeasible in strictly offline settings such as modeling animal behavior from fixed recordings. Recent offline or model-based IRL approaches (Zeng et al., 2023; Kostrikov et al., 2019) reduce this dependence, but still operate primarily through deterministic rewards or expectation-level matching. Finally, while recent work has explored riskaware policy learning within the IRL framework (Singh et al., 2018; Lacotte et al., 2019; Cheng et al., 2023; Bashiri et al., 2021), these approaches do not infer a stochastic reward distribution itself. We show a detailed comparison across modeling assumptions in Appendix A.

Bayesian Inverse Reinforcement Learning Bayesian IRL (BIRL) methods infer a posterior distribution over reward parameters to quantify uncertainty in reward estimation. Ramachandran and Amir (Ramachandran & Amir, 2007) introduce Bayesian IRL using MCMC to sample from a reward posterior under a Boltzmann-rationality likelihood. Follow-up works use related frameworks to handle larger state spaces and richer reward priors (Choi & Kim, 2011; Levine et al., 2011; Chan & van der Schaar, 2021; Li et al., 2023). Although these methods capture parameter uncertainty, they still rely on expected-return optimality models and do not exploit the full reward-induced return distribution. In continuous action spaces, exact Boltzmann likelihoods can also be difficult to normalize or differentiate. In contrast, we propose a scalable algorithm for learning full reward distributions through a variational distributional objective.

Distributional Reinforcement Learning DistRL extends classical value-based methods by modeling the full distribution of returns rather than only their expectation. Early work, such as Categorical DQN (C51) (Bellemare et al., 2017) and Quantile Regression DQN (QR-DQN) (Dabney et al., 2018b), demonstrates that learning a distributional critic improves stability and sample efficiency. More recent

<!-- Page 3 -->

Distributional Inverse Reinforcement Learning advances include Implicit Quantile Networks (IQN) (Dabney et al., 2018a), Implicit Q-Learning (Kostrikov et al., 2021), Multivariate Distribution RL (Wiltzer et al., 2024), and diffusion processes for RL (Hansen-Estruch et al., 2023; Li et al., 2024). Standard DistRL still typically optimizes expected return after learning a distributional critic. Risksensitive extensions (Lim & Malik, 2022; Schneider et al., 2024) optimize risk measures such as CVaR, showing that policies can be shaped by emphasizing specific regions of the return distribution. Related work also studies policy families for multiple or variable risk measures, including distributional Pareto-optimal multi-objective RL (Cai et al., 2023) and risk-conditioned RL (Yoo et al., 2024). These directions are complementary to ours: they adapt forward RL policies to risk preferences, whereas DistIRL infers a reward distribution from demonstrations.

Recent imitation-learning work also studies matching the expert’s return distribution directly (Lazzati & Metelli, 2026). This is an important adjacent direction, but it assumes a known reward in its main formulation and targets returndistribution matching for policy learning. Our problem is different: the reward is unknown, and the central object to infer is the reward distribution itself. IRL counterparts using distributional critics (Lee et al., 2022; Karimi & Ebadzadeh) remain limited in scope because they still assume deterministic reward functions and follow a MaxEntIRL-style mean-matching blueprint.

θ1 = F −1

X (τ1)

Sample Space of Returns (quantiles)

τ1 τ2 τ3 τ4

Probability Space (fractions)

FX(z)

FY(z)

FSD Violation

**Figure 1.** Illustration of quantile functions and first-order stochastic

dominance (FSD).

## 3. Preliminaries

We model the environment as a discounted Markov Decision Process (MDP) (S, A, P, r, γ), where S denotes the state space, A the action space, P(s′|s, a) the transition kernel, and γ ∈[0, 1) the discount factor. The reward function is a (integrable) random variable r: (Ω, F, P) →(R, B(R)), so that for each state–action pair (s, a), the reward r(s, a) induces a probability distribution over (R, B(R)). Here Ωis the sample space, F is a σ-algebra of events, P is the probability measure, and B(R) denotes the Borel σ-algebra on R. A policy π(a|s) generates a trajectory (s0, a0, s1, a1,...), and the return is the random variable

Zπ = P∞ t=0 γt r(st, at).

## 3.1. Maximum Entropy IRL

Given demonstrations {(st, at)}t≥1 collected by an unknown expert policy πE, MaxEntIRL (Ziebart et al., 2008) aims to recover the unknown policy, and the corresponding reward function r the policy is optimized to. Specifically, we consider the following formulation (Ho & Ermon, 2016):

max π min r Edπ[r(s, a)]−EdπE [r(s, a)]+H(π)+ψ(r), (1)

where dπ(s, a) = (1 −γ) P∞ t=0 γt Pr(st = s)π(a|s) denotes the discounted state-action occupancy measure induced by π, H:= Edπ[−log π(a|s)] denotes the entropy, and ψ is a general convex regularizer. This formulation reduces to MaxEntIRL if ψ = 0. If ψ is instantiated as a KL penalty between a reward posterior approximation q and a prior p0, it resembles the regularized Bayesian objective used in BIRL-style formulations, while the optimal policy still follows a Boltzmann distribution of the action-values.

## 4. Distributional Inverse Reinforcement Learning Framework

In our model, we treat the reward as a distribution rather than a deterministic function. During optimization, the first two terms in Eq. 1, Edπ[r(s, a)] −EdπE [r(s, a)], enforce mean dominance–that is, the learned reward should make the expert no worse than the learned policy in expected return. At optimality, this difference becomes zero, indicating mean matching between expert and agent returns. However, if the reward is inherently a distribution, mean matching alone fails to capture the relationship between the expert’s return distribution and the agent’s in its entirety. This leads to a loss of higher-order information in the reward. To accurately model the full reward distribution, we must impose a distributional form of dominance during optimization, ensuring that the entire return distribution is aligned at optimality, not just the mean. We therefore define an ordering over entire distributions.

Definition 4.1 (First-Order Stochastic Dominance (FSD) (Hadar & Russell, 1969)). Let X and Y be real-valued integrable random variables with cumulative distribution functions FX and FY. We say that X first-order stochastically dominates Y, written as X ⪰FSD Y, if FX(z) ≤ FY (z), ∀z ∈R.

The concept of FSD is illustrated in Fig. 1. If we aim for X ⪰FSD Y, then the shaded region indicates a violation of this condition. FSD has an equivalent definition relating to utility functions, which further implies mean dominance.

<!-- Page 4 -->

Distributional Inverse Reinforcement Learning

Proposition 4.2 (Theorem 1-2 (Hadar & Russell, 1969)). For real-valued X and Y, the following are equivalent:

1. FX(z) ≤FY (z) for all z ∈R.

2. E[ u(X) ] ≥E[ u(Y) ] for every non-decreasing utility function u: R →R.

Corollary 4.3 (Mean Dominance). If X ⪰FSD Y, it follows that E[X] ≥E[Y ], as the identity utility u(x) = x is nondecreasing.

We model the reward as a conditional distribution, rt ∼ qϕ(·|st, at), and define the random return for a trajectory (s0, a0,...) sampled from policy π as Zπ = P∞ t=0 γtrt. We now introduce the distributional counterpart to Eq. 1, the objective for distributional IRL, expressed as max π min r L(π, r):= max π min r

Z ∞

−∞

[FZE(z) −FZπ(z)]+dz

+ H(π) + ψ(r), (2)

where ZE is the return distribution of the expert policy.

## 4.1. Learning Reward through Stochastic Dominance

From Eq. 2, the objective of the reward function is min r {LFSD(π, r) + ψ(r)} = min r

Z ∞

−∞

[FZE(z) −FZπ(z)]+dz + ψ(r)

.

This objective minimizes the violation of FSD, drawing inspiration from the Kolmogorov-Smirnov (K-S) test (Massey Jr, 1951). To model the reward distribution in a principled manner, we treat LFSD(π, r) as an energy function that scores how compatible a proposed reward r is with the expert demonstrations. In particular, we define a likelihood function over the expert demonstrations D using the Energy-Based Model (EBM) formulation (LeCun et al., 2006): p(D|r) ∝exp (−LFSD(π, r)), so that reward functions that yield small FSD violations are exponentially more likely under the expert data. This construction is natural here because FSD does not provide an explicit probabilistic model, but does provide a calibrated energy landscape that reflects goodness-of-fit. A more detailed discussion can be found in Appendix B.3.

We also introduce a prior distribution p0(r), which reflects our initial belief before observing any data. The goal is to infer the posterior distribution p(r|D) using Bayes’ rule. As direct inference under the EBM formulation is generally intractable, we adopt the variational inference framework (Blei et al., 2017) by introducing a variational reward distribution qϕ(r|s, a), parameterized by ϕ, to approximate the posterior and optimize the evidence lower bound

(ELBO):

Eqϕ(r|s,a) [log p(D|r)] −KL (qϕ(r|s, a) ∥p0(r)).

Substituting the energy-based likelihood into it yields:

Lr(ϕ):= Eqϕ(r|s,a) [LFSD(π, r)] + KL (qϕ(r)∥p0). (3)

Notice the natural relationship between KL and ψ. Formally, we learn the reward distribution by solving Eq. 3. To compute the gradient of the first term, we apply the Inverse Transform Sampling technique (Devroye, 2006). We use the empirical quantile to approximate the quantile of the return. Specifically, using the change of variable formula and the relation between CDF and quantile, we have

R ∞

−∞[FZE(z) −

FZπ(z)]+dz =

R 1

0

F −1

Zπ (v) −F −1

ZE(v)

+ dv. We provide a short proof of the above relation in Appendix C.1. To approximate F −1

Zπ, we draw N samples {zn} by Monte Carlo sampling zn = P∞ t=0 γtrt, rt ∼qϕ(·|st, at), and form the empirical quantile using sorted order statistics z(1) ≤· · · ≤z(N), with F −1

Zπ (k/N) ≈z(k). As a result, minimizing Lr(ϕ) generalizes the usual IRL objective of matching expected returns by aligning higher-order moments.

## 4.2. Risk-aware Policy Learning

Once the inner minimization over r yields a fixed reward distribution, the policy, parameterized by φ, is updated by maximizing the following objective:

Lπ(φ) =

Z 1

0 [F −1

Zπφ (v) −F −1

ZE(v)]+dv + H(πφ). (4)

Define I(v):= 1F −1

Zπφ (v)≥F −1

ZE (v). Fig. 1 shows that I(v) takes the value 1 in regions where FSD is violated (shaded area), and 0 otherwise. We then rewrite the objective in Eq. 4 as

Z 1

0

F −1

Zπφ (v) −F −1

ZE(v)

I(v)dv + H(πφ). (5)

Note that the indicator function I depends on the current policy, the expert policy, and the quantile level v. Conceptually, I assigns weight only to regions of the return distribution where FSD is violated. The policy now aims to increase these FSD violations—encouraging the agent to obtain higher return samples in those regions. This leads to a maximization scheme that is inherently risk-aware, as it requires reasoning over the full return distribution rather than just its expectation.

Unfortunately, directly optimizing Eq. 4 is intractable, as the indicator function I is not observable during training. To

<!-- Page 5 -->

Distributional Inverse Reinforcement Learning address this, we take a broader perspective on risk-aware policy learning and propose replacing I(v) with a risk measure that retains the goal of encouraging risk-sensitive behavior while yielding a tractable objective. Furthermore, we show that the resulting surrogate objective provides a weaker form of optimality, but under certain conditions, it can theoretically achieve the same optimum as Eq. 4. To present our new objective, we need a few essential concepts.

Definition 4.4 (Distortion function). A distortion function ξ is a non-decreasing function ξ: [0, 1] →[0, 1] such that ξ(0) = 0, ξ(1) = 1.

Definition 4.5 (Distortion Risk Measure (DRM) (Dhaene et al., 2012)). For an integrable random variable X, and a distortion function ξ, a Distortion Risk Measure Mξ is defined as Mξ(X) =

R 1

0 F −1 X (v)d˜ξ(v) where ˜ξ = 1−ξ(1− v) ≥0 is the dual distortion function.

Common examples of DRMs and distortion functions are listed in Table 5. These measures offer various ways to quantify risk based on the return distribution. When d˜ξ admits a density, the resulting DRM is often called a spectral risk measure; in the paper we use the broader term DRM. Intuitively, when ˜ξ is concave, it places greater emphasis on lower returns, thereby encouraging risk-averse behavior. To induce risk-aware policies using distortion ξ(v), we maximize the DRM defined in Def. 4.5. In all main experiments, ξ is fixed within each run; unless otherwise stated, we use CVaR with risk parameter 0.05, with additional DRM choices studied in Appendix E.1.

Building on the above definitions, we propose replacing I(v) with ˜ξ(v) in Eq. 5, resulting in: maxφ

R 1

0

F −1

Zπ (v) −F −1

ZE(v)

d˜ξ(v) + H(π) = maxφ

R 1

0 F −1 Zπ (v)d˜ξ(v) + H(π). The equality holds because the expert policy does not depend on φ. We denote the final objective as

Lπ(φ) =

Z 1

0 F −1

Zπφ (v)d˜ξ(v) + H(πφ), (6)

where Mξ is a chosen DRM with a distortion function ξ.

Relation to Eq. 4. Additionally, we know that X ⪰FSD Y ⇒Mξ(X) ≥Mξ(Y) (Sereda et al., 2010). A natural question is which conditions are sufficient for FSD. We observe that the converse requires stronger conditions.

Proposition 4.6. Mξ(X) ≥Mξ(Y) for every distortion function ξ implies X ⪰FSD Y.

The proof is straightforward by observing that Mξ(X) − Mξ(Y) =

R 1

0 (F −1 X (v) −F −1

Y (v))d˜ξ(v) and the fact that ˜ξ(v) ≥ 0. We present a short proof in Appendix C.1. This implies that if we solve maxπφ

R 1

0

F −1

Zπφ(v) −F −1

E (v)

d˜ξ(v) + H(πφ) for every distortion function, we obtain the solution to Eq. 4. However, since optimizing over all utility conditions is intractable, our proposed objective serves as an approximation using a specific DRM. Nonetheless, under the conditions of the proposition, this surrogate objective can theoretically achieve the same optimality as Eq. 4.

## 4.3. Practical Algorithm

## Algorithm

## 1 A DistIRL method with FSD objective Input:

Expert data D = {(sE t, aE t)}, prior p0(r), risk measure ξ, step sizes ηθ, ηφ, ηϕ

Output: Reward distribution qϕ(r|s, a); policy πφ(a|s)

1 Initialize parameters of reward network ϕ, policy φ, and critic θ

2 for k = 1 to K do

3 Sample a mini-batch {(sE t, aE t)} from D

4 foreach (sE t, aE t) in mini-batch do

For each sE t, sample at ∼ πφ(·|sE t), rt ∼ qϕ(·|sE t, at), rE t ∼qϕ(·|sE t, aE t)

6 Compute return samples Zπk, ZE Critic update via quantile regression (Eq. 10): θk+1 ← θk − ηθ∇LQR(θk)

7 Policy update with distortion risk measure (Eq. 6):

φk+1 ←φk + ηφ∇Lπ(φk)

8 Reward distribution update via FSD loss (Eq. 3):

ϕk+1 ←ϕk −ηϕ∇Lr(ϕk).

To enable tractable and expressive modeling of reward uncertainty, we parameterize the reward distribution qϕ(r|s, a), for example, using Azzalini’s skew-normal distribution (Azzalini & Valle, 1996): qϕ(r|s, a) = SN(µϕ(s, a), σ2 ϕ(s, a); αϕ(s, a)), where the mean µϕ(s, a), standard deviation σϕ(s, a), and skew parameter αϕ(s, a) are outputs of a neural network with parameters ϕ. This choice allows for efficient sampling and computing regularization when using a standard normal prior. During training, for each state-action pair, we sample rewards rt ∼qϕ(·|st, at) to construct return samples for both the expert and the current policy.

Note that the choice of prior depends heavily on the task domain and the type of variability we expect in the reward signal. This prior sensitivity is shared with Bayesian IRL methods: an informative prior can help when domain knowledge is reliable, while a poor prior can bias the learned reward distribution. For example, skew-normal distributions can capture asymmetric reward uncertainty in tasks with systematic biases (e.g., contact-rich manipulation), whereas heavy-tailed priors may be more suitable when outliers or rare but significant events dominate the return structure. In

<!-- Page 6 -->

Distributional Inverse Reinforcement Learning contrast, the broader statistical learning community often defaults to Gaussian priors, primarily because of their analytical tractability, conjugacy with many likelihood models, and well-understood concentration properties. That said, DistIRL does not rely on a fixed distributional assumption. Any parameterized distribution pθ whose log-density or quantile function is differentiable in θ is compatible with our framework, since the algorithm only requires gradients.

To estimate the DRM Mξ(Zπ) for the policy, we follow an offline approach: we use states st drawn from the expert demonstration dataset, but sample actions aπ t ∼πθ(·|st) from the current policy, and a reward rt ∼qϕ(·|st, aπ t). Then we compute the return Zπ by taking the sum. For policy update, we first learn the critic by Off-policy Evaluation (OPE) (Sutton et al., 1998) on (st, at, rt, st+1, aπ t+1) where we use Quantile Regression with the Quantile Huber loss LQR as in Eq. 10. We then update the risk-aware policy by solving minπ KL π(·|s)

1

Z exp {Mξ(Zπ(·|s))}

, which corresponds to the KKT solution to Eq. 4, as originally introduced by Ziebart et al. (2008). We summarize the full procedure in Alg. 1.

## 5. Theoretical Results

In this section, we provide a theoretical analysis of the algorithm proposed above. The analysis fixes a distortion function ξ throughout the run and studies the idealized update in which the corresponding DRM policy-improvement step is solved exactly. For a reward parameter ϕ and policy π, let Qξ ϕ,π denote the risk-sensitive critic induced by the nested DRM Bellman operator. Let π⋆ ϕ denote the DRMoptimal policy for the reward distribution qϕ, and define the critic tracking error

Ek =

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞.

The stepsize exponent σ ∈(0, 1) controls the reward-update stepsize schedule. First, we introduce several regularity assumptions, the necessity of which is detailed in the appendix C.2.

Assumption 5.1. There exists Rmax < ∞such that

|qϕ(s, a)| ≤Rmax almost surely for all (s, a, ϕ). (7)

Assumption 5.2. For every (s, a) and all ϕ1, ϕ2 ∈Rd, the reward laws satisfy

W∞ qϕ1(·|s, a), qϕ2(·|s, a)

≤LR ∥ϕ1 −ϕ2∥, (8)

where W∞denotes the Wasserstein infinity distance. Equivalently, one can couple qϕ1(s, a) and qϕ2(s, a) such that |qϕ1(s, a) −qϕ2(s, a)| ≤LR ∥ϕ1 −ϕ2∥ almost surely.

We use the following assumption on a given DRM. Standard normalized DRMs satisfy these properties.

Assumption 5.3. For each state-action pair s ∈S, a ∈A, the one-step distortion risk measure Mξ(·|s, a) is

1. monotone: X ≤Y a.s. implies Mξ(X|s, a) ≤ Mξ(Y |s, a);

2. translation-equivariant: Mξ(X + c|s, a) = Mξ(X|s, a) + c for all c ∈R;

3. 1-Lipschitz in ∥·∥∞: for all bounded random variables X, Y,

Mξ(X|s, a) −Mξ(Y |s, a)

≤∥X −Y ∥∞.

First, we show that the critic under a given DRM converges in the average sense:

Theorem 5.4. Assume Assumptions 5.1-5.3 hold. Let Ek = Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞. Assume the reward update satisfies

Assumption C.9, with stepsizes ηk = η = η0K−σ, η0 > 0, and σ ∈(0, 1). Then running the DistIRL algorithm K steps, we have 1

K

PK k=1 Ek = O(K−1) + O(K−σ).

This gives a corresponding policy bound:

Theorem 5.5. For each k, define the learned and DRMoptimal policies induced by the current Q-functions:

πk(·|s)∝exp

Qξ ϕk,πk(s, ·)

, π⋆ ϕk(·|s)∝exp

Qξ ϕk,π⋆ ϕk(s, ·)

.

Then, running the DistIRL algorithm K steps, we have

1 K

PK k=1 ∥log πk −log π⋆ ϕk∥∞= O(K−1) + O(K−σ).

Finally, we obtain a rate of convergence towards a first-order stationary point:

Theorem 5.6. Suppose Assumptions 5.1, 5.2, C.9, and C.11 hold. Let ηk = η0k−σ with η0 > 0 and σ ∈(0, 1), and assume Lr is bounded below on Φ. Then there exists C > 0 such that

1 K

K−1 X k=0

E∥∇Lr(ϕk)∥2 =O

K−1

+O

K−σ

+O

K−1+σ

.

In particular, picking σ = 1/2, we obtain a O(ε−2) iteration bound for the algorithm to reach an ε-stationary point in averaged squared gradient norm. This rate characterizes the alternating DistIRL objective under our assumptions.

## 6. Experiment

## 6.1. Gridworld

We begin with a 5 × 5 gridworld environment where the agent is trained to navigate from the starting state (2, 0) (left-center) to rewarding goal locations. Two high-reward states are placed at (0, 4) (top-right) and (4, 4) (bottomright), with the top-right reward modeled as a stochastic

<!-- Page 7 -->

Distributional Inverse Reinforcement Learning

True mean DistIRL mean BIRL mean

True var DistIRL var BIRL var

**Figure 2.** Inferring reward mean and variance in the gridworld

example with 10 demonstrations.

outcome drawn from N(1, 1). The first column of Fig. 2 illustrates the ground-truth reward mean and variance.

This setup mimics an animal exploring an arena with two reward ports. In such compact environments, animals often display risk-averse behavior, i.e., avoiding locations where rewards have previously failed to appear (Mobbs et al., 2018; Daw et al., 2006). To model this, we collect 10 trajectories from a risk-averse agent trained under stochastic rewards. In 9 out of 10 episodes, the agent chooses the more reliable bottom-right goal. We then apply our DistIRL method to recover the full reward distribution. As shown in Fig. 2, using a symmetric Gaussian reward estimator combined with risk-averse policy learning, our approach not only identifies both high-reward states but also captures the variance at the top-right goal. This highlights the model’s ability to infer higher-order moments of the reward from expert demos.

As a baseline, we evaluate Bayesian IRL (BIRL) (Chan & van der Schaar, 2021; Mandyam et al., 2023; Bajgar et al., 2024). BIRL is a widely used framework that assumes a reward distribution but learns it by matching only the mean, without capturing the full distributional structure. We select BIRL because it is the method most comparable to ours in its ability to recover a reward distribution. BIRL reasonably recovers the mean reward but produces spurious high estimates in the lower-left corner. Furthermore, it fails to capture reward variance, emphasizing the need to enforce distance over the full distribution. Simply specifying a reward distribution, without integrating distribution-aware learning, fails to capture the true variance of the rewards.

## 6.2. Mouse Spontaneous Behavior

We apply our framework to a neuroscience dataset in which mice freely explore an arena without explicit rewards (Markowitz et al., 2023). Behavior was recorded using a depth camera, and the raw trajectories were converted into sequences of discrete syllables (e.g., grooming, sniffing). We model these trajectories with an MDP, treating each syllable as a state and the next syllable as the action, yielding ten states and ten actions. In total, we analyzed 159 such state-action sequences. The dataset also includes a time-aligned one-dimensional trace of dopamine fluctuations from the dorsolateral striatum. Prior work (Markowitz et al., 2023) showed that using dopamine as a reward enabled a simulated RL agent to reproduce observed transitions, suggesting IRL should recover a reward pattern resembling dopamine. Since dopamine varies even within the same state-action pair, the prior study used only its mean for simplicity. Here, we compare rewards learned under deterministic vs. distributional assumptions to assess how well they capture both the mean and the full distribution of dopamine signals.

We use both Azzalini’s skew-normal distribution (denoted “S-”) and the symmetric Gaussian as reward models for both

DistIRL and BIRL. Fig. 3A) and B) show two example state-action pairs, illustrating the true dopamine fluctuation distribution alongside the estimated reward distributions from four methods. The assumption of a parameterized reward distribution is motivated by prior findings in computational neuroscience: dopamine-related reward signals in rodents are well known to exhibit asymmetric, left-skewed variability. For this reason, we chose a skew-normal family, which captures exactly this type of asymmetric structure while remaining interpretable. For each case, we display both the probability density function and the CDF, along with the corresponding means. Deterministic rewards (Det) are shown as pink dashed lines in the density plots. Among all methods, S-DistIRL most accurately recovers the shape of the dopamine distribution, which is often right-skewed and multimodal. Its estimated mean also closely matches both the true mean and the deterministic estimate.

We also quantify the similarity between estimated rewards and actual dopamine distributions. In Fig. 4A), we report the correlation between the mean of dopamine fluctuations and the mean of the estimated reward across all mice and trajectories. Deterministic reward models yield moderate correlation, while DistIRL improves upon this, with S-DistIRL achieving the highest correlation overall. This finding indicates that incorporating full reward distributions, using suitable skewed distributional models, is essential for IRL to capture biologically meaningful reward signals. Fig. 4B) shows that, compared to BIRL, S-DistIRL also achieves a lower Wasserstein-1 distance between the estimated reward distribution and the actual dopamine distribution, indicating better alignment of the shape. Taken together, both qualitative examples and quantitative metrics support that modeling skewed reward distributions significantly enhances the ability to track dopamine fluctuations.

This result suggests that reward structure can be inferred directly from behavior data under appropriate modeling as-

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-distributional-inverse-reinforcement-learning/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

Distributional Inverse Reinforcement Learning

S-DistIRL

DistIRL

S-BIRL

BIRL

Det

True

S-DistIRL

DistIRL

S-BIRL

BIRL

True

S-DistIRL

DistIRL

S-BIRL

BIRL

Det

True

S-DistIRL

DistIRL

S-BIRL

BIRL

True A) B)

**Figure 3.** Learned reward distribution versus recorded dopamine signals and their empirical CDFs.

S-DistIRL

DistIRL

S-BIRL

BIRL

Det

Correlation

Wasserstein-1

S-DistIRL

DistIRL

S-BIRL

BIRL

A) B)

**Figure 4.** Left: Pearson correlation of the reward mean and dopamine level. Right: W-1 loss between learned distribution and dopamine level.

sumptions. While it is known that dopamine neurons encode reward-related signals (Schultz et al., 1997; Markowitz et al., 2023), our experiment shows not only a nontrivial correlation between the inferred and measured mean rewards (with a correlation around 0.3), but also that the full reward distribution recovered from behavior reasonably resembles the distribution of dopamine fluctuations. This suggests that detailed features of neuromodulatory signals, such as the variability in dopamine release, can be decoded from behavior alone, highlighting the potential of inverse modeling to uncover internal motivational states and their neural substrates.

## 6.3. MuJoCo Benchmarks

Risk-sensitive D4RL. In earlier experiments, we applied DistIRL to discrete state-action MDPs and compared it with BIRL. Here we extend the study to continuous MDPs to demonstrate DistIRL’s scalability and generalizability. We evaluate our method on Risk-sensitive D4RL benchmarks, following the reward formulations introduced in recent robustness studies (Urp´ı et al., 2021). Specifically, the reward functions incorporate stochastic penalties triggered by safety-related conditions: (1) Half-Cheetah: Rt(s, a) = ¯rt(s, a) −70Iν>¯ν · B0.1, where ¯rt(s, a) is the environment reward, ν is the forward velocity, and ¯ν is a velocity threshold (¯ν = 4 for the medium variant and ¯ν = 10 for the easy variant). This penalty models rare but catastrophic robot failures at high speed. (2) Walker2D/Hopper: Rt(s, a) = ¯rt(s, a)−pI|θ|>¯θ·B0.1, where ¯rt(s, a) is the environment reward, θ is the pitch an- gle, ¯θ is a task-dependent threshold (0.5 for Walker2D-M/E and 0.1 for Hopper-M/E), and p is the penalty magnitude (30 for Walker2D and 50 for Hopper).

We train expert agents on these stochastic reward formulations using Risk-averse Distributional SAC, a variant of DSAC (Duan et al., 2021) with a CVaR objective, and collect 10 demonstration trajectories. We then evaluate DistIRL against several state-of-the-art baselines. Results are averaged over 5 random seeds. We use a standard normal as the prior due to its general applicability when the underlying true reward distribution is unknown.

**Table 1.** shows that our method consistently outperforms other offline IRL baselines under stochastic reward settings. For reward parameterization, we use a Gaussian distribution (denoted as DistIRL) and a quantile-function parameterization (denoted as DistIRL-qtr, short for QuanTile Reward). Popular online methods such as GAIL (Ho & Ermon, 2016) are not directly applicable in this offline setting. Offline ML-IRL (Zeng et al., 2023) is a model-based MaxEntIRL method that relies on a separately trained transition model using additional non-expert data. Its poor performance here is expected: the transition model was pretrained under riskneutral rewards and does not align with the new expert data generated under risk-sensitive objectives, leading to severe distribution mismatch. ValueDICE (Kostrikov et al., 2019), a model-free offline MaxEntIRL baseline, also underperforms since it optimizes with respect to expected risk-neutral returns, while our experts follow risk-averse behavior. Behavior Cloning (BC) achieves moderately strong results, as it simply mimics the demonstrated actions without explicitly optimizing for either risk-neutral or risk-sensitive objectives. However, its performance is limited as the model overfits.

**Table 1.** D4RL performance averaged over 5 seeds.

## Method

HalfCheetah Hopper Walker2d

DistIRL (ours) 3469 ± 59 886 ± 1 1526 ± 148 DistIRL-qrt (ours) 3294 ± 172 747 ± 79 1211 ± 182 Offline ML-IRL 826 ± 231 192 ± 56 240 ± 50 ValueDICE 1259 ± 78 260 ± 10 798 ± 311 BC 2828 ± 281 346 ± 1 1321 ± 26 Expert 3540 ± 44 892 ± 3 1478 ± 200

<!-- Page 9 -->

Distributional Inverse Reinforcement Learning

Return

0.0

0.2

0.4

0.6

0.8

1.0

CDF

Expert DistIRL BIRL

**Figure 5.** Return distributions comparison in HalfCheetah.

To further validate the fidelity of our inferred return distributions from DistIRL and compare with the BIRL framework that only matches the mean, we collect 200 trajectories, sample the learned return distribution for each learned policy, and plot against the expert’s return distribution in Fig. 5. This shows that DistIRL’s reward and policy model better align with the expert. We also report a Pearson correlation coefficient of 0.92 between the mean estimated by DistIRL and the mean of the true return. This indicates strong agreement and demonstrates that our inferred reward is an accurate proxy for the true reward model. A further examination of the return distribution and its higher-order moments can be found in Appendix F. Additionally, the competitive results of quantile-based reward parameterization open the opportunity to use a broad range of parametric families, including diffusion models, and we leave this direction as a future extension.

Risk-neutral D4RL. We also test our algorithm in conventional deterministic reward settings using D4RL’s medium-expert trajectories (Fu et al., 2020). Table 2 shows that our method achieves competitive or superior performance even without tailoring to deterministic assumptions, underscoring the generality of DistIRL. We want to emphasize that Offline ML-IRL requires additional data1.

Ablation studies. We evaluate the contribution of different design choices by ablating our model under the HalfCheetah setting with right-skewed normal (SN η, η > 0) stochastic rewards and risk-averse expert policy, indicating the expert prefers conservative actions that yield more consistent rewards. Variants include: Dis/Det: Distributional or Deterministic rewards; QR/TD: Quantile Regression or TD-based critic; FSD/Mean: FSD loss or Mean matching. As shown in Table 3, which scales the performance between worst and best, using distributional rewards with FSD loss significantly outperforms mean-matching alternatives. Additionally, deterministic TD-learning with mean-matching (Det- TD-Mean) underperforms in learning risk-averse policies due to a lack of distributional supervision. This confirms

1For HalfCheetah, with the same amount of data as Offline ML-IRL, DistIRL can reach 11239 ± 539.

the effectiveness of FSD-based reward learning and risksensitive policy optimization. Note that the BIRL framework aligns with our Dis-TD-Mean configuration; RIZE (Karimi & Ebadzadeh) aligns with Det-Qt-Mean, which performs the worst; Det-TD-Mean aligns with ValueDice but with an explicit reward estimation. Thus, in this ablation study, we treat them as a specific setting within DistIRL when benchmarking against other approaches. Additionally, we conduct ablation studies on the choice of DRM in Appendix E.1, showing that DistIRL is not sensitive to a specific DRM as long as the chosen risk measure does not deviate too far from the underlying risk preference of the expert data. We also conduct experiments on the number of trajectories for the risk-sensitive D4RL dataset in Appendix E.2, which show that DistIRL is sufficiently robust in a low-data regime, indicating that our approach is computationally attractive.

**Table 2.** Performance on deterministic reward settings (D4RL).

## Method

HalfCheetah Hopper Walker2d

DistIRL (Ours) 7779 ± 228 3411 ± 42 4570 ± 305 Off. ML-IRL 11231 ± 585 3347 ± 238 4201 ± 638 ValueDICE 4935 ± 2836 3073 ± 539 3191 ± 1888 BC 623 ± 56 3236 ± 46 2822 ± 979 Expert 12175 ± 91 3512 ± 22 5384 ± 52

**Table 3.** Ablation study on model setting. Performance scaled.

Dis-Qt-Mean Det-Qt-Mean DistIRL (Ours)

0.22 ± 0.02 0.00 ± 0.01 1.00 ± 0.02

Dis-TD-FSD Dis-TD-Mean Det-TD-Mean

0.67 ± 0.31 0.33 ± 0.01 0.22 ± 0.00

## 7 Conclusion

We introduce a distributional framework for inverse reinforcement learning that jointly models reward uncertainty and return distributions. Our method enables risk-aware policy learning and accurate inference of high-order structure in demonstrations. We validate the framework on stochastic control tasks, deterministic settings, and real neural datasets, demonstrating state-of-the-art performance and strong generalization across domains. Like other IRL methods, DistIRL does not claim unique recovery of a ground-truth reward from demonstrations alone; it recovers a compatible reward distribution under the chosen prior, variational family, and FSD-based inductive bias. Future work should expand real-world validation, learn or adapt the DRM from demonstrations, study targeted finite-moment relaxations when only selected moments are scientifically important, and model correlations among state-action reward distributions.

<!-- Page 10 -->

Distributional Inverse Reinforcement Learning

Impact Statement

IRL enables powerful tools for understanding behavior, with positive applications in neuroscience, animal modeling, and AI alignment. However, it also raises ethical concerns. IRL could be misused in military settings to model or mimic adversarial behavior, or in surveillance contexts to infer personal goals without consent, posing risks to privacy and autonomy. These concerns highlight the need for careful oversight and responsible deployment.

## References

Abbeel, P. and Ng, A. Y. Apprenticeship learning via inverse reinforcement learning. In Proceedings of the twenty-first international conference on Machine learning, pp. 1, 2004.

Arora, S. and Doshi, P. A survey of inverse reinforcement learning: Challenges, methods and progress. Artificial Intelligence, 297:103500, 2021.

Ashwood, Z., Jha, A., and Pillow, J. W. Dynamic inverse reinforcement learning for characterizing animal behavior. Advances in neural information processing systems, 35:

29663–29676, 2022.

Azzalini, A. and Valle, A. D. The multivariate skew-normal distribution. Biometrika, 83(4):715–726, 1996.

Bajgar, O., Abate, A., Gatsis, K., and Osborne, M. A. Walk- ing the values in bayesian inverse reinforcement learning. arXiv preprint arXiv:2407.10971, 2024.

Bashiri, M. A., Ziebart, B., and Zhang, X. Distributionally robust imitation learning. In Ranzato, M., Beygelzimer, A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.), Advances in Neural Information Processing Systems, vol- ume 34, pp. 24404–24417. Curran Associates, Inc., 2021.

Bellemare, M. G., Dabney, W., and Munos, R. A distribu- tional perspective on reinforcement learning. In International conference on machine learning, pp. 449–458. PMLR, 2017.

Blei, D. M., Kucukelbir, A., and McAuliffe, J. D. Varia- tional inference: A review for statisticians. Journal of the American Statistical Association, 112(518):859–877, 2017.

Bloem, M. and Bambos, N. Infinite time horizon maximum causal entropy inverse reinforcement learning. In 53rd IEEE conference on decision and control, pp. 4911–4916. IEEE, 2014.

Cai, X.-Q., Zhang, P., Zhao, L., Bian, J., Sugiyama, M., and

Llorens, A. Distributional pareto-optimal multi-objective reinforcement learning. In Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., and Levine, S. (eds.), Advances in Neural Information Processing Systems, vol- ume 36, pp. 15593–15613. Curran Associates, Inc., 2023.

Chan, A. J. and van der Schaar, M. Scalable bayesian inverse reinforcement learning. arXiv preprint arXiv:2102.06483, 2021.

Cheng, Z., Coache, A., and Jaimungal, S. Eliciting risk aver- sion with inverse reinforcement learning via interactive questioning. arXiv preprint arXiv:2308.08427, 2023.

Choi, J. and Kim, K.-E. Map inference for bayesian inverse reinforcement learning. Advances in neural information processing systems, 24, 2011.

Dabney, W., Ostrovski, G., Silver, D., and Munos, R. Im- plicit quantile networks for distributional reinforcement learning. In International conference on machine learning, pp. 1096–1105. PMLR, 2018a.

Dabney, W., Rowland, M., Bellemare, M., and Munos, R.

Distributional reinforcement learning with quantile regression. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018b.

Daw, N. D., O’Doherty, J. P., Dayan, P., Seymour, B., and

Dolan, R. J. Cortical substrates for exploratory decisions in humans. Nature, 441(7095):876–879, 2006.

Devroye, L. Nonuniform random variate generation. Hand- books in operations research and management science, 13:83–121, 2006.

Dhaene, J., Kukush, A., Linders, D., and Tang, Q. Remarks on quantiles and distortion risk measures. European Actuarial Journal, 2:319–328, 2012.

Duan, J., Guan, Y., Li, S. E., Ren, Y., Sun, Q., and Cheng, B.

Distributional soft actor-critic: Off-policy reinforcement learning for addressing value estimation errors. IEEE transactions on neural networks and learning systems, 33 (11):6584–6598, 2021.

Fu, J., Kumar, A., Nachum, O., Tucker, G., and Levine,

S. D4rl: Datasets for deep data-driven reinforcement learning. arXiv preprint arXiv:2004.07219, 2020.

Garg, D., Chakraborty, S., Cundy, C., Song, J., and Ermon,

S. Iq-learn: Inverse soft-q learning for imitation. Advances in Neural Information Processing Systems, 34: 4028–4039, 2021.

Gleave, A. and Toyer, S. A primer on maximum causal entropy inverse reinforcement learning. arXiv preprint arXiv:2203.11409, 2022.

<!-- Page 11 -->

Distributional Inverse Reinforcement Learning

Gut, A. Probability: a graduate course, volume 200. Springer, 2006.

Hadar, J. and Russell, W. R. Rules for ordering uncertain prospects. The American economic review, 59(1):25–34, 1969.

Hansen-Estruch, P., Kostrikov, I., Janner, M., Kuba, J. G., and Levine, S. Idql: Implicit q-learning as an actorcritic method with diffusion policies. arXiv preprint arXiv:2304.10573, 2023.

Heil, C. Introduction to real analysis, volume 280. Springer,

2019.

Ho, J. and Ermon, S. Generative adversarial imitation learn- ing. Advances in neural information processing systems, 29, 2016.

Jeon, W., Seo, S., and Kim, K.-E. A bayesian approach to generative adversarial imitation learning. Advances in neural information processing systems, 31, 2018.

Karimi, A. and Ebadzadeh, M. M. Rize: Adaptive regular- ization for imitation learning. Transactions on Machine Learning Research.

Ke, J., Wu, F., Wang, J., Markowitz, J., and Wu, A. In- verse reinforcement learning with switching rewards and history dependency for characterizing animal behaviors. arXiv preprint arXiv:2501.12633, 2025.

Kopa, M. and ˇSm´ıd, M. Contractivity of bellman operator in risk averse dynamic programming with infinite horizon. Operations Research Letters, 51(2):133–136, 2023.

Kostrikov, I., Nachum, O., and Tompson, J. Imitation learn- ing via off-policy distribution matching. arXiv preprint arXiv:1912.05032, 2019.

Kostrikov, I., Nair, A., and Levine, S. Offline reinforce- ment learning with implicit q-learning. arXiv preprint arXiv:2110.06169, 2021.

Lacotte, J., Ghavamzadeh, M., Chow, Y., and Pavone, M.

Risk-sensitive generative adversarial imitation learning. In The 22nd International Conference on Artificial Intelligence and Statistics, pp. 2154–2163. PMLR, 2019.

Lazzati, F. and Metelli, A. M. Imitation learning as return distribution matching. In International Conference on Learning Representations, 2026.

LeCun, Y., Chopra, S., Hadsell, R., Ranzato, M., and Huang,

F. J. A tutorial on energy-based learning. Predicting structured data, 2006.

Lee, K., Isele, D., Theodorou, E. A., and Bae, S. Risk- sensitive mpcs with deep distributional inverse rl for autonomous driving. In 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 7635–7642. IEEE, 2022.

Levine, S., Popovic, Z., and Koltun, V. Nonlinear inverse re- inforcement learning with gaussian processes. Advances in neural information processing systems, 24, 2011.

Li, M., Zhao, X., Lee, J. H., Weber, C., and Wermter,

S. Internally rewarded reinforcement learning. In International Conference on Machine Learning, pp. 20556– 20574. PMLR, 2023.

Li, Y., Lai, C.-H., Sch¨onlieb, C.-B., Mitsufuji, Y., and Er- mon, S. Bellman diffusion: Generative modeling as learning a linear operator in the distribution space. arXiv preprint arXiv:2410.01796, 2024.

Lim, S. H. and Malik, I. Distributional reinforcement learn- ing for risk-sensitive policies. Advances in Neural Information Processing Systems, 35:30977–30989, 2022.

Mandyam, A., Li, D., Cai, D., Jones, A., and Engelhardt,

B. E. Kernel density bayesian inverse reinforcement learning. arXiv preprint arXiv:2303.06827, 2023.

Markowitz, J. E., Gillis, W. F., Jay, M., Wood, J., Harris,

R. W., Cieszkowski, R., Scott, R., Brann, D., Koveal, D., Kula, T., et al. Spontaneous behaviour is structured by reinforcement without explicit reward. Nature, 614 (7946):108–117, 2023.

Massey Jr, F. J. The kolmogorov-smirnov test for goodness of fit. Journal of the American statistical Association, 46 (253):68–78, 1951.

Mobbs, D., Trimmer, P. C., Blumstein, D. T., and Dayan,

P. Foraging for foundations in decision neuroscience: insights from ethology. Nature Reviews Neuroscience, 19 (6):419–427, 2018.

Ni, T., Sikchi, H., Wang, Y., Gupta, T., Lee, L., and Eysen- bach, B. f-irl: Inverse reinforcement learning via state marginal matching. In Conference on Robot Learning, pp. 529–551. PMLR, 2021.

Ramachandran, D. and Amir, E. Bayesian inverse rein- forcement learning. In IJCAI, volume 7, pp. 2586–2591, 2007.

Rockafellar, R. T., Uryasev, S., et al. Optimization of condi- tional value-at-risk. Journal of risk, 2:21–42, 2000.

Rosbach, S., James, V., Großjohann, S., Homoceanu, S., and

Roth, S. Driving with style: Inverse reinforcement learning in general-purpose planning for automated driving. In

<!-- Page 12 -->

Distributional Inverse Reinforcement Learning

## 2019 IEEE/RSJ International Conference on Intelligent Robots and

Systems (IROS), pp. 2658–2665. IEEE, 2019.

Ruszczy´nski, A. Risk-averse dynamic programming for markov decision processes. Mathematical programming, 125(2):235–261, 2010.

Schneider, L., Frey, J., Miki, T., and Hutter, M. Learning risk-aware quadrupedal locomotion using distributional reinforcement learning. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 11451– 11458. IEEE, 2024.

Schultz, W., Dayan, P., and Montague, P. R. A neural substrate of prediction and reward. Science, 275(5306): 1593–1599, 1997.

Sereda, E. N., Bronshtein, E. M., Rachev, S. T., Fabozzi,

F. J., Sun, W., and Stoyanov, S. V. Distortion risk measures in portfolio optimization. Handbook of portfolio construction, pp. 649–673, 2010.

Singh, S., Lacotte, J., Majumdar, A., and Pavone, M. Risk- sensitive inverse reinforcement learning via semi-and non-parametric methods. The International Journal of Robotics Research, 37(13-14):1713–1740, 2018.

Sutton, R. S., Barto, A. G., et al. Reinforcement learning:

An introduction, volume 1. MIT press Cambridge, 1998.

Urp´ı, N. A., Curi, S., and Krause, A. Risk-averse offline reinforcement learning. arXiv preprint arXiv:2102.05371, 2021.

Vasquez, D., Okal, B., and Arras, K. O. Inverse reinforce- ment learning algorithms and features for robot navigation in crowds: an experimental comparison. In 2014 IEEE/RSJ International Conference on Intelligent Robots and Systems, pp. 1341–1346. IEEE, 2014.

Viano, L., Huang, Y.-T., Kamalaruban, P., Weller, A., and

Cevher, V. Robust inverse reinforcement learning under transition dynamics mismatch. Advances in Neural Information Processing Systems, 34:25917–25931, 2021.

Wei, R., Zeng, S., Li, C., Garcia, A., McDonald, A. D., and Hong, M. A bayesian approach to robust inverse reinforcement learning. In Conference on Robot Learning, pp. 2304–2322. PMLR, 2023.

Wiltzer, H., Farebrother, J., Gretton, A., and Rowland, M.

Foundations of multivariate distributional reinforcement learning. Advances in Neural Information Processing Systems, 37:101297–101336, 2024.

Wu, F., Gu, Z., Wu, H., Wu, A., and Zhao, Y. Infer and adapt:

Bipedal locomotion reward learning from demonstrations via inverse reinforcement learning. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 16243–16250. IEEE, 2024a.

Wu, R., Chen, Y., Swamy, G., Brantley, K., and Sun, W.

Diffusing states and matching scores: A new framework for imitation learning. arXiv preprint arXiv:2410.13855, 2024b.

Wu, Z., Sun, L., Zhan, W., Yang, C., and Tomizuka, M. Effi- cient sampling-based maximum entropy inverse reinforcement learning with application to autonomous driving. IEEE Robotics and Automation Letters, 5(4):5355–5362, 2020.

Wulfmeier, M., Ondruska, P., and Posner, I. Maximum en- tropy deep inverse reinforcement learning. arXiv preprint arXiv:1507.04888, 2015.

Yin, H., Varava, A., and Kragic, D. Modeling, learning, perception, and control methods for deformable object manipulation. Science Robotics, 6(54):eabd8803, 2021.

Yoo, G., Park, J., and Woo, H. Risk-conditioned reinforce- ment learning: A generalized approach for adapting to varying risk measures. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 16513– 16521, 2024.

Zeng, S., Li, C., Garcia, A., and Hong, M. Maximum- likelihood inverse reinforcement learning with finite-time guarantees. Advances in Neural Information Processing Systems, 35:10122–10135, 2022.

Zeng, S., Li, C., Garcia, A., and Hong, M. When demon- strations meet generative world models: A maximum likelihood framework for offline inverse reinforcement learning. Advances in Neural Information Processing Systems, 36:65531–65565, 2023.

Zeng, S., Liu, Y., Rangwala, H., Karypis, G., Hong, M., and Fakoor, R. From demonstrations to rewards: Alignment without explicit human preferences. arXiv preprint arXiv:2503.13538, 2025.

Zhan, S. S., Wang, P., Wu, Q., Wang, Y., Jiao, R., Huang, C., and Zhu, Q. Enhancing inverse reinforcement learning through encoding dynamic information in reward shaping. In 8th Annual Learning for Dynamics & Control Conference (L4DC), 2026.

Ziebart, B. D., Maas, A. L., Bagnell, J. A., Dey, A. K., et al.

Maximum entropy inverse reinforcement learning. In Aaai, volume 8, pp. 1433–1438. Chicago, IL, USA, 2008.

Ziebart, B. D., Bagnell, J. A., and Dey, A. K. Modeling in- teraction via the principle of maximum causal entropy. In International conference on machine learning. Carnegie Mellon University, 2010.

<!-- Page 13 -->

Distributional Inverse Reinforcement Learning

A. Related work comparison

**Table 4.** Comparison of IRL methods under various settings

Reference Model reward dist.?

Infer risk aware policy?

Recover reward dist.?

Learn return dist.?

(Wulfmeier et al., 2015; Ziebart et al., 2008) (Garg et al., 2021; Ni et al., 2021) (Zeng et al., 2022; 2023; Wei et al., 2023)

✗ ✗ ✗ ✗

(Ramachandran & Amir, 2007; Choi & Kim, 2011) (Chan & van der Schaar, 2021; Lee et al., 2022) ✓ ✗ ✗ ✗

(Karimi & Ebadzadeh) ✗ ✗ ✗ ✓

(Singh et al., 2018; Lacotte et al., 2019) (Cheng et al., 2023) ✗ ✓ ✗ ✗

This work ✓ ✓ ✓ ✓

In Table A, we compare DistIRL with existing IRL methods along four key dimensions. The first column, Model reward distribution, asks whether a method explicitly represents the reward as a random variable rather than as a fixed deterministic function. For example, Bayesian IRL methods place a prior over reward parameters, thereby modeling uncertainty, but they do not recover the actual shape of the underlying distribution. This is distinct from Recover reward distribution, which requires learning the full distribution of rewards themselves, including higher-order statistics such as variance and skewness, rather than just a posterior over parameters.

The third column, Infer risk-aware policy, evaluates whether a method incorporates risk measures into policy inference. Methods in this category optimize beyond expected return, often capturing aversion or preference to variability in outcomes. The final column, Learn return distribution, indicates whether a method leverages distributional reinforcement learning (DistRL) techniques to estimate the full distribution of returns, rather than only their expectation. Unlike reward distributions, which describe stochasticity at the immediate reward level, return distributions capture the cumulative effect of randomness from rewards, transitions, and policies over trajectories.

As shown in the table, most prior IRL methods either assume deterministic rewards or restrict themselves to expectationbased inference. In contrast, DistIRL simultaneously models stochastic rewards, learns full reward distributions, integrates distributional return estimation, and supports risk-aware policy learning, thereby unifying these capabilities in a principled way.

B. Extended preliminaries

The state-value and action-value functions under π are defined as

V π(s) = E

Zπ|st = s

, Qπ(s, a) = E

Zπ|st = s, at = a

.

They satisfy the Bellman equations

V π(s) = Ea∼π,s′∼P [r(s, a) + γV π(s′)], Qπ(s, a) = Es′∼P r(s, a) + γ Ea′∼π[Qπ(s′, a′)]

.

We also define the occupancy measure of π as dπ(s, a) = (1 −γ) P∞ t=0 γt Pr(st = s) π(a|s), which satisfies P s,a dπ(s, a) = 1 and characterizes the long-run state-action visitation probability.

B.1. Distributional RL and Risk-Sensitive Control Rather than estimating only E[Zπ], distributional RL models the entire return distribution that obeys the distributional Bellman operator T π (Bellemare et al., 2017):

Zπ(s, a) =

∞ X t=0 γt r(st, at),

<!-- Page 14 -->

Distributional Inverse Reinforcement Learning

T πZ(s, a)

D= r(s, a) + γ Z s′, π(s′)

, where V:

D= U denotes equality of probability laws, indicating random variables {V, U} are distributed according to the same law. A popular parameterization uses quantile regression: one approximates Zπ(s, a) by N quantiles θ(s, a) = [θ1(s, a),..., θN(s, a)]: S × A →RN at fractions (quantile levels) τi = i/N, for i = 1,..., N. In other words, the quantile distribution of Zπ(s, a) is represented by a uniform probability distribution supported on {θi(s, a)}N i=1: Zπ(s, a) = 1

N

PN i=1 δθi(s, a) where δθi denotes a Dirac at θi. An example of quantile functions is illustrated in Fig. 1, with θ and τ indicated.

To update the critic, instead of formulating the TD error, one can minimize the quantile Huber loss (Dabney et al., 2018b) with threshold κ > 0:

ρκ τ(δ) = τ −1{δ < 0}

Hκ(δ), Hκ(δ) =

(

1 2 δ2, |δ| ≤κ, κ |δ| − 1 2 κ2, |δ| > κ. (9)

In distributional RL with N quantile fractions {τi}, the loss for the critic is defined as min θ LQR(θ) = min θ

1 N

N X i=1

N X j=1 ρτi (δij), δij = r + γ θj(s′, a′) −θi(s, a). (10)

Once the return distribution is learned, one can optimize risk measures M, e.g. Conditional Value at Risk (CVaR) (Rockafellar et al., 2000), by maximizing CVaR

Zπ rather than E[Zπ], yielding risk-sensitive policies.

Deterministic reward as a special case. If q(· | s, a) is a point mass at some value r(s, a) for every (s, a), then we recover the usual deterministic reward setting. Thus, our framework strictly generalizes standard IRL.

Why distributions matter. If the reward is inherently stochastic (for example, due to noisy human judgments), matching only the mean reward or mean return is not enough to capture the full behavior. Two policies can have the same expected return but very different risk profiles. This motivates working with the full return distribution Zπ, not just its expectation.

**Table 5.** Examples of distortion risk measures.

Measure ξ(v) Interpretation

CVaRα min (v/α, 1) Average of worst α-fraction of outcomes Wang’s Φ(Φ−1(v) + λ) λ > 0 risk-aversion, λ < 0 risk-seeking

B.2. First-Order Stochastic Dominance (FSD)

We now recall first-order stochastic dominance, which provides a way to compare entire distributions, not just means or variances. Definition B.1 (First-order stochastic dominance). Let X and Y be real-valued integrable random variables with cumulative distribution functions FX and FY. We say that X first-order stochastically dominates Y, written X ⪰FSD Y, if

FX(z) ≤FY (z) for all z ∈R.

Intuitively, X ⪰FSD Y means that X tends to take larger values than Y: for every threshold z, the probability that X falls below z is no larger than the probability that Y does. Graphically, the CDF of X lies everywhere below the CDF of Y.

Connection to utilities and mean dominance. A classical result states that X ⪰FSD Y if and only if

E[u(X)] ≥E[u(Y)]

for every non-decreasing utility function u. In particular, taking u(x) = x, we get

E[X] ≥E[Y ], so FSD implies mean dominance. However, the converse is false: matching or exceeding the mean does not guarantee FSD.

<!-- Page 15 -->

Distributional Inverse Reinforcement Learning

FSD in our context. In our framework, we would like the return distribution of the expert policy, ZE, to dominate that of any learned policy Zπ, or vice versa depending on the formulation. This is a strong requirement and is typically hard to enforce directly during learning. Our approach therefore designs an objective that penalizes violations of FSD and then turns this objective into an energy function for learning the reward distribution.

B.3. The FSD Violation Objective as an Energy Function

Recall the FSD-based objective in the main text:

LFSD(π, r) =

Z ∞

−∞

FZE(z) −FZπ(z)

+ dz, (11)

where [x]+ = max{x, 0} denotes the positive part. This quantity measures, in an integrated way, how much FZE lies above FZπ. If ZE ⪰FSD Zπ, then FZE(z) ≤FZπ(z) for all z, so the integrand is always zero, and hence LFSD(π, r) = 0. If FSD is violated, then LFSD(π, r) becomes positive.

Energy-based interpretation. We treat LFSD(π, r) as an energy that scores how well a reward function r explains the expert demonstrations under policy π. Lower LFSD means fewer FSD violations and thus better agreement with the expert. This motivates defining an energy-based model (EBM)

p(D | r) ∝exp

−LFSD(π, r)

, (12)

where D denotes the expert data and the proportionality hides a (typically intractable) normalizing constant. In words: reward functions that produce small FSD violations are exponentially more likely under the expert data.

This construction gives us a likelihood model for the reward r given the data D, which we will combine with a prior over r and then approximate via variational inference.

B.4. Variational Inference and ELBO Derivation

We now derive the variational objective used to learn the reward distribution. We start from Bayes’ rule:

p(r | D) = p(D | r) p0(r)

p(D), where p0(r) is a prior over reward functions and p(D) =

Z p(D | r) p0(r) dr is the evidence (marginal likelihood), which is typically intractable to compute or differentiate.

We introduce a variational family qϕ(r | s, a), parameterized by ϕ, to approximate the true posterior p(r | D). To measure how close qϕ is to the true posterior, consider the KL divergence

KL qϕ(r | s, a) ∥p(r | D)

= Eqϕ h log qϕ(r | s, a)

p(r | D)

i

. (13)

Plugging in Bayes’ rule for p(r | D) gives

KL qϕ(r | s, a) ∥p(r | D)

= Eqϕ h log qϕ(r | s, a) p(D | r) p0(r)/p(D)

i

(14)

= Eqϕ h log qϕ(r | s, a) −log p(D | r) −log p0(r) + log p(D)

i

. (15)

We can separate out the term that does not depend on r:

KL qϕ(r | s, a) ∥p(r | D)

= Eqϕ log qϕ(r | s, a) −log p(D | r) −log p0(r)

+ log p(D). (16)

<!-- Page 16 -->

Distributional Inverse Reinforcement Learning

Rearranging terms yields log p(D) = Eqϕ log p(D | r) + log p0(r) −log qϕ(r | s, a)

+ KL qϕ(r | s, a) ∥p(r | D)

. (17)

Since KL is non-negative, we obtain the evidence lower bound (ELBO):

log p(D) ≥Eqϕ log p(D | r) + log p0(r) −log qϕ(r | s, a)

=: ELBO(ϕ). (18)

Equivalently,

ELBO(ϕ) = Eqϕ(r|s,a)

log p(D | r)

−KL qϕ(r | s, a) ∥p0(r)

, (19)

which matches the expression in the main text.

From ELBO to our reward objective. Maximizing the ELBO is equivalent to minimizing its negative. Using the EBM likelihood from Eq. (12), log p(D | r) = −LFSD(π, r) + const, where the constant does not depend on r and thus can be dropped for optimization. Substituting into Eq. (19) and ignoring constants, we obtain the objective min ϕ Lr(ϕ):= min ϕ Eqϕ(r|s,a)

LFSD(π, r)

+ KL qϕ(r | s, a) ∥p0(r)

, (20)

which is precisely Eq. 3 in the main text. In other words, we learn the reward distribution by balancing two terms: (i) the expected FSD violation under qϕ, and (ii) a regularization term that keeps qϕ close to the prior p0.

B.5. Quantiles and the FSD Loss

We now explain in more detail why the FSD loss in Eq. (11) can be expressed in terms of quantile functions, which leads to a practical way to estimate it via sampling.

Quantile function. For a random variable X with CDF FX, its (generalized) quantile function F −1

X: [0, 1] →R is defined by

F −1

X (v) = inf{x ∈R | FX(x) ≥v}, v ∈(0, 1).

Intuitively, F −1

X (v) is the value such that a fraction v of the mass of X lies at or below it.

Key identity. We use the following identity (proved in Appendix C.1 of the main text):

Z ∞

−∞

[FZE(z) −FZπ(z)]+ dz =

Z 1

0

F −1

Zπ (v) −F −1

ZE(v)

+ dv. (21)

This shows that integrating the positive difference of the CDFs is equivalent to integrating the positive difference of the quantiles, but with the roles of expert and policy swapped inside the bracket.

Sketch of proof idea. The proof relies on two facts: (i) an integral representation of the difference between two distributions in terms of their quantiles, and (ii) a change of variables between z and v through the CDF/quantile mapping. One can start from the left-hand side, partition the real line into regions where FZE(z) ≥FZπ(z) and where the opposite holds, and then perform a change of variables z = F −1

Zπ (v) (and similarly for the expert), carefully tracking the positive part. We refer the reader to the detailed derivation in Appendix C.1.

Monte Carlo approximation. The identity (21) is particularly useful because we can approximate quantiles from samples. For example, to approximate F −1

Zπ, we draw N return samples zn =

∞ X t=0 γtr(n)

t, r(n)

t ∼qϕ(· | s(n)

t, a(n)

t),

<!-- Page 17 -->

Distributional Inverse Reinforcement Learning and sort them to obtain order statistics z(1) ≤z(2) ≤· · · ≤z(N).

A simple empirical approximation of the quantile function is then

F −1

Zπ k

N

≈z(k).

In practice, we use such empirical quantiles (for both the expert and the learned policy) to estimate the integral on the right-hand side of Eq. (21) via a Riemann sum.

B.6. Distortion Risk Measures and Their Relation to FSD

Finally, we explain how distortion risk measures (DRMs) provide a scalar, risk-sensitive summary of a return distribution and how they relate to FSD.

Definition B.2 (Distortion function). A distortion function is a non-decreasing function ξ: [0, 1] →[0, 1] such that ξ(0) = 0 and ξ(1) = 1. Its dual distortion is defined as

˜ξ(v):= 1 −ξ(1 −v), v ∈[0, 1].

Definition B.3 (Distortion risk measure). For an integrable random variable X and a distortion function ξ, the associated distortion risk measure Mξ is defined by

Mξ(X) =

Z 1

0 F −1

X (v) d˜ξ(v), where F −1

X is the quantile function of X.

Intuition. The DRM Mξ(X) aggregates all quantiles of X into a single scalar value, with weights determined by d˜ξ(v). Different choices of ξ emphasize different parts of the distribution: for example, a concave ˜ξ assigns more weight to lower quantiles, which corresponds to risk-averse behavior.

Connection to FSD. It is known that if X ⪰FSD Y, then

Mξ(X) ≥Mξ(Y) for every distortion function ξ.

Furthermore, the converse holds if we require the inequality to hold for all distortion functions: if Mξ(X) ≥Mξ(Y) for every distortion function ξ, then X ⪰FSD Y. This shows that DRMs are tightly linked to FSD: they preserve the FSD ordering if we consider all possible distortions.

In our method, we exploit this relationship by replacing the intractable indicator-based weighting of quantiles (from Eq. (5) in the main text) with a tractable distortion-based weighting. This yields a risk-aware policy objective of the form max φ Mξ(Zπφ) + H(πφ), which can be optimized with standard policy gradient techniques while still encoding a meaningful notion of distributional dominance relative to the expert.

Approximation viewpoint. Optimizing Mξ(Zπφ) for a single distortion function ξ does not guarantee FSD dominance by itself; it corresponds to a weaker condition. However, as discussed in the main text, if one could optimize this objective for all distortion functions simultaneously, then under mild assumptions the resulting policy would satisfy the original FSD-based objective. Our practical objective can therefore be viewed as an approximation that focuses on a particular, user-chosen notion of risk.

<!-- Page 18 -->

Distributional Inverse Reinforcement Learning

C. Proofs

C.1. Proofs for sections 4

We first wish to show that

Z ∞

−∞

[FZE(z) −FZπ(z)]+dz =

Z 1

0

F −1

Zπ (v) −F −1

ZE(v)

+dv. (22)

Proposition C.1. Let Zπ and ZE be two real-valued integrable random variables with cumulative distribution functions FZπ and FZE, and corresponding quantile functions F −1

Zπ and F −1

ZE. Then we have

Z ∞

−∞

[FZE(z) −FZπ(z)]+ dz =

Z 1

0

F −1

Zπ (v) −F −1

ZE(v)

+ dv, where [x]+:= max(x, 0).

Proof. Note that

Z ∞

−∞

[FZE(z) −FZπ(z)]+ dz =

Z ∞

−∞

Z 1

0 1FZE (z)≥v≥FZπ (z)dvdz

=

Z 1

0

Z ∞

−∞

1FZE (z)≥v≥FZπ (z)dvdz

=

Z 1

0

Z ∞

−∞

1F −1 Zπ (v)≥z≥F −1

ZE (v)dvdz

=

Z 1

0

F −1

Zπ (v) −F −1

ZE(v)

+ dv

The interchange of integrals are permitted by the Theorem of Fubini-Tonelli as everything is positive (Heil, 2019). Note that the definition of the quantile function (Gut, 2006) is:

F −1(v):= inf z∈R{F(z) ≥v}.

Proposition 4.6. Mξ(X) ≥Mξ(Y) for every distortion function ξ implies X ⪰FSD Y.

Proof. Define the difference in quantile functions:

h(v):= F −1

X (v) −F −1

Y (v).

Suppose for contradiction that the set

A:= {v ∈[0, 1]|h(v) < 0}

has positive Borel measure, i.e., µ(A) > 0. Define a distortion function ˜ξA whose derivative is:

˜ξ′

A(v) =

(

1 µ(A) if v ∈A,

0 otherwise.

Then ˜ξA is a valid distortion function and satisfies

R 1

0 d˜ξA(v) = 1. Note that

MξA(X) −MξA(Y) =

Z 1

0 h(v) d˜ξA(v) =

Z

A h(v) · 1 µ(A) dv < 0.

<!-- Page 19 -->

Distributional Inverse Reinforcement Learning

This contradicts the assumption that M˜ξ(X) ≥M˜ξ(Y) for all distortion functions ˜ξ. Therefore, the set where F −1

X (v) < F −1

Y (v) must have measure zero. Thus we have

F −1

X (v) ≥F −1

Y (v) for v ∈[0, 1] almost everywhere (a.e.)

which implies

FX(z) ≤FY (z) for all z ∈R, since

FX(z) = PX (X < z) = µ

{v ∈[0, 1]|F −1

X (v) ≤z}

≤µ

{v ∈[0, 1] ∩Ac|F −1

X (v) ≤z}

+ µ

{v ∈[0, 1] ∩A|F −1

X (v) ≤z}

= µ

{v ∈[0, 1] ∩Ac|F −1

X (v) ≤z}

≤µ

{v ∈[0, 1] ∩Ac|F −1

Y (v) ≤z}

≤µ

{v ∈[0, 1]|F −1

Y (v) ≤z}

= FY (z)

The second inequality is due to the fact that for any z,

{v ∈[0, 1] ∩Ac|F −1

X (v) ≤z} ⊆{v ∈[0, 1] ∩Ac|F −1

Y (v) ≤z}

Hence,

X ⪰FSD Y.

C.2. Convergence Analysis

This appendix provides complete derivations and proofs for the convergence results summarized in Section 5. We work in the discounted MDP setting with finite action space A and (possibly infinite) state space S. All function norms are ∥· ∥∞ unless otherwise specified.

We first recall the risk–sensitive Bellman operator. For a fixed policy π, reward parameter ϕ, and bounded Q: S × A →R, we write

(T π ξ,ϕQ)(s, a):= Eξ qϕ(s, a)

+ γ Eξ, s′∼P (·|s,a), a′∼π(·|s′)

Q(s′, a′)

. (23)

Here the notation Eξ[·] denotes the one-step evaluation combining the conditional expectation over the transition kernel and the dynamic distortion risk measure Mξ (i.e. a nested, time-consistent dynamic risk mapping). Under this formulation, T π ξ,ϕ is precisely the DRM Bellman operator: it preserves the Markov structure and is a γ-contraction under mild axioms on Mξ (Ruszczy´nski, 2010), guaranteeing a unique fixed point Qξ ϕ,π for each (ϕ, π).

C.2.1. ASSUMPTIONS

We collect the standing assumptions used in the analysis.

Assumption 5.1. There exists Rmax < ∞such that

|qϕ(s, a)| ≤Rmax almost surely for all (s, a, ϕ). (7)

This is standard in discounted RL and is enforced in our implementation by clipping the reward range (via a scaled tanh nonlinearity). It ensures that all risk-sensitive value functions are uniformly bounded.

Assumption 5.2. For every (s, a) and all ϕ1, ϕ2 ∈Rd, the reward laws satisfy

W∞ qϕ1(·|s, a), qϕ2(·|s, a)

≤LR ∥ϕ1 −ϕ2∥, (8)

where W∞denotes the Wasserstein infinity distance. Equivalently, one can couple qϕ1(s, a) and qϕ2(s, a) such that |qϕ1(s, a) −qϕ2(s, a)| ≤LR ∥ϕ1 −ϕ2∥ almost surely.

<!-- Page 20 -->

Distributional Inverse Reinforcement Learning

This assumption is mild for smooth neural parameterizations of qϕ(r|s, a) (e.g., skew-normal with smooth outputs for location, scale, and skew). It states that small changes in the reward parameters ϕ cannot drastically change the reward distribution, which is necessary for the critic and policy to track the moving reward model.

Assumption 5.3. For each state-action pair s ∈S, a ∈A, the one-step distortion risk measure Mξ(·|s, a) is

1. monotone: X ≤Y a.s. implies Mξ(X|s, a) ≤Mξ(Y |s, a);

2. translation-equivariant: Mξ(X + c|s, a) = Mξ(X|s, a) + c for all c ∈R;

3. 1-Lipschitz in ∥· ∥∞: for all bounded random variables X, Y, Mξ(X|s, a) −Mξ(Y |s, a)

≤∥X −Y ∥∞.

For normalized distortion risk measures Mξ (including CVaR, Wang-type, and more general spectral DRMs), these properties are standard and follow from their integral representation in terms of quantile functions.

C.2.2. CONTRACTION OF THE NESTED DRM BELLMAN OPERATOR

We now verify that T π ξ,ϕ is a γ-contraction in the sup norm. This is the risk-sensitive analogue of the standard Bellman contraction and is a special instance of the general results on nested risk mappings in Ruszczy´nski (2010); Kopa & ˇSm´ıd (2023).

Lemma C.2 (Contraction of T π ξ,ϕ). Under Assumptions 5.1 and 5.3, for any fixed (ϕ, π) and any bounded U, V: S ×A →R,

T π ξ,ϕU −T π ξ,ϕV

∞≤γ ∥U −V ∥∞. (24)

Proof. For any (s, a), the immediate reward terms cancel, and we have

(T π ξ,ϕU)(s, a) −(T π ξ,ϕV)(s, a)

= γ

Eξ, s′∼P (·|s,a)[U(s′, A′) −V (s′, A′)]

≤γ Es′∼P (·|s,a)

Mξ(U(s′, A′) −V (s′, A′)|s′)

≤γ Es′∼P (·|s,a)

∥U −V ∥∞

= γ ∥U −V ∥∞,

(25)

where we used Assumption 5.3 (1-Lipschitzness) in the third line. Taking the supremum over (s, a) yields 24.

By the Banach fixed-point theorem, we immediately obtain:

Corollary C.3 (Existence and uniqueness of the risk-sensitive critic). Under Assumptions 5.1 and 5.3, for each fixed (ϕ, π) there exists a unique Qξ ϕ,π solving

Qξ ϕ,π = T π ξ,ϕQξ ϕ,π. (26)

Moreover, the critic is uniformly bounded.

Lemma C.4. Under Assumption 5.1, let BQ:= Rmax/(1 −γ). Then for all (ϕ, π),

Qξ ϕ,π

∞≤BQ. (27)

Proof. By unfolding the fixed point 26 along trajectories and using |qϕ(s, a)| ≤Rmax, we get for all (s, a)

Qξ ϕ,π(s, a)

≤

∞ X t=0 γtRmax = Rmax

1 −γ = BQ. (28)

Taking the supremum over (s, a) yields 27.

<!-- Page 21 -->

Distributional Inverse Reinforcement Learning

C.2.3. SOFTMAX LIPSCHITZ PROPERTIES

We next relate Q-function errors to policy errors via the softmax parameterization.

Lemma C.5. Let Q, Q′: A →R be two vectors of Q-values, and define π(a) = eQ(a) P b eQ(b), π′(a) = eQ′(a) P b eQ′(b). (29)

Then

∥log π −log π′∥∞≤2 ∥Q −Q′∥∞. (30)

Proof. For any action a, log π(a) = Q(a) −log

X b eQ(b), log π′(a) = Q′(a) −log

X b eQ′(b).

(31)

Subtracting, log π(a) −log π′(a) =

Q(a) −Q′(a)

− log

X b eQ(b) −log

X b eQ′(b)

. (32)

The log-sum-exp function is 1-Lipschitz in ∥· ∥∞, i.e.

log

X b eQ(b) −log

X b eQ′(b) ≤∥Q −Q′∥∞. (33)

Combining 32 and 33 gives

| log π(a) −log π′(a)| ≤|Q(a) −Q′(a)| + ∥Q −Q′∥∞≤2 ∥Q −Q′∥∞. (34)

Taking the supremum over a yields 30.

C.2.4. LIPSCHITZ SENSITIVITY

We now show that the DRM Q-function depends smoothly on the reward parameters ϕ, both for optimal control and for fixed-policy evaluation.

Lemma C.6. Suppose Assumptions 5.1, 5.2, and 5.3 hold. Then for all (s, a) and all ϕ1, ϕ2, qϕ1(s, a) −qϕ2(s, a)

≤LR ∥ϕ1 −ϕ2∥. (35)

Let Mξ denote the nested distortion risk functional, and assume it is 1-Lipschitz in ∥· ∥∞as in Assumption 5.3. Define the optimal risk-sensitive Q-function for parameter ϕ by

Qξ ϕ,∗(s, a):= sup π Mξ

∞ X t=0 γtrϕ(st, at)

s0 = s, a0 = a, π

, (36)

where {(st, at)}t≥0 is the trajectory under policy π starting from (s0, a0) = (s, a). Then there exists

Lq:= LR 1 −γ (37)

such that for all ϕ1, ϕ2, Qξ ϕ1,∗−Qξ ϕ2,∗

∞≤Lq ∥ϕ1 −ϕ2∥. (38)

<!-- Page 22 -->

Distributional Inverse Reinforcement Learning

Proof. The bound on the reward smoothness is immediately due to assumption 5.2. Fix ϕ1, ϕ2 and (s, a). For any policy π, let {(st, at)}t≥0 be the trajectory under π with (s0, a0) = (s, a), and define

Gπ ϕi:=

∞ X t=0 γtqϕi(st, at), i ∈{1, 2}. (39)

By definition 36,

Qξ ϕi,∗(s, a) = sup π Mξ

Gπ ϕi s, a, π

, i ∈{1, 2}. (40)

Using the inequality sup π fπ −sup π gπ

≤sup π |fπ −gπ|, (41)

we obtain Qξ ϕ1,∗(s, a) −Qξ ϕ2,∗(s, a)

= sup π Mξ(Gπ ϕ1|s, a, π) −sup π Mξ(Gπ ϕ2|s, a, π)

≤sup π

Mξ(Gπ ϕ1|s, a, π) −Mξ(Gπ ϕ2|s, a, π)

.

(42)

For each fixed π, the 1-Lipschitz property of Mξ in ∥· ∥∞(Assumption 5.3) gives

Mξ(Gπ ϕ1|s, a, π) −Mξ(Gπ ϕ2|s, a, π)

≤

Gπ ϕ1 −Gπ ϕ2

∞

= sup ω

∞ X t=0 γt qϕ1(st(ω), at(ω)) −qϕ2(st(ω), at(ω))

≤

∞ X t=0 γt sup

(s′,a′)

qϕ1(s′, a′) −qϕ2(s′, a′)

≤

∞ X t=0 γt LR∥ϕ1 −ϕ2∥

= LR 1 −γ ∥ϕ1 −ϕ2∥.

(43)

The bound does not depend on π, so combining it with Eq. 42 we obtain

Qξ ϕ1,∗(s, a) −Qξ ϕ2,∗(s, a)

≤ LR 1 −γ ∥ϕ1 −ϕ2∥. (44)

Taking the supremum over (s, a) yields the desired result.

Lemma C.7 (Lipschitz continuity of Qξ ϕ,π in ϕ for fixed policy). Suppose Assumptions 5.1, 5.2, and 5.3 hold, and fix any stationary policy π. Define the risk–sensitive evaluation Q-function as

Qξ ϕ,π(s, a):= Mξ

∞ X t=0 γtqϕ(st, at)

s0 = s, a0 = a, π

, (45)

where {(st, at)}t≥0 is the trajectory under π starting from (s0, a0) = (s, a). Then for all ϕ1, ϕ2,

Qξ ϕ1,π −Qξ ϕ2,π

∞≤Lq ∥ϕ1 −ϕ2∥, Lq:= LR 1 −γ. (46)

Proof. Fix π and (s0, a0) = (s, a), and let {(st, at)}t≥0 be the trajectory under π. For i ∈{1, 2}, define Gπ ϕi as in 39. Then by 45,

Qξ ϕi,π(s, a) = Mξ(Gπ ϕi|s, a, π), i ∈{1, 2}. (47)

Thus Qξ ϕ1,π(s, a) −Qξ ϕ2,π(s, a)

=

Mξ(Gπ ϕ1|s, a, π) −Mξ(Gπ ϕ2|s, a, π)

≤

Gπ ϕ1 −Gπ ϕ2

∞

≤ LR 1 −γ ∥ϕ1 −ϕ2∥,

(48)

where the last inequality is identical to the bound in 43. Taking the supremum over (s, a) gives 46.

<!-- Page 23 -->

Distributional Inverse Reinforcement Learning

C.2.5. ONE-STEP CRITIC RECURSION

We now derive a simple one-step recursion for the critic’s tracking error as the reward parameters ϕk and policies πk evolve across iterations.

For each iteration k, define

Ek:=

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞, (49)

where π⋆ ϕk is an optimal DRM policy for reward parameter ϕk, i.e.

π⋆ ϕk ∝softmaxπQξ ϕk,π. (50)

Lemma C.8. Suppose Assumptions 5.1, 5.2, and 5.3 hold, and let Lq be as in Lemma C.7. Then for all k ≥1,

Ek ≤γ Ek−1 + 2Lq ∥ϕk −ϕk−1∥. (51)

Proof. Add and subtract Qξ ϕk−1,πk and Qξ ϕk−1,π⋆ ϕk−1 inside the norm:

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞

=

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk + Qξ ϕk−1,πk −Qξ ϕk−1,πk + Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk−1,π⋆ ϕk−1

∞

≤

Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk,π⋆ ϕk

∞+

Qξ ϕk,πk −Qξ ϕk−1,πk

∞+

Qξ ϕk−1,πk −Qξ ϕk−1,π⋆ ϕk−1

∞.

(52)

By Lemma C.6 (with π⋆ ϕk−1 and π⋆ ϕk both optimal) and Lemma C.7 (with π = πk), we have

Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk,π⋆ ϕk

∞≤Lq ∥ϕk −ϕk−1∥, Qξ ϕk,πk −Qξ ϕk−1,πk

∞≤Lq ∥ϕk −ϕk−1∥.

(53)

Therefore, Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞≤2Lq ∥ϕk −ϕk−1∥+

Qξ ϕk−1,πk −Qξ ϕk−1,π⋆ ϕk−1

∞. (54)

Next observe that for fixed ϕk−1, π⋆ ϕk−1 is optimal, so

Qξ ϕk−1,πk ≤Qξ ϕk−1,π⋆ ϕk−1 pointwise. (55)

Moreover, by monotonicity of the Bellman operator and Lemma C.2,

0 ≤Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk−1,πk ≤T πk ξ,ϕk−1

Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk−1,πk

, (56)

so taking norms and using 24 gives

Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk−1,πk

∞≤γ

Qξ ϕk−1,π⋆ ϕk−1 −Qξ ϕk−1,πk−1

∞= γ Ek−1. (57)

So that we get

Ek =

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞≤γ Ek−1 + 2Lq ∥ϕk −ϕk−1∥, (58)

as claimed.

C.2.6. SMOOTH REWARD UPDATES AND AVERAGED CRITIC TRACKING

We now relate the parameter drift ∥ϕk −ϕk−1∥to the reward update objective Lr(ϕ) used in Eq. 3.

Assumption C.9 (Smoothness and bounded gradients of the reward objective). Let Lr(ϕ) denote the reward-distribution objective in Eq. 3. Assume:

<!-- Page 24 -->

Distributional Inverse Reinforcement Learning

1. Lr is differentiable and its gradient is L∇–Lipschitz:

∇Lr(ϕ1) −∇Lr(ϕ2)

≤L∇∥ϕ1 −ϕ2∥ for all ϕ1, ϕ2. (59)

2. The iterates {ϕk} are projected onto a compact set Φ ⊂Rd, so that

Gmax:= sup ϕ∈Φ

∇Lr(ϕ)

< ∞. (60)

The reward update step is ϕk = ΠΦ ϕk−1 −ηk−1 ∇Lr(ϕk−1)

, (61)

where ΠΦ is the Euclidean projection onto Φ and {ηk} is a deterministic stepsize schedule. We state the assumption with projection for generality; in our implementation, the parameterization and reward clipping make this projection implicit.

Lemma C.10. Under Assumption C.9,

∥ϕk −ϕk−1∥≤ηk−1 Gmax. (62)

Proof. By non-expansiveness of the projection,

∥ϕk −ϕk−1∥=

ΠΦ(ϕk−1 −ηk−1∇Lr(ϕk−1)) −ΠΦ(ϕk−1)

≤ηk−1

∇Lr(ϕk−1)

≤ηk−1 Gmax, (63)

which is 62.

Now we are ready to get the main recursion formula.

Theorem 5.4. Assume Assumptions 5.1-5.3 hold. Let Ek =

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞. Assume the reward update satisfies

Assumption C.9, with stepsizes ηk = η = η0K−σ, η0 > 0, and σ ∈(0, 1). Then running the DistIRL algorithm K steps, we have 1

K

PK k=1 Ek = O(K−1) + O(K−σ).

Proof. By Lemmas C.8 and C.10,

Ek ≤γEk−1 + 2LqGmaxηk−1. (64)

Taking the sum, we have

K X k=1

Ek ≤

K X k=1 γEk−1 + 2LqGmax

K X k=1 ηk−1. (65)

Rearrange and average over K gives

1 −γ K

K X k=1

Ek ≤ γ K (E0 −EK) + 2LqGmaxηK−σ. (66)

Dividing both sides by 1 −γ gives

1 K

K X k=1

Ek ≤ γ (1 −γ)K C0 + 1 1 −γ 2LqGmaxηK−σ. (67)

This proves the claim.

<!-- Page 25 -->

Distributional Inverse Reinforcement Learning

C.2.7. POLICY CONVERGENCE IN LOG-PROBABILITY

Finally, we transfer the critic tracking guarantees to the induced policies.

Theorem 5.5. For each k, define the learned and DRM-optimal policies induced by the current Q-functions:

πk(·|s)∝exp

Qξ ϕk,πk(s, ·)

, π⋆ ϕk(·|s)∝exp

Qξ ϕk,π⋆ ϕk(s, ·)

.

Then, running the DistIRL algorithm K steps, we have

1 K

PK k=1 ∥log πk −log π⋆ ϕk∥∞= O(K−1) + O(K−σ).

Proof. Fix k and s. Let x(·) = Qξ ϕk,πk(s, ·), y(·) = Qξ ϕk,π⋆ ϕk (s, ·). (68)

By Lemma C.5, log π+ k (·|s) −log π⋆+ ϕk (·|s)

∞≤2∥x −y∥∞. (69)

Taking the supremum over s yields log π+ k −log π⋆+ ϕk

∞≤2

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞= 2Ek. (70)

Averaging over k = 1,..., K and substituting the bound from Theorem 5.4 gives Eq. 5.5.

C.2.8. FIRST–ORDER CONVERGENCE OF THE REWARD UPDATE

We now show that, under mild additional conditions, the reward update drives the gradient of the reward objective to zero in an averaged sense, so that the iterates approach a stationary point of the inner minimization problem over ϕ. This is the strongest guarantee available without assuming that the reward function approximator is convex.

Recall that the reward objective Lr(ϕ) and its update rule were introduced in Assumption C.9. The update at iteration k is ϕk+1 = ΠΦ ϕk −ηkgk

, (71)

where gk is the stochastic gradient computed using the current critic Qξ ϕk,πk and policy πk.

Assumption C.11 (Gradient estimator and critic bias). Let Fk denote the filtration generated by all randomness up to iteration k. Assume that the stochastic gradient gk satisfies, for some constants Cg, Gg > 0,

E[gk|Fk] −∇Lr(ϕk)

≤Cg Ek, (72)

E

∥gk∥2

≤G2 g, (73)

where

Ek:=

Qξ ϕk,πk −Qξ ϕk,π⋆ ϕk

∞ (74)

is the critic tracking error defined above.

Intuitively, (72) states that the gradient bias vanishes as soon as the critic tracks the DRM–optimal Q well (i.e., Ek is small), which is consistent with the inequality in (5.5): a small critic gap implies a small occupancy–measure mismatch, hence a small gradient bias. The second–moment bound (73) is standard in nonconvex stochastic optimization.

Theorem 5.6. Suppose Assumptions 5.1, 5.2, C.9, and C.11 hold. Let ηk = η0k−σ with η0 > 0 and σ ∈(0, 1), and assume Lr is bounded below on Φ. Then there exists C > 0 such that

1 K

K−1 X k=0

E∥∇Lr(ϕk)∥2 =O

K−1

+ O

K−σ

+ O

K−1+σ

.

<!-- Page 26 -->

Distributional Inverse Reinforcement Learning

Proof. We begin from the smoothness inequality with ϕ′ = ϕk+1, ϕ = ϕk:

Lr(ϕk+1) ≤Lr(ϕk) +

∇Lr(ϕk), ϕk+1 −ϕk

+ L∇

2 ∥ϕk+1 −ϕk∥2. (75)

By the non-expansiveness of the projection ΠΦ and the update rule,

∥ϕk+1 −ϕk∥=

ΠΦ(ϕk −ηkgk) −ΠΦ(ϕk)

≤ηk∥gk∥. (76)

Moreover,

∇Lr(ϕk), ϕk+1 −ϕk

=

∇Lr(ϕk), ΠΦ(ϕk −ηkgk) −ϕk

≤

∇Lr(ϕk), −ηkgk

(77)

= −ηk

∇Lr(ϕk), gk

. (78)

Substituting the above into Eq. 75 yields

Lr(ϕk+1) ≤Lr(ϕk) −ηk

∇Lr(ϕk), gk

+ L∇

2 η2 k∥gk∥2. (79)

Taking conditional expectation and expanding the inner product gives

∇Lr(ϕk), E[gk|Fk]

= 1

2

∥∇Lr(ϕk)∥2 + ∥E[gk|Fk]∥2 −∥E[gk|Fk] −∇Lr(ϕk)∥2

, which gives

−ηk

∇Lr(ϕk), E[gk|Fk]

= −ηk

2 ∥∇Lr(ϕk)∥2 −ηk 2 ∥E[gk|Fk]∥2 + ηk 2 ∥E[gk|Fk] −∇Lr(ϕk)∥2. (80)

Substituting Eq. 80 into Eq. 79 we obtain

Lr(ϕk+1) ≤Lr(ϕk) −ηk

2 ∥∇Lr(ϕk)∥2 −ηk 2 ∥E[gk|Fk]∥2 + ηk 2 ∥E[gk|Fk] −∇Lr(ϕk)∥2 + L∇ 2 η2 kE[∥gk∥2|Fk]

≤Lr(ϕk) −ηk

2 ∥∇Lr(ϕk)∥2 + ηk 2 ∥E[gk|Fk] −∇Lr(ϕk)∥2 + L∇ 2 η2 kE[∥gk∥2|Fk] (81)

where we discarded the negative term −ηk

2 ∥E[gk|Fk]∥2. Next we bound the bias term. Condition on ϕk, and use ∥E[gk|Fk] −∇Lr(ϕk)∥≤CgEk:

E

∥E[gk|Fk] −∇Lr(ϕk)∥2

≤E

C2 gE2 k

≤C2 g E[E2 k] ≤CC2 g E[Ek], (82)

where we used Ek ≥0 and Ek ≤C′∥Q∥∞so that E2 k ≤CEk. Similarly,

E

∥gk∥2

≤G2 g. (83)

Taking expectations of Eq. 81 and applying Eq. 82-83 gives

E[Lr(ϕk+1)] ≤E[Lr(ϕk)] −ηk

2 E

∥∇Lr(ϕk)∥2

+ ηk

2 C2 g E[Ek] + L∇

2 η2 kG2 g. (84)

Rearrange Eq. 84 as ηk

2 E

∥∇Lr(ϕk)∥2

≤E[Lr(ϕk)] −E[Lr(ϕk+1)] + ηk

2 CC2 g E[Ek] + L∇

2 η2 kG2 max. (85)

Multiply both sides by 2/ηk:

E

∥∇Lr(ϕk)∥2

≤2 ηk

E[Lr(ϕk)] −E[Lr(ϕk+1)]

+ C2 g E[Ek] + L∇ηkG2 g. (86)

<!-- Page 27 -->

Distributional Inverse Reinforcement Learning

Now sum Eq. 86 over k = 0,..., K −1:

K−1 X k=0

E

∥∇Lr(ϕk)∥2

≤2

K−1 X k=0

E[Lr(ϕk)] −E[Lr(ϕk+1)]

ηk

+ C2 g

K−1 X k=0

E[Ek] + L∇G2 g

K−1 X k=0 ηk. (87)

Using the boundedness equation and the fact that ηk is constant, we bound the first sum as

K−1 X k=0

E[Lr(ϕk)] −E[Lr(ϕk+1)]

ηk

=

K−1 X k=0

E[Lr(ϕk)] −E[Lr(ϕk+1)]

1 ηk

= Kσ η

K−1 X k=0

E[Lr(ϕk)] −E[Lr(ϕk+1)]

= Kσ η

E[Lr(ϕ0)] −E[Lr(ϕK)]

≤Lmax −Lmin η Kσ. (88)

Next, apply the averaged tracking bound on the action-value function:

K−1 X k=0

E[Ek] = K · 1

K

K−1 X k=0

E[Ek]

= O

1

+ O(K1−σ) (89)

Finally, since ηk = ηK−σ with 0 < σ < 1,

K−1 X k=0 ηk = η

K X k=1

K−σ = O

K1−σ

. (90)

Divide both sides by K:

1 K

K−1 X k=0

E

∥∇Lr(ϕk)∥2

≤2(Lmax −Lmin)

η Kσ−1 (91)

+ γ (1 −γ)C0C2 g/K + C2 g 1 −γ 2LqGmaxηK−σ (92)

+ L∇G2 g ηK−1. (93)

So that we have

1 K

K−1 X k=0

E

∥∇Lr(ϕk)∥2

= O(K−σ) + O(K−1+σ) + O(K−1), (94)

Since 0 < σ < 1, all three terms vanish as K →∞, so the averaged squared gradient converges to zero.

D. Model architecture and hyper-parameters

Throughout this paper, we use the following model architecture for all the experiments.

For gridworld, we specify the reward range as [0, 2]. For MuJoCo tasks, [−10, 10]. This is achieved by applying a (scaled) tanh function.

E. Additional Ablation studies

E.1. Ablation on choices of DRM and its parameter

In this section, we present additional ablation studies. First, we evaluate the performance of DistIRL on the risk-averse D4RL dataset with different choices of DRM in the HalfCheetah instance. Note that for CVaR and VaR, the smaller distortion

<!-- Page 28 -->

Distributional Inverse Reinforcement Learning

**Table 6.** Model Parameters for DistIRL

Parameter Value Training Parameters Learning Rate 3 × 10−4

Batch Size 512 Total Iterations 5,000 Entropy Coefficient 0.1 Risk Measure CVaR Risk Parameter 0.05 Reward Regularization 0.01 Network Architecture Policy Network [256, 128] Reward Distribution Family Task-dependent (Gaussian, skew-normal, or quantile) Reward Range [-5.0, 5.0] Number of Quantiles 200 Reward Hidden Features 128 parameter η is, the more risk-averse the policy will be. For Wang’s risk measure, which has parameter η ranging from −1 to 1, the policy varies from risk-seeking to risk-averse, with η = 0 having risk-neutral behavior. The choice of risk parameter affects the shape ˜ξ′, which affects the solution quality of the policy optimization problem in Eq. 4.

**Table 7.** demonstrates the effects of different choices of risk measure and its risk parameter. Note that since the data is generated by a risk-averse policy, a risk-averse DRM produces the best result, while risk-neutral policies are substantially worse, and risk-seeking policies fail to capture the expert’s behavior.

**Table 7.** Performance on distributional reward settings (D4RL).

DRM η = 0.05 η = 0.5 η = 0.9 η = −0.5 η = −0.9

CVaR 3539.74 ± 44.26 3384.27 ± 151.06 2851.13 ± 689.67 - - VaR 3539.12 ± 76.77 3423.43 ± 113.72 3081.96 ± 522.94 - - Wang 2670.42 ± 730.93 2849.94 ± 1220.71 3439.46 ± 314.48 1755.25 ± 13.42 444.62 ± 1.90

E.2. Ablation on Number of Trajectories

**Table 8.** Performance averaged over 5 seeds for varying dataset sizes (10, 5, 3, 1 trajectories).

Environment 10 5 3 1

HalfCheetah 3539.74 ± 44.26 3440.67 ± 58.48 3501.53 ± 91.82 3238.49 ± 339.72 Hopper 886.44 ± 0.79 888.71 ± 20.16 893.15 ± 14.13 748.93 ± 112.53 Walker2d 1526.46 ± 148.24 1291.44 ± 759.45 1143.62 ± 231.05 1151.86 ± 180.98

In addition to the main comparison, we conduct an ablation study on the number of expert trajectories used to train our DistIRL algorithm. For each environment, we construct datasets with {10, 5, 3, 1} expert trajectories, and train our method on each of these datasets independently. The evaluation protocol is kept identical to the main experiments. We report the average return over 5 random seeds, with the standard deviation across seeds.

**Table 8.** summarizes the results. Overall, the performance degrades as the number of trajectories decreases, which is expected given the reduced coverage of the expert behavior. Nevertheless, our IRL algorithm remains reasonably robust in the low-data regime. With as few as 3 to 5 trajectories, it still achieves returns close to those obtained with 10 trajectories on most tasks. Even in the extreme case of a single trajectory, the learned policies retain non-trivial performance, indicating that the method can extract useful structure from highly limited expert demonstrations.

F. Additional Results on Matching Return Distribution

**Figure 6.** presents a comparison of distributional fidelity between DistIRL and BIRL using three metrics: (a) relative errors of higher-order moments, (b) summarized moment errors up to kurtosis, and (c) estimated–versus–expert quantile alignment.

<!-- Page 29 -->

Distributional Inverse Reinforcement Learning

1 2 3 4 5 6 7 8 Moment order k

100

101

102

103

Relative error

(a) DistIRL BIRL

Mean Var Skew Kurt

100

101

Relative Error

(b) DistIRL BIRL

Expert quantile

Estimated quantile

(c)

Ideal DistIRL BIRL

**Figure 6.** Distributional fidelity of learned return distributions on HalfCheetah. Left: relative errors of higher-order moments. Middle:

summarized moment errors up to kurtosis. Right: estimated-versus-expert quantile alignment, where the diagonal indicates perfect matching.

In (a), DistIRL maintains consistently low relative error across all moment orders, demonstrating its ability to capture not only the mean and variance but also the skewness and tail behavior of the expert return distribution. In contrast, BIRL’s error grows rapidly with increasing moment order, indicating limited capacity to recover higher-order structure. Panel (b) further highlights this gap, showing that DistIRL achieves uniformly low errors on the first four moments, whereas BIRL exhibits substantial discrepancies, particularly in variance and higher moments. Panel (c) compares estimated and expert quantiles, where the dashed diagonal represents perfect alignment. DistIRL closely follows this ideal mapping across the entire range, while BIRL deviates significantly, especially in the upper tail. Overall, this figure illustrates that DistIRL reconstructs the full return distribution with higher accuracy than BIRL, which is necessary for risk-sensitive learning and downstream decision-making under uncertainty.

G. Additional Results on Dopamine Level

Figures in this section provide additional state-action examples from the mouse spontaneous behavior dataset. They are selected to show representative dopamine-response shapes across different syllable transitions and to complement the aggregate Wasserstein and correlation metrics in the main text. Across these examples, DistIRL is intended to recover not only the mean reward level but also the shape of the empirical dopamine fluctuation distribution.

4 2 0 2 4 Reward

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Density

Reward Distribution State 1, Action 7

True S-DistIRL DistIRL S-BIRL BIRL Det

4 2 0 2 4 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 1, Action 7

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 7.** Reward recovery for state 1 action 7

H. Limitations

Our ideal policy objective (Eq. 4) enforces first-order stochastic dominance (FSD) but the indicator-based formulation is nondifferentiable, making exact FSD-constrained optimization intractable in practice. Additionally, we treat each state-action

<!-- Page 30 -->

Distributional Inverse Reinforcement Learning

2 0 2 4 Reward

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Density

Reward Distribution State 3, Action 6

True S-DistIRL DistIRL S-BIRL BIRL Det

2 0 2 4 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 3, Action 6

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 8.** Reward recovery for state 3 action 6

2 0 2 Reward

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Density

Reward Distribution State 4, Action 8

True S-DistIRL DistIRL S-BIRL BIRL Det

2 0 2 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 4, Action 8

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 9.** Reward recovery for state 4 action 8

reward distribution qϕ(r|s, a) as independent. This ignores potential correlations across different (s, a) pairs—such as spatial or temporal dependencies that naturally arise in many tasks. Extending DistIRL to capture joint reward distributions remains an important direction for future work.

<!-- Page 31 -->

Distributional Inverse Reinforcement Learning

4 2 0 2 4 Reward

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Density

Reward Distribution State 5, Action 7

True S-DistIRL DistIRL S-BIRL BIRL Det

4 2 0 2 4 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 5, Action 7

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 10.** Reward recovery for state 5 action 7

4 2 0 2 4 Reward

0.0

0.1

0.2

0.3

0.4

0.5

Density

Reward Distribution State 5, Action 9

True S-DistIRL DistIRL S-BIRL BIRL Det

4 2 0 2 4 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 5, Action 9

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 11.** Reward recovery for state 5 action 9

4 2 0 2 4 Reward

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Density

Reward Distribution State 7, Action 8

True S-DistIRL DistIRL S-BIRL BIRL Det

4 2 0 2 4 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 7, Action 8

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 12.** Reward recovery for state 7 action 8

<!-- Page 32 -->

Distributional Inverse Reinforcement Learning

2 0 2 Reward

0.0

0.1

0.2

0.3

0.4

0.5

Density

Reward Distribution State 9, Action 7

True S-DistIRL DistIRL S-BIRL BIRL Det

2 0 2 Reward

0.0

0.2

0.4

0.6

0.8

1.0

Cumulative Probability

Empirical CDF State 9, Action 7

True S-DistIRL DistIRL S-BIRL BIRL

**Figure 13.** Reward recovery for state 9 action 7
