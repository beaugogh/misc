---
title: "M2FMoE: Multi-Resolution Multi-View Frequency Mixture-of-Experts for Extreme-Adaptive Time Series Forecasting"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39362
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39362/43323
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# M2FMoE: Multi-Resolution Multi-View Frequency Mixture-of-Experts for Extreme-Adaptive Time Series Forecasting

<!-- Page 1 -->

M2FMoE: Multi-Resolution Multi-View Frequency Mixture-of-Experts for

Extreme-Adaptive Time Series Forecasting

Yaohui Huang, Runmin Zou, Yun Wang*, Laeeq Aslam, Ruipeng Dong

School of Automation, Central South University, Changsha, China {yaohuihuang, rmzou, wangyun19, laeeq aslam, darol22}@csu.edu.cn

## Abstract

Forecasting time series with extreme events is critical yet challenging due to their high variance, irregular dynamics, and sparse but high-impact nature. While existing methods excel in modeling dominant regular patterns, their performance degrades significantly during extreme events, constituting the primary source of forecasting errors in real-world applications. Although some approaches incorporate auxiliary signals to improve performance, they still fail to capture extreme events’ complex temporal dynamics. To address these limitations, we propose M2FMoE, an extremeadaptive forecasting model that learns both regular and extreme patterns through multi-resolution and multi-view frequency modeling. It comprises three modules: (1) a multiview frequency mixture-of-experts module assigns experts to distinct spectral bands in Fourier and Wavelet domains, with cross-view shared band splitter aligning frequency partitions and enabling inter-expert collaboration to capture both dominant and rare fluctuations; (2) a multi-resolution adaptive fusion module that hierarchically aggregates frequency features from coarse to fine resolutions, enhancing sensitivity to both short-term variations and sudden changes; (3) a temporal gating integration module that dynamically balances long-term trends and short-term frequency-aware features, improving adaptability to both regular and extreme temporal patterns. Experiments on real-world hydrological datasets with extreme patterns demonstrate that M2FMoE outperforms stateof-the-art baselines without requiring extreme-event labels.

Code — https://github.com/Yaohui-Huang/M2FMoE

## Introduction

Time series forecasting is vital for decision-making across various real-world systems, including energy, transportation, and environmental monitoring (Jin et al. 2024; Wang et al. 2024b). Among these, hydrological forecasting is particularly difficult due to extreme events like flash floods, heavy rainfall, and sudden water level rises (Lavers, Pappenberger, and Zsoter 2014). These events are rare, abrupt, and high variance, often causing significant deviations from regular temporal patterns (Camps-Valls et al. 2025). Despite their importance for risk management, forecasting such extremes

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** Comparison of frequency spectra between regular and extreme events.

remains one of the most challenging problems in time series modeling (Li, Xu, and Anastasiu 2024).

Classical statistical models often fail under extreme or non-stationary conditions (Zhang 2003). Recent deep learning advancements offer enhanced flexibility in modeling intricate temporal dependencies (Wen et al. 2023; Wang et al. 2024b). However, these models typically emphasize capturing dominant patterns such as periodic trends, smooth transitions, and local correlations, resulting in the inadequate representation of rare, high-impact extreme events. Consequently, forecasting models tend to perform well under regular conditions but struggle to accurately represent these infrequent but critical dynamics. This limitation is especially pronounced in hydrological forecasting, where systems are highly sensitive to abrupt shifts, such as sudden heavy rainfall or rapid runoff (Li and Anastasiu 2025). Inaccurate predictions in such scenarios may lead to delayed warnings and severe consequences like widespread flooding. These challenges highlight the urgent need for forecasting models that can accurately capture both regular trends and extreme deviations within a unified framework.

Frequency-domain representations provide a promising way to decompose temporal dynamics into spectral components, facilitating models to separate high-frequency fluctuations from low-frequency trends (Ma et al. 2024; Liu 2025). The spectral characteristics of extreme and regular events

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22075

