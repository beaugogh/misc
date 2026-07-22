---
title: "Pacing Equilibria in Second-Price Auctions with Few Buyers"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38782
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38782/42744
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Pacing Equilibria in Second-Price Auctions with Few Buyers

<!-- Page 1 -->

Pacing Equilibria in Second-Price Auctions with Few Buyers

Yonglei Yan1, Zihe Wang2, Zhengyang Liu1*

1Beijing Institute of Technology 2Renmin University of China yanyonglei@bit.edu.cn, wang.zihe@ruc.edu.cn, zhengyang@bit.edu.cn

## Abstract

We present a polynomial-time algorithm for exactly computing second-price pacing equilibria (SPPE) in auction markets with a constant number of buyers. SPPE plays a central role in modern advertising auctions; however, computing or even approximating it is PPAD-hard in general. To overcome this computational barrier in the restricted setting, we adopt the cell-decomposition method. Specifically, we partition the solution space into polynomially many cells, each defined by hyperplanes corresponding to a fixed ordering of buyers’ scaled valuations across goods. Within each cell, the equilibrium computation reduces to solving a constant number of linear programs. Notably, our algorithm can also efficiently identify equilibria that optimize key objectives such as revenue or social welfare. To the best of our knowledge, this is the first algorithm that efficiently computes an exact SPPE for a simple and natural class of second-price pacing games.

## Introduction

Online advertising markets face a foundational challenge in auction design under budget constraints. As demonstrated by Aggarwal et al. (2024), advertisers must participate in sequences of second-price auctions while adhering to fixed overall budgets. Traditional second-price auction theory, reliant on quasi-linear utilities and unlimited budgets, fails to capture these real-world constraints. To bridge this gap, pacing mechanisms have become central to modern ad platforms (e.g., ad exchanges), where multiplicative pacing multipliers αi ∈[0, 1] scale bids to respect budget limits. This adjustment (with the yield of effective offers αivij) ensures that long-term expenditure remains within budgets Bi. It gives rise to the concept of Second-Price Pacing Equilibria (SPPE), a stable state where buyers’ multiplier choices, platform allocations, and pricing rules converge.

The seminal work of Conitzer et al. (2022) formalized SPPE, proving existence under general conditions and characterizing key properties, including potential nonuniqueness and efficiency losses relative to social optima. This framework has since underpinned diverse learning algorithms for revenue and utility optimization (Balseiro and Gur 2019; Wang et al. 2023; Balseiro et al. 2024; Lucier

*Zhengyang Liu is the corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

et al. 2024). Despite these advances, the computational complexity of finding SPPE has remained unresolved. Recent breakthroughs establish its intrinsic hardness: Chen, Kroer, and Kumar (2023) proved PPAD-completeness for computing approximate pacing equilibria with inverse-polynomial precision. Very recently, Chen and Li (2025) established strong inapproximability by showing that computing γapproximate pacing equilibria is PPAD-hard for any γ < 1/3. This impossibility result holds even in highly sparse settings where each bidder values only four goods, mirroring a similar phenomenon known for Nash equilibria (Chen, Deng, and Teng 2006; Liu and Sheng 2018; Liu, Li, and Deng 2021).

These negative results imply that efficient exact computation — or even high-precision approximation — of SPPE is likely intractable in large markets with many buyers and goods, at least in the worst case. This leads to an interesting open question: Under what practical constraints can SPPE be computed efficiently?

We give an affirmative answer to this question by focusing on markets with a constant number of buyers but an arbitrarily large number of goods.

Theorem 1. Given any instance of second-price pacing game with a constant number c of buyers, Algorithm 1 computes a second-price pacing equilibrium in polynomial time.

Such settings capture real-world scenarios, such as auctions involving a few major advertising agencies or niche markets dominated by a small number of key players.

Technical Overview

A pacing equilibrium consists of both allocations and pacing multipliers. Solving for it via programming-based methods requires introducing variables to capture both components. However, a single, universal formulation is unlikely to suffice due to the discrete structure imposed by the “no unnecessary pacing” condition (condition (d) in Definition 1). To address this challenge, we adopt the cell-decomposition method. This approach has been successfully applied in related domains, such as computing market equilibria (Devanur and Kannan 2008) and solving optimal multidimensional pricing problems (Chen et al. 2018).

Concretely, given a market with m goods and c buyers, we partition the pacing multiplier space (α1,..., αc) ∈(0, 1]c

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17302

<!-- Page 2 -->

