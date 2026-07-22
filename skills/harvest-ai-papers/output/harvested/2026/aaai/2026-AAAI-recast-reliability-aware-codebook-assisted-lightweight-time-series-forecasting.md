---
title: "ReCast: Reliability-aware Codebook-assisted Lightweight Time Series Forecasting"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39610
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39610/43571
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# ReCast: Reliability-aware Codebook-assisted Lightweight Time Series Forecasting

<!-- Page 1 -->

ReCast: Reliability-aware Codebook Assisted Lightweight Time Series Forecasting

Xiang Ma1, Taihua Chen1,2, Pengcheng Wang1, Xuemei Li1, Caiming Zhang1

1Shandong University, Jinan, China 2Joint SDU-NTU Centre for Artificial Intelligence Research (C-FAIR), Shandong University, Jinan, China {xiangma,xmli,czhang}@sdu.edu.cn, {cfair-cth,pengchengwang}@mail.sdu.edu.cn

## Abstract

Time series forecasting is crucial for applications in various domains. Conventional methods often rely on global decomposition into trend, seasonal, and residual components, which become ineffective for real-world series dominated by local, complex, and highly dynamic patterns. Moreover, the high model complexity of such approaches limits their applicability in real-time or resource-constrained environments. In this work, we propose a novel REliability-aware Codebook- ASsisted Time series forecasting framework (ReCast) that enables lightweight and robust prediction by exploiting recurring local shapes. ReCast encodes local patterns into discrete embeddings through patch-wise quantization using a learnable codebook, thereby compactly capturing stable regular structures. To compensate for residual variations not preserved by quantization, ReCast employs a dual-path architecture comprising a quantization path for efficient modeling of regular structures and a residual path for reconstructing irregular fluctuations. A central contribution of ReCast is a reliability-aware codebook update strategy, which incrementally refines the codebook via weighted corrections. These correction weights are derived by fusing multiple reliability factors from complementary perspectives by a distributionally robust optimization (DRO) scheme, ensuring adaptability to non-stationarity and robustness to distribution shifts. Extensive experiments demonstrate that ReCast outperforms state-of-the-art (SOTA) models in accuracy, efficiency, and adaptability to distribution shifts.

## Introduction

In recent years, time series forecasting has gained significant attention due to its critical applications in various real-world applications, including finance, energy, healthcare, and industrial automation (Wen et al. 2023; Ma et al. 2023; Qiu et al. 2024; Shibo et al. 2025). Capturing complex and irregular temporal patterns accurately remains a primary challenge in this domain. Conventional approaches typically address this complexity by globally decomposing time series into trend, seasonal, and residual components, and modeling these components independently (Wu et al. 2021; Zhou et al. 2022; Hu et al. 2025). However, while effective for structured or periodic data, such global decomposition methods often underperform when faced with dynamic and noisy

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

real-world time series (Tang and Zhang 2025). Moreover, these methods typically involve considerable model complexity, which limits their practicality in resource-limited environments (Ansari et al. 2025).

To address these challenges, we introduce a novel REliability-aware Codebook-ASsisted Time series forecasting (ReCast) framework, focusing explicitly on capturing local patterns. Observing that many real-world series exhibit recurring local shapes rather than clear global regularities (Yeh et al. 2016), ReCast quantizes these local shapes into a learnable codebook, generating discrete embeddings to represent evolving patterns. This codebook-based representation not only captures salient local structures but also reduces model complexity, enabling a inherently lightweight forecasting design. Meanwhile, residual modeling is introduced to capture irregular variations not adequately represented by the quantized embeddings, ensuring robustness to fluctuations without excessively increasing model size.

Specifically, ReCast segments input into patches, quantifying each as discrete embedding using a dynamically updated reliability-aware codebook. As shown in Figure 1, a quantization path is used to forecast the future discrete embeddings, and a residual path learns to estimate the difference between input and its approximate representation reconstructed by discrete embedding. These two paths work in synergy: the quantization path enables lightweight forecasting of regular structures, while the residual path ensures the reliable reconstruction of irregular fluctuations. The prediction results combine outputs from both paths. To reduce overfitting and improve generalization to distribution shifts, we perform random patch sampling, and select only a subset of patches for training and codebook updates. Downsampling is applied prior to quantization, helping to highlight salient local structures and lower computational cost.

More importantly, it can be observed that the performance of ReCast strongly depends on the stability and adaptability of the codebook (Guo et al. 2023). Therefore, we propose an incremental codebook update mechanism centered on a reliability-aware scoring method. This method can robustly guide the update process in response to evolving data distributions, striking a balance between stability and adaptability. Our contributions include:

• We propose a codebook assisted lightweight forecasting framework that effectively captures both regular and ir-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

24299

<!-- Page 2 -->

…

MLP

𝑋−𝑋𝑞

𝑋𝑟

𝑌𝑟

𝑋𝑞 …

Residual path

…

Instance norm

Stage 1:Patch-wise quantization

𝑋

𝑃

… 𝑠1 𝑠2 𝑠𝐾 𝑠1 𝑠7 𝑠9 … 𝑄𝑥

Stage 2:Dual-path forecasting

Unpatching

Instance denorm

Patching

෠𝑌 𝑆

