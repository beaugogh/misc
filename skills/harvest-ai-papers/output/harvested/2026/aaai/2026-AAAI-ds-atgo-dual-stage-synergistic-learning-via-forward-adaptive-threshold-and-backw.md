---
title: "DS-ATGO: Dual-Stage Synergistic Learning via Forward Adaptive Threshold and Backward Gradient Optimization for Spiking Neural Networks"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37165
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37165/41127
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# DS-ATGO: Dual-Stage Synergistic Learning via Forward Adaptive Threshold and Backward Gradient Optimization for Spiking Neural Networks

<!-- Page 1 -->

DS-ATGO: Dual-Stage Synergistic Learning via Forward Adaptive Threshold and

Backward Gradient Optimization for Spiking Neural Networks

Jiaqiang Jiang1, 2, Wenfeng Xu1, 2, Jing Fan1, 2, Rui Yan1, 2*

1College of Computer Science and Technology, Zhejiang University of Technology, Hangzhou 310023 2Zhejiang Key Laboratory of Visual Information Intelligent Processing, Hangzhou 310023 {jqjiang, wfxu, fanjing, ryan}@zjut.edu.cn

## Abstract

Brain-inspired spiking neural networks (SNNs) are recognized as a promising avenue for achieving efficient, lowenergy neuromorphic computing. Direct training of SNNs typically relies on surrogate gradient (SG) learning to estimate derivatives of non-differentiable spiking activity. However, during training, the distribution of neuronal membrane potentials varies across timesteps and progressively deviates toward both sides of the firing threshold. When the firing threshold and SG remain fixed, this may lead to imbalanced spike firing and diminished gradient signals, preventing SNNs from performing well. To address these issues, we propose a novel dual-stage synergistic learning algorithm that achieves forward adaptive thresholding and backward dynamic SG. In forward propagation, we adaptively adjust thresholds based on the distribution of membrane potential dynamics (MPD) at each timestep, which enriches neuronal diversity and effectively balances firing rates across timesteps and layers. In backward propagation, drawing from the underlying association between MPD, threshold, and SG, we dynamically optimize SG to enhance gradient estimation through spatio-temporal alignment, effectively mitigating gradient information loss. Experimental results demonstrate that our method achieves significant performance improvements. Moreover, it allows neurons to fire stable proportions of spikes at each timestep and increases the proportion of neurons that obtain gradients in deeper layers.

Code — https://github.com/jqjiang1999/DS-ATGO Extended version — https://arxiv.org/abs/2511.13050

## Introduction

As a new paradigm that combines biological plausibility with computational efficiency, spiking neural networks (SNNs) have recently attracted widespread attention (Maass 1997). Unlike artificial neural networks (ANNs), which work with continuous activation and real-valued encoding (Ju et al. 2025b,a; Zhang et al. 2025; Feng et al. 2025; Zhang, Yuan, and Pan 2024), SNNs operate with asynchronous, discrete spiking signals. This spike train-based way renders SNNs highly promising for spatio-temporal

*Corresponding author: Rui Yan (ryan@zjut.edu.cn) Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

0 0.5 1.0 0

10000

15000

20000

25000

30000

Number of neurons

U(t) N(0, 1/9)

0 0.5 1.0 Firing rates

0

10000

12000

14000 U(t) N(0, 1)

0 0.5 1.0 0

10000

U(t) N(0, 9)

**Figure 1.** The distributions of firing rates at differ variances of membrane potential when Vth = 1.0 (Zheng et al. 2021).

(ST) information processing and energy-efficient computation compared to ANNs (Roy, Jaiswal, and Panda 2019). Despite these advantages, the non-differentiable nature of spike activity hinders gradient backpropagation, making it more difficult to directly train high-performance SNNs than ANNs. To overcome this issue, surrogate gradient (SG) learning (Wu et al. 2018) estimates the gradients of output signals by introducing continuous smooth functions, which reconstruct a complete propagation path of ST gradients.

However, as spikes propagate through layers, the distribution of membrane potentials shifts and may fall into inappropriate areas (Guo et al. 2022b; Liu et al. 2025) (Fig. 2). To our best knowledge, most existing SG-based methods for directly training SNNs use a fixed threshold and SG. Thus, membrane potential dynamics (MPD) may present two challenges that lead to training difficulties.

The first challenge is the imbalanced spike firing of SNNs with a fixed threshold. The neuron fires a spike only when its membrane potential exceeds the threshold Vth. In Fig. 1, when membrane potentials are too small compared to the threshold, excessive sparse firing in neurons will lead to the “spike vanishing problem”. When membrane potentials are too large, neurons will be over-firing, reducing the ability to represent the input pattern differentially. To maintain the stability of information flow in SNN, we need to balance the threshold and membrane potentials to keep neurons in a moderately active state. Neuroscience has observed in various brain regions that the thresholds of biological neurons are not constant but exhibit variability between and within neurons (Azouz and Gray 2000; Farries, Kita, and Wilson 2010). This phenomenon, known as threshold plasticity, can

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

<!-- Page 2 -->

Degeneration

Membrane Potential Shifts Saturation

**Figure 2.** The distribution of membrane potentials deviating from the threshold in a vanilla SNN with ten timesteps. When almost all the membrane potentials of neurons are beyond Vth, called saturation. Conversely, called degeneration.

