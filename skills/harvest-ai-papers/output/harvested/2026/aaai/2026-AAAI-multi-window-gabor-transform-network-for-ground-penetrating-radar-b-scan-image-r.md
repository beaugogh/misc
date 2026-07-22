---
title: "Multi-Window Gabor Transform Network for Ground Penetrating Radar B-Scan Image Reconstruction"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37947
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37947/41909
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Multi-Window Gabor Transform Network for Ground Penetrating Radar B-Scan Image Reconstruction

<!-- Page 1 -->

Multi-Window Gabor Transform Network for Ground Penetrating Radar B-Scan

Image Reconstruction

Huabin Wang1, Yu Yang1, Xinran Zhong2, Zilong Ling1

1Anhui Provincial International Joint Research Center for Advanced Technology in Medical Imaging, School of Computer Science and Technology, Anhui University

2Anhui Guimu Robot Co., Ltd. wanghuabin@ahu.edu.cn, e24301223@stu.ahu.edu.cn, zhongxinran@gm-robot.com, e23301245@stu.ahu.edu.com

## Abstract

Transmitting and receiving electromagnetic wave signals reflected back to the ground can detect the structure of subsurface defects. However, the imaging process of groundpenetrating radar (GPR) is highly susceptible to interference from complex underground environments, leading to nonlinear attenuation and noise. This makes it challenging to directly locate and identify defect types from raw reflected radar waveform images. Currently, mainstream methods of manual radar signal gain and filtering heavily rely on expert experience, while common end-to-end generative models are typically designed for optical images. This paper proposes a defect-guided Multi-window Gabor Transform Network (MGT-Net) for GPR B-Scan image reconstruction which achieves automatic gain and defect enhancement of raw GPR signals. Firstly, a Multi-window Gabor Transform Module (MGTM) is designed to effectively represent and extract spatial-frequency features of defects at different locations and of various types. Secondly, a defect guidance network (DG-Net) is constructed to accurately direct the reconstruction of defect areas and enhance the saliency and discriminability of defect features. Additionally, we construct a large-scale GPR B-Scan image dataset (GRD) containing 41,613 images across 7 defect categories. Experimental results show the superior performance of MGT-Net, achieving state-of-the-art (SOTA) SSIM of 81.72% ± 3.5% and PSNR of 30.50 ± 0.442.

Code — https://github.com/YYAHU/MGT-Net Datasets — https://github.com/AHU-MedImagingIJR/GM-GRD

## Introduction

Ground-Penetrating Radar (GPR) has been widely adopted in domains requiring non-destructive structural detection, such as road subgrade inspection, underground pipeline detection, and bridge-tunnel assessment (Jiao et al. 2020; Noshahri, van der Meijde, and olde Scholtenhuis 2022; Luo et al. 2023). The GPR utilizes the different propagation characteristics of electromagnetic waves through varying medias, enabling the receiver to identify subsurface structures and objects based on the reflected signals (Jol 2008). However, when propagating through heterogeneous underground

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

medias, the velocity and energy of electromagnetic wave undergo nonlinear attenuation. Moreover, ground clutter and complex subsurface structures further obscure the authentic signals of subsurface targets. Consequently, gaining severely attenuated target signals, reducing complex and variable noise interference, and achieving the GPR image reconstruction remain critical challenges in the field of GPR technology applications.

The main goal of GPR image reconstruction is gain and filtering, which can improve the saliency and discrimination of defects in the raw radar waveform images. Traditional methods mainly include Dewow (Gerlitz et al. 1993; Battista, Addison, and Knapp 2009), Filtering (Baili et al. 2009; Xiao and Liu 2017), Gain (Allred et al. 2005; Bianchini Ciampoli et al. 2019), and Migration (Song et al. 2006; Yamaguchi, Mizutani, and Nagayama 2020) techniques. However, these methods typically necessitate manual parameter tuning by operators based on experience, leading to the processing outcomes susceptible to subjective influences.

Deep learning methods based on spatial convolutional neural networks, such as image enhancement (Dudhane et al. 2023; Li et al. 2025), image restoration (Gou et al. 2020; Cui, Ren, and Knoll 2024), and image-to-image translation (Isola et al. 2017; Li et al. 2023) can autonomously learn complex noise patterns and meaningful signal features from large-scale datasets without expert experience. However, these methods are primarily developed for optical images. Different from optical images, GPR images exhibit indistinct spatial features and sparse data distributions. Directly applying these methods to GPR image reconstruction often generate visually plausible outputs without meaningful physical interpretation.

Frequency-domain convolutional neural networks (FDC- NNs) (Zhang et al. 2022; Cai et al. 2021) transform data to the frequency domain and perform operations such as filtering. These approach are well-suited for processing GPR signals with typical frequency-domain characteristics. However, the defects in GPR signals present the following characteristics: (1) The defect areas are generally small, requiring precise localization of their spatial position. (2) While different types of defect show significant differences in optical images, their discrepancies are subtle in GPR signals and reflected in slight waveform variation. (3) A single GPR im-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

