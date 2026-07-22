---
title: "Fairness Aware Reinforcement Learning via Proximal Policy Optimization"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39434
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39434/43395
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Fairness Aware Reinforcement Learning via Proximal Policy Optimization

<!-- Page 1 -->

Fairness Aware Reinforcement Learning via Proximal Policy Optimization

Gabriele La Malfa1, Jie M. Zhang1, Michael Luck2, Elizabeth Black1

1King’s College London 2University of Sussex gabriele.la malfa@kcl.ac.uk, jie.zhang@kcl.ac.uk, Michael.Luck@sussex.ac.uk, elizabeth.black@kcl.ac.uk

## Abstract

Fairness in multi-agent systems (MAS) focuses on equitable reward distribution among agents in scenarios involving sensitive attributes such as race, gender, or socioeconomic status. This paper introduces fairness in Proximal Policy Optimization (PPO) with a penalty term derived from a fairness definition such as demographic parity, counterfactual fairness, or conditional statistical parity. The proposed method, which we call Fair-PPO, balances reward maximisation with fairness by integrating two penalty components: a retrospective component that minimises disparities in past outcomes and a prospective component that ensures fairness in future decision-making. We evaluate our approach in two games: the Allelopathic Harvest, a cooperative and competitive MAS focused on resource collection, where some agents possess a sensitive attribute, and HospitalSim, a hospital simulation, in which agents coordinate the operations of hospital patients with different mobility and priority needs. Experiments show that Fair-PPO achieves fairer policies than PPO across the fairness metrics and, through the retrospective and prospective penalty components, reveals a wide spectrum of strategies to improve fairness; at the same time, its performance pairs with that of state-of-the-art fair reinforcement-learning algorithms. Fairness comes at the cost of reduced efficiency, but does not compromise equality among the overall population (Gini index). These findings underscore the potential of Fair-PPO to address fairness challenges in MAS.

Code — https://github.com/gabrielelamalfakcl/fairness- aware-ppo Extended version — https://arxiv.org/pdf/2502.03953

## Introduction

In multi-agent systems (MAS), agents interact in an environment to pursue individual or shared goals. Fairness in MAS focuses on whether the reward distribution mechanisms, driven by agent decisions or other processes, treat agents fairly. For instance, fair reinforcement learning explores methods to promote fairness by enabling agents to learn a fair policy (Reuel and Ma 2024); fair division addresses fair resource allocation (Lindner and Rothe 2016; Amanatidis et al. 2023); and negotiation designs methods

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

for fair bargaining resolution (G¨uth and Kocher 2014; Debove, Baumard, and Andr´e 2016).

On the other hand, in human society, fairness is framed in terms of inequality or discrimination between privileged and disadvantaged groups. Sensitive attributes, such as race, gender and socioeconomic status, define subgroups historically marginalised in workplaces, healthcare, education, and politics.1 To enhance fairness, individuals (are often nudged to) adjust their behaviour towards those holding sensitive attributes. For example, giving up a seat on public transport for an elderly person illustrates a behavioural adjustment to promote fairness. For this reason, integrating fairness into agents’ policies has been an area of growing investigation (Reuel and Ma 2024).

Foundational works in social sciences (Griesinger and Livingston Jr. 1973; Liebrand 1984) have identified agents’ attributes as a crucial factor influencing fairness outcomes in games. In this sense, inspired by algorithmic fairness (Mitchell et al. 2021; Castelnovo et al. 2022), we propose sensitive attributes as characteristics that should not affect an agent’s expected reward. We apply metrics from the algorithmic fairness literature, specifically demographic parity, counterfactual fairness, and conditional statistical parity, to the MAS context and use them to constrain agent behaviour and obtain fair policies. Building on gradient-based algorithms in reinforcement learning, and inspired by the work of Zhang et al. (Zhang et al. 2022), we propose a fairness-aware Proximal Policy Optimization (PPO) (Schulman et al. 2017b) method, which we call Fair-PPO, that improves policy fairness. We modify the PPO objective function to include a penalty term derived from a fairness metric, allowing multi-objective optimisation of the policy that accounts for both performance and fairness.

Our proposed penalty has two components. The first component penalises total reward disparities between agents that differ by a sensitive attribute by looking at past outcomes. The second component penalises disparities in the expected rewards as per the estimate of the value function of each agent. In other words, the first component is retrospective, addressing disparities in past outcomes, while the second is

1Throughout the paper, we use the term ‘sensitive attribute’ instead of ‘protected characteristic’ to avoid any confusion with the legal meaning reported, for example, in the UK Equality Act.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22725

<!-- Page 2 -->

prospective, encouraging fairness in the agent’s future expectations and decision-making.

In summary, the main contribution of this work is the novel Fair-PPO reinforcement learning algorithm, which extends PPO with the retrospective and prospective penalty components. We perform experiments in a version of the Allelopathic Harvest (AH) game (Leibo et al. 2019), a MAS that combines cooperation and competition in resource collection, where two groups of agents with different preferences regarding available resources navigate a dynamic environment. Agents are distinguished according to whether they hold some sensitive attribute: agents with this attribute move more slowly and so are potentially disadvantaged in resource collection. Our evaluation of Fair-PPO extends to HospitalSim (HS), a novel hospital simulation. This MAS integrates classification, matching, and resource allocation as agents manage patients with different mobility and priority needs moving through various hospital areas.

