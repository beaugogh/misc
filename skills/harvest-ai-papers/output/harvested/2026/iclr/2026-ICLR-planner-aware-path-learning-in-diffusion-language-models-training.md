---
title: "Planner Aware Path Learning in Diffusion Language Models Training"
source_url: https://iclr.cc/virtual/2026/oral/10007708
paper_pdf_url: https://arxiv.org/pdf/2509.23405v3
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Planner Aware Path Learning in Diffusion Language Models Training

<!-- Page 1 -->

PLANNER AWARE PATH LEARNING IN DIFFUSION LAN- GUAGE MODELS TRAINING

Fred Zhangzhi Peng1,‡,∗, Zachary Bezemek1,‡,∗, Jarrid Rector-Brooks2,3,4, Shuibai Zhang5, Anru R. Zhang1, Michael Bronstein6,7, Alexander Tong7†, Avishek Joey Bose2,6,8†

## 1 Duke University 2 Mila 3

Universit´e de Montr´eal 4 California Institute of Technology 5 University of Wisconsin–Madison 6 University of Oxford 7 AITHYRA 8 Imperial College London ‡ Equal contribution † Equal advising

## ABSTRACT

Diffusion language models have emerged as a powerful alternative to autoregressive models, enabling fast inference through more flexible and parallel generation paths. This flexibility of sampling is unlocked by new engineered sampling strategies, or planners, that select more favorable generation paths by iteratively planning—versus uniformly at random—where to denoise along the sequence. However, by modifying the reverse paths via planning, planners create an irrevocable mismatch between the uniformly random denoising paths assumed during training and planning-based inference. In this paper, we systematically investigate the mismatch of discrete diffusion training and inference under planning and theoretically prove that the standard discrete diffusion training evidence lower bound (ELBO) does not accurately describe a denoiser that uses a non-uniform planner. To address this gap, we derive a new planned evidence lower bound (P-ELBO) that incorporates planner-based reverse dynamics directly into the training objective. Using the P-ELBO, we introduce Planner Aware Path Learning (PAPL), a novel training scheme that aligns training and inference under a planned denoiser. PAPL is implemented as a simple yet effective modification to the standard masked discrete diffusion loss, making it widely applicable and easy to adopt. Empirically, we show PAPL delivers consistent gains across domains, including a 40% relative improvement in protein sequences, improved text generation with up to a 4× relative MAUVE gain, and 23% relative improvement in code generation HUMANEVAL pass@10. Code is available at github.com/pengzhangzhi/PAPL.

## INTRODUCTION

The landscape of generative modeling over discrete data has led to foundational breakthroughs in deep learning, with Large Language Models (LLMs) being an exemplary technology that has transcended beyond natural language processing (Achiam et al., 2023). Until recently, the de facto gold standard for building LLMs has been Autoregressive models (ARMs), which are highly scalable for pre-training LLMs—allowing them to capture complex dependencies in data—but incur rigid inference schemes due to the autoregression mechanism that generates samples in a causal order—e.g., left to right for natural language (Guo et al., 2025). In contrast to ARMs, recent advances in Diffusion Language Models (DLMs) have the potential to disrupt the current status quo for generative modeling of discrete data, as they natively support flexible generation orders and allow for fully parallel sampling of tokens at inference time (Austin et al., 2021a; Lou et al., 2024; Sahoo et al., 2024; Shi et al., 2024). The increased flexibility of modeling discrete data in any order makes DLMs arguably a more natural tool than ARMs for tackling high-impact problem domains that lack a natural causal ordering, such as biological sequence design and code completion (Nie et al., 2025a; Wang et al., 2024; 2025b), spurring their rapid recent development and application (Song et al., 2025).

Indeed, the most performant variant of DLMs, i.e., Masked Diffusion Models (MDMs) (Shi et al., 2024; Sahoo et al., 2024), approach generative modeling as a denoising task, wherein partially masked

∗Correspondence to zp70@duke.edu and zwb@duke.edu arXiv:2509.23405v3 [cs.LG] 5 Mar 2026

<!-- Page 2 -->

sequences are iteratively refined using a learned denoiser that time-reverses the Markov transition dynamics of the masked corruption process. However, a key assumption, and thus a central limitation, of DLMs is that following the reverse dynamics of uniformly denoising a position at inference implicitly assumes denoising with a perfect denoiser (Peng et al., 2025a). As a result, in practice, to fully take advantage of flexible generation paths and generate higher-quality samples beyond uniform decoding, the reverse process must be modified by a planner: a rule that selects which tokens to reveal next, such as greedy decoding (Chang et al., 2022), ancestral sampling (Shi et al., 2024; Schiff et al., 2025), or Path planning (P2) (Peng et al., 2025a). In fact, using a planning strategy is more than a humble artefact of optimizing for inference; it can be seen as avoiding denoising over exponential infilling problems at inference—unlike training, in which the task is provably computationally intractable (Kim et al., 2025). More than just theory, employing a planner when denoising has been shown to substantially improve sample quality across various application domains, including text, code, protein sequences, and discrete image modeling (Peng et al., 2025a; Nie et al., 2025a; Shi et al., 2024).

A fundamental aspect of DLM inference under planning is the fact that denoising is not necessarily conducted by uniformly picking a position to unmask. Consequently, this new reverse process creates an irrevocable mismatch between the forward masking process, used during training, which corrupts sequences by masking positions uniformly at random. This mismatch of forward and reverse processes also suggests that, in effect, training denoisers in DLMs attempts to solve a harder problem than the one they are ultimately used for. This raises the following central question:

Q. How should we adapt the training of denoisers in diffusion language models when inference inevitably proceeds under a planner?

Present work. In this paper, we seek to answer the question by introducing a new theoretical framework that aims to align the training of DLMs with pre-assumed knowledge of planner-based inference. Our framework is built using basic facts of Markov chains, which allows us to set up the training of DLMs as minimizing a path-wise KL divergence. More precisely, the path-wise KL is between the reverse dynamics of a DLM using a planner and supervised ideal reverse dynamics, also under planning, that hit the data distribution.

Armed with this path-wise KL, we first theoretically prove in §3.1 how greedy ancestral sampling at inference of DLMs violates the standard DLM ELBO (Sahoo et al., 2024; Shi et al., 2024)—validating the thesis of a mismatch of forward and reverse dynamics under planning. We next derive a new planned evidence lower bound (P-ELBO) in §3.2, of which the standard planning-agnostic—i.e., uniformly at random denoising—DLM ELBO is a special case. Furthermore, we demonstrate recent heuristics that act as planners, such as MaskGIT (Chang et al., 2022), and P2 (Peng et al., 2025a), emerge as principled instances of our new P-ELBO, which unifies existing strategies under one umbrella. Given the insights in P-ELBO, we propose a new loss function for training the denoiser that directly incorporates any choice of planner, and thereby allows training to match inference properly. We summarize our main contributions in this paper as follows:

• Unifying framework. We derive a novel generalized planner-aware generalized lower bound (P-ELBO) that takes into account the use of planning in the reverse dynamics of a DLM. • Efficient implementation. Starting from the P-ELBO, we design a new simplified loss termed Planner Aware Path Learning (PAPL) that amounts to a one-line code change and uses self-planning. Specifically, PAPL leverages the denoiser itself—i.e., places where the denoiser is most confident— to compute a weighted loss on more likely generation paths compared to standard DLMs. • Improved performance. Empirically, PAPL consistently improves the quality of diffusion language models under identical configurations. We observe PAPL in protein sequence generation yields a 40% relative increase in foldability, surpassing larger diffusion and autoregressive baselines while preserving diversity. On code generation, PAPL improves HUMANEVAL pass@1 from 18.5 to 20.8, pass@10 from 31.1 to 38.4, and HUMANEVAL-INFILL pass@1 from 30.0 to 32.5. On text generation, PAPL achieves up to a 4× improvement in MAUVE and reduces generative perplexity by over 40% compared to prior diffusion models.

BACKGROUND AND PRELIMINARIES

Notation. Let V = {1,..., d} denote a finite vocabulary. We reserve the final symbol, d = m, as a special mask token, while the remaining d −1 symbols correspond to ordinary vocabulary items. We

<!-- Page 3 -->

consider sequences of length L, so that a data point is represented as x = (x1,..., xL) ∈VL. The empirical data distribution pdata is supported on a training set D ⊂VL. We denote by ∆d = {u ∈Rd: ui ≥0, Pd i=1 ui = 1} the probability simplex. Each u ∈∆d specifies a categorical distribution Cat(j; u) = uj over j ∈V. For a particular token x ∈V, we write δ(x) ∈∆d for the one-hot distribution that places all its mass on x. To avoid ambiguity, we use superscripts (e.g., xi) to index sequence positions, and subscripts (e.g., xt) to index time steps of a stochastic process. For x, y ∈VL, we use dHAM(x, y) to denote the Hamming distance between x and y. We also use NM(x) to denote the number of coordinates in x which are equal to m. For a finite set S, we use Unif(S) to denote the uniform distribution on that set. For l < n ∈N, we denote by [l: n] = {l, l + 1,..., n}.

## 2.1 MASKED DIFFUSION LANGUAGE MODELS

A masked diffusion language model (MDLM) generates samples from a data distribution pdata ∈∆dL through an iterative sampling process which gradually denoises a full mask sequence [m]L to a sequence which does not contain any masks. This iterative sampling procedure makes use of a denoiser Dθ: VL →(∆d)L, which outputs a distribution over the clean tokens at each position. In particular, for x ∈VL and y ∈V, y̸ = m, Cat(y; Di θ(x)) approximates the probability that the i’th token in a sequence is y given the unmasked positions in the sequence match those of x (Hoogeboom et al., 2022; Sahoo et al., 2024; Shi et al., 2024; Zheng et al., 2025; Ou et al., 2025).

Moreover, the Gillespie sampling scheme (Gillespie, 1977; 1976) allows us to establish an exact equivalence between DLM and any-order autoregressive model (AOARM) (Uria et al., 2014; Hoogeboom et al., 2022). More precisely, the Gillespie sampling scheme allows for a single coordinate to be denoised at each step. Concretely, starting from the fully masked sequence, the procedure iteratively (1) selects a position uniformly at random among the currently masked tokens, (2) samples a replacement token from the denoiser’s predictive distribution at that position, and (3) updates the sequence by filling in the chosen token while leaving all other positions unchanged.

Let punif θ be the distribution on VL of xL resulting from applying the above iterative sampling procedure in which the masked coordinate to denoise is chosen uniformly at random. This uniform unmasking process is the main sampling strategy employed by MDLMs (Sahoo et al., 2024; Shi et al., 2024). The connection between MDLMs and AOARMs (Ou et al., 2025) can be seen more explicitly through the MDLM evidence lower bound (ELBO), which lower bounds the log marginal log(punif θ (x0)), log(punif θ (x0)) ≥Eθ,unif(x0) = Eσ∼Unif(ΣL)

" L X i=1 log

Cat(xσ(i)

0; Di θ xσ(<i)

0 #

(1)

= LEk∼Unif([0:L−1])



Exk∼Unif(XL−k(x0))





L X i=1,xi k=m

1 L −k log

Cat xi

0; Di θ(xk)







, where ΣL is the set of all permutations of length L. Additionally, for σ ∈ΣL, we denote σ(< i) as the first i −1 elements of σ. Thus, for x ∈VL, xσ(<i) ∈VL has coordinates in σ(< i) set to those of x and the rest set to m, and for x ∈VL and k ∈[0: L], Xk(x) ⊂VL is the set of sequences which are the same as x but with exactly k coordinates masked.

Existing DLM Sampling Strategies. While the vanilla masked diffusion sampler proceeds by unmasking one position chosen uniformly at random, a variety of alternative planners have been proposed to improve generation quality by biasing the unmasking order. A straightforward modification is greedy decoding as in MaskGIT (Chang et al., 2022), where at each step the denoiser selects the position with the highest confidence to unmask next (Gong et al., 2025). Another line of work introduces remasking, where previously generated tokens may be reverted to the mask state and resampled. Resampling diffusion models (RDM) (Zheng et al., 2023) extend greedy planning with resampling. More recently, path planning (P2) (Peng et al., 2025a) has been proposed as a unifying framework that generalizes all of the above strategies. P2 decomposes each step into a planning stage, where a planner chooses positions to update—including both masked and already unmasked tokens—and a denoising stage, where the selected positions are resampled with the denoiser.

<!-- Page 4 -->

P

A

P

L

[M]

[M]

[M]

[M]

P

A

P

L

P

A

P

L

P

A

P

L

[M]

[M]

[M]

[M]

[M]

[M]

P

A

P

L

[M]

[M]

[M]

[M]

P

A

P

L

P

A

P

L

P

A

P

L

[M]

[M]

[M]

[M]

[M]

[M]

Standard Uniform Training Planner Aware Path Learning

**Figure 1.** Planner-Aware Path Learning (PAPL) resolves training–inference mismatch in DLMs. Standard uniform training for DLMs (left) applies a uniform loss across all masked positions, distributing capacity over regions that inference-time planners never traverse. PAPL (right) introduces planner-aware weights into the loss, aligning training with the planner’s preferred trajectories (outlined arrows) and eliminating training-inference mismatch.

## 3 METHOD: PATH LEARNING

We now present Planner-aware Path Learning (PAPL), aiming to align training with planner-based inference. In §3.1, we introduce a general formulation of sampling with a planner and derive the corresponding transition probabilities. In §3.2, we show that greedy sampling modifies these dynamics in a way that departs from the MDLM ELBO, motivating the need for a new objective. We then derive a planner-aware ELBO in(P-ELBO) §3.3, from which different sampling schemes—including uniform and greedy ancestral—emerge as special cases (§A.2). Finally, in §3.4, we simplify the P-ELBO into an efficient training objective, leading to our final efficient (PAPL) algorithm (Alg. 1).

Discrete-time Markov Chains. The starting point for our analysis is to re-examine the ELBO in Equation (1) through the lens of a continuous time Markov chain (CTMC) (Campbell et al., 2022; 2024; Lou et al., 2024; Sun et al., 2023). From the CTMC perspective, the sampling path of a DLM can be compared against a family of reference chains parameterized by a sample x0, which generates that specific datum. For ease of presentation, we forego lifting to this continuous perspective and instead compute the ELBO via a discrete-time Markov chain of the DLM Xθ to that of a family of reference discrete Markov chains Y, before taking appropriate limits to recover the continuous perspective. Specifically, for a datum x0 we have discrete Markov chains of length L which satisfy Xθ

0 d= Y x0

0 and Y x0

L = x0.

We now recall that the transition matrix Q for a discrete time Markov chain X encodes Q(y, x) = P(Xk+1 = y|Xk = x). From this perspective, for vanilla DLMs we have punif θ (x) = P(Xθ

L = x) where Xθ

0 = [m]L and Xθ’s dynamics are described the transition matrix, given by:

Qθ(y, x) =

Cat(yi; Di θ(x))/NM(x), dHAM(x, y) = 1, xi = m, yi̸ = m 0, otherwise, where dHAM is the hamming distance and x, y ∈VL. We compare to Y x0 with Y x0

0 = [m]L and define the transition matrices as follows:

R(y, x; x0) =

Cat(yi; δ(xi

0))/NM(x), dHAM(x, y) = 1, xi = m, yi̸ = m 0, otherwise. (2)

In this view, the second expression of equation 1 is can be rewritten as:

Eθ,unif(x0) = LEk∼Unif([0:L−1])



Exk∼rk(·;x0)



X y∈VL

R(y, xk; x0)) log

Qθ(y, xk)

R(y, xk; x0)







, (3)

where we set rk(x; x0) = P(Y x0 k = x). We rederive the ELBO from this perspective by stating the (discrete) path wise KL divergence in our Proposition §A.7. Importantly, this ELBO enjoys a simple interpretation in how the denoised coordinates are chosen—a fact which will later develop to incorporate coordinates chosen under a planner in Proposition 3.2. Moreover, this perspective is more easily amenable to modifying the sampling dynamics for Xθ and deducing the corresponding ELBO.

![Figure extracted from page 4](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

## 3.1 REVERSE DYNAMICS WITH A PLANNER

We begin by introducing a planner function Gϕ: VL × VL →∆L that modifies the sampling process by selecting in reverse transition which coordinate in the sequence to be denoised next. For simplicity, we assume the planner only selects masked positions, i.e. Cat(i; Gϕ(z, x)) = 0 whenever xi̸ = m— matching greedy ancestral sampling (Nie et al., 2025a). Under these dynamics, each backwards step can be decomposed into two substeps as follows: 1.) starting from the current sequence xk, the denoiser produces candidate predictions z ∼Dθ(xk) for all positions. 2.) The planner then samples an index i ∼Gϕ(z, xk), and the token at this index is updated by setting xi k+1 = zi while all other positions remain unchanged. Thus, each transition from xk to xk+1 differs at exactly one coordinate.

The probability of unmasking the i-th coordinate of xk to token y, after marginalizing over z can be explicitly written as a transition kernel qi θ,ϕ(y|xk) as follows:

qi θ,ϕ(y|xk) = Cat y; Di θ(xk)

Fθ,ϕ(xk, y, i) (4)

Fθ,ϕ(x, y, i):= Ez∼Dθ(x)

Cat i; Gϕ(z−i,y, xk)

, (5)

where z−i,y denotes the same sample z except that the i-th component has been replaced with y.

## 3.2 GREEDY ANCESTRAL VIOLATES THE VANILLA DLM ELBO

Greedy ancestral sampling (Nie et al., 2025a), as widely used in the literature (Gong et al., 2025; Besnier et al., 2025) such as MaskGIT (Chang et al., 2022), employs a specific choice of planner which selects the most confident position according to the denoiser itself,

Gϕ(z, xk) = δ arg max j:xj k=m

Cat(zj; Dθ(xk))

!

. (6)

Unfortunately, when using greedy sampling, the standard DLM ELBO may not, in fact, satisfy the ELBO inequality. Using the transition probabilities equation 4, we prove the following:

Proposition 3.1. For pgreedy θ (x0) defined with Gϕ in equation 6 and Dθ an imperfect denoiser, we may have log(pgreedy θ (x0)) < Eθ,unif(x0), where Eθ,unif(x0) is as in equation 1.

We prove Proposition 3.1in §A.1.7. The key takeaway is that the ELBO in equation 1 is only valid for the uniform unmasking process punif θ. As a result, the reverse dynamics of greedy sampling no longer match those assumed by the standard training loss. In a nutshell, the model is being trained for uniform unmasking, but inference follows a different process. More broadly, this insight applies to any planner: whenever the sampling procedure deviates from uniform, the training objective no longer strictly reflects the quality of the generated samples.

We remark that the proof of Proposition 3.1 hinges on constructing an explicit counter-example, in particular assuming the denoiser is inconsistent along different paths: That is, we assume in our construction that there are two different permutations σ, ¯σ of [1: L] and x0 ∈VL a clean sequence in the data distribution such that QL i=1 Cat xσ(i)

0; Di θ xσ(<i)

0 ̸

= QL i=1 Cat x¯σ(i)

0; Di θ x¯σ(<i)

0

. Indeed, for a perfect denoiser, in the above we would have equality for any x0, σ, and ¯σ, and sampling along any path σ would always result in a sample from the data distribution. In this situation, there would be no point of planning a generation path. However, in practice there is no relationship being enforced between these quantities, and it has been observed repeatedly in the literature that the “path”=“denoising order” taken greatly influences sample quality - see, e.g. Ou et al. (2025) Appendix

J.4, Shih et al. (2022) Section 4, and Li et al. (2021) Section 6.

## 3.3 PLANNER-AWARE EVIDENCE LOWER BOUND

The key mismatch is that vanilla DLM training assumes uniform unmasking, while inference instead follows a planner. To correct this, we next introduce a planner-aware ELBO (P-ELBO) that explicitly accounts for the planner’s role in the reverse dynamics.

<!-- Page 6 -->

Proposition 3.2. For any planner Gϕ, let pGϕ θ denote the distribution of xL obtained via the planner-guided sampling scheme. Then we have the following ELBO:

log(p

Gϕ θ (x0)) ≥Eθ,ϕ(x0) = Eθ,ϕ

1 (x0) + Eθ,ϕ

2 (x0),

Eθ,ϕ

1 (x0) = L E k∼Unif([0:L−1])



 E xk∼r

Gϕ k (·;x0)

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))





Eθ,ϕ

2 (x0) = −L E k∼Unif([0:L−1])



 E xk∼r

Gϕ k (·;x0)

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(i; Gϕ(x0, xk))

Fθ,ϕ(xk, xi

0, i)



, where rGϕ k is the distribution at time k of a Markov chain with initial data (m,..., m) and transition rates as in equation 2 but with 1/NM(x) replaced by Gi ϕ(x0, x).

A proof of this ELBO from a self-contained, discrete-time Markov chain perspective can be found in §A.1.4 and from a continuous time Markov chain perspective in §A.3.3. The first term Eθ,ϕ

1 resembles the standard DLM ELBO: it is the log-probability of predicting the correct token in each masked position, but now weighted by the probability that the planner would choose that position next. In other words, it is a planner-weighted cross-entropy.

The second term Eθ,ϕ

2 is new. It appears only when the planner’s decision can depend on the full clean target sequence x0. Intuitively, it measures the gap between (a) the “ideal” planner that has access to the ground truth, and (b) the “effective” planner that only relies on the denoiser’s predictions, and mathematically is the negative KL divergence between these two distributions. We highlight that for the uniform planner setting, this term vanishes, recovering the standard DLM ELBO. Putting this together, the planner-aware loss used for training is simply the negative ELBO from Proposition 3.2 L(θ, ϕ) = −Ex0∼pdata

Eθ,ϕ(x0)

, which minimizes the KL divergence between the planner-guided model distribution pGϕ θ and the data. We curate results on how several common existing instantiations of planned denoising fall into this framework and their corresponding ELBOs in §A.2. We also prove a result identifying the form of the optimal planner for a fixed denoiser under the trainling loss associated to the ELBO from Proposition 3.2 in §A.1.5.

## 3.4 EFFICIENT IMPLEMENTATION OF PLANNER AWARE PATH LEARNING (PAPL)

## Algorithm

## 1 PAPL

Training

1: while not converged do 2: x0 ∼pdata(x) 3: k ∼Unif([0: L −1]) 4: xk ∼Unif(XL−k(x0)) 5: wi ←Cat(i; Gτ ϕ(x0, xk)) for all masked i 6: // Setting α = 0 recovers standard DLM training 7: LPAPL ←−P 1 L−k(1 + αwi) log Cat(xi

0; Di θ(xk)) 8: Update parameters θ using ∇θLPAPL 9: end while 10: return Trained denoiser Dθ

Greedy decoding is widely used at inference and often improves sample quality. A natural idea is therefore to train the denoiser under the same greedy planner but with corrections such that we optimize the P-ELBO. Unfortunately, the exact greedy ELBO from Cor. A.9 is computationally infeasible: simulating the greedy path for each data point requires k denoiser evaluations at step k, whereas vanilla DLM training needs only a single forward pass. Consequently, we aim to design an efficient algorithm that still falls within our theoretical framework of training under planning.

Soft greedy planner. We relax the deterministic argmax in Equation (6) into a softmax:

Cat(j; Gτ ϕ(z, x)) ∝exp

1 τ log Cat zj; Dj θ(x)

, where τ is the softmax temperature. This assigns higher weight to positions where the denoiser is confident, and reduces to uniform sampling as τ ↑∞and greedy sampling as τ ↓0. Specializing Prop. 3.2 to Gτ ϕ yields a planner-weighted cross-entropy plus a complex correction term as outlined in Corollary A.10. Detaching gradients through the planner removes the correction term, leaving only the simple weighted cross-entropy. This makes the objective stable and efficient.

<!-- Page 7 -->

Stabilization. Instead of simulating planner-driven paths to sample xk, we reuse the vanilla DLM masking scheme: mask L −k positions uniformly at random. This keeps training as cheap as standard DLM. In practice, the pure weighted loss can have high variance, as shown in the training curves Fig. 5. We stabilize this by interpolating with the vanilla DLM loss. The resultant effect is that the uniform weights 1/(L −k) are replaced with planner-adjusted weights: 1 L−k(1 + αwi), where the weights are wi ∝Cat(i; Gτ ϕ(x0, xk)) and α controls the strength of planner weighting.

Final objective. The resulting Planner-Aware Path Learning (PAPL) loss is therefore just the standard masked diffusion cross-entropy, augmented with planner weights:

LPAPL(θ) = −Ex0,k,xk



X i: xi k=m

1 L−k(1 + αwi) log

Cat(xi

0; Di θ(xk))



. (7)

This amounts to a one-line modification of the vanilla DLM loss, making PAPL easy to adopt. We detail the connection between the softmax regularized training objective from Corollary A.10 and the PAPL training objective equation 7 in §A.2.3.

## 4 EXPERIMENTS

We evaluate PAPL on protein sequence generation, text and code generation, domains that demand non-trivial structure. Across domains, we compare against (i) the masked diffusion language model (DLM) baseline (same architecture, size, and training setup as PAPL), (ii) prior autoregressive and diffusion-based models (cf. §B for details).

## 4.1 PROTEIN SEQUENCE GENERATION

**Figure 2.** Visualization of PAPL generated proteins folded with ESMFold.

Setup. We evaluate PAPL on the task of protein sequence generation. We train a 150M DLM baseline and a PAPLaugmented variant under identical configurations. During inference, both models use P2 sampling. For evaluation, each model generates 100 sequences at lengths 200, 300,..., 800, which are folded into 3D structures using ESMFold (Lin et al., 2023). Structural quality is measured by pLDDT, pTM, and pAE; diversity is measured by token-level entropy and sequence uniqueness. To obtain a single robust metric of functionality, we define a sequence as foldable if it simultaneously satisfies pLDDT > 80, pTM > 0.7, and pAE < 10. Comparisons include diffusion-based baselines (EvoDiff (Alamdari et al., 2023), DPLM (Wang et al., 2024)) and autoregressive baselines (ESM3 (Hayes et al., 2025), ProGen2 (Nijkamp et al., 2023)). See §B.1 for further details.

**Table 1.** Protein sequence generation benchmark. We evaluate structure quality via pLDDT, pTM, and pAE, and diversity via token entropy and sequence uniqueness. Foldability is the percentage of sequences satisfying pLDDT > 80, pTM > 0.7, and pAE < 10.

## Model

pLDDT↑ pTM↑ pAE↓ Foldability (%)↑ Entropy↑ Diversity (%)↑

Large

ESM3 34.13 0.23 24.65 1.50 3.99 93.44 ProGen2-medium 57.94 0.38 20.81 12.75 2.91 91.45 ProGen2-large 55.07 0.35 22.00 11.87 2.73 91.48 DPLM-650M 79.53 0.66 11.85 49.14 3.18 92.22

150M-scale

EvoDiff 31.84 0.21 24.76 0.43 4.05 93.19 ProGen2-small 49.38 0.28 23.38 4.48 2.55 89.31 DPLM-150M 80.23 0.65 12.07 48.14 3.14 92.80 DLM-150M 81.32 0.65 12.00 42.43 3.21 92.45 DLM-150M + PAPL (ours) 81.48 0.72 8.97 59.40 3.12 91.73 Results. Table 1 reports quantitative results. Compared to the DLM-150M baseline, PAPL achieves higher pLDDT (81.48 vs. 81.32), stronger pTM (0.72 vs. 0.65), lower pAE (8.97 vs. 12.00), and yields a 40% relative increase in foldability (59.40% vs. 42.43%). Importantly, entropy (3.12) and diversity (91.73%) remain on par with the baseline, confirming that improved folding does not induce collapse. PAPL-trained models outperform EvoDiff and ESM3 in all structural metrics, even when compared to DPLM-650M and ProGen2-2.7B. Figure 2 visualizes 3D folds of sequences generated by PAPL, which exhibit well-formed helices and sheets with coherent tertiary organization.

