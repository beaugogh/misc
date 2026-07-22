---
title: "Streaming Generated Gaussian Process Experts for Online Learning and Control"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39993
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39993/43954
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Streaming Generated Gaussian Process Experts for Online Learning and Control

<!-- Page 1 -->

Streaming Generated Gaussian Process Experts for Online Learning and Control

Zewen Yang1, Dongfa Zhang1, Xiaobing Dai2, Fengyi Yu1, Chi Zhang3, Bingkun Huang1,

Hamid Sadeghian1, Sami Haddadin4

1Chair of Robotics and Systems Intelligence, Munich Institute of Robotics and Machine Intelligence, Technical University of Munich 2School of Computation, Information and Technology, Technical University of Munich 3Department of Informatics, School of Computation, Information and Technology, Technical University of Munich 4Mohamed bin Zayed University of Artificial Intelligence zewen.yang@tum.de

## Abstract

Gaussian Processes (GPs), as a nonparametric learning method, offer flexible modeling capabilities and calibrated uncertainty quantification for function approximations. Additionally, GPs support online learning by efficiently incorporating new data with polynomial-time computation, making them well-suited for safety-critical dynamical systems that require rapid adaptation. However, the inference and online updates of exact GPs, when processing streaming data, incur cubic computation time and quadratic storage memory complexity, limiting their scalability to large datasets in real-time settings. In this paper, we propose a streaming kernel-induced progressively generated expert framework of Gaussian processes (SkyGP) that addresses both computational and memory constraints by maintaining a bounded set of experts, while inheriting the learning performance guarantees from exact Gaussian processes. Furthermore, two SkyGP variants are introduced, each tailored to a specific objective, either maximizing prediction accuracy (SkyGP-Dense) or improving computational efficiency (SkyGP-Fast). The effectiveness of SkyGP is validated through extensive benchmarks and real-time control experiments demonstrating its superior performance compared to state-of-the-art approaches.

Code — https://github.com/Zewen-Yang/SkyGP Extended version — https://arxiv.org/abs/2508.03679

## Introduction

Real-time learning has become essential for modeling the dynamics of physical systems, where machine learning models must be continuously updated to adapt to changing environments while satisfying the requirements of responsiveness and safety. This capability is especially critical for autonomous systems, such as underwater vehicles, aerial drones, and healthcare robots, that operate in complex and safety-critical environments (Yang et al. 2025a). In such scenarios, the ability to learn accurate models online and seamlessly integrate them into control loops is key to ensuring robust and efficient operation (Dai et al. 2023).

Gaussian Processes (GPs) provide a powerful nonparametric framework for modeling dynamical systems, particularly in safety-critical applications, due to their ability

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

to quantify uncertainty (Wachi et al. 2018). However, despite their modeling flexibility, standard GP inference suffers from severe scalability limitations. It scales cubically with the number of data points, requiring O(N 3) time and O(N 2) memory for N training data. This scalability bottleneck makes conventional GPs impractical for online applications involving continuously streaming data or long-term deployments.

To mitigate these limitations, a variety of scalable approximation techniques have been developed. Among global approximations, sparse Gaussian Processes introduce a set of M ≪N inducing points to efficiently summarize the training data, reducing the complexity to O(NM 2) for training and O(M 2) for prediction. Notable methods include fully independent training conditional approximation (Snelson and Ghahramani 2005), variational free energy (Naishguzman and Holden 2007), and latent projection techniques (Reeb et al. 2018). While streaming variants such as incremental sparse spectrum GP (ISSGP) (Gijsberts and Metta 2013) and streaming sparse GP (SSGP) (Bui, Nguyen, and Turner 2017) allow for incremental online updates, these frequently require computationally expensive optimization at each update, which can undermine their practical use in latency-sensitive settings. Moreover, these methods typically forgo guarantees on prediction error bounds, sacrificing reliability in critical applications.

Distributed Gaussian Processes (DGPs) provide complementary scalability by partitioning data across multiple processors or agents for parallel processing. Within this paradigm, mixture-of-experts (MoE) approaches (Tresp 2000b; Yuan and Neubauer 2008; Trapp et al. 2020) aggregate predictions from independently trained GP experts using fixed or learned weights. Extensions such as productof-experts (PoE) (Cohen et al. 2020), generalized PoE (gPoE) (Cao and Fleet 2015), and correlated PoE with sparse GPs (Sch¨urch et al. 2023) have been proposed to better utilize uncertainty in aggregation. The Bayesian committee machine (BCM) (Tresp 2000a) and its robust variant (rBCM) (Deisenroth and Ng 2015; Liu et al. 2018) explicitly integrate the GP prior to mitigate overconfidence. To address real-time learning problems within distributed frameworks, Lederer et al. (2021) proposed LoG-GP, which incrementally constructs a tree-structured ensemble of GP experts of-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27719

<!-- Page 2 -->

fering a scalable solution for DGPs. However, the reliance on partitioning along a single dimension limits effectiveness in high-dimensional spaces. The structure of DGPs enables parallel and distributed deployment, with each GP model hosted on a separate computational node or agent. This is widely employed in multi-agent systems, where agents can independently operate local GPs and collaborate through a communication network for cooperative learning (Yang et al. 2021, 2024a,b; Lederer et al. 2023). Nevertheless, these methods overlook online learning requirements, particularly the need to efficiently incorporate new observations and adapt to nonstationary environments (Yuan and Zhu 2024; Dai et al. 2024, 2025). While Yang, Dai, and Hirche (2025) tackle asynchronous communication, their computation-aware random splitting strategy fails to exploit spatial or temporal correlations in the streaming data.

These limitations motivate our streaming kernel-induced progressively generated expert framework for Gaussian processes (SkyGP), which handles non-stationary, streaming data by dynamically allocating GP experts based on kernel similarity and temporal recency. Our main contributions:

• We propose a progressive expert generation strategy that leverages kernel-induced centers to determine whether incoming data should be incorporated into an existing expert model or used to initialize a new one. SkyGP enables dynamic partitioning of streaming data and addresses the limitations of the state-of-the-art (SOTA) approaches. • We develop a time-aware and configurable expert aggregation framework that incorporates temporal weighting to effectively manage the generated GP experts. The framework adapts to system constraints, such as memory and computational budgets, while ensuring bounded complexity during both training and inference. • We provide a learning-based policy for dynamical system control tasks with a rigorous theoretical analysis. The main theorem reveals the relationship between model uncertainty and control performance. • We validate the proposed approach on real-world benchmark datasets and real-time control tasks. Extensive experiments demonstrate that the Sky-GP outperforms SOTA methods in terms of prediction accuracy, computational efficiency, and closed-loop control performance.

Problem Statement and Preliminaries

This paper investigates the problem of online function approximation in a streaming data environment for learning and control tasks. The objective is to infer an unknown target function f(·): Rm →R using a estimated function ˆf(·) based on given an sequential stream of input-output data pairs (xs, ys) indexed by s →∞, where m, s ∈N>0. Each input xs ∈Rm is paired with an output ys = f(xs)+ε ∈R, where the noise ε follows a normal distribution with zero mean and variance σ2 n, and σn ∈R>0. Gaussian Processes represent a Bayesian non-parametric approach commonly employed for function regression and approximation tasks. It assumes that the target function f(·) is sampled from a GP prior, denoted as f(·) ∼

GP(m(·), κ(·, ·)), where m(·) is the mean function (often set to zero when no prior knowledge is assumed) (Rasmussen and Williams 2006) and κ(·, ·) is the covariance kernel (e.g., the squared exponential kernel). With the streaming observations accumulated up to time step tk ∈ R≥0 forming the dataset D(tk) = {(xs, ys)}s=1,2,...,N(tk), where N(tk) = |D(tk)|, the posterior mean and variance functions of the GP can be derived as follows µ(x) = κ(x, X)α, σ2(x) = κ(x, x) −vT v, (1) where κ(x, X) = [κ(x, xs)]s=1,...,N(tk) is the covariance vector between the test input x and training inputs X = [x1,..., xN(tk)], and α, v are computed using the Cholesky decomposition L = cholesky(K + σ2 nI) as α = L⊤\(L⊤\y), v = L\κ(x, X) (2)

with the training output y = [y1,..., yN(tk)]⊤. The kernel matrix K is defined by its elements Kij = κ(xi, xj) (Rasmussen and Williams 2006).

In online learning scenarios, the predictive mean and variance computations in (1) demonstrate O(N(tk)) and O(N 2(tk)) complexities respectively, indicating these operations computationally intractable as data grows without bound. To address these scalability challenges, a widely adopted strategy involves partitioning the data into multiple subsets and training separate GP experts with their means µi(·) and variances σ2 i (·), where i ∈N denotes the index of the GP expert. Various aggregation techniques have been proposed for DGPs, and the structure of such aggregation methods can be formulated in a general framework as

˜µ(x) =

X i∈N ωi(x)µi(x), (3a)

˜σ2(x) =

X i∈N ϖi(x)σ2 i (x), (3b)

where N ⊂N is the set of all GP experts, the functions ωi(·): Rn →R≥0 and ϖi(·): Rn →R≥0 represent the aggregation weights for the mean and variance, respectively.

## 3 Generated Experts of Gaussian Processes

In this section, we introduce an efficient online distributed learning framework designed to adaptively process streaming data in real time. At the core of SkyGP is a fully online and adaptive architecture that maintains a bounded, scalable set of GP experts. To enable dynamic expert allocation and effective aggregation, we first present the kernel-based center mechanism in Section 3.1. Building on this, we describe the progressive generation strategy for updating and predicting with the GP experts in Section 3.2, followed by the aggregation strategy in Section 3.3. Finally, we analyze the bounded computational complexity of SkyGP in Section 3.4.

## 3.1 Kernel-Induced Distance

To enable partitioning and localization for newly generated GP experts, we adopt a center-based representation of the training inputs, where the center of the i-th expert GPi is defined as ci = 1 Ni

PNi k=1 xk i, following (Nguyen-tuong, Peters, and Seeger 2008). Each expert maintains its own representative center to support fast and scalable online allocation. To facilitate online computation, the center of each

27720

<!-- Page 3 -->

## Algorithm

1: Expert Localization with an Adaptive Window

Require: xk, νprev, {ϑk−1 i }i∈N(tk−1) Step I: Compute adaptive window size 1: if k > 1 then 2: Compute distance: dtemp ←1/κ(xk−1, xk) 3: Window size: W ←min(¯W, ⌊exp(dtemp/ϱ)⌋) 4: else W ←0 end if Step II: Locate nearest expert 5: if W̸ = 0 then 6: I ←{νprev −W,..., νprev + W} from T (tk−1) 7: I ←{i ∈I ∩N(tk−1) | ϑk−1 i > ¯ϑ} 8: else I ←νprev end if 9: νnr ←arg maxi∈I κ(xk, ci); νprev ←νnr 10: GPnr(tk) ←Choose GP expert corresponding to νnr 11: return I and νprev expert is updated incrementally as new data points are assigned. Specifically, when a new point xk arriving at time step tk is allocated to the selected expert, the expert center is updated as ck i = (k −1)ck−1 i /k + xk/k. (4)

To evaluate the distance between the expert center ck i and the newly arrived input xk in the feature space induced by the kernel, we define the kernel-based distance as follows dk i (ck i, xk) = 1/κ(ck i, xk). (5)

## 3.2 Progressive Expert Generation Strategy Expert Localization and Generation

