---
title: "Weakest Bidder Types and New Core-Selecting Combinatorial Auctions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38771
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38771/42733
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Weakest Bidder Types and New Core-Selecting Combinatorial Auctions

<!-- Page 1 -->

Weakest Bidder Types and New Core-Selecting Combinatorial Auctions

Siddharth Prasad1*, Maria-Florina Balcan2, Tuomas Sandholm2,3,4,5

1Toyota Technological Institute at Chicago 2School of Computer Science, Carnegie Mellon University 3Strategy Robot, Inc. 4Strategic Machine, Inc. 5Optimized Markets, Inc. sprasad@ttic.edu, ninamf@cs.cmu.edu, sandholm@cs.cmu.edu

## Abstract

Core-selecting combinatorial auctions are popular auction designs that constrain prices to eliminate the incentive for any group of bidders—with the seller—to renegotiate for a better deal. They help overcome the low-revenue issues of classical combinatorial auctions. We introduce a new class of coreselecting combinatorial auctions that leverage bidder information available to the auction designer. We model such information through constraints on the joint type space of the bidders—these are constraints on bidders’ private valuations that are known to hold by the auction designer before bids are elicited. First, we show that type space information can overcome the well-known impossibility of incentive-compatible core-selecting combinatorial auctions. We present a revised and generalized version of that impossibility result that depends on how much information is conveyed by the type spaces. We then devise a new family of core-selecting combinatorial auctions and show that they minimize the sum of bidders’ incentives to deviate from truthful bidding. We develop new constraint generation techniques—and build upon existing quadratic programming techniques—to compute core prices, and conduct experiments to evaluate the incentive, revenue, fairness, and computational merits of our new auctions. Our new core-selecting auctions directly improve upon existing designs that have been used in many high-stakes auctions around the world. We envision that they will be a useful addition to any auction designer’s toolkit.

## Introduction

The design of combinatorial auctions (CAs) is a complex task that requires careful engineering along several axes to best serve the application at hand. Just some of these axes are: taming cognitive and communication costs of eliciting and understanding bidders’ inherently combinatorial valuations, tractable computation and optimization of economically efficient outcomes that allocate resources to those that value them the most, and determining prices that simplify bidders’ incentives while generating acceptable revenues for the seller. These complexities are most evident in fielded applications of CAs including sourcing (Sandholm 2013;

*Work performed while at Carnegie Mellon University. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Hohner et al. 2003; Sandholm et al. 2006), spectrum allocation (Cramton 2013; Leyton-Brown, Milgrom, and Segal 2017), treasury auctions (Klemperer 2010), and others. The focus of the present paper is on better pricing rules for CAs. The classical Vickrey (1961)-Clarke (1971)-Groves (1973) (VCG) mechanism is an economically efficient CA that is incentive compatible (IC)—a property of great practical importance since it levels the playing ground for bidders by making it worthless to strategize about their individual bids. But, the VCG auction has two major complementary issues (among others (Ausubel and Milgrom 2006)) that prevent it from being practically viable: low revenue and prices that are not in the core. The latter means that some bidders might end up paying so little for their winnings that others who offered more for those same items would take issue. Core-selecting CAs fix this problem with prices that ensure no coalition of bidders plus the seller would want to renegotiate for a better deal, but these give up on incentive compatibility. So, most core-selecting CAs use prices that minimize bidders’ incentives to deviate from truthful bidding.

Core-selecting CAs have been used to auction licenses for wireless spectrum by a number of countries’ governments including Australia, Canada, Denmark, Ireland, Mexico, the Netherlands, Portugal, Switzerland, the United Kingdom, and others, generating many billions of dollars in revenue (Cramton 2013; Palacios-Huerta, Parkes, and Steinberg 2024). Ausubel, Aperjis, and Baranov (2017) review some of the key design choices of the FCC incentive auction that was completed in the United States in 2017. They suggest that some instances of winners paying zero for certain packages despite losers bidding competitively (Ausubel and Baranov 2023) could have been avoided with a core-selecting payment rule instead of the VCG rule adopted by the FCC (though a core-selecting rule would have introduced other practical difficulties in other stages of the auction). While the most prominent real-world deployment of core-selecting CAs is probably spectrum auctions, their use has been proposed for other important applications such as electricity markets (Karaca and Kamgarpour 2019), advertisement markets (Goetzendorff et al. 2015; Niazadeh et al. 2022), and auctions for wind farm development rights (Ausubel and Cramton 2011).

In this paper we introduce a new class of core-selecting

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17206

<!-- Page 2 -->

CAs that improve upon prior designs by taking advantage of bidder information available to the auction designer through constraints on the bidders’ type spaces. Our starting point is the weakest-type (WT) auction, which is a type-spacedependent improvement of VCG (Krishna and Perry 1998; Balcan, Prasad, and Sandholm 2023). Our core-selecting CAs build upon the WT auction, and minimize the sum of bidders’ incentives to deviate from truthful bidding. They generalize and improve upon the core-selecting CA designs that have been developed in the literature so far, some of which have been successfully used in spectrum auctions (Day and Raghavan 2007; Day and Milgrom 2010; Day and Cramton 2012; Erdil and Klemperer 2010).

## 1.1 Our Contributions

First, we show that information expressed by type spaces can overcome the following well-known impossibility result due to Othman and Sandholm (2010) and Goeree and Lien (2016): under unrestricted type spaces either (i) VCG is not in the core in which case no IC core-selecting CA exists or (ii) VCG is the unique IC core-selecting CA. In general CAs where bidders’ valuations exhibit complementarities (that is, the value of a bundle is more than the sum of its parts), VCG is typically not in the core. VCG is in the core only under strict conditions on bidder valuations that rule out complementarity (like buyer-submodularity or gross-substitutes (Ausubel and Milgrom 2002)). We provide a revised and more general version of the impossibility result. Our result (Theorem 3.1) states that either (i) WT is not in the core in which case no IC core-selecting CA exists, (ii) WT is the unique IC core-selecting CA, or (iii) there are infinitely many IC core-selecting CAs including WT (and we characterize all such CAs). In particular, vanilla VCG has no bearing on the existence of IC core-selecting CAs (when type spaces are unrestricted VCG and WT are identical, so our result recovers the one by Othman and Sandholm (2010) and Goeree and Lien (2016) in that case).

