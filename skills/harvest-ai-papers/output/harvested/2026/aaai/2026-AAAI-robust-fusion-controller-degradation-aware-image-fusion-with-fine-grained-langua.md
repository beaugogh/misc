---
title: "Robust Fusion Controller: Degradation-Aware Image Fusion with Fine-Grained Language Instructions"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38240
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38240/42202
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Robust Fusion Controller: Degradation-Aware Image Fusion with Fine-Grained Language Instructions

<!-- Page 1 -->

Robust Fusion Controller: Degradation-Aware Image Fusion with Fine-Grained

Language Instructions

Hao Zhang1,2*, Yanping Zha1*, Qingwei Zhuang3, Zhenfeng Shao3, Jiayi Ma1†

1Electronic Information School, Wuhan University, China 2Suzhou Institute of Wuhan University, China 3State Key Laboratory of Information Engineering in Surveying Mapping and Remote Sensing, Wuhan University, China {zhpersonalbox, yanpingcha66, jyma2010}@gmail.com, {zhuangqingwei, shaozhenfeng}@whu.edu.cn

## Abstract

Current image fusion methods struggle to adapt to real-world environments encompassing diverse degradations with spatially varying characteristics. To address this challenge, we propose a robust fusion controller (RFC) capable of achieving degradation-aware image fusion through ﬁne-grained language instructions, ensuring its reliable application in adverse environments. Speciﬁcally, RFC ﬁrst parses language instructions to innovatively derive the functional condition and the spatial condition, where the former speciﬁes the degradation type to remove, while the latter deﬁnes its spatial coverage. Then, a composite control priori is generated through a multicondition coupling network, achieving a seamless transition from abstract language instructions to latent control variables. Subsequently, we design a hybrid attention-based fusion network to aggregate multi-modal information, in which the obtained composite control priori is deeply embedded to linearly modulate the intermediate fused features. To ensure the alignment between language instructions and control outcomes, we introduce a novel language-feature alignment loss, which constrains the consistency between feature-level gains and the composite control priori. Extensive experiments on publicly available datasets demonstrate that our RFC is robust against various composite degradations, particularly in highly challenging ﬂare scenarios.

Code — https://github.com/HaoZhang1018/RFC

## Introduction

Due to the limitation of the imaging principle, single-modal images can only capture partial scene attributes, failing to support comprehensive perception. In this context, image fusion technology emerges (Singh et al. 2023; Huang et al. 2024; Liu et al. 2024a,c), aiming to integrate complementary information from multi-modal images to provide a comprehensive representation of the imaging scene. Thanks to this excellent representational capability, image fusion has become a core component of numerous intelligent perception applications, effectively enhancing the accuracy of military reconnaissance (Muller and Narayanan 2009), autonomous driving (Yadav et al. 2020), etc.

*These authors contributed equally. †Corresponding author Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

“enhance the visibility of the image”

(a) Image Acquisition Process

Dual-Light Camera

Noise

Haze

Flash

Low-light

(b) Existing Fusion Methods

Fusion Network

Restoration

Network

Fusion Network +

(c) Our Fusion Method

0

Language-Feature Alignment Constraint

Multi- Condition

Coupling

Fusion Modulation

(d) Comparison VIS IR MRFS Ours (“remove the flare of the light”)

FISCNet SHIP

**Figure 1.** Comparisons between our RFC and existing fusion methods in the degraded scenario.

From the task deﬁnition, the application scenarios of image fusion typically involve environments where a single sensor is ineffective due to poor conditions. In the real world, such environments typically exhibit two key characteristics. On the one hand, degradations are pervasive (e.g., overexposure, low-light, noise, haze, blur, and ﬂare), with their types being diverse and severely compounded. On the other hand, these degradations exhibit spatially varying characteristics, potentially occurring both globally and locally. For instance, noise often appears in low-illumination regions, while ﬂares typically accompany light sources. Therefore, equipping fusion models with the ability to overcome spatial-varying composite degradations is crucial for ensuring their reliable application in the real world.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

12466

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-42.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-44.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-45.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-46.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-47.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-55.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-001-figure-58.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

Unfortunately, existing fusion methods struggle to meet this requirement, fundamentally hindering the practical application of image fusion technology. More concretely, mainstream fusion methods (Li and Wu 2018; Zhang and Demiris 2023; Ma et al. 2019; Tang, Yuan, and Ma 2022; Liu et al. 2024d) that focus solely on enhancing information aggregation capabilities essentially do not eliminate degradations. Instead, the persistent presence of degradations leads to the erroneous discarding of valuable information, rendering image fusion more akin to a problem of “information compression”. Differently, some of the latest methods (Zhang et al. 2024a; Chen et al. 2024; Zou and Yang 2023; Zhang et al. 2024c; Tang et al. 2023) cooperate to achieve degradation removal and information fusion, enabling the restoration of more information from lowquality source images. This perspective tends to turn image fusion into a problem of “information mining”. However, these methods can only handle a single type of degradation and are ineffective against composite degradations, let alone those with spatial variability.

