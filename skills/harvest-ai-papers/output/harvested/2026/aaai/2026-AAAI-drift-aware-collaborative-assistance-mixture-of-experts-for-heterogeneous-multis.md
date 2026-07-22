---
title: "Drift-aware Collaborative Assistance Mixture of Experts for Heterogeneous Multistream Learning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38656
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38656/42618
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Drift-aware Collaborative Assistance Mixture of Experts for Heterogeneous Multistream Learning

<!-- Page 1 -->

Drift-aware Collaborative Assistance Mixture of Experts for Heterogeneous

Multistream Learning

En Yu, Jie Lu*, Kun Wang, Xiaoyu Yang, Guangquan Zhang

Australian Artificial Intelligence Institute (AAII) University of Technology Sydney (UTS), Australia

## Abstract

Learning from multiple data streams in real-world scenarios is fundamentally challenging due to intrinsic heterogeneity and unpredictable concept drifts. Existing methods typically assume homogeneous streams and employ static architectures with indiscriminate knowledge fusion, limiting generalizability in complex dynamic environments. To tackle this gap, we propose CAMEL, a dynamic Collaborative Assistance Mixture of Experts Learning framework. It addresses heterogeneity by assigning each stream an independent system with a dedicated feature extractor and task-specific head. Meanwhile, a dynamic pool of specialized private experts captures stream-specific idiosyncratic patterns. Crucially, collaboration across these heterogeneous streams is enabled by a dedicated assistance expert. This expert employs a multi-head attention mechanism to distill and integrate relevant context autonomously from all other concurrent streams. It facilitates targeted knowledge transfer while inherently mitigating negative transfer from irrelevant sources. Furthermore, we propose an Autonomous Expert Tuner (AET) strategy, which dynamically manages expert lifecycles in response to drift. It instantiates new experts for emerging concepts (freezing prior ones to prevent catastrophic forgetting) and prunes obsolete ones. This expert-level plasticity provides a robust and efficient mechanism for online model capacity adaptation. Extensive experiments demonstrate CAMEL’s superior generalizability across diverse multistreams and exceptional resilience against complex concept drifts.

## Introduction

Learning from streaming data has become fundamental to modern intelligent systems, enabling real-time decisionmaking in dynamic and continuously evolving environments (Cacciarelli and Kulahci 2024; Marcu and Bouvry 2024; Agrahari and Singh 2022). A central challenge in streaming learning is concept drift—the phenomenon where the underlying data distribution changes over time—requiring models to continuously adapt in order to maintain predictive performance (Lu et al. 2018). While most streaming learning studies focus on singlestream settings (Jiao et al. 2024; Wen et al. 2023), many

*Correspondence to Jie Lu and Xiaoyu Yang Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

real-world applications inherently involve multiple concurrent data streams. For example, a smart city platform integrates traffic sensor feeds, weather reports, public transportation logs, and social media sentiment streams. These streams evolve independently yet often carry latent correlations that, if exploited effectively, can provide complementary information for more accurate and robust decisionmaking (Xiang et al. 2023; Zhang et al. 2025a; Read and Zliobaite 2025; Ma et al. 2024). Capturing such dynamic inter-stream relationships while adapting to concept drift is crucial for advancing streaming learning toward practical deployment (Yang, Lu, and Yu 2025a; Xu, Chen, and Wang 2025; Liang 2025). Despite recent progress, existing multistream learning methods face a critical dilemma. On the one hand, most approaches operate under a homogeneous space assumption, which presumes that all streams share the same feature and label spaces (Yu et al. 2024; Jiao et al. 2023). This assumption fails to deal with the intrinsic heterogeneity commonly present in practical applications, where streams may originate from distinct feature spaces or predictive objectives due to different data sources (Korycki and Krawczyk 2021; Panchal et al. 2023). On the other hand, prevailing methods typically employ a monolithic and static architecture, either retrained or incrementally fine-tuned (Wang et al. 2021). This design suffers from critical limitations in multistream environments, e.g., retraining induces catastrophic forgetting of prior knowledge, while fine-tuning becomes fragile under asynchronous drifts, where adapting to one stream’s evolution can degrade performance on others. The lack of structural flexibility and targeted adaptation thus prevents robust performance across heterogeneous evolving streams.

To bridge this gap, we formalize the problem as Heterogeneous Multistream Learning (HML), where multiple concurrent data streams exhibit intrinsic heterogeneity, latent inter-stream correlations, and asynchronous concept drifts. Specifically, 1) Intrinsic Heterogeneity: feature and label spaces across streams differ in dimensionality and semantics, precluding direct application of homogeneous models; 2) Knowledge Fusion: while streams may contain useful correlations, such relationships are dynamic and selective, requiring mechanisms that can leverage relevant information while avoiding negative transfer from irrelevant streams; and 3) Asynchronous Concept Drifts: streams evolve in-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16199

<!-- Page 2 -->

dependently with diverse drift patterns, demanding flexible and stream-specific adaptation. These challenges necessitate a generalized and drift-aware learning framework that can handle stream-wise specialization while enabling intelligent knowledge fusion across heterogeneous drifting streams.

