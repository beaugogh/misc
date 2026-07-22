---
title: "Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization"
source_url: https://icml.cc/virtual/2026/oral/71075
paper_pdf_url: https://arxiv.org/pdf/2603.03741v2
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

<!-- Page 1 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent

Lyapunov Policy Optimization

Hao Zhang 1 2 Yaru Niu 2 Yikai Wang 2 Ding Zhao 2 H. Eric Tseng 1

## Abstract

To improve generalization and resilience in human–robot collaboration (HRC), robots must handle the combinatorial diversity of human behaviors and contexts, motivating multi-agent reinforcement learning (MARL). However, inherent heterogeneity between robots and humans creates a rationality gap (RG), where decentralized policy updates deviate from cooperative joint optimization. The resulting learning problem is a generalsum differentiable game, so independent policygradient updates can oscillate or diverge without added structure. We propose heterogeneousagent Lyapunov policy optimization (HALO), a framework that stabilizes decentralized MARL by enforcing Lyapunov-based contraction in policyparameter space. Unlike Lyapunov-based safe RL, which targets state/trajectory constraints in constrained Markov decision processes, HALO uses Lyapunov certification to stabilize decentralized policy learning. HALO rectifies decentralized gradients via optimal quadratic projections, ensuring monotonic contraction of RG and enabling effective exploration of open-ended interaction spaces. Extensive simulations and real-world humanoidrobot experiments show that this certified stability improves generalization and robustness in collaborative corner cases.

## 1. Introduction

Human-robot collaboration (HRC) is a central challenge for embodied intelligence in human environments, requiring robots to achieve task-level coordination with diverse and

1ETAIC Lab, Department of Electrical Engineering, University of Texas at Arlington, USA 2Safe AI Lab, Department of Mechanical Engineering, Carnegie Mellon University, USA. Correspondence to: H. Eric Tseng <hongtei.tseng@uta.edu>, Ding Zhao <dingzhao@andrew.cmu.edu>, Hao Zhang <haoz4@andrew.cmu.edu>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

adaptive human, and potentially robotic, partners. (Vinyals et al., 2019). Traditional HRC is framed as a single-agent task where the human is treated as a static or perturbed environmental component (Foerster et al., 2018). Such robot–script or log–replay paradigm relies on simulators with predefined human inputs, failing to capture the stochastic richness in human behaviors (Hadfield-Menell et al., 2016). Consequently, robots often overfit to specific interaction traces (Carroll et al., 2019), leading to performance collapse when encountering out-of-distribution (OOD) behaviors (Samvelyan et al., 2019; Strouse et al., 2021).

To transcend these limits, this work adopts heterogeneous multi-agent reinforcement learning (MARL) for human– robot synergy (Oroojlooy & Hajinezhad, 2023). We argue - and later demonstrated empirically in our experiment - that replacing static scripts with learning-capable humanoid proxies as a computational imperative (Haight et al., 2025), enabling robots to navigate infinite interaction manifolds (Lowe et al., 2017). MARL allows adaptive strategies to emerge that are intractable via manual scripting (Li et al., 2025). This ensures that complex edge cases are captured (Hu et al., 2020), providing a foundation for generalization. However, heterogeneous learning introduces a critical structural pathology known as the rationality gap (RG) (Kim et al., 2021). In MARL, agents share a team-level objective, but heterogeneity forces each agent to update from its own individual perspective (Rashid et al., 2020; Kang et al., 2023). While many prior MARL methods rely on parameter-sharing that collapse the joint parameter space into a shared representation (Wen et al., 2022), such sharing is infeasible in heterogeneous HRC settings. This mismatch further widens the RG, as individual updates diverge from team-optimal directions (Son et al., 2019).

Beyond this structural misalignment, decentralized learning also suffers from inherent dynamical instabilities. MARL updates evolve under a non-conservative vector field with a non-symmetric Jacobian, giving rise to rotational dynamics and limit cycles (Zhao et al., 2023; Balduzzi et al., 2018; Letcher et al., 2018). Prior work in differentiable games has proposed several methods to damp or compensate for these rotational forces, including symplectic gradient adjustment, which subtracts the antisymmetric component of the Jaco- arXiv:2603.03741v2 [cs.RO] 31 May 2026

<!-- Page 2 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization bian to reduce cycling (Balduzzi et al., 2018). Consensus optimization and its variants that regularize gradients toward more potential-like behavior (Mescheder et al., 2017), extragradient and optimistic methods that stabilize saddle-point dynamics (Gidel et al., 2018; Daskalakis et al., 2017), and opponent-shaping approaches that estimate how an agent’s update will influence others (Foerster et al., 2017). However, these techniques typically assume low-dimensional differentiable games, centralized Jacobian access, or fully modeled opponents, and thus remain difficult to apply in heterogeneous, partially observed, embodied HRC settings. As a result, heterogeneous agents often still “chase” one another’s evolving strategies, producing unstable oscillations that prevent convergence to cooperative optima (Mazumdar et al., 2020; Fiez et al., 2020) leaving exploration largely tethered to a non-convergent regime (Yang et al., 2024).

Consequently, existing HRC architectures lack a stability kernel capable of neutralizing these non-conservative forces (Chow et al., 2018). To the best of the authors’ knowledge, the integration of MARL-based interaction paradigm with a learning-stability kernel remains an open challenge in the context of HRC (Gu et al., 2023). Therefore, we introduce heterogeneous-agent Lyapunov policy optimization (HALO), which establishes a formal stability certificate in the policy-parameter space by quantifying coordination disagreement as a Lyapunov potential. By employing an optimal quadratic projection to rectify optimization dynamics, HALO ensures the monotonic contraction of the RG.

Our contributions are summarized as follows: 1) we propose a learning kernel HALO that enforces stable policyparameter updates via an optimal quadratic projection, yielding a formal stability certificate in parameter space; 2) We establish theoretical guarantees, proving monotonic contraction of the rationality gap under HALO using nonlinear stability analysis (Khalil & Grizzle, 2002); 3) we demonstrate HALO across diverse HRC tasks and formalize why autonomous exploration with HALO is necessary to avoid the OOD brittleness of scripted HRC.

## 2. Related Work

Learning paradigms for HRC. Conventional HRC treats humans as reactive environment components via predefined scripts (Jaderberg et al., 2019), limiting coordination to finite interaction patterns (Foerster et al., 2018). Such single-agent formulations or imitation learning fail to generalize to nonstationary human behaviors (Vinyals et al., 2019; Raileanu et al., 2018). Therefore, the transition to co-adaptation is imperative for handling latent human intentions (Sarkadi et al., 2018). This work circumvents this by replacing scripts with learning-capable humanoid agents, and using MARL to force the robot to internalize a broader distribution of coordination patterns (Strouse et al., 2021).

Stability in MARL. MARL instability stems from differentiable game dynamics, where non-symmetric Jacobians and solenoidal vector fields induce rotational behaviors that obstruct convergence (Balduzzi et al., 2018; Zhao et al., 2023; Kim et al., 2021). Centralized training with decentralized execution (CTDE) methods address this via value factorization (Rashid et al., 2020; Son et al., 2019; Wang et al., 2020) or trust-region heuristics (Gu et al., 2021), yet they regularize update magnitudes rather than geometric directions. In contrast, our HALO algorithm analyzes the Lyapunov descent condition to neutralize the cyclic divergence in heterogeneous gradients (Fiez et al., 2020).