To address these challenges, we propose a robust fusion controller, termed RFC. It derives a degradation-aware image fusion framework with ﬁne-grained language instructions, enabling adaptability to harsh environments with spatial-varying composite degradations. Firstly, RFC parses language instructions to obtain two complementary control conditions. 1) Functional condition: enables the speciﬁcation of the degradation type to be removed, supporting both single-type degradation removal and uniﬁed removal of composite degradations. 2) Spatial condition: deﬁnes the regions to be enhanced, supporting both local and global enhancement. Secondly, functional and spatial conditions are processed through a multi-condition coupling network, to generate composite control priori. This process translates abstract language instructions into latent control variables, providing a high-quality interactive medium for dynamically modulating the fusion process. Thirdly, the composite control priori is embedded into a hybrid attentionbased fusion network through the linear feature modulation strategy (Perez et al. 2018). While aggregating multi-modal information, it can precisely perceive and remove spatialvarying composite degradations. Finally, a novel languagefeature alignment loss is introduced. By constraining the consistency between feature-level gains and the composite control priori, it can ensure that the controlled output aligns with the expectations of the language instructions. As presented in Fig. 1, our RFC signiﬁcantly outperforms state-ofthe-art methods in terms of harsh scenario characterization, particularly in challenging ﬂare environments.

In summary, we make the following contributions:

• We propose a robust fusion controller, forming a degradation-aware image fusion framework with ﬁnegrained language instructions. To our knowledge, this is the ﬁrst attempt in the ﬁeld of image fusion to eliminate spatial-varying composite degradations, enhancing the robustness of fusion models in harsh environments.

• We design a novel generative mechanism for composite control priori, which can translate abstract language in- structions into latent control variables. This enables us to establish an open-ended paradigm for image fusion, facilitating ﬁne-grained functional control over arbitrary regions in accordance with user-deﬁned instructions. • A language-feature alignment loss is introduced, which drives feature gains to maintain potential consistency with composite control priori, strongly ensuring the modulation rationality of our RFC.

## Methodology

Our RFC leverages language instructions to guide fusion, ensuring high-quality multi-modal aggregation while accurately removing spatial-varying composite degradations. We ﬁrst parse instructions into functional and spatial conditions, deﬁning the desired operation and target regions. These are then coupled into a composite control priori, modulating hybrid attention fusion modules to achieve the desired results. The overall framework is shown in Fig. 2.

Language Instruction Parsing Given the input language instruction ζ, which expresses a composite requirement. First, we split ζ to obtain language fragments ζf that describe the functions (e.g., remove noise) and language fragments ζs that specify the spatial regions. Their semantic content differs signiﬁcantly, so we introduce two strategies to parse them separately. Speciﬁcally, ζf essentially represents a requirement for visual appearance, so we leverage the visual-text alignment capability of the CLIP (Radford et al. 2021) model to parse it:

α = ET (ζf), (1)

where ET is the text encoder from the pretrained CLIP, α indicates the obtained functional condition.

In contrast, ζs is more related to spatial localization, which cannot be handled by CLIP due to a lack of ﬁnegrained parsing capability. Thus, we use a powerful spatial parsing model, CLIPSeg (L¨uddecke and Ecker 2022), for analyzing language fragments ζs, to locate speciﬁc image regions based on language instructions: {Svis, Sir} = CSeg({Ivis, Iir}|ζs), where CSeg indicates the function of the pertained CLIPSeg, {Ivis, Iir} denotes the visible and infrared image pairs, and {Svis, Sir} represent the output spatial response maps. Considering that CLIPSeg is trained only on the visible modality, the location con- ﬁdence on multi-modal data may be reduced. Thus, we ﬁne-tune the CLIPSeg by unfreezing the parameters in the last convolutional layers Φc of its decoder. The ﬁnetuned spatial response maps are generated by {S

′ vis, S

′ ir} = CSegΦ′ c({Ivis, Iir}|ζs), where CSegΦ′ c is the ﬁne-tuned CLIPSeg. To combine the cross-modal priori knowledge before and after ﬁne-tuning, we perform spatial response mixing, obtaining a comprehensive spatial condition β:

β = Svis ⊕Sir ⊕S

′ vis ⊕S

′ ir, (2)

where ⊕is the concatenation operation. Now, through parsing the input language instruction, we obtain the functional condition α and the spatial condition β.

12467

<!-- Page 3 -->

“enhance the visibility of the car”

CLIP Text Encoder Projଵୈ

CLIPSeg

MCC Module 1 𝛼௪ଵ

Encoder1 Encoder2

HAF Module 1

… 𝜙௖

Image Fusion Decoder

…

4

Functional Condition 𝛼 𝛼௪ 𝛼௕ 𝛾௪ 𝛾௕

Multi-condition Coupling (MCC) Network

MCC Module 2 MCC Module 3 𝛾ௐ

ଵ 𝛼௪ଶ 𝛼௕

ଶ 𝛼௪ଷ 𝛼௕

ଷ Projଶୈ

Controllable Information Fusion

HAF Module 2 HAF Module 4 𝛼௕

ଵ 𝛾௕

ଵ 𝛾ௐ

ଶ 𝛾௕

ଶ 𝛾ௐ

ସ 𝛾௕

ସ

Composite Control Priori

Functional Affine Variables 𝛾

Hybrid Affine Variables

Spatial Condition β

**Figure 2.** The overall framework of our proposed RFC.

