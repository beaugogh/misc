---
title: "DFRec: Dual Fluctuation Modeling of Multi-level Intent Evolution for Next-Item Recommendation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38694
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38694/42656
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# DFRec: Dual Fluctuation Modeling of Multi-level Intent Evolution for Next-Item Recommendation

<!-- Page 1 -->

DFRec: Dual Fluctuation Modeling of Multi-level Intent Evolution for Next-Item Recommendation

Nengjun Zhu1*, Lingdan Sun1, Qi Zhang2, Jian Cao3, Hang Yu1

1School of Computer Engineering and Science, Shanghai University, China 2School of Computer Science, Tongji University, China 3School of Computer Science, Shanghai Jiao Tong University, China {zhu nj, sunld1127, yuhang}@shu.edu.cn, zhangqi cs@tongji.edu.cn, cao-jian@sjtu.edu.cn

## Abstract

User sequential behaviors are driven by a variety of complex and evolving intents. Capturing the dynamic change of user intents has become critical yet challenging in the next-item recommendation. Existing studies usually model the transition relationships among multiple intents within a session or integrate temporal information to capture the dynamic evolution of user intents. However, they struggle to identify the precise timing and magnitudes of intent changes, leading to ambiguity in providing consistent or violated recommendations and ultimately yielding subpar performance. To this end, we propose a novel framework called Dual Fluctuation Modeling of Multi-level Intent Evolution for Next-Item Recommendation (DFRec) in this paper. DFRec explicitly identifies the user intent changes and further quantifies the magnitude of the changes. Specifically, we assume that a user’s intent fluctuates around an inherent intent, with the magnitude of fluctuations indicating the extent of changes in user intents. Thus, we design an Emerging Intent Generation Module that employs a normal distribution with dynamic variance to capture intent fluctuations at each time step. Furthermore, we introduce a dual-layer dynamic variance update mechanism to capture fluctuation characteristics at different temporal levels, enhancing the representation of possible emergent intents. Extensive experiments on three realworld datasets verify DFRec’s superiority over state-of-theart baselines.

Code — https://github.com/vgeek-z/DFRec

## Introduction

Next-item Recommender systems (RS) aim to predict the user’s next action based on historical interactions. User intents are key factors determining users’ interactions with the next items (Zhu et al. 2020; Qin et al. 2024), as they reveal the underlying reasons behind user behaviors. Growing research attention is dedicated to intent modeling for enhanced next-item recommendations, thereby fostering the development of intent-based next-item recommendations. However, user intents are typically intricate and evolve dynamically with time, presenting significant challenges in capturing precise intent dynamics in intent-based recommendations.

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** An example illustrates user intent fluctuation and how emerging intent can be triggered in a shopping scenario.

To capture the dynamics of user intent, existing methods (Luo et al. 2020; Liu et al. 2020; Li et al. 2022a) typically model the transition relationships among multiple intents within a session. For example, ISRec (Li et al. 2022a) extracts the intents of users from sequential contexts, and then takes complex intent transitions into account through an intention graph. Alternative approaches (Zhang et al. 2022; Fan et al. 2021; Huang et al. 2023) explicitly or implicitly integrate temporal information to capture the dynamic evolution of user intents. These methods establish intent modeling and reveal its effectiveness to recommendation performance.

However, these methods face a key limitation: failing to identify the precise timing and magnitudes of intent changes, which results in limited performance improvement of current intent-based recommendations. Intuitively, let us consider a familiar shopping scenario where a user plans a winter vacation, as shown in Figure 1. The user’s initial interactions revolve around winter apparel. Herein, a sudden shift to engaging with a digital camera in the subsequent interaction signals a significant fluctuation in user intent, revealing an emerged intent (Zhu et al. 2024) on documenting the user’s vacation experiences. It is essential to promptly and accurately capture such intent fluctuations, as this enables nextitem RS to suggest a travel backpack in a more prominent position, rather than shoes within the apparel category.

Accordingly, we contend that it is crucial to identify the intent fluctuations and quantify the fluctuation magnitude

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16540