![Figure extracted from page 7](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

Takeaway. By aligning the training objective with the inference-time planner, PAPL significantly improves the structural plausibility of generated proteins. This is achieved under identical model configurations and without sacrificing diversity, outperforming all baselines.

## 4.2 TEXT GENERATION

Setup. We evaluate PAPL on unconditional text generation using the OPENWEBTEXT (Gokaslan & Cohen, 2019) (OWT) corpus, a large-scale collection of web pages designed to replicate the distribution of OpenAI’s WebText. Text is tokenized with the GPT-2 byte-pair tokenizer, and sequences are wrapped to a maximum length of L = 1024 tokens. We compare against both autoregressive and diffusion-based baselines, including an autoregressive GPT-style language model, standard MDLMs, and MDLMs equipped with forward–backward (FB) and discrete flow matching (DFM) correctors. All checkpoints are reused from prior work to ensure comparability. In inference, we generate 5,000 sequences using planner-based decoding with P2 sampling (Peng et al., 2025a). We evaluate generation quality and diversity primarily with MAUVE (Pillutla et al., 2021), which measures the divergence between generated and reference distributions. As secondary metrics, we also report generative perplexity (Gen PPL) and entropy.

**Table 2.** Unconditional text generation. For each sampling step T, we report MAUVE (higher is better), generative perplexity (Gen PPL; lower is better), and entropy (higher is better). † indicates nucleus sampling. For each T, the best diffusion scores are bolded.

T = 32 T = 64 T = 128

## Method

MAUVE PPL Ent. MAUVE PPL Ent. MAUVE PPL Ent.

Data (ref.) 1.00 14.8 5.44 1.00 14.8 5.44 1.00 14.8 5.44 AR† 0.760 1.21 5.22 0.760 1.21 5.22 0.760 1.21 5.22

MDLM† 0.006 100.45 5.60 0.011 72.08 5.55 0.015 61.5 5.52 MDLM+FB† 0.007 95.76 5.56 0.016 59.05 5.49 0.064 42.8 5.44 MDLM+DFM† 0.004 303.8 5.31 0.007 108.8 5.33 0.041 37.9 5.31 ReMDM† 0.007 93.53 5.58 0.016 60.38 5.51 0.057 42.5 5.43 PAPL† (ours) 0.013 40.19 5.32 0.046 29.98 5.24 0.067 24.33 5.16

Results. Table 2 reports unconditional text generation performance across sampling steps T ∈{32, 64, 128}. Our method, PAPL, consistently and substantially improves diffusion-based generation. At T = 128, PAPL attains the strongest diffusion MAUVE (0.067) and lowest Gen PPL (24.3), outperforming ReMDM (0.057 MAUVE, 42.5 PPL) and MDLM+DFM (0.041 MAUVE, 37.9 PPL). entropy remains comparable across all methods (5.1–5.6), indicating that PAPL’s gains in quality and perplexity are not driven by mode collapse.

Takeaways. PAPL delivers consistent and significant improvements over prior discrete diffusion models across all sampling budgets. These gains hold under fast sampling regimes (T < L). While diffusion approaches still trail autoregressive models in absolute quality, PAPL markedly reduces this gap without sacrificing diversity.

## 4.3 CODE GENERATION

**Table 3.** Code infilling performance on HUMANEVAL-

INFILL PASS@1 and SANTACODER-FIM EXACT MATCH. Large-scale models (≥7B) are shown as reference, while the main comparison is among compact sub-billion models.

## Model

HumanEval SantaCoder

Reference Models (≥7B) LLaDA-8B 48.3 35.1 Dream-7B 39.4 40.7 DiffuCoder-7B 54.8 38.8 Dream-Coder-7B 55.3 40.0

Compact Models (≤1B) DLM (0.5B) 30.0 30.7 DLM (0.5B) + PAPL (Ours) 32.5 32.3 DLM (0.5B) + PAPL (Oracle length) 77.4 56.4

Setup. We evaluate PAPL on code generation, a domain requiring both syntactic validity and semantic correctness. Following the Open-dLLM framework (Peng et al., 2025b), we initialize from Qwen2.5-Coder and adapt it to the diffusion setting with bidirectional attention. Models are trained on the FineCode corpus, which combines algorithmic and QA-style data, and are optimized with a masked cross-entropy loss as in the Open-dLLM recipe. Evaluation covers HU- MANEVAL (Chen et al., 2021), MBPP (Austin et al., 2021b), and their augmented variants, as well as HUMANEVAL-INFILL and the Python subset of SANTACODER-FIM. We report pass@1 and pass@10 for completion tasks, and exact match for infilling, using official protocols. See Section B.3.1 for more details.

<!-- Page 9 -->

**Table 4.** Code generation performance on HUMANEVAL, HUMANEVAL+, MBPP, and MBPP+. Large-scale models (≥7B) are shown as reference, while the main comparison is among compact sub-billion models. Results marked with † are adopted from prior work (Havasi et al., 2025).

HUMANEVAL HUMANEVAL+ MBPP MBPP+

## Model

Pass@1 Pass@10 Pass@1 Pass@10 Pass@1 Pass@10 Pass@1 Pass@10

Reference Models (≥7B) LLaDA (8B) 35.4 50.0 30.5 43.3 38.8 53.4 52.6 69.1 Dream (7B) 56.7 59.2 50.0 53.7 55.4 56.2 71.5 72.5

Compact Models (≤1B) Autoregressive† (1.3B) 17.0 34.7 14.0 28.6 25.6 45.4 – – Mask DFM (1.3B)† 9.1 17.6 7.9 13.4 6.2 25.0 – – Edit Flow (1.3B)† 12.8 24.3 10.4 20.7 10.0 36.4 – – Uniform X0 + Edit Flow (1.3B)† 9.7 24.3 9.7 19.5 9.4 33.4 – – DLM (0.5B) 18.5 31.1 17.5 28.0 17.6 32.6 17.6 32.6 DLM (0.5B) + PAPL (Ours) 20.8 38.4 17.6 35.2 16.7 38.4 23.9 53.6

Results. Table 4 shows that PAPL consistently outperforms the baseline diffusion model across all completion benchmarks. On HUMANEVAL, pass@1 improves from 18.5 to 20.8 and pass@10 from 31.1 to 38.4. Similar gains are observed on HUMANEVAL+ and MBPP+, where PAPL improves pass@10 by more than +10 points. This disproportionate improvement at pass@10 suggests that PAPL is not just improving the single best prediction, but is learning a more robust generative distribution over the entire solution space, making it highly effective at generating a diverse set of high-quality candidates. Table 3 reports results on infilling. Here too, PAPL improves over the baseline: pass@1 increases from 30.0 to 32.5 on HUMANEVAL-INFILL, and exact-match accuracy rises from 30.7 to 32.3 on SANTACODER-FIM. These improvements hold under identical configurations and inference settings, confirming that planner-aware training better aligns the denoiser with the planner-based reverse process.

Takeaway. Across both completion and infilling tasks, PAPL consistently improves the correctness of code generation. These results highlight the generality of our approach: learning better generative paths benefits tasks requiring strict logical structure just as it does those requiring biological fidelity.

**Figure 3.** PAPL consistently improves over DLM across training, sampling steps, and temperature. (a) Faster convergence in training steps. (b) Higher performance across sampling steps. (c) More robust to temperature when training from scratch. (d) More robust to temperature when fine-tuning.

## 4.4 ABLATION

Head-to-head comparison. We compare PAPL with the vanilla DLM baseline across training and inference conditions. Figure 3 shows that PAPL converges faster during training (panel a), maintains stronger performance across different sampling steps (panel b), and is substantially more robust to temperature variation, both when trained from scratch and when fine-tuned (panels c–d). These results confirm that PAPL improves final quality while also stabilizing optimization and inference dynamics.

Hyperparameter tuning. We study the two key components introduced by PAPL: the softmax temperature τ and the path learning weight α. As shown in Fig. 4, lowering τ below the default (τ = 1) consistently improves foldability, while larger values hurt performance, suggesting that sharper planner distributions provide more effective supervision. Increasing α strengthens performance up to α = 5, demonstrating that emphasizing planner-weighted paths enhances stability and final quality. Increasing α beyond 5 on this task lowers performance indicating the usefulness of interpolating

![Figure extracted from page 9](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-009-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 10 -->

between MDLM and PAPL losses. Runs for these weights were stopped early to save compute and so do not appear in Fig. 4.

## 5 RELATED WORK

**Figure 4.** Effect of τ and α on foldability. Lower τ (< 1) improves performance. Increasing α steadily boosts foldability up to α = 5. The dashed line denotes the vanilla DLM baseline.

Masked diffusion language models (DLMs) have recently emerged as promising alternatives to autoregressive models for discrete sequence generation (Sahoo et al., 2024; Shi et al., 2024; Nie et al., 2025a; Gong et al., 2025). A large body of work has focused on improving sampling efficiency and quality through heuristic strategies such as greedy unmasking (Gong et al., 2025), iterative remasking (Zheng et al., 2023; Wang et al., 2024), informed correctors (Zhao et al., 2025), and planner-guided approaches like P2 (Peng et al., 2025a) and confidence-planning (). While effective, these methods assume models trained under a uniform denoising order and modify the sampling path only at inference time, creating a mismatch between training and generation.

A related line of work investigates generation order in the setting of any-order autoregressive models (AOARMs). Shih et al. (2022) propose restricting the model to a fixed family of orders to reduce redundancy, whereas LO-ARM (Wang et al., 2025c) and (Li et al., 2021) treat generation order as a latent variable and learn it with REINFORCE (Williams, 1992). However, the reliance on high-variance policy gradient estimators in LO-ARM limits its scalability to large models and datasets. DDPD (Liu et al., 2025) trains for a planner-selected denoising order, where the planner is effectively a uniform discrete diffusion model. This methodology requires a planner of similar or greater size to the denoiser, and hence suffers from a similar pitfall to its AOARM counterparts.

## 6 CONCLUSION

In this work, we investigate the role of planning at inference time with respect to denoiser training for DLMs. Through this, we identify a mismatch in popular planner-guided inference paths and standard denoiser training that uses uniformly at random masking. We propose a new Planner-Aware Evidence Lower Bound (P-ELBO) and developed a practical algorithm, Planner-Aware Path Learning (PAPL), to align the denoiser training with its intended use at inference. We demonstrate that the P-ELBO recovers all current planning strategies, and in particular enjoys straightforward implementation with PAPL being a single line code change with no additional computational overhead from standard DLM training. Empirically, PAPL achieves a 40% relative increase in protein foldability, a 4× MAUVE gain in text generation, and a 23% relative improvement in code generation on HumanEval. demonstrating the benefits of reconciling the training and sampling processes. While PAPL uses the denoiser’s own confidence to plan, there are many other possible planning functions presenting ripe directions to extend and generalize the PAPL algorithm. We discuss how other unmasking schemes such as “top probability margin Kim et al. (2025), RDM Zheng et al. (2023), Top-k “block-denoising” Nie et al. (2025b), and “Confidence Thresholding” Wu et al. (2025) can fit into a properly adapted version of our mathematical framework in §A.2 and §A.5. Expanding this analysis to find a computationally viable loss analogous to what the PAPL loss of equation 7 provides for greedy ancestral is an interesting avenue for future work. Finally, we remark that our papers strength is also its limitation: while we show that one should modify the ELBO in order to account for alternative decoding strategies in MDMs, this means that some amount of post-training is necessary in order to test whether the decoding strategies performance can be improved via using a planner-aware loss. This training overhead makes our methodology expensive to implement with large planning models compared to just testing performance at inference time.

![Figure extracted from page 10](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-010-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 11 -->

## ACKNOWLEDGMENTS

Fred extends sincere gratitude to Kaiwen Zheng for his invaluable insights. Zack extends his gratitude to Jim Nolen for his support and insightful discussions. The authors acknowledge funding from UNIQUE, CIFAR, NSERC, Intel, Samsung, as well as the Hartwell Foundation and CHDI Foundation. The research was enabled in part by computational resources provided by the Digital Research Alliance of Canada (https://alliancecan.ca), Mila (https://mila.quebec), and NVIDIA. This research is partially supported by the EPSRC Turing AI World-Leading Research Fellowship No. EP/X040062/1 and EPSRC AI Hub No. EP/Y028872/1. Z.B. is partially supported by NSF-DMS award 2038056. F.Z.P. and A.R.Z. are partially supported by NIH R01HL169347.

ETHICS STATEMENT

This work introduces Planner Aware Path Learning (PAPL), a training framework for discrete diffusion models. Our experiments are limited to publicly available datasets in code and biological sequence generation. All results are computational; no biological synthesis or wet-lab experiments were performed. While improved generative models may be misused (e.g., generating harmful biological sequences or insecure code), we explicitly discourage such applications and release models only with documentation of intended use and limitations.

REPRODUCIBILITY STATEMENT

We provide detailed descriptions of model architectures, training objectives, datasets, and evaluation protocols in the main text and appendix. Hyperparameters, training schedules, and implementation details are included to enable replication. Code and pretrained models will be released upon publication to support full reproducibility.

<!-- Page 12 -->

## REFERENCES

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman,

Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023. 1

Sarah Alamdari, Nitya Thakkar, Rianne van den Berg, Alex X. Lu, Nicolo Fusi, Ava P. Amini, and

Kevin Kaichuang Yang. Protein generation with evolutionary diffusion: sequence is all you need. In NeurIPS 2023 Generative AI and Biology (GenBio) Workshop, 2023. 4.1, B.1

Jacob Austin, Daniel D Johnson, Jonathan Ho, Daniel Tarlow, and Rianne Van Den Berg. Structured denoising diffusion models in discrete state-spaces. Advances in neural information processing systems, 34:17981–17993, 2021a. 1

Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan,

Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. Program synthesis with large language models. arXiv preprint arXiv:2108.07732, 2021b. 4.3, B.3.1

Mohammad Bavarian, Heewoo Jun, Nikolas Tezak, John Schulman, Christine McLeavey, Jerry

Tworek, and Mark Chen. Efficient training of language models to fill in the middle. arXiv preprint arXiv:2207.14255, 2022. B.3.1

Victor Besnier, Mickael Chen, David Hurych, Eduardo Valle, and Matthieu Cord. Halton scheduler for masked generative image transformer. In The Thirteenth International Conference on Learning Representations, 2025. 3.2

Amarjit Budhiraja and Paul Dupuis. Analysis and Approximation of Rare Events: Representations and Weak Convergence Methods, volume 94 of Probability Theory and Stochastic Modelling. Springer US, New York, NY, 2019. A.3.3

Andrew Campbell, Joe Benton, Valentin De Bortoli, Thomas Rainforth, George Deligiannidis, and

Arnaud Doucet. A continuous time framework for discrete denoising models. In Advances in Neural Information Processing Systems, volume 35, pp. 28266–28279. Curran Associates, Inc., 2022. 3, A.3

Andrew Campbell, Jason Yim, Regina Barzilay, Tom Rainforth, and Tommi Jaakkola. Generative flows on discrete state-spaces: enabling multimodal flows with applications to protein co-design. In Proceedings of the 41st International Conference on Machine Learning, ICML’24, 2024. 3, A.3, B.2.1

Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and William T. Freeman. Maskgit: Masked generative image transformer. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 11315–11325, 2022. 1, 2.1, 3.2, B.2.2

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared

Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374, 2021. 4.3, B.3.1

Daniel T Gillespie. A general method for numerically simulating the stochastic time evolution of coupled chemical reactions. Journal of Computational Physics, 22(4):403–434, 1976. ISSN 0021-9991. 2.1

Daniel T. Gillespie. Exact stochastic simulation of coupled chemical reactions. The Journal of

Physical Chemistry, 81(25):2340–2361, 1977. ISSN 0022-3654. 2.1

Aaron Gokaslan and Vanya Cohen. Openwebtext corpus. http://Skylion007.github.io/

OpenWebTextCorpus, 2019. 4.2

Shansan Gong, Shivam Agarwal, Yizhe Zhang, Jiacheng Ye, Lin Zheng, Mukai Li, Chenxin An,

Peilin Zhao, Wei Bi, Jiawei Han, Hao Peng, and Lingpeng Kong. Scaling diffusion language models via adaptation from autoregressive models. In The Thirteenth International Conference on Learning Representations, 2025. 2.1, 3.2, 5

<!-- Page 13 -->

Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu

Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025. 1

Marton Havasi, Brian Karrer, Itai Gat, and Ricky TQ Chen. Edit flows: Flow matching with edit operations. arXiv preprint arXiv:2506.09018, 2025. 4

Thomas Hayes, Roshan Rao, Halil Akin, Nicholas J Sofroniew, Deniz Oktay, Zeming Lin, Robert

Verkuil, Vincent Q Tran, Jonathan Deaton, Marius Wiggert, et al. Simulating 500 million years of evolution with a language model. Science, 387(6736):850–858, 2025. 4.1, B.1

Emiel Hoogeboom, Alexey A. Gritsenko, Jasmijn Bastings, Ben Poole, Rianne van den Berg, and

Tim Salimans. Autoregressive diffusion models. In 10th International Conference on Learning Representations, 2022. 2.1

Jean Jacod and Albert Shiryaev. Limit theorems for stochastic processes, volume 288. Springer

Science & Business Media, 2013. A.3.3

Jaeyeon Kim, Kulin Shah, Vasilis Kontonis, Sham M. Kakade, and Sitan Chen. Train for the worst, plan for the best: Understanding token ordering in masked diffusions. In Forty-second International Conference on Machine Learning, 2025. 1, 6, A.2, B.2.2

Xuanlin Li, Brandon Trabucco, Dong Huk Park, Michael Luo, Sheng Shen, Trevor Darrell, and

Yang Gao. Discovering non-monotonic autoregressive orderings with variational inference. In International Conference on Learning Representations, 2021. 3.2, 5

Zeming Lin, Halil Akin, Roshan Rao, Brian Hie, Zhongkai Zhu, Wenting Lu, Nikita Smetanin,

Robert Verkuil, Ori Kabeli, Yaniv Shmueli, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science, 379(6637):1123–1130, 2023. 4.1, B.1

Sulin Liu, Juno Nam, Andrew Campbell, Hannes Stark, Yilun Xu, Tommi Jaakkola, and Rafael

Gomez-Bombarelli. Think while you generate: Discrete diffusion with planned denoising. In The Thirteenth International Conference on Learning Representations, 2025. 5

Aaron Lou, Chenlin Meng, and Stefano Ermon. Discrete diffusion modeling by estimating the ratios of the data distribution. In Proceedings of the 41st International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research, pp. 32819–32848. PMLR, 21–27 Jul 2024. 1, 3, A.3, A.3.2

Shen Nie, Fengqi Zhu, Chao Du, Tianyu Pang, Qian Liu, Guangtao Zeng, Min Lin, and Chongxuan

Li. Scaling up masked diffusion models on text. In The Thirteenth International Conference on Learning Representations, 2025a. 1, 3.1, 3.2, 5

Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu, JUN ZHOU, Yankai Lin,

Ji-Rong Wen, and Chongxuan Li. Large language diffusion models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025b. 6, A.2, A.5

Erik Nijkamp, Jeffrey A Ruffolo, Eli N Weinstein, Nikhil Naik, and Ali Madani. Progen2: exploring the boundaries of protein language models. Cell systems, 14(11):968–978, 2023. 4.1, B.1

Jingyang Ou, Shen Nie, Kaiwen Xue, Fengqi Zhu, Jiacheng Sun, Zhenguo Li, and Chongxuan Li.

Your absorbing discrete diffusion secretly models the conditional distributions of clean data. In The Thirteenth International Conference on Learning Representations, 2025. 2.1, 3.2

Fred Zhangzhi Peng, Zachary Bezemek, Sawan Patel, Jarrid Rector-Brooks, Sherwood Yao,

Avishek Joey Bose, Alexander Tong, and Pranam Chatterjee. Path planning for masked diffusion model sampling. arXiv preprint arXiv:2502.03540, 2025a. 1, 2.1, 4.2, 5, A.2, A.4, A.4.2, B.2.1, B.2.2

Fred Zhangzhi Peng, Shuibai Zhang, Alex Tong, and contributors. Open-dllm: Open diffusion large language models. https://github.com/pengzhangzhi/Open-dLLM, 2025b. 4.3, B.3.1

<!-- Page 14 -->

Krishna Pillutla, Swabha Swayamdipta, Rowan Zellers, John Thickstun, Sean Welleck, Yejin Choi, and Zaid Harchaoui. Mauve: measuring the gap between neural text and human text using divergence frontiers. In Proceedings of the 35th International Conference on Neural Information Processing Systems, NIPS ’21, Red Hook, NY, USA, 2021. Curran Associates Inc. ISBN 9781713845393. 4.2, B.2.1

Yinuo Ren, Haoxuan Chen, Grant M. Rotskoff, and Lexing Ying. How discrete and continuous diffusion meet: Comprehensive analysis of discrete diffusion models via a stochastic integral framework. In The Thirteenth International Conference on Learning Representations, 2025. A.3.1, A.3.3, A.3.3

Hitesh Sagtani, Rishabh Mehrotra, and Beyang Liu. Improving fim code completions via context & curriculum based learning. In Proceedings of the Eighteenth ACM International Conference on Web Search and Data Mining, WSDM ’25, pp. 801–810, New York, NY, USA, 2025. Association for Computing Machinery. ISBN 9798400713293. B.3.1

Subham Sekhar Sahoo, Marianne Arriola, Aaron Gokaslan, Edgar Mariano Marroquin, Alexander M

Rush, Yair Schiff, Justin T Chiu, and Volodymyr Kuleshov. Simple and effective masked diffusion language models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. 1, 2.1, 5, A.3.2, B.2.1, B.2.1

Yair Schiff, Subham Sekhar Sahoo, Hao Phung, Guanghan Wang, Sam Boshar, Hugo Dalla-torre,

Bernardo P de Almeida, Alexander M Rush, Thomas PIERROT, and Volodymyr Kuleshov. Simple guidance mechanisms for discrete diffusion models. In The Thirteenth International Conference on Learning Representations, 2025. 1

Jiaxin Shi, Kehang Han, Zhe Wang, Arnaud Doucet, and Michalis Titsias. Simplified and generalized masked diffusion for discrete data. Advances in neural information processing systems, 37: 103131–103167, 2024. 1, 2.1, 5, A.3.2

Andy Shih, Dorsa Sadigh, and Stefano Ermon. Training and inference on any-order autoregressive models the right way. Advances in Neural Information Processing Systems, 35:2762–2775, 2022. 3.2, 5

Yuxuan Song, Zheng Zhang, Cheng Luo, Pengyang Gao, Fan Xia, Hao Luo, Zheng Li, Yuehang

Yang, Hongli Yu, Xingwei Qu, et al. Seed diffusion: A large-scale diffusion language model with high-speed inference. arXiv preprint arXiv:2508.02193, 2025. 1

Haoran Sun, Lijun Yu, Bo Dai, Dale Schuurmans, and Hanjun Dai. Score-based continuous-time discrete diffusion models. In The Eleventh International Conference on Learning Representations, 2023. 3, A.3, A.3.2

Benigno Uria, Iain Murray, and Hugo Larochelle. A deep and tractable density estimator. In

Proceedings of the 31th International Conference on Machine Learning, 2014. 2.1

Guanghan Wang, Yair Schiff, Subham Sekhar Sahoo, and Volodymyr Kuleshov. Remasking discrete diffusion models with inference-time scaling. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025a. A.2, B.2.1

Xinyou Wang, Zaixiang Zheng, Fei Ye, Dongyu Xue, Shujian Huang, and Quanquan Gu. Diffusion language models are versatile protein learners. In Proceedings of the 41st International Conference on Machine Learning, ICML’24, 2024. 1, 4.1, 5, B.1

Xinyou Wang, Zaixiang Zheng, Fei YE, Dongyu Xue, Shujian Huang, and Quanquan Gu. DPLM-2:

A multimodal diffusion protein language model. In The Thirteenth International Conference on Learning Representations, 2025b. 1

Zhe Wang, Jiaxin Shi, Nicolas Heess, Arthur Gretton, and Michalis Titsias. Learning-order autore- gressive models with application to molecular graph generation. In Forty-second International Conference on Machine Learning, 2025c. 5

Ronald J Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine learning, 8(3):229–256, 1992. 5

<!-- Page 15 -->

Chengyue Wu, Hao Zhang, Shuchen Xue, Zhijian Liu, Shizhe Diao, Ligeng Zhu, Ping Luo, Song

Han, and Enze Xie. Fast-dllm: Training-free acceleration of diffusion llm by enabling kv cache and parallel decoding. arXiv preprint arXiv:2505.22618, 2025. 6, A.2, A.5

G. George Yin and Qing Zhang. Continuous-Time Markov Chains and Applications, volume 37 of

Stochastic Modelling and Applied Probability. Springer, New York, NY, 2013. A.3.1

Yang Zhang and Jeffrey Skolnick. Scoring function for automated assessment of protein structure template quality. Proteins: Structure, Function, and Bioinformatics, 57(4):702–710, 2004. doi: https://doi.org/10.1002/prot.20264. B.1

Yixiu Zhao, Jiaxin Shi, Feng Chen, Shaul Druckmann, Lester Mackey, and Scott Linderman. Informed correctors for discrete diffusion models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. 5

Kaiwen Zheng, Yongxin Chen, Hanzi Mao, Ming-Yu Liu, Jun Zhu, and Qinsheng Zhang. Masked diffusion models are secretly time-agnostic masked models and exploit inaccurate categorical sampling. In The Thirteenth International Conference on Learning Representations, 2025. 2.1

Lin Zheng, Jianbo Yuan, Lei Yu, and Lingpeng Kong. A reparameterized discrete diffusion model for text generation. arXiv preprint arXiv:2302.05737, 2023. 2.1, 5, 6, A.2, A.5

<!-- Page 16 -->

APPENDICES

A Theoretical Derivations and Proofs 17

A.1 Foundational Derivations............................... 17

A.2 Instantiations..................................... 25

A.3 Alternative Proof of Proposition 3.2: Continuous Time Markov Chains Perspective 29

A.4 Generalization to Planners with Remasking (P2-style)................ 34

A.5 Other Sampling Methods with Multiple Denoising Positions and/or remasking... 38

B Experimental Details 38

B.1 Protein Sequence Generation............................. 38

B.2 Text Generation.................................... 40

B.3 Code Generation................................... 41

C Additional Results 42

C.1 Unstable Training with Pure PAPL Loss....................... 42

C.2 Comparison of Training Curves with Vanilla MDM Loss.............. 43

C.3 Empirical Estimation of the Effect of the Approximation Steps........... 43

C.4 HumanEval Performance Analysis.......................... 44

D Practitioner’s Guide 46

<!-- Page 17 -->

A THEORETICAL DERIVATIONS AND PROOFS

A.1 FOUNDATIONAL DERIVATIONS

A.1.1 PROPERTIES OF KL DIVERGENCE

Recall for p, q ∈∆|X| for X some finite set, we define

DKL(p||q):=

X x∈X p(x) log p(x)

q(x)

when p(x) = 0 for every x ∈X such that q(x) = 0 and +∞otherwise. Also recall that for x such that p(x) = 0, we interpret 0 log(0) = 0. Here we will recall some basic properties of DKL that will aid in our proof.

Lemma A.1. Non-negativity of KL-Divergence: For any p, q distributions on a finite set X,

DKL(p||q) ≥0, with DKL(p||q) = 0 if and only if p = q.

Proof. First we observe that that g: [0, ∞) →R given by g(t) = t log(t) −t + 1 has g′(t) = log(t), g′(t) < 0 for t ∈(0, 1) and g′(t) > 0 for t > 1, so g has a global minimum of 0 at t = 1. Then:

DKL(p||q) =

X x∈X p(x) log p(x)

q(x)

=

X x∈X q(x)p(x)

q(x) log p(x)

q(x)

+ 1 −1

=

X x∈X q(x)p(x)

q(x) log p(x)

q(x)

+

X x∈X q(x) −

X x∈X p(x)

=

X x∈X q(x)

p(x)

q(x) log p(x)

q(x)

−p(x)

q(x) + 1

=

X x∈X q(x)g p(x)

q(x)

≥

X x∈X q(x) ∗0, with equality holding if and only if q(x) = p(x), ∀x ∈X.

Lemma A.2. Chain Rule for KL Divergence between Joint Law of 2 Discrete Random Variables:

For p, q distributions on X × Y, where X and Y are finite sets, denoting by pX, qX the X marginals of p and q respectively and by pY|X (y|x) = p(x,y)

pX (x) and similarly for qY|X (y|x):

DKL(p||q) = DKL(pX ||qX) + Ex∼pX

DKL(pY|X (·|x)||qY|X (·|x))

.

Proof. By definition:

DKL(p||q) =

X

(x,y)∈X×Y p(x, y) log p(x, y)

q(x, y)

=

X

(x,y)∈X×Y p(x, y) log pY|X (y|x)pX (x)

qY|X (y|x)qX (x)

=

X

(x,y)∈X×Y p(x, y) log pX (x)

qX (x)

+

X

(x,y)∈X×Y p(x, y) log pY|X (y|x)

qY|X (y|x)

<!-- Page 18 -->

=

X x∈X pX (x) log pX (x)

qX (x)

+

X x∈X pX (x)

X y∈Y pY|X (y|x) log pY|X (y|x)

qY|X (y|x)

= DKL(pX ||qX) +

X x∈X pX (x)DKL(pY|X (·|x)||qY|X (·|x))

= DKL(pX ||qX) + Ex∼pX

DKL(pY|X (·|x)||qY|X (·|x))

.

Corollary A.3. Chain Rule for KL Divergence between Joint Law of N Discrete Random Variables:

For N ∈N and p, q distributions on X0 × X1 ×... XN where X0,..., XN are finite sets, denot- ing for k ∈{0, 1,..., N} p0:k the X0 × · · · × Xk marginal of p and similarly for q0:k, and by pk+1|0:k(xk+1|x0,..., xk) = pk+1(x0,...,xk,xk+1)

pk(x0,...,xk) for xi ∈Xi, i = 0, 1,..., k and similarly for qk+1|0:k, we have:

DKL(p||q) = DKL(p0||q0)

+

N−1 X k=0

E(x0,x1,...,xk)∼p0:k

DKL(pk+1|0:k(·|x0,..., xk)||qk+1|0:k(·|x0,..., xk))

Proof. This follows from iteratively applying Lemma A.2.

Corollary A.4. Inequality for Marginalization of Discrete Distributions:

For p, q distributions on X × Y, where X and Y are finite sets, denoting by pX, qX the X marginals of p and q respectively:

DKL(p||q) ≥DKL(pX ||qX)

Proof. This follows from Lemma A.2 via noting that the term inside the expectation is non-negative for each y via Lemma A.1.

A.1.2 DISCRETE TIME MARKOV CHAINS

Definition A.5. Discrete Time Markov Chains: A discrete time Markov chain on finite state space S is a sequence of random variables {Xk}k∈N such that for any k ∈N and x0, x1, · · ·, xk−2, y, x ∈S:

P(Xk = x|Xk−1 = y, Xk−2 = xk−2,..., X1 = x1, X0 = x0) = P(Xk = x|Xk−1 = y). (8)

The distribution of a path of length k (X0, X1,..., Xk) ∈Sk+1 of a Markov chain {Xk}k∈N at any time is entirely determined by its one step transition probabilities, which we encode into its transition matrix:

Qk(x, y) = P(Xk+1 = x|Xk = y), x, y ∈V, k ∈N. (9)

In the case where P(Xk = x|Xk−1 = y) = P(X1 = x|X0 = y) for all k ∈N, i.e. when the transition matrix does not depend on the time k, we say the chain is time-homogeneous.

Proposition A.6. KL Divergence Between Paths of Discrete Time Markov Chains:

Let R, P be probability distributions on SN+1 corresponding to the distribution of paths of length N of two discrete time Markov chains Y and X on S with transition matrices R and Q respectively. Also suppose that Y0 ∼µ and X0 ∼ν for some µ, ν ∈∆|S|. Then:

DKL(R||P) = DKL(µ||ν) +

N−1 X k=0

Exk∼rk



X y∈S

Rk(y, xk) log

Rk(y, xk)

Qk(y, xk)



, where rk ∈∆|S| is given by:

rk(x) = P(Yk = x).

<!-- Page 19 -->

Proof. By Corollary A.3 (using the same notation as in the statement thereof):

DKL(R||P) = DKL(R0||P0)

+

N−1 X k=0

E(x0,x1,...,xk)∼R0:k

DKL(Rk+1|0:k(·|x0, x1,..., xk)||Pk+1|0:k(·|x0, x1,..., xk))

= DKL(µ||ν)

+

N−1 X k=0

E(x0,x1,...,xk)∼R0:k [DKL(P(Yk+1 = ·|Yk = xk)||P(Xk+1 = ·|Xk = xk))]

by definition of µ, ν and the Markov property equation 8

= DKL(µ||ν) +

N−1 X k=0

Exk∼rk [DKL(P(Yk+1 = ·|Yk = xk)||P(Xk+1 = ·|Xk = xk))]

by definition of rk and R0:k

= DKL(µ||ν) +

N−1 X k=0

Exk∼rk



X y∈S

Rk(y, xk) log

Rk(y, xk)

Qk(y, xk)



 by definition of the transition matrix equation 18.

A.1.3 APPLICATION TO THE ELBO

The loss corresponding to an ELBO Eθ(x0) (i.e. a quantity satisfying log pθ(x0) ≥Eθ(x0), ∀x0 ∈ VL and pθ the generated data distribution) is always given by

L(θ) = −Ex0∼pdata

Eθ(x0)

, so that

DKL(pdata||pθ) =

X x∈SL pdata(x) log pdata(x)

pθ(x)

=

X x∈SL pdata(x) log pdata(x) −

X x∈SL pdata(x) log(pθ(x))

= −H(pdata) −Ex0∼pdata [log(pθ(x0))]

≤−H(pdata) −Ex0∼pdata

Eθ(x0)

= −H(pdata) + L(θ).

Here H(p) denotes the Shannon entropy of p. Note that, crucially, pθ must be the distribution on VL which one samples from at inference time, since this is what one wishes to make equal to pdata via minimizing L(θ) to H(pdata).

In the following proposition, we show Proposition A.6 and the basic properties of KL divergence from Subsection A.1.1 can be used to derive an ELBO, and hence training loss, for any sampling procedure which can be described via a discrete time Markov chain.

Proposition A.7. Application to ELBO:

Suppose p is a distribution on S the given by p(x) = P(XN = x) for some N ∈N and X a Markov chain on S with transition matrix Q. Then for x0 ∈S and Y x0 any Markov chain with rate matrix R(·, ·; x0) satisfying both

## 1. Y x0 0 is equal in distribution to X0

2. P(Y x0 N = x0) = 1,

<!-- Page 20 -->

we have:

log(p(x0)) ≥−

N−1 X k=0

Exk∼rk(·;x0)



X y∈S

Rk(y, xk; x0) log

Rk(y, xk; x0)

Qk(y, xk)



, where rk(·; x0) ∈∆|S| is given by:

rk(x; x0) = P(Y x0 k = x).

Proof. First we observe that:

log(p(x0)) = −DKL(δ(x0)||p) = −DKL(P(Y x0

N = ·)||P(XN = ·))

by definition. Then, applying Corollary A.4 to R(·; x0), P the distributions on SN+1 corresponding to paths of length N of Y x0 and X respectively, using X = S and Y = SN:

−DKL(P(Y x0

N = ·)||P(XN = ·)) ≥−DKL(R(·; x0)||P).

Finally, by Proposition A.6:

−DKL(R(·; x0)||P) = −DKL(P(Y x0

0 = ·)||P(X0 = ·))

−

N−1 X k=0

Exk∼rk(·;x0)



X y∈S

Rk(y, xk; x0) log

Rk(y, xk; x0)

Qk(y, xk)





= −

N−1 X k=0

Exk∼rk(·;x0)



X y∈S

Rk(y, xk; x0) log

Rk(y, xk; x0)

Qk(y, xk)



, where in the last step we used Lemma A.1 and that P(Y x0

0 = ·) = P(X0 = ·) by assumption.

A.1.4 PROOF OF PROPOSITION 3.2: A SIMPLE, DISCRETE TIME PERSPECTIVE

Here we provide a novel, self-contained proof of Proposition 3.2. In particular, this encapsulates the proof of the standard DLM ELBO equation 3 by setting Cat (i; Gϕ(z, x)) = 1 NM(x) for all z and i such that xi = m. This proof methodology helps elucidate the freedom of choice of reference dynamics, and does not require any of the prerequisite knowledge on continuous time Markov chains as other existing proofs in the discrete diffusion literature.

Proposition 3.2. For any planner Gϕ, let pGϕ θ denote the distribution of xL obtained via the plannerguided sampling scheme. Then we have the following ELBO:

log(p

Gϕ θ (x0)) ≥Eθ,ϕ(x0) = Eθ,ϕ

1 (x0) + Eθ,ϕ

2 (x0),

Eθ,ϕ

1 (x0) = L E k∼Unif([0:L−1])



 E xk∼r

Gϕ k (·;x0)

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))





Eθ,ϕ

2 (x0) = −L E k∼Unif([0:L−1])



 E xk∼r

Gϕ k (·;x0)

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(i; Gϕ(x0, xk))

Fθ,ϕ(xk, xi

0, i)



, where rGϕ k is the distribution at time k of a Markov chain with initial data (m,..., m) and transition rates as in equation 2 but with 1/NM(x) replaced by Gi ϕ(x0, x).

Proof. By equation 4, for x ∈VL, pGϕ θ (x) = P(XGϕ,θ

L = x) where XGϕ,θ is the time homogeneous discrete time Markov chain on VL with transition matrix given for x, y ∈VL by:

Qθ,ϕ(y, x) =

Cat yi; Di θ(x)

Fθ,ϕ(x, yi, i), dHAM(x, y) = 1, xi̸ = yi, xi = m 0, otherwise and P(XGϕ,θ

0 = x) = Cat(x; δ((m,..., m))).

<!-- Page 21 -->

So to obtain an ELBO for pGϕ θ using Proposition A.7, we select any family of transition matrices R(·, ·; x0) parameterized by x0 ∈VL determining a family Markov chains Y x0 such that

P(Y x0

L = x0|Y x0

0 = (m,..., m)) = 1. (10)

There are infinitely many such choices for the reference dynamics Y x0, but in order to make the paths of the reference dynamics apriori as close to those of XGϕ,θ as possible, we opt to keep the planner Gϕ in the transition probabilities and simply replace Dθ(x) by δ(x0) in the rate matrix Qθ,ϕ. Recalling the definition of Fθ,ϕ from equation 5, this yields R(·, ·; x0) to be the time homogeneous rate matrix RGϕ(·, ·; x0) given by, for x, y ∈VL:

RGϕ(y, x; x0) =

Cat(i; Gϕ(x0, x))Cat(yi; δ(xi

0)), dHAM(x, y) = 1, xi̸ = yi, xi = m 0, otherwise.

Observe that this is the same transition matrix from equation 2 but with 1/NM(x) replaced by Gi ϕ(x0, x). Also observe that indeed equation 10 is satisfied, since at each step we simply choose a coordinate i among masked positions of Y x0 with probability Cat(i; Gϕ(x0, x)) and flip it from m to xi

0.

Then, inserting these choices into Proposition A.7 and using log

Cat(i; Gϕ(x0, x)) Cat yi; Di θ(x)

Fθ,ϕ(x, yi, i)

!

= −log

Cat yi; Di θ(x)

−log

Fθ,ϕ(x, yi, i) Cat(i; Gϕ(x0, x))

the proof of Proposition 3.2 is complete.

A.1.5 ORM OF THE OPTIMAL PLANNER FOR A FIXED DENOISER: PROOF OF PROPOSITION A.8

Recall that the loss associated to the ELBO from Proposition A.7 is:

L(θ, ϕ) = −Ex0∼pdata

Eθ,ϕ(x0)

. (11)

A natural question is: for a fixed (imperfect) denoiser, what is the optimal form of Gϕ which minimizes this objective? We will show here:

Proposition A.8. Consider the loss L(ϕ) = −Ex0∼pdata

Eθ,ϕ(x0)

where Eθ,ϕ(x0) is as in Proposition A.7 and Dθ is fixed. Then L(ϕ) is uniquely minimized over Gϕ when, for x0, xk ∈VL with x0 containing no masked tokens and xk equal to x0 in all unmasked positions:

Gi ϕ(x0, xk) ∝qi θ,ϕ(xi

0|xk), (12)

for qi θ,ϕ the transition probabilities of the data generating discrete time Markov chain’s dynamics from equation 4.

That is, our loss finds a planner which is mutually consistent with the denoiser in that it picks at each step a coordinate i to unmask with probability proportional to the probability of denoising coordinate i to xi

0 at the current generation step under the planned path. In short: the optimal planner tends to assign high mass to trajectories whose sequence of single-coordinate updates yields high likelihood of producing the observed x0, which during training is supervised by the data. Observe that equation 12 is a fixed-point equation relating values of Gi ϕ(x0, xk) to itself and the imperfect denoiser through Fθ,ϕ(xk, xi

0, i) of equation 5, so one can not simply choose to use this optimal planner and indeed needs to train towards optimality in practice.

Proof. To see this, we first observe that for fixed xk, no constraint need be enforced in the relationship between the distributions Gϕ(z, xk), Gϕ(¯z, ¯xk) ∈∆L when (¯z, ¯xk)̸ = (z, x) ∈V2L. This means that minimizing equation 11 is equivalent to minimizing the integrand:

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(i; Gϕ(x0, xk)) Cat(xi

0; Di θ(xk))Fθ,ϕ(xk, xi

0, i)

<!-- Page 22 -->

= DKL(Gϕ(x0, xk)||rθ,ϕ(x0, xk)) + log(Cθ,ϕ(x0, xk)) (13)

for fixed x0, xk, and k, where rθ,ϕ(x0, xk) ∈∆L is given by:

Cat(i; rθ,ϕ(x0, xk)) ∝Cat(xi

0; Di θ(xk))Fθ,ϕ(xk, xi

0, i) = qi θ,ϕ(xi

0|xk), and where Cθ,ϕ is its normalizing constant.

Next we observe that, although Cθ,ϕ appears to depend implicitly on Gθ,ϕ(x0, xk) through Fθ,ϕ(xk, xi

0, i) (recall equation 5) this does not affect the minimization problem. To see this, we observe that

Fθ,ϕ(xk, xi

0, i) =

L Y j̸=i

Cat(xj

0; Dj θ(xk))Cat(i; Gϕ(x0, xk))

+ Ez∼Dθ(x)

h

1z−i̸=x−i 0 Cat i; Gϕ(z−i,xi

0, xk) i where for x ∈VL, x−i ∈VL−1 is x but with its i’th component removed.

Then

Cθ,ϕ(x0, xk) =

L X i=1

Cat(xi

0; Di θ(xk))Fθ,ϕ(xk, xi

0, i)

=

L Y j=1

Cat(xj

0; Dj θ(xk))

L X i=1

Cat(i; Gϕ(x0, xk))

!

+

L X i=1

Cat(xi

0; Di θ(xk))Ez∼Dθ(x)

h

1z−i̸=x−i 0 Cat i; Gϕ(z−i,xi

0, xk) i

=

L Y j=1

Cat(xj

0; Dj θ(xk))

+

L X i=1

Cat(xi

0; Di θ(xk))Ez∼Dθ(x)

h

1z−i̸=x−i 0 Cat i; Gϕ(z−i,xi

0, xk) i

.

That is, Cθ,ϕ(x0, xk) only depends on Gϕ(z, xk) for z̸ = x0. Hence, minimizing equation 13 over Gϕ(x0, xk) is equivalent to minimizing the KL divergence between Gϕ(x0, xk) and rθ,ϕ(x0, xk). By Lemma A.1, this occurs precisely when equation 12 holds.

A.1.6 DERIVATION OF GENERAL PLANNED TRANSITION PROBABILITIES (EQ. 4)

Recall that the sampling methodology discussed in §3 is as per Alg. 2.

## Algorithm

## 2 Gillespie Sampler with a

Planner

1: Initialize: t ←0, x0 ←(m,..., m), planner Gϕ, denoiser Dθ 2: for k = 0: L −1 do 3: Plan Sample z ∼Dθ(xk) 4: Sample dimension i ∼Gϕ(z, xk) 5: Denoise 6: xk+1 ←xk 7: xi k+1 ←zi

8: end for 9: return xL 10:

Let pGϕ θ ∈∆dL denote the distribution on VL of a sample obtained via running Alg. 2, and let pGϕ θ,k+1(·|xk) ∈∆dL denote the distribution of xk+1 given xk. With abuse of notation, we will also let pGϕ θ,k+1(·, ·|xk) ∈∆dL2 denote the joint distribution of xk+1 and the k + 1’st sample z. Note that

<!-- Page 23 -->

xk+1 may only differ from xk in a single coordinate i such that xi k = m. So, letting for x ∈VL, i ∈[1: L], y ∈V, x−i,y ∈VL be equal to x0, x1,..., xi−1, y, xi+1,... xL

:

pGϕ θ,k+1(x−i,y k |xk) =

X z∈VL pGϕ θ,k+1(x−i,y k, z|xk)

=

X z∈VL:zi=y

L Y j=1

Cat zj; Dj θ(xk)

Cat (i; Gϕ(z, xk))

= Cat y; Di θ(xk)

X z∈VL

L Y j=1

Cat zj; Dj θ(xk)

Cat i; Gϕ(z−i,y, xk)

= Cat y; Di θ(xk)

Fθ,ϕ(xk, y, i)

where Fθ,ϕ is as in equation 5. pGϕ θ,k+1(x−i,y k |xk) is precisely what we denote as qi θ,ϕ(y; xk) in equation 4.

A.1.7 PROOF OF PROPOSITION 3.1 (GREEDY ANCESTRAL VIOLATES THE VANILLA ELBO)

Continuing with the notation from the previous subsection, letting pGϕ θ,Σ(x, σ) denote the probability of generating the sample x along the path σ ∈ΣL, we have:

pGϕ θ,Σ(x, σ) =

L Y k=1 pGϕ θ,k(xσ(<k+1)|xσ(<k))

=

L Y k=1

Cat xσ(k); Dσ(k)

θ (xσ(<k))

Fθ,ϕ(xσ(<k), xσ(k), σ(k)), where here we use the same notation as in equation 1. Thus, we arrive at:

pGϕ θ (x) =

X σ∈ΣL pGϕ θ,Σ(x, σ)

=

X σ∈ΣL

L Y k=1

Cat xσ(k); Dσ(k)

θ (xσ(<k))

Fθ,ϕ(xσ(<k), xσ(k), σ(k)). (14)

Using equation 14 and specializing Gϕ to the case of greedy ancestral sampling, we readily obtain a proof of Proposition 3.1.

Proposition 3.1. For pgreedy θ (x0) defined with Gϕ in equation 6 and Dθ an imperfect denoiser, we may have log(pgreedy θ (x0)) < Eθ,unif(x0), where Eθ,unif(x0) is as in equation 1.

Proof. Since we just need a counterexample to the ELBO property, we may restrict to the case of L = 2 and V = {1, 2, m}. To construct an example denoiser in this setting, we only need to define 6 terms:

c1 = Cat

1, D1 θ(m, m)

, c2 =Cat

1, D2 θ(m, m)

, c3 =Cat

1, D1 θ(m, 1)

, c4 = Cat

1, D1 θ(m, 2)

, c5 =Cat

1, D2 θ(1, m)

, c6 =Cat

1, D2 θ(2, m)

.

Then:

Cat

2, D1 θ(m, m)

=1 −c1, Cat

2, D2 θ(m, m)

=1 −c2, Cat

2, D1 θ(m, 1)

=1 −c3,

Cat

2, D1 θ(m, 2)

=1 −c4, Cat

2, D2 θ(1, m)

=1 −c5, Cat

2, D2 θ(2, m)

=1 −c6.

Note that imperfect denoisers need not be inconsistent, meaning that there is no reason to enforce any relationship between c1,..., c6 ∈(0, 1).

<!-- Page 24 -->

Let’s take for our example x = (1, 1).

Then, from equation 1:

Eθ,unif(x) = 1

L!

X σ∈ΣL

L X i=1 log

Cat(xσ(i); Di θ(xσ(<i)

= 1

2 log(c1c2c3c5).

To find pgreedy θ (x), we use equation 14:

pgreedy θ (x) =

X σ∈ΣL

L Y i=1

Cat xσ(i); Dσ(i)

θ (xσ(<i))

Fθ,ϕ(xσ(<i), xσ(i), σ(i))

= c1c5Fθ,ϕ((m, m), 1, 1)Fθ,ϕ((1, m), 1, 2) + c2c3Fθ,ϕ((m, m), 1, 2)Fθ,ϕ((m, 1), 1, 1) =: c1c5d1 + c2c3d2.

d1, d2 will be found as functions of the c’s, and we will find c’s such that

(c1c5d1 + c2c3d2)2 < c1c2c3c5 Taking log of both sides and dividing by 2, the inequality will be shown.

Inserting the definition of Fθ,ϕ from equation 5 and the specific choice of Gϕ from equation 6, we have

Fθ,ϕ((m, m), 1, 1) = Ez∼D2 θ(m,m) [Cat (1, Gϕ((1, z), (m, m)))]

= c2Cat (1, Gϕ((1, 1), (m, m))) + (1 −c2)Cat (1, Gϕ((1, 2), (m, m))) = c21c1>c2 + (1 −c2)1c1>1−c2 and

Fθ,ϕ((1, m), 1, 2) = Ez∼D1 θ(1,m) [Cat (2, Gϕ((z, 1), (1, m)))]

= c5Cat (2, Gϕ((1, 1), (1, m))) + (1 −c5)Cat (2, Gϕ((2, 1), (1, m))) = c5 + (1 −c5) = 1, so d1 = c21c1>c2 + (1 −c2)1c1>1−c2. Here 1 denotes the indicator function.

Similarly,

Fθ,ϕ((m, m), 1, 2) = Ez∼D1 θ(m,m) [Cat (2, Gϕ((z, 1), (m, m)))]

= c1Cat (2, Gϕ((1, 1), (m, m))) + (1 −c1)Cat (2, Gϕ((2, 1), (m, m))) = c11c1<c2 + (1 −c1)11−c1<c2 and Fθ,ϕ((m, 1), 1, 1) = 1, so d2 = c11c1>c2 + (1 −c1)11−c1>c2.

Taking any c1, c2 such that c2 > c1 and 1 > c1 + c2, we get d1 = 0 and d2 = c1. Then

(c1c5d1 + c2c3d2)2 = c2

1c2 2c2 3 < c1c2c3c5 ⇔c1c2c3 < c5 There are many choices here that work. For instance, c1 = c3 = 1/4, c2 = c5 = 1/2, as c1c2c4 = 1/32 < 1/2 = c5.

Note that this means there are data distributions and denoisers for which

Lunif(θ) = −Ex0∼pdata

Eθ,unif(x0

< −Ex0∼pdata h log pgreedy θ (x0)

i

,

(recall here the discussion in Subsection A.1.3), so

DKL(pdata||pgreedy θ) = −H(pdata) −Ex0∼pdata h log pgreedy θ (x0)

i

> −H(pdata) + Lmask(θ).

This means that training to make Lmask(θ) small cannot provide any guarantee that pgreedy θ is close to pdata.

<!-- Page 25 -->

A.2 INSTANTIATIONS

Our general P-ELBO recovers familiar training objectives when we plug in specific planners.

Uniform planner. If Gϕ selects uniformly among masked tokens—that is, Cat(i; Gϕ(z, x)) = 1/NM(x) for masked i and 0 otherwise–then planner-based sampling reduces to vanilla ancestral sampling. In this case Gϕ does not depend on z, which makes Eθ,ϕ

2 (x0) = 0. Substituting into Prop. 3.2, we exactly recover the standard DLM ELBO in equation 1.

Greedy planner. If Gϕ always selects the most confident position according to the denoiser, as in equation 6, then the sampling path becomes deterministic. The associated ELBO is then as follows: Corollary A.9. Let Y0 = (m,..., m), and define recursively for k = 1,..., L:

jk = arg max i: Y i k−1=m

Cat(xi

0; Di θ(Yk−1)), Y i k = xjk

0, i = jk, Y i k−1, otherwise.

For pgreedy θ the distribution of xL under greedy ancestral sampling, log(pgreedy θ (x0)) ≥ Eθ,greedy(x0) = L Ek∼Unif([0:L−1])



X i: Y i k =m log Cat(xi

0; Di θ(Yk))



.

Compared to the uniform case in equation 1, the greedy ELBO only accumulates logits along the greedy path defined by the denoiser. This highlights the mismatch: the standard DLM objective trains on uniformly random paths, but greedy inference relies on a single deterministic path.

Soft greedy planner. We use the soft greedy planner:

Cat j; Gτ ϕ(z, x)

:= exp

1 τ log

Cat(zj; Dj θ(x)

/Cτ(z, x) (15)

Cτ(z, x):=

L X i=1,xi=m exp

1 τ log

Cat(zi; Di θ(x)

.

as a regularized approximation to the greedy planner 6 in order to motivate, after performing the series of modifications discussed in §3.4, the PAPL training algorithm 1. The ELBO associated to this choice of planner is: Corollary A.10. For pτ θ the distribution of xL resulting from the planned sampling Algorithm of §3 with Gϕ = Gτ ϕ as in equation 15, we have:

log(pτ θ(x0)) ≥Eθ,ϕ,τ

1 (x0) + Eθ,ϕ,τ

2 (x0),

Eθ,ϕ,τ

1 (x0) = L E k∼Unif([0:L−1])



 E xk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))





Eθ,ϕ,τ

2 (x0) = L E k∼Unif([0:L−1])

E xk∼rτ k(·;x0)

E z∼Dθ(xk)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk))×

× log

Cτ(x0, xk)

Cτ(z−i,xi

0, xk)

!

, where here we recall the notation z−i,xi

0 means the i’th coordinate of z is replaced by the i’th coordinate of x0, and rτ k(x; x0) = P(Y x0 k = x) for Y x0 the discrete time Markov chain with rate matrix equation 16

Rτ(y, x; x0) =

Cat(i; Gτ ϕ(x0, x))Cat(yi; δ(xi

0)), dHAM(x, y) = 1, xi̸ = yi, xi = m 0, otherwise (16)

and Y x0

0 = (m,..., m).

<!-- Page 26 -->

We remark that while this is simply used as an approximation to greedy ancestral sampling for the purposes of this manuscript, soft greedy sampling is also used in practice in, e.g. Wang et al. (2025a)’s “Confidence Based Schedule,” so this result is of independent interest as a corrected ELBO to these sampling schemes.

Other unmasking schemes. We remark there are other unmasking schemes in the literature for which one obtains an ELBO via our Proposition 3.2. For example, to obtain an ELBO for the “top probability margin” method of Kim et al. (2025), one inserts the choice

Gϕ(z, x) = δ arg max i:xi=m

|Cat(y; Di θ(x)) −Cat(¯y; Di θ(x))|

, where y = arg maxj∈V Cat(j; Di θ(x)) and ¯y = arg maxj̸=y∈V Cat(j; Di θ(x)). As the focus of this work is obtaining a viable objective for use with greedy ancestral sampling, we do not provide expanded details on how to train for this planner user our ELBO.

Extensions to remasking and denoising multiple positions simultaneously. So far we assumed that once unmasked, a token remains fixed. In practice, planners such as RDM (Zheng et al., 2023) P2 (Peng et al., 2025a) allow remasking and resampling, in addition to denoising multiple tokens simultaneously. There are also methods which attempt to denoise multiple tokens simultaneously, but do not allow remasking, such as top-k block denoising Nie et al. (2025b) and confidence thresholding Wu et al. (2025). Our proof technique extends naturally to these cases, yielding planner-aware ELBOs of the same form as Prop. 3.2. For completeness, in §A.4 we provide a generalization to P2-style planners and show its specialization to P2-TopK, in addition to discussion how the generalized version of the ELBO could be used for finding training stragies for these other sampling methods.

A.2.1 PROOF OF COROLLARY A.9 (ELBO FOR GREEDY PLANNER)

Specializing the ELBO from Proposition 3.2 to the case of greedy-ancestral sampling, we set Gϕ to be as in equation 6.

Proof. We first observe that inserting the choice of Gϕ from equation 6 into equation 2 in the place of 1/NM(x), Y x0 becomes deterministic, with dynamics Y0 = (m,..., m), and

Y i k =

( xjk−1

0, i = jk−1 Y i k−1, otherwise, k = 1,..., L, jk = argmaxi∈[1:L],Y i k =mCat(xi

0; Di θ(Yk)), k = 0,..., L.

For Eθ,ϕ

1 (x0), we have by definition Cat(i; Gϕ(x0, xk)) = Cat(i; δ(jk)), so:

Eθ,ϕ

1 (x0) =

L−1 X k=0 log

Cat(xjk

0; Djk θ (Yk)

Similarly, for the term Eθ,ϕ

2 (x0), we have, recalling the definition of Fθ,ϕ from equation 5:

Eθ,ϕ

2 (x0) =

L−1 X k=0 log

Fθ,ϕ(Yk, xjk

0, jk)

=

L−1 X k=0 log



 

X z∈VL:Cat(zi;Di θ(Yk))<Cat(x jk 0;D jk θ (Yk)),∀i∈[1,L],Y i k =m,i̸=jk

L Y i=1

Cat(zi; Di θ(Yk))



 

≥

L−1 X k=0 log



 Y i∈[1,L],Y i k =m,i̸=jk

Cat(xi

0; Di θ(Yk))



by definition of jk

=

L−1 X k=0

L X i=1,Y i k =m,i̸=jk log

Cat(xi

0; Di θ(Yk))

.

Summing this expression of Eθ,ϕ

1 with this lower bound on Eθ,ϕ

2 we have the result of Corollary A.9.

<!-- Page 27 -->

A.2.2 PROOF OF COROLLARY A.10 (ELBO FOR SOFTMAX PLANNER)

We now specialize the ELBO found in Proposition 3.2 to a smooth approximation of the greedy ancestral planner from equation 6 - namely, we take Gϕ = Gτ ϕ as in equation 15.

Proof. Eθ,ϕ,τ

1 is simply inserting Gϕ = Gτ ϕ into Eθ,ϕ from Proposition 3.2.

Now we make a lower bound on Eθ,ϕ

2 (x0). With this choice of Gϕ:

Eθ,ϕ

2 (x0) = −

L−1 X k=0



Exk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cat(i; Gτ ϕ(x0, xk))

F τ θ,ϕ(xk, xi

0, i)

! 

 where F τ θ,ϕ is as in equation 5 with Gϕ = Gτ ϕ. So, by Jensen’s inequality:

Eθ,ϕ

2 (x0)

= −

L−1 X k=0



Exk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cat(i; Gτ ϕ(x0, xk))





+

L−1 X k=0



Exk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

F τ θ,ϕ(xk, xi

0, i) 



≥−

L−1 X k=0



Exk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cat(i; Gτ ϕ(x0, xk))





+

L−1 X k=0



Exk∼rτ k(·;x0)





L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk))Ez∼Dθ(xk)

h log

Cat i; Gτ ϕ(z−i,xi

0, xk i









=

L−1 X k=0

Exk∼rτ k(·;x0)

Ez∼Dθ(xk)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk))×

× log





Cat i; Gτ ϕ(z−i,xi

0, xk

Cat(i; Gτ ϕ(x0, xk))





=

L−1 X k=0



Exk∼rτ k(·;x0)



Ez∼Dθ(xk)





L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cτ(x0, xk) Cτ(z−i,xi

0, xk)











, where in the last step we use that for any z, Cat i; Gτ ϕ(z−i,xi

0, xk and Cat(i; Gτ ϕ(x0, xk)) have the same numerator in equation 15, just different normalizing constants. This lower bound is denoted as Eθ,ϕ,τ

2 in Corollary A.10.

A.2.3 CONNECTION BETWEEN COROLLARY A.10 AND THE PAPL LOSS EQUATION 7

Here we show how one formally arrives at the PAPL loss from the detach gradient and stabilization steps taken in §3.4. We begin with the loss corresponding to the ELBO from Corollary A.10. This is given by:

L(θ, ϕ) = −Ex0∼pdata h

Eθ,ϕ,τ

1 (x0) + Eθ,ϕ,τ

2 (x0)

i

, where Eθ,ϕ,τ

1, Eθ,ϕ,τ

2 are as in Corollary A.10.

Next, we detach logits from the softmax weights Gτ ϕ given by equation 15. Observing that Eθ,ϕ,τ

2 depends only on these weights (through Cτ) and not on the logits from the denoiser, we have

<!-- Page 28 -->

minimizing L(θ, ϕ) is equivalent to minimizing:

L(θ) = −Ex0∼pdata h

Eθ,ϕ,τ

1 (x0)

i

= −

L−1 X k=0

E x0∼pdata



 E xk∼rτ k(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))



.

After this, we replace sampling xk ∼rτ k(·; x0) with sampling xk ∼rk(·; x0) with rk as in equation 3. Indeed, this was the reason for using the softmax approximation of Corollary A.10 rather than the greedy ELBO of Corollary A.9 in the first place- which the deterministic paths from Eθ,greedy may be very far from the uniformly random paths of rk, at least we have rτ k →rk as τ →∞. The loss becomes:

L(θ) = −

L−1 X k=0

E x0∼pdata



 E xk∼rk(·;x0)

L X i=1,xi k=m wi,τ log

Cat(xi

0; Di θ(xk))



, where wi,τ = Cat(i; Gτ ϕ(x0, xk)) ∝exp

1 τ log

Cat(zj; Dj θ(x)

. Finally, we observe that this is identical to the vanilla loss

Lunif(θ) = −Ex0∼pdata

Eθ,unif(x0)

associated to the vanilla ELBO equation 1, except that 1 L−k has been replaced by wi,τ as the weight in the sum. Thus, interpolating with a constant which decreases linearly with the number of samples yields:

LPAPL(θ) = −Ex0∼pdata

Eθ,unif(x0)

−

L−1 X k=0

E x0∼pdata



 E xk∼rk(·;x0)

L X i=1,xi k=m α L −k wi,τ log

Cat(xi

0; Di θ(xk))





= −

L−1 X k=0

E x0∼pdata



 E xk∼rk(·;x0)

L X i=1,xi k=m

1 L −k (1 + αwi,τ) log

Cat(xi

0; Di θ(xk))



.

Suppressing the distributions of the random variables x0, k, xk in the notation, this is precisely equation 7.

A.2.4 COMPARING RELATIVE SIZE OF THE APPROXIMATE LOSSES

Here we will see how the vanilla DLM loss (recalling here the discussion in A.1.3 and equation 3):

Lunif(θ) = −Ex0∼pdata

Eθ,unif(x0)

= −LEx0∼pdata



Ek∼Unif([0:L−1])



Exk∼rk(·;x0)





L X i=1,xi k̸=m

1 L −k log

Cat xi

0; Di θ(xk)











 compares with the surrogate corrected loss:

Lτ(θ) = −LEx0∼pdata

Ek∼Unif([0:L−1])

Exk∼rk(·;x0)

L X i=1,xi k=m

Cat(i; Gτ ϕ(x0, xk))×

× log

Cat(xi

0; Di θ(xk))

, which is the PAPL loss before interpolation with the vanilla MDM loss as per the previous subsection.

Here recall rk(·; x0) from equation 3 and Cτ, Gτ from equation 15.

Proposition A.11. For any τ1 > τ2 > 0, Lunif(θ) ≥Lτ1(θ) ≥Lτ2(θ).

<!-- Page 29 -->

Proof. As the expected values are over the same distributions, it suffices to prove the result for the integrands. Let x0, xk ∈VL and M = {i ∈{1,..., L}: xi = m}. Note |M| = L −k by definition. Define:

ℓi = log

Cat xi

0; Di θ(xk)

, i ∈M so that

Cat(i; Gτ ϕ(x0, xk)) = exp(ℓi/τ)/Cτ(ℓ):= wi τ(ℓ)

Cτ(ℓ) =

X i∈M exp(ℓi/τ).

Noting the minus sign in front of the losses, we simply need to establish that

X i∈M

1 L −k ℓi ≤

X i∈M wi τ1(ℓ)ℓi ≤

X i∈M wi τ2(ℓ)ℓi.

Observing that limτ→∞wi τ(ℓ) = 1 L−k, ∀i ∈M and ℓ, we simply show that d dτ

X i∈M wi τ(ℓ)ℓi < 0, ∀τ > 0.

Letting F(τ) = P i∈M wi τ(ℓ)ℓi, We have d dτ wi τ(ℓ) = wi τ(ℓ) τ 2



X j∈M wj τ(ℓ)ℓj −ℓi



= wi τ(ℓ) τ 2

F(τ) −ℓi

, so d dτ F(τ) =

X i∈M wi τ(ℓ) τ 2

F(τ) −ℓi ℓi = 1 τ 2

"

(F(τ))2 −

X i∈M wi τ(ℓ)(ℓi)2

#

.

By Jensen’s inequality, (F(τ))2 ≤P i∈M wi τ(ℓ)(ℓi)2, so we are done.

A.3 ALTERNATIVE PROOF OF PROPOSITION 3.2: CONTINUOUS TIME MARKOV CHAINS PERSPECTIVE

Here, for reference, we show how Proposition 3.2 can be derived from the continuous time Markov chains perspective taken in the discrete diffusion literature (Campbell et al., 2022; 2024; Lou et al., 2024; Sun et al., 2023).

A.3.1 TIME-INHOMOGENEOUS CONTINUOUS TIME MARKOV CHAINS (CTMC)

A (time-inhomogeneous) continuous-time Markov chain {Xt}t≥0 on a finite set X is a stochastic process satisfying the Markov property, which can be formally summarized as P(Xt = y|Xs1 = x1,..., Xsk = xk, Xs = x) = P(Xt = y|Xs = x), ∀y, x1,..., xk, x ∈X, 0 ≤s1 < s2 <... < sk < s < t ≤1. One can construct such a process by specifying a “rate matrix” Qt ∈R|X|×|X| with Qt(y, x) > 0 and Qt(x, x) = −P y̸=x Qt(y, x) for all x̸ = y ∈X and t ≥0. Along with an initial distribution µ ∈∆|X|, Q determines the 1-dimensional time marginals P(Xt = ·) ∈∆|X| via the Kolmogorov equation:

d dtP(Xt = ·) = QtP(Xt = ·), t ≥0 (17)

P(X0 = x) = µ(x), x ∈X.

When the above holds, we will say Q “generates” X. Note that one can see necessarily that if Q generates X,

Qt(y, x):= lim s↓t d dsP(Xs = y|Xt = x), x̸ = y ∈X. (18)

<!-- Page 30 -->

Knowing the entries of Q also provides a means of generating samples from Xt at any given time, since paths of {Xt}t≥0 can be realized via a sequence of jump times {τn}n∈N, with τi = inf{t > τi−1: Xt̸ = Xτi−1} and the effective discrete-time jump process {Xτi}i∈N. Then

P(Xτi+1 = y|Xτi+1 = x, τi = t) = −Qt(y, x)

Qt(x, x), (19)

and log(P(τi+1 > t|Xτi = x, τi = s)) =

Z t s

Qp(x, x)dp. (20)

For more background on time-inhomogenous continuous-time Markov chains, see e.g. Chapter 2 of Yin & Zhang (2013) or the appendix of Ren et al. (2025).

A.3.2 DLMS IN THE CTMC FRAMEWORK

In the original CTMC framework for DLMs (Lou et al., 2024; Shi et al., 2024; Sahoo et al., 2024), one begins with a coordinate-wise forward corruption process:

pt(xi t|xi

0) = Cat(xi t; αtδ(xi

0) + (1 −αt)δ(m)) (21)

for α: [0, 1] →[0, 1] a differentiable, monotone-decreasing function with α0 = 1 and α1 = 1. Using equation equation 17, one sees that noising each coordinate independently according to corresponds to a CTMC

→ Xt with state space VL, intial data x0 and rate matrix given by, for x, y ∈VL

→ Q x0 t (y, x) =

 

 σ(t), dHAM(x, y) = 1, xi̸ = yi, xi = m −σ(t)NM(x), x = y 0, otherwise where σ(t) = −d dt log(αt).

One then uses a classic time-reversal formula (see, e.g. Sun et al. (2023) Proposition 3.2.) to obtain a rate matrix generating

← X x0 t so that P

←

X x0 t = x

= P

→

Xt = x|

→ Xt = x0

, ∀x ∈VL. This rate matrix is given by, for x, y ∈VL:

← Q x0 t (y, x) =

 

 βtCat(yi; δ(xi

0)), dHAM(x, y) = 1, xi̸ = yi, xi = m −βtNM(x), x = y 0, otherwise

(22)

where βt:= − dα1−t dt 1 −α1−t (23)

Letting τk for k ∈N be the time of

← X x0 t ’s k’th jump, we have by equation 20:

log P(τk+1 > t|τk = s,

← X x0 τk = x) = −NM(x)

Z t s βτdτ and by equation 19, for x̸ = y:

P(

← X x0 τk+1 = y|

← X x0 τk = x, τk+1 = t)

=

1/NM(x), dHAM(x, y) = 1, xi̸ = yi, xi = m, yi = xi

0 0, otherwise. (24)

That is, one waits for an exponential clock to ring with the given speed, then regardless of how long it took, chooses uniformly at random between masked positions of x to get some index i, and unmasks that token to xi

0.

<!-- Page 31 -->

One then seeks to denoise from (m,..., m) to x0 ∼pdata using the CTMC

← X θ,unif t with state space VL which one obtains via replacing δ(xi

0) in equation 22 with a neural denoiser Di θ(x). A rate matrix generating

← X θ,unif t is given by, for x, y ∈VL:

Qθ,mask(y, x) =

 

 βtCat(yi; Di θ(x)), dHAM(x, y) = 1, xi̸ = yi, xi = m −βtNM(x), x = y 0, otherwise

. (25)

This means, letting τ θ k for k ∈N be the time of

← X θ,mask t ’s k’th jump, we have by equation 20:

log P(τ θ k+1 > t|τ θ k = s,

← X θ,mask τk = x) = −NM(x)

Z t s βτdτ (26)

and by equation 19, for x̸ = y:

P(

← X θ,mask τk+1 = y|

← X θ,mask τk = x, τk+1 = t)

=

Cat(yi; Di θ(x))/NM(x), dHAM(x, y) = 1, xi̸ = yi, xi = m, yi̸ = m 0, otherwise. (27)

That is, one waits for an exponential clock with the same given speed as for

← X x0 to ring, then regardless of how long it took, chooses uniformly at random between masked positions of x to get some index i, and unmasks that token to yi with probability Cat(yi; Di θ(x)).

This is summarized succinctly via the corresponding Gillespie sampling scheme for a standard masked diffusion model, which, defining

M(x):= {j ∈{1,..., L}: xj = m}, x ∈VL (28)

is given by Alg. 3.

## Algorithm

## 3 Gillespie Sampler for Masked Diffusion

Models

1: Initialize: x0 ←(m, m,..., m), denoiser Dθ 2: for k = 0: L −1 do 3: Choose Random Coordinate for Unmasking: 4: Sample dimension i ∼Unif

M(xk)

5: Denoise: 6: Sample zi ∼Di θ(xk) 7: xk+1 ←xk 8: xi k+1 ←zi

9: end for 10: return xL 11:

A.3.3 SETUP AND ELBO IN THE CTMC FRAMEWORK

Now we show how to derive a corrected ELBO for the dynamics described by Alg. 2 as one would using the CTMC framework. First, we observe that for any ˜Y x0 a CTMC on time interval [0, 1] and state space S such that P(˜Y x0

1 = x0) = 1 and p a distribution on S given by p(x) = P(X1 = x) for another CTMC on time interval [0, 1] and state space S:

log(p(x0)) = −DKL(δ(x0)||p) ≥−DKL(Rx0||Q), (29)

where we let Rx0 denote the distribution of ˜Y x0 (on the Skorokhod space D([0, 1]; S) of all c´adl´ag paths from [0, 1] to VL) and Q the same but for X, and to get the bound, we use the data-processing inequality (an infinite-dimensional generalization of Corollary A.4- see, e.g. Budhiraja & Dupuis (2019) Lemma 2.4 (f)).

<!-- Page 32 -->

That is, in order to make the terminal distribution p of X close to δ(x0), one can simply require that its entire path is close to that of ˜Y x0.

The benefit of using the KL divergence between the paths is that via Girsanov’s Theorem for Markov Jump processes (see e.g. Theorem III.5.34 in Jacod & Shiryaev (2013) for a general result or Ren et al. (2025) Theorems 3.3/3.5 for the specific Markov Chain setting) it yields a simple expression in terms of the rate matrices generating the dynamics of ˜Y x0 and X.

This result states that, for a CTMC Y with rate matrix Rt and Y0 ∼µ and a CTMC X with rate matrix Qt and X0 ∼ν on the same state space S, denoting by R the distribution of Y on D([0, 1]; S) and Q similarly but for X. the equality:

DKL(R||Q) = DKL(µ||ν) (30)

+

Z 1

0 Ext∼rt



Rt(xt, xt) −Qt(xt, xt) +

X y∈S,y̸=xt

Rt(y, xt) log

Rt(y, xt)

Qt(y, xt

)



dt rt(x):= P(Yt = x), x ∈S.

holds a under mild assumptions on R and Q (see remark 3.4 in Ren et al. (2025)). Note that equation 30 is simply a continuous time extension of Proposition A.6. Recalling equation 20, the term Rt(xt, xt) −Qt(xt, xt) measures the difference in jump times between X and Y, while the second term is essentially a KL divergence between the transition rates.

We proceed by identifying a CTMC Xθ,ϕ with state space VL such that P

Xθ,ϕ

1 = x

= pGϕ θ (x), so that we may apply equation 29 and equation 30 to pGϕ θ obtain an ELBO. Denoting by Qθ,ϕ t the rate matrix for Xθ,ϕ, via equation 4 and equation 19, we must have for any t ∈[0, 1] and x̸ = y ∈VL:

−Qθ,ϕ t (y, x)

Qθ,ϕ t (x, x)

=

Cat yi; Di θ(x)

Fθ,ϕ(x, yi, i), dHAM(x, y) = 1, xi̸ = yi, xi = m 0, otherwise.

As the transition probabilities do not depend on the transition rates, we simply need that the transition rates are so that by time 1 all tokens will become unmasked. We thus simply maintain those from vanilla DLMs, found in equation 26, and so, recalling equation 20, we set for x ∈VL:

Qθ,ϕ(x, x) = −βtNM(x), where we recall βt from equation 23.

We then have our full definition of Qθ,ϕ. For x, y ∈VL:

Qθ,ϕ(y, x) =

 

 βtNM(x)Cat yi; Di θ(x)

Fθ,ϕ(x, yi, i), dHAM(x, y) = 1, xi̸ = yi, xi = m −βtNM(x), x = y 0, otherwise

.

(31)

Letting Rt(·, ·; x0) be the rate matrix for our reference chain Y x0 to be used for inserting into equation 29, since we don’t want to worry about enforcing the jump times of Xθ,ϕ and Y x0 in the form of the ELBO (as these have no bearing on the sample generated by

← X θ,ϕ and hence should not be trained for), we also set for x ∈VL:

Rt(x, x; x0) = −βtNM(x).

Now, to choose the off diagonal entries of Rt(·, ·; x0), we seek to modify jump locations to be different than in the vanilla setting, where the coordinate to flip is chosen uniformly at random (see equation 24).

Instead, we opt to choose R(·, ·; x0) = RGϕ(·, ·; x0) to select coordinates to denoise according to the planner. In this sense, we will be learning both the forward and reverse process simultaneously when using this ELBO.

<!-- Page 33 -->

Recalling equation 19, we thus want for x̸ = y ∈VL:

−RGϕ(y, x; x0)

RGϕ(x, x; x0) =

Cat(i; Gϕ(x0, x))Cat(yi; δ(xi

0)), dHAM(x, y) = 1, xi̸ = yi, xi = m 0, otherwise.

Now the dynamics of Y x0 = Y Gϕ,x0 and its rate matrix R(·, ·; x0) = RGϕ(·, ·; x0) have been determined.

We have for x, y ∈VL:

RGϕ(y, x; x0) =

 

 βtNM(x)Cat(i; Gϕ(x0, x)), dHAM(x, y) = 1, xi̸ = yi, xi = m, yi = xi

0 −βtNM(x), x = y 0, otherwise

.

(32)

Note that, taking Y Gϕ,x0

0 = Xθ,ϕ

0 = (m,..., m), indeed Y Gϕ,x0

1 = x0, so that equation 29 applies.

We arrive at the following proposition: Proposition A.12. For any planner Gϕ, we have the following ELBO:

log(pGϕ θ (x0)) ≥Eθ,ϕ

1 (x0) + Eθ,ϕ

2 (x0), where, letting rGϕ t (·; x0) be the distribution of Y Gϕ,x0 with rate matrix equation 32 and Y Gϕ,x0

0 = (m,..., m):

Eθ,ϕ

1 (x0) =

Z 1

0 βt E xt∼r

Gϕ t (·;x0)

NM(xt)

L X i=1,xi t=m

Cat(i; Gϕ(x0, xt)) log

Cat(xi

0; Di θ(xt))

dt

Eθ,ϕ

2 (x0) = −

Z 1

0 βt E xt∼r

Gϕ t (·;x0)

NM(xt)

L X i=1,xi t=m

Cat(i; Gϕ(x0, xt)) log

Cat(i; Gϕ(x0, xt))

Fθ,ϕ(xt, xi

0, i)

dt

Proof. Let Rx0 denote the distribution of paths of Y Gϕ,x0 and Qθ,ϕ those of Xθ,ϕ from the preceeding discussion. Then, by equation 29, log(pGϕ θ (x0)) ≥−DKL(Rx0||Qθ,ϕ). From equation 30, we have, using Y Gϕ,x0 and Xθ,ϕ have the same initial data so that the first KL term is 0:

−DKL(Rx0||Qθ,ϕ)

= −

Z 1

0 Ext∼r

Gϕ t (·;x0)

−Qθ,ϕ t (xt, xt) + RGϕ(xt, xt; x0)

+

X y̸=xt

RGϕ(y, xt; x0) log

RGϕ(y, xt; x0)

Qθ,ϕ t (y, xt)

!

dt

= −

Z 1

0 βtExt∼r

Gϕ t (·;x0)

NM(xt)

L X i=1,xi t=m

Cat(i; Gϕ(x0, xt))×

× log

Cat(i; Gϕ(x0, xt)) Cat(xi

0; Di θ(xt))Fθ,ϕ(xt, xi

0, i)

dt

= Eθ,ϕ

1 (x0) + Eθ,ϕ

2 (x0).

This form is seen to be equivalent to that in Proposition 3.2 in the next subsection.

A.3.4 TIME INDEPENDENT FORMULATION OF THE ELBO

Now we observe that, as expected, the ELBO is independent of the time schedule αt (and hence βt). We start by observing that

P(NM(Y Gϕ,x0 t) = k) =

L k exp

−

Z t

0 βsds k

1 −exp

−

Z t

0 βsds

L−k

.

<!-- Page 34 -->

One can see this via law of competing exponentials or solving equation 17 for the pure death chain representing the number of mask states.

Then, recalling that the transition probabilities for Y Gϕ,x0 t are independent of time and using equation 19, we have Y Gϕ,x0 t |NM(Y Gϕ,x0 t) = L −k is equal in distribution to ¯Y Gϕ,x0 k, where ¯Y Gϕ,x0 is the effective discrete time Markov chain with rate matrix equation 16.

Denoting by ¯pGϕ k (·; x0) the distribution of ¯Y Gϕ,x0 k, we have, for example:

Eθ,ϕ

1 (x0) =

L X k=1

L k

Z 1

0 βt exp

−

Z t

0 βsds k

1 −exp

−

Z t

0 βsds

L−k dt

× kExk∼¯p

Gϕ L−k(·;x0)

L X i=1,xi k=m

Cat(i; Gϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))

.

Using exp(−

R 1

0 βsds) = exp(− R 1

0 d ds log(α1−s)ds) = lims↓0 exp(log(α(1 −s)) −log(α(0))) = lims↓0 α(1 −s) = 0 since α(1) = 0, α(0) = 1, we have

Z 1

0 βt exp

−

Z t

0 βsds k

1 −exp

−

Z t

0 βsds

L−k dt =

Z 1

0 uk−1(1 −u)L−kdu

= B(k, L −k + 1)

= 1 k

L k where B is the beta function.

Thus, changing k to L −k in the sum, we have:

Eθ,ϕ

1 (x0) =

L−1 X k=0

Exk∼¯p

Gϕ k (·;x0)

L X i=1,xi t=m

Cat(i; Gϕ(x0, xk)) log

Cat(xi

0; Di θ(xk))

.

Recalling that ¯pGϕ k is what is denoted as pGϕ k (we only added the bar here to distinguish it from the distribution of the continuous time chain), we see Eθ,ϕ

1 from Proposition A.12 is equal to Eθ,ϕ

1 from 3.2.

Applying the same manipulations to Eθ,ϕ

2 (x0), we arrive at the following:

Proposition A.13. For Eθ,ϕ

1, Eθ,ϕ

2 as in Proposition 3.2 and Eθ,ϕ

1, Eθ,ϕ

2 as in Proposition A.12, we have:

Eθ,ϕ

1 (x0) = Eθ,ϕ

1 (x0), Eθ,ϕ

2 (x0) = Eθ,ϕ

2 (x0), ∀x0 ∈VL.

That is, rather than simulate the CTMC up to some random time t ∼Unif(0, 1) to obtain a sample of Y Gϕ,x0 t, one may instead either sample an entire trajectory of the discrete time chain ¯Y Gϕ,x0 and accumulate losses, or sample a random number of jumps k ∼Unif([0: L −1]) and a trajectory of

¯Y Gϕ,x0 k up to time k.

A.4 GENERALIZATION TO PLANNERS WITH REMASKING (P2-STYLE)

P2 (Peng et al., 2025a) allows for the remasking of clean tokens while still requiring that the number of unmasked tokens in xk is k. We replace the planner Gϕ: VL × VL →∆L with a sequence of planners Gk ϕ,2: VL × VL →∆(

L k), k = 1,..., L, where Gk ϕ,2 outputs a distribution on subsets of size k of [1: L]. We then do:

In P2, we in practice use “P2-Topk”, which corresponds to:

Gk ϕ,2(z, x) = δ

Top-ki∈[1:L]

Cat i; ˆGη ϕ(z, x)

, (33)

<!-- Page 35 -->

## Algorithm

## 4 Gillespie

Sampler with a P2-Planner

1: Initialize: t ←0, x0 ←(m,..., m), P2 planner {Gk ϕ,2}L k=1, denoiser Dθ 2: for k = 0: L −1 do 3: Plan Sample z ∼Dθ(xk) 4: Sample dimensions Ik+1 = (i1,..., ik+1) ∼Gk+1 ϕ,2 (z, xk)

5: Denoise 6: xi k+1 ←zi for i ∈Ik+1

7: xi k+1 ←m for i̸ ∈Ik+1

8: end for 9: return xL 10:

where for i ∈{1,..., L} and η ≥0

Cat(i; ˆGη ϕ(z, x)) ∝ηCat(xi; δ(m))Cat(zi; Di θ(x)) +

1 −Cat(xi; δ(m))

Cat(zi; Bi ϕ(z)) (34)

in the case of P2-BERT, and

Cat(i; ˆGη ϕ(z, x)) ∝ηCat(xi; δ(m))Cat(zi; Di θ(x)) +

1 −Cat(xi; δ(m))

Cat(zi; ˆDi θ(x)) (35)

in the case of P2-self. Here the output of the denoiser in unmasked positions i of x is no longer assumed to be δ(xi) when we write it as ˆD, an Bϕ denotes an external BERT model. η is a “stochasticity parameter” which controls the frequency of remasking - increasing η boosts ˆGη in masked positions, so that unmasked positions are more likely to fall outside of the Top-k and be remasked.

A.4.1 DERIVING THE TRANSITION PROBABILITIES

Here we derive the one step transition probabilities for Alg. 4. This is the analogue of equation 4 in the setting where we generalize to allow for remasking.

Let pGϕ,2 θ ∈∆dL denote the distribution on VL of a sample obtained via running Alg. 4, and let pGϕ,2 θ,k+1(·|xk) ∈∆dL denote the distribution of xk+1 given xk. With abuse of notation, we will also let pGϕ,2 θ,k+1(·, ·|xk) ∈∆dL2 denote the joint distribution xk+1 and the k + 1’st sample z. Note that NM(xk+1) = L −(k + 1) with probability 1. So for y ∈VL with NM(y) = L −(k + 1), we let C(y) = {i ∈[1: L]: yi̸ = m}, and have:

pGϕ,2 θ,k+1(y|xk) =

X z∈V pGϕ,2 θ,k+1(y, z|xk)

=

X z∈V:zi=yi,∀i∈C(y)

L Y j=1

Cat zj; Dj θ(xk)

Cat

C(y); Gk+1 ϕ,2 (z, xk)

=

Y i∈C(y)

Cat yi; Di θ(xk)

X z∈VL

L Y j=1

Cat zj; Dj θ(xk)

Cat

C(y); Gk+1 ϕ,2 (z−y, xk)

=

Y i∈C(y)

Cat yi; Di θ(xk)

F k+1 θ,ϕ,2(xk, y) (36)

where

F k+1 θ,ϕ,2(xk, y):= Ez∼Dθ(x)

h

Cat

C(y); Gk+1 ϕ,2 (z−y, x)

i

, (37)

and for z, y ∈VL, we denote by z−y ∈VL the sequence which is the same as z except with zi replaced by yi for all i ∈C(y). Note by our assumption on Dθ that this is 0 if yi̸ = xi k in a position where yi, xi k̸ = m. Also note that the proof was the exact same as in Subsection A.1.6.

<!-- Page 36 -->

A.4.2 MARKOV CHAIN SETUP AND ELBO FOR P2 PLANNER

Now we observe how to apply Proposition A.7 to get an ELBO for pGϕ,2 θ. We will then specialize this to the case of P2-TopK, and discuss the difficulties in obtaining a “regularized” approximation similar to Corollary A.10 which lends itself to a computationally viable approximation as in Subsection 3.4.

By equation 36, we have pGϕ,2 θ (x) = P(XGϕ,2,θ

L = x), where XGϕ,2,θ is the time homogenous Markov chain on VL with transition matrix given for x, y by:

Qθ,ϕ,2(y, x) =

Y i∈C(y)

Cat yi; Di θ(x)

F L−NM(y)

θ,ϕ,2 (x, y) (38)

when NM(y) = NM(x) −1 and yi = xi, ∀i ∈C(y) ∩C(x) and 0 otherwise.

Once again, to obtain an ELBO for pGϕ,2 θ using Proposition A.7, we select any family of transition matrices R(·, ·; x0) parameterized by x0 ∈VL determining a family Markov chains Y x0 such that equation 10 holds.

We choose, as in Subsection A.1.4, Y x0 = Y Gϕ,2,x0 to be the Markov chain with rate matrix obtained from replacing Di θ(x) with δ(xi

0) in equation 38. Recalling the definition of Fθ,ϕ,2 from equation 37, this yields R(·, ·; x0) to be RGϕ,2(·, ·; x0) given by, for x, y ∈VL:

RGϕ,2(y, x; x0) =

Y i∈C(y)

Cat yi; δ(xi

0))

Cat

C(y); GL−NM(y)

ϕ,2 (x0, x)

(39)

when NM(y) = NM(x) −1 and 0 otherwise.

Note that indeed equation 10 holds, since at the k’th step Y x0 k always has L −k masks, with the positions of the masks determined by sampling from the planner at each step.

Applying now Proposition A.7 with this choice of RGϕ,2(y, x), we obtain:

Proposition A.14. For any P2-style collection of planners Gk ϕ,2, k ∈[1, L], let pGϕ,2 θ denote the distribution of xL obtained via the iterative sampling scheme Alg. 4. Then we have the following ELBO:

log(pGϕ,2 θ (x0)) ≥Eθ,ϕ,2

1 (x0) + Eθ,ϕ,2

2 (x0),

Eθ,ϕ,2

1 (x0) =

L−1 X k=0

E xk∼r

Gϕ,2 k (·;x0)

X y∈XL−k−1(x0)

Cat(C(y); Gk+1 ϕ,2 (x0, xk))×

×

X i∈C(y)

log

Cat(xi

0; Di θ(xk))

Eθ,ϕ,2

2 (x0) = −

L−1 X k=0

E xk∼r

Gϕ,2 k (·;x0)

X y∈XL−k−1(x0)

Cat(C(y); Gk+1 ϕ,2 (x0, xk))×

× log

Cat(C(y); Gk+1 ϕ,2 (x0, xk))

F k+1 θ,ϕ,2(xk, y)

!

where rGϕ,2 k (x; x0) = P(Y x0 k = x) for Y x0 the discrete time Markov chain with rate matrix equation 39 and Y x0

0 = (m,..., m), and here we recall the notation Xk(x0) from equation 1.

Specializing to P2 Top-k, where Gϕ,2 is as in equation 33 so the jump positions of Y x0 are deterministic and defined recursively via (suppressing the dependence on x0 in the notation):

Ik = Top-ki∈[1:L]Cat(i; ˆGη ϕ(x0, Yk−1)), k = 1,..., L, I0 = ∅ (40)

Y i k = xi

0, i ∈Ik m, i̸ ∈Ik,

<!-- Page 37 -->

We have Gk+1 ϕ,2 = δ(Ik+1). So Eθ,ϕ,2

1 becomes:

Eθ,ϕ,top-k

1 (x0) =

L−1 X k=0

X i∈Ik+1 log

Cat(xi

0; Di θ(Yk))

.

Eθ,ϕ,2(x0) similarly becomes:

Eθ,ϕ,top-k(x0) =

L−1 X k=0 log

F k+1 θ,ϕ,2(Yk, Yk+1)

.

Recalling the definition of F k+1 θ,ϕ,2, we have here that:

F k+1 θ,ϕ,2(Yk, Yk+1)

=

X z∈VL:Cat(i; ˆ Gη ϕ(z−Yk+1,Yk))<Cat(j; ˆ Gη ϕ(z−Yk+1,Yk))),∀j∈Ik+1,i̸∈Ik+1

L Y i=1

Cat(zi; Di θ(Yk))

≥

Y i̸∈Ik+1

Cat(xi

0; Di θ(Yk)), by definition of Ik+1. Thus we have:

Eθ,ϕ,top-k

1 (x0) + Eθ,ϕ,top-k(x0)

≥

L−1 X k=0



X i̸∈Ik+1 log(Cat(xi

0; Di θ(Yk))) +

X i∈Ik+1 log(Cat(xi

0; Di θ(Yk))





=

L−1 X k=0

L X i=1 log(Cat(xi

0; Di θ(Yk)) =

L−1 X k=0

L X i=1,Y i k =m log(Cat(xi

0; Di θ(Yk)), where in the last step we recall that we impose Di θ(Yk) = δ(Y i k) if Y i k̸ = m, and for any i such that Y i k̸ = m, Y i k = xi

## 0 The resulting ELBO specializing

Proposition A.14 to P2-Topk is just the same as that for greedy ancestral in Corollary A.9, except that the paths are determined by the P2-style sequence of planners:

Corollary A.15. For ptop-k θ the distribution of xL from Alg. 4 with Gϕ as in equation 33, we have:

log(ptop-k θ (x0)) ≥Eθ,top-k(x0),

Eθ,top-k(x0) = LEk∼Unif([0:L−1])





L X i=1,Y i k =m

Cat(xi

0; Di θ(Y x0 k))



, where Y x0 satisfies the recursion equation 40.

However, regularizing the δ in the definition of the P2-Topk planner equation 33 to make it have full support, and hence be better approximated by a uniformly random style of sampling, quickly reveals that using such the ELBO becomes computationally prohibitive, even using e.g. the soft-max gumbel noise trick. Recall this is precisely what we did for the greedy ancestral planner using the softmax approximation done in Corollary A.10. This additional overhead arises because for each randomly sampled time step k, one would need not only to simulate Y x0 k to time k, which requires k function evaluations of the planner, but also to compute and sum over all of the

L k−1 weights corresponding to the

L k−1 values of y which are possible locations for the next jump in the reference dynamics in lower bound Proposition A.14. For this reason, even though we use P2-Topk sampling in our experiments, we assume the role of remasking is relatively minimal compared to the unmasking selection process, so that the series of approximations inspired by Corollary A.10 outlined in §3.4 and detailed in §A.2.3 still results in a training objective more reflective of the sampling process than the vanilla loss equation 1.

<!-- Page 38 -->

Also note that, in P2 (Peng et al., 2025a), the ELBO result was proved assuming a continuous-time dependent, randomly sampled unmasking process, although the top-k sampling procedure Alg. 4 with Gϕ,2 as in equation 33 was used in practice. This creates a similar mismatch between training and sampling that is present in vanilla DLMs vs. greedy ancestral - see Proposition 3.1. The results shown here are for the practically used P2-Topk sampling procedure, hence there is little to no overlap in the analysis performed between the manuscripts.

A.5 OTHER SAMPLING METHODS WITH MULTIPLE DENOISING POSITIONS AND/OR REMASKING

We show here how one can view other sampling strategies in the literature as special cases of Alg. 4 and hence train also for these strategies using the result of Proposition A.14.

RDM sampling Zheng et al. (2023). is captured by taking

Gk ϕ,2(z, x) = δ

Top-ki∈[1:L]

Cat zi; ˆDi θ(x)

, where ˆDθ is as in equation 35. This strategy uses the denoisers logits on both masked and unmasked positions, and only keeps tokens which fall in the top−k threshold.

Top-j Block denoising Nie et al. (2025b). is captured by taking

Gk ϕ,2(z, x) = δ

Top-ji∈B(x)

Cat zi; Di θ(x)

∪{i: xi̸ = m}

.

Here previously unmasked tokens are kept, B(x) is a block of masked positions of x of a predetermined fixed size, and j is a fixed desired number of positions to be denoised at each step. Note that time here should instead only run to ⌊L/j⌋rather than L −1, since at this point all tokens will be clean.

Confidence Thresholding Wu et al. (2025).: In this strategy, the number of tokens to be clean at a given time step is adaptive to how many tokens exceed a certain confidence threshold. This means that one would need to allow k in Alg. 4 to change adaptively based on z and x. While we don’t provide details here for the sake of brevity, one can make such a modification to the sampling algorithm and follow the general principle of writing down the transitions of the discrete time Markov chain for the generation dynamics in terms of a planner and comparing with paths which use a supervised planner using Proposition A.7 to obtain a rigorous ELBO in such regimes.

B EXPERIMENTAL DETAILS

B.1 PROTEIN SEQUENCE GENERATION

Setup. We evaluate our approach against leading protein sequence generation models. The comparison includes three discrete diffusion models—DPLM (Wang et al., 2024), EvoDiff (Alamdari et al., 2023), and ESM3 (Hayes et al., 2025)—along with the autoregressive baseline ProGen2 (Nijkamp et al., 2023). Each model generates 100 sequences for target lengths in 200, 300,..., 800. DPLM follows its standard setting, using a sequence length tied to the number of sampling steps and temperature 0.9, with rejection resampling disabled to ensure fairness. ESM3 is sampled with temperature 1.0, cosine noise schedule, top-p = 1, and 500 denoising steps. Special tokens are stripped to guarantee valid amino acid outputs.

Evaluation. Generated sequences are assessed using structure prediction as a proxy for functional plausibility. Specifically, we fold each sequence with ESMFold (Lin et al., 2023) and extract three structural metrics:

• pLDDT (predicted Local Distance Difference Test): an estimate of local per-residue confidence, defined as the expected accuracy of predicted interatomic distances. Formally, for residue i, pLDDT(i) = 100 × E

"

1 − |dpred ij −dtrue ij | dtrue ij

## j∈N (i)

,

<!-- Page 39 -->

where dij denotes pairwise distances and N(i) indexes local neighbors. The reported score is the average over residues.

• pTM (predicted Template Modeling score): measures global structural similarity between predicted and true structures, adapted from the TM-score (Zhang & Skolnick, 2004). Given length L and alignment u(i) between residues, pTM = max alignments u

1 L

L X i=1

1

1 + di,u(i)/d0(L)

2, where di,u(i) is the distance deviation and d0(L) is a length-dependent scaling factor.

• pAE (predicted Alignment Error): estimates the expected positional error in aligning residue i of the predicted structure to residue j of the true structure. Formally, pAE(i, j) = E h

∥xpred i −xtrue j ∥2 i

, averaged across all residue pairs. Lower values indicate better global alignment.

Since high local confidence can mask poor global geometry (e.g., high pLDDT but high pAE), we combine these into a binary foldability criterion: the fraction of sequences with pLDDT > 80, pTM > 0.7, and pAE < 10. This composite measure penalizes degenerate patterns (e.g., repetitive “ABABAB” sequences) that often achieve misleadingly high scores in isolation.

In addition to structural metrics, we compute two distributional statistics that capture whether the model avoids mode collapse:

• Token entropy: measures per-position variability of amino acid usage across generated sequences. Let A denote the set of amino acids observed in the generated set, and p(a) the empirical frequency of amino acid a ∈A. The token entropy is

H = −

X a∈A p(a) log p(a), with higher values indicating richer amino acid usage.

• Sequence diversity: quantifies variability across full sequences. For a batch {x(1),..., x(B)} of equal length L, define pairwise identity as

Id(x(m), x(n)) = 1

L

L X i=1

1 h x(m)

i = x(n)

i i

.

The sequence diversity is then

Diversity = 1 − 2 B(B −1)

X

1≤m<n≤B Id(x(m), x(n)), which ranges from 0 (identical sequences) to 1 (completely dissimilar).

Training Details for the 150M DLM We train a 150M-parameter masked diffusion model on protein data. Training follows the open-source DPLM implementation1, using the same transformer backbone as DPLM-150M and ESM2-150M. The model is trained from scratch for 500k steps with an effective batch size of 320k tokens per iteration, achieved via multi-GPU, multi-node training with gradient accumulation on L40, H100, and A100. The dataset is UniRef50, which contains roughly 40M protein sequences clustered at 50% sequence identity, ensuring non-redundant coverage. UniRef50 is a widely adopted resource for protein language modeling.

1https://github.com/bytedance/dplm

<!-- Page 40 -->

B.2 TEXT GENERATION

B.2.1 SETUP

Dataset. We use the OPENWEBTEXT (OWT) corpus2, a large-scale collection of English web pages curated to match the distribution of OpenAI’s WebText. The dataset is preprocessed with the GPT-2 byte-pair tokenizer and sequences are wrapped or truncated to a maximum length of L = 1024 tokens. For evaluation, a held-out split is reserved to compute distributional metrics.

Baselines. We compare against a wide range of autoregressive and diffusion-based language models:

• AR (GPT-style): standard autoregressive language model trained on OWT.

• MDLM (Sahoo et al., 2024): masked diffusion language model with uniform random masking.

• MDLM + FB / DFM (Campbell et al., 2024): MDLM augmented with forward–backward or discrete flow matching correctors.

All checkpoints are reused from prior work for comparability.

Training. We follow the same training configurations as in MDLM (Sahoo et al., 2024). Unless otherwise noted, models are initialized with the same GPT-2 tokenizer and architecture. Training details are:

• Optimizer: AdamW, with learning rate 3 × 10−4 and linear warmup of 2.5k steps.

• Batch size: 32 sequences per GPU, 16 H100 GPUs in total.

• Gradient clipping: 0.1.

• Training steps: 228k steps, with checkpoints saved every 19k steps.

Sampling and Decoding. We use P2 self-planning (Peng et al., 2025a) in sampling. Unless otherwise specified, we use:

• 64-bit floating-point, as prior work showed 32-bit sampling led to reduced diversity.

• nucleus sampling with p = 0.9.

• 5,000 sequences per model–sampler pair.

Evaluation. We evaluate generated text against the held-out OWT distribution. Metrics include:

• MAUVE (Pillutla et al., 2021): MAUVE directly compares the generated distribution from a text generation model to a distribution of human-written text using divergence frontiers. Generated samples and a ground-truth corpus of data are embedded using an external language model. The two distributions are compared in the embedding space using an area under the divergence curve to summarize both Type I and Ttype II errors.

• Generative perplexity (Gen PPL.): cross-entropy of generated samples under a pretrained language model. This measures the concordance of the model under consideration and a strong pretrained language model on the generated text. This can be problematic as it only considers generated text. Some distributions of text make it much simpler (and thereby better Gen PPL) even when not satisfactory to a human reader.

• Entropy: average per-token entropy of the generated distribution. This measures the token diversity of the generated text. Model collapse can be evaluated if entropy decreases substantially.

MAUVE is a most robust indicator, while Gen PPL. can be gamed by overconfident sampling schedules. For all evaluation metrics we match the settings of Wang et al. (2025a).

2http://Skylion007.github.io/OpenWebTextCorpus

<!-- Page 41 -->

B.2.2 ABLATION OF SAMPLING METHODS

**Table 5.** compares inference-time planners while holding the denoiser fixed. Across all step budgets, P2-Self sampling consistently yields the best quality–diversity tradeoff: it achieves the highest MAUVE and the lowest generative perplexity, with only a mild reduction in entropy relative to Greedy and Probability Margin. The gap is most pronounced in the fast-sampling regime. At T = 64, Greedy decoding as in MaskGIT (Chang et al., 2022) substantially underperforms, suggesting that purely myopic confidence selection can lock the trajectory into suboptimal local choices when the model is imperfect. Probability Margin (Kim et al., 2025) improves over Greedy at intermediate and large T, but remains below P2-Self and does not scale monotonically with more steps, indicating that margin-based heuristics are less robust to sampling budget. Overall, these results reinforce that planner choice remains a crucial degree of freedom at inference, and that the P2 framework (Peng et al., 2025a) provides a more reliable path selection rule for converting denoiser confidence into high-quality generations.

**Table 5.** Comparison of Greedy, Probability Margin, and P2-Self Sampling across metrics and number of sampling steps.

Metric Method T = 32 T = 64 T = 128

MAUVE

Greedy 0.011 0.021 0.056 Probability Margin 0.011 0.039 0.051 P2-Self 0.013 0.046 0.067

Gen PPL

Greedy 44.34 34.18 29.38 Probability Margin 44.27 34.37 29.39 P2-Self 40.19 29.98 24.33

Entropy

Greedy 5.35 5.30 5.25 Probability Margin 5.35 5.30 5.25 P2-Self 5.32 5.24 5.16

B.3 CODE GENERATION

B.3.1 SETUP

We evaluate PAPL on code generation. Training follows the Open-dLLM framework (Peng et al., 2025b), where we initialize from Qwen2.5-Coder and adapt it to the diffusion setting with bidirectional attention. The model is trained on the FineCode corpus, which integrates the opc-annealing-corpus and Ling-Coder-SyntheticQA, providing both algorithmic and synthetic QA data. Following the Open-dLLM recipe, each training sequence is randomly masked with a ratio uniformly sampled from [0, 1], and the model is optimized with a cross-entropy loss over masked positions, weighted by the inverse of the mask ratio. This ensures compatibility with the released training pipeline, data recipes, and evaluation protocols.

## Evaluation

is conducted on the following benchmarks:

• HUMANEVAL (Chen et al., 2021): 164 hand-written Python programming problems designed to test functional correctness.

• MBPP (Austin et al., 2021b): 974 crowd-sourced Python problems of varying difficulty.

• HUMANEVAL+ and MBPP+: augmented variants that extend the original datasets with paraphrased prompts and additional test cases.

For code infilling, we use HUMANEVAL-INFILL (Bavarian et al., 2022) and the Python subset of SANTACODER-FIM (Sagtani et al., 2025). We report pass@1 and pass@10 for HUMANEVAL and MBPP, and exact match for SANTACODER-FIM, following the official evaluation protocols. To examine length control, we additionally test under different initial mask spans (4, 8, 16, 32, 64) and report their averaged results.

<!-- Page 42 -->

Training Loss

Training Step

Validation Loss

Training Step

**Figure 5.** Training with pure PAPL loss (τ = 1) leads to unstable behavior, with large fluctuations in training (left) and poor convergence on validation (right).

B.3.2 ABLATION OF SAMPLING METHODS

We ablate the role of the sampling strategy while keeping the denoiser and training setup fixed. Table 6 compares P2-self against several commonly used alternatives: (i) vanilla ancestral sampling with uniform unmasking, (ii) greedy ancestral sampling that always selects the highest-confidence positions, (iii) entropy-based confidence ordering, and (iv) the TopK-margin heuristic. Across all six code benchmarks, P2-self is consistently the strongest method. The improvements are most pronounced in Pass@1, where P2-self exceeds the best baseline by large margins (e.g., 20.8 vs. 12.6 on HumanEval and 16.7 vs. 9.2 on MBPP), and it also yields steady gains in Pass@10 and in the infilling and SantaCoder evaluations. Among baselines, confidence-aware orderings (greedy ancestral and entropy-based confidence) substantially outperform vanilla ancestral sampling, indicating that exploiting denoiser uncertainty during decoding is critical for code generation. However, these heuristics remain myopic: they make locally optimal unmasking decisions without explicitly reasoning about longer-range dependencies or future refinement steps, which limits their ability to traverse the high-probability decoding trajectories that matter at inference. TopK-margin is weaker than other confidence-based methods, suggesting that hard-thresholding margins can be overly conservative and discard useful intermediate updates. Overall, this ablation shows that simply reordering unmasking by instantaneous confidence is insufficient; self-planning with path-level lookahead is necessary to fully close the training–inference gap and achieve robust gains.

## Method

HumanEval HumanEval+ MBPP MBPP+ HumanEval Infill SantaCoder P@1 P@10 P@1 P@10 P@1 P@10 P@1 P@10 P@1 P@1

P2-self 20.8 38.4 17.6 35.2 16.7 38.4 23.9 53.6 77.4 56.4 Vanilla Ancestral 3.3 18.3 3.2 15.2 1.8 13.2 2.9 21.8 72.7 53.8 Greedy Ancestral 9.3 31.1 8.1 28.7 5.3 29.0 8.7 41.5 75.1 53.7 Entropy-based Confidence 12.6 35.4 10.9 29.9 9.2 36.8 15.2 50.7 75.1 53.2 TopK-Margin 7.6 27.4 6.5 26.2 3.9 24.0 6.2 33.5 75.0 54.4

**Table 6.** Performance comparison across coding benchmarks for sampling different methods.

C ADDITIONAL RESULTS

C.1 UNSTABLE TRAINING WITH PURE PAPL LOSS

We investigate the effect of training solely with the PAPL loss under the default temperature setting (τ = 1). As shown in Figure 5, training exhibits large fluctuations and fails to achieve stable convergence on the validation loss. We hypothesize that this instability arises from the denoiser becoming overly confident: the path weights bias the model toward a narrow set of generation paths, which reduces diversity and leads to overfitting.

![Figure extracted from page 42](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-042-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 42](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-042-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 43 -->

**Figure 6.** Vanilla MDM vs PAPL Training Curves. Early in training, the PAPL loss remains small because the denoiser has not yet formed meaningful beliefs about the correct token positions, causing the planner-dependent weights wi to be close to zero. As the model begins to identify correct positions with higher certainty, these weights increase, leading to a temporary rise in the PAPL loss. Once the denoiser becomes sufficiently confident, the loss decreases and eventually mirrors the behavior of the standard MDM loss. These dynamics provide additional evidence that PAPL naturally adapts its emphasis as the model’s confidence improves, stabilizing precisely when confidence becomes a reliable signal.

C.2 COMPARISON OF TRAINING CURVES WITH VANILLA MDM LOSS

In Figure 6 we observe that the PAPL loss exhibits distinct training curves compared to the vanilla MDM loss. In particular, initially the PAPL loss is small, because the denoiser has not established any confidence about the correct token positions, and hence the weights wi are near-zero. As the denoiser gains confidence about the correct token positions during the initial training stages, the weights and hence loss increase, before decreasing with a curve similar to that of the vanilla MDM loss.

C.3 EMPIRICAL ESTIMATION OF THE EFFECT OF THE APPROXIMATION STEPS

Loss Greedy E1softmax

E2softmax

Vanillasoftmax

PAPLsoftmax

E1rand

E2rand

PAPL Vanilla

Value 23294.002 3.364 17.897 17.897.002 3.365 18.362 18.362

**Table 7.** Ablation of the approximation steps used to obtain the PAPL loss.

Here we provide Table 7, where we empirically estimate the effect of the series of approximations used to move from the true ELBO of Proposition 3.2 specialized to Greedy Ancestral (see Corollary A.9) the PAPL loss equation 7. Here, rather than sampling a random timestep k, we sum along the entire generation trajectory. Greedy is the full greedy loss from Corollary A.9, calculated along the true greedy path from Corollary A.9. We remark that this term is extremely large due to the crude lower bound on Eθ,ϕ

2 used to arrive at A.9 from Proposition 3.2. E1-softmax is the contribution of the term Eθ,ϕ,τ

1 from specialization of Proposition 3.2 to the softmax planner from Corollary A.10 to the true softmax loss, and E2-softmax is the contribution of Eθ,ϕ,τ

## 2 PAPL-softmax is the PAPL loss equation 7 but with xk sampled from the softmax path from

Corollary A.10, and Vanilla-softmax is the vanilla loss from equation 1 but with xk sampled from the softmax path. Finally, E1-rand and E2-rand are the contribution of Eθ,ϕ,τ

1, Eθ,ϕ,τ

2 Corollary A.10 but taken along a random path, and PAPL and Vanilla are the actual PAPL and Vanilla losses, which are computed along the random path by definition.

The losses are estimated via accumulating along the entire trajectories for a batch-size of 1024, using the PAPL-fine-tuned protein MDM with α = 5 and τ = 1.

We remark that the computations of the E2 terms are highly unstable. However, we can observe still in Table 7 the following: As predicted by Proposition 3.1, Greedy Loss is much larger than Vanilla Loss - Vanilla Loss does not provide an upper bound for greedy ancestral sampling, so we would expect the true upper bound to be larger. Moreover, as predicted by Proposition A.11, when computed

![Figure extracted from page 43](2026-ICLR-planner-aware-path-learning-in-diffusion-language-models-training/page-043-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 44 -->

along the same path, E1 is dominated by the vanilla loss. Finally, we observe that indeed the path taken in terms of unmasking order does have effect on the losses - the losses increase while taking a random path. This is expected, as it is known that taking a random path, as is trained for in vanilla MDMs, yields significantly worse sample quality than a greedy or soft-greedy path.

C.4 HUMANEVAL PERFORMANCE ANALYSIS

We evaluated the model on 40 HumanEval tasks. While it handles straightforward problems well, performance declines sharply for tasks requiring careful constraint handling, multi-step logic, or less familiar algorithms.

Strengths The model performs best when tasks align with standard Python idioms or textbook solutions. In HumanEval/12: longest, for example, it produced the compact and idiomatic implementation in Listing 1, which is more direct than the canonical reference.

Listing 1: Model’s solution for HumanEval/12: longest.

def longest(strings: list) -> str

| None: if not strings:

return None return max(strings, key=len)

Listing 2: Canonical solution.

def longest(strings: list) -> str

| None: if not strings:

return None maxlen = max(len(x) for x in strings) for s in strings:

if len(s) == maxlen:

return s

The model also demonstrates competence in basic algorithmic tasks. For example, HumanEval/25: factorize was solved with a standard trial division approach (Listing 3), and string prefix generation (HumanEval/14) and set-based deduplication (HumanEval/34) were handled correctly.

def factorize(n: int) -> list[int]:

factors = [] while n % 2 == 0:

factors.append(2) n //= 2 i = 3 while i * i <= n:

while n % i == 0:

factors.append(i) n //= i i += 2 if n > 2:

factors.append(n) return factors

Listing 3: Model’s correct solution to HumanEval/25: factorize.

Weaknesses The most common failures stem from flawed algorithmic reasoning. In HumanEval/9: rolling max, the model produced a redundant nested loop instead of the correct single-pass running maximum (Listing 4).

Another recurring issue is misinterpretation of constraints. In HumanEval/3: below zero, the model ignored the requirement to detect negative balances at any point, checking only the final state instead (Listing 5).

Finally, there are occasional catastrophic failures, where the generated code bears no relation to the task. In HumanEval/2: truncate number, for instance, the model produced irrelevant

<!-- Page 45 -->

## Model (incorrect) def rolling_max(numbers: list) -> list[int]:

result = [] max_val = numbers[0] i = 0 while i < len(numbers):

max_val = max(max_val, numbers[i]) while i < len(numbers): # Redundant nested loop max_val = max(max_val, numbers[i]) i += 1 result.append(max_val) return result

## Canonical def rolling_max(numbers: list) -> list[int]:

running_max = None result = [] for n in numbers:

running_max = n if running_max is None else max(running_max, n) result.append(running_max) return result

Listing 4: Incorrect vs. canonical solutions for HumanEval/9: rolling max.

## Model (incorrect) def below_zero(operations: list[int]) -> bool:

balance = 0 for op in operations:

## Missing balance update logic if balance < 0:

return False return balance < 0

## Canonical def below_zero(operations: list[int]) -> bool:

balance = 0 for op in operations:

balance += op if balance < 0:

return True return False

Listing 5: Misinterpretation of temporal constraint in HumanEval/3: below zero.

variable assignments and returned the input unchanged, instead of applying a simple modulo operation (Listing 6).

## Model (incorrect) def truncate_number(number: float) -> float:

a, b, c = 1, 2, 3 # Irrelevant assignments return number

## Canonical def truncate_number(number: float) -> float:

return number % 1.0

Listing 6: Catastrophic failure on HumanEval/2: truncate number.

<!-- Page 46 -->

## Discussion

Overall, the model succeeds when tasks resemble common idioms or well-documented examples, but struggles as soon as prompts introduce layered constraints or require multi-step reasoning. The lack of self-checking mechanisms is evident in tautological or irrelevant code that would be immediately rejected by a human programmer. While the system can accelerate routine coding tasks, it cannot yet be relied upon for problems that demand algorithmic novelty or strict logical consistency. Improving decomposition of complex prompts and incorporating verification steps remain key directions for future work.

D PRACTITIONER’S GUIDE

There are two main parameters for PAPL, temperature τ and loss weight α. For practitioners, we recommend initial settings of τ = 1 and α = 1. All experiments in this work leave τ = 1. We experimented with α values in the range 1... 10. We found that higher values of α can be more effective in the range of ≈5, especially for protein models, but not beyond that. If hyperparameter tuning with PAPL, we therefore recommend starting with τ = 1 and α = 1 and doubling α to efficiently search the space.

We recommend this because there is no huge issue with setting α as low as 0, the model will still achieve good performance, as a reminder α = 0 recovers standard DLM training. However, you may not get the benefit of PAPL training, and slow convergence on practical inference paths.

With α too high, the training may become unstable, and may not be trained well on all paths. We hypothesis this may hinder performance on more out of distribution tasks, where the planner is not as confident, or may hinder performance by learning sub-optimal paths for generation by latching on to a specific path too quickly.