be regarded as an adaptation to membrane potentials, which plays an essential role in maintaining neuronal firing homeostasis (Fontaine, Pe˜na, and Brette 2014). To model threshold plasticity, (Wang, Cheng, and Lim 2022; Rathi and Roy 2023; Sun et al. 2024; Hasssan, Meng, and Seo 2024) directly set the threshold as a learnable parameter and optimize it dynamically via gradients. Although this effectively enhances neuronal firing levels, its optimization relies solely on the gradient of thresholds itself, leaving uncertainty in maintaining the balance of firing rates in SNNs.

The other challenge is the diminished gradient information of SNNs with a fixed SG. The neuron obtains a gradient only when its membrane potential falls within the gradientavailable interval of SG. In Fig. 2, when membrane potentials is too small or too large compared to the threshold, the limited gradient-available interval of fixed SG causes the membrane potentials of many neurons to fall into the areas where the approximate derivatives are zero or a tiny value. In this case, only a few neurons contribute gradients, leading to the “gradient vanishing problem”. (Lian et al. 2023) dynamically adjusted the SG based on changes in the MPD distribution. It ignores the dynamic nature of evolving MPD in the temporal dimension, which may exacerbate the inaccurate estimation of gradients. Then, (Jiang et al. 2025; Liu et al. 2025) optimized the SG of different timesteps in a temporalaligned manner. In SG learning, the gradient-available interval of SG is symmetrically centered around the threshold. However, these methods overlook the association between MPD, threshold, and SG, making SG fail to accurately capture the dynamic deviations of membrane potentials relative to thresholds. Therefore, the neuronal threshold can be regarded as an idealized tunable parameter that regulates spike firing and affects gradient optimization.

In this paper, we propose a novel dual-stage synergistic learning via forward adaptive threshold and backward gradient optimization for SNNs, named DS-ATGO. By utilizing the distribution characteristics of MPD at each timestep, we adaptively adjust thresholds to enhance the ability of neurons to encode dynamic information, achieving a linear response to input signals. Building on the observation that adaptive thresholds reflect shifts in membrane potentials, we further establish a correlation between SG and MPD via thresholds. Based on that, we dynamically adjust SG in a threshold-driven manner to align with evolving MPD, contributing smoother spatio-temporal gradients and maintaining the optimal gradient domain across timesteps. The overall framework of DS-ATGO is illustrated in Fig. 3. The main contributions of our work are summarized as follows:

• We propose an adaptive threshold mechanism that adapts the firing threshold in the temporal dimension by leveraging the MPD distribution. It balances neuronal spike firing across layers, enhancing the cross-layer information transmission capability of SNNs. • We propose a threshold-driven gradient optimization method that dynamically adjusts SG at each timestep by associating SG with evolving MPD via adaptive thresholds, effectively enhancing ST gradient information. • The experimental results on both static and neuromorphic datasets demonstrate that DS-ATGO achieves outstanding performance with low latency without additional inference overhead.

···

…1011…

…1110…

…0110…

…1001…

…1111…

…0101…

Pre-spikes Post-spikes

AT

TGO

AT: adaptively adjust thresholds to balance spike firing rates concentrated MPD, narrower SG concentrated MPD, lower dispersed MPD, higher spike firing area

TGO: dynamically optimize SG to reduce gradient information loss dispersed MPD, wider SG gradient-available area

**Figure 3.** The overall framework of DS-ATGO. Internal dynamics of LIF neurons in a layer (gray). In forward propagation, the adaptive threshold (AT) mechanism promotes neurons to generate stable firing rates under different MPD distributions (green). In backward propagation, the thresholddriven SG optimization (TGO) method dynamically scales SG to respond to evolving MPD (yellow).

Related Works Spiking Threshold Plasticity Spiking threshold plasticity is a biological mechanism by which neurons dynamically adjust their firing thresholds according to historical activity patterns. To express this characteristic, (Ai et al. 2025) dynamically adjusted the threshold based on the repetitive or high-frequency discharge re-

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-002-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

sponses of neurons, effectively preventing excessive activation of neurons. (Fu et al. 2025) proposed a spatio-temporal threshold adjustment strategy, which enhances the spike coding capacity of SNNs by coupling with neural dynamics. In addition, some studies on SNN training have introduced learning dynamics into spike processes (Wang, Cheng, and Lim 2022; Rathi and Roy 2023). (Sun et al. 2024) proposed a synapse-threshold synergistic learning, which allows stable signal transmission through appropriate firing rates by simultaneously training weights and thresholds. Considering the weights and threshold same landscape makes the learning sub-optimal, (Hasssan, Meng, and Seo 2024) achieved individually adaptive optimization of layer-wise thresholds and weights by introducing a separate gradient path.

Gradient Optimization The concept of gradient optimization in SNN aims to promote the efficient propagation of error signals in the ST domain by adjusting SG (Fang et al. 2021a). (Guo et al. 2022a) approximated the spike activity gradient by a continuously differentiable evolving asymptotic function, bridging the gap between pseudo and natural derivatives. (Che et al. 2022) proposed a differentiable gradient search method to optimize SG locally. (Lian et al. 2023) unlocked the width limitation of SG based on changes in MPD distributions, increasing the proportion of neurons that obtained gradients. (Wang et al. 2023) adaptively learned the accurate gradients of the loss landscape in SNN by fusing the learnable relaxation degree into a prototype network with random spike noise, effectively eliminating the smoothing error of SG learning. (Wang, Cheng, and Lim 2025) proposed a parametric SG strategy to control and calibrate SG, which mitigates the degradation caused by improper selection of SG. (Jiang et al. 2025; Liu et al. 2025) promotes balanced optimization by enhancing the gradients in a temporal-aligned manner.