To address these challenges, we propose CAMEL, a dynamic Collaborative Assistance Mixture of Experts Learning framework tailored for heterogeneous data streams. It introduces a modular drift-aware architecture that explicitly addresses the three core challenges. First, to handle intrinsic heterogeneity, we assign each stream a specific learning system comprising a dedicated feature extractor, a private expert pool, and a task-specific prediction head, ensuring stream-specific specialization. Second, to enable adaptive and selective knowledge fusion, CAMEL incorporates a novel collaborative assistance mechanism. It employs a dedicated attention-based expert per stream that dynamically distills relevant contextual information from all other concurrent streams on demand, effectively capturing latent inter-stream correlations while inherently mitigating negative transfer (Vaswani et al. 2017). Third, to cope with asynchronous concept drifts, an Autonomous Expert Tuner (AET) is proposed, which monitors drift signals by a distribution-based drift detector and performance indicators per stream, dynamically adding new experts for emerging concepts and pruning obsolete ones. This expert-level plasticity allows our method to autonomously restructure its capacity and specialization over time. Extensive experiments on diverse synthetic and real-world multistream scenarios demonstrate the superior adaptability and generalization ability of our method compared to existing state-of-theart methods. In summary, our main contributions are:

• We propose CAMEL, a generalized and dynamic MoE framework that learns from multiple data streams characterized by heterogeneous features, diverse label spaces, and asynchronous concept drifts. • We introduce a collaborative assistance mechanism, where dedicated attention-based experts perform targeted knowledge fusion, providing an effective and adaptive solution to the challenge of positive knowledge transfer. • We design an autonomous tuning strategy that manages the expert lifecycle at a modular level (adding/pruning experts), offering a more robust and interpretable way for drift adaptation. • Comprehensive experiments and theoretical analysis validate the generalizability and robustness of our method across complex synthetic and real-world HML scenarios.

Related Works Stream Learning. Early research in streaming learning primarily addressed single-stream scenarios with concept drift (Wan, Liang, and Yoon 2024; Li et al. 2022; Kim, Hwang, and Whang 2024; Yu et al. 2025; Liang et al. 2025; Yang, Lu, and Yu 2025b), broadly falling into two paradigms: 1) informed methods integrate explicit drift detection mechanisms to trigger model adaptation based on distribution variations or error signals (Bifet and Gavalda

2007; Lu et al. 2025a; Gomes, Read, and Bifet 2019; Lu et al. 2025b), while 2) adaptive approaches employ detection-free strategies that continuously adjust model parameters in response to evolving data dynamics (Guo, Zhang, and Wang 2021; Brzezinski and Stefanowski 2013; Jiao et al. 2024). Recognizing the ubiquity of concurrent streams, recent multistream learning works can be summarized into two categories: 1) Multistream classification aims to transfer knowledge from labeled source streams to unlabeled targets, such as MCMO using multi-objective feature selection (Jiao et al. 2023), OBAL dynamically weighting streams via drift-aware boosting (Yu et al. 2024), and BFSRL learning fuzzy shared representations across streams (Yu, Lu, and Zhang 2024); 2) Multistream collaborative prediction exploits complementary information across streams for joint forecasting, typically adopting testthen-adapt schemes. For instance, Wang et al. (Wang et al. 2024) propose adaptive stacking that selectively retrains models for knowledge fusion during drift adaptation, while Wen et al. (Wen et al. 2023) employ dual-branch networks separately modeling temporal and cross-variable dependencies. Similarly, CORAL (Xu, Chen, and Wang 2025) leverages the kernel-induced self-representation method for coevolving time series. However, both paradigms predominantly assume homogeneous feature spaces and shared label semantics, fundamentally struggling with heterogeneous heterogeneity and asynchronous drifts. Mixture-of-Experts (MoE). The MoE paradigm achieves scalable, efficient modeling through conditional computation, where a routing mechanism dynamically activates specialized sub-networks ("experts") (Mu and Lin 2025; Lei et al. 2024). This architecture demonstrates strong capabilities in multi-task coordination and continual learning (Qin et al. 2020; Li et al. 2025; Lei et al. 2024) with its sparse activation property preserving computational efficiency while maintaining high model capacity (Sarkar et al. 2023; Tran, Pham et al. 2025; Yang et al. 2025). These inherent advantages naturally align with streaming learning’s core challenges, including complex pattern recognition, concept drift adaptation and computational constraints. However, MoE frameworks remain largely unexplored for streaming scenarios while exhibiting critical limitations in HML: expert specialization is statically predefined for coarse task categories without mechanisms to dynamically reconfigure expertise for dynamic scenarios, while routing strategies optimize isolated objectives while neglecting knowledge transfer between complementary experts. Our approach fundamentally advances this paradigm through a correlation-aware expert synthesis framework that jointly models latent task dependencies and expert synergies, enabling real-time expert reorganization and coordinated optimization of both routing precision and cross-expert knowledge transfer, unlocking adaptive capacity allocation for evolving data streams.

Preliminary Definition 1 (Heterogeneous Multistream Learning) Let S = {Si}n i=1 be a set of n concurrent data streams. Each stream Si is an ordered sequence of instances {(xi,t, yi,t)}∞ t=1, where xi,t ∈Xi ⊆RDi is the feature

16200

<!-- Page 3 -->

Multi-Head

Attention c

MLP layer

{𝐡𝑗,𝑡}𝑗≠𝑖 𝐡𝑖,𝑡 𝐜𝑖,𝑡

Assistance Expert

Key/Values Query

Context

Vector

Assistant Expert

Active Private Expert

Frozen Private Expert

Pruned Private Expert

𝑷𝒉𝒂𝒔𝒆 ❸ - Adapt & Train

Update all modules to state 𝓕𝒕 for the next round

Feature Extractor: 𝐡𝑖,𝑡= FE𝑖𝐱𝑖,𝑡, 𝜃FE 𝑖,𝑡−1

Classification Head:

𝐿𝑜𝑔𝑖= CH𝑖𝒇𝑖,𝑡; 𝜃𝐶𝐻 𝑖,𝑡−1

𝑷𝒉𝒂𝒔𝒆 ❶ - Test & Record via state 𝓕𝒕−𝟏 Get Data chunk 𝑊𝑡 {𝒮𝑖}𝑖=1 𝑛

