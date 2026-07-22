---
title: "Federated Incomplete Multi-View Clustering with Tensorized Low-Rank Constraint"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39251
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39251/43212
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Federated Incomplete Multi-View Clustering with Tensorized Low-Rank Constraint

<!-- Page 1 -->

Federated Incomplete Multi-View Clustering with Tensorized Low-Rank

Constraint

Wei Feng1, Danting Liu2, Qianqian Wang3, Mengping Jiang3, Bin Liu1*

1College of Information Engineering, Northwest A&F University 2School of Computer Science and Technology, Xi’an Jiaotong University 3School of Telecommunication Engineerings, Xidian University wei.feng@nwafu.edu.cn, 2196123604@stu.xjtu.edu.cn, qqwang@xidian.edu.cn, mpjiang@foxmail.com, liubin0929@nwsuaf.edu.cn

## Abstract

Federated Multi-View Clustering has gained increasing attention for its ability to discover complementary clustering structures of distributed multi-view data while preserving data privacy. However, real-world clients often only have access to partial views, and the view incompleteness poses great challenges to federated multi-view feature fusion to exploit consistent and complementary information. Moreover, efficiency is highly expected in federated scenarios due to the limited resources of each client. To alleviate these issues, we propose Federated Incomplete Multi-View Clustering with Tensorized Low-Rank Constraint (FIMVC-TLRC), which incorporates anchors to improve efficiency and is able to address prevalent view incompleteness issue in federated scenarios. FIMVC-TLRC aligns the local anchor graphs and employs a tensorized low-rank constraint based on the tensor Schatten p-norm to enforce the consistency of the data representations learned by each client. Besides, a federated optimization framework is developed to jointly optimize the construction and alignment of anchor graphs, thus enabling collaborative and privacy-preserving training. Experimental results on multiple datasets demonstrate its effectiveness.

## Introduction

Multi-view clustering (MVC) has emerged as an effective unsupervised method for handling multi-view data since it fully exploits the complementary and consistent information between views (Fang et al. 2023; Liu et al. 2024). Existing MVC methods can be broadly classified into deep MVC (Cui et al. 2024; Wen et al. 2023) and heuristic MVC (Wan et al. 2023), and both of them achieve impressive performance in clustering. Compared with deep MVC methods, heuristic methods achieve advantages in interoperability and hence still receive increasing attention. Despite the numerous heuristic MVC approaches developed, most of them assume that the multi-view data is located in a single party, ignoring the real-world multi-view data is likely to be collected and maintained by different entities. In this case, the data holders may not be willing to share data with others for privacy concerns, and thus the data isolation leads to a great challenge in the deployment of MVC algorithms.

*Corresponding Author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Federated learning (Li et al. 2020; Zhang et al. 2021; Meng et al. 2024), which allows different entities to collaboratively train a global model without privacy leakage, has emerged as a possible solution to the above challenge. In particular, vertical federated learning (VFL) (Huang et al. 2022a) focuses on the scenario where different clients share the same sample space but different feature spaces, which is well-suited for distributed multi-view data processing by considering each view to be a subset of features. However, MVC requires the exploitation of consistent and complementary information embedded in different views, which is rarely explored by existing VFL works. As a result, VFL generally cannot obtain satisfactory performance on multiview data.

To address this issue, several federated MVC (Fed- MVC) algorithms have been proposed. For example, Chen et al. (2023) proposed a self-supervised deep FedMVC method to learn consistent clustering assignments; Huang et al. (2022b) developed a non-negative matrix factorization (NMF) based FedMVC method. Despite the outstanding performance of these methods, their effectiveness hinges on the completeness of data across all views, while incomplete multi-view data is ubiquitous in practical scenarios due to issues like sensor failure and transmission noises. Although incomplete multi-view clustering (IMVC) has been widely studied in centralized settings, only a few works explore it in federated scenarios. Ren et al. (2024) proposed a deep Federated IMVC (FedIMVC) method with collaborative missing view imputation and cluster alignment. Nevertheless, heuristic FedIMVC methods still remain underexplored, despite their inherent advantages of simplicity and interpretability.

Currently, heuristic FedIMVC confronts several challenges. First, heuristic methods might produce high computational complexity when handling high-dimensional data. Moreover, in centralized settings, the missing views can be imputed with the data from other views, while in federated scenarios, the data isolation and privacy requirements hinder the information exchange between different views. As a result, the features for clustering results learned by different clients suffer from an inconsistency issue, resulting in unsatisfactory clustering performance. How to fuse local clustering outcomes from different clients into a unified global result and meanwhile keep data security is an important chal-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

21083

<!-- Page 2 -->

lenge to be solved.

To overcome these challenges, we propose a novel heuristic FedIMVC method named Federated Incomplete Multi- View Clustering with Tensorized Low-Rank Constraint (FIMVC-TLRC), which incorporates anchor graph for clustering to improve its efficiency and scalability when handling high-dimensional data. To tackle the inconsistency problem due to local training, FIMVC-TLRC first aligns locally learned graphs with the global guidance matrix produced by the server-side model, which incorporates tensor Schatten p-norm to refine locally learned data representations from different clients, thereby efficiently exploring the consistent information between views. Finally, we design a federated optimization algorithm to optimize the model without exchanging any raw data. The main contributions are as follows:

• We propose a novel and efficient FedIMVC method based on anchor graph, i.e., FIMVC-TLRC, which aligns the local graphs and introduces a tensor Schatten p-norm for local multi-view representation refinement to explore the consistent information in each view. • We develop a federated optimization framework to support joint training of the construction and alignment of anchor graphs as well as clustering model. • We conduct extensive experiments to demonstrate the effectiveness and superiority of our method.

## Related Work

Federated Multi-view Clustering

Federated learning is a distributed machine learning framework designed to train a unified model by coordinating the training process on local data across multiple clients while maintaining data privacy for each client (Qi et al. 2025a,b). It can be broadly classified into Horizontal Federated Learning (HFL) and Vertical Federated Learning (VFL). Federated learning has quickly expanded its applications into the multi-view learning domain. In the context of FedMVC, Chen et al. (2023) developed a federated deep multi-view clustering method with global selfsupervision. Huang et al. (2022b) constructed a federated multi-view clustering method using Non-negative Matrix Factorization (NMF) and K-means, which effectively reduces computational costs. Despite their effectiveness, these FedMVC methods all assume complete views and are not suitable for FedIMVC. Recently, Ren et al. (2024) proposed a FedIMVC method based on deep autoencoders to learn local features and perform adaptive imputation globally, which utilizes deep models and incurs high computational costs, making it unsuitable for scenarios with stringent efficiency requirements.

Incomplete Multi-View Clustering

Existing incomplete multi-view clustering (IMVC) methods can be categorized into four types (Wen et al. 2022): deep learning-based IMVC (Xu et al. 2022), matrix factorizationbased IMVC (Jia et al. 2021), kernel learning-based

IMVC (Wu, Feng, and Yuan 2024), and graph learningbased IMVC (Fu et al. 2024). Deep learning-based methods leverage neural networks to capture complex patterns and relationships within the data. Among the latter three methods, graph methods excel at exploring intrinsic geometric structures and exhibit impressive performance on linearly nonseparable data. However, these methods are all designed for centralized scenarios, and how to deploy graph-based IMVC under federated settings efficiently remains underexplored.

Proposed Method Problem Statement Problem Definition: In the federated scenario, we consider a system consisting of a central server S and M clients {C1, · · ·, CM}, where incomplete multi-view data X = {X1, X2,..., XM} is distributed across these clients. The incomplete local data held by Cm is denoted as Xm ∈Rdm×n, where dm denotes the feature dimension of the m-th client and n denotes the sample number, but only nm samples are available. Our proposed method leverages local computations at each client and coordinates these with the server to obtain a unified global clustering outcome. This approach ensures that sensitive data remains on the clients while achieving effective clustering across distributed datasets.

Security Model and Design Goals: FedMVC aims to empower all clients to collaboratively train a multi-view clustering model without leaking any personal information. In this work, we adopt the semi-honest adversary model, where all clients and the server are curious about others’ private information but strictly follow the predefined protocol to behave honestly. However, they may attempt to infer others’ private data from the information they have obtained during the protocol execution. Our underlying model adopts an anchor-based method and further performs feature extraction on this basis, thereby avoiding the exchange of raw data. Therefore, we have the following goals:

• Security Goal: Neither of the server and clients could obtain the raw data, which is sensitive to the data privacy. • Availability Goal: The proposed FedIMVC method should be able to effectively partition the distributed incomplete multi-view data into disjoint clusters in a collaborative manner. The clustering performance should be comparable to the centralized MVC models.

Objectives FIMVC-TLRC is composed of four procedures: Initialization, Local Training, Global Training, and Aggregation. Specifically, the Initialization procedure initializes the necessary parameters on each client and server; the Local Training and Global Training respectively train the local models {f m(·)}(1 ≤m ≤M) on the client Cm and a global model fg(·) for consistency assurance on the server S. Aggregation is used to produce the final clustering result. In what follows, we introduce the local and global objectives in detail.

Objective for Local Training: For each client Cm, it trains a local clustering model Fm ←f (m)(ˆF m, Xm) on

21084

<!-- Page 3 -->

their local data Xm ∈Rdm×n, where Fm represents the learned local high-level representations, and ˆF m represents guidance matrix output by the global model fg(·) from S for Cm; f (m)

g (·) refers to taking the m-th component of fg(·)’s output. To efficiently exploit the complementary information of multi-view data, each client first constructs a local anchor graph and then utilizes a structural alignment module to align the anchors.

Local Anchor Graph Construction: Traditional graphbased IMVC methods generally require constructing a graph from all samples, resulting in computational complexity of O(n3) and space complexity of O(n2), which limits their scalability. For better efficiency, our clustering method is built on anchor graph, which establishes relationships between a small number of representative anchors and the samples. For each client Cm, it can build its anchor graph with local data by optimizing the following objective:

min Gm,Am,αm α2 m∥XmWm −AmGmWm∥2

