---
title: "Aggregate-Combine-Readout GNNs Can Express Logical Classifiers Beyond the Logic C2"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39308
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39308/43269
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Aggregate-Combine-Readout GNNs Can Express Logical Classifiers Beyond the Logic C2

<!-- Page 1 -->

Aggregate-Combine-Readout GNNs Can Express Logical Classifiers Beyond the Logic C2

Stan P Hauke*1, Przemysław Andrzej Wałęga*2

1Department of Informatics, King’s College London, UK 2School of Electronic Engineering and Computer Science, Queen Mary University of London, UK stanislaw.hauke@kcl.ac.uk, p.walega@qmul.ac.uk

## Abstract

In recent years, there has been growing interest in understanding the expressive power of graph neural networks (GNNs) by relating them to logical languages. This research has been initialised by an influential result of Barceló et al. (2020), who showed that the graded modal logic (or a guarded fragment of the logic C2), characterises the logical expressiveness of aggregate-combine GNNs. As a “challenging open problem” they left the question whether C2 characterises the logical expressiveness of aggregate-combine-readout GNNs. This question has remained unresolved despite several attempts. In this paper, we solve the above open problem by proving that aggregate-combine-readout GNNs can express logical classifiers beyond C2. This result holds over both undirected and directed graphs. Beyond its implications for GNNs, our work also leads to purely logical insights on the expressive power of infinitary logics.

Extended version — https://arxiv.org/abs/2508.06091

## Introduction

Graph Neural Networks (GNNs) (Gilmer et al. 2017) are state-of-the-art machine learning models tailored for processing graph-structured data. They have been successfully applied across numerous domains, including molecular property prediction (Besharatifard and Vafaee 2024), traffic forecasting and navigation (Derrow-Pinion et al. 2021), visual scene interpretation (Chen et al. 2024), personalised recommendations (Ying et al. 2018), as well as knowledge graph completion and reasoning under partial information (Tena Cucala et al. 2022; Zhang and Chen 2018; Huang et al. 2025a). In recent years, there has been growing interest in understanding the expressive power of GNNs, particularly focusing on the message-passing architectures. A key result (Morris et al. 2019; Xu et al. 2019) shows that GNNs have the same distinguishing power as the Weisfeiler–Leman (WL) algorithm (Weisfeiler and Leman 1968)—a widely used heuristic for testing graph isomorphism (Babai and Kucera 1979). This means that a pair of

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

graphs can be distinguished by WL if and only if there exists a GNN that can distinguish them. The result by Cai, Fürer, and Immerman (1992), in turn, shows that WL has the same distinguishing power as the fragment C2 of firstorder logic (FO), in which formulas are restricted to two variables but may use counting quantifiers ∃𝑘, interpreted as “there exist at least 𝑘distinct elements such that ….” Hence, we obtain a tight correspondence between GNNs, the Weisfeiler–Leman algorithm, and the logic C2.

The results on the distinguishable power, however, do not allow us to establish a one-to-one mapping between GNNs and logical formulas expressing the same properties. This finer correspondence is known as logical expressiveness, or uniform expressive power, and has attracted growing interest in recent years (Benedikt et al. 2024; Ahvonen et al. 2025; Schönherr and Lutz 2025; Nunn et al. 2024; Tena Cucala and Cuenca Grau 2024; Huang et al. 2025b,a; Grohe 2021). The main, and historically first, results in this direction have been established by Barceló et al. (2020). They have studied two architectures of message-passing GNNs: the standard aggregate-combine GNNs (AC-GNNs) and their extension with readout function called aggregate-combinereadout GNNs (ACR-GNNs). The two main results of Barceló et al. (2020) are as follows:

(i) the FO node properties expressible by AC-GNNs are exactly those definable in graded modal logic, (ii) the FO node properties expressible by ACR-GNNs con- tain all properties definable in C2.

Note that, in contrast to Result (i), Result (ii) does not provide an exact logical characterisation. This was left by the authors’ as an open problem.

The Open Problem The precise formulation of the open problem of Barceló et al. (2020) is whether the FO node properties expressible by ACR-GNNs are exactly those definable in C2. Their paper explicitly states that this is “a challenging open problem.” This question was subsequently highlighted in later papers, for example by Grohe (2021) as Question 4 on his list of “interesting theoretical questions that remain open.”

Several research groups have attempted to solve this problem (Pflueger, Tena Cucala, and Kostylev 2024;

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

21594

<!-- Page 2 -->

Benedikt et al. 2024), but without success. As a result the question has remained unresolved for the past five years.

Contributions In this paper we will solve the above open problem, by showing that ACR-GNNs can express FO node classifiers beyond C2.

We will show that this result holds not only in the setting of undirected graphs—as originally considered by Barceló et al. (2020)—but also in the setting of directed graphs. In both cases, our proofs follow a common structure: (1) we define a node property, (2) we show that it is expressible both in FO and by an ACR-GNN, and (3) we show that the property is not expressible in C2. In the directed case (Section 4), the property we consider is that of “being a node of a graph whose edge relation forms a strict linear order.” In the undirected case (Section 5), we simulate directed edges using paths of three undirected edges, where direction of an edge is encoded by colours of the two middle nodes in the path. We then consider the property of being a node of an undirected graph that simulates a strict linear order. To show Results (1) and (2) we provide constructions of FO formulas and ACR-GNNs, respectively. To show the inexpressibility Results (3), we introduce in Section 3 a bounded version of WL algorithm, which characterises the expressive power of C2 formulas whose counting quantifiers ∃𝑘have bounded 𝑘.

Note that, in particular, we show that linear orders cannot be expressed in C2. Inexpressibility of linear orders in logics is a well studied topic; it is known that FO2 (i.e. FO with two variables) cannot express linear orders (Immerman and Kozen 1989; Szwast and Tendera 2013) and a similar result for C2 can be inferred from results of Charatonik and Witkowski (2016). We will prove the latter result directly, which will be useful afterwards for the inexpressibility Result (3) for undirected graphs. Finally, in Section 6 we exploit our results to the study the expressive power of infinitary logics. As we show, the infinitary version of C2 can express strictly more FO properties than the standard, finitary C2.

## Preliminaries

We introduce notions and notation for graphs, GNNs, and logics. Our setting extends that ofBarceló et al. (2020) by considering not only undirected, but also directed graphs.

Graphs A directed (node-labelled, finite, and simple) graph of dimension 𝑑∈ℕis a tuple 𝐺= (𝑉, 𝐸, 𝜆), where 𝑉is a finite set of nodes, 𝐸⊆𝑉× 𝑉is a set of directed edges with no loops 𝐸(𝑣, 𝑣), and 𝜆∶𝑉→{0, 1}𝑑assigns to each node a binary vector of a dimension 𝑑. We will identify undirected graphs with directed graphs that have a symmetric edge relation, and write {𝑣, 𝑤} for a pair of edges (𝑣, 𝑤), (𝑤, 𝑣).

