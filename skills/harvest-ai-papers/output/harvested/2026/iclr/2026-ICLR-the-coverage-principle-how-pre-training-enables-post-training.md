---
title: "The Coverage Principle: How Pre-Training Enables Post-Training"
source_url: https://iclr.cc/virtual/2026/oral/10011030
paper_pdf_url: https://arxiv.org/pdf/2510.15020v2
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# The Coverage Principle: How Pre-Training Enables Post-Training

<!-- Page 1 -->

The Coverage Principle: How Pre-Training Enables Post-Training

Fan Chen1 Audrey Huang2 Noah Golowich3 Sadhika Malladi3

Adam Block4 Jordan T. Ash3 Akshay Krishnamurthy3 Dylan J. Foster3

## Abstract

Language models demonstrate remarkable abilities when pre-trained on large text corpora and fine-tuned for specific tasks, but how and why pre-training shapes the success of the final model remains poorly understood. Notably, although pre-training success is often quantified by cross-entropy loss, cross-entropy can be a poor predictor of downstream performance. Instead, we provide a theoretical perspective on this relationship through the lens of coverage, which quantifies the probability mass the pre-trained model places on high-quality responses and which is necessary and sufficient for post-training and test-time scaling methods such as Best-of-N to succeed. Our main results develop an understanding of the coverage principle, a phenomenon whereby next-token prediction (more generally, maximum likelihood) implicitly optimizes toward a model with good coverage. In particular, we uncover a mechanism that explains the power of coverage in predicting downstream performance: coverage generalizes faster than cross-entropy, avoiding spurious dependence on problem-dependent parameters such as the sequence length. We also study practical algorithmic interventions with provable benefits for improving coverage, including (i) model/checkpoint selection procedures, (ii) gradient normalization schemes, and (iii) test-time decoding strategies.

## Introduction

The remarkable capabilities of language models stem from a two-stage training process: (1) large-scale pretraining via next-token prediction with the cross-entropy loss (predicting what token should follow a prefix) and (2) targeted post-training—typically via reinforcement learning—to adapt the model to specific domains and tasks. Investing more compute and data into pre-training often enables post-training to produce a stronger model, but theoretical understanding of how these stages interact is limited. Indeed, despite substantial investment into scaling pre-training (Gadre et al., 2025; Sardana et al., 2024; Hoffmann et al., 2022), several works have demonstrated that starting post-training from a better next-token predictor does not ensure stronger performance on downstream tasks (Liu et al., 2022; Zeng et al., 2025; Chen et al., 2025; Lourie et al., 2025; Springer et al., 2025). Motivated by this disconnect, we theoretically investigate the connection between pre-training objectives and downstream success, asking:

Can we precisely characterize the relationship between the next-token prediction loss and downstream performance? What metrics are most predictive of downstream success?

Motivated by the recent interest in test-time scaling, we focus our attention on post-training via Best-of-N (BoN) sampling or reinforcement learning with verifiable rewards. For a prompt x, Best-of-N draws N responses y from the model and returns the best response according to a task-specific reward. Several prior works have demonstrated that the performance of BoN is strongly indicative of how well the model will perform after post-training via reinforcement learning (Yue et al., 2025; Wu et al., 2025).

1MIT, fanchen@mit.edu. Work partially completed during an internship at Microsoft Research. 2UIUC, audreyh5@illinois.edu. Work partially completed during an internship at Microsoft Research. 3Microsoft Research NYC, nzg@mit.edu, sadhika.malladi98@gmail.com, {ash.jordan, akshaykr, dylanfoster}@microsoft.com 4Columbia University, adam.block@columbia.edu arXiv:2510.15020v2 [stat.ML] 22 Oct 2025

<!-- Page 2 -->

0.0 0.2 0.4 0.6 0.8 Cov2.0

0.8

0.9

1.0 1.0

Pass@ N

Pass@4 Selected model Model w/ min. KL

0.0 0.1 0.2 Cov4.0

0.92

0.96

1.00 1.00

Pass@8 Selected model Model w/ min. KL

0.00 0.05 0.10 Cov5.7

0.96

0.98

1.00 1.00

Pass@12 Selected model Model w/ min. KL

0k 10k 20k 30k 40k 50k Iteration

0.0

0.2

0.4

0.6

0.8

1.0

CovN

KL Cov2.0 Cov3.0 Cov4.0 Cov4.6 Cov5.7

0.0

0.5

1.0

1.5

2.0

KL

0.0 0.5 1.0 1.5 KL

0.0 0.5 1.0 1.5 KL

0.0 0.5 1.0 1.5 KL

**Figure 1.** The coverage profile predicts Pass@N better than KL divergence. We train models in a graph reasoning task and record KL divergence, coverage profile (both measured w.r.t. πD), and Pass@N performance; see Appendix C for details. Left: Convergence of coverage and KL divergence over training, showing that KL im-

proves monotonically but coverage can degrade with training. Right: Scatter plots of KL (top axis), CovN/2 (lower axis) and Pass@N of checkpoints. Although KL and CovN exhibit comparable predictive power for small N, CovN is a better predictor for large N. Also visualized are checkpoints selected via the tournament procedure of Eq. (29) (marked ♢) and by minimizing KL (marked red), demonstrating that the former selects better models for Pass@N.

Our starting point is the observation that cross-entropy alone cannot provide meaningful answers to the questions above; see Figure 1, which illustrates that cross-entropy can be anti-correlated with BoN performance, echoing Chen et al. (2025). Instead, we show that the missing link is the coverage profile, a refinement of cross-entropy that explicitly quantifies the model’s ability to assign sufficient probability to rare but high-quality responses.

Definition 1.1 (Coverage profile). The coverage profile of a model bπ for a distribution π is

CovN(π ∥bπ):= Px∼µ,y∼π(·|x)

π(y | x)

bπ(y | x) ≥N

, (1)

where N ≥1 is the number of Best-of-N sampling attempts.

Here, y is the full response when prompted with x, π represents the pre-training data distribution, which we presuppose covers downstream tasks of interest, and bπ is the pre-trained model. We prove that a good coverage profile is necessary and sufficient for Best-of-N to succeed (see Section 2, as well as Propositions D.6 and D.7). This is highlighted in Figure 1, where we find that the coverage profile is correlated with downstream performance for Best-of-N (which is exactly Pass@N), even when cross-entropy is not.1 Motivated by this characterization of BoN performance, we ask: When, and through what mechanism, does next-token prediction produce a model bπ with good coverage?

## 1.1 Contributions

We develop a theoretical understanding of the coverage principle, whereby next-token prediction implicitly optimizes toward a model with good coverage, inheriting the training corpus’ coverage over tasks of interest.

Cross-entropy: Scaling laws and limitations (Section 3). We begin by deriving provable scaling laws that link cross-entropy—specifically, a certain sequence-level notion—to coverage and hence downstream performance, but show that cross-entropy can be sensitive to sequence length and other problem parameters, leading to vacuous predictions; this motivates our main results.

Next-token prediction implicitly optimizes coverage (Section 4). The first of our main theoretical results (Theorem 4.1) is a new generalization analysis for next-token prediction (more generally, maximum likelihood) that exploits the unique structure of the logarithmic loss to show that coverage can generalize faster than cross-entropy; we refer to this as the coverage principle. Concretely, our analysis shows that the coverage profile for models learned with next-token prediction (i) avoids spurious dependence on problem-dependent parameters such as sequence length (in contrast to cross-entropy), and (ii) converges faster still as the tail parameter N is increased. Our analysis—which is similar in spirit to Mendelson’s small ball

1Formally, the coverage profile refines cross-entropy/KL divergence; see Remark 2.1.

<!-- Page 3 -->

method (Mendelson, 2014, 2017)—can be viewed as giving a new, fine-grained understanding of maximum likelihood (Wong and Shen, 1995; van de Geer, 2000; Zhang, 2006), which we expect to be of broader interest.

Stochastic gradient descent through the lens of coverage (Section 5). The preceding results apply to general model classes Π, but consider the empirical maximizer of the next-token prediction (maximum likelihood) objective, in the vein of classical techniques in learning theory. For the second of our main results, we focus on a specific model class—overparameterized autoregressive linear models (3)—but take a more realistic approach and analyze stochastic gradient descent (SGD) on the next-token prediction objective, in the one-pass (“compute-optimal”) regime. We show that while SGD provably optimizes the coverage profile, it experiences suboptimal dependence on the sequence length H. We then show that gradient normalization (which is loosely connected to Adam-like updates (Bernstein and Newhouse, 2024)) provably improves coverage, removing dependence on the sequence length. We also consider the expert distillation setting where πD represents a teacher network for which token-level logits are available, and give a novel gradient normalization scheme which enjoys improved coverage even further.

Interventions for better coverage (Section 6). Finally, we look beyond standard next-token prediction and explore families of new interventions aimed at improving coverage in theory. (i) Test-time (Section 6.1). We show that for standard token-level SGD, a decoding strategy inspired based on test-time training (Krause et al., 2019; Sun et al., 2024; Akyürek et al., 2025) provably improves coverage. (ii) Model/checkpoint selection (Section 6.3). For selecting the best model (or checkpoint) from a small number of candidates, we give tournament procedures that enjoy significantly better coverage profile (particularly with respect to the tail parameter N) than naïve validation with cross-entropy.

Additional results (Appendix E). Beyond the results above, we show that coverage profile satisfies additional properties, including: (1) maximum likelihood can find models with low coverage even in the presence of severe misspecification (e.g., even if no model with low cross-entropy exists) (Appendix E.1); (2) coverage can generalize better under additional structural properties of the model class such as convexity (Appendix E.1).

In summary, we believe that coverage offers a new perspective on the connection between pre-training objectives and downstream post-training success. Our results demonstrate that this perspective is mathematically rich and fundamental, opening the door to a deeper understanding. To this end, we highlight a number of fascinating directions for future research in Section 7.

## 2 Problem Setup

We now introduce the formal problem setup for the remainder of the paper.

Next-token prediction and maximum likelihood. We work in the following setting, which subsumes next-token prediction: X is the prompt space, Y is the response space, and πD: X →∆(Y) is the data distribution. We are given a dataset D = {(xi, yi)}n i=1 where xi ∼µ and yi ∼πD(· | xi). We consider the maximum likelihood objective bLn(π):= n X i=1 log π(y i | x i). (2)

and refer to bπ:= arg maxπ∈Π bLn(π) as the maximum likelihood estimator for a user-specified model class Π. This is a generalization of the next-token prediction, where Y = VH is a token sequence and π(y | x) = QH h=1 π(yh | x, y1:h−1) is explicitly autoregressive, so that bLn(π) = Pn i=1

PH h=1 log π(yi h | xi, yi

1:h−1). We specialize to next-token prediction at certain points but otherwise focus on the general setting. We make the following realizability assumption throughout.

Assumption 2.1 (Realizability). The data distribution πD is realizable by some model π ∈Π.

This formulation captures pre-training and supervised fine-tuning, with some caveats; see Section 7.1.

<!-- Page 4 -->

Post-training and the coverage profile. Given a reward function rT(x, y) ∈{0, 1} representing success at a downstream task T, the goal is to fine-tune bπ—through reinforcement learning or test-time scaling—to obtain near-optimal reward. We show (Propositions D.6 and D.7) that for any task-specific comparator policy πT: X →∆(Y), Best-of-N sampling with eΘ(N) samples satisfies Ex∼µ[rT(x, πT(x)) −rT(x, bπBoN(x))] ≍CovN(πT ∥bπ), so a good coverage profile for πT is sufficient for high reward. Further, while less well understood, some form of coverage is thought to be necessary for the success of post-training methods like GRPO (Yue et al., 2025).

Returning to pre-training, it is clear that there is little hope that next-token prediction will produce a model bπ with good coverage with respect to a downstream task unless the data distribution πD itself has reasonable coverage with respect to this task. We therefore posit that the data distribution covers such a downstream task, in the sense that it includes high-reward responses with some bounded-below probability. Since coverage satisfies a transitivity property, it follows that coverage with respect to πD implies coverage with respect to the optimal policy for the downstream task. For example, if πD has a 10% chance of generating a correct response, and CovN/10(πD ∥bπ) = ε, then we get 10ε error.2 Thus, going forward, we focus on understanding when nexttoken prediction achieves good coverage CovN(πD ∥bπ) relative to the data distribution πD itself, and avoid concerning ourselves with specific details of the task policy πT or the specific relationship between πT and πD.

Autoregressive linear models. We analyze next-token prediction and maximum likelihood for general model classes Π, but our running example throughout the paper will be the class Π of autoregressive linear models, defined by a known feature map ϕ: X × V⋆→Rd. For each parameter θ ∈Θ ⊂Rd, the model πθ = (πθ)H h=1 is defined by πθ(yh | x, y1:h−1) ∝exp(⟨θ, ϕ(x, y1:h)⟩). (3)

In practice, autoregressive sequence models—such as those based on transformers—generate each token by sampling from a softmax distribution whose logits are given by a linear combination of learned features (Radford et al., 2019). Eq. (3) simplifies this by freezing the feature map, yet remains expressive enough to model complex non-Markovian dependencies, depending on the choice of features.

Assumption 2.2. We assume Θ ⊆{θ: ∥θ∥≤1} is convex, and suph,x,y1:h∥ϕ(x, y1:h)∥≤B for some B ≥1.

Additional notation. We adopt standard big-oh notation, and write f = eO(g) to denote that f = O(g · max{1, polylog(g)}), a ≲b as shorthand for a = O(b), and a ≍b as shorthand for a = Θ(b).

## 2.1 Properties of the Coverage Profile

Before proceeding, we briefly discuss some properties of the coverage profile that will be helpful to keep in mind.

Remark 2.1 (Coverage profile as a refinement of cross-entropy). The coverage profile can be viewed as a fine-grained, inference budget-sensitive refinement of cross-entropy. Concretely, if we write

CovN(πD ∥bπ) = PπD log πD(y | x)

bπ(y | x) ≥log N

, (4)

it becomes clear that the coverage profile is simply the cumulative distribution function (CDF) of the log density ratio X:= log πD(y|x)

bπ(y|x), while KL-divergence corresponds to the mean: EπD[X]. It is well known that the CDF of a random variable is a more informative statistic than its mean (Durrett, 2019); the former can be much more sensitive to the model’s behavior at the tail than the latter. Indeed, the coverage profile can behave very differently across scales, as shown by Figure 1.3

Remark 2.2 (KL divergence and coverage profile are not estimable). We emphasize that KL-divergence and the coverage profile are not estimable quantities in general, due to the fact both depend on the unknown density πD(y | x) for the data distribution. This motivates the use of cross-entropy in practice, as the former is an estimable upper bound on DKL(πD ∥bπ). Analogously, we show in Section 6.3 that various estimable proxies for the coverage profile can be used to select models with good coverage. One exception is the expert distillation setting (see Section 6.2), where πD is a teacher network for which the log-probabilities log πD(y | x) are available.

2See Proposition D.5 for formal results. 3Interestingly, we show (Proposition D.1) that if the coverage profile satisfies a certain growth condition uniformly for all scales M, then it implies a bound on KL-divergence—a weak converse to Proposition 3.1.

<!-- Page 5 -->

0k 10k 20k 30k 40k Iterations

0

10

15

20

KL

H=8 H=16 H=24

0k 10k 20k 30k 40k Iterations

0.00

0.25

0.50

0.75

1.00

CovN = 16

H=8 H=16 H=24

0k 10k 20k 30k 40k Iterations

0

50

100

150

200

Ratio KL

CovN = 16

H=8 H=16 H=24

**Figure 2.** The coverage profile avoids spurious dependence on sequence length. We train models in a graph reasoning task and record their KL divergence and coverage profile, measured w.r.t. πD as we vary the

problem horizon (sequence length); see Appendix C for details. Left: Convergence of KL over training for three horizons H, demonstrating that KL at convergence scales linearly in the horizon H. Center: Convergence of

CovN over training, manifesting no dependence on H at convergence. Right: Ratio of KL over CovN, showing that Proposition 3.1 can be overly conservative.

## 3 Cross-Entropy and Coverage: Scaling Laws and Limitations

A natural approach to understanding when next-token prediction achieves good coverage is to appeal to cross-entropy—perhaps first showing that next-token prediction achieves low cross-entropy (which is true asymptotically), and then relating cross-entropy to coverage. In this section we motivate our main results by showing that while this is possible in a weak sense, it does not yield predictive guarantees for downstream performance in the finite-sample regime.

Define the sequence-level cross-entropy for bπ as DCE(πD ∥bπ):= EπD hPH h=1 log 1 bπ(yh|x,y1:h−1)

i

. Since ED i.i.d. ∼πD bLn(π)

=

−n · DCE(πD ∥π), one expects that as we scale up compute, number of samples n, and model capacity Π,

DCE(πD ∥bπ) →DCE(πD ∥πD), or equivalently DKL(πD ∥bπ) →0, where DKL(πD ∥bπ):= EπD hPH h=1 log πD(yh|x,y1:h−1)

bπ(yh|x,y1:h−1)

i is the sequence-level KL divergence.

A simple scaling law for cross-entropy. We show below that if the model bπ has reasonable KL divergence to the data distribution, the coverage profile can be bounded:

Proposition 3.1 (KL-to-coverage; see Proposition D.1). For all N ≥e, CovN(πD ∥bπ) ≤DKL(πD ∥bπ)

log(N/e).

Combining Proposition 3.1 with Proposition D.6 and our assumption that πD has good coverage with respect to the downstream task yields a simple “scaling law” for test-time compute with BoN:

Consider a task of interest with reward rT(x, y), and suppose the data distribution πD itself has constant probability of success (i.e., sampling y ∼πD(· | x) with rT(x, y) = 1). To achieve sub-optimality ε with Best-of-N, it suffices to choose the compute budget N as

N ≈exp

DKL(πD ∥bπ)

ε

. (5)

That is, for a fixed model bπ and KL-divergence level DKL(πD ∥bπ) ≤DCE(πD ∥bπ), Eq. (5) predicts that test-time compute should increase exponentially with the desired accuracy ε.4

Insufficiency of cross-entropy. At first glance, this seems to be in line with empirical test-time scaling laws (OpenAI, 2024), but there is an issue: While token-level cross-entropy has been observed to be modest in contemporary language models (Kaplan et al., 2020; Hoffmann et al., 2022; Xia et al., 2022), the sequence-level cross-entropy (and KL-divergence) generally grows with the length H of the sequence, so that Eq. (5) predicts

4Neither KL divergence nor the coverage profile are observable quantities (though cross-entropy is an estimable upper bound on KL), so this is a theoretical prediction rather than a practical one as-is; see Remark 2.2.

<!-- Page 6 -->

exponential test-time scaling in the sequence length. Moreover, such a law cannot hold if we only assume token-level cross-entropy is bounded; see Proposition D.7.

Is this the end of the story? On the one hand, it is simple to show (Proposition D.2) that Proposition 3.1 is tight for a worst-case pair of models. Moreover, even for the autoregressive linear model in Eq. (3), sequence-level KL divergence scales linearly with the sequence length H, as shown in the next result.

Proposition 3.2. Fix H ∈N and d = 1. There exists a feature map ϕ: X × V⋆→[−1, 1] and induced autoregressive linear class Π with parameter space Θ = [−1, 1], distribution µ over X, such that for any proper estimator bπ = bπ(D) ∈Π, there exists data distribution πD ∈Π such that with probability at least 0.25,

DKL(πD ∥bπ) ≥H

4n. (6)

This behavior is reflected empirically in Figure 2 for a graph reasoning task. Yet, for this task, we find (Figure 2) that in spite of large cross-entropy/KL, next-token prediction learns a model bπ with a good coverage profile across a range of sequence lengths and that downstream Best-of-N succeeds. Why is this happening? In light of the discussion above, it must be related to specific inductive bias of the next-token prediction objective itself.

A glimmer of hope: Case study in Bernoulli models. To see why large cross-entropy may not be a barrier to coverage, consider perhaps the simplest setting, Bernoulli models, where X = {⊥}, Y = {0, 1}, Π = {Ber(p)}p∈(0,1/2), and πD = Ber(p⋆) for some small p⋆∈(0, 1/2).

The maximum likelihood model is bπ = Ber(bp), where bp is the empirical frequency of y = 1 in the dataset. We observe that with positive probability (and constant probability if n ≤1/p⋆), the dataset D will only contain examples where y = 0, so that the maximum likelihood model is bπ = Ber(0). This implies that expected KL divergence is infinite: E[DKL(πD ∥bπ)] = +∞. However, the coverage profile turns out to be well-behaved; to see this, we consider two cases:

1. If n ≳log(δ−1)/p⋆, a Binomial tail bound implies that bp ≥p⋆

2 with probability at least 1−δ, so Cov2(πD ∥bπ) = 0.

2. If n ≲log(δ−1)/p⋆, we can bound CovN(πD ∥bπ) ≤p⋆≲log(δ−1) n by simply writing off the missing mass.

Combining these cases, we see that CovN(πD ∥bπ) ≲log(δ−1)

n with probability at least 1−δ for all N ≥2; this gives hope that even though cross-entropy itself is infinite, maximum likelihood may actually learn a model with good coverage in the background. In what follows, we will show that this is not a fluke, but a general phenomenon.

Remark 3.1 (Missing mass). The underlying issue in both of the preceding examples is missing mass: there are responses that even a well-generalizing learner will fail to cover, and for these we may incur a large contribution to the KL-divergence. More generally, KL-divergence and cross-entropy are susceptible to contributions of the scale log Wmax where Wmax = maxπ∈Π πD π

∞(which could be as large as H, as in Proposition 3.2) when the model does not have enough information to generalize/extrapolate. This phenomenon is particularly pronounced when the prompt distribution is heterogeneous.

## 4 Next-Token Prediction Implicitly Optimizes Coverage

We now present our main result (Theorem 4.1): due to the unique structure of the logarithmic loss, maximum likelihood can learn models with a good coverage profile even when the cross-entropy is vacuously large. Henceforth, we abbreviate CovN(π):= CovN(πD ∥π). We make use of the following covering number.

Definition 4.1. For a class Π and α ≥0, we let N∞(Π, α) denote the size of the smallest cover Π′ ⊂ {X →∆(Y)} such that for all π ∈Π, there exists π′ ∈Π′ such that supx∈X,y∈Y|log π(y | x) −log π′(y | x)| ≤α.

Theorem 4.1 (Fast generalization for coverage). Fix N ≥8 and let c > 0 be an absolute constant. Suppose Assumption 2.1 holds. With probability at least 1−δ, the maximum likelihood estimator bπ:= arg maxπ∈Π bLn(π) has

CovN(bπ) ≲ 1 log N · inf ε>0 log N∞(Π, ε)

n + ε

| {z } =: Cfine(Π,n)

+ log N∞(Π, c log N) + log(δ−1)

n | {z } =: Ccoarse(Π,N,n)

. (7)

<!-- Page 7 -->

Eq. (7) has a fine-grained term Cfine(Π, n) and coarse-grained term Ccoarse(Π, N, n); we interpret each below.

Fine-grained term. Cfine(Π, n) evaluates the covering number N∞(Π, ε) at a small scale ε (typically ε ≈poly(1/n)), which matches typical bounds for conditional density estimation (e.g., Bilodeau et al. (2023)) in KL divergence; however, unlike KL-based bounds this term has no explicit dependence on sequence length H or density ratios log Wmax. The term is further scaled by 1/ log N, which implies that coverage enjoys faster convergence as we move further into the tail by increasing N; this reflects the unique structure of the logarithmic loss, and may be viewed as a new form of implicit bias.

Summarizing, the fine-grained term in Eq. (7) witnesses the phenomenon we term the coverage principle: the coverage profile enjoys faster generalization than cross-entropy; roughly, the rate is what we would expect (via Proposition 3.1) if we could somehow control KL without paying for the sequence length H or density ratio log Wmax. See Appendix B for a detailed comparison to standard (asymptotic and non-asymptotic) generalization bounds for maximum likelihood based on Hellinger distance and KL-divergence.

Coarse-grained term. The coarse-grained term Ccoarse(Π, N, n) captures the missing mass phenomenon exemplified by the Bernoulli example in the prequel. This term is not explicitly normalized by 1/ log N (compared to the fine-grained term), but depends on the covering number N∞(Π, α) only at a very large scale α ≈log N. As such, the dependence on the complexity/richness of Π in this term vanishes as we increase N.

Overall, while the guarantee in Eq. (7) might look surprising at first glance (particularly the coarse term, as we are not aware of any existing generalization bounds with dependence on covering numbers at such a large scale), we show in Proposition 4.1 (Appendix H) that both terms are tight in general.

Coverage can converge under severe misspecification. In Theorem 4.1, we assume realizability, i.e., the data distribution πD lies within the model class Π (Assumption 2.1). In the general misspecified setting where πD /∈Π, the coverage may instead scale with the approximation error minπ∈Π DKL(πD ∥π) (Proposition E.1), which is undesirable. Nevertheless, we show that when Π is convex, the MLE in fact enjoys a better coverage bound that depends only on the coverage profile of the best-in-class approximation to πD (Appendix E.1). Further, in Section 6.3, we propose tournament-style estimators with coverage guarantees scaling as minπ∈Π CovN(π) for any (possibly misspecified, non-convex) class Π.

## 4.1 Examples

To build intuition, we analyze the behavior of Theorem 4.1 under a general growth assumption on the covering number, then specialize to autoregressive linear models, showing how they exemplify the coverage principle.

Corollary 4.1. (i) Parametric regime: Suppose that there are parameters d ≥2 and C ≥2 such that log N∞(Π, α) ≤d log(C/α) for α ∈(0, C/2]. Then for any N ≥8, with probability at least 1 −δ,

CovN(bπ) ≲ d h

[log(C/ log N)]+ + log(Cn)

log N i

+ log(1/δ)

n.

(ii) Nonparametric regime: Suppose that there are parameters C ≥2 and p > 0 such that log N∞(Π, α) ≤ (C/α)p for α ∈(0, C/2]. Then for any N ≥8 and n ≥log1/p N · (C/ log N)p, with probability at least 1 −δ,

CovN(bπ) ≲ 1 log N

Cp n

1 p+1

+ log(1/δ)

n.

This result shows that for sufficiently rich classes (e.g., when p > 0), the fine-grained term dominates the coarse-grained term for n sufficently large. On the other hand, for simple classes (e.g., when p = 0), the coarse-grained term can dominate the fine-grained term.

Autoregressive linear models: Low dimension. We now consider the autoregressive linear model in Eq. (3). When the dimension d is small, this class satisfies log N∞(Π, α) ≍d log(BH/α) (corresponding to the parametric regime in Corollary 4.1), which gives the following coverage upper bound for next-token prediction.

<!-- Page 8 -->

Corollary 4.2. Consider the autoregressive linear model in Eq. (3). For any N ≥8, it holds that with probability at least 1 −δ, next-token prediction achieves

CovN(bπ) ≲ d h

[log(BH/ log N)]+ + log(BHn)

log N i

+ log(1/δ)

n.

Thus—in line with the coverage principle—coverage generalizes in a (nearly) horizon-independent fashion for autoregressive linear models, in stark contrast to the cross-entropy lower bound in Proposition 3.2. The only drawback (which is fundamental) is that since the class has low capacity, the coarse-grained term dominates for most parameter regimes, and the improvement as N scales is quite modest.

