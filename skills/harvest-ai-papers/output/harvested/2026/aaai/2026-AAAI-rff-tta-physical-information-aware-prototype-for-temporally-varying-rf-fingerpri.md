---
title: "RFF-TTA: Physical Information-Aware Prototype for Temporally Varying RF Fingerprinting Online Test-Time-Adaptation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37034
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37034/40996
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# RFF-TTA: Physical Information-Aware Prototype for Temporally Varying RF Fingerprinting Online Test-Time-Adaptation

<!-- Page 1 -->

RFF-TTA: Physical Information-Aware Prototype for Temporally Varying RF

Fingerprinting Online Test-Time-Adaptation

Taotao Li1,2, Yiyang Li1, Zhenyu Wen1*, Jiahao Lin1, Jinhao Wan1, Jie Su1, Cong Wang3, Zhen

Hong1

1Institute of Cyberspace Security, Zhejiang University of Technology, Hangzhou, China 2 College of Computer Science and Technology, Zhejiang University of Technology, Hangzhou, China 3 College of Control Science and Engineering, Zhejiang University, Hangzhou, China {taotaoli, zhenyuwen}@zjut.edu.cn

## Abstract

In recent years, deep learning(DL)-based RF fingerprint (RFF) recognition has become a promising wireless device verification technique in the Internet of Things (IoT). However, temporal variations in device load status effects as well as channel effects can lead to inconsistent RF fingerprint distributions during the training and testing phases, which causes performance degradation of DL models. To address this problem, we propose the first test-time-adaptation (TTA) approach to improve the domain generalization ability of RFF recognition models. We first analyze the causes of time-varying RFF distribution shifts, such as carrier frequency offset (CFO), and develop a physical impairment-based data augmentation strategy. Based on this, we further propose a physically information-aware prototype to guide the model for TTA. Our method requires no model retraining or labeled test samples, and is a lightweight, nonparametric solution. Finally, our approach is extensively evaluated using mobile phones with the IEEE 802.11 orthogonal frequency division multiplexing (OFDM) system, which demonstrates that our scheme can effectively improve RFF average recognition performance by about 7.8%.

## Introduction

The proliferation of Internet of Things (IoT) devices has significantly advanced the development of smart homes and smart city applications. Nevertheless, the inherent openness of wireless communication channels renders these connected devices particularly vulnerable to security threats, including unauthorized access. Recent progress in RF fingerprinting (RFF) has established it as a promising authentication mechanism for IoT systems (Huang et al. 2017; Polak and Goeckel 2015), utilizing intrinsic hardware imperfections like IQ imbalance (Huang et al. 2017), loop filter variations (Brik et al. 2008), and clock jitter (Jana and Kasera 2008) as unique, tamper-resistant identifiers. In recent years, deep learning (DL)-based RFF recognition techniques have been widely investigated, which can achieve impressive classification accuracy (Riyaz et al. 2018; Shen et al. 2022). However, most DL approaches assume ideal conditions with stable, independent, and identically distributed (i.i.d.) for RFF. Real-world deployments

*Corresponding author: zhenyuwen@zjut.edu.cn Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** Our work addresses the more realistic scenario where complex device loads (e.g., on a mobile phone) induce DSE, distorting the RFF and degrading accuracy in the test phase.

face significant domain shifts due to environmental changes and device status variations as shown in Fig. 1, leading to degraded generalization performance. This presents two key challenges: Channel Effect. Wireless communication environments exhibit dynamic channel conditions and noise levels that vary with time, location, and acquisition settings. These variations cause significant shifts in signal characteristics (amplitude, frequency, and phase), ultimately degrading the classification performance of deep learning models. Device Status Effect (DSE). Wireless devices experience varying operational states (e.g., various application loads lead to temperature differences) that significantly affect their RF fingerprints (Li et al. 2024). As shown in Fig. 3c, even fundamental RFF characteristics like carrier frequency offset (CFO) and carrier phase offset (CPO) exhibit notable distribution shifts across different mobile applications for the same device.

Existing studies have primarily focused on mitigating channel effects, proposing methods such as extracting channel-independent features (Liu et al. 2019; Restuccia et al. 2019), developing channel-robust features through transmitter operation (Rajendran and Sun 2022; Rajendran et al. 2020), and applying advanced signal processing algorithms (Xing et al. 2022; Shen et al. 2022). However, these algorithms do not take into account the phenomenon of RFF offset in the device itself due to complex DSE. To cope with the DSE, the researchers explored the effect of temperature

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

686

