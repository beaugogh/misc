---
title: "UniHR: Hierarchical Representation Learning for Unified Knowledge Graph Link Prediction"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38569
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38569/42531
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# UniHR: Hierarchical Representation Learning for Unified Knowledge Graph Link Prediction

<!-- Page 1 -->

UniHR: Hierarchical Representation Learning for Unified Knowledge Graph

Link Prediction

Zhiqiang Liu1,3, Yin Hua1,3, Mingyang Chen4, Yichi Zhang1,3, Zhuo Chen1,3,

Lei Liang2,3, Wen Zhang1,3*

1Zhejiang University 2Ant Group 3ZJU-Ant Group Joint Lab of Knowledge Graph 4Baichuan Inc {zhiqiangliu,zhang.wen}@zju.edu.cn

## Abstract

Real-world knowledge graphs (KGs) contain not only standard triple-based facts, but also more complex, heterogeneous types of facts, such as hyper-relational facts with auxiliary key-value pairs, temporal facts with additional timestamps, and nested facts that imply relationships between facts. These richer forms of representation have attracted significant attention due to their enhanced expressiveness and capacity to model complex semantics in real-world scenarios. However, most existing studies suffer from two main limitations: (1) they typically focus on modeling only specific types of facts, thus making it difficult to generalize to real-world scenarios with multiple fact types; and (2) they struggle to achieve generalizable hierarchical (inter-fact and intra-fact) modeling due to the complexity of these representations. To overcome these limitations, we propose UniHR, a Unified Hierarchical Representation learning framework, which consists of a learning-optimized Hierarchical Data Representation (HiDR) module and a unified Hierarchical Structure Learning (HiSL) module. The HiDR module unifies hyperrelational KGs, temporal KGs, and nested factual KGs into triple-based representations. Then HiSL incorporates intrafact and inter-fact message passing, focusing on enhancing both semantic information within individual facts and enriching the structural information between facts. To go beyond the unified method itself, we further explore the potential of unified representation in complex real-world scenarios. Extensive experiments on 9 datasets across 5 types of KGs demonstrate the effectiveness of UniHR and highlight the strong potential of unified representations.

Code — https://github.com/zjukg/UniHR

## Introduction

Real-world large-scale knowledge graphs (KGs) such as Wikidata (Vrandeˇci´c and Kr¨otzsch 2014) and DBpedia (Lehmann et al. 2015) have been widely applied in many areas including question answering (Kaiser, Saha Roy, and Weikum 2021) and natural language processing (Annervaz, Chowdhury, and Dukkipati 2018; Liu et al. 2025). To faithfully represent complex real-world knowledge, these KGs

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

usually incorporate not only standard triple-based facts, but also more complex and heterogeneous types of facts such as hyper-relational, temporal and nested facts.

Despite the simplicity of triple-based representation (i.e., (head, relation, tail)), such forms struggle to capture the complexity of real-world facts, e.g., “Oppenheimer is educated at Harvard University for a bachelor degree in chemistry”. Consequently, recent studies (Xiong et al. 2023b) have focused on semantically richer beyond-triple facts, including: hyper-relational fact ((Oppenheimer, educated at, Harvard University), degree: bachelor, major: chemistry), temporal fact (Oppenheimer, honored with, Fermi Prize, 1963), nested fact ((Oppenheimer, born in, New York), imply, (Oppenheimer, nationality, The United States)). These fact types allow for expression of complex semantics and revelation of relationships between facts. Thus in recent years, Hyper-relational KGs (HKG) (Luo et al. 2023), Temporal KGs (TKG) (Zhang et al. 2025), and Nested factual KGs (NKG) (Li et al. 2025) attract wide research interests.

We find that existing research mainly suffers from two major limitations: (1) They fail to reflect real-world scenarios with multiple heterogeneous fact types (Xiong et al. 2023b), instead artificially dividing and only modeling a single KG type; (2) Earlier triple-based studies (Chen et al. 2021) have demonstrated the effectiveness of hierarchical fact semantic modeling (inter-fact and intra-fact). But due to the complexity of beyond-triple representations, they struggle to achieve comprehensive hierarchical semantic modeling, even generalizing to other fact types. Specifically, for HKGs, StarE (Galkin et al. 2020) customizes GNN to enhance inter-fact interactions, while GRAN (Wang et al. 2021) designs attention variants with edge-bias to capture intra-fact heterogeneity. For NKGs, NestE (Xiong et al. 2024) et al. NKG methods connect bi-level facts and only score intra-fact semantics. For TKGs, either by explicitly incorporating temporal information into the score function like GeomE+ (Xu et al. 2023), or by unfolding entity neighborhood subgraphs along temporal chain and capturing inter-fact semantics to model temporal information like ECEformer (Fang et al. 2024). Although advanced methods like HAHE (Luo et al. 2023) begin to capture hierarchical semantics for HKGs, their heterogeneity in representation limits their scalability to other fact types. Therefore,

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

15421

<!-- Page 2 -->

establishing a unified hierarchical representation learning method for real-world KG with multiple fact types is worth investigating.

To fill this research gap, we propose UniHR, a Unified Hierarchical Representation learning framework, which includes a Hierarchical Data Representation (HiDR) module and a Hierarchical Structure Learning (HiSL) module. HiDR module standardizes hyper-relational facts, nested factual facts, and temporal facts into the form of triples without loss of information. Furthermore, HiSL module captures local semantic information during intra-fact message passing and then utilizes inter-fact message passing to enrich the global structure information to obtain better node embeddings based on HiDR form. Finally, the updated embeddings are fed into decoders for link prediction. Apart from the unification of method itself, UniHR’s unified representation enables flexible extensions. Unlike previous KG-specific models, UniHR accommodates more complex scenarios, such as compositional knowledge graphs, multi-task learning, and joint training on hybrid facts, thereby paving the way for pre-trained models across diverse KG types. Our contributions can be summarized as follows.

• We emphasize the value of investigating unified KG representation learning method, including unified symbolic representation and unfied learning for different KGs. • To our knowledge, we propose the first unified KG representation learning framework UniHR, across different types of KGs, including a hierarchical data representation module and a hierarchical structure learning module. • We conduct link prediction experiments on 9 datasets across 5 types of KGs. Compared to KG-specific methods, UniHR achieves the best or competitive results, verifying strong generalization capability.