via hyperplane arrangements. We establish that O(mc2) hyperplanes, induced by comparing scaled valuations αivij across buyers and goods, divide the space into O(mc−1) cells where the weak ordering of buyers’ scaled valuations remains invariant for all goods. Within each cell, we enumerate all 2c budget-activity cases that distinguish between the constraints 0 < αi < 1 and αi = 1 for each buyer i ∈[c]. Given each case, we reformulate equilibrium conditions as a linear programming through two critical steps. First, we introduce auxiliary variables yij = xijαi to linearize the payment terms xijpj(α) that arises when multiple buyers tie. Second, for each set I ⊆[c] of buyers who share some good j, we derive linear constraints of the form P i∈I yijvij = αi′vi′j, where i′ is any buyer in the set I, ensuring consistency of valuations among tied buyers. Budget exhaustion constraints are simultaneously preserved via transformed equalities. The resulting system of linear inequalities can then be efficiently solved using linear programming.

The algorithm runs in polynomial time due to two key properties: there are O(mc−1) cells, and each cell admits O(1) budget-activity cases. For each case, the corresponding linear system can be solved in poly(m) time. As a result, the overall complexity is O(poly(m)). We thus obtain a polynomial-time algorithm for computing a pacing equilibrium in budget-constrained second-price auctions with a constant number of buyers.

Related Works

Recent research by Aggarwal et al. (2024) highlighted that advertisers in online advertising markets must participate in a sequence of second-price auctions under a fixed total budget. The seminal work of Conitzer et al. (2022) formally introduced the concept of Second-Price Pacing Equilibria and established its existence under general conditions. Subsequent studies, including those by Balseiro and Gur (2019); Wang et al. (2023); Balseiro et al. (2024); Lucier et al. (2024), have shown that SPPE has been extensively utilized in the development of various learning algorithms.

For the complexity results, Chen, Kroer, and Kumar (2023) further proved that computing approximate pacing equilibria to inverse-polynomial precision is PPADcomplete. Very recently, Chen and Li (2025) established a strong inapproximability result for pacing equilibria in second-price auctions, showing that for any constant γ < 1/3, computing a γ-approximate pacing equilibrium is PPAD-hard. The above results suggest that efficient algorithms for general instances are unlikely to exist. To the best of our knowledge, this work is the first positive result for pacing equilibrium computation in second-price auctions. In contrast, Borgs et al. (2007); Chen, Kroer, and Kumar (2021) proposed efficient computation methods for pacing and throttling equilibria in the regime of first-price auctions.

## Preliminaries

In this section, we will introduce the necessary definitions and notation.

Second-Price Pacing Games

A second-price pacing game G = (n, m, (vij), (Bi)) involves n buyers and m indivisible goods. Each buyer has a specific value to each good, with vij denoting the value that buyer i places on good j, and Bi representing the budget of buyer i. In the game, each buyer i chooses a pacing multiplier αi, and submits a bid of αivij for each good j.

Each good is sold via a second-price auction. We denote by hj(α) = maxi αivij the highest bid for good j, and pj(α) the second-highest bid. The good is given to the highest-bidding buyers, who pay the second-highest bid pj(α). In case of a tie, i.e., when multiple buyers submit the highest bid, the good is allocated fractionally: each highest buyer receives a non-zero share of good j at the unit price pj(α). For indivisible goods, such fractional allocation can be interpreted as the probability that a buyer wins the good. We also denote by xij the probability that buyer i gets good j.

We characterize the stable state of this game with the following solution concept.

Definition 1 (Pacing Equilibrium). We say (α, x) with α = (αi) ∈[0, 1]n, x = (xij) ∈[0, 1]nm, and P i∈[n] xij ≤ 1, ∀j ∈[m] is a pacing equilibrium of a second-price pacing game G = (n, m, (vij), (Bi)) if

(a) xij > 0 implies αivij = hj(α); (b) hj(α) > 0 implies P i∈[n] xij = 1; (c) P j∈[m] xijpj(α) ≤Bi; (d) P j∈[m] xijpj(α) < Bi implies αi = 1.

For the conditions, (a) indicates that only the highestbidding buyers can own the good; (b) ensures that any good with a strictly positive bid needs to be entirely allocated; (c) enforces the feasibility of budget constraints; and (d) imposes that no buyer is subject to excessive or unnecessary pacing. Buyers with surplus budget will bid truthfully, as this is a dominant strategy in the second-price auction.

In their work, Conitzer et al. (2022) demonstrated that a pacing equilibrium always exists in the context of secondprice pacing games.

Theorem 2 (Conitzer et al. (2022)). Any second-price pacing game admits a pacing equilibrium.

Notation

For each good j ∈[m], we need to compare the values (α1v1j, α2v2j,..., αnvnj). We define a partition of the good set according to the induced weak orderings of these values.

Let Σn denote the set of all weak orderings over the set [n], and for each σ ∈Σn, define:

Sσ:= {j ∈[m]: (α1v1j,..., αnvnj) induces order σ}.

