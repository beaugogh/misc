---
title: "On Coresets for End-to-end Learning from Crowds"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38850
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38850/42812
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# On Coresets for End-to-end Learning from Crowds

<!-- Page 1 -->

On Coresets for End-to-end Learning from Crowds

Hang Yang1, Zhiwu Li1,*, Witold Pedrycz2,3

1Macau Institute of Systems Engineering, Macau University of Science and Technology 2Department of Electrical and Computer Engineering, University of Alberta 3Systems Research Institute, Polish Academy of Sciences hangy03@student.must.edu.mo, zwli@must.edu.mo, wpedrycz@ualberta.ca

## Abstract

Crowdsourcing is a common approach for training datahungry models by collecting high-quality labeled data with human labor. With crowdsourcing data, the end-to-end learning paradigm is rising, where the classifier is concatenated with annotator-specific confusion layers and the two parts are co-trained in a parameter-coupled manner. However, learning with the size of a very large set of annotations is a challenge when computation or energy is limited. In this paper, we analyze and refine the coresets for end-to-end learning from crowds under the sensitivity sampling framework. This coreset is a small possible subset of annotations, so one can efficiently optimize the Coupled Cross-Entropy Minimization problem with guaranteed approximation. We first prove the lower bound, which shows no coresets smaller than complete data with confusion layers. Then, with workers’ transition matrices Ar, we show that with the regularization term log det A⊤ r Ar, this lower bound can be prevented. Our main result is that under mild assumptions, a smaller coreset exists for the regularized Coupled Cross-Entropy Minimization problem. An upper bound of sensitivity is proposed for designing a sampling algorithm called CrowdCore. The experimental results on synthetic and real-world datasets demonstrate the effectiveness of our analysis.

## Introduction

In recent years, deep neural network training on large-scale datasets has achieved remarkable success (LeCun, Bengio, and Hinton 2015; Vaswani et al. 2017; Momeni et al. 2025). For these data-hungry deep models, crowdsourcing serves as a valuable approach for gathering labeled data from human workers (Chu, Ma, and Wang 2021). However, a key challenge arises when dealing with very large datasets of annotations. The size of annotations is usually far larger than the size of instances, e.g., images. Therefore, the computational burden of learning from crowds is worse than that of traditional machine learning, and it is urgent to develop efficient algorithmic techniques for reducing computational complexity.

Coreset (Feldman, Schmidt, and Sohler 2013) is a wellstudied technique that can efficiently sketch large datasets without sacrificing performance. For example, existing work

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

shows that empirically, a coreset of size less than 1% of the input is enough to represent the whole dataset with an error less than 0.001 (Tolochinksy, Jubran, and Feldman 2022). For input data with size N, developing coreset means that there will be a smaller subset with size O(f(N)) that can play the role of the whole dataset, where f(N) is the sample complexity. Assume that there are R annotators to label N data points. The worst sample complexity will be O(R · f(N)). However, this bound is not satisfied since the number of annotations M is much smaller than RN.

Our goal is to find a better bound on the coreset size for crowdsourcing. More detailed, we focus on the end-toend learning from crowds. “End-to-end” means that the task model and label correction mechanism are co-trained in an end-to-end fashion (Rodrigues and Pereira 2018). The basic paradigm is connecting the confusion layer behind the classifier. Since the parameters of confusion layers Ar and classifier f are coupled optimized with cross-entropy loss, this approach is called Coupled Cross-Entropy Minimization (CCEM). It is proven that under CCEM, the distances between the trained classifier, the confusion layer, and their ground truth are bounded (Ibrahim, Nguyen, and Fu 2023).

Our analysis is under the sensitivity framework, where the key challenge is to find the upper sensitivity function and total sensitivity. Our first observation is that with the original CCEM loss function, there is no coreset smaller than the complete annotations. This lower bound is similar to traditional classification, where a norm regularization of weight is introduced to prevent the lower bound. In CCEM, we find that the regularization term log det A⊤ r Ar can help coreset to exist. Geometrically, this term is a surrogate of the volume of conv{Ar} = {x ∈Rd|x = Arθ, θ ≥0}. Therefore, this term is called volume regularization. This regularization is widely used in improving identifiability in the nonnegative matrix factorization tasks (Fu et al. 2019; Ibrahim, Nguyen, and Fu 2023). Nonetheless, its property in coresets has not been studied yet.

Our main result lies in proving that, under mild assumptions, a smaller coreset exists for the regularized CCEM problem. We only add an assumption that limits the eigenvalues of Ar. The other assumptions follow the existing works. We first analyze the properties of the new cost function, then bridge the sensitivity to the confusion layer Ar. Then, we propose an upper-sensitivity function and derive

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17913

<!-- Page 2 -->

the sample probability for each data point. With total sensitivity, the bound of the coreset size is given. Our proof leverages the framework proposed in (Tolochinksy, Jubran, and Feldman 2022) but differs significantly from the study in that work due to different cost functions, assumptions, and data spaces. The contribution can be summarized as follows:

• We provide a rigorous theoretical analysis of coresets for end-to-end learning from crowdsourced data, establishing a lower bound that demonstrates the necessity of using complete data with confusion layers to achieve optimal solutions in the CCEM problem. • We show that the lower bound identified in our analysis can be avoided with a volume regularization term. We prove, under mild assumptions, the existence of a smaller coreset that can be used to solve the regularized CCEM problem efficiently. This provides an approach to scaling end-to-end learning from crowdsourced data without degrading much accuracy. • Through empirical evaluation of both synthetic and realworld datasets, the results empirically show that the proposed sampling strategy, CrowdCore, can reduce the number of annotations with small approximation error, and model performance will not significantly decrease. The originality of this work stems from our analysis and refinement of coresets for end-to-end learning from crowds under the sensitivity sampling framework to optimize the CCEM problem with guaranteed approximation.

Related Works End-to-end Learning from Crowds. The first work in end-to-end models is CrowdLayer (Rodrigues and Pereira 2018), which applies a learnable crowd layer after the classifier for confusion modeling. After that, TraceReg (Tanno et al. 2019) introduces a regularization term in mapping the classifier output onto the worker-specified output. Besides, CoNAL (Chu, Ma, and Wang 2021) goes further by distinguishing a common confusion from the individual confusion of each worker. UnionNet (Wei et al. 2022) integrates the confusion of all workers into a parametric transition matrix, treating all workers as a unified entity. The CCEM problem is formally analyzed in (Ibrahim and Fu 2021), where the error bounds of learning ground-truth classifier and confusion layers are provided. Besides, the geometry property of the non-negative matrix factorization is introduced to improve the identification (Ibrahim and Fu 2021; Fu et al. 2019). Coresets. Coreset is well-studied in clustering (Feldman, Schmidt, and Sohler 2013), classification (Chen et al. 2022), and regression (Mirzasoleiman, Bilmes, and Leskovec 2020). The most used framework to analyze coresets is provided in (Feldman and Langberg 2011), where the sensitivity of data points is modeled. The work most related to our paper is the coresets for classification. Existing works show that with an additional common regularization term, i.e., norm-2 regularization of classifier parameters, the smaller coreset always exists with sensitivity-based sampling (Tolochinksy, Jubran, and Feldman 2022) or uniform sampling (Alishahi and Phillips 2024; Samadian et al. 2020). There is no direct research on coresets in crowdsourcing, but some work has been done to decrease cost-saving. Probably approximately correct (PAC) is used to study the cost-saving effect, and an upper bound for the minimally sufficient number of crowd labels can be given (Wang and Zhou 2016). Then, the cost complexity, also based on PAC, is proposed to model the trade-off between costs and quality (Fang et al. 2018).

## Preliminaries

End-to-end Learning from Crowds Notation. In this paper, we focus on binary classification with crowdsourcing datasets. Suppose that there are R workers labeling N instances as belonging to K = 2 possible classes, and the number of annotations is M. Notation xi ∈Rd refers to the i-th instance, and yri ∈{1, −1} refers to the label from the r-th worker on the i-th instance, where d is the data dimension.

We denote the instance set as X = {xi}N i=1, the annotation set as Y = {yri}, where |Y | = M, and the unknown instance truth set as Z = {zi}N i=1. Let us represent the classifier as f, and the workers’ transition matrices as {Ar}R r=1, where the columns of Ar are conditional probability distributions. To keep consistent with the existing study (Tolochinksy, Jubran, and Feldman 2022), f is parameterized with a vector w with shape d × 1 as:

f(x) = 1 1 + exp (−w⊤x). (1)

End-to-end Training. In general, the end-to-end training paradigm, classifier f and worker parameters {Ar}R r=1 are optimized jointly, called CCEM. Note that the classifier is sequentially combined with a feature extractor and a linear layer. The objective function of CCEM is:

min f,{Ar}R r=1

−1

M

X yri∈Y

K X k=1

I(yri = k) log[Arf(xi)]k. (2)

After proper network initialization, the optimal parameters of crowd layer {Ar}R r=1 and classifier f can be estimated with stochastic gradient descent.

Coreset Construction with Sensitivity To illustrate the concept of sensitivity, we first expand the confusion layer Ar in the binary classification scenario with two variables ar, br ∈[0, 1] as Ar = ar 1 −br 1 −ar br

.

It can be verified that for any θ, if 1⊤θ = 1, 1⊤Arθ = 1. Then, combine Eqs. (1) and (2), the logistic cost function of a specific data point (xi, yri) is:

ϕ(t) = log(1 + et), ϕ1(t) = log[ar + (1 −br)et], ϕ2(t) = log[br + (1 −ar)et], c(xi, yri) = ϕ(−yriw⊤xi) −ϕ1(−yriw⊤xi), yri = 1, ϕ(−yriw⊤xi) −ϕ2(−yriw⊤xi), yri = −1.

(3) Some necessary definitions are given as follows.

17914

<!-- Page 3 -->

Definition 1 (Query space). A tuple containing:

• Input data: complete set of data points P = (X, Y); • Classifier space: f ∈F or equivalently, w ∈Rd; • Confusion layer space: matrix space ∆K, which is simplified to (a, b) ∈([0, 1], [0, 1]) when K = 2; • Cost function: c(xi, yri; f, Ar).

is called query space for end-to-end learning from crowds.

Note that the confusion layer space is sometimes ignored since the initialization of Ar is determined as an identify matrix. Then, the definition of the coreset is as follows.

Definition 2 (ε-coreset). Given query space (P, F, ∆K, c), and error parameter ε ∈ (0, 1), an ε-coreset for (P, F, ∆K, c) is a tuple (Q, u), where Q is a subset and u is a weight function, such that for every f ∈F, Ar ∈∆K,

|

X

P c(xi, yri)−

X

Q u(xi, yri)c(xi, yri)| ≤ε·

X

P c(xi, yri).

(4)

It can be seen that there is a relationship between the weight function u and the size M of the complete dataset.

Proposition 1. Assume that (Q, u) is a ε-coreset for (P, F, ∆K, c), where cost c is always positive. The following inequality holds:

|

X

Q u(xi, yri) −M| ≤εM. (5)

Proof. Let w = 0, and Ar = I, where I is the identity matrix. We have that for any data point, c(xi, yri) = ϕ(0) = log 2. By Definition 2, | P

P log 2 −P

Q u(xi, yri) log 2| ≤ ε P

P log 2. Since P

P 1 = M, we have | P

Q u(xi, yri) − M| ≤εM.

Definition (Sensitivity). Given query space (P, F, ∆K, c), the sensitivity of a data point (xi, yri) is defined as the supreme value of fraction between the cost of this point and the cost of all points for all possible classifiers, i.e., sensitivity(xi, yri) ≜ sup f∈F,Ar∈∆K c(xi, yri) P

P c(xi, yri), (6)

where the denominator P

P c(xi, yri) is assumed to be positive. Since it is almost impossible to get the closed form of sensitivity, a function s(xi, yri) is called an upper sensitivity function if for all xi, yri, s(xi, yri) ≥sensitivity(xi, yri).

The total sensitivity for (P, F, ∆K, c) is

S ≜

X

P s(xi, yri). (7)

With an upper bound for the sensitivity and total sensitivity, a sensitivity-based sample from P with a size of M ′ is a set of M ′, independent and identically distributed (i.i.d.), draws from the complete set of data points, where the sam- ple probability is Prob(·) = s(·)

S. Then, the coreset size is bounded according to the following theorem.

Theorem 1 ((Feldman and Langberg 2011)). Given query space (P, F, ∆K, c), let s be the upper sensitivity function, and S be the upper total sensitivity. Let D be the VCdimension of the loss function, and ε, δ ∈(0, 1) be the error and probability control parameters. Then, Q is a random sample of size M ′ that

M ′ ≥10S ε2 (D log S + log(1 δ))), (8)

where the sample probability of point i ∈[1, M] selected each time is si/S. Let the associated weight ui for each point i ∈[1, M] be S si |Q|. We have that (Q, u) is an ε- coreset with probability at least 1 −δ.

Lower Bound

Given a query space, the first question is whether the coreset exists. Studies such as those in (Tolochinksy, Jubran, and Feldman 2022; Samadian et al. 2020) show that for pure logistic regression, where the cost is cross-entropy between prediction and ground truth, the ε-coreset does not exist. The key lemma used is as follows.

Lemma 1 ((Tolochinksy, Jubran, and Feldman 2022)). If every data point (xi, yri) in P has sensitivity(xi, yri) = 1, then the only ε-coreset for P is P itself, i.e., no smaller coreset.

To determine the lower bound of corsets for crowdsourcing learning, we explore three cases that control the size of instances and annotators. Case (a): Multiple Instances, Single Annotator. Assume that there are N instances {xi}N i=1 and one annotator whose confusion layer A0 has diagonal elements a0 and b0. In this case, there are only single annotator, i.e., M = N. This situation will degrade to logistic regression when a0 and b0 are both fixed to 1. For points xi scattered on a circle which does not pass through the zero point:

sensitivity(xi, y0i) = sup w∈Rd,a0,b0∈[0,1]

c(xi, y0i) P

P c(xi, y0i)

(let a0 = b0 = 1) ≥sup w∈Rd c(xi, y0i; a0 = 1, b0 = 1) P

P c(xi, y0i; a0 = 1, b0 = 1)

(Eq. 3) = sup w∈Rd ϕ(−y0iw⊤xi) P

P ϕ(−y0iw⊤xi)

(∗) =1.

(9) We briefly describe the intuition of (∗). A geometric trick is used in the logistic cost function, where the data point xi is augmented with yri to become yrixi. With this trick, all points in Fig. 1(a) can be seen as positive samples. For each yrixi, there is a hyper-plane that can perfectly separate this point from others, i.e., for yrixi, one has yriw⊤xi > 0 holds, while for any other points yrjxj, yrjw⊤xj < 0. Let ∥w∥2 → ∞. We have that ϕ(−yriw⊤xi) → ∞for yriw⊤xi < 0, and ϕ(yrjw⊤xj) → 0 for

