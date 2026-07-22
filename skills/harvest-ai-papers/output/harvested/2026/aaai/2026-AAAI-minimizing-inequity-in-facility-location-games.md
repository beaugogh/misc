---
title: "Minimizing Inequity in Facility Location Games"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38747
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38747/42709
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Minimizing Inequity in Facility Location Games

<!-- Page 1 -->

Minimizing Inequity in Facility Location Games

Yuhang Guo, Houyu Zhou*

University of New South Wales {yuhang.guo2, houyu.zhou}@unsw.edu.au

## Abstract

This paper studies the problem of minimizing group-level inequity in facility location games on the real line, where agents belong to different groups and may act strategically. We explore a fairness-oriented objective that minimizes the maximum group effect. For each group, the group effect is defined as its total or maximum distance to the nearest facility, weighted by group-specific factors. We show that this formulation generalizes several prominent optimization objectives, including the classical utilitarian (social cost) and egalitarian (maximum cost) objectives, as well as two group-fair objectives, maximum total and average group cost. In order to minimize the maximum group effect, we first propose two novel mechanisms for the single-facility case, the Balanced mechanism and the Major-Phantom mechanism. Both are strategyproof and achieve tight approximation guarantees under distinct formulations of the maximum group effect objective. Our mechanisms not only close the existing gap in approximation bounds for the group-fairness objectives, maximum total group cost and maximum average group cost, but also unify many classical truthful mechanisms within a broader fairness-aware framework. For the two-facility case, we revisit and extend the classical endpoint mechanism to our generalized setting and demonstrate that it provides tight bounds for two distinct maximum group effect objectives.

## Introduction

Facility Location Games (FLGs), which study how to locate facilities based on agents’ preferences, have been extensively explored over the past two decades. Most prior work in this area has prioritized efficiency, typically aiming to minimize the total cost incurred by agents in accessing services. Such efficiency-driven approaches achieve optimal social welfare, however, at the expense of fairness and equity. In particular, mechanisms designed purely for efficiency tend to favor majority groups, leaving disadvantaged or minority populations marginalized. Recognizing these limitations, recent research has increasingly focused on incorporating fairness into facility location games. These efforts span a spectrum from individual fairness, which aims

*Corresponding Author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

to equalize costs across agents (Cai, Filos-Ratsikas, and Tang 2016; Walsh 2025), to group fairness, which ensures equitable treatment across predefined groups (Marsh and Schilling 1994; Zhou, Li, and Chan 2022; Aziz et al. 2025). A seminal contribution by Marsh and Schilling (1994) introduced various equity metrics, including the “center” objective, which seeks to minimize the maximum group effect. As they note,

“This is the earliest and most frequently used measure that has an equity component.”

This underscores the significance of the center objective in equity-aware location analysis. However, many subsequent studies have adopted a narrow interpretation of this objective, often modeling it as the maximum individual distance across all agents, thereby overlooking group structures and alternative definitions of group-level costs. In contrast, Marsh and Schilling (1994) proposed a broader formulation, in which the effect of a group, Ei, could be defined in terms such as the total distance incurred by all agents in group i. This generalization more accurately reflects the collective burden borne by each group, offering a richer fairness perspective. Motivated by this observation, we revisit the general objective of minimizing maxi Ei and study its implications within the framework of facility location games.

In this paper, we focus on the objective of minimizing the maximum group effect, where the effect Ei of a group i is defined as either the total or maximum distance from its agents to their nearest facility, multiplied by a weight wi, capturing group-specific priorities, such as socioeconomic status or policy-driven importance (see Section 2 for formal definitions). Our objective of minimizing maxi Ei emphasizes group-level fairness by bounding the worst-case burden among all groups. Unlike traditional formulations that protect only the most distant individual, our model accounts for the collective experience of each group. This perspective aligns with Rawlsian principles (Rawls 1958), which advocate prioritizing the welfare of the most disadvantaged. We aim to design new strategyproof mechanisms to this groupcentric fairness objective.

## Related Work

FLGs have received significant attention in the literature over the past decades, particularly following the influential

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16997

<!-- Page 2 -->

work of Procaccia and Tennenholtz (2009). For an overview of the diverse models, we refer readers to the comprehensive survey by Chan et al. (2021). In the remainder of this section, we focus specifically on research that investigates fairness notions within the context of facility location games.

There is a rich body of work studying fairness considerations in facility location problems from the optimization perspective. Early studies in the operations research community explored various equity-based fairness measures, including the standard deviation of distances (McAllister 1976) and the Gini coefficient (Marsh and Schilling 1994). In the context of algorithmic mechanism design, the pioneering work of Procaccia and Tennenholtz (2009) introduced the notion of individual fairness through the maximum cost objective, i.e., minimizing the maximum individual distance from any agent to the facility, and proposed strategyproof mechanisms that approximately optimize this objective. Building on this foundation, later research proposed alternative formulations of individual fairness. Cai, Filos-Ratsikas, and Tang (2016) studied the minimax envy objective, which captures fairness via the maximum difference in distances between any pair of agents; this framework was subsequently extended to the two-facility setting by Chen et al. (2022). Ding et al. (2020) introduced the envy ratio objective, adapted from the fair division problem, which measures the ratio of the best-off agent’s utility to that of the worst-off agent. This concept was further extended to the multi-facility case by Liu et al. (2020). Walsh (2025) studied the Gini index objective and proposed strategyproof mechanisms.

