---
title: "Formal Verification of Diffusion Auctions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38983
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38983/42945
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Formal Verification of Diffusion Auctions

<!-- Page 1 -->

Formal Verification of Diffusion Auctions

Rustam Galimullin1, Munyque Mittelmann2, Laurent Perrussel3

1University of Bergen, Norway 2CNRS, LIPN, Universit´e Sorbonne Paris Nord, France 3IRIT, Universit´e Toulouse Capitole, France rustam.galimullin@uib.no, mittelmann@lipn.univ-paris13.fr, laurent.perrussel@irit.fr

## Abstract

In diffusion auctions, sellers can leverage an underlying social network to broaden participation, thereby increasing their potential revenue. Specifically, sellers can incentivise participants in their auction to diffuse information about the auction through the network. While numerous variants of such auctions have been recently studied in the literature, the formal verification and strategic reasoning perspectives have not been investigated yet. Our contribution is threefold. First, we introduce a logical formalism that captures the dynamics of diffusion and its strategic dimension. Second, for such a logic, we provide modelchecking procedures that allow one to verify properties like the Nash equilibrium, and that pave the way towards checking the existence of sellers’ strategies. Third, we establish computational complexity results for the presented algorithms.

## Introduction

In auction theory and mechanism design (Nisan et al. 2007), the set of participants is typically fixed and socially independent, in the sense that any underlying social network among agents is not taken into account. In contrast, by leveraging agents’ social networks, a seller could use buyers’ connections to promote the auction (Guo and Hao 2021). This has a clear advantage: a larger market may include participants with higher valuations, leading to a potential increase in social welfare or the sellers’ revenue. On the other hand, buyers act as competitors and have no incentives to invite more participants, as doing so would increase competition and reduce their likelihood of securing the item being auctioned.

The challenge of encouraging participants to propagate the auction among their social connections has recently sparked interest in the mechanism design community (Zhao 2021). In particular, it led to the introduction of diffusion auctions (Zhao et al. 2018; Li et al. 2022), where sellers propose incentives to buyers so that they can benefit from inviting their neighbours. The intuition is that the mechanism guarantees that the buyer’s new utility after propagating the auction is not less than her utility of participating in the auction with the original participants. Their main benefit is the increase in the number of participants while guaranteeing economic properties such as incentive-compatibility

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

or optimality (Zhang, Zheng, and Zhao 2024). Yet, two critical aspects remain unexplored — the strategic behaviour of sellers in diffusion auctions, especially when multiple sellers compete to reach the most valuable buyers, and the formal verification of such mechanisms.

In the last decades, a number of logics have been proposed to reason about agents’ strategic capabilities with prime examples being Coalition Logic (CL) (Pauly 2002), Alternating-time Temporal Logic (ATL) (Alur, Henzinger, and Kupferman 2002), and Strategy Logic (Mogavero et al. 2014). Combined with model-checking techniques (Clarke et al. 2018), these frameworks provide powerful tools for specification and verification of multi-agent systems, with applications to several problems, from the analysis of voting protocols (Belardinelli et al. 2021; Jamroga, Kurpiewski, and Malvone 2022) to the verification of auctions and mechanism design (Mittelmann et al. 2025, 2023).

In this paper, we provide a formal framework for specification and verification of strategic properties in diffusion auctions. In doing so, we combine the intuitions from social network logics (Pedersen 2024), dynamic epistemic logic (DEL) (van Ditmarsch, van der Hoek, and Kooi 2008), as well as the aforementioned CL and ATL. We believe that this is the first logic-based approach to formal verification of diffusion auctions and strategic abilities of sellers in them.

Contribution We introduce the n-seller logic for diffusion incentives Ln and its strategic variant SLn. These logics are interpreted on diffusion auction mechanism models that are quite general and thus capture a wide variety of mechanisms. Both Ln and SLn allow us to capture the dynamics of diffusion of information about auctions and their strategic dimension. By ‘dynamics’ here, we mean the change of the underlying social network as a result of sellers proposing incentives to buyers to invite their neighbours to an auction. For these logics, we provide model-checking procedures that allow one to verify properties such as Nash equilibrium, and that pave the way towards checking the existence of sellers’ strategies. For the presented algorithms, we establish computational complexity results.

Diffusion Auctions With Multiple Sellers

We start by presenting a formal framework for multipleseller auctions, where each seller is selling (a copy of) the

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19099

<!-- Page 2 -->

same item. Sellers and buyers in such a setting are connected via an underlying social network, whose structure the sellers can try to exploit by incentivising their direct neighbours (i.e., buyers participating in the sellers’ auctions) to invite all their friends to join the corresponding auction.

Let S = {σ1, σ2,..., σn} be a finite non-empty set of n names of sellers, and B = {β1, β2,...} be a countable set of names of buyers, such that S∩B = ∅. Also, let Nom = S∪B denote the total set of agent names, or nominals. We will also write B• = B ∪{•} and Nom• = Nom ∪{•}, where nominal • intuitively stands for ‘the current agent’. Finally, let Terms = {utα | α ∈Nom•} be a set of terms denoting utilities of agents utα and a term ut• denoting the utility of the current agent. Definition 1. The language Ln of the n-seller logic for diffusion incentives is defined by the following grammar:

φ:= α | (z1t1 +... + zmtm) ⩾z | ¬φ | (φ ∧φ) | □φ | [σ1: β1,..., σn: βn]φ | ♡γ, where α ∈Nom, z ∈Z, ti ∈Terms, σi, σj ∈S with σi̸ = σj, βi ∈B•, and γ ∈Nom•. Here, □φ means ‘all friends of the current agent satisfy φ’, and ♡γ means that agent named γ, which can be either a seller or a buyer, gets an item in the current configuration of a mechanism.

