---
title: "Towards Distance-Invariant Radio Frequency Fingerprinting via Augmented Unsupervised Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37005
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37005/40967
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Towards Distance-Invariant Radio Frequency Fingerprinting via Augmented Unsupervised Learning

<!-- Page 1 -->

Towards Distance-Invariant Radio Frequency Fingerprinting via Augmented Unsupervised Learning

Shiyue Huang, Yuchen Su, Hongbo Liu*, Zikang Ding, Xuewan He, Yanzhi Ren, Haitao Jia

University of Electronic Science and Technology of China sy.huang@std.uestc.edu.cn, hongbo.liu@uestc.edu.cn

## Abstract

Radio Frequency Fingerprinting (RFF) exploits inherent hardware-level imperfections of wireless transmitters as unclonable identifiers for device identification. These unique signatures, concealed in transmitted signals, inevitably experience complex distortions during wireless propagation (i.e., coupled with ambient noise and channel fading), making it extremely challenging for reliable extraction. Despite substantial research efforts dedicated to advancing effective fingerprint extraction techniques, current approaches still struggle in handling fingerprint robustness under distance variations, leading to severe SNR fluctuations and complex multipath effects. To address this gap, we propose the first unsupervised framework for distance-invariant radio frequency fingerprinting, eliminating dependence on labeled target domain data. Specifically, we first preprocess raw RF samples by confining them within a specified variation range and filtering noisy high-frequency components while avoiding aliasing. For source domain data, we then propose a set of physics-inspired data augmentation techniques designed to emulate realistic wireless signal propagation effects. Building on this, we introduce a dual alignment contrastive learning method to explicitly decouple identity-discriminative features, ensuring the model focuses on device-specific traits. Furthermore, we incorporate a pseudo-labeling-based domain adaptation module to refine the model for the unlabeled target domain, enhancing its generalization to unseen distances. Extensive experiments on public datasets show that our method achieves the identification accuracy outperforming state-ofthe-art approaches by 40%, while maintaining computational efficiency suitable for edge deployment.

## Introduction

The proliferation of Internet of Things (IoT) devices in critical infrastructure and daily life has intensified the demand for lightweight, secure identification mechanisms. Traditional software-based identifiers (e.g., MAC addresses) are vulnerable to spoofing, while public-key cryptography (PKC) imposes severe power and computational burdens, making it incompatible for resource-constrained IoT devices. As a promising non-cryptographic alternative, radio frequency fingerprinting (RFF) leverages unique, unclonable hardware impairments in RF transceivers as physical

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

d0

Rx Tx

Constellation

Diagram d0 d

I

Q

I

Q Rx T x ‘

**Figure 1.** Illustration of distance-invariant RFF.

identifiers (Zhang et al. 2025), as shown in Figure 1. These hardware-imprinted signatures enable packet-level identification resistant to spoofing, making RFF ideal for highsecurity scenarios. Furthermore, RFF relies on hardwareintrinsic properties, eliminating the need for upper-layer protocols or additional computational overhead. Recognizing these advantages, the Defense Advanced Research Projects Agency (DARPA) has prioritized RFF research through its RF Machine Learning Systems (RFMLS) program (DARPA 2017), driving extensive studies on RFF for device identification.

Given above aforementioned merits, a critical limitation still persists: most RFF methods exhibit limited generalization under spatially variant channel conditions. Specifically, existing works (Wu et al. 2021; Yao et al. 2025; Zhang et al. 2025) have successfully mined discriminative features for stable-channel identification, but they often fails in dynamic channel. Domain adaptation techniques (Zhang et al. 2022; Li et al. 2022; Yin et al. 2023), although succeeded in dealing with temporal variations (e.g., cross-day identification), also struggle with spatial generalization. This challenge stems from two key factors: as the distance between devices increases, the signal-to-noise ratio (SNR) decreases under fixed transmission power, causing subtle fingerprint information to be easily masked by noise; meanwhile, the complex multipath effect caused by distance changes couples with the RF signal, further complicating fingerprint recognition. Alternative approaches have turned to few-shot learning (Zhao, Wang, and Mao 2024; Sun et al. 2025) to tackle domain shifts and scalability across different distances. However, these methods usually require labeled

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

426

<!-- Page 2 -->

training samples from the target domain. Collecting and annotating such data for each new separation distance is both labor-intensive and time-consuming, severely limiting their practical deployment. Thus, enabling distance-invariant RFF without relying on labeled target-domain data remains an open and critical challenge.

In this paper, we present the first distance-invariant RFF identification framework that eliminates reliance on labeled target-distance data. To obtain robust fingerprint representations, we develop several physics-inspired data augmentation strategies. Leveraging the augmented data, we propose a dual alignment framework that explicitly decouples identity-discriminative features, thereby extracting distanceinvariant fingerprints. Additionally, we propose a progressive pseudo-labeling adaptation framework that iteratively refines model parameters using high-confidence predictions on unlabeled target samples. This strategy bridges domain gaps without requiring manual annotation, achieving stateof-the-art (SOTA) performance over existing methods. Our main contributions are summarized as follows:

1) To the best of our knowledge, this is the first work enabling distance-invariant RFF that generalizes to unseen distances without labeled target samples, addressing a critical gap in practical deployment. 2) We propose physics-inspired data augmentation strategies that explicitly model the wireless signal propagation effects, effectively expanding the source domain to cover diverse wireless channel conditions. 3) We design a dual alignment and progressive adaptation framework that jointly learns invariant representations through class-level and prototype-level alignments and progressively adapts to unlabeled target domains. 4) Extensive experiments on public datasets show that our framework achieves encouraging identification accuracy on 16 devices across different distances from the source domain, outperforming SOTA methods by 40%.

