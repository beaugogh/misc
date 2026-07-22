---
title: "Efficient Tensorized Multi-View Anchor Graph Clustering with Affinity Propagation for Remote Sensing Data"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40080
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40080/44041
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Efficient Tensorized Multi-View Anchor Graph Clustering with Affinity Propagation for Remote Sensing Data

<!-- Page 1 -->

Efficient Tensorized Multi-View Anchor Graph Clustering with Affinity

Propagation for Remote Sensing Data

Yongshan Zhang1, Kangyue Zheng1, Shuaikang Yan1, Xinxin Wang2*, Zhihua Cai1

1School of Computer Science, China University of Geosciences, Wuhan, China 2School of Artificial Intelligence, Shenzhen University, Shenzhen, China yszhang.cug@gmail.com, zhengkangyue@cug.edu.cn, 1202221621ysk@cug.edu.cn, xinxinwang1024@gmail.com, zhcai@cug.edu.cn

## Abstract

Multi-view clustering of remote sensing data presents significant challenges, as it integrates diverse data representations to improve Earth observation. Although existing anchor graphbased methods have yielded promising results, they generally exhibit two key limitations: (1) the time-consuming process of directly exploring pixel clustering structures, and (2) insufficient modeling of high-order correlations among different views. To address these issues, we propose an Efficient Tensorized multi-view anchor graph clustering method with Affinity Propagation (ETAP) for remote sensing data. Based on superpixel preprocessing, anchor graphs are learned from view-specific pixels and anchors, while compressed anchor graphs are simultaneously learned from the view-specific anchors. An adaptive weighting scheme is introduced to facilitate the learning of these anchor graphs. To capture high-order correlations, tensor Schatten p-norm regularization is applied to the compressed anchor graphs. A connectivity constraint is introduced to uncover the clustering structures of anchors. Finally, pixel clustering structures are then efficiently revealed from the pseudo-labeled anchors through affinity propagation without requiring additional clustering steps. To solve the proposed formulation, we develop an alternating optimization algorithm. Extensive experiments on three public datasets demonstrate the efficacy and efficiency of the proposed method over state-of-the-art methods.

Code — https://github.com/ZhangYongshan/ETAP

## Introduction

Remote sensing data can be collected from various perspectives, providing multiple representations to enhance Earth observation (Yang, Li, and Zhang 2023; Zhang and Zhang 2022; Yang et al. 2023). The emergence of multi-view remote sensing data requires multi-view learning techniques to effectively integrate complementary information for better scene understanding (Xue et al. 2022; Zhang et al. 2020, 2023). Due to the time-consuming and labor-intensive nature of large-scale pixel labeling, multi-view clustering for remote sensing data has gained significant attention by leveraging cross-view consistency and complementarity to partition pixels into distinct clusters without the need for ground-

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

truth labels (Wang et al. 2024). It has been successfully applied in various fields, including precision agriculture, environmental protection and military defense.

Recently, a large number of multi-view clustering methods have been specifically proposed for remote sensing data. Based on the features utilized in different views, these methods can be divided into multi-feature-based and multisource-based methods (Guan et al. 2025). Multi-featurebased methods address the clustering problem of singlesensor remote sensing data represented by multi-view features, such as texture and contour (Luo et al. 2024). However, they are inadequate for capturing the complementary information in multi-view data derived from multiple sensors (Cai et al. 2025; Zhang et al. 2024a). To solve this issue, multi-source-based methods tackle the clustering problem of multi-view remote sensing data collected by different sensors, such as hyperspectral (HS), multispectral (MS) and synthetic aperture radar (SAR) images (Zhang et al. 2024b; Guan et al. 2025). Compared to single-sensor data, the exploration of multi-sensor data is more challenging due to the complex spatial distribution and significant spectral variations across different views (Li et al. 2024b).

Anchor graph-based clustering has emerged as an effective and efficient technique that explores the relationships between pixels and representative anchors to analyze multiview remote sensing data captured by different sensors (Cai et al. 2025; Zhang et al. 2024a,b; Li et al. 2025). Based on the clustering process, anchor graph-based methods are primarily categorized into post-processing and one-pass methods. Post-processing methods require an additional k-means clustering step applied to the fused anchor graph for pixelwise partitioning (Sun et al. 2022), whereas one-pass methods directly uncover pixel clustering structures by imposing connectivity constraints or learning clustering indicators (Liu et al. 2024). Although existing methods demonstrate satisfactory results, they primarily suffer from two limitations: (1) most of them are limited by the time-consuming process of directly exploring the clustering structures of pixels; and (2) many of them exhibit insufficient modeling of high-order correlations across different views.

To overcome the above limitations, in this paper, we propose an Efficient Tensorized multi-view anchor graph clustering method with Affinity Propagation (ETAP) for remote sensing data, as shown in Figure 1. Specifically, nonlin-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

28501

<!-- Page 2 -->

**Figure 1.** Illustration of the proposed ETAP.

ear denoising and anchor initialization are first performed based on the spatial texture characteristics of each view. After spatial preprocessing, anchor graphs and compressed anchor graphs are simultaneously learned using an adaptive weighting scheme to capture the relationships between view-specific pixels and anchors, as well as among viewspecific anchors. To accelerate the learning process, tensor Schatten p-norm regularization and a connectivity constraint are applied to the compressed anchor graphs rather than the original anchor graphs, enabling the modeling of high-order correlations and the discovery of anchor clustering structures. Pixel clustering structures can be efficiently revealed from the pseudo-labeled anchors based on affinity propagation. An alternating optimization algorithm is developed to solve the proposed formulation. Extensive experiments demonstrate the efficacy and efficiency of the proposed method over state-of-the-art competitors.

In summary, the main contributions of this paper are highlighted as follows.