Constructs [σ1: β1, σ2: β2,..., σn: βn]φ (abbreviated as [σ: β]φ), where n = |S|, capture the concurrent information diffusion about auctions. This is done by sellers σi incentivising the respective buyers βi, i.e., paying them some sum, to invite all their friends to join the seller’s auction. Clause σi: • denotes the case in which seller σi does not incentivise anyone, i.e., she does nothing or skips her turn. Hence, we will write, e.g., [σ1: β1, σ2: β2]φ if only sellers named σ1 and σ2 do not choose •. Given [σ: β]φ, we will denote as σ\• the set of agents σi ∈σ such that the corresponding βi̸ = •. Observe that even though this modality is concurrent, i.e., everyone is making moves in parallel, we can easily model consecutive moves by selecting • for all the agents who are not playing in the current turn. For the case of 1-seller auctions L1, we will write [β]φ instead of [σ: β]φ. Finally, having a sequence Upd = σ1: β1,..., σn: βn, we will denote by Upd(σi) the corresponding buyer’s name βi.

Duals are defined as ♢φ:= ¬□¬φ and ⟨σ: β⟩φ:= ¬[σ: β]¬φ. For the linear inequalities1, we can use the following abbreviations: t1 −t2 ⩾z for t1 + (−1)t2 ⩾z, t1 ⩾t2 for t1 −t2 ⩾0, t1 ⩽z for −t1 ⩾−z, t1 < z for ¬(t1 ⩾z), and t1 = z for (t1 ⩾z) ∧(t1 ⩽z). We can also use rational numbers in our formulas via abbreviations (e.g., t ⩾1

2 is an abbreviation for 2t ⩾1). All other standard abbreviations of logic and the rules for removing parentheses hold. Example 1. With our language, we can express various desirable properties of mechanisms, both static and dynamic. The following formulas are examples for L1.

1Originally, these linear inequalities in a logical context were used to capture reasoning about probabilities (Fagin, Halpern, and Megiddo 1990). Recently, they were also used to express budgets and costs in dynamic epistemic logic (Dolgorukov, Galimullin, and Gladyshev 2024). We follow the latter approach in this work.

• utα = 3 ∧[α](utα > 3) for ‘the utility of agent α is 3, and after she was incentivised by the seller to invite her friends to participate in the auction, her utility increased’. • ut• = 5 ∧□(ut• ⩾5) ∧♢(α ∧♡α) for ‘the utility of the current agent is 5, and all her friends have utilities of at least 5, and she also has a friend α who gets an item’. Formulas of Ln are interpreted on diffusion auction mechanisms. Definition 2. A market network with n sellers M is a tuple (Agt, F, Bdg, V, I, N), where

• Agt = B ∪S is the set of agents, where B = {a, b, c,...} is a non-empty set of buyers, and S = {s1,..., sn} is a non-empty set of sellers, and B ∩S = ∅; • F: Agt →2B is a symmetric irreflexive friendship (neighbour) relation; • Bdg: Agt →Q+ ∪{0} is a non-negative budget for each agent; • V: B →Q+ ∪{0} s.t. V (a) ⩽Bdg(a) assigns to each buyer a non-negative valuation of the item being sold; • I: B × S →Q+ ∪{0} assigns to each buyer the nonnegative incentive that each seller is willing to pay to them to invite their friends; • N = NS ∪NB is a naming function, where NS: S →S and NB: B →B are surjective functions2. An n-seller diffusion auction mechanism (n-DAM, or DAM) M is a tuple (M, P, Pay, U), where

• M = (Agt, F, Bdg, V, I, N) is a market network with n sellers; • PM: Agt →{0, 1} is the allocation (placement) function, which specifies whether an agent receives an item in an auction conducted within the market network M; • PayM: B →Q+ ∪{0} is the payment function, which specifies the value each buyer should pay in an auction run within the market network M; • UM: Agt →Q+ ∪{0} is the utility function. We omit subscripts M whenever it does not cause confusion. We write M, a to refer to a specific agent a in M.

Observe that the definitions of the allocation, payment, and utility functions do not specify their exact details. This makes our definition of diffusion auction mechanisms general, allowing us to incorporate various types of mechanisms. The only restriction we put on the functions is that their complexity is no greater than the complexity of the model-checking problem of a given logic. As we will see later, model checking Ln is in P, and thus in this section we assume that P, Pay, and U are computable in polynomial time. While the optimal allocation function in combinatorial auctions is NP-complete (Nisan et al. 2007)3, several mechanisms whose functions are computable in polynomial time have been proposed. Those include a strategyproof combinatorial auction (Dobzinski and Vondr´ak 2012), a double auction mechanism in social networks (Xu and He 2020), and McAfee’s double auction mechanism (McAfee 1992).

2Observe that function N is well-defined since S ∩B = ∅. 3The optimal allocation function is used to compute allocations and payments in the Vickrey–Clarke–Groves mechanism (Vickrey 1961; Clarke 1971; Groves 1973).

19100

<!-- Page 3 -->

For our running examples, we will use the single item, multiple units, first price (SMF) auctions.

Definition 3 (SMF Auction). Given a market network with n sellers M = (Agt, F, Bdg, V, I, N), the placement function P is defined as follows.

For a seller si, let si be the ordered set of valuations V (a) of buyers a such that a ∈F(si)4. The ordering is from the highest to the lowest valuations, where the ties are broken by the lexicographic ordering of the buyers. This set is totally ordered. We denote the first element of si as si(1).

We refine the sets si to account for the distribution of items. A refinement of a totally ordered set si, denoted by si, is defined as si = si \ {sj(1)|0 < j < i}. Intuitively, a refinement is the set of bidders in the current auction minus those bidders that are already getting the item from some other auction. Finally, for all si ∈S, if si is non-empty, then P(a) = 1 and P(si) = 0 for V (a) = si(1), and P(si) = 1 otherwise. Observe that in SMF auctions, it is implied that buyers strive to acquire only one (copy of the) item, and hence some sellers may end up not selling their items.

As for the Pay function, buyers, if they get an item, pay the amount equal to their valuation of the item. Function U is defined as follows: for a buyer a ∈B, U(a) = Bdg(a) − V (a) · P(a); for the seller si, U(si) = V (a) + Bdg(si), where V (a) = si(1), and U(si) = Bdg(si) if si is empty.

Example 2. As an example of how the placement function works in Definition 3, consider two mechanisms in Figure 1. In both mechanisms, all valuations and incentive values are identical. Moreover, ♡denotes the allocation of items.

s1 b1: ♡ s2 b2: ♡ s1 b: ♡ s2: ♡

**Figure 1.** Mechanisms M1 (left) and M2 (right).

