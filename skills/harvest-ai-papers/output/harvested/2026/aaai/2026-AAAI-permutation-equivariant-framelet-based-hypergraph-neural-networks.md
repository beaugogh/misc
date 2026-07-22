---
title: "Permutation Equivariant Framelet-based Hypergraph Neural Networks"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39474
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39474/43435
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Permutation Equivariant Framelet-based Hypergraph Neural Networks

<!-- Page 1 -->

Permutation Equivariant Framelet-based Hypergraph Neural Networks

Ming Li1, Yi Wang2*, Chengling Gao1*, Lu Bai3, Yujie Fang1, Xiaosheng Zhuang2, Pietro Lio4

1Zhejiang Key Laboratory of Intelligent Education Technology and Application, Zhejiang Normal University, Jinhua, China 2Department of Mathematics, City University of Hong Kong, Hong Kong, China 3School of Artificial Intelligence, Beijing Normal University, Beijing, China 4Department of Computer Science and Technology, Cambridge University, UK mingli@zjnu.edu.cn, ywan72@cityu.edu.hk, chl gao@zjnu.edu.cn, bailu@bnu.edu.cn, yjfang@zjnu.edu.cn, xzhuang7@cityu.edu.hk, pl219@cam.ac.uk

## Abstract

Hypergraphs provide a natural and expressive framework for modeling high-order relationships, enabling the representation of group-wise interactions beyond pairwise connections. While hypergraph neural networks (HNNs) have shown promise for learning on such structures, existing models often rely on shallow message passing and lack the ability to extract multiscale patterns. Framelet-based techniques offer a principled solution by decomposing signals into multiple frequency bands. However, most prior framelet systems, particularly Haar-type ones, are sensitive to node ordering and fail to ensure consistent representations under permutation, leading to instability in hypergraph learning. To address this, we propose Permutation Equivariant Framelet-based Hypergraph Neural Networks (PEF-HNN), a novel framework that integrates multiscale framelet analysis with permutationconsistent learning. We construct a new family of permutation equivariant Haar-type framelets specifically designed for hypergraphs, supported by theoretical analysis of their stability and decomposition properties. Built upon these framelets, PEF-HNN incorporates both low-pass and high-pass components across multiple scales into a unified neural architecture. Extensive experiments on nine benchmark datasets, including three homophilic and four heterophilic hypergraphs, as well as two real-world datasets for visual object classification, demonstrate the effectiveness of our approach, consistently outperforming existing HNN baselines and highlighting the advantages of permutation equivariant framelet design in hypergraph representation learning.

## Appendix

— https://mingli-ai.github.io/PEF-HNN.pdf

## Introduction

Hypergraphs offer a natural way to model high-order relationships among entities by allowing hyperedges to connect arbitrary-sized subsets of nodes. This generalization of pairwise graphs makes hypergraphs especially suitable for representing group-wise interactions in real-world systems such as co-authorship networks, biological complexes, and multiparty communications (Antelmi et al. 2023; Zhang et al. 2024). Recent works (Wang and Kleinberg 2024; Mill´an

*Corresponding authors: Yi Wang, Chengling Gao Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

et al. 2025) have already demonstrated both theoretically and empirically the advantages of using hypergraphs directly, rather than simplifying them into pairwise graphs for specific problem formulations.

While hypergraph neural networks (HNNs) (Kim et al. 2024) have emerged as a promising tool for learning from such structures, most existing models rely on local or shallow message passing, which may be insufficient to capture the diverse and multiscale dependencies inherent in complex hypergraph data. To enhance representational power, recent works (Li et al. 2025a) have explored the integration of spectral techniques, such as wavelets (Hammond, Vandergheynst, and Gribonval 2011) and framelets (Dong 2017), into neural architectures. Framelets, in particular, enable multiscale decomposition of signals, allowing simultaneous extraction of smooth (low-frequency) and detailed (high-frequency) structural patterns (Zheng et al. 2021, 2022). However, a critical limitation persists: many existing framelet constructions, especially Haar-type framelets, are sensitive to node ordering. Since their bases often depend on hierarchical structures built from a specific node sequence, reordering the nodes while preserving the hypergraph structure can lead to inconsistencies in the generated framelet representations. This lack of permutation equivariance undermines the stability and reproducibility of learned features, especially in hypergraph settings where the structural complexity magnifies sensitivity to input permutations. While recent advances have proposed permutation equivariant framelets for standard graphs (Li et al. 2024), the extension to hypergraphs remains unexplored.

To address this gap, we propose a novel framework, Permutation Equivariant Framelet-based Hypergraph Neural Networks (termed PEF-HNN), which combines the strengths of multiscale framelet analysis with permutationconsistent representation learning on hypergraphs. At the core of our framework lies a new design of Haar-type framelets that are permutation equivariant and specifically tailored for hypergraph structures, constructed based on hierarchical decompositions of node groups derived from hyperedge incidence. These framelets ensure that the transformation of node signals remains consistent under arbitrary reordering. Built on this foundation, PEF-HNN incorporates multi-scale framelet transforms as input chan-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

23079

<!-- Page 2 -->

