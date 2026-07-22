---
title: "From Markov to Laplace: How Mamba In-Context Learns Markov Chains"
source_url: https://iclr.cc/virtual/2026/oral/10007752
paper_pdf_url: https://arxiv.org/pdf/2502.10178v2
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# From Markov to Laplace: How Mamba In-Context Learns Markov Chains

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

FROM MARKOV TO LAPLACE: HOW MAMBA IN-CONTEXT LEARNS MARKOV CHAINS

Marco Bondaschi ∗ EPFL

Nived Rajaraman UC Berkeley

Xiuying Wei EPFL

Kannan Ramchandran UC Berkeley

Razvan Pascanu Google DeepMind

Caglar Gulcehre EPFL

Michael Gastpar EPFL

Ashok Vardhan Makkuva Télécom Paris

## ABSTRACT

While transformer-based language models have driven the AI revolution thus far, their computational complexity has spurred growing interest in viable alternatives, such as structured state space sequence models (SSMs) and Selective SSMs. Among these, Mamba (S6) and its variant Mamba-2 have shown remarkable inference speed-ups over transformers while achieving comparable or superior performance on complex language modeling tasks. However, despite these architectural innovations and empirical successes, the fundamental learning capabilities of Mamba remain poorly understood. In this paper, we address this gap by studying in-context learning (ICL) on Markov chains and uncovering an interesting phenomenon: even a single-layer Mamba efficiently learns the in-context Laplacian smoothing estimator, which is both Bayes and minimax optimal. To explain this, we theoretically characterize the representation capacity of Mamba and reveal the fundamental role of convolution in enabling it to represent the optimal Laplacian smoothing. These theoretical insights align strongly with empirical results and, to the best of our knowledge, represent the first formal connection between Mamba and optimal statistical estimators. Finally, we outline promising research directions inspired by these findings. Code is available at https://github.com/Bond1995/Markov-Mamba.

## INTRODUCTION

Transformers have been at the forefront of recent breakthroughs in language modeling, driving the AI revolution (Vaswani et al., 2017; Radford & Narasimhan, 2018; Devlin et al., 2018). Despite their empirical success, transformers suffer from high computational complexity, such as quadratic scaling in sequence length during training and linear cache size at inference (Gu & Dao, 2023a). To address these limitations, there is a growing interest in designing alternative efficient architectures among which structured state space models (SSMs) are the most prominent. In particular, Selective SSMs such as Mamba and Mamba-2, have achieved state-of-the-art results in various language modeling tasks, while greatly improving the inference throughput (Cirone et al., 2025).

Motivated by this success, there is tremendous interest in understanding the sequential modeling abilities of SSMs, especially that of Mamba. In particular, mirroring a theme that has been successful in unraveling fundamental mechanisms (e.g. induction heads) behind transformers (Makkuva et al., 2025; 2024; Rajaraman et al., 2024; Nichani et al., 2024; Edelman et al., 2024), a growing body of research explores Mamba through its in-context learning (ICL) capabilities (Grazzi et al., 2024; Halloran et al., 2024; Akyürek et al., 2024; Park et al., 2024). While these works reveal interesting insights about Mamba’s ICL abilities vis-a-vis transformers, they are largely empirical in nature, and we currently lack a fundamental theoretical understanding of Mamba and its underlying learning mechanisms. We are thus motivated to ask:

Can we systematically characterize the ICL capabilities of Mamba?

∗Correspondence to marco.bondaschi@epfl.ch.

arXiv:2502.10178v2 [cs.LG] 22 Jun 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026

0 10 20 30 40 50 60 70

0.3

0.4

0.5

0.6

0.7

0.8

0.9 t: xt = 0

Predicted probability Pθ xt+1 = 1 | xt

1

1-layer Mamba 1-layer Transformer 2-layer Transformer Optimal estimator

(a) Next-token probability estimation

1 3 4 0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

Markov order

L1 distance

1-layer Mamba 1-layer Transformer 2-layer Transformer

(b) L1 distance of model estimation from optimal

**Figure 1.** Single-layer Mamba learns the optimal Laplacian estimator when trained on random Markov chains, exhibiting ICL. (a) shows the predicted probability distribution on a fixed test sequence for models trained on binary first-order Markov sources. (b) quantifies the L1 deviation from the optimal estimator for random sequences and various Markov orders. The error intervals show the standard deviation across 5 runs. Sec. 4.3 and Fig. 10 further discuss Mamba vs. Transformers.

In this paper, we approach this question from the point of view of representation power, and characterize Mamba’s ICL capabilities on Markov processes, building upon the Markov-ICL framework originally introduced for transformers (Edelman et al., 2024). As opposed to a Mamba vs. Transformers comparison, here we leverage this framework for a detailed study of Mamba, and uncover an interesting phenomenon: even a single-layer Mamba efficiently learns the in-context Laplacian smoothing estimator, which is both Bayes and minimax optimal, for all Markov orders (Figs. 1 and 10a). Towards explaining this, we theoretically characterize the representation capacity of Mamba and demonstrate that the convolution mechanism, together with selectivity and recurrence, plays a fundamental role in realizing the Laplacian smoothing. Importantly, we showcase that these theoretical insights align strongly with empirical results, even outside the realm of Markovian data. To the best of our knowledge, this is the first result of its kind connecting Mamba and optimal statistical estimators.

In summary, we make the following contributions:

• Leveraging the Markov-ICL framework, we uncover the surprising fact that even a single-layer Mamba learns the optimal in-context estimator for all Markov orders (Fig. 1). Intriguingly, convolution plays a pivotal role, more so than gating and non-linear activation, in this learning ability (Sec. 3). • Towards explaining this phenomenon, we characterize the representational capacity of single-layer Mamba and show, both theoretically and empirically, how it represents the optimal in-context estimator for any finite-state first-order processes, through an intricate interplay of convolution, selectivity and recurrence. Further, we provide fundamental limits for higher-order processes (Sec. 4). • We demonstrate the generality of our findings on non-Markovian data and illustrate the fundamental role of convolution even on complex language-modeling tasks (Sec. 5).

## 1.1 RELATED WORK

SSMs (Gu et al., 2020; 2021) have been recently introduced as an alternative recurrent architecture aimed at rivaling the well established transformer backbone (Vaswani et al., 2017). The model was originally introduced as a discretized linear dynamical system (Gu et al., 2021). Recent works tried to re-frame the architecture from a linear recurrent perspective (Orvieto et al., 2023b). However, there are still many gaps in understanding this family of models (Team et al., 2024), such as questions around expressivity (Orvieto et al., 2023a). This is particularly important given the proliferation of Mamba-inspired architectures that have emerged since its introduction (Qin & Liu, 2024; Csordás et al., 2024; Zhu et al., 2024; Gu & Dao, 2023b; De et al., 2024; Beck et al., 2024).

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

To this end, our work squarely focuses on understanding the representation power of Mamba, and in particular its ICL capability, which, while extensively studied for transformers (Xie et al., 2021; Hendel et al., 2023; Bai et al., 2023), remains largely unexplored for SSMs. In this space, recent studies such as Sushma et al. (2024), have shown that SSMs can perform gradient-based learning for in-context adaptation similar to transformers. There is conflicting evidence whether Mamba’s ICL abilities are better (Grazzi et al., 2024) or worse (Halloran et al., 2024; Akyürek et al., 2024) compared to transformers. Nonetheless, SSMs have demonstrated promising results in in-context reinforcement learning tasks (Lu et al., 2024), as well as in next-state prediction for dynamical models (Joseph et al., 2024), highlighting the potential of SSMs as efficient alternatives to transformers for ICL tasks. Motivated by this, as opposed to an architectural comparison Jelassi et al. (2024); Bhattamishra et al. (2024); Merrill et al. (2024); Sarrof et al. (2024), here we solely focus on Mamba’s ICL capabilities, specifically, through the lens of random Markov processes. This framework has been successfully applied to transformers (Edelman et al., 2024; Makkuva et al., 2025; 2024; Rajaraman et al., 2024; Nichani et al., 2024), where it helped unveil fundamental learning mechanisms of transformers such as induction heads. Ours is the first work that employs this framework for Mamba and SSMs.

## 2 PROBLEM SETUP

We formally define the problem setting and provide necessary background. We use the following notation: scalars are denoted by such italic lower case letters as x, y, Euclidean vectors by bold x, y, and matrices by upper case X, Y, etc. 1 refers to the all-one vector. For T ∈N, [T] ≜{1,..., T}, and for a sequence (xt)t≥1, define xt k ≜(xk,..., xt). For z ∈R, sigmoid(z) ≜1/(1 + e−z), ReLU(z) ≜max(0, z), and softplus(z) ≜log(1 + ez). Unif(S) denotes the uniform distribution over a set S and Dir(β) denotes the Dirichlet distribution with parameter β > 0. DKL (P∥Q) denotes the KL divergence between distributions P and Q.

## 2.1 INPUT DATA: RANDOM MARKOV CHAINS

To investigate the ICL capabilities of Mamba, we build upon the Markov-ICL framework of Edelman et al. (2024). In particular, we let the input tokens to be stochastic and drawn from a random Markov chain of order k. That is, the token sequence x = (xt)T t=1 ∈X T on the state space (vocabulary) X follows the transition dynamics:

P xt+1 = · | xt

1

= P xt+1 = · | xt t−k+1

, (1)

almost surely for all t ∈[T], and the kth-order Markov kernels, P xt+1 = · | xt t−k+1 = it t−k+1

, are sampled independently for each tuple (it−k+1, · · ·, it) from the Dirichlet prior Dir(β · 1), with β > 0. When β = 1, this corresponds to the uniform distribution on the S-dimensional simplex ∆S

1, where size S = |X|.

The transition matrix P = (Pik

1)ik 1∈X k, Pik 1 ∈[0, 1]S, encapsulates the set of all Sk conditional probabilities of the chain, each row corresponding to one of them. While this transition matrix governs the generation of each token xt for t > k, the first k-tokens x1,..., xk are drawn i.i.d. from Unif(X). This constitutes the joint law of the random variables (P, x), termed random Markov distribution henceforth. More succinctly,

Data generation (Random Markov sequences).

1. Draw P with each row sampled i.i.d. from Dir(β · 1). 2. For t = 1,..., k, sample xt ∼Unif(X). 3. For t = k,..., T, sample xt+1 ∼Pxt t−k+1. 4. Return the input x = (xt)T t=1. 5. Repeat the above steps to generate a batch {x(b)}b∈[B].

Why Random Markov is a good testbed for ICL. As a consequence of the generation process, every sequence follows a different Markov distribution. Therefore, at inference, a model trained on this random Markovian data has to estimate the next-token distribution in-context for every test sequence. Hence, this data class serves as a good sandbox to gauge the ICL capabilities of Mamba, which was also used in a similar context for transformers (Nichani et al., 2024; Rajaraman et al., 2024).

