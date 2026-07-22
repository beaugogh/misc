---
title: "Scalable Semi-supervised Community Search via Graph Transformer on Attributed Heterogeneous Information Networks"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38485
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38485/42447
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Scalable Semi-supervised Community Search via Graph Transformer on Attributed Heterogeneous Information Networks

<!-- Page 1 -->

Scalable Semi-supervised Community Search via Graph Transformer on

Attributed Heterogeneous Information Networks

Linlin Ding1, Zhaosong Zhao1, Mo Li1*, Yishan Pan1, Xin Wang2, Renata Borovica-Gajic3

1Liaoning University, Shenyang, China 2Tianjin University, Tianjin, China 3The University of Melbourne, Melbourne, Australia limo@lnu.edu.cn

## Abstract

Attributed heterogeneous information networks (AHINs) encode rich semantics through diverse node and edge types. Recent learning-based community search methods on AHINs have shown promising performance but face two major limitations: i) difficulty scaling to large graphs due to memoryintensive neighbor-based propagation (e.g., GNNs and nodelevel attention), and ii) reliance on explicit communitylevel labels, which are often unavailable or costly to obtain. To address these issues, we propose a scalable Semisupervised Community Search framework on AHINs (SC- SAH), enabling scalability and efficiency, while eliminating the need for community-level labels by leveraging readily available node classification labels. Specifically, we devise MvSF2Token to extract Multi-view Semantic Features (MvSFs) as compact subgraph-level tokens before training, significantly reducing model propagation complexity. We then design a View-Aware Semantic Graph Transformer (VASGhormer) to effectively encode MvSFs by capturing cross-view dependencies and fusing semantic features. The combination of MvSF2Token and VASGhormer ensures scalability, efficiency, and robust performance. Furthermore, we design a View-Aware Contrastive Learner to train VASGhormer without requiring community-level supervision. Extensive experiments on five real-world datasets show that SCSAH outperforms state-of-the-art methods, achieving 18.06% higher performance and 10.43× faster training.

## Introduction

Heterogeneous Information Networks (HINs) offer a powerful framework for modeling complex, multi-typed data and capturing rich semantic relationships across various domains, such as social networks, academic collaborations, and mining sensor networks (Chen et al. 2022; Shi et al. 2017). Attributed HINs (AHINs) further extend this paradigm by integrating node attributes (Li et al. 2022b), thereby better reflecting the characteristics of real-world data. Within an AHIN, shown in Figure 1(a), meta-paths (Figure 1(b)) connect the same type nodes via predefined type sequences. These meta-paths not only express explicit semantics, e.g., the Author-Paper-Author (APA) path for co-

*Corresponding Author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

authorship, but enable the transformation of an AHIN into a homogeneous graph (Figure 1(c)) for downstream analysis.

Author(A)

Paper(P)

Venue(V)

a2 a2 a3 a3 a5 a5 a1 a1 a4 a4 p1 p1 p2 p2 p3 p3 p4 p4 v2 v2 v1 v1 community

(a) An AHIN (c) APA-based author graph a2 a2 a4 a4 a3 a3 a1 a1

(b) Meta-paths

APA:

APVPA:

**Figure 1.** A toy AHIN from the DBLP network. (a) An AHIN composed of three types of nodes with their attributes, and the dashed boxes indicate potential community. (b) Examples of meta-path. (c) A homogeneous graph constructed from the AHIN based on the APA meta-path.

Community search (CS) is a fundamental problem in graph analysis that aims to identify a query-dependent, densely connected subgraph (Gou et al. 2023; Ye, Zhu, and Chen 2023). In recent years, the extension of CS to AHINs has garnered increasing attention (Wang et al. 2024b; Chen et al. 2024), driven by applications such as fraud detection (Zhong et al. 2020) and gene function prediction (Li et al. 2022a). Most existing CS methods on AHINs are algorithmic (Zhou et al. 2023; Liu et al. 2024; Wang et al. 2024b,d), relying on predefined structural constraints, such as the (k, P)-core, where k and P denote the degree and meta-path constraints, respectively. However, these algorithmic approaches typically overlook node attribute information, limiting their flexiblity and expressive power.

Recent studies have begun exploring machine learning (ML)-based approaches to achieve more flexible CS and enhanced feature modeling. A straightforward strategy is to transform an AHIN into a homogeneous graph via metapaths and then apply existing homogeneous graph-based methods for CS. However, this transformation typically results in a loss of critical attribute and structural information inherent in AHINs. To address this limitation, recent approaches propose directly modeling AHINs by leveraging graph neural networks (GNNs) and attention mechanisms. For instance, ST-GNN (Li et al. 2024b) is the

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

14666

![Figure extracted from page 1](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-001-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

first to utilize GNNs with self-supervised training to capture heterogeneous node features. FCS-HGNN (Chen et al. 2024) further integrates GNNs and attention mechanisms for multi-type CS under label supervision. Furthermore, CS- DAHIN (Song et al. 2024) focuses on dynamic AHINs, employing attention-based attribute scoring to assist CS.

Nevertheless, these advanced methods still face two major limitations: i) Limited Scalability on Large-Scale Graphs. All these methods rely on structure-based propagation (e.g., GNNs in ST-GNN and FCS-HGNN, or node-level attention in CS-DAHIN), which aggregate information from neighboring nodes and requires processing a large number of node embeddings. For large graphs, this is inefficient and results in substantial GPU memory overhead during training, as intermediate activations must be stored for backpropagation, fundamentally limiting their scalability. ii) Reliance on Community Labels for Effective Training. For example, CS-DAHIN simply treats nodes with same-classification as positives, which fails to capture community-level information (here, classification refers to the category of specifictype nodes, such as author nodes labeled as data mining, ML, etc.). ST-GNN relies on pseudo-labels for training, which may not accurately reflect actual community patterns, while FCS-HGNN depends on community labels that are often unavailable in practice. Thus, effective training strategies without relying on community labels remain underexplored.