<!-- Page 2 -->

age may simultaneously contain multiple different types of defects. Therefore, existing frequency-domain-based CNNs struggle to extract spatial characteristics of defects and to simultaneously capture features of different types of defects that contain multiple frequency components. As a joint space-frequency analysis method, the 2D Gabor transform (Tao and Gu 2017) can analyze localized frequency features of a signal at various spatial locations and is well-suited for representing and extracting sparsely distributed defect information in GPR signals. However, A fixed-window Gabor transform also fails to solve the problem caused by various type defects with obvious frequency characteristics discrepancy.

To address these challenges, this paper propose a Defectguided Multi-window Gabor Transform Network for GPR B-scan image reconstruction to achieve automatic gain and defect enhancement of raw GPR signals. First, we design a Multi-window Gabor Transform Module within the image reconstruction network (RC-Net) to extract spatialfrequency features of defects at different locations and of various types from original GPR waveform images. This module dynamically computes both a narrow and a wide window functions. The narrow window with high spatial resolution but lower frequency resolution, can accurately capture local details and locate small defects(e.g., pipes, rebar). Conversely, the wide window provides high frequency resolution but lower spatial resolution, focusing on macroscopic structures and coarse textures, which is beneficial for identifying large-scale anomalies (e.g., voids, fractures) and extracting their frequency-domain features. In addition, we construct a defect guidance network (DG-Net) which employs a guidance loss by segmenting defect areas to direct defect areas reconstruction during backpropagation. This enhances the saliency and discriminability of defects in the reconstructed images. Task-driven guidance mechanism ensures that the reconstructed images directly serve subsequent defect detection tasks, ultimately improving defect detection accuracy. The specific contributions of this work are as follows:

• We propose a GPR B-Scan image reconstruction network based on Multi-window Gabor Transform. The integrated Multi-window Gabor Transform Module effectively represent and extract spatial-frequency features of defects at different locations and of various types to achieve automatic gain and defect enhancement of raw GPR signals.

• A defect guidance network is designed to precisely direct the reconstruction of defect areas, enhancing their saliency and discriminability in the reconstructed images to better adapt to downstream tasks such as defect detection.

• Experiments conducted on self-built large-scale realworld GPR dataset and public dataset demonstrate that the proposed MGT-Net achieves state-of-the-art (SOTA) performance in radar image processing tasks.

## Related Work

GPR Wave Signal

GPR wave signals are high-frequency electromagnetic (EM) wave signals (Jol 2008), typically operating in the range of 10 MHz to 2.6 GHz. When propagating through the subsurface and encountering interface between different medias, a portion of energy is reflected back as an echo captured by the receiving antenna, another portion is refracted into the next medium for continued propagation, and the remainder is lost due to scattering and absorption by the surrounding material. Higher frequencies correspond to shorter time durations and wider bandwidths which endow GPR signals with superior temporal resolution and broader frequency coverage. This enables precise detection and imaging of fine-scale underground targets and structures. However, this high-frequency characteristic also introduces significant drawbacks. Highfrequency EM waves suffer more severe energy loss, leading to rapid signal attenuation. This not only limits the penetration depth but also weakens target echoes which may be masked by environmental noise and surface reflections. Moreover, a single target may generate multiple echoes returning to the receiver via different paths. The multi-path effect aggravates imaging blur and artifacts. Precisely isolating and enhancing each target’s reflected signal from complex and diverse stochastic interference remains a significant challenge in GPR image preprocessing.

GPR image preprocessing methods

Following the geotechnical engineering researches (Davis and Annan 1989; Oldenborger, Knoll, and Barrash 2004) published, advancements in GPR data processing have enabled quantitative analysis and estimation of subsurface compositions. Dewow (Gerlitz et al. 1993; Battista, Addison, and Knapp 2009) aims to remove low-frequency or DC components caused by system bias from GPR signals while it indiscriminately removes useful low-frequency information. The multi-bandpass filtering algorithm (Xiao and Liu 2017), discrete wavelet transform (DWT) (Baili et al. 2009), and short-time Fourier transform-based time-frequency filtering technique (Luo et al. 2023) all target noise removal and clutter suppression, but they struggle to handle complex nonlinear noise. Gain, as another method to adjust signal intensity, mainly includes Spreading and Exponential Compensation (SEC) (Allred et al. 2005), Generalized S- Transform (Feng et al. 2015), inverse amplitude attenuation and exponential gain functions (Bianchini Ciampoli et al. 2019), envelope-based gain algorithm (Bai et al. 2020), and gain method based on Stationary Wavelet Packet Transform (SWPT) (Liu et al. 2024b). However, gain functions design and parameters selection for these methods are highly dependent on operator experience. Various migration algorithms, such as diffraction stack migration (Liu et al. 2020), Kirchhoff migration (Yamaguchi, Mizutani, and Nagayama 2020), frequency–wavenumber (F-K) migration (Jiao et al. 2020), phase-shift migration (Song et al. 2006), and reversetime migration (Liu et al. 2024a) have been developed to improve the spatial resolution of GPR images. These methods highly rely on the accuracy of velocity models, but con-