F + β∥Gm∥2

F s.t. Am⊤Am = I, Gm ≥0, Gm⊤1 = 1

(1) where Am ∈Rdm×σ denotes the anchor matrix from the m-th view by Cm, σ is the anchor number; Wm ∈Rn×n is the diagonal indicator matrix, and Wm ii = 0 means the i-th sample of the m-th view is missing; Gm ∈Rσ×n is the view-specific anchor graph; GmWm can be considered as the similarities between σ anchors and nm available instances; αm and β are parameters to balance the influence of each term, and PM m=1 αm = 1. We enforce the orthogonality of Am to enhance discriminability, i.e., Am⊤Am = Im.

Local Anchor Alignment: The local anchors and anchor graphs are selected independently by each client, which leads to two problems, i.e.,(1) anchor alignment: the anchors selected by each client does not correspond to those selected by other clients; and (2) inconsistency issue: the learned anchor graphs do not characterize the consistent features of each sample, degrading the final clustering performance. To address these issues, we employ the server to refine the anchor graphs to be consistent based on tensor learning, rather than enforce a single and consistent anchor graph to be learned. The refined anchor graphs are distributed to each client as guidance to instruct local anchor graph learning. Then, we leverage a permutation matrix Hm to structurally align the local anchor graph Gm the guidance matrix from the server, resulting in view-specific representations Fm:

min αm,Am,Gm,Hm,Fm α2 m∥XmWm −AmGmWm∥2

F

+ β∥Gm∥2

F + γ∥HmGm −Fm∥2

F s.t. Am⊤Am = I, Hm⊤Hm = I, Gm ≥0,

Gm⊤1 = 1, FmFm⊤= I, Fm = f m g ({Fm})

(2)

where γ is the trade-off parameter to balance the influence between anchor graph construction and the alignment module; The core idea is to enforce the local learned high-level representation Fm to be similar to the refined representation learned by fg(·). It should be noted that the guidance matrix is dynamic rather than constant during training rounds.

Objective for Global Training: The goal of the global training is to refine local high-level representation {Fm}(1 ≤m ≤M) via tensor learning to exploit the consistent and complementary information. Denote the refined representation for each view as ˆFm, and ˆ F is a tensor constructed by stacking all the ˆFm, we refine the local representations by minimizing the tensor low-rank objective of based on tensor Schatten-p norm and simultaneously enforcing the refined representation to be similar to the outputs of local models {f (m)(·)} via a constraint. Following this line, the global objective to be optimized is as follows min

ˆ F λ∥ˆ F∥p

Sp s.t. ˆF m = f (m)(ˆFm, Xm)(1 ≤m ≤M) (3)

where ∥· ∥p

Sp represents the tensor Schatten-p norm. Then, f m g (·) returns ˆF mthe guidance for Cm by taking the m-th frontal slice of ˆ F; λ is a hyper-parameter to balance the influence of the global training.

Federated Optimization

The optimization of local objectives and global objective requires the interaction between S and Cm by sharing the model output with each other. We adopt the Alternative Iteration Method for optimization, and in this case, the collaborative optimization of the local and global objectives is equivalent to optimizing the following objective:

min

M X m=1 α2 m∥XmWm −AmGmWm∥2

F + β∥Gm∥2

F

| {z } Local Anchor Graph Construction

+ γ

M X m=1

∥HmGm −Fm∥2

F | {z } Local Anchor Alignment

+ λ∥F∥p

Sp | {z } Global Training Objective s.t.α⊤1 = 1, Am⊤Am = I, Hm⊤Hm = I,

Gm ≥0, Gm⊤1 = 1, FmFm⊤= I

(4) where F is a tensor by stacking all Fms.

In our federated framework, the influence of S and Cm on each other is achieved with the constraint Fm = f m(Xm) and ˆF m = f m g ({Fm}), which enforces the local representations to be similar to be the globally refined representation. Since multi-view data is distributed across multiple clients, and for the sake of privacy, sensitive data should not be shared, which brings a great challenge for optimization. However, the high-level representation Fm learned based on local anchor graph projection does not lead to data leakage and can be transmitted between the server and clients. Based on these analyses, we illustrate our federated optimization framework as follows.

System Initialization: The server and all the clients negotiate the consistent public parameters. Each client initializes Hm and Fm as identity matrices and sets αm to 1/M, while the server initializes ˆF as empty tensors.

21085

<!-- Page 4 -->

Local Training: Suppose the guidance matrix output by the global model f m g ({Fm}) is ˆFm, and by introducing Augmented Lagrange Multiplier (ALM) method, the objective optimized by Cm is transformed to:

min αm,Am,Gm,Hm,Fmα2 m∥XmWm −AmGmWm∥2

F

+β

M X m=1

∥Gm∥2

F + γ∥HmGm −Fm∥2

F

+ρ

2∥Fm −ˆF m + Bm ρ ∥2

F

(5)

where Bm is the Lagrange multiplier, ρ is penalty parameter. By performing Alternative Iteration Method on it, the local training can be divided into the following subproblems.

