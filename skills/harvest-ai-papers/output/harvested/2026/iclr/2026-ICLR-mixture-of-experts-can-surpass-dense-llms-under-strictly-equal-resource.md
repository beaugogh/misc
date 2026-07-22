---
title: "Mixture-of-Experts Can Surpass Dense LLMs Under Strictly Equal Resource"
source_url: https://iclr.cc/virtual/2026/oral/10007429
paper_pdf_url: https://arxiv.org/pdf/2506.12119v2
venue: ICLR
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Mixture-of-Experts Can Surpass Dense LLMs Under Strictly Equal Resource

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

MIXTURE-OF-EXPERTS CAN SURPASS DENSE LLMS UNDER STRICTLY EQUAL RESOURCE

Houyi Li1,2 hyli22@m.fudan.edu.cn

Ka Man Lo2 kamanphoebe@gmail.com

Shijie Xuyang1 ysjxu24@m.fudan.edu.cn

Ziqi Wang3 wzq142857@mail.ustc.edu.cn

Wenzhen Zheng2 zhengwenzhen@amss.ac.cn

Haocheng Zhang1 hczhang25@m.fudan.edu.cn

Zhao Li4 lzjoey@gmail.com

Shuigeng Zhou1∗ sgzhou@fudan.edu.cn

Xiangyu Zhang2 robert.zhang@stepfun.com

Daxin Jiang2 djiang@stepfun.com

1Fudan University 2StepFun 3University of Science and Technology of China 4Zhejiang University

## ABSTRACT

Mixture-of-Experts (MoE) language models dramatically expand model capacity and achieve remarkable performance without increasing per-token compute. However, can MoEs surpass dense architectures under strictly equal resource constraints — that is, when the total parameter count, training compute, and data budget are identical? This question remains under-explored despite its signiﬁcant practical value and potential. In this paper, we propose a novel perspective and methodological framework to study this question thoroughly. First, we comprehensively investigate the architecture of MoEs and achieve an optimal model design that maximizes the performance. Based on this, we subsequently ﬁnd that an MoE model with activation rate in an optimal region is able to outperform its dense counterpart under the same total parameter, training compute and data resource. More importantly, this optimal region remains consistent across different model sizes. Although additional amount of data turns out to be a trade-off for enhanced performance, we show that this can be resolved via reusing data. We validate our ﬁndings through extensive experiments, training nearly 200 language models at 2B scale and over 50 at 7B scale, cumulatively processing 50 trillion tokens. All model checkpoints are publicly available†.

## INTRODUCTION

In recent years, Large Language Models (LLMs) built on the Transformer architecture (Vaswani et al., 2017) have achieved strong results on a range of NLP tasks (Radford et al., 2018; Achiam et al., 2023; Touvron et al., 2023a;b; Bai et al., 2023). Meanwhile, there has been growing interest in using Mixture-of-Experts (MoE) layers (Shazeer et al., 2017) to expand model capacity while keeping the training cost reasonable (Fedus et al., 2022; Zoph et al., 2022; Rajbhandari et al., 2022). Recent opensource initiatives have explored MoE-based LLMs (Dai et al., 2024; Jiang et al., 2024; Wei et al., 2024; Xue et al., 2024; DeepSeek-AI et al., 2024b), yet many widely adopted open-source models

∗Corresponding author. † https://huggingface.co/kamanphoebe/moe_surpass_dense.

arXiv:2506.12119v2 [cs.CL] 17 May 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026 such as LLaMA (Touvron et al., 2023a;b), DeepSeek’s ﬁrst-generation models (DeepSeek-AI et al., 2024a), and Qwen (Yang et al., 2024; Qwen et al., 2024), continue to utilize dense architectures, posing an open question of whether MoE LLMs can outperform their dense counterparts.

Current comparisons of MoE and dense LLMs often simplify the analysis to either a data-centric or a compute-centric perspective. The data-centric view, which keeps total training tokens constant for both MoE and dense models, praises MoE for its reduced activated parameter count per token (i.e., per-token compute cost) and potential for aggressive parameter scaling. For example, DeepSeek- MoE (Dai et al., 2024) reports a 16B-parameter MoE model (with 2.5B activated parameters) that achieves performance on par with a 7B dense model under the same data budget, thus suggesting a 2.5× “parameter-efﬁciency” advantage. The compute-centric view, which ﬁxes total training compute, examines the impact of MoE sparsity (i.e., the ratio of activated to total parameters) on performance. Under certain sparse conﬁgurations, total parameters can swell to nearly 100× those of a dense baseline, but at the cost of requiring more training data and managing high memory overhead.

However, neither perspectives fully addresses the complex interplay of critical resource constraints in large-scale model development: the ﬁnite nature of training data volume (D), training compute (C), and model size (N), which affects both memory and inference throughput. In particular, MoE models typically encounter bandwidth bottlenecks during inference, as all experts reside in GPU high-bandwidth memory and must be moved into shared memory, making parameter count a key runtime cost factor beyond FLOPs. These interdependencies complicate the conclusion of the absolute superiority of MoE or dense architectures. Intuitively, a dense model with equivalent total parameters should have an advantage by fully utilizing its capacity. This often leads studies to favor MoE for scaling model size rather than direct comparisons at the same parameter count, thus overlooking the real-world resource constraints in large-scale training and deployment.

In this work, we introduce a novel perspective aimed at providing a more convincing resolution to this debate by posing the following question:

Can Mixture-of-Experts surpass dense LLMs under equal total parameter, compute, and data constraints?

To reach a deﬁnitive conclusion on this issue, we draw insights from a uniﬁed parameterization framework for model architecture (§ 3) and propose a three-step experimental methodology. First, we search for an optimized architecture design to ensure each model candidate achieves its (near-) optimal performance (§ 4). Second, we explore the optimal activation rate based on this optimized model architecture, with the total parameters N and compute budget C ﬁxed (§ 5). Third, we present a data reuse strategy to address the additional data demand of MoE models, thereby equating data resource D (§ 6). We also analyze the efﬁcacy of this framework on downstream tasks (§ 7).

Our ﬁndings, derived from extensive experiments and systematic evaluation under the proposed strict N/C/D parity with dense models, provide strong evidence that MoE architectures with optimized backbones and activation rates can indeed achieve superior performance over dense models on both upstream and downstream tasks. This implies that any observed performance gains can be attributed solely to architectural advantages, rather than disparities in parameter count or compute budget. Moreover, this challenges conventional wisdom and paves the way for resource-efﬁcient yet powerful architectures in the next generation of large-scale NLP systems.

Our main contributions are: 1) We demonstrate, for the ﬁrst time, that under ﬁxed total parameters (N) and a ﬁxed compute budget (C), an MoE LLM can surpass its dense counterpart with careful architecture design (see Fig. 1b, 2b). 2) Our experiments reveal the existence of a stable “optimal AR” region that consistently maximizes performance across varying N (see Fig. 1, 2). 3) We introduce a practical data reuse strategy that offsets MoE’s additional data needs, enabling robust gains over dense models without substantially increasing unique training data D (see Fig. 2, 3).

## RELATED WORK

## 2.1 MOE LANGUAGE MODELS

Building upon MoE (Shazeer et al., 2017), GShard (Lepikhin et al., 2021) facilitates model parallelism across devices for massive MoE models. With the advent of Transformers (Vaswani et al.,

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

2017), the integration of MoE into the Transformer framework has become a popular model architecture and achieved state-of-the-art performance. As an early attempt, Switch Transformer (Fedus et al., 2022) proposes top-1 gating to simplify MoE architecture and alleviate communication overhead. More recent Transformer-based MoE LLMs include (Xue et al., 2024; Jiang et al., 2024; Wu et al., 2024; Wei et al., 2024; DeepSeek-AI et al., 2024b). The MoE architecture is brieﬂy reviewed in Appendix A.

## 2.2 ANALYSES OF MOE SPARSITY

Several studies investigated the impact of varying the number of MoE experts and adjusting granularity, both of which are factors related to sparsity. Through ablation studies, DeepSeekMoE (Dai et al., 2024) observes ﬁner granularity results in improvement on overall model performance, and acquires a ratio between shared and routed experts that yields slightly better Pile loss. Zoph et al. (2022) summarized the results of several MoE works and indicated that the gain of increasing sparsity quickly diminishes when the number of experts is greater than 256 — a very sparse model.

**Table 1.** Notation.

Symbol Deﬁnition D Dataset size in tokens. M Compute (w/o embedding) per token in FLOPs. C Total training compute in FLOPs, i.e., M · D. N Number of non-vocabulary parameters. Na Number of activated parameters. ra Activation rate, i.e., Na/N. Le Number of MoE layers. Ld Number of dense layers. L Number of total layers, i.e., Le + Ld. α FFN expansion ratio, i.e., Dffn/Dm. ζ Model aspect ratio, i.e., Dm/L. γ Sequence-to-width ratio, i.e., S/Dm.

Symbol Deﬁnition S Sequence length. H Number of attention heads. Dm Model hidden dimension. Dffn FFN hidden dimension. Dh Dimension of attention head. De Expert hidden dimension. Dse Shared expert hidden dimension. E Number of experts. K Number of chosen experts. β Activated FFN-to-model ratio in MoE layers, i.e., (Dse + KDe)/Dm. µ Total FFN-to-model ratio in MoE layers, i.e., (Dse + EDe)/Dm.

From a methodological perspective, our comparisons are conducted in a sufﬁciently trained regime (with D/N ≥20 for key models) and under a ﬁxed-N setting motivated by deployment memory constraints, which differs from scaling-law sweeps that often rely on undertrained large models at limited compute. We provide a more detailed discussion in Appendix B.