Predict &

Record

Return to Phase ❶ ❷ based on state 𝓕𝒕

𝑷𝒉𝒂𝒔𝒆 ❷ - Diagnose & Decide

Drift Detector:

{DD𝑖,𝑡}

𝐀𝐄𝐓𝒊, 𝒕

No action Add & Freeze Prune

Routing Network: 𝒇𝑖,𝑡= RN𝑖,𝑡−1 ∗ (Eq. (6)）

MoE Privates & Assistance

Performance track

≈Get new Data chunk 𝑊𝑡+1 {𝒮𝑖}𝑖=1 𝑛

**Figure 1.** The overall framework of CAMEL. Concretely, each stream’s MoE module leverages a dynamic pool of private experts and a dedicated assistance expert that performs collaborative fusion via multi-head attention. The entire system follows a Test-Diagnose-Adapt cycle where an Autonomous Expert Tuner (AET) dynamically manages the expert lifecycle (adding/freezing/pruning) in response to drift and performance signals, ensuring continuous adaptation in the HML scenario.

vector from a stream-specific feature space of dimensionality Di, and yi,t ∈Yi = {1,..., Ci} is the corresponding class label from a stream-specific label space of size Ci. The underlying joint distribution P (i)

t (xi,t, yi,t) for each stream Si can change over time, exhibiting concept drift. The goal in HML is to design an adaptive mechanism F: {Xi →Yi}n i=1 that continuously adapts to predict new data from each stream.

As mentioned before, three main challenges must be addressed simultaneously in HML, i.e., Intrinsic Heterogeneity, Knowledge Fusion and Asynchronous Drifts. These challenges are defined as follows,

Challenge 1 (Intrinsic Heterogeneity) Real-world multistream scenarios exhibit intrinsic heterogeneity in both feature and label spaces across streams. For any pair of streams Si and Sj (i̸ = j), their respective feature spaces may differ in dimensionality (Di̸ = Dj) and attribute structure (Xi̸ = Xj), while their label spaces can define disjoint predictive tasks (Yi̸ = Yj implying Ci̸ = Cj).

Challenge 2 (Knowledge Fusion) While the streams S are heterogeneous, they may contain latent time-varying correlations that can be exploited for mutual benefit. The core challenge is to design a mechanism for selective and adaptive knowledge fusion. This requires simultaneously achieving two conflicting objectives for any given stream Si. First, the model must be able to identify and leverage useful contextual information from all other concurrent streams {Sj}j̸=i to enhance its predictive capability for Si. Second, it must be robust to dynamically ignore information from any stream Sj that is irrelevant or contains misleading patterns, thereby avoiding negative transfer.

Challenge 3 (Asynchronous Drifts) The non-stationarity of each stream Si presents that its data-generating distribution P (i)

t evolves with uncoordinated and diverse dynamics. These concept drifts are both asynchronous and diverse. Formally, for any two streams Si and Sj (where i̸ = j), ∃t, P (i)

t (y|x)̸ = P (i)

t+1(y|x) while P (j)

t (y|x) = P (j)

t+1(y|x). Furthermore, the drift patterns vary across streams in type (e.g., sudden, gradual, incremental).

## Methodology

We present the CAMEL framework to address the three fundamental challenges in HML. The core innovation lies in a drift-aware autonomous architecture that combines streamspecific specialization with cross-stream collaboration.

Overview of CAMEL As shown in Figure 1, we introduce CAMEL, a framework designed to learn a generalized model F by processing n data streams S in a window-based prequential manner. It features a modular architecture where each stream Si is assigned a dedicated learning system, including:

• A stream-specific Feature Extractor (FEi) for dimensionality and feature space alignment. • A Mixture of Experts (MoE) core, which includes a dynamic pool of Private Experts (PEi), a dedicated Assistance Expert (AEi), and a Routing Network (RNi). • A task-specific Classification Head (CHi) for handling heterogeneous label spaces.

16201

<!-- Page 4 -->

• A control loop comprising a Drift Detector (DDi) and an Autonomous Expert Tuner (AETi) for online adaptation. The online learning process begins with an initial model trained on the first window W0. Subsequently, for each incoming data window Wt (t ≥1), the system executes a Test-Diagnose-Adapt cycle, and the whole process is summarized in Algorithm 1.

Phase 1 – Test and Record. The cycle begins by evaluating the current model state Ft−1 (trained on Wt−1) on the new data of window Wt. For each instance (xi,t, yi,t), its feature vector xi,t is first projected by FEi,t−1 to an aligned representation hi,t. It is then processed by the dynamic MoE. Concretely, the RNi,t−1 computes routing weights to combine outputs from the PEi(t −1) pool, which captures idiosyncratic patterns, and the AEi,t−1, which performs collaborative fusion by attending to features {hj,t}j̸=i from all other streams. The resulting integrated feature vector is finally passed to the task-specific CHi,t−1 to produce a prediction ˆyi,t. The performance (e.g., accuracy) against the true label yi,t is then recorded for the subsequent phase.

Phase 2 – Diagnose and Decide. Following the test, the system diagnoses the state of each stream by the drift detector DDi. It analyzes the distribution of features {hi,t} from Wt to detect drift in P (i)

t. Concurrently, an autonomous expert tuner AETi,t evaluates the performance metrics from the test phase and the long-term utilization statistics of its experts. Based on these evidences, i.e., the drift signal and performance analysis, the AETi,t makes an adaptation decision: it may expand the private expert pool PEi(t) by adding a new expert to learn an emerging concept, or prune an underutilized expert to maintain model parsimony.

Phase 3 – Adapt and Train. Finally, the model architecture is updated based on the decisions from the diagnosis phase. The potentially modified model is then trained on the data from window Wt via an end-to-end process. The total loss aggregated from all stream-specific classification heads is back-propagated through the entire network. This step refines the parameters of all active components, preparing the system for the next window Wt+1. This cyclical process allows CAMEL to continuously learn, adapt, and specialize in a non-stationary multistream environment.

Heterogeneity-Aware Representation To handle the intrinsic heterogeneity, i.e., Challenge 1, our framework employs a hierarchical approach involving feature-level alignment and task-level specialization. 1. Feature Alignment. First, to address the feature space heterogeneity (Xi̸ = Xj), each stream Si is assigned a dedicated feature extractor FEi. This is a neural network, parameterized by θ(i,t)

FE, whose architecture is tailored to the input dimensionality Di. Its primary function is to project the raw feature vector xi,t into a common latent space H ⊂RDh:

hi,t = FEi(xi,t, θ(i,t)

FE), i ∈[1, n]; (1) This explicit dimensionality alignment creates a standardized input format for all subsequent expert networks, forming the foundation for inter-stream knowledge fusion.

## Algorithm

## 1 CAMEL: Online Learning

Process

Require: Data streams {Si}n i=1, Window size |Wi|, Total windows Tmax. Ensure: Predicted labels.

1: % Initial training on the first window W0 2: W0 ∈{Xi,0, Yi,0}n i=1 ←GetData({Si}n i=1, |Wi|, 0). 3: F0 ←Train(W0). % Test-then-Adapt loop for subsequent windows. 4: for t = 1: Tmax do 5: Wt ∈{Xi,t, Yi,t}n i=1 ←GetWindow({Si}n i=1, l, t) % Phase 1 – Test & performance record. 6: {Perfi,t}n i=1 ←Test(Ft−1, Wt) 7: Update {AETi,t} with stream-specific performances {Perfi,t}. % Phase 2 – Diagnose & Decide. 8: for i = 1: n do 9: drift_signali,t ←DDi,t.update(Hi,t) 10: (actioni,t, pe_idi,t) ← AETi,t(drift_signali,t, Perfi,t) 11: if actioni,t is "ADD_PRIVATE" then 12: Add a new private expert to PEi(t); 13: Freeze old private experts; 14: else if actioni,t is "PRUNE_PRIVATE" then 15: Prune Private Experts PEi(t)[pe_id] 16: end if 17: end for % Phase 3 – Adapt & Train. 18: Ft ←Train(Wt) 19: end for

## 2 Task

Specialization. Second, to address the label space heterogeneity (Yi̸ = Yj), our framework adopts a multi-task learning paradigm. Each stream Si is equipped with an independent task-specific classification head CHi parameterized by θ(i,t)

CH. It is responsible for mapping the final refined feature representation f i,t (derived by Eq. (6)) to the stream’s unique label space Yi:

Logitsi,t = CHi(f i,t; θ(i,t)

CH) ∈RCi, i ∈[1, n]; (2) This architecture ensures that the final decision-making process is tailored to each stream’s specific predictive task, whether it is binary classification or multi-class classification with a different number of classes.

Adaptive Knowledge Fusion To address the Knowledge Fusion, i.e., Challenge 2, CAMEL introduces a novel dynamic MoE architecture with collaborative assistance designed to exploit inter-stream correlations while mitigating negative transfer. 1. Private Experts: capturing stream-specific knowledge. For each stream Si, we maintain a dynamic pool of private experts PEi(t) = {pei,j|j = 1,..., Ki(t)}. Each expert pei,j is an MLP parameterized by θ(i,j,t)

pe, that learns patterns idiosyncratic to stream Si. It processes the aligned feature hi,t to produce representations in a common expert output space E ⊂RDf:

f pe i,j,t = pei,j(hi,t; θ(i,j,t)

pe) (3)

16202

<!-- Page 5 -->

## 2 Assistance

Experts: collaborative knowledge fusion. Each stream Si is paired with a dedicated assistance expert AEi parameterized by θ(i,t)

AE. This expert’s unique role is to perform collaborative knowledge fusion. It takes the target stream’s feature hi,t as a query and leverages features from all other concurrent streams {hj,t}j̸=i as context (keys and values) (Vaswani et al. 2017; Zhang et al. 2025b). We employ a multi-head attention mechanism:

ci,t = Attention(hi,t, {hj,t}j̸=i) (4)

The resulting context vector ci,t ∈RDh is a weighted summary of information from other streams, where the weights are learned based on relevance to hi,t. This contextual information is then fused with the input features to produce the assistance expert’s output representations:

f AE i,t = MLP(i,t)

AE (Concat(hi,t, ci,t); θ(i,t)

AE) ∈RDf (5)

This end-to-end mechanism allows AEi to learn what information to transfer from other streams and how to use it to best serve stream Si. 3. Routing and feature integration. A stream-specific routing network RNi parameterized by θ(i,t)

RN determines the credibility of each expert for a given input hi,t. It outputs a probability distribution pi,t over the Ki(t) private experts and the assistance expert. The final refined representations f i,t for stream Si are a weighted combination of all expert outputs:

f i,t = pi,t[AEi] · f AE i,t +

Ki(t) X j=1 pi,t[pei,j] · f pe i,j,t (6)

The routing mechanism provides a natural defense against negative transfer as it can learn to assign a near-zero weight to the assistance expert if the external context is irrelevant or even harmful.

Drift Detection & Adaptation Our framework’s autonomy and ability to handle asynchronous drifts (Challenge 3) stem from a per-stream control loop involving a drift detector and an expert tuner. 1. Drift Detection. Each stream Si is independently monitored by a Maximum Mean Discrepancy (MMD) based drift detector DDi (Wan, Liang, and Yoon 2024). DDi maintains a reference window W ref i,t of past features hs and compares it with the features from the current window Wi,t.

MMD2 i,t(Wi,t, W ref i,t) =

1 |Wi,t|

X hi,t∈Wi,t ϕ(hi,t) − 1

|W ref i,t |

X hj,t∈W ref i,t ϕ(hj,t)

2

Hk(7) where ϕ is a mapping to a Reproducing Kernel Hilbert Space Hk induced by a kernel (Smola et al. 2007). If MMD2 i,t > τMMDi, DDi signals a drift for stream Si. The reference window W ref i,t is then updated with Wi,t. 2. Autonomous Expert Tuner. To achieve robust and efficient adaptation, our framework employs an Autonomous Expert

Tuner (AETi) that governs the lifecycle of private experts for each stream Si. Relying solely on distribution-based drift detection (DDi) can be suboptimal, as not all statistical shifts necessarily degrade predictive performance (Lu et al. 2018), which could lead to unnecessary and costly model adaptations. Conversely, some performance degradation might occur without a detectable distribution shift in the feature space. Therefore, the AETi integrates two complementary signals, i.e., the drift signal from DDi and the stream’s recent test performance. This expert-level plasticity is the core mechanism for adapting model capacity online:

• Expert Adding: A new private expert is added to the pool PEi only when a drift is detected by DDi and the stream’s test performance Perfi,t exhibits a significant degradation. This conjunctive condition ensures that the model only expands its capacity when there is clear evidence of a detrimental concept change. The new expert is initialized as trainable to learn the emerging concept, while all existing private experts in PEi are frozen to prevent catastrophic forgetting, thereby preserving knowledge of past concepts. • Expert Pruning: A private expert pei,j (whether frozen or active) is pruned from PEi if its long-term average utilization, determined by the routing weights from RNi, falls below a threshold τutil. This proactive mechanism removes irrelevant experts that no longer contribute to the stream’s predictions, maintaining model parsimony and preventing the accumulation of obsolete components. Since each AETi operates independently based on its stream’s specific signals, the framework naturally handles asynchronous drifts.

Learning Objective This method is trained end-to-end. For a given data window Wt, the total loss is the sum of the individual cross-entropy losses from each stream-specific classification head:

Ltotal(Wt) = n X i=1

E(xi,j,yi,j)∈Wt,i

LCE(CHi(f i,t), yi,t)

, (8)

Theoretical Analysis The design of our method is theoretically grounded in multi-task learning principles (Maurer, Pontil, and Romera- Paredes 2016), which demonstrates that jointly learning related tasks can yield superior generalization over isolated learning. Our collaborative assistance mechanism enables intelligent knowledge fusion while mitigating negative transfer, and can be formally justified by: Theorem 1 (Generalization Bound) Let F be the hypothesis space defined by the CAMEL architecture, for any hypothesis h ∈F trained on streams S = {Si}n i=1, the expected risk Ri(h) on any stream Si is bounded as:

Ri(h) ≤ˆRavg(h) + C({Sj}n j=1) + O s log(n|Wt|)

n|Wt|

!

(9)

where ˆRavg(h) = 1 n

Pn j=1 ˆRj(h) is the average empirical risk across all streams and C({Sj}) quantifies the interstream dissimilarity. A proof sketch is in Appendix A.

16203

<!-- Page 6 -->

Synthetic

Set 1: Tree (Homo.) Set 2 Hyperplane (Homo.) Set 3 (Hete.) Set 4 (Hete.)

S1 S2 S3 avg S1 S2 S3 avg SEAa RTG RBF avg LED LEDDri Wave avg

SRP 58.47 65.14 64.63 62.74 86.37 87.59 88.21 87.39 83.35 70.05 81.18 78.19 35.18 36.65 83.80 51.88 AMF 56.18 63.76 59.59 59.84 91.32 90.70 90.70 90.91 83.65 66.19 90.29 80.04 37.85 25.31 79.39 47.52 IWE 63.49 72.35 68.39 68.07 89.82 91.39 90.90 90.70 84.27 64.38 70.12 72.92 36.05 34.15 80.41 50.20 MCMO 64.77 67.29 66.32 66.13 82.21 85.37 85.12 84.23 - - - - - - - - OBAL 65.72 67.97 65.60 66.43 84.14 86.73 88.66 86.51 - - - - - - - - BFSRL 63.37 67.42 64.39 65.06 84.67 87.20 88.47 86.78 - - - - - - - - CAMEL 65.78 68.27 66.48 66.84 91.85 92.12 91.84 91.94 85.14 67.73 92.75 81.87 38.19 35.36 85.43 53.00

Real-World

Set 5: TV News (Homo.) Set 6: Weather (Homo.) Set 7: Credit card (Hete.) Set 8: CoverT. (Hete.)

CNN BBC TIMES avg S1 S2 S3 avg S1 S2 S3 avg S1 S2 S3 avg

SRP 78.46 75.55 80.84 78.28 81.46 77.45 78.15 79.02 77.81 82.01 78.04 79.29 87.21 52.99 56.36 65.52 AMF 79.25 79.49 78.70 79.15 81.37 75.70 77.91 78.33 77.86 81.40 77.88 78.39 86.15 53.62 61.75 67.17 IWE 78.66 74.42 77.54 76.87 80.40 76.24 74.91 77.18 75.89 80.15 75.92 77.32 72.58 51.52 51.75 58.62 MCMO 68.83 60.12 59.74 62.90 75.11 75.02 73.37 74.50 - - - - - - - - OBAL 67.72 59.39 64.42 63.84 77.46 74.35 76.21 75.97 - - - - - - - - BFSRL 60.18 55.09 61.29 59.12 74.77 74.09 75.42 74.76 - - - - - - - - CAMEL 80.06 79.66 80.90 80.21 82.04 78.33 79.39 79.92 80.42 81.93 80.37 80.91 86.97 62.91 82.22 77.37

**Table 1.** Classification accuracy (%) of various methods on all benchmarks. The best and second-best results are highlighted in red and blue respectively. "-" means it is not applicable to the task.

Implication 1 Theorem 1 formally justifies CAMEL’s architecture: The assistance expert (AEi) minimizes C({Si}n i=1) through attention-based knowledge transfer, while the routing network (RNi) dynamically balances this against streamspecific private experts (PEi) to prevent negative transfer when dissimilarity is high. This intrinsic collaborationspecialization tradeoff combined with joint training’s sample efficiency (O(1/ p n|Wt|)) explains the empirical robustness. The autonomous expert tuner (AET) maintains adaptability to concept drift across windows through expertlevel plasticity.

## Experiments

In experiments, we first assess the framework’s generality and robustness across both homogeneous and heterogeneous settings. Second, we provide a qualitative analysis of the online adaptation process visualizing how the AET dynamically manages the private expert pool to concept drifts. Finally, we perform an ablation study to dissect the contribution of each core component, thereby validating our fundamental design principles. More detailed analysis and supplementary experiments can be seen in Appendix C.

## Experiment

Settings

Benchmarks. We establish eight diverse multistream scenarios. The first four scenarios are constructed from twelve synthetic data streams, meticulously designed to isolate specific challenges: homogeneous (Set 1 & 2) and heterogeneous (Set 3) feature spaces, and heterogeneous label spaces (Set 4). In addition, we employ four real-world multistream datasets, which inherently exhibit a mix of homogeneous and heterogeneous characteristics (Set 5-8). More detailed descriptions can be found in Appendix B.1.

Baselines. We conduct a comparison against six SOTA methods, including 1) Single-stream learning: SRP (Gomes, Read, and Bifet 2019), AMF (Mourtada, Gaïffas, and Scornet 2021) and IWE (Jiao et al. 2024); 2) Multistream classification: MCMO (Jiao et al. 2023), OBAL (Yu et al. 2024) and BFSRL (Yu, Lu, and Zhang 2024). The detailed description and implementation are provided in Appendix B.2 & B.3.

