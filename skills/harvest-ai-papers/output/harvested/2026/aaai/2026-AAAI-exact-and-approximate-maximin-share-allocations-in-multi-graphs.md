---
title: "Exact and Approximate Maximin Share Allocations in Multi-Graphs"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38719
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38719/42681
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Exact and Approximate Maximin Share Allocations in Multi-Graphs

<!-- Page 1 -->

Exact and Approximate Maximin Share Allocations in Multi-Graphs

George Christodoulou1,2, Symeon Mastrakoulis1,2

1Aristotle University of Thessaloniki, 2 Archimedes, Athena Research Center, Greece gichristo@csd.auth.gr, smastra@csd.auth.gr

## Abstract

We study the problem of (approximate) maximin share (MMS) allocation of indivisible items among a set of agents. We focus on the graphical valuation model, in which the input is given by a graph where edges correspond to items, and vertices correspond to agents. An edge may have non-zero marginal value only for its incident vertices. We study additive, XOS and subadditive valuations and we present positive and negative results for (approximate) MMS fairness, and also for (approximate) pair-wise maximin share (PMMS) fairness.

## Introduction

The fair allocation of indivisible goods is a fundamental problem that arises in various fields, including game theory, social choice theory, and multi-agent systems. The objective is to allocate a set of m indivisible items among n agents in a way that satisfies a predefined notion of fairness. Over time, various fairness criteria have been explored, each capturing a distinct interpretation of what constitutes a “fair” allocation. In the case of divisible goods—studied in the context of cake-cutting—the key fairness concepts are envy-freeness and proportionality. An allocation is called envy-free if no agent envies the portion allocated to another agent, while it is called proportional if every agent receives her proportional share, which is at least 1/n of her total value for the whole cake. Unfortunately, it is well known that both notions may fail to exist in the discrete setting. It is therefore natural to employ relaxed or approximate fairness notions when dealing with indivisible goods.

In this work, we consider maximin share (MMS), the most prominent relaxation of proportionality in the context of indivisible goods, introduced by (Budish 2011). Each agent i has an associated threshold, called her maximin share µi, which is equal to the maximum value agent i can secure if she partitions the set of items into n bundles and receives the lowest-value bundle. Under this notion, an allocation is considered fair if every agent receives at least her MMS value.

(Kurokawa, Procaccia, and Wang 2018) first showed that, unfortunately, it is not always possible to guarantee the

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

MMS value for every agent, even under additive valuations. Consequently, research has shifted toward approximate MMS fairness, where each agent is guaranteed a given fraction of her MMS value. This has led to a surge of research in the past decade, primarily for additive valuations (Amanatidis et al. 2017; Akrami and Garg 2023; Garg and Taki 2021; Ghodsi et al. 2021) but also for more general valuation classes (Ghodsi et al. 2022; Barman and Krishnamurthy 2020; Seddighin and Seddighin 2024; Akrami et al. 2023b; Feige and Grinberg 2025; Feige and Huang 2025). Determining the best possible guarantees for important valuation classes, including additive, XOS, and subadditive, remains an active area of research.

Graphical Valuations. While exact MMS allocations are not always achievable in general, they are known to exist for the case of two agents. A natural extension of the two-agent setting to the multi-agent setting, is the graphical model introduced by (Christodoulou et al. 2023) in the context of EFX1. In this model, agent valuations are represented by a graph where vertices correspond to agents, and edges correspond to items. Each edge {i, j} may have a positive marginal value for agents i and j only; for all other agents, the item has zero marginal value. In the case of multi-graphs, multiple parallel edges between any pair of vertices are possible. The graphical model has recently received considerable attention in the study of EFX, with significant progress made for various classes of (multi-)graphs (see e.g. (Hsu 2024; Bhaskar and Pandit 2024; Afshinmehr et al. 2024; Zhou et al. 2024; Misra and Sethia 2024; Sgouritsa and Sotiriou 2025; Blaˇzej et al. 2025)) drawing interesting connections between graph theory and fair division. However, while the existence of EFX allocations in simple graphs is known (Christodoulou et al. 2023), the question of EFX existence for general multi-graphs remains open.

In this work, we study approximate MMS fairness, and other related notions of fairness, for the case of multi-graphs.

## 1.1 Our Contribution

We study (approximate) MMS, the predominant notion of share-based fairness for the case of indivisible goods for

1EFX, proposed in (Caragiannis et al. 2019) is an extensively studied relaxation of envy-freeness.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16761

<!-- Page 2 -->

graphical valuations2 which has been previously studied in the context of EFX. We also obtain results on pairwise maximin share (PMMS) (Caragiannis et al. 2019) as well as on ordinal approximation (1-out-of-d) (Budish 2011) which are strongly related to MMS. An allocation is PMMS fair, if for any pair of agents i and j, it guarantees that agent i receives at least the MMS threshold on the restricted set of items she shares with j. An allocation is 1-out-of-d fair if it ensures to each agent the minimum value she could guarantee if she could partition all the items in d parts, assuming she receives her least preferred bundle.

We explore additive, XOS, and subadditive valuations3.

Additive Valuations. In Section 3, we study additive valuations and show that in multi-graphs, an exact MMS allocation 4 always exists for any number of agents (Theorem 1). This contrasts with the general (non-graphical) case, where exact MMS cannot be achieved, for n ≥3 (Kurokawa, Procaccia, and Wang 2018). In fact, we establish two stronger results: first, the existence of an allocation that is both MMS and PMMS (Theorem 1), and second, the existence of a 1out-of-3 allocation, and hence MMS for n ≥3 (Theorem 2).

We also show that even in graphs, MMS does not imply αapproximation of PMMS up to any factor α. This was previously known for general instances (Caragiannis et al. 2019). Interestingly, our impossibility result holds even for the case of symmetric multi-graphs, where each item has the same value for both endpoints (agents).

XOS Valuations. In Section 4, we consider XOS valuations and prove the existence of a 2/3-MMS allocation for any n ≥3 (Theorem 4). This contrasts with general (nongraphical) XOS valuations, where an upper bound of 1/2 is known (Seddighin and Seddighin 2024). We complement this positive result by providing a