nels within a unified neural architecture, enabling effective capture of both low-pass and high-pass components across multiple structural resolutions. We evaluate PEF-HNN on hypergraph node classification tasks using nine benchmark datasets, including three homophilic and four heterophilic hypergraphs, as well as two real-world datasets for visual object classification. Extensive comparisons against existing HNN baselines demonstrate the compelling performance of our model, highlighting the benefits of constructing permutation equivariant framelets for enhancing hypergraph representation learning.

In summary, our contributions are three-fold:

• Theoretical Result: We construct a new family of permutation equivariant Haar-type framelets on hypergraphs and provide theoretical analysis of their key properties, enabling stable and consistent multiscale decomposition under arbitrary node reorderings; • Model Development: We propose PEF-HNN, a novel framework that integrates permutation equivariant framelet-based multiscale representations into hypergraph neural networks for effective hypergraph learning; • Experimental Study: We validate the effectiveness of PEF-HNN through extensive experiments on nine benchmark datasets, including three homophilic and four heterophilic hypergraphs, as well as two real-world datasets for visual object classification. The results consistently show performance gains over existing HNN baselines, underscoring the benefits of incorporating permutation equivariant framelet design in hypergraph learning.

## Related Work

Hypergraph neural networks (HNNs) have emerged as powerful tools for modeling high-order relational structures, where each hyperedge can connect an arbitrary subset of nodes. Classical models such as HGNN (Feng et al. 2019) and HyperGCN (Yadati et al. 2019) extend traditional graph neural networks (GNNs) by using incidence matrix-based propagation or clique expansion techniques. However, these methods primarily rely on shallow message passing and are constrained by their inability to effectively capture multiscale or high-frequency information inherent in complex hypergraphs. To improve learning capacity, UniGCNII (Huang and Yang 2021) introduces deep architectures with identity and residual connections to mitigate oversmoothing, while ED-HNN (Wang et al. 2023) incorporates edge-dependent transformations for more flexible and adaptive aggregation. Set-based approaches such as AllDeepSets and AllSetTransformer (Chien et al. 2022) treat each hyperedge as a set and model intra-hyperedge interactions through permutationinvariant functions, offering a principled way to handle unordered node sets and dynamic hyperedge cardinality. Nevertheless, these models largely ignore the global hierarchical structure of hypergraphs and often lack a spectral or frequency-aware perspective.

To overcome the limitations of local aggregation, recent efforts have explored spectral methods for hypergraph learning. For example, Li et al. (2025a,b) propose framelet-based

HNNs that construct multiscale representations using hypergraph Laplacian eigenbases. These spectral framelets enable the decomposition of node features into low- and highfrequency components, allowing the model to capture both smooth and oscillatory patterns. However, such Laplacianinduced framelet transforms are sensitive to node orderings and are typically designed in a global and rigid fashion, without accounting for the hierarchical or local multiscale structure within the hypergraph. As a result, they lack permutation consistency, meaning that reordering the input nodes can yield inconsistent feature representations and unstable learning outcomes. PEGFAN (Li et al. 2024) introduces Haar-type framelets with explicit permutation equivariance for standard graph neural networks. By constructing hierarchical trees over graph nodes and defining framelets in a spatially localized manner, PEGFAN achieves consistent multiscale decomposition regardless of node ordering. This property is crucial for learning robust representations and ensuring stability across varying graph structures. However, the extension of permutation equivariant framelets to hypergraphs has not been systematically studied. Hypergraphs present additional challenges due to their higher-order connectivity and more complex combinatorial structures, which require novel design principles beyond those developed for pairwise graphs.

Motivated by these observations, our work develops a new family of permutation equivariant Haar-type framelets specifically designed for hypergraphs. By leveraging hyperedge-induced hierarchical groupings, we construct localized framelet transforms that preserve equivariance under node permutations and support multiscale signal extraction. These framelets are integrated into a unified HNN framework, enabling robust and expressive hypergraph representation learning across both homophilic and heterophilic structures.

## 3 Proposed

## Method

## 3.1 Notation and

Preliminaries A hypergraph is represented as G = (V, E), comprising a vertex set V of size N = |V|, a hyperedge set E of size M = |E|. Suppose that vertices and hyperedges have feature dimensions d and m, respectively, we have the representation of vertex data as X ∈RN×d and hyperedge data as Y ∈RM×o.

The hypergraph structure, from a vertex perspective, is defined by an incidence matrix H ∈{0, 1}N×M where H(v, e) = 1 if vertex v is contained in hyperedge e, and 0 otherwise, as represented by:

H(v, e) =

1, if v ∈e; 0, otherwise. (1)

The degrees of vertex v and hyperedge e are denoted by diagonal matrices Dv ∈RN×N and De ∈RM×M, calculated as P e∈E H(v, e) and P v∈V H(v, e), respectively.

## 3.2 Construction of Permutation Equivariant Framelets on

Hypergraphs A hypergraph signal f = [f1,..., fN]⊤∈RN is considered as f: V = {1, 2,..., N} →R with ℓ2 norm

23080

<!-- Page 3 -->

