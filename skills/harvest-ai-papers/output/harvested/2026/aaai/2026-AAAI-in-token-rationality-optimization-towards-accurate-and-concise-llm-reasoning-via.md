---
title: "In-Token Rationality Optimization: Towards Accurate and Concise LLM Reasoning via Self-Feedback"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40826
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40826/44787
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# In-Token Rationality Optimization: Towards Accurate and Concise LLM Reasoning via Self-Feedback

<!-- Page 1 -->

In-Token Rationality Optimization: Towards Accurate and Concise LLM

Reasoning via Self-Feedback

Mingye Zhu1, Yi Liu2*, Zheren Fu1, Quan Wang3, Yongdong Zhang1

1University of Science and Technology of China, Hefei, China 2State Key Laboratory of Communication Content Cognition, People’s Daily Online, Beijing, China 3Beijing University of Posts and Telecommunications, Beijing, China

## Abstract

Training Large Language Models (LLMs) for chain-ofthought reasoning presents a significant challenge: supervised fine-tuning on a single “golden” rationale hurts generalization as it penalizes equally valid alternatives, whereas reinforcement learning with verifiable rewards struggles with credit assignment and prohibitive computational cost. To tackle these limitations, we introduce InTRO (In-Token Rationality Optimization), a new framework that enables both tokenlevel exploration and self-feedback for accurate and concise reasoning. Instead of directly optimizing an intractable objective over all valid reasoning paths, InTRO leverages correction factors—token-wise importance weights estimated by the information discrepancy between the generative policy and its answer-conditioned counterpart, for informative nexttoken selection. This approach allows the model to perform token-level exploration and receive self-generated feedback within a single forward pass, ultimately encouraging accurate and concise rationales. Across six math-reasoning benchmarks, InTRO consistently outperforms other baselines, raising solution accuracy by up to 20% relative to the base model. Its chains of thought are also notably more concise, exhibiting reduced verbosity. Beyond this, InTRO enables crossdomain transfer, successfully adapting to out-of-domain reasoning tasks that extend beyond the realm of mathematics, demonstrating robust generalization.

## Introduction

The remarkable success of Large Language Models (LLMs) is highlighted by their emergent ability to tackle complex reasoning and mathematical tasks. A critical breakthrough enabling these capabilities is Chain-of-Thought (CoT) reasoning (Wei et al. 2022; Yu et al. 2023; Wang et al. 2023; Hao et al. 2024), where models are instructed to generate step-by-step rationales before arriving at a final answer. The conventional approach to teaching CoT, supervised fine-tuning (SFT) with golden rationales, faces crucial limitations: obtaining high-quality step-by-step human annotations is prohibitively expensive, and reliance on singlesolution imitation often results in poor generalization as it penalizes equally valid alternative reasoning paths (Kumar et al. 2024; Chen et al. 2025a; Ni et al. 2022).

* Corresponding author: Yi Liu Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** When solving a reasoning task, the initial model gives a rationale (green) different from its answerconditioned counterpart (blue), InTRO leverages this information discrepancy to compute the correction factors during InTRO training, yielding an updated model that produces concise and accurate rationales (orange).

To enhance reasoning capabilities, recent research has predominantly focused on two alternative paradigms, each with distinct drawbacks. First, reinforcement learning (RL) with verifiable rewards, adopted by models such as OpenAIo1 (Jaech et al. 2024), DeepSeek-R1 (Guo et al. 2025), and Kimi-1.5 (Team et al. 2025), allows models to bootstrap multiple rationales beyond a single reference answer. However, such RL approaches suffer from sparse, sequence-level feedback that arrives upon rationale completion. This coarse-grained exploration faces the curse of dimensionality—with the space of valid reasoning sequences growing exponentially with length (Gao et al. 2025), further complicating effective credit assignment. Second, methods incorporating fine-grained feedback or process supervision address reward sparsity by employing external “verifier” models or human annotators to evaluate individual reasoning steps (Li et al. 2023; Weng et al. 2022; Chowdhury and Caragea 2025; Xie et al. 2024; Zhang et al. 2025b). While these process-level signals enhance credit assignment, they introduce challenges including limited labeled data, high annotation costs, significant computational overhead, and potential noise in verifier training.

The aforementioned approaches rely on either coarsegrained exploration or external feedback. Motivated by

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

35195