• We propose a novel multi-view anchor graph clustering framework that simultaneously learns view-specific anchor graphs and compressed anchor graphs to efficiently explore the clustering structures of multi-sensor remote sensing data.

• We explore high-order correlations among views using tensor Schatten p-norm regularization and uncover the clustering structures of anchors with a connectivity constraint, both applied to the compressed anchor graphs to accelerate the learning process.

• We design an efficient affinity propagation strategy to assign clustering labels to multi-view pixels from the pseudo-labeled anchors in the structured compressed anchor graphs.

• An alternating optimization algorithm is developed to solve the proposed formulation. Extensive experiments demonstrate the superior efficacy and efficiency of our proposed method.

## Related Work

Due to the diversity of data representations and the absence of ground-truth labels, various multi-view clustering methods have been proposed to achieve pixel partitioning for remote sensing data (Cai et al. 2022; Wan et al. 2022; Wang and Zhu 2020). They can group pixels into distinct clusters by leveraging multi-view information without label guidance. Based on the nature of multi-view information, these methods can be broadly separated into two categories: multifeature-based and multi-sensor-based methods. For multifeature-based methods, they perform multi-view clustering on multiple features derived from single-sensor remote sensing data. For instance, Luo et al. (Luo et al. 2024) utilize a Transformer with self-supervised learning to fuse spatial and spectral views for HS image clustering. Similarly, Chen et al. (Chen et al. 2022) perform polarimetric HS image clustering by organizing views into a tensor and imposing consistency constraints to strengthen inter-view correlations. For multi-sensor-based methods, they integrate multiview remote sensing data from different sensors for clustering. Specifically, Zhang et al. (Zhang et al. 2024b) learn a shared anchor graph and fuzzy membership matrix from multi-sensor data to facilitate clustering. Further, Guan et al. (Guan et al. 2025) adaptively refine graph and cluster structures through contrastive and consistent learning for multi-sensor data.

The aforementioned methods demonstrate promising performance in clustering multi-sensor remote sensing data. However, they often involve time-consuming processes to directly explore pixel clustering structures and fail to effectively model high-order correlations across different views.

Preliminary For clarity, notations and definitions are introduced here. Scalars, vectors, matrices and tensors are denoted by lowercase letters, boldface lowercase letters, boldface uppercase letters and boldface calligraphic letters, respectively. For a matrix S, we denote its trace, transpose and F-norm as tr(S), ST and ∥S∥F, respectively. For a third-order ten-

28502