Concurrently with our work, Ludziejewski et al. (2025) found that a sufﬁciently large MoEs trained with more tokens outperforms a dense model with the same total parameters. We further show MoE superiority even at smaller sizes and address the additional data demand via reuse. Abnar et al. (2025) studied the scaling law for optimal MoE sparsity. However, their models (up to N = 30B) were trained with C = 1e20, a much smaller budget compared to the approximately 9× and 30× compute we used for our 2B and 7B models to ensure an adequate D/N. This likely resulted in undertrained models, potentially affecting their conclusions. Moreover, our study ﬁrst optimizes the MoE architecture to isolate the effect of different activation rates on performance. Detailed differences between our work and this previous study are discussed in Appendix B.

EXPERIMENTAL METHODOLOGY

We begin by introducing a uniﬁed parameterization framework for model architecture, establishing a solid foundation. Then, we derive key insights from this parameterization, which informs our comprehensive three-step experimental methodology. Finally, we detail the experimental setup used consistently across all subsequent experiments. Our notation is summarized in Table 1.

<!-- Page 4 -->

Published as a conference paper at ICLR 2026

## 3.1 ARCHITECTURE PARAMETERIZATION

To enable a comprehensive and general comparison of dense and MoE-based LLM architectures under realistic deployment constraints, we introduce a uniﬁed parameterization framework that explicitly accounts for both model parameters and per-token compute cost.

Dense model parameterization. For a dense model, we approximate the number of nonembedding parameters N and the per-token forward-pass computation cost M as follows:

N ≈(4 + 3α)D2 mL = (4 + 3α)ζ2L3, (1)

M ≈2N + 4DmSL = 2N + 4ζ2γL3 (2) = 2N(1 + 2γ/(4 + 3α)), (3) where α = Dffn/Dm, γ = S/Dm, and ζ = Dm/L. Here, we omit the LayerNorm parameter count as it is negligible. Inference cost or training cost can be approximated by C ≈M × D or C ≈3M × D, respectively (based on the standard empirical observation that training typically takes about three times the forward pass for backward computation).

MoE model parameterization. In many real-world settings, only a subset of Transformer layers are replaced with MoE layers. The approximations for total non-vocabulary parameters N, activated parameters Na, and per-token computation cost M can be expressed as

N ≈(4 + 3µ)D2 mLe + (4 + 3α)D2 mLd, (4)

Na ≈(4 + 3β)D2 mLe + (4 + 3α)D2 mLd, (5)

M ≈Na + 4DmSL = 2raN + 4ζ2γL3, (6) where µ = (Dse + EDe)/Dm and β = (Dse + KDe)/Dm. We again omit the parameters and FLOPs of the gating network (router) as they are comparatively small, and the activation rate (AR) is denoted as ra. For the simple and common case where all L layers are MoE layers (i.e., Ld = 0), we have ra = Na/N = (4 + 3β)/(4 + 3µ), (7)

M ≈2raN + 4ζ2γL3 (8) = 2raN(1 + 2γ/(4 + 3β)). (9)

## 3.2 KEY OBSERVATIONS AND METHODOLOGICAL CONSIDERATIONS

Based on the above parameterization, we highlight the following insights that guide our experiments:

High structural degrees of freedom in MoE. Compared to a dense model (whose shape is almost uniquely determined by L, Dm, and α), an MoE model has many more design choices: the number of MoE layers (Le), expert-related dimensions (e.g., K, E, De, Dse), and so forth. Even with Ld = 0, the ﬁnal shape depends on µ and β in addition to ζ and ra. Exhaustively searching all combinations is prohibitively expensive. Therefore, a greedy strategy should be adopted.

Activation rate ra is the primary factor. At the same total parameter count N, the ratio of pertoken FLOPs between an MoE model and a dense model is primarily determined by the activation rate ra. More speciﬁcally, if Md is the per-token cost of the dense baseline (with ζ, α ﬁxed), then the pure MoE model’s compute, normalized by Md, roughly behaves as (the union of Equ. 3 and 9):

Rc = ra(4 + 3α + 2γd

4 + 3β + 2γm) (10)

where γd and γm denote S/Dm for dense and MoE layers, respectively. As γ strongly correlates with ζ, once the shape hyperparameters (ζ, α, β) are chosen, Rc grows monotonically with ra.

The trade-off among N, C, and D. Once N (the total parameters) is chosen and we ﬁx nearoptimal shapes for dense and MoE models, the total training compute for the MoE model can be approximated by C = 3 Rc Md D, where Md is the per-token cost of the dense baseline with the same total parameter count, and Rc is the fraction by which the MoE model reduces compute per token (relative to the dense baseline). If we want to keep the same total compute C for both MoE and dense models, the MoE model will need Rc times more training tokens.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

## 3.3 THREE-STEP EXPERIMENTAL METHODOLOGY

Motivated by the aforementioned observations, we propose a three-step experimental methodology which is both comprehensive and fair, so as to achieve the new perspective motivated in § 1 that enables a more conclusive comparison of MoE and dense LLMs under equal resource constraints. The methodology is outlined as follows: 1) Greedy architecture determination. First, determine the macro-level layer composition (i.e., the MoE-to-dense layer ratio Le vs. Ld and related choices such as shared experts). Second, determine the micro-level MoE design within each MoE layer (e.g., top-K routing and parameter allocation among routed/shared experts), which is largely orthogonal to the global model shape. Finally, select the near-optimal shape hyperparameters (e.g., ζ, α for dense and ζ, β for MoE) for fair comparisons at a ﬁxed N. 2) Activation rate analysis under ﬁxed N and C. With the optimal MoE architecture chosen in the previous step, and the optimal dense LLM shape proposed by Kaplan et al. (2020), we compare MoE models versus a dense baseline of the same size, ensuring the total training compute C is matched. Since C must be the same, the MoE model typically receives up to Rc times more tokens (initially considering repeated or augmented data). 3) Data reuse strategy. To ensure a truly fair comparison at the same unique data budget D, we develop a data reuse strategy that offsets MoE’s additional data requirement. This enables evaluation under strictly equal N, C, and D.

## 3.4 COMMON EXPERIMENTAL SETUP

Optimal hyperparameters. MoE training is sensitive to the learning rate (η) and batch size (B) (He et al., 2024). Even minor architectural changes, such as variations in E, can lead to different optimal hyperparameters. To address this, we train all our models using the optimal η and B based on the hyperparameter scaling laws proposed in (Li et al., 2025). Speciﬁcally, Li et al. (2025) found that the optimal η and B follow power laws and depend only on N and D. Since these scaling laws are applicable to both dense and MoE models and are robust across various pretraining data distributions, we apply them to determining η and B for each of our experiments.

Dense baseline tuning. To ensure a strictly fair comparison, we also tuned the dense baselines by searching for near-optimal structural ratios (e.g., aspect ratio ζ and FFN expansion α, equivalently L, Dm, Dffn with given N), guided by the scaling-law recommendations in Li et al. (2025); the resulting dense conﬁgurations used throughout the paper are summarized in Table 13.

Others. We use internal, high-quality training and validation datasets composed primarily of diverse web text and speciﬁc domains such as mathematics and code. The training and validation sets have different distributions, requiring the evaluated models to demonstrate strong generalization capabilities. Our models incorporate RMSNorm (Zhang & Sennrich, 2019) for pre-normalization, ALiBi (Press et al., 2022) positional encoding for multi-head attention, and the SwiGLU (Shazeer, 2020) activation function for both feed-forward networks (FFNs) and MoE experts. The training procedures used consistently across all experiments are outlined in Table 4 in Appendix E. We employ cross-entropy loss (L) as the training metric and bits-per-character (BPC) as the validation metric.

## 4 OPTIMIZED MOE ARCHITECTURE

Building on the insights discussed above, we systematically examine the following model components in the order outlined below: 1) Distribution of MoE and dense layers. 2) Gate score normalization. 3) Parameter allocation within MoE. 4) Exploration of optimal structural hyperparameters. Each component incorporates previous conclusions into its experimental settings.

MoE and dense layers arrangement. This part examines how to arrange the distribution between MoE and dense layers. We consider three layer arrangement schemes: every layer is an MoE layer (full), one dense layer followed by MoE layers (1dense), and interleaved MoE and dense layers (interleave). We additionally include shared experts (SE) for some of our experiments.

**Table 5.** in Appendix E presents the experimental settings and results. The conclusions are as follows: 1) 1dense+SE performs the best, possibly because the dense layer contributes to more stable training. 2) The ratio of shared expert size to total expert size Dse/(Dse + KDe) has minimal

<!-- Page 6 -->

Published as a conference paper at ICLR 2026

2 × 1020 3 × 1020 4 × 1020 6 × 1020

Total Compute C

4.9 × 10 1

4.95 × 10 1

5 × 10 1

5.05 × 10 1

5.1 × 10 1

5.15 × 10 1

5.2 × 10 1

5.25 × 10 1

BPC

2B MoE series, D=114B ra: 8.7% ~ 58% 2B MoE, ra=8.7%

2B MoE, ra=10.8% 2B MoE, ra=19% 2B MoE, ra=35%

2B MoE, ra=51%

Data ~tokens

114B 128B 147B 180B 223B 309B 468B 541B

(a) Fixed D (solid) or ra (dashed)

0.1 0.2 0.3 0.4 0.5 0.6 Activation rate ra

0.475

0.480

0.485

0.490

0.495

0.500

0.505

0.510

BPC

2B MoEs, 9.1e20 FLOPs 2B Dense, 9.1e20 FLOPs, D = 65B 2B Dense, 1.6e21 FLOPs, D = 114B

Data ~tokens

541B 468B 309B 223B 180B 147B 128B 114B

Data ~tokens

541B 468B 309B 223B 180B 147B 128B 114B

(b) Fixed C

**Figure 1.** Performance of N ≈2B models trained with varying data sizes D and activation rates ra. (a) With a ﬁxed D, performance gain exhibits a non-linear dependence on training budget C. Conversely, with a ﬁxed ra, increasing D leads to a linear performance gain. These ﬁndings indicate an optimal activation rate, r∗∗

a = 20%, that is consistent across various D values when N is constant. (b) With a ﬁxed training compute C, the optimal activation rate r∗∗ a = 20% can be clearly seen.

