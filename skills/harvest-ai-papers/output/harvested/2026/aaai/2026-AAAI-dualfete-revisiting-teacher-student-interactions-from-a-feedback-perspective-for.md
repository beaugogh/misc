---
title: "DualFete: Revisiting Teacher-Student Interactions from a Feedback Perspective for Semi-supervised Medical Image Segmentation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40008
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40008/43969
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# DualFete: Revisiting Teacher-Student Interactions from a Feedback Perspective for Semi-supervised Medical Image Segmentation

<!-- Page 1 -->

DualFete: Revisiting Teacher-Student Interactions from a Feedback Perspective for Semi-supervised Medical Image Segmentation

Le Yi1, Wei Huang1*, Lei Zhang1*, Kefu Zhao1, Yan Wang2, Zizhou Wang2

1College of Computer Science, Sichuan University, China 2Institute of High Performance Computing, A*STAR, Singapore {yile, kefuzhao}@stu.scu.edu.cn, {weihuang, leizhang}@scu.edu.cn, {wangyan, wang zizhou}@a-star.edu.sg

## Abstract

The teacher-student paradigm has emerged as a canonical framework in semi-supervised learning. When applied to medical image segmentation, the paradigm faces challenges due to inherent image ambiguities, making it particularly vulnerable to erroneous supervision. Crucially, the student’s iterative reconﬁrmation of these errors leads to self-reinforcing bias. While some studies attempt to mitigate this bias, they often rely on external modiﬁcations to the conventional teacherstudent framework, overlooking its intrinsic potential for error correction. In response, this work introduces a feedback mechanism into the teacher-student framework to counteract error reconﬁrmations. Here, the student provides feedback on the changes induced by the teacher’s pseudo-labels, enabling the teacher to reﬁne these labels accordingly. We specify that this interaction hinges on two key components: the feedback attributor, which designates pseudo-labels triggering the student’s update, and the feedback receiver, which determines where to apply this feedback. Building on this, a dual-teacher feedback model is further proposed, which allows more dynamics in the feedback loop and fosters more gains by resolving disagreements through cross-teacher supervision while avoiding consistent errors. Comprehensive evaluations on three medical image benchmarks demonstrate the method’s effectiveness in addressing error propagation in semi-supervised medical image segmentation.

## Introduction

Medical image segmentation, which provides quantitative proﬁles for inner-body anatomical structures, plays a vital role in clinical practice and has emerged as a rapidly evolving subﬁeld of AI for medicine (Luo et al. 2022a; Chen et al. 2024; Li et al. 2025; Lan et al. 2025a,b). However, annotating medical images requires specialized expertise and is particularly labor-intensive at the voxel level. As a result, segmentation models often suffer from performance degradation due to the limited availability of labeled training data.

Semi-supervised learning (SSL) overcomes this limitation by leveraging additional supervision from unlabeled data. One line of SSL work follows the smoothness assumption, which posits that if two samples are close in data space, then so should be their corresponding outputs (Chapelle et al.

*Corresponding author: Wei Huang; Lei Zhang. Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

Dice

FS MT

CS Fb 95HD FS MT

CS Fb image label error entropy

FullySupervise MeanTeacher CrossSuperviseFeedback Tea-Stu

(b) Heatmaps of error frequency and predicting entropy

(c) Histograms of error frequency

(a) Pseudolabel accuracy count lx θ

T θ

S θ

PL EMA ux lx ux

PL θ

2 θ lx ux lx ux

T θ

S θ

PL ux feedback lx ux

(d) Schematics of different learning frameworksFeedback-coupled teacher-student

0 100 4

12 85

91

0 0 0 0 0

4e4

0

4e4

0

4e4

0

4e4

**Figure 1.** Pre-experiments on the LA dataset. 16 labeled samples are used. FullySpervise runs with only the labeled set, while others use both. Results are evaluated on the ﬁrst unlabeled sample and averaged from the last 100 training steps. It can be seen that medical image segmentation is susceptible to continual errors, so the conﬁrmation bias issue is fairly problematic. Consistent errors can be reduced by the feedback interaction [highlighted in (d)].

2009). Consistency constraints, thus, are imposed on models to match the prediction of a perturbed sample to that of its vanilla counterpart (Luo et al. 2021; Huang et al. 2025). Another line follows the clustering assumption, emphasising that samples should reside in high-density regions. It motivates pseudo-labeling unlabeled data for entropy minimization (Grandvalet and Bengio 2004); ultimately, samples can be compactly clustered by classes. Notably, accurate supervision is crucial for both lines of work, as models tend to perpetuate historical errors without awareness of their own mistakes, thereby rendering these errors increasingly difﬁcult to correct. This degenerating case is known as conﬁrmation bias (Ke et al. 2019).

This bias, unfortunately, incurs more hazards in semisupervised medical image segmentation (SSMIS) due to image ambiguity; it leads to high regional uncertainty, especially near object boundaries. [Figure 1(b)] (Yi et al. 2025). For unseen samples, models are prone to generate erroneous pseudo-labels. Paradoxically, when trained on such

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27852

<!-- Page 2 -->

error-prone supervision, they exhibit overconﬁdence in mistakes (low-entropy regions yet with high error frequency). Some studies attempt to prevent models from ﬁtting to unreliable supervision, thereby partially alleviating error reinforcement (Bai et al. 2023; Wu et al. 2023; Wang et al. 2023; Shen et al. 2023; Chi et al. 2024). However, these heuristic-based methods remain insufﬁcient to counteract the intrinsic error-accumulation tendency of the prevailing teacher-student paradigm. This limitation stems from two fundamental issues. First, most methods rely on model-level perturbations to introduce teacher-student discrepancies and promote representation learning by resolving disagreement. However, such strategies are inadequate for highly nonlinear networks, as they tend to degenerate into self-training behavior, failing to sustain meaningful disagreement. Second, and more critically, the conventional teacher-student paradigm lacks inherent mechanisms for error correction. Although pseudo-labels can be inﬂuenced by the student using methods like Mean Teacher (Tarvainen and Valpola 2017) or cross supervision (Chen et al. 2021)[Figure 1(d)], the student has no way to verify whether the update induced by pseudo-labels remains aligned with the constraint induced by labeled data. Once convergence, such methods yield vast consistent mistakes [Figure 1(c)] and also derive negligible change in pseudo-labeling accuracy [Figure 1(a)]. Thus, during the degenerative process toward self-training, they continually accumulate errors, exacerbating miscalibrated predictions and intensifying conﬁrmation bias.