17915

<!-- Page 4 -->

(a) (c)

(b) (d)

Hyperplane

**Figure 1.** (a) Data points in R3 scattered on a circle, (b) Cross-sectional view of (a), the hyperplane w exists for every data point; (c) A second-order cone C in R3, and (d) Cross-sectional view of (c), where the dots denote the rows of Ar and the circle denotes the cone C.

yrjw⊤xj > 0. Therefore, supw∈Rd ϕ(−yriw⊤xi) P

P ϕ(−yriw⊤xi) = lim∥w∥2→∞ ϕ(−yriw⊤xi) P

P ϕ(−yriw⊤xi) = 1.

The above analysis holds for every point (xi, yri). Therefore, the sensitivity of every point is 1. According to Lemma 1, no smaller coreset exists in this case. Solution (a): Add Norm Regularization ∥w∥2. To prevent this lower bound, the norm-2 regularization term ∥w∥2 is added to the cost function. In this way, when w →∞, the cost of all points will approach ∞, and thus the sensitivity of any data point will not be 1. With this regularization term and some assumptions, the coreset size is bounded by different sampling methods.

Theorem 2 ((Alishahi and Phillips 2024)). The query space with a single annotator is (P, F, (a0, b0), c), where the confusion layer can be fixed without loss of generality, i.e., a0 = b0 = 1, and cost function is c(yriw⊤xi) = ϕ(yriw⊤xi) + ∥w∥2. Assume that for all i, ∥xi∥2 ≤ 1, and any ssensitivity sample with size M ′ by specific sampling strategy guarantees an ε-coreset with a probability of at least 1 −δ, with sensitivity-based sampling, M ′ = O(d2 log M ε2) holds.

Case (b): Single Instance, Multiple Annotators. Assume that there are M annotators with confusion layer {Ar}M r=1 and only one instance x0. Similarly to case (a), we analyze the sensitivity of data point (x0, yr0). We find that for the cost function in Eq. (3), the sensitivity of every point is 1, which implies that there is no nontrivial coreset. This observation is formally stated as follows.

Concept Case (a) Case (b)

Perspective Instance Annotator Problematic c →∞ c →0 Reg. Term ∥w∥2 log detA⊤ r Ar Existing Usage Avoid overfitting Improve identifiability

Geometry Length Volume

**Table 1.** Correspond concepts in classification and crowdsourcing.

Theorem 3 (No coreset for one-instance crowdsourcing). Given a query space (P, F, ∆K, c), where the instance space contains only one item. If the cost is a CCEM loss function, i.e., Eq. (3), and let the error parameter be ε ∈ (0, 1), then there is only an ε-coreset Q such that Q = P.

Proof. It can be checked that:

• If ar = 1 and br = 1, then c(x0, yr0) = ϕ(−yr0w⊤x0), • If yr0 = 1, ar = 1 and br = 0, then c(x0, yr0) = 0, • If yr0 = −1, ar = 0 and br = 1, then c(x0, yr0) = 0.

Therefore, for any data point, we have:

sensitivity(x0, yr0) = sup w∈Rd,ar,br∈[0,1]

c(x0, yr0) P

P c(x0, yr0)

≥sup w∈Rd c(xi, yri; ar = 1, br = 1) c(xi, yri; ar = 1, br = 1) + P

P ′ 0

=1,

(10) where P ′ = P −{(x0, yr0)}.

With Lemma 1, one concludes that there is no smaller coreset for P.

Solution (b): Add Volume Regularization log detA⊤ r Ar. What we need to prevent this lower bound is an additional item that dominates the cost when the cross-entropy loss approaches zero. We found that the volume regularization satisfied this requirement.

Remind that Ar = ar 1 −br 1 −ar br

. We have log detA⊤ r Ar = log(ar + br −1)2. Either ar →1 and br →0 or ar →0 and br →1, log detA⊤ r Ar →∞holds. Coincidentally, this regularization term is used to improve the identifiability of crowdsourcing (Ibrahim, Nguyen, and Fu 2023), where the volume of Ar cone is maximized. We summarize the corresponding concepts in coresets for logistic regression and crowdsourcing in Table 1. Case (c): Multiple Instances, Multiple Annotators. In this case, it is intuitive that to sample the smallest coreset, the norm and volume regularization terms should both be used. The cost function is:

c(xi, yri) = ∥w∥2 −log detA⊤ r Ar+ ϕ(−yriw⊤xi) −ϕ1(−yriw⊤xi), yri = 1, ϕ(−yriw⊤xi) −ϕ2(−yriw⊤xi), yri = −1.

(11)

In the next section, we show that a better coreset does exist for any input.

17916

<!-- Page 5 -->

Coresets with Volume Regularization Main Results We make the following assumptions.

Assumption 1 (Bounded ∥xi∥2, (Alishahi and Phillips 2024)). For all xi, ∥xi∥2 < 1, i.e., Prob(∥xi∥2 ≥1) = 0. This assumption is easy to satisfy with normalization.