1 − 1 ⌈n/2⌉+1

-MMS approximation upper bound for n agents. (Theorem 6). For 3 and 4 agents, this bound matches our lower bound of 2/3. Both the upper and lower bounds rely on an interesting connection with extremal combinatorics, particularly the existence of independent transversals in multipartite graphs.

Moreover, we show a (1 −1/d)-out-of-d approximation when the number of agents is n ≤3 and a 1

2-out-of-2 approximation for an arbitrary number of agents n. We explicitly show that there exists a graph with XOS agents in which no (1/2 + ε)-PMMS orientation exists, but an exact PMMS allocation does exist (Theorem 8).

Subadditive Valuations. Finally, in Section 5 we consider the case of subadditive valuations5 and we show a tight 1/2-

2We remark that for simple graphs, each agent’s MMS value is 0, making any allocation trivially MMS fair. 3We refer the reader to Section 2 for formal definitions of fairness notions and valuation functions.

4For MMS, we can focus on orientations—where each edge is allocated to an incident node— as for every allocation, there exists an equally good orientation while the orientation is not wasteful.

5Independently, (Feige 2025) showed the existence of 1/2-outof-2 for subadditive agents and multi-graphs, using different techniques.

Valuations General Model Graph Model Additive h

3/4 + 3/3836†, 1 − 1 n4

††i

Exact MMS XOS lower 4/17¶ 2/3 XOS upper 1/2§ 1 − 1 ⌈n/2⌉+1 Subadditive h

## 1 O(log log n)

∗∗, 1/2§i

1/2

**Table 1.** Best known approximate MMS for general model and for the graph model. Our contributions appear in bold. One fraction indicates a tight approximation and two fractions with brackets indicate lower and upper bounds. †(Akrami and Garg 2023); ††(Feige, Sapir, and Tauber 2021); ¶ (Feige and Grinberg 2025); § (Ghodsi et al. 2022); ∗∗(Feige 2025).

MMS approximation for any n ≥2 (Theorem 7). We emphasize that our results imply a separation between subadditive and XOS valuations with respect to approximate MMS in the graph model. Notably, such a separation remains an open problem in the general (non graphical) setting. Furthermore, for orientations, we show the existence of a 1/2- PMMS orientation and provide a matching impossibility result that is tight even for XOS.

Discussion. We remark that while at first look PMMS may seem to ”fit” better within the graphical model, our results show that it is wasteful6 i.e. there exist instances in which in order to achieve PMMS fairness, we may need to allocate to some agent an item with no value for her. In contrast, we show that this is not the case for MMS fairness. That is, the MMS fairness of an allocation from the perspective of agent i does not depend on the bundle or the valuation of any other agent j. Thus, it is reasonable to study MMS in graphical model and as a result, our techniques and our tools can be also used in the general model.

We also remark that the 1-out-of-d threshold is (weakly) monotonically decreasing as the number of partitions d increases. Hence, we obtain stronger results using d < n such as when d = 2.

Overall, we show that the graph setting yields provably improved results for additive and XOS valuations, but not for subadditive valuations, where we match the best known upper bound. We also investigate the relationship between orientations versus allocations under the PMMS notion. Additionally, we study other important share-based notions of fairness, such as PMMS and 1-out-of-d MMS fairness.

## 1.2 Further Related Work

We focus on approximate MMS fairness and also provide results for PMMS and 1-out-of-d fair notions which are strongly related to MMS. We refer the interested reader to the survey by (Amanatidis et al. 2023) covering a wide variety of discrete fair division settings along with the main fairness notions and their properties.

Maximin Share and α-MMS Over the past few years, MMS has seen significant progress for all valuation classes.

6This is similar to the case of EFX in graphs.

16762

<!-- Page 3 -->

Although for two agents with additive valuations, MMS allocations always exist, it is known that there exist instances where it is impossible to allocate items in such a way to guarantee for every agent her exact MMS value. (Kurokawa, Procaccia, and Wang 2018) proved an upper bound of 1−O(1

2n) for additive valuations and n agents. Later, (Feige, Sapir, and Tauber 2021) provided an improved bound of 1 − 1 n4. For additive valuations there is an abundance of works which has led to strong approximation guarantees. Among all the works, we note the existence of 2/3-MMS allocation for n agents in (Kurokawa, Procaccia, and Wang 2018), the existence of 3/4-MMS allocation for n agents by (Ghodsi et al. 2021) and the existence of 3/4 + 1/12n for n agents by (Garg and Taki 2021). (Akrami et al. 2023a) improved the approximation to 3

4 +min{ 1 36, 16n−4}. Recently, (Akrami and Garg 2023) improved the approximation factor to 3/4 + 3/3836, which is the best approximation we know so far for additive valuations.

Our understanding of valuation classes beyond additive is limited. For submodular functions, a tight 2/3-MMS approximation for two agents is known (Christodoulou and Christoforidis 2025; Kulkarni, Kulkarni, and Mehta 2023). For more agents, a lower bound of 10/27 is known (Ben- Uziahu and Feige 2023) and (Ghodsi et al. 2022) established an upper bound of 3/4. Moreover, for fractionally subadditive valuations, (Feige and Grinberg 2025) recently proved the existence of a 4/17-MMS allocation while a 1/2 upper bound is known (Ghodsi et al. 2022). The gaps are larger for the class of subadditive valuations; there always exists a 1 O(log log n)-MMS allocation (Feige 2025) while the best known upper bound is 1/2 (Ghodsi et al. 2022).

Research has also shifted towards more restricted valuations such as bi-values (Amanatidis et al. 2017), leveled valuations (Christodoulou and Christoforidis 2025), SPLC valuations (Chekuri et al. 2023), Borda and lexicographical valuations (Heinen et al. 2018), leading to interesting results.