Autoregressive linear models: High dimension. As a more interesting example, we next look at the behavior of next-token prediction for autoregressive linear models in an “overparameterized” regime where the dimension d is arbitrarily large (Zhang, 2002; Neyshabur et al., 2015; Bartlett et al., 2017). Here, we control the richness of the class Π by the norm parameter B. In this regime, it turns out that in the worst-case, the capacity log N∞(Π, α) scales polynomially in H. To address, this we prove a refined version of Theorem 4.1 that adapts to the variance in the data distribution πD, avoiding explicit dependence on sequence length.

Define the inherent variance for the data distribution as σ2

⋆:= EπD

" H X h=1 ϕ(x, y1:h) −ϕπD(x, y1:h−1)

2

#

, (8)

where ϕπD(x, y1:h−1):= Eyh∼πD(·|x,y1:h−1)[ϕ(x, y1:h)] is the average feature vector given the prefix (x, y1:h−1). We can interpret the inherent variance σ2

⋆as a notion of effective sequence length; it captures the number tokens that are “pivotal” in the sense that they have high variation conditioned on the prefix; the name reflects a noted phenomenon in language modeling that most tokens are near-deterministic and easy to predict given their prefix, with only a few having high entropy (Abdin et al., 2024). Thus, while σ2

⋆can be as large as B2H in the worst case, we expect it to be smaller in general.

Theorem 4.2 (Overparameterized autoregressive linear models). Consider the autoregressive linear model (3), and suppose Assumptions 2.1 and 2.2 hold. For any N ≥2, next-token prediction achieves

E[CovN(bπ)] ≲ s σ2⋆ n · log N + B2 n. (9)

Similar to Theorem 4.1, the first term in Eq. (9) can be viewed as “fine-grained” and the second term as “coarse-grained”; the former is typically larger, but decreases with the tail parameter N, while the latter does not decrease with N but is typically smaller to begin with. We prove (details in Proposition I.1) that this result is tight in the sense that if σ2

⋆≍H, n ≥H is indeed necessary to achieve good non-trivial coverage in the overparameterized regime.

We mention in passing that we view the introduction of the inherent variance σ2

⋆as an instance-dependent notion of complexity for autoregressive models to be a non-trivial conceptual contribution, which may find broader use.

## 4.2 Proof Sketch

The basic idea behind the proof of Theorem 4.1 is to interpret the condition CovN(π) ≥ε as an small-ball like anti-concentration condition in the vein of Mendelson (2014, 2017). That is, for models π ∈Π where coverage is large, the condition CovN(π) ≥ε witnesses a one-sided tail bound which implies that the empirical likelihood of π is not too large with high probability, and hence π cannot be a maximum-likelihood solution.

Let c ∈(0, 1/2) be the absolute constant in Theorem 4.1, and let C ≥log 4 be another absolute constant. Fix N such that log N ≥4C. For each model π ∈Π, let SN(π):= 1 n| i ∈[n] | πD(yi|xi)

π(yi|xi) ≥N 1−2c

| denote the

<!-- Page 9 -->

empirical probability that π fails to cover πD. Our first step is to show via covering and concentration that with high-probability, all π ∈Π satisfy

SN(π) ≥1

2CovN(π) −Ccoarse(Π, N, n). (10)

That is, a large coverage profile implies that the number of points in the data where π fails to cover πD is large. This argument only depends on the covering number at a coarse log N scale—leading to the coarse-grained term in Theorem 4.1—because we only need to show that coverage concentrates, not the log-loss itself.5

We now argue that models with large coverage profile must have low log-likelihood compared to πD. In particular, using Eq. (10), we have bLn(π) −bLn(πD) = − n X i=1 log πD(yi | xi)

π(yi | xi) −C

+

+ n X i=1 log π(yi | xi)

πD(yi | xi) ∨(−C)

(⋆)

≤−|SN(π)|((1 −2c) log N −C) + n X i=1 log π(yi | xi)

πD(yi | xi) ∨(−C)

≤−n

4 log N · CovN(π) + Ccoarse(Π, N, n) · O(n log N) + n X i=1 log π(yi | xi)

πD(yi | xi) ∨(−C), (11)

as long as c ≤1/8 and log N ≥4C. We view step (⋆) as using a form of implicit bias in the logarithmic loss: If an example (xi, yi) has πD(yi|xi)/π(yi|xi) ≥N (i.e., π fails to cover πD on this example), this witnesses a negative contribution of order log N to the difference bLn(π) −bLn(πD).

Next, using a variation of a standard one-sided tail bound for the logarithmic loss (van de Geer, 2000; Zhang, 2006),6 we show that with high probability, all π ∈Π satisfy n X i=1 log π(yi | xi)

πD(yi | xi) ∨(−C) ≲Cfine(Π, n) · n, (12)

as long as C ≥log 4. Combining Eq. (11) and Eq. (12), we conclude that all π ∈Π have

CovN(π) ≲ bLn(πD) −bLn(π) + Cfine(Π, n) · n n log N + Ccoarse(Π, N, n). (13)

Since the maximum likelihood estimator bπ has bLn(πD) −bLn(bπ) ≤0, the result follows.

To summarize the key ideas as they relate to the final guarantee in Theorem 4.1: The coarse-grained term Ccoarse(Π, N, n) enters because we only need to show that the coverage profile concentrates, not the log loss itself. The fine-grained term Cfine(Π, n) enters concentration of the empirical likelihood, with the 1/ log N scaling arising from implicit bias. The reason this argument avoids dependence on the sequence length H or other spurious parameters that would otherwise affect cross-entropy is that the argument is fundamentally one-sided: the conclusion Eq. (13) only shows that models with large coverage profile have low log-likelihood compared to πD.

Discussion. We emphasize that while covering numbers are a fundamental and widely used notion of capacity in statistical learning and estimation (van de Geer, 2000; Zhang, 2002; Rakhlin and Sridharan, 2012; Shalev-Shwartz and Ben-David, 2014; Bilodeau et al., 2023), they are conservative from a modern generalization perspective. Nonetheless, Theorem 4.1 shows that they are sufficient to capture rich aspects of generalization for coverage, and we expect that our core analysis techniques can be combined with contemporary advances in generalization theory for overparameterized models (Belkin et al., 2019; Bartlett et al., 2020).

We believe there are many exciting avenues for refined results that build on the basic techniques here. For example, in Theorem E.1 (Appendix E.1), we show that for convex model classes, the coverage profile for maximum likelihood converges at a 1/poly(N) rate instead of the 1/ log N rate in Theorem 4.1.

5The set SN(π) is defined with the threshold as N1−2c rather than N to account for approximation errors incurred by covering. 6That the bound is one-sided is critical, as this allows us to avoid paying for the range of the density ratios under consideration. For details, see Proposition H.1.

<!-- Page 10 -->

## 4.3 Tightness of

Theorem 4.1

To conclude, we show that the coarse and fine-grained terms in Theorem 4.1 are both tight in general.

Proposition 4.1. The following lower bounds on coverage hold for the maximum likelihood estimator.

(a) Coarse rate: For any n ≥d ≥2 and B ≥log(5n), there exists a class Π with log N∞(Π, α) ≲d log(B/α)∨1 and πD ∈Π such that with probability at least 0.5, it holds that for any N ≤eB,

CovN(bπ) ≥c · d n.

(b) Fine rate: For any d ≥1, n ≥2d, N ≥2, there exists a class Π and πD ∈Π such that |Π| = 2d + 1 and

N∞(Π, α) ≤2 for any α ≥ q d n, and with probability at least 0.1, it holds that

CovN(bπ) ≥c · d n · log N.

Informally, case (a) shows that for the class Π under consideration, the coverage does not decrease with log N until N is trivially large such that log N∞(Π, log N) = 0; this is precisely the behavior of the coarse term in Theorem 4.1, so this implies there is no hope of removing this term. Meanwhile, case (b) can be interpreted as showing that there is no hope of replacing the high-precision covering number found in the fine-grained term in Theorem 4.1 with a coarser notion (e.g, at the scale in the coarse-grained term), since the rate grows with d ≈log|Π| even though log N(Π, α) is constant for α ≥ q d n. We note that Proposition 4.1 is an algorithm-specific lower bound, not an information-theoretic lower bound; we show in Section 6.3 that it is possible to improve over Theorem 4.1 with algorithms explicitly designed to optimize for coverage.

## 5 Stochastic Gradient Descent Through the Lens of Coverage

The coverage-based generalization guarantees for next-token prediction in the prequel apply to general model classes Π, but consider the empirical maximizer bπ = arg maxπ∈Π bLn(π) of the next-token prediction (maximum likelihood) objective, in the vein of classical techniques in learning theory. For our second set of main results, we focus on autoregressive linear models (3) but take a more realistic approach and analyze stochastic gradient descent (SGD) on the next-token prediction objective, in the single-pass regime. This setup is motivated by contemporary (“compute-optimal”) language model training, which typically uses one or fewer passes over the training corpus (Kaplan et al., 2020; Hoffmann et al., 2022).

## 5.1 Stochastic Gradient Descent has Suboptimal Coverage

For the next-token prediction objective, single-pass stochastic gradient descent (SGD) takes the form7 θ t+1 ←ProjΘ(θ t + η∇log πθt(y t | x t)), (14)

for xt ∼µ and yt ∼πD(· | xt), where η > 0 is the learning rate. As the next-token prediction loss L(θ):= EπD[−log πθ(y | x)] is convex under the parameterization (3), we can show that SGD converges to πD in KL divergence. This implies a coverage bound, albeit a suboptimal one.

Proposition 5.1 (SGD for autoregressive linear models). Upper bound: Suppose Assumptions 2.1 and 2.2 hold. As long as η ≤ 1 2HB2, it holds that E 1

T

PT t=1 DKL(πD ∥πθt)

≤ 4 ηT + 2ησ2

⋆. Choosing η to minimize this bound gives

E

"

1 T

T X t=1

CovN(πθt)

#

≲ 1 log N · r σ2⋆

T + B2H

T

!

. (15)

7ProjΘ(·) denotes Euclidean projection onto Θ, so this is the SGD update on the loss L(θ):= E[−log πθ(y | x)].

<!-- Page 11 -->

Lower bound: Suppose that B ≥c · log2(TH). Then there exists an autoregressive linear class Π such that for any constant step size η > 0, there exists an instance πD ∈Π with σ⋆≤1 such that with probability at least 0.5, the SGD iterates satisfy

CovN(πD ∥πθt) ≥c · min

H T log N, 1

, ∀t ∈[T]. (16)

The coverage bound in Eq. (15) (which follows by passing from KL to coverage through Proposition 3.1) is similar to Theorem 4.2, except that the second term B2H

T has an unfortunate dependence on the sequence length H. The lower bound in Eq. (16) shows that this dependence is tight, and SGD can indeed experience poor coverage. This failure of SGD is related to heterogeneity across prompts: there are some prompts for which the effective scale of the gradient in Eq. (14) grows with H, leading to divergence unless we use a small learning rate η ≲ 1 HB. Yet for other prompts, the effective gradient range is small, leading to slow convergence (on the order of Ω(H) steps) unless η ≫ 1 HB.

Remark 5.1 (Sequence-level SGD). The update in Eq. (14) can be interpreted as a “sequence-level” form of SGD, since we perform a single gradient step for each full sequence yt (note that ∇log πθt(yt | xt) = PH h=1 ∇log πθt(yt h | xt, yt

1:h−1)). We view this as a model for what is done in practice, whereby one performs SGD on sequences of tokens spanning some fixed context window. While this context window may be shorter than the full training example (e.g., a long article), understanding the implications of a limited context window is beyond the scope of this work.

## 5.2 Gradient Normalization Improves Coverage

To address the suboptimality of SGD, we consider gradient normalization as a simple intervention. For a mini-batch D = {(xi, yi)}K i=1 of K samples from πD, define the batch stochastic gradient as bg(θ; D) = 1 |D|

X

(x,y)∈D

∇log πθ(y | x). (17)

We consider the following normalized SGD update:

θ t+1 ←ProjΘ θ t + η · bg(θt; Dt) λ + ∥bg(θt; Dt)∥

; (18)

here Dt is a mini-batch with K fresh samples drawn i.i.d. from πD, and λ > 0 is a regularization parameter for numerical stability. We show that this update achieves a horizon-independent coverage bound.

Theorem 5.1. Suppose Assumption 2.1 and Assumption 2.2 hold. Let T, K ≥1, N ≥3 be given. For an appropriate choice of η, λ > 0, the normalized SGD update (18) achieves the following coverage bound:

E

"

1 T

T X t=1

CovN(πθt)

#

≲ s σ2⋆ T · log N + B2

T + B K · log N. (19)

To achieve E[CovN(bπ)] ≤ε for a target level ε > 0, it suffices to choose T = O σ2

⋆ ε2 log N + B2 ε

, K = O

B ε log N +1

, giving total sample complexity n = TK = O σ2

⋆B ε3 log2 N + B3+σ2

⋆ ε2 log N + B2 ε

.

Theorem 5.1 shows that gradient normalization achieves horizon-independent coverage with a qualitatively similar rate to the guarantee for next-token prediction in Theorem 4.2: To achieve coverage ε, both rates scale as poly σ2

⋆ log N, B, ε−1

, though the dependence on ε for Theorem 5.1 is worse. We emphasize that minibatching alone is not enough to achieve this result; rather, minibatching is necessary to avoid excessive bias once we introduce gradient normalization.

Somewhat speculatively, we believe that it may be possible to use similar techniques to Theorem 5.1 to show that Adam (Kingma and Ba, 2015) and relatives enjoy improved coverage relative to SGD. Adam is believed

<!-- Page 12 -->

to behave similarly to the SignSGD update (Balles and Hennig, 2018; Bernstein et al., 2018; Bernstein and Newhouse, 2024), which takes the form θ t+1 ←θ t + η · sign bg(θ t; D t)

. (20)

In fact, Adam reduces to Eq. (20) when EMA and bias correction are disabled. This is very similar form of gradient normalization to Eq. (18), except that it normalizes per-coordinate rather than globally; this distinction is important for deep learning models, where different modules or layers can have very different scales, but we expect that it grants similar benefits with respect to sequence length.

## 6 Interventions for Better Coverage

In this section, we develop new interventions that improve coverage (and downstream performance) beyond the conventional algorithms analyzed in Sections 4 and 5. We view these results as promising proofs of concept for further research into interventions driven by coverage.

## 6.1 Improving Coverage at Test Time

In this section, we show that a modified decoding strategy based on test-time training (or, dynamic evaluation) (Mikolov et al., 2010; Krause et al., 2018, 2019; Sun et al., 2024; Akyürek et al., 2025) leads to improved coverage when combined with token-level SGD.

We focus on autoregressive linear models, but depart from Eq. (14) by learning models with a token-level SGD update, defined as θ t,h+1 = ProjΘ θ t,h + η∇log πθt,h(y t h | x t, y t 1:h−1)

, for h = 0, · · ·, H −1, (21)

and θt+1 ≡θt+1,0:= θt,H for t ∈[T], and where (xt, yt

1:H) ∼πD. We will show that—when combined with a test-time training-like update that performs token-level gradient updates during test time—the updates in Eq. (21) can circumvent the H-dependence in the lower bound of Proposition 5.1.

Concretely, for a parameter θ and prompt x, define the following test-time parameter update recursively for h = 0, 1, · · ·, H −1:

ϑTTT(x, y1:h; θ):= ProjΘ ϑTTT(x, y1:h−1; θ) + η∇log πϑTTT(x,y1:h−1;θ)(yh | x, y1:h−1)

. (22)

We then define a distribution πTTT θ: X →∆(YH) as πTTT θ (· | x, y1:h−1):= πϑTTT(x,y1:h−1;θ)(· | x, y1:h−1). (23)

The distribution πTTT θ can be interpreted as an augmented version of the autoregressive linear model πθ that performs test-time training during generation: Given a prompt x, we first sample y1 ∼πθ(· | x), then perform a gradient step θ′ ←ProjΘ(θ + η∇log πθ(y1 | x)) to increase the probability of the token we just sampled. We then sample y2 ∼πθ′(· | x, y1), update θ′′ ←ProjΘ(θ′ + η∇log πθ′(y2 | x, y1)), and so on. Once the full sequence y1:H is sampled, we reset back to θ (so that we can process the next test-time example). This bears similarity to many test-time training methods in the literature, and specifically coincides with the method used in Krause et al. (2019); Rannen-Triki et al. (2024). We show that when augmented with this test-time sampling scheme, token-level SGD achieves a horizon-independent coverage bound that matches and even slightly improves upon the bound for next-token prediction in Theorem 4.2.

Theorem 6.1 (Token-level SGD with test-time training). Suppose Assumption 2.1 and Assumption 2.2 hold.

For a suitably chosen parameter η > 0, token-level SGD (21) achieves E

1

T

PT t=1 DKL(πD ∥πTTT θt)

≲ q σ2⋆

T + B2

T, and thus

E

"

1 T

T X t=1

CovN(πTTT θt)

#

≲ 1 log N · r σ2⋆

T + B2

T

!

.

This improves Theorem 4.2 by a factor of 1/√log N on the leading term and a factor of 1/ log N on the second term. Furthermore, the algorithm bypasses the lower bound on KL divergence for proper methods in Proposition 3.2, demonstrating a provable benefit of being improper.

<!-- Page 13 -->

## 6.2 SGD: Improved Gradient Normalization for Distillation

We next consider a variant of our setting inspired by distillation (Hinton et al., 2015; Kim and Rush, 2016). We assume that for each example (xi, yi

1:H), for each h = 1,..., H, we have access to the true next-token probabilities πD(yh | xi, yi

1:h−1) for all yh ∈V. This is natural for distillation, where πD corresponds to a teacher model (in particular, the next-token probabilities are already computed as part of a standard forward pass through the teacher model). For the distillation setting, we give an improved gradient normalization scheme that improves upon the rate achieved by Theorem 5.1, closing the gap between SGD and maximum likelihood by matching the guarantee for Theorem 4.2.

Define ϵθ(x, y1:h−1):= DKL(πD(· | x, y1:h−1) ∥πθ(· | x, y1:h−1)); note that for the distillation setting, we can compute this quantity in closed form for any prefix x, y1:h−1 in the training corpus. We consider the following truncated stochastic gradient estimator, defined for a single sample as follows:

bgθ(y | x) =

H X h=1 αθ(x, y1:h−1)∇log πθ(yh | x, y1:h−1), (24)

where for A:= log N, we define αθ(x, y1:h−1) =

  

 

1, P j≤h−1 ϵθ(x, y1:j) ≤A, 0, P j<h−1 ϵθ(x, y1:j) > A, A−P j<h−1 ϵθ(x,y1:j) ϵθ(x,y1:h−1), otherwise.

(25)

We use the following SGD update based on this estimator:

θ t+1 = ProjΘ(θ t + ηbgθt(y t | x t)). (26)

The idea behind the update in Eq. (24) is to truncate the token-level gradients at a point where the sum of token-level KL divergences between the teacher and student model becomes too large, ensuring the sum stays normalized; this is inspired by the structural result Proposition D.10 in Appendix D.4, where we show a close connection between the coverage profile and a certain “stopped” variant of KL divergence.

Theorem 6.2. Let T, N ≥2 be given. With a suitably chosen stepsize η > 0, the truncated SGD update (26) achieves the following coverage bound:

E

"

1 T

T X t=1

CovN(πθt)

#

≲ s σ2⋆ T log N + B2

T. (27)

This guarantee matches the rate of Theorem 4.2 for the maximum likelihood estimator. The proof is presented in Appendix I.7.

## 6.3 Selecting for Coverage

We last consider the problem of selecting a model (e.g., checkpoint) from a small number of candidates to achieve the best coverage. We introduce two tournament-like procedures that improve upon maximum likelihood in two ways: (1) they attain a better coverage profile; and (2) they remove the requirement that πD ∈Π (i.e., they are guaranteed to find a model in the class with good coverage if one exists, even if πD itself is not in the class). As an algorithmic intervention, we envision using these procedures to select a single training checkpoint or hyperparameter configuration to use for RL fine-tuning or test-time scaling. Indeed, as demonstrated in Figure 1, using cross-entropy as a selection criterion—as is standard—may result in poor coverage, while these procedures can select better checkpoints. Our results here concern the general setting in Section 2, and are not restricted to autoregressive linear models.

While their main motivation is model/checkpoint selection with a finite class Π, both estimators can also be applied to general, infinite classes Π. In this case, they improve upon the coverage achieved by the maximum likelihood estimator in Theorem 4.1, even in the well-specified case where πD ∈Π; informally, the tournament estimators allow us to remove the fine-grained term in Theorem 4.1, leaving only a coarse-grained term.

<!-- Page 14 -->

A simple tournament for maximizing coverage. To describe the first tournament, given a dataset D = {(xi, yi)}i∈[n], define d CovN(π′ ∥π):= 1 n i ∈[n]: π′(yi | xi)

π(yi | xi) ≥N

, (28)

which can be interpreted as an empirical version of the coverage profile CovN(π′ ∥π) in Eq. (1) when π′ = πD (see Lemma H.2). For N ≥1, we consider the estimator bπ:= arg min π∈Π max π′∈Π d CovN(π′ ∥π). (29)

Informally, this estimator chooses the model π that minimizes the maximum coverage against any other model π′ in the class Π. When Π is small, we can implement this tournament by simply evaluating the empirical coverage in Eq. (28) for each pair. The main guarantee for this estimator is as follows.

Theorem 6.3. Let N ≥1 be given. Then, for any a ∈[0, 1], with probability at least 1 −δ, the tournament estimator (29) achieves

CovN1+a(bπ) ≲min π∈Π CovNa(π) + 1 N 1−a + log(|Π|/δ)

n. (30)

More generally, for any parameter c ≥0, with probability at least 1 −δ, it holds that

CovN1+a+2c(bπ) ≲min π∈Π CovNa(π) + 1 N 1−a−2c + log N∞(Π, c log N) + log δ−1 n. (31)

This shows that the tournament achieves a coverage profile nearly as good as the best-in-class, except for a small polynomial blow up, in that we bound the coverage at level N 1+a in terms of the coverage for the best-in-class at level N a. The additive 1/N 1−a term is due to the fact that some of the models we need to cover in the tournament could potentially be quite far from πD.

An improved tournament via on-policy generation. We next describe an improved tournament estimator that is able to remove that 1/N 1−a term from Theorem 6.3, meaning it achieves nontrivial guarantees even when the coverage parameter N is constant. Specifically, we augment the simple tournament estimator in Eq. (29) with an offset term:

bπ:= arg min π∈Π max π′∈Π {d CovN(π′ ∥π) −2N a · d Covπ

N(π′ ∥π)}, (32)

where we define d Covπ

N(π′ ∥π):= 1 n

Pn i=1 Py∼π(·|xi)

π′(y|xi)

π(y|xi) ≥N for models π, π′, π. The offset term is a penalty which accounts for the fact that some of the models in Π might be quite far from πD and hence hard to cover (this is the root cause of the 1/N 1−a term in Theorem 6.3). This algorithm is more complex to implement compared to Theorem 6.3 because we need to estimate the coverage profile d Covπ

N(π′ ∥π) for models π, π′ that we are choosing between. In practice, d Covπ

N(π′ ∥π) can be approximated by sampling a collection of generations from each π. The main guarantee is as follows.

Theorem 6.4. Fix N ≥1, a > 0 such that N 1−2a ≥8. Suppose that there exists π ∈Π such that |log πD(y | x) −log π(y | x)| ≤a log N for any x ∈X, y ∈Y. Then with probability 1 −δ, the tournament estimator (32) achieves

Cov2N1+a(bπ) ≲log(|Π|/δ)

n. (33)

More generally, for infinite classes Π, we can suitably instantiate the estimator on a covering of Π, so that with probability 1 −δ, the estimator achieves

Cov2N1+2a(bπ) ≲log N∞(Π, a log N) + log δ−1 n. (34)

Compared to Theorem 6.3, this tournament eliminates the additive 1/N 1−a term. It does, however, require a stronger condition on the best-in-class model π that |log πD(y | x) −log π(y | x)| ≤a log N, which implies in particular that CovNa(π) = 0.

<!-- Page 15 -->

## 7 Discussion and Future Work

Our work, through the lens of coverage, takes a first step toward clarifying the mechanisms through which pre-training with next-token prediction leads to models for which post-training is effective.

## 7.1 Simplifications in the Problem Formulation

In the course of the paper we have made various simplifying assumptions. Some of these can be relaxed in a straightforward fashion, while others are more fundamental.

• In language model pre-training, the pre-training corpus consists of sequences y with varying lengths H, and does not typically split examples into prompts and responses. Our formulation in Section 2 is a simplification (one that is closer in spirit to supervised fine-tuning), but we expect that the insights derived here can extend to the general setting.

• Much of our analysis focuses on the realizable/well-specified setting where πD ∈Π. We give evidence in Appendix E that the coverage profile is more tolerant to misspecification than KL-divergence, but we leave a deeper investigation for future work.

• Our treatment assumes the distribution over prompts µ is the same for pre-training and post-training. This is straightforward to relax at the cost of introducing an additional coverage or distribution shift coefficient to handle the mismatch between the two distributions.

• We show that a good coverage profile is necessary for BoN to succeed on downstream tasks. While there is ample evidence current RL techniques can fail in the absence of coverage (Yue et al., 2025; Gandhi et al., 2025; Wu et al., 2025), it is not clear what the minimal conditions required for RL are.

• Our results focus on coverage at the sequence level. For reasoning tasks, it is natural to explicitly factorize the response y = (ycot, yans) into a chain-of-thought (reasoning trajectory) component ycot and an answer component yans. For this setting, a weaker notion coverage is the following answer-level coverage profile: Covans

N (πD ∥bπ):= PπD h πD(yans|x)

bπ(yans|x) ≥N i

. The answer-level coverage profile is sufficient for downstream BoN success for tasks where it is only important to produce the right answer, not a correct reasoning trace. We have Covans

N (πD ∥bπ) ≤CovN(πD ∥bπ), but the former can be strictly smaller in general.

## 7.2 Future Work

Our results open several new directions for future research.

Interventions for coverage. There is much to be done in understanding and improving existing algorithms such as optimizers through the lens of coverage. Our results in Section 6 show initial promise for using coverage to guide design of optimizers and model selection schemes, but the algorithm design space remains opaque, and there may be significant room for futher improvement. More ambitiously, one could imagine re-structuring the entire language modeling pipeline itself around coverage.

Semantic coverage. The notion of coverage we focus on, the coverage profile, is mathematically convenient but may be conservative in regard to downstream performance, since it only depends on the model through its predicted probabilities. An important direction for future work is to understand pre-training and post-training through fine-grained “semantic” notions of coverage that more explicitly account for the representations learned by next-token prediction.

## Acknowledgements

We thank Clayton Sanford, Matus Telgarsky, and Nati Srebro for helpful discussions. FC acknowledges support from ARO through award W911NF-21-1-0328, Simons Foundation and the NSF through awards DMS-2031883 and PHY-2019786, and DARPA AIQ award.

<!-- Page 16 -->

## References

Marah Abdin, Jyoti Aneja, Harkirat Behl, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, Michael