![Figure extracted from page 1](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

are shown in Fig.1. As illustrated in Fig.1(a)–(d), the differenced sequences ∆X reveal clear contrasts between the two types of events. These differences become more pronounced in the wavelet domain (Fig. 1(e), 1(g)), where extreme events produce sharp, localized energy at fine resolutions. As the resolution becomes coarser, energy gradually shifts toward lower frequencies with reduced intensity, while the main structure of the event remains consistent across resolutions. In contrast, regular events exhibit smooth lowfrequency dynamics, resulting in diffuse and uniform energy distributions at all resolutions. Similar patterns are observed in the Fourier domain (Fig. 1(f), 1(h)). Extreme sequences exhibit broad-spectrum, multi-peaked energy with slow spectral decay, whereas regular sequences concentrate energy within narrow low-frequency bands. These observations highlight the need for frequency-aware modeling to capture the varied spectral properties of temporal patterns. In particular, the results reveal frequency heterogeneity, where different frequency bands contribute unequally to regular and extreme events. Accurately modeling such variation requires adaptive focus on informative frequencies, which is challenging within a single spectral domain. Fourier transforms provide accurate global frequency information but lack temporal resolution. In contrast, wavelet transforms offer time-frequency localization but suffer from reduced resolution at lower frequencies (Fei et al. 2025). Combining both views yields a more complete spectral representation that supports the modeling of both abrupt variations and long-term dependencies. Nevertheless, this dual-view strategy also introduces cross-view spectral misalignment. Differences in basis functions and resolution cause the same signal to localize inconsistently across Fourier and Wavelet domains, resulting in cross-view incompatibility that undermines shared modeling.

To address this, we propose a Multi-resolution Multiview Frequency Mixture-of-Experts (M2FMoE) to model frequency-aware temporal dynamics under both regular and extreme conditions. Specifically, M2FMoE first proposes a multi-view frequency mixture-of-experts (MFMoE) module to assigns specialized spectral experts to distinct frequency bands across both Fourier and Wavelet domains, thereby enabling selective specialization to handle diverse frequency characteristics. To ensure semantic coherence among experts and alleviate spectral misalignment, a cross-view shared band splitter (CSS) is integrated within MFMoE, aligning spectral boundaries across views. Furthermore, to capture temporal patterns at multiple resolutions, we introduce the multi-resolution adaptive fusion (MAF) module, which hierarchically aggregates features from coarse to fine frequency scales. Finally, a temporal gating integration (TGI) module adaptively fuses recent dynamics with long-range historical context via a learnable gating mechanism. Experiments on five hydrological datasets with extreme events demonstrate that M2FMoE outperforms stateof-the-art methods without using auxiliary event labels.

## Related Work

Time series forecasting has evolved from classical models like ARIMA, which are interpretable but limited by linear- ity and stationarity (Zhang 2003; Wang et al. 2024b), to deep learning methods that offer greater flexibility. Early deep learning approaches, including RNNs (Jia et al. 2024; Kong et al. 2025) and CNNs (Wu et al. 2023; Chen, Jiang, and Gel 2023), focused on local dependencies. Transformers (Liu et al. 2025a, 2024; Kim et al. 2024) then introduced selfattention for long-range structure, while recent MLP-based models (Lin et al. 2025, 2024; Liu et al. 2025b) offer efficient alternatives. Further advancements include GNNs (Jin et al. 2024, 2025a) and Mixture-of-Experts (MoE) models (Liu 2025; Shi et al. 2025) for nonlinear modeling, alongside multi-scale and multi-resolution representations (Wang et al. 2025, 2024a) for capturing varied temporal granularities. Frequency-based approaches have also emerged, utilizing Fourier transforms for global periodic structures and wavelet transforms for localized time-frequency representations (Ma et al. 2024; Fei et al. 2025). However, most existing models primarily target regular patterns, struggling with the irregular variations crucial for extreme events.

Extreme-adaptive forecasting targets time series with rare, abrupt, and high-impact changes such as floods or sudden surges in water levels, which require effective handling of rarity and volatility. Recent efforts span architectural designs and loss functions. Architecturally, models such as NEC+ (Li, Xu, and Anastasiu 2023a), VIE (Xiu et al. 2021), SADI (Liu et al. 2023), and SEED (Li, Xu, and Anastasiu 2023b) use multi-phase learning for non-stationary dynamics. Others, like MCANN (Li and Anastasiu 2025) and DAN (Li, Xu, and Anastasiu 2024), integrate priors or clustering for enhanced robustness. On the loss side, specialized objectives like EPL (Wang, Han, and Guo 2024), EVL (Ding et al. 2019), and GEVL (Zhang et al. 2021) leverage Extreme Value Theory or biases to emphasize tail behavior. Despite these advancements, current extreme-adaptive methods often neglect the joint modeling of frequency-aware patterns and resolution-specific dynamics, limiting their generalization across diverse temporal variations.

## Preliminaries

Problem Statement Let X = {X1, X2,..., XTin} denote a multivariate time series, where each Xt ∈RC represents a C-dimensional observation at time step t, and Tin is the input sequence length. The objective is to learn a forecasting model F(·) that predicts the subsequent Tp future values, denoted as ˆX = { ˆXTin+1,..., ˆXTin+Tp}.

Discrete Fourier Transform (DFT) The discrete Fourier transform (DFT) decomposes a sequence into global sinusoidal components. For X of length Tin, its n-th frequency coefficient is:

Fn =

Tin X t=1

Xt·e−j2πnt/Tin, n ∈{0, 1,..., Tin−1}, (1)

where Fn encodes periodicity but lacks temporal localization, limiting its applicability for non-stationary signals. FFT is implemented to efficiently compute Fn.

Continuous Wavelet Transform (CWT) The CWT enables localized time-frequency analysis. For a signal X(t),

22076

<!-- Page 3 -->

the wavelet coefficient at scale a and position b is defined as:

W(a, b) = 1 p

|a|

Z ∞

−∞

X(t) ψ∗ t −b a dt, (2)

where ψ∗is the complex conjugate of the mother wavelet ψ.

## Methodology

As illustrated in Fig. 2, the proposed M2FMoE comprises three modules: (1) an MFMoE module, (2) an MAF module, and (3) a TGI module. Each component is detailed below.

Hierarchical Temporal Segmentation As shown in Fig. 2(a), the hierarchical temporal segmentation module extracts a recent segment Xr = {XTin−Tr+1,..., XTin} to capture short-term dynamics, while the entire input sequence X = {X1,..., XTin} serves as the historical context to model long-term temporal patterns.

Multi-Resolution Sequence Generation To capture temporal dynamics at varying granularities, the recent segment Xr ∈RTr×C is decomposed into a multi-resolution set via 1D smoothing convolutions:

S = n

˜X(k)

r = SmoothConv(Xr, k) | k ∈K o

. (3)

For each resolution k (with k1 = 1 retaining the original sequence), we compute the first-order difference of the transformed recent sequence to highlight local variations, i.e., ∆X(k)

r = ˜X(k)

r [1: Tr]−˜X(k)

r [0: Tr −1]. The resulting multi-resolution differences ∆X(k)

r disentangle coarse and fine dynamics, forming a diverse input set for subsequent frequency-aware modeling in the MFMoE module.

Temporal Embedding To encode temporal order, a fixed sinusoidal positional embedding is added as an auxiliary feature (Liu et al. 2024). Each time step is mapped to a combination of sine and cosine functions at varying frequencies:

PE(t, 2i) = sin(t · ωi), PE(t, 2i + 1) = cos(t · ωi), (4)

where t is the time index and d the embedding dimension, i is the index of the embedding dimension, and ωi = 1/100002i/d. These embeddings are added to input features to provide position-aware inductive bias across time steps.

Multi-View Frequency Mixture-of-Experts Module The recent segment of extreme time series is challenging due to the sparsity and volatility of extreme events. To address this, we shift the learning paradigm to the frequency domain via the MFMoE module, which comprises two expert branches: a Fourier-view and a Wavelet-view branch. A CSS is introduced to align frequency bands across both domains.

Cross-View Shared Band Splitter To capture multiresolution temporal dynamics, we construct dual-view spectral representations using both Fourier and Wavelet transforms. However, a key challenge arises from the inherent differences in these views. The Fourier transform organizes spectral components on a uniform frequency axis, while the

CWT uses scales that correspond nonlinearly to frequency. Consequently, aligning expert assignments between the two views is difficult, as the same frequency content can appear at different positions in each representation.

To ensure consistent expert specialization across both spectral views, we propose the Cross-View Shared Band Splitter. Theorem 1 provides the theoretical basis for this module by formalizing the correspondence between frequency and wavelet scale. As shown in Fig. 2(b), the splitter learns shared frequency boundaries {β1, β2,..., βE−1} to divide the frequency range [0, 1] into E bands. For the FFT view, these boundaries are directly scaled into frequency indices {˜β1,..., ˜βE−1}. For the CWT view, they are nonlinearly mapped into wavelet scales {¨β1,..., ¨βE−1} using the inverse relationship from Theorem 1. This shared segmentation allows both views to decompose the input into semantically aligned sub-bands, ensuring experts operate on consistent spectral content. Theorem 1 (Spectral Boundary Correspondence). Let f denote the normalized frequency, a is the scale in the CWT, and γ = f0/fnyq is a wavelet-dependent constant. The mapping a = γ/f establishes a one-to-one correspondence between frequency and scale boundaries (Mallat 2002), such that fmax 7→amin = γ/fmax and fmin 7→amax = γ/fmin. Under this mapping, signal energy is conserved, satisfying R fmax fmin |F(f)|2df ∝

RR a∈[amin,amax] |W(a, b)|2 da a2 db.

Fourier-View Expert Branch As illustrated in Fig. 2(c), the Fourier-view expert branch is designed to extract frequency-aware representations by assigning specialized experts to distinct frequency bands. Using the shared boundaries {˜β1,..., ˜βE−1}, we divide the full frequency range into E non-overlapping intervals (i.e., [0, ˜β1), [˜β1, ˜β2),..., [˜βE−1, F]), where F = Tr/2 + 1 is the number of frequency bins after real-valued FFT. Each expert e is responsible for modeling the frequency components within its assigned band, such as high-frequency, midfrequency, and low-frequency patterns.

Given an input sequence ∆X(k)

r ∈RTr×C, we first perform per-channel standardization and apply the real FFT. Then, to isolate expert-specific frequency components, we define a set of binary masks ˜Ie ∈RF ×C, each indicating the active sub-band for expert e. The masked spectrum for expert e is:

Fe = ˜Ie ⊙F, ˜Ie =

1, if f ∈[˜βe−1, ˜βe) 0, otherwise, (5)

where F represents the full spectrum generated by applying FFT to ∆X(k)

r. To adaptively determine expert contributions, inspired by (Jin et al. 2025b), we employ a lightweight routing network. Specifically, we first compute the magnitude spectrum and average across channels, and then the summary vector is passed through a routing network ˜G(·) consisting of two linear layers with ReLU activation and softmax output to produce the expert routing weights:

˜M = 1

C

XC c=1 |Fe[c]|, α = Softmax

˜G(˜M)

, (6)

22077

<!-- Page 4 -->

**Figure 2.** The proposed M2FMoE with three experts per branch for capturing high-, mid-, and low-frequency patterns.

where α = [α1,..., αE] are the routing weights for each expert. ˜M ∈RF is the magnitude spectrum averaged across channels. The final output of the Fourier-view expert branch is obtained by aggregating expert-specific frequency components using routing weights αe, followed by inverse FFT and a linear projection:

˜V = Linear

IFFT(

XE e=1 αe · Fe)

, (7)

where ˜V ∈RTp×C is the final output of the Fourier-view expert branch. This design enables dynamic selection of frequency bands and temporal adaptation based on input spectral statistics.

Wavelet-View Expert Branch As illustrated in Fig. 2(d), the Wavelet-view expert branch captures temporally localized dynamics by operating on the CWT power spectrogram P = |W(a, b)|2 ∈RC×S×Tr, where S is the number of wavelet scales. The CWT is computed using the complex Gaussian wavelet, ensuring balanced localization in both time and frequency domains.

The shared frequency boundaries are first converted to scale indices {¨β1,..., ¨βE−1} via the inverse mapping defined in Theorem 1. Each expert e is assigned a binary scale mask Ie ∈{0, 1}S, and its corresponding component is computed as:

Pe = ¨Ie ⊙P, ¨Ie =

1, if s ∈[¨βe−1, ¨βe), 0, otherwise. (8)

Each expert network processes its masked input Pe using a convolutional block:

¨Ze = We,2 ∗

D

ReLU (We,1 ∗Pe)

, (9)

where ∗denotes the convolution operation, We,1, We,2 are convolution kernels, and the dropout layer D(·) is applied after the activation to prevent overfitting.

To adaptively assign expert contributions, the power spectrogram P is first averaged over the channel dimension to obtain a global summary ¨M ∈RS×Tr. This matrix is then flattened and passed through a lightweight routing network

¨G(·), which consists of two linear layers with ReLU activation, followed by a softmax function to produce the expert weighting vector:

¨M = 1

C

XC c=1 P[c], η = Softmax

¨G

Flatten(¨M)

, (10) where η represents the soft assignment weights over the E experts for a given input. The final output is obtained via gated aggregation of expert outputs, followed by two linear layers to project the result to the target shape:

¨V = Wo,1

Wo,2

Flatten

XE e=1 ηe · ¨Ze

⊤!

,

(11) where Wo,1, Wo,2 are learnable weighting matrices, and

¨V ∈RTp×C is the final output of the Wavelet-view expert branch. ηe ∈R is the gating weight for expert e.

Multi-Resolution Adaptive Fusion Module The MAF module consists of two key phases: (1) a multiview fusion phase and (2) a multi-resolution fusion phase, as illustrated in Fig. 2(e).

In the multi-view fusion phase, the temporal outputs from the Fourier and Wavelet expert branches, denoted as

22078

![Figure extracted from page 4](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

{ ˜V, ¨V} ∈RTp×C, are concatenated along the channel axis with temporal encoding E ∈RTp×2. Then, the fused representation is processed by a stacked projection block with two linear layers and batch normalization:

H(i)

u = Wu,2·D

ReLU

BN

Wu,1[ ˜V(i); ¨V(i); E]⊤

, (12) where Wu,1 ∈RH′×(2C+2) and Wu,2 ∈RC×H′ are learnable weights; H′ is the hidden dimension; BN(·) denotes batch normalization; and [·; ·] indicates channel-wise concatenation. The output H(i)

u ∈RTp×C represents the unified feature at the i-th resolution, with i ∈{1, 2,..., R}, where R is the total number of resolutions.

In the multi-resolution fusion phase, representations from different resolutions are projected into a shared space and combined via additive accumulation:

Hr =

XR i=1 Lineari(H(i)

u) ∈RTp×C, (13)

where Lineari(·) is a resolution-specific linear transformation. Since all frequency-view representations are learned from differenced sequences, the final fused output is shifted by adding back the last observed input slice to restore the original value space. This process enables coarse-to-fine feature refinement and enhances the integration of multi-scale temporal dynamics.

Temporal Gating Integration Module The TGI module adaptively combines the recent prediction and historical scene representation to produce the final output, as illustrated in Fig. 2(f). To adaptively integrate the recent prediction and the historical scene representation, a gating mechanism is applied. Let Hr ∈RTp×C denote the output from the multi-resolution fusion module, and Hh ∈RTp×C be the transformed embedding of the historical input, obtained via a linear projection Hh ←WgX with Wg ∈RTin×Tp. The gating coefficient is computed as:

G = σ (Linear ([Hr; Hh])), (14) ˆX = G ⊙Hr + (1 −G) ⊙Hh, (15)

where σ(·) denotes the sigmoid activation. ˆX ∈RTp×C is the final output of the model.

Optimization Objective The overall objective of M2FMoE consists of three components. The primary term is the forecasting loss Lpred, measured by Mean Squared Error (MSE). To promote diverse specialization within each branch and ensure consistency across branches, we introduce a regularization term comprising the expert diversity loss Ldiv and expert consistency loss Lcons:

Ldiv = s

1 E

XE e=1

∥Ze∥2 −1

E

XE j=1 ∥Zj∥2

2

, (16)

Lcons = 1

E

XE e=1

1 −cossim

˜Ze, ¨Ze

, (17)

where Ze ∈{˜Ze, ¨Ze} is the output of the e-th expert in either the Fourier-view or Wavelet-view expert branch, ∥· ∥2 denotes the ℓ2 norm, and cossim(·, ·) denotes the cosine similarity function. Here, ˜Ze indicates the inverse FFT of the masked frequency component Fe for the e-th expert, and ¨Ze is the output of the e-th expert in the Wavelet-view expert branch. The expert diversity loss Ldiv encourages the outputs of different experts to be diverse, while the expert consistency loss Lcons encourages the outputs of the same expert in different branches to be consistent. Finally, the overall optimization objective is defined as:

Ltotal = Lpred + λLdiv + µLcons, (18)

where λ and µ are hyperparameters that control the trade-off between the forecasting loss and the regularization terms.

## Experiments

Experimental Settings Datasets The experiment uses five public datasets containing hourly water level records from reservoirs in Santa Clara County, California. The datasets include Almaden, Coyote, Lexington, Stevens Creek, and Vasona, spanning the period from 1991 to 2019. Following the experimental protocol of (Li and Anastasiu 2025), the training and validation sets are randomly sampled from data between January 1991 and June 2018. The forecasting task targets the period from July 2018 to June 2019. To alleviate the data imbalance, we employed the same oversampling strategy as described in (Li and Anastasiu 2025).

Benchmarks To ensure a comprehensive evaluation, nine representative state-of-the-art baselines are selected: attention-based models (CATS (Kim et al. 2024), TQNet (Lin et al. 2025), iTransformer (iTrans.) (Liu et al. 2024)), frequency-domain models (FreqMoE (Liu 2025), Umixer (Ma et al. 2024)), linear-based models (KAN (Liu et al. 2025b), CycleNet (Lin et al. 2024)), and two extremeenhanced methods that leverage event labels (DAN (Li, Xu, and Anastasiu 2024), MCANN (Li and Anastasiu 2025)).

Implementation Details For fair evaluation, the optimal configurations from the official implementations of MCANN and DAN are adopted. Following the experimental protocol in (Li and Anastasiu 2025), the prediction horizons are set to 8 and 72 hours, with a look-back window of 360 hours (i.e., 15 days). For other methods, standard baseline practices are followed: all datasets are normalized using zscore normalization, and denormalization is applied during evaluation to ensure predictions are in the original scale. The models are trained using the Adam (Kingma and Ba 2015) optimizer with a batch size of 48. Following the official protocol, evaluation is performed using Root Mean Squared Error (RMSE) and Mean Absolute Percentage Error (MAPE).

Main Results Comparison with Benchmarks As shown in Table 1, we compare the proposed M2FMoE model with nine state-ofthe-art baselines on five reservoirs with prediction horizons of 8 and 72 hours. The results demonstrate that M2FMoE

22079

<!-- Page 6 -->

Data Metrics Horizon without extreme lables with extreme lables

M2FMoE CATS CycleNet FreqMoE iTrans. KAN TQNet Umixer DAN MCANN

Almaden

RMSE

8 7.990 16.087 17.754 14.729 32.127 18.934 18.023 18.658 37.857 8.447 MAPE 0.002 0.006 0.007 0.005 0.017 0.009 0.010 0.007 0.021 0.002

RMSE

72 54.120 57.916 61.379 63.038 65.325 70.181 59.427 64.816 66.597 56.840 MAPE 0.015 0.015 0.019 0.017 0.025 0.033 0.018 0.018 0.025 0.015

Coyote

RMSE

8 48.797 110.849 113.706 593.141 372.523 116.398 103.521 174.892 505.941 86.829 MAPE 0.002 0.004 0.003 0.018 0.022 0.005 0.003 0.005 0.025 0.002

RMSE

72 449.944 509.077 528.962 855.096 673.853 587.132 504.606 566.429 829.623 559.747 MAPE 0.012 0.012 0.012 0.025 0.029 0.021 0.012 0.013 0.042 0.012

Lexington

RMSE

8 251.957 618.991 463.293 386.995 690.426 429.054 400.991 466.669 476.936 252.965 MAPE 0.004 0.011 0.011 0.006 0.041 0.008 0.013 0.008 0.015 0.003

RMSE

72 772.836 906.531 865.092 1003.818 960.652 956.134 860.456 829.541 908.308 778.023 MAPE 0.014 0.020 0.021 0.018 0.048 0.020 0.025 0.018 0.024 0.015

Stevens

Creek

RMSE

8 10.559 18.500 28.400 80.937 48.876 25.672 24.475 37.654 24.319 12.130 MAPE 0.002 0.004 0.005 0.017 0.010 0.005 0.006 0.007 0.011 0.002

RMSE

72 76.939 82.739 94.578 117.282 106.606 94.034 89.265 141.505 82.794 81.084 MAPE 0.014 0.011 0.014 0.025 0.017 0.015 0.012 0.017 0.020 0.011

Vasona

RMSE

8 5.129 6.913 7.903 14.318 12.179 11.308 7.741 9.299 9.562 5.353 MAPE 0.004 0.007 0.007 0.020 0.013 0.019 0.007 0.009 0.012 0.004

RMSE

72 19.571 20.381 20.713 20.740 21.534 21.605 20.173 23.718 20.542 18.634 MAPE 0.021 0.021 0.021 0.027 0.023 0.027 0.020 0.023 0.023 0.019

Average Rank / Significance 1.4 3.7 / ⋆ 4.9 / ∗ 7.3 / ∗ 8.5 / ∗ 7.0 / ∗ 4.4 / ∗ 6.3 / ∗ 7.9 / ∗ 1.7 / ⋆

**Table 1.** Performance comparison on five reservoirs with predicted length as {8, 72} hours. ∗: both metrics are statistically significant (p < 0.05, Wilcoxon signed-rank test); ⋆: indicates significance in RMSE. Best results are bold, second-best underlined.

**Figure 3.** Prediction results and expert weights of M2FMoE.

achieves the best average rank across all datasets and prediction horizons, outperforming all baselines in most cases. The improvements in RMSE are statistically significant on all reservoirs according to the Wilcoxon signed-rank test. Specifically, M2FMoE achieves the average improvement of 22.30% over the best baseline without extreme labels and the maximum RMSE improvement of 52.86% on the Coyote dataset with a prediction horizon of 8 hours. Compared to the baselines with extreme labels, M2FMoE also achieves competitive performance, with an average RMSE improvement of 9.19% across all settings, and a maximum improvement of 43.8% on the Coyote dataset with a prediction horizon of 8 hours. These results indicate that the proposed M2FMoE model effectively captures the complex temporal dynamics of reservoir water levels, demonstrating its superiority over existing methods. Fig. 3 presents the prediction results and expert weights of M2FMoE, using three experts under two temporal resolutions (k=1 and k=24). The results show that Fourier-view experts primarily capture lowfrequency trends, while Wavelet-view experts provide complementary high-frequency details. The adaptive weighting mechanism dynamically adjusts expert contributions based on input characteristics, improving M2FMoE’s performance on both regular and extreme events.

Ablation Studies We conduct ablation studies to evaluate the effectiveness of each component in the proposed M2FMoE model. The ablation experiments are performed on the five reservoirs with a prediction horizon of 72 hours. The results are summarized in Table 2. The ablation studies include the following variants: (1) w/o- WaveletView: removes the Wavelet-view expert branch, (2) w/o-FourierView: removes the Fourier-view expert branch, (3) w/o-Ldiv & Lcons: removes the expert diversity and consistency losses, (4) w/o-Multi-Res: utilizes the singleresolution and removes the multi-resolution fusion module,

22080

![Figure extracted from page 6](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Model

Almaden Coyote Lexington Stevens Creek Vasona

RMSE MAPE RMSE MAPE RMSE MAPE RMSE MAPE RMSE MAPE

M2FMoE 54.120 0.015 449.944 0.012 772.836 0.014 76.939 0.014 19.571 0.021 w/o-WaveletView 57.697 0.016 555.641 0.014 827.392 0.016 87.194 0.016 19.836 0.022 w/o-FourierView 59.035 0.020 558.262 0.014 870.735 0.017 85.022 0.017 19.813 0.024 w/o-Ldiv & Lcons 54.950 0.017 448.150 0.013 826.408 0.015 77.293 0.012 20.080 0.021 w/o-Multi-Res 59.479 0.017 483.223 0.013 855.236 0.017 85.004 0.017 19.508 0.022 w/o-CSS 55.575 0.017 541.594 0.013 916.925 0.016 85.997 0.019 20.001 0.021

**Table 2.** Ablation study results on the five reservoirs with a prediction horizon of 72 hours.

**Figure 4.** Impact of the length of recent segment Tr/Tin.

**Figure 5.** Impact of the number of experts E.

and (5) w/o-CSS: replace the cross-view shared band splitter with a uniform band splitter. We observe that the full model achieves the optimal performance across almost all datasets, demonstrating the effectiveness of the proposed multi-view and multi-resolution fusion strategy.

Impact of the Recent Segment Length The length of the recent segment critically affects the model’s ability to capture extreme events. As shown in Fig. 4, reducing its length appropriately improves prediction accuracy by emphasizing relevant information. However, removing it entirely causes a significant performance drop, while overly long segments introduce noise and weaken the model’s focus on extremes.

Impact of the Number of Experts We further examined the impact of expert count in M2FMoE. As shown in Fig. 5, increasing the number of experts may improve pattern diversity but can also introduce noise and overfitting, leading to performance instability. Results suggest that using a moderate number (e.g., 3 or 4) yields the best predictive accuracy.

Visualization Analysis To better interpret the feature representations learned by M2FMoE, the t-SNE (Maaten and Hinton 2008) is employed to visualize expert embeddings trained on the Almaden dataset using three spectral experts corresponding to high-, mid-, and low-frequency bands, as shown in Fig. 6. The visualizations reveal the following insights: (1) In the Fourier view, low-frequency features form

**Figure 6.** The t-SNE visualization of feature representations.

a well-separated cluster from mid- and high-frequency features, indicating its effectiveness in capturing global trends. (2) The Wavelet view exhibits clearer separation between mid- and high-frequency features, suggesting superior sensitivity to localized, sparse patterns. (3) The cross-view distribution highlights the complementary nature of the two spectral views, with distinct clustering structures in each domain. (4) The cross-resolution view demonstrates that the multi-resolution fusion module maintains consistency while also capturing local variations. These results validate the proposed multi-view and multi-resolution strategy for effectively modeling diverse temporal patterns.

## Conclusion

This study proposes M2FMoE, an extreme-adaptive time series forecasting model that leverages multi-view frequency learning and multi-resolution fusion to capture both global trends and local extreme variations. Specifically, M2FMoE employs specialized Fourier- and Wavelet-based experts to extract multi-frequency representations, while a multiresolution fusion module progressively integrates temporal dependencies across resolutions. The model is optimized using forecasting, diversity, and consistency losses to promote adaptive and complementary expert behavior. Experiments on five reservoir datasets show that M2FMoE outperforms state-of-the-art methods without using extreme event labels.

22081

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-m2fmoe-multi-resolution-multi-view-frequency-mixture-of-experts-for-extreme-adap/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by the National Natural Science Foundation of China under Grant 62376289, in part by the Natural Science Foundation of Hunan Province, China under Grant 2024JJ4069, and in part supported by the Fundamental Research Funds for the Central Universities of Central South University.

## References

Camps-Valls, G.; Fern´andez-Torres, M.- ´A.; Cohrs, K.-H.; H¨ohl, A.; Castelletti, A.; Pacal, A.; Robin, C.; Martinuzzi, F.; Papoutsis, I.; Prapas, I.; et al. 2025. Artificial intelligence for modeling and understanding extreme weather and climate events. Nature Communications, 16(1): 1919.

Chen, Y.; Jiang, T.; and Gel, Y. R. 2023. H2-Nets: Hyper-hodge Convolutional Neural Networks for Time- Series Forecasting. In Proceedings of the Joint European Conference on Machine Learning and Knowledge Discovery in Databases, volume 14173, 271–289. Turin, Italy: Springer. Ding, D.; Zhang, M.; Pan, X.; Yang, M.; and He, X. 2019. Modeling Extreme Events in Time Series Prediction. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1114–1122. Anchorage, AK, USA: Association for Computing Machinery. Fei, J.; Yi, K.; Fan, W.; Zhang, Q.; and Niu, Z. 2025. Amplifier: Bringing Attention to Neglected Low-Energy Components in Time Series Forecasting. In Proceedings of the 39th AAAI Conference on Artificial Intelligence, volume 39, 11645–11653. Jia, Y.; Lin, Y.; Yu, J.; Wang, S.; Liu, T.; and Wan, H. 2024. PGN: The RNN’s New Successor is Effective for Long- Range Time Series Forecasting. In Proceedings of the 38th Annual Conference on Neural Information Processing Systems. Vancouver, BC, Canada. Jin, M.; Koh, H. Y.; Wen, Q.; Zambon, D.; Alippi, C.; Webb, G. I.; King, I.; and Pan, S. 2024. A Survey on Graph Neural Networks for Time Series: Forecasting, Classification, Imputation, and Anomaly Detection. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(12): 10466– 10485. Jin, M.; Shi, G.; Li, Y.-F.; Xiong, B.; Zhou, T.; Salim, F. D.; Zhao, L.; Wu, L.; Wen, Q.; and Pan, S. 2025a. Towards Expressive Spectral-Temporal Graph Neural Networks for Time Series Forecasting. IEEE Transactions on Pattern Analysis and Machine Intelligence, 47(6): 4926–4939. Jin, P.; Zhu, B.; Yuan, L.; and Yan, S. 2025b. MOH: Multihead attention as mixture-of-head attention. In ICML. Kim, D.; Park, J.; Lee, J.; and Kim, H. 2024. Are selfattentions effective for time series forecasting? In Proceedings of the 38th Annual Conference on Neural Information Processing Systems, 114180–114209. Kingma, D. P.; and Ba, J. 2015. Adam: A Method for Stochastic Optimization. In Proceedings of the 3rd International Conference on Learning Representations. San Diego, CA, USA.

Kong, Y.; Wang, Z.; Nie, Y.; Zhou, T.; Zohren, S.; Liang, Y.; Sun, P.; and Wen, Q. 2025. Unlocking the Power of LSTM for Long Term Time Series Forecasting. In Proceedings of the 39th AAAI Conference on Artificial Intelligence, 11968– 11976. Philadelphia, PA, USA. Lavers, D. A.; Pappenberger, F.; and Zsoter, E. 2014. Extending medium-range predictability of extreme hydrological events in Europe. Nature Communications, 5(1): 5382. Li, Y.; and Anastasiu, D. C. 2025. MC-ANN: A Mixture Clustering-Based Attention Neural Network for Time Series Forecasting. IEEE Transactions on Pattern Analysis and Machine Intelligence, 47(8): 6888–6899. Li, Y.; Xu, J.; and Anastasiu, D. 2024. Learning from polar representation: An extreme-adaptive model for long-term time series forecasting. In Proceedings of the 38th AAAI Conference on Artificial Intelligence, 1, 171–179. Vancouver, Canada. Li, Y.; Xu, J.; and Anastasiu, D. C. 2023a. An Extreme-Adaptive Time Series Prediction Model Based on Probability-Enhanced LSTM Neural Networks. In Proceedings of the 37th AAAI Conference on Artificial Intelligence, 7, 8684–8691. Washington, DC, USA. Li, Y.; Xu, J.; and Anastasiu, D. C. 2023b. SEED: An Effective Model for Highly-Skewed Streamflow Time Series Data Forecasting. In Proceedings of the 2023 IEEE International Conference on Big Data, 728–737. Sorrento, Italy: IEEE. Lin, S.; Chen, H.; Wu, H.; Qiu, C.; and Lin, W. 2025. Temporal Query Network for Efficient Multivariate Time Series Forecasting. In Proceedings of the 42nd International Conference on Machine Learning. Lin, S.; Lin, W.; Hu, X.; Wu, W.; Mo, R.; and Zhong, H. 2024. CycleNet: Enhancing Time Series Forecasting through Modeling Periodic Patterns. In Proceedings of the 38th Annual Conference on Neural Information Processing Systems, 106315–106345. Vancouver, BC, Canada: Curran Associates, Inc. Liu, H.; Ma, Z.; Yang, L.; Zhou, T.; Xia, R.; Wang, Y.; Wen, Q.; and Sun, L. 2023. SADI: A Self-Adaptive Decomposed Interpretable Framework for Electric Load Forecasting Under Extreme Events. In Proceedings of the ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing, 1–5. Rhodes Island, Greece. Liu, Y.; Hu, T.; Zhang, H.; Wu, H.; Wang, S.; Ma, L.; and Long, M. 2024. itransformer: Inverted transformers are effective for time series forecasting. In Proceedings of the 12th International Conference on Learning Representations. Vienna, Austria. Liu, Y.; Qin, G.; Huang, X.; Wang, J.; and Long, M. 2025a. Timer-XL: Long-Context Transformers for Unified Time Series Forecasting. In Proceedings of the 13th International Conference on Learning Representations. Singapore. Liu, Z. 2025. FreqMoE: Enhancing Time Series Forecasting through Frequency Decomposition Mixture of Experts. In Li, Y.; Mandt, S.; Agrawal, S.; and Khan, E., eds., Proceedings of the 28th International Conference on Artificial Intelligence and Statistics, volume 258, 3430–3438. PMLR.

22082

<!-- Page 9 -->

Liu, Z.; Wang, Y.; Vaidya, S.; Ruehle, F.; Halverson, J.; Soljaˇci´c, M.; Hou, T. Y.; and Tegmark, M. 2025b. Kan: Kolmogorov-arnold networks. In Proceedings of the 13th International Conference on Learning Representations. Singapore. Ma, X.; Li, X.; Fang, L.; Zhao, T.; and Zhang, C. 2024. U-mixer: An unet-mixer architecture with stationarity correction for time series forecasting. In Proceedings of the 38th AAAI conference on Artificial Intelligence, 13, 14255– 14262. Maaten, L. v. d.; and Hinton, G. 2008. Visualizing data using t-SNE. Journal of Machine Learning Research, 9: 2579– 2605. Mallat, S. G. 2002. A theory for multiresolution signal decomposition: the wavelet representation. IEEE Transactions on Pattern Analysis and Machine Intelligence, 11(7): 674– 693. Shi, X.; Wang, S.; Nie, Y.; Li, D.; Ye, Z.; Wen, Q.; and Jin, M. 2025. Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of Experts. In Proceedings of the 13th International Conference on Learning Representations. Singapore. Wang, S.; Li, J.; Shi, X.; Ye, Z.; Mo, B.; Lin, W.; Ju, S.; Chu, Z.; and Jin, M. 2025. Timemixer++: A general time series pattern machine for universal predictive analysis. In Proceedings of the 13th International Conference on Learning Representations. Singapore. Wang, S.; Wu, H.; Shi, X.; Hu, T.; Luo, H.; Ma, L.; Zhang, J. Y.; and ZHOU, J. 2024a. TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting. In Proceedings of the 12th International Conference on Learning Representations. Vienna, Austria. Wang, Y.; Han, Y.; and Guo, Y. 2024. Self-adaptive Extreme Penalized Loss for Imbalanced Time Series Prediction. In Proceedings of the 33rd International Joint Conference on Artificial Intelligence, 5135–5143. Jeju, South Korea. Wang, Y.; Wu, H.; Dong, J.; Liu, Y.; Long, M.; and Wang, J. 2024b. Deep time series models: A comprehensive survey and benchmark. arXiv preprint arXiv:2407.13278. Wen, Q.; Zhou, T.; Zhang, C.; Chen, W.; Ma, Z.; Yan, J.; and Sun, L. 2023. Transformers in Time Series: A Survey. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence, 6778–6786. ijcai.org. Wu, H.; Hu, T.; Liu, Y.; Zhou, H.; Wang, J.; and Long, M. 2023. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis. In Proceedings of the 11th International Conference on Learning Representations. Kigali, Rwanda. Xiu, Z.; Tao, C.; Gao, M.; Davis, C.; Goldstein, B. A.; and Henao, R. 2021. Variational disentanglement for rare event modeling. In Proceedings of the 35th AAAI Conference on Artificial Intelligence, 12, 10469–10477. Zhang, G. P. 2003. Time series forecasting using a hybrid ARIMA and neural network model. Neurocomputing, 50: 159–175.

Zhang, M.; Ding, D.; Pan, X.; and Yang, M. 2021. Enhancing time series predictors with generalized extreme value loss. IEEE Transactions on Knowledge and Data Engineering, 35(2): 1473–1487.

22083