Pairwise Maximin Share and α-PMMS Another fairness notion considered in this work is the PMMS introduced by (Caragiannis et al. 2019). For two agents, the PMMS value is equal to MMS and hence it is not guaranteed to exist for two agents and general valuations. It is an open problem whether we can guarantee exact PMMS value for all agents when their valuations are additive. In (Caragiannis et al. 2019), it is shown that a PMMS allocation is also EFX if each item has a strictly positive value for both agents. They also show that an approximate 0.618-PMMS allocation always exists and establish that a PMMS allocation is also an 1/2-MMS allocation for additive valuations despite the fact that neither PMMS implies MMS nor the opposite. Later, in (Amanatidis, Birmpas, and Markakis 2018) proved that a PMMS allocation implies a 4/7-MMS allocation and also showed that a 0.5914-MMS approximation cannot always be guaranteed. For approximate PMMS, the best known result is 0.781 by (Kurokawa 2017) for additive valuations.

1-out-of-d MMS The 1-out-of-d fair notion (ordinal approximation) was introduced by (Budish 2011) and established the existence of 1-out-of-(n + 1)-MMS, by adding a small number of excess goods. For additive valuations the main open problem is the minimum d such that we can guarantee at least 1-out-of-d for all agents. It is known that a 1out-of-⌈4n/3⌉-MMS always exists (Akrami, Garg, and Taki 2023) which is the minimum such d known so far. Whether 1-out-of-(n + 1) MMS allocations always exist remains an open question. For more general valuations Hosseini, Searns and Segal showed that an exact 1-out-of-d MMS allocation may not exist under submodular valuations (Hosseini, Searns, and Segal-Halevi 2022) for any d ≥1 even for 2 agents. (Babaioff, Nisan, and Talgam-Cohen 2021) introduced the ℓ-out-of-d maximin share, which corresponds to the maximum value an agent can guarantee to herself if she partitions the items into d bundles and then is allocated the worst ℓof them. (Christodoulou et al. 2025) used ordinal approximation with n > d to obtain stronger results.

Graphical Valuations (Christodoulou et al. 2023) first studied the graphical model considering the EFX property and show that, while an EFX allocation exists for simple graphs, an EFX orientation is not guarantee to exist and deciding if it exists is NP complete. (Zhou et al. 2024) studied the graphs with mixed mana; items with either positive or negative value. (Zeng and Mehta 2024) showed that EFX orientations are not guaranteed to exist in graphs with chromatic number greater than 3, and they always exist when the chromatic number is at most 2. (Afshinmehr et al. 2024; Bhaskar and Pandit 2024; Sgouritsa and Sotiriou 2025; Deligkas et al. 2024; Hsu 2024; Blaˇzej et al. 2025; Misra and Sethia 2024) studied the existence of EFX and also the complexity of finding EFX orientations for additive and more general valuations in multi-graphs under special conditions i.e. bipartite graphs, length of the shortest cycle, bounded neighbors, multi-trees etc. (Misra and Sethia 2024) studied the graph model assuming binary valuations.

We also note that this graphical model has been studied in other settings, including machine scheduling (Ebenlendr, Krc´al, and Sgall 2014; Verschae and Wiese 2010) and mechanism design (Christodoulou, Koutsoupias, and Kov´acs 2021).

## 2 Preliminaries

In this section, we introduce the main concepts and notation. We consider the graphical valuation. In this model, there is a given undirected graph G = (V, E), where the vertices corresponds to a set of n agents V = {1,..., n} and the set of edges corresponds to a set E = {1,..., m} of m indivisible goods. Each vertex (agent) i is equipped with a valuation function vi: 2E →R+, where vi (X) is the value of agent i for the subset X ⊆E. An item e ∈E is irrelevant to agent i ∈V if for all subsets X ⊆E, it holds that vi(X ∪ {e}) = vi(X). If an item is not irrelevant for agent i, it is called relevant for agent i. The graph G = (V, E) induces a special structure for the valuations as follows; an edge e = (i, j) is only relevant to at most agents i and j7. We allow

7We allow the edge e to be irrelevant for one of these agents (say for agent j), but in this case this edge could be equally modeled by a self-loop e = (i, i).

16763

<!-- Page 4 -->

multiple edges between two agents i and j which we denote by Ei,j8, and we denote by Ei the set of all edges adjacent to agent i, i.e., Ei = S j Ei,j.

Valuations Classes. We consider valuation classes that are monotone, i.e., vi(S) ≤vi(T) whenever S ⊆T ⊆E and normalized i.e., vi(∅) = 0, for all i ∈V. We study separately several important classes of complement-free valuations, such as additive, XOS, and subadditive valuation functions which we define below. It is well known that these classes form a hierarchy, namely additive ⊊ XOS ⊊ subadditive. A valuation function v is

• additive, if v(S) = P g∈S v(g) for any S ⊆E.

• fractionally subadditive (a.k.a. XOS) if there exists a set of additive functions a1,..., ak such that v(S) = maxl∈[k] al(S) for any S ⊆E. • subadditive if v(S)+v(T) ≥v(S∪T) for any S, T ⊆E.

Allocations and Orientations. We are interested in allocating (a subset of) edges in E into n mutually disjoint sets X1,..., Xn, where Xi is the set of edges assigned to agent i. We denote the respective (partial) allocation by X = (X1,..., Xn). An allocation X is called a partition if S i∈V Xi = E and partial if S i∈V Xi ⊂E. An allocation X is an orientation if every edge is allocated to an agent for which it is relevant; that is, for each edge e = (i, j), it must hold e ∈Xi ∪Xj.

Fairness Notions. Here, we provide the definitions for the fairness notions that we consider. For a positive integer d, let P = (P1,..., Pd) be a partition of E into d parts (we also call it d-partition), and let Πd(E) be the set of all possible d-partitions of E.

We define the 1-out-of-d maximin share value of agent i, denoted by µd i (E), to be the maximum over all d-partitions of E, of the minimum value under vi of a part in the dpartition, i.e.

µd i (E) = max P ∈Πd(E)

d min j=1 vi (Pj).