Harrison, Russell J Hewett, Mojan Javaheripi, Piero Kauffmann, et al. Phi-4 technical report. arXiv preprint arXiv:2412.08905, 2024.

Ekin Akyürek, Mehul Damani, Adam Zweiger, Linlu Qiu, Han Guo, Jyothish Pari, Yoon Kim, and Jacob

Andreas. The surprising effectiveness of test-time training for few-shot learning. In Forty-second International Conference on Machine Learning, 2025.

Zeyuan Allen-Zhu and Yuanzhi Li. Physics of language models: Part 3.3, knowledge capacity scaling laws.

In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview. net/forum?id=FxNNiUgtfa.

Gregor Bachmann and Vaishnavh Nagarajan. The pitfalls of next-token prediction. arXiv preprint arXiv:2403.06963, 2024.

Lukas Balles and Philipp Hennig. Dissecting adam: The sign, magnitude and variance of stochastic gradients.

In International Conference on Machine Learning, pages 404–413. PMLR, 2018.

Hritik Bansal, Arian Hosseini, Rishabh Agarwal, Vinh Q. Tran, and Mehran Kazemi. Smaller, weaker, yet better: Training LLM reasoners via compute-optimal sampling. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=3OyaXFQuDl.

Peter L. Bartlett and Andrea Montanari. Deep learning: A statistical viewpoint. Acta Numerica, 30:87–201,

2021.

Peter L. Bartlett, Dylan J. Foster, and Matus J. Telgarsky. Spectrally-normalized margin bounds for neural networks. In Advances in Neural Information Processing Systems, 2017.

Peter L. Bartlett, Philip M. Long, Gábor Lugosi, and Alexander Tsigler. Benign overfitting in linear regression.

Proceedings of the National Academy of Sciences (PNAS), 117(48):30063–30070, 2020.

Mikhail Belkin, Daniel Hsu, Siyuan Ma, and Soumik Mandal. Reconciling modern machine-learning practice and the classical bias–variance trade-off. Proceedings of the National Academy of Sciences (PNAS), 116(32): 15849–15854, 2019.

Jeremy Bernstein and Laker Newhouse. Old optimizer, new norm: An anthology. In OPT 2024: Optimization for Machine Learning, 2024.

Jeremy Bernstein, Yu-Xiang Wang, Kamyar Azizzadenesheli, and Animashree Anandkumar. signsgd: Com- pressed optimisation for non-convex problems. In International conference on machine learning, pages 560–569. PMLR, 2018.

Blair Bilodeau, Dylan J Foster, and Daniel M Roy. Minimax rates for conditional density estimation via empirical entropy. The Annals of Statistics, 2023.

Adam Block and Yury Polyanskiy. The sample complexity of approximate rejection sampling with applications to smoothed online learning. In The Thirty Sixth Annual Conference on Learning Theory, pages 228–273. PMLR, 2023.

Bradley Brown, Jordan Juravsky, Ryan Saul Ehrlich, Ronald Clark, Quoc V Le, Christopher Re, and Azalia

Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling, 2025. URL https://openreview.net/forum?id=0xUEBQV54B.

Fan Chen and Alexander Rakhlin. Decision making in changing environments: Robustness, query-based learning, and differential privacy. Conference on Learning Theory (COLT), 2025.

Fan Chen, Dylan J Foster, Yanjun Han, Jian Qian, Alexander Rakhlin, and Yunbei Xu. Assouad, fano, and le cam with interaction: A unifying lower bound framework and characterization for bandit learnability. Advances in Neural Information Processing Systems, 37:75585–75641, 2024a.

<!-- Page 17 -->

Feng Chen, Allan Raventos, Nan Cheng, Surya Ganguli, and Shaul Druckmann. Rethinking fine-tuning when scaling test-time compute: Limiting confidence improves mathematical reasoning. arXiv preprint arXiv:2502.07154, 2025.

Jinglin Chen and Nan Jiang. Information-theoretic considerations in batch reinforcement learning. In International conference on machine learning, pages 1042–1051. PMLR, 2019.

Yangyi Chen, Binxuan Huang, Yifan Gao, Zhengyang Wang, Jingfeng Yang, and Heng Ji. Scaling laws for predicting downstream performance in llms. Transactions on Machine Learning Research, 2024b.

Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang Tong, Saining Xie, Dale Schuurmans, Quoc V Le, Sergey

Levine, and Yi Ma. SFT memorizes, RL generalizes: A comparative study of foundation model post-training. In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/forum? id=dYur3yabMj.

Rick Durrett. Probability: theory and examples, volume 49. Cambridge university press, 2019.

Amir-massoud Farahmand, Csaba Szepesvári, and Rémi Munos. Error propagation for approximate policy and value iteration. Advances in Neural Information Processing Systems, 2010.

Bahare Fatemi, Jonathan Halcrow, and Bryan Perozzi. Talk like a graph: Encoding graphs for large language models. In The Twelfth International Conference on Learning Representations, 2024.

Marc Finzi, Sanyam Kapoor, Diego Granziol, Anming Gu, Christopher De Sa, J Zico Kolter, and Andrew Gordon

Wilson. Compute-optimal llms provably generalize better with scale. arXiv preprint arXiv:2504.15208, 2025.

Dylan J Foster and Alexander Rakhlin. Foundations of reinforcement learning and interactive decision making.

arXiv:2312.16730, 2023.

Dylan J Foster, Sham M Kakade, Jian Qian, and Alexander Rakhlin. The statistical complexity of interactive decision making. arXiv:2112.13487, 2021.

Dylan J Foster, Akshay Krishnamurthy, David Simchi-Levi, and Yunzong Xu. Offline reinforcement learning:

Fundamental barriers for value function approximation. In Conference on Learning Theory, pages 3489–3489. PMLR, 2022.

Dylan J Foster, Adam Block, and Dipendra Misra. Is behavior cloning all you need? understanding horizon in imitation learning. arXiv preprint arXiv:2407.15007, 2024.

Dylan J Foster, Zakaria Mhammedi, and Dhruv Rohatgi. Is a good foundation necessary for efficient reinforce- ment learning? the computational role of the base model in exploration. Conference on Learning Theory (COLT), 2025.

Samir Yitzhak Gadre, Georgios Smyrnis, Vaishaal Shankar, Suchin Gururangan, Mitchell Wortsman, Rulin Shao,

Jean Mercat, Alex Fang, Jeffrey Li, Sedrick Keh, et al. Language models scale reliably with over-training and on downstream tasks. In The Thirteenth International Conference on Learning Representations, 2024.

Samir Yitzhak Gadre, Georgios Smyrnis, Vaishaal Shankar, Suchin Gururangan, Mitchell Wortsman, Rulin

Shao, Jean Mercat, Alex Fang, Jeffrey Li, Sedrick Keh, Rui Xin, Marianna Nezhurina, Igor Vasiljevic, Luca Soldaini, Jenia Jitsev, Alex Dimakis, Gabriel Ilharco, Pang Wei Koh, Shuran Song, Thomas Kollar, Yair Carmon, Achal Dave, Reinhard Heckel, Niklas Muennighoff, and Ludwig Schmidt. Language models scale reliably with over-training and on downstream tasks. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=iZeQBqJamf.

Kanishk Gandhi, Ayush Chakravarthy, Anikait Singh, Nathan Lile, and Noah D Goodman. Cognitive behaviors that enable self-improving reasoners, or, four habits of highly effective stars. arXiv preprint arXiv:2503.01307, 2025.

Zhaolin Gao, Jonathan D Chang, Wenhao Zhan, Owen Oertell, Gokul Swamy, Kianté Brantley, Thorsten

Joachims, J Andrew Bagnell, Jason D Lee, and Wen Sun. REBEL: Reinforcement learning via regressing relative rewards. arXiv:2404.16767, 2024.

<!-- Page 18 -->

Behrooz Ghorbani, Orhan Firat, Markus Freitag, Ankur Bapna, Maxim Krikun, Xavier Garcia, Ciprian Chelba, and Colin Cherry. Scaling laws for neural machine translation. In International Conference on Learning Representations, 2022. URL https://openreview.net/forum?id=hR_SMu8cxCV.

Elad Hazan. Introduction to online convex optimization. Foundations and Trends® in Optimization, 2(3-4):

157–325, 2016.

Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. arXiv:1503.02531,

2015.

Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford,

Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. Training compute-optimal large language models. In Proceedings of the 36th International Conference on Neural Information Processing Systems, pages 30016–30030, 2022.

Audrey Huang, Adam Block, Dylan J Foster, Dhruv Rohatgi, Cyril Zhang, Max Simchowitz, Jordan T Ash, and

Akshay Krishnamurthy. Self-improvement in language models: The sharpening mechanism. International Conference on Learning Representations (ICLR), 2025a.

Audrey Huang, Adam Block, Qinghua Liu, Nan Jiang, Akshay Krishnamurthy, and Dylan J Foster. Is best-of-n the best of them? coverage, scaling, and optimality in inference-time alignment. International Conference on Machine Learning (ICML), 2025b.

Audrey Huang, Wenhao Zhan, Tengyang Xie, Jason D Lee, Wen Sun, Akshay Krishnamurthy, and Dylan J

Foster. Correcting the mythos of kl-regularization: Direct alignment without overoptimization via chi-squared preference optimization. In The Thirteenth International Conference on Learning Representations, 2025c.

Yuzhen Huang, Jinghan Zhang, Zifei Shan, and Junxian He. Compression represents intelligence linearly. In

First Conference on Language Modeling, 2024.

Arthur Jacot, Franck Gabriel, and Clément Hongler. Neural tangent kernel: Convergence and generalization in neural networks. In Advances in Neural Information Processing Systems (NeurIPS), 2018.

Xiang Ji, Sanjeev Kulkarni, Mengdi Wang, and Tengyang Xie. Self-play with adversarial critic: Provable and scalable offline alignment for language models. arXiv:2406.04274, 2024.

Nan Jiang and Tengyang Xie. Offline reinforcement learning in large state spaces: Algorithms and guarantees.

Statistical Science, 2024.

Hangzhan Jin, Sitao Luan, Sicheng Lyu, Guillaume Rabusseau, Reihaneh Rabbany, Doina Precup, and

Mohammad Hamdaqa. Rl fine-tuning heals ood forgetting in sft, 2025. URL https://arxiv.org/abs/2509. 12235.

Ying Jin, Zhuoran Yang, and Zhaoran Wang. Is pessimism provably efficient for offline rl? In International conference on machine learning, pages 5084–5096. PMLR, 2021.

Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray,

Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361, 2020.

Yoon Kim and Alexander M Rush. Sequence-level knowledge distillation. In Proceedings of the 2016 conference on empirical methods in natural language processing, pages 1317–1327, 2016.

Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. International Conference on

Learning Representations, 2015.

Ben Krause, Emmanuel Kahembwe, Iain Murray, and Steve Renals. Dynamic evaluation of neural sequence models. In International Conference on Machine Learning, pages 2766–2775. PMLR, 2018.

Ben Krause, Emmanuel Kahembwe, Iain Murray, and Steve Renals. Dynamic evaluation of transformer language models. arXiv preprint arXiv:1904.08378, 2019.

<!-- Page 19 -->

Hong Liu, Sang Michael Xie, Zhiyuan Li, and Tengyu Ma. Same Pre-training Loss, Better Downstream:

Implicit Bias Matters for Language Models, 2022.

Zhihan Liu, Miao Lu, Shenao Zhang, Boyi Liu, Hongyi Guo, Yingxiang Yang, Jose Blanchet, and Zhaoran

Wang. Provably mitigating overoptimization in RLHF: Your SFT loss is implicitly an adversarial regularizer. arXiv:2405.16436, 2024.

Sanae Lotfi, Marc Finzi, Yilun Kuang, Tim GJ Rudner, Micah Goldblum, and Andrew Gordon Wilson.

Non-vacuous generalization bounds for large language models. arXiv preprint arXiv:2312.17173, 2023.

Sanae Lotfi, Yilun Kuang, Marc Finzi, Brandon Amos, Micah Goldblum, and Andrew G Wilson. Unlocking tokens as data points for generalization bounds on larger language models. Advances in Neural Information Processing Systems, 37:9229–9256, 2024.

Nicholas Lourie, Michael Y Hu, and Kyunghyun Cho. Scaling laws are unreliable for downstream tasks: A reality check. arXiv preprint arXiv:2507.00885, 2025.

Xingyu Lu, Xiaonan Li, Qinyuan Cheng, Kai Ding, Xuanjing Huang, and Xipeng Qiu. Scaling laws for fact memorization of large language models. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Findings of the Association for Computational Linguistics: EMNLP 2024, pages 11263–11282, Miami, Florida,

USA, November 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.findings-emnlp.658. URL https://aclanthology.org/2024.findings-emnlp.658/.

Shahar Mendelson. Learning without Concentration. In Conference on Learning Theory, 2014.

Shahar Mendelson. Extending the scope of the small-ball method. arXiv preprint arXiv:1709.00843, 2017.