## Results

## Analysis

Overall Performance. Table 1 demonstrates that CAMEL consistently achieves SOTA average accuracy across almost all scenarios except for Set 1, validating its strong generality and robustness. The framework’s primary strength lies in its effective handling of the Intrinsic Heterogeneity (Challenge 1). Unlike contemporary multistream methods (MCMO, OBAL, BFSRL) which are confined to homogeneous settings and thus not applicable to our more realistic heterogeneous scenarios, our method thrives in these complex environments. This is enabled by its stream-specific modules (FEi, CHi), which provide the necessary specialization for each stream. Furthermore, compared against single-stream methods (SRP, AMF, IWE), CAMEL’s consistent top-tier performance validates its novel approach to the Knowledge Fusion (Challenge 2). While single-stream methods operate in isolation, our collaborative assistance mechanism successfully leverages latent inter-stream correlations. The attention-based experts perform targeted knowledge transfer, boosting the overall system performance. This dynamic interplay between specialized private experts managed by the AETi to address Asynchronous Drifts (Challenge 3), and the collaborative assistance experts allows it to strike a robust balance between focused learning and knowledge fusion. Consequently, our method excels across the full spectrum of HML challenges, proving its capability as a general and powerful solution for

16204

<!-- Page 7 -->

Variants

Set 3 Set 4 Set 6: Weather Set 7: Credit Card