Then the ordered tuple of sets (Sσ)σ∈Σn forms a partition of the good set. For example, when n = 3, Σ3 contains 13 distinct weak orderings such as (1 > 2 > 3), (1 = 2 > 3),..., (1 = 2 = 3), corresponding to the following sets, respectively: S1>2>3 = {j ∈[m]: α1v1j > α2v2j >

17303

<!-- Page 3 -->

α3v3j},..., S1=2>3 = {j ∈[m]: α1v1j = α2v2j > α3v3j}.

The ordered tuple (Sσ) consists of all subsets Sσ corresponding to preference orderings over the buyers. For example, when n = 3, we have (Sσ) = (S1>2>3, S1=2>3,..., S1=2=3).

The number of such orderings depends only on the number of buyers. When n = c, this number remains constant. One can obtain all possible orderings by partitioning the buyers into groups—using = within each group and > between groups

We further group the good partitions based on which buyers achieve the maximum scaled valuation for each good. For every non-empty subset I ⊆[n], define:

TI:= {j ∈[m]: argmaxi(αivij) = I}, that is

TI =

[ σ∈Σn, argmax(σ)=I

Sσ.

Given an instance G = (n, m, (vij), (Bi)), the ordered tuple of sets (TI)∅̸=I⊆[n] forms a partition of the good set [m] into 2n −1 parts, each corresponding to a distinct (and disjoint) subset of buyers simultaneously achieving the maximum bid on good j. For example, when n = 3, by definition we have that T{1} = S1>2>3 ∪S1>2=3 ∪S1>3>2 and T{1,2} = S1=2>3.

Note that when αi = 0, buyer i effectively places a bid of zero on all goods, which is equivalent to not participating in the auction. In this case, the setting reduces to an auction with n −1 rather than n buyers. Without loss of generality, we assume that all αi’s are strictly positive.

For ease of exposition in the subsequent analysis, we introduce the following notation: We denote by rij:= αi/αj the ratio between αi and αj, and yij:= xijαi the product of xij and αi.

It is also worth noting that, in a pacing equilibrium, assigning a good with a highest bid of zero still satisfies the definition of equilibrium. This is because the highest bid for such a good is zero, implying that its associated price pj(α) is also zero. As a result, allocating this good does not affect any budget constraints. Therefore, for ease of exposition, we assume that hj(α) is strictly positive for every good.

Warm-up: when n = 2 To facilitate a clearer exposition, we first restrict our attention to the case with only two buyers. We partition the set of goods into the following three parts according to α ∈(0, 1]2:

T{1} = S1>2 = {j: α1v1j > α2v2j},

T{2} = S1<2 = {j: α1v1j < α2v2j},

T{1,2} = S1=2 = {j: α1v1j = α2v2j}.

While the total number of possible ordered tuples (Sσ) may appear to be exponential in the number of goods m, it can in fact be bounded by a linear function of m. Lemma 3. When n = 2 and all the values vij’s are given, the number of ordered tuples (Sσ), due to α ∈(0, 1]2, is bounded by O(m).

Proof. To determine the ordered tuple (Sσ), it is necessary to compare α1v1j and α2v2j for each good j ∈[m]. This can be reduced to compare the ratio r12 = α1/α2 with v2j/v1j. Since all values of v2j/v1j are given as part of the input, the problem becomes identifying, for a given r12 ∈(0, ∞), which goods satisfy v2j/v1j > r12 (thus belonging to S1<2), which satisfy v2j/v1j = r12 (belonging to S1=2), and which satisfy v2j/v1j < r12 (belonging to S1>2).

It is important to note that if v1j = 0 while v2j > 0, the ratio v2j v1j is considered to be ∞. Moreover, the case where v1j = 0 and v2j = 0 cannot occur, since we require that the highest bid hj(α) for each good be strictly positive.

Without loss of generality, we can assume that the goods are sorted in ascending order based on their value ratios v2j/v1j. Geometrically, these goods can be interpreted as m distinct points on the real line, where each point corresponds to a ratio v2j/v1j. It follows that the number of distinct cells of (Sσ) is at most 2m + 1: m cells arise when r12 is exactly equal to some v2j/v1j for j ∈[m], and the other m+1 ones correspond to the cases where r12 lies strictly between adjacent ratios (or in the unbounded intervals (0, minj v2j/v1j) and (maxj v2j/v1j, ∞)).

Therefore, the total number of possible cells of (Sσ) is O(m).

So we can enumerate all the possible cells with the above result.

Given a specific ordered tuple (Sσ), the expression of pj(α) corresponding to each good can be explicitly determined.

In this case where n = 2, pj(α) = min{α1v1j, α2v2j}, and we can get that ∀j ∈T{1}, pj(α) = α2v2j and ∀j ∈ T{2}, pj(α) = α1v1j, then we get that buyer 1 needs to pay P j∈T{1} pj(α) + P j∈T{1,2} x1jα1v1j, and buyer 2 needs to pay P j∈T{2} pj(α) + P j∈T{1,2} x2jα2v2j. Note that for each good j ∈T{1,2}, we have α1v1j = α2v2j and x1j + x2j = 1.

Subsequently, for each ordered tuple (Sσ), we further categorize the problem into four cases based on the relative magnitudes of α1, α2 and 1. For each case, we construct a corresponding system of inequalities to facilitate the solution.

Case 1: α1 = 1, α2 = 1. In this case, we have the following:                    

                  

X j∈T{1}

v2j +

X j∈T{1,2}

x1jv1j ≤B1

X j∈T{2}

v1j +

X j∈T{1,2}

x2jv2j ≤B2 v1j = v2j, ∀j ∈T{1,2} x1j + x2j = 1, ∀j ∈T{1,2} 0 < xij < 1, ∀i ∈{1, 2}, ∀j ∈T{1,2} v1j > v2j, ∀j ∈S1>2 v1j = v2j, ∀j ∈S1=2 v1j < v2j, ∀j ∈S1<2

17304

<!-- Page 4 -->

Standard linear programming techniques, such as the ellipsoid method proposed by Khachiyan (1979) or that of Karmarkar (1984), can be directly applied to solve this system. If a feasible solution exists, it corresponds to a pacing equilibrium.

Case 2: α1 < 1, α2 = 1. Buyer 1 exhausts her budget, which gives us the equation

X j∈T{1}

v2j +

X j∈T{1,2}

x1jα1v1j = B1.

Note that although the term x1jα1v1j is quadratic in the variables x1j and α1, for goods in the set T{1,2}, we have the relation α2v2j = α1v1j. This allows us to rewrite the term as x1jα2v2j, thereby reducing it to a linear expression.

Then we get the system below:

                     

                    

X j∈T{1}

v2j +

X j∈T{1,2}

x1jv2j = B1

X j∈T{2}

α1v1j +

X j∈T{1,2}

x2jv2j ≤B2 α1v1j = v2j, ∀j ∈T{1,2} x1j + x2j = 1, ∀j ∈T{1,2} 0 < xij < 1, ∀i ∈{1, 2}, ∀j ∈T{1,2} 0 < α1 < 1 α1v1j > v2j, ∀j ∈S1>2 α1v1j = v2j, ∀j ∈S1=2 α1v1j < v2j, ∀j ∈S1<2 The existence of a solution to this linear system implies the existence of a pacing equilibrium in the second-price pacing game.

Case 3: α1 = 1, α2 < 1. Analogously, this case is almost identical to Case 2.

Case 4: α1 < 1, α2 < 1. It is similar to the previous situations that the following system holds:

                       

                      

X j∈T{1}

α2v2j +

X j∈T{1,2}

x1jα1v1j = B1

X j∈T{2}

α1v1j +

X j∈T{1,2}

x2jα2v2j = B2 α1v1j = α2v2j, ∀j ∈T{1,2} x1j + x2j = 1, ∀j ∈T{1,2} 0 < xij < 1, ∀i ∈{1, 2}, ∀j ∈T{1,2} 0 < α1 < 1 0 < α2 < 1 α1v1j > α2v2j, ∀j ∈S1>2 α1v1j = α2v2j, ∀j ∈S1=2 α1v1j < α2v2j, ∀j ∈S1<2

Since both x1jα1v1j and x2jα2v2j are quadratic terms. The observations that x1j + x2j = 1 and α1v1j = α2v2j can help us simplify the equation system. Recall that y1j = x1jα1 and y2j = x2jα2, we have

X j∈T{1}

α2v2j +

X j∈T{1,2}

y1jv1j = B1,

X j∈T{2}

α1v1j +

X j∈T{1,2}

y2jv2j = B2 and we use α1v1j = α2v2j, then we get: α1/α2 = v2j/v1j, ∀j ∈T{1,2}.

Note that for any good j ∈T{1,2}, we have x1j + x2j = 1, which is equivalent to y1j/α1 + y2j/α2 = 1. Using the equation above, this yields the identity:

y1j + v2j v1j y2j = α1, that is, y1jv1j + y2jv2j = α1v1j, which means that when all buyers in I submit identical scaled bids for good j, under the second-price auction mechanism, we have that the total payment for good j equals any individual buyer’s bid.

Hence we have:

                       

                      

X j∈T{1}

α2v2j +

X j∈T{1,2}

y1jv1j = B1

X j∈T{2}

α1v1j +

X j∈T{1,2}

y2jv2j = B2 α1v1j = α2v2j, ∀j ∈T{1,2} y1jv1j + y2jv2j = α1v1j, ∀j ∈T{1,2} 0 < yij < αi, ∀i ∈{1, 2}, ∀j ∈T{1,2} 0 < α1 < 1 0 < α2 < 1 α1v1j > α2v2j, ∀j ∈S1>2 α1v1j = α2v2j, ∀j ∈S1=2 α1v1j < α2v2j, ∀j ∈S1<2

This is a system of linear inequalities involving α1, α2, and y1j, y2j, ∀j ∈[m]. If this system has a solution, then we can obtain a pacing equilibrium.

Time Complexity. The number of ordered tuples (Sσ) is O(m), and the number of cases is 4, which is a constant. Then we get that the number of linear systems is O(m) and we can solve any linear system in polynomial time, so the algorithm can run in polynomial time.

General Result

Things become complicate when we think about the general constant n = c.

Pseudocode for the Algorithm. For general instances where n = c, we propose the following algorithm:

17305

<!-- Page 5 -->

## Algorithm

1: Finding a pacing equilibrium in second-price auctions with constant buyers.

Input: Set of buyers B = {1,..., c}, goods G = {1,..., m}, budget Bi for each i ∈B and valuation matrix (vij). Output: Pacing multipliers (αi) and allocations (xij).

1: Enumerate all ordered tuples (Sσ) 2: for each ordered tuple (Sσ) do 3: Construct (TI) corresponding to the (Sσ) 4: // Enumerate binary vectors of dimension c 5: for each binary vector b ∈{0, 1}c do 6: for each bi in b do 7: if bi = 1 then 8: Add constraint αi = 1 9: else 10: Add constraint 0 < αi < 1 11: end if 12: end for 13: Construct linear systems and solve the system to find (αi) and (xij). 14: if there is a feasible solution satisfying all constraints then 15: return the corresponding (αi) and (xij). 16: end if 17: end for 18: end for

The construction of the linear system involved in the algorithm will be detailed in the proof of Theorem 4. We can show that this algorithm computes a pacing equilibrium in polynomial time. Theorem 4 (Main Result). Given any instance of secondprice pacing game with a constant number c of buyers, Algorithm 1 computes a second-price pacing equilibrium in polynomial time.

Before proving our main result, we can also prove that the number of distinct ordered tuples (Sσ) is bounded by a polynomial of m. Lemma 5. Given all vij and n = c, which is a constant, the number of distinct ordered tuple (Sσ), over α ∈(0, 1]c is bounded by a polynomial in m.

Proof. For the case where n = c, we must compare αivij and αi′vi′j for all i, i′ and all j. To facilitate this, consider the tuple (α1/αc, α2/αc,..., αc−1/αc), denoted as (r1c, r2c,..., r(c−1)c).

When i̸ = c and i′ = c, comparing αivij with αi′vi′j is equivalent to comparing ric · vij with vcj. When i̸ = c and i′̸ = c, the comparison between αivij and αi′vi′j becomes equivalent to comparing ric · vij with ri′c · vi′j.

Thus, for each good j, we consider hyperplanes in the (c −1)-dimensional space of the form ricvij = vcj and ricvij = ri′cvi′j. Each good j induces (c −1) axis-aligned hyperplanes and (c−1)(c−2)/2 origin-passing hyperplanes, resulting in a total of m ·

(c −1) + (c −1)(c −2)

2

= mc(c −1)

2 hyperplanes overall.

By Theorem 6, we obtain that these hyperplanes partition the (c−1)-dimensional space into at most O(mc−1) distinct cells. Here, we confine our attention to the upper bound of O(mc−1), which remains valid even when the hyperplanes are not in general position.

Theorem 6 (Zaslavsky (1975); Orlik and Terao (1992)). Let A be a collection of k affine hyperplanes in general position in Rd. Then the number of j-dimensional faces (0 ≤j ≤d) induced by the arrangement is given by fj = k d −j j X i=0 k −d + j i

.

In particular, the number of d-dimensional cells (i.e., the connected components of Rd \ S A) is fd = d X i=0 k i

.

Now we are ready to prove our main result.

Proof of Theorem 4. By Lemma 5, we have that the ordered tuple (Sσ) is polynomial in m. Thus, it is sufficient to show that for each specific (Sσ), a pacing equilibrium can be computed in polynomial time.

Given a specific ordered tuple (Sσ), the expression of pj(α) can be explicitly determined for each good j. In particular, if good j is included in set T{i}, then xij = 1, which implies that the corresponding function pj(α) is linear in α.

For each (Sσ), we can decompose it into 2c cases and conduct a case-by-case analysis to facilitate the solution.

The 2c possible cases can be broadly classified into three categories: (i) all αi = 1, (ii) all αi < 1, and (iii) the remaining 2c −2 mixed cases, where some but not all αi’s equal 1. We analyze each of these categories separately.

Case 1: αi = 1 for each i ∈[c].

                                  

                                 

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI xijαivij ≤Bi, ∀i ∈[c]

αivij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i, i′ ∈I, ∀j ∈TI X i∈I xij = 1, ∀I ⊆[c], |I| ≥2, ∀j ∈TI

0 < xij < 1, ∀I ⊆[c], |I| ≥2, ∀i ∈I, ∀j ∈TI αi = 1, ∀i ∈[c] α1v1j > · · · > αc−1v(c−1)j > αcvcj, where

∀j ∈S1>2>···>c−1>c α1v1j > · · · > αc−1v(c−1)j = αcvcj, where

∀j ∈S1>2>···>c−1=c α1v1j > · · · > αcvcj > αc−1v(c−1)j, where

∀j ∈S1>2>···>c>c−1

... αcvcj > · · · > α2v2j > α1v1j, where

∀j ∈Sc>c−1>···>1

17306

<!-- Page 6 -->

In this setting, the above constraints constitute a linear system over the variables (xij). Solving this linear system. If a solution exists, then we get a pacing equilibrium.

Case 2: some but not all of αi’s equal 1. Note that there are actually 2c −2 possible cases. Given each case, we denote by E the set of buyers i satisfying αi = 1, and by L the set of buyers i′ satisfying αi′ < 1.

E:= {i ∈[c]: αi = 1}, L:= {i′ ∈[c]: αi′ < 1}.

All buyers in L exhaust their budgets, and consequently, we impose the following constraints.

                                         

                                        

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI xijαivij ≤Bi, ∀i ∈E

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI xijαivij = Bi, ∀i ∈L αivij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i, i′ ∈I, ∀j ∈TI X i∈I xij = 1, ∀I ⊆[c], |I| ≥2, ∀j ∈TI

0 < xij < 1, ∀I ⊆[c], |I| ≥2, ∀i ∈I, ∀j ∈TI αi = 1, ∀i ∈E 0 < αi < 1, ∀i ∈L α1v1j > · · · > αc−1v(c−1)j > αcvcj, where

∀j ∈S1>2>···>c−1>c α1v1j > · · · > αc−1v(c−1)j = αcvcj, where

∀j ∈S1>2>···>c−1=c α1v1j > · · · > αcvcj > αc−1v(c−1)j, where

∀j ∈S1>2>···>c>c−1

... αcvcj > · · · > α2v2j > α1v1j, where

∀j ∈Sc>c−1>···>1

In this case, the variables include αi′ for each i′ ∈L, as well as the allocation variables xij corresponding to goods that are assigned to multiple buyers.

Under these conditions, for all i′ ∈L, the term xi′jαi′vi′j is quadratic term. Notably, these quadratic terms arise only when a good is allocated to multiple buyers whose bids are equal. Consider one such quadratic term, xi′

0jαi′ 0vi′ 0j. The treatment of these quadratic terms requires a case-by-case analysis, which we divide into the following two scenarios.

If there exists a buyer i ∈E such that their bid for good j equals that of buyer i′

0, i.e., αi′ 0vi′ 0j = αivij, then the quadratic term becomes xi′

0jαivij, which is linear in xi′ 0j. Thus, the quadratic term can be eliminated in this case.

If no such buyer i ∈E exists, and instead there are k ≥1 buyers such that i′

1,..., i′ k ∈L whose bids for good j are equal to that of i′

0, then we proceed as follows. Let us define new variables yi′

0j = xi′ 0jαi′ 0,..., yi′ kj = xi′ kjαi′ k. Our goal is to eliminate the original allocation variables xi′

0j,..., xi′ kj. First, all associated quadratic terms xi′ ljαi′ lvi′ lj for 0 ≤l ≤k become linear in the form yi′ ljvi′ lj. Second, to handle the original constraints involving xi′ lj, we make the following transformations: The bounds 0 < xi′ lj < 1 become 0 < yi′ lj < αi′ l, for all 0 ≤l ≤k. To reformulate the constraint P

0≤l≤k xi′ lj = 1, we ob- serve that this is equivalent to P

0≤l≤k yi′ lj αi′ l

= 1, which can be rewritten as yi′

0j + X

1≤l≤k yi′ lj · αi′

0 αi′ l

= αi′

0.

Next, we employ the identities:

αivij = αi′vi′j, ∀j ∈TI, {i} ⊂I ⊆[c], ∀i, i′ ∈I, which means that all buyers in I submit identical scaled bids for good j.

Under the second-price auction mechanism, this leads to the conclusion that the total payment for good j equals any individual buyer’s bid. Consequently, we have:

X

0≤l≤k yi′ ljvi′ lj = αi′

0vi′ 0j.

Through these transformations, the original constraint is thus converted into the above equivalent form.

Consequently, the original system can be reduced to the following linear system.

                                                        

                                                       

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI xijαivij ≤Bi, ∀i ∈E

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c] ∃i′∈I,i′∈E