![Figure extracted from page 2](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

sor S ∈Rn1×n2×n3, the i-th frontal slice is denoted as S(i). The discrete Fourier transform (DFT) of S along the third dimension is given by S = fft(S, [], 3), and its reverse operation is S = ifft(S, [], 3). Due to space limit, we provide only the definition of the tensor Schatten p-norm. More related definitions can be found in (Kilmer and Martin 2011).

Definition 1. (Gao et al. 2021) Given S ∈Rn1×n2×n3, h = min(n1, n2), the tensor Schatten p-norm of S is defined as

∥S∥p sp ⃝= n3 X i=1

S

(i) p sp ⃝

1 p

= n3 X i=1 h X j=1 σj

S

(i) p

1 p

, (1)

where σj(S

(i)) is the j-th singular value of matrix S

(i). It should be noted that when p is appropriately chosen, the Schatten p-norm effectively improves the approximation of the rank function than other norms (Li et al. 2024a).

## Method

Formulation Superpixel Denoising and Anchor Initialization To mitigate the noise incurred by challenging observation conditions, denoising can be guided by spatial information of remote sensing data (Lu et al. 2023; Shi, Huang, and Wang 2020). Given a set of remote sensing images { ˆ X v}V v=1 with V views, ˆ X v ∈RW ×H×Bv represents the v-th view image, containing W × H pixels and Bv spectral channels. To generate M view-specifc superpixels that reflect the spatial distribution and texture complexity, we apply the entropy rate superpixel (ERS) segmentation method (Liu et al. 2011) to the first principal component of each image, owing to its promising efficacy and efficiency. Based on this, a superpixel-based reconstruction method is introduced for denoising. It follows that all original pixels within the same superpixel are close to the recovered ones and are more likely to be distributed on nonlinear geometric manifolds (Wang, Zhang, and Zhou 2025). Assume that the manifold structure of all pixels within a superpixel is represented by M ∈RL×L, where L denotes the number of pixels in the superpixel. The original pixels are then reconstructed as follows:

min

Y ∥ˆY −Y∥2

F + ξTr

YLMYT

, (2)

where ˆY ∈RBv×L indicates the L observed pixels within a superpixe, and Y ∈RBv×L denotes the corresponding recovered pixels. The parameter ξ is used to balance the distance deviation and manifold constraint, and LM = DM −M is a Laplacian matrix, where DM is a degree matrix with diagonal elements (dM)ii = PL j=1 mij. After denosing, the reconstructed remote sensing images are organized in matrix form as {Xv}V v=1, with each image in the v-th view represented as Xv = {xv

1, · · ·, xv N} ∈RBv×N, where N = H × W denotes the pixel size.

High-quality anchors are crucial for effective anchor graph-based clustering. To this end, we also generate highquality anchors based on the generated superpixels, specifically tailored for remote sensing data. For instance, consider a superpixel with L pixels, the corresponding anchor a ∈RBv×1 is generated by averaging all reconstructed pixels within the superpixel. In this way, we can obtain multi-view spatial-aware anchors {Av}V v=1, where Av = {av

1, · · ·, av M} ∈RBv×M corresponds to M anchors in the v-th view. This anchor graph initialization method is able to uncover pixel distributions and preserve spatial-spectral discriminative information, enabling the generation of highquality anchors for effective subsequent learning.

Anchor Graph Learning Compared to traditional graphs that describe the relationships between pairwise samples, anchor graphs reduce their size by representing the relationships between samples and representative anchors (Wang et al. 2022). This results in higher efficiency, significantly reducing both computational complexity and memory consumption for large-scale problems. Given {Xv}V v=1 and {Av}V v=1, we adaptively learn the anchor graphs {Zv}V v=1 through projection learning for different views. Here, Zv ∈ RN×M represents the anchor graph for the v-th view, where zv ij ∈Zv encodes the relationships between the i-th pixel and j-th anchor. Since the information varies across different views, an auto-weighted scheme is introduced to adaptively quantify the contributions of each view. To learn Zv, pixel xv i should be connected to anchor av j with a probability zv ij to describe their neighboring relationship. The larger value of zv ij corresponds to a shorter distance between xv i and av i, and vice versa. Thus, anchor graph learning for multi-view remote sensing data can be formulated as follows:

min Wv,Zv,

Uv,αv

V X v=1

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij + δ

V X v=1

∥Zv∥2

F s.t. zvT i 1 = 1, zv ij ≥0, αT 1 = 1, αv > 0, (3)

WvT Sv t Wv = I.

where Wv ∈RBv×Rv is the projection matrix used to perform learning in a Rv-dimensional reduced subspace, Uv = WvT Av ∈RRv×M is the projected anchor matrix for easy representation, δ represents a regularization parameter, and 1 αv denotes the view weight. Note that superscript or subscript v refers to the v-th view. For effective learning, nonnegativity and normalization constraints are imposed on both Zv and αv (Wang et al. 2022, 2019), while the constraint WvT Sv t Wv = I ensures that the projected data are statistically uncorrelated, where Sv t = XvXvT represents the total scatter matrix.

Optimal Compressed Anchor Graph Learning When the sample size is large, anchor graph-based methods still require a time-consuming process to learn the exact connected components or necessitate post-processing clustering steps (Cai et al. 2025). To solve this problem, we learn the compressed anchor graphs {Sv}V v=1 with connectivity constraints from {Uv}V v=1 in the reduced subspace. Here, Sv ∈ RM×M represents the compressed anchor graph for the vth view, where sv ij ∈Sv encodes the relationships between pair-wise anchors. Besides, high-order correlations among multi-view data are often overlooked in remote sensing image analysis. To capture these multi-way dependencies, we construct a tensor by stacking the multi-view compressed anchor graphs and impose a tensor Schatten-p norm regularization. This regularizer promotes low-rank structures across

28503

<!-- Page 4 -->

different views, effectively preserving shared and complementary information among views (Gao et al. 2020). Similarly, we also introduce an adaptive weighting scheme to quantify the view contributions. Thus, compressed anchor graph learning for multi-view remote sensing data can be formulated as follows:

min Uv,Sv,βv

V X v=1

1 βv ∥Uv −UvSv∥2

F + λ∥S∥p sp ⃝ (4)

s.t. sv i

T 1 = 1, sv ij ≥0, βT 1 = 1, βv > 0, rank(LSv) = M −C, where LSv = DSv −(SvT +Sv)/2 is the normalized Laplacian matrix related to Sv, DSv is the degree matrix with diagonal elements (dSv)ii = P j(sv ij+sv ji)/2, and 1 αv denotes the view weight. The first four constraints are nonnegativity and normalization constraints for S and β, while the final constraint is the connectivity constraint for Sv. Theorem 1 The multiplicity C of the eigenvalue 0 of the normalized Laplacian matrix LSv equals the number of connected components in the graph associated with Sv.

According to Theorem 1, if rank(LSv) = M −C, Sv has exactly C connected components, each corresponding to a distinct cluster. Consequently, the weighted Laplacian matrix also satisfies rank(LS) = M −C, where LS = PV v=1

1 βv LSv. Under this condition, the implicitly weighted consensus graph S = PV v=1

1 βv Sv preserves the same property, i.e., it has exactly C connected components (Chen et al. 2022). Therefore, the C-cluster structure among anchors can be directly uncovered. The constraint rank(LSv) = M −C is non-convex and thus difficult for direct optimization. Given that LSv is positive semi-definite, all its eigenvalues satisfy σi(LSv) ≥0. Therefore, the rank constraint can be relaxed by minimizing the sum of its smallest C eigenvalues, i.e., enforcing PC i=1 σi(LSv) = 0. Based on Ky Fan’s theorem (Fan 1949), we have PC i=1 σi(LSv) = minFT F=I Tr(FTLSvF), where F ∈RM×C denotes the embedding matrix subject to an orthogonality constraint. Based on these observations, Eq. (4) can be reformulated as follows:

min Uv,Sv, βv

V X v=1

1 βv ∥Uv −UvSv∥2

F + λ∥S∥p sp ⃝+ 2γ tr(FT LSF), s.t. sv i

T 1 = 1, sv ij ≥0, βT 1 = 1, βv > 0, FT F = I. (5) where γ denotes a regularization parameter.

Overall Objective Function The separation between anchor graph learning and compressed anchor graph learning may result in suboptimal performance. Thus, we combine Eqs. (3) and (5) into a unified framework to formulate the overall objective function of ETAP as follows:

min Wv,Zv,Sv,

Uv,βv,αv

V X v=1

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij + δ

V X v=1

∥Zv∥2

F

+

V X v=1

1 βv ∥Uv −UvSv∥2

F + λ∥S∥p sp ⃝+ 2γ tr

FT LSF s.t. zv i

T 1 = 1, zv ij ≥0, sv i

T 1 = 1, sv ij ≥0, αvT 1 = 1, (6)

αv > 0, βT 1 = 1, βv > 0, FT F = I, WvT Sv t Wv = I.

**Figure 2.** Illustration of the designed affinity propagation.

The joint learning of {Zv}V v=1 and {Sv}V v=1 facilitates the discovery of their optimal structures. Through iterative optimization, the clustering structures of anchors gradually emerges as in the exactly C connected components in the consensus graph S = PV v=1

1 βv Sv.

Affinity Propagation for Pixel Partitioning Finally, the clustering labels of pixels can be revealed through affinity propagation based on the structured anchors in S and the weighted anchor graph Z = PV v=1

1 αv Zv. Specifically, a multi-view pixel is assigned the same label as the anchor that exhibits the maximum affinity with the pixel in Z. Thus, the clustering structures of pixels are efficiently obtained. Figure 2 illustrates the affinity propagation strategy used for pixel label inference.

Optimization Motivated by augmented Lagrange multiplier (ALM) (Lin, Liu, and Su 2011), we introduce an auxiliary variable J and set J = S. Then, Eq. (6) can be rewritten as min

Ω

V X v=1

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij + δ

V X v=1

∥Zv∥2

F

+

V X v=1

1 βv ∥Uv −UvSv∥2

F + λ∥J ∥p sp ⃝+ 2γ tr

FT LSF

+ ⟨Y, S −J ⟩+ µ

2 ∥S −J ∥2 F (7)

s.t. zv i

T 1 = 1, zv ij ≥0, sv i

T 1 = 1, sv ij ≥0, αvT 1 = 1, αv > 0, βT 1 = 1, βv > 0, FT F = I, WvT Sv t Wv = I.

where Ω= {Wv, Zv, Sv, Uv, βv, αv, J } are variables to be optimized, Y(:, v,:) = Y(v) is the Lagrange multiplier, and µ > 0 is the penalty factor. Our model reliably converges by iteratively updating each variable individually while fixing the others during optimization.

1) Updating Zv: When Wv, Uv, Sv, F, αv, βv and J are fixed, the optimization for Zv becomes min