In this work, we incorporate a feedback mechanism into the teacher-student framework, wherein the student assesses whether the updates driven by pseudo-labels align with the direction implied by ground-truth supervision. This assessment is then fed back to the teacher to guide reﬁnements of pseudo-labels. Through this interaction, the framework acquires inherent error-correcting capabilities, helping to prevent error accumulation. As shown in Figure 1(c), this method effectively reduces recurring mistakes. To operationalize this feedback loop, we introduce two key components: the feedback attributor, which identiﬁes the pseudolabels responsible for triggering the student’s update, and the feedback receiver, which determines the pseudo-labeling probabilities to be adjusted. Building on this foundation, we propose a dual-teacher feedback model, where two teachers collaboratively instruct a student and receive individualized feedback from the student, while also improving each other by resolving their mutual disagreements. This dual-teacher framework not only strengthens the feedback dynamics to mitigate persistent errors but also encourages constructive disagreement, fostering more effective teaching curricula. Extensive experiments are conducted on three benchmarks, including LA (Xiong et al. 2021), Pancreas (Roth et al. 2015), and BraTS (Menze et al. 2014), with sufﬁcient justiﬁcation of our method in these error-prone scenarios.

Contributions are summarized as follows: (1) We introduce a feedback mechanism that equips the teacher-student model with error-correction capabilities, fundamentally mitigating vulnerability raised by error propagation in semi-supervised medical image segmentation.

(2) We develop a dual-teacher feedback model that coor- dinates: (i) cross-supervision for resolving conﬂicts, and (ii) feedback loss for preserving teachers’ diversity while suppressing errors. The two aspects enhance feedback dynamics and work collaboratively to teach a superior student.

(3) Comprehensive experiments on three benchmarks conﬁrm our method’s effectiveness in combating this errorprone scenario, with sufﬁcient justiﬁcation through detailed quantitative and qualitative analysis.

## Related Work

Semi-supervised medical image segmentation Advanced models are marching fastly and have made great breakthroughs in real-world segmentation tasks (Dosovitskiy et al. 2020; Hu et al. 2023). Such advancements, however, are lagging in the medical ﬁeld mainly due to the scarcity of annotations. As a solution, researchers turn to SSL to excavate gains from limited labeled data and massive unlabeled data. Methods are categorized into two lines: consistency regularization (Chapelle et al. 2009) and entropy minimization (Grandvalet and Bengio 2004). The former argues the output consistency between a perturbed data and its vanilla input. Such perturbations can be conducted at input (Bai et al. 2023; Chi et al. 2024), feature (Yang et al. 2023; Huang et al. 2024), and model (Luo et al. 2022b) levels. The latter argues for separating samples into clusters, driving to minimize entropy via pseudo labels. Representative methods, such as cross supervision (Chen et al. 2021) and Co-training (Qiao et al. 2018), employ multiple learnable models to facilitate mutual learning.

Notably, medical image ambiguity leads to error-prone supervision and inconsistent model predictions. While prior work has shown that models can beneﬁt from learning courses designed to reduce ambiguity (Xu et al. 2023) and disagreement (Shen et al. 2023; Wang et al. 2023), they inherently lack the ability to handle erroneous pseudo-labels in the teacher-student paradigm. Without explicit errorcorrection, this paradigm tends to accumulate more irreversible mistakes. Some studies address prediction disagreements while improving supervision accuracy, either by ﬁltering unreliable targets using conﬁdence thresholds (Shen et al. 2023; Huang et al. 2025) and predictive uncertainty (Yu et al. 2019; Shi et al. 2021), or by competitively generating pseudo-labels from multiple models (Wu et al. 2023; Wang et al. 2023; Su et al. 2024). However, these solutions introduce additional architectural constraints that often fail to maintain meaningful disagreement due to the models’ tendency to degenerate into trivial self-training behavior.

This paper introduces a feedback mechanism within the teacher-student framework, endowing it with intrinsic error correction capabilities. With this foundation, we propose a dual-teacher feedback model that not only prevents error accumulation but actively beneﬁts from disagreements.

Conﬁrmation bias in semi-supervised learning In SSL, conﬁrmation bias (Nickerson 1998) creates an errorreinforcing cycle where the model grows increasingly overconﬁdent in its mistakes and resistant to correction (Arazo et al. 2020). Rollwage et al. (2020) claim that metacognitive

27853

<!-- Page 3 -->

interventions are one kind of method to combat the high con- ﬁdence in the shaping process of conﬁrmation bias in psychology. Such ﬁndings hint at least two routes to address this bias in SSL: (1) conﬁdence reduction, which disrupts the reinforcing cycle of high-conﬁdence errors, and (2) active interventions, which devise strategies to regularize the model toward expected learning direction. Arazo et al. (2020) and Liu et al. (2022a) supervise the model using soft pseudolabels yielded by mixup techniques (Zhang et al. 2018); they argue for the alleviation of high-conﬁdence mistakes. Some studies impose a minimum labeled-data ratio, either per mini-batch (Arazo et al. 2020) or per image (Bai et al. 2023), to avoid the distributional shift far from the labeled data. Likewise, Shen et al. (2023) and Chi et al. (2024) substitute uncertain patches with more reliable ones, and thus avoid accumulating too many errors. Some studies also propose competitive methods to ensure the correctness of pseudo-labels (Wu et al. 2023; Wang et al. 2023).

While the above heuristically-driven solutions mitigate conﬁrmation bias to some extent, the feedback interaction proposed in this work can address this issue more straightforwardly, as it inherently acts like a metacognitive intervention. Moreover, in a dual-teacher framework, we can enhance this feedback to be more dynamic.

## Methodology

Let θ be a segmentation model; it inputs an image x and predicts probabilities f θ:= f(x; θ). This model is expected to generalize well with a labeled dataset Dl = {(xl, yl)}Nl and an unlabeled dataset Du = {xu}Nu, where xl, xu represents the labeled and unlabeled sample, respectively, yl is the label mask of xl, each voxel being one of C:= {0,..., C −1} classes. Nl = |Dl|, Nu = |Du| is the respective dataset size, and it satisﬁes Nl ≪Nu.