Quantization

𝑄𝑥= 𝑆(𝑃)

𝑞𝑖 𝑠1 𝑠7 𝑠9 …

MLP 𝑠7 𝑠4 𝑠6 … 𝑄𝑦

Quantization path

Reconstruction 𝑅𝑒𝑐(𝑄|𝑆)

𝑌𝑞

෨𝑃𝑡 center መ𝑆𝑡

Random sampling

Stage 3:Codebook construction and updating

Clustering …

Ƹ𝑠1 𝑡 Ƹ𝑠𝐾 𝑡 … Ƹ𝑠2 𝑡 ෤𝑝𝑖 𝑡 pseudo codebook

𝓛𝐩𝐫𝐞 cluster centers

Reliability-aware scoring

… updated codebook 𝑠1 𝑡 𝑠𝐾 𝑡 𝑠2 𝑡 Incremental updating

𝑆𝑡= 𝑆𝑡−1 + 1 𝑡(𝑊𝑡መ𝑆𝑡−𝑆𝑡−1)

𝓛𝒔𝒆𝒑

𝑆𝑡

Regularization … ෤𝑝𝑖 𝑡

… 𝑝𝑖 … current codebook

… at the t-th epoch

**Figure 1.** ReCast overview. It comprises patch-wise quantization, dual-path forecasting, codebook construction and updating.

regular local temporal patterns while significantly reducing model complexity. • We introduce a reliability-aware updating mechanism for codebook, which enhances adaptability and robustness to noise and distribution shifts with low computational cost. • Extensive experiments show that ReCast achieves superior accuracy, generalization, and robustness, relying on its lightweight architecture and efficient training strategy.

## Related Work

## 2.1 Deep Learning-based Forecasting

Recent advances in deep learning have significantly improved time series forecasting by leveraging powerful representation learning capabilities. The convolutional neural network(CNN)-based approaches (Wu et al. 2023) introduce local receptive fields to capture short-term dynamics efficiently, but they lack the ability to capture long-range dependencies. Transformer-based models (Liu et al. 2023; Nie et al. 2023) address this issue by employing self-attention to model global temporal interactions, achieving strong performance across benchmarks. Nonetheless, the quadratic complexity of attention and sensitivity to noise restrict their scalability and robustness in real-world scenarios. In parallel, lightweight MLP-based architectures (Tang and Zhang 2025; Ma et al. 2024) have recently emerged as promising alternatives, offering high efficiency but often struggling to represent heterogeneous and irregular patterns effectively.

## 2.2 Patch-based Representation Learning

To improve efficiency and capture fine-grained structures, patch-based strategies have gained increasing attention in time series modeling. Instead of processing sequences at raw temporal resolution, some methods (Wang et al. 2025; Nie et al. 2023; Tang and Zhang 2025) divide time series into non-overlapping or partially overlapping patches, enabling models to operate on compact representations and reduce sequence length. While effective in long-horizon forecasting, these methods typically rely on continuous embeddings without explicit mechanisms to leverage recurring local shapes, which are prevalent in real-world time series. Vector quantization (VQ) (Van Den Oord, Vinyals et al. 2017) provides a complementary perspective by discretizing local segments into a finite set of codewords, facilitating representation reuse and improving robustness, as extensively explored in domains such as vision and speech (Tian et al. 2024; Wu et al. 2025). Recent attempts (Shibo et al. 2025; Ansari et al. 2025) to integrate quantization into time series tasks demonstrate its potential to capture recurring patterns efficiently. However, static or heuristic codebooks fail to adapt to real-world data dynamics.

Different from existing methods, ReCast innovatively propose a dual-path forecasting architecture with quantization, capturing both stable recurring shapes and irregular fluctuations. Besides, it introduces a reliability-aware updating incrementally refines codebook, ensuring robust adaptation to distribution shifts.

## 3 Methodology In this section, we present

ReCast in detail, which has 3 modules: patch-wise quantization, dual-path forecasting, codebook construction and updating, as shown in Figure 1.

## 3.1 Patch-wise Quantization

Define the historical series as X ∈RC×L = {xi}L i=1, and the ground truth future values as Y ∈RC×H = {xi}L+H i=L+1.

24300

<!-- Page 3 -->

L and H are the length of the input and forecasting series, respectively. C means the number of variables (or channels). xi is a vector of dimension C at time step i. The goal of time series forecasting is to predict Y based on observed X. Re- Cast first normalizes the input using instance normalization, which is X = (X −µin)/ p σ2 in + ε. µin and σin denote the mean and variance of input, and ε is a small constant added for numerical stability. The normalized X is segmented into patches P = {pi}C×N i=1. pi ∈RLp is the i-th patch. Lp is the patch length, and N = ⌈L/Lp⌉.

Each patch is subsequently quantized by assigning it to the nearest codeword in a learnable codebook S = {sk}K k=1:

qi = S(˜pi) = arg min sk∈S

||˜pi −sk||2

2,

˜pi = Dsamp(pi), sk, ˜pi ∈RLp/2 (1)