(1). Update Am: Removing the irrelevant terms, the local objective becomes:

min Am⊤Am=I α2 m∥XmWm −AmGmWm∥2

F (6)

Rewrite the objective with traces and remove the irrelevant terms, Eq.(6) becomes:

max Am⊤Am=I Tr

Am⊤Qm

(7)

where Qm = XmWmWm⊤Gm⊤. The optimal solution of Am can be obtained by computing Fm∗= UmVm⊤, where Um and Vm are the left and right singular matrices obtained by performing SVD decomposition on Qm.

(2). Update Gm:

min Gm≥0,Gm⊤1=1α2 m∥XmWm −AmGmWm∥2

F

+β∥Gm∥2

F + γ∥HmGm −Fm∥2

F

(8)

To fully leverage global information to guide the update of local anchor graphs, we use the consistency high-level representation F = 1 M

PM m=1 Fm aggregated by the server to replace the local representation Fm in this step. Then, after a simple algebraic derivation, the optimization of Eq.(8) can be formulated as:

min Gm≥0,Gm⊤1=1 Tr

Gm⊤Gm α2 mWmWm⊤+ (β + γ)I

−2Tr

Gm⊤ α2 mAm⊤XmWmWm⊤+ γHm⊤F

(9) Since W is a diagonal matrix, it is easy to obtain that α2 mWmWm⊤+ (β + γ)I is a diagonal matrix and all the diagonal elements are non-zero. Denote α2 mWmWm⊤+ (β + γ)I and α2 mAm⊤XmWmWm⊤+ γHm⊤F as Qm

1 and Qm

2, Eq. (9) is transformed to:

min Gm≥0,Gm⊤1=1 Tr(1

2Gm⊤Gm −Gm⊤Qm 2 (Qm 1)−1) (10)

Introducing the Lagrange multiplier to Eq. (10), we get:

L

G(m), ν, Λ

= Tr(1

2Gm⊤Gm −Gm⊤Qm 2 (Qm 1)−1)

−νT Gm⊤1 −Tr(ΛT Gm)

(11)

where ν and Λ are Lagrange multipliers. Given the derivation of L(Gm, ν, Λ) with regard to Gm: Gm − Qm

2 (Qm 1)−1 −ν1 −Λ, the solution is given according to the Karush-Kuhn-Tucker (KKT) condition as follows:

 



Gm −Qm

2 (Qm)−1 −ν1 −Λ = 0 Gm⊤1 = 1 Λ⊤Gm = 0

(12)

Using Newton method to optimize ν, the solution is:

Gm = max(Qm

2 (Qm 1)−1 −ν1, 0) (13) (3). Update Hm: The objective can be written as:

min Hm⊤Hm=I γ∥HmGm −Fm∥2

F

⇔ max Hm⊤Hm=I Tr

Hm⊤FmGm⊤ (14)

Similar to optimizing Gm, we replace Fm with F, and Hm can be optimized by SVD decomposition on FGm⊤.

(4). Update αm: We only focus on the term related to αm:

min α⊤1=1 α2 m∥XmWm −AmGmWm∥2

F (15)

Let τm = ∥XmWm −AmGmWm∥2

F, we apply the Cauchy-Schwarz inequality as:

M X m=1 α2 mτm

! M X m=1

1 τm

!

≥

M X m=1 αm

!2

(16)

The equality holds when αm = k/τm, where k is a constant. Based on the constraint α⊤1 = 1, we can solve for k as k = PM m=1 1/τm. Finally, the optimal αm is given by:

αm = 1/τm PM m=1 1/τm

(17)

Step 5. Update Fm:

min FmFm⊤=I γ∥HmGm −Fm∥2

F + ρ

2∥Fm −ˆF m + Bm ρ ∥2

F

(18) where Bm is Lagrange multiplier and is updated by Bm = Bm + ρ(Fm −ˆFm). Eq. (18) can be transformed into:

max

Fm (γHmGm + ρ

2(ˆFm −Bm ρ))Fm⊤ s.t., FmFm⊤= I

(19)

We solve the optimal Fm by performing SVD on γHmGm + ρ

2(ˆFm −Bm ρ). The optimal Fm is sent to S for refinement.

Global Training: The only variable to be updated by S is ˆ F. By performing ALM, the global objective function w.r.t

ˆ F becomes:

min

ˆ F γ∥ˆ F∥p

Sp + ρ

2∥F −ˆ F + B ρ ∥2

F (20)

where B is Lagrange multiplier and is updated by B = B + ρ(F −ˆF), ρ is the penalty parameter. The solution is

ˆ F

∗= ifft

U ∗D γ ρ,p(P) ∗VT

(21)

where P = F +

ˆF ρ, and U and V are acquired via t-SVD of P, i.e., P = U ∗S ∗VT.

21086

<!-- Page 5 -->

## Algorithm

1: FIMVC-TLRC Input: Incomplete data X = {X1,..., XM}; Missing indicator matrix Wm; cluster number K.

