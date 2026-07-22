---
title: "DuGI-MAE: Improving Infrared Mask Autoencoders via Dual-Domain Guidance"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39928
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39928/43889
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# DuGI-MAE: Improving Infrared Mask Autoencoders via Dual-Domain Guidance

<!-- Page 1 -->

DuGI-MAE: Improving Infrared Mask Autoencoders via Dual-Domain Guidance

Yinghui Xing1 Xiaoting Su1 Shizhou Zhang1* Donghao Chu1 Di Xu2

1School of Computer Science, Northwestern Polytechnical University, China 2 Huawei, China

## Abstract

Infrared imaging plays a critical role in low-light and adverse weather conditions. However, due to the distinct characteristics of infrared images, existing foundation models such as Masked Autoencoder (MAE) trained on visible data perform suboptimal in infrared image interpretation tasks. To bridge this gap, an infrared foundation model known as Inf- MAE (Liu et al. 2024a) was developed and pre-trained on large-scale infrared datasets. Despite its effectiveness, Inf- MAE still faces several limitations, including the omission of informative tokens, insufficient modeling of global associations, and neglect of non-uniform noise. In this paper, we propose a Dual-domain Guided Infrared foundation model based on MAE (DuGI-MAE). First, we design a deterministic masking strategy based on token entropy, preserving only high-entropy tokens for reconstruction to enhance informativeness. Next, we introduce a Dual-Domain Guidance (DDG) module, which simultaneously captures global token relationships and adaptively filters non-uniform background noise commonly present in infrared imagery. To facilitate large-scale pretraining, we construct Inf-590K, a comprehensive infrared image dataset encompassing diverse scenes, various target types, and multiple spatial resolutions. Pretrained on Inf-590K, DuGI-MAE demonstrates strong generalization capabilities across various downstream tasks, including infrared object detection, semantic segmentation, and small target detection. Experimental results validate the superiority of the proposed method over both supervised and selfsupervised comparison methods.

## Introduction

Infrared (IR) imaging has emerged as a critical sensing modality in various applications, including surveillance (Jia et al. 2021) and target detection (Xing et al. 2024). Compared to visible images, infrared images exhibit unique characteristics such as lower spatial detail, reduced texture information, and generally lower signal-to-noise ratios. Their content is primarily governed by thermal radiation, making them highly sensitive to temperature differences but also less informative in scenes with low thermal contrast, all of which pose significant challenges for accurate visual interpretation.

*Corresponding Author:szzhang@nwpu.edu.cn Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** (a) Representative infrared image from a typical scene. Left: The original infrared image, where strong background responses often suppress the actual targets; Middle: Entropy map of the image; Right: Image processed with Adaptive Frequency-Domain Modulation (AFDM). (b) Comparison between Information-aware masking (Liu et al. 2024a) and our Entropy-based masking.

As illustrated in Figure 1, infrared images lack texture, and the temperature difference between the background and the target can cause the target to be suppressed, as in Figure 1(a), or highlighted, as in Figure 1(b). Therefore, models trained on visible images cannot be directly transferable, emphasizing the necessity of designing infrared modality-specific learning frameworks. Recent advances in modality-specific methods for infrared imagery include YOLO-Infrared (Zhang et al. 2022d) and PFGF (Li et al. 2025) for object detection in natural scenes, TBC-Net (Zhao et al. 2019) for semantic segmentation, and IRSTD (Liu et al. 2024b) and SCAFNet (Zhang et al. 2024) for small target detection. These methods learn task-specific representations through supervised training on dedicated datasets. However, due to the inherent modality gap between visible and infrared imagery, transferring features from ImageNet often results in suboptimal performance.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27135

![Figure extracted from page 1](2026-AAAI-dugi-mae-improving-infrared-mask-autoencoders-via-dual-domain-guidance/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

Vision foundation models have demonstrated remarkable generalization capabilities across a wide range of tasks, largely attributed to self-supervised pre-training on largescale image datasets. Among them, the Masked Autoencoder (MAE) (He et al. 2022) adopts masked reconstruction as a pretext task to learn transferable representations by reconstructing the masked tokens. MAE has achieved remarkable results in various downstream vision tasks. However, its random masking strategy is ineffective in infrared modality, since infrared images inherently have low information density, randomly masking out the informative tokens leads difficulties in reconstruction. Recently, (Liu et al. 2024a) proposed InfMAE, an infrared foundation model that employs an information-aware masking strategy to evaluate the information richness of each region based on its gray value. Although this strategy considers the characteristics of infrared images, it has the following limitations: 1) Omission of informative tokens. InfMAE utilizes a sampling strategy, which samples tokens with a fixed interval, resulting in the possible omission of some informative tokens. 2) Insufficient modeling of global association. InfMAE lacks a global association mechanism; if the tokens used for reconstruction are spatially dispersed within the image, InfMAE is ineffective in reconstructing the masked tokens. 3) Neglect of non-uniform noise. Due to the factors such as variations in detector responsivity, thermal instability, and imperfections in the optical system (Fang et al. 2025), infrared images often suffer from non-uniform noise. Figure 1(a) illustrates a type of non-uniform noise, temperature drift noise, which tends to suppress target regions while amplifying background responses. In this case, the gray-value-based masking strategy fails to account for non-uniform noise, leading to background regions being mistakenly retained as informative tokens.