![Figure extracted from page 1](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

to understand the dynamic change of user intents effectively. Naturally, modeling user intent fluctuations precisely is an extremely challenging task. First, the uncertainty of user intent fluctuations makes it difficult to model the randomness of these fluctuations (CH1). Second, the contextdependency of intent fluctuations presents a persistent challenge in effectively incorporating intricate contextual cues to quantify the magnitude of the fluctuations dynamically (CH2).

In this paper, we propose a novel framework called Dual Fluctuation Modeling of Multi-level Intent Evolution for Next-Item Recommendation (DFRec) to address the above issues. DFRec generates multiple consecutive item segments and explicitly identifies the magnitude of changes in user intent between different segments. Specifically, we assume that a user’s intent fluctuates around an inherent intent, with the magnitude of fluctuations indicating the extent of changes in user intents. Thus, we start with the first item in the session and progressively include more items to generate multiple consecutive item segments. Then Emerging Intent Generation Module (EIGM) is proposed to probe users’ intent fluctuations at each time step, implemented by a normal distribution with dynamic variance. Herein, the user’s inherent intent in item categories serves as the base, while the variance from the base represents the magnitude of the user’s intent fluctuation at the current time step. Thus, the emerging intent representation can be captured through sampling at each time step. Compared to existing methods that directly vectorize user intent, our generative approach incorporates uncertainty to model the randomness of user intent fluctuation, effectively tackling the challenge CH1 and accordingly identifying intent fluctuations. To address the challenge CH2, we further design a Dual Intent Fluctuation Modeling (DIFM) mechanism to capture fluctuation characteristics across different temporal levels. The shortterm fluctuation variance primarily captures the immediate intent fluctuations between consecutive time steps, while the long-term fluctuation variance considers the intent fluctuation from the base over a time segment through a sliding window mechanism. Finally, Intent Fusion Module (IFM) introduces a novel attention mechanism to combine multiple consecutive item segments with the corresponding emerging intent representations at each time step to form the final session representation. The representation is then utilized to make recommendations.

Our key contributions are summarized as follows:

• We propose a novel framework, DFRec, which generates multiple consecutive item segments and explicitly identifies the magnitude of user intent changes between different segments. • We capture the extent of changes in user intents by modeling intent fluctuations at each time step, utilizing a normal distribution with a dynamically adjusted variance. • We design a dual variance update mechanism to model long- and short-term intent fluctuations simultaneously. • Extensive experiments on three real-world datasets show the superiority of our DFRec compared with various state-of-the-art solutions.

## Related Work

Many recent approaches have turned their attention to studying users’ intentions to improve the performance of recommender systems. Some studies assume that users’ decisions can be influenced by multiple intents. Thus they explore a user’s multiple latent intentions from their interaction sequence in different ways. MCPRN (Wang et al. 2019) has a channel for each implicit intent and uses a purpose routing network to detect the purpose of each item and assign it to the corresponding channel. MSGIFSR (Guo et al. 2022) treats a group of locally consecutive items in a session as user intents and uses a multi-granularity heterogeneous session graph to capture the interaction between different granularity intent units. MiaSRec (Choi et al. 2024) represents various user intents by deriving multiple session representations centered on each item and dynamically selecting the important ones. In addition, some methods (Li et al. 2022b; Gao et al. 2023; Wu et al. 2023) use unentangled representation learning to embed user or item representation into multiple sub-channels, each of which captures a specific user intent. Thus they can explore user intents at different factor levels. However, these methods focus solely on the diversity of user intentions while overlooking that the users’ intents change over time.

To model the dynamic change of user intents, MIT- GNN (Liu et al. 2020) proposes a multi-intent translation graph neural network to mine users’ multiple intents by considering the correlations of the intents. GSRec (Fan et al. 2021) designs a continuous-time bipartite graph, which captures temporal dynamics within the sequential patterns of user-item interactions. DIDN (Zhang et al. 2022) captures the user’s dynamic intentions by learning dynamic item embeddings that incorporate the temporal order of items within the session. As a significant auxiliary information for items, category information has been explored in recommendation areas. Besides, the work (Zhu et al. 2024) proposed decoupling user behaviors to distinguish between the user’s inherent intents and emerging intents. This approach primarily identifies items with emerging intent signals from the itemlevel attributes. Although the aforementioned approaches have been shown to enhance recommendation performance, they fail to account for the fine-grained modeling of the moments and magnitudes of intent changes. As a result, these methods may fail to model user intent comprehensively.

Unlike previous works, our approach explicitly identifies the intent fluctuations and quantifies fluctuation magnitude to model the extent of changes in user intents. We argue that users’ interaction patterns reflect the sequential fluctuation of their intents. Capturing the fluctuation in user intent beyond their inherent intents at a specific moment can reveal underlying, dynamically shifting intents.

The Proposed DFRec Problem Definition Let I = {e1, e2,..., ej,..., eN} and C = {c1, c2,..., cK} denote a set of items and a set of item categories, where N and K are the numbers of items and categories, respectively. Each item ej has an initial randomized embedding vj. Let

16541

<!-- Page 3 -->

Intent Generation Module Intent Fusion Module Intent Fluctuation Modeling Input

Sample

Sample

Sample

**Figure 2.** The framework of DFRec.

{S1, S2,..., Si,...} be a set of anonymous sessions, where Si = {ei

1, ei 2,..., ei j,...} represents a session, which is a collection of clicked items following the chronological order, and ei j ∈I is an item interacted at time index j. Given a session Si and its Ci, our task is to predict the next item with the highest recommendation scores.

Overall Framework

DFRec has three main components as shown in Figure 2.

1) Emerging Intent Generation Module (EIGM): it utilizes a normal distribution N(µt, σ2 t) with dynamic variance to capture the user’s intent fluctuation at each time step. First, the inherent intent of users for item categories is obtained through Dirichlet distribution, which is considered as the baseline or mean µ0 of user intent. Then, the user’s intent fluctuation is captured by the Dual Intent Fluctuation Modeling (DIFM) for each time step, modeled as the variance σ2 t at that moment and representing the extent of change in the user’s intent. Therefore, at each time step, the current user’s emerging intent representation is generated by sampling from N(µt, σ2 t), where µt = µ0. 2) Dual Intent Fluctuation Modeling (DIFM): it introduces a dual variance update mechanism to consider fluctuation characteristics across different temporal levels, enabling a more comprehensive capture of user intent fluctuations. Short-term variance is updated based on the differences between the current and previous time steps, capturing immediate intent fluctuations within a session. Long-term variance is updated by setting a sliding window over multiple time steps, considering the residuals and the difference between the current step’s intent and the inherent intent.

