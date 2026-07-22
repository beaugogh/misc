---
title: "Learning Fair Graph Representations via Probability of Necessity and Sufficiency"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39540
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39540/43501
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Learning Fair Graph Representations via Probability of Necessity and Sufficiency

<!-- Page 1 -->

Learning Fair Graph Representations via Probability of Necessity and Sufficiency

Chuxun Liu1, Qingfeng Chen2*, Debo Cheng3, Jiangzhang Gan3†, Jiuyong Li4, Lin Liu4

## 1 Guilin University of Electronic Technology 2 Guangxi University 3 Hainan University 4 University of South

Australia chuxunliu@mails.guet.edu.cn, qingfeng@gxu.edu.cn, chengd@hainanu.edu.cn, ganjz@hainanu.edu.cn, Jiuyong.Li@unisa.edu.au, Lin.Liu@unisa.edu.au

## Abstract

Graph Neural Networks (GNNs) excel at modeling graph data but often amplify biases tied to sensitive attributes like gender and race. Existing causality-based methods use isolated interventions on graph topology or features but struggle to produce representations that balance predictive power with fairness. This leads to two issues: (1) weak predictive power, where representations miss critical task-relevant features, and (2) bias amplification, where representations encode sensitive attributes, causing unfair outcomes. To address these issues, we introduce the Probability of Necessity and Sufficiency (PNS), where necessity ensures representations capture only essential features for predictions, and sufficiency guarantees these features are adequate without relying on sensitive attributes. We propose FairSNR, a fairness-aware graph representation learning framework that introduces constraints based on the PNS. This leverages PNS to guide the learning of fair representations from graph data. In particular, FairSNR employs an encoder to learn node representations with high PNS for downstream tasks. To compute and optimize PNS, FairSNR introduces an intervenor to generate the most challenging counterfactual interventions on the representations, thereby enhancing the model’s causal stability even under worst-case scenarios. Further, a discriminator is trained to detect and mitigate sensitive information leakage in the learned representations, effectively disentangling sensitive biases from task-relevant features. Experiments on realworld graph datasets demonstrate that FairSNR outperforms existing state-of-the-art (SOTA) methods in both fairness and utility.

## Introduction

Graph Neural Networks (GNNs) have achieved remarkable success in modeling graph-structured data, driving breakthroughs in fields such as recommender systems, molecular property prediction, and bioinformatics (Ouyang et al. 2024; Li and Nabavi 2024; Lei et al. 2025). By leveraging the relational inductive biases inherent in graph data, GNNs effectively capture structural dependencies and contextual information (Job et al. 2025). However, as GNNs are increasingly deployed in high-stakes applications, growing concerns have

*Co-corresponding authors Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

emerged regarding their potential to amplify prediction biases associated with sensitive attributes (e.g., gender, race, or socioeconomic status) (Dai et al. 2024). Such biases can lead to unfair or even discriminatory outcomes, particularly in decision-critical contexts such as credit scoring (Trinh and Zhang 2024) and risk assessment (Li et al. 2025a).

Recently, fairness-aware graph representation learning has garnered significant research interest. With the growing adoption of GNNs, numerous methods have been proposed to improve fairness while preserving acceptable utility performance (Luo et al. 2025; Yang et al. 2024; Zhu et al. 2024b). Among these, causal inference has emerged as a theoretically grounded approach for fairness learning, aiming to fundamentally disentangle the influence of sensitive attributes. Causal methods mitigate spurious correlations and enable counterfactual reasoning by explicitly modeling the causal paths between sensitive attributes and prediction outcomes, thus offering a principled perspective on fairness. Typical strategies include edge pruning, feature masking, and counterfactual augmentation, which primarily reduce bias propagation through interventions on graph structures or node features (Li et al. 2024; Guo et al. 2023).

Existing fairness-aware GNN methods can be broadly classified into three categories (Dong et al. 2023). Structural intervention methods, such as FairDrop (Spinelli et al. 2021) and FairWalk (Rahman et al. 2019), aim to reduce bias propagation by adjusting edge retention probabilities or modifying path sampling strategies. Adversarial learning methods, such as FairGNN (Dai and Wang 2021) and FairVGNN (Wang et al. 2022), incorporate adversarial modules to explicitly disentangle sensitive attributes from the learned embeddings. Causal inference-based methods, such as NIFTY (Agarwal, Lakkaraju, and Zitnik 2021) and Fair- INV (Zhu et al. 2024a), attempt to model the causal effect of sensitive attributes on prediction outcomes, thereby mitigating discrimination through counterfactual reasoning or causal adjustment.

Current approaches however suffer from two critical limitations. Firstly, most methods rely on isolated interventions, such as modifying graph topology or balancing input features, which may lack semantic consistency and generalizability (Li et al. 2024). Secondly, and more fundamentally, these methods often overlook the necessity and sufficiency

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

23667

<!-- Page 2 -->

conditions of the learned representations, which are two crucial criteria for ensuring fair and robust prediction (Yang et al. 2023). Especially, a representation that is necessary but not sufficient may fail to provide predictive power, while one that is sufficient but not necessary may encode spurious dependencies with sensitive attributes, ultimately undermining fairness and generalizability.