Our experiments show that: (i) Fair-PPO produces fairer policies than PPO across the fairness metrics we propose and, through the retrospective and prospective penalty components, reveals a wide spectrum of strategies to improve fairness; (ii) fairness comes at the cost of efficiency but does not compromise equality among the overall population of agents, as measured by the Gini index; and (iii) Fair-PPO is well-suited for finding fair policies in a range of simulation types, from cooperative and competitive to coordinationbased scenarios.

The paper is structured as follows: in Section Related Work, we review the literature on fairness in MAS, fairness in reinforcement learning and algorithmic fairness. Section Preliminaries introduces preliminary concepts of MAS and PPO. In Section Fair-PPO, we detail the fairness metrics and the penalty component integration into PPO. Sections Experiments and Results focus on evaluating our approach, presenting experimental results using AH and HS.

## Related Work

Our work is inspired by algorithmic fairness in seeking to contribute to fair reinforcement learning literature in MAS. We review recent prominent works in these fields.

Fairness Measures in MAS

In MAS, fairness has been evaluated through methods tailored to the system design and objectives. A widely accepted and intuitive notion is proportionality: fairness is determined by the proportion of reward allocated to an agent or group compared to others. Proportionality is applied in many MAS where a resource is allocated to multiple agents, such as the ultimatum game (G¨uth and Kocher 2014; Debove, Baumard, and Andr´e 2016) or fair division games (Lindner and Rothe 2016; Amanatidis et al. 2023; Murhekar 2024). Beyond proportionality, envy-freeness ensures that no agent prefers another’s allocation, and maximin share fairness guarantees that each agent receives a share at least as good as they could secure by dividing resources themselves (Lipton et al. 2004; Budish 2011; Caragiannis, Kurokawa, and et al. 2019).

Alternative fairness measures propose to allocate rewards based on an agent’s merit (Joseph et al. 2016), enhancing treatment equality by equalising error rates across groups (Liu et al. 2017), or minimising regret, which captures the cost of deviating from the optimal trade-off between fairness and efficiency (Li, Liu, and Ji 2020; Patil et al. 2021; Jones, Nguyen, and Nguyen 2023; Barman et al. 2023). Last but not least are wealth distribution metrics such as social welfare (Kaplow and Shavell 2003; Brˆanzei, Gkatzelis, and Mehta 2017; Høgsgaard et al. 2023), which measure the total utility of all individuals based on a chosen outcome, and measures of inequality such as the Gini index (Farris 2010).

Our approach is based on the principle of ensuring a fair distribution of rewards among agents, similar to proportionality and equitable wealth distribution. However, the fundamental distinction lies in the basis of group formation through the sensitive attributes that permit the use of specialised fairness metrics from the algorithmic fairness literature to confront precise biases.

Algorithmic Fairness

Algorithmic fairness addresses bias and discrimination in decision-making systems across domains such as justice (Berk 2019), education (Baker and Hawn 2021), credit scoring (Kozodoi, Jacob, and Lessmann 2022), and healthcare (Vyas, Eisenstein, and Jones 2020), (Giovanola and Tiribelli 2022), with a focus on protected attributes characterising discriminated groups. Fairness metrics are classified into group and individual categories. Group fairness metrics include demographic parity (Kamishima et al. 2012) and equalised odds (Hardt, Price, and Srebro 2016), which use confusion matrix rates, while calibration-based metrics evaluate prediction accuracy relative to group membership (Chouldechova 2016). Individual fairness, such as counterfactual fairness (Kusner et al. 2018), assesses consistency across factual and counterfactual scenarios.

Fairness and Reinforcement Learning

Reinforcement learning traditionally focuses on learning policies that maximise expected rewards (Sutton and Barto 2018). However, this raises fairness concerns, as it can perpetuate biases and violate fairness and legal principles (Jabbari et al. 2017). To address these issues, fairness constraints can be added to the optimisation process. For example, Siddique et al. (Siddique, Weng, and Zimmer 2020) and Zimmer et al. (Zimmer et al. 2021) define fairness as finding solutions that are efficient (benefiting everyone without waste), impartial (treating identical agents equally), and equitable (helping those who are worse off).

Chen et al. (2021) propose adjusting rewards through a multiplicative weight to achieve α-fairness, while Zhang et al. (2014) implement maximin fairness to optimise the worst-performing agent’s outcome. Other works explore fairness across agent groups, including demographic parity (Jiang and Lu 2019; Wen, Bastani, and Topcu 2021; Chi et al. 2022). Some contributions address real-world complexities, such as agents with differing characteristics or

22726

<!-- Page 3 -->

preferences, necessitating tailored fairness mechanisms (Yu, Siddique, and Weng 2023; Ju, Ghosh, and Shroff 2024).

To contextualise Fair-PPO as an algorithm to enhance fairness in decentralised multi-agent reinforcement learning, we benchmark it to FEN (Jiang and Lu 2019) and SOTO (Zimmer et al. 2021). While Fair-PPO, FEN and SOTO all provide solutions to balance efficiency and fairness, they diverge significantly in their architectural and optimisation strategies. Fair-PPO incorporates a penalty term based on tailored fairness definitions, such as demographic parity, into its optimisation objective. FEN adopts a hierarchical learning system and defines a fair-efficient reward to guide agents toward fair outcomes. SOTO, instead, optimises a social welfare function, and it is flexible to fairness metrics adaptation.

## Preliminaries

