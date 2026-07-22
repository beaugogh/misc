---
title: "Optimal Look-back Horizon for Time Series Forecasting in Federated Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39781
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39781/43742
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Optimal Look-back Horizon for Time Series Forecasting in Federated Learning

<!-- Page 1 -->

Optimal Look-back Horizon for Time Series Forecasting in Federated Learning

Dahao Tang1, Nan Yang1 *, Yanli Li1, Zhiyu Zhu2, Zhibo Jin2, Dong Yuan1 *

1University of Sydney 2University of Technology Sydney dahao.tang@sydney.edu.au, n.yang@sydney.edu.au, yanli.li@sydney.edu.au, zhiyu.zhu@student.uts.edu.au, zhibo.jin@student.uts.edu.au, dong.yang@sydney.edu.au

## Abstract

Selecting an appropriate look-back horizon remains a fundamental challenge in time series forecasting (TSF), particularly in the federated learning scenarios where data is decentralized, heterogeneous, and often non-independent. While recent work has explored horizon selection by preserving forecasting-relevant information in an intrinsic space, these approaches are primarily restricted to centralized and independently distributed settings. This paper presents a principled framework for adaptive horizon selection in federated time series forecasting through an intrinsic space formulation. We introduce a synthetic data generator (SDG) that captures essential temporal structures in client data, including autoregressive dependencies, seasonality, and trend, while incorporating client-specific heterogeneity. Building on this model, we define a transformation that maps time series windows into an intrinsic representation space with well-defined geometric and statistical properties. We then derive a decomposition of the forecasting loss into a Bayesian term, which reflects irreducible uncertainty, and an approximation term, which accounts for finite-sample effects and limited model capacity. Our analysis shows that while increasing the lookback horizon improves the identifiability of deterministic patterns, it also increases approximation error due to higher model complexity and reduced sample efficiency. We prove that the total forecasting loss is minimized at the smallest horizon where the irreducible loss starts to saturate, while the approximation loss continues to rise. This work provides a rigorous theoretical foundation for adaptive horizon selection for time series forecasting in federated learning.

Extended Version — https://arxiv.org/abs/2511.12791

## Introduction

Time series forecasting (TSF) underpins numerous highimpact domains, including finance (Zivot and Wang 2006), healthcare (Futoma, Hariharan, and Heller 2017), and energy systems (Kong et al. 2019), where accurate prediction of future values from historical trends is crucial for informed decision-making and operational efficiency. A central modeling choice in TSF is the selection of the look-back horizon, defined as the number of past time steps used as input. This

*Corresponding authors. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

choice significantly influences model complexity, predictive accuracy, and generalization performance (Lim et al. 2021).

Traditionally, the look-back horizon is treated as a tunable hyperparameter, often selected via cross-validation or heuristic search. Recent theoretical advances offer a more principled perspective. Shi et al. (Shi et al. 2024) propose a scaling law theory based on a theoretical framework that embeds time series into an intrinsic representation space, allowing the forecasting loss to be decomposed into two components: Bayesian error, capturing irreducible uncertainty from noise and limited information, and approximation error, reflecting the model’s capacity to learn the true mapping. This decomposition enables analytical reasoning about the optimal look-back horizon as a function of dataset size, model complexity, and intrinsic dimensionality (Sharma and Kaplan 2020; Bahri et al. 2024). Empirical results support these insights, showing that the optimal horizon grows with data availability and varies by model type. For example, channeldependent models like iTransformer (Liu et al. 2024) benefit from shorter horizons under limited data, while linear models such as NLinear (Zeng et al. 2023) maintain performance with longer horizons due to smoother feature decay and lower intrinsic complexity (Xu, Zeng, and Xu 2024; Toner and Darlow 2024).

However, this framework relies on strong assumptions, including centralized data, independent identically distribution (IID), and homogeneous model architectures, which are often violated in real-world federated learning scenarios. In such decentralized settings, data is distributed across clients with diverse distributions, sequence lengths, and domain characteristics (Kairouz et al. 2021). Applying a globally fixed horizon in this context may lead to mismatches between local dynamics and model inputs, degrading forecasting performance (Edwards et al. 2024). Moreover, realworld data frequently exhibits feature sparsity, variable noise levels, and heterogeneous scaling behaviors, challenging the smooth manifold assumptions in intrinsic dimension theory (Levi and Oz 2024; Zador 1982). These limitations highlight the need for adaptive horizon strategies that account for both data heterogeneity and localized model constraints. Integrating hybrid architectures or meta-learning mechanisms with principled theoretical foundations, such as those introduced by Shi et al., presents a promising direction for addressing these challenges in federated time series fore-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

25823

<!-- Page 2 -->

casting.

This paper addresses the challenge of selecting the optimal look-back horizon for time series forecasting in federated learning environments characterized by non-IID client data. We develop a principled framework that leverages a structured Synthetic Data Generator (SDG) to model core temporal patterns (e.g., autoregressive dynamics, seasonality, and trends), while capturing client-specific heterogeneity. Using the SDG as a foundation, we construct a dataaware transformation that maps time series windows into an intrinsic representation space with well-defined geometric and statistical properties. This enables a rigorous loss decomposition into irreducible (Bayesian) and approximation components, each tied to the underlying generative structure. Crucially, the formulation reveals how the informativeness of historical context and thus the optimal look-back horizon varies across clients depending on their local dynamics and data regimes. Our analysis shows that the total forecasting loss is minimized at the smallest horizon where the Bayesian error saturates and the approximation error begins to dominate, yielding a theoretically grounded, clientadaptive criterion for horizon selection in federated forecasting settings. Our contributions include the following:

• We propose a novel intrinsic space formulation that transforms heterogeneous, non-IID multivariate time series into a compact and geometry-preserving representation. This space is rigorously characterized by bi-Lipschitz continuity, intrinsic dimensionality saturation, and interhorizon compatibility, enabling consistent comparison and reasoning across clients and temporal contexts. • We establish a tight decomposition of predictive loss into irreducible (Bayesian) and approximation components, each analytically tied to the structural elements of time series data (e.g., AR memory, seasonality, trend) and the look-back horizon. Our analysis uncovers the fundamental bias–variance trade-off that governs forecasting performance in federated settings. • We prove that the total loss is unimodal with respect to the horizon length and identify the smallest sufficient horizon as its global minimizer. This result provides the first rigorous criterion for horizon selection in time series forecasting and introduces a new design principle for model construction under sample-limited, heterogeneous environments.

## Related Work

Horizon Selection and Intrinsic Representation

A central yet understudied question in time series forecasting (TSF) is how much historical context, i.e., look-back horizon, is truly needed for accurate prediction (Kim et al. 2025). Traditional statistical models such as ARIMA select lag length using information criteria like AIC (Akaike 1974; Box et al. 2015), which implicitly perform horizon selection under strong linearity assumptions. While interpretable, these methods struggle to capture nonlinear or long-range dependencies. Modern deep learning approaches, including LSTMs (Hochreiter and Schmidhuber 1997), hybrid models like LSTNet (Lai et al. 2018), and attention-based architectures such as the Temporal Fusion Transformer (Lim et al. 2021) or Informer (Zhou et al. 2021), have greatly improved modeling capacity. However, they still treat the input horizon as a tunable hyperparameter, typically set through validation or heuristics, without theoretical grounding. This empirical approach can lead to overfitting, underfitting, or inefficient use of data, particularly in settings with limited or distributed samples (Woo et al. 2023; Koparanov, Georgiev, and Shterev 2020).

Recent theoretical work has begun to formalize the horizon selection problem. Notably, Shi et al. (2024) analyze how forecasting error scales with input length, dataset size, and model complexity, revealing a trade-off: longer horizons can improve identifiability of temporal structure but also increase approximation error due to model limitations and finite data (Shi et al. 2024). Their framework introduces the notion of an intrinsic representation space, where the forecasting loss decomposes into two parts: a Bayesian (irreducible) error reflecting inherent unpredictability, and an approximation error arising from statistical and model constraints. This idea builds on Takens’ embedding theorem (Takens, Young, and Rand 2006), which implies that a system’s future behavior can be reconstructed from a finite number of past observations, defining an intrinsic dimension sufficient for prediction. However, Shi’s work assumes centralized and IID data, limiting its relevance to modern federated learning scenarios where data is distributed, non-IID, and client-specific. We extend this theory to federated, non- IID settings by introducing an intrinsic representation that captures essential temporal structure across clients. This enables a principled approach to selecting the optimal lookback horizon in decentralized forecasting.

Time Series Forecasting in Federated Learning

Federated learning (FL) enables decentralized training across clients without sharing raw data. The foundational FedAvg algorithm introduced by McMahan et al. (2017) laid the groundwork for collaborative model training in privacysensitive environments (McMahan et al. 2017). However, FL under non-IID data poses major challenges, including model divergence, degraded generalization, and client imbalance. To address data heterogeneity, methods like FedProx (Li et al. 2020) introduce regularization terms that stabilize optimization across diverse client distributions. In time series forecasting specifically, recent works apply FL to real-world sequential tasks, such as traffic and energy demand prediction, but focus primarily on model architecture and aggregation (Perifanis et al. 2023). These systems rarely examine how temporal structure varies across clients or how such variation affects forecasting horizons. While personalization and communication efficiency have been explored, no prior work provides a theoretical framework for look-back horizon selection in federated TSF. Our paper addresses this gap by analyzing horizon choice through the lens of synthetic modeling and intrinsic representation under client heterogeneity.

25824

<!-- Page 3 -->

Preliminary In this section, we defined the basic settings for time series forecasting in the federated learning scenario. More specifically, we propose a synthetic data generator (SDG) that well describes real-world non-IID data and implement a step-bystep transformation that converts the time series data described by the SDG into an intrinsic space that represents the information carried by a time series.

Time Series Forecasting in Federated Learning We study S-step forecasting from a length-H look-back window in a federated setting with K clients. Client k ∈ {1,..., K} holds a multivariate time series {x(k)

t }Lk t=1 with F features, x(k)

t ∈RF. For time index t ∈{H,..., Lk−S}, define the input window and S-step target block as:

X(H)

t,k = x(k)

t−H+1,..., x(k)