The teacher-student model is a learning paradigm in the sense that a teacher θT pseudo-labels unlabeled data xu, which is used to supervise the student θS such that segmentation loss on Du is minimized in terms of pseudo-labels ˆyu:

ˆyu = arg max c∈C fc(xu; θT) (1)

min θS LS(θS,θT; Du) = min θS

1 Nu

Nu X i ℓ(f(xu i; θS), ˆyu i) (2)

f θ c = fc(·; θ) is the c-th class prediction, and ℓis the loss function. Due to the ambiguity, medical image segmentation is susceptible to error supervision. However, the current teacher-student model can not perceive whether the update induced by pseudo-labels would further cause error reinforcement. To this end, we propose DualFete, which employs a feedback mechanism to equip the teacher-student model with error-correcting abilities. This mechanism will be further enhanced in a dual-teacher framework.

Feedback-coupled teacher-student model To avoid error accumulation, current SSMIS work sets a minimum labeled-data ratio per batch and employs some heuristically-driven methods to regularize training towards

(a) vanilla feedback ux lx φ ψ

' θ θ

' θ l

' l

' l attributors receivers compare confidence a y φ  d y φ  a y ψ  d y ψ  a y d y a y δ d y δ ux lx pseudo-labelinduced update θ

' θ φ l

' l feedback

ˆuy

 δ feedback

(b) dual-teacher feedback

**Figure 2.** Schematic of the feedback mechanism. (a) Feedback is applied to each unit’s likelihood, leading to a uniform updating direction. (b) The dual-teacher framework enables the feedback more dynamic based on prediction conﬁdence.

the accurate direction (Yu et al. 2019; Luo et al. 2022b). Nonetheless, there is no way to verify if the updates induced by unlabeled data are aligned with those by labeled data.

Motivated by this fact, performance change of the student attributed to the update via pseudo labels is quantiﬁed on labeled data. Intriguingly, if performance improved, pseudo labels yielded by the teacher are favorable, prompting further enhancement of pseudo-labeling; otherwise, teacher should reduce the likelihood of yielding such labels. This creates a feedback mechanism within the teacher-student model. In formal, given θS, the performance on a labeled mini-batch D′ l ⊂Dl (with N ′ l = |D′ l|) is evaluated by

Ll(θS; D′ l) = 1

N ′ l

N ′ l X i ℓ f xl i; θS

, yl i

. (3)

Let θ′

S = θS −η∆θS represents the student with one-step update, where ∆θS = ∇θSLS(θS, θT; D′ u) is the stochastic gradient generated on an unlabeled mini-batch D′ u ⊂Du, and η is the step size. Then, feedback can be derived:

δ = Ll(θS) −Ll(θ′

S). (4) We drop D′ l from Ll for brevity. Let P (ˆyu|xu; θT, D′ u) represent the likelihood of the teacher generating pseudo-label as ˆyu on D′ u. The teacher minimizes the following feedback loss Lfb to reﬁne pseudo labels:

Lfb(θT; D′ u) = −δ log P (ˆyu|xu; θT, D′ u). (5) Correspondingly, when δ > 0, the teacher is guided to maximize the likelihood P; while, when δ < 0, the teacher is guided to reduce the likelihood.

Theoretically, the feedback δ is a ﬁrst-order approximation to the inner product of two gradients, i.e., ∆θS and ∇θSLl(θ′

S), contained by a meta-objective (Pham et al. 2021). This means that when δ > 0, the update induced by pseudo-labels aligns with the gradient direction implied by the supervised loss Ll; otherwise, the two gradients are in opposite directions. This meta-objective is in line with metacognitive intervention to address conﬁrmation bias in psychology (Rollwage et al. 2020). With this feedback mechanism, the teacher-student framework is equipped with inherent error-correcting abilities such that error accumulation can be circumvented.

27854

<!-- Page 4 -->

Dual-teacher feedback While the feedback loss Lfb provides signals for adjusting pseudo-labels ˆyu, it enforces a uniform update direction across all voxel predictions, potentially limiting its corrective capacity [Figure 2(a)]. To address this, we propose an enhanced feedback mechanism within a dual-teacher framework, which not only enriches feedback dynamics but also promotes mutual learning between teachers [Figure 2(b)]. To this end, two key components are identiﬁed from Lfb, namely the feedback attributor and receiver. Conceptually, the attributor refers to a set of pseudo-labels with which the student yields gradient for update, while the receiver indicates to which region feedback is applied to modulate the pseudo-labeling likelihood. In the following, the two components are speciﬁed in terms of the dual-teacher model.

Let φ, ψ denote the two teachers, and ˆyφu, ˆyψu be their predicted label by Eq. 1. Pseudo-labels are set to the consensus if agreement is achieved, and set to the higherconﬁdence label if predictions conﬂict:

ˆyu =

ˆyφu or equivalently ˆyψu, if ˆyφu = ˆyψu; arg maxc maxφ,ψ{f φ c, f ψ c }, if ˆyφu̸ = ˆyψu. (6)

This method is more likely to yield accurate pseudo-labels. Then, two types of feedback are quantiﬁed, induced by pseudo-labels of agreement and disagreement regions. We use ¯ya = {ˆyu|ˆyφu = ˆyψu}, ¯yd = {ˆyu|ˆyφu̸ = ˆyψu} to denote the attributor in terms of the agreement and disagreement region, respectively. Based on Eq. 4, we have δ¯y = Ll (θS) −Ll θS −η ∆¯yθS

∥∆¯yθS∥

. (7)

Here, ¯y ∈{¯ya, ¯yd}. ∆¯yθS is the gradient of LS w.r.t. θS induced by pseudo-labels ¯y. Without conﬂicts, we employ δa, δd, respectively, to simplify the notations δ¯ya, δ¯yd.

In our design, the agreement feedback δa is applied to the lower-conﬁdence side between φ and ψ. This is because when δa > 0, we would like to maximize the con- ﬁdence lower-bound of ˆyu; when δa < 0, the lower conﬁdence favors the easier occurrence of disagreement between two teachers. On the contrary, the disagreement feedback δd is applied to the higher-conﬁdence side. When δd > 0, the pseudo-label ˆyu should become more conﬁdent, while when δd < 0, ˆyu is more likely to ﬂip to the label predicted by the other teacher. With this idea, feedback receivers can be identiﬁed. Given a teacher θ ∈{φ, ψ}, and let ¯θ be the other, the receiver mask is deﬁned at ﬁrst by Mθ