In this section, we first define the elements composing a MAS and then define gradient-based policies and PPO.

Multi-Agent Systems A MAS consists of multiple agents acting in an environment to achieve their goals. Let N = {1,..., n} be the set of n agents. We denote a MAS as M = (S, s0, A, N, At, P), where S is the set of possible environment states, s0 ∈S is the initial state, A = A1 ×... An is the joint action space, where Ai is the set of actions available to agent i ∈N; At is the set of attributes available to the agents and we designate a single binary sensitive attribute z ∈At for fairness considerations; P: S × A →∆(S) is the non-deterministic state transition function, which maps a state-action pair to a probability distribution over the next states.

We define an agent i ∈N as a tuple of attributes, policy and individual reward function. For the designated sensitive attribute z ∈At, we denote its value for agent i as zi ∈ {0, 1}. This allows us to partition the agents into a sensitive group N1 = {i ∈N | zi = 1} and a non-sensitive group N0 = {i ∈N | zi = 0}. The stochastic policy πi: S → ∆(Ai) of agent i is a function mapping any given state s ∈S to a probability distribution over the agent’s actions Ai. We denote the probability of taking an action ai in state s as πi(ai | s) and the joint policy as π = {π1,..., πn}. The reward function for agent i from state st to st+1, due to the joint action at, is Ri: S ×A×S →R. In this way, an agent i receives a reward rt+1,i = Ri(st, at, st+1).

We define a trajectory or episode as a sequence of states, actions and rewards τ = (s0, a0, r1, s1, a1, r2,...), where at = (at,1,... at,n) is the joint action at time t and rt+1 = (rt+1,1,..., rt+1,n) is the resulting joint rewards. The total reward achieved by an agent i over a trajectory τ of length T is Gi(τ) = PT t=1 rt,i. The probability of a trajectory τ = (s0, a0,..., sT) occurring under a joint policy π is p(τ | π) = p(s0)

T −1 Q t=0

P(st+1 | st, at)

nQ i=1 πi(at,i | st), which is the product of the initial state probability, the environment transition probability and the policy probabilities at each step. The expected reward of an agent i is Ji(π) = P τ p(τ | π)Gi(τ), which is the sum of the total rewards Gi(τ) from every possible trajectory multiplied by the probability of that trajectory.

Proximal Policy Optimization

In reinforcement learning, policy-gradient methods optimise the parameters θ of a policy πθ to maximise the agent’s objective function. These parameters are updated through gradient ascent. To improve the stability of the learning process, modern algorithms implement methods that constrain the policy update, like Trust Region Policy Optimization (Schulman et al. 2017a). PPO works with Clipped Surrogate Objective (CLIP), limiting, within a small range, the change in the probability ratio of actions between the old and new policies.

PPO integrates policy optimisation and value function accuracy into a single objective function as follows:

Lt(θi) = ˆEt

LCLIP t (θi) −c1LVF t (θi) + c2H[πθi](st)

(1)

where t is a timestep, i is the agent and c1 and c2 are weighting coefficient. The objective is composed of the following three components.

The Clipped Surrogate Objective LCLIP constrains the policy update to improve the stability:

LCLIP t (θi) = min ψt(θi) ˆAt,i, clip (ψt(θi), 1 −ϵ, 1 + ϵ) ˆAt,i where ψt(θi) is the ratio of the probability of taking action at under the new policy to the probability of taking it under the old policy; ˆA(t,i) is the advantage function for agent i at step t, which estimates how much better the action at is compared to the average value of the state.

The Value Function Loss improves the accuracy of the policy’s value estimation:

LVF t (θi) = (Vθi(st) −Gt,i)2 where Vθi(st) is the estimate of the return for state st, and Gt,i is the empirical discounted rewards for agent i from state st onwards.

Finally, the Entropy Bonus encourages exploration by promoting more diverse action selection:

H[πθi](st) = −

X ai∈Ai πθi(ai | st) log πθi(ai | st).

Fair-PPO

In this section, we formalise demographic parity, counterfactual fairness and conditional statistical parity in MAS when sensitive attributes are involved; then, we detail the demographic parity-based penalty and integrate it as a constraint into the PPO objective function. The objective function formulations incorporating counterfactual fairness and conditional statistical parity penalties can be found in Section A of the supplementary material.

22727

<!-- Page 4 -->

Fairness Metrics in MAS

Fair-PPO incorporates the notions of demographic parity, counterfactual fairness and conditional statistical parity as a penalty term into the gradient optimisation. These definitions compare the average expected returns of agent groups partitioned by the sensitive attribute z.

Let π be the joint policy. We define the average expected rewards for any subgroup of agents G ⊆N as: ¯JG(π) =

1 |G|

P i∈G Ji(π).

Definition 0.1 (Demographic Parity). In a MAS M, demographic parity is satisfied if the average expected rewards are the same for both sensitive and non-sensitive groups N1 and N0, i.e., ¯JN1(π) = ¯JN0(π). When demographic parity does not hold, we quantify the disparity as the absolute difference between these averages:

∆DP(π) =

¯JN1(π) −¯JN0(π)

(2)

Definition 0.2 (Counterfactual Fairness). Consider a factual system M with joint policy π, and a counterfactual system M′ which is identical to M except that the sensitive attribute z is flipped for all agents. Let π′ be the joint policy in M′. Counterfactual fairness is satisfied if the expected return for every agent remains unchanged, i.e., Ji(π) = Ji(π′) ∀i ∈N. When counterfactual fairness does not hold, we quantify the total disparity by summing the individual differences:

∆CF(π, π′) =

X i∈N

|Ji(π) −Ji(π′)| (3)

Definition 0.3 (Conditional Statistical Parity). Let LF ∈ (At \ {z}) be a non-sensitive, legitimate attribute, whose value for agent i is denoted by LFi. Let LLF be the set of possible values for LF. Conditional statistical parity is satisfied if demographic parity holds across all subgroups of agents that share the same value for the attribute LF.

Formally, for each value v ∈LLF, let Nv = {i ∈N | LFi = v}. Conditional statistical parity holds if, for all v ∈ LLF: ¯JN1∩Nv(π) = ¯JN0∩Nv(π).

The total disparity is the sum of the disparities across each legitimate factor value:

∆CSP(π, LF) =

X v∈LLF

¯JN1∩Nv(π) −¯JN0∩Nv(π)

(4)

Fairness Metrics for Fair PPO

PPO focuses on maximising agents’ rewards. This section extends PPO by incorporating fairness constraints directly into the optimisation process. Specifically, we add a penalty term to the PPO objective function, discouraging behaviours that diverge from any of the selected disparities above. However, designing the penalty accounting only for collected rewards can limit the effectiveness of learning policies, particularly in stochastic environments and the early training process stage. Thus, we compose the penalty of two parts: a retrospective component based on the total rewards collected in the past, and a prospective component based on the critic’s real-time value estimates. We modify Eq. 1 using the ∆DP metric as follows:

LFair-PPO t (θi) = ˆEt

LCLIP t (θi) −c1LVF t (θi) + c2H[πθi](st) −λ · Lfair t where Lfair t is one of the fairness penalties, and the hyperparameter λ controls the magnitude of the fairness penalty.

To formulate the group-based penalties, we first define the sample average return ¯G and sample average value ¯V for any agent subgroup G ⊆N:

¯GG(τ) = 1

|G|

X i∈G

Gi(τ) and ¯VG(st) = 1

|G|

X i∈G

Vθi(st)

(5)

Demographic Parity Penalty. This penalty is the samplebased equivalent of the ∆DP metric, penalising the difference in average outcomes between the groups N1 and N0.

Lfair-DP t =α ·

¯GN1(τ) −¯GN0(τ)

+ β ·

¯VN1(st) −¯VN0(st)

(6)

where the first term, the retrospective component (weighted by α), compares the average total return of the two groups over the last trajectory τ. The second term, the prospective component (weighted by β), compares the groups’ average value estimates for the current state st. The parameters α and β balance their contributions.

## Experimental Setup

We test Fair-PPO in two MAS: a version of the Allelopathic Harvest (AH) (Leibo et al. 2019) and HospitalSim (HS), an original hospital simulation.2

Allelopathic Harvest. In this setup, two groups of agents with distinct preferences, one for red berries and the other for blue berries, move in a grid and engage in cooperative dynamics within their respective groups, i.e., they plant and ripen berry bushes of their favourite colour and compete against the opposing group by blocking agents with opposing preferences. The objective for each group is to ensure the proliferation of their preferred berry, thereby maximising their rewards. The allelopathic element of AH is reflected in the bushes’ spontaneous growth, which follows a linear function based on the number of red and blue bushes already on the ground. Thus, actions such as changing the colour of berries on a bush play a fundamental role in enhancing the growth of favoured bushes and ensuring future rewards for the group. Within each group, half of the agents can move every turn, while others are limited to moving only every two turns. This difference in mobility is a sensitive attribute which can be interpreted as an impairment.

HospitalSim. HospitalSim (HS) simulates a hospital where three agents, an escort dispatcher, a triage router, and a doctor manager, coordinate to maximise patient care efficiency while ensuring treatment fairness between sensitive and non-sensitive patients.

2More details of the game in the supplementary material.

22728

<!-- Page 5 -->

Floor 0

Entrance Triage Resuscitation

Imaging

Prompt Care Pediatrics Floor 1

Floor 2

Floor 3

Triage Router

Doctor Manager

Escort Dispatcher

Acute Care

Psychiatry

Input: vector of the patient's symptoms and expected wait times for each hospital ward. Learning goal: send patients to the correct hospital ward based on symptoms and ward congestion.

Input: counts of high, medium, low-priority requests, maximum waiting time, and idle ratios for nurses/robots. Learning goal: optimally assign available nurses/robots to waiting patients.

Input: queue length, ratio of idle doctors, average priority of patients for each ward. Learning goal: move "swing" doctors between different wards to address patient bottlenecks.

**Figure 1.** HospitalSim workflow and input/task descriptions for each agent.

The triage router assigns patients to six wards based on a multi-level mapping of symptoms/wards, and the expected wait time for each ward. Thus, the agent should balance a trade-off between sending patients to their specialised ward, which may be busy, versus a faster backup ward that offers a reduced reward. The escort dispatcher assigns available nurses and robots to impaired patients who need help moving in the hospital. Such an assignment is based on patients’ priority, how long they have been waiting for an escort and the proportion of nurses and robots available. The doctor manager mitigates overcrowding by assigning swing doctors to different wards. This decision considers each ward’s queue length, doctor availability, and the average patient priority.

