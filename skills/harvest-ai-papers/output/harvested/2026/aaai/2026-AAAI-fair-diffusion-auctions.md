---
title: "Fair Diffusion Auctions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38746
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38746/42708
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Fair Diffusion Auctions

<!-- Page 1 -->

Fair Diffusion Auctions

Zixin Gu1, Yaoxin Ge1, Yao Zhang2, Dengji Zhao1

1Key Laboratory of Intelligent Perception and Human-Machine Collaboration, ShanghaiTech University 2Kyushu University guzx@shanghaitech.edu.cn, geyx@shanghaitech.edu.cn, zhang@agent.inf.kyushu-u.ac.jp, zhaodj@shanghaitech.edu.cn

## Abstract

Diffusion auction design is a new trend in mechanism design which extends the original incentive compatibility property to include buyers’ private connection report. Reporting connections is equivalent to inviting their neighbors to join the auction in practice. Then, the social welfare is collectively accumulated by all participants: reporting high valuations or inviting high-valuation neighbors. Hence, we can measure each participant’s contribution by the marginal social welfare increase due to her participation. Therefore, in this paper, we introduce a new property called Shapley fairness to capture participants’ social welfare contribution and use it as a benchmark to guide our auction design for a fairer utility allocation. Not surprisingly, none of the existing diffusion auctions has ever approximated the fairness, because Shapley fairness depends on each buyer’s own valuation and this dependence can easily violate incentive compatibility. Thus, we combat this challenge by proposing a new diffusion auction called Permutation Diffusion Auction (PDA) for selling k homogeneous items, which is the first diffusion auction satisfying k+1-Shapley fairness, incentive compatibility and individual rationality. Moreover, PDA can be extended to the general combinatorial auction setting where the literature did not discover meaningful diffusion auctions yet.

## Introduction

Auction design over social networks, known as diffusion auction design, explored many novel mechanisms since the first diffusion auction proposed by Li et al. (2017) (Guo and Hao 2021; Li et al. 2022; Zhao 2022). Different from the traditional auction design, diffusion auction considers buyers’ private connections to other buyers. Buyers are asked to report their connections, which is equivalent to inviting their neighbors to join the market in practice (it is assumed that not all buyers are in the market initially), which enlarges the market for other purposes such as improving social welfare or the seller’s revenue. We want to design a mechanism to incentivize buyers to report their connections truthfully, so that all potential buyers can participate in the auction. However, this is challenging because buyers’ strategical action space has one more dimension (their connections) and all the traditional mechanisms are not suitable to prevent manipulations in the new space.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

The first diffusion auction, called Information Diffusion Mechanism (IDM) (Li et al. 2017), was designed for selling a single item in a network. It prioritises cut-points in the network from the seller to the winner and gives them sensible utilities to reward them to connect to the winner. Despite its novelty, IDM also has an inherent limitation: only the cut points on the path to reach the winner may gain a positive utility and the incentive for the other buyers to join the auction is very weak (their utilities are zero). This limitation weakens the applicability of IDM to actually enlarge a market. Thus, Zhang et al. (2019) (Zhang, Zhao, and Zhang 2020) considered about this limitation and proposed a variation to reward more buyers. It allows positive rewards for buyers who are not cut-points but are on some simple paths from the seller to the winner. However, this limitation was not fully resolved in their solution: (1) some buyers were still not allowed to get positive rewards; (2) the rewards are not related to their contributions. The limitation justifies the necessity for fairer diffusion auctions to better motivate all buyers to invite their neighbors to join the auction.

To solve the limitation above, a proper measure for rewarding buyers who are not on paths connecting to the winner is required. We consider a fair measure to satisfy the following requirements:

1. The social welfare is distributed to the agents efficiently; 2. agents with the same contributions have the same utility; 3. if one agent always contributes more than the other, then she should receive a higher utility than the other; 4. agents that do not contribute should receive 0 utility.

In cooperative game theory, it is proved that there exists a unique value, called Shapley value, satisfying these constraints (Shapley et al. 1953; Roth 1988; Young 1985). Similarly, we can define Shapley contribution as the measure here, which is the average marginal social welfare contribution of a player on all possible joining sequences.

Following the Shapley contribution, we define ϵ-Shapley fairness (ϵ-SF), which quantifies how close the buyers’ utilities are with their Shapley contributions, to evaluate the fairness of a diffusion auction. Under this, we show that all the existing diffusion auctions are not Shapley fair, which reflects the limitation we discussed above. The main difficulty is that Shapley fairness depends on each buyer’s own valuation and the dependence can easily violate truthful reporting.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16989

<!-- Page 2 -->

Against this background, we design the very first fair diffusion auction, named Permutation Diffusion Auction (PDA), for selling k homogeneous items. PDA imitates the calculation process of the Shapley contribution, but eliminates the dependency of a buyer’s payment on her valuation. We show that PDA satisfies 1 k+1-Shapley fairness, incentive compatibility, and individual rationality. Moreover, PDA can be generalized to combinatorial settings and still maintains its commitment to fairness, achieving 1 n-Shapley fairness when selling items in a network with n buyers.

