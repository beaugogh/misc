---
title: "METP: Multi-Granularity Integration of External Covariates for Temporal Point Processes"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39448
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39448/43409
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# METP: Multi-Granularity Integration of External Covariates for Temporal Point Processes

<!-- Page 1 -->

METP: Multi-Granularity Integration of External Covariates for Temporal Point

Processes

Boyang Li1*, Lingzheng Zhang2*, Fugee Tsung3†, Xi Zhang1†

1Peking University, Beijing, China 2The Hong Kong University of Science and Technology (GZ), Guangzhou, China 3The Hong Kong University of Science and Technology, Hong Kong, China 2101112018@stu.pku.edu.cn, lingzhengzhang01@gmail.com, season@ust.hk, xi.zhang@pku.edu.cn

## Abstract

Accurate modeling of temporal point processes is critical for reliable event forecasting and informed decision-making. While historical event sequences provide a foundation for intensity estimation, existing approaches often neglect external covariates whose lagged effects impact future intensities across multiple temporal granularities. To address this gap, we propose Multi-Granularity Integration of External Covariates for Temporal Point Processes (METP), a framework for incorporating lagged external influences into intensity modeling. METP extracts periodic structures and decomposes external covariate series into multiple temporal granularities. At each granularity, a lag-aware calibration module is introduced to align covariates with event dynamics. Finally, a hierarchical mixture-of-experts strategy is employed to integrate the multi-granular external covariates with historical event embeddings, enabling a representation of the conditional intensity function with enhanced information. Extensive experiments on public and proprietary datasets demonstrate that METP consistently outperforms existing methods in predictive accuracy.

Extended version — https://github.com/lbylbylby123456/AAAI-METP

## Introduction

Temporal Point Processes (TPPs) have emerged as a powerful mathematical framework for modeling stochastic event sequences in continuous time (Gu 2021). Their versatility is demonstrated by successful applications across diverse domains, including e-commerce systems (Boyd et al. 2020), social network analysis (Karpukhin, Shipilov, and Savchenko 2024), and clinical informatics (Xiao et al. 2025). The integration of deep learning methodologies has significantly advanced TPP modeling, with neural networkbased approaches offering enhanced capabilities for capturing complex temporal patterns (Shou et al. 2023). By leveraging the nonlinear approximation capacity of neural architectures, these models capture complex temporal dependencies from historical events, enabling more accurate pre-

*These authors contributed equally. †Corresponding authors. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

diction of future event intensities (Gracious and Dukkipati 2025). Despite the promising performance of existing methods in event prediction, many TPP models pay insufficient attention to external temporal covariates (Zuo et al. 2020; Zhang et al. 2020; Meng et al. 2024) and neglect their lagged effects on event intensities (Shams Eddin and Gall 2024), as illustrated in Fig. 1(b). Given that these covariates frequently correlate with events, neglecting them can lead to missed key dependencies, resulting in inaccurate intensity estimation and biased event time prediction. Incorporating external variables is therefore essential for enhancing predictive accuracy. Moreover, external temporal variables sometimes exhibit periodic patterns, which form a fundamental aspect of temporal modeling (Li et al. 2021a) and play a critical role in diverse applications such as consumption forecasting (Lin et al. 2024), healthcare prediction (Xiao et al. 2025), and industrial prognostics (Chen et al. 2025). To capture these periodicities, existing methods typically employ Fourier transforms to extract dominant frequency components (Mu, Shahzad, and Zhu 2025), analyzing subsequences of the original series for subsequent modeling tasks. However, relying solely on the original subsequences often results in limited expressiveness, not accounting for the necessity to model both long-term trends and short-term fluctuations, which are essential factors influencing event intensities. This limitation highlights the need to effectively model periodic patterns across multiple temporal granularities and to integrate their combined influences.

Furthermore, although some studies attempt to analyze the influence of external variables, these models often do not account for the lagged effects of external series (Zhang et al. 2024a). In real-world scenarios, such factors typically evolve asynchronously with event sequences, leading to temporal misalignments that challenge conventional modeling frameworks (Zhang et al. 2023; Kuang et al. 2024). Recent methods typically employ the time point within a fixed-length period before the event to approximate such lag effects (Shams Eddin and Gall 2024). However, they often neglect the decay influence of historical time series at different time points on current events. In addition, the absence of mechanisms for capturing periodic structures and multi-granularity temporal variations restricts their capacity to represent the dynamic heterogeneity of external influ-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

22850

<!-- Page 2 -->

(a) External Series

Event Intensity

Future

Event

Time

Time Lagged

Effect

Time

Historical Events

Predicted

Time

History

(b) Normal TPP, e.g., SAHP, THP

(c) METP

**Figure 1.** Comparison of Normal TPP and METP in Event Time Prediction with Lagged Effects.

ences. Compounding this issue is the unavailability of future environmental time series, making it difficult to align historical covariates with long-term event forecasting. These challenges highlight the need for advanced models that can dynamically synchronize historical external series with event processes while capturing their multi-granular dependencies to improve prediction accuracy.