¯y:= I h

ˆyθu ⋆ˆy¯θu, f θ

ˆyθu ⋄f ¯θ

ˆy ¯θu i

. I [·] is the indicator function. ⋆, ⋄are two comparative operators depended on ¯y; they are respectively replaced by =, < for ¯ya, while by̸ =, > for ¯yd. We can then deﬁne the receiver in terms of the feedback δ¯y as P

ˆyθu|xu; θ, Du, Mθ

¯y

, i.e., the pseudo-labeling likelihood of θ on Du after masking regions by Mθ

¯y. As a result, the dual-teacher feedback loss is formulated as

Ldf(θ) = −

X

¯y∈{¯ya,¯yd}

δ¯y log P

ˆyθu|xu; θ, Du, Mθ

¯y

. (8)

This design gives rise to two distinct yet coordinated types of feedback, each exhibiting greater dynamics by adapting

## Algorithm

1: DualFete in a stochastic training step

Input: Randomly sampled mini-batches of labeled data

D′ l ⊂Dl and unlabeled data D′ u ⊂Du. Models: Two teachers φ, ψ, and a student θS

1: Pseudo-label D′ u by φ, ψ, respectively. ▷[Eq. 1] 2: Get pseudo labels ˆyu and attributors ¯ya, ¯yd. ▷[Eq. 6] 3: Evaluate feedback δ¯ya, δ¯yd. ▷[Eq. 7]

4: Get receiver masks Mφ ¯ya, Mφ

¯yd, Mψ

¯ya, and Mψ

¯yd. 5: Compute dual-teacher feedback loss Ldf. ▷[Eq. 8] 6: Update θS by LS using D′ u and ˆyu. ▷[Eq. 2] 7: Update {φ, ψ} by LT (φ) + LT (ψ) using both D′ l and D′ u. ▷[Ldf and Eq. 9, 10] return φ, ψ, and θS to changes in prediction conﬁdence – thereby breaking the limits of uniform updates. Meanwhile, the individualized feedback not only helps prevent teachers from making consistent errors, but also fosters productive disagreement between them, enabling mutual improvement through crosssupervision [Eq. 10] (Qiao et al. 2018; Shen et al. 2023).

Holistic framework

In total, the training procedure for a stochastic step is presented in Algorithm 1. There exist differences in the training data and objectives between the teacher and the student. Student Model. The student updates its parameters only using Du with pseudo-label ˆyu yielded by the dual-teacher model [Eq. 6, Eq. 2]. Except for learning on Du, the student takes the duty of feeding back the performance change on labeled data Dl per-step of training [Eq. 7]. (Optionally) The student can be further ﬁne-tuned with Dl, particularly when the gap between Nl and Nu is relatively small. Dual-teacher Model. Feedback from the student alone cannot guarantee superior teachers; they need to improve themselves through both individual and mutual learning. Thus, in addition to Ldf, the teachers are fully-supervised on Dl and cross-supervised on Du. Speciﬁcally, given a teacher θ ∈{φ, ψ}, the objective is formulated as min θ LT (θ) = min θ Ll(θ) + Ldf(θ) + λLA cs(θ; ¯θ, A). (9)

Here, λ is a ramp-up weighted factor, and A is a strong augmentator [e.g., copy-paste (Ghiasi et al. 2021); colorjittor (Cubuk et al. 2020)]. Ll is the fully-supervised loss [Eq. 3], and the cross-supervised loss LA cs is deﬁned by

LA cs(θ; ¯θ, A) = 1 Nu

Nu X i ℓ f (A (xu i); θ), A

ˆy

¯θu

(10)

Here, ˆy¯θu is the pseudo-label yielded by the teacher ¯θ, and A(y) only operates positional transformations for the label y. In line with prior work, a conﬁdence threshold is employed to ﬁlter possibly unreliable targets (Yang et al. 2023; Huang et al. 2025). Besides, we use Lcs to refer crosssupervised loss without weak-to-strong consistency.

27855

<!-- Page 5 -->

## Methods

LA Pancreas BraTS 5% (4) 10% (8) 20% (16) 10% (6) 20% (12) 10% (25) 20% (50) Fully Supervise 52.55, 47.1 82.74, 13.4 86.96, 11.9 55.60, 45.3 72.38, 19.4 74.43, 37.1 80.16, 22.7 UA-MT [Y. (2019)] 82.26, 13.7 86.28, 18.7 88.74, 8.39 66.44, 17.0 76.10, 10.8 84.64, 10.5 85.32, 8.68 SASSNet [L. (2020)] 81.60, 16.2 85.22, 11.2 89.16, 8.95 68.97, 18.8 76.39, 11.1 84.73, 9.88 85.64, 9.17 DTC [L. (2021)] 81.25, 14.9 87.51, 8.23 89.52, 7.07 66.58, 15.5 76.27, 8.70 - - URPC [L. (2022b)] 82.48, 14.7 85.01, 15.4 88.74, 12.7 73.53, 22.6 80.02, 8.51 84.53, 9.79 85.38, 8.36 PS-MT [L. (2022b)] 88.49, 8.12 89.72, 6.94 90.02, 6.74 76.94, 13.1 80.74, 7.41 84.88, 9.93 85.91, 8.63 MC-Net+ [W. (2022a)] 83.59, 14.1 88.96, 7.93 91.07, 5.84 70.00, 16.0 80.59, 6.47 84.96, 9.45 86.02, 8.74 SS-Net [W. (2022b)] 86.33, 9.97 88.55, 7.49 89.28, 7.29 71.76, 17.6 78.98, 8.86 - - BCP [B. (2023)] 88.02, 7.90 89.62, 6.81 91.26, 5.76 73.83, 12.7 82.91, 6.43 85.14, 9.89 86.13, 8.99 UniMatch [Y. (2023)] - 89.04, 7.26 90.99, 6.07 - 82.35, 7.66 85.03, 9.50 85.84, 8.68 MutRel [S. (2024)] 87.20, 9.90 89.86, 6.91 91.02, 5.78 75.93, 9.07 81.53, 6.81 84.29, 9.57 85.47, 7.76 AD-MT [Z. (2024)] 89.63, 6.56 90.55, 5.81 - 80.21, 7.18 82.61, 4.94 - - TraCoCo [L. (2024)] - 89.86, 6.81 91.51, 5.63 79.22, 8.46 83.36, 7.34 85.71, 9.20 86.69, 8.04 DualFete [ours] 90.35, 6.42 91.28, 5.51 91.89, 5.24 81.99, 5.34 83.49, 4.76 86.13, 9.02 85.83, 8.12 DualFete w.ft. [ours] 90.22, 5.89 91.12, 5.44 91.91, 5.22 82.45, 5.96 83.85, 4.43 86.25, 8.94 86.46, 7.80