3) Intent Fusion Module (IFM): it generates multiple consecutive item units with different lengths and fuses them with the emerging intent representations using an attention mechanism, resulting in a comprehensive session representation.

Emerging Intent Generation Module (EIGM)

The uncertainty in user interaction behavior is reflected in the possibility that users may randomly deviate from their inherent intent and explore new options during a session. To identify the extent of changes in user intents, we capture the user intent fluctuations at a given time step by considering how much it exceeds their inherent intent. This reflects the user’s underlying and dynamically changing exploration and shifting behavior, such as exploring new item categories or a sudden increase in demand for certain specific categories.

To effectively model intent fluctuations, we utilize a normal distribution N(µt, σ2 t) with dynamic variance to adjust the intent deviation probabilistically at each time step. This generative approach incorporates uncertainty to model the randomness of user intent fluctuation and accordingly identify intent fluctuations. Assuming that the user’s intents fluctuate around the inherent intent µ0, the amplitude of these fluctuations is determined by the user’s current behaviors. Thus, the user’s emerging intent can be represented as:

µt+1 ∼N(µt, σ2 t) (1)

The item categories reflect user intents. We first obtain the user’s inherent intent for item categories through a Dirichlet distribution, which is considered as the baseline or mean µ0 of user intent. The Dirichlet distribution (Blei, Ng, and Jordan 2003) is a common prior distribution used in multinomial distributions, which naturally represents the user’s preference distribution over different item categories. Specifically, for each item category cj in the current session Si, we compute an intent relevance strength ˜ωj by incorporating the frequency ncj of category within the session and the category representation cj:

˜ωj = ReLU(W T cj + b) + λ · ncj (2)

where λ is a scaling factor, W ∈Rd×1 and b are trainable parameters. ReLU is an activation function that ensures the ˜ωj remains a positive value. Then, we sample the user’s interest distribution in each item category pi = (pi

1, pi 2,..., pi |Ci|) from the Dirichlet distribution as follows:

pi ∼Dirichlet(˜ωi

1, ˜ωi 2,..., ˜ωi |Ci|) (3)

where pi can be viewed as the coarse-grained intent distribution during the session Si, and |Ci| represents the number

16542