Of special interest is the case of d = n which is known as the maximin share (MMS) value of agent i, denoted by µi(E):= µn i (E). When E is clear from the context, we use the simpler notation µd i and µi respectively. We are now ready to define the notion of (approximate) MMS allocations. Fix an α ∈(0, 1]. We call X = (X1,..., Xn) an α-out-of-d MMS allocation if vi (Xi) ≥ αµd i for all agents i. Of special interest is the case of d = n, and then X is called an α-MMS allocation. When α = 1, X is simply called an (exact) MMS allocation. Regarding MMS approximations, we can focus on orientations, since for every allocation there exists an equally good orientation.

Canonical Partitions. A partition P of E into d parts, which maximizes the mind j=1 vi (Pj) for agent i is called a 1-out-of-d MMS partition of agent i. Note that there may be

8We allow i = j, Ei,i for the case of possibly multiple selfloops and an agent i.

more than one such partition. We fix one (arbitrary) partition

ˆP d i and define the respective partition of the set Ei. We refer to this partition of Ei as the canonical 1-out-of-d partition MMS of agent i, denoted by Bd i =

Bd i,1, Bd i,2,..., Bd i,d

, where Bd i,t is the t-th canonical bundle 9 of agent i. When it is clear from the context, we drop all superscripts.

We also study the notion of pairwise MMS (PMMS) fairness10. An allocation X = (X1,..., Xn) is a pairwise MMS allocation if for every agent i vi (Xi) ≥ max j∈V \{i} µ2 i (Xi ∪Xj) =: PMMSi (X).

Note that the PMMS threshold depends on the allocation X. When the allocation X is clear from the context we will write PMMSi instead of PMMSi(X).

## 3 Additive Valuations

First, we focus on multi-graphs with additive agents. The main result of this section asserts that there is always an MMS orientation in multi-graphs. We present two different algorithms that both guarantee exact MMS together with an additional property. The first algorithm computes an orientation that is both MMS and PMMS 11 (Theorem 1), while the second computes an 1-out-of-3 (and thus exact MMS for n ≥3) (Theorem 2). The results are in contrast to the general (non-graphical) case where even for the case of 3 additive agents, exact MMS allocations need not exist (Kurokawa, Procaccia, and Wang 2018). We also construct instances showing the limitations of our algorithms. Due to space limitations, we moved the proofs of the theorems and counterexamples in the Appendix.

Theorem 1. In every multi-graph with n additive agents there exists an orientation which is MMS and also PMMS.

The results of Theorem 1 are nontrivial. In general instances, PMMS does not imply an MMS allocation, nor does the converse hold (Caragiannis et al. 2019). The implications are even stronger, as there exists an orientation that satisfies PMMS. This positive result does not hold for more general valuations.

The next theorem shows an alternative algorithm that achieves an 1-out-of-3 MMS orientation which, in the case of 3 or more agents, implies MMS.12

Theorem 2. In every multi-graph with n additive agents there exists an 1-out-of-3 MMS orientation.

9Since every agent i is only interested in relevant items in our setting, we have vi(ˆPi,t) = vi(ˆPi,t ∩Ei) = vi(Bi,t). Therefore, it is convenient to define the canonical bundles Bi,t, which contain only edges relevant to agent i.

10Note that PMMS does not imply EFX in the graph setting. 11We note that PMMS does not imply MMS in multi-graphs. In the Appendix we elaborate on the relation between fair notions.

12Recall that when d < n, the existence of a 1-out-of-d MMS allocation is more restrictive than in general harder to achieve. Indeed, in Appendix we remark that the algorithm of Theorem 1 cannot guarantee 1-out-of-d MMS for any d < n.

16764

<!-- Page 5 -->

## 4 XOS Valuations

In this section, we study multi-graphs with agents having XOS valuations. First, we provide our tools which are of independent interest. Then, we study as a warm up the case of few agents and show the existence of an (1 −1/d)-out-of-d MMS for n ≤3 (Theorem 3). Our main result demonstrates the existence of a 2/3-MMS orientation in multi-graphs with three or more agents (Theorem 4). This separates the graphical model from the non-graphical model, for which a 1/2 upper bound is known (Ghodsi et al. 2022).

We complement this positive result with impossibility results (upper bounds) in Section 4.3 for any number of agents and any number of bundles. Specifically, we prove upper bounds of 2/3-MMS for three and four agents and for more agents, we show an upper bound of an

1 − 1 ⌈n/2⌉+1

- MMS (Theorem 6). Moreover, in the same theorem, we provide upper bounds for two and three agents with d bundles matching the corresponding lower bounds. For both the upper and lower bounds, we employ tools from combinatorics, particularly the theory of transversal independent sets in multipartite graphs.

We also focus on α-out-of-d MMS approximations for small values of d, independent of n. Analogous to the 1-outof-3 result for additive valuations (Theorem 2), we show that a modified version of the algorithm used in that proof can be adapted for XOS agents, achieving a 1/2-out-of-2 MMS for n agents (Theorem 5). This guarantee is optimal for the MMS notion in the graphical setting Theorem 6.

For the PMMS notion, we show the existence of a tight 1/2-PMMS orientation. The same result also holds for subadditive valuations so its presentation is deferred to Section 5 i.e. the lower bound holds for the general class of subadditive valuations while the impossibility result of the upper bound is shown by construction with XOS valuations. We note that in our construction for the upper bound there exists a PMMS allocation while we cannot guarantee more than (1/2 + ε)-PMMS orientation, showing that the fair notion is wasteful i.e. in order to guarantee fairness we must allocate the items in a suboptimal way. Due to space limitations, we moved some of the proofs to Appendix.

## 4.1 Our Tools

In this section, we present two lemmas and a definition that are essential to our analysis. We believe that our approach is of independent interest and may find its applications in future work. The following definition introduces a special type of partial allocation, which we call frugal, as it assigns each agent subsets from only one of the 1-out-of-d MMS bundles; it never combines items from different MMS bundles. Definition 1. Let Bd =

Bd