Zv

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij + δ

N X i=1

M X j=1 zv ij

2 s.t. zv i

T 1 = 1, zv ij ≥0. (8)

28504

![Figure extracted from page 4](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

## Algorithm

1: ETAP Input: Multi-view data {Xv}V v=1, number of anchors M, cluster number C, projected dimension {Rv}V v=1 Output: Clustering results.

1: Obtain {Xv}V v=1 by performing spatial denoising; 2: Initialize {Av}V v=1 from spatial anchor generation; 3: Initialize {Zv}V v=1; Initialize αv and βv with 1

V; 4: repeat 5: Update {Wv}V v=1 by solving Eq. (11); 6: Update {αv}V v=1 using Eq.(13); 7: Update {Zv}V v=1 by solving Eq. (9); 8: Update {Sv}V v=1 by solving Eq. (19); 9: Update F by solving Eq. (16); 10: Update J using Eq. (17); 11: Y = Y + µ(S −J); 12: µ = min(ηµ, µmax); 13: Update {βv}V v=1 using Eq. (15); 14: Update {Uv}V v=1 using Eq. (22); 15: until Convergence 16: return {Zv}V v=1 and {Sv}V v=1.

Denoting bv ij = 1 αv

WvT xv i −uv j

2

2, Eq. (8) can be solved by independently updating zv i as follows:

min zv i

1 2 zv i + bv i 2δ

2

2, s.t. zv i

T 1 = 1, zv ij ≥0. (9)

There is a closed-form solution to problem (9) as proved in (Nie et al. 2016).

2) Updating Wv: When Zv, Uv, Sv, F, αv, βv and J are fixed, the optimization for Wv becomes:

min WvT Sv t Wv=I

1 αv

N X i=1

M X j=1

WvT xv i −WvT av j

2

2 zv ij

+ 1 βv

WvT Av −WvT AvSv

2

F. (10)

According to (Wang et al. 2022) and Uv = WvT Av, problem (10) can be rewritten as:

min WvT Sv t Wv=I tr

WvT (Pv + Qv) Wv

. (11)

Pv = 1 αv

XvDrow z XvT −2XvZAvT + AvDcol z AvT with Drow z = diag(PM j=1 zv ij) and Dcol z = diag(PN i=1 zv ij), and Qv = 1 βv

AvAvT −2AvSvAvT + AvSvSvT AvT

. The optimal Wv is formed by the eigenvectors of Sv t

−1(Pv + Qv) corresponding to Rv smallest eigenvalues. 3) Updating αv: When Wv, Uv, Sv, F, Zv, βv and J are fixed, the optimization for αv becomes:

min αvT 1=1, αv>0

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij. (12)

Letting hv = qPN i=1

PM j=1

WvT xv i −uv j

2

2 zv ij, Eq. (12) can be solved according to Cauchy–Schwartz’s inequality (Nie, Wang, and Huang 2014) as follows:

αv = hv PV v=1 hv

. (13)

4) Updating βv: WhenWv, Uv, Sv, F, J, αv and Zv are fixed, the optimization for βv becomes min βv

1 βv ∥Uv −UvSv∥2

F, s.t. βT 1 = 1, βv > 0. (14)

Similar to the solution for αv, we denote ev = ∥Uv −UvSv∥F, and update βv as follows:

βv = ev PV v=1 ev. (15)

5) Updating F: When Wv, Uv, Sv, Zv, αv, βv and J are fixed, the optimization for F becomes min tr

FT LSF

, s.t. FT F = I. (16) The optimal solution of F is composed of the eigenvectors of LS corresponding to C smallest eigenvalues.

6) Updating J: When Wv, Uv, Sv, Zv, αv, βv and F are fixed, the optimization for J becomes