To address these limitations, we propose a novel Semisupervised Community Search framework over AHINs (SC- SAH), which enables scalable and efficient CS on large graphs without relying on community labels. The SCSAH consists of three stages: 1) MvSF2Token, for the preconstruction of Multi-view Semantic Features (MvSFs), 2) offline training of the View-Aware Semantic Graph Transformer (VASGhormer), and 3) online community search.

Specifically, for Limitation i, we propose MvSF2Token, which extracts MvSFs based on meta-paths and graph structures, transforming them into subgraph-level tokens before training. As these tokens are much fewer than node-level tokens, they replace node-level tokens in model propagation, substantially reducing token volume and GPU memory overhead on large graphs during training. To further improve effectiveness and efficiency, we design VASGhormer, which incorporates a Zoom-Aware Transformer to capture crossview dependencies and fuse semantic features. Together, MvSF2Token and VASGhormer enable our framework to achieve scalability, efficiency, and strong performance. To address Limitation ii, we design a View-Aware Contrastive Learner that achieves semi-supervised training by leveraging readily available node-level labels (e.g., the categories of author-type nodes) rather than costly community-level labels. Specifically, the learner combines semantic and unified contrastive losses, guided by a sampling strategy based on node categories, and incorporates node classification as an auxiliary task. Consequently, our approach achieves strong representation learning and model robustness while eliminating the need for community-level labels. Our main contributions are summarized as follows:

• We propose MvSF2Token to encode multi-view seman- tic features into subgraph-level tokens for downstream model use, effectively mitigating scalability issues. • We design VASGhormer to model cross-view and semantic dependencies among the input tokens, enabling scalable and efficient training on large graphs. • We introduce a View-Aware Contrastive Learner that enables semi-supervised training with the aid of node-level labels instead of community-level supervision. • Experiments on five public datasets demonstrate that SCSAH outperforms state-of-the-art methods, achieving 18.06% higher performance and 10.43× faster training.

## Related Work

Algorithmic Community Search on (A)HINs. Early CS studies on HINs focus on structure, often ignoring node attributes (Wang et al. 2020; Fang et al. 2020; Jiang et al. 2022a; Yang et al. 2022; Li et al. 2024a). For instance, the (k, P)-core model captures cohesiveness via meta-paths, facilitating cohesive community discovery (Wang et al. 2020). Keyword-centric methods further incorporate textual information into the search process (Qiao et al. 2021). Zhou et al. (Zhou et al. 2023) consider influence and multitype nodes, introducing Pareto-optimality to improve search quality. With the rise of AHINs, recent methods develop attribute-aware techniques that integrate structural and attribute cohesiveness for more effective search (Wang et al. 2024b,d). However, these methods still struggle to effectively model complex heterogeneous features. ML-based Community Search. Recent years have seen an increasing adoption of ML methods for CS, owning to the powerful feature capture capabilities of neural networks. For homogeneous graphs, ICS-GNN (Gao et al. 2021) firstly formulates CS as a learning task using GNN, while COCLEP (Li et al. 2023) pioneers the integration of contrastive learning. Subsequent studies focus on scalable and feature-aware training (Wang et al. 2024c), as well as addressing label sparsity (Wang et al. 2024a). SLRL (Ni et al. 2025) further employs reinforcement learning to guide community generation. In contrast, there is limited research on heterogeneous graphs. ST-GNN (Li et al. 2024b) is the first to apply GNNs with self-supervised training. FCS- HGNN (Chen et al. 2024) combines GNNs and attention to perform multi-type CS, while CS-DAHIN (Song et al. 2024) utilizes multi-level attention for attribute scoring over dynamic AHINs. However, these models are difficult to scale to large graphs, due to the high computational costs of graph-based propagation, and perform poorly when community labels are missing. Furthermore, due to inherent structural differences, models designed for homogeneous graphs cannot be directly applied to HINs, underscoring the need for further research on CS in heterogeneous settings.

Problem Definition Definition 1 (Attributed Heterogeneous Information Network, AHIN). An AHIN is a graph defined as G = (V, E, X, φ, ψ), where each node v ∈V and each edge e ∈E are associated with their specific type mapping functions φ(v): V →A and ψ(e): E →R. Here, A and R

14667

<!-- Page 3 -->

Community Score

Computation

Trained VASGhormer

Auxiliary features (performed once and reused)

Search preparation

Community search

...

Multi-Constrained

Community Search

(Algorithm 1)

query query

Stage1: MvSF2Token

APA

APVPA

Hyperedges

Hyperedges

MvSF tokens

MvSF tokens

...

A

P

V q

...

SVD

SVD

Low coh()

Low sim()

JS(q)

q

JS(q)

MvSFs of v1 MvSFs of vN...

Embedding

All Training Tokens

Embedding

Multi-view

Detach

...

Meta-path View

Representations

Meta-path View

Representations

Multi-view

Detach

Shared Weights

Unified view Representations

Lcls

Classification

Prediction

Lsem

Luni

VASGhormer: View-Aware Semantic Graph Transformer Semantic Feature

Construction

Multi-view Feature

Construction

Stage3: Online Search Stage2: Offline Training of VASGhormer

(example of one node)

Auxiliary Node

Classification

View-Aware Contrastive Learner

Attention- based Semantic Aggregation

Low sim()

L layers

ZMSA

Zoom Encoding

A&N

FFN

A&N

Zoom-Aware

Transformer

ZMSA

Zoom Encoding

A&N

FFN

A&N

Zoom-Aware

Transformer

ZMSA

Zoom Encoding

A&N

FFN

A&N

Zoom-Aware

Transformer

ZMSA

Zoom Encoding

A&N

FFN

A&N

Zoom-Aware

Transformer

×

×

×

1P v,loc h

1P v,glo h nP v,glo h nP v,loc h glo v h loc v h

H com for propagation for training

ˆ cls Y