The neighbourhoud, 𝑁𝐺(𝑣), of a node 𝑣in a graph 𝐺, is the set of all nodes 𝑤such that 𝐺has an edge (in any direction) between 𝑤and 𝑣. The in-neighbourhoud,⃖⃖𝑁𝐺(𝑣), are nodes 𝑤such that 𝐺has an edge from 𝑤to 𝑣, whereas the out-neighbourhoud,⃖⃗𝑁𝐺(𝑣), are nodes 𝑤such that 𝐺 has an edge from 𝑣to 𝑤. Hence, in undirected graphs we have 𝑁𝐺(𝑣) =⃖⃖𝑁𝐺(𝑣) =⃖⃗𝑁𝐺(𝑣).

GNN Node Classifiers We focus on aggregatecombine-readout GNNs (ACR-GNNs) introduced by Barceló et al. (2020), which extend the standard messagepassing mechanism with readout functions. First, we introduce ACR-GNN architecture for processing undirected graphs. In such GNNs, each layer is a triple (𝖺𝗀𝗀, 𝖼𝗈𝗆𝖻, 𝗋𝖾𝖺𝖽) consisting of an aggregation function, 𝖺𝗀𝗀, mapping a multiset (a generalisation of a set so that elements can have multiple occurrences) of vectors into a single vector, a combination function 𝖼𝗈𝗆𝖻, mapping three vectors to one vector, and a readout function, 𝗋𝖾𝖺𝖽, mapping a multiset of vectors into a single vector. Such layers applied to a graph 𝐺= (𝑉, 𝐸, 𝜆) computes a graph 𝐺′ = (𝑉, 𝐸, 𝜆′) with a new labelling function 𝜆′ such that for each 𝑣, the labelling 𝜆′(𝑣) is given by 𝖼𝗈𝗆𝖻(𝜆(𝑣), 𝖺𝗀𝗀(⦃𝜆(𝑤)⦄𝑤∈𝑁𝐺(𝑣)), 𝗋𝖾𝖺𝖽(⦃𝜆(𝑤)⦄𝑤∈𝑉)), where ⦃⋅⦄stands for a multiset. In the spirit of Rossi et al. (2023), we also consider a straightforward generalisation of ACR-GNN architecture for processing directed graphs. In this case a GNN is a tuple (⃖⃖⃖𝖺𝗀𝗀,⃖⃖⃗𝖺𝗀𝗀, 𝖼𝗈𝗆𝖻, 𝗋𝖾𝖺𝖽), which has two types of aggregation:⃖⃖⃖𝖺𝗀𝗀for incoming edges and⃖⃖⃗ 𝖺𝗀𝗀for outgoing edges. In such ACR-GNNs, a new labelling 𝜆′(𝑣) is computes as 𝖼𝗈𝗆𝖻(𝜆(𝑣),⃖⃖⃖𝖺𝗀𝗀(⦃𝜆(𝑤)⦄𝑤∈⃖𝑁𝐺(𝑣)),⃖⃖⃗ 𝖺𝗀𝗀(⦃𝜆(𝑤)⦄𝑤∈⃗𝑁𝐺(𝑣)), 𝗋𝖾𝖺𝖽(⦃𝜆(𝑤)⦄𝑤∈𝑉)).

An ACR-GNN classifier 𝒩of dimension 𝑑consists of a fixed number 𝐿of layers1 and a classification function 𝖼𝗅𝗌 from vectors to truth values; once applied to a graph of dimension 𝑑, the classifier 𝒩computes for each node 𝑣a truth value denoted as 𝒩(𝐺, 𝑣).

Logical Node Classifiers By FO we mean the standard first-order logic with identity =, one binary predicate 𝐸for edges, and unary predicates 𝑃1, …, 𝑃𝑑for node labels. Let C2 be the fragment of FO, which allows for using only two variables in formulas, but allows for additional counting quantifiers ∃𝑘, for any 𝑘∈ℕ, where ∃𝑘𝑥𝜑(𝑥) means that 𝜑holds in at least 𝑘different nodes. We will write ∃=𝑘𝜑(𝑥) as an abbreviation for ∃𝑘𝜑(𝑥) ∧¬∃𝑘+1𝜑(𝑥). Note that we write 𝜑(𝑥) for a formula with exactly one free variable 𝑥, and similarly we will use 𝜑(𝑥, 𝑦) for a formula with exactly two free variables. We let the quantifier depth of a formula 𝜑be its maximum nesting of quantifiers. Moreover, for C2 formulas we define the counting rank, 𝗋𝗄#(𝜑), as the maximal among numbers 𝑘occurring in its counting quantifiers. For a logic ℒ, we let ℒ𝓁,𝑐be the fragment with formulas of depth at most 𝓁and counting rank at most 𝑐. In the paper we pay special attention to C2 𝓁,𝑐.

1We assume that functions in the layers are of matching dimensions, so that they can be applied.

21595

<!-- Page 3 -->

A logical node classifier is a formula 𝜑(𝑥) in FO (or its fragment) with one free variable. To evaluate logical classifiers, we identify a graph 𝐺= (𝑉, 𝐸, 𝜆) of dimension 𝑑 with the FO structures 𝔐𝐺= (𝑉, 𝑃1, …, 𝑃𝑑, 𝐸), with domain 𝑉, sets 𝑃𝑖= {𝑣∈𝑉∣𝜆(𝑣)𝑖= 1} containing all nodes 𝑣with 1 on the 𝑖th position of 𝜆(𝑣), and the binary relation 𝐸being the graph edges. We assume the standard FO semantics over such models and write 𝐺⊧𝜑(𝑣) if classifier 𝜑(𝑥) holds in 𝔐𝐺at the node 𝑣. If this is the case, we say that the application of the logical classifier 𝜑(𝑥) to 𝐺at node 𝑣is 𝗍𝗋𝗎𝖾, and otherwise it is 𝖿𝖺𝗅𝗌𝖾. We write 𝐺, 𝑢≡ℒ𝐻, 𝑣, if 𝐺⊧𝜑(𝑢) is equivalent to 𝐻⊧𝜑(𝑣), for each logical classifier 𝜑(𝑥) in a logic ℒ.

WL Algorithm with Bounded Counting

In this section, we will introduce a bounded version of the one dimensional WL algorithm (Weisfeiler and Leman 1968). Our version WL𝑐is parametrised by 𝑐∈ℕ, which bounds the “counting abilities” of the algorithm. As we will show, 𝓁rounds of application of WL𝑐allows us to characterise expressiveness of the fragment C2 𝓁,𝑐of C2, where formulas have depth bounded by 𝓁and counting rank by 𝑐. This result will play a crucial role to establish non-expressivity results in the latter sections of the paper.

The main idea behind WL𝑐is that the algorithm is insensitive to multiplicities (occurring in processed multisets) greater than 𝑐. Standard WL computes new node labels based on multisets ⦃⋅⦄of neighbours labels. In WL𝑐 the computations are based on the 𝑐-bounded multisets ⦃⋅⦄𝑐, obtained by reducing all multiplicities to at most 𝑐. For example ⦃7, 7, 7, 3⦄2 = ⦃7, 7, 3⦄. In particular, over undirected graphs, labelling 𝑊𝓁+1 𝑐 (𝑣) of a node 𝑣in iteration 𝓁+1 will depend on the the previous label 𝑊𝓁 𝑐(𝑣), the 𝑐-bounded multiset of labels of 𝑣neighbours, and the 𝑐bounded multiset of non-neighbours, so 𝑊𝓁+1 𝑐 (𝑣) equals