J ∗= min

J λ∥J ∥p sp ⃝+ ⟨Y, S −J ⟩+ µ

2 ∥S −J ∥2 F

= min

J λ µ∥J ∥p sp ⃝+ 1

2

J −(S + Y µ)

2

F

.

(17)

Problem (17) has a closed-form solution based on Theorem 3 from (Gao et al. 2021). 7) Updating Sv: When Wv, Uv, Zv, F, αv, βv and J are fixed, let Qv = Jv −Yv µ. The optimization for Sv becomes min

Sv

1 βv ∥Uv −UvSv∥2

F + γ βv

M X i,j=1

∥fi −fj∥2

2sv ij

+ µ

2 ∥Sv −Qv∥2 F s.t. svT i 1 = 1, sv ij ≥0. (18) Expanding Eq. (18) into trace form, we have:

min

Sv

M X i=1 sv i

T

Kv βv + µ

2 I sv i +

−2 βv kv i + γ βv tT i −µqv i

T sv i s.t. svT i 1 = 1, sv ij ≥0. (19)

where tij = ∥fi −fj∥2

2, and Kv = UvT Uv. Many existing quadratic programming packages (Kang, Peng, and Cheng 2017) can be utilized to solve each sv i of Sv in problem (19). 8) Updating Uv: When Wv, Sv, Zv, F, αv, βv and J are fixed, the optimization for Uv becomes min

Uv

1 αv

N X i=1

M X j=1

WvT xv i −uv j

2

2 zv ij + 1 βv ∥Uv −UvSv∥2

F.

(20) Using the previously derived equations and removing irrelevant terms, we can derive the following equation:

min

Uv Tr

1 αv

−2WvT XvZvUvT + KvDcol z

+

1 βv

Kv −KvSv −KvSvT −SvT KvSv

.

(21)

The optimal solution of Uv can be obtained by taking the derivative and setting it to zero. Thus, we have

Uv = βvWvT XvZv βvDcol z +αv(I−Sv −SvT +SvSvT)

−1.

(22) Finally, the entire optimization procedure for Eq. (6) is outlined in Algorithm 1.

28505

<!-- Page 6 -->

Datasets Metrics MFLVC DIVIDE SCMVC TMPCC DFCPC AMKSC CDD MSSAGF SAMVGC Ours

Berlin

ACC 0.4174 0.4315 0.4459 0.4214 0.5327 0.5298 0.6447 0.5988 0.4890 0.7151 Kappa 0.2578 0.2806 0.2932 0.2342 0.3640 0.3798 0.4286 0.3587 0.3116 0.5120 NMI 0.2629 0.3076 0.3068 0.3245 0.3988 0.3039 0.2841 0.2716 0.2888 0.4404 Purity 0.6709 0.6969 0.6854 0.6843 0.7087 0.6645 0.6645 0.6008 0.7002 0.7621 ARI 0.1525 0.2256 0.2192 0.2016 0.3298 0.2091 0.3500 0.3376 0.2501 0.4994

MUUFL

ACC 0.5118 0.5132 0.3796 0.5353 0.5610 0.4364 0.5816 0.4335 0.4897 0.6659 Kappa 0.4215 0.4080 0.2911 0.4211 0.4357 0.3630 0.4885 0.1904 0.4115 0.5531 NMI 0.3928 0.3480 0.3010 0.5257 0.4624 0.4236 0.4689 0.1944 0.3978 0.5056 Purity 0.6361 0.5917 0.5660 0.6527 0.6285 0.6806 0.7011 0.4357 0.6769 0.7295 ARI 0.2956 0.3573 0.1765 0.4158 0.4368 0.2694 0.4098 0.1368 0.2556 0.6126

MDAS

ACC 0.2997 0.2450 0.2565 0.2841 0.3248 0.2832 N/A 0.3181 0.4215 0.5634 Kappa 0.2298 0.1874 0.1839 0.2100 0.1780 0.1871 N/A 0.0995 0.2851 0.3039 NMI 0.2666 0.2332 0.2387 0.2938 0.2073 0.2359 N/A 0.1493 0.2832 0.3092 Purity 0.6066 0.6059 0.6046 0.6022 0.5738 0.5960 N/A 0.4944 0.6394 0.6239 ARI 0.1134 0.0773 0.0884 0.1077 0.1195 0.1192 N/A 0.0678 0.1821 0.3008

**Table 1.** Clustering performance on multi-view remote sensing datasets. Best results are in bold, second-best are underlined.

Complexity Analysis The optimization algorithm of our ETAP involves updating eight variables. To solve {Wv}V v=1, it takes O

PV v=1 BvR2 v to achieve eigenvalue decomposition and matrix inversion. To learn Zv, it needs O(V NM) for calculation. The update of Sv requires O(V M 3) to get the closedform solution. To update {Uv}V v=1, it costs O(RBNM 2), where B = PV v=1 Bv and R = PV v=1 Rv. To solve F, it requires O(M 2C) to calculate the eigenvectors of LS.To update J, it takes O(2V M 2log(V M) + V 2M 2). As for αv and βv, their update trivially requires O(1). For clustering inference strategy, it takes O(NMR) to get clustering results. Due to M ≪N, and V,C are small constants, the main computational complexity is O

RBNM 2

. when R ≪N and B ≪N the proposed method shows a nearly linear time complexity of O(N).

## Experiments

## Experiment