**Figure 2.** The overall framework of SCSAH. 1) MvSF2Token: extracts multi-view semantic features (MvSFs) from the AHIN, constructing compact subgraph-level tokens before training; 2) Offline Training of VASGhormer: the VASGhormer efficiently learns representations with a semi-supervised contrastive strategy; 3) Online Search: generates auxiliary features via the trained VASGhormer and performs Multi-Constrained Community Search.

refer to the sets of node and edge types, where |A|+|R| > 2. When |A| = |R| = 1, the graph degenerates into a homogeneous graph. X(Ai) ⊆X is the attribute set of Ai type nodes. x(Ai)

j ∈Rdi is the attribute of v(Ai)

j ∈V (Ai), where di is the dimension of the attributes of Ai type nodes. Definition 2 (Meta-Path). A meta-path P is defined as a path in the form of A1

R1 −−→A2

R2 −−→...

Rl −−→Al+1 which describes a composite relation between types A1 and Al+1. Problem statement (Community Search on AHINs). Given an AHIN G, a target type At, a At type query node vq, and a meta-path set PS = {P1,..., PM}, the task of Community Search on AHINs aims to identify a set of nodes Cq of the target type At, where the nodes in Cq are densely intraconnected via meta-paths PS and exhibit similar attributes.

## Methodology

This section details the SCSAH framework, as shown in Figure 2. It comprises three stages: 1) MvSF2Token; 2) Offline Training of VASGhormer and 3) Online Search.

MvSF2Token: Feature Pre-construction In CS tasks, efficiently extracting structural features is critical for overcoming the scalability limitations of GNNs and neighbor-dependent Transformers. While prior work (Chen et al. 2023) achieves this by pre-computing multi-hop neighbor representations for homogeneous graphs, structural features in AHINs are inherently more complex due to the presence of multi-type nodes and meta-paths. Consequently, existing pre-computation strategies are insufficient for AHINs. To address this, we propose MvSF2Token, a non-ML method for transforming Multi-view Semantic Features (MvSFs) from AHIN’s structure into subgraph-level tokens before training, significantly reduces memory overhead of subsequent training while preserving rich structural features. It comprises two main stages: Semantic Feature Construction and Multi-view Feature Construction.

Semantic Feature Construction. A common way to unify feature dimensions across node types for semantic feature aggregation is padding, which, however, may dilute the contribution of target-type features. To mitigate this, we introduce a semantic feature extraction method based on Singular Value Decomposition (SVD).

Specifically, we first apply SVD to reduce the feature dimension of non-target-type nodes to a predefined dimension doth, which is smaller than that of target-type nodes. This ensures that, after concatenating features, target-node features retain their dominant influence. Given a meta-path P, we then construct new semantic features for each target node. For a target node v, its semantic feature is computed as xP v = [xv ∥ 1 |N G

P (v)|

P u∈N G

P (v) ˜xu] ∈Rd0, where xv is the original feature, ˜xu denotes the SVD-reduced feature of a non-target node u, d0 is the new concatenated dimension, and N G

P (v) denotes the non-target-type neighbors of v along P. For example, under the meta-path APVPA, N G

P (v) includes P-type nodes connected to v, and V-type nodes connected to those P-type nodes. After processing all target-type nodes, we obtain the semantic features XP ∈RN×d0, where N is the number of target-type nodes. Finally, by repeating the above process for different meta-paths, we construct a set of semantic feature matrices {XP1,..., XPM } and their corresponding meta-path-based homogeneous graphs {GP1,..., GPM } for subsequent stages.

Multi-view Feature Construction. Extracting meaningful community features is critical for CS tasks. Although simple aggregation of multi-hop neighbors (Chen et al. 2023; Wang et al. 2024a; Ding et al. 2025) enables efficient structural feature extraction, it may also incorporate

14668