1: Each client Cm initializes Wm, Hm and αm; 2: while not converged do 3: for m = 1 to M do 4: ▷On m-th client Cm 5: Update weight αm according to Eq. (17) 6: Update Am, Gm, Fm, Hm

7: Compute τm 8: Send Fm and 1/τm to the global server 9: end for 10: ▷On the Server S 11: Update ˆF 12: Aggregate Fm into F 13: Send ˆFm and F to Cm 14: Compute PM m=1 1/τm and send it to all clients 15: end while 16: Obtain U by performing SVD on F Output: Perform k-means on U to obtain labels

Aggregation: After the model converges, S computes F = 1 M

PM m=1 Fm and then performs SVD on F to learn U and applies k-means on U to obtain the clustering result.

Workflow FIMVC-TLRC requires the transmission of certain parameters to support the training of collaborative and privacypreserving models. To better illustrate the working procedures of FIMVC-TLRC, we briefly introduce its workflow here. Firstly, each client Cm conducts initialization by setting Gm as zero matrix and Hm and Fm as identity matrix, and setting αm with 1/M. After initialization, Cm updates Am, Gm, Hm, Fm, and calculates τm. Then, each client sends τm and Fm to the server S. The server S, after receiving all the parameters, stacks all the Fm into a tensor F, updates ˆF according to Eq.(21), and updates W. Subsequently, S will also calculate PM m=1

1 τm and global con- sistent representation F = hPM m=1

Fm

M i

, send them to all clients, and send the updated ˆF m to Cm, where client Cm can update αm using Eq.(17). This process is repeated until the model converges. Finally, the server aggregates the representations into a unified one and obtain the final clustering results. We summarize the algorithm in Algorithm 1.

Complexity Analysis Computational Complexity: (1) Local client-side: Each client’s computational load includes updating Am, Gm, Fm, Hm, and αm. In each local iteration, the computational complexity of updating Am, Fm, and Hmprimarily stems from SVD decomposition, with approximate complexities of O(nσdm + σ2dm),O(nσ2M), and O(nσ2M + M 3σ). The time complexity for updating Gm and αm is dominated by matrix multiplication, with a computational cost of O(nσdm). Therefore, the total computational complex- ity of the client is O(n(σdm + σ2M) + σ3M + σ2dm). (2) Global server-side: The server needs to update ˆF and W, where the primary computational cost arises from the DFT and SVD operations, and the computational complexity is O(Mnσ log(Mn) + M 2nσ).

Communication Complexity: Furthermore, we analyze the transmission load between each client and the global server. Local Client →Global Server: Each client transmits its local Fm to the global server before aggregation. For all clients, the amount of data transmitted in each communication round is O(nσM). Global Server →Local Client: The global server sends the m-th slice of ˆF to the m-th client along with the computed PM m=1 1/τm after aggregation. Thus, the total amount of data transmitted in each communication round is O(nσM).

## Experiment

Datasets: We evaluate our method on eight public multiview datasets: (1)Yale; (2)WebKB (Blum and Mitchell 1998); (3) BDGP (Cai et al. 2012); (4)Caltech101-7 (Fei- Fei, Fergus, and Perona 2004); (5)NGs (Hussain, Bisson, and Grimal 2010); (6)Sonar (Sejnowski and Gorman 1988); (7)SentencesNYU v2(RGB-D) (Silberman et al. 2012); (8)CiteSeer (Apt´e, Damerau, and Weiss 1994). Following (Li et al. 2022), we randomly remove samples from each view for incomplete data. For the federated setting, our experiments include a server and multiple clients, each holding a view of the data.

Compared Methods: We compared our methods with nine clustering methods: (1) BSV (Zhao, Liu, and Fu 2016); (2)Concat (Zhao, Liu, and Fu 2016); (3)DAIMC (Hu and Chen 2019); (4)PIC (Wang et al. 2019); (5)IMVC AGL (Wen, Xu, and Liu 2018); (6)IMVC- CBG (Wang et al. 2022); (7)VKMC (Huang et al. 2022a); (8)FedMVL (Huang et al. 2022b); (9)TensorFMVC (Feng et al. 2024). where (1)-(6) are centralized multi-view methods, (7)-(9) are federated multi-view methods.

Experimental Results Figure 1, Table 1, and Table 2 present the clustering results on eight multi-view datasets. The following points are easy to observe: (1) Compared with existing centralized IMVC methods, FIMVC-TLRC demonstrates superior performance across most datasets. For example, on the Yale dataset, our method outperforms the second-best method in terms of ACC, NMI, and PUR by 11.54%, 11.87%, and 11.87%, respectively. Additionally, as shown in Figure 1, the clustering performance of FIMVC-TLRC consistently surpasses that of other methods, demonstrating the effectiveness of Local Anchor Construction and Tensorial Representation Fusion; (2) Compared to the existing vertical federated method VKMC, both approaches meet the requirements for data privacy protection. However, our method significantly outperforms VKMC in overall performance, as it fully explores the consistency structure between views through a tensor regularization term and can be applied to incomplete data; (3) In contrast to FedMVL, our approach is

21087

<!-- Page 6 -->

