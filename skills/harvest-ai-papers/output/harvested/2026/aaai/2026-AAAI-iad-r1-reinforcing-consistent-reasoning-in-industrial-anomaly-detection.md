---
title: "IAD-R1: Reinforcing Consistent Reasoning in Industrial Anomaly Detection"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37588
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37588/41550
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# IAD-R1: Reinforcing Consistent Reasoning in Industrial Anomaly Detection

<!-- Page 1 -->

IAD-R1: Reinforcing Consistent Reasoning in Industrial Anomaly Detection

Yanhui Li1, Yunkang Cao2, Chengliang Liu3, Yuan Xiong1, Xinghui Dong4, Chao Huang1*

## 1 School of Cyber Science and Technology, Sun Yat-sen University Shenzhen Campus 2 School of Artificial Intelligence and

Robotics, Hunan University 3 Department of Computer and Information Science, University of Macau 4 Faculty of Information Science and Engineering, Ocean University of China liyh665@mail2.sysu.edu.cn, caoyunkang0207@gmail.com, liucl1996@163.com, xiongy89@mail.sysu.edu.cn xinghui.dong@ouc.edu.cn, huangch253@mail.sysu.edu.cn

## Abstract

Industrial anomaly detection is a critical component of modern manufacturing, yet the scarcity of defective samples restricts traditional detection methods to scenario-specific applications. Although Vision-Language Models (VLMs) demonstrate significant advantages in generalization capabilities, their performance in industrial anomaly detection remains limited. To address this challenge, we propose IAD- R1, a universal post-training framework applicable to VLMs of different architectures and parameter scales, which substantially enhances their anomaly detection capabilities. IAD- R1 employs a two-stage training strategy: the Perception Activation Supervised Fine-Tuning (PA-SFT) stage utilizes a meticulously constructed high-quality Chain-of-Thought dataset (Expert-AD) for training, enhancing anomaly perception capabilities and establishing reasoning-to-answer correlations; the Structured Control Group Relative Policy Optimization (SC-GRPO) stage employs carefully designed reward functions to achieve a capability leap from “Anomaly Perception” to “Anomaly Interpretation”. Experimental results demonstrate that IAD-R1 achieves significant improvements across 7 VLMs, the largest improvement was on the DAGM dataset, with average accuracy 43.3% higher than the 0.5B baseline. Notably, the 0.5B parameter model trained with IAD-R1 surpasses commercial models including GPT- 4.1 and Claude-Sonnet-4 in zero-shot settings, demonstrating the effectiveness and superiority of IAD-R1.

## Introduction

Industrial anomaly detection serves as a critical component of modern manufacturing quality control, facing challenges including diverse anomaly types, large inter-class variance, and scarce anomaly samples (Bae, Lee, and Kim 2023; Liu et al. 2024b; Roth et al. 2022; Jeong et al. 2023). The complexity and diversity of anomaly patterns make building universal detection models extremely challenging. Traditional methods primarily rely on hand-crafted feature extractors and domain-specific expert knowledge (You et al. 2022; He et al. 2024; Li et al. 2024d; Zhu and Pang 2024), but these approaches are often limited to single product categories, severely lacking generalization capabilities.

*Corresponding Author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

In recent years, Vision-Language Models (VLMs) have provided new possibilities for solving industrial anomaly detection problems through their powerful multimodal understanding and generalization capabilities (Li et al. 2025a; Jin et al. 2025; Li et al. 2025b; Zeng et al. 2025; Jiang et al. 2024). Researchers have primarily adopted two strategies to apply VLMs to anomaly detection: (1) Using traditional anomaly detection methods as visual anomaly experts, feeding their generated anomaly localization results along with prompt text and test images into VLMs for judgment (Gu et al. 2024b; Li et al. 2023; Xu et al. 2025; Chen et al. 2025); (2) Based on question-answering anomaly detection datasets, directly adapting VLMs to industrial anomaly detection tasks through post-training techniques such as supervised fine-tuning or reinforcement learning (Chao et al. 2025; Zeng et al. 2025; Li et al. 2025b). However, both strategies suffer from fundamental limitations. The anomaly expert-assisted approach has overall performance constrained by the capability ceiling of the selected anomaly expert, making it difficult to breakthrough the bottlenecks of traditional methods. End-to-end finetuning methods, while avoiding dependence on traditional algorithms, face deeper issues: existing training data lacks high-quality reasoning process annotations, leading models to learn only simple input-output mappings without mastering the intrinsic logic of anomaly analysis. More critically, traditional supervised fine-tuning easily leads to cognitive rigidity, while existing reinforcement learning methods, due to coarse reward design, frequently exhibit inconsistency between reasoning processes and final answers.

Successful experiences in general domains (Guo et al. 2025; Shen et al. 2025) demonstrate that high-quality chainof-thought (CoT) (Wei et al. 2022) data and reinforcement learning strategies can improve model reasoning capabilities. However, the exploration of the R1-style methods in the anomaly detection domain remains insufficient, lacking high-quality CoT datasets for this task and specifically designed reinforcement learning objectives.

To address these issues, we propose IAD-R1, a two-stage post-training framework specifically designed for industrial anomaly detection, aimed at addressing the scarcity of highquality CoT data and the lack of reasoning-answer consistency in existing models. As shown in Figure 1, we con-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

<!-- Page 2 -->

Interpretation Perception

IAD-R1

PA- SFT Initial Model

IAD-R1

(ours) High quality COT dataset

A1: 1.00 A2: 1.25 ……: 0.50 An: 0.90

KL

SC-GRPO

𝑅𝑐𝑜𝑛𝑅𝑙𝑜𝑐 𝑅𝑡𝑦𝑝𝑒𝑅𝑎𝑐𝑐

Damage

……

Are there any defects in this query image?

Query image

<think>...</think><location>top </location><type>contaminatio n</type><answer>yes</answer>

Anomaly type Expert-AD dataset

