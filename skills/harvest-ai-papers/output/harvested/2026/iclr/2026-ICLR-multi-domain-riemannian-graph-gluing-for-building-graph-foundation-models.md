---
title: "Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models"
source_url: https://iclr.cc/virtual/2026/oral/10010538
paper_pdf_url: https://arxiv.org/pdf/2603.00618v1
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

MULTI-DOMAIN RIEMANNIAN GRAPH GLUING FOR BUILDING GRAPH FOUNDATION MODELS

Li Sun1∗, Zhenhao Huang2, Silei Chen2, Lanxu Yang2, Junda Ye1, Sen Su1, Philip S. Yu3

1Beijing University of Posts and Telecommunications, Beijing 100876, China 2North China Electric Power University, Beijing 102206, China 3University of Illinois Chicago, IL, USA

## ABSTRACT

Multi-domain graph pre-training integrates knowledge from diverse domains to enhance performance in the target domains, which is crucial for building graph foundation models. Despite initial success, existing solutions often fall short of answering a fundamental question: how is knowledge integrated or transferred across domains? This theoretical limitation motivates us to rethink the consistency and transferability between model pre-training and domain adaptation. In this paper, we propose a fresh Riemannian geometry perspective, whose core idea is to merge any graph dataset into a unified, smooth Riemannian manifold, enabling a systematic understanding of knowledge integration and transfer. To achieve this, our key contribution is the theoretical establishment of neural manifold gluing, which first characterizes local geometry using an adaptive orthogonal frame and then “glues” the local pieces together into a coherent whole. Building on this theory, we present the GRAPHGLUE framework, which supports batched pre-training with EMA prototyping and provides a transferability measure based on geometric consistence. Extensive experiments demonstrate its superior performance across diverse graph domains. Moreover, we empirically validated GRAPHGLUE’s geometric scaling law, showing that larger quantities of datasets improve model transferability by producing a smoother manifold. Codes are available at https://github.com/RiemannGraph/GraphGlue.

## INTRODUCTION

Foundation models have revolutionized the representation learning in natural language processing Bommasani et al. (2021); Brown et al. (2020); Devlin et al. (2019) and computer vision Dosovitskiy et al. (2020) by integrating multi-domain knowledge during pre-training and transferring it to target domains. Graph-structured data are ubiquitous non-Euclidean structures in real-world applications, ranging from social network analysis Zhou et al. (2020); Sharma et al. (2024) to molecular design Guo et al. (2022); Wang et al. (2023). Hence, recent efforts have been made to replicate the success of the foundation model in the field of graphs, achieving multi-domain pre-training and cross-domain transfer learning for graphs.

Multi-domain graph pre-training is challenging given the significant semantic heterogeneity across different domains, such as social networks and biological molecules. In the literature, one line of work extracts multi-domain knowledge via Large Language Models (LLMs), leveraging the wellpretrained textual semantics but remaining limited to text-attributed graphs Zhu et al. (2025); Xia et al. (2024); Tang et al. (2024); Ren et al. (2024); Chen et al. (2024). However, many real graphs lack explicit textual attributes. Moreover, textual annotation is labor-intensive and may introduce hallucinations through LLM generation.

Rather than being tied to textual information, multi-domain pre-training for text-free graphs has garnered increasing attention recently. A series of methods seek to learn shared or invariant knowledge during pre-training using graph codebooks Wang et al. (2024); Sun et al. (2025b); Jiang et al. (2024);

∗Corresponding Author: Li Sun, lsun@bupt.edu.cn arXiv:2603.00618v1 [cs.LG] 28 Feb 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026

Bo et al. (2025), motifs Sun et al. (2025b), computation trees Wang et al. (2024; 2025c), etc. Meanwhile, advanced adaptation techniques are introduced to improve the downstream tasks, e.g., domain tokens Yu et al. (2025a); Jiao et al. (2025); Yuan et al. (2025); Wang et al. (2025a) and in-context learning Huang et al. (2023); Liu et al. (2024). While existing solutions have achieved encouraging results, a fundamental question remains inadequately addressed: how is knowledge integrated or transferred across domains? The theoretical underpinnings in this context remain underexplored. Though Wang et al. (2024); Zhang et al. (2024); Ruiz et al. (2020) give similarity measures across different domains, they do not frame model pre-training and domain adaptation within a consistent framework. This gap limits its ability to assess transfer difficulty, especially for the unseen graphs. Thus, we are motivated to rethink the consistency and transferability to target domains.

ogbn-arxiv Computers Reddit FB15k_237 PROTEINS HIV

**Figure 1.** An illustration of manifold gluing. The domains are distinguished by colors.

In this paper, we propose a fresh differential geometry perspective, whose core is the integration of any graph dataset into a unified, smooth Riemannian manifold, providing a rigorous foundation for systematically analyzing knowledge integration and transfer. To achieve this, we introduce a new theory – Neural Manifold Gluing, whose intuitive idea is to first characterize the local geometry, and then “glue” these local pieces together into a coherent whole. Specifically, we propose a sparse perturbation and an adaptive orthogonal frame to learn the local geometry. Gluing local pieces is achieved through metric compatibility along the edges (Theorem 4.5) and triangle triviality with respect to the concept of holonomy (Theorem 4.8). Finally, we smooth the manifold by controlling the change ratio of volume elements (Theorem 4.9), enhancing knowledge transport along the manifold.

Building on the theory established above, we design a pre-training-adaptation framework named GRAPHGLUE, which extends local geometry to the global scale. During pre-training, we incorporate an Exponential Moving Average (EMA) prototyping before gluing, which distinguishes domain semantics through different locations on the manifold and efficiently handles large-scale graphs in a batched manner. In the adaptation phase, GRAPHGLUE employs learnable prompts and a Riemannian Mixture-of-Experts, while gluing target domains to the pre-trained manifold, ensuring geometric consistency. A Geometric Transfer Metric (GTM) is naturally defined by metric compatibility to quantify transfer difficulty. Moreover, GRAPHGLUE exhibits a geometric scaling law: larger quantities of graph datasets produce a smoother manifold, thereby improving model transferability.

In summary, key contributions are listed as follows. 1. Problem. We investigate the theoretical underpinnings of multi-domain graph pre-training, and study a foundational problem of how knowledge is integrated and transferred across different domains. 2. Theory. We introduce a fresh differential geometry perspective for systematically understanding knowledge transfer, and propose the theory of neural manifold gluing, which consistently integrates multi-domain graphs into a unified, smooth Riemannian manifold via “gluing”. 3. Methodology. We propose a GRAPHGLUE framework based on the above theory, which supports batched pre-training for large-scale graphs and incorporates a natural metric to quantify its transferability. 4. Experiment. We evaluate GRAPHGLUE in cross-domain transfer learning and empirically demonstrate its geometric scaling law.

## RELATED WORK

Graph Foundation Models Graph Foundation Models (GFMs) aim to provide pre-trainable, general-purpose deep learning architectures for graphs Wang et al. (2025b); Liu et al. (2025). Recently, the capabilities of Large Language Models (LLMs) have extended to text-attributed graphs

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

Zhu et al. (2025); Xia et al. (2024); Tang et al. (2024); Ren et al. (2024); Chen et al. (2024). Also, GFMs have been developed for various specialized domains, such as knowledge graphs Huang et al. (2025); Luo et al. (2025), recommender systems Wu et al. (2025), and molecular graphs Xia et al. (2023); Sypetkowski et al. (2024). Given the prevalence of text-free graphs, recent efforts have focused on building general-purpose models via multi-domain pre-training Zhao et al. (2025).

Multi-domain Graph Pre-training In graph pre-training, Graph Neural Networks (GNNs) are trained by self-supervised learning—either generative Hou et al. (2022) or contrastive Veliˇckovi´c et al. (2019); Qiu et al. (2020). In light of the semantic heterogeneity across different domains, several methods have been proposed to learn shared or invariant knowledge Yuan et al. (2025); Chen et al. (2025); Wang et al. (2025a). Despite the encouraging results, the theoretical foundations of how knowledge is integrated and transferred remain underexplored.

Graph Fine-tuning and Prompt Learning The alignment of pre-trained models with downstream tasks necessitates an adaptation phase, which is roughly categorized into two paradigms: 1) Graph fine-tuning adapts the model behavior using limited target-domain data Sun et al. (2024d), and recent advances introduce parameter-efficient fine-tuning methods such as low-rank adaptation Yang et al. (2025b). 2) Graph prompting keeps pre-trained parameters frozen and enhances performance by inserting learnable prompt vectors Yu et al. (2025a); Liu et al. (2023); Sun et al. (2022b); Fang et al. (2023). Yet, how to quantify the transfer effort to target domains remains an open issue.

Riemannian Graph Representation Learning Most existing Riemannian models are tailored to specific tasks Chami et al. (2019); Grover et al. (2025); Bachmann et al. (2020); Gu et al. (2019). Recently, Sun et al. (2025b) design a new GNN backbone on the product manifold for GFM. In contrast, our focus lies on developing a framework for multi-domain pre-training, and on constructing a general manifold, rather specific ones. (Full related work is provided in Appendix E.)

NOTATIONS AND PRELIMINARIES

This part briefly reviews the key concepts of Riemannian manifold, frame and holonomy, and then states multi-domain pre-training where we reconsider its consistency and transferability from a fresh differential geometry perspective. Important notations are summarized in Appendix A.

Riemannian Geometry Riemannian geometry provides an elegant framework for studying graphs and structures. A Riemannian manifold (M, G) with dimension M is a smooth manifold M endowed with a Riemannian metric tensor G. Each point p ∈M ties to a tangent space TpM, and its volume element is the determinant of the Riemannian metric tensor, denoted as |G(p)|. The coordinate chart of tangent space is denoted as (U, x1,..., xM). Ricci curvature Ric(X, Y) governs the change ratio of volume elements along the geodesic. The concept of holonomy describes the changes of a tangent vector traversing a closed curve. Rigorous elaborations are in Appendix C.

Cartan’s Method of Moving Frame This renowned method Tron et al. (2024) offers a principled way to study manifold geometry with a frame. Though ´Elie Cartan laid the mathematical principle, its deep learning methodology remains largely unexplored. Our work seeks to bridge this gap.

Multi-domain Graph Pre-training In this context, a deep learning architecture is first pre-trained on different source domains and then adapted to a target domain. A graph is described as G = (V, E) with a feature matrix X ∈R|V|×F, where V and E denote the node set and edge set, respectively. We consider a collection of K graphs S = {S1, S2, · · ·, SK} from L domains D = {D1, D2, · · ·, DL}. A model fΘ(GNN(·)) is pre-trained on the graph dataset G with an encoder GNN(·), after which the pre-trained parameters {Θ⋆ f, Θ⋆

GNN} are frozen. The encoder is implemented with popular graph neural networks such as GCN Kipf & Welling (2017). Given a graph Gt of the target domain Dt, the pre-trained model can generate informative representations for Gt with slight adaptation. Note that the target domain can be seen Dt ∈D or unseen Dt /∈D during pre-training. Unlike existing solutions, our goal is to design a transferable graph model with a principled interpretation.

<!-- Page 4 -->

Published as a conference paper at ICLR 2026

THEORY: CONSTRUCTING A UNIFIED, SMOOTH MANIFOLD

Existing solutions often lack a principled framework to interpret how knowledge is integrated or transferred across domains. To fill this gap, we introduce a differential geometry perspective for multi-domain graph pre-training. The core of our approach is the construction of a pre-trainable, unified, and smooth Riemannian manifold, which provides a rigorous foundation for systematically analyzing knowledge integration and transfer. In the literature, Riemannian graph representation learning primarily studies the specific manifolds, e.g., hyperbolic spaces Chami et al. (2019); Yang et al. (2025a), spherical spaces Liu et al. (2022), and product manifolds Gu et al. (2019). However, constructing a general manifold underlying multi-domain graphs remains unexplored.

To achieve this, we establish a novel theory – neural manifold gluing, whose intuitive idea is to first characterize the local geometry, and then “glue” these local pieces together to form a unified, smooth Riemannian manifold. Derivations and proofs of our establishment are provided in Appendix B.

## 4.1 LEARNING LOCAL GEOMETRY WITH ADAPTIVE ORTHOGONAL FRAME

In a Riemannian manifold, the local geometry at a given point is characterized by its tangent space. Going beyond the classic Cartan’s method Tron et al. (2024), we present a deep learning approach to infer the basis of the tangent space. Specifically, we introduce a (k, M)-sparse perturbation, mimicking the directional derivative Dvf = limt→0 f(p+tv)−f(p)

t, to generate a set of tangent vectors at the given point, after which an adaptive orthogonal frame is applied to form the basis of the tangent space. Note that the perturbation is attached with a parametric fGNN in our establishment. Definition 4.1 ((k, M)-sparse perturbation). Given a graph perturbation set that consists of M nodes P = {pi} with parameters {pi}, for G = (V, E), the perturbed graph is denoted as ˆG =

(ˆV, ˆE):= G⊕P =

V ∪{pm}M m=1, E ∪{(vim, pm)}k,M im=1,m=1

, where (vi, pm) is a edge weighted by an attentive function h(xi, pm), vim are k nodes selected based on top-k h(xi, pm). Definition 4.2 (Adaptive Orthogonal Frame, AOF). With tangent vectors generated by the above perturbation and a graph encoder fGNN, after QR-decomposition with length recovery, the adaptive orthogonal frame is {wm: z(i) 7→w(i)

m ∈Rd}M m=1 for every representation z(i). There exists a dual frame {θm} such that θm(wl) = δml, where δml is the Kronecker delta.

We show that the aforementioned length recovery of the basis is important, since the length of the tangent vector, describing the space deformation, is upper-bounded by the perturbation. In fact, the angles and lengths of the basis vectors reflect how the space is stretched and twisted, respectively. Theorem 4.3 (Upper bound of Tangent Vector Length, Appendix B.1). Given a connected G with N nodes, the adjacency matrix A, the Laplacian L, and the feature matrix of perturbation nodes P, apply (k, M)-sparse perturbation to G, suppose kM

N = ε, where ε > 0 is small, and added edge weights satisfy P l h(vi, pl) = 1. Then, the upper bound ∥wp m∥≤(1 + ε)∥P ∥holds, where wp m is the component of wm determined by perturbation.

Thus, the local metric at each point is derived through the basis vectors of its tangent space. In particular, given the representation of Gi as zi ∈Rd, the coordinates Ui in a neighborhood around zi, and the learned dual frame θm, the local metric tensor Gi on Ui takes the form of Gi(w(i)

m, w(i)

l) = gml(zi)(θm ⊗θl), where gml(zi) = ⟨w(i)

m, w(i)

l ⟩. Equivalently, the matrix form of Gi is written as

Gi = W (i)⊤W (i) = diag(∥w1∥2,..., ∥wM∥2), (1)

with the basis of tangent space formulated as W (i) = [w(i)

1,..., w(i) M ] ∈Rd×M. The inner product w.r.t. Gi is given as Gi(u, v):= u⊤Giv for tangent vectors u, v ∈Tz(i)Ui.

## 4.2 GLUING LOCAL PIECES TO FORM A SMOOTH MANIFOLD

Given a set of isolated Riemannian manifolds {M(i) = (z(i), Tz(i)Ui, Gi)}N i=1, we are devoted to gluing them together to construct a unified, smooth Riemannian manifold with a global metric. In a nutshell, These local pieces are connected through the edges and triangles with the concept of holonomy, after which the constructed manifold is smoothed by controlling the Ricci curvature.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

Gluing. We begin with the compatibility of metric along edges, which is necessary for the existence of a global metric. According to Edelsbrunner & Harer; Chung, the gluing boundary can be defined by the adjacency in graph topology. To preserve compatibility, we perform a tangent translation along an edge (i, j) ∈E, referred to as edge tangent translation, to transform the local metrics. We show that it ensures metric compatibility along an edge, and is proven to induce a global metric. In addition, its computational complexity is reduced to O(M) with the QR-decomposition above. Definition 4.4 (Edge Tangent Translation). Given an edge (i, j) ∈E, the tangent spaces of its two endpoints Tz(i)Ui and Tz(j)Uj, and the Riemannian metric of Tz(i)Ui denoted as Gi, the edge tangent translation is defined as a linear map P (i,j): Tz(i)Ui →Tz(j)Uj on edge (i, j) ∈E as

P (i,j) = G−1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j. (2)

Theorem 4.5 (Tangent Edge Translation as Isometry, Appendix B.2). The tangent edge translation in Definition 4.4 is the optimal solution of minP ∈GL(M)

P ⊤GjP −Gi

2

F, (3)