SEAa RTG RBF avg LED LEDDri Wave avg S1 S2 S3 avg S1 S2 S3 avg

Base 80.28 64.37 81.42 75.36 29.21 21.96 76.94 42.70 74.32 73.17 73.21 73.57 74.29 77.24 74.02 75.18 Base+I 83.32 66.10 87.27 78.90 37.31 34.13 83.22 51.55 76.22 77.04 76.78 76.68 77.92 76.58 76.74 77.08 Base+I+DP 84.84 66.17 89.16 80.06 37.23 34.30 82.97 51.50 79.74 77.67 78.01 78.47 78.63 82.07 79.09 79.93 CAMEL 85.14 67.73 92.75 81.87 38.19 35.36 85.43 53.00 82.04 78.33 79.39 79.92 80.42 81.93 80.37 80.91

**Table 2.** Ablation study. Classification accuracy (%) of CAMEL’s variants. The best and second-best results are highlighted in red and blue, respectively.

diverse and evolving multistream environments.

Online Performance. Figure 2 qualitatively analyzes CAMEL’s online adaptation, plotting per-stream accuracy against the number of private experts. The results illustrate the ’drift-diagnose-adapt’ narrative and validate the Autonomous Expert Tuner (AET). For example, in Figure 2a, Stream 1 exhibits an accuracy dip at window 15, indicating concept drift. The AET correctly diagnoses this and responds by instantiating a new private expert, increasing model capacity and enabling swift performance recovery. Once the new concept is learned, the redundant expert is pruned (around window 20) to maintain model parsimony. Conversely, Stream 2 (without significant drift) demonstrates AET’s robustness: despite accuracy fluctuations, the private expert count remains constant, showing it avoids overreacting to inherent data noise (similar to Figure 2b). These behaviors highlight that CAMEL’s adaptation is highly selective, providing architectural plasticity precisely when and where needed to autonomously maintain high performance amidst asynchronous concept drifts. Additional visualizations are in Appendix C.1.

