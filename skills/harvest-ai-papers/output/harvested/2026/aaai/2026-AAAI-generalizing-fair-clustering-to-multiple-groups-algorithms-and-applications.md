---
title: "Generalizing Fair Clustering to Multiple Groups: Algorithms and Applications"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39077
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39077/43039
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Generalizing Fair Clustering to Multiple Groups: Algorithms and Applications

<!-- Page 1 -->

Generalizing Fair Clustering to Multiple Groups: Algorithms and Applications

Diptarka Chakraborty1, Kushagra Chatterjee1, Debarati Das2, Tien-Long Nguyen2

## 1 Nationaly University of Singapore 2 Pennsylvania State

University diptarka@comp.nus.edu.sg, kushagra.chatterjee@u.nus.edu, {dxd5606,tfn5179}@psu.edu

## Abstract

Clustering is a fundamental task in machine learning and data analysis, but it frequently fails to provide fair representation for various marginalized communities defined by multiple protected attributes – a shortcoming often caused by biases in the training data. As a result, there is a growing need to enhance the fairness of clustering outcomes, ideally by making minimal modifications, possibly as a postprocessing step after conventional clustering. A recent work initiated the study of closest fair clustering, though in a restricted scenario where data points belong to only two groups. In practice, however, data points are typically characterized by many groups, reflecting diverse protected attributes such as age, ethnicity, gender, etc. In this work, we generalize the study of the closest fair clustering problem to settings with an arbitrary number (more than two) of groups. We begin by showing that the problem is NP-hard even when all groups are of equal size – a stark contrast with the two-group case, for which an exact algorithm exists. Next, we propose near-linear time approximation algorithms that efficiently handle arbitrary-sized multiple groups. Leveraging our closest fair clustering algorithms, we further achieve improved approximation guarantees for the fair correlation clustering problem, advancing the state-of-the-art results. Additionally, we are the first to provide approximation algorithms for the fair consensus clustering problem involving multiple (more than two) groups.

Extended version — https://arxiv.org/pdf/2511.11539

## Introduction

Clustering, the task of partitioning a set of data points into groups based on their mutual similarity or dissimilarity, stands as a fundamental problem in unsupervised learning and is ubiquitous in applications of machine learning and data analysis. Often, each data point carries certain protected attributes, which can be encoded by assigning a specific color to each point. While traditional clustering algorithms typically succeed in optimizing their target objectives, they frequently fail to ensure fairness in their results. This shortfall can introduce or perpetuate biases against marginalized groups defined by sensitive attributes such as gender

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

or race (Kay, Matuszek, and Munson 2015; Bolukbasi et al. 2016). These potential biases arise not necessarily from the algorithms themselves, but from historical marginalization inherent in the data used for training. Addressing and mitigating such biases to achieve fair outcomes has emerged as a central topic in the field, with considerable attention given in recent years to the development of algorithms that guarantee demographic parity (Dwork et al. 2012) and/or equal opportunity (Hardt, Price, and Srebro 2016).

In the context of clustering, (Chierichetti et al. 2017) initiated the study of fair clustering to address the issue of disparate impact and promote fair representation. Their work initially focused on datasets with two groups, each point colored either red or blue, and aimed to partition the data such that the blue-to-red ratio in every cluster matched that of the overall dataset. However, restricting attention to only two colors is limiting, as real-world data often involves multiple (and sometimes non-binary) protected attributes, such as age, race, or gender, resulting in several disjoint colored groups. Subsequent research generalized the fair clustering framework to accommodate more than two colors (R¨osner and Schmidt 2018), requiring that the proportion of each colored group within clusters reflects the global proportions of colors. Further studies have considered scenarios where each color group is of equal size (B¨ohm et al. 2020). We refer to the related works for different variants of the clustering problems that have been studied under fairness constraints.

As previously highlighted, a range of effective clustering algorithms is available for various clustering paradigms; however, these methods may yield unfair or biased results when the training data itself is biased. Such skewed clustering outcomes may lead to inequitable treatment, particularly if the clusters serve as the basis for decision-making or analysis. To counteract this, post-processing existing clustering solutions to mitigate bias and achieve fairness is often necessary, ideally with only minimal adjustments to the cluster assignments. Despite the fundamental nature of this problem, it has received limited attention within the broader context of clustering in prior research. However, it has been studied for specific metric spaces, such as ranking (Celis, Straszak, and Vishnoi 2018; Chakraborty et al. 2022; Kliachkin et al. 2024). Only recently (Chakraborty et al. 2025a) did introduce the problem of obtaining a closest fair clustering, where given an existing clustering, finding a fair clustering

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19934

<!-- Page 2 -->

by altering as few assignments as possible. Their study, however, was confined to the special case of two colored groups, which, as previously noted, is restrictive in many practical scenarios. In their work, (Chakraborty et al. 2025a) presented O(1)-approximation algorithms for the case of blue and red groups with arbitrary ratios, and demonstrated that the problem can be solved exactly in near-linear time when the groups are of equal size. In the end, they posed the general case of more than two colored groups as an intriguing open direction. In this paper, we address this open problem by devising approximation algorithms and establishing computational hardness that holds even for equi-proportioned multiple-colored groups, thereby showing a stark distinction from the two-group case.

Building upon our findings for the closest fair clustering problem, we further investigate their implications for other prominent clustering variants, specifically correlation clustering and consensus clustering. In correlation clustering, one is presented with a labeled (typically complete) graph where each edge is marked as either + or −. The cost of a clustering is calculated as the total number of + edges that span across clusters and −edges that fall within clusters. This problem has widespread applications in fields such as data mining, social network analysis, computational biology, and marketing analysis (Bonchi, Garcia-Soriano, and Liberty 2014; Hou et al. 2016; Veldt, Gleich, and Wirth 2018; Bressan et al. 2019; Kushagra, Ben-David, and Ilyas 2019). The fair correlation clustering problem, introduced in (Ahmadian et al. 2020; Ahmadi et al. 2020), seeks a fair clustering that minimizes this cost. In their work, approximation algorithms were proposed for cases involving multiple colored groups, with the approximation factor depending on the ratios of the group sizes. In this paper, we improved upon their approximation bound and are the first to achieve an approximation guarantee independent of the group size ratio.

