---
title: "On the Edge of Core (Non-)Emptiness: An Automated Reasoning Approach to Approval-Based Multi-Winner Voting"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38709
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38709/42671
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# On the Edge of Core (Non-)Emptiness: An Automated Reasoning Approach to Approval-Based Multi-Winner Voting

<!-- Page 1 -->

On the Edge of Core (Non-)Emptiness: An Automated Reasoning Approach to Approval-Based Multi-Winner Voting

Ratip Emin Berker*1, Emanuel Tewolde*1, Vincent Conitzer1,2, Mingyu Guo3, Marijn Heule1, Lirong Xia4

1Carnegie Mellon University 2University of Oxford 3University of Adelaide 4Rutgers University {rberker, etewolde, conitzer, mheule}@cs.cmu.edu, mingyu.guo@adelaide.edu.au, lirong.xia@rutgers.edu

## Abstract

Core stability is a natural and well-studied notion for group fairness in multi-winner voting, where the task is to select a committee from a pool of candidates. We study the setting where voters either approve or disapprove of each candidate; here, it remains a major open problem whether a core-stable committee always exists. In this work, we develop an approach based on mixed-integer linear programming for deciding whether and when core-stable committees are guaranteed to exist. In contrast to SAT-based approaches popular in computational social choice, our method can produce proofs for a specific number of candidates independent of the number of voters. In addition to these computational gains, our program lends itself to a novel duality-based reformulation of the core stability problem, from which we obtain new existence results in special cases. Further, we use our framework to reveal previously unknown relationships between core stability and other desirable properties, such as notions of priceability.

Code — https://github.com/emanueltewolde/Core-MILP Extended version — https://arxiv.org/abs/2512.16895

## Introduction

Elected committees enable efficient implementation of highstakes decisions affecting large groups of voters, forming the backbone of representative democracies. The same formalization of electing a “committee” also applies to selecting sets of items of other types—a set of locations at which to build facilities, times at which to schedule webinars, etc. The benefits of committee elections, however, crucially rely on the committee itself being (proportionally) representative, reflecting the diverse preferences of the voters. One possible way of expressing such preferences is that of approval sets, where each voter specifies which candidates they approve of. Approval preferences are simple to elicit; they also come with a range of mathematical properties that enable us to rigorously argue about the quality of an elected committee. Accordingly, Aziz et al. (2017) defined a hierarchy

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

of representation axioms—desiderata a committee should ideally satisfy—for approval-based multi-winner elections. Their work paved the way for a rich literature analyzing further axioms in this setting, as well as the relationships among them; cf. Lackner and Skowron (2022) for an excellent overview. Importantly, several of these axioms guided the design of novel and efficient (multi-winner) voting rules (Aziz et al. 2018; Peters and Skowron 2020; Brill and Peters 2023; Casey and Elkind 2025), some of which are currently utilized in local elections in several countries (Peters 2025).

Out of the hierarchy of axioms introduced by Aziz et al., the one named core stability stands out, both due to its interpretability and strength. It stands on top of this hierarchy and implies many axioms introduced later on (see, e.g., Peters, Pierczy´nski, and Skowron 2021). Intuitively, a committee W consisting of k candidates is core-stable if no coalition of voters all strictly prefer an alternative committee that they can jointly “afford” with their proportional share of the seats. More formally, we say that a subset of candidates W ′ ⊆C is a successful deviation from W if there is a subset of voters N ′ ⊆N such that |W ′| k ≤|N ′|

|N| (i.e., N ′ can afford W ′) and all members of N ′ approve of strictly more members of W ′ than W. Then, W is core-stable if it does not admit any successful deviations. Equivalently, for any potential deviation W ′, the support it receives from the voters (who strictly prefer it to W) must be insufficient to afford W ′.

Example 1 (This paper’s running example). Consider an instance with |N| = 6 voters and |C| = 5 candidates. The approval sets of the voters are

A1 = {c1, c2, c3} A2 = {c2, c4} A3 = {c2, c4} A4 = {c2, c5} A5 = {c2, c5} A6 = {c4, c5}.

If our goal is to pick a committee with k = 3 candidates, then W = {c1, c3, c5} is not core-stable: W ′ = {c2, c5} is preferred to W by each voter in N ′ = {2, 3, 4, 5}, achieving

|W ′

1| k = 2

3 ≤4 6 = |N ′| |N|. The committee W ∗= {c2, c4, c5} is core-stable, as there is no successful deviation from it.

Core stability also captures the idea of “fair taxation” (Munagala et al. 2021): if the number of seats is seen as the total resources of the community (where each agent brings in

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16673

<!-- Page 2 -->

the same amount), no subgroup of voters are better off leaving the group with their share of the resources. Importantly, the appeal of this property extends beyond political elections; it can also be a powerful guiding principle for achieving group fairness in AI/ML. For example, Chaudhury et al. (2022, 2024) apply core stability (and an adaptation thereof) to define fair outcomes in federated learning, where a set of agents (clients) use their heterogeneous and decentralized data to train a single model. Indeed, if a subset of clients can use their own resources to train a different model that makes all of them happier, they will stop contributing their data and compute to the larger coalition. Approval-based multiwinner elections can also capture extensions of this setting, such as federated multi-objective optimization (introduced by Yang et al. 2024), where each voter is interested in only a subset of the objectives. In the AI alignment literature, Conitzer et al. (2024) emphasize that core-like deviations can guide decisions to create multiple AI systems serving different subgroups, rather than a single overall system.

Despite its wide applications and strong guarantees, core stability remains highly elusive: all known multi-winner voting rules fail it, and it remains a major open problem whether a core-stable committee always exists in approvalbased elections (Aziz et al. 2017; Cheng et al. 2019; Munagala, Shen, and Wang 2022). While approximations (Jiang, Munagala, and Wang 2020; Peters and Skowron 2020) and relaxations (Cheng et al. 2019; Brill et al. 2020) have been studied, until very recently the only known (unrestricted) existence result was for committees of size up to k = 3 (Cheng et al. 2019). In concurrent and soon-to-appear work, Peters (2025) pushes this boundary up to k = 8 by showing that a specific voting rule, Proportional Approval Voting (PAV), gives core-stable committees up to this point. However, he also gives a counterexample for PAV for k = 9, showing that this specific method cannot be pushed further. In this paper, we take an approach free of assumptions about the voting rule used; that is, we search over all possible voter preferences to find those where core stability comes closest to being failed by all committees. At the heart of many of our results lie techniques borrowed from automated reasoning.