impact on model performance. Therefore, we continue using the 1dense+SE conﬁguration and set Dse = KDe.

Gate score normalization. The results of normalizing gate scores of chosen experts are in Table 6 in Appendix E. Although the addition of normalization does not show an obvious difference in performance loss, it tends to reduce the average balance loss ¯Lbalance. Since normalization requires K > 1 to avoid zero gradient, we opt not to normalize given that some of our experiments have K=1.

Top-K setting. In this part, we discuss the allocation of parameters within MoE layers, focusing on the top-K setting. Expert granularity is adjusted by varying K and De while keeping their product constant. We conduct three groups of experiments with various ra and the results are given in Table 7 in Appendix E. Note that within each experiment group, the product K ·De is not strictly maintained due to compatibility with other hyperparameters. We observe that both overly large K and the K=1 setting are generally suboptimal across the three groups. Therefore, we avoid using large K and avoid setting K=1 in our main experiments whenever possible.

## Model

shape ratios. As discussed in § 3.2, the shape hyperparameters include three ratios: ζ, α, and β. We set α = 2.77 (Touvron et al., 2023b) and explore the optimal ζ and µ, from which β can be derived. As illustrated in Fig. 4 in Appendix E, although performance ﬂuctuates wildly given a value of ζ or µ, there is an overall upward trend with increasing Dm for ζ and a downward trend for µ. Following the observed trend, we set ζ ≈88 and µ ≈22 for the subsequent experiments.

## 5 OPTIMAL ACTIVATION RATE

In this section, we analyze how the performance of MoE LLMs varies with different activation rates (AR) using model backbones optimized based on the conclusions in § 4, and examine whether MoE models can outperform dense models. Note that a concurrent study (Abnar et al., 2025) suggests that the optimal sparsity of MoE depends on model capacity. However, our ﬁndings indicate that, with optimized backbones, the optimal AR remains consistent across models of different sizes. We ﬁrst detail our experimental setup and results, followed by a further discussion on the conclusions.

Setup. We built a series of MoE models with non-vocabulary parameters N ≈2B and N ≈7B, but varying activation rates ra from 8.7% to 58%. Noteworthy, the model backbones were built upon the ﬁndings in § 4, as detailed in Table 9, 10, 11 and 12 in Appendix E. Each model was trained on a proportional subset of our dataset, ensuring D/N ≥20 (Hoffmann et al., 2022) for sufﬁcient training.

<!-- Page 7 -->

Published as a conference paper at ICLR 2026

2 × 1021 3 × 1021

Total Compute C

4.66 × 10 1

4.68 × 10 1

4.7 × 10 1

4.72 × 10 1

4.74 × 10 1

4.76 × 10 1

4.78 × 10 1

4.8 × 10 1

BPC

7B MoE series, D=130B ra: 8.9% ~ 53% 7B MoE series, D=130B ra: 8.9% ~ 53%

(a) Fixed D

0.1 0.2 0.3 0.4 0.5 Activation rate ra

0.454

0.456

0.458

0.460

0.462

0.464

0.466

0.468

BPC

7B MoEs, 2.8e21 FLOPs, unique data

7B MoEs, 2.8e21 FLOPs, D = 68B

7B MoEs, 2.8e21 FLOPs, D = 0.5 * D 7B Dense, 5.4e21 FLOPs, D = 130B

Data ~tokens

608B 513B 444B 389B 250B 220B 130B

Data ~tokens

608B 513B 444B 389B 250B 220B 130B

(b) Fixed C and reusing data

**Figure 2.** Performance of N ≈7B models trained with varying data sizes D and activation rate ra. The optimal activation rate, r∗∗

a = 20%, align with the ﬁndings for the 2B models (Figure 1). Additionally, compared to training on the unique dataset, the strict data reuse scheme shows only a slight performance reduction, while the loose scheme often yields better performance.

## 5.1 OPTIMAL AR POINT

Focusing on the 2B models trained on the same data size D = 114B as shown by the green solid line in Figure 1a, we observe that the performance gain depends non-linearly on the training budget C. Speciﬁcally, the gain is more signiﬁcant within a relatively low range of ra. Starting from points on this curve and ﬁxing the corresponding ra values, increasing D results in linearly diminishing BPC, as indicated by the dashed lines in Figure 1a. These results conﬁrm the existence of an optimal AR point, r∗∗ a, that remains consistent regardless of D when N is unchanged. When plotting the results from a ﬁxed training compute perspective (C = C0 = 9.1e20) in Figure 1b, we clearly observe that the optimal AR point is approximately r∗∗ a ≈20%.

## 5.2 COMPARISON WITH DENSE MODELS

To compare with dense models, we trained two dense models (Table 13 in Appendix E) with N ≈2B parameters and training budgets C1 = C0 = 9.1e20 and C2 = 1.64e21 ≈2C1. The second model (C2) is included for comparison to account for the typically lower Model FLOPs Utilization (MFU) in MoE training. This reduced MFU arises from load balancing and expert parallelism mechanisms that limit large-block matrix computations. As illustrated in Figure 1b, MoE models outperform their C1 dense counterparts when ra falls within a speciﬁc range (approximately 15% to 48% for 2B models). For instance, the MoE model with the optimal AR point r∗∗ a = 20% achieves a BPC value that is 0.0064 lower than its C1 dense counterpart and only 0.0049 higher than the C2 dense model. This demonstrates the existence of an optimal activation rate region R∗ a, where MoE models with ra ∈R∗ a can outperform their dense counterparts under the same training budget C and approach the performance of dense models with double the compute. However, the performance gains of MoE models rely on a substantial increase in data, e.g., a 4.6× larger data size at ra = r∗∗ a = 20%. To mitigate this additional data requirement, we explore a data reuse strategy in § 6.

## 5.3 CONSISTENCY OF OPTIMAL AR

As illustrated in Fig. 2, an optimal AR point r∗∗ a also exists for 7B models. Surprisingly, r∗∗ a remains consistent for both 2B and 7B models at approximately 20%, suggesting that r∗∗ a is independent of model size. This ﬁnding contradicts established studies on MoE sparsity (Abnar et al., 2025), which proposes that optimal sparsity (deﬁned as (E −K)/E) is directly proportional to model size. Nevertheless, our experiments were conducted with strictly controlled variables using optimized backbones, leading us to believe that our conclusions are both reliable and scalable (see Appendix B

<!-- Page 8 -->

Published as a conference paper at ICLR 2026

0.15 0.20 0.25 0.30 Activation rate ra

0.46

0.47

0.48

0.49

Accuracy

Average

0.15 0.20 0.25 0.30 Activation rate ra

0.570

0.575

0.580

0.585

0.590

0.595

0.600

Knowledge

0.15 0.20 0.25 0.30 Activation rate ra

0.43

0.44

0.45

0.46

Reasoning

Data ~tokens

511B 443B 390B 316B 250B 221B

Data ~tokens

511B 443B 390B 316B 250B 221B

0.15 0.20 0.25 0.30 Activation rate ra

0.16

0.17

0.18

0.19

0.20

0.21

0.22

0.23

Accuracy

Average

0.15 0.20 0.25 0.30 Activation rate ra

0.22

0.24

0.26

0.28

Knowledge

0.15 0.20 0.25 0.30 Activation rate ra

0.175

0.200

0.225

0.250

0.275

0.300

## 0.325 Reasoning

0.15 0.20 0.25 0.30 Activation rate ra

0.36

0.38

0.40

0.42

0.44

Accuracy

Comprehensive

0.15 0.20 0.25 0.30 Activation rate ra

0.08

0.10

0.12

0.14

## 0.16 Math

0.15 0.20 0.25 0.30 Activation rate ra

0.060

0.065

0.070

0.075

0.080

0.085

## 0.090 Code

7B MoEs unique data 7B MoEs strict data reuse D = 68B 7B Dense unique data D = 130B

**Figure 3.** Downstream performance of 7B models: pre-trained (top) and SFT-ed (middle and bottom) versions. Across all benchmark types, MoE models with ra = 20% outperform dense model trained with twice the compute, aligning with upstream observations that the optimal AR is 20%.

for a more detailed discussion). To further validate the possible universality of our ﬁndings, we conducted experiments on N ≈3B models and achieved similar results (see Fig. 5 in Appendix E).

Expert specialization is another signiﬁcant potential of MoEs in addition to remarkable scalability, where each expert focuses on learning speciﬁc features or patterns within the data. However, this attribute has not yet been clearly observed even in state-of-the-art MoE LLMs (Lo et al., 2024; Zhang et al., 2024), and effective approaches to achieve it remain under-explored. Based on our observation that MoEs outperform dense models when ra ∈R∗ a, we conjecture a relationship between the optimal AR region and the degree of expert specialization. Speciﬁcally: 1) When the activation rate is too low (ra < 10%), the model lacks sufﬁcient parameters to store knowledge effectively. 2) When the activation rate is relatively high (ra > 50%), more experts are typically activated, which may lead to weaker specialization. An activation rate within the optimal region R∗ a likely facilitates a higher degree of expert specialization, thereby enhancing the MoE model’s performance compared to its dense counterpart. We leave further analysis of this potential relationship for future work.

## 6 DATA REUSE STRATEGY

As discussed in § 5.2, MoEs outperform their dense counterparts but require additional data. To eliminate this increased data demand, we investigate data reusability by training models for multiple epochs using a ﬁxed, smaller dataset size ˆD. We extract a sub-dataset of size ˆD from the original training dataset. At the beginning of each epoch after the ﬁrst, the data are shufﬂed.

Setup. We explore two distinct schemes, termed the strict and the loose data reuse schemes.

For the strict scheme, our aim is to ensure that both MoE and dense models are trained under completely equal conditions with respect to N, D, and C. Given a ﬁxed ˆD, the number of training epochs (ranging from 1.7 to 8.3 in our 3B and 7B model experiments) increases as ra decreases (hence decreasing M) to maintain the compute budget C. The experimental settings are detailed in Table 14, 15, 16, in Appendix E, which are mostly the same as those in § 5.2, except for the training data used. Speciﬁcally, we set ˆD = 65B and 114B for the 3B models, and ˆD = 68B for the 7B models, corresponding to the data used for training the dense models.