![Figure extracted from page 3](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-003-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

of categories in the Si. Then, the baseline of user intent µ0 is determined by:

µi

0 = X cj pi jcj (4)

Dual Intent Fluctuation Modeling (DIFM) Identifying the extent of changes in user intents can be considered as capturing the user’s intent fluctuations beyond the inherent intent at a certain moment, reflecting the user’s potential and dynamic exploration and shifting behaviors. Inspired by the GARCH (Bollerslev 1986), which is mainly used to model and predict volatility in financial data, we design a dual intent fluctuation mechanism to adjust users’ intent fluctuation dynamically. The core idea is to use the historical fluctuation and the change of user intent to predict future fluctuation, to dynamically update the amplitude of user intent fluctuation σt. When σt is larger, it indicates that the user’s intent fluctuation is stronger, and thus, a higher probability of emerging a new intent. In such a case, we should make a bold recommendation instead of exploiting existing behaviors discreetly.

First, the initial embedding vectors of items and categories in the current session Si are combined as the input ei:

ei t = vi t + ci t, t ∈{1,..., n} (5) Then we employ the Gate Recurrent Unit (GRU) to encode the current user’s historical interaction and the hidden state for each time step is obtained as follows:

..., hi t,... = GRU(..., ei t,...) (6)

To consider fluctuation characteristics across different temporal levels, we propose a dual intent fluctuation mechanism, which simultaneously considers both short-term and long-term fluctuation variances. Short-term variance is updated based on the differences between the current and previous time steps, capturing immediate intent fluctuations within a session. We first obtain the user’s intent offset for categories between the current and previous time steps:

ϵi t = ei t −ei t−1 (7)

Then, the fluctuation of short-term user intent, i.e., σshort t is predicted via historical fluctuation and the change of user intent as follows:

σshort t = α · ϵ2 t + β · σshort t−1

2 + γ · (ht −ht−1)2 (8)

where σshort t−1 denotes the short-term variance at t−1 step, ht denotes the hidden states fused with timing series. α, β, and γ are learnable parameters to tune the influence of each part.

Long-term fluctuations refer to changes in user intent over a longer time frame, where the differences between the current step’s intent and the inherent intent should be considered. To capture this level of fluctuation, we introduce a sliding window mechanism to track the long-term trend and the degree of fluctuations in user intent:

σlong t = 1 Nw t−1 X k=t−Nw ei k −µ0

2 + δ · (hk −µ0)2 (9)

where Nw denotes the length of the sliding window, and σlong t is the summation of intent fluctuation at the sliding window.

So far, the fused intent fluctuation variance σi t for session Si is obtained as follows:

σi t = σshort t + σlong t (10)

Intent Fusion Module (IFM) User intents exhibit hierarchy (Zhu et al. 2020), showing different focal points of intent over various time spans. To model the extent of changes in user intents more precisely, we propose an Intent Fusion Module (IFM), which composes the recommendation results from various granularity item segments and the corresponding emerging intents.

We first generate various granularity item segments for the current session Si and apply linear transformations to generate multi-level item units. Specifically, we start with the first item, progressively adding more items to form new segments. This allows us to capture the incremental changes in user intent at varying time granularities.

qi t = Wt(

X

{vj}j=1,...,t) (11)

where vi is the embedding of the ith item in session Si, and Wt ∈Rd×d, t = 1, 2,..., T refers to a learnable matrix. Besides, the emerging intent representation of each time step ri t can be sampled from the normal distribution N(µt, σ2 t) as in Eqn. (1). Thus qi t is further updated by incorporating emerging intent information as follows:

qi t = fc(concat(qi t, ri t)) (12)

where concat() is a concatenating operation and fc() represents a fully-connected layer network. Then these units are used to compute multi-head attention weights as follows:

αh = softmax

QWQ(KWK)⊤

√ d

(13)

where Q = (q1,..., qt)⊤∈Rt×d is the query matrix, K = (v1,..., vn)⊤∈Rn×d represents the hidden representation of each item in the sequence and WQ, WK ∈Rd×d are trainable parameters. h = 1, 2,..., H denotes the different attention head indexes. Then following (Zhang et al. 2023), we apply Lp-pooling to pool the attention map and multiply the hidden representation of the items in the sequence with the corresponding pooled attention weights to get the final session representation shybrid i.

shybrid i = concat

{si h}h=1,...,H

(14)

si h = n X j=1

ˆαj,hvj (15)

ˆαj,h =

" l−1 X m=0

(αj,mH+h)p

## 1 p

(16)

where ˆαj,h is the output of the pooling operator at the location (j, h), and αj,mH+h is the feature value within the pooling region. si h is the session representation under the hth head.

16543

<!-- Page 5 -->

## Model

Inference and Recommendation We utilize shybrid i to predict the recommendation scores of an item vj as the next items for a session Si:

ˆyij = σ(vi j

⊤shybrid i) (17)

where σ() is a sigmoid function. We formulate the learning objective as a cross-entropy loss function, which has been extensively used in recommender systems and is defined as:

L = −

X i log(ˆyij+) + log(1 −ˆyij−) (18)

where (i, j+) is a positive pair representing that item vj+ is a ground-truth for session Si, and instead, (i, j−) is a sampled negative pair and j−̸ = j+.

Complexity Analysis The time complexity of the DFRec is derived from several integral components. For EIGM, the complexity is O(TK), where T signifies the session length and K denotes the number of categories. In the dual-layer intent fluctuation modeling, the short-term fluctuation calculation, which involves the computation of the GRU hidden layer, has a complexity of O(Td2). while the long-term fluctuation has a complexity of O(TWd), where W represents the window size and d denotes the embedding dimension. The intent fusion module encompasses a multi-head attention mechanism with a time complexity of O(T 2d) and an Lp-pooling operation with a time complexity of O(Td). Overall, the total time complexity of the DFRec is O(TK + Td2 + TWd + T 2d + Td).

## Experiment

Experimental Setting Datasets. We conduct experiments on three datasets, i.e., (1) Yoochoose1: RecSys’15 Challenge dataset from an ecommerce website. (2) Jdata2: a challenge dataset hosted by JD corporation. It is filtered by a 1-hour duration to extract the session data. (3) Diginetica3: an e-commerce dataset composed of user purchasing behaviors.

For all datasets, we filter out the sessions whose length is less than 2 and the items that appear less than 5 times. Besides, we apply a data augmentation by treating the ith item as the label and the ones before the ith one as the input sequence. Dataset statistics are recorded in Table 1. The three datasets are chosen to diversify the number of categories, i.e., 12, 79, and 982, which can be used to evaluate their impacts. Baselines. We compare our DFRec with the following four types of baselines: conventional static approaches, i.e., BPR; typical session-based RSs, i.e., NARM and SASRec; graphbased RSs, i.e., SR-GNN, GCE-GNN, and SHARE; and intent-based RSs, i.e., DIDN, Atten-Mixer, and MiaSRec.

1) BPR (Rendle et al. 2012) optimizes the matrix factorization with implicit negative feedback using a pairwise loss

