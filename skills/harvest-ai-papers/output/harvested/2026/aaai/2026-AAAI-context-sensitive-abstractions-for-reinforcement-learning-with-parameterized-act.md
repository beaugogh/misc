---
title: "Context-Sensitive Abstractions for Reinforcement Learning with Parameterized Actions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39635
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39635/43596
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Context-Sensitive Abstractions for Reinforcement Learning with Parameterized Actions

<!-- Page 1 -->

Context-Sensitive Abstractions for Reinforcement Learning with Parameterized Actions

Rashmeet Kaur Nayyar*1, Naman Shah*1,2, and Siddharth Srivastava1

1Arizona State University, Tempe, AZ, USA 2 Brown Unviersity, Providence, RI, USA {rmnayyar, shah.naman, siddharths}@asu.edu

## Abstract

Real-world sequential decision-making often involves parameterized action spaces that require both, decisions regarding discrete actions and decisions about continuous action parameters governing how an action is executed. Existing approaches exhibit severe limitations in this setting—planning methods demand hand-crafted action models, and standard reinforcement learning (RL) algorithms are designed for either discrete or continuous actions but not both, and the few RL methods that handle parameterized actions typically rely on domain-specific engineering and fail to exploit the latent structure of these spaces. This paper extends the scope of RL algorithms to long-horizon, sparse-reward settings with parameterized actions by enabling agents to autonomously learn both state and action abstractions online. We introduce algorithms that progressively refine these abstractions during learning, increasing fine-grained detail in the critical regions of the state–action space where greater resolution improves performance. Across several continuousstate, parameterized-action domains, our abstraction-driven approach enables TD(λ) to achieve markedly higher sample efficiency than state-of-the-art baselines.

Code — https://github.com/AAIR-lab/PEARL.git Extended version — https://aair-lab.github.io/Publications/nss-aaai26.pdf

## Introduction

Reinforcement learning (RL) has delivered strong results across a diverse range of decision-making tasks, from discrete action settings like Atari games (Mnih et al. 2015) to continuous control scenarios such as robotic manipulation (Schulman et al. 2017). Yet most leading RL approaches (Schulman et al. 2017; Haarnoja et al. 2018; Schrittwieser et al. 2020; Hansen, Su, and Wang 2024) are designed for either discrete or continuous action spaces—not both. Many real-world problems violate this dichotomy. In autonomous driving, for example, the agent must choose among qualitatively distinct actions (accelerate, brake, turn), each endowed with discrete or continuous parameters such as braking force or steering angle. Such actions—known as param-

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** In a continuous version of the office domain, the agent needs to learn policies for delivering multiple items. Polygonal cells illustrate learned state abstractions, and arrows illustrate learned policies with abstract actions parameterized by parameter intervals. Each arrow corresponds to an interval [a, b) of possible movement values: the solid segment indicates the lower bound a, and the dotted segment indicates the interval width b−a. Narrower dotted segments denote higher precision in the learned action parameters.

eterized actions—require choosing not only the action but also determine its (real-valued) parameters before execution.

While recent methods have made progress in addressing parameterized actions (Xiong et al. 2018; Bester, James, and Konidaris 2019; Li et al. 2022), they largely ignore utilizing the underlying structure inherent in parameterized-action spaces. In navigation tasks, for instance, an agent should adjust movement parameters with high precision near obstacles but can act with much coarser control in open areas. Existing approaches also often rely on carefully engineered dense rewards and environment-specific initializations to facilitate learning or benefit from relatively short “effective horizons” to remain tractable (Laidlaw, Russell, and Dragan 2023). A detailed discussion of related work is in Sec. 5. This paper aims to extend the scope and sample efficiency of RL paradigms to relatively under-studied yet challenging

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

24522