Fairness notions have also been extended from individuals to groups of agents. Zhou, Li, and Chan (2022); Li, Li, and Chan (2024) investigated two group-based fairness objectives: the maximum total cost (mtgc) and maximum average cost (magc), each capturing the worst-case burden across predefined groups of agents. Aziz et al. (2025) introduced a model of proportional fairness, in which fairness guarantees are provided to endogenously defined groups of agents, and the strength of the guarantee scales proportionally with group size. This concept was further extended by Lam et al. (2024) to the setting of obnoxious facility location, where the facility imposes disutility rather than providing benefit.

Roadmap Section 2 introduces the group-based facility location game model, formally defines our key objective, maximum group effect, and provides an overview of our main contributions. Section 3 focuses on the single-facility setting, where we propose two novel mechanisms tailored to distinct formulations of the maximum group effect objective. In Section 4, we extend our analysis to the multifacility setting and revisit the classical ENDPOINT mechanism within the framework. Due to space constraints, some proofs are omitted.

## Model

and Contributions Facility Location Games For any t ∈N, let [t]:= {1, 2,..., t}. A facility location game consists of a set N = [n] of n agents, belonging to m groups. For each agent i ∈N, her type is denoted as θi = (xi, gi) where xi ∈R is the agent’s private location on a line, and gi ⊆[m] denotes the set of their public group memberships. The type profile of all agents is denoted by θ = (θ1, θ2,..., θn). Without loss of generality, we assume that agents are indexed by x1 ≤x2 ≤· · · ≤xn. Let G be the set of groups, G = {G1, G2,..., Gm} where Gj = {i ∈N: j ∈gi} represents the set of agents belonging to group j. Denote by |Gj| the cardinality of Gj. For each group j ∈[m], j is assigned with a weight wj ≥0, reflecting their priority, such as socioeconomic factors or policy-driven importance. To simplify notation, let wmax = maxj∈[m] wj and wmin = minj∈[m] wj denote the maximum and minimum group weights, respectively, and let wgi = maxg∈gi{wg} denote the maximum weight among all the groups to which agent i belongs. A deterministic mechanisms f: Θn →Rk maps the type profile θ to locations of k facilities on a real line. Given any mechanism f, for each agent i, the cost incurred by i is defined as c(f(θ), xi) = miny∈f(θ) |y −xi|, i.e., the distance from xi to the nearest facility.

In this paper, we primarily focus on designing strategyproof mechanisms. A mechanism f is said to satisfy strategyproofness (SP) if it is in the best interests of every agent i to report their truthful location xi, irrespectively of the reports of the other agents. Definition 2.1 (Strategyproofness (SP)). A mechanism f is strategyproof if, for any agent i with true location xi and group gi, any misreported location x′ i ∈R, and any profile θ′

−i of other agents’ reports, we have:

c(f((xi, gi), θ′

−i), xi) ≤c(f((x′ i, gi), θ′

−i), xi).

Maximum Group Effect Given the requirement of strategyproofness, our goal is to design mechanisms that minimize inequity, as captured by the maximum group effect objective, aligning with the central notion proposed by Marsh and Schilling (1994). Formally, for any profile θ, the objective is to minimize the maximum group effect (mge), defined as mge(θ, f(θ)) = max j∈[m] Ej.

We further interpret the maximum group effect Ej for each group j in both utilitarian and egalitarian manners, incorporating the group-specific weight wj in both formulations. Specifically, one is termed Weighted Total Group Cost (wTGC), Ej = wj · P i∈Gj c(f(θ), xi), corresponding to the weighted sum of distances from all agents in group Gj to their assigned facilities. The other is termed Weighted Maximum Group Cost (wMGC), i.e., Ej = wj · maxi∈Gj c(f(θ), xi), representing the weighted maximum distance among agents in group Gj. mge prioritizes fairness by limiting the worst-case weighted burden among groups, aligning with principles of equitable resource allocation.

For any strategyproof mechanism, we evaluate the performance by the approximation ratio, defined as the worstcase ratio (over all possible instances) between the maximum group effect produced by the mechanism and the optimal solution.

16998

<!-- Page 3 -->

Definition 2.2 (Approximation Ratio). For any mechanism f, the approximation ratio is:

ρ = sup θ∈Θn mge(θ, f(θ)) mge(θ, OPT(θ)), where OPT(θ) is the optimal facility placement that minimizes mge objective under the profile θ.

In the following sections, we focus on deterministic strategyproof mechanisms that optimize the mge objective. We begin with the single-facility setting (k = 1) and then extend our analysis to the multi-facility scenario.

Our Contribution We advance the field of fair mechanism design in FLGs by introducing a unified framework that seamlessly integrates efficiency, individual fairness, and group fairness.

Capturing Fairness Through Generalized Metrics. We first introduce the general metric termed maximum group effect (mge), which is defined as mge = maxj∈[m] Ej. Here Ej is interpreted either the weighted total group cost (wTGC), i.e., Ej = wj·P i∈Gj c(f(θ), xi), or the weighted maximum group cost (wMGC), i.e., Ej = wj ·maxi∈Gj c(f(θ), xi). Our proposed mge objective offers a unified framework for analyzing efficiency and fairness in facility location problems, which captures a broad range of objectives by appropriately adjusting the group partitioning and weight assignments, as illustrated in Figure 1.