Composite Control Priori Generation Effective control of the fusion process necessitates a variable that captures both functional and spatial conditions. Inspired by FiLM (Perez et al. 2018), we design multi-condition coupling (MCC) modules to combine α and β following the idea of feature-wise afﬁne transformation, as shown in Fig. 3.

We ﬁrst use two 1D convolution layers to generate functional afﬁne variables: {αi w, αi b} = Proji

1D(α), where αi w indicates the functional weight, αi b denotes the functional bias, and i is the index of the multi-condition coupling module. Then, we perform an afﬁne transformation (AT) for a functional compound and combine it with the spatial condition: AT(·|αi w, αi b) ⊕β. Such an operation ensures that the functional and spatial conditions are fully coupled, serving as the core component of the MCC module. The function of the MCC module can be represented as:

F i out = MCC(F i−1 out, AT(·|αi w, αi b) ⊕β), (3)

where F i−1 out is the composite control priori output from the i −1-th MCC module, and when i = 1, F i−1 out = β. Totally, 3 MCC modules are used, and the output F 3 out of the last module is regarded as the composite control priori γ. It then undergoes 2D convolution to produce ﬁnal hybrid afﬁne variables {γk w, γk b } = Projk

2D(γ), which can be considered to fully integrate both functional and spatial conditions.

Controllable Information Fusion Next, the task at hand is to enable high-quality multi-modal feature fusion and seamlessly embed the generated compos-

Conv2d

Leaky 𝛼௪௜ 𝛼௕

௜ c

Conv2d

Leaky 𝛽

**Figure 3.** The structure of multi-condition coupling module.

ite control priori into the fusion process. We develop hybrid attention fusion (HAF) modules based on CBAM (Woo et al. 2018) to achieve this goal, as illustrated in Fig. 4. First, we employ the channel attention mechanism to blend infrared and visible features. Formally, we use pooling operations to squeeze the input feature F, obtaining the maximum and average responses along the spatial dimensions, respectively. These responses are processed by a multi-layer perceptron (MLP), combined through summation, and subjected to a nonlinear activation to produce the ﬁnal attention map, which is used to enhance the aggregated feature F. This process can be represented as:

F k c = σ(κ(PM(F k−1)) + κ(PA(F k−1))) ⊗F k−1, (4)

where F k−1 is the feature output from the k −1-th HAF module, and when k = 1, F k−1 = Fir ⊕Fvis. PM and PA denote the maximum and average pooling, κ indicates the MLP function, and σ indicates the Sigmoid function. Building on it, the spatial attention mechanism is utilized to reinforce the spatial representation of fused features F k c. Concretely, pooling operations are applied to F k c to extract the maximum and average responses in the channel dimen-

12468

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-46.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-47.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-57.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-003-figure-93.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

MLP

AvgPool

[MaxPool, AvgPool] 𝛾௪௞ 𝛾௕

௞

Spatial Attention Channel Attention

MaxPool

𝐹ୱ,௖ ௞ 𝐹௖௞

𝐹

**Figure 4.** The structure of hybrid attention fusion module.

sion, which are subsequently concatenated, projected, and activated to produce the spatial attention map. The spatial attention-based reinforcement process can be deﬁned as:

F k c,s = σ(κ(PA(F k c) ⊕PM(F k c))) ⊗F k c, (5)

where F k c,s is the fused feature that has been attentionenhanced across both the spatial and channel dimensions. For embedding the composite control priori, we still follow the idea of feature-wise afﬁne transformation. Speciﬁcally, we use the afﬁne variables {γk w, γk b } to process F k c,s:

F k control = AT(F k c,s|γk w, γk b) + F k−1. (6)

Finally, an UNet-like (Ronneberger, Fischer, and Brox 2015) decoder DU with skip connections is employed to reconstruct the fused image: If = DU(F 1 control, F 2 control, F 3 control, F 4 control).

Optimization Regularization The above designs offer the architectural support for robust image fusion with ﬁne-grained language instructions. To ensure their effective operation, we formulate optimization regularization, comprising a degradation-aware reconstruction loss and a language-feature alignment loss. Degradation-Aware Reconstruction Loss. This regularization term aims to drive the targeted removal of degradations, enhancing perceptual ﬁdelity. The data used to construct this loss is multi-modal clean-degraded image pairs {Ivis, Iir, I

′ vis, I

′ ir}, where Ivis and Iir are degraded images, and I

′ vis and I

′ ir are corresponding clean ones. Based on the input language instruction ζ, we identify two conditions: the degradation type Ω(e.g, low-light, ﬂare, haze, noise, blur, and their composites) and the target region Λ (can be either a local region or the entire image). Firstly, according to Ω, we retrieve {IΩ vis, IΩ ir} that includes this speciﬁc degradation (or a compound of multiple types of degradation) from the dataset. Secondly, in conjunction with Λ, we simulate pseudo multi-modal references:

{ˆIvis, ˆIir} = {IΩ vis, IΩ ir}Λ + {I

′ vis, I

′ ir}Λ, (7)

where Λ indicate regions that are not speciﬁed by language instruction ζ. With the pseudo multi-modal references in place, we construct the degradation-aware reconstruction loss to constrain the ﬁnal fused image If from three aspects: contrast, structure, and color: Lrec = Lcon + Lstr + Lcor. The corresponding loss terms are deﬁned as:

Lcon=

X α{Λ,Λ}∥Iy f −max({ˆIy vis,ˆIir})∥{Λ,Λ}, (8)