![Figure extracted from page 3](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-scalable-semi-supervised-community-search-via-graph-transformer-on-attributed-he/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

weakly connected nodes, thereby undermining key community properties such as cohesion and feature similarity.

To address this, we propose a novel Multi-view Feature Construction method that selects nodes for each hop view based on a joint score, which enforces both structural and feature cohesion within the selected set for aggregation.

Specifically, given a meta-path P, target node v, and hop limit K, for each hop k ∈{1,..., K}, we first construct a k-hop neighbor subgraph N P k (v) from GP. For each node u ∈N P k (v), we compute a joint score based on the khop subgraph: JSk(u) = ws(u) sim(v, u) + wc(u) coh(u), where sim(v, u) is the cosine similarity between node features, and coh(u) is the Local Clustering Coefficient (Watts and Strogatz 1998) of u, measuring the structural cohesion. The weights ws(u) and wc(u) are defined as:

ws(u) = ecoh(v,u)

esim(v,u) + ecoh(u), wc(u) = 1 −ws(u). (1)

This equation adaptively balances structural cohesion and feature similarity, ensuring a high JSk(u) only when both are strong (see Appendix for proof). Nodes with JSk(u) ≥ θ, where θ is cohesion threshold, are retained to form the k-hop view subgraph. Repeating this process up to K hops, yields K subgraphs form distinct views. Next, we encode v and its multi-view subgraph as hyperedges, forming a hypergraph HP v ∈RN×(K+1), where each column represents one view. Finally, based on the semantic feature matrix XP, we compute the multi-view semantic features (MvSFs) for node v as XP v ←(HP v)⊤XP ∈R(K+1)×d0. Notably, MvSFs for all training nodes are constructed in a one-time offline step before training, and the associated cost is negligible compared with multi-epoch training.

Design of VASGhormer

To effectively model interactions among MvSFs, a straightforward approach is to apply a standard Transformer architecture. However, conventional Transformers treat all input tokens equally and fail to capture cross-view relationships and fuse information from meta-paths, limiting their effectiveness for community-oriented tasks on AHINs. To address this, we propose the View-Aware Semantic Graph Transformer (VASGhormer), a tailored model designed to work collaboratively with MvSFs. VASGhormer enables scalable and efficient training while capturing cross-view community dependencies, making it particularly suitable for CS on AHINs. The model design is detailed as follows:

Token Embedding. Under each meta-path P, we first project the feature tokens XP v into a dense representation using a linear transformation, i.e., H(0)

P,v = XP v We, where We ∈Rd0×d is a learnable weight matrix.

Zoom-Aware Transformer. Transformer-based methods for graphs (Ying et al. 2021; Ramp´asek et al. 2022; Bar- Shalom, Bevilacqua, and Maron 2024) aim to capture latent relationships among tokens using structural priors like shortest path or edge weights. However, existing variants focus solely on node-level input tokens and fail to explicitly model interactions between tokens from different hops. Such interactions are crucial for integrating local and global information, which is essential to generate coherent representations of multi-view community features.

To model these cross-hop relations, we design the Zoom- Aware Transformer, which enhances Multi-Head Self- Attention via a Zoom-aware Multi-head Self-Attention (ZMSA). ZMSA captures progressive correlations among tokens across hop-level views by introducing a zoom-aware bias. Given two tokens hv,i and hv,j from the i-hop and jhop views respectively, we define a zoom feature ϕ(i, j) = j −i. A learnable scalar bias bϕ(i,j) is associated with each zoom level, indicating a zoom-out when ϕ(i, j) > 0 and a zoom-in when ϕ(i, j) < 0. The (i, j)-element of the Query- Key product matrix in ZMSA is computed as:

Azoom(i, j) =

(h(l)

v,iWq)(h(l)

v,jWk)⊤ √ d(l+1) + bϕ(i,j), (2)

where Wq, Wk ∈Rd(l)×d(l+1) are projection matrices, and the zoom-aware bias bϕ(i,j) is shared across all layers.

For the propagation process, we feed H(0)

P,v into L stacked Zoom-Aware Transformers, each consisting of a ZMSA model and a feed-forward network (FFN), with layer normalization and residual connections:

H′(l)

P,v = ZMSA(LN(H(l−1)

P,v)) + H(l−1)

P,v,

H(l)

P,v = FFN(LN(H′(l)

P,v)) + H′(l)

P,v.

(3)

After L layers of propagation, we obtain the latent multiview representation HP v = {hP v,0,..., hP v,K} ∈R(K+1)×d.

Dual-View Detach. Next, we construct more informative local (node-level) and global (community-level) representations. The local representation aggregates multi-view tokens based on their relevance to the query node, while the global representation captures structural context reflective of community patterns. The attention weights are computed as:

αloc i = exp(hP v,0 · hP v,i) PK j=0 exp(hP v,0 · hP v,j)

, (4)

αglo i = exp hP v,0 ∥hP v,i

Wd

PK j=1 exp hP v,0 ∥hP v,j

Wd

, (5)

where ∥denotes concatenation, Wd ∈R2d×1 is a learnable weight. The local and global representations are obtained as: hP v,loc = PK i=0 αloc i · hP v,i, hP v,glo = PK i=1 αglo i · hP v,i.

Attention-based Semantic Aggregation. To effectively integrate semantic features from different meta-paths, we first compute the importance of each meta-path using a shared attention network over the local and global features:

βPi = exp(q⊤ s · tanh(Ws(hPi v,loc ∥hPi v,glo) + bs)) Pn j=1 exp(q⊤ s · tanh(Ws(hPj v,loc ∥hPj v,glo) + bs))

,

(6) where Ws, bs, and qs are shared parameters across different meta-paths. At last, the final unified local and global representations are then computed as weighted sums, i.e., hloc v = Pn i=1 βPi hPi v,loc and hglo v = Pn i=1 βPi hPi v,glo.

14669

<!-- Page 5 -->

Offline Training of VASGhormer We design a semi-supervised strategy, which employs a View-Aware Contrastive Learner and uses node classification as an auxiliary task to enable effective offline training.

View-Aware Contrastive Learner. In real communities, nodes exhibit both structural cohesion and feature similarity. To leverage this property and enable training without community labels, we introduce the View-Aware Contrastive Learner. It integrates a semantic contrastive loss from the meta-path view and a unified contrastive loss from the unified view, using both classification labels and graph structure for sampling. In this way, the learned representations are more closely align with true community patterns.

Specifically, inspired by the margin-based triplet loss (Schroff, Kalenichenko, and Philbin 2015), we define the semantic contrastive loss over meta-path-level representations to achieve discriminative learning from the meta-path view:

Lsem = 1

M

X v∈V t

X

P∈Ps max

0, sim hP v,glo, h

P v,neg

−sim hP v,glo, h

P v,pos

−sim hP v,loc, hP v,glo

+ ϵ

,

(7)

where V t is the set of training nodes, M is the number of meta-paths, sim(·, ·) denotes cosine similarity, h

P v,pos =

1 |PP v |

P u∈PP v hP u,glo and h

P v,neg = 1 |NP v |

P u′∈NP v hP u′,glo is the averaged positive and negative prototype, ϵ is a margin, PP v contains meta-path-based neighbors with the same category label, and NP v comprises nodes at least K-hops away or with different labels, ensuring that sampling respects both structural and attribute-level community patterns. This objective encourages tighter global (community-level) representations for nodes within the same community, separates nodes from different communities, and enforces consistency between the local and global representations of each node.

Additionally, to align with our learning goal under the unified view (after semantic aggregation), we adopt a similar principle and define the unified contrastive loss as:

Luni =

X v∈V t max

0, sim hglo v, hv,neg

− sim hglo v, hv,pos

−sim hloc v, hglo v

+ ϵ

.

(8)

To construct positive and negative samples for Luni, we use a multi-semantic adjacency matrix Amulti, where Amulti(u, v) = 1 if there exists any P ∈Ps such that AP u,v = 1, and 0 otherwise. Then, Pv contains nodes connected to v in Amulti and sharing the same category label, while Nv includes nodes that are either unconnected within K-hops or have different labels. Finally, the objective of the View-Aware Contrastive Learner is defined as LV AC = λ1Lsem + Luni, where λ1 is a hyperparameter.

Auxiliary Node Classification. Communities typically consist of densely connected nodes that share the same category, making node classification a valuable prior task for

## Algorithm

1: Multi-Constrained Community Search Input: Query node q, adjacency matrix Amulti, community score Sq, score threshold τ, predicted classification ˆY cls Output: Target community Cq

1: Cq ←{q} 2: Vcand ←{v ∈V tar | Sq,v ≥τ} 3: if ˆycls q is confident then 4: Vcand ←{v ∈Vcand | argmax ˆycls v = argmax ˆycls q } 5: end if 6: Cq ←largest component in Vcand containing q 7: return Cq community search. Leveraging this idea, we incorporate a node classification task to enhance the learning of node-level representations hloc v. Specifically, we apply a linear projection followed by a sigmoid activation: ˆycls v = σ(Wc ·hloc v + bc), where Wc ∈Rdc×d and bc ∈Rdc are trainable parameters. The cross-entropy loss is then adopted as the training loss: Lcls = − 1 |V t|

P v∈V t

Pdc j=1 ycls v,j log(ˆycls v,j), where ˆycls v is the predicted probability and ycls v is the category label. Finally, we integrate the two loss functions with a hyperparameter λ2, and define the overall training objective as Lall = LV AC + λ2Lcls. The overall training complexity is O

|V t| · M · L · ((K + 1)2d + (K + 1)d2)

; additional analysis is provided in the Appendix.

Online Search Strategy

During online search, ML-based methods (Li et al. 2024b; Chen et al. 2024) often incur high query costs by relying on model inference to obtain probabilities or scores. To improve efficiency, we precompute and store auxiliary features using the trained VASGhormer, thereby eliminating the need for model propagation during the query phase. Then, we design a Multi-Constrained Community Search approach that incorporates both structural and feature information, and aligns with our auxiliary node classification task.

Specifically, for auxiliary features generation, we employ the trained VASGhormer to obtain community-level representations and classification results for target-type nodes, denoted as Hcom = {hcom

1,..., hcom

Nt } and ˆY cls = {ˆycls

1,..., ˆycls Nt }. Note that Hcom and ˆY cls can be reused throughout the online query phase without recomputation.

According to our training objective, nodes with closer community representations are more likely to be tightly connected, share similar features, and belong to the same community. Thus, for a given query node q, we compute similarity scores to estimate the likelihood that node i is in the same community as q, i.e., Sq,i = sim(hcom q, hcom i). We then perform Multi-Constrained Community Search as outlined in Algorithm 1. It first initializes the target community and selects candidate nodes using a score threshold τ (Lines 1-2), where τ can be adjusted based on evaluation results. Next, nodes are conditionally selected if their predicted category are reliable; specifically, a prediction is considered reliable if the gap between the top-1 and top-2

14670

<!-- Page 6 -->

## Method

IMDB DBLP ACM OAG MAG F1 JAC NMI F1 JAC NMI F1 JAC NMI F1 JAC NMI F1 JAC NMI

ICS-GNN 51.73 42.03 43.47 55.17 43.40 45.06 50.42 41.88 42.12 - - - - - - QD-GNN 53.42 40.92 41.12 58.53 45.82 42.21 53.05 41.03 39.47 - - - - - - COCLEP 57.15 45.19 46.09 61.08 48.05 45.31 58.93 45.19 45.81 35.08 22.02 21.33 - - - TransZero 61.88 48.55 45.76 65.91 50.39 47.73 61.17 49.55 47.22 41.95 24.36 26.89 32.59 24.77 23.83 CS-DAHIN 65.73 50.75 49.58 72.10 55.89 56.03 63.52 53.69 50.46 - - - - - - ST-GNN 66.05 53.67 52.50 77.64 63.03 64.19 70.60 58.76 56.66 45.41 27.79 25.05 - - - FCS-HGNN 65.61 55.24 50.83 79.25 67.97 62.55 68.28 59.34 55.00 44.72 29.15 30.48 - - - SCSAH 75.34 62.80 60.29 87.76 73.12 71.44 80.71 72.09 66.50 50.42 35.92 34.26 42.45 32.98 32.53 Improve (%) 14.62 13.69 14.84 10.74 7.58 11.29 14.32 21.49 17.37 11.03 23.22 12.40 30.25 33.14 36.51

**Table 1.** Performance comparison with seven baseline methods based on F1, JAC, and NMI (%) across five datasets. Bold numbers indicate the best results, underlined numbers denote the second-best, and “-” indicates out-of-memory.

Dataset Nodes Edges Meta-path

IMDB

∗Movie (M): 4,780 M-A: 14,340

M-D: 4,780

MAM MDM Actor (A): 5,841 Director (D): 2,269

DBLP

∗Author (A): 4,057 A-P: 19,645 P-C: 14,328 P-T: 88,420

APA APCPA APTPA

Paper (P): 14,328 Conference (C): 20

Term (T): 8,789

ACM

∗Paper (P): 12,499 P-A: 37,055

P-S: 12,499

PAP PSP Author (A): 17,431

Subject (S): 73

OAG

∗Paper (P): 119,483 P-A: 340,959

PAP PAIAP Author (A): 510,189 A-A: 329,703 Venue (V): 6,934 P-V: 119,483 Institution (I): 9,079 A-I: 612,872

MAG

∗Paper (P): 736,389 P-A: 7,145,660 PAP PFP PAIAP

Author (A): 1,134,649 P-P: 5,416,271 Field (F): 59,965 P-F: 7,505,078 Institution (I): 8,740 A-I: 1,043,998

**Table 2.** Statistics of five real-word datasets.

predicted probabilities exceeds the confidence threshold τc. This ensures that only high-confident predictions influence community search (Lines 3–4). Finally, given Amulti and Vcand, the algorithm returns the largest connected component containing the query node q as the final result (Line 5), ensuring feature coherence and structural connectivity.

## Experiments

## Experimental Setup

Datasets. Table 2 summarizes the statistics of five realworld AHINs: IMDB (Wang et al. 2019), DBLP (Wang et al. 2019), ACM (Luo et al. 2021), OAG (OAG-L1-Field) (Li et al. 2024b) and MAG (OGB-MAG) (Chen et al. 2024; Li et al. 2024b). Community generation is inspired by previous research (Chen et al. 2024). More details of the datasets are provided in the Appendix. Comparing methods. We compare our approach with existing ML-based CS methods on AHINs, including CS- DAHIN (Song et al. 2024), ST-GNN (Li et al. 2024b), and FCS-HGNN (Chen et al. 2024). Due to the limited availability of methods tailored for AHINs, we additionally include

F1 JAC NMI 0.4 0.5 0.6 0.7 0.8

(a) Results on IMDB

-MvSF -Zoom -Class -SCL -UCL Full

F1 JAC NMI 0.5 0.6 0.7 0.8 0.9

(b) Results on DBLP

F1 JAC NMI 0.5 0.6 0.7 0.8 0.9

(c) Results on ACM

**Figure 3.** Ablation results of five variants on three datasets.

several methods designed for homogeneous graphs: ICS- GNN (Gao et al. 2021), QD-GNN (Jiang et al. 2022b), CO- CLEP (Li et al. 2023), and TransZero (Wang et al. 2024a). Details on how each model is adapted to our datasets and community search task are provided in the Appendix. Evaluation Metrics. We evaluate performance using three standard metrics based on community labels: F1-score, Jaccard Similarity (JAC), and Normalized Mutual Information (NMI) (Wang et al. 2024a; Chen et al. 2024). Appendix for more detailed environment and parameter settings. Code is available at github.com/XHBACR/SCSAH.

Effectiveness Evaluation Table 1 shows that SCSAH consistently outperforms all baselines, with average improvements of 16.19% in F1, 19.82% in JAC, and 18.18% in NMI. Graph-dependent models often struggle with scalability and memory usage on large-scale graphs. Among heterogeneous graph baselines, only SCSAH is able to process the MAG dataset without memory issues. Methods designed for homogeneous graphs generally perform poorly due to forced type conversion, which limits their ability to capture essential heterogeneous features. Among AHIN-based methods, CS-DAHIN, originally developed for dynamic graphs, performs inadequately when its dynamic module is removed for static community search. Although ST-GNN and FCS-HGNN show relatively strong baseline performance, they still fall short of SCSAH in both scalability and effectiveness. The full results with mean ± standard deviation are provided in the Appendix.

Ablation Study To evaluate the contribution of each component in SCSAH, we design the following variants: 1) -MvSF, where the

