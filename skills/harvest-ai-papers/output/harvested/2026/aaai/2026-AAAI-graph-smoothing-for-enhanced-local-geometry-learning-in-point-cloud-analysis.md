---
title: "Graph Smoothing for Enhanced Local Geometry Learning in Point Cloud Analysis"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38216
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38216/42178
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Graph Smoothing for Enhanced Local Geometry Learning in Point Cloud Analysis

<!-- Page 1 -->

Graph Smoothing for Enhanced Local Geometry Learning in Point Cloud Analysis

Shangbo Yuan1, Jie Xu2,*, Ping Hu1, Xiaofeng Zhu3, Na Zhao2

1School of Computer Science and Engineering, University of Electronic Science and Technology of China, Chengdu, China 2Information Systems Technology and Design Pillar, Singapore University of Technology and Design, Singapore 3School of Computer Science and Technology, Hainan University, Haikou, China

## Abstract

Graph-based methods have proven to be effective in capturing relationships among points for 3D point cloud analysis. However, these methods often suffer from suboptimal graph structures, particularly due to sparse connections at boundary points and noisy connections in junction areas. To address these challenges, we propose a novel method that integrates a graph smoothing module with an enhanced local geometry learning module. Specifically, we identify the limitations of conventional graph structures, particularly in handling boundary points and junction areas. In response, we introduce a graph smoothing module designed to optimize the graph structure and minimize the negative impact of unreliable sparse and noisy connections. Based on the optimized graph structure, we improve the feature extract function with local geometry information. These include shape features derived from adaptive geometric descriptors based on eigenvectors and distribution features obtained through cylindrical coordinate transformation. Experimental results on real-world datasets validate the effectiveness of our method in various point cloud learning tasks, i.e., classification, part segmentation, and semantic segmentation.

Code — https://github.com/shangboyuan/GSPoint

## Introduction

Point clouds have become foundational to advanced 3D technologies, enabling critical applications in autonomous driving (Sheng et al. 2022, 2025; Pan et al. 2025), robotic perception (Wang and Zhao 2025; Zhao et al. 2025; Xiu et al. 2025; Jiang et al. 2025; Li and Zhao 2024; Han et al. 2024), and 3D spatial reasoning (Li et al. 2024; Wang et al. 2025a,b; Yuan et al. 2025). A central challenge in representing point clouds for these applications is the effective organization of inherently unstructured points into structured data formats. This challenge stems from the absence of topological structure and irregular spatial distribution, which fundamentally preclude the direct application of conventional grid-based convolutional methods. As a result, this structural incompatibility necessitates specialized approaches to extract meaningful hierarchical features while preserving geo-

*Corresponding Author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

metric fidelity (Sohail et al. 2024; Wu et al. 2024), motivating researchers to develop many specialized deep methods of point cloud analysis (Wu et al. 2023; Wang et al. 2024).

Previous deep methods of point cloud analysis can be partitioned into four subgroups, i.e., voxel-based methods, MLP-based methods, transformer-based methods, and graph-based methods. Voxel-based methods (Wu et al. 2015; Maturana and Scherer 2015; Zhou and Tuzel 2018) convert point clouds into structured voxel grids and apply mature 3D convolutional models for effective feature extraction, but they ignore geometric precision to particularly affect the preservation of fine-grained details. Instead of taking voxel as input, other methods use individual points as input. Specifically, MLP-based methods (Qi et al. 2017b,a; Thomas et al. 2019) avoid the information loss associated with grid conversion by directly operating on raw point clouds. However, raw point data often include noise to affect the effectiveness of feature extraction. Transformer-based methods (Guo et al. 2021; Zhao et al. 2021; Yu et al. 2022) employ self-attention mechanisms to simultaneously focus on local details and global context, thereby enhancing the understanding of complex samples. However, they typically require a large number of data in the train process, placing high demands on computational resources. Graph-based methods (Wang et al. 2019a,b; Du, Ye, and Cao 2022) explicitly model the relationships between points with graphs, where nodes represent individual points and edges encode spatial adjacency or feature affinities. Graph can effectively organize the inherently unstructured points (Mo et al. 2022; He et al. 2025), and thus attracting much research interest.

Recent advances in graph-based methods have focused on two strategies, i.e., fixed graph methods and graph learning methods. Fixed graph methods capture the relationship between two points by the fixed graph structures with adaptive edge-weighting mechanisms to adjust convolution weights for neighboring points. For instance, Wang et al. (2019a) compute similarity weights based on position and feature disparities, while Xu et al. (2021) employ a weight bank combined with relative position to generate adaptive weights. Graph learning methods use dynamic graph structures to capture multi-scale relationships. For instance, Yan et al. (2020) propose to integrate attention-based global graph with a local graph constructed by the k-NN method, enabling the combined graph to capture global semantic

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

12250

<!-- Page 2 -->

(a) With normal ball query (b) With our method

**Figure 1.** Illustration of sparse connection. The heatmaps of degree distribution indicates that (a) When the graph is constructed using the normal ball query, some boundary points exhibit sparse connection and out-degree values below 20, whereas some points have out-degree values exceeding 35. (b) Through our method, the number of points with extreme out-degree values is reduced.

relationships and local geometric structures. Zhang et al. (2023) propose involving a correlation filter into a weighted local graph to suppress irrelevant connections from distant neighbors. Dynamic graph structures have attracted growing attention in recent research, due to their flexibility in adjusting graph connections which can establish multiscale relationships and mitigate noise interference (Peng et al. 2023; Du et al. 2024; Xu et al. 2024; Chen et al. 2025).