<!-- Page 9 -->

Published as a conference paper at ICLR 2026

**Table 2.** Accuracy of 7B SFT-ed models across different benchmarks.

Dense baseline MoE w/ optimal AR

Pretrain info

Activation rate - 20.07 20.07 Compute 5.45e21 2.86e21 2.86e21 Data reuse - strict

Knowledge

CMMLU (Li et al., 2024) 31.23 31.62 32.11 MMLU (Hendrycks et al., 2021b) 31.26 32.92 24.57 MMLU-Redux (Gema et al., 2024) 28.90 30.93 23.73 MMLU-Pro (Wang et al., 2024) 14.12 13.59 13.59

Reasoning

DROP (Dua et al., 2019) 32.32 35.13 30.93 LiveBench (White et al., 2024) 16.82 18.15 16.76 MUSR (Sprague et al., 2023) 35.98 35.58 48.94

Comprehensive AGIEval (Zhong et al., 2023) 20.89 22.07 21.02 BBH (Suzgun et al., 2023) 58.02 60.01 56.07

Math GAOKAO-Math24 (Zhang et al., 2023) 9.92 15.70 9.09 GSM8K (Cobbe et al., 2021) 13.34 15.54 11.22

Code

APPS (Hendrycks et al., 2021a) 7.35 6.80 8.18 DS-1000 (Lai et al., 2023) 5.70 6.90 4.60 HumanEval (Chen et al., 2021) 22.56 21.34 21.95 LeetCode (Coignion et al., 2024) 1.49 1.67 1.49 LiveCodeBench (Jain et al., 2024) 4.21 4.63 3.37

For the loose scheme, we relax the constraint of identical D by ﬁxing the number of training epochs to 2 for all ra, hence ˆD = 0.5D, where the exact value of D corresponds to the speciﬁc ra. We conduct experiments on 7B models and the experimental settings are in Table 17 in Appendix E.

Results. The performance under the strict scheme is illustrated by the blue dashed lines in Fig. 2b and 5 in Appendix E. Reusing data ˆD only marginally diminishes performance compared to training on the unique dataset D for a single epoch, and MoE models continue to outperform dense baselines. Moreover, increasing ˆD further narrows the performance gap. The similarity in curve shapes indicates that the optimal activation rate r∗∗ a remains unchanged. These ﬁndings address the primary question posed at the beginning of this paper: Mixture-of-Experts can surpass dense LLMs under equal total parameters, compute, and data constraints, provided that the backbones are optimized and ra ∈R∗ a. We further discuss the reuse-vs-unique trade-offs below.

Discussion. Prior works have explored the effectiveness of multi-epoch training for dense and MoE models. Muennighoff et al. (2023) developed a scaling law that accounts for the number of repeated tokens and found negligible loss for repeating up to 4 epochs compared to training on unique data, whereas Hernandez et al. (2022) showed degradation for dense models. Xue et al. (2023) noticed no signiﬁcant gain for MoEs with repeated training when high-quality data is insufﬁcient. We emphasize that our goal here is not to claim that multi-epoch training is generally better for MoEs; rather, we examine whether MoEs can still surpass dense models when the unique-token budget is ﬁxed. Concretely, under the loose scheme (green dashed line), for each ra we keep the consumed-token budget D ﬁxed and compare (i) a 2-epoch run on a subset of size ˆD = 0.5D (thus processing D tokens with reuse) and (ii) a 1-epoch run that consumes D tokens without reuse (i.e., D unique tokens), where both are sampled from the same data recipe/distribution. We ﬁnd that the 2-epoch reuse setting can match, and sometimes slightly improve over, the 1-epoch unique-token baseline at several suboptimal ra points; however, for the 7B models, at the most important optimal point (ra ≈20%) it does not exceed the 1-epoch unique-token baseline. In all case for the 7B models, using more than two epochs (multi-epoch) consistently degrades performance. For the 3B models under the strict reuse setting, at a ﬁxed ra, using a larger unique-token budget (e.g., ˆD = 114B) consistently outperforms a smaller one (e.g., ˆD = 65B), aligning with the intuition that more unique data is better even under multi-epoch training (see Fig. 5 and Tables 15–16 in Appendix E). Moreover, increasing the unique-token budget from 114B (trained for 2–3 epochs) to 309B (trained for 1 epoch) yields only a marginal improvement under the same token-consumption budget (Fig. 5). Moreover, under a ﬁxed consumed-token budget (D = 309B), increasing the unique-token budget from ˆD = 114B (trained for ∼2–3 epochs with reuse) to 309B (trained for 1 epoch without reuse) yields only a marginal improvement (Fig. 5). Overall, these results suggest that MoE models may

<!-- Page 10 -->

Published as a conference paper at ICLR 2026 tolerate mild repetition (around two epochs) under a ﬁxed token-consumption budget, but additional repetition becomes harmful.

## 7 ANALYSIS OF DOWNSTREAM PERFORMANCE

To assess whether the optimal ARs generalize to downstream tasks, we conduct SFT on our 7B pre-trained models (trained w/ and w/o strict data reuse) and evaluate both the pre-trained models and SFT-ed models on a total number of 29 benchmarks (see Fig. 3 and Tab. 2), including categories such as reasoning and knowledge. The comprehensive list of benchmarks can be found in Appendix D. For all SFT trainings, we use a ﬁxed data size D, and thus varying C across models with different ra. The 7B dense model trained with twice the compute is included for comparison.

MoE vs. Dense at ra = r∗∗ a. For both PT and SFT models, MoEs outperform their dense equivalents across all benchmark types when ra = 20%. This result aligns with upstream ﬁndings that the optimal activation rate (r∗∗ a) is 20%, highlighting the very possible universality of the optimal AR point across different training phases and data domains. Furthermore, r∗∗ a remains unchanged during SFT, even with varying C, suggesting that the SFT data size may have an upper limit for performance improvement, provided the PT model is adequately trained. Additionally, the average performance at ra̸ = r∗∗ a is consistently inferior to that of dense models, underscoring the critical role of the optimal AR point.

MoE vs. Dense at ra < r∗∗ a. Dense models outperform MoEs across all domains for PT models. After SFT, MoEs overtake dense models on comprehensive and knowledge tasks. However, a notable performance gap remains in math, highlighting the PT stage’s importance for math ability.

MoE vs. Dense at ra > r∗∗ a. Compared to the dense models, MoEs perform better on knowledge but worse on reasoning for PT models, and usually slightly underperform after SFT.

Sparser vs. Denser. For PT models, denser MoEs (ra > r∗∗ a) outperform or match the performance of sparser MoEs (ra < r∗∗ a) across all domains, consistent with Figure 2b, regardless of data reuse. When training on unique data, sparser MoEs perform better on knowledge. Notably, denser MoE performance signiﬁcantly degrades with data reuse, especially for SFT.

Impact of data reuse. For both PT and SFT models, data reuse has little impact on reasoning but causes signiﬁcant degradation in knowledge performance. Surprisingly, at ra = r∗∗ a, the SFT-ed MoEs trained with data reuse outperform both MoEs and dense models trained on unique data. This implies that a model can master reasoning skills (rather than merely memorizing information (Hu et al., 2024)) with a relatively small dataset (Muennighoff et al., 2025; Wang et al., 2025) and further enhance its capabilities through multiple training epochs.

## 8 CONCLUSION AND FUTURE WORKS

In this paper, we propose a three-step experimental methodology to investigate whether MoEs can surpass their dense counterparts under the same constraints on total parameters, compute, and data. By optimizing the architecture, identifying the optimal activation rate region, and reusing data, we arrive at a positive answer to this question. Future work will explore how optimal activation rates enhance model capabilities and whether similar conclusions hold for other training methods like upcycling (Komatsuzaki et al., 2023) and MoEﬁcation (Zhang et al., 2022). We hope this work offers valuable insights for the architectural design of next-generation models.

## LIMITATIONS

The limitations of this work include: 1) Hindering by the high computational cost, we did not train models larger than 7B. 2) As described in § 4, we focus mainly on the impact of several main components of MoEs, but ﬁx the rest to narrow the scale of experiments. 3) Exploration of other elements can provide further comprehensive guidance for the architectural design of MoEs.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

## REFERENCES

Samira Abnar, Harshay Shah, Dan Busbridge, Alaaeldin Mohamed Elnouby Ali, Josh Susskind, and Vimal Thilak. Parameters vs ﬂops: Scaling laws for optimal sparsity for mixture-of-experts language models. arXiv preprint arXiv:2501.12370, 2025.

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman,

Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge,

Yu Han, Fei Huang, et al. Qwen technical report. arXiv preprint arXiv:2309.16609, 2023.

Yonatan Bisk, Rowan Zellers, Ronan Le Bras, Jianfeng Gao, and Yejin Choi. Piqa: Reasoning about physical commonsense in natural language, 2019.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared

Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374, 2021.

Christopher Clark, Kenton Lee, Ming-Wei Chang, Tom Kwiatkowski, Michael Collins, and Kristina

Toutanova. Boolq: Exploring the surprising difﬁculty of natural yes/no questions. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 2924–2936, 2019. URL https://aclanthology.org/N19-1300/.

Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and

Oyvind Tafjord. Think you have solved question answering? try arc, the ai2 reasoning challenge. arXiv preprint arXiv:1803.05457, 2018.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,

Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training veriﬁers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021.

Tristan Coignion, Clément Quinton, and Romain Rouvoy. A performance study of llm-generated code on leetcode. In Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering, pp. 79–89, 2024.

Damai Dai, Chengqi Deng, Chenggang Zhao, RX Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding

Zeng, Xingkai Yu, Y Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixtureof-experts language models. arXiv preprint arXiv:2401.06066, 2024.