Patients arrive throughout the day with defined priorities, illnesses, and physical impairments (sensitive attribute); impaired patients have slow movement and need assistance, leading to potential delays. The waiting time is penalised based on the priority of the patient. The system’s learning agents integrate with rule-based agents, handling static functions like patient intake and diagnosis. A representation of HS is shown in Figure 1.

Train

In AH, we train two separate Fair-PPO models: one for agents with the sensitive attribute and another for those without. Training is conducted over 1000 episodes, each representing a new game, with 3000 time steps per episode. In HS, we train one model for each agent: the escort dispatcher, triage router, and doctor manager. Training spans 2000 episodes, with each episode simulating a new hospital day of twelve hours and a stream of 300 patients per day drawn from a generated pool. The simulation is eventdriven, with parallel agents’ actions that sequentially drive the game (thus, there are no time steps). Therefore, Fair- PPO employs a decentralised training approach, with a centralised fairness penalty calculation to add to the PPO objec- tive function.

In both games, after each episode, two penalty fairness components are calculated: the reward disparity is the difference in the total rewards accumulated by the non-sensitive group versus the sensitive group; the state-value disparity is the difference in the predicted state values between the two groups. Both components are normalised and weighted by α and β parameters. However, while in AH the fairness penalty is calculated based on the rewards experienced by the learning agents (red and blue agents), in HS the penalty is based on the total and expected rewards of the patients who are not the learning agents.

We train Fair-PPO using a penalty weighted by α and β, addressing demographic parity, counterfactual fairness, and conditional statistical parity separately. The parameters α and β range from 0 to 1, taking discrete values with a step of 0.25, for a total of 25 combinations. PPO is the specific instance of Fair-PPO with α = β = 0.

Test and evaluation We tested the policy on 500 episodes of 1500 time steps for AH and 500 episodes (days) of twelve hours with a stream of 300 patients per day drawn from a generated pool for HS (no time steps as explained in the previous section). Each metric is averaged over the time steps and episodes. In both AH and HS, demographic parity is the difference between the rewards collected by agents with and without a sensitive attribute (impairment). For conditional statistical parity, the legitimate factor is agents’ preference for red or blue berries in AH, and patients’ priority (high, medium and low) in HS.

Benchmarks We benchmark Fair-PPO against PPO (α = 0 and β = 0), FEN (Jiang and Lu 2019) and SOTO (Zimmer et al. 2021). The other hyperparameters of each algorithm are reported in the supplementary material.

In both AH and HS, FEN is implemented following a hierarchical policy structure where a controller selects from several sub-policies. One sub-policy optimises for efficiency while the others explore fair strategies. For example, in AH, an efficient action is eating a preferred berry, while a fair one is ripening a berry for another agent. In HS, the triage router’s efficiency policy learns to send a patient to the correct and least congested ward. In contrast, a fairness-oriented policy might prioritise patients with an impairment to better balance the utility across the entire system. The agent can change the policy every Tmacro macro-timesteps. The controller learns to maximise a fair-efficient reward that encourages actions oriented to the utility of all agents while penalising any deviation from fairness. In AH, FEN shares the parameters among all agents, employing a gossip protocol to average utility, while in HS, three independent FEN instances are employed for each learning agent.

In AH and HS, SOTO is implemented by providing each learning agent with a dual PPO-based policy that balances individual efficiency with collective fairness. In both cases, a self-oriented stream maximises local rewards. In contrast, a team-oriented stream optimises a social welfare function using an α-fairness mechanism that weights an agent’s advan-

22729

<!-- Page 6 -->

tage based on the utilities of others. The core difference of SOTO implementation in AH and HS is that in AH, the coordination of agents happens within each group (red and blue agents), and the fairness is calculated between non-sensitive and sensitive agents; in HS, the learning agents maximise their utility through the self-oriented policy, but the fairnessoriented policy minimises disparity between patients with and without impairment that are not learning agents.

## Results

In this section, we analyse the main findings from experiments in AH and HS.

Fairness and efficiency measures. Our focus is on demographic parity and conditional statistical parity calculated on agents’ rewards as the core fairness metrics. In AH, we also quantify fairness using the Gini index to assess reward distribution among agents, while overall efficiency is measured by the agents’ average accumulated rewards throughout the simulation. For HS, we evaluate hospital efficiency using several key metrics: the average number of patients treated daily, patients’ average waiting time for an escort, and the escorts’ average travel time. We specifically evaluate the triage router policy by analysing the percentage of patients directed to the primary ward, backup ward, or misclassified. The doctor manager is assessed by the average number of trips made by swing doctors.

Fair-PPO generates fairer policies than PPO Fair-PPO, through different combinations of α and β, produces several policies with lower demographic disparity than PPO in both AH and HS. Figure 2 shows three clusters of strategies (from light pink to dark purple) obtainable through adjusting the retrospective and prospective components of Fair-PPO in AH. Higher demographic parity generally corresponds to higher Price of Fairness, computed as the reward percentage agents renounce in favour of fairness compared to PPO. A similar result can be observed in HS, see the first (patients treated for efficiency) and the second column (demographic disparity for fairness) of Table 1. A lower disparity is also registered within the subgroups of agents (conditional statistical disparity), in both AH and HS: for example, Table 2 first column, shows the improvement within the priority groups of patients (high, medium and low priority).

Fair-PPO: comparison with FEN and SOTO In AH, Fair-PPO matches SOTO on fairness-reward tradeoffs, performing similarly in terms of equal reward distribution among agents. On the other hand, FEN records the lowest disparity but highly underperforms all algorithms in terms of inequality (Gini index) and average rewards. These results are reported in Figure 3.