To address these limitations, we propose FairSNR, a novel fairness-aware graph representation learning framework grounded in the causal principles of necessity and sufficiency. Our key insight is to treat fairness not merely as a post-hoc constraint or intervention, but as an intrinsic property of the learned fair representation. In practice, FairSNR employs PNS as a theoretical tool to regularize the representation learning process (Pearl 2009). By maximizing PNS with respect to the prediction task while minimizing its dependency on sensitive attributes, we ensure that the learned representation is both sufficiently informative for prediction and necessarily invariant to sensitive factors. In conjunction with adversarial learning, which decouples sensitive information from the learned representations, our framework effectively separates bias-inducing features from task-relevant information, thereby enhancing both fairness and utility in downstream tasks. The main contributions of this work are summarized as follows:

• We introduce the causal concept of PNS into the field of fair graph representation learning, where achieving fairness requires satisfying both sufficiency with respect to the prediction task and necessity invariance with respect to sensitive attributes. To the best of our knowledge, this is the first work in fairness that leverages causal PNS. • We develop FairSNR, a novel fairness-aware graph representation learning model that explicitly incorporates PNS as a core regularization term. FairSNR maximizes the causal relevance of representations for the prediction task while minimizing their sensitivity to protected attributes via adversarial learning. • Extensive empirical evaluations on multiple real-world benchmark datasets demonstrate that FairSNR consistently outperforms existing SOTA across a range of fairness and predictive performance metrics.

## Preliminaries

In this section, we first introduce the notations used in this work, followed by the definition of PNS and the associated theoretical foundations.

Notations

Let G = (V, A, X) denote an unweighted, undirected graph, where V = {v1, v2,..., vn} is the set of n = |V| nodes. The graph structure is represented by a symmetric adjacency matrix A ∈{0, 1}n×n, where Aij = 1 if there is an edge between nodes vi and vj, and Aij = 0 otherwise. Each node vi is associated with a feature vector xi ∈Rd, and we denote the node feature matrix as X = [x1, x2,..., xn] ∈Rn×d.

In fairness-aware settings, each node vi is associated with a sensitive attribute si ∈S (e.g., gender, race) and a ground truth label yi ∈Y, where S and Y denote the sets of possible sensitive attribute values and label categories, respectively. The downstream task considered in this work is node classification. The target label is denoted as y ∈{0, 1}, and the sensitive attribute is denoted as s ∈{0, 1}.

Definition of PNS on Graph-structured Data

We extend the concept of the PNS (Pearl 2009) to graphstructured data.

Definition 1 (Probability of Necessary and Sufficient) Given a node v in the graph G with label y, the probability of a necessary and sufficient cause of a learned representation c for y is defined as:

PNS(c, ¯c):= P

Ydo(C=c) = y

C = ¯c,

Y̸ = y

· P(C = ¯c, Y̸ = y)

+ P

Ydo(C=¯c)̸ = y

C = c,

Y = y

· P(C = c, Y = y).

(1)

Here, C and Y denote the cause (i.e., representation) and effect (i.e., label) of node v, respectively, where Y = y represents the observed true label. c and ¯c refer to two different states of C. The operator do(·) signifies an intervention, simulating an external manipulation of the causal mechanism (Pearl 2009). In the above definition, P

Ydo(C=c) = y

C = ¯c, Y̸ = y represents the probability that the outcome Y would occur if we intervened to set the cause C to c, given that we actually observed C = ¯c and Y̸ = y.

In this context, the first term in the PNS formula corresponds to the probability of sufficiency, and the second term represents the probability of necessity. A higher value of PNS indicates that the variable C is more likely to be a necessary and sufficient cause of Y.

Computing such counterfactual-based probabilities in real-world systems, however, is often challenging or even infeasible due to the need for knowledge of the underlying structural causal model. Fortunately, PNS, although originally defined through counterfactual distributions, becomes identifiable from purely observational data under certain conditions, particularly when the assumptions of exogeneity (no unmeasured confounding) and monotonicity (no prevention) are satisfied (Tian and Pearl 2000; Pearl 2009).

Definition 2 (Exogeneity (Pearl 2009)) A variable C is said to be exogenous with respect to Y if its interventional probability can be identified by the corresponding conditional probability.

In the context of the graph domain, the node representation C is said to be exogenous with respect to its label Y in both the source graph domain Gs and the target graph domain Gt if and only if the following conditions hold:

PGs

Ydo(C=c) = y

= PGs(Y = y | C = c),

PGt

Ydo(C=c) = y

= PGt(Y = y | C = c). (2)

23668

<!-- Page 3 -->

Eq. 2 implies that, when C is exogenous to Y, the discrepancy between the interventional and observational (i.e., conditional) distributions disappears. In other words, observing C = c provides the same information about Y as actively intervening to set C = c, indicating the absence of confounding between the two variables.

Definition 3 (Monotonicity (Tian and Pearl 2000)) The variable Y is said to be monotonic with respect to C if, for two possible states c and ¯c of C, one of the following conditions holds:

(

P

Ydo(C=c) = y, Ydo(C=¯c)̸ = y

= 0, or

P

Ydo(C=c)̸ = y, Ydo(C=¯c) = y

= 0 (3)

This definition ensures that C has a monotonic causal effect on Y, meaning that changing C from one state to another does not simultaneously increase and decrease the likelihood of the outcome Y.

Lemma 1 ((Pearl 2009)) If C is exogenous to Y and Y is monotonic with respect to C, then the PNS can be computed as:

PNS(c, ¯c) = PGt(Y = y | C = c) | {z } sufficiency −PGt(Y = y | C = ¯c) | {z } necessity

. (4)

According to Lemma 1, the computation of PNS becomes feasible using observational data under the joint assumptions of exogeneity and monotonicity. The original proof was presented by (Pearl 2009), further extended through probabilistic reasoning by (Yang et al. 2023), and subsequently generalized to subgraph learning by (Chen et al. 2025).

## Methodology

This section presents the methodology of the proposed FairSNR framework.

Causal Analysis Recent research has increasingly incorporated causal modeling into fairness studies to uncover intrinsic biases associated with sensitive attributes (Li et al. 2024; Agarwal, Lakkaraju, and Zitnik 2021). In this work, we propose a novel causal perspective that unifies the graph data generation process and the GNN prediction mechanism within a Structural Causal Model (SCM) (Pearl 2009), as illustrated in Figure 1.

• S →X →C →Y and S →A →C →Y: Achieving fairness in GNNs presents a unique challenge compared to other data modalities like images or text. Unlike conventional models, GNNs make predictions based on a node’s entire contextual subgraph, allowing the sensitive attribute S to influence the prediction Y through two critical causal pathways. S →X →C →Y: This pathway captures how the sensitive attribute S influences a node’s initial features X. GNNs encoder then processes these biased features into its representation C, which ultimately leads to a discriminatory outcome Y. The causal

S

X A

C

Y

**Figure 1.** The SCM illustrates the GNNs prediction process. Fairness issues in graph learning can arise through three causal pathways: S →X →C →Y, S →A →C →Y, and S →C →Y. The FairSNR framework mitigates these issues by simultaneously blocking all three pathways that transmit sensitive information S to the prediction target Y.

pathway S →A →C →Y illustrates how sensitive attributes S influence the prediction outcome Y through the graph topology A and node representations C. More precisely, S affects A by inducing structural bias. for example, social homophily may lead to stronger connectivity between nodes with similar attributes. The messagepassing mechanism of GNNs then aggregates information based on this biased adjacency matrix A, encoding the structural bias into the learned node representations C, which ultimately propagates to the prediction Y.

• S ↔C →Y: This causal pathway represents the direct influence of the sensitive attribute S on the node representation C, which in turn affects the prediction outcome Y. To mitigate this bias, we employ adversarial decorrelation to explicitly weaken sensitive information from the learned representations. Specifically, an adversarial loss is introduced to discourage the model from encoding any predictive signal of S in C. This weakens the dependency between between S and C, effectively blocking the causal link and ensuring that the final prediction Y is made based on fair and unbiased representations.

In summary, discriminatory decisions in GNNs arise from the three causal pathways discussed above. To eliminate the influence of the sensitive attribute S on the prediction Y through the paths S →X →C →Y and S →A → C →Y, we propose FairSNR, which learns a representation C that is both sufficient and necessary, while also being independent of S. Sufficiency ensures that C contains all information in X and A that is relevant for predicting Y, making Y conditionally independent of X and A given C. Necessity guarantees that C retains only the essential causal factors of Y, excluding redundant information. Furthermore, by enforcing C ⊥S, FairSNR explicitly removes the dependence of C on S, thereby blocking the causal influence of S on Y via X or A. This severs the unfair pathways and fundamentally eliminates bias arising from sensitive attributes.

23669

<!-- Page 4 -->

GNNS Backbone

…

Intervener ξ

…

+

…

…

Classifier

Discriminator

…

Classifier

Sufficiency

Monotonicity

MSE

Intervention variable Z

Intervention representation Generate the intervention representation

Graph

**Figure 2.** Overview of the FairSNR framework. The GNN backbone fg extracts node representations C from the input graph. The Intervener ξ generates an intervention variable Z, which is used to construct the counterfactual representation ¯C = C + Z. The classifier fc ensures sufficiency by predicting the label ˆY, while the discriminator Dθ mitigates sensitive attribute leakage by minimizing the dependence on sensitive information S. Monotonicity is enforced by minimizing the mean squared error (MSE) between the original prediction ˆY and the intercention-based prediction ¯Y.

GNNs in FairSNR GNNs leverage a message-passing framework, enabling each node to iteratively aggregate information from its neighbors to refine its latent representations. At the k-th layer, a node vi aggregates information from its neighborhood N(i) and updates its representation accordingly. This process is typically formulated as:

H(k) = σ

˜A H(k−1) W(k−1)

, (5)

where H(k) is the node embedding matrix at layer k (with H(0) = X), ˜A is a normalized or modified adjacency matrix (e.g., ˜A = ˜D−1/2 ˜A ˜D−1/2), W(k−1) is a learnable weight matrix, and σ(·) is a non-linear activation function.

For node classification tasks, a GNN model f typically consists of a GNN-based encoder fg and a task-specific classifier fc. The fg maps the input graph structure and node features to a low-dimensional representation:

C = fg(A, X), C ∈Rn×d′ (6) where d′ is the embedding dimension. The classifier in FairSNR then predicts labels based on this learned representation:

ˆY = fc(C). (7)

Necessary and Sufficient Graph Representation As illustrated in the Figure 2, our objective is to learn a node representation C that is both necessary and sufficient for predicting the node’s label y, while remaining independent of the node’s sensitive attribute S.

We generalize the PNS risk proposed in (Yang et al. 2023) to the graph setting at the node level. For a node v with label y, the PNS risk is designed to evaluate the necessity and sufficiency of the representation C learned by the GNN encoder fg. We define the empirical PNS risk on the graph as

ˆRt(fc, fg, ξ):

ˆRt(fc, fg, ξ):= E(v,y)∼TG h

I [sign(fc(c))̸ = y] +

E¯c∼Pt(¯C|x,A)I [sign(fc(¯c)) = y]

i

,

(8)

where TG denotes the empirical distribution of node-label pairs on the graph, x represents the input features of node v, and A is the adjacency matrix encoding the graph structure. C ∼Pt(C | x, A) denotes a sufficient representation sampled from the learned distribution, while ¯C ∼Pt(¯C | x, A) denotes a necessary representation obtained via intervention. The indicator function I[·] evaluates the correctness of the prediction.

Directly optimizing the PNS risk is intractable. Following the approach in (Yang et al. 2023), we instead decompose the risk and employ a more tractable upper bound, which consists of the sufficiency risk and a monotonicity measurement. The empirical sufficiency risk ˆ SF s corresponds directly to the classification error in the node classification task. It is defined as:

ˆ SF s(fc, fg):= 1

|V|

X v∈V

Ecv∼ˆ P fg (C|v,G)

I [sign(fc(cv))̸ = y],

(9)

where cv is a representation sampled from the encoderinduced distribution ˆP fg(C | v, G), and y is the groundtruth label of node v. The indicator function I[·] returns 1 if the predicted label sign(fc(c)) differs from the true label y, and 0 otherwise.

The empirical monotonicity measurement ˆ M s evaluates the consistency between the predictions made on the original representation c and the intervention-based representation ¯c:

ˆ M s(fc, fg, ξ):= 1

|V|

X v∈V

Ec∼ˆ P fg, ¯c∼ˆ P ξ

I[sign(fc(c)) = sign(fc(¯c))].

(10)

23670

<!-- Page 5 -->

Based on Eqs. 9 and 10, the empirical PNS risk is upper bounded by the combination of monotonicity measurement and sufficiency risk:

ˆRs ≤ˆ M s(fc, fg, ξ) + 2 · ˆ SF s(fc, fg). (11)

Therefore, our optimization objective is to minimize this upper bound, encouraging the learned representation to be both necessary and sufficient for prediction while maintaining a monotonic behavior under intervention.

To learn a representation C that is both necessary and sufficient for the downstream task while remaining unbiased, we formulate the learning process as a min-max optimization problem. Simultaneously, we incorporate an adversarial loss to mitigate the influence of the sensitive attribute S.

The overall optimization objective is defined as:

min fg,fc max ξ LPNS(fc, fg, ξ) + λk · LKL(fg, ξ)

+λd · Ld(fg, θ).

(12)

The three losses are the PNS loss (LPNS), the KLdivergence regularization (LKL), and the disentanglement loss (Ld). where LPNS encourages the learned representations C to be sufficient for the task and necessary under interventions; Ld aims to disentangle the sensitive attribute S from the representation C through adversarial learning; λk and λd are non-negative hyperparameters that balance the contributions of the KL regularization and adversarial loss, respectively.

Our objective is to minimize the upper bound of the PNS risk while incorporating a semantic separability constraint to ensure that the representation c and the intervention-based representation ¯c remain at least a distance δ apart. Formally, the loss LPNS(fg, fc, ξ) is defined as:

min fg,fc max ξ

ˆ M s(fc, fg, ξ) + ˆ SF s(fc, fg), s.t. ∥c −¯c∥2 > δ.

(13)

where the constraint ∥c −¯c∥2 > δ is imposed based on the Semantic Separability assumption to ensure sufficient perturbation between the original and intervention-based representations. The term LKL serves as a regularizer for the representation distributions, ensuring that the empirical risk approximates the expected risk effectively:

LKL(fg, ξ) = Ev∈V h

KL

ˆP fg(C | X, A) ∥πC

+ KL

ˆP ξ(¯C | X, A) ∥π ¯C i

,

(14)

where πC and π¯C are predefined prior distributions, typically chosen as standard Gaussian distributions.

To remove the influence of the sensitive attribute S, we introduce an adversarial loss. A discriminator Dθ is trained to predict the sensitive attribute S from the representation c, while the GNN encoder fg aims to generate representations that prevent Dθ from correctly identifying S, i.e., effectively minimizing the dependency between C and S.

Ld(fg, θ) = Ev∈V [log Dθ (S | C = fg(X, A))]. (15)

## Algorithm

1: Training Algorithm of FairSNR

1: Input: Graph G = (V, A, X), sensitive attribute S; hyperparameters α, β, T. 2: Output: Trained encoder fg, classifier fc, and intervenor ξ 3: Initialize fg, fc, ξ, variational encoder fmv, discriminator D 4: Set optimizers for all modules accordingly 5: for t = 1 to T do 6: Reset parameters of all modules 7: for i = 1 to |Vtrain| do 8: // Step A: Train Discriminator D 9: Freeze fg; compute C ←fg(X, A) 10: ˆS ←D(C) 11: Ld ←Calculate loss function according to Eq 15 12: Update D by gradient descent 13: // Step B: Update fg, fc, fmv, ξ 14: Enable training for fg, fc, fmv, ξ 15: C ←fg(X, E), (µ, σ) ←fmv(X, A) 16: ˆS ←D(GRL(C)) 17: Ld ←Calculate loss function according to Eq 15 18: Z ←ξ(C), ¯C ←C + Z 19: ˆY, Y ←fc(C), fc(¯C) 20: LP NS ←Calculate loss function according to Eq 13 21: LKL ←Calculate loss function according to Eq 14 22: L ←LP NS + αLKL + βLd 23: Update fg, fc, fmv by gradient descent 24: end for 25: end for 26: return fg, fc, ξ

In practice, the discriminator Dθ is trained by minimizing Ld, while the encoder fg maximizes it using a Gradient Reversal Layer (GRL) (Ganin et al. 2016).

Through this adversarial training process, the encoder fg is guided to learn a representation C that not only enables accurate prediction of y by minimizing the sufficiency risk ˆ SF s, but also satisfies the causal constraints of necessity and sufficiency by minimizing the monotonicity measurement ˆ M s. Simultaneously, it obfuscates sensitive information by maximizing the adversarial loss Ld, effectively fooling the sensitive attribute discriminator. In this way, FairSNR achieves the goal of learning a graph representation that is sufficient, necessary, and fair.

## Experiments

In this section, we conduct comprehensive experiments to examine the performance of the proposed FairSNR approach, following the experimental protocol established in (Li et al. 2024; Yang et al. 2024). Both fairness and utility metrics are considered across multiple datasets. Our experiments are designed to address the following research questions (RQs):

RQ1: Can FairSNR outperform existing baseline methods in terms of both utility and fairness? RQ2: Do necessary

23671

<!-- Page 6 -->

Dataset Metric Vanilla GCN EDITS NIFTY FairGNN FairVGNN FairINV FairGB Fprompt FairSNR

German

AUC (↑) 73.49±2.15 69.41±2.33 68.78±2.69 67.35±2.13 72.12±1.10 69.18±1.62 59.77±7.59 70.25±1.53 66.17±0.59 F1 (↑) 80.76±2.35 81.55±0.59 81.40±0.50 82.01±0.26 82.14±0.42 82.25±0.42 82.46±0.23 81.31±1.33 82.38±0.09 DP (↓) 33.75±12.34 4.25±3.28 5.73±5.25 3.49±2.15 1.71±1.68 1.15±1.32 1.68±3.30 2.39±1.65 0.64±0.85 EO (↓) 25.73±8.36 3.87±2.23 5.08±4.29 3.40±2.15 1.21±2.11 0.90±1.81 1.08±1.80 2.41±1.83 0.36±0.71

Credit

AUC (↑) 73.80±0.23 73.01±0.11 71.96±0.19 71.95±1.43 67.34±0.45 69.76±3.24 72.02±1.53 70.21±1.33 68.34±5.84 F1 (↑) 82.63±0.21 81.81±0.28 81.72±0.05 81.84±1.19 81.08±0.74 80.42±2.64 85.43±3.34 80.35±1.92 85.78±2.44 DP (↓) 12.53±0.25 10.90±1.22 11.68±0.07 12.64±2.11 5.02±5.22 6.05±4.37 2.30±3.00 4.22±1.65 1.71±1.72 EO (↓) 10.63±0.02 8.75±1.21 9.39±0.07 10.41±2.03 3.60±4.31 4.00±3.87 1.75±2.07 3.45±2.19 0.73±0.67

Pokec-z

AUC (↑) 75.42±0.33 OOM 71.59±0.17 76.12±0.12 76.02±0.16 75.79±0.08 OOM 76.03±1.77 76.15±0.68 F1 (↑) 70.32±0.20 OOM 67.13±1.66 69.75±2.65 70.45±0.57 70.78±0.50 OOM 70.89±0.53 71.17±0.54 DP (↓) 7.02±1.38 OOM 3.06±1.85 2.73±2.23 2.90±0.77 2.70±0.96 OOM 1.47±0.54 0.93±0.46 EO (↓) 7.60±1.24 OOM 3.86±1.65 2.17±1.85 3.09±0.97 2.23±0.66 OOM 1.38±0.68 0.98±0.94

Pokec-n

AUC (↑) 74.87±0.18 OOM 69.23±0.56 73.49±0.28 73.73±0.92 73.55±0.16 OOM 75.83±1.32 77.27±0.50 F1 (↑) 65.35±0.54 OOM 61.75±1.05 64.80±0.89 63.35±1.64 65.19±0.62 OOM 67.39±0.52 68.27±0.96 DP (↓) 7.17±1.46 OOM 6.96±1.80 2.26±1.19 4.28±1.33 1.24±0.64 OOM 1.23±1.09 1.12±1.25 EO (↓) 5.66±0.43 OOM 7.75±1.43 3.21±2.28 5.34±1.27 2.80±0.78 OOM 1.03±1.29 1.69±1.97

**Table 1.** Model performance on the German, Credit, Pokec-z, and Pokec-n datasets in terms of utility and fairness. Bold indicates the best results for each metric, while underline denotes the runner-up results. Arrows (↑/↓) indicate whether higher or lower values are preferable. Each result is averaged over five independent runs. All models use GCN as the backbone encoder.

and sufficient representations enhance model performance? RQ3: How do hyperparameters influence the performance of FairSNR?

Datasets and Implementation Details We evaluate our FairSNR on four widely used realworld datasets: German (Asuncion and Newman 2007), Credit (Yeh and Lien 2009), as well as two variants of the Pokec dataset, Pokec n and Pokec z (Takac and Zabovsky 2012). The key statistics of these datasets are summarized in the appendix.

Baselines We compared the performance of FairSNR with seven baseline methods across three backbone architectures. FairGNN (Dai and Wang 2021), EDITS (Dong et al. 2022), NIFTY (Agarwal, Lakkaraju, and Zitnik 2021), FairVGNN (Wang et al. 2022), FairINV (Zhu et al. 2024a), FairGB (Li et al. 2024), FPrompt (Li et al. 2025b). The details of the baselines can be found in the appendix.

## Evaluation

Metrics To evaluate the performance of the downstream classification task, we adopt AUC and F1 score as the primary utility metrics. These measures provide a comprehensive view of model effectiveness, particularly in imbalanced classification scenarios. For fairness evaluation, we employ two widely used group fairness criteria: Demographic Parity (DP) (Dwork et al. 2012) and Equal Opportunity (EO) (Hardt, Price, and Srebro 2016)

GNN Backbones In our experimental setup, we utilize three popular GNN models as the foundation of our encoder: GCN (Kipf and Welling 2017), GIN(Xu et al. 2019), and Graph- SAGE (Hamilton, Ying, and Leskovec 2017). These architectures are broadly recognized in the research community and have shown robust effectiveness across a range of graphbased learning tasks. The details of the GIN and Graph- SAGE baseline can be found in the appendix.

Comparison Results (RQ1)

We conduct a comprehensive comparison between our proposed FairSNR model and several state-of-the-art fair GNN methods on four publicly available benchmark datasets. As shown in Table 1, across all four datasets, FairSNR consistently achieves the lowest fairness disparities. For instance, on the German dataset, FairSNR reduces the DP and EO by 44.35% and 60%, respectively, compared to the bestperforming baseline method in terms of fairness. We attribute this performance gain to the core idea of our model, which is to learn graph representations that are both necessary and sufficient. This learning paradigm explicitly encourages the model to identify and retain only those features that have a direct causal relationship with the prediction task while actively discarding all spurious correlations. In fairness-sensitive scenarios, the influence of sensitive attributes on prediction outcomes is often mediated through spurious correlations. By discovering “necessary” representations, FairSNR fundamentally severs this connection, thereby producing predictions that are invariant to sensitive attributes and inherently fair.

On larger and structurally more complex datasets such as Pokec-z and Pokec-n, FairSNR not only leads in fairness metrics but also consistently outperforms all baseline models in predictive utility (AUC and F1). For instance, on the Pokec-n dataset, FairSNR achieves a relative improvement of approximately 1.90% in AUC and 1.31% in F1 score compared to the best-performing baseline. This result indicates that, as the graph structure becomes more complex, models that indiscriminately learn all correlations may become entangled in a multitude of spurious associations. In contrast, FairSNR leverages its causality-aware learning objective to more precisely extract true predictive signals, thus

23672

<!-- Page 7 -->

AUC (Pokec-z) ΔDP (Pokec-z) AUC (Credit) ΔDP (Credit)

**Figure 3.** Hyper-parameter analysis on Pokec-z and Credit.

**Figure 4.** Ablation study of FairSNR showing the trade-off between F1 score and DP.

minimizing overfitting to noise and bias. On relatively small datasets, FairSNR achieves slightly lower AUC scores than some baselines. This can be attributed to the trade-off between accuracy and fairness, as the model strictly enforces the necessity constraint. In such datasets, features correlated with sensitive attributes may also be strongly linked to the target label, despite lacking genuine causal relevance.

Ablation Study (RQ2)

To answer the research question RQ2 and evaluate the effectiveness of our proposed FairSNR, we construct two ablated variants of the model. w/o D denotes the version without the discriminator, while w/o SN refers to the version without the necessity and sufficiency constraints. We observe that both variants perform worse than the complete FairSNR model in balancing utility and fairness, which demonstrates the effectiveness of each individual component and the soundness of their integration. The details of the ablation study can be found in the appendix. In the w/o SN setting, although adversarial learning can partially mitigate bias, it leads to a noticeable drop in predictive performance. On the other hand, the w/o D variant generally achieves better fairness than w/o SN, but still falls short of the full FairSNR. This indicates that learning necessary and sufficient representations serves as an effective fairness intervention. It weakens major spurious correlation pathways while retaining essential predictive information, thus laying a strong foundation for achieving both fairness and utility, as shown in Figure 4. Although the two components may exhibit varying strengths across different tasks, we observe that FairSNR consistently benefits from their complementary effects, demonstrating a synergistic gain when the two modules are combined.

Hyper-parameter Analysis (RQ3) In this study, we investigate the impact of two key hyperparameters in FairSNR on model performance and fairness: the KL regularization strength α and the adversarial learning strength β. More precisely, α controls the alignment between the representation space and the prior distribution, thereby affecting the degree of compression and generalization of the learned representations. In contrast, β determines the extent to which sensitive attribute information is suppressed during training. To systematically assess the effects of these two hyperparameters, we conduct a grid search on the Credit and Pokec-z datasets with α ∈{0.0001, 0.0005, 0.001, 0.005, 0.01} and β ∈ {0.001, 0.005, 0.01, 0.05, 0.1}. The results are summarized in Figures 3. Overall, a too-small α fails to adequately regularize the representation space, while an excessively large α suppresses the expressiveness needed for accurate prediction. Meanwhile, a moderate adversarial strength (e.g., β = 0.01) effectively disrupts the influence paths of sensitive attributes, thereby enhancing fairness. Based on these findings, we adopt α = 0.001 and β = 0.01 as default settings in all subsequent experiments to ensure a good tradeoff between utility and fairness.

## Conclusion

In this paper, we propose a novel approach, FairSNR, to address the problem of unfairness in GNN representation learning. FairSNR consists of two synergistic modules that jointly learn necessary and sufficient fair representations in graphs. Guided by principles from causal theory, FairSNR mitigates bias by enforcing both necessity and sufficiency constraints on node representations. Additionally, it incorporates adversarial disentanglement to eliminate residual sensitive attribute information embedded in the learned representations. Experimental results on four real-world benchmark datasets demonstrate that FairSNR achieves SOTA performance in balancing predictive utility and group fairness. In future work, greater attention could be devoted to the fundamental challenge of fair representation learning, with particular emphasis on leveraging graph structural properties to design more effective bias mitigation strategies.

23673

<!-- Page 8 -->

## Acknowledgements

This work was partially supported by the Specific Research Project of Guangxi for Research Bases and Talents(GuiKe AD24010011) and the Key Research & Development Program Project of Guangxi (GuiKe AB25069095). We also wish to acknowledge the support from the Australian Research Council (under grant DP230101122).

## References

Agarwal, C.; Lakkaraju, H.; and Zitnik, M. 2021. Towards a unified framework for fair and stable graph representation learning. In Uncertainty in artificial intelligence, 2114– 2124. PMLR. Asuncion, A.; and Newman, D. 2007. UCI machine learning repository. Chen, X.; Cai, R.; Zheng, K.; Jiang, Z.; Huang, Z.; Hao, Z.; and Li, Z. 2025. Unifying invariant and variant features for graph out-of-distribution via probability of necessity and sufficiency. Neural Networks, 107044. Dai, E.; and Wang, S. 2021. Say no to the discrimination: Learning fair graph neural networks with limited sensitive attribute information. In Proceedings of the 14th ACM international conference on web search and data mining, 680– 688. Dai, E.; Zhao, T.; Zhu, H.; Xu, J.; Guo, Z.; Liu, H.; Tang, J.; and Wang, S. 2024. A comprehensive survey on trustworthy graph neural networks: Privacy, robustness, fairness, and explainability. Machine Intelligence Research, 1011–1061. Dong, Y.; Liu, N.; Jalaian, B.; and Li, J. 2022. Edits: Modeling and mitigating data bias for graph neural networks. In Proceedings of the ACM web conference, 1259–1269. Dong, Y.; Ma, J.; Wang, S.; Chen, C.; and Li, J. 2023. Fairness in graph mining: A survey. IEEE Transactions on Knowledge and Data Engineering, (10): 10583–10602. Dwork, C.; Hardt, M.; Pitassi, T.; et al. 2012. Fairness through awareness. In Proceedings of the 3rd innovations in theoretical computer science conference, 214–226. Ganin, Y.; Ustinova, E.; Ajakan, H.; Germain, P.; Larochelle, H.; Laviolette, F.; March, M.; and Lempitsky, V. 2016. Domain-adversarial training of neural networks. Journal of machine learning research, (59): 1–35. Guo, Z.; Li, J.; Xiao, T.; Ma, Y.; and Wang, S. 2023. Towards fair graph neural networks via graph counterfactual. In Proceedings of the 32nd ACM international conference on information and knowledge management, 669–678. Hamilton, W.; Ying, Z.; and Leskovec, J. 2017. Inductive representation learning on large graphs. Advances in neural information processing systems. Hardt, M.; Price, E.; and Srebro, N. 2016. Equality of opportunity in supervised learning. Advances in neural information processing systems. Job, S.; Tao, X.; Cai, T.; Li, L.; Xie, H.; Xu, C.; and Yong, J. 2025. HebCGNN: Hebbian-enabled causal classification integrating dynamic impact valuing. Knowledge-Based Systems, 113094.

Kipf, T. N.; and Welling, M. 2017. Semi-Supervised Classification with Graph Convolutional Networks. In 5th International Conference on Learning Representations, ICLR, Toulon, France, April 24-26. Lei, S.; Chang, X.; Yu, Z.; He, D.; Huo, C.; Wang, J.; and Jin, D. 2025. Feature-Structure Adaptive Completion Graph Neural Network for Cold-start Recommendation. In Proceedings of the AAAI Conference on Artificial Intelligence, 12022–12030. Li, B.; and Nabavi, S. 2024. A multimodal graph neural network framework for cancer molecular subtype classification. BMC bioinformatics, 25(1): 27. Li, X.; Li, W.; Yu, X.; Han, Z.; and Jin, Q. 2025a. Financial risk assessment of imbalanced data based on nonlinear causal time-series network. Information Processing & Management, 62(3): 104025. Li, Z.; Dong, Y.; Liu, Q.; and Yu, J. X. 2024. Rethinking fair graph neural networks from re-balancing. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 1736–1745. Li, Z.; Lin, M.; Wang, J.; and Wang, S. 2025b. Fairnessaware prompt tuning for graph neural networks. In Proceedings of the ACM on Web Conference 2025, 3586–3597. Luo, R.; Huang, H.; Lee, I.; Xu, C.; Qi, J.; and Xia, F. 2025. Fairgp: A scalable and fair graph transformer using graph partitioning. In Proceedings of the AAAI Conference on Artificial Intelligence, 12319–12327. Ouyang, Z.; Zhang, C.; Hou, S.; Zhang, C.; and Ye, Y. 2024. How to improve representation alignment and uniformity in graph-based collaborative filtering? In Proceedings of the International AAAI Conference on Web and Social Media, 1148–1159. Pearl, J. 2009. Causality. Cambridge university press. Rahman, T. A.; Surma, B.; Backes, M.; and Zhang, Y. 2019. Fairwalk: Towards Fair Graph Embedding. In Kraus, S., ed., Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI, Macao, China, August 10-16, 3289–3295. Spinelli, I.; Scardapane, S.; Hussain, A.; and Uncini, A. 2021. Fairdrop: Biased edge dropout for enhancing fairness in graph representation learning. IEEE Transactions on Artificial Intelligence, (3): 344–354. Takac, L.; and Zabovsky, M. 2012. Data analysis in public social networks. In International scientific conference and international workshop present day trends of innovations, 6. Tian, J.; and Pearl, J. 2000. Probabilities of causation: Bounds and identification. Annals of Mathematics and Artificial Intelligence, 28(1): 287–313. Trinh, T. K.; and Zhang, D. 2024. Algorithmic Fairness in Financial Decision-Making: Detection and Mitigation of Bias in Credit Scoring Applications. Journal of Advanced Computing Systems, 36–49. Wang, Y.; Zhao, Y.; Dong, Y.; Chen, H.; Li, J.; and Derr, T. 2022. Improving fairness in graph neural networks via mitigating sensitive attribute leakage. In Proceedings of the 28th ACM SIGKDD conference on knowledge discovery and data mining, 1938–1948.

23674

<!-- Page 9 -->

Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2019. How Powerful are Graph Neural Networks? In 7th International Conference on Learning Representations, ICLR New Orleans, LA, USA, May 6-9,. Yang, C.; Liu, J.; Yan, Y.; and Shi, C. 2024. Fairsin: Achieving fairness in graph neural networks through sensitive information neutralization. In Proceedings of the AAAI Conference on Artificial Intelligence, 9241–9249. Yang, M.; Fang, Z.; Zhang, Y.; Du, Y.; Liu, F.; Ton, J.-F.; Wang, J.; and Wang, J. 2023. Invariant learning via probability of sufficient and necessary causes. Advances in Neural Information Processing Systems, 79832–79857. Yeh, I.-C.; and Lien, C.-h. 2009. The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. Expert systems with applications, (2): 2473–2480. Zhu, Y.; Li, J.; Bian, Y.; Zheng, Z.; and Chen, L. 2024a. One Fits All: Learning Fair Graph Neural Networks for Various Sensitive Attributes. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 4688–4699. Zhu, Y.; Li, J.; Zheng, Z.; and Chen, L. 2024b. Fair Graph Representation Learning via Sensitive Attribute Disentanglement. In Proceedings of the ACM Web Conference 2024, 1182–1192.

23675