**Table 1.** Comparison with SOTAs on LA, Pancreas, and BraTS19 datasets. The best and second best results are highlighted.

GT DTC Ours MutRel SS-Net BCP TraCoCo

Pancreas LA

**Figure 3.** Visualizations of several methods (10% labels).

## Experiments

Experimental settings

Datasets. Experiments are conducted on LA (Xiong et al. 2021), Pancreas (Roth et al. 2015), and BraTS19 (Menze et al. 2014) datasets. We follow preprocessing steps and data split used in prior work (Yu et al. 2019; Li et al. 2020; Luo et al. 2021; Liu et al. 2024; Zhao et al. 2024). LA contains 100 MRIs, with 80 for training and 20 for testing. Three commonly used label-settings are involved, i.e., 5%, 10%, and 20%. Pancreas contains 82 CT scans, in which 62 for training and 20 for testing. Two label settings are used 10%, and 20%. BraTS contains 335 brain MRIs, with 250 for training, 25 for validation, and 60 for testing. Label settings are the same as the Pancreas dataset. DualFete details. We employ V-Net for LA and Pancreas, U-Net for BraTS, with the input size and evaluation protocol remaining the same as prior work (Liu et al. 2024). The SGD optimizer and data loading conﬁgurations are also in line with prior work (Wu et al. 2022b; Liu et al. 2024). We employ the Dice and cross-entropy combination as the segmentation loss while using cross-entropy loss to evaluate student performance on labeled data. The likelihood P is implemented as the cumulative product of per-voxel pseudolabeling probability. For LA, we employ normalized gradients in Eq. 7 while Pancreas and BraTS do not, as we experimentally ﬁnd it works better. Moreover, we ﬁnd that using likelihood of strong-augmented data can also be beneﬁcial in some cases. Performance is evaluated by Dice (%) and 95% Hausdorff distance (95HD, voxel), displayed on the left and right sides of each table cell, respectively.

Comparison with SOTAs

We ﬁrst compare DualFete with the fully supervision baseline (only with Dl) and various state-of-the-art methods, including: UA-MT (Yu et al. 2019), SASSNet (Li et al. 2020), DTC (Luo et al. 2021), URPC (Luo et al. 2022b), PS-MT (Liu et al. 2022b), MC-Net+ (Wu et al. 2022a), SS-Net (Wu et al. 2022b), BCP (Bai et al. 2023), Uni- Match (Yang et al. 2023), MutRel (Su et al. 2024), AD- MT (Zhao et al. 2024), and TraCoCo (Liu et al. 2024). The reported results of these methods are identical to those in Su et al. (2024), Zhao et al. (2024), and Liu et al. (2024) under the same settings. Our results are from the student, and we also report the ﬁne-tuned performance (DualFete w.ft.).

While recent state-of-the-art methods [AD-MT (Zhao et al. 2024), TraCoCo (Liu et al. 2024)] have made significant progress in SSMIS, our DualFete pushes these boundaries further. As shown in Table 1, DualFete outperforms existing approaches across nearly all benchmarks and label settings, even without ﬁne-tuning. Notably, on Pancreas with 10% labels, it achieves a +1.78% Dice improvement and 1.84-voxel 95HD reduction over previous best results [AD- MT (Zhao et al. 2024)]. This consistent outperformance suggests that our framework captures fundamental improvements beyond current teacher-student paradigms. The purely unlabeled training of the student model makes it possible to yield additional gains through ﬁne-tuning on labeled data. These gains are substantial in the 20% labeled data setting and on the more challenging Pancreas dataset. However, ﬁne-tuning on very limited data is susceptible to overﬁtting, e.g., on LA with 5% and 10% labels. Thus, DualFete has particular potential in label-scarce cases by using labeled data exclusively to guide pseudo-label updates toward correct di-

27856

<!-- Page 6 -->

(a) cs disag PL

(b) δa < 0 disag PL

(c) δd < 0 disag PL

(d) cs, δa < 0 disag PL

(e) cs, δd < 0 disag PL

(f) δa disag PL

(g) δd disag PL

(h) δa, δd disag PL disag PL disag PL disag PL disag PL disag PL disag PL disag PL disag PL

0 500 0.0

0.5

1.0 0.0

0.5

1.0

500 0 0 500 0 500 0 500 0 500 0 500 0 500

**Figure 4.** Disagreement between two teachers (disag) and the pseudo-label error (PL) [Eq. 6], measured by 1-Dice. We report results evaluated by training inputs (ﬁrst row) and by the testing set (last row), respectively. (LA, 10% labels).

rections, thereby avoiding the need for ﬁne-tuning and circumventing the overﬁtting issue. For the BraTS dataset, it is noteworthy that our DualFete shows some oscillations in terms of testing performance. We speculate that the validation set is prone to overﬁtting due to its relatively limited quantity (25 samples).

**Figure 3.** illustrates two challenging segmentation cases in the Pancreas and LA dataset. Our method shows the best alignments with the ground-truth masks, maintaining most spatial details, which suggests the improved generalizability.

Ablation studies

Qualitative analysis of DualFete. To investigate the effectiveness of DualFete, we pretrain a cross-supervised model (Ll + Lcs) for 6k steps and then experimentally impose different constraints with 0.5k extra steps. We evaluate the pseudo-label error and the disagreement between two teachers in the second stage.