Motivation: Overall, although existing methods achieve threshold or SG adjustment, they ignore the intrinsic association among membrane potential, threshold, and SG, which have limitations in jointly solving the two problems caused by membrane potential shifts. This motivates us to achieve the synergistic optimization of thresholds and SG to maintain balanced firing rates and stable gradient flows in SNNs.

## Preliminaries

Spiking Neural Model In this work, we use the Leaky Integrate-and-Fire (LIF) model in SNNs. The dynamics of an iterative LIF neuron (Wu et al. 2019) can be modeled by

Il i(t) =

N(l−1) X j=1 wl ijSl−1 j (t), (1)

U l i(t) = τU l i(t −1) ⊙(1 −Sl i(t −1)) + Il i(t), (2)

Sl i(t) = Θ(U l i(t)) =

1, U l i(t) ≥Vth 0, otherwise (3)

where the upper l, subscripts i and t denote the l-th layer, ith neuron, and t-th timestep, respectively. N(l −1) denotes the number of neurons in the (l−1)-th layer. wl ij denotes the synapse weight from the j-th neuron in the (l−1)-th layer to the i-th neuron in the l-th layer. I, U, and S denote the presynaptic input, the membrane potential, and the output spike of neurons. Vth is the firing threshold. τ is the membrane time constant that indicates how quickly the potential decays over time, affecting the duration of neuronal excitation.

Surrogate Gradient Function In Eq. 3, the firing function Θ(·) of SNNs is a Heaviside function. The derivative of output signals ∂S

∂U is a Dirac function that tends to infinity at the threshold Vth and zeros otherwise. Here, we employ the rectangular function (Wu et al. 2018) to estimate the gradients of ∂S ∂U, which is defined as

∂Sl i(t) ∂U l i(t) ≈h(U l i(t)) = 1 κsign(|U n i (t) −Vth| ≤κ

2), (4)

where hyperparameter κ controls the width of h(·) to ensure that it integrates to 1, normally set to 1. The gradient 1 κ is available when the membrane potential U n i (t) falls within the interval [Vth −κ

2, Vth + κ 2 ].

## Methods

Adaptive Threshold Mechanism It is difficult for SNNs with a fixed threshold to adapt to variations in input strength, making the network prone to silence or excessive firing when processing ST dynamic data. (Zheng et al. 2021) proposed a threshold-dependent batch normalization that normalized the pre-synaptic input I(t) to N(0, V 2 th) instead of N(0, 1). Although this method balances pre-synaptic inputs and thresholds to increase neuronal spike activity, the intrinsic dynamics of neurons still hinder it from maintaining the stability of firing rates across the entire timestep. That motivates us to explore how to adaptively adjust the firing threshold to keep neurons homeostatic, enhancing the dynamic responsiveness of SNNs.

Recent studies have revealed that the threshold of biological neurons exhibits a positive correlation with membrane potentials (Pena and Konishi 2002; Azouz and Gray 2003; Ding et al. 2022). Based on the insight that firing rates are directly regulated by membrane potential and threshold, we can adjust the threshold according to the evolving MPD, promoting neurons to fire appropriate spikes in SNNs. To achieve this, the key lies in balancing the proportion of membrane potentials that exceed the threshold. Theorem 1 shows that when the threshold is set as the sum of expectation and standard deviation of MPD distributions (Vth = µ + σ), the proportion of membrane potentials exceeding the threshold remains relatively constant under different distributions. Establishing a positive correlation between thresholds and membrane potentials retains the adaptive properties of biological neurons while ensuring a stable firing rate in SNNs. Theorem 1. For U(t) that satisfies a normal distribution N(µ, σ2), the probability that a random variable Ui(t) exceeds µ + σ is relatively constant and given by P(Ui(t) > µ + σ) = 1 −Φ(1), where Φ(·) denotes the cumulative distribution function of standard normal distributions.

<!-- Page 4 -->

𝑉𝑡ℎ= 0.25 Adaptive Threshold

RGB Image Gray Image C O N V

B N Encoder

Layer LIF

𝑆𝑆𝐼𝑀≈0.53 𝑆𝑆𝐼𝑀≈0.11 𝑆𝑆𝐼𝑀≈0.42

𝑉𝑡ℎ= 1.0 𝑉𝑡ℎ= 2.5

𝑆𝑆𝐼𝑀≈0.04

**Figure 4.** The structural similarity between the gray image and encoded images at different thresholds.

Proof. The proof of Theorem 1 is given in Appendix A.

To maintain neurons in a moderately active state, we first need to analyze the detailed distributions of membrane potentials. (Zheng et al. 2021) derived a high degree of similarity between the distribution of pre-synaptic inputs and membrane potentials. (Lian et al. 2023; Jiang et al. 2025) extended this theorem that for a given pre-synaptic inputs I(t) ∼N(0, V 2 th), the distribution of membrane potentials satisfies U(t) ∼N(0, (1 + τ 2)V 2 th). Given the approximate nature of MPD distributions derived by (Lian et al. 2023; Jiang et al. 2025), we can also directly use the true MPD distribution during training. Moreover, to trade-off energy efficiency and performance, we introduce a factor fc to control spiking firing rates. We will discuss these two distributions and the effect of factor fc in the ablation study. Finally, the adaptive threshold mechanism can be formulated as

∆Vth l(t)n ≈fc ∗ q