t

∈RF ×H, (1)

Y (S)

t,k = x(k)

t+1,..., x(k)

t+S

∈RF ×S. (2)

Training proceeds in rounds via standard FL aggregation (e.g., FedAvg). On client k, overlapping windows yield Dk training samples; due to overlap, the number of effectively independent samples scales as Dk/H.

Intrinsic Space Formulation We adopt the concept of intrinsic space to represent the information carried by a time series. The intrinsic dimension dI of the intrinsic space is defined as the minimum number of dimensions required to represent the time series without losing significant information. To gain a deeper understanding of the intrinsic space, we investigate the typical structure of non-IID time series data in the federated learning scenario and propose a synthetic data generator that is both theoretically and empirically proven to be sound in describing the structure of the focused non-IID time series data.

Synthetic Data Generator A Synthetic Data Generator (SDG) is a parametric model designed to simulate univariate time series data, which often exhibits structural patterns characterized by seasonality, temporal dependence (AR memory), and trend (Kim et al. 2025).

For a given client k, feature f, and time step t, the synthetic observation ˆxf,t,k is defined as:

ˆxf,t,k = Seasonal(Af,j,k, Tf,j,k, Θf,j,k) + ARp,k(ϕk)

+ Trend(βf,k) + ϵf,t,k

=

J X j=1

Af,j,k · sin

2πt

Tf,j,k

+ θf,j,k

+ p X i=1 ϕk,i xf,t−i,k + βf,k t + ϵf,t,k.

(3)

Here, seasonality is represented by a sum of sinusoids, parameterized by amplitude Af,j,k, period Tf,j,k, and phase shift θf,j,k. Temporal dependence is modeled via an autoregressive process ARp,k(ϕk) = Pp i=1 ϕk,i xf,t−i,k, where ϕk,i are the lag coefficients specific to client k. The trend is

2020-01 2020-03 2020-05 2020-07 2020-09 2020-11 2021-01 Time Step

0

5

10

15

20

25

Signal Value

Real vs Synthetic

Real Synthetic

**Figure 1.** Comparison between real-world data and data generated by the SDG. The close alignment indicates that the SDG effectively captures the patterns present in real data.

captured by a linear component Trend(βf,k) = βf,k t. The additive noise term is drawn from a Gaussian distribution: ϵf,t,k ∼N(µf,k, σ2 f,k). We also provide empirical studies to demonstrate the validity of the SDG, as illustrated in Figure 1. Please refer to the Extended Version for more details.

Feature Skewness Formulation In the federated learning scenario, each client tends to observe a different distribution of the same features in time series data, simulating feature skew (Wu et al. 2024). We apply a customized skewness partitioning method to create feature heterogeneity.

To be more precise, we construct an affine transformation for each data point of the SDG: for client k, feature k:

xf,t,k = Λf,k˜xf,t,k + δf,k (4) where Λfk is the linear scale, which controls how the variance of the feature f, σ2 f, changes for client k; δfk is the mean shift, which changes the mean of the feature f, µf, for the client k. Note that, though the univariate SDG is able to describe each feature, each client is allowed to observe a subset of all the features.

Intrinsic Space Construction At a high level, we construct a geometry-aware representation space that captures the essential temporal structure of non-IID time series through a transformation grounded in the SDG, which explicitly models autoregressive dependencies, seasonal cycles, and linear trends, and serves as a unifying scaffold for both analytical reasoning and empirical evaluation across heterogeneous clients.

Our construction is supported by a set of structural assumptions. These include: (i) compactness of the intrinsic image to ensure bounded representation norms; (ii) bi- Lipschitz continuity to preserve distances and guarantee stable inverses; (iii) a horizon-indexed intrinsic dimension that increases monotonically and saturates once all relevant temporal structure is captured; (iv) compatibility of representations across horizons via stable linear projections; (v) approximate commutativity between truncation and projection, ensuring robustness under input length variation; and (vi) a power-law spectrum of the intrinsic covariance, which enables efficient dimensionality reduction. These assumptions reflect statistical regularities commonly observed in time series data and enable a clean separation between modeling complexity and representational geometry.

25825

<!-- Page 4 -->

The transformation pipeline proceeds in five steps: (1) Client-wise normalization to remove affine feature skew and align marginal distributions; (2) Window flattening to convert each normalized time-series segment into a fixed-length vector; (3) Global covariance estimation and eigendecomposition to identify dominant axes of variation; (4) Intrinsic dimension estimation based on the SDG and empirical spectrum; and (5) Projection into intrinsic space via principal components. Specifically, the intrinsic dimension for client k is approximated as:

dI,k(H) ≈F · (min{H, ℓAR,k} + gk(H) + 1). (5)

Here, ℓAR,k denotes the effective AR memory:

ℓAR,k = ln(1/(1 −ϵ))

−ln ρk

, ϵ ∈(0, 1) (6)

where ρk ∈(0, 1) is the spectral radius of the AR companion matrix. gk(H) reflects the resolved seasonal complexity:

gk(H) = 2

J X j=1 wj,k · min

1, H T ∗ j,k

!

, (7)

wj,k =

PF f=1 A2 f,j,k PF f=1

