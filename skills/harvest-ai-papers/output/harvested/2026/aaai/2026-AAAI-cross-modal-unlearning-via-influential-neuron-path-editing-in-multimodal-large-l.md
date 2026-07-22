---
title: "Cross-Modal Unlearning via Influential Neuron Path Editing in Multimodal Large Language Models"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40870
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40870/44831
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Cross-Modal Unlearning via Influential Neuron Path Editing in Multimodal Large Language Models

<!-- Page 1 -->

Cross-Modal Unlearning via Influential Neuron Path Editing in Multimodal Large

Language Models

Kunhao Li*1, Wenhao Li*1, Di Wu*2, Lei Yang1†, Jun Bai3, 4, Ju Jia5, Jason Xue6

1School of Software Engineering, South China University of Technology, Guangzhou, China 2School of Computing, Engineering and Mathematical Science, La Trobe University, Melbourne, Australia 3School of Computer Science, McGill University, Montreal, Canada 4Mila-Quebec AI Institute, Montreal, Canada 5School of Cyber Science and Engineering, Southeast University, Nanjing, China 6CSIRO’s Data61 and Responsible AI Research (RAIR) Centre, Adelaide University kunhomlihf@gmail.com, wenhaoli-lwh@outlook.com, d.wu@latrobe.edu.au, sely@scut.edu.cn, jun.bai@mcgill.ca, jiaju@seu.edu.cn, minhuixue@gmail.com

## Abstract

Multimodal Large Language Models (MLLMs) extend foundation models to real-world applications by integrating inputs such as text and vision. However, their broad knowledge capacity raises growing concerns about privacy leakage, toxicity mitigation, and intellectual property violations. Machine Unlearning (MU) offers a practical solution by selectively forgetting targeted knowledge while preserving overall model utility. When applied to MLLMs, existing neuron-editingbased MU approaches face two fundamental challenges: (1) forgetting becomes inconsistent across modalities because existing point-wise attribution methods fail to capture the structured, layer-by-layer information flow that connects different modalities; and (2) general knowledge performance declines when sensitive neurons that also support important reasoning paths are pruned, as this disrupts the model’s ability to generalize. To alleviate these limitations, we propose a multimodal influential neuron path editor (MIP-Editor) for MU. Our approach introduces modality-specific attribution scores to identify influential neuron paths responsible for encoding forget-set knowledge and applies influential-pathaware neuron-editing via representation misdirection. This strategy also enables effective and coordinated forgetting across modalities while preserving the model’s general capabilities. Experimental results demonstrate that MIP-Editor achieves a superior unlearning performance on multimodal tasks, with a maximum forgetting rate of 87.75% and up to 54.26% improvement in general knowledge retention. On textual tasks, MIP-Editor achieves up to 80.65% forgetting and preserves 77.9% of general performance.

Code — https://github.com/PreckLi/MIP-Editor

## Introduction

The rapid advancement of multimodal large language models (MLLMs) has extended model capabilities to a

*These authors contributed equally. †Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Q1. What profession of this individual?

Q2. What profession is Lucas Harrington?

A2. Lucas is a software engineer.

A1. The person is likely a lawyer.

The person is a software engineer. Ground

Truth

Multi Input

Text Input

Forgot (Expected)

Retain (Unexpected)

Q3. What profession of this individual?

A3. The person is an singer.

The person is an art curator. Ground

Truth

Multi Input

Forgot (Unexpected)

General Neuron Influential Neuron Path Pruning

(b)Neuron

Editing

A1. The person is likely a banker. Forgot (Expected)

A2. Lucas is a graphic designer. Forgot (Expected)

A3. The person is an art curator. Retain (Expected)

General Neuron Influential Neuron Path

MIP-Editor

Neuron Updating

Forget-set (Data to forget)

Retain-set (Data to retain)

(a)Fine- tuning

Neuron Updating

**Figure 1.** Comparison between existing MU methods and MIP-Editor. Prior methods suffer from: (1) insufficient forgetting in the text modality, as point-wise attribution fails to capture structured cross-layer information flow; and (2) disruption of influential reasoning paths due to pruning.

wide range of applications through multimodal integration (Zhang et al. 2023; Caffagni et al. 2024). However, their vast knowledge capacity raises serious concerns about privacy leakage (Pi et al. 2024), intellectual property violations (Li et al. 2024a), regulatory compliance beyond privacy (Chundawat et al. 2023), toxicity mitigation (Łucki et al. 2025), and model refinement (Jia et al. 2023). Machine Unlearning (MU) (Si et al. 2023) offers a promised solution to remove unwanted knowledge from MLLMs, supporting controllable and compliant model adaptation. However, current research on MU for MLLMs remains underexplored.

## Methods

such as (Thudi et al. 2022; Liu, Liu, and Stone 2022; Zhang et al. 2024) primarily extend fine-tuning-based unlearning strategies originally designed for LLMs. However, these methods ignore the unique discrepancies between modalities in MLLMs, and struggle to forget modalityspecific knowledge effectively, especially under textual inputs, as illustrated in Fig. 1 (a). An alternative line of work that explores neuron-level editing has emerged as a

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

35589