∥f∥2 = PN i=1 |fi|2 < ∞. All such signals form a Hilbert space L2(G) under the usual inner product ⟨f, g⟩:= f ⊤g for f, g ∈L2(G). A collection {ei: i ∈[I]} ⊂L2(G) is a tight frame of L2(G) if f = PI i=1⟨f, ei⟩ei for all f ∈L2(G), where we denote [I]:= {1,..., I}. We denote the i-th column vector and row vector of a matrix M, by M:i and Mi:, respectively. For K ≥2, we call a sequence PK:= {Vj: j = 1,..., K} of sets as a K-hierarchical clustering of V if each Vj:= {sΛ ⊂V: dim(Λ) = j} is a partition of V, i.e., V = ∪ΛsΛ, and Vj is a refinement of Vj−1, where we use the index vector Λ = (λ1,..., λj) ∈ Nj to encode position, level j, and parent-children relationship, of the clusters sΛ, and dim(Λ) is the length of the index vector. If sΛ ∈Vj is a parent, then the index vectors of its children are appended with an integer, i.e. (Λ, i), indicating its i-th child, and thus the child is denoted by s(Λ,i) ∈Vj+1. Then we have the parent-children relationship s(Λ,i) ⊂sΛ. We denote the number of children of sΛ by LΛ. Unless specified, we consider K-hierarchical clustering PK with VK = {{1},..., {N}} and V1 = {[N]} being a singleton, i.e., PK is a tree.

Given PK and any j0 ∈[K], we next define a sequence of framelet systems

Fj0(PK):={ϕΛ: dim(Λ) = j0}

∪{ψΛ: dim(Λ) = j}K j=j0+1

(2)

of scaling vectors ϕΛ and framelet vectors ψ(Λ,m) in L2(G). For the scaling vectors ϕΛ, they are defined iteratively from dim(Λ) = K to dim(Λ) = 1. When dim(Λ) = K, each cluster (node) sΛ contains only one vertex in hypergraph G, and we define ϕΛ = I:i, where i ∈sΛ ⊂V and I:i is the i-th column of the identity matrix I ∈RN×N. When dim(Λ) < K, we define ϕΛ:=

X ℓ∈[LΛ]

p(Λ,ℓ)ϕ(Λ,ℓ), (3)

where pΛ,ℓ ≡ 1 √LΛ. Obviously, ϕΛ is with support suppϕΛ = sΛ and ∥ϕΛ∥= 1. For the framelet vectors, we define ψ(Λ,i), i ∈[IΛ] with IΛ:= LΛ(LΛ−1)

2 by ψ(Λ,i):=

X ℓ∈[LΛ]

(BΛ)i,ℓϕ(Λ,ℓ), (4)

where the matrices BΛ ∈RIΛ×LΛ are defined row-by-row with its i-th row [BΛ]i: = [w1,..., wLΛ] being given by wτ =

  

 

1 √LΛ τ = ℓ1;

−1 √LΛ τ = ℓ2; 0 otherwise.

(5)

Here 1 ≤ℓ1 < ℓ2 ≤LΛ is uniquely determined by i = i(ℓ1, ℓ2, LΛ) = (2LΛ−ℓ1)(ℓ1−1)

2 + ℓ2 −ℓ1. In short, the row of BΛ is obtained by permutating the row vector

1 √LΛ [1, −1, 0,..., 0].

## 3.3 Theoretical Properties Theorem 1 shows that

Fj0(PK) is a tight frame.

Theorem 1. Let Fj0(PK) be defined as by (2). Then Fj0(PK) is a tight frame of L2(G) for any j0 ∈[K].

Proof. We prove the result by induction on j0. Obviously, for j0 = K, FK(PK) = {I:i}N i=1 is simply the orthonormal basis and thus a tight frame. Suppose for j0 = k + 1, Fk+1(PK) is tight. We need to show that Fk(PK) is tight. That is, for all f ∈L2(G), we have f =

X dim(Λ)=k

⟨f, ϕΛ⟩ϕΛ +

K X j=k+1

X dim(Λ)=j

⟨f, ψΛ⟩ψΛ.

By the induction hypothesis, we only need to show

X dim(Λ)=k

⟨f, ϕΛ⟩ϕΛ +

X dim((Λ,i))=k+1

⟨f, ψ(Λ,i)⟩ψ(Λ,i)

=

X dim(Λ)=k+1

⟨f, ϕΛ⟩ϕΛ.

By definition of ϕΛ and ψ(Λ,i) in (3) and (4), it is equivalent to that for each Λ with dim(Λ) = k, it holds pΛp⊤

Λ + B⊤

ΛBΛ = I, where pΛ:= [p(Λ,1),..., p(Λ,LΛ)]⊤≡ 1 √LΛ 1 is the constant vector and BΛ is the matrix defined in (5), which is true thanks to the structures of pΛ and BΛ. Therefore, Fk(PK) is tight.

We have the following remarks concerning the properties of Fj0(PK).

Remark 1. Let Fj0(PK):= {ϕΛ, dim(Λ) = j0} ∪ {ψΛ, dim(Λ) = j}K j=j0+1 =: {ui}IG i=1 with IG the total number of vectors in Fj0(PK). We denote F:= [u1,..., uIG]⊤∈RIG×N to be its matrix representation. Then, by the tight frame property, we have F⊤F = I ∈ RN×N.