Several ﬁndings can be summarized by Figure 4. (1) The cross-supervised loss Lcs forces consensus between the teachers but ampliﬁes errors, leading to consistently worse pseudo-labels [Figure 4(a)]. (2) The constraint of δa < 0 forces teachers to fully conﬂict with each other [Figure 4(b)], while Lcs enables them to resolve these con- ﬂicts while reducing pseudo-labeling errors [Figure 4(d)]. (3) The δd < 0 constraint induces pseudo-labeling oscillation between the teachers. In extreme cases, this creates collapsing dynamics where object boundaries predicted by the teachers are alternatively eroded, resulting in backgroundonly predictions ultimately. This collapse can be observed from the completely incorrect pseudo-labels yet relatively low disagreement [Figure 4(c,e)]. Nonetheless, the observation suggests that if the constraint is prevented from collapsing, it has the potential to avoid invariant pseudo-labels. (4) δd > 0 can foster disagreements by reinforcing pseudo-label conﬁdence [Figure 4(g)]. Since the student is trained from scratch, it generates predominantly positive feedback, which continually reinforces one teacher’s conﬁdence while relatively weakening the other. Ultimately, two teachers evolve complementary prediction behaviors. (5) The two types of feedback δa, δd collaboratively counteract degenerating cases found in (2)-(4) [Figure 4(h)].

These ﬁndings suggest that the two types of feedback op-

D.T. Att. Rec. A LA 20% Pancreas 20% × × × × 88.55, 8.58 77.18, 9.81 × ˆyu P × 89.63, 7.92 79.27, 9.90 √ ˆyu P × 89.83, 8.08 76.83, 12.2 √ ¯ya Pl × 90.34, 6.43 79.56, 8.38 √ ¯yd Ph × 90.35, 6.19 80.77, 8.22 √ ¯ya,d Ph,l × 87.69, 8.73 78.06, 8.77 √ ¯ya,d Pl,h × 90.89, 6.11 81.12, 7.74 × ˆyu P √ 89.12, 8.68 78.59, 8.68 √ ¯ya,d Pl,h

√ 90.14, 7.30 80.77, 7.89

**Table 2.** Quantitative analysis of DualFete. ˆyu is either from Eq. 1 or Eq. 6 depended on whether the dual-teacher model is introduced (ﬁrst column). In the second and third columns, ¯ya,d and Pl,h indicate that the update is triggerred by agreement/disagreement pseudo-labels, and feedback is applied correspondingly to the lower/higher conﬁdence side. A indicates whether P is from strong-augmented data.

erate in different manners, yet work synergistically in the dual-teacher model: they (1) generate productive prediction disagreements; (2) maintain pseudo-label accuracy while preventing error accumulation. Quantitative analysis of DualFete. We further explore the proposed feedback mechanism quantitatively, and results are shown in Table 2. Compared to the baseline teacher-student model (ﬁrst row), the feedback mechanism actively prompts the teacher to reﬁne pseudo-labels, yielding consistent student performance gains (2, 4, 5, and 7-th rows). The singleteacher framework relies solely on naive feedback, while the dual-teacher extension introduces two distinct and collaborative feedback types (δa and δd), each capable of operating independently while surpassing the baseline. This extension achieves signiﬁcant improvements over the singleteacher protocol, demonstrating the value of coordinated yet independent feedback dynamics. However, performance degrades markedly when feedback attributors and receivers are mismatched (3 and 6-th rows), highlighting the criticality of proper component alignment. Strong-augmented likelihoods here do not result in performance gains, as only when weakto-strong consistency is imposed can teacher models learn to handle such cases, which will be shown later.

27857

<!-- Page 7 -->

loss teacher Ep.1 (Dice) Ep.2 (Entropy×104)

+LA cs φ 78.42 ± 8.46 12.65 ± 2.45 ψ 80.51 ± 6.23 13.13 ± 2.82

+Ldf φ 57.40 ± 24.63 14.30 ± 2.77 ψ 54.38 ± 28.83 15.23 ± 2.93

**Table 3.** Experiments with either Ldf only or LA

cs only. Label setting: Pancreas 20%.

dataset loss 10% 20%

LA

Ll 86.82, 9.96 88.55, 8.58 +Lcs 88.37, 9.27 90.30, 6.80 +Lcs+Ldf 90.77, 6.19 91.66, 6.12 +LA cs 90.39, 7.03 91.10, 6.12 +LA cs+Ldf 91.28, 5.51 91.89, 5.24

Pancreas

Ll 70.81, 14.3 77.18, 9.81 +Lcs 75.39, 10.6 79.62, 6.84 +Lcs+Ldf 78.13, 7.71 80.92, 7.89 +LA cs 80.30, 6.06 82.17, 5.43 +LA cs+Ldf 81.99, 5.34 83.49, 4.76

**Table 4.** Ablation study of Ldf, Lcs, and LA

cs in the dualteacher framework. Results are evaluated by the student.

Cross-teacher supervision. We design two experiments to verify that the feedback loss Ldf operates distinctly from both consistency regularization and entropy minimization. Speciﬁcally, we train two dual-teacher frameworks under identical conﬁgurations but with different unsupervised constraints: one using only feedback loss Ldf, and the other employing cross-supervised loss LA cs. In Experiment 1 (Ep.1), each test sample is evaluated six times with different strong augmentations, and we report the mean and standard deviation of Dice scores. Experiment 2 (Ep.2) similarly conducts six evaluations per test sample, yet with dropout perturbations. We measure the mean and standard deviation of perimage entropy summation. Table 3 suggests two key insights of using Ldf alone: (1) it fails to maintain robustness against input perturbations, evidenced by signiﬁcant Dice degradation and high performance variance; (2) it increases prediction uncertainty, showing no reduction in output entropy.

For further validation, we conducted an ablation study examining the impact of relevant unsupervised constraints. As shown in Table 4, cross-supervision between the dual teachers produces superior student performance, indicating that the teachers generate higher-quality pseudo-labels through mutual learning [Lcs, LA cs]. This virtuous cycle is further ampliﬁed by student feedback [Ldf], which continuously improves teacher pseudo-labeling accuracy, thereby enabling progressive student performance gains.

We experiment with varying conﬁdence thresholds in cross-supervised loss LA cs [Eq. 10] and analyze the effect of the likelihood type used in the feedback loss Ldf [Eq. 8]. Figure 5 demonstrates that a 0.7 threshold achieves optimal performance across most scenarios, validating the importance of ﬁltering low-conﬁdence predictions, which are

W S W S W S W S

W S W S W S W S

0.5 0.7 0.9 0.6 0.8 0.5 0.7 0.9 0.6 0.8

90.4 91.0 5.4 7.0

91.4 91.8 5.2 6.0

80.2 81.6 5.1 7.3

81.2 82.8 4.5 7.5

Dice 95HD confidence threshold