(𝑊𝓁 𝑐(𝑣), ⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈𝑁𝐺(𝑣), ⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈𝑉⧵{𝑁𝐺(𝑣)∪{𝑣}}).

Characterising C2 𝓁,𝑐over directed graphs is more challenging. In this case, instead of considering in WL𝑐one multiset of neighbours’ labels, we consider separately nodes which belong to⃖⃖𝑁𝐺and⃖⃗𝑁𝐺, those which belong to⃖⃖𝑁𝐺 only, and those which belong to⃖⃗𝑁𝐺only. Below we define WL𝑐for directed graphs, but for undirected graphs it reduces to the computations described above.

Definition 1. Let 𝑐∈ℕ. The 𝑐-bounded WL algorithm, WL𝑐, takes as an input a graph 𝐺= (𝑉, 𝐸, 𝜆), and computes labels 𝑊𝓁 𝑐(𝑣) for all 𝑣∈𝑉as follows:

𝑊0 𝑐(𝑣) = 𝜆(𝑣)

𝑊𝓁+1 𝑐 (𝑣) =

(

𝑊𝓁 𝑐(𝑣), ⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈⃖𝑁𝐺(𝑣)∩⃗𝑁𝐺(𝑣), (1)

⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈⃖𝑁𝐺(𝑣)⧵⃗𝑁𝐺(𝑣), ⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈⃗𝑁𝐺(𝑣)⧵⃖𝑁𝐺(𝑣),

⦃𝑊𝓁 𝑐(𝑤)⦄𝑐 𝑤∈𝑉⧵{𝑁𝐺(𝑣)∪{𝑣}}

)

.

We note that, over undirected graphs, WL𝑐with 𝑐< ∞ is strictly less expressive than the standard WL, whereas WL𝑐with 𝑐= ∞coincides with WL.

We will show that WL𝑐characterises the expressiveness of C2 with counting rank 𝑐. To this end, we will exploit a modal logic characterising C2 with counting rank 𝑐, which can be easily obtained based on the results of Lutz, Sattler, and Wolter (2001) and Barceló et al. (2020). Note that our proof below is over directed graphs, but since we treat undirected graphs as a special case of directed graphs, we can also use this result in the undirected setting. Theorem 2. Let 𝓁, 𝑐∈ℕ. For any directed graphs 𝐺and 𝐻with nodes 𝑢and 𝑣, the following holds:

𝐺, 𝑢≡C2 𝓁,𝑐𝐻, 𝑣 if and only if 𝑊𝓁 𝑐(𝑢) = 𝑊𝓁 𝑐(𝑣).

Proof sketch. Barceló et al. (2020) showed a modal logic ℰℳℒ𝒞that over undirected simple graphs has the same expressive power as C2. Formulas of ℰℳℒ𝒞are given by 𝜑∶= 𝑝∣¬𝜑∣𝜑∧𝜑∣⟨𝑆⟩⩾𝑘𝜑, where 𝑝are propositional variables, 𝑘∈ℕ, and 𝑆are modal parameters given by 𝑆∶= 𝑖𝑑∣𝑒∣𝑆∪𝑆∣𝑆∩𝑆∣¬𝑆. The logic is similar to (graded) modal logic, but allows for complex modal operators introduced by Lutz, Sattler, and Wolter (2001), which are constructed from the identity modality 𝑖𝑑(selfaccess) and standard modality 𝑒corresponding to edges in the graph, combined using Boolean operations. For example 𝐺, 𝑣⊧⟨𝑒∪¬𝑒⟩⩾3𝑝means that there are at least 3 nodes 𝑤such that 𝐸(𝑣, 𝑤) or ¬𝐸(𝑣, 𝑤), and 𝑝holds at 𝑤.

To characterise C2 over simple directed graphs we extend the grammar of modal parameters in ℰℳℒ𝒞with 𝑆−expressing the inverse of 𝑆. Let ℰℳℒ𝒞− 𝓁,𝑐be formulas in this extension with modal depth at most 𝓁and with 𝑘≤𝑐in graded modalities. We can show that over simple directed graphs ℰℳℒ𝒞− 𝓁,𝑐has the same expressiveness as

C2 𝓁,𝑐. Hence, it remains to show that 𝐺, 𝑢≡ℰℳℒ𝒞− 𝓁,𝑐𝐻, 𝑣if and only if 𝑊𝓁 𝑐(𝑢) = 𝑊𝓁 𝑐(𝑣). We prove this equivalence by induction on 𝑖≤𝓁. In the basis, we have 𝐺, 𝑢≡ℰℳℒ𝒞−

0,𝑐𝐻, 𝑣if and only if 𝑢and 𝑣satisfy the same unary predicates, which is equivalent to 𝑊0 𝑐(𝑢) = 𝑊0 𝑐(𝑣). For the inductive step we observe that each ℰℳℒ𝒞− 𝓁,𝑐formula can be equivalently written in the normal form, where 𝑆∶= 𝑖𝑑∣𝑒−∩𝑒∣𝑒−∩¬𝑒∣ 𝑒∩¬(𝑒−) ∣¬𝑒∩¬(𝑒−) ∩¬𝑖𝑑∣𝑆∪𝑆. In the forward implication assume that 𝑊𝑖+1 𝑐 (𝑢) ≠𝑊𝑖+1 𝑐 (𝑣), so 𝑊𝑖+1 𝑐 (𝑢) and 𝑊𝑖+1 𝑐 (𝑣) differ one of the five components from Equation (1). Since these components correspond to components of 𝑆grammar in our normal form, we can show that 𝐺, 𝑢≢ℰℳℒ𝒞− 𝑖+1,𝑐𝐻, 𝑣. For the backwards implication as- sume that 𝑊𝑖+1 𝑐 (𝑢) = 𝑊𝑖+1 𝑐 (𝑣). We show by induction on the structure of ℰℳℒ𝒞𝑖+1,𝑐formulas 𝜑that 𝐺, 𝑢⊧𝜑if and only if 𝐻, 𝑣⊧𝜑. The interesting case is for 𝜑= ⟨𝑆⟩⩾𝑘𝜓. Suppose towards a contradiction that 𝐺, 𝑢⊧⟨𝑆⟩≥𝑘𝜓, but 𝐻, 𝑣̸ ⊧⟨𝑆⟩≥𝑘𝜓. Since atomic parameters in the normal form of 𝑆have disjoint interpretations, there are 𝑘′ ≤𝑘

21596

<!-- Page 4 -->

and an atomic parameter 𝐴such that 𝐺, 𝑢⊧⟨𝐴⟩≥𝑘′𝜓, but 𝐻, 𝑣̸ ⊧⟨𝐴⟩≥𝑘′𝜓. By the inductive assumption and correspondence of atomic parameters to the sets occurring in Equation (1), we can show that 𝑊𝑖+1 𝑐 (𝑢) = 𝑊𝑖+1 𝑐 (𝑣), raising a contradiction.

