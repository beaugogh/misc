---
title: "Beyond the Lower Bound: Bridging Regret Minimization and Best Arm Identification in Lexicographic Bandits"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39959
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39959/43920
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Beyond the Lower Bound: Bridging Regret Minimization and Best Arm Identification in Lexicographic Bandits

<!-- Page 1 -->

Beyond the Lower Bound: Bridging Regret Minimization and Best Arm

Identification in Lexicographic Bandits

Bo Xue1,2, Yuanyu Wan3, Zhichao Lu1, Qingfu Zhang1,2*

## 1 Department of Computer Science, City University of Hong Kong, Hong Kong, China 2 The City University of Hong Kong

Shenzhen Research Institute, Shenzhen, China 3 School of Software Technology, Zhejiang University, Ningbo, China boxue4-c@my.cityu.edu.hk, wanyy@zju.edu.cn, {zhichao.lu, qingfu.zhang}@cityu.edu.hk

## Abstract

In multi-objective decision-making with hierarchical preferences, lexicographic bandits provide a natural framework for optimizing multiple objectives in a prioritized order. In this setting, a learner repeatedly selects arms and observes reward vectors, aiming to maximize the reward for the highestpriority objective, then the next, and so on. While previous studies have primarily focused on regret minimization, this work bridges the gap between regret minimization and best arm identification under lexicographic preferences. We propose two elimination-based algorithms to address this joint objective. The first algorithm eliminates suboptimal arms sequentially, layer by layer, in accordance with the objective priorities, and achieves sample complexity and regret bounds comparable to those of the best single-objective algorithms. The second algorithm simultaneously leverages reward information from all objectives in each round, effectively exploiting cross-objective dependencies. Remarkably, it outperforms the known lower bound for the single-objective bandit problem, highlighting the benefit of cross-objective information sharing in the multi-objective setting. Empirical results further validate their superior performance over baselines.

Extended version — https://arxiv.org/abs/2511.05802

## Introduction

The multi-armed bandit (MAB) problem is a foundational framework for sequential decision-making under uncertainty (Robbins 1952; Lai and Robbins 1985; Auer 2002), with widespread applications in domains such as online recommendation systems (Schwartz, Bradlow, and Fader 2017), clinical trials (Villar, Bowden, and Wason 2015), and adaptive routing (Awerbuch and Kleinberg 2008). In the classical MAB setting (Bubeck and Cesa-Bianchi 2012), a learner repeatedly selects one arm from a finite set of K arms, each associated with an unknown reward distribution. Upon each selection, the learner observes a stochastic reward sampled from the distribution of the chosen arm. Depending on the learning objective, bandit algorithms are generally categorized into two primary paradigms: (1) regret minimization (RM), which aims to minimize the cu-

*Qingfu Zhang is the corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

mulative regret incurred by not always selecting the optimal arm (Auer, Cesa-Bianchi, and Fischer 2002; Abbasiyadkori, P´al, and Szepesv´ari 2011; Lykouris, Mirrokni, and Paes Leme 2018; Xue et al. 2020); and (2) best arm identification (BAI), which aims to identify the optimal arm using as few samples as possible (Audibert and Bubeck 2010; Karnin, Koren, and Somekh 2013; Jamieson et al. 2014; Kaufmann, Capp´e, and Garivier 2016; Jin et al. 2024).

While traditional bandit algorithms focus on optimizing a scalar reward (Auer, Cesa-Bianchi, and Fischer 2002; Xue et al. 2023), many real-world applications involve multiple, often conflicting objectives (Xie et al. 2021; Shu et al. 2024; Cheng et al. 2025), which motivate the study of the multi-objective bandit problem (Drugan and Nowe 2013). Several formulations have been proposed in this context, including scalarized regret minimization (Q. Yahyaa, M. Drugan, and Manderick 2015), Pareto regret minimization (Lu et al. 2019; Xu and Klabjan 2023), and Pareto set identification (Auer et al. 2016). These methods offer different strategies for managing trade-offs among objectives, but generally assume that all objectives are equally important or can be aggregated into a single scalar value. However, in many practical scenarios, objectives have inherently different priorities. For instance, in medical diagnosis (Alkaabneh and Diabat 2023), patient safety typically outweighs considerations such as cost or treatment speed; in recommendation systems (Li et al. 2023), fairness may be prioritized over user engagement.

An effective framework for modeling such hierarchical decision-making is lexicographic bandits (Tekin and Turgay 2018; H¨uy¨uk and Tekin 2021; Xue et al. 2025a), where the agent seeks to optimize multiple objectives according to the lexicographic order. Unlike approaches that aggregate objectives into a single scalar using linear weights, the lexicographic bandit framework preserves the dominance structure: higher-priority objectives must be optimized before lower-priority ones are considered. This formulation provides a more faithful representation of structured decisionmaking in sensitive applications such as hyperparameter optimization (Zhang et al. 2023) and multi-criteria resource allocation (Kurokawa, Procaccia, and Shah 2018).

Research on lexicographic bandits has attracted increasing attention in recent years, with most studies focusing on the RM task (Tekin and Turgay 2018; H¨uy¨uk and Tekin

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27414

<!-- Page 2 -->

2021; Cheng et al. 2024; Xue et al. 2024, 2025b,c). However, to the best of our knowledge, another significant task in the bandit literature, BAI, has not yet been explored in the context of lexicographic bandits. In many real-world scenarios, it is important to minimize regret during the learning phase while also accurately identifying the optimal arm at the end (Zhong, Cheung, and Tan 2023). For instance, in clinical trials, ethical considerations require providing effective treatments during the study (low regret), while the ultimate goal is to determine the most effective treatment (accurate BAI). These dual requirements motivate a central research question:

Can we design algorithms for lexicographic bandits that effectively unify RM and BAI?

In this work, we answer this question affirmatively and demonstrate that a unified treatment of RM and BAI in lexicographic bandits is not only possible, but also yields surprising benefits. In particular, the rich multi-objective feedback naturally accelerates the elimination of suboptimal arms during the BAI process, thereby reducing the need to explore inferior actions and mitigating cumulative regret. This positive feedback loop between accurate identification and efficient learning highlights an unexpected advantage of jointly addressing BAI and RM in lexicographic bandits.