<!-- Page 4 -->

Published as a conference paper at ICLR 2026

## 2.2 MAMBA ARCHITECTURE

Selective SSMs such as Mamba and Mamba-2 are a class of sequence-to-sequence models that are closely related to RNNs and classical state space models (Gu & Dao, 2023b).

x1... xt... xT ∈{0, 1}

Embedding Embedding Embedding

Mamba Mamba Mamba x1 xt xT......

MLP u1

MLP ut

MLP uT......

Linear v1

Linear vt

Linear vT......

σ(·)

logit1 σ(·)

logitt σ(·)

logitT......

fθ(x1

1) fθ(xt

1) fθ(xT

1)......

**Figure 2.** Mamba-based language model.

A key feature underpinning these models is the selectivity mechanism, enabling them to selectively choose inputs at every timestep, as opposed to linear time-invariant (LTI) systems. While we believe our work captures the behavior of all selective SSMs, we will specifically focus on the state-of-theart Mamba-2 model to simplify exposition. By slight abuse of terminology, henceforth we will also refer to this model simply as Mamba. Mathematically speaking, Mamba implements the sequence-to-sequence mapping Mamba: Rd×T 7→ Rd×T, where given a sequence of input embeddings x = (xt)T t=1 ∈ Rd×T of dimension d, it outputs the corresponding output embeddings o = (ot)T t=1 ∈ Rd×T of the same dimension with o = Mamba(x). More precisely, fix t ∈ [T]. Then the output ot at time t is computed as ot = Mamba(xt

1) using the following recurrence equations (Dao & Gu, 2024):

Ht = at Ht−1 + ext b⊤ t ∈Red×N, yt = Ht ct ∈Red, zt = yt ⊙ReLU(Wz xt) ∈Red, ot = Wo zt ∈Rd,

(Mamba)

at ≜exp(−a · ∆t) ∈(0, 1),

∆t ≜softplus(⟨w∆, xt⟩+ δ) ∈R, ext ≜ReLU(convX(WX xt t−w+1)) · ∆t, bt ≜ReLU(convB(WB xt t−w+1)), ct ≜ReLU(convC(WC xt t−w+1)),

(Input selectivity)

where the initial state H0 = 0, Wz ∈Red×d, Wo ∈Rd×ed, a ≥0, w∆∈Rd, δ ∈R, WX ∈ Red×d, WB ∈RN×d and WC ∈RN×d are all learnable parameters, and conv(zt t−w+1) is a time-wise convolution of window w ∈N with distinct kernels per dimension. Here e ∈N is the feature expansion factor, typically 2. Let θMamba denote the set of all these parameters.

Intuition behind Mamba. The underlying intuition behind the update equations in Mamba is simple: given a sequence of input embeddings (xt), we first capture their local temporal information using separate convolutions to compute ext, bt, and ct (Input selectivity). Equipped with this local memory, we perform a linear state update to compute the current state Ht from the past Ht−1, weighed by an input-dependent decay factor at ∈(0, 1), and (ext, bt). Subsequently, we compute the state projection yt, modulate it with an input-selective term to yield zt, and finally project it down to get the output embedding ot, which is a function of the entire input sequence until then, xt

1, i.e., ot = Mamba(xt 1).

Mamba-based language model. Mamba block is then incorporated into a full-fledged language model as follows:

xt ∈{0, 1}

Embedding −−−−−−→xt

Mamba −−−−→ut MLP −−−→vt

Linear −−−→logitt

Prediction −−−−−→fθ(xt

1), (2)

where fθ(xt

1) ≜Pθ (xt+1 = · | xt 1) = softmax(logitt) ∈[0, 1]S is the probability estimation for the next symbol xt+1 conditioned on the past xt

1. We omit the layer norm here for simplicity. We compactly denote the set of all model parameters as θ ∈RD. We refer to § B for more details.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

## 2.3 LEARNING TASK: NEXT-TOKEN PREDICTION

With the objective of auto-regressively estimating the next token, we train the model parameters θ to minimize the cross-entropy loss between the next-token predicted probability fθ(xt

1) and the corresponding ground-truth symbol xt+1 across all the positions t ∈[T]:

L(θ) ≜−1

T

X t∈[T ]

EP Ext+1

1 ∼P log f (xt+1)

θ (xt

1)

, (3)

where f (j)

θ (xt

1) ≜Pθ (xt+1 = j | xt 1) for j ∈X, and the expectation is both over the transition kernels P and the Markov sequences x = (xt)T t=1 sampled from P. In practice, it is replaced by empirical average across a finite set of batches, sampled according to the random Markov distribution in Sec. 2.1. For our experiments we use the AdamW optimizer (Kingma & Ba, 2015).

## 2.4 OPTIMAL ESTIMATOR: LAPLACIAN SMOOTHING

Given the Bayesian prediction loss in Eq. (3), it is natural to ask: what is the optimal θ minimizing it? It follows from a classical result in statistics (Rissanen (1984), § A) that this minimum is achieved when the corresponding model prediction matches the (average) ground-truth predictive distribution, i.e. Pθ (xt+1 = j | xt

1) = EP |xt 1 [P (xt+1 = j | xt 1)], for all t. Given the joint distribution of the pair (P, xt+1

1) in Sec. 2.1, where the kernel P ∼Dir(β · 1), it can be shown (§ A) that the conditional expectation above simplifies to the well-known Laplacian smoothing, also known as the add-β estimator (see e.g. Merhav & Feder (1998)):

P(k)

β xt+1 = j | xt

1

≜EP |xt

1

P xt+1 = j | xt

1

= nj + β n + 2β, (Laplacian smoothing)

where nj is the number of times token j follows the current kth-order context xt t−k+1 in the sequence xt

1, i.e. nj = |{i: (xi−1 i−k, xi) = (xt t−k+1, j)}| and n is the frequency of this context, i.e. n = |{i: xi−1 i−k = xt t−k+1}|. Adjusting these counts by β plays the role of additive smoothing, which avoids assigning zero probabilities to unseen events, an idea dating back to Laplace (Laplace, 1814). It is also known that the add-β estimator is asymptotically minimax optimal, as T →∞(Xie & Barron, 1997; Hao et al., 2018).

How Laplacian smoothing implies ICL. If Mamba realizes this smoothing estimator, i.e. Pθ = P(k)

β, it automatically implies its ICL abilities: given a fresh test sequence at inference, in order to optimally predict the next token, it has to process the input tokens in-context to compute the relevant counts, as in the Laplacian smoothing. But does Mamba realize this optimal counting estimator in practice?

3 DOES MAMBA LEARN IN-CONTEXT ESTIMATORS?

To investigate the ICL capabilities of Mamba, we consider the problem setup described above and train Mamba and transformer models using AdamW on the next-token prediction loss in Eq. (3) on random Markov chains (we refer to § F for more experimental details). These experiments reveal interesting and rather surprising insights about Mamba:

## 1 Mamba learns the optimal Laplacian smoothing estimator on the

Markov prediction task, even with a single layer (Fig. 1a).

## 2 Convolution mechanism plays a fundamental role in

Mamba, more so than gating and non-linear activations, in aiding its learning abilities (Fig. 3a).

In the sequel, we expand upon these observations in detail.

1) Mamba learns the Laplacian smoothing. After training, we evaluate Mamba and transformers on the same test sequence fixed beforehand and compare their performance to that of the optimal Laplacian smoothing estimator. Specifically, we compare their next-token prediction probabilities with those of the add-β estimator. Fig. 1 illustrates these results for various Markov orders, which uncovers a surprising phenomenon: even a single-layer Mamba sharply matches the optimal

<!-- Page 6 -->

Published as a conference paper at ICLR 2026

0 5 10 15 20 25 30 35 0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

0.40

Iteration (×200)

Test loss

Mamba MambaZero Mamba without convolution

(a) Importance of convolution

2 3 4 5 0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

Convolution window of Mamba

Test loss

Order 1 Order 2 Order 3 Order 4

(b) Relation between window size and Markov order

**Figure 3.** (a) illustrates the fundamental role of convolution, without which the model fails to learn the task. In contrast, a simplified variant with just the convolution (MambaZero) matches the performance of the full model. (b) highlights the relation between the Markov order k and the window size w of Mamba. It is required that w ≥k + 1 for the model to learn the order-k prediction task.

estimator on the whole sequence. The same conclusion holds for larger state spaces and deeper models (Fig. 10a), as well as in over-parametrized settings (Fig. 9), and even when part of the dataset is held out (see § E). For transformers, we observe that a two-layer model also matches the predictor, albeit less sharply, whereas a single layer fails to solve the task. This aligns with recent theoretical results (Sanford et al., 2024; Ekbote et al., 2025), that show that two layers are required for transformers to implement an induction head (realizing the counting estimator) efficiently. We also observe that linear attention performs similarly to softmax attention in this setting (cf. Fig. 7). Sec. 4.3 further discusses Mamba vs. Transformers.

2) Convolution is the key. To decipher the key architectural component behind Mamba’s success in Markov prediction task, we do an ablation study on its three main features: (i) convolution in Input selectivity, (ii) ReLU non-linearity in Input selectivity, and (iii) the gating mechanism in Mamba and MLP. Amongst them, interestingly, convolution plays a fundamental role in the model’s performance, as illustrated in Fig. 3a. Here we compare the full Mamba architecture from Sec. 2.2, Mamba with just the convolution in Input selectivity removed, and a simplified Mamba architecture with only convolution (MambaZero in Sec. 4.1). Further experiments on adding/removing convolution to Mamba and transformers, as well as experiments with varying width, are shown in § E.6, while experiments on natural language are deferred to Sec. 5.2. As a metric of comparison, we use the closeness of each of these models’ losses L(θ) to that of the optimal add-β estimator Lβ, i.e. i.e. |L(θ) −Lβ|. The closer this metric is to zero, the better the model’s performance is. Remarkably, the simplified Mamba with just the convolution succeeds on the Markov prediction task, while the full model without convolution fails, highlighting its fundamental importance. This raises a natural question: how does convolution help Mamba to implement the optimal Laplacian estimator?

## 4 HOW MAMBA IMPLEMENTS THE LAPLACIAN ESTIMATOR

Motivated by its success in learning the optimal estimator, here we study how Mamba represents Laplacian smoothing. Specifically, we provide a concrete theoretical construction backed by empirical results, that illustrates the mechanism Mamba uses to implement the estimator in practice.

## 4.1 MAMBAZERO: SIMPLIFIED MODEL

Building upon the insight that Mamba with just the convolution achieves the same performance as that of the full model (Fig. 3a), we consider its simplified version: MambaZero. MambaZero retains only the essential elements of the full model in Sec. 2.2: the Embedding layer, the convolution