X j∈TI xijαi′vi′j

+

X

{i}⊂I⊆[c] ∀i′∈I,i′∈L

X j∈TI yijvij = Bi, ∀i ∈L αivij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i, i′ ∈I, ∀j ∈TI X i∈I xij = 1, ∀I ⊆[c], I ⊈L, |I| ≥2, ∀j ∈TI

0 < xij < 1, ∀I ⊆[c], I ⊈L, |I| ≥2, ∀j ∈TI X i∈I yijvij = αi′vi′j, ∀I ⊆L, |I| ≥2, ∀j ∈TI

0 < yij < αi, ∀I ⊆L, |I| ≥2, ∀j ∈TI αi = 1, ∀i ∈E 0 < αi < 1, ∀i ∈L α1v1j > · · · > αc−1v(c−1)j > αcvcj, where

∀j ∈S1>2>···>c−1>c α1v1j > · · · > αc−1v(c−1)j = αcvcj, where

∀j ∈S1>2>···>c−1=c α1v1j > · · · > αcvcj > αc−1v(c−1)j, where

∀j ∈S1>2>···>c>c−1

... αcvcj > · · · > α2v2j > α1v1j, where

∀j ∈Sc>c−1>···>1

17307

<!-- Page 7 -->

It can be observed that each quadratic term in this constraint has been transformed into a linear term. Therefore, we can directly apply linear programming techniques to solve this system. If a feasible solution exists, it corresponds to a pacing equilibrium.