To address the aforementioned problems, we propose a Dual-domain Guided Infrared foundation model based on MAE, termed DuGI-MAE. Specifically, we first design a deterministic masking strategy that selectively retains the most informative tokens. This “non-sampling” masking fundamentally avoids the loss of critical information often caused by random or fixed-interval sampling. To enhance global association and simultaneously suppress nonuniform noise, we further introduce a Dual-Domain Guidance (DDG) module, which incorporates an adaptive frequency filter. The integration of frequency-domain features is motivated by prior studies (He et al. 2023; Shi et al. 2024), which demonstrate their effectiveness in capturing global spatial structures and attenuating non-uniform noise in infrared images. The DDG module serves as a bridge between the encoder and decoder, enhancing the learning of robust and noise-resistant infrared representations. To facilitate pre-training, we construct a large-scale infrared dataset, Inf-590K, comprising 590,700 infrared images collected from diverse platforms and viewpoints, encompassing a wide range of scenes, target types, and spatial scales. Leveraging this large-scale pre-training, DuGI-MAE substantially outperforms state-of-the-art methods across various downstream tasks.

The main contributions are summarized as follows:

• We propose a dual-domain guided foundation model, DuGI-MAE, which uses a deterministic entropy-based masking strategy to mitigate missing informative tokens. • We present the DDG module to guide masked token reconstruction, employing adaptive frequency filtering to reduce non-uniform noise in infrared images. • We construct a large-scale dataset, Inf-590K, specifically for self-supervised pretraining on infrared imagery. Pretraining on Inf-590K significantly improves the generalization ability of various self-supervised methods for infrared image interpretation tasks. • Experimental results on infrared object detection, semantic segmentation, and small target detection consistently show the superiority and generalizability of DuGI-MAE.

## Related Work

Vision Foundation Model. Vision foundation models, which learn general image representations through largescale self-supervised pre-training, have emerged as a dominant paradigm in computer vision. Most existing foundation models have primarily focused on visible images, with representative approaches including Masked Autoencoders (MAE) (He et al. 2022), Bidirectional Encoder Representation from Image Transformers (BEiT) (Bao et al. 2021), and Self-Distillation with No Labels (DINO) (Caron et al. 2021). These models are typically pre-trained on large-scale datasets such as ImageNet, leading to substantial performance gains in various downstream tasks. However, they are inherently designed under the assumption that images contain rich texture and color information. Such assumptions present fundamental limitations when applied to infrared imagery, which typically lacks detailed textures and chromatic information. Recently, (Liu et al. 2024a) proposed InfMAE for the infrared modality, which used an Information-Aware Masking strategy to retain the informative regions by measuring their gray values. They further designed a multi-scale encoder to enhance local feature learning, achieving significant progress in infrared modality related tasks. InfMAE is pre-trained on a dataset of 300K samples, and its performance cannot be further improved without introducing more diverse data. Additionally, challenges still persist in the masking strategy and encoding process.

Frequency Domain in Infrared Image Processing. As a fundamental technique in signal processing (Pitas 2000), frequency-domain analysis enables powerful modeling of the distinct thermal radiation properties inherent in infrared imagery (Wang, Lv, and Xu 2012; Yang et al. 2011). Recent advances in infrared image processing have increasingly leveraged frequency-domain information to enhance feature representation and discrimination. For example, (Duan et al. 2023) introduced Fourier transform layers into convolutional neural network (CNN) backbones, enabling the model to learn spectral features that better characterize infrared targets. Similarly, (Wei et al. 2024) proposed a dual-domain fusion framework that integrates spatial and frequency-domain features at multiple levels, effectively capturing both local thermal edges and global scene structures, and demonstrating superior performance in infrared semantic segmentation.

27136

<!-- Page 3 -->

**Figure 2.** Resolution distribution of the Inf-590K dataset. The horizontal and vertical axes represent image width and height, respectively, while the size of each bubble indicates the number of samples corresponding to that resolution.

In contrast to these approaches, our work emphasizes the frequency-domain in the self-supervised pretext task to learn generalizable feature representations.

Infrared Pre-training Dataset: Inf-590K

We construct a large-scale infrared pre-training dataset named Inf-590K, comprising 590,700 infrared images. The primary data sources include several publicly available infrared datasets (Jia et al. 2021; Sun, Cao, and Hu 2022; Zhang et al. 2022c; Hwang et al. 2013; Xu et al. 2020; Liu et al. 2020, 2024a) as well as self-collected real-world infrared images. The dataset covers a variety of acquisition platforms and viewpoints, including aerial surveillance perspectives captured by UAV platforms, monitoring views from ground-based fixed cameras, street-level perspectives acquired by vehicle-mounted sensors, and maritime monitoring views obtained from ship-borne sensors. The diverse acquisition conditions contribute to a variety of scenarios and perspectives, but may also lead to a certain degree of data redundancy. To eliminate the redundant samples, we randomly select an anchor image from each scene and compute the cosine similarity between the features of this anchor and those of candidate images. Samples with high similarity scores (i.e., above 0.85) are excluded, thereby retaining images that exhibit distinct scene layouts or target distributions. Additionally, for visible-infrared video pairs, misalignment between imaging sensors often results in black borders in the infrared frames. To address this issue, we identify border regions with zero pixel values and apply adaptive cropping to remove these invalid areas.