This paper presents the first algorithmic framework for lexicographic bandits that simultaneously tackles both RM and BAI tasks. Our main contributions are as follows:

• We propose a simple yet effective elimination-based algorithm, LexElim-Out, which sequentially filters suboptimal arms, starting from the highest-priority objective and proceeding to the lowest. This top-down elimination strategy ensures that lower-priority objectives are only considered after higher-priority objectives have been sufficiently optimized. Theoretically, LexElim-Out matches the best-known problem-dependent BAI guarantees for the primary objective, without compromising performance when optimizing additional objectives.

• We further develop an enhanced algorithm, LexElim- In, which eliminates arms using joint reward information from all objectives in each round. By simultaneously incorporating information across objectives during each decision step, LexElim-In accelerates the identification and elimination of suboptimal arms. We show that it surpasses the known lower bounds for single-objective bandits in both regret and sample complexity, highlighting the advantage of exploiting the multi-objective structure.

• LexElim-In also enjoys anytime performance guarantees. Specifically, we establish a minimax regret bound of eO(Λi(λ) ·

√

Kt) for each objective i ∈[m] at any round t ≥1, ensuring that the regret grows at most at a square-root rate over time. This bound is comparable to the best-known results in single-objective bandits, while operating in a more challenging multi-objective setting.

• Through extensive experiments on synthetic data, we demonstrate that both LexElim-Out and LexElim-In outperform existing baselines in cumulative regret and BAI sample complexity. Notably, LexElim-In exhibits superior performance on some instances, validating the benefit of joint exploitation of multi-objective reward signals.

## Preliminaries

This paper studies the lexicographic bandit problem, where a learner selects arms to simultaneously optimize multiple objectives that are ranked according to their importance.

Let K ∈N+ denote the number of objectives, and m ∈ N+ be the number of objectives. For any N ∈N+, let [N] = {1, 2,..., N} denote the index set. At each round t ∈[T], the learner chooses an arm at ∈[K] and receives a stochastic reward vector rt(at) = [r1 t (at), r2 t (at),..., rm t (at)] ∈ Rm. The component ri t(at) corresponds to the reward for the i-th objective and is independently drawn from a 1sub-Gaussian distribution with an unknown mean µi(at) ∈ [0, 1]. That is, for all β ∈R and i ∈[m],

E[eβri t(at)] ≤exp β2/2

, µi(at) = E[ri t(at)]. (1)

The key challenge in lexicographic bandits is managing the hierarchical structure of objectives: the learner must optimize the most important objective first, followed by the second-most important, and so on. To formalize this, we adopt the standard notion of lexicographic dominance from prior work (H¨uy¨uk and Tekin 2021; Xue et al. 2024).

Definition 1 (Lexicographic Order) Let a1, a2 ∈[K] be two arms. We say that a1 lexicographically dominates a2 if there exists an index i ∈[m] such that µj(a1) = µj(a2) for all j < i, and µi(a1) > µi(a2).

An illustrate example is that the arm with expected rewards [5, 5, 2] lexicographically dominates the arm with expected rewards [5, 4, 8], even though the latter has a higher value on the third objective. Lexicographic order induces a total order over arms, enabling the comparison of any two arms and thereby defining the notion of the lex-optimal arm.

Definition 2 (Lex-optimal Arm) An arm a∗is lex-optimal if no other arm in [K] lexicographically dominates it.

We study two classical goals in the bandit literature, and adapt them to the lexicographic multi-objective setting. The first is Regret Minimization (RM), which aims to minimize the cumulative regret for each objective over T rounds,

Ri(T) = T · µi(a∗) −

T X t=1 µi(at), i ∈[m].

The second is Best Arm Identification (BAI) with fixed confidence. Given a confidence level δ ∈(0, 1), the goal is to identify the optimal arm (or optimal arm set) with probability at least 1 −δ, using as few samples as possible.

Unlike the single-objective setting where the optimal arm is uniquely defined, in the multi-objective case, different objectives may induce different optimal arms. To capture this, we consider the following two types of optimal arm sets for each objective i ∈[m]:

• O∗(i) = {a ∈[K] | µj(a) = µj(a∗) for all j ∈[i]}: the set of arms that match a∗on the top i objectives;

27415

<!-- Page 3 -->

## Algorithm

Sample Complexity Regret Bound # Objectives

Auer, Cesa-Bianchi, and Fischer (2002) – eO

P

∆(a)>0

1 ∆(a)

1

Degenne and Perchet (2016) – O

√

KT

1

Lattimore (2018) (Lower Bound) – Ω

P

∆(a)>0

1 ∆(a)

1

Karnin, Koren, and Somekh (2013) eO

P

∆(a)>0

1 (∆(a))2

– 1

Jamieson et al. (2014) (Lower Bound) Ω

P

∆(a)>0

1 (∆(a))2

– 1

Degenne et al. (2019) eO

P

∆(a)>0

1 (∆(a))2 eO

P

∆(a)>0

1 ∆(a)

1

LexElim-Out (Ours) eO

Pi j=1

P a∈S(j)

1 (∆j(a))2 eO

Pi j=1

P a∈S(j)

∆i(a) (∆j(a))2 i ∈[m]

LexElim-In (Ours) eO

P

∆i(a)>0

1 (˜∆(a))2 eO

P

∆i(a)>0

∆i(a) (˜∆(a))2 eO

Λi(λ) ·

√

KT i ∈[m]

1. ∆i(a) = µi(a∗) −µi(a) for all a ∈[K] and i ∈[m], where a∗is the lex-optimal arm defined in Definition 2. 2. For single-objective works, we simplify the notation by letting ∆(a):= ∆1(a). 3. S(i) = {a ∈O∗(i −1) | ∆i(a) > 0}, O∗(i −1) = {a ∈[K] | µj(a∗) = µj(a), ∀j ∈[i −1]} and O∗(0) = [K].

4. ˜∆(a) = max i∈[m]

n

∆i(a) Λi(λ) · I[∆i(a) > 0]

