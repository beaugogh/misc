---
title: "RouterNet: Hierarchical Point Routing Network for Robust Vertebral Landmark Localization on AP X-ray Images"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/42448
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/42448/46409
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# RouterNet: Hierarchical Point Routing Network for Robust Vertebral Landmark Localization on AP X-ray Images

<!-- Page 1 -->

RouterNet: Hierarchical Point Routing Network for Robust Vertebral Landmark

Localization on AP X-ray Images

Yingjie Guo1*, Jinxin Lv1*, Wei Fang2, Qiang Li1†, Zhiwei Wang1†

1Huazhong University of Science and Technology 2Wuhan United Imaging Surgical Healthcare Co., Ltd. guoyingjie@hust.edu.cn, lvjinxin@vivo.com, fenghui@hzau.edu.cn, liqiang8@hust.edu.cn, zwwang@hust.edu.cn

## Abstract

Locating vertebral landmarks on anteroposterior (AP) X-ray images is challenging due to the tissue overlap. Despite the great progress of heatmap-based methods, they often predict missing/false points, which are intolerable in the downstream applications like scoliosis assessment. In this paper, we instead modernize the classic point-regression scheme, and propose a novel model termed RouterNet to locate the 68 vertebral landmarks completely and accurately. RouterNet starts from an initial root point, and then gradually routes it onto more and more points with finer and finer semantics. Router- Net naturally couples such point routing process with its hierarchical and multi-scale feature learning. That is, lower-scale feature maps are utilized to regress points with coarser semantics, and the regressed points pilot a more focused local feature extraction on the next higher-scale map to route onto their subsequent positions with finer semantics. With this divide-and-conquer, RouterNet alleviates the task difficulty, and can robustly localize by routing from the whole spinal center to 17 vertebral centers, and further to their 68 corner points. Extensive and comprehensive experiments on both public and private datasets demonstrate our superior performance over other state-of-the-arts, by decreasing NMSE by 73.8% for landmark localization, and SMAPE by 14.8% for the downstream scoliosis assessment.

Code — https://github.com/YingJGuo/RouterNet

## Introduction

Scoliosis is characterized by lateral spinal curvature accompanied by vertebral rotation (Wang et al. 2021). Manual Cobb angle measurement, the current clinical gold standard, is time-consuming and suffers from high inter-observer variation. Accurately locating vertebral landmarks is crucial for automatic computer-aided scoliosis diagnosis and downstream applications like Cobb angle calculation.

X-ray imaging is widely used in scoliosis diagnosis due to its availability, economy, and lower radiation dose compared to CT. An anteroposterior (AP) X-ray image contains 12 thoracic and 5 lumbar vertebrae, with landmarks defined as four corner points of each vertebra (68 total). However,

*These authors contributed equally. †Corresponding authors Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

(a) (b)

**Figure 1.** (a): Tissue overlap and vertebra-like structures in AP X-ray images. (b): Missing/false points often predicted by heatmap-based methods. The different colors encode four corner points.

as shown in Fig. 1(a), tissue superposition makes the spine low-contrast, and vertebra-like structures cause confusion, making automatic localization extremely challenging.

Current solutions divide into two categories: heatmapbased and point-regression methods.

Heatmap-based methods generate Gaussian heatmaps for each landmark and locate points via local maxima, offering robustness to pose variations, and thus have dominated in tasks of natural scenes. However, the great robustness to large poses usually comes with a price of two types of errors, i.e., missing points (see Fig. 1(b) left) induced by dilution of overlapped tissues, and false points (see Fig. 1(b) right) incurred by other vertebra-like structures. Such errors result in dramatically misguiding biomarkers, and cause misdiagnosis in subsequent clinical applications.

Therefore, we in this paper argue that the heatmap-based methods are overkill in our focusing task, since the robustness to large poses is of secondary importance whereas a correct shape topology (no missing/false, only slightly misaligning) is the primary. Although there are several efforts (Payer et al. 2019; Wang et al. 2022) that have laboriously tried to embed a prior shape into the heatmap generation, the other classical point regression scheme can retain the shape topology effortlessly.

Point-regression methods initialize points and update them progressively, naturally preserving shape topology. However, the highly nonlinear mapping from images to

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