Case 3: αi < 1 for each i ∈[c]. In this case, all buyers exhaust their budgets, and we also use yij = xij, αi, we can get:

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI yijvij = Bi, ∀i ∈[c], which means that all buyers have exhausted their budgets.

Additionally, as in Case 2, the following relation also holds:

0 < yij < αi, ∀I ⊆[c], |I| ≥2, ∀i′ ∈I, ∀j ∈TI, and

X i∈I yijvij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i′ ∈I, ∀j ∈TI.

Upon applying the same idea, we result in the following set of constraints.

                                  

                                 

X j∈T{i}

pj(α) +

X

{i}⊂I⊆[c]

X j∈TI yijvij = Bi, ∀i ∈[c]

αivij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i, i′ ∈I, ∀j ∈TI X i∈I yijvij = αi′vi′j, ∀I ⊆[c], |I| ≥2, ∀i′ ∈I, ∀j ∈TI

0 < yij < αi, ∀I ⊆[c], |I| ≥2, ∀i ∈I, ∀j ∈TI 0 < αi < 1, ∀i ∈[c] α1v1j > · · · > αc−1v(c−1)j > αcvcj, where

∀j ∈S1>2>···>c−1>c α1v1j > · · · > αc−1v(c−1)j = αcvcj, where

∀j ∈S1>2>···>c−1=c α1v1j > · · · > αcvcj > αc−1v(c−1)j, where