(1 + τ ln2))Vth, #Estimated (5)

= fc ∗(E(U l(t)n) + q

VAR(U l(t)n)), #True where the subscript n denotes the n-th mini-batch, τ is layerwise learnable (Fang et al. 2021b). In this way, all neurons in different layers will have distinct thresholds across different timesteps. Fig. 4 shows that using the proposed adaptive threshold in the encoding layer produces better quality images than the fixed threshold.

Considering that different mini-batches in the inference stage may cause fluctuations in MPD distributions that affect the threshold, inspired by BN (Ioffe and Szegedy 2015), we also use the moving average of thresholds during training for inference to stabilize neuron outputs. It can be described as

∆Vth l(t) = m ∗∆Vth l(t)n + (1 −m) ∗∆Vth l(t), (6)

where m is the momentum coefficient, which we set to 0.1.

Threshold-driven Gradient Optimization In SNNs, adequate gradient information is crucial for achieving efficient learning, as it directly governs weight

−2 0 2 Value

0.0

0.2

0.4

0.6

0.8

1.0

Density

Vth

Vth

Vth

(a)

U(t) ∼N(0, 1/4)

47.72% U(t) ∼N(0, 1)

24.17% U(t) ∼N(0, 4)

12.10%

−2 0 2 Value

0.0

0.2

0.4

0.6

0.8

1.0

Vth

Vth

Vth

(b)

U(t) ∼N(0, 1/4)

26.00% U(t) ∼N(0, 1)

24.17% U(t) ∼N(0, 4)

21.30%

**Figure 5.** (a) The proportion of membrane potentials that fall into the gradient-available interval with fixed SG (k = 1) under different distributions when using adaptive threshold. (b) The proportion of gradient-available when using the adaptive threshold and threshold-driven gradient optimization.

updates and model convergence. When SG remains fixed, membrane potential shifts will cause decreased gradients during backpropagation. The adaptive threshold mechanism adjusts the gradient-available interval of fixed SG to [∆Vth−

1 2, ∆Vth + 1 2] instead of [Vth −1 2, Vth + 1 2], but the above issue remains due to the inherent mismatch between fixed SG and evolving MPD. Specifically, in Fig. 5, when the variance of MPD distributions becomes smaller (blue), a large number of neuronal membrane potentials will fall within the gradient-available interval for gradient computation, enlarging the approximation error with the natural gradient. Conversely, when the variance of MPD distributions becomes larger (green), only a few neurons will obtain gradients, and most neurons will fall into the saturation area with zero gradients, resulting in vanishing gradient.

To optimize SG learning, we need to modify SG accordingly to better respond to evolving MPD. (Lian et al. 2023; Jiang et al. 2025) indicated an association between SG and MPD. Given that the adaptive threshold reflects changes in MPD distributions (Eq. 5) and that the threshold determines the location of SG. Then, we propose a threshold-driven gradient optimization method that dynamically adjusts SG width (Fig. 5), ensuring that the gradient-available interval aligns with MPD. For the above two distinct cases, we design two rules to calculate the SG width, as follows:

• ∆Vth < Vth: When the adaptive threshold ∆Vth is less than the initial threshold Vth, which indicates the MPD distribution tends to concentrate, thus we need to reduce the SG width to decrease the proportion of neurons fall into the gradient-available interval, suppressing the cumulative enlargement of gradient approximation errors. • ∆Vth ≥Vth: When the adaptive threshold ∆Vth is greater than the initial threshold Vth, which indicates the MPD distribution tends to disperse, thus we need to expand the SG width to increase the proportion of neurons falling into the gradient-available interval, mitigating the loss of gradient information.

In summary, the threshold-driven gradient optimization method can be mathematically written as k =

(1 −tanh(Vth −∆Vth)) ∗k, ∆Vth < Vth (1 + tanh(∆Vth −Vth)) ∗k, ∆Vth ≥Vth

(7)

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-004-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

The Overall Procedure of SNNs In the output layer, we only accumulate the membrane potential of output neurons without leakage and firing (Rathi and Roy 2023), which can be described by

U lo i = 1

T

T X t=1

N(lo−1) X j=1 wlo ijSlo−1 j (t), i ∈{1, 2,..., c} (8)

where lo and c denote the output layer and the number of classes, respectively. The network loss L is calculated using the cross-entropy function. As U l i(t) not only contributes to Sl i(t) but also governs U l i(t + 1), it can be derived by

∂L ∂U l i(t) = ∂L ∂Sl i(t)

∂Sl i(t) ∂U l i(t) + ∂L ∂U l i(t + 1)

∂U l i(t + 1) ∂U l i(t), (9)

∂L ∂Sl i(t) = ∂L ∂U l i(t + 1)

∂U l i(t + 1) ∂Sl i(t)

+

N(l+1) X j=1

∂L ∂U l+1 j (t)

∂U l+1 j (t)

∂Sl j(t). (10)

where ∂Sl i(t) ∂U l i(t) are approximated by Eq. 4. Then, the gradient of synaptic weights wl ij can be derived by the chain rule:

∂L ∂wl ij

=

T X t=1

∂L ∂U l i(t)

∂U l i(t) ∂Il i(t)

∂Il i(t) ∂wl ij

=

T X t=1

∂L ∂U l i(t)

N(l−1) X j=1

Sl−1 j (t). (11)

Moreover, the pseudocode of the overall procedure is briefed in Appendix B.

## Experiments

