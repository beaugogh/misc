---
title: "UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37272
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37272/41234
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization

<!-- Page 1 -->

UniABG: Unified Adversarial View Bridging and Graph Correspondence for

Unsupervised Cross-View Geo-Localization

Cuiqun Chen1, Qi Chen1, 3, 4, Bin Yang2†, Xingyi Zhang1†

## 1 School of Computer Science and Technology, Anhui University, China 2 School of Computer Science, Wuhan University, Wuhan,

China 3 Information Materials and Intelligent Sensing Laboratory of Anhui Province, Anhui University 4 the Key Laboratory of Intelligent Computing and Signal Processing of Ministry of Education, Anhui University chencuiqun@ahu.edu.cn, cq@stu.ahu.edu.cn, yangbin cv@whu.edu.cn, xyzhanghust@gmail.com

† Corresponding authors

## Abstract

Cross-view geo-localization (CVGL) matches query images (e.g., drone) to geographically corresponding opposite-view imagery (e.g., satellite). While supervised methods achieve strong performance, their reliance on extensive pairwise annotations limits scalability. Unsupervised alternatives avoid annotation costs but suffer from noisy pseudo-labels due to intrinsic cross-view domain gaps. To address these limitations, we propose UniABG, a novel dual-stage unsupervised cross-view geo-localization framework integrating adversarial view bridging with graph-based correspondence calibration. Our approach first employs View-Aware Adversarial Bridging (VAAB) to model view-invariant features and enhance pseudo-label robustness. Subsequently, Heterogeneous Graph Filtering Calibration (HGFC) refines crossview associations by constructing dual inter-view structure graphs, achieving reliable view correspondence. Extensive experiments demonstrate state-of-the-art unsupervised performance, showing that UniABG improves Satellite →Drone AP by +10.63% on University-1652 and +16.73% on SUES- 200, even surpassing supervised baselines.

Code — https://github.com/chenqi142/UniABG Extended version — https://arxiv.org/abs/2511.12054

## Introduction

Cross-view geo-localization (CVGL) addresses the critical task of determining geographic coordinates for ground-level or aerial query images by matching them against georeferenced satellite imagery. The proliferation of unmanned aerial vehicles (UAVs) has significantly expanded CVGL’s scope, enabling centimeter-level positioning essential for urban navigation, autonomous systems, and augmented reality. UAVs’ flexible low-altitude imaging capability renders them particularly advantageous for fine-grained localization in complex environments.

Nevertheless, CVGL faces inherent challenges stemming from extreme cross-modal viewpoint and appearance variations. Prior efforts mitigate these through geometry-aware architectures (Regmi and Shah 2019; Liu and Li 2019), semantic-guided embedding (Hu et al. 2018; Zhao et al.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Drone View

(a) Viewpoint Difference

(b) Feature Ambiguity (c) Cluster Noise

Satellite View

Satellite View Drone View Noisy Instances

Ca

Inter-view

Distance

Inter-class

Distance

Ca

**Figure 1.** Key challenges in unsupervised CVGL. (a) Drastic appearance differences between drone and satellite views. (b) Feature space ambiguity, where the distance between different views of the same category may exceed the distance within different categories. (c) An enlarged view of the clustering space of category A (Ca). Noisy instances within clusters leading to incorrect pseudo-label association. Different colors represent different categories.

2024), and contrastive learning frameworks (Cai et al. 2019; Deuser, Habel, and Oswald 2023). While achieving notable performance, such supervised methods rely extensively on large-scale manually annotated cross-view image pairs, which incur prohibitive labelling costs.