1,..., Bd n be the vector of the canonical 1-out-of-d MMS partitions. An allocation X is said to be frugal with respect to Bd if for all i there exists a ti ≤d such that Xi ⊆Bd i,ti. For simplicity, we refer to an allocation as frugal (omitting Bd), with the understanding that this refers to the canonical partition vector Bd. A frugal allocation may be partial; however, assigning the remaining edges arbitrarily (e.g., orienting them randomly) does not affect the approximation factor of the allocation, as 1-out-of-d MMS fairness guarantees are preserved due to monotonicity.

The following normalization approach, which has been noted in the literature for MMS and XOS valuations (see, e.g., (Ghodsi et al. 2022)), allows us to assume (by appropriate rescaling) that an agent’s 1-out-of-d MMS bundles all have equal value. We provide a proof sketch for completeness. Lemma 1. If there exists an α-out-of-d MMS allocation for normalized graphical XOS valuations, where vi(Bi,t) = 1 and vi(S) ≤1, ∀S ⊆E for each agent i and each canonical bundle Bi,t, then there exists an α-out-of-d MMS allocation for graphical XOS valuations.

In light of Lemma 1, we assume for the rest of this section that all values are normalized; that is, µd i = 1 for all i ∈ V, and for the canonical 1-out-of-d MMS partition Bd i = (Bi,1,..., Bi,d) of agent i, we have vi(Bi,t) = 1, t ≤d.

The next Lemma establishes a useful property of frugal allocations for agents with XOS valuations, and its applicability extends beyond graphical instances. The Lemma state that it suffices to assume additive valuation functions and frugal allocations for XOS agents (in general). Lemma 2. The instance with n XOS agents admits an αout-of-d MMS allocation if and only if the instance with n additive agents admits a frugal α-out-of-d MMS allocation.

## 4.2 Lower Bounds

As a warm up, for the case of two and three agents we show that there always exists a frugal (1 −1/d)-out-of-d MMS allocation, for any d ≥1. This is used as a building block for the proof of the main result for many agents. In Theorem 6 we show that the results of Theorem 3 are tight. The proof of the theorem as well as the figures are moved to Appendix due to space limitations. Theorem 3. In every multi-graph with n ≤3 XOS agents there exists a frugal (1 −1/d)-out-of-d MMS orientation.

Next, we present our main result, asserting that there always exists a 2/3-MMS allocation for n ≥3. Theorem 4. In every multi-graph with 3 or more XOS agents there exists a 2/3-MMS orientation.

Proof. Let G = (V, E) be a graph with n ≥3 vertices, and let Bn i = (Bi,1,..., Bi,n) denotes the canonical MMS partition of agent i for the edge set Ei. For some k ≤n, let Ii(k) ⊆{1, 2,..., n} be a subset of k indices, i.e., |Ii(k)| = k. We define Bi(Ii(k)) as the set of the respective bundles Bi,t with t ∈Ii(k) i.e. Bi(Ii(k)) = {Bi,t | t ∈Ii(k)}.

We will employ Lemma 2, that asserts that it suffices to show that there exists a 2/3-MMS frugal allocation in every multi-graph with n ≥3 additive agents. We will show by induction on k ∈{3,..., n}, that for every subset P = {p1,..., pk} ⊆V of k agents and for any fixed collection of k sets Ip1(k),..., Ipk(k), of indices of size k there exists a frugal orientation X with respect to Bk = (Bp1(Ip1(k)),..., Bpk(Ipk(k))) such that vpi(Xpi) ≥ 2 3 mint∈Ipi(k){vpi(Bpi,t)} ≥ 2 3, ∀pi ∈P. Note that every frugal allocation with respect to bundles

16765

<!-- Page 6 -->

Bpi(Ipi(k)) for some agent pi ∈P and set of k indices Ipi(k) is also frugal with respect to the canonical partition Bn pi. Furthermore, observe that for k = n we have P = V. Thus for each agent i ∈V we have vi(Xi) ≥

2 3 mint∈Ii(n){vi(Bi,t)} ≥2 3V and the theorem follows. By Theorem 3 we have already established the base case of n = 3. Now, assume that the statement holds for all subsets P = {p1,..., pk} ⊂V of k agents and for all corresponding vectors of k subsets of k indices Ip1(k),..., Ipk(k), with 3 ≤ k < n. We now show that the statement also holds for all possible subsets P = {p1,..., pk+1} ⊆V of k+1 agents and for all possible vectors of k +1 subsets of indices Ip1(k +1),..., Ipk+1(k +1). W.l.o.g. we will establish the induction step for subset P = {1,..., k+1} and set of indices Ii(k+1) = {1,..., k+1}, for all i ∈{1,..., k + 1}; then, clearly, the statement holds for any other subset of agents and any other vector of indices of size k + 1 by appropriate renaming of agents and indices.

We divide the proof of the induction step into two key claims. Claim 1, using the inductive hypothesis, outlines the necessary conditions for the case of k + 1 agents when no 2/3-MMS frugal orientation exists. Definition 2 summarizes these conditions in terms of what we call an overconstrained set. Claim 2 shows that overconstrained sets reveal useful structural properties in the intersections of canonical bundles, and uses this structure to construct a 2/3-MMS orientation. Due to space limitations, we moved the proof to Appendix. We now proceed with the definition of an overconstrained set.

Definition 2 (Overconstrained set). Let P = {1,..., k +1} be a set of k + 1 agents and Ii(k + 1) = {1,..., k + 1}, with i ∈P be k + 1 subsets of indices. We say that set P is overconstrained if for every subset P \ {i} of k agents, there exist two 2/3-MMS frugal orientations X(i), X′(i) such that

X(i)

j ∩X′(i)

j = ∅, ∀j ∈P \ {i} and vi

Bi,ti ∩

X(i) ∪X′(i)

≥2/3, ti ∈{1,..., k + 1}.

(1)

Claim 1. Let P = {1,..., k+1} be a set of k+1 agents and Ii(k + 1) = {1,..., k + 1}, with i ∈P be k + 1 subsets of indices. Either (i) there exists a frugal 2/3-MMS orientation for agents in P, or (ii) P is overconstrained.