Feature Difference

Control Priori 𝛾 Cosine Similarity

1

0

“enhance the visibility of the car”

“enhance the visibility of the image”

“reduce the noise of the tree”

“enhance the light of the road”

**Figure 5.** Schematic diagram of the alignment mechanism between feature-level gains and language instructions.

Lstr=

X α{Λ,Λ}∥∇Iy f −max({∇ˆIy vis,∇ˆIir})∥{Λ,Λ}, (9)

Lcor =

X α{Λ,Λ}∥Icbcr f −ˆIcbcr vis ∥{Λ,Λ}, (10)

where superscripts y and cbcr denote the illumination and chrominance channels, respectively. We use dynamic weights α{Λ,Λ} to distinctively handle the distance calculations for the language-speciﬁed region Λ and other regions Λ. The dynamic weights are deﬁned as αΛ = Υ(If)/Υ(Λ), in which Υ is an operator that calculates the number of pixels in speciﬁc regions. Such a mechanism can prevent the limitation of the target region from being overlooked during the optimization process when its size is too small. Language-Feature Alignment Loss. Through the above loss, the dynamic responsiveness of the ﬁnal fused image to language instructions can be effectively driven. However, the internal fusion process still lacks constraints, which potentially compromises the fusion model’s sensitivity to language instructions. Thus, we introduce a novel languagefeature alignment loss, primarily ensuring that the featurelevel gains introduced by HAF modules remain consistent with the composite control priori. As shown in Fig. 5, we calculate the residual between the input of the ﬁrst HAF module and the output of the ﬁnal HAF module, representing the feature-level gains by the composite control priori: ∆F = F 0 control −F 4 control = Fir ⊕Fvis −F 4 control. Then, the language-feature alignment loss is deﬁned as:

Lali = 1 − ⟨τ(γ), τ(∆F)⟩ |τ(γ)| × |τ(∆F|), (11)

12469