Assumption 2 (Bounded log detA⊤ r Ar). Let ξ ∈(0, 1). The minimum eigenvalue of Ar is greater than or equal to ξ, which implies that |ar+br−1| ≥ξ, and log detA⊤ r Ar ≥ 2 log ξ. Note that log detA⊤ r Ar ≤0.

Remark 1. Assumption 2 is natural when there is no malicious annotator whose annotations are independent of instances. If the minimum eigenvalue of Ar is 0, or ar + br = 1, it can be checked that the output probability is always [ar, br]⊤. Without loss of generality, in our analysis, ar + br > 1. If ar + br < 1, with multiplying by an additional permutation matrix, ar + br > 1 (Ibrahim, Nguyen, and Fu 2023).

With the above assumption, and also, with the cost function Eq. (11), we first define auxiliary functions:

sA(yri, ar, br) =

(2 log |ar+br−1|+log(br−ar+1)−log 2

2 log |ar+br−1|+log(1−br), yri = 1, 2 log |ar+br−1|+log(ar−br+1)−log 2 2 log |ar+br−1|+log(1−ar), yri = −1.

(12)

bA(yri, ar, br) = sA(yri, ar, br) · (2 − 1 log |ar + br −1|).

(13) bx(xi) = 2 + ∥xi∥2

2. (14)

Then, the sensitivity is bound as follows.

Theorem 4 (Sensitivity). Given input data P = (X, Y) = {(xi, yri)} such that |P| = M, let the data points ascending sorted by bA(yri, ar, br) · bx(xi). Then the sensitivity of every (xi, yri) in position m is bounded by s(xi, yri) = O(L(bA(yri,ar,br)·bx(xi)+1)

m), where L is a sufficiently large constant, and the total sensitivity is t =

X

P s(xi, yri) = O(log M +

X

P

L(bAbx + 1)

m).

Compared with the existing bound of sensitivity which only considers the index position m and the norm of the data point ∥xi∥2, our bound extensively considers the factor of the annotator bA. With this upper sensitivity bound, the sampling strategy is given in Algorithm 1, and the bound of coreset size is given in the following theorem.

Theorem 5 (Coreset). Given input data P = (X, Y) = {(xi, yri)} such that |P| = M, let ε, δ ∈(0, 1), for every xi ∈Rd, yri ∈{1, −1}, the cost function is given as Eq. (11). Let (Q, u) be the output of Algorithm 1 while the input is query space (P, F, ∆K, c). Then, with probability at least 1 −δ, (Q, u) is an ε-coreset for (P, F, ∆K, c). And the size of Q is bounded by |Q| = O(log M ε2 (d log log M + log 1 δ)).

## Algorithm

1: CrowdCore Sample Strategy. Input: Query space: (P, F, ∆K, c), and coreset size M ′. Output: Coreset (Q, u), where Q is a subset of P and u is a weight function.

1: Sort the data points (xi, yri) in input P ascending by bA(yri, ar, br) · bx(xi), and record index position m. 2: Compute the upper sensitivity for data points in position m such that s(xi, yri) = L(bA(yri, ar, br) · bx(xi) + 1)

m, where L is a sufficiently large constant. 3: Compute total sensitivity S = P P s(xi, yri). 4: Sample M ′ data points from P to Q with probability s(xi, yri)

S, and set weight u(xi, yri) = S M ′s(xi, yri).

5: return Coreset (Q, u).

Proofs of Main Results Define function g(t) = g(−yriw⊤xi) = c−∥w∥2 = ϕ(t)− ϕri(t)−log(ar+br−1)2, where c is the cost function defined on Eq. (11), and ϕri(t) depends on yri. The properties of the function g are as follows.

• Given yri, the function g is increasing with −yriw⊤xi, • The minimum is min g = min(log 1 ar, log 1 br)−log(ar+ br −1)2 when yriw⊤xi →−∞. • The maximum is max g = max(log 1 1−ar, log 1 1−br) − log(ar + br −1)2 when yriw⊤xi →∞. • g(0) ≥log 2−max(log(ar −br +1), log(br −ar +1))− log(ar + br −1)2 ≥0. Using these properties, the key is to find the zero point of g(−t) = t2. Since the function g is always positive and increasing, it is clear that there is only one zero point t0. However, it is hard to give a closed form for this root. We give a bound of t0 related to (ar, br). Proposition 2. For g(t) = ϕ(t)−ϕri(t)−log(ar+br−1)2, let ˆt0 = p

−log(ar + br −1)2 ∈[0, √−2 log ξ], it holds g(−ˆt0) > ˆt2

0.

Proof. By the symmetry of a and b, let ϕri = ϕ1. The proof for ϕri = ϕ2 is similar. Let ˆt0 = p

−log(ar + br −1)2. We have g(−ˆt0) =ϕ(−ˆt0) −ϕ1(−ˆt0) −log(a + b −1)2

=ϕ(−ˆt0) −ϕ1(−ˆt0) + ˆt2

0, (15)

therefore, g(−ˆt0) −ˆt2

0 = ϕ(−ˆt0) −ϕ1(−ˆt0) ≥ min(log 1 ar, log 1 br) > 0. This bound t0 is tight since when ar →1, br →0, g(−ˆt0) = ˆt2

0.

Lemma 2. For g(t) = ϕ(t) −ϕri(t) −log(ar + br −1)2, let c > 0. Then, for every t > 0, g(ct) + t2 g(−ct) + t2 ≤max g g(0) (2 − 1 log |ar + br −1|)(2 + c2).

(16)

17917

<!-- Page 6 -->

MNIST MiniBooNE

UniSamp SenSamp GradSamp CrowdCore UniSamp SenSamp GradSamp CrowdCore

1% 1.422±0.986 0.647±0.439 2.408±1.467 0.471±0.212 1.091±0.425 1.180±0.699 1.233±0.388 0.804±0.130 Time 8.63±0.62 15.36±0.16 200.22±9.58 16.49±0.70 0.29±0.01 4.94±0.09 4.99±0.10 4.98±0.03

3% 0.789±0.418 0.599±0.360 1.181±0.677 0.467±0.191 0.636±0.268 0.785±0.315 1.039±0.207 0.471±0.050 Time 23.98±1.78 31.92±1.89 300.10±9.39 32.85±1.49 0.48±0.02 4.93±0.04 5.13±0.12 5.07±0.03

5% 0.784±0.510 0.422±0.257 0.856±0.654 0.394±0.175 0.451±0.179 0.668±0.269 1.062±0.484 0.345±0.090 Time 39.26±0.67 47.51±2.12 590.95±10.36 47.15±2.25 0.65±0.02 5.04±0.03 5.21±0.02 5.22±0.02

7% 0.568±0.336 0.312±0.188 0.890±0.729 0.344±0.169 0.424±0.164 0.534±0.189 0.601±0.223 0.343±0.129 Time 58.33±3.12 58.18±2.29 790.95±10.36 62.72±2.55 0.84±0.02 5.15±0.03 5.33±0.06 5.32±0.04

9% 0.362±0.229 0.317±0.089 0.793±0.634 0.256±0.208 0.313±0.172 0.478±0.244 0.628±0.153 0.235±0.107 Time 63.78±3.58 77.79±4.97 900.28±10.63 73.52±1.98 1.04±0.02 5.25±0.04 5.41±0.04 5.40±0.02

**Table 2.** Approximation Error and Running Time of Synthetic Annotations.

Proof. See the appendix.

Then, we give the proof of our main results. For a data point (xi, yri), according to Lemma 2, g(∥xi∥2 t) + t2 g(−∥xi∥2 t) + t2

≤max g g(0)

2 − 1 log |ar + br −1|

(2 + ∥xi∥2

2). (17)

We divide the bound in Eq. (17) into two parts:

bA(yri, ar, br) = max g g(0) (2 − 1 log |ar + br −1|), (18)

bx(xi) = 2 + ∥xi∥2

2. (19) According to Lemma 4.2 in (Tolochinksy, Jubran, and Feldman 2022), for (r′, i′)̸ = (r, i), it holds c(x′ i, yr′i′) ≤max

P c(xi, yri) ≤L(bAbx + 1)c(xi, yri),

(20) where L is a sufficiently large constant.

Then, sort points in P with bAbx. For data point (xi, yri) in the m position, we have

X

Top m c(x′ i, yr′i′) ≥

X

Top m

1 L(bAbx + 1)c(xi, yri)

≥m · c(xi, yri)

L(bAbx + 1).

(21)

Consider the cost on all data points in P, it holds X

P c(xi, yri) ≥

X

Top m c(x′ i, yr′i′) ≥m · c(xi, yri)

L(bAbx + 1). (22)

Therefore, the upper sensitivity function is derived, i.e., sensitivity(xi, yri) = sup f∈F,Ar∈∆K c(xi, yri) P

P c(xi, yri)

≤L(bAbx + 1)

m = s(xi, yri),

(23)

where m is the index after sorting.

Finally, summarize the upper sensitivity function over all data points to get the total sensitivity:

S =

X

P s(xi, yri) = O(log M +

X

P

L(bAbx + 1)

m). (24)

Theorems 4 and 5 are directly derived from Theorem 1 and Eq. (24).

## Experiments

## Experimental Setup

To solve these three research questions, we conduct experiments on both synthetic datasets and real-world datasets.

• RQ1: Though there is a theoretical guarantee of the approximation error of cost, how does the coreset sampling algorithm perform with the large-scale dataset? • RQ2: How does the model perform on unseen data with different coreset sampling algorithms? • RQ3: How does the annotators’ confusion matrix affect the approximation quality and generalization performance of the constructed coreset? Four comparable sampling algorithms are used. UniSamp: Sample annotations with the same probability (Alishahi and Phillips 2024). SenSamp: Only consider the norm of inputs ∥xi∥2 in the sensitivity (Tolochinksy, Jubran, and Feldman 2022). GradSamp: Set the sample probability to the norm of the gradient of parameters. CrowdCore: See Algorithm 1.

Extending to Multiple Classes A one-vs-rest strategy is taken to handle multi-class classification. We specify the label class as positive and the rest of the classes as negative.

For K > 2 classes, the complete confusion matrix A is a K × K matrix. For a sample with label y, the one-vs-rest confusion matrix is a 1 −b 1 −a b

, where a = Ay,y, and b = 1 − 1 K−1

P k̸=y Ak,y.

17918

<!-- Page 7 -->

5% 10% 15% 20% 0.5

0.6

0.7

0.8

LabelMe

5% 10% 15% 20% 0.3

0.4

0.5

0.6

Music

UniSamp SenSamp GradSamp CrowdCore

**Figure 2.** Performance of Classifiers Trained on Real-World Annotations.

Performance on Synthetic Annotations (RQ1) Settings. We take MNIST (Deng 2012) and Mini- BooNE (Aguilar-Arevalo et al. 2009) datasets. The number and dimension of MiniBooNE data points are 70,000 and 784, respectively. The number and dimension of MNIST data points are 130,064 and 50, respectively. To generate noisy annotations, R = 5 annotators are simulated. The ground-truth of the confusion layer is generated by Ar = Normalization(I+0.2M rand), where M rand is sampled from uniform distribution in range [0, 1].

Results. We run sampling algorithms and report the mean and standard error of the mean absolute approximation error (1e-3) and the running time (in seconds), as shown in Table 2. As the sample size increases, the approximation error for all sampling methods generally decreases. Crowd- Core and SenSamp perform better than the other two, implying that sensitivity-based sampling is helpful for preserving dataset information. When the coreset size is pretty small, the CrowdCore performs significantly better than others.

Performance on Human Annotations (RQ2) Settings. LabelMe (Rodrigues and Pereira 2018) is an open-source dataset containing 59 annotators, 1,000 instances, and 8 classes. The backbone is the VGG-16 network. Music (Rodrigues, Pereira, and Ribeiro 2014) is a music genre classification dataset. The backbone is a 3-layer MLP classifier. Normalization is used to control the feature norm before the last network layer. The training epochs for LabelMe and Music are set to 25 and 120, respectively.

Results. We run sampling algorithms and report the classification accuracy on test data, as shown in Figure 2. CrowdCore consistently maintains the highest performance, demonstrating its effectiveness in finding coresets, whereas GradSamp shows a significant decline in model performance, suggesting that the coreset sizes for this strategy should be larger. The performance gap between CrowdCore and other methods increases at smaller coresets, indicating that it is better at finding more relevant data.

Case Study (RQ3) We conduct a case study in LabelMe to analyze how annotator identifiability |ar + br −1| influence coreset selection.

0.0 0.2 0.4 0.6 0.8 1.0 Annotator Identifiability

0

2

4

6

8

10

Normalized weight (1e-5)

Uniform SenSamp

GradSamp CrowdCore

**Figure 3.** Weight across Sampled Annotations.

We take annotators in the dataset with different confusion properties, including: 1) high-quality with ar, br →1, 2) systematic-bias with ar, br →0, and 3) non-identifiable with ar + br →1. For the former two, identifiability |ar + br −1| →1 and for the last one, identifiability |ar + br −1| →0. Figure 3 shows the expected value of the normalized weights as a function of |ar + br −1|. We find that CrowdCore shows a clear preference for data labeled by high-quality and systematic-biased annotators, while actively downweights samples from non-identifiable annotators. This result shows that CrowdCore not only selects informative instances but also implicitly performs data denoising, enhancing robustness with different annotators.

