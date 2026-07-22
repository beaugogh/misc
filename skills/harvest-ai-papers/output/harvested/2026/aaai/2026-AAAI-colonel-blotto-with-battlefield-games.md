---
title: "Colonel Blotto with Battlefield Games"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38702
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38702/42664
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Colonel Blotto with Battlefield Games

<!-- Page 1 -->

Colonel Blotto with Battlefield Games

Salam Afiouni1, Jakub ˇCern´y1, Chun Kai Ling2, Christian Kroer1

1Columbia University, USA 2National University of Singapore, Singapore sa4316@columbia.edu, jakub.cerny@columbia.edu, chunkail@nus.edu.sg, christian.kroer@columbia.edu

## Abstract

We study a class of two-player zero-sum Colonel Blotto games in which, after allocating soldiers across battlefields, players engage in (possibly distinct) normal-form games on each battlefield. Per-battlefield payoffs are parameterized by the soldier allocations. This generalizes the classical Blotto setting, where outcomes depend only on relative soldier allocations. We consider both discrete and continuous allocation models and examine two types of aggregate objectives: linear aggregation and worst-case battlefield value. For each setting, we analyze the existence and computability of Nash equilibrium. The general problem is not convex-concave, which limits the applicability of standard convex optimization techniques. However, we show that in several settings it is possible to reformulate the strategy space in a way where convexconcave structure is recovered. We evaluate the proposed methods on synthetic and real-world instances inspired by security applications, suggesting that our approaches scale well in practice.

Code — github.com/CoffeeAndConvexity/

ColonelBlottoWithBattlefieldGames Extended version — arxiv.org/abs/2511.06518

## Introduction

Colonel Blotto games are a classic game class used to model competitive resource allocation (Borel and Ville 1991; Roberson 2006; Kovenock and Roberson 2012b). Introduced by ´Emile Borel in the 1920s, Blotto games describe situations where players simultaneously allocate soldiers (resources) between battlefields, after which each battlefield is “won” by the player who allocated more soldiers to it. In the classic setting, each battlefield features a winnertakes-all property, creating an interesting game theoretic conundrum where both players would like to either just barely win or badly lose every battlefield. Blotto games and their extensions have been studied in many disciplines including computer and social sciences, with applications to politics (Che and Gale 2008; Laslier and Picard 2002; Myerson 1993), warfare (Gross and Wagner 1950; Shubik and Weber 1981), and behavioral science (Chowdhury, Kovenock, and Sheremeta 2013; Arad and Rubinstein 2012).

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

In this paper, we consider a variant of a two-player Colonel Blotto game played over n heterogeneous battlefields that features two levels of play. In our setting, each battlefield i ∈[n] also comprises a zero-sum “subgame” Gi, the structure and payoffs of which depends on the soldiers each player allocated to i. This captures many real-world settings where players follow-up with individual battlefieldlevel strategies. For instance, a political party first allocates money between state elections, after which, each individual state decides how they should spend that money. Likewise in warfare, the tactics at a battlefield level play a huge part in the success of the overarching conflict; these battlefield level tactics are themselves games played at a lower level, the outcomes of which depend greatly on the number of soldiers assigned. In more abstract terms, players first simultaneously determine a soldier assignment over battlefields (unobserved by the opponent), then play, in every battlefield, a subgame whose payoff matrix is parametrized by the player’s soldier allocation on that battlefield. We refer to this game as the “two-level Blotto game”. By convention, Player 1 (resp. Player 2) seeks to minimize (resp. maximize) the payoff. Accordingly, we often refer to Player 1 (resp. Player 2) as the minimizing (resp. maximizing) player. We analyze three dimensions of the proposed two-level Blotto games. First, we study discrete versus continuous soldier types; the former implies that individual soldiers cannot be subdivided, though players are allowed to adopt randomization. Second, we study two ways of aggregating payoffs from individual battlefields – either with sum or min aggregators. Both these axes have been extensively explored in the Blotto literature (see, e.g, Roberson (2011); Washburn (2011), or Vu (2020)). Third, we study two strategic settings: the two-sided case, where both players allocate soldiers across battlefields and the simpler one-sided case, in which only the maximizing player is allowed soldier allocations. The one-sided setting is motivated by security applications, where only the “defending” player has soldiers to allocate, and provides stronger guarantees of equilibrium existence and computational tractability.

Our contributions are as follows. First, for every combination of soldier type (discrete vs. continuous), aggregator (sum vs. min), and strategic setting (two-sided vs. onesided), we address the following: (i) does a Nash equilibrium exist, and (ii) are the max-min and min-max strategies well-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16612

<!-- Page 2 -->

Setting NE Mx/Mn exist.

Discrete

Two-sided sum ✓ ✓ Two-sided min ✗ ✓ One-sided min ✓ ✓

Continuous

Two-sided sum ✗ ✓∗

One-sided sum ✗ ✓∗

One-sided sum (L) ✓ ✓ Two-sided min ✗ ✓∗

One-sided min ✓∗ ✓∗

One-sided min (L) ✓ ✓

**Table 1.** Existence of NE and max-min strategies in different settings of discrete and continuous Blotto games. ∗holds only when the utility u is continuous in the soldiers allocation. (L) means that battlefield utilities are linear in the maximizing player’s soldier allocation.

defined and attained? 1 Our results are summarized in Table 1. Second, for each of the cases where an equilibrium exists, we provide algorithms for solving them. In most cases, these problems reduce to linear programs, though in one special case the problem reduces to a quasiconcave problems. Third, we empirically evaluate these algorithms on synthetic data, demonstrating that these algorithms are usable.