We will use Theorem 2 in two following sections: in Section 4 for directed graphs (Theorem 6) and in Section 5 for undirected graphs (Theorem 12).

Logical Expressiveness Over Directed

Graphs In this section, we will study the expressiveness of ACR- GNNs over directed graphs. In this setting, we will consider an analogous question to the open problem of Barceló et al. (2020), namely: are C2 node classifiers exactly FO classifiers expressible by ACR-GNNs? As we will show, and which may be surprising, the answer is negative. To this end, we will prove that checking if edges of a graph form a strict linear order is expressible in FO and by ACR-GNNs, but cannot be expressed in C2. Although this is a property of graphs, we can formulate it also as a node classifier as follows. Definition 3. We let 𝜑𝐿𝑖𝑛(𝑥) be a node classifier accepting a node of a graph 𝐺if and only if 𝐺is a strict linear order.

Clearly, strict linear orders can be defined in FO with a formula 𝜓being a conjunction of the following three:

∀𝑥¬𝐸(𝑥, 𝑥) irreflexivity

∀𝑥∀𝑦

(

(𝑥= 𝑦) ∨𝐸(𝑥, 𝑦) ∨𝐸(𝑦, 𝑥)

)

totality

∀𝑥∀𝑦∀𝑧

(

𝐸(𝑥, 𝑦) ∧𝐸(𝑦, 𝑧) →𝐸(𝑥, 𝑧)

)

transitivity

Since we are considering simple graphs, irreflexivity can be omitted from 𝜓. Notice that 𝜓has no free variables, but we can always turn it into a node classifier by writing it as (𝑥= 𝑥) ∧𝜓. Thus, 𝜑𝐿𝑖𝑛(𝑥) is expressible in FO.

Next, we will show that 𝜑𝐿𝑖𝑛(𝑥) can be expressed as an ACR-GNN. This is more challenging, since ACR-GNNs cannot detect transitivity. To address this challenge, we will exploit the following equivalent definition of linear orders. Proposition 4. A finite binary relation 𝐸is a strict linear order if and only if 𝐸is irreflexive, total, and each element has a different number of 𝐸-successors.

Proof sketch. Strict linear orders clearly satisfy the three properties. For the opposite direction we show that 𝐸enjoying these properties is transitive. Assume that there are 𝑛elements. As each element has a different number of 𝐸successors and 𝐸is irreflexive, we can call the elements 𝑣0, …, 𝑣𝑛−1, where 𝑣𝑖is the unique element whose number of 𝐸-successors is 𝑖. By a strong induction on 𝑖≤𝑛−1, we can show that, for all 𝑣𝑗, we have (𝑣𝑖, 𝑣𝑗) ∈𝐸if and only if 𝑖> 𝑗. It implies that 𝐸must be transitive.

We will use Proposition 4 to construct an ACR-GNN which detects strict linear orders.

L1:

L2:

L3:

(1) (10) (100) (1000)

(1, 0) (10, 1) (100, 11) (1000, 111)

(1) (1) (1) (1)

**Figure 1.** Application of layers 1–3 of the ACR-GNN from Theorem 5 to the strict linear order with four nodes

Theorem 5. Over directed graphs, 𝜑𝐿𝑖𝑛(𝑥) is expressible by an ACR-GNN. It can be achieved using only 3 layers and no aggregation over the out-neighbourhood.

Proof. We will construct the required ACR-GNN 𝒩, whose application to a linear order of length four is presented in Figure 1. The first layer maps the initial vector of a node 𝑣into the number 10𝑛, where 𝑛is the indegree of 𝑣. This is obtained by setting⃖⃖⃖𝖺𝗀𝗀(𝑀) = 10|𝑀| and 𝖼𝗈𝗆𝖻(𝑥, 𝑦, 𝑧) = 𝑦. The second layer maps a vector of 𝑣 into a vector in ℝ2 of the form (10𝑛, 10𝑘1+⋯+10𝑘𝑛) where 10𝑛is as in the first layer, whereas each 𝑘𝑖is the in-degree of the 𝑖th among the 𝑛in-neighbours of 𝑣. This is obtained by setting⃖⃖⃖𝖺𝗀𝗀(𝑀) = 𝑠𝑢𝑚(𝑀) and 𝖼𝗈𝗆𝖻(𝑥, 𝑦, 𝑧) = (𝑥, 𝑦). The third layers maps each vector into 1 or 0 by setting 𝗋𝖾𝖺𝖽(𝑀) = 1 if both of the following conditions hold:

(i) 𝑥[1] ≠𝑦[1], for every pair 𝑥, 𝑦∈𝑀. (ii) if 𝑥[1] = 10𝑛, then 𝑥[2] = 1 … 1 ⏟⏟⏟ 𝑛times

, for each 𝑥∈𝑀.

If any of the conditions does not hold, we set 𝗋𝖾𝖺𝖽(𝑀) = 0. Finally, we let 𝖼𝗈𝗆𝖻(𝑥, 𝑦, 𝑧) = 𝑦.

Condition (i) guarantees that each node has a different in-degree. If this is the case, then Condition (ii)—which can be equivalently written as 𝑥[1]−1

9 = 𝑥[2]—checks if the graph is total. Hence, for any graph 𝐺= (𝑉, 𝐸, 𝜆), if 𝐸is a strict linear order, then 𝒩(𝐺, 𝑣) = 1 and otherwise 𝒩(𝐺, 𝑣) = 0, for any node 𝑣in 𝐺.

To finish this section, we need to show that 𝜑𝐿𝑖𝑛(𝑥) cannot be expressed in C2. For this, we will exploit our bounded WL algorithm and corresponding Theorem 2.

Theorem 6. Over directed graphs, 𝜑𝐿𝑖𝑛(𝑥) is not expressible in C2.

Proof sketch. Suppose towards a contradiction that 𝜑𝐿𝑖𝑛(𝑥) is expressible in C2, so it is definable by a formula in C2 𝓁,𝑐, for some 𝓁, 𝑐∈ℕ. To obtain a contradiction, we will construct a graph 𝐺with nodes 𝑣𝑖and a graph 𝐺′ with corresponding nodes 𝑣′ 𝑖, such that 𝐺⊧𝜑𝐿𝑖𝑛(𝑣𝑖) and 𝐺′̸ ⊧𝜑𝐿𝑖𝑛(𝑣′ 𝑖), but 𝐺, 𝑣𝑖≡C2 𝑙,𝑐𝐺′, 𝑣𝑖for all nodes 𝑣𝑖.

Let 𝑛= 𝓁⋅𝑐+ 1. We define 𝐺= (𝑉, 𝐸, 𝜆) as a strict linear order over 2𝑛+ 1 nodes 𝑉= {𝑣−𝑛, …, 𝑣𝑛}, with 𝐸= {(𝑣𝑖, 𝑣𝑗) ∶𝑖< 𝑗}, and 𝜆(𝑣𝑖) = 0 for each 𝑣𝑖.