![Figure extracted from page 1](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

class of problems that feature long horizons, sparse rewards, and parameterized actions. We introduce the first known approach called PEARL that automatically discovers structure in parameterized-action problems in the form of conditional abstractions of their state spaces and action spaces. As an illustration, Fig. 1 shows flexible abstraction of the state space and how the policy may require a different extent of action abstraction in different states in the OfficeWorld domain: in the tightly constrained region s8, navigation demands highprecision in action parameters, whereas the more open space of s7 tolerates far coarser abstraction. This contrast highlights why abstractions must capture this variation in the required precision of action parameters across different regions of the state space.

Given an input problem in the RL setting where a state is expressed using discrete and continuous state variables and an action is expressed using continuous or discrete parameters, PEARL learns context-sensitive abstractions while performing TD(λ). It uses a combination of dispersion in TD-error and value-function signals to learn which abstract states and action parameters require finer resolution during learning. Our approach builds upon our recent work on conditional state abstractions (Dadvar, Nayyar, and Srivastava 2023), and introduces new algorithms for learning more general forms of state abstractions alongside abstractions of action parameters.

Our main contributions are: (1) A unifying formal framework for context-sensitive abstractions of continuous state spaces and parameterized actions with continuous arguments; (2) an approach for learning flexible refinements of abstractions; (3) algorithms for learning such state and action abstractions on the fly, during RL, and thereby exploiting latent structural properties of problem instances for efficient learning without any hand-crafting of abstractions; (4) an evaluation of this approach as applied to TD(λ), showing that using this abstraction paradigm with foundational RL paradigms improves their performance beyond state-ofthe-art algorithms.

## Preliminaries

We use the framework of episodic factored goal-oriented Markov decision process (MDP) with parameterized actions (Bertsekas et al. 2011; Hausknecht and Stone 2016; Deng, Devic, and Juba 2022). An MDP M is defined as ⟨V, S, A, T, R, γ, h, s0, G⟩, where V is a set of state variables and the domain of each variable v ∈V is a bounded interval Dvi =

Dmin vi, Dmax vi

⊆R; S denotes the set of factored states defined by V, where a state s ∈S is an assignment of values to all variables in V: s = {vi = xk|vi ∈ V ∧xk ∈Dvi}. We use s(vi) to denote the value of variable vi in state s.

The action set A consists of a finite number of stochastic parameterized actions. Each action a ∈A is a parameterized function al(ap), where al is the action label and ap = ⟨x1,..., xk⟩is an ordered set of k continuous parameters where each parameter xi has a bounded and ordered domain Dxi ⊆R. The complete parameter space is defined as Pa =× k i=1 Dxi. A grounded action ˜ai assigns values to these parameters from their respective domains. The set of all possible grounded actions is denoted ˜ A, and may be infinite given continuous parameters.

The transition function T: S × ˜ A →µS defines a distribution over next states, given a state and a grounded action. The reward function R: S × ˜ A →R assigns scalar rewards to state-action pairs. The discount factor γ ∈[0, 1] determines the weights of future rewards, and h is the episode horizon. s0 is the initial state and G is the set of goal states.

The objective is to learn a policy πM: S →˜ A that when executed from the initial state s0, reaches a goal state in sg ∈ G while maximizing the expected cumulative discounted reward Eπ[Pt=h t=0 γtrt]. We use the RL setting, where both T and R are unknown (Sutton and Barto 1998).

The state-value function V π(s) under a policy π denotes the expected return starting from state s and following π:

V π(s) = Eπ

" h X t=0 γtrt | s0 = s

#

The action-value function Qπ(s, ˜a) gives the expected return starting from state s, executing action ˜a, and thereafter following π:

Qπ(s, ˜a) = Eπ

" h X t=0 γtrt | s0 = s, ˜a0 = ˜a

#

TD(λ) We use TD(λ) (Sutton 1988) for learning the policy π. It combines one-step TD and Monte Carlo methods by weighting updates across multiple future time steps, controlled by the trace-decay parameter λ ∈[0, 1].

Abstraction Abstraction has been recognized as a key mechanism for achieving scalability in long horizon, sparse reward settings (Li, Walsh, and Littman 2006; Shah and Srivastava 2024; Wang et al. 2024). A state abstraction is a mapping α: S →S that assigns each concrete state s ∈S to an abstract state s ∈S, where S is a partitioning of the original state space S. In this work, we define an analogous notion of abstraction for an action, defined as a partitioning of the action-parameter space (formalized in Sec. 3.1).

We now describe our approach for efficiently learning a policy in settings with parameterized actions by automatically learning context-sensitive state and action abstractions.

## 3 Our Approach

The central contribution of this paper is a novel abstraction paradigm for jointly representing and learning state and action abstractions. These abstractions exploit the structure of the environment in order to efficiently learn and represent policies for problems with parameterized actions.

Running example Consider an AI agent in an Office environment (Fig. 1) that must collect and deliver a coffee and a mail between rooms and offices. The state variables include the agent’s (x, y) position with x, y ∈[0.0, 5.0), and two binary variables: c ∈{0, 1} and m ∈{0, 1} indicating whether it is carrying coffee or mail. The agent has four actions to move in the cardinal directions, i.e.,

24523

<!-- Page 3 -->

**Figure 2.** Illustration of a SPA-CAT for Office World.

A = {up(d), down(d), left(d), right(d)}, each with one continuous parameter d ∈[0, 0.5) that determines the movement distance. Actions may result in stochastic displacements along orthogonal directions, and the agent picks or drops items automatically at designated locations. This setting extends the OfficeWorld environment (Icarte et al. 2022) by incorporating parameterized actions. This work builds upon our prior work (Dadvar, Nayyar, and Srivastava 2023) which learned state abstractions with strictly uniform refinements. It did not address the problem of parameterized actions and offered no mechanism for more flexible refinements of abstractions. The abstraction learned in this work has the following desirable properties: (i) The abstractions are flexible—the abstract state boundaries are not constrained to be orthogonal or axis-aligned. This flexibility allows the learned abstractions to better adapt to the geometry and dynamics of the environment—for example, by placing boundaries where agent behavior changes, following the contours of obstacles. Fig. 1 illustrates an example of such a state abstraction for Office World, where each colored region represents a distinct abstract state. (ii) Moreover, each abstract state has a conjoined action parameter tree for each action (shown in Fig. 2), allowing varying levels of precision in different abstract states. E.g., in open areas—such as the centers of rooms (e.g., abstract state s7)—the agent can move freely without requiring high precision in selecting movement distances (e.g., abstract action left([0.25,0.5))). In contrast, in more constrained areas—such as corridors, near obstacles, or narrow passages (e.g., abstract state s8)—precise control over movement is crucial (e.g., abstract action left([0.0,0.1))). Fig. 2 shows the unified state-action abstraction tree, where the leaves represent these abstract states and abstract actions. The shown abstractions capture the required higher precision for selecting action parameters. We hypothesize that automatically identifying such meaningful abstract states and corresponding action parameter trees can significantly improve sample efficiency in policy learning.

We now define our unified framework for jointly representing both state and action abstractions.

## 3.1 State and Action Abstractions

This section formalizes our representations for state and action abstractions, beginning with action parameter abstractions, followed by an integrated representation for state and action abstractions. We use action parameter trees (APTs) to formalize the intuitive example of action parameter abstractions discussed above. Each node in an APT represents a susbset of the parameter space of an action, and its children nodes together represent a partition of that subset. Formally, given a parameterized action a ∈A with a complete parameter space Pa, we define a corresponding APT as follows: Definition 3.1 (Action Parameter Tree (APT)). An APT τ is a directed hierarchical structure defined as a tuple ⟨N, E, N0, ℓ⟩where N is a set of nodes, E is a set of edges such that each (u, v) ∈E represents a directed edge from node u to node j. N0 is the root node. ℓ: N →2P defines a labeling function that maps each node ni ∈N to a subset of the parameter space such that ℓ(N0) = P, the complete set of parameter values. The set of all children nodes {nj}{j=1,...,k} of node ni represent a partition of ℓ(ni), i.e, ∪j=1,...,k ℓ(nj) = ℓ(ni) with labels of children nodes representing mutually exclusive sets.

Given an APT τa for a parameterized action a ∈A, we define Lτ ⊆Nτ as the set of leaf nodes or the “fringe” of τa. The tree structure is learned autonomously so that at any stage of learning, the fringe of an action’s APT represents the current abstraction of its parameter space. In this way, the fringe of τa can be used to define a set of abstractly grounded versions of a, where each version picks its parameters from one of the leaves of Lτ.

Formally, the set of abstract parameter sets defined by an APT τ for an action labeled a is defined as ¯ Aτ = {ℓ(n)|n ∈ Lτ}. Given a concrete action a(q) and an APT τ for a, we use ¯qτ to denote the unique element of ¯ Aτ that includes q. Thus, a(¯qτ) denotes the abstraction of a(q) under τ. For brevity, we will use the form ¯a to denote an abstract version of a, and ˜a to denote its concrete grounded version (henceforth referred to as a “concrete action”) with realvalued parameters. During RL, we execute an abstract action ¯a = a(¯qτ) by sampling its parameters q uniformly from ¯qτ to obtain a concrete executable action ˜a = a(q).

We define unified state and action abstractions using state and parameterized-action conditional abstraction trees (SPA-CATs). Intuitively, each node of a SPA-CAT defines a subset of the state space and is associated with its own APTs for each action. The structure of the state abstraction part of the tree is congruent with our notion of APTs but applied to the state space. Formally, Definition 3.2 (State and Parameterized Action Conditional Abstraction Tree (SPA-CAT)). A SPA-CAT ∆is a directed hierarchical structure defined as a tuple ⟨N, E, N0, ℓs, ℓa, ⟩, where N is a set of nodes, E is a set of directed edges. Each edge (u, v) ∈E defines a directed edge between nodes u to v. N0 ∈N defines a root node without a parent node. ℓs: N →2S defines a labeling function that

24524

![Figure extracted from page 3](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

maps each node n ∈N to a subset of the state space Sn ⊆S such that ℓs(N0) = S. The set of all children nodes {nj}{j=1,...,k} of a node ni repesent a partition of ℓ(ni), i.e., ∪j=1...,k ℓs(nj) = ℓs(ni), with labels of children nodes representing mutually exclusive sets. ℓa: N × A →Θ maps node ni ∈N and a parameterized action aj ∈A to an APT τaj in the set of all possible APTs, Θ.

SPA-CATs define state and action abstractions as follows. The set of leaf nodes (or the “fringe”) of a SPA-CAT ∆, denoted as L∆⊆N∆, define an abstract state space:

¯S∆= {ℓs(n)|n ∈L∆}. Let n∆(s) denote the unique fringe node of ∆that represents s. The abstraction of a concrete state s under ∆, ¯s∆, is defined as the set represented by the unique fringe element that includes s: ¯s∆= ℓs(n∆(s)). Further, each node n in the fringe is associated with an APT ℓ(n, a) for each a ∈A. This allows us to define the abstraction of a grounded action a(q) relative to a concrete state s and a SPA-CAT ∆, ¯as,∆, as a(¯qτ), where τ = ℓ(n∆(s), a). We omit subscripts when clear from context. In this representation, each abstract state defines its own APTs. This allows the agent to tune the level of precision in each action’s abstraction as a function of the current state. This is particularly conducive for compact expressions of Q(s, a) functions in RL. We now discuss our approach for automatically learning SPA-CATs from scratch during RL.

## 3.2 Learning Abstraction Trees

Throughout this work, we use abstraction trees introduced above to express Q functions. In particular, we express and maintain an abstract Q function as a mapping from the abstract states and actions defined by a SPA-CAT (Sec. 3.1) to R. This allows generalization over unseen state-action pairs using the Q values for their abstractions. This section describes our approach for learning SPA-CATs using state-action trajectories collected using any sequential decision making algorithm; our overall algorithm integrating the decision-making process, data collection, and the invocation of SPA-CAT learning phases is discussed in the next section.

SPA-CATs are learned autonomously through a process of hierarchical refinement. The SPA-CAT ∆is initialized with the universal abstraction where ∆has a single node corresponding to the entire state space, and each action’s APT associated with this node has a single node capturing that action’s entire parameter space. The refinement process creates children nodes for nodes at the fringes of the SPA-CAT and at the fringes of the APTs associated with SPA-CAT nodes. These refinements increase the granularity of abstraction in regions of the state and action spaces where finer distinctions are necessary for high performance decision-making.

Suppose the RL agent encounters a set of execution traces of the form D = {⟨s0, a0, r0,... sn, an, rn⟩} where si is a concrete state, ai is an action executed in si, and ri is the incurred reward for the transition. These traces are abstracted using the current version of ∆to produce ¯D = {⟨s0∆, a0s0,∆, ¯r0,..., sn∆, amsm,∆, ¯rm⟩}. The abstract sequence is constructed to avoid consecutive duplicate abstract states: trajectory subsequences ⟨si, ai, ri,... si+k, ai+k, ri+k⟩whose state-action segments are abstracted to the same pair are represented only once as ⟨si∆, aisi,∆, ¯ri⟩, where ¯ri is the total cumulative discounted reward for the original subsequence.

The learning process aims to create agglomerative abstractions where regions of the state and action space that portend similar futures are grouped together. This indicates that dispersions in the value function estimates of abstract states could be used to identify areas where heterogeneous states are incorrectly being combined into an abstraction. However, during early stages of learning, the agent’s policy can vary significantly, and the paucity of data makes value-function estimates extremely unreliable as indicators of similarity in future courses of action. To balance these considerations, we define a novel hybrid formulation of heterogeneity to identify elements of the current state-action abstraction that need to be refined.

Given abstract traces ¯D, the TD error δ(¯si, ¯ai) for each subsequent abstract state and action is defined as follows:

δ(si, ai) = (¯ri + γ max a Q(si+1, a)) −Q(si, ai) (1)

It is well-known that value-function is inaccurate at start of Q-learning, thus unsuitable for early refinement, whereas, TD-error better represents similar futures during early learning (e.g., (Kearns and Singh 1998)). Thus, in early stages of learning, we rely on the value of the temporal difference (TD) error to provide a stronger signal of behavioral inconsistency: if δ(¯s, ¯a) values show a high standard deviation (SD) for an abstract state-action pair in ¯D, then this abstract pair may be representing heterogeneous regions where the Q function is changing at significantly different rates. On the other hand, as learning progresses and the policy stabilizes, value function estimates become more reliable. At this point the variability of value-function estimates across concrete states in an abstract state are a better indicator of heterogeneity in the abstraction. Therefore, we blend TD error and value-function dispersion metrics. Since it is infeasible to maintain a tabular representation (e.g., a Q-table) over all continuous concrete states and actions, we compute an estimate of the concrete-state value function as follows:

ˆV (si) = ri + γ max a Q(si+1, a) −Q(si, a) (2)

This allows us to estimate the value function for a state using a learned Q-value function for abstract states and abstract actions. We capture the dispersion of ˆV estimates across all n concrete states si present in the dataset D.

We combine the standard deviation over TD errors and over V function estimates into a novel heterogeneity estimate for state-action pairs in ¯D:

H(si, ai) = β · SD ¯ D [δ(¯si, ¯ai)] +

(1 −β) · SDD h

ˆV (si)

i si∈si

(3)

Here, the standard deviation is computed over all occurrences of the pair ¯si, ¯ai in ¯D. A scheduling mechanism is used to gradually shift emphasis from TD error dispersions to value function dispersions. This is achieved with a weighting parameter β, initialized at 1.0 and annealed across

24525

<!-- Page 5 -->

**Figure 3.** Learned state abstractions using flexible (left) and uniform (right) refinement strategies. The agent is at the top left; it must deliver both coffee and mail to the bottom right. Black lines and regions indicate obstacles. Colors represent actions (yellow: right, green: down, red: up, blue: left).

episodes by a decay schedule. States with high heterogeneity, under the current β, are selected for refinement into finer abstractions.

We rank each abstract state-action pair using the computed heterogeneity H and select top-k abstract states and abstract actions to refine. We use H(s) = maxa H(s, a) to select abstract states for refinement and use H(s, a) for selecting abstract actions for refinements.

Multiple paradigms can be used for refining the abstract state-action regions that feature a high heterogeneity under this formulation. We consider two paradigms: uniform refinement as proposed in prior work (Dadvar, Nayyar, and Srivastava 2023), and a novel flexible refinement that uses statistical learning. Both state abstractions (nodes for SPA- CATs) and action abstractions (nodes for Action Trees) can be refined using these methods. However, for brevity, we describe them in the context of refining state abstractions.

Uniform refinement Given an abstract state s selected for refinement, uniform partitioning bisects the interval corresponding to each (variable) independently, resulting in an orthogonal binary tree decomposition of the state space (see Fig. 3 (right)). While straightforward, such abstractions are best suited for domains where the Q-function can be factorized into functions over individual state variables and they require extensive refinements to express regions that feature homogeneous value function estimates, but do not constitute hypercubes.

Learning flexible refinements We introduce a novel learning-based approach for constructing flexible refinements. Given an abstract state s selected for refinement and the associated set of execution traces, we partition s into at most K finer abstract states by clustering the concrete states contained within s. Specifically, we apply Agglomerative Clustering (Murtagh and Contreras 2012) from scikit-learn (Pedregosa et al. 2011) with an adaptive distance threshold: starting from 0.1, we incrementally increase the threshold by 0.001 until the number of clusters is below a specified maximum. This prevents over-fragmentation while ensuring meaningful behavioral distinctions are captured. We use the following similarity criterion to form coherent partitions that

## Algorithm

1: PEARL

Input: MDP M = ⟨V, S, A, T, R, γ, h⟩ Output: Policy π for MDP M and SPA-CAT ∆

1 Initialize SPA-CAT ∆and Qtable Q

## 2 Initialize buffers Ds,a and

Ds,a 3 for episode = 1: nepi do // Learning phase

4 s ←reset()

for step = 1: h do

6 a ←π(Q, s)

7 s′, r, {si, ¯ai, ri,..., sk} ←execute(s, a)

8 Ds,a.add({s, a, r, s′})

9 Q ←updateQvalue(s, a, r, s′)

10 Ds,a.add({si, ai, ri,..., sk})

11 V ←updateValue(s, a, r, s′, s′) // Refinement phase

12 if episode mod nrefine = 0 then

13 Ds,a ←computeHeterogeneity(Q, Ds,a)

14 ¯Sref, ¯ Aref ←findImprecise(Ds,a)

15 if refinement == flexible then

16 Ds,a ← estimateSimilarity(V, Ds,a, ¯Sref, ¯ Aref)

17 C ←cluster(¯Sref, Ds,a)

18 ∆←refine(C, ¯Sref, ¯ Aref)

19 else

20 ∆←refine(¯Sref, ¯ Aref)

## 21 Reinitialize Ds,a and Ds,a

22 return π, ∆ reflect underlying behavioral distinctions:

J(s) = β · ˆδ(s) + (1 −β) · ˆV (s) ˆδ(si) = r(si, a) + γ max a′ Q(si+1, a′) −Q(si, ai), where a = arg max a

H(s, a)

(4)

Here, ˆδ and ˆV are estimated TD-errors and state values for a concrete state, and a is the abstract action with high heterogeneity for an abstract state s. We use a schedule similar to the heterogeneity estimate shift to prioritize using TD-errors estimates earlier in the learning and state-values later in the learning using an annealed parameter β.

Once the partitions are identified, we train an SVM classifier to learn decision boundaries between them and define abstract states, with each partition corresponding to a new abstract state. We use balanced class weights and select the regularization parameter through cross-validation based on the smallest class size, evaluating both RBF and linear kernels. This yields refined abstract states that more effectively capture variations in decision-relevant signals like TD error and value estimates, enabling more expressive abstractions.

We now discuss our algorithm for autonomously learning a SPA-CAT and a policy for a given problem.

24526

![Figure extracted from page 5](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

## 3.3 PEARL Algorithm

Alg. 1 (Parameterized Extended state/action Abstractions for RL, PEARL), outlines the overall process of how SPA- CAT learning is integrated with TD(λ). It starts from an initial, coarse SPA-CAT with a single node N0 and one APT for each action a ∈A with one node each (line 1). It then lets the agent execute in the environment while collecting trajectories and incrementally refining the SPA-CAT. This enables PEARL to jointly learn a SPA-CAT and a policy for the MDP M. It alternates between two main phases: (a) a learning phase (lines 4-11) that trains the policy with a fixed SPA-CAT ∆, and (b) a refinement phase (lines 12-20) that improves the abstraction by refining the SPA-CAT.

Learning phase In this phase, the agent learns an abstract policy π: S →A over the current SPA-CAT structure using tabular TD-λ (Sutton 1988) for nrefine episodes (lines 4–11). During each episode, the agent follows the abstract policy by executing the corresponding abstract action in the current abstract state, continuing until it reaches a new abstract state or the episode terminates (lines 6–7).

Traces obtained during execution Ds,a are used to update Q-values and TD errors over abstract state-action pairs using standard TD(λ) updates (Eq. 1) (lines 8–9), enabling policy improvement in the abstract state space. Moreover, traces over concrete state and abstract action pairs Ds,a are used to approximate values of concrete states (Eq. 2) (lines 10–11).

Refinement phase After every nrefine episodes, PEARL enters the refinement phase to update the SPA-CAT (lines 12-21) via heterogeneity and similarity measures computed using the methods presented in Sec. 3.2 (Eq. 3 and Eq. 4). The SPA-CAT is then used to continue the learning phase.

We now discuss thorough empirical evaluation of our approach in a variety of settings with parameterized actions.

## 4 Empirical Results

We implemented PEARL along with the annealed heterogeneity estimation and abstraction refinement paradigm presented above. This implementation uses a flexible refinement strategy for refining SPA-CATs and a uniform refinement strategy for refining APTs. We evaluate PEARL along three key dimensions: (1) improvements in sampleefficiency, (2) the quality of the learned policies, and (3) the size of the abstractions generated. Our evaluation is conducted across four challenging SOTA RL domains with stochastic and unknown action models, continuous states, parameterized actions, and sparse rewards (a positive reward only upon reaching the goal). Combined with long-horizons, these tasks represent significant challenges for RL.

Test environments We evaluate on domains wellestablished as challenging (illustrated in Fig. 4): (i) OfficeWorld (Icarte et al. 2022; Corazza et al. 2024) (ii) Pinball (Roice et al. 2024; Rodriguez-Sanchez and Konidaris 2024), (iii) Multi-city transport (Ma et al. 2021; Oswald et al. 2024), and (iv) Robot Soccer Goal (Bester, James, and Konidaris 2019). Among these, former three are especially challenging due to longer effective planning horizons.

(a) Office (b) Pinball (c) Soccer Goal

(d) Multi-City Transport

**Figure 4.** (a) Office World: The robot needs to pickup coffee and mail and deliver to the office. (b) Pinball: A small, dynamic ball needs to be manouvered into a red hole, avoiding collisions with irregularly shaped obstacles. (c) Soccer Goal: The white agent needs to kick the small black ball past the red keeper. (d) Multi-City Transport: The agent needs to collect a package from a designated location (marked by blue) in a city and deliver to a target airport (marked by red) in a different city. Cities are connected only via airports.

Baseline selection Standard RL approaches—tabular RL (Sutton 1988; Watkins et al. 1989), deep RL (Mnih et al. 2015; Lillicrap et al. 2015; Schulman et al. 2017; Haarnoja et al. 2018), hierarchical RL (Nachum et al. 2018; Levy et al. 2019)—are not designed to handle parameterized actions, making them unsuitable as baselines. We therefore compare PEARL against two baselines that support parameterized actions: (i) MP-DQN (Bester, James, and Konidaris 2019), which extends P-DQN (Xiong et al. 2018) by combining DQN and DDPG while addressing P-DQN’s overparameterization problem through multi-pass processing, and (ii) HyAR (Li et al. 2022), which learns latent space of hybrid action space and models dependencies between discrete action and continuous parameter using an embedding table and a conditional Variational Auto-Encoder (VAE). To evaluate and compare learning performance fairly without manually biasing learning with head-starts towards favorable solutions, we used the original source code for these baselines while removing their hand-crafted, environmentspecific weight initializations. We replaced them with zero or randomized initializations, whichever yielded better performance. This provides a consistent, unbiased evaluation of each method’s true learning capability.

Metrics and hyperparameters We evaluate all agents using two key metrics: (i) cumulative average return during training, and (ii) the success rate of the learned greedy policy. We evaluate two variants of PEARL—PEARL-flexible and PEARL-uniform—which differ in their approach to learning abstractions. Reported performance of PEARL variants include all episodic interactions used for learning

24527

![Figure extracted from page 6](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

**Figure 5.** Comparison of PEARL-flexible and PEARL-uniform with MP-DQN and HyAR in four domains: Office World, Pinball, Multi-City Transport, and Soccer Goal with mean and standard deviation across 50 independent trials.

state and action abstractions. The results are averaged over 50 independent runs, with both mean and standard deviation reported. Full hyperparameter details for all methods are provided in the extended version.

## 4.1 Analysis of the Results Sample efficiency and performance

Fig. 5 shows the performance of all methods, with training episodes on the x-axis and two rows of metrics on the y-axis: cumulative return (during training) and success probability (during evaluation). Despite learning abstractions from scratch, both PEARL variants consistently outperform the baselines across all domains. This highlights the effectiveness of jointly learning state and action abstractions during RL. Notably, PEARL-flexible achieves the highest overall performance, demonstrating the benefits of adaptive refinement over a fixed, uniform strategy. In contrast, HyAR fails to learn effective policies in all but the Soccer domain, while MP-DQN fails across all tasks. Note that our comparison excludes the additional episodes HyAR requires to gather experience for training its continuous action embeddings, making the advantage of PEARL even more pronounced.

Parsimony of abstractions Among the two PEARL variants, PEARL-flexible offers greater flexibility in controlling abstraction granularity. To investigate how abstraction granularity influences learning, we compare three configurations: two PEARL-flexible variants—aggressive vs. conservative refinement (controlled by varying the maximum number of abstract states allowed for generation per

**Figure 6.** Comparison of training reward and state abstraction size for two PEARL-flexible variants: aggressive and conservative, and PEARL-uniform in Multi-city Transport.

refinement)—alongside PEARL-uniform. Fig. 5 shows how these refinement strategies influence both the quality of the learned policies and the size of the resulting abstractions in the Multi-city Transport domain. The aggressively refined PEARL-flexible variant achieves the highest overall performance, demonstrating the benefits of fine-grained abstractions for precise control. In contrast, the conservatively refined variant achieves comparable performance to PEARLuniform but results in a more compact abstraction. These results highlight a key strength of PEARL-flexible: its abil-

24528

![Figure extracted from page 7](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

**Figure 7.** Comparison of PEARL’s performance across all domains under different settings of the annealing hyperparameter β: TD+V (β=1.0 with a decay of 0.02 applied at each abstraction refinement step), TD (β=1.0), and V (β=0.0).

ity to adjust the level of abstraction granularity based on task requirements, allowing for better tuning of the trade-off between policy performance and representational simplicity.

Impact of annealing parameter Fig. 7 shows that blending dispersion over TD-errors and values yields better performance than relying on either alone. The annealing hyperparameter provides flexibility to smoothly trade off between these signals during training.

Computational cost Experiments show that PEARL has significantly lower runtime than baseline methods since PeARL’s abstraction avoids costly DNN backprops (see the extended version for runtimes).

These results support our hypothesis that jointly learning state-action abstractions improves RL efficiency, enabling TD(λ) to outperform SOTA methods. PEARL-flexible enables principled control over abstraction granularity, balancing computational simplicity and performance.

## 5 Related Work Parameterized actions in RL

Most standard RL methods (Mnih et al. 2015; Lillicrap et al. 2015; Schulman et al. 2017; Haarnoja et al. 2018) are designed for homogeneous action spaces, handling either purely discrete or purely continuous action spaces. Moreover, their success has mostly been limited to settings with short effective horizons, where multi-step lookahead is unnecessary (Laidlaw, Russell, and Dragan 2023). Parameterized actions, which combine discrete actions with associated continuous parameters, present additional challenges they do not address. Some early approaches, such as Q-PAMDP (Masson, Ranchod, and Konidaris 2016) alternate between optimizing discrete actions and their continuous parameters. PADDPG (Hausknecht and Stone 2016) collapses all action parameters into a single continuous vector. These methods do not exploit the inherent structure of the parameterized actions (the dependency between discrete actions and their associated parameters) essential for learning effective policies.

P-DQN (Xiong et al. 2018) directly handles hybrid action spaces without relaxation or approximation by inte- grating a DQN (to deal with discrete actions) and a DDPG (to deal with continuous actions). However, this approach treats all action-parameters as a single joint input to the Qnetwork, which results in dependence of each discrete action’s value on all action-parameters, not only those associated with that action. To overcome the over-parameterization problem of P-DQN, MP-DQN (Bester, James, and Konidaris 2019) extend P-DQN with a multiple-pass mechanism, splitting the action-parameter inputs to the Q-network using several passes. H-PPO (Fan et al. 2019) decomposes the action space using parallel sub-actor networks—one for discrete action selection and others for parameter learning—guided by a shared critic. HyAR (Li et al. 2022) learns a latent representation for hybrid actions via a variational autoencoder, enabling standard DRL algorithms. These methods incur added computational cost due to architectural complexity and hyperparameter sensitivity.

Abstraction refinement in RL Coarse-to-fine RL (CRL) (Seo, Uruc¸, and James 2025) discretize continuous action spaces by learning a single action discretization that spans the entire state space. This is achieved by independently learning a Q-network for each action dimension. In contrast, our method learns distinct abstractions of parameterized actions conditioned on abstract states. Unlike prior topdown abstraction methods limited to discrete actions (Dadvar, Nayyar, and Srivastava 2023; Nayyar and Srivastava 2025), PEARL handles parameterized actions with continuous parameters via action abstraction and supports flexible refinement to compactly capture structure in the problem.

## 6 Conclusion

We introduced a unified state-action abstraction framework with algorithms for learning refinements for an understudied setting of RL with parameterized action spaces. Our contributions are: (i) a formalism for context-sensitive abstractions unifying state and action parameters, (ii) a learningbased method for refining state abstractions flexibly, and (iii) PEARL, an algorithm that jointly learns abstractions during TD(λ). A theoretical analysis of this framework is a good direction for future work.

24529

![Figure extracted from page 8](2026-AAAI-context-sensitive-abstractions-for-reinforcement-learning-with-parameterized-act/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

## Acknowledgments

We thank Shivanshu Verma for helping with an earlier version of this approach. This work was supported in part by NSF under grants IIS 2419809 and IIS 1942856.

## References

Bertsekas, D. P.; et al. 2011. Dynamic programming and optimal control 3rd edition, volume ii. Belmont, MA: Athena Scientific, 1. Bester, C. J.; James, S. D.; and Konidaris, G. D. 2019. Multi-pass q-networks for deep reinforcement learning with parameterised action spaces. arXiv preprint arXiv:1905.04388. Corazza, J.; Aria, H. P.; Neider, D.; and Xu, Z. 2024. Expediting Reinforcement Learning by Incorporating Knowledge About Temporal Causality in the Environment. In Proceedings of Causal Learning and Reasoning. Dadvar, M.; Nayyar, R. K.; and Srivastava, S. 2023. Conditional abstraction trees for sample-efficient reinforcement learning. In Proceedings of Uncertainty in Artificial Intelligence. Deng, Z.; Devic, S.; and Juba, B. 2022. Polynomial time reinforcement learning in factored state MDPs with linear value functions. In International conference on artificial intelligence and statistics. PMLR. Fan, Z.; Su, R.; Zhang, W.; and Yu, Y. 2019. Hybrid actorcritic reinforcement learning in parameterized action space. In Proceedings of the 28th International Joint Conference on Artificial Intelligence. Haarnoja, T.; Zhou, A.; Abbeel, P.; and Levine, S. 2018. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In Proceedings of International conference on machine learning. Hansen, N.; Su, H.; and Wang, X. 2024. TD-MPC2: Scalable, Robust World Models for Continuous Control. In Proceedings of International Conference on Learning Representations. Hausknecht, M.; and Stone, P. 2016. Deep reinforcement learning in parameterized action space. In Proceedings of International Conference on Machine Learning. Icarte, R. T.; Klassen, T. Q.; Valenzano, R.; and McIlraith, S. A. 2022. Reward machines: Exploiting reward function structure in reinforcement learning. Journal of Artificial Intelligence Research, 73: 173–208. Kearns, M.; and Singh, S. 1998. Finite-sample convergence rates for Q-learning and indirect algorithms. Advances in neural information processing systems, 11. Laidlaw, C.; Russell, S. J.; and Dragan, A. 2023. Bridging rl theory and practice with the effective horizon. In Proceedings of Advances in Neural Information Processing Systems. Levy, A.; Konidaris, G.; Platt, R.; and Saenko, K. 2019. Learning multi-level hierarchies with hindsight. In Proceedings of International Conference on Learning Representations.

Li, B.; Tang, H.; ZHENG, Y.; HAO, J.; Li, P.; Wang, Z.; Meng, Z.; and Wang, L. 2022. HyAR: Addressing Discrete- Continuous Action Reinforcement Learning via Hybrid Action Representation. In Proceedings of International Conference on Learning Representations. Li, L.; Walsh, T. J.; and Littman, M. L. 2006. Towards a unified theory of state abstraction for MDPs. AI&M, 1(2): 3. Lillicrap, T. P.; Hunt, J. J.; Pritzel, A.; Heess, N.; Erez, T.; Tassa, Y.; Silver, D.; and Wierstra, D. 2015. Continuous control with deep reinforcement learning. arXiv preprint arXiv:1509.02971. Ma, Y.; Hao, X.; Hao, J.; Lu, J.; Liu, X.; Xialiang, T.; Yuan, M.; Li, Z.; Tang, J.; and Meng, Z. 2021. A hierarchical reinforcement learning based optimization framework for largescale dynamic pickup and delivery problems. In Proceeding of Advances in neural information processing systems. Masson, W.; Ranchod, P.; and Konidaris, G. 2016. Reinforcement learning with parameterized actions. In Proceedings of the AAAI conference on artificial intelligence. Mnih, V.; Kavukcuoglu, K.; Silver, D.; Rusu, A. A.; Veness, J.; Bellemare, M. G.; Graves, A.; Riedmiller, M.; Fidjeland, A. K.; Ostrovski, G.; et al. 2015. Human-level control through deep reinforcement learning. nature, 518(7540): 529–533. Murtagh, F.; and Contreras, P. 2012. Algorithms for hierarchical clustering: an overview. Wiley interdisciplinary reviews: data mining and knowledge discovery, 2(1): 86–97. Nachum, O.; Gu, S. S.; Lee, H.; and Levine, S. 2018. Dataefficient hierarchical reinforcement learning. Advances in neural information processing systems, 31. Nayyar, R. K.; and Srivastava, S. 2025. Autonomous option invention for continual hierarchical reinforcement learning and planning. In Proceedings of the AAAI Conference on Artificial Intelligence. Oswald, J.; Srinivas, K.; Kokel, H.; Lee, J.; Katz, M.; and Sohrabi, S. 2024. Large language models as planning domain generators. In Proceedings of the International Conference on Automated Planning and Scheduling. Pedregosa, F.; Varoquaux, G.; Gramfort, A.; Michel, V.; Thirion, B.; Grisel, O.; Blondel, M.; Prettenhofer, P.; Weiss, R.; Dubourg, V.; et al. 2011. Scikit-learn: Machine learning in Python. the Journal of machine Learning research, 12: 2825–2830. Rodriguez-Sanchez, R.; and Konidaris, G. 2024. Learning Abstract World Models for Value-preserving Planning with Options. In Reinforcement Learning Conference. Roice, K.; Panahi, P. M.; Jordan, S. M.; White, A.; and White, M. 2024. A New View on Planning in Online Reinforcement Learning. Schrittwieser, J.; Antonoglou, I.; Hubert, T.; Simonyan, K.; Sifre, L.; Schmitt, S.; Guez, A.; Lockhart, E.; Hassabis, D.; Graepel, T.; et al. 2020. Mastering atari, go, chess and shogi by planning with a learned model. Nature, 588(7839): 604– 609. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.

24530

<!-- Page 10 -->

Seo, Y.; Uruc¸, J.; and James, S. 2025. Continuous Control with Coarse-to-fine Reinforcement Learning. In Proceedings of Conference on Robot Learning. Shah, N.; and Srivastava, S. 2024. Hierarchical planning and learning for robots in stochastic settings using zero-shot option invention. In Proceedings of the AAAI Conference on Artificial Intelligence. Sutton, R. S. 1988. Learning to predict by the methods of temporal differences. Machine learning, 3: 9–44. Sutton, R. S.; and Barto, A. G. 1998. Reinforcement Learning: An Introduction. Cambridge, MA: The MIT Press. Wang, Z.; Wang, C.; Xiao, X.; Zhu, Y.; and Stone, P. 2024. Building minimal and reusable causal state abstractions for reinforcement learning. In Proceedings of the AAAI Conference on Artificial Intelligence. Watkins, C. J. C. H.; et al. 1989. Learning from delayed rewards. Xiong, J.; Wang, Q.; Yang, Z.; Sun, P.; Han, L.; Zheng, Y.; Fu, H.; Zhang, T.; Liu, J.; and Liu, H. 2018. Parametrized deep q-networks learning: Reinforcement learning with discrete-continuous hybrid action space. arXiv preprint arXiv:1810.06394.

24531
