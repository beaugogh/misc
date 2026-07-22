---
title: "Approximately Envy-free and Equitable Allocations of Indivisible Items for Non-monotone Valuations"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38712
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38712/42674
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Approximately Envy-free and Equitable Allocations of Indivisible Items for Non-monotone Valuations

<!-- Page 1 -->

Approximately Envy-free and Equitable Allocations of Indivisible Items for Non-monotone Valuations

Vittorio Bil`o1*, Martin Loebl2*, Cosimo Vinci1*

1Department of Mathematics and Physics “Ennio De Giorgi”, University of Salento, Lecce, Italy. 2Department of Applied Mathematics, Charles University, Prague, Czech Republic. vittorio.bilo@unisalento.it, loebl@kam.mff.cuni.cz, cosimo.vinci@unisalento.it

## Abstract

We revisit the setting of fair allocation of indivisible items among agents with heterogeneous, non-monotone valuations. We explore the existence and efficient computation of allocations that approximately satisfy either envy-freeness or equity constraints. Approximate envy-freeness ensures that each agent values her bundle at least as much as those given to the others, after some (or any) item removal, while approximate equity guarantees roughly equal valuations among agents, under similar adjustments. As a key technical contribution of this work, by leveraging fixed-point theorems (such as Sperner’s Lemma and its variants), we establish the existence of envy-free-up-to-one-good-and-one-chore (EF1c g) and equitable-up-to-one-good-and-one-chore (EQ1c g) allocations, for non-monotone valuations that are always either non-negative or non-positive. These notions represent slight relaxations of the well-studied envy-free-up-to-oneitem (EF1) and equitable-up-to-one-item (EQ1) guarantees, respectively. Our existential results hold even when items are arranged in a path and bundles must form connected sub-paths. The case of non-positive valuations, in particular, has been solved by proving a novel multi-coloring variant of Sperner’s Lemma that constitutes a combinatorial result of independent interest. In addition, we also design a polynomial-time dynamic programming algorithm that computes an EQ1c g allocation. For monotone non-increasing valuations and path-connected bundles, all the above results can be extended to EF1 and EQ1 guarantees as well. Finally, we provide existential and computational results for certain stronger up-to-any-item equity notions under objective valuations, where items are partitioned into goods and chores.

## Introduction

Fair division (Steinhaus 1948), the field that studies how to fairly allocate resources among a set of agents, has numerous applications across a variety of real-life scenarios, such as divorce settlements, credit assignment, and rent and land division, to name a few. Although fair division has been studied for decades in mathematics and economics, the field has attracted increasing attention from the computer science and AI community in recent years, driven by the flourishing of new fairness concepts and the demand for computation-

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

ally efficient solutions overcoming the inherent impossibility of achieving optimal fairness guarantees.

Two prominently investigated notions of fairness are envy-freeness (Foley 1966) and equitability (Dubins and Spanier 1961). An allocation (of items to agents) is envyfree (EF) if the value that every agent gives to her assigned bundle (of items) is not less than the value she gives to the bundle assigned to any other agent; it is equitable (EQ) if the value that every agent gives to her assigned bundle is not less than the value that the other agents assign to their respective bundles. So, the two notions coincide when agents have identical valuations.

The nature of valuation functions tremendously impacts the solution of a fair division problem. When an agent’s valuation is monotone non-decreasing (resp., non-increasing), items are said to be goods (resp., chores) for the agent; when it is non-monotone, items are said to be mixed. Notable special cases of non-monotone valuations include non-negative (resp. non-positive) valuations, where every bundle yields a non-negative (resp. non-positive) value, and objective valuations, in which items can be partitioned into goods and chores. Valuations, either monotone or non-monotone, are additive when the value of a bundle is defined by the sum of the values of its items. Finally, we implicitly assume that, for every valuation function considered, the empty bundle has value zero. While objective valuations have been widely studied (Aziz et al. 2022; Barman et al. 2024), less work has been done for non-negative or non-positive ones, despite their potential applicability in numerous settings. These valuations, for instance, arise when items correspond to nodes in an edge-weighted graph with exclusively positive or negative weights, allocations are interpreted as clusterings, and the value of each bundle/cluster is then determined by factors such as the total weight of internal or cut edges, or other graph-connectivity properties. This class of settings has interesting connections with clustering problems where further fairness guarantees are required (see, e.g., (Dinitz et al. 2022; Chierichetti et al. 2017; Schwartz and Zats 2022)). Either envy-free or equitable allocations are guaranteed to exist under non-negative or non-positive valuations in the setting of divisible items, where items can be arbitrarily split among subsets of agents (Dubins and Spanier 1961; Stromquist 1980). In contrast, in the presence of indivisible items which have to be integrally assigned to any of

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16700

<!-- Page 2 -->

the agents, existence cannot be guaranteed even for two agents with additive monotone valuations. To overcome this limitation, a number of relaxations have been proposed in the literature. They allow the removal of one item from a bundle when agents perform bundle comparisons. The removal strategy clearly depends on the nature of the considered items. When an agent compares her bundle A against another bundle B, she can choose between removing a chore from A or removing a good from B. These relaxations have given rise to the notions of envy-freeness-upto-any-good (EFX) (Caragiannis et al. 2019), envy-freenessup-to-one-good (EF1) (Lipton et al. 2004; Budish 2011), equitability-up-to-any-good (EQX) (Gourv`es, Monnot, and Tlilane 2014) and equitability-up-to-one-good (EQ1) (Freeman et al. 2019). By up-to-any-good, one means that the fairness property holds irrespectively of which item is selected for removal; by up-to-one-good, instead, the property must hold for at least one removed item. Clearly, fairness up-to-any-good implies fairness up-to-one-good.