Remark 2. If for all Λ, we have LΛ ≤h for some integer h ≥2, then K = O(logh N). One can show that the total number IG is of order IG = O(Nh) and hence the total number nnz(F) of nonzero entries of F is of order nnz(F) = O(Nh logh N). In practice, h is usually small (e.g., 2, 4, or 8), and hence F is a sparse matrix. Thus, F can be stored as a sparse matrix and the framelet coefficient vectors ˆf:= Ff can be computed efficiently with the computational complexity of order O(Nh logh N).

Let π: V →V be a reordering (relabeling, bijection) of V = {1, 2,..., N}, i.e., π is w.r.t. a permutation on [N] with π(V) = {π(1),..., π(N)}. We denote π(G) = (π(V), π(E)) with π(E):= {π(e): e ∈E} being given by π(e):= {π(v): v ∈e}. The corresponding signal f on G is reordered to be π(f) under the newly ordered π(G). In other words, given a π, there exists a permutation matrix Pπ of size N × N such that π(f) = Pπf. Fix G = (V, E) and PK. Denote our construction of F = Fj0(PK) by

A(G, PK) = F.

23081

<!-- Page 4 -->

For each permutation π, the construction A is called permutation equivariant if

A (π(G), PK) = π (A(G, PK)), where π(F):= FPπ. We have the following result concerning the permutation equivariant property of our construction of Fj0(PK) with respect to the reordering of V.

Theorem 2. For any permutation π, we have A (π(G), PK) = π(A(G, PK)).

Proof. Let ΦΛ:= [ϕ(Λ,1),..., ϕ(Λ,LΛ)]⊤and ΨΛ:= [ψ(Λ,1),..., ψ(Λ,IΛ)]⊤. Since the scaling vectors ϕ⊤

Λ = p⊤

ΛΦΛ are defined iteratively for dim(Λ) decreasing from K to 1 and the framelets ψ(Λ,m) are given by ΨΛ = BΛΦΛ, we only need to prove the permutation equivariant properties for each Λ. Note that ϕ(Λ,ℓ): V →R only depends on G, PK, and pΛ = 1 √LΛ 1. For any permutation π, the PK is determined by the index vectors Λ according to a tree structure and is independent of the permutation π. Moreover, the vectors pΛ are fixed constants. Hence, iteratively, after the permutation π acting on G, the new scaling vector ϕπ

(Λ,ℓ): π(V) →R is given by ϕπ

(Λ,ℓ) = Pπϕ(Λ,ℓ), where Pπ is the permutation matrix with respect to π. Consequently, the new Φπ

Λ and Ψπ

Λ on the permuted hypergraph π(G) are given by Φπ

Λ = ΦΛPπ and Ψπ

Λ = BΛΦπ

Λ = BΛΦΛPπ = ΨΛPπ. This implies the conclusion.

Remark 3. Theorem 2 shows that framelet system F = Fj0(PK) is permutation equivariant when reordering node indices. We call F a permutation equivariant framelet (PEF) system.

## 3.4 Hypergraph Neural Networks with PEF

After constructing the permutation equivariant framelet (PEF) system (see the above section), we can design Hypergraph Neural Networks with PEF, termed as PEF-HNN, as follows:

X(ℓ+1) =σ

(1 −αℓ)F⊤diag(θ)FX(ℓ) + αℓX(0)

·

(1 −βℓ)I + βℓΘ(ℓ)

,

(6)

where θ ∈RIG is the learnable filter, F ∈RIG×N denotes framelet matrix representation of our PEF system.

Theorem 3. Let G = (V, E) be a hypergraph with feature matrix X(0) and a K-hierarchical partition PK. Let P be a permutation matrix w.r.t. a permutation π on V. If the permuted feature matrix P X(0) and framelet system π(A(G, PK)) are used in the PEF-HNN network (6), then the new output X(ℓ+1)

P of each layer differs from the original one by a permutation matrix, i.e. X(ℓ+1)

P = P X(ℓ+1).

Proof. Let F:= A(G, PK). Then we have Fπ:= π(A(G, PK)) = FP. Thus, (by induction on ℓ), we have

X(ℓ+1)

P = σ

(1 −αℓ)F⊤ π diag(θ)FπP X(ℓ) + αℓP X(0)

·

(1 −βℓ)I + βℓΘ(ℓ)

= σ

(1 −αℓ)P F⊤diag(θ)FX(ℓ) + αℓP X(0)

·

(1 −βℓ)I + βℓΘ(ℓ)

= P X(ℓ+1).

## Experiments

## 4.1 Datasets

We evaluate the performance of PEF-HNN across a diverse collection of hypergraph datasets spanning various domains. Specifically, we use seven publicly available real-world hypergraph datasets: Cora, Citeseer, and Cora-CA (covering both cocitation and coauthorship networks) (Yadati et al. 2019), Actor and Twitch (Li et al. 2025b), as well as Senate and House (Fowler 2006; Chodrow, Veldt, and Benson 2021). These datasets are categorized based on the hyperedge homophily ratio Hedge (Li et al. 2025b), where datasets with Hedge > 0.5 are labeled homophilic, and those with Hedge ≤0.5 are labeled heterophilic. In addition, we include two real-world datasets for visual object classification: the 3D NTU2012 dataset (Chen et al. 2003) and the Princeton ModelNet40 dataset (Wu et al. 2015), which evaluate the model’s capability in geometric understanding and 3D shape classification.