∀j ∈S1>2>···>c>c−1

... αcvcj > · · · > α2v2j > α1v1j, where

∀j ∈Sc>c−1>···>1

The variables involved are yij and αi. Solving this system of linear inequalities, if a solution exists, yields a pacing equilibrium.

Time Complexity. By Lemma 5, we can deduce that the number of ordered tuples (Sσ) is O(mc−1). Then, according to the algorithm, for each ordered tuple (Sσ), there are 2c possible cases, where 2c is a constant. Each case corresponds to a linear system, and each linear system can be solved in polynomial time. Therefore, the algorithm can run in polynomial time.

As for the computation of the LP with n variables, Cohen, Lee, and Song (2019) established the time complexity of O(nω log(n δ)), where ω ≈2.37 denotes the matrix multiplication exponent and δ represents the relative accuracy. Integrating their result with our algorithm yields a total time complexity of O(mc−1+ω log(m δ)).

## Conclusion

We focus on the setting where the number of buyers in second-price auctions is constant. In this restricted regime, we present the first polynomial-time algorithm for computing an exact second-price pacing equilibrium (SPPE). Our approach leverages the cell-decomposition method. To make each cell tractable, we transform the formulation into a linear program by introducing auxiliary variables, which allows us to solve each case where the pacing multipliers are controlled efficiently.