After preprocessing, the Inf-590K dataset includes 445 unique resolutions ranging from a minimum of 50×34 to a maximum of 6912×576, showcasing a wide range of spatial resolutions. Figure 2 presents the top 10 most common image resolutions. This distribution aligns with the typical resolution characteristics of infrared imaging systems used in practical applications. In terms of scene diversity, Inf-590K comprises terrestrial (e.g., urban areas, highways, rural terrain), maritime (e.g., coastlines, open sea), and aerial (e.g., clouds, aerial views of ground targets) scenes, encompassing a variety of weather conditions (clear, foggy, rainy) and temporal scenarios (day and night). The annotated targets span common infrared objects, including vehicles, pedestrians, buildings, ships, aircraft, and public infrastructure.

Proposed Method

Overview

The overall framework of proposed DuGI-MAE is shown in Figure 3. The pretext task for self-supervised learning (SSL) is the masked image modeling (MIM). Driven by our entropy-based masking strategy, the masked autoencoder (MAE) (He et al. 2022) reconstructs the masked tokens to capture inherent thermal radiation characteristics. Meanwhile, we propose a dual-domain guidance (DDG) module, where frequency features act as a condition to fuse spatial structural and thermal radiation information, thereby guiding the decoder to reconstruct masked tokens.

Entropy-Based Masking Module

To make masked image reconstruction a meaningful pretext task, previous studies have commonly applied aggressive masking by randomly masking a substantial portion of input image tokens (He et al. 2022; Wei et al. 2022). This strategy, however, leads to the difficulties in reconstructing foreground details (Hou et al. 2022) if the remaining visible tokens comprise more background information.

For the infrared modality, precise selection of masked positions is particularly important, as infrared images often exhibit sparse thermal radiation distributions. In this paper, we employ Shannon Entropy as a quantitative metric to assess the information content of each token. Tokens with higher entropy values are prioritized for retention, while a higher proportion of masking is applied to other regions. This strategy encourages the model concentrate on discriminative features specific to the infrared modality. As shown in Figure 1(b), the retained tokens consistently preserve informative content, including target regions and the boundaries between targets and the background.

Given an infrared image X, we first use a convolutional layer Φ(·) to generate feature map M = Φ(X), which is further partitioned and flattened into N tokens {m1, m2, · · ·, mN}. We then calculate the entropy value of these tokens using the following formula:

EN(mi) = −

J X j=1

P(hj) · log2 (P(hj)), (1)

where hj denotes the j-th intensity value within mi, J is the total number of possible intensity levels, and P(hj) represents the probability of hj occurring in mi.

Let λ be the mask ratio, we sort the tokens according to their entropy values in an ascending order, and retain the last (1 −λ) tokens with the highest entropy values, which we think represent the most informative regions in the infrared image, typically containing important thermal targets. The remaining tokens with lower entropy are masked, as these

27137