However, previous graph-based methods for 3D point cloud analysis still have limitations to be addressed. First, sparse connections among boundary points hinder the effective usage of point cloud contour information. As shown in Figure 1(a), the out-degrees of boundary points are highly imbalanced due to the graph construction using a ball query. This causes their neighbors to be sparsely connected, making it difficult for useful boundary information to be sufficiently propagated in the representations of these points. Second, noisy connections in junctions of different parts result in the unreliable point neighbor relationships. As shown in Figure 2(a), conventional graph construction methods usually rely on Euclidean distance metrics without adequately considering geometric variations, thereby leading to inaccurate and noisy neighbor modeling.

In this paper, we propose a novel graph-based method equipped with graph smoothing and local geometry learning modules, which mitigate the two aforementioned issues, as demonstrated in Figures 1(b) and 2(b). To achieve this, we first systematically analyze the mechanisms responsible for the unreliable sparse and noisy connections originating from suboptimal graph structures, and then mitigate their side effects through a novel framework entitled GSPoint as in Figure 3. Specifically, our graph smoothing module is established by balancing the disparities of degrees, where we optimize the graph to alleviate both sparse and noisy connections inherent in suboptimal graph structures, thereby constructing more robust neighbor relationships. Subsequently, our local geometry learning module leverages local shape features and distribution features to provide geometric priors within the optimized point neighbors, thereby enhancing the feature extraction process. These two modules are employed in multiple blocks with hierarchical downsampling

(a) With normal ball query (b) With our method

**Figure 2.** Illustration of noisy connection. The constructed point neighborhoods indicate that (a) By the normal ball query, the constructed point cloud neighborhood might exhibit noisy connection, e.g., the neighbors of a point encompasses both fuselage and wing points. (b) Through our method, the neighbors of the point are refined to include only points from the fuselage.

strategy to achieve multi-scale feature extraction for downstream tasks. Our contributions are summarized as follows:

• We analyze the limitations of conventional graph structures for boundary points and junction areas, and then propose a graph smoothing module in our method to optimize the graph structures for reducing the negative impact of unreliable sparse and noisy connections. • We introduce a local geometry learning module, where the adaptive shape features extract complex local geometric information and the cylindrical coordinate can capture spatial distribution relationships within the optimized neighborhood. These components help to extract discriminative features and promote downstream tasks. • Extensive experiments on benchmark datasets for both point cloud classification and segmentation tasks demonstrated that our method achieved competitive performance. Furthermore, ablation studies validated the individual contribution of each component in our method.

Motivation and Analysis To extract point cloud features that are effective for downstream tasks, conventional graph-based methods typically construct a graph to model the similarity between points and then leverage convolution operations to aggregate point cloud neighbor information. Given a set of a point cloud P = {p1, p2,..., pn} where each point pi ∈R3 contains 3D coordinates, the feature extraction function at the l-th stage can be formulated as follows:

x(l+1)

i = A σ ψ

[x(l)

j ∥(pi −pj)]

j∈N (i)

, (1)

where x(l)

i ∈Rη denotes the feature vector of the i-th point at the l-th convolution stage, and ∥denotes vector concatenation. ψ: Rη+3 →Rη′ is a linear mapping function, σ(·) is an activation function, and A(·) is a permutation-invariant aggregation operator (e.g.,, max-pooling).

Here, N(i) denotes the neighbors of the point pi, and the construction of N(i) directly affects the performance of graph-based methods. Specifically, N(i) is typically constructed using the ball query algorithm with a predefined

12251

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-002-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

sym A xyz

MLP

Point Feature

Graph Smoothing

Local Geometry

Learning xyz

ResMLP

FPS

Point Feature

Graph Smoothing

Local Geometry

Learning xyz

ResMLP

Point Feature

Graph Smoothing

Local Geometry

Learning xyz

ResMLP

Point Feature

Graph

Feature Extraction xyz

ResMLP

Downstream

Task

()i  xyz

Point Feature

Eigenvalues

Cylindrical Coordinate

1DConv

2DConv & Pooling

()i

Ball Query & Symmetry

Graph Smoothing top-K

()i 

T S

FPS FPS

**Figure 3.** The proposed framework of GSPoint. Our method involves two key parts in the point cloud feature extraction process, i.e., graph smoothing module and local geometry learning module. Note that, FPS indicates farthest point sampling.

query radius r and a number of neighbors k, which can be mathematically represented as:

N(i) = Br,k(pi) = {pj ∈P | ρij ≤min(ρi(k), r)}, (2)

where ρi(k) is the distance from point pi to its k-th nearest neighbor, and ρij is the distance from pi to pj.

Subsequently, we construct a sparsely connected graph G = (V, E) based on the ball query method, where the vertices V = 1, 2,..., n represent individual points, and the edges E ⊆V × V denote the connections between pairs of points. The edge between points pi and pj is defined as:

E = {(i, j) | pj ∈Br,k(pi)}, (3)

and the corresponding adjacency matrix A ∈Rn×n is a sparse matrix, where aij = {1, if(i, j) ∈E; 0, otherwise}.

Previous work has primarily focused on improving the convolution process by adjusting the weights (Wang et al. 2019a; Xu et al. 2021) or adding edges based on semantic similarity (Yan et al. 2020; Zhang et al. 2023) to G, while overlooking the potential issue that the construction of the neighborhood Nk(i) could lead to a graph containing unreliable connections. In particular, these unreliable connections in the graph are typically sparse at boundary points and noisy in junction areas, which limits information propagation and hinders the extraction of discriminative features.

Let P = Pα ∪Pβ denote the partition of the point cloud into points inside and outside the radius. That is, Pα = {pi ∈P | ρi(k) ≤r} and Pβ = {pi ∈P | ρi(k) > r}.

For pu ∈Pα and pv ∈Pβ, considering the constraints of radius r and neighbor number k in Eq. (2) we observe:

ρu(k) ≤r,; ρv(k) > r ⇒ ru = ρu(k),; rv = r (4)

where ru and rv denote the actual radius of the two points. The variation of actual radius of different points indicates that the connections in the graph constructed by the ball query method are directional. In other words, there exists:

∃ρi(k) ≤ρij < ρj(k), (i, j)̸ ∈E, (j, i) ∈E. (5)

This directional property results in an inconsistency between the in-degree and out-degree. To examine the degree relationships, we visualize the out-degree distribution for each point as a heatmap in Figure 1 and provide a comprehensive analysis below. Sparse Connection. As shown in Figure 1(a), boundary points are generally located at regions with high curvature or along structural edges, which often encapsulate key geometric features and semantic information. For boundary points, the spatial distribution of points around them is inherently sparse, resulting in fewer neighboring points within the search radius r compared with internal points. Accordingly, the out-degree of a boundary point is expressed as:

d(out)

i ≤d(in)

i ≤k, (6)

where the out-degree d(out)

i indicates the number of neighbors that the point pi connects to, while the in-degree d(in)

i indicates the number of points that include pi as their neighbor. Due to the spatial distribution, fewer points include boundary points in their neighborhoods, resulting in sparse connections and this degree inequality.

These sparse connections restrict the propagation of boundary features to adjacent regions, potentially reducing the model’s ability to extract discriminative geometric features crucial for shape characterization. Noisy Connection. Junction points, which locate at the intersections of distinct instances, are characterized by high local point density where different instances exist in close Euclidean proximity. When employing ball query algorithms that rely solely on Euclidean distance metrics, these densely populated regions tend to generate noisy connections, as points from different instances are indiscriminately incorporated into the same neighborhood due to their spatial proximity. To be specific, for a junction point pi, the degree inequality contributes to these noisy connections:

d(out)

i ≥k = d(in)

i, (7)

with the in-degree d(in)

i equals exactly k because a junction point can include exactly k neighbors (as dictated by the algorithm’s constraint), while the out-degree dout i exceeds k due to the inclusion by multiple neighboring points. Such

12252