In HS, Fair-PPO finds the fairest solutions as reported in Table 1, revealing a trade-off between lower efficiency, in terms of daily average treated patients, and lower demographic disparity. On the other hand, SOTO and FEN produce very prolific policies in terms of daily average treated patients. Looking at Figure 5, where the training phase is

Price of fairness (vs. PPO)

Demogr Disp Price of Fairness (%)

PPO Baseline

Fair-PPO: Fairness vs. Price of Fairness by Cluster

**Figure 2.** Allelopathic Harvest: Fair-PPO (α, β) demographic disparity boxplots clusters (light pink, purple and dark purple) and the Price of Fairness vs. PPO.

reported, SOTO learns an efficient and fair policy, without succeeding in reaching the level of parity of Fair-PPO. The same trend is confirmed by the test in Table 1 and 2 throughout demographic disparity and conditional statistical disparity columns.

Interpreting the strategies

By varying α and β, Fair-PPO explores a wide variety of strategies in AH. For example, Figure 4, left chart, shows the action frequencies of a representative of each cluster of Figure 2 (light pink, purple and dark purple). Low demographic disparity (light pink) corresponds to a strategy that heavily prioritises ripening the bush, which is the action most beneficial for other agents collecting rewards. The highest disparity (dark purple) focuses more on berry consumption, the selfish action. SOTO reaches similar fairness results to Fair-PPO with lower disparity through a more uniformly distributed strategy, while FEN agents learns a berryeating policy, which, later in the game, exhausts resources and dramatically decreases the rewards to collect.

In HS, Fair-PPO reduces the disparity between impaired and unimpaired patients by alleviating overcrowding. Since the hospital must admit all 300 patients daily, Fair-PPO optimises the triage router to heavily direct patients to backup wards. This strategy is evidenced by the data in the last three columns of Table 1 and further illustrated in the training graph in Figure 5. We also observe that a reduction in demographic disparity aligns with decreased patients’ waiting times for escorts and lower escort travel time. Both metrics underscore improved access to supportive resources for impaired patients. In conclusion, although SOTO manages to optimise the triage router better than other algorithms to send the patients to the specialised ward and also to reduce the swing doctor moves (see Table 1, fifth column), it does not achieve the same parity level of Fair-PPO and PPO.

22730

<!-- Page 7 -->

Fair-PPO PPO FEN SOTO

Fair-PPO PPO FEN

SOTO

Demographic Disparity Gini Index

Fair-PPO PPO FEN SOTO

Pareto Front

Pareto Front Fairness/Rewards

Average Rewards

Demographic Disparity

**Figure 3.** Allelopathic Harvest. Fair algorithms’ performance (average demographic disparity and Gini index) for each architecture (Fair-PPO, PPO, FEN and SOTO) and disparity/rewards Pareto frontier plotted for all algorithms.

## Algorithm

Patients Treated (Daily Average)

Dem Disparity (Rewards)

Patient Wait Escort

(Minutes)

Escort Travel Time

(Minutes)

Swing Doctor

Moves (Average)

Perfect Routing

(% of Patients)

Backup Routing

(% of Patients)

Incorrect Routing

(% of Patients)

Fair-PPO α = 0.25, β = 0.25 105.74 6.98 4.01 3.67 1923.93 6.04 44.93 49.03 Fair-PPO α = 0.25, β = 0.5 105.84 6.62 3.94 3.55 1925.52 6.00 37.13 56.86 Fair-PPO α = 0.5, β = 0.25 68.69 5.31 4.07 3.77 1924.72 3.83 43.78 52.39

PPO 105.92 6.83 3.94 3.56 1923.99 6.01 38.17 55.82

FEN 223.17 11.76 4.54 4.09 1924.25 19.65 18.42 61.93

SOTO α-fair = 1.0 240.03 9.10 4.51 4.06 1167.36 27.64 21.17 51.19

**Table 1.** HospitalSim. Average efficiency (patients treated) and fairness performance (demographic disparity) across Fair-PPO and benchmark, sorted according to the lowest demographic disparity. Further metrics are reported to complete the analysis.

Action Profile Fair-PPO Action Profile Benchmark Change Bush Colour

Eat Berry

Move Down

Move Left

## Algorithm

PPO Non Sensitive

Sensitive FEN SOTO

Fair-PPO (0.25,0.0) Fair-PPO (0.25,0.25) Fair-PPO (0.75,0.25)

Group

Move Right

Move Up

Ripe Bush

Stay

Obstacolate Agent

Change Bush Colour

Eat Berry

Move Down

Move Left Move Right

Move Up

Ripe Bush

Stay

Obstacolate Agent

**Figure 4.** Allelopathic Harvest. Action frequencies of Fair- PPO and benchmarks. For Fair-PPO, we show one algorithm for each cluster of Figure 2.

Demographic Disparity

## of Patients # of Patients

Dem Disparity

(Rewards) Minutes α =0.5, ß=0.25 α =0.25, ß=0.5 α =0.25, ß=0.0 α =0.25, ß=0.25 α =0.0, ß=0.0 FEN SOTO

Waiting Time For Escort Patients Sent to Backup Ward (%)

Treated Patients

Simulation Days Simulation Days