A natural direction for future work is to explore the dual setting where the number of goods is constant. More importantly, obtaining a constant additive approximation of an SPPE remains an open challenge. We conjecture that the 1/3-approximation bound recently established by Chen and Li (2025) is tight.

## Acknowledgments

This work was supported by the National Natural Science Foundation of China (Grants 62472029 and 62572476) and the Key Laboratory of Interdisciplinary Research of Computation and Economics (Shanghai University of Finance and Economics), Ministry of Education.

## References

Aggarwal, G.; Badanidiyuru, A.; Balseiro, S. R.; Bhawalkar, K.; Deng, Y.; Feng, Z.; Goel, G.; Liaw, C.; Lu, H.; Mahdian, M.; Mao, J.; Mehta, A.; Mirrokni, V.; Leme, R. P.; Perlroth, A.; Piliouras, G.; Schneider, J.; Schvartzman, A.; Sivan, B.; Spendlove, K.; Teng, Y.; Wang, D.; Zhang, H.; Zhao, M.; Zhu, W.; and Zuo, S. 2024. Auto-Bidding and Auctions in Online Advertising: A Survey. SIGecom Exch., 22(1): 159–183. Balseiro, S. R.; Bhawalkar, K.; Feng, Z.; Lu, H.; Mirrokni, V.; Sivan, B.; and Wang, D. 2024. A Field Guide for Pacing Budget and ROS Constraints. In Proceedings of the 41st International Conference on Machine Learning (ICML). OpenReview.net. Balseiro, S. R.; and Gur, Y. 2019. Learning in Repeated Auctions with Budgets: Regret Minimization and Equilibrium. Management Science, 65(9): 3952–3968. Borgs, C.; Chayes, J. T.; Immorlica, N.; Jain, K.; Etesami, O.; and Mahdian, M. 2007. Dynamics of Bid Optimization in Online Advertisement Auctions. In Proceedings of the 16th International Conference on World Wide Web (WWW), 531–540. ACM. Chen, X.; Deng, X.; and Teng, S.-H. 2006. Sparse games are hard. In International Workshop on Internet and Network Economics, 262–273. Springer.

