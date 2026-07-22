---
title: "Optimally Auditing Adversarial Agents"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38722
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38722/42684
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Optimally Auditing Adversarial Agents

<!-- Page 1 -->

Optimally Auditing Adversarial Agents

Sanmay Das1, Fang-Yi Yu2, Yuang Zhang2

1Virginia Polytechnic Institute and State University 2George Mason University sanmay@vt.edu, fangyiyu@gmu.edu, yzhang78@gmu.edu

## Abstract

Fraud can pose a challenge in many resource allocation domains, including social service delivery and credit provision. For example, agents may misreport private information in order to gain benefits or access to credit. To mitigate this, a principal can design strategic audits to verify claims and penalize misreporting. In this paper, we introduce a general model of audit policy design as a principal-agent game with multiple agents, where the principal commits to an audit policy, and agents collectively choose an equilibrium that minimizes the principal’s utility. We examine both adaptive and non-adaptive settings, depending on whether the principal’s policy can be responsive to the distribution of agent reports. Our work provides efficient algorithms for computing optimal audit policies in both settings and extends these results to a setting with limited audit budgets.

Code — https://github.com/dasddassad/Optimally-

Auditing-Adversarial-Agents

## Introduction

AI is increasingly used in making high-stakes societal decisions. One example that has recently gained considerable attention is the use of AI to decide whether to approve or deny the receipt of social benefits, with worries about how the scale of AI might systematically cut off thousands of people from benefits they are eligible for because of suspicion of fraud (Eubanks 2018). The reason to use AI in these domains, is because human time and resources are limited. However, an alternative method is the use of AI to flag a limited number of applicants for audits that can then be conducted by humans. How should one design such audit policies?

The problem of optimal audit design is relevant not just in the case of benefit receipt, but also in many other scenarios where agents must report their types to a principal in order for the principal to decide whether or not an agent is qualified to receive a benefit or service from the principal. In addition to qualification to receive social services or government benefits, other examples include credit or loan applications and tax relief. In all of these, the principal has the ability to, at some cost, audit agents to determine whether or not

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

they are revealing their true types. The principal may also be able to impose a penalty on those caught misreporting (e.g., prosecution of tax fraud, ineligibility for future government services). The goals of the principal can vary. In some cases, they may want to minimize misreporting. For example, a social services agency can be thought of as a benevolent principal trying to maximize the social welfare of recipients, and it needs truthful elicitation in order to achieve this goal. In others, the principal may have their own utility function – for example, a bank making lending decisions.

There have been a number of papers that look at specific versions of the general auditing problem described above. In this paper, we systematically analyze the problem along three different dimensions, and present a number of new results. The first dimension is the goal, distinguishing between maximizing social welfare over the agents and maximizing the principal’s utility. The second is whether or not the principal’s strategy can be responsive to the actual distribution of agent reports (we call these the adaptive versus non-adaptive settings). Finally, the third dimension is whether audits are limited by a budget or whether the principal can undertake marginal-cost auditing by paying a specific cost for each additional audit.

To give a concrete example, consider the Social Security Administration’s Supplemental Security Income program, which has a strict upper limit on assets for eligibility. The U.S. Supplemental Security Income program provides monthly cash only to applicants who (among other requirements) claim less than $ 2000 in so-called “deemed” resources (essentially countable assets). As verifying every claim is costly, the agency can only audit a fraction of applicants. Deciding which brackets to inspect, whether to adapt those fractions after seeing the week’s claims, and how to weigh extra recoveries against audit costs mirrors the three axes we analyze: objective (social welfare vs. agency pay-off), adaptivity (fixed vs. responsive rules), and resources (budget vs. cost). Our model captures this core strategic tension: applicants choose whether to misreport their private asset levels, anticipating the mixed audit policy chosen by the principal.

Our contributions This paper studies audit mechanism problems when agents adversarially choose the worst equilibrium. A principal wants truthful reports from n strategic

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16787

<!-- Page 2 -->

agents with private types in [m]. She may commit in advance to a probability of auditing different types (audit vector) or to an adaptive policy that decides the audit vector after seeing the agents’ reports. Each audit costs λ (in the costly setting) or counts against a budget of B (in the budgeted setting); detected misreports incur a penalty. After the principal commits, agents adversarially select the worst-case equilibrium. 1. We fully characterize the equilibrium structure in the non-adaptive costly setting where the principal commits to an audit vector and each audit costs λ. This structure yields an ϵ-approximation algorithm in O(m2) time for the principal’s utility (Theorem 1). We further prove that exact optimality is impossible in Proposition 1. 2. When the prior is unknown and varies in each round, we develop an online learning algorithm in § 3.2 that has regret O(n p

Tm2 log m) in T rounds (Theorem 2). Interestingly, although exact optimality in the one-shot setting is impossible, careful choice of arms allows our online learning algorithm to satisfy the no regret property. 3. Beyond the principal’s utility, §3.3 adapts both the efficient algorithm and the online learner to maximize social welfare, and §3.4 shows that increasing the penalty function or decreasing audit cost can only benefit the principal’s utility and social welfare (Proposition 2). 4. For adaptive audits, although the principal has a larger action space, we show that they offer no advantage over nonadaptive audits under the insensitivity assumption Eq. (12) and the Wardrop equilibrium Eq. (6). The same algorithm applies in the adaptive costly-audit setting (Theorem 4). A similar algorithm for the budgeted case appears in the full version.