1https://www.kaggle.com/chadgostopp/recsys-challenge-2015 2https://jdata.jd.com/html/detail.html?id=8 3https://competitions.codalab.org/competitions/11161

Dataset Yoochoose Jdata Diginetica # of training sessions 189,166 221,879 153,387 # of test sessions 29,780 31,807 24,487 # of items 12,576 31,400 15,660 # of categories 12 79 982 average length 7.35 7.97 7.26

**Table 1.** Statistical information of evaluated datasets.

function. 2) NARM (Li et al. 2017) improves GRU4REC by incorporating attention into RNNs for session-based RSs. 3) SASRec (Kang and McAuley 2018) uses a transformer model with a single-head attention mechanism to recommend the next item. 4) SR-GNN (Wu et al. 2019) is the first to apply a gated graph convolutional network to establish transition relationships between items within a session. 5) GCE-GNN (Wang et al. 2020) exploits item transitions over the current and all-session graphs to learn session-level and global-level embeddings. 6) SHARE (Wang et al. 2021) utilizes hypergraph attention networks to exploit the contextual windows to model session-wise item representations. 7) DIDN (Zhang et al. 2022) designs a dynamic intent-aware module incorporating item-, user-, and temporal-aware information to learn dynamic item embeddings. 8) Atten- Mixer (Zhang et al. 2023) leverages both concept-view and instance-view readouts to achieve multi-level reasoning over3 item transitions to model multi-level user intent. 9) MiaSRec (Choi et al. 2024) represents various user intents by deriving multiple session representations centered on each item and selecting the important ones. Metrics. We employ commonly used Recall@K and NDCG@K (Normalized Discounted Cumulative Gain) to evaluate the recommendation results. Recall@K indicates the proportion of test cases in which the desired item appears in the Top-K items. NDCG@K takes the exact position of the correctly recommended items into account. Parameter Settings. In our experiments, models are tuned for their best performance using Adam to optimize the parameters. For example, the initial learning rate is 0.001 for all datasets. The batch size is set to 100 and the embedding dimension size is set to 256. In addition, the window size W in Eqn. (9) is searched in the ranges of {1, 2, 3, 4, 5, 6}.

Overall Performance

**Table 2.** illustrates the overall performance of our DFRec and the baselines on three datasets regarding Recall and NDCG metrics. We can have the following main observations:

First, DFRec generally outperforms all the baselines on all datasets, verifying the superiority of our model. For example, DFRec outperforms the best-performing baseline (i.e., MiaSRec) by 1.07% and the worst-performing sessionbased methods (i.e., NARM) by 12.19% on Jdata at Recall@5.

Second, the intent-based models (i.e., DIDN, Atten- Mixer, and MiaSRec) perform better than most models that fail to consider intent, such as SR-GNN, and SHARE. Among them, Atten-Mixer and MiaSRec consider multiple user intentions, leading to significantly improved per-