Related work. Due to space constraints, we only provide a small sampling of relevant work. Computationally, Ahmadinejad et al. (2019) provided an LP based approach for separable battlefields (similar to one of our settings) to solve Blotto games but using the ellipsoid method; their method extends to continuous Lotto games (Hart 2008; Dziubi´nski 2013), which admit infinite action spaces, though they do not have subgames. Behnezhad et al. (2023) avoid the impractical ellipsoid algorithm and propose a practical LP formulation based on layered graphs, and is very closely related to one of our approaches. Kvasov (2007) and Roberson and Kvasov (2012) study a non-constant (zero) sum variant of Blotto games, while Hortala-Vallve and Llorente- Saguer (2012) study pure strategy equilibria in such variants. Kovenock and Roberson (2012a) study a team variant where a single player plays against a coalition of 2 other players while Boix-Adser`a, Edelman, and Jayanti (2020) study more general multiplayer settings. Stephenson (2024) study payoffs which depend on a function of allocated soldiers per player. Powell (2009) and Hausken (2012) consider sequential variants of Blotto games.

## Preliminaries

Let n > 0 be the number of battlefields, and m1, m2 be the total number of soldiers available to Players 1 and 2. Let Zj denote the set of all possible soldier assignments zj for player j ∈{1, 2}, where zj = (zj

1,..., zj n) is a vector speci-

1A positive answer to both questions implies a valid minimax theorem in that regime. Moreover, any existence result in the twosided model implies the one-sided case by fixing the minimizer’s allocations to zero.

fying soldier distributions across the n battlefields, subject to the budget constraint Pn i=1 zj i = mj. When soldiers are discrete, we let zj = kj ∈Zn

≥0, and when soldiers are continuous, zj = σj ∈Rn

≥0. We denote by Kj and Σj the sets of all possible soldier assignments for player j in the discrete and continuous case, respectively. Each subgame Gi is a finite normal-form zero-sum game defined as a tuple (A1 i, A2 i, ui), where Aj i denotes the action space of player j ∈{1, 2} in battlefield i, and ui: A1 i × A2 i × Z1 × Z2 →R denotes the payoff in that battlefield that Player 2 (resp. Player 1) seeks to maximize (resp. minimize). For each battlefield i ∈[n], the payoff ui is a function of both the number of soldiers players allocated to that battlefield and the actions they play in the subgame Gi. We denote by αj i ∈Aj i the action player j plays on battlefield i. For battlefield i and any allocation profile (z1 i, z2 i), we let v∗ i (z1 i, z2 i) be the equilibrium value of subgame Gi when player j allocates zj i soldiers to it. To compute the overall utility in the two-level Blotto game, we consider two aggregation functions: 1) the sum of the expected utilities across battlefields U = P i∈[n] E[ui(.)], and 2) the minimum of the expected utilities in all battlefields U = mini∈[n] E[ui(.)].

Across the variants of the two-level Blotto game we analyze, players choose mixed strategies over their subgame actions. The use of randomization at the allocation stage depends on whether the model is discrete or continuous. In the discrete case, the allocating players (the maximizing player in the one-sided case and both players in the two-sided case) randomize over integer allocation vectors. In the continuous case, players could also mix over allocations; yet we show that in some settings, equilibrium can be guaranteed even when players commit to a deterministic (pure) allocation. This motivates our focus on pure strategies at the allocation stage, which offer simpler representation and tractable computation. The various strategy representations are summarized in the appendix. Finally, a strategy pair (x∗, y∗) ∈X × Y is a Nash equilibrium (NE) if U(x∗, y) ≤U(x∗, y∗) ≤U(x, y∗) for all x ∈X, y ∈Y, where X and Y are the strategy spaces of Player 1 and 2, respectively.

Minimax theorems play a central role in our analysis, particularly in establishing equilibrium existence. In fact, the existence of a minimax theorem for a setting is equivalent to equilibrium existence (Proposition 1). We rely on Sion’s minimax theorem (Sion 1958) in several of our proofs and also examine its applicability across various settings. In the setting where only Player 2 allocates a continuum of soldiers across battlefields and individual subgame payoffs are aggregated via the minimum operator, we apply a variant known as the Kneser-Fan minimax theorem (Sion 1958).

Proposition 1. Let u: X ×Y →R be an arbitrary function on arbitrary sets X, Y. Then maxx∈X infy∈Y u(x, y) = miny∈Y supx∈X u(x, y) if and only if there exists a NE in a two-player zero-sum game with action spaces X and Y and utility function u.

Theorem 1 (Sion’s minimax theorem). Let X and Y be nonempty convex and compact subsets of two linear topolog-

16613

<!-- Page 3 -->

ical spaces, and f: X × Y →R be a function that is upper semicontinuous and quasiconcave in the first variable and lower semicontinuous and quasiconvex in the second. Then miny∈Y maxx∈X f(x, y) = maxx∈X miny∈Y f(x, y).

Definition 1 (Concavelike, Convexlike, and Concave-convexlike). Consider two spaces X and Y, and let f be a function f on X × Y. We say f is concavelike in X if for every x1, x2 ∈X and 0 ≤t ≤1, there is an x ∈X such that tf(x1, y) + (1 −t)f(x2, y) ≤f(x, y) ∀y ∈Y, and f is convexlike in Y if for every y1, y2 ∈Y and 0 ≤t ≤1, there is a y ∈Y such that tf(x, y1) + (1 −t)f(x, y2) ≥ f(x, y) ∀x ∈X. Finally, f is called concave-convexlike if it is concavelike in X and convexlike in Y.

Theorem 2 (Kneser-Fan minimax theorem). Let X be compact, Y any space, and f a function on X × Y that is concave-convexlike. If f(x, y) is upper semicontinuous in x for each y, then supx∈X infy∈Y f = infy∈Y supx∈X f.

Colonel Blotto with Discrete Soldiers In the discrete two-level Blotto game, players allocate a finite number of indivisible soldiers across battlefields and randomize over both soldier assignments and subgame strategies. Let kj = (kj

1, · · ·, kj n) ∈Kj be player j’s discrete allocation vector. Then the payoff in battlefield i is given by ui(α1 i, α2 i, k1 i, k2 i). In our two-level formulation, each player j adopts a two-level strategy composed of 1) a probability distribution γj over soldier assignments, and 2) for each battlefield i and each soldier count kj i, a mixed strategy δj i,kj i over actions αj i ∈Aj i in subgame Gi. The action set in each battlefield is independent of the number of soldiers allocated to that battlefield (this may be relaxed easily). Since the number of possible assignments is finite, each subgame can be viewed as a Bayesian game in which player j has types {0,..., mj}, each occurring with probability equal to the chance that the player assigns that number of soldiers to the battlefield under γj.

## 3.1 Sum Aggregator The overall utility under the sum aggregator is given by

U(δ, γ) =

X i∈[n]

X k1∈K1

X k2∈K2 γ1(k1) γ2(k2)

×

X α1 i ∈A1 i

X α2 i ∈A2 i δ1 i,k1 i (α1 i) δ2 i,k2 i (α2 i) ui(α1 i, α2 i, k1 i, k2 i).

In this setting, we can formulate the two-level Blotto game as a linear program. For each battlefield i, and given a fixed distribution over k1 i and k2 i, the optimal subgame strategy corresponds to solving a Bayesian extensive-form game where nature randomizes over the (m1 + 1) · (m2 + 1) possible types. We model this randomization in two sequential phases – first determining Player 1’s probabilities, then Player 2’s – thereby inducing a product distribution over the joint types. By translating the type assignment into two stages, we can assign the first phase to Player 1 and the second phase to Player 2 while retaining perfect recall.

More precisely, for player j ∈{1, 2}, we define a flow polytope Γj with two types of variables. First, the variable xj i,kj i,αj i denotes the probability that player j allocates kj i sol- diers to battlefield i and plays action αj i in subgame Gi. Second, the flow variable hj i,a,b denotes the flow through battlefield i for player j: it represents the transition from a remaining soldiers to b remaining soldiers after allocating a −b soldiers to battlefield i. The polytope Γj is defined by the following constraints:

Γj = hj i,a,b, xj i,kj i,αj i ∈[0, 1] such that:

hj

0,mj,mj = 1, hj n−1,0,0 = 1, hj

0,a,b = 0 ∀a, b ∈[0, mj], (a, b)̸ = (mj, mj), mj X a=c hj i−1,a,c = c X b=0 hj i,c,b ∀i ∈[1, n −1], c ∈[0, mj],

X αj i ∈Aj i xj i,kj i,αj i =

X kj i ≤r≤mj hj i,r,r−kj i ∀i ∈[1, n −1], kj i ∈[0, mj]

.

By encoding strategies with a flow polytope, we obtain a polynomial-size representation of strategies that is payoff equivalent to the original strategy space ∆(Kj) × Q i∈[n] ∆(Aj i). This flow polytope is a generalization of the layered graph approach of Behnezhad et al. (2023), with the addition of subgames. Theorem 3 (Kuhn’s theorem under two-sided sum aggregator). Consider a discrete two-level Blotto game with sum aggregator, and suppose γj ∈ ∆(Kj), δj i ∈ ∆(Aj i), j ∈ {1, 2}. Then the overall payoff is bilinear in the strategies x1 and x2. Specifically, U = P i

P α1 i

P α2 i

P k1 i

P k2 i ui(α1 i, α2 i, k1 i, k2 i) · x1 i,k1 i,α1 i · x2 i,k2 i,α2 i.

Theorem 3 implies that rather than optimizing over ∆(Kj) × Q i∈[n] ∆(Aj i), we can optimize over a flow polytope Γj. Computing a NE may be expressed as a bilinear saddle point problem maxx2∈Γ2 minx1∈Γ1 U. Since Γ1 and Γ2 are compact and convex sets, Sion’s minimax theorem holds. Then, by Proposition 1, we have: Corollary 1. Under the sum-aggregator, the discrete twolevel Blotto game admits a NE.

We propose two methods to solve the bilinear saddle point problem. The first uses a common trick of taking the dual of the inner optimization problem, converting the min-max problem into a single minimization problem that can be solved by a linear program (Behnezhad et al. 2023). For brevity, details of the LP are deferred to the appendix. The second method is based on online learning and self-play. In the classic setting of zero-sum matrix games, each player’s strategy space is the probability simplex, and it is known that the recommendations given by the online learners converge

16614

<!-- Page 4 -->

on average to a NE (Hart and Mas-Colell 2000; Roughgarden 2010). This is readily adapted to imperfect information extensive-form games by defining regret minimizers over the treeplex (Zinkevich et al. 2007). In our setting, the regret minimizers are over the flow polytopes Γ1 and Γ2, which may be done using scaled extensions (Farina et al. 2019) or kernel-based approaches (Farina et al. 2022; Takimoto and Warmuth 2003). For brevity, we defer details to the appendix, but remark that the regret minimizers require O(n · maxi,j{mj(mj + |Aj i|)}) space (i.e., linear in the size of the flow polytope), O(n·maxi,j{mj(mj +|Aj i|)}+ maxi{m1 i m2 i |A1 i ||A2 i |}) time-per-iteration and incurs total regret at a rate of O(

√

T), depending on the implementation details. Our methods readily extend to settings where each subgame is a perfect recall extensive-form game. This is done by reformulating the strategy space in each Gi by the treeplex (Von Stengel 1996). Our results here extend trivially to the one-sided case.

Proposition 2. Under the sum aggregator, a NE of the discrete two-level Blotto game is polynomial-time computable.

Remark 1. Note that all results extend directly to the onesided setting, in which the minimizing player does not participate in the soldier allocation.

## 3.2 Min Aggregator

When the overall utility is defined as the minimum across all battlefields, the aggregate utility is given by

U(δ, γ) = min i∈[n]

X k1∈K1

X k2∈K2 γ1(k1)γ2(k2)

×

X α1 i ∈A1 i

X α2 i ∈A2 i δ1 i,k1 i (α1 i)δ2 i,k2 i (α2 i)ui(α1 i, α2 i, k1 i, k2 i)

.

Unlike with the sum aggregator, when both players allocate soldiers to battlefields, the two-level Blotto game may not admit a NE even when battlefield utilities are continuous.

Theorem 4. Consider a two-sided discrete two-level Blotto game under the min aggregator. Even if all battlefield utilities are continuous, a NE may not exist. Nevertheless, both the max-min and min-max values are well-defined and are attained.

This motivates our study of the one-sided model, in which only the maximizing player allocates soldiers to battlefields, then both players engage in independent zero-sum subgames. This variant captures common security scenarios where for example, only the defender allocates resources, and guarantees equilibrium existence while admitting efficient computation. In this setting, the total utility is

U(δ, γ) = min i∈[n]

X k2∈K2 γ2(k2)

×

X α1 i ∈A1 i

X α2 i ∈A2 i δ1 i (α1 i)δ2 i,k2 i (α2 i)ui(α1 i, α2 i, k2 i)

.

This formulation admits a tractable NE.

Theorem 5 (Kuhn’s theorem under one-sided min aggregator). Consider a one-sided discrete two-level Blotto game with min aggregator, and suppose γ2 ∈∆(K2), δj i ∈ ∆(Aj i), j ∈ {1, 2}. Then the overall payoff is convex and bilinear in p and x2, where p ∈ ∆(n) is a convexification variable and x2 is the treeplex strategy for Player 2. Specifically, U = minp

P i

P α2 i

P k2 i pi Eα1 i ∼δ1 i [ui(α1 i, α2 i, k2 i)]x2 i,k2 i,α2 i.

Using the bilinear formulation from Theorem 5 we can now express the min-max problem as minδ1 maxx2 minp

P i

P α2 i

P k2 i pix2 i,k2 i,α2 i E[ui(α1 i, α2 i, k2 i)]. Exploiting the bilinear structure of the payoff, we invoke Sion’s minimax theorem to interchange the inner maximization and minimization operators. By then combining the two minimizations, we define a sequence-form strategy over a two-level game for Player 1, in which he first chooses a battlefield and then plays an action in it, using y1(i, α1 i) to denote the product pi · δ1 i (α1 i). Under this reformulation, we recover the game’s max-min structure, which yields the following result. Theorem 6. Consider a one-sided discrete two-level Blotto game with min aggregator. Then the minimax theorem holds. Specifically, minδ1 maxδ2,γ2 mini E[ui(α1 i, α2 i, k2 i)] = maxδ2,γ2 minδ1 mini E[ui(α1 i, α2 i, k2 i)]. The flow polytope representation of Player 2’s strategy introduces a set of constraints captured by the polytope Γ2. Analogously, the sequence-form product representation of Player 1’s strategy induces the constraints defined over the following polytope

P =

   

   y1(i) ≥0 y1(i, α1 i) ≥0 y1(∅) = 1, P i∈[n]

y1(i) = y1(∅), P α1 i ∈A1 i y1(i, α1 i) = y1(i).

   

  

Therefore, a NE can be computed by solving a LP over the polytopes Γ2 and P, obtained by dualizing either player’s best-response program. Since both Γ2 and P have polynomial-size representations, we have: Corollary 2. In the one-sided model, a NE of the two-level Blotto game with min aggregator exists and can be computed in polynomial time.

Colonel Blotto with Continuous Soldiers In the continuous two-level Blotto game, we focus on equilibria where players choose deterministic (pure) soldier allocations and may randomize over subgame strategies. Unlike the discrete setting where equilibrium existence requires randomization at the resource allocation level, we show that when soldier allocations are continuous, deterministic allocations suffice to guarantee the existence of equilibrium in some cases. This yields several practical benefits: such equilibria admit exact representation, are computationally tractable, and, in applications such as security, can be easier to deploy when randomization at the allocation level is impractical or undesirable. We view this setting as a natural starting point for analyzing randomized allocation strategies, whose equilibria may lack finite representations and

16615

<!-- Page 5 -->

are more difficult to characterize. We leave the analysis of such strategies to future work.

In this setting, players allocate any real-valued fraction of soldiers to each battlefield. Let σj = (σj

1, · · ·, σj n) ∈Σj be player j’s continuous allocation vector. Then the payoff in battlefield i is ui(α1 i, α2 i, σ1 i, σ2 i). Considering both the sum and min aggregators, we show that, in the two-sided setting, a partially pure Nash equilibrium (PPNE) – i.e. one in which players use pure soldier allocation strategies and mixed subgame strategies – may fail to exist under either aggregator, even when the utility functions in all battlefields are continuous in the allocation variables. Theorem 7. Consider a two-sided continuous two-level Blotto game under the sum or min aggregator. Even if battlefield utilities are continuous in σ, a PPNE may not exist.

We proceed to analyze the one-sided setting. We show that under the sum aggregator, a PPNE may still fail to exist, whereas under the min aggregator, a PPNE is guaranteed to exist. We explain this divergence at the end of the section.

## 4.1 Sum Aggregator

In the continuous two-sided model, each player j deterministically selects a soldier allocation σj ∈ Σj, and employs a mixed strategy δj i,σj i over actions αj i ∈ Aj i in subgame Gi. We can write the overall in the two-sided model as: U(δ, σ) = P i

P α1 i

P α2 i δ1 i,σ1 i (α1 i)δ2 i,σ2 i (α2 i)ui(α1 i, α2 i, σ1 i, σ2 i)

.

The total payoff is non-convex non-concave in the minimizing and maximizing player’s strategies, respectively. This remains true even in the one-sided allocation model. Consequently, a PPNE may still fail to exist, even when each ui is continuous in the soldier allocation variables. Proposition 3. Even in the one-sided case, a continuous two-level Blotto with continuous battlefield utilities may not admit a PPNE under the sum aggregator. The max-min and min-max values are attained but do not coincide.

Although equilibrium existence cannot be guaranteed in the one-sided model under general continuous utilities, we show that if each battlefield payoff is linear in the maximizing player’s allocation, namely ui σ2 i

= ci σ2 i, ci > 0, a PPNE is guaranteed to exist. In fact, with linear battlefield utilities, the game can be cast as a bilinear saddle point problem by absorbing the soldier allocation variable σ2 and the subgame distribution over actions δ2 into a single sequence-form variable y2 σ2 via the treeplex construction. The product variable y2 σ2 is defined over a polytope Q that is represented by the following constraints:

Q =

   

   y2 σ2 i (i) ≥0 y2 σ2 i (i, α2 i) ≥0 y2(∅) = m2, P i∈[n]

y2 σ2 i (i) = y2(∅), P α2 i ∈A2 i y2 σ2 i (i, α2 i) = y2 σ2 i (i).

   

  

The resulting payoff is bilinear in the variables y2 σ2 and δ1, which allows us to invoke the minimax theorem and guarantee the existence of a PPNE.

Theorem 8. Consider a one-sided continuous two-level Blotto game with sum aggregator, and suppose σ2 ∈Σ2, δj i ∈∆(Aj i), j ∈{1, 2}. Assume that in each battlefield, the utility is linear in the maximizing player’s allocation, i.e. ui = ci · σ2 i for some constant ci > 0. Then the minimax theorem applies.

It follows from Theorem 8 that the continuous two-level Blotto game with sum aggregator and linear utilities admits an equilibrium, which can be computed by solving a linear program defined over the polytope Q. Since Q has a polynomial size representation, we have:

Corollary 3. When battlefield utilities are linear in the maximizing player’s allocation, a PPNE of the one-sided continuous two-level Blotto game with sum aggregator exists and can be computed in polynomial time.

## 4.2 Min aggregator

In the two-sided model, when the overall payoff is defined as the minimum of the expected utilities across battlefields, it can be written as U(δ, σ) = mini∈[n]

P α1 i

P α2 i δ1 i,σ1 i (α1 i)δ2 i,σ2 i (α2 i)ui(α1 i, α2 i, σ1 i, σ2 i)

.

Since a PPNE may fail to exist in the two-sided setting (Theorem 7), we focus on the one-sided model. We show that equilibrium non-existence arises only if the utility function in every battlefield i is discontinuous in σ2 i.

Theorem 9. Consider a one-sided continuous two-level Blotto game with min aggregator. Then a PPNE may not exist when battlefield utilities are discontinuous.

However, when the payoff in each battlefield is a continuous function of the soldier allocation, the continuous twolevel Blotto game with min aggregator admits a saddle point in the one-sided formulation: the max-min and min-max values coincide and are attained, so a PPNE exists. We establish this by invoking the Kneser-Fan minimax theorem. Suppose that only Player 2 allocates soldiers to battlefields, and both players employ mixed strategies to engage in the battlefield subgames. Then, the min-max formulation of the continuous two-level Blotto game is:

min δ1 max δ2,σ2 min i∈[n] E ui(α1 i, α2 i, σ2 i)

= min δ1 max δ2,σ2 min i∈[n]

X α1 i

X α2 i δ1 i (α1 i) δ2 i,σ2 i (α2 i)ui(α1 i, α2 i, σ2 i).

Ideally, we would like to invoke Sion’s minimax theorem to interchange the outer minimization and maximization, thereby recovering the equivalent max-min formulation of the game and establishing the minimax identity. However, the inner objective function cannot be made simultaneously quasiconvex in the minimizing player’s strategy and quasiconcave in the maximizing player’s strategy under any reordering of the operators and/or regrouping of the variables. Consequently, Sion’s conditions are not met. Therefore, we appeal to the Kneser-Fan minimax theorem (Theorem 2). Taking the dual of the inner minimization problem over i ∈[n], allows us to obtain the following result:

16616

<!-- Page 6 -->

Theorem 10. Consider a one-sided continuous two-level Blotto game with continuous battlefield utilities. Then the minimax theorem holds. Specifically, minδ1 maxδ2,σ2 mini E[ui(α1 i, α2 i, σ2 i)] = maxδ2,σ2 minδ1 mini E[ui(α1 i, α2 i, σ2 i)].

Remark 2. This approach does not extend to any of the other settings we analyzed in the continuous domain, which is consistent with the non-existence results established in Theorem 7 and Proposition 3. In particular, (1) in the one-sided continuous setting with sum aggregator, the payoff fails to be concavelike in the maximizing player’s strategy, which immediately extends to the sum-aggregated two-sided setting; whereas (2) in the two-sided continuous setting with min aggregator, convexlikeness of the payoff in the minimizing player’s strategy cannot be guaranteed.

For the special case where battlefield utilities are linear in σ2, we obtain a sequence-form representation of the strategies of both players defined over the polytopes P and Q. Hence, we have the following theorem:

Theorem 11. Consider a one-sided continuous two-level Blotto game under the min aggregator, and suppose σ2 ∈ Σ2, δj i ∈∆(Aj i), j ∈{1, 2}. Assume that in every battlefield, the utility is linear in the maximizing player’s allocation, i.e. ui = ci · σ2 i for some constant ci > 0. Then we can compute a PPNE of the game by solving a linear program.

Corollary 4. When battlefield utilities are linear in the soldier allocation of the maximizing player, the one-sided continuous two-level Blotto game with min aggregator admits a PPNE that can be computed in polynomial time.

Computing the max-min strategy In this paragraph, we focus on computing the max-min strategy for Player 2 in the one-sided continuous two-level Blotto game with min aggregator. We show that it can be reformulated as a maximization over the minimum Nash value across battlefields and hence it can be computed using a subgradient ascent algorithm.

Proposition 4. Consider a one-sided continuous twolevel Blotto game with min aggregator, and suppose σ2 ∈Σ2, δj i ∈∆(Aj i), j ∈{1, 2}. Then the maxmin problem can be formulated as a maximization problem over the minimum Nash value across battlefields. Specifically, maxδ2,σ2 minδ1 mini E[ui(α1 i, α2 i, σ2)] = maxσ2 mini∈[n] v∗ i (σ2 i).

Let V (σ2):= mini v∗ i (σ2) denote the objective function of this maximization problem. We show that this function is quasiconcave. Notice that, contrary to the sum, the min aggregator preserves quasiconvcavity. Hence, to achieve overall quasiconcavity of V (σ2), it suffices to have that the individual terms v∗ i (σ) are quasiconcave.

Lemma 1. If for each battlefield i ∈[n], ui(α1 i, α2 i, σ2) is increasing in σ2 i for all α1 i ∈A1 i and α2 i ∈A2 i, then the aggregate Nash value function V (σ2) is quasiconcave.

Since V (σ2) is quasiconcave on the compact convex set of soldier assignments Σ2, then finding the optimal σ2∗= arg maxσ2∈Σ2 V (σ2) reduces to maximizing a quasiconcave function over a convex set. Moreover, under the assumption that each battlefield utility function ui(σ2) is Lipschitz continuous on the soldiers assignments simplex Σ2, not only does a global maximizer σ2∗exist, but one can actually compute it using a simple projected subgradient-ascent (PSA) method. Specifically, at each iteration t, we select a subgradient gt ∈∂V (σ2 t), a step size ηt > 0 and perform the update σ2 t+1 = PΣ2 σ2 t +ηt gt

, where PΣ2 denotes the projection onto Player 2’s soldiers’ simplex. For completeness, the full pseudocode is given in the appendix. Next, we derive a closed-form description of the subdifferential ∂V (σ2 t), which enables efficient computation of each gt. Proposition 5. Consider the two-player zero-sum subgame Gi on battlefield i. Suppose that for every pure profile (α1 i, α2 i) ∈A1 i × A2 i, the payoff ui(α1 i, α2 i, σ2 i) is Lipschitz continuous in σ2 i. Let (δ1∗ i, δ2∗ i) be any NE of Gi at a given σ2 i. Then the vector gi = P α1 i ∈A1 i

P α2 i ∈A2 i δ1∗ i (α1 i) δ2∗ i (α2 i) zα1 i,α2 i, zα1 i,α2 i ∈ ∂σ2 i ui(α1 i, α2 i, σ2 i), is a subgradient of v∗ i (σ2).

Corollary 5. Under the assumptions of Proposition 5, V is Lipschitz on Σ2 and its subdifferentials ∂V (σ2) lie in Conv n

∂v∗ i (σ2): i ∈arg minj∈[n] v∗ j (σ2)

o

.

Finally, to obtain the optimal soldier allocation σ2∗for Player 2, we run the PSA algorithm. Each iteration t requires a subgradient gt ∈∂V (σ2 t). By Corollary 5, it suffices to pick any active battlefield i∗∈arg mini v∗ i (σ2 t) and use its subgradient. Proposition 5 then provides a concrete “Nash subgradient” for battlefield i∗: choose for each action pair (α1 i, α2 i) a subgradient zα1 i,α2 i ∈∂σ2 i∗ui∗(α1 i, α2 i, σ2 i∗), and set gt = P α1 i,α2 i δ1∗ i∗(α1 i) δ2∗ i∗(α2 i) zα1 i,α2 i ∈∂v∗ i∗(σ2 t). This gt is exactly the update direction used in the PSA algorithm.

Convergence Guarantees By Lemma 1 and Corollary 5, our aggregate Nash-value function V is quasiconcave and Lipschitz continuous on the soldiers simplex. Hence, the projected subgradient-ascent iterates {σ2 t } satisfy the general basic-inequality conditions (H1)-(H2) of (Hu, Li, and Yu 2020), which guarantee global convergence of any sequence with a suitably chosen step size rule. Moreover, they establish in Theorems 3.3-3.5 that, under an additional weak sharp minima of H¨olderian order assumption and upperbounded noise, such a sequence converges at a linear rate when the H¨older exponent equals 1. In our maximization context, this translates into a weak sharp maxima condition: Definition 2 (Weak Sharp Maxima). There exist constants ϵ > 0, p ∈(0, 1] such that ∀σ2 ∈Σ2, V (σ2∗) −V (σ2) ≥ ϵ ∥σ2 −σ2∗∥p, where σ2∗is the unique maximizer of V.

When battlefield utilities are affine functions of σ2, the induced Nash value v∗ i (σ2 i) remains an affine function of σ2 i. It follows that the aggregate function V = mini v∗ i is concave on the soldiers simplex Σ2. Applying the subgradient inequality at the maximizer σ2∗∈arg maxΣ2 V then yields the following sharp-max error bound for V. Proposition 6. If every battlefield utility is affine in Player 2’s soldier allocation, i.e. ui(σ2) = ci σ2 i + di with ci >

16617

<!-- Page 7 -->

0 10 20 30 Time [s]

0.88

0.90

0.92

0.94

0.96

0.98

Normalized objective value

Random affine utilities size = 20 size = 30 size = 40

0 200 400 600 800 Time [s]

0.90

0.92

0.94

0.96

0.98

Normalized objective value

Random quadratic utilities size = 20 size = 30 size = 40

0 25 50 75 100 125 150 Time [s]

0.309

0.310

0.311

0.312

0.313

0.314

0.315

0.316

Objective value

Security-inspired utilities

**Figure 1.** Convergence of the PSA algorithm in the one-sided min-aggregated setting with affine (left), quadratic (middle), and security-inspired (right) battlefield utilities.

0, then V satisfies the weak sharp-maxima condition with exponent p = 1.

It follows immediately from Theorem 3.3 of (Hu, Li, and Yu 2020) that the subgradient ascent iterates converge linearly to the optimal σ2∗.

## 5 Empirical Evaluation Discrete two-sided with sum-aggregator

We first evaluate in the most basic setting of discrete soldiers under the sum aggregator (Section 3.1). We consider (i) the LP-based approach similar to Behnezhad et al. (2023) and (ii) our approach based on online learning. The i ∈[n] battlefield has value i, such that winning (resp. losing) it gives +i (resp. −i) reward. For consistency, we re-normalize values of battlefields such that they sum to 1. The i-th battlefield is won by player 1 with probability k1 i /(k1 i + k2 i), with a random winner selected if no soldiers are allocated. For each subgame, players decide whether to double their stakes. If just one player doubles, payoffs and losses for that battlefield are doubled; if both players double, they are quadrupled.

We report running times for both methods. For the former, we use the default configuration for Gurobi (Gurobi Optimization, LLC 2024). For the latter, we adopt the Regret Matching-Plus (RM+) algorithm (Tammelin 2014) and construct Γj using scaled extensions (Farina et al. 2019). We declare convergence when the saddle-point gap is less than 0.002. More details on experimental setup are reported in the appendix. The results are shown in Table 2. We observe that when the game is small, the LP finds the NE easily. However, as the size of the game grows, LPs slow down dramatically and online learning approaches begin to shine. In fact, for larger instances Gurobi’s sometimes fails to converge because of numerical issues or simply going out-of-memory.2 In contrast, methods based on online learning scale better.

Continuous one-sided with min-aggregator We evaluate the PSA algorithm on randomly generated and security-

2In our experiments, it is unclear if Barrier or Primal/Dual simplexes are superior. For larger games, it would appear as though simplex performs better in practice, while barrier tends to lead to non-convergence.

n m1 m2 |Γ1|, |Γ2| LP [s] RM+ [s]

30 100 50 85, 49 91 0.02 35 125 70 281k, 92k 4.8 · 103 121 40 150 100 1M, 262k 5.4 · 103 525 50 200 100 12.6M, 2.05M NA (> 2.6 · 104) 9.5 · 103

**Table 2.** Runtime for discrete soldiers with sum aggregators.

inspired battlefield utilities. For random instances, we consider (i) affine utilities ui(σ2) = ci σ2 + di, and (ii) quadratic utilities ui(σ2) = bi (σ2)2 + ci σ2 + di, with bi, ci, di ∼Uniform[0, 100]. Player 2 is given 20 soldiers to allocate across 5 battlefields. We vary players’ action spaces in {20, 30, 40} and generate 10 independent instances per game size. In the first 2 plots of Figure 1, we show the aggregate normalized value ¯V t and its standard error SE(t) = p st ℓ, st = 1 ℓ−1

Pℓ k=1

V t k −¯V t 2, across ℓ= 10 instances, where V t k denotes the normalized objective value on instance k at iteration t. Under both utility functions, all three sizes reach near-optimality with very low dispersion. Next, we consider a real-world scenario inspired by security applications. We model a one-sided min-aggregated continuous two-level Blotto game where Player 2 allocates 10 soldiers across three battlefield, each featuring a two-player zero-sum security subgame where Player 2 is the defender’s and Player 1 the attacker. We follow the framework of (Krever et al. 2025). More details on the experimental setup are provided in the appendix. The rightmost plot of Figure 1 confirms the algorithm’s robustness in this practical setting.

## 6 Conclusion

In this paper, we introduced and analyzed a two-level variant of the Colonel Blotto game, where players allocate resources across battlefields then engage in parametrized subgames. We studied multiple modeling dimensions – soldier types, payoff aggregation methods, and strategic settings – and established equilibrium existence, provided solution algorithms, and validated their practicality through experiments.

16618

<!-- Page 8 -->

## Acknowledgments

This research was supported by the Office of Naval Research awards N00014-22-1-2530 and N00014-23-1-2374, the National Science Foundation awards IIS-2147361 and IIS-2238960, the Ministry of Education, Singapore, under the Academic Research Fund Tier 1 (FY2025) and by the National University of Singapore, under the Start-Up Grant Scheme. We thank Noah Krever for help with setting up the security-inspired subgames.

## References

Ahmadinejad, A.; Dehghani, S.; Hajiaghayi, M.; Lucier, B.; Mahini, H.; and Seddighin, S. 2019. From duels to battlefields: Computing equilibria of blotto and other games. Mathematics of Operations Research, 44(4): 1304–1325. Arad, A.; and Rubinstein, A. 2012. Multi-dimensional iterative reasoning in action: The case of the Colonel Blotto game. Journal of Economic Behavior & Organization, 84(2): 571–585. Behnezhad, S.; Dehghani, S.; Derakhshan, M.; Hajiaghayi, M.; and Seddighin, S. 2023. Fast and simple solutions of Blotto games. Operations Research, 71(2): 506–516. Boix-Adser`a, E.; Edelman, B. L.; and Jayanti, S. 2020. The multiplayer colonel blotto game. In Proceedings of the 21st ACM Conference on Economics and Computation, 47–48. Borel, E.; and Ville, J. 1991. Application de la th´eorie des probabilit´es aux jeux de hasard, original edition by Gauthier-Villars, Paris, 1938; reprinted at the end of Th´eorie math´ematique du bridg´ea la port´ee de tous, by E. Borel & A. Ch´eron, Editions Jacques Gabay, Paris. Che, Y.-K.; and Gale, I. L. 2008. Caps on political lobbying. In 40 Years of Research on Rent Seeking 2, 337–345. Springer. Chowdhury, S. M.; Kovenock, D.; and Sheremeta, R. M. 2013. An experimental investigation of Colonel Blotto games. Economic Theory, 52: 833–861. Dziubi´nski, M. 2013. Non-symmetric discrete General Lotto games. International Journal of Game Theory, 42: 801–833. Farina, G.; Lee, C.-W.; Luo, H.; and Kroer, C. 2022. Kernelized multiplicative weights for 0/1-polyhedral games: Bridging the gap between learning in extensive-form and normal-form games. In International Conference on Machine Learning, 6337–6357. PMLR. Farina, G.; Ling, C. K.; Fang, F.; and Sandholm, T. 2019. Efficient regret minimization algorithm for extensive-form correlated equilibrium. Advances in Neural Information Processing Systems, 32. Gross, O.; and Wagner, R. 1950. A continuous Colonel Blotto game. RAND Corporation. Research Memorandum, 408. Gurobi Optimization, LLC. 2024. Gurobi Optimizer Reference Manual. https://www.gurobi.com. Hart, S. 2008. Discrete colonel blotto and general lotto games. International Journal of Game Theory, 36(3-4): 441–460.