## 1.1 Related Work

At a high level, our setting is a principal–(multi-)agent Stackelberg game. In this section, we survey relevant techniques and highlight connections to three special cases— audit games, security games, and toll pricing in congestion games.

Our Stackelberg game features one leader and multiple heterogeneous followers. Computing the leader’s optimal commitment is known to be hard even with two followers (Conitzer and Sandholm 2006). Our robustness notion relates to standard pessimistic equilibria. (Coniglio, Gatti, and Marchesi 2017), but as our model has a larger action space (real-valued probability of auditing each report) with a non-convex structure, the standard bi-level optimization technique is not feasible. Recent work also considers solving multi-follower games under no externality assumptions (Personnat et al. 2025).

Classic costly-state-verification work (Townsend 1979) and subsequent allocation papers (Mookherjee and Png 1989; Ben-Porath, Dekel, and Lipman 2014) study auditing or verification in resource-allocation settings, typically targeting truthful outcomes. Alm, Bahl, and Murray (1993); Ben abdelaziz, Neifar, and de Bourmont (2015); Coates, Florence, and Kral (2002) analyze equilibrium of audit game, whereas our work address the mechanism design problem. Lundy et al. (2019) study penalty design with an exogenous audit process, whereas in our setting the principal designs the audit strategy. In multi-agent settings, Estornell, Das, and Vorobeychik (2021); Estornell, Chen, and Das (2023) use audits to discourage misreporting and promote beneficial recourse. A key difference of our work from the above is equilibrium selection: rather than targeting truth-telling equilibria, we guarantee the principal’s performance at the worst (pessimistic) equilibrium, which may be non-truthful. Recently, Jalota, Tsao, and Pavone (2024) connect information design to audit mechanisms when the agents can commit to a misreporting strategy; in our work, the principal is the one who can commit.

Less directly related are security games, where a defender allocates inspection or patrol resources to deter attackers and inspection costs do not scale with the number of attackers. (Pita et al. 2008; Tambe 2012) Closer to us are audit games that allow the leader to tune punishment for a single agent (Blocki et al. 2013, 2015).

Our audit probabilities play a role analogous to tolls in congestion games: they modify followers’ payoffs to steer equilibrium flows. However in our model an agent’s cost depends not only on its reported type but also the true type. Foundational work showed that marginal-cost tolls can implement the system optimum in nonatomic traffic (Roughgarden and Tardos 2002; Cole, Dodis, and Roughgarden 2003).

Audit Mechanism Problem We study an audit mechanism design problem where a principal interacts with a continuum of (non-atomic) agents with total mass n. Each agent has a private type drawn from a known prior and may choose to misreport this type. The principal aims to incentivize truthful reporting by combining costly audits and penalties. We extend our analysis to a setting with a hard audit-budget constraint in the full version.

Basic Setup There are m ≥2 ordered types, denoted by [m] = {0, 1,..., m −1}. Each agent has a private type i ∈ [m] which is sampled independently from a prior q ∈∆m with full support on [m], and reports k ∈[m] which may differ from i. We use i, j for true types and k, l for reported types.

When a type i agent reports k, the principal assigns a payment pay(k), and receives val(i, k). The principal detects misreporting through audits by choosing an audit vector p ∈[0, 1]m where pk is the probability of auditing an agent reporting type k. Once audited, the principal gets pen(i, k) from the agent. We consider a type-independent penalty of the form pen(k) so that for all i, k pen(i, k) = 1[i̸ = k] · pen(k).1 One example is an affine penalty where pen(k) = a pay(k) + b with a, b ≥0.2 This includes the

1A type-independent penalty can admit a weaker notion of auditing—one that can detect inconsistencies between the reported and true types but cannot identify the true type itself.

2Here are two real-world examples of affine penalties. China’s Export Control authority levies fines between five and ten times the illicit turnover from an unlicensed export, i.e., pen(k) = 10 pay(k) or pen(k) = 5 pay(k). Virginia requires an evading driver to pay the unpaid toll and an administrative fee of up to $100,

16788

<!-- Page 3 -->

formulation in (Estornell, Das, and Vorobeychik 2021) as a special case when a = 1.

Without loss of generality, we order the indices so that 0 < pay(k) < pay(l) for all k < l and pay(−1):= 0. Additionally, we assume misreporting higher can only decrease the value to the principal, val(i, k) ≥val(i, l) for all i ≤k ≤l, (1)

and an agent that knows it will be audited would have no incentive to misreport:

pen(k) ≥pay(k) for all k. (2)

Agents’ Utilities and Strategies Given an audit vector p, a type i agent reporting k has expected utility

Ui,k(p):= pay(k) −pk pen(i, k) (3)

Agents use a randomized report strategy represented by a matrix Q where Qi,k is the probability of a type i agent reporting type k. The induced report distribution3 is ˆq ∈ ∆m where ˆqk = P i qiQi,k for all k. Definition 1. Given p, a report strategy Q is a Bayes-Nash equilibrium if for all i and k, l ∈[m] with Qi,k > 0, Ui,k(p) ≥Ui,l(p). Let Eqi(p) be the set of all equilibria.