In consensus clustering, the objective is to derive a single, representative (consensus) clustering from a collection of clusterings over the same set of data points, to minimize a chosen objective function. The objective often depends on the application, with the most common being the median that minimizes the total distance to all input clusterings and the center that minimizes the maximum distance. Here, the distance between two clusterings is typically defined by the number of point pairs that are co-clustered (together) in one clustering but not in the other. Consensus clustering is widely applicable across various fields, including bioinformatics (Filkov and Skiena 2004b,a), data mining (Topchy, Jain, and Punch 2003), and community detection (Lancichinetti and Fortunato 2012). Recently, (Chakraborty et al. 2025a) extended the study of consensus clustering to incorporate fairness constraints, providing constant-factor approximations but only in the special case of two colored groups. In this work, we expand upon these results by establishing approximation guarantees for consensus clustering problems involving more than two colored groups.

Our Contribution In this work, we present both new algorithms and hardness results for the Closest Fair Clustering problem in settings where the input data points come from multiple groups, and also study two well-known applications, namely, the Fair Correlation Clustering and Fair Consensus Clustering problems, and provide new algorithm results. Below, we summarize our main contributions. Closest Fair Clustering with Multiple Groups. In this problem, we are given a clustering D = {D1, D2,..., Dm} defined on a dataset V where V is classified into a set χ of disjoint groups, each represented by a unique color. The objective is to compute a fair clustering of V, where the proportion of data points from each group (or color) within any output cluster should reflect their overall proportions in the entire dataset, while also minimizing the distance to the input clustering D.

• Considering |χ| to be the total number of colors, our first algorithm handles the case where each output cluster must contain the different colored points according to global ratio p1: p2: · · ·: p|χ|, and achieves an O(|χ|3.81)-approximation. This study significantly generalizes the work of (Chakraborty et al. 2025a), which focused solely on the binary (two-group) setting. • Next, we consider the special case where each output cluster must contain an equal number of data points from each color group, and we provide an O(|χ|1.6 log2.81 |χ|)-approximation for the Closest Fair Clustering problem. Furthermore, when |χ| is a power of two, we present an improved algorithm with an O(|χ|1.6)-approximation. • Finally, we show that the problem is NP-hard for any setting involving more than two colors, even when all color groups are equally represented in an output cluster. This shows a clear hardness gap between the two-color setting, where an exact algorithm exists, and the multicolor case, where the problem becomes computationally intractable; thus underscoring the necessity of our approximation algorithms.

Application to Fair Correlation Clustering. Building on the above result, we study their implications for another key clustering variant: the Fair Correlation Clustering problem. In correlation clustering, the input is a graph with edges labeled as + or -, and the goal is to produce a clustering minimizing disagreements; + edges between clusters and - edges within clusters. In the fair version, the clustering must also satisfy group fairness constraints. This problem has been shown to be NP-hard (Ahmadi et al. 2020).

• We begin by designing an algorithm for the setting where each output cluster must contain points from different color groups as per the global ratio p1: p2: · · ·: p|χ|, achieving an O(|χ|3.81)-approximation. This eliminates the dependence on the max-min color ratio q = max(pj)

min(pj) that appeared in the previous O(q2|χ|2) bound of (Ahmadian et al. 2020; Ahmadi et al. 2020), where q can be as large as a polynomial in |V |. • For the special case where each output cluster must contain an equal number of data points from each color group, we improve the approximation to

19935

<!-- Page 3 -->

O(|χ|1.6 log2.81 |χ|), and further to O(|χ|1.6) when |χ| is a power of two. This improves upon the previous O(|χ|2) bound given by (Ahmadian et al. 2020; Ahmadi et al. 2020).

Application to Fair Consensus Clustering. Next, we turn to another application: the consensus clustering problem. The goal here is to compute a single representative (consensus) clustering from a collection of input clusterings over the same dataset, minimizing a specified objective function (e.g., median or center) while also satisfying group fairness constraints. By combining a triangle inequality argument with our results for Closest Fair Clustering, we obtain new approximation guarantees for this problem. These results generalize the work of (Chakraborty et al. 2025a), which was limited to the binary (two-group) setting, to the more general multi-group case.

• Analogous to our results for fair correlation clustering, we obtain an O(|χ|3.81)-approximation algorithm for the general case with arbitrary group proportions. • For the equi-proportion case, we again improve the approximation to O(|χ|1.6 log2.81 |χ|), and further to O(|χ|1.6) when |χ| is a power of two.

The details are provided in the extended version.

Related Works Since the introduction of the fair clustering in (Chierichetti et al. 2017), recent years have witnessed a significant increase in research focused on different aspects of fair clustering problems. The literature so far encompasses numerous variants of the fair clustering problem with multiple colored groups, such as k-center/median/means clustering (Chierichetti et al. 2017; Huang, Jiang, and Vishnoi 2019), scalable clustering (Backurs et al. 2019), proportional clustering (Chen et al. 2019), fair representational clustering (Bera et al. 2019; Bercea et al. 2019), pairwise fair clustering (Bandyapadhyay, Fomin, and Simonov 2024; Bandyapadhyay et al. 2024, 2025), correlation clustering (Ahmadian et al. 2020; Ahmadi et al. 2020; Ahmadian and Negahbani 2023), 1-clustering over rankings (Wei et al. 2022; Chakraborty et al. 2022, 2025b), and consensus clustering (Chakraborty et al. 2025a), among others.