o

, where Λi(λ) = 1 + λ + · · · + λi−1 and λ ≥0 is defined in Eq. (2).

**Table 1.** Overview of Our Results and Comparisons with RM and BAI Methods: Since ˜∆(a) ≥∆1(a) for all a ∈[K], LexElim-In outperforms the lower bounds of the single-objective problem (Jamieson et al. 2014; Lattimore 2018).

• e O∗(i) = {a ∈[K] | µi(a) ≥µi(a∗)}: the set of arms that are optimal with respect to the i-th objective alone.

Let T i(δ) and eT i(δ) denote the number of samples used to identify O∗(i) and e O∗(i), respectively. Thus, the sample complexity of identifying a∗is T m(δ) or maxi∈[m] eT i(δ).

Finally, we introduce a parameter λ to capture the tradeoffs among conflicting objectives. In the lexicographic bandit problem, we assume that for any i ≥2 and a ∈[K], µi(a) −µi(a∗) ≤λ · max j∈[i−1]{µj(a∗) −µj(a)}. (2)

## Related Work

We review bandit work on four directions: regret minimization (RM), best arm identification (BAI), joint optimization of RM and BAI, and multi-objective bandits (MOB).

RM. The seminal work of Robbins (1952) initiated the study of the MAB problem. A foundational algorithm for minimizing regret in stochastic MABs is the Upper Confidence Bound (UCB) algorithm (Auer, Cesa-Bianchi, and Fischer 2002), which achieves a problem-dependent regret bound of eO

P

∆(a)>0 1/∆(a)

. To improve worst-case performance, Audibert and Bubeck (2009) proposed the MOSS algorithm, which attains the minimax-optimal regret bound of O(

√

KT). This was further improved by Degenne and Perchet (2016), who developed an anytime variant of MOSS that removes the need for prior knowledge of the time horizon T, thereby improving its practicality. Additionally, Lattimore (2018) established a fundamental lower bound of

Ω

P

∆(a)>0 1/∆(a)

, highlighting the intrinsic complexity of the problem. These foundational results have been extended to structured bandit settings, such as linear bandits (Dani, Hayes, and Kakade 2008), graphical bandits (Alon et al. 2015) and combinatorial bandits (Chen et al. 2016).

BAI. Existing work on BAI can be categorized into two primary settings: (a) Fixed-confidence setting: The algorithm aims to identify the best arm with probability at least 1 −δ, using as few samples as possible. Early approaches include the Successive Elimination algorithm (Even-Dar, Mannor, and Mansour 2006), which sequentially discards suboptimal arms based on empirical comparisons. Later works (Karnin, Koren, and Somekh 2013; Garivier and Kaufmann 2016) introduced more refined strategies that achieve near-optimal sample complexity by adaptively allocating samples to competitive arms. Jamieson et al. (2014) established a lower bound showing that the sample complexity of any algorithm is at least Ω(P

∆(a)>0 1/(∆(a))2). (b) Fixed-budget setting: Given a fixed budget T ∈N, the objective is to minimize the probability of incorrect identification at time T. Audibert and Bubeck (2010) first studied this setting and designed an algorithm based on successive rejects, proved its optimality up to logarithmic factors. A subsequent work of Karnin, Koren, and Somekh (2013) further improved the theoretic guarantees, leaving only doublylogarithmic gap. Carpentier and Locatelli (2016) constructed lower bounds to confirm the near-optimality of these results.

RM and BAI. While RM and BAI have traditionally been treated as separate goals, recent studies have sought to address them jointly. Degenne et al. (2019) explored both

27416

<!-- Page 4 -->

goals with a fixed confidence and introduced an algorithm UCBα, where the parameter α > 1 controls the trade-off between regret and sample complexity. Subsequently, Zhong, Cheung, and Tan (2023) quantified the trade-off between RM and BAI in the fixed-budget setting. In parallel, Zhang and Ying (2023) developed algorithms that achieve asymptotic regret optimality in Gaussian bandit models. Most recently, Yang, Tan, and Jin (2024) established an informationtheoretic lower bound for BAI with minimal regret and proposed an algorithm that attains asymptotic optimality.

MOB. Multi-objective bandits aim to balance competing objectives, often without a unique optimal solution. Prior research has explored various notions of optimality and preference structures to address this challenge. Early studies focus extended the Pareto optimality concept to online learning (Auer et al. 2016; Kone, Kaufmann, and Richert 2024; Crepon, Garivier, and M Koolen 2024), where the learner aims to approximate the Pareto front. Another line of work employs scalarization techniques (Drugan and Nowe 2013; Q. Yahyaa, M. Drugan, and Manderick 2015; Wanigasekara et al. 2019) to guide learning, based on utility functions or user-specified preferences. Lexicographic bandits, a specific form of preference-based MOB, have been studied under the RM framework (H¨uy¨uk and Tekin 2021; Tekin 2019; Xue et al. 2024). Our work contributes the first unified framework that simultaneously addresses RM and BAI under lexicographic preference, and we theoretically demonstrates how joint rewards signals lead to improved performance.

Algorithms

In this section, we propose two algorithms tailored for lexicographic bandits: LexElim-Out and LexElim-In.

Warm-up: LexElim-Out

We begin by introducing LexElim-Out, a warm-up algorithm for the lexicographic MAB problem. This algorithm follows an outer-layer elimination strategy, where arms are pruned layer-by-layer according to the lexicographic priority of objectives. Details are provided in Algorithm 1.

LexElim-Out requires prior knowledge of |O∗(i)|, i.e., the number of arms that are optimal up to objective i ∈[m]. This aligns with common practices in the single-objective BAI literature (Bubeck, Munos, and Stoltz 2009; Audibert and Bubeck 2010; Zhang and Ying 2023), where the optimal arm is typically assumed to be unique.

Given a confidence parameter δ ∈(0, 1), the number of arms K, the number of objectives m, and the cardinalities |O∗(i)| for all i ∈[m], LexElim-Out proceeds as follows. For each arm a ∈[K] and objective i ∈[m], it initializes the empirical mean reward ˆµi(a) and pull count n(a) to zero, and the confidence width c(a) to +∞. The active arm set is initialized as A1 = [K], and the round index as t = 1.