where GL denotes the general linear group, such that Gj(P (i,j)u, P (i,j)v) = Gi(u, v), which induces an isometry ϕ(i,j) between manifold boundaries ∂Ui and ∂Uj.

Theorem 4.6 (Existence of Global Metric, Appendix B.3). Let ({Gi}N i=1, {P (i,j)}(i,j)∈E) be local metrics and tangent edge translations. There exists a unique global continuous metric G on (S ϕ)N i=1Ui such that the restriction of G|Ui = Gi for all i.

The edge tangent translations connect gluing boundaries in accordance to Theorem 4.5 and 4.6. However, when gluing along higher-order motifs, such as triangles and cycles, some offsets may occur when going round trips, so that gluing boundaries are not well aligned. In other words, although the glued manifold is connected, it is not yet continuous everywhere. To address this issue, we introduce the concept of holonomy, describing how the tangent vector changes when traversing along a closed curve, and define a holonomy map to measure the changes. We show that, when the holonomy map of triangles is trivial, the offset at the gluing boundaries is eliminated. Definition 4.7 (Holonomy Map and Holonomy Loss). Let Z1(G) denote the real vector space of 1-cycles on graph G = (V, E) under symmetric difference. For any cycle C = (i0, i1,..., iL = i0), its holonomy map is defined as the composition of transport maps along the path,

H(C):=

YL−1 ℓ=0 P (iℓ,iℓ+1) ∈GL(M). (4)

The collection P:= {P (i,j)} is said to be trivial if H(C) is the identity map for ∀C ∈Z1(G). Given the set of all triangles Aijk = ((vi, vj), (vj, vk)), the corresponding holonomy loss is formulated as

Lholo(G) = 1 |A|

X

Aijk ∥P (k,i)P (j,k)P (i,j) −I∥2

F. (5)

Theorem 4.8 (Triangle Triviality, Appendix B.4). If every edge belongs to at least one triangle, and H(T) = I for all triangular cycles T in G, then H(C) = I for all cycles C ∈Z1(G).

Smoothing. So far, the glued manifold has achieved C1 continuity, but C2 continuity is required to yield a smooth global metric and to eliminate “fold” that hinders knowledge transport along the manifold. To bridge this gap, we visit the concept of Ricci curvature, a kind of C2 continuity on the manifold, which governs the rate of changes of the volume element along the geodesic. Nevertheless, calculating Ricci curvature is rather expensive Petersen (2016); Ollivier (2007). Instead, we propose an alternative of volume change ratio between two endpoints, which is shown to sufficiently determine whether the geodesic is “convex” or “concave”. Theorem 4.9 (Ricci Curvature Estimation, Appendix B.5). Given a graph G = (V, E) and an edge (i, j) ∈E, let z(i), z(j) ∈M be the corresponding embedded points, and γ: [0, 1] →M be the unit-speed geodesic connecting them, i.e., γ(0) = z(i), γ(1) = z(j). The sign of the Ricci curvature along ˙γ can be estimated by the ratio of metric determinants:

r(z(i), z(j)):= det Gi det Gj

≈1 −1

3Ric(˙γ). (6)

<!-- Page 6 -->

Published as a conference paper at ICLR 2026

AOF

Domain 1

Domain 2

...... Domain n

GNN

Generate Tangent Space

𝓛𝐩𝐫𝐨𝐭𝐨

Domain 1

Domain 2

Domain n

Target Domain

… AOF

𝓛𝐚𝐝𝐚𝐩

…

𝓛𝐠𝐥𝐮𝐞

…

Sparse perturbation: M Virtual Nodes

෡G1

෡G2

෡G𝒏 ①②…ⓜ

①②…ⓜ

①②…ⓜ Ƹ𝑧𝟏

Ƹ𝑧𝟐

Ƹ𝑧𝟏

Ƹ𝑧𝟐

Ƹ𝑧𝟐

Ƹ𝑧𝟏

Transferability

Metric

Prototypes Learnable

Frozen Manifold Skeleton

Unified Manifold

RMOE

EMA & Riemannian Prototypes

GTM = ∆H + ∆C

**Figure 2.** An Illustration of GRAPHGLUE Framework.

Accordingly, the volume element √det Gi varies smoothly along the path of length k, implying that the Ricci curvature changes continuously along that path, referred to as Log-Determinant k-order smoothness. Thus, we can investigate the k-order smoothness with a scalar field of volume element, and formulate a Ricci curvature loss which encourages the glued manifold to be smooth.

Definition 4.10 (k-order Smoothness and Curvature Loss). Define gi = 1

2 log det Gi as a scalar field over G, representing the logarithmic volume density at node vi. We say the manifold structure exhibits log-determinant smoothness if g ∈R|V| minimizes the graph Dirichlet energy: EDir[g] = ∥Lkg∥2, where L is the (normalized) Laplacian of G. In light of computational efficiency in practice, we define the curvature loss function of 2-order smoothness as follows,

LCurv(G) = 1 |A|

X

Aijk | log(rij) −log(rjk)|2 (7)

Geometric Scaling Law Consequently, any graph datasets are merged into a unified, smooth Riemannian manifold, allowing us to study knowledge transfer within the framework of differential geometry. As the quantities of graphs increase, (F, G, P) approximates an ideal manifold, and thus we deduce a geometric scaling law that larger quantities of datasets improve model transferability with a smoother manifold, which is empirically validated in Sec. 6.2.

Theorem 4.11 (Gluing into a Smooth Manifold, Appendix B.6). For any graph dataset G, if G is log-determinant ∞-order smooth, and P is trivial with induced metric-preserving diffeomorphism ϕ, then (F, G, P) glues to a smooth Riemannian manifold (F, G), where F = (S ϕ)N i=1Ui.

## 5 GRAPHGLUE: GEOMETRIC MULTI-DOMAIN GRAPH PRE-TRAINING

Building on our theory of neural manifold gluing, we present a novel pretraining-adaptation framework, GRAPHGLUE, as illustrated in Fig. 2. The pre-training first learns the local geometry and then glues these local pieces together as introduced in Sec. 4. Moreover, before gluing, an Exponential Moving Average (EMA) prototyping is proposed to distinguish domain semantics through different locations on the manifold, while enabling batched pre-training to efficiently handle largescale graphs. Then, we leverage prompt adaptation and a Riemannian Mixture-of-Experts (MoE), while gluing the target domain to the pre-trained manifold for geometric consistency. A Geometric Transfer Metric (GTM) is naturally induced to measure the transfer difficulty. The overall procedure is summarized in Algorithm 1.

## 5.1 PRE-TRAINING WITH EMA PROTOTYPING

For multi-domain source graphs S = {S1,..., SK}, we associate each graph with a Riemannian prototype, which is given as a tuple of global location and Riemannian metrics, (zSk, log GSk) =

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICLR-multi-domain-riemannian-graph-gluing-for-building-graph-foundation-models/page-006-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

Published as a conference paper at ICLR 2026

1 |Sk|

P

G∈Sk zG, 1 |Sk|

P

G∈Sk log G(zG)

. The challenges of Riemannian prototyping are dual: computation efficiency for large-scale graphs, and semantics distinction across different domains. To address the first challenge, we develop an EMA for Riemannian prototyping. For each batch, we perform the following updating rules, zSk ←βzSk + (1 −β) 1

|Bk|

X

G∈Bk zG (8)

log GSk ←β log GSk + (1 −β) 1

|Bk|

X

G∈Bk log G(zG), (9)

where β ∈(0, 1) is a momentum coefficient, and log means matrix logarithm. This EMA update ensures that (zSk, log GSk) gradually converge to the stable average value throughout pre-training Morales-Brotons et al. (2024); Izmailov et al. (2019). Note that the metric matrix belongs to a symmetric positive-definite manifold, and we utilize the log update, different from the traditional ones. To address the second challenge, we incorporate a sample-prototype contrastive loss that encourages graph prototypes to be well separated on the manifold, distinguishing domain semantics.

Lproto(G) = −1

K

K X k=1 log exp(sim(zG, zSk)/τ) PK j=1 exp(sim(zG, zSj)/τ)

. (10)

5.2 CONSISTENT ADAPTATION & QUANTIFIABLE TRANSFERABILITY

GRAPHGLUE employs prompt adaptation and Riemannian MoE to generate representations, while we emphasize geometric consistency between the pre-trained manifold and target graphs by “gluing”. To be specific, for a target sample GT, we first infer the global coordinates and local metric through prompting. With the coordinates zT, local metric Gz and basis vectors of the tangent space W T = [wT

1,..., wT M] given by the pre-trained model, we introduce a learnable prompt matrix Q ∈Rd×d. The global coordinates is adapted as zadapt = QzT. Note that the metric adaptation is challenging owing to the orthogonal requirement of basis vectors. Thus, instead of prompting the pre-trained local metric, we apply the prompt matrix Q to W T, and the adapted local metric is derived as Gadapt = diag

∥QwT

1 ∥2,..., ∥QwT M∥2

, where wT are the basis vectors undergoing the proposed adaptive orthogonal frame. Second, to ensure consistency, we glue the target sample to the pre-trained Riemannian manifold F, where Riemannian prototypes are treated as the anchors to align the target. In particular, we construct a transfer graph G0 by connecting the target to its k-nearest prototypes, and apply Lholo(G0) and Lcurv(G0) proposed in Sec. 4, penalizing non-trivial holonomy and abrupt volume changes, respectively. Third, we present a Riemmanian MoE where each Riemannian prototype (zSk, log GSk) serves as an expert and its weight is given by a gating function βk = gk(zadapt, Gadapt). This MoE generates log Galign = PK k=1 βk log GSk. summarized from the experts. Accordingly, we obtain the final representation ztask = zT; log Gadapt; log Galign

, where ztask ∈Rd+2M since log Gadapt, log Galign are both diagonal matrix that can be vectorized. The overall adaptation loss is given as

Ladap = Ltask(ztask; ytask) + λLglue, Lglue = Lholo(G0) + Lcurv(G0), (11)

where λ balances task-specific learning with consistency, and ytask is the label of downstream task.

On Transferability Within the framework of differential geometry, we are able to systematically analyze knowledge transfer across different domains, and transfer effort of GRAPHGLUE is naturally measured by the geometric compatibility. We introduce Geometric Transfer Metric (GTM) which is defined as the minimal geometric deformation required to merge the target GT into the pre-trained manifold F without disrupting its learned local geometry. GTM is computed along with the adaptation and decomposes into two interpretable components as follows,

GTM(GT; S) = ∆H + ∆C, ∆H = Lholo(G0), ∆C = Lcurv(G0). (12)

1. Holonomy disagreement ∆H. It measures how the holonomy map deviates from identity along paths connecting the target to its nearest prototype, interpreted as the “twisting” induced by GT. 2. Curvature disagreement ∆C. It is computed as the discrepancy between the volume element √det Gi, indicating the dismatch with respect to Ricci curvature according to Theorem 4.9. The natural interpretation is given as the “bending” or abrupt change in local volume.

<!-- Page 8 -->

Published as a conference paper at ICLR 2026

Accordingly, a low GTM means that the target is seamlessly integrated F with trivial deformation, implying high transferability; in contrast, a high value shows that the target is geometrically alien, thus requiring significant effort to fit the geometry of F. Different from similarity measures between source and target domains Wang et al. (2024), GTM examines the geometric consistency from GRAPHGLUE itself, and provides an interpretable assessment of transfer difficulty.

Further Insight The generalization error is related to the smoothness of the model objective Bartlett et al. (2017); Scaman & Virmaux (2018). In fact, GRAPHGLUE controls the smoothness by inducing a smooth global metric. Specifically, Lholo guarantees the topological continuity of gluing boundaries, while Lcurv achieves k-order smooth by log-determinant smoothness in Definition 4.10, similar to Czarnecki et al. (2017). The complexity analysis is provided in Appendix D.2, D.3.

## 6 EXPERIMENTS

We conduct experiments on six representative domains to evaluate cross-domain transfer learning performance. Also, we examine the transferability measure (GTM), geometric scaling law, the effect of incorporating graphs of distinct semantics, and the geometric interpretation. Ablation study, hyperparameter sensitivity and performance on heterophilic graphs are in Appendix G.2, G.3, G.4.

## 6.1 EXPERIMENTAL SETUPS

Datasets & Baselines We carefully select 6 representative benchmark datasets, covering various domains: an academic citation network Arxiv, a product co-purchase graph Computers, a social network Reddit, a knowledge graph FB15k 237, and benchmarks on bioinformatics PROTEINS and chemoinformatics HIV. We compare GRAPHGLUE against baselines from 3 main categories: (1) Supervised GNNs: GCN Kipf & Welling (2017), GraphSAGE Hamilton et al. (2017), and GIN Xu et al. (2019). (2) Self-Supervised GNNs: DGI Veliˇckovi´c et al. (2019), GraphMAE Hou et al. (2022), and GCC Qiu et al. (2020). (3) Graph Foundation Models: PRODIG Huang et al. (2023), GFT Wang et al. (2024), RAGraph Jiang et al. (2024), SAMGPT Yu et al. (2025a), GCOPE Zhao et al. (2024), and MDGFM Wang et al. (2025a). Detailed descriptions are specified in Appendix F.

## Evaluation

Protocol Our evaluation adopts a leave-one-out cross-domain setup, where models are pre-trained on five source datasets and fine-tuned on a single held-out target dataset. We use a few-shot fine-tuning setting, leveraging k labeled samples per class (k ∈{1, 5}) from the target task for adaptation. The remaining target data is randomly split into 10% for validation and 90% for testing. We evaluate performance on three tasks: node/edge classification measured by ACC and graph classification measured by AUC. All reported results are the average of 10 independent runs.

## 6.2 RESULTS AND DISCUSSION

Main Results on Cross-domain Transfer Learning As shown in Table 1, the empirical results demonstrate the superior effectiveness of GRAPHGLUE in challenging few-shot scenarios. For instance, in the 1-shot setting, it outperforms the strongest baselines on Computers and Reddit by significant margins of 4.9% and 2.3%, respectively. This strong performance is often maintained as more data becomes available. In the 5-shot setting on the Reddit dataset, GRAPHGLUE achieves 85.0% ACC, exceeding the runner-up by 4.6%. These results suggest that the geometric construction of GRAPHGLUE enhances the model performance, and we will demonstrate additional benefits of the constructed smooth manifold in the following parts.

Ablation study on the effectiveness of proposed Lcurv and Lholo are provided in Appendix G, showing that both gluing via holonomy and smoothing via Ricci curvature are important to downstream tasks.

On Transferability Measure This part shows how the proposed measure of GMT aligns with the transfer effort of the pre-trained model. To this end, we pre-train the model in Arxiv, Reddit, FB15k 237, PROTEINS, and HIV datasets, then conduct transfer settings on Computers with 2000 epochs. In this case, holonomy loss vanishes rapidly during training, and thus we investigate the curvature loss in Figure 3, where x-axis is the training epoch. We plot the test task loss of crossentropy for the classification task on the y-axis on the left. In the top of Figure 3, we find that, as

<!-- Page 9 -->

Published as a conference paper at ICLR 2026

**Table 1.** Performance of cross-domain transfer on various downstream tasks, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined.

## Model

Node Classification Link Classification Graph Classification

Arxiv Computers Reddit FB15k 237 PROTEINS

1-shot 5-shot 1-shot 5-shot 1-shot 5-shot 1-shot 5-shot 1-shot 5-shot

GCN 12.6±1.7 27.6±2.1 33.8±3.8 65.7±4.2 11.1±2.1 28.3±1.0 32.1±2.3 52.4±1.8 50.1±13.0 55.0±9.9 GraphSAGE 14.6±3.7 26.1±2.2 35.4±8.2 66.7±4.4 14.6±2.3 22.2±1.1 35.7±2.1 58.9±1.5 58.9±2.7 60.4±1.3 GIN 11.2±2.0 26.0±2.4 44.7±6.0 69.5±3.5 18.5±1.8 29.0±1.6 38.2±2.5 63.7±1.7 54.2±13.5 58.8±5.0

GCC 12.6±2.0 26.8±2.1 34.8±6.1 62.6±3.1 54.7±5.6 65.2±1.5 47.8±1.9 73.6±1.2 59.2±7.9 64.2±3.0 DGI 13.3±3.3 27.1±2.3 35.2±7.5 61.0±3.2 60.0±4.8 62.7±2.2 42.5±2.0 68.3±1.4 53.1±8.4 53.3±6.2 GraphMAE 12.6±1.7 27.6±2.1 33.8±3.8 65.7±4.2 11.1±2.1 28.3±1.0 51.3±1.8 77.2±1.0 60.1±13.0 65.0±9.9