PJ j=1 A2 f,j,k

. (8)

This formulation yields a compact and informationpreserving representation that enables a precise loss decomposition and supports optimal horizon analysis under federated, non-IID settings. Please refer to the Extended Version for more details.

Loss Analysis Before we proceed to analyze how the look-back horizon H affects forecasting performance in the federated setting, we explore decomposition of the prediction loss into two components: an intrinsic, irreducible term that captures the uncertainty of the data-generating process, and an approximation term that captures the difficulty of learning a mapping in an H-dimensional input space using a finite-capacity model trained on finite and heterogeneous data.

Overall Loss Analysis Consider the forecasting task of predicting the next S values from the previous H observations. Under the intrinsicspace representation, this corresponds to learning a mapping m: M(H) →M(S). For a given client distribution and any measurable predictor m, the squared loss can be decomposed into

L(H, S; m) = LBayes(H, S) + Lapprox(H, S; m) (9)

where:

• Bayesian loss LBayes(H, S) is the irreducible error incurred even by an ideal predictor with full knowledge of the data distribution. • Approximation loss Lapprox(H, S; m) captures the additional error due to using a finite-capacity predictor m trained on limited local data.

The formal derivation of (9) and the precise definitions of the two terms are given in the Extended Version.

We now formalize this intuition by establishing a precise decomposition of the prediction loss in the federated setting, showing how the Bayesian and approximation components arise directly from the client-specific data-generating distributions and the server-side evaluation protocol. Theorem 1 (Federated Loss Decomposition). For each client k ∈ {1,..., K}, let (Uk, Vk) denote its datagenerating pair, where Uk takes values in a measurable input space M(H) and Vk in an output space M(S), both embedded in a real Hilbert space (H, ∥· ∥) with the associated Borel σ-algebras.

Let m∗ k(u):= E[ Vk | Uk = u ] be the client-specific Bayesian predictor, defined PUk–almost everywhere. For any measurable, square-integrable predictor m: M(H) → M(S), the server’s global predictive loss is

L(H, S; m):= Ek∼π h

E

∥Vk −m(Uk) ∥2 i

(10)

where π = (π1,..., πK) is any distribution over clients and the inner expectation is over (Uk, Vk) under client k’s distribution. Then the loss decomposes as:

L(H, S; m) = LBayes(H, S) + Lapprox(H, S; m), (11)

where the federated Bayesian loss is

LBayes(H, S):= Ek∼π h

E

∥Vk −m∗ k(Uk) |2 i

, (12)

and the federated approximation loss is

Lapprox(H, S; m):= Ek∼π h

E

∥m∗ k(Uk) −m(Uk) ∥2 i

. (13) In particular, the total loss separates into the expected irreducible (client-wise Bayes) component and the expected approximation error of the global predictor relative to each client’s Bayes-optimal rule. Please refer to the Extended Version for the proof.

Server–client interpretation The global model m is hosted on the central server and evaluated on clients sampled according to k ∼π. The term LBayes(H, S) captures the irreducible uncertainty within each client’s local data-generating process, averaged over clients, while Lapprox(H, S; m) measures the discrepancy between the global server model and the collection of Bayes-optimal per-client predictors {m∗ k}K k=1. Although both components are defined via client-side distributions, the total loss L(H, S; m) represents the expected prediction error of the server’s global model.

In the remainder of this section, we investigate these two components respectively.

Bayesian (Irreducible) Loss We first characterize the irreducible component of predictive loss for each client using the structure of the SDG. Theorem 2 (Client-wise Bayesian Loss). According to the SDG model in Equation (3) for client k: each feature is generated as an additive sum of (i) an autoregressive component, (ii) a seasonal component, (iii) a linear trend, and (iv)

25826

<!-- Page 5 -->

an innovation noise term, with the innovations independent across time and independent of the deterministic seasonal and trend components. Then the client-wise Bayesian loss admits the exact decomposition:

L(k)

Bayes(H, S) = L(k)

AR(S) + L(k)

seas(H) + L(k)

trend(H) (14)

where each term is the contribution of the corresponding SDG component to the conditional mean-squared error under a horizon-H Bayesian predictor:

L(k)

AR(S):= E

∥Y (S)

AR,k −E[Y (S)

AR,k | X(H)

k ] ∥2

2

, (15)

L(k)

seas(H):= E

∥Y (S)

seas,k −E[Y (S)

seas,k | X(H)

k ] ∥2

2

, (16)

L(k)

trend(H):= E

∥Y (S)

trend,k −E[Y (S)

trend,k | X(H)

k ] ∥2

2

. (17)

Here X(H)

k and Y (S)

k denote the input window and S-step forecast block for client k, and Y (S)

AR,k, Y (S)

seas,k, Y (S)

trend,k are the corresponding SDG components of the future block Y (S)

k. Please refer to the Extended Version for the component-wise characterization and bounds. Remark 1. For each client k, the Bayesian loss L(k)

Bayes(H, S) decreases with the look-back horizon H as longer histories improve identifiability of seasonal structure and (where present) trend components. The loss increases in the forecast horizon S, reflecting the accumulation of autoregressive innovations. Once the dominant seasonal cycles and the client’s effective AR memory are covered, further increasing H yields only negligible improvement: the Bayesian loss has reached its horizon-dependent saturation level.