To circumvent this limitation, recent research has shifted toward unsupervised cross-view geo-localization (UCVGL). Pioneering works include Li et al. (Li, Qian, and Xia 2024), who synthesize projected ground images aligned with satellite views to generate pseudo-pairs, and self-supervised approaches (Li et al. 2024; Wang et al. 2025a) that leverage foundation models with Expectation-Maximization (EM) mechanisms and consistency regularization for pseudolabel assignment. Wang et al. (Wang et al. 2025b; Yang

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

![Figure extracted from page 1](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-001-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

et al. 2022a, 2024) further adopt clustering-based contrastive learning to extract instance- and centroid-level features without supervision.

Despite these advances, the current UCVGL paradigm performs cross-view label association directly during training, overlooking two critical limitations. As shown in Fig. 1(a-b), divergent imaging altitudes and resolutions between drone/satellite modalities cause identical categories to exhibit larger feature-space distances across views than different categories within the same view. This view distribution misalignment propagates clustering errors through erroneous label associations. Furthermore, existing UCVGL methods employ simplistic label transfer mechanisms that fail under cluster impurity. Fig. 1(c) demonstrates how noisy instances trigger catastrophic association errors when directly mapped across views.

To address these challenges, we propose UniABG, a dual-stage framework for unsupervised cross-view geolocalization. Our approach synergizes adversarial view bridging with graph-based correspondence calibration, mitigating feature-level view gaps while establishing noiserobust cross-view correspondences. Through this dual-stage design, UniABG concurrently generates high-fidelity association pairs and learns view-consistent representations, achieving significant performance gains on standard unsupervised CVGL benchmarks.

In the first stage, to bridge the inherent geometric and spectral divergence between drone and satellite views, we establish a unified embedding space via View-Aware Adversarial Bridging (VAAB). This framework deploys feature extractors that compete adversarially against a domain classifier. By deliberately confusing the classifier across all three views – drone, satellite, and an Auxiliary Pseudo View (APV) – this optimization eliminates view-specific artifacts and forces discriminative, view-invariant feature learning. The APV is generated through cross-view style transfer between existing drone/satellite data. This synthetic view preserves structural semantics while simulating perspective transitions from low-altitude drone imagery to nadir-aligned satellite views, serving as a geometric intermediary that enables progressive viewpoint adaptation.

The second stage addresses error propagation caused by distorted neighborhood graph filtering structures during early clustering. Our heterogeneous graph filtering calibration (HGFC) module constructs dual graphs encoding interview structures to achieve robust correspondence matching. Specifically, for correspondence purification, we introduce mutual k-reciprocal neighbour filtering, which requires satellite candidates to neighbour both the drone image and its APV in the heterogeneous graphs. This symmetric constraint preserves geometrically consistent pairs while eliminating ambiguous matches from noisy clusters, thereby resolving the problematic noisy instances.

In summary, our principal contributions encompass: (1) We propose the first dual-stage framework, e.g., Uni- ABG, for unsupervised cross-view geo-localization that integrates adversarial learning with graph correspondence filtering, jointly addressing the critical challenges of view discrepancy and association noise.

(2) We introduce a view-aware adversarial bridging strategy to mitigate cross-view discrepancies. This approach combines an auxiliary pseudo-view to model view-invariant embedding spaces while simultaneously enhancing crossview feature discriminability.

(3) We develop a robust correspondence calibration mechanism through heterogeneous graph construction and mutual k-reciprocal neighbour filtering, significantly enhancing matching accuracy by eliminating ambiguous cross-view associations while preserving geometrically consistent pairs.

(4) We demonstrate state-of-the-art performance on University-1652 and SUES-200 benchmarks, where our approach outperforms all existing unsupervised methods and surpasses most supervised baselines, establishing new standards for unsupervised cross-view geo-localization.

## Related Work

Supervised Cross-View Geo-localization Cross-View Geo-Localization (CVGL) is critical for tasks such as autonomous navigation and augmented reality, where large viewpoint differences between ground and aerial imagery pose significant challenges. Early works focused on global feature learning, such as CVM-Net (Tian, Chen, and Shah 2017) and spatial-aware aggregation (Shi et al. 2019), while orientation priors (Liu and Li 2019) helped reduce spatial ambiguity. Subsequent studies addressed geometric misalignment, including Optimal Feature Transport (OFT) (Shi et al. 2020) and disentangled geometric learning (Zhang et al. 2023). Recent methods emphasize semantic reasoning and attention-based models to improve robustness. Geo-Net (Zhu et al. 2021) and SemGeo (Rodrigues and Tani 2023) leverage semantic cues, while Transformer-based approaches such as Trans- Geo (Zhu, Shah, and Chen 2022) and layer-wise correlation (Yang, Lu, and Zhu 2021) enhance long-range dependencies. Other strategies incorporate part-level correlation (Wang et al. 2021) and multi-candidate matching (Zhu, Yang, and Chen 2021) to improve performance.

Unsupervised Cross-View Geo-localization The heavy reliance of supervised CVGL methods on labelled image pairs has motivated the development of unsupervised approaches. Li et al. (Li, Qian, and Xia 2024) proposed a framework that generates pseudo-labels through cross-view projection, while Li et al. (Li et al. 2024) introduced an EM-based self-supervised scheme but suffered from noisy label propagation. To alleviate such issues, Wang et al. (Wang et al. 2025b) employed clustering contrastive learning to learn cross-view representations without annotations, though it remained vulnerable to error accumulation. Building on these insights, we design a dual-stage framework that stabilizes clustering before performing cross-view association and integrates graph-based filtering to ensure contrastive supervision.

## Method

This section presents UniABG, our proposed dual-stage framework for cross-view matching (Fig. 2). In the first

<!-- Page 3 -->

View-Aware Adversarial

Bridging

UAV features

APV features

SAT features

Eq. (15)/(16)

Eq. (18)/(19)

Eq. (21)/(22) Eq. (23)

Cross-view Sample Pairs

Heterogeneous Graph Filtering

Calibration

(b) Stage2: Cross-view Association Learning

એ푪ȡ

Compute Jaccard distance

Compute Jaccard distance

Distance Matrix

Satellite

View Classifier

Drone

APV

UAV features

APV features

SAT features

Distance Matrix

Clustering

Clustering

UAV Memory

SAT Memory

Initialize

Initialize

(a) Stage1: Intra-view Pseudo-lable Generation

Eq. (8)

Eq. (9) ConvNext-Base

View Prediction ϱ∈ϱ,̊ Ϡ

CE(퐷ϱ(푓ϱ, 푡ϱ ϱ∈ϱ,̊

CE(퐷ϱ(푓ϱ, 푡ϫ

Backward path with Backbone Backward path with Classifier

Style Transfer

شǈ ش

એ풊Ɍ

Ⱥ

એ풊Ɍ ɉ

એ푰풏풇ɅȪ푪ȡ

એ푴ȯȡ

એ푪ȡ

Ʊ푅ƿ

Ʊƺƿ

Noisy Instance

Drone View

Satellite View APV View

**Figure 2.** The overall architecture of our proposed UniABG is a dual-stage model. The first stage employs adversarial learning to reduce the differences between perspectives. The second stage constructs cross-view association data through heterogeneous graph filtering calibration for supervised learning (for more details, please refer to the text).

stage, pseudo-labels are generated via clustering and optimized through intra-view contrastive learning. These pseudo-labels are further refined using view-aware adversarial learning to bridge the cross-view discrepancy. Subsequently, heterogeneous graph filtering calibration refines cross-view correspondences, effectively enhancing matching reliability. UniABG achieves state-of-the-art performance on the University-1652 and SUES-200 datasets.

Problem Formulation. In the UCVGL, given an unlabeled drone-satellite image set, denoted as {Xd, Xs}, where Xd = xd i i = 1, 2,..., N d represents the input drone image and Xs = {xs i|i = 1, 2,..., N s} represents the input satellite image. N d and N s represent the number of images in two views, respectively. The goal is to mine reliable positive and negative samples under this condition to complete the UCVGL task.

Dual-stage Unsupervised Cross-View Geo-Localization Baseline

Recent advances in cluster-based contrastive learning demonstrate significant potential for uncovering inherent data structures without labels. Building on this, we propose a dual-stage baseline for unsupervised cross-view geo- localization. Our framework employs ConvNeXt-B (Xia et al. 2024) for feature extraction and operates as follows: (1) Stage 1: Intra-view Pseudo-label Generation. Clustering methods generate pseudo-labels within each view. To optimize feature discrimination, we apply intra-view contrastive learning constrained by a dual-contrastive strategy (Yang et al. 2022b). (2) Stage 2: Cross-view Association Learning. Cross-view data associations are constructed based on cosine similarity. These associations then drive cross-view contrastive learning to align view representations.

Intra-view Pseudo-label Generation. We first construct representative feature banks (memory dictionaries) by clustering unlabeled data within each view, serving as anchors for subsequent contrastive learning. Specifically, we extract features from drone (Xd) and satellite (Xs) images using a shared backbone network Fbackbone, yielding cross-view features f d i = Fbackbone(xd i), i ∈{1, 2,..., N d}, (1)

f s i = Fbackbone(xs i), i ∈{1, 2,..., N s}, (2)

where Fd = f d i

N d i=1 and Fs = {f s i }N s i=1 represent the feature sets of two views, respectively. To discover inherent data structures without labels, we apply DBSCAN (Es-

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-36.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-37.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-38.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-46.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-53.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-54.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-55.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-003-figure-56.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

ter et al. 1996) separately on Fd and Fs to generate viewspecific pseudo-labels

ˆY d = DBSCAN(Fd), (3)

ˆY s = DBSCAN(Fs), (4)

where ˆY d = {ˆyd

1, ˆyd 2,..., ˆyd N d} and ˆY s = {ˆys

1, ˆys 2,..., ˆys N s} denote the pseudo labels of the input images Xd and Xs. Using these pseudo-labels, we compute the cluster centroids (prototypes) ϕd k for drone view and ϕs l for satellite view as the mean feature within each cluster ϕd k = 1 |Hd k|

X f d n∈Hd k f d n, ϕs l = 1 |Hs l |

X f s n∈Hs l f s n, (5)

where Hd k = f d n | ˆyd n = k is the set of drone features belonging to cluster k, Hs l = f s m | ˆys m = l is the set of satellite features belonging to cluster l, and |·| denotes set cardinality. Finally, we initialize the drone memory dictionary Md and satellite memory dictionary Ms with their respective cluster prototypes

Md ←{ϕd

1, ϕd 2, · · ·, ϕd K}, Ms ←{ϕs

1, ϕs 2, · · ·, ϕs L}.

(6) To further enhance the quality of intra-view pseudolabel generation, we employ an intra-view contrastive loss as a regularization mechanism. This approach optimizes the memory space distribution structure by reducing intramemory feature distances while increasing inter-memory separation. Given drone and satellite query features qd and qs, we compute the contrastive loss for drone view and satellite view by the following equations

Liv = Ld iv + Ls iv, (7)

Ld iv = −log exp(qd · ϕd

+/τ) PK k=0 exp(qd · ϕd k/τ)

, (8)

Ls iv = −log exp(qs · ϕs

+/τ) PL l=0 exp(qs · ϕs l /τ)

, (9)

where ϕ+ is the positive memory corresponding to the pseudo label of q and the τ is a temperature. ϕd k and ϕs l represent the view cluster center features, respectively.

Cross-view Association Learning. Following the initial feature extraction, we perform the cross-view association learning for view matching. The objective here is to establish direct correspondences between individual drone and satellite images using generated pseudo-labels for supervised contrastive learning.

Given the feature sets for the drone view, Fd = {f d i }N d i=1, and the satellite view, Fs = {f s j }N s j=1, we construct crossview associations using a greedy nearest-neighbour strategy. For each drone instance feature f d i, we compute its cosine similarity with every satellite instance feature in the set Fs. The satellite instance that yields the highest similarity is designated as the positive pair for f d i. This process identifies a corresponding satellite instance index j∗for each drone instance i j∗= argmax j∈{1,...,N s}

(f d i)⊤f s j ∥f d i ∥∥f s j ∥

!

. (10)

Once the positive drone-satellite pair (f d i, f s j∗) is identified via greedy matching (Eq. 10), all other satellite instances {f s j | j̸ = j∗} are treated as negatives for the drone query f d i. This allows us to define a cross-view contrastive learning objective: pull the positive pair closer in the embedding space while pushing negatives apart. We optimize the following supervised loss (Xia et al. 2024):

Lsup = LInfoNCE + LMSE + LCE, (11)

where LInfoNCE learns scene-discriminative features, LMSE establishes cross-view correspondences, and LCE optimizes positive sample representations. However, this approach is critically vulnerable to noise in the initial association. Greedy matching is highly susceptible to visual ambiguities, generating erroneous positive pairs. Propagating these incorrect pseudo-labels into the supervised learning framework leads to significant error accumulation, thereby fundamentally limiting model performance. This underscores the necessity of our bridging and correspondence purification strategy in UniABG, which refines pseudo-labels and enhances cross-view robustness.

View-Aware Adversarial Bridging A fundamental challenge in unsupervised cross-view geolocalization (UCVGL) stems from the significant domain gap induced by drastic perspective differences between drone and satellite imagery. This discrepancy, characterised by extreme scale variations, geometric distortions, and illumination disparities, results in substantial misalignment of feature distributions across views(Liu, Ye, and Du 2024). This misalignment is particularly detrimental in the unsupervised setting. However, naive cross-view clustering assumes cross-view feature compatibility but fails to bridge domain gaps, yielding performance-limiting noisy pseudolabels.

To explicitly mitigate this cross-view distribution divergence for robust clustering, we propose a view-aware adversarial bridging (VAAB) module. Inspired by cross-modal shared representation learning (Lin et al. 2022; Yang, Hu, and Hu 2025; Yang, Chen, and Ye 2023; Yang et al. 2023; Yang, Chen, and Ye 2024; Yao et al. 2025), VAAB employs a synthetic pseudo-view as a transitional domain with adversarial constraints. Its core mechanism uses triplet-view adversarial training to reduce view-specific characteristics, learning discriminative cross-view representations.

Auxiliary Pseudo View. Referring to (Reinhard et al. 2002; Wang et al. 2025b), we obtain the auxiliary pseudo view (APV) by performing a global color transfer from the satellite domain to the drone domain. Both images are first converted into the Lab color space, and then channelwise statistics (mean µc and standard deviation σc for c ∈ {L, a, b}) are computed. For the satellite domain, we compute the global mean and standard deviation (µs c, σs c) for

<!-- Page 5 -->

each channel c ∈{L, a, b}) over the entire dataset. For each input drone image, we compute its individual statistics (µd c, σd c) and apply the following channel-wise transformation l′ c = σs c σdc

(lc −µd c) + µs c, (12)

where lc and l′ c denote the original and transformed pixel values, and the superscripts s and d indicate satellite and drone domains, respectively. This transformation standardizes drone image appearance while preserving its structural content, forming the auxiliary pseudo view.

Adversarial View Bridging. While style transfer provides pixel-level approximation, it fails to ensure semanticlevel feature consistency across views. To achieve deeper domain invariance essential for cross-view association, we introduce an adversarial view bridging strategy. This approach transcends conventional feature alignment by explicitly harmonizing feature distributions through adversarial training. The core mechanism employs a view discriminator Dv that attempts to classify feature origins (drone xd, satellite xs, or APV xp). By adversarially training the backbone to confound Dv, we force it to suppress view-specific artefacts and extract viewpoint-invariant representations.

Formally, features from all views are extracted via shared backbone FB:

f d i = FB(xd i), f s i = FB(xs i), f p i = FB(xp i). (13) A view discriminator Dv is trained to identify perspective origins, while FB adversarially learns to induce geometric confusion – making features indistinguishable across views yet discriminative for location. This is achieved through a unified adversarial objective

LVAAB =

X v∈V,θd

CE

Dv(f v), tv

+

X v∈V,θ

CE

Dv(f v), tp

,

(14) where V = d, s, p denotes drone/satellite/APV views. Thus, td, ts, and tp are the corresponding view labels for three views. θd denotes the parameters of the view classifier and θ denotes the parameters of the backbone. This convergence emerges from complementary roles where the first item of LVAAB forces the discriminator to explore view-specific patterns, while the second drives the backbone to eliminate spectral and geometric biases. This establishes a foundation for reliable pseudo-label generation in subsequent clustering and correspondence optimization stages.

Heterogeneous Graph Filtering Calibration The quality of cross-view association data is crucial to the effectiveness of subsequent supervised training. However, traditional methods mostly rely solely on the feature similarity within a single view to perform matching. This approach is highly sensitive to noise and is prone to generating a large number of ambiguous matches, making it difficult to ensure the quality of the association data(Xu et al. 2025).

To address this, we propose a Heterogeneous Graph Filtering Calibration (HGFC) module based on the auxiliary pseudo-view. HGFC aims to construct high-quality crossview association data by exploiting the structural consensus across two complementary views: drone-to-satellite and

APV-to-satellite. Our key hypothesis is that true matching relationships should exhibit structural consistency across multiple feature manifolds, thereby effectively filtering out incorrect matches and improving the accuracy and reliability of the associations.

Heterogeneous Graph Construction. Given the extracted feature sets of drone and satellite images, denoted as Fd = {f d i } and Fs = {f s j } respectively, we compute the cosine similarity between each drone feature and all satellite features sim(f d i, f s j) = (f d i)⊤f s j ∥f d i ∥· ∥f s j ∥. (15)

Then, for each f d i, we construct its k-nearest satellite neighbors

N RU k (f d i) = Top-k f s j ∈Fs sim(f d i, f s j), (16)

which defines the edge set ERU of the Real-to-Real Graph GRU = (Fd, Fs, ERU). The edge set E is defined as the connection relationships based on feature similarity

ERU = {(f d, f s) | f s ∈Nk(f d)}. (17)

Similarly, we use the auxiliary pseudo view feature set Fp = {f p i } and compute its similarity with Fs sim(f p i, f s j) = (f p i)⊤f s j ∥f p i ∥· ∥f s j ∥, (18)

and define its neighbour set as

N P U k (f p i) = Top-k f s j ∈Fs sim(f p i, f s j), (19)

which forms the Pseudo-to-Real Graph GP U = (Fp, Fs, EP U). The edge set E is defined as the connection relationships based on feature similarity

EP U = {(f p, f s) | f s ∈Nk(f p)}. (20)

Topological Consistency Alignment. To filter out noisy matches, we align the graph structures across the two views. Specifically, we apply mutual k-nearest neighbour (mutual- KNN) verification and evaluate the consistency of neighbours between the two graphs. For a satellite feature f s j, let NRU(f s j) and NP U(f s j) denote the sets of UAV and pseudoview features that link to f s j in the respective graphs. The cross-graph consistency score is computed as scross ij = |N RU k (f s j) ∩N P U k (f s j)| k, (21)

and only satellite features with scross ij > τ are retained for reliable association.

Semantics-Guided Intra-Cluster Weighted Voting. To suppress outliers and leverage the collective evidence within each cluster, we introduce a semantically guided weighted voting mechanism that uses semantic similarity and structural confidence to refine pseudo-labels. For a candidate pair (f d i, f s j), the weighted confidence is defined as ωij = sim(f d i, f s j) · scross ij. (22)

<!-- Page 6 -->

Within each UAV cluster Ck, the final association is obtained via

ˆyi = arg max c

X f s j ∈Cc ωij, (23)

where ˆyi is the refined pseudo-label, and Cc denotes the c-th cluster of satellite features. This heterogeneous graph filtering calibration ensures that associations are not only based on appearance similarity but also structurally validated across heterogeneous views, thus significantly improving the precision of cross-view matching under unsupervised settings.

The Overall Loss Function

UniABG employs a dual-stage optimization strategy. The first stage leverages view-aware adversarial learning to reduce cross-view discrepancies and extract discriminative features, facilitating robust clustering. The stage 1 objective combines

Lstage1 = Liv + λ · LVAAB, (24)

where Liv enforces intra-view feature consistency, and LVAAB ensures cross-view domain invariance. These losses jointly learn discriminative, view-invariant representations.

Using heterogeneous graph filtering, we generate highconfidence matching pairs from the clustered view images. These purified pairs serve as supervisory signals for the second stage, optimized via supervised contrastive loss Lsup.

## Experiments

Datasets and Experimental Settings

We evaluate our method on two public cross-view geolocalization benchmarks: University-1652 (Zheng, Wei, and Yang 2020) and SUES-200 (Zhu et al. 2023) using Recall@K (R@K) and Average Precision (AP).

University-1652 (Zheng, Wei, and Yang 2020) contains 1,652 buildings from 72 universities, featuring satellite, ground, and synthetic drone views to support cross-view retrieval and navigation.

SUES-200 (Zhu et al. 2023) focuses on altitude variations, providing 24,120 drone images across four heights (150m–300m) and 200 scenes for drone-satellite matching.

Implementation Details. We implement our framework in PyTorch and conduct training on four NVIDIA RTX 4090 GPUs (24GB each). All input images are resized to 384 × 384 pixels. We adopt ConvNeXt-Base and a supervised objective as baseline (Xia et al. 2024). Both training stages use a batch size of 24 (12 drone + 12 satellite image pairs per GPU) for 5 epochs. Optimization employs AdamW with an initial learning rate of 1e−3, following a cosine decay schedule. The hyperparameter λ is fixed at 0.1.

Ablation Study

We ablate two core components: View-Aware Adversarial Bridging (VAAB) and Heterogeneous Graph Filtering Calibration (HGFC). These progressively mitigate crossview variations while enhancing association quality. Table 1 quantifies contributions under identical settings: 1) Effect

## Method

Drone →Satellite Satellite →Drone

R@1 AP R@1 AP B 35.94 41.64 65.47 35.61

B+VAAB 60.36 65.03 80.74 58.77 ↑24.42 ↑23.57 ↑15.27 ↑23.16

B+HGFC 90.83 92.85 94.57 90.87 ↑54.89 ↑51.21 ↑29.10 ↑55.26

B+HGFC+VAAB 93.62 94.61 95.43 93.29 ↑2.79 ↑1.76 ↑0.86 ↑2.42

**Table 1.** The results of ablation studies of the proposed method on the University-1652. B represents the baseline.

(a) Baseline (b) Our

**Figure 3.** The t-SNE visualization of the baseline and our proposed method. We randomly selected 50 location categories from the University-1652 dataset, with each color representing a location. “△” represents satellite features, and “◦” represents UAV features. Red circles indicate ambiguous matches.

of the HGFC: HGFC enforces structural consistency for robust associations. For Drone →Satellite, it boosts R@1 by +54.89% and AP by +51.21%. For Satellite →Drone, gains reach +29.1% R@1 and +55.26% AP. This verifies that structural filtering is essential to overcome ambiguous appearance-based matches. 2) Effect of the VAAB: VAAB reduces domain gaps through adversarial pseudo-view (APV) generation. It yields further improvements: +2.79% R@1 / +1.76% AP for Drone →Satellite and +0.86% R@1 / +2.42% AP for Satellite →Drone. This confirms that explicit view-invariant learning via APV is critical for feature robustness. 3) Visual Analysis: Fig. 3 compares t-SNE visualizations of baseline and our UniABG. Baseline features show poor clustering with incorrect matches. Our model tightly clusters cross-view features of the same class while separating different classes with distinct margins.

Comparison with the State-of-the-art Methods We evaluate our method on University-1652 and SUES-200 benchmarks. On University-1652 (Table 2), our approach advances the state-of-the-art by significant margins: +7.67% Drone →Satellite R@1 and +10.63% Satellite →Drone AP.

SUES-200 results (Table 3) further demonstrate superiority, with particularly notable gains at the challenging 150m altitude. For Drone →Satellite retrieval, we achieve +15.5% R@1 and +9.0% AP. In the Satellite →Drone direction, improvements reach +11.25% R@1 and +16.73% AP.

![Figure extracted from page 6](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-uniabg-unified-adversarial-view-bridging-and-graph-correspondence-for-unsupervis/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Method

Drone →Satellite Satellite →Drone R@1 AP R@1 AP

S

Zhen et al. (Zheng, Wei, and Yang 2020) 59.69 64.8 73.18 59.4 PCL (Tian et al. 2021) 79.47 83.63 87.69 78.51 F3-net (Sun, Liu, and Yuan 2023) 78.64 81.60 - - Sample4Geo (Deuser, Habel, and Oswald 2023) 92.65 93.81 95.14 91.39 DAC (Xia et al. 2024) 94.67 95.50 96.43 93.79 QDFL (Hu et al. 2025) 95.00 95.83 97.15 94.57

U

Li et al. (Li et al. 2024) 70.29 74.93 79.03 61.03 Wang et al. (Wang et al. 2025b) 85.95 90.33 94.01 82.66 UniABG 93.62 94.61 95.43 93.29

**Table 2.** Performance (R@1 % and AP %) comparison with SOTA methods on the University-1652 dataset. Supervised (S); Unsupervised (U). Best results are marked in bold.

Drone →Satellite

## Method

150m 200m 250m 300m R@1 AP R@1 AP R@1 AP R@1 AP

S

SUES-200 (Zhu et al. 2023) 55.65 61.92 66.78 71.55 72.00 76.43 74.05 78.26 FSRA (Dai et al. 2021) 68.25 73.45 83.00 85.99 90.68 92.27 91.95 93.46 MCCG (Shen et al. 2023) 82.22 85.47 89.38 91.41 93.82 95.04 95.07 96.20 DAC (Xia et al. 2024) 96.80 97.54 97.48 97.97 98.20 98.62 97.58 98.14 QDFL (Hu et al. 2025) 93.97 95.42 98.25 98.67 99.30 99.48 99.31 99.48

U Wang et al. (Wang et al. 2025b) 76.90 84.95 87.88 92.60 92.98 95.66 95.10 96.92 UniABG 92.40 93.95 97.32 97.92 98.07 98.55 98.67 98.98 Satellite →Drone

## Method

150m 200m 250m 300m R@1 AP R@1 AP R@1 AP R@1 AP

S

SUES-200 (Zhu et al. 2023) 75.00 55.46 85.00 66.05 86.25 69.94 88.75 74.46 FSRA (Dai et al. 2021) 83.75 76.67 90.00 85.34 93.75 90.17 95.00 92.03 MCCG (Shen et al. 2023) 97.50 93.63 98.75 96.70 98.75 98.28 98.75 98.05 DAC (Xia et al. 2024) 97.50 94.06 98.75 96.66 98.75 98.09 98.75 97.87 QDFL (Hu et al. 2025) 98.75 95.10 98.75 97.92 100.00 99.07 100.00 99.07

U Wang et al. (Wang et al. 2025b) 87.50 74.81 92.50 87.15 96.25 91.20 98.75 94.52 UniABG 98.75 91.54 98.75 97.06 100.00 98.32 98.75 97.58

**Table 3.** Performance (R@1 % and AP %) comparison with SOTA methods on the SUES-200 dataset. Supervised (S); Unsupervised (U). Best results are marked in bold.

## Conclusion

We propose UniABG, a dual-stage unsupervised framework addressing viewpoint discrepancy and association noise in cross-view geo-localization. Specifically, our approach integrates adversarial learning to align drone-satellite feature distributions, while simultaneously employing heterogeneous graph filtering to resolve ambiguous matches and suppress error propagation during association construction. Experimental results demonstrate state-of-the-art unsupervised performance on University-1652 and SUES-200 benchmarks. Crucially, UniABG establishes that combin- ing structural graph filtering with adversarial learning generates robust feature representations for label-free localization. Collectively, this work provides both an effective solution for cross-view geo-localization and a promising paradigm for future cross-modal matching research.

## Acknowledgments

This work is partially supported by National Natural Science Foundation of China under Grants (62306215, 62501428), Postdoctoral Fellowship Program of China Postdoctoral Science Foundation (GZC20241268, 2024M762479), Hubei

<!-- Page 8 -->

Postdoctoral Talent Introduction Program (2024HBB- HJD070) and Hubei Provincial Natural Science Foundation of China (2025AFB219).The numerical calculations in this paper had been supported by the super-computing system in the Supercomputing Center of Wuhan University.

## References

Cai, S.; Guo, Y.; Khan, S.; Hu, J.; and Wen, G. 2019. Ground-to-aerial image geo-localization with a hard exemplar reweighting triplet loss. In Proceedings of the IEEE/CVF international conference on computer vision, 8391–8400. Dai, M.; Hu, J.; Zhuang, J.; and Zheng, E. 2021. A transformer-based feature segmentation and region alignment method for UAV-view geo-localization. IEEE Transactions on Circuits and Systems for Video Technology, 32(7): 4376–4389. Deuser, F.; Habel, K.; and Oswald, N. 2023. Sample4geo: Hard negative sampling for cross-view geo-localisation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 16847–16856. Ester, M.; Kriegel, H.-P.; Sander, J.; Xu, X.; et al. 1996. A density-based algorithm for discovering clusters in large spatial databases with noise. In kdd, volume 96, 226–231. Hu, S.; Feng, M.; Nguyen, R. M.; and Lee, G. H. 2018. Cvm-net: Cross-view matching network for image-based ground-to-aerial geo-localization. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 7258–7267. Hu, S.; Shi, Z.; Jin, T.; and Liu, Y. 2025. Query-Driven Feature Learning for Cross-View Geo-Localization. IEEE Transactions on Geoscience and Remote Sensing, 63: 1–15. Li, G.; Qian, M.; and Xia, G.-S. 2024. Unleashing unlabeled data: A paradigm for cross-view geo-localization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 16719–16729. Li, H.; Xu, C.; Yang, W.; Yu, H.; and Xia, G.-S. 2024. Learning Cross-View Visual Geo-Localization Without Ground Truth. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–17. Lin, X.; Li, J.; Ma, Z.; Li, H.; Li, S.; Xu, K.; Lu, G.; and Zhang, D. 2022. Learning Modal-Invariant and Temporal-Memory for Video-based Visible-Infrared Person Re-Identification. In 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 20941– 20950. Liu, F.; Ye, M.; and Du, B. 2024. Learning a generalizable re-identification model from unlabelled data with domainagnostic expert. Visual Intelligence, 2(1): 28. Liu, L.; and Li, H. 2019. Lending orientation to neural networks for cross-view geo-localization. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 5624–5633. Regmi, K.; and Shah, M. 2019. Bridging the domain gap for ground-to-aerial image matching. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 470–479.

Reinhard, E.; Adhikhmin, M.; Gooch, B.; and Shirley, P. 2002. Color transfer between images. IEEE Computer graphics and applications, 21(5): 34–41. Rodrigues, R.; and Tani, M. 2023. Semgeo: Semantic keywords for cross-view image geo-localization. In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 1–5. IEEE. Shen, T.; Wei, Y.; Kang, L.; Wan, S.; and Yang, Y.-H. 2023. MCCG: A ConvNeXt-based multiple-classifier method for cross-view geo-localization. IEEE Transactions on Circuits and Systems for Video Technology, 34(3): 1456–1468. Shi, Y.; Liu, L.; Yu, X.; and Li, H. 2019. Spatialaware feature aggregation for cross-view image based geolocalization. In Proceedings of the 33rd Annual Conference on Neural Information Processing Systems, NeurIPS 2019, 10090–10100. Shi, Y.; Yu, X.; Liu, L.; Zhang, T.; and Li, H. 2020. Optimal feature transport for cross-view image geo-localization. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 34, 11990–11997. Sun, B.; Liu, G.; and Yuan, Y. 2023. F3-Net: Multiview scene matching for drone-based geo-localization. IEEE Transactions on Geoscience and Remote Sensing, 61: 1–11. Tian, X.; Shao, J.; Ouyang, D.; and Shen, H. T. 2021. UAVsatellite view synthesis for cross-view geo-localization. IEEE Transactions on Circuits and Systems for Video Technology, 32(7): 4804–4815. Tian, Y.; Chen, C.; and Shah, M. 2017. Cross-view image matching for geo-localization in urban environments. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 3608–3616. Wang, T.; Zheng, Z.; Yan, C.; Zhang, J.; Sun, Y.; Zheng, B.; and Yang, Y. 2021. Each part matters: Local patterns facilitate cross-view geo-localization. IEEE Transactions on Circuits and Systems for Video Technology, 32(2): 867–879. Wang, X.; Liu, L.; Yang, B.; Ye, M.; Wang, Z.; and Xu, X. 2025a. TokenMatcher: Diverse Tokens Matching for Unsupervised Visible-Infrared Person Re-Identification. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 7934–7942. Wang, X.; Zhang, L.; Fan, Z.; Liu, Y.; Chen, C.; and Deng, F. 2025b. From Coarse to Fine: A Matching and Alignment Framework for Unsupervised Cross-View Geo- Localization. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 8024–8032. Xia, P.; Wan, Y.; Zheng, Z.; Zhang, Y.; and Deng, J. 2024. Enhancing Cross-View Geo-Localization With Domain Alignment and Scene Consistency. IEEE Transactions on Circuits and Systems for Video Technology, 34(12): 13271–13281. Xu, Y.; Wu, M.; Guo, Z.; Cao, M.; Ye, M.; and Laaksonen, J. 2025. Efficient text-to-video retrieval via multi-modal multitagger derived pre-screening. Visual Intelligence, 3(1): 1– 13. Yang, B.; Chen, J.; Chen, C.; and Ye, M. 2024. Dual Consistency-Constrained Learning for Unsupervised

<!-- Page 9 -->

Visible-Infrared Person Re-Identification. IEEE Transactions on Information Forensics and Security, 19: 1767–1779. Yang, B.; Chen, J.; Ma, X.; and Ye, M. 2023. Translation, Association and Augmentation: Learning Cross-Modality Re-Identification From Single-Modality Annotation. IEEE Transactions on Image Processing, 32: 5099–5113. Yang, B.; Chen, J.; and Ye, M. 2023. Towards Grand Unified Representation Learning for Unsupervised Visible- Infrared Person Re-Identification. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 11069–11079. Yang, B.; Chen, J.; and Ye, M. 2024. Shallow-Deep Collaborative Learning for Unsupervised Visible-Infrared Person Re-Identification. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 16870– 16879. Yang, B.; Ye, M.; Chen, J.; and Wu, Z. 2022a. Augmented Dual-Contrastive Aggregation Learning for Unsupervised Visible-Infrared Person Re-Identification. In ACM MM, 2843–2851. Yang, B.; Ye, M.; Chen, J.; and Wu, Z. 2022b. Augmented dual-contrastive aggregation learning for unsupervised visible-infrared person re-identification. In Proceedings of the 30th ACM International Conference on Multimedia, 2843–2851. Yang, H.; Lu, X.; and Zhu, Y. 2021. Cross-view geolocalization with layer-to-layer transformer. Advances in Neural Information Processing Systems, 34: 29009–29020. Yang, Y.; Hu, W.; and Hu, H. 2025. Progressive Cross- Modal Association Learning for Unsupervised Visible- Infrared Person Re-Identification. IEEE Transactions on Information Forensics and Security, 20: 1290–1304. Yao, H.; Yang, B.; Huang, W.; Du, B.; and Ye, M. 2025. Unsupervised Visible-Infrared Person Re-identification under Unpaired Settings. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 11916–11926. Zhang, X.; Li, X.; Sultani, W.; Zhou, Y.; and Wshah, S. 2023. Cross-view geo-localization via learning disentangled geometric layout correspondence. In Proceedings of the AAAI conference on artificial intelligence, volume 37, 3480–3488. Zhao, H.; Ren, K.; Yue, T.; Zhang, C.; and Yuan, S. 2024. TransFG: A cross-view geo-localization of satellite and UAVs imagery pipeline using transformer-based feature aggregation and gradient guidance. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–12. Zheng, Z.; Wei, Y.; and Yang, Y. 2020. University-1652: A multi-view multi-source benchmark for drone-based geolocalization. In Proceedings of the 28th ACM international conference on Multimedia, 1395–1403. Zhu, R.; Yin, L.; Yang, M.; Wu, F.; Yang, Y.; and Hu, W. 2023. SUES-200: A multi-height multi-scene cross-view image benchmark across drone and satellite. IEEE Transactions on Circuits and Systems for Video Technology, 33(9): 4825–4839.

Zhu, S.; Shah, M.; and Chen, C. 2022. Transgeo: Transformer is all you need for cross-view image geo-localization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1162–1171. Zhu, S.; Yang, T.; and Chen, C. 2021. Vigor: Cross-view image geo-localization beyond one-to-one retrieval. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 3640–3649. Zhu, Y.; Sun, B.; Lu, X.; and Jia, S. 2021. Geographic semantic network for cross-view image geo-localization. IEEE Transactions on Geoscience and Remote Sensing, 60: 1–15.