Then, LexElim-Out performs iterations over the objectives in order of priority, from the most to the least important. For each objective i ∈[m], it repeatedly performs elimination rounds until the size of the active arm set is reduced to the known optimal set size, i.e., |At| = |O∗(i)|. In each

## Algorithm

1: Outer-layer Active Arm Elimination in Lexicographic Bandits (LexElim-Out)

Input: δ ∈(0, 1), K, m, {|O∗(i)|, ∀i ∈[m]}

1: Initialize empirical mean ˆµi(a) = 0, counter n(a) = 0, and confidence width c(a) = +∞for i ∈[m], a ∈[K] 2: Initialize active set A1 = [K] and round counter t = 1 3: for i = 1, 2,..., m do 4: while |At| > |O∗(i)| do 5: Choose the arm at = argmaxa∈At c(a) 6: ˆai t = argmaxa∈At ˆµi(a) 7: At+1 = {a ∈At|ˆµi(ˆai t) −ˆµi(a) ≤2c(at)} 8: Play at and observe reward vectors rt(at) 9: Update ˆµi(at) for all i ∈[m] by Eq. (3) 10: Update n(at) and c(at) by Eq. (4) 11: Set t = t + 1 12: end while 13: end for 14: Output the arm in At round, the algorithm selects the arm with the highest uncertainty, at = argmax a∈At c(a).

It then identifies the empirical best arm with respect to the current objective, i.e., ˆai t = arg maxa∈At ˆµi(a). The active arm set is updated by retaining only those arms whose empirical means are within 2c(at) of the best empirical arm ˆai t,

At+1 = {a ∈At | ˆµi(ˆai t) −ˆµi(a) ≤2c(at)}. This ensures that arms that are suboptimal on the i-th objective are eliminated.

After the elimination step, LexElim-Out plays the most uncertain arm at and observes its reward vector rt(at) = [r1 t (at), r2 t (at),..., rm t (at)]. The empirical mean for each objective i ∈[m] is updated using an incremental average,

ˆµi(at) = n(at) · ˆµi(at) + ri t(at) n(at) + 1. (3)

Next, the pull count n(at) is incremented, and the confidence width c(at) is updated by a concentration inequality, n(at) = n(at) + 1, c(at) = s n(at) log

6Km · n(at)

δ

.

(4)

The round index t is then incremented to t + 1.

Once all objectives have been processed, LexElim-Out terminates and outputs the sole remaining arm in the final active set. The regret bounds and sample complexity of the algorithm are established in Theorems 1 and 2, respectively. Theorem 1 Suppose that Eq. (1) holds, define S(i) = {a ∈ O∗(i −1) | ∆i(a) > 0} with O∗(0) = [K], and set γi(δ) = 64 log

392Km (∆i(a))2·δ

. With probability at least 1 −δ, for any objective i ∈[m], the regret of LexElim-Out satisfies

Ri(t) ≤ i X j=1

X a∈S(j)

γj(δ) · ∆i(a)

(∆j(a))2.

27417

<!-- Page 5 -->

Remark 1 Theorem 1 states that LexElim-Out achieves a regret bound of eO

Pi j=1

P a∈S(j)

∆i(a) (∆j(a))2 for any objec- tive i ∈[m], with the following key implications.

• For the primary objective (i = 1), its regret bound is eO

P

∆1(a)>0

1 ∆1(a)

, matching the known lower bound for single-objective bandits (Lattimore 2018). This ensures no performance degradation for the highest-priority objective when optimizing additional objectives. • For the secondary objective (i = 2), its regret bound includes two terms:

eO



 X

∆1(a)>0

∆2(a) (∆1(a))2





| {z } cross-objective cost

+ eO



X a∈S(2)

1 ∆2(a)





| {z } single-objective term

.

The second term aligns with the regret bound in the single-objective setting. The first term captures the cost due to the need to prioritize the first objective. This cost becomes negligible if (∆1(a))2 ≫∆2(a). The same decomposition can be applied to i > 2, where the regret bound includes cumulative cross-objective costs from all higher-priority objectives j < i, and a local term that matches the single-objective bound for objective i. Theorem 2 Suppose the same conditions and notations as in Theorem 1. With probability at least 1 −δ, for any objective i ∈[m], the number of samples required by LexElim- Out to identify O∗(i) satisfies

T i(δ) ≤ i X j=1

X a∈S(j)

γj(δ) (∆j(a))2.

Remark 2 LexElim-Out uses eO

Pi j=1

P a∈S(j)

1 (∆j(a))2 samples to identify the optimal arm set of the first i objectives. In particular, for the first objective, the sample complexity simplifies to eO

P

∆1(a)>0

1 (∆1(a))2

, which matches the known lower bound for single-objective bandits (Jamieson et al. 2014). This implies that LexElim-Out identifies the optimal arm for the primary objective as efficiently as state-of-the-art single-objective algorithms (Karnin, Koren, and Somekh 2013). For general i ∈[m], the bound reflects that identifying the lex-optimal arm requires solving a sequence of BAI problems, where suboptimal arms for higher-priority objectives are progressively eliminated before being evaluated on lower-priority ones.

Improved Algorithm: LexElim-In LexElim-Out handles objectives layer by layer, it ignores lower-priority objectives when optimizing higher-priority ones. As a result, the arm selection for lower-priority objectives in early rounds is purely random, lacking any targeted exploration. To address this limitation, we propose an improved algorithm, LexElim-In, which adopts an inner-layer elimination strategy that leverages information from all objectives throughout the decision-making process. The complete procedure is presented in Algorithm 2.

## Algorithm

2: Inner-layer Active Arm Elimination in Lexicographic Bandits (LexElim-In)

Input: δ ∈(0, 1), K, m, λ ≥0

1: Initialize empirical mean ˆµi(a) = 0, counter n(a) = 0, and confidence width c(a) = +∞for i ∈[m], a ∈[K] 2: Initialize active set A1 = [K] and round counter t = 1 3: while |At| > 1 do 4: Choose the arm at = argmaxa∈At c(a) 5: Initialize the arm set A0 t = At 6: for i = 1, 2,..., m do 7: ˆai t = argmaxa∈Ai−1 t ˆµi(a)