## Related Work

Deep learning-based RFF. Deep learning has become a dominant paradigm in RF fingerprinting (RFF) due to its strong capability of automatic feature extraction from raw RF signals, with a variety of architectures validated for performance improvement. For instance, convolutional neural networks (CNNs) (Wu et al. 2021; Sankhe et al. 2019; Al- Shawabka et al. 2020) have been widely adopted to capture local discriminative patterns in signal representations. Recurrent models such as LSTM (Shen et al. 2021) and GRU (Shen et al. 2023) later emerged to model temporal dependencies in sequential IQ samples. More recently, Transformer-based models (Xu and Xu 2021; Han et al. 2025) and state-space alternatives like Mamba (Yao et al. 2025) have been proposed to handle long-range correlations in signals, while KAN networks (Chen et al. 2025) offer more interpretable fingerprint extraction. Despite these advancements in improving identification accuracy under fixed experimental settings (e.g., static locations and stable channels), most deep learning-based methods still face critical generalization issues across spatially variant channel conditions. This limitation highlights the need for more robust frameworks that can decouple device-specific fingerprints from distance sensitive channel distortions.

Contrative Learning for RFF. Contrastive learning (CL), as a powerful unsupervised representation learning tool, has shown great potential in RFF identification. For instance, Zha et al. (Zha et al. 2023) treat receiver-induced distribution shifts as a data augmentation strategy, leveraging SimSiam-based contrastive pre-training to extract receiveragnostic features and alleviate cross-receiver performance degradation. Wang et al. (Wang et al. 2024) further propose a CL-based heterogeneous feature fusion method, yielding more discriminative RFF representations and improving open-set classification performance. Despite these advances, critical challenges remain. Most CL approaches for RFF assume same place deployment, making them vulnerable to real-world spatial variations. While recent work explores residual contrastive learning between pre- and postequalization signals to mitigate channel impacts (Pan et al. 2025), their validation is confined to simulations, lacking practical verification in real-world scenarios.

Domain Adaptation for RFF. Domain adaptation (DA) techniques (Li et al. 2024) have been explored to address distribution shifts in RFF authentication, primarily focusing on cross-modulation or cross-day scenarios. Yin et al. (Yin et al. 2023) proposed a few-shot DA framework for modulation-agnostic emitter identification, while Zhang et al. (Zhang et al. 2022) leveraged domain adversarial adaptation by contrasting real signals with demodulated ideal signals to improve robustness under variable modulations. In cross-day scenarios, RadioNet (Li et al. 2022) leveraged adversarial adaptation and a device rank metric to mitigate temporal drift. However, distance-invariant RFF adaptation remains under-explored. Most existing DA methods assume static device-receiver distances, yet spatial variations introduce SNR degradation and multipath distortions that obscure intrinsic RFF patterns (Wan et al. 2024). Wan et al. proposed the only cross-distance approach (VC-SEI) using semi-supervised DA, but it requires partial labeled targetdomain data—a costly constraint for IoT deployments. Unlike these works, our method achieves fully unsupervised cross-distance adaptation without target-domain labels.

## Methodology

Problem Definition

Assume we have a dataset from source domain Ds = {(xs i, ys i)}Ns i=1, where xs i ∈X ⊆CT represents complexvalued RF samples acquired by a wireless receiver(Rx) with a fixed distance from the transmitter(Tx), and ys i ∈ {1, 2,..., K} corresponds the device identity labels spanning K distinct classes. For the target domain, we consider an unlabeled dataset Dt = {xt j}Nt j=1 consists of Nt RF samples. These samples are collected at transceiver separation distances distinct from those in the source domain, which imply different multipath effects and SNR characteristics from the source domain. Our objective is to learn a feature extractor fe: X →Rd that maps raw RF sam-

427

<!-- Page 3 -->

Initialize

Encoder Classifier

Augment

Lclass Lproto

LCE

...

Update Pseudo-labels

Classifier

...

Source Samples (Labeled)

d0

Rx Tx

LPL

LIM

Target Samples (Unlabeled)

>>>> d0 d

Rx Tx T x

Preprocess

Preprocess y

‘

**Figure 2.** Framework of our method.

ples to d-dimensional feature embeddings, and a classifier fc: Rd →RK that predicts device labels from these embeddings. The feature extractor fe captures spatially invariant, device-specific physical-layer features from Ds, enabling the composite mapping fc◦fe to achieve high target-domain (Dt) accuracy without requiring labeled Dt samples.

## Model

Overview As shown in Figure 2, our framework comprises three stages: preprocessing, contrastive learning on the source domain, and unsupervised domain adaptation on the target domain. First, preprocessing aims to mitigate domain shifts of raw input RF samples, establishing a consistent input space. Given the preprocessed RF samples, contrastive learning applies dual alignment to learn distance-invariant features, thereby constructing the source model. Finally, target domain adaptation facilitates adaptation to the unlabeled data in target domain with the feature encoder initialized from the source model.

Preprocessing To reduce the impact of noise and multipath effects over wireless channel, we design the following preprocessing pipeline:

Normalization and Min-Max Scaling. Wireless signals experience different attenuation as the distance between transceivers varies, causing the amplitude of RF samples usually spanning over a large range. To eliminate such impact of distance on the RF samples for better domain adaption, we confine the raw RF samples through normalization and min-max scaling. First, we normalize the sample using the root-mean-square (RMS) value:

ˆxi = xi q

1 T

PT t=1 |xi[t]|2