## Preliminaries

Link Prediction on Triple-based KG. A triple-based KG GKG = {V, R, F} represents facts as triples, denoted as F ={(h, r, t) |h, t ∈V, r ∈R}, where V is the set of entities and R is the set of relations. The link prediction on triplebased KGs involves answering a query (h, r,?) or (?, r, t), where the missing element ‘?’ is an entity in V.

Link Prediction on Hyper-relational KG. A hyperrelational KG (HKG) GHKG = {V, R, F} consists of hyperrelational facts (H-Facts) F, denoted as F ={((h, r, t), {(ki: vi)}m i=1)| h, t, vi ∈V, r, ki ∈R}. Typically, we refer to (h, r, t) as the main triple and {(ki: vi)}m i=1 as m auxiliary key-value pairs. Link prediction on HKGs aims to predict entities in the main triple or the key-value pairs. Symbolically, the aim is to predict the missing element, denoted as ‘?’ for queries ((h, r, t), (k1: v1),... (ki:?)), ((?, r, t), {(ki:vi)}m i=1) or ((h, r,?), {(ki:vi)}m i=1).

Link Prediction on Nested Factual KG. A nested factual KG (NKG) can be represented as GNKG = {V, R, F, ˆR, ˆF}, which is composed of two levels of facts, called atomic facts and nested facts. F = {(h, r, t) |h, t ∈V, r ∈R} is the set of atomic facts, where V is a set of atomic entities and R is a set of atomic relations. ˆF = {(Fi, ˆr, Fj) | Fi, Fj ∈F, ˆr ∈ˆR}

is the set of nested facts, where ˆR denotes nested relations. We refer to the link prediction on atomic facts as Base Link Prediction, and the link prediction on nested facts as Triple Prediction. For base link prediction, given a query (h, r,?) or (?, r, t), the aim is to predict missing atomic entity ‘?’ from V. For triple prediction, given a query (?, ˆr, Fj) or (Fi, ˆr,?), the aim is to predict atomic fact ‘?’ from F.

Link Prediction on Temporal KG. A temporal KG (TKG) GTKG = {V, R, F, T } is composed of quadruplebased facts, represented as F = {(h, r, t, [τb, τe])|h, t ∈V, r ∈R, τb, τe ∈T }, where τb is the begin time, τe is the end time, V is the set of entities, R is the set of relations and T is the set of timestamps. The link prediction on TKGs aims to predict missing entities ‘?’ in V for two types of queries (?, r, t, [τb, τe]) or (h, r,?, [τb, τe]).

Related Works

Link Prediction on Hyper-relational Knowledge Graph. Early HKG methods typically focus on modeling either local or global information. Galkin et al. (2020) customize StarE based on CompGCN (Vashishth et al. 2019) for H-Facts to capture global structure information among H-Facts, demonstrating the importance of structure information in HKGs. GRAN (Wang et al. 2021) with edge-aware bias in attention (Vaswani et al. 2017) layer, HyNT (Chung, Lee, and Whang 2023) with qualifier-aware encoder, and ShrinkE with relation-specific box (Xiong et al. 2023a) all focus on modeling intra-fact semantic information. Recent advanced methods aim to comprehensively capture both inter-fact and intra-fact information. For example, HAHE (Luo et al. 2023) employs dual-graph attention and edge-aware bias in the transformer attention layer for hierarchical modeling, achieving significant performance improvements. Similarly, HyperSAT (Wang, Chen, and Zhang 2025) accomplishes this through a combination of graph sampling and a keyvalue joint attention mechanism. We consider hierarchical modeling of KGs to be a promising direction, existing approaches are customized for HKG form and difficult to generalize to other types of facts.

Link Prediction on Nested Factual Knowledge Graph. Chung et al. (Chung and Whang 2023) are the first to introduce nested facts to model relationships between facts, and also propose BiVE which bridges semantics between atomic facts and fact nodes via a simple MLP and scores both atomic facts and nested facts using quaternion-based KGE scoring functions like QuatE (Zhang et al. 2019) or BiQUE (Guo and Kok 2021). Based on BiVE, NestE (Xiong et al. 2024) represents fact nodes using a 1 × 3 embedding matrix and the nested relations as a 3 × 3 matrix to avoid information loss. GRADATE (Li et al. 2025) enhances entity and fact representation learning by mining latent intra-fact semantics. However, due to the complexity of NKG representations, existing methods have so far primarily focused on capturing intra-fact semantic information.

Link Prediction on Temporal Knowledge Graph. Recent studies on TKG representation learning have mainly

15422

<!-- Page 3 -->

h t r v 𝒆𝒓 h t r v a f a

HKG h t r 𝒕𝒆 𝒆𝒓 h t r

TKG

[𝒕𝒃, 𝒕𝒆]

𝒕𝒃 f 𝒕𝟏 𝒓𝟏

NKG 𝒉𝟏 𝒕𝟐 𝒓𝟐 𝒉𝟐

R 𝒇𝟏 𝒇𝟐 𝒕𝟏 𝒉𝟏 𝒕𝟐 𝒉𝟐 𝒆𝒓𝟏 𝒆𝒓𝟐

R 𝒇𝟏 𝒇𝟐

ℱ!"#

!$%&= { ℎ, 𝑟, 𝑡, 𝑓, 𝑎, 𝑣, 𝑓, ℎ𝑎𝑠 𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛, 𝑒% 𝑓, ℎ𝑎𝑠 ℎ𝑒𝑎𝑑 𝑒𝑛𝑡𝑖𝑡𝑦, ℎ, 𝑓, ℎ𝑎𝑠 𝑡𝑎𝑖𝑙 𝑒𝑛𝑡𝑖𝑡𝑦, 𝑡}

ℱ'"#