mge wTGC wMGC mtgc magc Social Cost Max Cost wj = 1 wj = 1 |Gj| m = 1 m = n m = 1

**Figure 1.** mge: a generalization of objective metric.

Unified Mechanisms with Tight Approximation Guarantee. We propose two novel strategyproof mechanisms: the BALANCED mechanism and the MAJOR-PHANTOM mechanism. The BALANCED mechanism, a flagship contribution for single-facility location games, not only unifies classic facility location mechanisms, but also provides tight results for group-fairness objectives. Specifically, regarding the social cost objective, the BALANCED mechanism aligns with the median-point mechanism, while for the maximum cost objective, it degenerates to the LEFTMOST mechanism. In the context of group fairness, it achieves 2-approximation ratios for both maximum total group cost (mtgc) and maximum average group cost (magc), closing the bound gap in (Zhou, Li, and Chan 2022). Furthermore, we prove that the BALANCED mechanism provides tight bounds for any weighted total group cost objective. Consequently, this unification establishes the BALANCED mechanism as a versatile instrument capable of adapting to diverse fairness and efficiency goals without bespoke designs for objectives. To optimize the weighted maximum group cost objective, we introduce the MAJOR-PHANTOM mechanism and show it provides tight results for this objective.

In the two-facility setting (see Section 4), we revisit the ENDPOINT mechanism (Procaccia and Tennenholtz 2009), which places facilities at the leftmost and rightmost agent locations. For both wTGC and wMGC, we show it achieves tight bounds. For settings beyond two facilities (k > 2), we leverage results from Fotakis and Tzamos (2014) to show that all strategyproof, anonymous, and deterministic mechanisms yield unbounded approximation ratios. Our established tight approximation ratios and matching lower bounds are comprehensively summarized in Table 1.

Setting Objectives Mechanisms Bounds k = 1 wTGC BALANCED 2 wMGC MAJOR-PHANTOM 2 k = 2 wTGC ENDPOINT 1 + (n −2) wmax wmin wMGC ENDPOINT 1 + wmax wmin k ≥3 General / ∞

**Table 1.** Summary of results. All listed bounds are tight. Gray shading denotes the contributions of this work.

Single-Facility Mechanism Design

We begin by considering single-facility setting (k = 1). For the wTGC group effect metric, i.e., Ej = wj · P i∈Gj c(f(θ), xi), we propose the BALANCED mechanism which places the facility at the location under which the maximum weighted values are balanced. Regarding the wMGC objective where Ej = wj · maxi∈Gj c(f(θ), xi), we introduce the MAJOR-PHANTOM mechanism, which places the facility at the median-point of the locations of agents in the group Gmax with the largest weight, together with (|Gmax| −1) constant phantom points. For both cases, we provide tightness results, showing the optimality of the proposed mechanisms.

Weighted Total Group Cost

We first look at the weighted total group cost (wTGC) objective, where Ej = wj · P i∈Gj c(f(θ), xi). As illustrated in Figure 1, the wTGC metric subsumes several wellstudied objectives, including the social cost, maximum cost, and group-fairness objectives mtgc and magc. To address this generalized setting, we introduce our first BALANCED mechanism (Mechanism 1), which places the facility at a location that equilibrates the weighted number of agents on either side of it.

Intuitively, the BALANCED mechanism defines, for each group j ∈[m] and location y ∈R, two functions Lj(y) and Rj(y), representing respectively the number of agents in group j located at or to the left of y, and those located to its right. Since wjLj(y) is non-decreasing and wjRj(y) is non-increasing over y ∈[x1, xn], the mechanism places the facility at a location that most closely balances the two

16999

<!-- Page 4 -->

Mechanism 1: BALANCED Mechanism Input: Agent profile θ, group weights {wj}j∈[m].

1: Define Lj(y) ←|{i ∈N: xi ≤y and j ∈gi}| and Rj(y) ←|{i ∈N: xi > y and j ∈gi}|. 2: Compute f(θ)←min y∈R: max j∈[m]wjLj(y)≥max j′∈[m]wj′Rj′(y)

.

Output: Facility location f(θ).

quantities maxj∈[m] wjLj(y) and maxj∈[m] wjRj(y). The BALANCED mechanism can be implemented in O((n + m) log n) time by performing a binary search over the sorted agent locations to identify the smallest xi satisfying maxj∈[m] wjLj(xi) ≥maxj′∈[m] wj′Rj′(xi). Each iteration of the binary search requires evaluating these maximum functions, which takes O(n + m) time.

Proposition 3.1. The BALANCED mechanism coincides with the median-point mechanism (resp. leftmost mechanism) when the mge objective degenerates to the social cost (resp. maximum cost) objective.

We next present the main theorem for the BALANCED mechanism, which satisfies strategyproofness and achieves a 2-approximation for minimizing the mge objective when Ej = wj · P i∈Gj c(f(θ), xi) for all j ∈[m].

Theorem 3.2. The BALANCED mechanism is strategyproof and has an approximation ratio of 2 for minimizing mge when Ej = wj · P i∈Gj c(f(θ), xi).