To address these limitations, we propose a novel framework, Multi-Granularity Integration of External Covariates in Temporal Point Processes (METP), which incorporates external series more effectively than standard approaches, as illustrated in Fig. 1(c). The method integrates periodic patterns from external sequences across multiple temporal granularities. By aligning the weights of a causal selfattention mechanism with a prior reversed geometric distribution, it adaptively models the lagged effects of external covariates at each granularity. Finally, a hierarchical mixtureof-experts (MoE) framework integrates the multi-granular external covariates with historical event sequence embeddings, leading to significant improvements in event intensity forecasting accuracy. The key contributions of this work are summarized as follows:

• We propose a multi-granularity, periodicity-aware attention architecture. It models the lagged effects of external covariates on event occurrence by aligning the distributions of reversed geometric priors and causal attention scores. To the best of our knowledge, this is the first method that enables adaptive alignment of lagged effects in temporal point processes. • We integrate historical external covariates through a hierarchical granular mixture-of-experts strategy, combined with historical event embeddings to predict future event intensities. • Experiments on a proprietary dataset and three public benchmarks demonstrate consistent improvements, validating the robustness and generalizability of the proposed framework.

## Related Work

Temporal Point Process Methods Temporal Point Processes (TPP) provide a probabilistic framework for modeling discrete event sequences in continuous time. Traditional parametric models, such as the Hawkes process (Hawkes 1971), employ parametric and stationary intensity functions, which limit their ability to capture complex and dynamic temporal dependencies. To overcome these limitations, recent approaches have introduced neural TPP models that leverage data-driven architectures to capture intricate temporal dependencies. RMTPP (Du et al. 2016) integrates recurrent neural networks with TPP to learn irregular temporal structures. IFTPP (Shchur, Biloˇs, and G¨unnemann 2019) eliminates the need for explicit intensity functions by using normalizing flows to directly model inter-event time distributions.

With the rise of attention-based mechanisms, THP (Zuo et al. 2020) introduces a Transformer-based self-attention structure to capture both short- and long-range dependencies. FTHP (Isik et al. 2023) further replaces standard attention with learnable triggering kernels and gating functions to enhance modeling effectiveness and interpretability. To address the distinct characteristics of short- and long-term prediction tasks, HoTPP (Karpukhin, Shipilov, and Savchenko 2024) introduces a long-horizon forecasting benchmark and proposes a new evaluation metric (T-mAP). ITHP (Meng et al. 2024) extends Transformer Hawkes models with nonlinear inter-type interaction modeling for improved interpretability. TPP-Gaze (D’Amelio et al. 2025) incorporates spatial-temporal attention for modeling visual attention dynamics in eye movement sequences. Despite these advancements in modeling internal event dependencies, challenges remain in effectively leveraging external covariates. In practice, these external variables often exhibit periodic behaviors (Lin et al. 2024). Their influences on event dynamics manifest through both long-term trends and short-term perturbations across multiple temporal granularities (Li et al. 2021a). They also tend to produce lagged and temporally misaligned effects, which are difficult to capture using static lag structures.

Most existing models do not explicitly model complex lagged effects, which lead to an incomplete representation of the dynamic heterogeneity and multi-granular temporal structures commonly observed in real-world scenarios. As a result, the absence of effective mechanisms for incorporating external information continues to limit the predictive accuracy and generalizability of current TPP frameworks.

Misalignment between Covariate and Event Temporal misalignment is a fundamental challenge in time series modeling, where outputs are influenced not only by concurrent inputs but also by temporally lagged signals. Recent studies have proposed solutions such as hierarchical latent space decomposition (Li et al. 2021b), attentionbased inter-feature delay modeling (Dai et al. 2024), and component-wise attention normalization (Deng et al. 2024). For irregular time series, asynchronous graph diffusion (Zhang et al. 2024c) and transformable time-aware convo-

22851

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-002-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

External Covariate Series

Position Encoding

Segments

Period

Multi-Granularity

Event Embedding

RGeo

Attention Scores

Softplus

Prediction

Scale

SoftMax

Fourier-Based Periodicity Detection

Hierarchical Granular MoE

Multi- Granularity Embedding

Historical Series 1 K

Periodic Encoding

Length

Scale 1 K t n

FFN 2 Router

FFN K

Output

Layer

Linear Projection in Inner Loop

Fine Granularity

Coarse Granularity

Series Weights

Current

Time concat Intensity

Loss

T

History

Event

Prediction

(a) Periodicity and Multi-Granular (b) Lagged Effect Distribution Alignment

(c) Fusion of Multi-Granular Covariate and Event

Optimization Process in (b)

Hierarchical Granular MoE in (c)

...

T

Joint Optimization

Series

Softmax

Statistic Parameter

Update

Update

Scores

Epoch Epoch

Update

Update

Optimization Process

Series Weights

Attention Scores

Pooling

**Figure 2.** The framework of METP.