In M1 we have that both buyers participate in both auctions run by s1 and s2, and each buyer wins an item. For the sellers, sets s1 and s2 are {V (b1), V (b2)}. Recall that V (b1) = V (b2) and we use the lexicographic preference ordering to break ties. The refinement s1 = {V (b1), V (b2)}, and the refinement s2 = {V (b1), V (b2)} \ {V (b1)} = {V (b2)}. Hence, by the definition of the placement function, P(b1) = 1, P(b2) = 1, P(s1) = 0, and P(s2) = 0.

Now, let us take a look at mechanism M2, where we again have two sellers but now only one buyer. There, s1 = s2 = {V (b)}, and the corresponding refinements are s1 = {V (b)} and s2 = {V (b)} \ {V (b)} = ∅(using lexicographic ordering over sellers as a tie-breaking rule). Hence, the placement function is P(b) = 1, P(s1) = 0, and P(s2) = 1. Note that following Definition 3, seller s2 keeps her item.

4Observe that having sets si, and not multisets, suffice as each buyer submits at most one valuation per seller, or auction.

Since sellers can incentivise buyers to invite their friends to join an auction, our mechanisms are dynamic, i.e., the social network structure changes as a result of sellers’ actions. To capture this, we define the update of a mechanism. In our definition, we assume that each buyer can be incentivised by one seller at a time. And, moreover, since buyers are rational, if they are offered incentives from two separate sellers, they choose the higher incentive, and their friends join the auction of the seller offering the higher incentive. Definition 4. Let an n-DAM M = ((Agt, F, Bdg, V, I, N), P, Pay, U) and a sequence Upd = σ1: β1,..., σn: βn be given. An n-DAM updated by the concurrent invitations by n sellers M Upd is a tuple ((Agt, F Upd, BdgUpd, V, I, N), P, Pay, U), where for all s ∈S, if N(σi) = s, Upd(σi) = βi̸ = •, and s = arg maxs′∈S I(N(βi), s′), then

• F Upd(s) = F(s) ∪{b|b ∈B and b ∈F(N(βi))}, • BdgUpd(s) = Bdg(s) − I(N(βi), s) and BdgUpd(N(βi)) = Bdg(N(βi)) + I(N(βi), s), Ties are broken by the lexicographic order of sellers’ names5.

Intuitively, given a concurrent information diffusion operator σ: β, in the updated mechanism all friends of buyer βi will join the auction run by σi if σi is one of the sellers that incentivise βi, and moreover, offers the highest incentive. Then, the seller’s budget is reduced by the value of the incentive, and the budget of the corresponding buyer is increased by the value of the incentive. Definition 5. Let M = ((Agt, F, Bdg, V, I, N), P, Pay, U) be an n-DAM. The semantics of Ln is defined by induction as follows:

M, a |= α iff N(α) = a M, a |= ¬φ iff M, a̸ |= φ M, a |= φ ∧ψ iff M, a |= φ and M, a |= ψ M, a |= □φ iff ∀b ∈Agt: b ∈F(a) implies M, b |= φ

M, a |= [σ: β]φ iff if ∀σi ∈σ\•: N(βi) ∈F(N(σi)) and

Bdg(N(σi)) ⩾I(N(βi), N(σi)), then M σ:β, a |= φ

M, a |= ♡α iff

P(N(α)) = 1 if α̸ = •, P(a) = 1 if α = •

M, a |= m X i=1 ziti ⩾z iff m X i=1 zit′ i ⩾z, where t′ i =

U(N(α)) if ti = utα, U(a) if ti = ut•.

The semantics definition for the clause M, a |= [σ: β]φ checks whether all sellers, who did not choose to skip their turn, are (i) incentivising the buyers that currently participate in their auction, and (ii) whether the sellers have sufficient budgets to pay the incentives. If (i) and (ii) hold, then φ is

5In particular, if there are two or more sellers offering a buyer the same maximal incentive, the buyer propagates the auction information of the seller that appears first in the lexicographic order.

19101

<!-- Page 4 -->

s: σ, 5 a: α, (3, 1, 5)

b: β, (8, 2, 6)

c: γ, (9, 9, 1)

d: δ, (11, 10, 0)

s: σ, 0 a: α, (8, 1, 5)

b: β, (8, 2, 6)

c: γ, (9, 9, 1)

d: δ, (11, 10, 0)

**Figure 2.** Mechanism M (left) and updated mechanism M σ:α (right). For the seller s, her name is σ and her budget in M is 5. For buyer a, her name is α, and (3, 1, 5) denotes the fact that Bdg(a) = 3, V (a) = 1, and I(a, s) = 5. Similarly, for other agents. The new link in M α is dashed.

evaluated in the updated mechanism M σ:β, a. The dual ⟨σ: β⟩φ holds iff (i) and (ii) hold, and M σ:β, a |= φ. For clauses of ♡α and linear inequalities, we distinguish the cases of an agent named α and the current agent, denoted by nominal •. Example 3. Consider 1-seller SMF mechanism M and its update M σ:α in Figure 2. We have, for example, that M, a |= (utσ = 7) ∧♡β ∧⟨α⟩(utσ = 9 ∧♡γ), where the utility of the seller σ increases after she incentivises the agent named α to invite her friends. Indeed, in mechanism M, the seller’s budget is 5, and the highest valuation among the buyers participating in the auction is 2 (from agent β). Hence, the total utility of the seller is 7. Since agent β is currently the highest bidder, she would have been the winner of the auction in the current mechanism (conjunct ♡β). After the seller incentivises α to invite all her friends to the auction, the budget of α increases by her incentive (i.e. by 5 to the total 8), and agent γ joins the auction (dashed line in M σ:α). Since her valuation is the highest, she gets the item (conjunct ♡γ) and the utility of the seller increases to 9. We also have that M, a |= ¬⟨α⟩⟨γ⟩(utσ > 9), i.e., the seller cannot increase her utility further by trying to reach the richest buyer δ as she does not have enough budget for two rounds of referrals.