LA (10%) LA (20%) Pancreas (10%) Pancreas (20%)

**Figure 5.** Tuning of conﬁdence threshold in LA

cs and strongaugmentation likelihood in Ldf (W: weak. S: strong).

## Method

Train (s/iter) Mem. (GB) Infer. (s/case) FullySup 0.15 5.15 1.93 AD-MT 0.67 7.26 1.93 TraCoCo 2.39 21.93 1.81 DualFete 2.28 10.25 1.91

**Table 5.** Training (time, memory) and inference (time) cost on the LA dataset with V-Net as the backbone.

possibly incorrect. More importantly, preventing converging to low-conﬁdence targets further ensures achieving expected performance using feedback loss, as it mostly modulates the likelihood of these easy-to-error targets, thereby circumventing error accumulation. Notably, strong-augmentation likelihood yields signiﬁcant improvements on the Pancreas 20% benchmark and also remains effective with lower thresholds. We hypothesize this occurs because teachers beneﬁt from additional low-conﬁdence supervision to better align the likelihood from strong and weak augmentations. Efﬁciency. The dual-teacher design is used only during training, while inference relies solely on the student. We consider the trade-off worthwhile between training cost and inference performance. As show in Table 5, our method achieves comparable inference speed (about 1.9 s/case with TITAN RTX) with superior accuracy (see in Table 1).

Conclusions

In this work, we revisit the teacher-student paradigm through the lens of feedback and propose a dual-teacher feedback model to address conﬁrmation bias in semi-supervised medical image segmentation. Our framework makes two key contributions: (1) an error-correcting feedback mechanism that mitigates error propagation, and (2) a collaborative architecture that integrates the student’s individualized feedback with mutual reﬁnement between teachers, thereby enhancing teaching effectiveness. The dual-teacher design strengthens feedback dynamics, enabling both productive disagreement between teachers and reduced error consistency, two essential factors for improving robustness under imperfect supervision. Extensive experiments on three benchmark datasets demonstrate consistent performance gains, with both quantitative metrics and qualitative analyses validating the effectiveness of our approach.

27858

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by the National Natural Science Foundation for Distinguished Young Scholar under Grant No.62025601, in part by the National Natural Science Foundation Regional Innovation and Development Joint Fund under Grant No.U24A20341, in part by Transformation of Tianfu Jincheng Laboratory under Grant No.2025ZH013, and in part by Sichuan Province Innovative Talent Funding Project for Postdoctoral Fellows under Grant No.BX202512.

## References

Arazo, E.; Ortego, D.; Albert, P.; O’Connor, N. E.; and McGuinness, K. 2020. Pseudo-Labeling and Conﬁrmation Bias in Deep Semi-Supervised Learning. In 2020 International Joint Conference on Neural Networks (IJCNN). IEEE. Bai, Y.; Chen, D.; Li, Q.; Shen, W.; and Wang, Y. 2023. Bidirectional copy-paste for semi-supervised medical image segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 11514–11524. Chapelle, O.; et al. 2009. Semi-supervised learning (chapelle, o. et al., eds.; 2006)[book reviews]. IEEE Transactions on Neural Networks, 20(3): 542–542. Chen, J.; Mei, J.; Li, X.; Lu, Y.; Yu, Q.; Wei, Q.; Luo, X.; Xie, Y.; Adeli, E.; Wang, Y.; et al. 2024. TransUNet: Rethinking the U-Net architecture design for medical image segmentation through the lens of transformers. Medical Image Analysis, 97: 103280. Chen, X.; Yuan, Y.; Zeng, G.; and Wang, J. 2021. Semisupervised semantic segmentation with cross pseudo supervision. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2613–2622. Chi, H.; Pang, J.; Zhang, B.; and Liu, W. 2024. Adaptive bidirectional displacement for semi-supervised medical image segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 4070– 4080. Cubuk, E. D.; Zoph, B.; Shlens, J.; and Le, Q. V. 2020. Randaugment: Practical automated data augmentation with a reduced search space. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition workshops, 702–703. Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; et al. 2020. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929. Ghiasi, G.; Cui, Y.; Srinivas, A.; Qian, R.; Lin, T.-Y.; Cubuk, E. D.; Le, Q. V.; and Zoph, B. 2021. Simple copy-paste is a strong data augmentation method for instance segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2918–2928. Grandvalet, Y.; and Bengio, Y. 2004. Semi-supervised learning by entropy minimization. Advances in neural information processing systems, 17. Hu, Y.; Yang, J.; Chen, L.; Li, K.; Sima, C.; Zhu, X.; Chai, S.; Du, S.; Lin, T.; Wang, W.; et al. 2023. Planning-oriented autonomous driving. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 17853– 17862. Huang, W.; Zhang, L.; Wang, Z.; and Wang, L. 2024. Exploring inherent consistency for semi-supervised anatomical structure segmentation in medical imaging. IEEE Transactions on Medical Imaging. Huang, W.; Zhang, L.; Wang, Z.; and Wang, Y. 2025. Gap- Match: Bridging Instance and Model Perturbations for Enhanced Semi-Supervised Medical Image Segmentation. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, 17458–17466. Ke, Z.; Wang, D.; Yan, Q.; Ren, J.; and Lau, R. W. 2019. Dual student: Breaking the limits of the teacher in semisupervised learning. In Proceedings of the IEEE/CVF international conference on computer vision, 6728–6736. Lan, T.; Chen, N.; Yi, Z.; Xu, X.; and Zhu, M. 2025a. Domain Generalization for Pulmonary Nodule Detection via Distributionally-Regularized Mamba. In International Conference on Medical Image Computing and Computer- Assisted Intervention, 152–162. Springer. Lan, T.; Yi, Z.; Xu, X.; and Zhu, M. 2025b. LooBox: Loose-box-supervised 3D Tumor Segmentation with Selfcorrecting Bidirectional Learning. In Proceedings of the 33rd ACM International Conference on Multimedia, 8077– 8086. Li, S.; Qi, L.; Yu, Q.; Huo, J.; Shi, Y.; and Gao, Y. 2025. Stitching, ﬁne-tuning, re-training: A sam-enabled framework for semi-supervised 3d medical image segmentation. IEEE Transactions on Medical Imaging. Li, S.; et al. 2020. Shape-aware semi-supervised 3D semantic segmentation for medical images. In International Conference on Medical Image Computing and Computer- Assisted Intervention, 552–561. Springer. Liu, F.; Tian, Y.; Chen, Y.; Liu, Y.; Belagiannis, V.; and Carneiro, G. 2022a. Acpl: Anti-curriculum pseudo-labelling for semi-supervised medical image classiﬁcation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 20697–20706. Liu, Y.; Tian, Y.; Chen, Y.; Liu, F.; Belagiannis, V.; and Carneiro, G. 2022b. Perturbed and strict mean teachers for semi-supervised semantic segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 4258–4267. Liu, Y.; Tian, Y.; Wang, C.; Chen, Y.; Liu, F.; Belagiannis, V.; and Carneiro, G. 2024. Translation consistent semisupervised segmentation for 3d medical images. IEEE Transactions on Medical Imaging. Luo, X.; Chen, J.; Song, T.; and Wang, G. 2021. Semisupervised medical image segmentation through dual-task consistency. In Proceedings of the AAAI conference on arti- ﬁcial intelligence, volume 35, 8801–8809. Luo, X.; Hu, M.; Song, T.; Wang, G.; and Zhang, S. 2022a. Semi-supervised medical image segmentation via cross teaching between cnn and transformer. In International conference on medical imaging with deep learning, 820–833. PMLR.