In conventional online GP approximation methods, new data points are typically assigned to the first available expert that has not yet reached its capacity (Nguyen-tuong, Peters, and Seeger 2008; Lederer et al. 2021; Yang, Dai, and Hirche 2025). Once the expert becomes full, it is either no longer updated or directly split into sub-experts, often without explicitly accounting for the underlying distributional properties and space features of the data. In contrast, our SkyGP framework dynamically allocates each incoming data point to the most appropriate expert based on kernel proximity and time-aware factor. Specifically, from the prediction phase, we have already calculated the kernel distances between the new arriving point and the experts within an adaptive window W ∈I[1, ¯ W ] and found the nearest experts with in the expert set N(tk), where N(t0) = 1 (see Algorithm 1). After locating the previous index νprev of the nearest expert denoted by νnr, we are able to process the streaming data based on the index list I filtered by the time-aware factor ϑ ∈(0, 1] initialized by 1, which encodes the usage history of the experts. Moreover, we define the upper bound of ϑ as ¯ϑ to filter out the outdated experts. If the expert has not reached its capacity, the data point is added to it (see Figure 1). Otherwise, the two SkyGP variants handle this situation in two different ways outlined in Algorithm 2.

In particular, a data replacement strategy is employed in SkyGP-Dense. When the new data pair (xk, yk) is confirmed to add to Dnr(tk), and the data point within GPnr that

**Figure 1.** Data allocation process