, ∀xi ∈X, (1)

where T denotes the length of each complex-valued sample xi ∈CT, and then we apply min-max scaling to bound the sample within a standardized dynamic range:

˜xi[t] = ˆxi[t] −min(ˆxi) max(ˆxi) −min(ˆxi), ∀t ∈{1,..., T}. (2)

Resampling. High-frequency components of RF fingerprints easily couple with interference and multipath effects on wireless channel, obscuring genuine feature extraction, while the low frequency components are more resilient to the external factors. Thus, we next resample the signal ˜xi at a lower sampling rate to restrict the RF fingerprints within low frequency band. In the meanwhile, it also dimensionally compresses the input data, thereby expediting subsequent feature extraction.

Source Model with Contrastive Alignment To learn distance-invariant features from the source domain for robust fingerprinting, we design a dual contrastive learning framework to build the source model, combining both class-level and prototype-level alignment.

Backbone. Inspired by the MCNN (Cui, Chen, and Chen 2016), we propose a Multi-Scale Attention Network (MSAN) as the backbone network, specifically tailored for RF fingerprint extraction. As shown in Figure 3, the MSAN architecture consists of six cascaded encoder modules. Each module integrates three components: multi-scale convolutional layers to capture device-specific fingerprint across different time-frequency resolutions, a channel-wise attention module to suppress noise, and ReLU activation. To preserve gradient flow and mitigate vanishing gradients in deep stacks, we implement identity mappings that directly connect each block’s output to subsequent layers. Detailed specifications and comparative experiments refer to the Appendix A and C.

Data Augmentation. Contrastive learning relies on maximizing agreement between augmented views of the same sample while minimizing similarity with negative samples, making the design of domain-specific augmentations

428