where qi ∈{1, · · ·, K} is the discrete index associated with patch pi. K is the number of codewords. To reduce computational cost and suppress redundant local fluctuations, we apply downsampling Dsamp(·) on patches prior to quantization. This is supported by the well-established assumption in time series modeling that local patterns demonstrate invariance across scales and redundant morphology (Lu et al. 2022), which makes resolution reduction both meaningful and robust (Senin and Malinchik 2013). ˜pi is the downsampled patch of pi. This operation reduces the dimension of patches to Lp/2, significant savings in codebook matching, storage, and embedding projection. Besides, it helps the codebook focus on salient structures, improving robustness and generalization to noisy or distribution shifts. The discrete embeddings for the full input series is organized as Qx = [Q1; · · ·; QC], and Qi = {qj}i·N j=(i−1)·N+1 is the discrete embedding of i-th variable. This discrete embeddings serves as the input to downstream forecasting modules.

## 3.2 Dual-path Forecasting To simultaneously achieve computational efficiency and representational fidelity,

ReCast adopts a dual-path forecasting architecture. This design decomposes the prediction task into two complementary paths, each responsible for capturing distinct aspects of temporal dynamics.

Quantization path To capturing the regular structures and modeling the evolution of local patterns, a lightweight multilayer perceptron (MLP) Mquant is employed to forecast the discrete indices of future patches:

Qy = Mquant(Qx), (2)

where Qy ∈RC×Ny, and Ny = ⌈H/Lp⌉. This path enables compact and efficient modeling of stable local patterns.

Residual path While quantization promotes simplicity, it inevitably discards subtle variations. To mitigate this loss, ReCast introduces a residual correction branch. First, the input X is approximately reconstructed from its quantized representation via codebook lookup:

Xq = Rec(Qx|S) = Rec(Q1; · · ·; QC|S), Rec(Qi|S) = Usamp([sq(i−1)·N || · · · ||sqi·N ]), (3)

where Xq ∈RC×L denotes the approximate representation of X. Rec(Qi|S) means reconstruction from discrete embedding Qi using the codebook S. Usamp(·) denotes the upsampling. || denotes the concatenation. The residual component Xr = X −Xq captures fine-scale discrepancies. A separate MLP forecaster Mres is trained to predict the residual signal for the future window:

Yr = Mres(Xr), Yr ∈RC×H, (4) The final result combines both paths and is followed by instance denormalization to restore the original scale

ˆY = σin(Yq + Yr) + µin, ˆY ∈RC×H,

Lpre = ||ˆY −Y||1,

(5)

where Yq = Rec(Qy|S). To mitigate the distribution shift effect between the input X and forecasting result, we use instance denormalization by σin and µin. We employ the L1 Loss as the training objective to ensure robustness to outliers and stabilizes training.

## 3.3 Codebook Construction and Updating The performance and robustness of

ReCast are tightly coupled with the quality of its quantization codebook. Since real-world time series are often non-stationary and subject to distribution shifts, a static codebook is insufficient for capturing evolving local patterns. So, we adopt an incremental updating strategy for codebook construction, which allows the model to gradually refine its representation of local patterns based on data observed over time, as shown in stage 3 of Figure 1. This approach can enable adaptation to evolving distributions, and avoid the instability and overfitting associated with outliers.

Pseudo codebook construction At each epoch, we cluster the patches and obtain cluster centers. These centers are the representative local patterns that can be used to construct pseudo codebooks in the current epoch. The clustering objects are randomly sampled patches from the input. This random sampling reduces computational cost and prevents overfitting (Lu et al. 2022; Senin and Malinchik 2013). To ensure the efficiency, we express the energy function Lc of clustering in the form of matrix operation:

Lc = Tr((˜P t −MˆS t)⊤I(˜P t −MˆS t)), (6)

where ˆS t = {ˆst k}K k=1 and ˜P t = {˜pt i}C×Np i=1 denote the cluster center matrix and the sampled downsampled patches at t-th epoch, respectively. ˜pt i ∈RLp/2 is the i-th patch of ˜P t, and ˆst k ∈RLp/2 is the k-th cluster center of ˆS t. Np is the number of sampled patches. I is the weight matrix, here we take the identity matrix. Tr(·) is the trace of matrix. M ∈R(C×Np)×K is the indicator matrix to indicate the membership of patches, which is a learnable binary matrix. Mi,j = 1 means the patch i belong to cluster j. The update function of cluster center is:

ˆS t = (M⊤I˜P t)/(M⊤IM), (7)

the ˆS t reflects representative local patterns captured from the current training data distribution, which can serve as the pseudo codebook of t-th epoch.

24301

<!-- Page 4 -->

෡ܹ௧ Incremental updatingܵ

௧=ܵ ௧−1 + 1

ݐ(෡ܹ௧መܵ௧−ܵ ௧−1) weights Fusion by distributionally robust optimization (DRO)

Fusion by distributionally robust optimization࣓

∆࢚ joint energy࣓

࢐ࢋ,࢏࢚࣓ ࢐ࢋ࢚

መܵ௧ …

…

…ܵ ௧−1 current codebook pseudo codebook

෨ܲ௧ …

…࣓࢘ ࢋ࢖࢚ …

|| መܵ௧−ܵ௧−1||2

2 ||ܴ݁ܿ (መܵ௧(෨ܲ௧)| መܵ௧)−෨ܲ௧||2