**Figure 1.** Clustering performance of FIMVC-TLRC on eight multi-view datasets with different missing rates.

Datasets Yale WebKB BDGP Caltech101-7

Metrics ACC NMI PUR ACC NMI PUR ACC NMI PUR ACC NMI PUR

BSV 34.41 35.62 36.30 82.89 16.43 82.93 33.07 9.23 33.41 55.10 36.98 75.90 Concat 24.78 29.56 28.22 79.16 13.80 81.69 33.80 9.12 34.03 46.42 35.31 77.94 DAIMC 39.12 44.73 41.62 83.05 31.30 86.29 36.83 11.83 37.16 43.99 39.74 83.14 PIC 47.13 50.99 48.30 71.38 7.37 80.42 20.04 0.16 20.16 64.63 51.57 85.89 IMSC AGL 46.73 50.29 48.01 72.93 6.66 78.80 37.31 12.89 38.65 52.30 42.59 83.78 IMVC-CBG 46.65 52.84 48.94 88.89 45.85 83.43 40.29 17.84 40.86 60.20 43.75 81.06 VKMC 20.54 24.99 21.42 64.56 2.69 78.12 24.64 1.82 25.67 36.39 3.58 57.65 FedMVL 18.02 16.31 19.47 66.36 17.45 68.55 27.70 5.05 33.65 16.78 7.98 22.54 TensorFMVC 44.24 51.75 46.06 58.94 3.53 78.11 44.24 19.38 46.06 58.62 5.29 58.94 FIMVC-TLRC 58.67 64.71 60.81 96.05 70.04 96.05 51.41 22.12 51.43 64.41 49.65 84.14

**Table 1.** Clustering performance of ACC(%), NMI(%), and PUR(%) on Yale, WebKB, BDGP, and Caltech101-7 datasets.

**Figure 2.** The convergence curves of FIMVC-TLRC.

more efficient due to it is based on anchor graph, and it leverages tensor low-rank constraints to uncover complementary information between views in incomplete data, resulting in superior clustering performance.

**Figure 3.** ACC w.r.t. γ and λ.

Ablation Experiments: We conducted ablation studies and summarize the results in Table 3. We evaluate the per-

21088