14671

<!-- Page 7 -->

0.5 0.6 0.7 0.8

0.6 0.7 0.8 0.9

2 4 6 8 10 0.6 0.7 0.8 0.9

2 4 6 8 10 0.3

0.4

0.5

1 2 3 4 5 0.5 0.6 0.7 0.8

1 2 3 4 5 0.6 0.7 0.8 0.9

0.5 0.6 0.7 0.8

0.6 0.7 0.8 0.9

0.5 0.6 0.7 0.8

0.6 0.7 0.8 0.9

0.6 0.7 0.8 0.9

0.5 0.6 0.7 0.8

F1 JAC NMI

(a) on IMDB (b) on DBLP (c) K on DBLP (d) K on OAG

(e) L on IMDB (f) L on DBLP (g) 1 on IMDB (h) 1 on DBLP

(i) 2 on IMDB (j) 2 on DBLP (k) c on IMDB (l) c on DBLP

0.5 0.1 0.3 0.5 0.1 0.3

0.9 0.1 0.5 0.9 0.1 0.5

1.2 0.4 0.8 1.2 0.4 0.8 0.5 0.1 0.3 0.5 0.1 0.3

**Figure 4.** Hyperparameter sensitivity results, with varying cohesion threshold θ (a-b) and hop limitation K (c-d) in MvSF2Token; Transformer layers L (e-f); semantic contrastive loss weight λ1 (g-h); classification loss weight λ2 (i-j); and confidence threshold τc (k-l) in search Algorithm.