**Figure 5.** HospitalSim. Fairness (demographic disparity) and efficiency (daily treated patients and patients’ waiting time for escort) metrics convergence over the training for Fair- PPO and benchmarks.

Cond Stat Disp Patients Treated

## Algorithm

High Med Low (Daily Average)

Fair-PPO α=1.0 β=0.5 5.43 5.45 7.63 63.75 Fair-PPO α=0.25 β=1.0 5.43 5.43 7.54 64.05 Fair-PPO α=1.0 β=0.0 5.19 5.39 7.44 64.15

PPO 5.32 5.30 8.10 63.85

FEN 11.77 11.80 11.63 223.76

SOTO α-fair=2.0 9.17 9.14 9.11 239.95

**Table 2.** HospitalSim. Average conditional statistical disparity (high, medium, low patients’ priority) and efficiency (patients treated) performance across Fair-PPO and benchmark, sorted for best demographic disparity.

## Conclusion

This paper extends PPO by incorporating a penalty based on fairness metric violations in the objective function. We design two penalty components: a retrospective component that addresses fairness violations based on past rewards and a prospective component that anticipates future fairness violations by leveraging the value function to estimate upcoming rewards. We refer to this algorithm as Fair-PPO. We found that Fair-PPO can discover various strategies to reduce unfairness across metrics for different levels of efficiency in both cooperative and competitive games (AH) and coordination-based simulations (HS). This work represents a step towards a fairness-aware PPO based on metrics in MAS involving agents with and without sensitive attributes. The implementation of the HS aims to stimulate fair reinforcement learning research towards real-world applications.

22731

<!-- Page 8 -->

Ethical Statement This work shows how a penalty-based approach can make a multi-agent policy converge towards fairer behaviours. The penalty is based on metrics involving agents with and without sensitive attributes. Thus, this work requires careful ethical considerations. First, the fairness metrics used and the sensitive attribute are an inevitable simplification of fairness in reality. In particular, we recognise that the sensitive attribute cannot capture the complexity of real-world scenarios. Second, our results show a trade-off between fairness and efficiency of a system. The deployment of a model requires transparency and awareness in the presence of this trade-off, in particular when the applications are intended to imitate a hospital, as in the HS. In conclusion, we stress that the findings of the paper should be only a stimulus for discussion on computational simulations and fairness, rather than a direct basis for policy.

## Acknowledgments

This work was supported by UK Research and Innovation [grant number EP/S023356/1], in the UKRI Centre for Doctoral Training in Safe and Trusted Artificial Intelligence (www.safeandtrustedai.org).

## References

Amanatidis, G.; Aziz, H.; Birmpas, G.; and et al. 2023. Fair division of indivisible goods: Recent progress and open questions. Artificial Intelligence, 322: 103965. Baker, R.; and Hawn, A. 2021. Algorithmic Bias in Education. International Journal of Artificial Intelligence in Education, 32. Barman, S.; Khan, A.; Maiti, A.; and Sawarni, A. 2023. Fairness and welfare quantification for regret in multi-armed bandits. In AAAI’23/IAAI’23/EAAI’23, AAAI’23/IAAI’23/EAAI’23. ISBN 978-1-57735-880-0. Berk, R. 2019. Accuracy and Fairness for Juvenile Justice Risk Assessments. Journal of Empirical Legal Studies, 16(1): 175–194. Brˆanzei, S.; Gkatzelis, V.; and Mehta, R. 2017. Nash Social Welfare Approximation for Strategic Agents. arXiv:1607.01569. Budish, E. 2011. The Combinatorial Assignment Problem: Approximate Competitive Equilibrium from Equal Incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Kurokawa, D.; and et al., M. 2019. The Unreasonable Fairness of Maximum Nash Welfare. ACM Trans. Econ. Comput., 7(3). Castelnovo, A.; Crupi, R.; Greco, G.; and et al. 2022. A clarification of the nuances in the fairness metrics landscape. Scientific Reports, 12(1). Chen, J.; Wang, Y.; and Lan, T. 2021. Bringing Fairness to Actor-Critic Reinforcement Learning for Network Utility Optimization. In IEEE INFOCOM 2021, 1–10. Chi, J.; Shen, J.; Dai, X.; and et al. 2022. Towards Return Parity in Markov Decision Processes. volume 151, 1161– 1178. PMLR.