16544

<!-- Page 6 -->

## Method

Yoochoose Jdata Diginetica

R@5 N@5 R@10 N@10 R@5 N@5 R@10 N@10 R@5 N@5 R@10 N@10

BPR 20.36 30.40 30.40 16.69 19.15 12.34 28.14 15.24 18.94 12.26 27.89 15.15 NARM 68.11 60.59 72.35 61.97 32.41 25.18 39.73 27.55 57.46 72.04 77.44 72.68 SASRec 56.10 43.84 67.03 47.38 25.64 18.24 34.53 21.10 58.76 45.71 69.23 49.12 SR-GNN 72.93 60.54 74.46 61.03 41.78 27.81 46.13 29.22 77.14 72.22 77.78 72.42 GCE-GNN 69.87 60.04 74.97 61.71 33.87 23.47 43.71 26.67 76.59 71.77 78.49 72.39 SHARE 72.99 61.19 76.91 61.73 37.15 26.91 44.41 27.88 77.14 70.41 79.03 70.67 DIDN 70.54 60.03 75.81 61.73 36.77 26.16 46.64 29.37 76.34 69.47 78.29 70.43 Atten-Mixer73.51 64.83 77.57 66.23 40.27 32.09 47.87 34.55 77.77 72.54 79.32 73.05 MiaSRec 74.60 67.64 77.27 67.88 43.53 36.40 50.18 38.29 78.09 74.85 79.31 75.01

DFRec 75.16 69.48 77.85 69.55 44.60 37.58 50.71 39.56 78.18 75.26 79.40 75.21

*Bold value indicates the best performance in each column, and the value with an underline is the second-best one. * It shows that the performance of our work is significantly (p < 0.05) better than the second-best one based on a Wilcoxon test.

**Table 2.** Overall model performance on both datasets, with the metrics of Recall@K and NDCG@K (K=5, 10).

(a) Yoochoose (b) Jdata (c) Diginetica

**Figure 3.** Performance of variants of the proposed DFRec.

formance. However, they focus solely on the diversity of user intentions while overlooking their dynamic evolution. DIDN captures the user’s dynamic intentions by learning dynamic item embeddings that incorporate the temporal order of items within the session. However, this straightforward approach may overlook the complexity of user intention variation.

Compared with them, our DFRec captures multi-level user intentions by generating multiple consecutive item segments of varying lengths. Besides, we introduce intent fluctuation modeling to capture the emerging intention signals between different levels of user intent. Thus, diversity and dynamic variability of intent are simultaneously considered to generate recommendations. Especially by quantifying the amplitude of intent change, it’s more specific for DFRec to make discreet or bold recommendations, thus improving the recommendation performance.

Ablation Study To evaluate the effectiveness of each module in DFRec, we carry out multiple variants of DFRec. The variants’ performance is shown in Figure 3, where “all” represents DFRec in which all components are considered; the notation “w/o” represents the removal of an element, e.g., w/o-EIGM indicates the emerging intent generation modeling is removed from DFRec. w/o-DIFM-L and w/o-DIFM-S indicate that long-term and short-term fluctuation variances in DIFM are removed, respectively. Besides, we replace the corresponding continuous item segments with each time step’s item to evaluate the impact of fusing multi-level item segments, denoted as w/o-IFM.

We then have the following observations: 1) “all” outperforms others, showing the effectiveness of its structure. 2) Removing Emerging Intent Generation Module (EIGM) harms the model’s performance, i.e., the performance of “w/o-EIGM” is worse than “all”. It indicates that it is necessary to capture emerging intent signals by modeling user intent fluctuations explicitly. 3) The Recall and NDCG metrics on all datasets degrade regardless of whether short-term or long-term variances are removed. These show that dual variances are valuable signals to model intent fluctuation. 4) Dropping the fused modeling for continuous item segments shows a substantial decline compared to the whole model, reflecting that a set of continuous segments may contain richer information than a single item.

Parameter Analysis The window size Nw in Eqn. (9) determines how many timesteps of information are considered to capture long-term intent fluctuations of users. To evaluate its influence, we change the size from 1 to 6, and the results are shown in Figure 5. We can observe that the setting Nw = 2 for the Yoochoose datasets and dropout Nw = 3 for the Jdata datasets are generally proper to DFRec. The Recall and NDCG per-

16545