Ablation Study The performance improvement of our model benefits from the adaptive threshold mechanism (AT) and threshold-driven gradient optimization method (TGO). We conducted experiments to evaluate their contributions. In Fig. 6, applying AT (w/ AT) outperforms Vanilla-SNN on two datasets. This indicates that adaptively adjusting thresholds in response to evolving MPD enables flexible control over the timing and intensity of neuron activation, enhancing the SNN’s ability to model complex dynamic information. Notably, applying TGO (w/ TGO) also achieves significant improvements over Vanilla-SNN, even surpassing AT. The reason is that, unlike AT, which focuses on spike modulation in information encoding, TGO synchronously adjusts SG to accurately capture the dynamic deviation of membrane potentials relative to thresholds. It effectively maintains the balance of gradient signals in the temporal dimension, enhancing the efficiency and correctness of parameter updates. Furthermore, combining the two techniques (w/ AT+TGO) enables SNNs to balance firing rates for improved encoding efficiency and optimize SG through temporal alignment for gradient enhancement, further boosting performance. It achieved remarkable

**Figure 6.** Comparison of training loss and test accuracy.

CIFAR100 CIFAR10-DVS Datasets

79

80

81

82

83

84

Accuracy (%)

Estimated True

**Figure 7.** Comparison of estimated with true MPD distribution and w/ vs. w/o moving average (box plot vs. violin plot).

improvements of 1.71% and 2.30% on the CIFAR10 and CIFAR10-DVS datasets, respectively.

Moreover, Fig. 7 illustrates that DS-ATGO driven by the true MPD distribution outperforms the theoretical distribution derived by (Lian et al. 2023), which indicates that the theorem derivation involves certain approximation errors. Then, we evaluated the effectiveness of the moving average rule. When applying this rule in AT, the accuracy of both datasets surpassed the baseline without the rule. Especially for CIFAR10-DVS trained with mini-batches, the threshold moving average more effectively adapts to MPD fluctuations, exhibiting higher performance improvements.

Performance Evaluation As listed in Table 1, we compare the classification accuracy of our method with other advanced methods. DS-ATGO performed well on all four datasets, achieving an accuracy of 96.91%/80.59% with low latency on CIFAR10/100, 83.70% and 68.86% accuracy on CIFAR10-DVS and ImageNet, respectively. Methods that only adjust thresholds (e.g., LT- SNN) or only optimize SG (e.g., DeepTAGE) both perform worse than ours, indicating that the two challenges arising