Second, we devise a new family of type-space-dependent core-selecting CAs that minimize the sum of bidders’ incentives to deviate from truthful bidding. Typical core-selecting CAs choose prices that lie on the minimum-revenue face— referred to as the minimum-revenue core (MRC)—of the core polytope (Parkes, Kalagnanam, and Eso 2001; Day and Raghavan 2007; Day and Milgrom 2010; Erdil and Klemperer 2010; Day and Cramton 2012). Day and Milgrom (2010) show that MRC points minimize bidders’ total incentive to deviate from truthful bidding (and therefore minimize incentives to deviate in a Pareto sense as well). Our new design chooses core prices that minimize revenue subject to the additional constraint that they lie above WT. We generalize Day and Milgrom’s result (which hinges on the assumption of unrestricted typespaces), and show that our revised version of the minimum-revenue core provides optimal incentives for bidders.

Third, we develop new constraint generation routines for computing WT prices. We compare two linear programming formulations of WT price computation: one is due to Balcan, Prasad, and Sandholm (2023) and the other is based on Bikhchandani and Ostroy (2002). Both linear pro- grams have an exponential number of constraints, so we develop constraint generation routines to solve them. In our experiments, the Balcan, Prasad, and Sandholm (2023) formulation leads to significantly smaller constraint-generation solve times and iterations. On most instances, WT price computation via our constraint generation routine only adds a modest run-time overhead to winner determination.

Finally, we present proof-of-concept experiments that evaluate the incentive, revenue, and fairness properties of our new core-selecting CAs. We coin and implement three new core-selecting payment rules that select payments on our revised MRC. Our implementation uses the quadratic programming and core-constraint generation technique developed by Day and Cramton (2012).

In Appendix A, we survey additional related work.

## Problem Formulation

and Background

In a combinatorial auction (CA) there is a set M = {1,..., m} of indivisible items to be auctioned off to bidders N = {1,..., n} who can submit bids for distinct bundles (or packages) of items. Bidder i reports to the auction designer her valuation vi: 2M →R≥0 that encodes the maximum value vi(S) she is willing to pay for every distinct bundle of goods S ⊆M. Let v = (v1,..., vn) denote the valuation profile of all bidders, and let v−i = (v1,..., vi−1, vi+1,..., vn) denote the profile of bids excluding bidder i. For C ⊆N let vC = (vj)j∈C and let v−C = (vj)j∈N\C. We assume bidders report their valuations in the XOR bidding language (Sandholm 1999; Nisan 2000), under which a bidder can only win at most one of the bundles she explicitly placed a nonzero bid for. For bidder i, let Bi ⊆2M be the set of bundles she bid on (assume for notational convenience that each bidder i implicitly submits vi(∅) = 0). Let Γ = Γ(B1,..., Bn) ⊆B1×· · ·×Bn denote the set of feasible allocations, that is, the set of partitions S1,..., Sn of M with Si ∈Bi for each i and Si ∩Sj = ∅ for each i, j. Boldface S = (S1,..., Sn) ∈Γ(B1,..., Bn) denotes a feasible allocation.

Before bids/valuations are submitted, bidder i’s valuation vi, also called her type, is her own private information. The auction designer might have some prior information about the bidders, and that is modeled by the joint type space of the bidders, denoted Θ ⊆×i∈N R2m

≥0. The auction designer knows that v ∈Θ. Given v−i, let Θi(v−i) = {ˆvi: (ˆvi, v−i) ∈Θ} be the projected type space of bidder i. So, after seeing the revealed bids v−i of all other bidders, the auction designer knows vi ∈Θi(v−i). This model of type spaces begets a rich and expressive language of bidder information available to the auction designer—Θ can represent any statement of the form “the joint valuation profile v of all bidders satisfies property P” (Balcan, Prasad, and Sandholm (2023) provide concrete examples). The typical assumption in mechanism design is an unrestricted type space Θ = ×i∈N R2m

≥0 (what is usually assumed is the existence of a known prior distribution over the type space). In contrast, we will be concerned with explicit representations of the auction designer’s knowledge via the type space and how that influences both practical computation and the

17207

<!-- Page 3 -->

auction design itself.

Auction Design Desiderata An auction is determined by its allocation rule and its payment rule. In this paper we are concerned with efficient auctions. An efficient auction selects the efficient (welfare-maximizing) allocation: S∗= (S∗

1,..., S∗ n) = argmaxS∈Γ

P j∈N vj(Sj). The winner determination problem of computing the efficient allocation is NP-complete (by a reduction from weighted set packing), but solving its integer programming formulation is generally a routine task for modern integer programming solvers. Let w(v) = maxS∈Γ

P j∈N vj(Sj) denote the efficient welfare. An auction is incentive compatible (IC) if each bidder’s utility (value minus payment) is weakly maximized by truthful bidding, independent of other bidders. An auction is individually rational (IR) if truthful bidders are always guaranteed non-negative utility, independent of other bidders.

VCG and WT Auctions The classical auction due to Vickrey (1961), Clarke (1971), and Groves (1973) (VCG) chooses the efficient allocation S∗, and charges bidder i a payment of pVCG i (v) = w(0, v−i) −P j̸=i vj(S∗ j). Let pVCG = (pVCG

1,..., pVCG n) denote the vector of VCG payments. VCG is incentive compatible and individually rational. The weakest-type (WT) auction (Krishna and Perry 1998; Balcan, Prasad, and Sandholm 2023) chooses the efficient allocation S∗achieving welfare w(v) and charges bidder i a payment of pWT i (v) = minevi∈Θi(v−i) w(evi, v−i) − P j̸=i vj(S∗ j). The evi achieving the minimum is the weakest type in Θi(v−i). Let pWT = (pWT

1,..., pWT n) denote the vector of WT payments. For Θ closed and convex, WT is revenue maximizing among all efficient, IC, and IR auctions (Krishna and Perry 1998; Balcan, Prasad, and Sandholm 2023).