27859

<!-- Page 9 -->

Luo, X.; Wang, G.; Liao, W.; Chen, J.; Song, T.; Chen, Y.; Zhang, S.; Metaxas, D. N.; and Zhang, S. 2022b. Semisupervised medical image segmentation via uncertainty rectiﬁed pyramid consistency. Medical Image Analysis, 80: 102517. Menze, B. H.; Jakab, A.; Bauer, S.; et al. 2014. The multimodal brain tumor image segmentation benchmark (BRATS). IEEE transactions on medical imaging, 34(10): 1993–2024. Nickerson, R. S. 1998. Conﬁrmation bias: A ubiquitous phenomenon in many guises. Review of general psychology, 2(2): 175–220. Pham, H.; Dai, Z.; Xie, Q.; and Le, Q. V. 2021. Meta pseudo labels. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 11557–11568. Qiao, S.; Shen, W.; Zhang, Z.; Wang, B.; and Yuille, A. 2018. Deep co-training for semi-supervised image recognition. In Proceedings of the european conference on computer vision (eccv), 135–152. Rollwage, M.; Loosen, A.; Hauser, T. U.; Moran, R.; Dolan, R. J.; and Fleming, S. M. 2020. Conﬁdence drives a neural conﬁrmation bias. Nature communications, 11(1): 2634. Roth, H. R.; Lu, L.; Farag, A.; et al. 2015. Deeporgan: Multilevel deep convolutional networks for automated pancreas segmentation. In Medical Image Computing and Computer- Assisted Intervention–MICCAI 2015, 556–564. Springer. Shen, Z.; Cao, P.; Yang, H.; et al. 2023. Co-training with high-conﬁdence pseudo labels for semi-supervised medical image segmentation. In Proceedings of the Thirty-Second International Joint Conference on Artiﬁcial Intelligence, 4199–4207. Shi, Y.; Zhang, J.; Ling, T.; Lu, J.; Zheng, Y.; Yu, Q.; Qi, L.; and Gao, Y. 2021. Inconsistency-aware uncertainty estimation for semi-supervised medical image segmentation. IEEE transactions on medical imaging, 41(3): 608–620. Su, J.; Luo, Z.; Lian, S.; Lin, D.; and Li, S. 2024. Mutual learning with reliable pseudo label for semi-supervised medical image segmentation. Medical Image Analysis, 94: 103111. Tarvainen, A.; and Valpola, H. 2017. Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. Advances in neural information processing systems, 30. Wang, Y.; Xiao, B.; Bi, X.; Li, W.; and Gao, X. 2023. Mcf: Mutual correction framework for semi-supervised medical image segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 15651– 15660. Wu, H.; Li, X.; Lin, Y.; and Cheng, K.-T. 2023. Compete to win: Enhancing pseudo labels for barely-supervised medical image segmentation. IEEE Transactions on Medical Imaging, 42(11): 3244–3255. Wu, Y.; Ge, Z.; Zhang, D.; Xu, M.; Zhang, L.; Xia, Y.; and Cai, J. 2022a. Mutual consistency learning for semisupervised medical image segmentation. Medical Image Analysis, 81: 102530.

Wu, Y.; Wu, Z.; Wu, Q.; Ge, Z.; and Cai, J. 2022b. Exploring Smoothness and Class-Separation for Semi-supervised Medical Image Segmentation. In International Conference on Medical Image Computing and Computer-Assisted Intervention, volume 13435, 34–43. Springer, Cham. Xiong, Z.; Xia, Q.; Hu, Z.; Huang, N.; et al. 2021. A global benchmark of algorithms for segmenting the left atrium from late gadolinium-enhanced cardiac magnetic resonance imaging. Medical image analysis, 67: 101832. Xu, Z.; Wang, Y.; Lu, D.; Luo, X.; Yan, J.; Zheng, Y.; and Tong, R. K.-y. 2023. Ambiguity-selective consistency regularization for mean-teacher semi-supervised medical image segmentation. Medical Image Analysis, 88: 102880. Yang, L.; Qi, L.; Feng, L.; Zhang, W.; and Shi, Y. 2023. Revisiting weak-to-strong consistency in semi-supervised semantic segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 7236– 7246. Yi, L.; Zhang, L.; Zhao, K.; and Xu, X. 2025. Learning from certain regions of interest in medical images via probabilistic positive-unlabeled networks. Medical Image Analysis, 103745. Yu, L.; Wang, S.; Li, X.; Fu, C.-W.; and Heng, P.-A. 2019. Uncertainty-aware self-ensembling model for semisupervised 3D left atrium segmentation. In Medical image computing and computer assisted intervention–MICCAI 2019, 605–613. Springer. Zhang, H.; Cisse, M.; Dauphin, Y. N.; and Lopez-Paz, D. 2018. mixup: Beyond Empirical Risk Minimization. In International Conference on Learning Representations. Zhao, Z.; Wang, Z.; Wang, L.; Yu, D.; Yuan, Y.; and Zhou, L. 2024. Alternate diverse teaching for semi-supervised medical image segmentation. In European Conference on Computer Vision, 227–243. Springer.

27860
