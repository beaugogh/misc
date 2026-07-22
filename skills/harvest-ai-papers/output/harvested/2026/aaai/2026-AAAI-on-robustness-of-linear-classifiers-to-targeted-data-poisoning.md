---
title: "On Robustness of Linear Classifiers to Targeted Data Poisoning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39301
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39301/43262
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# On Robustness of Linear Classifiers to Targeted Data Poisoning

<!-- Page 1 -->

On Robustness of Linear Classifiers to Targeted Data Poisoning

Nakshatra Gupta1, Sumanth Prabhu S1*, Supratik Chakraborty2, Venkatesh R1

1Tata Consultancy Services, Pune, India 2IIT Bombay, Mumbai, India nakshatra.g@tcs.com, sumanthsprabhu@gmail.com, supratik@cse.iitb.ac.in, r.venky@tcs.com

## Abstract

Data poisoning is a training-time attack that undermines the trustworthiness of learned models. In a targeted data poisoning attack, an adversary manipulates the training dataset to alter the classification of a targeted test point. Given the typically large size of training dataset, manual detection of poisoning is difficult. An alternative is to automatically measure a dataset’s robustness against such an attack, which is the focus of this paper. We consider a threat model wherein an adversary can only perturb the labels of the training dataset, with knowledge limited to the hypothesis space of the victim’s model. In this setting, we prove that finding the robustness is an NP-Complete problem, even when hypotheses are linear classifiers. To overcome this, we present a technique that finds lower and upper bounds of robustness. Our implementation of the technique computes these bounds efficiently in practice for many publicly available datasets. We experimentally demonstrate the effectiveness of our approach. Specifically, a poisoning exceeding the identified robustness bounds significantly impacts test point classification. We are also able to compute these bounds in many more cases where state-of-the-art techniques fail.

Extended Version — https://doi.org/10.5281/zenodo.17627646

## Introduction

Data poisoning is a training-time attack wherein an adversary perturbs the training dataset to alter the predictions of the trained models (Biggio, Nelson, and Laskov 2012). Here, the perturbation is called poisoning. Manually determining whether a training dataset is poisoned or not is challenging due its size. Consequently, this attack affects the trustworthiness of machine learning models and hinders their deployment in industries (Kumar et al. 2020).

Targeted data poisoning refers to an adversary manipulating the training data to alter the prediction of a single (or a small fixed subset of) test data. While targeted data poisoning can be sophisticated, such as backdoor attacks that use patterns called triggers, we focus on trigger-less attack. In such an attack, an adversary targets a specific test point

*Now at Relyance AI, Bangalore, India Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

and aims for the victim’s classifier to classify this point as a desired class. An example is a loan applicant adversary who poisons the training data so that the model trained on the poisoned data approves the adversary’s loan.

We consider a practical adversary who can poison the training dataset only by contaminating labels. While contaminating the features of a dataset can be difficult, labels can be easily manipulated as label errors are common, especially when they are collected from external sources (Adebayo et al. 2023). Furthermore, we assume that the adversary has knowledge of only the hypothesis space of the victim’s classifier, but not the training procedure or the actual classifier. In other words, the victim’s training procedure is treated as a black-box. In this setting, we define robustness as:

The minimum number of label perturbations in the training dataset required for a classifier from the hypothesis space to classify the test point as desired. For example, consider the dataset Pen-based Handwritten Digit Recognition (Alpaydin and Alimoglu 1996). In the dataset, a test point shown in Figure 1 represents the handwritten digit ‘0’. However, our tool finds that it can be labeled as the digit ‘4’ by changing the labels of just two points in the training dataset, out of thousands.

The above notion of robustness is not only useful to measure confidence in the training data, but also in contesting a model’s predictions. When a model produces an undesirable decision, the user may want to identify the minimal set of training point labels that potentially influenced the outcome. If any of these labels are incorrect, the user can flag and contest the decision. This application is directly addressed by a solution to the robustness problem defined above.

In our setting of targeted black-box poisoning by label perturbation, we focus on linear classifiers in this work. While existing data poisoning work typically considers linear classifiers (Biggio, Nelson, and Laskov 2011, 2012; Xiao, Xiao, and Eckert 2012; Xiao et al. 2015; Suya et al. 2024; Zhao et al. 2017; Paudice, Mu˜noz-Gonz´alez, and Lupu 2019; Yang, Xu, and Yu 2023), our setting considers a weaker threat model. Moreover, linear models are still relevant as they perform well on many tasks (Ferrari Dacrema, Cremonesi, and Jannach 2019; Tramer and Boneh 2020; Chen et al. 2021; Chen, Ding, and Wagner 2023) and are subject of several recent related works (Yang, Xu, and Yu 2023; Yang, Jain, and Wallace 2023; Suya et al. 2024).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

21531

<!-- Page 2 -->

**Figure 1.** A test point (leftmost plot) and two training points all originally labeled as digit ‘0’. Our tools finds that modifying only these two training points as digit ‘4’ can change the test point’s label to digit ‘4’.

We make five contributions in this paper. We first establish a theoretical result showing that the problem of finding robustness is NP-Complete. To address this challenge, we propose techniques that approximate robustness. In this direction, our second contribution is a partition-based method that computes a lower bound for robustness. Third, we introduce an augmented learning procedure designed to find an upper bound for robustness. Our fourth contribution is a prototype tool ROBUSTRANGE, which implements our novel techniques. Finally, we evaluate ROBUSTRANGE on 15 publicly available datasets of different sizes. Our experiments reveal several interesting facts: the average robustness can be as low as 3%, ROBUSTRANGE performs better than a SOTA tool (Yang, Xu, and Yu 2023), even when the SOTA tool knows the victim’s classifier and learning procedure.

## Related Work