Now we turn to a 2-seller example. Consider the SMF mechanism M and its updates in Figure 3. We assume that sellers s1 and s2 have both budgets 1, and that for both of them and all buyers, the incentives are 1, i.e., each seller can incentivise only one buyer. Moreover, let us assume that each buyer, apart from b and e, evaluates the item as 1. Buyer b has valuation 4, and buyer e has valuation 3.

We can see that in mechanism M, each seller has utility of 2, and buyers a and c get the item (recall that we assume the lexicographic tie-breaking rule). Formally, utσ1 = 2 ∧utσ2 = 2 ∧♡α ∧♡γ. We can also consider a more cooperative goal of the mechanism configuration, where each agent either has the item or has a friend who has the item, expressed by V i∈NomM i →(♡• ∨♢♡•), where NomM = {σ1, σ2, α,..., ζ}. Mechanism M does not satisfy this goal, as, for example, the formula does not hold for agent d.

Now, assume that both sellers decide to diffuse the information about their auctions over the network. Seller s1 incentivises buyer d to invite all her friends, i.e., e, to the auction; and similarly for seller s2 and buyer c who invites b. The resulting update M σ1:δ,σ2:γ is depicted in the middle of Figure 3. After this diffusion, the utility of seller s1 be- s1: σ1 d: δ a: α, ♡ f: ζ e: ϵ, 3 s2: σ2 c: γ, ♡ b: β, 4 s1: σ1 d: δ a: α f: ζ e: ϵ, 3, ♡ s2: σ2 c: γ b: β, 4, ♡ s1: σ1 d: δ a: α f: ζ e: ϵ, 3 s2: σ2 c: γ, ♡ b: β, 4, ♡

**Figure 3.** Mechanism M and its updates. In the mechanisms, there are two sellers, s1 and s2, and six buyers, a, b,..., f. Agents’ names are shown near the state label. New links are dashed. The allocation of the sold items is depicted by ♡.

comes 3 (1 is spent on the incentive, and agent e bids 3), and the utility of seller s2 is 4, i.e., for both sellers, the diffusion allowed them to increase their utilities by reaching bidders with higher valuations. Formally, we can write this as utσ1 = 2∧utσ2 = 2∧[σ1: δ, σ2: γ](utσ1 > 2∧utσ2 > 2).

Interestingly, such a diffusion performed by both sellers allows us to reach the cooperative goal: formula [σ1: δ, σ2: γ] V i∈NomM i →(♡• ∨♢♡•) is valid in mechanism M. Although the diffusion operator [σ1: δ, σ2: γ] allows sellers to increase their utilities and also achieve the cooperative goal, it requires a coordinated action from the sellers. Thus, seller s1 can increase her utility even more and outperforms seller s2 by incentivising buyer a instead of d, and the resulting updated mechanism M σ1:α,σ2:γ is depicted on the right of Figure 3. In this case, a will invite her friends, including b, to join the auction of seller s1. Observe that there is nothing seller s2 can do to make her utility greater than 1 and thus outperform s1 (recall that as a tie-breaking rule we use the lexicographic ordering, and hence, if buyer b is being invited to both auctions, she will choose seller s1). In formulas, V i∈NomM∪{•}[σ1: α, σ2: i](utσ1 > utσ2). The cooperative goal V i∈NomM i →(♡• ∨♢♡•) is no longer valid in the mechanism as agent d does not satisfy it.

Strategic Properties of Diffusion Auctions Let us now demonstrate how to express Nash equilibrium in our setting, as well as study the complexities of the model checking and strategy existence problem.

We first define an appropriate notion of a finite DAM. The nuance here is that even if the set of agents is finite, we have a countably infinite number of names that can be assigned to buyers. Luckily for us, whenever a problem requires both a mechanism and a formula in the input, we need to care about only those nominals that occur explicitly in the formula.

Let M = ((B ∪S, F, Bdg, V, I, N), P, Pay, U) be a DAM with a finite B, and let name(φ) be the finite set of buyers’ names appearing in φ. Also, let buyers(φ) = {b ∈

19102

<!-- Page 5 -->

B | ∃β ∈name(φ) s.t. N(β) = b} be a subset of buyers that are named in φ. For each buyer b ∈B \ buyers(φ), i.e., not named in φ, we pick one arbitrary β ∈B such that N(β) = b, and the finite set of such names is unnamed(φ). We denote X = name(φ) ∪unnamed(φ). We define function N fin = NS ∪NB|X, where NB|X: X →B is a restriction of NB to only those names that explicitly appear in φ and single names for buyers not named in φ. By construction, N fin is finite. We denote M with N substituted with N fin as Mfin. Intuitively, N fin is a finite restriction of N.

It is straightforward to show the following by induction on φ and using the definition of the semantics.

Proposition 1. Let φ ∈Ln and a mechanism M be given. Then we have that M, a |= φ iff Mfin, a |= φ.

The size of a finite mechanism M is |M| = |Agt|+|F|+ |Bdg|+|V |+|I|+|N fin|+|P|+|Pay|+|U|. Since all mechanisms in this section are finite, we will use interchangeably M and Mfin, and N and N fin.

Nash Equilibrium We can now verify that a given joint diffusion action is a one-step Nash equilibrium (NE) over a given finite mechanism M. This is significant, as it allows reasoning about optimal strategies of sellers. Let φ:= ⟨σ: β⟩V

1⩽i⩽n utσi = mi express that after a joint diffusion action ⟨σ: β⟩, utilities of all sellers i are mi.

In order to verify that such a diffusion is indeed an NE, we check that no single seller can increase her utility by deviating, i.e., by incentivising some other buyer present in the same mechanism. The formula for the NE in this case is φ ∧Vn i=1

V γ∈Nom•

M ⟨σ1: β1,..., σi: γ,..., σn: βn⟩(utσi ⩽ mi), where Nom•

M is the set of names appearing in the finite mechanism plus •.

We can further generalise the setting to a k-step NE, by taking φk:= ⟨σ: α⟩1...⟨σ: γ⟩k V

1⩽i⩽n utσi = mi meaning that after a k-sequence of joint diffusion actions, sellers’ utilities are mi’s. Then the corresponding formula for the k-step NE is φk ∧Vn i=1

V γ∈Nom•

M ⟨σ1: α1,..., σi: γ,..., αn: βn⟩1.... Vn i=1

V γ∈Nom•