<!-- Page 7 -->

Published as a conference paper at ICLR 2026 inside the Mamba block in Input selectivity, and the Linear layer. More formally, it is given by:

xt = ext ∈Rd, (Embedding)

ut = xt + MambaZero(xt

1), (MambaZero)

logitt = Wℓut ∈RS, (Linear)

fθ(xt

1) = (logitt/∥logitt∥1), (Prediction)

Ht = atHt−1 + ext b⊤ t ∈Red×N, yt = Ht ct ∈Red, ot = Wo yt ∈Rd,

(MambaZero)

where ex is the token embedding for x ∈X, and the input-selective terms at, ext, bt and ct are computed as in Input selectivity without ReLU and just the convolution. Here we use the L1 normalization instead of the softmax in the Prediction layer to ease theoretical analysis, similar to Nichani et al. (2024); Rajaraman et al. (2024). Let θ = ({ei}i∈X, θMambaZero, Wℓ) ∈RD denote the full set of parameters for appropriate D ≥1.

## 4.2 MAIN THEOREM: MAMBA REPRESENTS THE LAPLACIAN ESTIMATOR

We now present our main theorem that MambaZero can represent Laplacian smoothing for any finite-state first-order Markov process. A key defining feature of our constructive proof is that it aligns with the structures empirically learned by the model, shedding light on the fundamental learning mechanisms of Mamba.

Theorem 1. For a state space X = {1, 2,..., S} of size |X| = S, there is a choice of parameters for the canonical MambaZero model, with dimensions N = S, d = 2S, e = 1 and convolution window w = 2, such that its output prediction exactly matches that of the Laplacian estimator, for first-order Markov chains on X. More formally, for any β > 0, there exists a set of parameters θ such that, for all sequences (xt)t≥1 and all t ≥1,

DKL

P(1)

β (· | xt

1)∥Pθ

· | xt 1

= 0.

Remark. The KL divergence above is precisely the penalty paid in the cross-entropy loss in Eq. (3) at time t when using the predictor Pθ instead of the optimal P(1)

β. In other words, the result implies that the loss of MambaZero can be made exactly equal to the optimal.

## 4.2.1 KEY MECHANISM AND PROOF SKETCH

Main idea. To build our intuition towards how MambaZero can realize the add-β counting estimator for first-order Markov sequences, let’s focus on the core MambaZero block. The key observation here is the following: if the state Ht−1 can capture all the transition counts i →j till xt−1

1, the new state Ht can be updated to account for the current transition xt−1 →xt on top of the existing counts, by a suitable choice of at, ext, and bt. Then the relevant count information corresponding to the current prefix xt could be read off from the state projection yt = Htct, and be modified to account for β-smoothing via the Linear and Prediction layers. Buttressing this idea are two key empirical facts, which in fact hold for any k ≥1, underpinning our construction:

(i) State-to-state transition factor at ≈1 for all t ≥1. We empirically observe that when the MambaZero model is trained on random first-order Markov data, at convergence we have at ≈1 for all t ≥1 (Fig. 4). Since at modulates how much past information flows into the present, at = 1 is required for the state Ht to store all previous transition counts. Note that this can be easily achieved by setting either a or ∆t to be zero in Input selectivity, which we empirically observe as well.

(ii) Convolution window w ≥k + 1. Recalling that k is the Markov order, we empirically observe that the window size w = k + 1 is sufficient for the full Mamba to learn the Laplacian smoothing on kth-order Markov chains (Fig. 3b). To understand why, note that in the MambaZero architecture above, apart from the MambaZero block, all remaining equations operate on the current token at time t. In the MambaZero block, the dependency of the output yt on the previous tokens is due to that of the state Ht on (ext, bt) in the update equation, and of ct in the state projection. Since (ext, bt, ct) depend on the past through the convolutions, a window of size k + 1 enables them to keep track of the current token as well as its length-k prefix, which is necessary to compute the counts needed in Laplacian smoothing. On the other hand, if wX, wB ≤k, then one can find confusable sequences, i.e. sequences that share the same number of occurrences of all length-k prefixes, but whose counts

<!-- Page 8 -->

Published as a conference paper at ICLR 2026 of the tokens following each prefix is different, resulting in the model’s estimate to deviate from that of the optimal add-β. We refer to § C.1 for more details. While having all the window sizes wX, wB, wc ≥k + 1 is sufficient, it can be further strengthened to wc = k (§ C.1).

We now detail our construction for the first-order case, capitalizing on these insights.

Construction. Let us fix w = k + 1 = 2. Then, ext and bt only depend on the current token xt and the previous one xt−1, while ct only depends on xt. Thus, ext and bt can only take S2 possible values depending on the last transition in the sequence, whereas ct only S. To ease the notation, we will denote these values by ex(ij), b(ij), and c(i) respectively, for i, j ∈X. Additionally, at t = 1, these terms depend only on the current symbol, taking two additional values each, denoted by ex(i), b(i). Let nij denote the number of transitions i →j in the input sequence xt

## 1. Then, unfolding the state update recursion in MambaZero, we get that the output of the MambaZero block is

ot = Wo ex0b⊤

0 ct + X ij nij Wo ex(ij)b(ij)⊤ct. (4)

While the output in Eq. (4) depends on all the transition counts, in view of Laplacian smoothing, we ideally want only those counts pertaining to relevant transitions, i.e. if xt = 0, the counts n0j, for j ∈X, and similarly for other values of xt. To this end, we empirically observe that at convergence, the model’s parameters are such that b(ij)⊤ct ≈0 whether i̸ = xt (cf. Fig. 5). Due to this property, only the counts that are involved in the computation of the Laplacian estimator for the current token xt appear in the output ot. Stitching these facts, the final logits in the Linear layer depend on the first and current token via logitt = Wℓxt + WℓWo ex0b⊤

0 ct + X j nxt,jWℓWo ex(xt,j)b(xt,j)⊤ct. (5)

The final step is to then show that for properly chosen parameters, one can make the two vectors associated with the counts to be orthogonal, and the other vectors, independent of the counts, to sum up to the vector β1 (which we also empirically verified, cf. Fig. 5). Subsequently, the L1 normalization in Prediction layer will give a next-token probability estimate, matching that of the add-β estimator. We defer the full proof and additional details to § C.

Dimension reduction for binary state space. Interestingly, for the binary case X = {0, 1}, it is possible to further reduce the hidden dimension d = 2S in Thm. 1 to d = S = 2 by leveraging the relationship between the transition counts. The key theoretical insight is that the transition counts in binary sequences are strongly correlated. Specifically, n01 and n10 are at most one apart: every time a transition 0 →1 occurs, either the sequence is followed by only 1’s until the end, or a subsequent transition 1 →0 also occurs. Therefore, the dependency of the output on n01 is in fact a dependency on n10. One can leverage this property to help MambaZero realize Laplacian smoothing with just two-dimensional embeddings, with arbitrarily small error. We refer to Thm. 4 in § C.3 for full details.

## 4.3 LOWER BOUND: FUNDAMENTAL LIMIT ON THE REPRESENTATION POWER OF MAMBA

We now provide a fundamental limit on the representation power of recurrent architectures like Mamba, in the form of a lower bound on the hidden dimension that is required to represent the optimal estimator. In particular, our result establishes that with finite bit precision, irrespective of depth, for any recurrent architecture to implement the Laplacian estimator, the hidden dimension has to at least scale as Ω(2k). Theorem 2. Consider a recurrent model of the form

Ht = ht(Ht−1, xt), yt = Pθ

· | xt 1

= gt(Ht), with transformations (ht, gt), where Ht ∈Rd and the model has a bit precision of p. Suppose that the kth-order Markov kernel P is sampled from the Dirichlet prior with β = 1, P ∼Dir(1 · 1). Suppose also that the recurrent architecture satisfies the following point-wise guarantee: for any sufficiently large t, almost surely over P and xt

1 ∼P, Pθ

· | xt 1

−P(k)

1 (· | xt 1)

∞≤ε, (6)

<!-- Page 9 -->

Published as a conference paper at ICLR 2026 where P(k)

1 (· | xt 1) is the Laplacian estimator for β = 1. Then, the recurrent architecture must satisfy d · p ≥2k(1 −3ε) log(1/ε).

We defer the full proof and additional details to App. D.

Depth. We note that Thm. 2 does not assume depth one, and holds for recurrent models of any depth.

Mamba vs. Transformers. As Thm. 2 demonstrates, to capture a kth-order Markov process, Mamba requires the hidden dimension to scale exponentially in k, whereas the best known result for transformers needs a three layer model with the hidden dimension growing linearly in k (Rajaraman et al., 2024). On the other hand, for first-order sources we empirically observe from Fig. 1a that 1-layer Mamba tracks the optimal estimator more sharply than a transformer (see § E for additional comparative results). While these comparisons are meant to provide a more detailed context for Mamba, we would like to emphasize that the main focus of our paper is not a comparative study but rather a fundamental understanding of Mamba’s ICL abilities.

Higher orders and learning dynamics. While Thm. 1 demonstrates that Mamba can represent the optimal estimator for finite-state first-order processes, our empirical results in Fig. 1b strongly suggest that a similar conclusion holds for higher-order sources. In a similar vein, analyzing Mamba’s learning dynamics in its convergence to this smoothing estimator is an interesting topic of future research, but outside the scope of this paper, whose focus is on representation power.

## 5 BEYOND MARKOV

## 5.1 SWITCHING MARKOV MODEL

A key component of Mamba enabling selectivity is the state-transition factor at, that controls the flow of information from the past state Ht−1 to the current Ht: if at = 1, the past information is fully utilized in computing the current state, and hence the output, whereas at = 0 completely ignores the past. In the Markovian setting considered so far, the role of at has largely been dormant: at ≈1 for all t ≥1, as the optimal Laplacian predictor requires counts of all transitions, demanding the use of full past (Sec. 4.2). To better highlight this selectivity mechanism, we consider a non-Markovian process, where the role of at becomes fundamental.

Specifically, we focus on the switching Markov process, where we add a switch token to the binary alphabet, i.e. we consider X = {0, 1, S}. The key difference here compared to the random Markov generation in Sec. 2.1 is that until we hit switch token, we follow the same binary Markov sequence generation as the former, but once the switch state is reached, we sample a new Markov kernel and then generate a new Markov sequence. The switch tokens are sampled according to a parallel i.i.d. Bernoulli process with probability pswitch (0.01 in our experiments). The sampling process is described in detail in § E.7. With this data model, the optimal prediction strategy is to use the add-β estimator in between two switch tokens, and reset the transition counts every time a switch occurs. We provide empirical evidence in § E.7. Indeed, Fig. 13 illustrates that Mamba implements precisely this strategy, closely tracking the switching events via the transition factor at: it sets at to be zero whenever xt = S and to one otherwise.