lutional networks have been introduced to achieve spatialtemporal alignment. These methods have demonstrated effectiveness in continuous, high-density settings.

In contrast, sparse event-driven scenarios, such as those encountered in temporal point processes, present unique challenges. Temporal misalignment between event sequences and external variables often arises due to lagged effects and indirect interactions. Existing approaches commonly adopt fixed-length lag windows (Shams Eddin and Gall 2024), which do not explicitly account for variable periodic structures and multi-granularity dependencies, limiting adaptability to dynamic external influences.

Recent developments, including diffusion-based alignment (Gao, Cao, and Chen 2025) and cross-modal matching frameworks (Liu et al. 2025), provide improved alignment mechanisms. However, they generally neglect the incorporation of prior knowledge regarding lag structures and the dynamic adjustment of alignment strategies across multiple temporal granularities, which could result in inaccurate predictions when modeling complex temporal dependencies. These limitations highlight the need for alignment strategies that are both prior-informed and granularity-aware to effectively capture the temporal misalignment in sparse, event-based data.

## Methodology

## Problem Formulation

Let S1:n = {t1, t2,..., tn} ∈Rn denote a sequence of n observed event timestamps, where tj represents the times- tamp of the j-th event. The goal is to predict the time of the next event, tn+1. External variables observed at discrete time steps t ∈[1, T] are denoted by xt, which are assumed to influence the temporal dynamics of event occurrences. In contrast to traditional methods that focus exclusively on past event histories, the proposed framework incorporates external inputs to capture their impact on events. Given the historical event sequence S1:n and the corresponding external input sequence XT = {x1,..., xT }, the conditional intensity function λ(t) at time t > T is defined as λ(t) = F (t > T|S1:n, XT), (1)

where F(·) jointly models temporal dependencies and dynamic external effects, enabling improved next-event time prediction under non-stationary conditions. Following (Zuo et al. 2020), the conditional density of the next event time given the known observations is defined based on the conditional intensity function λ(t) as κ(t) = λ(t) exp

−

Z t tn λ(τ) dτ

, (2)

where t ≥tn and tn denotes the timestamp of the most recent observed event. Based on this density, the expected arrival time of the next event after T is obtained via the conditional expectation:

tn+1 =

Z ∞

T t · κ(t) dt. (3)

This formulation forms the theoretical basis for our predictive framework, which aims to jointly model temporal de-

22852

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-003-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

pendencies and exogenous environmental influences for accurate event time forecasting.

Framework Overview. The proposed METP framework integrates three key modules: periodicity and multi-granular encoding, alignment of external lag effects, and fusion of covariates and events for event intensity prediction, as illustrated in Fig. 2.

Periodicity and Multi-Granular Encoding To effectively model temporal dependencies and capture periodic patterns in the external time series, we extract the dominant periodicity from the external time series {x1, x2,..., xt} using the Discrete Fourier Transform. The frequency with the highest magnitude, excluding zero frequency, is identified to determine the dominant period δ. The detailed algorithm is provided in the Appendix. A sliding window then extracts the most recent segment of length δ:

xt−δ+1:t = [xt−δ+1,..., xt]. (4)

To incorporate multiple past cycles, we construct a compact periodic time matrix X(t) ∈Rδ×m, where δ is the period length and m is the number of past periods. Each row corresponds to a complete historical period, and each column represents the same relative position across periods:

X(t) = xt−δ+1:t,..., xt−mδ+1:t−(m−1)δ

⊤. (5)

Right-padding is applied when insufficient data points are available. To capture both long-term trends and short-term fluctuations, a hierarchical pooling strategy is applied to X(t) to analyze information across different granularities. We define a set of granularities {sk}K k=1, where each sk represents the length of a non-overlapping pooling window. For each granularity, a max pooling is performed:

Uk(t) = MaxPoolsk (X(t)) ∈R j δ sk ×m k

, (6)

where MaxPoolsk(·) denotes a temporal pooling operator with kernel and stride size sk. This process facilitates the extraction of both short-term and long-term temporal dependencies. Subsequently, the temporal positioning of events is encoded to distinguish events based on their absolute occurrence times. We adopt a sinusoidal position encoding scheme. While prior work such as (Xiao et al. 2025) determines periodicity based on sampling patterns from the event sequence, our approach differentiates itself by directly deriving the encoding period δ from the dominant periodicity present in the external covariates. This enables a more covariate-aware temporal encoding. Specifically, each timestamp t is mapped to a deterministic vector e(t) ∈Rd:

e(t) = q

2 d h sin

2πω1t δ

, cos

2πω1t δ

,..., sin

2πωd/2t δ

, cos

2πωd/2t δ i

,

(7)

where {ωi}d/2 i=1 are frequency components defined as ωi = 10000 2(i−1) d. This design introduces a data-driven temporal basis with external dynamics, improving the model sensitivity to periodic structures in real-world event sequences.