8: Ai t = {a ∈Ai−1 t |ˆµi(ˆai t)−ˆµi(a) ≤(2+4λ+· · ·+ 4λi−1) · c(at)} 9: end for 10: Play at and observe reward vectors rt(at) 11: Update ˆµi(at) for all i ∈[m] by Eq. (3) 12: Update n(at) and c(at) by Eq. (4) 13: Update At+1 = Am t and t = t + 1 14: end while 15: Output the arm in At

Given a confidence level δ ∈(0, 1), the number of arms K, the number of objectives m, and a trade-off parameter λ ≥0, LexElim-In begins with an initialization phase similar to that of LexElim-Out. Specifically, for each arm a ∈[K] and each objective i ∈[m], the empirical mean reward ˆµi(a) and pull count n(a) are set to zero, and the confidence width c(a) is initialized to +∞. The initial active set of arms is defined as A1 = [K], and the round index is initialized as t = 1.

At each round, LexElim-In selects the arm at ∈At with the largest confidence width c(a), corresponding to the highest uncertainty, and plays this arm. It then updates the active arm set through a layered filtering process that incorporates empirical means across all objectives in a nested fashion.

Specifically, let A0 t = At and for each objective i = 1, 2,..., m, LexElim-In identifies the empirical best arm ˆai t = arg maxa∈Ai−1 t ˆµi(a), and eliminates arms in Ai−1 t whose empirical mean falls below that of ˆai t by more than a scaled confidence threshold. Formally, the updated set is

Ai t = a ∈Ai−1 t | ˆµi(ˆai t) −ˆµi(a) ≤

2 + 4λ + · · · + 4λi−1 · c(at)

.

(5)

The scaling factor 2+4λ+· · ·+4λi−1 grows geometrically with i, allowing lower-priority objectives to tolerate larger reward gaps while still contributing to elimination decisions.

After completing the elimination process across all m objectives, LexElim-In updates the active set to At+1 = Am t. It then pulls arm at to observe the full reward vector rt(at) = [r1 t (at),..., rm t (at)]. For each objective i ∈[m], the empirical mean ˆµi(at) is updated using an incremental average defined in Eq. (3). The pull count n(at) and the confidence width c(at) are then updated by Eq. (4). The round index is incremented, and the procedure repeats until the active set contains only a single arm.

27418

<!-- Page 6 -->

The key innovation of LexElim-In is its cross-objective elimination strategy, which utilizes information from all objectives at each round. By jointly incorporating elimination evidence across objectives, LexElim-In more efficiently eliminates suboptimal arms, especially when lower-priority objectives provide stronger signals. This approach leads to faster identification of the lexicographic optimum compared to LexElim-Out, albeit at the cost of requiring the prior knowledge λ. Formal regret and sample complexity guarantees are presented in Theorems 3 and 4, respectively.

Theorem 3 Suppose that Eq. (1) and Eq. (2) hold. Define

Λi(λ) = i−1 X j=0 λj, and γi(δ) = 64 log

392Km (∆i(a))2 · δ

.

With probability at least 1−δ, for any objective i ∈[m], the regret of LexElim-In satisfies

Ri(t) ≤

X

∆i(a)>0 min j∈[m]

(Λj(λ))2 · ∆i(a) · γj(δ)

(∆j(a))2 · I(∆j(a) > 0)

.

Remark 3 For the primary objective (i = 1), the regret incurred due to ∆1(a) > 0 is bounded by min j∈[m]

∆1(a) · (Λj(λ))2

(∆j(a))2 · I(∆j(a) > 0)

≤ 1 ∆1(a), where the right-hand side matches the known lower bound (Lattimore 2018). The existence of minj∈[m] allows the bound to go beyond the lower bound: if for some j ≥2, the suboptimality gap ∆j(a) is much larger than ∆1(a) · Λj(λ), the corresponding regret term can become significantly smaller than 1/∆1(a). Thus, LexElim-In can adaptively exploit auxiliary objectives to accelerate learning.

Moreover, while the gap-dependent bound in Theorem 3 highlights how LexElim-In can exploit the relative gap structures among objectives to reduce regret, it remains essential to understand the algorithm’s behavior in the worst case.

Corollary 1 Suppose the same conditions and notations as in Theorem 3. With probability at least 1 −δ, for any objective i ∈[m], the regret of LexElim-In satisfies

Ri(t) ≤eO

Λi(λ) ·

√

Kt

.

Corollary 1 shows that for any objective i ∈[m], the worstcase regret of LexElim-In grows at most as eO(Λi(λ)

√

Kt). This matches the minimax bound eO(

√

Kt) of singleobjective bandits (Degenne and Perchet 2016), up to the factor Λi(λ). Hence, LexElim-In achieves minimax-optimal regret rates in terms of K and t. Since Λ1(λ) = 1, the regret for the highest-priority objective remains unaffected even if optimizing lower-priority objectives.

Theorem 4 Suppose the same conditions and notations as in Theorem 3. With probability at least 1 −δ, for any objective i ∈[m], the number of samples required by LexElim-In to identify e O∗(i) satisfies eT i(δ) ≤

X

∆i(a)>0 min j∈[m]

(Λj(λ))2 · γj(δ) (∆j(a))2 · I(∆j(a) > 0)

.

𝜇𝜇(𝑎𝑎∗)

𝜇𝜇2 𝜇𝜇1 𝜆𝜆= 0

1

1 𝑂𝑂

(a) 𝜆𝜆= 0 𝜇𝜇(𝑎𝑎∗)

𝜇𝜇2 𝜆𝜆= 1

1

1 𝑂𝑂

(b) 𝜆𝜆= 1 𝜇𝜇1

**Figure 1.** Cross-objective Acceleration

