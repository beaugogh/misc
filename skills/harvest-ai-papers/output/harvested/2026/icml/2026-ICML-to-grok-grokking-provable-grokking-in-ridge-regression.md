---
title: "To Grok Grokking: Provable Grokking in Ridge Regression"
source_url: https://icml.cc/virtual/2026/oral/71134
paper_pdf_url: https://arxiv.org/pdf/2601.19791v4
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# To Grok Grokking: Provable Grokking in Ridge Regression

<!-- Page 1 -->

To Grok Grokking: Provable Grokking in Ridge Regression

Mingyue Xu 1 Gal Vardi 2 Itay Safran 3

## Abstract

We study grokking—the onset of generalization long after overfitting—in a classical ridge regression setting. We prove end-to-end grokking results for learning over-parameterized linear regression models using gradient descent with weight decay. Specifically, we prove that the following stages occur: (i) the model overfits the training data early during training; (ii) poor generalization persists long after overfitting has manifested; and (iii) the generalization error eventually becomes arbitrarily small. Moreover, we show, both theoretically and empirically, that grokking can be amplified or eliminated in a principled manner through proper hyperparameter tuning. To the best of our knowledge, these are the first rigorous quantitative bounds on the generalization delay (which we refer to as the “grokking time”) in terms of training hyperparameters. Lastly, going beyond the linear setting, we empirically demonstrate that our quantitative bounds also capture the behavior of grokking on non-linear neural networks. Our results suggest that grokking is not an inherent failure mode of deep learning, but rather a consequence of specific training conditions, and thus does not require fundamental changes to the model architecture or learning algorithm to avoid.

## 1. Introduction

By the standard of classical machine learning, overfitting the training data is usually believed to be harmful to generalization. To overcome this, regularization techniques such as early-stopping, dropout and weight decay have been developed. However, deep learning can sometimes exhibit

1Department of Computer Science, Purdue University, West Lafayette, IN, USA 2Department of Computer Science and Applied Mathematics, Weizmann Institute of Science, Israel 3Stein Faculty of Computer and Information Science, Ben-Gurion University of the Negev, Israel. Correspondence to: Mingyue Xu <xu1864@purdue.edu>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

counterintuitive phenomena that contravene this traditional wisdom. One of the most striking examples is “grokking” (Power et al., 2022), a phenomenon where generalization only starts improving long after the model achieves perfect training performance. The phenomenon of grokking has been extensively studied in recent years (Chughtai et al., 2023; Tan & Huang, 2023; Notsawo Jr et al., 2023; Fan et al., 2024), and was also encountered in models that are different from neural networks (Blanc et al., 2020; Humayun et al., 2024; Merrill et al., 2023), as well as in large language models (Zhu et al., 2024; Wang et al., 2024; Xu et al., 2025) (see Subsection 1.1 for further discussion). But despite its increasing popularity, only a few prior works have established rigorous theoretical guarantees.

Several existing theoretical papers attribute the occurrence of grokking to a transition in the optimization dynamics from the lazy to the rich regime (Lyu et al., 2024; Mohamadi et al., 2024; Kumar et al., 2024). Among these works, Lyu et al. (2024) consider training homogeneous neural networks for both classification and regression problems using gradient flow with weight decay, and prove a sharp transition between the kernel and rich regimes. However, their technique only guarantees convergence to a KKT (Karush-Kuhn-Tucker) point, which is, in general, not sufficient for arguing global optimality, and their result does not provably imply grokking. In another work, Mohamadi et al. (2024) provide a theoretical foundation for grokking on the specific regression problem of modular addition. They consider training two-layer quadratic networks with an ℓ∞ regularization, and show that grokking is a consequence of the transition from kernel-like behavior to the limiting behavior of gradient descent (GD). Yet, their analysis does not establish that GD converges to a solution with a small weight norm that generalizes well, despite empirically verifying this. To the best of our knowledge, the work closest to showing a provable grokking result is Xu et al. (2024). By studying a high-dimensional clustered XOR dataset in a binary classification setting, they show that after a catastrophic one-step overfitting—where generalization is no better than a random guess—the model eventually achieves perfect test accuracy. Still, they do not show that the onset of generalization is delayed beyond the first iteration of GD, which could begin as early as the second iteration. While many prior works attribute grokking to the transition arXiv:2601.19791v4 [cs.LG] 16 Jul 2026

<!-- Page 2 -->

Provable Grokking in Ridge Regression between the lazy and rich regimes during optimization, a recent work by Boursier et al. (2025) focused specifically on studying the role of weight decay in grokking, revealing that grokking can also arise from the transition between the “ridgeless” to the “ridge” regimes. They considered training using gradient flow with weight decay on a smooth loss objective and showed a two-phase behavior of the trajectory. Nevertheless, they do not prove that the unregularized solution does not generalize and the ridge solution does generalize, and thus their results do not imply provable grokking. Relatedly, Tikeng Notsawo et al. (2025) study a general loss-plus-regularizer framework, showing an early loss-minimization phase followed by a regularization-driven phase on a time scale proportional to 1/(ηλ). Our work provides sharper end-to-end guarantees in the specific setting of ridge regression.

Given the current theoretical gaps around grokking, our goal is to prove an end-to-end grokking guarantee demonstrating that: (i) the model overfits early, while test performance remains poor; (ii) poor generalization persists long after overfitting; and (iii) the optimization algorithm eventually converges to a model that achieves good generalization. See Figure 1 for an illustration. To this end, we investigate the phenomenon of grokking within a classical teacher-student framework. We specifically consider linear regression, a classical statistical method that has been extensively studied over the centuries (Galton, 1886; Tikhonov, 1963; Hoerl & Kennard, 1970; Uyanık & G¨uler, 2013). To address overfitting, fundamental regularization techniques such as Lasso and ridge regression have been developed and proven invaluable. Despite being a special case of overfitting, it is surprising that almost no previous work has focused on grokking in linear regression. While prior work has observed this phenomenon mainly in complex, non-linear architectures, our findings reveal that neither deep nor non-linear structural components are strictly necessary for grokking to occur, offering a rigorous, foundational framework for the phenomenon in purely linear settings. To our best knowledge, the only theoretical work on this topic is Levi et al. (2024), in which the authors analyze grokking in a linear regression setting by leveraging random matrix theory. Yet, despite the similar setting being studied, their analysis lacks formal guarantees. Apart from the fact that the results are non-rigorous, their work differs from ours in the following aspects. (1) They assume only Gaussian data, whereas our data distribution is more general; (2) their results consider the regimes where the feature dimension roughly equals the sample size, while we allow arbitrary over-parameterization; and (3) they do not include weight decay as we do.

In this paper, we consider an over-parameterized linear regression problem of learning a ground-truth realizable teacher function, by training a student linear model using randomly initialized GD, on a squared loss objective, and

**Figure 1.** Comparing training and test squared losses using GD with weight decay over 50 independent runs (with independent datasets and student initializations). Left: training a ridge regression model to learn the zero teacher; Right: training a twolayer ReLU neural network (training both layers) to learn the zero teacher. We scale the x-axis logarithmically, which is commonly adopted for plotting the grokking phenomenon (Power et al., 2022; Lyu et al., 2024; Xu et al., 2024; Mohamadi et al., 2024). See Section 5 for further details of the experimental setup.

with an ℓ2 regularization. We provide the first end-to-end provable grokking result, and unlike Xu et al. (2024), we are able to prove that poor generalization persists beyond the point where we overfit. Our results hold for a family of teacher functions: any function that is realizable by a linear model over any fixed feature map. Moreover, we also demonstrate, both theoretically and empirically, that grokking can be fully and quantitatively controlled by hyperparameter tuning. Specifically, one way to effectively manipulate the delay before generalization begins is to tune the weight decay, which aligns with the empirical findings of Lyu et al. (2024). To summarize the main novelty in this work, for the first time, (1) we show an end-to-end provable grokking result, while all prior works on grokking in neural networks or linear models did not establish such a comprehensive result; (2) we give a formal analysis of grokking in the fundamental setting of linear/ridge regression; and (3), we provide exact quantitative bounds on the grokking time that reveal how each hyperparameter affects grokking.

In a bit more detail, our main contributions are as follows:

• We study an over-parameterized ridge regression problem (Section 4), and show the first end-to-end provable grokking result (Theorem 4.2) for learning any realizable teacher function using gradient descent. Specifically, we prove the following separate components:

– We prove that when optimizing the ℓ2 regularized squared loss using gradient descent, the training (empirical) squared error decays at a fast convergence rate (Theorem 4.4). – We provide a lower bound for the generalization error which admits a slower convergence rate than the one for the training error, implying long-term overfitting (Theorem 4.5). – Lastly, we show that gradient descent will eventu- ally reach a global minimum with a generalization guarantee (Theorem 4.6).