Alignment of Lagged Effect Distributions Given the discrete time steps and strong temporal dependencies between adjacent inputs, a non-symmetric decay modeled by a reversed geometric distribution offers an effective prior for capturing lagged effects. Flexibility is further enhanced by incorporating an additional causal selfattention mechanism. This mechanism captures time-aware dependencies between different historical moments and the current event time, with attention scores adaptively reflecting their relative importance. To conform to established temporal-decay patterns while retaining data-driven flexibility, reversed-geometric weights are precisely aligned with causal self-attention scores, yielding an accurate portrayal of lagged effects. For simplicity, the time index t is omitted in the notation. Let uk denote the vector corresponding to the latest time in the temporal sequence Uk. The decay parameter is given by ϕk = ukwk, where wk is a learnable projection vector. The corresponding normalized reversed geometric prior distribution models the temporal influence as rk(j) = (1 −ϕk)j−1 · ϕk

1 −(1 −ϕk)γk, (8)

where j = 1, 2,..., γk, and γk denotes the maximum delay window at the k-th granularity. To flexibly learn the relevance distribution in a data-driven manner (Xu et al. 2021), we adopt a time-aware causal self-attention mechanism. For each granularity k, the query and key vectors are computed as qk = ukw1, kk = ukw2, where w1 and w2 are learnable projection matrices. To capture the influence of all key vectors on the query vector at granularity k, the raw attention scores are computed as sj k = q⊤ k kj k √ l

, (9)

where kj k represents the j-th key vector, and l is the dimensionality of the vectors. For the γk-th query position, the attention score αj k assigned to the j-th key is given by the softmax function as pk(j) = αj k = exp(sj k) Pγk i=1 exp(si k), (10)

where the distribution pk(j) quantifies the attention score at the j-th time point when predicting the current query at granularity k. To align the learned reverse geometric distribution rk with the attention score distribution pk, we adopt the Symmetric Kullback–Leibler (SKL) divergence:

DSKL(k) = DKL(pk ∥rk) + DKL(rk ∥pk), (11) where

DKL(pk ∥rk) = γk X j=1 pk(j) log pk(j) rk(j) + ϵ, (12)

where ϵ > 0 is a small constant to ensure numerical stability. Subsequently, the aggregated hidden representation at time t for granularity k is computed as the attention-weighted sum of historical hierarchical vectors:

zk t = γk X j=1 αj kut−j+1 k, (13)

22853

<!-- Page 5 -->

where ut−j+1 k denotes the hierarchical representation at granularity k and delay step j. The prediction ˆyt of future event occurrence is then obtained via a linear transformation and sigmoid activation:

ˆyk t = σ(wzzk t + bz), (14) where wz, bz ∈R, and σ(·) is the sigmoid function. The loss function is minimized to optimize model parameters:

Lk =

T X t=1

LCE(yt, ˆyk t) + η DSKL(k), (15)

where LCE(·, ·) is the weighted cross-entropy with a weighting factor determined by the event ratio. yt ∈{0, 1} indicates whether an event occurs at time t, and η > 0 is a trade-off parameter that balances predictive accuracy and regularization. The cross-entropy term drives prediction accuracy, while the SKL term constrains the attention weight distribution to remain consistent with the prior, thereby regularizing temporal structure learning.

Fusion of Multi-Granular Covariates and Events To model the conditional intensity function of the event ej+1 occurring at time t, given the j-th event at time tj, we fuse aligned external variables with historical event embeddings to capture both past events and external influences on future occurrences. The aligned external representation at granularity k is defined as:

Pk(t) = 1

Zk γk X i=1 αi k · dk(t −tj) · utj−i+1 k, (16)

where the attention weights αi k are derived from causal selfattention at granularity k, and u(tj−i+1)

k denotes the external covariate embedding at the i-th lag step with respect to event time tj. The normalization constant is defined as Zk = Pγk i=1 αi k. The scalar lagged weight is defined as dk(t−tj) = (1−ϕk)t−tj, which applies an exponential decay based on the temporal distance between the current time t and tj. This method separates the effects of attention-based relevance and temporal decay, enabling more interpretable modeling of lagged external influences. Multi-granularity embeddings {Pk}K k=1 are integrated using a hierarchical granular MoE mechanism. To ensure the analysis remains grounded in the original temporal resolution, the embedding at the first granularity is always included. The remaining K −1 expert embeddings are dynamically selected at each time step t, yielding the aggregated representation:

P(t) = π1P1(t) +

X k∈Kt πkPk(t), (17)

where the set Kt ⊆{2,..., K} denotes the indices of the top-(K−1) selected experts at time t, and π = (π1, πk)k∈Kt are the learned mixture coefficients, producing a unified environment-aware context. The historical event embedding sequence E = [e1,..., en] is processed through multi-head self-attention and feed-forward layers:

M = MultiHeadAttention(E), (18) H = LayerNorm(M + FFN(M)). (19)

The conditional intensity function at time t is formulated as λ(t|Ht) = softplus ρt −ti ti

+ w⊤ a ha(t) + b