Hart, S.; and Mas-Colell, A. 2000. A simple adaptive procedure leading to correlated equilibrium. Econometrica, 68(5): 1127–1150. Hausken, K. 2012. On the impossibility of deterrence in sequential colonel blotto games. International Game Theory Review, 14(02): 1250011. Hortala-Vallve, R.; and Llorente-Saguer, A. 2012. Pure strategy Nash equilibria in non-zero sum colonel Blotto games. International Journal of Game Theory, 41: 331–343. Hu, Y.; Li, J.; and Yu, C. K. W. 2020. Convergence rates of subgradient methods for quasi-convex optimization problems. Computational Optimization and Applications, 77(1): 183–212. Kovenock, D.; and Roberson, B. 2012a. Coalitional Colonel Blotto games with application to the economics of alliances. Journal of Public Economic Theory, 14(4): 653–676. Kovenock, D.; and Roberson, B. 2012b. Conflicts with multiple battlefields. Krever, N.; ˇCern´y, J.; Blanchard, M.; and Kroer, C. 2025. GUARD: Constructing Realistic Two-Player Matrix and Security Games for Benchmarking Game-Theoretic Algorithms. arXiv:2505.14547. Kvasov, D. 2007. Contests with limited resources. Journal of Economic Theory, 136(1): 738–748. Laslier, J.-F.; and Picard, N. 2002. Distributive politics and electoral competition. Journal of Economic Theory, 103(1): 106–130. Myerson, R. B. 1993. Incentives to cultivate favored minorities under alternative electoral systems. American Political Science Review, 87(4): 856–869. Powell, R. 2009. Sequential, nonzero-sum “Blotto”: Allocating defensive resources prior to attack. Games and Economic Behavior, 67(2): 611–615. Roberson, B. 2006. The colonel blotto game. Economic Theory, 29(1): 1–24. Roberson, B. 2011. Allocation Games. John Wiley, Ltd. Roberson, B.; and Kvasov, D. 2012. The non-constant-sum Colonel Blotto game. Economic Theory, 51: 397–433. Roughgarden, T. 2010. Algorithmic game theory. Communications of the ACM, 53(7): 78–86. Shubik, M.; and Weber, R. J. 1981. Systems defense games: Colonel Blotto, command and control. Naval Research Logistics Quarterly, 28(2): 281–287. Sion, M. 1958. On general minimax theorems. Pacific Journal of Mathematics, 8(1): 171 – 176. Stephenson, D. 2024. Multi-battle contests over complementary battlefields. Review of Economic Design, 1–16. Takimoto, E.; and Warmuth, M. K. 2003. Path kernels and multiplicative updates. Journal of Machine Learning Research, 4(Oct): 773–818. Tammelin, O. 2014. Solving large imperfect information games using CFR+. arXiv preprint arXiv:1407.5042. Von Stengel, B. 1996. Efficient computation of behavior strategies. Games and Economic Behavior, 14(2): 220–246.

16619

<!-- Page 9 -->

Vu, D. Q. 2020. Models and solutions of strategic resource allocation problems: Approximate equilibrium and online learning in blotto games. Ph.D. thesis, Sorbonne Universites, UPMC University of Paris 6. Washburn, A. R. 2011. TPZS Applications: Blotto Games. John Wiley, Ltd. Zinkevich, M.; Johanson, M.; Bowling, M.; and Piccione, C. 2007. Regret minimization in games with incomplete information. Advances in neural information processing systems, 20.

16620
