---
title: "Constrained Online Convex Optimization with Memory and Predictions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39031
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39031/42993
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Constrained Online Convex Optimization with Memory and Predictions

<!-- Page 1 -->

Constrained Online Convex Optimization with Memory and Predictions

Mohammed Abdullah1,2, George Iosifidis3, Salah Eddine Elayoubi1, Tijani Chahed2

1Universit´e Paris-Saclay, CentraleSup´elec, CNRS, L2S, Gif-sur-Yvette, France 2Institut Polytechnique de Paris, T´el´ecom SudParis, Palaiseau, France 3Delft University of Technology, The Netherlands {mohammed.abdullah, salaheddine.elayoubi}@centralesupelec.fr,

G.Iosifidis@tudelft.nl, tijani.chahed@telecom-sudparis.eu

## Abstract

We study Constrained Online Convex Optimization with Memory (COCO-M), where both the loss and the constraints depend on a finite window of past decisions made by the learner. This setting extends the previously studied unconstrained online optimization with memory framework and captures practical problems such as the control of constrained dynamical systems and scheduling with reconfiguration budgets. For this problem, we propose the first algorithms that achieve sublinear regret and sublinear cumulative constraint violation under time-varying constraints, both with and without predictions of future loss and constraint functions. Without predictions, we introduce an adaptive penalty approach that guarantees sublinear regret and constraint violation. When short-horizon and potentially unreliable predictions are available, we reinterpret the problem as online learning with delayed feedback and design an optimistic algorithm whose performance improves as prediction accuracy improves, while remaining robust when predictions are inaccurate. Our results bridge the gap between classical constrained online convex optimization and memory-dependent settings, and provide a versatile learning toolbox with diverse applications.

## Introduction

Online Convex Optimization (OCO) is the workhorse model for sequential decisions under adversarial uncertainty. In its basic version, a learner picks an decision xt from a convex set X at the start of each round t; an adversary then reveals a convex loss function ft: X 7→R and the learner suffers ft(xt). The learning is assessed by the metric of regret RT, i.e., the distance of the accumulated loss from that of the best-in-hindsight decision x⋆= arg minx∈X

PT t=1 ft(x), and the goal is to ensure sublinear regret. Since its conception (Zinkevich 2003), OCO has been extended to an impressive range of problems (Orabona 2025).

One of these extensions is OCO with memory (OCO-M), where the loss at each round t depends on the previous m decisions of the learner xt−m,..., xt. Data caching with fetching costs, communication systems with reconfiguration delays, user-engagement in recommender systems, investment portfolio selection, and model training in continual learning,

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

are only some of the problems that can be tackled with OCO- M (Anava, Hazan, and Mannor 2015). Further, the recent online non-stochastic control (NSC) framework owes its success to OCO-M, as such stateful systems can be controlled with memory-based functions (Hazan and Singh 2025).

Beyond minimizing losses, real-world systems must often satisfy average constraints of time-varying functions, gt(xt) ≤0. This constrained OCO (COCO) extension is attracting growing interest and has several flavors. In some cases the goal is to ensure sublinear long-term violation (LTV), P t gt(xt), and in others to bound the cumulative constraint violation (CCV), P t max{gt(xt), 0}; also, the functions may be known when xt is decided or not, and they might be static gt = g, stochastically-perturbed or selected by an adversary. Importantly, similarly to losses, the constraints may exhibit memory and depend jointly on the m recent decisions. Examples include energy budget constraints over m-slot windows in smart grid, thermal envelopes that integrate recent power inputs in processors, QoE user metrics capturing service volatility, and battery-health limits tied to cumulative depth-of-discharge, to mention only few. Apart from such operational or resource constraints, LTV and CCV are also relevant for multi-criteria optimization.

It is clear from the above that COCO-M is an important and practical extension of OCO which, nevertheless, remains largely unexplored. This work contributes in addressing this gap by studying several instances of this problem.

Contributions. We study the most compounded version of COCO-M where the constraints are unknown and adversarially varying, and we are interested in CCV, which we denote VT. We consider two problems, one with memory effects on losses and constraints (COCO-M2), and another with memory-less constraints (COCO-M). Following a penaltybased relaxation analysis (Zangwill 1967) we design an algorithm that achieves regret RT = O m3/2√T log T

, and CCV VT = O max{T 3/4, m3/2√T log T}

for COCO-M2, improving upon the RT, VT = O(T 2/3 log2T) bounds of (Liu, Yang, and Ying 2023) for T ∈[3, 1049], the only prior work related to COCO-M2. For COCO-M, we achieve VT = O(T 3/4) which improves to VT = O(m3/2√

T log T) for short memory.

We take the next step and study, for the first time, the problem through the lens of optimistic learning (OL),

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19524

<!-- Page 2 -->

(Rakhlin and Sridharan 2013b). That is, we assume the availability of untrusted predictions about the gradients of forthcoming losses and constraints, and design an algorithm that, under a more restrictive benchmark than in the no-prediction setting, ensures

RT =O p

ET (f)

, VT =O p

ET (g+)+m log T

, where ET (f) and ET (g+) denote the total prediction errors for the loss and constraint functions over the T rounds. These bounds diminish with the predictions’ accuracy, becoming RT = O(log T), VT = O(m log T) for perfect predictions, and RT = O(m2√

T), VT = O(m2√

T log(T)) when the prediction fail maximally. These rates subsume the optimistic COCO bounds without memory (Lekeufack and Jordan 2024); and the optimistic unconstrained OCO- M bounds (Mhaisen and Iosifidis 2024).

To streamline the presentation of the material, we defer all proofs to the Appendix where, the interested reader, can also find extensive discussion of related work, analysis of special problem cases and numerical experiments.

## Related work

COCO Bounds. The COCO literature falls in two strands. First, works that assume constraints are static or known. The earliest work here (Mahdavi, Jin, and Yang 2012), considers fixed affine constraints; (Chaudhary and Kalathil 2022) study fixed but unknown constraints observed via stochastic feedback; and (Qiu, Wei, and Kolar 2023), (Yu and Neely 2020) address static unknown constraints to get LTV O(1). This regime is less relevant to our setting but provides useful insights. The second strand considers constraints that are both time-varying and unknown. Here, (Guo et al. 2022) match the O

√

T regret and obtain O(T 3/4) CCV. Other papers, e.g., (Wang, Wan, and Zhang 2025) focused on projection free algorithms for this problem. (Sinha and Vaze 2024) achieve O √

T regret with O

√

T log T

CCV. For a dynamic benchmark, (Wang, Yan, and Liu 2025) provide a bound of O

T (1+Vx)/2 and O

T Vg violation, where Vx and Vg ∈[0, 1] quantify the functions variability. However, there are no OCO-M papers with either CCV or LTV.