![Figure extracted from page 3](2026-AAAI-dugi-mae-improving-infrared-mask-autoencoders-via-dual-domain-guidance/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

**Figure 3.** Overall architecture of DuGI-MAE. It consists of the (a) Entropy-Based Masking Module, the (b) Encoder, the (c) Dual-Domain Guidance (DDG) module, and the (d) Decoder.

regions often indicate uniform backgrounds. This process is formulated as:

Ikeep = {Isort[i] | i ∈[⌊λ · N⌋, N −1]},

Mask[i] =

1, if i ∈Ikeep, 0, otherwise,

(2)

where i is the token index, and Isort denotes the sorted index sequence. Ikeep represent the tokens to be kept. ⌊·⌋is the floor function. In our method, we set λ = 0.75.

Dual-Domain Guidance Due to the low information density of infrared modality, the preserved tokens used for reconstruction may be dispersed in the image. In this case, the global association is very important. Furthermore, infrared images typically exhibit non-uniform noises, which disrupt the discrimination between targets and background. Since the frequency domain is capable of modeling global information present in the spatial domain. Additionally, high-pass filtering in the frequency domain can help alleviate non-uniform noise, we incorporate frequency transform into our model. Specifically, we propose a Dual-Domain Guidance (DDG) module that leverages both spatial and frequency domain features to enhance performance. As illustrated in Figure 3(c), frequency features are extracted from infrared images using Adaptive Frequency-Domain Modulation (AFDM). These features are then projected through a patch embedding to serve as key-value pairs for subsequent Transformer block.

**Figure 4.** Adaptive Frequency-Domain Modulation (AFDM). The input images are first transformed into the frequency domain via the Fast Fourier Transform (FFT). A learnable radial filter is then applied to suppress non-uniform background noise(usually low-frequency components) while preserving discriminative features. Finally, the processed features are transformed back to the spatial domain using the Inverse FFT (IFFT).

In parallel, spatial features from the encoder are formulated as query-key-value triplets. The frequency-enhanced features subsequently guide the spatial features, enabling them to more effectively attend to target regions.

Adaptive Frequency-Domain Modulation. Although the non-uniform noise, especially the temperature drift noise can be alleviated by the high-pass filtering, we argue that directly filtering the low-frequency component leads to the loss of image contents. Therefore, we propose an adaptive

27138

![Figure extracted from page 4](2026-AAAI-dugi-mae-improving-infrared-mask-autoencoders-via-dual-domain-guidance/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-dugi-mae-improving-infrared-mask-autoencoders-via-dual-domain-guidance/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

frequency-domain modulation (AFDM), shown in Figure 4. Firstly, the Fast Fourier Transform (FFT) converts the input image X to the frequency domain, obtaining F(X), where F(·) denotes the FFT. In the frequency spectrum, the central region corresponds to low-frequency components. We design a parameterized radial function H(u, v) for filtering the frequency spectrum centered at the spectral center, dynamically adjusting central (low-frequency) suppression intensity via learnable parameters while preserving information in the peripheral (mid-to-high frequency) regions:

H(u, v) = α · exp

−β ·

D(u, v)

r

2!

,

S = F(X) ⊙H,

(3)

where S is the modulated frequency spectrum, and “⊙” denotes the element-wise multiplication. r, α ∈[0, 1), and β > 0 are learnable parameters, where r is the radius, and α and β control the attenuation degree and rate, respectively. D(u, v) is the Euclidean distance from the coordinate (u, v) to the center of the frequency spectrum. By adjusting the suppression parameters α and β, the model can dynamically control the attenuation of low-frequency signals. This frequency modulation selectively attenuates the spectral center to reduce non-uniform noise while preserving high-frequency thermal radiation signals, enhancing the feature discriminability. The modulated frequency spectrum S is then transformed back to the spatial domain via Inverse FFT (IFFT), yielding the frequency-enhanced feature map Ffreq after the patch embedding and downsampling.

Frequency-Guided Attention Injection. We use the frequency-enhanced feature map Ffreq to act as the guidance for the features in spatial domain. Specifically, in the first Transformer block, Ffreq is firstly encoded into Key (Kfreq) and Value (Vfreq) pairs, and they are then integrated with the spatial Key (Kspatial) and Value (Vspatial) pairs:

Attention(F1, Ffreq) = σ(

Qspatial

KT spatial + KT freq

√dk

) · (Vspatial + Vfreq),

(5) where F1 represents the output of Stage 1 in the encoder. σ(·) is the softmax function, Qspatial is the query of spatial features, and √dk is the scaling factor. In the subsequent Transformer block, spatial features are added to the output of the previous block to form the Key and Value representations, while the spatial features themselves continue to serve as the Query. The frequency-guided attention injection steers attention weights toward high-response target regions to enhance critical structures.

DuGI-MAE for Downstream Tasks The pre-trained encoder of DuGI-MAE can be adapted to downstream tasks, including infrared object detection, semantic segmentation, and small target detection. To enable multi-scale feature aggregation, we extract intermediate features from the encoder, denoted as F1, F2, and F3, which

## Method

Backbone Model mAP AP50

DETR ResNet101 – 41.5 72.7 DINO Swin-L – 44.6 74.8 YOLOv8 CSPDarkNet – 53.7 80.3

From scratch VIT-B Cascade R-CNN 51.2 80.1 MAE ViT-B Cascade R-CNN 51.9 82.0 MCMAE ViT-B Cascade R-CNN 55.1 85.4 InfMAE ViT-B Cascade R-CNN 56.5 86.3 DuGI-MAE(Ours) ViT-B Cascade R-CNN 57.3 86.9

From scratch VIT-B Mask R-CNN 49.6 80.3 MAE ViT-B Mask R-CNN 52.2 83.8 MCMAE ViT-B Mask R-CNN 56.8 87.2 InfMAE ViT-B Mask R-CNN 57.1 87.9 DuGI-MAE(Ours) ViT-B Mask R-CNN 59.1 89.7

**Table 1.** Performance comparisons of different object detection methods on the M3FD-inf dataset.

## Method

Backbone Model mIoU mAcc

DeeplabV3+ Resnet50 – 65.2 73.8 UperNet Resnet50 – 65.6 74.7 DNLNet Resnet101 – 67.0 75.7 DDRNet – – 67.3 73.3

From scratch ViT-B FCN 57.0 63.6 MAE ViT-B FCN 63.4 70.8 MCMAE ViT-B FCN 70.8 79.2 InfMAE ViT-B FCN 72.6 80.5 DuGI-MAE(Ours) ViT-B FCN 73.1 80.8

From scratch ViT-B UperNet 61.5 61.3 MAE ViT-B UperNet 71.3 78.0 MCMAE ViT-B UperNet 73.2 81.1 InfMAE ViT-B UperNet 74.5 82.9 DuGI-MAE(Ours) ViT-B UperNet 75.0 83.6

**Table 2.** Performance comparisons of different semantic segmentation methods on MSRS dataset.

are the outputs of Stage 1, Stage 2, and Stage 3, respectively. These features progressively encode spatial and semantic information at different levels. We additionally apply a downsampling operation to F3 ∈RH/16×W/16×C, producing F4 ∈RH/32×W/32×C. Finally, the multi-scale features F1, F2, F3, and F4 are fed into the downstream tasks for detection and segmentation.

## Experiment

In this section, we outline the pre-training setup on Inf-590K dataset and proceed to evaluate our model’s generalization performance through three downstream tasks. Finally, we present comprehensive ablation studies. Our code is available at https://github.com/Xtingsu/DuGI-MAE.

Pre-training Setup

The DuGI-MAE framework is implemented using PyTorch 1.8.0 and trained on four NVIDIA GeForce RTX 4090 GPUs. In line with the settings commonly adopted in MAE-

27139

<!-- Page 6 -->

## Method

Backbone Model mIoU Pd

MPCM – – 7.3 60.3 IPI – – 28.0 81.3 RIPT – – 14.1 77.5 ACMNet – – 60.3 90.3 DNANet – – 65.7 89.2 UIUNet – – 65.6 91.3 SCAFNet – – 66.3 91.1

MAE ViT-B IRSTD 57.5 88.2 MCMAE ViT-B IRSTD 64.3 77.9 InfMAE ViT-B IRSTD 66.5 96.9 DuGI-MAE(Ours) ViT-B IRSTD 67.1 95.9

**Table 3.** Performance comparisons of different infrared small target detection methods on the IRSTD-1k dataset.

series self-supervised learning frameworks (He et al. 2022; Gao et al. 2022), we utilize mean squared error loss during pre-training and employ a mask ratio of 75%. The encoder is structured into three hierarchical stages comprising 2, 2, and 11 Transformer layers, respectively, to effectively capture multi-scale thermal features. Pre-training is conducted over 400 epochs using a cosine learning rate schedule, with the initial 40 epochs allocated for warm-up to enhance training stability. The model is optimized with the AdamW optimizer, utilizing a base learning rate of 1.5 × 10−4, a weight decay of 0.05, and a batch size of 96. To improve the generalization across diverse infrared scene variations, random cropping is employed as the primary data augmentation strategy.

Infrared Object Detection Experimental Settings. We validate the effectiveness of proposed method on infrared object detection using the M3FD-inf dataset (Liu et al. 2022). The M3FD dataset is a multimodal object detection benchmark comprising 4,200 paired infrared and visible images, covering six object categories: person, car, bus, motor, truck, and lamp. In our experiments, only the infrared image subset, referred to as M3FDinf, is employed for performance evaluation. We adopt Mask R-CNN (He et al. 2017) and Cascade R-CNN (Cai and Vasconcelos 2018) as detection heads, with the pre-trained DuGI-MAE model serving as the backbone. The entire network is fine-tuned for 260k iterations using a base learning rate of 1 × 10−6 and a weight decay of 0.1.

## Results

and Analyses. To comprehensively evaluate the effectiveness of the proposed method, we compare it with both fully supervised approaches-DETR (Carion et al. 2020), DINO (Zhang et al. 2022a), YOLOv8) and selfsupervised methods, including MAE (He et al. 2022), MC- MAE (Gao et al. 2022), and InfMAE (Liu et al. 2024a). Except for the model trained from scratch, all methods are pretrained on the proposed Inf-590K dataset. As shown in Table 1, our method achieves an mAP of 59.1 and an AP50 of 89.7 when using Mask R-CNN as the detection head, surpassing InfMAE (57.1/87.9) by 2.0 and 1.8 points, respectively. Moreover, it consistently outperforms all other baselines, demonstrating the superiority of the DuGI-MAE framework on the infrared object detection task.

Infrared Semantic Segmentation Experimental Settings. Experiments on infrared semantic segmentation are conducted using the MSRS dataset (Tang et al. 2022), which comprises 1,444 pairs of co-registered infrared and visible images. The training set contains 1,083 image pairs, while the test set consists of 361 pairs. In our experiments, only the infrared images are utilized for performance evaluation. We adopt FCN (Long, Shelhamer, and Darrell 2015) and UperNet (Xiao et al. 2018) as segmentation heads, and integrate them with the pre-trained DuGI- MAE encoder. The entire model is then fine-tuned in a supervised manner to adapt to the semantic segmentation task.

## Results

and Analyses. The comparison methods including typical semantic segmentation models such as DeepLabV3+ (Chen et al. 2018), UperNet (Xiao et al. 2018), DNLNet (Ni et al. 2022), DDRNet (Zhang et al. 2021), as well as self-supervised learning (SSL)-based methods including MAE (He et al. 2022), MCMAE (Gao et al. 2022), and InfMAE (Liu et al. 2024a). The backbones of the SSL-based methods are all pre-trained on the Inf-590K dataset. Overall, SSL-based methods consistently outperform conventional semantic segmentation models on the infrared modality. As presented in Table 2, integrating the encoders of infrared foundation models, such as InfMAE and DuGI-MAE, with segmentation heads like FCN or Uper- Net leads to substantial improvements in segmentation performance. These results highlight the effectiveness of selfsupervised representations learned from large-scale infrared data. Among all compared methods, DuGI-MAE achieves the highest overall performance, proving its effectiveness and superiority in infrared semantic segmentation.

Infrared Small Target Detection Experimental Settings. Infrared small target detection presents unique challenges due to the inherently limited features of the targets, thereby placing higher demands on the model’s ability to learn discriminative representations. To evaluate the performance in this context, we conduct experiments on the IRSTD-1K dataset (Zhang et al. 2022b), which comprises 1,000 infrared images with pixel-level annotations. Specifically, we replace the original encoder of IRSTD (Liu et al. 2023) with the DuGI-MAE encoder to assess its effectiveness in capturing and representing small target features in infrared imagery.

## Results

and Analyses. We conduct a comprehensive comparison of the proposed method with traditional handcrafted approaches (MPCM (Wei, You, and Li 2016), IPI (Gao et al. 2013), RIPT (Dai and Wu 2017)), fully supervised methods (ACMNet (Qu et al. 2021), DNANet (Li et al. 2022), UIUNet (Wu, Hong, and Chanussot 2022), SCAFNet (Zhang et al. 2024)), and self-supervised learning (SSL)-based methods (MAE (He et al. 2022), MC- MAE (Gao et al. 2022), InfMAE (Liu et al. 2024a)) on the IRSTD-1K dataset. For a fair comparison, all SSL-based models adopt the ViT-B backbone pre-trained on Inf-590K and are integrated into IRSTD (Liu et al. 2023). As demonstrated in Table 3, the proposed DuGI-MAE achieves the

27140

<!-- Page 7 -->

## Method

Pre-training Data mAP AP50

MAE Inf30 51.2 82.9 Inf-590K 52.2 83.8

MCMAE Inf30 56.2 87.0 Inf-590K 56.8 87.2

InfMAE Inf30 56.5 88.2 Inf-590K 57.1 87.9

DuGI-MAE(Ours) Inf30 57.4 88.6 Inf-590K 59.1 89.7

**Table 4.** Comparison of self-supervised methods using different pre-training datasets on infrared object detection tasks under the M3FD-inf dataset (ViT-B backbone & Mask R- CNN detection head).

Masking Strategy mAP AP50 Random mask (He et al. 2022) 57.2 88.1 Gray-values mask (Liu et al. 2024a) 58.4 88.9 Ours 59.1 89.7

**Table 5.** Ablation study on masking strategies for DuGI- MAE (ViT-B backbone & Mask R-CNN detection head).

superior performance with an mIoU of 67.1, outperforming MCMAE and InfMAE by 2.8 and 0.6, respectively. This performance gain can be attributed to the dual-domain mechanism designed for infrared small targets, which effectively enhances the discriminability of target representations by deeply correlating spatial local features with frequencydomain global characteristics.

Ablation Study Comparisons on Pre-trained Models. To quantify the impact of pre-training dataset scales, we pre-train MAE, MC- MAE, InfMAE and the proposed method on infrared dataset of varying sizes, including Inf30 (Liu et al. 2024a) and the larger Inf-590K. The experimental results on the M3FD-inf dataset are presented in Table 4. It can be observed that all self-supervised methods consistently achieve higher mAP when pre-trained on the larger Inf-590K dataset, underscoring the critical role of large-scale infrared pre-training in improving downstream detection performance.

Masking Methods. We compare three different masking strategies in Table 5: 1) Random Masking (He et al. 2022), 2) Information-aware Masking (Liu et al. 2024a), and 3) Entropy-based Masking (ours). The information-aware masking ranks tokens by grayscale intensity and retains 25% tokens using a fixed sampling stride of 4. In contrast, our entropy-based masking selects tokens based on local entropy values, deterministically preserving the top 25% most informative tokens. As shown in Table 5, the entropy-based masking consistently outperforms alternative methods. We attribute the inferior performance of random masking to its indiscriminate nature, which disrupts the spatial continuity of high-entropy regions, often critical in infrared imagery,