M ⟨σ1: β1,..., σi: γ,..., σn: βn⟩k(utσi ⩽mi).

## Model

Checking and Strategy Existence First, we show that the complexity of the model checking problem for Ln is in P.

Theorem 1. Model checking Ln is in P for the class of finite DAMs with polynomially computable placement, payment, and utility functions.

Proof. In Algorithm 1, we focus on the dynamic modality and the allocation operator6.

## Algorithm

## 1 An algorithm for model checking

Ln

1: procedure MC(M, a, φ) 2: case φ = [σ: β]ψ

6Modal, nominal (Franceschet and de Rijke 2006), and arithmetic cases (Dasgupta, Papadimitriou, and Vazirani 2006) are standard and computed in polynomial time. We omit them for brevity.

3: for σi ∈σ\• do 4: if N(βi) ∈F(N(σi)) and Bdg(N(σi)) ⩾

I(N(βi), N(σi)) then 5: if N(σi) = arg maxN(σi)∈S I(N(βi), N(σi)))

then

6: F σ:β(N(σi)) = F(N(σi)) ∪{a | a ∈B and a ∈F(N(βi))}

7: Bdgσ:β(N(σi)) = Bdg(N(σi)) −

I(N(βi), N(σi))

8: Bdgσ:β(N(βi))) = Bdg(N(βi))) +

I(N(βi), N(σi))) 9: else 10: return true 11: return MC(M σ:β, a, ψ) 12: case φ = ♡γ 13: if γ̸ = • then 14: return P(N(γ)) = 1 15: else 16: return P(a) = 1

On line 5, we check that seller N(σi) offers the highest incentive to the corresponding buyer. If there are two sellers that offer the highest incentive to the same buyer, we assume that arg maxN(σi)∈S I(N(βi), N(σi))) returns the seller that appears earlier in the lexicographic order.

The algorithm directly mimics the semantics of Ln and thus correctness can be shown by induction on φ. First, recall that here we assume that the allocation, payment, and utility functions are all computable in polynomial time. For the case of φ = [σ: β]ψ, the size of an updated mechanism M σ:β is at most O(|M|2) (in the worst case, the friendship relation is universal) and it can be computed in polynomial time. The procedure MC(M, a, φ) is run for at most |φ| times and for at most |φ| mechanisms. Hence, MC(M, a, φ) is used for a polynomial amount of time.

Having the model checking result at hand, we can formulate and show the complexity of the strategy existence problem (proof is given in (Galimullin, Mittelmann, and Perrussel 2025)). The problem intuitively consists in checking whether, for a given mechanism and a mutual sellers’ goal, there is a way (a strategy) for all sellers to achieve φ in a finite number of steps.

Definition 6. Given a finite mechanism M and a goal φ ∈Ln, the strategy existence problem consists in determining whether there is a finite sequence of concurrent incentivisations ⟨σ: β⟩∗= ⟨σ: α⟩....⟨σ: γ⟩such that M, s |= ⟨σ: β⟩∗φ for sellers s ∈S.

Theorem 2. The strategy existence problem is NP-complete for the class of finite DAMs with polynomially computable placement, payment, and utility functions.

Reasoning About Sellers’ Strategies While considering the strategy existence problem, we looked at how all sellers can reach their joint goal via a sequence of concurrent incentivisation actions. However, in diffusion auctions with multiple sellers selling the copy of

19103

<!-- Page 6 -->

the same item, sellers and coalitions thereof may compete against each other for buyers. To capture this strategic competitive setting, we introduce a modality inspired by coalitional operators from CL (Pauly 2002) and ATL (Alur, Henzinger, and Kupferman 2002). In particular, we extend the language of Ln with ⟨[C]⟩φ for C ⊆S, meaning that there is a (one-step) strategy for the coalition of sellers C to incentivise buyers such that no matter what other sellers do, φ holds. In other words, modalities ⟨[C]⟩capture the ability of sellers in C to reach outcome φ in the competitive setting.

Definition 7. The language SLn of the n-seller strategic logic for diffusion incentives is defined as follows:

φ:= α | (z1t1 +... + zmtm) ⩾z | ¬φ | (φ ∧φ) | □φ | [σ1: β1,..., σn: βn]φ | [⟨C⟩]φ | ♡γ, where C ⊆S, and the dual of [⟨C⟩]φ is ⟨[C]⟩φ:= ¬[⟨C⟩]¬φ. We will denote by σC: βC the assignment of buyers names βC from B• to the coalition of sellers σC such that all sellers not in coalition are assigned • (i.e., they skip their turn). Moreover, we will denote σC ∪σS\C: βC ∪βS\C the full assignment of n buyers from B• to n sellers.

Definition 8. Let M = ((Agt, F, Bdg, V, I, N), P, Pay, U) be an n-DAM. The semantics of SLn extends the semantics of Ln with the following clause and its dual:

M, a |= ⟨[C]⟩φ iff ∃βC∀βS\C: M, a |= ⟨σC: βC⟩⊤and

M, a |= [σC ∪σS\C: βC ∪βS\C]φ

M, a |= [⟨C⟩]φ iff ∀βC∃βS\C: M, a |= ⟨σC: βC⟩⊤implies

M, a |= ⟨σC ∪σS\C: βC ∪βS\C⟩φ

Intuitively, ⟨[C]⟩φ holds if and only if there is a choice of buyers for the coalition of sellers C such that this choice is possible (part ⟨σC: βC⟩⊤) and whichever buyers the rest of the sellers decide to incentivise, φ holds after the resulting joint concurrent action.

It is immediate that the following formulas are valid7:

• ⟨[C]⟩φ →⟨[C ∪D]⟩φ, i.e., a superset of a coalition is at least as powerful as the coalition. • [⟨∅⟩]φ →⟨[S]⟩φ, i.e., the relationship between the empty and the grand coalitions. • ⟨[C]⟩(φ∧ψ) →⟨[C]⟩φ, i.e., the ability to achieve two goals implies the ability to achieve any single one of them.

