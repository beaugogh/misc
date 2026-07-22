---
title: "Cross-view Anchor Graph Learning and Factorization for Incomplete Multi-view Clustering"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39865
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39865/43826
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Cross-view Anchor Graph Learning and Factorization for Incomplete Multi-view Clustering

<!-- Page 1 -->

Cross-view Anchor Graph Learning and Factorization for Incomplete Multi-view

Clustering

Xinxin Wang1,3, Yongshan Zhang2*, Xiaochen Yuan4, Yicong Zhou5

1School of Artificial Intelligence, Shenzhen University 2School of Computer Science, China University of Geosciences 3Guangdong Provincial Key Laboratory of Intelligent Information Processing 4Faculty of Applied Sciences, Macau Polytechnic University 5Department of Computer and Information Science, University of Macau xinxinwang1024@gmail.com, yszhang.cug@gmail.com, xcyuan@mpu.edu.mo, yicongzhou@um.edu.mo

## Abstract

Graph-based incomplete multi-view clustering algorithms have gathered much attention due to their impressive clustering performance. However, existing methods primarily leverage intra-view correlation from observed views, while ignoring the exploration of explicit compensation relationships between different views. Moreover, these methods need postprocessing to get labels, and the separate steps lack negotiation, which may lead to sub-optimal solutions. To address these issues, we propose a Cross-view Anchor Graph Learning and Factorization (AGLF) method. AGLF develops an Anchor Graph Completion (AGC) framework that explicitly learns the missing subgraph structures. Instead of requiring post-processing, AGC directly produces soft labels. By establishing a third-order tensor of soft labels, it employs the tensor Schatten p-norm to enhance anchor graph learning and factorization. To significantly improve the quality of subgraph learning, AGLF incorporates compensation subgraphs from supplementary views into the AGC framework, enabling the construction of a better anchor graph for label learning. An optimization algorithm is devised to solve the objective function. Experimental results across various datasets demonstrate the effectiveness of our method.

## Introduction

Multi-view clustering exploits the consistent and complementary information among views to enhance clustering performance and have been extensively deployed in applications that have no label information (Hu, Shi, and Ye 2022; Qin et al. 2025). For example, they use hyperspectral and multispectral images to recognize land cover in earth observation (Wang, Zhang, and Zhou 2025c; Zhang et al. 2025b), as well as utilize textual information, click records, and user behavior logs to recommend news articles (Wang et al. 2021). However, existing multi-view clustering methods assume that all views of samples are complete. This assumption can be easily violated in real scenarios due to data corruption and equipment malfunction (Wen et al. 2023b; Liu et al. 2023). Therefore, when multi-view clustering approaches are directly applied to incomplete multi-view data, they often experience significant performance degradation

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

or even complete failure. Consequently, Incomplete Multiview Clustering (IMVC) has become a significant challenge.

To solve this problem, various solutions have been proposed in literature (Li et al. 2025; Qin and Qian 2024; Qin, Feng, and Zhang 2025). These existing incomplete clustering methods can be divided into three categories: representation-based, kernel-based, and graph-based. Representation-based IMVC methods typically transform the incomplete multi-view features into a unified representation. The work in (Wen et al. 2020b) utilized enhanced matrix factorization to obtain a unified latent embedding, on which K-mean is applied to yield final clustering results. The work in (Lin et al. 2021) applied contrastive learning to obtain discriminative presentation and clustering prediction. With the development of kernel technologies, many researchers developed IMVC methods based on kernel learning (Liu et al. 2019; Li et al. 2022a; Zhang et al. 2025a). These methods map all views into kernel space and then impute incomplete kernels for clustering. The third category of IMVC method involves the application of graph-based information to obtain clustering results (Cui et al. 2022; Li et al. 2022b, 2024c; Xia et al. 2022). These methods fuse multiple graphs to create a consensus graph, on which spectral clustering technologies are applied to obtain final clustering results. For example, Wen et al. proposed a subspace learning framework that uses tensor technologies to constrain graph learning (Wen et al. 2021). The works in (Wang, Zhang, and Zhou 2025a; Wen et al. 2023a) explored high-confidence information from the graph of each viewpoint to guide the learning of the consensus graph.

These aforementioned methods have achieved extensive success in IMVC. However, we observe that the complementary information in incomplete data is not adequately exploited. Furthermore, graph-based methods leverage only observed views for intra-view correlations of samples, ignoring the potential structural information for missing views. Additionally, most methods require separate post-processing to yield final clustering results, which may lead to suboptimal outcomes. To address these problems, this paper proposes a Cross-view Anchor Graph Learning and Factorization (AGLF) method, which unifies cross-view imputation and clustering partition into a single optimization process and incorporates a low rank tensor constraint to cap-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

26570

<!-- Page 2 -->

ture complementary information for improved partitioning. Specifically, since anchor graph can reduce the computational and storage burdens compared to full graph, we first construct an anchor graph for each view, filling in zero values for the elements missing from incomplete views. Then, inspired by the clustering efficiency of non-negative matrix factorization (Wang et al. 2025), we introduce an explicit subgraph matrix to fill the missing elements in anchor graph and decompose it to derive the clustering indicators. Meanwhile, a tensor Schatten p-norm is imposed on a third-order tensor constructed with indicator matrices to explore the complementary information. Finally, inspired by the potential information compensation from supplementary views, we construct supplementary view data for each view and use it to further enhance subgraph learning. The main contributions are summarized as follows:

• We propose an Anchor Graph Completion (AGC) framework, which unifies missing subgraph learning and graph decomposition in a unified model, incorporating a tensor Schatten p-norm on indicator tensor to enhance these processes. • We construct supplementary view data matrices and utilize dynamic anchors to learn missing subgraphs, effectively exploring the compensation relationships between missing views and cross-view observed data. • We propose an effective optimization algorithm to solve the objective function, which scales well with data size. Comprehensive experimental results clearly demonstrate the efficacy of the proposed AGLF method.

## Related Work

Graph-based IMVC methods utilize graph structures to capture correlations among samples, applying clustering techniques to the fused consensus graph to derive final clustering results (Wen et al. 2020a). However, constructing a full graph from the entire original dataset can lead to redundant information and waste resources (Zhang et al. 2024). The anchor approach has emerged as an alternative and is gaining increasing attention (Liu et al. 2024). It first generates m representative data points P(v) ∈Rdv×m from entire data X(v) ∈Rdv×n to serve as anchors. Then, it constructs the anchor graph E(v) ∈Rm×n that characterizes the relationships between m anchors and n original data points. This significantly reduces computational and storage costs compared to a full graph, as m ≪n. Inspired by this, Wang et al. proposed an anchor graph-based IMVC method, IMVC- CBG (Wang et al. 2022). To adequately explore view information diversity, Liu et al. proposed FIMVC-VIA that utilizes view-independent anchors to learn a consensus anchor graph (Liu et al. 2022). Li et al. developed a parameterfree PSIMVC-PG method to enhance model practicability (Li et al. 2024b). To mitigate the randomness impact associated with heuristic anchors, (Chen et al. 2023) introduced dynamic anchor learning to improve model stability. To address the cross-view anchor misalignment problem, (Li et al. 2023) introduced a predefined anchor-level guiding graph to align dynamic anchors during learning process. The work RISE (Wang, Zhang, and Zhou 2025b) addressed the issue of rotational mismatch in the spectral embedding process of incomplete anchor graphs. Drawing on the outstanding representation learning capability of neural networks, CPSCAN leveraged the distribution calibration capability of anchors to enhance latent embedding alignment and imputation (Jin et al. 2023). The PMIMC work applied contrastive learning to strengthen anchors used for imputing missing data (Yuan et al. 2025). These methods have shown significant success, highlighting the substantial potential of anchors. However, they primarily focus on leveraging intra-view correlations of samples from observed views, neglecting the exploration of compensation relationships between different views.

## Methodology

Notations This section introduces the notations used throughout paper. We use bold calligraphy letters for third-order tensors, F ∈Rn1×n2×n3, bold upper case letters for matrices, F, bold lower case letters for vectors, f, and lower case letters such as fi,j for the element in F. We use F(i) to represent the i-th frontal slice of F. F = fft(F, [], 3) and F = ifft(F, [], 3) are the discrete Fourier transform (DFT) of F along the third dimension and its reverse operation. Moreover, tr(F) and FT stand for the trace and transpose of matrix F. The F-norm of F is denoted by ∥F∥F. To save space, we present only the definition of tensor Schatten pnorm; more definitions can be found in (Kilmer and Martin 2011). Definition 1. (Gao et al. 2021) Given a third-order tensor F ∈Rn1×n2×n3, the tensor Schatten p-th norm of F is defined as

∥F∥p sp ⃝= n3 X i=1

F

(i)

p sp ⃝

! 1 p

=



 n3 X i=1 min(n1,n2) X j=1 σj

F

(i) p





1 p

(1) where σj

F

(i)

is the j-th singular value of matrix F

(i), 0 < p ≤1. Recent researches show that when p is appropriately chosen, the Schatten p-norm provides an effective improvement for seeking tighter approximation of the rank function (Li et al. 2024a).

Proposed Formula We first construct a local anchor graph from the observed features for each view, reducing computational and storage costs. Next, we aim to explicitly fill in the missing elements corresponding to the absent views and decompose the combined anchor graph to achieve the final clustering results. We formulate this process as an Anchor Graph Completion (AGC) framework:

Gv,Fv min av,Mv

V X v=1 a2 v

Ev + MvPv −GvFT v

F + λ1 ∥F∥p sp ⃝ s.t. MT v1 = 1, Mv ≥0, GT vGv = I, Fv ≥0, aT1 = 1, av ≥0,

(2)

where Ev ∈Rm×n is an anchor graph constructed on incomplete data, with missing elements filled with zero val-

26571

<!-- Page 3 -->

ues. Mv ∈Rm×nv represents missing information as a subgraph, with column normalization applied to avoid trivial solutions. Pv ∈{0, 1}nv×n is an index matrix used to place the similarity elements of Mv into the missing positions. Gv ∈Rm×k is a basis matrix, with an orthogonal constraint imposed to enhance the discriminability of the bases. Fv ∈Rn×k is an indicator matrix. av is the view weight used to balance contributions from different views, and λ1 is the trade-off parameter. Moreover, we stack matrices Fv into a third-order tensor as lateral slices and impose a tensor Schatten p-norm minimization constraint on F. This operation ensures a cross-view spatial low-rank structure for indicators of each sample, which effectively captures complementary information from different views.

In model (2), cross-view complementary information is explored solely on indicators using tensor learning, while subgraph information is inferred within view by minimizing data reconstruction loss. However, when the missing ratio is large, the limited observed information in the incomplete anchor graphs Ev may fail to effectively recover the missing data, leading to significant performance degradation. To address this problem, we propose to explicitly exploit the complementary information from data as follows:

min

Ω

V X v=1 a2 v

Ev + MvPv −GvFT v

2

F + λ1 ∥F∥p sp ⃝

+λ2 ∥WvXv −AvMv∥2

F s.t. MT v1 = 1, Mv ≥0, GT vGv = I, Fv ≥0, aT1 = 1, av ≥0, WT vWv = I, AT vAv = I,

(3)

where Ω= {av, Mv, Gv, Fv, Wv, Av} is a set of variables. v indicates the supplementary views of v-th view. Xv ∈Rdv×nv represents the supplementary matrix for the v-th view, which concatenates the supplementary views along the column dimension. Wv ∈Rh×dv is a projection matrix that enhances feature discriminability. Av ∈Rh×m consists of dynamic anchors learned to disclose the clustering structure from complementary data. λ2 is a trade-off parameter. The proposed third term leverages supplementary data across views to identify alternatives for missing information through dynamic anchor-based graph learning. It effectively expands the utilization of observed data by emphasizing inter-view information interaction.

Optimization Inspired by Augmented Lagrange Multiplier (ALM), we introduce an auxiliary variable J, and let J = F. Then we rewrite the objective function as the following separable augmented Lagrange function:

min

Ω

V X v=1 a2 v

Ev + MvPv −GvFT v

2

F + λ1 ∥J ∥p sp ⃝

+ λ2 ∥WvXv −AvMv∥2

F + ρ

2∥F −J ∥2 F

+ ⟨Y, F −J ⟩ s.t. MT v1 = 1, Mv ≥0, GT vGv = I, Fv ≥0, aT1 = 1, av ≥0, WT vWv = I, AT vAv = I,

(4)

where Ω= {av, Mv, Gv, Fv, J, Wv, Av} are variables to be solved. Y is the Lagrange multiplier and ρ > 0 is the penalty parameter. Then, we can solve each variable individually while fixing the others.

Update Gv with fixed {av, Mv, Fv, J, Wv, Av}, Eq. (4) becomes:

min GT vGv=I

Ev + MvPv −GvFT v

2

F (5)

which can be obviously written as:

max GT vGv=I tr

GT v(Ev + MvPv)Fv

(6)

To solve Eq. (6), we introduce the following Theorem 1.

Theorem 1. For the following optimization problem, the optimal solution of max

G tr

GTB s.t. GTG = I,

(7)

is G = U[I, 0]VT, where U and V are the left-singular vectors and right-singular vectors, produced by singular value decomposition (SVD) on B.

Proof. From SVD solution B = UΣVT and together with Eq. (7), it is evident that tr

GTB

= tr

GTUΣVT

= tr

ΣVTGTU

= tr (ΣH) (8)

where H = VTGTU, Σi,i and Hi,i are the i-th row and column elements from Σ and H, respectively. We can simply verify HHT = I, where I is an identity matrix. Consequently, Σi,i ≥0 and −1 ≤Hi,i ≤1. Thus, we have:

tr

GTB

=

X i

Σi,iHi,i ≤

X i

Hi,i. (9)

The equality holds when H is an identity matrix. Therefore, when H = [I, 0], tr

GTB reaches its maximum. Thus, we get the solution of Eq. (6) is: G = U[I, 0]VT.

Update Fv with fixed {av, Mv, Gv, J, Wv, Av}, Eq. (4) becomes:

min

Fv a2 v

Ev + MvPv −GvFT v

2

F + ρ

2

Fv −Jv + Yv ρ

2

F s.t. Fv ≥0.

(10) And minimizing Eq. (10) is equivalent to min Fv≥0

Fv − a2 v(Ev + MvPv)TGv + ρ

2(Jv −Yv ρ)

av + ρ

2

2

F

.

(11) The solution of Eq. (11) is:

Fv = a2 v(Ev + MvPv)TGv + ρ

2(Jv −Yv ρ)

av + ρ

2

!

+

. (12)

26572

<!-- Page 4 -->

Update Mv with fixed {av, Gv, Fv, J, Wv, Av}, Eq. (4) becomes:

min

Mv a2 v ∥Qv + MvPv∥2

F + λ2 ∥WvXv −AvMv∥2

F.

s.t. MT v1 = 1, Mv ≥0, WT vWv = I, AT vAv = I,

(13) where Qv = Ev −GvFT v. And Eq. (13) can be transformed into following equivalence problem:

min MT v1=1,Mv≥0

Mv −−a2 vQvPT v + λ2AT vWvXv av + λ2

2

F

.

(14) Eq. (14) is an euclidean projection problem on the simplex space, which has a closed-form solution (Wang, Zhang, and Zhou 2025d).

Update J with fixed {av, Mv, Gv, Fv, Wv, Av}, Eq. (4) becomes:

min

J λ1 ∥J ∥p sp ⃝+ρ

2

F −J + Y ρ

2

F

, (15)

which has a closed-form as Lemma 1 (Gao et al. 2021):

Lemma 1. Given a third-order tensor C ∈Rn1×n2×n3 and its tensor singular value decomposition C = U∗Σ∗VT. The optimal solution of min

J β ∥J ∥p sp ⃝+1

2 ∥J −C∥2 F, (16)