## 5.2 NATURAL LANGUAGE MODELING

**Table 1.** Perplexity results on the WikiText-103 dataset.

## Model

Params. Perplexity

Mamba-2 (w/o conv) 14.53 M 30.68 Mamba-2 (w/ conv) 14.54 M 27.55

Transformer (w/o conv) 14.46 M 29.28 Transformer (w/ conv) 14.46 M 28.67

To test the generality of our finding that convolution plays a key role on Markovian data (Fig. 3), we conduct experiments on language modeling using the WikiText- 103 dataset. Details on the experimental setup can be found in § F. By adding or removing convolution in both these models, we obtain the results in Table 1. The results illustrate that convolution enhances the performance of the two architectures, in particular for Mamba (11% vs. 2%),

<!-- Page 10 -->

Published as a conference paper at ICLR 2026 highlighting its saliency. Further ablation studies on this task show that together with convolution, gating also plays a central role (17% change, cf. § E.8, Table 4). Furthermore, additional experiments with deeper models show that the relative importance of convolution seems to decrease as the number of layers increases (cf. § E.8, Table 5). This may be due to the fact that the role of convolution is taken over by other Mamba layers, which are known to successfully approximate convolution (Wang & Xue, 2023).

## 6 CONCLUSION

Structured state space sequence models (SSMs) and Selective SSMs such as Mamba have shown remarkable inference speed-ups over transformers while achieving comparable or superior performance on complex language modeling tasks. In this paper, we studied in-context learning (ICL) capabilities of Mamba on random Markov chains and show that, unlike transformers, even a single-layer Mamba efficiently learns the in-context Laplacian smoothing estimator. To explain this, we theoretically and empirically characterized the representation capacity of Mamba, which revealed the fundamental role of convolution, together with selectivity and recurrence, in enabling it. We further provided additional empirical results on non-Markovian data, showing the generality of our insights. Extending our results to deeper Mamba models, as well as investigating Mamba’s learning dynamics, are some interesting future directions.

## ACKNOWLEDGMENTS

The work in this manuscript was partially supported by the Swiss National Science Foundation under Grant 200364.

## REFERENCES

Ekin Akyürek, Bailin Wang, Yoon Kim, and Jacob Andreas. In-context language learning: Arhitec- tures and algorithms. arXiv preprint arXiv:2401.12973, 2024.

Yu Bai, Fan Chen, Huan Wang, Caiming Xiong, and Song Mei. Transformers as statisticians:

Provable in-context learning with in-context algorithm selection. In Workshop on Efficient Systems for Foundation Models @ ICML2023, 2023.

Maximilian Beck, Korbinian Pöppel, Markus Spanring, Andreas Auer, Oleksandra Prudnikova,

Michael Kopp, Günter Klambauer, Johannes Brandstetter, and Sepp Hochreiter. xlstm: Extended long short-term memory. arXiv preprint arXiv:2405.04517, 2024.

Satwik Bhattamishra, Michael Hahn, Phil Blunsom, and Varun Kanade. Separations in the represen- tational capabilities of transformers and recurrent architectures. Advances in Neural Information Processing Systems, 37:36002–36045, 2024.

Marco Bondaschi and Michael Gastpar. Batch universal prediction. In 2024 IEEE International

Symposium on Information Theory (ISIT), pp. 3552–3557, 2024. doi: 10.1109/ISIT57864.2024. 10619270.

Marco Bondaschi and Michael Gastpar. Alpha-NML universal predictors. IEEE Transactions on

Information Theory, 71(2):1171–1183, 2025. doi: 10.1109/TIT.2024.3521221.

N. Cesa-Bianchi and G. Lugosi. Prediction, Learning, and Games. Cambridge University Press,

2006.

Nicola Muca Cirone, Antonio Orvieto, Benjamin Walker, Cristopher Salvi, and Terry Lyons. Theo- retical foundations of deep selective state-space models, 2025. URL https://arxiv.org/ abs/2402.19047.

Róbert Csordás, Kazuki Irie, Jürgen Schmidhuber, Christopher Potts, and Christopher D Manning.

Moeut: Mixture-of-experts universal transformers. arXiv preprint arXiv:2405.16039, 2024.

Tri Dao and Albert Gu. Transformers are SSMs: Generalized Models and Efficient Algorithms

Through Structured State Space Duality. arXiv preprint arXiv:2405.21060, 2024.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

Soham De, Samuel L Smith, Anushan Fernando, Aleksandar Botev, George Cristian-Muraru, Albert

Gu, Ruba Haroun, Leonard Berrada, Yutian Chen, Srivatsan Srinivasan, et al. Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models. arXiv preprint arXiv:2402.19427, 2024.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional transformers for language understanding, 2018. URL https://arxiv.org/ abs/1810.04805.

Benjamin L. Edelman, Ezra Edelman, Surbhi Goel, Eran Malach, and Nikolaos Tsilivis. The

Evolution of Statistical Induction Heads: In-Context Learning Markov Chains, 2024.

Chanakya Ekbote, Marco Bondaschi, Nived Rajaraman, Jason D. Lee, Michael Gastpar, Ashok Vard- han Makkuva, and Paul Pu Liang. What one cannot, two can: Two-layer transformers provably represent induction heads on any-order markov chains, 2025. URL https://arxiv.org/ abs/2508.07208.

Riccardo Grazzi, Julien Siems, Simon Schrodi, Thomas Brox, and Frank Hutter. Is mamba capable of in-context learning? arXiv preprint arXiv:2402.03170, 2024.

Albert Gu and Tri Dao. Mamba: Linear-Time Sequence Modeling with Selective State Spaces. arXiv preprint arXiv: 2312.00752, 2023a.

Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. arXiv preprint arXiv:2312.00752, 2023b.

Albert Gu, Tri Dao, Stefano Ermon, Atri Rudra, and Christopher Ré. Hippo: Recurrent memory with optimal polynomial projections. In Advances in Neural Information Processing Systems, volume 33, pp. 1474–1487, 2020.

Albert Gu, Isys Johnson, Karan Goel, Khaled Saab, Tri Dao, Atri Rudra, and Christopher Ré.

Combining recurrent, convolutional, and continuous-time models with linear state space layers. In Advances in Neural Information Processing Systems, volume 34, pp. 572–585, 2021.

John T Halloran, Manbir Gulati, and Paul F Roysdon. Mamba state-space models can be strong downstream learners. arXiv preprint arXiv:2406.00209, 2024.

Yi Hao, Alon Orlitsky, and Venkatadheeraj Pichapati. On learning markov chains. In Advances in

Neural Information Processing Systems, volume 31, pp. 646–655, 2018.

Roee Hendel, Mor Geva, and Amir Globerson. In-context learning creates task vectors. arXiv preprint arXiv:2310.15916, 2023.

Samy Jelassi, David Brandfonbrener, Sham M Kakade, and Eran Malach. Repeat after me: Trans- formers are better than state space models at copying. arXiv preprint arXiv:2402.01032, 2024.

Federico Arangath Joseph, Kilian Konstantin Haefeli, Noah Liniger, and Caglar Gulcehre. Hippo- prophecy: State-space models can provably learn dynamical systems in context. arXiv preprint arXiv:2407.09375, 2024.

Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In International

Conference on Learning Representations (ICLR), 2015.

Pierre Simon Laplace. Essai philosophique sur les probabilités. Courcier, Paris, France, 1814.

Reprinted by Cambridge University Press, 2009. In the reprint, the estimator appears on page 23.

Chris Lu, Yannick Schroecker, Albert Gu, Emilio Parisotto, Jakob Foerster, Satinder Singh, and

Feryal Behbahani. Structured state space models for in-context reinforcement learning. Advances in Neural Information Processing Systems, 36, 2024.

Ashok Vardhan Makkuva, Marco Bondaschi, Adway Girish, Alliot Nagle, Hyeji Kim, Michael

Gastpar, and Chanakya Ekbote. Local to Global: Learning Dynamics and Effect of Initialization for Transformers. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Ashok Vardhan Makkuva, Marco Bondaschi, Alliot Nagle, Adway Girish, Hyeji Kim, Martin Jaggi, and Michael Gastpar. Attention with Markov: A curious case of single-layer transformers. In The Thirteenth International Conference on Learning Representations, 2025.

N. Merhav and M. Feder. Universal prediction. IEEE Transactions on Information Theory, 44(6):

2124–2147, 1998. doi: 10.1109/18.720534.

William Merrill, Jackson Petty, and Ashish Sabharwal. The illusion of state in state-space models.

arXiv preprint arXiv:2404.08819, 2024.

Eshaan Nichani, Alex Damian, and Jason D Lee. How Transformers Learn Causal Structure with

Gradient Descent. arXiv preprint arXiv:2402.14735, 2024.

Antonio Orvieto, Soham De, Caglar Gulcehre, Razvan Pascanu, and Samuel L Smith. On the univer- sality of linear recurrences followed by nonlinear projections. arXiv preprint arXiv:2307.11888, 2023a.

Antonio Orvieto, Samuel L Smith, Albert Gu, Anushan Fernando, Caglar Gulcehre, Razvan Pascanu, and Soham De. Resurrecting recurrent neural networks for long sequences. arXiv preprint arXiv:2303.06349, 2023b.

Matteo Pagliardini. GPT-2 modular codebase implementation. https://github.com/epfml/ llm-baselines. Accessed: Jan. 2025.

Jongho Park, Jaeseung Park, Zheyang Xiong, Nayoung Lee, Jaewoong Cho, Samet Oymak, Kang- wook Lee, and Dimitris Papailiopoulos. Can mamba learn how to learn? a comparative study on in-context learning tasks. In Proceedings of the 41st International Conference on Machine Learning, 2024.

Jiahao Qin and Feng Liu. Mamba-spike: Enhancing the mamba architecture with a spiking front-end for efficient temporal data processing. arXiv preprint arXiv:2408.11823, 2024.

Alec Radford and Karthik Narasimhan. Improving language understanding by generative pre-training.

2018. URL https://api.semanticscholar.org/CorpusID:49313245.

Nived Rajaraman, Marco Bondaschi, Ashok Vardhan Makkuva, Kannan Ramchandran, and Michael

Gastpar. Transformers on Markov data: Constant depth suffices. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024.

J. Rissanen. Universal coding, information, prediction, and estimation. IEEE Transactions on

Information Theory, 30(4):629–636, 1984. doi: 10.1109/TIT.1984.1056936.

Clayton Sanford, Daniel Hsu, and Matus Telgarsky. One-layer transformers fail to solve the induction heads task, 2024. URL https://arxiv.org/abs/2408.14332.

Yash Sarrof, Yana Veitsman, and Michael Hahn. The Expressive Capacity of State Space Models: A

Formal Language Perspective. arXiv preprint arXiv: 2405.17394, 2024.