!

, (20)

where wa = [wh, we], ha(t) = [ht, p(t)]. (21)

Here, ρ controls the temporal decay, wh and we are learnable weight vectors, and b is a bias term. The softplus activation function guarantees the non-negativity of λ(t|Ht). This formulation enables modeling of intensity by jointly capturing dependencies in historical events and covariates.

Training Objective The negative log-likelihood loss Lp is constructed based on the conditional intensity function and approximated by a discrete summation:

Lp = − n X i=1 log λ(ti|Hti) +

T X j=1 λ(j|Hj), (22)

where λ(t|Ht) denotes the conditional intensity at time t, and the integral is estimated over T discrete time steps. The overall loss function is given by:

L = Lp +

K X k=1

Lk, (23)

where Lk denotes the alignment loss at granularity level k. A two-stage optimization is adopted for stability. Details of the overall algorithm and training procedure are provided in the Appendix. Additionally, based on the learned intensity function, the expected time of the next event in Equation (3) is approximated by:

ˆtj+1 =

M X t=T t · p(t|κ(t)), (24)

where M is the number of discrete time points considered. This approximation enables practical prediction of event timings in discrete settings.

## Experiment

## Experiment

Setting Datasets. We evaluate our method on one proprietary dataset and three publicly available benchmarks. The proprietary Gasoline Transaction Dataset (GTD) records longitudinal gasoline transaction data, with external covariates representing sales prices. The Tianchi-Walmart Storm Sales Dataset1 includes product-level sales data across multiple stores, accompanied by external temperature time series. The Elevator Fault Dataset2 involves event modeling for annotated elevator fault types, with associated indi-

1https://tianchi.aliyun.com/dataset/89813 2https://www.kaggle.com/datasets/ziya07/elevator-faultmonitoring-and-early-warning-system

22854

<!-- Page 6 -->

## Model

GTD Tianchi Fault Earthquake Avg. NLL

Avg. NMAE

Avg. NRMSE

Avg. Rank NLL NMAE NRMSE NLL NMAE NRMSE NLL NMAE NRMSE NLL NMAE NRMSE

RMTPP (2016) 15.90 0.24 0.94 0.02 1.86 0.05 1.99 0.02 0.58 0.03 4.58 0.03 1.70 0.04 0.42 0.01 0.77 0.01 12.01 0.28 0.94 0.02 9.32 0.10 7.90 0.72 4.13 7.13 IFTPP (2019) 14.85 0.18 0.97 0.03 1.79 0.05 2.56 0.10 1.50 0.03 6.01 0.06 2.06 0.03 0.63 0.01 1.05 0.03 12.73 0.19 2.19 0.06 10.05 0.09 8.55 1.32 4.73 7.38 THP (2020) 9.81 0.07 0.49 0.01 1.08 0.02 1.60 0.04 1.25 0.05 3.87 0.03 1.50 0.04 0.36 0.02 0.98 0.03 11.24 0.12 1.12 0.02 9.02 0.03 6.54 0.81 3.23 3.63 SAHP (2020) 14.56 0.10 0.78 0.04 1.49 0.03 2.56 0.10 1.50 0.03 6.01 0.06 2.84 0.05 0.71 0.02 1.12 0.04 13.24 0.15 2.31 0.03 10.01 0.04 8.80 1.33 4.66 6.88 A-NHP (2022) 9.97 0.08 0.62 0.03 1.64 0.04 1.76 0.05 0.46 0.05 5.61 0.03 3.57 0.08 1.04 0.03 3.82 0.05 18.26 0.10 0.99 0.02 11.28 0.06 8.89 0.78 5.09 5.75 ITHP (2024) 9.09 0.09 0.40 0.02 1.01 0.04 1.64 0.08 0.98 0.04 3.19 0.02 1.31 0.05 0.41 0.03 0.99 0.05 10.86 0.04 0.91 0.10 8.77 0.03 5.72 0.68 3.24 2.63 XTSFormer (2025) 10.15 0.32 1.23 0.04 1.98 0.03 1.60 0.04 1.41 0.03 3.45 0.05 1.50 0.04 0.38 0.02 0.95 0.03 16.58 0.01 0.91 0.04 10.75 0.08 7.46 0.98 4.28 5.88

METP 8.25 0.08 0.38 0.03 0.90 0.02 1.55 0.02 0.98 0.02 3.15 0.02 1.23 0.04 0.36 0.02 0.84 0.03 10.06 0.08 0.88 0.02 8.91 0.07 5.27 0.65 3.20 1.63

**Table 1.** Quantitative performance comparison across GTD, Tianchi, Fault, and Earthquake datasets using NLL, NMAE, and NRMSE. Average scores over all available datasets are reported on the right. Lower values indicate better performance. The last column shows the average ranking of each model over all metrics.

## Model

Variant GTD Tianchi

NLL NMAE NRMSE NLL NMAE NRMSE