We denote by Si,ti the high value intersections of an overconstrained set, Si,ti = Bi,ti∩

X(i) ∪X′(i)

for each agent i ∈P and ti ∈{1,..., k + 1}. Notably, due to the frugality, each bundle Si,ti intersects with exactly two canonical MMS bundles of any other agent j ∈P \ {i}; with (i) the bundle Bj,tj such that X(i)

j ⊆Bj,tj and (ii) the bundle Bj,t′ j such that X′(i)

j ⊆Bj,t′ j. Symmetrically, each bundle Sj,tj intersects with exactly two MMS bundles of agent i.

We say that bundle Si,ti intersects with bundle Sj,tj if and only if X(i)

j ⊆Bj,tj or X′(i)

j ⊆Bj,tj and additionally

X(j)

i ⊆Bi,ti or X′(j)

i ⊆Bi,ti. By definition, for each pair of agents there are exactly four such intersections.

In the next claim, we show that for |P| ≥5, we can allocate to each agent i ∈P some bundle Si,ti in a feasible way, i.e., the bundles will not intersect and achieve 2/3-MMS frugal orientation. We emphasize that for the special case of |P| = 4, such an orientation need not exist (i.e. allocate a bundle Si,ti to each agent i in a feasible way). In this case, we show that if such an orientation is not possible, we can redistribute the edges in the Si,ti sets and still achieve a 2/3- MMS frugal orientation.

Claim 2. If P is overconstrained and has 5 or more agents, then, a greedy approach admits a 2/3-MMS allocation X = (X1,..., Xk+1) such that for every agent i, the allocated bundle satisfies Xi = Si,ti for some ti ∈Ii(k + 1). If |P| = 4, then we can use a special treatment and achieve 2/3-MMS frugal orientation.

Claim 2 proves the inductive hypothesis and hence completes the proof. Due to the space limitations, we move the proof to Appendix. Here, we present a simpler proof of a slightly weaker statement, which is of particular interest when |P| ≥15. The existence of such an allocation can be established through an interesting connection to the theory of independent transversal sets in r-partite graphs. An independent transversal set is a selection of r vertices, one from each part, such that no two vertices share an edge.

An overconstrained set P can be modeled by a |P|-partite graph. Part i consists of k + 1 vertices corresponding to the Si,ti sets. An edge (vi,ti, vj,tj) represents the intersecting bundles Si,ti and Sj,tj. Because overlapping bundles cannot be assigned simultaneously to their respective agents, the goal is to find an independent transversal set. We claim that, using Corollary 10 of (Wanless and Wood 2022), existence can be established for |P| ≥15.

Lemma 3 ((Wanless and Wood 2022)). Fix any t ≥1. For a graph G, let V1,..., Vn be a partition of V (G) such that |Vi| ≥t and there are at most t

4|Vi| edges in G with exactly one endpoint in Vi for each i ∈{1,..., n}. Then there exists at least (t

2)n independent transversal of V1,..., Vn.

Indeed, by setting t = |P| and n = |P| we observe that when |P| ≥15, the conditions of Lemma 3 are satisfied for the graph that models the overconstrained set, which guarantees the existence of an independent transversal set and, consequently, a 2/3-MMS frugal orientation.

Next, we show that a 1/2-out-of-2 MMS orientation exists for n XOS agents. This result is tight, due to the upper bound of (Ghodsi et al. 2022) for two agents, which can extend by adding n−2 disconnected vertices. The tightness can be also derived from the more general Theorem 6.

Theorem 5. In every multi-graph with n XOS agents, there exists a 1/2-out-of-2 MMS orientation.

## 4.3 Upper Bounds

In this section, we present impossibility results for n agents and d bundles. For the special case of d = n, the following upper bound complements the positive results of Theorem 4 and provides a tight 2/3 MMS guarantee for the case of 3

16766

<!-- Page 7 -->

and 4 agents. Moreover, for n ∈{2, 3} the upper bounds match the lower bounds established in Theorem 3 while for d = 2, they match the bounds from Theorem 5. Theorem 6. A (1 −1/∆n(d) + ε)-out-of-d MMS allocation in multi-graphs with n XOS agents is not guaranteed to exist for any ε > 0 where

∆n(d) =