Neeraj Mohan Sushma, Yudou Tian, Harshvardhan Mestha, Nicolo Colombo, David Kappel, and

Anand Subramoney. State-space models can learn in-context by gradient descent. arXiv preprint arXiv:2410.11687, 2024.

Jamba Team, Barak Lenz, Alan Arazi, Amir Bergman, Avshalom Manevich, Barak Peleg, Ben

Aviram, Chen Almagor, Clara Fridman, Dan Padnos, et al. Jamba-1.5: Hybrid transformer-mamba models at scale. arXiv preprint arXiv:2408.12570, 2024.

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz

Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in Neural Information Processing Systems, pp. 5998–6008, 2017.

Shida Wang and Beichen Xue. State-space models with layer-wise nonlinearity are universal approximators with exponential decaying memory. Advances in Neural Information Processing Systems, 36:74021–74038, 2023.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Qun Xie and A.R. Barron. Minimax redundancy for the class of memoryless sources. IEEE

Transactions on Information Theory, 43(2):646–657, 1997.

Sang Michael Xie, Aditi Raghunathan, Percy Liang, and Tengyu Ma. An explanation of in-context learning as implicit bayesian inference. arXiv preprint arXiv:2111.02080, 2021.

L Zhu, B Liao, Q Zhang, X Wang, W Liu, and X Wang. Vision Mamba: Efficient visual representation learning with bidirectional state space model. arXiv preprint arXiv:2401.09417, 2024.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

A PRELIMINARIES ON LAPLACIAN SMOOTHING

Laplacian smoothing is a mature and well understood topic. An account can be found, e.g., in Merhav & Feder (1998); Cesa-Bianchi & Lugosi (2006), with some recent updates in Bondaschi & Gastpar (2024; 2025). For the sake of completeness, we provide a brief outline of how it applies to our context. For k-th order Markov data, at every time instant t, the Laplacian add-β estimator applied to the subsequence of tokens with the same context ik

1 ∈X k as the current one is the predictor that minimizes the Bayesian cross-entropy loss in Eq. (3), when the Markov kernel is sampled according to the product Dirichlet distribution Dir(β · 1). We first give an intuition of why this is the case, and we provide a full proof at the end of the section. We consider the binary case X = {0, 1}, but the results can be extended to arbitrary finite alphabets.

Consider a given sequence (xt)T t=1. For every length-k context ik

1 ∈X k, let (xt)|ik 1 be the subsequence of tokens preceded by ik

## 1 Note that, since each sequence (xt) is generated by a k-th order

Markov chain, all the tokens in the sequence with the same length-k prefix share the same conditional probability distribution. Furthermore, since each of the conditional distributions of the chain is randomly chosen independently from the others, the subsequence (xt)|ik

1 is a sufficient statistic to estimate the probability distribution of all the tokens with the same prefix ik

## 1. Therefore, the optimal prediction for a sequence (xt)T

t=1 is given by employing the optimal predictor for each i.i.d. subsequence (xt)|ik

1, for every ik 1 ∈X k. Since each conditional distribution is sampled from a Dirichlet distribution with parameter β, it is well known that the optimal predictor for such subsequences is the add-constant estimator, with constant equal to β. More specifically, if xt−1 t−k = ik

1, then the optimal estimation for xt is

P(k)

β xt+1 = j | xt

1

= nj + β n + 2β, (7)

where nj is the number of times token j appears in the subsequence xt

1|ik 1 = (xℓ∈xt 1: xℓ−1 ℓ−k = ik

1), and n is the length of the subsequence.

We now provide a formal proof of this fact. Theorem 3. Consider the class of all k-th order Markov kernels P = (Pik

1)ik 1∈X k, where each Pik 1 = P(· | ik

1) is a probability distribution on X = {0, 1}. Let each Pik 1 be sampled i.i.d. from Dir(β · 1), and let xk

1 ∼Unif(X k) and xt+1|xt 1 ∼Pxt t−k+1. Then, the predictor f (j)(xt

1) = ˆP(xt+1 = j | xt 1), for j ∈{0, 1}, that minimizes the loss

L ≜−1

T

X t∈[T ]

EP Ext+1

1 ∼P xt+1 · log f (1)(xt

1) + (1 −xt+1) · log f (0)(xt 1)

(8)

is the add-β estimator in Eq. (7), i.e. the minimizer f (j)

∗(xt

1) = P(k) β (xt+1 = j | xt

1), for all t ≥k.

Proof. First note that

L = −1

T

X t

EP Ext+1

1 ∼P xt+1 · log f (1)(xt

1) + (1 −xt+1) · log f (0)(xt 1)

= −1

T

X t

Ext

1Ext+1|xt 1 xt+1 · log f (1)(xt

1) + (1 −xt+1) · log f (0)(xt 1)

= −1

T

X t

Ext

1

Ext+1|xt

1[xt+1] · log f (1)(xt 1) + (1 −Ext+1|xt 1[xt+1]) · log f (0)(xt 1)

.

Let us define the distribution f (1)

∗(xt

1) ≜Ext+1|xt 1[xt+1] and f (0) ∗(xt

1) ≜1 −f (1) ∗(xt

1). Then, we can rewrite the loss as

L = 1

T

X t

Ext

1

−f (1)

∗(xt

1) · log f (1)(xt 1) −f (0) ∗(xt

1) · log f (0)(xt 1)

.

For every t ∈[T] and every xt

1 ∈X t, the term inside the expectation is minimized by picking f (1)(xt

1) = f (1) ∗(xt

1). In fact, note that it can be rewritten as

−f (1)

∗(xt

1) · log f (1)(xt 1) −f (0) ∗(xt

1) · log f (0)(xt 1)

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

= f (1)

∗(xt

1) · log f (1) ∗(xt

1) f (1)(xt

1) + f (0) ∗(xt

1) · log f (0) ∗(xt

1) f (0)(xt

1) −f (1) ∗(xt

1) log f (1) ∗(xt

1)

−f (0)

∗(xt

1) log f (0) ∗(xt

1)

= DKL f∗(xt

1)∥f(xt 1)

+ H(f∗(xt

1)), which is minimized when DKL (f∗(xt

1)∥f(xt 1)) = 0, i.e., when f(xt 1) = f∗(xt 1). We will now show that f∗(xt

1) is precisely the add-β estimator. Consider any context ik 1 and any sequence xt 1 such that xt t−k+1 = ik

1. Let also p ≜Pik 1(1) = P(1 | ik 1). Then, f (1)

∗(xt

1) ≜Ext+1|xt 1[xt+1]

= EPik

1 |xt 1Ext+1|xt 1,Pik 1 [xt+1]

= EPik

1 |xt 1[Pik 1(1)]

= EPik

1 |xt 1|ik 1 [Pik 1(1)], where in the last equation we used the fact that, when xk

1 ∼Unif(X k), the subsequence xt 1|ik 1 is a sufficient statistic for Pik

## 1. Hence,

f (1)

∗(xt

1) = EPik 1 |xt 1|ik 1 [Pik 1(1)]

=

Z 1

0 pβ−1(1 −p)β−1pn1(1 −p)n0 R 1

0 qβ−1(1 −q)β−1qn1(1 −q)n0 dq · p dp

=

R 1

0 pn1+β(1 −p)n0+β−1 dp R 1

0 qn1+β−1(1 −q)n0+β−1 dq

= Γ(n1 + β + 1)Γ(n0 + β)

Γ(n + 2β + 1) · Γ(n + 2β) Γ(n1 + β)Γ(n0 + β)

= n1 + β n + 2β, where we used the fact that Pik

1 ∼Dir(β · 1), that R 1

0 qz1−1(1 −q)z0−1 = Γ(z1)Γ(z0)/Γ(z1 + z0), and that Γ(z + 1) = zΓ(z).

Remark. The proof above is for xk

1 ∼Unif(X k). However, note that the same proof would also work for xk

1 distributed according to any distribution that is independent of the Markov kernel P. If instead the distribution depends on P (e.g., the stationary distribution of the Markov chain), then the proof would fail in the step where xt

1|ik 1 is a sufficient statistic for Pik 1.

Remark. It is important to note that, to be able to implement such a predictor requires in-context capabilities: at inference, in order to optimally predict the next token, the model must be able to look into the previous tokens of the test sequence, and count the tokens with the correct prefix.

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

B MAMBA-BASED LANGUAGE MODELING ARCHITECTURE

Mamba block can be incorporated into a full-fledged language model as follows: let x = (x1, x2, · · ·, xT) ∈X T be an input token-sequence over the alphabet X; here X = {0, 1} as explained in Sec. 2.1. Then, at every t ∈[T], the output of the language model θ is given by the following sequence of equations (Dao & Gu, 2024):

xt = ext ∈Rd, (Embedding)

ut = xt + Mamba(xt

1) ∈Rd, (Mamba)

vt = ut + W2[ReLU(W1ut) ⊙W3ut] ∈Rd, (MLP)

logitt = Wℓvt ∈RS, (Linear)

fθ(xt

1) ≜Pθ xt+1 = · | xt

1

= softmax(logitt) ∈[0, 1]S, (Prediction)

where the parameters ei ∈Rd, W1 ∈R4d×d, W2 ∈Rd×4d and Wℓ∈RS×d are learnable, and fθ(xt

1) is the probability law for the next symbol xt+1 conditioned on the past xt 1. We omit the layer norm here for simplicity. We compactly denote the set of all model parameters as θ, i.e. θ = ({ei}i∈X, θMamba, W1,2,3, Wℓ) ∈RD.

<!-- Page 17 -->

Published as a conference paper at ICLR 2026

C PRELIMINARIES AND PROOF OF THM. 1 AND THM. 4

C.1 EMPIRICAL INSIGHTS

Here we expand upon our empirical observations in 4.2.1, which form the basis of our proof.

State-to-state transition factor at ≈1 for all t ≥1. We empirical evidence supporting this observation in Fig. 4.

Position t at

**Figure 4.** Value of at across positions at convergence.

Convolution window w ≥k + 1. Recalling that k is the Markov order, we empirically observe that the window that w = k + 1 is sufficient for the full Mamba to learn the Laplacian smoothing on kth-order Markov chains. To understand why, note that in the MambaZero architecture above, apart from the MambaZero block, all remaining equations operate on the current token at time t. In the MambaZero block, same as the Mamba block except ReLU, the dependency of the output yt on the previous tokens is due to that of the state Ht on (ext, bt) in the update equation, and of ct in the state projection. Since (ext, bt, ct) depend on the past through the convolutions, a window of size k + 1 enables them to keep track of the current token as well as its length-k prefix, which is necessary to compute the counts needed in Laplacian smoothing. On the other hand, if w ≤k, then one can find confusable sequences, i.e. sequences that share the same number of occurrences of all length-k prefixes, but whose counts of the tokens following each prefix is different.