DeepSeek-AI, Xiao Bi, Deli Chen, Guanting Chen, Shanhuang Chen, Damai Dai, et al. Deepseek llm: Scaling open-source language models with longtermism, 2024a. URL https://arxiv. org/abs/2401.02954.

DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, et al. Deepseek-v3 technical report, 2024b. URL https://arxiv.org/abs/2412.19437.

Dheeru Dua, Yizhong Wang, Pradeep Dasigi, Gabriel Stanovsky, Sameer Singh, and Matt Gardner.

Drop: A reading comprehension benchmark requiring discrete reasoning over paragraphs. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 2368–2378, 2019. URL https://aclanthology.org/N19-1246/.

William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efﬁcient sparsity. Journal of Machine Learning Research, 23(120):1–39, 2022.

Aryo Pradipta Gema, Joshua Ong Jun Leang, Giwon Hong, Alessio Devoto, Alberto Carlo Maria

Mancino, Rohit Saxena, Xuanli He, Yu Zhao, Xiaotang Du, Mohammad Reza Ghasemi Madani, et al. Are we done with mmlu? arXiv preprint arXiv:2406.04127, 2024.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Ethan He, Abhinav Khattar, Ryan Prenger, Vijay Korthikanti, Zijie Yan, Tong Liu, Shiqing Fan,

Ashwath Aithal, Mohammad Shoeybi, and Bryan Catanzaro. Upcycling large language models into mixture of experts. arXiv preprint arXiv:2410.07524, 2024.

Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin

Burns, Samir Puranik, Horace He, Dawn Song, et al. Measuring coding challenge competence with apps. arXiv preprint arXiv:2105.09938, 2021a.

Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob

Steinhardt. Measuring massive multitask language understanding. In International Conference on Learning Representations, 2021b.

Danny Hernandez, Tom Brown, Tom Conerly, Nova DasSarma, Dawn Drain, Sheer El-Showk,

Nelson Elhage, Zac Hatﬁeld-Dodds, Tom Henighan, Tristan Hume, Scott Johnston, Ben Mann, Chris Olah, Catherine Olsson, Dario Amodei, Nicholas Joseph, Jared Kaplan, and Sam McCandlish. Scaling laws and interpretability of learning from repeated data, 2022. URL https: //arxiv.org/abs/2205.10487.

Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza

Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. Training compute-optimal large language models. In Advances in Neural Information Processing Systems, volume 35, pp. 30016–30030, 2022.

Junjie Hu, Sebastian Ruder, Aditya Siddhant, Graham Neubig, Orhan Firat, and Melvin Johnson.

Xtreme: A massively multilingual multi-task benchmark for evaluating cross-lingual generalisation. In International conference on machine learning, pp. 4411–4421. PMLR, 2020.

Yi Hu, Xiaojuan Tang, Haotong Yang, and Muhan Zhang. Case-based or rule-based: How do transformers do the math? In Forty-ﬁrst International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024. URL https://openreview. net/forum?id=4Vqr8SRfyX.

Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando

Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. arXiv preprint arXiv:2403.07974, 2024.

Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bam- ford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts. arXiv preprint arXiv:2401.04088, 2024.

Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child,

Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361, 2020.

Aran Komatsuzaki, Joan Puigcerver, James Lee-Thorp, Carlos Riquelme Ruiz, Basil Mustafa,

Joshua Ainslie, Yi Tay, Mostafa Dehghani, and Neil Houlsby. Sparse upcycling: Training mixtureof-experts from dense checkpoints. In International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=T5nUQDrM4u.

Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redﬁeld, Michael Collins, Ankur Parikh, Chris Al- berti, Danielle Epstein, Illia Polosukhin, Matthew Kelcey, Jacob Devlin, Kenton Lee, Kristina N. Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural questions: a benchmark for question answering research. Transactions of the Association of Computational Linguistics, 2019.

Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang, and Eduard Hovy. RACE: Large-scale ReAding comprehension dataset from examinations. In Martha Palmer, Rebecca Hwa, and Sebastian Riedel (eds.), Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing, pp. 785–794, Copenhagen, Denmark, September 2017. Association for Computational Linguistics. doi: 10.18653/v1/D17-1082. URL https://aclanthology.org/D17-1082/.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Wen-tau

Yih, Daniel Fried, Sida Wang, and Tao Yu. Ds-1000: A natural and reliable benchmark for data science code generation. In International Conference on Machine Learning, pp. 18319–18345. PMLR, 2023.

Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang,

Maxim Krikun, Noam Shazeer, and Zhifeng Chen. Gshard: Scaling giant models with conditional computation and automatic sharding. In International Conference on Learning Representations, 2021. URL https://openreview.net/forum?id=qrwe7XHTmYb.

Haonan Li, Yixuan Zhang, Fajri Koto, Yifei Yang, Hai Zhao, Yeyun Gong, Nan Duan, and Timothy

Baldwin. Cmmlu: Measuring massive multitask language understanding in chinese. In Findings of the Association for Computational Linguistics ACL 2024, pp. 11595–11620, 2024. URL https://aclanthology.org/2024.findings-acl.671/.

Houyi Li, Wenzhen Zheng, Jingcheng Hu, Qiufeng Wang, Hanshan Zhang, Zili Wang, Shijie

Xuyang, Yuantao Fan, Shuigeng Zhou, Xiangyu Zhang, et al. Predictable scale: Part i, step law – optimal hyperparameter scaling law in large language model pretraining. arXiv preprint arXiv:2503.04715, 2025.

Ka Man Lo, Zeyu Huang, Zihan Qiu, Zili Wang, and Jie Fu. A closer look into mixture-of-experts in large language models. arXiv preprint arXiv:2406.18219, 2024.

Jan Ludziejewski, Maciej Pióro, Jakub Krajewski, Maciej Stefaniak, Michał Krutul, Jan Mała´snicki,

Marek Cygan, Piotr Sankowski, Kamil Adamczewski, Piotr Miło´s, and Sebastian Jaszczur. Joint moe scaling laws: Mixture of experts can be memory efﬁcient, 2025. URL https://arxiv. org/abs/2502.05172.

Niklas Muennighoff, Alexander Rush, Boaz Barak, Teven Le Scao, Nouamane Tazi, Aleksandra

Piktus, Sampo Pyysalo, Thomas Wolf, and Colin A Raffel. Scaling data-constrained language models. Advances in Neural Information Processing Systems, 36:50358–50376, 2023.

Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke

Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time scaling. arXiv preprint arXiv:2501.19393, 2025.

Oﬁr Press, Noah A Smith, and Mike Lewis. Train short, test long: Attention with linear biases enables input length extrapolation. In International Conference on Learning Representations, 2022. URL https://openreview.net/forum?id=R8sQPpGCv0.

Qwen, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan

Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2024. URL https://arxiv.org/abs/2412.15115.

Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving language understanding by generative pre-training. 2018. URL https://cdn.openai.com/ research-covers/language-unsupervised/language_understanding_ paper.pdf.

Samyam Rajbhandari, Conglong Li, Zhewei Yao, Minjia Zhang, Reza Yazdani Aminabadi, Am- mar Ahmad Awan, Jeff Rasley, and Yuxiong He. Deepspeed-moe: Advancing mixture-of-experts inference and training to power next-generation ai scale, 2022. URL https://arxiv.org/ abs/2201.05596.

Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi. Winogrande: An adver- sarial winograd schema challenge at scale. 2020.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Maarten Sap, Hannah Rashkin, Derek Chen, Ronan LeBras, and Yejin Choi. Socialiqa: Commonsense reasoning about social interactions. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 4463–4473, 2019. URL https: //aclanthology.org/D19-1454/.

Noam Shazeer. Glu variants improve transformer. arXiv preprint arXiv:2002.05202, 2020.

Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017.

Zayne Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett. Musr: Testing the limits of chain-of-thought with multistep soft reasoning. arXiv preprint arXiv:2310.16049, 2023.

Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung,

Aakanksha Chowdhery, Quoc V Le, Ed H Chi, Denny Zhou, et al. Challenging big-bench tasks and whether chain-of-thought can solve them. In Findings of the Association for Computational Linguistics: ACL 2023, pp. 13003–13051, 2023. URL https://aclanthology. org/2023.findings-acl.824/.

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée

Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efﬁcient foundation language models. arXiv preprint arXiv:2302.13971, 2023a.

Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Niko- lay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and ﬁne-tuned chat models. arXiv preprint arXiv:2307.09288, 2023b.

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez,

Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in Neural Information Processing Systems, 2017.

Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Lucas Liu, Baolin Peng, Hao Cheng, Xuehai

He, Kuan Wang, Jianfeng Gao, et al. Reinforcement learning for reasoning in large language models with one training example. arXiv preprint arXiv:2504.20571, 2025.

Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming

Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. Mmlu-pro: A more robust and challenging multitask language understanding benchmark. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2024.

Tianwen Wei, Bo Zhu, Liang Zhao, Cheng Cheng, Biye Li, Weiwei Lü, Peng Cheng, Jianhao Zhang,

Xiaoyu Zhang, Liang Zeng, et al. Skywork-moe: A deep dive into training techniques for mixtureof-experts language models. arXiv preprint arXiv:2406.06563, 2024.

Johannes Welbl, Nelson F Liu, and Matt Gardner. Crowdsourcing multiple choice science questions.

arXiv preprint arXiv:1707.06209, 2017.

Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid Shwartz-

Ziv, Neel Jain, Khalid Saifullah, Siddartha Naidu, et al. Livebench: A challenging, contaminationlimited llm benchmark. arXiv preprint arXiv:2406.19314, 2024.

Shaohua Wu, Jiangang Luo, Xi Chen, Lingjun Li, Xudong Zhao, Tong Yu, Chao Wang, Yue Wang,

Fei Wang, Weixu Qiao, et al. Yuan 2.0-m32: Mixture of experts with attention router. arXiv preprint arXiv:2405.17976, 2024.

Liang Xu, Hai Hu, Xuanwei Zhang, Lu Li, Chenjie Cao, Yudong Li, Yechen Xu, Kai Sun, Dian Yu,