![Figure extracted from page 2](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

Provable Grokking in Ridge Regression

• We quantitatively state the sufficient conditions of the hyperparameters to realize grokking (Equations (3), (4) and (5)) and provide a rigorous lower bound on the grokking time in terms of model hyperparameters (Equations (6) and (7)). We then analyze how different hyperparameters affect grokking, which is in keeping with our experimental verifications. • We support our theoretical findings with empirical simulations that illustrate how grokking can be controlled in a principled manner (Section 5). • Finally, we conduct experiments on non-linear neural networks, and demonstrate empirically that the dependencies of the grokking time on hyperparameters qualitatively match our provable predictions in linear regression.

## 1.1. Additional Related Work

The intriguing phenomenon of grokking was first coined by Power et al. (2022), who observed it when training on algorithmic datasets for modular addition. However, the underlying behavior—where generalization emerges long after overfitting—had already been noted in earlier work by Blanc et al. (2020), in the context of matrix sensing and simplified shallow neural networks. Following these seminal works, grokking has also been observed in other learning paradigms, which include learning sparse parities (Barak et al., 2022; Merrill et al., 2023), learning the greatest common divisor of integers (Charton, 2024), and image classification (Radhakrishnan et al., 2022).

Several works proposed thoughtful ideas to explain grokking, although none of them provided rigorous endto-end grokking results. Liu et al. (2022) offered an explanation via the lens of representation learning. Thilak et al. (2022) attributed grokking to the use of adaptive optimizers—an optimization anomaly named the “Slingshot Mechanism” (cyclic phase transitions). Liu et al. (2023) identified a mismatch between training and test loss landscapes, which they called the “LU mechanism”, and used it to explain certain aspects of grokking. Nanda et al. (2023) revealed that grokking can arise from the gradual amplification of structured mechanisms encoded in the weights via progress measuring. Davies et al. (2023) hypothesized that grokking and double descent can be understood using the same pattern-learning model, and provided the first demonstration of model-wise grokking. Merrill et al. (2023) studied the problem of training two-layer neural networks on a sparse parity task, and attributed grokking therein to the competition between dense and sparse subnetworks. Gromov (2023) demonstrated that fully-connected two-layer networks exhibit grokking on modular arithmetic tasks without any regularization and attributed grokking to feature learning. Miller et al. (2024) studied grokking beyond neural networks, e.g. Bayesian models. Beck et al. (2025) ex- plored the phenomenon of grokking in a logistic regression problem. They provided evidence that grokking may occur under some asymptotic assumptions on the hyperparameters, but they did not rigorously prove grokking. Varma et al. (2023) interpreted grokking from the perspective of circuit efficiency, and discovered two related phenomena named “ungrokking” and “semi-grokking”. Jeffares et al. (2024)

provided empirical insights into grokking, by investigating a telescoping model that suggests that grokking may reflect a transition to a measurably benign overfitting regime during training. Humayun et al. (2024) attributed grokking of deep neural networks to their delayed robustness. Prieto et al. (2025) demonstrated the dependence of grokking on regularization by showing that Softmax Collapse (i.e. floating point errors due to numerical instability) is responsible for the absence of grokking without regularization. We note that in addition to Prieto et al. (2025), several other papers considered grokking without explicit regularization (e.g., Xu et al. (2024); Levi et al. (2024)), but the grokking literature mostly focuses on settings with explicit regularization, as in this paper. Mallinar et al. (2025) revealed that grokking is not specific to neural networks nor to GD-based optimization methods by showing that grokking occurs when learning modular arithmetic with Recursive Feature Machines (RFM). ˇZunkoviˇc & Ilievski (2024) analyzed grokking in linear classification, and showed quantitative bounds on the grokking time, but they did not provide rigorous proofs. Yunis et al. (2024) showed empirically that grokking is con- nected to rank minimization, namely, that the sudden drop in the test loss coincides precisely with the onset of lowrank behavior in the singular values of the weight matrices. Jeffares & van der Schaar (2025) argue that the settings in which grokking and other counterintuitive phenomena in deep learning can be shown to occur are limited in practice, as they may only appear in very specific situations.

## 1.2. Organization

The remaining of the paper is organized as follows. In Section 2, we formally describe the problem setup and introduce necessary notations. In Section 3, we provide an informal theorem to convey our main results in an accessible manner. In Section 4, we present our main results of end-to-end provable grokking in ridge regression. In Section 5, we support our theory with empirical verifications. In Section 6, we conclude the paper and propose some interesting future research directions. All proofs and additional experiments are deferred to the appendix.

## 2. Preliminaries

Notations. We use bold-face letters to denote vectors such as x = (x1,..., xd) ∈Rd and use bold-face capital letters to denote matrices such as X = (x1,..., xn)⊤∈Rn×d.

<!-- Page 4 -->

Provable Grokking in Ridge Regression

We denote by Id the d-dimensional identity matrix. For a vector x, we denote by ∥x∥2 its ℓ2 norm. For a matrix X, we denote by ∥X∥op and ∥X∥F its operator and Frobenius norms, respectively. For a symmetric matrix A, let λmin(A) and λ+ min(A) denote its smallest eigenvalue and its smallest positive eigenvalue, respectively. We use 1{·} to denote the indicator function, which equals one when its Boolean input is true and zero otherwise. We use standard asymptotic notations O(·) and Ω(·) to hide numerical constant factors.

Linear regression and data generation. We consider a fundamental regression problem of learning a teacher function N ∗(x) where x ∈Rd. The training data {(xi, yi)}n i=1 ⊆ Rd × R are generated according to the following: the input x ∼Dx follows some marginal distribution Dx (which we do not specify), and is exactly labeled by the teacher function, i.e. y = N ∗(x). We train a student linear regression model

N(x; θ) = ⟨θ, ϕ(x)⟩, where ϕ(x): Rd 7→Rm is some fixed feature map and θ ∈Rm is the trainable parameters, to learn the teacher. We assume that the teacher is realizable, i.e., N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm.

Ridge regression. In a regression problem, it is natural to train the model by minimizing the empirical mean squared loss 1 n

Pn i=1(N(xi; θ) −N ∗(xi))2 and evaluate the learning performance on the population squared loss Ex[(N(x; θ) −N ∗(x))2]. We use ridge regression by appending an ℓ2-regularization term to the loss function. Let Ln(θ; λ) denote the regularized mean squared training error, let Ln(θ) denote the unregularized mean squared loss, and let Lλ(θ) denote the ℓ2 penalty. Our training objective is

Ln(θ; λ) = Ln(θ) + Lλ(θ)

= 1

2n n X i=1

(N(xi; θ) −N ∗(xi))2 + λ

2 ∥θ∥2 2, (1)

where λ > 0 is the regularization parameter. We scale the loss objective by a constant factor of 1/2 for the simplicity of gradient analysis. We optimize Equation (1) using the vanilla Gradient Descent (GD) algorithm, which updates θ via θ(t+1) = θ(t) −η∇θLn(θ(t); λ), ∀t ∈N, where η > 0 is the step-size or learning rate. While we focus on GD with a fixed step size, we note that our analysis should also hold for GD with a decaying step size and for gradient flow.

When N(x; θ) = ⟨θ, ϕ(x)⟩and N ∗(x) = ⟨θ∗, ϕ(x)⟩, our loss objective in Equation (1) can be simplified to

Ln(θ; λ) = 1

2n n X i=1

(⟨θ −θ∗, ϕ(x)⟩)2 + λ

2 ∥θ∥2 2, and each GD iteration realizes an update in the form of θ(t+1) = θ(t) −η∇θLn(θ(t); λ)

= θ(t) −η n n X i=1

D θ(t) −θ∗, ϕ(xi)

E ϕ(xi) −ηλθ(t) (2)

To present our results, we introduce the following additional notations. Let L(θ) = Ex[(N(x; θ) −N ∗(x))2] denote the generalization (population) squared loss. We define the empirical feature map as Φ = (ϕ(x1),..., ϕ(xn))⊤∈ Rn×m. Let L = 1 n∥Φ∥2

F = 1 n

Pn i=1 ∥ϕ(xi)∥2

2 denote the (average) norm of the feature vectors. Let Σ = Ex[ϕ(x)ϕ(x)⊤] ∈Rm×m denote the feature population covariance matrix.

## 3. Informal Results

To demonstrate a clear manifestation of grokking, our main theorem is formulated as follows: GD achieves a training error smaller than ϵ > 0 in an early stage of training (at step t1), while a poor generalization error well above some constant c > 0 persists far beyond the point of overfitting (until step t2 > t1), yet eventually a generalization error smaller than ϵ is reached. In particular, this establishes grokking when c ≥ϵ. Our results give a lower bound on (t2 −t1) in terms of both ϵ and c, where this difference can be made arbitrarily large via proper hyperparameter tuning for any choice of ϵ and c ≥ϵ. Specifically, let t1 be the largest number of training steps such that the empirical squared loss is above ϵ, and let t2 be the smallest number of training steps for which the generalization loss is below c. Our main results are summarized by the following informal theorem, establishing end-to-end provable grokking in ridge regression. Informal Theorem (End-to-end provable grokking for ridge regression). Consider a linear regression problem of training a student model N(x; θ) = ⟨θ, ϕ(x)⟩to learn a realizable teacher N ∗(x) = ⟨θ∗, ϕ(x)⟩, where θ ∈Rm is the trainable parameter and θ∗is unknown. Suppose that the training is done by optimizing an MSE over n samples using randomly initialized gradient descent at θ(0) with weight decay parameter λ.

Under the initialization θ(0) ∼N(0, ν2Im) for some ν2 > 0, and some mild distributional assumptions on the feature map ϕ(x), we have with high probability that for a sufficiently large sample size n, and a sufficiently large feature space dimensionality m, (t2−t1) can be lower bounded by an arbitrarily large value by choosing a sufficiently small weight decay λ.

## 4. Grokking in Ridge Regression

We now formalize our end-to-end provable grokking results for ridge regression problems. For any realizable teacher

<!-- Page 5 -->

Provable Grokking in Ridge Regression function, we provide a quantitative lower bound for the grokking time (t2 −t1) in terms of training hyperparameters, as well as bounds on the hyperparameters that suffice to realize grokking. Based on these bounds, we analyze how the different hyperparameters affect grokking, which is corroborated in our experiments in Section 5.

## 4.1. Warmup: Grokking with the Zero Teacher

We start by considering a simple scenario where the target teacher is the zero function. When N ∗(x) = 0, we have

Ln(θ; λ) = 1

2n n X i=1

(N(xi; θ))2 + λ

2 ∥θ∥2 2;

θ(t+1) = θ(t) −η n n X i=1

⟨θ(t), ϕ(xi)⟩ϕ(xi) −ηλθ(t).

The following theorem describes an end-to-end provable grokking result for learning the zero teacher in a ridge regression setting using gradient descent. To develop some initial intuition on what causes grokking, we state the aforementioned three stages of grokking in terms of the convergence rates of the training/generalization squared losses, in contrast to the format of our Theorem 4.2 which appears later.

Theorem 4.1 (End-to-end provable grokking for the zero teacher). Suppose that the teacher function is N ∗(x) = 0. Consider training a student N(x; θ) = ⟨θ, ϕ(x)⟩to learn the teacher via optimizing the ridge regression objective in Equation (1) using randomly initialized GD with θ(0) ∼ N(0, ν2Im). Assume that η ≤2/(L + 2λ). Then for any t ∈N, we have

(i) Ln(θ(t)) ≤L

2 ·(1−1 nηλ+ min(Φ⊤Φ)−ηλ)2t ·∥θ(0)∥2

2; (ii) With probability at least 1 −2e−(m−n)/32,

L(θ(t)) ≥λmin(Σ) · (1 −ηλ)2t · (m−n)ν2

2; (iii) ∥θ(t)∥2

2 ≤(1 −ηλ)2t · ∥θ(0)∥2 2.

Studying the zero teacher as a warmup yields the following advantages. First, choosing the zero teacher enables us to build a much simpler generalization guarantee. Clearly, item (iii) above implies that GD eventually converges to the solution θ∗= 0. Since N ∗(x) = 0, this yields generalization. Additionally, choosing the zero teacher allows us to derive matching lower (ii) and upper (iii) bounds for the generalization loss in terms of the convergence rate.

More importantly, Theorem 4.1 reveals that the training and test losses can decrease at different rates, and the potentially considerable discrepancy between these rates causes grokking. Specifically, given the empirical feature map Φ⊤Φ, a sufficiently small regularization λ can only have a negligible effect on the convergence rate of the training MSE. This is because the convergence rate of (1 −1 nηλ+ min(Φ⊤Φ) −ηλ)2t will be dominated by the term (1 −1 nηλ+ min(Φ⊤Φ))2t when λ is sufficiently small. However, decreasing λ can make the generalization convergence rate (1 −ηλ)2t arbitrarily slow. In conclusion, Theorem 4.1 establishes a provable instance of grokking whenever m ≫n, λ ≪1 nλ+ min(Φ⊤Φ) and λ →0.

## 4.2. Grokking with Realizable Teachers

For the most general setting studied in this paper, we consider the realizable case where the ground-truth teacher is N ∗(x) = ⟨θ∗, ϕ(x)⟩for some unknown θ∗∈Rm, and the student is N(x; θ) = ⟨θ, ϕ(x)⟩where θ ∈Rm is the vector of trainable parameters. We show that for any teacher, there is a realization of training hyperparameters that results in an arbitrarily long grokking time. Our main result is the following. Theorem 4.2 (End-to-end provable grokking for realizable ridge regression). Assume a realizable teacher function N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume the boundedness of the feature map, i.e. ∥ϕ(x)∥2 ≤b for any x and some b > 0. Consider training a student N(x; θ) = ⟨θ, ϕ(x)⟩to learn the teacher via optimizing the ridge regression objective in Equation (1) using randomly initialized GD with θ(0) ∼N(0, ν2Im). For all ϵ > 0, let c ≥ϵ be arbitrary. We define t1:= t1(ϵ):= max n t ∈N: Ln(θ(t)) ≥ϵ o and t2:= t2(c):= min n t ∈N: L(θ(t)) ≤c o

.

For any δ ∈(0, 1), assume a sufficiently large sample size:

n = Ω b4∥θ∗∥4

2 ϵ2 log

1 δ

, (3)

a sufficiently large dimensionality of the feature map:

m = n + Ω max log

1 δ

, ∥θ∗∥2

2 ν2, c λmin(Σ)ν2

,

(4) and finally, a sufficiently small weight decay:

λ = O min ϵ ∥θ∗∥2

2, b√ϵ

∥θ∗∥2

. (5)

Then, if η < 1/(λ + b2), we have with probability at least 1 −δ that t1 ≤ n ln

6b2∥θ(0)∥2 2 ϵ

2ηλ+ min(Φ⊤Φ) (6)

and t2 ≥ ln

(m−n)ν2

2 q c λmin(Σ) + ∥θ∗∥2

−2!

4ηλ. (7)

<!-- Page 6 -->

Provable Grokking in Ridge Regression

Moreover, L(θ(t)) ≤ϵ for all sufficiently large t.

The main intuition behind this discrepancy between t1 and t2 can be explained as follows: When the student regression model is sufficiently over-parameterized (m ≫n), we are solving a high-dimensional regression problem. Therefore, when the weight decay λ is small, the GD optimization process only effectively updates the projection of the weight vector θ∥onto the data-spanning subspace to fit the training data, while having negligible effect on the component θ⊥ in the complementary subspace, which remains close to its initialization. This occurs since the information captured by the data only contributes to the convergence of θ∥at a rate of (1 −1 nηλ+ min(Φ⊤Φ) −ηλ)t. In contrast, θ⊥converges at a negligible rate of (1 −ηλ)t as a consequence of longterm weight decay. Such an imbalanced trajectory prevents timely generalization and leads to harmful overfitting. As a remedy, weight decay plays a crucial role in decreasing the complexity of the model class, which eventually guarantees uniform convergence and thus good generalization.

Next, we disentangle the influence of individual hyperparameters on the grokking time according to our theory, which aligns closely with our experimental results in Section 5. Notably, these functional dependencies on the hyperparameters are not only qualitatively corroborated by our experiments, but they also quantitatively predict the expected scaling rates (see Figure 2).

Evidently, Equations (6) and (7) together provide strong control of the grokking time (t2 −t1), which reveals the following effects of hyperparameter tuning on grokking:

• Weight decay λ: For small λ, decreasing λ increases t2 with t2 ∝1/λ when other hyperparameters are held fixed, and λ has no effect on our bound for t1. Therefore, (t2 −t1) →∞as λ →0. We remark that for large λ (which is not our focus in this work), our upper bound in Equation (6) is not tight in general, as a tight bound should incorporate the term ηλ+ min(Φ⊤Φ) + ηλ in the denominator. • Sample size n and feature dimensionality m: It is difficult to deduce clean dependencies that capture the behavior of t1 as a function of n and m, since there is no known quantitative bound revealing how λ+ min(Φ⊤Φ) depends on m and n, even when making strong assumptions on the distribution of the features (see Remark 4.3 for a discussion). On a more positive note, we show empirically that the behavior of t1 as a function of n and m strongly accords with our theoretical bound in Equation (6). As for t2, since we make no assumption on the feature map ϕ(x), the quantity λmin(Σ) is not necessarily controlled. Indeed, more explicit dependencies of t2 on n and m can be derived by assuming distributional assumptions. For instance, if ϕ(x1),..., ϕ(xn)

are i.i.d. spherical Gaussian vectors. We present such clean bounds in Equation (8) and show that it strongly matches our experimental results. • Initialization scale ν2: Increasing ν2 increases t1 and t2 simultaneously with t1, t2 ∝ln(ν2). More precisely, when λ is sufficiently small, we have t2 > t1, and moreover t1 ≤c1 ln(ν2)+a1 and t2 ≥c2 ln(ν2)+ a2 for some c2 > c1 > 0 and some a1, a2. In such a scenario, increasing ν2 increases (t2 −t1) and amplifies grokking. Remark 4.3 (on λ+ min(Φ⊤Φ) and its dependence on n and m). λ+ min(Φ⊤Φ) is an empirical quantity which depends on the sampled features. We note that even for simple distributions such as ϕ(x) ∼N(0, 1 mIm), the behavior of λ+ min(Φ⊤Φ) as a function of n and m is not yet fully understood. While there is a known asymptotic result given by the celebrated Marchenko–Pastur law (Marˇcenko & Pastur, 1967), showing that when m, n →∞and m/n →γ for some γ ∈(0, ∞), λ+ min(Φ⊤Φ) →γ−1(1 −√γ)2, to the best of our knowledge, there is no quantitative bound revealing how this depends on m and n.

Next, we state a separate theorem for each of the three stages of our grokking result, as it is helpful for understanding each hyperparameter effect separately. Theorem 4.4 (Training loss convergence). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm, and that θ(0) ∼ N(0, ν2Im). Assume that η < 1/(λ + λmax(Φ⊤Φ)/n). For any ϵ > 0 and δ ∈(0, 1), suppose that m = Ω max log

1 δ

, ∥θ∗∥2

2 ν2 and λ = O min

( ϵ ∥θ∗∥2

2,

√

Lϵ ∥θ∗∥2

)!

.

Then, with probability at least 1 −δ, we have Ln(θ(t)) ≤ϵ for all t ≥1

2 log 1− ηλ+ min(Φ⊤Φ)

n −ηλ ϵ 6L∥θ(0)∥2 2

.

The above assumption that m = Ω(∥θ∗∥2

2/ν2) implies that the student is initialized to have a large norm with respect to the teacher’s norm. Since we aim to upper bound Ln(θ(t)) and not Ln(θ(t); λ), the assumed upper bound on λ is for technical purposes, and it does not limit our results since small values of λ facilitate grokking. Theorem 4.5 (Poor generalization when overfitting). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm, that θ(0) ∼N(0, ν2Im), and further assume that η < 1/λ. For any c > 0 and δ ∈(0, 1), suppose that m = n + Ω max log

1 δ

, ∥θ∗∥2

2 ν2, c λmin(Σ)ν2

.

<!-- Page 7 -->

Provable Grokking in Ridge Regression

Then, with probability at least 1 −δ, we have L(θ(t)) ≥c for all t ≤log1−ηλ s

2 (m −n)ν2 r c λmin(Σ) + ∥θ∗∥2

!

.

The lower bound on m here is stronger than the one in Theorem 4.4, which ensures that we are in a high-dimensional regression situation. In our last theorem, we prove that good generalization eventually occurs.

Theorem 4.6 (Generalization). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume that ∥ϕ(x)∥2 ≤b for any x for some b > 0. Let θ∗ λ = arg minθ {Ln(θ; λ)}. For any ϵ > 0 and δ ∈(0, 1), suppose that n = Ω b4∥θ∗∥4

2 ϵ2 log

1 δ

.

Then, if η ≤1/(λ + b2), GD converges to θ∗ λ satisfying L(θ∗ λ) ≤2Ln(θ∗ λ) + ϵ, with probability at least 1 −δ.

The lower bound on the sample size n = Ω(b4∥θ∗∥4

2ϵ−2) stems from a standard uniform convergence argument based on Rademacher complexity.

## 5. Experiments

In this section, we systematically verify our theoretical understanding of grokking via experiments. Throughout, we use n, η and λ to denote the training sample size, GD step size and weight decay parameter, respectively. In all of our experiments, we set the error thresholds c = ϵ = 0.01.

## 5.1. Hyperparameter Control

We empirically verify our quantitative bounds on how the model’s hyperparameters affect grokking in realizable ridge regression. Specifically, we train a student linear regression model using gradient descent with weight decay, to learn a realizable teacher with unit norm, i.e. ∥θ∗∥2 = 1. We simply choose the feature map to be the identity function, i.e. ϕ(x) = x ∈Rm. We use ν2 to denote the initialization scale of weights in line with our theory.

As discussed in Section 4, λmin(Σ) cannot be controlled without making additional assumptions on ϕ(x). Consequentially, by introducing additional distributional assumptions, we are able to provide more explicit bounds for t1 and t2 based on Theorem 4.2. Specifically, we assume that ϕ(x1),..., ϕ(xn) are drawn i.i.d. from a Gaussian distribution N(0, 1 mIm). In such a case, if ηλ ≤0.01, a simple calculation (see Remark A.14 for details) yields that t2 ≥ ln

(m−n)ν2

8mϵ

2.02ηλ and t1 ≤ n ln

14mν2 ϵ

2ηλ+ min(Φ⊤Φ). (8)

**Figure 2.** Plots for the effects of hyperparameters on grokking in

ridge regression. Left Upper: decreasing weight decay extends the generalization delay (t2 ∝1/λ); Right Upper: decreasing sample size amplifies grokking by speeding up the convergence of the training loss (affects t1); Left Lower: increasing the feature dimension has little effect on t1 and t2; Right Lower: increasing the initialization scale increases t1 and t2 simultaneously at logarithmic rates (t1, t2 ∝ln(ν2)).

Our experiments are also implemented with such a distributional assumption. We set η = 1, and unless otherwise stated for comparison purposes, we use the default values n = 100, m = 1000, ν2 = 1 and λ = 10−4.

The results are shown in Figure 2, where the dashed lines represent our theoretical bounds for t1 and t2 in Equation (8), and solid lines represent the values of t1 and t2 that were observed empirically. Notably, all pairs of solid and dashed lines seem to match in their behavior, implying that our theoretical bounds provide strong control.

## 5.2. Random-Features Neural Networks

In this subsection, we train a two-layer random ReLU features network to learn a single ReLU neuron teacher network with unit norm weights, i.e. x 7→σ(⟨w∗, x⟩) with ∥w∗∥2 = 1, where σ(·) = max{0, ·} is the ReLU activation. A two-layer ReLU neural network is in the form of N(x; θ) = Pm j=1 ajσ(⟨wj, x⟩) for all x ∈Rd. For random-features neural networks, we only optimize the output layer weights θ = a, and the hidden layer weights are initialized and then fixed during training. Clearly, this random feature model is a special case of linear regression with feature map ϕ(x) = (ϕ1(x),..., ϕm(x)) where ϕj(x) = σ(⟨wj, x⟩) for all j ∈[m]. We use the following initialization scheme a(0)

j ∼N(0, 1), wj ∼N(0, ν2 dmId) for each j ∈[m].

![Figure extracted from page 7](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

Provable Grokking in Ridge Regression

**Figure 3.** Plots of training and test losses of a two-layer random

ReLU features network. Dashed/solid lines indicate train/test loss respectively. Left Upper: using smaller weight decay amplifies the grokking time by delaying generalization (increases t2); Right Upper: having smaller sample size amplifies grokking by speeding up the training convergence (decreases t1); Left Lower: increasing the student’s width does not significantly prolong grokking; Left Lower: increasing the initialization scale does not significantly prolong grokking, but instead widens the gap between the generalization and training losses during the overfitting stage.

We present the results in Figure 3, by a standard comparison between the training and test losses. We set: d = 100, η = 1, and unless otherwise stated for comparison purposes, we use the default values n = 100, λ = 10−5, m = 10000 and ν2 = 1. Since the teacher w∗is sampled independently of the student network, this sets us in a non-realizable setting. However, since a sufficiently wide student network can approximate any teacher to arbitrary accuracy with high probability, we are essentially arbitrarily close to the realizable setting with sufficient over-parameterization. The figure shows behavior similar to that of realizable ridge regression.

## 5.3. Non-linear Neural Networks

We also study empirically the effects of the different hyperparameters on grokking for training (both layers of) a twolayer ReLU neural network as defined in Subsection 5.2 with θ = (W, a). We use the following initialization scheme a(0)

j ∼N(0, 1 m), w(0)

j ∼N(0, ν2 d Id) for each j ∈[m]. Specifically, we choose the zero function to be the underlying teacher, and set η = 10−4, d = 50, and unless otherwise stated for comparison purposes, we use the default values n = 50, m = 1000, ν2 = 1 and λ = 0.05.

The results are presented in Figure 4. Notably, the dependencies of t1 and t2 on the hyperparameters match qualitatively to those in Figure 2. This suggests that our bounds might capture behaviors that hold much more generally than our

**Figure 4.** Plots for the effect of the hyperparameters on grokking when training a two-layer ReLU network with the zero teacher.

currently analyzed setting, and thus exploring it further is an intriguing direction for future work.

Finally, we include the experimental setup for Figure 1 for completeness. Left: n = 100, m = 10000, λ = 10−5, ν2 = 1 and η = 1; Right: d = 50, n = 50, m = 1000, λ = 0.1, ν2 = 1 and η = 10−4. See Appendix B for additional experiments.

## 6. Discussion and Future Directions

We study grokking and establish the first end-to-end provable grokking result for the classical ridge regression model. We derive quantitative bounds for the grokking time in terms of the model hyperparameters and verify our theoretical findings via experiments. Our work establishes a rigorous theoretical foundation for grokking. Observing this phenomenon within the fundamental framework of linear regression is not only surprising in its simplicity, but also highly illuminating; it provides a controlled environment that allows us to cleanly isolate the precise effects of individual hyperparameters. By uncovering the root causes of grokking in this transparent setting, our analysis may serve as a stepping stone toward demystifying its dynamics in modern deep learning architectures.

Our work leaves several interesting questions open. Firstly, can we show end-to-end provable grokking results for nonrealizable ridge regression? This includes the special case of ridge regression with label noise (see Figure 6 in Appendix B). Since we have already observed grokking empirically in non-realizable learning with two-layer randomfeatures neural networks, it is natural to start studying such random features models. Indeed, deriving provable

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-008-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Provable Grokking in Ridge Regression grokking results for learning agnostically with two-layer ReLU random features neural networks seems challenging. We find that current theoretical analyses fail to identify a hyperparameter realization for grokking. Specifically, when using our techniques, choosing an arbitrarily small weight decay parameter in the agnostic learning setting may impede generalization entirely. This suggests that new tools and more careful convergence analyses might be required.

Another question left open by our research is whether we can show end-to-end provable grokking as a result of a transition from the lazy to the rich regime of training neural networks. As discussed earlier, many existing works attribute grokking to such lazy-to-rich regime transitions, and have verified it empirically, but none provided a rigorous theoretical analysis proving it. Motivated by this, we have also explored grokking in a setting where we learn a target neural network teacher, by training a two-layer student network using GD with weight decay. Unlike the ridge regression setting addressed in this paper, proving that overfitting occurs remains challenging even under strong assumptions, such as a zero-teacher model where GD only optimizes the hidden layer weights. While a classical neural tangent kernel (NTK) analysis implies that each neuron remains close to its initialization during training, this does not guarantee persistent poor generalization; the collective contribution of m neurons may still allow the trained network to converge toward the zero function.

We note that when training with a small weight decay coefficient, the overfitting solution that we obtain corresponds to training without weight decay, and the asymptotic solution is the minimum-norm interpolating predictor, which corresponds to training with zero initialization without weight decay (Gunasekar et al., 2018; Vardi & Shamir, 2021). Hence, in our setting grokking corresponds to a transition from a misspecified to a well-specified prior. Moreover, Lauditi et al. (2025) showed that weight decay in wide non-linear neural networks may cause the initial NTK to decay leaving only a data-dependent NTK. Thus, similarly to our work, in their setting weight decay changes an implicit prior. However, it is unclear whether their prior change can lead to grokking.

Finally, it is worth noting that grokking in regression tasks exhibits structural differences from its classification counterpart, particularly regarding the characteristic “test error plateau”. In classification, this plateau is typically an artifact of evaluating a discrete metric (accuracy) rather than a continuous loss (e.g. Gromov, 2023, Figure 1). In regression, however, the continuous loss is the natural primary metric, which typically decays smoothly without an explicit plateau. To bridge this gap and investigate whether our setting captures this classic phenomenon, we define a threshold-based surrogate accuracy metric given by Px((N(x; θ(t)) −N ∗(x))2 ≤ϵ) for a fixed ϵ > 0. Remarkably, evaluating our model under this metric reveals the familiar plateauing phenomenon experimentally (see Figure 5 in Appendix B). This confirms that the plateau is not unique to classification settings but can be recovered in linear regression under appropriate evaluation, offering a promising direction for future theoretical analysis.

## Acknowledgements

We thank the anonymous reviewers who provided useful suggestions to improve the quality of this paper. GV is supported by the Israel Science Foundation (grant No. 2574/25), by a research grant from Mortimer Zuckerman (the Zuckerman STEM Leadership Program), and by research grants from the Center for New Scientists at the Weizmann Institute of Science, and the Shimon and Golde Picker – Weizmann Annual Grant. IS is supported by the Israel Science Foundation (grant No. 1753/25).

Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. Since this work is mainly theoretical in its nature, there are no societal implications that require discloser as far as we can discern.

## References

Barak, B., Edelman, B., Goel, S., Kakade, S., Malach, E., and Zhang, C. Hidden progress in deep learning: Sgd learns parities near the computational limit. Advances in Neural Information Processing Systems, 35:21750– 21764, 2022.

Bartlett, P. L. and Mendelson, S. Rademacher and gaussian complexities: Risk bounds and structural results. Journal of Machine Learning Research, 3(Nov):463–482, 2002.

Beck, A., Levi, N., and Bar-Sinai, Y. Grokking at the edge of linear separability. In Forty-second International Conference on Machine Learning, 2025.

Blanc, G., Gupta, N., Valiant, G., and Valiant, P. Implicit reg- ularization for deep neural networks driven by an ornsteinuhlenbeck like process. In Conference on Learning Theory, pp. 483–513, 2020.

Boursier, E., Pesme, S., and Dragomir, R.-A. A theoreti- cal framework for grokking: Interpolation followed by riemannian norm minimisation. Advances in Neural Information Processing Systems, 2025.

Charton, F. Learning the greatest common divisor: explain- ing transformer predictions. The Twelfth International Conference on Learning Representations, 2024.

<!-- Page 10 -->

Provable Grokking in Ridge Regression

Chughtai, B., Chan, L., and Nanda, N. A toy model of universality: Reverse engineering how networks learn group operations. In International Conference on Machine Learning, pp. 6243–6267, 2023.

Davies, X., Langosco, L., and Krueger, D. Unifying grokking and double descent. arXiv preprint arXiv:2303.06173, 2023.

Dudeja, R. and Hsu, D. Learning single-index models in gaussian space. In Conference On Learning Theory, pp. 1887–1930, 2018.

Fan, S., Pascanu, R., and Jaggi, M. Deep grokking: Would deep neural networks generalize better? arXiv preprint arXiv:2405.19454, 2024.

Galton, F. Regression towards mediocrity in hereditary stature. The Journal of the Anthropological Institute of Great Britain and Ireland, 15:246–263, 1886.

Gromov, A. Grokking modular arithmetic. arXiv preprint arXiv:2301.02679, 2023.

Gunasekar, S., Lee, J., Soudry, D., and Srebro, N. Charac- terizing implicit bias in terms of optimization geometry. In International Conference on Machine Learning, pp. 1832–1841. PMLR, 2018.

Hoerl, A. E. and Kennard, R. W. Ridge regression: Biased estimation for nonorthogonal problems. Technometrics, 12(1):55–67, 1970.

Humayun, A. I., Balestriero, R., and Baraniuk, R. Deep net- works always grok and here is why. In International Conference on Machine Learning, pp. 20722–20745, 2024.

Jeffares, A. and van der Schaar, M. Position: Not all explana- tions for deep learning phenomena are equally valuable. In Forty-second International Conference on Machine Learning Position Paper Track, 2025.

Jeffares, A., Curth, A., and van der Schaar, M. Deep learning through a telescoping lens: A simple model provides empirical insights on grokking, gradient boosting & beyond. Advances in Neural Information Processing Systems, 37: 123498–123533, 2024.

Kumar, T., Bordelon, B., Gershman, S. J., and Pehlevan,

C. Grokking as the transition from lazy to rich training dynamics. In The Twelfth International Conference on Learning Representations, 2024.

Lauditi, C., Bordelon, B., and Pehlevan, C. Adaptive kernel predictors from feature-learning infinite limits of neural networks. In Proceedings of the Forty-second International Conference on Machine Learning, pp. 32617– 32648, 2025.

Levi, N., Beck, A., and Bar-Sinai, Y. Grokking in linear estimators–a solvable model that groks without understanding. In The Twelfth International Conference on Learning Representations, 2024.

Liu, Z., Kitouni, O., Nolte, N. S., Michaud, E., Tegmark,

M., and Williams, M. Towards understanding grokking: An effective theory of representation learning. Advances in Neural Information Processing Systems, 35:34651– 34663, 2022.

Liu, Z., Michaud, E. J., and Tegmark, M. Omnigrok: Grokking beyond algorithmic data. The Eleventh International Conference on Learning Representations, 2023.

Lyu, K., Jin, J., Li, Z., Du, S. S., Lee, J. D., and Hu, W.

Dichotomy of early and late phase implicit biases can provably induce grokking. The Twelfth International Conference on Learning Representations, 2024.

Mallinar, N. R., Beaglehole, D., Zhu, L., Radhakrishnan, A.,

Pandit, P., and Belkin, M. Emergence in non-neural models: grokking modular arithmetic via average gradient outer product. In Forty-second International Conference on Machine Learning, 2025.

Marˇcenko, V. A. and Pastur, L. A. Distribution of eigenval- ues for some sets of random matrices. Mathematics of the USSR-Sbornik, 1(4):457, 1967.

Merrill, W., Tsilivis, N., and Shukla, A. A tale of two circuits: Grokking as competition of sparse and dense subnetworks. arXiv preprint arXiv:2303.11873, 2023.

Miller, J. W., O’Neill, C., and Bui, T. D. Grokking beyond neural networks: An empirical exploration with model complexity. Transactions on Machine Learning Research, 2024. ISSN 2835-8856.

Mohamadi, M. A., Li, Z., Wu, L., and Sutherland, D. J. Why do you grok? a theoretical analysis on grokking modular addition. In International Conference on Machine Learning, pp. 35934–35967, 2024.

Nanda, N., Chan, L., Lieberum, T., Smith, J., and Steinhardt,

J. Progress measures for grokking via mechanistic interpretability. In The Eleventh International Conference on Learning Representations, 2023.

Notsawo Jr, P., Zhou, H., Pezeshki, M., Rish, I., Dumas,

G., et al. Predicting grokking long before it happens: A look into the loss landscape of models which grok. arXiv preprint arXiv:2306.13253, 2023.

Power, A., Burda, Y., Edwards, H., Babuschkin, I., and

Misra, V. Grokking: Generalization beyond overfitting on small algorithmic datasets. arXiv preprint arXiv:2201.02177, 2022.

<!-- Page 11 -->

Provable Grokking in Ridge Regression

Prieto, L., Barsbey, M., Mediano, P. A., and Birdal, T.

Grokking at the edge of numerical stability. In The Thirteenth International Conference on Learning Representations, 2025.

Radhakrishnan, A., Beaglehole, D., Pandit, P., and Belkin,

M. Mechanism of feature learning in deep fully connected networks and kernel machines that recursively learn features. arXiv preprint arXiv:2212.13881, 2022.

Shalev-Shwartz, S. and Ben-David, S. Understanding ma- chine learning: From theory to algorithms. Cambridge university press, 2014.

Tan, Z. and Huang, W. Understanding grokking through a robustness viewpoint. arXiv preprint arXiv:2311.06597, 2023.

Thilak, V., Littwin, E., Zhai, S., Saremi, O., Paiss, R., and Susskind, J. The slingshot mechanism: An empirical study of adaptive optimizers and the grokking phenomenon. arXiv preprint arXiv:2206.04817, 2022.

Tikeng Notsawo, Pascal, J., Dumas, G., and Rabusseau, G.

Grokking beyond the Euclidean norm of model parameters. In Proceedings of the 42nd International Conference on Machine Learning, volume 267 of Proceedings of Machine Learning Research, pp. 28552–28618. PMLR, 2025. URL https://proceedings.mlr.press/ v267/junior25a.html.

Tikhonov, A. N. Solution of incorrectly formulated prob- lems and the regularization method. Sov Dok, 4:1035– 1038, 1963.

Uyanık, G. K. and G¨uler, N. A study on multiple linear regression analysis. Procedia-Social and Behavioral Sciences, 106:234–240, 2013.

Vardi, G. and Shamir, O. Implicit regularization in relu networks with the square loss. In Conference on Learning Theory, pp. 4224–4258, 2021.

Varma, V., Shah, R., Kenton, Z., Kram´ar, J., and Kumar,

R. Explaining grokking through circuit efficiency. arXiv preprint arXiv:2309.02390, 2023.

Wang, B., Yue, X., Su, Y., and Sun, H. Grokking of implicit reasoning in transformers: A mechanistic journey to the edge of generalization. Advances in Neural Information Processing Systems, 37:95238–95265, 2024.

Xu, Z., Wang, Y., Frei, S., Vardi, G., and Hu, W. Benign overfitting and grokking in relu networks for xor cluster data. The Twelfth International Conference on Learning Representations, 2024.

Xu, Z., Ni, Z., Wang, Y., and Hu, W. Let me grok for you: Accelerating grokking via embedding transfer from a weaker model. The Thirteenth International Conference on Learning Representations, 2025.

Yunis, D., Patel, K. K., Wheeler, S., Savarese, P., Vardi, G.,

Livescu, K., Maire, M., and Walter, M. R. Approaching deep learning through the spectral dynamics of weights. arXiv preprint arXiv:2408.11804, 2024.

Zhu, X., Fu, Y., Zhou, B., and Lin, Z. Critical data size of language models from a grokking perspective. arXiv preprint arXiv:2401.10463, 2024.

ˇZunkoviˇc, B. and Ilievski, E. Grokking phase transitions in learning local rules with gradient descent. Journal of Machine Learning Research, 25(199):1–52, 2024.

<!-- Page 12 -->

Provable Grokking in Ridge Regression

A. Missing Proofs

Theorem A.1 (Theorem 4.1 restated). Assume that 0 < η ≤2/(L + 2λ) and θ(0) ∼N(0, ν2Im). Then for any t ∈N, we have

1. Ln(θ(t)) ≤L 2 · (1 −1 nηλ+ min(Φ⊤Φ) −ηλ)2t · ∥θ(0)∥2

2;

2. w.p. at least 1 −2e−(m−n)/32, L(θ(t)) ≥λmin(Σ) · (1 −ηλ)2t · (m−n)ν2

2; 3. ∥θ(t)∥2 ≤(1 −ηλ)t · ∥θ(0)∥2.

Proof of Theorem A.1. The proof of Theorem A.1 follows from the following Theorem A.2, Theorem A.4 and Theorem A.5.

Theorem A.2 (Training loss convergence). For all t ∈N, we have

Ln(θ(t)) ≤L

2 ·

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

· ∥θ(0)∥2 2.

Remark A.3. Let Γ:= 1 nΦ⊤Φ + λIm and let λmin(Γ) denote its smallest eigenvalue. Following a standard argument for showing convergence for ridge regression, we can easily prove Ln(θ(t)) ≤L(1 −ηλmin(Γ))2t∥θ(0)∥2

2. To show grokking, we need to prove that the convergence of the training error is faster than the generalization error. However, when the feature map Φ is not full rank, λmin(Γ) = λ, making this rate match the lower bound in Theorem A.4 below, and thus does not suffice to prove grokking. Therefore, a more tight bound on the convergence rate is required here.

Proof of Theorem A.2. For any vector θ ∈Rm, we write the following unique decomposition θ = θ∥+ θ⊥where θ∥is in the row space of Φ and θ⊥is orthogonal to the row space of Φ (or equivalently, θ⊥is in the null space of Φ). We can express the training loss (at θ)

Ln (θ) = 1

2n n X i=1

(⟨θ, ϕ(xi)⟩)2 = 1

2n n X i=1 θ∥, ϕ(xi)

2 = Ln(θ∥)

as a function of θ∥. Note that

∥∇θLn(θ) −∇θLn(θ′)∥2 =

1 n n X i=1

N(xi; θ)ϕ(xi) −1 n n X i=1

N(xi; θ′)ϕ(xi)

2

=

1 n n X i=1 ϕ(xi) ⟨θ −θ′, ϕ(xi)⟩

2

≤ v u u t

1 n n X i=1

(⟨θ −θ′, ϕ(xi)⟩)2

!

1 n n X i=1

∥ϕ(xi)∥2

2

!

≤

1 n n X i=1

∥ϕ(xi)∥2

2

!

· ∥θ −θ′∥2 = L ∥θ −θ′∥2.

Due to the above Lipschitz continuity of the gradient, we have

Ln(θ(t)) −Ln(θ∗) =Ln(θ(t)

∥) −Ln(θ∗

∥)

≤

∇θLn(θ∗

∥)

⊤ θ(t)

∥ −θ∗

∥

+ L

2 θ(t)

∥ −θ∗

∥

2

2 = L 2 θ(t)

∥ −θ∗

∥

2

2. (9)

<!-- Page 13 -->

Provable Grokking in Ridge Regression

Next, we write out the GD iteration as θ(t) =θ(t−1) −η n n X i=1

N(xi; θ(t−1))ϕ(xi) −ηλθ(t−1)

=θ(t−1) −η n n X i=1

D θ(t−1), ϕ(xi)

E ϕ(xi) −ηλθ(t−1)

=

Im −η

1 nΦ⊤Φ + λIm θ(t−1). (10)

Based on the orthogonal decomposition, we can further write θ(t+1)

∥ =θ(t)

∥ −ηΦ⊤Φθ(t)

∥ −ηλθ(t)

∥, θ(t+1)

⊥ =θ(t)

⊥−ηλθ(t)

⊥= (1 −ηλ) θ(t)

⊥.

Let λ+ min(Φ⊤Φ) denote the smallest non-zero eigenvalue of the matrix Φ⊤Φ. It follows that

∥θ(t)

∥∥2

2 =

Im −η nΦ⊤Φ −ηλIm t θ(0)

∥

2

2 ≤

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥θ(0)

∥∥2

2. (11)

To have the above hold, it suffices to choose a sufficiently small step size η < 1 λ + (1/n)λmax(Φ⊤Φ).

Since θ∗= 0 and Ln(θ∗) = 0, we have from Equations (9) and (11) that

Ln θ(t)

≤L

2 ∥θ(t) ∥∥2

2 ≤L 2 ·

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

· ∥θ(0) ∥∥2

2.

Note that the convergence rate of (1 −ηλ+ min(Φ⊤Φ)/n −ηλ/n)2t is always faster than (1 −ηλ/n)2t. In particular, a small weight decay λ will amplify grokking. The proof is done!

Theorem A.4 (Overfitting). Assume that θ(0) ∼N(0, ν2Im). Then, for all t ∈N, we have

L(θ(t)) ≥λmin(Σ) · (1 −ηλ)2t · (m −n)ν2

2, with probability at least 1 −2e−(m−n)/32.

Proof of Theorem A.4. By definition, the generalization error satisfies

Ex

N(x; θ(t)) −N ∗(x)

2

= (θ(t))⊤Σθ(t) ≥λmin(Σ) · ∥θ(t)∥2

2.

Recall that Φ:= (ϕ(x1),..., ϕ(xn))⊤and θ(t+1) = θ(t) −(η/n)Φ⊤Φθ(t) −ηλθ(t). For any θ ∈Rm, we inherit the notations θ = θ∥+ θ⊥used in the proof of Theorem A.2. It holds that θ(t+1)

∥ =θ(t)

∥ −(η/n)Φ⊤Φθ(t)

∥ −ηλθ(t)

∥, θ(t+1)

⊥ =θ(t)

⊥−ηλθ(t)

⊥= (1 −ηλ) θ(t)

⊥.

Hence, we have at step t > 0 that θ(t)

⊥= (1 −ηλ) θ(t−1)

⊥ = · · · = (1 −ηλ)t θ(0)

⊥.

<!-- Page 14 -->

Provable Grokking in Ridge Regression

Note that θ(0)

⊥lies in a subspace of dimensionality k, which is at least m −n. Let e1,..., ek represent an orthogonal basis for the subspace, we have

∥θ(0)

⊥∥2

2 = k X j=1

⟨θ(0), ej⟩

2

.

Since θ(0) ∼N(0, ν2Id), we have that ⟨θ(0), ej⟩, j ∈[k] are independent N(0, ν2) random variables. By standard concentration inequality for Chi-squared distribution (c.f. Dudeja & Hsu, 2018, Fact 5), we have that with probability at least 1 −2 exp(−k/32),

∥θ(0)

⊥∥2

2 = k X j=1

⟨θ(0), ej⟩

2

≥kν2

2.

Since k ≥m −n, we have with probability of at least 1 −2 exp(−(m −n)/32),

∥θ(t)∥2

2 ≥∥θ(t) ⊥∥2

2 = (1 −ηλ)2t ∥θ(0) ⊥∥2

2 ≥(1 −ηλ)2t (m −n)ν2

2.

It follows that

Ex

N(x; θ(t)) −N ∗(x)

2

≥λmin(Σ) · (1 −ηλ)2t · (m −n)ν2

2, with probability at least 1 −2e−(m−n)/32.

Theorem A.5 (Generalization). Assume that 0 < η ≤2/(L + 2λ). Then, for all t ∈N, we have

∥θ(t)∥2 ≤(1 −ηλ)t · ∥θ(0)∥2.

Remark A.6. Note that a student network with zero output weights is exactly the zero function.

Proof of Theorem A.5. We analyze the behavior of the regularization. Note that θ(t+1)

2

2 = θ(t) −η∇θLn(θ(t)) −ηλθ(t)

2

2

=(1 −ηλ)2 θ(t)

2

2 + η2 ∇θLn(θ(t))

2

2 −2η(1 −ηλ) D

∇θLn(θ(t)), θ(t)E

, and then we have θ(t+1)

2

2 − θ(t)

2

2 −

(1 −ηλ)2 −1 θ(t)

2

2

= θ(t+1)

2

2 −(1 −ηλ)2 θ(t) 2

2

=η2 ∇θLn(θ(t))

2

2 −2η(1 −ηλ) D

∇θLn(θ(t)), θ(t)E

=η2

1 n n X i=1

N(xi; θ(t))ϕ(xi)

2

2 −2η(1 −ηλ) · 1 n n X i=1

N(xi; θ(t))

2

≤η2

1 n n X i=1

N(xi; θ(t))

2

!

1 n n X i=1

∥ϕ(xi)∥2

2

!

−2η(1 −ηλ) · 1 n n X i=1

N(xi; θ(t))

2

.

It is clear that when

0 < η ≤ 2 1 n

Pn i=1∥ϕ(xi)∥2

2 + 2λ = 2 L + 2λ, the total norm of parameters is decreasing in a linear rate:

θ(t)

2 ≤(1 −ηλ)t · θ(0)

2.

This implies that GD eventually reaches θ∗= 0 and yields generalization.

<!-- Page 15 -->

Provable Grokking in Ridge Regression

Theorem A.7 (Theorem 4.2 restated). Assume a realizable teacher function N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume the boundedness of the feature map, i.e. ∥ϕ(x)∥2 ≤b for any x and some constant b > 0. Randomly initialize a student linear regression model N(x; θ(0)) = ⟨θ(0), ϕ(x)⟩with θ(0) ∼N(0, ν2Im). Consider training the student to learn the teacher using gradient descent on the ridge regression objective in Equation (1). Let c ≥ϵ be a constant. For any ϵ > 0, define t1:= t1(ϵ):= max n t ∈N: Ln(θ(t)) ≥ϵ o and t2:= t2(c):= min n t ∈N: L(θ(t)) ≤c o

.

For any δ ∈(0, 1), assume a sufficiently large sample size:

n = Ω b4∥θ∗∥4

2 ϵ2 log

1 δ

, a sufficiently wide regression model:

m = n + Ω max log

1 δ

, ∥θ∗∥2

2 ν2, c2 λ2 min(Σ)ν2

, and finally a sufficiently small weight decay:

λ = O min

( ϵ ∥θ∗∥2

2,

√

Lϵ ∥θ∗∥2

)!

.

Then, if η < 1/(λ + b2), we have with probability at least 1 −δ, t1 ≤ n ln

6b2∥θ(0)∥2 2 ϵ

2ηλ+ min(Φ⊤Φ)

and t2 ≥ ln

(m−n)ν2

2 q c λmin(Σ) + ∥θ∗∥2

−2!

4ηλ.

Moreover, L(θ(t)) ≤ϵ for sufficiently large t.

Proof of Theorem A.7. Based on the following Theorem A.8 and Theorem A.9, we can obtain that, with probability at least 1 −δ, t1 ≤1

2 log 1− ηλ+ min(Φ⊤Φ)

n −ηλ ϵ 6L∥θ(0)∥2 2

, and with probability at least 1 −δ, t2 ≥1

2 log1−ηλ

2 (m −n)ν2 r c λmin(Σ) + ∥θ∗∥2

2!

.

We use the following Taylor expansion ln(1 −x) = −x −x2

2 −x3 3 −· · ·. For a sufficiently small λ > 0, it implies that ln(1 −ηλ) ≥−2ηλ and also ln(1 −ηλ+ min(Φ⊤Φ)

n) ≤−ηλ+ min(Φ⊤Φ)

n. Now, we can further write t1 ≤1

2 log 1− ηλ+ min(Φ⊤Φ)

n −ηλ ϵ 6L∥θ(0)∥2 2

≤1

2 log 1− ηλ+ min(Φ⊤Φ)

n ϵ 6L∥θ(0)∥2 2

= ln ϵ 6L∥θ(0)∥2 2

2 ln

1 −ηλ+ min(Φ⊤Φ)

n

≤ n ln

6L∥θ(0)∥2 2 ϵ

2ηλ+ min(Φ⊤Φ),

<!-- Page 16 -->

Provable Grokking in Ridge Regression and t2 ≥1

2 log1−ηλ

2 (m −n)ν2 r c λmin(Σ) + ∥θ∗∥2

2!

= ln

2 (m−n)ν2 q c λmin(Σ) + ∥θ∗∥2

2!

2 ln(1 −ηλ)

≥ ln

(m−n)ν2

2 q c λmin(Σ) + ∥θ∗∥2

−2!

4ηλ.

The bounds on the grokking time are proved via bounding L ≤b2. Finally, we explain the generalization guarantee. Let θ∗ λ = arg minθ {Ln(θ; λ)}. Fix some t > 0, we have by triangle inequality that

L(θ(t)) =(L(θ(t)) −L(θ∗ λ)) + (L(θ∗ λ) −2Ln(θ∗ λ)) + 2Ln(θ∗ λ)

≤(L(θ(t)) −L(θ∗ λ)) + (L(θ∗ λ) −2Ln(θ∗ λ)) + 2Ln(θ∗ λ; λ).

Since θ(t) converges to θ∗ λ (as we show in the proof of Theorem A.10), we have L(θ(t))−L(θ∗ λ) ≤ϵ/4 for some sufficiently large t > 0. Applying Theorem A.10 with ϵ/4 yields that L(θ∗ λ) −2Ln(θ∗ λ) ≤ϵ/4, with probability at least 1 −δ. Also, we can have 2Ln(θ∗ λ; λ) ≤ϵ/2 with a sufficiently small λ. Note that we proved the theorem with probability 1 −3δ here. This does not matter since in the theorem assumptions δ only appears in asymptotic notations which ignore constant factors.

Theorem A.8 (Theorem 4.4 restated). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume that θ(0) ∼ N(0, ν2Im). For any ϵ > 0 and δ ∈(0, 1), if m = Ω max log

1 δ

, ∥θ∗∥2

2 ν2 and λ = O min

( ϵ ∥θ∗∥2

2,

√

Lϵ ∥θ∗∥2

)!

, then, if η < 1/(λ + λmax(Φ⊤Φ)/n), when t ≥1

2 log 1− ηλ+ min(Φ⊤Φ)

n −ηλ ϵ 6L∥θ(0)∥2 2

, we have Ln(θ(t)) ≤ϵ with probability at least 1 −δ.

Proof of Theorem A.8. Let θ∗ λ denote the global minimum of the regularized objective. We consider the following decomposition of the unregularized squared loss objective:

Ln(θ(t)) = Ln(θ(t)) −Ln(θ∗ λ) + Ln(θ∗ λ).

Since θ∗ λ is the global minimum, we have

∇θLn(θ∗ λ; λ) = 1 n n X i=1

(N(xi; θ∗ λ) −N ∗(xi)) ϕ(xi) + λθ∗ λ

= 1 n n X i=1

⟨θ∗ λ, ϕ(xi)⟩ϕ(xi) −1 n n X i=1

N ∗(xi)ϕ(xi) + λθ∗ λ

=

1 nΦ⊤Φ + λIm θ∗ λ −1 n n X i=1

N ∗(xi)ϕ(xi) = 0.

<!-- Page 17 -->

Provable Grokking in Ridge Regression

Now, the gradient descent iteration can be written as θ(t) =θ(t−1) −η n n X i=1

N(xi; θ(t−1)) −N ∗(xi)

ϕ(xi) −ηλθ(t−1)

=θ(t−1) −η n n X i=1

D θ(t−1), ϕ(xi)

E ϕ(xi) + η n n X i=1

N ∗(xi)ϕ(xi) −ηλθ(t−1)

=θ(t−1) −η

1 nΦ⊤Φ + λIm θ(t−1) + η n n X i=1

N ∗(xi)ϕ(xi)

=θ(t−1) −η

1 nΦ⊤Φ + λIm

(θ(t−1) −θ∗ λ).

Let u(t):= θ(t) −θ∗ λ for any t ≥0. The above implies that u(t) = u(t−1) −η

1 nΦ⊤Φ + λIm u(t−1) =

Im −η

1 nΦ⊤Φ + λIm u(t−1).

For any vector u ∈Rm, we can write a unique decomposition u = u∥+ u⊥where u∥is in the row space of Φ and u⊥is orthogonal to the row space of Φ (or equivalently, u⊥is in the null space of Φ). Then, we can further write the gradient descent along with the orthogonal decomposition:

u(t)

∥ =u(t−1)

∥ −η nΦ⊤Φu(t−1)

∥ −ηλu(t−1)

∥ =

Im −η

1 nΦ⊤Φ + λIm u(t−1)

∥, u(t)

⊥=u(t−1)

⊥ −ηλu(t−1)

⊥ = (1 −ηλ) u(t−1)

⊥, which implies

∥u(t)

∥∥2

2 =

Im −η nΦ⊤Φ −ηλIm t u(0)

∥

2

2

≤

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥u(0)

∥∥2

2 ≤

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥u(0)∥2

2.

To have the above hold, it suffices to choose a sufficiently small step size:

η < 1 λ + (1/n)λmax(Φ⊤Φ).

From here, we cannot follow the same argument as in the proof of Theorem A.2 via analyzing the Lipschitz continuity since ∇θLn(θ∗ λ)̸ = 0. Note that for any vector θ ∈Rm, we can write the squared loss (at θ) as a function of θ∥:

Ln (θ) = 1

2n n X i=1

(⟨θ −θ∗, ϕ(xi)⟩)2 = 1

2n n X i=1

D θ∥−θ∗

∥, ϕ(xi)

E 2

=: ˜Ln(θ∥).

We can write Ln(θ(t)) −Ln(θ∗ λ) as follow:

Ln(θ(t)) −Ln(θ∗ λ) =˜Ln(θ(t)

∥) −˜Ln(θ∗ λ,∥)

= 1

2n n X i=1

D θ(t)

∥ −θ∗

∥, ϕ(xi)

E 2

−1

2n n X i=1

D θ∗ λ,∥−θ∗

∥, ϕ(xi)

E 2

= 1

2n n X i=1

D θ(t)

∥ −θ∗ λ,∥, ϕ(xi)

E 2

+ 1 n n X i=1

D θ(t)

∥ −θ∗ λ,∥, ϕ(xi)

E D θ∗ λ,∥−θ∗

∥, ϕ(xi)

E

.

<!-- Page 18 -->

Provable Grokking in Ridge Regression

Recall that 1 n

Pn i=1⟨θ∗ λ, ϕ(xi)⟩ϕ(xi) −1 n

Pn i=1⟨θ∗, ϕ(xi)⟩ϕ(xi) + λθ∗ λ = 0, which implies that 1 n

Pn i=1⟨θ∗ λ,∥− θ∗

∥, ϕ(xi)⟩ϕ(xi) + λθ∗ λ,∥= 0 and thus

Ln(θ(t)) −Ln(θ∗ λ)

= 1

2n n X i=1

D θ(t)

∥ −θ∗ λ,∥, ϕ(xi)

E 2

−λ

D θ(t)

∥ −θ∗ λ,∥, θ∗ λ,∥

E

= 1

2n n X i=1

D u(t)

∥, ϕ(xi)

E 2

−λ

D u(t)

∥, θ∗ λ,∥

E

≤L

2 ∥u(t) ∥∥2

2 + λ∥u(t) ∥∥2∥θ∗ λ,∥∥2

≤L

2

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥u(0)∥2

2 + λ

1 −ηλ+ min(Φ⊤Φ)

n −ηλ t

∥u(0)∥2∥θ∗ λ,∥∥2.

It remains to bound ∥θ∗ λ,∥∥2 and Ln(θ∗ λ). Since θ∗ λ is the global minimum of the regularized objective and Ln(θ∗) = 0, we have

Ln(θ∗ λ) + λ

2 ∥θ∗ λ∥2

2 ≤Ln(θ∗) + λ 2 ∥θ∗∥2 2 = λ 2 ∥θ∗∥2 2.

It follows immediately that ∥θ∗ λ,∥∥2 ≤∥θ∗ λ∥2 ≤∥θ∗∥2 and Ln(θ∗ λ) ≤λ

2 ∥θ∗∥2 2. Moreover, note that

∥u(0)∥2 = ∥θ(0) −θ∗ λ∥2 ≤∥θ(0)∥2 + ∥θ∗ λ∥2 ≤∥θ(0)∥2 + ∥θ∗∥2 ≤2∥θ(0)∥2, where the last step holds if ∥θ∗∥2 ≤∥θ(0)∥2. Since θ(0) ∼N(0, ν2Im), when m = Ω(log(1/δ)), we have from Lemma C.1 that ∥θ(0)∥2

2 = Ω(mν2) with probability at least 1 −δ. In particular, when m = Ω max log

1 δ

, ∥θ∗∥2

2 ν2

, we have ∥θ∗∥2 ≤∥θ(0)∥2 with probability at least 1 −δ. Altogether, we have for any t ∈N,

Ln(θ(t)) ≤2L

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥θ(0)∥2

2

+ 2λ

1 −ηλ+ min(Φ⊤Φ)

n −ηλ t

∥θ(0)∥2∥θ∗∥2 + λ

2 ∥θ∗∥2 2.

with probability at least 1 −δ. Finally, for any ϵ > 0, we have

Ln(θ(t)) ≤2L

1 −ηλ+ min(Φ⊤Φ)

n −ηλ

2t

∥θ(0)∥2

2

+ 2λ

1 −ηλ+ min(Φ⊤Φ)

n −ηλ t

∥θ(0)∥2∥θ∗∥2 + λ

2 ∥θ∗∥2 2

≤ϵ

3 + ϵ 3 + ϵ 3 = ϵ, with probability at least 1 −δ, if the following holds:

λ ≤min

(

2ϵ 3∥θ∗∥2 2,

√

Lϵ √

6∥θ∗∥2

)

, and t ≥1

2 log 1− ηλ+ min(Φ⊤Φ)

n −ηλ ϵ 6L∥θ(0)∥2 2

.

Theorem A.9 (Theorem 4.5 restated). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume that θ(0) ∼ N(0, ν2Im). For any constant c > 0 and δ ∈(0, 1), if m = n + Ω max log

1 δ

, ∥θ∗∥2

2 ν2, c λmin(Σ)ν2

,

<!-- Page 19 -->

Provable Grokking in Ridge Regression then, if η < 1/λ, when t ≤log1−ηλ s

2 (m −n)ν2 r c λmin(Σ) + ∥θ∗∥2

!

, we have L(θ(t)) ≥c with probability at least 1 −δ.

Proof of Theorem A.9. Let Σ:= Ex[ϕ(x)ϕ(x)⊤]. Since N ∗(x) = ⟨θ∗, ϕ(x)⟩, we have

L(θ(t)) = Ex h

(N(x; θ(t)) −N ∗(x))2i

= (θ(t) −θ∗)⊤Σ(θ(t) −θ∗) ≥λmin(Σ) · ∥θ(t) −θ∗∥2

2.

Moreover, the gradient descent follows as θ(t) =θ(t−1) −η n n X i=1

N(xi; θ(t−1)) −N ∗(xi)

ϕ(xi) −ηλθ(t−1)

=θ(t−1) −η n n X i=1

D θ(t−1), ϕ(xi)

E ϕ(xi) + η n n X i=1

N ∗(xi)ϕ(xi) −ηλθ(t−1)

=θ(t−1) −η nΦ⊤Φθ(t−1) −ηλθ(t−1) + η nΦ⊤Φθ∗.

Using the same notation θ = θ∥+ θ⊥for any θ ∈Rm where θ⊥is orthogonal to the row space of Φ, we can write θ(t+1)

∥ =θ(t)

∥ −(η/n)Φ⊤Φθ(t)

∥ −ηλθ(t)

∥ + (η/n)Φ⊤Φθ∗

∥, θ(t+1)

⊥ =θ(t)

⊥−ηλθ(t)

⊥= (1 −ηλ) θ(t)

⊥.

Hence, we have at step t > 0 that θ(t)

⊥= (1 −ηλ) θ(t−1)

⊥ = · · · = (1 −ηλ)t θ(0)

⊥.

By triangle inequality, we have

∥θ(t) −θ∗∥2 ≥∥θ(t)∥2 −∥θ∗∥2 ≥∥θ(t)

⊥∥2 −∥θ∗∥2 = (1 −ηλ)t ∥θ(0)

⊥∥2 −∥θ∗∥2.

When θ(0) ∼N(0, ν2Id), following the same analysis in the proof of Theorem A.4, we get

∥θ(t) −θ∗∥2 ≥(1 −ηλ)t r

(m −n)ν2

2 −∥θ∗∥2, with probability at least 1 −2e−(m−n)/32. When m ≥n + 32 log(2/δ), we have 2e−(m−n)/32 ≤δ. This implies that with probability at least 1 −δ,

L(θ(t)) ≥λmin(Σ) ·

(1 −ηλ)t r

(m −n)ν2

2 −∥θ∗∥2

!2

.

Now, for any constant c > 0, m ≥n + 8∥θ∗∥2

2 ν2 and m ≥n + 8c λmin(Σ)ν2 suffice to guarantee that L(θ(0)) ≥c. Then, when t ≤log1−ηλ s

2 (m −n)ν2 r c λmin(Σ) + ∥θ∗∥2

!

, we have L(θ(t)) ≥c, with probability at least 1 −δ.

<!-- Page 20 -->

Provable Grokking in Ridge Regression

Theorem A.10 (Theorem 4.6 restated). Suppose that N ∗(x) = ⟨θ∗, ϕ(x)⟩for some θ∗∈Rm. Assume that ∥ϕ(x)∥2 ≤ b, ∀x for some b > 0. For any ϵ > 0 and δ ∈(0, 1), if n = Ω b4∥θ∗∥4

2 ϵ2 log

1 δ

, then, if η ≤1/(λ + b2), we have with probability at least 1 −δ,

L(θ∗ λ) ≤2Ln(θ∗ λ) + ϵ.

Proof of Theorem A.10. The proof of generalization follows from the standard argument of uniform convergence based on Rademacher complexity, which is defined formally as

Definition A.11 (Rademacher Complexity). Let Sn = {(xi, yi)}n i=1 be a dataset and let H be a function class. The (empirical) Rademacher complexity of H with respect to Sn is defined as follow

RadSn (H):= Eσ1,...,σn∼Unif({±1})

" sup h∈H

1 n n X i=1 σih(xi)

#

, (12)

where σ1,..., σn are called Rademacher variables.

Let us first define the following class of regression models for any positive value B:

Hθ(B):= {x 7→⟨θ, ϕ(x)⟩: ∥θ∥2 ≤B}.

The (empirical) Rademacher complexity of Hθ(B) can be bounded as shown in the following lemma.

Lemma A.12. We have RadSn(Hθ(B)) ≤B p

L/n where L:= 1 n

Pn i=1∥ϕ(xi)∥2

2.

Proof of Lemma A.12.

RadSn(Hθ(B)) = 1 nE

" sup ∥θ∥2≤B n X i=1 σi⟨θ, ϕ(xi)⟩

#

= 1 nE

" sup ∥θ∥2≤B

* θ, n X i=1 σi · ϕ(xi)

+#

Cauchy Schwarz

≤ 1 nE

" sup ∥θ∥2≤B

∥θ∥2 n X i=1 σi · ϕ(xi)

2

#

≤ B n E



 v u u t n X i=1 σi · ϕ(xi)

2

2





Jensen’s ineq.

≤ B n v u u u tE



 n X i=1 σi · ϕ(xi)

2

2





≤ B n v u u tE

" n X i=1

∥σi · ϕ(xi)∥2

2

## σi ∈{±1} = B n v u u t n X i=1

∥ϕ(xi)∥2

2 = B r

L n.

<!-- Page 21 -->

Provable Grokking in Ridge Regression

Next, we introduce the following classical generalization bound based on the Rademacher complexity. The theorem has been adjusted for the purpose of our setting.

Lemma A.13 (Shalev-Shwartz & Ben-David, 2014, Theorem 26.5). Let Hθ be a function class and Sn = {(xi, yi)}n i=1 be a dataset independently selected according to some probability measure P. For any N(x; θ) ∈Hθ, let

Ln(θ):= 1 n n X i=1 ℓ(N(xi; θ), yi) and LP (θ):= E(x,y)∼P [ℓ(N(x; θ), y)]

with some loss function ℓ(·, ·). Assume the boundedness of the loss function, i.e. |ℓ(·, ·)| ≤c. Then, for any integer n > 0 and any δ ∈(0, 1), we have that with probability of at least 1 −δ over samples Sn,

LP (θ) ≤Ln(θ) + 2RadSn(ℓ◦Hθ) + 4c r

2 log(4/δ) n, where ℓ◦H:= {(x, y) 7→ℓ(h(x), y): h ∈H}. Specifically, if the loss function ℓ(·, ·) is L-Lipschitz in the first argument, we can have RadSn(ℓ◦H) = O(L · RadSn(H)) (c.f. Theorem 12 Bartlett & Mendelson, 2002).

With all these technical tools in hand, we now continue to prove Theorem A.10. Note that our kernel ridge regression objective is convex min θ {Ln(θ; λ)} = min θ

(

1 2n n X i=1

(N(xi; θ) −N ∗(xi))2 + λ

2 ∥θ∥2 2

)

.

Moreover, since

∇θLn(θ; λ) = 1 n n X i=1

⟨θ, ϕ(xi)⟩ϕ(xi) −1 n n X i=1

N ∗(xi)ϕ(xi) + λθ, we have by triangle inequality that

∥∇θLn(θ; λ) −∇θLn(θ′; λ)∥2 ≤(b2 + λ)∥θ −θ′∥2, i.e., the loss objective is smooth. Hence, we know that GD converges to the global minimum θ∗ λ of the regularized loss objective if using a small enough step size η < 2/(b2 + λ). Moreover, since Ln(θ∗ λ; λ) ≤Ln(θ∗; λ) and Ln(θ∗) = 0, we have λ

2 ∥θ∗ λ∥2

2 ≤Ln(θ∗ λ) + λ

2 ∥θ∗ λ∥2

2 = λ 2 ∥θ∗∥2 2, i.e., ∥θ∗ λ∥2 ≤∥θ∗∥2. Now, we know N(xi; θ∗ λ) ∈Hθ(∥θ∗∥2).

Note that, in order to apply Lemma A.13 to Hθ(∥θ∗∥2), we need to argue the Lipschitzness of the loss function. While the squared loss is not Lipschitz globally, it is indeed Lipschitz on a bounded domain. Since we assume that ∥ϕ(x)∥2 ≤b for some universal constant b > 0, we have for any N(x; θ) ∈Hθ(∥θ∗∥2),

|N(x; θ)| = | ⟨θ, ϕ(x)⟩| ≤∥θ∥2 · ∥ϕ(x)∥2 ≤b∥θ∗∥2.

Hence, the squared loss is 4b∥θ∗∥2-Lipschitz in the first argument for Hθ(∥θ∗∥2). Next, we argue the boundedness of the squared loss objective. This is clear since for any N(x; θ) ∈Hθ(∥θ∗∥2), we have

|ℓ(N(x; θ), y)| = (N(x; θ) −N(x; θ∗))2 ≤4b2∥θ∗∥2

2.

Additionally, we also have L = 1 n

Pn i=1∥ϕ(xi)∥2

2 ≤b2.

Now, applying the uniform convergence (Lemma A.13), we get with probability at least 1 −δ,

L(θ∗ λ) ≤2Ln(θ∗ λ) + Cb2∥θ∗∥2

2 √n + 16b2∥θ∗∥2

2 r

2 log(4/δ) n, where C > 0 is some universal constant. Finally, for any ϵ > 0, if the following holds:

n ≥max

4C2b4∥θ∗∥4

2 ϵ2, 2048b4∥θ∗∥4

2 ϵ2 log

4 δ

, then we have

Cb2∥θ∗∥2

2 √n + 16b2∥θ∗∥2

2 r

2 log(4/δ) n ≤ϵ

2 + ϵ 2 ≤ϵ.

Therefore, with probability at least 1 −δ, we have L(θ∗ λ) ≤2Ln(θ∗ λ) + ϵ.

<!-- Page 22 -->

Provable Grokking in Ridge Regression

Remark A.14. We discuss how to derive our bounds in Equation (8) when assuming specific distributions over features. Specifically, under the setting and notations of Theorem 4.2, we assume further that ϕ(x1),..., ϕ(xn) are drawn i.i.d. from N(0, 1 mIm). For any ϵ > 0, we also assume that m = Ω(∥θ∗∥2

2/ϵ). The bounds then follow directly from applying Theorem 4.2. Since ϕ(x1),..., ϕ(xn) are i.i.d. N(0, 1 mIm) random variables, we can have b2 = 3/2 with high probability and λmin(Σ) = 1/m. Moreover, since θ(0) ∼N(0, ν2Im), we have mν2/2 ≤∥θ(0)∥2

2 ≤3mν2/2 with high probability. For t1, we have t1 ≤ n ln

6b2∥θ(0)∥2 2 ϵ

2ηλ+ min(Φ⊤Φ) ≤ n ln

14mν2 ϵ

2ηλ+ min(Φ⊤Φ).

For t2, note that according to the assumption, we have c = ϵ and ϵ > λmin(Σ)∥θ∗∥2

2 = ∥θ∗∥2 2/m and thus

(m −n)ν2

2 r c λmin(Σ) + ∥θ∗∥2

−2

≥(m −n)ν2

8mϵ.

Moreover, to get a better approximation, we note that the inequality ln(1 −ηλ) ≥−2ηλ used in the proof of Theorem A.7 is loose when λ is sufficiently small. Instead, we can have ln(1 −ηλ) ≥−1.01ηλ when ηλ ≤0.01. This gives a more tight bound followed from the same analysis:

t2 ≥ ln

(m−n)ν2

2 q c λmin(Σ) + ∥θ∗∥2

−2!

2.02ηλ ≥ ln

(m−n)ν2

8mϵ

2.02ηλ.

Putting together, we get t2 ≥ ln

(m−n)ν2

8mϵ

2.02ηλ and t1 ≤ n ln

14mν2 ϵ

2ηλ+ min(Φ⊤Φ).

B. Additional Experiments

In this section we provide several additional experiments.

First, we define a threshold-based surrogate accuracy metric by

Px

N(x; θ(t)) −N ∗(x)

2

≤ϵ for a fixed ϵ > 0. Evaluating our model under this metric reveals the familiar plateauing phenomenon experimentally (Figure 5). This confirms that the plateau can be recovered in linear regression under appropriate evaluation, offering a promising direction for future theoretical analysis.

**Figure 5.** Plotting the grokking by evaluating the surrogate loss (an accuracy-type metric) compared to evaluating the actual loss. The data

for the two plots are collected from a single simulation. We set m = 10000, d = 100, n = 100, η = 1, λ = 10−5 and ϵ = 0.01.

![Figure extracted from page 22](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-022-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-022-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 23 -->

Provable Grokking in Ridge Regression

We also observe grokking in ridge regression with labels that are contaminated with mean-zero variance-std2 Gaussian noise (Figure 6).

**Figure 6.** Ridge regression with label noise — Left: We set m = 5000, d = 50, n = 100, η = 1, std = 0.1 and λ = 10−5; Right: We

notice that different noise levels do not affect the grokking time by much. We set m = 5000, d = 50, n = 100, η = 1, and λ = 10−5.

Finally, we observe grokking in the following setting. We study training a random Fourier feature network to learn a randomly-initialized realizable teacher. We implemented the random Fourier feature map ϕ(x) = p

2/m cos(W x + b) where each row of W is sampled from N(0, σ2I) and each entry of b is sampled from Uniform([0, 2π]). Our randomlyinitialized realizable teacher is a single such Fourier feature function generated from the same distribution. We note that this setting requires careful hyperparameter tuning to observe grokking (Figure 7).

**Figure 7.** Random Fourier features — we set m = 5000, d = 10, n = 100, η = 1, σ2 = 1 and λ = 10−4.

C. Technical Lemmas

Lemma C.1 (Chi-squared Concentration). Let w ∈Rd such that w ∼N(0, σ2Id) for some σ2 > 0. For all t ∈(0, 1),

P

1 dσ2

∥w∥2

2 −dσ2 ≥t

≤2e−dt2/8.

![Figure extracted from page 23](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-023-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-023-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-to-grok-grokking-provable-grokking-in-ridge-regression/page-023-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