MvSF2Token module is removed and the original attributes of target-type nodes are used, with structural features captured by Hop2Token method (Chen et al. 2023); 2) -Zoom, which replaces the Zoom-Aware Transformer with a standard Transformer; 3) -Class, which omits the node classification task from both training and search phases; 4) - SCL, which eliminates the semantic contrastive loss; and 5) -UCL, which removes the unified contrastive loss. As shown in Figure 3, all components have a positive impact on overall performance. Removing the MvSF2Token module results in significant drop, highlighting the critical role of multi-view semantic features in modeling graph structure. The Zoom- Aware Transformer consistently outperforms the standard version, demonstrating its effectiveness in capturing crossview dependencies. Notably, the unified contrastive loss is especially important—its removal leads to an average performance drop of 15.2%—underscoring the central role of unified features in learning effective representations.

Hyperparameter Analysis We analyze the sensitivity of six key hyperparameters in our model.As shown in Figure 4, the cohesion threshold θ is varied from 0.1 to 0.5, with the best performance at θ = 0.2; higher values filter out too many relevant nodes, thereby hindering multi-view feature construction. The hop limitation K is tested over {2, 4, 6, 8, 10}, with K = 4 performing best on DBLP and K = 6 on OAG, indicating that excessively large hop ranges may introduce noise from unrelated nodes. We vary the Transformer layers L from 1 to 5, and observe peak performance at 1 or 2, suggesting that a shallow architecture suffices for capture multi-view interactions. For the semantic contrastive loss weight λ1, we test values from 0.1 to 1.1, and find λ1 = 0.7 achieves the best results, highlighting the greater importance of unified view learning than meta-path view. The classification loss weight λ2 is also

IMDB DBLP ACM OAG MAG 100 101 102 103 104

ICS-GNN QD-GNN COCLEP TransZero CS-DAHIN ST-GNN FCS-HGNN SCSAH