![Figure extracted from page 1](2026-AAAI-rff-tta-physical-information-aware-prototype-for-temporally-varying-rf-fingerpri/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

RFF-TTA

... Online Test Streaming

... Online Test Streaming

Channel 1, Load Status 1 Unknown Channel or Load

Immediate Inference

RFF-TTA

Immediate Inference

Source

Pre-train

Train

Parameter

**Figure 2.** We propose RFF-TTA to solve this DG problem. RFF-TTA can utilize batch samples from an online test stream to guide model adaptation and direct inference.

on the CFO fingerprints in mobile phone (Li et al. 2024). Then, the research attempts to address this problem by modeling recognition at different phone temperatures (Gu et al. 2024). However, the prior temperature of the phone is unavailable in many cases. Furthermore, the combined effects of channel variations and DSE lead to highly complex and unpredictable RFF distribution patterns, significantly compounding the identification challenges.

Recent studies have attempted to address the RFF distribution shift problem through domain adaptation (DA) (Zhang et al. 2024; Cai et al. 2025) and domain generalization (DG) (Tang et al. 2024) techniques. However, DG struggles with unseen device states, while DA requires test data for training - both are impractical for online scenarios. In the broader machine learning field, test-time adaptation (TTA) has emerged as an effective paradigm to address distribution shifts by dynamically adjusting models using unlabeled test data. This approach is particularly appealing for RFF recognition as it enables real-time adaptation without costly retraining. However, existing TTA strategies (Jiang et al. 2024; Gong et al. 2025), primarily developed for computer vision tasks, demonstrate limited effectiveness when directly applied to RF fingerprint data due to fundamental differences in data characteristics. For example, as shown in Fig. 3a, the latest decoupled prototype learning (DPL) (Wang et al. 2025) and non-parametric classifier (NPC) (Zhang et al. 2023) methods are unstable and have even experienced a decline compared to the DG method.

This paper presents RFF-TTA, a novel TTA method that uniquely exploits inherent DSE characteristics like CFO to guide model adaptation. Unlike conventional approaches, our core innovation lies in using physically-grounded signal impairment transformations to generate reliable prototype points, which then provide well-directed adaptation targets. This physics-aware design specifically addresses the unique challenges of RFF distribution shifts on DSE. Our main contributions are as follows:

• To the best of our knowledge, we are the first to propose a RFF-TTA technique that combines physical impairments to drive model adaptation. Our RFF-TTA can significantly improve the existing RFF method’s performance upper bound. • We propose a physical impairment-based (CFO and CPO) data augmentation framework targeted to overcome the DSE by systematically characterizing the random drift properties of hardware impairments.

• We propose a physical information-aware prototype ensemble approach by utilizing physical impairmentsbased augmented data. The method is non-parametricbased and can directly utilize unlabeled online batch flow data to implement TTA.

## Background

and Challenges Temporally-Varying RF Fingerprint Modeling This study examines RFF identification in WiFi-enabled mobile devices using IEEE 802.11 OFDM systems. During signal transmission, various analog components (including DACs, IF filters, oscillators, power amplifiers, and antennas) imprint unique hardware-specific characteristics onto the signals. These components introduce distinct physicallayer impairments such as DC offset, CFO, and I/Q imbalance, which collectively form distinctive device signatures (Huang et al. 2017). We mathematically model these hardware imperfections through a composite function f(·). For a given baseband signal xb(t) at time t, its transformed version after traversing the RF front-end can be represented as f(xb(t)). Furthermore, to account for the electromagnetic channel’s influence during wireless propagation, we introduce a channel response function h(·). Consequently, the received signal rk(t) from the k-th transmitting device can be mathematically expressed as rk(t) = fk(xb(t)) ∗h(t) + wgn(t), k ∈{1, 2,.., K}, (1)

where the K denotes the number of transmitters, ∗denotes the linear convolution operation, wgn(t) denotes the additive white Gaussian noise (AWGN).

In real-world RFF implementations (Fig. 1), dynamic device workloads and fluctuating channel conditions can significantly alter fingerprint characteristics. Our analysis begins with the established hardware imperfection framework from (Zheng, Sun, and Ren 2019), which provides fundamental insights into these variations. Specifically, we examine fk(xb(t), τ) = A(1 + powk(xb(t), τ))· ei(wc+∆wk+Θ)2π(nTs+τ)+iφk(xb(t),τ) (2)

where A denotes the amplitude, nTs is the sampling interval, τ is the sampling phase, wc is the carrier frequency, ∆wk denotes the CFO of k-th device, Θ(nTs + τ) is modulation information, powk(xb(t), τ) and φk(xb(t), τ) denote the nonlinear part of the amplitude and CPO, respectively.

Since signal propagation goes through wireless channels, we apply channel effects h(·) to the transmit signal in Eq. 2, so that the signal at the receiver in Eq. 1 is simplified as rk(xb(t), τ) = fk(xb(t), τ)ei(2π∆wk+φk)(xb(t),τ)

∗h(t) + wgn(t). (3)

Online TTA Definition To address such distribution shifts, TTA offers an efficient solution by leveraging target domain batch data for realtime model adaptation, eliminating the need for retraining while maintaining low computational overhead—making it

687

![Figure extracted from page 2](2026-AAAI-rff-tta-physical-information-aware-prototype-for-temporally-varying-rf-fingerpri/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-rff-tta-physical-information-aware-prototype-for-temporally-varying-rf-fingerpri/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

0 2 4 6 8 10 12 14 16 0.82

0.84

0.86

0.88

0.90

0.92

Accuracy

Number of Test Streams

Ours NPC DPL

Baseline Accuracy: 0.875

(a) (b)

0

1

## 2 S1 S2 S3 S4 S5 S6

CPO(rad)

CFO(Hz) (c)

Day 1 Day 2 Day 3 Day 4 Day 5 40

60

80

100

Accuracy (%)

CFO Comp. w/o CFO Comp. CFO Aug.(Ours)

(d)

**Figure 3.** (a) Comparative analysis of different TTA algorithms for RFF; (b) Analysis of the causes of TTA failure; (c) RF physical feature distribution offset in different days, devices and application loads, S1∼S2: Day1-Dev0-App0∼1, S3∼S4: Day1-Dev1-App0∼1, S5∼S6: Day2-Dev1-App0∼1; (d) Effectiveness analysis of CFO compensation.

particularly suitable for online testing scenarios. Assuming the existence of multi-source domain dataset denoted as Dtrain = {Ds}S s=1 with Ds = {rs(t) = (xi s, yi s)}N i=1, where xi s ∈CM denotes a signal sample with dimension M in complex space C, yi s ∈RK denotes the K-dimensional label by one-hot encoding in real number space R, S and N denote the number of domains and the number of samples, respectively. Similarly, we define the T target domain test sample as Dtest = {Dt}T t=0 with Dt = {rt = (xi t, yi t)}N i=1. It is noteworthy that DS̸ = DT, and probability distribution shift exists between p(xS) and p(xT). Specifically, we first train a DL model Fθ: xi →yi on Ds. Then, for a stream of unlabeled batch test samples {xb ∼p(xT)}B b=0, TTA aims to minimize the deviation of the distribution of model features Fθ(y|x) from the distribution of test data P(yb|xb), i.e., min θ Exb∼p(xT) ∥Fθ(y|x) −P(yb|xb)∥→0 (4)

where b denotes the batch index, ∥·∥denotes the distance.

## Analysis

of TTA Challenges under Time-Varying RFF

To realize online TTA for RFF, the most mainstream approach is currently based on class prototype movement learning, such as DPL(Wang et al. 2025) and NPC(Zhang et al. 2023), which has a minimal computational overhead and does not require model optimization training. Fig. 3 (a) shows the results of these TTA methods for RFF. We can observe that these methods are unstable compared to ours, which have larger error bands, and the DPL also produces an accuracy degradation compared to baseline accuracy. Instability Analysis. As shown in Fig. 3 (b), the feature space contains distinct prototypes for class 1 (P1) and class 2 (P2), with corresponding batch test samples {xb 1}B i=0 and {xb

2}B i=0. There is a vertical decision boundary line in the space dividing the space into left and right parts. When testing adaptive, few-shot test samples {xb

1}B i=0 of class 1 are assigned pseudo-labels as y2 due to domain bias (red triangles in the figure). Due to the noise in the pseudo-labeling of the test sample, the P2 will move towards that sample {xb

1}B i=0, which results in more test samples of x1 being misclassified as y2. The wrong direction of prototype movement will result in model performance degradation. Therefore, this paper focuses on how to design reliable test adaptive directions for RFF recognition models. Solution Ideas. Based on the above analysis, if we increase the sample size of class 1 and class 2, a more realistic distribution will be revealed, thus providing more accurate prototype points for the target domain. However, in the online test stream, the samples are reached in batches, and there is a problem of insufficient sample size. To increase the sample size, an intuitive approach is data augmentation. However, most of the data augmentation in TTA is image-based, which makes it difficult to apply to RFF. For this reason, we need to explore the key factors of the time-varying RFF distribution bias and use them to design a suitable augmentation strategy.

Fortunately, as described earlier in Eq. 3, the factors of RFF offset mainly contain CFO and CPO. Fig. 3 (c) illustrates the phenomenon of CFO and CPO shift of RFF for different time and application load cases. Conventional wisdom might suggest applying CFO compensation techniques, a common preprocessing step in many RFF systems (Tang et al. 2024), to eliminate this instability. However, our empirical results, presented in Fig. 3 (d), reveal a counter-intuitive finding: applying standard CFO compensation dramatically degrades recognition accuracy in our test scenario. This contradicts previous work, which often relied on dedicated WiFi modules with stable thermal profiles and thus stable RFF signatures. The above observations provide important data augmentation ideas for our TTA implementation, i.e., CFO and CPO augmentation can generate samples to approximate the true distribution, and thus determine a more accurate direction of adaptation for prototype-based TTA.

Physical Information-Aware Prototype-based

RFF-TTA Scheme Overview

To enhance the DG capability of radio frequency fingerprint (RFF) recognition, we propose RFF-TTA, a novel TTA method leveraging physics-aware prototypes. Our design idea is mainly to utilize CFO and CPO augmentation, which are physical impairments, to get a more accurate sample distribution. From there, we determine the physics-aware points of the test samples and guide the model prototype points for sliding adaptation. Specifically, as illustrated in Fig. 4, our approach first pre-trains source-domain data to

688

![Figure extracted from page 3](2026-AAAI-rff-tta-physical-information-aware-prototype-for-temporally-varying-rf-fingerpri/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

**Figure 4.** Framework diagram of the RFF-TTA. The model employs prototype learning for pre-training to obtain category prototypes. During testing, each data stream undergoes CFO/CPO augmentation before feature integration. An entropy compression scheme then computes test prototypes, which adaptively update memory bank prototypes via sliding average.

establish category prototypes stored in a memory bank. During online inference, we perform physics-informed augmentation on streaming test data, extract and fuse features from both original and augmented samples. Further, we integrate the two deep features and classification probabilities. These are progressively integrated into the memory bank via exponential moving average, enabling continuous model adaptation to new domains.

Feature Pre-training Stage To overcome channel-induced distribution shifts in RF fingerprinting, we develop a dual approach combining channelinvariant feature extraction with prototype learning. RF Signal Introduction. In this paper, we mainly use device information-independent WiFi preamble signals to perform the RFF recognition task. The IEEE 802.11 OFDM standard defines a preamble at the beginning of the packet, which consists of 10 short training symbols (STS), 1 guard interval (GI), and 2 long training symbols (LTS)(Xing et al. 2022). For the received RF signals x(t), we first use a synchronization technique (Liu et al. 2019) to determine the starting point of the signal, and then use root-mean-square normalization. Channel-Invariant Fingerprint. Since different symbols in the same RF signal go through the same channel, we mainly utilize different adjacent symbol bits in the preamble signal, i.e., STL and LTS, to cancel the channel (Xing et al. 2022). Our main approach is to use the Fast Fourier Transform (FFT) and logarithmic operations Flog to transform the channel time-domain convolution in Eq. 3 into a frequencydomain addition that eliminates the channel. For more information, please refer to the (Xing et al. 2022) and Appendix. Our channel-invariant RFF consists of two main components, namely Steady RFF Symbol Pairs and Transient RFF Symbol Pairs.

Steady RFF Symbol Pairs. In the preamble, the first STS signal, as well as the GI, usually contains transient infor- mation for device startup and information transition. In contrast, the 2-th to 10-th STS as well as LTSs are steady-state signals. We use the 2nd to 5th STS xST S

2:5 to compute the logarithmic spectrum and then perform a subtraction operation with the first LTS xLT S

1 to eliminate the channel. Therefore, we define the steady-state RFF as

RFFStable = {(Flog(xST S

2:5) −Flog(xLT S 1)), (Flog(xST S

5:9) −Flog(xLT S 2))}, (5)

where xST S

5:9 denotes the 2nd to 5th STSs, xLT S

2 denotes the 2-th LTS. Transient RFF Symbol Pairs. Similarly, we define the remaining transient RFF to be

RFFT ransient = {Flog(xST S

0:4)− Flog(concat(xST S

9:10, xGI, xLT S 1∗))}, (6)

where xLT S

1∗ denotes the first 16 bits of the 1-th LTS, xGI denotes GI segment, xST S

9:10 denotes the 9-th to 10-th STSs, concat(·) denotes the a concatenate operation. Prototype-based model pre-training. After that, we integrate RFFT ransient and RFFStable to ˜x and use ResNet- 18(He et al. 2016) as a feature extractor to perform the classification task. Specifically, we first train the feature embedding network Fθ(•) and classifier W0. The classifier weights wi are represented by the average embedding of each new class yi (i.e., the class prototype or the most representative feature of the class). The class prototype wj in Ds can be calculated by:

wj =

1 |Ds|

|Ds| X i=1

I(yi = j)Fθ(˜xi)

2

, (7)

where ∥•∥2 denotes the l2 normalization and I(·) denotes the indicator function. With the class prototype points wi, we can calculate the class probability pj for each train sample

689

![Figure extracted from page 4](2026-AAAI-rff-tta-physical-information-aware-prototype-for-temporally-varying-rf-fingerpri/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

as p(y = j|˜x; Fθ) = exp(sim(Fθ(˜x), wj)) P j∈ys exp(sim(Fθ(˜x), wj)), (8)

where sim(•) denotes the cosine similarity function. The Eq. 8 suggests that the similarity of the sample to the class prototype point determines the sample prediction category.

Finally, we use prototype contrastive learning loss ℓcontr for pre-training:

ℓcontr = −1

|Ds|

|Ds| X i=1 log(exp(sim(Fθ(˜x), wj)) P j∈ys exp(sim(Fθ(˜x), wj))).

(9) Using Eq. 9 to train the DL model, we can get the prototype points wj for each category yj, which are saved in the memory bank as Ps = {w0, w1,...wj|wj ∈Ds}.

Online Test Time Adaptive Scheme for RFF

Physical Impairment Data Augmentation. We aim to design TTA strategies using batch online test data streams to improve the generalization of DL models to unseen RFF distributions. We first utilize the physical information (CFO, CPO) for data augmentation and then compute the prototype point as an adaptive direction.

CFO Random Augmentation. To determine the scope of the augmentation, we first use the CFO estimation method in (Shen et al. 2021), which consists mainly of coarse frequency offset ∆

⌢w coarse estimation and fine frequency offset ∆

⌢w fine estimation. Then, we perform frequency random offset augmentation on the source domain. We define a variable α obeying a uniform distribution: α ∼U[0, 1]. We design the randomly augmented frequency offset to be α∆f ∼U[0, ∆f], where ∆f ∈max[∆

⌢w fine, ∆

⌢w coarse] denotes the frequency offset range. In combination with Eq. 3 and without considering noise, the frequency augmentation can be calculated by the following equation

ˆx(t)f = fk(xb(t), τ)ei(2π(∆wk+α∆f)+φt)(xb(t),τ) ∗h(t).

(10) CPO Random Augmentation.Similarly, we propose random phase ∆φ augmentation by utilizing a random variable β ∼U[−1, 1] to control. The augmented phase offset can be denoted as β∆φ ∼U[−β∆φ, β∆φ]. In combination with Eq. 3, the phase augmentation can be calculated by the following equation

ˆx(t)p = fk(xb(t), τ)ei(2π∆wk+φt+β∆φ)(xb(t),τ) ∗h(t).

(11) We perform channel-invariant fingerprint extraction of the augmented ˆx(t)f and ˆx(t)p through Eqs. 5 and 6, which are then fed into the DL model to obtain the augmented features Fθ(˜xaug). Physics Informed-Aware Prototypical Ensemble. For online batch flow data, we use the original test data ˜xraw and its augmented sample pairs ˜xaug to jointly perceive the prototype point distribution of the test set. We first average this sample pairwise and categorical probabilities to obtain the ensemble features Fθ(˜x)ens and probabilities p(˜x)ens, respectively, as

Fθ(˜x)ens = (Fθ(˜xraw) + Fθ(˜xaug))/2 p(˜x)ens = (p(˜x)raw + p(˜x)aug)/2 (12)

where Fθ(˜xraw) denote the extracted original feature, p(˜x)raw and p(˜x)aug denote the probability values for the original sample classification and the augmented sample, respectively, which can be calculated using Eq. 8.

We then perform the computation of the physical-aware prototype Pens. We can assign pseudo-labels ˜y for each sample by p(˜x)ens, i.e., ˜y = arg max p(˜x)ens. Based on the pseudo-labeling, we can classify the test samples into categories so that we can calculate the prototype points of each test category. However, since pseudo-labeling contains noise, i.e., false predictions, this can lead to bias in the calculation of physically perceived prototype points. Therefore, we need to filter the test samples and extract high-confidence samples as the source of prototype calculation samples. We mainly use entropy compression methods to extract highconfidence samples, which can be computed by

Hi ens = −

Xys j=1 σ(p(˜x)j ens) log σ(p(˜x)j ens) (13)

where Hi ens denotes information entropy of the i-th xi b, σ denotes the softmax function. For the batch test sample information entropy set {Hi ens}N i=0, we select topK samples, topK = arg sort i∈{1,...,N}

{Hi ens}[: K]

SK = {xi b|I(i ∈topK) = 1}

, (14)

where sort(·) denotes the sorting function, SK denotes the subset of samples that are selected. Eq. 14 clarifies that the smallest information entropy samples ranked as K are selected, and these samples usually have higher classification confidence.

Finally, using SK, we can compute the physical-aware prototype on test set as

Pens = { ˜w1, ˜w2,..., ˜wj| ˜wj ∈SK},

˜wj =

1 |SK|

|SK| P i=1

I(yi = j)Fθ(˜x)ens

2. (15)

Exponential sliding average of prototype points.. Once the physically-aware prototypes Pens of the test set are available, we will move the prototype points Ps in the memory bank so that the model gradually adapts to the class distribution of the test data. Since the test data are reached in batches, for the t-th arrival, the prototype points P t

M in its memory bank can be updated simultaneously with the following equation

P t

M = γP t−1

M + (1 −γ)P t ens, t ≥1 P t

M = Ps, t = 0 (16)

where γ ∈[0, 1] denotes the momentum coefficient. Using Eq. 16, our model can continuously estimate P t ens based on the received data, followed by a gradual migration of the class distribution centered on the prototype points, leading to online TTA.

690

<!-- Page 6 -->

Source Target Classification Accuracy (↑)

RFF-TTA CLPS DoLos ChIns FFT IQ PSD EPS STST CWT HHT EMD

E1 D1

E1 D1 0.9630 0.9750 0.9250 0.9125 0.9141 0.9297 0.9688 0.9219 0.9375 0.9453 0.9366 0.9312 E1 D2 0.9118 0.8750 0.8625 0.8249 0.7891 0.8125 0.8203 0.7969 0.8516 0.8672 0.7656 0.7734 E1 D3 0.9521 0.7624 0.8625 0.8125 0.7266 0.8047 0.7188 0.7134 0.8359 0.7422 0.7500 0.7578 E1 D4 0.8091 0.6125 0.4875 0.7125 0.4297 0.4368 0.4844 0.4531 0.5859 0.5836 0.4688 0.5156 E1 D5 0.9123 0.7750 0.7750 0.8125 0.7656 0.7734 0.7500 0.7322 0.8125 0.8234 0.6953 0.7031

**Table 1.** Identification Accuracy of ResNet with Different Feature Representations in Single-Source Domain.

Day1 Day2 Day3 Day4

40

60

80

100

Accuracy(%)

IQ DG DPL NPC Ours

+5% -7.43%

(a)

Day2 Day3 Day4 0

20

40

60

80

100

Accuracy(%)

CLPS DoLos ChIns CLPS+ DoLos+ ChIns+

8.95 %

9.13 %

17.51 %

(b)

**Figure 5.** (a) Performance comparison of different TTA algorithms. (b) Efficiency of RFF-TTA imposed on other RFF recognition algorithms.

Classification. Finally, we mainly use the updated prototype points P t

M and Eq. 8 for classification probability calculation, p(y = j|˜x; Fθ) = exp(sim(Fθ(˜x), P tj

M)) P j∈ys exp(sim(Fθ(˜x), P tj

M))

. (17)

## Experiments

and Analysis

Dataset. To validate the effectiveness of RFF-TTA, we collected time-varying RFF datasets from the real world. We used 10 mobile phones with complex tasks as signal transmitters. Because running different applications on the phone produces different DSEs and thus time-varying RFFs, we then conducted tests at different times and locations to simulate the impact of channel effects. The RF signal from all the devices is captured using the USRP N210 software radio (SDR) with a sampling rate of 20 MS/s. 10,000 samples per day and 2,000 samples per device were used for testing. In total, we collected data for 9 days and 2 months. For more information, please refer to the Appendix.

## Experiments

Setup

Hardware Setup. The RFF-TTA algorithm is implemented by using Pytorch 1.10.0 and executed on a computer running Ubuntu 18.04.6 LTS, with Intel(R) Core(TM) i9-10900K CPU@3.70 GHz and 2 NVIDIA GeForce RTX3090 GPUs. Models’ Setup and Comparison Baselines. To ensure the fairness of the comparison, we use a uniform network architecture (ResNet-18 (He et al. 2016)) for all baseline methods. The state-of-the-art RFF recognition algorithms we compare include CLPS (Tang et al. 2024), DoLos (Xing et al. 2022), ChIns (Shen et al. 2022). In addition to this, other signal features are considered for comparison, including power spectral density (PSD), envelope’s power spectrum (EPS)(Elmaghbub and Hamdaoui 2023), shorttime Fourier transform (STST), continuous wavelet transform (CWT), Hilbert Huang transform (HHT), and empirical modal decomposition (EMD). In addition, we considered two advanced TTAs (NPC (Zhang et al. 2023) and DPC (Wang et al. 2025)) for comparison. Both algorithms are used for real-time TTA and are more similar to our scenario. Metrics. To quantitatively evaluate the RFF recognition performance, we use Accuracy (Acc) as a metrics

Acc = TP + TN TP + TN + FP + FN, (18)

where TP, TN, FP, FN denote the true-positives, truenegatives, false-positives, and false-negatives, respectively. Implementation Details. We set ∆f to 2000 MHz for CFO augmentation and to [−2π, 2π] in CPO augmentation. K in Eq. 14 is set to 5 and the parameter γ in Eq. 16 is set to 0.5. The model optimization is mainly done using the Adam optimizer with a learning rate of 0.001.

Evaluating the Generalization of RFF-TTA

Comparison of different RF fingerprint recognition algorithms. We use the data collected on the first day for model training and then test it in the same environment on the following days. Table 1 demonstrates that our RFF- TTA improves the average recognition performance by 8.7% compared to the state-of-the-art RFF recognition algorithm (CLPS). In addition, we find that RFF is slightly lower than CLPS in the test of E1 D1, while CPLS performs poorly in the later tests. This suggests that CLPS produces overfitting on the same distributed data, whereas our method mitigates the overfitting well and thus improves the generalization. Fig. 6a illustrates the prototype point adaptation results for RFF-TTA. We can see that the method in this paper can better move the prototype points with distribution offset to the target domain data. The above results show that the RFF- TTA in this paper can better cope with channel effects and DSE. Comparison of different TTA algorithms. Since the study in this paper focuses on online TTA, we mainly compare it with two more advanced online TTA methods(NPC, DPL). Figure 7a illustrates the results, and it can be seen that our RFF has better performance improvement compared to DG,

691

<!-- Page 7 -->

C1 C2 C3 C4 C5 C6 C7 C8 C9 C10

Moving

(a)

K=1 K=3 K=5 K=7 40

50

60

70

80

90

100

110

120

Accuracy(%)

Number of prototype points

Day1 Day2 Day3 Day4 Day5

(b)

0 2 4 6 8 10 12 14 16 -10

0

10

20

30

## 40 Ours-M Ours-T NPC-M NPC-T DPL-M DPL-T

Number of Test Streams

Memory(Mb)

010 20 30 40 50 60 70 80 90 100 110 120 130 140

Time Delay(ms)

(c)

**Figure 6.** (a) The t-SNE diagram of the updated prototype point is passed through the RFF-TTA, ▽and ✩denote the old prototype and the adapted prototype, respectively. (b) Sensitivity analysis of the sample selection parameter K. (c) Running latency and memory consumption of different TTA algorithms.

M1 M2 M3 M4 Day6 Day7 Day8 Day9 - - - - 0.8101 0.7698 0.6010 0.6421 ✓ - - - 0.9153 0.8762 0.8257 0.8684 ✓ ✓ - - 0.9195 0.8952 0.8563 0.8934 ✓ ✓ ✓ - 0.9512 0.9173 0.8624 0.8944 ✓ ✓ ✓ ✓ 0.9674 0.9426 0.8878 0.9355

**Table 2.** Comparing the recognition efficiency of different training modules: M1 (stable features), M2 (CFO augmentation), M3 (CPO augmentation), and M4 (transient features).

Ours Gaussian noise

Channel

Effect Scaling Amplitude distortion

Time Warp

Day1 0.9630 0.9695 0.9673 0.9517 0.9599 0.9492 Day2 0.9118 0.8465 0.7691 0.8414 0.8444 0.8398 Day3 0.9475 0.8578 0.8200 0.8346 0.8127 0.8330

**Table 3.** Performance comparison of different time series augmentation methods.

where DG denotes our channel-invariant fingerprint method, and IQ denotes the raw IQ signal. The performance of DPL as well as NPC is not stable due to their inability to adapt to the RFF data characteristics and find the exact direction of prototype update. Effectiveness of the TTA algorithm for other RFF extraction methods. Fig. 5b shows the efficiency of the TTA strategy proposed in this paper imposed on other RFF algorithms. It can be seen that the RFF-TTA can improve the recognition performance of other algorithms by an average magnitude of about 8%. The above results demonstrate the applicability of the RFF-TTA, which can be effectively embedded into other methods and improve their performance upper bound.

Ablation Study

## Analysis

of the validity of data augmentation. Table 2 demonstrates the performance differences resulting from different data augmentation (Iwana and Uchida 2021) and

RFF features. The channel-invariant fingerprinting adopted in this paper can eliminate the channel effect, thereby improving performance. In addition, the CFO augmentation and CPO augmentation used in this paper can increase data diversity and also improve the model’s generalization performance, thus mitigating the effect of DSE. Additionally, we compare various time series augmentation methods. As shown in Table 3, it can be seen that our data augmentation achieves the best results, indicating that our approach is more aligned with the DSE problem explored in this paper.

Sensitivity of the sample selection parameter K. Eq. 14 requires the selection of Top-K samples for target adaptation. Figure 7b shows the results for different values of K. It can be seen that a larger value of K is not better. Choosing a smaller K value indicates a higher confidence in the sample.

Operational efficiency of different TTA algorithms.. Fig. 6c illustrates the operational efficiency of different TTA algorithms. We can see that NPC has the highest time delay and memory consumption because it needs to keep adding features to the memory bank. RFF-TTA has the same memory consumption as DPL, and the prototype memory bank does not grow because only prototype updates are implemented instead of adding new prototype points. However, RFF computational latency is higher than DPL, but still within acceptable limits. In contrast. Finally, in terms of performance, as shown in Fig. 5a, ours is the best and DPL the worst.

## Conclusion

In this paper, we propose a physical impairment-based augmented method and a physical information-aware prototypebased TTA method to solve the DG problem in time-varying RFF. We first propose random CFOs and CPOs to augment the data. Then the combination of transient and steady-state RFF is used to eliminate the channel effect. Finally, we propose a physical information-aware prototype ensemble approach to implement TTA. Our approach has achieved initial results, but extensive application testing in larger IoT scenarios is needed in the future.

692

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Natural Science Foundation of China under Grant 62472387, 62576310 the Zhejiang Provincial Science Fund for Distinguished Young Scholars under Grant LR24F020004, the Zhejiang Provincial Natural Science Foundation of Major Program (Youth Original Project) under Grant LDQ24F020001, LZ25F020007, Zhejiang Province Key R&D Leading Goose Project 2025C02263, and China Postdoctoral Science Foundation under Grant 2025M771517.

## References

Brik, V.; Banerjee, S.; Gruteser, M.; and Oh, S. 2008. Wireless device identification with radiometric signatures. In Proceedings of the 14th ACM international conference on Mobile computing and networking, 116–127. Cai, Z.; Lu, G.; Wang, Y.; Gui, G.; and Sha, J. 2025. Robust Cross-Domain UAV RFFI Method Using Domain-Invariant Adversarial Learning and Manifold Regularization. IEEE Transactions on Cognitive Communications and Networking. Elmaghbub, A.; and Hamdaoui, B. 2023. A Needle in A Haystack: Distinguishable Deep Neural Network Features for Domain-Agnostic Device Fingerprinting. In 2023 IEEE Conference on Communications and Network Security (CNS), 1–9. IEEE. Gong, P.; Ragab, M.; Wu, M.; Chen, Z.; Su, Y.; Li, X.; and Zhang, D. 2025. Augmented contrastive clustering with uncertainty-aware prototyping for time series test time adaptation. arXiv preprint arXiv:2501.01472. Gu, X.; Wu, W.; Song, A.; Yang, M.; Ling, Z.; and Luo, J. 2024. RF-TESI: Radio Frequency Fingerprint-based Smartphone Identification under Temperature Variation. ACM Transactions on Sensor Networks, 20(2): 1–21. He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, 770–778. Huang, Y.; et al. 2017. Radio frequency fingerprint extraction of radio emitter based on I/Q imbalance. Procedia computer science, 107: 472–477. Iwana, B. K.; and Uchida, S. 2021. An empirical survey of data augmentation for time series classification with neural networks. Plos one, 16(7): e0254841. Jana, S.; and Kasera, S. K. 2008. On fast and accurate detection of unauthorized wireless access points using clock skews. In Proceedings of the 14th ACM international conference on Mobile computing and networking, 104–115. Jiang, Q.; Ye, C.; Wei, D.; Xue, Y.; Jiang, J.; and Wang, Z. 2024. Discover Your Neighbors: Advanced Stable Test-Time Adaptation in Dynamic World. arXiv preprint arXiv:2406.05413. Li, Y.; Lin, H.; Lv, J.; Gao, Y.; and Dong, W. 2024. BLE Location Tracking Attacks by Exploiting Frequency Synthesizer Imperfection. In IEEE INFOCOM 2024-IEEE Conference on Computer Communications.

Liu, P.; Yang, P.; Song, W.-Z.; Yan, Y.; and Li, X.-Y. 2019. Real-time identification of rogue WiFi connections using environment-independent physical features. In IEEE IN- FOCOM 2019-IEEE Conference on Computer Communications, 190–198. IEEE. Polak, A. C.; and Goeckel, D. L. 2015. Identification of wireless devices of users who actively fake their RF fingerprints with artificial data distortion. IEEE Transactions on Wireless Communications, 14(11): 5889–5899. Rajendran, S.; and Sun, Z. 2022. RF impairment modelbased IoT physical-layer identification for enhanced domain generalization. IEEE Transactions on Information Forensics and Security, 17: 1285–1299. Rajendran, S.; Sun, Z.; Lin, F.; and Ren, K. 2020. Injecting reliable radio frequency fingerprints using metasurface for the Internet of Things. IEEE Transactions on Information Forensics and Security, 16: 1896–1911. Restuccia, F.; D’Oro, S.; Al-Shawabka, A.; Belgiovine, M.; Angioloni, L.; Ioannidis, S.; Chowdhury, K.; and Melodia, T. 2019. DeepRadioID: Real-time channel-resilient optimization of deep learning-based radio fingerprinting algorithms. In Proceedings of the Twentieth ACM International Symposium on Mobile Ad Hoc Networking and Computing, 51–60. Riyaz, S.; Sankhe, K.; Ioannidis, S.; and Chowdhury, K. 2018. Deep learning convolutional neural networks for radio identification. IEEE Communications Magazine, 56(9): 146–152. Shen, G.; Zhang, J.; Marshall, A.; and Cavallaro, J. R. 2022. Towards scalable and channel-robust radio frequency fingerprint identification for LoRa. IEEE Transactions on Information Forensics and Security, 17: 774–787. Shen, G.; Zhang, J.; Marshall, A.; Peng, L.; and Wang, X. 2021. Radio frequency fingerprint identification for LoRa using spectrogram and CNN. In IEEE INFOCOM 2021-IEEE Conference on Computer Communications, 1– 10. IEEE. Tang, P.; Xu, Y.; Ding, G.; Jiao, Y.; Song, Y.; and Wei, G. 2024. Causal Learning for Robust Specific Emitter Identification over Unknown Channel Statistics. IEEE Transactions on Information Forensics and Security. Wang, G.; Ding, C.; Tan, W.; and Tan, M. 2025. Decoupled Prototype Learning for Reliable Test-Time Adaptation. IEEE Transactions on Multimedia. Xing, Y.; Hu, A.; Zhang, J.; Peng, L.; and Wang, X. 2022. Design of a channel robust radio frequency fingerprint identification scheme. IEEE Internet of Things Journal, 10(8): 6946–6959. Zhang, M.; Tang, P.; Wei, G.; Ni, X.; Ding, G.; and Wang, H. 2024. Open set domain adaptation for automatic modulation classification in dynamic communication environments. IEEE Transactions on Cognitive Communications and Networking. Zhang, Y.; Wang, X.; Jin, K.; Yuan, K.; Zhang, Z.; Wang, L.; Jin, R.; and Tan, T. 2023. Adanpc: Exploring non-parametric classifier for test-time adaptation. In International conference on machine learning, 41647–41676. PMLR.

693

<!-- Page 9 -->

Zheng, T.; Sun, Z.; and Ren, K. 2019. FID: Function modeling-based data-independent and channel-robust physical-layer identification. In IEEE INFOCOM 2019- IEEE Conference on Computer Communications, 199–207. IEEE.

694