For such sequences, the state Ht is the same, and so are the predicted probabilities by the Mamba model; however, the optimal estimator, depending on the transition counts, would give very different probability estimates, allowing Mamba’s prediction loss to deviate from that of the optimal. For example, consider k = 1. If w = 1, then (ext, bt, ct) depend only on the current token xt. Then, consider the two sequences x = (0, 1, 0, 1, 0, 1) and ex = (0, 0, 0, 1, 1, 1). At time t = 6, these two sequences would give the same state Ht and the same output yt, since they share the same number of tokens 0 and 1. Therefore, the estimated probability given by the model would be the same in both cases. However, the optimal add-constant estimator (with β = 1) would estimate the probability of xt+1 = 1 to be 1/4 for x, and 3/4 for ex.

Further, it is sufficient that the convolution for ct has window wC = k. That is, the convolution convC involved in the computation of ct can have a window size equal to the Markov order k (i.e., one less than convX and convB) without affecting the model’s capability of learning the task (or, equivalently, the left-most kernel coefficients of convC can be taken to be zero). Intuitively, this is because the role of ct in the state projection is to select the correct transition counts for the computation of the estimator, distilled into yt. In order to do so, it is sufficient to know the length-k context of the current symbol xt, which can be encoded by a convolution with window size k.

Orthogonal count-dependent vectors. The inner products b(ij)⊤c(k) corresponding to i̸ = k go to zero at convergence: only the correct counts are kept in the final logit.

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

Convergence to the optimal β = 1. The count-independent part of the final logit converges to β = 1, corresponding to the optimal Laplacian estimator.

0 100 200 300 400 500 600 700 Iterations

−0.25

0.00

0.25

0.50

0.75

1.00

1.25

1.50

1.75

Inner products b(00)⊤c(0)

b(01)⊤c(0)

b(10)⊤c(0)

b(11)⊤c(0)

(a) Counts-related inner products

0 25 50 75 100 125 150 175 200 Iterations (x10)

0.8

0.9

1.0

1.1

1.2

Value β0 β1

(b) Counts-independent vector

**Figure 5.** (a) Counts-related inner products across interations. Only the correct counts corresponding to b(ij)⊤c(k) for i = k have a non-zero inner product at convergence. (b) Binary coordinates of the counts-independent vector across iterations. Both coordinates converge to the optimal β = 1.

C.2 PROOF OF THM. 1

Let β > 0 be the constant of the considered add-constant estimator. Let us fix a = 0 and ∆t = 1, so that at = 1, for all t ≥1. This can be done by picking, e.g., w∆= 0 and δ such that softplus(δ) = 1. Note that the application of convolution to a given sequence of vectors zt

1 can be rewritten as a linear matrix-form operation. For example, for convX, one has that convX(zt) = D(0)

X zt−1 + D(1)

X zt (9)

where D(0)

X and D(1)

X are diagonal matrices. The same holds for convB and convC, with corresponding diagonal matrices D(0)

B, D(1)

B, D(0)

C and D(1)

C.

Let us take the embedding vectors ei, i ∈X, to be the one-hot encoding vectors for the alphabet X, interleaved with zeros, i.e., let ei be such that ei,2i−1 = 1 and 0 otherwise. Furthermore, take WX to be the 2S × 2S matrix such that WX(i, j) = 1 for i = 2k and j = 2k −1, for 1 ≤k ≤S, and 0 otherwise. (The role of WX is shift each coordinate of the embedding vectors by one.) Take now convX to be such that its output is simply equal to the current vector, i.e., take D(0)

X = 0 and D(1)

X = I2S×2S. Take also WB = IS×S and convB so that the output is equal to the second-to-last vector, i.e., take D(0)

B = IS×S and D(1)

X = 0. Finally, take WC = IS×S and convC such that C(0) = 0 and C(1) = IS×S.

The final logit vector is in general equal to logitt = Wℓxt + WℓWo ex(x1)b(x1)⊤ct +

X ij nij WℓWo ex(ij)b(ij)⊤ct. (10)

Using the matrices chosen above, we can simplify the formula as follows. Firstly, note that b(x1) = 0, as the b vectors only depend on the second-to-last vectors. Furthermore, since the embedding vectors are orthogonal to each other, we have that b(ij)⊤ct = 1 whether i = xt, and 0 otherwise. (That is, only the correct counts are kept in the logit computation.) With these simplifications, the logit formula becomes logitt = Wℓxt +

X j nxt,j WℓWo ex(j). (11)

Finally, take Wo = I2S×2S and take Wℓsuch that Wℓ(i) = β1 for all odd i, Wℓ(2i, i) = 1 for 1 ≤i ≤S, and 0 otherwise. With this choice, we get, for all t ≥1, logitt = β1 +

X j nxt,jei (12)

<!-- Page 19 -->

Published as a conference paper at ICLR 2026 where ei is the one-hot vector for symbol i ∈X. After the normalization, we finally get fθ(xt

1)j = nij + β P k nik + Sβ (13)

if xt = i, for i ∈X. This is precisely the required add-β Laplacian estimator.

C.3 THM. 4: DIMENSIONALITY REDUCTION FOR THE BINARY CASE

Theorem 4. For the canonical MambaZero model with dimensions d = N = 2, e = 1, and convolution window w = 2, there is a choice of parameters such that the model prediction is arbitrarily close to the Laplacian estimator for random first-order Markov chains. More formally, for any β > 0 and ϵ ∈(0, 1), there exists a set of parameters θ such that, for all sequences (xt)t≥1 and all t ≥1,

DKL

P(1)

β (· | xt

1)∥Pθ

· | xt 1

≤ϵ.

Proof. Fix ϵ > 0 and let β > 0 be the constant of the considered add-constant estimator. Let us fix a = 0 and ∆t = 1, so that at = 1, for all t ≥1. This can be done by picking, e.g., w∆= 0 and δ such that softplus(δ) = 1. Let us compactly denote the convolution kernels as convX = α00 α01 α10 α11

, convB = γ00 γ01 γ10 γ11

(14)

where each row corresponds to the kernel weights applied time-wise to each coordinate of the input sequence (xt)t≥1. Since the window for convC is wC = 1, we can simply assume w.l.o.g. that Ct = WCxt.

Let us denote the embedding vectors to be e0 = (e00, e01)⊤and e1 = (e10, e11)⊤, and assume that the vectors are not collinear. Take also WX = WB such that

WX e0 =

1 0

, WX e1 =

0 1

(15)

and take WC such that

WC e0 = c0

0

, WC e1 =

0 c1

. (16)

Let us also take the kernels of convX and convB to be the same across coordinates, i.e., convX = α0 α1 α0 α1

, convB = γ0 γ1 γ0 γ1

(17)

such that the following conditions are satisfied:

    

    α0γ0 + α1γ1 = 0 α0γ1 + α1γ0 > 0 α0̸ = α1 α0γ1 α0γ1+α1γ0 = −βϵ

(18)

Note that, with such a choice of parameters, we have

X(0) = α1

0

, X(1) =

0 α1

, B(0) = γ1

0

, B(1) =

0 γ1

(19)

C(0) = c0

0

, C(1) =

0 c1

(20)

X(00) = α0 + α1

0

, X(01) = α0 α1

, X(10) = α1 α0

, X(11) =

0 α0 + α1

(21)

B(00) = γ0 + γ1

0

, B(01) = γ0 γ1

, B(10) = γ1 γ0

, B(11) =

0 γ0 + γ1

. (22)

<!-- Page 20 -->

Published as a conference paper at ICLR 2026

(We replaced the vector notation of Sec. 4 with matrix notation, so that X(0) has to be intended as ex(0), and so on.) Take also Wo = Wℓ= I. With this choice of parameters, the final logit vector becomes, using Eq. (5), logitt = Wℓ xt + WoX(x1)B(x1)⊤C(xt) + 1{x1̸=xt}WoX(x1xt)B(x1xt)⊤C(xt)

+ nxtxtWo X(xtxt)B(xtxt)⊤Ct + nxt¯xtWo

X(xt¯xt)B(xt¯xt)⊤+ X(¯xtxt)B(¯xtxt)⊤

Ct

(23)

= e00 + c0α1γ1 e01

+ 1{x1=1} ·

0 c0α0γ1

+ n00 ·

(α0 + α1)(γ0 + γ1)c0

0

+ n01 ·

(α0γ0 + α1γ1)c0 (α0γ1 + α1γ0)c0

(24)

= e00 + c0α1γ1 e01

+ 1{x1=1} ·

0 c0α0γ1

+ n00 ·

(α0γ1 + α1γ0)c0

0

+ n01 ·

0 (α0γ1 + α1γ0)c0

(25)

if xt = 0, and logitt = e10 e11 + c1α1γ1

+ 1{x1=0} · c1α0γ1

0

+ n10 ·

(α0γ1 + α1γ0)c1 (α0γ0 + α1γ1)c1

+ n11 ·

0 (α0 + α1)(γ0 + γ1)c1

(26)

= e10 e11 + c1α1γ1

+ 1{x1=0} · c1α0γ1

0

+ n10 ·

(α0γ1 + α1γ0)c1

0

+ n11 ·

0 (α0γ1 + α1γ0)c1

(27)

if xt = 1. Take now e00 = e11 = (α0γ1 + α1γ0)βc0 −α1γ1c0 (28) e01 = e10 = (α0γ1 + α1γ0)βc0 −α0γ1c0 (29)

With this choice of parameters, after the layer normalization, the final output probability vector is fθ(xt

1) = n00 + β n00 + n01 + 2β + 1{x1=0} · βϵ, n01 + β + 1{x1=0} · βϵ n00 + n01 + 2β + 1{x1=0} · βϵ

⊤

(30)

if xt = 0, and fθ(xt

1) = n10 + β + 1{x1=1} · βϵ n10 + n11 + 2β + 1{x1=1} · βϵ, n11 + β n10 + n11 + 2β + 1{x1=1} · βϵ

⊤

(31)

if xt = 1. Note that the resulting predicted probabilities exactly match the add-β estimator when x1̸ = xt, but they are slightly different when x1 = xt due to the additional βϵ factor. We now show that, when the additional factor is present, the two predictors nevertheless differ by at most ϵ in KL distance. We show it for the case x1 = xt = 0, the other case follows in the same way. In fact, note that n01 + β + βϵ n00 + n01 + 2β + βϵ = n01 + β n00 + n01 + 2β ·

1 + βϵ n01+β 1 + βϵ n00+n01+2β

. (32)

Now, since

1 ≤1 + βϵ n01 + β ≤1 + ϵ (33)

<!-- Page 21 -->

Published as a conference paper at ICLR 2026 and

1 ≤1 + βϵ n00 + n01 + 2β ≤1 + ϵ (34)