Setup Datasets. Three datasets are utilized for experiments, including Berlin, MUUFL and MDAS. The Berlin dataset contains two views: an HS image with 244 spectral bands and a SAR image with 4 channels. It covers an area of 1723 × 476 pixels and includes 8 land-cover categories. The MUUFL dataset comprises three views: an HS image with 180 spectral bands, a SAR image with 4 features, and a DSM image with 1 channel. The dataset size is 332 × 485 pixels with 7 land-cover categories. The MDAS dataset is composed of four views: an HS image with 242 spectral bands, an MS image with 12 bands, a SAR image with 2 features, and an DSM image with 1 channel. The dataset spans 300 × 360 pixels and includes 14 land-cover categories. These datasets span diverse resolutions, modalities and scenarios, offering a comprehensive testbed.

Compared Methods. To evaluate our ETAP, nine stateof-the-art methods are adopted for comparison, including MFLVC (Xu et al. 2022), DIVIDE (Lu et al. 2024), SCMVC (Yu et al. 2024), TMPCC (Cai et al. 2023), DFCPC (Xu et al. 2024), AMKSC (Cai et al. 2025), CDD (Liu and

Chang 2025), MSSAGF (Wang, Zhang, and Zhou 2025) and SAMVGC (Guan et al. 2025).

Implementation Details. The optimal parameters for ETAP is set by a grid-search strategy. Specifically, M is tuned within [150: 25: 300], and p is varied from [0.1: 0.1: 1]. Rv is selected from [Bv/4: 5: Bv/2] for high-dimensional views and from [1: 2: Bv] for lowdimensional views. For ξ, γ and λ, they are selected from [10−3, 10−2,..., 103]. For other baselines, we adopt their released code and recommended parameter settings. Clustering performance is evaluated using five common metrics, including accuracy (ACC), Kappa coefficient, normalized mutual information (NMI), purity and adjusted rand index (ARI). All experiments are carried out on a server configured with two NVIDIA RTX 4090 GPUs, each with 24GB of memory. Under optimal parameter settings, all reported results are averaged over ten independent runs to reduce randomness and ensure reliability.

Comparison Results

Clustering Performance. As shown in Table 1, our ETAP achieves the optimal performance across all datasets in most cases. On the MUUFL dataset, it exceeds the second-best baseline CCD by 8.43%, 6.46%, 3.67%, 2.84% and 20.28% in terms of the five metrics. On the Berlin dataset, it surpasses CDD by 7.04%, 8.34%, 15.63%, 9.76% and 14.94%, demonstrating notable improvements over SAMVGC and DFCPC as well. On the MDAS dataset, CDD fails to handle more than two views, resulting in no derived results. Our ETAP outperforms the second-best method SAMVGC by 14.19%, 1.88%, 2.6% and 11.87% in terms of the four metrics, with the exception of Purity. These substantial and consistent gains demonstrate the superiority of our ETAP in leveraging multi-view information for improved clustering accuracy across diverse remote sensing scenarios.

To visualize the clustering effect, we display the clustering maps of different methods on the MUUFL datasets in Figure 3. Our ETAP aligns best with the ground truth. This is because the spatial structure alignment of anchors across views, enhancing the quality of anchor graph fusion.

28506

<!-- Page 7 -->

GT MFLVC DIVIDE SCMVC TMPCC DFCPC AMKSC CDD MSSAGF SAMVGC Ours

**Figure 3.** Clustering maps of the MUUFL dataset obtained by different methods. GT: Ground truth.

## Methods

Berlin MUUFL MDAS

MFLVC 312.07 140.96 378.07 DIVIDE 188111.80 18696.60 3483.00 SCMVC 3081.72 1999.63 993.69 TMPCC 2238.89 891.45 477.50 DFCPC 8697.48 682.90 218.24 AMKSC 149.59 137.68 29.57 CDD 308.68 39.56 N/A MSSAGF 1495.70 59.98 130.12 SAMVGC 239.82 179.01 1080.73 ETAP 214.96 9.03 8.59

**Table 2.** Runtime record on multiple datasets (in seconds).

(a) Effect of M (b) Effect of p

(c) Effect of λ (d) Effect of γ

**Figure 4.** Performance variance of our ETAP.

Running Time. Table 2 reports the runtime comparison of different methods across three datasets. Our ETAP achieves the highest efficiency on the MUUFL and MDAS datasets, reducing execution time by 30.53 and 20.98 seconds compared to the second fastest methods. In addition, it obtains the second-best efficiency on the Berlin dataset. These results demonstrate the practical potential of our method for real-world applications.

## Model

Analyses

Parameter Sensitivity Study. To investigate the parameter sensitivity of ETAP, we conduct experiments with different parameter settings and display the results in Figure 4. The results show that the superpixel size (i.e., M) should align

Settings S1 S2 S3 S4 Ours

Factors

SG ✓ ✓ ✓ ✓ ✓ SD ✗ ✓ ✓ ✓ ✓ SP ✗ ✗ ✓ ✓ ✓ PL ✗ ✗ ✗ ✓ ✓ AMW ✗ ✗ ✗ ✗ ✓

Datasets

Berlin 0.5051 0.5317 0.5588 0.6241 0.7151 MUUFL 0.3583 0.3786 0.4367 0.4527 0.6659 MDAS 0.2721 0.3494 0.4565 0.4662 0.5634

**Table 3.** Ablation study of our ETAP (in ACC).

with dataset size, with values between 175 and 250 generally yielding good performance. The tensor Schatten p-norm offers stable results across a wide range of p. While λ has minimal impact, γ significantly affects performance and should be tuned for each dataset. Overall, proper parameter selection enhances the accuracy of ETAP.