Principal’s Utility Given p and Q, let C(p, Q):= n P i,k qiQi,kpk be the expected number of audit, and the principal’s utility without audit costs V (p, Q) = n P i,k∈[m] qiQi,k (val(i, k) −pay(k) + pk pen(i, k)) where the final term is the gain from auditing.

We consider the costly setting where the principal can audit any number of agents, but incurs a cost λ ≥0 per audit. The principal’s utility is

Vλ(p, Q) = V (p, Q) −λC(p, Q) (4)

We assume that the cost of audits is less than the penalty λ ≤pen(k) for all k. (5)

We defer the budgeted setting to the full version.

Principal Strategies: Non-adaptive and Adaptive The principal’s audit vector may be fixed or adaptively chosen based on agents’ reports, ˆq.

In the non-adaptive setting, the principal commits to an audit vector p. After observing p, the agents collectively choose an equilibrium Q ∈Eqi(p) that is worst for the principal. In the adaptive setting, the principal commits to an audit strategy π, which maps a reported distribution ˆq to an audit vector p = π(ˆq). After observing π, all agents collectively choose a worst equilibrium Q under π so that

Ui,k(π(ˆq)) ≥Ui,l(π(ˆq)), ∀i, k, l ∈[m] with Qi,k > 0 (6)

The above is a Wardrop equilibrium; a single agent’s deviation does not change the report distribution ˆq. We denote Eqi(π) as the set of equilibria among agents under strategy π, and Vλ(π, Q) = Vλ(π(ˆq), Q) where ˆq is the report distribution of Q.

i.e., pen = pay +100.

3As agents are non-atomic, the observed report distribution equals the expectation. In particular, if all are truthful, the report distribution equals q.

Optimal Non-Adaptive Audits with Costs We study non-adaptive costly audit games with (n, m, q, val, pay, pen) and λ. Most proofs are deferred to the full version.

## 3.1 Optimizing the

Principal’s Utility The principal wants to maximize her utility under the worstcase Bayes-Nash equilibrium, defined below

Vλ(p):= min Q∈Eqi(p) Vλ(p, Q). (7)

An audit vector p ϵ-approximates p′ if Vλ(p) ≥Vλ(p′) −ϵ, and p is ϵ-optimal if it ϵ-approximates any p′, i.e. Vλ(p) ≥ supp′ Vλ(p′) −ϵ.

Theorem 1 shows that there exists an algorithm that computes an ϵ-optimal audit vector in time O(m2). This runtime is tight, as reading all entries of val already requires Ω(m2) times. Moreover, Proposition 1 shows that computing an exactly optimal audit vector is impossible. Theorem 1. For any small enough ϵ > 0, (n, m, q, val, pay, pen) and λ, Algorithm 1 computes a 2nϵ-optimal audit vector for Eq. (7) in O(m4) time.

Moreover, the time complexity can be improved to O(m2). The idea of Algorithm 1 is to search over a finite set of audit vectors, called critical audit vectors (Definition 2). We also show that any audit vector can be approximated by one from this set.

The remainder of this section is organized as follows. We begin by defining equalized and critical audit vectors and presenting the algorithm. Next, we characterize agents’ best responses and equilibrium behavior in Lemma 1, a result that underpins both Theorem 1 and later analyses. We then show that exact optimization in Eq. (7) may be impossible, justifying our approximation approach. Finally, we prove Theorem 1.

Let ρk(u) be the probability that a type k report is audited when u is the utility of misreporting.

ρk(u) = pay(k) −u pen(k) (8)

This is a valid probability when 0 ≤u ≤pay(k) by Eq. (2). Note that ρk(u) is decreasing in u, and pk = ρk(Ui,k(p)), for all p and i̸ = k. Hence, ρk is a bijection between misreport utility and audit probability of type k. Definition 2 (Equalized and critical audit vectors). Given 0 < u ≤maxk pay(k) with ι = min{i: pay(i) ≥u}, A ⊆{i ∈[m]: i ≥ι}, and 0 < ϵ < u, we define the equalized audit vector p = equa(u, A, ϵ) such that for all k ∈[m]

pk =

 



0 k < ι, ρk(u) k ∈A, ρk(u −ε) otherwise.

If ˆA = {κ}, we write equa(u, A, ϵ) as equa(u, κ, ϵ). Given 0 < ϵ < γ:= 1 2 mink(pay(k) −pay(k − 1)) and ι ≤ κ we define the critical audit vectors as equa+(ι, κ, ϵ) = equa(pay(ι −1) + ϵ, κ, ϵ) and equa−(ι, κ, ϵ) = equa(pay(ι) −ϵ, κ, ϵ).

16789

<!-- Page 4 -->

## Algorithm

1: SuccinctSearch

Require: ϵ > 0, (n, m, q, val, pay, pen), and λ ≥0 Ensure: Audit vector p∗

1: Initialize Vmax ←−∞and p∗←1 2: for i ∈[m] do 3: for k = i to m −1 do 4: p+ ←equa+(i, k, ϵ) ▷critical audit vector 5: p−←equa−(i, k, ϵ) 6: if Vmax < COMPUTEVAL(p+) then 7: p∗←p+

8: Vmax ←COMPUTEVAL(p+)

9: if Vmax < COMPUTEVAL(p−) then 10: p∗←p−

11: Vmax ←COMPUTEVAL(p−)

12: return p∗