Our Contributions We study one fairness of diffusion auctions and introduce a new property called Shapley fairness to evaluate the fairness. We then propose a new mechanism to approximate the fairness in all diffusion auction settings. Specifically, 1. We define the Shapley contribution by mimicing the Shapley value in a diffusion auction setting. Then we use Shapley contribution to define a fairness property. 2. For auctioning k homogeneous items, we propose a Permutation Diffusion Auction (PDA) to achieve 1 k+1- Shapley fair. 3. For combinatorial settings, we extend PDA to achieve at least 1 n-Shapley fair with n buyers.

## Related Work

Single-item Diffusion Auctions. Information Diffusion Mechanism (IDM) (Li et al. 2017), the first diffusion auction, was designed for selling a single item in a network and it prevented manipulations in the new space by offering priorities to the cut points to the winner in the network. IDM treated these cut points as sellers, which made them gain a profit from reselling the item to incentivize them to report their connections truthfully. Follow-up mechanisms were then proposed. Critical Diffusion Mechanism (CDM) (Li et al. 2019) was developed from IDM for further improving the seller’s revenue. Fair Diffusion Mechanism (FDM) (Zhang, Zhao, and Zhang 2020) rewarded noncut-point buyers with redistribution techniques. Sybil Cluster Mechanism (SCM) (Chen et al. 2023) achieved Sybilproofness; Sequential Resale Auction (SRA) (Liu, Zhang, and Zhao 2023) focused on distributed scenarios; Closest Winner of Myerson’s (CWM) (Zhang, Zheng, and Zhao 2024) was dedicated to maximizing the seller’s revenue. All existing mechanisms chose certain buyers on the paths from the seller to the winner to offer positive utilities. They are not Shapley fair because some contributed participants would receive zero utilities. Multi-item Diffusion Auctions. Diffusion auctions was also extensively studied in the context of selling multiple homogeneous items. The Generalized Information Diffusion Mechanism (GIDM), the Distance-based Network Auction Mechanism for Multi-unit, and the Unit-demand Buyers (DNA-MU) (Kawasaki et al. 2020) were unsuccessful in guaranteeing IC, thereby rendering the achievement of an IC mechanism a significant challenge. Two IC mechanisms were then proposed: the Layer-based Diffusion Mechanism (LDM) (Liu, Lian, and Zhao 2023) localized compe- tition within layers based on the buyers’ distances from the seller; the Multi-unit Diffusion Auction Mechanism (MU- DAN) (Fang et al. 2023) iteratively allocated items to winners during graph exploration. None of these mechanisms are Shapley fair as they only allow partial buyers to achieve positive utilities. Shapley Value in Auctions. The balanced winner contribution rule (BWC) (Lindsay 2018) was proposed for allocating surplus to winners with modified Shapley value in auctions and exchanges, which is proved to be not incentive compatible. Nested knockout (Graham, Marshall, and Richard 1990) was proposed to frequently distribute collusive gains among members in a bidder coalition in auctions, giving out the expected payments equal the Shapley value in many settings. A Shapley Value based profit allocation scheme (SPA) (Pan et al. 2009) was proposed to distribute the profit among the bidding nodes according to their marginal contributions in the spectrum auction. All these work sought for a payoff distribution that matched the Shapley value on behalf of fairness in traditional settings, which was not compatible with truthful reporting. In our paper, we consider a new trending model of diffusion auctions, and aims at a good approximation of Shapley contribution with the hard constraint of incentive compatibility.

## Preliminaries

Consider an auction that a seller s sells k ≥1 homogeneous items in a social network with n buyers, notated as N. The social network is modeled as a graph G = (V, E), where V = N ∪{s} and E is the edge set, representing the social relationships between agents. We use eij to represent the edge between agent i and j.

Each buyer i ∈N has a private type θi = (vi, ri), where vi is her valuation and ri shows her social relationship. vi(q) denotes agent i’s valuation of q ∈{0, 1,..., k} items, which we restrict to be marginal non-increasing, i.e. vi(q + 1) −vi(q) ≤vi(q) −vi(q −1). We assume that the valuation is normalized, which means v(0) = 0. ri = {j | eij ∈E} denotes buyer i’s direct neighbors in the social network. Specially, the neighbors of the seller rs, called initial buyers, are the only buyers knowing that s is selling the item initially. Let Θi be the type space of buyer i and Θ = (Θ1,..., Θn) be the joint type space of all buyers.

Diffusion auction mechanisms ask each buyer to report not only her valuation but also neighbors, so that the seller can invite more potential buyers to join. Let v′ i denote the reported valuation and r′ i ⊆ri be the actual neighbor set reported by i. We call θ′ i = (v′ i, r′ i) the reported type of i and let θ′

−i represent the reported type profile of all buyers except for buyer i. Let θ′ = (θ′

1, θ′ 2,..., θ′ n) = (θ′ i, θ′

−i) represent the reported type profile of all buyers.