Ablation Study. To dissect component contributions, our ablation study progressively constructs the full CAMEL framework (Table 2) validating core design principles. Transitioning from the naive Base (full retraining) to Base+I (incremental learning) yields significant gains, confirming that continuous fine-tuning mitigates catastrophic forgetting. Integrating the Autonomous Expert Tuner (Base+I+DP) further improves performance on drifting streams (e.g., RBF: +1.89%), demonstrating expert-level plasticity effectively addresses Asynchronous Drifts (Challenge 3). The full CAMEL framework with collaborative assistance delivers the most substantial improvement, which empirically shows the attention-based mechanism masters Knowledge Fusion (Challenge 2) by distilling cross-stream knowledge for superior HML generalization.

## Conclusion

& Limitation In this paper, we introduced CAMEL, a novel autonomous Mixture of Experts framework designed to robustly handle the complexities of multistream learning. By assigning each stream a dynamic ensemble of specialized private experts alongside a dedicated collaborative assistance expert, our method effectively addresses intrinsic heterogeneity and facilitates adaptive knowledge fusion. In addition, an autonomous tuner manages the expert lifecycle at a modular

0.25

0.50

0.75

1.00

Acc.

Stream 1 Stream 2 Stream 3

0 20 40 60 80 100

1

2

Num. of pei, t