![Figure extracted from page 3](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

excessive and cross-instance connections, i.e., noisy connections lead to a scenario in which junction points propagate their features across structurally distinct instances, thereby blurring the crucial geometric and semantic boundaries.

For example, as depicted in Figure 2(a), a point on a fuselage might incorrectly incorporate several points from a wing into its neighborhood merely due to their spatial proximity, despite the clear structural separation. Our Motivation. The analysis above demonstrates the correlation between the unreliable connections (sparse at boundaries and noisy at junctions) and the resulting imbalance in degree distributions within the graph. This imbalance inherently stems from the limitations of fixed graph structures that rely on the Euclidean-distance-based ball query algorithm. Consequently, these suboptimal graph structures limit the model’s ability to extract discriminative features with the feature aggregation function as Eq. (1). In response, this paper aims to introduce a novel method which optimizes graph structures to address the unreliable sparse and noisy connections and incorporates richer geometric information to enable a more robust feature extraction.

## Method

Our method is abbreviated as GSPoint whose framework is shown in Figure 3. It employs a hierarchical downsampling architecture, where the graph smoothing module balances degree distribution through symmetric adjacency refinement and leverages graph smoothing process to capture multi-hop relationships within the graph. The local geometry learning module exploits the enhanced geometric properties of within the optimized neighborhoods of the smoothed graph to extract more discriminative features. Details are as follows.

Graph Smoothing

To address the limitations of unreliable sparse and noisy connections, we propose a graph smoothing module, where the symmetric adjacency refinement aims to establish balanced connections, and the finite steps graph smoothing aims to capture multi-hop relationships while maintain local similarities. This approach achieves a more uniform degree distribution, cf. Figure 1(b), and facilitates a more robust neighborhood construction, cf. Figure 2(b), thereby enhancing the model’s discriminative feature extraction capability. Symmetric Adjacency Refinement. To resolve structural asymmetry, we first enforce symmetric connectivity constraints through floor operation:

Asym =

A + A⊤

2

. (8)

This process eliminates directional connections and creates a real symmetric matrix Asym. After the transformation, the degrees satisfy the following relationship:

k ≥d(in)

u = d(out)

u ≥d(out)

v = d(in)

v, (9)

This symmetry prevents imbalances in connections during the subsequent graph smoothing process. Furthermore, we leverage the degree inequality in Eq.(9) for re-weighting Asym and conduct symmetric normalization as follows:

˜A = D−1/2AsymD−1/2, (10)

where D is the degree matrix of Asym, and di = Pn j=1 ˜aij is the degree of node i in the undirected graph. The symmetrically normalized adjacency matrix ˜A introduces normalized edge weight ˜aij = 1/ p didj, inversely scaling with degrees. This inverse proportionality underpins our key insights: low-degree boundary points gain higher weights, while high-degree junction points are adaptively suppressed, naturally balancing their influence in feature aggregation. Multi-hop Relationships in the Graph. Direct utilization of the refined adjacency matrix is suboptimal as sparse and noisy connections remain. To further create more connections for boundary points and suppress noise, we consider multi-hop relationships in the graph.

The weight between the i-th point and the j-th point considering all paths of length T in the graph is given by:

(˜AT)ij =

X ξ∈ΞT ij

T Y t=1

1 pdξt−1dξt

, (11)

where ξ0 = i and ξT = j, ΞT ij denotes the set of all possible paths of length T and ξt are intermediate points in the path. Due to the property of degree distribution in the graph, we have 1 √dv · 1 √ dξ1 > 1 √du · 1 √ dξ1 for a point pv with sparse connections and a point pu with more connections. When comparing paths with identical intermediate points (ξ1, ξ2,.., ξT −1) leading to pj, the path starting from pv to pj exceeds that from pu to pj, i.e.,

(˜AT)vj > (˜AT)uj, (12)

which indicates that within the T-hop neighborhood, the lower-degree point pv has higher propagation weights (˜AT)vj compared to the higher-degree point pu. This is expected to facilitate more connections to boundary points while mitigating the noise from junction points. von Neumann Kernel. However, the high-order terms of ˜A present two challenges. First, ˜AT is numerically unstable as the order T increases. Second, ˜AT cannot maintain local consistency, as it only considers paths exactly equal to T in length, ignoring shorter paths that are critical for the consistency of the local structure. Based on these considerations, we introduce the von Neumann kernel (Neumann et al. 2016) as the smoothing kernel in our graph smoothing process, which can be expressed as:

KNEU = (I −α ˜A)−1 = lim

T →∞

T X t=0

(α ˜A)t, (13)

where I denotes the identity matrix, and α ∈(0, 1) is an attenuation factor that controls the trade-off between local consistency and global connectivity by progressively suppressing higher-order terms.

The matrix KNEU can be viewed as a kernel function over the vertices of the graph, where KNEU(i, j) represents the

12253

<!-- Page 5 -->

(i, j)-th element of the matrix, indicating the strength of connection between vertices i and j after smoothing. The positive definiteness of KNEU ensures that:

∀i̸ = j, KNEU(i, i) ≥KNEU(i, j), (14)

which guarantees that each point maintains maximum weights on itself during the smoothing process. Compared with ˜AT which only considers paths of exact length of T, the von Neumann kernel considers all paths from 1 to T, providing a more stable graph structure. Finite Steps Graph Smoothing Process. For practical implementation of the von Neumann kernel, we approximate it with a finite sum to define our multi-hop graph smoothing process with the finite smoothing order T:

ST =

T X t=0

(α ˜A)t, α ∈(0, 1), (15)

and we obtain the final neighborhoods N ′(i) through the top-K selection for each row of ST. This process preserves the boundary amplification effect while maintaining computational efficiency. The progressive summation over t = 0,..., T optimizes the neighborhood of each point where sparsely connected boundary points rank higher in the top-K selection, with simultaneous suppression of noisy connections from junction points.

Local Geometry Learning To exploit the geometric representation of each point’s local neighborhood, which has been optimized by our graph smoothing method, we enhance the feature extraction function with two sets of adaptive features, i.e., local shape features and local distribution features. Local Shape Features. For a set of points, the eigenvalues of its covariance matrix contain rich geometry information. Previous works (Dong et al. 2017; Lin et al. 2014) derive classical shape descriptors such as planarity, sphericity, and linearity as hand-crafted geometric features. However, fixed descriptors might be not adaptable in complex structures or scenes. Therefore, we use a learnable network to transfer the eigenvalues into adaptive shape features.

Specifically, for each point pi with its N ′(i), we perform eigenvalue decomposition on its covariance matrix Ci:

Ci = ViΛiV⊤ i, (16)

where Λi = diag(λ(1)

i, λ(2)

i, λ(3)

i) contains the eigenvalues λ(1)

i ≥λ(2)

i ≥λ(3)

i ≥0, and Vi = [v(1)

i, v(2)

i, v(3)

i ] consists of the corresponding orthonormal eigenvectors of Ci.

Then we feed the eigenvalues into a learnable MLP network projecting them into η′-dimensional feature space as local shape features and denote it as ϕ(Λ). Local Distribution Features. To further capture the anisotropic and distance distribution information of the optimized neighborhoods, we complement the local geometry features with a cylindrical coordinate transformation that aligns the local structure along its principal axes. Based on the above eigenvalue decomposition, we compute the cylindrical coordinates of each neighbor point relative to the query point by projecting the displacement vector ∆pj = pj −pi onto three principal axes:

(x′ j, y′ j, z′ j) =

∆pj·v(2)

i, ∆pj·v(3)

i, ∆pj·v(1)

i

, (17)

and the new coordinate system is given by:

hj, ωj, cos θj

= z′ j, q x′ j

2 + y′ j

2, x′ j/ q x′ j

2 + y′ j

2. (18) To ensure numerical stability, both the height and radial distance are divided by their respective maximum values in the neighborhood, yielding the normalized values h′ and ω′.

Then, the neighbor points in the original Cartesian coordinates are transformed by (x, y, z) →(h′, ω′, cos θ) into the new cylindrical coordinate system as p′ = (h′, ω′, cos θ), where h′ quantifies the axial anisotropy and ω′ characterizes the radial distance distribution. This transformation enables us to leverage the local distribution information to implement our feature extraction function.

Finally, our feature extraction function with the mapping function ψ′: Rη+6 →Rη′ can be formulated as:

x(l+1)

i =

A σ ψ′

[x(l)

j ∥(pi −pj) ∥p′(l)

j ]

j∈N ′(i)

∥ϕ(Λi).

(19)

We integrate this enhanced feature extraction function with our graph smoothing module and hierarchical downsampling strategies, as illustrated in Figure 3, to achieve multi-stage feature extraction for point cloud analysis.

## Experiments

Comparison Methods. For point cloud classification and segmentation tasks, we compare our method with the following representative point cloud analysis methods: Point- Net++ (Qi et al. 2017b), PointTrans. (Zhao et al. 2021), PointMLP (Ma et al. 2022), PointNeXt (Qian et al. 2022), PointMAE (Pang et al. 2022), PointGPT (Chen et al. 2023), GSLCN (Liang et al. 2023), PointWavelet (Wen et al. 2025) and DuGREAT (Li, Wang, and Qiu 2025).

Point Cloud Classification We conduct point cloud classification tasks on Model- Net40 (Wu et al. 2015) and ScanObjectNN (Uy et al. 2019). Experimental Setups. The ModelNet40 dataset is a benchmark for synthetic 3D object classification. It comprises 9,843 training samples and 2,468 testing samples across 40 object categories. The ScanObjectNN dataset consists of 15,000 point cloud samples extracted from 2,902 unique object instances spanning 15 categories. In particular, the PB T50 RS subset of ScanObjectNN is particularly challenging due to real-world scanning artifacts such as noise, occlusion, and rotations. Following previous work (Qian et al. 2022; Ma et al. 2022), we use 1024 points without normals as input for both datasets. For ModelNet40, we apply random translations and train the model for 500 epochs. For ScanObjectNN, we augment data with random scaling and rotations, and train the model for 250 epochs.

12254

<!-- Page 6 -->

## Method

ModelNet40 ScanObjectNN mAcc(%) OA(%) mAcc(%) OA(%) PointNet++ (2017) 88.5 91.9 69.8 73.7 PointTrans. (2021) 90.6 93.7 – – PointMLP (2022) 91.3 94.1 83.9 85.4 PointNeXt (2022) 90.8 93.2 85.8 87.7 PointMAE (2022) – 93.8 – 85.2 PointGPT-S (2023) – 94.0 – 86.9 GSLCN (2023) 91.4 94.2 84.1 85.8 PointWavelet (2024) 91.1 94.3 85.8 87.7 DuGREAT (2025) 90.9 94.0 84.5 87.1 GSPoint (ours) 91.5 94.5 86.4 88.1

**Table 1.** Classification on ModelNet40 and ScanObjectNN

## Method

Cls.mIoU (%) Ins.mIoU (%) PointNet++ (2017) 81.9 85.1 PointMLP (2022) 84.6 86.1 PointNeXt (2022) 85.2 87.0 GSLCN (2023) 85.4 87.1 PointWavelet (2024) 85.2 86.8 DuGREAT (2025) 84.9 86.5 GSPoint (ours) 85.6 87.2

**Table 2.** Part Segmentation on ShapeNetPart

## Method

mIoU (%) OA (%) PointNet++ (2017) 56.0 86.4 PointNeXt (2022) 70.5 90.6 GSLCN (2023) 68.1 90.5 PointWavelet (2024) 71.3 – GSPoint (ours) 71.5 91.2

**Table 3.** Indoor Scene Segmentation on S3DIS

Classification on ModelNet40 and ScanObjectNN. In Table 1, we report the results with mean accuracy (mAcc) and overall accuracy (OA) to evaluate the effectiveness of all comparison method on object-level point cloud classification tasks. For ModelNet40, our method achieves an mAcc of 91.5% and an OA of 94.5%, demonstrating its competitive performance on synthetic object-level point cloud classification tasks. On the PB T50 RS subset of the ScanObjectNN dataset, our method obtains a mAcc of 86.4% and an OA of 88.1%. These results validate the good generalization of our method under challenging real-world conditions, including adverse factors of noise, occlusion, and rotation.

Point Cloud Segmentation We further evaluate our method on two challenging benchmarks for point cloud segmentation: part segmentation on ShapeNetPart (Chang et al. 2015) and indoor scene segmentation on S3DIS (Armeni et al. 2016). Experimental Setups. The ShapeNetPart dataset is widely used for 3D object part segmentation. It comprises 12,137 training models and 2,874 testing models across 16 object categories, with each model annotated with 2 to 6 parts, re-

Component Dataset (metric)

SA GS Λ p′ Model- Scan- Shape- S3DIS Net40 ObjectNN NetPart Area5 (OA) (OA) (Ins.mIoU) (mIoU) A 92.6 86.9 86.5 68.2 B ✓ 92.6 85.2 85.4 67.4 C ✓ 93.6 86.6 86.9 68.3 D ✓ ✓ 93.9 87.3 87.0 70.2 E ✓ 93.4 87.0 86.7 69.2 F ✓ 93.6 87.1 86.6 69.6 G ✓✓ 93.6 87.1 86.9 69.8 H ✓ ✓ ✓ 94.0 87.5 87.1 70.9 I ✓ ✓ ✓ 94.3 87.9 87.1 70.4 J ✓ ✓ ✓✓ 94.5 88.1 87.2 71.5

**Table 4.** Ablation study on our method’s key components. SA: symmetric adjacency refinement, GS: graph smoothing, Λ: adaptive shape features, p′: cylindrical coordinates.

sulting in a total of 50 distinct part labels. The S3DIS dataset includes six large-scale indoor areas with 271 rooms, where each point is annotated with one of 13 semantic categories, enabling rigorous studies in 3D semantic segmentation. Typically, Area5 is reserved for testing the generalization performance on unseen indoor scenes. For the ShapeNetPart dataset, each 3D shape is uniformly sampled to 2048 points. The training process spans 300 epochs, and data augmentation strategies including random scaling and point cloud jittering are applied. Following standard practice in previous work (Thomas et al. 2019), the raw point clouds from the S3DIS dataset are downsampled using voxels with a size of 0.04 m. Then the model is trained for 100 epochs using a combination of random scaling, rotation, and jittering. Part Segmentation on ShapeNetPart. In Table 2, we report the results with classification mean IoU (Cls.mIoU) and instance mean IoU (Ins.mIoU) to evaluate the effectiveness of all comparison method on point cloud part segmentation tasks on ShapeNetPart. Our approach achieves a Cls.mIoU of 85.6% and an Ins.mIoU of 87.2%, indicating that our proposed method is sufficient to preserve the local geometric details of object parts. Indoor Scene Segmentation on S3DIS Area5. In Table 3, we report the results with mean IoU (mIoU), mean accuracy (mAcc) and overall accuracy (OA) to evaluate the effectiveness of indoor scene segmentation task on the S3DIS Area5 benchmark. Our method achieves 71.5% mIoU, 77.8% mAcc, and 91.2% OA, demonstrating the robustness of our method within indoor scenes.

Ablation Study We perform ablation study to verify the components, and visualization to better understand how our method works. Effectiveness of Different Components. As shown in Table 4, we evaluate the contributions of key components through ten experimental configurations. Item-A reports the results of our model variant without the proposed four components. From Items-B,C,D, we can observe that symmetric adjacency refinement (SA) and graph smoothing (GS) alone play a small role, while the synergistic combination

12255

<!-- Page 7 -->

Ours+Method

Model- Scan- Shape- S3DIS Net40 ObjectNN NetPart Area5 (OA) (OA) (Ins.mIoU) (mIoU) + PointNet++ 93.0(↑1.1) 82.9(↑9.2) 84.1(↑2.2) 63.9(↑7.9) + PointMLP 94.4(↑0.3) 85.8(↑0.4) 85.0(↑0.4) – + PointNeXt 93.8(↑0.6) 87.9(↑0.2) 85.4(↑0.2) 70.8(↑0.3)

**Table 5.** The performance gain of our graph smoothing method as a plug-in for other point cloud analysis methods.

of SA and GS yields consistent improvements across all benchmarks (+1.3%, +0.4%, +0.5%, +2.0% improvements on ModelNet40, ScanObjectNN, ShapeNetPart, S3DIS). From Items-E,F,G, the similar results can be observed from the combination of using adaptive shape features (Λ) and cylindrical coordinates (p′). Compared with Item-A, it has +1.3%, +0.2%, +0.6%, +2.2% improvements on Model- Net40, ScanObjectNN, ShapeNetPart, S3DIS. Subsequent incorporation of (SA, GS, Λ) in Item-H and (SA, GS, p′) in Item-I further boosts performance, validating the effectiveness of encoding geometric priors in feature aggregation combined with the graph smoothing module. The full configuration (Item-J) achieves optimal results through component collaboration, confirming the effectiveness of our proposed framework across diverse tasks. Effectiveness of Graph Smoothing as a Plug-in. We conducted the experiments by integrating our graph smoothing method into other point cloud analysis methods in Table 5. As shown, our method consistently improves the performance on multiple tasks across different methods, further demonstrating its effectiveness and general applicability. Visualization Validation. Figure 4 shows the neighbors of the points obtained by our proposed graph smoothing method versus the neighbors of the points obtained by the normal ball query method. By comparing the details, we observe that our method constructs more accurate neighbors for specific points, effectively mitigates the sparse and noisy connections introduced by previous graph construction strategy. Figure 5 shows that in the process of our local geometry learning, the neighbors of the points obtained by our proposed cylindrical coordinate transformation and the neighbors of the points obtained by ordinary three-dimensional coordinates. It is also observed that our method can capture the geometric information of objects well and avoid the limitations of Euclidean space measurement. Hyper-Parameter Analysis. The main hyper-parameters in our method include α as the attenuation factor and T as the smoothing order. By iterating over their range of values with other fixed settings, we get the corresponding evaluation metrics OA on the ModelNet40 and ScanObjectNN datasets, Ins.mIoU on ShapeNetPart dataset and mIoU on S3DIS dataset. The results are shown in Figure 6, we can easily observe that on datasets ModelNet40, ScanObjectNN and ShapeNetPart, both hyper-parameters α and T are insensitive despite facing different classification and segmentation tasks. For the semantic segmentation task on the dataset S3DIS, our method performs better on the interval [0.4, 0.6] of α and the interval [3, 4] of T.

**Figure 4.** With normal ball query (upper row) vs. With our graph smoothing (bottom row).

(a) With xyz coordinate (b) With cylindrical coordinate

**Figure 5.** xyz coordinate vs. cylindrical coordinate.

(a) The attenuation factor α (b) The smoothing order T

**Figure 6.** Hyper-parameter analysis.

## Conclusion

In this paper, we provide an insightful analysis of traditional graph construction and ball query methods, identifying their inherent issue of suboptimal graph structures, which result in sparse connections at boundary points and noisy connections in junction areas. We propose a novel approach with a graph smoothing module to refine the structure and a local geometry learning module that enhances feature learning using adaptive geometric features and cylindrical coordinate transformation. Extensive experiments demonstrate the effectiveness of our method in classification and segmentation tasks. Future work will focus on improving model efficiency and generalization to unseen categories through selfsupervised learning, further advancing the practical applications of graph-based point cloud learning.

12256

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-graph-smoothing-for-enhanced-local-geometry-learning-in-point-cloud-analysis/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This research was supported in part by the National Key Research & Development Program of China under Grant 2022YFA1004100, in part by National Natural Science Foundation of China under Grant 62476048, and in part by the Ministry of Education, Singapore, under its MOE Academic Research Fund Tier 2 (MOE-T2EP20124-0013).

## References

Armeni, I.; Sener, O.; Zamir, A. R.; Jiang, H.; Brilakis, I.; Fischer, M.; and Savarese, S. 2016. 3d semantic parsing of large-scale indoor spaces. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1534–1543. Chang, A. X.; Funkhouser, T.; Guibas, L.; Hanrahan, P.; Huang, Q.; Li, Z.; Savarese, S.; Savva, M.; Song, S.; Su, H.; et al. 2015. Shapenet: An information-rich 3d model repository. arXiv preprint arXiv:1512.03012. Chen, G.; Wang, M.; Yang, Y.; Yu, K.; Yuan, L.; and Yue, Y. 2023. Pointgpt: Auto-regressively generative pre-training from point clouds. In Advances in Neural Information Processing Systems, 29667–29679. Chen, J.; Ling, Y.; Xu, J.; Ren, Y.; Huang, S.; Pu, X.; Hao, Z.; Yu, P. S.; and He, L. 2025. Variational Graph Generator for Multiview Graph Clustering. IEEE Transactions on Neural Networks and Learning Systems, 36(6): 11078–11091. Dong, W.; Lan, J.; Liang, S.; Yao, W.; and Zhan, Z. 2017. Selection of LiDAR geometric features with adaptive neighborhood size for urban land cover classification. International Journal of Applied Earth Observation and Geoinformation, 60: 99–110. Du, Z.; Liang, J.; Liang, J.; Yao, K.; and Cao, F. 2024. Graph Regulation Network for Point Cloud Segmentation. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(12): 7940–7955. Du, Z.; Ye, H.; and Cao, F. 2022. A novel local–global graph convolutional method for point cloud semantic segmentation. IEEE Transactions on Neural Networks and Learning Systems, 35(4): 4798–4812. Guo, M.-H.; Cai, J.-X.; Liu, Z.-N.; Mu, T.-J.; Martin, R. R.; and Hu, S.-M. 2021. Pct: Point cloud transformer. Computational Visual Media, 7: 187–199. Han, Y.; Zhao, N.; Chen, W.; Ma, K. T.; and Zhang, H. 2024. Dual-perspective knowledge enrichment for semisupervised 3d object detection. In Proceedings of the AAAI Conference on Artificial Intelligence, 2049–2057. He, H.; Xu, J.; Wen, G.; Ren, Y.; Zhao, N.; and Zhu, X. 2025. Graph embedded contrastive learning for multi-view clustering. In Proceedings of the International Joint Conference on Artificial Intelligence, 5336–5344. Jiang, S.; Zhao, Q.; Rahmani, H.; Soh, D. W.; Liu, J.; and Zhao, N. 2025. GaussianBlock: Building Part-Aware Compositional and Editable 3D Scene by Primitives and Gaussians. In International Conference on Learning Representations.

Li, L.; and Zhao, N. 2024. End-to-end semi-supervised 3d instance segmentation with pcteacher. In IEEE International Conference on Robotics and Automation, 5352–5358. Li, X.; Wang, Q.; and Qiu, B. 2025. Dual-path geometric relation-aware transformer for point cloud classification and segmentation. Applied Soft Computing, 174: 112801. Li, Y.; Zhao, N.; Xiao, J.; Feng, C.; Wang, X.; and Chua, T.s. 2024. Laso: Language-guided affordance segmentation on 3d object. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 14251–14260. Liang, J.; Du, Z.; Liang, J.; Yao, K.; and Cao, F. 2023. Long and Short-Range Dependency Graph Structure Learning Framework on Point Cloud. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(12): 14975– 14989. Lin, C.-H.; Chen, J.-Y.; Su, P.-L.; and Chen, C.-H. 2014. Eigen-feature analysis of weighted covariance matrices for LiDAR point cloud classification. ISPRS Journal of Photogrammetry and Remote Sensing, 94: 70–79. Ma, X.; Qin, C.; You, H.; Ran, H.; and Fu, Y. 2022. Rethinking network design and local geometry in point cloud: A simple residual MLP framework. arXiv preprint arXiv:2202.07123. Maturana, D.; and Scherer, S. 2015. Voxnet: A 3d convolutional neural network for real-time object recognition. In IEEE/RSJ International Conference on Intelligent Robots and Systems, 922–928. Mo, Y.; Peng, L.; Xu, J.; Shi, X.; and Zhu, X. 2022. Simple unsupervised graph representation learning. In Proceedings of the AAAI Conference on Artificial Intelligence, 7797– 7805. Neumann, M.; Garnett, R.; Bauckhage, C.; and Kersting, K. 2016. Propagation kernels: efficient graph kernels from propagated information. Machine Learning, 102: 209–245. Pan, Y.; Cui, Q.; Yang, X.; and Zhao, N. 2025. How Do Images Align and Complement LiDAR? Towards a Harmonized Multi-modal 3D Panoptic Segmentation. In International Conference on Machine Learning. Pang, Y.; Wang, W.; Tay, F. E.; Liu, W.; Tian, Y.; and Yuan, L. 2022. Masked Autoencoders for Point Cloud Selfsupervised Learning. In European Conference on Computer Vision, 604–621. Peng, L.; Mo, Y.; Xu, J.; Shen, J.; Shi, X.; Li, X.; Shen, H. T.; and Zhu, X. 2023. GRLC: Graph representation learning with constraints. IEEE Transactions on Neural Networks and Learning Systems, 35(6): 8609–8622. Qi, C. R.; Su, H.; Mo, K.; and Guibas, L. J. 2017a. Pointnet: Deep learning on point sets for 3d classification and segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 652–660. Qi, C. R.; Yi, L.; Su, H.; and Guibas, L. J. 2017b. Pointnet++: Deep hierarchical feature learning on point sets in a metric space. In Advances in Neural Information Processing Systems, 5105–5114. Qian, G.; Li, Y.; Peng, H.; Mai, J.; Hammoud, H.; Elhoseiny, M.; and Ghanem, B. 2022. Pointnext: Revisiting pointnet++

12257

<!-- Page 9 -->

with improved training and scaling strategies. In Advances in Neural Information Processing Systems, 23192–23204. Sheng, H.; Cai, S.; Zhao, N.; Deng, B.; Huang, J.; Hua, X.- S.; Zhao, M.-J.; and Lee, G. H. 2022. Rethinking IoU-based optimization for single-stage 3D object detection. In European Conference on Computer Vision, 544–561. Sheng, H.; Cai, S.; Zhao, N.; Deng, B.; Liang, Q.; Zhao, M.- J.; and Ye, J. 2025. CT3D++: Improving 3D Object Detection with Keypoint-Induced Channel-wise Transformer. International Journal of Computer Vision, 133(7): 4817–4836. Sohail, S. S.; Himeur, Y.; Kheddar, H.; Amira, A.; Fadli, F.; Atalla, S.; Copiaco, A.; and Mansoor, W. 2024. Advancing 3D point cloud understanding through deep transfer learning: A comprehensive survey. Information Fusion, 102601. Thomas, H.; Qi, C. R.; Deschaud, J.-E.; Marcotegui, B.; Goulette, F.; and Guibas, L. J. 2019. Kpconv: Flexible and deformable convolution for point clouds. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 6411–6420. Uy, M. A.; Pham, Q.-H.; Hua, B.-S.; Nguyen, T.; and Yeung, S.-K. 2019. Revisiting point cloud classification: A new benchmark dataset and classification model on real-world data. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 1588–1597. Wang, J.; Cheng, Z.; Zhao, N.; Cheng, J.; and Yang, X. 2024. On-the-fly Point Feature Representation for Point Clouds Analysis. In Proceedings of the 32nd ACM International Conference on Multimedia, 9204–9213. Wang, J.; and Zhao, N. 2025. Uncertainty Meets Diversity: A Comprehensive Active Learning Framework for Indoor 3D Object Detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 20329–20339. Wang, L.; Huang, Y.; Hou, Y.; Zhang, S.; and Shan, J. 2019a. Graph attention convolution for point cloud semantic segmentation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 10296–10305. Wang, X.; Yang, X.; Xu, Y.; Wu, Y.; Li, Z.; and Zhao, N. 2025a. AffordBot: 3D Fine-grained Embodied Reasoning via Multimodal Large Language Models. In Advances in Neural Information Processing Systems. Wang, X.; Zhao, N.; Han, Z.; Guo, D.; and Yang, X. 2025b. Augrefer: Advancing 3d visual grounding via cross-modal augmentation and spatial relation-based referring. In Proceedings of the AAAI Conference on Artificial Intelligence, 8006–8014. Wang, Y.; Sun, Y.; Liu, Z.; Sarma, S. E.; Bronstein, M. M.; and Solomon, J. M. 2019b. Dynamic graph cnn for learning on point clouds. ACM Transactions on Graphics, 38(5): 1– 12. Wen, C.; Long, J.; Yu, B.; and Tao, D. 2025. PointWavelet: Learning in Spectral Domain for 3-D Point Cloud Analysis. IEEE Transactions on Neural Networks and Learning Systems, 36(3): 4400–4412. Wu, X.; Jiang, L.; Wang, P.-S.; Liu, Z.; Liu, X.; Qiao, Y.; Ouyang, W.; He, T.; and Zhao, H. 2024. Point Transformer V3: Simpler Faster Stronger. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 4840–4851. Wu, Z.; Song, S.; Khosla, A.; Yu, F.; Zhang, L.; Tang, X.; and Xiao, J. 2015. 3d shapenets: A deep representation for volumetric shapes. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1912– 1920. Wu, Z.; Wang, Y.; Feng, M.; Xie, H.; and Mian, A. 2023. Sketch and text guided diffusion model for colored point cloud generation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 8929–8939. Xiu, J.; Li, Y.; Zhao, N.; Fang, H.; Wang, X.; and Yao, A. 2025. Geometric Alignment and Prior Modulation for View- Guided Point Cloud Completion on Unseen Categories. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 27435–27444. Xu, J.; Ren, Y.; Wang, X.; Feng, L.; Zhang, Z.; Niu, G.; and Zhu, X. 2024. Investigating and mitigating the side effects of noisy views for self-supervised clustering algorithms in practical multi-view scenarios. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 22957–22966. Xu, M.; Ding, R.; Zhao, H.; and Qi, X. 2021. Paconv: Position adaptive convolution with dynamic kernel assembling on point clouds. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 3173– 3182. Yan, X.; Zheng, C.; Li, Z.; Wang, S.; and Cui, S. 2020. Pointasnl: Robust point clouds processing using nonlocal neural networks with adaptive sampling. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 5589–5598. Yu, X.; Tang, L.; Rao, Y.; Huang, T.; Zhou, J.; and Lu, J. 2022. Point-bert: Pre-training 3d point cloud transformers with masked point modeling. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 19313–19322. Yuan, Z.; Jiang, S.; Feng, C.-M.; Zhang, Y.; Cui, S.; Li, Z.; and Zhao, N. 2025. Scene-R1: Video-Grounded Large Language Models for 3D Scene Reasoning without 3D Annotations. arXiv preprint arXiv:2506.17545. Zhang, N.; Pan, Z.; Li, T. H.; Gao, W.; and Li, G. 2023. Improving graph representation for point cloud segmentation via attentive filtering. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 1244–1254. Zhao, H.; Jiang, L.; Jia, J.; Torr, P. H.; and Koltun, V. 2021. Point transformer. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 16259–16268. Zhao, N.; Qian, P.; Wu, F.; Xu, X.; Yang, X.; and Lee, G. H. 2025. SDCoT++: Improved Static-Dynamic Co-Teaching for Class-Incremental 3D Object Detection. IEEE Transactions on Image Processing, 34: 4188–4202. Zhou, Y.; and Tuzel, O. 2018. Voxelnet: End-to-end learning for point cloud based 3d object detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 4490–4499.

12258