A buyer can join the auction only when she is invited, but to make the model mathematically clean and also make the related definitions more accessible, we assume all buyers in network report to the mechanism (this does not mean that we require this in practice). Given all buyers’ reports θ′, we need to decide who can actually join the auction. We define the feasible set F(θ′) ⊆V as the set of agents connected to

16990

<!-- Page 3 -->

s in the reported network graph G(θ′) = (V, E(θ′)), where E(θ′) = {eij | j ∈r′ i}. The auction can only use the reports from the feasible set to make the decisions. For an infeasible buyer i /∈F(θ′), she actually cannot participate in the auction in practice. Now the definition of a diffusion auction mechanism is formalized as follows. Definition 1. A diffusion auction mechanism M = (π, p) is defined by an allocation and a payment policy (π, p) = {(πi, pi)}i∈N, where πi: Θ →{0, 1,..., k} and pi: Θ → R are the allocation and payment functions for i. For all reported type profile θ′ ∈Θ, it is satisfied that 1. for infeasible buyers i /∈F(θ′), πi(θ′) = 0, pi(θ′) = 0, 2. for feasible buyers i ∈F(θ′), πi(θ′) and pi(θ′) are independent of the reports of the infeasible buyers, and 3. P i∈F (θ′) πi(θ′) ≤k.

We denote the set of all allocations satisfying above constraints given θ′ and k as Π(θ′, k). In this definition, πi(θ′) represents the quantity of the items allocated to i; pi(θ′) indicates the amount i should pay to the seller s and pi(θ′) < 0 means that buyer i can receive |pi(θ′)| from the seller s. Given a reported type profile θ′ and a diffusion auction mechanism M = (π, p), the utility of a buyer i with type θi = (vi, ri) is determined by her allocation and payment:

ui(θi, θ′, (π, p)) = vi(πi(θ′)) −pi(θ′).

Note that for a randomized mechanism, ui is calculated in expectation. In the paper, we will define a randomized mechanism by a probability distribution on deterministic ones.

The social welfare (SW) of an allocation π is

SW(θ′, π) =

X i∈N v′ i(πi).

An allocation is called to be efficient if it maximizes SW:

π∗∈arg maxπ∈Π(θ′,k)SW(θ′, π)

with the corresponding social welfare

SW∗(θ′) = SW(θ′, π∗) = maxπ∈Π(θ′,k)SW(θ′, π).

We consider two key properties for a diffusion auction: Definition 2. A diffusion auction mechanism (π, p) is incentive compatible (IC) if for all buyer i ∈N, all type θi ∈Θi all reports θ′ i ∈Θi and θ′

−i ∈Θ−i, we have ui(θi, (θi, θ′

−i), (π, p)) ≥ui(θi, (θ′ i, θ′

−i), (π, p)).

Definition 3. A diffusion auction mechanism (π, p) is individually rational (IR) if for all buyer i ∈N, all θi ∈Θi, and all θ′

−i ∈Θ−i, we have ui(θi, (θi, θ′

−i), (π, p)) ≥0. Intuitively, IC guarantees that buyers report their valuation truthfully and invite all their neighbors; IR guarantees buyers who report truthfully to get non-negative utilities.

Beyond the previous studies, we aim to propose a diffusion mechanism where the payment is determined fairly according to the buyers’ contribution to the social welfare. To evaluate this, we formalize the definition of fairness property following the Shapley value, which is a classic solution to share value ‘fairly’ among players in cooperative games (Shapley et al. 1953). We use each participant’s Shapley contribution for generating social welfare in the network as a reference for utility distribution in a diffusion auction.

Denote B ⊆V as a coalition of agents. Let SW∗(θ′, B) be the maximum social welfare can be achieved by coalition B, which is the social welfare of the efficient allocation only among the feasible buyers in B who are connected to the seller via B only. Specially, if the seller s is not in B, then no buyers are feasible within B and the social welfare can be achieved in B is always zero. Definition 4. For any coalition B ⊆V, the feasible set of B, denoted as F(θ′, B), is the set of buyers connected to the seller via B only (specifically, F(θ′, B) = ∅if s /∈B). Correspondingly, the maximum social welfare within B is

SW∗(θ′, B) = max π∈Π(θ′,k) and πi/ ∈F (θ′,B)=0 SW(θ′, π)

Let O(V) be the set of all permutations of V, and o ∈ O(V) denote an order. Let i ≺o j denote that i precedes j in o. In order o, o≺i = {j | j ≺o i} represents the set of agents preceding i, and o⪯i = o≺i ∪{i}. Then, the marginal social welfare increase of i in order o is

MCo i (θ′) = SW∗(θ′, o⪯i) −SW∗(θ′, o≺i).

Then, the Shapley contribution of an agent is determined as her averaged marginal social welfare increase on all permutations of V. Definition 5. The Shapley contribution of agent i ∈V in a diffusion auction is defined as:

ϕi(θ′) = 1 |O(V)|

X o∈O(V)

MCo i (θ′) =

X

B⊆V \{i}

|B|!(|V \ B| −1)!

|V |! [SW∗(θ′, B ∪{i}) −SW∗(θ′, B)].