21597

<!-- Page 5 -->

𝑊0

2:

𝑊1

2:

𝑊2

2:

𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5

**Figure 2.** Application of WL𝑐to 𝐺from Theorem 6; for readability we draw only arrows (𝑣𝑖, 𝑣𝑖+1) between consecutive nodes and (𝑣−1, 𝑣1) distinguishing 𝐺from 𝐺′

We let 𝐺′ = (𝑉′, 𝐸′, 𝜆′) be such that 𝑉′ = {𝑣′

−𝑛, …, 𝑣′ 𝑛}, 𝐸′ = {(𝑣′ 𝑖, 𝑣′ 𝑗) ∶𝑖< 𝑗} ⧵{(𝑣′

−1, 𝑣′

1)} ∪{(𝑣′ 1, 𝑣′ −1)}, and 𝜆′(𝑣′ 𝑖) = 0 for each 𝑣′ 𝑖. For example, if 𝑐= 2 and 𝓁= 2, the graphs 𝐺is depicted on top of Figure 2; graph 𝐺′ is similar, but instead of (𝑣′

−1, 𝑣′

1) it has the opposite edge (𝑣′ 1, 𝑣′ −1). Notice that both graphs are irreflexive, asymmetric, and total, but only 𝐺is transitive. Hence, for all nodes 𝑣𝑖, we have 𝐺⊧𝜑𝐿𝑖𝑛(𝑣𝑖) and 𝐺′̸ ⊧𝜑𝐿𝑖𝑛(𝑣′ 𝑖). It remains to show that 𝐺, 𝑣𝑖≡C2 𝑙,𝑐𝐺′, 𝑣′ 𝑖. To this end, by

Theorem 2, it suffices to show that 𝑊𝓁 𝑐(𝑣𝑖) = 𝑊𝓁 𝑐(𝑣′ 𝑖). We can prove it by showing, with a simultaneous induction on 𝑘≤𝓁, the following two statements:

(i) 𝑊𝑘 𝑐(𝑣𝑖) = 𝑊𝑘 𝑐(𝑣′ 𝑖), for 𝑖∈{−𝑛, …, 𝑛}, (ii) 𝑊𝑘 𝑐(𝑣𝑖) = 𝑊𝑘 𝑐(𝑣𝑗), for 𝑖, 𝑗∈{−(𝑛−𝑐𝑘), …, 𝑛−𝑐𝑘}.

Statement (ii) ensures that all ‘middle nodes’ have the same colour; for instance in Figure 2 nodes 𝑣−3, …, 𝑣3 have the same colour in 𝑊1

## 2 We use it to show

Statement (i), which implies required 𝐺, 𝑣𝑖≡C2 𝑙,𝑐𝐺′, 𝑣′ 𝑖.

Hence, we can conclude this sections as follows.

Corollary 7. Over directed graphs, there are FO node classifiers expressible by ACR-GNNs which are not expressible in C2. In particular, 𝜑𝐿𝑖𝑛(𝑥) is such a classifier.

Logical Expressiveness Over

Undirected Graphs Now we consider the setting of undirected graphs. We will solve the open problem of Barceló et al. (2020), asking whether over undirected graphs the FO node properties expressible by ACR-GNNs are exactly those definable in C2. We will show that, the answer is negative. In particular, we will show that, similarly to the case of directed graphs in Section 4, there is a property expressible by both FO and ACR-GNNs, but which cannot be expressed in C2. Our proofs will build on some ideas from Section 4, but no access to directed edges will require more complex argumentation.

In place of 𝜑𝐿𝑖𝑛(𝑥) from Section 4, we will use now classifier 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥). It checks if a node belongs to a gadgetised linear order, which is an undirected graph 𝗀𝖺𝖽(𝐺)

𝑃1 𝑣1 𝑎

𝑃1 𝑣1 𝑏

𝑃1 𝑣1 𝑐

𝑃1 𝑣1 𝑑

𝑃2 𝑣2

(𝑎,𝑏)

𝑃3 𝑣3

(𝑎,𝑏)

𝑃2 𝑣2

(𝑏,𝑐)

𝑃3 𝑣3

(𝑏,𝑐)

𝑃2 𝑣2

(𝑐,𝑑)

𝑃3 𝑣3

(𝑐,𝑑)

𝑃2 𝑣2

(𝑎,𝑐)

𝑃3 𝑣3

(𝑎,𝑐)

𝑃2 𝑣2

(𝑏,𝑑)

𝑃3 𝑣3

(𝑏,𝑑) 𝑃2 𝑣2

(𝑎,𝑑)

𝑃3 𝑣3

(𝑎,𝑑)

**Figure 3.** Gadgetisation of the linear order from Figure 1 assuming its nodes are called 𝑎, 𝑏, 𝑐, and 𝑑; labels (1, 0, 0), (0, 1, 0), and (0, 0, 1) are represented as 𝑃1, 𝑃2, and 𝑃3, respectively (and also with colours)

obtained by encoding (gadgetising) some strict linear order 𝐺. Intuitively, 𝗀𝖺𝖽(𝐺) is obtained by replacing each directed edge (𝑢, 𝑤) in 𝐺with a path of three undirected edges—called gadgetised edges—as depicted in Figure 3. Next, we present a formal definition of gadgetisation. Definition 8. The gadgetisation, 𝗀𝖺𝖽(𝐺), of a directed graph 𝐺 = (𝑉, 𝐸, 𝜆) is an undirected graph 𝐺′ = (𝑉′, 𝐸′, 𝜆′) of dimension 3 such that for each edge (𝑢, 𝑤) ∈ 𝐸, the graph 𝐺′ has:

• nodes 𝑣1 𝑢, 𝑣2

(𝑢,𝑤), 𝑣3

(𝑢,𝑤), 𝑣1 𝑤in 𝑉′,

• edges {𝑣1 𝑢, 𝑣2

(𝑢,𝑤)}, {𝑣2

(𝑢,𝑤), 𝑣3

(𝑢,𝑤)}, {𝑣3

(𝑢,𝑤), 𝑣1 𝑤} in 𝐸′,

• labelling of nodes with 𝜆′(𝑣1 𝑢) = 𝜆′(𝑣1 𝑤) = (1, 0, 0), 𝜆′(𝑣2

(𝑢,𝑤)) = (0, 1, 0), and 𝜆′(𝑣3

(𝑢,𝑤)) = (0, 0, 1).

Recall that we identify undirected graphs with symmetric directed graphs, so an undirected edge, like {𝑣1 𝑢, 𝑣2

(𝑢,𝑤)} in the definition above, can be seen as a pair of directed edges (𝑣1 𝑢, 𝑣2

(𝑢,𝑤)), (𝑣2

(𝑢,𝑤), 𝑣1 𝑢). Note also that our construction of 𝗀𝖺𝖽(𝐺) does not depend on the labelling 𝜆in 𝐺. Now, the formal definition of 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is as follows: Definition 9. We let 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) be a node classifier accepting a node of a graph 𝐺if and only if 𝐺is isomorphic to 𝗀𝖺𝖽(𝐺′), for some strict linear order 𝐺′.