Training Time (s) Search Time (s)

(a) Effciency results of training phase

(b) Effciency results of search phase o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m o.o.m

IMDB DBLP ACM OAG MAG 10-3 10-2 10-1 100 101

**Figure 5.** Efficiency evaluation results of training and search phases, where o.o.m denotes out-of-memory.

varied from 0.1 to 1.1; performance remains stable between 0.6 and 1.0, while values outside this range cause imbalance between objectives. Finally, the confidence threshold τc is tuned from 0.1 to 0.6, with optimal results when τc falls between 0.3 and 0.4, effectively filtering out uncertain predictions while preserving reliable classification signals for community search. Overall, most hyperparameters remain stable within a certain range, indicating the robustness of our method across different scenarios without extensive tuning. A more detailed analysis is provided in the Appendix.

Efficiency Evaluation In Figure 5, we report the efficiency results for both training and search phases, evaluated on the same datasets and baseline methods as in the effectiveness evaluation. Note that the training phase begins only after extracting MvSFs for all training nodes, while the querying phase starts after generating the auxiliary features for the full graph. Among all methods, only TransZero and our SCSAH are able train on the large-scale MAG dataset without out-of-memory issues, as both approaches convert structural information into compact tokens, substantially reducing GPU memory overhead during training. Since TransZero is originally designed for homogeneous graphs and does not perform per-meta-path propagation or semantic aggregation, our SCSAH exhibits slightly slower. On datasets where AHIN-specific methods can be executed, SCSAH achieves an average speedup of 10.43× over CS-DAHI, ST-GNN and FCS-HGNN in the training phase, and 4.27× in the search phase.

## Conclusion

In this paper, we present SCSAH, a novel framework for community search on AHINs that scales to large graphs and supports scenarios without community labels. SCSAH consists of three stages: 1) MvSF2Token, which extracts compact multi-view semantic features as subgraph-level tokens; 2) offline training of VASGhormer, training a view-aware semantic graph transformer that captures semantic dependencies without requiring community labels; and 3) online community search via a Multi-Constrained Community Search algorithm. Extensive experiments on five real-world datasets show that SCSAH consistently outperforms existing stateof-the-art methods in performance and efficiency.

14672

<!-- Page 8 -->

## Acknowledgements

This study was funded by the National Natural Science Foundation of China (Nos.52574191, 62072220, 62472311); the youth talent support program of ‘Xing Liao Talent Program’ (No.XLYC2203003); the Basic Scientific Research Project of the Department of Education of Liaoning Province (No.LJ232510140001); Natural Science Foundation of Liaoning Province (No.2022-KF-13-06, 2025- MSLH-300); Liaoning Provincial Department of Education Youth Project (No.JYTQN2023189); Natural Science Foundation of Liaoning University (No.LDZDJC2402); Australian Research Council Discovery Early Career Researcher Award (No.DE230100366).

## References

Bar-Shalom, G.; Bevilacqua, B.; and Maron, H. 2024. Subgraphormer: Unifying Subgraph GNNs and Graph Transformers via Graph Products. In Proceedings of the 41st International Conference on Machine Learning. Chen, D.; Wang, M.; Chen, H.; Wu, L.; Qin, J.; and Peng, W. 2022. Cross-Modal Retrieval with Heterogeneous Graph Embedding. In Proceedings of the 30th ACM International Conference on Multimedia, 3291–3300. Chen, G.; Guo, F.; Wang, Y.; Liu, Y.; Yu, P.; Shen, H.; and Cheng, X. 2024. FCS-HGNN: Flexible Multi-type Community Search in Heterogeneous Information Networks. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, 207–217. ACM. Chen, J.; Gao, K.; Li, G.; and He, K. 2023. NAGphormer: A Tokenized Graph Transformer for Node Classification in Large Graphs. In Proceedings of the 11th International Conference on Learning Representations. Ding, L.; Han, Y.; Li, M.; Cui, N.; Wang, X.; and Borovica- Gajic, R. 2025. Adaptive anchor-based attention networks for large-scale sparse bipartite graph embedding. Knowl. Based Syst., 329: 114242. Fang, Y.; Yang, Y.; Zhang, W.; Lin, X.; and Cao, X. 2020. Effective and Efficient Community Search over Large Heterogeneous Information Networks. In Proceedings of the VLDB Endowment, volume 13, 854–867. Gao, J.; Chen, J.; Li, Z.; and Zhang, J. 2021. ICS-GNN: Lightweight Interactive Community Search via Graph Neural Network. In Proceedings of the VLDB Endowment, volume 14, 1006–1018. Gou, X.; Xu, X.; Wu, X.; Chen, R.; Wang, Y.; Wu, T.; and Ke, X. 2023. Effective and Efficient Community Search with Graph Embeddings. In Proceedings of the 26th European Conference on Artificial Intelligence, volume 372, 891–898. Jiang, Y.; Fang, Y.; Ma, C.; Cao, X.; and Li, C. 2022a. Effective Community Search over Large Star-Schema Heterogeneous Information Networks. In Proceedings of the VLDB Endowment, volume 15, 2307–2320. Jiang, Y.; Rong, Y.; Cheng, H.; Huang, X.; Zhao, K.; and Huang, J. 2022b. Query Driven-Graph Neural Networks for Community Search: From Non-Attributed, Attributed, to Interactive Attributed. In Proceedings of the VLDB Endowment, volume 15, 1243–1255.