<!-- Page 3 -->

**Figure 1.** Overall Architecture of the proposed MGT-Net. This model can achieve automatic gain and defect enhancement of raw GPR signals during GPR B-Scan image reconstruction. It consists of (a) RC-Net and (c) DG-Net. We design (b) MGTM to extract spatial-frequency features of defects at different locations and of various types. The (c) DG-Net is constructed to accurately direct the reconstruction of defect areas.

structing precise velocity models itself presents a significant challenge. Deep learning-based GPR image preprocessing methods are relatively rare. Liu et al. (2024c) proposed a closed-loop denoising network framework that integrates bandpass filtering into a convolutional neural network (CNN). However, the denoising effectiveness of bandpass filtering is quite limited.

## Methods

The overview of MGT-Net is illustrated in Figure 1. It mainly consists of two parts: an image reconstruction network Figure 1(a) and a defect guidance network Figure 1(c). In this section, we describe the motivation and implementation details of each sub-network in sequence. Finally, we introduce the loss functions employed during the training phase.

Image Reconstruction Network

Raw radar waveform image records the reflection signals generated by the interaction between electromagnetic waves and underground medias, serving as an indirect representation of the electromagnetic properties of underground structures or targets. It is inherently different from optical images. GPR image reconstruction typically needs to adhere to strict physical principles. Therefore, we integrate traditional signal analysis method and propose a GPR B-Scan image reconstruction network based on Multi-window Gabor Transform, as shown in Figure 1(a). This design significantly enhances the interpretability of our network.

Multi-window Gabor Transform. Given an image I(x, y), where x ∈[0, X −1] and y ∈[0, Y −1], the 2D multi-window real-valued discrete Gabor expansion is formulated as:

I(x, y) =

P −1 X p=0

K−1 X k=0

L−1 X l=0

M−1 X m=0

N−1 X n=0 a(p)[k, l, m, n]g(p)

klmn[x, y]

(1) where P is the number of Gabor windows. (K, L) and (M, N) represent the number of sampling points in the spatial and frequency domains of 2D Gabor transform, respectively, X = KM and Y = LN. g(p)

klmn[x, y] denotes the pth Gabor synthesis window function, defined as follows:

g(p)

klmn[x, y] = g(p)[x−kM, y−lN]·exp n j2π hmx

M + ny

N io

(2) where j2 = −1, the corresponding pth Gabor transform coefficient a(p)[k, l, m, n] is computed as follows:

a(p)[k, l, m, n] =

X−1 X x=0

Y −1 X y=0

I(x, y)γ(p)

klmn[x, y] (3)

where γ(p)

klmn[x, y] denotes the pth Gabor analysis window function, defined as follows:

γ(P)

klmn[x, y] = γ(P)[x−kM, y−lN]·exp n j2π hmx

M + ny

N io

(4) The synthesis and analysis window functions are required to satisfy the biorthogonality condition. Therefore, given a 2D Gabor synthesis window, the 2D Gabor analysis window can be derived.

Since the Gaussian function achieves the minimum timebandwidth product under the uncertainty principle, resulting