## Conclusion

In this paper, we focus on the coresets for end-to-end learning from crowdsourced data. By analyzing the CCEM problem with data sensitivity, we provide: (1) It is impossible to find coresets smaller than the complete dataset with confusion layers under the CCEM loss. (2) With the volume regularization term, coresets exist for any input data. (3) After proposing the upper-sensitivity function, we derive a novel sample algorithm called CrowdCore. Experimental validation on synthetic and real datasets confirms that our proposed method can effectively sample better coresets compared to some existing sampling strategies.

17919

<!-- Page 8 -->

## Acknowledgments

This work is supported by the Science and Technology Development Fund (FDCT) under Grant number 0029/2023/RIA1, and the AI Super Computing Platform of Macau University of Science and Technology.

## References

Aguilar-Arevalo, A.; Anderson, C.; Bartoszek, L.; Bazarko, A.; Brice, S. J.; Brown, B.; Bugel, L.; Cao, J.; Coney, L.; Conrad, J.; et al. 2009. The miniboone detector. Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment, 599(1): 28–46. Alishahi, M.; and Phillips, J. M. 2024. No dimensional sampling coresets for classification. In Proceedings of the 41st International Conference on Machine Learning, 1008– 1049. Vienna, Austria. Chen, J.; Yang, Q.; Huang, R.; and Ding, H. 2022. Coresets for relational data and the applications. In Proceedings of the 36th International Conference on Neural Information Processing Systems, 434–448. New Orleans, LA, United States. Chu, Z.; Ma, J.; and Wang, H. 2021. Learning from crowds by modeling common confusions. In Proceedings of the 35th AAAI Conference on Artificial Intelligence, 5832–5840. Virtual Conference. Deng, L. 2012. The mnist database of handwritten digit images for machine learning research. IEEE Signal Processing Magazine, 29(6): 141–142. Fang, Y.; Sun, H.; Chen, P.; and Huai, J. 2018. On the cost complexity of crowdsourcing. In Proceedings of the 27th International Joint Conference on Artificial Intelligence, 1531–1537. Stockholm, Sweden. Feldman, D.; and Langberg, M. 2011. A unified framework for approximating and clustering data. In Proceedings of the 43rd Annual ACM Symposium on Theory of Computing, 569–578. San Jose, CA, United States. Feldman, D.; Schmidt, M.; and Sohler, C. 2013. Turning big data into tiny data: constant-size coresets for kmeans, PCA and projective clustering. In Proceedings of the 24th Annual ACM-SIAM Symposium on Discrete Algorithms, 1434–1453. New Orleans, LA, United States. Fu, X.; Huang, K.; Sidiropoulos, N. D.; and Ma, W.-K. 2019. Nonnegative matrix factorization for signal and data analytics: Identifiability, algorithms, and applications. IEEE Signal Processing Magazine, 36(2): 59–80. Ibrahim, S.; and Fu, X. 2021. Crowdsourcing via annotator co-occurrence imputation and provable symmetric nonnegative matrix factorization. In Proceedings of the 38th International Conference on Machine Learning, 4544–4554. Virtual Conference. Ibrahim, S.; Nguyen, T.; and Fu, X. 2023. Deep learning from crowdsourced labels: Coupled Cross-Entropy Minimization, identifiability, and regularization. In Proceedings of the 11th International Conference on Learning Representations, 1–39. Kigali, Rwanda.