Stream 1 Stream 2 Stream 3

(a) Set 3: SEAa, RTG, RBF.

0.5

0.0

0.5

1.0

Acc.

Stream 1 Stream 2 Stream 3

0 200 400 600 800 0.50

0.75

1.00

1.25

1.50

Num. of pei, t

Stream 1 Stream 2 Stream 3

(b) Set 4: LED, LEDDrift, Waveform

**Figure 2.** Online accuracy and the corresponding number of private experts over time.

level and allows our method to dynamically adapt to concept drifts. A generalization bound based on multi-task learning theory formally connects inter-stream relatedness and routing decisions with task-level risk. Empirical results on diverse synthetic and real-world multistream settings demonstrate the superiority under HML challenges.

## Limitations

include suboptimal handling of recurring concepts through expert freezing and computational overhead from dynamic architecture adaptation. Future work will explore expert reactivation strategies and efficiency optimizations for resource-constrained environments.

16205

<!-- Page 8 -->

## Acknowledgments

The work was supported by the Australian Research Council (ARC) under Laureate project FL190100149 and Discovery Project DP220102635.

## References

Agrahari, S.; and Singh, A. K. 2022. Concept drift detection in data stream mining: A literature review. Journal of King Saud University-Computer and Information Sciences, 34(10): 9523–9540. Bifet, A.; and Gavalda, R. 2007. Learning from timechanging data with adaptive windowing. In Proceedings of the 2007 SIAM international conference on data mining, 443–448. SIAM. Brzezinski, D.; and Stefanowski, J. 2013. Reacting to different types of concept drift: The accuracy updated ensemble algorithm. IEEE transactions on neural networks and learning systems, 25(1): 81–94. Cacciarelli, D.; and Kulahci, M. 2024. Active learning for data streams: a survey. Machine Learning, 113(1): 185–239. Gomes, H. M.; Read, J.; and Bifet, A. 2019. Streaming random patches for evolving data stream classification. In 2019 IEEE International Conference on Data Mining, 240–249. IEEE. Guo, H.; Zhang, S.; and Wang, W. 2021. Selective ensemble-based online adaptive deep neural networks for streaming data with concept drift. Neural Networks, 142: 437–456. Jiao, B.; Guo, Y.; Yang, C.; Pu, J.; Zheng, Z.; and Gong, D. 2024. Incremental Weighted Ensemble for Data Streams with Concept Drift. IEEE Transactions on Artificial Intelligence, 5(01): 92–103. Jiao, B.; Guo, Y.; Yang, S.; Pu, J.; and Gong, D. 2023. Reduced-Space Multistream Classification Based on Multiobjective Evolutionary Optimization. IEEE Transactions on Evolutionary Computation, 27(4): 764–777. Kim, M.; Hwang, S.-H.; and Whang, S. E. 2024. Quilt: robust data segment selection against concept drifts. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 21249–21257. Korycki, Ł.; and Krawczyk, B. 2021. Concept drift detection from multi-class imbalanced data streams. In 2021 IEEE 37th International Conference on Data Engineering (ICDE), 1068–1079. IEEE. Lei, T.; Chen, S.; Wang, B.; Jiang, Z.; and Zou, N. 2024. Adapted-moe: Mixture of experts with test-time adaption for anomaly detection. arXiv preprint arXiv:2409.05611. Li, H.; Lin, S.; Duan, L.; Liang, Y.; and Shroff, N. 2025. Theory on Mixture-of-Experts in Continual Learning. In The Thirteenth International Conference on Learning Representations. Li, W.; Yang, X.; Liu, W.; Xia, Y.; and Bian, J. 2022. Ddgda: Data distribution generation for predictable concept drift adaptation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, 4092–4100.