![Figure extracted from page 3](2026-AAAI-multi-window-gabor-transform-network-for-ground-penetrating-radar-b-scan-image-r/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

in the most compact representation in the time-frequency domain. This work adopts the 2D Gaussian function as the Gabor synthesis window:

g(p)[x, y] =

√

2 Q(p) ·exp

(

−π

(x −X/2)2 + (y −Y/2)2

Q(p) 2

)

(5) where Q(p) denotes the window size of the pth synthesis window, with the constraint Q(p) ≤min

X

2, Y 2

. It serves to adjust the trade-off between spatial resolution and frequency resolution. A larger Q results in lower spatial resolution but higher frequency resolution, whereas a smaller Q yields higher spatial resolution but lower frequency resolution. A single GPR image typically contains defects of various types which exhibit distinct spatial and frequency localized components. It is obvious that Single-Window Gabor Transform fails to effectively represent all types of defects. To sufficiently extract the spatial-frequency features of all defects, we implemented Multi-window Gabor Transform within our image reconstruction network. Given that the computational complexity of the Multi-window Gabor Transform increases proportionally with the number of windows, we limit the number of windows to two to mitigate time complexity. One narrow window is employed to accurately capture local details and locate small-scale defects, while the wide window is used to detect large-scale defects and extract their frequency features. The calculation method of window sizes is detailed in Algorithm 1 in the Appendix.1.

Multi-window Gabor Transform Module. As shown in Figure 1(b), this module takes a feature block I ∈RC×H×W as input, aiming to effectively represent and extract useful information closely related to defects in GPR waveform images. For the input feature block I ∈RC×H×W we adopt a partitioning strategy where H = KM and W = LN. Using Algorithm 1 to compute two window sizes for each feature block. These sizes are substituted into Equation 5 to generate the corresponding analysis window functions. The Gabor transform coefficients of the feature block are then computed using Equation 3:

a(p)(C, k, l, m, n) = γ(p)

klmn[x, y] · I, (p = 1, 2) (6)

The Gabor transform coefficients represent the frequencydomain features of defects at different spatial locations. We reshape a(p) ∈RC×K×L×M×N into a(p) ∈RC×H×W, and modulate the spectrum using different learnable filters Ki ∈RC×H×W. This modulation serves the dual purpose of suppressing noise and enhancing defect features:

˜a(p) = a(p) ⊙Ki (7)

where ⊙denotes element-wise multiplication. Finally, we reshape ˜a(p) ∈RC×H×W back to ˜a(p) ∈RC×K×L×M×N, and reconstruct the output ˜I ∈RC×H×W using the synthesis windows:

˜I =

P −1 X p=0

K−1 X k=0

L−1 X l=0

M−1 X m=0

N−1 X n=0

˜a(p)[k, l, m, n] g(p)

klmn[x, y]

(8)

Defect guidance Network To enhance the saliency and discriminability of defect areas in the reconstructed image, thereby better serving downstream tasks, we construct a defect guidance network, as shown in Figure 1(c). It performs defect segmentation on reconstructed GPR image and computes a defect guidance loss which is employed to optimize the reconstruction network during backpropagation. We adopt a pre-trained ResNeXt-101 (Xie et al. 2017) as a multi-level feature extractor to extract various hierarchical features. First, deeplevel features are concatenated and fused via an attention mechanism to generate a deep context feature Fd = Att concat

F up

1, F2, F down 3 where F1, F2, and F3 represent the feature maps from the deepest three levels, to improve the comprehension of overall structure. Then, a transposed convolution upsample Fd into a guidance Fmap to modulate shallow-level features for detail enhancement. Finally, the network fuses deep-level and shallow-level features and refines these combined features via attention mechanism and convolution to output segmentation result.

PatchGAN Discriminator In conventional GANs, the discriminator typically evaluates the entire image and outputs a single authenticity score while it is not well-suited for GPR images which contain abundant local features. GPR image reconstruction task pay more attention to the realism and clarity of defect areas rather than the smooth background. PatchGAN (Isola et al. 2017) is a discriminator architecture specifically designed to penalize structural discrepancies at the local patch level. It assesses the authenticity of each patch region, encouraging the generator to enhance high-frequency details. The PatchGAN discriminator is composed of four convolutional blocks, where each block consists of a 4 × 4 convolutional layer, a normalization layer, and a ReLU activation. The final output is a 2D matrix, which undergoes an average pooling operation to derive the final image authenticity score.

Loss Function In the image reconstruction network, to balance perceptual quality and detail preservation, we adopt a generative adversarial loss LGAN and a pixel-wise loss LP IX.

LGAN = Ex [∥D(RG(x)) −True∥1] (9) LPIX = Ex,y [∥y −RG(x)∥1] (10) where E denotes the expectation, x is the original image and y is the target GPR image. D represents the PatchGAN discriminator and RG represents the image reconstruction network. True is an all-one vector, the subscript 1 refers to L1 loss (Barron 2019). In the defect guidance network, the guidance loss comprises Binary Cross-Entropy (BCE) Loss and Intersection over Union (IoU) Loss. The former constrains pixel-level discrepancies, while the latter quantifies region overlap. The formulas are as follows:

Lgd = Lbce + Liou (11) Overall, the total loss function is defined as:

Ltotal = LGAN + λ1LPIX + λ2Lgd (12) where λ1 and λ2 are two hyperparameters.

<!-- Page 5 -->

**Figure 2.** Visual comparison between our method and other methods on the GRD dataset.

Dataset Image Number PIP DT CRACK DT GAP PSP S DT LACUNAS GROUND lamp

Train 71 53 Test 297 22 13 Val 194 14 14

**Table 1.** Data characteristics of the GRD dataset. PIP and PIPS denote rebar oriented perpendicular and parallel to the radar’s scanning direction, respectively. DT CRACK is cracks, DT GAP is voids, DT LACUNAS indicates loosened areas, and GROUND LAMP is the ground lamp.

## Experiments

Datasets We construct a large-scale GPR dataset (GRD) for GPR B- Scan image research. This dataset consists of 13,871 groups of images. Each group includes the raw GPR waveform image, a radar image manually processed using traditional methods, an expert-annotated defect location image, and a defect label file. The training set contains 9,728 groups, the test set includes 2,075 groups, and the validation set comprises 2,068 groups. Detailed information is presented in Table 1. Additionally, we incorporate a public dataset (GPRD) (Mojahid et al. 2025), from which 210 pairs of GPR images with defects are selected for training and testing.

Experimental Settings The proposed MGT-Net is implemented in PyTorch 1.13.0, Python 3.7, and CUDA 11.7 on a computer equipped with an NVIDIA GeForce RTX 3090 GPU. The training configuration is as follows: the learning rate of the Adam optimizer is set to 1e-4, and the model is trained for a total of 100 epochs.

The settings of the loss weights and corresponding experimental results are detailed in Table 2. All subsequent experiments adopt the optimal hyperparameter configuration. The parameter count and FLOPs of the model are 116.793M and 231.905G.

Hyperparameter λ1 / λ2 SSIM(%) PSNR λ1

2/1 80.01±3.8 30.11±0.396 5/1 80.99±4.3 29.56±0.587 10/1 81.72±3.5 30.50±0.442 20/1 79.93±4.3 29.97±0.442 λ2

10/2 80.14±4.3 29.83±0.472 10/5 79.77±4.9 29.91±0.401 10/10 79.15±3.8 30.18±0.412 10/20 78.83±4.0 30.05±0.433

**Table 2.** Hyperparameter Experiments

![Figure extracted from page 5](2026-AAAI-multi-window-gabor-transform-network-for-ground-penetrating-radar-b-scan-image-r/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

## Methods

GRD GPRD

SSIM(%) PSNR SSIM(%) PSNR

Pix2Pix (CVPR2017) 69.33 ± 4.1 29.18 ± 0.235 86.12 ± 5.6 30.08 ± 1.901 PGAN (TMI2019) 69.26 ± 6.8 29.37 ± 0.311 86.93 ± 6.7 30.89 ± 2.164 TransGAN (NeurIPS2021) 72.52 ± 5.3 29.44 ± 0.221 86.96 ± 6.6 30.94 ± 1.986 ResViT (TMI2022) 71.39 ± 6.7 29.53 ± 0.363 87.19 ± 6.3 31.07 ± 2.043 Burstormer (CVPR2023) 66.12 ± 6.7 28.13 ± 0.454 85.31 ± 6.9 29.53 ± 2.206 Scenimefy (ICCV2023) 71.00 ± 4.2 29.38 ± 0.291 87.03 ± 5.8 30.54 ± 1.910 DSG (CIBM2024) 64.71 ± 9.2 29.02 ± 0.391 85.23 ± 8.1 29.47 ± 1.977 OKNet (AAAI2024) 69.72 ± 8.5 28.62 ± 0.271 86.38 ± 7.1 28.37 ± 1.860 DN (ECCV2024) 78.32 ± 4.2 30.14 ± 0.447 87.27 ± 6.7 31.15 ± 2.202 MAG (TRPMS2025) 66.53 ± 7.7 29.26 ± 0.355 85.30 ± 7.2 29.51 ± 1.933 SFIN (CVPR2025) 70.02 ± 9.9 29.86 ± 0.359 87.23 ± 7.0 31.12 ± 2.749

Ours 81.72 ± 3.5 30.50 ± 0.442 88.56 ± 6.6 32.02 ± 2.162

**Table 3.** Comparison of our method with other methods on GRD and GPRD datasets.

Comparison with State-of-the arts

To validate the effectiveness of the proposed method, we evaluate MGT-Net on both the GRD dataset and the public GPRD dataset. We also conduct repeated experiments using several mainstream deep learning-based image generation algorithms. For fairness, we adopt the default settings of these methods and fine-tuned on the GRD dataset to achieve optimal performance.

Quantitative analysis. We employed Structural Similarity Index Measure (SSIM) and Peak Signal-to-Noise Ratio (PSNR) as quantitative evaluation metrics to assess the performance of MGT-Net. As shown in Table 3, the experimental results demonstrate that our MGT-Net outperforms existing models in the GPR image reconstruction task.

On the GRD dataset, the large domain gap between the source and target limits the performance of Pix2Pix (Isola et al. 2017). PGAN (Dar et al. 2019) and ResVit (Dalmaz, Yurt, and C¸ ukur 2022) generate multi-contrast images while GPR image reconstruction is not merely about contrast enhancement. Methods such as TransGAN (Jiang, Chang, and Wang 2021), Burstormer (Dudhane et al. 2023), and OKNet (Cui, Ren, and Knoll 2024) expand the receptive field, making them unable to focus on defect areas.The performance of Scenimefy (Jiang et al. 2023)) is limited by its reliance on pre-trained models. DSG (Wang et al. 2024b) and MAG (Wang et al. 2024a) overly focus on pixel-level differences, which enhances the influence of noise in non-defective areas. DN (Ho et al. 2024) aims to mitigate tiling artifacts but tends to over-smooth defect areas. SFIN (Li et al. 2025) employs Fourier transform for spatial-to-frequency domain conversion. However, Fourier transform is not suitable for processing transient and non-stationary signals like GPR data.

On the GPRD dataset, all methods exhibit excellent performance, but MGT-Net still achieves the best results. We attribute this to the minimal differences between the raw and target images in the GPRD dataset, which allows even rel- atively simple models to achieve competitive performance. Furthermore, the training set of the GPRD dataset contains only 160 pairs of GPR images. This further demonstrates that our model can effectively handle extreme conditions with a limited number of training samples.

Visual analysis. We further conduct a visual comparison between our method and other methods on the GRD dataset in Figure 2 and the GPRD dataset in Figure 3. The contours of defect areas in the GPR images reconstructed by our method exhibit more clearly and distinctly. Through magnifying the defect areas, the heatmaps in which darker colors indicate higher similarity and brighter colors indicate lower similarity demonstrate that the GPR images reconstructed by our methods more closely approximate the ground truth, achieving superior defect enhancement.

**Figure 3.** Visual comparison between our method and other methods on the GPRD dataset.

Defect detection experiments on GRD. We designed the defect guidance network not only to guide the reconstruction

![Figure extracted from page 6](2026-AAAI-multi-window-gabor-transform-network-for-ground-penetrating-radar-b-scan-image-r/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Methods

BER IOU PA F-measure MAE

Pix2Pix (CVPR2017) 11.91 61.07 77.72 79.38 3.72 PGAN (TMI2019) 11.87 59.94 78.03 79.30 4.12 TransGAN (NeurIPS2021) 10.07 62.48 81.69 80.23 3.95 ResVit (TMI2022) 9.46 62.83 82.02 80.28 3.67 Burstormer (CVPR2023) 9.55 62.13 80.69 80.19 3.68 Scenimefy (ICCV2023) 9.76 63.95 82.11 81.06 3.63 DSG (CIBM2024) 10.06 62.81 81.65 80.38 3.63 OKNet (AAAI2024) 10.21 60.57 81.66 78.15 3.87 DN (ECCV2024) 9.39 65.04 82.81 82.11 3.36 MAG (TRPMS2025) 10.06 60.90 81.85 78.65 3.81 SFIN (CVPR2025) 9.88 62.64 81.45 80.24 3.86

Ours 7.01 66.43 85.23 82.54 3.03

**Table 4.** The results of defect detection by using the reconstructed GPR images from different methods.

network to focus on defect regions, but also to better support downstream tasks such as defect detection. Due to the lack of defect annotations in the GPRD dataset, defect detection experiments were conducted only on the GRD dataset, as shown in Table 4. First, we utilize the GPR images reconstructed by MGT-Net and other methods as their respective training sets (1,500 images) and validation sets (568 images). Then, identical defect detection networks were trained on each method’s training set, and evaluation metrics were computed on the corresponding validation set. The evaluation metrics include Balanced Error Rate (BER), Intersection over Union (IOU), Pixel Accuracy (PA), as well as Fmeasure and Mean Absolute Error (MAE), which are commonly used in salient object detection. The results show that images reconstructed by MGT-Net achieve significantly higher detection accuracy compared to those generated by other methods. This validates the accuracy of our motivation in designing the defect guideance network.

Ablation studies

To evaluate the contribution of each proposed component to the overall model performance, we conduct an ablation study on the GRD dataset. The ablation results are summarized in Table 5. The baseline refers to the U-Net-based generative network.

DGNet denotes the Defect Guidance Network. By integrating DGNet into the baseline and introducing the guidance loss, the model achieves improvements of 3.12% and 1.27 in SSIM and PSNR. This sufficiently demonstrates that DGNet effectively guides the reconstruction of defect areas, enhancing the saliency and discriminability of defects.

SGTM refers to the Single-window Gabor Transform Module. By integrating SGTM into the baseline, as shown in Table 5, the SSIM improves by 7.13% and the PSNR increases by 1.66. This indicates that the Gabor transform, as a joint space-frequency analysis method, can analyze frequency features of signals at various spatial locations and is well-suited for representing and extracting sparsely dis-

## Methods

SSIM(%) PSNR

Baseline 67.93±6.9 28.02±0.398 Baseline+DGNet 71.05±6.1 29.29±0.391 Baseline+SGTM 75.06±5.2 29.68±0.466 Baseline+MGTM 78.59±4.8 30.21±0.488

MGT-Net 81.72±3.5 30.50±0.442

**Table 5.** Ablation studies for the proposed components.

tributed defect information in GPR wave signals.

MGTM refers to the Multi-window Gabor Transform Module. We replace SGTM with MGTM while keeping all other settings unchanged. As shown in Table 5, the model’s SSIM improves by 10.66% and PSNR increases by 2.19. This finding emphasizes that multiple windows can better capture various type defects with obvious discrepancy in frequency domain.

## Conclusion

In this paper, we propose a novel Defect-guided Multiwindow Gabor Transform Network (MGT-Net) for GPR Bscan image reconstruction, achieving automatic gain and defect enhancement of raw GPR signals. The Multi-window Gabor Transform Module can effectively represent and extract spatial-frequency features of defects at different locations and of various types. The defect guidance network can accurately direct the reconstruction of defect areas and enhance the saliency and discriminability of defects. Experimental results on our large-scale, real-world GPR datasets show that our proposed MGT-Net achieves state-of-the-art performance. Future work will focus on further improving the ability to extract defect features and designing new algorithms to accelerate the Gabor computation process.

<!-- Page 8 -->

## Acknowledgements

We thank Anhui Guimu Robot Co., Ltd. for their valuable help. This work was supported in part by the Anhui Provincial Key Research and Development Program under Grant NO.202304a05020047, in part by the National Natural Science Foundation of China under Grant 62576007, and in part by the Natural Science Foundation for the Higher Education Institutions of Anhui Province under Grant 2022AH050091.

## References

Allred, B.; Daniels, J.; Fausey, N.; Chen, C.; Peters, L.; Youn, H.; et al. 2005. Important considerations for locating buried agricultural drainage pipe using ground penetrating radar. Applied engineering in agriculture, 21(1): 71–87. Bai, X.; Luo, X.; Guo, S.; Wang, L.; Chen, H.; Mi, H.; Liu, L.; Ji, M.; and Gao, Y. 2020. A novel gain control method based on extremum envelope for high speed array GPR. In 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall), 1–5. IEEE. Baili, J.; Lahouar, S.; Hergli, M.; Al-Qadi, I. L.; and Besbes, K. 2009. GPR signal de-noising by discrete wavelet transform. Ndt & E International, 42(8): 696–703. Barron, J. T. 2019. A general and adaptive robust loss function. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 4331–4339. Battista, B. M.; Addison, A. D.; and Knapp, C. C. 2009. Empirical mode decomposition operator for dewowing GPR data. Journal of Environmental & Engineering Geophysics, 14(4): 163–169. Bianchini Ciampoli, L.; Tosti, F.; Economou, N.; and Benedetto, F. 2019. Signal processing of GPR data for road surveys. Geosciences, 9(2): 96. Cai, M.; Zhang, H.; Huang, H.; Geng, Q.; Li, Y.; and Huang, G. 2021. Frequency domain image translation: More photorealistic, better identity-preserving. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 13930–13940. Cui, Y.; Ren, W.; and Knoll, A. 2024. Omni-kernel network for image restoration. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 1426–1434. Dalmaz, O.; Yurt, M.; and C¸ ukur, T. 2022. ResViT: Residual vision transformers for multimodal medical image synthesis. IEEE Transactions on Medical Imaging, 41(10): 2598– 2614. Dar, S. U.; Yurt, M.; Karacan, L.; Erdem, A.; Erdem, E.; and Cukur, T. 2019. Image synthesis in multi-contrast MRI with conditional generative adversarial networks. IEEE transactions on medical imaging, 38(10): 2375–2388. Davis, J. L.; and Annan, A. P. 1989. Ground-penetrating radar for high-resolution mapping of soil and rock stratigraphy 1. Geophysical prospecting, 37(5): 531–551. Dudhane, A.; Zamir, S. W.; Khan, S.; Khan, F. S.; and Yang, M.-H. 2023. Burstormer: Burst image restoration and enhancement transformer. In 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 5703– 5712. IEEE.

Feng, K.; Zhao, Y.; Zhang, Z.; and Ge, S. 2015. Stratigraphic absorption compensation of GPR signal based on improved S-transform. In 2015 8th International Workshop on Advanced Ground Penetrating Radar (IWAGPR), 1–4. IEEE. Gerlitz, K.; Knoll, M. D.; Cross, G. M.; Luzitano, R. D.; and Knight, R. 1993. Processing ground penetrating radar data to improve resolution of near-surface targets. In 6th EEGS Symposium on the Application of Geophysics to Engineering and Environmental Problems, cp–209. Gou, Y.; Li, B.; Liu, Z.; Yang, S.; and Peng, X. 2020. Clearer: Multi-scale neural architecture search for image restoration. Advances in neural information processing systems, 33: 17129–17140. Ho, M.-Y.; Wu, C.-M.; Wu, M.-S.; and Tseng, Y. J. 2024. Every pixel has its moments: Ultra-high-resolution unpaired image-to-image translation via dense normalization. In European Conference on Computer Vision, 312–328. Springer. Isola, P.; Zhu, J.-Y.; Zhou, T.; and Efros, A. A. 2017. Imageto-image translation with conditional adversarial networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, 1125–1134. Jiang, Y.; Chang, S.; and Wang, Z. 2021. Transgan: Two pure transformers can make one strong gan, and that can scale up. Advances in Neural Information Processing Systems, 34: 14745–14758. Jiang, Y.; Jiang, L.; Yang, S.; and Loy, C. C. 2023. Scenimefy: Learning to craft anime scene via semisupervised image-to-image translation. In Proceedings of the IEEE/CVF international conference on computer vision, 7357–7367. Jiao, L.; Ye, Q.; Cao, X.; Huston, D.; and Xia, T. 2020. Identifying concrete structure defects in GPR image. Measurement, 160: 107839. Jol, H. M. 2008. Ground penetrating radar theory and applications. elsevier. Li, B.; Xue, K.; Liu, B.; and Lai, Y.-K. 2023. Bbdm: Imageto-image translation with brownian bridge diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern Recognition, 1952–1961. Li, H.; Wu, Z.; Shao, R.; Zhang, T.; and Fu, Y. 2025. Noise calibration and spatial-frequency interactive network for stem image enhancement. In Proceedings of the Computer Vision and Pattern Recognition Conference, 21287– 21296. Liu, H.; Lin, C.; Cui, J.; Fan, L.; Xie, X.; and Spencer, B. F. 2020. Detection and localization of rebar in concrete by deep learning using ground penetrating radar. Automation in construction, 118: 103279. Liu, H.; Yue, Y.; Lian, Y.; Meng, X.; Du, Y.; and Cui, J. 2024a. Reverse-time migration of GPR data for imaging cavities behind a reinforced shield tunnel. Tunnelling and Underground Space Technology, 146: 105649. Liu, X.; Ling, T.; Liu, W.; Tan, J.; Zhang, L.; and Jiang, Y. 2024b. Accurate gain method for ground-penetrating radar signals based on stationary wavelet packet transform. Journal of Applied Geophysics, 228: 105473.

<!-- Page 9 -->

Liu, X.; Liu, S.; Jia, Z.; Vogt, D.; Tian, S.; Liu, X.; and Lu, Q. 2024c. GPR Closed-Loop Denoising Based on Bandpass Filtering Constraints. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–14. Luo, W.; Lee, Y. H.; Yusof, M. L. M.; and Yucel, A. C. 2023. A depth-adaptive filtering method for effective GPR tree roots detection in tropical area. IEEE Transactions on Instrumentation and Measurement, 72: 1–10. Mojahid, A.; El Ouai, D.; El Amraoui, K.; and El-Hami, K. 2025. Intelligent Recognition of Subsurface Utilities and Voids: A Ground Penetrating Radar Dataset for Deep Learning Applications. Data in Brief, 59(1): 111338. Noshahri, H.; van der Meijde, M.; and olde Scholtenhuis, L. 2022. GPR surveys in enclosed underground sewer pipe space. Tunnelling and Underground Space Technology, 129: 104689. Oldenborger, G. A.; Knoll, M. D.; and Barrash, W. 2004. Effects of signal processing and antenna frequency on the geostatistical structure of ground-penetrating radar data. Journal of Environmental & Engineering Geophysics, 9(4): 201– 212. Song, J.; Liu, Q. H.; Torrione, P.; and Collins, L. 2006. Two-dimensional and three-dimensional NUFFT migration method for landmine detection using ground-penetrating radar. IEEE Transactions on Geoscience and Remote Sensing, 44(6): 1462–1469. Tao, L.; and Gu, J.-j. 2017. Real-valued Gabor transforms: theory algorithms and applications. Anhui Sci. Technol. Press Anhui. Wang, H.; Li, Z.; Han, X.; Zhang, G.; Zhang, Q.; Zhang, D.; and Liu, F. 2024a. MAG-Net: A Multiscale Adaptive Generation Network for PET Synthetic CT. IEEE Transactions on Radiation and Plasma Medical Sciences, 9(1): 83–94. Wang, H.; Wang, X.; Liu, F.; Zhang, G.; Zhang, G.; Zhang, Q.; and Lang, M. L. 2024b. DSG-GAN: A dual-stagegenerator-based GAN for cross-modality synthesis from PET to CT. Computers in Biology and Medicine, 172: 108296. Xiao, J.; and Liu, L. 2017. Suppression of clutters caused by periodic scatterers in GPR profiles with multibandpass filtering for NDT&E imaging enhancement. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 10(10): 4273–4279. Xie, S.; Girshick, R.; Doll´ar, P.; Tu, Z.; and He, K. 2017. Aggregated residual transformations for deep neural networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, 1492–1500. Yamaguchi, T.; Mizutani, T.; and Nagayama, T. 2020. Mapping subsurface utility pipes by 3-D convolutional neural network and Kirchhoff migration using GPR images. IEEE Transactions on Geoscience and Remote Sensing, 59(8): 6525–6536. Zhang, L.; Chen, X.; Tu, X.; Wan, P.; Xu, N.; and Ma, K. 2022. Wavelet knowledge distillation: Towards efficient image-to-image translation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 12464–12474.