## Method

Backbone Model mAP AP50

MAE ViT-B Mask R-CNN 52.2 83.8 MAE+DDG ViT-B Mask R-CNN 53.1 84.9

MCMAE ViT-B Mask R-CNN 56.8 87.2 MCMAE+DDG ViT-B Mask R-CNN 57.2 88.1

InfMAE ViT-B Mask R-CNN 57.1 87.9 InfMAE+DDG ViT-B Mask R-CNN 57.6 88.4

**Table 6.** Performance improvement of DDG Module on different self-supervised pre-training models.

resulting in fragmented feature representations. While the information-aware strategy introduces content sensitivity, its fixed sampling pattern may overlook salient high-entropy regions, resulting in incomplete semantic preservation. In contrast, our entropy-based approach explicitly focuses on preserving the most informative regions, thereby facilitating more effective reconstruction and feature learning.

DDG Module. The proposed DDG module is compatible with various pre-trained models that follow the typical encoder-decoder architecture. To evaluate its generalizability and effectiveness, we conduct ablation studies by integrating the DDG module as a feature bridging component between the encoder and decoder in several representative self-supervised frameworks, including MAE (He et al. 2022), MCMAE (Gao et al. 2022), and InfMAE (Liu et al. 2024a). As shown in Table 6, incorporating the DDG module consistently improves both the mAP and AP50 metrics across all baseline models. These results validate the effectiveness of the DDG module in enhancing feature representations and improving downstream task performance.