METP (Full Model) 8.25 0.38 0.90 1.55 0.98 3.15 w/o External Variables 9.56 0.49 1.12 1.92 1.56 3.82 w/o Lagged Weights 8.96 0.44 1.03 1.85 1.25 3.41 w/o Multi-Scale Structure 8.31 0.42 0.94 1.62 1.07 3.32 w/o Periodic Structure 8.65 0.43 1.15 1.70 1.09 3.30

**Table 2.** Ablation study results on the GTD dataset and the public benchmark dataset (Tianchi).

cator time series as external features. The Global Earthquake Dataset3 contains large-scale geophysical earthquake records, with extreme weather conditions as external variables. Detailed descriptions are provided in the Appendix.

Baselines and Evaluation. We compared our method with several state-of-the-art TPP baselines. RMTPP (Du et al. 2016) combines RNNs with TPPs to capture temporal dependencies. IFTPP (Shchur, Biloˇs, and G¨unnemann 2019) uses normalizing flows to model inter-event times without explicit intensity functions. THP (Zuo et al. 2020) employs Transformer self-attention for short- and long-term dependencies. SAHP (Zhang et al. 2020) replaces RNNs with attention and encodes inter-event times via sinusoidal phase shifts. A-NHP (Yang, Mei, and Eisner 2022) uses symbolic time-varying embeddings to improve parallelizability. ITHP (Meng et al. 2024) models nonlinear inter-type dependencies for better interpretability. NJDTPP (Zhang et al. 2024b) defines intensities via neural jump-diffusion SDEs for unified dynamic modeling. XTSFormer (Xiao et al. 2025) captures multi-scale irregular clinical events with cross-temporal-scale Transformers.

To evaluate the model effectiveness in predicting event times, we employ three widely used metrics: Negative Log-Likelihood (NLL), Normalized Mean Absolute Error (NMAE), and Normalized Root Mean Square Error

3https://www.kaggle.com/datasets/alessandrolobello/theultimate-earthquake-dataset-from-1990-2023/data

(NRMSE). NLL evaluates the probabilistic fit between the predicted intensity function and the observed event sequence, while NMAE and NRMSE assess the normalized deviations between predicted and actual time, with lower values across all metrics indicating better performance.

Implementation Details. The proposed model is implemented in PyTorch using a 3-layer Transformer encoder architecture with 4 attention heads. The model is trained with the Adam optimizer (learning rate = 1e−3, batch size = 16) for 100 epochs. For numerical stability in divergence estimation, we apply a small constant ϵ = 1e−9. Further architectural and implementation details are provided in the Appendix.

## Experiments

on Performance Table 1 presents the performance of all models across four datasets using NLL, NMAE, and NRMSE as evaluation metrics. The proposed METP consistently achieves the best performance on the GTD dataset across all metrics. On the Tianchi dataset, it achieves the lowest NLL and NRMSE, while its NMAE is slightly higher than that of RMTPP, as the recurrent structure of RMTPP better captures short-term fluctuations in densely occurring events. On the Fault dataset, METP does not achieve the best NRMSE, which is slightly higher than that of RMTPP, due to RMSE’s higher sensitivity to rare but large deviations, despite METP maintaining relatively strong overall accuracy across other metrics. For the Earthquake dataset, METP surpasses all baselines in NLL and NMAE, while its NRMSE remains marginally higher than that of ITHP, as ITHP demonstrates stronger suppression of long-interval prediction errors. Overall, METP obtains the lowest average scores across all three metrics, indicating superior robustness and generalization across diverse temporal event prediction tasks. Statistical tests further confirm that METP outperforms the baselines. Complete test results are reported in the Appendix.

Ablation Study We perform ablation studies on both the GTD and Tianchi datasets to assess the contribution of each model component. As shown in Table 2, removing external variables

22855

<!-- Page 7 -->

10 4 10 3 10 2 10 1 100

2

4

6

8

10

NLL

GTD Tianchi Fault Earthquake

(a) Alignment regularization coefficient η

41632 64 128 256

2

4

6

8

10

12

14

NLL

GTD Tianchi Fault Earthquake

(b) Scale of temporal encoding d

1 2 3 4 5 6

2

4

6

8

10

12

NLL

GTD Tianchi Fault Earthquake

(c) Number of granularities K

**Figure 3.** Performance variations of the method under different hyperparameter settings.

causes the most significant degradation, with NLL, NMAE, and NRMSE increasing by 15.6%, 28.9%, and 24.4% on the GTD dataset, and by 23.9%, 59.2%, and 21.3% on the Tianchi dataset, respectively. This highlights the critical role of environment-aware modeling. Excluding the lagged weights leads to an 8.6% rise in NLL on GTD and a 27.6% increase in NMAE on Tianchi, indicating the effectiveness of lagged temporal dynamics. When the multi-scale structure is ablated, performance deteriorates across all metrics, with a 7.3% increase in NRMSE on Tianchi, confirming its importance in capturing multi-granular temporal patterns. Finally, the periodic structure also contributes notably, especially on GTD where the NLL rises by 4.8%. These results demonstrate that each component plays a distinct role, and the full model consistently achieves the best performance across datasets.

