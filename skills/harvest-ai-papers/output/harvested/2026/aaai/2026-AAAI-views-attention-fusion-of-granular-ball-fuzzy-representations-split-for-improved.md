---
title: "Views Attention Fusion of Granular-ball Fuzzy Representations Split for Improved Multi-view Clustering"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39556
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39556/43517
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Views Attention Fusion of Granular-ball Fuzzy Representations Split for Improved Multi-view Clustering

<!-- Page 1 -->

Views Attention Fusion of Granular-ball Fuzzy Representations Split for Improved Multi-View Clustering

Shuaiyu Liu1, Song Wu1, Jie Xu2, Yazhou Ren1,3,*, Yang Yang1, Xiaorong Pu1,3, Guoyin Wang4

1School of Computer Science and Engineering, University of Electronic Science and Technology of China, Chengdu, China 2Information Systems Technology and Design Pillar, Singapore University of Technology and Design, Singapore 3Shenzhen Institute for Advanced Study, University of Electronic Science and Technology of China, Shenzhen, China 4Key Laboratory of Cyberspace Big Data Intelligent Security, Ministry of Education, China

## Abstract

Multi-View Clustering (MVC) is a pivotal multi-view learning paradigm widely adopted across various fields. Despite recent advances, existing methods primarily focus on enhancing the performance of fused multi-view representation, often neglecting the issue of Representation Degradation (RD) arising from discrepancies in the intrinsic quality of different views. To address the limitations, we propose a novel Granular-ball Fuzzy Split and Attention Fusion (GFSAF) learning, which leverages the nature of granularball to extract mutual and complementary representation separately. Meanwhile, the proposed method introduces an attention variant for fused representations to mitigate the RD issue. GFSAF mainly consists of two training stages: Split- Extract Stage and Views-Fusion Stage. Specifically, we design a novel Granular-ball Fuzzy Contrastive Learning to extract mutual representation, and introduce Noise Stripping Loss to reduce the influence of noise for complementary representation. Then, a novel multi-head Cross Views Attention is proposed to employ attention mechanism from multiview perspectives for comprehensive fused representations. Experimental results on eight databases demonstrate that our GFSAF achieves superior performance compared to several state-of-the-art MVC methods.

Code — https://github.com/Lsy235/GFSAF

## Introduction

Nowadays, in the era of highly intensive informationization, events or objects of the same type are frequently captured through multiple heterogeneous devices (Zhang et al. 2020; Sun et al. 2023; Li et al. 2023; Xu et al. 2024), resulting in the inherently multi-view nature of data. With the advancement of information technologies, the diversity and complexity of such multi-view data continue to increase. Consequently, effectively extracting comprehensive and valuable information from multi-view data has emerged as a core challenge for Multi-View Learning (MVL) (Muslea, Minton, and Knoblock 2002; Xu et al. 2025).

The essential difference between multi-view data and single-view data is that multi-view data exhibits both homogeneity and heterogeneity across views (Xu et al. 2025).

*Corresponding Author (yazhou.ren@uestc.edu.cn). Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Specifically, views contain homogeneous mutual information while retaining heterogeneous complementary information unique to each view (Sridharan and Kakade 2008). MVL focuses on effectively balancing and integrating these two types of information to achieve a more comprehensive representation. This fundamental difference in the nature of data leads to different learning paradigms. Single view approaches tend to learn cross-sample generalized representations based on mutual information (Tian, Krishnan, and Isola 2020; Tosh, Krishnamurthy, and Hsu 2021). In contrast, multi-view approaches combine multiple views of data, aiming to learn more comprehensive representations by effectively integrating mutual and complementary information (Xu et al. 2022; Trosten et al. 2023).

Although existing methods have shown extraordinary performance, a critical yet underexplored issue is that the performance of downstream tasks is generally dominated by a single superior view, which can even outperform the fusion of all views (Xu et al. 2023). For specific explanation, we consider the representative, unsupervised MVL task, i.e., Multi-View Clustering (MVC) (Bickel and Scheffer 2004; Lebeau, Seddik, and de M Goulart 2024; Ren et al. 2024b; Chen et al. 2025; Zhang et al. 2025b). The clustering performance obtained from one high-quality view often surpasses that of the multi-view fusion, which is referred to as Representations Degradation (RD). Although some methods (Xu et al. 2023; Wu et al. 2024) consider to address the RD issue, they are still limited by the complexity of real-world multi-view data and the RD issue need to be further investigated. Essentially, current paradigms align with the concept of MVL by utilizing diverse perspectives from multiple views, but still have difficulty learning comprehensive and robust models for understanding multi-view samples.

RD phenomenon primarily arises from the model’s tendency to over-rely on mutual information while insufficiently capturing complementary information. During training, the representations of each view increasingly encode mutual information, whereas complementary information diminishes. This process results in elevated similarity between the representations of high-quality and low-quality views. Although such learning may enhance the performance of individual views, it ultimately leads to mediocre fusion results. Consequently, the high-quality view often outperforms the fused representation, particularly when

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

23810

<!-- Page 2 -->

other views are of lower quality. To establish a genuinely effective MVL paradigm, it is crucial to address two longstanding challenges: (i) the inevitable quality discrepancy among different views, and (ii) the effective extraction and fusion of both mutual and complementary information across views.