Proof. Strategyproofness. Let f(θ) denote the outcome of the BALANCED mechanism, and consider any agent i with truthful location xi. We prove by discussing the relative positions of f(θ) and xi. Clearly, if xi coincides with f(θ), agent i has no incentive to misreport her location. Case (1). If xi < f(θ), misreporting x′ i < f(θ) will not change the facility location as Lj(f(θ)) and Rj(f(θ)) don’t change for all j ∈[m]. If agent i misreports to x′ i ≥f(θ), we have that Lj(f(θ)) decreases and Rj(f(θ)) increases for each j ∈ gi, potentially shifting the facility location rightward as maxj′∈[m]{wj′Rj′(f(θ))} increases while maxj∈[m] wj{Lj(f(θ))} decreases. Consequently, agent i’s cost increases as the facility moves farther from xi, implying that misreporting cannot be beneficial. We next consider Case (2). If xi > f(θ), similarly, when misreporting x′ i > f(θ), the facility location remains at f(θ). When x′ i ≤f(θ), by an analogical induction, it could only potentially pushing the facility location farther away from agent i’s location xi. Hence, we conclude that for any agent i ∈N, i has no incentive to misreport her location, which implies the BALANCED mechanism is strategyproof.

Approximation Ratio. Denote by f(θ) the BALANCED mechanism outcome and y∗= arg miny∈R mge(θ, y) the optimal location for profile θ. We begin with a key observation that underpins the proof of the approximation ratio. Given any profile θ, we construct a modified profile θ′ by relocating all agents whose positions lie between f(θ) and y∗to the point y∗. Under the construction, we first observe that for each agent i who lies between f(θ) and y∗, c(f(θ), xi) increases while c(y∗, xi) decreases, which follows that mge(θ′, f(θ)) ≥mge(θ, f(θ)) and mge(θ′, y∗) ≤mge(θ, y∗). Let ρ(θ) (resp. ρ(θ′)) denote the approximation ratio under θ (resp. θ′). By construction, we have ρ(θ) ≤ρ(θ′). Henceforth, we focus exclusively on profiles involving such movements. For the sake of clarity, we will abuse the notation θ to refer to the modified profile.

Case 1: f(θ) ≤y∗. For each group Gj, the group effects under f(θ) and y∗are expressed as Ej(f(θ)) = wj

P i∈Gj |f(θ) −xi| and Ej(y∗) = wj

P i∈Gj |y∗−xi|. Viewing Ej(y) as a function of location y. its derivative can be expressed as dEj(y)

dy = wj · (−Lj(y) + Rj(y)). Consequently, we derive that

Ej(f(θ)) −Ej(y∗) =

Z y∗ f(θ)

wj · (Rj(y) −Lj(y))dy.

Since there is no agent located in the interval [f(θ), y∗), the derivative is a constant value. We further have

Ej(f(θ))−Ej(y∗)=wj(Rj(f(θ))−Lj(f(θ)))·(y∗−f(θ)).

Recall that mge(θ, f(θ)) = maxj∈[m] Ej(f(θ)) and mge(θ, y∗) = maxj∈[m] Ej(y∗). We then have mge(θ, f(θ)) −mge(θ, y∗)

≤max j∈[m]{Ej(f(θ)) −Ej(y∗)}

≤max j∈[m]{wj(Rj(f(θ)) −Lj(f(θ)))(y∗−f(θ))}.

On the other hand, there are Lj(f(θ)) agents in each group Gj who are at or on the left of f(θ). It follows that mge(θ, y∗) ≥max j∈[m]{wj · Lj(f(θ))} · (y∗−f(θ)).

Moreover, we have maxj∈[m]{wjRj(f(θ))} ≤ maxj∈[m]{wjLj(f(θ))} as f(θ) is the outcome by BALANCED mechanism. With these inequalities in hand, we derive the approximation ratio ρ of the BALANCED mechanism.

ρ = mge(θ, f(θ))

mge(θ, y∗) = 1 + mge(θ, f(θ)) −mge(θ, y∗)

mge(θ, y∗)

≤1+ maxj∈[m]{wj(Rj(f(θ))−Lj(f(θ)))}(y∗−f(θ))

maxj∈[m]{wjLj(f(θ))}(y∗−f(θ))

≤1+ maxj∈[m]{wjRj(f(θ))}

maxj∈[m]{wjLj(f(θ))} ≤2.

Case 2: When f(θ) > y∗. Keep in mind that we still have the derivative expression for function Ej(y). Observe that in the interval [y∗, f(θ)), the derivative of function Ej(y) is a constant value as there is no agent in the interval. By an analogous approach, we have

Ej(f(θ))−Ej(y∗) = wj(Rj(y∗)−Lj(y∗)) · (f(θ) −y∗).

17000

<!-- Page 5 -->

We next establish the group effect difference between solution f(θ) and y∗.

mge(θ, f(θ)) −mge(θ, y∗)

≤max j∈[m]{Ej(f(θ)) −Ej(y∗)}

≤max j∈[m]{wj(Rj(y∗) −Lj(y∗))(y∗−f(θ))}.

Since we know that there is no agent in the interval (y∗, f(θ)), then for all the agents on the right of y∗, they must satisfy xi ≥f(θ). Therefore, we can bound mge(θ, y∗) by mge(θ, y∗) ≥max j∈[m]{wj · Rj(y∗)} · (f(θ) −y∗).

Based on the aforementioned analysis, we derive the approximation ratio ρ = mge(θ, f(θ))

mge(θ, y∗)

≤1 + maxj∈[m]{wj(Rj(y∗) −Lj(y∗))}(f(θ) −y∗)

maxj∈[m]{wj · Rj(y∗)}(f(θ) −y∗)