## Conclusion

In this paper, we propose DuGI-MAE, a self-supervised pretraining framework tailored for the infrared modality, which is inherently characterized by low information density. To enable effective representation learning, we first construct Inf-590K, a large-scale infrared dataset comprising 590,700 images. To mitigate the risk of masking informative tokens during pre-training, we propose an entropy-based masking strategy that selectively retains tokens with high information content. Furthermore, to address the reconstruction bottleneck caused by aggressive masking, we design a Dual- Domain Guidance (DDG) module that incorporates both spatial- and frequency-domain cues. This design enhances the model’s ability to capture fine-grained local details and global structural patterns simultaneously. Extensive experiments across multiple downstream tasks, including object detection, semantic segmentation, and small target detection, demonstrate that DuGI-MAE consistently outperforms state-of-the-art methods. In addition, the DDG module an be seamlessly integrated into existing encoder-decoder pretraining frameworks, further improving their performance on infrared data. In future work, we will incorporate more physical priors into the pre-training process to advance the development of infrared foundation models.

27141

<!-- Page 8 -->

## Acknowledgements

This work was supported in part by the National Natural Science Foundation of China (NSFC) under Grant 62476223, 62576282; in part by the National Key Research and Development Program of China under Grant 2024YFF1306501; in part by Innovation Capability Support Program of Shaanxi (Program No. 2024ZC-KJXX-043); in part by the Natural Science Basic Research Program of Shaanxi Province (2024JC-DXWT-07).