Automated Reasoning in Social Choice The automated reasoning paradigm involves the development of theoretical results and interpretable proofs through the intuition gained from computer-generated proofs for instances to which the techniques scale. Tang and Lin (2008, 2009) demonstrated its effectiveness in social choice by rederiving the celebrated impossibility theorems by Arrow (1963) and Gibbard–Satterthwaite (Gibbard 1973; Satterthwaite 1975). The central and recurring idea since then has been to express the input parameters to social choice problems (votes, candidate selection, etc.) via Boolean variables, and to encode axioms via Boolean formulas over these variables. In the following years, this paradigm—and specifically SAT solving (Biere et al. 2021)—has lead to advancements in a plethora of social choice settings (Geist and Peters 2017). Examples include problems such as ranking sets of objects (Geist and Endriss 2011), irresolute voting rules and tournament solutions (Brandt and Geist 2016), fair di- vision (Brandl et al. 2021), the no-show paradox (Moulin 1988; Brandt, Geist, and Peters 2017; Brandl et al. 2019), and matching markets (Endriss 2020). Closer to our setting of multi-winner elections, Peters (2018) showed that forms of proportionality and strategyproofness can be incompatible with regards to some resolute voting rules.

A drawback to the SAT approach is that solvers do not scale well with the number of voters, which can get large. This is a bottleneck in our setting especially because multiwinner voting instances are parametrized by three values (number of voters, candidates, and committee seats), which further complicates the key step of extending computer proofs for small instances to the general setting. In this work, we analyze core stability for vote distributions, which enables us to leverage “linearity” properties of the core (Xia 2025) to eliminate dependencies on the number of voters. To do so, we abandon SAT methods in favor of mixedinteger linear programming. Related approaches have previously found fruitful applications in probabilistic social choice (Mennle and Seuken 2016; Brandl et al. 2018). They have also long been fundamental to the adjacent field of automated mechanism design, where (mixed integer) linear programs can be used to solve the discretized version of the general problem (Conitzer and Sandholm 2002, 2004) and have helped in proving new (im)possibility results, for example in the context of redistribution mechanisms (Guo and Conitzer 2009, 2010; Damle, Padala, and Gujar 2024). Last but not least, Peters (2025) analyzes the PAV rule in our problem setting by describing the PAV solutions as a linear program. Overall, however, we find that automated reasoning approaches beyond SAT—especially those taking the perspective of linear theories—have been relatively underexplored in the literature. Indeed, we suspect that a variety of other social choice settings can benefit from them.

Our Contributions Leveraging the formulation of core stability in terms of vote distributions, we introduce and study the problem of finding the vote distributions in which committees are “least” core-stable. In Section 3, we cast this problem first as a nested optimization problem, and then as a mixed-integer linear program, where the optimal value corresponds to the (positive or negative) excess support the best deviation of each committee is guaranteed to have. By running experiments with the latter in Section 4, we identify a pattern in the optimal values of instances with few candidates, leading us to a surprising connection to the stronger axiom of Droop core stability. We show that the identified pattern indeed forms a lower bound for all instances. In Section 5, we then use linear program duality to prove matching upper bounds in specific cases with small deviations or large committees, proving novel non-emptiness results and rediscovering previously known results as corollaries. In Section 6, we use a modification of our program to identify the minimal instances for which (Droop) core stability does not imply priceability axioms from the literature. Our findings resolve previously open problems, including disproving a conjecture on Lindahl priceability. The omitted proofs can be found in the appendix of the full version of the paper.

16674

<!-- Page 3 -->

## 2 Preliminaries

In approval-based multi-winner elections, we have a set of candidates C = {c1, c2,..., cm}, from which we have to select a committee W ⊂C of size k ∈N, also called a kcommittee. We assume 0 < k < m. Denote the set of all k-committees and non-empty committees of size up to k by

Mk:= {W ⊂C: |W| = k}, and M≤k:= {W ′ ⊂C: 1 ≤|W ′| ≤k}

respectively. We refer to each W ′ ∈M≤k as a (potential) deviation. Let N:= {1, 2,..., n} be the set of voters, where n ∈N. Each voter i ∈N has a subset Ai ⊆C of candidates they approve of, also called an approval set. Together, these sets form an (approval) profile A:= (Ai)i∈N.

We call a k-committee W core-stable if, intuitively, no deviation W ′ is strictly preferred to W by a subset of voters whose proportional share of candidates exceeds |W ′|.

Definition 2 (Core Stability). A k-committee W ∈Mk is core-stable w.r.t. profile A if for all W ′ ∈M≤k, we have

|{i ∈N: |Ai ∩W ′| > |Ai ∩W|}| · k n < |W ′|. (1)

Here, k n is the fraction of a committee seat that a single voter can “buy”, or dually, n k is the “cost” (expressed in number of voters) of securing a seat. The core of a profile is defined as the set of all of its core-stable committees.

Core as a Mixed-Integer Linear Program In this section, we develop a mixed-integer linear program for computing profiles for which core stability is “least satisfiable,” i.e., the core, if not empty, is closest to being empty. Recently, Xia (2025) has noted the following “linearity” property: The exact number of voters n is not crucial to the core of a profile A, but rather the frequency with which each vote A ⊆C appears in A. In particular, if we multiply each voter by a constant number, then the core remains unchanged. This can be seen from Equation (1); note that k stays fixed. Hence, for any profile A = (Ai)i∈N, we can study its associated vote distribution x ∈∆(2C) ∩Q2C, defined as x[A]:= 1 n · |{i ∈N: Ai = A}|. Here, ∆(S) ⊆RS denotes the probability simplex over a discrete set S. For the profile from Example 1, the associated vote distribution is x[A] =

 



