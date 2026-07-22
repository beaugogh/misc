---
title: "LLM Collaborative Filtering: User-Item Graph as New Language"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40816
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40816/44777
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# LLM Collaborative Filtering: User-Item Graph as New Language

<!-- Page 1 -->

LLM Collaborative Filtering: User-Item Graph as New Language

Huachi Zhou1, Yujing Zhang1, Hao Chen2*, Qinggang Zhang1, Qijie Shen3, Feiran Huang4, Xiao Huang1

1The Hong Kong Polytechnic University, Hong Kong 2City University of Macau, Macao 3Alibaba Group, China 4Jinan University, China {huachi.zhou, yu-jing.zhang, qinggangg.zhang}@connect.polyu.hk sundaychenhao@gmail.com, qjshenxdu@gmail.com huangfr@jnu.edu.cn, xiaohuang@comp.polyu.edu.hk

## Abstract

In collaborative filtering, learning effective embeddings for users and items from interaction data remains a central challenge. While recent efforts leverage large language models (LLMs) to enhance collaborative filtering, two critical limitations persist: (1) Efficiency: LLM-based inference is significantly slower than traditional embedding-based search; and (2) Topological Modeling: LLMs struggle to capture graph structures, which are essential for modeling multi-order useritem interactions. To address these limitations, we propose New Language Collaborative Filtering (NLCF), a framework that aligns LLMs with collaborative filtering by conceptualizing user-item graphs as new languages. This approach is based on two key insights: (1) LLMs excel at mastering new languages when trained on suitable corpora, and (2) the empirical conditional probability between tokens in corpora converges to the transition probabilities between nodes in graphs. NLCF translates user-item graphs into corpora, where users and items are treated as tokens. These corpora are used to fine-tune LLMs, and the learned representations are aggregated to construct user and item embeddings that encode multi-order interactions. Unlike methods that deploy LLMs for inference, NLCF distills LLM knowledge learned from corpora into compact embeddings, enabling both efficient training and real-time inference. The framework has been deployed on a billion-scale e-commerce platform for several months. Extensive experiments demonstrate that NLCF outperforms traditional graph CF models and LLM-based baselines while achieving significant training and inference efficiency improvement over LLM-based baselines.

## Introduction

Collaborative Filtering (CF) plays a pivotal role in recommender systems by suggesting new items to users based on the collaborative information that users with similar interactions share similar preferences (Yuan et al. 2023). Multiorder interactions which represent the multi-order relationships connecting users and items through various paths in the user-item graph enrich this information by uncovering

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** Comparison of pipelines between existing methods and NLCF. NLCF achieves efficiency through using short graph sentences for training and embeddings for inference.

preferences beyond immediate interactions. To model multiorder interactions, traditional models like LightGCN (He et al. 2020) achieve this by iteratively aggregating embeddings from immediate interactions in the user-item graphs to learn user and item embeddings. Recently, the capabilities of large language models (LLMs) (Chen et al. 2024; Hong et al. 2024) have inspired their application in CF. However, aligning LLMs with CF tasks remains challenging, as LLMs are optimized for natural language tasks rather than learning user and item embeddings based on user-item graphs.

Existing methods attempt to adapt LLMs for CF by transforming a user’s immediate interactions into natural language graph descriptions. These approaches can be broadly categorized into two classes: (i) Description Reasoningbased methods: These methods leverage LLMs’ natural language understanding to reason about collaborative information. For instance, TransRec (Lin et al. 2024b) constructs descriptive sequences from item identifiers, while LLM-CF (Sun et al. 2024) employs Chain-of-Thought prompting to distill collaborative information explicitly. (ii) Embedding Injection-based methods: Methods like LC- Rec (Zheng et al. 2024) and LETTER (Wang et al. 2024) inject user and item embeddings from traditional models (e.g., LightGCN) into prompts. By tokenizing collaborative embeddings and combining them with natural language descriptions, these methods aim to capture both semantic and collaborative information.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

35103