An interesting and largely studied generalization of fair division assumes the existence of an item graph modeling proximity relationships among items. Every bundle has to induce a connected subgraph and an item removal is allowed only if it does not disconnect the induced subgraph (Bouveret et al. 2017; Bil`o et al. 2022; Igarashi 2023; Misra et al. 2021; Suksompong 2019). In this respect, the path constraint assumes that the item graph is a connected path.

Our Contribution. Given the lack of positive results for non-monotone valuations under standard approximate fairness notions, often due to impossibility barriers (see, e.g., (Amanatidis et al. 2023; Barman et al. 2024)), we study slight relaxations of EF1, EQ1 and EQX, denoted by EF1c g (envy-free-up-to-one-good-and-onechore), EQ1c g (equitable-up-to-one-good-and-one-chore), and EQXc g (equitable-up-to-any-good-or-any-chore), respectively. While EF1 and EQ1 require the envy-freeness and equitability properties, respectively, to hold upon the removal of at most one item from “some” bundle, EF1c g and EQ1c g allow the properties to hold when removing at most one item from “each” bundle (i.e., for each agent, at most one chore from her own bundle and at most one good from others’ bundles). Similarly, while EQX requires the equitability property to hold regardless of which item is removed (i.e., whether it is a good or a chore), EQXc g allows it to hold for the removal of either goods only or chores only. We obtain positive results on the existence and computation of allocations satisfying the above fairness criteria across several broad classes of non-monotone valuations.

## Results

for non-negative or non-positive valuations: Our main contribution concerns the existence and computation of allocations which are fair up-to-one-good-and-one-chore, under non-negative or non-positive valuations. In particular, we show that an EQ1c g allocation always exists and can be computed in polynomial time, for both non-negative (Theorem 3.3 and 3.4) and non-positive valuations (Theorem 4.2). For EF1c g allocations, we only show existence (Theorem 3.5 and Theorem 4.3). The existence and computation of approximately envy-free or equitable allocations under non- monotone valuations is one of the major open problems in fair division (see, e.g., the surveys by Amanatidis et al. (2023); Liu et al. (2024)). Our results represent a significant step forward in this direction, due to the generality of the non-monotone valuations we consider (either non-negative or non-positive) and the fairness guarantees achieved (requiring the removal of at most one good and one chore).

It is worth noting that our results continue to hold even under path constraints, and in this sense, they generalize the findings of Bil`o et al. (2022); Igarashi (2023); Misra et al. (2021); Suksompong (2019), which apply only to monotone non-decreasing valuations, and the results of Bouveret et al. (2017); Bouveret, Cechl´arov´a, and Lesca (2019), which address the computational problem of finding EF and EQ allocations (that, in general, may not exist). Our existential results are obtained using Sperner’s Lemma (Sperner 1928) or its variants, and represent a non-trivial generalization of the approaches previously explored in (Bil`o et al. 2022; Igarashi 2023), as handling the non-monotonicity of the valuations poses significant technical challenges (such as the derivation and analysis of the cases described in Figure 1). In particular, to address the specific case of non-positive valuations, we introduce and exploit a novel multi-coloring variant of Sperner’s Lemma (Theorem 4.1), that constitutes a combinatorial result of independent interest. The computational results have been obtained by means of the dynamicprogramming paradigm. Finally, when valuations are monotone (non-decreasing or non-increasing), our results extend to the stronger EQ1 and EF1 guarantees under path constraints, thereby generalizing the results of Igarashi (2023); Bil`o et al. (2022); Misra et al. (2021), which exhibit EF1 and EQ1 allocations under monotone non-decreasing valuations and path constraints.

## Results

for objective valuations: To complete the picture for non-monotone valuations, we also consider fair allocations under objective valuations, and in most cases the obtained results hold even under the up-to-any-good-or-anychore approximation guarantee. In particular, we show that an EQXc g allocation always exists and can be computed in pseudopolynomial time, via a simple variant of the localsearch approach adopted by Barman et al. (2024). This result extends to EQX when valuations are monotone nonincreasing, thereby generalizing the result of Barman et al. (2024), which holds only for monotone non-decreasing valuations. For valuations that are both objective and additive, we strengthen the above computational result by showing that an EQXc g allocation can be found through a simple and more efficient greedy algorithm. This result strengthens the findings of Hosseini and Sethia (2025), who establish existence and polynomial-time computability of EQ1 allocations under additive objective valuations. We also show that a slight generalization of the polynomial-time algorithm proposed by Hosseini and Sethia (2025), continues to produce EQ1 allocations even for non-additive objective valuations1. We note that, just as EQXc g is considered a relaxation of EQX, similar relaxations for EFX have been studied for

1The EQ1 algorithm of Hosseini and Sethia (2025) and the algorithms employed in this work were developed independently.

16701

<!-- Page 3 -->

objective (Hosseini et al. 2023) or identical non-monotone valuations (B´erczi et al. 2024). However, these works only show non-existence of these relaxed notions.

Due to the lack of space, most technical details on nonnegative and non-positive valuations, as well as all missing proofs, are deferred to the full arXiv version of this work (Bil`o, Loebl, and Vinci 2025), while all results on objective valuations are moved to the full version. Table 1 summarizes our results, related work and cases that remains unsolved.

Further Related Work. Lipton et al. (2004) show that an EF1 allocation always exists and can be efficiently computed for non-decreasing valuations. Their result has been extended to objective valuations by Aziz et al. (2022); Bhaskar, Sricharan, and Vaish (2021); B´erczi et al. (2024). Again under objective valuations, (Hosseini and Sethia 2025) show existence and polynomial time computation of an EQ1 allocation; conversely, they show that under additive nonobjective valuations EQ1 allocations may not exist. Existence and computation of Pareto optimal EF1 or EQ1 allocations have been studied by Caragiannis et al. (2019); Freeman et al. (2019, 2020); Garg and Murhekar (2024). EF1 and EQ1 allocations under non-objective valuations have been determined for restricted cases only, and their general existence and computation is a major open problem (see surveys by Amanatidis et al. (2023); Liu et al. (2024)).

EQX allocations were first proved to exist for additive monotone non-decreasing valuations in (Gourv`es, Monnot, and Tlilane 2014). Efficient algorithms computing one have been later designed by Freeman et al. (2019, 2020), also covering the non-increasing case. Existence and pseudopolynomial time computation of an EQX allocation for monotone non-decreasing (and possibly non-additive) valuations has been shown in (Barman et al. 2024). This result is complemented by showing that, if one drops the monotonicity assumption, EQX allocations may not exist even for two agents with additive valuations. So, our results state that, slightly relaxing EQX to EQXc g suffices to recover existence under non-monotone objective valuations.

The EFX criterion was introduced by Caragiannis et al. (2019). Its existence under additive non-negative or nonpositive valuations has been addressed only in specific cases, and remains a major open problem in fair division (see surveys by Amanatidis et al. (2023) and Liu et al. (2024)). Whereas, for objective additive valuations (Hosseini et al. 2023) or chore valuations (Christoforidis and Santorinaios 2024), an EFX allocation might not exist. Plaut and Roughgarden (2020) show that an EFX allocation exists and can be efficiently computed for non-negative additive valuations when agents assign the same ranking to all items; this result has also been extended to additive objective valuations with equally ranked items (Aziz and Rey 2020). Restricting to identical valuations, EFX allocations are known to exist for additive non-decreasing valuations (Gourv`es, Monnot, and Tlilane 2014) and additive non-increasing valuations (Barman, Narayan, and Verma 2023), whereas they may not exist for non-monotone valuations (B´erczi et al. 2024).

Finally, additional relaxed notions of fairness have been investigated (e.g., in (Akrami et al. 2025; Akrami and Rathi

2025; Amanatidis, Markakis, and Ntokos 2020; Aziz et al. 2024; Bil`o, Markakis, and Vinci 2024; Caragiannis et al. 2023; Halpern and Shah 2019; Hoefer, Schmalhofer, and Varricchio 2024; Plaut and Roughgarden 2020)).

## 2 Model and Definitions

Let N = {1, 2,..., n} be a finite set of n agents and M be a finite set of m items. Each agent i ∈N has an integral valuation function vi: 2M →Z with vi(∅) = 0 for any i ∈N. We denote by I = (N, M, (vi)i∈N) an allocation instance. Given an agent i ∈N, a bundle of items S ⊆M and an item x ∈S, we say that x is a good (resp., a chore) for i w.r.t. S, if vi(S) ≥vi(S \{x}) (resp., vi(S) ≤vi(S \{x})). We observe that an item x for which vi(S) = vi(S \ {x}) is both a good and a chore for i w.r.t. S. An item x is a good (resp., a chore) if it is a good (resp., a chore) for any agent i ∈N w.r.t. any bundle S ⊆M. An allocation A = (A1,..., An) is a partition of M into n (possibly empty) bundles of items, such that Ai is the bundle assigned to agent i ∈N. We aim at finding allocations satisfying fairness criteria related to envy-freeness and equity, as described below.

Envy-freeness. An allocation A = (A1,..., An) is:

• envy-free (EF) if, for any i, j ∈N, vi(Ai) ≥vi(Aj); • envy-free-up-to-any-item (EFX) if, for any i, j ∈N such that vi(Ai) < vi(Aj), all the following conditions hold: (i) vi(Ai) ≥vi(Aj \ {g}) for any good g for agent i w.r.t. Aj; (ii) vi(Ai \ {c}) ≥vi(Aj) for any chore c for i w.r.t. Ai; (iii) either there exists a good g for i w.r.t. Aj, or there exists a chore c for i w.r.t. Ai; • envy-free-up-to-one-item (EF1) if, for any i, j ∈N such that vi(Ai) < vi(Aj), there exists x ∈Ai ∪Aj such that vi(Ai \ {x}) ≥vi(Aj \ {x}); • envy-free-up-to-one-good-and-one-chore (EF1c g) if, for any i, j ∈N such that vi(Ai) < vi(Aj), there exists a subset X ⊆M with |Ai ∩X| ≤1 and |Aj ∩X| ≤1, such that vi(Ai \ X) ≥vi(Aj \ X).

Under EF1c g allocations, agent i stops envying agent j after removing at most one chore from Ai and at most one good from Aj, possibly two items in total. In contrast, under EF1 (resp. EFX), agent i stops envying agent j after removing at most one (resp. any) envy-reducing item from Ai ∪Aj. We observe that EF ⇒EFX ⇒EF1 ⇒EF1c g.

Equitability. The equitability notions we consider are analogous to the envy-freeness criteria described above, but the comparison each agent i makes is not against the valuation vi(Aj) that she assigns to the bundle given to any other agent j, but rather against the valuation vj(Aj) that agent j assigns to her own bundle. This naturally leads to the definitions of equitable (EQ), equitable-up-to-anyitem (EQX), equitable-up-to-one-item (EQ1) and equitableup-to-one-good-and-one-chore (EQ1c g) allocations. In addition, we consider equitable-up-to-any-good-or-any-chore (EQXc g) allocations, a slight relaxation of EQX that, unlike EQX, allows the equitability to hold after the removal of either only goods or only chores. In particular, an allocation A

16702

<!-- Page 4 -->

EQ1c g EF1c g EQ1 EF1 EQXc g EQX EFX

Gen ✗a[HS25]?a ✗a[HS25]?a ✗a[HS25] ✗a[HS25] ✗a[HSVX23]

NNeg ✓cp ✓c?????a

NPos ✓cp ✓c???? ✗[CS24],?ao NDec ✓cp[MSVV21] ✓p[LMMS04], ✓c[I23] ✓cp[MSVV21] ✓p[LMMS04], ✓c[I23] ✓p-[BBPP24] ✓p-[BBPP24]?a

NInc ✓cp ✓p[BSV21], ✓c ✓cp ✓p[BSV21], ✓c ✓p- ✓p- ✗[CS24],?ao

Obj ✓p, ✓p ao[HS25] ✓p[BSV21] ✓p, ✓p ao[HS25] ✓p[BSV21] ✓p-, ✓p ao?a ✗a[HSVX23]

**Table 1.** Landscape of results for the considered fairness notions. Gen, NNeg, NPos, NDec, NInc, and Obj denote, respectively, General, Non-negative, Non-positive, Non-decreasing, Non-increasing, and Objective valuations. Gray-highlighted results indicate our contributions, whereas the short citations point to some previous works from which the other (non-highlighted) results follow. Symbols ✓, ✗, and? indicate, respectively, “always exists”, “does not generally exist”, and “open problem”. Subscript a (resp., ao) means that an ✗or? (resp., ✓or?) result holds even (resp., only) for additive valuations. Superscripts p and p- denote existence under polynomial and pseudopolynomial algorithms, respectively; c indicates that existence holds under path constraints, and cp means that existence under path constraints can be achieved in polynomial time. Although positive (resp., negative) results for some approximate notions of fairness are derived from stronger (resp., weaker) notions, we include repeated citations for completeness.

is EQXc g if, for any i ∈N, at least one of the following conditions holds: (i) for any j ∈N such that vi(Ai) < vj(Aj), there exists at least one good for j w.r.t. Aj, and for any such good g, vi(Ai) ≥vj(Aj \ {g}); (ii) if vi(Ai) < vj(Aj) for some j ∈N, there exists a chore for i w.r.t. Ai, and for any such chore c, vi(Ai \ {c}) ≥vj(Aj) holds for any j ∈N. We observe that EQ ⇒EQX ⇒EQXc g ⇒EQ1 ⇒EQ1c g.

Classes of Valuations. We consider the following classes of valuations: (i) Objective: any item x is either a good or a chore, independently of the agent and the bundle considered; in such a case, we can partition M into a set of goods G and a set of chores C (choosing arbitrarily how to classify dummy items that qualify as both); (ii) Non-negative (resp., Non-positive): vi(S) ≥0 (resp. vi(S) ≤0) for any i ∈N, S ⊆M; (iii) Monotone non-decreasing (resp., nonincreasing): each item x is a good (resp., a chore), independently of the agents and bundles considered; (iv) Additive: vi(S) = P x∈S vi(x) for any i, S ⊆M. We observe that monotone non-decreasing (resp. non-increasing) valuations are also non-negative (resp. non-positive) and objective. Finally, we assume the existence of an oracle that, given i ∈N and S ⊆M, returns vi(S) in constant time.

## 3 Non-negative Valuations

To address the case of non-negative valuations, we consider a generalization of the fixed-point approach employed in (Bil`o et al. 2022; Igarashi 2023), which is extended in a nontrivial manner to handle the peculiarities of these valuations.

Fairness under Path Constraints. We say that an allocation instance is path-constrained if the m items of M are numbered from 1 to m and organized as a path P = (1,..., m). Given s, t ∈[m] ∪{0}, let Js, tK denote the bundle {s, s + 1,..., t} if t ≥s, and the empty bundle otherwise. A bundle S is connected if S = Js, tK for some s ∈[m] and t ∈[m] ∪{0}. An allocation A is connected if it is made of connected bundles only. Given a connected bundle S = Js, tK, let ∂S = {s, t} denote the boundary of S (note that ∂S = S if |S| ≤2). For a given connected allocation A = (A1,..., An), we consider the following path-based notions of EF1c g and EQ1c g: A is envy-free-upto-one-good-and-one-chore-over-paths (EF1Pc g) if, for any i, j ∈N such that vi(Ai) < vi(Aj), there exists a subset X ⊆∂Ai ∪∂Aj with |∂Ai ∩X| ≤1 and |∂Aj ∩X| ≤1, such that vi(Ai \ X) ≥vi(Aj \ X); A is equitable-upto-one-good-and-one-chore-over-paths (EQ1Pc g) if, for any i, j ∈N such that vi(Ai) < vj(Aj), there exists a subset X ⊆∂Ai ∪∂Aj with |∂Ai ∩X| ≤1 and |∂Aj ∩X| ≤1, such that vi(Ai \ X) ≥vj(Aj \ X). Note that the notions of EFOP and EQ1Pc g respectively strengthen EF1c g and EQ1c g by ensuring that items are removed only from the boundary, so that bundles remain path-connected after the removal.

Sperner’s Lemma. Before presenting our results, we provide a brief overview of the underlying theoretical framework based on Sperner’s Lemma. For more details, see, for example, (Flegg 1974).

Let conv(v1, v2,..., vn) denote the convex hull of the n vectors v1, v2,..., vn. An (n −1)-simplex ∆is an (n − 1)-dimensional polytope defined as the convex hull of its n (affinely independent) vertices v1, v2,..., vn. Given k ∈ [n], a (k−1)-face of an (n−1)-simplex is the (k−1)-simplex obtained as convex hull of a subset of k −1 of its vertices. A triangulation T of a simplex ∆is a collection of sub-(k−1)simplices (with k ∈[n]) whose union is ∆, with the property that the intersection of any two sub-simplices in T is either empty or a face shared by both, which also belongs to T. Each sub-simplex ∆′ ∈T is referred to as an elementary simplex. The set of vertices of T, denoted as V (T), is the union of the vertices of all the elementary simplices in T (i.e., the union of all the elementary 0-simplices).

Now, let T be a fixed triangulation of an (n −1)-simplex ∆= conv(v1, v2,..., vn). A coloring function of T is a mapping L: V (T) →[n] that assigns a number, referred to as a color, from the set [n] to each vertex of T. A coloring function L is called special if, for any vertex x ∈V (T) belonging to the (n −2)-face Fi of ∆that does not include vi (i.e., the face opposite to vi, obtained as convex hull of all vertices of ∆except for vi), the condition L(x)̸ = i holds.

16703

<!-- Page 5 -->

We observe that, if L is a special coloring function, then L(vi) = i holds for any i ∈[n]. An elementary (n −1)simplex ∆∗= conv(x∗

1,..., x∗ n) ∈T is said to be fullycolored under a coloring function L if each of its n vertices is assigned a distinct color by L, that is, L(x∗ σ(i)) = i for any i ∈[n], for some permutation σ: [n] →[n].

Theorem 3.1 (Sperner’s Lemma (Sperner 1928)). Let T be a triangulation of an (n −1)-simplex ∆, where n ≥2, and let L be a special coloring function of T. Then, there exists a fully-colored elementary (n −1)-simplex ∆∗∈T under L; moreover, the number of such simplices is odd.

Below, we also consider a generalized version of Sperner’s Lemma, as presented by (Bapat 1989). In this generalized form, there are n special coloring functions L1,..., Ln, and we seek an elementary (n −1)-simplex that is fully-colored according to a broader definition, which holds simultaneously for all of the coloring functions. Let T be a triangulation of an (n −1)-simplex, and let L1,..., Ln be the coloring functions on T. An elementary (n −1)simplex ∆∗= conv(x∗

1, x∗ 2,..., x∗ n) ∈T is jointly fullycolored under L1,..., Ln if there exist two permutations σ, τ: [n] →[n] such that Li(x∗ σ(i)) = τ(i) for any i ∈[n], i.e., each vertex of ∆∗receives a distinct color under a distinct coloring function.

Theorem 3.2 (Generalized Sperner’s Lemma (Bapat 1989)). Let T be a triangulation of an (n −1)-simplex ∆, and let L1,..., Ln be special coloring functions of T. Then, there exists a jointly-fully-colored elementary (n −1)-simplex ∆∗∈T under L1,..., Ln.

EQ1Pc g Allocations

Given a path-constrained allocation instance I with nonnegative valuations, we construct a suitable triangulation T of an n-simplex ∆and define a special coloring L for T. Each elementary (n −1)-simplex ∆∗∈T that is fullycolored under L corresponds to an EQ1Pc g allocation for I. By Sperner’s Lemma (Theorem 3.1), the existence of such fully-colored simplices is guaranteed, which in turn ensures the existence of an EQ1Pc g allocation. We also design a polynomial-time algorithm, based on dynamic programming, that efficiently computes such an EQ1Pc g allocation.

Triangulation. Consider the (n −1)-simplex ∆ = {x = (x1,..., xn−1) ∈ Rn−1: 0 ≤ x1 ≤ x2 ≤... ≤xn−1 ≤m}, which is the convex hull conv(v1, v2,..., vn) of the points v1,..., vn, with vi:=

( i−1 z }| { 0, 0,..., 0, n−i z }| { m, m,..., m) for any i ∈[n]. We observe that each of the n (n −2)-faces of ∆can be defined as Fi:= {x = (x1,..., xn−1) ∈∆: xi−1 = xi}, where we set x0:= 0 and xn:= m. We construct a triangulation T of ∆whose set of vertices is V (T) = {x ∈∆: xi ∈ {0, 1

3, 2 3, 1, 4 3, 5 3, 2, 7 3,..., m −1, m −2 3, m −1 3, m} ∀i ∈ [n −1]} and whose simplicial structure is defined below. Each coordinate xi of vertices x ∈V (T) can be either integral, or 1-fractional or 2-fractional, where integral (resp. 1-fractional, 2-fractional) means xi ∈Z (resp. xi −1 3 ∈Z, xi −2

3 ∈Z); we write xi ≡0 (resp. xi ≡1, xi ≡2) if xi is integral (resp. 1-fractional, 2-fractional). By leveraging Kuhn’s triangulation (Kuhn 1960; Scarf 1982; Deng, Qi, and Saberi 2012), we construct the triangulation T such that each elementary (n −1)-simplex ∆′ = conv(x1, x2,..., xn) ∈ T can be generated by fixing the first vertex x1 ∈V (T) and a permutation π: [n −1] →[n −1], and then iteratively determining the remaining vertices as follows: xi+1 = xi + 1

3eπ(i) for each i ∈[n−1], where ei is the i-th vector of the canonical basis of Rn−1 (1 in the i-th position, and 0 elsewhere). Each vertex x ∈V (T) can be understood as a vector representing the positions of n −1 knives that divide the interval [0, m] into n connected segments having endpoints a, b ∈[0, m] ∩{ x

3|x ∈Z}. Following this interpretation, the n vertices of any elementary (n −1)-simplex in T are derived by starting with an initial configuration of n −1 cuts (i.e., vertex x1) and sequentially shifting each knife one position to the right (by a length of 1/3) according to a specific ordering defined by a permutation π.

Coloring Function. We now construct the coloring function L: V (T) →[n]. Given a vertex x = (x1,..., xn−1) ∈ V (T), let ˜ A(x) = (˜A1(x),..., ˜An(x)) be the fractional connected allocation obtained from the partition of [0, m] in n fractional connected bundles, defined as ˜Ai(x) = [xi−1, xi] for any i ∈[n], with x0:= 0 and xn:= m; furthermore, each bundle ˜Ai(x) is assigned by default to agent i, for any i ∈[n] (i.e., bundles are assigned from left to right following the agents order).

Given a ∈R≥0, let a−:= ⌊a⌋and a+:= min{⌊a⌋+ 1, m}. Let ˜vi denote the virtual valuation of agent i, which applies to fractional connected bundles [a, b] (where a, b ∈ [0, m] ∩{ x

3|x ∈Z} and a ≤b) and returns an integer value ˜vi([a, b]) that is defined as follows: left-value (LV): if a ≡0, ˜vi([a, b]):= vi(Ja−, b−K); borderline-value (BV): if a ≡1, ˜vi([a, b]) is set equal to the middle value among vi(Ja−, b−K), vi(Ja+, b−K) and vi(Ja+, b+K); rightvalue (RV): if a ≡2, ˜vi([a, b]):= vi(Ja+, b−K). Since the original valuations vis are non-negative, the resulting virtual valuations ˜vis are also non-negative. Let L be the coloring function that assigns each vertex x the agent/index i that maximizes the virtual valuation ˜vi(˜Ai(x)) applied to the fractional connected bundle ˜Ai(x), where ties are broken in favor of agents receiving a non-empty bundle and, in case of further ties, arbitrarily. We observe that L is a special coloring function. Indeed, for any i ∈[n], the (n −2)-face Fi of ∆, which does not contain vi, is such that the fractional allocations ˜ A(x) corresponding to vertices x ∈V (T) located on Fi have their i-th bundle empty (˜Ai(x) = ∅). Because of the non-negativity of the virtual valuations, any empty bundle always has the lowest virtual value, regardless of the agent or allocation being considered. Therefore, by the construction of L, we have L(x)̸ = i for any i ∈[n] and any vertex x ∈V (T) located on the (n −2)-face Fi. Thus, L is a special coloring function.

From the Fully-colored Simplex to the EQ1Pc g Allocation. According to Sperner’s Lemma (Theorem 3.1), there exists at least one fully-colored elementary (n −1)-simplex

16704

<!-- Page 6 -->

∆∗= conv(x∗

1,..., x∗ n) ∈T under the coloring L, where L(x∗ σ(i)) = i for all i ∈[n], for some permutation σ: [n] →[n]. Equivalently, each i ∈[n] is among those agents j who maximize the virtual valuation ˜vj(˜Aj(x∗ σ(i))) in the fractional connected allocation ˜ A(x∗ σ(i)) associated with the σ(i)-th vertex x∗ σ(i) of ∆∗, where the sequence of alloca- tions ˜A(x∗

1),..., ˜A(x∗ n) is obtained by moving each knife one at a time from left to right in a specific order, starting from the position of knives determined by ˜A(x∗

1). Denote by ˜ A the first allocation ˜ A(x∗

1), and refer to it as the main allocation of ∆∗. By appropriately rounding the fractional bundles of ˜ A, we will obtain the desired (integral) allocation A that satisfies the EQ1Pc g guarantee. The rounding procedure processes all fractional bundles ˜Ajs of the main allocation ˜ A from j = n down to j = 1, and for each bundle ˜Aj, it returns the integral bundle Aj that will form the final (integral) allocation A = (A1,..., An). Specifically, once the bundles Aj+1,..., An have been determined, the bundle Aj is obtained by rounding the fractional bundle

˜Aj = [aj, bj] based on the three possible fractionality levels of the two endpoints (9 = 3 × 3 cases) and other properties. This rounding process is formally described in Figure 1, and is carefully designed so that the following two lemmas hold.

Lemma 3.1. A is a connected (integral) allocation.

Given i ∈N and an integral bundle S = Js, tK ⊆[m], let v+ i (S) = max{vi(Js, tK), vi(Js + 1, tK), vi(Js, t −1K)} and v− i (S) = min{vi(Js, tK), vi(Js + 1, tK), vi(Js, t −1K)}; v+ i (S) and v− i (S) represent, respectively, the maximum and the minimum valuation that agent i can obtain from S, after possibly removing one of its endpoint items. Lemma 3.2. For any h, i, j ∈[n], the connected (integral) allocation A satisfies v− i (Aj) ≤˜vi(˜Aj(x∗ h)) ≤v+ i (Aj). These lemmas yield the following theorem. Theorem 3.3. A is an EQ1Pc g allocation, if valuations are non-negative.

Proof. First, A is a connected allocation by Lemma 3.1. Next, we show the EQ1Pc g guarantee. As observed above, the full coloring of simplex ∆∗implies that each i ∈[n] is one of the indices j ∈[n] that maximize ˜vj(˜Aj(x∗ σ(i))) (i.e., agent i has the highest virtual valuation in allocation

˜ A(x∗ σ(i))). Thus, for any i, j ∈N, we have v+ i (Ai) ≥

˜vi(˜Ai(x∗ σ(i))) ≥˜vj(˜Aj(x∗ σ(i))) ≥v− j (Aj), where the second inequality follows from the above observation, and the first and last inequalities follow from Lemma 3.2. Since v+ i (Ai) ≥v− j (Aj) for any i, j ∈N, we conclude that A satisfies the EQ1Pc g guarantee (i.e., equitability is obtained by removing at most one chore from the boundary of Ai and one good from the boundary of Aj).

Efficient Computation. The EQ1Pc g allocation guaranteed by Theorem 3.3 can be computed by a polynomialtime algorithm. The algorithm first computes the set Cv of

1: 2(i): 2(ii):

3:

4: 5(i): 5(ii):

6(i): 6(ii):

7:

8(i): 8(ii):

9:

aj ≡0 (LV)

aj ≡1 (BV)

aj ≡2 (RV)

**Figure 1.** Given j ∈[n], we describe how the fractional bundle ˜Aj = [aj, bj] of the main allocation of ∆∗can be rounded to obtain the integral bundle Aj in each of the following nine cases, assuming that Aj+1,..., An have already been determined: 1: aj ≡0, bj ≡0: Aj ←Ja− j, b−

j K; 2: aj ≡0, bj ≡1: (i) Aj ←Ja− j, b− j K if b+ j ∈Aj+1, and (ii) Aj ←Ja− j, b+ j K if b+ j̸ ∈Aj+1; 3: aj ≡0, bj ≡2: Aj ←Ja− j, b+ j K; 4: aj ≡1, bj ≡0: Aj ←Ja− j, b− j K; 5: aj ≡1, bj ≡1: (i) Aj ←Ja− j, b− j K if b+ j ∈Aj+1, and (ii) Aj ←Ja+ j, b+ j K if b+ j̸ ∈Aj+1; 6: aj ≡1, bj ≡2: (i) Aj ←Ja+ j, b+ j K if ∆∗is left-first, and (ii) Aj ←Ja− j, b+ j K if ∆∗is right-first, where left-first (resp. right-first) means that, in the sequence ˜A(x∗

1),..., ˜A(x∗ n), the left (resp. right) knife delimiting the j-th bundle is the first to move rightward; 7: aj ≡2, bj ≡0: Aj ←Ja+ j, b− j K; 8: aj ≡2, bj ≡1: (i) Aj ←Ja+ j, b− j K if b+ j ∈Aj+1, (ii) Aj ←Ja+ j, b+ j K if b+ j̸ ∈Aj+1; 9: aj ≡2, bj ≡2: Aj ←Ja+ j, b+ j K. The figure illustrates each of the nine cases as follows: each item and its three associated fractionality levels are represented by an ellipse divided into three parts; the two black triangles in each case represent the positions (aj and bj) of the two knives that determine the j-th fractional bundle

˜Aj = [aj, bj] (by possibly cutting the two boundary items of the considered bundle); the red rectangle encloses all items that are fully included in the j-th bundle Aj of the rounded (integral) allocation A; the right-hand item, when marked with crossed lines, indicates that it was included in bundle Aj+1 during the previous step of the rounding procedure; the blue circle on the left (resp. right) knife indicates that bundle [aj, bj] is left-first (resp. right-first) in ∆∗.

the valuations vi(S) that each agent i has for any bundle S (in O(nm2) time) and then, by dynamic programming, determines for each c ∈Cv if there exists an allocation A such that v+ i (Ai) ≥c ≥v− i (Ai) for any i ∈[n] (in O(nm2) time), where v+ i (S) and v− i (S) denote the maximum and the minimum valuation that i can obtain from a bundle S by deleting at most one item from its boundary;

16705

<!-- Page 7 -->

again, we restrict ourselves to allocations where the i-th leftmost bundle is assigned to agent i. We show that finding a value c ∈Cv satisfying the above condition is equivalent to finding an EQ1Pc g allocation, whose existence is ensured by Theorem 3.3. Hence, we obtain the following theorem: Theorem 3.4. If valuations are non-negative, an EQ1Pc g allocation can be found in time O(n2m4).

EF1Pc g Allocations To show the existence of EF1Pc g allocations, we employ the same framework as in the equitability case, with minor modifications. We use the same triangulation T as in the previous case but equip it with n distinct coloring functions L1,..., Ln, instead of the single coloring function L used earlier. Here, each Li colors any vertex in V (T) with the index j of the bundle that agent i prefers under virtual valuation ˜vi (defined as in the previous case); we note that each Li is special, as the empty bundle is the least valuable.

By applying the Generalized Sperner’s Lemma (Theorem 3.2), we show the existence of a jointly fully-colored elementary (n−1)-simplex ∆∗. As in the previous case, this simplex corresponds to a sequence of n connected fractional partitions, but now the bundles are initially unallocated, and there exist two permutations σ and τ such that, in the σ(i)th allocation, agent i ∈[n] does not envy any other agent if i receives the τ(i)-th bundle. Then, by applying the same rounding procedure used for the EQ1Pc g case, the first fractional partition of ∆∗is converted into an integral EF1Pc g allocation, where each agent i receives the τ(i)-th bundle. This leads to the following theorem: Theorem 3.5. Under non-negative valuations, an EF1Pc g allocation always exists.

We conjecture that computing an EF1Pc g allocation is PPAD-complete, similarly to the result shown in (Deng, Qi, and Saberi 2012); furthermore, even without path constraints, the complexity of finding EF1 or EF1c g remains open. In the subclass of monotone non-decreasing valuations (i.e., goods only), Theorems 3.3–3.5 extend to (the stronger) EF1 and EQ1 under path constraints, thus recovering the results of Bil`o et al. (2022); Igarashi (2023); Misra et al. (2021); Suksompong (2019).

## 4 Non-positive Valuations

To address the case of non-positive valuations under pathconnectivity constraints, we resort to a novel multi-coloring variant of Sperner’s Lemma, where the underlying coloring functions assign, to each vertex x ∈V (T), a set of colors (rather than a single color), including the indices i of the (n −2)-dimensional faces Fi to which x belongs.

Multi-coloring Sperner’s Lemma. Let T be a fixed triangulation of an (n −1)-simplex ∆= conv(v1,..., vn). A multi-coloring function of T is a mapping L: V (T) → 2[n] \ {∅} that assigns a non-empty subset of colors L(x) ⊆ [n] to each vertex of x ∈V (T). We recall that Fi is the (n −2)-dimensional face of ∆opposite to vertex vi. A multi-coloring function L is called special if, for any vertex x ∈V (T), L(x) ⊇{i ∈[n]: x ∈Fi} holds (i.e., if x is a boundary vertex, the set of colors L(x) contains the indices associated with all (n −2)-faces of ∆on which x is located). We observe that, if L is a special multi-coloring function and F is a (k −1)-face of ∆spanned by vertices vi1,..., vik, it holds that L(x) ⊇[n] \ {i1,..., ik} for any vertex x ∈V (T) that lies on F. An elementary (n −1)simplex ∆∗= conv(x∗

1,..., x∗ n) ∈T is said to be fullycolored under a multi-coloring function L if there exists a permutation σ: [n] →[n] such that i ∈L(x∗ σ(i)) for any i ∈[n] (that is, a distinct color i appears in the set L(x∗ σ(i)) associated with a distinct vertex x∗ σ(i)).

Theorem 4.1 (Multi-coloring Sperner’s Lemma). Let T be a triangulation of an (n −1)-simplex ∆, where n ≥2, and let L be a special multi-coloring function of T. Then, there exists a fully-colored elementary (n −1)-simplex ∆∗∈T under multi-coloring function L.

The Multi-coloring Sperner’s Lemma can be viewed as the dual of the standard one: whereas the classical version forbids color i on face Fi, the multi-coloring version requires it to appear in L(x) for every x ∈Fi.

EQ1Pc g and EF1Pc g Allocations To show the existence of an EQ1Pc g allocation for nonpositive valuations, we use the same triangulation T as in the case of non-negative one, but we equip T with the multicoloring function L that assigns to each vertex x ∈V (T) the set L(x) of indices j which maximize ˜vj(˜Aj(x)), where ˜vj is the virtual valuation defined as in Section 3. Unlike the case of non-negative valuations, in this case the empty bundle is always the best for each agent. Thus, L is a special multi-coloring function and, by the Multi-coloring Sperner’s Lemma (Theorem 4.1), there exists an elementary (n −1)simplex ∆∗= conv(x∗

1,..., x∗ n) that is fully-colored under the multi-coloring function L. As in the case of non-negative valuations, this means that there exists a permutation σ such that each agent i ∈[n] attains the highest valuation among all agents in allocation A(x∗ σ(i)) (where each agent j receives the j-th bundle). From this point onward, we can apply the same approach used for non-negative valuations to transform ∆∗into an EQ1Pc g allocation. Theorem 4.2. Under non-positive valuations, an EQ1Pc g allocation always exists and is polynomial-time computable.

As in the non-negative case, we generalize the multicoloring Sperner’s Lemma to handle n distinct multicoloring functions, each representing the virtual valuation of an agent i. This yields a jointly fully-colored simplex ∆∗, where each vertex corresponds to an allocation in which a distinct agent prefers a distinct bundle. Applying the rounding procedure then provides the desired EF1Pc g allocation. Theorem 4.3. Under non-positive valuations, an EF1Pc g allocation always exists.

The following corollary holds since, in the case of monotone non-increasing valuations, there are chores only. Corollary 4.1. Under non-increasing valuations, EQ1 and EF1 allocations always exist, even under path constraints, with the former being computable in polynomial time.

16706

<!-- Page 8 -->

## Acknowledgements

This work was partially supported by: the Horizon EU Framework Programme under Grant agreement No 101183743 (AGATE); the PNRR MIUR project FAIR - Future AI Research (PE00000013), Spoke 9 - Green-aware AI; the MUR - PNRR IF Agro@intesa; the Project SERICS (PE00000014) under the NRRP MUR program funded by the EU – NGEU; GNCS-INdAM. We thank the anonymous reviewers for their insightful comments.

AI Use Declaration

ChatGPT (OpenAI) was used exclusively for minor language polishing and figure formatting. All scientific content, analyses, and data were fully conceived and prepared by the authors.

## References

Akrami, H.; Alon, N.; Chaudhury, B. R.; Garg, J.; Mehlhorn, K.; and Mehta, R. 2025. EFX: A Simpler Approach and an (Almost) Optimal Guarantee via Rainbow Cycle Number. Oper. Res., 73(2): 738–751. Akrami, H.; and Rathi, N. 2025. Epistemic EFX Allocations Exist for Monotone Valuations. In AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, 13520–13528. AAAI Press. Amanatidis, G.; Aziz, H.; Birmpas, G.; Filos-Ratsikas, A.; Li, B.; Moulin, H.; Voudouris, A. A.; and Wu, X. 2023. Fair division of indivisible goods: Recent progress and open questions. Artif. Intell., 322: 103965. Amanatidis, G.; Markakis, E.; and Ntokos, A. 2020. Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle elimination. Theor. Comput. Sci., 841: 94– 109. Aziz, H.; Caragiannis, I.; Igarashi, A.; and Walsh, T. 2022. Fair allocation of indivisible goods and chores. Auton. Agents Multi Agent Syst., 36(1): 3. Aziz, H.; Freeman, R.; Shah, N.; and Vaish, R. 2024. Best of Both Worlds: Ex Ante and Ex-Post Fairness in Resource Allocation. Operations Research, 72(4): 1674–1688. Aziz, H.; and Rey, S. 2020. Almost group envy-free allocation of indivisible goods and chores. In Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence, IJCAI 2020, 39–45. Bapat, R. B. 1989. A constructive proof of a permutationbased generalization of Sperner’s Lemma. Mathematical Programming, 44(1): 113–120. Barman, S.; Bhaskar, U.; Pandit, Y.; and Pyne, S. 2024. Nearly Equitable Allocations beyond Additivity and Monotonicity. In 38th AAAI Conference on Artificial Intelligence, AAAI 2024, 9494–9501. AAAI Press. Barman, S.; Narayan, V. V.; and Verma, P. 2023. Fair Chore Division under Binary Supermodular Costs. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems AAMAS, 2863–2865. ACM.

B´erczi, K.; B´erczi-Kov´acs, E. R.; Boros, E.; Gedefa, F. T.; Kamiyama, N.; Kavitha, T.; Kobayashi, Y.; and Makino, K. 2024. Envy-free relaxations for goods, chores, and mixed items. Theor. Comput. Sci., 1002: 114596. Bhaskar, U.; Sricharan, A. R.; and Vaish, R. 2021. On Approximate Envy-Freeness for Indivisible Chores and Mixed Resources. In Approximation, Randomization, and Combinatorial Optimization. Algorithms and Techniques, AP- PROX/RANDOM, volume 207 of LIPIcs, 1:1–1:23. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Bil`o, V.; Caragiannis, I.; Flammini, M.; Igarashi, A.; Monaco, G.; Peters, D.; Vinci, C.; and Zwicker, W. S. 2022. Almost envy-free allocations with connected bundles. Games Econ. Behav., 131: 197–221. Bil`o, V.; Loebl, M.; and Vinci, C. 2025. On Almost Fair and Equitable Allocations of Indivisible Items for Nonmonotone Valuations. CoRR, abs/2503.05695. Bil`o, V.; Markakis, E.; and Vinci, C. 2024. Achieving Envy-Freeness Through Items Sale. In 32nd Annual European Symposium on Algorithms, ESA 2024, volume 308 of LIPIcs, 26:1–26:16. Bouveret, S.; Cechl´arov´a, K.; Elkind, E.; Igarashi, A.; and Peters, D. 2017. Fair Division of a Graph. In Proceedings of the Twenty-Sixth International Joint Conference on Artificial Intelligence, IJCAI 2017, 135–141. Bouveret, S.; Cechl´arov´a, K.; and Lesca, J. 2019. Chore division on a graph. Auton. Agents Multi Agent Syst., 33(5): 540–563. Budish, E. 2011. The combinatorial assignment problem: Approximate competitive equilibrium from equal incomes. Journal of Political Economy, 119(6): 1061–1103. Caragiannis, I.; Garg, J.; Rathi, N.; Sharma, E.; and Varricchio, G. 2023. New Fairness Concepts for Allocating Indivisible Items. In Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, IJCAI 2023, 2554–2562. ijcai.org. Caragiannis, I.; Kurokawa, D.; Moulin, H.; Procaccia, A. D.; Shah, N.; and Wang, J. 2019. The Unreasonable Fairness of Maximum Nash Welfare. ACM Transactions on Economics and Computation, 7(3): 12:1–12:32. Chierichetti, F.; Kumar, R.; Lattanzi, S.; and Vassilvitskii, S. 2017. Fair Clustering Through Fairlets. In Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, 5029–5037. Christoforidis, V.; and Santorinaios, C. 2024. On the Pursuit of EFX for Chores: Non-existence and Approximations. In Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI 2024, 2713–2721. Deng, X.; Qi, Q.; and Saberi, A. 2012. Algorithmic solutions for envy-free cake cutting. Operations Research, 60(6): 1461–1476. Dinitz, M.; Srinivasan, A.; Tsepenekas, L.; and Vullikanti, A. 2022. Fair Disaster Containment via Graph-Cut Problems. In International Conference on Artificial Intelligence and Statistics, AISTATS 2022, 28-30 March 2022, Virtual

16707

<!-- Page 9 -->

Event, volume 151 of Proceedings of Machine Learning Research, 6321–6333. PMLR. Dubins, L. E.; and Spanier, E. H. 1961. How to cut a cake fairly. American Mathematical Monthly, 68(1P1): 1–17. Flegg, H. G. 1974. From Geometry to Topology. Crane, Russak & Co. Foley, D. K. 1966. Resource allocation and the public sector. Yale University. Freeman, R.; Sikdar, S.; Vaish, R.; and Xia, L. 2019. Equitable Allocations of Indivisible Goods. In 28th International Joint Conference on Artificial Intelligence, IJCAI 2019, 280–286. Freeman, R.; Sikdar, S.; Vaish, R.; and Xia, L. 2020. Equitable Allocations of Indivisible Chores. In 19th International Conference on Autonomous Agents and MultiAgent Systems, AAMAS 2020, 384–392. Garg, J.; and Murhekar, A. 2024. Computing Pareto- Optimal and Almost Envy-Free Allocations of Indivisible Goods. J. Artif. Intell. Res., 80: 1–25. Gourv`es, L.; Monnot, J.; and Tlilane, L. 2014. Near fairness in matroids. In 21st European Conference on Artificial Intelligence, ECAI 2014, 393–398. Halpern, D.; and Shah, N. 2019. Fair Division with Subsidy. In Algorithmic Game Theory - 12th International Symposium, SAGT 2019, Proceedings, volume 11801, 374–389. Hoefer, M.; Schmalhofer, M.; and Varricchio, G. 2024. Best of Both Worlds: Agents with Entitlements. J. Artif. Intell. Res., 80: 559–591. Hosseini, H.; and Sethia, A. 2025. Equitable Allocations of Mixtures of Goods and Chores. CoRR, abs/2501.06799. Hosseini, H.; Sikdar, S.; Vaish, R.; and Xia, L. 2023. Fairly Dividing Mixtures of Goods and Chores under Lexicographic Preferences. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems, AAMAS 2023, 152–160. ACM. Igarashi, A. 2023. How to Cut a Discrete Cake Fairly. In Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI, 5681–5688. AAAI Press. Kuhn, H. W. 1960. Some Combinatorial Lemmas in Topology. IBM Journal of Research and Development, 4(5): 518– 524. Lipton, R. J.; Markakis, E.; Mossel, E.; and Saberi, A. 2004. On approximately fair allocations of indivisible goods. In Proceedings of the 5th ACM Conference on Electronic Commerce EC 2004, 125–131. Liu, S.; Lu, X.; Suzuki, M.; and Walsh, T. 2024. Mixed Fair Division: A Survey. J. Artif. Intell. Res., 80: 1373–1406. Misra, N.; Sonar, C.; Vaidyanathan, P. R.; and Vaish, R. 2021. Equitable Division of a Path. CoRR, abs/2101.09794. Plaut, B.; and Roughgarden, T. 2020. Almost Envy-Freeness with General Valuations. SIAM Journal on Discrete Mathematics, 34(2): 1039–1068. Scarf, H. E. 1982. The computation of equilibrium prices: an exposition. Handbook of Mathematical Economics, 2: 1007–1061.

Schwartz, R.; and Zats, R. 2022. Fair Correlation Clustering in General Graphs. In Approximation, Randomization, and Combinatorial Optimization. Algorithms and Techniques, APPROX/RANDOM 2022, volume 245 of LIPIcs, 37:1–37:19. Sperner, E. 1928. Neuer beweis f¨ur die invarianz der dimensionszahl und des gebietes. Abhandlungen aus dem Mathematischen Seminar der Universit¨at Hamburg, 6: 265–272. Steinhaus, H. 1948. The problem of fair division. Econometrica, 16(1): 101–104. Stromquist, W. 1980. How to cut a cake fairly. American Mathematical Monthly, 87(8): 640–644. Suksompong, W. 2019. Fairly allocating contiguous blocks of indivisible items. Discret. Appl. Math., 260: 227–236.

16708