Ablation Study. Table 3 presents the ablation study results. We use “✓” and “✗” to indicate whether the model includes or excludes each component. For clarity, SG denotes superpixel generation, SD represents spatial denoising, SP refers to the tensor Schatten p-norm constraint, PL stands for projection learning, and AMW indicates adaptive modality weighting. From Table 3, the model performance on all three datasets shows a consistent improvement as each component is gradually added. For example, on the Berlin dataset, “S2” surpasses “S1” by 2.66%, “S3” outperforms “S2” by 2.71%, “S4” improve upon S3 by over 6.53%, and our ETAP exceeds “S4” by 9.10%. Compared to the degraded settings, our ETAP with all components achieves the best performance across all three datasets, demonstrating the synergistic effect of each component in enhancing the model.

## Conclusion

In this paper, we proposed an efficient tensorized multi-view anchor graph clustering method with affinity propagation for remote sensing data. Based on superpixel-based denoising and anchor selection, anchor graph learning and compressed anchor graph learning with tensor regularization are jointly performed in a unified framework to uncover the clustering structures of anchors through a connectivity constraint. The designed affinity propagation strategy enables accurate and efficient partitioning for multi-view pixels. An alternating optimization algorithm is developed for the proposed formulation. Extensive experiments demonstrate the superiority of the proposed method.

28507

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-efficient-tensorized-multi-view-anchor-graph-clustering-with-affinity-propagatio/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work was funded by the China National Key R&D Program (Grant 2023YFF0807000).

## References

Cai, Y.; Zhang, Z.; Ghamisi, P.; Ding, Y.; Liu, X.; Cai, Z.; and Gloaguen, R. 2022. Superpixel Contracted Neighborhood Contrastive Subspace Clustering Network for Hyperspectral Images. IEEE Transactions on Geoscience and Remote Sensing, 60: 1–13. Cai, Y.; Zhang, Z.; Ghamisi, P.; Rasti, B.; Liu, X.; and Cai, Z. 2023. Transformer-Based Contrastive Prototypical Clustering for Multimodal Remote Sensing Data. Information Sciences, 649: 119655. Cai, Y.; Zhang, Z.; Liu, X.; Ding, Y.; Li, F.; and Tan, J. 2025. Learning Unified Anchor Graph for Joint Clustering of Hyperspectral and LiDAR Data. IEEE Transactions on Neural Networks and Learning Systems, 36(4): 6341–6354. Chen, Z.; Zhang, C.; Mu, T.; and He, Y. 2022. Tensorial Multiview Subspace Clustering for Polarimetric Hyperspectral Images. IEEE Transactions on Geoscience and Remote Sensing, 60: 1–13. Fan, K. 1949. On a Theorem of Weyl Concerning Eigenvalues of Linear Transformations I. Proceedings of the National Academy of Sciences, 35(11): 652–655. Gao, Q.; Wan, Z.; Liang, Y.; Wang, Q.; Liu, Y.; and Shao, L. 2020. Multi-View Projected Clustering with Graph Learning. Neural Networks, 126: 335–346. Gao, Q.; Zhang, P.; Xia, W.; Xie, D.; Gao, X.; and Tao, D. 2021. Enhanced Tensor RPCA and its Application. IEEE Transactions on Pattern Analysis and Machine Intelligence, 43(6): 2133–2140. Guan, R.; Tu, W.; Wang, S.; Liu, J.; Hu, D.; Tang, C.; Feng, Y.; Li, J.; Xiao, B.; and Liu, X. 2025. Structure-Adaptive Multi-View Graph Clustering for Remote Sensing Data. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 16933–16941. Kang, Z.; Peng, C.; and Cheng, Q. 2017. Twin Learning for Similarity and Clustering: A Unified Kernel Approach. Proceedings of the AAAI Conference on Artificial Intelligence, 31(1). Kilmer, M. E.; and Martin, C. D. 2011. Factorization strategies for third-order tensors. Linear Algebra and its Applications, 435(3): 641–658. Li, J.; Gao, Q.; Wang, Q.; and Xia, W. 2024a. Tensorized label learning on anchor graph. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 13537– 13544. Li, X.; Pan, Y. P.; Sun, Y.; Sun, Q.; Sun, Y.; W. Tsang, I.; and Ren, Z. 2025. Incomplete Multi-view Clustering with Paired and Balanced Dynamic Anchor Learning. IEEE Transactions on Multimedia, 7087–7098. Li, X.; Pan, Y. P.; Sun, Y.; Sun, Q. S.; Tsang, I. W.; and Ren, Z. 2024b. Fast Unpaired Multi-view Clustering. Proceedings of the 33rd International Joint Conference on Artificial Intelligence, 4488–4496.