We now define our new property ϵ-Shapley fair (ϵ-SF) by comparing buyers’ utilities with their Shapley contributions. Definition 6. A diffusion auction mechanism M = (π, p) is ϵ-Shapley fair (ϵ-SF), ϵ ∈(0, 1], if for all buyer i ∈N, for all type θi ∈Θi, all other reports θ′

−i ∈Θ−i, we have ϵ · ϕi((θi, θ′

−i)) ≤ui(θi, (θi, θ′

−i), (π, p)) ≤ϕi((θi, θ′

−i)).

ϵ-SF requires the utilities of all buyers that report truthfully are at least ϵ times of their Shapley contributions and should not exceed their Shapley contributions. Specially, if ϵ = 1, then a buyer’s utility is equal to her Shapley contribution. A mechanism is not SF, if such ϵ does not exist. Remark. None of existing diffusion auction mechanisms are Shapley fair. It can be showed via a network example shown in Figure 1. For single-item mechanisms, IDM (Li et al. 2017), CDM (Li et al. 2019), and SCM (Chen et al. 2023) only allow the red buyers (the cut-points from seller s to the buyer who reports the highest value) to have positive utilities; CWM (Zhang, Zheng, and Zhao 2024) only allows buyer H (the winner) to have positive utility; FDM (Zhang, Zhao, and Zhang 2020) and SRA (Liu, Zhang, and Zhao 2023) allow the red and blue buyers (buyers on some simple paths from seller s to the buyer who reports the highest

16991

<!-- Page 4 -->

**Figure 1.** A network example of diffusion auctions. A single item is sold in this network. Each node represents one participant with her valuation in the circle (s is the seller). The edges show the social relationships among them.

value) to have positive (expected) utilities. We can observe that buyers A, C, and E always get 0 utilities in all these mechanisms. However, the Shapley contributions of all buyers except for J in this example are positive. Hence, they are not Shapley fair. For multi-item mechanisms, VCG (Vickrey 1961; Clarke 1971; Groves 1973) for all multi-item settings, and GIDM (Zhao et al. 2018), DNA-MU (Kawasaki et al. 2020), LDM (Liu, Lian, and Zhao 2023), MUDAN (Fang et al. 2023) for homogeneous multi-item setting, are all not Shapley fair. Among multi-item mechanisms, VCG (Vickrey 1961; Clarke 1971; Groves 1973) and GIDM (Zhao et al. 2018) allow only the cut-points from seller s to winners to have positive utilities; LDM (Liu, Lian, and Zhao 2023) allows only the first 3 layers of buyers to potentially receive positive utilities; MUDAN (Fang et al. 2023) and DNA- MU (Kawasaki et al. 2020) only benefit the winners. Therefore, all of them are not Shapley fair.

Permutation Diffusion Auction In this section, we propose a diffusion auction mechanism called Permutation Diffusion Auction (PDA), and show that it achieves 1 k+1-SF, together with IC and IR.

The Definition of PDA The main idea of PDA is first randomly select an order from O(V), and then traverse all agents to check their marginal social welfare increase. The process of the traverse is described informally as follows (and formally in Algorithm 1).

• If the current traversed agent i is the seller or she cannot be feasible by only traversed agents, we just skip her; • If the current traversed buyer i can be feasible by only traversed agents, we calculating an efficient allocation for remaining unsold item (if any) within these agents. If the allocation suggests that i will be allocated with several items, then i will receive these items and pay the loss of social welfare of the coalition before i because of her winning items. If the allocation does not suggest that i could be the winner of some items, we do not perform any allocation in this step, but we will reward buyer i with her marginal social welfare increase. One key point of the above process is that we decide each buyer’s allocation and payment when she is traversed instantly, and will never change it in the future. That is to

## Algorithm

1: Permutation Diffusion Auction (PDA)

Input: k, θ′

Output: π, p

1: Initialize {πi}i∈N = 0N and {pi}i∈N = 0N. 2: Select one order o from O(V) uniformly. 3: for each i in o and i̸ = s do 4: πi ←π∗ i (θ′, o⪯i, πo≺i) 5: pi ←SW∗(θ′, o≺i, πo≺i) −SW∗(θ′, o⪯i, πo≺i) + v′ i(πi) 6: if all items are allocated then break 7: end for say, we should keep the allocation of sold items when selling the remaining items to a newly traversed buyer, and each buyer’s allocation is affected by earlier traversed buyers’ allocations. More precisely, denote πo≺i as the allocation right before i in order o. When i is traversed, we denote the efficient allocation with the irrevocable πo≺i as π∗(θ′, o⪯i, πo≺i) and the corresponding maximized social welfare as SW∗(θ′, o⪯i, πo≺i). They can be decided by the following optimization problem.

maximize π SW(θ′, π)

s.t. π ∈Π(θ′, k), πi/∈F (θ′,o⪯i) = 0, πj ≥πo≺i j, ∀j ∈o≺i.