IAD-R1(ours) Answer: <think>Upon examining the provided zippered fabric sample……, it is evident that deformation has occurred at one point along the central section of this section. The teeth appear misaligned compared to their usual straight alignment seen in the normal image...... making it difficult for users to smoothly operate their zippers……Therefore, further investigation into production processes……</think> <location>center</location><type>Deformation</type><answer>Yes</answer>

Claude-Sonnet-4 Answer: No, I don't observe any obvious defects. Looking at this image of what appears to be a zipper, I can see the zipper teeth/coils and the fabric tape on either side. The zipper appears to be functioning normally with the teeth properly aligned and interlocked.

Question: Are there any defects in the test image?

GT: Yes

GPT-4o Claude-Sonnet-4 Qwen2.5-VL-72B GPT-4.1 ours 100

90

80

70

## 60 MVTec

VisA DAGM DTD SDD MPDD

0-shot 1-shot +SC-GRPO +PA-SFT Base

VisA MVTec

LLaVA-

1.5-7B LLaVA-1.6

-8B

Qwen2-VL

-2B

Qwen2.5-VL

-3B

Qwen2.5-

VL-7B

LLaVA-

1.5-7B

LLaVA-1.6

-8B

Qwen2-VL

-2B

Qwen2.5-VL

-3B

Qwen2.5-

VL-7B LLaVA-

1.5-7B LLaVA-1.6

-8B

Qwen2-VL

-2B

Qwen2.5-VL

-3B

Qwen2.5-

VL-7B

LLaVA-

1.5-7B

LLaVA-1.6

-8B

Qwen2-VL

-2B

Qwen2.5-VL

-3B

Qwen2.5-

VL-7B

Base Model +PA-SFT +SC-GRPO +24.0%

+19.5%

+30.8%

+24.3%

MVTec(0/1-shot) VisA(0/1-shot) 100 200300400 500 Steps

Acc%

SC-GRPO(MVTec) SC-GRPO(VisA)

PA-SFT(VisA) PA-SFT(MVTec)

80 75 70 65 60 55

80

70

60

50

**Figure 1.** Overview of IAD-R1. The top left panel illustrates the composition of the Expert-AD and the two-stage training framework of IAD-R1. The bottom left panel shows an output example of IAD-R1 for anomaly detection. The right panels present quantitative analyses showcasing the performance of IAD-R1 across different model configurations and datasets.

struct the Expert-AD (totaling 5.9K QA pairs) dataset, the first industrial anomaly detection dataset containing highquality CoT reasoning. Its CoT template follows a progressive three-layer approach of spatial perception, knowledgedriven analysis, and comprehensive decision-making to systematically simulate the expert anomaly detection process. Inspired by successful two-stage training experiences in DeepSeek-R1 (Guo et al. 2025), we propose the Perception Activation Supervised Fine-Tuning Strategy (PA-SFT) and Structured Control Group Relative Policy Optimization (SC-GRPO) strategies. Targeting the specificity of industrial anomaly detection, we design multi-dimensional reward functions: Racc, Rloc, Rtype, and Rcon to achieve refined optimization of model reasoning processes, thereby enhancing the model’s anomaly understanding capabilities.

Extensive experimental results demonstrate that IAD-R1 can significantly improve anomaly detection performance across different backbones, achieving up to 43.3% average accuracy. Notably, small parameter models (0.5B) trained with IAD-R1 not only outperform larger baseline models (72B) in zero-shot settings but also surpass advanced commercial models such as GPT-4.1 (OpenAI 2025) and Claude-Sonnet-4 (Anthropic 2025), validating the superior parameter efficiency and performance advantages of our method. IAD-R1 effectively addresses the key problem of insufficient generalization capability in traditional methods, providing an efficient and universal solution for practical applications of VLMs in industrial anomaly detection. Our main contributions are summarized as follows:

• We construct the first industrial anomaly detection dataset Expert-AD containing high-quality CoT reasoning, providing crucial data support for training.

• We propose IAD-R1, a two-stage post-training framework suitable for industrial anomaly detection, which guides models to achieve a capability leap from “Anomaly Perception” to “Anomaly Interpretation” through PA-SFT and SC-GRPO.

• Extensive experiments validate the effectiveness and universality of IAD-R1, providing an efficient solution for VLMs applications in industrial anomaly detection.

## Related Work

Traditional Industrial Anomaly Detection

Due to the challenge of scarce anomaly samples in industrial anomaly detection, researchers utilize a small number of normal samples as auxiliary datasets for training and testing. WinCLIP (Jeong et al. 2023) pioneered the application of CLIP (Radford et al. 2021) to industrial anomaly detection by computing the similarity between handcrafted text prompts and test images to achieve defect detection. Addressing the complexity of manual prompt design, PromptAD (Li et al. 2024c) simplified text prompt design through semantic connections to construct negative samples and explicit anomaly boundaries. In contrast, One-to-Normal (Li

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-002-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

et al. 2024e) provided visual support for detection by performing one-to-one normal transformations on query images through an anomaly-free generative model. Considering the unpredictability of anomaly categories in production environments (Deng et al. 2023; Ma et al. 2025; Qu et al. 2024, 2025; Gu et al. 2024a), AnomalyCLIP (Zhou et al. 2023) achieved zero-shot anomaly detection by learning objectagnostic text prompts. AdaCLIP (Cao et al. 2024) further enhanced anomaly detection capabilities by learning dynamic prompts for both text and images.

VLMs on Industrial Anomaly Detection

With the emergence of VLMs (Zhang et al. 2024; Yin et al. 2024; Wu et al. 2023), researchers have begun exploring the utilization of their powerful generalization capabilities for industrial anomaly detection (Li et al. 2025b; Chen et al. 2025; Jiang et al. 2024; Li et al. 2025a; Jin et al. 2025; Kwon et al. 2025; Zeng et al. 2025). AnomalyGPT (Gu et al. 2024b) adapted to anomaly detection tasks by generating training data through simulated anomaly images and finetuning the model using image decoders and prompt learners. However, due to the modality gap between textual and visual domains, Myriad (Li et al. 2023) further introduced anomaly maps generated by visual experts to guide the model’s attention toward anomalous regions. Addressing the requirements of zero-shot scenarios, Anomaly-OV (Xu et al. 2025) achieved more precise zero-shot anomaly detection through feature matching mechanisms that adaptively select and emphasize anomalous visual tokens.

