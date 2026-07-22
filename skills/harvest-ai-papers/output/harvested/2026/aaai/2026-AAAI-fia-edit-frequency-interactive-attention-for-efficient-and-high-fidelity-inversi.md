---
title: "FIA-Edit: Frequency-Interactive Attention for Efficient and High-Fidelity Inversion-Free Text-Guided Image Editing"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38145
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38145/42107
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# FIA-Edit: Frequency-Interactive Attention for Efficient and High-Fidelity Inversion-Free Text-Guided Image Editing

<!-- Page 1 -->

FIA-Edit: Frequency-Interactive Attention for Efficient and High-Fidelity

Inversion-Free Text-Guided Image Editing

Kaixiang Yang1, †, Boyang Shen1, †, Xin Li1, Yuchen Dai1, Yuxuan Luo1, Yueran Ma1

Wei Fang2, Qiang Li1, *, Zhiwei Wang1, *

1Huazhong University of Science and Technology 2Wuhan United Imaging Healthcare Surgical Technology Co., Ltd {kxyang, boyangshen, liqiang8, zwwang}@hust.edu.cn

## Abstract

Text-guided image editing has advanced rapidly with the rise of diffusion models. While flow-based inversion-free methods offer high efficiency by avoiding latent inversion, they often fail to effectively integrate source information, leading to poor background preservation, spatial inconsistencies, and over-editing due to the lack of effective integration of source information. In this paper, we present FIA- Edit, a novel inversion-free framework that achieves highfidelity and semantically precise edits through a Frequency- Interactive Attention. Specifically, we design two key components: (1) a Frequency Representation Interaction (FRI) module that enhances cross-domain alignment by exchanging frequency components between source and target features within self-attention, and (2) a Feature Injection (FIJ) module that explicitly incorporates source-side queries, keys, values, and text embeddings into the target branch’s crossattention to preserve structure and semantics. Comprehensive and extensive experiments demonstrate that FIA-Edit supports high-fidelity editing at low computational cost (∼6s per 512 × 512 image on an RTX 4090) and consistently outperforms existing methods across diverse tasks in visual quality, background fidelity, and controllability. Furthermore, we are the first to extend text-guided image editing to clinical applications. By synthesizing anatomically coherent hemorrhage variations in surgical images, FIA-Edit opens new opportunities for medical data augmentation and delivers significant gains in downstream bleeding classification.

Code — https://github.com/kk42yy/FIA-Edit

## Introduction

Text-guided image editing aims to modify an image according to a given textual description while preserving content unrelated to the edit. This task has witnessed significant progress in recent years, driven by the development of powerful generative models such as Denoising Diffusion Probabilistic Models (DDPMs) (Ho, Jain, and Abbeel 2020; Song, Meng, and Ermon 2020), Latent Diffusion Models (LDMs) (Rombach et al. 2022), and Diffusion Transformers (DiTs) (Peebles and Xie 2023; Labs 2024). These models

†Co-first authors. ∗Corresponding authors. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

SummerDay→AAAI 2026 Tulip→Lion

Ride a Lion Monkey→Man

Gold→Blue Add a girl

Cabin→Car Remove Paraglider

**Figure 1.** FIA-Edit is capable of handling a wide range of image editing tasks, including object modification, addition and removal, color transformation, and text replacement.

have been widely applied in real-world scenarios containing video editing (Geyer et al. 2023; Yoon et al. 2024; Gao et al. 2025; Yang et al. 2025; Cai et al. 2025; Li et al. 2025), visual effects production, and social media content creation.

Among these advances, tuning-free diffusion-based methods (e.g., DDIM-based sampling (Hertz et al. 2022; Tumanyan et al. 2023; Cao et al. 2023; Koo et al. 2024; Wu et al. 2024; Brooks, Holynski, and Efros 2023) and Rectified Flow (Avrahami et al. 2024; Deng et al. 2024; Rout et al. 2024; Wang et al. 2024; Hu et al. 2025)) have gained increasing attention. These approaches eliminate the need for per-instance fine-tuning, allowing for flexible and efficient zero-shot editing. Most existing methods fall into one of two categories, each presenting a fundamental trade-off

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

11613

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-001-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

Source Edited Source Edited (a) Inversion-based (b) Inversion-free: FlowEdit (c) Inversion-free: Ours

Inverted Noise

Inversion

Reconstruction

Editing

푣￿

￿￿￿ 푣￿

￿

푣￿

￿￿￿

Add Noise

Editing 푣￿

￿

Source Edited

푣￿

￿￿￿푣￿

￿푣￿

￿￿￿

Add Noise

Editing 푣￿

￿

Constraint

FIA Constraint

**Figure 2.** Overview of inversion-based and inversion-free image editing methods. (a) Inversion-based methods first invert the source image to noise, then edit from noise using the target prompt, often injecting source features during denoising. (b) Inversion-free methods bypass inversion by estimating velocity fields from noisy latent to source and noisy latent to target. Their difference defines the editing direction from source to target. However, this does not guarantee that the result preserves both background and target semantics (dark red ellipse). (c) Our method incorporates source-aware constraints (i.e., FIA Constraint) during the computation of the noisy latent to target velocity field vtar