we have that n01 + β n00 + n01 + 2β ≤ n01 + β + βϵ n00 + n01 + 2β + βϵ · (1 + ϵ) (35)

but we also have n00 + n01 + 2β + βϵ n00 + n01 + 2β ≤1 + βϵ n00 + n01 + 2β ≤1 + ϵ, (36)

so that

DKL

P(1)

β

· | xt 1

∥Pθ

· | xt 1

= P(1)

β xt+1 = 0 | xt

1 log

P(1)

β (xt+1 = 0 | xt

1)

Pθ (xt+1 = 0 | xt

1)

+ P(1)

β xt+1 = 1 | xt

1 log

P(1)

β (xt+1 = 1 | xt

1)

Pθ (xt+1 = 1 | xt

1) (37)

= n00 + β n00 + n01 + 2β log n00+β n00+n01+2β n00+β n00+n01+2β+βϵ

+ n01 + β n00 + n01 + 2β log n01+β n00+n01+2β n01+β+βϵ n00+n01+2β+βϵ

(38)

≤ n00 + β n00 + n01 + 2β log(1 + ϵ) + n01 + β n00 + n01 + 2β log(1 + ϵ)

(39)

≤log(1 + ϵ) (40) ≤ϵ (41)

concluding the proof.

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

D PROOF OF THM. 2

Consider a recurrent model of the form Ht = h(Ht−1, xt) and yt = g(Ht) for each t ≥1 where Ht ∈Rd and the model has a bit precision of p. In this proof, we will assume that the state space of the underlying Markov chain is {0, 1}. By the recurrent architecture, the predicted distribution over the next token xt+k+1 is of the form, yt+k = Pθ xt+k+1 = z | xt+k

1

= g(z, Ht+k). (42)

Recall that the add-1 estimator is defined as, n(z, xt+k t+1) + 1 n(xt+k t+1) + 2

, (43)

where n(zk

1) = Pt+1 i=1 I(xi+k−1 i = zk

1) indicates the number of times zk 1 appears in the sequence. This is the optimal estimator for sequences drawn from the product-Dirichlet prior: for every ik

1, P(· | ik

1) ∼Dir(1 · 1), which is the distribution we will assume for this proof. Fixing xt 1, we can write the add-1 estimator more explicitly as a function of xt+k t+1 as,

P(k)

1 xt+k+1 = z | xt

1, xt+k t+1 = zk

1

= n(zk

1, z) + 1 n(zk

1) + 2. (44)

Now, fixing xt

1, correctness of the recurrent model means that, almost surely over P drawn from the prior, and xt

1 ∼P and zk 1 ∼P(·|xt 1), g(xt+k+1 = 0, Ht+k) ∈P(k)

1 xt+k+1 = 0 | xt

1, xt+k t+1 = zk

1

+ [−ε, ε]. (45)

where Ht+k is a function of xt

1 and zk 1. As t →∞, under the randomness of the draw of xt 1 ∼P, by the strong law of large numbers RHS converges almost surely to the conditional distribution under P, almost surely over the choice of P from the product-Dirichlet prior. Here we use the fact that for P drawn from the product-Dirichlet prior, P(z|zk

1) > 0 almost surely, and so the resulting distributions are exponentially mixing and ergodic. Namely, for each zk

1 ∈{0, 1}k, almost surely over P drawn from the product-Dirichlet prior,

Pr lim sup t→∞

P(k)

1 xt+k+1 = 0 | xt

1, xt+k t+1 = zk

1

−P(0|zk

1) > γ)

= 0 (46)

for any γ > 0. Therefore, a necessary condition to satisfy Equation (45) is, for each zk

1 ∈X k, g(xt+k+1 = 0, Ht+k) ∈P(0|zk

1) + [−ε −ηP (t), ε + ηP (t)]. (47)

for some ηP (t), which is a function of P satisfying lim supt→∞ηP (t) = 0 almost surely over P drawn from the prior; note that Ht+k is implicitly a function of xt

1 and zk 1. Divide the interval [0, 1] into 1/ε disjoint intervals of size ε each. Recall that P(·|zk

1) ∼ρ = Dir(1 · 1), which implies that the random variable P(0|zk

1) for each fixed zk 1 (randomness is over P) is distributed as,

Pr ρ

P(0|zk

1) = · zk

1

= Unif([0, 1]). (48)

Consider the buckets Bε = {[0, ε), [ε, 2ε), · · ·, [1 −ε, 1]}. Define the function round(p): [0, 1] → {0, · · ·, |Bε| −1} to return the index of the bucket in Bε such that p falls in that bucket.

Lemma 1. Consider any function f(zk

1): X k →{0, · · ·, |Bε| −1} such that, pointwise,

|round(P(0|zk

1)) −f(zk 1)| ≤r. (49)

Then, when P(0|zk

1) i.i.d. ∼Dir(1 · 1),

HShannon({f(zk

1): zk 1 ∈{0, 1}k}) ≥2k ((1 −3ε) log(1/ε) −log(2r + 1)) (50)

where the randomness is over the draw of P and HShannon is the discrete Shannon entropy.

<!-- Page 23 -->

Published as a conference paper at ICLR 2026

Proof. Recall that P(0|zk

1) i.i.d. ∼Unif([0, 1]) across zk

1 ∈X k. Then,

Pr(round(P(0|zk

1)) = j) = Pr(P(0|zk 1) ∈[ε(j −1/2), ε(j + 1/2))) (51)

= ε if 1 ≤j ≤|Bε| −2, 3ε/2 if j = 0 or j = |Bε| −1. (52)

This implies that, by independence of the P(0|zk

1)’s across zk 1 ∈X k,

HShannon

P(0|zk

1): zk 1 ∈X k ≥|X|k(1 −3ε) log(1/ε). (53)

Let e(zk

1) be the random variable P(0|zk 1) −f(zk 1). P(0|zk 1) is a measurable function of f(zk 1) and e(zk

1), and therefore,

HShannon f(zk

1): zk 1 ∈X k ∪ e(zk

1): zk 1 ∈X k ≥HShannon

P(0|zk

1): zk 1 ∈X k (54)

Note that e(zk

1) is bounded in the rate {−r, · · ·, r} and can take at most 2r + 1 values. Therefore, H e(zk

1): zk 1 ∈X k ≤|X|k log(2r + 1). Since H(A, B) ≤H(A) + H(B), we have that,

HShannon f(zk

1): zk 1 ∈X k ≥HShannon

P(0|zk

1): zk 1 ∈X k −H e(zk

1): zk 1 ∈X k

(55)

≥|X|k ((1 −3ε) log(1/ε) −log(2r + 1)). (56)

Recall that we are guaranteed that g(xt+k+1 = 0, Ht+k) ∈P(0|zk

1) + [−ε −ηP (t), ε + ηP (t)]. This implies that the recurrent model is able to recover round(p) for p = P(0|zk

1) up to an error of r = ⌈η(t)/ε⌉for each zk

1 ∈X k by computing round(ˆp) where ˆp = g(xt+k+1 = 0, Ht+k). Informally, this just means that ˆp is likely to fall in a bucket close to p. In combination with Lemma 1, for f(zk

1) = g(xt+k+1 = 0, Ht+k) we have that,

HShannon({g(xt+k+1 = 0, Ht+k): zk

1 ∈{0, 1}k}) ≥2k ((1 −3ε) log(1/ε) −log(2⌈ηP (t)/ε⌉+ 1)) (57)

Note however, that g(xt+k+1 = 0, Ht+k) is a function of zk

1 implicitly, through Ht+k (which is also a function of xt

1). Since the dimensionality of Ht+k is d and the model is implemented to p bits of precision,

HShannon({g(xt+k+1 = 0, Ht+k): zk

1 ∈{0, 1}k}) ≤HShannon(Ht+k) ≤dp (58)

where all randomness here is induced by the random draw of the kth-order Markov kernel P. Therefore, for the correctness guarantee Equation (45) to hold, we need, dp ≥2k ((1 −3ε) log(1/ε) −log(2⌈ηP (t)/ε⌉+ 1)) (59)

in the limit t →∞, and noting that lim supt→∞ηP (t) = 0 almost surely over P drawn from the prior, it is necessary that, dp ≥2k(1 −3ε) log(1/ε). (60)

**Fig. 6.** provides empirical evidence that the exponential dependency of the theorem on the order k is consistent.

Remark. The proof above assumes that the kth-order Markov chain is on a binary state space. However, the result can easily be extended to give the lower bound d · p ≥Ω(|X|k) for larger state spaces, as well as similar scaling results for priors Dir(β · 1) for any β > 0. Furthermore, we believe it should be possible to replace the L∞error guarantee in Equation (6) by the KL-divergence between the two distributions without significantly changing the conclusion (d · p = 2Ω(k)).

Intuition. The intuition behind this result is in the manner in which the recurrent architecture carries out computation: by proceeding sequentially and compressing the information from the sequence it has seen thus far at some time t into a small hidden vector, the model does not know what the next

<!-- Page 24 -->

Published as a conference paper at ICLR 2026 k tokens will be: the knowledge of this is vital to be able to compute the add-β estimator at time t + k + 1 with a small memory footprint. Indeed, when the identity of the next k tokens changes, the output of the model at time t + k + 1 must look drastically different (as the add-β estimator corresponds to approximately evaluating P(·|ik

1), which are unrelated distributions under different choices of ik

1). There are ∼22k possible values the set P = {P(·|ik 1): ik 1 ∈{0, 1}k} can take. But when d and p are small, the output of the model just cannot take so many values: it can realize at most 2dp possible sets. In other words, in order to succeed, the recurrent architecture is essentially forced to keep track of the number of occurrences of each ik

1 ∈{0, 1}k in the sequence at each time t, which costs an exponential dependence on k in the hidden dimension/precision.

1 2 3 4 5 Order

0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

Test loss d = 2 d = 4 d = 8 d = 16 d = 32

**Figure 6.** Relation between the Markov order k and the hidden dimension d of the 1-layer Mamba model. The plot shows that d = 2k is sufficient for the model to learn the k-th order Markov task. This corroborates the fact that Theorem 2 in the main paper has the correct order dependency.

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

E ADDITIONAL RESULTS

E.1 LINEAR ATTENTION

0 10 20 30 40 50 60 70 Position

0.3

0.4

0.5

0.6

0.7

0.8

0.9

Predicted probability

1-layer Mamba 1-layer Transformer 2-layer Transformer 1-layer Linear Transformer 2-layer Linear Transformer Optimal estimator

(a) Predicted probability

1 2 3 4 Orders

0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

L1 norm

1-layer Mamba 1-layer Transformer 2-layer Transformer 1-layer Linear Transformer 2-layer Linear Transformer

(b) Test loss