is J ∗= Sτ(C) = U ∗ifft(Γτ(Σ)) ∗VT, where Γτ(Σ) is a f-diagonal tensor in Fourier domain, whose diagonal elements can be obtained by using the GST algorithm introduced in (Gao et al. 2021).

By utilizing Lemma 1, the solution of J in Eq. (15) is:

S λ1 ρ (F + Y ρ). (17)

Update Av with fixed {av, Mv, Gv, Fv, J, Wv}, Eq. (4) becomes:

min AT vAv=I ∥WvXv −AvMv∥2

F, (18)

which is equivalent to:

max AT vAv=I tr

AT vWvXvMT v

. (19)

According to Theorem 1, we get the closed-form solution.

Update Wv with fixed {av, Mv, Gv, Fv, J, Av}, Eq. (4) becomes:

min WT vWv=I ∥WvXv −AvMv∥2

F, (20)

which can be written as:

max WT vWv=I tr

WT vAvMvXT v

. (21)

Similarly, Eq.(21) has a closed-form solution as Eq.(19).

Update av with fixed {Mv, Gv, Fv, J, Wv, Av}, Eq. (4) becomes:

min av

V X v=1 a2 vr2 v s.t.av ≥0, a⊤1 = 1, (22)

where rv =

Ev + MvPv −GvFT v

F. According to Cauchy-Schwarz’s inequality, we can get the optimal solution of av by av =

1 rv PV v=1

1 rv

. (23)

Finally, the entire optimization procedure for Eq. (4) is listed in Algorithm 1. The code is available at https://github.com/W-Xinxin/AGLF

## Algorithm

1: AGLF

Input: Data matrices {Xv}V v=1 ∈Rdv×(n−nv), the number of anchors m, the number of clusters k. Output: Clustering labels of data points.

1: Initialize Mv = 0, Gv = 0, Fv = Jv = 0, Y = 0, Wv = 0, Av = 0, av = 1

V, ρ = 10−4

2: Compute graph Ev and construct Xv for each view. 3: while not converge do 4: Update Gv by solving Eq. (6); 5: Update Fv by solving Eq. (12); 6: Update J by solving Eq. (17); 7: Update Mv by solving Eq. (14); 8: Update Av by solving Eq. (19); 9: Update Wv by solving Eq. (21); 10: Update av by Eq. (23); 11: Update Y and ρ: Y = Y + ρ(F −J), ρ = min(µρ, 1012); 12: end while 13: Calculate the clustering results by using F = PV v=1 a2 vFv/ PV v=1 a2 v. 14: return Clustering result.

Convergence Analysis Our objective function (4) is bounded since it is a sum of various terms with positive norms. The optimization algorithm divides the optimization problem into six sub-procedures, each solving for one variable while keeping the others fixed. Each sub-problem is monotonically decreasing, allowing our algorithm to converge to a local optimum, as supported by the convergence theorem in (Rudin 1976). The empirical results presented in the experiment section demonstrate this point in practice.

Complexity Analysis Our method consists of two stages: 1) Construction of Ev; 2) using Algorithm 1 to solve Eq. (4). The first stage costs O(V nmd + V nmlog(m)), where d is the sum of the feature dimensions on each view. The second stage focuses

26573

<!-- Page 5 -->

on solving {Mv, Fv, Gv, J, Wv, Av}. The complexity for updating these variables iteratively are O(V nmk + PV v=1 hmnvdv + PV v=1 mnv),O(V nmk), O(V nmk + V mk2), O(2V nklog(V k) + V 2kn), O(PV v=1 hmnvdv + dvh2), and O(PV v=1 hmnvdv + mh2). Due to m ≪n, and k, V are small constants, the main computational complexity of solving (4) is O(V nmk + PV v=1 hmnvdv). Therefore, the total computational complexity is O(V nmd + PV v=1 hmnvdv), highlighting that our method scales well with data size.

## Experiments

Datasets and Baselines We evaluate the performance of our algorithm on six extensively used multi-view datasets: MSRCv1, BDGP, Caltech101-7, CCV, Animal, and FMNIST. The details of these datasets are demonstrated in Table 1.

Datasets Samples Cluster View

MSRCv1 210 7 Caltech101-7 7 6 BDGP 3 CCV 20 3 Animal 11673 20 4 FMNIST 60000 10 3

**Table 1.** Description of used multi-view datasets

Following the common approach in (Wang, Zhang, and Zhou 2025b; Wang et al. 2022), we set 9 missing ratios ω = [0.1: 0.1: 0.9] to represent the percentage of samples with incomplete views. When ω = 0.1, we randomly select 10% of the samples to drop partial views, ensuring that at least one view is retained.

Our algorithm is compared with the following incomplete multi-view clustering methods: UEAF (Wen et al. 2019), IMVC-CBG (Wang et al. 2022), FIMVC-VIA (Liu et al. 2022), PIMVC (Deng et al. 2023), CPSCAN (Jin et al. 2023), PSIMVC-PG (Li et al. 2024b), DIVIDE (Lu et al. 2024), PMIMC (Yuan et al. 2025), RISE (Wang, Zhang, and Zhou 2025b). They are introduced in related work.

Implementation Details For experimental fairness, the hyperparameters for the aforementioned methods are set to the recommended values specified in their original papers. For our model, the parameter λ1 is searched in [10−2, 10−1,..., 102] and the parameter λ2 is adjusted in [10−5, 10−4,..., 105]. The traditional models: UEAF, IMVC-CBG, FIMVC-VIA, PIMVC, PSIMVC-PG, and RISE were performed on a computer with a 3.5GHz AMD Ryzen 9 3950x CPU and 64GB of RAM, utilizing MATLAB 2022b (64-bit), while the deep learning models: CPSCAN, DIVIDE, and PMIMC were run on an Ubuntu system with an NVIDIA TITAN RTX GPU.