Remark 4 Theorem 4 characterizes the sample complexity of LexElim-In for identifying the optimal arm set e O∗(i) for the i-th objective, revealing an objective-adaptive complexity. For each suboptimal arm a, the cost of distinguishing it is governed by the most distinguishable objective j ∈[m]. In particular, if some objective j exhibits a large suboptimality gap ∆j(a) for a given arm a, that arm can often be eliminated early, without requiring extensive exploration of other objectives. In such case, LexElim-In adaptively leverages the reward structure across objectives to accelerate the identification process. Notably, in the single-objective setting, the lower bound on sample complexity is known to be Ω(P

∆(a)>0

1 (∆(a))2) (Jamieson et al. 2014). Our bound recovers this result when i = 1, since Λ1(λ) = 1, and the minj∈[m] term ensures our result surpasses this lower bound.

Cross-objective Acceleration. Figure 1 illustrates how the second objective can accelerate BAI under varying degrees of trade-offs. The red star denotes the lex-optimal arm, while the circles represent suboptimal arms. In Figure 1(a), there is no conflict between other arms and the lex-optimal arm, resulting in λ = 0. The two yellow arms exhibit much larger reward gaps in the second objective than in the first, enabling LexElim-In to efficiently eliminate them by leveraging second objective information. Figure 1(b) shows a conflict between the lex-optimal arm and the red suboptimal arm, leading to λ = 1. In this case, only the yellow arm that is far from the optimal arm can be quickly eliminated, as the confidence term for the second objective is scaled by 2 + 4λ = 6, as specified in Eq. (5).

## Experiments

In this section, we evaluate the empirical performance of our proposed algorithms on both RM and BAI tasks. Baselines. There are three baselines. (a) EGE, which addresses BAI in single-objective MAB (Karnin, Koren, and Somekh 2013). (b) UCBα, designed to handle both BAI and RM in the single-objective MAB setting (Degenne et al. 2019). (c) PF-LEX, an algorithm tailored to RM in lexicographic MAB (H¨uy¨uk and Tekin 2021). Experimental Setup. Let m = 3, and the expected rewards across the three objectives are defined as: for any a ∈[K], µ1(a) = 1−minp∈{0.3,0.6,0.9} |a/K −p|, µ2(a) = 1−2×minp∈{0.5,0.8} |a/K−p|, µ3(a) = 1−2×|a/K−0.5|. This construction ensures that multiple arms are optimal for

27419

<!-- Page 7 -->

0.0 0.2 0.4 0.6 0.8 1.0 t 1e4

0

2

4

6

8

Regret

1e2

(a) 1st Objective

LexElim-Out LexElim-In PF-LEX UCB

0.0 0.2 0.4 0.6 0.8 1.0 t 1e4

0

2

4

6

8 1e2

(b) 2nd Objective

0.0 0.2 0.4 0.6 0.8 1.0 t 1e4

0

1

2

3

4 1e3

(c) 3rd Objective

**Figure 2.** Regret Comparison of Our Algorithms versus PF-LEX and UCBα: K = 10

1st 2nd 3rd 0.0

0.2

0.4

0.6

0.8

1.0

1.2

1.4

Samples

1e4

N/A N/A N/A N/A

(a) K=10

LexElim-Out LexElim-In EGE UCB

1st 2nd 3rd 0.0

0.2

0.4

0.6

0.8

1.0

1.2

1.4

1e4

N/A N/A N/A N/A

(b) K=20

1st 2nd 3rd 0.0

0.2

0.4

0.6

0.8

1.0

1.2

1.4

1e4

N/A N/A N/A N/A

(c) K=30

**Figure 3.** Sample Complexity Comparison of Our Algorithms versus EGE and UCBα

the higher-priority objectives: {0.3K, 0.6K, 0.9K} are optimal for the first objective, while {0.6K, 0.9K} are optimal for both the first and second objectives. To identify the unique lex-optimal arm a∗= 0.6K, all three objectives must be considered. Stochastic rewards ri t(a) are drawn from Gaussian distributions with mean µi(a) and variance 0.1. Each algorithm is run for 10 independent trials, and we report the average regret and sample complexity. RM Results. For those RM algorithms (UCBα, PF-LEX, LexElim-Out, and LexElim-In), we fix K = 10 and run each algorithm for T = 10,000. Figure 2 presents the cumulative regret over time, where Panels (a), (b), and (c) correspond to objectives 1, 2, and 3, respectively. LexElim-Out and LexElim-In exhibit uniformly sublinear regret growth across all objectives, demonstrating their ability to optimize multiple objectives simultaneously. In contrast, UCBα tailored for single-objective optimization, only achieves low regret for the first objective, while incurring linear regret on the second and third. Although PF-LEX is designed for multiobjective settings, it suffers from a slower convergence rate, as reflected in its eO(T 2/3) regret bound. BAI Results. For BAI algorithms (EGE, UCBα, LexElim- Out, and LexElim-In), we set the confidence level δ = 0.01 and evaluate their performance under varying numbers of arms K ∈{10, 20, 30}. The results are shown in Figure 3, where Panels (a) – (c) correspond to increasing K. All algorithms require more samples as K increases, reflecting the greater difficulty of distinguishing between arms when reward gaps shrink. LexElim-In consistently outperforms the baselines, and its advantage becomes more significant with larger K. This is because LexElim-In exploits information from lower-priority objectives, which have larger reward gaps and provide stronger signals for elimination. In our setting, the reward gaps for the second and third objectives are twice as large as that of the first, allowing LexElim-In to identify the optimal arm more efficiently.

## Conclusion

and Future work

This paper develops the first unified framework for simultaneously addressing both RM and BAI tasks in lexicographic multi-objective bandits. We propose two principled algorithms, LexElim-Out and LexElim-In, which adhere to the lexicographic preference structure while optimizing multiple objectives. LexElim-Out adopts a conservative elimination strategy that sequentially filters arms based on priority, ensuring no compromise on higher-priority objectives. LexElim-In exploits the joint reward signals across all objectives to perform more efficient arm elimination. We provide a comprehensive theoretical analysis for both algorithms: LexElim-Out matches the known instancedependent lower bounds for the primary objective, while LexElim-In achieves better instance-dependent bounds than classical single-objective methods.