1/3 if A = {c2, c4} or A = {c2, c5} 1/6 if A = {c1, c2, c3} or A = {c4, c5} 0 otherwise

. (2)

Define the binary vector δW,W ′ ∈{0, 1}2C for each W ∈ Mk and W ′ ∈M≤k to have entry 1 at index A ⊆C if and only if |A∩W ′| > |A∩W|. That is, δW,W ′ indicates which votes A strictly prefer W ′ over W.

Lemma 3 (Xia 2025). Given m, k, n, and profile A, a kcommittee W is core-stable if and only if δT

W,W ′x−|W ′| k < 0 for A’s vote distribution x and for all W ′ ∈M≤k.

Lemma 3 allows us to work in the vote distribution space ∆(2C) ∩Q2C instead of in profile spaces (2C)n for varying numbers n ∈N. That is because if we found a vote distribution x ∈∆(2C)∩Q2C with an empty core, we can construct a profile A out of it with that same property by rescaling x to an element of N2C, and interpret its entries as the number of voters in N with the respective approval sets.

Therefore, we can decide for a given m and k whether there exists a profile A = (Ai)i∈N with any number of voters n such that the core is empty by deciding whether

∃x ∈∆(2C) ∩Q2C ∀W ∈Mk ∃W ′ ∈M≤k:

δT

W,W ′x −|W ′| k ≥0. We reformulate this into an optimization problem. Proposition 4. Suppose m and k are given. Then there exists a set of voters N and profile A = (Ai)i∈N for which the core is empty if and only if the optimization problem max x∈∆(2C)∩Q2C min W ∈Mk max W ′∈M≤k δT

W,W ′x −|W ′| k (M3)

has nonnegative value.