## References

Bao, H.; Dong, L.; Piao, S.; and Wei, F. 2021. Beit: Bert pre-training of image transformers. arXiv preprint arXiv:2106.08254. Cai, Z.; and Vasconcelos, N. 2018. Cascade r-cnn: Delving into high quality object detection. In Proceedings of the IEEE conference on computer vision and pattern recognition, 6154–6162. Carion, N.; Massa, F.; Synnaeve, G.; Usunier, N.; Kirillov, A.; and Zagoruyko, S. 2020. End-to-end object detection with transformers. In European conference on computer vision, 213–229. Springer. Caron, M.; Touvron, H.; Misra, I.; J´egou, H.; Mairal, J.; Bojanowski, P.; and Joulin, A. 2021. Emerging properties in self-supervised vision transformers. In Proceedings of the IEEE/CVF international conference on computer vision, 9650–9660. Chen, L.-C.; Zhu, Y.; Papandreou, G.; Schroff, F.; and Adam, H. 2018. Encoder-decoder with atrous separable convolution for semantic image segmentation. In Proceedings of the European conference on computer vision (ECCV), 801–818. Dai, Y.; and Wu, Y. 2017. Reweighted infrared patch-tensor model with both nonlocal and local priors for single-frame small target detection. IEEE journal of selected topics in applied earth observations and remote sensing, 10(8): 3752– 3767. Duan, C.; Hu, B.; Liu, W.; Ma, T.; Ma, Q.; and Wang, H. 2023. Infrared Small Target Detection Method Based on Frequency Domain Clutter Suppression and Spatial Feature Extraction. IEEE Access, 11: 85549–85560. Fang, H.; Wang, X.; Li, Z.; Wang, L.; Li, Q.; Chang, Y.; and Yan, L. 2025. Detection-Friendly Nonuniformity Correction: A Union Framework for Infrared UAV Target Detection. In Proceedings of the Computer Vision and Pattern Recognition Conference, 11898–11907. Gao, C.; Meng, D.; Yang, Y.; Wang, Y.; Zhou, X.; and Hauptmann, A. G. 2013. Infrared patch-image model for small target detection in a single image. IEEE transactions on image processing, 22(12): 4996–5009. Gao, P.; Ma, T.; Li, H.; Lin, Z.; Dai, J.; and Qiao, Y. 2022. Convmae: Masked convolution meets masked autoencoders. arXiv preprint arXiv:2205.03892. He, K.; Chen, X.; Xie, S.; Li, Y.; Doll´ar, P.; and Girshick, R. 2022. Masked autoencoders are scalable vision learners. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 16000–16009.

He, K.; Gkioxari, G.; Doll´ar, P.; and Girshick, R. 2017. Mask r-cnn. In Proceedings of the IEEE international conference on computer vision, 2961–2969. He, Y.; Zhang, C.; Zhang, B.; and Chen, Z. 2023. FSPnP: Plug-and-play frequency–spatial-domain hybrid denoiser for thermal infrared image. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–16. Hou, Z.; Sun, F.; Chen, Y.-K.; Xie, Y.; and Kung, S.-Y. 2022. Milan: Masked image pretraining on language assisted representation. arXiv preprint arXiv:2208.06049. Hwang, S.; Park, J.; Kim, N.; Choi, Y.; and Kweon, I. S. 2013. Multispectral pedestrian detection: Benchmark dataset and baseline. IEEE. Jia, X.; Zhu, C.; Li, M.; Tang, W.; and Zhou, W. 2021. LLVIP: A visible-infrared paired dataset for low-light vision. In Proceedings of the IEEE/CVF international conference on computer vision, 3496–3504. Li, B.; Xiao, C.; Wang, L.; Wang, Y.; Lin, Z.; Li, M.; An, W.; and Guo, Y. 2022. Dense nested attention network for infrared small target detection. IEEE Transactions on Image Processing, 32: 1745–1758. Li, T.; Ye, M.; Wu, T.; Li, N.; Li, S.; Tang, S.; and Ji, L. 2025. Pseudo Visible Feature Fine-Grained Fusion for Thermal Object Detection. In Proceedings of the Computer Vision and Pattern Recognition Conference, 6710–6719. Liu, F.; Gao, C.; Chen, F.; Meng, D.; Zuo, W.; and Gao, X. 2023. Infrared small and dim target detection with transformer under complex backgrounds. IEEE Transactions on Image Processing, 32: 5921–5932. Liu, F.; Gao, C.; Zhang, Y.; Guo, J.; Wang, J.; and Meng, D. 2024a. InfMAE: A foundation model in the infrared modality. In European Conference on Computer Vision, 420–437. Springer. Liu, J.; Fan, X.; Huang, Z.; Wu, G.; Liu, R.; Zhong, W.; and Luo, Z. 2022. Target-aware dual adversarial learning and a multi-scenario multi-modality benchmark to fuse infrared and visible for object detection. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 5802–5811. Liu, Q.; Li, X.; He, Z.; Li, C.; Li, J.; Zhou, Z.; Yuan, D.; Li, J.; Yang, K.; Fan, N.; et al. 2020. LSOTB-TIR: A large-scale high-diversity thermal infrared object tracking benchmark. In Proceedings of the 28th ACM international conference on multimedia, 3847–3856. Liu, Q.; Liu, R.; Zheng, B.; Wang, H.; and Fu, Y. 2024b. Infrared small target detection with scale and location sensitivity. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 17490–17499. Long, J.; Shelhamer, E.; and Darrell, T. 2015. Fully convolutional networks for semantic segmentation. In Proceedings of the IEEE conference on computer vision and pattern recognition, 3431–3440. Ni, J.; Wu, J.; Elazab, A.; Tong, J.; and Chen, Z. 2022. DNL- Net: deformed non-local neural network for blood vessel segmentation. BMC Medical Imaging, 22(1): 109.