Cong Yu, et al. Clue: A chinese language understanding evaluation benchmark. In Proceedings of the 28th International Conference on Computational Linguistics, pp. 4762–4772, 2020. URL https://aclanthology.org/2020.coling-main.419/.

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

Fuzhao Xue, Yao Fu, Wangchunshu Zhou, Zangwei Zheng, and Yang You. To repeat or not to repeat:

Insights from scaling llm under token-crisis, 2023. URL https://arxiv.org/abs/2305. 13230.

Fuzhao Xue, Zian Zheng, Yao Fu, Jinjie Ni, Zangwei Zheng, Wangchunshu Zhou, and Yang

You. Openmoe: An early effort on open mixture-of-experts language models. arXiv preprint arXiv:2402.01739, 2024.

An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li,

Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jianxin Yang, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao,

Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, Zhifang Guo, and Zhihao Fan. Qwen2 technical report, 2024. URL https://arxiv.org/abs/2407.10671.

Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. Hellaswag: Can a ma- chine really ﬁnish your sentence? In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 3444–3453, 2019. doi: 10.18653/v1/P19-1472. URL https://aclanthology.org/P19-1472/.

Biao Zhang and Rico Sennrich. Root mean square layer normalization. Advances in Neural Infor- mation Processing Systems, 32, 2019.

Xiaotian Zhang, Chunyang Li, Yi Zong, Zhengyu Ying, Liang He, and Xipeng Qiu. Evaluating the performance of large language models on gaokao benchmark. arXiv preprint arXiv:2305.12474, 2023.

Zeliang Zhang, Xiaodong Liu, Hao Cheng, Chenliang Xu, and Jianfeng Gao. Diversifying the expert knowledge for task-agnostic pruning in sparse mixture-of-experts. arXiv preprint arXiv:2407.09590, 2024.

Zhengyan Zhang, Yankai Lin, Zhiyuan Liu, Peng Li, Maosong Sun, and Jie Zhou. Moeﬁcation:

Transformer feed-forward layers are mixtures of experts. In Findings of the Association for Computational Linguistics: ACL 2022, pp. 877–890, 2022. URL https://aclanthology.org/ 2022.findings-acl.71/.

Wanjun Zhong, Ruixiang Cui, Yiduo Guo, Yaobo Liang, Shuai Lu, Yanlin Wang, Amin Saied,

Weizhu Chen, and Nan Duan. Agieval: A human-centric benchmark for evaluating foundation models. arXiv preprint arXiv:2304.06364, 2023.

Barret Zoph, Irwan Bello, Sameer Kumar, Nan Du, Yanping Huang, Jeff Dean, Noam Shazeer, and

William Fedus. St-moe: Designing stable and transferable sparse expert models. arXiv preprint arXiv:2202.08906, 2022.

## APPENDIX

A BACKGROUND: MIXTURE-OF-EXPERTS

The MoE architecture primarily consists of a gate and several experts. Typically, the gate g(·) is composed of a linear layer Wg followed by a Softmax and a Top-K operation, and the experts {Ei}E i=1 follow the standard FFN structure. The computation of an MoE block can then be formulated as

<!-- Page 16 -->

Published as a conference paper at ICLR 2026 follows:

si(x) = Softmaxi(Wgx), (11) T (x) = TopK(s(x); K), (12)

gi(x) =