A comprehensive study of the correlation clustering problem was first undertaken in (Bansal, Blum, and Chawla 2004). Since then, correlation clustering has been studied across various graph settings, including the extensively examined complete graphs (Ailon, Charikar, and Newman 2008; Chawla et al. 2015) and weighted graphs (Demaine et al. 2006). The problem, even when restricted to complete graphs, is known to be APX-hard (Charikar, Guruswami, and Wirth 2005), with the best-known approximation algorithm currently achieving a 1.438-approximation factor (Cao et al. 2024). Its fair variant remains NP-hard even in the case of two color groups of equal sizes (Ahmadi et al. 2020), and several approximation algorithms have been developed for both the exact fairness notion (Ahmadian et al. 2020; Ahmadi et al. 2020) and the relaxed fairness notion (Ahmadian and Negahbani 2023).

The consensus clustering problem, under both the median and center objectives, is known to be NP-hard (Kˇriv´anek and Mor´avek 1986; Swamy 2004) and in fact, APX-hard (that is it is unlikely to have an (1 + ε)-factor algorithm for any ε > 0) even with as few as three input clusterings (Bonizzoni et al. 2008). Currently, the best-known algorithms include an 11/7-approximation for the median objective (Ailon, Charikar, and Newman 2008) and an approximation slightly better than 2 for the center objective (Das and Kumar 2025). Apart from that, various heuristics have been proposed to produce reasonable solutions (e.g.,(Goder and Filkov 2008; Monti et al. 2003; Wu et al. 2014)). More recently,(Chakraborty et al. 2025a) began examining fair consensus clustering, focusing on only two colored groups.

## Preliminaries

In this section, we define key terms and concepts that are essential for understanding our proofs and algorithms. Definition 1 (Fair Clustering). Given a set of points V and a set of colors χ = {c1, c2,..., ck}, suppose cj(V) ⊆V be the set of points of color cj in V. We call a clustering F of V a Fair Clustering if for all clusters F ∈F we have

|c1(F)|: · · ·: |ck(F)| = |c1(V)|: · · ·: |ck(V)|.

For two clustering C and C′ of V we define dist(C, C′) as the distance between two clustering C and C′. The distance is measured by the number of pairs (u, v) that are together in C but separated by C′ and the number of pairs (u, v) that are separated by C but together in C′. More specifically, dist(C, C′) =

{u, v} | u, v ∈V, [u ∼C v ∧u̸ ∼C′ v]

∨[u̸ ∼C v ∧u ∼C′ v]

where u ∼C v denotes whether both u and v belong to the same cluster in C or not. Definition 2 (Closest Fair Clustering). Given an arbitrary clustering D, a clustering F∗

D is called a closest Fair Clustering to D if for all Fair Clustering F we have dist(D, F) ≥dist(D, F∗

D). We use F∗

D to denote a closest Fair Clustering to D.

γ-close Fair Clustering We call a Fair Clustering F a γclose Fair Clustering to a clustering D if dist(D, F) ≤γ dist(D, F∗

D).

Approximate Closest Fair Clustering for

Equi-Proportion Groups In this section, we provide an approximation algorithm to find a closest Fair Clustering when all the groups are of equal size. Theorem 1. There exists an algorithm that, given a clustering D where each color group contains an equal number of points, computes an O(|χ|1.6 log2.81 |χ|)-close Fair Clustering in O(|V | log |V |) time, where χ denotes the set of colors. Moreover, when |χ| is a power of two, the algorithm computes a O(|χ|1.6)-close Fair Clustering.

First, let us handle the case when |χ| is a power of 2. To do that, we provide an algorithm fairpower-of-two, which produces an O(|χ|1.6)-close fair clustering Ffpt to a clustering D when |χ| is a power of 2.

19936

<!-- Page 4 -->

## Algorithm

fairpower-of-two Let the input be a clustering D = {D1, D2,..., Dm}, where each point is colored from a color set χ = {c1,..., ck}, and assume |χ| is a power of two. The goal is to output a clustering Ffpt in which every cluster contains an equal number of points of each color, i.e., cp(Fa) = cq(Fa) for all p̸ = q, Fa ∈Ffpt.

The algorithm proceeds in log |χ| iterations. At iteration i, the color set χ is partitioned into |χ|/2i disjoint blocks of size 2i, defined as:

Bi j = {c(j−1)·2i+1,..., cj·2i}, for j = 1,..., |χ|/2i.

Let N i be the clustering at iteration i, with N 0:= D. The algorithm maintains the invariant that, in every cluster N i a ∈ N i, the colors within each block Bi j appear equally. For adjacent blocks Bi j and Bi j+1 in a cluster N i a, the surplus T j a is the excess of the larger bucket over the smaller. The surplus is chosen so that all colors in the surplus are equally represented. Let us now describe the algorithm fairpower-of-two. 1. Initialization: Set N 0 ←D. 2. Iterative Refinement: For each iteration i = 1 to log |χ|: • Initialize N i ←N i−1. • For each pair of disjoint adjacent blocks (Bi j, Bi j+1): – For each cluster N i a ∈N i and odd j, compute the surplus T j a between adjacent blocks Bi j(N i a) and Bi j+1(N i a), and remove it. Here for a color block Bi j, Bi j(N i a) is the set of points in N i a that has a color from the block Bi j. – Store removed surpluses into sets Sj or Sj+1, de- pending on which block had the surplus. – Call multi-GM(Sj, Sj+1) to form new fair clusters and add them to N i. 3. Output: Return N log |χ| →Ffpt. Let us now describe the subroutine multi-gm. Given two collections of point groups from blocks Bi j and Bi j+1, the multi-GM procedure greedily merges pairs of subsets into fair subsets in which each color from Bi j ∪Bi j+1 is equally represented.

The subroutine: • Iteratively selects one subset from each collection. • Trims the larger subset to match the smaller, preserving equal color counts. • Merges the trimmed subsets into a fair set and adds it to the output. Continue this until no further fair subsets can be formed.

