---
title: "Modality-free Graph In-context Alignment"
source_url: https://iclr.cc/virtual/2026/oral/10008532
paper_pdf_url: https://arxiv.org/pdf/2603.13434v1
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Modality-free Graph In-context Alignment

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

MODALITY-FREE GRAPH IN-CONTEXT ALIGNMENT

Wei Zhuo, Siqiang Luo Nanyang Technological University {wei.zhuo, siqiang.luo}@ntu.edu.sg

## ABSTRACT

In-context learning (ICL) converts static encoders into task-conditioned reasoners, enabling adaptation to new data from just a few examples without updating pretrained parameters. This capability is essential for graph foundation models (GFMs) to approach LLM-level generality. Yet current GFMs struggle with crossdomain alignment, typically relying on modality-specific encoders that fail when graphs are pre-vectorized or raw data is inaccessible. In this paper, we introduce Modality-Free Graph In-context Alignment (MF-GIA), a framework that makes a pretrained graph encoder promptable for few-shot prediction across heterogeneous domains without modality assumptions. MF-GIA captures domain characteristics through gradient fingerprints, which parameterize lightweight transformations that align pre-encoded features and indexed labels into unified semantic spaces. During pretraining, a dual prompt-aware attention mechanism with episodic objective learns to match queries against aligned support examples to establish prompt-based reasoning capabilities. At inference, MF-GIA performs parameter-update-free adaptation using only a few-shot support set to trigger cross-domain alignment and enable immediate prediction on unseen domains. Experiments demonstrate that MF-GIA achieves superior few-shot performance across diverse graph domains and strong generalization to unseen domains. The code is available at https://github.com/JhuoW/MF-GIA.

## INTRODUCTION

**Table 1.** Comparison of methods with respect to the three main criteria of true ICL.

## Method

Post-Training Free Domain Alignment Modality-Free

SSL-GNN ✗ ✗ ✓ All in One (Sun et al., 2023) ✗ ✗ ✓ GPF (Fang et al., 2023) ✓ ✗ ✓ GCOPE (Zhao et al., 2024) ✗ ✓ ✓ GFT (Wang et al., 2024b) ✗ ✓ ✗ Prodigy (Huang et al., 2023) ✓ ✗ ✓ Unigraph (He et al., 2025a) ✓ ✓ ✗ AutoGFM (Chen et al., 2025) ✗ ✓ ✗ GraphAlign (Hou et al., 2024) ✓ ✓ ✗ OFA (Liu et al., 2024a) ✓ ✓ ✗ GOFA (Kong et al., 2025) ✓ ✓ ✗

MF-GIA ✓ ✓ ✓

The remarkable success of Large Language Models (LLMs) has fundamentally revolutionized AI, with in-context learning (Brown et al., 2020; Zhang et al., 2023; Lu et al., 2022) emerging as a pivotal capability that enables these models to adapt to new tasks through mere exposure to a few demonstration examples, without any parameter updates like fine-tuning. This paradigm shift, from task-specific fine-tuning to prompt-based adaptation, naturally sparks a profound question for the graph learning community: Can we achieve similar foundation-level generality for graph-structured data? Unlike sequential text where context flows naturally, graphs encode complex topological patterns, multihop dependencies, and heterogeneous node and edge attributions that demand fundamentally new approaches to demonstration selection, prompt design, and reasoning.

Achieving true graph in-context learning demands three fundamental criteria that remain elusive in existing methods. First, post-training-free inference is essential for genuine ICL, where models must adapt to new tasks through demonstrations alone, without fine-tuning or learnable prompt engineering. Second, cross-domain alignment enables a single model to reason across diverse graph types within a unified semantic space, mirroring LLMs’ domain-agnostic capabilities. Third, modality-free operation ensures that the model can process arbitrary pre-encoded graphs without requesting raw data, crucial for the heterogeneous domains of real-world graphs. As shown in Table 1, prior approaches fall short of meeting all three criteria at once: self-supervised GNNs (You et al., 2020; Qiu et al., 2020) and GFMs like All in One (Sun et al., 2023), GCOPE (Zhao et al., arXiv:2603.13434v1 [cs.LG] 13 Mar 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026

2024), and GFT (Wang et al., 2024b) compromise ICL through required post-training on downstream graphs, where All in One trains task-specific prompts while GCOPE and GFT require fine-tuning; GPF (Fang et al., 2023) and Prodigy (Huang et al., 2023) lack cross-domain alignment, limiting their generalization on graphs from unseen domains; recent advances like UniGraph (He et al., 2025a), GraphAlign (Hou et al., 2024), and OFA (Liu et al., 2024a) achieve alignment and post-training-free inference, yet sacrifice modality freedom by requiring conversion to a single unified modality (e.g., text-attributed graphs) for alignment, making them inapplicable when raw data are inaccessible or when graphs are already pre-encoded by domain-specific pipelines. More related work is discussed in Appendix A.

In this work, we present Modality-free Graph In-context Alignment (MF-GIA), the first GFM to achieve all three criteria for true in-context learning on graphs. Our key insight is that the interaction between a graph and a shared frozen encoder reveals its domain characteristics, which can be captured by a gradient fingerprint: a single-step parameter update that encodes how features, labels, and structure jointly influence the model. This fingerprint drives lightweight domain-conditioned transformations that align pre-encoded features and graph-local label IDs into unified semantic spaces, where related domains occupy neighboring subspaces while preserving intra-domain geometry, thereby achieving modality-free domain alignment. The aligned features and labels are then processed by Dual Prompt-Aware Attention (DPAA) optimized with an episodic objective that learns to match queries against support examples. This approach establishes prompt-based in-context reasoning that simulates the few-shot scenarios faced at test time. At inference, given a few labeled examples as prompts, MF-GIA computes the fingerprint, instantiates the aligners, and performs parameterupdate-free prediction on unseen domains. Experiments across diverse benchmarks demonstrate that MF-GIA excels at few-shot node-level tasks, generalizes to entirely unseen domains without additional training, and transfers seamlessly to edge-level tasks. These results bring GFMs closer to the universal in-context learning capabilities exhibited by LLMs.

PRELIMINARIES

Following the ICL setup of the pioneering work Prodigy (Huang et al., 2023), we study few-shot, prompt-based node and edge classification. In this section, we formalize graph ICL as episodic classification over graphs and introduce a modality-free alignment perspective that standardizes features and labels across domains.

## 2.1 GRAPH IN-CONTEXT LEARNING

Let G = {G1, G2, · · ·, GM} denote a collection of M graphs drawn from heterogeneous domains, where each graph Gi = (Vi, Ei, Xi, Yi) comprises a node set Vi, an edge set Ei ⊆Vi × Vi, node features Xi = {xi,1, · · ·, xi,|Vi|} ∈R|Vi|×di, and labels Yi. The node features Xi may exist in domain-specific formats (e.g., dense vectors, categorical attributes, IDs), with potentially different dimensions di. To pretrain a universal model across these graphs with a common input width, following (Yu et al., 2025; Zhao et al., 2024), we first unify feature dimensions to do by applying SVD on each Xi ←SVD(Xi) ∈R|Vi|×do. Depending on the task, Yi is either a node-label vector Ynode i = {0, 1, · · ·, Cnode i −1}|Vi| or an edge-label vector Yedge i = {0, 1, · · ·, Cedge i −1}|Ei|, where Cnode i and Cedge i denote the number of node and edge classes in Gi, respectively. A universal GNN encoder fθ: Rdo →Rd maps graph items (nodes or edges) to d-dimensional representations. For node classification, the representation of v ∈Vi is hi,v = fθ(v; Gi) ∈Rd. For edge classification, we analogously obtain hi,e = fθ(e; Gi) for e ∈Ei using endpoint features and structure as needed. We use the generic symbol w to denote an item (w = v or w = e).

Given G as a pretraining corpus with M graphs and a target graph Gnew = (Vnew, Enew, Xnew, Ynew) from an unseen domain with Cnew classes, graph in-context learning aims to classify graph items in Gnew using a few labeled examples per class as in-context demonstrations, without updating model parameters. Formally, the graph ICL operates in two phases. During pretraining, we learn a unified model MΦ: G →Y on the corpus G. At test time, given a support set S = {(wj, yj)}k·Cnew j=1 containing k labeled graph items per class from Gnew as prompts, the model predicts labels for query items Q = {q: q ∈Gnew\S} as:

ˆyq = MΦ (q, Gnew, S), ∀q ∈Q, (1)

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

Unified Space

Modality-free Alignment

Citation Citation Social

Related Unrelated

Domain Space

Domain-Conditioned

Transformations

Episodic Pre-training

GNN

Domain-aligned

Features

In-Context Prediction

Episode Meta Learning

Domain-aligned

Labels

Prompt Query

… … m-way k-shot DPAA

GNN

DPAA

Modality-free Alignment

Prompt

Query

Prediction

Trainable

Frozen

**Figure 1.** Overview of MF-GIA. (Left) Modality-free Alignment: The pretraining graphs are mapped to a unified space via domain-conditioned transformations. Domain descriptors e ensure similar domains occupy neighboring subspaces. (Middle) Episodic Pretraining: The model learns from m-way k-shot episodes using domain-aligned features and labels. The DPAA mechanism matches queries to classes using only prompts as context. (Right) In-context Prediction: For an unseen graph, the frozen model performs few-shot classification using the support set as a prompt.

where the pretrained model MΦ is parameterized by Φ. Crucially, Φ remains frozen during inference, so the model leverages the in-context demonstrations in S to adapt to the new domain without fine-tuning. For example, consider MΦ pretrained on citation and E-commerce networks. When tested on a social network Gnew from an unseen domain, the model can classify users in Gnew without fine-tuning. Instead, we provide a support set containing a few labeled users from each class. By leveraging these in-context demonstrations as prompts, MΦ identifies patterns between the support examples and query users to classify the remaining users, all while keeping its parameters frozen.

Episodic Meta Learning. To enable in-context adaptation, we adopt an episodic training paradigm (Vinyals et al., 2016; Li et al., 2019). Specifically, for each pretraining graph Gi ∈G, we construct m-way k-shot episodes by sampling m classes and k examples per class as a support set S, with additional samples as queries Q. The model MΦ consumes (Gi, S) as the prompt and is optimized to maximize the likelihood of the ground-truth labels on Q:

min

Φ E[−1

|Q|

X q∈Q log ˆp (yq | q, S, Gi)]. (2)

This episodic formulation teaches the model to recognize patterns from limited examples. By pretraining on numerous episodes that simulate the few-shot scenarios encountered at test time, the model acquires the capacity to perform in-context reasoning. At inference, this enables adaptation to new domains through few-shot prompts alone, with all pretrained parameters Φ remaining frozen.

## 2.2 MODALITY-FREE ALIGNMENT

The pretraining graphs in G often differ in both input modalities and label systems. Features range from dense vectors to categorical attributes or domain-specific identifiers. Likewise, label spaces are graph-local and vary in cardinality, with no global alignment across domains. These heterogeneities make direct in-context transfer across graphs challenging.

Recent GFMs (Wang et al., 2024b; He et al., 2025a; Liu et al., 2024a) attempt to unify graphs from heterogeneous domains with Text-Attributed Graphs (TAGs), which convert all features and labels to natural language, then map them with language models into shared semantic spaces. However, this approach has fundamental limitations. Real-world graph data is typically already vectorized through domain-specific methods, such as word2vec (Mikolov et al., 2013) for documents, molecular

<!-- Page 4 -->

Published as a conference paper at ICLR 2026 fingerprints (Rogers & Hahn, 2010) for compounds, and user behavior embeddings (Pan & Ding, 2019). Converting these optimized representations to text and back introduces information loss and computational overhead. Furthermore, privacy constraints often restrict access to raw data, and data providers usually release only pre-encoded datasets, making modality-aware conversions infeasible in sensitive domains. Instead, we adopt a modality-free alignment perspective, which aligns graphs directly in their existing representations without modality-aware conversion.

Definition 1. (Modality-free Alignment) Let {(Gi, Li)}M i=1 be graphs from M domains, whose item features are already pre-encoded by (unknown) domain-specific pipelines, Xi ∈Rdo, and whose labels have been indexed by Li = {0, · · ·, Ci −1}. A modality-free alignment is a domain- conditioned transformation system T = n

(Kfeat i, Klabel i)

oM i=1 with:

Kfeat i: Rdo →Rd (feature alignment) and Klabel i: Li →Rd (label alignment) (3)

that maps domain-specific features and label IDs directly into a unified d-dimensional feature space and label space, respectively, without reconstructing or converting to any intermediate modality. The transformations should be conditioned on the domain descriptors ei ∈Rde that capture domain characteristics of Gi, such that for any two domain i, j,

∥Kfeat i −Kfeat j ∥∝∥ei −ej∥ and ∥Klabel i −Klabel j ∥∝∥ei −ej∥. (4)