2

Historical consistency Representational quality OOD sensitivity

**Figure 2.** Illustration of reliability-aware scoring, showing three scoring factors and their fusion via distributionally robust optimization (DRO).

Incremental updating To ensure generalization to new patterns or distribution shifts, and avoid drastic changes of embeddings, we introduce a incremental updating strategy for codebook to balance adaptability and stability. At the first epoch, we initialize the codebook as S1 = ˆS

## 1. In subsequent epochs, the codebook is updated as:

St = St−1 + 1 t (WtˆS t −St−1), (8)

where St denotes the codebook of t-th epoch. ˆS t is the pseudo codebook computed from the current epoch’s sampled patches via Equation 7. Wt is a set of correction weights that adjust the influence of the current epoch’s pseudo codebook. W t k is the weight for cluster center ˆst k. Equation 8 can ensure equitable contribution across epochs, while adaptively adjusting by Wt (See Appendix A.1 in the extended version for complete proof).

Embedding regularization To promote better utilization of the embedding space and prevent codeword collapse, we introduce a limited separation loss that encourages diversity among the cluster centers:

Lsep = log k X i,j=1 exp(−||ˆst i −ˆst j||2

2)/τ, (9)

where Lsep promotes the dispersion of embeddings in hidden space and prevents excessive expansion of the space by the temperature τ. τ = ||ˆS t||2

2 ensures the embedding space size remains approximately consistent across each epoch. This loss penalizes excessive similarity among codewords, encouraging a well-distributed and expressive codebook.

## 3.4 Reliability-aware Scoring As shown in Equation 8,

Wt can control the contribution of each pseudo codeword during updating. Rather than treating all cluster centers equally, ReCast introduces a reliabilityaware scoring method that selectively integrates pseudo codewords based on their reliability to ensure robust and adaptive codebook updates. Wt = {wt k}K k=1 is computed by aggregating three complementary factors: wt rep, wt

∆, wt je ∈ RK, and meets Wt ∝Mfus(wt rep, wt

∆, wt je), PK k=1 wt k = 1. Mfus is a fusion function.

Representational quality The wt rep evaluates how well ˆS t k represents its assigned patches, measured by the intracluster reconstruction error:

wt rep,k = 1 −exp(||Bk(Rec(ˆS t(˜P t)|ˆS t) −˜P t)||2

2)

exp(||Rec(ˆS t(˜P t)|ˆS t) −˜P t||2

2) + ε, (10)

where wt rep,k ∈wt rep is the weight assigned to the k-th cluster center. Bk is a binary matrix to mask values unrelated to the k-th cluster center. Rec(ˆS t(˜P t)|ˆS t) is the approximate representation reconstructed from discrete embeddings ˆS t(˜P t) using pseudo codebook ˆS t. Higher value of wt rep,k corresponds to better representational quality of the k-th cluster center, which has higher reliability.

Historical consistency The wt

∆assesses the temporal sta- bility of ˆS t k by measuring its deviation from the corresponding codeword in the previous epoch:

wt

∆,k = exp(||Bk(ˆS t −St−1)||2

2)

exp(||ˆS t −St−1||2

2) + ε, (11)

where wt

∆,k ∈wt

∆is the weight assigned to the k-th cluster center. Higher value of wt

∆,k denotes the greater difference between ˆst and st−1. Under the constraint of wt rep, this difference arises because St−1 lacks sufficient fitting capability for the newly input patches. So ˆS t should be given a greater weight to adjust the previous codebook, which is consistent with the expression of wt

∆,k.

OOD sensitivity The wt je measures the OOD sensitivity of ˆS t by capturing potentially novel or rare patterns, estimated from assignment frequency and variance. The function is similar to joint-energy (Duvenaud et al. 2020):

wt je,k = 1 − exp(PC×Np i=1 |˜pt i −ˆst k|)

exp(PK k=1

PC×Np i=1 |˜pt i −ˆst k|) + ε

, (12)

where wt je,k ∈wt je is the weight assigned to the k-th cluster center. Higher value of wt je,k indicates lower selection probabilities for the k-th cluster. By increasing its corresponding weight, we can prevent the embedding space of the codebook from collapsing into a few fixed codewords, and evaluate adaptability to OOD data (Duvenaud et al. 2020).

Fusion by distributionally robust optimization In Re- Cast, each pseudo codeword is associated with three normalized reliability scores: wt rep, wt

∆, and wt je. While these metrics are complementary, their relative importance may vary across epochs and data regimes. Directly assigning fixed weights can be suboptimal or unstable, especially when some metrics are noisy or biased due to transient data conditions (Duchi and Namkoong 2019). Thus, we formulate

24302

<!-- Page 5 -->

Models ReCast PatchMLP TQNet CycleNet iTransformer TimesNet PatchTST Dlinear

Metric MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE

ETTm1 0.371 0.379 0.374 0.382 0.377 0.393 0.379 0.396 0.407 0.410 0.400 0.406 0.387 0.400 0.403 0.407 ETTm2 0.265 0.309 0.269 0.311 0.277 0.323 0.266 0.314 0.286 0.327 0.291 0.333 0.281 0.326 0.350 0.401 ETTh1 0.437 0.428 0.438 0.429 0.441 0.434 0.457 0.441 0.454 0.447 0.458 0.450 0.469 0.454 0.456 0.452 ETTh2 0.347 0.385 0.349 0.378 0.378 0.402 0.388 0.409 0.383 0.407 0.414 0.427 0.387 0.407 0.559 0.515 ECL 0.163 0.257 0.171 0.265 0.164 0.259 0.168 0.259 0.178 0.270 0.192 0.295 0.216 0.304 0.212 0.300 Traffic 0.418 0.272 0.417 0.273 0.445 0.276 0.472 0.301 0.428 0.282 0.620 0.336 0.555 0.362 0.625 0.383 Weather 0.229 0.250 0.231 0.256 0.242 0.269 0.243 0.271 0.258 0.279 0.259 0.287 0.259 0.281 0.265 0.317 Solar 0.209 0.260 0.211 0.261 0.198 0.256 0.210 0.261 0.233 0.262 0.319 0.330 0.307 0.641 0.401 0.282

1st Count 12 2 2 0 0 0 0 0

**Table 1.** Performance Comparison. The best results are highlighted in bold, while the second-best results are underlined.

the fusion of reliability metrics as a distributionally robust optimization (DRO) problem (Qi et al. 2021). The goal is to obtain a conservative estimate of a codeword’s reliability by minimizing the expected reliability under the worst-case weighting distribution over the three metrics.

Formally, let the score vector for the k-th pseudo codeword at epoch t be denoted as:

zt k = [wt rep,k, wt

∆,k, wt je,k] ∈R3. (13)

Instead of computing a simple average, we consider all possible distributions θ ∈Θ3 over the three scores, where Θ3 = {θ ∈R3 | P3 i=1 θi = 1, θi ≥0}. We then define the reliability score wt k as the minimum expected value of zt k under the worst-case distribution within a KLdivergence neighborhood around the uniform distribution u = [1/3, 1/3, 1/3]:

ˆwt k = min θ∈Uγ⟨θ, zt k⟩, (14)

where Uγ = {θ ∈Θ3 | DKL(θ ∥u) ≤γ}. The parameter γ > 0 determines the size of the uncertainty set: smaller values encourage near-uniform weighting, while larger values permit more skewed, adversarial distributions. This robust optimization problem has a closed-form solution (See Appendix A.2 in the extended version for complete proof):

ˆwt k = −γ · log

3 X i=1 exp(− zt k,i γ). (15)

The result is a soft-minimum over the scores, allowing the most reliable metric to dominate while softly discounting others. This formulation can be interpreted as an entropyregularized minimization over reliability signals.

By adopting this distributionally robust fusion scheme, ReCast is able to adaptively and conservatively score pseudo codewords, mitigating the impact of outliers or transient inconsistencies in individual metrics. This not only enhances the stability of the incremental codebook update but also improves the generalization of non-stationary time series.

Finally, the reliability score ˆW t = { ˆwt k}K k=1 is used as a weighting coefficient to regulate the effect intensity of pseudo codewords in the codebook update. The Equation 8 can been improved as:

St = St−1 + 1 t (ˆW tˆS t −St−1). (16)

## 3.5 Learning Objective The final loss function is:

L = Lpre + wsepLsep, (17)

where wsep is adjustment parameters. During the inference phase, the codebook remains fixed, and only Equation 5 needs to be computed to efficiently obtain prediction results in a lightweight manner.

4 Experiments 4.1 Datasets and Baselines We evaluate the proposed ReCast on 8 widely used realworld datasets: Electricity (ECL), Traffic, Weather, Solar (Liu et al. 2022; Wu et al. 2021), and 4 ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2) (Zhou et al. 2021). To evaluate the performance of ReCast, we compare it against 8 representative SOTA models from recent years: Transformer-based models: TQNet (Lin et al. 2025), iTransformer (Liu et al. 2023), PatchTST (Nie et al. 2023); CNNbased model: TimeNet (Wu et al. 2023); MLP-based models: PatchMLP (Kong et al. 2025), CycleNet (Lin et al. 2024), DLinear (Zeng et al. 2023).

## 4.2 Metrics and Implementation Details The models are evaluated based on both Mean Squared Error (MSE) and Mean Absolute

Error (MAE). ReCast is implemented using Pytorch (Paszke et al. 2019) and trained on an Nvidia L40 GPU (48GB). The detailed implementations and the corresponding pseudocode of ReCast are provided in the extended version.

## 4.3 Main Results Table 1 compares the forecasting performance of

ReCast with baselines across 8 datasets, with lower MSE/MAE values indicating greater forecasting accuracy. ReCast achieves

24303

<!-- Page 6 -->

Setup Original -Residual -Updating -Random -Scoring -DRO

Metric MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE MSE MAE

ETTm1 0.371 0.379 0.377 0.395 0.400 0.402 0.377 0.396 0.385 0.399 0.375 0.385 Traffic 0.418 0.272 0.435 0.281 0.553 0.332 0.427 0.285 0.441 0.285 0.424 0.281 Weather 0.229 0.250 0.248 0.275 0.257 0.303 0.240 0.271 0.249 0.277 0.237 0.266

**Table 2.** Ablation study of ReCast.