Example 4. The ability to reason about strategies of coalitions of sellers allows us to consider truly competitive and cooperative scenarios. For the first one, consider ⟨[σ1, σ2]⟩[⟨σ3⟩](utσ1 > utσ3) meaning that a coalition of the first two sellers can preclude the third seller from having a utility equal to or higher than that of the first seller in a twostep incentivisation scenario. In a more altruistic setting, consider ¬⟨[σ1, σ2]⟩(utσ1 +utσ2 > 3)∧⟨[σ1, σ2, σ3]⟩(utσ1 + utσ2 > 3) meaning that together, the first and the second sellers cannot achieve a joint utility higher than 3, but if they cooperate with the third seller, this goal is satisfied.

7These formulas are some of the validites of CL (Pauly 2002).

Expressivity and Model Checking Having introduced a strategic extension of Ln, it is quite natural to wonder whether we gain anything in terms of expressivity, and, if yes, whether it comes at a price. We show that the answer to both questions is yes (with a caveat).

Theorem 3. Let M, a be a finite n-DAM and φ ∈SLn. Then there exists a ψ ∈Ln s.t. M, a |= φ iff M, a |= ψ.

Proof. To prove the theorem, we present a truth-preserving translation t: SLn →Ln. All cases, apart from the strategic one, are trivial as Ln ⊂SLn. For the strategic case, we have t(⟨[C]⟩φ) = W βC∈Nom•

M

|C|

V βS\C∈Nom•

M

|S\C|(⟨σC:

βC⟩⊤∧[σC ∪σS\C: βC ∪βS\C]t(φ)). Note that this is a well-formed formula because we are dealing with a finite mechanism and hence we can explicitly go over the elements in Nom•

M

|C| one by one, where Nom•

M

|C| is the set of all tuples of agent names in M of size |C|. It follows from the definition of the semantics that the translation is truthpreserving and terminating.

While Theorem 3 presents a translation that, for a given finite mechanism M, a and a formula φ ∈SLn, produces a corresponding formula ψ ∈Ln that agrees with φ on M, a, this result cannot be extended to arbitrary DAMs. In particular, the next theorem states that it is not the case that for a given φ ∈SLn we can always find a ψ ∈Ln that will agree with φ on all mechanisms. In other words, SLn is more expressive than Ln. To show this, observe that modalities ⟨[C]⟩φ quantify over all buyers’ names, even those that are not explicitly present in the formula. A sketch of the proof of the next theorem is given in (Galimullin, Mittelmann, and Perrussel 2025).

Theorem 4. SLn is strictly more expressive than Ln, i.e. Ln ⊂SLn and there is a φ ∈SLn s.t. for all ψ ∈Ln there is a mechanism M, a such that M, a |= φ iff M, a̸ |= ψ.

As promised, the greater expressive power comes with a higher model checking complexity.

Theorem 5. Model checking SLn is PSPACE-complete for the class of finite DAMs with the placement, payment, and utility functions computable in polynomial space.

Proof. To show that the problem is in PSPACE, we present Algorithm 2 that extends the P-time Algorithm 1.

## Algorithm

2 An algorithm for model checking SLn

1: procedure MC(M, a, φ) 2: case φ = ⟨[C]⟩ψ 3: for βC = β1,..., β|C| s.t. βi ∈dom(NB|X) do 4: flag: = true 5: if MC(M, a, ⟨σC: βC⟩⊤) then 6: for βS\C = β1,..., β|S\C| s.t. βi ∈dom(NB|X) do 7: if not MC(M, a, [σC ∪σS\C: βC ∪βS\C]ψ) then 8: flag: = false 9: break 10: else 11: flag:= false 12: if flag then 13: return true

19104

<!-- Page 7 -->

14: return false

The only new case is φ = ⟨[C]⟩ψ. The treatment of the case follows the semantics and thus the correctness follows. Indeed, to verify whether for a given agent we have ⟨[C]⟩ψ, we look for a set of buyers that sellers in C will incentivise (lines 3–5), and then we check whether for all possible incentive diffusions by the remaining sellers (line 6) we still can satisfy ψ after each seller performs their action (line 7). Variable ‘flag’ keeps track of whether we have found such a choice for the sellers in C, and the algorithm returns true is yes, and false if not.

Observe that the algorithm checks an exponential number of subsets of buyers, and hence the running time is exponential in the size of the input. However, the algorithm uses only a polynomial amount of space. Note that we explore the tree of mechanism updates in a depth-first manner. The space required by a branch in such a tree, and hence by the algorithm, is bounded by O(|φ| · |M|2). PSPACE-hardness is shown via a reduction from the QBF problem (see (Galimullin, Mittelmann, and Perrussel 2025)).

## Related Work

Logics for auctions Logic-based formalisms have been developed to capture and reason about various aspects of auctions. One direction is bidding languages, most notably OR and XOR-based languages, which express the preferences of auction participants (see (Nisan 2000) for an overview). These languages compactly represent possible bids on item combinations, an important aspect in combinatorial auctions, where bidders place bids on bundles of distinct items. Our work, instead, is closer to logical approaches for reasoning about and designing auctions. Mittelmann, Bouveret, and Perrussel (2022) proposed a lightweight formalism to represent auction rules, whereas Belardinelli et al. (2022) addressed the representation of strategies in repeated auctions, and Mittelmann, Herzig, and Perrussel (2021) captured bounded rationality in auctions. Another line of research proposes the use of variants of Strategy Logic (SL) for the design of auction mechanisms, exploiting verification and synthesis (Mittelmann et al. 2025, 2023). Notably, the model-checking complexity for specifications in SL is non-elementary in the general case (Mogavero et al. 2014). There is also research on automated verification of auction protocols (Garg et al. 2025; Caminati et al. 2015; Lange et al. 2013) that stresses the importance of formal verification techniques for auctions.

Across all these works, the set of agents involved in the auction is fixed throughout its execution. To the best of our knowledge, our work is the first one to explore the dynamics of auction diffusion from a logic-based perspective.