≤1 + maxj∈[m]{wjRj(y∗)}

maxj∈[m]{wjRj(y∗)} = 2.

Combining the analyses of both cases, we conclude that the BALANCED mechanism achieves an approximation ratio of 2 for minimizing the maximum group effect when Ej = wj · P i∈Gj c(f(θ), xi).

Since mge generalizes the maximum cost objective when m = n and Gj = {j} with equal weights, the lower bound from Procaccia and Tennenholtz (2009) applies, confirming the tightness of BALANCED ’s approximation ratio. Corollary 3.3 (Procaccia and Tennenholtz 2009). Any deterministic mechanism has an approximation ratio of at least 2 for mge when Ej = wj · P i∈Gj c(f(θ), xi).

Note that mge also generalizes the group-fairness objectives mtgc and magc proposed by Zhou, Li, and Chan (2022) for which the approximation ratios remained an open question, with a 3-approximation upper bound and a 2-approximation lower bound. Our proposed BALANCED mechanism now closes the gap. Corollary 3.4. The BALANCED mechanism achieves a 2approximation ratio w.r.t. the mtgc and magc objectives.

Weighted Maximum Group Cost We next turn to the weighted maximum group cost objective, wherein Ej = wj · maxi∈Gj c(f(θ), xi). Intuitively, it is a weighted maximum cost problem where each agent i is assigned with a maximum weight wgi = maxj∈gi wj, and the objective is to minimize the maximum value of wgi · c(f(θ), xi) over all agents i ∈N. In view of this, we propose the MAJOR-PHANTOM mechanism (Mechanism 2) which selects the facility location by prioritizing the group with the largest weight wj.

MAJOR-PHANTOM mechanism extends the PHANTOM mechanisms (Moulin 1980) by prioritizing agents in the

Mechanism 2: MAJOR-PHANTOM Mechanism Input: Agent profile θ, group weights {wj}j∈[m].

1: Let Gmax denote the largest weight group and xGmax = {xGmax

1,..., xGmax

|Gmax|} denote the location profile of agents in G∗, tie-breaking in favor of the smallest index. 2: Let v1 ≤· · · ≤v|Gmax|−1 denote |Gmax| −1 values v1 ≤· · · ≤v|Gmax|−1. 3: f(θ) ← median(xGmax, v1,..., v|Gmax|−1), tiebreaking by selecting the leftmost. Output: Facility location f(θ).

largest-weighted group, thereby ensuring fairness for groups with greater importance. Before analyzing the approximation ratio of the MAJOR-PHANTOM mechanism with respect to the wMGC objective, we first provide a characterization of the optimal solution in two-agent instances, which will facilitate the subsequent analysis.

Lemma 3.5. Given two-agent profile θ and optimal solution y∗, for any two agents with locations x1 ≤x2 and maximum weights wg1, wg2 ≥0, mge(θ, y∗) = maxj∈[m] wj · maxi∈Gj |y∗−xi| is either

• wg1 · (x2−x1) 2 when g1 = g2 with the maximum weight wg1, achieved at y∗= x1+x2

2; or

• wg1·wg2·(x2−x1)

wg1+wg2 when wg1̸ = wg2, achieved at y∗= wg2x2+wg1x1 wg1+wg2.

We next prove that for any MAJOR-PHANTOM mechanism, it is strategyproof and achieves an approximation ratio of 2 for minimizing mge under the wMGC objective.

Theorem 3.6. Any MAJOR-PHANTOM mechanism is strategyproof and has an approximation ratio of 2 for minimizing the mge objective when Ej = wj · maxi∈Gj c(f(θ), xi).

Proof. Strategyproofness. Given any agent profile θ, consider an agent i ∈N with true location xi. If i /∈Gmax, it is clear that misreporting cannot influence the facility location under the mechanism. If i ∈Gmax, then since group membership cannot be misreported, we can apply a similar analytical approach to that used in the proof of strategyproofness for PHANTOM mechanisms by Moulin (1980).

Approximation Ratio. Given any profile θ, let f(θ) denote the location outputted by the MAJOR-PHANTOM mechanism and y∗denote the optimal location under θ.

We first consider the case that y∗≥f(θ). Suppose that mge(θ, f(θ)) is achieved by agent ℓ. We first observe that if xℓ≤f(θ), we have mge(θ, f(θ)) = wgℓ· (f(θ) −xℓ) and mge(θ, y∗) ≥wgℓ· (y∗−xℓ), which gives us ρ = mge(θ, f(θ))

mge(θ, y∗) ≤wgℓ· (f(θ) −xℓ)

wgℓ· (y∗−xℓ) ≤1.

If xℓ> f(θ), let k ∈Gmax be the agent in group Gmax whose location xk satisfies xk = minj∈Gmax |xj −f(θ)| with the additional condition that xk ≤f(θ). That is, xk is

17001

<!-- Page 6 -->

the closest agent to the left of f(θ) within Gmax1. We claim that such an agent k always exists. Toward this end, suppose, for the sake of contradiction, that no such xk exists. It implies that all the agents’ locations {xGmax

1,..., xGmax

|Gmax|}

lie strictly to the right of f(θ), i.e., xGmax i > f(θ) for all i ∈Gmax. However, under the MAJOR-PHANTOM mechanism, the facility is placed at the median of the multiset {xGmax, v1,..., v|Gmax|−1}, which has a size of 2·|Gmax|− 1. In this case, there can be at most |Gmax|−1 points strictly to the right of f(θ), contradicting the assumption. Therefore, such an agent k always exists.