Sensitivity Analysis The sensitivity analysis evaluates METP’s hyperparameters via NLL minimization. Fig. 3(a) shows optimal performance at η = 10−3–10−2, balancing feature alignment and flexibility since lower values under-regularize while higher values suppress informative variations. Fig. 3(b) indicates d = 64–128 optimally encodes temporal patterns, with smaller dimensions lacking expressiveness and larger ones causing overfitting. Fig. 3(c) reveals 4–5 granularity levels best capture multi-scale features, as fewer levels are insufficient and more introduce redundant computation. These results confirm METP’s robustness when hyperparameters trade off representation capacity and model complexity.

Visualization of Event Prediction Fig. 4 presents a comparative visualization of event prediction performance from January to June 2023. The two real-case examples demonstrate how historical external series evolve into future event time predictions, with METP effectively capturing the lagged temporal dependencies that influence event occurrences. Across the six predicted events (E1: 01-18 to E6: 05-28), METP’s predictions show closer alignment with the actual events than those of THP and XTSFormer, especially during the prediction period where conventional methods tend to diverge. This performance advantage stems from METP’s integrated modeling of historical event patterns, external variable influences, and multi-

External

Lagged

Effects

Historical

Series

Unknown

Future

Historical Events 2023-01 2023-02 2023-03 2023-04 2023-05 2023-06 Time

E1 01-18 E2 02-05 E3 02-22 E4 03-14 E5 04-21 E6 05-28

Time Prediction

**Figure 4.** Comparison of event prediction between baselines and METP.

scale temporal relationships via its causal attention mechanism, enabling more stable and accurate forecasts throughout the prediction horizon. The visualization underscores that explicitly accounting for these external covariates allows METP to better anticipate the time of future events.

## Conclusion and Future Work

The proposed METP framework advances temporal point process modeling by effectively incorporating multigranular lagged external covariates through its novel lagaware calibration and hierarchical fusion approach, demonstrating superior predictive accuracy across diverse datasets. Future extensions will focus on adapting the framework to streaming temporal point processes, enabling real-time event prediction under evolving external conditions.

Ethics Statement

The data used in this work, including public benchmarks and a proprietary dataset, consists of aggregated and deidentified information, ensuring no privacy violations. We acknowledge that enhanced forecasting models could be misused and strongly discourage such applications. Our

22856