To evaluate the performance, three widely used clustering metrics: accuracy (ACC), normalized mutual information (NMI), and Purity are used. The higher the values of these metrics, the better the clustering performance. To mitigate the initialization sensitivity of K-means used in several methods, we repeat the experiments 10 times and report the average results.

Anchor Selection and Graph Construction Our method employs K-means to select anchors from each view and construct anchor graphs Ev using a parameterfree and effective bipartite graph construct strategy (Li et al. 2020). More details are provided in the appendix.

Performance Comparison We summarize the results across all missing ratios and report the averages, with the best and second best results marked in Table 2. We can draw the following observations:

1. Our proposed method consistently outperforms all compared methods across three metrics in most circumstances. For example, regarding the ACC metric, it achieves an average improvements of 11.65%, 18.04%, 35.61%, 14.37%, 25.16%, 8.42% over the state-of-theart across six datasets with missing ratios varying from 0.1 to 0.9. The superiority observed in the other criteria are similar, further demonstrating its outstanding performance across all datasets. 2. Data diversity may exhibit varying clustering patterns, leading to different algorithms performing differently across various datasets. For example, PIMVC achieves the promising results on the MSRCv1, CCV, and Animal datasets, while PMIMC excels on the Caltech101-7 and BDGP datasets. Additionally, RISE shows strong performance on the FMNIST dataset. In contrast, our proposed method consistently demonstrates the best performance across all datasets, indicating the effectiveness of anchor graph learning. 3. By comparing our method with various approaches that do not rely on anchors, such as UEAF and PIMVC, we observe that our proposed method not only achieves superior performance but also effectively handles largescale dataset, such as FMNIST. In addition, our method outperforms deep learning methods, highlighting its potential for practical applications.

To further evaluate the stability of our model regarding varying missing ratios, we plot the result curves across the varying missing ratios of [0.1: 0.1: 0.9]. As shown in Figure 1, this visualization allows us to observe how performance changes as the missing ratio increases. When the percentage of incomplete samples increases, most methods experience a decline in performance, while our method exhibits a more stable response. Moreover, our method shows upward trends in performance on the Caltech101-7 and BGDP datasets during certain phases as the missing ratio increases. This indicates the advantages of combining compensation subgraphs from supplementary views.

Parameter Study Our method involves four parameters that need to be adjusted appropriately, i.e., the trade-off parameters λ1 and λ2,

26574

<!-- Page 6 -->

Datasets Metrics UEAF IMVC-CBG FIMVC-VIA PIMVC CPSCAN PSIMVC-PG DIVIDE PMIMC RISE Ours AAAI’19 CVPR’22 TNNLS’22 TNNLS’23 CVPR’23 TNNLS’24 AAAI’24 TIP’25 AAAI’25

ACC 56.23 60.93 74.28 79.56 74.13 60.27 53.50 70.42 71.66 91.21 MSRCv1 NMI 45.22 51.20 62.43 69.54 65.60 50.53 42.35 61.26 58.85 86.96 Purity 57.21 61.80 74.33 80.49 75.50 61.34 55.84 72.91 75.47 91.21

ACC 37.27 59.88 48.60 66.89 54.92 48.52 35.92 47.70 70.72 88.76 Caltech101-7 NMI 27.89 43.13 44.94 54.09 56.04 42.80 37.59 59.65 53.35 82.41 Purity 77.57 81.03 80.61 86.94 86.76 80.61 76.16 87.36 80.15 92.58

ACC 44.37 36.06 41.25 30.83 39.96 40.97 33.87 50.85 44.85 86.46 BDGP NMI 21.80 14.44 16.87 8.46 15.70 18.33 11.01 28.90 19.22 83.25 Purity 45.41 37.22 41.67 31.97 40.75 43.64 35.68 51.88 61.41 86.64

ACC 14.75 16.77 12.97 20.81 17.23 16.66 18.77 16.06 17.61 35.18 CCV NMI 10.55 13.40 14.90 18.25 14.28 11.76 15.02 13.03 12.30 49.65 Purity 18.75 20.15 22.84 25.27 21.11 19.97 22.01 20.10 29.36 36.14

ACC 17.40 15.51 16.07 19.73 13.04 14.90 15.91 16.01 15.95 44.89 Animal NMI 13.94 11.25 11.31 15.62 8.68 10.65 11.56 15.16 9.77 59.05 Purity 20.83 18.90 19.47 22.21 15.52 18.34 19.24 20.08 32.14 45.80

ACC OM 22.74 20.60 OM 14.77 22.20 10.52 25.13 51.24 59.66 FMNIST NMI OM 6.01 4.04 OM 3.42 3.11 3.11 22.70 38.08 49.12 Purity OM 22.80 21.05 OM 15.78 22.20 10.58 25.23 59.51 60.62

**Table 2.** Average clustering performance of our proposed method and other compared methods on six datasets. ‘OM’ represents out of memory. The 1st/2nd best results are marked in bold and underline.

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

20

40

60

80

100