If xk ≤f(θ) < xℓ< y∗, we have mge(θ, f(θ)) = wgℓ· (xℓ−f(θ)) ≤wgℓ· (xℓ−xk) and mge(θ, y∗) ≥ wgk ·(y∗−xk) ≥wgk ·(xℓ−xk). Hence, the approximation ratio is expressed as ρ = mge(θ, f(θ))

mge(θ, y∗) ≤wgℓ· (xℓ−xk)

wgk · (xℓ−xk) = wgℓ wgk

.

Recall the definition of MAJOR-PHANTOM mechanism. We know that ρ ≤ wgℓ wgk = wgℓ wmax ≤1 as wgk = wmax ≥wgℓ. If xk ≤f(θ) < y∗< xℓ, we have mge(θ, f(θ)) = wgℓ· (xℓ−f(θ)) ≤wgℓ· (xℓ−xk). By Lemma 3.5, when only considering agent k and ℓ, we have the maximum cost achieved by these two agents is at least wgℓwgk (xℓ−xk)

wgℓ+wgk.

Hence, we have mge(θ, y∗) ≥ wgℓwgk (xℓ−xk)

wgℓ+wgk. Consequently, the approximation ratio is bounded by ρ = mge(θ, f(θ))

mge(θ, y∗) ≤wgℓ· (xℓ−xk)

wgℓwgk (xℓ−xk)

wgℓ+wgk

= wgℓ+ wgk wgk

.

Since wgk = wmax ≥wgℓ, it follows that ρ = wgℓ+wgk wgk = wgℓ+wmax wmax ≤2. For the case where y∗< f(θ), the same approximation ratio of 2 can be established by applying an analogous analysis to that used for the case f(θ) ≥y∗.

Notice that the mge objective coincides with the maximum cost objective when m = n and Gj = {j} with equal weights. In this case, the lower bound of 2 for the maximum cost objective established by Procaccia and Tennenholtz (2009) applies, thereby confirming the tightness of the bounds achieved by the MAJOR-PHANTOM mechanism. Corollary 3.7 (Procaccia and Tennenholtz 2009). Any deterministic, strategyproof mechanism has an approximation ratio of at least 2 for mge when Ej = wj · maxi∈Gj c(f(θ), xi).

## 4 Multi-Facility Mechanism Analysis

In this section, we extend our analysis from single-facility to multi-facility settings. In view of the impossibility result of Fotakis and Tzamos (2014), which shows that for k ≥3, no deterministic, anonymous, and strategyproof mechanism can achieve a bounded approximation ratio for either the social cost or maximum cost objectives, our primary focus is on the two-facility case (k = 2).

1If multiple agents satisfy this condition, we break ties by selecting the agent with the largest index k.

Corollary 4.1. When k ≥ 3, there is no deterministic, anonymous, strategyproof mechanisms with a bounded approximation ratio for mge, for either Ej = wj · P i∈Gj c(f(θ), xi) or Ej = wj · maxi∈Gj c(f(θ), xi).

We next restrict our attention to the case of k = 2 and revisit the ENDPOINT mechanism (placing facilities at the leftmost and rightmost agent locations), which remains the only known deterministic, anonymous, and strategyproof mechanism with bounded approximation guarantees for these objectives (Fotakis and Tzamos 2014).

While Fotakis and Tzamos (2014) established that the ENDPOINT mechanism is the only deterministic, anonymous, and strategyproof mechanism with bounded approximation guarantees for social cost in the two-facility setting (k = 2), evaluating its performance under our group-centric mge objective presents a novel and nontrivial challenge. Unlike classical objectives, the mge objective requires accounting for weighted group effects, where both the group structures and the distribution of group weights play a critical role, which demand a fundamentally different analytical approach. Our contribution lies in establishing tight approximation bounds for the ENDPOINT mechanism under mge, thereby extending its applicability to equitable facility placement and offering theoretical insights into group fairness.

Weighted Total Group Cost We first explore the maximum group effect objective by considering the weighted total group cost (wTGC). Our result shows that the ENDPOINT mechanism achieves an approximation ratio of 1 + (n −2) · wmax wmin.

Theorem 4.2. The ENDPOINT mechanism has an approximation ratio of 1 + (n −2) wmax wmin for minimizing mge when Ej = wj · P i∈Gj c(f(θ), xi).

Proof. Given any agent profile θ, let Y = (x1, xn) denote the outputs of the ENDPOINT mechanism and Y ∗= (y∗

1, y∗ 2) (w.l.o.g, y∗ 1 ≤y∗ 2) denote the optimal facility locations which achieves optimal mge(θ, Y ∗). We first observe that x1 ≤y∗

1 ≤y∗ 2 ≤xn. For any group Gj, suppose there are kj

1 agents (excluding agent 1) who are assigned to facility y∗

1 while kj 2 agents (excluding agent n) assigned to facility y∗

2 2. Now we consider the follow movement, moving one facility from y∗

1 to x1 and the other facility from y∗ 2 to xn. For group Gj, after the movement, the changes of the group effect is expressed as

Ej(Y)−Ej(Y ∗) ≤wj kj

1(y∗ 1 −x1) + kj 2(xn −y∗ 2)