Chouldechova, A. 2016. Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. arXiv:1610.07524. Debove, S.; Baumard, N.; and Andr´e, J.-B. 2016. Models of the evolution of fairness in the ultimatum game: a review and classification. Evolution and Human Behavior, 37(3): 245–254. Farris, F. A. 2010. The Gini Index and Measures of Inequality. The American Mathematical Monthly, 117(10): pp. 851– 864. Giovanola, B.; and Tiribelli, S. 2022. Beyond bias and discrimination: redefining the AI ethics principle of fairness in healthcare machine-learning algorithms. AI Soc., 38(2): 549–563. Griesinger, D. W.; and Livingston Jr., J. W. 1973. Toward a model of interpersonal motivation in experimental games. Behavioral Science, 18(3): 173–188. G¨uth, W.; and Kocher, M. G. 2014. More than thirty years of ultimatum bargaining experiments: Motives, variations, and a survey of the recent literature. Journal of Economic Behavior & Organization, 108: 396–409. Hardt, M.; Price, E.; and Srebro, N. 2016. Equality of opportunity in supervised learning. NIPS’16, 3323–3331. Red Hook, NY, USA. ISBN 9781510838819. Høgsgaard, M. M.; Karras, P.; Ma, W.; and et al. 2023. Optimally Interpolating between Ex-Ante Fairness and Welfare. arXiv:2302.03071. Jabbari, S.; Joseph, M.; Kearns, M.; Morgenstern, J.; and Roth, A. 2017. Fairness in Reinforcement Learning. volume 70, 1617–1626. PMLR. Jiang, J.; and Lu, Z. 2019. Learning fairness in multi-agent systems. Red Hook, NY, USA: Curran Associates Inc. Jones, M.; Nguyen, H.; and Nguyen, T. 2023. An Efficient Algorithm for Fair Multi-Agent Multi-Armed Bandit with Low Regret. AAAI’23, 37(7): 8159–8167. Joseph, M.; Kearns, M.; Morgenstern, J. H.; and Roth, A. 2016. Fairness in Learning: Classic and Contextual Bandits. In NIPS’16, volume 29. Ju, P.; Ghosh, A.; and Shroff, N. 2024. Achieving Fairness in Multi-Agent MDP Using Reinforcement Learning. In ICLR. Kamishima, T.; Akaho, S.; Asoh, H.; and Sakuma, J. 2012. Fairness-Aware Classifier with Prejudice Remover Regularizer. In ECML PKDD, 35–50. ISBN 978-3-642-33486-3. Kaplow, L.; and Shavell, S. 2003. Fairness versus Welfare: Notes on the Pareto Principle, Preferences, and Distributive Justice. The Journal of Legal Studies, 32(1): 331–362. Kozodoi, N.; Jacob, J.; and Lessmann, S. 2022. Fairness in credit scoring: Assessment, implementation and profit implications. European Journal of Operational Research, 297(3): 1083–1094. Kusner, M. J.; Loftus, J. R.; Russell, C.; and Silva, R. 2018. Counterfactual Fairness. arXiv:1703.06856. Leibo, J. Z.; Perolat, J.; Hughes, E.; and et al. 2019. Malthusian Reinforcement Learning. AAMAS ’19, 1099–1107. Richland, SC. ISBN 9781450363099.

22732

<!-- Page 9 -->

Li, F.; Liu, J.; and Ji, B. 2020. Combinatorial Sleeping Bandits With Fairness Constraints. IEEE Transactions on Network Science and Engineering, 7(3): 1799–1813. Liebrand, W. B. G. 1984. The effect of social motives, communication and group size on behaviour in an N-person multi-stage mixed-motive game. European Journal of Social Psychology, 14(3): 239–264. Lindner, C.; and Rothe, J. 2016. Cake-Cutting: Fair Division of Divisible Goods, 395–491. Springer Berlin Heidelberg. ISBN 978-3-662-47904-9. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. EC ’04, 125–131. ISBN 1581137710. Liu, Y.; Radanovic, G.; Dimitrakakis, C.; Mandal, D.; and Parkes, D. C. 2017. Calibrated Fairness in Bandits. arXiv:1707.01875. Mitchell, S.; Potash, E.; Barocas, S.; and et al. 2021. Algorithmic Fairness: Choices, Assumptions, and Definitions. Annual Review of Statistics and Its Application, 8(Volume 8, 2021): 141–163. Murhekar, A. 2024. Fair and Efficient Chore Allocation: Existence and Computation. In Larson, K., ed., IJCAI-24, 8500–8501. Doctoral Consortium. Patil, V.; Ghalme, G.; Nair, V.; and Narahari, Y. 2021. Achieving Fairness in the Stochastic Multi-Armed Bandit Problem. Journal of Machine Learning Research, 22(174): 1–31. Reuel, A.; and Ma, D. 2024. Fairness in Reinforcement Learning: A Survey. arXiv:2405.06909. Schulman, J.; Levine, S.; Moritz, P.; Jordan, M. I.; and Abbeel, P. 2017a. Trust Region Policy Optimization. arXiv:1502.05477. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017b. Proximal Policy Optimization Algorithms. arXiv:1707.06347. Siddique, U.; Weng, P.; and Zimmer, M. 2020. Learning fair policies in multiobjective (deep) reinforcement learning with average and discounted rewards. ICML’20. Sutton, R. S.; and Barto, A. G. 2018. Reinforcement Learning: An Introduction. Cambridge, MA, USA. ISBN 0262039249. Vyas, D. A.; Eisenstein, L. G.; and Jones, D. S. 2020. Hidden in Plain Sight — Reconsidering the Use of Race Correction in Clinical Algorithms. New England Journal of Medicine, 383(9): 874–882. Wen, M.; Bastani, O.; and Topcu, U. 2021. Algorithms for Fairness in Sequential Decision Making. arXiv:1901.08568. Yu, G.; Siddique, U.; and Weng, P. 2023. Fair Deep Reinforcement Learning with Preferential Treatment. In ECAI, 2922–2929. Zhang, C.; and Shah, J. A. 2014. Fairness in multi-agent sequential decision-making. NIPS’14, 2636–2644. Zhang, L.; Shen, L.; Yang, L.; and et al. 2022. Penalized Proximal Policy Optimization for Safe Reinforcement Learning. arXiv:2205.11814.

Zimmer, M.; Glanois, C.; Siddique, U.; and Weng, P. 2021. Learning Fair Policies in Decentralized Cooperative Multi- Agent Reinforcement Learning. arXiv:2012.09421.

22733