![Figure extracted from page 1](2026-AAAI-llm-collaborative-filtering-user-item-graph-as-new-language/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

Despite their potential, natural language graph description-based methods face one or both of the following limitations in efficiency and topological modeling for CF tasks.

(1) Multi-order Collaborative Information Loss: LLMs can process only a limited number of interactions at a time, making it extremely expensive to model multiorder interactions and the underlying collaborative information during training. While some methods inject collaborative embeddings into prompts (Zheng et al. 2024; Wang et al. 2024), fine-tuning LLMs on precomputed embeddings, rather than the original user-item graph, inevitably leads to information loss (Yang et al. 2024).

(2) Slow Inference: LLMs generate items token by token, with each token depending on the entire prompt (Zhao et al. 2023). The computational cost of generation scales with the prompt length. This sequential generation process, especially when using lengthy graph description prompts, significantly slows down inference compared to embedding-based search.

Although recent methods, e.g., LLMEmb (Liu et al. 2025) and LLM-CF (Sun et al. 2024), have proposed efficient inference mechanisms, they still focus on generating accurate user and item profile representations rather than modeling the user-item graph with LLMs. Given that user-item graphs have been proven highly effective for capturing multi-order collaborative information (Wei et al. 2024), modeling the graph with LLMs powerful learning ability is a promising direction. However, LLMs excel at learning a new language but find it challenging to efficiently learn from the graph with two key reasons:

(1) Structural Mismatch between Graph and LLM In- puts: User-item graphs are irregular, two-dimensional structures, while LLMs are designed to process onedimensional sequential data. Unlike graph CF models, which aggregate multi-order interactions through graph structure (Wu et al. 2020), LLMs lack a built-in mechanism to handle such graph structures.

(2) Computational Constraints: As the order increases, the number of multi-order interactions grows geometrically. Modeling these interactions while maintaining a concise representation is necessary since LLMs, containing billions of parameters, are computationally expensive during both fine-tuning and inference. And deploying LLMs in real-world recommender systems is particularly challenging due to latency constraints.

To address these challenges, we propose New Language Collaborative Filtering (NLCF), a novel framework that enables LLMs to efficiently learn collaborative embeddings by treating the graph as a new language. As shown in Figure 1, NLCF transforms the graph into concise corpus, where empirical conditional probabilities between tokens in the corpus converge to the transition probabilities between nodes in the graph. This transformation enables NLCF to model multi-order interactions, and then NLCF balances common and rare interactions in the corpus through similarity-based sampling. The resulting graph corpus is then used to finetune the LLM efficiently, allowing it to construct collaborative embeddings. NLCF achieves efficient training by using compact graph corpus rather than lengthy natural language graph descriptions, and efficient inference by leveraging collaborative embeddings instead of token-by-token generation. Our contributions are as follows:

• We propose NLCF, a novel framework that efficiently integrates LLMs with CF tasks to learn user and item collaborative embeddings by treating the user-item graph as a new language.

• We design two core modules: (i) a graph corpus collection module that transforms the graph into concise corpus, modeling multi-order interactions; and (ii) a collaborative embedding construction module that fine-tunes LLMs on this corpus to construct collaborative embeddings for efficient item search.

• Extensive experiments on three datasets show performance gains over both traditional graph CF and LLMbased baselines, with significant efficiency improvement over LLM-based baselines. Online A/B tests further validate NLCF’s effectiveness in industrial applications.

Preliminary

Notation. We represent the user-item graph as a tuple G = (V, E), where V = U ∪I denotes the union of user nodes U and item nodes I. The node set is indexed as {v1, v2,..., v|V|}, where |V| is the total number of nodes. The edge set E ⊆U × I represents user-item interactions, with cardinality |E|. These interactions are encoded in the adjacency matrix A ∈R|V|×|V|:

Aui =

1, if (vu, vi) ∈E, 0, otherwise. (1)

The bipartite structure ensures Aui = 0 for all user-user and item-item pairs. We fine-tune LLMs on user-item graph G with LoRA (Hu et al. 2021) ˆ W to learn user embeddings hvu and item embeddings hvi. More preliminary details are put in Appendix D.

New Language Collaborative Filtering

In this section, we present NLCF, an efficient framework that applies LLMs to learn collaborative embeddings from the user-item graph through new language learning. As shown in Figure 2, NLCF consists of two primary modules: (i) Graph Corpus Collection: The user-item graph is transformed into a new language corpus that encodes multi-order interactions. We retrieve this corpus by employing similarity-based sampling to reduce the computational burden. (ii) Collaborative Embedding Construction: The retrieved corpus is used to fine-tune LLMs, enabling the model to capture multi-order collaborative information. Hidden representations from the fine-tuned model are then aggregated to construct collaborative user and item embeddings for inference.

35104

<!-- Page 3 -->

1

5

4

2

6

7 8

User node Item node

9

Frozen

Tuned

Hash Function

1.

2.

1 3 7 4

9 5 2 1

1 3 7 4 1 4 7 3 9 5 2 1 8 6 2 1

1 1 4

1

Item Search

Collaborative Embedding Construction

1

1 p = 2

2 5 9

1 7 4 1 p = 5 p = 1

1

(b)

(d)

(a) (c)

(a) (b)

(c) (d)

Item Set

Aggregation

Graph Corpus Collection User-item Graph

1 2 5 9

1 4 7 1

Large Language Model

WA WB LoRA

Similarity-based Sampling

Random

Walk

Sampled Sentences

1

4 7

1

2

5 9

1

4 7

1 4

2

6 8

(a)

(c)

Hidden Representation 2 4 8 9

2 4 8 9

0.01 0.01 0.01 0.01 0.96

**Figure 2.** The overall pipeline of the proposed NLCF framework. NLCF treats the user-item graph as a new language. The framework consists of two key modules: in the top part, NLCF first collects graph corpus through random walks and then applies similarity-based sampling; in the bottom part, NLCF constructs collaborative user-item embeddings using fine-tuned LLMs for efficient item search.

Graph Corpus Collection

We begin by mapping basic concepts in user-item graph to their counterparts in graph language and then describe our similarity-based sampling strategy for reducing corpus size.

Definition of Graph Language-related Concepts. User and Item Nodes as Graph Tokens. We define the union of user and item nodes V as a set of unique graph tokens in this new language and extend the LLM tokenizer’s vocabulary accordingly. These newly added tokens have randomly initialized embeddings.

Graph Path as Graph Sentence. A connected sequence of nodes in the graph, or a path, forms a graph sentence in the corpus. For example, as shown in Figure 2, the path s1 = {v9, v5, v2, v1, v3} represents a graph sentence. These paths model multi-order interactions and capture collaborative information by revealing behavior similarity. For instance, v1 is likely to interact with v9 because the secondorder neighbor user v5 has previously interacted with v9. The initial corpus S = {s1, s2, s3,... } is composed of such sentences extracted from the user-item graph.

To extract graph sentences from the user-item graph, we employ random walks (Grover and Leskovec 2016), whose transition probability between nodes is defined as:

Pg(vi | vu) =

(Aui P j∈N (vu) Auj, vi ∈N(vu),

0, (vu, vi) /∈E,

(2)

where N(vu) denotes the neighbor set of node vu, and Aui represents the edge weight between nodes vu and vi. Each random walk continues walking until reaching a predefined length l. This process is designed to ensure that empirical conditional probability between tokens in resulting corpus converges to the transition probabilities between nodes in graphs. The guarantee is proved by the following theorem:

Theorem 1. Let Ps(vi|vu) be the empirical conditional probability computed from the corpus generated by a sufficiently large number of random walks. As the number of walks approaches infinity, Ps(vi|vu) converges in probability to Pg(vi|vu).

The proof is provided in Appendix A. To sufficiently capture collaborative information, we generate du sequences starting at each node vu, where du = P Au: is the degree of vu. This strategy yields the initial corpus S, which serves as the foundation for the following processing.

Similarity-based Sampling for Graph Corpus Reduction. The scale of possible graph corpus is proportional to the number of nodes and the average node degree. To limit the corpus size, traditional method, e.g., random sampling or node degree-based sampling does not account for subgraph density around each node. In dense subgraphs, random walks tend to generate highly overlapping sentences due to frequent visits to common nodes. Some existing LLM-based recommendation sampling methods (Lin et al. 2024a,c) focus on selecting important interactions for a small set of candidate items, which are incompatible with our goal of efficient item search from the entire item set (Zhou et al. 2025d). Other approaches rely on LLM fine-tuning (Zhou et al. 2025c) or LLM data integration to identify important samples (Wu et al. 2023) which would be computationally expensive to use.

We propose a similarity-based sampling strategy that addresses these limitations. Our approach groups similar graph sentences into clusters based on their sentence overlapping and assigns lower sampling probabilities to densely popu-

35105

![Figure extracted from page 3](2026-AAAI-llm-collaborative-filtering-user-item-graph-as-new-language/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-llm-collaborative-filtering-user-item-graph-as-new-language/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

lated clusters. By sampling representative sentences within a pre-defined budget, this strategy reduces redundancy while preserving essential collaborative information.

We measure the overlapping between any two graph sentences using the Jaccard similarity:

Ssimilarity(sp, sq) = |sp ∩sq|

|sp ∪sq|, (3)

where sp and sq represent two graph sentences. We then group sentences into clusters based on their pairwise similarities. A cluster Ci is defined as a set of sentences where each sentence shares a similarity above threshold t with all other sentences in the cluster:

Ci = sp ∈S: Ssimilarity(sp, sq) ≥t, ∀sq ∈Ci. (4) The size of each cluster |Ci| reflects the density of similar sentences within it. To achieve balanced representation, we assign higher sampling probabilities to sentences from larger clusters. The sampling probability for each sentence is normalized across all clusters:

P(sq) = |Ci| Pm j=1 |Cj|: sq ∈Ci, (5)

where m is the cluster number automatically determined by the algorithm. Then given a pre-defined sampling ratio α ∈ (0, 1], we sample sentences according to these normalized probabilities to create a representative subset:

S′ = sq ∼P(sq): sq ∈S, |S′| = α|S|. (6) This stratified sampling approach ensures balanced representation across clusters while maintaining computational efficiency within the specified budget constraints.

While computing pairwise similarities using Eq. (3) provides fine-grained clustering, it introduces a significant computational complexity of O(|S|2), which is impractical for large corpus. To address this challenge, we employ MinHash to efficiently estimate Jaccard similarities, whose efficiency is guaranteed by the following theorem: Theorem 2. Let J(sp, sq) be the Jaccard similarity between two graph sentences sp and sq. The MinHash estimator,

ˆJ(sp, sq), constructed from k independent hash functions, is an unbiased estimator of J(sp, sq) with a variance of

J(sp,sq)(1−J(sp,sq))

k. The proof is detailed in the Appendix B. This theorem demonstrates that MinHash provides a statistically sound approximation of the true Jaccard similarity. By generating compact signatures for each sentence and storing them in hash tables, we can identify similar sentences with an expected complexity of O(|S|), thus making the similarity estimation feasible for large-scale graph corpora.

Theoretical Analyses about Connection between Graph Corpus and Collaborative Information. The graph corpus collection module models multi-order interactions by transforming the two-dimensional user-item graph into a one-dimensional graph corpus. It is important to formally analyze whether this transformation quantitatively guarantees the preservation of multi-order collaborative information in the graph corpus. To address this, we present the following theorem:

Theorem 3. Let w denote the importance of node vi to node vu, as measured by the gradient norm of a GCN, and let w′ = n′

ˆn represent the empirical co-occurrence ratio, where n′ is the number of graph sentences containing both nodes vu and vi, and ˆn is the number of graph sentences containing node vu. The standard error of |w −w′|, is bounded by O

1

ˆn

.

Proof. Let h(l)

vu denote the hidden feature learned by GCN (Hamilton, Ying, and Leskovec 2017), defined as ReLU

1 du · P vj∈N (vu) Wlh(l−1)

vj

. For simplicity, we remove the non-linear activation function and GCN weights from the GCN aggregation in this proof. However, the theorem still holds when these components are included. The gradient of h(l)

vu with respect to h(0)

vi is given by:

∂h(l)

vu ∂h(0)

vi

= 1 du

· X vj∈N (vu)

∂h(l−1)

vj ∂h(0)

vi

.

We iteratively expand this formula using the chain rule to get:

∂h(l)

vu ∂h(0)

vi

= n X p=1

"

∂h(l)

vu ∂h(0)

vi

## p

= n X p=1 l′ Y q=1

1 dvq|p

= w, where n is the number of paths containing both nodes vi and vu, l′ is the length of the current path p, dvq|p represents the degree of the q-th node in the current path p. Since we use Eq. (2) and perform random walk, the probability of node vu visiting vi is exactly the same as the sum of probabilities for all paths shown above.

However, it is computationally impractical to retrieve all such paths for every pair of nodes, especially when similarity-based sampling is used. Let Xp be an indicator Bernoulli variable for the p-th walk in practice, which shows whether the walk successfully reaches node vi starting from vu:

Xp =

1 if the walk reaches vi, 0 otherwise.

From the previous theorem, the following expectation and variance properties hold: E[Xp] = w, and V ar(Xp) = w(1−w). Now, if there are ˆn paths from node vu to node vi, the empirical probability satisfies the following properties:

E

Pˆn p=1 Xp

ˆn

= w, and V ar

Pˆn p=1 Xp

ˆn

= w(1−w)

ˆn. This variance is bounded by 1. Therefore, the sampling standard error of the empirical probability w′, i.e., n′

ˆn encoded in the sampled corpus, satisfies:

|w −w′| = O

1

ˆn

.

In the proof, w represents collaborative information captured by GCNs in prediction by modeling multi-order interactions, while w′ denotes the importance derived from

35106

<!-- Page 5 -->

the sampled graph corpus as reflected by the empirical occurrence ratio. The theorem demonstrates that the sampled graph corpus encodes collaborative information in a manner consistent with GCNs, with the difference diminishing as the number of sampled graph sentences increases. This result provides a theoretical foundation for using graph sentences as a proxy for mining collaborative information underlying multi-order interactions.

Collaborative Embedding Construction Having transformed the user-item graph into a new language corpus rich in collaborative information, we proceed to fine-tune LLMs to incorporate this information. After finetuning, to enable efficient inference across the entire item set, we construct collaborative user and item embeddings by aggregating the hidden representations derived from the curated corpus.

Fine-tuning LLMs on the Corpus. Within these graph sentences, multi-order collaborative information enables distant tokens to influence the prediction of the next token in the sentence. To capture this collaborative information, we fine-tune LLMs by maximizing the likelihood of predicting the next token within the graph corpus. Formally, the finetuning objective is defined as:

Lpre = −

|S′| X q=1

|sq| X j=1 log P(sq,j | sq,<j, Wp, ˆ W), (7)

where Wp ∈R|V |×d is the learnable head layer parameter for predicting the next token. By optimizing this objective, the fine-tuned LLM learns to capture multi-order collaborative information embedded in the graph sentences. To control the memory usage, we incorporate the dynamic memory bank mechanism and the details are put in the Appendix E.

Graph Sentence Representation Aggregation. After fine-tuning, we obtain a well-trained LLM. However, directly deploying LLMs in an online recommender system would incur prohibitive latency. To address this issue, we precompute collaborative user and item embeddings offline, enabling efficient recommendation at inference time.

LLM is used to compute hidden representations for each graph token in the vocabulary:

hq,j = LLM({sq,1, sq,2,..., sq,j−1}), (8)

where hq,j represents the hidden representation of the j-th token in sentence sq, computed based on its preceding tokens sq,1, sq,2,..., sq,j−1.

To comprehensively encode multi-order collaborative information, we aggregate the hidden representations of the target user vu across multiple graph sentences. The aggregation is defined as:

hvu =

X p∈K hq,p,

K = {p: sq ∈S′, sq,p = vu, p = |sq| −k, 0 < k < |sq|}

(9) where K specifies the valid positions of the token vu across the sampled corpus S′, and k is a hyperparameter controlling the allowed positions of user vu within a sentence. The item embeddings are computed analogously through the same aggregation process.

By precomputing user and item embeddings offline, NLCF enables efficient real-time inference through simple inner product search with these embeddings, eliminating the need for costly LLM computations during serving.

## Experiments

We conduct extensive experiments on three real-world datasets to evaluate the effectiveness and efficiency of the NLCF framework. Our experimental study aims to address the following research questions: RQ1: How does NLCF perform compared to state-of-the-art graph CF and LLMbased baselines? RQ2: How do different design choices affect NLCF’s performance, particularly regarding sampling strategies and LLM backbone selections? RQ3: How sensitive is NLCF to key hyperparameters, such as sampling ratio and sentence length? RQ4: How does NLCF perform in real-world recommendation applications?

Experimental Settings

Datasets. We evaluate NLCF on three real-world datasets: Steam (Kang and McAuley 2018), ML-1M and ML- 10M (Harper and Konstan 2016). Details about these datasets are shown in Appendix F.1. Specifically, Steam contains 918,951 interactions, 41,008 users, and 2,438 items. ML-10M contains 2,340,369 interactions, 69,428 users, and 5,180 items. ML-1M contains 370,647 interactions, 4,869 users, and 1,818 items.

Baseline Methods. We compare NLCF with the following groups of baselines: Traditional Graph CF Baselines: (i) LightGCN (He et al. 2020),(ii) LightGCL (Cai et al. 2023),(iii) HMLET (Kong et al. 2022), and (iv) AFDGCF (Wu et al. 2024b); LLM-based Baselines: TransRec (Lin et al. 2024b), LLM-CF (Sun et al. 2024), LET- TER (Wang et al. 2024), LC-Rec (Zheng et al. 2024) and LLMEmb (Liu et al. 2025). Details about these baselines are shown in Appendix F.2. To evaluate the effectiveness of the similarity-based sampling approach, we compare it with random sampling.

Implementation Details. All experiments are conducted using publicly released codes, with each baseline running on one dedicated NVIDIA A100-SXM4-40GB GPU. The software environment is based on 20.04.6. The Python version is 3.9.22. We use the Hugging Face Transformers library 4.45.2. And we use metric Precision@N (Zhuang et al. 2025; Zhang et al. 2025) and NDCG@N (Zhou et al. 2023). More implementation details are shown in Appendix F.3.

Main Comparison (RQ1)

Tables 1 and 4 present the overall comparison across three datasets, revealing two key observations:

First, LLM-based approaches do not consistently achieve performance improvement over traditional graph CF approaches across all metrics. LLM-based approaches face

35107

<!-- Page 6 -->

challenges in effectively incorporating collaborative information from user-item graph. While methods like LC-Rec and LETTER attempt to integrate collaborative embeddings from traditional graph CF models, these methods that rely on intermediate embeddings instead of directly modeling multiorder interactions suffer from collaborative information loss. This limitation may explain their performance degradation as metric k increases and their inability to consistently outperform state-of-the-art graph CF models, particularly in Precision metrics.

Second, NLCF achieves the most superior performance across all three datasets, demonstrating a successful paradigm shift. Rather than relying on traditional graph CF methods to model multi-order interactions, NLCF enables LLMs to directly capture the collaborative information from the user-item graph, marking a paradigm shift.

Efficiency Comparison (RQ1) Table 2 presents the training and testing efficiency results across three datasets, revealing that most LLM-based baselines exhibit significantly longer training and inference times compared to NLCF. This performance gap is expected, as LLM-specific strategies—such as user sequence augmentation and diverse prompt template designs—add considerable computational overhead. During inference, many LLMbased approaches still rely on active LLM computations, further increasing inference costs. While LLMEmb fine-tunes LLMs to generate side information from user-item interactions, it struggles with the inefficiency of lengthy natural language graph descriptions during training. As a result, it only improves inference efficiency compared to earlier methods. Notably, LLMEmb does not model user-item interactions directly; instead, it fine-tunes LLMs based on user-item attributes, which fails to encode multi-order useritem interactions and limits potential performance gains over other LLM-based approaches. In contrast, NLCF achieves remarkable efficiency through two key design choices: (i) during training, it fine-tunes LLMs on concise graph sentences derived from the user-item graph; and (ii) during inference, it constructs collaborative embeddings, enabling efficient item retrieval across the entire item set. These designs significantly reduce both training and inference computational costs, making NLCF more efficient than most LLMbased baselines.

Ablation Study (RQ2) We examine different variants of NLCF through experiments shown in Figure 4 and 6. Since NLCF employs a straightforward architecture without composite components or multiple training objectives, we focus our analysis on two key factors beyond hyper-parameters: the LLM backbone and sampling strategy. Our experiments reveal two significant observations:

First, NLCF’s performance aligns with empirical neural scaling laws. As the LLM parameter size increases, the model’s performance improves substantially. For instance, the Llama 1B model performs well, highlighting the power of LLMs, while the 7B model achieves better results. However, the performance improvement from 7B to 8B models

0.25

0.50

0.75

1.00

Sampling ratio

2

3

4

5

Sentence length

0.245

0.250

0.255

0.260

0.265 precision@5

0.245

0.252

0.248

0.245

0.249

0.263

0.269

0.261

0.262

0.261 0.265 0.267

0.260 0.263

0.262

0.260 walk=2 walk=3 walk=4 walk=5

**Figure 3.** The impact of graph sentence length l and sampling ratio α on Precision@5 on ML-1M dataset.

is relatively modest, suggesting a saturation point in model scaling benefits.

Second, our comparison with alternative sampling strategies demonstrates the superiority of our similarity-based approach across almost all sampling ratios. This advantage likely stems from two factors: random sampling fails to account for subgraph density and struggles to preserve representative samples from each subgraph, while our similaritybased sampling controls the granularity needed for effective graph sentence grouping, particularly at lower sampling ratios where performance gap becomes significant.

Hyper-parameter Sensitivity (RQ3)

We extensively evaluate the effect of hyper-parameters on the performance of NLCF, including sampling ratio α, graph sentence length l, and similarity threshold t. The results, presented in Figure 3, Figure 5, and Table 5, reveal two observations:

First, NLCF achieves optimal performance with a graph sentence length l = 4. This length indicates that third-order collaborative information suffices for high-quality recommendations, while higher-order information may introduce noise without contributing positively to performance. Increasing the sampling ratio improves model performance. Notably, performance declines only slightly when the ratio is lowered from 1 to 0.75, indicating the effectiveness of our sampling method.

Second, the similarity threshold demonstrates a critical role in sampling effectiveness. A moderate threshold value enables NLCF to maintain a more representative subset of samples. High threshold values impose overly strict similarity constraints, effectively reducing the sampling to random selection as most graph sentences are deemed dissimilar. Conversely, low threshold values lack discriminative power, marking most samples as similar and diminishing the sampling strategy’s effectiveness.

35108

<!-- Page 7 -->

## Model

Steam ML-10M ML-1M NDCG@5 NDCG@10 NDCG@5 NDCG@10 NDCG@5 NDCG@10 LightGCN (He et al. 2020) 0.2744 0.2790 0.1988 0.2007 0.2695 0.2436 LightGCL (Cai et al. 2023) 0.2623 0.2807 0.1944 0.2065 0.2112 0.2045 HMLET (Kong et al. 2022) 0.2730 0.2853 0.1919 0.1950 0.2723 0.2503 AFDGCF (Wu et al. 2024b) 0.2809 0.2897 0.2002 0.2004 0.2694 0.2484 TransRec (Lin et al. 2024b) 0.2796 0.2843 0.1961 0.1975 0.2706 0.2435 LLM-CF (Sun et al. 2024) 0.2772 0.2829 0.1976 0.1993 0.2735 0.2478 LETTER (Wang et al. 2024) 0.2717 0.2776 0.1928 0.1883 0.2683 0.2350 LC-Rec (Zheng et al. 2024) 0.2615 0.2682 0.1865 0.1822 0.2626 0.2321 LLMEmb (Liu et al. 2025) 0.2785 0.2858 0.2042 0.2034 0.2711 0.2446 NLCF 0.2864 0.2948 0.2171 0.2147 0.2796 0.2558

**Table 1.** NDCG performance with N = 5 and 10 across Steam, ML-10M, and ML-1M datasets.

## Model

Steam ML-10M ML-1M Train Test Train Test Train Test TransRec 16h5m 3h25m 18h44m 4h18m 4h32m 52m42s LLM-CF 13h24m 0.029s 16h58m 0.101s 3h47m 0.003s LETTER 5h6m 3m31s 7h27m 5m35s 1h43m 1m16s LC-Rec 11h49m 18m59s 13h22m 26m07s 3h18m 7m21s LLMEmb 41m36s 0.029s 48m15s 0.101s 10m23s 0.003s NLCF 42m43s 0.029s 44m19s 0.101s 8m12s 0.003s

**Table 2.** Training and test time comparison among LLMbased models (in seconds [s], minutes [m], and hours [h]).

A/B Test PCTR UCTR GMV ResTime v.s. LightGCN +4.15% +3.11% +5.78% + 1.46% v.s. LLM-CF +2.51% +2.47% +3.14% - 20.17%

**Table 3.** Online A/B tests on the industrial platform.

Online Evaluation (RQ4)

We deploy NLCF on a billion-scale online shopping platform and conduct A/B testing to evaluate its performance. The platform serves hundreds of millions of users and billions of items, supported by two main components: an offline computing center and an online service center. The offline computing center processes user logs and generates a graph corpus from processed user interactions through distributed jobs. It trains NLCF and generates collaborative embeddings for each user and item. Notably, we do not require a tokenizer to handle billions of tokens for mapping. Another offline computing center task is the routine update of collaborative embeddings. This process involves generating a new graph corpus from recent user interactions on a daily basis. Because the final embeddings are constructed via summation, they can be updated incrementally by simply adding the hidden representations derived from this new corpus. The generated collaborative embeddings are then transmitted to the online service center, which uses these pre-computed user embeddings to efficiently retrieve items from a massive item pool, thereby eliminating the need for costly real-time LLM reasoning. NLCF is deployed as a recall model, replacing two baselines: the traditional graph CF model LightGCN and the LLM-based approach LLM-CF.

The performance metrics shown in Table 3 are averaged over eight consecutive weeks, with each model allocated 5% of online traffic. Compared to LightGCN, NLCF achieves significant improvements: +4.15% in PCTR, +3.11% in UCTR, and +5.78% in GMV, demonstrating its superiority in capturing user preferences and driving item consumption. Despite using higher-dimensional embeddings, NLCF incurs only a 1.46% increase in latency, ensuring scalability. Against LLM-CF, NLCF shows moderate gains: +2.51% in PCTR, +2.47% in UCTR, and +3.14% in GMV, confirming the benefits of learning collaborative embeddings over data augmentation. Additionally, NLCF reduces latency by 20.17% compared to LLM-CF, highlighting embedding-only inference efficiency.

## Conclusion

This study introduces a novel paradigm for fine-tuning LLMs for CF task, enabling efficient modeling of multiorder interactions in the user-item graph to learn effective user and item embeddings. Existing methods that prompt LLMs with graph descriptions face two major limitations: (i) Efficiency – slower inference due to token-by-token item generation compared to embedding-based search, and (ii) Topological Modeling – difficulty encoding multi-order interactions and collaborative information from user-item graphs. To address these challenges, we propose NLCF, which treats the user-item graph as a new language. This approach is built on two insights: (1) LLMs excel at learning new languages with suitable corpora, and (2) token transition probabilities in language align with node transition probabilities in graphs. NLCF operates in two stages: (i) transforming the user-item graph into a language corpus that encodes multi-order interactions, and (ii) fine-tuning LLMs on this corpus to capture underlying multi-order collaborative information and construct collaborative user and item embeddings for efficient search. Extensive offline experiments demonstrate NLCF’s superior performance over both LLM-based and traditional graph CF baselines while significantly improve computational efficiency over LLMbased baselines. And online A/B tests conducted on a worldleading shopping platform validate NLCF’s effectiveness in real-world applications.

35109

<!-- Page 8 -->

## Acknowledgements

The work described in this paper was fully supported by a grant from the Innovation and Technology Commission of the Hong Kong Special Administrative Region, China (Project No. GHP/391/22).

## References

Bao, K.; Zhang, J.; Zhang, Y.; Wang, W.; Feng, F.; and He, X. 2023. Tallrec: An effective and efficient tuning framework to align large language model with recommendation. In Proceedings of the 17th ACM Conference on Recommender Systems, 1007–1014. Cai, X.; Huang, C.; Xia, L.; and Ren, X. 2023. LightGCL: Simple Yet Effective Graph Contrastive Learning for Recommendation. In The Eleventh International Conference on Learning Representations. Chen, S.; Zhang, Q.; Dong, J.; Hua, W.; Li, Q.; and Huang, X. 2024. Entity Alignment with Noisy Annotations from Large Language Models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems. Chen, S.; Zhou, C.; Yuan, Z.; Zhang, Q.; Cui, Z.; Chen, H.; Xiao, Y.; Cao, J.; and Huang, X. 2025. You Don’t Need Pre-built Graphs for RAG: Retrieval Augmented Generation with Adaptive Reasoning Structures. In The Fortieth AAAI Conference on Artificial Intelligence. Grover, A.; and Leskovec, J. 2016. node2vec: Scalable feature learning for networks. In Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining, 855–864. Hamilton, W.; Ying, Z.; and Leskovec, J. 2017. Inductive representation learning on large graphs. Advances in neural information processing systems, 30. Harper, F. M.; and Konstan, J. A. 2016. The MovieLens Datasets: History and Context. ACM Trans. Interact. Intell. Syst., 5(4): 19:1–19:19. He, X.; Deng, K.; Wang, X.; Li, Y.; Zhang, Y.; and Wang, M. 2020. Lightgcn: Simplifying and powering graph convolution network for recommendation. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, 639–648. Hong, Z.; Yuan, Z.; Chen, H.; Zhang, Q.; Huang, F.; and Huang, X. 2024. Knowledge-to-SQL: Enhancing SQL Generation with Data Expert LLM. In Findings of the Association for Computational Linguistics: ACL 2024. Hong, Z.; Yuan, Z.; Zhang, Q.; Chen, H.; Dong, J.; Huang, F.; and Huang, X. 2025. Next-generation database interfaces: A survey of llm-based text-to-sql. IEEE Transactions on Knowledge and Data Engineering. Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.; Wang, L.; and Chen, W. 2021. Lora: Low-rank adaptation of large language models. arXiv preprint arXiv:2106.09685. Huang, F.; Yang, Z.; Jiang, J.; Bei, Y.; Zhang, Y.; and Chen, H. 2024. Large Language Model Interaction Simulator for Cold-Start Item Recommendation. arXiv preprint arXiv:2402.09176.

Jiang, Y.; Yang, Y.; Xia, L.; Luo, D.; Lin, K.; and Huang, C. 2024. RecLM: Recommendation Instruction Tuning. arXiv preprint arXiv:2412.19302. Kang, W.; and McAuley, J. J. 2018. Self-Attentive Sequential Recommendation. In IEEE International Conference on Data Mining, ICDM 2018, Singapore, November 17-20, 2018, 197–206. IEEE Computer Society. Kim, S.; Kang, H.; Choi, S.; Kim, D.; Yang, M.; and Park, C. 2024. Large language models meet collaborative filtering: An efficient all-round llm-based recommender system. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 1395–1406. Kong, T.; Kim, T.; Jeon, J.; Choi, J.; Lee, Y.-C.; Park, N.; and Kim, S.-W. 2022. Linear, or non-linear, that is the question! In Proceedings of the fifteenth ACM international conference on web search and data mining, 517–525. Liao, J.; Li, S.; Yang, Z.; Wu, J.; Yuan, Y.; Wang, X.; and He, X. 2024. Llara: Large language-recommendation assistant. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 1785–1795. Lin, J.; Shan, R.; Zhu, C.; Du, K.; Chen, B.; Quan, S.; Tang, R.; Yu, Y.; and Zhang, W. 2024a. Rella: Retrieval-enhanced large language models for lifelong sequential behavior comprehension in recommendation. In Proceedings of the ACM on Web Conference 2024, 3497–3508. Lin, X.; Wang, W.; Li, Y.; Feng, F.; Ng, S.-K.; and Chua, T.-S. 2024b. Bridging items and language: A transition paradigm for large language model-based recommendation. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 1816–1826. Lin, X.; Wang, W.; Li, Y.; Yang, S.; Feng, F.; Wei, Y.; and Chua, T.-S. 2024c. Data-efficient Fine-tuning for LLMbased Recommendation. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 365–374. Lin, Z.; Tian, C.; Hou, Y.; and Zhao, W. X. 2022. Improving graph collaborative filtering with neighborhoodenriched contrastive learning. In Proceedings of the ACM web conference 2022, 2320–2329. Liu, Q.; Wu, X.; Wang, W.; Wang, Y.; Zhu, Y.; Zhao, X.; Tian, F.; and Zheng, Y. 2025. LLMEmb: Large Language Model Can Be a Good Embedding Generator for Sequential Recommendation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 12183–12191. Qu, H.; Fan, W.; Zhao, Z.; and Li, Q. 2024. TokenRec: Learning to Tokenize ID for LLM-based Generative Recommendation. arXiv preprint arXiv:2406.10450. Sun, Z.; Si, Z.; Zang, X.; Zheng, K.; Song, Y.; Zhang, X.; and Xu, J. 2024. Large language models enhanced collaborative filtering. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, 2178–2188. Wang, W.; Bao, H.; Lin, X.; Zhang, J.; Li, Y.; Feng, F.; Ng, S.-K.; and Chua, T.-S. 2024. Learnable item tokenization for generative recommendation. In Proceedings of the 33rd

35110

<!-- Page 9 -->

ACM International Conference on Information and Knowledge Management, 2400–2409. Wang, X.; He, X.; Wang, M.; Feng, F.; and Chua, T.-S. 2019. Neural graph collaborative filtering. In Proceedings of the 42nd international ACM SIGIR conference on Research and development in Information Retrieval, 165–174. Wei, W.; Ren, X.; Tang, J.; Wang, Q.; Su, L.; Cheng, S.; Wang, J.; Yin, D.; and Huang, C. 2024. Llmrec: Large language models with graph augmentation for recommendation. In Proceedings of the 17th ACM International Conference on Web Search and Data Mining, 806–815. Wu, J.; Liu, Q.; Hu, H.; Fan, W.; Liu, S.; Li, Q.; Wu, X.- M.; and Tang, K. 2023. Leveraging Large Language Models (LLMs) to Empower Training-Free Dataset Condensation for Content-Based Recommendation. arXiv preprint arXiv:2310.09874. Wu, L.; Qiu, Z.; Zheng, Z.; Zhu, H.; and Chen, E. 2024a. Exploring large language model for graph data understanding in online job recommendations. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 9178–9186. Wu, W.; Wang, C.; Shen, D.; Qin, C.; Chen, L.; and Xiong, H. 2024b. Afdgcf: Adaptive feature de-correlation graph collaborative filtering for recommendations. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 1242– 1252. Wu, Z.; Pan, S.; Chen, F.; Long, G.; Zhang, C.; and Philip, S. Y. 2020. A comprehensive survey on graph neural networks. IEEE transactions on neural networks and learning systems, 32(1): 4–24. Yang, H.; Wang, X.; Tao, Q.; Hu, S.; Lin, Z.; and Zhang, M. 2024. GL-Fusion: Rethinking the Combination of Graph Neural Network and Large Language model. arXiv preprint arXiv:2412.06849. Yang, Z.; Wu, J.; Luo, Y.; Zhang, J.; Yuan, Y.; Zhang, A.; Wang, X.; and He, X. 2023. Large language model can interpret latent space of sequential recommender. arXiv preprint arXiv:2310.20487. Yuan, Z.; Chen, H.; Hong, Z.; Zhang, Q.; Huang, F.; Li, Q.; and Huang, X. 2025. Knapsack optimization-based schema linking for llm-based Text-to-SQL generation. arXiv preprint arXiv:2502.12911. Yuan, Z.; Yuan, F.; Song, Y.; Li, Y.; Fu, J.; Yang, F.; Pan, Y.; and Ni, Y. 2023. Where to go next for recommender systems? id-vs. modality-based recommender models revisited. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2639–2649. Zhang, A.; Deng, Y.; Lin, Y.; Chen, X.; Wen, J.-R.; and Chua, T.-S. 2024a. Large Language Model Powered Agents for Information Retrieval. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2989–2992. Zhang, Q.; Chen, S.; Bei, Y.; Yuan, Z.; Zhou, H.; Hong, Z.; Chen, H.; Xiao, Y.; Zhou, C.; Dong, J.; et al. 2025. A sur- vey of graph retrieval-augmented generation for customized large language models. arXiv preprint arXiv:2501.13958. Zhang, Y.; Bao, K.; Yan, M.; Wang, W.; Feng, F.; and He, X. 2024b. Text-like Encoding of Collaborative Information in Large Language Models for Recommendation. arXiv preprint arXiv:2406.03210. Zhang, Y.; Feng, F.; Zhang, J.; Bao, K.; Wang, Q.; and He, X. 2023. Collm: Integrating collaborative embeddings into large language models for recommendation. arXiv preprint arXiv:2310.19488. Zhao, W. X.; Zhou, K.; Li, J.; Tang, T.; Wang, X.; Hou, Y.; Min, Y.; Zhang, B.; Zhang, J.; Dong, Z.; et al. 2023. A survey of large language models. arXiv preprint arXiv:2303.18223. Zheng, B.; Hou, Y.; Lu, H.; Chen, Y.; Zhao, W. X.; Chen, M.; and Wen, J.-R. 2024. Adapting large language modA survey of large language modelsels by integrating collaborative semantics for recommendation. In 2024 IEEE 40th International Conference on Data Engineering (ICDE), 1435– 1448. IEEE. Zhou, C.; Du, J.; Zhou, H.; Chen, H.; Huang, F.; and Huang, X. 2025a. Text-Attributed Graph Learning with Coupled Augmentations. In Proceedings of the 31st International Conference on Computational Linguistics, 10865–10876. Zhou, C.; Wang, Z.; Chen, S.; Du, J.; Zheng, Q.; Xu, Z.; and Huang, X. 2025b. Taming language models for textattributed graph learning with decoupled aggregation. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 3463–3474. Zhou, H.; Chen, H.; Dong, J.; Zha, D.; Zhou, C.; and Huang, X. 2023. Adaptive popularity debiasing aggregator for graph collaborative filtering. In Proceedings of the 46th international ACM SIGIR conference on research and development in information retrieval, 7–17. Zhou, H.; Du, J.; Zhou, C.; Yang, C.; Xiao, Y.; Xie, Y.; and Huang, X. 2025c. Each Graph is a New Language: Graph Learning with LLMs. arXiv preprint arXiv:2501.11478. Zhou, H.; Yu, K.; Zhang, Q.; Chen, H.; Zha, D.; Pei, W.; Kong, A.; and Huang, X. 2025d. Self-Monitoring Large Language Models for Click-Through Rate Prediction. ACM Transactions on Information Systems, 44(1): 1–25. Zhou, H.; Zhou, S.; Chen, H.; Liu, N.; Yang, F.; and Huang, X. 2024. Enhancing explainable rating prediction through annotated macro concepts. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 11736–11748. Zhuang, L.; Chen, S.; Xiao, Y.; Zhou, H.; Zhang, Y.; Chen, H.; Zhang, Q.; and Huang, X. 2025. LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora. arXiv preprint arXiv:2510.10114.

35111