PRODIGY 28.4±2.2 33.6±2.8 45.3±4.1 52.7±3.6 35.6±3.2 42.3±2.9 53.5±1.0 72.1±6.9 48.9±5.4 55.2±4.7 GFT 26.5±2.4 36.7±1.9 54.6±4.0 69.1±3.5 58.8±2.5 66.2±1.4 58.0±1.3 79.1±1.6 55.4±5.8 62.1±3.5 RAGraph 18.7±2.5 32.3±1.7 46.2±4.3 62.3±3.7 52.5±3.4 63.0±1.3 52.1±3.0 64.5±2.5 51.4±5.1 58.6±2.8 SAMGPT 24.1±3.8 34.4±2.2 47.6±7.4 60.8±3.6 62.8±4.2 75.1±1.6 57.4±2.4 77.6±2.7 52.4±3.1 59.1±2.6 GCOPE 26.5±5.5 39.1±1.9 54.5±9.1 72.2±2.8 62.7±4.5 80.4±0.7 58.2±2.6 79.3±2.2 55.1±3.5 64.8±2.4 MDGFM 26.0±2.4 32.2±1.7 46.6±8.4 64.0±5.3 64.8±3.3 76.5±1.7 56.1±1.6 77.6±2.0 53.4±5.3 57.7±3.4

GRAPHGLUE 28.8±5.2 37.0±2.3 59.5±7.0 73.2±0.7 67.1±3.3 85.0±1.1 59.7±5.2 81.5±2.3 59.8±4.8 65.3±2.4

0 200 400 600 800 Epoch

0.50

0.75

1.00

1.25

1.50

1.75

2.00

Loss

Task Loss vs Curvature Loss

Task Loss

0.3

0.4

0.5

0.6

## 0.7 Curvature Loss

Oscillation ±1

0 200 400 600 800 Epoch

0.00

0.02

0.04

0.06

0.08

0.10

0.12

0.14

Oscillation Amplitude

Curvature Loss Oscillation Decay (Log Scale)

Rolling Std Trend

100

101

**Figure 3.** GTM vs Test Task Loss.

curvature loss decreases and converges, the test task loss exhibits the same pattern, and it suggests that GMT measures the effort of training the pre-trained model in transfer setting. Moreover, at the bottom of Figure 3, it shows another feature of curvature loss that the convergence of its oscillation amplitude implies the convergence of the test task loss, which meets the theory in Keskar et al. (2017); Czarnecki et al. (2017).

Reddit Only Reddit+PROTEINS Reddit+PROTEINS+HIV Pre-training Corpus 50

55

60

65

70

ACC (%)

61.53 62.71

64.33

58.32 58.16

54.95

GraphGlue GCOPE

**Figure 4.** Effect of including distinct domains during pre-training.

Case Study We conduct an interesting case study to examine the effect of including semantically distinct data during pre-training. To this end, we incrementally expand a Reddit-only pre-training with the distinct PROTEINS and HIV datasets, and consistently evaluate on Reddit under the 1-shot setting. As shown in Figure 4, GRAPHGLUE achieves a steady improvement with the inclusion of each dataset. In contrast, GCOPE suffers from negative transfer and results in possible performance decline. This result provides evidence that GRAPHGLUE can effectively incorporate knowledge from even vastly different domains to enhance its capabilities.

On Geometric Scaling Law We validate the geometric scaling law by enlarging the quantities of pre-training datasets. Specifically, we show the few-shot performance on Computers and Reddit in Figure 5, where the original datasets are same as that in Figure 3, denoted as +0, and we incrementally incorporate Pubmed, Photo, FacebookPagePage, WordNet18RR, MUATG and Lipophilicity in order, referred to as +1, +2, +3, +4, +5 and +6, respectively. In the 1shot setting, average accuracy rises steadily while transfer loss drops consistently, both well-fitted by logarithmic functions (blue curves), and thus it exhibits clear scaling laws. 5-shot performance remains more stable (red curves), with only marginal gains in accuracy and a slight reduction in loss. The insight is that, under extreme data scarcity (1-shot), the performance is highly sensitive to

<!-- Page 10 -->

Published as a conference paper at ICLR 2026

+0 +1 +2 +3 +4 +5 +6 Pre-training Datasets Size

50

60

70

80

Average ACC (%)

61.03 61.01

67.38 67.12

69.94 70.88 71.85

73.07 74.41 73.14 74.85 75.37 74.30 74.22

1-shot ACC ln(y)=0.09ln(x)+4.09 5-shot ACC ln(y)=0.01ln(x)+4.29

+0 +1 +2 +3 +4 +5 +6 Pre-training Datasets Size

1.0

1.5

2.0

Transfer Loss

1.79 1.76

1.56

1.28 1.39 1.33 1.25

1.24 1.20

1.34 1.29 1.37

1.16 1.05

1-shot loss ln(y)=-0.20ln(x)+0.63 5-shot loss ln(y)=-0.04ln(x)+0.26

(a) Computers

+0 +1 +2 +3 +4 +5 +6 Pre-training Datasets Size

70

80

90

Average ACC (%)

75.85

78.64 79.77 81.48 81.33 81.77 82.74

85.89 85.51 86.85 86.03 87.11 87.96 87.13

1-shot ACC ln(y)=0.04ln(x)+4.33 5-shot ACC ln(y)=0.01ln(x)+4.45

+0 +1 +2 +3 +4 +5 +6 Pre-training Datasets Size

0.6

0.8

1.0

1.2

1.4

Transfer Loss

1.18

1.07 1.03 0.96 0.97 0.92 0.90

0.70 0.72 0.72 0.72 0.69 0.66 0.67

1-shot loss ln(y)=-0.14ln(x)+0.16 5-shot loss ln(y)=-0.03ln(x)+-0.32

(b) Reddit

**Figure 5.** Geometric scaling law on (a) Computers and (b) Reddit datasets.

the pre-trained model’s capacity, the expressive power of the learned manifold, while more labeled samples restrain such scaling effect. The observed logarithmic scaling supports our claim on the scaling law.

ogbn-arxiv Computers Reddit FB15k_237 PROTEINS HIV

**Figure 6.** Visualization of the pre-trained manifold from 6 datasets.

Visualization & Geometric Interpretation To illustrate our intuition, we visualize a 3D per-trained manifold on the 6 datasets in Figure 6, where the configuration is detailed in Appendix G. We observe that the datasets—Reddit (social network), Arxiv (citation network), Computers (e-commerce network), and FB15k 237 (knowledge graph)—exhibit substantial semantic overlap while retaining the difference. Their corresponding regions on the manifold lie in close proximity, sometimes intermingling owing to shared semantics, yet remain distinguishable. The two chemistry-related datasets (PROTEINS and HIV) are well-separated from the others on the learned manifold. That is, the proposed neural manifold gluing captures the complicated domain semantics. Also, the smoothness is generally ensured, facilitating knowledge transport along the manifold. The visualization underscores our framework’s ability to unify diverse domains into a coherent geometric structure, which forms the foundation for effective crossdomain transfer.

## 7 CONCLUSION

This work present the first multi-domain graph pre-training framework through the lens of Riemannian geometry, enabling the merging of arbitrary graph datasets into a unified, smooth Riemannian manifold and facilitating a principled understanding of knowledge transfer across different graphs. The theoretical contribution lies in the establishment of neural manifold gluing, which “glues” the local pieces together into a coherent whole. Building on this theory, we introduce the GRAPHGLUE framework, supporting the batched pre-training and providing a means to measure its transferability. Furthermore, we empirically validate the geometric scaling law of GRAPHGLUE.

## ACKNOWLEDGEMENT

This work is supported in part by NSFC under grants 62202164. Philip S. Yu is supported in part by NSF under grants III-2106758, and POSE-2346158.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

## REFERENCES

Gregor Bachmann, Gary B´ecigneul, and Octavian-Eugen Ganea. Constant curvature graph convo- lutional networks. In Proceedings of the 37th International Conference on Machine Learning (ICML), volume 119, pp. 486–496, 2020.

Peter L Bartlett, Dylan J Foster, and Matus J Telgarsky. Spectrally-normalized margin bounds for neural networks. In Advances in Neural Information Processing Systems 31 (NeurIPS), volume 30, pp. 6240–6249, 2017.

Beatrice Bevilacqua, Joshua Robinson, Jure Leskovec, and Bruno Ribeiro. Holographic node repre- sentations: Pre-training task-agnostic node embeddings. In Proceedings of the 13th International Conference on Learning Representations (ICLR), 2025.

Jianyuan Bo, Hao Wu, and Yuan Fang. Quantizing text-attributed graphs for semantic-structural integration. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2 (KDD), pp. 107–118, 2025.

Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ B. Altman, Simran Arora, Sydney von Arx,

Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri S. Chatterji, Annie S. Chen, Kathleen Creel, Jared Quincy Davis, Dorottya Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren E. Gillespie, Karan Goel, Noah D. Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei Koh, Mark S. Krass, Ranjay Krishna, Rohith Kuditipudi, and et al. On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258, 2021.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,

Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, and et al. Language models are few-shot learners. Advances in neural information processing systems (NeurIPS), 33:1877– 1901, 2020.

Ines Chami, Zhitao Ying, Christopher R´e, and Jure Leskovec. Hyperbolic graph convolutional neural networks. In Advances in Neural Information Processing Systems 31 (NeurIPS), volume 32, 2019.

Haibo Chen, Xin Wang, Zeyang Zhang, Haoyang Li, Ling Feng, and Wenwu Zhu. AutoGFM:

Automated graph foundation model with adaptive architecture customization. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025.

Runjin Chen, Tong Zhao, Ajay Kumar Jaiswal, Neil Shah, and Zhangyang Wang. Llaga: Large language and graph assistant. arXiv preprint arXiv:2402.08170, 2024.

Fan R. K. Chung. Spectral Graph Theory. Number 92 in Regional Conference Series in Mathemat- ics. American Mathematical Society, reprint edition. ISBN 978-0-8218-0315-8.

Wojciech M. Czarnecki, Simon Osindero, Max Jaderberg, Grzegorz Swirszcz, and Razvan Pascanu.

Sobolev training for neural networks. In Advances in Neural Information Processing Systems 31 (NeurIPS), volume 30, 2017.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of the 2019 Conference of the North American chapter of the Association for Computational Linguistics (NAACL), pp. 4171–4186, 2019.

Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas

Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929, 2020.

H. Edelsbrunner and J. Harer. Computational Topology: An Introduction. Applied Mathematics.

American Mathematical Society. ISBN 978-0-8218-4925-5.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Taoran Fang, Yunchao Zhang, Yang Yang, Chunping Wang, and Lei Chen. Universal prompt tuning for graph neural networks. In Advances in Neural Information Processing Systems 37 (NeurIPS), 2023.

Aditya Grover and Jure Leskovec. node2vec: Scalable feature learning for networks. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2016.

Karish Grover, Geoffrey J. Gordon, and Christos Faloutsos. CurvGAD: Leveraging curvature for enhanced graph anomaly detection. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025.

Albert Gu, Frederic Sala, Beliz Gunel, and Christopher R´e. Learning mixed-curvature representa- tions in product spaces. In Proceedings of the 7th International Conference on Learning Representations (ICLR), 2019.

Zhichun Guo, Kehan Guo, Bozhao Nan, Yijun Tian, Roshni G Iyer, Yihong Ma, Olaf Wiest, Xian- gliang Zhang, Wei Wang, Chuxu Zhang, et al. Graph-based molecular representation learning. arXiv preprint arXiv:2207.04869, 2022.

William L. Hamilton, Rex Ying, and Jure Leskovec. Inductive representation learning on large graphs. In Advances in Neural Information Processing Systems 29 (NeurIPS), 2017.

Allen Hatcher. Algebraic Topology. Cambridge University Press, 2002. ISBN 978-0-521-79540-1.

Morris W. Hirsch. Differential Topology, volume 33 of Graduate Texts in Mathematics. Springer,

1976. ISBN 978-1-4684-9451-8 978-1-4684-9449-5. doi: 10.1007/978-1-4684-9449-5.

Zhenyu Hou, Xiao Liu, Yukuo Cen, Yuxiao Dong, Hongxia Yang, Chunjie Wang, and Jie Tang.

Graphmae: Self-supervised masked graph autoencoders. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD), pp. 594–604, 2022.

Qian Huang, Hongyu Ren, Peng Chen, Gregor Krˇzmanc, Daniel Zeng, Percy S Liang, and Jure

Leskovec. Prodigy: Enabling in-context learning over graphs. In Advances in Neural Information Processing Systems (NeurIPS), volume 36, pp. 16302–16317, 2023.

Xingyue Huang, Pablo Barcelo, Michael M. Bronstein, Ismail Ilkan Ceylan, Mikhail Galkin, Juan L

Reutter, and Miguel Romero Orth. How expressive are knowledge graph foundation models? In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025.

Pavel Izmailov, Dmitrii Podoprikhin, Timur Garipov, Dmitry Vetrov, and Andrew Gordon Wilson.

Averaging weights leads to wider optima and better generalization, 2019.

Xinke Jiang, Rihong Qiu, Yongxin Xu, Yichen Zhu, Ruizhe Zhang, Yuchen Fang, Chu Xu, Junfeng

Zhao, and Yasha Wang. Ragraph: A general retrieval-augmented graph learning framework. Advances in Neural Information Processing Systems (NeurIPS), 37:29948–29985, 2024.

Pengfei Jiao, Jialong Ni, Di Jin, Xuan Guo, Huan Liu, Hongjiang Chen, and Yanxian Bi. Hgmp:

Heterogeneous graph multi-task prompt learning. In Proceedings of the 34th International Joint Conference on Artificial Intelligence (IJCAI), pp. 2982–2990, 2025.

Ce Ju and Cuntai Guan. Graph neural networks on spd manifolds for motor imagery classification:

A perspective from the time–frequency analysis. IEEE Transactions on Neural Networks and Learning Systems, 35, 2024.

Nitish Shirish Keskar, Dheevatsa Mudigere, Jorge Nocedal, Mikhail Smelyanskiy, and Ping Tak Pe- ter Tang. On large-batch training for deep learning: Generalization gap and sharp minima. In Proceedings of the 5th International Conference on Learning Representations (ICLR), 2017.

Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In Proceedings of the 3rd International Conference on Learning Representations (ICLR), 2015.

Thomas N. Kipf and Max Welling. Semi-supervised classification with graph convolutional net- works. In Proceedings of the 5th International Conference on Learning Representations (ICLR), 2017.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Hao Liu, Jiarui Feng, Lecheng Kong, Ningyue Liang, Dacheng Tao, Yixin Chen, and Muhan Zhang.

One for all: Towards training one graph model for all classification tasks. In Proceedings of the 12th International Conference on Learning Representations. OpenReview.net, 2024.

Jiawei Liu, Cheng Yang, Zhiyuan Lu, Junze Chen, Yibo Li, Mengmei Zhang, Ting Bai, Yuan Fang,

Lichao Sun, Philip S Yu, et al. Graph foundation models: Concepts, opportunities and challenges. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2025.

Yi Liu, Limei Wang, Meng Liu, Yuchao Lin, Xuan Zhang, Bora Oztekin, and Shuiwang Ji. Spherical message passing for 3d molecular graphs. In Proceedings of the 10th International Conference on Learning Representations (ICLR), 2022.

Zemin Liu, Xingtong Yu, Yuan Fang, and Xinming Zhang. Graphprompt: Unifying pre-training and downstream tasks for graph neural networks. In Proceedings of the 32nd ACM Web Conference (WWW), 2023.

Ilya Loshchilov and Frank Hutter. SGDR: Stochastic gradient descent with warm restarts. In Pro- ceedings of the 5th International Conference on Learning Representations (ICLR), 2017.

Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Dinh Phung, Chen Gong, and Shirui Pan. Gfm-rag:

Graph foundation model for retrieval augmented generation, 2025.

Daniel Morales-Brotons, Thijs Vogels, and Hadrien Hendrikx. Exponential moving average of weights in deep learning: Dynamics and benefits. Transactions on Machine Learning Research, 2024.

Yann Ollivier. Ricci curvature of markov chains on metric spaces, 2007.

Peter Petersen. Riemannian Geometry, volume 171 of Graduate Texts in Mathematics. Springer

International Publishing, 2016. ISBN 978-3-319-26652-7 978-3-319-26654-1. doi: 10.1007/ 978-3-319-26654-1.

Jiezhong Qiu, Qibin Chen, Yuxiao Dong, Jing Zhang, Hongxia Yang, Ming Ding, Kuansan Wang, and Jie Tang. Gcc: Graph contrastive coding for graph neural network pre-training. arXiv preprint arXiv:2006.09963, 2020.

Xubin Ren, Jiabin Tang, Dawei Yin, Nitesh Chawla, and Chao Huang. A survey of large language models for graphs. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD), pp. 6616–6626, 2024.