We provide the pseudocode of the algorithms fairpower-of-two and multi-gm in the extended version.

Proof of theorem 1 We now analyze the algorithm fairpower-of-two by first establishing the following. Lemma 1. Given a clustering D as input, the algorithm fairpower-of-two computes a O(|χ|1.6)-close Fair Clustering, where |χ| is a power of 2.

We show the above result by generating a sequence of log |χ| intermediate clusterings, with each intermediate step involving an approximation factor of 2, and thus finally achieving a factor of 3log |χ| = |χ|1.6. We provide the proof in the extended version.

The above lemma 1 proves theorem 1 when |χ| is a power of 2. Now, we prove theorem 1 for any values of |χ|. To do that, we need to describe the algorithm make-pdc-fair.

## Algorithm

make-pdc-fair Given a clustering I = {I1, I2,..., Is} over a point set V, where each point is colored from ζ = {z1,..., zr} and satisfies the global proportion:

z1(V): z2(V): · · ·: zr(V) = p1: p2: · · ·: pr, the goal is to construct a fair clustering Fmpf such that every cluster F ∈Fmpf satisfies this ratio. We assume w.l.o.g. that p1 > p2 > · · · > pr. Also assume that each input cluster is p-divisible, i.e., zj(Ii) is a multiple of pj. We call such clustering p-divisible clustering(pdc for short). Let us now describe the algorithm make-pdc-fair.

1. The algorithm proceeds in T = ⌈log2 r⌉iterations. Let F0:= I, and define:

I = F0 →F1 →· · · →FT = Fmpf, where each Ft enforces proportionality within blocks of colors. 2. Hierarchical Block Structure: At iteration t, the color set is partitioned into blocks {Bt

1, Bt 2,..., Bt mt}, constructed hierarchically:

Bt i = Bt−1

2i−1 ∪Bt−1 2i, with singleton blocks B0 j = {zj}.

If mt−1 is odd, the last block is carried forward unchanged. 3. Balancing Rule: To merge two sub-blocks A = Bt−1 2i−1 and B = Bt−1

2i, consider a cluster F t−1 ∈Ft−1, where zc(F t−1) = pc · x for zc ∈A, zd(F t−1) = pd · y for zd ∈B.

To equalize the scaling factors x and y, we do:

• If x > y: merge pd · (x −y) points of color zd ∈B into F t−1. • If x < y: cut pd · (y −x) points of color zd ∈B from F t−1.

This ensures that the merged block Bt i = A ∪B in each cluster F t ∈Ft satisfies the combined proportionality. 4. Output: After T = ⌈log2 r⌉iterations, the final clustering Fmpf satisfies: For all F ∈Fmpf, z1(F): z2(F): · · ·: zr(F) = p1: p2: · · ·: pr.

We provide the pseudocode of make-pdc-fair in the extended version.

To analyze the algorithm make-pdc-fair, we need to prove the following lemma.

19937

<!-- Page 5 -->

Lemma 2. The algorithm make-pdc-fair outputs a clustering F that is O(r2.81)-close Fair Clustering to the input clustering I, where r is the number of colors.

We show the above result by generating a sequence of log r intermediate clusterings, with each intermediate step involving an approximation factor of 6, and thus finally achieving a factor of 7log r = r2.81. We provide a detailed proof in the extended version.

Using lemma 1 and lemma 2, we can prove theorem 1. We provide the full proof of theorem 1 in the extended version.

Proof Sketch of theorem 1. We design an algorithm fair-equi to convert an arbitrary clustering D, where the color set χ is not necessarily a power of two, into a fair clustering F in which every color appears equally in each cluster. The algorithm proceeds in two main stages:

## 1 Color Grouping and Intermediate

Fairness: • Partition the color set χ into log |χ| disjoint groups G1,..., Glog |χ|, where each group’s size is a power of two. This is done greedily by assigning group sizes according to the binary representation of |χ|. • Apply the algorithm fairpower-of-two to obtain an intermediate clustering I, in which each group Gℓ satisfies intra-group fairness: all colors in Gℓappear equally in each cluster. 2. Global Fairness via Multi-Group Merging: • Treat each group Gℓas a single meta-color and apply the algorithm make-pdc-fair on I to obtain the final clustering F. • make-pdc-fair ensures that across all clusters, the meta-colors (i.e., groups) are in proportion to their sizes, and also restores uniformity within each group, thus achieving full color-wise fairness.

Approximation Bound:

• By lemma 1, the intermediate clustering I is O(|χ|1.6)close to D. • By lemma 2, the final clustering F is O(log2.81 |χ|)close to I. • Combining via triangle inequality yields:

dist(D, F) ≤O(|χ|1.6 log2.81 |χ|) · dist(D, F∗

D)

where F∗

D is the closest fair clustering to D.

This completes the proof sketch.

Approximate Closest Fair Clustering for

Arbitrary-Proportion Groups In this section, we prove the following theorem.

Theorem 2. There is an algorithm that, given an arbitrary clustering D over a vertex set V where each vertex v ∈V has a color in χ = {c1,..., ck}, finds a O(|χ|3.81)-close Fair Clustering F in time O(|V | log |V |).

To prove the above theorem, we take a 2-step approach similar to (Chakraborty et al. 2025a), which was constrained to only two colors.

(i) First, we convert the clustering D to a clustering M such that for each cluster Mi ∈M, cj(Mi) is divisible by pj. Recall we call such a clustering a p-divisible clustering. (ii) In the second step, we will provide the clustering M as input to the algorithm make-pdc-fair and get a fair clustering F as output.

Now, we provide an algorithm create-pdc to convert a clustering D on a vertex set V to a p-divisible clustering M.

## Algorithm