Core-Selecting CAs and the Minimum-Revenue Core Let W = {i ∈N: S∗ i̸ = ∅} be the set of winning bidders in the efficient allocation S∗. A combinatorial auction is in the core if (i) it chooses the efficient allocation S∗and (ii) prices p ∈RW lie in the core polytope Core(v), defined by core constraints for every coalition of bidders

P i∈W \C pi ≥w(0N\C, vC) −P j∈C vj(S∗ j) ∀C ⊆N and IR constraints vi(S∗ i) −pi ≥0 ∀i ∈W. This formulation of the core gives rise to a direct interpretation of core prices as “group VCG prices”: any set of winners must in aggregate pay the externality they impose on the other bidders (ours is not the typical formulation of the core, which is a notion originally from cooperative game theory, but is most convenient from an implementation/mathematical programming perspective as in Day and Raghavan (2007); Day and Cramton (2012); B¨unz, Seuken, and Lubin (2015)).

The minimum-revenue core (MRC) is the set MRC = argmin{∥p∥1: p ∈Core} that consists of all core prices of minimal revenue. Day and Raghavan (2007); Day and Milgrom (2010) show that the MRC captures exactly the set of core prices that minimize the sum of bidders’ incentives to deviate from truthful bidding. The MRC is not unique and there can be (infinitely) many MRC prices. Some coreselecting CAs that select unique MRC points that have been proposed are VCG nearest (Day and Cramton 2012), which finds the MRC point closest in Euclidean distance to VCG, and zero nearest (Erdil and Klemperer 2010), which finds the MRC point closest in Euclidean distance to the origin.

Since core-selecting CAs are in general not IC, a coreselecting CA only guarantees that prices are in the revealed core with respect to reported bids. But, from a regulatory viewpoint, the revealed core is nonetheless a useful solution concept since core constraints prevent any group of bidders from lodging a meaningful complaint based on their actual bids (B¨unz, Lubin, and Seuken 2022).

Impossibility of IC Core-Selecting CAs We revisit the following dichotomy for core-selecting CAs when type spaces are unrestricted (Goeree and Lien 2016; Othman and Sandholm 2010): either (i) VCG is not in the core which implies no IC core-selecting auction exists or (ii) VCG is in the core and is the unique IC core-selecting auction. That dichotomy relies on the assumption that Θ is unrestricted, that is, Θ = R2m

≥0. We revise and generalize that result to depend on bidders’ type spaces. The proof (proofs of all results in this paper are in Appendix F) relies on the revenue optimality of WT prices subject to efficiency, IC, and IR (Balcan, Prasad, and Sandholm 2023). Theorem 3.1. Let Θ be closed and convex. Let v be the vector of bidders’ true valuations. If pWT(v) /∈Core(v), no incentive compatible core-selecting CA exists. Otherwise, let C ⊆2N be the set of core constraints that pWT satisfies with equality. Let C′ = {C′ ⊆N: C′ ∩C = ∅∀C ∈C} and for C′ ∈C′ let s(C′) = P i∈W \C′ pWT i −w(0, vC′) + P j∈C′ vj(S∗ j) be the slack of the C′-core constraint. Then for any C′ ∈C′ all prices in the set {(pWT

W ∩C′ −ε, pWT

W \C′):

∥ε∥1 ≤s(C′), ε ∈RW ∩C′

≥0 } are in the core and are attainable via an incentive compatible CA.

Theorem 3.1 implies that if WT is in the core, there is a potential continuum of IC core-selecting payment rules obtained by decreasing WT prices along non-binding faces of the core. In particular, the existence of IC core-selecting CAs does not depend on VCG prices but on WT prices. WT and VCG coincide when type spaces do not convey sufficient information about the additional welfare created by a bidder: pWT i = pVCG i if and only if minevi∈Θi(v−i) w(evi, v−i) = w(0, v−i), which says that the information conveyed by Θi(v−i) about bidder i is so weak that it cannot even guarantee that i’s presence adds any nonzero welfare to the auction. In this case, Theorem 3.1 recovers the result of Othman and Sandholm (2010) and Goeree and Lien (2016).

In Appendix B, we discuss a modified “agents-aresubstitutes” condition that characterizes when pWT ∈Core.

## 4 Our New Core-Selecting CAs

In this section we introduce our new class of core-selecting CAs based on weakest types, and prove that it provides bidders with optimal incentives (by minimizing the sum of bidders’ incentives to deviate, therefore providing optimal incentives in a Pareto sense as well) among all core-selecting CAs. Our result generalizes the result of Day and Milgrom

17208

<!-- Page 4 -->

(2010) which was in the setting of unrestricted type spaces (our result recovers theirs in the unrestricted case).

In Section 3 we have shown that if WT is not in the core, then all core-selecting CAs necessarily violate incentive compatibility. To measure the incentive violations of a core-selecting CA, we borrow the notion of an incentive profile from Day and Milgrom (2010). The utility profile (resp., deviation profile) of an efficient CA with payment rule p(v) is given by {µp i (v)}i∈W (resp. {δp i (v)}i∈W), where µp i (v) = maxbvi(vi(ˆSi) −pi(bvi, v−i)) is bidder i’s maximum obtainable utility from misreporting and δp i (v) = µp i (v)−(vi(S∗ i)−pi(vi, v−i)) is bidder i’s maximum utility gain over truthful bidding (ˆS denotes the efficient allocation under reported bid profile (ˆvi, v−i)). Our goal is to design core-selecting payment rules p that minimize the sum of bidders’ incentives to deviate, which is precisely P i δp i (v). The quantity δp i can be viewed as a form of ex-post regret for truthful bidding for bidder i. Throughout this section, v denotes the true valuations of the bidders.

The following lemma generalizes Day and Raghavan (2007, Theorem 3.2); its proof is identical to theirs. Lemma 4.1. Let ˆp be any payment rule that implements the efficient allocation such that ˆpi ≥pWT i. Then, µ ˆp i (v) ≤ vi(S∗ i) −pWT i (v) and δ ˆp i (v) ≤ˆpi(v) −pWT i (v). That is, the maximum utility winner i can obtain by misreporting under