Lyapunov methods in RL. In safe RL, Lyapunov functions are used as certificates to enforce constraint-satisfaction conditions during learning (Chow et al., 2018), sometimes augmented by additional safety tools, including barrier function (Sikchi et al., 2021). More broadly, Lyapunov-based tools have been used to ensure stability of learned dynamics models (Kolter & Manek, 2019) and to infer stability certificates directly from data, extending a long tradition in nonlinear systems analysis (Boffi et al., 2021). Despite these advancements, there is little exploration of using Lyapunov functions to directly certify the stability of policy-parameter learning dynamics in MARL (Leonardos et al., 2021). This work moves in this direction by applying Lyapunov principles on policy-parameter space, inducing a contracting potential even under non-stationary updates.

Gradient alignment and geometry. Geometric heuristics like PCGrad (Yu et al., 2020) mitigate conflicts by projecting gradients with negative similarity, yet they lack global invariants over the learning trajectory. More robust geometric approaches involve Riemann-Finsler metrics (Yang & Nachum, 2021) or mirror descent on the simplex (Shani et al., 2020). Frameworks like heterogeneous mirror learning provide unified convergence guarantees for multiobjective settings (Zhong et al., 2024). Our HALO extends geometric intuitions toward a Lyapunov-based perspective on learning dynamics, using stability principles to formalize contraction properties that promote coordination. The full algorithmic details appear in the following section.

## 3. Preliminaries

## 3.1. Decentralized POMDPs

HRC tasks use a decentralized partially observable Markov decision process (POMDP) M = ⟨S, A, P, R, γ, N, O, Z⟩ (Foerster et al., 2018). Unlike parameter sharing, heterogeneous agents rely on independent policies πθi(ai,t|oi,t) given local observations oi,t = Z(st, i). The parameter vector is defined as θ = [θ⊤

1,..., θ⊤ N]⊤∈RD. Agents share a global reward rt = R(st, at) and the objective is to maximize the return J(θ) = Eat∼πθ,st∼P [P∞ t=0 γtR(st, at)].

<!-- Page 3 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

Agent

Agent Decentralized execution

Infinite interaction space

Collaboration

Interference

Final parameter update

Independent rationality

Team rationality

Differentiable gradient fields

Lyapunov policy optimization

Hessian-vector product Lyapunov rationality gap

Stability normal vector Lyapunov-constrained optimization

Analytic closed-form projection

KKT condition

Centralized training

Lyapunov policy optimization

Real-world collaboration

Policy

MoCap

**Figure 1.** The HALO framework architecture combining the transition from standard decentralized learning to Lyapunov policy

optimization for real-world HRC. Key components include the computation of the rationality gap V (θ) and the stability normal vector h to derive the final analytic closed-form projection d∗.

## 3.2. Decoupled CTDE and the stationarity assumption

Under the CTDE paradigm (Yu et al., 2020), each agent independently updates its parameters for heterogeneous embodiments, where ˆAtot is a centralized advantage estimator: ∇θiJi(θi) = E h

∇θi log πθi(ai|oi) ˆAtot(s, a)

i

. The concatenation of these updates forms an independent rationality field [∇θ1J⊤

1,..., ∇θN J⊤ N]⊤, computed as if the partner’s policies πθ−i were part of a fixed environment component. This implicitly assumes partner stationarity.

## 3.3. Learning dynamics and rationality gap

A fundamental pathology in decoupled architectures is that uind(θ) constitutes a non-conservative vector field (Balduzzi et al., 2018). Because agent parameters are independently updated, the joint Jacobian is non-symmetric, ∇θj∇θiJi̸ = ∇θi∇θjJj, inducing rotational components that lead to limit cycles and divergent trajectories (Zhao et al., 2023). The structural mismatch in HRC creates a rationality gap between the decentralized update directions and the true team-level ascent direction ∇J(θ).

## 4. Methodology: The HALO Framework

We design a stability-aware control law that rectifies decentralized gradients to satisfy a convergence certificate, as illustrated in Fig. 1.

## 4.1. Vector field misalignment and Lyapunov stability

Let θ = [θ⊤

1,..., θ⊤ N]⊤∈RD represent the joint parameter vector of N heterogeneous agents. In the CTDE paradigm with decoupled architectures (Zhao et al., 2023), the learning dynamics are governed by the interaction between local agent intentions and the global team objective. We formalize this interaction via two competing vector fields:

## 1 The independent rationality field (uind):

This field is formed by the concatenation of individual actor gradients. For each agent i, the update is driven by a local surrogate Ji(θi) = Eai∼πθi[Qtot(s, a)], which assumes other agents’ policies are momentarily stationary:

uind(θ) ≜[∇θ1J⊤

1,..., ∇θN J⊤ N]⊤∈RD. (1)

## 2 The team rationality field (uteam):

This represents the true ascent direction of the global team reward function J(θ) = Ea∼πθ[P t γtrt]. Under the chain rule in the joint parameter space, it defines the team rationality field:

uteam(θ) ≜∇θJ(θ) =

"

∂J ∂θ1

⊤

,..., ∂J

∂θN

⊤#⊤

∈RD.

(2)

In this formulation, we define the rationality gap, the Variational mismatch between decentralized best-response dynamics and centralized cooperative dynamics, via a Lyapunov candidate function as the discrepancy:

V (θ) ≜1

2∥uind(θ) −uteam(θ)∥2 2. (3)

Structural pathology: In heterogeneous MARL, uind is generally non-conservative (Balduzzi et al., 2018). With decoupled parameters, the Jacobian Hind ≜∇θuind is nonsymmetric, as cross-terms ∇θj∇θiJi and ∇θi∇θjJj differ. By Helmholtz decomposition, uind = ∇Φ + Ψ, where the solenoidal component Ψ drives limit cycles and oscillations

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-003-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

(Zhao et al., 2023). V (θ) monitors this dissonance and our control objective is to design an update d realizing

⟨∇θV, d⟩≤−σV (θ), σ > 0, (4)

enforcing a Lyapunov dissipation constraint for asymptotic contraction of the rationality gap and stabilizing decentralized learning.

## 4.2. Structural stability and analytic projection

Standard decentralized updates θk+1 = θk+ηuind prioritize local greedy progress but frequently increase the rationality gap V (θ) (Dai et al., 2025). To ensure structural stability, we seek an optimal update direction d∗that strictly satisfies a Lyapunov stability certificate (Yang et al., 2020). This is formulated as a constrained quadratic program:

min d∈RD

1 2∥d −uind(θk)∥2 2 s.t. ⟨∇θV (θk), d⟩≤−σV (θk).

(5)

Eq. (5) performs a minimum-norm projection of uind onto the stability half-space Hstable = {d ∈RD | ∇V ⊤d ≤ −σV }. This functions as a structural stability certificate based on decentralized gradients. The Karush-Kuhn-Tucker (KKT) conditions permit an exact analytic solution (Clempner, 2016). Let h ≜∇θV (θk) denote the gradient of the disagreement and we define the Lagrangian as:

L(d, λ) = 1

2∥d −uind∥2 2 + λ h⊤d + σV

, (6)

where λ is the dual variable. For optimal update d∗, the stationarity condition ∇dL = 0, combined with the primal feasibility h⊤d∗+ σV ≤0 and complementary slackness λ(h⊤d∗+ σV) = 0, reveals the structure d∗= uind −λh. To determine the optimal multiplier λ∗, we substitute the stationarity condition into the slackness equation:

λ h⊤(uind −λh) + σV

= 0