(

⌈ n−1 2(n−2)d⌉ if n is odd ⌈ n 2(n−1)d⌉ if n is even

In particular, a

1 − 1 ⌈n/2⌉+1 + ε

-MMS allocation for n XOS agents, is not guaranteed to exist for any ε > 0.

Proof. We construct a counterexample for n agents. The valuations are defined such that a single edge has one of two possible values, i.e., vi(e) ∈{0, 1/b} for b = ∆n(d). The construction ensures that, if an agent i receives a bundle Xi satisfying vi(Xi) ≥1 −1/∆n(d) + ε for some ε > 0, then she receives a whole canonical bundle i.e. Xi = Bi,t∗ i for some t∗ i ≤d. However, the structure of the edges prevents all agents from simultaneously achieving this condition, proving that no allocation can guarantee an approximation factor strictly greater than 1 −1/∆n(d).

We show this argument using a combinatorial result on independent transversals. In (Szab´o and Tardos 2006), Construction 3.3 is shown that for given integers k, d and b, with b ≥ l kd 2k−1 m

= ∆n(d), there exists a construction of a 2kpartite graph G2k with partition P = {V1,..., V2k}, where |Vi| = d, and maximum degree at most b such that no independent transversal exists. Later, in (Haxell and Szab´o 2006) it is proved that the same maximum degree also holds for n = 2k −1 parts i.e. if b ≥ l

(2k−1)d 2(2k−2) m

= ∆n(d), there exists a construction of a (2k −1)-partite graph G2k−1 with partition P = {V1,..., V2k−1} and |Vi| = d, and maximum degree at most b such that no independent transversal exists.

In the rest of the proof we show that the absence of an independent transversal in the 2k-partite graph implies an upper bound of (1−1/b)-out-of-d MMS for an even number of agents n = 2k and the same analysis also holds for an odd number of agents n = 2k −1. Thus, we can set b = ∆n(d) ensuring the desired upper bound.

Let G = (V, E) be a graph with 2k agents and a set of edges E. Consider the constructed 2k-partite graph G2k of (Szab´o and Tardos 2006), Construction 3.3 of maximum degree at most b, together with a vertex set partition into 2k disjoint subsets V1,..., V2k of size |Vi| = n = 2k, i ∈ {1,..., 2k} with Vi = {vi,1,..., vi,2k}. We associate every edge (vi,ti, vj,tj) in G2k with an edge e(i, ti, j, tj) = (i, j) in G. For each vertex vi,ti in graph G2k with degree d(vi,ti) < b we additionally add b −d(vi,ti) self-loops e(i, ti, i, ti) = (i, i). We denote the additive functions ai∗,t∗ i (e(i, ti, j, tj)) =

1/b, if i = i∗and ti = t∗ i 0, otherwise that is, ai∗t∗(e) = 1/b if and only if edge e corresponds to an edge connecting vertex vi∗,t∗ i in G2k (or to a corresponding self loop). We denote the valuation vi(S) = maxt≤d{ai,t(S)}, S ⊆E of agent i which is XOS i.e. maximum over additive. For each agent i, there are exactly n disjoint bundles of edges Bi,ti, ti ∈{1,..., d}, with value 1, namely Bi,ti = n e(i, ti, j, tj): j > i, tj ∈

{1,..., d}

o

∪ n e(j, tj, i, ti): j < i, tj ∈{1,..., d}

o

. By construction, each set Bi,ti has exactly b edges.

The partition Bi = (Bi,1,..., Bi,d) is the unique 1out-of-d MMS partition for agent i, with µd i (E) = 1. To see this, suppose there exists another MMS partition X = (X1,..., Xd) such that vi(XtX) = 1 for every tX, but X is not a reordering of Bi. Then, for every tX ∈{1,..., d}, there exists some Bi,t such that Xt ⊇Bi,t with the containment being strict for at least some t∗, but this is impossible.

Now, assume there exists a X = (X1,..., Xd) (1 −1/b + ε)-MMS allocation. By construction, for each agent i, there must exist a bundle Bi,t∗ i ⊆Xi i.e. agent i receives all edges e ∈Bi,t∗ i. Let (B1,t∗

1,..., Bn,t∗ n) be the set of MMS bundles allocated wholly to agents in X. Since such an allocation exists, no edge can be assigned to more than one agent which admits Bi,t∗ i ∩Bj,t∗ j = ∅for all allocated pairs (Bi,t∗ i, Bj,t∗ j). By construction, each MMS bundle corresponds to a vertex in G2k, and each shared edge among these bundles corresponds to an edge in G2k. Consequently, the existence of such an allocation would imply the existence of an independent transversal in G2k —a contradiction to the result of (Szab´o and Tardos 2006).

## 5 Subadditive Valuations

In this section, we establish that for multi-graphs with subadditive valuations, there always exists a 1/2-MMS allocation, and this guarantee is tight (Theorem 7). In the general (non-graphical) setting, the best previously known lower bound was 1/(log log n), as shown by (Feige 2025), while an upper bound of 1/2 was established in (Ghodsi et al. 2022). We complete the landscape for subadditive valuations showing that the algorithm described in Theorem 1 guarantees a tight 1/2-PMMS orientation for both XOS and subadditive agents. Due to space limitations, we moved the proofs of the two theorems to Appendix. Theorem 7. In every multi-graph with n subadditive agents there exists 1/2-MMS orientation. Furthermore, an (1/2 + ε)-MMS allocation is not guaranteed to exist, for any ε > 0. Theorem 8. In every multi-graph with n subadditive agents, there exists a 1/2-MMS orientation. However, there exists a graph with XOS agents where there is not a (1/2+ε)-PMMS orientation for any ε > 0 while an exact PMMS allocation exists.

## Acknowledgments

The research project is implemented in the framework of H.F.R.I call “3rd Call for H.F.R.I.’s Research Projects to Support Faculty Members & Researchers” (H.F.R.I. Project Number:24896). This work has been partially supported by project MIS 5154714 of the National Recovery and Resilience Plan Greece 2.0 funded by the European Union under the NextGenerationEU Program.

16767

<!-- Page 8 -->

## References

Afshinmehr, M.; Danaei, A.; Kazemi, M.; Mehlhorn, K.; and Rathi, N. 2024. EFX Allocations and Orientations on Bipartite Multi-graphs: A Complete Picture. CoRR, abs/2410.17002. Akrami, H.; and Garg, J. 2023. Breaking the 3/4 Barrier for Approximate Maximin Share. CoRR, abs/2307.07304. Akrami, H.; Garg, J.; Sharma, E.; and Taki, S. 2023a. Simplification and Improvement of MMS Approximation. CoRR, abs/2303.16788. Akrami, H.; Garg, J.; and Taki, S. 2023. Improving Approximation Guarantees for Maximin Share. CoRR, abs/2307.12916. Akrami, H.; Seddighin, M.; Mehlhorn, K.; and Shahkarami, G. 2023b. Randomized and Deterministic Maximin-share Approximations for Fractionally Subadditive Valuations. CoRR, abs/2308.14545. Amanatidis, G.; Aziz, H.; Birmpas, G.; Filos-Ratsikas, A.; Li, B.; Moulin, H.; Voudouris, A. A.; and Wu, X. 2023. Fair division of indivisible goods: Recent progress and open questions. Artif. Intell., 322: 103965. Amanatidis, G.; Birmpas, G.; and Markakis, E. 2018. Comparing Approximate Relaxations of Envy-Freeness. CoRR, abs/1806.03114. Amanatidis, G.; Markakis, E.; Nikzad, A.; and Saberi, A. 2017. Approximation Algorithms for Computing Maximin Share Allocations. ACM Trans. Algorithms, 13(4): 52:1– 52:28. Babaioff, M.; Nisan, N.; and Talgam-Cohen, I. 2021. Competitive Equilibrium with Indivisible Goods and Generic Budgets. Math. Oper. Res., 46(1): 382–403. Barman, S.; and Krishnamurthy, S. K. 2020. Approximation Algorithms for Maximin Fair Division. ACM Trans. Economics and Comput., 8(1): 5:1–5:28. Ben-Uziahu, G.; and Feige, U. 2023. On Fair Allocation of Indivisible Goods to Submodular Agents. CoRR, abs/2303.12444. Bhaskar, U.; and Pandit, Y. 2024. EFX Allocations on Some Multi-graph Classes. CoRR, abs/2412.06513. Blaˇzej, V.; Gupta, S.; Ramanujan, M. S.; and Strulo, P. 2025. Tractable Graph Structures in EFX Orientation. arXiv:2506.15379. Budish, E. 2011. The Combinatorial Assignment Problem: Approximate Competitive Equilibrium from Equal Incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The Unreasonable Fairness of Maximum Nash Welfare. ACM Trans. Economics and Comput., 7(3): 12:1–12:32. Chekuri, C.; Kulkarni, P.; Kulkarni, R.; and Mehta, R. 2023. 1/2 Approximate MMS Allocation for Separable Piecewise Linear Concave Valuations. CoRR, abs/2312.08504. Christodoulou, G.; and Christoforidis, V. 2025. Fair and truthful allocations under leveled valuations. Inf. Process. Lett., 190: 106577.

Christodoulou, G.; Christoforidis, V.; Mastrakoulis, S.; and Sgouritsa, A. 2025. Maximin Share Guarantees for Few Agents with Subadditive Valuations. arXiv:2502.05141. Christodoulou, G.; Fiat, A.; Koutsoupias, E.; and Sgouritsa, A. 2023. Fair allocation in graphs. In EC, 473–488. ACM. Christodoulou, G.; Koutsoupias, E.; and Kov´acs, A. 2021. Truthful allocation in graphs and hypergraphs. CoRR, abs/2106.03724. Deligkas, A.; Eiben, E.; Goldsmith, T.; and Korchemna, V. 2024. EF1 and EFX Orientations. CoRR, abs/2409.13616. Ebenlendr, T.; Krc´al, M.; and Sgall, J. 2014. Graph Balancing: A Special Case of Scheduling Unrelated Parallel Machines. Algorithmica, 68(1): 62–80. Feige, U. 2025. From multi-allocations to allocations, with subadditive valuations. arXiv:2506.21493. Feige, U.; and Grinberg, V. 2025. Fair allocations with subadditive and XOS valuations. CoRR, abs/2503.10513. Feige, U.; and Huang, S. 2025. Concentration and maximin fair allocations for subadditive valuations. CoRR, abs/2502.13541. Feige, U.; Sapir, A.; and Tauber, L. 2021. A tight negative example for MMS fair allocations. CoRR, abs/2104.04977. Garg, J.; and Taki, S. 2021. An improved approximation algorithm for maximin shares. Artif. Intell., 300: 103547. Ghodsi, M.; Hajiaghayi, M. T.; Seddighin, M.; Seddighin, S.; and Yami, H. 2021. Fair Allocation of Indivisible Goods: Improvement. Math. Oper. Res., 46(3): 1038–1053. Ghodsi, M.; Hajiaghayi, M. T.; Seddighin, M.; Seddighin, S.; and Yami, H. 2022. Fair allocation of indivisible goods: Beyond additive valuations. Artif. Intell., 303: 103633. Haxell, P. E.; and Szab´o, T. 2006. Odd Independent Transversals are Odd. Comb. Probab. Comput., 15(1-2): 193–211. Heinen, T.; Nguyen, N.; Nguyen, T. T.; and Rothe, J. 2018. Approximation and complexity of the optimization and existence problems for maximin share, proportional share, and minimax share allocation of indivisible goods. Auton. Agents Multi Agent Syst., 32(6): 741–778. Hosseini, H.; Searns, A.; and Segal-Halevi, E. 2022. Ordinal Maximin Share Approximation for Goods. J. Artif. Intell. Res., 74. Hsu, K. 2024. EFX Orientations of Multigraphs. CoRR, abs/2410.12039. Kulkarni, P.; Kulkarni, R.; and Mehta, R. 2023. Maximin Share Allocations for Assignment Valuations. In AAMAS, 2875–2876. ACM. Kurokawa, D. 2017. Fair Division in Game theoretic Settings. Ph.D. thesis, Carnegie Mellon University. Kurokawa, D.; Procaccia, A. D.; and Wang, J. 2018. Fair Enough: Guaranteeing Approximate Maximin Shares. J. ACM, 65(2): 8:1–8:27. Misra, N.; and Sethia, A. 2024. Envy-Free and Efficient Allocations for Graphical Valuations. CoRR, abs/2410.14272.

16768

<!-- Page 9 -->

Seddighin, M.; and Seddighin, S. 2024. Improved maximin guarantees for subadditive and fractionally subadditive fair allocation problem. Artif. Intell., 327: 104049. Sgouritsa, A.; and Sotiriou, M. M. 2025. On the existence of EFX allocations in multigraphs. CoRR, abs/2502.09777. Szab´o, T.; and Tardos, G. 2006. Extremal Problems For Transversals In Graphs With Bounded Degree. Comb., 26(3): 333–351. Verschae, J.; and Wiese, A. 2010. On the Configuration- LP for Scheduling on Unrelated Machines. CoRR, abs/1011.4957. Wanless, I. M.; and Wood, D. R. 2022. A General Framework for Hypergraph Coloring. SIAM Journal on Discrete Mathematics, 36(3): 1663–1677. Zeng, J. A.; and Mehta, R. 2024. On the structure of envyfree orientations on graphs. CoRR, abs/2404.13527. Zhou, Y.; Wei, T.; Li, M.; and Li, B. 2024. A Complete Landscape of EFX Allocations on Graphs: Goods, Chores and Mixed Manna. In IJCAI, 3049–3056. ijcai.org.

16769