It the remaining part of this section, we will show that 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is expressible in FO and by ACR-GNNs, but it is not expressible in C2. Theorem 10. Over undirected graphs, 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is expressible in 𝐹𝑂.

Proof sketch. We will express 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) as a conjunction of four FO formulas 𝜑1, 𝜑2, 𝜑3, and 𝜑4. Recall that we identify graphs with FO structures interpreting unary predicates 𝑃1, …, 𝑃𝑑, where 𝑑is the dimension of the graph, and one binary predicate 𝐸. Since gadgetisations are always of dimension 𝑑= 3, our formulas will mention three unary predicated 𝑃1, 𝑃2, and 𝑃3.

Formula 𝜑1 states that 𝑃1, 𝑃2, and 𝑃3 partition the set of nodes. Formula 𝜑2 states that every node satisfying 𝑃2 has exactly two 𝐸-neighbours: one satisfying 𝑃1 and the other satisfying 𝑃3. It states also that every node satisfying 𝑃3 has exactly two 𝐸-neighbours: one satisfying 𝑃1 and the other satisfying 𝑃2. Finally, it states that if 𝑢and 𝑣are nodes satisfying 𝑃1, then 𝐸(𝑢, 𝑣) cannot be true. Formulas 𝜑3 and 𝜑4 are about gadgetised edges, which are paths in

21598

<!-- Page 6 -->

𝗀𝖺𝖽(𝐺) that correspond to directed edges in 𝐺. In particular, we let a gadgetised edge from 𝑢to 𝑧be a path of the form 𝐸(𝑢, 𝑤), 𝐸(𝑤, 𝑣), 𝐸(𝑣, 𝑧) with 𝑃1(𝑢), 𝑃2(𝑤), 𝑃3(𝑣), and 𝑃1(𝑧).

Formula 𝜑3 states that between any two distinct nodes satisfying 𝑃1 there is exactly one gadgetised edge. Formula 𝜑4, in turn, states that there are no nodes 𝑢, 𝑤, 𝑣with gadgetised edges from 𝑣to 𝑤, from 𝑤to 𝑢, and from 𝑢to 𝑣.

All formulas 𝜑1–𝜑4 can be written in FO, and we can show that a graph satisfies all of them if and only if the graph is a gadgetised linear order.

In Theorem 10 we have showed how to express 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) with FO formulas 𝜑1–𝜑4. We observe that 𝜑1 and 𝜑2 are in C2, so by the result of Barceló et al. (2020), we can express them with ACR-GNNs. However 𝜑3 and 𝜑4 cannot be expressed by ACR-GNNs. However, as will show, 𝜑3 and 𝜑4 can be replaced with a property that is expressible by ACR-GNNs. This will show that 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is expressible by ACR-GNNs.

Theorem 11. Over undirected graphs, 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is expressible by an ACR-GNN.

Proof sketch. We can show that a graph 𝐺is a gadgetised linear order if and only if 𝐺satisfies 𝜑1, 𝜑2 (see the proof of Theorem 10) and a property 𝜓explained next. Property 𝜓states that for all 𝑖< 𝑗< |𝑃1|, the graph has nodes 𝑣𝑖 and 𝑣𝑗such that (1) both 𝑣𝑖and 𝑣𝑗satisfy 𝑃1, (2) 𝑣𝑖has 𝑖neighbours satisfying 𝑃2 and 𝑣𝑗has 𝑗such neighbours, and (3) there is a gadgetised edge (see the proof of Theorem 10) from 𝑣𝑗to 𝑣𝑖. Since 𝜑1 and 𝜑2 are C2 formulas, they can be expressed by ACR-GNNs (Barceló et al. 2020, Theorem 5.1). It remains to construct an ACR-GNN 𝒩 which expresses 𝜓, since it is straightforward to combine the three ACR-GNNs into a single GNN.

Recall that gadgetised linear orders are graphs of dimension three, so we will consider application of 𝒩to such graphs 𝐺. In each layer, 𝒩will assign to nodes vectors of dimesion five, where the first three positions are always as in the input graph 𝐺, so information about 𝑃1, 𝑃2, and 𝑃3 in the input graph is preserved across all layers. The fourth and fifth positions will always keep binary numbers. The details of 𝒩are provided next and and example of its application is visualised in Figure 4.

The first layer assigns to the fourth position of nodes 𝑣 satisfying 𝑃1 the number 10𝑛, where 𝑛is the number of neighbours of 𝑣satisfying 𝑃2. Fourth and fifth positions of other nodes are set to 0. The next three layers will compute bitwise 𝑂𝑅applied to binary numbers, for example 𝑂𝑅(100, 10, 10) = 110. The second layer assigns to the fourth position of nodes 𝑣satisfying 𝑃3 the value of 𝑂𝑅 over the fourth positions of 𝑣neighbours satisfying satisfy 𝑃1.

The third layer assigns to the fourth position of nodes 𝑣satisfying 𝑃2 the value of 𝑂𝑅over the fourth positions of 𝑣neighbours satisfying 𝑃3. The fourth layer assigns to the fifth position of nodes 𝑣satisfying 𝑃1 the value of 𝑂𝑅 over the fourth positions of 𝑣neighbours satisfying 𝑃2. Finally, the fifth layer uses a global readout to assign 1 to

𝑃1

(𝟏𝟎𝟎𝟎, 0)

L1:

𝑃1

(𝟏𝟎𝟎, 0)

𝑃1

(𝟏𝟎, 0)

𝑃1

(𝟏, 0)

𝑃2

(0, 0)

𝑃3

(0, 0)

𝑃2

(0, 0)

𝑃3

(0, 0)

𝑃2

(0, 0)

𝑃3

(0, 0)

𝑃2

(0, 0)

𝑃3

(0, 0)

𝑃2

(0, 0)

𝑃3

(0, 0) 𝑃2

(0, 0)

𝑃3

(0, 0)

𝑃1

(1000, 0)

L2:

𝑃1

(100, 0)

𝑃1

(10, 0)

𝑃1

(1, 0)

𝑃2

(0, 0)

𝑃3

(𝟏𝟎𝟎, 0)

𝑃2

(0, 0)

𝑃3

(𝟏𝟎, 0)

𝑃2

(0, 0)

𝑃3

(𝟏, 0)

𝑃2

(0, 0)

𝑃3

(𝟏𝟎, 0)

𝑃2

(0, 0)

𝑃3

(𝟏, 0) 𝑃2

(0, 0)

𝑃3

(𝟏, 0)

𝑃1

(1000, 0)

L3:

𝑃1

(100, 0)

𝑃1

(10, 0)

𝑃1

(1, 0)

𝑃2

(𝟏𝟎𝟎, 0)

𝑃3

(100, 0)

𝑃2

(𝟏𝟎, 0)

𝑃3

(10, 0)

𝑃2

(𝟏, 0)

𝑃3

(1, 0)

𝑃2

(𝟏𝟎, 0)

𝑃3

(10, 0)

𝑃2

(𝟏, 0)

𝑃3

(1, 0) 𝑃2