This ensures that similar domains with close descriptors ei ≈ej produce similar transformations, causing their aligned features and labels to occupy neighboring subspaces in the unified space.

Fig. 1-left illustrates the idea intuitively. Modality-free alignment maps every graph into a unified semantic space according to domain relationships: graphs from related domains (e.g., two citation networks G1 and G2) have similar domain descriptors and thus map to neighboring subspaces, whereas unrelated domains (social network G3) sit far away. The domain-conditioned transformations Kfeat i and Klabel i project each graph’s pre-encoded features and indexed labels into unified feature and label spaces, preserving intra-domain semantics while enabling cross-domain transfer. This is essential because numerically similar feature vectors from different domains can carry entirely different meanings (each domain’s encoder defines its own coordinate system), and indexed label IDs [0, 1, 2, · · · ] are reused with domain-specific semantics. Modality-free alignment reconciles these differences by calibrating features and labels via the domain descriptor, unifying them in shared spaces without requiring any knowledge of the original data modality like TAGs.

## 3 MF-GIA: MODALITY-FREE GRAPH IN-CONTEXT ALIGNMENT

In this section, we present MF-GIA for enabling in-context learning across heterogeneous graph domains without modality-specific priors. MF-GIA addresses the fundamental challenge of aligning graphs with incompatible feature spaces and label systems through three key components: (1) domain embedder encodes domain characteristics, (2) domain-conditioned alignment maps pre-encoded features and indexed labels to unified spaces, and (3) episodic pretraining realizes few-shot adaptation during pretraining. We then describe in-context inference on graphs from unseen domains.

## 3.1 DOMAIN EMBEDDER

one gradient step

**Figure 2.** Domain embedder.

Reliable domain embeddings are the pivot of MF-GIA: they summarize graphs’ domain characteristics, parameterize the domain-conditioned aligners (Kfeat i, Klabel i), and ensure that graphs with related domains are mapped to neighboring subspaces while preserving intra-/cross- domain semantics. Prior work represents graph domains using learnable tokens, but depends on external signals, such as domain labels (Yu et al., 2025) or modality metadata (He et al., 2025a), which are often unavailable in practice. We instead induce the domain embeddings {ei}M i=1 directly from each graph’s intrinsic properties by capturing the interactions between the graph and a shared encoder, without external signals. Starting from a single shared weight initialization θ0 ∈Rdo×d for a one-layer GNN encoder followed by a fixed all-ones projection matrix 1d×Ci from embedding to label space as shown

<!-- Page 5 -->

Published as a conference paper at ICLR 2026 in Fig. 2, we take a single gradient step on each pretraining graph Gi ∈G as θi = θ0 −η∇θLi (θ0), where η is a small learning rate uniformly set to 0.01 and Li is the task loss w.r.t. the available labels on Gi. The resulting single-step displacement ∆θi = θi −θ0 serves as a gradient fingerprint that captures how the graph’s features, labels, and structure jointly influence the shared encoder. Intuitively, graphs with similar gradient patterns are likely to come from related domains, making ∆θi a natural descriptor of domain-level information. To obtain compact domain embeddings, we project these fingerprints through a learnable domain embedder fϕde: Rdo×d →Rde:

ei = fϕde (∆θi) = MLP (Flatten (Conv2D (∆θi))) ∈Rde, (5)

where the fingerprint ∆θi ∈Rdo×d is treated as a single-channel image to be embedded. The embedder fϕde is trained to preserve domain relationships by minimizing:

Lde =

X

Gi,Gj∈G

∥∆θi −∆θj∥F −∥ei −ej∥2

2, (6)

so that pairwise relationships among graphs are retained in the embedding space. This approach naturally captures domain characteristics without domain labels or modality priors, as the gradient pattern inherently reflects the unique way each domain’s data distribution interacts with the shared model initialization.

The domain embedding induced by the gradient fingerprint is central to MF-GIA, and the subsequent alignment operations are established on it. To justify its effectiveness, we provide a theoretical analysis showing that this embedding faithfully preserves domain characteristics (Proof in Appendix B.1).

Theorem 3.1. Let Gi and Gj be graphs sampled from domains Di and Dj respectively, with corresponding gradient fingerprints ∆θi, ∆θj ∈Rdo×d computed using task loss Li and Lj (e.g., cross-entropy). The domain embedder fϕde produces domain embeddings ei and ej. Assuming every task loss L is Ltask-smooth with respect to model parameters, and fϕde has Lipschitz constant Lde, the domain embeddings preserve domain relationships:

∥ei −ej∥2 ≤eC · W2 (Di, Dj) (7)

where W2(·, ·) measures inherent distance between two domains, and eC is a constant.

This upper bound ensures that if two domains are inherently similar, their embeddings learned by fϕde will be close in the embedding space, while dissimilar domains produce distant embeddings.

In-context Domain Embedding. For a downstream graph Gnew from an unseen domain, we compute its domain embedding using the same fingerprinting process. Given a few labeled items S = {(wi, yi)}k·Cnew i=1 as a Cnew-way k-shot prompt from Gnew, we perform a single gradient step from the same initialization θ0, which is a component of the pretraining model M (θ0 ∈Φ), as θnew = θ0 −η∇θLnew(θ0, S), where Lnew is computed using only the prompt S. The in-context domain embedding of Gnew is then computed by passing the gradient fingerprint through the pretrained domain embedder:

enew = fϕde (θnew −θ0). (8)

This process automatically captures Gnew’s characteristics and positions it within the learned domain space. Since the domain embedder fϕde has been trained to preserve domain relationships during pretraining, it naturally maps the new graph’s fingerprint to an appropriate location based on the knowledge learned from existing domains.

## 3.2 DOMAIN-CONDITIONED ALIGNMENT

With the domain embedding ei for Gi ∈G, MF-GIA instantiates two lightweight transformations (Kfeat i, Klabel i) as aligners that respectively align Gi’s item features and graph-local label IDs into unified semantic spaces. Because the transformations are conditioned on ei, related domains with nearby ei induce similar transformations and occupy neighboring subspaces after alignment, while dissimilar domains remain separated. Here, we detail the feature and label alignment mechanisms and their application during in-context inference.

<!-- Page 6 -->

Published as a conference paper at ICLR 2026

## 3.2.1 FEATURE ALIGNMENT

For each pretraining graph Gi, we learn a domain-conditioned feature transformation Kfeat i mapping pre-encoded item features to a unified feature space. Given an item w ∈Gi with its feature xw ∈Rdo, we first obtain its base representation via a shared GNN encoder fθ, whose first-layer weight matrix is initialized from the stored θ0:

hi,w = fθ(w, Gi) ∈Rd. (9)

Then we apply Feature-wise Linear Modulation (FiLM) (Perez et al., 2018) to generate domainconditioned transformations from the domain embedding:

γfeat i, βfeat i

= fϕfeat (ei), γfeat i, βfeat i ∈Rd, zi,w = Kfeat i (hi,w) = γfeat i ⊙hi,w + βfeat i,

(10)

where fϕfeat: Rde →R2d is a two-layer MLP that outputs scale γfeat i (with SoftPlus head for positivity) and shift βfeat i parameters, ⊙denotes element-wise product, and zi,w is the aligned feature for w in Gi. The FiLM-based transformation Kfeat i is affine, so it calibrates scales and offset across domains to map features to a domain-specific subspace determined by ei, while preserving the intradomain geometry already present in hi,w. Formally, the alignment satisfies (Proof in Appendix B.2):

Property 1. If fϕfeat is L -Lipschitz continuous, then ∥γfeat i −γfeat j ∥2+∥βfeat i −βfeat j ∥2 ≤L ∥ei−ej∥2 for two graph Gi and Gj, so nearby domains yield similar feature transforms and thus neighboring subspaces in the unified feature space.

The domain-conditioned transformations {Kfeat i }M i=1 parameterized by shared ϕfeat, are learned jointly over all pre-training graphs G using their domain embeddings {ei}M i=1 to form a unified and general feature space. Together with the GNN encoder fθ, they constitute part of the pretrained model M (i.e., θ, ϕfeat ∈Φ).

In-context Feature Alignment. At test time, for a downstream graph Gnew with domain embedding enew computed via the pretrained domain embedder, we generate its alignment parameters (γfeat new, βfeat new) = fϕfeat(enew). For any item w ∈Gnew, its aligned feature is computed as:

znew,w = γfeat new ⊙fθ(w, Gnew) + βfeat new. (11)

## 3.2.2 LABEL ALIGNMENT Domain-agnostic Domain-specific Label Distributions

**Figure 3.** Domain-conditioned label alignment.

Different graphs have their own label systems, leading to label IDs across domains having inconsistent semantics, such as label ID 0 representing different concepts across graphs. To reconcile graph-local label systems, we maintain a shared label base Elabel ∈RLmax×d with Lmax = maxi Ci, where each row Elabel l serves as a domain-agnostic label prototype for ID l, initialized as Elabel l ∼N(0, Id). Given domain embedding ei of Gi, we instantiate a domain-conditioned label transformation with FiLM, architecturally identical to the feature-side transformation, that maps ei to scale and shift parameters for label alignment:

γlabel i, βlabel i

= fϕlabel (ei), γlabel i, βlabel i ∈Rd, ui,l = Klabel i (El) = γlabel i ⊙Elabel l + βlabel i, l ∈Li = {0, · · ·, Ci −1},

(12)

where fϕlabel: Rd →R2d is a two-layer MLP with a SoftPlus for γlabel i. ui,l is the aligned label embeddings conditioned on ei for label l. As illustrated in Fig. 3, this mechanism transforms a single domain-agnostic distribution into domain-specific label distributions. The shared base Elabel provides a common reference, while FiLM parameters shift and scale these prototypes based on domain characteristics, ensuring semantically distinct labels occupy different subspaces in a unified label space even when sharing the same ID. fϕlabel is a component of the pretrained model M (ϕlabel ∈Φ).

<!-- Page 7 -->

Published as a conference paper at ICLR 2026

In-context Label Alignment. For a new graph Gnew with Cnew classes, we compute label alignments using the pretrained transformation (γlabel new, βlabel new) = fϕlabel(enew). The aligned label embeddings for Gnew are:

unew,l = γlabel new ⊙Elabel l + βlabel new, l ∈{0,..., Cnew −1} (13)

which yields domain-aware label prototypes that are compatible with the unified feature space and ready for few-shot matching.

## 3.3 EPISODIC PRETRAINING

MF-GIA is pretrained with an episodic, prompt-based objective that teaches the model to match aligned item features to aligned label prototypes, mimicking the few-shot scenarios encountered during inference.

For each pretraining graph Gi ∈G, we construct m-way k-shot episodes to simulate in-context learning scenarios. Specifically, in each episode, we select m classes and sample k labeled items per class to form a support set S = Sm c=1 n w(c)

j, l(c) ok j=1, where w(c)

j is the j-th item of the c-th selected class and l(c) = yj is its label ID. We also sample T items per class for the query set

Q = Sm c=1 n q(c)

t, l(c)oT t=1. Using the domain embedding ei, we compute aligned item features with

Eq. (10) and aligned label prototypes with Eq. (12), yielding zi,w(c)

j = Kfeat i hi,w(c)

j

, zi,q(c)

t =

Kfeat i hi,q(c)

t

, and ui,l(c) = Klabel i

Elabel l(c)

. The prompt-query pairs become:

Prompt S:

n zi,w(c)

j, ui,l(c)

o c∈[m],j∈[k], Query Q:

n zi,q(c)

t o c∈[m],t∈[T ]. (14)

Recalling the episodic meta learning objective in Eq. (2), which requires matching queries to classes using only the prompt, we propose a Dual Prompt-Aware Attention (DPAA) mechanism. It allows queries to attend to prompt examples but prevents prompts from interacting with each other, strictly following the principle of in-context learning. Specifically, let Zpmt = h zi,w(1)

1, · · ·, zi,w(m) k i

∈

Rmk×d be the matrix of row-stacked support features and Upmt = ui,l(1), · · ·, ui,l(m)

∈Rm×d be the label prototype matrix. DPAA consists of two single-query attention layers, one feature-side and one label-side, both sharing the same projection matrices WK, WV ∈Rd×d. For an aligned query feature zi,q ∈Q from Gi, the feature-side attention computes:

Kfeat = ZpmtWK, Vfeat = ZpmtWV, Qfeat = zi,qWQ, zout i,q = softmax

Qfeat(Kfeat)⊤

√ d

Vfeat,

(15)

where the attended representation zout i,q aggregates features from prompt examples relevant to the query. In other words, Eq. (15) aims to use the support features Zpmt to prompt the query feature zi,q, producing the prompt-conditioned feature zout i,q for the query. zout i,q is then projected to label space via a learnable function fΩ: Rd →Rd, which is also prompted by the support set. Thus, the label-side attention lets the query interact with label prototypes:

Klabel = UpmtWK, Vlabel = UpmtWV, Qlabel = fΩ(zout i,q), uout i,q = softmax

Qlabel(Klabel)⊤

√ d

Vlabel,

(16)

Analogous to LLMs, where prompt examples guide task completion, here (Zpmt, Upmt) serves as the few-shot demonstrations, zi,q as the query to be answered, and zout i,q as the prompt-conditioned intermediate, and uout i,q as the answer produced from the prompt for the task objective zi,q. Thus, the pretraining objective is to build the matching between uout i,q and the ground-truth label. The final prediction is obtained by scoring the query’s prompted representation against all label prototypes:

si,q = uout i,q(Upmt)⊤∈Rm, (17)

<!-- Page 8 -->

Published as a conference paper at ICLR 2026 where si,q contains the per-class scores for the query item q. For each episode from Gi, we minimize the cross-entropy loss over all queries in Q:

Lepisode(Gi) = −1 mT m X c=1

T X t=1 log exp si,q(c)

t [c]/τ

Pm j=1 exp si,q(c)

t [j]/τ

, (18)

where τ > 0 is a temperature that controls the sharpness of the softmax, si,q(c)

t [c] denotes the score of the ground-truth class for the query q(c)

t. The complete pretraining loss aggregates episodes across all pretraining graphs:

Lpretrain = EGi∼GEepisode∼Gi [Lepisode(Gi)]. (19)

Note that the domain embedder fϕde is optimized with Lde prior to episodic pretraining and then kept fixed. Overall, the pretraining model MΦ comprises the frozen encoder initialization fθ0, the domain embedder fϕde, the domain-conditioned transformation fϕfeat and fϕlabel, the DPAA projection matrices and the projection head fΩ. This episodic regime trains the model to leverage prompt examples for prediction, establishing the feature-label matching capability essential for ICL on unseen domains.

## 3.4 IN-CONTEXT PREDICTION ON UNSEEN DOMAINS

At test time, MF-GIA freezes all pretrained parameters. Given an unseen graph Gnew together with a Cnew-way k-shot support set S = {(wi, yi)}k·Cnew i=1 as prompts, we compute the in-context domain embedding enew using the gradient fingerprint and the pretrained domain embedder described in Section 3.1. With the pretrained domain-conditioned transformations, any item w ∈Gnew is mapped to its aligned feature znew,w via Eq. (11). For label IDs l ∈Lnew = {0, · · ·, Cnew −1}, the aligned label prototypes are {unew,l}l∈Lnew obtained by Eq. (13). We then form the prompt matrices Zpmt new = h znew,w(1)

1,..., znew,w(Cnew) k i

∈R(kCnew)×d and Upmt new = unew,l(1),..., unew,l(Cnew)

∈RCnew×d. To make a prediction on a query item q, we apply the pretrained DPAA on it. Specifically, the featureside attention produces the prompt-conditioned feature zout new,q by Eq. (15), which is then fed to the label-side attention Eq. (16) to yield uout new,q. The final scores and prediction are:

snew,q = uout new,q

Upmt new

⊤∈RCnew,

ˆyq = arg max j∈[Cnew] snew,q[j]. (20)

This inference procedure is parameter-update-free w.r.t. the pretrained model M, and the same pipeline applies to node or edge items by letting w range over Vnew or Enew. The detailed algorithms and complexity analysis of MF-GIA are provided in Appendix C.

To fully exploit the sparse few-shot support labels and the topology of Gnew during inference, we further enhance prototype construction and prediction refinement beyond DPAA. Specifically, we construct graph-aware class prototypes by propagating soft label distributions initialized from the support set through the graph structure using label propagation, which enriches the prototypes with neighborhood context to compensate for the sparsity of the k-shot support. For query classification, we employ an adaptive distance metric that combines cosine similarity and inverse Euclidean distance, weighted per query by σ(Var(znew,q)), enabling the metric to adapt to local feature geometry. Finally, predictions are iteratively refined through semi-supervised label propagation, where query pseudolabels are updated by blending propagated and current distributions while keeping support labels fixed, enforcing graph-level consistency in the final output.

## 4 EXPERIMENTS

## 4.1 EXPERIMENTAL SETUP

We employ cross-domain graph datasets to evaluate MF-GIA, which is pretrained exclusively on node classification tasks using four datasets: WikiCS (web link), PubMed and ogbn-Arxiv (citation), and Amazon-ratings (e-commerce rating). These datasets are pre-encoded with heterogeneous feature spaces and label systems, enabling us to learn domain alignment without modality priors.

<!-- Page 9 -->

Published as a conference paper at ICLR 2026

**Table 2.** Few-shot node classification accuracy (%) with standard deviation over 10 runs. Best and second-best results are shown in bold and underlined. “–” denotes datasets where only encoded features and indexed labels are available, making modality-dependent models inapplicable.

## Method

Cora-7 way ogbn-Products-47 way Computers-10 way Physics-5 way BlogCatalog-6 way Citation E-commerce E-commerce Co-authorship Social Media

1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot

GCN 43.07±7.37 42.38±7.42 42.55±2.09 8.27±1.48 7.85±1.62 8.77±1.71 36.42±6.28 39.33±6.87 41.09±6.35 65.43±5.12 73.28±4.44 77.15±3.96 43.22±3.95 49.08±3.02 52.16±2.88 GAT 46.12±7.10 47.31±7.58 47.71±8.66 7.14±1.55 7.90±1.74 8.39±1.86 37.15±6.43 40.27±6.92 42.03±6.61 66.80±5.05 75.22±4.31 78.41±3.88 46.37±3.88 52.47±3.10 56.42±2.76 GraphSAGE 40.50±6.11 42.07±6.12 42.40±6.12 7.36±1.68 8.59±1.74 9.42±1.70 35.89±6.34 38.76±6.79 40.58±6.41 67.12±5.23 71.95±4.57 77.36±4.02 40.56±4.02 53.12±3.21 58.03±2.93

GraphMAE 42.41±6.38 43.36±6.94 44.22±6.49 8.58±1.63 9.87±1.69 9.94±1.71 40.86±6.31 42.72±6.83 43.35±6.51 68.23±4.89 77.04±3.92 80.35±3.51 43.25±3.71 57.93±2.86 62.14±2.64 DGI 41.28±6.54 42.18±6.75 43.27±6.33 9.04±1.49 10.08±1.52 10.87±1.59 39.91±6.22 41.77±6.75 45.54±6.39 66.12±5.01 74.83±4.20 78.09±3.76 42.11±3.79 56.08±2.94 60.91±2.71 GraphCL 40.22±6.47 44.68±6.88 45.56±6.42 11.93±1.65 11.26±1.71 13.14±1.77 38.74±6.39 41.55±6.91 43.19±6.58 74.35±4.95 82.12±4.05 85.40±3.62 44.87±3.66 57.20±2.90 63.55±2.69

GCOPE 42.63±6.33 43.89±6.77 44.74±6.36 11.18±1.60 11.73±1.68 12.54±1.72 43.02±6.36 43.84±6.87 47.46±6.55 76.18±4.81 84.65±3.88 85.07±3.42 45.02±3.58 58.76±2.81 63.05±2.61 GPF 41.12±6.45 40.26±6.84 43.16±6.41 11.12±1.57 12.65±1.63 13.43±1.70 37.02±6.28 39.84±6.79 41.62±6.48 69.28±4.95 76.91±4.22 83.85±3.73 43.08±3.63 58.01±2.83 63.47±2.62 All in One 42.66±6.38 43.92±6.81 44.78±6.37 8.15±1.54 8.77±1.61 8.83±1.68 35.64±6.36 40.48±6.82 44.07±6.50 73.43±5.10 81.36±4.37 85.20±3.85 42.54±3.75 56.72±2.96 61.31±2.70 GFT 41.40±0.04 43.31±1.11 43.55±7.43 11.12±1.57 14.65±1.63 15.43±1.70 – – – – – – – – – AutoGFM 46.29±7.24 47.33±7.80 47.76±8.06 – – – – – – – – – – – –

Prodigy 43.27±6.52 42.23±7.65 44.29±5.50 9.53±1.69 10.89±2.01 11.46±1.74 40.29±6.87 41.03±7.52 45.82±5.61 67.26±7.33 71.98±5.25 79.47±4.62 39.85±3.97 46.56±2.62 53.44±2.78 OFA 30.38±2.39 36.03±2.11 32.10±1.79 7.42±1.44 7.98±1.51 8.66±1.60 – – – – – – – – – GraphAlign 44.37±8.64 48.96±8.25 52.64±7.53 12.42±1.62 13.07±1.69 15.92±1.73 – – – – – – – – –

MF-GIA 47.64±8.77 57.38±9.02 63.98±7.13 16.86±2.55 19.16±2.19 22.61±1.71 41.49±7.49 46.21±14.16 53.71±3.28 79.12±11.54 86.48±0.96 88.92±0.84 49.46±4.02 62.69±2.53 67.31±2.60 Table 3: Few-shot edge classification accuracy (%) with standard deviation over 20 episodes.

## Method

FB15K237-5 way FB15K237-10 way FB15K237-40 way WN18RR-5 way WN18RR-10 way Encyclopedic KG Encyclopedic KG Encyclopedic KG Lexical KG Lexical KG

1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot 1-shot 3-shot 5-shot

GCN 82.45±1.20 84.30±1.05 85.12±0.98 70.28±3.50 74.61±2.85 78.94±2.43 55.72±0.95 58.11±0.78 60.05±0.70 32.14±2.90 38.62±2.35 42.57±2.01 24.05±1.60 28.93±1.42 31.20±1.35 GraphSAGE 83.11±1.14 85.05±1.01 86.02±0.92 71.36±3.28 75.43±2.71 79.45±2.36 56.40±0.90 58.86±0.74 60.72±0.68 33.05±2.80 39.41±2.26 43.28±1.96 24.83±1.55 29.62±1.39 31.88±1.31

DGI 84.22±1.08 85.67±0.96 86.30±0.88 72.48±3.10 76.58±2.59 80.12±2.21 56.95±0.88 59.44±0.72 61.31±0.65 34.57±2.75 40.28±2.20 44.05±1.92 25.67±1.50 30.18±1.34 32.41±1.28 GraphMAE 84.90±1.02 86.12±0.90 88.05±0.83 73.35±2.98 79.02±2.47 83.66±2.14 57.43±0.85 59.96±0.70 61.82±0.63 35.42±2.70 41.16±2.13 44.83±1.86 26.31±1.47 30.71±1.32 32.95±1.25

GCOPE 80.12±1.08 81.56±0.96 82.41±0.90 68.03±2.85 71.22±2.43 74.18±2.05 51.08±0.97 53.12±0.85 56.74±0.79 30.47±3.10 36.05±2.62 40.21±2.34 22.18±1.72 26.73±1.55 29.31±1.42 Prodigy 87.59±0.84 88.02±0.48 88.05±0.68 66.10±9.89 79.61±8.28 84.30±7.80 54.30±0.69 59.58±0.22 62.03±0.59 46.57±6.63 47.28±4.06 53.94±4.88 27.01±2.58 28.46±3.77 33.54±4.29 GFT 87.67±0.89 86.00±1.84 86.27±1.10 79.17±1.76 79.13±1.57 78.83±1.80 60.79±1.41 61.48±1.32 61.12±1.64 48.13±4.37 48.53±3.68 48.80±3.61 35.33±4.20 35.50±5.02 35.50±4.59 AutoGFM – – – – – – – – – 48.47±4.38 49.10±3.31 49.93±3.63 39.34±3.03 39.55±2.46 40.02±2.26 GraphAlign 83.02±1.28 83.15±1.07 84.92±0.98 73.25±3.05 76.14±2.58 77.02±2.20 53.10±8.32 54.26±3.93 59.35±6.70 45.08±10.55 47.47±9.88 60.19±10.31 27.80±3.05 30.65±2.82 32.10±2.60

MF-GIA 98.77±1.03 99.42±0.38 99.64±0.20 87.57±4.03 91.24±1.27 91.38±1.01 57.17±3.79 61.18±3.66 62.03±3.79 55.64±10.30 64.54±6.42 68.05±4.39 28.87±3.89 33.12±4.67 35.12±3.80

For downstream evaluation, we test on both node-level and edge-level classification tasks across seen and unseen domains. For node classification, we evaluate on Cora (citation), and unseen domains including ogbn-Products and Computers (e-commerce product), Physics (co-authorship), and BlogCatalog (social media). For link classification, we assess performance on two knowledge graphs (KGs) from different domains to predict the relation types: FB15K237 (encyclopedic) and WN18RR (lexical), which represent entirely new tasks not encountered in pretraining. To unify the task formulation, we transform the edge-level task into the node-level task by converting edges to nodes in a line graph, as detailed in Appendix D. This task allows us to evaluate our model’s generalization capability on an entirely new task and domains not seen during pretraining. More information about baseline configurations, datasets, and implementation details is provided in Appendix E.