Going beyond the question of nonnegativity, we can give the optimization in M3 an interpretation `a la “least core” from cooperative game theory (Shapley and Shubik 1966; Maschler, Peleg, and Shapley 1979). For a fixed vote distribution x, we define a k-committee W to be in x’s sizewiseleast core if it solves the inner min-max problem of M3 for x. We call the corresponding optimal objective µ∗ x the value of x’s sizewise-least core; hence, M3 essentially searches for a point x∗with the largest such value. Intuitively, any committee W in the sizewise-least core of x gives rise to at most µ∗ x excess voter support to any deviation W ′ beyond what is required afford it. No matter the instance, the sizewise-least core always exists. Moreover, if µ∗ x is negative, the sizewiseleast core will be a subset of the core, making the core nonempty. In such cases, we intuitively expect committees in the sizewise-least core to be the most robust among core-stable committees against fluctuations in the vote distribution; cf. Li and Conitzer (2015) for an analogous study in cooperative game theory. Indeed, our interpretations above cannot be captured by notions of approximate core in prior literature (see, e.g., Lackner and Skowron 2022, Definition 4.11).

In order to make the max-min-max problem M3 amenable to empirical as well as theoretical analysis, we next reformulate it to a single-level optimization problem. We have tried multiple reformulations and found that a particular one yields a mixed-integer linear problem that is most efficient in practice, which we present below.

max x∈R2C, µ∈R, y∈{0,1}Mk×M≤k µ (MILP)

s.t.

X

A⊆C x[A] = 1 and ∀A ⊆C: x[A] ≥0

∀W ∈Mk:

X

W ′∈M≤k y[W, W ′] ≥1

∀W ∈Mk, W ′ ∈M≤k:

µ ≤δT

W,W ′x −|W ′| k + 3(1 −y[W, W ′])

16675

<!-- Page 4 -->

The main idea of MILP is to introduce a binary variable y[W, W ′] that evaluates to 1 only if deviation W ′ maximizes the inner max problem of M3 for k-committee W. Despite searching over real variables, MILP will admit a rational optimal solution since all of its coefficients are rational. We next show these solutions match those of M3.

Theorem 1. For any m and k, the optimal values of M3 and MILP coincide, and solutions x∗to M3 are exactly the x-components of solutions (x∗, µ∗, y∗) to MILP. Further, solution component µ∗represents the largest value achievable for the sizewise-least core for m and k.

Intuitively, we replaced the inner min-max in M3 with a continuous variable µ. To ensure that this is a correct interpretation of µ given the chosen values of x, we have to make sure that for every committee W, there in fact exists a W ′ such that µ is at most δT

W,W ′x −|W ′| k. (This will ensure that µ will not be set too high; we do not need to worry that µ will be set too low, because the solver will try to maximize µ.) To do so, we force the solver to set y[W, W ′] to 1 for at least one W ′, and for that one, the value of δT

W,W ′x −|W ′| k must be large enough because the last term in the last MILP constraint disappears when y[W, W ′] = 1. (Whereas if y[W, W ′] = 0, that constraint automatically holds due to the slack of 3 added by this last term. Any slack of ≥2 would have sufficed here.)

From Experiments to Lower Bounds We implement MILP using Gurobi (Gurobi Optimization, LLC 2024), a popular commercial solver for mixed-integer, linear, and nonlinear optimization that guarantees global optimality (up to a small tolerance error) upon termination. All experiments in this paper were run up to the default tolerance of 10−4. Table 1 depicts the optimal values of MILP that we computed for various (m, k) pairs with 1 ≤k < m.

Our experiments show that for m ≤7 candidates, there will always be a core-stable committee, for any committee size k, any number of votes n, and any vote profile A. It improves on Cheng et al. (2019), which confirms experimentally that the core is non-empty for m + n ≤14 and k < m. Concurrent and soon to appear work by Peters (2025) subsumes our experimental (non-emptiness) results since it shows that the core is always non-empty if m ≤15, or, alternatively, if k ≤8. Peters obtains these results by focusing on when the PAV rule and modifications thereof are guaranteed to select a core-stable committee. For any larger m or k, Peters (2025) gives PAV failure modes, showing the limitations to his PAV-focused approach. In contrast, our MILP resolves (non-)emptiness of core for given values of m and k in general, rather than focusing just on whether one particular voting rule selects core-stable committees.

The limitations of our approach, however, lie in bounded computational resources. MILP contains 2m + 1 continuous variables and m k

· Pk l=1 m l binary variables (or a few less after eliminating certain (W, W ′) pairs, such as when W ′ ⊆W, without loss of optimality). For k ≈m/2, these values grow super-polynomially in m. For small values of m, our implementation is still quite fast: on 8 cores, the in- k\m 5 6 7 Fraction

1 -0.5000 -0.5000 -0.5000 -0.5000 = −1

2 2 -0.1667 -0.1667 -0.1667 -0.1667 = −1

6 3 -0.0833 -0.0833 -0.0833 -0.0833 = −1

12 — -0.0500 -0.0500 -0.0500 = −1

20 5 — — -0.0333 -0.0333 = −1

30 6 — — — -0.0238 = −1

42 k — — — — −1 k(k+1)

**Table 1.** Optimal values of MILP computed for various combinations of m, k. Columns m ≤3 are omitted for brevity.

stance m = 7 and k = 3 takes ≤2.5h time to run on our laptop, while Peters (2025) briefly describes an implementation attempt for the same general problem that does not terminate within a time limit of 37h. If we investigate m = 8, however, then the solver does not terminate within the timelimit of 72h when k = 4. More generally, we find the case k ≈m/2 takes the longest to solve in our implementations.

That being said, our experiments continue to offer insights beyond just non-emptiness: we observe that the optimal values in Table 1 have a structure to them. They are independent of m and take on the value −1 k(k+1). If this were true for all (m, k), the core would always be non-empty. While we cannot prove this in full generality in this paper, we can make progress towards such a result. First, we prove −1 k(k+1) is a lower bound to the optimal value of MILP for all m and k.

Theorem 2. For all m, k, MILP ≥ −1 k(k+1).

Proof. Since MILP is a maximization, we can prove this lower bound by giving a feasible variable assignment to MILP that achieves objective value −1 k(k+1). Given pair k < m, fix a subset of candidates B ⊆C with |B| = k + 1. For each A ⊆C, set x[A]:=

(

1 k+1 if A = {c} with c ∈B 0 otherwise.

For each W ∈Mk, fix some cW ∈B \ W (such a cW ex- ists as |B| > |W|). Set y[W, W ′]:=

1 if W ′ = {cW } 0 otherwise.

Finally, set µ = −1 k(k+1), which is also equal to the objective. It is straightforward to check that this assignment is feasible for MILP. In particular, for any W and for W ′ = {cW }, we have δT

W,W ′x = x[{cW }], since |W ∩{cW }| = 0. Further, δT

W,W ′x −|W ′| k + 3(1 −y[W, W ′]) = x[{cW }] −1 k = 1 k+1 −1 k = −1 k(k+1) = µ, indicating that for the above x and y values, the µ is chosen maximal while staying feasible.

Theorem 2 shows that no profile can have a sizewise-least core with value less than −1 k(k+1). In the proof, this value emerges after subtracting 1 k (the cost of a deviation of size 1)

16676

<!-- Page 5 -->

from 1 k+1 (the maximum amount of support any such deviation will get in our assignment). The former value originates from the intuition that a coalition is entitled to make decisions about a seat in the committee only if they comprise at least 1 k fraction of the total electorate, a quantity also known as the Hare quota. The latter value, on the other hand, is reminiscent of an alternative intuition, requiring the coalition to be strictly greater than a fraction of 1 k+1, also known as the Droop quota. Defining core stability with respect to the latter leads to a strictly stronger criterion (Brill et al. 2020). The next definition introduces this notion in our framework.

Definition 5 (Droop core). Given m and k, and a profile A, a k-committee W ∈Mk is Droop core-stable if δT

W,W ′x −

|W ′| k+1 ≤0 for A’s vote distribution x and for all W ′ ∈M≤k.

MILP can be easily edited to search for profiles with an empty Droop core (again for given m, k) by replacing each occurrence of k in a denominator with k + 1. If we call this analogous program DrMILP, then an empty Droop core is found if its objective value is strictly larger than 0. The proof of Theorem 2 then implies for any m, k, there is always a profile sitting at the boundary of an empty Droop core.

Corollary 6. For all m, k, DrMILP ≥0.

Indeed, when we run DrMILP for the values of m, k in Table 1, the program converges to a value of 0, showing that the Droop core is always non-empty for these values.1 Further, Corollary 6 indicates that Droop quota is the “best we can hope for” if we require non-emptiness, since for any m and k, core notions with any smaller quota (giving deviating coalitions more power) will be empty for some vote distribution x. A similar observation was previously made by Janson (2018, Remark 3.6) for related fairness properties.

Next, we study when the lower bounds of Theorem 2 and Corollary 6 can be matched with an identical upper bound.

Upper Bounds Using Duality

We derive a general strategy for proving upper bounds on MILP, and prove an upper bound of −1 k(k+1) for certain special cases. More generally, our approach provides a novel way of proving core non-emptiness results.

The key observation in our approach is that for any fixed values of the integer variables y in MILP, we get a linear program over variables µ and x, the optimal value of which is the largest value MILP can achieve using that y. Without loss of optimality of MILP, we can restrict our attention to instances of y that have y[W, W ′] = 1 for only one deviation W ′ ∈M≤k for each committee W ∈Mk (call this deviation DW). Each such y then corresponds to a deviation function D: Mk →M≤k such that D(W) = DW for each W ∈Mk. Taking the dual of the linear program associated with D (and performing some simplification steps to significantly decrease the number of variables; see the proof

1Relatedly, PAV satisfies Droop core for k ≤5 (Peters 2025).

of Theorem 3), we obtain the following linear program.

min q∈RMk,u∈R u −

X

W ∈Mk

|D(W)| k q[W] (DLP)

s.t.

X

W ∈Mk q[W] = 1 and ∀W ∈Mk: q[W] ≥0

∀A ⊆C:

X

W ∈Mk: |D(W)∩A|>|W ∩A| q[W] ≤u

As with MILP and DrMILP, we refer to the analogous linear program for Droop core (where the k in the objective is replaced with k + 1) as DrDLP. Since the optimal value of MILP is the optimal value over all assignments of y, we can use strong duality and obtain an upper bound on MILP by bounding DLP across all deviation functions.

Theorem 3. Given m, k, and value v ∈R, we have MILP ≤ v (resp. DrMILP ≤v) if and only if DLP ≤v (resp. DrDLP ≤v) for all functions D: Mk →M≤k.

Furthermore, a closer look at DLP shows that q defines a probability distribution over Mk. Combining this observation with Lemma 3 and Theorem 3 lends itself to a novel way of formulating the core non-emptiness problem.

Corollary 7. Given m and k, the core (resp. Droop core) is non-empty for all profiles / vote distributions if and only if the following statement is true:

For every function D: Mk →M≤k, there exists a distribution q ∈∆(Mk) s.t. for all votes A ⊆C, we have

P W ∼q

|W ∩A| < |D(W) ∩A|

< (resp. ≤)

E W ∼q

|D(W)| k (resp. k + 1)

The boxed statement in Corollary 7 is notably similar to a lemma proven by Cheng et al. (2019, Inequality (3)) which implies the existence of stable lotteries (distributions over Mk such that the expected support of any deviation is not sufficient), a weaker result than core non-emptiness. In the appendix, we reinterpret their formulation (where D is replaced by distributions over M≤k) in our framework. We believe Corollary 7 lays the foundations for a probabilistic analysis towards proving core non-emptiness, possibly similar to Cheng et al.’s approach for stable lotteries.

Next, we illustrate the strength of Theorem 3 by proving upper bounds to MILP in special cases. Our results improve on previously known results, implying them as corollaries.

Small deviations The example profile we used in the proof of Theorem 2 relied on singleton deviations (|D(W)| = 1 for all W). Indeed, in all of the the experiments in Table 1, we see that the objective-maximizing values of y correspond to singleton deviations. We now formalize this intuition by showing that our lower bound for MILP is tight for singleton deviations, and the objective can only get worse when we add a single non-singleton deviation.

Theorem 4. Say we are given m, k, and a deviation function D such that |D(W)| = 1 for all W ∈Mk but possibly one W ∗. Then, DLP ≤− 1 k(k+2−|D(W ∗)|) (resp. DrDLP ≤0).

16677

<!-- Page 6 -->

Proof. Start with W1:= W ∗, and say t:= |D(W ∗)|. For i = {2,..., k+2−t}, pick Wi to be some arbitrary committee in Mk such that S j∈[i−1] D(Wj) ⊆Wi (the union will contain at most i −2 + t ≤k elements). Set q ∈∆(Mk) as q[W] =

(

1 k+2−t if W = Wi for some i ∈[k + 2 −t] 0 otherwise.

Fix any A ⊆C. We claim that the inequality |A ∩Wi| < |A ∩D(Wi)| can be true for at most one i ∈[k + 2 −t]. Say i∗is the smallest i ∈[k + 2 −t] such that A ∩D(Wi)̸ = ∅ (if no such i∗exists, we are done). For any j < i∗, we have |A ∩D(Wj)| = 0, so the inequality must be false. For any j > i∗, we have D(Wi∗) ⊆Wj; therefore, |A ∩Wj| ≥ |A ∩D(Wi∗)| ≥1 = |D(Wj)| ≥|A ∩D(Wj)|, so the inequality must be once again false. Hence, the inequality can only be true for i∗, implying u = 1 k+2−t with the above q is a feasible assignment to DLP (and DrDLP). Further, we have P

W ∈Mk |D(W)| · q[W] = t+(k+1−t)

k+2−t = k+1 k+2−t. Dividing by k (resp. k + 1) and subtracting from u gives the desired upper bound for DLP (resp. DrDLP).

Theorem 4 has several implications. First, for t = 1, it shows that the lower bound for MILP is exactly met when the deviations are restricted to singletons; further, when we add one non-singleton deviation, we only get farther from core emptiness. It also opens up a novel possibility for proving core non-emptiness in general, namely, by proving a similar effect from adding further non-singleton deviations to D. Second, Theorem 4 implies a known result as a corollary: a weaker version of the core named justified representation (where deviations are restricted to M1 rather than M≤k) can always be satisfied, regardless of whether we use Hare or Droop quota; indeed, the voting rule PAV is known to satisfy it with either quota (Aziz et al. 2017; Janson 2018).

Adapting our proof of Theorem 4 to broader classes of deviation functions presents several challenges.2 Nonetheless, an analogous construction can lead us to proving novel non-emptiness results, as we show next.

Large committees We turn to the setting of m = k + 1, for any k. In words, the problem is to select a single candidate that will not be in the committee. Unlike the opposite extreme of k = 1 (in which case any candidate that is approved by some voter is a core-stable 1-committee, and picking the candidate approved by the most voters is sufficient for Droop core), the core is not trivially non-empty when m = k + 1, as the next example shows. Example 8. Consider the profile from Example 1, the vote distribution of which is in (2), this time for k = m −1 = 4. Fix W = {c1, c3, c4, c5} and W ′ = {c2, c4, c5}. We have

2For example, say |D(W)| = 2 for all W ∈Mk, rather than singletons. Using the same construction as above, where for each i ≥1 we force ∪j<iD(Wj) ⊆Wi, we can only pick ≈k

2 committees before the union has more elements than a single committee can contain. Further, there may be an A ⊆C with |Wi ∩A| < |D(Wi) ∩A| for multiple i (e.g., since |D(W1) ∩A| = 1 and |D(W2) ∩A| = 2). The left-hand side of Corollary 7 will then be ≈ 2 k/2 for the uniform distribution over {Wi}, which violates the inequality as the right-hand side is 2 k.

δT

W,W ′x = x[{c2, c4}] + x[{c2, c5}] = 2

3 > 3 5 = |W ′| k+1, showing W is not in the Droop core. If we slightly modify the profile such that A1 = {c2} instead, then W is not even in the core, as certified by the same deviation W ′.

Nevertheless, our next result shows that the core is always non-empty in this case, even with Droop quota. Theorem 5. For any m and k = m−1, given any deviation function D, we have DLP ≤− 1 k(k+1) (resp. DrDLP ≤0).

The proof follows from a construction similar to that of Theorem 4. However, unlike the latter, Theorem 5 does not put any restrictions on the deviation function D. As a result, Theorem 3 gives us core non-emptiness in this setting.3

Corollary 9. The core is always non-empty for any m and k = m −1, even using Droop quota.

Overall, Theorems 3 and 4 demonstrate that our dual formulation offers a novel framework for deriving core nonemptiness results and investigating restricted notions of core stability in terms of deviation powers.

Relationship to Other Axioms We now modify MILP to investigate the relationship of core stability with other axioms in the literature. Our experiments here resolve previously open problems by efficiently finding counterexamples. They also identify the minimal m and k values for which a counterexample exists in the first place.

Lindahl priceability Munagala, Shen, and Wang (2022) introduce Lindahl priceability as another axiom in approvalbased multi-winner elections, based on the idea of market clearing. To introduce it, we can think of each voter i ∈N as having a budget of 1. Given a committee W ∈Mk, any voter is able to switch to a strictly preferred alternative set of candidates T ⊆C (not necessarily bounded in size by k) if they can “afford” all candidates in T. The question of whether W is Lindahl priceable becomes whether one can set prices (from voters to candidates) in a way that no candidate is cumulatively overpriced (specifically, larger than n/k) and no voter can afford a strictly preferred set of candidates. Definition 10. A k-committee W is Lindahl priceable w.r.t. profile A if ∃a price system {p[i, c]}i∈N,c∈C ≥0 such that 1. ∀c ∈C: P i∈N p[i, c] ≤n k, and 2. ∀i ∈N, T ⊆C: |Ai ∩T| > |Ai ∩W| ⇒P c∈T p[i, c] > 1.

Lindahl priceability implies weak priceability, which can be defined via Definition 10, except we restrict the T ⊆C in condition 2 to be of the form {d}∪(Ai∩W) s.t. d ∈Ai\W, i.e., each voter can only add candidates to their approved ones in W. While it is known that weak priceability is not

3The concurrent work of Peters (2025) shows that PAV satisfies core stability with m = k + 1 (using Hare quota). Our Corollary 9 strengthens this non-emptiness result using the Droop core. As noted by Casey and Elkind (2025), improving an axiom satisfiability result from Hare to Droop can often be nontrivial. Still, we note that this result is also obtainable by combining an analogous argument to that of Peters using the observation that PAV still satisfies EJR+ with Droop quota (Janson 2018; Brill and Peters 2023).

16678

<!-- Page 7 -->

sufficient for core stability, we have found no prior work with an explicit counterexample showing it is also not necessary.4 On the other hand, Munagala, Shen, and Wang (2022) show that Lindahl priceability also implies core stability. In a later report, Munagala and Shen (2024) state “even though Lindahl priceability implies core stability, we do not know if it is strictly stronger than the core. We conjecture that these two notions are the same.” In contrast, we are able to show through our framework that this conjecture is false.5

Combining it with the core In order to incorporate weak/Lindahl priceability into MILP, we first show that both axioms are compatible with our framework of vote distributions, mirroring what Lemma 3 showed for core stability. Lemma 11. For any given m, k, n, and profile A, a kcommittee W is weakly (resp. Lindahl) priceable iff there exists a price system p = {p[A, c]}A⊆C,c∈C ≥0 such that

1. ∀c ∈C: P A⊆C x[A] · p[A, c] ≤1 k, and 2. ∀A ⊆C, d ∈A\W, T = (A∩W)∪{d}: P c∈T p[A, c] > 1

(resp. ∀A, T ⊆C s.t. |A ∩T| > |A ∩W|), where x, again, is the vote distribution associated with A.

Fixing x and W, this forms a system of linear (strict) inequalities over variables p. In the appendix, we describe how we leverage linear program duality once again to get a dual program of this system. If the dual admits a feasible solution, then it serves as a certificate to W not being weakly/Lindahl priceable for x. This allows us to search for a core-stable committee W ∗that is not weakly/Lindahl priceable. Namely, for any desired counterexample W ∗, w.l.o.g. W ∗= {c1,..., ck}, minimize µ over vote distributions x such that µ ≥maxW ′∈M≤k δT

W ∗,W ′x −|W ′| k. To this linear program, add constraints of the weak (resp. Lindahl) priceability dual program for W ∗. This results in a program with quadratic constraints,6 whose optimal value is negative iff W ∗is core-stable but not weakly (resp. Lindahl) priceable. Using this approach, we show that even the stronger axiom of Droop core does not imply either priceability axiom. Theorem 6. There exists a vote distribution for m = 5 and k = 3 (resp. m = 4 and k = 2) with a k-committee that is Droop core-stable but not weakly (resp. Lindahl) priceable.

4What we here call weak priceability was defined by Munagala, Shen, and Wang (2022), who, in that version of their paper, stated it is equivalent to priceability as defined by Peters and Skowron (2020). However, as we show in the appendix, priceability (as an axiom for k-committees) is strictly stronger than weak priceability and incomparable with Lindahl priceability. Therefore, our Theorem 6 also shows that (Droop) core does not imply priceability.

5We suspect this conjecture might have been an oversight on the part of the authors, as checking whether a committee fails Lindahl priceability can be done in polynomial time (Munagala, Shen, and Wang 2022), whereas the equivalent problem for core stability is NP-hard (Brill et al. 2020, Thm 5.3). Hence, the two axioms cannot be equivalent unless P = NP. In any case, we will see that our minimal counterexample in Theorem 6 disproves the conjecture unconditionally, and also shows Lindahl priceability is strictly stronger than the core and weak priceability together (Corollary 12).

6Recall that the weak/Lindahl priceability dual is only linear as long as we do not also optimize over the vote distribution x.

Another strength of our program is that it enables us to confirm the minimality of these counterexamples, in the sense that it rules out counterexamples for any (m′, k′) with m′ < m or [m′ = m, k′ < k]. In contrast, hand-designed counterexamples for similar problems can get quite large— such as that no welfarist rule (a class of voting rules including PAV) is priceable for k = 57 and m = 669 (Peters and Skowron 2020)—without revealing whether simpler ones exist. Further, leveraging minimality, we derive that Lindahl priceability is strictly stronger than both axioms it implies. Corollary 12. There exists a vote distribution for m = 4 and k = 2 that admits a k-committee that is (Droop) corestable and weakly priceable, but not Lindahl priceable.

We end this section with remarking that while we obtain the counterexamples in Theorem 6 via Gurobi experiments, we can construct simple human-readable proofs uisng the optimal variable assignments in the dual weak/Lindahl priceability program. We demonstrate this with Example 1, whose vote distribution in (2) we obtained through one of our programs (showing core stability does not imply weak priceability for m = 5 and k = 3). Here, W = {c1, c2, c3} is core-stable. For the sake of contradiction, assume W is also weakly priceable, certified by a price system p = {p[A, c]}A⊆C,c∈C. Condition 1 of Lemma 11 then implies:

p[{c2, c4}, c2]

3 + p[{c2, c5}, c2]

3 ≤

X

A⊆C x[A]p[A, c2] ≤1

3 p[{c2, c4}, c4]

3 + p[{c4, c5}, c4]

6 ≤

X

A⊆C x[A]p[A, c4] ≤1

3 p[{c2, c5}, c5]

3 + p[{c4, c5}, c5]

6 ≤

X

A⊆C x[A]p[A, c5] ≤1

3

Similarly, condition 2 of Lemma 11 yields p[{c2, c4}, c2] + p[{c2, c4}, c4] > 1 (3) p[{c2, c5}, c2] + p[{c2, c5}, c5] > 1 (4) p[{c4, c5}, c4] > 1 and p[{c4, c5}, c5] > 1. (5) If we multiply (3)-(4) by −1/3, multiply (5) by −1/6, and add them up together with the previous three inequalities from Condition 1, we get the contradiction 0 < 0.

## Conclusion

& Future Directions We used modifications to MILP to explore core’s logical relationship with other axioms, proving minimal incomparability results. A natural next step is to use our program to search for incompatibility: Does there exist a profile for which no core-stable committee satisfies (weak) priceability? This is currently an open problem. Similarly, to the best of our knowledge, whether the core is compatible with other axioms such as EJR+ and committee monotonicity is not known. These axioms can be incorporated into MILP, searching for counterexamples of simultaneous satisfiability. Another direction is to extend our tools to settings different from (but related to) approval elections, such as “thumbs up and down voting”, where each voter has three options per candidate: approval, neutral, and disapproval (Kraiczy et al. 2025). Overall, we hope our framework will open up new directions for using MILPs in social choice settings.

16679

<!-- Page 8 -->

## Acknowledgements

We thank Chase Norman, Ulle Endriss, Paul G¨olz, Dominik Peters, Kangning Wang, Jan Vondr´ak, Edith Elkind, Markus Brill, and Yiheng Shen for helpful discussions and feedback at various stages of this project. R.E.B., E.T., and V.C. thank the Cooperative AI Foundation, Macroscopic Ventures (formerly Polaris Ventures / the Center for Emerging Risk Research), and Jaan Tallinn’s donor-advised fund at Founders Pledge for financial support. R.E.B. and E.T. are also supported by the Cooperative AI PhD Fellowship. M.H. is supported by the National Science Foundation (NSF) under grant CCF-2415773. L.X. acknowledges NSF 2450124, 2517733, and 2518373 for support.

## References

Arrow, K. 1963. Social choice and individual values. New Haven: Cowles Foundation, 2nd edition. 1st edition 1951. Aziz, H.; Brill, M.; Conitzer, V.; Elkind, E.; Freeman, R.; and Walsh, T. 2017. Justified Representation in Approval- Based Committee Voting. Social Choice and Welfare. Aziz, H.; Elkind, E.; Huang, S.; Lackner, M.; Sanchez- Fernandez, L.; and Skowron, P. 2018. On the Complexity of Extended and Proportional Justified Representation. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). Biere, A.; Heule, M.; van Maaren, H.; and Walsh, T., eds. 2021. Handbook of Satisfiability - Second Edition, volume 336 of Frontiers in Artificial Intelligence and Applications. IOS Press. Brandl, F.; Brandt, F.; Eberl, M.; and Geist, C. 2018. Proving the Incompatibility of Efficiency and Strategyproofness via SMT Solving. The Journal of the ACM. Brandl, F.; Brandt, F.; Geist, C.; and Hofbauer, J. 2019. Strategic Abstention based on Preference Extensions: Positive Results and Computer-Generated Impossibilities. Journal of Artificial Intelligence Research. Brandl, F.; Brandt, F.; Peters, D.; and Stricker, C. 2021. Distribution Rules Under Dichotomous Preferences: Two Out of Three Ain’t Bad. In Proceedings of the ACM Conference on Economics and Computation (EC). Brandt, F.; and Geist, C. 2016. Finding Strategyproof Social Choice Functions via SAT Solving. Journal of Artificial Intelligence Research. Brandt, F.; Geist, C.; and Peters, D. 2017. Optimal bounds for the no-show paradox via SAT solving. Mathematical Social Sciences. Brill, M.; G¨olz, P.; Peters, D.; Schmidt-Kraepelin, U.; and Wilker, K. 2020. Approval-Based Apportionment. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). Brill, M.; and Peters, J. 2023. Robust and Verifiable Proportionality Axioms for Multiwinner Voting. In Proceedings of the ACM Conference on Economics and Computation (EC). Casey, M. M.; and Elkind, E. 2025. Justified Representation: From Hare to Droop. In Proceedings of the Conference on Web and Internet Economics (WINE).

Chaudhury, B. R.; Li, L.; Kang, M.; Li, B.; and Mehta, R. 2022. Fairness in Federated Learning via Core-Stability. In Proceedings of the Annual Conference on Neural Information Processing Systems (NeurIPS). Chaudhury, B. R.; Murhekar, A.; Yuan, Z.; Li, B.; Mehta, R.; and Procaccia, A. D. 2024. Fair Federated Learning via the Proportional Veto Core. In Proceedings of the International Conference on Machine Learning (ICML). Cheng, Y.; Jiang, Z.; Munagala, K.; and Wang, K. 2019. Group Fairness in Committee Selection. In Proceedings of the ACM Conference on Economics and Computation (EC). Conitzer, V.; Freedman, R.; Heitzig, J.; Holliday, W. H.; Jacobs, B. M.; Lambert, N.; Moss´e, M.; Pacuit, E.; Russell, S.; Schoelkopf, H.; Tewolde, E.; and Zwicker, W. S. 2024. Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback. In Proceedings of the International Conference on Machine Learning (ICML). Conitzer, V.; and Sandholm, T. 2002. Complexity of Mechanism Design. In Proceedings of the Uncertainty in Artificial Intelligence Conference (UAI). Conitzer, V.; and Sandholm, T. 2004. Self-interested Automated Mechanism Design and Implications for Optimal Combinatorial Auctions. In Proceedings of the ACM Conference on Electronic Commerce (EC). Damle, S.; Padala, M.; and Gujar, S. 2024. Designing Redistribution Mechanisms for Reducing Transaction Fees in Blockchains. In Proceedings of the International Conference on Autonomous Agents and Multiagent Systems. Endriss, U. 2020. Analysis of One-to-One Matching Mechanisms via SAT Solving: Impossibilities for Universal Axioms. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). Geist, C.; and Endriss, U. 2011. Automated Search for Impossibility Theorems in Social Choice Theory: Ranking Sets of Objects. Journal of Artificial Intelligence Research. Geist, C.; and Peters, D. 2017. Computer-Aided Methods for Social Choice Theory. In Endriss, U., ed., Trends in Computational Social Choice. AI Access. Gibbard, A. 1973. Manipulation of Voting Schemes: A General Result. Econometrica. Guo, M.; and Conitzer, V. 2009. Worst-Case Optimal Redistribution of VCG Payments in Multi-Unit Auctions. Games and Economic Behavior. Guo, M.; and Conitzer, V. 2010. Computationally Feasible Automated Mechanism Design: General Approach and Case Studies. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). Gurobi Optimization, LLC. 2024. Gurobi Optimizer Reference Manual. Janson, S. 2018. Thresholds quantifying proportionality criteria for election methods. arXiv preprint arXiv:1810.06377. Jiang, Z.; Munagala, K.; and Wang, K. 2020. Approximately Stable Committee Selection. In Proceedings of the Annual Symposium on Theory of Computing (STOC).

16680

<!-- Page 9 -->

Kraiczy, S.; Papasotiropoulos, G.; Pierczy´nski, G.; and Skowron, P. 2025. Proportionality in Thumbs Up and Down Voting. arXiv preprint arXiv:2503.01985. Lackner, M.; and Skowron, P. 2022. Multi-Winner Voting with Approval Preferences. SpringerBriefs in Intelligent Systems. Springer International Publishing. Li, Y.; and Conitzer, V. 2015. Cooperative Game Solution Concepts that Maximize Stability under Noise. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). Maschler, M.; Peleg, B.; and Shapley, L. S. 1979. Geometric Properties of the Kernel, Nucleolus, and Related Solution Concepts. Mathematics of Operations Research. Mennle, T.; and Seuken, S. 2016. The Pareto Frontier for Random Mechanisms. In Proceedings of the ACM Conference on Economics and Computation (EC). Moulin, H. 1988. Condorcet’s principle implies the no show paradox. Journal of Economic Theory. Munagala, K.; and Shen, Y. 2024. Core Stability in Participatory Budgeting: Approximations and Open Questions. In New Directions in Social Choice at EC 2024. Munagala, K.; Shen, Y.; and Wang, K. 2022. Auditing for Core Stability in Participatory Budgeting. In Proceedings of the Conference on Web and Internet Economics (WINE). Munagala, K.; Shen, Y.; Wang, K.; and Wang, Z. 2021. Approximate Core for Committee Selection via Multilinear Extension and Market Clearing. In Proceedings of the Annual ACM-SIAM Symposium on Discrete Algorithms. Peters, D. 2018. Proportionality and Strategyproofness in Multiwinner Elections. In Proceedings of the International Conference on Autonomous Agents and Multiagent Systems. Peters, D. 2025. The Core of Approval-Based Committee Elections with Few Seats. In Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI). Peters, D.; Pierczy´nski, G.; and Skowron, P. 2021. Proportional Participatory Budgeting with Additive Utilities. In Proceedings of the Annual Conference on Neural Information Processing Systems (NeurIPS). Peters, D.; and Skowron, P. 2020. Proportionality and the Limits of Welfarism. In Proceedings of the ACM Conference on Economics and Computation (EC). Satterthwaite, M. A. 1975. Strategy-proofness and Arrow’s conditions: Existence and correspondence theorems for voting procedures and social welfare functions. Journal of Economic Theory. Shapley, L. S.; and Shubik, M. 1966. Quasi-Cores in a Monetary Economy with Nonconvex Preferences. Econometrica. Tang, P.; and Lin, F. 2008. A Computer-Aided Proof to Gibbard-Satterthwaite Theorem. Technical report, Department of Computer Science, Hong Kong University of Science and Technology. Tang, P.; and Lin, F. 2009. Computer-aided proofs of Arrow’s and other impossibility theorems. Artificial Intelligence. Xia, L. 2025. A Linear Theory of Multi-Winner Voting. arXiv preprint arXiv:2503.03082.

Yang, H.; Liu, Z.; Liu, J.; Dong, C.; and Momma, M. 2024. Federated Multi-Objective Learning. In Proceedings of the Annual Conference on Neural Information Processing Systems (NeurIPS).

16681