## 4.2 Baselines and Implementation Details

We adopt different data splits for training, validation, and testing according to standard practices. For Actor and Twitch, we follow the 40%/20%/40% split introduced in (Wang et al. 2023), while the remaining datasets use a 50%/25%/25% split following (Li et al. 2025b). PEF-HNN is evaluated against two groups of baseline methods: (i) general-purpose HNNs, including HGNN (Feng et al. 2019), HyperGCN (Yadati et al. 2019), UniGCNII (Huang and Yang 2021), AllDeepSets, and AllSetTransformer (Chien et al. 2022); and (ii) heterophily-aware HNNs, specifically ED-HNN (Wang et al. 2023) and HyperUFG (Li et al. 2025b). Additional experimental settings as well as the code link are provided in the Appendix.

All experiments are implemented in PyTorch and conducted on a single NVIDIA RTX A6000 GPU with 48GB memory. We use the Adam optimizer (Kingma and Ba 2014) and perform grid search to tune hyperparameters. The learning rate is selected from {5e−3, 3e−3, 2e−3, 1e−3, 5e−2, 3e−2, 2e−2, 1e−2}; weight decay from {5e−5, 1e−5, 5e−4, 1e−4, 5e−3, 1e−3}; hidden dimensions from {32, 64, 128, 256, 512, 1024}; and the number of layers from the range [1, 128]. For baseline methods, we report published results when available. Otherwise, we reproduce results using the original implementations provided by the authors.

23082

<!-- Page 5 -->

## Methods

Cora Citeseer Cora-CA Actor Twitch Senate House Hom. ratio, Hedge 0.7462 0.6814 0.7797 0.4675 0.4857 0.4642 0.4851

HGNN 79.39 ± 1.36 72.45 ± 1.16 82.64 ± 1.65 74.47 ± 0.32 51.88 ± 0.26 48.59 ± 4.52 61.39 ± 2.96 HyperGCN 78.45 ± 1.26 71.28 ± 0.82 79.48 ± 2.08 68.67 ± 4.38 51.32 ± 1.02 42.45 ± 3.67 48.32 ± 2.93 UniGCNII 78.81 ± 1.05 73.05 ± 2.21 83.60 ± 1.14 80.48 ± 1.13 50.84 ± 0.76 49.30 ± 4.25 67.25 ± 2.57 AllDeepSets 76.88 ± 1.80 70.83 ± 1.63 81.97 ± 1.50 82.00 ± 2.33 50.72 ± 0.96 52.82 ± 3.20 51.70 ± 3.37 AllSetTransformer 78.58 ± 1.47 73.08 ± 1.20 83.63 ± 1.47 83.39 ± 1.73 50.45 ± 0.76 51.83 ± 5.22 69.33 ± 2.20

ED-HNN 80.31 ± 1.35 73.70 ± 1.38 83.97 ± 1.55 91.86 ± 0.43 50.86 ± 0.88 64.79 ± 5.14 72.45 ± 2.28 HyperUFG 81.51 ± 0.99 74.72 ± 2.10 85.18 ± 0.69 89.32 ± 0.75 52.35 ± 0.04 67.61 ± 7.00 72.82 ± 2.22

PEF-HNN (Ours) 81.51 ± 0.98 74.96 ± 1.77 86.00 ± 0.71 90.27 ± 2.13 53.18 ± 0.37 68.45 ± 6.84 73.25 ± 1.55

**Table 1.** Performance comparison between PEF-HNN and baselines on classification accuracy (%) across three homophilic and four heterophilic hypergraphs. The best results are shown in bold, and the second-best are underlined.

1 2 4 8 16 32 64 128 The Number of Layers

0

25

50

75

100

Accuracy (%)

PEF-HNN ED-HNN AllDeepSets HGNN UniGCNII AllSetTranformer HyperUFG

1 2 4 8 16 32 64 128 The Number of Layers

0

20

40

60

80

Accuracy (%)

PEF-HNN ED-HNN AllDeepSets HGNN UniGCNII AllSetTranformer HyperUFG

1 2 4 8 16 32 64 128 The Number of Layers

0

20

40

60

80

Accuracy (%)

PEF-HNN ED-HNN AllDeepSets HGNN UniGCNII AllSetTranformer HyperUFG

**Figure 1.** Comparison of the models’ ability to alleviate oversmoothing: Cora-CA (left), Senate (middle), House (right).

## 4.3 Results and Discussion

We thoroughly evaluate PEF-HNN on diverse hypergraphs with varying homophily levels, comparing it to both conventional HNNs and recent heterophilic-specific models. As shown in Table 1, PEF-HNN achieves competitive or superior performance across homophilic (Cora, Citeseer, Cora-CA) and heterophilic (Actor, Twitch, Senate, House) datasets. It attains top accuracy on Cora-CA (86.00%) and matches top results on Cora, while outperforming others on Twitch, Senate, and House, remaining competitive on Actor.