## 4.2 IN-CONTEXT LEARNING RESULTS

**Table 2.** demonstrates that MF-GIA achieves state-of-the-art node classification results across diverse graph domains. Remarkably, MF-GIA reaches 63.98% on Cora with 5-shot prompting, which is an 11.34% absolute improvement over the second-best baseline. Across all 15 configurations, MF-GIA consistently outperforms existing methods with an average margin of 4.2%, despite using pure promptbased inference without any parameter updates. In contrast, methods like GFT and AutoGFM require extensive fine-tuning on target domains yet still achieve inferior results. This superiority reveals a fundamental insight: when equipped with proper cross-domain alignment, ICL beats fine-tuning. The critical role of alignment is also evident when comparing MF-GIA with Prodigy, which is a true ICL model without domain alignment. MF-GIA consistently outperforms Prodigy on unseen domains, demonstrating that domain embeddings capture domain characteristics for successful cross-domain transfer. Recent modality-dependent GFMs fail on graphs without raw text data (marked “–”), while MF-GIA operates universally on any pre-encoded graphs. Moreover, as shown in Table 3, MF-GIA excels at edge-level tasks, an entirely new task formulation never encountered during pretraining. It demonstrates that MF-GIA captures generalizable patterns for in-context reasoning rather than memorizing dataset/task-specific features. On WN18RR dataset with a 10-way setting, our MF-GIA does not surpass the state-of-the-art baselines GFT and AutoGFM, achieving third-best performance across all shot settings. It is because MF-GIA is pretrained exclusively on node classification tasks, while WN18RR is a dataset for edge-level tasks, which is an entirely different task formulation never encountered during pretraining. We deliberately evaluate on this dataset to assess our model’s generalization capacity to unseen tasks, as we believe a genuine graph foundation model should generalize not only to unseen domains but also to unseen task types. While GFT and AutoGFM achieve superior performance on WN18RR-10way, they are pretrained on both node-level and

<!-- Page 10 -->

Published as a conference paper at ICLR 2026

**Table 4.** Effect of core components.

## Method

Cora Computers Physics

1-shot 5-shot 1-shot 5-shot 1-shot 5-shot

GraphSAGE+FT 40.50 42.40 35.89 40.58 67.12 77.36 + Feat. Align. 42.78 45.26 37.86 45.97 75.83 85.29 ++ Label Alig. 43.96 49.16 37.93 47.00 76.54 87.66

+++ DPAA & Lepisode 47.64 63.98 41.49 53.71 79.12 88.92 Cora Computers Physics BlogCatalog 30

40

50

60

70

80

Accuracy (%)

GCN GAT GraphSAGE

**Figure 4.** Backbone selections.

edge-level tasks. Therefore, edge classification is not an unseen task for these baselines, so their performance advantage does not necessarily demonstrate stronger cross-task generalization.

## 4.3 MODEL ANALYSIS

Effect of Core Components. We analyze the contribution of each component in MF-GIA, starting from its GraphSAGE backbone. GraphSAGE+FT is pretrained on the same datasets and fine-tuned on support sets of test graphs. Adding a domain embedder with FiLM-based feature alignment (+Feat. Align.) improves cross-domain adaptability. Extending alignment to the label space (++Label Align.) further boosts performance by unifying class indices across graphs. Finally, incorporating DPAA with an episodic objective yields the full MF-GIA, which achieves the largest gains across datasets and shots. Table 4 shows a clear step-wise improvement, underscoring that both domain-conditioned alignment and prompt-aware reasoning are crucial for effective graph ICL.

**Table 5.** Effect of ICL scheme.

Computers Physics

MF-GIAsup 38.73 75.26 MF-GIA 41.49 79.12

Effect of Episodic Inference. ICL can be achieved through two paradigms: episodic meta-learning, which unifies pretraining and inference by training the model to perform inference episodes (MF- GIA and Prodigy), and supervised pretraining with test-time prototype construction, where class prototypes are built from support sets and queries are classified by proximity (GraphAlign). As shown in Table 5, episodic inference (MF-GIA) consistently outperforms the supervised variant (MF-GIAsup).

Effect of Backbone GNNs. In MF-GIA, we adopt GraphSAGE as the default backbone. Fig. 4 shows MF-GIA exhibits minor accuracy fluctuations across different GNN backbones under 1-shot settings, demonstrating that MF-GIA is robust to backbone selections. More analytical results are provided in Appendix F.

## 5 CONCLUSION

We introduced MF-GIA, a pretraining framework for graph neural networks that enables in-context learning across heterogeneous domains without relying on modality assumptions. By capturing domain characteristics via gradient fingerprints and aligning pre-encoded features and graph-local labels through domain-conditioned transformations, MF-GIA supports parameter-update-free adaptation from few-shot prompts. This design overcomes key limitations of existing GFMs by removing the need for post-training fine-tuning and modality-specific conversions. Experiments demonstrate strong performance on both seen and unseen domains, with seamless transfer to new tasks.

Future Directions. Beyond our current design, MF-GIA opens up several promising avenues for future work. One direction is to couple our gradient fingerprints with LLMs to generate semantic domain descriptions, enabling human-interpretable summaries of latent domain characteristics and more transparent cross-domain reasoning. Another is to leverage these fingerprints to automatically discover latent domain structure from large unlabeled graph collections, moving from manually curated domains to data-driven domain decomposition. We believe these extensions will further enhance the interpretability, automation, and scalability of modality-free graph foundation models.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

## ACKNOWLEDGEMENTS

This research is supported by the National Research Foundation, Singapore under its Frontier CRP Grant (NRF-F-CRP-2024-0005). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of the National Research Foundation, Singapore.

## REFERENCES

Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko.

Translating embeddings for modeling multi-relational data. Advances in neural information processing systems, 26, 2013.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,

Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. Advances in neural information processing systems, 33:1877–1901, 2020.

Haibo Chen, Xin Wang, Zeyang Zhang, Haoyang Li, Ling Feng, and Wenwu Zhu. AutoGFM:

Automated graph foundation model with adaptive architecture customization. In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/ forum?id=fCPB0qRJT2.

Zhikai Chen, Haitao Mao, Hang Li, Wei Jin, Hongzhi Wen, Xiaochi Wei, Shuaiqiang Wang, Dawei

Yin, Wenqi Fan, Hui Liu, et al. Exploring the potential of large language models (llms) in learning on graphs. ACM SIGKDD Explorations Newsletter, 25(2):42–61, 2024a.

Zhikai Chen, Haitao Mao, Jingzhe Liu, Yu Song, Bingheng Li, Wei Jin, Bahare Fatemi, Anton

Tsitsulin, Bryan Perozzi, Hui Liu, et al. Text-space graph foundation models: Comprehensive benchmarks and new insights. Advances in Neural Information Processing Systems, 37:7464–7492, 2024b.

Yuanning Cui, Zequn Sun, and Wei Hu. A prompt-based knowledge graph foundation model for universal in-context reasoning. Advances in Neural Information Processing Systems, 37:7095–7124, 2024.

Tim Dettmers, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel. Convolutional 2d knowledge graph embeddings. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.

Taoran Fang, Yunchao Zhang, Yang Yang, Chunping Wang, and Lei Chen. Universal prompt tuning for graph neural networks. Advances in Neural Information Processing Systems, 36:52464–52489, 2023.

Yi Fang, Dongzhe Fan, Sirui Ding, Ninghao Liu, and Qiaoyu Tan. Uniglm: Training one unified language model for text-attributed graphs embedding. In Proceedings of the Eighteenth ACM International Conference on Web Search and Data Mining, pp. 973–981, 2025.

Tao Feng, Yexin Wu, Guanyu Lin, and Jiaxuan You. Graph world model. In Forty-second Interna- tional Conference on Machine Learning, 2025. URL https://openreview.net/forum? id=xjTrTlBbrc.

Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In International conference on machine learning, pp. 1126–1135. PMLR, 2017.

Mikhail Galkin, Xinyu Yuan, Hesham Mostafa, Jian Tang, and Zhaocheng Zhu. Towards foundation models for knowledge graph reasoning. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=jVEoydFOl9.

Shivam Garg, Dimitris Tsipras, Percy S Liang, and Gregory Valiant. What can transformers learn in-context? a case study of simple function classes. Advances in neural information processing systems, 35:30583–30598, 2022.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Qi Guo, Leiyu Wang, Yidong Wang, Wei Ye, and Shikun Zhang. What makes a good order of examples in in-context learning. In Findings of the Association for Computational Linguistics: ACL 2024, pp. 14892–14904, 2024.

Will Hamilton, Zhitao Ying, and Jure Leskovec. Inductive representation learning on large graphs.

Advances in neural information processing systems, 30, 2017.

Yufei He, Yuan Sui, Xiaoxin He, and Bryan Hooi. Unigraph: Learning a unified cross-domain foundation model for text-attributed graphs. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1, pp. 448–459, 2025a.

Yufei He, Yuan Sui, Xiaoxin He, Yue Liu, Yifei Sun, and Bryan Hooi. Unigraph2: Learning a unified embedding space to bind multimodal graphs. In Proceedings of the ACM on Web Conference 2025, pp. 1759–1770, 2025b.

Zhenyu Hou, Xiao Liu, Yukuo Cen, Yuxiao Dong, Hongxia Yang, Chunjie Wang, and Jie Tang.

Graphmae: Self-supervised masked graph autoencoders. In Proceedings of the 28th ACM SIGKDD conference on knowledge discovery and data mining, pp. 594–604, 2022.

Zhenyu Hou, Haozhan Li, Yukuo Cen, Jie Tang, and Yuxiao Dong. Graphalign: Pretraining one graph neural network on multiple graphs via feature alignment. arXiv preprint arXiv:2406.02953, 2024.

Weihua Hu, Matthias Fey, Marinka Zitnik, Yuxiao Dong, Hongyu Ren, Bowen Liu, Michele Catasta, and Jure Leskovec. Open graph benchmark: Datasets for machine learning on graphs. Advances in neural information processing systems, 33:22118–22133, 2020.

Weihua Hu, Matthias Fey, Hongyu Ren, Maho Nakata, Yuxiao Dong, and Jure Leskovec. OGB-

LSC: A large-scale challenge for machine learning on graphs. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2), 2021. URL https://openreview.net/forum?id=qkcLxoC52kL.

Qian Huang, Hongyu Ren, Peng Chen, Gregor Krˇzmanc, Daniel Zeng, Percy S Liang, and Jure

Leskovec. Prodigy: Enabling in-context learning over graphs. Advances in Neural Information Processing Systems, 36:16302–16317, 2023.

Xingyue Huang, Pablo Barcelo, Michael M. Bronstein, Ismail Ilkan Ceylan, Mikhail Galkin,

Juan L Reutter, and Miguel Romero Orth. How expressive are knowledge graph foundation models? In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/forum?id=mXEdUcLtaK.

Pengfei Jiao, Jialong Ni, Di Jin, Xuan Guo, Huan Liu, Hongjiang Chen, and Yanxian Bi. Hgmp:

Heterogeneous graph multi-task prompt learning. arXiv preprint arXiv:2507.07405, 2025.

Thomas N. Kipf and Max Welling. Semi-supervised classification with graph convolutional networks.

In International Conference on Learning Representations, 2017. URL https://openreview. net/forum?id=SJU4ayYgl.

Lecheng Kong, Jiarui Feng, Hao Liu, Chengsong Huang, Jiaxin Huang, Yixin Chen, and Muhan

Zhang. GOFA: A generative one-for-all model for joint graph language modeling. In The Thirteenth International Conference on Learning Representations, 2025.

Jure Leskovec and Rok Sosiˇc. Snap: A general-purpose network analysis and graph-mining library.

ACM Transactions on Intelligent Systems and Technology (TIST), 8(1):1–20, 2016.

Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 2021.

Da Li, Jianshu Zhang, Yongxin Yang, Cong Liu, Yi-Zhe Song, and Timothy M Hospedales. Episodic training for domain generalization. In Proceedings of the IEEE/CVF international conference on computer vision, pp. 1446–1455, 2019.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Hao Liu, Jiarui Feng, Lecheng Kong, Ningyue Liang, Dacheng Tao, Yixin Chen, and Muhan

Zhang. One for all: Towards training one graph model for all classification tasks. In The Twelfth International Conference on Learning Representations, 2024a.

Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike

Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692, 2019.

Yixin Liu, Shiyuan Li, Yu Zheng, Qingfeng Chen, Chengqi Zhang, and Shirui Pan. Arc: A generalist graph anomaly detector with in-context learning. Advances in Neural Information Processing Systems, 37:50772–50804, 2024b.