![Figure extracted from page 3](2026-AAAI-towards-distance-invariant-radio-frequency-fingerprinting-via-augmented-unsuperv/page-003-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-towards-distance-invariant-radio-frequency-fingerprinting-via-augmented-unsuperv/page-003-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

AvgPool

3x1 Conv

12x1 Conv

6x1 Conv

1x1 Conv

Channel Attention Module

1x1 conv

Encoder

Encoder

......

Avg Pool

Learner

Encoder

Multi-conv

Relu

Channel Attention Module x5

Re

Im

**Figure 3.** The structure of backbone.

critical for effective representation learning (Grill et al. 2020; Demirel and Holz 2023). To augment input RF samples, we propose a physics-inspired augmentation strategy through simulating realistic wireless channel effects with six transformations: Signal scaling applies random normaldistributed factors N(1, 0.12) to mimic wireless signal fluctuations caused by different path loss; Permutation (Liu and Chen 2024) partitions signals into multiple segments and reorders them randomly to emulate multipath effect; Window slicing extracts partial of the signals and expands it with linear interpolation, simulating the channel fading; Time warping (Zhang et al. 2024) introduces nonlinear distortions via random warping factors to replicate time-varying delays; Magnitude warping (Um et al. 2017) applies random scaling at knot points with cubic spline interpolation, modeling amplitude-varying channel fading; and Window warping (Rashid and Louis 2019) randomly select the segment of RF sample and stretch it through the linear interpolation, capturing local signal distortions. These augmentations systematically encode physical-layer invariances into the representation learning process, enabling the model to disentangle device-specific RF fingerprint from spatially variant propagation artifacts during contrastive optimization. During the training phase, we randomly sample and compose four distinct augmentations from the available set for each batch, denoted as A(·).

Discrimination Loss. To achieve accurate device discrimination, we leverage cross entropy loss to directly optimize the model’s classification performance. For a batch of source samples {(xs b, ys b)}B b=1, after data augmentation A(xs b), the backbone fe(·) generates feature embedding zs b. Classifier fc then projects zs b to produce logits ˆys b = fc(zs b) over K device classes. The cross entropy loss is computed as:

LCE = −1

B

B X b=1

K X k=1

1(ys b = k) log e(ˆys b)k PK j=1 e(ˆys b)j

!

. (3)

Here, 1(ys b = k) is an indicator function for the true class label of sample b, and (ˆys b)k denotes the k-th element of ˆys b. LCE ensures the model learns maximally discriminative device-specific features.

Class-level Alignment Loss. Given LCE, device-specific features may still be entangled with the channel variations in RF samples caused by the distance change. To resolve this problem, we introduce a supervised N-pairs contrastive loss (Khosla et al. 2020) that explicitly enforces all transformed views of the RF fingerprint from the same device to converge toward a unified representation. For a batch of source samples {(xb, yb)}B b=1 and their augmented embeddings zb = fe(A(xb)), the class-level alignment loss is defined as:

Lclass = −1

B

B X b=1

1 |Pb|

X p∈Pb log exp(z⊤ b · zp/τ) P a∈Ab exp(z⊤ b · za/τ), (4)

where Ab ≡I \ {b}, I ≡{1,..., B} denotes the index set of all augmented samples; Pb ≡{p ∈Ab: ˜yp = ˜yb} is the set of positive samples that belong to the same device as zb, and |Pb| is the cardinality of this set; τ is a temperature parameter controlling feature distribution concentration, and · represents cosine similarity. Lclass promotes the clustering of RFF features from the same device, even when distorted by distance-related factors.

Prototype-level Alignment Loss. To further refine feature distributions for each device, we introduce prototype-level alignment, which anchors the features to class-specific references inspired by (Snell, Swersky, and Zemel 2017). This mechanism tightly clusters all features of a particular device around its prototype, enhancing both intra-class consistency and inter-class discriminability. Formally, we define a set of trainable prototypes U = {u1,..., uK} ∈RK×d, where K is the number of devices and d matches the embedding dimension of the feature extractor fe. For an augmented instance feature zb, we compute its prototype assignment distribution via:

p(k)

b = exp u⊤ k · zb/τ

PK j=1 exp u⊤ j · zb/τ

, ∀k ∈{1,..., K}, (5)

where τ is the temperature parameter and · denotes cosine similarity. To enforce consistency in the prototype space, we treat each zb as an anchor and construct positive pairs (zb, zp), where zp is another augmented view of the same original sample as zb. In each training batch, the features from the same sample with different augmentations are split into labeled and unlabeled subsets. For a labeled anchor, its positive counterpart is randomly selected from the same device class; for an unlabeled anchor, its positive counterpart is the nearest neighbor in the embedding space. To ensure positive pairs exhibit consistent prototype association patterns, we define the prototype-level alignment loss as:

Lproto = − 1 |Ppos|

X i∈Ppos log (pi · p′ i), (6)

where pi and p′ i are the prototype assignment distributions of the anchor zb and its positive instance zp, respectively, and Ppos denotes all positive pairs in the batch. Optimizing Lproto further refines feature representations and effectively suppresses residual distance-dependent biases.

Overall Objective in Source Domain. The complete objective function for source domain is formulated as:

Lsource = LCE + λ1Lclass + λ2Lproto, (7)

429

<!-- Page 5 -->

where λ1 and λ2 are hyperparameters used to balance the class and prototype loss, respectively.

Target Domain Adaptation While the source-domain model achieves initial feature discrimination, its identification accuracy may still deteriorate when transceivers are separated at other distances from each other owing to inherent domain shifts. To address this issue, we aim to further adapt the model to the target domain where the separation distances between transceivers are different from those in source domain. Notably, in resourceconstrained IoT settings, the devices are incapable in accessing the RF samples in source domain, making source-datadependent methods (e.g., MMD (Yan et al. 2017) and adversarial alignment (Long et al. 2018)) infeasible. In the following, we elaborate on the target domain adaptation framework, which enables on-device adaptation without accessing source domain data.

Self-Supervised Pseudo-Labeling. Since no ground-truth labels are available for the target domain, we propose a dynamic cluster-based pseudo-labeling strategy to generate reliable supervision signals. Unlike conventional methods (Hu et al. 2021) that directly use source-domain classifiers for label assignment (suffering from noise induced by domain shift), our approach leverages target data’s intrinsic structure to refine pseudo-labels. Given unlabeled target data Dt = {xt j}Nt j=1, we initialize the adaptation process using the feature extractor fe and the frozen classifier fc from the source model. For each target sample xt j, its initial classification output is ˆyt j = fc(fe(xt j)). To reduce domain shift noise, we compute initial class prototypes µ(0)

k weighted by the confidence scores from the source classifier:

µ(0)

k =

P xt j∈Dt δk(Softmax(ˆyt j)) · fe(xt j) P xt j∈Dt δk(Softmax(ˆyt j)), (8)

where δk(·) takes the kth logit, and µ(0)

k denotes the initial prototype for class k. Then each target sample is assigned to the class corresponding to its closest prototype, generating initial pseudo-labels:

ˆyt = arg min k cos(fe(xt), µ(0)

k). (9)

To further strengthen the class structure in the target domain, we refine prototypes using these hard pseudo-labels and reassign labels with updated prototypes:

µ(1)

k =

P xt j∈Dt 1(ˆyt = k)fe(xt j) P xt j∈Dt 1(ˆyt = k), (10)

ˆyt = arg min k cos(fe(xt), µ(1)

k).

Here, µ(1)

k is the refined prototype for class k. The final pseudo-labels ˆyt are used to supervise the training of a target-domain classifier ft (initialized from fc) through a cross-entropy loss:

LP L = −Ext∈Dt

K X k=1

1(ˆyt = k) log δk(ft(xt)). (11)

Information Maximization. Relying solely on pseudolabeling may lead to error propagation, as the quality of pseudo-labels is inherently limited. Thus, we introduce an information maximization (IM) loss (Hu et al. 2017) that simultaneously maximizes per-sample confidence and class diversity. Let y = Softmax(ˆyt j), the IM loss is defined as:

LIM(y) = Lent(y) −Ldiv(y), (12)

where Lent(y) = −Exi∈Xt h C X c=1 δc(y) log δc(y)

i

,

Ldiv(y) = −

K X k=1

¯pk log ¯pk, where ¯pk = Ext∈Dt[δk(y)] is the average probability of class k across all target samples. Individual certainty Lent ensures that each sample is assigned to a single class with high confidence, and global diversity Ldiv prevents mode collapse, where the classifier overemphasizes a subset of classes and ignores others.

Target Domain Overall Objective. To summarize, building on the source model fs = fc ◦fe and the pseudo-labels generated above, the target-domain adaptation optimizes the target classifier ft using the following composite objective:

Ltarget = γ · LP L + LIM, (13)

where γ > 0 is a hyperparameter that controls the balance between the loss components LP L and LIM.

## Experiments

## Experimental Setup

Datasets. We evaluate the distance robustness of our RFF model on two benchmark datasets: (1) ORACLE (Sankhe et al. 2019): This dataset contains raw IQ samples captured using 16 USRP X310 Tx and a USRP B210 Rx, with Tx–Rx distances of 2–62 feet (6ft intervals). Owing to significant frame decoding failure rates at the communication range 56/62ft (Zhao, Wang, and Mao 2024), we retain 9 valid distance (2–50 ft) for validation across its two subsets, ORA- CLE.1 and ORACLE.2, which were collected at different time periods. (2) LoRa (Elmaghbub and Hamdaoui 2021): A LoRaWAN-specific RFF dataset collected from 5 identical Pycom IoT devices (Tx) and a USRP B210 Rx. Samples were captured by the same receiver at four distances (5m, 10m, 15m, and 20m) across different transmitters. To further evaluate the temporal robustness, we include two time-variant datasets: (3) WiSig (Hanna, Karunaratne, and Cabric 2022): Comprising wireless samples from 6 COTS Wi-Fi cards captured by the same USRP receiver over four days, with a fixed spatial setup. (4) CORES (Hanna, Karunaratne, and Cabric 2020): Samples from 6 Wi-Fi cards deployed in a static grid at the Orbit Testbed over five days.

Baselines. We compare against two baseline categories. For cross-domain RFF tasks, we choose three representative models: OpenRFI(Han et al. 2025), VC-SEI(Wan et al. 2024), and the modified prototypical network (MPTN) from

430

<!-- Page 6 -->

Dataset Avg.

## Model

Ours OpenRFI ConvTran VC-SEI MPTN

S T T(Only S) S T S T S T S T

ORACLE.1 1S→8T 95.2 65.0 50.9 31.3 25.1 88.3 17.6 93.8 23.1 94.1 22.1

2S→7T 95.9 81.0 70.6 46.8 36.7 91.7 56.7 93.8 41.7 95.7 55.9

ORACLE.2 1S→8T 95.3 66.0 53.9 29.7 24.6 83.0 20.7 94.6 25.0 93.8 24.8

2S→7T 95.9 79.0 72.1 47.5 36.0 93.5 56.2 94.8 45.8 95.8 47.8

LoRa 1S→3T 99.3 93.4 74.0 32.0 26.7 59.3 41.1 94.3 43.0 93.8 76.0

**Table 1.** Distance robustness comparison of RFF models.

2 8 14 20 26 32 38 44 50 Target Distance (ft)

2

8

14

20

26

32

38

44

50

Source Distance (ft)

100

70

52

90

57

37

19

14

23

91

99

59

91

69

38

25

22

26

83

78

90

88

72

47

31

24

31

92

87

65

97

80

45

28

25

26

77

62

68

81

94

48

30

29

30

61

53

59

68

71

95

43

48

50

43

25

44

42

66

37

95

51

38

45

30

47

48

59

53

42

92

54

55

30

41

55

54

45

45

50

95

(a) Source-only training.

2 8 14 20 26 32 38 44 50 Target Distance (ft)

100

92

52

90

57

46

43

64

57

95

99

74

96

69

58

40

72

61

84

89

90

91

76

57

49

63

67

93

92

65

97

80

57

51

66

71

84

82

69

89

94

61

53

74

66

71

64

66

81

71

95

50

48

60

46

52

58

66

69

51

95

62

41

49

59

47

64

60

53

49

92

58

63

67

51

70

67

63

45

61

95

(b) With target adaptation.

**Figure 4.** Distance robustness confusion matrices.

(Zhao, Wang, and Mao 2024). Additionally, we include ConvTran (Foumani et al. 2024), a well-known model in time series classification. We adopt the same preprocessing method as used in our model for the fairness of comparison.

## Evaluation

Metrics. In line with prior research in the same field, we adopt identification accuracy as the primary metric, defined as the percentage of device instances correctly classified.

Main Results Overall Performance. To evaluate the distance robustness, we conducted experiments using the ORACLE.1 dataset, where models were trained on a single source domain and test across all other target domains where the samples are captured at different distances from that in source domain. Figure 4 presents the confusion matrices before and after applying domain adaptation, with the vertical axis representing source domains and the horizontal axis representing target domains. Diagonal entries thus reflect sourcedomain accuracy, while off-diagonal entries indicate crossdomain performance. As shown in Figure 4a, even when trained solely on source-domain data, the model achieves an average accuracy of 50.9% across all source-to-target domain transfers (mean of off-diagonal entries). After applying target-domain adaptation, as shown in Figure 4b, overall performance improves significantly: cross-domain accuracy increases by an average of 14.1%, reaching 65% overall. Additionally, the matrices reveal that models trained on the source domain captured at close distance exhibit stronger

## Model

Dataset ORACLE LoRa WiSig CORES

Domains 2 5 4 5

Ours S/T 95/86 98/83 99/88 92/82

OpenRFI S/T 28/19 80/71 99/77 91/68

ConvTran S/T 95/36 72/58 99/74 90/66

VC-SEI S/T 90/34 92/49 99/84 90/79

MPTN S/T 94/24 91/70 98/75 99/72

**Table 2.** Temporal robustness for RFF models.

generalization to far-distance scenarios: the average accuracy of off-diagonal entries in the upper triangle (close-to-far distance transfers) reaches 67%. This phenomenon attributes to higher SNR of short-range wireless transmissions, where fingerprint information is less perturbed by noise and thus more reliably extracted. We also note that performance is relatively lower in the 32ft and 38ft rows, which likely stems from more complex multipath effects, increasing the difficulty of fingerprint extraction. More results can be found in the Appendix C.

Comparison Study. To benchmark the distance robustness, we compare our method against four SOTA RFF approaches across diverse experimental setups, as summarized in Table 1. The notation nS→mT denotes training on n source domains and testing on m target domains (e.g., 1S→8T: average accuracy training on any single source domain and testing across other eight targets; 2S→7T: training on the high-SNR 2ft source plus one additional source against seven targets). Across all setups, our methods consistently outperform competitors in both sourcedomain (S) and target-domain (T) accuracy. Specifically, our model trained solely on source-domain data (T(Only S)) already achieves SOTA cross-domain accuracy of 50.9%, validating effective decoupling of fingerprint features from channel variations. Using data from the 2ft and another source domain, target-domain accuracy further improves by 20%, with the 2S→7T setup reaching an average accuracy of 70.6%, demonstrating the benefit of leveraging multiple source domains. In contrast, VC-SEI and MPTN exhibit strong source performance but fail to transfer to targets, as they lack explicit mechanisms to decouple devicespecific features from domain-specific noise. While Open- RFI shows moderate cross-distance capability, its overall ac-

431

![Figure extracted from page 6](2026-AAAI-towards-distance-invariant-radio-frequency-fingerprinting-via-augmented-unsuperv/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-towards-distance-invariant-radio-frequency-fingerprinting-via-augmented-unsuperv/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Method

ORACLE.1 (Source Distance: 2ft)

P Augment Loss Target Distances 0 1 2 3 4 5 s c i 8ft 14ft 20ft 26ft 32ft 38ft 44ft 50ft Avg 8.5 3.4 0 8.1 0 15.9 6.3 1.7 5.5 ✓✓✓✓✓✓✓ 17.8 20.2 19.1 17.4 18.3 16 13.1 12.8 16.8 ✓✓✓✓✓✓✓✓✓18.3 23.1 18.3 17.5 17.9 14.8 15.4 12 17.2 ✓ 33.9 41.3 40 23.9 26.4 21.6 22.8 21.8 29.0 ✓✓ ✓ 52.4 59.5 50 53.3 42.3 33.2 37.5 41 46.2 ✓ ✓ ✓ 40.7 42.6 47.8 41.7 28.3 24.3 25.9 28 34.9 ✓ ✓ ✓ 42.6 51.1 40.2 51.6 35.8 35 27.3 27.8 38.9 ✓ ✓ ✓ 57.9 48.4 58.8 42.6 25.3 11.4 10.7 13.5 33.6 ✓ ✓ ✓ 65.4 49.2 59.5 34.7 31.7 20.3 21.4 18.8 37.6 ✓ ✓✓ 68.8 54.3 66.5 37 25.3 17.1 16.2 17.8 37.9 ✓ ✓ 49.3 46.1 54.8 36.2 19.3 15.3 19.4 21 32.7 ✓✓✓✓✓✓✓✓ 90.8 82.9 91.7 76.8 61.4 43.8 45.2 55.1 68.5 ✓✓✓✓✓✓✓✓✓ 94.7 83.6 91.9 83.1 64.4 44.3 35.8 58.1 69.5 ✓✓✓✓✓✓✓✓✓95 84.1 92.8 83.9 70.3 46.6 48.9 61.9 72.9 Full Model 95.3 84.2 93.1 84.4 71.1 46.1 49.4 62.8 73.3

Notation: P = Preprocessing; 0=Signal Scaling, 1=Permutation, 2=Window Slicing, 3=Time Warping, 4=Magnitude Warping, 5=Window Warping; s = Lclass + Lproto; c = LP L; i = LIM.

**Table 3.** Ablation study on model components.

curacy is much lower than ours. ConvTran, despite architectural advances, overfits to source-domain noise without dedicated enhancement strategies, leading to poor generalization. These results highlight our method’s advantage on distance robustness.

Temporal Robustness. We further validate our method’s robustness to temporal domain shifts—a widely studied RFF task where the surrounding environments drift over time while the spatial configuration of transceivers keep fixed. Beyond ORACLE (2 time domains, all distances) and LoRa (5 time domains, fixed distance), we include two dedicated temporal benchmarks: WiSig (4 time domains) and CORES (5 time domains). As shown in Table 2, our framework achieves 88% and 82% average cross-temporal accuracy on WiSig and CORES (i.e., any single domain trained to generalize across others), outperforming all SOTA methods. This observation aligns with our intuition that features robust to severe spatial perturbations naturally adapt to milder temporal shifts (e.g., gradual environmental drift), as distanceinduced domain shifts are more disruptive.

Analytical Experiments Ablation Study. To analyze the contribution of each component in our cross-distance RFF framework, we conducted ablation experiments using the ORACLE.1 dataset, with the source domain at 2ft and target domain at the distances ranging from 8ft to 50ft for generalization evaluation. As shown in Table 3, we incrementally added modules draw the following conclusions: (1) Preprocessing is an indispensable step. When disabled, the average accuracy drops to 17.2%. Normalization and filtering noisy high-freuquency components stabilize subsequent feature learning, providing a consistent input space for downstream optimization. (2) Combinatorial data augmentations (0 to 5 types) play a criti-

Target Source

Target Source

**Figure 5.** t-SNE visualization of features (ORACLE.1).

cal role in distance-invariant feature learning. By simulating channel effects induced by path loss and multipath effects, these augmentations enable the contrastive optimizer to extract robust features. (3) Our framework exhibits inherent cross-distance capability even without adaptation: using only the source model already achieves an average accuracy of 68.5%. When enhanced with domain adaptation, the overall performance improves to 73.3%.

Hyperparameter Analysis. We optimize hyperparameters via grid search, identifying λ1 = 1.5, λ2 = 1, and γ = 1 as optimal values. Detailed experimental setups and hyperparameter analysis are provided in Appendix C.

Visualization of Features Space. To demonstrate the effectiveness of fingerprint disentanglement and domain alignment, we visualize the feature distributions of source (2ft) and target (8ft) domains using t-SNE embeddings (Figure 5). For device separation (16 devices, each with a distinct color), the top-left shows source-only training without augmentation produces blurred device clusters, while the topright reveals target-domain adaptation sharpens inter-class boundaries; for domain alignment, the bottom-left exhibits distinct source–target clusters under source-only training, whereas the bottom-right shows their blending after adaptation, indicating effective cross-domain feature alignment.

## Conclusion

In this paper, we propose the first unsupervised framework for distance-invariant RFF, resolving the critical issue of cross-distance generalization in practical deployment. To this end, we design a preprocessing pipeline that operates directly on raw IQ signals, enhancing fingerprint saliency while suppressing noise. Building on this, our suite of data augmentation strategies simulates diverse channel effects; when integrated with contrastive learning, this enables the extraction of distance-invariant fingerprints. Furthermore, we introduce an unsupervised domain adaptation module leveraging pseudo-labeling and information maximization, achieving robust cross-distance generalization. Extensive experiments validate that our method outperforms SOTA approaches in both cross-distance and cross-temporal scenarios, addressing a critical generalization gap in RFF.

432

<!-- Page 8 -->

## Acknowledgments

This work was supported by National Natural Science Foundation of China under Grant No.62172080, No.62271124, and National Key R&D Program of China No.2022YFB3103404.

## References

Al-Shawabka, A.; Restuccia, F.; D’Oro, S.; Jian, T.; Rendon, B. C.; Soltani, N.; Dy, J.; Ioannidis, S.; Chowdhury, K.; and Melodia, T. 2020. Exposing the fingerprint: Dissecting the impact of the wireless channel on radio fingerprinting. In IEEE Conference on Computer Communications (INFO- COM), 646–655. IEEE. Chen, H.; Zhou, R.; Yuan, Q.; Guo, Z.; and Fu, W. 2025. KAN-ResNet-Enhanced Radio Frequency Fingerprint Identification with Zero-Forcing Equalization. IEEE Sensors Journal, 25(7): 2222–2252. Cui, Z.; Chen, W.; and Chen, Y. 2016. Multi-scale convolutional neural networks for time series classification. arXiv preprint arXiv:1603.06995. DARPA. 2017. The Radio Frequency Spectrum + Machine Learning = A New Wave in Radio Technology. https://www. darpa.mil/news-events/2017-08-11a. Demirel, B. U.; and Holz, C. 2023. Finding order in chaos: a novel data augmentation method for time series in contrastive learning. In Proceedings of the 37th International Conference on Neural Information Processing Systems(NeurIPS). Red Hook, NY, USA: Curran Associates Inc. Elmaghbub, A.; and Hamdaoui, B. 2021. LoRa Device Fingerprinting in the Wild: Disclosing RF Data-Driven Fingerprint Sensitivity to Deployment Variability. IEEE Access, 9: 142893–142909. Foumani, N. M.; Tan, C. W.; Webb, G. I.; and Salehi, M. 2024. Improving position encoding of transformers for multivariate time series classification. Data Mining and Knowledge Discovery, 38(1): 22–48. Grill, J.-B.; Strub, F.; Altch´e, F.; Tallec, C.; Richemond, P.; Buchatskaya, E.; Doersch, C.; Avila Pires, B.; Guo, Z.; Gheshlaghi Azar, M.; et al. 2020. Bootstrap your own latenta new approach to self-supervised learning. In Proceedings of the International Conference on Neural Information Processing Systems(NeurIPS), volume 33, 21271–21284. Han, Z.; Xiao, J.; Zhao, Q.; Cui, Z.; Wang, Y.; Zhang, D.; and Ding, W. 2025. Open-world Radio Frequency Fingerprint Identification via Augmented Semi-supervised Learning. In Proceedings of the AAAI Conference on Artificial Intelligence(AAAI), 264–272. AAAI Press. Hanna, S.; Karunaratne, S.; and Cabric, D. 2020. Open set wireless transmitter authorization: Deep learning approaches and dataset considerations. IEEE Transactions on Cognitive Communications and Networking, 7(1): 59–72. Hanna, S.; Karunaratne, S.; and Cabric, D. 2022. WiSig: A Large-Scale WiFi Signal Dataset for Receiver and Channel Agnostic RF Fingerprinting. IEEE Access, 10: 22808– 22818.

Hu, W.; Miyato, T.; Tokui, S.; Matsumoto, E.; and Sugiyama, M. 2017. Learning discrete representations via information maximizing self-augmented training. In Proceedings of the 34th International Conference on Machine Learning(ICML), volume 70, 1558–1567. PMLR. Hu, Z.; Yang, Z.; Hu, X.; and Nevatia, R. 2021. Simple: Similar pseudo label exploitation for semi-supervised classification. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 15099–15108. Khosla, P.; Teterwak, P.; Wang, C.; Sarna, A.; Tian, Y.; Isola, P.; Maschinot, A.; Liu, C.; and Krishnan, D. 2020. Supervised contrastive learning. In Proceedings of the International Conference on Neural Information Processing Systems(NeurIPS), volume 33, 18661–18673. Li, H.; Gupta, K.; Wang, C.; Ghose, N.; and Wang, B. 2022. RadioNet: Robust deep-learning based radio fingerprinting. In IEEE Conference on Communications and Network Security (CNS), 190–198. IEEE. Li, J.; Yu, Z.; Du, Z.; Zhu, L.; and Shen, H. T. 2024. A comprehensive survey on source-free domain adaptation. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(8): 5743–5762. Liu, J.; and Chen, S. 2024. Timesurl: Self-supervised contrastive learning for universal time series representation learning. In Proceedings of the AAAI conference on artificial intelligence, 13918–13926. AAAI Press. Long, M.; Cao, Z.; Wang, J.; and Jordan, M. I. 2018. Conditional adversarial domain adaptation. In Proceedings of the International Conference on Neural Information Processing Systems(NeurIPS), volume 31. Pan, R.; Chen, H.; Shen, G.; and Chen, H. 2025. Residual Channel Boosts Contrastive Learning for Radio Frequency Fingerprint Identification. IEEE Wireless Communications Letters, 14(6): 1728–1732. Rashid, K. M.; and Louis, J. 2019. Window-warping: A time series data augmentation of IMU data for construction equipment activity identification. In Proceedings of the international symposium on automation and robotics in construction(ISARC), volume 36, 651–657. IAARC Publications. Sankhe, K.; Belgiovine, M.; Zhou, F.; Riyaz, S.; Ioannidis, S.; and Chowdhury, K. 2019. ORACLE: Optimized Radio clAssification through Convolutional neuraL nEtworks. In IEEE Conference on Computer Communications (INFO- COM), 370–378. Shen, G.; Zhang, J.; Marshall, A.; Peng, L.; and Wang, X. 2021. Radio frequency fingerprint identification for LoRa using deep learning. IEEE Journal on Selected Areas in Communications, 39(8): 2604–2616. Shen, G.; Zhang, J.; Marshall, A.; Valkama, M.; and Cavallaro, J. R. 2023. Toward length-versatile and noise-robust radio frequency fingerprint identification. IEEE Transactions on Information Forensics and Security, 18: 2355–2367. Snell, J.; Swersky, K.; and Zemel, R. 2017. Prototypical networks for few-shot learning. In Proceedings of the International Conference on Neural Information Processing Systems(NeurIPS), volume 30.

433

<!-- Page 9 -->

Sun, M.; Teng, J.; Liu, X.; Wang, W.; and Huang, X. 2025. Few-Shot Specific Emitter Identification: A Knowledge, Data, and Model-Driven Fusion Framework. IEEE Transactions on Information Forensics and Security, 20: 3247–3259.

Um, T. T.; Pfister, F. M.; Pichler, D.; Endo, S.; Lang, M.; Hirche, S.; Fietzek, U.; and Kuli´c, D. 2017. Data augmentation of wearable sensor data for parkinson’s disease monitoring using convolutional neural networks. In Proceedings of the 19th ACM international conference on multimodal interaction(ICMI), 216–220. ACM.

Wan, H.; Wang, Q.; Fu, X.; Wang, Y.; Zhao, H.; Lin, Y.; Sari, H.; and Gui, G. 2024. VC-SEI: Robust variable-channel specific emitter identification method using semi-supervised domain adaptation. IEEE Transactions on Wireless Communications, 23(12): 18228–18239.

Wang, X.; Wang, Q.; Fang, L.; Hua, M.; Jiang, Y.; and Hu, Y. 2024. Radio frequency fingerprint authentication based on feature fusion and contrastive learning. Expert Systems with Applications, 255: 124537.

Wu, W.; Hu, S.; Lin, D.; and Liu, Z. 2021. DSLN: Securing Internet of Things through RF fingerprint recognition in low- SNR settings. IEEE Internet of Things Journal, 9(5): 3838– 3849.

Xu, H.; and Xu, X. 2021. A transformer based approach for open set specific emitter identification. In 2021 7th International Conference on Computer and Communications (ICCC), 1420–1425. IEEE.

Yan, H.; Ding, Y.; Li, P.; Wang, Q.; Xu, Y.; and Zuo, W. 2017. Mind the class weight bias: Weighted maximum mean discrepancy for unsupervised domain adaptation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2272–2281.

Yao, M.; Liu, C.; Xie, L.; and Chi, M. 2025. MambaRF: A Bi-directional Mamba Structure for Radio Frequency Signal Classification of Unmanned Aerial Vehicle. In IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 1–5. IEEE.

Yin, L.; Fu, X.; Shi, S.; Liu, P.; Lin, Y.; Wang, Y.; and Sari, H. 2023. Few-shot domain adaption-based specific emitter identification under varying modulation. In IEEE 23rd International Conference on Communication Technology (ICCT), 1439–1443. IEEE.

Zha, X.; Li, T.; Qiu, Z.; and Li, F. 2023. Cross-receiver radio frequency fingerprint identification based on contrastive learning and subdomain adaptation. IEEE Signal Processing Letters, 30: 70–74.

Zhang, J.; Ardizzon, F.; Piana, M.; Shen, G.; and Tomasin, S. 2025. Physical Layer-Based Device Fingerprinting For Wireless Security: From Theory To Practice. IEEE Transactions on Information Forensics and Security, 20: 5296–5325.

Zhang, K.; Wen, Q.; Zhang, C.; Cai, R.; Jin, M.; Liu, Y.; Zhang, J. Y.; Liang, Y.; Pang, G.; Song, D.; et al. 2024. Self-supervised learning for time series analysis: Taxonomy, progress, and prospects. IEEE transactions on pattern analysis and machine intelligence, 46(10): 6775–6794.

Zhang, X.; Li, T.; Gong, P.; Zha, X.; and Liu, R. 2022. Variable-modulation specific emitter identification with domain adaptation. IEEE Transactions on Information Forensics and Security, 18: 380–395. Zhao, T.; Wang, X.; and Mao, S. 2024. Cross-domain, scalable, and interpretable RF device fingerprinting. In IEEE Conference on Computer Communications (INFOCOM), 2099–2108. IEEE.

434