![Figure extracted from page 5](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-005-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-005-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-005-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-ds-atgo-dual-stage-synergistic-learning-via-forward-adaptive-threshold-and-backw/page-005-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

Dataset Method AT GO Architecture Timestep Accuarcy(%)

CIFAR10

STAtten+ (Lee et al. 2025) Spikformer-4-384 4 94.36 Distillation-based SNN (Yu et al. 2025a) ResNet-18 6 / 4 95.96 / 95.57 STL-SNN (Sun et al. 2024) 8-layers SNN 8 92.42 LT-SNN (Hasssan, Meng, and Seo 2024) Spikformer-4-256 4 95.19 DeepTAGE (Liu et al. 2025) ResNet-18 4 95.86 MPD-AGL (Jiang et al. 2025) ResNet-19 4 / 2 96.35 / 96.18 AT-LIF&ASG-S (Ai et al. 2025) ResNet-18 6 / 4 95.47 / 95.30 Ours ResNet-19 2 96.91±0.12

CIFAR100

TMC (Yan et al. 2025) ResNet-19 6 / 4 / 2 78.05 / 77.52 / 76.35 SNN-ViT (Wang et al. 2025) VGG-16 4 80.01 LT-SNN (Hasssan, Meng, and Seo 2024) ResNet-19 6 / 2 74.82 / 72.78 ALSF (Fu et al. 2025) ResNet-19 2 78.73 DeepTAGE (Liu et al. 2025) ResNet-18 4 78.80 MPD-AGL (Jiang et al. 2025) ResNet-19 4 / 2 79.72 / 78.84 AT-LIF&ASG-S (Ai et al. 2025) ResNet-18 6 / 4 76.44 / 76.42 Ours ResNet-19 2 80.59±0.17

CIFAR10-DVS

FSTA-SNN (Yu et al. 2025b) ResNet-20 10 81.50 QP-SNN (Wei et al. 2025) VGGSNN 10 82.10 STL-SNN (Sun et al. 2024) 7-layers SNN 20 77.30 LT-SNN (Hasssan, Meng, and Seo 2024) VGG-9 30 80.07 DeepTAGE (Liu et al. 2025) VGG-11 10 81.23 MPD-AGL (Jiang et al. 2025) VGGSNN 10 82.50 AT-LIF&ASG-S (Ai et al. 2025) VGGSNN 10 78.70 Ours VGGSNN 10 83.70±0.41

ImageNet

AGMM (Liang et al. 2025) ResNet-18 4 64.67 ReverB (Guo et al. 2025) ResNet-18 4 66.22 MTT (Du et al. 2025) ResNet-34 4 67.54 LTF&ALSF (Fu et al. 2025) SEW ResNet-18 4 63.67 DeepTAGE (Liu et al. 2025) ResNet-18 4 68.52 Ours ResNet-18 4 68.86±0.25

**Table 1.** Comparison of classification accuracy. AT and GO denote adaptive threshold and gradient optimization, respectively.

from membrane potential shifts limit performance. Enhancing SNNs requires considering both adaptive regulation of neuronal firing thresholds and dynamic optimization of gradient learning. In particular, as analyzed in ablation studies, most methods related to gradient optimization are superior to methods for threshold adaptation. Although AT- LIF&ASG-S also achieves threshold and SG adjustment, it ignores the correlation between them, lacking synergistic learning. In summary, our method combines these two techniques to develop a two-stage synergistic learning that achieves higher accuracy with low latency, demonstrating weak-to-strong generalization and computational efficiency.

Spike Firing Rates To validate whether our method can effectively balance firing rates, we conducted experiments on the CIFAR10 dataset. In Fig. 8, Vanilla-SNN exhibits a low firing rate (average 10.66%) with large fluctuations between layers, which hinders adequate encoding of input information. DIET-SNN (Rathi and Roy 2023) and LTMD (Wang, Cheng, and Lim 2022) methods substantially increase the firing level of neurons by adapting thresholds, avoiding extensive information loss. However, their firing rates across layers exhibit even greater oscillations, and the high firing rates certainly increase energy consumption. Instead, our firing rates remain within a small fluctuation range of nearly 15±1.62%. This stability stems from DS-ATGO’s adaptive adjustment of

10

## 20 Vanilla-SNN

25

## 50 DIET-SNN

25

## 50 LTMD

1 2 3 4 5 7 8 9 10 11 12 13 14 15 16 17 18 Layer

15

20 average

Ours

Firing rate (%)

**Figure 8.** Comparison of firing rates for each layer in ResNet-19, where grey dotted lines denote average values.

thresholds based on the MPD distribution at each timestep, which helps neurons maintain moderate activation. Moreover, the firing rates of the last layer in the other three methods exhibit a steep increase. This may be due to the accumulated deviation of membrane potentials from thresholds over time, resulting in a slow decrease in firing rates. To compensate for the diminishing useful features in the hidden layers, output layer neurons are forced to fire more spikes by dynamically lowering thresholds or enhancing weights in an

<!-- Page 7 -->

1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00 1.00

0.75

0.50

0.25

0.00

0.25

0.50

0.75

## 1.00 Vanilla-SNN

1.1

1.6

2.1

2.6

3.1

3.6

4.1

4.6

5.1

5.1

5.1

5.1

5.1

5.6

1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00 1.00

0.75

0.50

0.25

0.00

0.25

0.50

0.75

## 1.00 ASG-S

1.1

1.6

2.1

2.6

3.1

3.6

4.1

4.6

5.1

5.6

5.6

6.1

6.1

6.1

6.1

6.6

6.6

1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00 1.00

0.75

0.50

0.25

0.00

0.25

0.50

0.75

## 1.00 Ours

1.1

1.6

2.1

2.6

3.1

3.6

4.1

4.6

5.1

5.6

6.1

6.1

6.1

6.6

6.6

7.1

**Figure 9.** The 2D loss landscape of ResNet-19 trained with different methods on the CIFAR100 dataset.

T=1

T=6

FR: 0.142

FR: 0.159

T=2

T=7

FR: 0.140

FR: 0.149

T=3

T=8

FR: 0.147

FR: 0.158

T=4

T=9

FR: 0.154

FR: 0.154

T=5

T=10

FR: 0.150

FR: 0.157

**Figure 10.** Case study of firing rates (FR) at each timestep.

attempt to reconstruct complete feature representations. Although this temporarily enhances the excitability of output neurons, it causes neurons to over-respond to non-sharp signals, which is not conducive to recognition. Then, we presented the original image (rows 1, 3) and feature maps (rows 2, 4) on the CIFAR10-DVS dataset. In Fig. 10, our method effectively maintains the firing rate stable over timesteps and extracts good feature maps.

Proportion of Gradient Available To investigate whether our method can effectively mitigate the gradient vanishing problem, we conducted experiments on the CIFAR100 dataset. In Fig. 11, the fixed SG of Vanilla- SNN cannot dynamically match the membrane potential shifts, resulting in only a few neurons in each layer falling within the gradient-available interval. As the number of layers deepens, this exacerbates the loss of gradient information, causing the proportion of neurons that obtain gradients in the last three layers to drop to an average of less than 15.13%. Although ASG-S (Ai et al. 2025) slightly increases the proportion by adjusting SG, it still fails to accurately capture MPD that evolves with timesteps due to the lack of temporal dependence. By comparison, our method increases the gradient-available rate of each layer in ResNet-19 to over 38.53%, and even maintains 36.54% in the deeper layers. Then, we visualized the 2D loss landscapes of these meth-

1 2 3 4 5 6 8 9 10 11 12 13 14 15 16 17 18 Layer

0

20

40

60

80

100

Proportion (%)

Vanilla LSG Ours

**Figure 11.** The proportion of neurons falling within the gradient-available interval of each layer in ResNet-19.

ods. In Fig. 9, the loss surface of Vanilla-SNN exhibits two local minima, with obvious protrusions in the contour lines around the center point, reflecting oscillations in weight updates caused by gradient loss. Although the loss landscape of ASG-S contains only one local minimum, its contour lines form an elliptical region. In contrast, the loss surface of our method exhibits a uniformly continuous downward trend in the parameter space through synergistic optimization, generating a sparser and flatter loss landscape.

## Conclusion

In this paper, we present a new perspective on the performance limitations of SNNs by analyzing shifts in membrane potential distributions and deviations from the threshold. Fixed thresholds and SG are inherently mismatched with evolving MPD across timesteps, leading to imbalanced firing and diminished gradient problems. Then, we propose the DS-ATGO learning algorithm, which responds to evolving MPD across both temporal and spatial dimensions via forward adaptive thresholding and backward SG optimization. This dual-stage synergistic learning framework aims to help SNNs break through the performance bottlenecks of single-path techniques. Experimental results and analyzes demonstrate that DS-ATGO outperforms methods that only adjust thresholds or optimize SG. By balancing the firing rate and enhancing the gradient signal across timesteps, our method improves information encoding efficiency while optimizing loss landscapes, potentially advancing the application of SNNs to more complex tasks and wider scenarios.

<!-- Page 8 -->

## Acknowledgements

This work was supported by the National Key R&D Program of China (Grant No. 2025YFG0100700) and the National Natural Science Foundation of China (Grant No. 62276235).

## References

Ai, Q.; Yang, Y.; Cai, M.; Chen, K.; Liu, Q.; and Ma, L. 2025. A cross-layer residual spiking neural network with adaptive threshold leaky integrate-and-fire neuron and learnable surrogate gradient. Knowledge-Based Systems, 319: 113575. Azouz, R.; and Gray, C. M. 2000. Dynamic spike threshold reveals a mechanism for synaptic coincidence detection in cortical neurons in vivo. Proceedings of the National Academy of Sciences, 97(14): 8110–8115. Azouz, R.; and Gray, C. M. 2003. Adaptive coincidence detection and dynamic gain control in visual cortical neurons in vivo. Neuron, 37(3): 513–523. Che, K.; Leng, L.; Zhang, K.; Zhang, J.; Meng, Q.; Cheng, J.; Guo, Q.; and Liao, J. 2022. Differentiable hierarchical and surrogate gradient search for spiking neural networks. Advances in Neural Information Processing Systems, 35: 24975–24990. Ding, J.; Dong, B.; Heide, F.; Ding, Y.; Zhou, Y.; Yin, B.; and Yang, X. 2022. Biologically inspired dynamic thresholds for spiking neural networks. Advances in neural information processing systems, 35: 6090–6103. Du, K.; Wu, Y.; Deng, S.; and Gu, S. 2025. Temporal flexibility in spiking neural networks: towards generalization across time steps and deployment friendliness. In The Thirteenth International Conference on Learning Representations. Fang, W.; Yu, Z.; Chen, Y.; Huang, T.; Masquelier, T.; and Tian, Y. 2021a. Deep residual learning in spiking neural networks. Advances in Neural Information Processing Systems, 34: 21056–21069. Fang, W.; Yu, Z.; Chen, Y.; Masquelier, T.; Huang, T.; and Tian, Y. 2021b. Incorporating learnable membrane time constant to enhance learning of spiking neural networks. In Proceedings of the IEEE/CVF international conference on computer vision, 2661–2671. Farries, M. A.; Kita, H.; and Wilson, C. J. 2010. Dynamic spike threshold and zero membrane slope conductance shape the response of subthalamic neurons to cortical input. Journal of Neuroscience, 30(39): 13180–13191. Feng, X.; Zhang, H.; Zhang, Y.; Zhang, L. Y.; and Pan, S. 2025. BiMark: Unbiased Multilayer Watermarking for Large Language Models. In Forty-second International Conference on Machine Learning. Fontaine, B.; Pe˜na, J. L.; and Brette, R. 2014. Spikethreshold adaptation predicted by membrane potential dynamics in vivo. PLoS computational biology, 10(4): e1003560. Fu, J.; Gou, S.; Wang, P.; Jiao, L.; Guo, Z.; Li, J.; and Liu, R. 2025. Adaptation and learning of spatio-temporal thresholds in spiking neural networks. Neurocomputing, 130423.

Guo, Y.; Chen, Y.; Zhang, L.; Liu, X.; Wang, Y.; Huang, X.; and Ma, Z. 2022a. IM-Loss: Information maximization loss for spiking neural networks. Advances in Neural Information Processing Systems, 35: 156–166. Guo, Y.; Tong, X.; Chen, Y.; Zhang, L.; Liu, X.; Ma, Z.; and Huang, X. 2022b. RecDis-SNN: Rectifying membrane potential distribution for directly training spiking neural networks. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 326–335. Guo, Y.; Zhang, Y.; Jie, Z.; Liu, X.; Tong, X.; Chen, Y.; Peng, W.; and Ma, Z. 2025. ReverB-SNN: Reversing bit of the weight and activation for spiking neural networks. In Forty-second International Conference on Machine Learning. Hasssan, A.; Meng, J.; and Seo, J.-S. 2024. Spiking neural network with learnable threshold for event-based classification and object detection. In 2024 International Joint Conference on Neural Networks (IJCNN), 1–8. Ioffe, S.; and Szegedy, C. 2015. Batch normalization: accelerating deep network training by reducing internal covariate shift. In International conference on machine learning, 448– 456. pmlr. Jiang, J.; Wang, L.; Jiang, R.; Fan, J.; and Yan, R. 2025. Adaptive gradient learning for spiking neural networks by exploiting membrane potential dynamics. In Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence. Ju, J.; Zheng, Y.; Koh, H. Y.; and Pan, S. 2025a. Uni-MRL: Unified MultiModal Molecular Representation Learning with Large Language Models and Graph Neural Networks. In Pacific-Asia Conference on Knowledge Discovery and Data Mining, 275–287. Springer. Ju, J.; Zheng, Y.; Koh, H. Y.; Wang, C.; and Pan, S. 2025b. M2LLM: Multi-view Molecular Representation Learning with Large Language Models. In IJCAI-25, 7437–7445. International Joint Conferences on Artificial Intelligence Organization. Lee, D.; Li, Y.; Kim, Y.; Xiao, S.; and Panda, P. 2025. Spiking transformer with spatial-temporal attention. In Proceedings of the Computer Vision and Pattern Recognition Conference, 13948–13958. Lian, S.; Shen, J.; Liu, Q.; Wang, Z.; Yan, R.; and Tang, H. 2023. Learnable surrogate gradient for direct training spiking neural networks. In Proceedings of the Thirty- Second International Joint Conference on Artificial Intelligence, 3002–3010. Liang, Y.; Wei, W.; Belatreche, A.; Cao, H.; Zhou, Z.; Wang, S.; Zhang, M.; and Yang, Y. 2025. Towards accurate binary spiking neural networks: learning with adaptive gradient modulation mechanism. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 1402–1410. Liu, W.; Yang, L.; Zhao, M.; Wang, S.; Gao, J.; Li, W.; Li, B.; and Hu, W. 2025. DeepTAGE: Deep temporalaligned gradient enhancement for optimizing spiking neural networks. In The Thirteenth International Conference on Learning Representations.

<!-- Page 9 -->

Maass, W. 1997. Networks of spiking neurons: the third generation of neural network models. Neural networks, 10(9): 1659–1671. Pena, J. L.; and Konishi, M. 2002. From postsynaptic potentials to spikes in the genesis of auditory spatial receptive fields. Journal of Neuroscience, 22(13): 5652–5658. Rathi, N.; and Roy, K. 2023. DIET-SNN: A low-latency spiking neural network with direct input encoding and leakage and threshold optimization. IEEE Transactions on Neural Networks and Learning Systems, 34(6): 3174–3182. Roy, K.; Jaiswal, A.; and Panda, P. 2019. Towards spikebased machine intelligence with neuromorphic computing. Nature, 575(7784): 607–617. Sun, H.; Cai, W.; Yang, B.; Cui, Y.; Xia, Y.; Yao, D.; and Guo, D. 2024. A synapse-threshold synergistic learning approach for spiking neural networks. IEEE Transactions on Cognitive and Developmental Systems, 16(2): 544–558. Wang, S.; Cheng, T. H.; and Lim, M.-H. 2022. LTMD: Learning improvement of spiking neural networks with learnable thresholding neurons and moderate dropout. Advances in Neural Information Processing Systems, 35: 28350–28362. Wang, S.; Cheng, T. H.; and Lim, M.-H. 2025. Potential distribution adjustment and parametric surrogate gradient in spiking neural networks. Neurocomputing, 620: 129189. Wang, S.; Zhang, M.; Zhang, D.; Belatreche, A.; Xiao, Y.; Liang, Y.; Shan, Y.; Sun, Q.; Zhang, E.; and Yang, Y. 2025. Spiking vision transformer with saccadic attention. In The Thirteenth International Conference on Learning Representations. Wang, Z.; Jiang, R.; Lian, S.; Yan, R.; and Tang, H. 2023. Adaptive smoothing gradient learning for spiking neural networks. In International conference on machine learning, 35798–35816. PMLR. Wei, W.; Zhang, M.; Zhou, Z.; Belatreche, A.; Shan, Y.; Liang, Y.; Cao, H.; Zhang, J.; and Yang, Y. 2025. QP- SNN: Quantized and pruned spiking neural networks. In The Thirteenth International Conference on Learning Representations. Wu, Y.; Deng, L.; Li, G.; Zhu, J.; and Shi, L. 2018. Spatiotemporal backpropagation for training high-performance spiking neural networks. Frontiers in neuroscience, 12: 331. Wu, Y.; Deng, L.; Li, G.; Zhu, J.; Xie, Y.; and Shi, L. 2019. Direct training for spiking neural networks: faster, larger, better. In Proceedings of the AAAI conference on artificial intelligence, volume 33, 1311–1318. Yan, J.; Wang, C.; Ma, D.; Tang, H.; Zheng, Q.; and Pan, G. 2025. Training high performance spiking neural network by temporal model calibration. In Forty-second International Conference on Machine Learning. Yu, C.; Zhao, X.; Liu, L.; Yang, S.; Wang, G.; Li, E.; and Wang, A. 2025a. Efficient logit-based knowledge distillation of deep spiking neural networks for full-range timestep deployment. In Forty-second International Conference on Machine Learning.

Yu, K.; Zhang, T.; Wang, H.; and Xu, Q. 2025b. FSTA-SNN: Frequency-based spatial-temporal attention module for spiking neural networks. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 22227–22235. Zhang, H.; Wu, B.; Yang, X.; Yuan, X.; Liu, X.; and Yi, X. 2025. Dynamic graph unlearning: a general and efficient post-processing method via gradient transformation. In Proceedings of the ACM on Web Conference 2025, 931–944. Zhang, H.; Yuan, X.; and Pan, S. 2024. Unraveling privacy risks of individual fairness in graph neural networks. In 2024 IEEE 40th International Conference on Data Engineering (ICDE), 1712–1725. IEEE. Zheng, H.; Wu, Y.; Deng, L.; Hu, Y.; and Li, G. 2021. Going deeper with directly-trained larger spiking neural networks. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 11062–11070.