Compared to general HNNs, PEF-HNN performs more stably across homophilic and heterophilic settings. It also surpasses specialized heterophilic models on three of four datasets. These results underscore the benefit of permutation equivariant framelets, which enable PEF-HNN to capture both coarse and fine-grained structural patterns, ensuring robust and generalizable performance across varying hypergraph structures.

## 4.4 Ability to Alleviate Oversmoothing

We also study empirically the ability of PEF-HNN to alleviate oversmoothing as the number of layers increases. Figure 1 presents accuracy trends on three representative datasets: Cora-CA (left), Senate (middle), and House (right) as the number of layers increases from 1 to 128. We compare PEF-HNN with HGNN, UniGCNII, AllDeepSets, AllSet- Transformer, ED-HNN, and HyperUFG.

Among the baselines, UniGCNII benefits from residual connections and maintains moderate performance at deeper layers on Cora-CA. However, its accuracy drops significantly beyond two layers on the heterophilic Senate and House datasets. ED-HNN performs competitively on Senate and House at shallower depths but exhibits sharp degradation and higher variance after 8 layers on Cora-CA. Hyper- UFG remains relatively stable across all three datasets, yet its performance does not consistently improve with depth. In contrast, PEF-HNN demonstrates strong resistance to oversmoothing and consistently benefits from increased depth. On all three datasets, its accuracy either improves or remains steady as the number of layers increases, with notably lower variance compared to other methods. This indicates that the integration of permutation equivariant framelet transforms enables effective multi-scale representation learning while preserving discriminative features even in very deep architectures. These results demonstrate that PEF-HNN effectively avoids oversmoothing on both homophilic and heterophilic hypergraphs, even at large depths.

## 4.5 Parameter Sensitivity Analysis

We investigate the sensitivity of PEF-HNN to two key hyperparameters, α and β, which influence the architectural dynamics of the model. As illustrated in Figure 2, we conduct univariate experiments by varying each parameter independently in the range {0.1, 0.2,..., 0.9} on three representative datasets: Cora, Senate, and House. The parameter α controls the trade-off between the current node features and their initial representations, whereas β modulates the relative importance of the initial features in each layer via

23083

<!-- Page 6 -->

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0

25

50

75

100

Accuracy (%)

**Figure 2.** Sensitivity analysis of α (top row) and β (bottom row) on Cora (left), Senate (middle), and House (right) datasets.

Cora Citeseer Cora-CA Actor Twitch Senate House

Full model 81.51 ± 0.98 74.96 ± 1.77 86.00 ± 0.71 90.27 ± 2.13 53.18 ± 0.37 68.45 ± 6.84 73.25 ± 1.55 w/o high pass 81.39 ± 1.17 75.06 ± 2.01 85.58 ± 1.00 88.71 ± 2.76 51.32 ± 0.89 67.32 ± 6.53 71.98 ± 1.76 w/o low pass 81.45 ± 0.99 74.81 ± 2.00 85.44 ± 0.72 89.12 ± 2.55 52.63 ± 1.04 66.34 ± 7.38 72.26 ± 1.83

**Table 2.** Ablation study evaluating the impact of low-pass and high-pass components in PEF-HNN.

a decaying schedule. Experimental results show that PEF- HNN maintains stable performance across a broad range of values for both parameters. In particular, model accuracy is moderately affected by α, indicating its importance in preserving useful initial information. In contrast, the model is less sensitive to β, likely due to its diminishing influence over deeper layers. Overall, these results suggest that PEF- HNN is robust to the choice of α and β, and does not require fine-grained tuning to achieve strong performance.

## 4.6 Ablation Study

We conduct an ablation study to evaluate the individual contributions of the low-pass and high-pass components in PEF- HNN. As shown in Table 2, removing either component leads to performance degradation across most datasets, confirming the effectiveness of the full multi-scale design. On heterophilic datasets (Actor, Twitch, Senate, and House), the absence of high-pass signals results in notable accuracy drops, underscoring their role in capturing fine-grained, discriminative features. On homophilic datasets (Cora, Citeseer, and Cora-CA), low-pass filtering is essential, while high-pass components still provide complementary benefits by capturing local variations. Overall, both low-pass and high-pass components are critical for achieving robust performance across hypergraphs with varying degrees of homophily.

## 4.7 Visualization

To qualitatively assess the representation quality, we visualize the original input features and the aggregated deep representations learned by various HNNs on a homophilic dataset (Citeseer) and a heterophilic dataset (House), as shown in Figure 3. The original features exhibit unclear or overlapping class distributions. On Citeseer, most methods produce reasonably separable clusters, though HGNN and UniGCNII show evident class mixing. ED-HNN and PEF- HNN yield cleaner separation, with PEF-HNN producing the most compact and distinct clusters. On the heterophilic House dataset, HGNN fails to distinguish class boundaries, and UniGCNII and ED-HNN provide partial improvements. In contrast, PEF-HNN forms clearly separated and wellstructured clusters, demonstrating its superior ability to capture discriminative features in both homophilic and heterophilic settings.

## 4.8 Visual Object Classification