COCO-M and Non-stochastic Control. Since their introduction by (Agarwal, Hazan, and Singh 2019), NSC methods have used disturbance–action (DAC) policies: the control at round t is a weighted sum of the last m disturbances, and these weights are learned through OCO-M. In that sense NSC is relevant to our study. However, most NSC papers impose deterministic constraints on the state and input (Jiang, Hutchinson, and Alizadeh 2025; Li, Das, and Li 2021; Nonhoff and M¨uller 2021; Yan, Zhao, and Zhou 2023) or assume the constraint at t+1 is revealed one round before (Zhou and Tzoumas 2023); in both cases the goal is per–round feasibility rather than an average–sense guarantee. The sole exception is (Liu, Yang, and Ying 2023), who analyze a fully adversarial setting and obtain regret and CCV bounds of O

T 2/3 log2 T when the memory length is fixed to m = log T. Our work tightens these bounds to

O m3/2√T log T regret and O m3/2√T log T ∨T 3/4

CCV. Besides, our bounds hold for any memory length m.

Optimism. Look-ahead gradients can compress regret in proportion to their prediction error. In OCO, this is well studied (Rakhlin and Sridharan 2013a; Mohri and Yang 2016; Joulani, Gyorgy, and Szepesvari 2020; Flaspohler et al. 2021). Extending optimism to OCO-M is harder because one must predict farther than the next round; (Mhaisen and Iosifidis 2024) is the only work that tackles this challenge for linear losses in NSC under imperfect predictions. In online control, perfect look-ahead predictions can yield exponential improvements in dynamic regret. For example, Yu et al. (Yu et al. 2020) analyze quadratic, time-invariant losses with adversarial disturbances under model-predictive control, and Li et al. (Li, Chen, and Li 2019) study timevarying convex losses without disturbances. In both cases, the dynamic-regret bound decreases exponentially with the length of the prediction window. Predictions may also be viewed through the lens of “context” (Li et al. 2022) in stochastic MDPs with presume finite states and action sets. Lastly, prior works (Yu et al. 2022; Zhang, Li, and Li 2021) assume full-horizon predictions, blocking the learner from using updates; we instead let it incorporate the latest forecasts each round.

Finally, OL in COCO remains surprisingly sparse. (Anderson, Iosifidis, and Leith 2023) proposed a primal-dual algorithm to achieve RT = O(1) and LTV O

√

T under perfect predictions; (Zhang, Guo, and Liu 2025) achieves RT = O(√VT), where VT captures the aggregate variation of successive gradients, and grantees LTV = O(1) under the Slater condition, while (Lekeufack and Jordan 2024) used instead a penalty method, attaining RT =O p ¯ET (f)

and CCV O log T( p ¯ET (g+) + 1)

, where ¯ET (f) and ¯ET (g+) denote the prediction errors. None of these works consider memory in the objective or constraints.

Summary. OCO-M with adversarial time-varying cumulative constraints has only been studied in NSC by (Liu, Yang, and Ying 2023), which we strictly outperform for T ∈[1, 1049]. The optimistic version of the problem is introduced by this work, and we obtain bounds which for m = 0 match the OL COCO results (Lekeufack and Jordan 2024). A summary of the most relevant COCO results is provided in the appendix (Table??).

## 3 Preliminaries

Notation. The diameter of a non-empty, closed and convex decision set X ⊂Rd, is defined as ∥X∥.= supx,y∈X ∥x−y∥, where ∥· ∥is the ℓ2 norm. We write T:= {m,..., T} and at each round t ∈T the learner selects an decision xt ∈X. The memory length is denoted with m, and we use:

xt t−m

.= (xt−m,..., xt) ∈X m+1, xa:b.= b X i=a xi.

For a function ft(xt−m,..., xt) we define its memory-less version ˆft(xt).=ft(xt,..., xt) with ˆft:X 7→R, and its prediction is denoted by ˜ft. We use f + t (x).= max ft(x), 0

,

19525

<!-- Page 3 -->

and abuse notation to denote ∇ft(xt) the gradient of ft at xt or its subgradient if it is non-differentiable.

Background. In OCO the learner selects an decision xt ∈ X before the convex loss ft: X 7→R is revealed. The performance of the learner is measured with the regret:

OCO: RT =

T X t=1 ft(xt) −min x∈X

T X t=1 ft(x), (1)

and the learner wishes to achieve limT →∞RT /T = 0, for any possible sequence of loss functions {ft}t.

In a more recent extension of this framework, the learner’s decisions need additionally to satisfy a time-average (budget) of constraints gt: X 7→R ∀t. In this Constrained OCO (COCO) formulation, the regret is defined as:

Rc

T =

T X t=1 ft(xt) −min x∈XT

T X t=1 ft(x), (2)

where the set of eligible decisions is modified to:

XT = n x ∈X gt(x) ≤0, ∀t ∈T o

. (3)

Observe that we restrict the benchmark to satisfy the constraints at every round and not on average; a necessary compromise to avoid the impossibility result of COCO, cf. (Mannor, Tsitsiklis et al. 2009). The learner here aims to achieve sublinear regret and constraint violation:

COCO: Rc

T = o(T), Vc

T ≜

T X t=1 g+ t (xt) = o(T). (4)

In this work we are interested in functions with m-length memory where the loss ft: X m+1 7→R at each round t, depends on the previous m>0 decisions of the learner. Following (Anava, Hazan, and Mannor 2015), the regret for this OCO-M problem is defined as:

OCO-M: Rm

T =

T X t=m ft(xt t−m)−min x∈X

T X t=m ft(x,..., x), (5)

where the benchmark is defined using the respective memory-less functions ˆft(x).= ft(x,..., x) that are assumed convex. In this work, we make a further step and introduce the COCO-M2 framework, where the constraints also exhibit memory effects, gt: X m+1 7→R. We thus define:

Rmc

T =

T X t=m ft(xt t−m) −min x∈X m

T

T X t=m ft(x,..., x), (6)

where the set of eligible decisions is:

X m

T = n x ∈X gt(x,..., x) ≤0, ∀t ∈T o

(7)

and, as in the typical COCO, the learner aims to achieve:

COCO-M2: Rmc

T, Vmc

T

.=

T X t=1 g+ t (xt t−m) = o(T). (8)

Decide Observe Calculate Prediction

Oracle

Next Round xt ft, gt ft(xt t−m) gt(xt t−m) 1 2 4 xt−m, xt−m+1,..., xt−1 Memory

Effect

**Figure 1.** decision stages of COCO-M (with predictions).

Finally, the COCO setting where only the loss functions have memory while the constraints, gt: X 7→R, are memoryless, is of independent interest. In this case, the definition of regret Rmc

T remains the same, but the benchmark is x⋆∈XT, and the constraint violation changes to:

COCO-M: Rmc

T, Vc

T

.=

T X t=1 g+ t (xt) = o(T). (9)