Zemin Liu, Xingtong Yu, Yuan Fang, and Xinming Zhang. Graphprompt: Unifying pre-training and downstream tasks for graph neural networks. In Proceedings of the ACM web conference 2023, pp. 417–428, 2023.

Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.

Kevin Lu, Aditya Grover, Pieter Abbeel, and Igor Mordatch. Frozen pretrained transformers as universal computation engines. In Proceedings of the AAAI conference on artificial intelligence, volume 36, pp. 7628–7636, 2022.

Man Luo, Xin Xu, Yue Liu, Panupong Pasupat, and Mehran Kazemi. In-context learning with retrieved demonstrations for language models: A survey. Transactions on Machine Learning Research, 2024. ISSN 2835-8856. URL https://openreview.net/forum?id= NQPo8ZhQPa. Survey Certification.

P´eter Mernyei and C˘at˘alina Cangea. Wiki-cs: A wikipedia-based benchmark for graph neural networks. arXiv preprint arXiv:2007.02901, 2020.

Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. Efficient estimation of word representa- tions in vector space. arXiv preprint arXiv:1301.3781, 2013.

Sewon Min, Mike Lewis, Luke Zettlemoyer, and Hannaneh Hajishirzi. MetaICL: Learning to learn in context. In NAACL-HLT, 2022.

Shimei Pan and Tao Ding. Social media-based user embedding: A literature review. arXiv preprint arXiv:1907.00725, 2019.

Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.

Oleg Platonov, Denis Kuznedelev, Michael Diskin, Artem Babenko, and Liudmila Prokhorenkova.

A critical look at the evaluation of GNNs under heterophily: Are we really making progress? In The Eleventh International Conference on Learning Representations, 2023. URL https: //openreview.net/forum?id=tJbbQfw-5wv.

Chengwei Qin, Aston Zhang, Chen Chen, Anirudh Dagar, and Wenming Ye. In-context learning with iterative demonstration selection. In Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 7441–7455, 2024.

Jiezhong Qiu, Qibin Chen, Yuxiao Dong, Jing Zhang, Hongxia Yang, Ming Ding, Kuansan Wang, and Jie Tang. Gcc: Graph contrastive coding for graph neural network pre-training. In Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining, pp. 1150–1160, 2020.

Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings using siamese bert-networks.

In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 3982. Association for Computational Linguistics, 2019.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Ruifeng Ren and Yong Liu. Towards understanding how transformers learn in-context through a representation learning lens. Advances in Neural Information Processing Systems, 37:892–933, 2024.

David Rogers and Mathew Hahn. Extended-connectivity fingerprints. Journal of chemical information and modeling, 50(5):742–754, 2010.

Ohad Rubin, Jonathan Herzig, and Jonathan Berant. Learning to retrieve prompts for in-context learning. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 2655–2671, 2022.

Oleksandr Shchur, Maximilian Mumme, Aleksandar Bojchevski, and Stephan G¨unnemann. Pitfalls of graph neural network evaluation. arXiv preprint arXiv:1811.05868, 2018.

Jake Snell, Kevin Swersky, and Richard Zemel. Prototypical networks for few-shot learning. Advances in neural information processing systems, 30, 2017.

Xiangguo Sun, Hong Cheng, Jia Li, Bo Liu, and Jihong Guan. All in one: Multi-task prompting for graph neural networks. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 2120–2131, 2023.

Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay

Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.

Petar Veliˇckovi´c, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Li`o, and Yoshua

Bengio. Graph Attention Networks. International Conference on Learning Representations, 2018. URL https://openreview.net/forum?id=rJXMpikCZ.

Petar Veliˇckovi´c, William Fedus, William L. Hamilton, Pietro Li`o, Yoshua Bengio, and R Devon

Hjelm. Deep Graph Infomax. In International Conference on Learning Representations, 2019. URL https://openreview.net/forum?id=rklz9iAcKQ.

Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Daan Wierstra, et al. Matching networks for one shot learning. Advances in neural information processing systems, 29, 2016.

Johannes Von Oswald, Eyvind Niklasson, Ettore Randazzo, Jo˜ao Sacramento, Alexander Mordvintsev,

Andrey Zhmoginov, and Max Vladymyrov. Transformers learn in-context by gradient descent. In International Conference on Machine Learning, pp. 35151–35174. PMLR, 2023.

Kai Wang, Siqiang Luo, Caihua Shan, and Yifei Shen. Towards graph foundation models: Training on knowledge graphs enables transferability to general graphs. arXiv preprint arXiv:2410.12609, 2024a.

Zehong Wang, Zheyuan Zhang, Nitesh V Chawla, Chuxu Zhang, and Yanfang Ye. Gft: Graph foundation model with transferable tree vocabulary. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024b.

Renchi Yang, Jieming Shi, Xiaokui Xiao, Yin Yang, Sourav S Bhowmick, and Juncheng Liu. Pane:

scalable and effective attributed network embedding. The VLDB journal, 32(6):1237–1262, 2023.

Zhilin Yang, William Cohen, and Ruslan Salakhudinov. Revisiting semi-supervised learning with graph embeddings. In International conference on machine learning, pp. 40–48. PMLR, 2016.

Yuning You, Tianlong Chen, Yongduo Sui, Ting Chen, Zhangyang Wang, and Yang Shen. Graph contrastive learning with augmentations. Advances in neural information processing systems, 33: 5812–5823, 2020.

Xingtong Yu, Zechuan Gong, Chang Zhou, Yuan Fang, and Hui Zhang. Samgpt: Text-free graph foundation model for multi-domain pre-training and cross-domain adaptation. In Proceedings of the ACM on Web Conference 2025, pp. 1142–1153, 2025.

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

Haonan Yuan, Qingyun Sun, Junhua Shi, Xingcheng Fu, Bryan Hooi, Jianxin Li, and Philip S.

Yu. How much can transfer? BRIDGE: Bounded multi-domain graph foundation model with generalization guarantees. In Forty-second International Conference on Machine Learning, 2025. URL https://openreview.net/forum?id=bjDKZ3Roax.

Ruiqi Zhang, Spencer Frei, and Peter L Bartlett. Trained transformers learn linear models in-context.

Journal of Machine Learning Research, 25(49):1–55, 2024.

Yiming Zhang, Shi Feng, and Chenhao Tan. Active example selection for in-context learning. In

Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 9134–9148, 2022.

Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex Smola. Automatic chain of thought prompting in large language models. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=5NTt8GFjUHkr.

Haihong Zhao, Aochuan Chen, Xiangguo Sun, Hong Cheng, and Jia Li. All in one and one for all: A simple yet effective method towards cross-domain graph pretraining. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 4443–4454, 2024.

Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and Sameer Singh. Calibrate before use: Improving few-shot performance of language models. In International conference on machine learning, pp. 12697–12706. PMLR, 2021.

Yun Zhu, Haizhou Shi, Xiaotang Wang, Yongchao Liu, Yaoke Wang, Boci Peng, Chuntao Hong, and

Siliang Tang. Graphclip: Enhancing transferability in graph foundation models for text-attributed graphs. In Proceedings of the ACM on Web Conference 2025, pp. 2183–2197, 2025.

Wei Zhuo and Guang Tan. Efficient graph similarity computation with alignment regularization.

Advances in Neural Information Processing Systems, 35:30181–30193, 2022.

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

A RELATED WORK

In-context Learning. The modern paradigm of in-context learning (ICL) emerged with GPT- 3 (Brown et al., 2020), which demonstrated that large autoregressive transformers can adapt to new tasks using only a few labeled demonstrations, without any parameter updates. This breakthrough sparked extensive research along multiple dimensions. From a theoretical perspective, subsequent work has clarified the fundamental mechanisms underlying ICL. Several studies establish connections between ICL and classical meta learning frameworks, drawing parallels to metric-based few-shot methods, including Matching Networks (Vinyals et al., 2016), Prototypical Networks (Snell et al., 2017), and Model-Agnostic Meta Learning (Finn et al., 2017). More recent theoretical analyses reveal that transformers can implement gradient descent algorithms within their forward pass (Von Oswald et al., 2023; Ren & Liu, 2024; Zhang et al., 2024), effectively learning to optimize in-context. Complementary work by (Garg et al., 2022) demonstrates that transformers can learn entire function classes from context, providing an alternative computational perspective on ICL capabilities. On the methodological front, researchers have developed techniques to enhance ICL performance through improved prompt engineering. Min et al. (2022) introduce MetaICL, which explicitly trains models to perform in-context learning. Practical advances focus on demonstration selection and ordering: retrieval-based methods identify optimal examples (Rubin et al., 2022; Luo et al., 2024), while active selection strategies iteratively refine the demonstration set (Zhang et al., 2022; Qin et al., 2024). The sensitivity of ICL to prompt construction has motivated calibration techniques (Zhao et al., 2021) and continuous prompt optimization (Lester et al., 2021), with recent work revealing substantial impacts from demonstration ordering (Guo et al., 2024). However, extending ICL to graph-structured data presents unique challenges due to the heterogeneous nature of graph domains and the complex interplay between topology, features, and labels.

Graph Foundation Models. Graph Foundation Models (GFMs) have evolved from early selfsupervised methods like GraphCL (You et al., 2020) and GraphMAE (Hou et al., 2022) toward comprehensive cross-domain and cross-task generalization. This evolution follows three primary research directions. First, cross-domain unification is achieved by using text-attributed graphs (TAGs) as a universal modality. Specifically, OFA (Liu et al., 2024a), GOFA (Kong et al., 2025), and UniGraph (He et al., 2025a) convert graphs to textual representations, then adopt LLMs and GNNs to learn semantic and structural information, respectively. UniGLM (Fang et al., 2025) trains unified language models over multiple TAGs, GraphCLIP (Zhu et al., 2025) aligns graph summaries with language via contrastive learning, and (Wang et al., 2024b) introduces transferable tree vocabularies. AutoGFM (Chen et al., 2025) studies the automatically adapting architectures to different TAGs. In contrast, text-free methods avoid modality conversion. For example, SAMGPT (Yu et al., 2025) employs learnable domain tokens for domain alignment, and GCOPE (Zhao et al., 2024) connects disparate graphs with virtual nodes to enable cross-domain pretraining. Second, for prompt-based adaptation, GraphPrompt (Liu et al., 2023) and All in One (Sun et al., 2023) unify pretraining and downstream tasks via learnable prompts; Prodigy (Huang et al., 2023) enables graph ICL with prompt graphs and shows few-zero transfer to unseen graphs; ARC (Liu et al., 2024b) achieves generalist anomaly detection via contextual cues. Knowledge graph models (Wang et al., 2024a) have particularly benefited from this paradigm. For example, ULTRA (Galkin et al., 2024) learns universal relational representations, KG-ICL (Cui et al., 2024) frames reasoning as prompting, and theoretical analysis (Huang et al., 2025) links expressivity to learned relation motifs. Third, for multimodal extensions, emerging work extends GFMs beyond single modalities. UniGraph2 (He et al., 2025b) unifies text and visual features with graph structure, while Graph World Model (Feng et al., 2025) integrates graph-structured states for planning and control. These advances establish a trajectory toward GFMs that function as universal encoders and reasoners across domains, tasks, and modalities.

Our MF-GIA framework is particularly suited to privacy-constrained settings where schemas and modalities differ across organizations but raw features cannot be shared, such as cross-organization fraud detection over transaction graphs from different banks and multi-hospital patient networks with heterogeneous EHR systems. In such scenarios, each party can locally encode its graph, while MF-GIA uses gradient fingerprints and lightweight domain aligners to align these heterogeneous domains without any modality assumptions, such as TAGs. This complements recent trends in GFMs toward realistic cross-domain deployment, including text-based cross-domain models (Chen et al., 2024b) and graph prompt optimization frameworks like HGMP (Jiao et al., 2025), all of which

<!-- Page 17 -->

Published as a conference paper at ICLR 2026 highlight the growing need for privacy-preserving, modality-agnostic foundation models in practical applications.

B PROOFS

B.1 PROOF OF THEOREM 3.1

The theorem shows that the domain embedder fϕde acts as a distance-preserving map from the domain space to the embedding space. To prove it, we first give a formal definition of the graph domain and graph distance. Definition 2 (Graph Domain). A graph domain Di is characterized by a joint distribution Pi(G, Y) over graphs G = (V, E, X) and labels Y, where the feature distribution Pi(X), label distribution Pi(Y), and structure distribution Pi(E|V) jointly define the domain characteristics. Definition 3 (Graph Distance). For two graphs Gi = (Vi, Ei, Xi) and Gj = (Vj, Ej, Xj) with normalized adjacency matrices Ai and Aj, we define the graph distance as dG (Gi, Gj) = ∥Xi −Xj∥F +∥Ai −Aj∥F, where we assume |Vi| = |Vj| (padding with isolated nodes if necessary for comparison).

Then we define the domain distance used in Eq. (7) to measure the inherent similarity between domains. Definition 4 (Domain Distance). The distance between two domains Di and Dj is measured by the Wasserstein distance:

W2 (Di, Dj) = inf κ∈Γ(Pi,Pj)

E(Gi,Gj)∼κ d2

G(Gi, Gj)

1/2, (21)

where Γ (Pi, Pj) denotes all joint distributions with marginals Pi and Pj, dG(Gi, Gj) is a graph distance metric that captures both feature and structural differences between graphs.

Before proving this theorem, we establish a technical lemma that characterizes the properties of gradient fingerprints. Lemma B.1. For a graph G = (V, E, X, Y) and the one-layer GNN encoder initialization θ0 ∈ Rdo×d, the gradient of the task loss at θ0 can be decomposed as:

∇θL (θ0, G) = 1 |V |X⊤A · diag(g) · 1d, (22)

where A is the normalized adjacency matrix, g = g1, · · ·, g|V |

⊤∈R|V | is a vector of per-node loss gradients with gv = ∇hvℓ(hv, yv), ℓis the node-level loss function, and 1d is the all-ones vector.

Proof. Consider the forward pass of a one-layer GNN with weight matrix θ ∈Rd0×d:

H = σ(AXθ), (23)

where σ is the nonlinear activation function (e.g., ReLU). The task loss over the graph is:

L(θ, G) = 1 |V |

X v∈V ℓ(hv, yv), (24)

where hv is the representation of v, which is the v-th row of H, and ℓis the node-level loss function (e.g., cross-entropy). Computing the gradient with respect to θ via the chain rule:

∇θL(θ, G) = 1 |V |

X v∈V

∇θh⊤ v · ∇hvℓ(hv, yv). (25)

For the gradient of hv w.r.t. θ, it can be represented as:

∇θhv =



X u∈N(v)

Avuxu





⊤

⊗σ′ ((AXθ)v). (26)

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

At initialization θ0, assuming ReLU activation with appropriate initialization ensuring positive pre-activations, we have σ′ ((AXθ0)v) ≈1d. Therefore, the gradient can be represented as:

∇θL (θ0, G) = 1 |V |

X v∈V



X u∈N(v)

Avuxu





⊤

· gv, (27)

where gv = ∇hvℓ(hv, yv) is the gradient of the loss with respect to node v’s representation. This can be rewritten in matrix form as:

∇θL (θ0, G) = 1 |V |X⊤A⊤· diag(g) · 1d. (28)

For undirected graphs with symmetric normalized adjacency matrices, A⊤= A, yielding:

∇θL (θ0, G) = 1 |V |X⊤A · diag(g) · 1d, (29)

which completes the proof.

Building on the above definitions and lemmas, we now present the proof of Theorem 3.1.

Proof. Since the gradient fingerprint for Gi sampled from domain Di, gradient fingerprint is defined as:

∆θi = θ0 −η∇θLi (θ0, Gi). (30) For two graphs Gi and Gj from two domains, we have:

∆θi −∆θj = −η (∇θLi (θ0, Gi) −∇θLj (θ0, Gj)). (31)

Then the Frobenius norm can be represented as:

∥∆θi −∆θj∥F = η ∥∇θLi (θ0, Gi) −∇θLj (θ0, Gj)∥F. (32)

Based on the Lemma B.1, and assuming |Vi| = |Vj| = n (we can pad with isolated nodes if necessary) for simplicity, the gradient difference becomes:

∇θLi (θ0, Gi) −∇θLj (θ0, Gj) = 1 n

X⊤ i Ai · diag (gi) −X⊤ j Aj · diag (gj)

· 1d, (33)

where gi = [gi,1, gi,2, · · ·, gi,n]⊤∈Rn is the vector of per-node loss gradient with gi,v = ∇hi,vℓ(hi,v, yi,v) for node v in Gi. Let Mi = X⊤ i Ai · diag (gi) ∈Rdo×n and Mj = X⊤ j Aj · diag (gj) ∈Rdo×n, taking into Eq. (33) and computing the Frobenius norm, we have:

∥∇θLi (θ0, Gi) −∇θLj (θ0, Gj)∥F = 1 n ∥(Mi −Mj) · 1d∥2. (34)

Since ∥1d∥2 =

√ d, with the property of operator norm, the following inequality holds:

∥(Mi −Mj) · 1d∥2 ≤∥Mi −Mj∥op · ∥1d∥2 = ∥Mi −Mj∥op ·

√ d, (35)

where ∥· ∥op denotes the operator norm. To bound ∥Mi −Mj∥op, we decompose it by adding and subtracting intermediate terms as:

Mi −Mj = X⊤ i Ai · diag(gi) −X⊤ j Aj · diag(gj)

= (Xi −Xj)⊤Ai · diag(gi) + X⊤ j (Ai −Aj) · diag(gi)

+ X⊤ j Aj · (diag(gi) −diag(gj)).

(36)

Taking the operator norm and using the triangle inequality on Eq. (36), we can bound the ∥Mi −Mj∥op with:

∥Mi −Mj∥op ≤

(Xi −Xj)⊤ op ∥Ai∥op ∥diag (gi)∥op

+

X⊤ j op ∥(Ai −Aj)∥op ∥diag (gi)∥op

+

X⊤ j op ∥Aj∥op ∥diag (gi) −diag (gj)∥op.

(37)

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

For a diagonal matrix, the operator norm is the maximum absolute value of its diagonal entries. Therefore, for the diagonal matrix of the per-node gradient vector diag(gi) of graph Gi, its operator norm can be computed by ∥diag (gi)∥op = maxv∈Vi |gi,v|. Based on the assumption in Theorem 3.1 that the task loss L is Ltask-smooth with respect to model parameters, it means that its gradient is Ltask-Lipschitz continuous. Let the task loss L be a cross-entropy loss with Ci classes, the node-level loss on node v in Gi is ℓ(hi,v, yv) = −log exp h(yv)

i,v

PCi c=1 exp h(c)

i,v

. The gradient on v is gi,v = ∇hi,vℓ(hi,v, yv) = pv −ryv, where pv = softmax(hi,v) ∈[0, 1]Ci and ryv is the one-hot encoding of the ground-truth label of v. Therefore, the following inequality holds:

∥gi,v∥2 = ∥pv −ryv∥2 ≤∥pv∥2 + ∥ryv∥2 ≤ p

Ci + 1. (38)

Since we are considering gi,v as a scalar after projection, we have:

|gi,v| ≤ p

Ci + 1 =: ˆCi (39)

Thus, we have ∥diag (gi)∥op ≤ ˆCi. Based on the nature of the operator norm, we have (Xi −Xj)⊤ op = ∥Xi −Xj∥op ≤∥Xi −Xj∥F,

X⊤ j op = ∥Xj∥op ≤B (bounded by fea- ture norms), and ∥Ai∥op, ∥Aj∥op ≤1 where A is the normalized adjacency matrix, we get:

∥Mi −Mj∥op ≤ˆCi ∥Xi −Xj∥F + B ˆCi ∥Ai −Aj∥F + B ∥diag (gi) −diag (gj)∥op. (40)

For the last term of Eq. (40), since the task loss L is Ltask-smooth, the node-level loss ℓinherits smoothness with Lipschitz gradient constant Lℓ. Given node v with the same index in Gi and Gj, the gradient difference between gi and gj is ∥diag(gi) −diag(gj)∥op = maxv |gi,v −gj,v|. Since gi,v = ∇hi,vℓ(hi,v, yi,v) and the gradient is Lipschitz, we have:

∥gi,v −gj,v∥≤Lℓ∥hi,v −hj,v∥. (41)

In the one-layer message passing defined in Eq. (23), the activation function σ(·) is typically ReLU, which is 1-Lipschitz. Thus, we have:

∥hi,v −hj,v∥≤

[(AiXi −AjXj) θ0]v

≤

(AiXi −AjXj)v

· ∥θ0∥, (42)

where the node v in AiXi −AjXj can be rewritten as (AiXi)v −(AjXj)v = P u Ai,vuxT i,u − P u Aj,vuxT j,u, which can be further bounded by:

∥(AiXi −AjXj)v∥≤∥(Ai −Aj)vXi∥+ ∥(Aj)v(Xi −Xj)∥

≤∥(Ai −Aj)v∥∥Xi∥op + ∥(Aj)v∥∥Xi −Xj∥op. (43)

Since A is normalized where ∥(Aj)v∥1 = 1 and thus ∥(Aj)v∥2 ≤1. Taking Eq. (43) into Eq. (42), we can bound the difference between hi,v and hj,v as:

∥hi,v −hj,v∥≤∥θ0∥·

(Ai −Aj)v

B + ∥Xi −Xj∥op

. (44)

To get a uniform bound over all nodes, we have:

max v ∥hi,v −hj,v∥≤∥θ0∥·

∥Ai −Aj∥F B + ∥Xi −Xj∥F

, (45)

which gives us:

∥diag (gi) −diag (gj)∥op ≤Lℓ∥θ0∥·

B ∥Ai −Aj∥F + ∥Xi −Xj∥F

. (46)

Since Lℓ, θ0, and B are fixed, we can use L ′ = Lℓ∥θ0∥max(B, 1) to combine them. There, Eq. (46) can be rewritten as:

∥diag (gi) −diag (gj)∥op ≤L ′

∥Xi −Xj∥F + ∥Ai −Aj∥F

. (47)

To measure the inherently distance between two graphs, we define the graph distance as dG(Gi, Gj) = ∥Xi −Xj∥F + ∥Ai −Aj∥F as Definition 3. Then, taking the graph distance and Eq. (47) into Eq. (40), we have:

∥Mi −Mj∥op ≤eC · dG (Gi, Gj), (48)

<!-- Page 20 -->

Published as a conference paper at ICLR 2026 where eC = ˆCi + B ˆCi + BL ′. Recall Eq. (32), Eq. (34), and Eq. (35), we can integrate the used constants, such as

√ d and 1 n, into eC. Then the difference between the gradient fingerprints of two domains is bounded as:

∥∆θi −∆θj∥F ≤η eC · dG (Gi, Gj). (49) For the graph distance dG, we have:

dG (Gi, Gj) = ∥Xi −Xj∥F + ∥Ai −Aj∥F ≤

√

2 q

∥Xi −Xj∥2

F + ∥Ai −Aj∥2

F. (50)

The Wasserstein distance can be rewritten as:

W2 (Di, Dj) = inf γ∈Γ(Pi,Pj)

q

E(Gi,Gj)∼κ d2

G (Gi, Gj)

(51)

For the optimal coupling κ∗that achieves the Wasserstein distance, by Jensen’s inequality for the concave square root function, we have:

E(Gi,Gj)∼κ∗[dG (Gi, Gj)] ≤ q

E(Gi,Gj)∼κ∗ d2

G (Gi, Gj)

= W2 (Di, Dj). (52)

Combining Eq. (52) and Eq. (49), the bound of ∥∆θi −∆θj∥F can be expressed as:

∥∆θi −∆θj∥F ≤η eC · E[dG(Gi, Gj)] ≤η eC · W2(Di, Dj). (53)

Eq. (53) shows that the similarity between gradient fingerprints can effectively reflect the domain similarity. Recall the domain embedder defined in Eq. (5), we can conduct the Lipschitz analysis on it. First, the Conv2D with kernel weights Wconv satisfy ∥Conv2D(x) −Conv2D(y)∥≤ ∥Wconv∥op · ∥x −y∥, the Flatten operation preserves norms ∥Flatten(A) ∥2 =∥A∥F, and the MLP with R-layer weight matrices W1 · · ·, WR satisfy ∥MLP(x)−MLP(y)∥≤QR r=1 ∥Wr∥op·∥x−y∥. Thus, the overall Lipschitz constant of the domain embedder fϕde is:

Lde = ∥Wconv∥op ·

R Y r=1

∥Wr∥op. (54)

Thus, the following Lipschitz inequality holds:

∥ei −ej∥2 = ∥fde (∆θi) −fde (∆θj)∥2 ≤Lde ∥∆θi −∆θj∥F. (55)

We can substitute Eq. (53) into Eq. (55) and merge all constants into eC, we can get:

∥ei −ej∥2 ≤eC · W2(Di, Dj) (56)

This shows that the domain embedding function preserves domain relationships: similar domains with small W2 map to nearby embeddings with small ∥ei −ej∥2.

B.2 PROOF OF PROPERTY 1

Proof. By definition, fϕfeat being L -Lipschitz means that for all e, e′ ∈Rde,

∥fϕfeat(e) −fϕfeat (e′)∥2,1 ≤L ∥e −e′∥2. (57)

Applying this with e = ei and e′ = ej for domain embeddings of Gi and Gj, we have:

fϕfeat (ei) −fϕfeat (ej) = γfeat (ei) −γfeat (ej), βfeat (ei) −βfeat (ej)

= (∆γ, ∆β). (58)

Then using the definition of ∥· ∥2,1 gives:

∥∆γ∥2 + ∥∆β∥2 = ∥fϕfeat (ei) −fϕfeat (ej)∥2,1 ≤L ∥ei −ej∥2, (59)

which is exactly the claimed inequality in Property 1. For the graph Gi, the domain-conditioned transformation for its domain i on an item w is Kfeat i: Rd →Rd:

Kfeat i = γfeat i ⊙h + βfeat i. (60)

<!-- Page 21 -->

Published as a conference paper at ICLR 2026

Then for any h ∈Rd, the following inequality holds:

Kfeat i (h) −T feat j (h)

2 = γfeat i −γfeat j

⊙h + βfeat i −βfeat j

2 ≤ γfeat i −γfeat j

⊙h

2 + βfeat i −βfeat j

2 ≤∥h∥∞ γfeat i −γfeat j

2 + βfeat i −βfeat j

2 ≤∥h∥2 γfeat i −γfeat j

2 + βfeat i −βfeat j

2,

(61)

Combining Eq. (59) and Eq. (61) yields:

Kfeat i (h) −T feat j (h)

2 ≤max {∥h∥2, 1} L ∥ei −ej∥2. (62)

Thus, as domains move closer in the embedding space, their induced feature transforms move closer uniformly on any set of bounded ∥h∥2, so the collections {Kfeat i (hi,w)}w and {Kfeat j (hj,w)}w occupy neighboring subspaces in the unified feature space.

C ALGORITHMS AND COMPLEXITY ANALYSIS

C.1 ALGORITHMS

## Algorithm

1 presents the episodic pretraining procedure for MF-GIA. Algorithm 2 details parameterupdate-free in-context inference on unseen graphs. At a high level, pretraining teaches the model to (1) extract a gradient-fingerprint domain embedding from a small support set, (2) map that embedding to domain-conditioned feature and label transforms that place heterogeneous graphs in a shared space, and (3) perform prompt-aware matching between queries and aligned supports. At test time, we reuse the same pipeline with frozen parameters, computing the domain embedding and transforms on-the-fly from a few labeled examples only.

C.2 COMPLEXITY ANALYSIS

Let Gi = (Vi, Ei, Xi, Yi) be a pretraining graph with |Vi| nodes and |Ei| edges, GNN encoder width d, input width do, and domain embedding width de. Offline, the domain embedder computes a single gradient fingerprint per graph by one forward–backward through the shared J-layer GNN fθ from θ0, which costs O(J(|Ei| + |Vi|), d) per Gi. Each fingerprint ∆θi ∈Rdo×d is then embedded via fϕde, giving O (dedod) time. After caching ∆θi, training fϕde with the pairwise metric-preserving loss adds O

M 2de per epoch for M pretraining graphs. In each episode on Gi with m-way k-shot support and T queries per way, generating FiLM parameters for domain-conditioned transformations γfeat i, βfeat i

= fϕfeat (ei) and γlabel i, βlabel i

= fϕlabel (ei) costs O (ded), and applying Kfeat i to (mk + mT) item embeddings and Klabel i to m label rows of the shared base Elabel ∈RLmax×d costs O((mk + mT)d + md). The time complexity of DPAA is O

(mk + m)d2 + mT d2 + mkd + md

, which is typically secondary to the encoder when m and k are few-shot. Typically, we have M, J, T, k, m ≪|Vi|, |Ei|, d, do, de, therefore the overall time complexity can be represented as O

PM i=1 (|Ei| + |Vi|) d + dedod

, which is linear in graph size.

D TASK UNIFICATION

With a bit of notation abuse, in knowledge graphs FB15K237 and WN18RR, link classification aims to predict the relation type r for a given triple (h, r, t), where h and t are head and tail entities, respectively. To leverage our node classification framework for this task, we transform the link classification problem into node classification through line graph construction. Given a knowledge graph G = (V, E, R, X) with entities V, edges E, relation types R, and node feature matrix X, we construct a line graph LG(G) = (VLG, ELG, XLG), where each edge ε = (h, r, t) ∈E becomes a node vε ∈VLG. Two nodes vεi, vεj ∈VLG and are connected if the corresponding edges εi, εj share a common entity (head or tail). Formally, the edge set ELG is defined as:

ELG = vεi, vεj

: εi = (hi, ri, ti), εj = (hj, rj, tj), {hi, ti} ∩{hj, tj}̸ = ∅

(63)

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

## Algorithm

1: MF-GIA Pretraining

Input: Pretraining graphs G = {Gi = (Vi, Ei, Xi, Yi)}M i=1; unified item dim do; embedding dim d; GNN encoder fθ with stored initialization θ0 (kept frozen); base label table Elabel ∈RLmax×d; Domain embedder fϕde; FiLM aligners fϕfeat, fϕlabel; DPAA params WK, WV, WQ and head fΩ; Episode spec (m-way, k-shot, T queries), temperature τ, learning rate η. Output:Pretrained model MΦ = {θ0, fϕde, fϕfeat, fϕlabel, WK, WV, WQ, fΩ}.

1 (Optional) feature unification. For each Xi, map to Rdo via SVD. // unify dims

## 2 Stage A:

Train domain embedder fϕde. // gradient fingerprints

3 for i = 1,..., M do

## 4 Compute one gradient step on

Gi from θ0: θi ←θ0 −η∇θLi(θ0).

5 Store fingerprint ∆θi ←θi −θ0.

6 end

7 repeat

8 ei ←fϕde(∆θi) for all i.

9 Lde ←P i,j

∥∆θi −∆θj∥F −∥ei −ej∥2

2.

10 Update fϕde by descending ∇Lde.

11 until converged

12 Freeze fϕde (and keep fθ at θ0).

## 13 Stage B:

Episodic pretraining with DPAA (encoder init frozen).

14 for episodes do

## 15 Sample a graph Gi and an m-way k-shot support set S plus T queries per class as the query

set Q.

16 ei ←fϕde(∆θi); (γfeat i, βfeat i) ←fϕfeat(ei); (γlabel i, βlabel i) ←fϕlabel(ei). // Aligned features / labels

17 For any item w, hi,w ←fθ0(w, Gi), zi,w ←γfeat i ⊙hi,w + βfeat i.

18 For each class l used in the episode, ui,l ←γlabel i ⊙Elabel l + βlabel i.

## 19 Form

Zpmt ∈R(mk)×d from support {zi,w} and Upmt ∈Rm×d from {ui,l}. // Dual Prompt-Aware Attention (single-query attention)

20 for each query item q with class c do

21 Kfeat ←ZpmtWK, Vfeat ←ZpmtWV, Qfeat ←zi,qWQ.

zout i,q ←softmax

QfeatKfeat⊤

√ d

Vfeat.

23 Klabel ←UpmtWK, Vlabel ←UpmtWV, Qlabel ←fΩ(zout i,q).

24 uout i,q ←softmax

QlabelKlabel⊤

√ d

Vlabel.

25 si,q ←uout i,q(Upmt)⊤∈Rm; Lepisode ←−log exp(si,q[c]/τ) Pm j=1 exp(si,q[j]/τ).

26 end

27 Update {fϕfeat, fϕlabel, Elabel, WK, WV, WQ, fΩ} to minimize the mean query loss Lpretrain of the episode.

28 end

For each node vε ∈VLG in the line graph corresponding to edge ε = (h, r, t), we construct features by aggregating the embeddings of the connected entities and relation as xve = [xh∥xt], where [·∥·] denotes concatenation. The concatenated features are then projected to the unified dimension using PCA to maintain consistency with the node classification framework. After transformation, link classification becomes a node classification problem on the line graph, where each node (representing an edge in the original graph) needs to be classified into one of R relation types.

<!-- Page 23 -->

Published as a conference paper at ICLR 2026

## Algorithm

2: MF-GIA Test-time In-context Inference (Parameter-Update-Free w.r.t. MΦ) Input: Frozen pretrained Φ from Algorithm 1; unseen graph Gnew = (Vnew, Enew, Xnew)

with Cnew classes; Cnew-way k-shot support set S = {(wj, yj)}kCnew j=1; queries Q ⊆Gnew \ S. Output:Predictions {ˆyq}q∈Q.

// In-context domain embedding (from support only)

1 Compute a one-step fingerprint from θ0 on S: θnew ←θ0 −η∇θLnew(θ0; S); enew ←fϕde(θnew −θ0).

// Domain-conditioned alignment for Gnew

2 (γfeat new, βfeat new) ←fϕfeat(enew); (γlabel new, βlabel new) ←fϕlabel(enew).

3 For any item w: hnew,w ←fθ0(w, Gnew), znew,w ←γfeat new ⊙hnew,w + βfeat new.

4 For l = 0,..., Cnew −1: unew,l ←γlabel new ⊙Elabel l + βlabel new.

## 5 Form

Zpmt new ∈R(kCnew)×d from {znew,w}(w,y)∈S and Upmt new ∈RCnew×d from {unew,l}.

// Dual Prompt-Aware Attention inference (no parameter update)

6 for each query q ∈Q do

7 Kfeat ←Zpmt newWK, Vfeat ←Zpmt newWV, Qfeat ←znew,qWQ.

8 zout new,q ←softmax

QfeatKfeat⊤

√ d

Vfeat.

9 Klabel ←Upmt newWK, Vlabel ←Upmt newWV, Qlabel ←fΩ(zout new,q).

10 uout new,q ←softmax

QlabelKlabel⊤

√ d

Vlabel.

11 sq ←uout new,q(Upmt new)⊤; ˆyq ←arg maxj sq[j].

12 end

**Table 6.** Dataset statistics.

Usage Dataset Domain Task #Nodes #Edges # Classes

Pretrain WikiCS Web link Node 11,701 216,123 10 PubMed Citation Node 19,717 44,338 3 ogbn-Arxiv Citation Node 169,343 1,166,243 40 Amazon-ratings E-commerce (Ratings) Node 24,492 93,050 5

## Evaluation

Cora Citation Node 11,701 216,123 10 ogbn-Products E-commerce (Product Category) Node 2,449,029 61,859,140 47 Computers E-commerce (Product Category) Node 13,752 491,722 10 Physics Co-authorship Node 34,493 495,924 5 BlogCatalog Social Media Node 5,196 343,486 6 FB15K237 Encyclopedic KG Link 14,541 310,116 237 WN18RR Lexical KG Link 40,943 93,003 11

E EXPERIMENTAL DETAILS

E.1 DATASETS

We pretrain MF-GIA on four source graphs: WikiCS (Mernyei & Cangea, 2020), PubMed (Yang et al., 2016), ogbn-Arxiv (Hu et al., 2020), and Amazon-ratings (Leskovec & Sosiˇc, 2016; Platonov et al., 2023). The pretrained model is evaluated on five held-out graphs on node-level tasks: Cora (Yang et al., 2016), ogbn-Products (Hu et al., 2020), Computers (Shchur et al., 2018), Physics (Shchur et al., 2018), and BlogCatalog (Yang et al., 2023), spanning citation, e-commerce, co-authorship, and social media domains. The pretrained model is also evaluated on edge-level tasks on FB15K237 (Bordes et al., 2013) and WN18RR (Dettmers et al., 2018), which are knowledge graphs from encyclopedic and lexical domains to predict relation types. Dataset statistics are summarized in Table 6. Note that although Amazon-ratings, ogbn-Products, and Computers are E-commerce networks, they form distinct domains: Amazon-ratings is labeled by average user rating per item, whereas ogbn-Products and Computers use product-category labels. We therefore treat them as separate domains.

<!-- Page 24 -->

Published as a conference paper at ICLR 2026

## 0 Epoch

1.4

1.6

1.8

Loss

(a) Training loss.

## 0 Epoch

0.2

0.3

0.4

0.5

0.6

0.7

Accuracy

(b) Validation accuracy.

**Figure 5.** Pretraining curves of MF-GIA.

E.2 BASELINE CONFIGURATIONS

We compare MF-GIA against two categories of baselines: (1) Traditional GNNs: GCN (Kipf & Welling, 2017), GAT (Veliˇckovi´c et al., 2018), and GraphSAGE (Hamilton et al., 2017); (2) Selfsupervised GNNs: GraphMAE (Hou et al., 2022), DGI (Veliˇckovi´c et al., 2019), and GraphCL (You et al., 2020); (3) GFM with post-training: GCOPE (Zhao et al., 2024), GFT (Wang et al., 2024b), AutoGFM (Chen et al., 2025), GPF (Fang et al., 2023), and All in One (Sun et al., 2023); (4) GFM with ICL: Prodigy (Huang et al., 2023), OFA (Liu et al., 2024a), and GraphAlign (Hou et al., 2024).