The irreducible uncertainty perceived by the server is the weighted combination of these client-level Bayesian losses. Lemma 1 (Server-level Bayesian Loss Aggregation). Let π = (π1,..., πK) be any probability distribution over the K clients. The population-level Bayesian loss is

L(server)

Bayes (H, S) =

K X k=1 πk L(k)

Bayes(H, S), (18)

a quantity determined by the client data-generating processes (Uk, Vk) and independent of any global predictor. It aggregates the client-wise irreducible components (autoregressive variation, seasonal residuals, and optional trend terms), each of which exhibits a distinct dependence on the horizon H according to the client’s temporal dynamics.

Approximation Loss We now analyze the approximation loss in the federated setting, where a global model m is trained on a central server using client-local updates. This loss arises from the discrepancy between the global model and the Bayes-optimal predictor on each client. Theorem 3 (Client-wise Approximation Loss). For client k, let m∗ k(X) be the Bayesian predictor and m be any learned predictor. The approximation loss at horizon (H, S) is

L(k)

approx(H, S; m):= E

∥m(X) −m∗ k(X)∥2

2

. (19)

Assume the Bayesian predictor m∗ k is twice differentiable on the intrinsic representation space with bounded curvature, and that m is a piecewise-affine model defined on the intrinsic manifold of dimension dI,k(H). Let Dk denote the number of training windows on client k.

Then the approximation loss admits the intrinsicdimension–dependent bound

L(k)

approx(H, S; m) ≲

K2

2 dI,k(H)2 dI,k(H) 4+dI,k(H)

+ dI,k(H) H

Dk

4 4+dI,k(H) (20)

where K2 is a curvature constant depending only on m∗ k. The first term reflects the geometric complexity of the intrinsic manifold, and the second term quantifies finite-sample limitations due to the effective sample size Dk/H. Full technical derivation is provided in the Extended Version.

The client-wise approximation losses aggregate to form the global loss on the server: Lemma 2 (Server-level Approximation Loss Aggregation). Let π = (π1,..., πK) be the client-sampling distribution used by the server, with πk ≥0 and P k πk = 1. The global approximation loss under the server-side predictor m is the weighted aggregation of the client-wise approximation losses:

L(server)

approx (H, S; m) =

K X k=1 πk L(k)

approx(H, S; m). (21)

Remark 2. Because the intrinsic dimension dI,k(H) typically increases with the look-back horizon H, and the number of effectively independent samples scales as Dk/H, both the curvature-driven bias term and the finite-sample variance term in L(k)

approx(H, S; m) grow with H. Consequently, each client exhibits a horizon beyond which approximation error begins to dominate. The server-level approximation loss inherits this behavior via the mixture weights π, reflecting how rising intrinsic complexity and diminishing effective sample size jointly amplify the approximation error. In this section, we decompose the forecasting error into its fundamental components and characterize how each behaves as a function of the look-back horizon H and forecasting span S. We begin by expressing the population prediction error as the sum of (i) the Bayes loss, which reflects irreducible uncertainty in the SDG, and (ii) the approximation loss, which arises from learning a nonlinear predictor from finite data. This yields the client-wise decomposition with the global loss obtained by aggregation across clients.

The combined loss, therefore, exhibits a fundamental tradeoff: the Bayesian loss decreases and eventually plateaus, while the approximation loss increases with H. Their interaction induces a unimodal structure in the total loss L(k)(H, S) and yields a client-specific optimal lookback horizon that balances signal coverage with statistical efficiency. This analysis forms the theoretical basis for the optimal horizon selection framework developed in the next section.

25827

<!-- Page 6 -->

Optimal Horizon H This section formalizes the choice of the look-back horizon H as an explicit optimization over the total loss

L(H, S; m) = LBayes(H, S) + Lapprox(H, S; m) (22)

where LBayes and Lapprox are defined through the intrinsicspace formulation and federated loss decomposition in the previous sections. Since the trained model implicitly depends on the horizon, we slightly abuse notation and write L(H, S) and Lapprox(H, S) for L(H, S; m) and Lapprox(H, S; m), suppressing the dependence on m to avoid clutter.

We work client-wise (suppressing the client index when clear) and treat H ∈N, using forward differences

∆f(H):= f(H+1) −f(H) (23)

to study how each loss component changes when one additional time step is added to the look-back window. Intuitively, the Bayesian loss should decrease as more history becomes available, while the approximation loss should increase due to higher intrinsic dimensionality and lower effective sample size. The remainder of this section quantifies this trade-off and characterizes the minimizer H∗.

Bayesian–Approximation Loss Dynamics We study how the total client-wise prediction loss

L(k)(H) = L(k)

Bayes(H) + L(k)

approx(H; m) (24)

varies with the look-back horizon H. We use the discrete forward difference ∆f(H):= f(H+1) −f(H) to analyze whether adding one additional step of history decreases or increases the loss.

Bayesian Loss Behavior Under the SDG generative model (Eq. (3)), the irreducible loss decomposes into AR, seasonal, and (optionally zero) trend components. As H increases, ∆L(k)