13: function COMPUTEVAL(p) 14: ˆu ←maxk {pay(k) −pk pen(k)} 15: ˆA ←arg maxk {pay(k) −pk pen(k)} 16: v ←0 17: for i ∈[m] do 18: vi ←(val(i, i) −pay(i) −piλ) 19: ˆvi ←min k∈ˆ A val(i, k) −pay(k) + pk(pen(k) −λ)

20: if pay(i) > ˆu then ▷truthful 21: v ←v + qivi 22: else if pay(i) < ˆu then ▷misreporting 23: v ←v + qiˆvi 24: else ▷indifferent 25: v ←v + qi min {vi, ˆvi}

26: return v

Intuitively, an equalized audit vector sets the misreport value of all types in A to u, and minimizes audit probabilities for others so that agents either misreport as A or report truthfully. Lemma 2 formalizes this property. Note that because the ρk are decreasing, equa+(ι, κ, ϵ) ≥equa−(ι, κ, ϵ) coordinate-wise.

Characterizing Best Response and Equilibrium Before proving the theorem, we show that the best response of each agent follows a threshold structure. There exists a minimal truthful type and a misreporting range such that all agents with lower types strictly prefer to misreport as a type within the misreport range, while higher types strictly prefer to report truthfully.

Given p, by Eq. (3), we can write the best-response set of type-i agents as Ai(p) = arg max k∈[m](pay(k) − pk pen(i, k)). To simplify the notation, we define the misreport utility of reporting k as

ˆUk(p):= pay(k) −pk pen(k)

, which is independent of the misreporting agent’s type, and the utility of being truthful as Uk = pay(k). Finally, let ˆu(p) = maxk ˆUk(p) be the highest misreport utility, itruth(p) = min{i ∈[m]: Ui ≥ˆu(p)} be the minimal truthful type (the lowest type that is willing to be truthful), and misreporting range ˆA(p) = arg maxk{ ˆUk(p)} ⊆[m]

be the set of types that have the highest misreport utility. We will omit p when it is clear in context.

Lemma 1 (Threshold structure). Given p with ˆu(p), ˆA(p), and itruth(p) defined above, ˆA(p) ⊆{i ∈[m]: i ≥ itruth(p)} and

Ai(p) =

    

   

{i} if i > itruth, ˆA if i < itruth {itruth} if i = itruth and Uitruth > ˆu ˆA ∪{itruth} if i = itruth and Uitruth = ˆu

.

An audit vector is strict if ˆu /∈{Ui: i ∈[m]} so that every agent is either truthful or misreports as ˆA. Additionally, a report strategy Q is single-minded with ι ≤κ if all types i ≥ι are truthful and all types i < ι report as κ.4

By Lemma 1, Eqi(p) is non-empty and closed, so the minimum in Eq. (7) is well-defined. However, Proposition 1 shows that the maximum of Eq. (7) does not always exist.

**Figure 1.** A non-adaptive audit game with unattainable optimum: As in Proposition 1, we consider binary types (m = 2) with q0 = q1 = 1/2, pay = (1, 2), pen = (3, 4),

val =

3 0 0

, and λ = 1. We vary the audit probability of the high type, using p = (0, p1) since auditing the low type is useless. The principal’s utility if all agents misreport as the high type is Vlie(p1) = p1 (red), and if all are truthful is Vtru(p1) = 4−p1

2 (blue). When p1 < 1

4, misreporting as the highest type is the unique equilibrium, for p1 > 1 4, truth-telling is the unique equilibrium, and at the threshold p1 = 1

4, any mixture is an equilibrium. Therefore, the principal’s worst-case equilibrium utility at p1 = 1 4 is 1 4, but supp Vλ(p) = limp1→1/4+ Vλ(0, p1) = 15

8 which is not attained by any p.

Proposition 1. There exists a nonadaptive costly audit game so that supp∈[0,1]m Vλ(p) < +∞but for all p, Vλ(p) < supp′∈[0,1]m Vλ(p′).

Lemma 2 establishes that the equalized audit vector is well-defined and corresponds to the u, A, and ι in Lemma 1.

4If ι = 0 everyone is truthful.

16790