=⇒λ(h⊤uind −λ∥h∥2

2 + σV) = 0. (7)

Solving Eq. (7) identifies two operational regimes: an inactive regime where h⊤uind + σV ≤0 (yielding λ∗= 0). Unifying these cases via the rectifier function yields the HALO projection operator, where ϵ is a damping constant:

d∗= uind −max

0, ⟨h, uind⟩+ σV ∥h∥2

2 + ϵ h (8)

## 4.3. Scalability via Hessian-vector product

A primary concern regarding Lyapunov-based optimization is the perceived second-order complexity. The vector h =

## Algorithm

1 HALO practical implementation

Require: Initial joint policy θ0, critic Qϕ, hyperparameters η, σ, ϵ 1: for iteration k = 0, 1,... do 2: Sample mini-batch D ∼πθk 3: {Step 1: Compute differentiable gradient fields} 4: uind ←∇θLind|θk with create graph=True 5: uteam ←∇θLteam|θk with create graph=True 6: {Step 2: Obtain stability normal h via HVP} 7: V ←1

2∥uind −uteam∥2 2 8: h ←∇θV |θk ▷Double back-prop pass 9: {Step 3: Stability-constrained projection} 10: ψ ←⟨h, detach(uind)⟩+ σ · detach(V) 11: λ∗←max

0, ψ/(∥h∥2 2 + ϵ)

12: {Step 4: Update parameters and critic} 13: d∗←detach(uind) −λ∗h 14: θk+1 ←θk + ηd∗

15: Update ϕ by minimizing LMSE(Qtot, y) 16: end for

∇θV requires differentiating through the gradient fields, involving a Jacobian-vector product:

h = ∇θ

1

2∥uind −uteam∥2 2

= (Hind −Hteam)⊤(uind −uteam),

(9)

where H denotes the Jacobian of the respective vector fields. While explicit O(D2) Hessian construction is intractable, HALO leverages double back-propagation to compute Eq. (9) as a Hessian-vector product (HVP). This procedure, detailed in Algorithm 1, by retaining the computational graph, the backward pass on V yields the required product without ever materializing the full Hessian matrix. The detailed step-by-step derivation is provided in Appendix A.1.

## 5. Theoretical Analysis

Assumption 5.1 (Regularity and smoothness). The team objective J(θ) is C2-continuous and the Lyapunov potential V (θ) is L-smooth on the parameter manifold Θ. That is, ∥∇θV (θ1) −∇θV (θ2)∥2 ≤L∥θ1 −θ2∥2 for all θ1, θ2 ∈ Θ.

## 5.1. Monotonic descent of the rationality gap

HALO transforms a potentially oscillatory decentralized learning process into a dissipative dynamical system.

Theorem 5.2 (Monotonicity of potential decay). Under Assumption 5.1, let {θk}∞ k=0 be the sequence of parameters generated by the HALO update law. If the learning rate η satisfies the stability bound η ≤2σV (θk)/(L∥d∗ k∥2

2), then

<!-- Page 5 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

Robot trajectory

Training in parallel

Start point

(a) Simulation infrastructure and task snapshots.

0.00 0.25 0.50 0.75 1.00 1.25 1.50 1.75 2.00 Step (-) 1e9 0.0

1.0

2.0

3.0

4.0

Cumulative reward (-)

HALO PCGrad HATRPO HAPPO

(b) Learning dynamics (cumulative reward).

**Figure 2.** Simulation benchmark and learning dynamics: (a) massively parallelized training infrastructure in Isaac Lab, where the arrows

indicate the emergent synergy collaboration; (b) performance comparison across nine scenarios, where HALO demonstrates significantly faster convergence, reaching its performance plateau at approximately 1.3B steps.

the rationality gap V (θ) is monotonically non-increasing:

V (θk+1) −V (θk) ≤−ησV (θk) + Lη2

2 ∥d∗ k∥2

2. (10)

Summary. The proof utilizes the descent Lemma for Lsmooth functions. By solving the KKT conditions for the stability-constrained projection, we show that the update direction d∗ k always maintains a dissipative inner product with the stability gradient, ⟨∇V, d∗⟩≤−σV. The detailed algebraic derivation is provided in Appendix A.2.

## 5.2. Asymptotic convergence to equilibrium

Beyond local stability, we establish that HALO drives the multi-agent system toward a state of rationality agreement. Theorem 5.3 (Convergence to the synergy manifold). Suppose V (θ) is bounded below by 0 and the learning rate {ηk} satisfies the Robbins-Monro conditions (P ηk = ∞, P η2 k < ∞). Then, the sequence of disagreement energies {V (θk)}∞ k=0 converges to zero. Consequently:

lim k→∞∥uind(θk) −uteam(θk)∥2 = 0. (11)

Summary. We construct a summable sequence of the potential energies and apply the monotone convergence theorem. The divergence of P ηk ensures that the Rationality Gap must vanish asymptotically. The convergence V →0 implies that the limit points of HALO are stationary points where decentralized preferences ∇θiJi are aligned with global team ascent directions. The complete measuretheoretic treatment is provided in Appendix A.3.

## 6. Experiments and Results

## 6.1. Experimental setup

Embodied task suite and test setup. We study three continuous-space coordination tasks: (1) Orientationsensitive pushing (OSP): pushing an object through a

OSP SCT SLH Task Category (-)

70

75

80

85

90

Success Rate (%)

HAPPO HATRPO PCGrad HALO

**Figure 3.** Comparison of HALO and baseline MARL algorithms

across the nine scenarios in OSP, SCT and SLH tasks.

directional opening requiring precise yaw alignment. (2) Spatially-confined transport (SCT): transport through narrow passages requiring synchronized velocity and tight spatial coordination. (3) Super-long object handling (SLH): transporting a long board via coordinated pivoting and shuffling maneuvers. The training is performed in the Isaac Lab (Mittal et al., 2023), and the physical experiments are conducted on a Unitree G1 robot cooperating with a human partner with reliance on motion-capture (MoCap) system. The detailed test settings are provided in Appendix B.

Baselines and metrics. We evaluate HALO against stateof-the-art heterogeneous MARL methods: (1) HAPPO and HATRPO, representing the sequential trust-region paradigm; (2) PCGrad, a baseline integrates the HAPPO architecture with gradient surgery. Performance is quantified via success rate (SR), gradient alignment cos(ϕ) (Align), the rationality gap V (θ) (Gap) and gradient conflict rate (GCR) as the primary stability indicator.

## 6.2. Performance benchmark in simulation

We demonstrate the performance superiority of HALO across physical coupling tasks including OSP, SCT and SLH, shwon in Fig. 2a and the cumulative reward is visualized in Fig. 2b. Besides, Fig. 3 further illustrates the scenario-specific success rates. As synthesized in Table 1, in