DEL and social network logics Our intuition of model updates stems from dynamic epistemic logic (DEL), where one can model various information-changing events in the context of agents’ knowledge. Ideas of DEL were also adopted in the field of social network logics (SNLs), where one uses formal tools to study such phenomena on social networks as information diffusion (Christoff and

Hansen 2015; Baltag et al. 2019), social influence (Christoff, Hansen, and Proietti 2016), and echo chambers (Pedersen, Smets, and ˚Agotnes 2019), to name a few. See (Pedersen 2024, Chapter 3) for an overview. Perhaps the most related work here is (Galimullin and Pedersen 2024), where the authors explore visibility of posts on social networks, and how these posts propagate through the network, somewhat akin to how the information about an auction is spread in diffusion auctions. Using nominals for agent names is common in SNLs and comes from hybrid logic (see, e.g., (Areces and ten Cate 2007)). While discussing strategic logic SLn, we noted that our coalitional operators are inspired by those of CL and ATL. However, in CL and ATL models are static, i.e., they do not change as a result of agents’ actions. Hence, a more relevant work is that on coalition announcements (˚Agotnes and van Ditmarsch 2008; Galimullin 2021; de Lima 2014) in DEL, where strategic operators quantify over model changes that agents can bring about in a competitive setting, and with model checking complexity being PSPACE-complete (Alechina et al. 2021). Another related work is (Maubert et al. 2020), where agents play a multi-step concurrent game by modifying a model using modalities of DEL. Finally, there has been some work on adding arrows in modal logics (Areces, Fervari, and Hoffmann 2015).

## Conclusion

We have presented a formal framework for reasoning about sellers’ strategies in diffusion auctions. In particular, we introduced two logics, the n-seller logic for diffusion incentives Ln and its strategic version SLn, that can capture various properties of such auctions, like item allocations, utility increase, local properties of the underlying social network, and Nash equilibrium, to name a few. Our logics are dynamic, and hence they also allow us to verify whether the above-mentioned properties hold after modifications of the underlying social network that are engendered by sellers incentivising buyers to invite their friends to join auctions. To the best of our knowledge, this is the first work that tackles the problem of formal verification of diffusion auctions.

Our definition of diffusion auction mechanisms is quite general and allows us to capture a variety of auction types as long as the complexity of computing the placement, payment, and utility functions is no higher than the complexity of the model-checking problem of the corresponding logic. We have shown that it is in P for Ln and is PSPACEcomplete for SLn. Moreover, we have demonstrated that the complexity of the strategy existence problem for a given mechanism and a joint goal of sellers is NP-complete.

With our work, we start a research line on formal verification of diffusion auctions, and there are plenty of interesting further directions. In particular, we would like to tackle the formal verification of a probabilistic framework, capturing incomplete information and Bayesian analysis (Huang et al. 2025), as well as consider strategies of buyers. We have also mentioned some of the validities of our logics, and we find it very tempting to explore their axiomatisations. Finally, we plan to explore the case of multi-item diffusion auctions.

19105

<!-- Page 8 -->

## Acknowledgements

This research is partially supported by the ANR project NOGGINS ANR-24-CE23-4402.

## References

˚Agotnes, T.; and van Ditmarsch, H. 2008. Coalitions and announcements. In Padgham, L.; Parkes, D. C.; M¨uller, J. P.; and Parsons, S., eds., Proceedings of the 7th AAMAS, 673– 680. IFAAMAS. Alechina, N.; van Ditmarsch, H.; Galimullin, R.; and Wang, T. 2021. Verification and Strategy Synthesis for Coalition Announcement Logic. Journal of Logic, Language and Information, 30(4): 671–700. Alur, R.; Henzinger, T. A.; and Kupferman, O. 2002. Alternating-time temporal logic. Journal of the ACM, 49: 672–713. Areces, C.; Fervari, R.; and Hoffmann, G. 2015. Relationchanging modal operators. Logic Journal of the IGPL, 23(4): 601–627. Areces, C.; and ten Cate, B. 2007. Hybrid logics. In Blackburn, P.; Van Benthem, J.; and Wolter, F., eds., Handbook of Modal Logic, volume 3 of Studies in Logic and Practical Reasoning, 821–868. Elsevier. Baltag, A.; Christoff, Z.; Rendsvig, R. K.; and Smets, S. 2019. Dynamic Epistemic Logics of Diffusion and Prediction in Social Networks. Studia Logica, 107(3): 489–531. Belardinelli, F.; Condurache, R.; Dima, C.; Jamroga, W.; and Knapik, M. 2021. Bisimulations for verifying strategic abilities with an application to the ThreeBallot voting protocol. Information and Computation, 276: 104552. Belardinelli, F.; Jamroga, W.; Malvone, V.; Mittelmann, M.; Murano, A.; and Perrussel, L. 2022. Reasoning about Human-Friendly Strategies in Repeated Keyword Auctions. In Faliszewski, P.; Mascardi, V.; Pelachaud, C.; and Taylor, M. E., eds., Proceedings of the 21st AAMAS, 62–71. Caminati, M. B.; Kerber, M.; Lange, C.; and Rowat, C. 2015. Sound Auction Specification and Implementation. In Roughgarden, T.; Feldman, M.; and Schwarz, M., eds., Proceedings of the 16th EC, 547–564. ACM. Christoff, Z.; and Hansen, J. U. 2015. A logic for diffusion in social networks. Journal of Applied Logic, 13(1): 48–77. Christoff, Z.; Hansen, J. U.; and Proietti, C. 2016. Reflecting on Social Influence in Networks. Journal of Logic, Language and Information, 25(3-4): 299–333. Clarke, E. H. 1971. Multipart pricing of public goods. Public choice, 17–33. Clarke, E. M.; Henzinger, T. A.; Veith, H.; and Bloem, R., eds. 2018. Handbook of Model Checking. Springer. Dasgupta, S.; Papadimitriou, C.; and Vazirani, U. 2006. Algorithms. McGraw-Hill Higher Education. de Lima, T. 2014. Alternating-time temporal dynamic epistemic logic. Journal of Logic and Computation, 24(6): 1145–1178.