Data poisoning attacks have received considerable attention as a primary security threat during the training stage of machine learning (Barreno et al. 2010; Tian et al. 2022). Depending on the adversary’s goals, these attacks can be either indiscriminate or targeted. In an indiscriminate attack, the adversary aims to maximize the overall loss of victim’s classifier, which was the focus of many works (Biggio, Nelson, and Laskov 2011, 2012; Xiao, Xiao, and Eckert 2012; Xiao et al. 2015; Suya et al. 2024). In contrast, a targeted attack aims to alter the prediction of a specific test point while minimally affecting overall loss, which is the focus of this paper.

A targeted attack can be achieved by assuming different capabilities of the adversary. For instance, an attacker can add/modify/remove training points without changing labels (Shafahi et al. 2018; Suciu et al. 2018; Zhu et al. 2019; Yang, Jain, and Wallace 2023), posses full or partial knowledge of the victim’s learning process (Cin`a et al. 2021; S¸uvak et al. 2022; Paudice, Mu˜noz-Gonz´alez, and Lupu 2019), or trigger poisoning when the test point is embedded by certain patterns (Chen et al. 2017; Saha, Subramanya, and Pirsiavash 2020; Gu et al. 2019). We assume a more constrained attacker who can only perturb labels, lacks knowledge of the victim’s learning process (black-box), and targets a specific test point.

There are techniques that construct a poisoned dataset with stronger threat model. In particular, (Zhao et al. 2017) also considers label perturbations and a black-box victim model, but requires a bound on robustness to compute the poisoned dataset, along with an objective model. The work in (Paudice, Mu˜noz-Gonz´alez, and Lupu 2019) also computes a perturbation set, but it similarly requires a bound and the victim’s loss function. The work closest to ours is (Yang, Xu, and Yu 2023), which aims to find the minimal labelperturbed set. However, it only computes an upper bound, and, more importantly, requires knowledge of the victim’s model and loss function to determine the influence function (Koh and Liang 2017).

(Gao, Karbasi, and Mahmoody 2021) gives a relationship between the dataset size and maximum allowed perturbations, whose accuracy has been subsequently improved in (Wang, Levine, and Feizi 2022a). The work in (Hanneke et al. 2022) characterizes the optimal error rate when the dataset is poisoned. In these works, data points are either removed or inserted. Furthermore, these works characterizes bounds on targeted data poison, while we compute upper and lower bounds. An orthogonal line of work is that of certified robustness (Rosenfeld et al. 2020; Levine and Feizi 2020; Wang, Levine, and Feizi 2022b; Jia et al. 2022), which gives a model that predicts with guaranteed robustness.

Problem Setting Preliminaries Consider the task of binary classification from d dimensional input features X ⊆Rd to binary output labels Y = {+1, −1}. The goal of the classification task is to find a function (called classifier) f: X →Y that has a small generalization error. In machine learning, f is derived from a given set of hypotheses (called hypothesis space) H and a set of labeled training data D. We assume H is a set of linear functions fw,b of the form fw,b(x) = sign(wT x + b), where w ∈Rd is the weight parameter, and b ∈R is the bias parameter. The labeled training data D is generated from an i.i.d over X ×Y. Given H and D, the classification task is to find a model fw,b ∈H that minimizes a loss function (e.g., hinge loss) over D.

Threat Model We model the overall workflow via causative targeted attack (Barreno et al. 2010), which is a game between a victim and an attacker, that proceeds as follows:

## 1 The victim generates a clean training data

Dc = {(xi, yi) | i ∈[m]} from an i.i.d over X × Y. 2. The attacker poisons Dc by perturbing (a subset of) labels to get Dp = {(xi, y′ i) | i ∈[m], y′ i = yi or y′ i = −yi}. 3. The victim finds a model fw,b ∈H that minimizes a loss function over Dp. 4. The attacker has a target test point with label (xt, yt) ∈ X × Y, where (xt, y) is not in Dc for any y ∈Y. The attacker wins the game if the victim learns a model fw,b from Dp such that fw,b(xt) = yt. Otherwise, victim wins the game.

We assume an attacker who can only perturb labels in Dc, and is aware of the victim’s hypothesis space, but not the training procedure, the loss function, or the model’s weights.

21532

<!-- Page 3 -->

Robustness The robustness r of a dataset Dc = {(xi, yi) | i ∈[m]} with respect to a target test point (xt, yt) is the minimum number of label perturbations required for the attacker to win the above game. Sans knowledge of the victim’s loss function, we define robustness as follows. Let P be the set of all (possibly) poisoned datasets Dp = {(xi, y′ i) | i ∈ [m], y′ i = yi or y′ i = −yi} s.t. there exists fw,b ∈H with:

1. fw,b(xi) = y′ i, ∀i ∈[m] 2. fw,b(xt) = yt Then r = minDp∈P

Pm i=1 I(y′ i̸ = yi), where I is the indicator function.

Note that some authors prefer to define robustness as the maximum number of label perturbations in Dc such that no classifier in H learned from the poisoned data classifies the test point xt as yt. Clearly, this is r −1, where r is as defined above. For computational simplicity, we use the definition provided above.

Computing Robustness A naive way to compute robustness is by perturbing labels of subsets of the training dataset Dc in increasing order of subset size, and finding whether there exists a classifier that satisfies all required conditions for the poisoned dataset. The time complexity of such an algorithm is clearly exponential in |Dc|. Hence, a natural question is whether this algorithm can be improved. Theorem 1 shows that this is unlikely.

Theorem 1. Given a dataset Dc = {(xi, yi) | i ∈[m]} and a target test point (xt, yt), deciding whether its robustness r is less than a threshold κ is NP-Complete, when H is a set of linear binary classifiers.

Proof Sketch. In NP: Given a witness classifier fw,b, we can check whether (a) fw,b(xt) = yt, and (b) Pm i=1 I(fw,b(xi)̸ = yi) < κ in polynomial time. Alternatively, given a witness poisoned dataset Dp = {(xi, y′ i) | i ∈ [m]}, we can check in polynomial time if (a) Pm i=1 I(y′ i̸ = yi) < κ, and (b) there exists a linear classifier fw,b that satisfies fw,b(xt) = yt and fw,b(xi) = y′ i for all i ∈[m]. The latter can be done by standard techniques for solving linear systems of equations, viz. Gaussian elimination.

NP-hardness: We show this by reduction from the vertex cover problem. Let G = (V, E) be an undirected graph, where V is the set of vertices, and E ⊆V × V is the set of edges. A vertex cover of G is a subset C of V such that for every edge (u, v) ∈V, at least one of u, v is in C. Given G and a threshold κ, the vertex cover problem asks whether G has a vertex cover C s.t. |C| < κ. It is well known (Karp 2009) that the vertex cover problem is NPcomplete. We give below a polynomial-time reduction from the vertex cover problem to the problem of deciding if the robustness of a dataset w.r.t. a target test point is less than a threshold. This proves NP-hardness of deciding if robustness is less than a threshold.

Let V = {v1,... vn} be the set of vertices in G. We create a training dataset Dc ⊆X × Y, where X = {0, 1}n+1 and Y = {+1, −1}. Thus, every x ∈X can be thought of as a

0-1 vector of n+1 dimensions. Below, we use x[j] to denote the jth component of vector x, for j ∈{1,... n + 1}.

For every vi ∈V, we add a training datapoint (xi, yi) to Dc, where (a) xi[j] = 1 iff i = j, and (b) yi = −1. We say that these datapoints encode vertices in V. Similarly, for every edge (vi, vj) ∈E, we add a training datapoint (xi,j, yi,j), where (a) xi,j[k] = 1 iff either i = k or j = k or k = n + 1, and (b) yi,j = +1. We say that these datapoints encode edges in E. As an example, if V = {v1, v2, v3} and E = {(v1, v2), (v2, v3), (v3, v1)}, then Dc = DV c ∪ DE c, where DV c = {

(1, 0, 0, 0), −1

,

(0, 1, 0, 0), −1

,

(0, 0, 1, 0), −1

} encodes the three vertices, and DE c = {

(1, 1, 0, 1), +1

,

(0, 1, 1, 1), +1

,

(1, 0, 1, 1), +1

} encodes the three edges. Notice that for Dc defined above, there exists a linear classifier fw,b such that fw,b(xi) = yi for all (xi, yi) ∈Dc. Indeed, if w[j] = −1 for j ∈ {1,... n}, w[n+1] = 3, and if b = 0, then sign(wT x+b) = y for all (x, y) ∈Dc.

Finally, we construct the test datapoint (xt, yt), where xt[j] = 0 for all j ∈{1,... n}, xt[n + 1] = 1 and yt = −1. For the abve example, (xt, yt) =

(0, 0, 0, 1), −1

. Notice that the linear classifier discussed above that correctly classifies all datapoints in Dc no longer gives fw,b(xt) = yt.

With Dc and (xt, yt) defined as above, we claim that the graph G has a vertex cover of size less than κ iff the robustness of Dc w.r.t. (xt, yt) is less than κ. The only if part is easy to prove. Suppose C is a vertex cover of G, and |C| < κ. We construct the poisoned dataset Dp by changing the label (to +1) of only those datapoints in Dc that encode vertices in C. A linear classifier fw,b(x) = sign(wT x + b) for Dp that also satisfies fw,b(xt) = yt can now be obtained as follows: w[i] = 3 for all vi ∈C, w[i] = −1 for all vi̸ ∈C, w[n + 1] = −1 and b = 0. In our running example with 3 vertices, considering the vertex cover C = {v1, v2}, we get Dp = {

(1, 0, 0, 0), +1

,

(0, 1, 0, 0), +1

,

(0, 0, 1, 0), −1

,

(1, 1, 0, 1), +1

,

(0, 1, 1, 1), +1

,

(1, 0, 1, 1), +1

}. To prove the if part, let S be the subset of datapoints in Dc whose labels are flipped to obtain Dp, and suppose |S| < κ. Let fw,b be a linear classifier corresponding to Dp that satisfies fw,b(xt) = yt. From the definition of (xt, yt), it follows that w[n + 1] + b < 0. Note that for every non-poisoned datapoint (xi,j, +1) corresponding to an edge (vi, vj) ∈E, we must also have fw,b(xi,j) = 1, or w[i] + w[j] + w[n + 1] + b ≥0. This requires at least one of the datapoints corresponding to vi or vj to be poisoned, as otherwise, we would have w[i] < 0 and w[j] < 0, which is inconsistent with w[i]+w[j]+w[n+1]+b ≥0. In general, the set S may contain datapoints encoding both vertices and edges in G. We describe below a process for successively transforming S, such that it eventually contains only datapoints encoding vertices in V. Specifically, for every datapoint (xi,j, +1) in S that encodes an edge (vi, vj) in graph G, we check if the datapoint encoding vi (or vj) is also in S. If so, we simply remove (xi,j, +1) from S; otherwise, we add the datapoint corresponding to vi (resp. vj) to S and remove all datapoints corresponding to edges incident on vi (resp. vj) from S. By repeating this process, we obtain a

21533

<!-- Page 4 -->

poisoned dataset D′ p in which every poisoned datapoint corresponds to a vertex in V. Let the corresponding set of datapoints whose labels have been flipped in D′ p be called S′. Following the same reasoning as in the proof of the ”only if” part above, the linear classifier fw,b corresponding to Dp can be modified to yield a linear classifier fw,b

′ for D′ p that also satisfies fw,b

′(xt) = yt. Since the datapoint corresponding to every edge (vi, vj) ∈E has its label unchanged in D′ p, the datapoint corresponding to either vi or vj must have been poisoned in D′ p. Hence, the set of poisoned datapoints must correspond to a subset of vertices that forms a vertex cover of G. Since we added at most one datapoint corresponding to a vertex in S when removing a datapoint corresponding to an edge from S, we have |S′| ≤|S| < κ.

Since perturbing subsets results in an exponential algorithm, it does not scale even for a small dataset. To overcome this, we propose to compute an approximation of robustness r. Notice that the victim is interested in how low the robustness of their dataset is, to ensure that it is not susceptible to an attack, while the attacker’s interest lies in how high the robustness is, so that the attack is likely to succeed without detection. Considering these perspectives, we compute both a lower bound ˇr and an upper bound ˆr of robustness r, such that it is guaranteed that ˇr ≤r ≤ˆr.

Lower Bound Robustness ˇr via Partitioning We observe that the problem of finding robustness for linear classifiers can be formulated as an optimization problem. In particular, it can be encoded as a mixed-integer linear program (MILP) using the big M method (Bazaraa, Jarvis, and Sherali 2011), assuming a known bound on the range of the linear classifier function. A solution to this optimization problem determines the weights of the function that classifies the test point as required, while minimizing misclassifications on the training dataset. More formally, for a dataset Dc and a test point (xt, yt), we encode the problem as the following optimization problem:

Variables: • w1,..., wd, b ∈R as weights and bias, and • δ1,..., δm ∈{0, 1} as indicators for label perturbations. Objective: Minimize Pm i=1 δi Constraints:

yt (w · xt + b) ≥ϵ yi (w · xi + b) + M δi ≥ϵ, ∀i ∈[m] yi (w · xi + b) −M (1 −δi) ≤−ϵ, ∀i ∈[m]

Parameters: M ≫0 is a large integer constant, ϵ ≈0, and (xi, yi) ∈Dc.

A solution to the problem provides weights and bias (w1,..., wd, b) that classifies the test point xt as yt and minimizes the sum of perturbed labels in Dc, denoted by Pm i=1 δi. The first constraint ensures that yt = sign(w·xi + b). For each point (xi, yi) ∈Dc, the next two constraints ensure the following:

δi =

0 yi = sign(w · xi + b) 1 yi̸ = sign(w · xi + b)

For instance, δi = 0 makes the second constraint yi (w · xi + b) ≥ϵ, which in turn makes yi = sign(w · xi + b). Similarly, δi = 1 makes the third constraint yi (w · xi + b) ≤ ϵ, which makes yi̸ = sign(w · xi + b). These constraints additionally adds the conditions yi (w · xi + b) < M and yi (w · xi + b) > −M, resp..

Hence, a solution gives the robustness r (where r = Pm i=1 δi), along with the labels that were perturbed (yi for which δi is 1). A solution exists only when w · xi + b is in the interval (−M, M).

Since the complexity of solving such optimization problems is exponential, we can get robustness in this way for only small datasets. To scale this, we propose an optimization approach that finds a lower bound of robustness. In this approach, the dataset is partitioned into smaller size, then robustness is computed individually for each partition, and finally the results are summed. Although this sum provides a lower bound, it significantly improves the scalability as the optimization problem is on small sized sets.

Consider the partition of Dc into k ∈N disjoint subsets D1 c... Dk c, where each subset Dj c contains m/k points, except for the last subset, which contains the remaining points.

For each partition Dj c we compute robustness r j by encoding it as the optimization problem(as before). Finally, we compute the sum of these robustness ˇr = Pk j=1 r j.

Theorem 2. For dataset Dc and a test point (xt, yt), ˇr ≤r.1

Upper Bound Robustness ˆr via Augmentation

In addition to the lower bound, we also compute an upper bound of robustness. For this purpose, we train a linear classifier on an augmented version of the training dataset Dc. The augmentation biases the learning to train a classifier that classifies the test point xt as yt. While theoretically this classifier may not minimize the label perturbations of Dc, in practice we observe that it will give a tighter upper bound. Moreover, this procedure will be quick, as it requires only learning a classifier, hence scales for large datasets.

In order to find such a classifier, we restrict our objective to learn a classifier fw,b ∈H such that fw,b(xt) = yt. Since not all classifiers can achieve this objective, we first introduce a targeted augmentation scheme, wherein k′ ∈N identical copies of the test point (xt, yt) are added to Dc. Let the augmented set be D′ c = Dc

S{(xt, yt)}k′, where {(xt, yt)}k′ is a multi-set of k′ copies of (xt, yt).

We then train a classifier on D′ c by minimizing the empirical loss with respect to a loss function l:

fw,b = arg min fw,b∈H

1 m + k′



      m X i=1 l(fw,b(xi), yi)+ k′ X j=1 l(fw,b(xt), yt)



     

Once a classifier fw,b is learned on the augmented dataset, it is checked whether the classifier correctly classifies the

1Remaining proofs are in the extended version.

21534

<!-- Page 5 -->

## Algorithm

## 1 ROBUSTNESSINTERVAL(Dc, (xt, yt)) Input:

Dc – training dataset, (xt, yt) – test point Parameter: M, k, k′, l, ϵ – hyperparameters Output: lower bound ˇr and upper bound ˆr robustness

1: D1 c,..., Dk c ←RANDOMPARTITION(Dc, k) 2: for j = 1 to k do 3: r j ←MILPSOLVE(Dj c, (xt, yt), M) 4: end for 5: ˇr ←Pk j=1 r j

6: D′ c ←AUGMENT(Dc, (xt, yt), k′) 7: fw,b ←LEARNCLASSIFIER(D′ c, l) 8: ˆr ←Pm i=1 I(fw,b(xi)̸ = yi) 9: return (ˇr, ˆr)

test point xt as yt. If it does, then the number of misclassified points from the original dataset Dc will be the the upper bound. In other words, ˆr = Pm i=1 I(fw,b(xi)̸ = yi). Theorem 3. For dataset Dc and a test point (xt, yt), r ≤ˆr.

## Algorithm

## Algorithm

1 gives a formal description of our technique discussed in previous sections. It takes as input a training dataset Dc and a test point xt with target label yt. It also assumes hyperparameter M, k, k′, l are set. It starts with computing random k partitions of Dc into D1 c,..., Dk c. Then, for each partition Dj c it computes its robustness r j by encoding the problem as a MILP using M and then using a solver to find the optimal solution. These robustness are then summed up to get ˇr. In order to computer ˆr, the algorithm starts with augmenting Dc with k′ copies of the test point and target label. This augmented data Dc is then passed to a learning algorithm along with a loss function (l). When the learning algorithm returns a classifier fw,b, ˆr is computed by calculating the number of misclassifications fw,b makes with respect to Dc. Finally, the pair (ˇr, ˆr) is returned to the user.

Implementation Details We implemented Algorithm 1 as a Python tool ROBUS- TRANGE. It uses SCIP (Bolusani et al. 2024) as the MILP solver (within Google OR-Tools v9.12) to compute lower bound robustness, and SGDClassifier from scikit-learn (Pedregosa et al. 2011) (v1.3.2) to learn a classifier from the augmented dataset. As an optimization, 10 classifiers were learned from the augmented dataset and the minimum upper bound robustness ˆr among them was chosen. The hyperparameters used had the following values: M and ϵ in the MILP encoding are set to 1000 and 10−10, resp., the number of partitions k had multiple values such as 20, 1000, 250, and 100 depending on the dataset, the number of augmented test point k′ was set to m + 1, and the loss function l used were hinge loss, log loss, and modified hueber.

## Evaluation

In this section, we present evaluation of our tool ROBUS- TRANGE on several publicly available datasets with differ- ent sizes. We first describe the datasets used.

Datasets We use datasets that represent different classification tasks where linear classifiers are used. Specifically, we use: Census Income (Kohavi 1996), Fashion-MNIST (Xiao, Rasul, and Vollgraf 2017), Pen-Based Handwritten Digits Recognition (Alpaydin and Alimoglu 1996), Letter Recognition (Slate 1991), Emo (Yang, Xu, and Yu 2023), Speech (de Gibert et al. 2018), SST (Socher et al. 2013), and Tweet (Go, Bhayani, and Huang 2009), as well as the Essays Scoring (Hamner et al. 2012) and the Loan Prediction (Surana 2021) dataset from Kaggle. For the text datasets, we use both bag-of-words (BOW) and BERT-based (BERT) representations where indicated. Multi-class classification datasets were converted to binary classification datasets by only two classes. This was done for Fashion- MNIST(Pullover vs. Shirt), Pen-Based Handwritten Digits Recognition(4 vs. 0) and Letter Recognition(D vs. O).

ROBUSTRANGE was used to compute both robustness bounds for all test points in each dataset. For datasets without predefined test-train splits (e.g., Census Income, Fashion MNIST, Letter Recognition, Pen-Based Handwritten Digits Recognition), 10% of points were randomly sampled as test data, with the remainder constituted the train data. Dataset summaries are in Table 1.

In order to evaluate ROBUSTRANGE, we address the following research questions (RQs):

RQ1: How effective is our technique in finding upper bound robustness ˆr? RQ2: How does upper bound robustness ˆr impact victim’s training process? RQ3: How does our technique for finding ˆr compare against SOTA? RQ4: How effective is our technique in finding lower bound robustness ˇr? In the remaining section, we address our research questions through experiments conducted on an 8-core CPU with 30 GB RAM running Ubuntu 20.04.

RQ1: How effective is our technique in finding upper bound robustness ˆr? Table 1 reports the average upper bound robustness ˆr (column ˆr) computed using the hinge loss function (denoted as l in Algorithm 1), while Figure 2 shows the average computation time. The average ˆr value ranged from 1% (Digits Recognition) to 31% (Loan (BOW)) of the training points. For five datasets (specifically, Census Income, Essays BOW and BERT, and Letter and Digits Recognition), ROBUS- TRANGE identified ˆr values as low as 4% (or even less) of the training points. The average time required to compute ˆr for a test point was under two minutes.

**Figure 3.** shows the ˆr histogram for the Census Income dataset, where nearly 60% of test points have robustness values around 3% of the training points. Similar results for other datasets are provided in the extended version.

Overall, ROBUSTRANGE was able to compute low ˆr values for most datasets within a short duration.

21535

<!-- Page 6 -->

## Dataset d m #xt ˆr ˆrIP r(normalized) ˆrIP r %Found ˆrIP r ρ ρIP r ˇr

## 1 Letter

Recognition 16 149 38.16 569.62 168.18 66 0.55 0.34 0.68 2 Digits Recognition 16 156 10.79 1305.88 226.54 8 0.17 0.04 0.03 3 SST (BOW) 300 872 1758.08 93.76 66.99 100 0.99 0.61 0.96 4 SST (BERT) 768 872 1141.54 439.64 247.90 97 0.97 0.52 0.00 5 Emo (BOW) 300 1558.92 237.95 167.28 99 0.99 0.52 0.00 Speech (BOW) 300 1071.90 624.09 373.20 97 0.61 0.58 0.49 7 Speech (BERT) 768 891.28 931.04 593.20 96 0.54 0.49 0.10 8 Fashion-MNIST 784 10800 1389.91 1037.25 274.13 93 0.98 0.45 0.01 9 Loan (BOW) 18 11200 3548.16 10069.39 42.22 60 0.93 0.46 111.21 10 Emo (BERT) 768 11678 2153.26 2913.84 232.23 77 0.97 0.40 560.45 11 Essays (BOW) 300 11678 495.90 2884.23 1664.89 88 0.21 0.50 0.00 12 Essays (BERT) 768 11678 350.85 3761.81 1245.04 76 0.22 0.39 0.00 13 Tweet (BOW) 300 18000 4256.26 304.15 216.32 99 1.00 0.54 7.70 14 Tweet (BERT) 768 18000 3795.24 352.38 343.72 100 0.99 0.55 0.32 15 Census Income 41 80136 2542.06 66003.10 7012.80 19 0.33 0.07 87.19

**Table 1.** Here, d, m – dimension and size of datasets, #xt– count of test points, ˆr, ˇr – avg upper and lower bound robustness from ROBUSTRANGE, ˆrIP r(normalized), ˆrIP r – avg upper bound robustness from IP-RELABEL, %Found ˆrIP r– % of robustness found by IP-RELABEL, and ρ, ρIP r– avg likelihood of getting desired classification by ROBUSTRANGE and IP-RELABEL.

1 2 3 4 5 7 8 9 10 11 12 13 14 15 Dataset

0 100 200 Time (s)

r time (s) r time (s)

rIPr time (s)

**Figure 2.** Average time taken in seconds per test point by ROBUSTRANGE (ˆr, ˇr) and IP-RELABEL (ˆrIP r).

10000 12500 15000 r

0

10

20

30

Percent of points (%)

Total training points: 80136 Total test points: 8923

Median = 2006.0

**Figure 3.** Histograms of the distribution of points across ˆr values for the Census Income dataset.

RQ2: How does upper bound robustness ˆr impact victim’s training process?

To assess the impact of ˆr on the victim’s training process, we poisoned the training dataset by perturbing the labels of the training points corresponding to ˆr. We then trained a classi- fier on the poisoned dataset and compared its accuracy with the frequency of desired classification for test points (denoted by ρ). Since we assume the victim’s training process is a black-box, we compared all pairs of loss functions.

More specifically, we assumed a loss function (l) for RO- BUSTRANGE and computed ˆr for each test point. We then created poisoned datasets by perturbing the labels of 0, ˆr

4, ˆr 2, ˆr, 2ˆr, and 4ˆr points (for 2ˆr, 4ˆr, additional random points were chosen). Each poisoned dataset was used to train a linear classifier with a loss function. We calculated the classifier’s accuracy and ρ. This process was repeated for all possible pairs of loss functions, three to compute ˆr and three for training the classifier.

**Figure 4.** shows results for the Census Income dataset: the optimal outcome for all loss functions is when the poisoned value is ˆr, as higher values sharply reduce accuracy without increasing flip likelihood. Similar trends appear in other datasets (see extended version), confirming that ˆr computed from ROBUSTRANGE is an effective poisoning measure.

RQ3: How does our technique for finding ˆr compare against SOTA?

We compare our tool against the IP-RELABEL technique (Yang, Xu, and Yu 2023). While IP-RELABEL assumes a white-box victim’s model and computes only an upper bound robustness, we include it in our comparison as it is the most closely related recent work. The average upper bound robustness computed by IP-RELABEL is presented in Table 1 (column ˆrIP r). Notably, IP-RELABEL does not guarantee an upper bound robustness for all points. In our evaluation, it was able to compute robustness for all points in only 2/15 datasets (see column %Found ˆrIP r). In contrast, ROBUSTRANGE was able to find robustness for all test points across all datasets. For a fair comparison, when IP-RELABEL failed to generate an upper bound, we assigned the size of the training dataset as the bound (column ˆrIP r(normalized)). Under this metric, ROBUSTRANGE found lower average robustness for 8 datasets.

21536

<!-- Page 7 -->

0 1 2 3 4

25 50 75 100

HingeLoss, HingeLoss Avg Robustness: 2542.1

Accuracy

0 1 2 3 4

25 50 75 100

HingeLoss, LogLoss Avg Robustness: 2542.1

Accuracy

0 1 2 3 4

25 50 75 100

HingeLoss, ModifiedHeuber

Avg Robustness: 2542.1

Accuracy

0 1 2 3 4

25 50 75 100

LogLoss, HingeLoss Avg Robustness: 2541.2

Accuracy

0 1 2 3 4

25 50 75 100

LogLoss, LogLoss Avg Robustness: 2541.2

Accuracy

0 1 2 3 4

25 50 75 100

LogLoss, ModifiedHeuber

Avg Robustness: 2541.2

Accuracy

0 1 2 3 4

25 50 75 100

ModifiedHeuber, HingeLoss

Avg Robustness: 2542.0

Accuracy

0 1 2 3 4

25 50 75 100

ModifiedHeuber, LogLoss

Avg Robustness: 2542.0

Accuracy

0 1 2 3 4

25 50 75 100

ModifiedHeuber, ModifiedHeuber

Avg Robustness: 2542.0

Accuracy

**Figure 4.** Comparison of average accuracy vs ρ for Census Income dataset with {0, ˆr

4, ˆr 2, ˆr, 2ˆr, 4ˆr} and loss functions.

Additionally, we poison the dataset using each tool’s robustness and compare the success rate of desired test classifications (columns ρ and ρIP r). In this evaluation, ROBUS- TRANGE outperforms IP-RELABEL on 12 datasets, including 6 where its average robustness is lower.

In summary, our tool assumes a realistic black-box adversary, provides tighter robustness bounds, and more reliably achieves the desired test point classification.

RQ4: How effective is our technique in finding lower bound robustness ˇr?

The average lower bound ˇr computed by ROBUSTRANGE is presented in Table 1 (column ˇr), along with the average time taken per test point in Figure 2. ROBUSTRANGE generated a non-zero average ˇr for ten datasets. The average time taken per test point was under four minutes.

While the average lower bound robustness can be low for some datasets, our tool is capable of generating high low bounds. For example, consider the histograms in Figure 5 for Census Income dataset. Although the median robustness was 0, ROBUSTRANGE was able to generate robustness values greater than 500 for 5% of the test points, and non-zero robustness for 15% of the points. Therefore, the lower bound robustness generated by our tool can still be useful for individual test points.

0 500 1000 1500 2000 2500 3000 3500 r

10 1

100

101

102

% of points (log scale)

Total training points: 80136 Total test points: 8905

Median = 0

**Figure 5.** Histograms of the distribution of points across ˇr values for the Census Income dataset.

## Conclusion and Future Work

In this paper, we have proven that the problem of finding robustness in targeted data poisoning is NP-complete in the setting considered, and have introduced effective techniques for computing lower and upper bound of robustness. An interesting future direction is to extend the lower bound algorithm for non-linear classifiers.

21537

<!-- Page 8 -->

## References

Adebayo, J.; Hall, M.; Yu, B.; and Chern, B. 2023. Quantifying and mitigating the impact of label errors on model disparity metrics. arXiv preprint arXiv:2310.02533. Alpaydin, E.; and Alimoglu, F. 1996. Pen-Based Recognition of Handwritten Digits. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5MG6K. Barreno, M.; Nelson, B.; Joseph, A. D.; and Tygar, J. D. 2010. The security of machine learning. Machine learning, 81: 121–148. Bazaraa, M. S.; Jarvis, J. J.; and Sherali, H. D. 2011. Linear programming and network flows. John Wiley & Sons. Biggio, B.; Nelson, B.; and Laskov, P. 2011. Support vector machines under adversarial label noise. In Asian conference on machine learning, 97–112. PMLR. Biggio, B.; Nelson, B.; and Laskov, P. 2012. Poisoning attacks against support vector machines. arXiv preprint arXiv:1206.6389. Bolusani, S.; Besanc¸on, M.; Bestuzheva, K.; Chmiela, A.; Dion´ısio, J.; Donkiewicz, T.; van Doornmalen, J.; Eifler, L.; Ghannam, M.; Gleixner, A.; Graczyk, C.; Halbig, K.; Hedtke, I.; Hoen, A.; Hojny, C.; van der Hulst, R.; Kamp, D.; Koch, T.; Kofler, K.; Lentz, J.; Manns, J.; Mexi, G.; M¨uhmer, E.; Pfetsch, M. E.; Schl¨osser, F.; Serrano, F.; Shinano, Y.; Turner, M.; Vigerske, S.; Weninger, D.; and Xu, L. 2024. The SCIP Optimization Suite 9.0. Technical report, Optimization Online. Chen, X.; Liu, C.; Li, B.; Lu, K.; and Song, D. 2017. Targeted backdoor attacks on deep learning systems using data poisoning. arXiv preprint arXiv:1712.05526. Chen, Y.; Ding, Z.; and Wagner, D. 2023. Continuous learning for android malware detection. In 32nd USENIX Security Symposium (USENIX Security 23), 1127–1144. Chen, Y.; Wang, S.; Qin, Y.; Liao, X.; Jana, S.; and Wagner, D. 2021. Learning security classifiers with verified global robustness properties. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, 477–494. Cin`a, A. E.; Vascon, S.; Demontis, A.; Biggio, B.; Roli, F.; and Pelillo, M. 2021. The hammer and the nut: Is bilevel optimization really needed to poison linear classifiers? In 2021 International Joint Conference on Neural Networks (IJCNN), 1–8. IEEE. de Gibert, O.; Perez, N.; Garc´ıa-Pablos, A.; and Cuadros, M. 2018. Hate Speech Dataset from a White Supremacy Forum. In Fiˇser, D.; Huang, R.; Prabhakaran, V.; Voigt, R.; Waseem, Z.; and Wernimont, J., eds., Proceedings of the 2nd Workshop on Abusive Language Online (ALW2), 11–20. Brussels, Belgium: Association for Computational Linguistics. Ferrari Dacrema, M.; Cremonesi, P.; and Jannach, D. 2019. Are we really making much progress? A worrying analysis of recent neural recommendation approaches. In Proceedings of the 13th ACM conference on recommender systems, 101–109. Gao, J.; Karbasi, A.; and Mahmoody, M. 2021. Learning and certification under instance-targeted poisoning. In Uncertainty in Artificial Intelligence, 2135–2145. PMLR.

Go, A.; Bhayani, R.; and Huang, L. 2009. Twitter sentiment classification using distant supervision. Processing, 150. Gu, T.; Liu, K.; Dolan-Gavitt, B.; and Garg, S. 2019. Badnets: Evaluating backdooring attacks on deep neural networks. Ieee Access, 7: 47230–47244. Hamner, B.; Morgan, J.; lynnvandev; Shermis, M.; and Ark, T. V. 2012. The Hewlett Foundation: Automated Essay Scoring. https://kaggle.com/competitions/asap-aes. Kaggle. Hanneke, S.; Karbasi, A.; Mahmoody, M.; Mehalel, I.; and Moran, S. 2022. On optimal learning under targeted data poisoning. Advances in Neural Information Processing Systems, 35: 30770–30782. Jia, J.; Liu, Y.; Cao, X.; and Gong, N. Z. 2022. Certified robustness of nearest neighbors against data poisoning and backdoor attacks. In Proceedings of the AAAI conference on artificial intelligence, volume 36, 9575–9583. Karp, R. M. 2009. Reducibility among combinatorial problems. In 50 Years of Integer Programming 1958-2008: from the Early Years to the State-of-the-Art, 219–241. Springer. Koh, P. W.; and Liang, P. 2017. Understanding black-box predictions via influence functions. In International conference on machine learning, 1885–1894. PMLR. Kohavi, R. 1996. Census Income. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5GP7S. Kumar, R. S. S.; Nystr¨om, M.; Lambert, J.; Marshall, A.; Goertzel, M.; Comissoneru, A.; Swann, M.; and Xia, S. 2020. Adversarial machine learning-industry perspectives. In 2020 IEEE security and privacy workshops (SPW), 69– 75. IEEE. Levine, A.; and Feizi, S. 2020. Deep partition aggregation: Provable defense against general poisoning attacks. arXiv preprint arXiv:2006.14768. Paudice, A.; Mu˜noz-Gonz´alez, L.; and Lupu, E. C. 2019. Label sanitization against label flipping poisoning attacks. In ECML PKDD 2018 Workshops: Nemesis 2018, UrbReas 2018, SoGood 2018, IWAISe 2018, and Green Data Mining 2018, Dublin, Ireland, September 10-14, 2018, Proceedings 18, 5–15. Springer. Pedregosa, F.; Varoquaux, G.; Gramfort, A.; Michel, V.; Thirion, B.; Grisel, O.; Blondel, M.; Prettenhofer, P.; Weiss, R.; Dubourg, V.; Vanderplas, J.; Passos, A.; Cournapeau, D.; Brucher, M.; Perrot, M.; and Duchesnay, E. 2011. Scikitlearn: Machine Learning in Python. Journal of Machine Learning Research, 12: 2825–2830. Rosenfeld, E.; Winston, E.; Ravikumar, P.; and Kolter, Z. 2020. Certified robustness to label-flipping attacks via randomized smoothing. In International Conference on Machine Learning, 8230–8241. PMLR. Saha, A.; Subramanya, A.; and Pirsiavash, H. 2020. Hidden trigger backdoor attacks. In Proceedings of the AAAI conference on artificial intelligence, volume 34, 11957–11965. Shafahi, A.; Huang, W. R.; Najibi, M.; Suciu, O.; Studer, C.; Dumitras, T.; and Goldstein, T. 2018. Poison frogs! targeted clean-label poisoning attacks on neural networks. Advances in neural information processing systems, 31.

21538

<!-- Page 9 -->

Slate, D. 1991. Letter Recognition. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5ZP40.

Socher, R.; Perelygin, A.; Wu, J.; Chuang, J.; Manning, C. D.; Ng, A.; and Potts, C. 2013. Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank. In Yarowsky, D.; Baldwin, T.; Korhonen, A.; Livescu, K.; and Bethard, S., eds., Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, 1631–1642. Seattle, Washington, USA: Association for Computational Linguistics.

Suciu, O.; Marginean, R.; Kaya, Y.; Daume III, H.; and Dumitras, T. 2018. When does machine learning {FAIL}? generalized transferability for evasion and poisoning attacks. In 27th USENIX Security Symposium (USENIX Security 18), 1299–1316.

Surana, S. 2021. Loan Prediction based on Customer Behavior. https://www.kaggle.com/datasets/subhamjain/loanprediction-based-on-customer-behavior. Accessed: 2025- 07-31.

S¸uvak, Z.; Anjos, M. F.; Brotcorne, L.; and Cattaruzza, D. 2022. Design of poisoning attacks on linear regression using bilevel optimization.

Suya, F.; Zhang, X.; Tian, Y.; and Evans, D. 2024. What Distributions are Robust to Indiscriminate Poisoning Attacks for Linear Learners? Advances in neural information processing systems, 36.

Tian, Z.; Cui, L.; Liang, J.; and Yu, S. 2022. A comprehensive survey on poisoning attacks and countermeasures in machine learning. ACM Computing Surveys, 55(8): 1–35.

Tramer, F.; and Boneh, D. 2020. Differentially private learning needs better features (or much more data). arXiv preprint arXiv:2011.11660.

Wang, W.; Levine, A.; and Feizi, S. 2022a. Lethal dose conjecture on data poisoning. Advances in Neural Information Processing Systems, 35: 1776–1789.

Wang, W.; Levine, A. J.; and Feizi, S. 2022b. Improved certified defenses against data poisoning with (deterministic) finite aggregation. In International Conference on Machine Learning, 22769–22783. PMLR.

Xiao, H.; Biggio, B.; Nelson, B.; Xiao, H.; Eckert, C.; and Roli, F. 2015. Support vector machines under adversarial label contamination. Neurocomputing, 160: 53–62.

Xiao, H.; Rasul, K.; and Vollgraf, R. 2017. Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms. arXiv:1708.07747.

Xiao, H.; Xiao, H.; and Eckert, C. 2012. Adversarial label flips attack on support vector machines. In ECAI 2012, 870– 875. IOS Press.

Yang, J.; Jain, S.; and Wallace, B. C. 2023. How many and which training points would need to be removed to flip this prediction? arXiv preprint arXiv:2302.02169.

Yang, J.; Xu, L.; and Yu, L. 2023. Relabeling minimal training subset to flip a prediction. arXiv preprint arXiv:2305.12809.

Zhao, M.; An, B.; Gao, W.; and Zhang, T. 2017. Efficient label contamination attacks against black-box learning models. In IJCAI, 3945–3951. Zhu, C.; Huang, W. R.; Li, H.; Taylor, G.; Studer, C.; and Goldstein, T. 2019. Transferable clean-label poisoning attacks on deep neural nets. In International conference on machine learning, 7614–7623. PMLR.

21539