![Figure extracted from page 1](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

landmarks makes direct regression challenging. Recent work (Wang et al. 2024) proposed multi-stage cascaded CNNs, but this complicates training and creates dependency on first-stage predictions.

In view of the above analysis, we in this paper propose a novel and efficient CNN model termed RouterNet, which absorbs the idea of cascade point regression to learn the complex mapping, yet by cascading the intrinsic decoding layers instead of separate models. The task difficulty is further alleviated via a hierarchical point routing strategy on the top of decoded multi-scale global feature maps. Specifically, using the global maps one by one in increasing order of scale, RouterNet first routes the input points onto more points with finer semantics, and then further adjust their positions for the next routing. RouterNet employs a differentiable Precision RoI Pooling (Jiang et al. 2018) to select more focused local features conditioning on the guidance of previously localized points, and also permits itself to be trained in an endto-end manner as a whole.

In summary, our contributions are listed as follows:

• We propose RouterNet, a novel and efficient CNN model for robust vertebral landmark localization by coupling its in-built multi-scale layers with a classic cascaded point regression process. • We alleviate the learning difficulty by hierarchically routing points from coarse to fine in terms of both quantity and semantics. Point-guided local feature selection in RouterNet also permits an end-to-end training and usage of more discriminative visual cues for predicting points with finer semantics. • Extensive and comprehensive experiments on two public and one private datasets demonstrate the superior performance of RouterNet in both the focusing task of landmark localization and the downstream task of scoliosis assessment. Furthermore, RouterNet can almost eliminate missing/false points, and thus shows great potential for other clinical applications.

## Related Work

Heatmap-based Landmark Localization Heatmap-based approaches have achieved success in computer vision (Yu and Tao 2021; Sun et al. 2019) and been applied to vertebral landmarks. FARNet (Ao and Wu 2023) predicts 68 individual heatmaps while Zhang et al. (Zhang et al. 2021) use 6 grouped semantic heatmaps. Both suffer from quantization errors due to discrete arg-max operations (Tompson et al. 2015). Yi et al. (Yi et al. 2020) and Guo et al. (Guo et al. 2021b) address this via coordinate offset regression and Transformers respectively. However, heatmap methods struggle with missing detections and false positives due to tissue occlusion and vertebra-like structures, limiting clinical applicability.

Point-regression Landmark Localization Point-regression methods directly update initialized points toward targets, preserving shape topology. Classical approaches include Active Appearance Models (Matthews and

Baker 2004) and Explicit Shape Regression (Cao et al. 2014). For vertebral landmarks, Sun et al. (Sun et al. 2017) used Structured Support Vector Regression while Wu et al. (Wu et al. 2017) proposed BoostNet. Although these methods eliminate missing/false points, single-stage regression struggles with the complex nonlinear mapping from visual features to landmark coordinates. Wang et al. (Wang et al. 2024) addressed this via cascaded CNNs with PCA constraints, but stage-by-stage training complicates optimization and creates dependency chains. Our RouterNet unifies cascading within a single end-to-end network using hierarchical point routing.

## Method

Revisiting Classic Cascaded Point Regression

The key insight of cascaded point regression is using several regressors to gradually fit a set of initialized points to the target positions stage by stage. In each stage, the regressor uses shape-indexed features to estimate the coordinate offsets. Given an input image I, the process of cascaded point regression can be formulaically expressed as follows:

ˆSt = ˆSt−1 + Regt(Findex(I, ˆSt−1)), t = 1,..., T (1)

where T is the number of total stages, ˆSt is the estimated coordinates of points in the tth stage, Findex is the shapeindexed feature extraction conditioning on points, and Regt is the learnable regressor for the tth stage. The initial ˆS0 is often the average of all training labels, ˆS0 = 1/N P Sn, where Sn is the nth sample’s ground-truth (GT) coordinates. In the training phase, the regression target of Regt is the offsets between the GT and previous-stage coordinates of points, that is, θt

Reg = arg min 1/N P ∥Regt n −(Sn − ˆSt−1 n)∥2. There are two key issues when translating the above cascaded point regression using the concept of deep neural networks. First, the complication of training is unbearable if each Regt is an independent CNN model. Second, the optimization is separate for each stage since Findex is none-differentiable. To address these, our proposed Router- Net reinvents the cascaded process as a coarse-to-fine hierarchical point routing, and tightly couples it with the CNN’s inherent multi-scale feature learning. RouterNet is also equipped with a differentiable local feature selection guided by points, making itself enjoy an end-to-end optimization as a whole.

RouterNet: CNN-style Point Regression

We denote a training sample as {I, (Srt, Sctr, Scnr)}, where I is the AP X-ray image, and Scnr ∈R68×2 is the manually annotated coordinates of the entire 68 vertebral landmarks. Sctr ∈R17×2 is the GT 17 vertebrae’s center points, which is the average of every 4 corners, and Srt is simply defined as one of the centers. We set Srt to the 9th center point, which is the closest point to the whole spine center.

These root, center and corner points (Srt, Sctr, Scnr) are hierarchical representations of the same spine, but with more

<!-- Page 3 -->

704x384x1 z

𝑬𝟏352x192x24

𝑬𝟐176x96x32

𝑬𝟑88x48x48

𝑬𝟒44x24x136 C up, Conv, k3x3, 136

𝑬𝟓22x12x1536

𝑭𝟓

𝑭𝟒

𝑭𝟑

𝑭𝟐

𝑭𝟏

Conv, k1x1, 136 up, Conv, k3x3, 48

C

Conv, k1x1, 48 up, Conv, k3x3, 32

Conv, k1x1, 32 up, Conv, k3x3, 24

C

Conv, k1x1, 24

C

Encoder Decoder

× 𝟏

× 𝟐

× 𝟑 × 𝟑

× 𝟏 × 𝟒

Conv, k1x1, 1536

× 𝟐

22x12x1536

44x24x136

88x48x48

176x96x32

352x192x24

Multi-scale Global Feature Extraction Hierarchical Point Routing Process more point and finer semantic

PLFS

Router

Updater

෠𝑺𝒓𝒕 𝒐

+

PLFS

PLFS

PLFS

PLFS

⊕

Updater

Updater

෡𝑺𝒄𝒓𝒕 𝒐

෠𝑺𝒓𝒕

+

෠𝑺𝒄𝒕𝒓

⊕

෠𝑺𝒄𝒏𝒓 𝒐

+

෠𝑺𝒄𝒏𝒓

Router

෡𝑺𝒓𝒕 ෡𝑺𝒄𝒕𝒓

෡𝑺𝒄𝒏𝒓

𝑺𝒓𝒕

𝑺𝒄𝒕𝒓

𝑺𝒄𝒏𝒓

L1 loss

L1 loss

L1 loss

× 𝟐

× 𝟐

× 𝟐

× 𝟐

MBConv1, k3x3, 24

MBConv6, k3x3, 32

MBConv6, k3x3, 96 MBConv6, k5x5, 136

MBConv6, k5x5, 232 MBConv6, k3x3, 384

MBConv6, k5x5, 48

Conv, k3x3, 32

**Figure 2.** RouterNet contains two parts, i.e., Multi-scale Global Feature Extraction and Hierarchical Point Routing Process. Point-guided Local Feature Selection (PLFS) bridges the two parts as well as routers/updaters, enabling an end-to-end training of RouterNet as a whole.

and more points as well as finer and finer semantics. The relationship between them is formulated as follows:

     

    

Scnr = {(xcnr, ycnr)k},

Sctr = {(xctr, yctr)k} = {1

4

4 X i=1

(xcnr, ycnr)4(k−1)+i},

Srt = (xrt, yrt) = (xctr, yctr)9,

(2)

where k = 1,..., 68 for Scnr and k = 1,..., 17 for Sctr.

RouterNet follows a coarse-to-fine hierarchical routing path: ˆSrt →ˆSctr →ˆScnr. This coarse-to-fine path can be naturally coupled with the inherent multi-scale feature learning in CNN. Motivated by this, RouterNet adopts the framework as shown in Fig. 2, consisting of two major parts, i.e., Multi-scale Global Feature Extraction and Hierarchical Point Routing Process.

Multi-scale Global Feature Extraction RouterNet resizes input I to 704 × 384 and uses a modified EfficientNet- B3 (Tan and Le 2019) encoder-decoder to extract 5 multiscale feature maps {F1,..., F5} with downsampling ratios 22, 42, 82, 162, 322. The encoder consists of MBConv6 blocks with squeeze-and-excitation optimization (Tan et al. 2019; Hu, Shen, and Sun 2018). The decoder progressively fuses encoding features{E1,..., E5} with lowerscale maps to recover semantic information.

Hierarchical Point Routing Process Similar to Eq. (1), RouterNet also starts from an initialized root point. Router- Net makes the feature extraction and point regression highly entangled with each other. The hierarchical point routing process can be formulated as follows:

y

ˆSo rt = 1

N

X

(Srt)n,

ˆSrt = ˆSo rt + Urt(PLFS(F5, ˆSo rt)), ˆSo ctr = ˆSrt ⊕Rrt→ctr(PLFS(F4, ˆSrt)), ˆSctr = ˆSo ctr + Uctr(PLFS(F3, ˆSo ctr)), ˆSo cnr = ˆSctr ⊕Rctr→cnr(PLFS(F2, ˆSctr)), ˆScnr = ˆSo cnr + Ucnr(PLFS(F1, ˆSo cnr))

(3)

where (Srt)n is the nth sample’s GT root, superscript o means a primary status for routing, U(·) and R(·) are updater and router for estimating coordinate offsets, ⊕means broadcast-adding, and PLFS(·) is Point-guided Local Feature Selection (PLFS) which will be detailed in the following.

RouterNet uses lightweight MLP-based routers and updaters that efficiently select local features from static decoding pools. The differentiable PLFS enables end-to-end optimization across the entire path in Eq. (3).

PLFS: Point-guided Local Feature Selection The shape-indexed feature plays a key role in the cascaded shape regression, whereas the previous implementations lack differentiability, impeding a joint learning of both multi-scale feature extractor and point regressors.

In this case, we propose a differentiable parametric module termed PLFS as detailed in Fig. 3, which extracts local features {zk} from a global map F conditioning on the given points S = {(x, y)k} ∈RK×2, where the kth point (x, y)k corresponds to the local feature vector zk (see Eq. (4)).

{zk} = PLFS (F, S; w, h) ∈RKd (4)

where d is channel length identical to F, and (w, h) defines a local window of interest as indicated in Fig. 3.

![Figure extracted from page 3](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

......

𝑥1, 𝑦1

⋮ 𝑥𝑘, 𝑦𝑘

⋮ 𝑥𝐾, 𝑦𝐾 𝒛𝟏

⋮ 𝒛𝒌

⋮ 𝒛𝑲 points placed on map

Point-guided Local Feature Selection (PLFS)

𝑆= point for guidance interpolation at continuous

**Figure 3.** Details in Point-guided Local Feature Selection (PLFS) module. Given points S and a global feature map F, PLFS generates a set of local feature vectors, each of which zk is an differentiable integration within an interesting local windows.

Essentially, PLFS(·) consists of multiple Precise RoI- Pooling layers (Jiang et al. 2018), which ensures gradient back propagation. Each layer corresponds to a point in S, yielding a local feature vector from F. Specifically, a continuous map f (the yellow region in Fig. 3) has to be defined using the following equation:

f(x, y) =

X i,j

IC (x, y, i, j) × F (i, j) (5)

where IC(x, y, i, j) = max(0, 1−|x−i|)×max(0, 1−|y− j|) is an interpolation coefficient, (i, j) is a discrete index of F, and (x, y) is a continuous index of f. Therefore, zk is calculated by integrating over f within the scaled local window centering at the kth point, as formulated in Eq. (6).

zk =

R γ(yk+h/2)

γ(yk−h/2)

R γ(xk+w/2)

γ(xk−w/2) f(x, y)dxdy γ2 × w × h (6)

where k indexes the point in S, γ is a downsampling factor between the feature map F and input image I, that is, γ =

1

2, 1 4, 1 8, 1 16, 1 32 for {F1,..., F5}, and the window size (w, h) is set to (96, 64) in our case.

Point Updating and Routing The entire updating and routing path in Eq. (3) can be viewed as a chain of connected segments. Each segment is a sub-path So F−→

U S

Fnext −−−→

R So next (see Fig. 4), where

So ∈RK×2 is from the initialization or the previous time of routing. So next ∈RKM×2 is the routed points, M means the number of finer points corresponding to each point in S.

Specifically, RouterNet first concatenates the differentiable shape-indexed local features into a single feature vector Z = concat({PLFS (F, So)}) ∈RKd. The updating process can be formulated as follows:

∆S = U(Z) = Z × WU + bU,

S = So + ∆S (7)

where WU ∈RKd×K×2 and bU ∈RK×2 are the updater’s learnable parameters.

With the updated S = {(x, y)k}, the local features of the next routing can be extracted {znext,k} =

**Figure 4.** Details of point updating and routing. PLFSextracted features are concatenated for first updating the point positions. The local features from new positions are then individually processed by a shared router to ‘split’ each point into multiple finer points.

PLFS (Fnext, S) ∈RK×d. The router estimates the coordinate offsets between each point to its finer counterparts. The routing process can be formulated as follows:

{(∆xo next, ∆yo next)k,m} = R(znext,k) = znext,k × WR + bR, {(xo next, yo next)k,m} = {(x, y)k + (∆xo next, ∆yo next)k,m}

(8) where WR ∈Rd×M×2 and bR ∈RM×2 are the router’s learnable parameters, and m = 1,..., M.

The router is shared to spread each point onto M points. Thus, S finally becomes So next containing more points and finer semantics, which can further be updated and routed till the final positions of all landmarks are precisely localized.

Implementation and Training Details The objective of RouterNet is getting close to the GT regression targets of different semantics, i.e., Srt, Sctr, Scnr. The loss for each level of semantic is the total L1 distance between the updated and target points. Unlike the classic point regression which optimizes each regressor independently, PLFS allows the parameters of all updaters and routers as well as the multi-scale feature extractor to be optimized jointly. Therefore, we add the losses together for an endto-end training. The overall loss function can be formulated as:

Ltotal = |Srt −ˆSrt| + |Sctr −ˆSctr| + |Scnr −ˆScnr| (9)

We use data augmentation (horizontal flipping, affine transformation, Gaussian blurring, Gamma transformation), Adam optimizer (lr=1e-3, halved quarterly), batch size 40, and 10 epochs.

Dataset and Evaluation Metrics Dataset This work includes two AP X-ray datasets, i.e., AASCE1 (public) and our private dataset, and a public lateral X-ray dataset, i.e., NHANES II2.

AASCE consists of 707 spinal AP X-ray images from the London Health Sciences Center in Canada. The images were

1https://aasce19.github.io/\#challenge-dataset 2https://wwwn.cdc.gov/nchs/nhanes/nhanes2/default.aspx

![Figure extracted from page 4](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

## Method

AASCEval AASCEtest Private

NMSE ↓ OR20 ↓ OR40 ↓ NMSE ↓ OR20 ↓ OR40 ↓ NMSE ↓ OR20 ↓ OR40 ↓

SCN 4.16E-3 45.14 22.35 5.32E-3 40.32 19.03 5.08E-3 34.34 15.74 SLSN 3.01E-3 49.60 23.22 3.40E-3 63.60 25.35 4.13E-3 48.88 22.66 HRNet 1.82E-3 36.35 15.40 2.65E-3 27.16 10.83 1.26E-3 17.95 7.61 Yi et al. 1.29E-3 29.33 11.26 1.66E-3 31.95 11.06 9.51E-4 18.94 6.19 H3R 1.25E-3 33.13 8.84 8.43E-4 24.56 5.87 9.52E-4 27.64 4.33 FARNet 1.15E-3 29.03 9.87 7.04E-4 14.99 4.73 8.20E-4 22.75 4.46

3000FPS 8.13E-4 12.26 2.16 1.43E-3 14.62 3.14 1.23E-3 13.88 3.68 Cascaded CNNs 4.88E-4 3.62 0.36 7.78E-4 6.68 0.96 3.38E-4 3.68 0.04 RouterNet (Ours) 1.28E-4 1.72 0.08 2.00E-4 2.16 0.24 1.26E-4 1.17 0.09

**Table 1.** Comparison results of vertebral landmark localization on three datasets, i.e., AASCEval, AASCEtest and Private. The first 6 methods are heatmap-based and the last 3 methods uses point-regression strategy. The best performance is marked in bold. See supplementary material for detailed results.

officially divided into 481, 128, and 98 for training, validation, and test, respectively. The training and validation images have the GT labels, each of which contains 4 corner points for each of 17 vertebrae, resulting in 68 landmarks in total. Since the official labels of 98 test images are unavailable, we invited two local experts to label them manually and the annotations are released with our codes for the research purpose.In the following, we denote the 128 validation and 98 test images as AASCEval and AASCEtest, respectively.

Our private dataset contains 36 AP X-ray images collected from a local hospital. Each image was scanned from a scoliosis patient using the Canon X-ray system. The same two local experts were invited to annotate the 68 landmarks of each image, which are consistent with those in the AASCE.

NHANES II contains 214 cervical annotated images collected from 1976 to 1980 conducted by the NCHS for the Second National Health and Nutrition Examination Survey. The images were annotated with 4 vertebrae (C2-C5, 16 corner landmarks). We randomly divided the images into 171 (80%) and 43 (20%) for training and test, respectively.

## Evaluation

Metrics For the task of landmark localization, we employ the consistent metrics with the previous works, i.e., Normalized Mean Squared Error (NMSE), which is calculated as:

NMSE = 1

K

K X k=1

(xk −ˆxk

W)2 + (yk −ˆyk

H)2 (10)

where K is the number of landmarks, i.e., 68 for AASCE and our Private, and 16 for NHANES II, (xk, yk) and (ˆxk, ˆyk) are the predicted and GT absolute point coordinates, and W and H are the width and height of image.

We also report Outlier Ratio outside the distance of r pixels (ORr) to evaluate the missing/false points, calculated as:

ORr = 1

K

K X k=1

I((xk −ˆxk)2 + (yk −ˆyk)2 > r2) (11)

where I(.) is 1 if the inner equation is true and 0 if false, and r defines an error radius.

Besides, AASCE was initialized for a challenge of downstream task called Cobb angle estimation and provided the GT of three angles, i.e., the proximal thoracic (PT), main thoracic (MT), and thoracolumbar (TL) angles. Therefore, we convert the predicted landmarks to the Cobb angle biomarker using the AASCE official tool3, and employ the five challenge-adopted metrics for evaluation, i.e., Manhattan Distance (MD), Euclidean Distance (ED), Chebyshev Distance (CD), Circular Mean Absolute Error (CMAE), and Symmetric Mean Absolute Percentage Error (SMAPE). The calculation of these metrics can refer to the challenge paper (Wang et al. 2021).

Experimental Results and Discussions AP-view Vertebral Landmark Localization We choose 8 recent state-of-the-arts for comparison of vertebral landmark localization, i.e., Yi et al. (Yi et al. 2020), FARNet (Ao and Wu 2023), SLSN (Zhang et al. 2021), Cascaded CNNs (Wang et al. 2024), SCN (Payer et al. 2019), H3R (Yu and Tao 2021), HRNet (Sun et al. 2019), and 3000FPS (Ren et al. 2016). Among them, Cascaded CNNs (Wang et al. 2024) and 3000FPS (Ren et al. 2016) belong to point-regression and the rest ones are heatmapbased. All comparison methods have released source codes. We train the comparison methods and ours using the training data (481 images) of AASCE, and perform the evaluation on AASCEval, AASCEtest, and Private, respectively.

The comparison results are listed in Table 1. Pointregression methods consistently outperform heatmap-based approaches due to inherent shape constraints that eliminate missing/false detections critical for clinical applications. RouterNet achieves significant improvements: 73.8% NMSE reduction on AASCEval compared to Cascaded CNNs (Wang et al. 2024) and 71.6% on AASCEtest compared to FARNet (Ao and Wu 2023), with near-zero missing/false detections.

3http://spineweb.digitalimaginggroup.ca/

<!-- Page 6 -->

HRNet Ours Ground truth

AASCEval AASCEtest Private

SCN Face 3000fps Cascaded CNNs Yi et al SLSN H3R FARNet

**Figure 5.** Visualization results on AASCEval, AASCEtest and our private dataset. Different colors indicate the four corner points for each vertebra.

To further verify the cross-dataset generalization performance of the compared methods, we directly apply the best model evaluated on ASSCEval to predict our private dataset. On Private dataset, RouterNet still achieves 62.7% NMSE improvement over Cascaded CNNs, demonstrating consistent performance across datasets.

**Fig. 5.** gives visual results of different methods on AASCEval, AASCEtest and our private dataset. It can be observed that the heatmap-based methods predict many missing/false points. In comparison, this error rarely occurs in RouterNet’s results. To further reveal this, we plot curves of detection rate by varying normalized error radius(see supplementary material). The curves show that RouterNet achieves near-perfect detection rates with minimal missing/false predictions compared to heatmap-based methods.

Lateral-view Cervical Landmark Localization

To verify the applicability, we compare our method with others on the cervical lateral X-ray images from NHANES II, and the comparison results are shown in Table 2. We can observe that the performance on this dataset is better than that on AP X-ray images for all methods. This is due to the fact that the lateral cervical X-ray images contain fewer vertebralike structures from the heart and lung, and the advantage of using heatmaps emerges, that is, HRNet (Sun et al. 2019) becomes the second-best. Nevertheless, RouterNet still outperforms others in terms of all metrics, indicating its good applicability to other body parts.

## Method

NMSE ↓ OR15 ↓ OR30 ↓

SCN 1.55E-4 3.20 2.91 SLSN 9.47E-5 0.73 0.73 HRNet 2.87E-5 0.29 0.15 Yi et al. 1.12E-4 1.45 1.16 H3R 2.53E-4 6.40 3.78 FARNet 8.55E-5 1.60 1.31

3000FPS 2.93E-5 0.87 0.00 Cascaded CNNs 1.03E-4 0.73 0.00 RouterNet (Ours) 1.74E-5 0.00 0.00

**Table 2.** Comparison results of cervical landmark localization on NHANES II. The best performance is marked in bold.

Ablation Studies

The Effectiveness of Hierarchical Routing Table 3 validates hierarchical routing effectiveness through three variants: direct 68-landmark regression without routing, routing once (centers→corners), and routing twice (root→centers→corners). Progressive routing achieves 61.7% and 60.6% NMSE improvements respectively, confirming the divide-and-conquer strategy’s effectiveness.

The Selection of Root Point We also analyze the impact of different selections of root point. We exhaustively train

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-26.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-29.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-routernet-hierarchical-point-routing-network-for-robust-vertebral-landmark-local/page-006-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Method

NMSE ↓ OR20 ↓ OR40 ↓ w/o Routing 8.48E-4 23.98 2.83 Routing once 3.25E-4 4.39 0.13 Routing twice 1.28E-4 1.72 0.08

**Table 3.** The comparison results on AASCEval of Router- Net (‘Routing twice’) and its two variants with different routing times.

## Method

CMAE ↓ED ↓MD ↓CD ↓SMAPE ↓

Wang et al. - - - - 23.43 Horng et al. - - - - 16.48 PFA 6.69 - - - 12.97 CGN 4.77 - - - 10.25 Guo et al. - - - - 8.62 Kpt-Transformer - - - - 8.40 W-Transformer - - - - 8.26 VF 3.51 - - - 7.84 Seg4Reg 3.96 - - - 7.64 Seg4Reg+ 3.73 - - - 7.32

SCN 22.80 44.08 68.42 34.74 31.62 SLSN 4.04 8.19 12.14 6.86 9.08 HRNet 12.23 24.38 36.71 19.53 21.77 Yi et al. 3.55 7.13 10.63 5.90 8.21 H3R 7.20 14.60 21.60 12.12 15.34 FARNet 8.06 16.38 24.17 13.43 16.15 3000FPS 7.61 15.23 22.84 12.64 17.01 Cascaded CNNs 6.51 12.81 19.54 10.37 14.60 RouterNet (Ours) 2.69 5.30 8.07 4.27 6.24

**Table 4.** Comparison results of scoliosis assessment on AASCEval.The best performance is marked in bold.

0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8

0.00E+00

5.00E-05

1.00E-04

1.50E-04

2.00E-04

2.50E-04

1 3 5 9 11 13 15 17

NMSE OR_40

NMSE

Root point index

𝑶𝑹𝟒𝟎

**Figure 6.** The effect of selecting different vertebra as root point on AASCEval.

17 variants of RouterNet by using the first to last vertebra’s center point as root, and the comparison results are shown in Fig. 6. Analysis of root point selection shows the 9th vertebra center achieves optimal performance, enabling potential semi-automatic clinical deployment.

Application on Scoliosis Assessment We evaluate our method in a downstream task called scoliosis assessment on AASCEval using the officially released

## Method

CMAE ↓ED ↓MD ↓CD ↓SMAPE ↓

XMU 4.91 11.23 14.74 10.17 22.18 iFLYTEK 5.48 12.14 16.45 10.74 22.17 Seg4Reg 4.85 11.17 14.55 10.16 21.71

SCN 29.79 58.34 89.35 46.11 48.26 SLSN 3.59 7.39 10.78 6.21 11.51 HRNet 17.64 34.72 52.99 27.64 36.59 Yi et al. 3.42 6.84 10.25 5.61 11.44 H3R 8.95 17.43 26.85 14.04 23.48 FARNET 8.61 17.37 25.77 14.20 21.63 3000FPS 7.58 14.90 22.75 12.01 23.68 Cascaded CNNs 7.46 14.83 22.38 12.24 21.30 RouterNet (Ours) 2.80 5.63 8.40 4.64 9.45

**Table 5.** Comparison results of scoliosis assessment on AASCEtest. The best performance is marked in bold.

GT Cobb angles.

For the localization methods, the Cobb angles are calculated using the official tool as mentioned in the evaluation metrics section. Besides, we also include 10 recent state-of-the-arts focusing on scoliosis assessment. The results of (Huo et al. 2021; Guo et al. 2021a,b; Yao et al. 2022; Lin et al. 2019, 2021) are reported in their original papers, and the results of (Wang et al. 2019; Horng et al. 2019; Wang, Wang, and Liu 2019; Kim et al. 2020) are borrowed from (Yao et al. 2022; Lin et al. 2021).

The comparison results are listed in Table 4. RouterNet achieves the best scoliosis assessment performance, outperforming VF (Kim et al. 2020) by 23.4% (CMAE) and Seg4Reg+ (Lin et al. 2021) by 14.8% (SMAPE).

On challenge test data AASCEtest, we include the results of the top three participants(Lin et al. 2019; Chen et al. 2019; Wang, Huang, and Wang 2019). The comparison results are listed in Table 5. Our method achieves SMAPE less than half of the champion’s (Lin et al. 2019).

## Conclusion

We propose RouterNet, a hierarchical point routing network that decomposes vertebral landmark localization into progressive sub-tasks. By coupling multi-scale feature learning and point-guided local feature selection (PLFS) with coarseto-fine point routing, RouterNet achieves superior performance while eliminating missing/false detections. Extensive experiments on three datasets demonstrate significant improvements in both landmark localization and scoliosis assessment, with potential for clinical deployment through semi-automatic operation.

Although RouterNet is fully automatic in this work by use of the initial root pre-calculated based on all training samples, it can be naturally extended to be semi-automatic and more controllable in the clinical practice by allowing the doctor to give an initial point manually. Our further work will focus on vertebral landmark localization on X-ray images with arbitrary FOV.

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by National Natural Science Foundation of China (Grant No.62202189), research grants from Wuhan United Imaging Healthcare Surgical Technology Co., Ltd.

## References

Ao, Y.; and Wu, H. 2023. Feature Aggregation and Refinement Network for 2D Anatomical Landmark Detection. Journal of Digital Imaging, 36(2): 547–561. Cao, X.; Wei, Y.; Wen, F.; and Sun, J. 2014. Face alignment by explicit shape regression. International journal of computer vision, 107(2): 177–190. Chen, K.; Peng, C.; Li, Y.; Cheng, D.; and Wei, S. 2019. Accurate automated keypoint detections for spinal curvature estimation. In International Workshop and Challenge on Computational Methods and Clinical Applications for Spine Imaging, 63–68. Springer. Guo, Y.; Li, Y.; He, W.; and Song, H. 2021a. Heterogeneous Consistency Loss for Cobb Angle Estimation. In 2021 43rd Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC), 2588–2591. IEEE. Guo, Y.; Li, Y.; Zhou, X.; and He, W. 2021b. A keypoint transformer to discover spine structure for cobb angle estimation. In 2021 IEEE International Conference on Multimedia and Expo (ICME), 1–6. IEEE. Horng, M.-H.; Kuok, C.-P.; Fu, M.-J.; Lin, C.-J.; and Sun, Y.-N. 2019. Cobb angle measurement of spine from X-ray images using convolutional neural network. Computational and mathematical methods in medicine, 2019. Hu, J.; Shen, L.; and Sun, G. 2018. Squeeze-and-excitation networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, 7132–7141. Huo, L.; Cai, B.; Liang, P.; Sun, Z.; Xiong, C.; Niu, C.; Song, B.; and Cheng, E. 2021. Joint Spinal Centerline Extraction and Curvature Estimation with Row-Wise Classification and Curve Graph Network. In International Conference on Medical Image Computing and Computer-Assisted Intervention, 377–386. Springer. Jiang, B.; Luo, R.; Mao, J.; Xiao, T.; and Jiang, Y. 2018. Acquisition of localization confidence for accurate object detection. In Proceedings of the European conference on computer vision (ECCV), 784–799. Kim, K. C.; Yun, H. S.; Kim, S.; and Seo, J. K. 2020. Automation of spine curve assessment in frontal radiographs using deep learning of vertebral-tilt vector. IEEE Access, 8: 84618–84630. Lin, Y.; Liu, L.; Ma, K.; and Zheng, Y. 2021. Seg4Reg+: Consistency Learning Between Spine Segmentation and Cobb Angle Regression. In International Conference on Medical Image Computing and Computer-Assisted Intervention, 490–499. Springer. Lin, Y.; Zhou, H.-Y.; Ma, K.; Yang, X.; and Zheng, Y. 2019. Seg4Reg networks for automated spinal curvature estimation. In International Workshop and Challenge on Computational Methods and Clinical Applications for Spine Imaging, 69–74. Springer.

Matthews, I.; and Baker, S. 2004. Active appearance models revisited. International journal of computer vision, 60(2): 135–164. Payer, C.; ˇStern, D.; Bischof, H.; and Urschler, M. 2019. Integrating spatial configuration into heatmap regression based CNNs for landmark localization. Medical image analysis, 54: 207–219. Ren, S.; Cao, X.; Wei, Y.; and Sun, J. 2016. Face alignment via regressing local binary features. IEEE Transactions on Image Processing, 25(3): 1233–1245. Sun, H.; Zhen, X.; Bailey, C.; Rasoulinejad, P.; Yin, Y.; and Li, S. 2017. Direct estimation of spinal cobb angles by structured multi-output regression. In International conference on information processing in medical imaging, 529– 540. Springer. Sun, K.; Xiao, B.; Liu, D.; and Wang, J. 2019. Deep highresolution representation learning for human pose estimation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 5693–5703. Tan, M.; Chen, B.; Pang, R.; Vasudevan, V.; Sandler, M.; Howard, A.; and Le, Q. V. 2019. Mnasnet: Platform-aware neural architecture search for mobile. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2820–2828. Tan, M.; and Le, Q. 2019. Efficientnet: Rethinking model scaling for convolutional neural networks. In International conference on machine learning, 6105–6114. PMLR. Tompson, J.; Goroshin, R.; Jain, A.; LeCun, Y.; and Bregler, C. 2015. Efficient object localization using convolutional networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, 648–656. Wang, J.; Jin, Y.; Cai, S.; Xu, H.; Heng, P.-A.; Qin, J.; and Wang, L. 2022. Real-time landmark detection for precise endoscopic submucosal dissection via shape-aware relation network. Medical Image Analysis, 75: 102291. Wang, J.; Wang, L.; and Liu, C. 2019. A multi-task learning method for direct estimation of spinal curvature. In International Workshop and Challenge on Computational Methods and Clinical Applications for Spine Imaging, 113–118. Springer. Wang, L.; Xie, C.; Lin, Y.; Zhou, H.-Y.; Chen, K.; Cheng, D.; Dubost, F.; Collery, B.; Khanal, B.; Khanal, B.; et al. 2021. Evaluation and comparison of accurate automated spinal curvature estimation algorithms with spinal anteriorposterior X-Ray images: The AASCE2019 challenge. Medical Image Analysis, 72: 102115. Wang, L.; Xu, Q.; Leung, S.; Chung, J.; Chen, B.; and Li, S. 2019. Accurate automated Cobb angles estimation using multi-view extrapolation net. Medical Image Analysis, 58: 101542. Wang, S.; Huang, S.; and Wang, L. 2019. Spinal curve guide network (SCG-Net) for accurate automated spinal curvature estimation. In International Workshop and Challenge on Computational Methods and Clinical Applications for Spine Imaging, 107–112. Springer.

<!-- Page 9 -->

Wang, Z.; Lv, J.; Yang, Y.; Lin, Y.; Li, Q.; Li, X.; and Yang, X. 2024. Accurate scoliosis vertebral landmark localization on X-ray images via shape-constrained multi-stage cascaded CNNs. Fundamental Research, 4(6). Wu, H.; Bailey, C.; Rasoulinejad, P.; and Li, S. 2017. Automatic landmark estimation for adolescent idiopathic scoliosis assessment using BoostNet. In Medical Image Computing and Computer Assisted Intervention- MICCAI 2017: 20th International Conference, Quebec City, QC, Canada, September 11-13, 2017, Proceedings, Part I 20, 127–135. Springer. Yao, Y.; Yu, W.; Gao, Y.; Dong, J.; Xiao, Q.; Huang, B.; and Shi, Z. 2022. W-Transformer: Accurate Cobb angles estimation by using a transformer-based hybrid structure. Medical Physics. Yi, J.; Wu, P.; Huang, Q.; Qu, H.; and Metaxas, D. N. 2020. Vertebra-focused landmark detection for scoliosis assessment. In 2020 IEEE 17th International Symposium on Biomedical Imaging (ISBI), 736–740. IEEE. Yu, B.; and Tao, D. 2021. Heatmap regression via randomized rounding. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(11): 8276–8289. Zhang, C.; Wang, J.; He, J.; Gao, P.; and Xie, G. 2021. Automated vertebral landmarks and spinal curvature estimation using non-directional part affinity fields. Neurocomputing, 438: 280–289.