Bayes(H) ≤0, and ∆L(k)

Bayes(H) →0.

Proof sketch. If H2 > H1, then σ(X1:H1) ⊆σ(X1:H2), and thus Var(Y | X1:H2) ≤Var(Y | X1:H1) almost surely; taking expectations yields L(k)

Bayes(H2) ≤L(k)

Bayes(H1). Under the SDG, the future depends on finite AR memory ℓAR,k, finite seasonal periods Tf,j,k, and a linear trend; therefore, the conditional expectation becomes invariant once H ≥H∗ k, implying ∆L(k)

Bayes(H) →0. The monotonic decrease, therefore, follows from the conditional-variance identity, and the eventual plateau follows from the finite dependency structure of the SDG. Thus, the Bayesian loss enters a plateau where additional history yields negligible improvement.

Approximation Loss Behavior The learned model must approximate the intrinsic mapping from past to future. From the dimension-dependent bound (Theorem 3),

L(k)

approx(H; m) ≲

K2

2 dI,k(H)2 dI,k(H) 4+dI,k(H)

+ dI,k(H) H

Dk

4 4+dI,k(H),

(25)

where dI,k(H) denotes the intrinsic dimension of the input window and Dk is the number of overlapping training windows on client k.

Proof sketch. Both terms in (25) worsen as H grows. First, dI,k(H) is nondecreasing by construction, so the model must approximate a higherdimensional function class; the dimension-dependent term

K2

2dI,k(H)2 dI,k(H)/(4+dI,k(H)) therefore increases with H. Second, due to window overlap, the number of effectively independent samples scales as Dk/H; hence, the statistical term dI,k(H)H/Dk

4/(4+dI,k(H)) also increases with H since the numerator grows and the effective sample size shrinks. Thus, for sufficiently large H, ∆L(k)

approx(H; m) > 0, showing that the approximation cost eventually worsens once the horizon is long enough.

Hence, the approximation loss exhibits the opposite trend of the Bayesian loss: increasing window size ultimately leads to higher approximation error.

Smallest sufficient horizon Now we define a key concept, the smallest sufficient horizon, which serves as the optimal look-back horizon that minimizes the forecasting loss.

Formally, for any tolerance δ > 0, define the smallest sufficient horizon as

H∗ k(δ):= min{H: |∆L(k)

Bayes(H)| ≤δ}, (26)

at which the Bayesian loss has effectively saturated: further historical context improves the irreducible loss by at most δ. Together, these monotonicity properties imply a unimodal structure for the total loss. Theorem 4 (Unimodality and Optimal Horizon). If for a given δ > 0 the Bayesian loss satisfies ∆L(k)

Bayes(H) ≤−δ for all H < H∗ k(δ), and the approximation loss satisfies ∆L(k)

approx(H; m) ≥δ for all H ≥H∗ k(δ), then the combined loss obeys that L(k)(H) decreases on [1, H∗ k(δ)], and L(k)(H) increases on [H∗ k(δ), ∞). Consequently, H∗ k(δ) ∈ arg minH∈N L(k)(H) with uniqueness up to integer ties.

Proof. From the Bayesian loss analysis, increasing H reduces seasonal/phase ambiguity and uncovers AR structure, but only up to a finite coverage horizon. Hence, there exists H0 such that

∆LBayes(H, S) < 0 (H < H0), (27)

while for any δ > 0 we can choose H0 large enough so that

∆LBayes(H, S) ≥−δ (H ≥H0). (28)

For the approximation term, the curvature–variance bound on the intrinsic manifold shows that the error grows with both the intrinsic dimension dI(H) and the factor H/D coming from the effective sample size per window (∝D/(HN)). Since dI(H) is non-decreasing and eventually saturated, while H/D grows linearly, there exists η > 0, independent of H, such that

∆Lapprox(H, S) ≥η (H ≥H0). (29)

25828

<!-- Page 7 -->

Fix any δ ∈(0, η) and define H∗(δ) as the smallest H ≥ H0 with ∆LBayes(H, S) ≥−δ. Then for H < H∗(δ), we have ∆LBayes(H, S) < −δ and ∆Lapprox(H, S) ≥0, so ∆L(H, S) = ∆LBayes(H, S) + ∆Lapprox(H, S) < −δ < 0, and L(H, S) is strictly decreasing. For H ≥H∗(δ), we have ∆LBayes(H, S) ≥−δ and ∆Lapprox(H, S) ≥η, hence ∆L(H, S) ≥−δ + η > 0, so L(H, S) is strictly increasing.

Thus L(H, S) decreases up to H∗(δ) and increases thereafter, so it is unimodal in H and attains its unique minimum at H∗(δ) (up to trivial ties), as claimed.

Hence, before H∗ k(δ), the reduction in irreducible error outweighs the increase in approximation error; afterwards, the opposite holds. The total loss thus has a single optimal basin, and the smallest sufficient horizon attains the minimum.

Seasonal Coverage and Horizon Selection The tolerance δ can be linked to an interpretable signal structure via seasonal coverage. Let A2 k = P f,j A2 f,j,k denote the total seasonal energy of client k, and define the τ-coverage horizon T (τ)