{si(x) if i ∈T (x), 0 otherwise, (13)

y =

E ∑ i=1 gi(x) · Ei(x), (14)

where si(x) denotes the gate score for the i-th expert. Unless otherwise speciﬁed, we use the above non-normalized Top-K gating in this paper (i.e., we do not renormalize the K selected scores to sum to 1). For completeness, the commonly used Top-K normalization is

˜gi(x) =

 

 gi(x) ∑ j∈T (x) gj(x) if i ∈T (x),

0 otherwise.

(15)

We also adopt the standard auxiliary load-balancing loss (used throughout our experiments) to encourage uniform expert utilization. Given a minibatch B, deﬁne fi = 1

|B|

∑ x∈B

I[i ∈T (x)], (16)

pi = 1

|B|

∑ x∈B si(x), (17)

and compute

Lbalance = E

E ∑ i=1 fi pi, Ltotal = LCE + λLbalance. (18)

B EXTENDED ANALYSIS ON RELATED WORK

We notice a concurrent work (Abnar et al., 2025) studied scaling law for optimal MoE sparsity. We highlight the differences between our work and theirs as follows:

• Formulation: We deﬁne “sparsity” as the activation rate ra = Na/N, which is a more general deﬁnition than that proposed by Abnar et al. (2025), namely the ratio of inactive experts to the total number of experts, (E −K)/E. • Methodology: Given that the activation rate ra does not depend on the underlying model architecture, we can thus easily take into consideration other components such as shared expert and build all our models upon the optimized architecture proposed in § 4. This ensures the observed performance differences solely attribute to the varying activation rates. • Sufﬁcient training: Our main comparisons operate in a sufﬁciently trained regime (often beyond the compute-optimal point). For example, the 2B MoE models in Table 9 have D/N ranging from 53 to 252, and the 7B MoE models in Table 11 have D/N ranging from 20 to 93, while our dense baselines satisfy D/N ≥20 (Table 13), aligning with the common compute-optimal guideline (Hoffmann et al., 2022). This perspective is practically important since industrial model design often cares about the best achievable performance at a ﬁxed-N budget (e.g., training a 7B model on trillions of tokens), and it also enables more reliable downstream SFT comparisons that would be less meaningful with undertrained checkpoints. • Perspective under limited resources: Scaling-law studies often adopt broad sweeps that trade depth for breadth under limited compute, which can lead to undertrained large-model settings (e.g., Abnar et al. (2025) uses C = 1e20 per run for a sweep up to 30B, and Ludziejewski et al. (2025) uses at most 80B tokens). In contrast, our 7B study allocates substantially more compute per setting (e.g., multiple runs with C ≈2.86e21 or C ≈ 5.45e21; Table 12 and Table 13), prioritizing a high-D/N regime to more deeply investigate the ﬁxed-N & ﬁxed-C question motivated by deployment memory constraints.

<!-- Page 17 -->

Published as a conference paper at ICLR 2026

**Table 3.** Pretraining data recipe compared with the LLaMA-1 recipe.

DataSet Class Our Recipe Our Data Set Detail LLaMA-1 Recipe LLaMA-1 Data Set Detail Recipe Diff

WebData-en 79.53% CC (English) 82% 67% CC + 15% C4 (English) -2.47% Code 4.62% The Stack 4.50% Github-Big Query +0.12% Wikipedia 5.06% en: 1.69%, cn: 0.13%, others: 3.24% 4.50% multi-lingual +0.56% Book 5.18% open source English books 4.50% book3, Gutenberg +0.68% arXiv 3.38% as class name 1.06% as class name +2.32% StackExchange 2.21% as class name 2.00% as class name +0.21%

• Conclusion: We discover an optimal activation rate that appears to be independent of model sizes, whereas Abnar et al. (2025) ﬁnd that the optimal sparsity increases with model size.

Our conclusion regarding a consistent optimal activation rate contradicts the ﬁndings of Abnar et al. (2025). While we believe our ﬁndings are reliable, given that our experiments are conducted with strictly controlled variables using optimized backbones and sufﬁcient training data, we acknowledge the possibility that the optimal ra might slightly shift for model sizes signiﬁcantly beyond our studied range (i.e., N >> 7B). Nevertheless, we contend that the optimal ra can be considered consistent within a certain range of model sizes, in contrast to the signiﬁcant changes reported by Abnar et al. (2025).

C PRETRAINING DATA RECIPE

For reproducibility, we provide the mixture ratios of our pretraining corpus and a comparison with the LLaMA-1 recipe (Touvron et al., 2023a). Our recipe is intentionally close to a LLaMA-1–style mixture, and the corresponding data sources have public counterparts.

D COMPREHENSIVE LIST OF BENCHMARKS

To assess whether the optimal ARs generalize to downstream tasks, we conduct SFT on our 7B pre-trained models (trained w/ and w/o strict data reuse) and evaluate both the pre-trained models and SFT-ed models on a total number of 29 benchmarks (Figure 3). The comprehensive list of benchmarks is provided here.

For pre-trained models, we evaluate on:

• Knowledge: BBH (Suzgun et al., 2023), PIQA (Bisk et al., 2019), SCIQ (Welbl et al., 2017), SIQA (Sap et al., 2019)

• Reasoning: ARC (Clark et al., 2018), BoolQ (Clark et al., 2019), CLUE (Xu et al., 2020), DROP (Dua et al., 2019), HellaSwag (Zellers et al., 2019), NaturalQA (Kwiatkowski et al., 2019), RACE (Lai et al., 2017), WinoGrande (Sakaguchi et al., 2020), XTREME (Hu et al., 2020)

For SFT-ed models, we evaluate on:

• Comprehensive: AGIEVAL (Zhong et al., 2023), BBH

• Knowledge: CMMLU (Li et al., 2024), MMLU (Hendrycks et al., 2021b), MMLU- Redux (Gema et al., 2024), MMLU-Pro (Wang et al., 2024)

• Reasoning: DROP, LiveBench (White et al., 2024), MuSR (Sprague et al., 2023)

• Math: GAOKAO-Math24 (Zhang et al., 2023), GSM8K (Cobbe et al., 2021)

• Code: APPS (Hendrycks et al., 2021a), DS-1000 (Lai et al., 2023), HumanEval (Chen et al., 2021), LeetCode (Coignion et al., 2024), LiveCodeBench (Jain et al., 2024)

E MORE EXPERIMENTAL RESULTS

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

20 40 60 80 100 120

1.675

1.680

1.685

1.690

1.695

1.700

Loss

20 30 40 50 60

Dm

640 768 896

**Figure 4.** Results for model shape ratios ζ and µ. An overall upward trend is observed in ζ as Dm increases, while µ exhibits a downward trend with increasing Dm.

**Table 4.** Common training recipe.

Hyperparameter Setting

Vocab 65536 Optimizer Adam Weight decay 0.1 Gradient clipping norm 1.0 LR Scheduler Cosine Warmup iters clip(0.01 · Iters, 200, 2000) Min LR 1e-5

**Table 5.** Experimental settings and results of MoE layer arrangement and shared expert. Hyperparameters shared by all experiments: Dm = 1408, Dffn = 3904, Norm = True.

N Na M H Dh L E K De Dse Scheme L Conclusion

2.02B 346M 8.77e8 22 64 16 35 2 800 full+SE 1.6813 interleave performs better than full 2.02B 346M 8.77e8 22 64 16 68 2 800 interleave+SE 1.6766 2.02B 346M 8.77e8 22 64 16 70 4 800 0 interleave 1.6697

2.15B 366M 6.63e9 11 128 16 85 5 352 1dense+SE 1.8700

1dense+SE performs the best 2.15B 366M 6.63e9 22 64 16 85 5 352 1dense+SE 1.8557 2.15B 367M 6.63e9 11 128 16 70 4 800 0 interleave 1.8737 2.15B 367M 6.63e9 22 64 16 70 4 800 0 interleave 1.8620

2.15B 368M 9.31e8 22 64 17 37 4 800 0 1dense 1.6752 Dse (Dse + KDe) impacts little 2.15B 368M 9.31e8 22 64 17 36 3 800 800 1dense+SE 1.6712 2.15B 368M 9.31e8 22 64 17 35 2 800 1dense+SE 1.6726

**Table 6.** Experimental settings and results of gate score normalization. Hyperparameters shared by all experiments: Scheme = 1dense, L = 17, Dm = 1408, Dffn = 3904, H = 22, Dh = 64.

N Na ra (%) M E K De Dse Norm L ¯ Lbalance

2.15B 368M 17.08 9.31e8 35 2 800 Y 1.6726 1.355 2.15B 368M 17.08 9.31e8 35 2 800 N 1.6712 1.452

2.15B 368M 17.08 9.31e8 37 4 800 0 Y 1.6752 1.409 2.15B 368M 17.08 9.31e8 37 4 800 0 N 1.6750 1.440

**Table 7.** Experimental settings and results of top-K setting. Hyperparameters shared by all experiments: Scheme = 1dense, L = 16, Dm = 1408, Dffn = 3904, H = 11, Dh = 128, Norm = False.

N Na ra (%) M E K De Dse L

2.15B 591M 27.47 8.00e9 8 1 2.0470 2.15B 591M 27.40 8.00e9 88 11 320 2.0338

2.15B 949M 44.00 1.01e10 8 2 1.9996 2.15B 948M 44.05 1.01e10 88 22 288 2.0266

2.15B 1.24B 57.57 1.19e10 8 3 2.0156 2.11B 1.22B 57.68 1.18e10 88 33 256 2.0235

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

**Table 8.** Experimental settings and results of model shape ratios. Hyperparameters shared by all experiments: Scheme = 1dense, S = 16384, Dh = 128.

N Na Dm Dffn L H E K De Dse µ ζ L

2.15e9 3.67e8 640 34 5 50 4 608 51.30 20.39 1.694 2.15e9 3.69e8 640 37 5 38 3 736 47.15 18.78 1.696 2.14e9 3.69e8 640 49 5 41 3 512 35.20 14.33 1.695 2.14e9 3.67e8 768 20 6 99 8 448 62.42 41.42 1.693 2.15e9 3.69e8 896 15 7 124 10 416 62.21 65.00 1.699 2.15e9 3.68e8 896 20 7 91 7 416 45.50 48.16 1.687 2.13e9 3.67e8 896 24 7 54 4 576 37.29 39.96 1.692 2.15e9 3.69e8 896 34 7 61 4 352 25.54 28.15 1.680 2.16e9 3.68e8 896 37 7 47 3 416 23.21 25.89 1.682 2.14e9 3.70e8 28 8 80 5 288 23.91 38.93 1.681 2.16e9 3.69e8 49 8 49 2 256 512 12.75 22.33 1.693 2.15e9 3.67e8 12 9 79 6 640 47.22 105.73 1.688 2.14e9 3.68e8 34 9 64 3 256 768 14.89 35.91 1.679 2.15e9 3.69e8 28 10 113 5 160 800 14.75 48.41 1.675 2.15e9 3.70e8 24 11 46 2 416 832 14.18 62.22 1.678 2.13e9 3.68e8 12 12 65 4 576 25.88 140.64 1.685 2.16e9 3.68e8 15 12 91 5 320 20.00 110.71 1.674 2.15e9 3.66e8 20 12 95 4 224 896 14.44 81.84 1.681 2.16e9 3.68e8 15 14 128 5 192 960 14.25 129.00 1.693 2.14e9 3.67e8 12 15 71 3 416 16.03 175.55 1.699

**Table 9.** Experimental settings and results of optimal ARs for MoE models with N = 2.15B and ﬁxed ra. Hyperparameters shared by all experiments: L = 16, S = 2048, Dm = 1408, Dffn = 3904, H = 11, Dh = 128, ζ = 88.

Na ra (%) M D C D/N E K De Dse η B # Iters BPC

1.88e8 8.74 1.68e9 1.14e11 1.92e20 53 89 1 352 352 2.01e-3 672 82833 0.5235 1.88e8 8.74 1.68e9 1.68e11 2.83e20 78 89 1 352 352 2.26e-3 832 98771 0.5159 1.88e8 8.74 1.68e9 3.67e11 6.16e20 170 89 1 352 352 2.87e-3 133187 0.5090 1.88e8 8.74 1.68e9 5.41e11 9.10e20 252 89 1 352 352 3.24e-3 152927 0.5048

2.33e8 10.81 1.95e9 1.14e11 2.22e20 53 88 2 352 704 2.01e-3 672 82833 0.5136 2.33e8 10.81 1.95e9 1.62e11 3.16e20 75 88 2 352 704 2.24e-3 896 88446 0.5084 2.33e8 10.81 1.95e9 2.31e11 4.50e20 107 88 2 352 704 2.49e-3 110149 0.5027 2.33e8 10.81 1.95e9 3.29e11 6.41e20 153 88 2 352 704 2.78e-3 125427 0.5002 2.33e8 10.81 1.95e9 4.68e11 9.12e20 218 88 2 352 704 3.10e-3 142822 0.4967

4.11e8 19.11 3.02e9 1.14e11 3.44e20 53 84 6 352 2.01e-3 672 82833 0.5013 4.11e8 19.11 3.02e9 1.46e11 4.42e20 68 84 6 352 2.17e-3 768 93015 0.4971 4.11e8 19.11 3.02e9 1.88e11 5.67e20 87 84 6 352 2.34e-3 960 95469 0.4953 4.11e8 19.11 3.02e9 2.41e11 7.27e20 112 84 6 352 2.52e-3 114870 0.4909 4.11e8 19.11 3.02e9 3.09e11 9.34e20 144 84 6 352 2.73e-3 117950 0.4872

7.52e8 34.95 5.06e9 1.14e11 5.77e20 53 84 15 320 2.01e-3 672 82833 0.4963 7.52e8 34.95 5.06e9 1.80e11 9.13e20 84 84 15 320 2.31e-3 896 98256 0.4892

1.09e9 50.79 7.11e9 1.14e11 8.10e20 53 84 26 288 2.01e-3 672 82833 0.4950 1.09e9 50.79 7.11e9 1.28e11 9.13e20 60 84 26 288 2.08e-3 704 89125 0.4933

**Table 10.** Experimental settings and results of optimal ARs for MoE models N = 2.15B with ﬁxed C. Hyperparameters shared by all experiments: L = 16, S = 2048, Dm = 1408, Dffn = 3904, H = 11, Dh = 128, ζ = 88. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) M D C D/N µ E K De Dse η B # Iters BPC

1.88e8 8.74 1.70e9 5.41e11 9.18e20 252 22.50 89 1 352 352 3.24e-3 152927 0.5048 2.33e8 10.82 1.96e9 4.68e11 9.19e20 218 22.50 88 2 352 704 3.10e-3 142822 0.4967 3.24e8 15.04 2.50e9 3.75e11 9.38e20 174 22.50 86 4 352 2.89e-3 136378 0.4896 3.68e8 17.11 2.77e9 3.39e11 9.38e20 158 22.50 85 5 352 2.80e-3 127756 0.4874 3.89e8 18.06 2.89e9 3.25e11 9.38e20 151 22.50 93 6 320 2.76e-3 123862 0.4871 4.11e8 19.12 3.03e9 3.09e11 9.38e20 144 22.50 84 6 352 2.73e-3 117950 0.4872 4.29e8 19.94 3.13e9 2.99e11 9.38e20 139 22.50 92 7 320 2.70e-3 117177 0.4857 5.90e8 27.46 4.10e9 2.23e11 9.15e20 104 22.55 8 1 2.46e-3 106335 0.4907 7.52e8 34.96 5.08e9 1.80e11 9.16e20 84 22.50 84 15 320 2.31e-3 896 98256 0.4892 9.48e8 44.11 6.25e9 1.47e11 9.16e20 68 22.56 8 2 2.16e-3 768 93460 0.4899 1.09e9 50.80 7.12e9 1.29e11 9.15e20 60 22.50 84 26 288 2.08e-3 704 89125 0.4933 1.24e9 57.73 8.01e9 1.14e11 9.13e20 53 22.56 8 3 2.006e-3 672 82833 0.4934

<!-- Page 20 -->

Published as a conference paper at ICLR 2026

**Table 11.** Experimental settings and results of optimal ARs for MoE models with N = 6.52B with ﬁxed D. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 2048, Dffn = 5464, H = 16, Dh = 128, ζ = 85.3.

Na ra (%) M D C D/N E K De Dse η B # Iters BPC