Then, in PDA, we use π∗(θ′, o⪯i, πo≺i) to define the allocation of buyer i, i.e., πi = π∗(θ′, o⪯i, πo≺i). Notice that we will not update the allocation πo≺i for those who has been traversed before i. The payment for buyer i is the difference of the maximized social welfare for buyers before i in o within the constraints of πo≺i and their welfare in π∗(θ′, o⪯i, πo≺i). For the former one, to be convenient, we use a similar notation SW∗(θ′, o≺i, πo≺i) to represent the maximized social welfare can be achieved by buyers in o≺i, without decreasing anyone’s allocated item in πo≺i. For the latter one, it just equals to SW∗(θ′, o⪯i, πo≺i) −v′ i(πi). Finally, the formal description for the process of PDA is given in Algorithm 1.

We note that PDA could be performed in polynomial time because: 1) we only traverse one randomly selected order so that the number of total steps is at most n + 1; 2) the efficient allocation in each step can be computed by a polynomial greedy method since the items are homogeneous with diminishing marginal valuations. Example 1. We show a running example of PDA that a seller sells a single item in the network shown as Figure 2. In Figure 2(a) and Figure 2(b), assume that agents C, I, B, s, F, J, and D have been traversed sequentially. Under this scenario, the item is not allocated among these buyers, and the current feasible set is comprised of s, B, D, and F, with an associated maximum social welfare of 5.

Now, if the next traversed agent is buyer G as shown in Figure 2(a), then she wins the item as her reported valuation v′

G is the highest among all feasible buyers, and her

16992

![Figure extracted from page 4](2026-AAAI-fair-diffusion-auctions/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

**Figure 2.** An example of PDA. (a)&(b) The dashed nodes represent buyers who have not joined yet, the blue nodes signify buyers who have joined but are not feasible, and the red nodes indicate feasible participants. Specifically, the triangles mark the newly joined buyers, and the filled nodes represent those who have become feasible due to the entry of the new buyers. (c) The expected utility in PDA (red) and the Shapley contribution (blue) of buyers.

payment equals 5−7+7 = 5, namely her reported valuation of the item minus her marginal contribution on the maximum social welfare. The remaining buyers that have not been traversed will all get nothing.

If the next traversed agent is buyer H as shown in Figure 2(b), then she will make H, I, and J feasible. The maximum social welfare will rise to 10 and H will be rewarded by her marginal contribution 10 −5 = 5. After H, none of G, A, and E will win the item because the maximum social welfare keeps 10, which is higher than their reported valuations. They will all get 0 payments as their marginal contributions are 0. We can notice that in this case, the auction ends without allocating the item to any buyers.

Finally, Since PDA is a randomized mechanism, we consider its expected utility distribution. Figure 2(c) reveals that the distribution of expected utilities of all buyers in PDA are highly close to their Shapley contributions.

IC and IR Analysis

Firstly, we show that PDA satisfies the property of IR and IC.

Theorem 1. PDA is individually rational and incentive compatible.

Proof. IR. Whichever order selected by PDA, the utility of buyer i with any order o ∈O(V) will be uo i (θi, θ′) = vi(πi) −pi = vi(πi)

−SW∗(θ′, o≺i, πo≺i) + SW∗(θ′, o⪯i, πo≺i) −v′ i(πi)

(θ′ i=θi) = SW∗(θ′, o⪯i, πo≺i) −SW∗(θ′, o≺i, πo≺i) ≥0.

Because the maximum social welfare can be achieved is monotone non-decreasing with the enlarging of the set of buyers, we have SW∗(θ′, o⪯i, πo≺i) ≥SW∗(θ′, o≺i, πo≺i); thus the last inequality holds. Then, uo i (θi, (θi, θ′

−i))) ≥0 for any sampled o. Therefore, PDA is IR. IC. Whichever order o ∈O(V) selected, for all buyer i, all type θi ∈Θi, all reports θ′ i ∈Θi and θ′

−i ∈Θ−i, we denote πo i (·) and uo i (·) as i’s allocation and utility function within o, separately.

As for any buyer i ∈N, πo i (θ′) = π∗ i (θ′, o⪯i, πo≺i), which maximizes the social welfare when traversing at i,

SW∗((θi, θ′

−i), o⪯i, πo≺i) ≥SW∗((θ′ i, θ′

−i), o⪯i, πo≺i)