To further assess the generalization capability of PEF-HNN beyond graph benchmarks, we apply it to the task of 3D visual object classification. Specifically, we conduct experiments on two publicly available real-world datasets: Model- Net40 (Wu et al. 2015), a large-scale CAD model benchmark widely used in shape classification, and NTU2012 (Chen et al. 2003), a smaller but challenging dataset consisting of geometric 3D models with high intra-class variability. Hypergraph Construction. We construct both single-view and multi-view hypergraphs based on shape features extracted from two well-established deep architectures: Multiview Convolutional Neural Network (MVCNN)(Su et al. 2015) and Group-View Convolutional Neural Network (GVCNN)(Feng et al. 2018). In the single-view setting, each 3D object is embedded into either the MVCNN or GVCNN feature space, and a hypergraph is constructed using the knearest neighbor (k-NN) approach: each object is treated as a centroid and connected to its k nearest neighbors to form one hyperedge. This procedure results in N hyperedges for N objects, where the structure reflects local simi-

23084

<!-- Page 7 -->

Original Feature HGNN UniGCNII ED-HNN PEF-HNN

**Figure 3.** Visualization comparison of raw input features and learned representations on Citeseer (top) and House (bottom).

Feature GCN HGNN PEF-HNN

GVCNN 91.8% 92.6% 97.2% MVCNN 86.7% 91.0% 92.1% GVCNN&MVCNN 94.4% 96.7% 98.4% Feature GCN HGNN PEF-HNN

GVCNN 78.8% 82.5% 93.3% MVCNN 71.3% 75.6% 89.1% GVCNN&MVCNN 76.1% 84.2% 91.4%

**Table 3.** Comparison between GCN, HGNN and PEF-HNN on ModelNet40 (top) and NTU2012 (bottom).

## Methods

Accuracy

PointNet (Qi et al. 2017a) 89.2% PointNet++ (Qi et al. 2017b) 90.7% PointCNN (Li et al. 2018) 91.8% SO-Net (Li, Chen, and Lee 2018) 93.4% Point-UMAE (Zeng et al. 2025) 94.2%

HGNN (Feng et al. 2019) 96.7% ED-HNN (Wang et al. 2023) 98.3%

PEF-HNN 98.4%

**Table 4.** Performance comparison of state-of-the-art classification methods on ModelNet40.

larities in the selected feature space. For the multi-view setting, we independently perform k-NN hyperedge construction in both feature spaces and then concatenate the resulting hyperedge incidence matrices. This fused representation integrates complementary information from both MVCNN and GVCNN, thereby enriching the relational structure used in PEF-HNN. Full implementation details and hyperparameter choices are provided in the Appendix. Performance Comparison. As shown in Tables 3 and 4,

PEF-HNN consistently achieves superior performance across both ModelNet40 and NTU2012 benchmarks. On ModelNet40, it attains the highest classification accuracy of 98.4%, outperforming strong point-based models such as PointCNN (91.8%) and Point-UMAE (94.2%), as well as existing hypergraph methods like HGNN and ED-HNN. This highlights the effectiveness of our permutation equivariant framelet design in capturing structured geometric information. Furthermore, PEF-HNN demonstrates robust performance across different feature extraction settings: when using single-view embeddings (MVCNN or GVCNN), it consistently surpasses both GCN and HGNN on both datasets. Notably, the multi-view fusion setting (combining GVCNN and MVCNN) further boosts accuracy, allowing PEF-HNN to leverage complementary shape features for more discriminative representations. These results collectively confirm that PEF-HNN is well-suited for visual object classification and generalizes effectively to complex, real-world hypergraph structures.

## 5 Conclusion

This paper proposes PEF-HNN, a permutation-equivariant framelet-based hypergraph neural network for multiscale representation learning. By designing Haar-type framelets specifically tailored for hypergraph structures and ensuring consistency under node reordering, our method overcomes limitations of prior framelet approaches and captures both global and local structures. Experiments on multiple benchmarks and two real-world visual object classification datasets demonstrate its effectiveness in homophilic and heterophilic settings. For future work, it is promising to extend PEF-HNN to dynamic or temporal hypergraphs. It is also desirable to develop theoretical studies on the stability and generalization of PEF-HNN, building on theoretical results for GNNs (Yang et al. 2025). Moreover, combining permutation-equivariant framelets with other high-order signal-processing techniques is expected to improve generalization and interpretability across broader learning tasks.

23085

<!-- Page 8 -->

## Acknowledgements

This work was supported in part by the “Pioneer” and “Leading Goose” R&D Program of Zhejiang (No. 2024C03262), and the National Natural Science Foundation of China (No. U21A20473, No. 62172370, No. 62536006, No. 62576371). X. Zhuang was supported in part by the Research Grants Council of Hong Kong (Project no. CityU 11309122, CityU 11302023, CityU 11301224, and CityU 11300825).

## References