Dobzinski, S.; and Vondr´ak, J. 2012. The computational complexity of truthfulness in combinatorial auctions. In Faltings, B.; Leyton-Brown, K.; and Ipeirotis, P., eds., Proceedings of the 13th EC, 405–422. Dolgorukov, V.; Galimullin, R.; and Gladyshev, M. 2024. Dynamic Epistemic Logic of Resource Bounded Information Mining Agents. In Dastani, M.; Sichman, J. S.; Alechina, N.; and Dignum, V., eds., Proceedings of the 23rd AAMAS, 481–489. IFAAMAS / ACM. Fagin, R.; Halpern, J. Y.; and Megiddo, N. 1990. A Logic for Reasoning about Probabilities. Information and Computation, 87(1/2): 78–128. Franceschet, M.; and de Rijke, M. 2006. Model checking hybrid logics (with an application to semistructured data). Journal of Applied Logic, 4(3): 279–304. Galimullin, R. 2021. Coalition and relativised group announcement logic. Journal of Logic, Language and Information, 30(3): 451–489. Galimullin, R.; Mittelmann, M.; and Perrussel, L. 2025. Formal Verification of Diffusion Auctions. CoRR, abs/2511.08765. Galimullin, R.; and Pedersen, M. Y. 2024. Visibility and exploitation in social networks. Mathematical Structures in Computer Science, 34(7): 615–644. Garg, M.; Raja, N.; Sarswat, S.; and Singh, A. K. 2025. Double Auctions: Formalization and Automated Checkers. Journal of Automated Reasoning., 69(3): 17. Groves, T. 1973. Incentives in teams. Econometrica: Journal of the Econometric Society, 617–631. Guo, Y.; and Hao, D. 2021. Emerging Methods of Auction Design in Social Networks. In Zhou, Z., ed., Proceedings of the 30th IJCAI, 4434–4441. ijcai.org. Huang, Y.; Hao, D.; Fan, Z.; Guo, Y.; and Li, B. 2025. Approximate Revenue Maximization for Diffusion Auctions. CoRR, abs/2507.14470. Jamroga, W.; Kurpiewski, D.; and Malvone, V. 2022. How to measure usable security: Natural strategies in voting protocols. Journal of Computer Security, 30(3): 381–409. Lange, C.; Caminati, M. B.; Kerber, M.; Mossakowski, T.; Rowat, C.; Wenzel, M.; and Windsteiger, W. 2013. A Qualitative Comparison of the Suitability of Four Theorem Provers for Basic Auction Theory. In Carette, J.; Aspinall, D.; Lange, C.; Sojka, P.; and Windsteiger, W., eds., Proceedings of the 6th CICM, volume 7961 of LNCS, 200–215. Springer. Li, B.; Hao, D.; Gao, H.; and Zhao, D. 2022. Diffusion auction design. Artificial Intelligence, 303: 103631. Maubert, B.; Pinchinat, S.; Schwarzentruber, F.; and Stranieri, S. 2020. Concurrent Games in Dynamic Epistemic Logic. In Bessiere, C., ed., Proceedings of the 29th IJCAI, 1877–1883. ijcai.org. McAfee, R. P. 1992. A dominant strategy double auction. Journal of economic Theory, 56(2): 434–450. Mittelmann, M.; Bouveret, S.; and Perrussel, L. 2022. Representing and reasoning about auctions. Autonomous Agents and Multi-Agent Systems, 36(1): 20.

19106

<!-- Page 9 -->

Mittelmann, M.; Herzig, A.; and Perrussel, L. 2021. Epistemic Reasoning About Rationality and Bids in Auctions. In Faber, W.; Friedrich, G.; Gebser, M.; and Morak, M., eds., Proceedings of the 17th JELIA, volume 12678 of LNCS, 116–130. Springer. Mittelmann, M.; Maubert, B.; Murano, A.; and Perrussel, L. 2023. Formal Verification of Bayesian Mechanisms. In Williams, B.; Chen, Y.; and Neville, J., eds., Proceedings of the 37th AAAI, 11621–11629. AAAI Press. Mittelmann, M.; Maubert, B.; Murano, A.; and Perrussel, L. 2025. Formal verification and synthesis of mechanisms for social choice. Artificial Intelligence, 339: 104272. Mogavero, F.; Murano, A.; Perelli, G.; and Vardi, M. Y. 2014. Reasoning About Strategies: On the Model-Checking Problem. ACM Transactions on Computational Logic, 15(4): 34:1–34:47. Nisan, N. 2000. Bidding and allocation in combinatorial auctions. In Jhingran, A.; MacKie-Mason, J.; and Tygar, D. J., eds., Proceedings of the 2nd EC, 1–12. ACM. Nisan, N.; Roughgarden, T.; Tardos, ´E.; and Vazirani, V. V., eds. 2007. Algorithmic Game Theory. CUP. Pauly, M. 2002. A modal logic for coalitional power in games. Journal of Logic and Computation, 12(1): 149–166. Pedersen, M. Y. 2024. Malicious Agents and the Power of the Few: On the Logic of Abnormality in Social Networks. Ph.D. thesis, University of Bergen, Norway. Pedersen, M. Y.; Smets, S.; and ˚Agotnes, T. 2019. Analyzing Echo Chambers: A Logic of Strong and Weak Ties. In Blackburn, P.; Lorini, E.; and Guo, M., eds., Proceedings of the 7th LORI, volume 11813 of LNCS, 183–198. Springer. van Ditmarsch, H.; van der Hoek, W.; and Kooi, B. 2008. Dynamic Epistemic Logic, volume 337 of Synthese Library. Springer. Vickrey, W. 1961. Counterspeculation, auctions, and competitive sealed tenders. The Journal of Finance, 16(1): 8–37. Xu, J.; and He, X. 2020. Design of double auction mechanism based on social network. IEEE Access, 8: 8324–8335. Zhang, Y.; Zheng, S.; and Zhao, D. 2024. Optimal Diffusion Auctions. In Proceedings of the 27th ECAI, volume 392 of Frontiers in Artificial Intelligence and Applications, 3501– 3508. IOS Press. Zhao, D. 2021. Mechanism Design Powered by Social Interactions. In Dignum, F.; Lomuscio, A.; Endriss, U.; and Now´e, A., eds., Proceedings of the 20th AAMAS, 63–67. ACM. Zhao, D.; Li, B.; Xu, J.; Hao, D.; and Jennings, N. R. 2018. Selling Multiple Items via Social Networks. In Andr´e, E.; Koenig, S.; Dastani, M.; and Sukthankar, G., eds., Proceedings of the 17th AAMAS, 68–76. IFAAMAS.

19107