is furthest from its center is cast off and moved to a separate dropped dataset Doff nr (tk), whose center offck nr is then updated in the same method in (4). Since such a replacement requires recomputing the expert’s kernel matrix and Cholesky factorization, we introduce an event-triggered mechanism to limit updates only to critical cases. Let cnr and offca be the center and the dropped center of expert GPnr with Nnr(tk) data points {(xs nr, ys nr}Nnr(tk)

s=1. The event-triggered data forwarding strategy is designed as

Dnr(tk)=

Dnr(tk−1)∪(xk,yk)\(xkoff,ykoff), if ∆< 0

Dnr(tk−1), otherwise, (6)

where ∆∈R is defined as ∆= maxs=1,···,Nnr(tk) ∆(s) and

∆(s)=κ(xs, cnr)−κ(xs,offcnr)−κ(xk, cnr)+κ(xk,offcnr).

This kernel-based selection strategy encourages experts to retain points that align with the current local distribution while avoiding repeated inclusion of previously discarded regions. Although computationally expensive, this step is infrequent and remains tractable under the predefined data threshold ¯N. If no expert accepts xk, a new expert will be created and the center will be initialized with xk. In SkyGP- Fast, no replacement is performed. This design ensures all update GP expert is a rank-one update to the Cholesky factor, which incurs a computational complexity of O(N 2 nr). SkyGP-Fast bypasses recomputations by appending new experts instead of replacing data, favoring low-latency updates and scalability. In contrast, SkyGP-Dense limits memory usage by reusing expert slots, making it more suitable for resource-constrained settings. Together, these two modes offer a flexible trade-off between computational efficiency and memory control across diverse online learning scenarios.

Dynamic Expert List Creation The expert search is implemented over a center-indexed list that maintains a globally ordered list of expert centers based on their insertion positions. The index of this list is defined as νi ∈N with corresponding GPi expert. The newly instantiated expert with center xk will be inserted adjacent to the nearest existing expert identified during search. To update the table when new GP expert generated, we compare the kernel-based distance between xk and the left/right neighbors of the selected experts with their corresponding center c− nr and c+ nr:

dleft = 1/κ(xk, c− nr), dright = 1/κ(xk −c+ nr) (7)

27721

![Figure extracted from page 3](2026-AAAI-streaming-generated-gaussian-process-experts-for-online-learning-and-control/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

## Algorithm

2: Expert Update Strategy

Require: xk, νprev, I, {ϑk−1 i }i∈N(tk−1) Step I: Aggregated Prediction 1: Itemp ←{ν ∈I | ϑk−1 ν > ¯ϑ} 2: Iagg ←indices of the largest ¯ N values in Itemp 3: ˜µ(xk), ˜σ(xk) ←(3) with MOE/POE/BCM (9) to (11) Step II: GP Expert Model Update 4: {ϑk i }i∈N ←{ϑk−1 i }i∈N 5: for all ν ∈Iagg do 6: ϑk ν←1,Dtemp←{x∈Dν(tk−1)|κ(x, cν)>κ(xk, cν)} 7: if |Dν(tk−1)| < ¯N then 8: Dν(tk) ←Dν(tk−1) ∪(xk, yk) 9: Update GPν(tk) ←Cholesky rank-one update 10: return {ϑk i }i∈N(tk) 11: else if SkyGP-Dense and Dtemp = ∅then 12: Update Dν(tk) ←(6), GPν(tk) ←(2) 13: Update offcν ←(4) with dropped data 14: return {ϑk i }i∈N(tk) 15: end if 16: end for 17: Create GP|N (tk−1)|+1 with dataset D(tk) = (xt, yt) 18: Update expert list T (tk) ←T (tk−1) and (8) 19: Update N(tk) ←{N(tk−1), |N(tk−1)| + 1} Step III: Update Time-Aware Factor 20: for i = N\Iagg do ϑk i ←ρϑk−1 i end for 21: return {ϑk i }i∈N(tk)

According to the previous νnr in Algorithm 1, the new index of GPnew is νnew = min(νnr |N|), if dright < dleft max(νnr −1, 0) otherwise. (8)

## 3.3 Aggregated Prediction Leveraging DGP framework in (3), our proposed

SkyGP can be seamlessly integrated with existing aggregation strategies to enhance predictive performance and uncertainty estimation across decentralized data streams. These weights are typically chosen to satisfy certain properties, such as nonnegativity and normalization, ensuring that the aggregated predictions are coherent and interpretable. For example, the aggregated weight functions of MoE are ωi(x) = wi, (9a)

ϖi(x) = wi σ2 i (x) + µ2 i (x)

−˜µ2(x)/wi, (9b) satisfying P i∈Iagg wi = 1, which is also utilized in the mixture of explicitly localized experts. Considering the posterior variance in GP experts, the PoE family methods employ the following aggregation structure ωi(x) = wiσ2 i (x)/ϖi(x), (10a)

ϖi(x) = 1/

X s∈Iagg wsσ−2 s (x). (10b)

Furthermore, these aggregation schemes can be extended to incorporate the prior variance of the unknown function, denoted as σ∗, to further refine the combined predictive uncertainty in the BCM family approaches. In this context, the weight function for the mean remains consistent with that of the PoE in (10a), while the corresponding weight function for the aggregated posterior variance is given by ϖi(x)=1/

X s∈Iaggwjσ−2 j (x)+

1− X j∈Iaggwj σ−2

∗

. (11)

This extension ensures that the aggregated predictions remain well-calibrated, especially in distributed or federated learning scenarios where each expert may have access to different subsets of the data.

According to Algorithm 1, given a new input xk, SkyGP performs prediction by first identifying the definable ¯ N number of experts within the search window. Based on the returned aggregation expert list Iagg, each expert predicts the posterior mean µi(xk) and variance σ2 i (xk). These predictions then are fused using a principled weighting strategy, e.g., MoE, PoE or BCM, yielding the final prediction in (3).

## 3.4 Bounded Complexity Analysis In this section, we formalize the computational efficiency of the proposed

SkyGP framework, which is designed to maintain bounded per-step complexity during both model update and prediction. The primary sources of computational cost include nearest expert localization, aggregated prediction, and expert model update. Each component is explicitly designed to ensure low complexity and scalability in streaming scenarios, while maintaining high prediction accuracy.

## Model

Update For expert localization, as described in Algorithm 1, the computational cost from evaluating kernel similarities between the current input and the expert centers to obtaining index set I (line 1-8) is O(1). The subsequent selection of the nearest expert from the candidate set I in line 9, even when incorporating the time-aware factor, requires only a linear search over I with the same order of complexity, i.e., O(W). Consequently, the overall computational complexity of Algorithm 1 is O(W).

The overall computational cost of the Algorithm 2 is dominated by three components. First, the selection of the aggregated expert set in line 2 requires filtering the candidate index set I and selecting the top ¯ N elements, which can be performed in O(|I| log ¯ N) time. Second, the update phase iterates over the ¯ N aggregated experts. For each, the construction of the temporary data subset incurs O(|Dν(tk−1)|) cost, which is bounded by O(¯N) considering |Dν(tk)| ≤¯N. Moreover, when a GP model is updated via a rank-one Cholesky modification for SkyGP-Fast, an additional O(¯N 2) cost per expert is incurred. On the other hand, SkyGP-Dense requires full Cholesky factor recomputation when performing replacement operations, incurring a higher cost of O(¯N 3). Third, the time-aware weighting update over the remaining experts requires O(¯ N) operations. Hence, the total worst-case complexity can be expressed as O(W log ¯ N + ¯ N ¯N 2) for SkyGP-Fast, and similarly O(W log ¯ N + ¯ N ¯N 3) for SkyGP-Dense.

Prediction Aggregated mean and variance in SkyGP are computed using the bounded top ¯ N nearest experts. As each local GP performs inference with O(N 2(tk)) complexity, the overall prediction complexity per step is O(¯ NN 2(tk)).

27722

<!-- Page 5 -->

## 4 Safe Learning-based Control Policy

In this section, we present a learning-based control policy that integrates the proposed SkyGP framework into nonlinear systems with unknown dynamics. The key idea is to leverage real-time GP predictions to estimate model uncertainties and design a feedback controller that ensures safe and stable trajectory tracking. Following the introduction of the prediction error bound of SkyGP in Section 4.1, we analyze the control performance for general dynamical systems and design a tracking control policy specifically for Euler–Lagrange (EL) systems in Section 4.2.

## 4.1 Learning Performance of SkyGP

We consider a function f belonging to a reproducing kernel Hilbert space (RKHS) Hκ associated with a positive definite kernel κ(·, ·), such that ∥f∥κ ≤Γ. Let µi(x) and σi(x) denote the posterior mean and standard deviation from the i-th GP expert trained on dataset Di for i = 1, · · ·, N. Then the following probabilistic prediction error bound holds.

Lemma 1. Consider the regression task in a compact domain X, and suppose the kernel function κ(·, ·) is Lipschitz with Lipschitz constant Lκ ∈R0,+. Choose δ ∈(0, 1/ ¯ N) and τ ∈R+, then the prediction error satisfies

|f(x) −˜µ(x | D)| ≤βσ(x) + γ(x), ∀x ∈X (12)

with a probability of at least 1 −¯ Nδ, where γ(x) = P i∈N ωi(x)γi, σ(x) = P i∈N ωi(x)σi(x), and β = 2

2 Xn j=1 log l√n

2τ (¯xj −xj) m

−2 log δ n

1/2

, (13)

γi = p βδLσ,i + Γ p

2Lκ + Lµ,i τ, (14)

with ¯xj = maxx∈X xj, xj = minx∈X xj and xj as the jth dimension of x. The positive constants Lµ,i ∈R0,+ and Lσ,i ∈R0,+ are the Lipschitz constant for posterior mean µi(·) and variance σi(·), respectively for i ∈N.

Lemma 1 shows the probabilistic theoretical error bound of the aggregated prediction ˜µ(·), which also holds for the proposed Sky-GP1. Note that the boundness of the prediction error does not rely on the choice of aggregating strategy reflected by the weighting function ωi(·). For notational simplicity, denote the prediction error bound as η(x) = βσ(x) + γ(x), which is used in Section 4.2.

Remark 1. Compared with the other probabilistic (Srinivas et al. 2012; Scharnhorst et al. 2022) or deterministic bounds (Maddalena, Scharnhorst, and Jones 2021; Hashimoto et al. 2022), the error bound chosen in this paper follows (Lederer, Umlauft, and Hirche 2019), which results in an amplitude constant β of posterior variance σ(·). Moreover, it is shown that there always exists a sufficiently small grid factor τ ∈R+ such that γ(x) ≪βσ(x) for all x ∈X, i.e., the posterior variance dominates the error bound η(x). Therefore, the prediction error bound could also be written as η(x) ≤2βσ(x) (Lederer et al. 2024).

1The proofs of all lemmas and theorems are provided in Appendix A in (Yang et al. 2025b).

## 4.2 Safe Critical Control Application A General Control System

The objective is to design a GP-based control law that drives an unknown dynamical system to exhibit a desired behavior. Specifically, we consider a class of control applications focused on output stabilization, where the goal is to ensure that the system output converges to the equilibrium point asymptotically. The continuous-time nonlinear system is described as follows

˙x = f(x, u) + g(x, u), z = h(t, x) (15)

where x ∈ X ⊂ Rm, u ∈ U ⊂ Rmu and z ∈ Rmz denote the system state, control input and system output, respectively. The transition function f(·, ·) = [f1(·, ·), · · ·, fm(·, ·)]⊤: X × U →Rm is unknown, where each scalar fj(·, ·) belongs to a RKHS Hκ,j corresponding to a kernel function κj(·, ·): Xe × Xe →R0,+ with Xe = X × U ⊂Rm+mu for all j = 1, · · ·, m. The measurement function h(·, ·): R≥0 × X →Rmz is known. To achieve system output stabilization, i.e., limt→∞z(t) = 0mz×1, a control policy π(·, ·, ·): R≥0 ×X×Hκ →Rmu is designed satisfying the following assumption.

Assumption 1. Suppose there exists a differentiable function V (·, ·): R≥0 × Rmy →R≥0 satisfying α(∥z∥) ≤V (t, z) ≤¯α(∥z∥) (16)

with class-K functions α(·), ¯α(·): R≥0 →R0,+. The control law π(·, ·, ·) is designed such that

∇xV (t, x)(µ(x, π(t, x, µ)) + g(x, π(t, x, µ))) (17)

+ ∇tV (t, x) ≤−α(V (t, h(t, x))) −∥∇xV (t, x)∥2/(4ε), with a positive constant ε ∈R>0, where the function α(·): R≥0 →R≥0 belongs to class-K and

∇tV (t, x) = ∂V (t, h(t, x))

∂t + ∂V (t, h(t, x))

∂h(t, x)

∂h(t, x)

∂t,

∇xV (t, x) = ∂V (t, h(t, x))

∂h(t, x)

∂h(t, x)

∂x, (18)

for any µ(·) = [µ1(·), · · ·, µm(·)]T satisfying µi(·) ∈Hκ,j for all j = 1, · · ·, m.

This assumption indicates the asymptotic output stability of the equivalent system ˙x = µ(x, u) + g(x, u) using the control law π(t, x, µ). Compared to the condition in conventional asymptotic stability (Khalil 2002), the additional term ∥∇xV (t, x)∥2/(4ε) introduced in (17) is used following input-to-state control Lyapunov functions to partially compensate for the potential effect from unknown disturbances. Later, an example is provided to demonstrate how to design a model-based controller that satisfies this assumption. Notably, the true dynamical system is unknown f(·) instead of µ(·), whose performance is shown as follows.

Theorem 1. If there exists a control law π(·, ·, ·) satisfying Assumption 1. Choose δ ∈(0, 1/m), then the output z(t) of the true system (15) is ultimately bounded by limt→∞∥z(t)∥≤α−1(α−1(ε¯η2)) (19)

27723

<!-- Page 6 -->

with a probability of at least 1 −mδ. The positive constant ¯η = maxt∈R0,+,x∈X ∥η(ξ(t, x, µ))∥denotes an upper bound on the model error between f(·) and its GP approximation µ, where ξ(t, x, µ) = [xT, πT (t, x, µ)]T and η(·) = [η1(·), · · ·, ηdx(·)]T and ηi(·) obtained using prediction error bound.

This theorem guarantees that the system output ultimately remains within a bounded neighborhood of the desired equilibrium, despite the presence of model uncertainties. To instantiate this theorem and derive a practically applicable controller, we next consider a representative Euler–Lagrange (EL) system and demonstrate the design and performance of a corresponding learning-based policy.

Euler-Lagrange System Control Consider an EL system M(q)¨q + C(q, ˙q) ˙q + g(q, ˙q) = u + d(q, ˙q), (20) where q∈Q⊂Rmq and u∈U⊂Rmu denote the generalized coordinate and control input with mq = m/2. Define x = [q⊤, ˙q⊤]⊤∈X, then the dynamics of (20) is rewritten as

˙x=

˙q M −1(q)(u −C(q, ˙q) ˙q −g(x))

| {z } g(x,u)

+

0mq×1 M −1(q)d(x)

| {z } f(x,u) The control task is to track a pre-defined trajectory xd(·) = [q⊤ d (·), ˙q⊤ d (·)]⊤: R≥0 →X, such that the output is defined as tracking error as z(t) = x(t) −xd(t). To achieve this control objective, a learning-based control law inspired by computed torque control is proposed as π(t, x, µ) = C(x) ˙q + g(x) −µ(x) + M(q)¨qd(t) (21)

+M(q)(Kp(q−qd(t))+Kd(˙q−˙qd(t)))−BT(x)P z/(2ε), where B = [0dq×dq, M −⊤(q)]⊤. The control gains Kp and

Kd are chosen such that A =

0mq×mq Imq Kp Kd is Hurwitz.

The matrix P is the solution to the Lyapunov equation associated with the quadratic Lyapunov function V (t, z) = z⊤P z, where P ≻0 satisfies A⊤P + P A = −Q with Q ≻0 being a positive definite matrix. The existence and uniqueness of the solution P is guaranteed due to Hurwitz A (Khalil 2002). Then, the control performance in terms of tracking error bound is shown as follows. Theorem 2. Consider the EL system (20) driven by the control law (21) using the proposed Sky-GP satisfying all assumptions in Lemma 1. Choose δ ∈(0, 1/mq) ⊂R, then the tracking error z is ultimately bounded by limt→∞∥z(t)∥≤ε¯λ(P)(λ(Q)λ(P))−1¯η2 (22) with a probability of at least 1 −mqδ.

Theorem 2 shows the tracking error bound obtained by using the controller (21) with the proposed Sky-GP, which is relevant to the worst-case learning performance ¯η and the desired convergence strength reflected by Q. Specifically, smaller prediction error ¯η and larger eigenvalues of Q induce smaller tracking error. Note that increasing the control gains with larger eigenvalues of Q also leads to high sensitivity of the measurement noise, which may deteriorate the control performance. Therefore, an accurate prediction for a smaller ¯η is essential to achieve high tracking precision.

## 5 Experimental Evaluation We conduct comprehensive experiments to evaluate the proposed

SkyGP framework from both regression and control perspectives. In Section 5.1, we assess the regression performance on multiple real-world benchmark datasets. Then, a closed-loop control performance comparison is evaluated against SOTA approaches on a nonlinear dynamical system in Section 5.2. Finally, we present an ablation study analyzing different algorithmic design choices2.

## 5.1 Regression Performance Evaluation We evaluate the proposed

SkyGP framework on four realworld benchmark datasets. The SARCOS dataset contains 44,484 samples with 21 input features. The PUMA- DYN32NM (PUMA) dataset consists of 7,168 samples with 32 input features. The KIN40K dataset includes 10,000 samples with 8-dimensional inputs. The ELECTRIC dataset records household electricity consumption, comprising over 2 million samples with 11-dimensional inputs. For simplicity, we use the first 20,000 samples of ELECTRIC dataset. To assess the performance of SkyGP, we compare our two variants against several strong baselines: LoG-GP (Lederer et al. 2021) and Local GPs (Nguyen-tuong, Peters, and Seeger 2008) with each expert holding at most 50 data points, SSGP with 50 inducing points (Bui, Nguyen, and Turner 2017), and ISSGP with 200 random features (Gijsberts and Metta 2013). All methods use an ARD kernel with hyperparameters pre-trained with the first 1000 samples in each dataset. Each model is evaluated in a sequential setting, where predictions and updates are performed on-the-fly as each new data point arrives. We evaluated the average prediction and update times, as well as the standardized mean squared error (SMSE) and the mean standardized log loss (MSLL) in a sequential interpretation (Lederer et al. 2021). The maximal number of experts ¯ N ∈{1, 2, 4} are used in all benchmark. Each expert with SkyGP holds at most ¯N = 50 data points and the maximal search window size ¯W = 40 and uses the rBCM aggregation method. Set the time-aware decay weighting factor ρ = 0.995 and ¯ϑ = 10−3. SkyGP- Fast with a maximum of one expert is denoted by SkyGP-F- 1, and SkyGP-Dense with one expert by SkyGP-D-1. Other variants follow the same naming convention.

**Table 1.** shows the average SMSE and MSLL across three benchmark datasets, demonstrating that the proposed SkyGP variants consistently outperform baseline methods such as LoG-GP and LocalGPs in both predictive accuracy and uncertainty calibration. While ISSGP achieves the best SMSE and MSLL on the PUMA dataset, its prediction and update time is over 30 times slower, as detailed in Table 2, making it less suitable for real-time applications. Notably, SkyGP- D-4 achieves the best overall performance, with the lowest SMSE (0.017) and MSLL (-2.03) on the SARCOS dataset, and competitive results on PUMA and ELECTRIC. Table 2 summarizes the average prediction and update times across three datasets. SkyGP-F-1 achieves the lowest overall latency, with update times consistently at 0.04s and the fastest

2For additional results and ablation study analysis, refer to Appendix B in (Yang et al. 2025b).

27724

<!-- Page 7 -->

## Model

SARCOS PUMA ELECTRIC ϵsmse ϵmsll ϵsmse ϵmsll ϵsmse ϵmsll LoG-GP 0.044 -1.83 0.20 -1.00 0.11 -3.08 SkyGP-F-1 0.037 -1.83 0.26 -0.92 0.08 -3.29 SkyGP-F-4 0.024 -1.91 0.09 -1.39 0.07 -3.36 SkyGP-D-1 0.031 -1.89 0.23 -1.10 0.08 -3.31 SkyGP-D-4 0.017 -2.03 0.08 -1.40 0.07 -3.38 LocalGPs-1 0.031 -1.90 0.18 -1.11 0.08 -3.26 LocalGPs-4 0.071 -1.38 0.18 -0.79 0.14 -2.20 ISSGP 0.023 -1.91 0.08 -1.46 0.06 -2.19 SSGP 0.068 -1.11 0.09 -1.05 – –

**Table 1.** Average SMSE and MSLL on 3 datasets.

## Model

SARCOS PUMA ELECTRIC tpred tup tpred tup tpred tup LoG-GP 0.30 0.22 0.22 0.20 0.18 0.24 SkyGP-F-1 0.16 0.04 0.26 0.04 0.15 0.04 SkyGP-F-4 0.23 0.04 0.35 0.04 0.21 0.04 SkyGP-D-1 0.17 0.09 0.25 0.08 0.14 0.06 SkyGP-D-4 0.24 0.16 0.28 0.16 0.22 0.08 LocalGPs-1 1.17 0.15 1.07 0.08 2.78 0.06 LocalGPs-4 1.25 0.23 1.14 0.08 2.88 0.06 ISSGP 18 3 6 4 8 SSGP 5 4 2 6 – –

**Table 2.** Average prediction and update time on 3 datasets.

prediction on SARCOS (0.16s), making it well-suited for real-time applications. SkyGP-D-1 has the best prediction time on ELECTRIC (0.14s) while maintaining competitive update performance. In contrast, traditional baselines such as ISSGP and SSGP exhibit significantly higher computational costs, with ISSGP requiring up to 18s for prediction and 7s for update on SARCOS, rendering them impractical for online deployment. Notably, SSGP fails to produce results on the ELECTRIC dataset within 20s, so we omit it.

## 5.2 Control Performance Evaluation

We evaluate the control performance of the system described as m¨q + 9.8 = u + f(x) with m = 1, where f(x) = 1 + x1x2/10 + cos(x2)/2 (23)

−10 sin(5x1) + (1 + exp(−x2/10))−1/2.

Choose x1 = q, x2 = ˙q, then the dynamics is reformulated as ˙x1 = x2, ˙x2 = g(u) + f(x) with g(u) = u −9.8 = (u −c ˙q −g)/m similar as (21) with c = 0 and g = 9.8.

π(t, x, ˜µ) = 9.8 −˜µ(x) −arw2 r sin(wrt) + kp(q −qd(t)) + kd(˙q −˙qd(t)) −[0, 1]P (x −xd)/(2ε) (24)

with control gains kp = 5, kd = 10 and ε = 1. The matrix P is obtained by solving the Lyapunov equation with Q = I2. The two variants of SkyGP are with ¯N = 50,

¯W = 10, Γ = 1 and the maximal data size set to 100.

**Figure 2.** Learning and tracking performance comparison of the control task from the 100 times Monte Carlo tests.

Other hyperparameters are set the same in Section 5.1. Furthermore, the desired reference is chosen with the form qr(t) = ar sin(wrt) with coefficients ar = 1, wr = 0.1.

The maximum norm values of tracking errors z = x−xd and prediction errors f(x) −˜µ(x) are shown in Figure 2. The box plot summarizes the distribution of the performance on prediction error and tracking error over 100 trials with a random initial state x(0) uniformly distributed in [0, 1]2. The proposed SkyGP variants demonstrate both lower average and median in prediction and tracking errors, indicating more accurate and consistent learning and control behavior compared to all baselines. Particularly, the prediction and tracking errors of SkyGP-Dense are lower than those of SkyGP-Fast with sufficiently fast computation time, which is consistent with the regression benchmarks in Section 5.1.

## 6 Conclusion and Discussion

In this paper, we introduced SkyGP for scalable and adaptive learning. Designed to address the computational and memory bottlenecks of exact GPs in real-time settings, SkyGP maintains a bounded set of experts while preserving strong predictive performance with uncertainty quantification. SkyGP-Fast, targeted for computational efficiency, and SkyGP-Dense, designed for high prediction accuracy. Our extensive empirical evaluation across multiple real-world regression datasets and real-time control tasks demonstrates the superiority of SkyGP over SOTA baselines.

A limitation of the center update rule in Equation (4) is that it may fail to accurately capture special data distributions, such as annular or multimodal patterns. We adopt the method from (Nguyen-tuong, Peters, and Seeger 2008) for its simplicity and computational efficiency. Another limitation lies in the use of the dynamic table list, which may struggle to handle data with sudden distributional shifts, potentially affecting the timely allocation or reuse of experts.

27725

![Figure extracted from page 7](2026-AAAI-streaming-generated-gaussian-process-experts-for-online-learning-and-control/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

The authors acknowledge the financial support by the Federal Ministry of Education and Research of Germany in the programme of “Souver¨an. Digital. Vernetzt.” under joint project 6G-life with project identification number: 16KISK002.

## References

Bui, T. D.; Nguyen, C.; and Turner, R. E. 2017. Streaming Sparse Gaussian Process Approximations. In Guyon, I.; Luxburg, U. V.; Bengio, S.; Wallach, H.; Fergus, R.; Vishwanathan, S.; and Garnett, R., eds., Advances in Neural Information Processing Systems, volume 30. Curran Associates, Inc. Cao, Y.; and Fleet, D. J. 2015. Generalized Product of Experts for Automatic and Principled Fusion of Gaussian Process Predictions. arXiv:1410.7827. Cohen, S.; Mbuvha, R.; Marwala, T.; and Deisenroth, M. 2020. Healing Products of Gaussian Process Experts. In III, H. D.; and Singh, A., eds., Proceedings of the 37th International Conference on Machine Learning, volume 119 of Proceedings of Machine Learning Research, 2068–2077. PMLR. Dai, X.; Lederer, A.; Yang, Z.; and Hirche, S. 2023. Can Learning Deteriorate Control? Analyzing Computational Delays in Gaussian Process-Based Event-Triggered Online Learning. In Matni, N.; Morari, M.; and Pappas, G. J., eds., Proceedings of The 5th Annual Learning for Dynamics and Control Conference, volume 211 of Proceedings of Machine Learning Research, 445–457. PMLR. Dai, X.; Yang, Z.; Xu, M.; Zhang, S.; Liu, F.; Hattab, G.; and Hirche, S. 2024. Decentralized event-triggered online learning for safe consensus control of multi-agent systems with Gaussian process regression. European Journal of Control, 80: 101058. 2024 European Control Conference Special Issue. Dai, X.; Yang, Z.; Zhang, S.; Zhai, D.-H.; Xia, Y.; and Hirche, S. 2025. Cooperative Online Learning for Multiagent System Control via Gaussian Processes With Event- Triggered Mechanism. IEEE Transactions on Neural Networks and Learning Systems, 36(7): 13304–13318. Deisenroth, M.; and Ng, J. W. 2015. Distributed Gaussian Processes. In Bach, F.; and Blei, D., eds., Proceedings of the 32nd International Conference on Machine Learning, volume 37 of Proceedings of Machine Learning Research, 1481–1490. Lille, France: PMLR. Gijsberts, A.; and Metta, G. 2013. Real-time model learning using Incremental Sparse Spectrum Gaussian Process Regression. Neural Networks, 41: 59–69. Special Issue on Autonomous Learning. Hashimoto, K.; Saoud, A.; Kishida, M.; Ushio, T.; and Dimarogonas, D. V. 2022. Learning-based Symbolic Abstractions for Nonlinear Control Systems. Automatica, 146: 110646. Khalil, H. K. 2002. Nonlinear Systems. Prentice-Hall.

Lederer, A.; Begzadi´c, A.; Hirche, S.; Cort´es, J.; and Herbert, S. 2024. Safe barrier-constrained control of uncertain systems via event-triggered learning. arXiv preprint arXiv:2408.16144. Lederer, A.; Conejo, A. J. O.; Maier, K. A.; Xiao, W.; Umlauft, J.; and Hirche, S. 2021. Gaussian Process-Based Real-Time Learning for Safety Critical Applications. In Meila, M.; and Zhang, T., eds., Proceedings of the 38th International Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, 6055–6064. PMLR. Lederer, A.; Umlauft, J.; and Hirche, S. 2019. Uniform error bounds for Gaussian process regression with application to safe control. Advances in Neural Information Processing Systems, 32. Lederer, A.; Yang, Z.; Jiao, J.; and Hirche, S. 2023. Cooperative Control of Uncertain Multiagent Systems via Distributed Gaussian Processes. IEEE Transactions on Automatic Control, 68(5): 3091–3098. Liu, H.; Cai, J.; Wang, Y.; and Ong, Y. S. 2018. Generalized Robust Bayesian Committee Machine for Large-scale Gaussian Process Regression. In Dy, J.; and Krause, A., eds., Proceedings of the 35th International Conference on Machine Learning, volume 80 of Proceedings of Machine Learning Research, 3131–3140. PMLR. Maddalena, E. T.; Scharnhorst, P.; and Jones, C. N. 2021. Deterministic Error Bounds for Kernel-based Learning Techniques under Bounded Noise. Automatica, 134: 109896. Naish-guzman, A.; and Holden, S. 2007. The Generalized FITC Approximation. In Platt, J.; Koller, D.; Singer, Y.; and Roweis, S., eds., Advances in Neural Information Processing Systems, volume 20. Curran Associates, Inc. Nguyen-tuong, D.; Peters, J.; and Seeger, M. 2008. Local Gaussian Process Regression for Real Time Online Model Learning and Control. In Koller, D.; Schuurmans, D.; Bengio, Y.; and Bottou, L., eds., Advances in Neural Information Processing Systems, volume 21. Curran Associates, Inc. Rasmussen, C. E.; and Williams, C. K. I. 2006. Gaussian Processes for Machine Learning. Adaptive Computation and Machine Learning. Cambridge, Mass: MIT Press. ISBN 978-0-262-18253-9. Reeb, D.; Doerr, A.; Gerwinn, S.; and Rakitsch, B. 2018. Learning Gaussian Processes by Minimizing PAC-Bayesian Generalization Bounds. In Bengio, S.; Wallach, H.; Larochelle, H.; Grauman, K.; Cesa-Bianchi, N.; and Garnett, R., eds., Advances in Neural Information Processing Systems, volume 31. Curran Associates, Inc. Scharnhorst, P.; Maddalena, E. T.; Jiang, Y.; and Jones, C. N. 2022. Robust Uncertainty Bounds in Reproducing Kernel Hilbert Spaces: A Convex Optimization Approach. IEEE Transactions on Automatic Control, 68(5): 2848–2861. Sch¨urch, M.; Azzimonti, D.; Benavoli, A.; and Zaffalon, M. 2023. Correlated product of experts for sparse Gaussian process regression. Machine Learning, 112(5): 1411–1432. Snelson, E.; and Ghahramani, Z. 2005. Sparse Gaussian Processes using Pseudo-inputs. In Weiss, Y.; Sch¨olkopf, B.; and

27726

<!-- Page 9 -->

Platt, J., eds., Advances in Neural Information Processing Systems, volume 18. MIT Press. Srinivas, N.; Krause, A.; Kakade, S. M.; and Seeger, M. W. 2012. Information-theoretic Regret Bounds for Gaussian Process Optimization in the Bandit Setting. IEEE Transactions on Information Theory, 58(5): 3250–3265. Trapp, M.; Peharz, R.; Pernkopf, F.; and Rasmussen, C. E. 2020. Deep Structured Mixtures of Gaussian Processes. In Chiappa, S.; and Calandra, R., eds., Proceedings of the Twenty Third International Conference on Artificial Intelligence and Statistics, volume 108 of Proceedings of Machine Learning Research, 2251–2261. PMLR. Tresp, V. 2000a. A Bayesian committee machine. Neural computation, 12(11): 2719–2741. Tresp, V. 2000b. Mixtures of Gaussian Processes. In Leen, T.; Dietterich, T.; and Tresp, V., eds., Advances in Neural Information Processing Systems, volume 13. MIT Press. Wachi, A.; Sui, Y.; Yue, Y.; and Ono, M. 2018. Safe Exploration and Optimization of Constrained MDPs Using Gaussian Processes. Proceedings of the AAAI Conference on Artificial Intelligence, 32(1). Yang, Z.; Dai, X.; Dubey, A.; Hirche, S.; and Hattab, G. 2024a. Whom to Trust? Elective Learning for Distributed Gaussian Process Regression. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems, AAMAS ’24, 2020–2028. Richland, SC: International Foundation for Autonomous Agents and Multiagent Systems. ISBN 9798400704864. Yang, Z.; Dai, X.; Fang, L.; Zhou, J.; and Yan, Z. 2025a. Safe event-triggered control of unmanned surface vehicles with Gaussian processes: Resilience in denial of service attacks and uncertain dynamics. Engineering Applications of Artificial Intelligence, 153: 110776. Yang, Z.; Dai, X.; and Hirche, S. 2025. Asynchronous Distributed Gaussian Process Regression. Proceedings of the AAAI Conference on Artificial Intelligence, 39(21): 22065– 22073. Yang, Z.; Dong, S.; Lederer, A.; Dai, X.; Chen, S.; Sosnowski, S.; Hattab, G.; and Hirche, S. 2024b. Cooperative Learning with Gaussian Processes for Euler-Lagrange Systems Tracking Control Under Switching Topologies. In 2024 American Control Conference (ACC), 560–567. Yang, Z.; Sosnowski, S.; Liu, Q.; Jiao, J.; Lederer, A.; and Hirche, S. 2021. Distributed Learning Consensus Control for Unknown Nonlinear Multi-Agent Systems based on Gaussian Processes. In 2021 60th IEEE Conference on Decision and Control (CDC), 4406–4411. Yang, Z.; Zhang, D.; Dai, X.; Yu, F.; Zhang, C.; Huang, B.; Sadeghian, H.; and Haddadin, S. 2025b. Streaming Generated Gaussian Process Experts for Online Learning and Control: Extended Version. arXiv:2508.03679. Yuan, C.; and Neubauer, C. 2008. Variational Mixture of Gaussian Process Experts. In Koller, D.; Schuurmans, D.; Bengio, Y.; and Bottou, L., eds., Advances in Neural Information Processing Systems, volume 21. Curran Associates, Inc.

Yuan, Z.; and Zhu, M. 2024. Lightweight Distributed Gaussian Process Regression for Online Machine Learning. IEEE Transactions on Automatic Control, 69(6): 3928–3943.

27727