≤wj(kj

1 + kj 2)·max{y∗ 1 −x1, xn −y∗ 2} ≤wj(n −2)·max{y∗

1 −x1, xn −y∗ 2}.

Recall that wmax = maxj wj and wmin = minj wj. Now we consider the mge objective and have mge(θ, Y) −mge(θ, Y ∗) ≤max j∈[m](Ej(Y) −Ej(Y ∗))

≤wmax · (n −2) · max{y∗

1 −x1, xn −y∗ 2}. (1)

2Breaking ties by assigning to y∗ 1

17002

<!-- Page 7 -->

On the other hand, since there exists at least one agent who is assigned to each facility under the optimal solution Y ∗, we have the lower bound that mge(θ, Y ∗) ≥max{wg1(y∗

1 −x1), wgn(xn −y∗ 2)} ≥wmin · max{y∗

1 −x1, xn −y∗ 2}. (2)

From Equation (1) and Equation (2), we derive the upper bound of the approximation ratio ρ mge(θ, Y) mge(θ, Y ∗) ≤1 + (n −2)wmax ·max {y∗

1 −x1, xn −y∗ 2} max {wg1(y∗

1 −x1), wgn(xn −y∗ 2)}

≤1 + (n −2)wmax ·max {y∗

1 −x1, xn −y∗ 2} wmin max {y∗

1 −x1, xn −y∗ 2}

≤1 + (n −2)wmax wmin

.

To show the tightness, consider an instance with n agents where x1 = 0, x2 = x3 = · · · = xn−1 = 1

2, and xn = 1, and G1 = {1}, G2 = {2, 3,..., n}. For group weights, let w1 = wmin and w2 = wmax. We first observe the optimal solution Y ∗= (y∗

1 = wmax(n−2) 2[wmin+wmax(n−2)], y∗ 2 = 1), achieving mge(θ, Y ∗) = wminwmax(n−2) 2[wmin+wmax(n−2)]. In contrast, the ENDPOINT mechanism has an mge of wmax(n−2)

2. This gives us an approximation ratio of 1 + (n −2) · wmax wmin.

We adapt the characterization of Fotakis and Tzamos (2014), which identifies the ENDPOINT mechanism as the unique deterministic, anonymous, and strategyproof mechanism with bounded approximation ratio for k = 2, to establish the tightness.

Proposition 4.3. Any deterministic, strategyproof mechanism has an approximation ratio of at least 1+(n−2)· wmax wmin when Ej = wj · P i∈Gj c(f(θ), xi).

Weighted Maximum Group Cost

We now turn to the weighted maximum group cost (wMGC) objective. Under this criterion, the ENDPOINT mechanism attains an approximation ratio of (1 + wmax wmin).

Theorem 4.4. The ENDPOINT mechanism has an approximation ratio of 1 + wmax wmin for minimizing mge when Ej = wj · maxi∈Gj c(f(θ), xi).

Proof. Given any agent profile θ, Denote by Y = (x1, xn) the outputs of the ENDPOINT mechanism and Y ∗ = (y∗

1, y∗ 2) (y∗ 1 ≤y∗ 2) the optimal facility placement which achieves optimal mge(θ, Y ∗). We first observe that x1 ≤ y∗

1 ≤ y∗

2 ≤ xn. Without loss of generality, assume mge(θ, Y) is achieved by agent k and xk ≤ x1+xn

2, i.e., k is assigned to facility located at x1 under Y.

Case 1. When x1 ≤xk ≤y∗

1, we have mge(θ, Y) = wgk(xk −x1) and mge(θ, Y ∗) ≥wg1(y∗

1 −x1). The approximation ratio ρ is upper-bounded by mge(θ, Y) mge(θ, Y ∗) ≤wgk·(xk −x1)

wg1·(y∗

1 −x1) ≤wgk·(xk −x1) wg1·(xk −x1) ≤wmax wmin

.

Case 2. When y∗

1 < xk < y∗ 2 and k is assigned to y∗ 1. By Lemma 3.5, we have mge(θ, Y ∗) ≥ wg1wgk (xk−x1)

wg1+wgk and the approximation ratio ρ is upper-bounded by mge(θ, Y) mge(θ, Y ∗) ≤wgk · (xk −x1)

wg1wgk (xk−x1)

wg1+wgk

≤1 + wgk wg1

≤1 + wmax wmin

.

Case 3. When y∗

1 < xk < y∗ 2 and agent k is assigned to y∗

2. Similarly, we can lower-bound mge(θ, Y ∗) ≥ wgk wgn(xn−xk)

wgk +wgn. Recall that xk ≤ x1+xn

2. It implies that xk −x1 ≤xn −xk. So we have the lower bound for the approximation ratio ρ that mge(θ, Y) mge(θ, Y ∗) ≤wgk · (xk −x1)

wgk wgn(xn−xk)

wgk +wgn

≤1 + wgk wgn

≤1 + wmax wmin

.

Case 4. When y∗

2 ≤xk ≤xn. In this case, agent k is assigned to the facility located at y∗

2. Hence we derive that mge(θ, Y ∗) ≥wn(xn −y∗

2). Consequently, the approximation ratio ρ satisfies ρ = mge(θ,Y) mge(θ,Y ∗) ≤ wgk ·(xk−x1)

wn·(xn−y∗

2). Note that we also have xk −x1 ≤xn −xk and xn −y∗