create-pdc Given a clustering D = {D1,..., Dm} over vertex set V, color set χ = {c1,..., ck}, and a proportion vector p = (p1,..., pk) satisfying:

c1(V): c2(V): · · ·: ck(V) = p1: p2: · · ·: pk.

The goal of create-pdc is to convert D into a pdivisible clustering M where each cluster contains a multiple of pj points of color cj. Key Definitions:

• Surplus: σ(Di, cj) ⊆Di of size cj(Di) mod pj if pj ∤ cj(Di), else it has size pj, denoting excess cj-colored vertices in Di. • Total surplus: σj = P Di∈D |σ(Di, cj)| (always a multiple of pj). • Deficit: δ(Di, cj) ⊆V \ Di, of size pj −|σ(Di, cj)|. Represents the number of cj colored points required to make it a multiple of pj. • Cut and merge costs:

κj(Di) = |σ(Di, cj)| · (|Di| −|σ(Di, cj)|)

µj(Di) = |δ(Di, cj)| · |Di|

Let us now describe the algorithm create-pdc

1. For each color cj, initialize σj/pj empty auxiliary clusters {P1,..., Pσj/pj}. 2. Classify each cluster Di ∈D into:

• CUT, if |σ(Di, cj)| ≤pj/2 • MERGE, otherwise.

## 3. Cut and redistribute: While CUT is non-empty:

• For Di ∈CUT, remove σ(Di, cj) from Dk. • Try to donate surplus to deficits in Dℓ∈MERGE. • If no deficit remains, assign surplus to an available extra cluster Pm, ensuring each Pm reaches size pj.

## 4. Handle remaining merges: While deficits remain:

• Pick the cluster with minimal κj(Dk) −µj(Dk), redistribute its surplus as above. Note that in this step, we can pick a cluster multiple times. • Remove a cluster Dℓ∈MERGE if it deficit is satisfied. • Repeat until all deficits are filled.

## 5 Output:

The final clustering M where each cluster is pdivisible for all colors.

19938

<!-- Page 6 -->

We provide the pseudocode of the algorithm create-pdc in the extended version.

Now, we analyze the algorithm create-pdc. To analyze and state the lemma, let us define some terms

• Optimal-p-divisible clustering: Given a clustering D, we call a clustering M∗an optimal-p-divisible clustering if dist(D, M∗) ≤dist(D, M). • α-close-p-divisible clustering: Given a clustering D, we call a clustering M an α-close-p-divisible clustering if dist(D, M) ≤α dist(D, M∗).

Now, we state the lemma for analyzing the algorithm create-pdc.

Lemma 3. Given a clustering D, the algorithm create-pdc outputs a clustering M s.t. M is O(|χ|)close-p-divisible clustering to D.

We provide the proof of lemma 3 in the extended version. Next, we prove theorem 2 assuming lemma 3.

Proof of theorem 2. To prove the theorem, we describe an algorithm fair-general that proceeds in two stages. First, we apply the algorithm create-pdc to the input clustering D to obtain a p-divisible clustering M that is O(|χ|)-close to D. Then, we apply the algorithm make-pdc-fair on M to obtain the final fair clustering F, which is O(|χ|2.81)-close to M (see lemma 2). By combining the guarantees from both steps, we conclude that F is O(|χ|3.81)-close Fair Clustering to the input D.

dist(D, F) ≤dist(D, M) + dist(M, F)

(by triangle inequality)

≤O(|χ|) dist(D, F∗)

+ O(|χ|2.81) dist(M, F∗)

≤O(|χ|) dist(D, F∗)

+ O(|χ|2.81)(dist(D, M) + dist(D, F∗))

≤O(|χ| + |χ|3.81 + |χ|2.81) dist(D, F∗)

≤O(|χ|3.81) dist(D, F∗)

This completes the proof of theorem 2.

Hardness for Three Equi-Proportion Groups In this section, we show that finding a closest fair clustering to a given clustering where each point is assigned one color from a set of k ≥3 colors is hard even when the number of points in each color class is equal. Our reduction also extends to arbitrary color ratios.

We begin by defining the decision version of closest fair clustering with multiple colors and equal representation.

Definition 3 (k-CLOSEST EQUIFAIR). Given a clustering H over a set of points V where each point is assigned with one of the colors from a set of k ≥3 colors, and the number of points of each color is equal, together with a non-negative integer τ, decide between the following:

• YES: There exists a Fair Clustering (on input point set) F such that dist(H, F) ≤τ;

• NO: For every Fair Clustering (on input point set) F, dist(H, F) > τ.

We show the following theorem.

Theorem 3. For any integer k ≥3, k-CLOSEST EQUIFAIR is NP-hard.

We present a polynomial-time reduction from the 3-PARTITION problem (defined below) to k-CLOSEST EQUIFAIR.

Definition 4 (3-PARTITION). Given a (multi)set of positive integers S = {x1,..., xd}, decide whether (YES:) there exists a partition of S into m disjoint subsets S1, S2,..., Sf ⊆ S where f = d/3, such that

• For all i, |Si| = 3; and

• For all i, P xj∈Si xj = T, where T =

P xj ∈S xj n/3, or (NO:) no such partition exists.

We reduce from a restricted version of 3-PARTITION, in which each xi ∈S satisfies xi ∈(T/4, T/2), where T = 3 n

P xi∈S xi, and additionally xi ≤db, for some non-negative constant b. Note that, this variant remains NP-complete, as established by (Garey and Johnson 1975), which shows that 3-PARTITION as defined in definition 4 is strongly NP-complete. Hence, for the rest of this section, we refer to this restricted version simply as 3-PARTITION.

Description of Reduction. Given a 3-PARTITION instance S = {x1, x2,..., xd} we create a k-CLOSEST EQUIFAIR instance (H, τ) as follows:

• H = {GB1, GB2,..., GBd/3, R1, R2,..., Rd}, where for each i ∈{1,..., d/3}, GBi is a cluster of size (k − 1)T with T points of color ct (2 ≤t ≤k), and for each j ∈{1,..., n}, Rj is a monochromatic c1 cluster (i.e., containing only points with color c1) of size xj (i.e., |Rj| = xj);

• Set τ = n 3 (k −1)T 2 + 1 2 Pn i=1 xi(T −xi), if k > 3, and, τ = 2 Pn i=1 x2 i + 2 Pn i=1 xi(T −xi), if k = 3.

Note that for each xi ≤db, for some non-negative constant b, the size of the instance (H, τ) is polynomial in d. Moreover, it is straightforward to see that the reduction runs in polynomial time.

The following lemma argues that the above reduction maps a YES instance of the 3-PARTITION to a YES instance of the k-CLOSEST EQUIFAIR, the proof of which is deferred to the extended version.

Lemma 4. For any integer k ≥3, if S is a YES instance of the 3-PARTITION, then (H, τ) is also a YES instance of the k-CLOSEST EQUIFAIR.

It remains to demonstrate that our reduction maps a NO instance of the 3-PARTITION to a NO instance of the k-CLOSEST EQUIFAIR.

Lemma 5. For k ≥3, if S is a NO instance of the 3-PARTITION, then (H, τ) is also a NO instance of the k-CLOSEST EQUIFAIR.

19939

<!-- Page 7 -->

Proof. Assume to the contrary that (H, τ) is a YES instance. Then there exists a Fair Clustering F such that dist(H, F) ≤τ.

Without loss of generality, we refer to c1 as the color red, and refer to c2 as the color blue.

Let V ′ be the set of red-blue points obtained from V by recoloring every point with color cj (j ≥3) to blue. Denote Hc and Fc the clusterings obtained from H and F, respectively, under this recoloring. Then, dist(Hc, Fc) = dist(H, F). We analyze the structure of Hc and Fc.

Observe that Hc is a clustering over V ′, in which Hc = {B1, B2,..., Bn/3, R1, R2,..., Rn}, where each Bi is a monochromatic blue cluster of size (k −1)T, obtained from the original cluster GBi in H by recoloring every point to blue. Each Ri is a monochromatic red cluster, which remains unchanged from H.

Now we claim that Fc is a Fair Clustering clustering over V ′. Indeed, recall that F is a Fair Clustering over V. Hence, in every cluster F ∈F, the numbers of points of each color are equal, that is, |ci(F)| = |cj(F)|, for all 1 ≤i, j ≤k. Note that each cluster F c ∈Fc is obtained from a cluster in F by recoloring every point with color ci (i ≥3) to blue. Hence, the ratio between the number of blue points and the number of red points in F c is (k −1). This implies that Fc is a Fair Clustering over V ′.

Applying a result from (Chakraborty et al. 2025a, Lemma 45, Lemma 46) for the set of points V ′, it follows that dist(Hc, Fc) > τ, which is a contradiction since we have established that dist(Hc, Fc) = dist(H, F) ≤τ. This concludes that (H, τ) is a NO instance.

As our reduction runs in polynomial time, from lemma 4 and lemma 5, we conclude that k-CLOSEST EQUIFAIR is NP-hard. This completes the proof of theorem 3. In the extended version, we remark on how to generalize this reduction for arbitrary ratios.

Implication to Fair Correlation Clustering Given a complete undirected graph G(V, E) where each edge (u, v) ∈E is labeled either “+” (similar) or “−” (dissimilar), let E+ and E−denote the sets of “+” and “−” edges, respectively. A clustering C = {C1, C2,..., Ct} partitions V into disjoint subsets.

Let EXT(C) denote the set of inter-cluster edges and INT(C) the set of intra-cluster edges. The cost of clustering C is defined as:

cost(C) = | EXT(C) ∩E+| + | INT(C) ∩E−|.

The goal is to find a clustering that minimizes cost(C). In addition, when we want C to be also a Fair Clustering, the problem is referred to as fair correlation clustering.

Theorem 4. There exists an algorithm that, given a correlation clustering instance G, computes a O(|χ|1.6 log2.81 |χ|) approximate fair correlation clustering when there are equal number of data points from each color group, and a O(|χ|3.81) approximate fair correlation clustering when the ratio between the number of points from different color groups is arbitrary.

To prove theorem 4, we use the following.

Lemma 6. Let C be a clustering, and suppose there exists an algorithm A that computes an γ-close fair clustering with respect to C. Additionally, suppose there exists a β-approximation algorithm B for the standard correlation clustering problem on a graph G. Then, there exists an algorithm that computes a fair correlation clustering of G with approximation factor (γ + β + γβ).

Proof. Let us first describe the algorithm fairifyCC, which computes a fair correlation clustering for a given instance G.

• Input: Correlation clustering instance G. • Output: A fair clustering F. • Procedure: 1. Compute a correlation clustering D of G using a βapproximation algorithm B. 2. Apply the closest fair clustering algorithm A to D to obtain a fair clustering F that is γ-close to D. 3. Return F.

We argue that F is (γ + β + γβ) approximate correlation clustering of G using triangle inequality. We defer the proof to the extended version.

Proof of theorem 4. By (Cao et al. 2025), we get that there exists an O(1)-approximation algorithm to find a correlation clustering for a correlation clustering instance G. When each color group has the same size, the algorithm fair-equi produces an O(|χ|1.6 log2.81 |χ|)-close clustering to any input clustering D. Hence, by lemma 6 we get that the algorithm fairifyCC produces an O(|χ|1.6 log2.81 |χ|) approximate fair correlation clustering.

In the general case with arbitrary group size ratio p1: p2: · · ·: p|χ|, the algorithm fair-general gives O(|χ|3.81)close clustering to any input clustering D. Hence, again by lemma 6 we show algorithm fairifyCC produces an O(|χ|3.81) approximate fair correlation clustering.