!$%&= { 𝑓, ℎ𝑎𝑠 ℎ𝑒𝑎𝑑 𝑒𝑛𝑡𝑖𝑡𝑦, ℎ, 𝑓, ℎ𝑎𝑠 𝑡𝑎𝑖𝑙 𝑒𝑛𝑡𝑖𝑡𝑦, 𝑡 𝑓, ℎ𝑎𝑠 𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛, 𝑒%, 𝑓, 𝑏𝑒𝑔𝑖𝑛, 𝑡&, 𝑓, 𝑒𝑛𝑑, 𝑡', ℎ, 𝑟, 𝑡}

ℱ("#

!$%&= { 𝑓(, ℎ𝑎𝑠 𝑟𝑒𝑙𝑎𝑡𝑖𝑜𝑛, 𝑒%%, 𝑓(, ℎ𝑎𝑠 ℎ𝑒𝑎𝑑 𝑒𝑛𝑡𝑖𝑡𝑦, ℎ(, 𝑓(, ℎ𝑎𝑠 𝑡𝑎𝑖𝑙 𝑒𝑛𝑡𝑖𝑡𝑦, 𝑡(, ℎ(, 𝑟(, 𝑡(|𝑖= 1,2} ∪{ 𝑓), 𝑅, 𝑓* }

relation atomic fact connected atomic nested end begin

Node

Relation

**Figure 1.** Diverse beyond-triple facts are translated into the hierarchical data representation (HiDR) form.

focused on designing elegant time-aware modules to enhance representation capability. Advanced models like TGeomE+ (Xu et al. 2023) improve the modeling of local semantics in TKGs through 4th-order tensor factorization and linear temporal regularization. Similarly, HGE (Pan et al. 2024) and 5EL (Zhang et al. 2025) enhance the expressiveness of temporal spaces by introducing geometric spaces. In contrast, ECEformer (Fang et al. 2024) captures only interfact semantics by unfolding entity neighborhood subgraphs along the temporal chain to model temporal information. However, TKG representation learning methods that can simultaneously capture both intra-fact temporal semantics and global structural information remain largely unexplored. UniHR achieves this by regarding timestamps as nodes and directly employing hierarchical message passing.

## Methodology

In this section, we introduce UniHR, a Unified Hierarchical Representation learning framework, which includes a Hierarchical Data Representation (HiDR) module and a Hierarchical Structure Learning (HiSL) module. Our workflow includes the following three steps: (1) Given a KG G of any type, we represent it into HiDR form GHiDR. (2) The GHiDR will be encoded by HiSL module to enhance the se- mantic information within individual facts and structural information between facts on the whole graph. (3) In the phase of decoding, the updated node and edge embeddings are serialized and fed into the transformer to optimize the model.

Hierarchical Data Representation To overcome the limitations of beyond-triple representations in hierarchical modeling, we introduce a Hierarchical Data Representation module (HiDR), which is optimized for representation learning.

Unlike existing triple-based systems (Ali et al. 2022) including RDF (triple) reification, RDF-star and labeled RDF representation techniques, we constrain “triple” to serve as the basic units of HiDR form, and split “nodes” and “relations” into three types respectively, making it more suitable for graph representation learning. Meanwhile, “triple” form makes HiDR could continuously benefit from the model developments of triple-based KGs, which is the most active area of research for link prediction over KGs.

As shown in Figure 1, we denote the entities in original KGs as atomic nodes and abstract fact nodes for HKGs and TKGs lacking a designated fact node. To facilitate the interaction between fact nodes and relations explicitly, we incorporate relation nodes into the graph, represented as er for each relation r. To facilitate direct access of fact nodes to the relevant atomic nodes during message passing, we also introduce three connected relations: has relation, has head entity and has tail entity, which establish directly connections between atomic nodes and fact nodes. Ultimately, we denote the (main) triple (h, r, t) in original fact as three connected facts: (f, has relation, er), (f, has head entity, h), (f, has tail entity, t), and an atomic fact (h, r, t), where f is fact node. Formally, the definition of HiDR form is as follows:

Definition 1. Hierarchical Data Representation (HiDR): A KG represented as the HiDR form is denoted as GHiDR = {VHiDR, RHiDR, FHiDR}, where VHiDR = Va∪Vr∪Vf is a joint set of atomic node set (Va), relation node set (Vr), fact node set (Vf). RHiDR = Ra ∪Rn ∪Rc is a joint set of atomic relation set (Ra), nested relation set (Rn), connected relation set Rc ={has relation, has head entity, has tail entity}. The fact set FHiDR = Fa ∪Fc ∪Fn is jointly composed of three types of triple-based facts: atomic facts (Fa), connected facts (Fc) and nested facts (Fn), where Fa= {(v1, r, v2)| v1, v2 ∈Va, r ∈Ra}, Fc = {(v1, r, v2)| v1 ∈Vf, r ∈ Rc, v2 ∈Va}, Fn = {(v1, r, v2)| v1, v2 ∈Vf, r ∈Rn}.

Next, we introduce how to transform different types of beyond-triple KGs into HiDR form. For HKGs, we regard the key-value pairs as complementary information for facts. Thus, we translate the H-Facts FHKG ={((h, r, t), {(ki: vi)}m i=1} into the HiDR form that GHiDR

HKG = {V, R, FHiDR

HKG } following the definition, where Fc = {(f, has relation, er), (f, has head entity, h), (f, has tail entity, t), (f, k1, v1),..., (f, km, vm)}, Fa={(h, r, t) |((h, r, t), {(ki: vi)}m i=1) ∈FHKG)} and Fn= ∅. For NKGs, HiDR can naturally represent the hierarchical facts, so we translate the atomic facts FNKG = {(hi, ri, ti)} and the nested facts ˆFNKG = {((h1, r1, t1), R, (h2, r2, t2))|

15423

![Figure extracted from page 3](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

intra-fact subgraph h t v 𝒆𝒓 𝛼!,# 𝛼$,# 𝛼%!,# 𝛼&,#

Aggregation f

Transformer

Decoder Multiple KGs Hierarchical Data

Representation

Hierarchical Structure Learning

𝒢!"#$ forward reverse

Aggregation

𝒢!"#$ fact-level atomic-level

Sequence relation atomic fact connected atomic nested arbitrary arbitrary

Node

Relation intra-fact message passing inter-fact message passing

**Figure 2.** The overview of UniHR, including HiSL module for intra-fact and inter-fact message passing.

(hi, ri, ti) ∈FNKG} into the form of HiDR that GHiDR

NKG = {V, R, FHiDR

NKG } following the definition, where Fa = {(hi, ri, ti)| (hi, ri, ti) ∈FNKG}, Fc ={(fi, has head entity, hi), (fi, has tail entity, ti), (fi, has relation, eri)|fi = (hi, ri, ti) ∈ FNKG} and Fn={(f1, R, f2)|fi ∈FNKG}. For TKGs, we regard the TKG as a special HKG, and convert timestamps to auxiliary key-value pairs in HKGs by adding two special atomic relations: begin and end, regarding timestamps as special numerical atomic nodes. Thus, we firstly translate the temporal facts in TKGs FTKG= {(h, r, t, [τb, τe])} into H-Facts form FHKG

TKG = {(h, r, t, begin:τb, end:τe)}. Then according to the previous transformation in HKG, it can be translated into the HiDR form that GHiDR

TKG ={V, R, FHiDR

TKG } following the definition, where Fa = {(h, r, t) | (h, r, t, begin: τb, end:τe) ∈FHKG

TKG }, Fc = {(f, has relation, er), (f, has head entity, h), (f, has tail entity, t), (f, begin, τb), (f, end, τe) | f = (h, r, t, begin: τb, end: τe) ∈FHKG

TKG } and Fn = ∅. In summary, HiDR serves as a module that dynamically transforms the original data into a unified representation optimized for the model, without altering the storage format of the original data. Moreover, from the perspective of graph learning, it fully preserves the semantics of the original knowledge graphs without any loss of information.

Hierarchical Structure Learning It’s evident that HiDR form introduces many additional relation nodes and fact nodes. To avoid significantly increasing the model’s training parameters while fully capturing the hierarchy of HiDR form, we design a Hierarchical Structure Learning module, abbreviated as HiSL shown in Figure 2.

Representation Initialization. We first initialize the embedding matrices Ha ∈R|Va|×d and E ∈R|RHiDR|×d for atomic nodes and all relation edges. Then we also initialize the embedding of relation node Hr ∈R|Vr|×d, which can be transformed from the relation edge r with a projection matrix Wr ∈Rd×d: Hr = Ea · Wr, where Ea ⊆E is the atomic relation embeddings. Then we initialize the fact node embeddings Hf to explicitly capture key information within facts by utilizing the embedding of (main) triple:

hf = fm([hh; hr; ht]), (1)

where (h, r, t) ∈Fa, fm: R3d →Rd is a 1-layer MLP, [·; ·] is the concatenation, hh, ht ⊆Ha, hr ⊆Hr denote (main) triple embedding. Therefore, the initialization of relation nodes and fact nodes is sufficiently parameter-efficient.

For numerical atomic nodes, namely timestamps in temporal knowledge graphs, we encode the timestamp τ into an embedding with Time2Vec (Kazemi et al. 2019): hτ = ωp sin (fp(τ))+fnp(τ), where fp: R1 →Rd and fnp:R1 → Rd are both 1-layer linear layers as periodic and nonperiodic functions, and ωp ∈R1 is a learnable parameter for scaling the periodic features.

Intra-fact Message Passing. In this stage, massage passing is conducted for fact nodes. Given a fact node fk ∈Vf, we construct its constituent elements, i.e., one-hop neighbors, as the node set Vk = {v ∈Nfk | v ∈Va ∪Vr}, where Nfk is the set of one-hop neighbors of fact node fk. Then we retain the edges directly connected to fact node fk, thereby constructing a subgraph Gk = {Vk, Rk, Fk} ⊆GHiDR. For this subgraph, we employ the graph attention to aggregate local information, computing the attention score αi,j between node i ∈Vk and its neighbor j. The formula for calculating αi,j in the l-th layer is as follows:

αl i,j = exp(Wl(σ(Wl inhl i+Wl outhl j))) P j′∈Ni exp

Wl σ

Wl inhl i+Wl outhl j′

, (2)

where hl i, hl j ∈Rd represent the embeddings of node i and its neighbor j in l-th layer. And there are three learnable weight matrices Wl in, Wl out ∈Rd×d and Wl ∈Rd. We choose LeakyReLU as activation function σ. Then, the updated node embeddings are obtained by aggregating the information of neighbors according to the attention scores:

hl i = hl i + P j∈Ni αl i,j · Wl outhl j. (3)

Inter-fact Message Passing. At this stage, message passing is conducted on the whole graph GHiDR. Specifically, we use a non-parametric aggregation operator ϕ (·):Rd ×Rd → Rd to obtain messages from neighbouring nodes and edges. We employ the circular-correlation operator, defined as:

ϕ (hj, er) = hj ⋆er = F−1

(Fhj) ⊙(Fer)

, (4)

15424

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-004-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

WikiPeople WD50K

## Model

subject/object all entities subject/object all entities

MRR H@1 H@10 MRR H@1 H@10 MRR H@1 H@10 MRR H@1 H@10

NaLP (Guan et al. 2019) 0.356 0.271 0.499 0.360 0.275 0.503 0.230 0.170 0.347 0.251 0.187 0.375 StarE (Galkin et al. 2020) 0.458 0.364 0.611 - - - 0.309 0.234 0.452 - - - GRAN (Wang et al. 2021) 0.477 0.408 0.596 0.480 0.411 0.599 0.329 0.259 0.465 0.363 0.294 0.493 tNaLP (Guan et al. 2023) 0.358 0.288 0.486 0.361 0.290 0.490 0.221 0.163 0.331 0.243 0.182 0.360 HyNT (Chung, Lee, and Whang 2023) 0.479 0.411 0.601 0.478 0.409 0.601 0.328 0.256 0.468 0.356 0.285 0.493 ShrinkE (Xiong et al. 2023a) 0.485 0.431 0.601 - - - 0.345 0.275 0.482 - - - HAHE∗(Luo et al. 2023) 0.498 0.418 0.610 0.497 0.421 0.614 0.343 0.269 0.484 0.378 0.306 0.515 NYLON∗(Yu, Yang, and Yang 2024) 0.385 0.299 0.527 0.384 0.300 0.520 0.326 0.262 0.446 0.291 0.226 0.414 HyperSAT (Wang, Chen, and Zhang 2025) 0.493 0.427 0.610 0.496 0.430 0.613 0.345 0.270 0.489 0.380 0.306 0.520

UniHR 0.496 0.419 0.619 0.496 0.420 0.621 0.348 0.278 0.482 0.382 0.313 0.517

**Table 1.** Results on HKG datasets, ∗are reproduced by us and others are taken from (Wang, Chen, and Zhang 2025).

where F and F−1 denote the discrete fourier transform (DFT) matrix and its inverse matrix, and the ⊙is the element-wise product. In order to fully capture the graph’s heterogeneity, we classify edges along two dimensions: direction λ(r) ∈{forward, reverse} and type τ(r) ∈ {connected relation, atomic relation, nested relation} and adopt two relation-specific learnable parameters Wλ(r) ∈Rd×d and ωτ(r) ∈R1 for fine-grained aggregation:

hl+1 i = P

(r,j)∈N(i)

σ ωl τ(r)

Wl λ(r)ϕ hl j, el r

+ Wl selfhl i, (5)

where Wl self ∈Rd×d, σ is a sigmoid function and N (i) is a set of immediate neighbors of i for its outgoing edges r. We utilize ϕ (·) to combine the information from edge r and node j, and then passes it to node i for update. Meanwhile, we update the relation representation as: el+1 r = Wl relel r. Through Intra-fact and Inter-fact two-stage message passing, nodes can fully capture both local semantic and global structural information. Moreover, the number of training parameters does not increase with the scale of the graph, thereby effectively adapting to the HiDR form.

Link Prediction Decoder

Since the query varies across different settings, we use the transformer (Vaswani et al. 2017) as the decoder with mask pattern. Specifically, we serialize the updated node and edge embeddings into a sequence of fact embeddings, mask the elements to be predicted in facts with the [M] token as the input. Finally, we obtain the embedding of output [M] in the last layer to measure the plausibility of the fact, denoted as hpre, and calculate the probability distribution of candidates, followed by training it using the cross-entropy loss:

L =

|R|+|V| X t=0 yt log Pt, (6)

where P = Softmax f (hpre) [E; H]⊤

∈R|R|+|V| represents the confidence scores of all candidates, f: Rd →Rd is a 1-layer MLP, and [E; H] ∈R(|R|+|V|)×d is the embedding matrix of all candidate edges or nodes. The Pt and yt are probability and ground truth of the t-th candidate.

## Experiment

## Experiment

Settings

Datasets. For HKGs, we use WikiPeople (Guan et al. 2019) and WD50K (Wang et al. 2021). For NKGs, we select FBH, FBHE and DBHE (Chung and Whang 2023). For TKGs, we use wikidata12k (Dasgupta, Ray, and Talukdar 2018). To further evaluate the potential of the unified representation, we further introduce hyper-relational TKG datasets WIKI-hy and YAGO-hy (Ding et al. 2024).

## Evaluation

Metric. We use the MR (Mean Rank), MRR (Mean Reciprocal Rank) and Hits@K (K=1,3,10) as our evaluation metrics. We abbreviate ‘Hits@K’ as ‘H@K’ and employ filtering settings (Bordes et al. 2013) during the evaluation to eliminate existing facts in the dataset. It is worth noting that for the query ((h, r,?), (ki: vi)m i=1) in HKGs, there are two evaluation filtering settings in existing models: one that filters out facts satisfying ((h, r,?), (ki: vi)m i=1) and another that filters out facts satisfying only (h, r,?) in the training set. Similarly, the difference in filtering settings of TKG occurs in timestamp. In this paper, we adopt the strict filtering setting of the former. To ensure fair comparison, for HKG we utilize the results of HyperSAT (Wang, Chen, and Zhang 2025) with the same settings as ours. For TKG, we thoroughly review the original code of our baselines and reproduce the results of some methods.

Baselines. For HKG, we compare with NaLP (Guan et al. 2019), StarE (Galkin et al. 2020), GRAN (Wang et al. 2021), tNaLP (Guan et al. 2023), HyNT (Chung, Lee, and Whang 2023), ShrinkE (Xiong et al. 2023a), HAHE (Luo et al. 2023), NYLON (Yu, Yang, and Yang 2024) and HyperSAT (Wang, Chen, and Zhang 2025). For NKG, QuatE (Zhang et al. 2019), BiQUE (Guo and Kok 2021), BiVE (Chung and Whang 2023), NestE (Xiong et al. 2024), HOKE (Pirr`o 2025) and GRADATE (Li et al. 2025) are chosen as baselines. For TKG, we compare against following methods: ATiSE (Xu et al. 2019), TGeomE+ (Xu et al. 2023), HGE (Pan et al. 2024), DuaTHP (Chen et al. 2025), ECEformer (Fang et al. 2024) and 5EL (Zhang et al. 2025).

Implementation details. All experiments are conducted on a single Nvidia 80G A800 GPU and implemented with PyTorch. For base link prediction on NKGs, we also use

15425

<!-- Page 6 -->

FBH DBHE FBH FBHE DBHE

## Model

MRR H@10 MRR H@10 MR MRR H@10 MR MRR H@10 MR MRR H@10

Base link prediction Triple prediction

QuatE (Zhang et al. 2019) 0.354 0.581 0.264 0.440 145603.8 0.103 0.114 94684.4 0.101 0.209 26485.0 0.157 0.179 BiQUE (Guo and Kok 2021) 0.356 0.583 0.274 0.446 81687.5 0.104 0.115 61015.2 0.135 0.205 19079.4 0.163 0.185 BiVE (Chung and Whang 2023) 0.370 0.607 0.274 0.422 6.20 0.855 0.941 8.35 0.711 0.866 3.63 0.687 0.958 NestE (Xiong et al. 2024) 0.371 0.608 0.289 0.443 3.34 0.922 0.982 3.05 0.851 0.962 2.07 0.862 0.984 HOKE (Pirr`o 2025) - - - - 3.06 0.719 0.777 2.82 0.674 0.764 2.10 0.674 0.777 GRADATE (Li et al. 2025) - - - - 18.15 0.780 0.871 26.81 0.603 0.757 4.72 0.654 0.916

UniHR 0.401 0.619 0.296 0.448 2.46 0.946 0.993 5.20 0.793 0.890 1.90 0.862 0.987

**Table 2.** Results of base link prediction and triple prediction. Results of NKG-specific methods are taken from original papers.

## Model

wikidata12k

MRR H@1 H@3 H@10

ATiSE (Xu et al. 2019) 0.252 0.148 0.288 0.462 TGeomE+ (Xu et al. 2023) 0.333 0.232 0.361 0.546 HGE∗(Pan et al. 2024) 0.290 0.176 0.323 0.514 ECEformer∗(Fang et al. 2024) 0.262 0.159 0.255 0.462 DuaTHP (Chen et al. 2025) 0.304 0.209 0.331 0.509 5EL (Zhang et al. 2025) 0.311 0.237 0.355 0.546

UniHR 0.334 0.242 0.368 0.527

**Table 3.** Results of link prediction on wikidata12k. Results∗ are reported by us, and others are taken from original papers.

augmented triples from (Chung and Whang 2023) for training to ensure fairness. For triple prediction, due to the small size of training set, we conduct training based on fixed embeddings of entities obtained from the base link prediction and set ωnested relation= 0 to prevent overfitting.

Main Results Link Prediction on HKG. We compare our method with previous methods on the WD50K and WikiPeople datasets shown in Table 1. Among these methods, it can be seen that our proposed UniHR achieves competitive results with the state-of-the-art method HAHE and HyperSAT, which means our method effectively captures hierarchical fact information. Compared to GNN-based method StarE, we achieve improvements of 3.9 points (12.6%) in MRR, 4.4 points (18.8%) in Hits@1 and 3.0 points (6.6%) in Hits@10 on WD50K. This indicates that the performance of StarE’s customized GNN is limited by its inability to flexibly capture key-value pair information and hierarchical semantics.

Link Prediction on NKG. From the results in Table 2, we can see that our proposed UniHR obtains competitive results as the first method to capture global structural information of NKGs. For base link prediction task on triple-based KGs, UniHR achieves considerable improvements. Of particular note, the MRR of FBHE increases by 8.1%.

For triple prediction, we perform best on FBH and DBHE datasets, especially obtaining an improvement of 2.4 points in MRR on FBH, and achieve the second-best performance on FBHE, which suggests that structural information is also valuable for NKG and UniHR can effectively capture the heterogeneity of NKG to enhance node embeddings. Unlike previous methods that use customized decoders for triples, our unified approach does not.

Variant FBHE (N) DB15K (H) wikidata12k (T)

MRR H@10 MRR H@10 MRR H@10 w/o initial hf 0.767 0.885 0.346 0.481 0.333 0.525 w/o Wr 0.792 0.885 0.346 0.480 0.331 0.521 w/o intra-fact MP 0.754 0.883 0.341 0.471 0.321 0.515 w/o ωτ(r) 0.782 0.888 0.342 0.476 0.328 0.522 w/o Wλ(r) 0.778 0.889 0.341 0.474 0.327 0.521 w/o inter-fact MP 0.776 0.887 0.338 0.468 0.319 0.511

UniHR 0.793 0.890 0.348 0.482 0.334 0.527

**Table 4.** Results of ablation studies on three KG types.

Link Prediction on TKG. As shown in Table 3, we achieve competitive results on wikidata12k, even surpassing TGeomE+ by 4.3% on Hits@1 and 1.9% on Hits@3. However, existing TKG methods (e.g, TGeomE+ and HGE with temporal-augmented triple encoding, or ECEformer with temporal-guided subgraph encoding) only focus on partial factual semantics. In contrast, our approach efficiently encodes timestamps as atomic nodes only during initialization and learns temporal information through message passing on graph structure, demonstrating that graph structure information is also beneficial for temporal knowledge graphs.

Ablation Study on HiSL To analyze the contribution of different modules across various KG types, we present ablation results in Table 4. It can be observed that both intra-fact and inter-fact message passing contribute to performance improvement. In particular, intra-fact message passing proves to be more beneficial for NKGs. We attribute this to fact nodes in NKGs being inherently composed of other atomic nodes, making triple prediction rely heavily on comprehensive bi-level fact semantics. In contrast, HKGs and TKGs focus solely on atomic nodes, whose representations are not dependent on other nodes. Therefore, inter-fact message passing, by capturing the global context among facts, works more effective for HKGs and TKGs, leading to better performances.

Potential of Unified Representation Generalize to Compositional KGs. Owing to its unified representation, UniHR can flexibly generalize to compositional knowledge graphs, such as hyper-relational temporal KGs (HTKGs) (Ding et al. 2024), which integrate the characteristics of both HKGs and TKGs. In HTKGs, each hyper-relational fact is associated with a timestamp that explicitly indicates its temporal validity. As shown in Table

15426

<!-- Page 7 -->

s/o entities all entities

WikiPeople∗ wikidata12k∗

(b)

FBH DBHE FBH DBHE

(a)

base link prediction triple prediction

MRR H@10 MRR H@10 MRR H@10 MRR H@10 1-!"

#$$$ MRR H@1 H@10 1-!"

#$$$ MRR H@1 H@10 1-

!"

#$$$ MRR H@1 H@10

**Figure 3.** (a) improvements of joint training on hybrid tasks. (b) improvements of joint training on wikimix dataset with hybrid fact forms. Yellow region indicates improvements achieved by joint training.

## Model

WiKi-hy YAGO-hy

MRR H@1 H@3 H@10 MRR H@1 H@3 H@10

HGE 0.602 0.507 0.666 0.765 0.790 0.760 0.814 0.837 StarE 0.565 0.491 0.599 0.703 0.765 0.737 0.776 0.820 GRAN 0.661 0.610 0.679 0.750 0.808 0.789 0.817 0.842 HyNT 0.537 0.444 0.587 0.723 0.763 0.724 0.787 0.836 HypeTKG 0.687 0.633 0.710 0.789 0.832 0.817 0.838 0.857

UniHR 0.692 0.626 0.716 0.792 0.841 0.810 0.841 0.862

**Table 5.** Results on hyper-relational TKG datasets.

5, UniHR offers a performance improvement in link prediction tasks on HTKGs, outperforming both TKG-specific and HKG-specific models. This result illustrates the strong ability of UniHR to jointly model auxiliary key-value pairs and temporal information. Furthermore, UniHR achieves competitive performance with the specialized model HypeTKG, despite not relying on complex module stacking.

Joint Learning on Different Tasks of KGs. For link prediction on NKGs, the two subtasks, namely base link prediction and triple prediction, share the same KG during the message-passing phase under our unified representation form. Therefore, we attempt joint training on two tasks using the NKG dataset, as shown in Fig 3(b). Consistent with previous studies (Li et al. 2025), we also observe that results of joint training are generally superior to those of separate training, further confirming that nested and atomic facts can mutually enhance and complement each other’s semantics.

Joint Learning on Different Types of KGs. We believe unified representation is key to develop pre-trained models that integrate multiple KG types. To explore this potential, we jointly train on different KG types. Thus, we construct a hybrid dataset wikimix, by filtering two Wikidata subsets: HKG WikiPeople and TKG wikidata12k, which share 3,546 entities and 18 relations but have no overlapping facts. To prevent data leakage, we remove test entries whose main triples appear in the other subset’s train set. As shown in Figure 3(a), we find joint learning outperforms separate learning across most metrics. Notably, MR improves by 17.1% on HKG and 39.7% on TKG, indicating that leveraging richer structural interactions across different fact types facilitates more effective representation learning.

As shown in Figure 4, entity embeddings from different categories are more coherently clustered and better separated under joint training, demonstrating that joint learning enables the model to acquire more structured and discriminative representations across diverse fact types.

wikidata12k* WikiPeople* wikimix

**Figure 4.** t-SNE visualization of shared entity’s embeddings.

**Figure 5.** Results of efficiency analysis.

Efficiency Analysis

For memory usage, HiDR as a data preprocessing module, incurs minimal additional storage overhead. Although some extra nodes and relations are introduced, only embeddings for three “connected relations” need to be stored, while embeddings for other nodes can be derived from existing atomic elements. For runtime efficiency, as shown in Figure 5, UniHR does not significantly increase the number of model parameters or runtime compared to state-of-theart methods. The embeddings of newly introduced nodes are computed from atomic elements, thus avoiding parameter inflation. During message passing, we employ subgraph sampling instead of using the entire graph, and apply dropout to prevent overfitting, which effectively improves training efficiency. Overall, UniHR achieves a better tradeoff between effectiveness and efficiency.

## Conclusion

In this paper, we propose UniHR, a unified hierarchical KG representation learning framework consisting of a learningoptimized Hierarchical Data Representation (HiDR) module and a Hierarchical Structure Learning (HiSL) module. The HiDR module unifies hyper-relational, nested and temporal facts into the triple form. Moreover, HiSL captures local semantic information within facts and global structural information between facts. Extensive experiments show UniHR achieves the best or competitive performance across 5 types of KGs over 9 datasets and further highlight the strong potential of unified representations across 3 complex scenarios.

15427

![Figure extracted from page 7](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-unihr-hierarchical-representation-learning-for-unified-knowledge-graph-link-pred/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

This work is founded by National Natural Science Foundation of China (NSFC62306276/NSFCU23B2055), Yongjiang Talent Introduction Programme (2022A-238-G), and Fundamental Research Funds for the Central Universities (226-2023-00138). This work was supported by Ant Group.

## References

Ali, W.; Saleem, M.; Yao, B.; Hogan, A.; and Ngomo, A. N. 2022. A survey of RDF stores & SPARQL engines for querying knowledge graphs. VLDB J., 31(3): 1–26. Annervaz, K.; Chowdhury, S. B. R.; and Dukkipati, A. 2018. Learning beyond Datasets: Knowledge Graph Augmented Neural Networks for Natural Language Processing. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), 313–322. Bordes, A.; Usunier, N.; Garc´ıa-Dur´an, A.; Weston, J.; and Yakhnenko, O. 2013. Translating Embeddings for Modeling Multi-relational Data. In Burges, C. J. C.; Bottou, L.; Ghahramani, Z.; and Weinberger, K. Q., eds., Advances in Neural Information Processing Systems 26: 27th Annual Conference on Neural Information Processing Systems 2013. Proceedings of a meeting held December 5-8, 2013, Lake Tahoe, Nevada, United States, 2787–2795. Chen, S.; Liu, X.; Gao, J.; Jiao, J.; Zhang, R.; and Ji, Y. 2021. HittER: Hierarchical Transformers for Knowledge Graph Embeddings. In Moens, M.; Huang, X.; Specia, L.; and Yih, S. W., eds., Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021, 10395–10407. Association for Computational Linguistics. Chen, Y.; Li, X.; Liu, Y.; and Hu, T. 2025. Integrating Transformer Architecture and Householder Transformations for Enhanced Temporal Knowledge Graph Embedding in DuaTHP. Symmetry, 17(2): 173. Chung, C.; Lee, J.; and Whang, J. J. 2023. Representation Learning on Hyper-Relational and Numeric Knowledge Graphs with Transformers. In Singh, A. K.; Sun, Y.; Akoglu, L.; Gunopulos, D.; Yan, X.; Kumar, R.; Ozcan, F.; and Ye, J., eds., Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD 2023, Long Beach, CA, USA, August 6-10, 2023, 310–322. ACM. Chung, C.; and Whang, J. J. 2023. Learning Representations of Bi-level Knowledge Graphs for Reasoning beyond Link Prediction. In Williams, B.; Chen, Y.; and Neville, J., eds., Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February 7-14, 2023, 4208–4216. AAAI Press. Dasgupta, S. S.; Ray, S. N.; and Talukdar, P. 2018. Hyte: Hyperplane-based temporally aware knowledge graph em- bedding. In Proceedings of the 2018 conference on empirical methods in natural language processing, 2001–2011. Ding, Z.; Wu, J.; Wu, J.; Xia, Y.; Xiong, B.; and Tresp, V. 2024. Temporal Fact Reasoning over Hyper-Relational Knowledge Graphs. In Al-Onaizan, Y.; Bansal, M.; and Chen, Y., eds., Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, November 12-16, 2024, 355–373. Association for Computational Linguistics. Fang, Z.; Lei, S.; Zhu, X.; Yang, C.; Zhang, S.; Yin, X.; and Qin, J. 2024. Transformer-based Reasoning for Learning Evolutionary Chain of Events on Temporal Knowledge Graph. In Yang, G. H.; Wang, H.; Han, S.; Hauff, C.; Zuccon, G.; and Zhang, Y., eds., Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR 2024, Washington DC, USA, July 14-18, 2024, 70–79. ACM. Galkin, M.; Trivedi, P.; Maheshwari, G.; Usbeck, R.; and Lehmann, J. 2020. Message Passing for Hyper-Relational Knowledge Graphs. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), 7346–7359. Guan, S.; Jin, X.; Guo, J.; Wang, Y.; and Cheng, X. 2023. Link Prediction on N-ary Relational Data Based on Relatedness Evaluation. IEEE Trans. Knowl. Data Eng., 35(1): 672–685. Guan, S.; Jin, X.; Wang, Y.; and Cheng, X. 2019. Link prediction on n-ary relational data. In Proceedings of the 28th International Conference on World Wide Web (WWW’19), 583–593. Guo, J.; and Kok, S. 2021. BiQUE: Biquaternionic Embeddings of Knowledge Graphs. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, 8338–8351. Kaiser, M.; Saha Roy, R.; and Weikum, G. 2021. Reinforcement learning from reformulations in conversational question answering over knowledge graphs. In Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval, 459–469. Kazemi, S. M.; Goel, R.; Eghbali, S.; Ramanan, J.; Sahota, J.; Thakur, S.; Wu, S.; Smyth, C.; Poupart, P.; and Brubaker, M. A. 2019. Time2Vec: Learning a Vector Representation of Time. CoRR, abs/1907.05321. Lehmann, J.; Isele, R.; Jakob, M.; Jentzsch, A.; Kontokostas, D.; Mendes, P. N.; Hellmann, S.; Morsey, M.; van Kleef, P.; Auer, S.; and Bizer, C. 2015. DBpedia - A large-scale, multilingual knowledge base extracted from Wikipedia. Semantic Web, 6(2): 167–195. Li, H.; Liang, K.; Yang, W.; Meng, L.; Wang, Y.; Zhou, S.; and Liu, X. 2025. Eyes on Islanded Nodes: Better Reasoning via Structure Augmentation and Feature Co-Training on Bi- Level Knowledge Graphs. IEEE Trans. Image Process., 34: 3268–3280. Liu, Z.; Gan, C.; Wang, J.; Zhang, Y.; Bo, Z.; Sun, M.; Chen, H.; and Zhang, W. 2025. OntoTune: Ontology-Driven Selftraining for Aligning Large Language Models. In Long, G.; Blumestein, M.; Chang, Y.; Lewin-Eytan, L.; Huang, Z. H.;

15428

<!-- Page 9 -->

and Yom-Tov, E., eds., Proceedings of the ACM on Web Conference 2025, WWW 2025, Sydney, NSW, Australia, 28 April 2025- 2 May 2025, 119–133. ACM. Luo, H.; E, H.; Yang, Y.; Guo, Y.; Sun, M.; Yao, T.; Tang, Z.; Wan, K.; Song, M.; and Lin, W. 2023. HAHE: Hierarchical Attention for Hyper-Relational Knowledge Graphs in Global and Local Level. In Rogers, A.; Boyd-Graber, J. L.; and Okazaki, N., eds., Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9- 14, 2023, 8095–8107. Association for Computational Linguistics. Pan, J.; Nayyeri, M.; Li, Y.; and Staab, S. 2024. HGE: embedding temporal knowledge graphs in a product space of heterogeneous geometric subspaces. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 8913–8920. Pirr`o, G. 2025. Higher Order Knowledge Graph Embeddings. In Hauff, C.; Macdonald, C.; Jannach, D.; Kazai, G.; Nardini, F. M.; Pinelli, F.; Silvestri, F.; and Tonellotto, N., eds., Advances in Information Retrieval - 47th European Conference on Information Retrieval, ECIR 2025, Lucca, Italy, April 6-10, 2025, Proceedings, Part I, volume 15572 of Lecture Notes in Computer Science, 181–195. Springer. Vashishth, S.; Sanyal, S.; Nitin, V.; and Talukdar, P. 2019. Composition-based Multi-Relational Graph Convolutional Networks. In International Conference on Learning Representations. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, Ł.; and Polosukhin, I. 2017. Attention is all you need. Advances in neural information processing systems, 30. Vrandeˇci´c, D.; and Kr¨otzsch, M. 2014. Wikidata: a free collaborative knowledgebase. Communications of the ACM, 57(10): 78–85. Wang, J.; Chen, H.; and Zhang, W. 2025. Structure-Aware Transformer for hyper-relational knowledge graph completion. Expert Syst. Appl., 277: 126992. Wang, Q.; Wang, H.; Lyu, Y.; and Zhu, Y. 2021. Link Prediction on N-ary Relational Facts: A Graph-based Approach. In Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021, 396–407. Xiong, B.; Nayyer, M.; Pan, S.; and Staab, S. 2023a. Shrinking embeddings for hyper-relational knowledge graphs. arXiv preprint arXiv:2306.02199. Xiong, B.; Nayyeri, M.; Daza, D.; and Cochez, M. 2023b. Reasoning beyond triples: Recent advances in knowledge graph embeddings. In Proceedings of the 32nd ACM International Conference on Information and Knowledge Management, 5228–5231. Xiong, B.; Nayyeri, M.; Luo, L.; Wang, Z.; Pan, S.; and Staab, S. 2024. NestE: modeling nested relational structures for knowledge graph reasoning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 9205–9213. Xu, C.; Nayyeri, M.; Alkhoury, F.; Yazdi, H. S.; and Lehmann, J. 2019. Temporal knowledge graph embedding model based on additive time series decomposition. arXiv preprint arXiv:1911.07893. Xu, C.; Nayyeri, M.; Chen, Y.; and Lehmann, J. 2023. Geometric Algebra Based Embeddings for Static and Temporal Knowledge Graph Completion. IEEE Trans. Knowl. Data Eng., 35(5): 4838–4851. Yu, W.; Yang, J.; and Yang, D. 2024. Robust Link Prediction over Noisy Hyper-Relational Knowledge Graphs via Active Learning. In Chua, T.; Ngo, C.; Kumar, R.; Lauw, H. W.; and Lee, R. K., eds., Proceedings of the ACM on Web Conference 2024, WWW 2024, Singapore, May 13-17, 2024, 2282–2293. ACM. Zhang, S.; Liang, X.; Niu, S.; Niu, Z.; Wu, B.; Hua, G.; Wang, L.; Guan, Z.; Wang, H.; Zhang, X.; et al. 2025. Integrating Large Language Models and M¨obius Group Transformations for Temporal Knowledge Graph Embedding on the Riemann Sphere. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 13277–13285. Zhang, S.; Tay, Y.; Yao, L.; and Liu, Q. 2019. Quaternion knowledge graph embeddings. Advances in neural information processing systems, 32.

15429