![Figure extracted from page 1](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

these limitations, we pose a fundamental question: Can a model autonomously explore at the token level while selfgenerating feedback signals, removing the dependency on external supervision? We answer this question affirmatively. However, realizing this capability hinges on solving the intractable objective of optimal reasoning. That is, the model must explore and evaluate reasoning steps in a way that genuinely reflects the true distribution over valid reasoning paths.

To this end, we propose In-Token Rationality Optimization (InTRO), a training framework that enables both token-level exploration and self-feedback for accurate and concise reasoning. InTRO approximates the intractable objective of optimal reasoning by aligning the model’s generative policy πθ(z | x) with its own posterior πθ(z | x, y) via KL divergence minimization, as this alignment yields equivalent gradient updates with optimal reasoning under mild assumptions. To implement this, we construct an estimated posterior by conditioning the model on the correct answer, which we denote as πθ(z | x ⊕y). This estimated posterior is used to compute correction factors—token-wise importance weights that reflect the information discrepancy between the generative policy and the posterior. These correction factors function as self-generated feedback, enabling the model to evaluate how much each token contributes toward the final answer in a single forward pass, thereby facilitating fine-grained, token-level exploration during training.

To elucidate InTRO’s intuitive operation, we present a simple illustration in Fig. 1 and outline the detailed training framework in Fig. 2. Starting from a query x, the policy πθ generates multiple rationales, retaining paths whose answers match the ground truth. For every retained prefix, the model samples n alternative next-token candidates from its forward policy, obtains the corresponding token probabilities from the estimated posterior by conditioning on the ground truth answer, and computes token-level correction factors. Subsequently, the weighted gradients reinforce the most accurate and logically salient actions, delivering dense, self-generated feedback at every reasoning step.

Empirically, across mathematical reasoning tasks, InTRO produces rationales that are remarkably shorter than strong RL baselines while lifting accuracy by up to 20% relative to the base model. Importantly, InTRO enables cross-domain transfer, successfully adapting to out-of-domain reasoning tasks that extend beyond mathematics, demonstrating robust generalization.

In summary, in this paper we:

• propose InTRO, a novel token-level exploration and endogenous dense-feedback paradigm for enhancing LLM reasoning capabilities • derive a theoretically grounded, practically feasible learning algorithm that aligns generative and answerconditioned policies via KL divergence minimization, which equates to solving an intractable optimal reasoning problem under mild conditions • demonstrate that InTRO exhibits superior performance and more concise rationales compared to state-of-the-art reasoning methods • provide evidence of enhanced cross-task generalization capabilities, indicating robust and transferable reasoning competence of InTRO.

In-Token Rationality Optimization 2.1 Preliminaries: Goal of Optimal Reasoning Let x denote the question, y denote the final answer, and z = (z1, z2, · · ·, zT) represent the CoT reasoning path, where zt is an intermediate token at step t. We use πθ to denote the model’s policy parameterized by θ. The standard training objective for CoT reasoning via SFT is to maximize the log-likelihood of a single “golden” reasoning path z∗:

LSFT = E(x,z∗,y)∼D [−log πθ(z∗, y | x)] (1) This approach is fundamentally limited as it forces the model to imitate a single reference solution, thereby assigning low probabilities to alternative but equally valid reasoning paths. A more principled objective is to maximize the marginal log-likelihood of the correct answer y (Hoffman et al. 2023), which involves summing over all valid rationales:

Lmarg. = E(x,y)∼D [−log πθ(y | x)]

= E(x,y)∼D



−log

X z∈Zy πθ(z, y | x)



, (2)

where Zy = {z: f(z) = y}. However, directly optimizing this marginal likelihood is intractable due to the exponential growth of the reasoning space.

## 2.2 From Intractability to Alignment with Model Posterior

Given that directly optimizing the marginal likelihood is intractable, we shift our perspective. Rather than explicitly summing over all valid rationales, we ask: What characterizes optimal reasoning? Intuitively, an optimal reasoning policy is one whose generative distribution πθ(z | x) naturally emphasizes correct and logically consistent rationales. Such rationales are exactly those the model itself would generate if it already knew the correct answer. Thus, we introduce the model’s answer-conditioned posterior, πθ(z | x, y), as an idealized “teacher” distribution that embodies correct reasoning.

The challenge then becomes: how do we train the “student” policy πθ(z | x) to emulate the “teacher” posterior πθ(z | x, y)? The most principled way to make one probability distribution resemble another is to minimize the KL divergence between them. In our case, we choose the forward KL divergence as it encourages the policy to broaden its support and better capture diverse valid solutions. This aligns with our goal of improving exploration while still focusing on logically grounded reasoning:

min θ DKL(πθ(z | x, y) ∥πθ(z | x))

= min θ Ez∼πθ(z|x,y)

log πθ(z | x, y)

πθ(z | x)

= min θ −Ez∼πθ(z|x,y)[log πθ(z | x)] + const.

(3)

35196

<!-- Page 3 -->

**Figure 2.** The illustration of the InTRO framework. Top. The policy πθ generates reasoning paths for query x and only paths that yield the correct answer are retained. Middle. For each retained prefix z<t we (i) sample n next tokens zi

t from the forward policy (green) and (ii) obtain the corresponding token probabilities from the estimated posterior by conditioning on the concatenated input x ⊕y (blue). The ratio of these probabilities gives the token-level correction factor wi t (orange) for zi t. Bottom. At every position, gradients are aggregated according to wi t, providing token-level feedback that guides training.

We treat the posterior as a fixed proposal distribution for estimating the expectation in the KL divergence. Under this view, the entropy term Ez∼πθ(z|x,y)[log πθ(z | x, y)] can be approximated as a constant. Therefore, we exclude it from the optimization objective in Eq. (3).

## 2.3 Gradient Equivalence to Marginal Likelihood

This KL-based alignment is not merely intuitive, rather, it theoretically equates our original intractable objective of marginal likelihood optimization in Eq. (2). Importantly, we first assume that y is a deterministic function of z, i.e., y = f(z), where f extracts the final answer from the reasoning path. Next, we establish this relationship through the following proposition (proof provided in Appendix A):A

Proposition 2.1 Under the assumption that y = f(z) is a deterministic function of z, the gradient of the marginal loglikelihood objective (Eq. (2)) is identical to the gradient derived from minimizing the KL-divergence objective (Eq. (3)):

∇θ log πθ(y | x) | {z } MLL Grad

= Ez∼πθ(z|x,y) [∇θ log πθ(z | x)] | {z } Grad derived from KL-minimization

(4)

Proposition 2.1 illustrates that by training the model to approximate the posterior πθ(z | x, y) over rationales z, we are, in fact, performing a gradient ascent on the marginal log-likelihood of producing the correct answer y.

## 2.4 Approximation with the Estimated Posterior While theoretically appealing, optimizing according to

Eq. (3) involves direct sampling from πθ(z | x, y), which is still infeasible. Therefore, we propose a practical estimated posterior, denoted as πθ(· | x⊕y), where ⊕is the concatenation operation. The underlying logic behind this choice leverages modern LLMs’ powerful in-context reasoning capabilities. Empirical evidence demonstrates that LLMs robustly interpret instructions embedded within their inputs (Wei et al. 2021; Ouyang et al. 2022; Shinn et al. 2023). Conditioning on both the original question x and the known correct answer y simultaneously provides the model with a clear, explicit instructional signal. Formally, conditioning on x⊕y can be viewed as instructing the model to justify a known solution.

Leveraging this insight, we invoke importance sampling with the proposal πθ(z | x), then Eq. (3) leads to:

Ez∼πθ(z|x)

πθ(z | x ⊕y)

πθ(z | x) log πθ(z | x)

. (5)

Critically, breaking down the above sequence-level importance weight at the token level yields:

w(z) =

T Y t=1 πθ(zt | x ⊕y, z<t)

πθ(zt | x, z<t). (6)

This allows us to compute token-level correction factors and derive the following practical objective of InTRO:

E(x,y)∼D



 1 |z| · n

|z| X t=1 n X i=1 wi t · log πθ(zi t | x, z<t)



, (7)

where wt,i = πθ(zi t | x⊕y, z<t) πθ(zi t | x, z<t) is the correction score for token zi t, and |z| refers to the length of the rational z. Sampling n alternatives per position directly encourages exploration and yields a low-variance gradient estimate. Tokens with correction factors wi t > 1 reflect high posterior confidence and are reinforced, whereas tokens with wi t < 1

35197

![Figure extracted from page 3](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

## Algorithm

1: InTRO:In-Token Rationality Optimization Input: Policy network πθ, training data D, number of sequences to generate per query G, number of tokens to explore per timestep n Output: Optimized policy π∗ θ 1: Initialize θ ←θold 2: for each training iteration do 3: Sample a batch of prompts x ∼D 4: for each prompt x do 5: Generate G rationales {zi}G i=1 ∼πθold(· | x) 6: Filter out invalid rationales (e.g., incorrect final answers) 7: for each valid rationale z do 8: for each timestep t = 1 to T do 9: Sample n token candidates {zj t }n j=1 including the ground-truth token zi t 10: end for 11: end for 12: end for 13: Compute the surrogate loss L(θ) (see Eq. (7)) 14: Update policy: θ ←θ + α∇θL(θ) 15: Set θold ←θ 16: end for 17: return π∗ θ are suppressed. This objective guides generation towards teacher-preferred tokens while refining the teacher’s judgment simultaneously. Moreover, in practice we clip wi t ∈ [0, 200] to ensure stability during training and curb unreliable teacher effects. The detailed algorithmic steps of InTRO are summarized in Algorithm 1.

Difference with traditional RL methods. Our InTRO objective, as shown in Eq. (7), maximizes the probability of explored actions weighted by the computed correction factors. This fundamentally differs from traditional RL algorithms that maximize expected rewards E[R]. Besides, RL methods typically operate by exploring at the sequence level, relying on sparse, rule-based rewards. In contrast, JAPO additionally leverages dense, token-level exploration with selfgenerated feedback, fostering a more accurate and concise internalization of principled reasoning paths.

## 3 Experiments

## 3.1 Models and Baselines

We mainly employ the Qwen series: Qwen2.5-1.5B/3B/7B base models and Qwen3-4B/8B base models, as this represents an established practice in the field for their advanced mathematical reasoning capabilities (Wang et al. 2025; Yan et al. 2025). We compare InTRO with several closely-related baselines: SFT, LaTRO (Chen et al. 2024), RAFT++ (Xiong et al. 2025), GPG (Chu et al. 2025) and GRPO (Shao et al. 2024). Detailed descriptions and objectives for each baseline method are available in Appendix B.1.

## 3.2 Implementation Details

Our implementation builds upon the OpenRLHF framework (Hu et al. 2024)1 with 80GB A100 GPUs. For training, we utilize problems with difficulty levels 3-5 from the MATH dataset (Hendrycks et al. 2021), comprising approximately 9.2k samples. All training experiments use a batch size of 128 and a learning rate of 5e-7. Following the findings of Liu et al. (2025), we avoid prompt templating for the Qwen family during both training and evaluation for better performance. For each training instance, we generate four candidate responses and assign binary outcomebased rewards (1.0 for correct, 0.0 otherwise). At each step we sample 5 alternative next-token candidates (including the ground-truth token from the original rationale). To ensure fair comparisons, baseline models are trained using their publicly available codebases and recommended hyperparameter settings, except for RAFT++, which was directly integrated into our experimental setup. Task-specific hyperparameters, including the number of sampled rationales per prompt and the binary reward structure, are held constant across all experiments.

## 3.3 Evaluation

Our evaluation focuses on two main categories: Indistribution mathematical reasoning and other out-ofdistribution (OOD) tasks. For mathematical reasoning, we employ a comprehensive suite of benchmarks: MATH500, Minerva Math, OlympiadBench, College Math, AMC23, and AIME25. All evaluations were conducted using the Qwen2.5-Math evaluation codebase 2. We set the sampling temperature to 0.6 and top-p to 0.95. We report pass@1 for all benchmarks except for AMC23 and AIME25, which have smaller test sets (40 and 30 problems, respectively). For these two tasks, we report avg@32 to mitigate sampling noise, providing a more robust performance indicator compared to pass@1. Consistent with our training procedure, no templates were applied during evaluation. While this might lead to performance disparities compared to templated evaluations (particularly for Minerva Math), it ensures consistency with our training methodology and allows for a clearer assessment of our model’s inherent reasoning capabilities.

To evaluate OOD performance, we test on a diverse set of benchmarks including LiveCodeBench (dynamic programming), BigCodeBench (code understanding and generation), GPQA (open-domain knowledge), HumanEval (functionlevel code generation), and IFEval (instruction following).

## 3.4 Experimental Results

InTRO improves in-distribution mathematical reasoning abilities. We conduct a comprehensive comparison with established baselines on several mathematical reasoning tasks, presented in Table 1. We see that InTRO consistently demonstrates superior performance, frequently achieving the highest accuracy. Notably, InTRO yields more significant performance gains on stronger models, such as

1https://github.com/OpenRLHF/OpenRLHF 2https://github.com/QwenLM/Qwen2.5-Math

35198

<!-- Page 5 -->

Math Reasoning MATH500 Minerva Math Olympiad College Math AMC23 AIME25 Average Impr.(%)

Accuracy % pass@1 pass@1 pass@1 pass@1 avg@32 avg@32 (over base)

Qwen2.5-1.5B 50.4 11.4 14.1 36.7 23.2 0.6 22.7 - SFT 39.2 7.7 15.3 34.2 14.6 0.5 18.6 -18.1 LaTRO 46.2 8.5 16.1 36.0 20.9 1.0 21.5 -5.3 RAFT++ 53.6 8.5 17.3 36.9 23.0 1.1 23.4 +3.1 GPG 51.2 8.5 16.4 37.1 23.8 0.8 23.0 +1.3 GRPO 50.6 9.6 17.9 37.0 24.5 1.1 23.5 +3.5 InTRO 54.2 9.6 19.6 38.4 25.5 1.8 24.9 +9.7

Qwen2.5-3B 57.2 15.4 21.5 38.9 30.9 1.6 27.6 - SFT 44.0 11.0 18.1 36.4 19.1 1.5 21.7 -21.4 LaTRO 53.2 14.3 21.2 38.4 31.4 1.4 26.7 -3.3 RAFT++ 59.0 15.1 26.4 40.5 35.6 2.8 29.9 +8.3 GPG 57.6 15.4 23.3 40.7 34.4 1.9 28.9 +4.7 GRPO 63.2 15.1 26.4 41.0 35.0 2.0 30.5 +10.5 InTRO 62.6 16.4 25.9 41.1 40.1 2.3 31.4 +13.8

Qwen2.5-7B 66.4 15.1 30.4 42.4 41.9 5.0 33.5 - SFT 51.0 11.0 23.0 37.3 21.6 2.8 24.5 -26.9 LaTRO 65.0 12.5 29.5 42.8 41.8 5.5 32.9 -1.8 RAFT++ 69.8 14.7 31.1 44.0 44.2 6.6 35.1 +4.8 GPG 69.2 18.4 32.1 43.6 44.1 5.3 35.5 +6.0 GRPO 71.8 17.6 33.9 44.7 46.2 5.1 36.6 +9.3 InTRO 72.6 19.9 35.3 45.0 47.0 5.6 37.6 +12.2

Qwen3-4B 69.0 12.5 31.3 30.3 45.5 8.9 32.9 - SFT 65.0 7.7 29.9 28.1 40.4 7.3 29.7 -37.1 LaTRO 67.8 12.5 31.6 29.6 47.1 8.2 32.8 -0.3 RAFT++ 73.6 15.8 34.7 34.0 52.5 8.3 36.5 +10.9 GPG 74.6 13.6 34.1 34.1 49.8 7.7 35.7 +8.5 GRPO 73.8 15.8 34.4 34.2 50.9 7.9 36.2 +10.0 InTRO 74.8 17.6 39.4 35.1 58.3 12.6 39.6 +20.4

Qwen3-8B 65.8 11.8 34.7 29.8 53.4 10.0 34.3 - SFT 61.6 11.0 34.1 22.6 41.6 8.9 30.0 -12.5 LaTRO 70.0 12.9 33.5 29.3 52.7 11.3 35.0 +2.0 RAFT++ 72.6 12.5 36.1 31.1 55.4 10.9 36.4 +6.1 GPG 70.4 15.4 33.8 31.4 53.5 10.1 35.8 +4.4 GRPO 74.4 14.3 36.3 33.1 55.8 10.9 37.5 +9.3 InTRO 75.2 18.8 38.7 35.2 56.7 12.4 39.5 +15.2

**Table 1.** Detailed performance of various models across multiple math benchmarks. The best result is in bold, the second best one is underscored. Our method consistently outperforms baselines across all model scales. Notably, stronger models (e.g., Qwen3 series) show greater performance gains, demonstrating up to 20% improvement compared to base models.

the Qwen3 series, indicating the scaling potential of In- TRO. Furthermore, InTRO shows substantial improvements on highly challenging datasets like Olympiad and AIME25, which demand complex, multi-step reasoning. This suggests that token-level exploration and intermediate feedback internalize a more principled and accurate reasoning process, especially for tackling intricate problems.

InTRO enhances out-of-distribution generalization performance. Enabling machines to reason precisely over math is central to automated scientific discovery, but realworld tasks extend far beyond math (Huan et al. 2025). Therefore, we are curious how do the improved mathemati- cal reasoning abilities transfer to broader capabilities. The results in Tab. 2 demonstrate that employing InTRO extends its benefits beyond pure mathematical tasks, significantly improving performance across a range of OOD tasks compared to GRPO. These results reveal a critical insight: InTRO minimizes token-level information discrepancy to strengthen causal links, enabling logic-driven OOD generalization, especially for coding tasks.

InTRO optimizes its reasoning trajectories to promote conciseness. Fig. 3 reports the average length of the rationales from different test sets, where “Hard” denotes challenging problems from Olympiad and AIME25.

35199

<!-- Page 6 -->

Non-math tasks LiveCodeBench BigCodeBench GPQA HumanEval IFEval Average

Qwen2.5-7B 7.2 23.7 36.0 78.7 44.4 38.0 GRPO 7.8 23.4 35.0 79.9 48.5 38.9 InTRO 11.4 23.3 36.5 81.1 49.8 40.4

Qwen3-4B 4.1 27.7 22.1 81.7 45.6 36.2 GRPO 6.2 27.8 21.9 83.5 40.6 36.0 InTRO 22.6 35.4 38.6 89.2 50.4 47.2

Qwen3-8B 16.0 31.0 36.0 86.6 53.2 44.6 GRPO 17.5 32.3 39.7 86.6 54.0 46.0 InTRO 22.4 35.2 40.6 86.0 54.9 47.8

**Table 2.** Performance of InTRO and GRPO on OOD tasks. Results illustrate that InTRO consistently demonstrates improved generalization capabilities compared to GRPO, particularly notable on coding benchmarks for stronger base models.

Training-phase variations in response length (Fig. 4) correlate with improved test accuracy on the “Hard” set (Fig. 5), revealing InTRO’s dual optimization for conciseness and accuracy. This pattern is supported by additional visualizations on training dynamics presented in Appendix B.2.

(a) “Hard” problems. (b) All problems.

**Figure 3.** Avg. response length on test questions. InTRO provides remarkably shorter rationales, especially on more challenging problems and stronger base models (Qwen3).

**Figure 4.** Generated response length during training (on training and test questions, respectively).

## 3.5 Ablations

Token-level exploration with different n values. We investigate with Qwen2.5-1.5B how varying the number of per-step sampled tokens n affects model performance.

(a) Qwen2.5-7B. (b) Qwen3-4B.

**Figure 5.** Test accuracy on “Hard” set during training.

## Sampled tokens 1 2 5 10 20 40

Avg. accuracy 20.1 24.4 24.9 25.6 25.0 23.8

**Table 3.** Effect of different n. Increasing n improves accuracy by enabling denser token-level exploration, with performance gains gradually saturating beyond a moderate n.

Specifically, larger n enables more aggressive token-level exploration in InTRO. As shown in Tab. 3, the accuracy generally improves as we increase n, suggesting that more extensive token-level exploration enhances reasoning capabilities. However, beyond a moderate threshold (e.g., n = 20), performance gains plateau then degrade, suggesting that an optimal range for n exists to maximize model effectiveness. We also provide the relationship between larger n and policy entropy in Appendix B.6 for further analysis.

How well does the answer-conditioned posterior improve reasoning and approximate the true posterior? To probe this problem, we ask the model to reason w/ and w/o the final answer, given any question. To exclude cases where the model simply copy-paste the final answer without giving a genuine rationale, we leverage an external verifier model (Qwen-2.5-70B-Instruct, prompt in Appendix B.3) to check whether the produced CoT was internally consistent with the answer. Fig. 6 shows that answer-conditioned reasoning (πθ(z|x⊕y)) boosts performance on hard sets such as AIME25 and Olympiad, but may slightly hurt on easier ones

35200

![Figure extracted from page 6](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

(a) Qwen2.5-1.5B. (b) Qwen3-8B.

**Figure 6.** Effect of answer-conditioned reasoning. Prompting w/ Answer greatly increases performance on more challenging benchmarks (AIME25 and Olympiad), but yields marginal gains or small drops on easier sets such as Math.

like Math. The interpretation is intuitive. When the policy faces a vast, high-entropy search space, conditioning on the answer prunes implausible branches and guides the model toward a valid path. For a sanity check, we also estimate the true posterior πθ(z|x, y) via Bayes’ theorem with N sampled reasoning paths in a toy setup. With sufficiently large N(1000 in our experiments), the sequence-level KL divergence between πθ(z|x, y) and πθ(z|x ⊕y) is around 2.3, indicating substantial consistency between the two policies.

Computational efficiency analysis. While InTRO does token-level exploration with n candidates at each step, it simply reweights pre-computed logits, adding virtually no extra cost. As a result, for each rationale, only two forward passes are required to compute the correction factors. In contrast, GRPO must proportionally increase the number of fully sampled trajectories G to stimulate exploration. This requires 2G forward passes to evaluate each rationale under both the new and old policies. Consequently, InTRO maintains significantly lower logit-compute overhead compared to GRPO, especially as the exploration density increases.

## 4 Related

Work 4.1 Improving the Reasoning Chains

CoT reasoning techniques have been shown to be effective in instructing modern LLMs to solve complex reasoning tasks. A large body of works fall into this category, such as prompting methods (Wei et al. 2022; Khot et al. 2022) and tuning-based methods (Yu et al. 2023; Hao et al. 2024; Cheng and Van Durme 2024; Wang, Yue, and Chen 2025). One line of work focuses on improving the correctness of the reasoning steps. For instance, GRACE (Khalifa et al. 2023) first learn a discriminator over correct and incorrect steps, then leverages it during decoding to score next-step candidates. CFT (Wang, Yue, and Chen 2025) improves traditional SFT by explicitly training models to critique noisy responses and verify correctness via maximizing the likelihood of the annotated critique. Another line of work explores latent reasoning in LLMs (Pfau, Merrill, and Bowman 2024; Deng et al. 2023; Deng, Choi, and Shieber 2024). Specifically, Coconut (Hao et al. 2024) directly feeds the last hidden state as the input embedding for the next token prediction and enables reasoning in continuous space, and CCoT (Cheng and Van Durme 2024) produces contemplation tokens for additional reasoning over dense representations. Another literature explores self-play (Zelikman et al. 2022; Qu et al. 2024; Kumar et al. 2024; Zelikman et al. 2024). TRICE (Hoffman et al. 2023) leverages Markovchain Monte Carlo expectation-maximization to maximize the marginal log-likelihood of generating a correct answer using CoT prompting, and LaTRO (Chen et al. 2024) formulates reasoning as sampling from a latent distribution and optimizes it via variational approaches, with RLOO employed to optimize the reasoner (Kool, van Hoof, and Welling 2019) Our work, while also trying to improve the rationale quality, lets the model’s own posterior serve as the teacher, supplying token-level feedback during training.

## 4.2 LLMs for Mathematical Reasoning

With the rapid development of the reasoning-centered LLMs, especially following the release of GPT-o1 (Jaech et al. 2024) and DeepSeek-R1 (Guo et al. 2025), the research focus has shifted to leveraging RL-based algorithms to boost reasoning capabilities. Specifically, GRPO (Shao et al. 2024) is a representative work that greatly simplifies the RL process by eliminating the value function in Proximal Policy Optimization (PPO) (Schulman et al. 2017). It leverages the behavior policy to sample a group of responses and calculate the advantage by normalizing the group-level rewards. GRPO has been shown to be really impressive and inspired subsequent works such as Dr.GRPO (Liu et al. 2025), DAPO (Yu et al. 2025), SEED-GRPO (Chen et al. 2025b), and EMPO (Zhang et al. 2025a). Rejection sampling fine-tuning, or RAFT (Dong et al. 2023), turns out to be a highly comparable alternative to complex RL algorithms (Xiong et al. 2025) by fine-tuning the models on the self-generated correct generations. Xiong et al. (2025) also proposes RAFT++, which is an improved RAFT with importance sampling and gradient clipping, and Reinforce- Rej, which is an RL variant that filters out both fully incorrect and correct samples. Similarly, GPG (Chu et al. 2025) directly optimizes the original RL objective, with a thresholding mechanism to avoid large variance in gradient estimation. The proposed InTRO sits at the intersection of these lines. It re-uses the model’s own generations, but attaches a soft, answer-conditioned weight to every explored token, providing a new avenue for accurate and concise reasoning.

## 5 Conclusion In this paper, we introduce

InTRO to enable accurate and concise reasoning by unifying token-level exploration with self-generated feedback, all without external guidance. In- TRO training is theoretically grounded as it is gradientequivalent to maximizing the intractable goal of optimal reasoning. The derived practical implementation involves an estimated posterior to compute correction factors in a single forward pass, ultimately encouraging accurate and concise rationales. Experiments on multiple mathematical and other reasoning tasks show that InTRO provides consistent improvement over other baselines to a great margin.

35201

![Figure extracted from page 7](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-in-token-rationality-optimization-towards-accurate-and-concise-llm-reasoning-via/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This research is supported by Artificial Intelligence- National Science and Technology Major Project 2023ZD0121200.

## References

Chen, H.; Feng, Y.; Liu, Z.; Yao, W.; Prabhakar, A.; Heinecke, S.; Ho, R.; Mui, P.; Savarese, S.; Xiong, C.; et al. 2024. Language models are hidden reasoners: Unlocking latent reasoning capabilities via self-rewarding. arXiv preprint arXiv:2411.04282. Chen, H.; Tu, H.; Wang, F.; Liu, H.; Tang, X.; Du, X.; Zhou, Y.; and Xie, C. 2025a. Sft or rl? an early investigation into training r1-like reasoning large vision-language models. arXiv preprint arXiv:2504.11468. Chen, M.; Chen, G.; Wang, W.; and Yang, Y. 2025b. Seed-grpo: Semantic entropy enhanced grpo for uncertainty-aware policy optimization. arXiv preprint arXiv:2505.12346. Cheng, J.; and Van Durme, B. 2024. Compressed chain of thought: Efficient reasoning through dense representations. arXiv preprint arXiv:2412.13171. Chowdhury, J. R.; and Caragea, C. 2025. Zero-Shot Verification-guided Chain of Thoughts. arXiv preprint arXiv:2501.13122. Chu, X.; Huang, H.; Zhang, X.; Wei, F.; and Wang, Y. 2025. Gpg: A simple and strong reinforcement learning baseline for model reasoning. arXiv preprint arXiv:2504.02546. Deng, Y.; Choi, Y.; and Shieber, S. 2024. From explicit cot to implicit cot: Learning to internalize cot step by step. arXiv preprint arXiv:2405.14838. Deng, Y.; Prasad, K.; Fernandez, R.; Smolensky, P.; Chaudhary, V.; and Shieber, S. 2023. Implicit chain of thought reasoning via knowledge distillation. arXiv preprint arXiv:2311.01460. Dong, H.; Xiong, W.; Goyal, D.; Zhang, Y.; Chow, W.; Pan, R.; Diao, S.; Zhang, J.; Shum, K.; and Zhang, T. 2023. Raft: Reward ranked finetuning for generative foundation model alignment. arXiv preprint arXiv:2304.06767. Gao, J.; Lin, R.; Lu, K.; Yu, B.; Lin, J.; and Chen, J. 2025. MARGE: Improving Math Reasoning for LLMs with Guided Exploration. arXiv:2505.12500. Guo, D.; Yang, D.; Zhang, H.; Song, J.; Zhang, R.; Xu, R.; Zhu, Q.; Ma, S.; Wang, P.; Bi, X.; et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948. Hao, S.; Sukhbaatar, S.; Su, D.; Li, X.; Hu, Z.; Weston, J.; and Tian, Y. 2024. Training large language models to reason in a continuous latent space. arXiv preprint arXiv:2412.06769. Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart, S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measuring Mathematical Problem Solving With the MATH Dataset. NeurIPS.

Hoffman, M. D.; Phan, D.; Dohan, D.; Douglas, S.; Le, T. A.; Parisi, A.; Sountsov, P.; Sutton, C.; Vikram, S.; and Saurous, R. A. 2023. Training chain-of-thought via latentvariable inference. In NeurIPS. Hu, J.; Wu, X.; Zhu, Z.; Xianyu; Wang, W.; Zhang, D.; and Cao, Y. 2024. OpenRLHF: An Easy-to-use, Scalable and High-performance RLHF Framework. arXiv preprint arXiv:2405.11143. Huan, M.; Li, Y.; Zheng, T.; Xu, X.; Kim, S.; Du, M.; Poovendran, R.; Neubig, G.; and Yue, X. 2025. Does Math Reasoning Improve General LLM Capabilities? Understanding Transferability of LLM Reasoning. arXiv preprint arXiv:2507.00432. Jaech, A.; Kalai, A.; Lerer, A.; Richardson, A.; El-Kishky, A.; Low, A.; Helyar, A.; Madry, A.; Beutel, A.; Carney, A.; et al. 2024. Openai o1 system card. arXiv preprint arXiv:2412.16720. Khalifa, M.; Logeswaran, L.; Lee, M.; Lee, H.; and Wang, L. 2023. Grace: Discriminator-guided chain-of-thought reasoning. arXiv preprint arXiv:2305.14934. Khot, T.; Trivedi, H.; Finlayson, M.; Fu, Y.; Richardson, K.; Clark, P.; and Sabharwal, A. 2022. Decomposed prompting: A modular approach for solving complex tasks. arXiv preprint arXiv:2210.02406. Kool, W.; van Hoof, H.; and Welling, M. 2019. Buy 4 reinforce samples, get a baseline for free! Kumar, A.; Zhuang, V.; Agarwal, R.; Su, Y.; Co-Reyes, J. D.; Singh, A.; Baumli, K.; Iqbal, S.; Bishop, C.; Roelofs, R.; et al. 2024. Training language models to self-correct via reinforcement learning. arXiv preprint arXiv:2409.12917. Li, Y.; Lin, Z.; Zhang, S.; Fu, Q.; Chen, B.; Lou, J.-G.; and Chen, W. 2023. Making language models better reasoners with step-aware verifier. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 5315–5333. Liu, Z.; Chen, C.; Li, W.; Qi, P.; Pang, T.; Du, C.; Lee, W. S.; and Lin, M. 2025. Understanding r1-zero-like training: A critical perspective. arXiv preprint arXiv:2503.20783. Ni, A.; Inala, J. P.; Wang, C.; Polozov, O.; Meek, C.; Radev, D.; and Gao, J. 2022. Learning math reasoning from self-sampled correct and partially-correct solutions. arXiv preprint arXiv:2205.14318. Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.; et al. 2022. Training language models to follow instructions with human feedback. Advances in neural information processing systems, 35: 27730–27744. Pfau, J.; Merrill, W.; and Bowman, S. R. 2024. Let’s think dot by dot: Hidden computation in transformer language models. arXiv preprint arXiv:2404.15758. Qu, Y.; Zhang, T.; Garg, N.; and Kumar, A. 2024. Recursive introspection: Teaching language model agents how to self-improve. Advances in Neural Information Processing Systems, 37: 55249–55285. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.

35202

<!-- Page 9 -->

Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.; Zhang, H.; Zhang, M.; Li, Y.; Wu, Y.; et al. 2024. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and Yao, S. 2023. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36: 8634–8652. Team, K.; Du, A.; Gao, B.; Xing, B.; Jiang, C.; Chen, C.; Li, C.; Xiao, C.; Du, C.; Liao, C.; et al. 2025. Kimi k1. 5: Scaling reinforcement learning with llms. arXiv preprint arXiv:2501.12599. Wang, P.; Li, L.; Shao, Z.; Xu, R.; Dai, D.; Li, Y.; Chen, D.; Wu, Y.; and Sui, Z. 2023. Math-shepherd: Verify and reinforce llms step-by-step without human annotations. arXiv preprint arXiv:2312.08935. Wang, S.; Yu, L.; Gao, C.; Zheng, C.; Liu, S.; Lu, R.; Dang, K.; Chen, X.; Yang, J.; Zhang, Z.; et al. 2025. Beyond the 80/20 rule: High-entropy minority tokens drive effective reinforcement learning for llm reasoning. arXiv preprint arXiv:2506.01939. Wang, Y.; Yue, X.; and Chen, W. 2025. Critique fine-tuning: Learning to critique is more effective than learning to imitate. arXiv preprint arXiv:2501.17703. Wei, J.; Bosma, M.; Zhao, V. Y.; Guu, K.; Yu, A. W.; Lester, B.; Du, N.; Dai, A. M.; and Le, Q. V. 2021. Finetuned language models are zero-shot learners. arXiv preprint arXiv:2109.01652. Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-ofthought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35: 24824–24837. Weng, Y.; Zhu, M.; Xia, F.; Li, B.; He, S.; Liu, S.; Sun, B.; Liu, K.; and Zhao, J. 2022. Large language models are better reasoners with self-verification. arXiv preprint arXiv:2212.09561. Xie, Y.; Goyal, A.; Zheng, W.; Kan, M.-Y.; Lillicrap, T. P.; Kawaguchi, K.; and Shieh, M. 2024. Monte Carlo Tree Search Boosts Reasoning via Iterative Preference Learning. arXiv:2405.00451. Xiong, W.; Yao, J.; Xu, Y.; Pang, B.; Wang, L.; Sahoo, D.; Li, J.; Jiang, N.; Zhang, T.; Xiong, C.; et al. 2025. A minimalist approach to llm reasoning: from rejection sampling to reinforce. arXiv preprint arXiv:2504.11343. Yan, J.; Li, Y.; Hu, Z.; Wang, Z.; Cui, G.; Qu, X.; Cheng, Y.; and Zhang, Y. 2025. Learning to reason under off-policy guidance. arXiv preprint arXiv:2504.14945. Yu, L.; Jiang, W.; Shi, H.; Yu, J.; Liu, Z.; Zhang, Y.; Kwok, J. T.; Li, Z.; Weller, A.; and Liu, W. 2023. Metamath: Bootstrap your own mathematical questions for large language models. arXiv preprint arXiv:2309.12284. Yu, Q.; Zhang, Z.; Zhu, R.; Yuan, Y.; Zuo, X.; Yue, Y.; Dai, W.; Fan, T.; Liu, G.; Liu, L.; et al. 2025. Dapo: An opensource llm reinforcement learning system at scale. arXiv preprint arXiv:2503.14476.

Zelikman, E.; Harik, G.; Shao, Y.; Jayasiri, V.; Haber, N.; and Goodman, N. D. 2024. Quiet-star: Language models can teach themselves to think before speaking. arXiv preprint arXiv:2403.09629. Zelikman, E.; Wu, Y.; Mu, J.; and Goodman, N. 2022. Star: Bootstrapping reasoning with reasoning. Advances in Neural Information Processing Systems, 35: 15476–15488. Zhang, Q.; Wu, H.; Zhang, C.; Zhao, P.; and Bian, Y. 2025a. Right question is already half the answer: Fully unsupervised llm reasoning incentivization. arXiv preprint arXiv:2504.05812. Zhang, Z.; Zheng, C.; Wu, Y.; Zhang, B.; Lin, R.; Yu, B.; Liu, D.; Zhou, J.; and Lin, J. 2025b. The lessons of developing process reward models in mathematical reasoning. arXiv preprint arXiv:2501.07301.

35203