(𝟏, 0)

𝑃3

(1, 0)

𝑃1

(1000, 111)

L4:

𝑃1

(100, 11)

𝑃1

(10, 1)

𝑃1

(1, 0)

𝑃2

(100, 0)

𝑃3

(100, 0)

𝑃2

(10, 0)

𝑃3

(10, 0)

𝑃2

(1, 0)

𝑃3

(1, 0)

𝑃2

(10, 0)

𝑃3

(10, 0)

𝑃2

(1, 0)

𝑃3

(1, 0) 𝑃2

(1, 0)

𝑃3

(1, 0)

𝑃1

(1)

L5:

𝑃1

(1)

𝑃1

(1)

𝑃1

(1)

𝑃2

(1)

𝑃3

(1)

𝑃2

(1)

𝑃3

(1)

𝑃2

(1)

𝑃3

(1)

𝑃2

(1)

𝑃3

(1)

𝑃2

(1)

𝑃3

(1) 𝑃2

(1)

𝑃3

(1)

**Figure 4.** Application of the ACR-GNN from Theorem 11 to the graph from Figure 3; we present only the fourth and fifth components of vectors, and write in bold values updated in a given layer

each node if for all 𝑖< 𝑗< |𝑃1| there exists a node whose fourth position of the vector is 10𝑗and the fifth position of the vector has 1 as the 𝑖th bit from the right (when counting from 0).

The first four layers can be implemented without readout functions. The fifth layer, in contrast, requires using readout, but no aggregation. To show that the construction is correct, we can show that in layer 4, each node 𝑣 satisfying 𝑃1 has on the fourth position of its vector 10𝑗, where 𝑗is the number of 𝑣neighbours satisfying 𝑃2. On the fifth position 𝑣has a binary number, whose 𝑖th bit is 1 if there is a gadgetised edge from 𝑣to some node with 𝑖 neighbours satisfying 𝑃2. Therefore, the fifth layer assigns 1 to all nodes if the graphs satisfies 𝜓, and otherwise it assigns 0 to all nodes.

To finish this section, it remains to show that gadgetised linear orders are not expressible in C2. To this end, we will again use bounded WL from Section 3, as it is applicable to both directed and undirected graphs.

Theorem 12. Over undirected graphs, the classifier 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is not expressible in C2.

Proof sketch. The proof is similar to the one for Theorem 6, namely we suppose towards a contradiction that 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is expressible by a 𝐶2 𝓁,𝑐formula, for some 𝓁, 𝑐∈

21599

<!-- Page 7 -->

𝑊0

2:

𝑊1

2:

𝑊2

2:

𝑊3

2:

𝑊4

2:

𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5 𝑣−5 𝑣−4 𝑣−3 𝑣−2 𝑣−1 𝑣0 𝑣1 𝑣2 𝑣3 𝑣4 𝑣5

**Figure 5.** Application of WL2 to 𝐻 = 𝗀𝖺𝖽(𝐺), for 𝐺 from Theorem 6; for readability we draw only gadgetised edges corresponding to 𝑣𝑖, 𝑣𝑖+1 in 𝐺, as well as to edges (𝑣−5, 𝑣−3), (𝑣−1, 𝑣−1), and (𝑣2, 𝑣4), which helps to understand better the colourings

ℕ. In the proof of Theorem 6 we have obtained contradiction by applying 𝑊𝐿𝑐to directed graphs 𝐺and 𝐺′. Now, we will apply 𝑊𝐿𝑐to their gadgetisations 𝐻= 𝗀𝖺𝖽(𝐺) and 𝐻′ = 𝗀𝖺𝖽(𝐺′). Since 𝐺is a strict linear order, but 𝐺′ is not, we obtain that 𝐻is a gadgetised linear order, but 𝐻′ is not. Hence, by Theorem 2, it remains to show that 𝑊𝓁 𝑐outputs the same colourings on 𝐻and 𝐻′. The proof is similar as in Theorem 6. Colourings obtained by applying 𝑊𝓁 𝑐to 𝐻 are presented in Figure 5; application of 𝑊𝓁 𝑐to 𝐻′ results in the exactly same colourings.

By combining Theorems 10 and 11, we obtain a solution to the open problem of Barceló et al. (2020). Corollary 13. Over undirected graphs, there are FO node classifiers expressible by ACR-GNNs which are not expressible in C2. In particular, 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) is such a classifier.

The above result, shows that ACR-GNNs can express FO node classifiers beyond C2. Consequently, we establish that the converse of the result of Barceló et al. (2020, Theorem 5.1) does not hold. As we show in the following short section, our results have interesting implications beyond the expressive power of GNNs, contributing to a better understanding of the expressiveness of logics.

## 6 Impact on the Expressiveness of Logics

It turns out that our results can be used to show an interesting relation between the expressive power of finitary and infinitary logics. To formulate this result, let us use 𝗂𝗇𝖿-C2 for an extension of C2 which allows for infinitary conjunctions and disjunctions. Notice that the expressive power of 𝗂𝗇𝖿-C2 is not only beyond C2, but also beyond the whole FO. For example 𝗂𝗇𝖿-C2 allows us to express parity of a graph size using the infinite formula:

∃=2𝑥(𝑥= 𝑥) ∨∃=4𝑥(𝑥= 𝑥) ∨∃=6𝑥(𝑥= 𝑥) ∨… which is well-known to be inexpressible in FO—it can be shown by a standard application of Ehrenfeucht–Fraïssé games (Libkin 2004).

This naturally leads us to the question: what are the FO properties expressible in 𝗂𝗇𝖿-C2? It maybe tempting to assume that those are exactly the properties expressible in C2. In other words, that the (semantical) intersection of 𝗂𝗇𝖿-C2 and FO is exactly C2. As we show next, it is not true.

Theorem 14. There are strictly more FO properties expressible in 𝗂𝗇𝖿-C2 than the properties expressible in C2. This result holds both over directed and undirected graphs.

Proof sketch. Clearly each C2 property can be expressed in both FO and in 𝗂𝗇𝖿-C2. Thus, it suffices to show properties which disprove the opposite implication. For this, we can show that both 𝜑𝐿𝑖𝑛(𝑥) and 𝜑𝐺𝑎𝑑𝐿𝑖𝑛(𝑥) are expressible in 𝗂𝗇𝖿-C2. Indeed, by the results obtained in the paper it suffices to show that the third condition from Proposition 4 can be expressed in 𝗂𝗇𝖿-C2 over directed graphs as

⋀ 𝑖∈ℕ

∀𝑥∀𝑦(∃=𝑖𝑦𝐸(𝑥, 𝑦) ∧∃=𝑖𝑥𝐸(𝑦, 𝑥) →𝑥= 𝑦)

whereas 𝜓from Theorem 11 is expressed in 𝗂𝗇𝖿-C2 over undirected graphs as

⋀ 𝑖∈ℕ

⋀ 𝑗∈ℕ∶𝑖<𝑗