![Figure extracted from page 6](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

(a) Yoochoose (b) Jdata (c) Diginetica

**Figure 4.** Visualization of user intent fluctuation curves on three datasets. The color scale represents the fluctuation amplitude, with darker shades indicating higher values and lighter shades representing lower amplitudes.

(a) Yoochoose (b) Jdata

**Figure 5.** Impact of the size of window size.

formance decreases when the window size is set to a small or large value. This is because fewer time steps of interactions are inadequate to capture the user’s long-term information, but overmuch items make it easy to introduce noise.

Recommendation Diversity Evaluation We evaluate diversity metrics to verify the effectiveness of DFRec in capturing emerging intent signals. Following (Wang et al. 2019), we quantify diversity by utilizing the category distribution of recommendations, measured using information entropy.

Diversity@k = − k X i=1

Pri log2 Pri (19)

while Pri is the probability of the category to which item ei belongs and is estimated by the frequency. Figure 6 illustrates that the Diversity and Recall metrics increase on the Yoochoose and Jdata datasets as training progresses. This indicates the effectiveness of our model in capturing users’ emerging intent signals through intent fluctuation modeling. The results on Diginetica show similar observations, but like Figure 5, the related subfigure is not exhibited to save space.

Case Study We randomly sample 3 sessions from three datasets to visualize the users’ intent fluctuations learned by DFRec, respectively, as shown in Figure 4. We observe that the intent fluctuations vary between datasets. For Yoochoose, the magnitude of intent fluctuations is minimal, with the curve exhibiting a relatively smooth distribution, indicating stable user intents in this scenario. Conversely, for Diginetica, the

(a) Yoochoose (b) Jdata

**Figure 6.** Recommendation Diversity of DFRec.

curve shows pronounced fluctuations, suggesting substantial variations in user intents with noticeable differences between consecutive time steps. These observations align with the characteristics of the datasets: Yoochoose has a limited number of categories, 12; Jdata has a moderate number of categories, 79; and Diginetica contains the highest number of categories, 982.

## Conclusion

In this paper, we studied intent-modeling methods for the next-item recommendations and claimed that user intent fluctuations embedded in consecutive item segments can serve as the extent of changes in user intents. Accordingly, we proposed a novel framework called DFRec, which generates multiple consecutive item segments and explicitly identifies the magnitude of user intent changes between different segments. Specifically, we hypothesized that a user’s intent fluctuates around an inherent intent, with the magnitude of fluctuations indicating the extent of changes in user intents. Thus, we designed an Emerging Intent Generation Module to capture intent fluctuations at each time step, where larger fluctuations indicate a higher probability of emerging a new intent. Furthermore, we introduced a dual-layer dynamic variance update mechanism to capture fluctuation characteristics at different temporal levels. Finally, extensive experiments on real-world datasets validated the superiority of our model. There are potentially interesting directions for future work. For example, we can incorporate a large language model (LLM) to enhance the modeling of intent fluctuations by considering text attribute changes in sessions.

16546

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-dfrec-dual-fluctuation-modeling-of-multi-level-intent-evolution-for-next-item-re/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work is supported by National Natural Science Foundation of China under Grant No. 62202282 and 62406225.

## References

Blei, D. M.; Ng, A. Y.; and Jordan, M. I. 2003. Latent dirichlet allocation. Journal of machine Learning research, 3(Jan): 993–1022. Bollerslev, T. 1986. Generalized autoregressive conditional heteroskedasticity. Journal of Econometrics, 31(3): 307– 327. Choi, M.; Kim, H.-y.; Cho, H.; and Lee, J. 2024. Multiintent-aware Session-based Recommendation. In Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval, 2532–2536. Fan, Z.; Liu, Z.; Zhang, J.; Xiong, Y.; Zheng, L.; and Yu, P. S. 2021. Continuous-Time Sequential Recommendation with Temporal Graph Collaborative Transformer. In Proceedings of the ACM International Conference on Information and Knowledge Management, 433–442. Gao, R.; Tao, Y.; Yu, Y.; Wu, J.; Shao, X.; Li, J.; and Ye, Z. 2023. Self-Supervised Dual Hypergraph Learning with Intent Disentanglement for Session-Based Recommendation. Knowledge-Based Systems., 270(C). Guo, J.; Yang, Y.; Song, X.; Zhang, Y.; Wang, Y.; Bai, J.; and Zhang, Y. 2022. Learning Multi-granularity Consecutive User Intent Unit for Session-based Recommendation. In Proceedings of the International Conference on Web Search and Data Mining, 343–352. Huang, C.; Wang, S.; Wang, X.; and Yao, L. 2023. Modeling Temporal Positive and Negative Excitation for Sequential Recommendation. In Proceedings of the ACM Web Conference 2023, 1252–1263. Kang, W.-C.; and McAuley, J. 2018. Self-Attentive Sequential Recommendation. In Proceedings of the IEEE International Conference on Data Mining, 197–206. Li, H.; Wang, X.; Zhang, Z.; Ma, J.; Cui, P.; and Zhu, W. 2022a. Intention-Aware Sequential Recommendation With Structured Intent Transition. IEEE Transactions on Knowledge and Data Engineering, 34(11): 5403–5414. Li, J.; Ren, P.; Chen, Z.; Ren, Z.; and Ma, J. 2017. Neural Attentive Session-based Recommendation. In Proceedings of the ACM on Conference on Information and Knowledge Management, 1419–1428. Li, Y.; Gao, C.; Luo, H.; Jin, D.; and Li, Y. 2022b. Enhancing Hypergraph Neural Networks with Intent Disentanglement for Session-based Recommendation. In Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieve, 1997–2002. Liu, Z.; Li, X.; Fan, Z.; Guo, S.; Achan, K.; and Yu, P. S. 2020. Basket Recommendation with Multi-Intent Translation Graph Neural Network. In Proceedings of the IEEE International Conference on Big Data, 728–737.

Luo, A.; Zhao, P.; Liu, Y.; Zhuang, F.; Wang, D.; Xu, J.; Fang, J.; and Sheng, V. S. 2020. Collaborative Self-Attention Network for Session-based Recommendation. In Proceedings of the International Joint Conference on Artificial Intelligence. Qin, X.; Yuan, H.; Zhao, P.; Liu, G.; Zhuang, F.; and Sheng, V. S. 2024. Intent Contrastive Learning with Cross Subsequences for Sequential Recommendation. In Proceedings of the International Conference on Web Search and Data Mining, 548–556. Rendle, S.; Freudenthaler, C.; Gantner, Z.; and Schmidt- Thieme, L. 2012. BPR: Bayesian Personalized Ranking from Implicit Feedback. In Proceedings of the International Conference on Learning Representations, 452–461. Wang, J.; Ding, K.; Zhu, Z.; and Caverlee, J. 2021. Sessionbased Recommendation with Hypergraph Attention Networks. In Proceedings of the SIAM International Conference on Data Mining, 82–90. Wang, S.; Hu, L.; Wang, Y.; Sheng, Q. Z.; Orgun, M.; and Cao, L. 2019. Modeling Multi-Purpose Sessions for Next- Item Recommendations via Mixture-Channel Purpose Routing Networks. In Proceedings of the International Joint Conference on Artificial Intelligence, 3771–3777. Wang, Z.; Wei, W.; Cong, G.; Li, X.-L.; Mao, X.-L.; and Qiu, M. 2020. Global Context Enhanced Graph Neural Networks for Session-based Recommendation. In Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval, 169–178. Wu, H.; Zhang, Y.; Ma, C.; Guo, W.; Tang, R.; Liu, X.; and Coates, M. 2023. Intent-aware Multi-source Contrastive Alignment for Tag-enhanced Recommendation. In Proceedings of the IEEE International Conference on Data Engineering, 1112–1125. Wu, S.; Tang, Y.; Zhu, Y.; Wang, L.; Xie, X.; and Tan, T. 2019. Session-Based Recommendation with Graph Neural Networks. In Proceedings of the AAAI Conference on Artifcial Intelligence, volume 33, 346–353. Zhang, P.; Guo, J.; Li, C.; Xie, Y.; Kim, J. B.; Zhang, Y.; Xie, X.; Wang, H.; and Kim, S. 2023. Efficiently Leveraging Multi-level User Intent for Session-based Recommendation via Atten-Mixer Network. In Proceedings of the International Conference on Web Search and Data Mining, 168–176. Zhang, X.; Lin, H.; Xu, B.; Li, C.; Lin, Y.; Liu, H.; and Ma, F. 2022. Dynamic Intent-Aware Iterative Denoising Network for Session-Based Recommendation. Information Processing and Management., 59(3). Zhu, N.; Cao, J.; Liu, Y.; Yang, Y.; Ying, H.; and Xiong, H. 2020. Sequential Modeling of Hierarchical User Intention and Preference for Next-item Recommendation. In Proceedings of the International Conference on Web Search and Data Mining, 807–815. Zhu, N.; Sun, L.; Luo, X.; Cao, J.; Zhang, Q.; and Lu, X. 2024. Exploitation or Exploration Next? User Behavior Decoupling and Emerging Intent Modeling for Next-Item Recommendation. In Proceedings of the IEEE International Conference on Data Mining, 965–970.

16547