Antelmi, A.; Cordasco, G.; Polato, M.; Scarano, V.; Spagnuolo, C.; and Yang, D. 2023. A survey on hypergraph representation learning. ACM Computing Surveys, 56(1): 1–38. Chen, D.-Y.; Tian, X.-P.; Shen, Y.-T.; and Ouhyoung, M. 2003. On visual similarity based 3D model retrieval. Computer Graphics Forum, 22(3): 223–232. Chien, E.; Pan, C.; Peng, J.; and Milenkovic, O. 2022. You are AllSet: A multiset function framework for hypergraph neural networks. In ICLR. Chodrow, P. S.; Veldt, N.; and Benson, A. R. 2021. Generative hypergraph clustering: From blockmodels to modularity. Science Advances, 7(28): eabh1303. Dong, B. 2017. Sparse representation on graphs by tight wavelet frames and applications. Applied and Computational Harmonic Analysis, 42(3): 452–479. Feng, Y.; You, H.; Zhang, Z.; Ji, R.; and Gao, Y. 2019. Hypergraph neural networks. In AAAI, 3558–3565. Feng, Y.; Zhang, Z.; Zhao, X.; Ji, R.; and Gao, Y. 2018. GVCNN: Group-view convolutional neural networks for 3D shape recognition. In CVPR, 264–272. Fowler, J. H. 2006. Legislative cosponsorship networks in the US House and Senate. Social Networks, 28(4): 454–465. Hammond, D. K.; Vandergheynst, P.; and Gribonval, R. 2011. Wavelets on graphs via spectral graph theory. Applied and Computational Harmonic Analysis, 30(2): 129–150. Huang, J.; and Yang, J. 2021. UniGNN: A unified framework for graph and hypergraph neural networks. In IJCAI, 2563–2569. Kim, S.; Lee, S. Y.; Gao, Y.; Antelmi, A.; Polato, M.; and Shin, K. 2024. A survey on hypergraph neural networks: An in-depth and step-by-step guide. In KDD, 6534–6544. Kingma, D. P.; and Ba, J. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980. Li, J.; Chen, B. M.; and Lee, G. H. 2018. SO-Net: Selforganizing network for point cloud analysis. In CVPR, 9397–9406. Li, J.; Zheng, R.; Feng, H.; Li, M.; and Zhuang, X. 2024. Permutation equivariant graph framelets for heterophilous graph learning. IEEE Transactions on Neural Networks and Learning Systems, 35(9): 11634–11648. Li, M.; Fang, Y.; Wang, Y.; Feng, H.; Gu, Y.; Bai, L.; and Lio, P. 2025a. Deep hypergraph neural networks with tight framelets. In AAAI, 18385–18392. Li, M.; Gu, Y.; Wang, Y.; Fang, Y.; Bai, L.; Zhuang, X.; and Lio, P. 2025b. When hypergraph meets heterophily: New benchmark datasets and baseline. In AAAI, 18377–18384.

Li, Y.; Bu, R.; Sun, M.; Wu, W.; Di, X.; and Chen, B. 2018. PointCNN: Convolution on X-transformed points. In NeurIPS, 652–660. Mill´an, A. P.; Sun, H.; Giambagli, L.; Muolo, R.; Carletti, T.; Torres, J. J.; Radicchi, F.; Kurths, J.; and Bianconi, G. 2025. Topology shapes dynamics of higher-order networks. Nature Physics, 21: 353––361. Qi, C. R.; Su, H.; Mo, K.; and Guibas, L. J. 2017a. Point- Net: Deep learning on point sets for 3D classification and segmentation. In CVPR. Qi, C. R.; Yi, L.; Su, H.; and Guibas, L. J. 2017b. Point- Net++: Deep hierarchical feature learning on point sets in a metric space. In NIPS, 5105–5114. Su, H.; Maji, S.; Kalogerakis, E.; and Learned-Miller, E. 2015. Multi-view convolutional neural networks for 3D shape recognition. In ICCV, 945–953. Wang, P.; Yang, S.; Liu, Y.; Wang, Z.; and Li, P. 2023. Equivariant hypergraph diffusion neural operators. In ICLR. Wang, Y.; and Kleinberg, J. 2024. From graphs to hypergraphs: Hypergraph projection and its reconstruction. In ICLR. Wu, Z.; Song, S.; Khosla, A.; Yu, F.; Zhang, L.; Tang, X.; and Xiao, J. 2015. 3D ShapeNets: A deep representation for volumetric shapes. In CVPR, 1912–1920. Yadati, N.; Nimishakavi, M.; Yadav, P.; Nitin, V.; Louis, A.; and Talukdar, P. 2019. HyperGCN: A new method for training graph convolutional networks on hypergraphs. In NeurIPS, 1511–1522. Yang, G.; Li, M.; Feng, H.; and Zhuang, X. 2025. Deeper insights into deep graph convolutional networks: Stability and generalization. IEEE Transactions on Pattern Analysis and Machine Intelligence. Zeng, H.; Zhang, P.; Li, F.; Ye, T.; Wang, J.; and Yang, X. 2025. Point-UMAE: Unet-like masked autoencoders for point cloud self-supervised learning. In ICASSP. Zhang, Q.; Xia, L.; Cai, X.; Yiu, S.-M.; Huang, C.; and Jensen, C. S. 2024. Graph augmentation for recommendation. In ICDE, 557–569. Zheng, X.; Zhou, B.; Gao, J.; Wang, Y. G.; Li´o, P.; Li, M.; and Mont´ufar, G. 2021. How framelets enhance graph neural networks. In ICML, 12761–12771. Zheng, X.; Zhou, B.; Wang, Y. G.; and Zhuang, X. 2022. Decimated framelet system on graphs and fast G-framelet transforms. Journal of Machine Learning Research, 23(18): 1–68.

23086