We denote this problem as COCO-M to distinguish it from the above problem with double memory (M2).

Regarding the solution of COCO problems, the main techniques use a simple idea: apply an OCO algorithm on some type of (time-varying) Lagrange function, Lt(·), that scalarizes the objective and constraints. These techniques can be classified in two broad categories. Those that introduce explicit dual variables µ and perform primal-dual iterations on Lt(x, µ), i.e., employ coordinated learning in the primal and dual space, e.g., see (Yuan and Lamperski 2018; Valls et al. 2020). And the second category that draws from penalty methods (Zangwill 1967) and creates again a Lagrange-type function, Lt(x), where the constraint violation is penalized with some parameter (Liakopoulos et al. 2019; Leith and Iosifidis 2023; Lekeufack and Jordan 2024; Sinha and Vaze 2024). We follow this latter approach.

Learning Model & Assumptions. We consider the most general COCO model where both the loss and the constraint functions may change over time, and in each round they are revealed after the learner commits its decision. Regarding the adversary model, we follow (Anava, Hazan, and Mannor 2015; Merhav et al. 2002; Gyorgy and Neu 2014) and consider an oblivious adversary which implies that these functions are determined in advance (i.e., at t = 0) but, of course, are not revealed. Finally, we consider full-information feedback for all the arguments of the memory functions; see Fig. 1. We also use the following standard OCO assumptions. Assumption 1. X is closed and convex, with ∥X∥< ∞. Assumption 2. For every t, functions ft(·) and gt(·) are convex and F-, G-bounded, respectively. Assumption 3 (Lipschitz continuous). For every time t ∈ T, let ft, gt: X m+1 7→R and ˜ft, ˜gt: X m+1 7→R.

All functions are Lipschitz continuous, i.e., there exist finite constants Lt,f, Lt,g ≥0 such that, ∀x, y ∈X m+1, ft(x) −ft(y)

,

˜ft(x) −˜ft(y)

≤Lf ∥x −y∥, gt(x) −gt(y)

,

˜gt(x) −˜gt(y)

≤Lg ∥x −y∥.

Finally, the following remark is without loss of generality.

19526

<!-- Page 4 -->

Remark 1. If we have n constraints gt,k with k = 1,..., n, we can follow the standard approach and define gt:= maxk gt,k. Hence, to streamline the presentation, we consider constraints that map to R, not to Rn.

## Algorithm

Design & Analysis Our method is closer to penalty COCO techniques, while the memory effect is handled as in (Anava, Hazan, and Mannor 2015), i.e., we perform the analysis using the memory-less functions and lift the results to the original problem. Namely, we use the memory-less versions of ft, gt: X m+1 7→R, which are defined on X as:

ˆft(x):= ft(x,..., x), ˆgt(x):= gt(x,..., x), and following (Lekeufack and Jordan 2024; Sinha and Vaze 2024), we define the (memory-less) surrogate function: ˆLt(x) = ˆft(x) + Φ′ ˆVt

ˆg+ t (x), (10) where Φ:R+ 7→R is a non-negative, convex monotonically increasing penalty function with Φ(0)=0, and Φ′ its derivative. Observe that Φ is applied to the cumulative memoryless constraint violation which is denoted ˆVt and defined:

ˆVt =

ˆV mc t, in COCO-M2, V c t, in COCO-M. This quantity evolves with time as:

ˆVt =