For traditional GNNs and Self-Supervised Methods, we pretrain on the same four datasets as our MF-GIA. Since these models lack in-context learning capabilities, we fine-tune them on the support set and evaluate on the query set for each episode. For GFMs with post-training (no ICL), we consider two pretraining regimes and report the stronger results: (1) pretraining on the same four graphs as MF-GIA, and (2) pretraining on the datasets used by the methods’ official implementations. For Prodigy, we compare two variants: one pretrained on our datasets and another on MAG240M (Hu et al., 2021) as in the original work, reporting the better result. For modality-dependent models (OFA, GraphAlign), which require text-attributed graphs (TAGs) and cannot operate on pre-encoded features, we use their original TAG datasets and implementations. To ensure fairness, all baselines follow the same episode protocol (identical m-way, k-shot support/query splits), use comparable backbones when applicable, and tune hyperparameters on validation episodes within the authors’ recommended ranges.

E.3 IMPLEMENTATION

We evaluate MF-GIA under the few-shot learning paradigm without any fine-tuning. For each test graph, we randomly sample k-shot support sets, where k = {1, 3, 5}, and evaluate on the remaining nodes. For node classification tasks, we measure classification accuracy and report the mean performance across 10 independent trials, each with randomly sampled support/query splits to ensure robustness of our results. For edge classification tasks, we focus on relation type prediction and conduct evaluation over 20 episodes to account for variance in the few-shot sampling process.

For the dimension alignment, we use SVD to unify all graphs’ feature dimensions to do = 64. The domain embedder uses a 2-layer CNN followed by a 1-layer MLP to project gradient fingerprints into 64-dimensional domain embeddings. For feature alignment, we also employ a 1-layer GNN encoder with a hidden dimension 64, followed by FiLM-based transformations. The label alignment uses a shared label base of dimension Lmax × 64. The DPAA mechanism consists of 1 attention layer with 1 head each. During pretraining, we use episodic meta learning with 10-way 5-shot tasks sampled from the pretraining graphs. We train for 10000 episodes using AdamW (Loshchilov & Hutter, 2017) with learning rate 0.005 and weight decay 0.0005. For gradient fingerprint computation, we use a fixed learning rate η = 0.01 for single-step updates. Fig. 5 illustrates the pretraining dynamics of MF-GIA. The training loss exhibits stable convergence, while validation accuracy shows consistent improvement before plateauing at approximately 6000 epochs, indicating effective model convergence.

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

**Table 7.** Effect of pretraining dataset composition on few-shot node classification accuracy (%). We systematically vary domain coverage from single to full four-domain pretraining. Results are 5-shot accuracy averaged over 20 episodes. Best results are bold.

Configuration Pretraining Datasets Domain Coverage In-Domain Out-of-Domain Avg OOD Overall Cora Products Physics BlogCatalog

Single

PubMed Citation 42.76 12.43 68.15 41.28 40.62 40.91 Arxiv Citation 48.31 13.86 76.42 43.67 44.65 45.57 WikiCS Web 39.23 14.72 65.83 45.91 42.15 41.67 Amazon E-commerce 35.47 17.28 61.26 38.74 39.09 38.19

Two

PubMed + Arxiv Citation 52.14 14.92 79.87 47.35 47.38 48.57 WikiCS + Amazon Web + E-commerce 41.68 18.35 67.42 48.26 44.68 43.93 PubMed + WikiCS Citation + Web 47.92 15.76 73.21 49.84 46.27 46.68 Arxiv + Amazon Citation + E-commerce 50.36 19.14 78.53 46.72 48.13 48.69

Three

PubMed + Arxiv + WikiCS w/o E-commerce 56.47 16.82 83.74 54.38 51.65 52.85 PubMed + Arxiv + Amazon w/o Web 57.82 20.67 85.91 52.16 52.91 54.14 PubMed + WikiCS + Amazon w/o Citation (Arxiv) 51.36 19.43 77.62 57.83 51.63 51.56 Arxiv + WikiCS + Amazon w/o Citation (PubMed) 59.24 21.38 86.73 60.47 56.19 56.96

Full

All Four Datasets Complete 63.98 22.61 88.92 67.31 59.61 60.73

F MORE EXPERIMENTS

F.1 EFFECT OF DOMAIN DIVERSITY IN PRETRAINING

**Table 7.** demonstrates that domain diversity is critical for MF-GIA to construct an effective domain embedding space that enables robust alignment (Zhuo & Tan, 2022) of downstream graphs. Singledataset pretraining yields limited performance, where Arxiv shows the strongest individual results due to its diverse academic content, providing richer domain signals. When combining two datasets, cross-domain pairs (e.g., Arxiv + Amazon: 48.69%) perform comparably to same-domain pairs (PubMed + Arxiv: 48.57%) despite Amazon’s weaker individual performance, indicating that structural diversity helps the domain embedder learn more generalizable alignment patterns beyond surface-level similarities. This effect amplifies with three datasets, where the configuration without PubMed (Arxiv + WikiCS + Amazon) achieves 56.96%, notably outperforming the configuration without Arxiv (51.56%), despite Arxiv’s superior standalone performance. This counterintuitive result reveals that once sufficient domain signals are captured, maintaining diverse structural patterns (Web link, E-commerce) becomes more valuable than redundant citation networks for constructing a comprehensive domain space. The full four-dataset model achieves optimal performance (60.73%), with remarkable generalization to entirely unseen domains like BlogCatalog (67.31%), validating that comprehensive domain coverage during pretraining enables the domain embedder to map novel graphs into appropriate subspaces of the learned domain space. These results confirm that MF-GIA’s domain-conditioned transformations require diverse pretraining to establish a rich domain embedding space where graphs from any domain, seen or unseen, can be effectively mapped and aligned based on their intrinsic characteristics.

F.2 EFFECT OF GRAPH PRE-ENCODER

**Table 8.** Performance of MF-GIA on Cora with different feature encodings.

Pre-encoder 1-shot 3-shot 5-shot

BoW 47.64 57.38 63.98 ST 48.37 62.79 68.54 RoBERTa 48.24 61.53 69.85 LLaMa2-7B 47.93 58.64 65.33

While the raw text data of the Cora dataset has been made available by Chen et al. (2024a), popular end-to-end GNN models typically utilize the pre-encoded version from Yang et al. (2016), which employs bag-of-words (BoW) encoding for node features. Modality-dependent GFMs such as GFT, AutoGFM, and OFA require access to raw text data and rely on specific language models, such as Sentence Transformer (ST) 1 (Reimers & Gurevych, 2019), LLaMa2- 7B 2 (Touvron et al., 2023), or RoBERTa 3 (Liu et al., 2019), to align the semantic space between the Cora dataset and their pretraining graphs. In contrast, MF-GIA demonstrates modality freedom, i.e., it operates directly on graphs with arbitrary pre-encoded features without requiring knowledge of the

1https://huggingface.co/sentence-transformers/multi-qa-distilbert-cos-v1 2https://huggingface.co/meta-llama/Llama-2-7b 3https://huggingface.co/FacebookAI/roberta-base

<!-- Page 26 -->

Published as a conference paper at ICLR 2026 encoding method. Whether a graph has been encoded using bag-of-words, advanced language models, or even unknown proprietary encoders, MF-GIA can seamlessly adapt to these features. The results in Table 2 employ the public bag-of-words features for MF-GIA. To validate our modality-free claim, in Table 8, we conduct additional experiments applying our pretrained model (without re-pretraining) to the graph pre-encoded through different pipelines. The results show that MF-GIA maintains its effectiveness regardless of the underlying feature encoding, confirming its ability to generalize across diverse pre-processing methods and enabling practical deployment in scenarios where encoding details are unknown or heterogeneous.

F.3 DIMENSION UNIFICATION

For GFMs, feature dimensions are unified before feeding data into the model because GFMs require inputs in a consistent format. We adopt SVD-based unification to achieve a fair comparison with baselines which isolates the contribution of our core innovation from preprocessing effects. Dedicated methods such as Domain-Invariant Aligner (DIA) (Yuan et al., 2025) provide more expressive and learnable pre-unifiers, which can be seamlessly integrated into our MF-GIA framework. Table 9 shows that our framework remains effective and compatible with advanced dimension unification techniques.

**Table 9.** Performance on MF-GIA with expressive dimension unification component.

## Method

Computers Physics BlogCatalog

1-shot 5-shot 1-shot 5-shot 1-shot 5-shot

MF-GIA 41.49 53.71 79.12 88.92 49.46 67.31 MF-GIA (w. DIA) 41.96 54.60 80.15 89.74 48.37 66.53

F.4 MORE PRETRAINING TASKS

**Table 10.** Performance of MF-GIA with additional pretraining tasks (5-shot).

ogbn-Products Computers FB15K237

MF-GIA 22.61 53.71 91.38 MF-GIA (w. link) 24.59 56.60 92.36

In this work, we pretrain our model on a small number of datasets to showcase its ability to adapt to diverse unseen domains and task types. The four datasets we use are among the widely adopted, publicly available, and easily accessible graph benchmarks. This design ensures that anyone can reproduce or extend our pretraining process without the need for extensive dataset curation, as common benchmarks already provide sufficient diversity to pretrain our model effectively. Here, we expand pretraining beyond node classification by adding link existence prediction and re-pretrain the model, denoted as MF-GIA (w. link), and report the inference results under the 5-shot setting in Table 10. It shows that a broader pretraining corpus yields consistent improvements on unseen domains.

F.5 STABILITY OF GRADIENT FINGERPRINTS

**Table 11.** Stability of gradient fingerprints.

Datasets Avg. Cosine Similarity Std. Dev. Min. Similarity

Physics 0.931 0.015 0.896 BlogCatalog 0.917 0.021 0.873

The stability of the gradient fingerprints is dependent on the size of the support set. From Lemma B.1, the gradient decomposes as ∇0L (θ0, G) = 1 |V |X⊤A · diag(g) · 1d, which reveals that the fingerprint aggregates information from domain-specific components including feature distribution X, graph structure A and label distribution g. As the support set size increases, the law of large numbers ensures that these aggregated statistics converge to their population expectations, making the gradient fingerprints increasingly stable. Here, we examine the fingerprint stability under a 5-shot setting. Take Physics and BlogCatalog datasets as examples, we randomly sample 20 different 5-shot support sets from all classes, and compute fingerprints ∆θ for each support set and feed it into the domain embedder to get the domain embedding. Then we can measure the stability by computing the pairwise cosine similarity between all domain embedding pairs from the same graph. The results are shown in

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

**Table 12.** Effect of τ on different datasets (5-shot).

τ ogbn-Products Computers FB15K237

0.05 21.45 52.10 91.82 0.2 (Default) 22.61 53.71 91.38 0.5 22.60 53.93 90.45 1 22.15 53.29 90.27

**Table 13.** Sensitivity of DPAA configurations

Computers Physics BlogCatalog

1-layer, 1-head (Shared) 53.71 88.92 67.31 1-layer, 1-head (Separated) 51.25 88.10 67.05 1-layer, 4-head 52.47 86.58 66.15 2-layer, 1-head 54.05 88.53 67.46 2-layer, 4-head 53.39 87.52 66.83

Table 11, where the high average cosine similarity and low standard deviation demonstrate that different support sets from the same domain produce highly consistent domain embeddings.

F.6 SENSITIVITY ANALYSIS

Sensitivity of the Temperature τ. The temperature parameter τ in Eq. (18) controls the sharpness of the softmax distribution over class predictions. We conduct systematic experiments varying τ ∈ {0.05, 0.2, 0.5, 1} across multiple datasets in Table 12. We can find that the default τ = 0.2 provides optimal balance, but the model is not highly sensitive to this hyperparameter within a reasonable range [0.2, 1]. However, as a foundation model, all trainable parameters and hyperparameters must remain fixed across all datasets and tasks. Thus, we set τ = 0.2 uniformly for all experiments both during pretraining and in-context inference without any task- and dataset-specific tuning.

Sensitivity of DPAA Configurations For the DPAA depth and number of heads, we directly adopt a single-layer and single-head design for complexity and generalization considerations. Adding more layers and heads would increase computational and memory costs and could introduce a higher risk of overfitting, whereas our goal is to keep the learning process efficient, lightweight, yet expressive. The results Table 2 and Table 3 already show that this simplest DPAA configuration outperforms baselines, which highlights the architectural strength of our approach rather than relying on heavy over-parameterization. Table 13 shows that the 1-layer 1-head and 2-layer 1-head settings achieve the best performance, with 1-layer 1-head offering the best trade-off between efficiency and effectiveness. Therefore, we adopt the 1-layer 1-head configuration as the unified default setting for all datasets in our experiments. Moreover, we conduct an ablation study comparing shared and separate weight matrices WK and WV in this table. The shared setting outperforms the separate setting, possibly because the latter introduces more parameters and is more prone to over-fitting, and shared parameters can effectively improve efficiency.

G THE USE OF LARGE LANGUAGE MODELS (LLMS)

In this paper, LLMs have been used solely for polishing the writing and identifying typographical errors. No LLMs were used for generating research content, analysis, or conclusions.