![Figure extracted from page 4](2026-AAAI-optimally-auditing-adversarial-agents/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

Lemma 2. Given p = equa(u, A, ϵ) with ι = min{i: pay(i) ≥u}, if u /∈{Ui: i ∈[m]}, p is a strict audit vector, ˆu(p) = u, ˆA(p) = A, and itruth(p) = ι.

Ai(p) =

{i} if i ≥itruth, A if i < itruth

.

Approximation by Equalized and Critical Audit Vectors We now show that any audit vector can be approximated by some strict equalized vector (Lemma 3), and some critical vector (Lemma 4).

Lemma 3. For any p ∈[0, 1]m, there is a strict equalized audit vector p′ = equa(u, κ, ϵ) with u > 0, κ ∈[m], and 0 < ϵ < u so that Eqi(p′) ⊆Eqi(p) and for all Q ∈ Eqi(p′)

Vλ(p, Q) ≤Vλ(p′, Q) + nϵ.

To prove Lemma 3, we use Lemma 2 to find a a strict equalized audit vector p′ so that Eqi(p′) = {Q} ⊆Eqi(p) consists of a single-minded equilibrium with ι and κ. Then we upper bound the difference of the principal’s utilities with these two audit vectors, Vλ(p, Q) −Vλ(p′, Q) to get n

X i,k∈[m]

qiQi,k (pen(i, k) −λ) (pk −p′ k). (9)

To minimize Eq. (9), consider two cases. If k̸ = κ, the smaller p′ k yields a larger utility (which is the intuition of Eq. (8)). For type κ, the equalized audit vector ensures p′ κ ≈pκ.

Lemma 4. For any ϵ′ and p = equa(u, κ, ϵ) with ι = itruth(p) and ϵ, ϵ′ < γ, there are p− = equa(Uι −ϵ′, κ, ϵ) and p+ = equa(Uι−1 + ϵ′, κ, ϵ) so that Eqi(p+) = Eqi(p−) = Eqi(p) and Vλ(p, Q) ≤ max{Vλ(p+, Q), Vλ(p−, Q)} + nϵ′ for all Q ∈Eqi(p).

To prove Lemma 4, we note that fixing κ ∈[m] and ϵ > 0, an equalized audit vector p = equa(κ, u, ϵ) is parameterized by a single parameter u ∈R. Moreover, the audit probabilities are affine in u, so the principal’s utility is affine in u by Eq. (9). Therefore, we can optimize the principal’s utility using the extreme value of u ∈(Uι−1, Uι) by Lemma 2.

Proof of Theorem 1 Algorithm 1 iterates over critical audit vectors with all combinations of i ≤k and computes the principal’s worst-case utility. By Lemma 1, ComputeVal computes Vλ(p) by considering whether a type is truthful or misreporting as ˆA. Therefore, Algorithm 1 returns the optimal critical audit vector.

For the approximation guarantee, given any audit vector p ∈[0, 1]m, by Lemma 3, there exists a strict equalized audit vector p′ = equa(u, κ, ϵ) with ι = itruth(p′) so that Vλ(p) ≤ Vλ(p′)+nϵ. By Lemma 4, there exists a critical audit vector p′′ = equa+(ι, κ, ϵ) or equa−(ι, κ, ϵ) with ι ≤κ so that Vλ(p′) ≤Vλ(p′′) + nϵ. Therefore, there exists some critical audit vector

Vλ(p) ≤Vλ(p′′) + 2nϵ, and the algorithm is 2nϵ-optimal.

The algorithm searches through all 2( m

2

+m) = O(m2) critical vectors. By Lemma 1, ComputeValcomputes

Vλ(p) by computing the worst report in Ai(p) that minimizes the principal’s utility for all i. This takes O(m2) for each audit vector. Therefore, the time complexity is in O(m4). We can improve the running time of Algorithm 1 to O(m2) using dynamic programming for ComputeVal.

## 3.2 No-Regret Auditing Without a Prior One limitation of

## Algorithm

1 is assuming access to the prior q. We provide a no-regret online learning algorithm when the prior q is unknown and can vary in each round.

Let Vλ(p, Q; q) be the principal’s (single-round) utility from Eq. (4) under prior q, and Vλ(p; q):= minQ∈Eqi(p) Vλ(p, Q; q).

Consider the principal and agents interacting over T rounds. The principal knows (n, m, val, pay, pen) and λ while Nature secretly chooses⃗q:= (q0,..., qT −1). For round t = 0,..., T −1, 1. The principal with algorithm A samples an audit vector pt from a distribution P t based on the history (p0, v0,..., pt−1, vt−1). 2. After observing pt, agents collectively choose the worst equilibrium Qt ∈arg minQ∈Eqi(pt) Vλ(pt, Q; qt)

3. The principal gets vt = Vλ(pt, Qt; qt) = Vλ(pt; qt). The principal designs an online learning algorithm A that maximizes her accumulative expected utility. Formally, the algorithm is evaluated by its (multi-agent) Stackelberg regret (Dong et al. 2018; Chen, Liu, and Podimata 2020)5 against the optimal audit vector in hindsight which knows agents’ prior⃗q. We define

RegT (A,⃗q) = sup p

X t∈[T ]

Vλ(p; qt)−EA



X t∈[T ]

Vλ(pt; qt)



,

(10) and RegT (A) = sup⃗q RegT (A,⃗q) where the randomness is over the choice of audit vectors. Theorem 2. Given any (n, m, val, pay, pen) and λ, the online learning algorithm A in Algorithm 2 has RegT (A) = O(n p

Tm2 log m). The key observation is that the equalized and critical audit vectors in Definition 2 are independent of prior qt. Additionally, we can reuse Lemmas 3 and 4 to show that the critical vectors are approximately optimal as in Lemma 5. Lemma 5. Given any 0 < ϵ < γ, there exist p+ = equa+(ι, κ, ϵ) or p−= equa−(ι, κ, ϵ) with ι ≤κ so that for all⃗q = (q0,..., qT −1) and p,

Vλ(p;⃗q) ≤max{Vλ(p+;⃗q), Vλ(p−;⃗q)} + 2nϵT where Vλ(p;⃗q):= P t Vλ(p; qt). With Lemma 5, given ϵ > 0 we run a no regret algorithm for adversarial bandits (e.g., EXP3) on O(m2) critical audit vectors in order to achieve regret bounded by

5Classical online-Stackelberg work assumes a single agent (follower) who best-responds to the leader’s action. In our model the follower is a population of n agents who play the worst equilibrium under the n-player game induced by the audit vector.

16791

<!-- Page 6 -->

## Algorithm

2: EXP3 algorithm on critical audit vectors

Require: Game parameters (n, m, val, pay, pen) with L = n maxi,k (val(i, k) + pay(k) + pen(k)), cost λ ≥0, horizon T, and learning rate η = q log(2m2)

2m2T 1: Initialize ϵ0 ←2 3γ and s0 σ ←0 for all σ ∈Σ. 2: for t = 1 to T do 3: Compute Pt with Pt,σ ∝exp(ηst σ) for all σ 4: Sample σt ∼Pt and set pt = equa(σt, ϵt) 5: Observe reward vt = Vλ(pt; qt), 6: Update ϵt+1 ←1

2ϵt and for all σ st+1 σ ←st σ + 1 −L −vt

2L · I[σ = σt] Pt,σ

.

O( p

Tm2 log m+nϵT). However, to achieve no-regret, Algorithm 2 considers the set of critical vectors in Definition 2 with ϵt = 2−tϵ0. Specifically, we consider the set of all critical audit vectors σ ∈Σ:= {(i, k, +), (i, k, −): i, k ∈ [m]}, and at round t we use equa(σ, ϵt) = equa+(i, k, ϵt) if σ = (i, k, +) and equa−(i, k, ϵt) if σ = (i, k, −) as the set of arms.6

## 3.3 Optimizing Social Welfare

Now we show how to maximize social welfare, the sum of utility between the principal and all agents,

Wλ(p, Q):=Vλ(p, Q) +

X i,k∈[m]

qiQi,kUi,k(p)

=n

X i,k∈[m]

qiQi,k (val(i, k) −pkλ).

(11)

For instance, if val(i, k) = 1[i = k], the social welfare is the number of truthful agents minus the cost of audits.

As agents are strategic, we need to design an audit vector p so that Wλ(p):= minQ∈Eqi(p) Wλ(p, Q) is large, and say p is ϵ-optimal if Wλ(p) ≥Wλ(p′) −ϵ for all p′. Theorem 3. There is an algorithm that computes a 2nϵoptimal audit vector for Eq. (11) in time O(m2) for any ϵ > 0 and nonadaptive audit game with (n, m, q, val, pay, pen) and cost λ.

The algorithm is nearly identical to Algorithm 1. Since the agent’s best-response still follows from Lemma 1, we can reuse Lemmas 3 and 4 and search through all critical audit vectors as in Algorithm 1 and return the one that maximizes the worst-case social welfare. We omit the proof. Similarly, we can adopt Algorithm 2 to have a no-regret algorithm for social welfare maximization.

## 3.4 Monotonicity in Penalty and Audit Cost

Besides designing the audit vector, the principal may also adjust the penalty function or face a different audit cost λ.

6We treat each tuple (i, k, +) or (i, k, −) as a template arm. EXP3 maintains weights over these templates, while the audit vector played in round t depends on the template and ϵt

We show that increasing the penalty or decreasing the audit cost λ can only improve the principal’s utility and social welfare.

Let Vλ(p; pen) and Wλ(p; pen) be the principal’s worst case utility (Eq. (7)) and worst-case social welfare respectively under penalty function pen and cost λ.

Proposition 2. If λ ≥λ′ and pen(k) ≤pen′(k) for all k ∈[m], for any p there exists p′ so that Vλ(p; pen) ≤ Vλ′(p′; pen′) and Wλ(p; pen) ≤Wλ′(p′, pen′).

The idea of Proposition 2 is that if the penalty increases, we can decrease the audit probability p′ k = pen(k)

pen′(k)pk, which preserves the same equilibria and expected penalty gain, but lowers the audit cost.

## 4 Optimal Adaptive Audits With Costs

We now explore adaptive audit games, where the principal’s strategy depends on both the agents’ prior distribution q and report distribution ˆq. We discuss the costly setting and defer the budgeted setting to the full version.

In this section, we assume that the penalty is less sensitive than the payment: for all k ≤l in [m]

pay(l) pay(k) ≥pen(l)

pen(k). (12)

In particular, any positive affine function pen(k) = a pay(k) + b with a, b ≥0 for all k satisfies Eq. (12).

As multiple equilibria may exist, the principal optimizes for the worst-case utility by solving the following optimization problem:

sup π:∆m→[0,1]m min Q∈Eqi(π) Vλ(π, Q). (13)

We define Vλ(π) = minQ∈Eqi(π) Vλ(π, Q) as the principal’s worst case utility and set to −∞if Eqi(π) = ∅following the standard convention in pessimistic Stackelberg games. (Coniglio, Gatti, and Marchesi 2017) We say that π ϵ-approximates π′ if Vλ(π) ≥Vλ(π′)−ϵ, and π is ϵ-optimal if it ϵ-approximates any π′.

Theorem 4. There is an algorithm that computes an ϵoptimal audit vector for Eq. (13) with Eq. (4) in O(m2) time for all small enough ϵ > 0 and adaptive audit game with cost λ ≥0 and parameters (n, m, q, val, pay, pen) satisfying Eq. (12). Moreover, sup π min Q∈Eqi(π) Vλ(π, Q) = sup p∈[0,1]m,Q∈Eqi(p)

Vλ(p, Q).

Proof Sketch. To prove Theorem 4, we use three key observations. First, due to Lemma 1 equilibria depend only on the output vector p. Adaptive strategies cannot yield new equilibria beyond those already attainable by some fixed p. Consequently,

Vλ(π) ≤ sup p,Q∈Eqi(p)

Vλ(p, Q) (14)

and we will show that Eq. (14) holds with equality.

16792

<!-- Page 7 -->

Second, let a dictator audit strategy with p∗and ˆq∗∈∆m πdict(ˆq) =

 

 p∗ if ˆq = ˆq∗

1 if ˆq̸ = q and ˆq̸ = ˆq∗

0 if ˆq = q and ˆq̸ = ˆq∗

. (15)

Intuitively, if the observed reports differ from q∗, we either audit everyone (making any misreporting strictly unprofitable) or audit no one (agents strictly prefer to over-report as the highest type). Lemma 6 shows that a dictator audit strategy can eliminate any report strategy with ˆq̸ = ˆq∗, while ensuring the existence of an equilibrium with ˆq = ˆq∗by choosing p∗appropriately. Lemma 6 (Dictator strategies). For any dictator audit strategy πdict in Eq. (15) with p∗and ˆq∗, Eqi(πdict) = {Q ∈ Eqi(p∗): ˆq = ˆq∗}.

Finally, Lemma 7 shows that for any audit vector p, the best equilibrium can be single-minded. Therefore, it is sufficient to iterate all single-minded strategies Q and search the optimal audit vector p with Q ∈Eqi(p). Moreover, by a similar argument as in Lemma 4, we show that the optimal audit vector is critical. This reduces the search to O(m2) candidates, yielding the claimed O(m2) running time. Lemma 7. For any audit vector p, if Eq. (12) holds, there exists a single-minded equilibrium Q′ ∈Eqi(p) so that for all Q ∈Eqi(p) Vλ(p, Q) ≤Vλ(p, Q′). Remark 1. Note that the argument to prove Lemma 7 also applies to social welfare, so Theorem 4 also holds for optimizing social welfare. Additionally, by Lemma 7, if Eq. (12) holds, Algorithm 1 also finds an approximately optimal audit vector in the non-adaptive setting, and the worst-case utility coincides with the best-case utility sup p min Q∈Eqi(p) Vλ(p, Q) = sup p max Q∈Eqi(p) Vλ(p, Q).

Conversely, if Eq. (12) is not satisfied, the optimal equilibrium may not be single-minded, and this equivalence no longer applies.

## 5 Simulations

Thus far, we have analyzed the optimal audit policy theoretically. We now provide simple simulations to illustrate how the optimal policy and the resulting equilibria depend on the prior and the payment function in small three-type examples.

**Figure 2.** illustrates the effect of the prior q. In the lowerleft corner, most agents have the lowest type (type 0), which admits the truthful equilibrium (0, 1, 2). At the top corner, most agents have type 2, and it becomes preferable to allow everyone to report the highest type (2, 2, 2) rather than impose huge audit costs to enforce truth-telling. Similarly, in the lower-right corner, it is optimal to allow type 0 to misreport as type 1. Finally, we note that the principal-optimal policy in Fig. 2a is stricter than the welfare-optimal one in Fig. 2b, and yields a larger truth-telling region. This is because misreports impose greater costs on the principal than on overall welfare.

**Figure 3.** shows effect of the payment function is nonmonotone when all other parameters are fixed. In Fig. 3a,

(a) Principal’s utility (b) Social Welfare

**Figure 2.** Effect of prior q: There are three types m = 3 with n = 1, val = diag(0.5, 1.4, 3.0), pay = (0.3, 0.8, 1.3), pen = (1.0, 1.2, 1.4), and λ = 0.7. Each point corresponds to a prior vector q = (q0, q1, q2), and the color encodes the principal’s optimal utility by Theorem 1 with ϵ = 10−3 in Fig. 2a, and the optimal social welfare by Theorem 3 in Fig. 2b. We also indicate the region of the worst equilibrium.

(a) Principal’s utility (b) Social Welfare

**Figure 3.** Effect of pay: There are three types m = 3 and change the payment of type 1 with the following parameters

n = 1, q = (0.4, 0.3, 0.3), val =

0.99 0.90 0.50 0 1.50 1.40 0 0 4.00

!

, pay(0) = 1, pay(2) = 3, pen = pay +0.5, and λ = 1.

the worst equilibrium is always truth-telling, and increasing the payments monotonically decreases the principal’s utility. In contrast, in Fig. 3b, when the type-1 payment is small, the equilibrium is still truth-telling and welfare decreases. However, for large type-1 payment, type 0 agents begin to misreport as type 1, and increasing pay(1) reduces audit probability p2 and increases welfare.

## 6 Discussion and Future Work

We provide several optimal and efficient audit policies for utility- and welfare-maximizing under pessimistic equilibrium selection. At the same time, extending our model suggests fruitful directions for future work. First, extending our guarantees to finite agents, noisy or partial verification, and richer penalty structures remains open. Second, we take the classifier or allocation rule as exogenous; jointly designing the predictive model and the audit policy could yield better performance. Finally, it would be interesting to extend the incentive-minimization framework of Estornell, Chen, and Das (2023) to non-binary payment outcomes.

## Acknowledgments

SD is grateful for support from NSF Award 2533162.

16793

![Figure extracted from page 7](2026-AAAI-optimally-auditing-adversarial-agents/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-optimally-auditing-adversarial-agents/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-optimally-auditing-adversarial-agents/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-optimally-auditing-adversarial-agents/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## References

Alm, J.; Bahl, R.; and Murray, M. N. 1993. Audit selection and income tax underreporting in the tax compliance game. Journal of development Economics, 42(1): 1–33. Ben abdelaziz, F.; Neifar, S.; and de Bourmont, M. 2015. Auditing and game theory: A survey. In Multiple Criteria Decision Making in Finance, Insurance and Investment, 249–272. Springer. Ben-Porath, E.; Dekel, E.; and Lipman, B. L. 2014. Optimal allocation with costly verification. American Economic Review, 104(12): 3779–3813. Blocki, J.; Christin, N.; Datta, A.; Procaccia, A. D.; and Sinha, A. 2013. Audit Games. In Rossi, F., ed., IJCAI 2013, Proceedings of the 23rd International Joint Conference on Artificial Intelligence, Beijing, China, August 3-9, 2013, 41– 47. IJCAI/AAAI. Blocki, J.; Christin, N.; Datta, A.; Procaccia, A. D.; and Sinha, A. 2015. Audit Games with Multiple Defender Resources. In Bonet, B.; and Koenig, S., eds., Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, January 25-30, 2015, Austin, Texas, USA, 791–797. AAAI Press. Chen, Y.; Liu, Y.; and Podimata, C. 2020. Learning Strategy- Aware Linear Classifiers. In Larochelle, H.; Ranzato, M.; Hadsell, R.; Balcan, M.; and Lin, H., eds., Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. Coates, C. J.; Florence, R. E.; and Kral, K. L. 2002. Financial statement audits, a game of chicken? Journal of Business Ethics, 41(1): 1–11. Cole, R.; Dodis, Y.; and Roughgarden, T. 2003. Pricing network edges for heterogeneous selfish users. In Proceedings of the Thirty-Fifth Annual ACM Symposium on Theory of Computing, STOC ’03, 521–530. New York, NY, USA: Association for Computing Machinery. ISBN 1581136749. Coniglio, S.; Gatti, N.; and Marchesi, A. 2017. Pessimistic Leader-Follower Equilibria with Multiple Followers. In Sierra, C., ed., Proceedings of the Twenty-Sixth International Joint Conference on Artificial Intelligence, IJCAI 2017, Melbourne, Australia, August 19-25, 2017, 171–177. ijcai.org. Conitzer, V.; and Sandholm, T. 2006. Computing the optimal strategy to commit to. In Proceedings of the 7th ACM Conference on Electronic Commerce, EC ’06, 82–90. New York, NY, USA: Association for Computing Machinery. ISBN 1595932364. Dong, J.; Roth, A.; Schutzman, Z.; Waggoner, B.; and Wu, Z. S. 2018. Strategic Classification from Revealed Preferences. In Tardos, ´E.; Elkind, E.; and Vohra, R., eds., Proceedings of the 2018 ACM Conference on Economics and Computation, Ithaca, NY, USA, June 18-22, 2018, 55–70. ACM. Estornell, A.; Chen, Y.; and Das, S. 2023. Incentivizing Recourse through Auditing in Strategic Classification. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence (IJCAI), 400–408.

Estornell, A.; Das, S.; and Vorobeychik, Y. 2021. Incentivizing Truthfulness Through Audits in Strategic Classification. In Thirty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2021, Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021, The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI 2021, Virtual Event, February 2-9, 2021, 5347–5354. AAAI Press. Eubanks, V. 2018. Automating Inequality: How High-Tech Tools Profile, Police, and Punish the Poor. New York, NY: St. Martin’s Press. ISBN 1250074312. Jalota, D.; Tsao, M.; and Pavone, M. 2024. Catch Me If You Can: Combatting Fraud in Artificial Currency-Based Government Benefits Programs. arXiv:2402.16162. Lundy, T.; Wei, A.; Fu, H.; Kominers, S. D.; and Leyton- Brown, K. 2019. Allocation for Social Good: Auditing Mechanisms for Utility Maximization. In Proceedings of the 2019 ACM Conference on Economics and Computation, EC ’19, 785–803. New York, NY, USA: Association for Computing Machinery. ISBN 9781450367929. Mookherjee, D.; and Png, I. 1989. Optimal auditing, insurance, and redistribution. The Quarterly Journal of Economics, 104(2): 399–415. Personnat, G.; Lin, T.; Hossain, S.; and Parkes, D. C. 2025. Learning to Play Multi-Follower Bayesian Stackelberg Games. arXiv:2510.01387. Pita, J.; Jain, M.; Marecki, J.; Ord´o˜nez, F.; Portway, C.; Tambe, M.; Western, C.; Paruchuri, P.; and Kraus, S. 2008. Deployed ARMOR protection: the application of a game theoretic model for security at the Los Angeles International Airport. In Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems: Industrial Track, AAMAS ’08, 125–132. Richland, SC: International Foundation for Autonomous Agents and Multiagent Systems. Roughgarden, T.; and Tardos, E. 2002. How bad is selfish routing? J. ACM, 49(2): 236–259. Tambe, M. 2012. Security and Game Theory - Algorithms, Deployed Systems, Lessons Learned. Cambridge University Press. ISBN 978-1-10-709642-4. Townsend, R. M. 1979. Optimal contracts and competitive markets with costly state verification. Journal of Economic theory, 21(2): 265–293.

16794