## Methodology

Problem Definition

In this study, we focus on zero-shot and one-shot scenarios for industrial anomaly detection, where training and testing adopt different data distribution settings. Specifically, our problem formulation is as follows. Training Phase. We adopt a zero-shot training paradigm, where training data comes entirely from our constructed auxiliary dataset Expert-AD, containing no samples from the target test domain. Testing Phase. We conduct evaluations under two settings on the target domain:

• Zero-shot testing: The model receives only text prompts p and the image to be detected Itest as input, outputting model reasoning and anomaly detection results. • One-shot testing: In addition to text prompts p and test images Itest, the model additionally receives a normal reference image Iref from the same product category as contextual information, with the output being model reasoning and anomaly detection results.

Expert-AD Dataset

The field of industrial anomaly detection lacks high-quality prompt tuning datasets, severely hindering the application of VLMs in this downstream task. Although Anomaly-Instruct- 125k proposed by Anomaly-OV (Xu et al. 2025) contains a substantial amount of instruction tuning data, the webcrawled data differs significantly from real industrial images in practical scenarios. Moreover, these prompts only include image descriptions and answers, failing to help models develop a complete logic for anomaly inspection. To bridge this gap, we create Expert-AD, a high-quality real industrial scenario tuning dataset containing CoT reasoning.

The core innovation of Expert-AD lies in the construction of a systematic anomaly detection reasoning framework that implements structured anomaly detection reasoning through observation, comparison, identification, evaluation, and decision-making stages. This reasoning process comprises three core layers: the basic perception layer achieves precise localization of anomaly positions through spatial scanning and key component positioning; the knowledgedriven analysis layer combines industrial standard knowledge to identify anomaly types from dimensions of appearance integrity, surface quality, and structural integrity; the comprehensive decision layer provides final judgments on anomaly existence and evaluates their impact. Based on this reasoning framework, we adopt a two-stage training strategy: the PA-SFT stage trains anomaly perception capabilities through QA pairs containing detailed CoT, establishing mappings between structured reasoning processes and detection results; the SC-GRPO stage enhances the model’s analytical and decision-making accuracy in complex scenarios through fine-grained reward function design. In total, our Expert-AD comprises 2.9K QA pairs for PA-SFT stage and 3K QA pairs for SC-GRPO stage.

IAD-R1 In this paper, we propose IAD-R1, a two-stage post-training framework specifically designed for industrial anomaly detection. As shown in Figure 2, IAD-R1 comprises two progressive stages: (1) PA-SFT stage, which employs supervised fine-tuning on Expert-AD CoT data to enable the model to acquire structured anomaly analysis thinking patterns and establish effective associations between reasoning processes and detection results; (2) SC-GRPO stage, which guides the model to break through simple pattern memorization, achieving more flexible and accurate anomaly analysis decisions through multi-dimensional reward functions.

Perception Activation Supervised Fine-Tuning In the PA-SFT stage, we activate the model’s anomaly perception potential through supervised fine-tuning on the Expert-AD dataset. Training samples adopt a triplet format (I, p, O), where I represents the industrial image, p denotes the text prompt, and O is the conditional output sequence. Through high-quality CoT data training, the model learns to identify anomaly patterns from visual features and generates outputs with different structures based on image content. For normal images, O = (T, A), containing the CoT reasoning process T and final answer A; for anomalous images, O = (T, L, t, A), containing the CoT reasoning process T, anomaly location L, anomaly type t, and final answer A. This training approach ensures that the model can produce logically coherent structured outputs when processing both normal and anomalous images, avoiding contradictions between the reasoning process and final conclusions. The training objective maximizes the conditional probability of gen-

<!-- Page 4 -->

SC-GRPO Reward (1) Consistency Reward Abnormal: <think></think> <location></location> <type></type> <answer></answer>

Normal: <think></think> <answer></answer>

𝑅con = 0, Consistent 1, Not

(2) Accuracy Reward

𝑅acc = 1, Answer = GT 0, Otherwise

(3) Location Reward

𝑅loc = 1, Location = GT 0, Otherwise

Initial: (2,2) Left: (,y-1) Right: (,y+1) Top: (x-1,) Bottom: (x+1,)

(4) Type Reward

𝑅𝑡𝑦𝑝𝑒= 1, Exact match

0.85, Semantic match

0.6, Category match

0.4, Fuzzy match

0.3, Group match

0, Otherwise

Damage

……

Anomaly Perception

……

Pretrained VLMs

Initial Policy Model

Are there any defects in this query image?

Query image

<think>...</think><location>top </location><type>Contaminatio n</type><answer>yes</answer>

Reference Policy Model

Are there any defects in this query image?

Query image

<location>top</location> <type>Contamination</t ype> <answer>yes</answer>

RL-Stage Data

IAD-R1 Policy Model KL divergence

SC-GRPO

Candidate Responses

Policy Gradient Update Reward Function

Anomaly Interpretation

Consistency

Reward

Type Reward

Accuracy

Reward

Location

Reward

**Figure 2.** Architecture of IAD-R1. IAD-R1 employs a progressive two-stage training strategy: First, in the PA-SFT stage, supervised fine-tuning is conducted on pre-trained VLMs using CoT reasoning samples from the Expert-AD dataset to enhance the model’s anomaly perception capabilities and establish structured reasoning pathways; Subsequently, in the SC-GRPO stage, reward functions across four dimensions (consistency, accuracy, location, and type) are designed as reinforcement learning objectives to optimize the policy model, thereby improving its anomaly detection and understanding capabilities.

erating the output sequence given the image and prompt:

LPA-SFT = −E(I,p,O)∼DExpert-AD

L X i=1 log πθ(oi|I, p, o<i), (1)