![Figure extracted from page 5](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-005-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

**Table 1.** Comprehensive performance matrix and global optimization analysis of heterogeneous coordination: the upper part evaluates the

scenario-specific success rate across nine representative coordination challenges in OSP, SCT and SLH tasks, reported as mean ± std. The lower part provides a synchronized mechanism analysis at the 2B-step steady state, correlating overall task proficiency with fundamental optimization metrics including Overall success rate, convergence, final return, gradient alignment (cos ϕ), rationality gap (V) and gradient conflict rate. Bold and underlined indicate first and second best, respectively.

Task category Scenario name HAPPO HATRPO PCGrad HALO (Ours) Improvement

OSP

Alignment 83.6 ± 5.3 87.9 ± 4.5 87.7 ± 3.8 92.8 ± 3.0 +5.6% Turnaround 77.6 ± 6.3 81.5 ± 5.5 83.6 ± 4.8 86.7 ± 3.5 +3.7% Corner entry 72.7 ± 7.0 75.3 ± 6.0 77.8 ± 5.3 82.2 ± 4.0 +5.7%

OSP average 78.0 ± 6.3 81.6 ± 5.3 83.0 ± 4.5 87.2 ± 3.5 +5.1%

SCT

Narrow gate 80.1 ± 4.8 83.4 ± 4.3 88.6 ± 3.5 91.1 ± 2.8 +2.8% S-shaped path 76.3 ± 5.8 82.1 ± 5.0 80.6 ± 4.5 84.9 ± 3.8 +3.4% U-shaped path 75.7 ± 6.5 79.2 ± 5.3 81.3 ± 4.8 85.1 ± 4.3 +4.7%

SCT average 77.4 ± 5.8 81.6 ± 4.8 83.5 ± 4.3 87.0 ± 3.5 +4.2%

SLH

Facing mode 79.3 ± 5.0 84.4 ± 1.6 83.2 ± 3.5 88.2 ± 2.8 +4.5% Lateral shuffle 73.7 ± 6.8 75.9 ± 5.8 77.3 ± 5.0 80.7 ± 4.5 +4.4% Pivoting 74.9 ± 6.0 77.5 ± 5.3 78.6 ± 4.5 82.3 ± 3.8 +4.7%

SLH average 76.0 ± 6.0 79.3 ± 5.0 79.7 ± 4.3 83.7 ± 3.8 +5.0%

Learning stability and mechanism analysis (steady-state at 2B steps)

## Algorithm

Overall SR ↑ Conv. step ↓ Final return ↑ Align cos ϕ ↑ Gap V ↓ GCR ↓

HAPPO 77.1% 1.8B 3.44 0.67 4.89 72.5% HATRPO 80.8% 1.3B 3.60 0.68 1.53 54.2% PCGrad 82.1% 1.2B 3.76 0.84 0.20 25.0% HALO 86.0% 1.3B 4.02 0.91 0.09 4.2%

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9 0.0

1.0

2.0

3.0

4.0

5.0

Rationality gap V() (-)

HALO PCGrad HATRPO HAPPO

(a) Rationality gap V (θ)

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9 0.2

0.4

0.6

0.8

Alignment cos() (-)

HALO PCGrad HATRPO HAPPO

(b) Gradient alignment cos(ϕ)

**Figure 4.** Optimization dynamics analysis: (a) monotonic dissi-

pation of V (θ) under the Lyapunov stability certificate; (b) rapid convergence of gradient alignment. HALO eliminates solenoidal components to stabilize the joint parameter manifold.

the OSP task, HALO achieves an average SR of 87.2%, outperforming HATRPO (81.6%) and HAPPO (78.0%). These results are consistent with our structural pathology analysis, with HALO achieving a rationality gap of 0.09 and the highest alignment score of 0.91. The increased computation time of HVP is diluted by environment sampling and inference in high-throughput settings, with negligible memory overhead (< 21.1%) due to autograd-based HVP without explicit Hessian materialization, and HALO achieves a 13.1% reduction in total wall-clock training time compared to HAPPO.

HAPPO

HATRPO

PCGrad

HALO

## Algorithm

(-)

1.5

2.0

Conv. step / 1e9 (-)

(a)

HAPPO

HATRPO

PCGrad

HALO

## Algorithm

(-)

0.6

0.7

0.8

0.9

1.0

Alignment (-)

(b)

HAPPO

HATRPO

PCGrad

HALO

## Algorithm

(-)

0

2

4

Rationality Gap (-)

(c)

HAPPO

HATRPO

PCGrad

HALO

## Algorithm

(-)

0

25

50

75

GCR (%)

(d)

**Figure 5.** Scalability and algorithm metrics analysis: (a) conver-

gence steps required to reach performance plateau; (b) steady-state rationality gap V; (c) final gradient alignment cos ϕ. (d) gradient conflict rate across algorithms.

## 6.3. Mechanism analysis of HALO

Geometric rectification of the vector field. As shown in Fig. 4(a), Fig. 5 and Table 1, HALO ensures a descent of

<!-- Page 7 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9 0.0

0.2

0.4

0.6

Gap std (-)

HALO PCGrad HATRPO HAPPO

(a) Gap std evolution

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9 0

1

2

3

Alignment std (-)

1e 2

HALO PCGrad HATRPO HAPPO

(b) Alignment std evolution

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9 0

2

4

6

Gap decay rate (-)

1e 9

HALO PCGrad HATRPO HAPPO

(c) Gap decay rate

0.0 0.5 1.0 1.5 2.0 Step (-) 1e9

0.0

0.2

0.4

0.6

0.8

1.0

Alignment change rate (-)

1e 9

HALO PCGrad HATRPO HAPPO

(d) Alignment change rate

**Figure 6.** Detailed mechanism evolution: (a) standard deviation of

rationality gap; (b) standard deviation of alignment; (c) temporal decay rate of the gap; (d) instantaneous change rate of alignment.

V (θ), reaching a steady state of 0.09, while HAPPO shows a gap of 4.89. This is further evidenced by the temporal decay rate of the gap achieved by HALO (Fig. 6).

Stabilization via alignment. Table 1 demonstrates that by projecting uind onto the stability half-space Hstable, HALO achieves a global alignment of 0.91 and reduces the GCR to 4.2%. This geometric rectification, visualized in Fig. 4(b) and in Fig. 6(d), filters out rotational instabilities.

## 6.4. Ablation study and structural robustness

To isolate the contribution of each algorithmic component, an ablation study is conducted as shown in Table 2.

Hard projection vs. Lagrangian penalty. The Soft-V variant, which incorporates V (θ) as a Lagrangian penalty term in the objective, yields only marginal improvements (76.5% SR). This confirms that soft regularization merely modulates gradient magnitude but lacks the geometric necessity to rectify the update direction. Only the hard analytic projection (P) onto the stability half-space Hstable ensures that policy updates strictly enter the contractive set.

Mechanism of adaptive synergy. The progression from static projection to the full HALO framework underscores the synergy between stability and coherence. While P provides the convergence certificate, adaptive scheduling (η)

Robot wrist trajectory Robot hip trajectory

Human wrist trajectory

Human wrist trajectory

(a) Vertical synchronization: adaptive squatting t=0 t=5 t=10 t=12 t=32 t=35 t=45 t=55 t=60 t=70 t=80 t=90

Robot stationary stepping Human obstructed

(b) Movement synchronization: obstruction resilience

**Figure 7.** Micro-view analysis of coordination resilience: (a)

reactive height modulation during unscripted partner motion; (b) stability maintenance during 20s obstructions through stationary stepping and velocity re-synchronization.

and alignment (cos ϕ) further refine the trajectory on the joint parameter manifold. HALO suppresses coordination dissonance, as evidenced by the final gap V of 0.09.

**Table 2.** Ablation matrix on SLH-extreme (pivoting) task. Re-

sults report mean ± std. P: Lyapunov projection; η: adaptive scheduling; cos ϕ: alignment rectification.

Variant P η cos ϕ SR (%) ↑ Gap V ↓

HAPPO baseline × × × 74.9 ± 6.0 4.89 Soft-V penalty × × × 76.5 ± 5.8 3.21 Static projection ✓ × × 79.5 ± 4.8 0.85 HALO w/o align ✓ ✓ × 80.8 ± 4.2 0.24 HALO (full) ✓ ✓ ✓ 82.3 ± 3.8 0.09

## 6.5. Real-world human-robot collaboration

To verify the effectiveness and sim-to-real transferability of HALO for HRC, the real-world evaluation focuses on coordination resilience under partner non-stationarity. We compare HALO against two primary baselines: PCGrad and Robot-Script (see Appendix B.4).

Microview resilience analysis. The effectiveness of HALO

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

Robot trajectory Color-coded temporal progression (orange → purple)

Orientation-sensitive pushing

Super-long object handling

Entry orientation Entry orientation

Narrow passage

Spatially-confined transport

Narrow entrance

Entry orientation

**Figure 8.** Sim-to-real deployment across embodied tasks: macro-view of deployment on OSP (top), SCT (Middle) and SLH (Bottom). Temporal progression is indicated by color gradients; arrows trace the stable trajectories maintained by HALO despite complex physical coupling and human-induced perturbations.

is examined through coordination resilience as shown in Fig. 7. In Fig. 7a, it is observed that the G1 autonomously maintains a horizontal load plane when its partner’s height varies. Furthermore, Fig. 7b demonstrates movement synchronization during unscripted 20s obstructions.

**Table 3.** Real-world performance: metrics are mean values over 5

trials. T: time to destination (s); SR: success rate; DR: object drop rate (%); Ang: absolute value of tilt rate (◦/s); vd: post-halt drift (cm/s); Wait: proactive waiting for partner synchrony.

Task 1: OSP Task 2: SCT

## Method

T ↓ SR ↑ T ↓ DR ↓ Ang ↓

Robot-Script 74.2 100% 101.6 60% 4.3 PCGrad 65.2 100% 81.5 0% 2.4 HALO 61.7 100% 76.2 0% 2.2

Task 3: SLH (Stability Under Halting)

## Method

Wait T ↓ DR ↓ Ang ↓ vd ↓

Robot-Script – – 100% 4.9 – PCGrad ✓ 86.9 20% 2.7 1.59 HALO ✓ 85.6 20% 2.4 1.22

Quantitative analysis. As synthesized in Table 3, HALO exhibits superior coordination resilience. In OSP and SCT tasks, it significantly reduces time-to-destination (76.2 s)

and minimizes tilt rates (2.2◦/s). Notably, in the SLH task, HALO maintains exceptional stability during unscripted human halting; unlike the robot-script baseline, HALO proactively dissipates residual momentum, yielding a minimal post-halt drift of 1.22 cm/s. This performance underscores HALO’s ability to internalize team-level synergy and fluid interaction, as visualized in Fig. 8.

## 7. Conclusion

In this study, we propose HALO to address the inherent structural instabilities in decentralized human-robot collaboration. We establish MARL as a unified paradigm for exploring expansive interaction manifolds, effectively transcending the limitations of traditional scripted human models. We define RG as a variational mismatch between decentralized best-response dynamics and a centralized cooperative ascent direction, reformulating the learning process as a dissipative dynamical system. HALO introduces a formal stability certificate within the policy-parameter manifold, utilizing an optimal quadratic projection to rectify decentralized gradients and ensure the monotonic contraction of coordination disagreement. Our theoretical framework, validated through both large-scale simulations and real-world humanoid deployments, demonstrates that certifying sta-

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-learning-human-robot-collaboration-via-heterogeneous-agent-lyapunov-policy-optim/page-008-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization bility in the parameter space directly translates to superior trajectory coordination and resilience in safety-critical, unstructured environments. Ultimately, HALO provides a foundation for bridging the gap between decentralized individual rationality and global collaborative synergy.

Software and Data

The project website, which includes videos, additional results, the software, and supplementary materials, is available at: https://HaoZhang-THU.github.io/HALO/.

## Acknowledgements

The authors express their gratitude to the ETAIC Lab (https://ETAIC.github.io/) led by Prof. H. Eric Tseng at UTA, for providing the experimental resources and facilities that made this research possible. We also thank Yisen Li (UPenn), John Song (UTA), and all research assistants and volunteers at ETAIC Lab for their technical support during physical deployments and for helping validate the generalization and robustness of the system.

Impact Statement

Assistive human–robot collaboration requires robustness to long-tail and out-of-distribution human behaviors that scripted, replay-based, or imitation-driven paradigms cannot adequately capture. These limitations present a practical bottleneck for deploying collaborative robots in settings where non-stationary human intent and physical coupling make failure costly. This work frames HRC as a MARL problem defined over an effectively infinite interaction space, enabling robots to co-adapt with human partners rather than overfit to predefined trajectories. However, decentralized MARL introduces structural instabilities that impede convergence and prevent reliable collaborative behavior. HALO addresses this challenge by introducing a Lyapunov-stabilized learning kernel that contracts coordination disagreement in parameter space.

The resulting stability-centered formulation provides a scalable foundation for the deployment of collaborative robots in industrial workflows, logistics operations, and assistive environments where mixed-autonomy systems must operate in heterogeneous users, dynamic intent patterns, and rare interaction modes. Potential positive societal impacts include reducing physical workload, expanding human operational capacity, and improving safety in labor-intensive settings. Ethical and deployment considerations are primarily related to safety, transparency, and operational responsibility, as well as potential labor displacement and transition of the workforce in society.

## References

Balduzzi, D., Racaniere, S., Martens, J., Foerster, J., Tuyls,

K., and Graepel, T. The mechanics of n-player differentiable games. In Proceedings of the 35th International Conference on Machine Learning, pp. 354–363, 2018.

Boffi, N., Tu, S., Matni, N., Slotine, J.-J., and Sindhwani, V.

Learning stability certificates from data. In Proceedings of the 2020 Conference on Robot Learning, volume 155 of Proceedings of Machine Learning Research, pp. 1341– 1350, 2021.

Bottou, L., Curtis, F. E., and Nocedal, J. Optimization methods for large-scale machine learning. SIAM Review, 60:223–311, 05 2018.

Carroll, M., Shah, R., Ho, M. K., Griffiths, T., Seshia, S.,

Abbeel, P., and Dragan, A. On the utility of learning about humans for human-ai coordination. Advances in neural information processing systems, 32, 2019.

Chen, M., Li, B., Zhang, S., Zhang, H., Zhuang, W., Yin,

G., and Chen, B. A game-theoretical framework for safe decision making and control of mixed autonomy vehicles. IEEE Transactions on Intelligent Transportation Systems, 27(1):1338–1351, 2026.

Chow, Y., Nachum, O., Duenez-Guzman, E., and Ghavamzadeh, M. A lyapunov-based approach to safe reinforcement learning. Advances in neural information processing systems, 31, 2018.

Clempner, J. B. Necessary and sufficient karush–kuhn– tucker conditions for multiobjective markov chains optimality. Automatica, 71:135–142, 2016.

Clempner, J. B. On lyapunov game theory equilibrium:

Static and dynamic approaches. International Game Theory Review, 20(02):1750033, 2018.

Dai, P., Mo, Y., Yu, W., and Ren, W. Distributed neural policy gradient algorithm for global convergence of networked multiagent reinforcement learning. IEEE Transactions on Automatic Control, 70(11):7109–7124, 2025. doi: 10.1109/TAC.2025.3570065.

Daskalakis, C., Ilyas, A., Syrgkanis, V., and Zeng,

H. Training gans with optimism. arXiv preprint arXiv:1711.00141, 2017.

Duchi, J., Shalev-Shwartz, S., Singer, Y., and Chandra, T.

Efficient projections onto the l 1-ball for learning in high dimensions. In Proceedings of the 25th international conference on Machine learning, pp. 272–279, 2008.

Fiez, T., Chasnov, B., and Ratliff, L. Implicit learning dy- namics in stackelberg games: Equilibria characterization,

<!-- Page 10 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization convergence analysis, and empirical study. In International conference on machine learning, pp. 3133–3144. PMLR, 2020.

Fletcher, R. Practical Methods of Optimization. John Wiley

& Sons, 2013.

Foerster, J., Farquhar, G., Afouras, T., Nardelli, N., and

Whiteson, S. Counterfactual multi-agent policy gradients. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.

Foerster, J. N., Chen, R. Y., Al-Shedivat, M., Whiteson, S.,

Abbeel, P., and Mordatch, I. Learning with opponentlearning awareness. arXiv preprint arXiv:1709.04326, 2017.

Gidel, G., Berard, H., Vignoud, G., Vincent, P., and

Lacoste-Julien, S. A variational inequality perspective on generative adversarial networks. arXiv preprint arXiv:1802.10551, 2018.

Gnecco, G., Sanguineti, M., and Gaggero, M. Suboptimal solutions to team optimization problems with stochastic information structure. SIAM Journal on Optimization, 22 (1):212–243, 2012.

Gu, S., Kuba, J. G., Wen, M., Chen, R., Wang, Z., Tian, Z.,

Wang, J., Knoll, A., and Yang, Y. Multi-agent constrained policy optimisation. arXiv preprint arXiv:2110.02793, 2021.

Gu, S., Kuba, J. G., Chen, Y., Du, Y., Yang, L., Knoll, A., and Yang, Y. Safe multi-agent reinforcement learning for multi-robot control. Artificial Intelligence, 319:103905, 2023.

Hadfield-Menell, D., Russell, S. J., Abbeel, P., and Dragan,

A. Cooperative inverse reinforcement learning. Advances in neural information processing systems, 29, 2016.

Haight, J., Peterson, I., Allred, C., and Harper, M. Het- erogeneous multi-agent learning in isaac lab: Scalable simulation for robotic collaboration. In 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 13446–13451, 2025.

Hempel, A. B., Goulart, P. J., and Lygeros, J. Strong sta- tionarity conditions for optimal control of hybrid systems. IEEE Transactions on Automatic Control, 62(9):4512– 4526, 2017.

Hu, H., Lerer, A., Peysakhovich, A., and Foerster, J. “other- play” for zero-shot coordination. In International Conference on Machine Learning, pp. 4399–4410, 2020.

Jaderberg, M., Czarnecki, W. M., Dunning, I., Marris, L.,

Lever, G., Castaneda, A. G., Beattie, C., Rabinowitz,

N. C., Morcos, A. S., Ruderman, A., et al. Human-level performance in 3d multiplayer games with populationbased reinforcement learning. Science, 364(6443):859– 865, 2019.

Kang, H., Chang, X., Miˇsi´c, J., Miˇsi´c, V. B., Fan, J., and

Liu, Y. Cooperative uav resource allocation and task offloading in hierarchical aerial computing systems: A mappo-based approach. IEEE Internet of Things Journal, 10(12):10497–10509, 2023.

Khalil, H. K. and Grizzle, J. W. Nonlinear systems, vol- ume 3. Prentice hall Upper Saddle River, NJ, 2002.

Kim, D. K., Liu, M., Riemer, M. D., Sun, C., Abdulhai,

M., Habibi, G., Lopez-Cot, S., Tesauro, G., and How, J. A policy gradient algorithm for learning to learn in multiagent reinforcement learning. In Proceedings of the 38th International Conference on Machine Learning, volume 139, pp. 5541–5550, 2021.

Kolter, J. Z. and Manek, G. Learning stable deep dynam- ics models. Advances in neural information processing systems, 32, 2019.

Leonardos, S., Overman, W., Panageas, I., and Pil- iouras, G. Global convergence of multi-agent policy gradient in markov potential games. arXiv preprint arXiv:2106.01969, 2021.

Letcher, A., Foerster, J., Balduzzi, D., Rockt¨aschel, T., and

Whiteson, S. Stable opponent shaping in differentiable games. arXiv preprint arXiv:1811.08469, 2018.

Leung, C.-w., Hu, S., and Leung, H.-f. Modelling the dy- namics of multi-agent q-learning: The stochastic effects of local interaction and incomplete information. In Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI-22, pp. 384–390, 2022.

Li, J., Cheng, X., Huang, T., Yang, S., Qiu, R., and Wang, X.

Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. In Robotics: Science and Systems, 2025.

Lowe, R., Wu, Y. I., Tamar, A., Harb, J., Pieter Abbeel,

O., and Mordatch, I. Multi-agent actor-critic for mixed cooperative-competitive environments. Advances in neural information processing systems, 30, 2017.

Mazumdar, E., Ratliff, L. J., and Sastry, S. S. On gradient- based learning in continuous games. SIAM Journal on Mathematics of Data Science, 2(1):103–131, 2020.

Mesbahi, M. and Egerstedt, M. Graph theoretic methods in multiagent networks. 2010.

<!-- Page 11 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

Mescheder, L., Nowozin, S., and Geiger, A. The numer- ics of gans. In Guyon, I., Luxburg, U. V., Bengio, S., Wallach, H., Fergus, R., Vishwanathan, S., and Garnett, R. (eds.), Advances in Neural Information Processing Systems, volume 30, 2017.

Mittal, M., Yu, C., Yu, Q., Liu, J., Rudin, N., Hoeller, D.,

Yuan, J. L., Singh, R., Guo, Y., Mazhar, H., et al. Or- bit: A unified simulation framework for interactive robot learning environments. IEEE Robotics and Automation Letters, 8(6):3740–3747, 2023.

Nocedal, J. and Wright, S. J. Numerical optimization. Springer, 2006.

Oroojlooy, A. and Hajinezhad, D. A review of coopera- tive multi-agent deep reinforcement learning. Applied Intelligence, 53(11):13677–13722, 2023.

Raileanu, R., Denton, E., Szlam, A., and Fergus, R. Mod- eling others using oneself in multi-agent reinforcement learning. In International conference on machine learning, pp. 4257–4266, 2018.

Rashid, T., Samvelyan, M., de Witt, C. S., Farquhar, G.,

Foerster, J., and Whiteson, S. Monotonic value function factorisation for deep multi-agent reinforcement learning. Journal of Machine Learning Research, 21(178):1–51, 2020.

Samvelyan, M., Rashid, T., De Witt, C. S., Farquhar, G.,

Nardelli, N., Rudner, T. G., Hung, C.-M., Torr, P. H., Foerster, J., and Whiteson, S. The starcraft multi-agent challenge. arXiv preprint arXiv:1902.04043, 2019.

Sarkadi, S¸., Panisson, A. R., Bordini, R. H., McBurney,

P., and Parsons, S. Towards an approach for modelling uncertain theory of mind in multi-agent systems. In International Conference on Agreement Technologies, pp. 3–17. Springer, 2018.

Shani, L., Efroni, Y., and Mannor, S. Adaptive trust region policy optimization: Global convergence and faster rates for regularized mdps. In Proceedings of the AAAI conference on artificial intelligence, volume 34, pp. 5668–5675, 2020.

Sikchi, H., Zhou, W., and Held, D. Lyapunov barrier policy optimization. arXiv preprint arXiv:2103.09230, 2021.

Son, K., Kim, D., Kang, W. J., Hostallero, D. E., and Yi,

Y. Qtran: Learning to factorize with transformation for cooperative multi-agent reinforcement learning. In International conference on machine learning, pp. 5887–5896. PMLR, 2019.

Strouse, D., McKee, K., Botvinick, M., Hughes, E., and

Everett, R. Collaborating with humans without human data. Advances in neural information processing systems, 34:14502–14515, 2021.

Vinyals, O., Babuschkin, I., Czarnecki, W. M., Mathieu, M.,

Dudzik, A., Chung, J., Choi, D. H., Powell, R., Ewalds, T., Georgiev, P., et al. Grandmaster level in starcraft ii using multi-agent reinforcement learning. nature, 575 (7782):350–354, 2019.

Wang, J., Ren, Z., Liu, T., Yu, Y., and Zhang, C.

Qplex: Duplex dueling multi-agent q-learning. ArXiv, abs/2008.01062, 2020.

Wen, M., Kuba, J., Lin, R., Zhang, W., Wen, Y., Wang, J., and Yang, Y. Multi-agent reinforcement learning is a sequence modeling problem. Advances in Neural Information Processing Systems, 35:16509–16521, 2022.

Yang, C., Xu, P., and Zhang, J. Learning individual potential- based rewards in multiagent reinforcement learning. IEEE Transactions on Games, 17(2):334–345, 2024.

Yang, M. and Nachum, O. Representation matters: Of- fline pretraining for sequential decision making. In International Conference on Machine Learning, pp. 11784– 11794, 2021.

Yang, T.-Y., Rosca, J., Narasimhan, K., and Ramadge, P. J.

Projection-based constrained policy optimization. arXiv preprint arXiv:2010.03152, 2020.

Yu, T., Kumar, S., Gupta, A., Levine, S., Hausman, K., and Finn, C. Gradient surgery for multi-task learning. Advances in neural information processing systems, 33:

5824–5836, 2020.

Zhang, H., Lei, N., Li, S. E., Zhang, J., and Wang, Z. Multi- scale reinforcement learning of dynamic energy controller for connected electrified vehicles. IEEE Transactions on Intelligent Transportation Systems, 26(12):22607–22619, 2025.

Zhang, H., Zhao, D., and Tseng, H. E. Cognition to control- multi-agent learning for human-humanoid collaborative transport. arXiv preprint arXiv:2603.03768, 2026.

Zhao, Y., Yang, Y., Lu, Z., Zhou, W., and Li, H. Multi- agent first order constrained optimization in policy space. In Advances in Neural Information Processing Systems, volume 36, pp. 39189–39211. Curran Associates, Inc., 2023.

Zhong, Y., Kuba, J. G., Feng, X., Hu, S., Ji, J., and Yang, Y.

Heterogeneous-agent reinforcement learning. Journal of Machine Learning Research, 25(32):1–67, 2024.

<!-- Page 12 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

A. Detailed theoretical derivations

A.1. Analytical derivation of the stability gradient

The core of HALO’s rectification lies in the gradient of the Lyapunov potential V (θ). Recall that the rationality gap measures the L2 discrepancy between the independent gradient field uind and the team rationality field uteam (Zhang et al., 2026; Clempner, 2018):

V (θ) ≜1

2∥uind(θ) −uteam(θ)∥2 2. (12)

To compute the stability normal vector h ≜∇θV, we apply the multivariate chain rule to the inner product. Let e(θ) = uind(θ) −uteam(θ) denote the error vector. The gradient is derived as follows (Mesbahi & Egerstedt, 2010):

## 1 Vector-valued chain rule:

The gradient ∇θV is the product of the jacobian of the error field and the error vector itself:

∇θV =

∂e

∂θ

⊤ e =

∂uind

∂θ −∂uteam

∂θ

⊤

(uind −uteam). (13)

## 2 Jacobian components: We define

Hind ∈RD×D as the jacobian of the independent field. In decentralized MARL, this matrix is generally non-symmetric, reflecting the underlying geometry of multi-agent learning dynamics (Leung et al., 2022):

Hindjk = ∂uindj

∂θk

. (14)

Correspondingly, Hteam ∈RD×D is the hessian of the global team objective J(θ) (Gnecco et al., 2012):

Hteamjk = ∂2J ∂θj∂θk

. (15)

## 3. Final analytic form: The stability normal h is thus:

h = (Hind −Hteam)⊤(uind −uteam). (16)

A.2. Explicit derivation of the stability-constrained projection

We assume V (θ) is L-smooth on the parameter manifold Θ. For any two points θ, θ′ ∈Θ, the L-smoothness property implies (Nocedal & Wright, 2006):

V (θ′) ≤V (θ) + ⟨∇V (θ), θ′ −θ⟩+ L

2 ∥θ′ −θ∥2 2. (17)

Substituting the HALO update law θk+1 = θk + ηd∗ k:

V (θk+1) ≤V (θk) + η⟨∇θV (θk), d∗ k⟩+ Lη2

2 ∥d∗ k∥2

2 (18)

= V (θk) + η⟨h, d∗ k⟩+ Lη2

2 ∥d∗ k∥2

2. (19)

To ensure the monotonic dissipation of the rationality gap V (θ), HALO formulates a quadratic programming problem (Duchi et al., 2008):

d∗= arg min d∈RD

1 2∥d −uind∥2 2 s.t. ⟨∇θV, d⟩≤−σV,

(20)

We define the Lagrangian function L(d, λ) with a multiplier λ ≥0 (Fletcher, 2013):

L(d, λ) = 1

2∥d −uind∥2 2 + λ(h⊤d + σV). (21)

<!-- Page 13 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

The KKT stationarity condition ∇dL = 0 yields (Hempel et al., 2017):

d∗= uind −λh. (22)

Solving λ(h⊤d∗+ σV) = 0:

## 1 Case 1:

If h⊤uind + σV ≤0, then λ∗= 0.

## 2 Case 2:

If h⊤uind + σV > 0, the constraint is active. Substituting d∗into the boundary:

h⊤(uind −λ∗h) + σV = 0 =⇒λ∗= h⊤uind + σV

∥h∥2

2. (23)

The unified closed-form solution is:

λ∗= max

0, ⟨h, uind⟩+ σV ∥h∥2

2 + ϵ

, d∗= uind −λ∗h. (24)

A.3. Asymptotic convergence analysis

From the descent inequality V (θk+1) ≤V (θk) −ηkσV (θk) + Lη2 k 2 ∥d∗ k∥2

2, summing from k = 0 to K:

σ

K X k=0 ηkV (θk) ≤V (θ0) −V (θK+1) + L

2

K X k=0 η2 k∥d∗ k∥2

2. (25)

Under Robbins-Monro conditions (P ηk = ∞, P η2 k < ∞) and bounded gradients ∥d∗∥≤G (Chen et al., 2026; Bottou et al., 2018):

σ

∞ X k=0 ηkV (θk) ≤V (θ0) + LG2

2

∞ X k=0 η2 k < ∞. (26)

Since P ηk diverges, it must hold that lim infk→∞V (θk) = 0. Due to the monotonicity and uniform continuity of the update, we conclude:

lim k→∞V (θk) = 0 =⇒ lim k→∞∥uind(θk) −uteam(θk)∥2 = 0. (27)

This confirms that HALO asymptotically collapses the learning dynamics onto the rationality agreement manifold.

B. Implementation and experimentation details

B.1. Technical details of the hierarchical control architecture

The coordination framework operates via a tri-level control hierarchy designed to decouple long-term mission guidance from high-frequency physical stabilization (Zhang et al., 2025). Each layer operates at a distinct temporal scale and functional scope as specified in table 4.

Top-level global mission planner. At the start of each episode, the system establishes a geometric backbone using the path planning algorithm, which can also be realized alternatively using vision language model (VLM). The A* or VLM planner generates a collision-free path for the object’s center of mass (CoM) based on a static environmental map. This path serves as the reference trajectory for the downstream tactical and execution layers.

Mid-level tactical MARL policy. Operating at 2 Hz (500ms intervals), the mid-level MARL policy acts as the coordination command generator. It receives spatially-sampled waypoints from the global path and generates motion command for whole-body controller (WBC).

Bottom-level whole-body controller. The bottom-level execution is handled by a WBC policy operating at 50 Hz (20ms intervals). This layer ensures the dynamic stability of the G1 humanoid robot by tracking the 11-dimensional (11D) commands generated by the MARL policy. To bridge the frequency gap between the MARL (2 Hz) and WBC (50 Hz) layers, mid-level commands are held constant via a zero-order hold mechanism within each 500ms decision cycle.

<!-- Page 14 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

**Table 4.** Temporal and functional specification of the control hierarchy.

Layer Frequency Update schedule Core functional scope

Top-level N/A Episode initialization Global path planning (A* or VLM) for object CoM Mid-level 2 Hz Tactical MARL policy Motion command generation for collaboration Bottom-level 50 Hz WBC execution Body balancing and motion command tracking

B.2. Observation and command space formulations

To facilitate long-horizon navigation without the computational overhead of recurrent architectures, we implement a dualsnapshot temporal encoding alongside a spatially-sampled look-ahead mechanism. Each agent processes a 210-dimensional observation vector oi, detailed in table 5. The strategic guidance is provided by a sliding window of waypoints {pk}5 k=1 extracted from the A* or VLM-planned global path at fixed curvilinear intervals (1m to 5m) relative to the robot’s current position. All exteroceptive features—including waypoints, partner relative pose, and object geometry—are transformed into the agent’s egocentric local frame to ensure spatial invariance.

**Table 5.** Composition of the 210-dimensional observation space.

Feature domain Dim Description (Egocentric coordinates)

Look-ahead guidance 10 2D XY waypoints sampled via a sliding window along the global path Self-proprioception 13 XY pos/vel, yaw, CoM height, torso pitch, wrist-to-shoulder XYZ Partner observation 13 Relative XY pos/vel, yaw, CoM height, torso pitch, wrist-to-shoulder XYZ Object geometry 18 4 Top-surface corners XYZ, CoM XYZ pos, CoM XYZ vel Contact feedback 4 Contact signals (left/right end-effector contact for both of the agents)

Temporal features 174 Snapshot accumulation (58D per frame × 3 snapshots) Environment awareness 36 36-ray synthetic proximity, normalized as 1 −d/dmax

Total observation 210 Input to the 2 Hz tactical MARL policy

The command space utilizes a delta-over-base mechanism for precise end-effector coordination. As shown in table 6, the MARL policy modulates a 3D spatial offset (∆p) superimposed onto a task-specific base pose.

**Table 6.** MARL command space specification (11D).

Command set Dim Formulation Physical meaning

Locomotion base 3 Absolute Target velocities [vx, vy] and orientation (yaw angle) Postural setpoints 2 Absolute Target CoM height (HCoM) and torso pitch (αtorso) Wrist modulation 6 Relative delta 3D XYZ offset added to task-specific base poses for both Wrist

B.3. Hyperparameters and training configuration

The tactical coordinator is implemented via a shared-parameter HAPPO framework. This architecture facilitates CTDE, effectively mitigating the non-stationarity inherent in multi-agent coordination. Both actor and critic networks utilize a multilayer perceptron (MLP) backbone with hidden layers of [256, 256, 128]. To ensure stable gradient propagation over the 2.0 × 109 steps, we employ orthogonal initialization with a gain of

√

## 2 The optimization process utilizes the

Adam optimizer coupled with a cosine annealing learning rate schedule, balancing exploratory breadth with asymptotic convergence. Detailed hyperparameters are synthesized in table 7.

The training objective is defined through a path-wise reward that prioritizes geodesic progress along the A* or VLM pre-planned object CoM movement trajectory while enforcing structural stability. This formulation provides a dense reward signal that guides agents through non-convex environmental constraints by focusing on incremental advancement.

<!-- Page 15 -->

Learning Human-Robot Collaboration via Heterogeneous-Agent Lyapunov Policy Optimization

**Table 7.** Optimization and topology hyperparameters.

Optimization parameter Value Architecture parameter Value

Learning rate (α) 1.0 × 10−4 Hidden layers (actor/critic) [256, 256, 128] Epochs per update 10 Activation function ReLU Minibatch count 16 Layer initialization Orthogonal Entropy coefficient 0.01 Optimizer Adam Discount factor (γ) 0.99 Weight decay (L2) 1.0 × 10−4

GAE parameter (λ) 0.95 Gradient clipping (∥g∥2) 10.0 Clipping epsilon (ϵ) 0.2 Learning rate schedule Cosine annealing Value loss coefficient 0.5 Total MARL action steps 2.0 × 109

B.4. Baseline robot-script implementation

To evaluate the necessity of the MARL framework and the coordination gains of HALO, we implement a robot-script baseline based on independent PPO (IPPO). This baseline simplifies the HRC into a single-agent control task by modeling the human partner as a stochastic dynamical load source with predefined mobility. The robot-script policy utilizes a MLP backbone with hidden layers of [256, 256, 128], identical to the architecture employed in HALO. To ensure a fair yet rigorous comparison, the action and observation spaces are aligned with those of HALO, with the exception of collaborative features. Specifically, the state of the interactive partner is replaced by the simplified kinematic state of the human proxy (represented as two boxes), which comprises the relative position, velocity, and orientation.

**Table 8.** Stochastic perturbations for simulating human-like dynamical loads.

Noise type Distribution Magnitude Target simulation phenomenon

Vertical jitter Gaussian 2.0 cm Gait-induced oscillations and lifting shifts Velocity noise Uniform 0.1 m/s Non-uniform walking speed and intent changes Yaw perturbation Gaussian 3.0 deg Subtle directional adjustments during transport

**Table 9.** Robot-script training hyperparameters.

Optimization parameter Value Architecture parameter Value

Learning rate (α) 1.0 × 10−4 Hidden layers (actor/critic) [256, 256, 128] Epochs per update 10 Activation function ReLU Minibatch count 16 Layer initialization Orthogonal Entropy coefficient 0.01 Optimizer Adam Discount factor (γ) 0.99 Weight decay (L2) 1.0 × 10−4

Learning rate schedule Cosine annealing Total RL action steps 2.0 × 109

The policy is trained for 2.0 × 109 steps, using the IPPO algorithm. We employ orthogonal initialization and the Adam optimizer with a cosine annealing learning rate schedule to maintain consistency with our HALO framework. To simulate gait-induced oscillations and intentional shifts, multi-axis stochastic noise is injected into the human proxy’s motion. These perturbations, detailed in Table 8, force the robot to implicitly compensate for interaction residuals through individual proprioceptive feedback. The comprehensive training and optimization hyperparameters are provided in Table 9.