[∃𝑗+1𝑥𝑃1(𝑥) →∃𝑥(∃=𝑗𝑦(𝑃2(𝑦) ∧𝐸(𝑥, 𝑦))

∧𝑃1(𝑥) ∧∃𝑦(𝑃2(𝑦) ∧𝐸(𝑥, 𝑦) ∧∃𝑥

(

𝑃3(𝑥) ∧𝐸(𝑦, 𝑥)

∧∃𝑦(𝑃1(𝑦) ∧𝐸(𝑥, 𝑦) ∧∃=𝑖𝑥(𝑃2(𝑥) ∧𝐸(𝑦, 𝑥))))

))].

Note that both formulas rely on infinite conjunctions.

Conclusions In this paper, we have solved the open problem asking whether FO classifiers expressible by aggregate-combinereadout GNNs are exactly the classifiers expressible in logic C2 (Barceló et al. 2020). As we show, the answer is negative. In particular, over both directed and undirected graphs, FO classifiers expressible by ACR-GNNs have a strictly higher expressive power than C2. Recall that the distinguishing power of AC-GNNs is the same as of the 1-dimensional Weisfeiler-Leman algorithm, and so, the same as of C2. It turns out, however, that the logical (FO) expressive power of standard GNN architectures cannot be characterised by C2. In particular, AC-GNNs can express strictly less FO properties than C2, whereas ACR- GNNs can express strictly more FO properties than C2. Interestingly our results transfer to results on the expressive power of infinitary logics. As we have shown, the infinitary version of C2 can express strictly more FO properties than the standard, finitary, C2.

21600

<!-- Page 8 -->

## Acknowledgements

We are grateful to Bernardo Cuenca Grau for insightful comments and for drawing our attention to relevant work on the (in)definability of linear orders in fragments of first-order logics.

## References

Ahvonen, V.; Heiman, D.; Kuusisto, A.; and Lutz, C. 2025. Logical Characterizations of Recurrent Graph Neural Networks with Reals and Floats. arXiv:2405.14606. Babai, L.; and Kucera, L. 1979. Canonical Labelling of Graphs in Linear Average Time. In Proc. FOCS, 39–46. Barceló, P.; Kostylev, E. V.; Monet, M.; Pérez, J.; Reutter, J. L.; and Silva, J. P. 2020. The Logical Expressiveness of Graph Neural Networks. In Proc. of ICLR. Benedikt, M.; Lu, C.; Motik, B.; and Tan, T. 2024. Decidability of Graph Neural Networks via Logical Characterizations. In Proc. of ICALP. Besharatifard, M.; and Vafaee, F. 2024. A Review on Graph Neural Networks For Predicting Synergistic Srug Combinations. Artif. Intell. Rev., 57(3): 49. Cai, J.; Fürer, M.; and Immerman, N. 1992. An Optimal Lower Bound on The Number of Variables for Graph Identification. Comb., 12. Charatonik, W.; and Witkowski, P. 2016. Two-variable Logic with Counting and a Linear Order. Logical Methods in Computer Science, Volume 12, Issue 2. Chen, C.; Wu, Y.; Dai, Q.; Zhou, H.; Xu, M.; Yang, S.; Han, X.; and Yu, Y. 2024. A Survey on Graph Neural Networks and Graph Transformers in Computer Vision: A Task- Oriented Perspective. IEEE Trans. Pattern Anal. Mach. Intell., 46(12): 10297–10318. Derrow-Pinion, A.; She, J.; Wong, D.; Lange, O.; Hester, T.; Perez, L.; Nunkesser, M.; Lee, S.; Guo, X.; Wiltshire, B.; Battaglia, P. W.; Gupta, V.; Li, A.; Xu, Z.; Sanchez- Gonzalez, A.; Li, Y.; and Velickovic, P. 2021. ETA Prediction with Graph Neural Networks in Google Maps. In Proc. of CIKM, 3767–3776. Gilmer, J.; Schoenholz, S. S.; Riley, P. F.; Vinyals, O.; and Dahl, G. E. 2017. Neural Message Passing for Quantum Chemistry. In Proc. of ICML, 1263–1272. Grohe, M. 2021. The Logic of Graph Neural Networks. In Proc. of LICS, 1–17. Huang, X.; Orth, M. A. R.; Barceló, P.; Bronstein, M. M.; and Ceylan, İ. İ. 2025a. Link Prediction with Relational Hypergraphs. Trans. Mach. Learn. Res. Huang, X.; Romero, M.; Ceylan, İ. İ.; and Barceló, P. 2025b. Logical Expressiveness of Graph Neural Networks on Knowledge Graphs. In Handbook on Neurosymbolic AI and Knowledge Graphs, 68–95. Immerman, N.; and Kozen, D. 1989. Definability with Bounded Number of Bound Variables. Inf. Comput., 83(2): 121–139. Libkin, L. 2004. Elements of Finite Model Theory. Springer.

Lutz, C.; Sattler, U.; and Wolter, F. 2001. Modal Logic and the Two-Variable Fragment. In Proc. of CSL, 247–261. Morris, C.; Ritzert, M.; Fey, M.; Hamilton, W. L.; Lenssen, J. E.; Rattan, G.; and Grohe, M. 2019. Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks. In Proc. of AAAI, 4602–4609. Nunn, P.; Sälzer, M.; Schwarzentruber, F.; and Troquard, N. 2024. A Logic for Reasoning about Aggregate-Combine Graph Neural Networks. In Proc. of IJCAI, 3532–3540. Pflueger, M.; Tena Cucala, D.; and Kostylev, E. V. 2024. Recurrent Graph Neural Networks and Their Connections to Bisimulation and Logic. In Proc. of LICS, 14608–14616. Rossi, E.; Charpentier, B.; Giovanni, F. D.; Frasca, F.; Günnemann, S.; and Bronstein, M. M. 2023. Edge Directionality Improves Learning on Heterophilic Graphs. In Proc. of LoG. Schönherr, M.; and Lutz, C. 2025. Logical Characterizations of GNNs with Mean Aggregation. arXiv preprint arXiv:2507.18145. Szwast, W.; and Tendera, L. 2013. 𝐹𝑂2 with one transitive relation is decidable. In Proc. of STACS, 317–328. Tena Cucala, D. J.; and Cuenca Grau, B. 2024. Bridging Max Graph Neural Networks and Datalog with Negation. In Proc. of KRR. Tena Cucala, D. J.; Cuenca Grau, B.; Kostylev, E. V.; and Motik, B. 2022. Explainable GNN-Based Models over Knowledge Graphs. In Proc. of ICLR. Weisfeiler, B.; and Leman, A. 1968. The Reduction of a Graph to Canonical Form and the Algebra Which Appears Therein. Nauchno-Technicheskaya Informatsia. Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2019. How Powerful are Graph Neural Networks? In Proc. of ICLR. Ying, R.; He, R.; Chen, K.; Eksombatchai, P.; Hamilton, W. L.; and Leskovec, J. 2018. Graph Convolutional Neural Networks for Web-Scale Recommender Systems. In Proc. of KDD, 974–983. Zhang, M.; and Chen, Y. 2018. Link Prediction Based on Graph Neural Networks. In Proc. of NeurIPS, 5171–5181.

21601