Luana Ruiz, Luiz Chamon, and Alejandro Ribeiro. Graphon neural networks and the transferability of graph neural networks. In Advances in Neural Information Processing Systems, volume 33, pp. 1702–1712. Curran Associates, Inc., 2020.

Kevin Scaman and Aladin Virmaux. Lipschitz regularity of deep neural networks: analysis and effi- cient estimation. In Advances in Neural Information Processing Systems 32 (NeurIPS), NIPS’18, pp. 3839–3848, 2018.

Kartik Sharma, Yeon-Chang Lee, Sivagami Nambi, Aditya Salian, Shlok Shah, Sang-Wook Kim, and Srijan Kumar. A survey of graph neural networks for social recommender systems. ACM Computing Surveys, 56(10):1–34, 2024.

Li Sun, Zhongbao Zhang, Junda Ye, Hao Peng, Jiawei Zhang, Sen Su, and Philip S. Yu. A self- supervised mixed-curvature graph neural network. In Proceedings of the 36th AAAI, pp. 4146– 4155, 2022a.

Li Sun, Zhenhao Huang, Hua Wu, Junda Ye, Hao Peng, Zhengtao Yu, and Philip S. Yu. Deepricci:

Self-supervised graph structure-feature co-refinement for alleviating over-squashing. In Proceedings of the 23rd ICDM, pp. 558–567, 2023a.

Li Sun, Feiyang Wang, Junda Ye, Hao Peng, and Philip S. Yu. Congregate: contrastive graph clustering in curvature spaces. In Proceedings of the 32nd IJCAI, pp. 2296–2305, 2023b.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Li Sun, Zhenhao Huang, Hao Peng, Yujie Wang, Chunyang Liu, and Philip S. Yu. Lsenet: Lorentz structural entropy neural network for deep graph clustering. In Proceedings of the 41st ICML, pp. 47078–47104, 2024a.

Li Sun, Zhenhao Huang, Qiqi Wan, Hao Peng, and Philip S. Yu. Spiking graph neural network on riemannian manifolds. In Advances in NeurIPS, 2024b.

Li Sun, Zhenhao Huang, Zixi Wang, Feiyang Wang, Hao Peng, and Philip S. Yu. Motif-aware riemannian graph neural network with generative-contrastive learning. In Proceedings of the 38th AAAI, pp. 9044–9052, 2024c.

Li Sun, Zhenhao Huang, Ming Zhang, and Philip S. Yu. Deeper with riemannian geometry: Over- coming oversmoothing and oversquashing for graph foundation models. In Advances in NeurIPS, 2025a.

Li Sun, Zhenhao Huang, Suyang Zhou, Qiqi Wan, Hao Peng, and Philip S. Yu. Riemanngfm: Learning a graph foundation model from riemannian geometry. In Proceedings of the ACM on Web Conference 2025 (WWW), pp. 1154–1165, 2025b.

Li Sun, Zhenhao Huang, Yujie Wang, Hongbo Lv, Chuanyang Liu, Hao Peng, and Philip S. Yu.

Asil: Augmented structural information learning for deep graph clustering in hyperbolic space. IEEE Transactions on Pattern Analysis and Machine Intelligence, pp. 1–18, 2026a.

Li Sun, Ming Zhang, Wenxin Jin, Zhongtian Sun, Zhenhao Huang, Hao Peng, Sen Su, and Philip S.

Yu. Heterophily-agnostic hypergraph neural networks with riemannian local exchanger. In Proceedings of the ACM Web Conference (WWW), 2026b.

Mingchen Sun, Kaixiong Zhou, Xin He, Ying Wang, and Xin Wang. Gppt: Graph pre-training and prompt tuning to generalize graph neural networks. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD), KDD ’22, pp. 1717–1727, 2022b.

Yifei Sun, Qi Zhu, Yang Yang, Chunping Wang, Tianyu Fan, Jiajun Zhu, and Lei Chen. Fine-tuning graph neural networks by preserving graph generative patterns. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), volume 38, pp. 9053–9061, 2024d.

Maciej Sypetkowski, Frederik Wenkel, Farimah Poursafaei, Nia Dickson, Karush Suri, Philip Frad- kin, and Dominique Beaini. On the scalability of GNNs for molecular graphs. In Advances in Neural Information Processing Systems 38 (NeurIPS), 2024.

Jiabin Tang, Yuhao Yang, Wei Wei, Lei Shi, Lixin Su, Suqi Cheng, Dawei Yin, and Chao Huang.

Graphgpt: Graph instruction tuning for large language models. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR), pp. 491–500, 2024.

Eliot Tron, Rita Fioresi, Nicolas Couellan, and St´ephane Puechmorel. Cartan moving frames and the data manifolds. CoRR, abs/2409.12057, 2024.

Laurens van der Maaten and Geoffrey Hinton. Visualizing data using t-sne. Journal of Machine

Learning Research, 9(86):2579–2605, 2008.