## Conclusion

In this paper, we generalize the closest fair clustering problem originally proposed by (Chakraborty et al. 2025a) to scenarios involving any number of groups, thereby addressing settings with non-binary, multiple protected attributes. We demonstrate that the problem becomes NP-hard even when there are just three equal-sized groups, showing a strong separation with the two equi-proportion group case, where an exact solution exists. We further propose nearlinear time approximation algorithms for clustering with multiple (potentially unequal-sized) groups, answering an open problem posed by (Chakraborty et al. 2025a). Leveraging these results, we achieve improved approximation guarantees for fair correlation clustering and, for the first time, provide approximation guarantees for fair consensus clustering involving more than two groups. Promising directions for future research include improving the approximation factors further and investigating alternative fairness criteria with similar approximation guarantees.

19940

<!-- Page 8 -->

## Acknowledgments

Diptarka Chakraborty was supported in part by an MoE AcRF Tier 1 grant (T1 251RES2303), and a Google South & South-East Asia Research Award. Kushagra Chatterjee was supported by an MoE AcRF Tier 1 grant (T1 251RES2303). Debarati Das was supported in part by NSF grant 2337832.

## References

Ahmadi, S.; Galhotra, S.; Saha, B.; and Schwartz, R. 2020. Fair correlation clustering. arXiv preprint arXiv:2002.03508.

Ahmadian, S.; Epasto, A.; Kumar, R.; and Mahdian, M. 2020. Fair Correlation Clustering. In International Conference on Artificial Intelligence and Statistics (AISTATS), volume 108, 4195–4205.

Ahmadian, S.; and Negahbani, M. 2023. Improved approximation for fair correlation clustering. In International Conference on Artificial Intelligence and Statistics, 9499–9516. PMLR.

Ailon, N.; Charikar, M.; and Newman, A. 2008. Aggregating inconsistent information: ranking and clustering. Journal of the ACM (JACM), 55(5): 1–27.

Backurs, A.; Indyk, P.; Onak, K.; Schieber, B.; Vakilian, A.; and Wagner, T. 2019. Scalable Fair Clustering. In International Conference on Machine Learning (ICML), volume 97, 405–413.

Bandyapadhyay, S.; Chen, T.; Friggstad, Z.; and Jamshidian, M. 2025. A Constant-Factor Approximation for Pairwise Fair k-Center Clustering. In International Conference on Integer Programming and Combinatorial Optimization, 43– 57. Springer.

Bandyapadhyay, S.; Chlamt´aˇc, E.; Friggstad, Z.; Jamshidian, M.; Makarychev, Y.; and Vakilian, A. 2024. A Polynomial-Time Approximation for Pairwise Fair k- Median Clustering. arXiv preprint arXiv:2405.10378.

Bandyapadhyay, S.; Fomin, F. V.; and Simonov, K. 2024. On coresets for fair clustering in metric and euclidean spaces and their applications. Journal of Computer and System Sciences, 142: 103506.

Bansal, N.; Blum, A.; and Chawla, S. 2004. Correlation clustering. Machine learning, 56(1): 89–113.

Bera, S.; Chakrabarty, D.; Flores, N.; and Negahbani, M. 2019. Fair algorithms for clustering. Advances in Neural Information Processing Systems, 32.

Bercea, I. O.; Groß, M.; Khuller, S.; Kumar, A.; R¨osner, C.; Schmidt, D. R.; and Schmidt, M. 2019. On the Cost of Essentially Fair Clusterings. In Approximation, Randomization, and Combinatorial Optimization. Algorithms and Techniques (APPROX/RANDOM 2019), 18–1. Schloss Dagstuhl–Leibniz-Zentrum f¨ur Informatik.

B¨ohm, M.; Fazzone, A.; Leonardi, S.; and Schwiegelshohn, C. 2020. Fair clustering with multiple colors. arXiv preprint arXiv:2002.07892.

Bolukbasi, T.; Chang, K.-W.; Zou, J. Y.; Saligrama, V.; and Kalai, A. T. 2016. Man is to computer programmer as woman is to homemaker? debiasing word embeddings. Advances in Neural Information Processing Systems (NeurIPS), 29. Bonchi, F.; Garcia-Soriano, D.; and Liberty, E. 2014. Correlation clustering: from theory to practice. In KDD, 1972. Bonizzoni, P.; Vedova, G. D.; Dondi, R.; and Jiang, T. 2008. On the Approximation of Correlation Clustering and Consensus Clustering. J. Comput. Syst. Sci., 74(5): 671–696. Bressan, M.; Cesa-Bianchi, N.; Paudice, A.; and Vitale, F. 2019. Correlation clustering with adaptive similarity queries. Advances in neural information processing systems, 32. Cao, N.; Cohen-Addad, V.; Lee, E.; Li, S.; Lolck, D. R.; Newman, A.; Thorup, M.; Vogl, L.; Yan, S.; and Zhang, H. 2025. Solving the Correlation Cluster LP in Sublinear Time. In Proceedings of the 57th Annual ACM Symposium on Theory of Computing, 1154–1165. Cao, N.; Cohen-Addad, V.; Lee, E.; Li, S.; Newman, A.; and Vogl, L. 2024. Understanding the Cluster Linear Program for Correlation Clustering. In Proceedings of the 56th Annual ACM Symposium on Theory of Computing, 1605–1616. Celis, L. E.; Straszak, D.; and Vishnoi, N. K. 2018. Ranking with Fairness Constraints. In International Colloquium on Automata, Languages, and Programming (ICALP), volume 107, 28:1–28:15. Chakraborty, D.; Chatterjee, K.; Das, D.; Nguyen, T. L.; and Nobahari, R. 2025a. Towards Fair Representation: Clustering and Consensus. 38th Annual Conference on Learning Theory (COLT 2025); full version: arXiv preprint arXiv:2506.08673. Chakraborty, D.; Das, H.; Dey, S.; and Yao, A. Y. H. 2025b. Improved Rank Aggregation Under Fairness Constraint. In Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence, IJCAI 2025, Montreal, Canada, August 16-22, 2025, 330–338. ijcai.org. Chakraborty, D.; Das, S.; Khan, A.; and Subramanian, A. 2022. Fair rank aggregation. Advances in Neural Information Processing Systems, 35: 23965–23978. Full version: arXiv preprint arXiv:2308.10499. Charikar, M.; Guruswami, V.; and Wirth, A. 2005. Clustering with qualitative information. Journal of Computer and System Sciences, 71(3): 360–383. Chawla, S.; Makarychev, K.; Schramm, T.; and Yaroslavtsev, G. 2015. Near optimal lp rounding algorithm for correlationclustering on complete and complete k-partite graphs. In Proceedings of the forty-seventh annual ACM symposium on Theory of computing, 219–228. Chen, X.; Fain, B.; Lyu, L.; and Munagala, K. 2019. Proportionally Fair Clustering. In International Conference on Machine Learning (ICML), 1032–1041. Chierichetti, F.; Kumar, R.; Lattanzi, S.; and Vassilvitskii, S. 2017. Fair clustering through fairlets. In Advances in Neural Information Processing Systems (NeurIPS), 5029–5037.