(

ˆVt−1 + ˆg+ t (xt), in COCO-M2, ˆVt−1 + g+ t (xt), in COCO-M.

The intuition of ˆLt is that we penalize the violation of constraints at round t, with a penalty commensurate to the accumulated constraint violation. Different from (Lekeufack and Jordan 2024), (Sinha and Vaze 2024), we use:

Φ(V) = λV 2, with parameter λ > 0 determined below. This penalty leads to tighter bounds compared to the exponential function in those prior works; we revisit this discussion later.

Now, focusing on the surrogate function, we observe that it operates on decisions drawn from the convex set X, and under Assumptions 1-3 it is convex with bounded gradients for fixed T. Namely, by the triangle inequality, we get:

sup t,x

∇ˆLt(x)

≤Lf +Φ′(VT)Lg = Lf +2λVT Lg. (11)

Therefore, performing Online Gradient Descent (OGD), i.e., xt+1 = PX xt −ηt∇ˆLt(xt)

, (12)

where PX is the ℓ2 projection on X, ensures sublinear regret for these surrogate functions, which we denote RT (ˆL). Lemma 1. Under Assumptions 1-3, performing OGD on (10) with step ηt =

√

2∥X∥

2√Pt τ=1 ∥∇ˆ Lt(xt)∥2, we obtain:

RT (ˆL) ≜

T X t=1

ˆLt(xt) −min x∈X b

T

T X t=1

ˆLt(x)

≤

√

2∥X∥ v u u t

T X t=1

∥∇ˆLt(xt)∥2

## Algorithm

1: Learning for COCO-M and COCO-M2

Require: initial history xm−1

0 ∈Xm; dual seed ˆVm−1

0 ←0 1: for t = m to T −1 do 2: Play xt and observe ft(·), gt(·) 3: Calculate ft(xt t−m) and gt(xt). // for COCO-M 4: Calculate ft(xt t−m), gt(xt t−m). // for COCO-M2

5: Vt ←Vt−1 + g+ t (xt) // dual update for COCO-M 6: ˆVt ←ˆVt−1 + g+ t (xt,..., xt) // for COCO-M2

7: Compute surrogate gradient ∇ˆLt(xt) via (10) 8: xt+1 ←solution of (12) // devise next decision 9: end for where the benchmark set depends on the problem: X b

T = X m

T for COCO-M2 and X b

T = XT for COCO-M.

In the sequel, we explain how this result sets the basis for tackling the COCO-M and COCO-M2 problems.

Problem COCO-M2: Double Memory Effect We start with the more compounded problem COCO-M2 in (8), having memory in losses and constraints. Without loss of generality, we assume these effects are of the same length m. The solution is summarized in Algorithm 1. In brief, in each round t, the learner commits its decision xt ∈X, observes the current loss and constraint functions and calculates the loss and constraint violation. Then, it updates the constraint violation, calculates the t-round gradient ∇ˆLt(xt) and uses OGD to devise the next decision.

To characterize the performance of this algorithm, we take two steps. First, we utilize the following regret decomposition result, which links the regret of the memoryless Lagrangian RT (ˆL) to the regret of the memory-less loss (denoted ˆRc

T) and the constraint violation ˆVmc

T over the memory-less functions.

Lemma 2 (Regret decomposition (Sinha and Vaze 2024)). For any OCO algorithm, if Φ is a convex increasing function, we have for any t ≥m and x⋆∈X m

T ˆRc

T + Φ(ˆVT) −Φ(ˆVm) ≤RT (ˆL). (13)

And, secondly, we transfer these results to the original problem with memory, by observing that we can write:

Rc

T =

T X t=m ft(xt t−m) −ft(xt,..., xt)

| {z } memory deviation

+ ˆRc

T (14)

Vmc

T =

T X t=m g+ t (xt t−m) −g+ t (xt,..., xt) + ˆVmc

T. (15)

We bound this memory deviation by exploiting the functions Lipschitz continuity together with the one-step OGD bound. The following theorem summarizes the achieved bounds.

Theorem 1 (Regret and CCV for COCO-M2). Assume (i) Assumptions 1, 2, 3 hold; (ii) the constraint is gt(xt t−m), and

(iii) we use the step ηt =

√

2∥X∥

2√Pt τ=1 ∥∇ˆ Lt(xt)∥2 and the penalty

19527

<!-- Page 5 -->

Φ(V)=λV 2 with λ= 1 √

T. Then, ∀T ≥m it is:

Rmc

T = O m

3 2 p T log(T)

(16)

Vmc

T = O max{T 3/4, m

3 2 p T log(T)

. (17)

Discussion. In Theorem 1 we see the effect of m: longer memory amplifies both the regret and CCV, thus the performance degrades as the window grows. The only directly comparable study is (Liu, Yang, and Ying 2023), which assumes m=log T and achieves strictly inferior bounds (Table??) for any T ∈[3, 1049]. When memory vanishes (m = 0), our bounds collapse to O(

√

T) for the regret and O(T 3/4) for the CCV; which are looser than the bounds of (Sinha and Vaze 2024). This gap arises because we employ a quadratic penalty that yields sharper results for the memory problem, whereas (Sinha and Vaze 2024) use an exponential penalty in the memory–free setting. We will show later that, for COCO-M and sufficiently short memory, this gap vanishes as we also use there a different penalty function.

Problem COCO-M We continue with the case where memory affects only the losses, while the constraints are time-varying memory-less functions. The goal is to ensure sublinear regret Rmc

T and constraint violation Vc

T, see (9). The algorithm is identical to the one above, with only changes in the calculation of the constraint violation and the dual update. In particular, following the same steps, we first invoke the regret–decomposition lemma and translate the bound back to the original problem using solely (14), because, here, the term ˆVT appearing in the lemma coincides with the cumulative violation Vc

T. We thus get the next result. Theorem 2 (Regret and CCV with memory-free constraint). Given that (i) Assumptions 1, 2, and 3 hold, (ii) the constraint is memory-less (gt = (xt)), and (iii) we use the adaptive step ηt =

√

2∥X∥

2√Pt τ=1 ∥∇ˆ Lt(xt)∥2 and the penalty

Φ(V) = λV 2 with λ = 1 √

T. Then, for any T ≥m we have:

Rmc

T = O m

3 2 p T log(T)

, Vc

T = O

T 3/4

. (18)

## Discussion

Relatively to COCO-M2 (Theorem 1), two points stand out: (i) The CCV no longer depends on the window m; it remains O(T 3/4) regardless of the loss functions’ memory. (ii) The regret retains the m3/2√T log T factor. Compared to the regret bound O m3/2√

T of (Anava, Hazan, and Mannor 2015), this carries an extra √log T factor; this is the price of enforcing time–varying constraints.

Furthermore, it is important to stress that when the memory length satisfies m ≤

T 1/6/ log T

1/3, thus m3/2√T log T ≤T 3/4, we can replace the quadratic penalty with an exponential one with a tuned λ, to achieve tighter guarantees for CCV: Rmc

T = O

√

T + m3/2√T log T and Vc

T = O

√T log T + m3/2√

T log T

. While Vc

T depends now on m, this bound is smaller than O(T 3/4). In several practical applications indeed m is a constant and much smaller than any expression of the growing T. Hence, for all these problems we can enable these improved rates. Finally, we note that for m=0 the bounds reduce to those in (Sinha and Vaze 2024). We provide the details for these cases in the Appendix.

Benefiting from Predictions We next study COCO-M2 when predictions about forthcoming loss and constraint functions are available see Figure 1 for the decision stages. We study problem COCO-M in the Appendix. This form of learning, known as Optimistic Learning (OL), achieves bounds that shrink with the initially-unknown predictions’ accuracy. Predictions are widely studied in OCO (Rakhlin and Sridharan 2013a), less so in COCO (Lekeufack and Jordan 2024), and only recently in OCO-M (Mhaisen and Iosifidis 2024) – still, without constraints. In classical OCO, it suffices to predict the next gradient; alas in the presence of memory the forecasting should involve the gradients of the next m slots.

This compounded problem requires modifying the approach in Sec. 4. First, we use the memory-based surrogate:

Lt x t t−m

= ft x t t−m

+ Φ′

Vt−m−1 g+ t x t t−m

, (19)

with Φ(V) = exp(λV) −1 that has delayed argument Vt−m−1. We study the COCO-M2 problem, where:

Vt = Vt−1 + g+ t x t t−m

, i.e., VT = Vmc

T.

Secondly, instead of performing OL on (19), we turn the problem on its head and interpret the losses and constraints as having delayed gradients instead of depending on past decisions: at round t the learner selects xt but is only able to observe the gradient of this decision at the end of t+m, i.e., after all functions influenced by xt are revealed. This change of vantage point allow us to replace the memory effect with a delay effect, which then is handled through a particular version of OL. Before we proceed, we need the following. Assumption 4 (Separability). Every memory-based function can be decomposed into components, each depending on a decision from a different round:

ft xt t−m

= m X i=0 f i t(xt−i), gt xt t−m

= m X i=0 gi t(xt−i).

where f i t, gi t are defined on X, and i marks that their argument was decided in round t −i. Assumption 5 (Linearity). Every function f i t(·) and gi t(·) is linear, for all t ∈T, i ∈[0, m].

Now, the key idea for pivoting to delayed learning is introducing a forward loss function to capture the influence of each xt on the system operation, i.e., Zt(xt).= m X i=0

Li t+i(xt)≜ m X i=0 f i t+i(xt)+Φ′(Vt−m−1+i) gi,+ t+i(xt).

Despite the similarities with Lt x t t−m

, Zt depends only on round t decision (is memory-less) and includes function components from the next m rounds (has delayed gradient),

19528

<!-- Page 6 -->

< l a t e x i t s h a

1

_ b a s e

4

=

" e

C

9 t

1 h n

K i

U w h

C

H

I

M a

F p q

P l

Q

X

7

7

E

=

"

>

A

A

A

C

A

H i c b

V

C

7

S g

N

B

F

J

2

N r x h f q x

Y

W

N o

N

B

W

A v

D r k

W

0

D

N p

Y

W

E

Q w

D

0 j i

M j u

Z

T

Y b

M

P p i

5

K

4

Y l

F p b

+

R h o

L

R

W z

9

D

D t r f

8

T

J o

9

D

E

A x c

O

5

9 z

L v f d

4 s e

A

K b

P v

L y

C w s

L i

2 v

Z

F d z a

+ s b m

1 v m

9 k

5

V

R

Y m k r

E

I j

E c m

R x

Q

T

P

G

Q

V

4

C

B

Y

P

Z a

M

B

J

5 g

N a

9

3

M f

J r d

0 w q

H o

U

3

0

I

9

Z

K y

C d k

P u c

E t

C

S a

+

4

1

A w

J d

S g

S

+ c s

G d

1

M

4

D g a

3 c

O

S a e b t g j

4

H n i

T

M l

+

Z

J l f

T

8

9 q

G

H

Z

N

T

+ b

7

Y g m

A

Q u

B

C q

J

U w

7

F j a

K

V

E

A q e

C

D

X

L

N

R

L

G

Y

0

B

7 p s

I a m

I

Q m

Y a q

X j

B w b

4

U

C t t

7

E d

S

V w h

4 r

P e

S

E m g

V

D

/ w d

O f o

X

D

X r j c

T

/ v

E

Y

C

/ l k r

5

W

G c

A

A v p

Z

J

G f

C

A w

R

H q

W

B

2

1 w y

C q

K v

C a

G

S

1 s x

7

R

J

J

K

O j

M c j o

E

Z

/ b l e

V

I

9

K

T j

F

Q v

F a p

3

G

O

J s i i f

X

S

A

L

O

S g

U

1

R

C l i

M

K o i i

A

R q i

F

/

R q

P

B r

P x p v x

P m n

N

G

N

O

Z

X f

Q

H x s c

P

0

/

C

Z n g

=

=

<

/ l a t e x i t

>

Lt(xt t−m)

< l a t e x i t s h a

1

_ b a s e

4

=

" e

P

D

O

/

4

3

4

N

J

K

1

I v

+ m

K

J

J

3

P

W

B q

A

=

"

>

A

A

A

B

/

H i c b

V

C

7

S g

N

B

F

J

3

1

G e

M r m t

J m

S

B

A i

Q t i

1 i

J

Z

B

G w u

L

C

O

Y

B

2 b j

M

T i b

J k

N n

Z

Z e a u u

I

T

4

F f

Y

2

F o r

Y

+ i

F

2

+

R t n k x

S a e

G

D g c

M

9

3

D

P

H j w

T

X

Y

N s

T a

2

V

1 b

X

1 j

M

7

O

V

3 d

7

Z

3 d v

P

H

R w

2 d

B g r y u o

0

F

K

F q

+

U

Q z w

S

W r

A w f

B

W p

F i

J

P

A

F a

/ r

D q

9

R v

P j

C l e

S j v

I

I l

Y

J y

B

9 y

X u c

E j

C

S l

8 u

7

A

Y

E

B

J

Q

L f e

H

B v l x

4

9

O

P

F y

R b t s

T

4

G

X i

T

M n x

W r

B

P

X

2 e

V

J

O a l

/ t

2 u y

G

N

A y a

B

C q

J

1

2

7

E j

I y

I

A k

4

F

G

2 f d

W

L

O

I

0

C

H p s

7 a h k g

R

M d

0 b

T

8

G

N

8 b

J

Q u

7 o

X

K

P

A l

4 q v

7 e

G

J

F

A y

T w z

W

Q a

V

S

9 q f i f

1

4 h d

9

E

Z c

R n

F w

C

S d

H e r

F

A k

O

I

0 y

Z w l y t

G

Q

S

S

G

E

K q

4 y

Y r p g

C h

C w f

S

V

N

S

U

4 i

1

9 e

J o

2 z s l

M p

V

2

5

N

G

5 d o h g w

Q g

V

U

Q g

4

R

1

V

0 j

W q o j i h

K

0

A t

Q

+

/

W k

/

V q f

V i f s

9

E

V a

7

T

R

3

9 g f f

0

A q

K

S

X

H g

=

=

<

/ l a t e x i t

>

L0 t(xt)

L1 t(xt−1)

Lm t (xt−m)

L1 t+1(xt)

Lm t+m(xt)

< l a t e x i t s h a

1

_ b a s e

4

=

" o

9 y a

Y z c s

W o f e p n b

0 z

A

Z

W

H

4 w w

A

=

"

>

A

A

A

B

7

3 i c b

V

D

L

S s

N

A

F

J

3

4 r

P

V

V d e l m a

B

E q

Q k l c

V

J d

F

N y

4 r

2

A e

2

I

U y m k

3 b o

Z

B

J n b s

Q

Q

+ h

M i u

F

D

E r b

/ j r n

/ j

9

L

H

Q

1 g

M

X

D u f c y

7

3

3

+

L

H g

G m x

7 b

K

2 s r q

1 v b

O a

2

8 t s

7 u

3 v

7 h

Y

P

D p o

4

S

R

V m

D

R i

J

S b

Z

9 o

J r h k

D e

A g

W

D t

W j

I

S

+

Y

C

1

/ e

D

3 x

W

4

9

M a

R

7

J

O

0 h j

5 o a k

L

3 n

A

K

Q

E j t e

8

9

K

D

9

5 c

O o

V

S n b

F n g

I v

E

2 d

O

S r

V i

9

+ x l

X

E v r

X u

G

7

2

4 t o

E j

I

J

V

B

C t

O

4

4 d g

5 s

R

B

Z w

K

N s p

3

E

8

1 i

Q o e k z z q

G

S h

I y

7

W b

T e

0 f

4 x

C g

9

H

E

T

K l

A

Q

8

V

X

9

P

Z

C

T

U

O g

1

9

0 x k

S

G

O h

F b y

L

+

5

3

U

S

C

C

7 d j

M s

4

A

S b p b

F

G

Q

C

A w

R n j y

P e

1 w x

C i

I

1 h

F

D

F z a

2

Y

D o g i

F

E x

E e

R

O

C s

/ j y

M m m e

V

5 x q p

X p r

0 r h

C

M

+

T

Q

M

S q i

M n

L

Q

B a q h

G

1

R

H

D

U

S

R

Q

M

/ o

D b

1 b

D

9 a r

9

W

F

9 z l p

X r

P n

M

E f o

D

+ s

H l

B e

S q

Q

=

=

<

/ l a t e x i t

>

Zt(xt)

< l a t e x i t s h a

1

_ b a s e

4

=

" j

H

Y

L s

9

P

+ h h

F

L

O

A

R

2

W

2 m

C

X k

S

5 y

/

8

=

"

>

A

A

A

B

+

X i c b

V

D

L

T s

J

A

F

J

3 i

C

/

F

V d e m m g

Z h g

S

E j r

A l

0

S

3 b j

E

R

B

4

R m m

Y

D

D

B h

O m

1 m b o l

N w

1

+

4 d

O

N

C

Y

9 z

J

+

7

4

G w f

K

Q s

G

T

3

N y

T c

+

7

N

3

D l

+ x

J k

C

2

5

4

Z u

Y

3

N r e

2 d

/

G

5 h b

/

/ g

8

M g

8

P m m p

M

J a

E

N k n

I

Q

9 n x s a

K c

C d o

E

B p x

2

I k l x

4

H

P a

9 s e

3 c

7

8

9 o

V

K x

U

D x

A

E l

E

3 w

E

P

B

B o x g

0

J

J n m o

9 e

C h

V n

W n

7

K

+ o

V n l u y q v

Y

C

1

T p w l

K d

W

L v c r z r

J

4

0

P

P

O

7

1 w

9

J

H

F

A

B h

G

O l u o

4 d g

Z t i

C

Y x w

O i

3

0

Y k

U j

T

M

Z

4

S

L u a

C h x

Q

5 a a

L y f

W u

V b

1 i

C

U u g

R

Y

C

/

X

3

R o o

D p

Z

L

A

1

5

M

B h p

F a

9 e b i f

1

4

3 h s

G

1 m z

I

R x

U

A

F y

R

4 a x

N y

C

0

J r

H

Y

P

W

Z p

A

R

4 o g k m k u l b

L

T

L

C

E h

P

Q

Y

R

V

0

C

M

7 q l

9 d

J

7

L q

1

K q

1 e

5

3

G

D c q

Q

R

2 e o i

M r

I

Q

V e o j u

5

Q

A z

U

R

Q

R

P

0 g t

7

Q u

5

E a r

8 a

H

8

Z m

N

5 o z l z i n

A

+

P r

B

1 s n l d

I

=

<

/ l a t e x i t

>

Zt+1(xt+1)

t = 1,..., T L0 t+1(xt+1)

…

…

…

**Figure 2.** Diagonal: Zt(xt) depends only on xt, but includes loss/constraint components from next m rounds. Vertical: Lt(xt

t−m) includes function components only from round t, but depends on all past m decisions.

see Figure 2). Our strategy is to bound the regret of Zt and translate that bound to the initial problem. A similar construction was used for OCO in (Mhaisen and Iosifidis 2024).

The next new decomposition lemma ties the regret and CCV to memory-based surrogate loss and forward function. Lemma 3. For any valid penalty function Φ and under Assumption1 4 it holds:

Φ

VT

−Φ

Vm−1

+ Rmc

T ≤RT (L) + G(m + 1) Φ′

VT

(20)

≤RT (Z) + G(m + 1) Φ′

VT

. (21)

where the regret is defined for benchmarks in the set:

X mp

T = x ∈X: g i t (x) ≤0, ∀t ∈T, i ≤m

.

Equipped with this result, it suffices to bound RT (Z), which we achieve by utilizing predictions to cope with its delayed gradients. In particular, we leverage (Flaspohler et al. 2021) that proposed a suite of delayed–optimistic algorithms (without memory or constraints), and adapt their Optimistic Delayed AdaF (ODAF) algorithm, which has the tightest guarantees, for our problem. ODAF relies on FTRL (McMahan 2011) which decides the next decision using all the previous gradients. In the standard delayed-feedback OCO, the entire gradient ∇ft(xt) is revealed in one shot, exactly m rounds after xt is decided. With a memory window of length m the situation is subtler: each decision xt affects some of the components of the loss functions in rounds t,..., t + m; hence, the gradient information arrives piecemeal and may be delayed up to m rounds before fully revealed. Specifically, at round t the learner possesses: ✓revealed gradients ∇Zτ(xτ), for τ = 1,..., t −m −1

(coming from x1,..., xt−m−1); ◦delayed gradients that still depend on xt−m,..., xt−1; × unseen gradients that will depend on decision xt.

With this in mind, we perform OL using an oracle that provides the next forward function gradient:

∇˜Zt(˜xt) = m X i=0 h

∇˜f i t+i(˜xt) + Φ′

Vt−m−1+i

∇˜gi,+ t+i(˜xt)

i

,

1We trivially set ft(·) = gt(·) = 0 for t ≤m or t > T.

## Algorithm

2: Optimistic learning for COCO-M2

Require: initial history xm

0 ∈X m+1; dual seed ˆV m−1 0 ←0 1: for t = m + 1 to T −1 do 2: Play xt and observe ft(·), gt(·) 3: Calculate ft(xt t−m), gt(xt t−m). 4: Vt ←Vt−1 + g+ t (xt t−m) 5: Compute the prediction error ϵt−m as in (22). 6: Compute the predictions ht+1 7: Decide decision: xt+1 ←ODAF (∇Z1:t−m, ht+1, ϵt−m). 8: end for as well as the missing past gradients, which we combine into a single hint vector: ht.= m−1 X i=0 m−i−1 X j=0 h

∇f j t−m+i+j+Φ′

Vt+i+j−2m−1

∇gj,+ t−m+i+j i

| {z } available at t

+ m X j=m−i h

∇˜f j t−m+i+j+Φ′

Vt+i+j−2m−1

∇˜gj,+ t−m+i+j i!

+∇˜Zt

| {z } future predictions where we denote ∇Zt(xt) with ∇Zt, and ∇˜Zt(˜xt) with ∇˜Zt.

Similarly to other OL algorithms (Rakhlin and Sridharan 2013b), ODAF performs an update (here, using FTRL) whose regularization is scaled by the prediction error. After the decision is committed, the losses ft and gt are revealed, rendering available the forward function Zt−m(xt−m). At the end of t, the learner therefore knows the gradients ∇Zτ for all τ = 1,..., t−m and can evaluate the error of the hint ht−m, which covered the window τ = (t −2m)(:t −m), ϵt−m(Z) = t−m X τ=t−2m

∇Zτ −ht−m

2

, (22)

with ET (Z) = PT t=m ϵt(Z) denoting the cumulative prediction error. The loss-function prediction error is then:

ϵt−m(f) = t−m X s=t−2m m X i=t−s

∇˜f i s+i(˜xs) −∇f i s+i(xs)

2

, where the outer sum runs over the last m decisions xs, s = t −m,..., m, whose delayed contributions have not been fully revealed at t −m, and the inner sum selects only those slices that arrive after t−m (i.e., delays i ≥t−s), and measures the difference between their predicted and true gradients. Similarly, we can define the constraint-function error as ϵt−m(g+), and we denote ET (f) = PT t=m ϵt(f) and ET (g+) = PT t=m ϵt(g+) the cumulative errors. Having clarified the prediction and error calculations, we proceed to present the learning mechanism, which is summarized in Algorithm 2. At each round t the learner chooses an decision xt, observes the realized loss and constraint functions (line 3), and updates the multiplier Φ′

Vt−m−1 for use at the next step. It then evaluates the prediction–error

19529

<!-- Page 7 -->

(line 5) and predicts the forward loss ht+1 for the next round; finally, it feeds the ODAF routine (line 7) with the cumulative revealed gradients ∇Z1:t−m, the hintht+1, and the prediction error ϵt−m, to find the next decision. Due to lack of space, the details for ODAF are deferred to Appendix. Essentially, using the hints and prediction errors designed specifically for our problem, one can readily call the algorithm from (Flaspohler et al. 2021). The next theorem establishes regret and CCV guarantees for this optimistic setting. Theorem 3. Under the following conditions:

• Assumptions 1, 2, 3, 4 and 5 hold; • The update rule is ODAF; • Φ(V)=exp(λV)−1, with λ = 1 2

C√

ET (g+)+G(m+1)

, the following bounds hold:

Rmc

T = O p

ET (f)

, (23)

Vmc

T = O p

ET (g+) + m log T

. (24)

Discussion. Let us start by noting that the value of λ depends on the (unknown) prediction error ET (g), but we can adjust it online via a doubling trick that adds only an extra log T to the bounds, similar in spirit to (Lekeufack and Jordan 2024); the full analysis is in Appendix. As prediction accuracy improves, the bounds tighten, where under perfect prediction, they reach O(1) regret and O(m log T) CCV. On the other hand, even if the predictors fail completely, the algorithm guarantees regret O(m2√

T) and CCV O(m2√

T log T). These bounds are tighter than those of Section 4, but they refer to a more restrictive benchmark X mp

T ⊂X m

T. What is more, the predictions accuracy does not need to be known in advance, and, further, our solution allows the oracle to update its forecast at every round and benefit from more accurate information whenever available. This flexibility is crucial as predictions can indeed improve with time. Finally, we note that these bounds include as special cases important prior works. When m = 0, the rates coincide with those of (Lekeufack and Jordan 2024), who study COCO with predictions but no memory. For OCO- M, (Mhaisen and Iosifidis 2024) obtain O(1) regret under perfect predictions, relying on the delayed-feedback framework of (Flaspohler et al. 2021); our analysis yields the same bound when constraints are omitted. Our work extends these ideas to time-varying and memory-dependent constraints.

There are also some important notes in place regarding the Assumptions. First, observe that the surrogate function uses the delayed penalty Vt−m−1 because at t the freshest known value is Vt−1. Relying on Vt−m−1 let us form ∇˜Zt without forecasting the entire future constraint gt(xt t−m), and yet it does not affect the bound. Secondly, due to Assumption 5, the gradient of f i t+i is the constant coefficient vector (independent of xt), and for the constraint gi,+ t+i(x) = max{0, ai t+ix + bi t+i}, we only need to predict the sign of ai t+ixt+bi t+i. Thus the predictor only guesses the half-space of xt, a far weaker requirement than guessing the exact ˜xt. However, this assumption can be lifted if a predictor is available that directly provides an estimate ˜xt of xt.

Finally, there is an interesting trade-off between the assumptions about the predictions and the problem structure. In general, satisfying the memory-based constraints gt(xt t−m) would require not only forecasting the future loss and constraints, but also their dependence on the yetunknown decisions xt+1,..., xt+m, which in turn demands perfect predictions for a look-ahead horizon H = Θ(log T) as in (Yu et al. 2020). For shorter or imperfect forecasts, the sublinear bounds are not guaranteed. To sidestep this, we invoke Assumption 4 and replace the comparator set X m

T with X mp

T. This relaxation allows us recasting it as a memoryless problem with delayed gradients. Consequently, we recover sublinear bounds on both regret an CCV, even under untrusted predictions. The reader might recall that similar concessions about the benchmark set are made in traditional COCO, where X is reduced to XT so as to avoid the impossibility result of (Mannor, Tsitsiklis et al. 2009). Making bolder assumptions for the availability of more informative predictions to learn against an expanded benchmark set is certainly a direction where our framework can be extended.

## 6 Conclusions

As discussed, COCO-M2 appears in many real systems, e.g., smart-grid energy budgets, battery-health limits, etc., and directly captures the handling of constraints in NSC. Our penalty method tightens the only prior COCO-M2 rates of (Liu, Yang, and Ying 2023) (O(T 2/3 log2 T)) to RT = O m3/2√T log T and VT = O max{T 3/4, m3/2√T log T}

, and extends the analysis to the COCO-M case. Moreover, this is the first work to study untrusted gradient forecasts for timevarying COCO problems with memory. The proposed optimistic algorithm achieves RT = O p

ET f and VT = O max{ p

ET g log T, m log T}

, matching the results of (Lekeufack and Jordan 2024) without memory and reducing to them when m = 0. Indeed, previous COCO, OCO-M and optimistic OCO bounds emerge as special cases of our framework. Finally, as future work, these techniques can be extended to dynamic (adaptive) regret metrics via static-todynamic reductions, and with the design of penalties that react to time-varying windows and constraint hardness.

19530

<!-- Page 8 -->

## Acknowledgments

The work was supported in part by the Dutch National Growth Fund through the 6G flagship project “Future Network Services” and by the European Commission under Grants 101139270 (ORIGAMI) and 101192462 (FLECON- 6G), and in part by the French government through the France 2030 program within the Celtic RAI-6green project.

## References

Agarwal, N.; Hazan, E.; and Singh, K. 2019. Logarithmic regret for online control. Advances in Neural Information Processing Systems (NeurIPS), 32. Anava, O.; Hazan, E.; and Mannor, S. 2015. Online learning for adversaries with memory: price of past mistakes. Advances in Neural Information Processing Systems (NeurIPS), 28. Anderson, D.; Iosifidis, G.; and Leith, D. J. 2023. Lazy Lagrangians for Optimistic Learning with Budget Constraints. IEEE/ACM Transactions on Networking, 31(5): 1935–1949. Chaudhary, S.; and Kalathil, D. 2022. Safe Online Convex Optimization with Unknown Linear Safety Constraints. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, 6175–6182. Flaspohler, G. E.; Orabona, F.; Cohen, J.; Mouatadid, S.; Oprescu, M.; Orenstein, P.; and Mackey, L. 2021. Online learning with optimism and delay. In International Conference on Machine Learning (ICML), 3363–3373. PMLR. Guo, H.; Liu, X.; Wei, H.; and Ying, L. 2022. Online Convex Optimization with Hard Constraints: Towards the Best of Two Worlds and Beyond. Advances in Neural Information Processing Systems (NeurIPS), 35: 36426–36439. Gyorgy, A.; and Neu, G. 2014. Near-Optimal Rates for Limited-Delay Universal Lossy Source Coding. IEEE Transactions on Information Theory, 60(5): 2823–2834. Hazan, E.; and Singh, K. 2025. Introduction to Online Control. arXiv:2211.09619. Jiang, N.; Hutchinson, S.; and Alizadeh, M. 2025. Online Nonstochastic Control with Convex Safety Constraints. arXiv preprint arXiv:2501.18039. Joulani, P.; Gyorgy, A.; and Szepesvari, C. 2020. A modular analysis of adaptive (non-)convex optimization: Optimism, composite objectives, variance reduction, and variational bounds. Theoretical Computer Science, 808: 108– 138. Leith, D. J.; and Iosifidis, G. 2023. Penalized FTRL with Time-Varying Constraints. In Proceedings of the European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases (ECML/PKDD), 311–326. Lekeufack, J.; and Jordan, M. I. 2024. An Optimistic Algorithm for Online Convex Optimization with Adversarial Constraints. arXiv preprint arXiv:2412.08060. Li, T.; Yang, R.; Qu, G.; Shi, G.; Yu, C.; Wierman, A.; and Low, S. 2022. Robustness and Consistency in Linear Quadratic Control with Untrusted Predictions. Proceedings of the ACM on Measurement and Analysis of Computing Systems, 6(1): 1–35. Li, Y.; Chen, X.; and Li, N. 2019. Online Optimal Control with Linear Dynamics and Predictions: Algorithms and Regret Analysis. Advances in Neural Information Processing Systems (NeurIPS), 32. Li, Y.; Das, S.; and Li, N. 2021. Online optimal control with affine constraints. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, 8527–8537. Liakopoulos, N.; Destounis, A.; Paschos, G.; Spyropoulos, T.; and Mertikopoulos, P. 2019. Cautious Regret Minimization: Online Optimization with Long-Term Budget Constraints. In Proceedings of the 36th International Conference on Machine Learning (ICML), Proceedings of Machine Learning Research, 3944–3952. PMLR. Liu, X.; Yang, Z.; and Ying, L. 2023. Online Nonstochastic Control with Adversarial and Static Constraints. In Proceedings of the International Conference on Machine Learning (ICML). Mahdavi, M.; Jin, R.; and Yang, T. 2012. Trading Regret for Efficiency: Online Convex Optimization with Long Term Constraints. Journal of Machine Learning Research, 13(1): 2503–2528. Mannor, S.; Tsitsiklis, J. N.; et al. 2009. Online Learning with Sample Path Constraints. Journal of Machine Learning Research, 10(3). McMahan, B. 2011. Follow-the-Regularized-Leader and Mirror Descent: Equivalence Theorems and ℓ1 Regularization. In Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics (AISTATS), 525–533. JMLR Workshop and Conference Proceedings. Merhav, N.; Ordentlich, E.; Seroussi, G.; and Weinberger, M. J. 2002. On Sequential Strategies for Loss Functions with Memory. IEEE Transactions on Information Theory, 48(7): 1947–1958. Mhaisen, N.; and Iosifidis, G. 2024. Optimistic Online Non- Stochastic Control via FTRL. In Proceedings of the IEEE Conference on Decision and Control (CDC). Mohri, M.; and Yang, S. 2016. Accelerating Online Convex Optimization via Adaptive Prediction. In Proceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS). Nonhoff, M.; and M¨uller, M. A. 2021. An online convex optimization algorithm for controlling linear systems with state and input constraints. In 2021 American Control Conference (ACC), 2523–2528. IEEE. Orabona, F. 2025. A modern introduction to online learning. arXiv preprint arXiv:1912.13213. Qiu, S.; Wei, X.; and Kolar, M. 2023. Gradient-Variation Bound for Online Convex Optimization with Constraints. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 9534–9542. Rakhlin, A.; and Sridharan, K. 2013a. Optimization, Learning, and Games with Predictable Sequences. In Advances in Neural Information Processing Systems (NeurIPS).