The first challenge is commonly introduced during data collection due to factors (Ren et al. 2024a; Chen et al. 2024) such as device heterogeneity, acquisition conditions. Although the low-quality view naturally lacks sufficient information, it also contains complementary information that is crucial for MVL. We propose an innovative paradigm for complementing the information of high-quality views with the complementary information of low-quality views to cleverly deal with quality discrepancy. The second challenge lies in extraction and fusion. Mutual information pursues more robust representation, which emphasizes the common semantics captured across views. As in multi-view images of the trucks, mutual information typically denotes the outline or structural shape, whereas complementary information includes unique attributes such as colors or decorations.

For extraction, we adopt granular-ball computing (Xia et al. 2019) and introduce a novel Granular-ball Fuzzy Contrastive Learning (GFCL) for improving MVL. As in the Split-Extract Stage shown in Fig. 1, traditional method operates at the sample level, which leads to an overemphasis on the special information of each sample. Alternatively, using single-size clusters as a basis for classification is simple but tends to suboptimal solutions (Su et al. 2025). To this end, GFCL is proposed to learn representations of mutual information with stronger robustness across views at multiple granularities level. For complementary information, typically hidden in fine-grained local patterns, we employ deeper network and LNS to split-extract representations. In the fusion, we innovatively design a Cross View Attention (CVA) module, a multi-view attention variant inspired by multi-head attention, that effectively fuses both mutual and complementary representations. Unlike usual fusion methods such as concatenation or weighted averaging (Yang et al. 2023; Luo et al. 2024; Su et al. 2025), our studies reveal that the relationship between mutual and complementary information is non-linear and highly entangled, which causes traditional methods to fall into the RD challenge.

Moreover, we propose a novel Granular-ball Fuzzy Split and Attention Fusion (GFSAF) method based on a two-stage learning paradigm, consisting of a Split-Extract Stage (SES) and a Views-Fusion Stage (VFS). Unlike traditional twostage methods, in SES, we introduce and integrate granularball and multi-view contrastive learning. Via a customized pre-training structure, our model aims not only to minimize reconstruction differences, but more importantly, to explicitly split and extract mutual and complementary information across views as the primary objective. In VFS, we design a novel variant of the attention mechanism customized for MVL. Motivated by the complex interdependence between mutual and complementary information, the design of CVA enables to fuse heterogeneous and homogeneous information more effectively. The proposed method significantly alleviates the RD problem observed in existing methods.

Our main contributions can be summarized as follows. • A novel two-stage learning paradigm for MVL is proposed, which effectively deals with the two challenges. In GFSAF, we innovatively divide MVL into the twostage split and fusion task. In SES, one fuzzy contrastive learning in the level of granular-ball is designed to improve the ability of model, which separates and extracts the two types of information effectively. • We propose a novel attention mechanism variant for MVL, which explicitly alleviates the problem of RD. Based on complex and non-linear interdependencies between mutual and complementary information, the proposed CVA utilizes a cross-view attention mechanism to fuse cross-view representations. • Our method is evaluated on multiple databases compared with a variety of state-of-the-art methods in recent years, effectively mitigates RD and achieves superior results.

## Related Work

Multi-View Learning Multi-View Learning, shortly named MVL, has recently gained significant attention and has been widely applied in clustering (Jiang et al. 2025; He et al. 2025; Ren et al. 2025; Eisenberg, Svirsky, and Lindenbaum 2025), recognition (Lu et al. 2025; Zhang et al. 2025a), and so on. However, how to fully and effectively utilize the information containing in multi-view data remains a problem, which is closely related to the challenges mentioned above. Su et al. (2025) proposed a contrastive clustering method and selectively deleted some views to solve quality differences. Yang et al. (2023) proposed a novel dual contrastive calibration network for optimizing cross-view learning. Sun et al. (2024) proposed RMCNC to alleviate the influence of misaligned pairs from multi-view data. Although the above methods effectively improve the information extraction ability from different perspectives, the RD problem arises, which deviates from the concept of MVL. Xu et al. (2023) proposed a novel self-weighted multi-view contrastive learning with reconstruction regularization to alleviate the RD problem.

Our method proposes a novel MVL two-stage method. We introduce multi-granularity balls to effectively alleviate the influence of quality differences and improve the effect of representations split extraction. In addition, we design a novel attention variant to fuse information representations, which effectively alleviates the RD and has been proven to achieve superior performance via extensive experiments.

Granular-ball Computing Inspired by the “large scale first” cognitive mechanism (Chen 1982) and multi-granularity cognitive computation, Xia et al. (2019) proposed one efficient and robust method named granular-ball computing. While preserving the quality of the original database, it can greatly reduce the amount of data, which can be used to effectively mine the distribution structure between arbitrary data of the same category for more generalized models. In recent years, granular-ball has made significant strides in many fields, such as clustering (Xie et al. 2024), classification (Li et al. 2025; Huang

23811

<!-- Page 3 -->

**Figure 1.** Overview of our proposed GFSAF. Multi-view encoder and GFCL form the main structure of SES. CVA (Fig. 2) forms the main of VFS. The single arrow denotes the dataflow of SES and the double arrows denotes the dataflow of VFS.

et al. 2025), graph learning (Xia et al. 2025b), generation (Hu et al. 2025; Xia et al. 2025a), etc. Quadir and Tanveer (2024) proposed granular ball twin support vector machine to deal with challenges in TSVM field.

In this paper, we introduce granular-ball to maximize the extraction of information structures from similar data, thereby extracting representations of mutual information. Compared to existing MVL paradigms, our method represents multi-view data with different quality using multigranularity balls, which mitigates the influence of quality differences and encourages the model to extract more robust mutual representations. Our design maximizes the preservation of multi-view data with quality differences, rather than simply removing low-quality views (Su et al. 2025) or assigning weights for multiple views (Xu et al. 2023).