![Figure extracted from page 1](2026-AAAI-cross-modal-unlearning-via-influential-neuron-path-editing-in-multimodal-large-l/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-cross-modal-unlearning-via-influential-neuron-path-editing-in-multimodal-large-l/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

promising direction, based on the observation that model knowledge is stored in distributed patterns within learnable parameters (Yao et al. 2023). Recent approaches such as DEPN (Wu et al. 2023) and MANU (Liu et al. 2025b) attempt modality-specific forgetting via single-neuron pruning or activation-based scoring. However, the point-wise estimation fails to capture the structured information flow across layers in multimodal architectures. As a result, forgetting remains uncoordinated across modalities. This limitation is statistically demonstrated in Table 1. Moreover, as illustrated in Fig. 1 (b), pruning neurons solely based on their individual importance to the forget-set may inadvertently disrupt reasoning pathways critical to the retain-set, leading to severe degradation of general knowledge.

Recent studies (Wang et al. 2025) have confirmed that information in large models is transmitted through structured, layer-wise neuron pathways. These influential paths offer a more coherent and semantically grounded basis for unlearning compared to isolated neurons. In MLLMs, both textual and multimodal (e.g., image–text) inputs rely on such structured reasoning flows. This motivates a shift from point-based deletion to path-aware interventions that better align with the model’s internal knowledge organization. To this end, we propose a Multimodal Influential neuron Path Editor (MIP-Editor) tailored for MU in MLLMs. Our approach locates modality-specific influential neuron paths in the FFN layers of both the textual and visual branches by computing inter-layer gradient-integrated and Fisher-integrated attribution scores. In particular, we introduce an influential-path-based neuron editing method using Representation Misdirection Unlearning (RMisU) that adaptively steers the representations of forget-set inputs away from their original semantics, reducing the impact on general knowledge. To sum up, our contributions are as follows:

• We propose a dual-branch (visual and textual) influential neuron path localization framework. This approach leverages inter-layer gradient-integrated and Fisher-integrated attribution scores to capture modality-specific information flow, enabling precise localization of neurons responsible for specific knowledge in each modality. • We analyze the limitations of direct pruning strategies, where overlapping neurons between forget and retain sets cause a collapse of general reasoning paths. To mitigate this, we propose a targeted RMisU-based neuron editing strategy that operates only on the influential neuron paths, decoupling specific and general knowledge. • Experiments demonstrate that MIP-Editor achieves modality-consistent forgetting with strong retain-set performance, reaching up to 87.75% forgetting and 54.26% retention improvement on multimodal tasks, and 80.65% forgetting with 77.9% retention on textual tasks.

Related Works Fine-tuning for MLLM Unlearning Recent MU efforts aim to remove specific knowledge from models for privacy and safety. Early approaches for LLMs employ gradient ascent (Thudi et al. 2022; Liu, Liu, and Stone 2022), KL minimization (Nguyen, Low, and Jaillet 2020), and preference- based objectives (Zhang et al. 2024), with applications in toxicity mitigation (Chen et al. 2025) and hallucination reduction (Xing et al. 2024). However, these methods are confined to text-only settings. Multimodal unlearning for MLLMs remains largely unexplored. To support multimodal research, dedicated benchmarks MLLMU-Bench (Liu et al. 2025a) and CLEAR (Dontsov et al. 2024) have been proposed. Recent studies (Yang et al. 2024; Cheng and Amiri 2024; Li et al. 2024b; Huo et al. 2025) extend fine-tuning to erase visual concepts, yet they require full-model updates and overlook the modular architecture of MLLMs.

Neuron Editing in Large Language Models Neuron editing provides a fine-grained mechanism to alter model behavior while preserving general capabilities. Studies have examined how pretrained LMs encode knowledge (Chen et al. 2024; Li et al. 2023; Cao et al. 2024; Lamparth and Reuel 2024), enabling targeted neuron-level interventions. This technique has been applied to MU (Wu, Hashemi, and Srinivasa 2022; Hase et al. 2023; Gandikota et al. 2023), harmful content mitigation (Hu et al. 2024), continual learning (Biesialska, Biesialska, and Ruiz Costa-Juss`a 2020), and privacy protection (Wu et al. 2023). In multimodal contexts, MANU (Liu et al. 2025b) introduces neuron-level editing for modality-specific forgetting, yet its heuristic scoring and zero-out pruning can disrupt reasoning coherence. Our approach mitigates these issues through path-aware editing, identifying coherent, modality-specific neuron sequences for more consistent and effective unlearning.

## 3 Problem Definition

We focus on MU for MLLMs, aiming to remove targeted forgetting knowledge while minimizing degradation of general capabilities. Let Mθ denote the original MLLM with parameters θ, trained on a dataset D = {(Ii, Ti)}N i=1 of N image–text pairs, where Ii is an image and Ti = {si

1,..., si ti} is its corresponding tokenized text. Each pair includes a question–answer prompt for visual understanding. We divide D into a forget-set Df = {(If j, T f j)}Nf j=1, containing specific concepts to be forgotten, and a retain-set Dr = {(Ir k, T r k)}Nr k=1, used to preserve general knowledge. Following (Liu et al. 2025a,b), we define MU in MLLMs as: The process of removing both visual and textual forgetting data from a model while preserving its predictive performance on unrelated inputs. To achieve this, we minimize the negative log-likelihood of next-token prediction and obtain the unlearned model Mˆθ via the objective:

arg min θ∗

(

−E(I,T)∈Df h

−

Nf X n=1 log pMˆθ(wn|(I, T), w<n)

i

| {z } Forget specific visual & textual patterns

+ E(I,T)∈Dr h

−

Nr X n=1 log pMˆθ(wn|(I, T), w<n)

i

| {z } Retain general knowledge

)

(1)

35590

<!-- Page 3 -->

Multi Input

Who is this man?

Forget-set Locating Influential Path

Visual Model FFN

Language Model FFN Multi Input Q3. What profession of this individual?

Editing Influential Neuron Paths

A1. Lucas Harrington in the image is likely a banker. Visual Forgot (Expected) A2. Lucas Harrington is a graphic designer. Textual Forgot (Expected)

A3. The person in the image is likely an art curator. Retain (Expected)

Unlearned MLLM by MIP-Editor

Inter-layer Gradient Integration Retain-set

Frozen Neuron Pruned Neuron

Pruning

Frozen Neuron Activated Neuron

Retain Knowledge Forget Misdirection Forget Knowledge

1

Editing with RMisU

2

Representation Misdirection

Unlearning Output

1 2

Inter-layer Fisher Integration

Output

1 2

Q1. What profession is Lucas Harrington?

Lucas Harrington

General Neuron

Visual Path MLLM

Forward

Q2. What profession is Lucas Harrington?

Text Input

Retain Target

RMisU Neuron Updating

Answer

Textual Path

**Figure 2.** Overview of MIP-Editor. (1) Influential neuron paths are located using inter-layer gradient (text) and Fisher (vision) integration. (2) Neurons inside the selected paths are pruned, and (3) path-specific editing is performed via representation misdirection to achieve modality-consistent forgetting while preserving general knowledge.

## 4 Method

## 4.1 Locating Influential Neuron Path

In MIP-Editor (Fig. 2), the textual and visual influential paths are inherently related, as each input pair (I, T) carries semantically aligned content. Prior works (Radford et al. 2021; Pan et al. 2024; Sato and Takagi 2025) show that vision and text features are mapped into a shared embedding space and jointly processed via cross-attention, ensuring correspondence between activations across modalities.

Inter-layer Gradient Integration To locate influential neurons in the textual modality, we propose an interlayer gradient integration method inspired by information flow (Lu et al. 2021) and joint attribution (Wang et al. 2025). Given the L-layer architecture of a language model, where each FFN layer is regarded as a key repository of factual knowledge, we aim to quantify the contribution of selected neurons across the first N layers.

Let ⟨T, Y ⟩denote a labeled text pair, where T ∈Rd is the input text and Y is the expected output. The model’s output over the first N layers is represented as:

FT (w) = p(Y | T, w1 i1, · · ·, wN iN), (2)

where w = (w1 i1, · · ·, wN iN) are the activations of selected neurons in the textual FFN layers, and ˜wn in denotes the original activation of neuron wn in of the n-th layer. To estimate the joint contribution of these neurons, we scale the activation values {α1 i1, · · ·, αN iN } from 0 to their original activations { ˜w1 i1, · · ·, ˜wN iN }. The inter-layer gradient-integrated attribution score is defined as:

IGI(w) =

N X n=1

˜wn in

Z ˜ wn in

0

N X l=1

∂FT (α1 i1, · · ·, αn in) ∂wl il dαn in,

(3) which measures how the neurons along the path contribute to the model’s output by integrating gradients across layers.

To approximate the integral, we employ Riemann approximation (Dai et al. 2022) by interpolating m frames into the activation values. The discrete form of the IGI becomes:

IGI(w) =

N X j=1

˜wn ij m X k=1

N X l=1

∂FT k mα1 i1, · · ·, k mαN iN

∂wl il

. (4)

Inter-layer Fisher Integration To locate influential neurons in the visual modality, we adopt an inter-layer Fisher integration method similar to the gradient-based approach used for text. Due to the high dimensionality, spatial correlation, and parameter redundancy in vision encoders, the Fisher Information Matrix (FIM) offers a more suitable signal for estimating neuron importance.

Let ⟨(I, T), Y ⟩denote a multimodal input with visual input I ∈RdI, text input T ∈RdT, and target output Y. The log-likelihood output over the first N visual FFN layers is:

G(z) = log p(Y | I, T, z1 i1, · · ·, zN iN), (5)

where z = (z1 i1, · · ·, zN iN) are the activations of selected visual neurons, and ˜zn in their original values. Similar to the textual integration (Eq. 4), we interpolate neuron activations from 0 to their original values using m steps. To approximate the diagonal of the FIM, we adopt the squared-gradient formulation. The inter-layer Fisherintegrated score is defined as:

IFI(z) =

N X n=1

˜zn in m X k=1

N X l=1

∂G k mβ1 i1, · · ·, k mβN iN

∂zl il

!2

,

(6) where {βn in} are the interpolated activations. This formulation enables efficient estimation of visual neuron importance by integrating second-order signals across layers.

Locating Paths Following (Wang et al. 2025), we define the influential neuron paths in the FFN layers of MLLMs. Definition 1 (Influential Paths) Let F: Rd →R be a multimodal model consisting of L FFN layers for a given modality, and let x denote either a text input T or an image–text

35591

<!-- Page 4 -->

## Algorithm

1: Inter-layer Integrated Influential Path Locating

Input: MLLM Mθ with Lt textual layers and Lv visual lay- ers, input pair (I, T) Output: Visual path Pv, Textual path Pt

1: Pv ←∅, Pt ←∅ 2: for k = 1 to Lt do 3: Let Wt be the set of neurons in textual layer k 4: Score ←−∞, bestNeuron ←None 5: for all w ∈Wt do 6: s ←IGI(Pt ∪{w}, T) 7: if s > Score then 8: Score ←s, bestNeuron ←w 9: end if 10: end for 11: Pt ←Pt ∪{bestNeuron} 12: end for 13: for l = 1 to Lv do 14: Let Wv be the set of neurons in visual layer l 15: Score ←−∞, bestNeuron ←None 16: for all z ∈Wv do 17: s ←IFI(Pv ∪{z}, I, T) 18: if s > Score then 19: Score ←s, bestNeuron ←z 20: end if 21: end for 22: Pv ←Pv ∪{bestNeuron} 23: end for 24: return Pv, Pt pair (I, T). A neuron path is defined as

Px = {w1, w2,..., wL}, wl ∈W, (7)

where wl denotes the set of selected neurons in the l-th layer. W represents the general FFN layer parameters

We define a modality-specific scoring function as follows:

S(Px) =

IGI(Px), if x = T, IFI(Px), if x = (I, T), (8)

The influential path P∗ x is then defined as the one that maximizes the corresponding score:

P∗ x = arg max

Px S(Px). (9)

To locate influential paths efficiently, we apply a greedy layer-wise search (Algorithm 1) that selects the most influential neuron per layer. Given input (I, T) and a pretrained model F with Lt textual and Lv visual FFN layers, the algorithm outputs two ordered paths: Pt and Pv for the textual and visual modalities, respectively.

## 4.2 Editing Influential Neuron Paths

Having located influential paths, we prune encoding forgetset information and employ RMisU to redirect their activations away from undesired semantics while reinforcing retain-set representations. This prune-and-finetune strategy updates only a small subset of neurons, enabling effective forgetting with negligible impact on general knowledge.

Pruning Specifically, we perform targeted pruning by zeroing the activations of neurons identified as specificrelevant along the influential paths. For a text-only input T and a multimodal input (I, T), let the corresponding influential paths be PT = { ˜w1, ˜w2,..., ˜wLt} and P(I,T) = {˜z1, ˜z2,..., ˜zLv}, the pruning can be formally expressed as:

˜wl ←0, ∀l ∈{1,..., Lt}; ˜zl ←0, ∀l ∈{1,..., Lv},

(10) where 0 represents an all-zero vector with the same dimension, ˜wl and ˜zl denote the activation values set of the selected neurons in the l-th layer. This operation ensures that the flow of information associated with forgetting concepts is blocked, thereby achieving targeted forgetting.

Editing with RMisU Pruning risks losing general knowledge in overlapping neurons of the retain-set. To recover it adaptively with minimal forgetting, we fine-tune only the pruned neurons using the retain-set, enabling adaptive recovery with less reintroduction of forgotten content. Specifically, all other parameters in the MLLM are frozen, and only neurons along influential paths are updated. Let Mθ∗denote the pruned model. To preserve general knowledge, we minimize a cross-entropy loss over the retain-set Dr:

Lretain = E(xr,yr)∈Dr



−

|yr| X i=1 log PMθ∗(yr i | xr, yr

<i)



,

(11) where xr ∈{T r, (Ir, T r)} denotes either a text or image–text input, and yr is the corresponding output sequence.

To forget specific knowledge in the forget-set Df, prior methods use gradient ascent, KL divergence, or contrastive objectives, but often at the cost of linguistic and utility degradation (Fan et al. 2024). To avoid this, we adopt adaptive Representation Misdirection Unlearning (RMisU) (Dang et al. 2025), which steers forget-set representations away from their original semantics via localized directional perturbation at a specific layer l. This targeted editing removes specific knowledge while preserving general linguistic ability (Li et al. 2024c).

For each forget-set input xf ∈{T f, (If, T f)}, we sample a random unit vector from the unit sphere:

u ∼Uniform

Sd−1

, (12)

and define a layer-specific target representation as vf = λ · h(l)

Mθ(xf)

2 · u, (13)

where h(l)

Mθ(xf) denotes the frozen model’s hidden representation at layer l, and λ is a scaling coefficient modulating the influence of the perturbation.

Forgetting RMisU loss. This term forces the representation of forget-set samples to align with the randomized vector vF, effectively erasing forgetting knowledge:

Lf

RMisU = Exf ∈Df h(l)

Mθ∗(xf) −vf

2

2, (14)

where h(l)

Mθ∗(xf) denotes the intermediate representation at layer l for a forget-set sample xf in Mθ∗at current epoch.

35592

<!-- Page 5 -->

Retaining RMisU loss. We minimize deviation of retainset representations from the frozen model for generalization:

Lr

RMisU = Exr∈Dr h(l)

Mθ∗(xr) −h(l)

Mθ(xr)

2

2. (15)

Full objective. The overall adaptive RMisU loss is:

LRMisU = Lf

RMisU + γ · Lr

RMisU, (16)

where γ > 0 balances forgetting and retention.

## Experiments

In this section, we answer the following key questions concerning the performance of MIP-Editor with experiments. Q1: Can MIP-Editor effectively eliminate multimodal information from the target MLLMs? Q2: Can MIP-Editor achieve coordinated forgetting across visual and textual modalities? Q3: Can MIP-Editor strike a balance between forgetting information and preserving general knowledge? Q4: Does MIP-Editor retain more informative content through influential neuron paths compared to point-wise probing methods?

## 5.1 Experimental Setup and Baselines

To evaluate the effectiveness of MIP-Editor, we conduct experiments on two representative MLLMs of different scales: Qwen2.5-VL-3B-Instruct (Wang et al. 2024) and LLaVA1.5-7B (Liu et al. 2023), using two dedicated multimodal unlearning benchmarks: MLLMU-Bench (Liu et al. 2025a) and CLEAR (Dontsov et al. 2024). These datasets provide structured forget and retain splits across diverse multimodal tasks, including visual question answering (VQA) and text-based QA, covering both generation and classification settings. We compare MIP-Editor with four strong baselines: GA Diff (Liu, Liu, and Stone 2022), KL Min (Nguyen, Low, and Jaillet 2020), NPO (Zhang et al. 2024), and MANU (Liu et al. 2025b). Vanilla denotes the original model without unlearning. For fair comparison, all methods are trained using the same configurations. MLLMU-Bench uses 5%, 10%, and 15% of its samples as forget-sets, while CLEAR uses 1%, 5%, and 10%.

## 5.2 Main Results

To answer Q1 and Q2, we evaluate the unlearning performance of various methods on multimodal and textual tasks using Qwen2.5-VL-3B-Instruct and LLaVA1.5-7B under a 5% forget ratio on MLLMU-Bench and CLEAR (Table 1). On multimodal tasks, MIP-Editor significantly reduces forgetting knowledge retention. For instance, it lowering FVQA accuracy from 39.20% (Vanilla) to 4.80% and improving RVQA from 37.72% to 58.19% on MLLMU based on Qwen2.5-VL. This corresponds to an 87.75% forgetting rate and a 54.26% improvement in general knowledge retention, outperforming GA Diff, KL Min, and NPO. Similar trends are observed for LLaVA1.5. On textual tasks, MIP-Editor reduces FQA accuracy from 49.60% to 9.60%, achieving an 80.65% forgetting rate while retaining 77.9% of the original performance. Compared with MANU,

0 10 20 30 Forget Accuracy Diff

30

40

50

Ret VQA Acc

0 10 20 30 Forget Rouge-L Diff

20

30

40

Ret VGEN Rouge-L

0 20 40 Forget Accuracy Diff

30

40

Ret QA Acc

0 10 20 Forget Rouge-L Diff

30

40

50

Ret GEN Rouge-L

GA5% GA10% GA15%

KL5% KL10% KL15%

NPO5% NPO10% NPO15%

MANU5% MANU10% MANU15%

OURS5% OURS10% OURS15%

**Figure 3.** The overall trade-off between unlearning effectiveness and model utility across four dimensions under varying forget ratios, using Qwen2.5-VL as the base model.

NPO, and KL Min, MIP-Editor more effectively suppresses residual forgetting knowledge while preserving competitive accuracy on the retain-set (e.g., 58.19% RVQA and 47.34% RQA). These results confirm the strength of MIP-Editor in achieving coordinated forgetting across modalities with minimal impact on general capability.

5.3 Unlearning v.s. Model Utility To evaluate whether MIP-Editor achieves a superior trade-off between forgetting specific data and retaining general knowledge (Q3), we compare the performance differences on the forget-set with the post-unlearning accuracy on the retain-set. This analysis reflects each method’s ability to balance unlearning and utility preservation. We evaluate four tasks on MLLMU-Bench: VQA (visual question answering), VGEN (visual generation), QA (textual question answering), and GEN (textual generation). As shown in Fig. 3, the x-axis denotes the performance drop on the forget-set (higher is better for forgetting), and the y-axis represents the retain-set performance after unlearning (higher is better for retention). An ideal method lies toward the upper right, indicating strong forgetting with minimal generalization loss. Results show that MIP-Editor achieves a consistently favorable trade-off across all tasks and forget ratios, with stronger gains in multimodal settings. Notice that in the GEN task, the gap is less pronounced due to the limitations of Rouge-L, which measures only semantic overlap and may not capture forget-set-related differences effectively.

## 5.4 Influential

Paths v.s. Influential Neurons To assess whether influential neuron paths capture more information than point-wise neurons (Q4), we compare two selection strategies: (a) path-based (MIP-Editor) and (b) point-wise (Liu et al. 2025b). For each, we select the top-k neurons per layer in both modalities and zero out the rest.

35593

<!-- Page 6 -->

## Method

MLLMU-Bench CLEAR

Task FVQA RVQA FVGEN RVGEN FQA RQA FVQA RVQA FVGEN RVGEN FGEN RGEN Metric Acc(↓) Acc(↑) Rouge(↓) Rouge(↑) Acc(↓) Acc(↑) Acc(↓) Acc(↑) Rouge(↓) Rouge(↑) Rouge(↓) Rouge(↑)

Qwen2.5-VL-3B-Instruct

Vanilla 39.20% 37.72% 0.4527 0.4347 49.60% 47.20% 72.34% 73.42% 0.3196 0.2997 0.3776 0.3900 GA Diff 32.00% 32.80% 0.4450 0.4756 46.40% 43.20% 27.66% 23.04% 0.2946 0.2751 0.3740 0.3896 KL Min 33.60% 27.59% 0.2139 0.1940 41.60% 42.57% 12.77% 9.11% 0.2532 0.2400 0.3270 0.3287 NPO 37.60% 36.20% 0.4507 0.4307 42.40% 44.80% 7.45% 9.37% 0.0803 0.0605 0.0805 0.0639 MANU 36.00% 34.47% 0.4406 0.4367 30.80% 34.65% 78.72% 77.97% 0.3220 0.2987 0.3809 0.3903 MIP-Editor 4.80% 58.19% 0.0997 0.4195 9.60% 36.80% 3.19% 24.05% 0.0707 0.2684 0.0926 0.3631

Llava-1.5-7B

Vanilla 56.80% 51.56% 0.5580 0.4946 50.40% 52.59% 44.68% 43.54% 0.3060 0.2937 0.3462 0.3546 GA Diff 54.40% 52.78% 0.5719 0.5071 42.40% 49.83% 14.36% 15.19% 0.3057 0.2931 0.3565 0.3620 KL Min 32.80% 38.27% 0.3594 0.3390 43.20% 43.29% 43.62% 42.28% 0.2200 0.2068 0.1380 0.1671 NPO 48.00% 47.26% 0.5388 0.4907 46.40% 51.52% 10.64% 15.95% 0.2091 0.1815 0.0150 0.0136 MANU 56.00% 52.11% 0.5486 0.4960 48.80% 52.19% 43.62% 42.28% 0.3070 0.2920 0.3452 0.3556 MIP-Editor 38.40% 47.22% 0.3418 0.3552 36.80% 47.34% 6.38% 52.66% 0.9690 0.2258 0.1441 0.2268

**Table 1.** Overall performances of baseline methods and MIP-Editor on machine unlearning tasks with 5% forget ratio. F: Forget-set; R:Retain-set; VQA:Vision Question Answer; QA: Question Answer; VGEN: Vision Generation; GEN: Generation.

We then measure model performance on the forget and retain sets as a proxy for general knowledge retention. Notice that higher accuracy implies greater representational capacity. Experiments are conducted on MLLMU-Bench using Qwen2.5-VL with a 5% forget ratio. Results for generation tasks are shown in Fig. 4. From the results, we observe that when only a small number of neurons are retained, both strategies yield low ROUGE-L scores. However, performance under the path-based strategy begins to improve significantly after the top-k exceeds 25, peaking around 29. In contrast, the point-wise strategy lags behind and only approaches the performance of the path-based method near 213. These findings suggest that neuron paths capture richer and more functionally critical information, and are thus more effective in preserving model performance.

23 25 27 29 211 213

Top k

0.0

0.2

0.4

Rouge-L

Neurons Paths

(a) Multi Input (Forget)

23 25 27 29 211 213

Top k

0.0

0.2

0.4

Rouge-L

Neurons Paths

(b) Multi Input (Retain)

23 25 27 29 211 213

Top k

0.0

0.2

0.4

Rouge-L

Neurons Paths

(c) Text Input (Forget)

23 25 27 29 211 213

Top k

0.0

0.2

0.4

Rouge-L

Neurons Paths

(d) Text Input (Retain)

**Figure 4.** Performance comparison on generation tasks between influential neuron paths and point-wise influential neurons under varying top-k neuron selections.

Act

## Methods

0.00

0.02

0.04

0.06

Logits MAE

Act MANU

Reference Line

Ours MANU

Ours

(a) Multi Classification

0.00

0.02

0.04

0.06

Logits MAE

Act

## Methods

Ours MANU

Act MANU

Reference Line Ours

(b) Multi Generation

**Figure 5.** Relative MAE of predicted logit probabilities for ground-truth labels after pruning neurons selected by different methods.

Moreover, we analyze the deviations in predicted probabilities for ground-truth classes on MLLMU’s multimodal classification and generation tasks after neuron pruning by Qwen2.5-VL. Specifically, we prune the top-5 neurons located by Activation-based, MANU, and MIP-Editor, and compute the MAE of the model’s logits before and after pruning. As shown in Fig. 5, our method causes larger shifts in predicted logits compared to the other two approaches, indicating that the neurons selected by MIP-Editor play a more critical role in model inference.

## 5.5 Ablation Studies and Variants

We conduct ablation studies on MLLMU-Bench using Qwen2.5-VL with a 5% forget ratio to evaluate the contribution of each component in MIP-Editor. (1) Disabling modality coordination by using only textual (ours (IGI)) or visual (ours (IFI)) paths substantially weakens forgetting effectiveness (e.g., 36.00% FVQA and 49.60% FQA), confirming the necessity of dual-path localization for modalityconsistent forgetting. (2) Replacing inter-layer attribution

35594

<!-- Page 7 -->

Task FVQA RVQA FVGEN RVGEN FQA RQA Metric Acc(↓) Acc(↑) Rouge(↓) Rouge(↑) Acc(↓) Acc(↑)

Ours 4.80% 58.19% 0.0997 0.4195 9.26% 36.31% Ours (IGI) 36.00% 31.60% 0.4045 0.4090 41.60% 45.99% Ours (IFI) 32.00% 33.46% 0.3746 0.4313 49.60% 47.55% Ours-Path 2.40% 2.11% 0.0334 0.0479 2.40% 2.15% Ours-Edit 43.60% 46.00% 0.4035 0.4675 42.80% 52.08% Ours-RMisU 46.40% 42.23% 0.3594 0.3403 34.40% 31.62% RMisU 8.00% 14.65% 0.2667 0.2949 12.00% 10.99%

**Table 2.** Ablation studies and variants of MIP-Editor on MLLMU-Bench with 5% forget ratio by Qwen2.5-VL. F: Forget-set; R:Retain-set; VQA:Vision Question Answer; QA: Question Answer; VGEN: Vision Generation.

with a simple activation residual score (ours-Path) achieves low forget accuracy but severely degrades retain performance (e.g., 2.11% RVQA), showing that point-wise locating disrupts general knowledge. (3) Omitting RMisU editing (ours-Edit) or replacing it with standard fine-tuning (ours- RMisU) leads to ineffective forgetting and weak retention, demonstrating the limitations of pruning directly and the importance RMisU editing. (4) Applying RMisU to the full model without pruning (RMisU) yields moderate forgetting but fails to preserve utility (e.g., 14.65% RVQA), validating the advantage of selective neuron editing.

## 5.6 Visualization

We visualize activation residuals across layers using heatmaps to assess the forgetting and retention behavior of different unlearning methods. Specifically, we input both forget-set and retain-set samples into the unlearned MLLMs and record activation values at each FFN layer. These are compared with the vanilla model’s activations, and absolute residuals are used to generate the heatmaps. Darker colors indicate greater deviation from the original model (stronger forgetting), while lighter colors reflect better retention. Experiments are conducted on Qwen2.5-VL using MLLMU- Bench (5% forget ratio) across generation tasks. Results for generation are shown in Fig. 6. As shown in Fig. 6(a) and Fig. 6(c), baseline methods yield consistently shallow color intensities, especially under textual inputs, suggesting limited forgetting. Moreover, similar intensities across forget and retain sets indicate poor separation of specific and general knowledge. In contrast, MIP-Editor exhibits clear modality-aware behavior: deeper residuals on the forget-set and lighter residuals on the retain-set, particularly under textual inputs, demonstrating effective cross-modal unlearning with minimal performance degradation.

## 5.7 Specific Information Separability

To assess the effectiveness of unlearning methods in separating specific information from general knowledge in MLLMs, we train an MLP-based binary classifier using the output logits of the post-unlearning model. Experiments on MLLMU-Bench and CLEAR with Qwen2.5-VL evaluate two settings: (1) classification over the full fine-tuning set and (2) classification on CLEAR’s generation tasks (Multi

1

11 16 21 26 31 36

Layer

6

GA

## Method

s

KL NPO MA Ours

(a) Multi Input (Forget)

1

11 16 21 26 31 36

Layer

6

GA

## Method

s

KL NPO MA Ours 0.000

0.002

0.004

0.006

Activation Strength

(b) Multi Input (Retain)

1

11 16 21 26 31 36

6

GA

## Method

s

KL NPO MA Ours

Layer

(c) Text Input (Forget)

0.000

0.002

0.004

0.006

Activation Strength

1

11 16 21 26 31 36

Layer

6

GA

## Method

s

KL NPO MA Ours

(d) Text Input (Retain)

**Figure 6.** Layer-wise visualization of knowledge retention in the language FFN of MLLMs across forget and retain sets on MLLMU-Bench. GA: Grad Diff; Ours: MIP-Editor.

MLLMU CLEAR 0

25

50

75

100

Accuracy (%)

(a) Fullset of MLLMU and CLEAR

Multi Text 0

20

40

60

80

Accuracy (%)

(b) Generation task of CLEAR

Vanilla GA KL NPO MANU Ours

**Figure 7.** Classification of specific vs. general data using Qwen2.5-VL, including (a) full-set classification on MLLMU-Bench and CLEAR, and (b) generation-task classification on CLEAR (Multi and Text).

and Text). As shown in Fig. 7, MIP-Editor consistently achieves the highest classification accuracy, exceeding 85% across datasets and input types, indicating clearer behavioral separation between specific and general inputs. In contrast, GA, KL, NPO, and MANU perform near random (around 50%) on MLLMU-Bench, showing limited separation capability. On CLEAR’s text generation tasks, where questions and answers lack visual modality, the performance of the classification becomes harder to distinguish. Nonetheless, MIP-Editor still outperforms all baselines.

## 6 Conclusion

In this paper, we address machine unlearning in Multimodal Large Language Models (MLLMs), highlighting key limitations of existing methods, such as cross-modal inconsistency and general performance degradation. To tackle these issues, we propose MIP-Editor, a multimodal pathway-editor that identifies influential neuron paths in each modality and applies path-aware editing through representation misdirection. Experiments demonstrate that MIP-Editor achieves effective unlearning of forgetting knowledge while preserving general utility. This work offers a principled framework for fine-grained knowledge removal in MLLMs.

35595

<!-- Page 8 -->

## Acknowledgements

This work was supported in part by Hong Kong RGC Theme-based Research Scheme (TRS) under Grant T43- 513/23-N, in part by the NSFC and Hong Kong RGC Collaborative Research Scheme under Grant 62321166652, in part by the Guangdong Basic and Applied Basic Research Foundation under Grant 2025A1515011996, and in part by the Fundamental Research Funds for the Central University under Grant CXTD202406. We also thank the grant from NVIDIA and utilized NVIDIA A100 GPUs through the NVIDIA Academic Grants Program.

## References

Biesialska, M. M.; Biesialska, K.; and Ruiz Costa-Juss`a, M. 2020. Continual lifelong learning in natural language processing: a survey. In COLING 2020, The 28th International Conference on Computational Linguistics: December 8-13, 2020, Barcelona, Spain (online): proceedings of the conference, 6523–6541. Association for Computational Linguistics. Caffagni, D.; Cocchi, F.; Barsellotti, L.; Moratelli, N.; Sarto, S.; Baraldi, L.; Cornia, M.; and Cucchiara, R. 2024. The Revolution of Multimodal Large Language Models: A Survey. In Findings of the Association for Computational Linguistics ACL 2024, 13590–13618. Cao, B.; Tang, Q.; Lin, H.; Jiang, S.; Dong, B.; Han, X.; Chen, J.; Wang, T.; and Sun, L. 2024. Retentive or Forgetful? Diving into the Knowledge Memorizing Mechanism of Language Models. In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), 14016– 14036. Chen, J.; Deng, Z.; Zheng, K.; Yan, Y.; Liu, S.; Wu, P.; Jiang, P.; Liu, J.; and Hu, X. 2025. SAFEERASER: Enhancing Safety in Multimodal Large Language Models through Multimodal Machine Unlearning. arXiv preprint arXiv:2502.12520. Chen, Y.; Cao, P.; Chen, Y.; Liu, K.; and Zhao, J. 2024. Journey to the center of the knowledge neurons: Discoveries of language-independent knowledge neurons and degenerate knowledge neurons. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 17817–17825. Cheng, J.; and Amiri, H. 2024. Multidelete for multimodal machine unlearning. In European Conference on Computer Vision, 165–184. Springer. Chundawat, V. S.; Tarun, A. K.; Mandal, M.; and Kankanhalli, M. 2023. Zero-shot machine unlearning. IEEE Transactions on Information Forensics and Security, 18: 2345– 2354. Dai, D.; Dong, L.; Hao, Y.; Sui, Z.; Chang, B.; and Wei, F. 2022. Knowledge Neurons in Pretrained Transformers. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 8493–8502. Dang, H.-T.; Pham, T.; Thanh-Tung, H.; and Inoue, N. 2025. On Effects of Steering Latent Representation for Large Lan- guage Model Unlearning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 23733–23742. Dontsov, A.; Korzh, D.; Zhavoronkin, A.; Mikheev, B.; Bobkov, D.; Alanov, A.; Rogov, O. Y.; Oseledets, I.; and Tutubalina, E. 2024. Clear: Character unlearning in textual and visual modalities. arXiv preprint arXiv:2410.18057. Fan, C.; Liu, J.; Lin, L.; Jia, J.; Zhang, R.; Mei, S.; and Liu, S. 2024. Simplicity Prevails: Rethinking Negative Preference Optimization for LLM Unlearning. In Neurips Safe Generative AI Workshop 2024. Gandikota, R.; Materzynska, J.; Fiotto-Kaufman, J.; and Bau, D. 2023. Erasing concepts from diffusion models. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 2426–2436. Hase, P.; Bansal, M.; Kim, B.; and Ghandeharioun, A. 2023. Does localization inform editing? surprising differences in causality-based localization vs. knowledge editing in language models. Advances in Neural Information Processing Systems, 36: 17643–17668. Hu, X.; Li, D.; Hu, B.; Zheng, Z.; Liu, Z.; and Zhang, M. 2024. Separate the wheat from the chaff: Model deficiency unlearning via parameter-efficient module operation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 18252–18260. Huo, J.; Yan, Y.; Zheng, X.; Lyu, Y.; Zou, X.; Wei, Z.; and Hu, X. 2025. MMUNLEARNER: Reformulating Multimodal Machine Unlearning in the Era of Multimodal Large Language Models. Jia, J.; Liu, J.; Ram, P.; Yao, Y.; Liu, G.; Liu, Y.; Sharma, P.; and Liu, S. 2023. Model sparsity can simplify machine unlearning. Advances in Neural Information Processing Systems, 36: 51584–51605. Lamparth, M.; and Reuel, A. 2024. Analyzing and editing inner mechanisms of backdoored language models. In Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency, 2362–2373. Li, H.; Deng, G.; Liu, Y.; Wang, K.; Li, Y.; Zhang, T.; Liu, Y.; Xu, G.; Xu, G.; and Wang, H. 2024a. Digger: Detecting Copyright Content Mis-usage in Large Language Model Training. CoRR. Li, J.; Wei, Q.; Zhang, C.; Qi, G.; Du, M.; Chen, Y.; Bi, S.; and Liu, F. 2024b. Single image unlearning: Efficient machine unlearning in multimodal large language models. Advances in Neural Information Processing Systems, 37: 35414–35453. Li, N.; Pan, A.; Gopal, A.; Yue, S.; Berrios, D.; Gatti, A.; Li, J. D.; Dombrowski, A.-K.; Goel, S.; Mukobi, G.; et al. 2024c. The WMDP benchmark: measuring and reducing malicious use with unlearning. In Proceedings of the 41st International Conference on Machine Learning, 28525–28550. Li, Z.; Zhang, N.; Yao, Y.; Wang, M.; Chen, X.; and Chen, H. 2023. Unveiling the Pitfalls of Knowledge Editing for Large Language Models. CoRR. Liu, B.; Liu, Q.; and Stone, P. 2022. Continual learning and private unlearning. In Conference on Lifelong Learning Agents, 243–254. PMLR.

35596

<!-- Page 9 -->

Liu, H.; Li, C.; Wu, Q.; and Lee, Y. J. 2023. Visual instruction tuning. Advances in neural information processing systems, 36: 34892–34916. Liu, Z.; Dou, G.; Jia, M.; Tan, Z.; Zeng, Q.; Yuan, Y.; and Jiang, M. 2025a. Protecting Privacy in Multimodal Large Language Models with MLLMU-Bench. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), 4105– 4135. Liu, Z.; Dou, G.; Yuan, X.; Zhang, C.; Tan, Z.; and Jiang, M. 2025b. Modality-Aware Neuron Pruning for Unlearning in Multimodal Large Language Models. Proceedings of the 63nd Annual Meeting of the Association for Computational Linguistics. Lu, K.; Wang, Z.; Mardziel, P.; and Datta, A. 2021. Influence patterns for explaining information flow in bert. Advances in Neural Information Processing Systems, 34: 4461–4474. Łucki, J.; Wei, B.; Huang, Y.; Henderson, P.; Tram`er, F.; and Rando, J. 2025. An Adversarial Perspective on Machine Unlearning for AI Safety. Transactions on Machine Learning Research. Nguyen, Q. P.; Low, B. K. H.; and Jaillet, P. 2020. Variational bayesian unlearning. Advances in Neural Information Processing Systems, 33: 16025–16036. Pan, H.; Cao, Y.; Wang, X.; Yang, X.; and Wang, M. 2024. Finding and Editing Multi-Modal Neurons in Pre-Trained Transformers. In Findings of the Association for Computational Linguistics ACL 2024, 1012–1037. Association for Computational Linguistics. Pi, R.; Han, T.; Zhang, J.; Xie, Y.; Pan, R.; Lian, Q.; Dong, H.; Zhang, J.; and Zhang, T. 2024. MLLM-Protector: Ensuring MLLM’s Safety without Hurting Performance. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, 16012–16027. Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In International conference on machine learning, 8748–8763. PmLR. Sato, Y.; and Takagi, T. 2025. Identifying Multi-modal Knowledge Neurons in Pretrained Transformers via Twostage Filtering. arXiv preprint arXiv:2503.22941. Si, N.; Zhang, H.; Chang, H.; Zhang, W.; Qu, D.; and Zhang, W. 2023. Knowledge unlearning for llms: Tasks, methods, and challenges. arXiv preprint arXiv:2311.15766. Thudi, A.; Deza, G.; Chandrasekaran, V.; and Papernot, N. 2022. Unrolling sgd: Understanding factors influencing machine unlearning. In 2022 IEEE 7th European Symposium on Security and Privacy (EuroS&P), 303–319. IEEE. Wang, P.; Bai, S.; Tan, S.; Wang, S.; Fan, Z.; Bai, J.; Chen, K.; Liu, X.; Wang, J.; Ge, W.; et al. 2024. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint arXiv:2409.12191. Wang, Y.; Liu, Y.; Shi, Y.; Li, C.; Pang, A.; Yang, S.; Yu, J.; and Ren, K. 2025. Discovering Influential Neuron Path in

Vision Transformers. In The Thirteenth International Conference on Learning Representations. Wu, G.; Hashemi, M.; and Srinivasa, C. 2022. Puma: Performance unchanged model augmentation for training data removal. In Proceedings of the AAAI conference on artificial intelligence, volume 36, 8675–8682. Wu, X.; Li, J.; Xu, M.; Dong, W.; Wu, S.; Bian, C.; and Xiong, D. 2023. DEPN: Detecting and Editing Privacy Neurons in Pretrained Language Models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, 2875–2886. Xing, S.; Zhao, F.; Wu, Z.; An, T.; Chen, W.; Li, C.; Zhang, J.; and Dai, X. 2024. EFUF: Efficient Fine-Grained Unlearning Framework for Mitigating Hallucinations in Multimodal Large Language Models. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, 1167–1181. Yang, T.; Dai, L.; Liu, Z.; Wang, X.; Jiang, M.; Tian, Y.; and Zhang, X. 2024. CLIPErase: Efficient Unlearning of Visual-Textual Associations in CLIP. arXiv preprint arXiv:2410.23330. Yao, Y.; Wang, P.; Tian, B.; Cheng, S.; Li, Z.; Deng, S.; Chen, H.; and Zhang, N. 2023. Editing Large Language Models: Problems, Methods, and Opportunities. In The 2023 Conference on Empirical Methods in Natural Language Processing. Zhang, R.; Lin, L.; Bai, Y.; and Mei, S. 2024. Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning. In First Conference on Language Modeling. Zhang, S.; Dong, L.; Li, X.; Zhang, S.; Sun, X.; Wang, S.; Li, J.; Hu, R.; Zhang, T.; Wu, F.; et al. 2023. Instruction tuning for large language models: A survey. arXiv preprint arXiv:2308.10792.

35597