![Figure extracted from page 6](2026-AAAI-federated-incomplete-multi-view-clustering-with-tensorized-low-rank-constraint/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-federated-incomplete-multi-view-clustering-with-tensorized-low-rank-constraint/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-federated-incomplete-multi-view-clustering-with-tensorized-low-rank-constraint/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

Datasets NGs Sonar RGB-D CiteSeer

Metrics ACC NMI PUR ACC NMI PUR ACC NMI PUR ACC NMI PUR

BSV 40.47 18.39 41.31 58.92 1.79 58.92 35.58 26.80 48.04 29.09 6.81 29.87 Concat 32.38 14.20 32.96 56.94 1.81 57.05 33.18 26.09 45.80 30.13 7.65 30.85 DAIMC 63.13 45.62 64.27 57.59 1.81 57.59 33.68 23.27 46.51 35.81 13.39 38.09 PIC 79.31 62.46 79.58 60.26 4.14 60.42 35.50 25.74 48.16 35.93 13.05 37.92 IMSC AGL 86.60 66.74 86.60 56.46 1.49 56.62 33.26 19.85 44.11 46.47 21.00 50.58 IMVC-CBG 84.92 71.48 84.92 58.19 2.29 58.19 34.23 25.27 45.54 43.65 18.17 46.11 VKMC 23.38 2.09 23.64 54.49 6.59 55.02 14.01 3.22 40.89 20.69 3.89 21.78 FedMVL 22.66 2.15 26.89 44.49 1.75 46.63 13.27 4.65 17.18 21.08 1.89 25.51 TensorFMVC 37.86 14.56 38.30 62.61 5.08 62.61 28.81 24.75 47.29 24.20 4.95 24.50 FIMVC-TLRC 90.90 77.39 90.90 67.45 9.22 67.45 35.94 26.64 48.63 48.85 23.94 51.87

**Table 2.** Clustering performance of ACC(%), NMI(%), and PUR(%) on NGs, Sonar, RGB-D, and CiteSeer

Dataset Yale RGB-D BDGP NGs

Metric ACC NMI Purity ACC NMI Purity ACC NMI Purity ACC NMI Purity

Fixed-Anchor 40.41 44.79 41.80 17.32 6.71 30.67 23.36 4.93 24.65 27.13 2.41 27.61 w.o. A-A & T-R 43.22 49.91 45.00 32.11 21.67 39.67 43.14 17.15 44.80 61.01 36.89 61.14 w.o. T-R 44.44 50.34 46.34 34.82 26.61 46.89 47.89 20.22 49.12 86.44 73.56 83.33 FIMVC-TLRC 58.61 64.71 60.81 35.94 26.64 48.63 51.41 22.12 51.43 90.90 77.39 90.90

**Table 3.** Clustering results of the ablation experiments.

**Figure 4.** ACC w.r.t. β and p.

formance of FIMVC-TLRC in four cases: (1) Fixed anchor graph FIMVC-TLRC (Fixed-Anchor): The anchors are initialized by k-means cluster centers without updating during the optimization process. (2) FIMVC-TLRC without anchors alignment and tensor regularization (w.o. A-A & T- R); (3) FIMVC-TLRC without tensor regularization (w.o. T-R); (4) the complete FIMVC-TLRC (FIMVC-TLRC). Compared to Fixed-Anchor, our method achieves better clustering performance across all datasets, demonstrating the effectiveness of locally constructing learnable anchor graphs. In the NGs dataset, w.o. T-R improves ACC, NMI, and PUR compared to w.o. A-A & T-R, further validating the effectiveness of the structure alignment module. Additionally, in the Yale dataset, FIMVC-TLRC achieves superior performance compared to w.o. T-R, indicating that tensor regularization effectively captures consistent information across different views, thereby enhancing clustering performance. The ablation experiment demonstrates the contribution and the necessity of each component.

Convergence Analysis: Figure 2 presents the convergence curves of ACC and the objective function on the WebKB, and NGs datasets. The results indicate that both ACC and the objective loss converge within limited iterations.

Parameter Analysis: Our objective function involves four hyperparameters: γ, λ, β, and p. Figure 3 illustrates the ACC variations across four datasets when γ and λ take values in the set of {0.0001, 0.01, 1, 100, 10000}. From these results, we can observe that γ set to 0.01 yields better performance, while λ has minimal impact. Figure 4 shows the ACC variations for β and p. The clustering performance is optimal when β takes values between 0.0001 and 1, and the performance remains high when p is between 0.1 and 0.9.

## Conclusion

This work presents a novel tensorial federated incomplete multi-view clustering with local anchor alignment (FIMVC- TLRC). The proposed method constructs view-specific anchor graphs to capture complementary information and improve anchor correspondence across views through a structural alignment module. Additionally, it leverages a tensor Schatten p-norm regularizer to fuse representations and effectively exploits consistent information between various views. To support collaborative training under the distributed data settings, we developed a federated unified framework to jointly optimize the construction and alignment of anchor graphs. Experimental results on multiple datasets demonstrate the effectiveness of FIMVC-TLRC.

21089

![Figure extracted from page 7](2026-AAAI-federated-incomplete-multi-view-clustering-with-tensorized-low-rank-constraint/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This research is supported by the National Natural Science Foundation of China (No.62376226), Shaanxi’s Key Research and Development Program (No.2024NC-ZDCYL- 05-05), Xi’an Key Technology Research Projects for Key Agricultural Industry Chains (No. 2024JH-NYZD-0027)and the Yangling Demonstration Zone Science and Technology Plan Project under Grant (No.2024NY-14).

## References

Apt´e, C.; Damerau, F.; and Weiss, S. M. 1994. Automated learning of decision rules for text categorization. ACM Transactions on Information Systems (TOIS), 12(3): 233– 251.

Blum, A.; and Mitchell, T. 1998. Combining labeled and unlabeled data with co-training. In Proceedings of the eleventh annual conference on Computational learning theory, 92– 100.

Cai, X.; Wang, H.; Huang, H.; and Ding, C. 2012. Joint stage recognition and anatomical annotation of drosophila gene expression patterns. Bioinformatics, 28(12): i16–i24.

Chen, X.; Xu, J.; Ren, Y.; Pu, X.; Zhu, C.; Zhu, X.; Hao, Z.; and He, L. 2023. Federated deep multi-view clustering with global self-supervision. In Proceedings of the 31st ACM International Conference on Multimedia, 3498–3506.

Cui, C.; Ren, Y.; Pu, J.; Li, J.; Pu, X.; Wu, T.; Shi, Y.; and He, L. 2024. A novel approach for effective multi-view clustering with information-theoretic perspective. Advances in Neural Information Processing Systems, 36.

Fang, U.; Li, M.; Li, J.; Gao, L.; Jia, T.; and Zhang, Y. 2023. A comprehensive survey on multi-view clustering. IEEE Transactions on Knowledge and Data Engineering, 35(12): 12350–12368.

Fei-Fei, L.; Fergus, R.; and Perona, P. 2004. Learning generative visual models from few training examples: An incremental bayesian approach tested on 101 object categories. In 2004 conference on computer vision and pattern recognition workshop, 178–178. IEEE.

Feng, W.; Wu, Z.; Wang, Q.; Dong, B.; Tao, Z.; and Gao, Q. 2024. Federated multi-view clustering via tensor factorization. In Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24, 3962–3970.

Fu, Y.; Li, Y.; Huang, Q.; Cui, J.; and Wen, J. 2024. Anchor graph network for incomplete multiview clustering. IEEE Transactions on Neural Networks and Learning Systems.

Hu, M.; and Chen, S. 2019. Doubly aligned incomplete multi-view clustering. arXiv preprint arXiv:1903.02785.

Huang, L.; Li, Z.; Sun, J.; and Zhao, H. 2022a. Coresets for Vertical Federated Learning: Regularized Linear Regression and K-Means Clustering. Advances in Neural Information Processing Systems, 35: 29566–29581.

Huang, S.; Shi, W.; Xu, Z.; Tsang, I. W.; and Lv, J. 2022b. Efficient federated multi-view learning. Pattern Recognition, 131: 108817.

Hussain, S. F.; Bisson, G.; and Grimal, C. 2010. An improved co-similarity measure for document clustering. In 2010 ninth international conference on machine learning and applications, 190–197. IEEE. Jia, X.; Dong, X.; Chen, M.; and Yu, X. 2021. Missing data imputation for traffic congestion data based on joint matrix factorization. Knowledge-Based Systems, 225: 107114. Li, L.; Fan, Y.; Tse, M.; and Lin, K.-Y. 2020. A review of applications in federated learning. Computers & Industrial Engineering, 149: 106854. Li, Z.; Tang, C.; Zheng, X.; Liu, X.; Zhang, W.; and Zhu, E. 2022. High-order correlation preserved incomplete multiview subspace clustering. IEEE Transactions on Image Processing, 31: 2067–2080. Liu, H.; Lou, T.; Zhang, Y.; Wu, Y.; Xiao, Y.; Jensen, C. S.; and Zhang, D. 2024. EEG-based multimodal emotion recognition: A machine learning perspective. IEEE Transactions on Instrumentation and Measurement, 73: 1–29. Meng, L.; Qi, Z.; Wu, L.; Du, X.; Li, Z.; Cui, L.; and Meng, X. 2024. Improving global generalization and local personalization for federated learning. IEEE Transactions on Neural Networks and Learning Systems, 36. Qi, X.; Li, M.; Zhou, S.; Feng, W.; and Qi, Z. 2025a. Federated Learning for Science: A Survey on the Path to a Trustworthy Collaboration Ecosystem. Qi, Z.; Meng, L.; Li, Z.; Hu, H.; and Meng, X. 2025b. Cross-Silo Feature Space Alignment for Federated Learning on Clients with Imbalanced Data. In The 39th Annual AAAI Conference on Artificial Intelligence (AAAI-25), 19986–19994. Ren, Y.; Chen, X.; Xu, J.; Pu, J.; Huang, Y.; Pu, X.; Zhu, C.; Zhu, X.; Hao, Z.; and He, L. 2024. A novel federated multi-view clustering method for unaligned and incomplete data fusion. Information Fusion, 108: 102357. Sejnowski, T.; and Gorman, R. 1988. Connectionist bench (sonar, mines vs. rocks). UCI Machine Learning Repository, 10: C5T01Q. Silberman, N.; Hoiem, D.; Kohli, P.; and Fergus, R. 2012. Indoor segmentation and support inference from rgbd images. In Computer Vision–ECCV 2012: 12th European Conference on Computer Vision, Florence, Italy, October 7-13, 2012, Proceedings, Part V 12, 746–760. Springer. Wan, X.; Liu, X.; Liu, J.; Wang, S.; Wen, Y.; Liang, W.; Zhu, E.; Liu, Z.; and Zhou, L. 2023. Auto-weighted multi-view clustering for large-scale data. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, 10078– 10086. Wang, H.; Zong, L.; Liu, B.; Yang, Y.; and Zhou, W. 2019. Spectral perturbation meets incomplete multi-view data. arXiv preprint arXiv:1906.00098. Wang, S.; Liu, X.; Liu, L.; Tu, W.; Zhu, X.; Liu, J.; Zhou, S.; and Zhu, E. 2022. Highly-efficient incomplete largescale multi-view clustering with consensus bipartite graph. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 9776–9785.

21090

<!-- Page 9 -->

Wen, J.; Xu, Y.; and Liu, H. 2018. Incomplete multiview spectral clustering with adaptive graph learning. IEEE transactions on cybernetics, 50(4): 1418–1429. Wen, J.; Zhang, Z.; Fei, L.; Zhang, B.; Xu, Y.; Zhang, Z.; and Li, J. 2022. A survey on incomplete multiview clustering. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 53(2): 1136–1149. Wen, Y.; Wang, S.; Liang, K.; Liang, W.; Wan, X.; Liu, X.; Liu, S.; Liu, J.; and Zhu, E. 2023. Scalable incomplete multiview clustering with structure alignment. In Proceedings of the 31st ACM international conference on multimedia, 3031–3040. Wu, T.; Feng, S.; and Yuan, J. 2024. Low-Rank Kernel Tensor Learning for Incomplete Multi-View Clustering. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 15952–15960. Xu, J.; Li, C.; Ren, Y.; Peng, L.; Mo, Y.; Shi, X.; and Zhu, X. 2022. Deep incomplete multi-view clustering via mining cluster complementarity. In Proceedings of the AAAI conference on artificial intelligence, volume 36, 8761–8769. Zhang, C.; Xie, Y.; Bai, H.; Yu, B.; Li, W.; and Gao, Y. 2021. A survey on federated learning. Knowledge-Based Systems, 216: 106775. Zhao, H.; Liu, H.; and Fu, Y. 2016. Incomplete multi-modal visual data grouping. In IJCAI, 2392–2398.

21091