7.26e8 11.15 5.59e9 1.30e11 7.25e20 19.90 82 2 512 4.74e-4 640 98816 0.4808 8.70e8 13.36 6.46e9 1.30e11 8.37e20 19.90 81 3 512 4.74e-4 640 98816 0.4763 1.02e9 15.67 7.33e9 1.30e11 9.49e20 19.90 80 4 512 4.74e-4 640 98816 0.4737 1.31e9 20.03 9.07e9 1.30e11 1.17e21 19.88 78 6 512 4.74e-4 640 98816 0.4703 1.70e9 26.11 1.15e10 1.30e11 1.48e21 19.90 86 10 448 4.74e-4 640 98816 0.4681 3.47e9 53.30 2.21e10 1.30e11 2.86e21 19.90 84 28 384 10752 4.74e-4 640 98816 0.4664

**Table 12.** Experimental settings and results of optimal ARs for MoE models with N = 6.52B with ﬁxed C. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 2048, Dffn = 5464, H = 16, Dh = 128, ζ = 85.3. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) M D C D/N µ E K De Dse η B # Iters BPC

5.85e8 8.97 4.73e9 6.05e11 2.86e21 92.88 21.00 83 1 512 512 7.62e-4 195502 0.4665 7.30e8 11.19 5.59e9 5.11e11 2.86e21 78.47 21.00 82 2 512 7.23e-4 183630 0.4624 8.74e8 13.41 6.46e9 4.43e11 2.86e21 67.93 21.00 81 3 512 6.92e-4 175482 0.4580 1.02e9 15.63 7.33e9 3.90e11 2.86e21 59.89 21.00 80 4 512 6.64e-4 165447 0.4571 1.31e9 20.07 9.07e9 3.16e11 2.86e21 48.50 21.00 78 6 512 6.23e-4 148410 0.4543 1.71e9 26.18 1.15e10 2.50e11 2.86e21 38.32 21.00 86 10 448 5.80e-4 960 127035 0.4580 1.96e9 30.07 1.30e10 2.21e11 2.86e21 33.83 21.00 84 12 448 5.57e-4 800 134597 0.4588 3.48e9 53.38 2.21e10 1.30e11 2.86e21 19.87 21.00 84 28 384 10752 4.74e-4 640 98816 0.4670

**Table 13.** Experimental settings and results of optimal ARs for 2B, 3B, and 7B dense baselines.

N M D C D/N L H Dm Dffn η B # Iters BPC

2.15e9 1.44e10 6.50e10 9.36e20 30.23 28 17 8.44e-4 320 99182 0.4921 2.15e9 1.44e10 1.14e11 1.64e21 53.02 28 17 1.00e-3 448 124032 0.4808

3.29e9 2.24e10 6.26e10 1.40e21 19.03 44 19 1.23e-3 448 68253 0.4833 3.29e9 2.24e10 1.25e11 2.80e21 38.06 44 19 1.52e-3 640 95554 0.4684

6.48e9 4.21e10 6.80e10 2.86e21 10.49 32 32 11008 3.89e-4 432 76813 0.4736 6.48e9 4.21e10 1.30e11 5.45e21 20.00 32 32 11008 4.76e-4 640 98816 0.4594

**Table 14.** Experimental settings and results of data reusing (ˆD = 68B) for MoE models with N = 6.52B with ﬁxed C. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 2048, Dffn = 5464, H = 16, Dh = 128, ζ = 85.3. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) M D Epoch M D/N µ E K De Dse η B # Iters BPC

7.30e8 11.19 5.59e9 5.11e11 7.52 2.86e21 78.47 21.00 82 2 512 7.23e-4 185816 0.4656 8.74e8 13.41 6.46e9 4.43e11 6.51 2.86e21 67.93 21.00 81 3 512 6.92e-4 175482 0.4618 1.02e9 15.63 7.33e9 3.90e11 5.74 2.86e21 59.89 21.00 80 4 512 6.64e-4 165447 0.4601 1.31e9 20.07 9.07e9 3.16e11 4.65 2.86e21 48.50 21.00 78 6 512 6.23e-4 150729 0.4590 1.71e9 26.18 1.15e10 2.50e11 3.67 2.86e21 38.32 21.00 86 10 448 5.80e-4 960 127035 0.4597 1.96e9 30.07 1.30e10 2.21e11 3.24 2.86e21 33.83 21.00 84 12 448 5.57e-4 792 135956 0.4603

**Table 15.** Experimental settings and results of strict data reuse (ˆD = 65B) for MoE models with N = 3.29B with ﬁxed C. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 1408, Dffn = 3904, H = 11, Dh = 128. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) D Epoch M C D/N E K De Dse η B # Iters BPC

2.78e8 8.46 5.41e11 8.33 2.51e9 1.36e21 164.62 89 1 352 352 3.24e-3 152927 0.4916 3.47e8 10.54 4.68e11 7.20 2.92e9 1.36e21 142.36 88 2 352 704 3.10e-3 142822 0.4841 4.83e8 14.70 3.75e11 5.78 3.74e9 1.40e21 114.19 86 4 352 2.89e-3 136378 0.4774 6.20e8 18.83 3.09e11 4.76 4.56e9 1.41e21 94.06 84 6 352 2.73e-3 117950 0.4757 8.93e8 27.12 2.23e11 3.43 6.19e9 1.38e21 67.74 8 1 2.465e-3 106335 0.4794 1.14e9 34.75 1.80e11 2.77 7.69e9 1.39e21 54.85 84 15 320 2.31e-3 896 98256 0.4786 1.44e9 43.77 1.47e11 2.26 9.48e9 1.39e21 44.52 8 2 2.169e-3 768 93460 0.4799 1.66e9 50.63 1.29e11 1.98 1.08e10 1.39e21 39.09 84 26 288 2.08e-3 704 89125 0.4830 1.89e9 57.40 1.14e11 1.75 1.22e10 1.39e21 34.61 8 3 2.006e-3 672 82833 0.4823

<!-- Page 21 -->

Published as a conference paper at ICLR 2026

0.1 0.2 0.3 0.4 0.5 Activation rate ra

0.470

0.475

0.480

0.485

0.490

BPC

3B MoEs, 1.4e21 FLOPs, D = 65B

3B MoEs, 1.4e21 FLOPs, D = 114B

3B MoE, 1.4e21 FLOPs, unique data 3B Dense, 1.4e21 FLOPs, D = 65B 3B Dense, 2.8e21 FLOPs, D = 130B

Data ~tokens

541B 468B 309B 223B 180B 147B 128B 114B

Data ~tokens

541B 468B 309B 223B 180B 147B 128B 114B

**Figure 5.** Performance of N ≈3B models trained with varying data sizes D and activation rate ra. The optimal activation rate, r∗∗

a = 20%, aligns with the ﬁndings for the 2B models (Figure 1). Additionally, compared to training on the unique dataset, the data reuse scheme shows only a slight performance reduction. To save computational costs, only one model trained on unique data is included for reference.

**Table 16.** Experimental settings and results of data reuse (ˆD = 114B) for MoE models with N = 3.29B with ﬁxed C. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 1408, Dffn = 3904, H = 11, Dh = 128. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) D Epoch M C D/N E K De Dse η B # Iters BPC

2.78e8 8.46 5.41e11 4.75 2.51e9 1.36e21 164.62 89 1 352 352 3.24e-3 152927 0.4896 3.47e8 10.54 4.68e11 4.11 2.92e9 1.36e21 142.36 88 2 352 704 3.10e-3 142822 0.4820 4.83e8 14.70 3.75e11 3.29 3.74e9 1.40e21 114.19 86 4 352 2.89e-3 136378 0.4760 6.20e8 18.83 3.09e11 2.71 4.56e9 1.41e21 93.93 84 6 352 2.73e-3 117950 0.4747 8.93e8 27.12 2.23e11 1.96 6.19e9 1.38e21 67.74 8 1 2.465e-3 106335 0.4774 1.14e9 34.75 1.80e11 1.58 7.69e9 1.39e21 54.85 84 15 320 2.31e-3 896 98256 0.4778 1.44e9 43.77 1.47e11 1.29 9.48e9 1.39e21 44.52 8 2 2.169e-3 768 93460 0.4792 1.66e9 50.63 1.29e11 1.13 1.08e10 1.39e21 39.09 84 26 288 2.08e-3 720 87144 0.4825 1.89e9 57.40 1.14e11 1.00 1.22e10 1.39e21 34.61 8 3 2.006e-3 672 82833 0.4816

**Table 17.** Experimental settings and results of loose data reuse for MoE models with N = 6.52B with ﬁxed C. Hyperparameters shared by all experiments: L = 24, S = 2048, Dm = 2048, Dffn = 5464, H = 16, Dh = 128. The green row corresponds to the MoE model with the lowest BPC on the validation set.

Na ra(%) ˆ D M C D/N E K De Dse η B # Iters BPC

7.30e8 11.19 2.56e11 5.59e9 2.86e21 78.47 82 2 512 7.23e-4 185816 0.4591 8.74e8 13.41 2.21e11 6.46e9 2.86e21 67.93 81 3 512 6.92e-4 175482 0.4557 1.02e9 15.63 1.95e11 7.33e9 2.86e21 59.89 80 4 512 6.64e-4 165447 0.4550 1.31e9 20.07 1.58e11 9.07e9 2.87e21 48.50 78 6 512 6.23e-4 150729 0.4549 1.71e9 26.18 1.25e11 1.15e10 2.86e21 38.32 86 10 448 5.80e-4 960 127035 0.4570 1.96e9 30.07 1.10e11 1.30e10 2.86e21 33.83 84 12 448 5.57e-4 792 135956 0.4583

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

F THE USE OF LARGE LANGUAGE MODELS: AN EXPLANATION

Only a small fraction of complex paragraphs are written with the assistance and modiﬁcation of ChatGPT. For instance, we provide the prompt: “I am writing an academic conference paper in the ﬁeld of computer science. Please help me polish the wording of this paragraph, organize the sentences, and express them in a more academic way.” After that the outputs are rigorously reviewed to ensure accuracy and appropriateness.