k as the smallest H for which the unresolved seasonal energy beyond H obeys:

X f,j:Tf,j,k>H

A2 f,j,k ≤(1 −τ) A2 k, (30)

assuming the residual seasonal loss satisfies L(k)

seas(H) ≤ A2 kr(H, T) with r(·, T) decreasing in H.

Corollary 1 (Coverage–Tolerance Mapping). If a coverage level τ is chosen so that (1−τ)A2 k ≤δ, then every H ≥T (τ)

k satisfies |∆L(k)

Bayes(H)| ≤δ. Thus, the optimal horizon is given by

H∗ k(δ) = max{ℓAR,k, T (τ)

k }. (31)

This provides a direct way to set the horizon using interpretable signal parameters: choose a desired seasonal coverage τ, infer the corresponding δ, and compute H∗ k(δ).

Federated Horizon Aggregation In federated learning, the server must choose a single global horizon Hserver despite heterogeneous client optima {H∗ k(δ)}. Because extreme clients (e.g., very large horizons) can substantially reduce effective sample sizes for all participants, robustness is crucial. Let wk ∝nk be data-proportional weights normalized so that P k wk = 1.

Robust Federated Horizon The global horizon can be defined via the weighted trimmed mean:

H∗ server = TrimMeanα

{H∗ k(δ)}K k=1; {wk}K k=1

(32)

which discards an α-fraction of the smallest and largest client-specific horizons (by weight) and averages the remainder.

This estimator is equivalent to minimizing a convex Huber-type aggregation objective and yields a horizon that balances most clients while avoiding inflation by a small number of extreme ones.

## Discussion

and Conclusion

Limitation and Discussion

This work proposes a principled framework for federated time-series forecasting under non-IID conditions, grounded in a structured synthetic data generator (SDG) and an intrinsic space formulation. The framework enables a precise decomposition of forecasting error and leads to a provably optimal look-back horizon. To make the analysis tractable and the theoretical guarantees possible, several assumptions are made that define the scope of applicability.

The SDG models additive components, e.g., trend, autoregressive memory, and seasonality, with Gaussian innovations. While this structure captures core dynamics observed in real-world data, it does not account for regime switches, nonlinear seasonal patterns, or cross-feature interactions beyond what is implicitly represented through PCA. The analysis assumes local stationarity and a stable autoregressive structure, which may be challenged in longmemory or near-unit-root settings. Additionally, estimating global covariance in a federated context requires secure or privacy-aware aggregation, and our sample efficiency analysis treats overlapping windows as approximately independent, which may overstate the effective sample size under certain data regimes.

These assumptions are common in theoretical work and are intentionally chosen to isolate the role of horizon length and data heterogeneity. Importantly, they enable the first provable characterization of optimal look-back windows in federated forecasting, providing a foundation for future extensions that relax these constraints.

## Conclusion

This paper introduces a principled framework for horizon selection in federated time series forecasting under non-IID conditions, grounded in a synthetic data generator (SDG) that models key temporal structures, trend, autoregressive memory, and seasonality, along with client-specific heterogeneity. By embedding time-series windows into a geometry-preserving intrinsic space, we enable a precise decomposition of forecasting loss into irreducible Bayesian error and model-dependent approximation error, each tied to the underlying statistical structure and data distribution. Our analysis reveals a fundamental trade-off: while the Bayesian loss decreases with horizon length as more temporal structure becomes identifiable, the approximation loss increases due to growing intrinsic dimension and reduced sample efficiency. This yields a provable result that the total loss is minimized at the smallest sufficient horizon H∗, where additional history no longer improves identifiability but exacerbates overfitting. Furthermore, we propose a robust aggregation strategy to identify a global horizon across clients. Together, these contributions establish the first theoretically grounded criterion for adaptive horizon selection in federated settings, offering practical guidance for model design, deployment, and benchmarking in decentralized, heterogeneous environments.

25829

<!-- Page 8 -->

## Acknowledgments

This work is partly supported by the Australian Research Council Linkage Project (Grant No. LP220200893).

## References