Tomas Mikolov, Martin Karafiát, Lukas Burget, Jan Cernock`y, and Sanjeev Khudanpur. Recurrent neural network based language model. In Interspeech, volume 2, pages 1045–1048. Makuhari, 2010.

Vaishnavh Nagarajan and J. Zico Kolter. Uniform convergence may be unable to explain generalization in deep learning. In Advances in Neural Information Processing Systems (NeurIPS), 2019.

Vaishnavh Nagarajan, Chen Henry Wu, Charles Ding, and Aditi Raghunathan. Roll the dice & look before you leap: Going beyond the creative limits of next-token prediction. In Forty-second International Conference on Machine Learning, 2025.

Behnam Neyshabur, Ryota Tomioka, and Nati Srebro. Norm-based capacity control in neural networks. In

Conference on Learning Theory (COLT), 2015.

OpenAI. Introducing openai o1. Blog, 2024. URL https://openai.com/o1/.

Yury Polyanskiy. Channel coding: Non-asymptotic fundamental limits. Princeton University, 2010.

Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.

Alexander Rakhlin and Karthik Sridharan. Statistical learning and sequential prediction, 2012. Available at http://www.mit.edu/~rakhlin/courses/stat928/stat928_notes.pdf.

Amal Rannen-Triki, Jorg Bornschein, Razvan Pascanu, Marcus Hutter, Andras György, Alexandre Galashov,

Yee Whye Teh, and Michalis K Titsias. Revisiting dynamic evaluation: Online adaptation for large language models. arXiv preprint arXiv:2403.01518, 2024.

Dhruv Rohatgi, Adam Block, Audrey Huang, Akshay Krishnamurthy, and Dylan J. Foster. Computational- statistical tradeoffs at the next-token prediction barrier: Autoregressive and imitation learning under misspecification. arXiv preprint arXiv:2502.12465, 2025.

Clayton Sanford, Bahare Fatemi, Ethan Hall, Anton Tsitsulin, Mehran Kazemi, Jonathan Halcrow, Bryan

Perozzi, and Vahab Mirrokni. Understanding transformer reasoning capabilities via graph algorithms. Advances in Neural Information Processing Systems, 37:78320–78370, 2024.

Abulhair Saparov, Srushti Ajay Pawar, Shreyas Pimpalgaonkar, Nitish Joshi, Richard Yuanzhe Pang, Vishakh

Padmakumar, Mehran Kazemi, Najoung Kim, and He He. Transformers struggle to learn to search. In The

<!-- Page 20 -->

Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025.

OpenReview.net, 2025.

Nikhil Sardana, Jacob Portes, Sasha Doubov, and Jonathan Frankle. Beyond chinchilla-optimal: Accounting for inference in language model scaling laws. In Forty-first International Conference on Machine Learning, 2024. URL https://openreview.net/forum?id=0bmXrtTDUu.

Shai Shalev-Shwartz and Shai Ben-David. Understanding machine learning: From theory to algorithms. Cambridge university press, 2014.

Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute optimally can be more effective than scaling parameters for reasoning. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=4FWAwZtd2n.

Yuda Song, Gokul Swamy, Aarti Singh, J Bagnell, and Wen Sun. The importance of online data: Understanding preference fine-tuning via coverage. Advances in Neural Information Processing Systems, 37:12243–12270, 2024.

Vladimir Spokoiny. Parametric estimation. finite sample theory. The Annals of Statistics, pages 2877–2909,

2012.

Jacob Mitchell Springer, Sachin Goyal, Kaiyue Wen, Tanishq Kumar, Xiang Yue, Sadhika Malladi, Graham

Neubig, and Aditi Raghunathan. Overtrained language models are harder to fine-tune. In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/forum?id=YW6edSufht.

Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei Chen,

Xiaolong Wang, Sanmi Koyejo, et al. Learning to (learn at test time): Rnns with expressive hidden states. arXiv preprint arXiv:2407.04620, 2024.

Jianheng Tang, Qifan Zhang, Yuhan Li, Nuo Chen, and Jia Li. Grapharena: Evaluating and exploring large language models on graph computation. In The Thirteenth International Conference on Learning Representations, 2025.

Alexander K Taylor, Anthony Cuturrufo, Vishal Yathish, Mingyu Derek Ma, and Wei Wang. Are large-language models graph algorithmic reasoners? arXiv preprint arXiv:2410.22597, 2024.

S. A. van de Geer. Empirical Processes in M-Estimation. Cambridge University Press, 2000.

Aad W Van der Vaart. Asymptotic statistics, volume 3. Cambridge University Press, 2000.

Martin J Wainwright. High-dimensional statistics: A non-asymptotic viewpoint, volume 48. Cambridge

University Press, 2019.

Heng Wang, Shangbin Feng, Tianxing He, Zhaoxuan Tan, Xiaochuang Han, and Yulia Tsvetkov. Can language models solve graph problems in natural language? Advances in Neural Information Processing Systems, 36: 30840–30861, 2023.

Xinyi Wang, Shawn Tan, Mingyu Jin, William Yang Wang, Rameswar Panda, and Yikang Shen. Do larger language models imply better generalization? a pretraining scaling law for implicit reasoning, 2025. URL https://arxiv.org/abs/2504.03635.

Wing Hung Wong and Xiaotong Shen. Probability inequalities for likelihood ratios and convergence rates of sieve mles. The Annals of Statistics, 1995.

Fang Wu, Weihao Xuan, Ximing Lu, Zaid Harchaoui, and Yejin Choi. The Invisible Leash: Why RLVR May

Not Escape Its Origin, 2025.

Mengzhou Xia, Mikel Artetxe, Chunting Zhou, Xi Victoria Lin, Ramakanth Pasunuru, Danqi Chen, Luke

Zettlemoyer, and Ves Stoyanov. Training trajectories of language models across scales. arXiv preprint arXiv:2212.09803, 2022.

Tengyang Xie and Nan Jiang. Q* approximation schemes for batch reinforcement learning: A theoretical comparison. In Conference on Uncertainty in Artificial Intelligence, 2020.

<!-- Page 21 -->

Yuhong Yang and Andrew R Barron. An asymptotic property of model selection criteria. IEEE Transactions on Information Theory, 44(1):95–116, 1998.

Gilad Yehudai, Noah Amsel, and Joan Bruna. Compositional reasoning with transformers, rnns, and chain of thought. arXiv preprint arXiv:2503.01544, 2025.

Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Shiji Song, and Gao Huang. Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model? arXiv preprint arXiv:2504.13837, 2025.

Hansi Zeng, Kai Hui, Honglei Zhuang, Zhen Qin, Zhenrui Yue, Hamed Zamani, and Dana Alon. Can Pre-training

Indicators Reliably Predict Fine-tuning Outcomes of LLMs?, 2025.

Chiyuan Zhang, Samy Bengio, Moritz Hardt, Benjamin Recht, and Oriol Vinyals. Understanding deep learning requires rethinking generalization. In International Conference on Learning Representations (ICLR), 2017.

Tong Zhang. Covering number bounds of certain regularized linear function classes. Journal of Machine

Learning Research, 2(Mar):527–550, 2002.

Tong Zhang. From ϵ-entropy to KL-entropy: Analysis of minimum information complexity density estimation.

The Annals of Statistics, 2006.

<!-- Page 22 -->

Contents of Appendix

I Additional Discussion and Results 23

A Related Work 23

B Comparison to Classical Generalization Bounds for MLE 24

C Experiments 25 C.1 Graph Reasoning Task......................................... 25 C.2 Experiment Details for Figure 1.................................... 27 C.3 Experiment Details for Figure 2.................................... 28

D Supporting Results 30 D.1 Properties of the Coverage Profile................................... 30 D.2 Analysis of Best-of-N Sampling under a Good Coverage Profile.................. 32 D.3 Properties of Maximum Likelihood.................................. 32 D.4 Autoregressive Models: Coverage and Stopped KL-Divergence................... 33

E Additional Results 35 E.1 Maximum Likelihood: Better Coverage for Convex Classes..................... 35 E.2 Lower Bound for Maximum Likelihood under Misspecification................... 35

II Proofs 37

F Technical Tools 37 F.1 Concentration Inequalities....................................... 37 F.2 Information-Theoretic Inequalities.................................. 38

G Proofs from Section 3 39

H Proofs from Section 4 39 H.1 Proof of Theorem 4.1 (Coverage for MLE).............................. 39 H.2 Proof of Theorem E.1 (Coverage for MLE with Convex Classes).................. 42 H.3 Proofs for Supporting Results..................................... 43

I Proofs for Autoregressive Linear Models 45 I.1 Organization.............................................. 45 I.2 Proof of Theorem 4.2 (Coverage for MLE for Autoregressive Linear Models)........... 46 I.3 Proof of Proposition 5.1 (Vanilla SGD: Coverage Upper Bound).................. 52 I.4 Proof of Proposition 5.1 (Vanilla SGD: Coverage Lower Bound).................. 53 I.5 Proof of Theorem 5.1 (Coverage for Normalized SGD)....................... 56 I.6 Proof of Theorem 6.1 (Test-Time Training)............................. 61 I.7 Proof of Theorem 6.2 (Gradient Normalization for Distillation).................. 63 I.8 Necessity of Variance Dependence in High Dimension........................ 65

J Proofs from Section 6 66 J.1 Proof of Theorem 6.3 (Simple Tournament)............................. 66 J.2 Proof of Theorem 6.4 (Offset Tournament).............................. 67

<!-- Page 23 -->

Part I Additional Discussion and Results

A Related Work

Related empirical observations. On the empirical side, our results are connected to a line of work that studies scaling laws for zero-shot downstream performance based on pre-training metrics such as crossentropy (Gadre et al., 2024; Huang et al., 2024; Chen et al., 2024b; Sardana et al., 2024). Several empirical works have also investigated how specific capabilities scale with additional pre-training, including machine translation (Ghorbani et al., 2022), knowledge capacity and memorization (Allen-Zhu and Li, 2025; Lu et al., 2024), and multi-hop reasoning (Wang et al., 2025). Our findings are consistent with Liu et al. (2022); Zeng et al. (2025); Lourie et al. (2025); Springer et al. (2025), who observe that cross-entropy is not always sufficient for predicting downstream performance, and in some cases can be anti-correlated.

Perhaps most closely related, Chen et al. (2025) show empirically that decreasing cross-entropy in pre-training does not necessarily lead to better Pass@N performance, and that Pass@N can even degrade as pre-training proceeds—a finding similar to Figure 1.8 Our results can be viewed as placing their findings on stronger theoretical footing; conversely, their empirical results provide strong motivation for our theoretical treatment. Chen et al. (2025) also study a modification to the maximum likelihood objective aimed at improving coverage (in the spirit of Section 6); their approach targets the structure of outcome-based reward, whereas our notion of coverage profile and results are agnostic to the downstream task/reward structure.

We mention in passing some additional works. Chu et al. (2025) explored the different (synergistic) roles that supervised fine-tuning (SFT) and RL play in language model development, and subsequent work observed that the best checkpoint to start RL from can sometimes be in the middle of SFT training (Jin et al., 2025). Bansal et al. (2025) empirically identified the coverage of teacher-generated synthetic data as an important indicator for how effective distillation can be for reasoning tasks. Several papers have also investigated empirical tradeoffs between model size and reasoning performance under best-of-N sampling (Snell et al., 2025; Brown et al., 2025).

Coverage in post-training. Coverage metrics similar to coverage profile play a central role in theoretical literature on post-training and test-time algorithms (Huang et al., 2025a,b,c; Foster et al., 2025; Liu et al., 2024; Song et al., 2024; Gao et al., 2024; Liu et al., 2024; Ji et al., 2024), which analyze algorithms under the assumption that the base model has good coverage; our work can be viewed as providing theoretical motivation for this assumption. Formally, one can use Markov’s inequality to bound the coverage profile by the Lp-like coverage quantities considered in these works.

Various notions of coverage similar to coverage profile have also appeared in the more classical literature on offline reinforcement learning (Farahmand et al., 2010; Chen and Jiang, 2019; Xie and Jiang, 2020; Jin et al., 2021; Foster et al., 2022; Jiang and Xie, 2024); here coverage is typically used to quantify the quality of an offline dataset rather than a model/policy itself.

Generalization in deep learning. Understanding the generalization behavior of deep learning models has been a central focus of the theory community for the last decade (Neyshabur et al., 2015; Zhang et al., 2017; Bartlett et al., 2017; Jacot et al., 2018; Belkin et al., 2019; Nagarajan and Kolter, 2019; Bartlett et al., 2020; Bartlett and Montanari, 2021). Our approach is somewhat complementary, in the sense that it focuses on the specific objective of next-token prediction with the logarithmic loss, and aims to understand when minimizing this loss leads to generalization for an alternative objective, coverage profile. We expect that our techniques can be combined with these contemporary generalization results to provide a more refined understanding of generalization for the coverage profile with deep models.

From this line of work, perhaps most closely related are Lotfi et al. (2023, 2024); Finzi et al. (2025), which aim to provide non-vacuous generalization bounds for the cross-entropy loss itself for autoregressive models.

8Note that Chen et al. (2025) also uses the term “coverage”, but as a synonym for Pass@N; this is not specifically related to the notion of the coverage profile we consider here.

<!-- Page 24 -->

## Analysis

of maximum likelihood. Our theoretical results are closely related to a classical line of work in statistics (Wong and Shen, 1995; van de Geer, 2000; Zhang, 2006), which shows that maximum likelihood can converge to the true model in Hellinger distance (or other Renyi divergences) under minimal assumptions, even when KL divergence is poorly behaved (large or infinite); see Appendix B below for a detailed comparison. Our results in Section 4 are similar in spirit, but provide a more fine-grained perspective, showing that the coverage profile can converge even faster than these results might suggest, particularly as one ventures further into the tail. Our analysis has some conceptual similarity to the small ball method of Mendelson (2014, 2017), which we elaborate on in Section 4.2.

Our techniques are also related to recent work of Foster et al. (2024); Rohatgi et al. (2025), which specializes the general techniques above to autoregressive models (e.g., under Hellinger distance).

B Comparison to Classical Generalization Bounds for MLE

In this section we briefly compare our main coverage-based generalization bound for maximum likelihood to classical generalization bounds for maximum likelihood based on Hellinger distance and KL-divergence.

Comparison to KL concentration. For general model classes Π, the best non-asymptotic KL-based generalization bound we are aware of is Proposition D.9 (Appendix D), which scales as roughly

DKL(πD ∥bπ) ≲log Wmax · Cfine(Π, n)

under the assumption that all π ∈Π obey a sequence-level density ratio bound πD π

∞≤Wmax. Note that for the autoregressive linear class, we have log Wmax = BH, matching Proposition 3.2. Combining such a guarantee with Proposition 3.1 gives a coverage bound of roughly

CovN(bπ) ≲log Wmax log N · Cfine(Π, n);

this is rather uninteresting since CovN(bπ) = 0 for N ≥Wmax; in other words, we do not get a meaningful improvement as we scale N.

Comparison to Hellinger concentration. The Hellinger distance is a standard metric of distribution estimation, defined via D2

H(P, Q) = 1

2 R

(

√

P −√Q)2. The guarantees of maximum likelihood estimation (Wong and Shen, 1995; Van der Vaart, 2000; Zhang, 2006) also imply convergence in Hellinger distance. For general model classes Π, the best non-asymptotic Hellinger-based generalization bound we are aware of is Proposition D.8 (Appendix D), which scales as roughly

D2

H(πD, bπ) ≲Cfine(Π, n)

Combining such a guarantee with Proposition 3.1 gives a coverage bound of

CovN(bπ) ≲Cfine(Π, n)

for all N ≥2. Compare to the KL-based result above, this result gives a non-trivial bound on coverage when N is constant (comparable to Theorem 4.1), but the issue is that it gives no further improvement as we scale N.

Asymptotic bounds for maximum likelihood. We also note that the classical theory of maximum likelihood (e.g., Van der Vaart (2000)) provides asymptotic convergence rates for d-dimensional parametric classes Π which have the following form:

DKL(πD ∥bπ) ≲d n ≲Cfine(Π, n), as n →+∞.

While this upper bound does not scale with log Wmax, it can only be attained with n ≥n0 for a sufficiently large burn-in cost n0, which itself will typically scale with log Wmax or similar problem-dependent parameters; see, e.g., Spokoiny (2012) for non-asymptotic bounds of this type. Our lower bounds (e.g., Proposition 3.2) imply that there is no hope of removing such a burn-in cost in general.

<!-- Page 25 -->

C Experiments

This section presents details for the experiments in Figure 1 and Figure 2. We describe the general graph search task used throughout our experiments in Appendix C.1, then detail the specific setups used for Figure 1 in Appendix C.2, and for Figure 2 in Appendix C.3.

C.1 Graph Reasoning Task

We evaluate our theoretical predictions using experiments in graph reasoning tasks, in which transformer models are trained to find paths between source and target nodes in graphs. Both graph reasoning benchmarks and synthetic datasets have seen increasing use as abstractions for reasoning problems and for probing language modeling phenomena (Sanford et al., 2024; Nagarajan et al., 2025; Saparov et al., 2025; Bachmann and Nagarajan, 2024; Yehudai et al., 2025; Taylor et al., 2024; Wang et al., 2023; Fatemi et al., 2024; Tang et al., 2025). These tasks provide minimal abstractions of core reasoning problems, yet are expressive enough to capture pre-training and fine-tuning phenomena. They also offer flexibility in problem structure and difficulty: by specifying different graph topologies and path depths, we can modulate difficulty and expose sources of hardness.

C.1.1 Graph Search Task Description

The graph search tasks for all of our experiments in Appendix C.2 and Appendix C.3 share the same high-level components, and are comprised of

• Problem instances. A set of graph search problems G that map bijectively to a set of prompts X.

• Data distribution. A distribution over the prompts µ ∈∆(X). and a data collection policy πD: X → ∆(Y)

• Dataset. The training dataset D = {(x, y)} is comprised of prompts x ∼µ and y ∼πD(x).

Next, we describe the general details of the graph search task common to all experiments, as well as how the graph search task is converted to a sequence modeling problem for language models.

Graph problem instances. Each graph search problem in G ∈G is specified by a tuple G = (G, s, t). Here, G = (V, E) is a graph structure with nodes (or vertices) V and edges E = {(u, v): u, v ∈V, u̸ = v}, s ∈V is the source node, and t is the target node. The nodes V are represented as integers, so that V ⊂[m] for some fixed m ∈Z.

For all experiments, we utilize a layered directed acyclic graph (layered DAG) for each graph structure (G, _, _) ∈G, in which nodes are organized into sequential layers with edges flowing only from one layer to the next. The graph G = (V, E) has L + 2 layers with disjoint sets of nodes, so that V = ⊔i∈{1,...,L+2}V i where V i denotes the set of nodes in layer i. The first and last layers contain only the source and target nodes, respectively, so that V 1 = {s} and V L+2 = {t}.

The edge structure E connects only a subset of nodes in each layer to the next. We refer to this subset in each layer i ∈{1,..., L + 2} as its passable nodes V i

∗⊆V i, or the set of nodes with non-zero out-degree,

V i

∗= v ∈V i: deg+(v) > 0

.

The passable nodes in layer i are fully connected to all nodes in the next layer, that is,

E =

(u, v): u ∈V i

∗, v ∈V i+1, i ∈{1,..., L + 1}

.

The remaining nodes in V i \ V i

∗have no outgoing edges, and are thus nodes the model must learn to avoid in order to output valid paths.

Data distribution. The model’s task is to imitate the data collection policy πD, which samples only a subset of the (potentially many) valid paths from source to target based on global features of the graph. A valid path from s to t is a list of nodes of the form (s, v2,..., vL+1, t) where vi ∈V i

∗for each i ∈{2,..., L + 1}; that is, the path must start with the source node s and end with the target node t, and each intermediate node in

<!-- Page 26 -->

the path must be a passable node from its respective layer. A graph may have many valid paths, specifically, Q i∈[L+2]|V i

∗| many. In order for a model to learn valid paths, learning a simple local rule suffices: it can output any node in the next layer with > 0 out-degree, which is representable by a fairly shallow transformer.

However, imitating πD is a much harder problem. The data collection policy πD samples a subset of these valid paths determined via global rules, or complex functions computed over features of the entire graph that go beyond those required for path validity alone. By varying the complexity of these rules, we can modulate both the difficulty and the nature of the learning problem. This structure naturally maps onto reasoning tasks: following passable nodes corresponds to taking “reasoning steps” that make progress towards the solution, while selecting non-passable nodes corresponds to reasoning errors that lead to invalid solutions. Moreover, when πD selects among valid paths via such global rules, this corresponds to learning high-quality solutions that accurately reflect desired properties for the problem.

Dataset. Recall that the model learns to imitate πD from a dataset D = {(x, y)}, where each prompt x corresponds to a graph search problem G = (G, s, t) ∈G, and each response y ∼πD(· | x) is an expert response, formatted as follows.

We convert a given graph search problem G = (G, s, t) ∈G with graph structure G = (V, E) to a prompt x by concatenating the edge list E, the source node s, and the target node t, formatted as x: u_1 v_1 | u_2 v_2 |... | u_k v_k / s t = where (ui, vi) ∈[m]2 are the vertices of the i-th edge in the edge set E. For formatting, the special character | separates two edges, the character / separates the adjacency list from the source and target nodes, while the character = marks the end of the prompt.

As an example, for edge set E = {(10, 23), (86, 47),..., (45, 32)}, the prompt is x: 10 23 | 86 47 |... | 45 32 / 10 45 =.

Next, each response y encodes the path from the source to the target node in G as a sequence of nodes. That is, the response takes the form of a string y: v_1 v_2 v_2 v_3... v_H-1 v_H where vi ∈[m] is the i’th nodes in the path for each i ∈[H], and v1 = s while vH = t. Here, the horizon H corresponds to the path length in G, and in the layered DAG we have H = L + 2.

Summary: Graph search to sequence modeling problem. In summary, a graph search task with set of problem instances G induces an autoregressive sequence modeling problem with a vocabulary space V = [m] ∪{|, /, =}, prompts X ⊆V∗corresponding to search problems in a layered DAG graph structure with L + 2 layers, and responses Y ⊆VH corresponding to paths with length H = L + 2. In addition, the task is equipped with µ ∈∆(X) and πD: X →∆(Y) that is used to collect the training dataset D = {(x, y)}, where x ∼µ and y ∼πD(x).

C.1.2 Model Details

Next, we describe the common implementation details for the models we train to solve the graph search task.

Tokenizer. We use a numeral tokenizer, which is standard for graph reasoning tasks (Sanford et al., 2024; Bachmann and Nagarajan, 2024). Each node v ∈[m] is tokenized as its integer node value, and the special characters |, /, and = are tokenized as m + 1, m + 2, m + 3, respectively.

Transformer model. We train causally-masked GPT2-like transformer models to minimize the cross-entropy loss using the Adam optimizer with fixed learning rate, and perform a grid search over the parameters displayed in Table 1. Parameters with fixed values were chosen based on related papers such as Bachmann and Nagarajan (2024). In both experiments, the model architecture with 4 heads, 6 hidden layers, and 384 hidden dimensions worked best. We use absolute positional encodings. Training iterations and grid search values for the learning rate are different for each experiment, and discussed further below.

<!-- Page 27 -->

Hyperparameter Values

Number of heads {4, 6, 8} Number of layers {3, 4, 6, 8} Hidden dimensions 384 Activation function GeLU Batch size 128 Weight decay 0.01

**Table 1.** Hyperparameter grid search values for transformer models in graph search.

C.2 Experiment Details for Figure 1

The graph search task for Figure 1 exposes natural properties of pre-training data under which cross-entropy reduction comes at the cost of a worse coverage profile. The key idea is that because the pre-training data is diverse (with multiple distinct modes or graph classes), the model is unable to perfectly fit the distribution. As a result, when one mode of behavior is better-represented than another, cross-entropy minimization, which is an average-case distribution-matching metric, can sacrifice coverage across the different modes in order to increase performance on a single mode.

Concretely, the graph search task for Figure 1 is a mixture of two classes of graph structures. Due to representational and finite-sample constraints, the model is unable to fit both perfectly during training, and, in particular, fitting one class well (in the sense of cross-entropy loss) comes at the cost of worse performance on the other. The checkpoint with the best coverage arises at some middle point in training when the model learns both classes of graphs equally well, and has good coverage over both classes (the dip CovN in the leftmost subplot of Figure 1). Further reduction of cross-entropy loss over the latter half of training requires the model to lose coverage over πD in the less-represented graph class (observed as the increase in CovN in the latter half of training iterations).

Even though the task cannot be learned perfectly from the supervised learning feedback, the model can still learn a policy that always samples a correct path matching πD’s with N = O(1) Best-of-N sampling attempts, which means that it leads to efficient downstream post-training (e.g., on one of the modes or with reward-based feedback), and also achieves optimal performance with test-time scaling methods.

For the experiments in Figure 1, we first pre-train a model on a larger set of graph structure classes so that it learns a diverse set of behaviors, then finetune its behavior on two. The performance on the fine-tuning task is displayed in Figure 1, and we first describe the fine-tuning dataset, followed by the pre-training dataset.

C.2.1 Task Description

All graphs in G follow the layered DAG structure described in Appendix C.1 with L = 8 intermediate layers that each have 4 nodes, i.e., |V i| = 4 for layers i ∈{2,..., 9} (recall the first and last layers contain only s and t, respectively).

Recall that in a layer i, V i

∗= v ∈V i: deg+(v) > 0 denotes the set of passable nodes. For each graph problem G = (G, s, t) ∈G with graph structure G = (V, E), a subset of the layers indexed by I2 ⊂{2,..., 9} with |I2| = 2 is randomly selected. Then, the edges E are defined so that the layers in I2 have two passable nodes each (i.e., |V i

∗| = 2 for i ∈I2), while the remaining layers have only one passable node each (i.e., |V i

∗| = 1 for i ∈{2,..., 9} \ I2). The passable nodes in each layer are chosen at random, but for the layers in I2 are guaranteed to have one even and one odd node. For each graph in G, there are 22 = 4 total valid paths since |I2| = 2 layers have two passable nodes each while the other layers have one.

Data distribution. The set of problem instances G = G1 ⊔G2 is comprised of two disjoint classes of problems, G1 and G2. The prompt distribution in the fine-tuning task is a skewed mixture over the two classes with eµ ∈∆({1, 2}) denoting the probability of each class in the data; within each class, the graphs are drawn uniformly at random (described at the end of this section). Although there are 4 valid paths from source to target, in each class G1 or G2 the policy πD chooses one path based on a different global rule, described below.

<!-- Page 28 -->

Class G1 (probability eµ(1) = 0.9). For an integer j ∈Z, let the function p(j) = (j mod 2) denote its parity. For layers i with |V i

∗| = 1, πD deterministically selects the unique passable node. For layers i ∈I2 (where |V i

∗| = 2), the set V i

∗contains one even and one odd node, and πD deterministically chooses the node v ∈V i

∗such that p(v) = p(i); that is, the node whose parity matches the parity of the layer index.

Class G2 (probability eµ(2) = 0.1). For layers i with |V i

∗| = 1, πD deterministically selects the unique passable node. For layers i ∈I2 (where |V i

∗| = 2), πD chooses the node v ∈V i

∗such that p(v) = 1 ⊕p(i); that is, the node whose parity is opposite to the parity of the layer index.

The class of a graph is technically identifiable from the prompt by computing a parity-based feature over a randomly selected subset of the nodes, but this problem is too difficult for the model to learn in the fine-tuning stage. Let V ′ ⊆V be a fixed subset of nodes whose cardinality is half the total number of nodes in the graph (i.e., |V ′| = |V |/2). Then all graphs in G1 satisfy 1 = L u∈V ′ p(u), while all graphs in G2 satisfy 0 = L u∈V ′ p(u). However, determining which nodes belong to V ′ requires complex reasoning over the graph structure.

Dataset. Each sample in the dataset D = {(x, y)} is then generated via the following procedure.

1. First sample an index i ∼eµ.

2. Sample G ∈Gi by randomly drawing V ⊂[m] without replacement, and instantiate the edges according to the description for each class above.

## 3 Format the prompt x per

## Appendix

C.1.

4. Draw y ∼πD(· | x) according to description for each class above.

C.2.2 Pre-Training Description

The graph problem instances in the pre-training task, Gpre, are a superset of the graphs in the fine-tuning task, that is, ∪i∈[K]Gi = Gpre with K = 3, and G1 and G2 defined as in the previous section for the finetuning dataset. The data distribution is a uniform mixture of these 3 classes, eµ(i) = 1

K for each i ∈[K], and the third class G3 shares the same layered DAG structure as G1 and G2 (with L = 8 intermediate layers, where two layers are randomly chosen to have multiple passable nodes). However, in G3, πD is a stochastic policy and samples one of the 22 = 4 valid paths at random. The dataset is then drawn using the same data generation procedure described for the fine-tuning task above.

C.2.3 Task-Specific Implementation Details

The transformer model is first pre-trained on a fixed dataset drawn from the pre-training distribution, with 8 × 64, 000 prompts in total, using a learning rate of 1e−4 for 200k iterations, which was chosen based on a grid search over learning rates {5e−5, 1e−4, 5e−4}.

The final checkpoint is then finetuned for 50k iterations in an online fashion, where fresh samples are drawn for each batch (this is equivalent to offline training with a dataset that has an equivalent number of samples). The learning rate is 5e−6, which was chosen based on a grid search over learning rates {5e−6, 1e−5}.

C.3 Experiment Details for Figure 2

For Figure 2, we consider a family of tasks that is parameterized by the horizon H, in order to expose the fact that cross-entropy is sensitive to horizon, but the coverage profile is not. This construction leverages the intuition from Remark 3.1. The training data is heterogeneous, with a fraction consisting of difficult graph problems that the model cannot learn to cover with the given number of training samples. This un-learnable subset of the data contributes to the large KL-divergence, but does not affect the coverage profile.

C.3.1 Task Description

For Figure 2, we devise a family of tasks parameterized by the number of intermediate layers H ∈{8, 16, 24}. For a fixed H, each task GH utilizes the layered DAG graph structure described in Appendix C.1 with L = H

<!-- Page 29 -->

intermediate layers, each containing 4 nodes, so that each graph has H + 2 total layers (including source and target). The response space is Y = VH+2, corresponding to paths of length H + 2 (including the source and target nodes).

Data distribution. The task is a heterogeneous mixture over 3 classes of graphs described below that we refer to as GH,1 ∪GH,2 ∪GH,3 = GH. The classes GH,2 and GH,3 are significantly harder to learn and the model will fail to do so with the given number of training samples, even though GH,1 is learned quickly (and also provides useful features for learning the other two tasks). The distribution over these 3 classes is fixed for all H and specified by eµ ∈∆({1, 2, 3}).

Class GH,1 (probability eµ(1) = 0.94). All H intermediate layers have only 1 passable node each (i.e., |V i

∗| = 1 for all i ∈{2,..., H + 1}), so each G ∈GH,1 has only one valid path from source to target. For prompts corresponding to graphs in this class, πD deterministically selects the unique valid path.

Class GH,2 (probability eµ(2) = 0.05). For each graph, half of the intermediate layers (or H/2) are randomly selected to have two passable nodes, while the rest have one. More formally, a subset IH/2 ⊂{2,..., H +1} with |IH/2| = H/2 is randomly selected, such that |V i

∗| = 2 for i ∈IH/2 and |V i

∗| = 1 for i ∈{2,..., H + 1} \ IH/2.

There are 2H/2 valid paths from source to target, and πD deterministically selects one of them. For layers i with |V i

∗| = 1, πD selects the unique passable node. For layers i ∈IH/2 (where |V i

∗| = 2), πD selects the node v ∈V i

∗ by following a difficult, deterministic rule. This rule requires πD to select the node v whose parity matches the parity of the layer index, XOR’ed with the parity of each passable node in the entire graph. More specifically, recall that p(j) denotes the parity of an integer j ∈[m], and let V∗:= SH+1 i=2 V i

∗denote the set of all passable nodes across all intermediate layers (including those with just one passable node). Then in layer i ∈IH/2, πD selects the node v ∈V i

∗such that p(v) = p(i) ⊕

L u∈V∗p(u)

.

Class GH,3 (probability eµ(3) = 0.01). Regardless of H, for each graph a subset I4 ⊂{2,..., H + 1} with |I4| = 4 is randomly selected, such that |V i

∗| = 2 for i ∈I4 and |V i

∗| = 1 for i ∈{2,..., H + 1} \ I4. There are 24 = 16 valid paths from source to target. The policy πD samples uniformly at random from these valid paths.

Note that prompts/graphs from each class are distinguishable from each other (or, identifiable) based on prompt features alone, so a powerful-enough model can achieve perfect performance across all of them simultaneously. GH,2, for example, has more edges and thus a longer prompt than GH,1; similar statements apply to GH,3. Dataset generation occurs in the same manner as described in Appendix C.2.

C.3.2 Task-Specific Implementation Details

Lastly, we describe experiment-specific implementation details on top of those previously described in Appendix C.1, which are common to all experiments. In addition to a grid search over the parameters in Table 1, we perform a search over learning rates {5e−5, 1e−4, 5e−4}, for which the learning rate of 1e−4 exhibited the best validation performance. The model is trained for 40k iterations over a fixed dataset of 8 × 64, 000 samples.

The results in Figure 2 are computed from evaluations of training checkpoints on per-class validation datasets of 1024 prompts from each GH,i for i ∈[3]; these metrics are then averaged according to the probabilities in eµ to obtain the final result. In total we ran 16 seeds, and plot their median. The shaded region in Figure 2 displays the region between the 1 16 quantile and 15 16 quantile.

<!-- Page 30 -->

D Supporting Results

This section presents technical results used throughout the paper. Appendix D.1 presents basic properties of the coverage profile. Appendix D.2 analyzes the performance of the Best-of-N algorithm under coverage. Appendix D.3 presents properties of the maximum likelihood estimator, and Appendix D.4 presents structural results relating the coverage profile to a “stopped” KL-divergence, which are useful for analyzing autoregressive models.

D.1 Properties of the Coverage Profile

This section presents elementary properties of the coverage profile.

Proposition D.1 (KL-to-coverage conversion). For all models πD and π and M ≥2, we have

CovN(π) ≤ DKL(πD ∥π) log N −1 + 1

N

.

Proof of Proposition D.1. Lemma 27 of Block and Polyanskiy (2023) states that for any N > 1 and any convex f: [0, ∞] →[0, ∞] with f(1) = f ′(1) = 0,

CovN(π) = PπD πD(y | x)

π(y | x) > N

≤NDf(πD ∥π)

f(N), (35)

where Df(πD ∥π):= Eπ f dπD dπ

. Applying this with KL-divergence, which corresponds to f(x) = x log x−x+1 with f ′(x) = log x, we have that

N f(N) = 1 log N −1 + 1/N, (36)

which gives the result.

Proposition D.2 (Tightness of KL-to-coverage conversion). For any N ≥2, there exist models πD and bπ such that

CovN(bπ) ≥ DKL(πD ∥bπ) log N −1

2 + 1 2N.

Proof of Proposition D.2. Consider πD = Ber(p) and bπ = Ber(p/N) with p ≤1

## 2 Then

CovN(bπ) = p and

DKL(πD ∥bπ) = p log N + (1 −p) log 1 −p

1 −p N

≤p log N + (1 −p)

1 −p

1 −p N

−1

= p log N −(1 −p)1 −1

N 1 −p N

≤p · log N −1

2 + 1 2N

.

This is the desired result.

Proposition D.3 (Uniform coverage decay implies bounded KL). Given π, πD: X →∆(Y), define Wmax:= supx,y πD(y|x)

π(y|x) and

C:= sup

N≥1

{CovN(π) · log N}, where we note that C ≤log Wmax. It holds that

DKL(πD ∥π) ≤C · (1 + log(log(Wmax)/C)). (37)

<!-- Page 31 -->

Proof of Proposition D.3. Let δ > 0 a fixed parameter, and define X:= πD/π. Then we have

DKL(πD ∥π) = EπD[log(X)] ≤EπD[log(X)I{log(X) > δ}] + δ. (38)

Since X ≤Wmax almost surely, we can write

EπD[log(X)I{log(X) > δ}] =

Z log(Wmax)

δ

PπD[log(X) > t]dt (39)

=

Z log(Wmax)

δ

PπD

X > et dt (40)

≤C

Z log(Wmax)

δ

1 t dt (41)

= C log log(Wmax)

δ

. (42)

The result now follows by setting δ = C.

Proposition D.4 (Hellinger-to-coverage conversion). For all models πD and π and N > 1, we have

CovN(πD ∥π) ≤ 2N (

√

N −1)2 · D2

H(πD, π).

Proof of Proposition D.4. Without loss of generality, we assume Y is discrete in the following proof. By definition,

D2

H(πD, π) = 1

2 Ex∼πD

"X y p πD(y | x) − p π(y | x)

2

#

≥1

2 Ex∼πD

"X y πD(y | x)

1 − 1 √

N

2

I π(y | x) ≤1

N πD(y | x)

#

= 1

2

1 − 1 √

N

2

PπD πD(y | x)

π(y | x) > N

, where the inequality follows from the fact that p πD(y | x) − p π(y | x) ≥

1 − 1 √

N p πD(y | x) is implied by π(y | x) ≤1

N πD(y | x). Re-organizing completes the proof.

Proposition D.5 (Chain rule for coverage profile). For any models πD, πT, and bπ, and any M1, M2 ≥2, we have

CovM1(πT ∥bπ) ≤M2 · CovM1/M2(πD ∥bπ) + CovM2(πT ∥πD). (43)

Proof of Proposition D.5. We can write

CovM1(πT ∥bπ) = PπT πT(y | x)

bπ(y | x) > M1

= PπT πT(y | x)

bπ(y | x) > M1, πT(y | x)

πD(y | x) ≤M2

+ PπT πT(y | x)

bπ(y | x) > M1, πT(y | x)

πD(y | x) > M2

≤M2PπD πD(y | x)

bπ(y | x) > M1/M2

+ PπT πT(y | x)

πD(y | x) > M2

= M2CovM1/M2(πD ∥bπ) + CovM2(πT ∥πD).

<!-- Page 32 -->

D.2 Analysis of Best-of-N Sampling under a Good Coverage Profile

In this section we analyze the performance of the Best-of-N algorithm under a good coverage profile. Let a base model bπ be given, and let a reward function rT(x, y) ∈[0, 1] be given. Let πT: X →∆(Y) denote an arbitrary task-specific comparator policy.

We let bπBoN

N (x) denote the distribution of the Best-of-N algorithm with parameter N, which draws N responses y1,..., yN i.i.d. ∼bπ(· | x) and returns y = arg maxyi rT(x, yi).

Proposition D.6 (Coverage implies success for BoN). Let M ≥1 be given. For any ε > 0, if N ≥2M log(ε−1) and CovM(πT ∥bπ) ≤1

2, then we are guaranteed that

Ex∼µ rT(x, πT(x)) −rT(x, bπBoN

N (x))

≤CovM(πT ∥bπ) + ε. (44)

Proof of Proposition D.6. This is an immediate consequence of Lemma F.1 in Huang et al. (2025b), noting that we can bound EM(πT ∥bπ) ≤CovM(πT ∥bπ).

Proposition D.7 (Coverage is necessary for BoN). For any model bπ and reference πT, and for any N ≥2, there exists a reward function rT(x, y) ∈{0, 1} such that

Ex∼µ rT(x, πT(x)) −rT(x, bπBoN

N (x))

≥1

2Cov2N(πT ∥bπ). (45)

Proof of Proposition D.7. For any x ∈X, we define Sx:= y ∈Y: πT(y|x)

bπ(y|x) ≥2N and let rT(x, y) = I{y ∈ Sx}.

By definition, for any fixed x ∈X, it holds that rT(x, bπBoN

N (x)) = Py∼bπBoN

N (x)(y ∈Sx) = Py1,...,yN i.i.d. ∼bπ(·|x)(∃i ∈[N], y i ∈Sx)

= 1 −

1 −Py∼bπ(·|x)(y ∈Sx) N ≤N · Py∼bπ(·|x)(y ∈Sx)

= N ·

X y∈Sx bπ(y | x) ≤N ·

X y∈Sx

1 2N πT(y | x) = 1 2Py∼πT(·|x)(Sx), where we use the fact that bπ(y | x) ≤ 1 2N πT(y | x) for any y ∈Sx. We also note that Px∼µ,y∼πT(·|x)(y ∈Sx) = Cov2N(πT ∥bπ). Therefore,

Ex∼µ rT(x, πT(x)) −rT(x, bπBoN

N (x))

≥1

2Cov2N(πT ∥bπ).

D.3 Properties of Maximum Likelihood

In this section, we specialize standard guarantees for maximum likelihood (Wong and Shen, 1995; van de Geer, 2000; Zhang, 2006) to derive bounds on the coverage profile; as discussed in Appendix B, these results are not tight compared to Theorem 4.1.

Proposition D.8 (Convergence of maximum likelihood in Hellinger distance). Assume that πD ∈Π. With probability at least 1 −δ, the maximum likelihood estimator bπ:= arg maxπ∈Π bLn(π) satisfies,

D2

H(πD, bπ) ≲inf ε>0 log N∞(Π, ε)

n + ε

, (46)

and consequently

CovM(bπ) ≲inf ε>0 log N∞(Π, ε)

n + ε

. (47)

for all M ≥2.

<!-- Page 33 -->

Proof of Proposition D.8. The first bound follows from Proposition B.2 of Foster et al. (2024). The second bound follows from applying Proposition D.4.

Proposition D.9 (Convergence of maximum likelihood in KL). Assume that πD ∈Π, and that all π ∈Π satisfy πD π

∞≤Wmax. With probability at least 1−δ, the maximum likelihood estimator bπ:= arg maxπ∈Π bLn(π) satisfies,

DKL(πD ∥bπ) ≲log Wmax · inf ε>0 log N∞(Π, ε)

n + ε

, (48)

and consequently

CovM(bπ) ≲log Wmax log M · inf ε>0 log N∞(Π, ε)

n + ε

, (49)

for all M ≥2.

We remark that the log(Wmax)-factor in Eq. (48) can be tight in general. For example, for the class Π considered in Proposition 3.2, it holds that log N∞(Π, ε) ≲log(1/ε) ∨1 and πD π

∞≤e2H.

Proof of Proposition D.9. By Lemma 4 of Yang and Barron (1998), it holds that

DKL(πD ∥bπ) ≤(2 + log(Wmax))D2

H(πD, bπ).

Therefore, the first bound then follows from Eq. (46). The second bound follows from applying Proposition D.1.

D.4 Autoregressive Models: Coverage and Stopped KL-Divergence

This section shows that we can relate the coverage profile to a “stopped” KL-divergence defined in Eq. (50). This is a useful result in the context of autoregressive models because the stopped KL-divergence is always bounded, even when KL-divergence itself may not be.

Proposition D.10. Define the stopped KL-divergence for parameter N as

Dseq,N(πD ∥π) = E(x,y1:H)∼πD

" min

( log N,

H X h=1

DKL(πD(· | x, y1:h−1) ∥π(· | x, y1:h−1))

)#

. (50)

Then as long as N > e, it holds that

CovN(πD ∥π) ≤ 2 log N −1Dseq,N(πD ∥π). (51)

Proof of Proposition D.10. Consider the stopping time τ:= min

 

h: h = H or

X j≤h

DKL(πD(yj+1 = · | x, y1:j) ∥π(yj+1 = · | x, y1:j)) > log N

 

.

Then, for the process Y τ = (x, y1:τ), we have the chain rule:

DKL(πD(Y τ = ·) ∥π(Y τ = ·))

= EπD

" τ X h=1

DKL(πD(yh = · | x, y1:h−1) ∥π(yh = · | x, y1:h−1))

#

≤EπD min

( log N,

H X h=1

DKL(πD(yh = · | x, y1:h−1) ∥π(yh = · | x, y1:h−1))

)

,

<!-- Page 34 -->

where the inequality uses P j<τ DKL(πD(yj+1 = · | x, y1:j) ∥π(yj+1 = · | x, y1:j)) ≤log N, which follows from the definition of τ. Therefore, by Proposition D.1, we have

PπD πD(Y τ)

π(Y τ) ≥log N

≤DKL(πD(Y τ = ·) ∥π(Y τ = ·))

log N −1 + 1/N.

Finally, we bound

PπD πD(y1:H | x)

π(y1:H | x) ≥N

≤PπD(τ < H) + PπD πD(Y τ)

π(Y τ) ≥log N

.

By Markov’s inequality,

PπD(τ < H) ≤PπD

H X h=1

DKL(πD(· | x, y1:h−1) ∥π(· | x, y1:h−1)) > log N

!

≤ 1 log N EπD min

( log N,

H X h=1

DKL(πD(· | x, y1:h−1) ∥π(· | x, y1:h−1))

)

.

Combining the inequalities above completes the proof.

The following result is a sort of partial converse to Proposition D.10, showing that the coverage profile can be lower bounded in terms of the tail behavior for a sum of step-wise Hellinger distances.

Proposition D.11. For any N ≥1 and δ ∈(0, 1), it holds that

CovN(πD ∥π) ≥PπD

H X h=1

D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) ≥log(N/δ)

!

−δ.

Proof of Proposition D.11. By definition,

Eyh∼πD(·|x,y1:h−1) exp

−1

2 log πD(yh | x, y1:h−1) π(y | x, y1:h−1)

=

X yh∈Y p πD(yh | x, y1:h−1) · π(y | x, y1:h−1)

= 1 −D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) ≤exp

−D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1))

.

Therefore, it holds that

EπD exp

H X h=1

D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) −1

2 log πD(yh | x, y1:h−1) π(y | x, y1:h−1)

!

≤1.

By Markov inequality, this implies

PπD

1 2 log πD(y1:H | x) π(y1:H | x) ≤

H X h=1

D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) −log(1/δ)

!

≤δ.

To conclude, we note that

PπD

H X h=1

D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) ≥log(N/δ)

!

≤PπD

H X h=1

D2

H(πD(· | x, y1:h−1), π(· | x, y1:h−1)) ≥1

2 log πD(y1:H | x) π(y1:H | x) + log(1/δ)

!

+ PπD

1

2 log πD(y1:H | x) π(y1:H | x) + log(1/δ) ≥log(N/δ)

≤δ + CovN(πD ∥π).

Re-organizing gives the desired result.

<!-- Page 35 -->

E Additional Results

E.1 Maximum Likelihood: Better Coverage for Convex Classes

In this section, we give an extension to Theorem 4.1 which shows that maximum likelihood can achieve a faster convergence rate for coverage—as well as strong tolerance to misspecification—when the model class is convex.

Assumption E.1 (Convex model class). The class Π satisfies Π = {πθ: θ ∈Θ} for a convex, compact parameter space Θ, and the mapping θ 7→πθ(y | x) is concave for all x ∈X, y ∈Y.

Theorem E.1 (Fast convergence of coverage for convex classes). Let α ≥0, N ′ ≥1, N ≥2e2αN ′ be given, and suppose that Assumption E.1 holds. Let θ⋆∈arg min θ∈Θ

DKL(πD ∥πθ).

With probability at least 1 −δ, the maximum likelihood estimator bπ:= arg maxπ∈Π bLn(π) satisfies

CovN(bπ) ≤CovN′(πθ⋆) + C log N∞(Π, α) + log(δ−1)

n + Ce2αN ′

N · inf ε>0 log N∞(Π, ε)

n + ε

, (52)

where C > 0 is an absolute constant.

Note that we allow for misspecification here, as Eq. (52) shows that the coverage of bπ can be upper bounded by the coverage of πθ⋆, the best-in-class approximator of πD with respect to KL-divergence. In the well-specified case where πD ∈Π, the bound simplifies to

CovN(bπ) ≲ 1 N 1−2c · inf ε>0 log N∞(Π, ε)

n + ε

+ log N∞(Π, c log N) + log(δ−1)

n

= Cfine(Π, n)

N 1−2c + Ccoarse(Π, N, n), which improves upon the rate CovN(bπ) ≲Cfine(Π,n)

log N + Ccoarse(Π, N, n) in Theorem 4.1. The proof of Theorem E.1 is presented in Appendix H.2.

E.2 Lower Bound for Maximum Likelihood under Misspecification

In the following proposition, we show that without a well-specified model class (Assumption 2.1), maximum likelihood may have coverage profile scaling with 1 log M minπ∈Π DKL(πD ∥π) (cf. Proposition D.3), even when there exists π ∈Π such that CovN(π) = 0.

Proposition E.1 (MLE under misspecification). For any α ∈[0, 1], M > eα, there exists a problem instance πD and class Π = {π1, π2} such that sup x,y |log πD(y | x) −log π1(y | x)| ≤α, CovN(π2) ≥ cα2 log M, and for any n ≥1, it holds that with probability at least 1

4, the MLE bπ = π2, i.e., CovN(bπ) = Ω α2 log M

.

Proof of Proposition E.1. Let p = α 32 log M. Consider X = {+, −}, Y = {0, 1}, ρ(−) = p, ρ(+) = 1 −p, and πD is given by πD(· | +) = πD(· | +) = Ber

1

2

.

We construct the class Π = {π1, π2} as π1(·|+) = Ber

1

2eα

, π2(·|−) = Ber

1

2

, π2(·|+) = Ber

1

2

, π2(·|−) = Ber

1

2M

.

<!-- Page 36 -->

Given the dataset D = {(xt, yt)}t∈[n] sampled from πD, we define N(x, y) = #{t ∈[n]: (xt, yt) = (x, y)} and N(x) = N(x, 0) + N(x, 1). Then bLn(π2) −bLn(π1) = N(+, 1) · α + N(+, 0) · log eα

2eα −1

−N(−, 1) · log M + N(−, 0) · log

2 −1 M

.

By symmetric, it holds that P(N(+, 1) ≥N(+, 0)) ≥ 1 2. Further, by Markov’s inequality, it holds that P(N(−) ≥4np) ≤1

4. Therefore, for the event E = {N(+, 1) ≥N(+, 0), N(−) ≤4np}, we have P(E) ≥1 4. In the following, we show that bLn(π2) −bLn(π1) > 0 under E.

We condition on E. We first note that under this event, we have N(+, 1) ≥1

2N(+), N(+, 0) ≤1 2N(+). Hence, bLn(π2) −bLn(π1) ≥N(+)

1

2 · α + 1 2 · log eα

2eα −1

−N(−) · log M

= N(+) · DKL

Ber

1

2

∥Ber

1

2eα

−N(−) · log M

≥N(+) · (1 −e−α)2 −N(−) · log M.

Finally, using the fact that 1 −e−α > 1

2α and N(+) ≥(1 −4p)n ≥1 2n under E, we have bLn(π2) −bLn(π1) > α2

8 −4p log M n = 0.

Hence, under the event E, we have bπ = π2. However, it is clear that

CovN(π2) = p, CovN(π1) = 0.

This completes the proof.

<!-- Page 37 -->

Part II Proofs

F Technical Tools

Notation. We denote by Bd

2(R):= v ∈Rd: ∥v∥≤R the d-dimensional Euclidean ball of radius R. We drop the superscript when the dimension d is clear from context.

F.1 Concentration Inequalities

Lemma F.1 (Freedman’s inequality). Let (Zi)i≤n be a real-valued martingale difference sequence adapted to a filtration (Fi)i≤n. If |Zi| ≤R almost surely, then for any η ∈(0, 1/R), with probability at least 1 −δ, for all n′ ≤n, n′ X i=1

Z i ≤η n′ X i=1

Ei−1

(Z i)2

+ log(δ−1)

η.

The next result is a standard consequence of Lemma F.1 (e.g., Foster et al. (2021)).

Lemma F.2. Let (Zi)i≤n be a sequence of random variables adapted to a filtration (Fi)i≤n. If 0 ≤Zi ≤R almost surely, then with probability at least 1 −δ, for all n′ ≤n, n′ X i=1

Z i ≤3

2 n′ X i=1

Ei−1[Z i] + 4R log(2δ−1), (53)

and n′ X i=1

Ei−1[Z i] ≤2 n′ X i=1

Z i + 8R log(2δ−1). (54)

The following lemma is a uniform version of, e.g., Lemma 23 in Foster and Rakhlin (2023).

Lemma F.3. Suppose that µ is a distribution over Z, and let F ⊆(Z →R) be a function class. We let N(F, ϵ; ∥·∥∞) be the ϵ-covering number of F under the norm ρ(f, f ′):= supz∈Z|f(z) −f ′(z)|. Let D = {Z1, · · ·, Zn} be drawn i.i.d. from µ. Then the following holds with probability at least 1 −δ:

n X i=1 f(Z i) ≤n log Eµ[exp(f(Z))] + log(1/δ) + inf ϵ≥0{log N(F, ϵ; ∥·∥∞) + 2nϵ}, ∀f ∈F.

Proof of Lemma F.3. Fix ϵ ≥0 attaining the minimum of log N(F, ϵ; ∥·∥∞) + 2nϵ, and let f1, · · ·, fJ be an ϵ-covering of F of size J = N(F, ϵ; ∥·∥∞). For each j ∈[J], we define gj(z):= fj(z) −log Eµ[exp(fj(Z))]. Then, it is clear that Eµ egj(Z)

= 1, and hence

E

" exp n X i=1 gj(Z i)

!#

= 1, ∀j ∈[J].

By Markov’s inequality and the union bound, it holds that with probability at least 1 −δ, n X i=1 gj(Z i) ≤log(J/δ), ∀j ∈[J]. (55)

Note that for any f ∈F, there exists j ∈[J] such that ρ(f, fj) ≤ϵ, and in particular f(Z i) −log Eµ[exp(f(Z))] ≤2ϵ + fj(Z i) −log Eµ[exp(fj(Z))] = 2ϵ + gj(Z i), ∀i ∈[n],

<!-- Page 38 -->

and hence Eq. (55) implies that Pn i=1 f(Zi) ≤n log Eµ[exp(f(Z))] + log(J/δ) + 2nϵ. By the arbitrariness of f, the proof is hence completed.

F.2 Information-Theoretic Inequalities

Lemma F.4. For distribution P, Q ∈∆(X), function f: X →[−B, B], it holds that

|EP [f] −EQ[f]| ≤4 q

VarQ[f] · D2

H(P, Q) + 8BD2

H(P, Q).

More generally, for any g: X →B2(B), it holds that

∥EP [g] −EQ[g]∥≤4 q

EQ∥g −EQ[g]∥2 · DH(P, Q) + 8BD2

H(P, Q). (56)

and

EP ∥g −EP [g]∥2 ≤3 EQ∥g −EQ[g]∥2 + 16B2D2

H(P, Q). (57)

Proof of Lemma F.4. We denote P(x) (resp. Q(x)) to be the density function of P (resp. Q). Then for any function f: X →R,

|EP [f] −EQ[f]|2 =

Z

X

(f(x) −EQ[f])(P(x) −Q(x))dx

2

≤

Z

X

(f(x) −EQ[f])2( p

P(x) + p

Q(x))2dx ·

Z

X

( p

P(x) − p

Q(x))2dx

≤4D2

H(P, Q) ·

VarQ[f] + EP (f −EQ[f])2

.

In particular, when h: X →[0, M], the inequality above implies that

|EP [h] −EQ[h]| ≤2DH(P, Q)

q

M(EP [h] + EQ[h]) ≤1

2(EP [h] + EQ[h]) + 2MD2 H(P, Q), and hence it holds that EP [h] ≤3 EQ[h] + 4MD2

H(P, Q).

Now, suppose that f: X →[−B, B]. Applying the above inequality to h(x) = (f −EQ[f])2 ∈[0, 4B2] gives

EP (f −EQ[f])2 ≤3 EQ(f −EQ[f])2 + 16B2D2

H(P, Q). (58)

Combining the above inequalities implies that

|EP [f] −EQ[f]| ≤4 q

VarQ[f] · D2

H(P, Q) + 8BD2

H(P, Q).

To prove the upper bound for a vector-valued function g: X →B2(B), we can apply the above inequality with fv(x):= ⟨v, g(x)⟩and take the maximum over v ∈B2(1). The second upper bound follows similarly by applying Eq. (58).

Lemma F.5. Suppose that ϕ: Y →B2(B) with B ≥1, and for any θ ∈B2(1), πθ ∈∆(Y) is defined as πθ(y) ∝exp(⟨ϕ(y), θ⟩). Then for any θ⋆, θ ∈B2(1), it holds that

Ey∼πθ⋆⟨ϕ(y) −Eπθ⋆[ϕ], θ −θ⋆⟩2 ≤15BDKL(πθ⋆∥πθ).

Proof of Lemma F.5. Denote ϕ(y):= ϕ(y) −Eπθ⋆[ϕ]. By definition,

DKL(πθ⋆∥πθ) = log Ey∼πθ⋆ exp

⟨ϕ(y), θ −θ⋆⟩

≥B log Ey∼πθ⋆ exp

1

B ⟨ϕ(y), θ −θ⋆⟩

.

<!-- Page 39 -->

Note that for x ≥−4, we have ex ≥1 + x + 1

10x2. Therefore, we have

1 B DKL(πθ⋆∥πθ) ≥log

1 + 1 10B2 Ey∼πθ⋆⟨ϕ(y), θ −θ⋆⟩2

≥ 1 15B2 Ey∼πθ⋆⟨ϕ(y), θ −θ⋆⟩2, where we use log(1 + x) ≥3

4x for all x ∈[0, 8 5].

G Proofs from Section 3

Proof of Proposition 3.2. Consider the setting where d = 1, X = {0, 1}, V = {−1, 1}, the distribution µ is given by µ(1) = 1 −µ(0) = 1 2n, and the feature map ϕ: X × V⋆→[−1, 1] is given by ϕ(0, ·) = 0, and ϕ(1, y1:h) = yh.

In the following, we fix any algorithm Alg: (X × Y)n →∆(Π). Let Pπθ,Alg be the probability distribution of (D = {(xt, yt)}t∈[n], bπ) where xt ∼µ, yt ∼πθ(· | xt) are sampled i.i.d. and bπ ∼Alg(D).

Note that under this construction, Pπθ,Alg(xt = 0 ∀t ∈[T]) ≥1 −nµ(1) = 1

2. Consider the event E = {xt = 0 ∀t ∈[T]}. Then, for any θ⋆∈[−1, 1], event A, it holds that

P πθ⋆,Alg(A | E) = E π0,Alg(A | E), because for any θ ∈Θ, the distribution πθ(y1:H = · | 0) = Ber

1

2 ⊗H is a product of H Bernoulli distributions and does not depend on θ. Furthermore, for any θ ∈[−1, 1],

DKL(πθ⋆∥πθ) = µ(1) · DKL(πθ⋆(y1:H = · | x = 1) ∥πθ(y1:H = · | x = 1))

= Hµ(1) · DKL

Ber eθ⋆ eθ⋆+ e−θ⋆

∥Ber eθ eθ + e−θ

, and hence θ 7→DKL(π1 ∥πθ) + DKL(π−1 ∥π) is minimized at θ = 0, i.e., for any bπ ∈Π,

DKL(π1 ∥bπ) + DKL(π−1 ∥bπ) ≥H

2n · 2DKL

Ber e e + e−1

∥Ber

1

2

≥H

2n.

Therefore, consider the event Aθ:=

DKL(πθ ∥bπ) ≥H

4n

, and we have shown that Ac

1 ⊆A−1. Hence, we can lower bound

P π1,Alg(A1) + P π−1,Alg(A−1) ≥P π1,Alg(E)P π1,Alg(A1 | E) + P π−1,Alg(E)P π−1,Alg(A−1 | E)

≥1

2 E π0,Alg[A1 | E] + 1

2 E π0,Alg[A−1 | E] ≥1

2.

This gives maxθ⋆∈{−1,1} Pπθ⋆,Alg

DKL(πθ⋆∥bπ) ≥H

4n

≥1

4, and the desired result follows immediately.

As a remark, we note that the construction above can be modified so that the variance σ2

⋆(defined in Section 4.1) can be bounded as σ2

⋆≲He−2B n. In particular, as long as B ≳log H, it holds that σ⋆≤1, implying that KL can converge slowly even when the “inherent variance” σ⋆is small.

H Proofs from Section 4

H.1 Proof of Theorem 4.1 (Coverage for MLE)

Theorem 4.1′ (General version of Theorem 4.1). Let N ≥8 be given. With probability at least 1 −δ, any approximate maximum likelihood estimator bπ with bLn(bπ) ≥maxπ∈Π bLn(π) −nεapx satisfies

CovN(bπ) ≲log N∞(Π, c log N) + log(δ−1)

n + 1 log N inf ε>0 log N∞(Π, ε)

n + ε

+ εapx

, (59)

where c > 0 is an absolute constant.

<!-- Page 40 -->

In the following, for a fixed threshold C ≥log 4, we define the clipped log loss as

L+

C(π):= n X i=1 max log π(yi | xi)

πD(yi | xi), −C

, (60)

L−

C(π):= n X i=1 max

0, log πD(yi | xi) π(yi | xi) −C

. (61)

Note that bLn(π) −bLn(πD) = L+

C(π) −L−

C(π). Furthermore, since πD ∈Π, the approximate maximum likelihood estimator satisfies bLn(bπ) ≥bLn(πD) −nεapx, and hence

L−

C(bπ) ≤L+

C(bπ) + nεapx.

In the following, we show that L+

C(π) can be bounded by a one-sided uniform convergence argument, and show that L−

C(π) upper bounds the coverage profile CovN(π) for any π ∈Π and log N > C.

Proposition H.1. Suppose that C ≥log 4. Then, with probability at least 1 −δ, it holds that for any π ∈Π,

L+

C(π) ≤log(1/δ) + 2 inf ϵ≥0{log N∞(Π, ϵ) + nϵ}.

Proposition H.2. Fix any α ∈(0, log N−C

2). Then, with probability at least 1 −δ, it holds that

CovN(π) ≤ 2 log N −C −2α · L−

C(π) + 16 log(2N∞(Π, α)/δ)

n.

The proof of Theorem 4.1 and Theorem 4.1′ is completed by combining the propositions above and setting α = 1

4 log N. In what follows, we prove the propositions.

Proof of Proposition H.1. This is a direct corollary of Lemma F.3. For each π ∈Π, we let fπ(x, y):=

1 2 max n log π(y|x)

πD(y|x), −C o and consider the function class F = {fπ: π ∈Π}. Then, N(F, ϵ; ∥·∥∞) ≤N∞(Π, 2ϵ) for any ϵ ≥0. Applying Lemma F.3 with Lemma H.1 (stated and proved below) gives the desired upper bound.

Lemma H.1. As long as C ≥log 4, it holds that

E(x,y)∼πD exp

1

2 max log π(y | x)

πD(y | x), −C

≤1. (62)

Proof of Lemma H.1. We denote u = e−C and E:= n

(x, y): π(y|x)

πD(y|x) ≥u o

. Then it holds that

E(x,y)∼πD exp

1

2 max log π(y | x)

πD(y | x), −C

= E(x,y)∼πD

"s π(y | x) πD(y | x)I{(x, y) ∈E} + √u I{(x, y)̸ ∈E}

#

= Ex∼πD



 X y:(x,y)∈E p π(y | x)πD(y | x)



+ √u PπD(Ec).

For x ∈X, denote Ex:= {y: (x, y) ∈E}. By the Cauchy-Schwarz inequality, we have

X y:(x,y)∈E p π(y | x)πD(y | x) ≤ s X y∈Ex π(y | x) ·

X y∈Ex πD(y | x) ≤ q

Py∼πD(·|x)(Ex).

<!-- Page 41 -->

Therefore, as long as u ≤1

4 (or equivalently, C ≥log 4), it holds that

E(x,y)∼πD exp

1

2 max log π(y | x)

πD(y | x), −C

≤ p

PπD(E) + 1

2PπD(Ec) ≤1, where we use 1 −p = (1 + √p)(1 −√p) ≤2(1 −√p) for any p ∈[0, 1].

Proof of Proposition H.2. Fix any N ≥1, α ≥0. By definition, for any π ∈Π,

L−

C(π) = n X i=1 max

0, log πD(yi | xi) π(yi | xi) −C

≥(log N −C)

i ∈[n]: log πD(yi | xi)

π(yi | xi) ≥log N

= n(log N −C) · d CovN(πD ∥π), where we recall that (see Eq. (28))

d CovN(πD ∥π) = 1 n t ∈[n]: πD(yt | xt)

π(yt | xt) ≥N

.

Then, by Lemma H.2 (stated and proved below), it holds that with probability at least 1 −δ, for any π ∈Π, d CovN(πD ∥π) ≥1

2Cove2αN(πD ∥π) −8 log(2N∞(Π, α)/δ) n.

Rescaling N ←e−2αN and reorganizing completes the proof.

Lemma H.2. For any model π, π′, we consider the quantities d CovN(π′ ∥π) = 1 n t ∈[n]: π′(yt | xt)

π(yt | xt) ≥N

, CovπD

N (π′ ∥π) = PπD π′(y | x)

π(y | x) ≥M

.

Fix α ≥0 and model π. With probability at least 1 −δ, for any π ∈Π, it holds that d CovN(π ∥π) ≥1

2CovπD e2αN(π ∥π) −8 log(2N∞(Π, α)/δ)

n.

Similarly, with probability at least 1 −δ, for any π ∈Π, it holds that d CovN(π ∥π) ≤2 CovπD e−2αN(π ∥π) + 8 log(2N∞(Π, α)/δ)

n.

Proof of Lemma H.2. We only prove the first inequality. Let Π′ ⊆Π be an α-covering of Π with |Π′| = N∞(Π, α). Then, by Freedman’s inequality (Lemma F.2) and union bound, it holds that with probability at least 1 −δ, for any π′ ∈Π′, d CoveαN(π ∥π′) ≥1

2CovπD eαN(π ∥π′) −εstat, where we denote εstat = 8 log(2|Π′|/δ) n. Then, note that for any π ∈Π, there exists π′ ∈Π′ such that | log π(y | x) −log π′(y | x)| ≤α for ∀x, y, we know t ∈[n]: π(yt | xt)

π′(yt | xt) ≥eαN

⊆ t ∈[n]: π(yt | xt)

π(yt | xt) ≥N and hence d CoveαN(π ∥π′) ≤d CovN(π ∥π). Similarly, CovπD eαN(π ∥π′) ≥CovπD e2αN(π ∥π). Hence, under the above event, it holds that d CovN(π ∥π) ≥d CoveαN(π ∥π′) ≥1

2CovπD eαN(π ∥π′) −εstat

≥1

2CovπD e2αN(π ∥π) −εstat.

Since π ∈Π is arbitrary, the proof is hence completed.

<!-- Page 42 -->

H.2 Proof of Theorem E.1 (Coverage for MLE with Convex Classes)

Let α ≥0, N ′ ≥1, N ≥2e2αN ′ be fixed. By definition and concavity of θ 7→πθ(y | x), we know θ⋆is an optimal solution of the following concave problem θ⋆∈arg max θ∈Θ

E(x,y)∼πD[log πθ(y | x)].

Hence, the optimality of θ⋆implies that

⟨θ −θ⋆, −EπD[∇log πθ⋆(y | x)]⟩≥0, ∀θ ∈Θ.

Consider the function F(θ) = EπD h πθ(y|x) πθ⋆(y|x)

i

−1, which is also concave by Assumption E.1. For any θ ∈Θ,

⟨θ −θ⋆, −∇F(θ⋆)⟩= θ −bθ, −EπD

∇πθ⋆(y | x)

πθ⋆(y | x)

=

D θ −bθ, −EπD[∇log πθ⋆(y | x)]

E

≥0.

Therefore, F attains its maximum over Θ at θ⋆, i.e., F(θ) ≤F(θ⋆) = 0 for any θ ∈Θ.

Similarly, it is also clear that θ 7→Pn i=1 log πθ(yi | xi) is concave, and hence bπ = πbθ, where bθ ∈Θ satisfies * θ −bθ, n X i=1

−∇log πbθ(y i | x i)

+

≥0, ∀θ ∈Θ.

In particular, we consider the function bF(θ):= n X i=1 πθ(yi | xi)

πbθ(yi | xi) −1

.

Under Assumption E.1, bF is concave, and for any θ ∈Θ,

D θ −bθ, −∇bF(bθ)

E

=

* θ −bθ, − n X i=1

∇πbθ(yi | xi)

πbθ(yi | xi)

+

=

* θ −bθ, n X i=1

−∇log πbθ(y i | x i)

+

≥0.

Therefore, bF attains its maximum over Θ at bθ, and in particular, bF(θ⋆) ≤bF(bθ) = 0. This implies n X i=1 πθ⋆(yi | xi)

bπ(yi | xi) −log πθ⋆(yi | xi)

bπ(yi | xi) −1

≤ n X i=1 log bπ(y i | x i) − n X i=1 log πθ⋆(y i | x i). (63)

In the following, we use that N ≥2. Note that x −log x −1 ≥0 for any x > 0, and x 7→x −log x −1 is increasing for x ≥1. Therefore, Eq. (63) implies that

(N −log N −1) · n · d CovN(πθ⋆∥bπ) ≤bLn(bπ) −bLn(πθ⋆). (64)

Then, by Lemma H.2, we have with probability at least 1 −δ, for all π ∈Π, d CovN(πθ⋆∥π) ≥1

2 · PπD πθ⋆(y | x)

π(y | x) ≥e2αN

−log(N∞(Π, α)/δ)

n, ∀π ∈Π.

Further, by Lemma F.3, the following holds with probability at least 1 −δ: For any θ ∈Θ, bLn(πθ) −bLn(πθ⋆) = n X i=1 log πθ(yi | xi)

πθ⋆(yi | xi)

≤n log EπD πθ(y | x)

πθ⋆(y | x)

+ inf ϵ≥0{log(N∞(Π, ϵ)/δ) + 2nϵ}

≤inf ϵ≥0{log(N∞(Π, ϵ)/δ) + 2nϵ},

<!-- Page 43 -->

where we use EπD h πθ(y|x) πθ⋆(y|x)

i

= F(θ)+1 ≤1 for any θ ∈Θ. By union bound, we have shown that with probability at least 1 −2δ,

PπD πθ⋆(y | x)

bπ(y | x) ≥e2αN

≲log(N∞(Π, α)/δ)

n + 1

N inf ϵ≥0 log N∞(Π, ϵ)

n + ϵ

.

Note that

Cove2αNN ′(bπ) = PπD πD(y | x)

bπ(y | x) ≥e2αNN ′

≤PπD πθ⋆(y | x)

bπ(y | x) ≥e2αN

+ PπD πD(y | x)

πθ⋆(y | x) ≥N ′

.

Therefore, the proof is completed by rescaling N ←Ne−2α/N ′, δ ←δ

2 and combining the inequalities above.

H.3 Proofs for Supporting Results

Proof of Proposition 4.1 (a). Assume that B ≥log(5n) and n ≥d ≥2. Consider X =⊥, Y = [d] and let the feature map be given by ϕ(y) = Bey for y ∈Y, where (e1,..., ed) is the coordinate basis of Rd. We consider Θ = θ ∈Rd: ∥θ∥∞≤1

, and we set θ⋆= log(4n)

2B ·



e1 − d X j=2 ej



.

Then it holds that πD(1) = 4n d −1 + 4n, πD(y) = 1 d −1 + 4n, ∀y > 1.

Given the dataset D = {y1, · · ·, yn}, we consider the random variables ny = |{i ∈[n]: yi = y}|. Note that under D ∼πD, it holds that

E

"X y>1 ny

#

= E

" n X t=1

I{y t̸ = 1}

#

≤ n(d −1) d −1 + 4n ≤d −1

4.

In particular, with probability at least 0.5, it holds that P y>1 ny ≤d−1

2, i.e., the set Y0:= {y ∈[d]: ny = 0} has cardinality at least d−1

2.

In the following, we condition on this event analyze the MLE bθ. By the definition of MLE, bθ ∈arg max θ∈Θ

−n log



X y∈[d]

eBθy



+ B

X y∈[d]

nyθy.

We denote py:= πbθ(y) = eB bθy P i∈[d] eB bθi. Then, the KKT conditions imply that for each y ∈[d], either py = ny n, or bθy = −1 and py ≥ny n, or bθy = 1 and py ≤ny n. In particular, for any y ∈Y0, py > 0 = ny n, and hence it must hold that bθy = −1. Then, because P y∈[d] py = 1 = P y∈[d]

ny n, there must exist j ∈[d] such that pj < nj n, and by the KKT condition we have bθj = 1. Therefore, for any y ∈Y0, it holds that py ≤ e−B e−B+eB ≤ 1 e2B, and in particular πD(y)

πbθ(y) ≥ e2B 4n+d−1 ≥eB. This implies that

CoveB(πbθ) = PπD πD(y)

πbθ(y) ≥eB

≥PπD(Y0) ≥ d −1 2(d −1 + 4n) ≥d −1 10n.

This is the desired lower bound.

<!-- Page 44 -->

Proof of Proposition 4.1 (b). Let ϵ = c0 q d n and p = c0ϵ2 log N for a sufficiently small absolute constant c0 > 0,

X = {0, 1, · · ·, d}, Y = {0, 1}, and the distribution µ be given by µ(0) = p, µ(1) = · · · = µ(d) = 1−p d.

Let the data distribution πD be πD(· | i) = Ber(1/2) for i ∈[d] and πD(1 | 0) = 1. For any θ ∈Θ:= {+1, −1}d, we define πθ as πθ(· | 0) = Ber

1

N

, πθ(· | i) = Ber

1 + ϵθi

2

, ∀i ∈[d].

Consider the model class Π = {πD} ∪{πθ: θ ∈Θ}. Note that for any θ ∈Θ, CovN(πD ∥πθ) ≥µ(0) = p.

Then, we can calculate bLn(πθ) −bLn(πD) = −C(0, 1) log N +

X i∈[d]

[C(i, 1) log(1 + ϵθi) + C(i, 0) log(1 −ϵθi)], where we denote C(x, y) = |{t ∈[n]: (xt, yt) = (x, y)}|. We further write C(x) = C(x, 0) + C(x, 1). Taking maximum over θ ∈Θ = {−1, 1}d gives max θ∈Θ bLn(πθ) −bLn(πD)

= −C(0) log N + 1

2

X i∈[d]

|C(i, 1) −C(i, 0)| log 1 + ϵ

1 −ϵ + C(i) log(1 −ϵ2)

≥−C(0) log N −nϵ2 + ϵ

2

X i∈[d]

|C(i, 0) −C(i, 1)|,

In the following, we denote ∆i = C(i, 1) −C(i, 0) and ∆:= P i∈[d] ∆i. Note that for any i ∈[d], condition on C(i), ∆i is a sum of C(i) i.i.d. random variables drawn from Unif({−1, 1}), and hence

E[(∆i)2 | C(i)] = C(i), E[|∆i| | C(i)] ≥ r

C(i)

2, where we apply Khintchine’s inequality. In addition, we note that C(i) ∼B(n, q) is a binomial random variable, where q = 1−p d. Hence, E[C(i)] = nq, and to lower bound E p

C(i), we invoke Lemma H.3 (stated and proven in the sequel) to show that E p

C(i) ≥√nq

1 −1−q 2nq

≥

√nq

2 (because n ≥2d and hence nq ≥1). Therefore,

E[∆] =

X i∈[d]

E[|∆i|] ≥ 1 √

2

X i∈[d]

E[ p

C(i)] ≥d√nq

2 √

2, and we can also bound E(∆)2 ≤d P i∈[d] E(∆i)2 = d P i∈[d] E[C(i)] = dn(1 −p) = d2nq. Then, by Paley- Zygmund inequality, it holds that

P(∆> b E[∆]) ≥(1 −b)2 (E[∆])2

E[∆2] ≥(1 −b)2

8, ∀b ∈[0, 1].

We choose b = 1 −

√

0.88 to be a numeric constant so that P(∆> b E[∆]) ≥0.11. By Markov’s inequality, it also holds that P(C(0) ≥100np) ≤0.01. In the following, we condition on the event E = {∆> b E[∆]} ∩{C(0) ≤100np} (note that P(E) ≥0.1). Then, we have max θ∈Θ bLn(πθ) −bLn(πD) ≥−C(0) log N −nϵ2 + ϵ

2∆> bϵ √ nd 8 −100np log N −nϵ2 ≥0, as long as c0 ≤10−4. This implies that there exists θ ∈Θ such that bπ = πθ, and hence CovN(bπ) ≥p. This is the desired lower bound.

Lemma H.3. For non-negative random variable Z, it holds that E[

√

Z] ≥ p

E[Z]

1 − Var[Z] 2(E[Z])2

.

Proof of Lemma H.3. Note that the inequality √u ≥3u−u2

2 holds for u ≥0. Setting u = Z E[Z] and taking expectation completes the proof.

<!-- Page 45 -->

I Proofs for Autoregressive Linear Models

I.1 Organization

This section contains proofs for all of the results in Sections 4 to 6 concerning autoregressive linear models (3). We begin with the proof of Theorem 4.2 (MLE for autoregressive linear models). We then present the proofs for various SGD methods, starting with vanilla SGD (Proposition 5.1; upper and lower bounds), followed by normalized SGD (Theorem 5.1), test-time training (Theorem 6.1), and expert-guided gradient normalization (Theorem 6.2). The final subsection provides an additional lower bound, showing that the dependence on the parameter σ2

⋆is necessary in high dimension.

Throughout this section, all upper bounds are derived under Assumptions 2.1 and 2.2, i.e., we assume that Θ ⊆B2(1), ϕ: X × V⋆→B2(R), and πD = πθ⋆is realized by some parameter θ⋆∈Θ.

Notation and preliminaries. For any f: X × V⋆→R and dataset D = {(xi, yi

1:H)}i∈[n], we write bED[f]:= 1 n n X i=1 f(x i, y i 1:H),

For notational simplicity, we denote ϕθ(x, y1:h−1) = Eyh∼πθ(·|x,y1:h−1)[ϕ(x, y1:h)], and ϕ⋆(x, y1:h):= ϕ(x, y1:h) −ϕθ⋆(x, y1:h−1),

VarπD(x, y1:h−1):= Eyh∼πθ(·|x,y1:h−1)∥ϕ⋆(x, y1:h)∥2.

Then, by definition,

∇log πθ(y1:H | x) =

H X h=1 ϕ(x, y1:h) −ϕθ(x, y1:h−1)

=

H X h=1 ϕ⋆(x, y1:h) +

H X h=1 ϕθ⋆(x, y1:h−1) −ϕθ(x, y1:h−1)

, (65)

and it holds that σ2

⋆= EπD hPH h=1 VarπD(x, y1:h−1)

i

.

In addition, we write ϵθ(x, y1:h−1) = DKL(πD(· | x, y1:h−1) ∥πθ(· | x, y1:h−1)). (66)

For any θ ∈Θ, the key quantity of interest is Dseq,N(πD ∥πθ), defined via

Dseq,N(πD ∥πθ) = EπD min

( log N,

H X h=1

DKL(πD(· | x, y1:h−1) ∥πθ(· | x, y1:h−1))

)

= EπD min

( log N,

H X h=1 ϵθ(x, y1:h−1)

)

.

By Proposition D.10, it holds that CovN(πθ) ≤ 2 log N−1Dseq,N(πD ∥πθ).

Further, by concavity, we have ϵθ(x, y1:h−1) ≤⟨ϕθ(x, y1:h−1) −ϕθ⋆(x, y1:h−1), θ −θ⋆⟩. (67)

By Lemma F.4, it holds that

∥ϕθ⋆(x, y1:h−1) −ϕθ(x, y1:h−1)∥≤4 p

VarπD(x, y1:h−1) · ϵθ(x, y1:h−1) + 8Bϵθ(x, y1:h−1). (68)

<!-- Page 46 -->

I.2 Proof of Theorem 4.2 (Coverage for MLE for Autoregressive Linear Models)

We prove the following slightly stronger result. Theorem 4.2 follows immediately by combining Theorem I.1 and Proposition D.10.

Theorem I.1. Suppose that Assumption 2.2 holds. Then the MLE bπ achieves

ED[Dseq,N(πD ∥bπ)] ≲ r σ2⋆log N n + B2 log N n, for any parameter N ≥2, where the divergence Dseq,N(· ∥·) is defined in Proposition D.10.

We begin with two central technical lemmas, which are proven in the sequel. The first lemma is a consequence of the fact that the MLE bπ = πbθ maximizes the empirical likelihood, i.e., bθ = arg max θ∈Θ bED[log πθ(y1:H | x)], (69)

where we recall that for any dataset D = {(xi, yi

1:H)}i∈[n], we write bED[f]:= 1 n

Pn i=1 f(xi, yi

1:H) for any f: X × V⋆→R. Lemma I.1 shows that in expectation, a sum of per-step conditional KL divergences between πD and bπ is bounded (this does not imply a bound on sequence-level KL divergence, since bθ is dependent on the data D).

Lemma I.1. Recall that we denote ϵθ(x, y1:h−1) = DKL(πD(· | x, y1:h−1) ∥πθ(· | x, y1:h−1)). Further, define

E1:= bED

" H X h=1 ϵbθ(x, y1:h−1)

#

(70)

Then it holds that E[E1] ≤2σ⋆ √n.

Define A:= log N. The next lemma is a uniform convergence-like argument which shows that the quantity E1 above—when truncated at a certain level A—concentrates around its expectation up to a multiplicative factor. This argument is inspired by the fractional covering method introduced in Chen et al. (2024a); Chen and Rakhlin (2025).

Lemma I.2. Fix any ∆∈(0, 1 200B ], δ ∈(0, 1), and let J = exp 1

∆2 + 2 log(1/δ). Let Θ′:= {θ1, · · ·, θJ}, where θ1, · · ·, θJ ∼N(0, ∆2I) are sampled i.i.d. Then the following holds with probability at least 1 −δ over the randomness of Θ′ and D:

(1) For any j ∈[J], it holds that

EπD min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

≤2bED min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

+ 8A log(4J/δ)

n.

(2) There exists j ∈[J] such that

EπD min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

≤2 EπD min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

+ C∆2σ2

⋆, (71)

and bED min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

≤2bED min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

+ C∆2bED

" H X h=1

VarπD(x, y1:h−1)

#

,

(72)

where C = 1000 is a numeric constant.

<!-- Page 47 -->

Above, the distribution of πθ under θ ∼N(0, ∆2I) can be viewed as a fractional cover for Π in the sense of Chen et al. (2024a). In particular, working with the fractional cover offers the following technical advantages:

• The fractional cover N(0, ∆2I) incurs error σ2 ⋆∆2 (see Lemma I.3) that depends only on the variance at the ground-truth parameter θ⋆. This contrasts with classical coverings, which enforce a uniform bound for all θ ∈Θ.

• For Θ = Bd 2(1), the L∞covering number of Π (cf. Definition 4.1) scales with the dimension d. A standard approach to deriving dimension-independent bounds is to apply symmetrization techniques and use a data-dependent L2 covering to show uniform convergence. In contrast, our fractional-covering approach avoids the (technically subtle) symmetrization step because the cover {θ1,..., θJ} ∼N(0, ∆2I) is drawn independently of the dataset D.

Completing the proof. Equipped with the lemmas above, we complete the proof as follows. First, we condition on the success event E of Lemma I.2, and let j ∈[J] be an index such that (71) and (72) hold. Then, we can upper bound (recall that A = log N and Dseq,N(· ∥·) is defined in Proposition D.10)

Dseq,N πD ∥πbθ

= EπD min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

≤2 EπD min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

+ C∆2σ2

⋆

≤4bED min

(

A,

H X h=1 ϵθj(x, y1:h−1)

)

+ 16A log(4J/δ)

n + C∆2σ2

⋆

≤8bED min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

+ 4C∆2bED

" H X h=1

VarπD(x, y1:h−1)

#

+ 16A log(4J/δ)

n + C∆2σ2

⋆.

where the first inequality uses (71), the second inequality uses Lemma I.2 (1), and the third inequality uses (72). Therefore, we denote σ2(D):= bED hPH h=1 VarπD(x, y1:h−1)

i

, and we have shown that for any δ ∈(0, 1), any ∆∈(0, 1 200B ], it holds that

PD∼πD

Dseq,N πD ∥πbθ

≥C1

E1 + ∆2σ2(D) + ∆2σ2

⋆+ A n

1

∆2 + log(1/δ)

≤δ, where C1 > 0 is an absolute constant.

Since δ ∈(0, 1) is arbitrary, integrating the tail inequality above yields the following bound on the expected value:

E

Dseq,N πD ∥πbθ

≤C1

E[E1] + ∆2 E[σ2(D)] + ∆2σ2

⋆+ A n

1

∆2 + 1

≤2C1 r σ2⋆ n + ∆2σ2

⋆+ A n∆2

!

, ∀0 < ∆≤ 1 200B.

Choosing ∆= min

1 200B,

A σ2

⋆n

1/4 completes the proof. The coverage upper bound follows immediately from Proposition D.10.

<!-- Page 48 -->

I.2.1 Proofs for Supporting Lemmas

Proof of Lemma I.1. Recall that bπ = πbθ, where bθ = arg maxθ∈Θ bED[log πθ(y1:H | x)]. Then by concavity of the log-likelihood, we have that

D bED

∇log πbθ(y1:H | x)

, θ −bθ

E

≤0, ∀θ ∈Θ.

Using the expression (65) and θ⋆∈Θ, we know bED

"* H X h=1 ϕ(x, y1:h) −ϕbθ(x, y1:h−1)

, θ⋆−bθ

+#

≤0.

Therefore, combining the inequality above with Eq. (67), we have bED

" H X h=1 ϵbθ(x, y1:h−1)

#

= bED

" H X h=1

DKL(πD(· | x, y1:h−1) ∥bπ(· | x, y1:h−1))

#

≤bED

" H X h=1

D ϕθ⋆(x, y1:h−1) −ϕbθ(x, y1:h−1), θ⋆−bθ

E#

≤bED

" H X h=1

D ϕθ⋆(x, y1:h−1) −ϕ(x, y1:h), θ⋆−bθ

E#

≤2 bED

" H X h=1 ϕ⋆(x, y1:h)

## =: E′

1, where we recall that ϕ⋆(x, y1:h):= ϕ(x, y1:h)−ϕθ⋆(x, y1:h−1). By definition, it holds that EπD[ϕ⋆(x, y1:h) | x, y1:h−1] = 0, and hence

E(E′

1)2 = E bED

" H X h=1 ϕ⋆(x, y1:h)

#

2

= 1 n EπD

H X h=1 ϕ⋆(x, y1:h)

2

= 1 n EπD

" H X h=1

∥ϕ⋆(x, y1:h)∥2

#

= σ2

⋆ n.

This gives the desired upper bound.

Proof of Lemma I.2. By Freedman’s inequality (Lemma F.2) and the union bound, it follows that (1) holds with probability at least 1 −δ

2. In the remainder of the proof, we prove (2).

Define the following weight function α = αbθ: X × V⋆→[0, 1]:9 αbθ(x, y1:h−1) =

  

 

1, P j≤h−1 ϵbθ(x, y1:j) ≤A, 0, P j<h−1 ϵbθ(x, y1:j) ≥A, A−P j<h−1 ϵbθ(x,y1:j) ϵbθ(x,y1:h−1), otherwise.

We also define F(a, b) = |a −b| −1

2a. The properties of F(·, ·) and the weight function α are summarized in Lemma I.4 (stated and proven in the sequel).

9Inspired by the analysis here, we also adopt this weight function in the SGD update (26) with the truncated stochastic gradient estimator.

<!-- Page 49 -->

Then, by Lemma I.4, it holds that for any θ ∈Θ,

EπD min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

≤2 EπD min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

+ 2 EπD

" H X h=1 α(x, y1:h−1)F ϵbθ(x, y1:h−1), ϵθ(x, y1:h−1)

#

, and bED min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

≤2bED min

(

A,

H X h=1 ϵbθ(x, y1:h−1)

)

+ bED

" H X h=1 α(x, y1:h−1)F ϵbθ(x, y1:h−1), ϵθ(x, y1:h−1)

#

,

Therefore, it remains to control the error PH h=1 α(x, y1:h−1)F ϵbθ(x, y1:h−1), ϵθ(x, y1:h−1)

under both EπD[·] and bED[·]. We next state the following lemma (proven in the sequel), which leverages the structure of Gaussian distribution. This result can be viewed as a fractional covering number bound (Chen et al., 2024a) and hence generalizes the argument of Chen and Rakhlin (2025, Proposition C.4).

Lemma I.3. For any K ≥1, ∆∈(0, 1 100KB ], θ ∈B2(1), distributions ρ1, · · ·, ρK over Z:= X × V⋆, and weight function α: Z →[0, 1], it holds that

−log Pθ′∼N(0,∆2)

∀i ∈[K], Ez∼ρi α(z)F(ϵθ(z), ϵθ′(z)) ≤70K2∆2 Ez∼ρi VarπD(z)

≤1

∆2 + 2, where we recall that F(a, b) = |a −b| −1

2a.

In the following, we apply Lemma I.3 with K = 2, parameter θ = bθ, weight function α, and the distributions ρ1, ρ2 defined as follows:

• Let ρ1 be the distribution of x′ = (x, y1:h−1) under x ∼µ, y1:H ∼πD(· | x) and h ∼Unif([H]).

• Let ρ2 be the distribution of x′ = (xt, yt 1:h−1) under t ∼Unif([n]) and h ∼Unif([H]).

By definition, it holds that

Ez∼ρ1 α(z)F(ϵθ(z), ϵθ′(z)) = 1

H EπD

" H X h=1 α(x, y1:h−1)F ϵbθ(x, y1:h−1), ϵθ(x, y1:h−1)

#

,

Ez∼ρ1 VarπD(z) = 1

H EπD

" H X h=1

VarπD(x, y1:h−1)

#

= σ2

⋆ H,

Ez∼ρ2 α(z)F(ϵθ(z), ϵθ′(z)) = 1

H bED

" H X h=1 α(x, y1:h−1)F ϵbθ(x, y1:h−1), ϵθ(x, y1:h−1)

#

,

Ez∼ρ2 VarπD(z) = 1

H bED

" H X h=1

VarπD(x, y1:h−1)

#

.

Now, consider the following set for any θ ∈Θ:

Θ+ θ:=

∀i ∈{1, 2}, Ez∼ρi α(z)F(ϵθ(z), ϵθ′(z)) ≤300∆2 Ez∼ρi VarπD(z)

.

By Lemma I.3, it holds that q(θ):= Pθ′∼N(0,∆2I)(θ′ ∈Θ+ θ) ≥exp

−1

∆2 −2

, ∀θ ∈Θ, ∀∆∈(0, 1 200B ].

<!-- Page 50 -->

Therefore, we have

P

∀j ∈[J], θj̸ ∈Θ+ bθ | bθ

= Pθ1,···,θJ∼N (0,∆2I)

∀j ∈[J], θj̸ ∈Θ+ bθ

≤(1 −q(bθ))J ≤exp

−Jq(bθ)

≤δ

2, and hence P

∃j ∈[J], θj ∈Θ+ bθ

≥1 −δ

## 2 The proof of

Lemma I.2 (2) is thus completed, as Eq. (71) and

Eq. (72) hold for any j ∈[J] such that θj ∈Θ+ bθ.

Proof of Lemma I.3. We first fix any h ∈[H] and z = (x, y1:h−1) ∈X × Vh−1 and analyze the behavior of log πθ′(yh | z) under θ′ ∼N(θ, ∆2I).

By definition, we have πθ′(yh | z) ∝yh πθ(yh | z) · exp(⟨θ′ −θ, ϕ(z, yh)⟩), i.e., log πθ′(yh | z) −log πθ(yh | z) = ⟨θ′ −θ, ϕ(z, yh)⟩−log Eyh∼πθ(·|z) exp(⟨θ′ −θ, ϕ(z, yh)⟩).

Therefore, ϵθ(z) −ϵθ′(z) = DKL(πD(yh = · | z) ∥πθ(yh = · | z)) −DKL(πD(yh = · | z) ∥πθ′(yh = · | z))

= EπD(·|z)⟨θ′ −θ, ϕ(z, yh)⟩−log Eyh∼πθ(·|z) exp(⟨θ′ −θ, ϕ(z, yh)⟩)

= ⟨θ′ −θ, ϕθ⋆(z) −ϕθ(z)⟩−log Eyh∼πθ(·|z) exp

⟨θ′ −θ, ϕ(z, yh) −ϕθ(z)⟩

, where we recall that ϕθ(z) = Eyh∼πθ(·|z)[ϕ(z, yh)].

In the following, we denote ϕθ(z, yh):= ϕ(z, yh) −ϕθ(z), and

E+ θ′(z):= log Eyh∼πθ(·|z) exp(⟨θ′ −θ, ϕθ(z, yh)⟩),

E− θ′(z):= ⟨θ′ −θ, ϕθ⋆(z) −ϕθ(z)⟩.

We first bound E+ θ′(z). By definition, we have E+ θ′(z) = DKL(πθ(· | z) ∥πθ′(· | z)) ≥0. Further, using Jensen’s inequality, for any z ∈Z, we have

Eθ′∼N(θ,∆2I)

E+ θ′(z)

≤log Eθ′∼N (θ,∆2I) Eyh∼πθ(·|z)[exp(⟨θ′ −θ, ϕθ(z, yh)⟩)]

= log Eyh∼πθ(·|z) exp

1

2∆2∥ϕθ(z, yh)∥2

≤∆2 Eyh∼πθ(·|z)∥ϕθ(z, yh)∥2, where the last inequality follows from et ≤1 + 2t for t ∈[0, 1]. Further, using Lemma F.4, we have

Eyh∼πθ(·|z)∥ϕθ(z, yh)∥2 = Eyh∼πθ(·|z)∥ϕ(z, yh) −ϕθ(z)∥2

≤3 Ey∼πD(·|z)∥ϕ(z, yh) −ϕθ⋆(z)∥2 + 16B2DKL(πD(· | z) ∥πθ(· | z))

= 3VarπD(z) + 16B2ϵθ(z).

Next, we bound |E− θ′(z)|. Under θ′ ∼N(θ, ∆2I), it is clear that ⟨θ′ −θ, ϕθ⋆(z) −ϕθ(z)⟩∼N(0, ∆2∥ϕθ⋆(z) − ϕθ(z)∥2) for any fixed z. Therefore, it holds that

Eθ′∼N(θ,∆2I)

E− θ′(z)

= r

2 π ∆· ∥ϕθ⋆(z) −ϕθ(z)∥

≤∆·

4 p

VarπD(z) · ϵθ(z) + 8Bϵθ(z)

≤

1

8K + 8B∆ ϵθ(z) + 32K∆2VarπD(z),

<!-- Page 51 -->

where the second line uses Eq. (68).

Combining the inequalities above and taking expectation of z ∼ρi, we know that for i ∈[K], it holds that

Eθ′∼N(θ,∆2I)

Ez∼ρi α(z)E+ θ′(z)

≤∆2 Ez∼ρi

3VarπD(z) + 16B2α(z)ϵθ(z)

,

Eθ′∼N(θ,∆2I)

Ez∼ρi α(z)

E− θ′(z)

≤Ez∼ρi

32K∆2VarπD(z) + 1

8K + 8B∆ α(z)ϵθ(z)

, and hence by Markov’s inequality and ∆≤ 1 100KB, it holds that p:= Pθ′∼N (θ,∆2I)(θ′̸ ∈Θ−) ≥1 2, where we denote Θ−= ∪i∈[K]Θ− i, and

Θ− i:= θ′ ∈Rd: Ez∼ρi α(z)|ϵθ(z) −ϵθ′(z)| ≥Ez∼ρi

(6K + 64K2)∆2VarπD(z) + 1

2α(z)ϵθ(z)

.

Note that DKL

N(θ, ∆2I) ∥N(0, ∆2I)

= ∥θ∥2

2∆2 ≤ 1 2∆2. Hence, by data-processing inequality, we can bound q:= Pθ′∼N(0,∆2I)(θ′̸ ∈Θ−) as

1 2∆2 ≥DKL

N(θ, ∆2I) ∥N(0, ∆2I)

≥DKL(Ber(p) ∥Ber(q))

= p log p q + (1 −p) log 1 −p

1 −q ≥1 2 log(1/q) −log 2.

This implies that −log q ≤ 1 ∆2 + 2, giving the desired result.

Lemma I.4. Suppose that a1, · · ·, aH, b1, · · ·, bH ≥0, A ≥0. Define F(a, b) = |a −b| −1

2a. Let αh =

  

 

1, P j≤h aj ≤A, 0, P j<h aj > A, A−P j<h aj ah, otherwise.

Then clearly αh ∈[0, 1] ∀h ∈[H], and it holds that PH h=1 αhah = min n

A, PH h=1 ah o

, and min

(

A,

H X h=1 ah

)

≤2 min

(

A,

H X h=1 bh

)

+ 2

H X h=1 αhF(ah, bh), and min

(

A,

H X h=1 bh

)

≤2 min

(

A,

H X h=1 ah

)

+

H X h=1 αhF(ah, bh).

Proof of Lemma I.4. Fix the sequence a1, · · ·, aH. We first prove that

H X h=1 αhah = min

(

A,

H X h=1 ah

)

. (73)

To do so, we consider two cases.

Case 1: PH h=1 ah ≤A. In this case, αh = 1∀h ∈[H], and the equation holds trivially.

Case 2: PH h=1 ah > A. In this case, we let ℓ∈[H] be the maximal index such that αℓ> 0. Then, by definition, P j<ℓaj ≤A and P j≤ℓaj > A, and αℓ=

A−P j<ℓaj aℓ. Hence,

H X h=1 αhah = ℓ X h=1 αhah =

X j<ℓ aj + αℓaℓ= A.

<!-- Page 52 -->

We also note that from the proof above, we also know that for any sequence (c1, · · ·, cH) such that ch ≥ah for h ∈[H], we have min

(

A,

H X h=1 ch

)

≤

H X h=1 αhch. (74)

Equipped with these results, we prove the inequalities in the lemma statement. We note that

H X h=1 αhF(ah, bh) =

H X h=1 αh|ah −bh| −1

2

H X h=1 αhah, or equivalently,

H X h=1 αh|ah −bh| =

H X h=1 αhF(ah, bh) + 1

2 min

(

A,

H X h=1 ah

)

.

Therefore, min

(

A,

H X h=1 ah

)

=

H X h=1 αhah ≤min

(

A,

H X h=1 bh

)

+

H X h=1 αh|ah −bh|

= min

(

A,

H X h=1 bh

)

+

H X h=1 αhF(ah, bh) + 1

2 min

(

A,

H X h=1 ah

)

.

Re-organizing yields the first inequality. Similarly, we have min

(

A,

H X h=1 bh

)

≤min

(

A,

H X h=1

(ah + |ah −bh|)

)

≤

H X h=1 αh(ah + |ah −bh|)

= 3

2 min

(

A,

H X h=1 ah

)

+

H X h=1 αhF(ah, bh).

The proof is hence completed.

I.3 Proof of Proposition 5.1 (Vanilla SGD: Coverage Upper Bound)

We first invoke the following standard lemma.

Lemma I.5. Suppose that the sequence (θt, gt)t≥1 satisfies θt+1 = ProjΘ(θt + ηgt) for t ≥1. Then it holds that for any θ⋆∈Θ, T ≥1,

T X t=1

⟨−g t, θ t −θ⋆⟩≤∥θ⋆−θ0∥2

2η + η

2

T X t=1

∥g t∥2. (75)

Specializing Lemma I.5 to the SGD update (14) and taking expectation, we have

E

" T X t=1

⟨−∇log πθt(y t | x t), θ t −θ⋆⟩

#

≤2 η + η

2 E

" T X t=1

∥∇log πθt(y t | x t)∥2

#

. (76)

Note that (xt, yt) | θt ∼πD, and hence

E[∇log πθt(y t | x t) | θ t] = E(x,y)∼πD[∇log πθt(y | x)] = ∇θDKL(πD ∥πθ)|θ=θt.

<!-- Page 53 -->

Further, by convexity, it holds that for any θ ∈Θ,

G(θ):= EπD[⟨−∇log πθ(y | x), θ −θ⋆⟩] = ⟨∇θDKL(πD ∥πθ), θ −θ⋆⟩≥DKL(πD ∥πθ).

Therefore, we have

E

" T X t=1

DKL(πD ∥πθt)

#

≤E

" T X t=1

G(θ t)

#

≤2 η + η

2 E

" T X t=1

E(x,y)∼πD∥∇log πθt(y | x)∥2

#

.

On the other hand, using the fact that log πθ(y | x) is concave and (HB2)-smooth (i.e., −HB2I ⪯∇2 log πθ(y | x) ⪯0),

∥∇log πθ(y | x) −∇log πθ⋆(y | x)∥2 ≤HB2 · ⟨θ −θ⋆, ∇log πθ⋆(y | x) −∇log πθ(y | x)⟩

Taking expectation of (x, y) ∼πD and using the fact that EπD[∇log πθ⋆(y | x)] = 0, we have

EπD∥∇log πθ(y | x) −∇log πθ⋆(y | x)∥2 ≤HB2 · G(θ), ∀θ ∈Θ.

Further, note that EπD∥∇log πθ⋆(y | x)∥2 = σ2

⋆, it holds that

EπD∥∇log πθ(y | x)∥2 ≤2σ2

⋆+ 2HB2 · G(θ), ∀θ ∈Θ. (77)

Combining the inequalities above, we can conclude that

E

" T X t=1

G(θ t)

#

≤2 η + ηHB2 E

" T X t=1

G(θ t)

#

+ ηTσ2

⋆.

We conclude that as long as η ≤ 1 2HB2, it holds

4 η + 2ηTσ2

⋆≥E

" T X t=1

G(θ t)

#

≥E

" T X t=1

DKL(πD ∥πθt)

#

.

This is the desired upper bound.

Proof of Lemma I.5. A standard result (e.g., Hazan (2016)) is that because the projection operator ProjΘ is an contraction, we have that for all t ∈[T], the update satisfies

∥θ t −θ⋆∥2 −∥θ t+1 −θ⋆∥2

≥∥θ t −θ⋆∥2 −∥θ t + ηg t −θ⋆∥2

= 2η⟨−g t, θ t −θ⋆⟩−η2∥g t∥2.

(78)

Summing this inequality across steps t = 1, 2, · · ·, T, telescoping, and taking expectation, we have

T X t=1

⟨−g t, θ t −θ⋆⟩≤∥θ⋆−θ0∥2 −∥θ⋆−θT +1∥2

2η + η

2

T X t=1

∥g t∥2. (79)

This gives the desired upper bound.

I.4 Proof of Proposition 5.1 (Vanilla SGD: Coverage Lower Bound)

In the following, we construct X = [ 8 HB, +∞) ⊔{−, +}, V = {−1, 0, 1} and Θ = B2(1) with d = 2. We fix parameters B ≥B ≥1.

<!-- Page 54 -->

Construction of ϕ. We first construct a map v: X × V →R2 as follows. For any η ≥ 8 HB, we define αη = ηHB 2(ηHB−1) ≤5 8 and let v(η, 0) = [1; 0], v(η, 1) = [αη;

q

1 −α2η], v(η, −1) = [αη; − q

1 −α2η].

We further define v(+, a) = 1

B [Ba; 0], v(−, a) = 1

B [0; Ba] ∀a ∈V = {−1, 0, 1}.

For x ∈X, y1:h ∈Vh, we define ϕ(x, y1:h) = Bv(x, yh).10

Under this construction of ϕ, we then prove the lower bound by considering two cases based on the value of η.

Lemma I.6. Suppose that η ≥ 8 HB, log N ≤HB

8, and B ≥cB log(TH) for a large constant cB > 1. Then, with the distribution µ being supported on x = η and θ⋆= [1; 0], the following holds.

(1) The variance of such an instance is bounded: σ⋆≤1.

(2) There exists θ0 ∈Θ such that with probability at least 0.5, the SGD sequence (θt) satisfies CovN(πθt) ≥1−1

2T for all t ∈[T].

Lemma I.7. Suppose that η ≤ 8 HB, log N ≤HB

8, and B ≥B ≥cB log(TH) for a large constant cB > 1. Then, there exists distribution µ and θ⋆∈Θ such that the following holds.

(1) The variance of such an instance is bounded: σ⋆≤1.

(2) There exists θ0 ∈Θ such that with probability at least 0.5, the SGD sequence (θt) satisfies

CovN(πθt) ≥c min

1, HB T · B2 log N

, ∀t ∈[T].

The proof of Proposition 5.1 (lower bound) is then completed by combining Lemma I.6 and Lemma I.7.

Proof of Lemma I.6. Fix the parameter η ≥ 8 HB. We denote η:= η · HB and α = αη = η 2(η−1) ≤5 8. Denote v0 = [1; 0], v1 = [α;

p

1 −α2], v−1 = [α; − p

1 −α2].

Under our construction, we have πθ(yh | η, y1:h−1) = exp(B⟨θ, vyh⟩) P a∈V exp(B⟨θ, va⟩) =: Pθ(yh).

We study the SGD update starting from θ0 = v1. By definition, ϕ(η, y1:h) = Bv(η, yh), and hence

∇log πθ(y1:H | η) =

H X h=1

Bv(η, yh) − E a∼Pθ[Bv(η, a)]

= B

H X h=1 vyh − E a∼Pθ[va]

.

In the following, we denote bF(y1:H):= 1

H

H X h=1 vyh, F(θ):= E a∼πθ[va] =

P a∈V a exp(B⟨θ, va⟩) P a∈V exp(B⟨θ, va⟩).

Then, the SGD update can be written as u t = θ t + η bF(y t 1:H) −F(θ t)

, θ t+1 = ProjΘ(u t).

10In other words, for any θ ∈Θ, y1:H ∼πθ(· | x) are sampled i.i.d. with y ∼Pθ(· | x), where Pθ is defined as Pθ(a | x) = exp(B⟨v(x,a),θ⟩) P a′∈V exp(B⟨v(x,a′),θ⟩).

<!-- Page 55 -->

We make the following claims.

Claim 1. For a ∈{−1, 0, 1} and ∥θ −va∥≤ 1 16, it holds that 1 −Pθ(a) ≤2e−B/4 =: ϵ1 and hence ∥F(θ) −va∥≤2ϵ1.

Claim 2. Suppose that ϵ1 ≤min

1 4T H, 1 5HB2

. Then it holds that σ⋆≤1. Further, with probability at least 0.5, it holds that bF(yt 1:H) = e0 for all t ∈[T].

In the following, we condition on this event.

Claim 3. By definition, for a ∈{−1, 1}, we have ∥va + η(v0 −va)∥= η −1 and v−1 + v1 = η η−1v0.

Claim 4. Let ϵ = 16ϵ1. Suppose that ϵ ≤ 1 16. Then for a ∈{−1, 1}, if ∥θt −va∥≤ϵ, then it holds that ∥θt+1 −v−a∥≤ϵ.

Claim 5. Suppose that ϵ1 ≤ 1 2T H and log N ≤HB 8. Then CovN(πD ∥πθ) ≥1 − 1 2T for θ ∈Θ such that min{∥θ −v1∥, ∥θ −v−1∥} ≤ 1 16.

Combining the above claims, we know that there is a constant C such that as long as B ≥cB log(TH), it holds that σ⋆≤1. Further, under the success event of claim 2, it holds that for a ∈{−1, 1}, ∥θt −va∥≤ 1 16 for all t ∈[T] such that 2 | t −a. Therefore, by Claim 5, this gives CovN(πθt) ≥1

2 as long as log N ≤HB 8.

Proof for Claims 1-5. To prove Claim 1, we note that ⟨θ, va⟩≥1 −∥θ −va∥≥ 15 16 and for i̸ = a, ⟨θ, vi⟩≤⟨va, vi⟩+ ∥θ −va∥≤α + 1

16 ≤11 16. Therefore,

1 −Pθ(a) ≤

P i̸=a eB⟨θ,vi⟩ eB⟨θ,va⟩ ≤ 2 eB/4 = ϵ1.

This completes the proof of Claim 1.

Next, we prove Claim 2. Recall that θ⋆= [1; 0] = v0. By Claim 1, we know 1 −Pθ⋆(0) ≤ϵ1, and hence Vara∼Pθ⋆[va] ≤5ϵ1. This implies σ2

⋆= HB2Vara∼Pθ⋆[va] ≤5HB2ϵ1 ≤1.

We also know PπD(yh = 0 ∀h ∈[H]) = Pθ⋆(0)H ≥(1 −ϵ1)H ≥1 −Hϵ1. Therefore, taking the union bound, we know P(yt h = 0 ∀h ∈[H], t ∈[T]) ≥1 −THϵ1 ≥1

## 2 This completes the proof of

Claim 2.

Furthermore, for any θ such that min{∥θ −v1∥, ∥θ −v−1∥} ≤ 1 16, as long as log N ≤H(log(1 −ϵ1) −log(ϵ1)), we have

CovN(πD ∥πθ) ≥

1 −1 2n

I{H log πD(0) −H log πθ(0) ≥log N} ≥1 −1

2n.

In particular, this is ensured when log N ≤HB

## 8 This completes the proof of

Claim 5.

Claim 3 follows immediately from the definition of α, v0, v1 and v−1.

Finally, we prove Claim 4. Recall that ut:= θt + η bF(yt

1:H) −F(θt)

. Then it holds that

∥u t −(η −1)v−a∥= ∥u t −ηv0 + (η −1)va∥≤∥θ t −va∥+ η∥bF(y t 1:H) −v0∥+ η∥F(θ t) −va∥

≤ϵ + 2ηϵ1 =: ϵ′.

In particular, it holds that |∥ut∥−(η −1)| ≤ϵ′ and hence ∥ut∥≥η −1 −ϵ′ = (1 −2ϵ1)η −1 −ϵ ≥η

2 ≥1. Therefore, θt+1 = ProjΘ(ut) = ut ∥ut∥, and we can bound

∥θ t+1 −v−a∥= ut −(η −1)v−a

∥ut∥ + v−a η −1

∥ut∥−1

≤∥ut −(η −1)v−a∥

∥ut∥ + |η −1 −∥ut∥|

∥ut∥

≤ 2ϵ′

∥ut∥≤4ϵ′ η = 4 η ϵ + 8ϵ1 ≤ϵ.

<!-- Page 56 -->

Proof of Lemma I.7. We again denote η = HBη ≤8. We choose θ⋆= [ 1

2; 1 2], and let the distribution µ be supported on {−, +}:

µ(+) = 1 −µ(−) = min

(

1, BH

512enB 2 log N

)

.

Note that for x ∈{−, +}, πD(1 | x) = eB/2 e−B/2+1+eB/2, and hence 1 −πD(y1 = 1 | x) ≤2e−B/2. Therefore, similar to Case 1, we have the following claims.

Claim 1. Suppose that B ≥cB log(TH) for a large constant cB > 0. Then it holds that σ⋆≤1, and with probability at least 0.5, it holds that PT t=1 I{xt = +} ≤4Tµ(1), and yt h = 1 for all h ∈[H], t ∈[T].

In the following, we condition on this event. We choose r ≤1

2 such that erB = H 4 log N, and we let θ0 = [r −1 B; 1

4].

Claim 2. For any θ ∈Θ ⊂R2, it holds that 1 −Pθ(1 | +) ≤ 2 eθ[1]B (where w[1] denotes the first coordinate of a vector w ∈R2). Hence, when xt = +, using yt h ≡1, we have ∇log πθ(yt | xt)[2] = 0 and

0 ≤∇log πθ(y t | x t)[1] = HB(1 −Ea∼Pθ(·|+)[a]) ≤2HB(1 −Pθ(1 | +)) ≤4HB eθ[1]B.

Similarly, when xt = −, we have

∇log πθ(y t | x t)[1] = 0, 0 ≤∇log πθ(y t | x t)[2] ≤4HB eθ[2]B.

Then, combining the inequalities above with Claim 1, we can inductively show that for any t ∈[T], θ t[1] −θ

0[1] ≤

T X t=1

I{x t = +} · 4ηHB eθ0[1]B ≤T · µ(+)16eηB

BerB ≤µ(+) · 512eBn log N

BH ≤1

B.

Therefore, we have θt[1] ≤r for t ≤T. It remains to prove the following claim.

Claim 3. Suppose that eθ[1]B ≤ H 4 log N. Then it holds that CovN(πθ) ≥µ(+) 2.

To prove Claim 3, we note that similar to Claim 2, PπD(yh = 1 ∀h ∈[H] | x = +) ≥1

2. Further, log πD(y1 = 1 | +) ≥log(1 −2e−B/2) ≥−3e−B/2 and log πθ(y1 = 1 | +) ≤− 1 3eθ[1]B. Hence, for y⋆∈VH being y⋆ h = 1 for h ∈[H], it holds that log πD(y⋆| +) −log πθ(y⋆| +) ≥H ·

1

3eθ[1]B −3e−B/2

≥log N.

The immediately yields

CovN(πθ) ≥µ(+) · PπD(y = y⋆| x = +) ≥µ(+)

2.

I.5 Proof of Theorem 5.1 (Coverage for Normalized SGD)

We denote M:= log N. We analyze the normalized SGD iterates assuming λ ≥8BM and λη

M ≤ 1 16.

Denote eg(θ; D):= bg(θ; D) λ + ∥bg(θ; D)∥.

<!-- Page 57 -->

Then the normalized SGD update can be rewritten as θt+1 = ProjΘ(θ + ηeg(θt; Dt)). Specializing Lemma I.5 to the normalized SGD update and using Θ ⊆B2(1) yields

T X t=1

⟨−eg(θ t; D t), θ t −θ⋆⟩≤2 η + η

T X t=1

∥eg(θ t; D t)∥2.

Taking an expectation on both sides and noting that Dt ∼πD is generated independently, we have

E

" T X t=1

ED∼πD⟨−eg(θ t; D), θ t −θ⋆⟩

#

≤2 η + η E

" T X t=1

ED∼πD∥eg(θ t; D)∥2

#

. (80)

In what follows, we prove a number of upper and lower bounds for the expressions involving eg(θ; D) above, then combine them with Eq. (80) to complete the proof.

Intermediate bounds. Recall that we write ϵθ(x, y1:h−1) = DKL(πD(· | x, y1:h−1) ∥πθ(· | x, y1:h−1)). Also recall that we adopt the notation that for any function f and dataset D, we write bED[f]:= 1 |D|

P

(x,y1:H)∈D f(x, y1:H).

Denote (recall that Dseq,N(· ∥·) is defined in Proposition D.10)

ϵθ(D):= bED

" H X h=1 ϵθ(x, y1:h−1)

#

, ∆θ:= EπD min{M, ϵθ(D)}.

Using the key structural result in Proposition D.10 (recall M:= log N), we can bound the coverage in terms of the expected sum of stopped KL divergences as follows:

CovN(πθ) ≤ 2 M −1Dseq,N(πD ∥πθ) = 2 M −1 EπD min

(

M,

H X h=1 ϵθ(x, y1:h−1)

)

≤ 2 M −1 ED∼πD min

(

M, bED

" H X h=1 ϵθ(x, y1:h−1)

#)

= 2 M −1∆θ.

(81)

Therefore, it remains to derive upper bounds on ∆θ for θ ∈{θ1, · · ·, θT}.

Lemma I.8. Suppose that λ ≥8BM. It holds that for any θ ∈Θ,

EπD∥eg(θ; D)∥2 ≤2∆θ

M + 4Mσ2

⋆ λ2 + σ⋆ λ

√

K

.

Lemma I.9. Suppose that λ ≥8BM. Denote Λθ:= ⟨−eg(θ; D), θ −θ⋆⟩. Then it holds that for any θ ∈Θ,

∆θ ≤8λΛθ + 240B

K + 8

Mσ⋆ λ

2

.

Putting everything together. Under the notation of Lemma I.8 and Lemma I.9, Eq. (80) can be rewritten as

E

" T X t=1

Λθt

#

≤2 η + η

2 E

" T X t=1

ED∼πD∥eg(θ t; D)∥2

#

. (82)

Applying Lemma I.8 and Lemma I.9, we have

## 1 T E

" T X t=1

∆θt

#

−240B

K −8

Mσ⋆ λ

2

≤8λ

T E

" T X t=1

Λθt

#

≤16λ

Tη + 4ηλ

T E

" T X t=1

ED∼πD∥eg(θ t; D)∥2

#

≤16λ

Tη + 8ηλ

MT E

" T X t=1

∆θt

#

+ 16ηMσ2

⋆ λ + 4ησ⋆ √

K

,

<!-- Page 58 -->

where the first inequality uses Lemma I.9, the second inequality follows from Eq. (82), and the last inequality uses Lemma I.8. Therefore, as long as ηλ ≤M

16, it holds that

## 1 T E

" T X t=1

∆θt

#

≲B

K +

Mσ⋆ λ

2

+ λ

Tη + ηMσ2

⋆ λ + ησ⋆ √

K

.

Simplifying the upper bound. In the following, we require η ≤ 1 128B and choose λ = M 16η. Then, it holds that

## 1 T E

" T X t=1

∆θt

#

≲B

K + (ησ⋆)2 + M

Tη2 + ησ⋆ √

K

≲B

K + (ησ⋆)2 + M

Tη2, where we use AM-GM inequality and B ≥1. Finally, we may choose η = min

1 128B,

M σ2

⋆T

1/4

. Recall that

M = log N, and hence our choice of η gives

## 1 T E

" T X t=1

Dseq,N(πD ∥πθt)

#

≤1

T E

" T X t=1

∆θt

#

≲ r σ2⋆log N

T + B2 log N

T + B

K, which implies (by Eq. (81))

## 1 T E

" T X t=1

CovN(πθt)

#

≤1

T E

" T X t=1

2 log N −1Dseq,N(πD ∥πθt)

#

≲ s σ2⋆ T log N + B2

T + B K log N.

This is the desired upper bound.

Proof of Lemma I.8. Note that ∥eg(θ; D)∥≤min n

1, ∥bg(θ;D)∥ λ o

. Recall that bg(θ; D) = bED[∇log πθ(y | x)], ∇log πθ(y | x) =

H X h=1 ϕ(x, y1:h) −ϕθ(x, y1:h−1)

, with the notation introduced at the beginning of Appendix I.

We decompose bg(θ; D) by introducing gθ(D):= bED

" H X h=1 ϕθ(x, y1:h−1) −ϕθ⋆(x, y1:h−1)

#

, (83)

and z(D):= bED

" H X h=1 ϕ⋆(x, y1:h)

#

= bED

" H X h=1 ϕ(x, y1:h) −ϕθ⋆(x, y1:h−1)

#

. (84)

Then, by definition, −bg(θ; D) = gθ(D)−z(D). In the following, we first analyze ∥gθ(D)∥and ∥z(D)∥separately under D = {(xi, yi

1:H)}i∈[K] ∼πD and summarize the corresponding upper bounds on in Lemma I.10 (stated and proven in the sequel).

Now, using ∥eg(θ; D)∥≤min n

1, ∥bg(θ;D)∥ λ o

, we know

∥eg(θ; D)∥2 ≤I{ϵθ(D) > M} + I{ϵθ(D) ≤M} · ∥bg(θ; D)∥ λ

≤I{ϵθ(D) > M} + I{ϵθ(D) ≤M}

λ ·

4 p σ2(D) · ϵθ(D) + 8Bϵθ(D)

+ 1 λ∥z(D)∥

≤1

M min{M, ϵθ(D)} + 4 λ p σ2(D) · min{M, ϵθ(D)} + 1 λ∥z(D)∥,

<!-- Page 59 -->

where the second inequality uses ∥bg(θ; D)∥≤∥gθ(D)∥+ ∥z(D)∥and Lemma I.10 (2), and the last inequality uses λ ≥8BM and 1 M min{M, ϵθ(D)} = 1 when ϵθ(D) > M. Taking expectation of D ∼πD, we have

EπD∥eg(θ; D)∥2

≤1

M EπD min{M, ϵθ(D)} + 4 λ EπD p σ2(D) · min{M, ϵθ(D)} + σ⋆ λ

√

K

≤1

M EπD min{M, ϵθ(D)} + 4σ⋆ λ p

EπD min{M, ϵθ(D)} + σ⋆ λ

√

K

= ∆θ

M + 4σ⋆ λ p

∆θ + σ⋆ λ

√

K

.

where the second inequality follows from Cauchy-Schwarz inequality, Lemma I.10 (3) and the fact that E[σ2(D)] = σ2

⋆. By AM-GM inequality, it holds that 4σ⋆ λ

√∆θ ≤∆θ

M + 4Mσ2

⋆ λ2, and the desired upper bound follows immediately.

Lemma I.10. For any θ ∈Θ, the following holds:

(1) It holds that

⟨gθ(D), θ −θ⋆⟩≥bED

" H X h=1 ϵθ(x, y1:h−1)

#

=: ϵθ(D)

(2) Denote σ2(D):= bED hPH h=1 VarπD(x, y1:h−1)

i

. Then

∥gθ(D)∥≤4 p σ2(D) · ϵθ(D) + 8Bϵθ(D).

(3) It holds that ED∼πD∥z(D)∥2 = σ2

⋆ K and

ED∼πD

⟨z(D), θ −θ⋆⟩−1

2ϵθ(D)

+

≤30B

K =: α.

Proof of Lemma I.10. Lemma I.10 (1) follows immediately from Eq. (67):

⟨gθ(D), θ −θ⋆⟩= bED

" H X h=1 ϕθ(x, y1:h−1) −ϕθ⋆(x, y1:h−1), θ −θ⋆

#

≥bED

" H X h=1 ϵθ(x, y1:h−1)

#

=: ϵθ(D).

Lemma I.10 (2) follows immediately from Eq. (68):

∥gθ(D)∥≤bED

" H X h=1

∥ϕθ(x, y1:h−1) −ϕθ⋆(x, y1:h−1)∥

#

≤bED

" H X h=1

4 p

VarπD(x, y1:h−1) · ϵθ(x, y1:h−1) + 8Bϵθ(x, y1:h−1)

#

≤4 p σ2(D) · ϵθ(D) + 8ϵθ(D).

It remains to prove Lemma I.10 (3). Note that K · z(D) = K · bED hPH h=1 ϕ⋆(x, y1:h)

i

= PK i=1

PH h=1 ϕ⋆(xi, yi

1:h)

is a sum of the martingale difference sequence {ϕ⋆(xi, yi

1:h)}i∈[K],h∈[H]. Therefore, we can calculate

E∥z(D)∥2 = 1

K EπD

" H X h=1

∥ϕ⋆(x, y1:h)∥2

#

= σ2

⋆ K.

<!-- Page 60 -->

Furthermore, by Freedman’s inequality (Lemma F.1), for any fixed vector v, parameter γ ∈(0, 1

B) and δ ∈(0, 1), it holds that

P

K X i=1

H X h=1

⟨ϕ⋆(x i, y i 1:h), v⟩−γ E

⟨ϕ⋆(x i, y i 1:h), v⟩2 | x i, y i 1:h−1

≥γ−1 log(1/δ)

!

≤δ.

Note that for v = θ −θ⋆, by Lemma F.5, we have

E

⟨ϕ⋆(x i, y i 1:h), v⟩2 | x i, y i 1:h−1

= Eyh∼πD(·|xi,yi

1:h−1)⟨ϕ(x i, y i 1:h−1, yh) −ϕθ⋆(x i, y i 1:h−1, yh), θ −θ⋆⟩2

≤15BDKL πD(· | x i, y i 1:h−1) ∥πθ(· | x i, y i 1:h−1)

= 15Bϵθ(x i, y i 1:h−1).

Therefore, setting γ = 1 30B, we have shown that for any δ ∈(0, 1), it holds that

PπD

⟨z(D), θ −θ⋆⟩≥1

2 bED

" H X h=1 ϵθ(x, y1:h−1)

#

+ 30B log(1/δ)

K

!

≤δ.

Recall that we denote ϵθ(D):= bED hPH h=1 ϵθ(x, y1:h−1)

i

. Then, for the random variable V:= K 30B

⟨z(D), θ −θ⋆⟩−1

2ϵθ(D)

, the above inequality implies that for any u > 0, P(V ≥u) ≤e−u, and hence P((V)+ ≥u) ≤e−u. Therefore, integrating out the above inequality gives E[(V)+] ≤1, or equivalently,

EπD

⟨z(D), θ −θ⋆⟩−1

2ϵθ(D)

+

≤30B

K =: α.

Proof of Lemma I.9. Recall that we can decompose −bg(θ; D) = gθ(D) −z(D), where gθ(D) and z(D) are defined in Eq. (83) and Eq. (84), respectively. Then, we know

Λθ:= EπD⟨−eg(θ; D), θ −θ⋆⟩

= EπD

⟨gθ(D), θ −θ⋆⟩−⟨z(D), θ −θ⋆⟩ λ + ∥bgθ(D)∥

≥EπD ϵθ(D) −⟨z(D), θ −θ⋆⟩ λ + ∥bgθ(D)∥

≥1

2 EπD ϵθ(D) λ + ∥z(D)∥+ ∥gθ(D)∥

−1 λ EπD

"

⟨z(D), θ −θ⋆⟩−1

2ϵθ(D)

+

#

≥1

2 EπD ϵθ(D) λ + ∥z(D)∥+ ∥gθ(D)∥

−α λ, where the first inequality uses Lemma I.10 (1) and the last inequality uses Lemma I.10 (3) and we recall that α = 30B

K. Note that by Lemma I.10 (2), λ + ∥z(D)∥+ ∥gθ(D)∥

≤λ + ∥z(D)∥+ 4 p σ2(D) · ϵθ(D) + 8Bϵθ(D)

≤max{M, ϵθ(D)}

M ·

"

2λ + ∥z(D)∥+ 4M s σ2(D) min{M, ϵθ(D)}

#

,

<!-- Page 61 -->

where we use min{M, x} max{M, x} = Mx, and λ ≥8BM. Combining these two inequalities, we have

2Λθ + 2α λ ≥EπD ϵθ(D) λ + ∥z(D)∥+ ∥gθ(D)∥

≥EπD

" min{M, ϵθ(D)}

2λ + ∥z(D)∥+ 4M p σ2(D)/ min{M, ϵθ(D)}

#

≥ (EπD min{M, ϵθ(D)})2

EπD h min{M, ϵθ(D)}(2λ + ∥z(D)∥) + 4M p σ2(D) · min{M, ϵθ(D)}

i

≥ (EπD min{M, ϵθ(D)})2

2λ EπD min{M, ϵθ(D)} + M p σ2⋆/K + 4M p σ2⋆EπD min{M, ϵθ(D)}

= ∆2 θ 2λ∆θ + Mσ⋆ h

1 √

K + 4√∆θ i, where the last two inequalities follow from Cauchy-Schwarz inequality. Therefore, there are two cases: (a) ∆θ ≤1

K, and the desired upper bound is trivially true. (b) ∆θ ≥1

K, and then it holds that

2λ∆θ + Mσ⋆

1 √

K

+ 4 p

∆θ

≤2λ∆θ + 5Mσ⋆ p

∆θ ≤3λ∆θ + 8(Mσ⋆)2 λ, where we use AM-GM inequality. Hence, it holds that

∆2 θ ≤8(λΛθ + α) max

(

∆θ, 8

Mσ⋆ λ

2)

, and reorganizing yields

∆θ ≤8 max

 

(λΛθ + α), s

(λΛθ + α)

Mσ⋆ λ

2

 



≤8(λΛθ + α) + 8

Mσ⋆ λ

2

.

This is the desired result.

I.6 Proof of Theorem 6.1 (Test-Time Training)

While the algorithm in Theorem 6.1 might seem somewhat complicated and mysterious, the proof is actually a based on a fairly simple online-to-batch conversion argument. We use a number of basic inequalities already found in the proof of Proposition 5.1 (cf. Appendix I.3).

We first note that we can specialize Lemma I.5 to the token-level SGD update (21), and taking expectation gives

E

" T X t=1

H X h=1

−∇log πθt,h(y t h | x t, y t 1:h−1), θ t,h −θ⋆

#

≤2 η + η

2 E

" T X t=1

H X h=1

∇log πθt,h(y t h | x t, y t 1:h−1) 2

#

. (85)

In the following, we denote ϵt,h:= E

−∇log πθt,h(y t h | x t, y t 1:h−1), θ t,h −θ⋆

.

By triangle inequality,

∥∇log πθ(yh | x, y1:h−1)∥2

≤2∥∇log πθ⋆(yh | x, y1:h−1)∥2 + 2∥∇log πθ(yh | x, y1:h−1) −∇log πθ⋆(yh | x, y1:h−1)∥2.

<!-- Page 62 -->

Using the fact that θ 7→log πθ(yh | x, y1:h−1) is concave and B2-smooth, it holds that for any θ,

∥∇log πθ(yh | x, y1:h−1) −∇log πθ⋆(yh | x, y1:h−1)∥2

≤B2 · ⟨θ −θ⋆, ∇log πθ⋆(yh | x, y1:h−1) −∇log πθ(yh | x, y1:h−1)⟩.

Combining the two inequalities above gives that for all t ∈[T], h ∈[H],

∇log πθt,h(y t h | x t, y t 1:h−1) 2

≤2

∇log πθ⋆(y t h | x t, y t 1:h−1) 2

+ 2B2

∇log πθ⋆(y t h | x t, y t 1:h−1) −∇log πθt,h(y t h | x t, y t 1:h−1), θ t,h −θ⋆

Note that the conditional distribution of yt h | (xt, yt

1:h−1, θt,h) is given by yt h ∼πD(· | xt, yt

1:h−1). Hence, taking the expectation over the entire learning process, we have

E h ∇log πθt,h(y t h | x t, y t 1:h−1) 2i

≤2 EπD∥∇log πθ⋆(yh | x, y1:h−1)∥2

+ 2B2 E

−∇log πθt,h(y t h | x t, y t 1:h−1), θ t,h −θ⋆

= 2 EπD[VarπD(x, y1:h−1)] + 2B2ϵt,h.

Plugging the above inequality to Eq. (85) yields

T X t=1

H X h=1 ϵt,h ≤2 η + η

2 E

" T X t=1

H X h=1

∇log πθt,h(y t h | x t, y t 1:h−1) 2

#

≤2 η + ηT EπD

" H X h=1

VarπD(x, y1:h−1)

#

+ ηB2

T X t=1

H X h=1 ϵt,h.

Therefore, as long as η ≤ 1 2B2, it holds that

T X t=1

H X h=1 ϵt,h ≤4 η + 2ηT EπD

" H X h=1

VarπD(x, y1:h−1)

#

= 4 η + 2ηTσ2

⋆.

By Eq. (67), it also holds that ϵt,h = E

−∇log πθt,h(y t h | x t, y t 1:h−1), θ t,h −θ⋆

≥E DKL πD(· | x t, y t 1:h−1) ∥πθt,h(· | x t, y t 1:h−1)

.

Combining the inequalities above, as long as η ≤ 1 2B2, we have that

E

" T X t=1

H X h=1

DKL πD(· | x t, y t 1:h−1) ∥πθt,h(· | x t, y t 1:h−1)

#

≤

T X t=1

H X h=1 ϵt,h ≤4 η + 2ηTσ2

⋆. (86)

Finally, we note that θ t,h = ϑTTT(x t, y t h−1; θ t), and that for all t and h, xt, yt h−1 | θt ∼πD. Therefore, we have the following key identity:

E

DKL πD(· | x t, y t 1:h−1) ∥πθt,h(· | x t, y t 1:h−1)

| θ t

= E(x,y)∼πD

DKL πD(· | x, y1:h−1) ∥πϑTTT(x,y1:h−1;θt)(· | x, y1:h−1)

= E(x,y)∼πD

DKL πD(· | x, y1:h−1) ∥πTTT θt (· | x, y1:h−1)

.

<!-- Page 63 -->

Combined with Eq. (86), this implies that

4 η + 2ηTσ2

⋆≥E

" T X t=1

H X h=1

DKL πD(· | x t, y t 1:h−1) ∥πθt,h(· | x t, y t 1:h−1)

#

= E

" T X t=1

E

" H X h=1

DKL πD(· | x t, y t 1:h−1) ∥πθt,h(· | x t, y t 1:h−1) θ t

##

= E

" T X t=1

EπD

" H X h=1

DKL πD(· | x, y1:h−1) ∥πTTT θt (· | x, y1:h−1)

##

= E

" T X t=1

DKL πD ∥πTTT θt

#

, where the last equality uses the chain rule for KL divergence.

In particular, we may choose η = min

1 2B2,

1 σ2⋆T

1/2 to derive 1

T E hPT t=1 DKL(πD ∥πTTT θt)

i

≲ q σ2⋆

T + B2

T.

I.7 Proof of Theorem 6.2 (Gradient Normalization for Distillation)

Specializing Lemma I.5 to the update (26) and taking expectation gives

E

" T X t=1

−E(x,y)∼πD[bgθt(y | x)], θ t −θ⋆

#

≤2 η + η

2 E

" T X t=1

E(x,y)∼πD∥bgθt(y | x)∥2

#

. (87)

In the following, we analyze

−E(x,y)∼πD[bgθ(y | x)], θt −θ⋆ and E(x,y)∼πD∥bgθt(y | x)∥2 for any θ ∈Θ, following the proof of Proposition 5.1 (cf. Appendix I.3).

Relating the gradient to stopped KL divergence. Recall that the estimator bg is defined in Eq. (24):

bgθ(y | x) =

H X h=1 αθ(x, y1:h−1)∇log πθ(yh | x, y1:h−1), and the weight function αθ is defined in Eq. (25).

We first recall an elementary property of the quantity αθ. By Lemma I.4, we have

H X h=1 αθ(x, y1:h−1)ϵθ(x, y1:h−1) = min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

, (88)

and hence

E(x,y)∼πD

" H X h=1 αθ(x, y1:h−1)ϵθ(x, y1:h−1)

#

= E(x,y)∼πD min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

= Dseq,N(πD ∥πθ),

(89)

where we recall that Dseq,N(πD ∥πθ) is defined in Proposition D.10 and we denote A = log N. Hence,

−E(x,y)∼πD[bgθ(y | x)], θ −θ⋆

= E(x,y)∼πD

" H X h=1 αθ(x, y1:h−1)

ϕθ(x, y1:h−1) −ϕθ⋆(x, y1:h−1), θ −θ⋆

#

≥E(x,y)∼πD

" H X h=1 αθ(x, y1:h−1)ϵθ(x, y1:h−1)

#

= Dseq,N(πD ∥πθ),

(90)

<!-- Page 64 -->

where the inequality uses Eq. (67).

In addition, the following lemma shows that E(x,y)∼πD∥bgθ(y | x)∥2 is well-controlled.

Lemma I.11 (Gradient error bound). For any θ ∈Θ, it holds that

E(x,y)∼πD∥bgθ(y | x)∥2 ≤(64A + 2)σ2

⋆+ 256AB2Dseq,N(πD ∥πθ).

Putting everything together. Finally, combining the inequalities above, we know that

E

" T X t=1

Dseq,N(πD ∥πθt)

#

≤E

" T X t=1

−E(x,y)∼πD[bgθt(y | x)], θ t −θ⋆

#

≤2 η + η

2 E

" T X t=1

E(x,y)∼πD∥bgθt(y | x)∥2

#

≤2 η + ηT(32A + 1)σ2

⋆+ 128AB2 E

" T X t=1

Dseq,N(πD ∥πθt)

#

, where the first inequality uses Eq. (90), the second inequality follows from Eq. (87), and the third inequality uses Lemma I.11. Therefore, as long as η ≤ 1 2(32A+1)B2, it holds that

E

" T X t=1

Dseq,N(πD ∥πθt)

#

≲1 η + ηTAσ2

⋆.

In particular, we may choose η = min

1 (64 log N+2)B2,

1 T σ2⋆log N

1/2 and derive

E

"

1 T

T X t=1

Dseq,N(πD ∥πθt)

#

≲ r σ2⋆log N

T + B2 log N

T.

By Proposition D.10, this implies

E

"

1 T

T X t=1

CovN(πθt)

#

≲ s σ2⋆ T log N + B2

T.

Proof of Lemma I.11. Fix any θ ∈Θ. By triangle inequality, it holds that

∥bgθ(y | x) −bgθ⋆(y | x)∥

≤

H X h=1 αθ(x, y1:h−1)

ϕθ⋆(x, y1:h) −ϕθ(x, y1:h−1)

≤

H X h=1 αθ(x, y1:h−1)

4 p

VarπD(x, y1:h−1) · ϵθ(x, y1:h−1) + 8Bϵθ(x, y1:h−1)

≤4

H X h=1 αθ(x, y1:h−1)VarπD(x, y1:h−1)

!1/2 H X h=1 αθ(x, y1:h−1)ϵθ(x, y1:h−1)

!1/2

+ 8B

H X h=1 αθ(x, y1:h−1)ϵθ(x, y1:h−1)

≤4 v u u tA ·

H X h=1

VarπD(x, y1:h−1) + 8B min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

.

<!-- Page 65 -->

where the second inequality follows from Eq. (68), the third inequality follows from Cauchy-Schwarz inequality, and the final lines follow from the property (88) of the weight function αθ ∈[0, 1]. Hence, using (a + b)2 ≤ 2a2 + 2b2, we have

∥bgθ(y | x) −bgθ⋆(y | x)∥2

≤32A

H X h=1

VarπD(x, y1:h−1)

!

+ 128AB2 min

(

A,

H X h=1 ϵθ(x, y1:h−1)

)

.

Therefore, taking expectation of (x, y) ∼πD and using EπD∥bgθ⋆(y | x)∥2 ≤σ2

⋆and Eq. (89), it holds that

E(x,y)∼πD∥bgθ(y | x)∥2 ≤(64A + 2)σ2

⋆+ 256AB2Dseq,N(πD ∥πθ).

This is the desired upper bound.

I.8 Necessity of Variance Dependence in High Dimension

We generalize Proposition 3.2 to show that in the worst case (where σ2

⋆≍HB2), the scaling CovN(bπ) = Ω(H n log N) can be unavoidable for autoregressive linear model. This implies that the dependence on σ2

⋆is generally necessary to achieve upper bounds that do not explicitly scale with H.

Proposition I.1. Let H, B, N, n ≥1, and assume log N ≤c min{H, B2} for a sufficiently small constant c > 0. There exists an instance of the autoregressive linear model class Π with d = H, ϕ: X × V⋆→B2(B), and Θ = B2(1), such that for any proper algorithm Alg with output bπ = πbθ for bθ ∈Θ, there exists πD ∈Π, such that under πD, it holds that

E πD,Alg[CovN(πD ∥bπ)] ≥c · min

1, H n · log N

.

Proof of Proposition I.1. We consider X = {+, −}, V = {0, 1}, and the distribution µ be given by µ(+) = 1 −µ(−) = p, where p ∈[0, 1] is a parameter to be chosen later. Let the feature map ϕ be given by ϕ(−, y1:h) = 0, ϕ(+, y1:h) = Byheh, where (e1, · · ·, eH) is a fixed orthonormal basis of RH. Note that with this construction, we have πθ(yh = · | −, y1:h−1) = Ber(1/2), and πθ(yh = · | +, y1:h−1) = Ber eBθh

1 + eBθh

=: πθ,h.

Note that for any h ∈[H], we can bound

C0B|θh −θ′ h| ≤DH(πθ,h, πθ′,h) ≤C1B|θh −θ′ h|, as long as θh ∈[−1

B, 1

B ].

We fix ϵ ∈[0, 1 max{

√

H,B}] to be determined later, and for any v ∈{−1, 1}H, we let θv:= ϵ PH h=1 vheh, and

Θ0:= θv: v ∈{−1, 1}H

⊂B2(1), Π0:= {πθ: θ ∈Θ0}.

Then a direct argument (see e.g., (Wainwright, 2019, Section 15.3)) shows that when pn ≤ c0 B2ϵ2 for a sufficiently small constant c0, there exists θ⋆∈Θ0 such that under πD = πθ⋆, it holds that

H X h=1

P πD,Alg

|bθh −θ⋆ h| ≥ϵ

≥cH.

Therefore, with probability at least c

2, it holds that PH h=1 I n

|bθh −θ⋆ h| ≥ϵ o

≥cH

2, and this in turn implies

H X h=1

D2

H πθ⋆,h, πbθ,h

≥c1HB2ϵ2.

<!-- Page 66 -->

Then, by Proposition D.11, we know that under the above event, as long as log N ≤ c1HB2ϵ2

2, we have

CovN(bπ) ≥p

2. Choosing ϵ = q

4 log N c1HB2 and p = min

1, c0 nB2ϵ2 gives the desired lower bound.

J Proofs from Section 6

J.1 Proof of Theorem 6.3 (Simple Tournament)

Fix N, N ′ ≥1, α > 0, and let π ∈arg minπ∈Π CovN ′(πD ∥π). We study the estimator bπ:= arg min π∈Π max π′∈Π d CovN(π′ ∥π). (91)

Recall that we denote CovπD

N (π′ ∥π) = PπD π′(y|x)

π(y|x) ≥N

(cf. Lemma H.2). By Lemma H.2, with probability at least 1 −δ

2, it holds that d CovN(π ∥π) ≥1

2CovπD e2αN(π ∥π) −εstat, ∀π ∈Π, (92)

where εstat = 8 log(4N∞(Π,α)/δ)

n. Next, again by Lemma H.2, with probability at least 1 −δ

2, it holds that d CovN(π ∥π) ≤2CovπD e−2αN(π ∥π) + εstat, ∀π ∈Π. (93)

In the following, we condition on the success event of Eq. (92) and Eq. (93). Then, we can bound

1 2CovπD e2αN(π ∥bπ) −εstat ≤d CovN(π ∥bπ) ≤max π′∈Π d CovN(π′ ∥bπ)

= min π∈Π max π′∈Π d CovN(π′ ∥π) ≤max π′∈Π d CovN(π′ ∥π)

≤2 max π′∈Π CovπD e−2αN(π′ ∥π) + εstat.

Reorganizing yields

CovπD e2αN(π ∥bπ) ≤4 max π∈Π CovπD e−2αN(π ∥π) + 4εstat. (94)

Note that for any N ′′ and models π, π′, π′′,

CovπD

N′N′′(π′ ∥π) ≤CovπD

N′(π′ ∥π′′) + CovπD

N′′(π′′ ∥π). (95)

Hence, for any model π ∈Π,

CovπD e2αNN ′(πD ∥π) ≤CovπD

N′(πD ∥π) + CovπD e2αN(π ∥π), (96)

CovπD e−2αN(π ∥π) ≤CovπD

N′(π ∥πD) + CovπD e−2αN/N ′(πD ∥π). (97)

Therefore, combining the inequalities above, we see that

Cove2αNN ′(bπ) = CovπD e2αNN ′(πD ∥bπ)

≤CovπD

N′(πD ∥π) + CovπD e2αN(π ∥bπ)

≤CovπD

N ′(πD ∥π) + 4 max π∈Π CovπD e−2αN(π ∥π) + 4εstat

≤5CovπD

N′(πD ∥π) + 4 max π∈Π CovπD e−2αN/N′(π ∥πD) + 4εstat

≤5CovπD

N′(πD ∥π) + e2αN ′

N + 4εstat, where the first inequality uses Eq. (96), the second inequality uses Eq. (94), the third inequality uses Eq. (97), and the last inequality follows from the fact that CovπD

A (π ∥πD) = PπD π(y|x) πD(y|x) ≥A

≤1

A.

The claimed bound (31) follows by setting α = c log N, and N ′ = N a.

<!-- Page 67 -->

J.2 Proof of Theorem 6.4 (Offset Tournament)

Divergence. For distributions P, Q ∈∆(Y), we define the following divergence for N ≥1:11

EN(P ∥Q):= max

(

Ey∼P dQ dP −N

+

, Ey∼Q dP dQ −N

+

)

∈[0, 1].

Then, for models π, π′: X →∆(Y), we further define

EN,µ(π ∥π′):= Ex∼µ EN(π(· | x) ∥π′(· | x)).

Under this divergence, it holds that for any event E,

Pµ,π(E) ≤N · Pµ,π′(E) + EN,µ(π ∥π′), (98)

Pµ,π′(E) ≤N · Pµ,π(E) + EN,µ(π ∥π′), (99)

where Pµ,π is the probability under x ∼µ and y ∼π(· | x). Furthermore, we can bound

Cov2N(π) = Pµ,πD πD(y | x)

π(y | x) ≥2N

≤EN,µ(πD ∥π). (100)

Theorem 6.4′ (General version of Theorem 6.4). Fix N, γ ≥1 such that N ≥8γ2. Consider the estimator bπ:= arg min π∈Π max π′∈Π {d CovN(π′ ∥π) −2γ · d Covπ

N(π′ ∥π)}. (101)

Then with probability 1 −δ, it holds that

Cov2Nγ(bπ) ≲min π∈Π Eγ(πD ∥π) + log(|Π|/δ)

n.

Note that Eγ(πD ∥π) = 0 when |log πD(y | x)−log π(y | x)| ≤log γ for any x ∈X, y ∈Y. Therefore, Theorem 6.4 is an immediate corollary by setting γ = N a.

Proof of Theorem 6.4′. For π, π′ ∈Π, we define the set

CN(π, π′) =

(x, y) | π(y | x)

π′(y | x) ≥N

.

Suppose an i.i.d. dataset D = {(xi, yi)}i∈[n] ∼πD is drawn. We write bPn = 1 n

Pn i=1 δ(xi,yi) and µn = 1 n

Pn i=1 δxi to denote the empirical measures (i.e., bPn is the uniform distribution over D), and let Pµn,π be the probability under the distribution x ∼µn, y ∼π(· | x). Under this notation, we have d CovN(π′ ∥π) = bPn(CN(π′, π)) and we also recall that d Covπ

N(π′ ∥π):= 1 n n X i=1

Py∼π(·|xi)

π′(y | xi)

π(y | xi) ≥N

= Pµn,π(CN(π′, π)).

Thus, the tournament estimator in Eq. (101) can be expressed as bπ:= arg min π∈Π max π′∈Π L(π, π′), (102)

where

L(π, π′):= bPn(CN(π′, π)) −2γ · Pµn,π(CN(π′, π)). (103)

As an immediate consequence of Lemma F.2 and the union bound, we have the following lemma.

11This divergence is inspired by Huang et al. (2025b), but our definition differs slightly from the standard EM-divergence (Polyanskiy, 2010; Block and Polyanskiy, 2023).

<!-- Page 68 -->

Lemma J.1. Fix δ ∈(0, 1), and define εstat = 16 log(16|Π|/δ)

n. With probability 1 −δ, the following bounds hold simultaneously:

(1) For all π, π′ ∈Π, it holds that

2Pµ,πD(CN(π′, π)) + εstat ≥bPn(CN(π′, π)) ≥1 2Pµ,πD(CN(π′, π)) −εstat, (104)

2Pµn,πD(CN(π′, π)) + εstat ≥bPn(CN(π′, π)) ≥1 2Pµn,πD(CN(π′, π)) −εstat. (105)

(2) For any π ∈Π, it holds that Eγ,µn(πD ∥π) ≤2Eγ,µ(πD ∥π) + εstat.

In the following, we fix δ ∈(0, 1) and condition on the success event of Lemma J.1. Let π ∈arg minπ∈Π Eγ,µ(πD ∥π). We denote εapx = Eγ,µ(πD ∥π) and ε′ apx = Eγ,µn(πD ∥π). Note that by Lemma J.1, we have ε′ apx ≤2εapx + εstat.

Then, for any π′ ∈Π,

L(π, π′) ≤2Pµn,πD(CN(π′, π)) −2γPµn,π(CN(π′, π)) + εstat

≤2Eγ,µn(πD ∥π) + εstat = ε′ apx + εstat.

where the first inequality uses Eq. (105), and the second inequality uses Eq. (98).

Therefore, we have max π′∈Π L(bπ, π′) = min π∈Π max π′∈Π L(π, π′) ≤max π′∈Π L(π, π′) ≤εstat + ε′ apx.

In particular, we know L(bπ, π) ≤εstat + ε′ apx. Then, we can bound bPn(CN(π, bπ)) −L(bπ, π) = 2γPµn,bπ(CN(π, bπ))

≤2γ

N Pµn,π(CN(π, bπ))

≤2γ

N γPµn,πD(CN(π, bπ)) + ε′ apx

≤2γ

N h

2γ bPn(CN(π, bπ)) + εstat

+ ε′ apx i

, where the first inequality follows from the fact that π(y | x) ≥Nbπ(y | x) for (x, y) ∈CN(π, bπ), the second inequality uses Eq. (99): Pµn,π(E)−γPµn,πD(E) ≤Eγ,µn(πD ∥π) = ε′ apx for any event E, and the third inequality uses Eq. (105). Therefore, using N ≥8γ2, we know bPn(CN(π, bπ)) ≤5εstat + 2ε′ apx. Then, using Eq. (104), we have

CovπD

N (π ∥bπ) = Pµ,πD(CN(π, bπ)) ≤2bPn(CN(π, bπ)) + 2εstat ≤12εstat + 4ε′ apx.

By Eq. (95), it holds that

Cov2Nγ(bπ) = CovπD

2Nγ(πD ∥bπ) ≤CovπD 2γ(πD ∥π) + CovπD N (π ∥bπ), and we also have CovπD

2γ(πD ∥π) = Cov2γ(π) ≤Eγ,µ(πD ∥π) = εapx by Eq. (100). Combining the inequalities above, we can conclude that

Cov2Nγ(bπ) ≤CovπD

N (π ∥bπ) + εapx ≤12εstat + 4ε′ apx + εapx.

Finally, using Lemma F.2, we have ε′ apx ≤2εapx + εstat. This is the desired upper bound.