t, effectively guiding the editing trajectory toward regions that preserve background fidelity while achieving semantic accuracy. Dashed arrows in (c) indicate FlowEdit, which lacks this guidance and fails to reach such optimal region.

between editing fidelity and computational efficiency.

The first and more established category adopts an inversion-first paradigm (Hertz et al. 2022; Tumanyan et al. 2023; Cao et al. 2023; Wu et al. 2024), where the source image is first projected into a latent prior distribution, typically Gaussian noise, using techniques such as DDIM inversion (Song, Meng, and Ermon 2020), Rectified Flow inversion (Lipman et al. 2022; Liu, Gong, and Liu 2022; Esser et al. 2024), or more advanced schemes (Miyake et al. 2025; Mokady et al. 2023). The editing process is then carried out in two stages: reconstructing the source image from the latent using the source prompt, and navigating from the same latent point to the target using the edited prompt. In this design, the prior distribution serves as a central “waypoint” that connects the source and target domains. To better align content and structure across the two branches, various feature interaction strategies including attention replacement and prompt injection have been proposed (see Fig. 2a). However, the inversion step is computationally intensive and significantly slows down the overall editing pipeline.

To improve efficiency, recent works have explored inversion-free approaches (Xu et al. 2023; Kulikov et al. 2024; Kim, Hong, and Ye 2025). These methods avoid explicit mapping to the latent prior and instead aim to directly construct the source-to-target trajectory. Since the sourceto-target path is not directly accessible, these methods introduce virtual intermediate states by injecting noise into the source image. From this noisy reference point, two velocity fields are estimated: one pointing back to the source using source-prompt and the other toward the target using targetprompt. The vector difference between these two flows serves as an approximation of the editing direction, which implicitly encodes the source-to-target semantic transforma- tion without ever performing an actual inversion. While this design enables much faster inference, it lacks explicit integration of source features during the editing process. As shown in Fig. 2b, this often results in poor content preservation in non-edited regions, leading to semantic drift, spatial inconsistency, and over-editing artifacts.

To address these limitations, we propose FIA-Edit (Fig. 2c), a novel inversion-free image editing framework that achieves high editing quality, strong background preservation, and fast generation. Instead of relying on an implicit feature transformation, FIA-Edit introduces an explicit feature-level interaction mechanism between the source and target representations throughout the editing trajectory. This design improves structural consistency and mitigates semantic drift in background regions.

The core of our method lies in a lightweight Frequency- Interactive Attention architecture. It contains two key modules: (1) The Frequency Representation Interaction (FRI) module, which fuses source and target features in the frequency domain within self-attention blocks, promoting cross-domain alignment without additional memory cost; (2) The Feature Injection (FIJ) module, which injects source-side queries, keys, values, and text embeddings into the cross-attention layers of the target branch, enhancing spatial and semantic consistency.

Our main contributions are summarized as follows:

• We propose FIA-Edit, an efficient and inversion-free image editing framework that achieves high-fidelity edits while explicitly preserving background structures. • We introduce a unified Frequency-Interactive Attention mechanism, consisting of the FRI and FIJ modules, which enable explicit feature-level interaction between source and target to improve content alignment and structural consistency. • We conduct extensive experiments on the PIE-Bench benchmark, and demonstrate that FIA-Edit achieves state-of-the-art performance across diverse editing tasks, with superior background preservation and semantic controllability. • To the best of our knowledge, we are the first to apply general-purpose text-guided image editing methods to clinical images. Moving beyond artistic manipulation, FIA-Edit enables anatomically meaningful modifications, such as adjusting bleeding severity in surgical scenes. This opens up new opportunities for using image editing tools in medical data augmentation and downstream clinical tasks.

Related Works 2.1 Inversion-based Methods Inversion-based image editing methods typically rely on first inverting the source image back into noise through an inversion process, and then performing editing conditioned on target prompts. Broadly, existing work in this category can be divided into three main directions:

Improvements to the inversion process. A number of approaches aim to enhance the quality, stability, and ac-

11614