Akaike, H. 1974. A New Look at the Statistical Model Identification. IEEE Transactions on Automatic Control, 19(6): 716–723. Bahri, Y.; Dyer, E.; Kaplan, J.; Lee, J.; and Sharma, U. 2024. Explaining neural scaling laws. Proceedings of the National Academy of Sciences, 121(27): e2311878121. Box, G. E. P.; Jenkins, G. M.; Reinsel, G. C.; and Ljung, G. M. 2015. Time Series Analysis: Forecasting and Control. Hoboken: Wiley, 5th edition. Edwards, T. D. P.; Alvey, J.; Alsing, J.; Nguyen, N. H.; and Wandelt, B. D. 2024. Scaling-laws for Large Time-Series Models. arXiv preprint arXiv:2405.13867. Futoma, J.; Hariharan, S.; and Heller, K. 2017. Learning to detect sepsis with a multitask Gaussian process RNN classifier. In International conference on machine learning, 1174– 1182. PMLR. Hochreiter, S.; and Schmidhuber, J. 1997. Long Short-Term Memory. Neural Computation, 9(8): 1735–1780. Kairouz, P.; McMahan, H. B.; Avent, B.; Bellet, A.; Bennis, M.; Bhagoji, A. N.; Bonawitz, K.; Charles, Z.; Cormode, G.; Cummings, R.; et al. 2021. Advances and open problems in federated learning. Foundations and trends® in machine learning, 14(1–2): 1–210. Kim, J.; Kim, H.; Kim, H.; Lee, D.; and Yoon, S. 2025. A Comprehensive Survey of Deep Learning for Time Series Forecasting: Architectural Diversity and Open Challenges. Artificial Intelligence Review, 58(7). Kong, W.; Dong, Z. Y.; Jia, Y.; Hill, D. J.; Xu, Y.; and Zhang, Y. 2019. Short-term residential load forecasting based on LSTM recurrent neural network. IEEE Transactions on Smart Grid, 10(1): 841–851. Koparanov, K. A.; Georgiev, K. K.; and Shterev, V. A. 2020. Lookback Period, Epochs and Hidden States Effect on Time Series Prediction Using a LSTM Based Neural Network. In 2020 28th National Conference with International Participation (TELECOM), 61–64. Sofia, Bulgaria: IEEE. Lai, G.; Chang, W.-C.; Yang, Y.; and Liu, H. 2018. Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks. In Proceedings of the 41st International ACM SIGIR Conference on Research & Development in Information Retrieval, 95–104. New York, NY, USA: ACM. Levi, N.; and Oz, Y. 2024. The Underlying Scaling Laws and Universal Statistical Structure of Complex Datasets. arXiv preprint arXiv:2403.09756. Li, T.; Sahu, A. K.; Zaheer, M.; Sanjabi, M.; Talwalkar, A.; and Smith, V. 2020. Federated optimization in heterogeneous networks. Proceedings of Machine learning and systems, 2: 429–450. Lim, B.; Arık, S. ¨O.; Loeff, N.; and Pfister, T. 2021. Temporal fusion transformers for interpretable multi-horizon time series forecasting. International journal of forecasting, 37(4): 1748–1764. Liu, Y.; Hu, T.; Zhang, H.; Wu, H.; Wang, S.; Ma, L.; and Long, M. 2024. iTransformer: Inverted Transformers are Effective for Time Series Forecasting. arXiv preprint arXiv:2402.08372. McMahan, B.; Moore, E.; Ramage, D.; Hampson, S.; and y Arcas, B. A. 2017. Communication-Efficient Learning of Deep Networks from Decentralized Data. In Artificial intelligence and statistics, 1273–1282. PMLR. Perifanis, V.; Pavlidis, N.; Koutsiamanis, R.-A.; and Efraimidis, P. S. 2023. Federated Learning for 5G Base Station Traffic Forecasting. Computer Networks, 235(109950). Sharma, U.; and Kaplan, J. 2020. A neural scaling law from the dimension of the data manifold. arXiv preprint arXiv:2004.10802. Shi, J.; Ma, Q.; Ma, H.; and Li, L. 2024. Scaling Law for Time Series Forecasting. In Globerson, A.; Mackey, L.; Belgrave, D.; Fan, A.; Paquet, U.; Tomczak, J.; and Zhang, C., eds., Advances in Neural Information Processing Systems, volume 37, 83314–83344. Curran Associates, Inc. Takens, F.; Young, L.-S.; and Rand, D. 2006. Detecting Strange Attractors in Turbulence. In Dynamical Systems and Turbulence, Warwick 1980, 366–381. Berlin, Heidelberg: Springer Berlin Heidelberg. Toner, W.; and Darlow, L. 2024. An Analysis of Linear Time Series Forecasting Models. arXiv preprint arXiv:2403.14587. Woo, G.; Liu, C.; Sahoo, D.; Kumar, A.; and Hoi, S. 2023. Learning deep time-index models for time series forecasting. In International Conference on Machine Learning, 37217–37237. PMLR. Wu, C.; Wang, H.; Zhang, X.; Fang, Z.; and Bu, J. 2024. Spatio-Temporal Heterogeneous Federated Learning for Time Series Classification with Multi-View Orthogonal Training. In Proceedings of the 32nd ACM International Conference on Multimedia (MM ’24), 2613–2622. New York, NY, USA: ACM. Xu, Z.; Zeng, A.; and Xu, Q. 2024. FiTS: Modeling Time Series with 10K Parameters. arXiv preprint arXiv:2307.03756. Zador, P. L. 1982. Asymptotic quantization error of continuous signals and the quantization dimension. IEEE Transactions on Information Theory, 28(2): 139–149. Zeng, A.; Chen, M.; Zhang, L.; and Xu, Q. 2023. Are transformers effective for time series forecasting? In Proceedings of the AAAI conference on artificial intelligence, volume 37, 11121–11128. Zhou, H.; Zhang, S.; Peng, J.; Zhang, S.; Li, J.; Xiong, H.; and Zhang, W. 2021. Informer: Beyond efficient transformer for long sequence time-series forecasting. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 11106–11115. Zivot, E.; and Wang, J. 2006. Modeling Financial Time Series with S-Plus. New York, NY: Springer, 2nd edition.

25830