27142

<!-- Page 9 -->

Pitas, I. 2000. Digital image processing algorithms and applications. John Wiley & Sons. Qu, S.; Chen, G.; Li, Z.; Zhang, L.; Lu, F.; and Knoll, A. 2021. Acm-net: Action context modeling network for weakly-supervised temporal action localization. arXiv preprint arXiv:2104.02967. Shi, Y.; Deng, X.; Wang, L.; Zhang, Y.; and Huang, Z. 2024. Semi-supervised learning for infrared thermal radiation correction in the real world. IEEE Transactions on Geoscience and Remote Sensing. Sun, Y.; Cao, B.; and Hu, Z. Q. 2022. Drone-Based RGB- Infrared Cross-Modality Vehicle Detection Via Uncertainty- Aware Learning. IEEE Transactions on Circuits and Systems for Video Technology, 32(10): 6700–6713. Tang, L.; Yuan, J.; Zhang, H.; Jiang, X.; and Ma, J. 2022. PIAFusion: A progressive infrared and visible image fusion network based on illumination aware. Information Fusion. Wang, X.; Lv, G.; and Xu, L. 2012. Infrared dim target detection based on visual attention. Infrared Physics & Technology, 55(6): 513–521. Wei, C.; Fan, H.; Xie, S.; Wu, C.-Y.; Yuille, A.; and Feichtenhofer, C. 2022. Masked feature prediction for self-supervised visual pre-training. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 14668–14678. Wei, G.; Xu, J.; Yan, W.; Chong, Q.; Xing, H.; and Ni, M. 2024. Dual-Domain Fusion Network Based on Wavelet Frequency Decomposition and Fuzzy Spatial Constraint for Remote Sensing Image Segmentation. Remote Sensing, 16(19). Wei, Y.; You, X.; and Li, H. 2016. Multiscale patch-based contrast measure for small infrared target detection. Pattern recognition, 58: 216–226. Wu, X.; Hong, D.; and Chanussot, J. 2022. UIU-Net: U-Net in U-Net for infrared small object detection. IEEE Transactions on Image Processing, 32: 364–376. Xiao, T.; Liu, Y.; Zhou, B.; Jiang, Y.; and Sun, J. 2018. Unified perceptual parsing for scene understanding. In Proceedings of the European conference on computer vision (ECCV), 418–434. Xing, Y.; Yang, S.; Wang, S.; Zhang, S.; Liang, G.; Zhang, X.; and Zhang, Y. 2024. MS-DETR: Multispectral pedestrian detection transformer with loosely coupled fusion and modality-balanced optimization. IEEE Transactions on Intelligent Transportation Systems. Xu, H.; Ma, J.; Le, Z.; Jiang, J.; and Guo, X. 2020. FusionDN: A Unified Densely Connected Network for Image Fusion. In AAAI, 12484–12491. Yang, H. X.; Wang, X. S.; Xie, P. H.; Leng, A. L.; and Peng, Y. 2011. Infrared Image Denoising Based on Improved Threshold and Inter-scale Correlations of Wavelet Transform. Acta Automatica Sinica. Zhang, H.; Li, F.; Liu, S.; Zhang, L.; Su, H.; Zhu, J.; Ni, L. M.; and Shum, H.-Y. 2022a. Dino: Detr with improved denoising anchor boxes for end-to-end object detection. arXiv preprint arXiv:2203.03605.

Zhang, M.; Zhang, R.; Yang, Y.; Bai, H.; Zhang, J.; and Guo, J. 2022b. ISNet: Shape matters for infrared small target detection. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 877–886. Zhang, P.; Zhao, J.; Wang, D.; Lu, H.; and Ruan, X. 2022c. Visible-Thermal UAV Tracking: A Large-Scale Benchmark and New Baseline. Zhang, S.; Wang, Z.; Xing, Y.; Lin, L.; Su, X.; and Zhang, Y. 2024. SCAFNet: Semantic-Guided Cascade Adaptive Fusion Network for Infrared Small Targets Detection. IEEE Transactions on Geoscience and Remote Sensing. Zhang, Y.; Shen, K. J.; He, Z. F.; and Pan, Z. S. 2022d. Yoloinfrared: Enhancing Yolox for infrared scene. In Journal of Physics: Conference Series, volume 2405, 012015. IOP Publishing. Zhang, Z.; Chen, G.; Wang, X.; and Shu, M. 2021. DDR- Net: Fast point cloud registration network for large-scale scenes. ISPRS Journal of Photogrammetry and Remote Sensing, 175: 184–198. Zhao, M.; Cheng, L.; Yang, X.; Feng, P.; Liu, L.; and Wu, N. 2019. TBC-Net: A real-time detector for infrared small target detection using semantic constraint. arXiv preprint arXiv:2001.05852.

27143