where DExpert−AD is the Expert-AD dataset, oi is the i-th token in the output sequence O, L is the sequence length, and πθ denotes the parameterized model. The trained model serves as the initial policy model for the SC-GRPO stage.

Structured Control Group Relative Policy Optimization We utilize the model πP A−SF T, obtained through PA-SFT training, as the initial policy model. Targeting the unique characteristics of industrial anomaly detection tasks, we develop an optimized SC-GRPO algorithm. Through carefully designed multi-dimensional reward functions, we achieve consistency between model reasoning and answers while enhancing overall detection accuracy. Multi-dimensional Reward Function Design. The core innovation of SC-GRPO lies in the multi-dimensional reward function specifically designed for industrial anomaly detection tasks, comprising four key components. Consistency Reward Function. The consistency reward function Rcon enhances semantic consistency between model reasoning and detection conclusions by enforcing structured output formats that align with anomaly detection results. We define two standard output patterns corresponding to different anomaly states. For normal images, the output follows the Normal Pattern Pnormal, containing only the reasoning process and final answer:

Pnormal = ⟨think⟩...⟨/think⟩⟨answer⟩...⟨/answer⟩.

For anomalous images, the output follows the Anomalous Pattern Pabnormal, which includes complete structured in- formation to maintain reasoning consistency:

Pabnormal = ⟨think⟩...⟨/think⟩⟨location⟩...⟨/location⟩

⟨type⟩...⟨/type⟩⟨answer⟩...⟨/answer⟩.

Given model output oi and corresponding ground truth label yi, the consistency reward function is defined as:

Rcon(oi) =