## Methodology

Overview As shown in Fig. 1, the proposed GFSAF method adopts a two-stage learning paradigm to train the model, consisting of SES and VFS, which is based on the Encoder-Decoder (E-D) framework to construct the network.

Given a multi-view database {Xi}V i=1 with M samples, each sample has multiple instances from V different views. In SES, each view is encoded by its corresponding encoder into a mutual representation Hi ∈Rb×DH of consistent dimension across views. Then Hi is fed into multi-view GFCL, which progressively enhances the quality of Hi as training epochs iterate. Subsequently, we take Hi as the input of deeper fully connected layers to extract the latent complementary representations Zi ∈Rb×DZ. In the extraction of Zi, we design a novel Noise Stripping Loss to mitigate the influence of noise on Zi. Eventually, the concatenated repre- sentation [Hi, Zi] is passed into the decoder, forming a complete training loop during SES. In VFS, we propose CVA to more effectively fuse Hi and Zi, yielding a more comprehensive representation. To ensure consistency in the space of semantic representation and feature dimension, we further adopt Hi to guide the output of CVA, enhancing the convergence efficiency and clustering performance of our model.

Granular-ball Fuzzy Contrastive Learning Multi-view Contrastive Learning (MCL) has emerged as a crucial research direction within the field of MVL. However, the traditional clustering paradigm (Xu et al. 2022; Liu et al. 2024; Zhang et al. 2025c), which only considers single and simplistic MCL or reconstruction during pre-training, has become a key factor contributing to RD. To this end, we enable the model to explore information representations from a multi-granularity perspective by introducing granular-balls, which blur fine-grained details while emphasizing robust decision boundary information effectively. Unlike traditional approaches that rely solely on pointwise cosine similarity as the optimization in MCL, we employ InfoNCE (Information Noise Contrastive Estimation) as the loss, which effectively extracts Hi cross multiple views from the mutual information theoretic perspective. Based on these ideas, we propose a novel Granular-ball Fuzzy Contrastive loss to guide mutual representation learning more effectively. That is:

Li,j

InfoNCE = −Es+∈PGB[s+ −log(es+ +

NGB X s− es−)], (1)

where PGB denotes the set of positive granular-ball pairs and NGB is the set of negative granular-ball pairs in the i, j-th views. s+(s−) denotes the cosine distance between the representations of positive (negative) granular-ball pair.

23812