LeCun, Y.; Bengio, Y.; and Hinton, G. 2015. Deep learning. Nature, 521(7553): 436–444. Mirzasoleiman, B.; Bilmes, J.; and Leskovec, J. 2020. Coresets for data-efficient training of machine learning models. In Proceedings of the 37th International Conference on Machine Learning, 6950–6960. Virtual Conference. Momeni, A.; Rahmani, B.; Scellier, B.; Wright, L. G.; McMahon, P. L.; Wanjura, C. C.; Li, Y.; Skalli, A.; Berloff, N. G.; Onodera, T.; Oguz, I.; Morichetti, F.; del Hougne, P.; Gallo, M. L.; Sebastian, A.; Mirhoseini, A.; Zhang, C.; Markovic, D.; Brunner, D.; Moser, C.; Gigan, S.; Marquardt, F.; Ozcan, A.; Grollier, J.; Liu, A. J.; Psaltis, D.; Al`u, A.; and Fleury, R. 2025. Training of physical neural networks. Nature, 645(8079): 53–61. Rodrigues, F.; Pereira, F.; and Ribeiro, B. 2014. Gaussian process classification and active learning with multiple annotators. In Proceedings of the 31st International Conference on International Conference on Machine Learning, 433–441. Beijing, China. Rodrigues, F.; and Pereira, F. C. 2018. Deep learning from crowds. In Proceedings of the 32nd AAAI Conference on Artificial Intelligence and 30th Innovative Applications of Artificial Intelligence Conference and 8th AAAI Symposium on Educational Advances in Artificial Intelligence, 1611–1618. New Orleans, LA, United States. Samadian, A.; Pruhs, K.; Moseley, B.; Im, S.; and Curtin, R. 2020. Unconditional coresets for regularized loss minimization. In Proceedings of the 23rd International Conference on Artificial Intelligence and Statistics, 482–492. Palermo, Italy. Tanno, R.; Saeedi, A.; Sankaranarayanan, S.; Alexander, D. C.; and Silberman, N. 2019. Learning from noisy labels by regularized estimation of annotator confusion. In Proceedings of the 32nd IEEE/CVF Conference on Computer Vision and Pattern Recognition, 11236–11245. Long Beach, CA, United States. Tolochinksy, E.; Jubran, I.; and Feldman, D. 2022. Generic coreset for scalable learning of monotonic kernels: Logistic regression, sigmoid and more. In Proceedings of the 39th International Conference on Machine Learning, 21520– 21547. Baltimore, MD, United States. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Łukasz Kaiser; and Polosukhin, I. 2017. Attention is all you need. In Proceedings of the 31st International Conference on Neural Information Processing Systems, 6000–6010. Long Beach, CA, United States. Wang, L.; and Zhou, Z.-H. 2016. Cost-saving effect of crowdsourcing learning. In Proceedings of the 27th International Joint Conference on Artificial Intelligence, 2111– 2117. New York, NY, United States. Wei, H.; Xie, R.; Feng, L.; Han, B.; and An, B. 2022. Deep learning from multiple noisy annotators as a union. IEEE Transactions on Neural Networks and Learning Systems, 34(12): 10552–10562.

17920