ˆp is no more than her utility under pWT.

The following result generalizes Day and Milgrom (2010, Theorem 2). Theorem 4.2. Let ˆp be any IR payment rule that implements the efficient allocation such that ˆpi ≥pWT i. Let v′ i denote the misreport for winner i defined by v′ i(S∗ i) = pWT i (v), v′ i(S) = 0 for all S̸ = S∗ i. Then, v′ i is a best response for i that gives her utility equal to vi(S∗ i) −pWT i (v). That is, under ˆp, winner i can always guarantee herself utility equal to what her utility would have been under pWT.

Theorem 4.2 allows us to characterize the subset of points that minimize the sum of bidders’ incentives to deviate of any upwards closed region. They are exactly the set of points of minimal revenue. Given a price vector ˆp ∈ RW and any closed region A ⊆RW, let MRA(ˆp) = argmin {∥p∥1: p ∈A, ˆp ≤p ≤(vi(S∗ i))i∈W } be the set of IR price vectors in A of minimal revenue that lie above

ˆp. Let MRC(bp) = MRCore(bp) denote the MRC above bp. Theorem 4.3. For A ⊆ RW upwards closed, MRA(pWT) ⊆argmin

P i∈W δp i (v): p ∈A

. Therefore, MRC(pWT(v)) ⊆argmin

P i∈W δp i (v): p ∈Core(v)

. Any payment rule p ∈MRC(pWT(v)) is therefore incentive optimal in a Pareto sense as well: there is no other core-selecting p′ such that δp′ i (v) ≤δp i (v) for all i and δp′ i∗(v) ≤δp i∗(v) for some i∗. Theorem 4.3 generalizes the results of Day and Raghavan (2007); Day and Milgrom (2010) since when Θi(v−i) is unrestricted for each agent i, MRC(pWT) = MRC(pVCG) which is the (unrestricted) minimum-revenue core they consider.

Theorem 4.3 gives strong theoretical justification for payment rules that lie on MRC(pWT). We expand on specific

**Figure 1.** Price vectors pVCG and pWT (in red) and their nearest respective minimum-revenue core points (in yellow, connected by a green line) as derived in Example 4.4. MRC(pWT) lies on a different face of the core than MRC(pVCG) and is of higher revenue.

rules in Section 6, but as one concrete example one of the rules we coin—WT nearest—selects the price vector in MRC(pWT) that minimizes Euclidean distance to pWT. WT nearest is the most direct generalization of the VCG nearest rule proposed by Day and Cramton (2012) that has been successfully used in spectrum auctions. In order to implement rules like WT nearest, we need algorithms for computing pWT. That is the topic of the next section (Section 5). We conclude this section with an example illustrating some of the key concepts introduced so far.

Example 4.4. Consider the CA with three items {a, b, c} and 10 single-minded bidders who submit the following bids: v1(a) = 20, v2(b) = 20, v3(c) = 20, v4(ab) = 28, v5(ac) = 26, v6(bc) = 23, v7(a) = 10, v8(b) = 10, v9(c) = 10, v10(abc) = 41 (this a slight modification of an example from Day and Cramton (2012)). Bidders 1, 2, and 3 win in the efficient allocation and their VCG prices are pVCG = (10, 10, 10). Say Θ1 = R≥0, Θ2 = {v2(b) ≥ 17}, Θ3 = {v3(c) ≥15}, so pWT = (10, 17, 15). The core constraints are given by {p1, p2, p3 ≥10, p1 + p2 ≥ 28, p1 + p3 ≥26, p2 + p3 ≥23, p1 + p2 + p3 ≥41}. The vanilla VCG-nearest point of Day and Cramton (2012) on MRC(pVCG) is (14, 14, 13) and the WT-nearest point on MRC(pWT) is (11, 17, 15). Figure 1 illustrates this example.

## 5 Computing Weakest-Type Prices

In this section we develop techniques to compute pWT, which are needed as a subroutine for computing the payments of our new core-selecting CAs. Balcan, Prasad, and Sandholm (2023) provide an initial theoretical investigation of WT computation, and our approaches builds upon their formulation, but we are the first to develop practical techniques and evaluate them via experiments. Appendix C contains the needed background on winner determination.

Recall Bi ⊆2M is the set of bundles bidder i bids on, so, for each S ∈Bi, bidder j submits her value vi(S) which is the maximum amount she would be willing to pay to win

17209

