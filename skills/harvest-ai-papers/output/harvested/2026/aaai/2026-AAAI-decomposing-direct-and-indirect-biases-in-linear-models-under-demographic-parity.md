---
title: "Decomposing Direct and Indirect Biases in Linear Models Under Demographic Parity Constraint"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39793
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39793/43754
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Decomposing Direct and Indirect Biases in Linear Models Under Demographic Parity Constraint

<!-- Page 1 -->

Decomposing Direct and Indirect Biases in Linear Models Under Demographic

Parity Constraint

Bertille Tierny1,2, Arthur Charpentier3, Franc¸ois Hu1

1Milliman France, R&D Department, Paris AI Lab 2ENSAE - Institut Polytechnique de Paris 3Universit´e du Qu´ebec `a Montr´eal bertille.tierny@milliman.com, charpentier.arthur@uqam.ca, francois.hu@milliman.com

## Abstract

Linear models are widely used in high-stakes decisionmaking due to their simplicity and interpretability. Yet when fairness constraints such as demographic parity are introduced, their effects on model coefficients, and thus on how predictive bias is distributed across features, remain opaque. Existing approaches on linear models often rely on strong and unrealistic assumptions, or overlook the explicit role of the sensitive attribute, limiting their practical utility for fairness assessment. We propose a post-processing framework that can be applied on top of any linear model to decompose the resulting bias into direct (sensitive-attribute) and indirect (correlated-features) components. Our method analytically characterizes how demographic parity reshapes each model coefficient, including those of both sensitive and nonsensitive features. This enables a transparent, feature-level interpretation of fairness interventions and reveals how bias may persist or shift through correlated variables. Our framework requires no retraining and provides actionable insights for model auditing and mitigation. Experiments on both synthetic and real-world datasets demonstrate that our method captures fairness dynamics missed by prior work, offering a practical and interpretable tool for responsible deployment of linear models.

Code — https://github.com/bias-mitigator/interpretable.git

## Introduction

Linear models remain a foundational tool in statistical learning due to their interpretability, scalability, and simplicity (Hastie et al. 2009). They are widely used in high-stakes domains such as credit scoring, hiring, insurance, and healthcare, where algorithmic decisions have significant consequences and fairness considerations are critical (Obermeyer et al. 2019; Barocas, Hardt, and Narayanan 2023). In these settings, linear models may inadvertently encode or amplify unfair biases. These biases can arise directly, through the explicit use of sensitive attributes such as race or gender, or indirectly, through features correlated with those attributes (Hajian and Domingo-Ferrer 2012; Nabi and Shpitser 2018; Tang, Zhang, and Zhang 2023). Fairness in machine learning has been extensively studied, with various formal definitions

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

and mitigation strategies proposed (Del Barrio, Gordaliza, and Loubes 2020; Mehrabi et al. 2021; Pessach and Shmueli 2022). One of the most common criteria is Demographic Parity (DP), which requires that the predictions be statistically independent of sensitive attributes. Although many methods aim to enforce DP in classification settings (Agarwal et al. 2018; Gaucher, Schreuder, and Chzhen 2023; Hu, Ratz, and Charpentier 2024; Denis et al. 2024), few provide systematic tools to quantify and separate the sources of unfairness, especially in linear models. In particular, existing approaches, such as (Chzhen and Schreuder 2022; Fukuchi and Sakuma 2023), do not provide a systematic decomposition of bias stemming from the sensitive feature versus that induced by correlated non-sensitive features. The absence of a clear decomposition is particularly limiting for linear models: despite their transparency, it remains unclear how fairness constraints modify individual coefficients. Consequently, practitioners lack insight into how these constraints redistribute predictive weight across features or whether indirect biases persist after the removal of sensitive variables.

## 1.1 Main Contributions

We propose a framework for learning fair linear models, designed to identify and mitigate both indirect and direct biases in linear models. Specifically:

• We introduce a linear modeling framework aligned with standard practices and derive a closed-form solution for the optimal fair regressor. To our knowledge, this is the first solution that remains linear under group-wise feature standardization. In practice, it can be applied on top of any linear model (penalized, with or without intercept) making it broadly compatible and easily deployable. • Building on this optimal solution, we disentangle the contributions of sensitive and non-sensitive features to fairness violations (see Fig. 1) while providing clear guidance on how to adjust coefficients toward fairness. • We illustrate the effectiveness of our approach on both synthetic and real-world datasets, demonstrating its ability to produce fair linear models while offering interpretability of both direct and indirect biases.

This work advances the understanding of fairness in linear models and contributes to the broader literature by providing tools to dissect and interpret bias at the feature level. For

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

25932

<!-- Page 2 -->

Total Unfairness

First-Moment Disparity

(Mean Bias)

Second-Moment Disparity

(Indirect Structural Bias)

Indirect Direct Interaction

Arises from group dis- parities in the feature covariance structure

**Figure 1.** Conceptual decomposition of the total unfairness measure.The unfairness splits into two bias sources: disparities in the mean of predictions (First-Moment) and disparities in the variance of predictions (Second-Moment).

clarity of presentation, all proofs are provided in the supplementary materials.

## 1.2 Related Work

The study of fairness constraints in linear regression, particularly under DP, is relatively recent. Most existing methods either focus on model-level fairness objectives or rely on restrictive assumptions that limit their applicability in practice.

(Chzhen and Schreuder 2022) propose a minimax solution for linear regression under DP, deriving a closed-form intercept correction. However, their formulation is based on a strong assumption: the sensitive feature is independent of the other covariates. Therefore, they are omitting completely the indirect biases. This assumption rarely holds in real-world data and significantly restricts both the predictive accuracy of the model and the relevance of its fairness guarantees.

(Fukuchi and Sakuma 2023) extend this line of work by adjusting both intercept and non-sensitive feature coefficients. Although this allows more flexibility, their framework still omits an explicit treatment of the sensitive feature’s contribution, which limits bias diagnostics. Moreover, their solution also still builds on simplifying assumptions that may distort the fairness-performance trade-off.

In contrast, our approach explicitly characterizes the effect of DP constraints on all model components, including the sensitive feature. This enables a fine-grained decomposition of direct and indirect biases and provides clearer insights into how fairness interventions affect both predictive behavior and feature-level fairness contributions.

## 1.3 Outline of the Paper The remainder of this article is structured as follows:

Section 2, introduces the problem setup and the key metrics

Direct (Mean) Indirect (Mean) Interaction Indirect [CS22] ✓ ✓ [FS23] ✓ ✓ ✓ ours ✓ ✓ ✓ ✓

**Table 1.** Comparison of bias mitigation methods across linear models proposed by [CS22] (Chzhen and Schreuder 2022), [FS23] (Fukuchi and Sakuma 2023), and our approach. Checkmarks indicate addressed biases.

used throughout the article. Section 3 reviews the limitations of existing fair linear models. Section 4 presents our main contribution: a general framework for learning optimal fair linear models. This is followed in Section 5 by a decomposition of unfairness into direct and indirect biases. Finally, Section 6 details the practical implementation of our methodology and Section 7 presents numerical results comparing our method to state-of-the-art baselines.

## Problem Formulation

Let (X, S, Y) be a random triplet, where X ∈X ⊂Rd is a non-sensitive feature vector, Y ∈Y ⊂R is the target variable, and S ∈S = [M] is a discrete sensitive attribute where [M]:= {1,..., M}. We define ps = P(S = s) for all s ∈[M]. Our goal is to find a predictor f: X × S →Y from a set F that balances predictive utility with fairness. We denote by νf the distribution of f(X, S), and by νf|s its distribution given S = s. We make the following standard assumption.

Assumption 1. For f ∈F, measures (νf|s)s∈[M] are non atomic with finite second moments.

We evaluate any predictor f along three key and potentially competing dimensions: predictive risk, fairness, and goodness-of-fit. Each is formally defined below.

## 2.1 Measuring Risk

We measure the predictive performance of a predictor using the classical quadratic risk, defined as:

R(f) = E

(f(X, S) −Y)2

.

This risk is uniquely minimized by the Bayes optimal predictor f ∗(X, S) = E[Y | X, S], recognizing that fairness constraints entail a trade-off with this optimal benchmark.

## 2.2 Measuring Unfairness

Our work is grounded in the concept of Demographic Parity, which exists in both a weak and a strong form. In particular, a predictor f satisfies Weak DP if its expectation is independent of the sensitive attribute. That is,

E[f(X, S) | S = s] = E[f(X, S)], for all s ∈[M], ensuring fairness at the level of the first moment (the mean).

Definition 2 ((Strong) Demographic Parity). A predictor f satisfies Strong DP if its entire output distribution is independent of the sensitive attribute. That is, νf|s = νf for all s ∈[M].

This is a much stricter criterion, requiring equivalence of all statistical moments.

Unfairness Measure. We quantify unfairness through the lens of Strong DP, using Wasserstein-2 (W2) to measure distributional dissimilarities. For further details, we refer the reader to (Santambrogio 2015). Specifically, the unfairness of a predictor f is defined as the weighted sum

25933

<!-- Page 3 -->

of W2 distance between the group-conditional distributions (νf|s)s∈[M] and their common barycenter:

U(f) = min ν∈P2(R)

M X s=1 psW2

2(νf|s, ν). (1)

A predictor f is said to be exactly fair, that is, U(f) = 0 iff the predictor satisfies Strong DP. Thus, it provides a measure of how far a model is from achieving exact fairness.

## 2.3 Measuring Goodness-of-fit

Evaluating fair regression models requires more than assessing overall risk and unfairness. A key consideration is the group-conditional adequacy of the model. The classical coefficient of determination defined as R2(f) = Var(f(X, S))/Var(Y) is a standard metric for explained variance, particularly in linear settings. While it provides a familiar baseline, R2 can obscure performance disparities and fails to capture group-specific goodness-of-fit. For example, a linear model may approximate one group well but fit another poorly, a limitation not revealed by R2.

Group-Weighted Coefficient of Determination (GWR2). To diagnose this critical issue, we use the Group-Weighted R2 (GWR2). This metric is the average of the R2 computed independently within each sensitive group, providing a direct measure of how well a model fits the data, on average, for all populations under consideration. For a predictor f, the definition is:

GWR2(f):=

X s∈S psR2 s(f), where,

R2 s = 1 −Var(Y −f(X, s) | S = s)

Var(Y | S = s),

The strength of this metric is theoretically grounded in our analysis of the gap between GWR2 and the global R2. Divergence between these two metrics indicates model failure to capture group-specific structures. Thus, GWR2 is a necessary diagnostic to signal structural mismatch that global metrics can obscure.

## Limitations

of Existing Fair Linear Models The existing literature on fair linear regression provides foundational solutions but often relies on simplifying assumptions about the data-generating process. We review two key works that represent the progression from handling direct bias to incorporating some forms of indirect bias.

Mitigating Direct Bias. (Chzhen and Schreuder 2022) consider a hypothesis where unfairness arises solely from a group-dependent intercept term:

Y = ⟨X, βCS22⟩+β(s)

0,CS22+ζ, where ζ ∼N(0, 1), (2)

with the key assumption that features are independent of the sensitive group, i.e., X ⊥⊥S. In this setting, the associated Bayes optimal predictor is ⟨X, βCS22⟩+β(s)

0,CS22. The independence assumption eliminates all sources of indirect bias by construction, isolating direct bias as the only source of unfairness. Therefore, achieving fairness is straightforward.

Lemma 3 (Adapted from (Chzhen and Schreuder 2022)). Given the equation in Eq. (2), the optimal DP-fair predictor is obtained by averaging out the group-specific intercepts:

fCS22(x, s) = ⟨x, βCS22⟩+

X s∈[M]

psβ(s)

0,CS22.

Mitigating Indirect Mean Bias. (Fukuchi and Sakuma 2023) relax the feature independence assumption, allowing for group-dependent feature means and slopes:

Y = ⟨X, β(S)

F S23⟩+ ζ, where ζ ∼N(0, 1), (3)

where X ∼N(µ(s), σ2

XI). This structure introduces an indirect bias that results from the differing feature means µ(s). However, it maintains a restrictive assumption of homoscedastic, uncorrelated features across groups.

Lemma 4 (Adapted from (Fukuchi and Sakuma 2023), Lemma 1). Given the model in Eq. (3), the optimal DP-fair predictor is:

fF S23(x, s) = ∥β(.)

F S23∥⟨˜β(s)

F S23, x −µ(s)⟩

+

X s′∈[M]

ps′⟨β(s′)

F S23, µ(s′)⟩, with

∥β(.)

F S23∥=

X s∈[M]

ps∥β(s)

F S23∥ and ˜β(s)

F S23 = β(s)

F S23 ∥β(s)

F S23∥

.

## Limitations

of Prior Work. While these works represent important progress, they rely on restrictive assumptions about the data covariance structure. In particular, they do not address heteroscedasticity, where the feature covariance matrix Σ(s) varies across groups. As a result, it overlooks indirect structural bias from distributional disparities, highlighting the need for a more general approach.

## 4 A General Framework for Optimal Fair

Regression

We introduce a linear model framework that captures all key sources of bias, enabling us to derive the optimal fair predictor for more complex, group-dependent data structures.

## 4.1 The General Model

We consider a setting where the outcome Y is generated by:

Y = ⟨X, β∗⟩+ γ∗S + β∗

0 + ζ, (4)

where the features X | S = s ∼N(µ(s), Σ(s)) are groupdependent, and the noise ζ ∼N(0, 1) is independent of S and X. This model captures direct bias (γ∗), indirect mean bias (µ(s)), and indirect structural bias (Σ(s)).

Our goal is to find the optimal predictor within the class of linear models, Flinear, that minimizes the quadratic risk R subject to Strong DP. Given (x, s) ∈X × S, the Bayes optimal predictor is f ∗(x, s) = ⟨x, β∗⟩+ γ∗s + β∗

0.

25934

<!-- Page 4 -->

## 4.2 The Optimal Risk-Fairness Trade-off

We seek to find the predictor that optimally navigates the trade-off between minimizing risk and ensuring fairness. To formalize this, we adopt the ε-Relative Fairness Improvement (ε-RI) constraint from (Chzhen and Schreuder 2022). A predictor fε satisfies this constraint if its unfairness is bounded by an ε-fraction of the Bayes-optimal predictor:

U(fε) ≤ε · U(f ∗).

A key result, applicable to our framework, is that the predictor achieving the optimal risk-fairness trade-off under this constraint, i.e., verifying f ∗ ε ∈arg min{R(f): U(f) ≤ ε·U(f ∗)}, is a linear interpolation of the Bayes predictor f ∗ and the optimal fair predictor f ∗

DP:

f ∗ ε = (1 −√ε)f ∗

DP + √εf ∗.

Our main result is to derive the explicit closed-form expression for f ∗ ε within our Gaussian linear model framework.

## 4.3 Characterizing the Optimal Fair Predictor

To state our main result, we first define the group-conditional mean and standard deviation of the Bayes optimal score:

• Group-conditional mean:

µ(s)

f ∗:= E[f ∗(X, S) | S = s] = ⟨µ(s), β∗⟩+ γ∗s + β∗

0.

• Group-conditional variance:

(σ(s)

f ∗)2:= Var(f ∗(X, S) | S = s) = (β∗)⊤Σ(s)β∗.

We also define their population-level averages, weighted by the group prior probabilities ps:

¯µf ∗=

X s′∈[M]

ps′µ(s′)

f ∗ and ¯σf ∗=

X s′∈[M]

ps′σ(s′)

f ∗.

Proposition 5 (Optimal ε-Fair Predictor). For the model in Eq. (4), the unique predictor f ∗ ε that satisfies the ε-RI constraint and minimizes the quadratic risk is given by:

f ∗ ε (x, s) = σ(s)

ε

⟨x −µ(s), β∗⟩ σ(s)

f ∗

!

+ µ(s)

ε, (5)

where the mean and std are convex combinations of the group-specific and population-averaged statistics:

µ(s)

ε = (1 −√ε)¯µf ∗+ √εµ(s)

f ∗ σ(s)

ε = (1 −√ε)¯σf ∗+ √εσ(s)

f ∗.

The optimal exactly-fair predictor f ∗

DP is recovered at ε = 0, and the Bayes optimal predictor f ∗is recovered at ε = 1.

## 4.4 Interpreting the Fairness Mechanism

The structure of f ∗ ε reveals a clear and tunable mechanism for enforcing fairness, which can be understood from two complementary perspectives.

Perspective 1: Tunable Standardization and Averaging. This perspective views fairness as the controlled shift of group-dependent moments toward global average moments. 1. Group-wise Standardization: within each group s, the term ⟨x −µ(s), β∗⟩/σ(s)

f ∗creates a standardized score (zero mean and unit variance). This procedure simultaneously removes indirect mean and structural biases. 2. Controlled Re-scaling and Shifting: This standardized score is then re-scaled by σ(s)

ε and shifted by µ(s)

ε. These coefficients are a direct interpolation between the groupspecific moments (µ(s)

f ∗, σ(s)

f ∗) and the global averages (¯µf ∗, ¯σf ∗). The parameter ε directly control this tradeoff: at ε = 0, the predictor uses only global averages, eliminating all bias; at ε = 1, it uses only group-specific values, retaining all original bias for maximum accuracy.

Perspective 2: A Group-Conditional Fair Model. Alternatively, we can express the predictor as a linear model, f ∗ ε (x, s) = ⟨x, β(s)

ε ⟩+ β(s)

0,ε, to see how fairness is encoded into the parameters of the model. By rearranging the terms from Proposition 5, we find the effective slope and intercept for each group are:

β(s)

ε = σ(s)

ε σ(s)

f ∗

!

β∗ and β(s)

0,ε = µ(s) ε − σ(s)

ε σ(s)

f ∗

!

⟨µ(s), β∗⟩.

This view highlights that fairness is achieved by constructing a group-aware model with parameters systematically adjusted to counteract group-specific biases. The scaling factor σ(s)

ε /σ(s)

f ∗compensates for the structural bias, while the in- tercept β(s)

0,ε corrects for the mean-based biases.

## 5 Decomposition of Direct and Indirect

Biases Through the Unfairness In this section, we develop a comprehensive framework for understanding unfairness in linear regression.

## 5.1 Prediction-level Decomposition of Unfairness

We begin by decomposing our unfairness measure U(f) for any predictor within the class of linear models, Flinear. Proposition 6 (Linear Model Bias Decomposition). For any predictor f ∈Flinear with coefficients (β, γ, β0), its total unfairness U(f) decomposes into First-Moment Disparity (FMD) and Second-Moment Disparity (SMD):

U(f) = Var(E[f|S]) | {z } FMD

+ Var( p

Var(f|S)) | {z } SMD

. (6)

These components further decompose into four bias sources:

U(f) = γ2Var(S) | {z } Direct Mean

+ Var(⟨µ(S), β⟩) | {z } Indirect Mean

(7)

+ 2γCov(S, ⟨µ(S), β⟩) | {z } Interaction

+ Var p β⊤Σ(s)β

| {z } Indirect Structural

.

25935

<!-- Page 5 -->

This decomposition formalizes the conditions required to achieve Strong DP, showing that fairness in this stronger sense necessitates mitigating bias at two distinct levels:

• The First-Moment Disparity Var(E[f | S]) captures unfairness in average predictions. It arises from direct dependence on the sensitive attribute (Direct Mean Bias, related to Weak DP) or from correlations between group membership and feature means (Indirect Mean Bias).

• The Second-Moment Disparity Var(p

Var(f | S)) captures a more subtle form of unfairness (Indirect Structural Bias) where predictive certainty differs across groups due to variations in feature covariance Σ(s).

This decomposition reveals that a model can satisfy Weak DP (without FMD) while remaining unfair under Strong DP. The following corollary demonstrates a key advantage of our optimal ε-fair predictor:

Corollary 7 (Residual Unfairness of our method). The total unfairness of our predictor f ∗ ε, (see Prop. 5), is exactly:

U(f ∗ ε) = ε·Var(E[f ∗| S])+ε·Var( p

Var(f ∗| S)).

This corollary highlights a direct, analytical link between a single control parameter (ε) and the total amount of multisource unfairness, a property not available in prior models.

## 5.2 Feature-level Decomposition of Unfairness via Approximation

While the prediction-level decomposition quantifies total unfairness, practical intervention requires attributing this unfairness to individual features. A fully additive decomposition is challenging due to the nonlinearity introduced by the square root in the structural bias. To enable interpretability, we apply a first-order Taylor expansion to linearize this term, yielding a tractable and accurate additive approximation.

The Additive Case: Uncorrelated Features. We consider a simplified setting where features are mutually uncorrelated within each group (Σ(s) are diagonal matrices). In this case, the total indirect unfairness of any linear model decomposes into a sum of marginal contributions from each feature.

Proposition 8 (Additive Feature-Level Decomposition). Given f ∈Flinear with coefficients (β, γ), let its indirect unfairness be Uindirect(f) = U(f) −γ2Var(S). If all Σ(s) are diagonal, then this unfairness can be approximated by an additive sum:

Uindirect(f) ≈ d X j=1

Uapprox j (f), with the approximate main contribution from feature Xj is:

Uapprox j (f) = (βj)2Var(µ(S)

j) | {z } Mean

+ 1

4 ¯V (βj)4Var((σ(S) j)2) | {z } Structural

+ 2γβjCov(S, µ(S)

j) | {z } Interaction

, where µ(s)

j = E[Xj|S = s] and (σ(s)

j)2 = Var(Xj|S = s). Here, ¯V = E[Var(f|S)] is the average conditional score variance.

This proposition attributes model unfairness to individual features via three pathways: (1) mean disparity, (2) variance disparity (structural bias), and (3) interaction with direct bias. The term 1/(4 ¯V) indicates that structural bias diminishes as predictive variance increases.

The General Case: Interactional Unfairness. When features are correlated, the decomposition becomes more complex due to cross-terms capturing interactional unfairness. This includes: (1) the compounding of mean biases through correlated feature means, and (2) a deeper structural effect, which we term Covariance Disparity, driven by group-level differences in feature correlations.

This analysis provides both practical and comprehensive insight. The additive decomposition highlights features with primary unfairness, while the general case reveals how feature correlations amplify or mitigate these effects.

## 6 Practical Implementation and Estimation

To apply our framework in practice, the optimal fair predictor must be estimated from finite data, since the population parameters (β∗, γ∗, µ(s), Σ(s)) are unknown.

The Plug-in Estimator. The plug-in estimator ˆfε of f ∗ ε is constructed by replacing all quantities in Prop. 5 with their empirical estimates. 1. Estimate Model Parameters. We estimate the base model parameters (ˆβ, ˆγ, ˆβ0). Our framework is agnostic to the fitting procedure; any standard method, such as OLS or penalized version (Ridge, Lasso), is applicable. 2. Estimating Group Statistics. For each s, we compute the standard estimates for the group proportions ˆps, feature means ˆµ(s), and feature covariance matrices ˆΣ(s). 3. Assemble the Fair Predictor. Finally, these empirical components are used to construct the plug-in versions of the conditional score moments (ˆµ(s)

f, ˆσ(s)

f) and their population averages (ˆ¯µf, ˆ¯σf). These are then combined according to Prop. 5 to form the final estimator.

## Evaluation

Metrics. We evaluate all models on a held-out test set using empirical estimators of our three key metrics. For both the Risk and GWR2, we consider their empirical counterparts, denoted ˆR (mean squared error) and \ GWR2, respectively, where:

\ GWR2(f) =

X s∈[M]

ˆps

1 − d Var(Y −f | S = s)

d Var(Y | S = s)

!

.

We quantify the unfairness using the Kolmogorov-Smirnov (KS) test, as it is model-agnostic and does not rely on structural assumptions.

ˆUKS(f) = max sj,sk∈[M] DKS(ˆFf|sj, ˆFf|sk).

Here, ˆFf|s is the empirical CDF of scores for group s.

25936

<!-- Page 6 -->

**Figure 2.** Bias decomposition (see Prop. 6) of a base linear model on synthetic data using by default T = (3, 2, 3, 0.7).

**Figure 3.** Comparison of group-conditioned model output distribution on synthetic data using T = (10, 2, 2, 0.7).

## 7 Numerical Experiments

We run experiments on synthetic and real-world data to: (1) validate our bias decomposition framework, (2) illustrate the transparent remediation capability of our tunable predictor under complex bias scenario.

**Figure 4.** Coefficients adjustments for fairness, shown for a sample of features on synthetic data with T = (3, 2, 3,.7).

## 7.1 Application on Synthetic Data

We generated synthetic triplets (X, S, Y). The sensitive attribute S ∈{1, 2} is drawn from a Bernoulli distribution. Features X ∈Rd follow N(µ(s), Σ(s)) conditional on S = s, introducing indirect bias through groupspecific means, variances and correlations. The outcome Y = Pd j=1 Xj + Ty · S introduces direct bias via Ty. The data-generating process is governed by four control parameters T:= (Ty, Tmean, Tstd, Tcorr), mapping to our bias decomposition (Prop. 6). Setting a parameter to zero eliminates the corresponding bias source.

• Ty sets the direct bias coefficient γ∗; • Tmean introduces indirect mean bias by shifting group 2’s means: µ(2) = µ(1) + Tmean; • Tstd and Tcorr control indirect structural bias via group- specific standard deviations ( q

Σ(2)

jj = q

Σ(1)

jj + √Tstd)

and correlations structures within Σ(s): Tcorr = 0 yields independent features for both groups, while Tcorr ∈(0, 1) yields different correlation structures between groups.

Experimentation scheme. Given T, we create datasets of d = 5 features and n = 20, 000 samples and split it into training (50%), testing (25%), and unlabeled (25%) subsets. As a base model, we use linear regression of Y on (X, S), using scikit-learn default parameters. Coefficients of this regression serve as input to build of fair linear model.

**Figure 5.** Analysis of Approximate fairness model on synthetic data with T = (10, 2, 3, 0.7).

Validating the Bias Decomposition. Fig. 2 empirically validate our bias decomposition of a base linear model: increasing (Ty) inflates the Direct Mean and Interaction terms, while increasing Tmean and Tstd) primarily maps to the Indirect Mean and Indirect Structural bias components respectively. This confirms our decomposition effectively identifies the root causes of unfairness in linear models.

Fairness Mitigation and Robustness to Bias Shifts. In complex scenarios with full bias interactions T = (3, 2, 3, 0.7), our model uniquely preserves remediation capabilities (Fig. 3). The remediation operates through the fol-

25937

![Figure extracted from page 6](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Model

CRIME LAW GOSSIS GWR2 RMSE Unfairness GWR2 RMSE Unfairness GWR2 RMSE Unfairness Base Model Unaware.45 ±.05 0.15 ± 0.01 0.55 ± 0.04.15 ±.01 0.37 ±.00.13 ±.01.69 ±.01 10.3 ± 0.1.14 ±.01 Base Model.46 ±.05 0.15 ± 0.01 0.61 ± 0.04.15 ±.01 0.37 ±.00.43 ±.02.69 ±.01 10.3 ± 0.1.15 ±.01 CS22.46 ±.05 0.15 ± 0.01 0.54 ± 0.04.15 ±.01 0.37 ±.00.08 ±.01.69 ±.01 10.3 ± 0.1.14 ±.01 FS23.35 ±.09 0.19 ± 0.01 0.20 ± 0.05.08 ±.05 0.39 ±.01.15 ±.05.51 ±.40 12.5 ± 3.3.13 ±.07 Our model.38 ±.07 0.19 ± 0.01 0.12 ± 0.04.15 ±.01 0.37 ±.00.07 ±.02.69 ±.01 10.4 ± 0.1.03 ±.01

**Table 2.** Comparison of model performances across all datasets. Results are presented as mean ± standard deviation over 50 runs. Bold cells indicate the lowest unfairness.

lowing mechanisms (Fig. 4): (1) direct bias elimination via sensitive attribute coefficient nullification and equal intercept compensation; (2) indirect mean bias correction through asymmetric intercept adjustment (group 1 receives larger positive shift to offset lower means); (3) structural bias remediation via group-specific coefficient scaling (upward for group 1, downward for group 2) and modified intercept adjustments accounting for variance differences; (4) correlation refinement adapting coefficients and intercepts to group-specific dependence structures. All adjustments maintain overall predictive accuracy.

**Figure 6.** Analysis of Model performance w.r.t. direct bias shifts (Ty) on synthetic data using T = (∗, 2, 2, 0.7).

We also test robustness under direct bias shifts by increasing Ty (Fig. 6). Our method and CS22 remain stable in both performance and fairness, while FS23 deteriorates.

Tracing the Optimal Risk–Fairness Frontier. Under ε- RI constraint, ε provides continuous control over the desired fairness level. In a full bias scenario (Fig. 5), our method either achieves higher accuracy than baselines at a given unfairness level, or ensures lower unfairness at a given accuracy.

## 7.2 Results on Real-World Data

We use three benchmarks. (1) GOSSIS (Raffa et al. 2022) contains medical data from over 130,000 patients admitted to intensive care units. The task consists in predicting the vital variable h1 diaspb max with ethnicity as protected attribute. (2) CRIME (Redmond and Baveja 2002) includes US communities’ demographic and crime data with 1994 samples. We predict the number of violent crimes per 105 population with a sensitive attribute based on Black population percentage (Calders et al. 2013). (3) LAW covers law school admissions. We predict normalized GPA using race as protected attribute.

**Figure 7.** Analysis of coefficient shifts from the linear model to our fair model on the CRIME dataset.

Comparison w.r.t state-of-the-art. Experimental results (Table 2) shows our model effectively reduces unfairness while maintaining competitive predictive performance. The Unaware baseline confirms that omitting the sensitive attribute fails to eliminate discrimination. On LAW, where direct bias dominates, CS22 performs well by mitigating this bias component; nevertheless, our model achieves lower unfairness. Compared to the best-performing baselines, we achieve substantial unfairness reduction for each dataset, while preserving competitive accuracy.

Feature-level interpretation on CRIME Dataset. While the direct bias is nullified (Fig. 7), the model mitigates indirect biases through group-specific coefficient adjustments.

## Conclusion

We propose a closed-form solution for fair linear regression that enables exact control over the risk-fairness trade-off via the optimal predictor f ∗ ε. Building upon this Gaussian framework, we introduce a novel decomposition of unfairness into direct and indirect components, highlighting four distinct sources, including the previously overlooked Indirect Structural Bias arising from disparities in predictive variance.

Our results demonstrate that mean-based fairness alone is insufficient. By explicitly accounting for structural disparities, our method ensures fairness in both average predictions and predictive certainty across groups. The decomposition, along with the Group-Weighted R2, provides actionable tools for diagnosing unfairness in linear models. While grounded in Gaussian assumptions, our approach shows strong empirical robustness on real-world data. Future work may extend these insights to non-linear models and broader fairness notions.

25938

![Figure extracted from page 7](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-decomposing-direct-and-indirect-biases-in-linear-models-under-demographic-parity/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## References

Agarwal, A.; Beygelzimer, A.; Dud´ık, M.; Langford, J.; and Wallach, H. 2018. A reductions approach to fair classification. In International conference on machine learning, 60–69. PMLR. Barocas, S.; Hardt, M.; and Narayanan, A. 2023. Fairness and machine learning: Limitations and opportunities. MIT press. Calders, T.; Karim, A.; Kamiran, F.; Ali, W.; and Zhang, X. 2013. Controlling attribute effect in linear regression. In 2013 IEEE 13th international conference on data mining, 71–80. IEEE. Chzhen, E.; and Schreuder, N. 2022. A minimax framework for quantifying risk-fairness trade-off in regression. The Annals of Statistics, 50(4): 2416–2442. Del Barrio, E.; Gordaliza, P.; and Loubes, J.-M. 2020. Review of mathematical frameworks for fairness in machine learning. arXiv preprint arXiv:2005.13755. Denis, C.; Elie, R.; Hebiri, M.; and Hu, F. 2024. Fairness guarantees in multi-class classification with demographic parity. Journal of Machine Learning Research, 25(130): 1– 46. Fukuchi, K.; and Sakuma, J. 2023. Demographic parity constrained minimax optimal regression under linear model. Advances in Neural Information Processing Systems, 36: 8653–8689. Gaucher, S.; Schreuder, N.; and Chzhen, E. 2023. Fair learning with Wasserstein barycenters for non-decomposable performance measures. In International Conference on Artificial Intelligence and Statistics, 2436–2459. PMLR. Hajian, S.; and Domingo-Ferrer, J. 2012. A methodology for direct and indirect discrimination prevention in data mining. IEEE transactions on knowledge and data engineering, 25(7): 1445–1459. Hastie, T.; Tibshirani, R.; Friedman, J. H.; and Friedman, J. H. 2009. The elements of statistical learning: data mining, inference, and prediction, volume 2. Springer. Hu, F.; Ratz, P.; and Charpentier, A. 2024. A sequentially fair mechanism for multiple sensitive attributes. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 12502–12510. Mehrabi, N.; Morstatter, F.; Saxena, N.; Lerman, K.; and Galstyan, A. 2021. A survey on bias and fairness in machine learning. ACM computing surveys (CSUR), 54(6): 1–35. Nabi, R.; and Shpitser, I. 2018. Fair inference on outcomes. In Proceedings of the AAAI conference on artificial intelligence, volume 32. Obermeyer, Z.; Powers, B.; Vogeli, C.; and Mullainathan, S. 2019. Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464): 447–453. Pessach, D.; and Shmueli, E. 2022. A review on fairness in machine learning. ACM Computing Surveys (CSUR), 55(3): 1–44. Raffa, J. D.; Johnson, A. E. W.; O’Brien, Z.; Pollard, T. J.; Mark, R. G.; Celi, L. A.; Pilcher, D.; and Badawi, O. 2022.

The Global Open Source Severity of Illness Score (GOS- SIS). Critical Care Medicine, 50(7): 1040–1050. Redmond, M.; and Baveja, A. 2002. A data-driven software tool for enabling cooperative information sharing among police departments. European Journal of Operational Research, 141(3): 660–678. Santambrogio, F. 2015. Optimal transport for applied mathematicians. Springer. Tang, Z.; Zhang, J.; and Zhang, K. 2023. What-is and howto for fairness in machine learning: A survey, reflection, and perspective. ACM Computing Surveys, 55(13s): 1–37.

25939