## Model

iTransformer TimesNet Original +ReCast Original +ReCast

Metric MSE MAE MSE MAE MSE MAE MSE MAE

ETTm1 0.407 0.410 0.375 0.381 0.400 0.406 0.389 0.395

Traffic 0.428 0.282 0.420 0.275 0.620 0.336 0.499 0.303 Weather 0.258 0.279 0.231 0.259 0.259 0.287 0.245 0.272

**Table 3.** Portability of ReCast across different backbones.

the best performance in 12 out of 16 forecasting error metrics, demonstrating overall SOTA accuracy.

Notably, CNN-based models no longer retain a performance advantage due to their limited capacity in modeling long-range dependencies. Transformer-based models lies in modeling temporal contextual dependencies through attention mechanisms, which exhibit high sensitivity to noise. This inherent sensitivity limits their potential for further improving predictive performance. While they occasionally outperform simple MLP-based models, their performance is inconsistent, especially in noisy or irregular settings. Recent lightweight MLP-based models offer improved efficiency, but some of them often struggle to capture intricate intervariable dependencies.

Moreover, channel-independent models (PatchTST and DLinear) often fail to realize their full potential, suggesting the irreplaceable role of inter-variable interactions. In contrast, ReCast employs a shared codebook across all variables, implicitly facilitating inter-variable interaction and thereby circumventing the performance limitations inherent in channel-independent architectures.

## 4.4 Model Analysis

Ablation Study Four variants are designed to assess the contributions of ReCast’s core components:‘-Residual’ disables the residual path, retaining only the quantization path; ‘-Updating’freezes the codebook, preventing incremental updates; ‘-Random’removes both downsampling during quantization and random sampling during codebook construction; ‘-Scoring’ disables the reliability-aware fusion weights ˆWt in Equation 16, treating all pseudo codewords equally during codebook updates; ‘-DRO’ uniformly weights the three scores. These variants can systematically evaluate the effects of dual-path architecture, robust enhancement operation, incremental updating, reliabilityaware scoring, and DRO on model performance.

The results of Table 2 lead to several key observations:

0 50 100 150 200

0.20

0.22

0.24

0.26

MSE

Train time(ms/iter)

PatchTST

ReCast (ours)

TQNet

PatchMLP

CycleNet

TimesNet iTransformer

10M

1.0M 25ms

8.3M 195ms 6M 36ms

352k 18ms

12M 70ms

9.4M 70ms

1.2M 19ms

3M 1M

5M

Parameters

300k

DLinear 131k 18ms

**Figure 3.** Computational efficiency of ReCast on the ECL dataset (horizon = 720).

1) All ablated variants exhibit degraded performance relative to the full ReCast model, validating the effectiveness of each component. 2) The performance drop in ‘- Residual’ highlights the critical role of the residual path in recovering fine-grained variations that are lost during quantization. 3)The performance deterioration in ‘-Updating’ and ‘-Scoring’ confirms that both dynamic codebook refinement and reliability-aware weighting are essential for capturing evolving local patterns and ensuring adaptability to distribution shifts. 4) The degradation observed in ‘- Random’ underscores the importance of downsampling and random sampling for reducing overfitting and computational cost, while preserving performance. 5) The gap between ‘- Scoring’ and ‘-DRO’ reveals the importance of the DRObased fusion strategy, which avoids over-reliance on any single score and enables robust reliability estimation.

Portability To evaluate the portability of ReCast, we examine whether its dual-path forecasting architecture and reliability-aware codebook mechanism can generalize beyond the original MLP-based backbone. Specifically, we replace the MLP backbone with two widely used backbones: iTransformer, representative of Transformer-based methods, and TimesNet, representative of CNN-based methods. As reported on Table 3, integrating ReCast’s dual-path framework with either iTransformer or TimesNet improves forecasting performance. These results demonstrate that the proposed architecture is not tightly coupled with any specific backbone type and can be seamlessly adapted to a broad range of

24304

<!-- Page 7 -->

-50 -100

𝑺𝟏

𝑺𝟐

෡𝑺𝟐

෡𝑊2

Epoch 2

-50 -100

𝑺𝟏

𝑺𝟐 𝑺𝟑

෡𝑺𝟑 ෡𝑊3

Epoch 3

-50 -100 -100

-50

0

𝑺𝟏

Epoch 1

-50 -100

𝑺𝟏

𝑺𝟐 ෡𝑺𝟒

෡𝑊4

Epoch 4

𝑺𝟑

𝑺𝟒

100 0 50 -50 -100 -100

-50

0

50

100

111

Selected UnSelected

Past center Updated center 111 Updated center Past center

Different clusters

**Figure 4.** Visualization of codebook evolution and cluster assignments across epochs.

8 16 24 32 64 0.16

0.17

0.18

## 0.19 ECL ETTh2

K

8 16 24 32 64

ECL ETTh2

Lp

0.34

0.36

0.38

0.40

**Figure 5.** Parameter sensitivity.

forecasting models, thereby confirming its strong portability and general applicability.