Petar Veliˇckovi´c, William Fedus, William L. Hamilton, Pietro Li`o, Yoshua Bengio, and R Devon

Hjelm. Deep graph infomax. In Proceedings of the 7th International Conference on Learning Representations (ICLR), 2019.

Shuo Wang, Bokui Wang, Zhixiang Shen, Boyan Deng, and Zhao Kang. Multi-domain graph foun- dation models: Robust knowledge transfer via topology alignment. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025a.

Yuyang Wang, Zijie Li, and Amir Barati Farimani. Graph neural networks for molecules. In Machine learning in molecular sciences, pp. 21–66. Springer, 2023.

Zehong Wang, Zheyuan Zhang, Nitesh Chawla, Chuxu Zhang, and Yanfang Ye. Gft: Graph founda- tion model with transferable tree vocabulary. Advances in Neural Information Processing Systems (NeurIPS), 37:107403–107443, 2024.

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

Zehong Wang, Zheyuan Liu, Tianyi Ma, Jiazheng Li, Zheyuan Zhang, Xingbo Fu, Yiyang Li,

Zhengqing Yuan, Wei Song, Yijun Ma, et al. Graph foundation models: A comprehensive survey. arXiv preprint arXiv:2505.15116, 2025b.

Zehong Wang, Zheyuan Zhang, Tianyi Ma, Nitesh V Chawla, Chuxu Zhang, and Yanfang Ye. To- wards graph foundation models: Learning generalities across graphs via task-trees. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025c.

Grady Wright and Bengt Fornberg. Scattered node compact finite difference-type formulas gener- ated from radial basis functions. In Computational Methods, pp. 1391–1395, Dordrecht, 2006.

Bin Wu, Yihang Wang, Yuanhao Zeng, Jiawei Liu, Jiashu Zhao, Cheng Yang, Yawen Li, Long Xia,

Dawei Yin, and Chuan Shi. Graph foundation models for recommendation: A comprehensive survey, 2025.

Jun Xia, Chengshuai Zhao, Bozhen Hu, Zhangyang Gao, Cheng Tan, Yue Liu, Siyuan Li, and Stan Z.

Li. Mole-BERT: Rethinking pre-training graph neural networks for molecules. In Proceedings of the 11th International Conference on Learning Representations (ICLR), 2023.

Lianghao Xia, Ben Kao, and Chao Huang. Opengraph: Towards open graph foundation models. In

Findings of Empirical Methods in Natural Language Processing (EMNLP), pp. 2365–2379, 2024.

Bo Xiong, Shichao Zhu, Nico Potyka, Shirui Pan, Chuan Zhou, and Steffen Staab. Pseudoriemannian graph convolutional networks. In Advances in neural information processing systems (NeurIPS), 2022.

Keyulu Xu, Weihua Hu, Jure Leskovec, and Stefanie Jegelka. How powerful are graph neural networks? In Proceedings of the 7th International Conference on Learning Representations (ICLR), 2019.

Menglin Yang, Min Zhou, Tong Zhang, Jiahong Liu, Zhihao Li, Lujia Pan, Hui Xiong, and Irwin

King. Hyperbolic graph neural networks: A review of methods and applications, 2025a.

Zhe-Rui Yang, Jindong Han, Chang-Dong Wang, and Hao Liu. Graphlora: Structure-aware con- trastive low-rank adaptation for cross-graph transfer learning. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1, pp. 1785–1796, 2025b.

Xingtong Yu, Yuan Fang, Zemin Liu, and Xinming Zhang. Hgprompt: bridging homogeneous and heterogeneous graphs for few-shot prompt learning. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), 2024a.

Xingtong Yu, Chang Zhou, Yuan Fang, and Xinming Zhang. Multigprompt for multi-task pre- training and prompting on graphs. In Proceedings of the 33rd ACM Web Conference (WWW), pp. 515–526, 2024b. ISBN 9798400701719.

Xingtong Yu, Chang Zhou, Yuan Fang, and Xinming Zhang. Text-free multi-domain graph pre- training: Toward graph foundation models, 2024c.

Xingtong Yu, Zechuan Gong, Chang Zhou, Yuan Fang, and Hui Zhang. Samgpt: Text-free graph foundation model for multi-domain pre-training and cross-domain adaptation. In Proceedings of the ACM on Web Conference 2025 (WWW), pp. 1142–1153, 2025a.

Xingtong Yu, Jie Zhang, Yuan Fang, and Renhe Jiang. Non-homophilic graph pre-training and prompt learning. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1 (KDD), pp. 1844–1854, 2025b.

Haonan Yuan, Qingyun Sun, Junhua Shi, Xingcheng Fu, Bryan Hooi, Jianxin Li, and Philip S.

Yu. How much can transfer? BRIDGE: Bounded multi-domain graph foundation model with generalization guarantees. In Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025.

Bohang Zhang, Jingchu Gai, Yiheng Du, Qiwei Ye, Di He, and Liwei Wang. Beyond weisfeiler- lehman: A quantitative framework for GNN expressiveness. In Proceedings of the 12th International Conference on Learning Representations, 2024.

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

Haihong Zhao, Aochuan Chen, Xiangguo Sun, Hong Cheng, and Jia Li. All in one and one for all: A simple yet effective method towards cross-domain graph pretraining. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 4443–4454, 2024.

Zihao Zhao, Xinlong Zhai, Jinyu Yang, and Chuan Shi. Towards text-free graph foundation models:

Rethinking multi-domain graph contrastive learning. In arXiv, 2025.

Jie Zhou, Ganqu Cui, Shengding Hu, Zhengyan Zhang, Cheng Yang, Zhiyuan Liu, Lifeng Wang,

Changcheng Li, and Maosong Sun. Graph neural networks: A review of methods and applications. AI Open, 1:57–81, 2020.

Xi Zhu, Haochen Xue, Ziwei Zhao, Wujiang Xu, Jingyuan Huang, Minghao Guo, Qifan Wang,

Kaixiong Zhou, and Yongfeng Zhang. Llm as gnn: Graph vocabulary learning for text-attributed graph foundation models. arXiv preprint arXiv:2503.03313, 2025.

<!-- Page 17 -->

Published as a conference paper at ICLR 2026

APPENDIX: TABLE OF CONTENT

A Notations................................................... 19

B Proofs..................................................... 20

B.1 Proof of Theorem 4.3........................................ 20

B.2 Proof of Theorem 4.5........................................ 21

B.3 Proof of Theorem 4.6........................................ 22

B.4 Proof of Theorem 4.8 and Clarification............................. 24

B.5 Proof of Theorem 4.9........................................ 24

B.6 Proof of Theorem 4.11....................................... 25

C Background: Differential Geometry on Riemannian Manifolds.............. 26

C.1 Riemannian Manifold: The Continuous Setting....................... 26

C.2 Levi-Civita Connection and Parallel Transport........................ 26

C.3 Curvature and Holonomy...................................... 26

C.4 Ricci Curvature and Volume Change.............................. 26

C.5 Smoothness and Harmonic Functions.............................. 27

C.6 Cartan’s Method of Moving Frame............................... 27

C.7 Connection to Our Framework.................................. 27

D Algorithms.................................................. 29

D.1 Multi-Domain Pre-training..................................... 29

D.2 Complexity Analysis......................................... 29

D.3 Complexity Comparison with Other GFMs.......................... 29

E Related Work................................................ 30

E.1 Graph Foundation Models..................................... 30

E.2 Multi-domain Graph Pre-training................................. 30

E.3 Graph Fine-tuning and Prompt Learning............................ 31

E.4 Riemannian Graph Representation Learning......................... 31

F Empirical Details.............................................. 31

F.1 Dataset Description.......................................... 31

F.2 Baselines................................................ 32

F.3 Implementation notes........................................ 33

G Additional Results............................................. 34

G.1 Supplementary Results....................................... 34

G.2 Comprehensive Ablation Study.................................. 34

G.3 Hyperparameter Sensitivity Analysis.............................. 35

G.4 Results on Heterophilic Graphs.................................. 36

G.5 Visualization of Manifold Gluing................................ 36

H Reproducibility Statement....................................... 40

I Ethics Statement.............................................. 41

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

J Declaration of LLM Usage....................................... 41

K Broader Impact............................................... 41

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

A NOTATIONS

**Table 2.** Notation and Description

Notation Description

M A smooth manifold G A Riemannian metric tensor p A point in M TpM The tangent space of point p on M |G(p)| The volume element at p (U, x1,..., xM) A coordinate chart of tangent space TpM { ∂

∂x1,..., ∂ ∂xM }, {∂i} The standard frame of T M Ric(X, Y) Ricci curvature for vector fields X, Y G = (V, E) A graph with node set V and edge set E X ∈R|V|×F A feature matrix with node set V Gt The graph of target domain Dt

G = {G1, G2, · · ·, GK} A collection of K graphs from L domains D D = {D1, D2, · · ·, DL} L domains fΘ(GNN(·)) A pretrained model on the graph dataset G with an encoder GNN(·) {Θ⋆ f, Θ⋆

GNN} The pre-training parameters fGNN: G →Rd A differentiable encoder from manifold G into the Euclidean space wm The set of tangent vectors of graph G Dvf The directional derivative G H(C) The holonomy map of cycle C EDir[g] The graph Dirichlet energy of function g Si(Vi, Ei) The h-hop neighborhood centered at vi with node set Vi and edge set Ei within this subgraph ˆGm = (ˆVm, ˆEm) The augmented graph P[M, d] The Adaptive Orthogonal Frame Ui A neighborhood around z(i)

W (i) The basis of Tz(i)Ui generated from AFB Gi(u, v) The local Riemannian metric defined on Ui SM×M

++ The set of positive-definite matrix S = {S1,..., SK} The source graph datasets (zSk, log GSk) the Riemannian prototypes for each source graph dataset Lproto(G) The prototype-level contrastive loss P (i,j) The tangent edge translation A The set of all triangles Aijk = ((vi, vj), (vj, vk)) Lhol(G) The holonomy loss r(z(i), z(j)) The overall sign of the Ricci curvature along the geodesic γ(t) between zi and zj LCurv(G) The curvature loss regularizing the change of curvature by controlling the volume change ratio GT = (VT, ET) An unseen graph W adapt, Gadapt The adaptive tangent vectors and adaptive metric Q The prompt matrix log Galign The aligned log-metric to give a K-dimensional weighted vector Ladap The adaptation loss λ The balance coefficient of task loss and gluing loss ∆H Holonomy disagreement ∆C Curvature disagreement

<!-- Page 20 -->

Published as a conference paper at ICLR 2026

B PROOFS

B.1 PROOF OF THEOREM 4.3

Theorem 4.3 (Upper bound of Tangent Vector Length) Given a connected G with N nodes, A, L the adjacency matrix and Laplacian of G, and P the feature matrix of perturbation nodes. Apply (k, M)-sparse perturbation to G, suppose kM

N = ε, where ε > 0 is small, and added edge weights satisfy P l h(vi, pl) = 1. Then,

∥wp m∥≤(1 + ε)∥P ∥ holds, where wp m is the component of wm determined by perturbation.

Proof. We denote the weighted matrix H ∈RN×M that consists of h(vi, pl), the row summation rH = H1M. Then, the perturbed adjacency matrix ˆ A is

ˆ A =

A H H⊤ IM

∈R(N+M)×(N+M).

The perturbed Laplacian is

ˆL =

L + diag(rH) −H −H⊤ IM

∈R(N+M)×(N+M). (13)

Let the d-dimensional graph signal F ∈R(N+M)×d in heat diffusion on a perturbed graph ˆG be

F (t) = exp(−t ˆL)F (0), t > 0, (14)

F (0) =

X

P

∈R(N+M)×d. (15)

By the linearity of the heat equation, we can divide F (t) into two parts:

F (t) = exp(−t ˆL)

X

0

+ exp(−t ˆL)

0 P

. (16)

We denote

Fbase(t) = exp(−t ˆL)

X

0

, (17)

Fpert(t) = exp(−t ˆL)

0 P

. (18)

We are only concerned about Fpert(t) since it reflects how perturbation P affects other nodes. Observe from the construction of ˆL, the affected nodes are non-zero elements in rH. Let S = supp rH ⊂{1,..., N}, that S:= |S| ≤kM. We can extract the corresponding part of

ˆL:

Llocal =

LS −HS −H⊤

S IM

∈R(S+M)×(S+M)), (19)

where

LS = (L + diag(rH))[S,S],

HS = H[S,:].

Then we have

Fpert(t) =

Fpert,N(t) Fpert,M(t)

=





S exp(−tLlocal)

0S P

[1:S]

exp(−tLlocal)

0S P

[S+1:S+M]



, (20)

<!-- Page 21 -->

Published as a conference paper at ICLR 2026 where S ∈RN×S is an index projection matrix such that (S)[i, j] = 1 if i = S[j]. To simplify the notation, let

K(t) = exp(−tLlocal) =

KSS(t) KSM(t) KMS(t) KMM(t)

∈R(S+M)×(S+M)). (21)

We can find

Fpert,N(t) = SKSM(t)P, (22) Fpert,M(t) = KMM(t)P. (23)

As return to Eq. (16), we obtain

FN(t) = Fbase,N(t) + SKSM(t)P, (24) FM(t) = Fbase,M(t) + KMM(t)P, (25)

where Fbase,N(t) = Fbase(t)[:N], Fbase,M(t) = Fbase(t)[N+1:N+M].

We simply consider the global mean pooling operation that we obtain z(t) = 1

N 1⊤

NFN(t) ∈Rd, (26)

wm(t) = fm(t) −z(t) ∈Rd, (27)

where fm(t) = FM(t)[m], the m-th row of FM.

Similarly, we can still divide wm(t) into two parts as wm(t) = f p m(t) −zp(t) + (term affects by X), (28)

where f p m(t) is the m-th row of KMM(t)P, and zp(t) = 1

N 1⊤

NSKSM(t)P = 1

N (1⊤

S KSM(t))P. (29)

Let a(t) = 1 N K⊤

SM(t)1S ∈RM, then we have zp(t) = a⊤(t)P. We denote wp m(t) = f p m(t) − zp(t), then wp m(t) = [KMM(t)P ][m] −1

N a⊤(t)P =

KMM(t)[m,:] −a⊤(t)

P. (30)

Let b(t) = KMM(t)[m,:] −a(t), we have wp m(t) = b⊤(t)P.

Since kM

N = ε, S ≤kM = εN, we obtain

∥a(t)∥= ∥1

N (1⊤

S KSM(t))∥≤S

N max i,j |KSM(t)[i,j]| ≤S

N ≤ε, (31)

which means

∥wp m(t)∥≤(∥KMM(t)[m,:]∥+ ∥a(t)∥)∥P ∥≤(1 + ε)∥P ∥, (32)

since each element is finite, and the diagonal elements of the heat kernel matrix are near 1 while the other elements are less than 1. Then, we complete the proof.

B.2 PROOF OF THEOREM 4.5

Theorem 4.5 (Edge Tangent Translation as Isometry) The tangent edge translation in Definition 4.4 is the optimal solution of minP ∈GL(M)

P ⊤GjP −Gi

2

F, (33)

where GL denotes the general linear group, such that Gj(P (i,j)u, P (i,j)v) = Gi(u, v), which induces an isometry ϕ(i,j) between ∂Ui and ∂Uj.

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

Proof. We prove that the tangent edge translation P (i,j) = G−1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j uniquely minimizes ∥P ⊤GjP −Gi∥2

F over P ∈GL(M) and induces an isometry.

Let Q = G1/2 j P. Then P ⊤GjP = Q⊤Q, and the objective becomes:

min Q∈GL(M) ∥Q⊤Q −Gi∥2

F. (34)

The minimum is achieved when Q⊤Q = Gi, since the Frobenius norm is strictly convex over SPD matrices. Thus, Q = G1/2 i R for orthogonal R, and minimal norm occurs at R = I, giving Q∗= G1/2 i.

From Q = G1/2 j P, we get candidate P0 = G−1/2 j G1/2 i. However, this is not symmetric in Gi, Gj unless they commute. To ensure geometric consistency and symmetry, we instead use the metric geometric mean:

P (i,j) = G−1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j. (35)

Then, we compute

P (i,j)⊤GjP (i,j) = G−1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j · Gj · G−1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j

(36)

= G−1/2 j

G1/2 j GiG1/2 j

G−1/2 j = Gi. (37)

Thus, Gj(P (i,j)u, P (i,j)v) = u⊤P (i,j)⊤GjP (i,j)v = u⊤Giv = Gi(u, v), so P (i,j) is an isometry.

All isometric maps satisfy P ⊤GjP = Gi, and form the set {P (i,j)R | R⊤GiR = Gi}. The Frobenius norm ∥P ∥2

F = Tr(P ⊤P) is minimized when GjP is symmetric. Then, we have

GjP (i,j) = G1/2 j

G1/2 j GiG1/2 j

1/2

G−1/2 j. (38)

Hence, P (i,j) is the minimum-norm isometry, and thus the global minimizer of the original Frobenius problem (since the constraint is active and satisfied exactly).

Since P (i,j): Tz(i)Ui →Tz(j)Uj is a linear isometry, and assuming smooth compatibility of charts near z(i), z(j), we can lift P (i,j) via the exponential map (or local parametrization) to a local diffeomorphism ϕ(i,j): ∂Ui →∂Uj such that ϕ(i,j)

∗,z(i) = P (i,j), which is the differential of a diffeo- morphism and preserves metric. Hence ϕ(i,j) is a isometry.

B.3 PROOF OF THEOREM 4.6

Theorem 4.6 Existence of Global Metric) Let ({Gi}N i=1, {P (i,j)}(i,j)∈E) be local metrics and tangent edge translations. There exists a unique global continuous metric G on (S ϕ)N i=1Ui such that G|Ui = Gi for all i.

Proof. We aim to construct a global continuous Riemannian metric G on the space F = SN i=1 Ui, where each Ui is an open subset of Rd, and the overlaps Ui ∩Uj are non-empty for (i, j) ∈E. By assumption, we have a local Riemannian metric Gi on each Ui, and tangent edge translations P (i,j): Tz(i)Ui →Tz(j)Uj satisfying

P (i,j)⊤GjP (i,j) = Gi, (39)

which ensures that P (i,j) is an isometry between (Tz(i)Ui, Gi) and (Tz(j)Uj, Gj).

Let us define a topological space F = SN i=1 Ui, with topology induced by the Euclidean topology on each Ui. For each pair (i, j) ∈E, let ϕ(i,j): ∂Ui →∂Uj be a diffeomorphism whose differential

<!-- Page 23 -->

Published as a conference paper at ICLR 2026 at the shared boundary point z(i) is precisely P (i,j). Since P (i,j) is an isometry, it preserves inner products, so ϕ(i,j) is a local isometry near z(i).

Now, we consider that, let M1 = Ui, M2 = Uj, N1 = ∂Ui, N2 = ∂Uj, and ϕ: N1 →N2 be the diffeomorphism induced by P (i,j). Now we introduce the following lemma to complete the proof.

Lemma B.1 (Gluing Manifolds via Boundary Isometries Hirsch (1976)). Let M1 and M2 be smooth M-dimensional manifolds with boundary, and let N1 ⊂∂M1, N2 ⊂∂M2 be closed, smoothly embedded (M −1)-dimensional submanifold of their respective boundaries. Suppose ϕ: N1 →N2 is a diffeomorphism such that its differential ϕ∗,x: TxN1 →Tϕ(x)N2 extends to an isometry

Px: TxM1 →Tϕ(x)M2 (40)

between the Riemannian metrics G1 on M1 and G2 on M2, i.e.,

P ⊤ x G2(ϕ(x))Px = G1(x), ∀x ∈N1. (41)

Then, the topological space M1 ∪ϕ M2 obtained by identifying N1 with N2 via ϕ admits a unique smooth structure such that:

1. The inclusions M1,→M1 ∪ϕ M2 and M2,→M1 ∪ϕ M2 are smooth embeddings;

## 2 The Riemannian metrics G1 and G2 extend to a continuous

Riemannian metric G on M1 ∪ϕ M2.

Moreover, this smooth structure is unique up to a diffeomorphism that fixes N1 ≃N2 point-wise.

By the Lemma B.1, there exists a smooth structure on the glued space M1 ∪ϕ M2 that arises from identifying N1 with N2 via ϕ. Moreover, this smooth structure is unique up to a diffeomorphism fixing N1 ≃N2.

Applying this construction iteratively over all edges (i, j) ∈E, we can glue all charts Ui together along their boundaries using the maps ϕ(i,j), resulting in a globally defined topological space F equipped with a smooth structure.

On each Ui, we already have a Riemannian metric Gi. We now define a global metric G on M by setting G|Ui = Gi. To ensure that G is well-defined on overlaps Ui ∩Uj, we must verify that the values agree under coordinate changes.

Let u ∈Tz(F) for z ∈Ui ∩Uj. In the chart Ui, u is represented as ui ∈Tz(i)Ui, and in Uj, as uj = P (i,j)ui ∈Tz(j)Uj. Then:

Gi(ui, ui) = u⊤ i Giui, Gj(uj, uj) = u⊤ j Gjuj = (P (i,j)ui)⊤Gj(P (i,j)ui). (42)

But by the isometry condition:

P (i,j)⊤GjP (i,j) = Gi ⇒u⊤ i Giui = u⊤ i P (i,j)⊤GjP (i,j)ui = u⊤ j Gjuj. (43)

Thus, Gi(ui, ui) = Gj(uj, uj), so the metric value is independent of the chart. Hence, G is well-defined on M.

Since each Gi is continuous on Ui, and the transition maps P (i,j) are smooth, the metric G is continuous across overlaps.

Uniqueness follows from the fact that any other metric ˜G agreeing with Gi on each Ui must coincide with G on overlaps due to the isometry constraint. Thus, G is the unique continuous metric extending Gi consistently.

Therefore, under the given assumptions, there exists a unique continuous Riemannian metric G on SN i=1 Ui such that G|Ui = Gi for all i, completing the proof.

<!-- Page 24 -->

Published as a conference paper at ICLR 2026

B.4 PROOF OF THEOREM 4.8 AND CLARIFICATION

Theorem 4.8 (Triangle Triviality) If every edge belongs to at least one triangle, and H(T) = I for all triangular cycles T in G, then H(C) = I for all cycles C ∈Z1(G).

Proof. Under the assumption that every edge lies in at least one triangle, the cycle space Z1(G) is generated by triangular cycles (see, e.g., the simplicial/cellular homology discussion in (Hatcher, 2002, Section 2.1), where 1-cycles are generated by boundaries of 2-simplices — here, triangles). Since the holonomy map H: Z1(G) →GL(M) is multiplicative and trivial on generators (i.e., H(T) = I for all triangles T), it follows that H(C) = I for all C ∈Z1(G).

Note that every edge belonging to at least one triangle is not the assumption of Theorem 4.8. This theorem states that, if every edge belongs to at least one triangle, triangles are already sufficient to construct the coherent manifold described in this work. It means that there is no need for exploring any higher-order motifs, but the triangle coverage is not a necessary condition of manifold gluing.

We clarify that GraphGlue does not need to add synthetic motifs. Since GraphGlue aims to approximate a smooth manifold, the closed triple paths (strict triangles) benefit the approximation process. As we consider that sample closed triangle paths may be impossible in large-scale graphs or tree-like graphs, the triangle holonomy regularization gives a computationally efficient way to approximate a “perfect gluing.” In practice, we only sample two adjacent edges to approximate strict triangles (at the end of Appendix D.1), and the computation of Lcurv only relies on two adjacent edges.

B.5 PROOF OF THEOREM 4.9

Theorem 4.9 (Ricci Curvature Estimation) Given a graph G = (V, E) and an edge (i, j) ∈E, let z(i), z(j) ∈M be the corresponding embedded points, and let γ: [0, 1] →M be the unit-speed geodesic connecting them, i.e., γ(0) = z(i), γ(1) = z(j). The sign of the Ricci curvature along ˙γ can be estimated by the ratio of metric determinants:

r(z(i), z(j)):= det Gi det Gj

≈1 −1

3Ric(˙γ). (44)

Proof. We work in Gaussian normal coordinates centered at z(i) = γ(0), aligned with the geodesic γ(t). In these coordinates, the element of metric tensor gij(t) = gij(γ(t)) admits the following Taylor expansion near t = 0 (see, Petersen (2016)):

gij(t) = δij −1

3Rikjl(z(i)) ˙γk ˙γl t2 + O(t3), (45)

where Rikjl denotes the components of the Riemann curvature tensor at z(i), and ˙γ = ˙γ(0) is the initial tangent vector.

Let g(t) = det(gij(t)). Since g(0) = det(δij) = 1, we compute the expansion of g(t) using the Jacobi formula for the derivative of a determinant:

d dt log g(t) = gij(t) d dtgij(t). (46)

At t = 0, gij(0) = δij and d dtgij(0) = 0 (since first-order terms vanish in normal coordinates). Differentiating again:

d2 dt2 log g(t)

t=0 = δij d2 dt2 gij(t)

t=0 = δij

−2

3Rikjl ˙γk ˙γl

= −2

3Rkl ˙γk ˙γl = −2 3Ric(˙γ). (47)

Thus, expanding log g(t) to second order:

log g(t) = −1

3Ric(˙γ) t2 + O(t3), (48)

and exponentiating:

g(t) = exp

−1

3Ric(˙γ) t2 + O(t3)

= 1 −1

3Ric(˙γ) t2 + O(t3). (49)

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

Now, evaluate at t = 1 (i.e., at z(j) = γ(1)), assuming the higher-order terms remain negligible (which holds if either the curvature is bounded and the edge length is small, or if we consider the leading-order behavior):

det Gj = g(1) ≈1 −1

3Ric(˙γ), det Gi = g(0) = 1. (50)

Therefore, the ratio satisfies:

r(z(i), z(j)) = det Gi det Gj

≈ 1 1 −1 3Ric(˙γ) ≈1 + 1 3Ric(˙γ) + O(Ric2), (51)

where the last step uses (1 −x)−1 ≈1 + x for small x. However, since we are only interested in the sign of Ric(˙γ), and under the assumption that

1

3Ric(˙γ) ≪1, we may directly approximate:

det Gi det Gj

≈1 −1

3Ric(˙γ), (52)

by matching leading-order terms in the reciprocal expansion (equivalently, approximating det Gj ≈ 1−1 3Ric implies det Gi/ det Gj ≈1+ 1 3Ric, but since det Gi = 1, the direct expansion of det Gj gives the sign relation).

Thus, we conclude:

• If Ric(˙γ) > 0, then det Gj < det Gi ⇒r(z(i), z(j)) < 1.

• If Ric(˙γ) < 0, then det Gj > det Gi ⇒r(z(i), z(j)) > 1.

• If Ric(˙γ) = 0, then det Gj ≈det Gi ⇒r(z(i), z(j)) ≈1.

This establishes the correspondence between the sign of Ricci curvature and the metric volume ratio, as claimed.

B.6 PROOF OF THEOREM 4.11

Theorem 4.11 (Glue to a Global Riemannian Manifold) For the set of all graph data G, if G is log-determinant ∞-order smooth, and P is trivial with induced metric-preserving diffeomorphism ϕ, then (F, G, P) glues to a smooth Riemannian manifold (F, G), where F:= (S ϕ)N i=1Ui.

Proof. We construct the global manifold structure in three steps, leveraging the established components:

(1) Trivial holonomy ⇒path-independent parallel transport. By Theorem 4.8 and Definition 4.7, the triviality of P on all cycles implies that the tangent edge translations P (i,j) define a flat connection on the graph. Consequently, the induced diffeomorphisms ϕ(i,j) (from Theorem 4.5) are compatible across higher-order overlaps: for any two paths from Ui to Uj, the composed gluing maps agree. This ensures the cocycle condition for manifold gluing.

(2) Global metric existence. By Theorem 4.6 (Existence of Global Metric), the pairwise isometric identifications ϕ(i,j) — now globally consistent due to trivial holonomy — allow us to glue the charts {Ui} into a topological space F = S ϕ Ui equipped with a unique continuous Riemannian metric G such that G|Ui = Gi.

(3) Smoothness from log-det ∞-order smoothness. By Definition 4.10, the scalar field gi =

1 2 log det Gi minimizes ∥Lkg∥2 for all k ≥1, which implies g is in the kernel of all powers of L — i.e., g is infinitely smooth over the graph. Since Lkg = 0 for all k only if g is constant on connected components (under mild graph connectivity), and since det Gi = exp(2gi), it follows that the metric determinants vary smoothly (in fact, constantly, if the graph is connected). Combined with the smoothness of the transition maps ϕ(i,j) (which are isometries, hence C∞), this ensures that the metric tensor G is smooth in overlapping charts. Thus, (F, G) is a smooth Riemannian manifold.

Therefore, the triple (F, G, P), under the given conditions, glues consistently to form the smooth Riemannian manifold (F, G).

<!-- Page 26 -->

Published as a conference paper at ICLR 2026

C BACKGROUND: DIFFERENTIAL GEOMETRY ON RIEMANNIAN MANIFOLDS

This appendix provides the necessary background on continuous Riemannian geometry, which forms the theoretical foundation for our claim that MERGE learns a smooth, intrinsic manifold in the latent space. While our implementation operates on discrete graphs and neural networks, we argue that the learned structure approximates a true, continuous Riemannian manifold due to the smoothness of the GNN encoder. We emphasize concepts relevant to Sections 5 and 6 of the main text.

C.1 RIEMANNIAN MANIFOLD: THE CONTINUOUS SETTING

A Riemannian manifold (M, g) is a smooth (typically C∞) topological manifold M of dimension M, endowed with a Riemannian metric tensor g. At each point p ∈M, the metric gp is a symmetric, positive-definite bilinear form defined on the tangent space TpM:

gp: TpM × TpM →R. (53)

The metric gp allows us to compute lengths of tangent vectors, angles between them, and volumes of regions on M. In local coordinates (x1,..., xM) around p, the metric is represented by a matrix G(p) = [gij(p)], where gij(p) = gp(∂i, ∂j), and {∂i = ∂ ∂xi } is the coordinate basis of TpM.

The volume element at p is given by dVp = p det G(p) dx1 ∧· · · ∧dxM. The scalar field f(p) = 1 2 log det G(p) is called the logarithmic volume density. A manifold is said to be Ck-smooth if the components gij are Ck-differentiable functions of the coordinates.

C.2 LEVI-CIVITA CONNECTION AND PARALLEL TRANSPORT

A connection ∇on M defines how to differentiate vector fields along curves, enabling the notion of parallel transport. The unique connection compatible with the metric g and torsion-free is called the Levi-Civita connection. It is characterized by two properties:

## 1. Metric Compatibility: For any vector fields X, Y, Z on M,

X⟨Y, Z⟩= ⟨∇XY, Z⟩+ ⟨Y, ∇XZ⟩. (54)

This means parallel transport preserves inner products (and thus lengths and angles). 2. Torsion-Free: ∇XY −∇Y X = [X, Y ], where [·, ·] is the Lie bracket.

Given a smooth curve γ(t): [a, b] →M, a vector field V (t) along γ is parallel transported if ∇˙γ(t)V (t) = 0. The parallel transport map PTγ: Tγ(a)M →Tγ(b)M is the linear isometry that maps a vector at the start of the curve to its parallel-transported version at the end.

C.3 CURVATURE AND HOLONOMY

The failure of parallel transport to be path-independent is measured by the curvature tensor R, a (1, 3)-tensor defined as:

R(X, Y)Z = ∇X∇Y Z −∇Y ∇XZ −∇[X,Y ]Z. (55)

If R ≡0 everywhere, the manifold is flat, and parallel transport depends only on the endpoints, not the path.

For a closed loop (cycle) C starting and ending at p, the composition of parallel transports along C yields a linear transformation H(C): TpM →TpM, called the holonomy of C. If H(C) = id for all loops C, then the curvature vanishes (R ≡0), and the manifold is flat. Conversely, if R̸ ≡0, then H(C)̸ = id for some non-contractible loop.

C.4 RICCI CURVATURE AND VOLUME CHANGE

The Ricci curvature Ric is a (0, 2)-tensor obtained by contracting the curvature tensor: Ric(X, Y) = PM i=1 R(ei, X, Y, ei), where {ei} is an orthonormal basis.

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

On a geodesic γ(t) with unit speed ˙γ(t), the Ricci curvature governs the rate of change of the volume element along the geodesic. In Gaussian normal coordinates centered on γ(0), the determinant of the metric satisfies the following expansion for small t:

det G(γ(t)) = 1 −1

3Ric(˙γ(0))t2 + O(t3). (56)

Thus, the ratio of volume elements between two nearby points p = γ(0) and q = γ(t) is approximately:

p det G(q) p det G(p)

≈1 −1

6Ric(˙γ(0))t2. (57)

This implies:

1. Ric > 0: Volume shrinks along the geodesic (elliptic/positive curvature region).

2. Ric < 0: Volume expands along the geodesic (hyperbolic/negative curvature region).

3. Ric = 0: Volume is locally preserved (flat region). This relationship underpins our use of the metric volume ratio det Gi/ det Gj as a proxy for estimating Ricci curvature along graph edges.

C.5 SMOOTHNESS AND HARMONIC FUNCTIONS

A scalar function f: M →R is harmonic if it satisfies ∆f = 0, where ∆is the Laplace- Beltrami operator. On a compact manifold without boundary, harmonic functions are constant. More importantly, solutions to ∆f = 0 are infinitely differentiable (C∞) by elliptic regularity theory.

In the context of our framework, minimizing the Dirichlet energy P

(i,j)∈E(fi −fj)2 over the graph Gdata is a discrete approximation to minimizing

R

M ∥∇f∥2dV. Minimizing this energy drives f = 1

2 log det G toward a harmonic function on the underlying continuous manifold. By elliptic regularity, this ensures that the log-volume density f is smooth, implying the metric G has continuous first derivatives (C1). This justifies our assumption that the learned manifold is geometrically well-behaved, free from pathological singularities.

C.6 CARTAN’S METHOD OF MOVING FRAME

The renowned Cartan’s Method Tron et al. (2024) offers a principled way to explore the geometry of Riemannian manifolds, establishing a profound connection between differential calculus and geometry. Specifically, ´Elie Cartan introduces the concept of frame to characterize the local geometry, which is then extended to a global manifold through “ moving frame”. Although ´Elie Cartan laid the mathematical principle, its deep learning theory and methodology remain largely unexplored. Our work seeks to bridge this gap.

C.7 CONNECTION TO OUR FRAMEWORK

Our work does not assume a pre-existing manifold. Instead, we posit that the embedding space Rd induced by a smooth GNN fGNN contains a low-dimensional submanifold M, whose intrinsic geometry encodes the generalizable rules of graph data. The Adaptive Frame Bank (AFB) samples the local tangent spaces TpM. The optimal isometric alignment (Theorem 5.6) approximates the Levi-Civita connection’s action between sampled points. The cycle-consistency loss enforces trivial holonomy, mimicking flatness. The log-determinant smoothness regularization drives the volume element toward harmonicity. Together, these components constitute a learning procedure that constructs a continuous, smooth, nearly-flat Riemannian manifold M within the latent space of a neural network, using only discrete graph samples and their embeddings. The graph structure Gdata serves as a sampling mesh, not the domain of geometry.

<!-- Page 28 -->

Published as a conference paper at ICLR 2026

## Algorithm

## 1 Training

Procedure for GRAPHGLUE

Require: Epoch index e, optimizer, datasets Dmix, Dsingle, Dmulti with data name mappings. Ensure: Updated model parameters Θ.

// Stage 1: Mix Training for Local Construction 1: Initial Llocal = 0 2: for each batch B in Dmix do 3: Z, W ←GRAPHGLUE(B) 4: Llocal ←ContrastiveLoss(Z) 5: if e ≥warmup epochs then 6: Lproto ←PrototypeLoss(Z, data name) 7: Llocal ←Llocal + Lproto 8: end if 9: ∇θLlocal ←Backward(Llocal) 10: OptimizerStep() 11: Update Prototypes with Z, W in Eq. (8) 12: end for // Stage 2: Mix Training for Global Manifold Skeleton 13: for each batch B in Dmix do 14: Z, W ←GRAPHGLUE(B) 15: Eknn ←Cross-Dataset KNN Graph(Z, data name) 16: T ←SampleTrianglePaths(Eknn, Number Sampled, Tsample) 17: Lgeo ←0 18: for t = 1 to Tsample do 19: Lgeo += GeometricLoss(W, T [t]) in Eq. (7) and Eq. (5) 20: end for 21: Lgeo ←Lgeo/Tsample 22: ∇θLgeo ←Backward(Lgeo) 23: OptimizerStep() 24: end for // Stage 3: Refine Local Manifold Structure For Each Dataset 25: for each dataset Ds in Dsingle do 26: Load graph data Gs with edge set Es 27: Ts ←SampleTrianglePaths(Es, Number Sampled, Tlocal) 28: for t = 1 to Tlocal do 29: Construct mini-graph batch Bt from Ts[t] 30: z, ztan ←GRAPHGLUE(Bt) 31: Lrefine ←GeometricLoss(W, Ts[t]) in Eq. (7) and Eq. (5) 32: ∇θLrefine ←Backward(Lrefine) 33: OptimizerStep() 34: end for 35: end for 36: for each dataset Dm in Dmulti do 37: for each batch (B) in Dm do 38: Z, W ←GRAPHGLUE(B) 39: Eknn ←Intra-Dataset KNN Graph(Z) 40: T ←SampleTrianglePaths(Eknn, Number Sampled, Tsample) 41: for t = 1 to Tsample do 42: Lgeo += GeometricLoss(W, T [t]) in Eq. (7) and Eq. (5) 43: end for 44: Lgeo ←Lgeo/Tsample 45: ∇θLgeo ←Backward(Lgeo) 46: OptimizerStep() 47: end for 48: end for 49: return Optimized Model parameters Θ∗

<!-- Page 29 -->

Published as a conference paper at ICLR 2026

D ALGORITHMS

D.1 MULTI-DOMAIN PRE-TRAINING

The training procedure is given in Algorithm 1, which consists of the data loader for pre-processing.

To use a unified interface, we process all the graph datasets at the graph level, which means each data sample in the dataset is a graph. Taking Reddit for instance, we extract 2-hop neighborhood ego-subgraph as a data sample for each node, and store the global edge index.

As we have many datasets from multiple domains, we need to build a mixture graph dataset loader that can iteratively load a batch of data from different datasets. For each batch, we uniformly sample from all source graph datasets.

During training, in each epoch, we first build locality recognition using graph contrastive learning Veliˇckovi´c et al. (2019); Qiu et al. (2020) that distinguishes the different semantics from different graph datasets. Meanwhile, we will update the Riemannian prototypes using EMA Izmailov et al. (2019); Morales-Brotons et al. (2024) for each dataset as in Eq. (8). After warm-up epochs, we still use sample-prototypes contrastive learning that guarantees the prototypes are truly around the center of each dataset distribution. Second, we build a cross-dataset KNN graph that builds a rough skeleton of the manifold, and learn from the regularization in Eq. (5) and Eq. (7). Finally, we refine the region for each dataset. We load every dataset and compute the geometric regularization, like the second step.

Here, since sampling triangles from a graph costs many computational resources, especially for large-scale graphs, we replace it with sampling pairs of adjacent edges for effective implementation.

D.2 COMPLEXITY ANALYSIS

We list the cost of the key modules of GraphGlue in Table 3, where B is the batch size, the number of graph samples in a batch; |V |, |E| are the average nodes/edges per graph in a batch; d is hidden dimension, setting to 512 commonly. M is number of nodes P in (k, M)-sparse perturbation, also the dimension of the manifold, commonly set to 32. ks is number of selected top-ks nodes in the sparse perturbation. Ts is number of sampled triangle paths, NOT all triangles. For more effectiveness, we sample pairs of adjacent edges to approximate closed triangle paths.

**Table 3.** Computational and memory complexity of each module in GraphGlue.

Module Computational complexity Memory complexity

(k, M)-Sparse Perturbation O(ksMB) O(BM(ks + d)) Adaptive Orthogonal Frame O(B(|V | + |E| + M 2)d) O(BMd) Matrix form of metric tensor O(BMd) O(BM) Lholo and Lcurv O(TsM) O(Ts) Riemannian prototypes and Lproto O(KBd + K(d + M)) O(K(d + M)) Riemannian MoE O(KBd) O(KB)

Thus, the total computational cost in pretraining phase is O(B(|V | + |E| + M 2 + K)d + TsM), and the adaption (per graph) costs O((|V | + |E|)d + K(d + M) + TsM). That is, in *GraphGlue* scales linearly with respect to the graph size. In our experiment, we pretrain the model on large-scale datasets, e.g., ogbn-arxiv and Reddit.

D.3 COMPLEXITY COMPARISON WITH OTHER GFMS

We compare the proposed GraphGlue to other GFM in pretraining and adaptation phases regarding the total computational cost. The results are summarized in Table 4.

Notes

• PRODIGY: In-context learning requires full attention over prompt and query nodes;

<!-- Page 30 -->

Published as a conference paper at ICLR 2026

**Table 4.** Comparison of computational complexity across graph few-shot learning methods.

## Model

Pretraining Adaptation (per graph sample)

PRODIGY O(B|V |2d) O((|V | + |E|)d + |V |2) GFT O(B(|V | + |E|)d + BTh) O((|V | + |E|)d + Th) RAGraph O(B(|V | + |E|)d + B|Er|d) O((|V | + |E|)d + |Er|d) SAMGPT O(B(|V | + |E|)d + Bksd) O((|V | + |E|)d + kpd) GCOPE O(B(|V | + |E|)d + BKcd) O((|V | + |E|)d + Kcd) MDGFM O(B(|V | + |E|)d + B|V |2) O((|V | + |E|)d + |V |2) GraphGlue O(B(|V | + |E| + M 2 + K)d + TsM) O((|V | + |E|)d + K(d + M) + TsM)

• GFT: T: number of trees, h: tree height; tree construction adds overhead;

• RAGraph: |Er|: retrieved edges from external library;

• SAMGPT: ks: number of structure tokens, kp: prompt tokens;

• GCOPE: Kc: number of virtual coordinators;

• MDGFM: Graph Structure Learning (GSL) involves dense adjacency refinement;

• GraphGlue: M = 32, Ts ≪|E|.

Furthermore, we compare the memory cost to GCOPE and MDGFM on six datasets. [1, 2, 3,..., 6] denotes that we incrementally include ogbn-arxiv, computers, FB15k-237, Reddit, PROTEINS, HIV in the pretraining dataset. Under the setting of 512 batch size, [10, 10] neighbor sampler size, d = 512. Results on GPU memory cost (GB) are collected in Table 5.

**Table 5.** Memory Cost. Lower values indicate better efficiency.

## Model

1 2 3 4 5 6

GCOPE 18.39 19.11 21.12 OOM OOM OOM MDGFM 19.71 21.67 29.35 OOM OOM OOM GraphGlue 12.53 15.07 15.73 16.87 28.67 29.21

E RELATED WORK

E.1 GRAPH FOUNDATION MODELS

Graph Foundation Models (GFMs) aim to provide pre-trainable, general-purpose deep learning architectures for graph-structured data Wang et al. (2025b); Liu et al. (2025). Recently, researchers have extended the capabilities of Large Language Models (LLMs) to text-attributed graphs, enabling cross-domain transfer learning through textual descriptions Zhu et al. (2025); Xia et al. (2024); Tang et al. (2024); Ren et al. (2024); Chen et al. (2024). Additionally, GFMs have been developed for various specialized domains, such as knowledge graphs Huang et al. (2025); Luo et al. (2025), recommender systems Wu et al. (2025), and molecular graphs Xia et al. (2023); Sypetkowski et al. (2024). Given the prevalence of text-free graphs, recent efforts have focused on constructing generalpurpose models via multi-domain pre-training Yuan et al. (2025); Chen et al. (2025); Wang et al. (2025a).

E.2 MULTI-DOMAIN GRAPH PRE-TRAINING

In graph pre-training, Graph Neural Networks (GNNs) are trained by self-supervised learning—either generative Hou et al. (2022) or contrastive Veliˇckovi´c et al. (2019); Qiu et al. (2020). In light of the semantic heterogeneity across different domains, several methods have been proposed to learn shared or invariant knowledge Yuan et al. (2025); Chen et al. (2025); Wang et al. (2025a). Despite the encouraging results, the theoretical foundations of how knowledge is integrated and transferred remain underexplored.

<!-- Page 31 -->

Published as a conference paper at ICLR 2026

In graph pre-training, Graph Neural Networks (GNNs) are trained using self-supervised learning—either generative Hou et al. (2022) or contrastive Veliˇckovi´c et al. (2019); Qiu et al. (2020)—to capture intrinsic semantics from unlabeled data. While traditional pre-training typically operates within a single domain, multi-domain graph pre-training has recently attracted growing interest. However, integrating knowledge across diverse domains remains challenging due to significant semantic heterogeneity. Several methods have been proposed to learn shared or invariant knowledge using advanced techniques Yuan et al. (2025); Chen et al. (2025); Wang et al. (2025a). For instance, Chen et al. (2025) addresses architecture inconsistency by using disentangled learning to adaptively customize network architectures based on invariant graph patterns. Meanwhile, Yuan et al. (2025) aligns multi-domain features with domain-invariant aligners and uses a graph spectral-based error bound to theoretically guide knowledge transfer. Despite the encouraging results, the theoretical foundations of how knowledge is integrated and transferred in this context remain underexplored.

E.3 GRAPH FINE-TUNING AND PROMPT LEARNING

The alignment of pre-trained graph models with downstream tasks necessitates an adaptation phase, and existing adaptation methods can be roughly categorized into two paradigms: graph fine-tuning and prompt learning. Concretely, graph fine-tuning adapts the model behavior using limited targetdomain data Sun et al. (2024d); Wang et al. (2024; 2025c). For example, Sun et al. (2024d) finetunes the entire model on downstream data. A more common strategy is to keep the majority of the pre-trained parameters frozen and only train a simple classification head, a technique employed by models like Zhao et al. (2024); Liu et al. (2024). Bevilacqua et al. (2025) proposes a unique adaptation strategy: it freezes the large, pre-trained expansion map and only trains a smaller reduction map and a task-specific head for the new task. And recent advances introducing parameter-efficient finetuning methods such as low-rank adaptation Yang et al. (2025b). On the contrary, graph prompting keeps the pre-trained parameters frozen and enhances performance by inserting learnable prompt vectors Yu et al. (2025a); Liu et al. (2023); Yu et al. (2024a;b; 2025b). For instance, Liu et al. (2023) unifies tasks under a subgraph similarity template and employs a learnable vector to guide the READOUT function. Other approaches generate more adaptive prompts, such as PRONOG Yu et al. (2025b), which uses a conditional network to create node-specific prompts for non-homophilic graphs, and PRODIGY Huang et al. (2023), which formulates a novel prompt graph for in-context learning. To tackle more complex scenarios, several works have developed dual-prompting mechanisms. Jiao et al. (2025); Yu et al. (2024a) introduce a feature prompt and a heterogeneity prompt to bridge the gap between homogeneous and heterogeneous graphs. Yu et al. (2024c) leverages a composed prompt for task-specific knowledge and an open prompt for global knowledge from multiple pre-training tasks. Similarly, Yu et al. (2025a) designs holistic and specific structural prompts for cross-domain adaptation. Yet, how to quantify the transfer effort to the target domain remains an open issue.

E.4 RIEMANNIAN GRAPH REPRESENTATION LEARNING

In recent years, Riemannian manifolds have emerged as a promising alternative to traditional Euclidean spaces in graph representation learning Sun et al. (2026b; 2025a; 2024a;b; 2026a; 2023b;a; 2024c). Most existing Riemannian models are tailored to specific tasks Grover et al. (2025), and often leverage the particular manifolds, such as the hyperbolic space Chami et al. (2019); Yang et al. (2025a), the spherical space Liu et al. (2022), the symmetric positive definite manifold Ju & Guan (2024), and their products Gu et al. (2019); Bachmann et al. (2020); Sun et al. (2022a) and quotients Xiong et al. (2022). Very recently, Sun et al. (2025b) introduces a structural vocabulary and designs a new GNN backbone on the product manifold for general-purpose graph foundation model. In contrast to backbone architecture design, our focus lies in developing a framework for multi-domain pre-training and characterizing a general manifold that underlies diverse graphs.

F EMPIRICAL DETAILS

F.1 DATASET DESCRIPTION

This section provides a detailed description of the 12 benchmark datasets used in our experiments. For a summary of their statistics, please refer to Table 6.

<!-- Page 32 -->

Published as a conference paper at ICLR 2026

**Table 6.** Statistics of 12 datasets used in our experiment.

Domain Dataset Task # Graphs Avg. #Nodes Avg. #Edges # Classes

Citation PubMed Node 1 19,717 88,648 3 Arxiv Node 1 169,343 1,166,243 40

Co-purchase Computers Node 1 13,752 491,722 10 Photo Node 1 7,650 238,162 8

Social Network Reddit Node 1 232,965 114,615,892 41 FacebookPagePage Node 1 22,470 342,004 4

Knowledge Graph FB15K 237 Edge 1 14,541 310,116 237 WordNet18RR Edge 1 40,943 93,003 11

Bioinformatics PROTEINS Graph 1,113 39.1 145.6 2 MUTAG Graph 188 17.9 39.6 2

Molecule HIV Graph 41,127 25.5 27.5 2 Lipophilicity Graph 4,200 27.0 59.0 2

Our experiments utilize a diverse set of 12 benchmark datasets. For citation networks, we include PubMed, where nodes represent scientific publications, and the task is to classify their category, as well as Arxiv, a large-scale network for academic paper classification. In the co-purchase domain, both Computers and Photo are sourced from Amazon; in these graphs, nodes are products, edges signify frequent co-purchases, and the task is to predict product categories. For social networks, Reddit is constructed from posts, with the goal of predicting a post’s community, while FacebookPagePage consists of official pages with edges as mutual likes, and the task is to classify the page’s category. Our knowledge graph datasets include WordNet18RR, where the task is to classify the semantic relation between synsets, and FB15K 237, used to predict the relation type between entities. Finally, for graph-level classification, we use several benchmarks: PROTEINS and MUTAG are bioinformatics datasets for binary classification, with the latter predicting compound mutagenicity; similarly, HIV and Lipophilicity are molecular datasets for binary classification tasks that predict molecular properties.

F.2 BASELINES

We evaluate our model against a comprehensive set of baselines from three main categories: Supervised GNNs, Self-Supervised GNNs, and Graph Foundation Models.

Supervised GNNs This category includes foundational GNNs that are trained from scratch in a supervised manner for a specific downstream task.

• GCN Kipf & Welling (2017) is a widely used GNN model that generates node representations by aggregating information from local node neighborhoods. It employs a meanpooling approach for neighborhood aggregation to integrate information from adjacent nodes.

• GraphSAGE Hamilton et al. (2017) is an inductive representation learning framework designed for large graphs. It utilizes a mean-pooling propagation rule and often employs a neighborhood sampling approach to scale efficiently to large-scale graphs.

• GIN Xu et al. (2019) is a state-of-the-art GNN that is commonly used as a powerful supervised baseline, particularly for graph classification tasks.

Self-Supervised GNNs These methods first pre-train a GNN encoder on unlabeled graph data using self-supervised objectives and are then fine-tuned for downstream tasks. They represent the predominant pre-training paradigm in graph machine learning.

• DGI Veliˇckovi´c et al. (2019) learns node representations by maximizing the mutual information between local patch representations and a global graph summary vector. Its contrastive objective is notably not based on random walks.

• GraphMAE Hou et al. (2022) operates by masking a portion of node features and training a GNN-based architecture to reconstruct them. It utilizes a scaled cosine error for reconstruction to improve training robustness.

<!-- Page 33 -->

Published as a conference paper at ICLR 2026

• GCC Qiu et al. (2020) is a self-supervised pre-training framework designed to capture transferable structural representations across multiple networks. Its pre-training task is subgraph instance discrimination, using contrastive learning to distinguish between augmented views of a node’s local subgraph and those from other nodes.

Graph Foundation Models This group comprises recent, large-scale models pre-trained on diverse datasets and fine-tuned for strong generalization. They are the most direct competitors to our work and represent the current state-of-the-art.

• PRODIGY Huang et al. (2023) enables in-context learning over graphs by formulating tasks with a novel prompt graph representation. This structure connects prompt examples with queries, allowing the model to perform new tasks without updating its parameters.

• GFT Wang et al. (2024) rethinks transferable patterns as computation trees derived from the GNN message-passing process. It uses a tree reconstruction task for pre-training and unifies downstream tasks as tree classification.

• RAGraph Jiang et al. (2024) is a retrieval-augmented framework that improves GNN generalization by retrieving knowledge from an external library of toy graphs. The retrieved information is injected into the target graph using a message-passing prompt mechanism to enhance performance.

• SAMGPT Yu et al. (2025a) is a text-free graph foundation model for multi-domain pretraining and cross-domain adaptation. It uses learnable structure tokens to harmonize structural differences across domains during pre-training and dual prompts to adapt knowledge to new target domains.

• GCOPE Zhao et al. (2024) mitigates negative transfer during cross-domain pre-training by introducing coordinators, which are virtual nodes that act as bridges between disparate graph datasets. This approach helps create a unified representation from multiple graphs.

• MDGFM Wang et al. (2025a) focuses on achieving robust knowledge transfer through topology alignment. It employs a Graph Structure Learning (GSL) module to refine graph structures, reduce noise, and learn domain-invariant knowledge.

F.3 IMPLEMENTATION NOTES

Our primary framework is a leave-one-out cross-domain evaluation. We pre-train models on five source datasets and evaluate them on a single held-out target dataset. This protocol applies to Self- Supervised GNNs and Graph Foundation Models. In contrast, supervised GNNs are not pre-trained and are instead trained directly from scratch on the target task. All downstream evaluations use a few-shot fine-tuning setting. For the pre-trained models, we use only k labeled samples per class from the target task for fine-tuning. In our experiments, k is set to 1 and 5. After setting aside these training samples, the remaining data is randomly split into a validation set (10%) and a test set (90%). We evaluate performance across three downstream tasks: node classification, Link Classification, and graph classification. For node and Link Classification, we use Accuracy (ACC) as the evaluation metric. For graph classification, we use Area Under the Curve (AUC). To ensure robust results, the final reported score for each experiment is the average over 10 runs with different random data splits.

For pretraining, we extract the 2-hop ego-graph with 10 neighbors each hop for single graph datasets and adopt a 2-layer GCN Kipf & Welling (2017) as backbone model. The dimension of the manifold, or the number of virtual nodes in (k, M)-sparse perturbation, is set to M = 32 with k = 15. For the KNN construction for mixed data training in Algorithm 1 and multi-graph datasets training, we also set k = 15. The dropout rate is 0.1 and the learning rate is 1e−4. The model input dimension is 128. For different datasets, we unify the input dimension by random projection or SVD. For the knowledge graph datasets, we use Node2Vec Grover & Leskovec (2016) to get the node embeddings. The hidden dimension is 512. The temperature in contrastive learning is 1.0. The optimizer is Adam Kingma & Ba (2015), with a cosine annealing schedule Loshchilov & Hutter (2017).

**Table 7.** to Table 12 show the hyperparameters in few-shot transferring: the learning rate lr, dropout rate drop, the KNN number k between prototypes and target graph data points, and the balance coefficient λ. We adopt the classifier head with only a linear layer for the node or graph classification

<!-- Page 34 -->

Published as a conference paper at ICLR 2026 task. For the link classification task, we simply adopt a bilinear layer as a classifier. The gated function for Riemannian MoE is an MLP with 2 layers.

**Table 7.** Hyper-parameters for 1-shot and

5-shot cross-domain transfer on Arxiv.

lr drop k λ

1-shot 1e−3 0.1 3 1.0

5-shot 1e−3 0.15 3 1.0

**Table 8.** Hyper-parameters for 1-shot and 5-shot cross-domain transfer on Computers.

lr drop k λ

1-shot 1e−3 0.2 3 1.0

5-shot 1e−3 0.2 3 1.0

**Table 9.** Hyper-parameters for 1-shot and 5-shot cross-domain transfer on Reddit.

lr drop k λ

1-shot 1e−3 0.1 3 0.1

5-shot 1e−3 0.15 3 0.1

**Table 10.** Hyper-parameters for 1-shot and 5-shot cross-domain transfer on FB15k 237.

lr drop k λ

1-shot 1e−4 0.5 3 0.5

5-shot 1e−4 0.5 3 0.5

**Table 11.** Hyper-parameters for 1-shot and 5-shot cross-domain transfer on PROTEINS.

lr drop k λ

1-shot 1e−3 0.1 1 2.0

5-shot 1e−3 0.15 1 2.0

**Table 12.** Hyper-parameters for 1-shot and

5-shot cross-domain transfer on HIV.

lr drop k λ

1-shot 1e−3 0.1 2 2.0

5-shot 1e−3 0.15 2 2.0

G ADDITIONAL RESULTS

G.1 SUPPLEMENTARY RESULTS

We provide additional empirical results to further validate our framework. We present comprehensive results for both cross-domain transfer (Table 18 and 19) and intra-domain transfer (Table 20 and 21) in few-shot settings. Furthermore, an ablation study in Table 22 demonstrates the effectiveness of the key components of our model. We also include an additional visualization of the pre-trained manifold in Figure 8, where we first project the 512-dimensional embeddings into 3-D using t-SNE van der Maaten & Hinton (2008) and then apply RBF interpolation Wright & Fornberg (2006) to generate a smooth surface that approximates the learned global Riemannian manifold.

G.2 COMPREHENSIVE ABLATION STUDY

We conduct a further ablation study to verify the effectiveness of EMA, prototype loss and Riemannian MoE. Specifically, we introduce 3 variants of GraphGlue, described as follows:

• “w/o EMA” means that we replace EMA with the common average of a batch of embeddings;

• “w/o Lproto” means pretraining without prototype loss;

• “w/o Riemannian MoE” means that during adaption, Riemannian MoE module is replaced by a typical prompting scheme.

In Table 13, both results on 1-shot setting and 5-shot setting demonstrate the effectiveness of the proposed components.

<!-- Page 35 -->

Published as a conference paper at ICLR 2026

**Table 13.** Ablation study of GraphGlue’s key components.

Variants Arxiv Computers Reddit FB15k 237 PROTEINS HIV

1-shot w/o EMA 15.46±1.41 30.84±9.50 7.43±2.37 35.90±17.40 58.48±2.56 52.62±2.41 w/o L proto 9.57±4.56 31.24±10.36 37.90±9.34 43.59±8.13 58.49±2.60 54.10±2.76 GRAPHGLUE 29.73±2.56 61.03±7.13 68.42±4.68 60.89±2.11 69.12±4.19 58.53±8.20

5-shot w/o EMA 16.08±2.13 34.90±7.77 11.53±2.26 40.21±12.07 59.85±4.53 53.87±2.43 w/o L proto 15.26±9.91 36.63±11.84 46.13±14.14 64.56±16.42 61.64±6.28 55.50±2.70 GRAPHGLUE 39.98±1.67 74.15±2.38 84.89±0.68 79.52±1.75 73.94±2.38 62.18±2.50

G.3 HYPERPARAMETER SENSITIVITY ANALYSIS

For AOF, we investigate the hyperparameter sensitivity on the neighborhood size k and the number of nodes M in (k, M)-sparse perturbation. Results are shown in Table 14 and 15.

**Table 14.** 1-shot results under different settings.

(a) Analysis on k (M = 32).

k Arxiv Computers Reddit FB15k 237 PROTEINS HIV

2 18.64±3.10 49.80±12.41 66.04±1.91 31.63±6.19 57.80±3.05 53.07±3.02 5 17.16±3.08 43.76±10.78 48.57±6.76 21.10±2.47 59.49±2.62 52.04±3.01 10 15.29±2.69 46.21±11.10 61.03±2.89 45.51±15.83 58.10±3.41 54.42±3.16 15 29.73±2.56 61.03±7.13 68.42±4.68 60.89±2.11 69.12±4.19 58.53±8.20 30 20.23±2.83 55.39±10.15 49.57±4.80 38.85±19.62 54.36±5.80 54.49±3.33 60 18.20±2.63 51.88±10.22 75.76±3.00 31.83±16.41 58.24±3.34 51.64±3.44

(b) Analysis on M (k = 15).

M Arxiv Computers Reddit FB15k 237 PROTEINS HIV

4 19.89±3.79 42.66±11.17 60.57±4.48 45.16±5.85 56.99±4.64 52.58±3.68 8 22.64±2.51 46.24±9.12 61.73±5.02 54.80±9.57 58.77±1.92 52.32±2.94 16 27.84±1.47 56.92±14.86 62.73±1.97 57.09±7.44 55.34±5.68 54.18±3.84 32 29.73±2.56 61.03±7.13 68.42±4.68 60.89±2.11 69.12±4.19 58.53±8.20

**Table 15.** 5-shot results under different settings.

(a) Analysis on k (M = 32).

k Arxiv Computers Reddit FB15k 237 PROTEINS HIV

2 29.49±3.14 70.82±3.14 80.46±1.21 36.24±5.11 59.42±2.03 56.10±2.76 5 23.95±7.88 67.74±4.02 67.41±8.74 39.26±14.50 60.45±3.05 54.76±2.33 10 25.86±7.17 70.59±18.03 80.49±0.59 48.01±10.53 60.86±3.08 55.69±4.23 15 39.98±1.67 74.15±2.38 84.89±0.68 79.52±1.75 73.94±2.38 62.18±2.50 30 33.00±1.63 57.65±29.35 64.57±6.84 42.88±16.13 62.09±2.45 54.63±3.01 60 32.59±1.57 68.08±1.66 85.24±0.42 45.42±8.09 60.40±1.35 54.01±3.69

(b) Analysis on M (k = 15).

M Arxiv Computers Reddit FB15k 237 PROTEINS HIV

4 32.62±3.40 64.66±13.87 70.86±2.92 60.63±4.80 57.38±4.76 56.27±1.62 8 34.92±1.50 72.25±1.99 78.82±1.79 63.18±14.37 59.70±1.92 54.64±2.35 16 37.78±5.79 74.22±13.95 74.92±2.41 70.11±11.89 60.62±3.66 57.55±2.65 32 39.98±1.67 74.15±2.38 84.89±0.68 79.52±1.75 73.94±2.38 62.18±2.50

<!-- Page 36 -->

Published as a conference paper at ICLR 2026

G.4 RESULTS ON HETEROPHILIC GRAPHS

We demonstrate the performance of GraphGlue on several benchmarking heterophilic graphs (Amazon-ratings, Roman-empire, Texas and Wisconsin). The results are in Table 16 and 17.

**Table 16.** Performance under different shot settings with pretrained on ogbn-arxiv, Reddit, Computers, FB15k 237, PROTEINS, and HIV.

## Method

Amazon-Ratings Roman-empire Texas Wisconsin

1-shot GCOPE 28.65±5.82 11.44±1.91 33.19±6.62 31.22±6.85 MDGFM 29.53±3.45 14.51±2.08 34.63±10.70 35.11±10.53 GraphGlue 31.16±3.56 16.23±3.00 35.16±20.43 37.95±10.91

5-shot GCOPE 30.06±5.11 16.00±1.29 36.31±10.14 38.21±2.96 MDGFM 30.42±3.80 17.15±1.66 48.33±6.36 47.46±4.86 GraphGlue 32.17±2.91 18.50±1.07 50.88±11.93 49.71±8.00

**Table 17.** Performance under different shot settings with pretrained on 8 datasets (including Amazon-Ratings and Roman-Empire).

## Method

Amazon-Ratings Roman-empire Texas Wisconsin

1-shot GCOPE 29.03±4.17 13.14±2.36 33.82±7.39 30.08±5.13 MDGFM 27.01±2.98 14.11±2.14 36.02±9.54 33.28±8.76 GraphGlue 34.12±2.57 18.19±2.51 38.65±13.88 40.17±10.09

5-shot GCOPE 32.83±3.26 16.98±1.40 41.33±9.85 43.74±3.19 MDGFM 32.54±3.75 16.77±1.92 48.10±7.26 46.62±4.16 GraphGlue 36.26±3.09 20.67±1.34 52.60±6.07 51.49±7.97

G.5 VISUALIZATION OF MANIFOLD GLUING

Manifold gluing aims to glue local pieces into one smooth surface, whose process is described as follows.

• First, we construct local geometry on each patch using (k, M)-sparse perturbation–like drawing a coordinate grid;

• Then, when two graphs share similar structures, we ”glue” their grids together along overlapping regions, ensuring no stretching or twisting (via the isometry of Def. 4.4 and holonomy of Eq. 5);

• Finally, we smooth the entire surface so that curvature changes gradually–forming a unified manifold where knowledge flows naturally across domains.

In addition, we visualize a toy example of the aforementioned process in Figure 7.

<!-- Page 37 -->

Published as a conference paper at ICLR 2026

Isometry and holonomy regularization k-order smoothing regularization

Local geometry construction

**Figure 7.** Visualization of the pre-trained manifold from 6 datasets.

**Table 18.** Performance of cross-domain transfer on various downstream tasks in the 1-shot setting, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined.

## Model

Node Classification Link Classification Graph Classification

Arxiv Computers Reddit FB15k 237 PROTEINS HIV

GCN 12.61±1.75 33.89±3.86 11.15±2.14 32.11±2.37 50.11±13.07 52.56±5.39 GraphSAGE 14.68±3.76 35.47±8.29 14.69±2.31 35.74±2.19 58.99±2.79 56.78±3.75 GIN 11.20±2.03 44.77±6.02 18.53±1.89 38.25±2.55 54.22±13.50 52.63±7.47

GCC 12.65±2.08 34.82±6.13 54.78±5.64 47.84±1.95 59.20±7.97 52.63±3.63 DGI 13.32±3.35 35.26±7.58 60.08±4.80 42.50±2.03 53.18±8.44 52.80±7.53 GraphMAE 12.61±1.75 33.89±3.86 11.15±2.14 51.34±1.87 60.11±13.07 52.78±6.72

PRODIGY 28.45±2.20 45.32±4.10 35.67±3.20 53.50±1.02 48.90±5.40 41.78±4.50 GFT 26.59±2.45 54.65±4.08 58.87±2.53 58.07±1.39 55.41±5.87 58.94±6.32 RAGraph 18.71±2.58 46.21±4.37 52.56±3.48 52.18±3.04 51.42±5.18 54.26±3.51 SAMGPT 24.15±3.81 47.61±7.42 62.85±4.22 57.44±2.46 52.42±3.15 55.48±3.26 GCOPE 26.52±5.56 54.55±9.14 62.76±4.52 58.25±2.67 55.19±3.59 58.93±2.60 MDGFM 26.05±2.40 46.68±8.43 64.88±3.31 56.11±1.68 53.41±5.34 51.46±2.85

GRAPHGLUE 28.88±5.22 59.50±7.05 67.12±3.39 59.75±5.27 59.87±4.85 60.22±3.09

<!-- Page 38 -->

Published as a conference paper at ICLR 2026

**Table 19.** Performance of cross-domain transfer on various downstream tasks in the 5-shot setting, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined.

## Model

Node Classification Link Classification Graph Classification

Arxiv Computers Reddit FB15k 237 PROTEINS HIV

GCN 27.68±2.13 65.78±4.20 28.36±1.01 52.43±1.87 55.04±9.98 47.81±3.91 GraphSAGE 26.18±2.21 66.75±4.45 22.27±1.17 58.91±1.52 60.45±1.39 50.59±0.75 GIN 26.06±2.42 69.51±3.50 29.03±1.66 63.76±1.73 58.87±5.05 49.12±4.95

GCC 26.84±2.14 62.63±3.16 65.21±1.56 73.69±1.24 64.20±3.09 57.41±1.73 DGI 27.18±2.33 61.02±3.20 62.72±2.21 68.32±1.46 53.34±6.27 52.23±8.49 GraphMAE 27.68±2.13 65.78±4.20 28.36±1.01 77.25±1.07 65.04±9.98 57.81±3.91

PRODIGY 33.67±2.80 52.78±3.60 42.34±2.90 72.17±6.94 55.23±4.70 48.65±3.80 GFT 36.78±1.92 69.13±3.56 66.28±1.42 79.13±1.68 62.18±3.59 57.68±5.43 RAGraph 32.35±1.78 62.38±3.75 63.08±1.32 64.52±2.57 58.62±2.86 56.32±3.46 SAMGPT 34.42±2.25 60.87±3.64 75.12±1.63 77.63±2.71 59.14±2.60 57.63±2.87 GCOPE 39.18±1.96 72.27±2.84 80.45±0.70 79.38±2.29 64.85±2.41 58.47±1.82 MDGFM 32.28±1.77 64.08±5.38 76.55±1.72 77.67±2.05 57.79±3.42 55.79±3.16

GRAPHGLUE 37.02±2.33 73.29±0.70 85.05±1.17 81.51±2.31 65.32±2.45 61.55±2.66

**Table 20.** Performance of intra-domain transfer on various downstream tasks in the 1-shot setting, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined.

## Model

Node Classification Link Classification Graph Classification

Arxiv Computers Reddit FB15k 237 PROTEINS HIV

GCN 12.61±1.75 33.89±3.86 11.15±2.14 32.11±2.37 60.11±13.07 52.56±5.39 GraphSAGE 14.68±3.76 35.47±8.29 14.69±2.31 35.74±2.19 68.99±2.79 56.78±3.75 GIN 11.20±2.03 44.77±6.02 18.53±1.89 38.25±2.55 64.22±13.50 52.63±7.47

GCC 12.65±2.08 34.82±6.13 54.78±5.64 47.80±1.97 59.20±7.97 52.63±3.63 DGI 13.32±3.35 35.26±7.58 60.08±4.80 42.56±2.05 53.18±8.44 52.80±7.53 GraphMAE 12.61±1.75 33.89±3.86 11.15±2.14 51.34±1.87 60.11±13.07 52.56±5.39

PRODIGY 28.45±2.20 45.32±4.10 35.67±3.20 53.50±1.02 48.90±5.40 41.78±4.50 GFT 28.83±1.76 53.94±3.47 63.03±2.34 59.43±0.87 63.54±4.98 58.17±5.76 RAGraph 20.53±2.13 50.39±3.81 59.91±2.79 52.09±2.57 52.83±4.37 55.73±3.06 SAMGPT 25.88±3.58 55.31±6.67 63.05±3.75 58.75±2.16 64.59±2.89 52.38±2.71 GCOPE 27.41±4.77 58.24±7.48 65.07±3.76 58.33±1.79 68.55±3.17 60.67±2.42 MDGFM 10.76±2.04 43.22±8.53 64.38±3.11 58.32±1.71 57.79±11.51 53.03±3.88

GRAPHGLUE 29.73±2.56 61.03±7.13 68.42±4.68 60.89±2.11 69.12±4.19 58.53±8.20

**Table 21.** Performance of intra-domain transfer on various downstream tasks in the 5-shot setting, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined.

## Model

Node Classification Link Classification Graph Classification

Arxiv Computers Reddit FB15k 237 PROTEINS HIV

GCN 27.68±2.13 65.78±4.20 28.36±1.01 52.43±1.87 65.04±9.98 57.81±3.91 GraphSAGE 26.18±2.21 66.75±4.45 22.27±1.17 58.91±1.52 70.45±1.39 60.59±0.75 GIN 26.06±2.42 69.51±3.50 29.03±1.66 63.76±1.73 68.87±5.05 59.12±4.95

GCC 26.84±2.14 62.63±3.16 65.21±1.56 73.64±1.25 64.20±3.09 58.34±2.19 DGI 27.18±2.33 61.02±3.20 62.72±2.21 68.32±1.47 53.34±6.27 52.23±8.49 GraphMAE 27.68±2.13 65.78±4.20 28.36±1.01 77.25±1.07 65.04±9.98 57.81±3.91

PRODIGY 33.67±2.80 52.78±3.60 42.34±2.90 72.17±6.94 55.23±4.70 48.65±3.80 GFT 39.02±1.39 73.41±3.21 71.37±1.45 79.25±0.94 74.69±2.84 61.03±4.83 RAGraph 35.74±1.46 61.98±2.79 66.30±0.75 67.86±1.69 62.52±3.83 59.23±2.80 SAMGPT 38.14±1.87 64.68±2.87 74.89±1.51 78.76±2.33 70.48±2.19 59.09±2.49 GCOPE 39.45±1.23 73.06±2.19 82.12±0.53 78.69±1.87 73.76±2.53 60.05±1.73 MDGFM 19.17±2.39 68.19±4.03 81.27±1.23 78.24±2.35 65.95±8.62 54.73±4.37

GRAPHGLUE 39.98±1.67 74.15±2.38 84.89±0.68 79.52±1.75 69.74±2.38 62.18±2.50

<!-- Page 39 -->

Published as a conference paper at ICLR 2026

**Table 22.** Ablation study of GRAPHGLUE’s key components.

Variants Arxiv Computers Reddit FB15k 237 PROTEINS HIV

1-shot w/o Lcurv 22.33±2.56 49.63±5.11 64.38±5.12 53.12±3.74 51.21±3.54 50.34±3.87 w/o Lholo 27.14±3.62 56.39±4.16 65.93±4.33 54.85±4.78 53.23±4.48 54.83±2.15 GRAPHGLUE 28.88±5.22 59.50±7.05 67.12±3.39 59.75±5.27 55.87±4.85 60.22±3.09

5-shot w/o Lcurv 29.17±3.14 66.85±3.58 74.13±1.92 69.33±3.98 58.77±4.35 57.13±3.33 w/o Lholo 35.77±2.64 67.16±2.45 79.11±3.47 74.02±0.97 58.74±2.18 54.12±4.19 GRAPHGLUE 37.02±2.33 73.29±0.70 85.05±1.17 81.51±2.31 65.32±2.45 61.55±2.66 ogbn-arxiv Computers Reddit FB15k_237 PROTEINS HIV

**Figure 8.** Visualization of the pre-trained manifold from 6 datasets.

<!-- Page 40 -->

Published as a conference paper at ICLR 2026

H REPRODUCIBILITY STATEMENT

This part provides the reproducibility statement on claims, theory assumptions and proofs, empirical result reproducibility, empirical setting/details, empirical statistical significance, open access to data/code, computation resources, code of ethics, safeguards, licenses for existing assets, new assets, crowdsourcing and research with human subjects, declaration of LLM usage, and broader impacts.

1. Claims. Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? Yes. Main claims made in the abstract and introduction reflect the contributions in Sections 4, 5 and 6.

2. Theory assumptions and proofs. For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? Yes. The theoretical results including the assumptions are clearly stated in Theorems in this paper, while the complete and correct proofs are provided in Appendix B.

3. Empirical result reproducibility. Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? Yes. Key information is introduced in the subsection of “Evaluation Protocals”, and further details are disclosed in Appendix F entitled “Empirical Details”.

4. Empirical setting/details. Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results? Yes. Specifications are provided in Appendix F entitled “Empirical Details”, and the full details are included in the code.

5. Empirical statistical significance. Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? Yes. In the experiment, each case undergoes 10 independent runs, and we report the mean with the error bar of standard derivations.

6. Open access to data and code. Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results? Yes. Codes and data are available at the anonymous GitHub link with sufficient instructions.

7. Computation resources. For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? Yes. The computer resources for the evaluation are described in Appendix F entitled “Empirical Details”.

8. Code of ethics. Does the research conducted in the paper conform, in every respect, with the ICLR Code of Ethics https://iclr.cc/public/CodeOfEthics? Yes. We confirm that the research conducted in the paper conform, in every respect, with the ICLR Code of Ethics.

9. Safeguards. Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)? Not available.

10. Licenses for existing assets. Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? Yes. The original papers that produced the code package or dataset are properly cited in this submission.

<!-- Page 41 -->

Published as a conference paper at ICLR 2026

11. New assets. Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? Yes. The documentation is provided alongside the Codes of the proposed model.

12. Crowdsourcing and research with human subjects. For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? Not available. This paper does not involve crowdsourcing nor research with human subjects.

13. Institutional review board (IRB) approvals or equivalent for research with human subjects. Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? Not available. This paper does not involve crowdsourcing nor research with human subjects.

14. Declaration of LLM usage. Does the paper describe the usage of LLMs (especially when it is an important, original, or non-standard component of the core methods in this research)? Yes. LLM is used to polish writing only, and we include a section of “Declaration of LLM Usage” in the Appendix.

15. Broader impacts. Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? Yes. Both potential positive societal impacts and negative societal impacts are included in the section of “Broader Impact and Limitations” in the Appendix.

I ETHICS STATEMENT

We confirm that the research conducted in the paper conform, in every respect, with the ICLR Code of Ethics https://iclr.cc/public/CodeOfEthics.

J DECLARATION OF LLM USAGE

Large Language Model (LLM) is used to polish writing. Concretely, we refine the textual contents in Section 1 (Introduction) and Section 7 (Conclusion) with LLM.

K BROADER IMPACT

Our work brings together two previously separate domains – multi-domain graph pre-training and differential geometry. Our constructions taking in multi-domain graphs with a unified, smooth Riemannian manifold, thus enabling the solid tools of differential geometry to systematically understand the knowledge integration and transfer across graphs. Theoretically, we develop the neural manifold gluing that makes the differential geometry principles implementable through deep learning. In practice, the proposed pre-training model paves the way to build a powerful graph foundation model with better generality and quantifiable transferability.

Positive societal impacts lie in the transferability and generality of the proposed graph pre-training model, allowing for the analysis on more complicated real-world graphs. None of negative societal impacts we feel must be specifically highlighted.