An interesting direction for future work is to establish tighter lower bounds for lexicographic RM and BAI that explicitly capture the interactions among objectives. Additionally, eliminating the need for prior knowledge of the parameter λ would further enhance the applicability of LexElim-In.

27420

<!-- Page 8 -->

## Acknowledgments

The work described in this paper was supported by the Research Grants Council of the Hong Kong Special Administrative Region, China [GRF Project No. CityU 11215622].

## References

Abbasi-yadkori, Y.; P´al, D.; and Szepesv´ari, C. 2011. Improved Algorithms for Linear Stochastic Bandits. In Advances in Neural Information Processing Systems 24, 2312– 2320. Alkaabneh, F.; and Diabat, A. 2023. A multi-objective home healthcare delivery model and its solution using a branchand-price algorithm and a two-stage meta-heuristic algorithm. Transportation Research Part C: Emerging Technologies, 147: 103838. Alon, N.; Cesa-Bianchi, N.; Dekel, O.; and Koren, T. 2015. Online Learning with Feedback Graphs: Beyond Bandits. In Proceedings of the 28th Conference on Learning Theory, 23–35. Audibert, J.-Y.; and Bubeck, S. 2009. Minimax policies for adversarial and stochastic bandits. In Proceedings of the 22th annual conference on learning theory, 217–226. Audibert, J.-Y.; and Bubeck, S. 2010. Best Arm Identification in Multi-Armed Bandits. In Proceedings of the 23rd Annual Conference on Learning Theory, 41–53. Auer, P. 2002. Using Confidence Bounds for Exploitation- Exploration Trade-offs. Journal of Machine Learning Research, 3(11): 397–422. Auer, P.; Cesa-Bianchi, N.; and Fischer, P. 2002. Finitetime Analysis of the Multiarmed Bandit Problem. Machine Learning, 47(2–3): 235–256. Auer, P.; Chiang, C.-K.; Ortner, R.; and Drugan, M. 2016. Pareto Front Identification from Stochastic Bandit Feedback. In Proceedings of the 19th International Conference on Artificial Intelligence and Statistics, 939–947. Awerbuch, B.; and Kleinberg, R. 2008. Online linear optimization and adaptive routing. Journal of Computer and System Sciences, 74(1): 97–114. Bubeck, S.; and Cesa-Bianchi, N. 2012. Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems. Foundations and Trends in Machine Learning, 5(1): 1–122. Bubeck, S.; Munos, R.; and Stoltz, G. 2009. Pure exploration in multi-armed bandits problems. In Proceedings of the 20th International Conference on Algorithmic Learning Theory, 23–37. Carpentier, A.; and Locatelli, A. 2016. Tight (Lower) Bounds for the Fixed Budget Best Arm Identification Bandit Problem. In Proceedings of the 29th Annual Conference on Learning Theory, 590–604. Chen, W.; Hu, W.; Li, F.; Li, J.; Liu, Y.; and Lu, P. 2016. Combinatorial Multi-Armed Bandit with General Reward Functions. In Advances in Neural Information Processing Systems 29, 1659–1667. Cheng, J.; Xue, B.; Lu, C.; Cui, Z.; and Zhang, Q. 2025. Multi-Objective Neural Bandits with Random Scalarization.

In Proceedings of the 34th International Joint Conference on Artificial Intelligence, 4914–4922. Cheng, J.; Xue, B.; Yi, J.; and Zhang, Q. 2024. Hierarchize Pareto Dominance in Multi-Objective Stochastic Linear Bandits. In Proceedings of the 38th AAAI Conference on Artificial Intelligence, 11489–11497. Crepon, E.; Garivier, A.; and M Koolen, W. 2024. Sequential learning of the Pareto front for multi-objective bandits. In Proceedings of The 27th International Conference on Artificial Intelligence and Statistics, 3583–3591. Dani, V.; Hayes, T. P.; and Kakade, S. M. 2008. Stochastic Linear Optimization under Bandit Feedback. In Proceedings of the 21st Annual Conference on Learning, 355–366. Degenne, R.; Nedelec, T.; Calauzenes, C.; and Perchet, V. 2019. Bridging the gap between regret minimization and best arm identification, with application to A/B tests. In Proceedings of the 32nd International Conference on Artificial Intelligence and Statistics, 1988–1996. Degenne, R.; and Perchet, V. 2016. Anytime optimal algorithms in stochastic multi-armed bandits. In Proceedings of The 33rd International Conference on Machine Learning, 1587–1595. Drugan, M. M.; and Nowe, A. 2013. Designing multiobjective multi-armed bandits algorithms: A study. In The 2013 International Joint Conference on Neural Networks, 1–8. Even-Dar, E.; Mannor, S.; and Mansour, Y. 2006. Action Elimination and Stopping Conditions for the Multi-Armed Bandit and Reinforcement Learning Problems. Journal of Machine Learning Research, 7(39): 1079–1105. Garivier, A.; and Kaufmann, E. 2016. Optimal Best Arm Identification with Fixed Confidence. In Proceedings of the 29th Annual Conference on Learning Theory, 998–1027. H¨uy¨uk, A.; and Tekin, C. 2021. Multi-objective multi-armed bandit with lexicographically ordered and satisficing objectives. Machine Learning, 110(6): 1233–1266. Jamieson, K.; Malloy, M.; Nowak, R.; and Bubeck, S. 2014. lil’ UCB: An Optimal Exploration Algorithm for Multi- Armed Bandits. In Proceedings of The 27th Conference on Learning Theory, 423–439. Jin, T.; Yang, Y.; Tang, J.; Xiao, X.; and Xu, P. 2024. Optimal Batched Best Arm Identification. In Advances in Neural Information Processing Systems 37, 134947–134980. Karnin, Z.; Koren, T.; and Somekh, O. 2013. Almost Optimal Exploration in Multi-Armed Bandits. In Proceedings of the 30th International Conference on Machine Learning, 1238–1246. Kaufmann, E.; Capp´e, O.; and Garivier, A. 2016. On the Complexity of Best-Arm Identification in Multi-Armed Bandit Models. Journal of Machine Learning Research, 17(1): 1–42. Kone, C.; Kaufmann, E.; and Richert, L. 2024. Bandit Pareto Set Identification: the Fixed Budget Setting. In Proceedings of The 27th International Conference on Artificial Intelligence and Statistics, 2548–2556.