−v′ i(πo i ((θ′ i, θ′

−i))) + vi(πo i ((θ′ i, θ′

−i)), where the right-hand side means the social welfare achieved in (θi, θ′

−i) with the allocation under (θ′ i, θ′

−i). On the other hand, since i /∈o≺i, then by definition, it has SW∗((θi, θ′

−i), o≺i, πo≺i) = SW∗((θ′ i, θ′

−i), o≺i, πo≺i) so that PDA is IC by following inequality:

uo i (θi, (θi, θ′

−i))

= SW∗((θi, θ′

−i), o⪯i, πo≺i) −SW∗((θi, θ′

−i), o≺i, πo≺i)

≥SW∗((θ′ i, θ′

−i), o⪯i, πo≺i) −v′ i(πo i ((θ′ i, θ′

−i)))

+ vi(πo i ((θ′ i, θ′

−i)) −SW∗((θ′ i, θ′

−i), o≺i, πo≺i)

= uo i (θi, (θ′ i, θ′

−i)).

Fairness Analysis Now we will analyze the fairness can be achieved by PDA. We show the lower bound of the approximation ratio for Shapley-fairness in the following theorem. Theorem 2. PDA is 1 k+1-Shapley fair for selling k items.

Before proving the theorem, first notice that the Shapley contribution of a player is the expected marginal social welfare increase without any constraints on previous allocation. It is equivalent to keep a zero allocation 0N as the constraint, so that the Shapley contribution can also be written as:

ϕi(θ′) =

X

B⊆V \{i}

|B|!(|V | −|B| −1)!

|V |!

·

SW∗(θ′, B ∪{i}, 0N) −SW∗(θ′, B, 0N)

.

Now we prove Theorem 2 through two propositions: we first show that ϵ is associated to the lower bound of ratio that all items are unsold, and then show that this ratio is not

16993

![Figure extracted from page 5](2026-AAAI-fair-diffusion-auctions/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-fair-diffusion-auctions/page-005-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

less than 1 k+1. In the proof, we denote µ(θ′) as the rate that no items are sold in PDA for reported type profile θ′, and denote θ′

B as the induced reported type profile that sets all agents’ reports who are not in coalition B as nil.

Proposition 1. When a buyer reports her true type, the lower bound of the ratio between her expected utility in PDA and her Shapley contribution is no less than the lower bound of rate that all items are unsold, and no greater than one.

Proposition 2. The lower bound of the ratio that all items are unsold of PDA is 1 k+1 for selling k items.

Proof of Proposition 1. For ∀o ∈O(V), ∀i ∈N, given θ′ = (θi, θ′

−i), i’s marginal social welfare increase is affected by πo≺i, the allocations of buyers preceding i. When no items are sold in o≺i (with probability µ(θ′ o≺i)), i.e., πo≺i is a zero vector, i will get SW∗(θ′, o⪯i, 0N) − SW∗(θ′, o≺i, 0N) as her utility; if some items have already been sold before traversing to i, then i’s utility is at least 0 by IR. Hence, for the expected utility of buyer i, we have

EPDA(ui) ≥

X

B⊆V \{i}

|B|!(|V | −|B| −1)!

|V |! µ(θ′

B)

·

SW∗(θ′, B ∪{i}, 0N) −SW∗(θ′, B, 0N)

.

Compared to the formula of the Shapley contribution, inf θ′

B∈Θ µ(θ′

B) · ϕi ≤EPDA(ui) ≤ϕi.

Therefore, a lower bound of the ratio between an arbitrary buyer’s expected utility in PDA and her Shapley contribution is infθ′

B∈Θ µ(θ′

B), which is exactly the lower bound of the rate that all items are unsold.

Proof of Proposition 2. If n ≤k, then the ratio that all items are unsold is at least 1 n+1 ≥ 1 k+1 (for the cases where s herself is the last agent in the order).

If n > k, let M be the set of buyers who reports the k highest valuations, which must satisfy |M| ≤k. Then, we can first observe that if no item is sold when buyers in M all become feasible in the loops of PDA, then all items are remain unsold after PDA terminates.

Considering a group of orders where buyers in M all become feasible at the same time when we traverse at s, then no items can be sold. By changing the order of the seller s and buyers in M while keeping the order of all other buyers, we can get another group of orders where at least one buyer in M is feasible as long as we traverse at her, and hence at least one item must be sold (to the buyer would be traversed at last among M or some other buyer who has been traversed before her) in these orders. The number of the orders in the latter group is |M| times that in the previous group. Denote the probability of selecting these two groups of orders as a; then the conditioned ratio that all items are unsold among these orders is 1 |M|+1 ≥ 1 k+1. We then check the orders that not being included above, notated as O∗, which totally has a probability of (1 −a) to appear. In an arbitrary order o ∈O∗, let x(o) be the one who brings the last buyer among M to be feasible, i.e. M ⊆F(θ′, o⪯x(o)) but M ⊈F(θ′, o≺x(o)). We also have {s} ∪M ⊆o≺x(o). As the maximum social welfare reaches the peak as SW∗(θ′, o⪯x(o), πo≺x(o)) when traversing to x(o), x(o) and buyers after x(o) cannot win any items. Hence, whether items are sold in o only depends on o≺x(o). Notice that M ⊈F(θ′, o≺x(o)), so for any order o′ where only the order of o≺x(o) is shuffled in o, we have o′ ∈O∗. Namely, the set {o′ | x(o′) = x(o), o′

≺x(o′) = o≺x(o)} ⊆ O∗and we can use o as the representative element to denote the set. Then, O∗can be partitioned by a series of representative orders o1, o2,..., ol, where l is the number of different representative orders. For each representative order o, let ρ(o) be the probability that selects an order belongs to the set represented by o in O∗.

Then taking all parts together, the total probability of all items are unsold is, µ(θ′) ≥a · 1 k + 1 + (1 −a) ·

X o∈{o1,o2,...,ol}

ρ(o)µ(θ′ o≺x(o)).

Notice that if for any o ∈{o1, o2,..., ol}, we can have µ(θ′ o≺x(o)) ≥1/(k + 1), and then µ(θ′) ≥a/(k + 1) + (1 −a)/(k + 1) = 1/(k + 1).

To show that it is true, we can recursively analyze arbitrary o≺x(o) as above and stop with the following conditions:

1. The buyers reports the k highest valuation among feasible buyers in o≺x(o) are all initial buyers, then a = 1, and hence µ(θ′ o≺x(o)) ≥1/(k + 1); 2. There are less than or equal to k feasible buyers in o≺x(o) (i.e. |F(θ′, o≺x(o) \ {s}| ≤k), then µ(θ′ o≺x(o)) ≥1/(|F(θ′, o≺x(o)) \ {s}| + 1)

= 1/|F(θ′, o≺x(o))| ≥1/(k + 1).

Therefore, µ(θ′ o≺x(o)) ≥1/(k + 1) for arbitrary o≺x(o), indicating that µ(θ′) ≥1/(k + 1).

Finally, Theorem 2 can be proved through Proposition 1 and Proposition 2. We would also like to point out that the bound is consequently tight when k = 1 (shown through a simple example in Figure 3), while the tightness of the bound when k ≥2 remains an open problem.

Extension to Combinatorial Auctions In this section, we demonstrate that PDA can be extended into a combinatorial setting as Combinatorial PDA (CPDA).

Consider the setting that a seller s sells k items K = {1, 2, · · ·, k} via a social network. Indicator vector q ∈ {0, 1}k denotes a bundle of items, where qj represents whether item j is in the bundle q. In particular, q = 0 means the empty bundle, and q = 1 means the bundle of all items. Each buyer i ∈N has a private valuation function vi(q) for any bundle q, and we assume vi(0) = 0. Now, for a given

16994

<!-- Page 7 -->

**Figure 3.** An example of PDA that shows 1

2 is a tight bound when selling a single item. The graph illustrates a singlechain network containing s, A, B; the table shows the utility and marginal contribution of A and B under different choices of orders, as well as their expected utilities and Shapley contribution. We can find that the expected utility is half of her Shapley contribution for buyer B.

reported type profile θ′, πi(θ′) is an indicator vector that represents the bundle of items that allocated to buyer i.

Similar to the homogeneous multi-item setting, we need to maintain the allocation of sold items when selling the remaining items. We consider the irrevocable πo≺i when maximizing the social welfare in the procedure of CPDA. When traversing to i, the efficient allocation π∗(θ′, B, πo≺i) can be solved as following maximize π SW(θ′, π)

s.t. π ∈Π(θ′, K), πi/∈F (θ′,B) = 0, πjl ≥πo≺i jl, ∀j ∈o≺i, ∀l ∈K.

Let SW∗(θ′, B, πo≺i) be the corresponding social welfare. Then, CPDA follows the same procedure of PDA with a generalized form of π. We present CPDA formally in Algorithm 2. Theorem 3. CPDA is IR, IC and 1 n-Shapley fair. The proof procedure of IR and IC for CPDA is the same as that for PDA, so the full proof is omitted.

For Shapley-fairness of CPDA, we know that it is bounded by the ratio that no items are sold before an arbitrary agent joins according to Proposition 1. Given θ′, ∀o ∈O(V), ∀i ∈N, µ(θ′o≺i) ≥1 n because o≺i ⊆V \ {i}

## Algorithm

2: Combinatorial PDA (CPDA)

Input: K, θ′

Output: π, p

1: Initialize all πi = 0, pi = 0; uniformly select o ∈O(V). 2: for i in o and i̸ = s do 3: πi ←π∗ i (θ′, o⪯i, πo≺i) 4: pi ←SW∗(θ′, o≺i, πo≺i)−SW∗(θ′, o⪯i, πo≺i)+v′ i(πi) 5: if all items are allocated then break 6: end for contains at most n agents, and no items would be sold when the seller s is the last to participate in o≺i. The fairness of CPDA is superior to the classic VCG (Vickrey 1961; Clarke 1971; Groves 1973), which is not Shapley fair. Specially, since PDA is a special case of CPDA, then it is also 1 n-SF, which gives a tighter bound than 1 k+1 when n ≤k.

## Discussion

This paper designs a diffusion auction that fairly rewards participants to better motivate their involvement. To do so, our solution sacrifices some seller revenue, potentially causing deficits when items remain unallocated. Concretely, with an order o, the revenue of the seller Revo(θ′) is equal to

SW(θ′, πo) −SW(θ′, π∗(θ′, V, πo))

+ SW∗(θ′, o⪯s), and then the expected revenue of PDA EPDA is:

ϕs(θ′) − 1 |O(V)|

X o∈O(V)

[SW(θ′, π∗(θ′, V, πo)) −SW(θ′, πo)].

Intuitively, the expected revenue of PDA equals to the seller’s Shapley contribution minus the expected loss of social welfare due to the unsold items. The deficit does limit the applicability of PDA if the market’s goal is for profit. However, if the goal is getting more people to know the auction, then the deficit could be a kind of advertisement cost.

Unfortunately, the deficit issue appears unavoidable. In a 1-SF mechanism, participants’ utilities equal their Shapley contributions, summing to the maximal social welfare. Avoiding a seller deficit requires efficient allocation, but efficiency conflicts with IC and non-deficit (Li et al. 2022, Theorem 2). Thus, 1-SF is incompatible with these conditions.

**Figure 4.** highlights a trade-off between revenue and allocation efficiency. The revenue upper bound for an ϵ-SF mechanism, ϵ · ϕs + (1 −ϵ) · SW∗(θ′), decreases with ϵ, meaning stronger Shapley fairness reduces revenue. An open question remains if non-deficit is a strict constraint:

Whether there exists a Shapley fair diffusion auction that is IC, IR, and non-deficit?

**Figure 4.** The relationship between expected revenue and the allocation efficiency of Shapley fair diffusion auction mechanisms. The horizontal axis represents the efficiency of allocations and the vertical axis represents the expected revenue. The red parallelogram shows the space of ϵ-Shapley fair mechanisms. Specially, for 1-Shapley fair mechanisms, the space is an inclined line segment at the bottom.

16995

![Figure extracted from page 7](2026-AAAI-fair-diffusion-auctions/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fair-diffusion-auctions/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was supported by the Science and Technology Commission of Shanghai Municipality (No. 23010503000), the Shanghai Frontiers Science Center of Human-centered Artificial Intelligence (ShangHAI), and JST ERATO (Grant Number JPMJER2301).

## References

Chen, H.; Deng, X.; Wang, Y.; Wu, Y.; and Zhao, D. 2023. Sybil-Proof Diffusion Auction in Social Networks. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems, 1379–1387. Clarke, E. H. 1971. Multipart pricing of public goods. Public choice, 17–33. Fang, Y.; Zhang, M.; Liu, J.; Khoussainov, B.; and Xiao, M. 2023. Multi-unit auction over a social network. In ECAI 2023, 676–683. IOS Press. Graham, D. A.; Marshall, R. C.; and Richard, J.-F. 1990. Differential payments within a bidder coalition and the Shapley value. The American Economic Review, 493–510. Groves, T. 1973. Incentives in teams. Econometrica: Journal of the Econometric Society, 617–631. Guo, Y.; and Hao, D. 2021. Emerging Methods of Auction Design in Social Networks. In Zhou, Z.-H., ed., Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI-21, 4434–4441. International Joint Conferences on Artificial Intelligence Organization. Kawasaki, T.; Barrot, N.; Takanashi, S.; Todo, T.; and Yokoo, M. 2020. Strategy-proof and non-wasteful multi-unit auction via social network. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 34, 2062–2069. Li, B.; Hao, D.; Gao, H.; and Zhao, D. 2022. Diffusion auction design. Artificial Intelligence, 303: 103631. Li, B.; Hao, D.; Zhao, D.; and Yokoo, M. 2019. Diffusion and Auction on Graphs. In Proceedings of the Twenty- Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, 435–441. Li, B.; Hao, D.; Zhao, D.; and Zhou, T. 2017. Mechanism Design in Social Networks. In Proceedings of the Thirty- First AAAI Conference on Artificial Intelligence, 586–592. AAAI Press. Lindsay, L. 2018. Shapley value based pricing for auctions and exchanges. Games and Economic Behavior, 108: 170– 181. Liu, H.; Lian, X.; and Zhao, D. 2023. Diffusion multi-unit auctions with diminishing marginal utility buyers. In ECAI 2023, 1505–1512. IOS Press. Liu, H.; Zhang, Y.; and Zhao, D. 2023. Distributed Mechanism Design in Social Networks. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems, 1826–1834. Pan, M.; Chen, F.; Yin, X.; and Fang, Y. 2009. Fair profit allocation in the spectrum auction using the shapley value. In GLOBECOM 2009-2009 IEEE Global Telecommunications Conference, 1–6. IEEE.

Roth, A. E. 1988. Introduction to the Shapley value. The Shapley value, 1–27. Shapley, L. S.; et al. 1953. A value for n-person games. Vickrey, W. 1961. Counterspeculation, auctions, and competitive sealed tenders. The Journal of finance, 16(1): 8–37. Young, H. P. 1985. Monotonic solutions of cooperative games. International Journal of Game Theory, 14(2): 65– 72. Zhang, W.; Zhao, D.; and Zhang, Y. 2020. Incentivize diffusion with fair rewards. In ECAI 2020, 251–258. IOS Press. Zhang, Y.; Zheng, S.; and Zhao, D. 2024. Optimal Diffusion Auctions. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems, 2600– 2602. Zhao, D. 2022. Mechanism design powered by social interactions: a call to arms. In Proceedings of the Thirty- First International Joint Conference on Artificial Intelligence, IJCAI-22, 5831–5835. Zhao, D.; Li, B.; Xu, J.; Hao, D.; and Jennings, N. R. 2018. Selling Multiple Items via Social Networks. In Proceedings of the 17th International Conference on Autonomous Agents and MultiAgent Systems, 68–76.

16996