![Figure extracted from page 2](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

curacy of the inversion process. In the DDIM-based setting, Null-Text Inversion (Mokady et al. 2023) demonstrates that effective inversion can be achieved without any textual prompt to suppress irrelevant content during reconstruction. For rectified flow–based approaches, methods such as RF- Inv (Rout et al. 2024) and FireFlow (Deng et al. 2024) focus on refining the inversion process to reduce reconstruction artifacts. Other methods, including Direct Inversion (Ju et al. 2023) and DNAEdit (Xie et al. 2025), aim to minimize the discrepancy between the actual and ideal inversion outputs, thereby boosting the quality of reconstruction.

Feature injection during editing. To improve controllability and fidelity, many tuning-free approaches incorporate feature injection mechanisms during the generation process. Prompt-to-Prompt (P2P) (Hertz et al. 2022) explores direct feature replacement within cross-attention layers, whereas Plug-and-Play (PnP) (Tumanyan et al. 2023) injects source features between residual and attention blocks to enhance background preservation. FTEdit (Xu et al. 2024) introduces semantic feature replacement within adaptive layer normalization modules, enabling more precise and disentangled control over the generated content.

Frequency-aware latent processing. Recent studies have increasingly explored the integration of frequency operations. FlexiEdit (Koo et al. 2024) suppresses highfrequency components in DDIM latents associated with editable regions, enabling non-rigid edits. FDS (Ren et al. 2025) adopts wavelet decomposition to adaptively select frequency bands according to the editing task, enabling finegrained control. Despite their effectiveness, these methods require an inversion process, increasing editing time and involving multiple task-specific hyperparameters.

## 2.2 Inversion-free Methods

To reduce the computational overhead of image editing, a natural direction is to eliminate the time-consuming inversion process. Several recent approaches have explored this idea by bypassing the explicit mapping of source images into the noise space. InfEdit (Xu et al. 2023) introduces the Denoising Diffusion Consistent Model (DDCM), which adopts a multi-step consistency sampling strategy that enables image editing without requiring explicit inversion. FlowEdit (Kulikov et al. 2024) further proposes an inversion-free framework by leveraging the velocity field to construct a direct trajectory from the source image to the edited target, avoiding inversion to Gaussian noise. Building on this, FlowAlign (Kim, Hong, and Ye 2025) introduces trajectory regularization to achieve more consistent and controllable text-driven editing within this inversionfree paradigm.

While these methods significantly reduce editing time, they often underutilize source image features, leading to insufficient background preservation and noticeable inconsistencies in non-edited regions. In contrast, we propose FIA- Edit, which enhances inversion-free editing by introducing frequency-aware feature interaction directly within the velocity field. This design effectively retains high-fidelity background information while ensuring both editing quality and runtime efficiency.

## Method

**Fig. 3.** illustrates the overall architecture of our method. As shown in Fig. 3a, our approach builds upon the inversionfree FlowEdit paradigm (Kulikov et al. 2024) as backbone. On this basis, we enhance the integration of relevant information from the source velocity field into the target velocity field, thereby improving both background preservation and semantic consistency during editing. Then, we detail the backbone and the proposed FIA Constraint, which consists of two sub-modules: Frequency Representation Interaction (FRI) and Feature Injection (FIJ).

## 3.1 Backbone

Our backbone is built upon Rectified Flow, which enables direct progression from the source domain to the target domain by estimating the difference between their respective velocity fields.

At a given discrete editing time step σt with index t, a linear interpolation is first employed between the source image Xsrc and Gaussian noise N(0, I), following the Rectified Flow formulation:

xsrc t = (1 −σt) · Xsrc + σt · ϵt, ϵt ∼N(0, I). (1)

Using the source prompt Psrc, corresponding source velocity vθ(xsrc t, Psrc, t) is computed. Next, to obtain the corresponding target velocity field, the current editing feature xF E t and the additive relationship of vectors xF E = Xsrc + xtar −xsrc are leveraged. Accordingly, the target representation at step t can be expressed as:

xtar t = xF E t + xsrc t −Xsrc. (2)

Target velocity vθ(xtar t, Ptar, t) is obtained with target prompt Ptar. It is worth noting that during the editing process, xsrc t and xtar t progressively move toward the source and target domains, respectively. At the initial step, the two are identical.

The direction is then determined by velocity difference:

v∆ t = vθ(xtar t, Ptar, t) −vθ(xsrc t, Psrc, t). (3)

As evident, the backbone relies solely on the implicit interaction between xsrc t and xtar t, without any explicit guidance from the source image features. This often causes the editing process to deviate toward the target domain too freely, leading to weak constraints from Xsrc and suboptimal results, especially in preserving source-relevant content.

Finally, the editing feature is updated iteratively according to the rectified flow stepping rule:

xF E t−1 = xF E t + (σt−1 −σt) · v∆ t. (4)

After completing all time steps, the edited image is synthesized from the final state xF E

0.

## 3.2 FIA Constraint

As shown in Fig. 3b, to better preserve background content and ensure semantic alignment, we explicitly incorporate source features into the computation of target velocity fields

11615

<!-- Page 4 -->

(b) FIA Constraint

(c) FRI Module

FFT

IFFT

FFT

ℱ￿￿￿

ℱ￿￿￿

ℒ

1 −ℒ

ℒ

1 −ℒ

ℱ￿￿￿￿

￿￿￿

ℱ￿￿￿

￿￿￿

휆￿ 휆￿

휆￿ 휆￿

ℱ￿￿￿

￿￿￿

ℱ￿￿￿￿

￿￿￿

+

+ ℱ￿￿￿￿￿ 푓￿￿￿￿￿

+ 푓￿￿￿

푓￿￿￿

Source Target 퐱￿

￿￿￿= 퐱￿

￿￿

퐱￿

￿￿￿

푣￿

￿￿￿

퐱￿

￿￿￿

푣￿

￿￿￿

FIA Constraint

퐱￿

￿￿

퐱￿

￿￿

(a) FIA-Edit

푣￿

￿

휎￿∙휖￿

퐱￿￿￿

￿￿

휖￿∼풩(ퟎ, 퐈) 퐱￿

￿￿￿

Source Velocity Field

❄

⋯ ⋯

퐱￿

￿￿￿

Target Velocity Field

❄

⋯ ⋯

FRI

FIJ

푣￿

￿￿￿ 푣￿

￿￿￿

(d) FIJ Module

Cross-Attention 푄￿￿￿퐾￿￿￿푉￿￿￿

Cross-Attention 푄￿￿￿퐾￿￿￿푉￿￿￿

퐞￿￿￿

퐞￿￿￿

Cross-Attention

퐞￿￿￿ 푄￿￿￿퐾￿￿￿푉￿￿￿

Self-Attention

푄￿￿￿ 퐾￿￿￿ 푉￿￿￿

Self-Attention

푄￿￿￿ 퐾￿￿￿ fri fri

푉￿￿￿ 푄￿￿￿ 퐾￿￿￿ fri Detail

**Figure 3.** Details of our framework. (a) Overview of FIA-Edit. During the computation of source and target velocity fields, we introduce the FIA constraint to enable interaction between source and target features. (b) FIA constraint. (c) Frequency Representation Interaction (FRI). FRI is integrated into the self-attention layers. Both source and target Q/K features are fused in the frequency domain, and the fused output replaces the target Q/K. The right side shows the detailed structure of the frequency-domain fusion module fri. (d) Feature Injection (FIJ). FIJ is used in the cross-attention layers in the latter of DiT.

through a proposed FIA Constraint. This constraint consists of two key components: (1) the FRI module, which operates within self-attention to enable frequency-domain interaction between source and target features, and (2) the FIJ module, applied in cross-attention to inject source features directly.

We denote the attention features extracted from vθ(xsrc t, Psrc, t) and vθ(xtar t, Ptar, t) as {f src t } and {f tar t }, respectively. Then, Eq. 3 can be reformulated as:

v∆ t = vθ(xtar t, Ptar, t, FIA({f src t }, {f tar t })) −vθ(xsrc t, Psrc, t) (5)

## 3.3 Frequency Representation Interaction

To preserve structural fidelity while enabling meaningful semantic transformation, we introduce the Frequency Representation Interaction (FRI) module, which performs crossdomain feature fusion in the frequency domain, as illustrated in Fig. 3c.

FRI is motivated by the observation that structure and semantics are more naturally disentangled in the frequency space: low-frequency components primarily encode coarse spatial layouts and background structures, while highfrequency components capture fine-grained textures and semantic details. Based on this insight, we propose a crossdomain frequency fusion strategy that enhances the highfrequency components of the source and the low-frequency components of the target, while suppressing low-frequency content in the source and high-frequency signals in the target. This selective fusion effectively leverages source information through frequency-domain interaction.

We first compute the velocity fields of xsrc t and xtar t, and extract the intermediate features f src t ∈RC×H×W and f tar t ∈RC×H×W from DiT. A 2D Fast Fourier Transform (FFT) FFT(·) is then applied:

Fsrc = FFT(f src t), Ftar = FFT(f tar t). (6)

Using a Gaussian low-pass filter L, we decompose each into high- and low-frequency components:

Fsrc high = Fsrc · (1 −L), Fsrc low = Fsrc · L, (7)

Ftar high = Ftar · (1 −L), Ftar low = Ftar · L. (8)

The fused spectrum is computed by applying crossweighted fusion:

Ffused = λ1 · (Fsrc high + Ftar low) + λ2 · (Fsrc low + Ftar high), (9)

where λ1 = 0.8, λ2 = 0.2 are weighting coefficients, emphasizing structure and semantics from source image while suppressing conflicting signals.

The fused feature is then reconstructed via inverse FFT:

f fused = IFFT(Ffused), (10)

which is then injected into the self-attention layers, guiding the target velocity updates. By aligning complementary information across domains, FRI allows our model to perform semantically accurate edits while preserving the source’s visual structure, improving both realism and control.

## 3.4 Feature Injection

To further improve background preservation, we draw inspiration from inversion-based methods (Tumanyan et al. 2023;

11616

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-004-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

Cao et al. 2023) that inject source features to maintain spatial consistency and fine-grained control. We propose a Feature Injection (FIJ) module (Fig. 3d) to explicitly introduce source features into the editing process.

Unlike prior works that inject only Q or K across the entire network, FIJ operates within the cross-attention layers of the later DiT blocks (i.e., layers 13 ∼23). Specifically, we inject source-side query (Qsrc), key (Ksrc), value (V src), and text embedding (esrc) into the target attention computation:

Qtar ←Qsrc, Ktar ←Ksrc, V tar ←V src, etar ←esrc.

(11) The injection is applied only during the early generation steps, when xtar t and xsrc t are still similar. This early fusion allows xtar t to absorb source information smoothly under Ptar’s guidance, enabling coherent edits and avoiding the abrupt changes seen in other methods. Additionally, FIJ stabilizes the semantic alignment between source and target prompts.

4 Experiment 4.1 Experiment Design Dataset and Baselines. To thoroughly evaluate the effectiveness of our proposed method, we conduct experiments on the PIE-Bench (Ju et al. 2023) benchmark, which comprises 700 image–prompt pairs spanning 10 diverse editing categories. We compare our approach with a comprehensive set of baselines, including: LDM-based methods (P2P (Hertz et al. 2022), PnP (Tumanyan et al. 2023), MasaCtrl (Cao et al. 2023), FlexiEdit (Koo et al. 2024), and FreeDiff (Wu et al. 2024)), FLUX-based approaches (RF-Inv (Rout et al. 2024), StableFlow (Avrahami et al. 2024), RF-Edit (Wang et al. 2024), and DCEdit (Hu et al. 2025)), and DiT-based methods (FTEdit (Xu et al. 2024), FlowEdit (Kulikov et al. 2024), and DNAEdit (Xie et al. 2025)). All models are evaluated using their publicly released implementations and default settings to ensure fair and consistent comparison.

Metrics. To comprehensively evaluate both editing performance and background preservation, we adopt six complementary metrics. Structure Distance (Tumanyan et al. 2022) quantifies structural consistency between the edited and original images. PSNR, LPIPS (Zhang et al. 2018), MSE, and SSIM (Wang et al. 2004) jointly assess content fidelity in unedited regions. For text-image alignment, we calculate CLIP similarity (Radford et al. 2021) over both the entire image and the specifically edited regions. Note that region masks provided by the dataset are used solely for evaluation purposes to isolate the edited areas.

Implementation Details. FIA-Edit is based on the SD3.5-Medium (Stability AI 2025) model with 50 sampling steps. Velocity fields are computed using CFG scales of 3.5 (source) and 13.5 (target). The FRI module is applied across all 50 steps, while the FIJ module is activated only during the first 27 steps to constrain early velocity field. During the xF E t stepping process, we add the reused interpolation noise ϵt with a scaling factor of σt. Details of the Gaussian lowpass filter are provided in the Appendix. All experiments are run on a single NVIDIA RTX 4090 GPU. For comparison, we reproduce results of open-source baselines using their official code and default settings (see Appendix for details), while results of non-released methods are directly reported from their original papers.

## 4.2 Comparisons with Other Editing Methods

Quantitative Comparison. As shown in Table 1, we conduct comprehensive evaluations on PIE-Bench across representative LDM-, FLUX-, and DiT-based methods. FIA-Edit achieves the best performance in background preservation while also demonstrating strong semantic alignment. Compared to the inversion-free baseline FlowEdit, our method preserves background details more accurately, highlighting the effectiveness of integrating source-target feature interactions during velocity field computation. Among inversionbased methods, P2P maintains relatively good background consistency but suffers from weak prompt alignment, suggesting that it overly retains source content. Overall, FIA- Edit delivers both superior background fidelity and precise semantic edits, leading to the best average ranking across all metrics, which validates the effectiveness of our approach.

Qualitative Comparison. Visual results are shown in Fig. 4, covering content alterations, object addition, and pose change. Our method produces high-quality, semantically accurate edits while maintaining background integrity. In contrast, other methods either fail to achieve the intended semantic change or suffer from noticeable background distortion (e.g., FlowEdit), clearly demonstrating the superiority of our approach.

GPU Memory and Runtime. We report GPU memory and runtime of open-source methods in Table 2, measured on a single RTX 4090 for fair comparison. Due to high memory demands, RF-Inv, StableFlow, and RF-Edit are tested on an A100 (80GB). Runtime is averaged over 10 samples (image size: 512 × 512), covering the full pipeline from loading to saving. As shown, inversion-free methods are notably faster. Compared to FlowEdit, our method incurs slightly more runtime due to feature interaction, while keeping memory usage comparable. Overall, FIA-Edit strikes a strong balance between quality and efficiency.

## 4.3 Ablation Study

We conduct ablations to evaluate the effectiveness of Frequency Representation Interaction (FRI) and Feature Injection (FIJ), as shown in Table 3. In FRI, freq denotes our frequency-domain fusion, while add refers to simple feature addition. Row 1 vs. Row 2 shows that FIJ greatly improves background preservation by injecting source features during velocity estimation. Row 2 vs. Row 4 indicates that combining FRI on top of FIJ further enhances semantic alignment while retaining strong background consistency, demonstrating the value of frequency-guided interaction. Row 3 vs. Row 4 shows that our structured freq design outperforms naive add. Note that CLIP score alone does not reflect editing quality, ideal edits require both high semantic fidelity and accurate background preservation. See Appendix for visual examples illustrating this balance.

11617

<!-- Page 6 -->

## Method

## Model

Structure Background Preservation CLIP Similarity Rank

Distance×103 ↓ PSNR ↑ LPIPS×103 ↓ MSE×104 ↓ SSIM×102 ↑ Whole ↑ Edited ↑ Avg. ↓

P2P SD1.4 11.652 27.222 54.551 32.863 84.76 25.02 22.10 5.3

PnP SD1.5 24.29 22.46 106.06 80.45 79.68 25.41 22.62 9.6

MasaCtrl SD1.4 24.70 22.64 87.94 81.09 81.33 24.38 21.35 10.7

FlexiEdit SD1.4 22.13 25.74 80.45 58.45 82.62 25.15 22.872 6.0

FreeDiff SD1.5 18.70 24.73 89.76 55.32 81.68 25.03 22.12 7.9

RF-Inv FLUX 48.76 19.51 195.85 155.74 68.95 25.11 22.50 11.6

StableFlow FLUX 19.24 23.04 76.94 84.85 87.22 24.30 21.28 8.9

RF-Edit FLUX 27.70 23.22 131.18 75.00 81.44 25.22 22.40 9.4

DCEdit FLUX 22.36 25.41 94.17 48.09 85.60 25.47 22.71 6.1

FTEdit SD3.5 18.17 26.62 80.55 40.24 91.501 25.743 22.27 4.43

FlowEdit SD3.5 23.62 23.21 93.81 69.95 85.09 26.781 23.731 6.1

DNAEdit SD3.5 14.193 26.663 74.573 32.762 88.633 25.63 22.71 3.12

Ours SD3.5 10.341 27.321 55.022 28.661 89.212 25.892 22.823 1.71

**Table 1.** Quantitative comparison on PIE-Bench. Rank denotes the average ranking across all evaluation metrics. Our method achieves strong performance in both background preservation and semantic alignment, yielding the best average rank. Superscripts 1, 2, and 3 denote the best, second-best, and third-best performance, respectively.

## Method

P2P PnP MasaCtrl FlexiEdit FreeDiff RF-Inv StableFlow RF-Edit FlowEdit Ours

GPU(GB) 10.95 8.99 11.42 18.73 6.08 69.22 35.39 32.91 17.93 17.93

Time(s) 34.84 18.09 21.71 38.97 17.41 76.74 26.07 34.51 3.49 6.30

**Table 2.** Memory and runtime comparison. RF-Inv, StableFlow, and RF-Edit were run on an A100 80GB GPU, while all other methods were tested on a single RTX 4090. Our approach achieves a favorable balance between speed and editing quality.

Module Structure Background Preservation CLIP Similarity

FIJ FRI Distance×103 ↓ PSNR ↑ LPIPS×103 ↓ MSE×104 ↓ SSIM×102 ↑ Whole ↑ Edited ↑

× × 23.62 23.21 93.81 69.95 85.09 26.78 23.73

✓ × 14.89 25.59 70.18 41.74 87.51 26.30 23.12

✓ add 16.50 25.93 85.44 38.72 86.51 26.05 22.68

✓ freq 10.34 27.32 55.02 28.66 89.21 25.89 22.82

**Table 3.** Ablation study on key components of FIA-Edit. FRI and FIJ denote the proposed Frequency Representation Interaction and Feature Injection modules, respectively. Within FRI, freq refers to our frequency-domain fusion design, while add denotes direct addition of source and target features.

## Method

ConvNeXt-T Aug PnP MasaCtrl FlexiEdit FreeDiff FlowEdit Ours

AUC (%) 81.54 82.10 81.98 84.22 82.05 82.25 83.83 85.05

PR-AUC (%) 38.66 38.81 38.53 38.82 37.97 38.60 40.34 43.81

Precision (%) 50.90 49.18 53.03 51.92 52.62 53.68 50.88 54.01

Recall (%) 29.49 30.84 26.57 27.17 26.03 25.65 31.44 32.90

F1-score (%) 37.35 37.91 35.40 35.67 34.83 34.71 38.86 40.89

Accuracy (%) 91.93 91.76 92.09 92.01 92.05 92.13 91.93 92.24

**Table 4.** Comparison of bleeding classification performance. All methods except ConvNeXt-T augment bleeding data with an additional ∼5,000 images. Aug denotes traditional augmentation. Ours significantly improves Recall, showing the value of editing-based augmentation. Bold: best; underline: second-best.

11618

<!-- Page 7 -->

an apple with two faces on it → an apple with two hands on it

Source PnP MasaCtrl FreeDiff Ours P2P StableFlow RF-Inv RF-Edit FlowEdit a cat sitting on a wooden chair → a dog sitting on a wooden chair a monkey wearing colorful goggles and scarf → a man wearing colorful goggles and scarf a small island with a tree → a small island with a tree and a girl panda bear sitting sitting on the ground → panda bear standing sitting on the ground

**Figure 4.** Qualitative comparison. Our method preserves the background while accurately reflecting the target semantics. White circles highlight cases where other methods poorly preserve non-editing regions.

## 5 Editing for Bleeding Classification Task Clinical

Motivation. Early detection of abnormal intraoperative bleeding is crucial yet challenging. Identifying early bleeding from surgical videos can assist surgeons in rapidly locating bleeding sites. However, such cases are rare, leading to severe data imbalance. Existing efforts on surgical image or video synthesis rarely address bleeding scenarios, let alone via image editing. To the best of our knowledge, we are the first to explore text-guided image editing for surgical bleeding augmentation. Our approach aims to enrich bleeding variations and mitigate data imbalance, ultimately improving downstream classification performance.

Experimental Setup. We use the Laparoscopic Rouxen-Y Gastric Bypass dataset (Bose et al. 2025) with 140 videos (100 for training, 40 for testing), sampled at 1fps for 770K frames. The training set includes 512K normal and 44K bleeding frames; the test set has 197K normal and 17K bleeding frames, indicating severe imbalance. We adopt ConvNeXt-T (Liu et al. 2022) as the classification backbone. From the training set, we extract 4,803 early-stage bleeding frames (∼50 per video) and edit them into varying bleeding levels (see Appendix). To ensure editing quality and efficiency, we compare four LDM-based and two inversionfree methods, plus standard augmentations (e.g., flipping, rotation). All editing models use SD 1.5 or 3.5 checkpoints without task-specific finetuning. The augmented images are incorporated into training set for downstream classification.

## Results

and Analysis. Quantitative results are shown in Table 4, with visualizations provided in the Appendix. Traditional augmentation methods yield only marginal gains despite generating an additional 5K frames. The four inversion-based methods improve precision but degrade recall, indicating reduced sensitivity to bleeding. This may stem from limited generation quality of SD1.5, potentially requiring domain-specific finetuning. In contrast, FlowEdit and our method both improve recall, suggesting better utility in enhancing bleeding classification. However, FlowEdit’s poor background preservation may lead to false positives. Benefiting from both semantic fidelity and structural consistency, our method achieves the most balanced performance, demonstrating the potential of image editing techniques for surgical data augmentation and downstream applications.

## 6 Conclusion We present FIA-Edit, a novel and efficient inversion-free image editing framework that introduces

Frequency-Interactive Attention for improved semantic alignment and background preservation. By explicitly modeling source-target interactions in both the frequency and spatial domains, our approach addresses key limitations of existing inversion-free methods, achieving high-quality, controllable image edits without costly inversion. To the best of our knowledge, we are the first to explore the use of generative image editing for clinical data augmentation. Specifically, we apply FIA- Edit to synthesize plausible variations of surgical bleeding images, resulting in improved performance on downstream classification task. This demonstrates the potential of controlled image editing in medical data scenarios, opening new avenues for future research. We hope our work contributes a new perspective to tuning-free editing and inspires broader exploration of generative techniques in real-world applications.

11619

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-26.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-29.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-34.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-36.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-37.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-38.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-39.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-41.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-42.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-44.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-45.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-46.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-47.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-49.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-fia-edit-frequency-interactive-attention-for-efficient-and-high-fidelity-inversi/page-007-figure-50.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by National Key R&D Program of China (Grant No. 2023YFC2414900), National Natural Science Foundation of China (Grant No.62202189), and research grants from Wuhan United Imaging Healthcare Surgical Technology Co., Ltd.

## References

Avrahami, O.; Patashnik, O.; Fried, O.; Nemchinov, E.; Aberman, K.; Lischinski, D.; and Cohen-Or, D. 2024. Stable Flow: Vital Layers for Training-Free Image Editing. arXiv preprint arXiv:2411.14430. Bose, R.; Nwoye, C. I.; Lazo, J.; Lavanchy, J. L.; and Padoy, N. 2025. Feature Mixing Approach for Detecting Intraoperative Adverse Events in Laparoscopic Roux-en-Y Gastric Bypass Surgery. arXiv preprint arXiv:2504.16749. Brooks, T.; Holynski, A.; and Efros, A. A. 2023. Instructpix2pix: Learning to follow image editing instructions. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 18392–18402. Cai, L.; Zhao, K.; Yuan, H.; Wang, X.; Zhang, Y.; and Huang, K. 2025. DFVEdit: Conditional Delta Flow Vector for Zero-shot Video Editing. arXiv preprint arXiv:2506.20967. Cao, M.; Wang, X.; Qi, Z.; Shan, Y.; Qie, X.; and Zheng, Y. 2023. Masactrl: Tuning-free mutual self-attention control for consistent image synthesis and editing. In Proceedings of the IEEE/CVF international conference on computer vision, 22560–22570. Deng, Y.; He, X.; Mei, C.; Wang, P.; and Tang, F. 2024. Fire- Flow: Fast Inversion of Rectified Flow for Image Semantic Editing. arXiv preprint arXiv:2412.07517. Esser, P.; Kulal, S.; Blattmann, A.; Entezari, R.; M¨uller, J.; Saini, H.; Levi, Y.; Lorenz, D.; Sauer, A.; Boesel, F.; et al. 2024. Scaling rectified flow transformers for high-resolution image synthesis. In Forty-first international conference on machine learning. Gao, J.; Yang, K.; Yao, X.; and Hu, Y. 2025. Unity in Diversity: Video Editing via Gradient-Latent Purification. In Proceedings of the Computer Vision and Pattern Recognition Conference, 23401–23411. Geyer, M.; Bar-Tal, O.; Bagon, S.; and Dekel, T. 2023. Tokenflow: Consistent diffusion features for consistent video editing. arXiv preprint arXiv:2307.10373. Hertz, A.; Mokady, R.; Tenenbaum, J.; Aberman, K.; Pritch, Y.; and Cohen-Or, D. 2022. Prompt-to-prompt image editing with cross attention control. arXiv preprint arXiv:2208.01626. Ho, J.; Jain, A.; and Abbeel, P. 2020. Denoising diffusion probabilistic models. Advances in neural information processing systems, 33: 6840–6851. Hu, Y.; Peng, J.; Lin, Y.; Liu, T.; Qu, X.; Liu, L.; Zhao, Y.; and Wei, Y. 2025. DCEdit: Dual-Level Controlled Image Editing via Precisely Localized Semantics. arXiv preprint arXiv:2503.16795.

Ju, X.; Zeng, A.; Bian, Y.; Liu, S.; and Xu, Q. 2023. Direct inversion: Boosting diffusion-based editing with 3 lines of code. arXiv preprint arXiv:2310.01506. Kim, J.; Hong, Y.; and Ye, J. C. 2025. FlowAlign: Trajectory-Regularized, Inversion-Free Flow-based Image Editing. arXiv preprint arXiv:2505.23145. Koo, G.; Yoon, S.; Hong, J. W.; and Yoo, C. D. 2024. Flexiedit: Frequency-aware latent refinement for enhanced nonrigid editing. In European Conference on Computer Vision, 363–379. Springer. Kulikov, V.; Kleiner, M.; Huberman-Spiegelglas, I.; and Michaeli, T. 2024. Flowedit: Inversion-free text-based editing using pre-trained flow models. arXiv preprint arXiv:2412.08629. Labs, B. F. 2024. FLUX. https://github.com/black-forestlabs/flux. Li, G.; Yang, Y.; Song, C.; and Zhang, C. 2025. FlowDirector: Training-Free Flow Steering for Precise Text-to-Video Editing. arXiv preprint arXiv:2506.05046. Lipman, Y.; Chen, R. T.; Ben-Hamu, H.; Nickel, M.; and Le, M. 2022. Flow matching for generative modeling. arXiv preprint arXiv:2210.02747. Liu, X.; Gong, C.; and Liu, Q. 2022. Flow straight and fast: Learning to generate and transfer data with rectified flow. arXiv preprint arXiv:2209.03003. Liu, Z.; Mao, H.; Wu, C.-Y.; Feichtenhofer, C.; Darrell, T.; and Xie, S. 2022. A convnet for the 2020s. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 11976–11986. Miyake, D.; Iohara, A.; Saito, Y.; and Tanaka, T. 2025. Negative-prompt inversion: Fast image inversion for editing with text-guided diffusion models. In 2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2063–2072. IEEE. Mokady, R.; Hertz, A.; Aberman, K.; Pritch, Y.; and Cohen- Or, D. 2023. Null-text inversion for editing real images using guided diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 6038–6047. Peebles, W.; and Xie, S. 2023. Scalable diffusion models with transformers. In Proceedings of the IEEE/CVF international conference on computer vision, 4195–4205. Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In International conference on machine learning, 8748–8763. PmLR. Ren, Y.; Jiang, Z.; Zhang, T.; Forchhammer, S.; and S¨usstrunk, S. 2025. FDS: Frequency-Aware Denoising Score for Text-Guided Latent Diffusion Image Editing. arXiv preprint arXiv:2503.19191. Rombach, R.; Blattmann, A.; Lorenz, D.; Esser, P.; and Ommer, B. 2022. High-resolution image synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 10684– 10695.

11620

<!-- Page 9 -->

Rout, L.; Chen, Y.; Ruiz, N.; Caramanis, C.; Shakkottai, S.; and Chu, W.-S. 2024. Semantic image inversion and editing using rectified stochastic differential equations. arXiv preprint arXiv:2410.10792. Song, J.; Meng, C.; and Ermon, S. 2020. Denoising diffusion implicit models. arXiv preprint arXiv:2010.02502. Stability AI. 2025. Stable Diffusion 3.5 Medium. Tumanyan, N.; Bar-Tal, O.; Bagon, S.; and Dekel, T. 2022. Splicing vit features for semantic appearance transfer. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 10748–10757. Tumanyan, N.; Geyer, M.; Bagon, S.; and Dekel, T. 2023. Plug-and-play diffusion features for text-driven image-toimage translation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1921– 1930. Wang, J.; Pu, J.; Qi, Z.; Guo, J.; Ma, Y.; Huang, N.; Chen, Y.; Li, X.; and Shan, Y. 2024. Taming rectified flow for inversion and editing. arXiv preprint arXiv:2411.04746. Wang, Z.; Bovik, A. C.; Sheikh, H. R.; and Simoncelli, E. P. 2004. Image quality assessment: from error visibility to structural similarity. IEEE transactions on image processing, 13(4): 600–612. Wu, W.; Fan, Q.; Qin, S.; Gu, H.; Zhao, R.; and Chan, A. B. 2024. FreeDiff: Progressive Frequency Truncation for Image Editing with Diffusion Models. In European Conference on Computer Vision, 194–209. Springer. Xie, C.; Li, M.; Li, S.; Wu, Y.; Yi, Q.; and Zhang, L. 2025. DNAEdit: Direct Noise Alignment for Text-Guided Rectified Flow Editing. arXiv preprint arXiv:2506.01430. Xu, P.; Jiang, B.; Hu, X.; Luo, D.; He, Q.; Zhang, J.; Wang, C.; Wu, Y.; Ling, C.; and Wang, B. 2024. Unveil Inversion and Invariance in Flow Transformer for Versatile Image Editing. arXiv preprint arXiv:2411.15843. Xu, S.; Huang, Y.; Pan, J.; Ma, Z.; and Chai, J. 2023. Inversion-free image editing with natural language. arXiv preprint arXiv:2312.04965. Yang, X.; Zhu, L.; Fan, H.; and Yang, Y. 2025. Videograin: Modulating space-time attention for multi-grained video editing. In The Thirteenth International Conference on Learning Representations. Yoon, S.; Koo, G.; Hong, J. W.; and Yoo, C. D. 2024. Dni: Dilutional noise initialization for diffusion video editing. In European Conference on Computer Vision, 180–195. Springer. Zhang, R.; Isola, P.; Efros, A. A.; Shechtman, E.; and Wang, O. 2018. The unreasonable effectiveness of deep features as a perceptual metric. In Proceedings of the IEEE conference on computer vision and pattern recognition, 586–595.

11621