ACC (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

20

40

60

80

100

ACC (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

20

40

60

80

100

ACC (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

10

30

50

70

90

ACC (%)

UEAF IMVC-CBG FIMVC-VIA PIMVC CPSPAN PSIMVC-PG DIVIDE PMIMC RISE Ours

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

0

20

40

60

80

100

NMI (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

10

40

70

100

NMI (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

0

20

40

60

80

100

NMI (%)

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

0

20

40

60

NMI (%)

UEAF IMVC-CBG FIMVC-VIA PIMVC CPSPAN PSIMVC-PG DIVIDE PMIMC RISE Ours

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

40

60

80

100

Purity (%)

(a) MSRCv1

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

60

80

100

Purity (%)

(b) Caltech101-7

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

0

20

40

60

80

100

Purity (%)

(c) BDGP

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 Missing Ratio

10

30

50

Purity (%)

(d) CCV

UEAF IMVC-CBG FIMVC-VIA PIMVC CPSPAN PSIMVC-PG DIVIDE PMIMC RISE Ours

**Figure 1.** The ACC, NMI, and Purity curves under varying missing ratios. The curves on other datasets are similar and we omit them due to space limitations.

26575

<!-- Page 7 -->

0 0.2 0.4

1e-2

0.6

ACC

0.8

1e5

1e-1

1

1e3

61

1e1

1

62

1

1e1

1e-1 1e-3

1e2

1e-5

(a) MSRCv1 (ω = 0.1)

0 0.2 0.4

1e-2

0.6

ACC

0.8

1e5

1e-1

1

1e3

61

1e1

1

62

1

1e1

1e-1 1e-3

1e2

1e-5

(b) MSRCv1 (ω = 0.5)

**Figure 2.** Variation of ACC values with respect to λ1 and λ2 on the MSRCv1 dataset for different missing ratios.

0 0.10.20.30.40.50.60.70.80.9 1 p (! = 0.1)

0

0.5

1

ACC

Caltech101-7 MSRCv1

0 0.10.20.30.40.50.60.70.80.9 1 p (! = 0.5)

0

0.5

1

ACC

Caltech101-7 MSRCv1

**Figure 3.** Variation of ACC values with respect to coefficient p across two datasets for different missing ratios.

k 3k 5k 7k 10k 20k Anchor Num (! = 0.1)

0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1

ACC

Caltech101-7 MSRCv1 k 3k 5k 7k 10k 20k Anchor Num (! = 0.5)

0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1

ACC

Caltech101-7 MSRCv1

**Figure 4.** Variation of ACC values with respect to different anchor number on two datasets for different missing ratios.

tensor low rank coefficient p, and the number of anchors used to construct the anchor graphs Ev. We first conduct an experiment on the MSRCv1 dataset with a missing ratio of 0.1 to analyze the sensitivity of λ1 and λ2. As shown in Figure 2, we observe that our method achieves satisfactory performance across a wide range of λ1 and λ2. To illustrate the effect of missing ratio on the model’s sensitivity, we repeat the experiment with a missing ratio of 0.5. The results demonstrate that our model remains relatively stable against changes in the missing ratio.

**Figure 3.** presents the effects of the parameter p, which is tuned within p ∈{0.1: 0.1: 1}. Different values of p affect model performance, with appropriate settings leading to better results. The performance fluctuations are slight across varying missing ratios, demonstrating the model’s stability.

**Figure 4.** demonstrates the impact of the number of anchors. We observe that it is feasible to use a small amount of anchors to achieve promising performance with only slight adjustments, regardless of the missing ratio.

ACC Miss Ratios

Models 0.3 0.5 0.7

AGLF w/o CSL 61.43 (↓33.33) 53.33 (↓39.53) 50.00 (↓37.62) AGLF w/o TS 90.47(↓4.29) 84.28 (↓8.58) 80.95(↓6.67) AGLF 94.76 92.86 87.62

**Table 3.** Ablation study on the MSRCv1 dataset.

0 10 20 Iterations

0.2

0.4

0.6

0.8

Metric

0

1

2

Residual

ACC NMI Purity Residual

(a) Caltech01-7

0 10 20 Iterations

0.2

0.4

0.6

0.8

Metric

0

1

Residual

ACC NMI Purity Residual

(b) MSRCv1

**Figure 5.** Convergence curves of AGLF on two datasets.

Ablation Study

The compensation subgraph learning is a primary contribution of our model, and the tensor Schatten p-norm is also a key constraint. To assess the effect of these two techniques, we devise two degraded models: “AGLF w/o CSL”, which indicates the removal of compensation subgraph learning, and “AGLF w/o TS”, which represents substituting the tensor Schatten p-norm with F-norm. The performance comparison is shown in Table 3. We observe that AGLF consistently outperforms the degraded models across varying missing ratios. This indicates these components are essential and effective for our model.

Convergence Study

The proposed algorithm optimizes the objective function iteratively by introducing an auxiliary variable J. Convergence of our algorithm is determined by checking the difference between J = F. As shown in Figure 5, The difference decreases to nearly zero in fewer than 20 iterations, while three metrics stabilize at high values, demonstrating the effectiveness and practicability of our optimization algorithm.

## Conclusion

This paper focuses on exploring cross-view information compensation for incomplete multi-view data, further investigating the complementary information among views. The proposed Cross-view Anchor Graph Learning and Factorization (AGLF) method achieves cross-view structural imputation based on supplementary view data and directly derives soft clustering indicators without the need for postprocessing. To solve the proposed objective function, we devise an optimization algorithm based on the Augmented Lagrange Multiplier. Extensive experiments across six datasets demonstrate the effectiveness of our method.

26576

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by the Scientific Foundation for Youth Scholars of Shenzhen University (File no. 868-000001033519), by the Guangdong-Macao Science and Technology Innovation Joint Fundation under Grant 2024A0505090003, by the Guangdong Provincial Key Laboratory under Grant 2023B1212060076, and by the Science and Technology Development Fund, Macau SAR (File no. 0050/2024/AGJ, 0049/2022/A1).

## References

Chen, Y.; Zhao, X.; Zhang, Z.; Liu, Y.; Su, J.; and Zhou, Y. 2023. Tensor learning meets dynamic anchor learning: From complete to incomplete multiview clustering. IEEE Transactions on Neural Networks and Learning Systems, 35(11): 15332–15345. Cui, J.; Fu, Y.; Huang, C.; and Wen, J. 2022. Low-rank graph completion-based incomplete multiview clustering. IEEE Transactions on Neural Networks and Learning Systems, 35(6): 8064–8074. Deng, S.; Wen, J.; Liu, C.; Yan, K.; Xu, G.; and Xu, Y. 2023. Projective incomplete multi-view clustering. IEEE Transactions on Neural Networks and Learning Systems, 35(8): 10539–10551. Gao, Q.; Zhang, P.; Xia, W.; Xie, D.; Gao, X.; and Tao, D. 2021. Enhanced tensor RPCA and its application. IEEE transactions on pattern analysis and machine intelligence, 43(6): 2133–2140. Hu, S.; Shi, Z.; and Ye, Y. 2022. DMIB: Dual-Correlated Multivariate Information Bottleneck for Multiview Clustering. IEEE Trans. Cybern., 52(6): 4260–4274. Jin, J.; Wang, S.; Dong, Z.; Liu, X.; and Zhu, E. 2023. Deep incomplete multi-view clustering with cross-view partial sample and prototype alignment. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 11600–11609. Kilmer, M. E.; and Martin, C. D. 2011. Factorization strategies for third-order tensors. Linear Algebra and its Applications, 435(3): 641–658. Li, J.; Gao, Q.; Wang, Q.; and Xia, W. 2024a. Tensorized label learning on anchor graph. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 13537– 13544. Li, M.; Wang, S.; Liu, X.; and Liu, S. 2024b. Parameter-free and scalable incomplete multiview clustering with prototype graph. IEEE Transactions on Neural Networks and Learning Systems, 35(1): 300–310. Li, X.; Pan, Y. P.; Sun, Y.; Sun, Q.; Sun, Y.; W. Tsang, I.; and Ren, Z. 2025. Incomplete Multi-view Clustering with Paired and Balanced Dynamic Anchor Learning. IEEE Transactions on Multimedia, 27: 1486–1497. Li, X.; Pan, Y. P.; Sun, Y.; Sun, Q. S.; Tsang, I. W.; and Ren, Z. 2024c. Fast Unpaired Multi-view Clustering. 4488–4496. Li, X.; Sun, Y.; Sun, Q.; and Ren, Z. 2022a. Consensus cluster center guided latent multi-kernel clustering. IEEE Transactions on Circuits and Systems for Video Technology, 33(6): 2864–2876.

Li, X.; Sun, Y.; Sun, Q.; Ren, Z.; and Sun, Y. 2023. Cross-view graph matching guided anchor alignment for incomplete multi-view clustering. Information Fusion, 100: 101941. Li, X.; Zhang, H.; Wang, R.; and Nie, F. 2020. Multiview clustering: A scalable and parameter-free bipartite graph fusion method. IEEE transactions on pattern analysis and machine intelligence, 44(1): 330–344. Li, X.-L.; Chen, M.-S.; Wang, C.-D.; and Lai, J.-H. 2022b. Refining graph structure for incomplete multi-view clustering. IEEE transactions on neural networks and learning systems, 35(2): 2300–2313. Lin, Y.; Gou, Y.; Liu, Z.; Li, B.; Lv, J.; and Peng, X. 2021. Completer: Incomplete multi-view clustering via contrastive prediction. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 11174–11183. Liu, C.; Wen, J.; Wu, Z.; Luo, X.; Huang, C.; and Xu, Y. 2023. Information recovery-driven deep incomplete multiview clustering network. IEEE Transactions on Neural Networks and Learning Systems, 35(11): 15442–15452. Liu, S.; Liang, K.; Dong, Z.; Wang, S.; Yang, X.; Zhou, S.; Zhu, E.; and Liu, X. 2024. Learn from view correlation: An anchor enhancement strategy for multi-view clustering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 26151–26161. Liu, S.; Liu, X.; Wang, S.; Niu, X.; and Zhu, E. 2022. Fast incomplete multi-view clustering with view-independent anchors. IEEE Transactions on Neural Networks and Learning Systems, 35(6): 7740–7751. Liu, X.; Zhu, X.; Li, M.; Tang, C.; Zhu, E.; Yin, J.; and Gao, W. 2019. Efficient and effective incomplete multi-view clustering. In Proceedings of the AAAI conference on artificial intelligence, volume 33, 4392–4399. Lu, Y.; Lin, Y.; Yang, M.; Peng, D.; Hu, P.; and Peng, X. 2024. Decoupled contrastive multi-view clustering with high-order random walks. In Proceedings of the AAAI conference on artificial intelligence, volume 38, 14193–14201. Qin, Y.; Feng, G.; and Zhang, X. 2025. Scalable One- Pass Incomplete Multi-View Clustering by Aligning Anchors. Proceedings of the AAAI Conference on Artificial Intelligence, 39(19): 20042–20050. Qin, Y.; and Qian, L. 2024. Fast Elastic-Net Multi-view Clustering: A Geometric Interpretation Perspective. In Proceedings of the 32nd ACM International Conference on Multimedia, 10164–10172. Qin, Y.; Zhang, X.; Yu, S.; and Feng, G. 2025. A survey on representation learning for multi-view data. Neural Networks, 181: 106842. Rudin, W. 1976. Principles of mathematical analysis. 3rd ed. Wang, J.; Chen, Y.; Wang, Z.; and Zhao, W. 2021. Popularity-enhanced news recommendation with multi-view interest representation. In Proceedings of the 30th ACM international conference on information & knowledge management, 1949–1958.

26577

<!-- Page 9 -->

Wang, S.; Liu, X.; Liu, L.; Tu, W.; Zhu, X.; Liu, J.; Zhou, S.; and Zhu, E. 2022. Highly-efficient incomplete largescale multi-view clustering with consensus bipartite graph. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 9776–9785.

Wang, X.; Zhang, Y.; Zhang, J.; and Zhou, Y. 2025. Incomplete Multiview Clustering using Discriminative Feature Recovery and Tensorized Matrix Factorization. IEEE Transactions on Circuits and Systems for Video Technology, 35: 10716–10727.

Wang, X.; Zhang, Y.; and Zhou, Y. 2025a. Bidirectional Probabilistic Multi-graph Learning and Decomposition for Multi-view Clustering. IEEE Transactions on Image Processing, 34: 3609–3621.

Wang, X.; Zhang, Y.; and Zhou, Y. 2025b. Highly efficient rotation-invariant spectral embedding for scalable incomplete multi-view clustering. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 21312– 21320.

Wang, X.; Zhang, Y.; and Zhou, Y. 2025c. Multimodal Remote Sensing Image Clustering with Multi-scale Spectral- Spatial Anchor Graphs. IEEE Transactions on Geoscience and Remote Sensing, 63: 1–12.

Wang, X.; Zhang, Y.; and Zhou, Y. 2025d. Pseudo- Supervision Affinity Propagation for Efficient and Scalable Multiview Clustering. IEEE Transactions on Neural Networks and Learning Systems, 36: 15282–15293.

Wen, J.; Liu, C.; Xu, G.; Wu, Z.; Huang, C.; Fei, L.; and Xu, Y. 2023a. Highly confident local structure based consensus graph learning for incomplete multi-view clustering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 15712–15721.

Wen, J.; Xu, G.; Tang, Z.; Wang, W.; Fei, L.; and Xu, Y. 2023b. Graph regularized and feature aware matrix factorization for robust incomplete multi-view clustering. IEEE Transactions on Circuits and Systems for Video Technology, 34(5): 3728–3741.

Wen, J.; Yan, K.; Zhang, Z.; Xu, Y.; Wang, J.; Fei, L.; and Zhang, B. 2020a. Adaptive graph completion based incomplete multi-view clustering. IEEE Transactions on Multimedia, 23: 2493–2504.

Wen, J.; Zhang, Z.; Xu, Y.; Zhang, B.; Fei, L.; and Liu, H. 2019. Unified embedding alignment with missing views inferring for incomplete multi-view clustering. In Proceedings of the AAAI conference on artificial intelligence, volume 33, 5393–5400.

Wen, J.; Zhang, Z.; Zhang, Z.; Fei, L.; and Wang, M. 2020b. Generalized incomplete multiview clustering with flexible locality structure diffusion. IEEE transactions on cybernetics, 51(1): 101–114.

Wen, J.; Zhang, Z.; Zhang, Z.; Zhu, L.; Fei, L.; Zhang, B.; and Xu, Y. 2021. Unified tensor framework for incomplete multi-view clustering and missing-view inferring. In Proceedings of the AAAI conference on artificial intelligence, 10273–10281.

Xia, W.; Gao, Q.; Wang, Q.; and Gao, X. 2022. Tensor completion-based incomplete multiview clustering. IEEE Transactions on Cybernetics, 52(12): 13635–13644. Yuan, H.; Sun, Y.; Zhou, F.; Wen, J.; Yuan, S.; You, X.; and Ren, Z. 2025. Prototype matching learning for incomplete multi-view clustering. IEEE Transactions on Image Processing, 34: 828–841. Zhang, Y.; Wang, S.; Liu, J.; Yu, S.; Dong, Z.; Liu, S.; Liu, X.; and Zhu, E. 2025a. DLEFT-MKC: Dynamic Late Fusion Multiple Kernel Clustering with Robust Tensor Learning via Min-Max Optimization. In The Thirteenth International Conference on Learning Representations. Zhang, Y.; Wang, X.; Jiang, X.; Zhang, L.; and Du, B. 2025b. Elastic Graph Fusion Subspace Clustering for Large Hyperspectral Image. IEEE Transactions on Circuits and Systems for Video Technology, 35: 6300–6312. Zhang, Y.; Yan, S.; Zhang, L.; and Du, B. 2024. Fast projected fuzzy clustering with anchor guidance for multimodal remote sensing imagery. IEEE Transactions on Image Processing, 33: 4640–4653.

26578