2 ≥xn −xk. Therefore, we bound the approximation ratio ρ by mge(θ, Y) mge(θ, Y ∗) ≤wgk·(xk −x1)

wn·(xn −y∗

2) ≤wgk·(xn −xk) wn·(xn −xk) ≤wmax wmin

.

Combining the analysis across all four cases, we conclude that the ENDPOINT mechanism achieves an approximation ratio of 1 + wmax wmin. To establish the tightness of this bound, consider the following instance. There are n agents where x1 = x2 = · · · = xn−2 = 0, xn−1 = 1 2, and xn = 1. The group structure is given by G1 = {1}, and G2 = {2, 3,..., n} with weights w1 = wmin, and w2 = wmax. We first identify that the optimal solution is Y ∗= (y∗

1 = wmax 2(wmax+wmin), y∗ 2 = 1), achieving an mge value of wmin·wmax 2(wmin+wmax). In contrast, the ENDPOINT mechanism attains an mge value of wmax

2, implying that it has an approximation ratio of 1 + wmax wmin.

Proposition 4.5. Any deterministic, strategyproof mechanism has an approximation ratio of at least 1 + wmax wmin when Ej = wj · maxi∈Gj c(f(θ), xi).

## 5 Conclusion and Discussion

We study facility location games through the lens of fairness by introducing a unified framework based on the maximum group effect, a general metric that encompasses a broad class of classical objectives. In the single-facility setting, we develop two strategyproof mechanisms, BALANCED and MAJOR-PHANTOM, both of which achieve tight approximation guarantees for minimizing the maximum group effect. Our results further close the open approximation gaps for group-fairness objectives identified by Zhou, Li, and Chan (2022). In the two-facility setting, we revisit the classical ENDPOINT mechanism and establish tight approximation bounds. Looking forward, promising research directions include extending our framework to randomized mechanisms to circumvent the impossibility of achieving bounded approximations for k ≥3, as well as adapting the mge objective to higher dimensional metric spaces.

17003

<!-- Page 8 -->

## Acknowledgements

This work was supported by the NSF-CSIRO grant on “Fair Sequential Collective Decision-Making” (RG230833) and the ARC Laureate Project FL200100204 on “Trustworthy AI”. The authors would like to express their gratitude to the anonymous reviewers of AAAI 2026 for their insightful and constructive feedback, which greatly helped improve this paper.

## References

Aziz, H.; Lam, A.; Lee, B. E.; and Walsh, T. 2025. Proportionality-based fairness and strategyproofness in the facility location problem. Journal of Mathematical Economics, 119: 103129.

Cai, Q.; Filos-Ratsikas, A.; and Tang, P. 2016. Facility location with minimax envy. In Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI), 137–143.

Chan, H.; Filos-Ratsikas, A.; Li, B.; Li, M.; and Wang, C. 2021. Mechanism Design for Facility Location Problems: A Survey. In Proceedings of the 30th International Joint Conference on Artificial Intelligence (IJCAI), 4356–4365.

Chen, X.; Fang, Q.; Liu, W.; Ding, Y.; and Nong, Q. 2022. Strategyproof mechanisms for 2-facility location games with minimax envy. Journal of Combinatorial Optimization, 43(5): 1628–1644.

Ding, Y.; Liu, W.; Chen, X.; Fang, Q.; and Nong, Q. 2020. Facility location game with envy ratio. Computers & Industrial Engineering, 148: 106710.

Fotakis, D.; and Tzamos, C. 2014. On the Power of Deterministic Mechanisms for Facility Location Games. ACM Transactions on Economics and Computation, 2(4): 15:1– 15:37.

Lam, A.; Aziz, H.; Li, B.; Ramezani, F.; and Walsh, T. 2024. Proportional fairness in obnoxious facility location. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 1075– 1083.

Li, J.; Li, M.; and Chan, H. 2024. Strategyproof Mechanisms for Group-Fair Obnoxious Facility Location Problems. In Proceedings of the 38th AAAI Conference on Artificial Intelligence, (AAAI), 9832–9839.

Liu, W.; Ding, Y.; Chen, X.; Fang, Q.; and Nong, Q. 2020. Multiple Facility Location Games with Envy Ratio. In Proceedings of the 14th International Conference on Algorithmic Aspects in Information and Management (AAIM), 248–259.

Marsh, M. T.; and Schilling, D. A. 1994. Equity measurement in facility location analysis: A review and framework. European journal of operational research, 74(1): 1–17.

McAllister, D. M. 1976. Equity and efficiency in public facility location. Geographical analysis, 8(1): 47–63.

Moulin, H. 1980. On strategy-proofness and single peakedness. Public Choice, 35(4): 437–455.

Procaccia, A. D.; and Tennenholtz, M. 2009. Approximate mechanism design without money. In Proceedings of the 10th ACM Conference on Electronic Commerce (EC), 177– 186. Rawls, J. 1958. Justice as fairness. The philosophical review, 67(2): 164–194. Walsh, T. 2025. Equitable Mechanism Design for Facility Location. In Proceedings of the 34th International Joint Conference on Artificial Intelligence, (IJCAI), 275–283. Zhou, H.; Li, M.; and Chan, H. 2022. Strategyproof Mechanisms for Group-Fair Facility Location Problems. In Proceedings of the 31st International Joint Conference on Artificial Intelligence and the 25th European Conference on Artificial Intelligence (IJCAI), 613–619.

17004