**Figure 7.** Comparison of predicted probability and test loss between a 1-layer Mamba and the other baselines, including linear attention. Mamba outperforms all baselines. Linear attention and softmax attention Transformers perform similarly.

E.2 MULTIPLE STATES

**Fig. 8.** shows that our results extend to larger number of states.

0 5 10 15 20 30 35 Iteration (x 200)

0.0

0.1

0.2

0.3

0.4

0.5

Test loss gap

2 states 4 states 6 states 8 states

(a) Absolute test loss gap

0 5 10 15 20 30 35 Iteration (x 200)

0.0

0.1

0.2

0.3

0.4

0.5

Loss gap relative to optimal

2 states 4 states 6 states 8 states

(b) Relative test loss gap

**Figure 8.** Test loss gap from the optimal for 1-layer Mamba and first-order Markov data, for different number of states. (a) shows the absolute gap L(θ) −L∗; (b) shows the relative gap (L(θ) −L∗)/L∗. The loss gap is consistently small for all state sizes.

E.3 DEEPER NETWORKS

**Fig. 10.** show that our results are consistent with larger number of layers.

E.4 OVER-PARAMETRIZED SETTINGS

**Fig. 9.** shows that our observations hold also for larger convolution width and deeper networks.

<!-- Page 26 -->

Published as a conference paper at ICLR 2026

0 20 40 60 80 100 Iterations

0.0

0.1

0.2

0.3

0.4

Loss gap from optimal w = 2 w = 3 w = 4 w = 5

(a) Convolution width

0 20 40 60 80 100 Iterations

0.0

0.1

0.2

0.3

0.4

Loss gap from optimal ℓ= 1 ℓ= 2 ℓ= 3 ℓ= 4

(b) Depth

**Figure 9.** Test loss gap from optimal across iterations in over-parametrized settings. (a) shows 1-layer Mamba with varying convolution width. (b) shows a Mamba with convolution width w = 2 and varying number of layers. The models correctly learn the optimal predictor in all cases.

1 2 3 4 Order

0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

Test loss

1 layer 2 layers 3 layers 4 layers

(a) Mamba

1 2 3 4 Order

0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

Test loss

1 layer 2 layers 3 layers 4 layers

(b) Transformers

**Figure 10.** Test loss gap from the optimal for Mamba and Transformers, for different number of layers and Markov orders. Mamba has a smaller loss gap than transformers across all orders. Furthermore, adding more layers to Mamba does not significantly improve performance. As expected, 1-layer Transformers cannot solve the Markov task, while 1-layer Mamba can.

E.5 HOLD-OUT EXPERIMENT

We also consider the following interesting experiment: we trained Mamba only on sequences from a subset of the Markov simplex, specifically the interval [0, 0.5], and we tested it on sequences from its complement [0.5, 1]. Interestingly, our experiments show that the test loss still converges to the optimal. However, by inspecting the actual estimated probabilities on a fixed test sequence, we see that the absolute difference between the model’s estimation and the optimal Laplacian smoothing is high for the first samples, and gradually decreases as the sequence progresses. This is justified by the fact that the Laplacian estimator is not only Bayes-optimal, but also minimax optimal (i.e., independently of the prior on the simplex) in the limit of long sequences (i.e., the gap from the optimal loss goes to 0 as n →∞). Table 2 shows the absolute difference |Pθ(xt = 1|xt−1

1) −P∗(xt = 1|xt−1

1)| for several t, showing how this difference gradually goes to zero as t increases.

E.6 CONVOLUTION

**Fig. 11.** shows that adding convolution to transformers (similarly to Mamba) makes the model solve the task with just one layer. On the contrary, Fig. 12 shows that Mamba needs two layers to solve the

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

**Table 2.** Results for the hold-out experiment.

Length t Abs. difference from optimal

1 0.378 ± 0.050 50 0.098 ± 0.039 100 0.007 ± 0.003 300 0.001 ± 0.001 task if convolution is removed. Table 3 shows that a one-layer Mamba without convolution cannot learn the optimal estimator, no matter how wide the model is.

0 10 20 30 40 50 60 70 t: x_t = 0

0.0

0.2

0.4

0.6

0.8

1.0

Predicted probability

1-layer Mamba 1-layer Transformer 1-layer Transformer + convolution Optimal predictor

(a) Predicted probability

0 5 10 15 20 25 30 35 Iteration (x 200)

0.00

0.05

0.10

0.15

0.20

0.25

0.30

0.35

0.40

Test loss

1-layer Mamba 1-layer Transformer 1-layer Transformer + convolution

(b) Test loss

**Figure 11.** Predicted probability and test loss for Transformers with and without convolution. Adding convolution to the K, Q, V matrices of transformers makes the models succeed in learning the Markov task, similarly to 1-layer Mamba.

0 10 20 30 40 50 60 70 t: x_t = 0

0.3

0.4

0.5

0.6

0.7

0.8

0.9

Predicted probability

1-layer Mamba 1-layer Mamba without convolution 2-layer Mamba without convolution Optimal predictor

(a) Predicted probability

0 2 4 6 8 10 12 14 Iteration (x 200)

0.0

0.1

0.2

0.3

0.4

0.5

Test loss

1-layer Mamba 1-layer Mamba without convolution 2-layer Mamba without convolution

(b) Test loss

**Figure 12.** Predicted probability and test loss for the full 1-layer Mamba and a 2-layer Mamba without convolution. Similarly to transformers, Mamba needs two layers to solve the Markov task when convolution is removed.

E.7 SWITCHING MARKOV

Here we detail the switching Markov process more formally:

1. Initialize t = 0.

<!-- Page 28 -->

Published as a conference paper at ICLR 2026

**Table 3.** Experiments on one-layer Mamba without convolution, with varying width. The model does not learn the optimal estimator successfully.

Hidden dimension d Avg. test loss gap from optimal

10 0.113 ± 0.032 100 0.158 ± 0.055 0.140 ± 0.072

## 2 Draw a binary

Markov kernel P with each row sampled i.i.d. from Dir(β · 1). 3. Let xt = S with probability pswitch, or sample xt ∼Pxt t−k+1,: with probability 1 −pswitch. 4. If xt = S, set t = t + 1 and go to step 2; if xt̸ = S, set t = t + 1 and go to step 3.

**Fig. 13.** illustrates the behavior of Mamba on this process when pswitch = 0.01.

0 50 100 150 200 250 300 0.0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8 t: xt = 0

Predicted probability Pθ xt+1 = 1 | xt

1

1-layer Mamba Optimal estimator

(a) Predicted probabilities

0 100 200 300 400 500

0.0

0.2

0.4

0.6

0.8

1.0

Position t at

(b) Value of at across positions

**Figure 13.** One-layer Mamba on switching Markov data. Mamba is able to learn the optimal predictor by forgetting past counts every time a switch token occurs. This is achieved by setting at = 0 at every switch, and at = 1 otherwise.

E.8 FURTHER ABLATION FOR NATURAL LANGUAGE

The fundamental role played by convolution in modeling natural language is demonstrated in Table 1. However, we find that other components, in particular gating factor at, play an essential role as well, when natural language is considered. In Table 4, we show the increase in test perplexity when convolution, gating factor at and non-linearities are individually removed from the full Mamba-2 architecture.

**Table 4.** Perplexity results on the WikiText-103 dataset.

## Model

Params. Perplexity Percentage increase

Mamba-2 (full) 14.54 M 27.55 – Mamba-2 (w/o conv) 14.53 M 30.68 11% Mamba-2 (w/o gating factor) 14.54 M 32.16 17% Mamba-2 (w/o non-linearities) 14.54 M 28.98 5%

<!-- Page 29 -->

Published as a conference paper at ICLR 2026

**Table 5.** Perplexity results on WikiText-103 and PG-19 datasets for Mamba with 12 layers.

Dataset Model Params. Perplexity

WikiText-103 Mamba-2 110 M 21.38 WikiText-103 Mamba-2 w/o convolution 110 M 21.46 WikiText-103 Mamba-2 w/o gating 110 M 21.71

PG-19 Mamba-2 200 M 14.16 PG-19 Mamba-2 w/o convolution 200 M 14.28 PG-19 Mamba-2 w/o gating 200 M 14.66

<!-- Page 30 -->

Published as a conference paper at ICLR 2026

F MODEL ARCHITECTURES AND HYPER-PARAMETERS

The following tables discuss details on the architectures and hyperparameters used in all the paper’s experiments. Each experiment was run on a single Nvidia A100 GPU. The time taken by each experiment was between 10 to 60 minutes.

**Table 6.** Parameters in the Mamba architecture with their shape.

Parameter Matrix shape embedding 2 × d mamba.A 1 mamba.dt 1 mamba.in_proj (2ed + 2N + 1) × d mamba.conv1d (ed + 2N) × w mamba.out_proj d × (2ed + 2N + 1) mlp.fc1 4d × d mlp.fc2 d × 4d lm_head d × 2

**Table 7.** Settings and parameters for the Mamba model used in the experiments.

Dataset k-th order binary Markov source Architecture Based on the Mamba-2 architecture as implemented in Dao & Gu (2024)

Batch size Grid-searched in {16, 32, 64, 128, 256} Accumulation steps 1

Optimizer AdamW (β1 = 0.9, β2 = 0.95) Learning rate 0.001 Scheduler Cosine # Iterations 10000 Weight decay 1 × 10−3

Dropout 0 Sequence length Grid-searched in {128, 256, 512} Embedding dimension Grid-searched in {2, 4, 8, 16, 32} Mamba layers 1 Heads 1 Convolution window Between 2 and 6

Repetitions 5

**Table 8.** Parameters in the transformer architecture with their shape.

Parameter Matrix shape transformer.wte 2 × d transformer.wpe N × d transformer.h.ln_1 (×ℓ) d × 1 transformer.h.attn.c_attn (×ℓ) 3d × d transformer.h.attn.c_proj (×ℓ) d × d transformer.h.ln_2 (×ℓ) d × 1 transformer.h.mlp.c_fc (×ℓ) 4d × d transformer.h.mlp.c_proj (×ℓ) d × 4d transformer.ln_f d × 1

<!-- Page 31 -->

Published as a conference paper at ICLR 2026

**Table 9.** Settings and parameters for the transformer model used in the experiments.

Dataset k-th order binary Markov source Architecture Based on the GPT-2 architecture as implemented in Pagliardini

Batch size Grid-searched in {16, 32, 64, 128, 256} Accumulation steps 1

Optimizer AdamW (β1 = 0.9, β2 = 0.95) Learning rate 0.001 Scheduler Cosine # Iterations 10000 Weight decay 1 × 10−3

Dropout 0 Sequence length Grid-searched in {128, 256, 512, 1024} Embedding dimension Grid-searched in {4, 8, 16, 32} Transformer layers Between 1 and 2 depending on the experiment Attention heads 1

Repetitions 5