Efficiency Benefiting from its lightweight dual-path architecture and a series of efficiency-oriented design choices, such as patch-wise quantization, residual correction, and selective sampling, ReCast achieves state-of-the-art forecasting accuracy while maintaining low computational overhead. As illustrated in Figure 3, ReCast consistently ranks among the top-performing models in terms of both parameter efficiency and training speed, without compromising predictive performance. These results highlight ReCast’s ability to strike a favorable balance between forecasting accuracy and computational complexity, making it well-suited for deployment in resource-constrained environments.

Parameter sensitivity Figure 5 shows the performance under different hyperparameters (the number of clusters (codewords) K and the patch length Lp).

## 4.5 Visualization

ReCast performs patch-wise clustering to generate discrete embeddings, its forecasting accuracy hinges on clustering quality and the representational capacity of the resulting cluster centers (codewords). To intuitively illustrate the codebook construction and update process, Figure 4 presents qualitative visualizations. The left side of Figure 4 shows clustering results over 8 clusters and the evolution of cluster centers across epochs, where each color denotes a distinct cluster. Despite random sampling, cluster assignments remain stable and centers converge smoothly, demonstrating the robustness of the clustering. The right side of Figure 4 illustrates the temporal dynamics of codebook updates. Taking epoch 2 as an example, the pseudo codebook ˆS

2 better fits the current data distribution than S1, and the reliabilityaware update assigns higher weight to ˆS

2, shifting S2 closer to it. This confirms that the proposed reliability-aware update mechanism effectively balances adaptation and stability, supporting robust and generalizable forecasting.

## 4.6 Limitations

Despite its demonstrated accuracy and efficiency, ReCast presents a notable practical limitation: As shown in Figure 5, its performance is sensitive to the choice of K and Lp. These parameters influence the trade-off between representational granularity and generalization capability to OOD patterns, yet are currently set empirically without adaptive or theoretical guidance. A promising direction is to scale ReCast to a pre-trained large language model with a richer codebook, diverse patch configurations, and heterogeneous time series pre-training, thereby improving robustness and reducing hyperparameter sensitivity.

## 5 Conclusion

In this work, we present ReCast, a novel codebook-assisted framework for reliable and efficient time series forecasting. Our dual-path architecture innovatively combines patchwise quantization for capturing recurring local patterns with residual modeling for recovering irregular variations, achieving an optimal balance between lightweight design and forecasting accuracy. The proposed reliability-aware codebook update mechanism, supported by a reliabilityaware scoring strategies, ensures robust adaptation to distribution shifts while maintaining stability. Extensive experiments across 8 real-world datasets demonstrate that ReCast outperforms SOTA baselines, achieving superior accuracy with significantly reduced computational complexity.

24305

<!-- Page 8 -->

## Acknowledgments

The authors appreciate the financial support by the National Natural Science Foundation of China (NSFC) Joint Fund with Zhejiang Integration of Informatization and Industrialization under Key Project (Grant Number U22A2033), the Postdoctoral Fellowship Program of CPSF under Grant Number GZC20251643, the NSFC under Grant Number 62576193.

## References

Ansari, A. F.; Stella, L.; Turkmen, A. C.; Zhang, X.; Mercado, P.; Shen, H.; Shchur, O.; Rangapuram, S. S.; Arango, S. P.; Kapoor, S.; et al. 2025. Chronos: Learning the Language of Time Series. Transactions on Machine Learning Research. Duchi, J.; and Namkoong, H. 2019. Variance-based regularization with convex objectives. Journal of Machine Learning Research, 20(68): 1–55. Duvenaud, D.; Wang, J.; Jacobsen, J.; Swersky, K.; Norouzi, M.; and Grathwohl, W. 2020. Your classifier is secretly an energy based model and you should treat it like one. In International Conference on Learning Representations (ICLR), volume 4. Guo, H.; Peng, S.; Yan, Y.; Mou, L.; Shen, Y.; Bao, H.; and Zhou, X. 2023. Compact neural volumetric video representations with dynamic codebooks. Advances in Neural Information Processing Systems, 36: 75884–75895. Hu, Y.; Liu, P.; Zhu, P.; Cheng, D.; and Dai, T. 2025. Adaptive multi-scale decomposition framework for time series forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 17359–17367. Kong, Y.; Wang, Z.; Nie, Y.; Zhou, T.; Zohren, S.; Liang, Y.; Sun, P.; and Wen, Q. 2025. Unlocking the power of lstm for long term time series forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 11968–11976. Lin, S.; Chen, H.; Wu, H.; Qiu, C.; and Lin, W. 2025. Temporal Query Network for Efficient Multivariate Time Series Forecasting. In Forty-second International Conference on Machine Learning. Lin, S.; Lin, W.; Hu, X.; Wu, W.; Mo, R.; and Zhong, H. 2024. Cyclenet: Enhancing time series forecasting through modeling periodic patterns. Advances in Neural Information Processing Systems, 37: 106315–106345. Liu, M.; Zeng, A.; Chen, M.; Xu, Z.; Lai, Q.; Ma, L.; and Xu, Q. 2022. Scinet: Time series modeling and forecasting with sample convolution and interaction. Advances in Neural Information Processing Systems, 35: 5816–5828. Liu, Y.; Hu, T.; Zhang, H.; Wu, H.; Wang, S.; Ma, L.; and Long, M. 2023. iTransformer: Inverted Transformers Are Effective for Time Series Forecasting. arXiv preprint arXiv:2310.06625. Lu, Y.; Wu, R.; Mueen, A.; Zuluaga, M. A.; and Keogh, E. 2022. Matrix profile XXIV: scaling time series anomaly detection to trillions of datapoints and ultra-fast arriving data streams. In Proceedings of the 28th ACM SIGKDD conference on knowledge discovery and data mining, 1173–1182.