(

1, if Match(oi, P) 0, otherwise, (2)

where Match(oi, P) is a pattern matching function that uses regular expressions to verify whether output oi strictly conforms to the format requirements of pattern P. Answer Accuracy Reward Function. The answer accuracy reward function Racc is used to evaluate the correctness of the model’s final anomaly judgment and serves as the core reward signal in the reinforcement learning process. This function directly compares the model’s predicted answer and ground truth label. Given the model’s predicted answer apred and the ground truth answer label agt, the answer accuracy reward function is defined as:

Racc(apred, agt) =

(

1, if apred = agt 0, otherwise. (3)

This function ensures that rewards are only obtained when the model provides correct anomaly judgments (“Yes” or “No”), providing a prerequisite condition for subsequent location and type classification rewards. Location Accuracy Reward Function. The location accuracy reward function Rloc is used to evaluate the accuracy of the model’s anomaly location. This function maps location description text to a standardized 3 × 3 spatial grid we

![Figure extracted from page 4](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-004-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

established for comparison, converting textual descriptions into corresponding grid position numbers by parsing location keywords (such as “left,” “right,” “top,” “bottom,” etc.). Given the model’s predicted location description lpred and the ground truth location label lgt, the location accuracy reward function is defined as:

Rloc(lpred, lgt) =

(

1, if Φ(lpred) = Φ(lgt) 0, otherwise, (4)

where Φ(·) represents the text-to-grid position mapping function, which provides rewards when the predicted location matches the ground truth location. Type Accuracy Reward Function. The type accuracy reward function Rtype is used to evaluate the accuracy of the model’s anomaly type classification. Considering the diversity and semantic complexity of type descriptions in industrial anomaly detection, using only string matching strategies is overly restrictive and may lead to sparse rewards for the model during the reinforcement learning process, affecting training stability. Therefore, we design a multi-level matching mechanism to improve the stability of reinforcement learning and encourage the model to explore diverse output expressions. Given the matching degree between the predicted type tpred and the ground truth type tgt, the type accuracy reward function is defined as:

Rtype(tpred, tgt) =

        

       

1.0, if exact match 0.85, if semantic match 0.6, if category match 0.4, if fuzzy match 0.3, if group match 0, otherwise

. (5)

Relative Advantage Computation. Our SC-GRPO strategy employs intra-group reward normalization to compute relative advantages between responses. This design avoids the training overhead of value function networks in Proximal Policy Optimization (Schulman et al. 2017) while maintaining optimization effectiveness:

Ai = RSC-GRPO(oi) −mean{RSC-GRPO(oj)}G j=1 std{RSC-GRPO(oj)}G j=1

. (6)

## Experiment

## Experiment

Setup Evaluation Details. To evaluate the performance of IAD- R1, we select six representative datasets encompassing two major categories: industrial objects (MVTec-AD (Bergmann et al. 2019), VisA (Zou et al. 2022), MPDD (Jia et al. 2022)) and surface textures (DAGM (Wieler and Hahn 2007), DTD (Aota, Tong, and Okatani 2023), SDD (Tabernik et al. 2020)), to simulate complex real-world industrial production scenarios. Considering that overall accuracy is prone to evaluation bias under data imbalance conditions, we adopt balanced accuracy as our evaluation metric. For IAD-R1 models, we extract answers from the structured output tags ⟨answer⟩...⟨/answer⟩; for baseline models, we directly obtain their output answers for comparison. Implementation Details. To validate the generalizability of IAD-R1, We employ seven VLMs with diverse architectures and sizes as backbones, including Qwen2-VL-2B (Wang et al. 2024), Qwen2.5-VL (3B, 7B) (Bai et al. 2025), LLaVA-1.5-7B (Liu et al. 2024a), LLaVA-OneVision-SI (0.5B, 7B) (Li et al. 2024a), and LLaVA-1.6-8B (Li et al. 2024b). All experiments are conducted on 4×A100 GPUs.

Main Results Model Comparison. As shown in Table 1, IAD-R1(LLaVA- OneVision-SI-7B) achieved the highest average accuracy of 86.1%, representing improvements of 7.2% and 7.8% over the best open-source model Anomaly-OV (Xu et al. 2025) and commercial model GPT-4.1 (OpenAI 2025), respectively. Notably, small-parameter models trained with IAD-R1 demonstrated exceptional performance: the IAD-R1(Qwen2.5-VL-Instruct-3B) model surpassed the 72B model of the same series by 4.5%, while the IAD-R1(LLaVA-OneVision-SI-0.5B) even outperformed all open-source and commercial models. These results indicate that IAD-R1 is more effective than simply increasing parameters, providing a parameter-efficient solution for industrial applications in resource-constrained environments.

Ablation Results Ablation on Data Activation Method. To verify the role of CoT responses on model performance, we compare different data preparation methods during the PA-SFT stage. As shown in Table 2, “Expert-AD” refers to fine-tuning with our Expert-AD dataset containing complete structured reasoning processes, and “Original” refers to fine-tuning with the same questions but using direct answers only. Using Expert- AD data in the PA-SFT stage significantly outperforms original data, with this result being validated across all three models. Notably, fine-tuning with original data even exhibits performance degradation in some cases, indicating that simple question-answer training may lead to inadequate learning or overfitting, while the CoT responses in Expert-AD can guide models to learn deeper anomaly analysis logic. Ablation on Reward Strategy. To verify the importance of multi-dimensional reward functions, we compare SC- GRPO and the original reward strategy on three models finetuned with PA-SFT, where the original reward strategy employs only the correctness of final answers as the reward signal. As shown in Table 3, experimental results demonstrate that SC-GRPO significantly outperforms the original reward strategy across all models. The original reward strategy exhibits performance degradation primarily because its single reward design easily leads to sparse reward problems and cannot distinguish between “correct answers with clear reasoning” and “correct answers with chaotic reasoning”. In contrast, SC-GRPO provides more refined optimization guidance through multi-dimensional reward mechanisms, achieving more stable reinforcement learning optimization. Table 5 presents an ablation study of the contribution of each reward function in SC-GRPO. Each individual reward function makes a meaningful contribution to the overall performance. Furthermore, the integration of all reward functions achieves optimal performance across different datasets. Discussion about Grid Size. Figure 3 demonstrates the impact of grid partition size in the location accuracy reward

<!-- Page 6 -->

Type Model Parameter Industrial Workpieces Surface Texture Average MVTec MPDD VisA DAGM DTD SDD

Commercial

GPT-4o-mini / 71.3 67.9 65.1 72.6 79.5 66.6 70.5 GPT-4o / 69.6 60.3 63.5 63.0 69.9 65.7 65.3 GPT-4.1-nano / 74.7 61.7 60.5 62.4 78.3 50.0 64.6 GPT-4.1-mini / 74.0 69.8 63.4 70.7 82.1 72.1 72.0 GPT-4.1 / 81.9 66.7 69.1 81.8 90.1 79.9 78.3 Claude-Sonnet-4 / 67.6 65.9 63.5 69.2 88.4 81.7 72.7

Open Source

LLaVA-OneVision-SI 0.5B 50.0 50.0 50.0 50.0 54.3 50.0 50.7 Anomaly-OV[CVPR 2025] 0.5B 50.0 50.0 50.0 50.0 53.8 50.0 50.6 Qwen2.5-VL-Instruct 3B 62.6 52.9 58.4 54.2 64.4 50.3 57.1 AnomalyR1[arxiv 2025] 3B 69.4 56.0 59.8 56.7 61.0 57.6 60.1 InternVL-2.5 4B 56.6 59.1 53.7 57.7 81.3 64.1 62.1 Qwen2.5-VL-Instruct 7B 66.0 56.0 58.4 57.7 59.2 67.4 60.8 AnomalyGPT[AAAI 2024] 7B 46.6 54.2 57.3 49.6 64.1 49.5 53.6 LLaVA-OneVision-SI 7B 82.0 57.0 59.6 75.4 76.8 55.1 67.7 Anomaly-OV[CVPR 2025] 7B 74.3 70.3 74.3 77.5 90.7 88.7 78.9 LLaVA-1.5 13B 61.4 61.4 67.2 50.4 75.9 50.0 61.1 LLaVA-1.6 34B 53.7 50.0 53.9 50.0 52.7 50.0 51.7 Qwen2.5-VL-Instruct 72B 77.4 64.7 68.2 77.9 81.9 69.0 73.2

IAD-R1

IAD-R1(LLaVA-OneVision-SI) 0.5B 81.0 69.4 74.9 93.3 95.5 88.6 83.8 IAD-R1(Qwen2.5-VL-Instruct) 3B 77.6 59.2 69.8 86.0 89.1 84.5 77.7 IAD-R1(Qwen2.5-VL-Instruct) 7B 81.9 65.8 75.4 85.2 90.8 83.4 80.4 IAD-R1(LLaVA-OneVision-SI) 7B 86.7 70.9 78.0 94.8 96.2 90.1 86.1

**Table 1.** Performance comparison of different models on industrial workpieces and surface texture benchmarks. The best results are highlighted in bold, while the second-best results are underlined.

## Model

Data 0-shot 1-shot Average

LLaVA-OneVision-SI

(0.5B)

Base 50.7 50.0 50.4 Original 50.9 50.0 50.5 Expert-AD 82.7 69.5 76.1

Qwen2.5-VL-Instruct

(3B)

Base 57.1 60.3 58.7 Original 65.8 59.5 62.7 Expert-AD 73.1 73.5 73.3

LLaVA-OneVision-SI

(7B)

Base 67.7 60.6 64.2 Original 68.4 62.3 65.4 Expert-AD 85.9 74.9 80.4

**Table 2.** Results of different data preparation in PA-SFT.

function on model performance (left: LLaVA-OneVision-SI- 0.5B;right: Qwen2-VL-Instruct-2B). The 3×3 grid partition achieves optimal performance, providing sufficient anomaly localization details while avoiding noise interference from overly fine-grained partitioning. Model Promotion. Table 4 provides a detailed presentation of the gains brought by IAD-R1 relative to the backbone across different test settings and datasets. The PA-SFT stage significantly activates the anomaly perception capabilities, while the SC-GRPO stage further optimizes output quality. Across the parameter range from 0.5B to 8B, all tested models in the Qwen and LLaVA series achieved significant performance improvements from the two-stage training, validating the broad applicability of IAD-R1 as a general industrial anomaly detection post-training framework. Notably, IAD-R1 demonstrates more pronounced improvement ef-

## Model

Strategy 0-shot 1-shot Average

LLaVA-OneVision-SI

(0.5B)

Fine-tuned 82.7 69.5 76.1 Original 78.1 59.0 68.6 SC-GRPO 83.8 68.8 76.3

Qwen2.5-VL-Instruct

(3B)

Fine-tuned 73.1 73.5 73.3 Original 70.0 71.9 71.0 SC-GRPO 77.7 76.4 77.1

LLaVA-OneVision-SI

(7B)

Fine-tuned 85.9 74.9 80.4 Original 78.5 65.8 72.2 SC-GRPO 86.1 75.8 81.0

**Table 3.** Results of different reward strategy in SC-GRPO.

fects in 0-shot scenarios, which aligns with our training design using single-image data. Analysis of Reasoning and Answer Consistency. Figure 4 illustrates the performance of different models. Qwen3 (Yang et al. 2025) provides incorrect answers, although Claude-Sonnet-4 (Anthropic 2025) produces the correct answer, it exhibits flawed reasoning processes. IAD-R1 not only delivers the correct answer but also ensures consistency between the reasoning process and the final answer.

## Conclusion

In this paper, we propose IAD-R1 to address key challenges faced by VLMs in industrial anomaly detection. We construct the Expert-AD dataset, contributing the first highquality CoT reasoning data resource for this domain. Additionally, we design PA-SFT and SC-GRPO methods, achiev-

<!-- Page 7 -->

## Model

Parameter

Strategy 0-shot 1-shot

PA-SFT SC-GRPO MVTec DAGM DTD SDD MPDD VisA MVTec VisA

LLaVA-OneVision-SI 0.5B 50.0 50.0 54.3 50.0 50.0 50.0 50.0 49.9 ✓ 79.4 91.3 96.0 90.7 65.3 73.4 72.6 66.4 ✓ ✓ 81.0 93.3 95.5 88.6 69.4 74.9 70.8 66.8

Qwen2-VL-Instruct 2B 63.5 54.3 59.3 57.2 55.0 59.6 69.9 59.6 ✓ 73.5 65.4 81.6 56.3 59.3 58.8 77.0 60.4 ✓ ✓ 77.3 73.8 84.0 62.8 69.5 67.7 78.5 69.7

Qwen2.5-VL-Instruct

3B 62.6 54.2 64.4 50.3 52.9 58.4 60.9 59.6 ✓ 73.3 82.8 87.7 76.3 53.4 65.1 75.9 71.0 ✓ ✓ 77.6 86.0 89.1 84.5 59.2 69.8 78.6 74.1

7B 66.0 57.7 59.2 67.4 56.0 58.4 81.0 69.8 ✓ 78.2 83.8 88.0 80.4 63.9 70.4 82.6 70.5 ✓ ✓ 81.9 85.2 90.8 83.4 65.8 75.4 85.5 77.4

LLaVA-1.5 7B 67.4 63.7 79.3 58.8 62.0 71.1 59.8 53.6 ✓ 78.1 69.6 84.0 83.9 60.9 69.8 76.1 67.2 ✓ ✓ 79.4 75.4 86.7 83.6 62.3 72.9 77.8 71.8

LLaVA-OneVision-SI 7B 82.0 75.4 76.8 55.1 57.0 59.6 67.5 53.7 ✓ 86.7 94.3 96.1 89.5 70.5 78.0 79.3 70.4 ✓ ✓ 86.7 94.8 96.2 90.1 70.9 78.0 80.0 71.5

LLaVA-1.6 8B 62.7 52.0 73.6 50.0 66.2 56.7 51.5 52.6 ✓ 83.1 73.4 80.0 69.4 66.2 68.2 80.1 63.7 ✓ ✓ 84.7 79.0 88.0 84.5 64.1 70.4 78.0 64.4

**Table 4.** Performance gains from using IAD-R1 on VLMs with different architectures and parameter scales.

Accuracy

MVTec VisA MPDD SDD DAGM DTD

1*1 2*2 3*3 4*4 5*5 1*1 2*2 3*3 4*4 5*5

98

91

84

77

70

63

85

75

65

55

45

**Figure 3.** Ablation on grid size.

Rcon Rloc Rtype MVTec VisA DAGM MPDD SDD DTD

72.7 59.0 72.5 55.5 79.3 81.0 ✓ 76.3 66.3 83.9 57.9 77.4 88.4 ✓ 77.4 67.0 84.8 57.9 81.6 88.1 ✓ ✓ 75.4 67.0 85.8 58.6 79.5 90.0 ✓ ✓ 76.7 67.5 85.1 56.5 80.8 89.1 ✓ ✓ ✓ 77.6 69.8 85.2 59.2 83.4 89.1

**Table 5.** Ablation of reward function contributions.

ing a leap from “Anomaly Perception” to “Anomaly Interpretation”. Experimental results demonstrate that IAD-R1 achieves significant performance improvements over baseline models across all benchmark datasets, providing a viable and effective technical pathway for advancing VLM applications in industrial anomaly detection scenarios.

## Acknowledgments

This work was supported in part by the National Natural Science Foundation of China (No.62301621), Shenzhen Science and Technology Program (No. 20231121172359002,

Question: Are there any defects in the test image?

GT：YES

Qwen3

IAD-R1(ours)

Claude-Sonnet-4

The image shows a screw, and upon visual inspection, there are no obvious defects such as cracks, bends, or missing threads. However, the tip of the screw appears slightly damaged or worn, which could be considered a defect depending on the intended use and quality standards. For a more thorough analysis, especially in terms of material integrity and precise measurements, specialized equipment and tests would be necessary.

Looking at this screw in the image, I can see what appears to be some surface irregularities or potential defects. There seem to be some spots or marks on the screw's surface that could indicate corrosion, staining, or manufacturing defects. The head of the screw and parts of the threaded shaft show some discoloration or surface imperfections. Yes, there appear to be defects in this test image. <think>During my thorough inspection of this screw, focusing particularly on its right side due to prior guidance regarding expected locations…… Upon closer observation near the upper-right section, it appears there‘s evidence suggesting some form of damage has occurred—possibly indicating wear or fracture at those specific points along the thread pattern. This irregularity stands out against our established standards which require smooth continuity across all components without visible anomalies like cracks or deformities. Therefore …… requiring further investigation into potential causes leading up until now observed state. </think> <location>right</location> <type>Damage</type><answer>Yes</answer>

**Figure 4.** Comparison of model output.

2023A008), Shenzhen General Research Project (No. JCYJ20241202125904007), and Guangdong Basic and Applied Basic Research Foundation (No. 2025A1515011398).

![Figure extracted from page 7](2026-AAAI-iad-r1-reinforcing-consistent-reasoning-in-industrial-anomaly-detection/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## References

Anthropic. 2025. Introducing Claude 4. https://www. anthropic.com/news/claude-4. Accessed: 2025-07-28. Aota, T.; Tong, L. T. T.; and Okatani, T. 2023. Zero-shot versus many-shot: Unsupervised texture anomaly detection. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 5564–5572. Bae, J.; Lee, J.-H.; and Kim, S. 2023. Pni: industrial anomaly detection using position and neighborhood information. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 6373–6383. Bai, S.; Chen, K.; Liu, X.; Wang, J.; Ge, W.; Song, S.; Dang, K.; Wang, P.; Wang, S.; Tang, J.; et al. 2025. Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923. Bergmann, P.; Fauser, M.; Sattlegger, D.; and Steger, C. 2019. MVTec AD–A comprehensive real-world dataset for unsupervised anomaly detection. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 9592–9600. Cao, Y.; Zhang, J.; Frittoli, L.; Cheng, Y.; Shen, W.; and Boracchi, G. 2024. Adaclip: Adapting clip with hybrid learnable prompts for zero-shot anomaly detection. In European Conference on Computer Vision, 55–72. Springer. Chao, Y.; Liu, J.; Tang, J.; and Wu, G. 2025. Anomalyr1: A grpo-based end-to-end mllm for industrial anomaly detection. arXiv preprint arXiv:2504.11914. Chen, Z.; Chen, H.; Imani, M.; and Imani, F. 2025. Can multimodal large language models be guided to improve industrial anomaly detection? arXiv preprint arXiv:2501.15795. Deng, H.; Zhang, Z.; Bao, J.; and Li, X. 2023. Anovl: Adapting vision-language models for unified zero-shot anomaly localization. arXiv preprint arXiv:2308.15939, 2(5). Gu, Z.; Zhu, B.; Zhu, G.; Chen, Y.; Li, H.; Tang, M.; and Wang, J. 2024a. Filo: Zero-shot anomaly detection by finegrained description and high-quality localization. In Proceedings of the 32nd ACM International Conference on Multimedia, 2041–2049. Gu, Z.; Zhu, B.; Zhu, G.; Chen, Y.; Tang, M.; and Wang, J. 2024b. Anomalygpt: Detecting industrial anomalies using large vision-language models. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 1932–1940. Guo, D.; Yang, D.; Zhang, H.; Song, J.; Zhang, R.; Xu, R.; Zhu, Q.; Ma, S.; Wang, P.; Bi, X.; et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948. He, H.; Zhang, J.; Chen, H.; Chen, X.; Li, Z.; Chen, X.; Wang, Y.; Wang, C.; and Xie, L. 2024. A diffusion-based framework for multi-class anomaly detection. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 8472–8480. Jeong, J.; Zou, Y.; Kim, T.; Zhang, D.; Ravichandran, A.; and Dabeer, O. 2023. Winclip: Zero-/few-shot anomaly classification and segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 19606–19616.

Jia, M.; Tang, L.; Chen, B.-C.; Cardie, C.; Belongie, S.; Hariharan, B.; and Lim, S.-N. 2022. Visual prompt tuning. In European conference on computer vision, 709–727. Springer. Jiang, X.; Li, J.; Deng, H.; Liu, Y.; Gao, B.-B.; Zhou, Y.; Li, J.; Wang, C.; and Zheng, F. 2024. Mmad: A comprehensive benchmark for multimodal large language models in industrial anomaly detection. arXiv preprint arXiv:2410.09453. Jin, E.; Feng, Q.; Mou, Y.; Lakemeyer, G.; Decker, S.; Simons, O.; and Stegmaier, J. 2025. Logicad: Explainable anomaly detection via vlm-based text feature extraction. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 4129–4137. Kwon, Y.; Moon, D.; Oh, Y.; and Yoon, H. 2025. LogicQA: Logical Anomaly Detection with Vision Language Model Generated Questions. arXiv preprint arXiv:2503.20252. Li, B.; Zhang, Y.; Guo, D.; Zhang, R.; Li, F.; Zhang, H.; Zhang, K.; Zhang, P.; Li, Y.; Liu, Z.; et al. 2024a. Llava-onevision: Easy visual task transfer. arXiv preprint arXiv:2408.03326. Li, F.; Zhang, R.; Zhang, H.; Zhang, Y.; Li, B.; Li, W.; Ma, Z.; and Li, C. 2024b. Llava-next-interleave: Tackling multiimage, video, and 3d in large multimodal models. arXiv preprint arXiv:2407.07895. Li, W.; Chu, G.; Chen, J.; Xie, G.-S.; Shan, C.; and Zhao, F. 2025a. Lad-reasoner: Tiny multimodal models are good reasoners for logical anomaly detection. arXiv preprint arXiv:2504.12749. Li, X.; Zhang, Z.; Tan, X.; Chen, C.; Qu, Y.; Xie, Y.; and Ma, L. 2024c. Promptad: Learning prompts with only normal samples for few-shot anomaly detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 16838–16848. Li, Y.; Feng, Y.; Chen, B.; Chen, W.; Wang, Y.; Hu, X.; Qu, C.; Zhou, M.; et al. 2024d. Vague prototype-oriented diffusion model for multi-class anomaly detection. In Forty-first International Conference on Machine Learning. Li, Y.; Wang, H.; Yuan, S.; Liu, M.; Zhao, D.; Guo, Y.; Xu, C.; Shi, G.; and Zuo, W. 2023. Myriad: Large multimodal model by applying vision experts for industrial anomaly detection. arXiv preprint arXiv:2310.19070. Li, Y.; Yuan, S.; Wang, H.; Li, Q.; Liu, M.; Xu, C.; Shi, G.; and Zuo, W. 2025b. Triad: Empowering lmmbased anomaly detection with vision expert-guided visual tokenizer and manufacturing process. arXiv preprint arXiv:2503.13184. Li, Y.; Zhang, S.; Li, K.; and Lao, Q. 2024e. One-to-normal: Anomaly personalization for few-shot anomaly detection. Advances in Neural Information Processing Systems, 37: 78371–78393. Liu, H.; Li, C.; Li, Y.; and Lee, Y. J. 2024a. Improved baselines with visual instruction tuning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 26296–26306. Liu, J.; Xie, G.; Wang, J.; Li, S.; Wang, C.; Zheng, F.; and Jin, Y. 2024b. Deep industrial image anomaly detection: A survey. Machine Intelligence Research, 21(1): 104–135.

<!-- Page 9 -->

Ma, W.; Zhang, X.; Yao, Q.; Tang, F.; Wu, C.; Li, Y.; Yan, R.; Jiang, Z.; and Zhou, S. K. 2025. Aa-clip: Enhancing zeroshot anomaly detection via anomaly-aware clip. In Proceedings of the Computer Vision and Pattern Recognition Conference, 4744–4754. OpenAI. 2025. Introducing GPT-4.1 in the API. https:// openai.com/index/gpt-4-1/. Accessed: 2025-07-28. Qu, Z.; Tao, X.; Gong, X.; Qu, S.; Chen, Q.; Zhang, Z.; Wang, X.; and Ding, G. 2025. Bayesian Prompt Flow Learning for Zero-Shot Anomaly Detection. In Proceedings of the Computer Vision and Pattern Recognition Conference, 30398–30408. Qu, Z.; Tao, X.; Prasad, M.; Shen, F.; Zhang, Z.; Gong, X.; and Ding, G. 2024. Vcp-clip: A visual context prompting model for zero-shot anomaly segmentation. In European Conference on Computer Vision, 301–317. Springer. Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In International conference on machine learning, 8748–8763. PmLR. Roth, K.; Pemula, L.; Zepeda, J.; Sch¨olkopf, B.; Brox, T.; and Gehler, P. 2022. Towards total recall in industrial anomaly detection. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 14318– 14328. Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347. Shen, H.; Liu, P.; Li, J.; Fang, C.; Ma, Y.; Liao, J.; Shen, Q.; Zhang, Z.; Zhao, K.; Zhang, Q.; et al. 2025. Vlm-r1: A stable and generalizable r1-style large vision-language model. arXiv preprint arXiv:2504.07615. Tabernik, D.; ˇSela, S.; Skvarˇc, J.; and Skoˇcaj, D. 2020. Segmentation-based deep-learning approach for surfacedefect detection. Journal of Intelligent Manufacturing, 31(3): 759–776. Wang, P.; Bai, S.; Tan, S.; Wang, S.; Fan, Z.; Bai, J.; Chen, K.; Liu, X.; Wang, J.; Ge, W.; et al. 2024. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint arXiv:2409.12191. Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-ofthought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35: 24824–24837. Wieler, M.; and Hahn, T. 2007. Weakly supervised learning for industrial optical inspection. In DAGM symposium in, volume 6, 11. Wu, J.; Gan, W.; Chen, Z.; Wan, S.; and Yu, P. S. 2023. Multimodal large language models: A survey. In 2023 IEEE International Conference on Big Data (BigData), 2247–2256. IEEE. Xu, J.; Lo, S.-Y.; Safaei, B.; Patel, V. M.; and Dwivedi, I. 2025. Towards zero-shot anomaly detection and reasoning with multimodal large language models. In Proceedings of the Computer Vision and Pattern Recognition Conference, 20370–20382. Yang, A.; Li, A.; Yang, B.; Zhang, B.; Hui, B.; Zheng, B.; Yu, B.; Gao, C.; Huang, C.; Lv, C.; et al. 2025. Qwen3 technical report. arXiv preprint arXiv:2505.09388. Yin, S.; Fu, C.; Zhao, S.; Li, K.; Sun, X.; Xu, T.; and Chen, E. 2024. A survey on multimodal large language models. National Science Review, 11(12): nwae403. You, Z.; Cui, L.; Shen, Y.; Yang, K.; Lu, X.; Zheng, Y.; and Le, X. 2022. A unified model for multi-class anomaly detection. Advances in Neural Information Processing Systems, 35: 4571–4584. Zeng, P.; Pang, F.; Wang, Z.; and Yang, A. 2025. LR-IAD: Mask-Free Industrial Anomaly Detection with Logical Reasoning. arXiv preprint arXiv:2504.19524. Zhang, D.; Yu, Y.; Dong, J.; Li, C.; Su, D.; Chu, C.; and Yu, D. 2024. Mm-llms: Recent advances in multimodal large language models. arXiv preprint arXiv:2401.13601. Zhou, Q.; Pang, G.; Tian, Y.; He, S.; and Chen, J. 2023. Anomalyclip: Object-agnostic prompt learning for zero-shot anomaly detection. arXiv preprint arXiv:2310.18961. Zhu, J.; and Pang, G. 2024. Toward generalist anomaly detection via in-context residual learning with few-shot sample prompts. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 17826–17836. Zou, Y.; Jeong, J.; Pemula, L.; Zhang, D.; and Dabeer, O. 2022. Spot-the-difference self-supervised pre-training for anomaly detection and segmentation. In European conference on computer vision, 392–408. Springer.