Liang, D. 2025. DistPred: A Distribution-Free Probabilistic Inference Method for Regression and Forecasting. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1, 753–764. Liang, D.; Chen, J.; Wang, X.; Wang, Y.; and Li, S. 2025. DeepBooTS: Dual-Stream Residual Boosting for Drift-Resilient Time-Series Forecasting. arXiv preprint arXiv:2511.06893. Lu, J.; Liu, A.; Dong, F.; Gu, F.; Gama, J.; and Zhang, G. 2018. Learning under concept drift: A review. IEEE transactions on knowledge and data engineering, 31(12): 2346– 2363. Lu, P.; Lu, J.; Liu, A.; Yu, E.; and Zhang, G. 2025a. Autonomous Concept Drift Threshold Determination. arXiv preprint arXiv:2511.09953. Lu, P.; Lu, J.; Liu, A.; and Zhang, G. 2025b. Early Concept Drift Detection via Prediction Uncertainty. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 19124–19132. Ma, G.; Lu, J.; Fang, Z.; Liu, F.; and Zhang, G. 2024. Multiview classification through learning from interval-valued data. IEEE Transactions on Neural Networks and Learning Systems. Marcu, O.-C.; and Bouvry, P. 2024. Big data stream processing. Ph.D. thesis, University of Luxembourg. Maurer, A.; Pontil, M.; and Romera-Paredes, B. 2016. The benefit of multitask representation learning. Journal of Machine Learning Research, 17(81): 1–32. Mourtada, J.; Gaïffas, S.; and Scornet, E. 2021. AMF: Aggregated Mondrian forests for online learning. Journal of the Royal Statistical Society Series B: Statistical Methodology, 83(3): 505–533. Mu, S.; and Lin, S. 2025. A comprehensive survey of mixture-of-experts: Algorithms, theory, and applications. arXiv preprint arXiv:2503.07137. Panchal, K.; Choudhary, S.; Mitra, S.; Mukherjee, K.; Sarkhel, S.; Mitra, S.; and Guan, H. 2023. Flash: Concept drift adaptation in federated learning. In International Conference on Machine Learning, 26931–26962. PMLR. Qin, Z.; Cheng, Y.; Zhao, Z.; Chen, Z.; Metzler, D.; and Qin, J. 2020. Multitask mixture of sequential experts for user activity streams. In Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining, 3083–3091. Read, J.; and Zliobaite, I. 2025. Supervised Learning from Data Streams: An Overview and Update. ACM Computing Surveys. Sarkar, R.; Liang, H.; Fan, Z.; Wang, Z.; and Hao, C. 2023. Edge-moe: Memory-efficient multi-task vision transformer architecture with task-level sparsity via mixture-of-experts. In 2023 IEEE/ACM International Conference on Computer Aided Design (ICCAD), 01–09. IEEE. Smola, A.; Gretton, A.; Song, L.; and Schölkopf, B. 2007. A Hilbert space embedding for distributions. In International conference on algorithmic learning theory, 13–31. Springer.

16206

<!-- Page 9 -->

Tran, V.-T.; Pham, Q.-V.; et al. 2025. Revisiting Sparse Mixture of Experts for Resource-adaptive Federated Fine-tuning Foundation Models. In ICLR 2025 Workshop on Modularity for Collaborative, Decentralized, and Continual Deep Learning. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, Ł.; and Polosukhin, I. 2017. Attention is all you need. Advances in neural information processing systems, 30. Wan, K.; Liang, Y.; and Yoon, S. 2024. Online drift detection with maximum concept discrepancy. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2924–2935. Wang, K.; Lu, J.; Liu, A.; and Zhang, G. 2024. An Adaptive Stacking Method for Multiple Data Streams Learning under Concept Drift. In The 19th ISKE Conference on Intelligence Systems and Knowledge Engineering (FLINS-ISKE 2024), 267–274. World Scientific. Wang, K.; Lu, J.; Liu, A.; Zhang, G.; and Xiong, L. 2021. Evolving gradient boost: A pruning scheme based on loss improvement ratio for learning under concept drift. IEEE Transactions on Cybernetics, 53(4): 2110–2123. Wen, Q.; Chen, W.; Sun, L.; Zhang, Z.; Wang, L.; Jin, R.; Tan, T.; et al. 2023. Onenet: Enhancing time series forecasting models under concept drift by online ensembling. Advances in Neural Information Processing Systems, 36: 69949–69980. Xiang, Q.; Zi, L.; Cong, X.; and Wang, Y. 2023. Concept drift adaptation methods under the deep learning framework: A literature review. Applied Sciences, 13(11): 6515. Xu, K.; Chen, L.; and Wang, S. 2025. Coral: Concept drift representation learning for co-evolving time-series. arXiv preprint arXiv:2501.01480. Yang, M.; Lin, S.; Li, C.; and Chang, X. 2025. Let LLM Tell What to Prune and How Much to Prune. In Forty-second International Conference on Machine Learning. Yang, X.; Lu, J.; and Yu, E. 2025a. Adapting Multi-modal Large Language Model to Concept Drift From Pre-training Onwards. In The Thirteenth International Conference on Learning Representations. Yang, X.; Lu, J.; and Yu, E. 2025b. Walking the Tightrope: Autonomous Disentangling Beneficial and Detrimental Drifts in Non-Stationary Custom-Tuning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems. Yu, E.; Lu, J.; Yang, X.; Zhang, G.; and Fang, Z. 2025. Learning Robust Spectral Dynamics for Temporal Domain Generalization. In The Thirty-ninth Annual Conference on Neural Information Processing Systems. Yu, E.; Lu, J.; Zhang, B.; and Zhang, G. 2024. Online boosting adaptive learning under concept drift for multistream classification. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 16522–16530. Yu, E.; Lu, J.; and Zhang, G. 2024. Fuzzy Shared Representation Learning for Multistream Classification. IEEE Transactions on Fuzzy Systems, 32(10): 5625–5637.

Zhang, B.; Lu, J.; Song, Y.; and Zhang, G. 2025a. A Multistream Concept Drift Handling Framework via Data Sharing. IEEE Transactions on Cybernetics. Zhang, T.; Yu, E.; Shao, Y.; and Sun, J. 2025b. Multimodal Inverse Attention Network with Intrinsic Discriminant Feature Exploitation for Fake News Detection. arXiv preprint arXiv:2502.01699.

16207