19941

<!-- Page 9 -->

Das, D.; and Kumar, A. 2025. Breaking the Two Approximation Barrier for Various Consensus Clustering Problems. In Azar, Y.; and Panigrahi, D., eds., Proceedings of the 2025 Annual ACM-SIAM Symposium on Discrete Algorithms, SODA 2025, New Orleans, LA, USA, January 12-15, 2025, 323–372. SIAM. Demaine, E. D.; Emanuel, D.; Fiat, A.; and Immorlica, N. 2006. Correlation clustering in general weighted graphs. Theoretical Computer Science, 361(2-3): 172–187. Dwork, C.; Hardt, M.; Pitassi, T.; Reingold, O.; and Zemel, R. 2012. Fairness through awareness. In Innovations in Theoretical Computer Science, 214–226. Filkov, V.; and Skiena, S. 2004a. Heterogeneous data integration with the consensus clustering formalism. In International Workshop on Data Integration in the Life Sciences, 110–123. Springer. Filkov, V.; and Skiena, S. 2004b. Integrating microarray data by consensus clustering. International Journal on Artificial Intelligence Tools, 13(04): 863–880. Garey, M. R.; and Johnson, D. S. 1975. Complexity results for multiprocessor scheduling under resource constraints. SIAM journal on Computing, 4(4): 397–411. Goder, A.; and Filkov, V. 2008. Consensus clustering algorithms: Comparison and refinement. In 2008 Proceedings of the Tenth Workshop on Algorithm Engineering and Experiments (ALENEX), 109–117. SIAM. Hardt, M.; Price, E.; and Srebro, N. 2016. Equality of opportunity in supervised learning. In Advances in Neural Information Processing Systems (NeurIPS), 3315–3323. Hou, J. P.; Emad, A.; Puleo, G. J.; Ma, J.; and Milenkovic, O. 2016. A new correlation clustering method for cancer mutation analysis. Bioinformatics, 32(24): 3717–3728. Huang, L.; Jiang, S. H.; and Vishnoi, N. K. 2019. Coresets for Clustering with Fairness Constraints. In Advances in Neural Information Processing Systems (NeurIPS), 7587– 7598. Kay, M.; Matuszek, C.; and Munson, S. A. 2015. Unequal representation and gender stereotypes in image search results for occupations. In ACM conference on human factors in computing systems, 3819–3828. Kliachkin, A.; Psaroudaki, E.; Mareˇcek, J.; and Fotakis, D. 2024. Fairness in Ranking: Robustness through Randomization without the Protected Attribute. In 2024 IEEE 40th International Conference on Data Engineering Workshops (ICDEW), 201–208. IEEE. Kˇriv´anek, M.; and Mor´avek, J. 1986. NP-hard problems in hierarchical-tree clustering. Acta informatica, 23: 311–323. Kushagra, S.; Ben-David, S.; and Ilyas, I. 2019. Semisupervised clustering for de-duplication. In The 22nd International Conference on Artificial Intelligence and Statistics, 1659–1667. PMLR. Lancichinetti, A.; and Fortunato, S. 2012. Consensus clustering in complex networks. Scientific reports, 2(1): 336. Monti, S.; Tamayo, P.; Mesirov, J.; and Golub, T. 2003. Consensus clustering: a resampling-based method for class discovery and visualization of gene expression microarray data. Machine learning, 52: 91–118.

R¨osner, C.; and Schmidt, M. 2018. Privacy Preserving Clustering with Constraints. In 45th International Colloquium on Automata, Languages, and Programming (ICALP 2018), 96–1. Schloss Dagstuhl–Leibniz-Zentrum f¨ur Informatik. Swamy, C. 2004. Correlation Clustering: maximizing agreements via semidefinite programming. In SODA, volume 4, 526–527. Citeseer. Topchy, A.; Jain, A. K.; and Punch, W. 2003. Combining multiple weak clusterings. In Third IEEE international conference on data mining, 331–338. IEEE. Veldt, N.; Gleich, D. F.; and Wirth, A. 2018. A correlation clustering framework for community detection. In Proceedings of the 2018 World Wide Web Conference, 439–448. Wei, D.; Islam, M. M.; Schieber, B.; and Roy, S. B. 2022. Rank Aggregation with Proportionate Fairness. In SIG- MOD International Conference on Management of Data, 262–275. Wu, J.; Liu, H.; Xiong, H.; Cao, J.; and Chen, J. 2014. Kmeans-based consensus clustering: A unified view. IEEE transactions on knowledge and data engineering, 27(1): 155–169.

19942