Li, L.; Luo, S.; Zhao, Y.; Shan, C.; Wang, Z.; and Qin, L. 2023. COCLEP: Contrastive Learning-based Semi- Supervised Community Search. In Proceedings of the 39th IEEE International Conference on Data Engineering, 2483– 2495. Li, M.; Borovica-Gajic, R.; Choudhury, F. M.; Cui, N.; and Ding, L. 2024a. Maximal size constraint community search over bipartite graphs. Knowl. Based Syst., 297: 111961. Li, M.; Cai, X.; Li, L.; Xu, S.; and Ji, H. 2022a. Heterogeneous Graph Attention Network for Drug-Target Interaction Prediction. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management, 1166–1176. Li, X.; Wu, Y.; Ester, M.; Kao, B.; Wang, X.; and Zheng, Y. 2022b. SCHAIN-IRAM: An Efficient and Effective Semi- Supervised Clustering Algorithm for Attributed Heterogeneous Information Networks. IEEE Transactions on Knowledge and Data Engineering, 34(4): 1980–1992. Li, Y.; Chen, X.; Zhao, Y.; Shan, W.; Wang, Z.; Yang, G.; and Wang, G. 2024b. Self-Training GNN-based Community Search in Large Attributed Heterogeneous Information Networks. In Proceedings of the 40th IEEE International Conference on Data Engineering, 2765–2778. Liu, Y.; Guo, F.; Xu, B.; Bao, P.; Shen, H.; and Cheng, X. 2024. SACH: Significant-Attributed Community Search in Heterogeneous Information Networks. In Proceedings of the 40th IEEE International Conference on Data Engineering, 3283–3296. Luo, L.; Fang, Y.; Cao, X.; Zhang, X.; and Zhang, W. 2021. Detecting Communities from Heterogeneous Graphs: A Context Path-based Graph Neural Network Model. In Proceedings of the 30th ACM International Conference on Information and Knowledge Management, 1170–1180. Ni, L.; Ye, R.; Luo, W.; Zhang, Y.; Zhang, L.; and Sheng, V. S. 2025. SLRL: Semi-Supervised Local Community Detection Based on Reinforcement Learning. In Proceedings of the AAAI Conference on Artificial Intelligence, 631–639. Qiao, L.; Zhang, Z.; Yuan, Y.; Chen, C.; and Wang, G. 2021. Keyword-Centric Community Search over Large Heterogeneous Information Networks. In Proceedings of the 26th International Conference on Database Systems for Advanced Applications, volume 12681, 158–173. Ramp´asek, L.; Galkin, M.; Dwivedi, V. P.; Luu, A. T.; Wolf, G.; and Beaini, D. 2022. Recipe for a General, Powerful, Scalable Graph Transformer. In Advances in Neural Information Processing Systems, volume 35, 14501–14515. Schroff, F.; Kalenichenko, D.; and Philbin, J. 2015. FaceNet: A unified embedding for face recognition and clustering. In IEEE Conference on Computer Vision and Pattern Recognition, 815–823. Shi, C.; Li, Y.; Zhang, J.; Sun, Y.; and Yu, P. S. 2017. A Survey of Heterogeneous Information Network Analysis. IEEE Transactions on Knowledge and Data Engineering, 29(1): 17–37. Song, Y.; Zhou, L.; Yang, P.; Wang, J.; and Wang, L. 2024. CS-DAHIN: Community Search Over Dynamic Attribute

14673

<!-- Page 9 -->

Heterogeneous Network. IEEE Transactions on Knowledge and Data Engineering, 36(11): 5874–5888. Wang, J.; Wang, K.; Lin, X.; Zhang, W.; and Zhang, Y. 2024a. Efficient Unsupervised Community Search with Pretrained Graph Transformer. In Proceedings of the VLDB Endowment, volume 17, 2227–2240. Wang, J.; Zhou, L.; Wang, X.; Wang, L.; and Li, S. 2024b. Attribute-sensitive community search over attributed heterogeneous information networks. Expert Systems with Applications, 235: 121153. Wang, X.; Ji, H.; Shi, C.; Wang, B.; Ye, Y.; Cui, P.; and Yu, P. S. 2019. Heterogeneous Graph Attention Network. In Proceedings of The World Wide Web Conference, 2022– 2032. Wang, Y.; Gou, X.; Xu, X.; Geng, Y.; Ke, X.; Wu, T.; Yu, Z.; Chen, R.; and Wu, X. 2024c. Scalable Community Search over Large-scale Graphs based on Graph Transformer. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 1680–1690. Wang, Y.; Gu, C.; Xu, X.; Zeng, X.; Ke, X.; and Wu, T. 2024d. Efficient and effective (k, P)-core-based community search over attributed heterogeneous information networks. Information Sciences, 661: 120076. Wang, Z.; Yuan, Y.; Zhou, X.; and Qin, H. 2020. Effective and Efficient Community Search in Directed Graphs Across Heterogeneous Social Networks. In Borovica-Gajic, R.; Qi, J.; and Wang, W., eds., Proceedings of the 31st Australasian Database Conference on Databases Theory and Applications, volume 12008, 161–172. Watts, D. J.; and Strogatz, S. H. 1998. Collective dynamics of ‘small-world’ networks. Nature, 393(6684): 440–442. Yang, F.; Ma, H.; Gao, W.; and Li, Z. 2022. Community search over heterogeneous information networks via weighting strategy and query replacement. Frontiers of Computer Science, 16(4): 164345. Ye, J.; Zhu, Y.; and Chen, L. 2023. Top-r keyword-based community search in attributed graphs. In Proceedings of the 39th IEEE International Conference on Data Engineering, 1652–1664. Ying, C.; Cai, T.; Luo, S.; Zheng, S.; Ke, G.; He, D.; Shen, Y.; and Liu, T. 2021. Do Transformers Really Perform Badly for Graph Representation? In Advances in Neural Information Processing Systems, volume 34, 28877–28888. Zhong, Q.; Liu, Y.; Ao, X.; Hu, B.; Feng, J.; Tang, J.; and He, Q. 2020. Financial Defaulter Detection on Online Credit Payment via Multi-view Attributed Heterogeneous Information Network. In Proceedings of The Web Conference, 785– 795. Zhou, Y.; Fang, Y.; Luo, W.; and Ye, Y. 2023. Influential Community Search over Large Heterogeneous Information Networks. In Proceedings of the VLDB Endowment, volume 16, 2047–2060.

14674