Ma, X.; Li, X.; Fang, L.; Zhao, T.; and Zhang, C. 2024. Umixer: An unet-mixer architecture with stationarity correction for time series forecasting. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 14255– 14262. Ma, X.; Li, X.; Feng, W.; Fang, L.; and Zhang, C. 2023. Dynamic graph construction via motif detection for stock prediction. Information Processing & Management, 60(6): 103480. Nie, Y.; Nguyen, N. H.; Sinthong, P.; and Kalagnanam, J. 2023. A Time Series is Worth 64 Words: Long-term Forecasting with Transformers. In The Eleventh International Conference on Learning Representations. Paszke, A.; Gross, S.; Massa, F.; Lerer, A.; Bradbury, J.; Chanan, G.; Killeen, T.; Lin, Z.; Gimelshein, N.; Antiga, L.; et al. 2019. Pytorch: An imperative style, high-performance deep learning library. Advances in neural information processing systems, 32. Qi, Q.; Guo, Z.; Xu, Y.; Jin, R.; and Yang, T. 2021. An online method for a class of distributionally robust optimization with non-convex objectives. Advances in Neural Information Processing Systems, 34: 10067–10080. Qiu, X.; Hu, J.; Zhou, L.; Wu, X.; Du, J.; Zhang, B.; Guo, C.; Zhou, A.; Jensen, C. S.; Sheng, Z.; et al. 2024. TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods. Proceedings of the VLDB Endowment, 17(9): 2363–2377. Senin, P.; and Malinchik, S. 2013. Sax-vsm: Interpretable time series classification using sax and vector space model. In 2013 IEEE 13th international conference on data mining, 1175–1180. IEEE. Shibo, F.; Zhao, P.; Liu, L.; Wu, P.; and Shen, Z. 2025. Hdt: Hierarchical discrete transformer for multivariate time series forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 746–754. Tang, P.; and Zhang, W. 2025. Unlocking the Power of Patch: Patch-Based MLP for Long-Term Time Series Forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 12640–12648. Tian, K.; Jiang, Y.; Yuan, Z.; Peng, B.; and Wang, L. 2024. Visual autoregressive modeling: Scalable image generation via next-scale prediction. Advances in neural information processing systems, 37: 84839–84865. Van Den Oord, A.; Vinyals, O.; et al. 2017. Neural discrete representation learning. Advances in neural information processing systems, 30. Wang, M.; Yang, J.; Yang, B.; Li, H.; Gong, T.; Yang, B.; and Cui, J. 2025. Towards Lightweight Time Series Forecasting: a Patch-wise Transformer with Weak Data Enriching. arXiv preprint arXiv:2501.10448. Wen, Q.; Zhou, T.; Zhang, C.; Chen, W.; Ma, Z.; Yan, J.; and Sun, L. 2023. Transformers in time series: a survey. In Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, 6778–6786. Wu, C.; Chen, X.; Wu, Z.; Ma, Y.; Liu, X.; Pan, Z.; Liu, W.; Xie, Z.; Yu, X.; Ruan, C.; et al. 2025. Janus: Decoupling visual encoding for unified multimodal understanding

24306

<!-- Page 9 -->

and generation. In Proceedings of the Computer Vision and Pattern Recognition Conference, 12966–12977. Wu, H.; Hu, T.; Liu, Y.; Zhou, H.; Wang, J.; and Long, M. 2023. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis. In International Conference on Learning Representations. Wu, H.; Xu, J.; Wang, J.; and Long, M. 2021. Autoformer: Decomposition transformers with auto-correlation for longterm series forecasting. Advances in Neural Information Processing Systems, 34: 22419–22430. Yeh, C.-C. M.; Zhu, Y.; Ulanova, L.; Begum, N.; Ding, Y.; Dau, H. A.; Silva, D. F.; Mueen, A.; and Keogh, E. 2016. Matrix profile I: all pairs similarity joins for time series: a unifying view that includes motifs, discords and shapelets. In 2016 IEEE 16th international conference on data mining (ICDM), 1317–1322. IEEE. Zeng, A.; Chen, M.; Zhang, L.; and Xu, Q. 2023. Are Transformers Effective for Time Series Forecasting? In Proceedings of the AAAI Conference on Artificial Intelligence. Zhou, H.; Zhang, S.; Peng, J.; Zhang, S.; Li, J.; Xiong, H.; and Zhang, W. 2021. Informer: Beyond efficient transformer for long sequence time-series forecasting. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 11106–11115. Zhou, T.; Ma, Z.; Wen, Q.; Wang, X.; Sun, L.; and Jin, R. 2022. Fedformer: Frequency enhanced decomposed transformer for long-term series forecasting. In International Conference on Machine Learning, 27268–27286. PMLR.

24307