Lin, Z.; Liu, R.; and Su, Z. 2011. Linearized Alternating Direction Method with Adaptive Penalty for Low-Rank Representation. In Advances in Neural Information Processing Systems 24, 612–620. Liu, M.-Y.; Tuzel, O.; Ramalingam, S.; and Chellappa, R. 2011. Entropy Rate Superpixel Segmentation. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2097–2104. Liu, S.; and Chang, L. 2025. Conditional Dual Diffusion for Multimodal Clustering of Optical and SAR Images. IEEE Transactions on Circuits and Systems for Video Technology, 35(6): 5318–5330. Liu, S.; Liao, Q.; Wang, S.; Liu, X.; and Zhu, E. 2024. Robust and Consistent Anchor Graph Learning for Multi-View Clustering. IEEE Transactions on Knowledge and Data Engineering, 36(8): 4207–4219. Lu, P.; Jiang, X.; Zhang, Y.; Liu, X.; Cai, Z.; Jiang, J.; and Plaza, A. 2023. Spectral–Spatial and Superpixelwise Unsupervised Linear Discriminant Analysis for Feature Extraction and Classification of Hyperspectral Images. IEEE Transactions on Geoscience and Remote Sensing, 61: 1–15. Lu, Y.; Lin, Y.; Yang, M.; Peng, D.; Hu, P.; and Peng, X. 2024. Decoupled Contrastive Multi-View Clustering with High-Order Random Walks. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 14193– 14201. Luo, F.; Liu, Y.; Gong, X.; Nan, Z.; and Guo, T. 2024. EMVCC: Enhanced Multi-View Contrastive Clustering for Hyperspectral Images. In Proceedings of the 32nd ACM International Conference on Multimedia, 6288–6296. Nie, F.; Wang, X.; and Huang, H. 2014. Clustering and projected clustering with adaptive neighbors. In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 977–986. ACM. Nie, F.; Wang, X.; Jordan, M. I.; and Huang, H. 2016. The Constrained Laplacian Rank Algorithm for Graph-Based Clustering. In Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence (AAAI), 1969–1976. Shi, G.; Huang, H.; and Wang, L. 2020. Unsupervised Dimensionality Reduction for Hyperspectral Imagery via Local Geometric Structure Feature Learning. IEEE Geoscience and Remote Sensing Letters, 17(8): 1425–1429. Sun, Y.; Li, X.; Sun, Q.; Zhang, M.; Ren, Z.; Cai, J.; Kankanhalli, M.; Prabhakaran, B.; Boll, S.; Subramanian, R.; Zheng, L.; Singh, V.; Cesar, P.; Xie, L.; and Xu, D. 2022. Structure Diversity-Induced Anchor Graph Fusion for Multi-View Clustering. IEEE Transactions on Knowledge and Data Engineering, 34(12): 5682–5695. Wan, Y.; Ma, A.; Zhang, L.; and Zhong, Y. 2022. Multiobjective Sine Cosine Algorithm for Remote Sensing Image Spatial-Spectral Clustering. IEEE Transactions on Cybernetics, 52(10): 11172–11186. Wang, H.; and Zhu, S. 2020. Multisource Aggregation Search and Scheduling for Remote Sensing Data Cluster. IEEE Geoscience and Remote Sensing Letters, 17(2): 352– 356.

28508

<!-- Page 9 -->

Wang, L.; Zhang, Y.; Li, H.; Liu, X.; and Chen, J. 2024. Adaptive Fusion of Multi-view Remote Sensing Data for Optimal Sub-field Crop Yield Prediction. arXiv preprint arXiv:2401.11844. Wang, R.; Nie, F.; Wang, Z.; He, F.; and Li, X. 2019. Scalable Graph-Based Clustering With Nonnegative Relaxation for Large Hyperspectral Image. IEEE Transactions on Geoscience and Remote Sensing, 57(10): 7352–7364. Wang, S.; Liu, X.; Zhu, X.; Zhang, P.; Zhang, Y.; Gao, F.; and Zhu, E. 2022. Fast Parameter-Free Multi-View Subspace Clustering With Consensus Anchor Guidance. IEEE Transactions on Image Processing, 31: 556–568. Wang, X.; Zhang, Y.; and Zhou, Y. 2025. Multimodal Remote Sensing Image Clustering with Multi-scale Spectral-Spatial Anchor Graphs. IEEE Transactions on Geoscience and Remote Sensing, 63(4405612): 1–12. Xu, J.; Tang, H.; Ren, Y.; Peng, L.; Zhu, X.; and He, L. 2022. Multi-Level Feature Learning for Contrastive Multi- View Clustering. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 16051–16060. Xu, S.; Ding, X.; Zhang, Y.; Zhang, Z.; Gao, H.; and Zhang, B. 2024. Dual-Feature Attention-Based Contrastive Prototypical Clustering for Multimodal Remote Sensing Data. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–13. Xue, Z.; Tan, X.; Yu, X.; Liu, B.; Yu, A.; and Zhang, P. 2022. Deep Hierarchical Vision Transformer for Hyperspectral and LiDAR Data Classification. IEEE Transactions on Image Processing, 31: 3095–3110. Yang, C.; Li, Z.; and Zhang, L. 2023. Bootstrapping Interactive Image-Text Alignment for Remote Sensing Image Captioning. arXiv:2312.01191. Yang, X.; Cao, W.; Lu, Y.; and Zhou, Y. 2023. QTN: Quaternion Transformer Network for Hyperspectral Image Classification. IEEE Transactions on Circuits and Systems for Video Technology, 33(12): 7370–7384. Yu, H.; Bian, H.-X.; Chong, Z.-L.; Liu, Z.; and Shi, J.-Y. 2024. Multi-View Clustering with Semantic Fusion and Contrastive Learning. Neurocomputing, 603: 128264. Zhang, L.; and Zhang, L. 2022. Artificial Intelligence for Remote Sensing Data Analysis: A Review of Challenges and Opportunities. IEEE Geoscience and Remote Sensing Magazine, 10(2): 270–294. Zhang, M.; Li, W.; Du, Q.; Gao, L.; and Zhang, B. 2020. Feature Extraction for Classification of Hyperspectral and LiDAR Data Using Patch-to-Patch CNN. IEEE Transactions on Cybernetics, 50(1): 100–111. Zhang, M.; Li, W.; Zhang, Y.; Tao, R.; and Du, Q. 2023. Hyperspectral and LiDAR Data Classification Based on Structural Optimization Transmission. IEEE Transactions on Cybernetics, 53(5): 3153–3164. Zhang, Y.; Yan, S.; Jiang, X.; Zhang, L.; Cai, Z.; and Li, J. 2024a. Dual Graph Learning Affinity Propagation for Multimodal Remote Sensing Image Clustering. IEEE Transactions on Geoscience and Remote Sensing, 62: 1–13.

Zhang, Y.; Yan, S.; Zhang, L.; and Du, B. 2024b. Fast Projected Fuzzy Clustering With Anchor Guidance for Multimodal Remote Sensing Imagery. IEEE Transactions on Image Processing, 33: 4640–4653.

28509