![Figure extracted from page 7](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-metp-multi-granularity-integration-of-external-covariates-for-temporal-point-pro/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

study focuses on general methodological improvement in temporal event modeling.

## Acknowledgments

This work is supported by the National Natural Science Foundation of China (Grant Nos. 72271009 and 72371217), the Guangzhou Industrial Informatics and Intelligence Key Laboratory (Grant No. 2024A03J0628), the Nansha Key Area Science and Technology Project (Grant No. 2023ZD003), and Project No. 2021JC02X191.

## References

Boyd, A.; Bamler, R.; Mandt, S.; and Smyth, P. 2020. User-dependent neural sequence models for continuoustime event data. Advances in Neural Information Processing Systems, 33: 21488–21499. Chen, S.; Xu, G.; Tao, T.; Zhang, S.; Zhang, K.; and Kuang, J. 2025. An Efficient Bearing Prognostic Approach through Modeling Multiperiodic and Nonperiodic Temporal Patterns. IEEE Transactions on Industrial Informatics. Dai, Z.; He, L.; Yang, S.; and Leeke, M. 2024. Sarad: Spatial association-aware anomaly detection and diagnosis for multivariate time series. Advances in Neural Information Processing Systems, 37: 48371–48410. Deng, J.; Ye, F.; Yin, D.; Song, X.; Tsang, I.; and Xiong, H. 2024. Parsimony or capability? decomposition delivers both in long-term time series forecasting. Advances in Neural Information Processing Systems, 37: 66687–66712. Du, N.; Dai, H.; Trivedi, R.; Upadhyay, U.; Gomez- Rodriguez, M.; and Song, L. 2016. Recurrent marked temporal point processes: Embedding event history to vector. In Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery and data mining, 1555– 1564. D’Amelio, A.; Cartella, G.; Cuculo, V.; Lucchi, M.; Cornia, M.; Cucchiara, R.; and Boccignone, G. 2025. TPP-Gaze: Modelling Gaze Dynamics in Space and Time with Neural Temporal Point Processes. In 2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 8786– 8795. IEEE. Gao, J.; Cao, Q.; and Chen, Y. 2025. Auto-regressive moving diffusion models for time series forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 16727–16735. Gracious, T.; and Dukkipati, A. 2025. Deep Representation Learning for Forecasting Recursive and Multi-Relational Events in Temporal Networks. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 16897– 16905. Gu, Y. 2021. Attentive neural point processes for event forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, 7592–7600. Hawkes, A. G. 1971. Spectra of some self-exciting and mutually exciting point processes. Biometrika, 58(1): 83–90. Isik, Y.; Chapfuwa, P.; Davis, C.; and Henao, R. 2023. Hawkes Process with Flexible Triggering Kernels. In

Machine Learning for Healthcare Conference, 308–320. PMLR. Karpukhin, I.; Shipilov, F.; and Savchenko, A. 2024. HoTPP Benchmark: Are We Good at the Long Horizon Events Forecasting? arXiv preprint arXiv:2406.14341. Kuang, Y.; Yang, C.; Yang, Y.; and Li, S. 2024. Unveiling latent causal rules: A temporal point process approach for abnormal event explanation. In International Conference on Artificial Intelligence and Statistics, 2935–2943. PMLR. Li, Y.; Li, K.; Chen, C.; Zhou, X.; Zeng, Z.; and Li, K. 2021a. Modeling temporal patterns with dilated convolutions for time-series forecasting. ACM Transactions on Knowledge Discovery from Data (TKDD), 16: 1–22. Li, Z.; Zhao, Y.; Han, J.; Su, Y.; Jiao, R.; Wen, X.; and Pei, D. 2021b. Multivariate time series anomaly detection and interpretation using hierarchical inter-metric and temporal embedding. In Proceedings of the 27th ACM SIGKDD conference on knowledge discovery & data mining, 3220–3230. Lin, S.; Lin, W.; Hu, X.; Wu, W.; Mo, R.; and Zhong, H. 2024. Cyclenet: Enhancing time series forecasting through modeling periodic patterns. Advances in Neural Information Processing Systems, 37: 106315–106345. Liu, P.; Guo, H.; Dai, T.; Li, N.; Bao, J.; Ren, X.; Jiang, Y.; and Xia, S.-T. 2025. Calf: Aligning llms for time series forecasting via cross-modal fine-tuning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 18915–18923. Meng, Z.; Wan, K.; Huang, Y.; Li, Z.; Wang, Y.; and Zhou, F. 2024. Interpretable Transformer Hawkes processes: Unveiling complex interactions in social networks. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2200–2211. Mu, Y.; Shahzad, M.; and Zhu, X. X. 2025. MPTSNet: Integrating multiscale periodic local patterns and global dependencies for multivariate time series classification. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 19572–19580. Shams Eddin, M. H.; and Gall, J. 2024. Identifying spatiotemporal drivers of extreme events. Advances in Neural Information Processing Systems, 37: 93714–93766. Shchur, O.; Biloˇs, M.; and G¨unnemann, S. 2019. Intensityfree learning of temporal point processes. arXiv preprint arXiv:1909.12127. Shou, X.; Gao, T.; Subramanian, D.; Bhattacharjya, D.; and Bennett, K. P. 2023. Concurrent multi-label prediction in event streams. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 9820–9828. Xiao, T.; Xu, Z.; He, W.; Xiao, Z.; Zhang, Y.; Liu, Z.; Chen, S.; Thai, M. T.; Bian, J.; Rashidi, P.; et al. 2025. XTS- Former: Cross-Temporal-Scale Transformer for Irregular- Time Event Prediction in Clinical Applications. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 28502–28510. Xu, J.; Wu, H.; Wang, J.; and Long, M. 2021. Anomaly transformer: Time series anomaly detection with association discrepancy. arXiv preprint arXiv:2110.02642.

22857

<!-- Page 9 -->

Yang, C.; Mei, H.; and Eisner, J. 2022. Transformer Embeddings of Irregularly Spaced Events and Their Participants. In Proceedings of the Tenth International Conference on Learning Representations (ICLR). Zhang, D.; Du, C.; Peng, Y.; Liu, J.; Mohammed, S.; and Calvi, A. 2024a. A multi-source dynamic temporal point process model for train delay prediction. IEEE Transactions on Intelligent Transportation Systems. Zhang, P.; Zhou, Z.; Feng, Z.; Wang, J.; and Zhang, Y. 2023. Inference and analysis on the evidential reasoning rule with time-lagged dependencies. Engineering Applications of Artificial Intelligence, 126: 106978. Zhang, Q.; Lipani, A.; Kirnap, O.; and Yilmaz, E. 2020. Self-attentive Hawkes process. In International conference on machine learning, 11183–11193. PMLR. Zhang, S.; Zhou, C.; Liu, Y. A.; Zhang, P.; Lin, X.; and Ma, Z.-M. 2024b. Neural jump-diffusion temporal point processes. In Forty-first International Conference on Machine Learning. Zhang, W.; Zhang, L.; Han, J.; Liu, H.; Fu, Y.; Zhou, J.; Mei, Y.; and Xiong, H. 2024c. Irregular traffic time series forecasting based on asynchronous spatio-temporal graph convolutional networks. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 4302–4313. Zuo, S.; Jiang, H.; Li, Z.; Zhao, T.; and Zha, H. 2020. Transformer hawkes process. In International conference on machine learning, 11692–11702. PMLR.

22858