![Figure extracted from page 4](2026-AAAI-weakest-bidder-types-and-new-core-selecting-combinatorial-auctions/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

bundle S. For B = (B1,..., Bn), Γ(B) denotes the set of feasible selections of winning bids.

## 5.1 Constraint Generation for WT Computation

Let eBi denote the set of bundles Si such that vi(Si) is constrained by Θi(v−i) (so if Θi(v−i) is explicitly represented as a list of constraints on vi, eBi is the set of bundles Si such that vi(Si) appears in one of those constraints). WT computation for bidder i is the minmax optimization problem minevi∈Θi(v−i) maxS∈Γ(e Bi,B−i) evi(Si) + P j∈N\i vj(Sj), which can be expressed as a pure minimization problem by enumerating the set of feasible allocations Γ in its constraints and adding an auxiliary scalar variable γ to upper bound those constraints (adapting the formulation in Balcan, Prasad, and Sandholm (2023)). The resulting mathematical program is min

( γ: evi(Si) + P j̸=i vj(Sj) ≤γ ∀S ∈Γ(eBi, B−i)

evi ∈Θi(v−i)

)

.

In constraint generation, we initialize the program with some restricted set of constraints corresponding to feasible allocations Γ0 ⊆Γ(eBi, B−i) and solve to get a candidate solution bγ, bvi. Next, we find the most violated constraint not currently in Γ0 by computing w(bvi, v−i) and comparing to bγ. If bγ −w(bvi, v−i) < 0 we have found a (most) violated constraint, and we add the constraint corresponding to the violating allocation (bS1,..., bSn) that solves w(bv, v−i) to the restricted pricing LP (that is, Γ0 ←Γ0 ∪{ bS}). The program with the additional constraint is resolved and the process iterates. Otherwise if bγ −w(bvi, v−i) ≥0, all constraints of the unrestricted program are satisfied and so bγ, bvi is an optimal solution to the program and constraint generation terminates. (Experiments presented in Appendix D show that the above approach is superior to an alternate formulation based on Bikhchandani and Ostroy (2002).)

## 6 Experiments

We ran experiments to evaluate revenues, incentives, fairness, and computation of our new core-selecting CAs. We describe the main components of the setup below.

New and Old Core-Selecting CAs For a given CA instance we compare five different core-selecting payment rules (the three new CAs we introduce are bolded): Vanilla VCG nearest (Day and Cramton 2012) and Vanilla zero nearest (Erdil and Klemperer 2010) are the points p ∈ MRC(pVCG) that minimize ∥p −pVCG∥2

2, and ∥p∥2 2, respectively; WT nearest, Zero nearest, and VCG nearest are the points p ∈MRC(pWT) that minimize ∥p−pWT∥2

2, ∥p∥2 2, and ∥p −pVCG∥2

2, respectively. The WT-nearest rule is the most direct generalization of the vanilla VCG-nearest rule proposed by Day and Cramton (2012) and the zero-nearest rule is the most direct generalization of the vanilla zero-nearest rule proposed by Erdil and Klemperer (2010). Each of the five price vectors is computed via the quadratic programming and core-constraint generation techniques developed by Day and Cramton (2012), detailed in Appendix E.

Type Space Generation For each CA instance, we generated synthetic bidder type spaces Θi(v−i) determined by linear constraints (so the formulations for WT price computation from Section 5 are LPs). We generated Θi(v−i) independently for each bidder by generating K random linear constraints according to parameter β as follows. Each constraint is of the form P

Si∈Bi X(Si)c(Si)evi(Si) ≥α · P

Si∈Bi X(Si)c(Si)vi(Si) where evi(Si) are the variables representing bidder i’s bids, each X(Si) is an independent Bernoulli 0/1 random variable with success probability β, each c(Si) is drawn uniformly and independently from a decay distribution where c(Si) is initially equal to 1 and is repeatedly incremented with success probability 0.2 until failure, and α is drawn uniformly at random from [1/2, 1]. So, each constraint is guaranteed to be satisfied by the actual bids, and α determines how close to tight it is. Each of the K constraints per-bidder is generated this way independently.

We used the Combinatorial Auction Test Suite (CATS) (Leyton-Brown, Pearson, and Shoham 2000) version 2.1 to generate CA instances. Like Day and Raghavan (2007) and Day and Cramton (2012), we generated each instance from a randomly chosen distribution from the seven available distributions meant to model real-world CA applications. Code for our experiments was written in C++ and we used Gurobi version 12.0.1, limited to 8 threads, to solve all linear, integer, and quadratic programs. All computations were done on a 64-core machine with 16GB of RAM allocated for each CA instance.

Run-time Cost of WT Computation Table 1 records the effects of varying β ∈{0.2, 0.5, 0.8} (which controls the sparsity of type space constraints) on the run-time and number of CG iterations to compute pWT. We fixed the number of constraints K = 8, and for each β and each setting of goods in {64, 128} and bids in {250, 500} generated 100 instances (for a total of 400 instances). For these instances, the (geometric) mean run-time and worst-case run-time for pVCG were 2.7 seconds and 608.5 seconds, respectively.

β Run-time

(GM)

CG iters

(GM)

Run-time

(Max)

CG iters

(Max) 0.2 9.9 32.0 1515.1 424 0.5 13.2 56.4 1610.0 536 0.8 15.3 75.3 1896.0 567

**Table 1.** Run-times and constraint generation iterations for the BPS formulation as β varies, with # goods ∈{64, 128} and # bids ∈{250, 500}, averaged over 100 instances for each β and each setting of goods/bids.

The worst run-time for WT computation was thus roughly 3.1× the worst run-time for VCG computation. In general, increasing β, which increases the density of the type space constraints, increases the cost of WT computation. The additional run-time cost for finding a MRC(pWT) via coreconstraint generation was in fact less expensive than the run-time of core-constraint generation to find vanilla MRC points. The geometric mean runtime of the vanilla VCG nearest rule of Day and Cramton (2012) on the above instances was 1.7 seconds, with a worst case run-time of 523.9

17210

<!-- Page 6 -->

**Figure 2.** Incentive effects as type spaces convey more information (by varying the number of constraints K ∈ {1, 2, 4, 8, 16}, with # goods ∈{64, 128} and # bids ∈ {250, 500, 1000}, averaged over 100 instances for each K and each setting of goods/bids.

seconds. The geometric mean of our WT nearest rule on the same instances was 1.0 seconds, with a worst case run-time of 475.0 seconds. So, the main run-time cost of our new core-selecting CAs is in computing pWT.

Varying the number of type space constraints K did not have a significant impact on run-time nor number of constraint generation iterations for WT computation. Over all CA instances with number of goods in {64, 128} number of bids in {250, 500, 1000}, and β = 0.3, the geometric mean of run-times over all K was 19.7 seconds and the geometric mean of constraint generation iterations was 42.7. The worst-case VCG run-time was 19545.2 seconds and the worst-case WT run-time was 47718.0 seconds (2.4× larger than the worst VCG run-time). (The significantly larger runtime relative to the previous experiment varying β is due to the inclusion of the the CATS instances with 1000 bids.)

Incentive and Revenue Effects We now discuss the impact of type space information on the sum of bidders’ incentives to deviate from truthful bidding in a MRC(pWT)selecting CA. That is, we record the quantity P i∈W δp i where p is any one of our new pricing rules. By Theorem 4.2 this is equal to P i∈W pi −pWT i, that is, the difference in revenue between the MRC(pWT)-selecting rule and WT. We track this quantity as the number of type space constraints K per bidder varies in {1, 2, 4, 8, 16}, and compare it to the sum of bidders’ incentives to deviate in the vanilla unrestricted setting, which by Day and Milgrom (2010) is equal to the difference in revenue between a MRC(pVCG)-selecting rule and VCG. Each revenue difference recorded on the yaxis of Figure 2 is averaged over 100 CA instances each for goods in {64, 128} and bids in {250, 500, 1000}, for a total of 600 CA instances and a total of 600 × 5 = 3000 type space instances/WT computations. We fixed the constraint sparsity parameter β = 0.3. Figure 2 shows a clear trend that more information about the bidders (in the form of more type space constraints) yields better core incentives—and vastly better incentives than a vanilla MRC-selecting rule.

On the revenue front, Figure 3 shows the impact of more informative type spaces on the revenues generated

**Figure 3.** Revenue effects as type spaces convey more information (by varying the number of constraints K ∈ {1, 2, 4, 8, 16}, with # goods ∈{64, 128} and # bids ∈ {250, 500, 1000}, averaged over 100 instances for each K and each setting of goods/bids.

by our new core-selecting CAs (the experimental setup is the same as in the previous paragraph). The MRC(pWT)selecting rules are the clear winner, nearly closing half the gap between MRC revenue and the efficient social welfare when type spaces are determined by K = 16 constraints. While the MRC(pWT) revenue is not significantly larger than the MRC revenue for K ≤8, WT’s revenue is much larger than VCG’s, leading to much better incentives for the MRC(pWT) rule than the MRC rule in that regime despite similar revenues. So, a MRC(pWT)-selecting rule with revenue not much larger than a vanilla MRC(pVCG)-selecting rule can still provide significantly better incentives for bidders if ∥pWT∥1 is much larger than ∥pVCG∥1.

How Often is WT in The Core? We now report on the frequency with which pWT ∈Core. For CA instances with this property, all MRC(pWT)-selecting rules return pWT unmodified. Here, we record the frequency as the number of type space constraints K varies (the setup is the same as those in Figures 2 and 3). For K = 1, 2, 4, 8, 16, the frequencies with which pVCG /∈Core ∧pWT ∈Core were 2.00%, 3.02%, 3.36%, 3.69%, and 4.18%, respectively. Additionally, 1.17% of all instances had the property that both VCG and WT were in the core, both generating nonzero revenue An interesting phenomenon we observed was that 7.5% of instances had the property that all vanilla MRCselecting rules (like vanilla VCG-nearest of Day and Cramton (2012) and vanilla zero-nearest of Erdil and Klemperer (2010)) generated zero revenue. In other words, VCG generates zero revenue yet is in the core, which is a worse situation than the zero revenue cases described by Ausubel, Aperjis, and Baranov (2017) and Ausubel and Baranov (2023) that a vanilla core-selecting rule is unable to fix. WT is therefore indispensable to generate any revenue in these cases.

Who Shoulders the Core Burden? In Day and Cramton (2012), the impact of core pricing on the highest and lowest bidder is visualized. They show that on CATS instances with few bids (100 or less), their vanilla VCG nearest rule provides a more equitable apportionment of the core burden than the vanilla zero nearest rule of Erdil and Klemperer

17211

![Figure extracted from page 6](2026-AAAI-weakest-bidder-types-and-new-core-selecting-combinatorial-auctions/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-weakest-bidder-types-and-new-core-selecting-combinatorial-auctions/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

**Figure 4.** Core burdens shouldered by the lower and upper halves of bidders (measured by winning bid value). For the three MRC(pWT)-selecting rules, the left and right bars display the core burden split relative to WT and VCG, respectively. For the two vanilla MRC-selecting rules, the bar displays the core burden split relative to VCG.

(2010). That trend is less pronounced for the numbers of bids that we consider (250, 500, and 1000), and hence we present a slightly different visualization of the core burden split.

For each CA instance, and each core-pricing rule p, the core burden relative to WT (resp. VCG) of bidder i is the quantity (pi −pWT i)/(P i∈W pi −pWT i) (resp. (pi − pVCG i)/(P i∈W pi −pVCG i)). We sorted the bidders in ascending order of winning bid vi(S∗ i), and summed up the total core burdens for the lower and higher halves of bidders. Figure 4 displays the splitting of core burdens between the lower and higher halves, averaged across all instances with K = 8. For VCG-nearest, WT-nearest, and zero-nearest, the left bar displays core burdens relative to WT, with the solid black bottom representing the lower half of bidders and the gray top representing the upper half. The right bar displays core burdens relative to VCG, with the darker gray bottom representing the lower half of bidders and the lighter gray top representing the upper half. Only the core burden relative to VCG is displayed for the vanilla VCG nearest (Day and Cramton 2012) and vanilla zero nearest (Erdil and Klemperer 2010) since it would not make sense to compute core burdens relative to WT for these rules. Overall, there was not a significant difference between WT-nearest, zero-nearest, and VCG-nearest (this was also the case in Day and Cramton (2012) in their comparison of vanilla VCG-nearest and vanilla zero-nearest on CATS instances with more than 250 bids). VCG-nearest placed the least core burden and zeronearest placed the greatest core burden on the lower half of bidders, and all three rules are similar to the vanilla MRC rules in terms of core burdens relative to VCG. This fact provides further validation for our MRC(pWT)-selecting rules as they do not unfairly skew the core burden apportionment.

The previous discussion of equitable sharing of the core burden begets the question of whether there exist coreselecting rules that explicitly enforce how the core burden should be split. For example, is there a MRC(pWT)selecting CA p that enforces that each bidder pays a core burden in exact proportion to their winning bid, that is, (pi −pWT i)/(P i∈W pi −pWT i) ≥α · vi(S∗ i)/(P i∈W vi(S∗ i))

for some α? The answer is no due to the asymmetric information that can be conveyed about bidders by type spaces. For example, if Θ1(v−1) = {v1}, so pWT

1 = v1(S∗ i), IR constraints force p1 = pWT

1 for any core-selecting p. So in such situations a low bidder might be forced to shoulder a large majority of the core burden. A general rule of thumb here appears to be that the bidders with type spaces that convey the least information about them must pay most of the core burden. A formal investigation of this idea is an interesting direction for future research.

Conclusions and Future Research

We presented a new family of core-selecting CAs that take advantage of bidder information known to the auction designer through bidders’ type spaces. We showed that sufficiently informative type spaces can overcome the wellknown impossibility of core-selecting CAs, and gave a revised and generalized impossibility result that depends on whether or not the WT auction is in the core. We then showed that our new family of core-selecting CAs, defined by minimizing revenue on the section of the core above WT prices, minimizes the sum of bidders’ incentives to deviate from truthful bidding. On the computational front, we developed new constraint generation techniques for computing WT prices and evaluated our new core-selecting CAs on CATS instances, with synthetic generators for type space constraints. The revenue and incentive benefits of our new CAs, along with their manageable computational overhead, make them a useful addition to the auction design toolkit.

Future Research Perhaps the most pressing direction is the development of realistic type space generators by incorporating the specific details of the application domain. Our new CAs display promise on our synthetically-generated type spaces, but to understand their viability in real-world auctions one must develop detailed models of auctioneer knowledge. A more thorough investigation is needed for the design of MRC(pWT)-selecting rules. There might be other more economically meaningful rules than the ones we introduced in this paper. A computational study extending B¨unz, Lubin, and Seuken (2022) to MRC(pWT)-selecting rules is relevant here as well. A promising direction along this vein is to use machine learning to design the reference point, weights, and amplifications of the parameterized rules in B¨unz, Lubin, and Seuken (2022). Explicit equilibrium analysis in the style of Goeree and Lien (2016) and Ausubel and Baranov (2020) is important as well. Finally, an important direction within the research strand of mechanism design with predictions (Balcan, Prasad, and Sandholm 2023; Balkanski, Gkatzelis, and Tan 2024) is to relax the assumption that v ∈Θ, that is, that type spaces convey correct information about bidders. How can core-selecting CAs with strong incentive properties be designed using the techniques developed in this paper when type spaces can have errors? The techniques developed in Balcan, Prasad, and Sandholm (2023) in the general setting of multidimensional mechanism design will likely be useful here, and can also help shed light on better core selection in mechanisms beyond CAs.

17212

![Figure extracted from page 7](2026-AAAI-weakest-bidder-types-and-new-core-selecting-combinatorial-auctions/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This material is based on work supported by the NSF under grants IIS-1901403, CCF-1733556, and RI-2312342, the ARO under award W911NF2210266, the Vannevar Bush Faculty Fellowship ONR N00014-23-1-2876, and NIH award A240108S001.

## References

Ausubel, L.; Aperjis, C.; and Baranov, O. 2017. Market design and the FCC incentive auction. Presentation at the NBER Market Design Meeting. Ausubel, L.; and Baranov, O. 2020. Core-selecting auctions with incomplete information. International Journal of Game Theory, 49(1): 251–273. Ausubel, L.; and Baranov, O. 2023. The VCG Mechanism, the Core, and Assignment Stages in Auctions. Working paper. Ausubel, L.; and Cramton, P. 2011. Auction design for wind rights. Report to Bureau of Ocean Energy Management, Regulation and Enforcement, 1. Ausubel, L.; and Milgrom, P. 2002. Ascending auctions with Package Bidding. The BE Journal of Theoretical Economics, 1(1): 1–44. Ausubel, L.; and Milgrom, P. 2006. The Lovely but Lonely Vickrey Auction. In Cramton, P.; Shoham, Y.; and Steinberg, R., eds., Combinatorial Auctions, chapter 1. MIT Press. Balcan, M.-F.; Prasad, S.; and Sandholm, T. 2023. Bicriteria Multidimensional Mechanism Design with Side Information. In Conference on Neural Information Processing Systems (NeurIPS). Balcan, M.-F.; Prasad, S.; and Sandholm, T. 2025. Increasing Revenue in Efficient Combinatorial Auctions by Learning to Generate Artificial Competition. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), volume 39, 13572–13580. Balkanski, E.; Gkatzelis, V.; and Tan, X. 2024. Mechanism design with predictions: An annotated reading list. ACM SIGecom Exchanges, 21(1): 54–57. Batziou, E.; Bichler, M.; and Fichtl, M. 2022. Core-stability in assignment markets with financially constrained buyers. In Proceedings of the 23rd ACM Conference on Economics and Computation, 473–474. Bichler, M.; Shabalin, P.; and Wolf, J. 2013. Do coreselecting combinatorial clock auctions always lead to high efficiency? An experimental analysis of spectrum auction designs. Experimental Economics, 16: 511–545. Bichler, M.; and Waldherr, S. 2017. Core and pricing equilibria in combinatorial exchanges. Economics Letters, 157: 145–147. Bichler, M.; and Waldherr, S. 2022. Core pricing in combinatorial exchanges with financially constrained buyers: Computational hardness and algorithmic solutions. Operations Research, 70(1): 241–264. Bikhchandani, S.; de Vries, S.; Schummer, J.; and Vohra, R. V. 2001. Linear Programming and Vickrey Auctions. Draft.

Bikhchandani, S.; and Ostroy, J. M. 2002. The Package Assignment Model. Journal of Economic Theory, 107: 377– 406. Bosshard, V.; B¨unz, B.; Lubin, B.; and Seuken, S. 2017. Computing Bayes-nash equilibria in combinatorial auctions with continuous value and action spaces. In Proceedings of the 26th International Joint Conference on Artificial Intelligence (IJCAI), 119–127. B¨unz, B.; Lubin, B.; and Seuken, S. 2022. Designing coreselecting payment rules: A computational search approach. Information Systems Research, 33(4): 1157–1173. B¨unz, B.; Seuken, S.; and Lubin, B. 2015. A faster core constraint generation algorithm for combinatorial auctions. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 29. Clarke, E. H. 1971. Multipart pricing of public goods. Public Choice. Cramton, P. 2013. Spectrum auction design. Review of industrial organization, 42: 161–190. Cramton, P.; Gibbons, R.; and Klemperer, P. 1987. Dissolving a partnership efficiently. Econometrica: Journal of the Econometric Society, 615–632. Day, R.; and Cramton, P. 2012. Quadratic core-selecting payment rules for combinatorial auctions. Operations Research, 60(3): 588–603. Day, R.; and Milgrom, P. 2010. Optimal incentives in coreselecting auctions. Handbook of Market Design. Day, R.; and Raghavan, S. 2007. Fair Payments for Efficient Allocations in Public Sector Combinatorial Auctions. Management Science, 53(9): 1389–1406. de Vries, S.; Schummer, J.; and Vohra, R. V. 2007. On ascending Vickrey auctions for heterogeneous objects. Journal of Economic Theory, 132(1): 95–118. Erdil, A.; and Klemperer, P. 2010. A new payment rule for core-selecting package auctions. Journal of the European Economic Association, 8(2-3): 537–547. Goel, G.; Khani, M. R.; and Leme, R. P. 2015. Corecompetitive auctions. In Proceedings of the Sixteenth ACM Conference on Economics and Computation, 149–166. Goeree, J. K.; and Lien, Y. 2016. On the impossibility of core-selecting auctions. Theoretical economics, 11(1): 41– 52. Goetzendorff, A.; Bichler, M.; Shabalin, P.; and Day, R. W. 2015. Compact bid languages and core pricing in large multi-item auctions. Management Science, 61(7): 1684– 1703. Groves, T. 1973. Incentives in Teams. Econometrica. Hohner, G.; Rich, J.; Ng, E.; Reid, G.; Davenport, A. J.; Kalagnanam, J. R.; Lee, H. S.; and An, C. 2003. Combinatorial and Quantity-Discount Procurement Auctions Benefit Mars, Incorporated and Its Suppliers. Interfaces, 33(1): 23–35. Karaca, O.; and Kamgarpour, M. 2019. Core-selecting mechanisms in electricity markets. IEEE Transactions on Smart Grid, 11(3): 2604–2614.

17213

<!-- Page 9 -->

Klemperer, P. 2010. The product-mix auction: A new auction design for differentiated goods. Journal of the European Economic Association, 8(2-3): 526–536. Krishna, V.; and Perry, M. 1998. Efficient mechanism design. Available at SSRN 64934. Leyton-Brown, K.; Milgrom, P.; and Segal, I. 2017. Economics and computer science of a radio spectrum reallocation. Proceedings of the National Academy of Sciences, 114(28): 7202–7209. Leyton-Brown, K.; Pearson, M.; and Shoham, Y. 2000. Towards a universal test suite for combinatorial auction algorithms. In Proceedings of the 2nd ACM Cconference on Electronic Commerce (EC), 66–76. Lu, P.; Wan, Z.; and Zhang, J. 2024. Competitive auctions with imperfect predictions. In Proceedings of the 25th ACM Conference on Economics and Computation (EC), 1155– 1183. Markakis, E.; and Tsikiridis, A. 2019. On core-selecting and core-competitive mechanisms for binary single-parameter auctions. In International Conference on Web and Internet Economics (WINE), 271–285. Springer. Moor, D.; Seuken, S.; Grubenmann, T.; and Bernstein, A. 2016. Core-selecting payment rules for combinatorial auctions with uncertain availability of goods. In Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI), 424–432. Myerson, R.; and Satterthwaite, M. 1983. Efficient mechanisms for bilateral trading. Journal of Economic Theory, 28: 265–281. Niazadeh, R.; Hartline, J.; Immorlica, N.; Khani, M. R.; and Lucier, B. 2022. Fast core pricing for rich advertising auctions. Operations Research, 70(1): 223–240. Nisan, N. 2000. Bidding and allocation in combinatorial auctions. In Proceedings of the 2nd ACM Conference on Electronic Commerce (EC), 1–12. Othman, A.; and Sandholm, T. 2010. Envy quotes and the iterated core-selecting combinatorial auction. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 24, 829–835. Ott, M.; and Beck, M. 2013. Incentives for overbidding in minimum-revenue core-selecting auctions. Palacios-Huerta, I.; Parkes, D. C.; and Steinberg, R. 2024. Combinatorial auctions in practice. Journal of Economic Literature, 62(2): 517–553. Parkes, D. 2002. On indirect and direct implementations of core outcomes in combinatorial auctions. Parkes, D. C.; Kalagnanam, J.; and Eso, M. 2001. Achieving budget-balance with Vickrey-based payment schemes in exchanges. In Proceedings of the 17th International Joint Conference on Artificial Intelligence (IJCAI), 1161–1168. Prasad, S.; Balcan, M.-F.; and Sandholm, T. 2025. Revenue- Optimal Efficient Mechanism Design with General Type Spaces. arXiv preprint arXiv:2505.13687. Rostek, M.; and Yoder, N. 2015. Core Selection in Auctions and Exchanges. Working paper.

Rostek, M.; and Yoder, N. 2025. Reallocative auctions and core selection. Review of Economic Studies, rdaf065. Sandholm, T. 1999. An Algorithm for Optimal Winner Determination in Combinatorial Auctions. In Proceedings of the 16th International Joint Conference on Artificial Intelligence (IJCAI), 542–547. Stockholm, Sweden. Extended journal version published in Artificial Intelligence in 2002. Sandholm, T. 2013. Very-Large-Scale Generalized Combinatorial Multi-Attribute Auctions: Lessons from Conducting $60 Billion of Sourcing. In Neeman, Z.; Roth, A.; and Vulkan, N., eds., Handbook of Market Design. Oxford University Press. Sandholm, T.; Levine, D.; Concordia, M.; Martyn, P.; Hughes, R.; Jacobs, J.; and Begg, D. 2006. Changing the Game in Strategic Sourcing at Procter & Gamble: Expressive Competition Enabled by Optimization. Interfaces, 36(1): 55–68. Vickrey, W. 1961. Counterspeculation, Auctions, and Competitive Sealed Tenders. Journal of Finance.

17214