27421

<!-- Page 9 -->

Kurokawa, D.; Procaccia, A. D.; and Shah, N. 2018. Leximin Allocations in the Real World. ACM Transactions on Economics and Computation, 6(3–4): 1–24. Lai, T. L.; and Robbins, H. 1985. Asymptotically efficient adaptive allocation rules. Advances in Applied Mathematics, 6(1): 4–22. Lattimore, T. 2018. Refining the Confidence Level for Optimistic Bandit Strategies. Journal of Machine Learning Research, 19(20): 1–32. Li, Y.; Chen, H.; Xu, S.; Ge, Y.; Tan, J.; Liu, S.; and Zhang, Y. 2023. Fairness in Recommendation: Foundations, Methods, and Applications. ACM Transactions on Intelligent Systems and Technology, 14(5): 1–48. Lu, S.; Wang, G.; Hu, Y.; and Zhang, L. 2019. Multi- Objective Generalized Linear Bandits. In Proceedings of the 28th International Joint Conference on Artificial Intelligence, 3080–3086. Lykouris, T.; Mirrokni, V.; and Paes Leme, R. 2018. Stochastic Bandits Robust to Adversarial Corruptions. In Proceedings of the 50th Annual ACM SIGACT Symposium on Theory of Computing, 114–122. Q. Yahyaa, S.; M. Drugan, M.; and Manderick, B. 2015. Thompson Sampling in the Adaptive Linear Scalarized Multi Objective Multi Armed Bandit. In International Conference on Agents and Artificial Intelligence, 55–65. Robbins, H. 1952. Some aspects of the sequential design of experiments. Bulletin of the American Mathematical Society, 58(5): 527–535. Schwartz, E.; Bradlow, E.; and Fader, P. 2017. Customer Acquisition via Display Advertising Using Multi-Armed Bandit Experiments. Marketing Science, 36(2): 500–522. Shu, T.; Shang, K.; Gong, C.; Nan, Y.; and Ishibuchi, H. 2024. Learning pareto set for multi-objective continuous robot control. In Proceedings of the 33rd International Joint Conference on Artificial Intelligence, 4920 – 4928. Tekin, C. 2019. The biobjective multiarmed bandit: learning approximate lexicographic optimal allocations. Turkish Journal of Electrical Engineering and Computer Sciences, 27(2): 1065–1080. Tekin, C.; and Turgay, E. 2018. Multi-objective Contextual Multi-armed Bandit With a Dominant Objective. IEEE Transactions on Signal Processing, 66(14): 3799–3813. Villar, S. S.; Bowden, J.; and Wason, J. 2015. Multi-armed Bandit Models for the Optimal Design of Clinical Trials: Benefits and Challenges. Statistical Science, 30(2): 199 – 215. Wanigasekara, N.; Liang, Y.; Goh, S. T.; Liu, Y.; Williams, J. J.; and Rosenblum, D. S. 2019. Learning Multi-Objective Rewards and User Utility Function in Contextual Bandits for Personalized Ranking. In Proceedings of the 28th International Joint Conference on Artificial Intelligence, 3835– 3841. Xie, Y.; Shi, C.; Zhou, H.; Yang, Y.; Zhang, W.; Yu, Y.; and Li, L. 2021. MARS: Markov Molecular Sampling for Multiobjective Drug Discovery. In International Conference on Learning Representations.

Xu, M.; and Klabjan, D. 2023. Pareto Regret Analyses in Multi-objective Multi-armed Bandit. In Proceedings of the 40th International Conference on International Conference on Machine Learning, 38499–38517. Xue, B.; Bu, D.; Cheng, J.; Wan, Y.; and Zhang, Q. 2025a. Multi-objective Linear Reinforcement Learning with Lexicographic Rewards. In Proceedings of the 42nd International Conference on Machine Learning. Xue, B.; Cheng, J.; Liu, F.; Wang, Y.; and Zhang, Q. 2024. Multiobjective Lipschitz Bandits under Lexicographic Ordering. Proceedings of the 36th AAAI Conference on Artificial Intelligence, 16238 – 16246. Xue, B.; Lin, X.; Wan, Y.; and Zhang, Q. 2025b. Problemdependent Regret for Lexicographic Multi-Armed Bandits with Adversarial Corruptions. In Proceedings of the 34th International Joint Conference on Artificial Intelligence, 6776–6784. Xue, B.; Lin, X.; Zhang, X.; and Zhang, Q. 2025c. Multiple Trade-offs: An Improved Approach for Lexicographic Linear Bandits. In Proceedings of the 39th AAAI Conference on Artificial Intelligence, 21850–21858. Xue, B.; Wang, G.; Wang, Y.; and Zhang, L. 2020. Nearly Optimal Regret for Stochastic Linear Bandits with Heavy- Tailed Payoffs. In Proceedings of the 29th International Joint Conference on Artificial Intelligence, 2936–2942. Xue, B.; Wang, Y.; Wan, Y.; Yi, J.; and Zhang, L. 2023. Efficient Algorithms for Generalized Linear Bandits with Heavy-tailed Rewards. In Advances in Neural Information Processing Systems 36, 70880–70891. Yang, J.; Tan, V. Y. F.; and Jin, T. 2024. Best Arm Identification with Minimal Regret. arXiv:2409.18909. Zhang, Q.; and Ying, L. 2023. Fast and Regret Optimal Best Arm Identification: Fundamental Limits and Low- Complexity Algorithms. In Advances in Neural Information Processing Systems 36, 16729–16769. Zhang, S.; Jia, F.; Wang, C.; and Wu, Q. 2023. Targeted Hyperparameter Optimization with Lexicographic Preferences Over Multiple Objectives. In The 11th International Conference on Learning Representations. Zhong, Z.; Cheung, W. C.; and Tan, V. 2023. Achieving the Pareto Frontier of Regret Minimization and Best Arm Identification in Multi-Armed Bandits. Transactions on Machine Learning Research.

27422