![Figure extracted from page 4](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-004-figure-38.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-004-figure-39.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-004-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-004-figure-41.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-004-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

“reduce the noise of the car” “enhance the light of the tree” VIS IR w/o text “enhance the visibility of the building”

(b) Local

“reduce the haze of the image” VIS “enhance the visibility of the image” IR w/o text “reduce the noise of the image”

(a) Global

**Figure 6.** Demonstrating global and local degradation-aware fusion ability of our RFC.

where τ is the ﬂattening operator, and ⟨·⟩is the vector dot product. This loss effectively ensures the rationality of the intermediate fusion processes under language instructions.

## Experiments

Experimental Conﬁgurations Datasets. We construct the required training and testing dataset based on MFNet (Ha et al. 2017), LLVIP (Jia et al. 2021), M3FD (Liu et al. 2022), FMB (Liu et al. 2023), and RoadScene (Xu et al. 2020) datasets. Speciﬁcally, we extend these existing datasets with simulated degradations (e.g, low light, ﬂare, haze, noise, blur, and their composites). Our training set includes 14, 654 image-text pairs with annotations specifying degradation types and regions. Testing employs 700 multi-modal image pairs. Implementation. We use the AdamW optimizer with an initial learning rate 2e−4 to update the parameters of all network modules. Meanwhile, the multi-scale training strategy is adopted to enhance our RFC’s generalization performance across images of varying scales. All experiments are conducted on four NVIDIA Tesla P100 GPUs with 16 GB memory and one Intel(R) Xeon(R) Gold 5117 CPU.

Robust Fusion Controller Validation First, we demonstrate our method’s capability as a robust fusion controller that effectively removes degradation artifacts during the fusion process, both globally and locally. Global Degradation-Aware Fusion. As shown in Fig. 6 (a), our RFC achieves global degradation removal under different language instructions. For instance, instructions like “reduce the noise” selectively suppress noise while preserving other characteristics, whereas “enhance the visibility” eliminates composite degradations, producing a completely clean output. This highlights RFC’s capability to interpret language instructions for targeted enhancement precisely. Local Degradation-Aware Fusion. Our RFC also supports local degradation removal, addressing practical needs such as enhancing key objects (e.g., cars, pedestrians). As shown in Fig. 6 (b), when an instruction speciﬁes both the degradation type and target region, RFC selectively restores the

VIS IR “remove the flare of the light” w/o text

**Figure 7.** The ﬂare removal function of our RFC.

designated areas while maintaining contextual consistency. Flare Removal. In nighttime driving scenarios, lens ﬂare degrades image quality, impairing visibility. As a highlight, our RFC mitigates ﬂare artifacts through language-driven modulation in Fig. 7, leveraging infrared cues to compensate for overexposed regions. This results in robustness improvements to produce perceptually superior fused results.

Comparison Under Composite Degradations We ﬁrst compared RFC with nine SOTA methods under composite-degradation scenarios, including MRFS (Zhang et al. 2024b), CDDFuse (Zhao et al. 2023a), DDFM (Zhao et al. 2023b), CAF (Liu et al. 2024b), SHIP (Zheng et al. 2024a), FISCNet (Zheng et al. 2024b), ReFusion (Bai et al. 2024), SDCFusion (Liu et al. 2024e), and Text-IF (Yi et al. 2024). For methods without degradation removal capabilities, we use an all-in-one enhancement method, InstructIR (Conde, Geigle, and Timofte 2024) for pre-processing. For Text-IF, we inform it of all the types of degradation present in the source images through textual input. Our RFC is tested with the default instruction: “enhance the visibility of the image”. Visual results in Fig. 8 highlight RFC’s advantages in handling composite degradations. For example, the competitors all fail to handle the noise that is introduced

12470

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-34.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-39.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-41.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-42.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-49.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-50.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-51.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-54.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-57.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-58.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-59.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-63.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-69.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-005-figure-70.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

VIS Ins. + CAF Ins. + CDD. Ins. + DDF. Ins. + FIS. IR

Ins. + MRF. Ins. + SHI. Ours (“enhance visibility...”) Ins. + ReF. Ins. + SDC. Tex.

**Figure 8.** Qualitative results under composite degradations.

VIS CAF CDDFuse DDFM FISCNet IR

MRFS SHIP Ours (“enhance visibility...”) ReFusion SDCFusion Text-IF

**Figure 9.** Qualitative results under no degradation. The highlighted area at the bottom represents the residual maps between fused results and the source visible image.

Degradation DDF. SHI. CDD. MRF. CAF ReF. FIS. SDC. Tex. Ours Qabf 0.25 0.41 0.39 0.24 0.32 0.43 0.43 0.43 0.38 0.45 SSIM 0.27 0.27 0.29 0.25 0.28 0.29 0.27 0.28 0.23 0.32 MI 2.29 2.53 2.73 2.47 2.34 2.62 2.40 2.38 2.22 2.79 VIF 0.44 0.45 0.48 0.42 0.44 0.49 0.46 0.49 0.39 0.50 SCD 1.35 1.06 1.27 1.16 1.25 1.26 1.04 1.24 1.04 1.28

**Table 1.** Quantitative results under composite degradations.

No-Degra. DDF. SHI. CDD. MRF. CAF ReF. FIS. SDC. Tex. Ours SD 37.18 46.54 49.16 46.83 39.65 48.19 48.63 47.04 50.89 49.90 AG 4.40 7.37 6.96 5.16 6.23 7.30 7.79 7.32 7.62 9.78 EN 6.99 7.24 7.28 7.24 7.03 7.30 7.31 7.29 7.35 7.36 SF 12.48 21.28 20.71 14.66 21.65 21.27 22.26 21.07 22.14 26.62

**Table 2.** Quantitative results under no degradation.

when enhancing illumination. In contrast, our RFC effectively removes composite degradations, while preserving the saliency of the pedestrian and the ﬁne details in the background. Furthermore, we use ﬁve full-reference metrics to compute the correlation between the fused result and source images, as shown in Table 1. Our RFC outperforms other methods on most metrics, showing its ability to retain key scene information.

Comparison Under No Degradation Beyond removing degradations, our RFC can further generate additional textures in degradation-free environments with the instruction “enhance the details of the image”. As shown in Fig. 9, the residual maps between fused results and the source visible image reveal that RFC retains more highfrequency information in areas like trees and grass, while preserving richer thermal radiation in the human region. Since RFC achieves information generation beyond source images in degradation-free scenarios, full-reference metrics in Table 1 are no longer applicable. Instead, we employ four no-reference metrics for objective evaluation. In Table 2, our method achieves the best scores on most metrics.

Vis. Ins. + CAF Ins. + CDD. Ins. + DDF. Ins. + FIS. Inf.

Ins. + MRF. Ins. + SHI. Ours (“enhance visibility...”) Ins. + ReF. Ins. + SDC. Tex.

**Figure 10.** Qualitative results of generalization experiment.

w/ 𝐿௔௟௜ w/o 𝐿௔௟௜ VIS & IR

“enhance the visibility of the image”

ℒ௔௟௜

ℒ௥௘௖

ℒ௔௟௜ ℒ௥௘௖ (w/ ℒ௔௟௜) ℒ௥௘௖ (w/o ℒ௔௟௜)

1.5

7.5

4.5

0.6

1.1

0.9

Step1

**Figure 11.** Ablation on language-feature alignment loss.

w/o α VIS & IR

“reduce…noise

…image”

“enhance…light

…image” w/o β w/ α and β w/o α w/o β

No change: functional control failed No change: spatial control failed

Distinct control successful

“enhance…light

…bus”

**Figure 12.** Ablation on functional and spatial conditions.

General. DDF. SHI. CDD. MRF. CAF ReF. FIS. SDC. Tex. Ours Qabf 0.30 0.48 0.47 0.42 0.24 0.48 0.49 0.49 0.52 0.54 SSIM 0.26 0.22 0.22 0.30 0.19 0.24 0.23 0.26 0.26 0.31 MI 2.39 2.60 2.77 2.98 1.97 2.76 2.68 2.62 2.68 2.44 VIF 0.35 0.33 0.33 0.39 0.21 0.34 0.34 0.35 0.38 0.40 SCD 1.34 1.09 1.13 1.45 1.02 1.14 1.12 1.25 1.19 1.39

**Table 3.** Quantitative results of generalization experiment.

Generalization Experiment

Besides, we conduct generalization experiments on the M3SVD dataset (Tang et al. 2025), which contains realcaptured degraded data using the MAG64AI camera. As shown in Fig. 10 and Table 3, RFC outperforms others in both visual quality and objective scores, demonstrating its strong generalization ability across diverse fusion scenarios.

Ablation Studies

Language-Feature Alignment Loss. Lali is directly removed for verifying its role. As shown in Fig. 11, removing Lali hinders full alignment with language instructions, leaving artifacts due to incomplete degradation removal. This can be attributed to the facilitating effect of Lali on the reconstruction loss Lrec. Speciﬁcally, Lali aligns internal feature changes with the instruction, while Lrec enforces pixellevel consistency with the instruction-speciﬁed appearance. With the shared goal of ensuring the output faithfully follows the instruction, Lali can help Lrec achieve better optimization, as shown in Fig. 11. The quantitative results in Table 4 also demonstrate the importance of Lali. Functional and Spatial Conditions. We remove functional condition α and spatial condition β from the FiLM-inspired

12471

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-26.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-37.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-59.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-70.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-77.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-78.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-79.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-80.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-81.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-82.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-83.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-84.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-93.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-98.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-99.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-100.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-101.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-102.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-103.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-104.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-105.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-106.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-107.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-110.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-112.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-123.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-125.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-126.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-127.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-006-figure-128.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

VIS IR Fea. w/o fine-tuning

Resu. w/o fine-tuning

Fea.w/ fine-tuning

Resu. w/ fine-tuning

“enhance the visibility of the image”

**Figure 13.** Ablation on ﬁne-tuning CLIPSeg.

VIS CAF CDD. DDF. FIS.

Tex. SHI. SDC. ReF. Ours MRF.

IR

**Figure 14.** Qualitative object detection veriﬁcation.

VIS&IR CAF CDD. DDF. FIS. MRF.

Tex. SHI. SDC. ReF. Ours GT

**Figure 15.** Qualitative semantic segmentation veriﬁcation.

MCC module, respectively. As shown in Fig. 12. When removing α, RFC loses the ability to perform the speciﬁed degradation removal function. When removing β, RFC cannot specify regions for target processing. In contrast, RFC responds correctly only when both α and β are present. At this time, RFC is capable of accurately localizing the speciﬁed spatial regions while achieving the desired function of degradation removal. Fine-Tuning CLIPSeg. Fine-tuning is applied to the decoder’s last convolutional layers in CLIPSeg to adapt to multi-modal data, thereby improving both local localization and global perception. As shown in Fig. 13, ﬁne-tuning enables image-wide responses and effective removal of global degradations, which are not present before ﬁne-tuning. Additionally, the quantitative results in Table 4 show that removing ﬁne-tuning leads to a decline in fusion performance. The Number of Modules. In this work, we use three MCC modules to generate variables that capture both functional and spatial conditions, and use four HAF modules to embed the composite control priori into the fusion process. To verify the rationality of this conﬁguration, we conduct an ablation study on the number of modules. As shown in Table 4, we evaluate the performance under different settings, using 2, 3, and 4 MCC modules and 3, 4, and 5 HAF modules, respectively. Our method achieves the best fusion performance with the conﬁguration of 3 MCC & 4 HAF modules.

Semantic Veriﬁcation on High-Level Tasks

Object Detection. We implement object detection on the LLVIP dataset with YOLO-v5, in which the detector is retrained on the results of these fusion methods and the source

Ablation SSIM MI VIF SCD Qabf w/o Lali 0.324 2.815 0.484 1.242 0.465 w/o Fine-tuning 0.321 2.817 0.479 1.226 0.460 2 MCC & 4 HAF 0.320 2.749 0.476 1.220 0.431 4 MCC & 4 HAF 0.323 2.687 0.474 1.172 0.439 3 HAF & 3 MCC 0.319 2.725 0.481 1.197 0.440 5 HAF & 3 MCC 0.324 2.732 0.487 1.193 0.435 Full Model (3 MCC & 4 HAF) 0.325 2.867 0.485 1.242 0.469

**Table 4.** Quantitative results of ablation studies.

LLVIP Precision Recall mAP@0.6 mAP@0.85 mAP@(0.5:0.95) VIS 79.0 62.5 65.4 50.6 53.5 IR 90.2 78.1 71.2 51.0 54.7 DDFM 95.6 85.8 85.4 61.7 71.1 SHIP 93.0 87.1 72.2 55.8 61.5 CDDFuse 93.9 89.0 80.6 52.8 65.5 MRFS 94.1 82.8 83.3 60.7 74.4 CAF 94.7 86.2 79.2 57.7 65.9 ReFusion 96.0 91.0 77.8 55.0 60.7 FISCNet 93.6 89.0 72.2 52.4 56.8 SDCFusion 93.2 88.6 72.2 53.5 56.4 Text-IF 96.0 90.9 79.5 58.3 64.8 Ours 96.7 90.2 87.5 61.5 75.3

**Table 5.** Quantitative object detection veriﬁcation.

FMB DDF. SHI. CDD. MRF. CAF ReF. FIS. SDC. Tex. Ours Vegetation 42.12 48.67 49.28 73.16 40.83 50.32 50.89 49.76 43.64 75.18 Building 56.81 62.01 60.18 78.7 55.42 62.4 60.73 59.27 53.24 81.38 Person 50.25 48.67 42.69 52.45 41.03 42.77 31.7 33.02 34.37 49.86 Car 70.63 75.07 72.61 77.66 70.21 74.66 73.91 72.59 70.71 77.59 Sky 54.39 67.34 69.28 90.5 50.3 69.94 72.3 71.13 58.19 89.6 mIoU 52.15 56.37 56.61 67.54 50.64 57.79 57.24 57.65 51.79 67.01

**Table 6.** Quantitative semantic segmentation veriﬁcation.

images. As shown in Fig. 14 and Table 5, our RFC surpasses all competitors in detection accuracy, demonstrating its ability to improve high-level semantic tasks. Notably, detection performance based on the fused images outperforms those based on the source images, highlighting the value of the image fusion technology. Semantic Segmentation. We retrain SegFormer (Xie et al. 2021) on the FMB dataset and apply it to the fused results of each method. As shown in Fig. 15 and Table 6, RFC achieves superior segmentation performance across multiple categories, with results second only to MRFS. This is because MRFS is a speciﬁc method designed for the collaboration of image fusion and semantic segmentation.

## Conclusion

This study proposes a robust fusion controller, termed RFC. It can achieve degradation-aware image fusion with ﬁnegrained language instructions, improving the fusion model’s robustness in harsh environments with spatial-varying composite degradations. RFC parses language instructions into functional and spatial conditions, and couples them to obtain the composite control priori. With the continuous modulation of this priori on the fusion process, combined with the guidance of the language-feature alignment loss, RFC can eliminate composite degradations according to language instructions. Extensive experiments demonstrate RFC’s superiority in both perceptual performance and semantic quality.

12472

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-29.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-34.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-36.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-37.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-38.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-39.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-47.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-53.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-54.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-55.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-56.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-57.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-58.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-robust-fusion-controller-degradation-aware-image-fusion-with-fine-grained-langua/page-007-figure-59.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Natural Science Foundation of China (62506268, 62276192), the Fundamental Research Funds for the Central Universities (2042024kf0038), the Natural Science Foundation of Jiangsu Province (BK20250454), and the Postdoctoral Fellowship Program of CPSF (GZB20250066).

## References

Bai, H.; Zhao, Z.; Zhang, J.; Wu, Y.; Deng, L.; Cui, Y.; Jiang, B.; and Xu, S. 2024. ReFusion: Learning image fusion from reconstruction with learnable loss via meta-learning. International Journal of Computer Vision, 1: 1–21. Chen, J.; Yang, L.; Liu, W.; Tian, X.; and Ma, J. 2024. Lenfusion: A joint low-light enhancement and fusion network for nighttime infrared and visible image fusion. IEEE Transactions on Instrumentation and Measurement, 73: 5018715. Conde, M. V.; Geigle, G.; and Timofte, R. 2024. Instructir: High-quality image restoration following human instructions. In Proceedings of the European Conference on Computer Vision, 1–21. Ha, Q.; Watanabe, K.; Karasawa, T.; Ushiku, Y.; and Harada, T. 2017. MFNet: Towards real-time semantic segmentation for autonomous vehicles with multi-spectral scenes. In Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems, 5108–5115. Huang, Q.; Wu, G.; Jiang, Z.; Fan, W.; Xu, B.; and Liu, J. 2024. Leveraging a self-adaptive mean teacher model for semi-supervised multi-exposure image fusion. Information Fusion, 112: 102534. Jia, X.; Zhu, C.; Li, M.; Tang, W.; and Zhou, W. 2021. LLVIP: A visible-infrared paired dataset for low-light vision. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 3496–3504. Li, H.; and Wu, X.-J. 2018. DenseFuse: A fusion approach to infrared and visible images. IEEE Transactions on Image Processing, 28: 2614–2623. Liu, J.; Fan, X.; Huang, Z.; Wu, G.; Liu, R.; Zhong, W.; and Luo, Z. 2022. Target-aware dual adversarial learning and a multi-scenario multi-modality benchmark to fuse infrared and visible for object detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 5802–5811. Liu, J.; Lin, R.; Wu, G.; Liu, R.; Luo, Z.; and Fan, X. 2024a. Coconet: Coupled contrastive learning network with multilevel feature ensemble for multi-modality image fusion. International Journal of Computer Vision, 132(5): 1748–1775. Liu, J.; Liu, Z.; Wu, G.; Ma, L.; Liu, R.; Zhong, W.; Luo, Z.; and Fan, X. 2023. Multi-interactive feature learning and a full-time multi-modality benchmark for image fusion and segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 8115–8124. Liu, J.; Wu, G.; Liu, Z.; Ma, L.; Liu, R.; and Fan, X. 2024b. Where elegance meets precision: Towards a compact, automatic, and ﬂexible framework for multi-modality image fu- sion and applications. In Proceedings of the International Joint Conference on Artiﬁcial Intelligence, 1110–1118. Liu, J.; Wu, G.; Liu, Z.; Wang, D.; Jiang, Z.; Ma, L.; Zhong, W.; and Fan, X. 2024c. Infrared and Visible Image Ffusion: From Data Compatibility to Task Adaption. IEEE Transactions on Pattern Analysis and Machine Intelligence, 47(4): 2349–2369. Liu, R.; Liu, Z.; Liu, J.; Fan, X.; and Luo, Z. 2024d. A taskguided, implicitly-searched and metainitialized deep model for image fusion. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(10): 6594–6609. Liu, X.; Huo, H.; Li, J.; Pang, S.; and Zheng, B. 2024e. A semantic-driven coupled network for infrared and visible image fusion. Information Fusion, 108: 102352. L¨uddecke, T.; and Ecker, A. 2022. Image segmentation using text and image prompts. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 7086–7096. Ma, J.; Yu, W.; Liang, P.; Li, C.; and Jiang, J. 2019. FusionGAN: A generative adversarial network for infrared and visible image fusion. Information Fusion, 48: 11–26. Muller, A. C.; and Narayanan, S. 2009. Cognitivelyengineered multisensor image fusion for military applications. Information Fusion, 10: 137–149. Perez, E.; Strub, F.; De Vries, H.; Dumoulin, V.; and Courville, A. 2018. Film: Visual reasoning with a general conditioning layer. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, 3942–3950. Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In Proceedings of the International Conference on Machine Learning, 8748–8763. Ronneberger, O.; Fischer, P.; and Brox, T. 2015. U-net: Convolutional networks for biomedical image segmentation. In Proceedings of the International Conference on Medical Image Computing and Computer-Assisted Intervention, 234– 241. Singh, S.; Singh, H.; Bueno, G.; Deniz, O.; Singh, S.; Monga, H.; Hrisheekesha, P.; and Pedraza, A. 2023. A review of image fusion: Methods, applications and performance metrics. Digital Signal Processing, 137: 104020. Tang, L.; Wang, Y.; Gong, M.; Li, Z.; Deng, Y.; Yi, X.; Li, C.; Xu, H.; Zhang, H.; and Ma, J. 2025. VideoFusion: A spatio-temporal collaborative network for mutlimodal video fusion and restoration. arXiv preprint arXiv:2503.23359. Tang, L.; Xiang, X.; Zhang, H.; Gong, M.; and Ma, J. 2023. DIVFusion: Darkness-free infrared and visible image fusion. Information Fusion, 91: 477–493. Tang, L.; Yuan, J.; and Ma, J. 2022. Image fusion in the loop of high-level vision tasks: A semantic-aware real-time infrared and visible image fusion network. Information Fusion, 82: 28–42. Woo, S.; Park, J.; Lee, J.-Y.; and Kweon, I. S. 2018. Cbam: Convolutional block attention module. In Proceedings of the European Conference on Computer Vision, 3–19.

12473

<!-- Page 9 -->

Xie, E.; Wang, W.; Yu, Z.; Anandkumar, A.; Alvarez, J. M.; and Luo, P. 2021. SegFormer: Simple and efﬁcient design for semantic segmentation with transformers. Advances in Neural Information Processing Systems, 34: 12077–12090. Xu, H.; Ma, J.; Le, Z.; Jiang, J.; and Guo, X. 2020. Fusiondn: A uniﬁed densely connected network for image fusion. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, 12484–12491. Yadav, R.; Samir, A.; Rashed, H.; Yogamani, S.; and Dahyot, R. 2020. Cnn based color and thermal image fusion for object detection in automated driving. Irish Machine Vision and Image Processing, 2: 1–8. Yi, X.; Xu, H.; Zhang, H.; Tang, L.; and Ma, J. 2024. Text-if: Leveraging semantic text guidance for degradationaware and interactive image fusion. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 27026–27035. Zhang, H.; Tang, L.; Xiang, X.; Zuo, X.; and Ma, J. 2024a. Dispel darkness for better fusion: A controllable visual enhancer based on cross-modal conditional adversarial learning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 26487–26496. Zhang, H.; Zuo, X.; Jiang, J.; Guo, C.; and Ma, J. 2024b. MRFS: Mutually reinforcing image fusion and segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 26974–26983. Zhang, X.; and Demiris, Y. 2023. Visible and infrared image fusion using deep learning. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45: 10535–10554. Zhang, X.; Wang, X.; Yan, C.; and Sun, Q. 2024c. EVfusion: A novel infrared and low-light color visible image fusion network integrating unsupervised visible image enhancement. IEEE Sensors Journal, 24: 4920–4934. Zhao, Z.; Bai, H.; Zhang, J.; Zhang, Y.; Xu, S.; Lin, Z.; Timofte, R.; and Van Gool, L. 2023a. Cddfuse: Correlation-driven dual-branch feature decomposition for multi-modality image fusion. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 5906–5916. Zhao, Z.; Bai, H.; Zhu, Y.; Zhang, J.; Xu, S.; Zhang, Y.; Zhang, K.; Meng, D.; Timofte, R.; and Van Gool, L. 2023b. DDFM: Denoising diffusion model for multi-modality image fusion. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 8082–8093. Zheng, N.; Zhou, M.; Huang, J.; Hou, J.; Li, H.; Xu, Y.; and Zhao, F. 2024a. Probing synergistic high-order interaction in infrared and visible image fusion. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 26384–26395. Zheng, N.; Zhou, M.; Huang, J.; and Zhao, F. 2024b. Frequency integration and spatial compensation network for infrared and visible image fusion. Information Fusion, 109: 102359. Zou, D.; and Yang, B. 2023. Infrared and low-light visible image fusion based on hybrid multiscale decomposition and adaptive light adjustment. Optics and Lasers in Engineering, 160: 107268.

12474