17308

<!-- Page 8 -->

Chen, X.; Diakonikolas, I.; Paparas, D.; Sun, X.; and Yannakakis, M. 2018. The complexity of optimal multidimensional pricing for a unit-demand buyer. Games and Economic Behavior, 110: 139–164. Chen, X.; Kroer, C.; and Kumar, R. 2021. Throttling Equilibria in Auction Markets. In Proceedings of the 17th Conference on Web and Internet Economics (WINE), volume 13112 of Lecture Notes in Computer Science, 551. Springer. Chen, X.; Kroer, C.; and Kumar, R. 2023. The Complexity of Pacing for Second-Price Auctions. Mathematics of Operations Research, 49(4): 2109–2135. Chen, X.; and Li, Y. 2025. Constant Inapproximability of Pacing Equilibria in Second-Price Auctions. arXiv preprint arXiv:2501.15295. Cohen, M. B.; Lee, Y. T.; and Song, Z. 2019. Solving linear programs in the current matrix multiplication time. In Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing, STOC 2019, 938–942. New York, NY, USA: Association for Computing Machinery. ISBN 9781450367059. Conitzer, V.; Kroer, C.; Sodomka, E.; and Moses, N. E. S. 2022. Multiplicative Pacing Equilibria in Auction Markets. Operations Research, 70(2): 963–989. Devanur, N. R.; and Kannan, R. 2008. Market equilibria in polynomial time for fixed number of goods or agents. In 2008 49th Annual IEEE Symposium on Foundations of Computer Science, 45–53. IEEE. Karmarkar, N. 1984. A new polynomial-time algorithm for linear programming. In Proceedings of the Sixteenth Annual ACM Symposium on Theory of Computing, STOC ’84, 302–311. New York, NY, USA: Association for Computing Machinery. ISBN 0897911334. Khachiyan, L. G. 1979. A polynomial algorithm in linear programming. Dokl. Akad. Nauk SSSR, 244(5): 1093–1096. Liu, Z.; Li, J.; and Deng, X. 2021. On the approximation of Nash equilibria in sparse win-lose multi-player games. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, 5557–5565. Liu, Z.; and Sheng, Y. 2018. On the approximation of Nash equilibria in sparse win-lose games. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 32. Lucier, B.; Pattathil, S.; Slivkins, A.; and Zhang, M. 2024. Autobidders with Budget and ROI Constraints: Efficiency, Regret, and Pacing Dynamics. In Proceedings of the 37th Annual Conference on Learning Theory (COLT), volume 247 of Proceedings of Machine Learning Research, 3642– 3643. PMLR. Orlik, P.; and Terao, H. 1992. Arrangements of Hyperplanes, volume 300 of Grundlehren der mathematischen Wissenschaften. Berlin: Springer-Verlag. ISBN 978-3-540- 55259-3. Wang, Q.; Yang, Z.; Deng, X.; and Kong, Y. 2023. Learning to Bid in Repeated First-Price Auctions with Budgets. In Proceedings of the 40th International Conference on Machine Learning (ICML), volume 202 of Proceedings of Machine Learning Research, 36494–36513. PMLR.

Zaslavsky, T. 1975. Facing up to arrangements: face-count formulas for partitions of space by hyperplanes. Memoirs of the American Mathematical Society, 1(154): 1–102.

17309