![Figure extracted from page 3](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

For multi-view, we adopt the granular-ball representation to express the point set of each view as granular-ball set. Granular-ball from different views within the same sample is denoted as PGB. In the same view, when sample points overlap between two granular-balls, they are also classified as PGB to consider potential false negatives. Dissimilar granular-ball is designated as NGB.

LGF C = 1 V (V −1)

V X i=1

V X j=1

Li,j

InfoNCE (∀i̸ = j), (2)

where V denotes the number of views. By minimizing LGF C to maximize the mutual information cross views, Hi tends toward a more robust mutual information representation.

Split-Extract Stage We build the complete framework of GFSAF based on the self-supervised E-D, in which two types of structure, Autoencoder (AE) and Denoising Autoencoder (DAE), are selected as the backbone for SES. Specifically, for the ith view, Ei(·; θi) and Di(·; ϕi) denote its encoder and decoder, respectively. Firstly, Ei(·; θi) performs embeddingbased representation extraction on raw data for Hi. That is:

Hi = Ei(Xi; θi), (3)

where θi denotes the learnable parameters of Ei(·). To further enhance the robustness of Hi, we employ multigranularity balls to represent each view, which fuzzifies the decision boundary of inter-class. Then, we configure positive and negative granular-ball pairs for multi-view GFCL.

Noise Stripping Loss. Based on Hi, we employ deeper fully connected layers to extract Zi that are specific to each view. The core idea for extracting Zi lies in the specific nature of each view itself. However, noise information also shares this same specificity, which has long been a significant challenge in MVL and is one of the main reasons that existing methods struggle to effectively disentangle and extract Zi. From the perspective of definition, complementary information is inherently correlated with mutual information in a complex manner, whereas noise represents a type of information that actively interferes with the learning of mutual information. Recognizing the inherent duality between complementary and noise information, we design a novel Noise Stripping Loss LNS that aims to strip noise representation Ni ∈Rb×DZ in order to significantly extract Zi. That is:

Zi = ReLUsi

Z(FCsi

Z(Hi)), (4)

N i = ReLUsi

N(FCsi

N(Hi)), (5) where ∗i

Z and ∗i

N represent the layers of the network for complementary and noise information, respectively.

LNS = 1

2

V X i=1

(cos(Zi, N i) + 1), (6)

where cos(·) denotes the cosine similarity between two vectors. Eventually, we concatenate Hi and Zi to obtain the fusion representation Fi ∈Rb×DF of SES, which is fed into Di(·; ϕi) to complete the training loop. That is:

**Figure 2.** The proposed Cross Views Attention (CVA) module is as shown. More details can be found in VFS section.

F i = concat(Hi, Zi), (7)

Lrec = 1

V

M X m=1

V X i=1

||Xi m −Di(F i m; ϕi)||

2 2, (8)

where Lrec denotes the reconstruction loss regularization term in SES. ϕi denotes the learnable parameters of Di(·) and Xi m denotes the m-th sample of Xi. In SES, we incorporate the reconstruction loss not as a primary optimization but rather as one regularization term, which encourages the model to place greater emphasis on the split and extraction of mutual and complementary information, rather than focusing on the reconstruction of the data.

Views-Fusion Stage After the split and extraction of mutual and complementary representations in SES, our method proceeds to the next learning stage, which focuses on mining the complex nonlinear interdependence between Hi and Zi, with the target of producing a more comprehensive fused representation ˆF i.

Unlike existing multi-view fusion methods, we propose a novel CVA module, inspired by the attention mechanism, to effectively enhance the fusion between Hi and Zi. As shown in Fig. 2, H and Z extracted for each view are concatenated separately to obtain the multi-view mutual representations Hs and complementary representations Zs, which then are fed into CVA. A transpose separation operation is applied to Hs to generate the key matrix FK, while a deepcopy operation is applied to Zs to obtain the query matrix FQ. The value matrix FV is defined as a weighted mean of both Hs and Zs. Eventually, FQ, FK, and FV are fed into CVA to generate the fused representation, which is formulated as:

FV = mean(FQ, FK), (9)

Attn(FQ, FK, FV) = softmax(

F T

Q × FK √DZ

)FV, (10)

where Attn(·) denotes the attention mechanism. FK represents the mutual information representation of the view to be matched for relevance, while FQ denotes the complementary information representation used to query the relevant associations. The matrix FV serves as the actual source of information, containing Hs and Zs, which are used for fusion.

23813

![Figure extracted from page 4](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

## Algorithm

1: Training steps of GFSAF Input: Multi-view database {Xi}V i=1 Parameter: Batch size b. Hyper-parameters λ1 and λ2. Training epochs Eses, Evfs. Learning rate ℓ. Output: The prediction y

′

1: for e ∈{0, 1,..., Eses + Evfs} do 2: for l ∈{0, 1,..., M/b} do

3: Pick mini-batch {Xi m}(l+1)b m=lb from {Xi}V i=1 4: Compute the gradient of loss 5: Update {θi, ϕi}V i=1 via Adam optimizer 6: if e < Eses then 7: θi = θi −ℓ b

Pb m=1

∂LSES

∂θi, and

8: ϕi = ϕi −ℓ b

Pb m=1

∂LSES

∂ϕi 9: end if 10: if e >= Eses then 11: θi = θi −ℓ b

Pb m=1

∂Lrec

∂θi, and

12: ϕi = ϕi −ℓ b

Pb m=1

∂Lrec

∂ϕi 13: end if 14: end for 15: Obtain y

′ by applying the K-means algorithm in ˆF 16: end for 17: return The prediction y ′

The interdependence between Hs and Zs is deeply mined via the operation of scaled dot-product, which generates an interdependence weight matrix used to guide the fusion. The introduction of multiple attention heads h enhances the ability of mining interdependence from multiple view perspectives. In CVA, we set the number of h equal to V, which encourages view-level attention focus, and prevents attention distraction leading to overattention to details, caused by assigning more heads than views.

Eventually, the fused representation obtained via CVA and the Hi are concatenated for the final representation ˆF i in VFS. This design allows the model to retain connections to the original view representations, which serves for ensuring consistency in the space of semantic representation and feature dimension. The CVA module is not trained during the SES process and is initialized with random weights at the beginning of VFS. Directly using the output of CVA for decoding can result in a large difference of the semantic representation space between SES and VFS, potentially leading to high loss and unstable optimization. To this end, we employ mutual information as a form of semantic space guidance, which helps align the semantic distributions across stages, improves the convergence speed in VFS.

Joint Loss Function

In our GFSAF, SES and VFS are trained separately within the end-to-end manner. The joint loss functions for the two stages, denoted as LSES and LV F S, are defined as follows:

LSES = LGF C + λ1LNS + λ2Lrec, (11)

LV F S = Lrec, (12)

where λ1 and λ2 denote the regularization parameters. By minimizing the loss in both stages, GFSAF effectively alleviates the RD, and extracts a fusion representation that better aligns with the fundamental objective of MVL.

Optimization. In the beginning, the parameters of GF- SAF are randomly initialized. For unsupervised MVC task, we firstly utilize GFSAF and minimize LSES in SES. Nextly, we employ LV F S as the loss function in VFS. Specially, K-means is applied in ˆF to obtain the clustering results. We utilize mini-batch gradient descent optimization to train the proposed GFSAF, which is summarized in Algorithm 1. More details of parameters can be found in next.

## Experiments

Databases and Evaluation Setups The databases involved in the experiments include WebKB, Multi-COIL-10, Multi-COIL-20, Caltech101-7, Prokaryotic, NUSWIDE, Reuters, DHA, and UCI-Digits, as shown in Table 1. The evaluation metric of Accuracy and PUR are selected. PUR, named pairwise unsupervised ranking, is one metric that measures consistency in MVC.

Database Size View Class WebKB (2007) 2, 102 2 2-classes Multi-COIL-10 (1996) 2, 160 3 10-classes Multi-COIL-20 (1996) 4, 320 3 20-classes Caltech101-7 (2004) 1, 400 6 7-classes Prokaryotic (2016) 1, 653 3 4-classes NUSWIDE (2010) 186, 577 5-classes Reuters (2009) 7, 500 6-classes DHA (2012) 966 2 23-classes UCI-Digits (2007) 12, 000 6 10-classes

**Table 1.** Detailed information of all benchmark databases.

Experimental Settings The GFSAF method is implemented with the Pytorch toolbox, employing AE or DAE as the backbone, which is initialized with random weights.

The dimensions of Hi, Zi and ˆF i are based on V. The value of DZ is set to 64, the value of DH is set to V × DZ and DF is set to DH + DZ. Based on extensive experiments in the databases, the values of λ1 and λ2 in Eq. (11) is empirically set to 0.3 and 0.1, respectively. We train GFSAF in an end-to-end manner with single NVIDIA GeForce RTX 4080 SUPER, and the batch size for all databases is set to 256. Then our model is trained using the Adam (Kingma and Ba 2014) with an initial learning rate of 5e −5, weight decay = 0.01. More details are given in open-source code.

Ablation Studies The ablation studies in this section are recorded in the databases. The ablation studies set up in this section focus on the challenge of alleviating the RD problem, the important modules of the proposed method (GFCL, CVA, LNS), and the weight values λ1 and λ2. The effect of each module

23814

<!-- Page 6 -->

## Method

#Params WebKB Multi-COIL-10 Multi-COIL-20 Caltech101-7 Prokaryotic ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ K-means (McQueen 1967) −− 61.74 61.74 42.10 42.10 41.37 41.37 55.17 55.17 56.20 56.20 SEM (Xu et al. 2023) 20.17M 64.41 78.12 97.08 97.08 81.18 83.82 87.20 87.20 56.26 62.61 DealMVC (Yang et al. 2023) 25.12M 59.37 78.12 80.14 80.14 80.00 80.00 88.71 88.71 59.20 63.20 DIVIDE (Lu et al. 2024) 25.19M 88.01 89.12 98.16 98.16 80.39 81.24 62.20 63.51 54.99 54.99 FMCSC (Chen et al. 2024) 23.53M 54.80 54.80 93.75 93.75 82.80 82.80 61.57 61.57 54.16 54.16 RMCNC(Sun et al. 2024) 27.59M 81.59 81.59 89.32 90.57 80.96 81.28 69.16 69.16 54.83 56.19 MGBCC (Su et al. 2025) 21.35M 90.02 90.02 98.86 98.86 40.83 40.83 77.14 77.14 53.36 53.36 GFSAFAE (ours) 19.11M 98.29 98.29 100.0 100.0 83.26 84.17 88.74 88.74 63.89 76.59 GFSAFDAE (ours) 19.11M 94.13 94.13 100.0 100.0 90.42 90.42 90.57 90.57 62.07 84.03

## Method

#Params NUSWIDE Reuters UCI-Digits DHA Average ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ ACC↑ PUR↑ K-means (McQueen 1967) −− 39.73 40.26 31.27 31.27 45.26 45.26 65.60 65.60 48.71 48.77 SEM (Xu et al. 2023) 20.17M 60.60 60.60 56.50 56.50 79.64 79.64 80.90 80.90 72.85 75.37 DealMVC (Yang et al. 2023) 25.12M 25.92 25.96 47.05 48.36 73.16 73.16 48.65 48.65 61.39 64.07 DIVIDE (Lu et al. 2024) 25.19M 53.16 56.35 59.30 59.30 79.16 79.16 70.63 71.84 71.77 72.62 FMCSC (Chen et al. 2024) 23.53M 56.10 56.10 35.67 35.67 57.70 57.70 78.54 78.54 63.90 63.90 RMCNC(Sun et al. 2024) 27.59M 67.59 67.59 51.66 53.07 79.64 80.37 75.49 75.49 72.25 72.81 MGBCC (Su et al. 2025) 21.35M 27.94 30.47 41.83 44.83 46.40 47.60 68.22 68.22 60.51 61.26 GFSAFAE (ours) 19.11M 62.64 62.64 57.94 58.68 84.27 84.27 80.90 80.90 79.99 81.58 GFSAFDAE (ours) 19.11M 61.03 61.03 60.50 60.50 88.50 88.50 78.60 78.60 80.65 83.09

**Table 2.** Performance comparisons among different SoTA methods on several public multi-view databases. The best results are boldfaced and the second results are underlined. ACC↑denotes the accuracy (%) of performance in the database.

(a) Caltech101-7 (b) NUSWIDE (c) Reuters

(d) UCI-Digits (e) WebKB (f) Prokaryotic

**Figure 3.** Ablation of alleviating the problem of RD. vi denotes the performance of single view and vs denotes the fusion views. More results are shown in Appendix B.

in the proposed method is explored through ablation studies on the databases. Ablation studies for the other model parameters are shown in Appendix B.

Challenge of alleviating the RD problem. We show our GFSAF method about RD existing in current MVL paradigm. As shown in Fig. 3, we can observe that the performance of ˆF in our method is significantly higher than that of any other single-view representation. In particular, in the Caltech101-7, NUSWIDE, and Prokaryotic databases, the

#1 #2 #3 ACC↑/ PUR↑ WebKB Caltech101-7 Prokaryotic ✗ ✗ ✗ 88.64/88.64 77.89/77.89 59.47/59.47 ✓ ✗ ✗ 91.24/91.24 79.62/79.62 60.34/60.34 ✗ ✓ ✗ 89.96/89.96 78.12/78.12 59.98/59.98 ✗ ✗ ✓ 91.89/91.89 81.34/81.34 61.24/61.24 ✓ ✓ ✗ 94.03/94.03 84.86/84.86 62.67/74.07 ✓ ✗ ✓ 96.41/96.41 85.74/86.09 62.38/71.29 ✗ ✓ ✓ 93.46/93.46 84.37/84.37 62.97/74.79 ✓ ✓ ✓ 98.29/98.29 88.74/88.74 63.89/76.59

**Table 3.** The ablation study of the proposed key modules. #1, #2 and #3 denote the GFCL, LNS and CVA respectively.

accuracy performance of ˆF is on average 3.97%, 25.98% and 11.92% superior than that of vi, respectively. In all databases, our method shows no any degradation in term of representation quality, which sufficiently demonstrates that the novel MVL paradigm we propose effectively deals with this existing challenge. The proposed paradigm does not merely aim to improve fusion representation performance, but also balances the extraction of effective information from other views and the effective fusion of multi-view information, which aligns more closely with the core of MVL.

Influence of the key modules. As shown in Table 3, when only a single key module is employed in our model, the accuracy performance in three databases all shows a slight improvement. The primary reason is that the three key modules are all designed form the core of MVL, improving information extraction or enhancing fusion, to enhance the ability of

23815

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-006-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

(a) WebKB (b) Multi-COIL-10 (c) Multi-COIL-20 (d) Caltech101-7 (e) UCI-Digits

**Figure 4.** Visualization of fusion features ˆF using t-SNE on five databases.

(a) Influence in WebKB (b) Influence in NUSWIDE

**Figure 5.** Ablation studies for the different of λ1 and λ2.

GFSAF. It should be noted that the improvement achieved by using CVA alone is smaller compared to that of other modules. The primary reason is that the CVA is designed to enhance the fusion effect of the model, which depends on the information quality of Hi and Zi. In particular, when the other two modules are used in combination with CVA, the accuracy performance improves significantly, with the average final performance being 3.12% superior.

Influence of the λ1 and λ2. We evaluate the accuracy performance of our method with the different weight values of λ1 and λ2 in Eq. (11), as shown in Fig. 5. In particular, we can observe that GFSAF achieves the best accuracy when the values of λ1 and λ2 are set to 0.3 and 0.1, respectively.

When a large value of λ1 is set, GFSAF tends to focus excessively on the separation of Zi and Ni, which is theoretically achievable. However, LNS cannot strictly be regarded as the separation of noise. Furthermore, LNS represents an approximate fitting of the separation loss. The relationship between Ni and Zi is complex, and LNS certainly belongs to this relationship, but it cannot fully represent it. Therefore, excessive focus on LNS is not beneficial for model learning. In addition, when a large value of λ2 is set, GF- SAF may overly focus the view reconstruction, which is not beneficial to learning multi-view information. A lower value of Lrec only indicates that the hidden layer representations effectively represent the view data, but this representation has drawbacks in MVL. Under this learning paradigm, there is excessive similarity between the hidden representations of multiple views, which is not conducive to the fusion, which is particularly easy to causing the RD problem.

Comparisons with State-of-The-Art Methods

**Table 2.** shows the comparison results between the proposed GFSAF method and several state-of-the-art methods on all databases shown in Table 1. Only a different portion of the databases in Table 1 is generally selected in the article for each comparison method. To ensure more complete and effective comparability, we use the open source code of the comparison methods to conduct several experiments on the databases without records to obtain the optimal results, which are then compared with our method.

As shown in Table 2, our GFSAF method basically improves the accuracy and PUR performance on all databases with the average improvement of 6.58% and 7.72%, respectively. The accuracy is significantly improved by 8.27% and 8.86% in WebKB and UCI-Digits, respectively. It also improves on all other databases except NUSWIDE. These comparison experiments with the state-of-the-art method clearly demonstrate our advantage in MVC as well as the existence of the proposed GFSAF method with high robustness on different databases. In addition, the method we propose has lighter parameters, which indirectly proves that the improved performance of our method does not necessarily depend on the complex backbone. Our method focuses more on creating a novel paradigm to deal with the common problems of current MVL methods and improve the performance of MVL models by dealing with core challenges. This learning paradigm can also be transferred to other MVL tasks.

2D feature visualization. We use t-SNE (Maaten and Hinton 2008) to visualize ˆF of GFSAF on different databases on the 2D space, respectively, as shown in Fig. 4. We can conclude that ˆF extracted by GFSAF has good classification results not only works well within the network.

## Conclusion

In this paper, we propose a novel GFSAF consisting of SES and VFS. To deal with the challenges of quality discrepancy and RD broadly existing in current methods, we import granular-ball into MVL and design the GFCL and LNS, which obtain mutual representation and complementary representation effectively via the Split-Extract design. In addition, we innovatively introduce attention mechanism and propose CVA, an attention variant, for more effective representations fusion to alleviate the RD. We conduct ablation studies to demonstrate the contributions we mentioned.

23816

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-views-attention-fusion-of-granular-ball-fuzzy-representations-split-for-improved/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work is supported in part by National Natural Science Foundation of China (Nos. 62221005, 62476052, 62450043, and 62222601), Radiation Oncology Key Laboratory of Sichuan Province Open Fund (No. 2024ROKF05), and the Open Fund of the Key Laboratory of Cyberspace Big Data Intelligent Security, Ministry of Education (No. CB- DIS202501).

## References

Amini, M. R.; Usunier, N.; and Goutte, C. 2009. Learning from multiple partially observed views-an application to multilingual text categorization. NeurIPS, 22. Asuncion, A.; Newman, D.; et al. 2007. UCI machine learning repository. Bickel, S.; and Scheffer, T. 2004. Multi-view clustering. In ICDM, volume 4, 19–26. Brbi´c, M.; Piˇskorec, M.; Vidulin, V.; Kriˇsko, A.; ˇSmuc, T.; and Supek, F. 2016. The landscape of microbial phenotypic traits and associated genes. NUCLEIC ACIDS RES, gkw964. Chen, J.; Ling, Y.; Xu, J.; Ren, Y.; Huang, S.; Pu, X.; Hao, Z.; Yu, P. S.; and He, L. 2025. Variational Graph Generator for Multiview Graph Clustering. IEEE TNNLS, 36(6): 11078–11091. Chen, L. 1982. Topological structure in visual perception. Science, 218(4573): 699–700. Chen, X.; Ren, Y.; Xu, J.; Lin, F.; Pu, X.; and Yang, Y. 2024. Bridging gaps: Federated multi-view clustering in heterogeneous hybrid views. NeurIPS, 37: 37020–37049. Eisenberg, R.; Svirsky, J.; and Lindenbaum, O. 2025. COPER: Correlation-based Permutations for Multi-View Clustering. In ICLR. Fei-Fei, L.; Fergus, R.; and Perona, P. 2004. Learning generative visual models from few training examples: An incremental bayesian approach tested on 101 object categories. In CVPR, 178–178. He, H.; Xu, J.; Wen, G.; Ren, Y.; Zhao, N.; and Zhu, X. 2025. Graph Embedded Contrastive Learning for Multi- View Clustering. In IJCAI, 5336–5344. Hu, L.; Chen, F.; Zhao, S.; Duan, S.; et al. 2025. GRICP: Granular-Ball Iterative Closest Point with Multikernel Correntropy for Point Cloud Fine Registration. In AAAI, volume 39, 1710–1718. Huang, J.; Cheung, Y.-m.; Vong, C.-m.; and Qian, W. 2025. GBRIP: Granular Ball Representation for Imbalanced Partial Label Learning. In AAAI, volume 39, 17431–17439. Jiang, X.; He, B.; Zhou, P. Y.; Chen, X.; Guo, J.; Xu, J.; and Liao, Y. 2025. A Unified Framework to BRIDGE Complete and Incomplete Deep Multi-View Clustering under Non-IID Missing Patterns. In ICCV, 594–603. Kingma, D. P.; and Ba, J. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980. Lebeau, H.; Seddik, M. E. A.; and de M Goulart, J. H. 2024. Performance Gaps in Multi-view Clustering under the Nested Matrix-Tensor Model. In ICLR.

Li, Y.; Ouyang, X.; Pan, C.; Zhang, J.; Zhao, S.; Xia, S.; Yang, X.; Wang, G.; and Li, T. 2025. Multi-Granularity Open Intent Classification via Adaptive Granular-Ball Decision Boundary. In AAAI, volume 39, 24512–24520. Li, Y.; Zhang, D.; Yang, M.; Peng, D.; Yu, J.; Liu, Y.; Lv, J.; Chen, L.; and Peng, X. 2023. scBridge embraces cell heterogeneity in single-cell RNA-seq and ATAC-seq data integration. Nat. Commun., 14(1): 6045. Lin, Y.-C.; Hu, M.-C.; Cheng, W.-H.; Hsieh, Y.-H.; and Chen, H.-M. 2012. Human action recognition and retrieval using sole depth information. In ACM MM, 1053–1056. Liu, S.; Liang, K.; Dong, Z.; Wang, S.; Yang, X.; Zhou, S.; Zhu, E.; and Liu, X. 2024. Learn from view correlation: An anchor enhancement strategy for multi-view clustering. In CVPR, 26151–26161. Lu, F.; Hou, Y.; Li, W.; Yang, X.; Zheng, H.; Luo, W.; Chen, L.; Cao, Y.; Liao, X.; Zhang, Y.; et al. 2025. NaFV-Net: An Adversarial Four-view Network for Mammogram Classification. In AAAI, volume 39, 28213–28221. Lu, Y.; Lin, Y.; Yang, M.; Peng, D.; Hu, P.; and Peng, X. 2024. Decoupled contrastive multi-view clustering with high-order random walks. In AAAI, volume 38, 14193– 14201. Luo, C.; Xu, J.; Ren, Y.; Ma, J.; and Zhu, X. 2024. Simple Contrastive Multi-View Clustering with Data-Level Fusion. In IJCAI, 4697–4705. Maaten, L. v. d.; and Hinton, G. 2008. Visualizing data using t-SNE. J Mach Learn Res., 9(Nov): 2579–2605. McQueen, J. B. 1967. Some methods of classification and analysis of multivariate observations. In Proc. of 5th Berkeley Symposium on Math. Stat. and Prob., 281–297. Muslea, I.; Minton, S.; and Knoblock, C. A. 2002. Active + semi-supervised learning = robust multi-view learning. In ICML, volume 2, 435–442. Nene, S. A.; Nayar, S. K.; Murase, H.; et al. 1996. Columbia object image library (coil-20). Quadir, A.; and Tanveer, M. 2024. Granular ball twin support vector machine with pinball loss function. IEEE TCSS. Rasiwasia, N.; Costa Pereira, J.; Coviello, E.; Doyle, G.; Lanckriet, G. R.; Levy, R.; and Vasconcelos, N. 2010. A new approach to cross-modal multimedia retrieval. In ACM MM, 251–260. Ren, Y.; Chen, X.; Xu, J.; Pu, J.; Huang, Y.; Pu, X.; Zhu, C.; Zhu, X.; Hao, Z.; and He, L. 2024a. A novel federated multi-view clustering method for unaligned and incomplete data fusion. INFORM FUSION, 108: 102357. Ren, Y.; Ke, J.; Wen, Z.; Wu, T.; Yang, Y.; Pu, X.; and He, L. 2025. Multi-View Graph Clustering via Node-Guided Contrastive Encoding. In ICML. Ren, Y.; Pu, J.; Cui, C.; Zheng, Y.; Chen, X.; Pu, X.; and He, L. 2024b. Dynamic weighted graph fusion for deep multiview clustering. In IJCAI, 4842–4850. Sridharan, K.; and Kakade, S. M. 2008. An information theoretic framework for multi-view learning. In COLT, 114, 403–414.

23817

<!-- Page 9 -->

Su, P.; Huang, S.; Ma, W.; Xiong, D.; and Lv, J. 2025. Multiview Granular-ball Contrastive Clustering. In AAAI, volume 39, 20637–20645. Sun, T.-K.; Chen, S.-C.; Jin, Z.; and Yang, J.-Y. 2007. Kernelized discriminative canonical correlation analysis. In ICWAPR, volume 3, 1283–1287. Sun, Y.; Qin, Y.; Li, Y.; Peng, D.; Peng, X.; and Hu, P. 2024. Robust multi-view clustering with noisy correspondence. IEEE TKDE. Sun, Y.; Ren, Z.; Hu, P.; Peng, D.; and Wang, X. 2023. Hierarchical consensus hashing for cross-modal retrieval. IEEE TMM, 26: 824–836. Tian, Y.; Krishnan, D.; and Isola, P. 2020. Contrastive multiview coding. In ECCV, 776–794. Tosh, C.; Krishnamurthy, A.; and Hsu, D. 2021. Contrastive learning, multi-view redundancy, and linear models. In Algorithmic Learning Theory, 1179–1206. Trosten, D. J.; Løkse, S.; Jenssen, R.; and Kampffmeyer, M. C. 2023. On the effects of self-supervision and contrastive alignment in deep multi-view clustering. In CVPR, 23976–23985. Wu, S.; Zheng, Y.; Ren, Y.; He, J.; Pu, X.; Huang, S.; Hao, Z.; and He, L. 2024. Self-weighted contrastive fusion for deep multi-view clustering. IEEE TMM, 26: 9150–9162. Xia, S.; Dai, D.; Chen, F.; Yang, L.; Wang, G.; Wang, G.; and Gao, X. 2025a. An Adaptive Multi-Granularity Graph Representation of Image via Granular-Ball Computing. IEEE TIP. Xia, S.; Liu, Y.; Ding, X.; Wang, G.; Yu, H.; and Luo, Y. 2019. Granular ball computing classifiers for efficient, scalable and robust learning. Information Sciences, 483: 136– 152. Xia, S.; Ma, X.; Liu, Z.; Liu, C.; Zhao, S.; and Wang, G. 2025b. Graph coarsening via supervised granular-ball for scalable graph neural network training. In AAAI, volume 39, 12872–12880. Xie, J.; Jiang, L.; Xia, S.; Xiang, X.; and Wang, G. 2024. An adaptive density clustering approach with multi-granularity fusion. INFORM FUSION, 106: 102273. Xu, J.; Chen, S.; Ren, Y.; Shi, X.; Shen, H.; Niu, G.; and Zhu, X. 2023. Self-weighted contrastive learning among multiple views for mitigating representation degeneration. NeurIPS, 36: 1119–1131. Xu, J.; Ren, Y.; Wang, X.; Feng, L.; Zhang, Z.; Niu, G.; and Zhu, X. 2024. Investigating and mitigating the side effects of noisy views for self-supervised clustering algorithms in practical multi-view scenarios. In CVPR, 22957–22966. Xu, J.; Tang, H.; Ren, Y.; Peng, L.; Zhu, X.; and He, L. 2022. Multi-level feature learning for contrastive multi-view clustering. In CVPR, 16051–16060. Xu, J.; Zhao, N.; Niu, G.; Sugiyama, M.; and Zhu, X. 2025. Robust Multi-View Learning via Representation Fusion of Sample-Level Attention and Alignment of Simulated Perturbation. In ICCV, 4232–4241.

Yang, X.; Jiaqi, J.; Wang, S.; Liang, K.; Liu, Y.; Wen, Y.; Liu, S.; Zhou, S.; Liu, X.; and Zhu, E. 2023. Dealmvc: Dual contrastive calibration for multi-view clustering. In ACM MM, 337–346. Zhang, C.; Cui, Y.; Han, Z.; Zhou, J. T.; Fu, H.; and Hu, Q. 2020. Deep partial multi-view learning. IEEE TPAMI, 44(5): 2402–2415. Zhang, H.; Yue, H.; Xiao, X.; Yu, L.; Li, Q.; Ling, Z.; and Zhang, Y. 2025a. Revolutionizing Encrypted Traffic Classification with MH-Net: A Multi-View Heterogeneous Graph Model. In AAAI, volume 39, 1048–1056. Zhang, Y.; Lin, Y.; Yan, W.; Yao, L.; Wan, X.; Li, G.; Zhang, C.; Ke, G.; and Xu, J. 2025b. Incomplete Multi-view Clustering via Diffusion Contrastive Generation. In AAAI, volume 39, 22650–22658. Zhang, Y.; Yan, W.; Tang, C.; Zhou, W.; and Jin, J. 2025c. Multi-branch Space Sharing Feature Aggregation for contrastive multi-view clustering. Pattern Recognition, 111704.

23818