19531

<!-- Page 9 -->

Rakhlin, S.; and Sridharan, K. 2013b. Optimization, Learning, and Games with Predictable Sequences. Advances in Neural Information Processing Systems (NeurIPS), 26. Sinha, A.; and Vaze, R. 2024. Optimal Algorithms for Online Convex Optimization with Adversarial Constraints. Advances in Neural Information Processing Systems (NeurIPS), 37: 41274–41302. Valls, V.; Iosifidis, G.; Leith, D.; and Tassiulas, L. 2020. Online Convex Optimization with Perturbed Constraints: Optimal Rates against Stronger Benchmarks. In Proceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS). Wang, J.; Yan, B.; and Liu, Y. 2025. Doubly-Bounded Queue for Constrained Online Learning: Keeping Pace with Dynamics of Both Loss and Constraint. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 21135–21143. Wang, Y.; Wan, Y.; and Zhang, L. 2025. Revisiting Projection-Free Online Learning with Time-Varying Constraints. Proceedings of the AAAI Conference on Artificial Intelligence, 39(20): 21339–21347. Yan, Y.-H.; Zhao, P.; and Zhou, Z.-H. 2023. Online Non- Stochastic Control with Partial Feedback. Journal of Machine Learning Research, 24(273): 1–50. Yu, C.; Shi, G.; Chung, S.-J.; Yue, Y.; and Wierman, A. 2020. The power of predictions in online control. Advances in Neural Information Processing Systems (NeurIPS), 33: 1994–2004. Yu, C.; Shi, G.; Chung, S.-J.; Yue, Y.; and Wierman, A. 2022. Competitive Control with Delayed Imperfect Information. In 2022 American Control Conference (ACC), 2604–2610. IEEE. Yu, H.; and Neely, M. J. 2020. A Low Complexity Algorithm with O(

√

T) Regret and O(1) Constraint Violations for Online Convex Optimization with Long Term Constraints. Journal of Machine Learning Research, 21(1): 1– 24. Yuan, J.; and Lamperski, A. 2018. Online Convex Optimization for Cumulative Constraints. In Advances in Neural Information Processing Systems (NeurIPS), 6140–6149. Zangwill, W. I. 1967. Non-Linear Programming via Penalty Functions. Management Science, 13(5): 344–358. Zhang, H.; Guo, H.; and Liu, X. 2025. On the Power of Optimism in Constrained Online Convex Optimization. In Kwok, J., ed., Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence (IJCAI-25), 6976–6983. International Joint Conferences on Artificial Intelligence Organization. Main Track. Zhang, R.; Li, Y.; and Li, N. 2021. On the Regret Analysis of Online LQR Control with Predictions. In 2021 American Control Conference (ACC), 699–703. IEEE. Zhou, H.; and Tzoumas, V. 2023. Safe non-stochastic control of linear dynamical systems. In Proceedings of the IEEE Conference on Decision and Control (CDC). Zinkevich, M. 2003. Online Convex Programming and Generalized Infinitesimal Gradient Ascent. In Proceedings of the International Conference on Machine Learning (ICML).

19532
