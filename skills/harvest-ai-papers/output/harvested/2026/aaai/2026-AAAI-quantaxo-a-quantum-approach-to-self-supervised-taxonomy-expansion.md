---
title: "QuanTaxo: A Quantum Approach to Self-Supervised Taxonomy Expansion"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40526
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40526/44487
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# QuanTaxo: A Quantum Approach to Self-Supervised Taxonomy Expansion

<!-- Page 1 -->

QuanTaxo: A Quantum Approach to Self-Supervised Taxonomy Expansion

Sahil Mishra1, Avi Patni2, Niladri Chatterjee2, Tanmoy Chakraborty1

1Department of Electrical Engineering, Indian Institute of Technology Delhi 2Department of Mathematics, Indian Institute of Technology Delhi sahil.mishra@ee.iitd.ac.in, patni.avi@gmail.com, {niladri, tanchak}@iitd.ac.in

## Abstract

A taxonomy is a hierarchical graph of knowledge that provides valuable insights for various web applications. However, the manual construction of taxonomies requires significant human effort. As web content continues to expand at an unprecedented pace, existing taxonomies risk becoming outdated, struggling to incorporate new and emerging information effectively. As a consequence, there is a growing need for dynamic taxonomy expansion to keep them relevant and up-to-date. Existing taxonomy expansion methods often rely on classical word embeddings to represent entities. However, these embeddings fall short of capturing hierarchical polysemy, where an entity’s meaning can vary based on its position in the hierarchy and its surrounding context. To address this challenge, we introduce QuanTaxo, a quantum-inspired framework for taxonomy expansion that encodes entities in a Hilbert space and models interference effects between them, yielding richer, context-sensitive representations. Comprehensive experiments on five real-world benchmark datasets show that QuanTaxo significantly outperforms classical embedding models, achieving substantial improvements of 12.3% in accuracy, 11.2% in Mean Reciprocal Rank (MRR), and 6.9% in Wu & Palmer (Wu&P) metrics across nine classical embedding-based baselines.

Code: https://github.com/sahilmishra0012/QuanTaxo

## Introduction

Taxonomy is a hierarchically structured knowledge graph designed to portray the hypernymy (“is-a”) relationship between concepts, showing how broad categories subsume more specific ones. Therefore, it serves as core infrastructure for many online applications by efficiently indexing and organizing knowledge. For example, Amazon (Mao et al. 2020) and Alibaba (Karamanolakis, Ma, and Dong 2020) use taxonomies to power e-commerce search and browsing, while Pinterest leverages them for content recommendation and advertisement targeting (Gonc¸alves et al. 2019; Manzoor et al. 2020).

Traditional taxonomies are typically constructed from scratch by domain experts, making the process slow and labor-intensive. Early automation efforts used unsupervised

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** An illustration of taxonomy expansion using QuanTaxo on the Environment seed taxonomy, where the query terms Soil Pollution and Used Oil are to be inserted.

methods such as graph pruning (Velardi, Faralli, and Navigli 2013), hierarchical clustering (Zhang et al. 2018a), and topic modeling (Liu et al. 2012; Wang et al. 2013) to induce taxonomies from raw data, but they often fail to match the structure and coherence of expert-designed taxonomies. As data continuously evolves, there is a growing need to incorporate new concepts into existing taxonomies. To address this, we focus on taxonomy expansion —- the task of integrating new concepts, or query nodes, into an existing seed taxonomy by placing them under suitable anchor nodes. For example, as shown in Fig. 1, Soil Pollution can be accurately placed under Pollution to maintain structural consistency.

Early work on taxonomy expansion used self-supervision, relying on lexical patterns or distributional embeddings to learn parent-child relationships from a small seed taxonomy (Jurgens and Pilehvar 2015; Snow, Jurafsky, and Ng 2004). However, these methods struggled with limited data and underused structural information. More recent approaches improve this by using paths (Liu et al. 2021; Jiang et al. 2022) or local graphs (Wang et al. 2021; Berant et al. 2015) to better model hierarchy. Others leverage hyperbolic geometry (Ganea, Becigneul, and Hofmann 2018; Nickel and Kiela 2017) or box embeddings (Abboud et al. 2020; Jiang et al. 2023) for more expressive hierarchical representations. Most existing methods represent taxonomy entities using classical word embeddings and infer parent–child relations by measuring similarity between their vectors. How-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

32501

![Figure extracted from page 1](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

ever, such embeddings struggle to capture nuanced, compositional meaning. For instance, “fish” and “drown” may appear similar because they co-occur in sentences like “Fish can swim in water where others would drown.” Yet, these embeddings fail to capture the negative connotation - “Fish cannot drown.” These limitations call for more expressive representations that model hierarchical and contextual subtleties. This motivates quantum-inspired embeddings, which use principles such as superposition and entanglement to better encode such complex semantics.

To show the importance of quantum embeddings, we model the parent-child hierarchy in the taxonomy by treating individual entities as having limited standalone significance, while their superposition reveals the degree of relatedness between them. Specifically, as illustrated in Fig. 1, we draw inspiration from Fraunhofer’s double-slit experiment in Quantum Physics (Born and Wolf 2013). In this analogy, the two slits represent the parent-child relationship between taxonomy entities. When only one of the slits is opened, the wave corresponding to the individual word passes through, registering on the detection screen as a neutral entity, as seen in cases like “Soil Pollution” and “Used Oil.” However, when both slits are opened, the superposition of the waves from both words reveals the nature of their relationship, which is positive between “Pollution” and “Soil Pollution”, but negative between “Pollution” and “Used Oil.”

We introduce QuanTaxo, the Quantum Taxonomy Expansion Framework that leverages the superposition principle from quantum physics to represent hierarchical polysemy in a taxonomy. Our key contributions are as follows:

We first construct training data using a self-supervised framework based on the seed taxonomy. Each ⟨parent, child⟩ pair from the taxonomy serves as a positive example, while negative samples are created by pairing the child with nonancestral nodes. As illustrated in Fig. 1, ⟨Environment, Waste⟩and ⟨Pollution, Radioactive Pollution⟩are positive samples, whereas ⟨Pollution, Chemical Waste⟩and ⟨Chemical Waste, Radioactive Pollution⟩are negatives.

Secondly, we propose a quantum modeling framework to represent ⟨parent, child⟩pairs in a complex probabilistic Hilbert space. Inspired by Fraunhofer’s double-slit experiment, we adopt an entanglement-based approach to superimpose parent and child embeddings, yielding quantum entity representations via density matrices. The framework is based on two core hypotheses: (i) a word is a linear combination of latent concepts with complex weights, and (ii) multiple words form a complex superposition of their states. Accordingly, we introduce two variants: (i) Quant-Sup, which models entities as linear combinations of latent concepts, and (ii) Quant-Mix, which models them as weighted mixtures of word states.

Thirdly, we propose a joint representation framework to quantify the relatedness between parent and child entities in the taxonomy. This involves superimposing their quantum representations to form a composite representation that captures their degree of “entanglement” or interconnectedness. From this, we extract specialized “entangled features” reflecting relational coherence. We assess relatedness using mathematical properties such as the trace and diagonal elements of the joint matrix—the trace captures cumulative shared attributes, while the diagonal highlights individual contributions and structural alignment within the hierarchy. Ablation studies comparing complex and real embeddings reveal why the complex space is essential, and comprehensive experiments on five benchmarks against nine strong baselines show that QuanTaxo lifts performance by an average of 12.3% in accuracy, 11.2% in MRR, and 6.9% in Wu&P metrics, confirming its effectiveness for taxonomy expansion.

## Preliminaries

## 2.1 Hilbert Space In quantum probability theory (Nielsen and Chuang 2010; Von

Neumann 2018), quantum systems are modeled within a Hilbert space Hn, a complex vector space where states are represented as vectors (or density operators), and probabilities are computed from their inner products.

We follow the Dirac notation commonly used in quantum theory, where a state vector⃗ψ ∈Cn is denoted as a ket |ψ⟩, and its transpose as a bra ⟨ψ|. The inner and outer products of unit vectors⃗u and⃗v are written as ⟨u|v⟩and |u⟩⟨v|, respectively. A vector |ψ⟩can be expressed as a superposition of basis vectors,

|ψ⟩= n X i=1 ajeiϕj |ej⟩, (1)

where ajeiϕj is the complex-valued probability amplitude for the jth basis vector |ej⟩. Here, aj ≥0 are real amplitudes satisfying the normalization P j a2 j = 1, and ϕj ∈[−π, π] are the phase angles. Each amplitude can also be expressed in Euler form as aj cos ϕj + iaj sin ϕj, and is computed via the inner product: ajeiϕj = ⟨ej|ψ⟩.

Further, the projection measurement is computed as p(ej | ψ) = a2 j =

⟨ej | ψ⟩

2, where p (ej | ψ) represents the probability of the quantum event |e1⟩, given the quantum state |ψ⟩. The vector |ψ⟩in Eq. 1 represents a word as a combination of sememes (Goddard 1994) 1, which are the fundamental, indivisible semantic components of word meanings in a language. For instance, the word “robot” can be composed of sememes like “machine”, “automation”, “technology” and “artificial.” The complex phases {ϕj}n j=0 capture quantum interference between words. For example, given two words, wk and wp with complex am- plitudes a(k)

j eiϕ(k)

j and a(p)

j eiϕ(p)

j respectively for the sememe ej, their combination affects the probability of be- ing in state ej as follows a(k)

j eiϕ(k)

j + a(p)

j eiϕ(p)

j

= a(k)

j

+ a(p)

j

+ 2a(k)

j a(p)

j cos ϕ(k)

j −ϕ(p)

j

, where the term 2a(k)

j a(p)

j cos ϕ(k)

j −ϕ(p)

j represents the interference between wk and wp.

1Sememes are also referred to as latent concepts. Each word is a combination of n latent concepts.

32502

<!-- Page 3 -->

**Figure 2.** An illustration of the QuanTaxo framework.

## 2.2 Sentence

Representation A sentence is formed as a combination of words, with each existing in a superposition of underlying sememes. Therefore, the sentence S is a non-classical combination of these sememes. Mathematically, it is represented by an n×n density matrix ρ, which is positive semi-definite (ρ ≥0) and with a unit trace (Tr(ρ) = 1). The diagonal elements of ρ indicate the contribution of individual concepts, while offdiagonal elements capture their quantum-like correlations between them.

In quantum probabilistic space, a sentence can be represented in two ways: superposition and mixture. In the superposition representation, the sentence exists simultaneously in multiple potential states as a combination of latent concepts, capturing the inherent uncertainty and overlap of interpretations, akin to a quantum particle that exists in multiple states. The density matrix for the sentence S is, ρ = |S⟩⟨S|, (2) where sentence S is represented (using Eq. 1) as |S⟩= Pn i=1 ajeiϕj |ej⟩. While in the mixture representation, a sentence is a combination of different word states, where each interpretation is considered as a distinct possibility, weighted by its corresponding probability. Unlike superposition, where states coexist as latent concepts, the mixture approach assigns a classical probability distribution over possible word states. The density matrix is computed as, ρ = n X i=1 λi |ψi⟩⟨ψi|, (3)

where λi represents the weight of the word ψi with Pn i=1 λi = 1.

## 2.3 Taxonomy Expansion

Definition 1. Taxonomy: A taxonomy T o = (N o, Eo) is a tree-like directed acyclic graph, where each node n ∈N o represents a concept and each edge ⟨np, nc⟩∈Eo denotes a ”parent-child” relationship between nodes np and nc.

Definition 2. Taxonomy Expansion: Given a seed taxonomy T o = (N o, Eo) and a set of emerging concepts C, the task is to update the seed taxonomy to T = (N o∪C, Eo∪R), where R is the set of newly created relationships linking existing entities Eo with emerging entities C. Since surface names of entities alone lack true semantics, entity descriptions D are used to augment representations. Moreover, during inference, query node q ∈C identifies its best-suited parent node np ∈N o by maximizing the matching score (np = arg maxa∈N 0 f(a, q)).

The QuanTaxo Framework

This section presents QuanTaxo, an end-to-end neural network implemented in the Hilbert space (c.f Figure 2).

## 3.1 Complex-valued Entity Representation

We start with computing the complex-valued representation of the entities. Given a candidate term np ∈N o and a query term nq (nq ∈N o during training or nq ∈C while inference), we compute their real-valued vector representations from their surface names and descriptions and then project them into complex space. Real-valued Entity Projection: Taxonomy nodes, defined by surface names and descriptions D, are encoded into realvalued vectors using pretrained models like BERT (Kenton and Toutanova 2019), in preparation for projection into complex space Cn. Each entity ne ∈{np, nq} is formatted as de = [CLS]sur(ne)[SEP]D(ne)[SEP], where sur(ne) and D(ne) denote the entity’s surface name and description, respectively, and [CLS], [SEP] are BERTspecific tokens.

The textual input de is encoded by BERT as ze = BERT(de), where ze contains the final-layer embeddings of all tokens. We extract the sentence embedding S = ze[0] from the [CLS] token for the Quant-Sup and token embeddings {ψ}m i=0 = ze[1:m] for the Quant-Mix. Complex-valued Entity Projection: We project real-valued embeddings into the Hilbert space Hn = Cn using a complex phase projector parameterized by amplitude A, phase Φ, and a learnable weight table Λ. Given a real-valued vector x, the projection is defined as ComplexProjector(x) = A(x) ⊙eiΦ(x), where A(x) = ∥x∥2 computes the amplitude, and Φ(x) = fϕ(x) applies a linear transformation to generate the phase. To maintain a probabilistic interpretation, amplitudes are normalized such that Pn j=0 aj = 1, ∀aj ∈A. The complex word embedding is then |ψi⟩= ComplexProjector(ψi), combining amplitude a and phase ϕ as per Eq. 1. The weights Λ = {αi}n i=0 modulate semantic importance in the Quant-Mix network (Section 3.2). For the Quant-Sup network, the complex embedding is |S⟩= ComplexProjector(S).

## 3.2 Quantum Representation

Quantum embeddings of entities are modeled as density matrices (Section 2.2). The Quant-Sup and Quant-Mix

32503

![Figure extracted from page 3](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Dataset |N 0| |E0| |D|

SemEval-Env 261 261 6 SemEval-Sci 429 452 8 MAG-CS-WIKI 25,170 40,314 6 MAG-PSY-WIKI 10,671 14,080 6 WordNet 20.5 19.5 3

**Table 1.** Statistics of benchmark datasets. |N 0| and |E0| denote the number of nodes and edges in the seed taxonomy, while |D| is the taxonomy depth. For WordNet, values are averaged across 114 sub-taxonomies.

networks compute superposition and mixture-based representations, respectively. In the mixture representation (Eq. 3), a weighted sum of outer products of complex word embeddings is computed. To ensure the unit trace condition Tr(ρ) = 1, weights are normalized into probabilities: λi = αi Pn j=0 αj, where λi is the probability of the i-th word ψi. For comparison, we also consider a uniform weighting with λi = 1/n. In contrast, the superposition-based sentence embedding |S⟩directly produces a normalized density matrix (Eq. 2), inherently satisfying the trace condition.

## 3.3 Joint Representation

The query and parent entities are represented as density matrices ρq and ρp. Instead of using distance-based scoring or concatenation, we model their interaction via a joint representation defined as Mpq = ρqρp.

We decompose the query and parent density matrices as ρq = P i λi |vi⟩⟨vi| and ρp = P j λj |vj⟩⟨vj|, where λi, |vi⟩and λj, |vj⟩are the eigenvalues and eigenvectors of the query and parent respectively. These eigenvectors represent latent concepts (or sememes), weighted by their corresponding eigenvalues. The joint representation is given by ρqρp = P i,j λiλj ⟨vi| vj⟩|vi⟩⟨vj|, where the inner product ⟨vi| vj⟩captures the alignment between basis vectors. Since ⟨vi| vj⟩= Tr(|vi⟩⟨vj|), the trace inner product becomes Tr(ρqρp) = P i,j λiλj⟨vi|vj⟩2, representing a cosine-similarity-based measure between latent spaces. This quantum-inspired similarity, denoted as Mpq, encodes the coherence between query and parent (Balkır 2014).

## 3.4 Entangled Features for Scoring

In quantum natural language processing, entity similarity is often measured using the negative von Neumann (VN) divergence, −∆V N(ρp∥ρq) = Tr(ρp log ρq). However, the matrix logarithm makes it difficult to use in end-to-end learning. To overcome this, we adopt the trace inner product, previously used for word and sentence similarity (Blacoe, Kashefi, and Lapata 2013), and shown to approximate the negative VN divergence effectively (Sordoni, Bengio, and Nie 2014; Zhang et al. 2018b). Formally, it is defined as xtrace = Tr(ρqρp) = P i,j λiλj⟨ri|rj⟩2. This expression captures the semantic overlap driving the similarity between the density matrices of the parent and query entities. To enrich their joint representation, we include the diagonal ele- ments of the similarity matrix Mpq, denoted as⃗xdiag, which reflect varying importance scores. The final feature vector is thus defined as⃗xfeat = [xtrace;⃗xdiag]. Leveraging these entangled features, we learn a scoring function to effectively rank anchor nodes np ∈N o for a query node q. We define the scoring function as f(·): RD2 × RD1 →R where f (i) = γ

Wif (i−1) + bi

∀i ≥1, f (0) =⃗xfeat and f(np, nq) = f (N) = σ f (N−1)

, where γ and σ are the ReLU and sigmoid activations respectively.

## 3.5 Model Training and Inference

Self-supervised Data Generation. We use the seed taxonomy T o = (N o, Eo) to construct training data in a self-supervised manner. For each edge ⟨np, nc⟩ ∈ Eo, where np is the parent and nc the query term, we create a positive sample ⟨np, nc⟩. To generate negatives, we fix nc and randomly sample N non-descendant nodes {nl p′}N l=1 from N o—typically siblings, cousins, or other relatives of nc. This yields a training instance X = {⟨np, nc⟩, ⟨n1 p′, nc⟩,..., ⟨nN p′, nc⟩}. Repeating this for each edge in T o forms the self-supervised dataset X = {X1,..., X|Eo|}.

## Model

Training. We train the scoring function f(·) on the dataset X using the binary cross-entropy loss L(Θ) = −PX|Eo|

X1

PN+1 i=1 h yi log f

⃗ xi feat

+

1 −yi log

1 −f ⃗ xi feat i

, where each sample (⃗xi feat, yi)

corresponds to a candidate pair ⟨ni p, ni c⟩in data point Xk, with yi = 1 for positives and yi = 0 for negatives.

Inference. Given a query node c ∈C, the goal during inference is to predict its parent node np ∈N o from the seed taxonomy. For each candidate np, we compute a matching score f(np, nc) and select the parent that maximizes this score: np:= arg maxnp∈N o f(np, nc). Candidates are ranked by their scores, and the top-ranked node is chosen as the predicted parent. This approach can be extended to return the top-k candidates, if needed.

Computational Complexity Analysis. During the training phase, the model processes |Eo| × (N + 1) training instances per epoch, resulting in a computational cost that scales linearly with the number of edges in the seed taxonomy T o. During inference, for each query node nc ∈N o, the model computes |N o| matching scores, one for every node in N o. Although O(|N o|) computations per query can be expensive, in practice, this is sped up via batched scoring and GPU-accelerated matrix multiplications.

## Experimental Setup

We first outline the experimental setup to evaluate the performance of QuanTaxo, covering benchmark datasets, baseline methods, evaluation metrics and implementation details.

## 4.1 Benchmark Datasets

We evaluate QuanTaxo on five benchmarks (c.f. Table 1) – two SemEval-2016 Task 13 datasets, SemEval- Env (Env) and SemEval-Sci (Sci) (Bordea, Lefever, and

32504

<!-- Page 5 -->

Dataset SemEval16-Env SemEval16-Sci MAG-WIKI-CS WordNet MAG-WIKI-PSY Metric Acc MRR Wu&P Acc MRR Wu&P Acc MRR Wu&P Acc MRR Wu&P Acc MRR Wu&P BERT+MLP 12.61.1 23.91.6 48.30.8 12.21.7 19.71.4 45.11.1 8.32.4 15.71.5 36.21.3 9.21.2 17.41.3 43.50.4 7.81.4 15.51.1 37.10.6

TAXI 18.51.3 N/A 47.70.4 13.81.4 N/A 33.10.7 17.31.6 N/A 42.30.5 11.51.8 N/A 38.70.7 12.91.4 N/A 39.70.6

Arborist 9.93.9 27.23.5 43.41.6 19.15.0 32.73.2 47.81.8 15.63.7 34.42.9 46.31.8 12.53.3 27.72.1 52.01.2 15.12.8 28.11.9 44.91.5

TaxoExpan 10.74.1 28.73.8 48.51.7 24.25.4 40.33.3 55.61.9 16.84.1 34.93.2 47.71.3 17.33.5 31.12.3 57.61.8 15.92.2 30.41.8 51.21.1

TMN 34.63.0 41.74.4 53.63.5 32.62.4 46.11.9 65.31.5 24.43.2 39.72.3 53.11.6 20.31.9 35.91.5 54.71.3 19.72.0 34.81.7 51.90.3

STEAM 34.13.4 44.32.1 65.21.4 34.84.5 50.72.5 72.11.7 25.94.0 41.32.5 53.70.4 21.42.8 38.21.4 59.81.3 23.53.1 36.31.6 53.31.2

BoxTaxo 32.35.8 45.73.2 73.11.2 26.34.5 41.13.1 61.61.4 23.55.4 35.74.1 49.21.7 22.33.1 35.72.7 58.61.2 21.13.4 34.92.9 54.01.3

Musubu 42.33.2 57.11.4 64.40.7 44.52.3 59.71.6 75.21.2 28.52.9 37.12.0 51.90.7 25.34.9 36.12.9 61.20.9 25.74.4 35.02.3 57.11.0

TEMP 45.58.6 59.16.3 77.32.8 43.57.8 57.55.6 76.31.5 31.81.4 45.32.1 57.81.2 24.65.1 37.54.6 61.22.3 25.92.1 38.91.9 59.70.3

Quant-Sup 49.22.1 59.51.2 79.10.3 57.32.8 67.41.2 82.10.4 35.72.2 51.81.6 61.40.6 25.81.1 41.80.6 71.00.3 27.31.4 43.20.7 61.00.4

Quant-Mix 46.62.1 57.91.2 76.10.1 52.41.7 64.11.1 77.60.6 33.21.9 47.71.1 59.20.7 22.11.3 39.60.8 69.80.4 23.51.5 38.41.0 59.40.5

**Table 2.** Performance comparison between QuanTaxo and baseline methods. Results for each method are presented as meanstd-dev in percentage across three runs with three random seeds. The best performance is marked in bold, while the best baseline is underlined. As TAXI (Panchenko et al. 2016) outputs the taxonomy as a whole, it cannot produce MRR values.

Buitelaar 2016), WordNet, which contains 114 depth-3 subtaxonomies with 10–50 nodes each (Bansal et al. 2014), and two large-scale taxonomies, MAG-CS-WIKI (CS) and MAG-PSY-WIKI (PSY), derived from subgraphs of the Microsoft Academic Graph (MAG) (Sinha et al. 2015). Concept definitions are taken from prior work (Yu et al. 2020; Jiang et al. 2023; Wang et al. 2021; Liu et al. 2021; Arous, Dolamic, and Cudr´e-Mauroux 2023). Following (Yu et al. 2020), we randomly sample 20% of leaf nodes as test nodes (with valid parents) and use the remaining nodes as the seed taxonomy for self-supervised training. Since taxonomies such as CS and PSY allow multiple parents, but Wu&P similarity assumes a tree, we derive a spanning tree by duplicating subtrees for multi-parent nodes, ensuring a cycle-free structure with a unique ancestor path for each node.

## 4.2 Baseline Methods

We evaluate QuanTaxo against a range of baselines based on classical embeddings utilizing pretrained language models, graph neural networks, and a few prompting-based methods, all of which encode semantic and structural features. We use the following baselines: • BERT+MLP (Kenton and Toutanova 2019) encodes term surface forms with BERT and feeds the resulting vectors to a multilayer perceptron to classify hypernym relationship. • TAXI (Panchenko et al. 2016) extracts candidate hypernyms via lexical patterns and substring heuristics, then prunes them to produce an acyclic taxonomy without ranking. • Arborist (Manzoor et al. 2020) models heterogeneous edge semantics and trains with a large-margin ranking loss whose margin adapts dynamically. • TaxoExpan (Shen et al. 2020) represents an anchor node by encoding its ego network with a graph neural network and scores parent–child pairs through a log-bilinear feed-forward layer. • TMN (Zhang et al. 2021) fuses auxiliary and primary signals using a neural tensor network and refines embeddings via a channelwise gating mechanism. • STEAM (Yu et al. 2020) ensembles graph, contextual, and lexical-syntactic features in

**Figure 3.** Performance comparison of real and complexvalued embeddings across ‘Env’, ‘Sci’ and ‘PSY’.

a multi-view co-training framework to score hypernymy links. • BoxTaxo (Jiang et al. 2023) learns box embeddings and evaluates parent candidates with geometric and probabilistic losses derived from hyper-rectangle volumes. • Musubu (Takeoka, Akimoto, and Oyamada 2021) finetunes language-model classifiers on Hearst-pattern phrases that contain both query and parent terms. • TEMP (Liu et al. 2021) encodes full root–to–parent paths and trains with a dynamic-margin loss to represent query nodes.

Baselines such as TMN are designed for taxonomy completion. They insert a query q between a parent–child pair and therefore score triplets f(p, c, q). Our setting is taxonomy expansion, where q is attached as a leaf under a parent and no child c is available. For a fair comparison, we follow (Wang et al. 2022) and adapt these baselines by instantiating c with a dummy placeholder (e.g., a blank/sentinel token). This converts their triplet scorer to an effective leafattachment scheme while preserving their original scoring function.

## 4.3 Evaluation Metrics

Given a query set C, let {ˆy1, ˆy2,..., ˆy|C|} be the predicted parent nodes and {y1, y2,..., y|C|} the corresponding ground-truth labels. Following prior work (Jiang et al. 2023; Liu et al. 2021), we evaluate the performance of QuanTaxo and all baselines using three standard metrics, namely, Ac-

32505

![Figure extracted from page 5](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

Acc MRR Wu&P 0.0

0.5

Metric Values

Environment

Acc MRR Wu&P 0.0

0.5

Science

Acc MRR Wu&P 0.00

0.25

0.50

MAG-WIKI-CS

Real, Direct Sum Real, Weighted Sum

Complex, Direct Sum Complex, Weighted Sum

**Figure 4.** Performance comparison of direct and weighted sum in real-valued and complex-valued mixture models across ‘Env’, ‘Sci’, and ‘WIKI’ benchmarks.

curacy (Acc)= Hit@1 = 1 |C|

P|C| i=1 I(yi = ˆyi), where I(·) is the indicator function, Mean Reciprocal Rank (MRR)=

1 |C|

P|C| i=1

1 rank(yi) and Wu & Palmer Similarity (Wu&P)

(Wu and Palmer 1994)= 1 |C|

P|C| i=1

2×DEPTH(LCA(ˆyi,yi)) DEPTH(ˆyi)+DEPTH(yi), where DEPTH(·) denotes the node’s depth in the taxonomy.

## 4.4 Implementation Details We implement QuanTaxo in

PyTorch, with baselines, excluding BERT+MLP, sourced from the respective repositories of their original authors. All training and inference tasks are conducted on an 80GB NVIDIA A100 GPU to ensure high computational efficiency. For the implementation, we utilize bert-base-uncased as the default pre-trained model, with the hidden layer size W2 set to 64 and a dropout rate of 0.1. The maximum padding length for inputs is fixed at 128, and the optimizer used is AdamW, with a learning rate of 2 × 10−5 for BERT fine-tuning and of 1 × 10−3 for training the remaining weights. Training is performed using a batch size of 128 over a maximum of 100 epochs. The sizes of density matrices are kept the same as the dimensions of bert-base-uncased, i.e., 768.

## 5 Experimental

## Results

## 5.1 Main Results Table 2 shows that

QuanTaxo consistently outperforms prior state-of-the-art models based on classical embeddings and structural summaries across all evaluation metrics. Early methods like BERT+MLP rely on surface-level names and classical embeddings, ignoring structural cues. First-generation models (e.g., Musubu, TAXI) add lexical and semantic features but struggle with semantic ambiguity. Second-generation methods (e.g., TaxoExpan, STEAM) include structural signals yet still use classical embeddings, limiting semantic depth. Recent baselines like TEMP use path-based transformers but remain bound to classical embeddings. BoxTaxo explores geometric embeddings but is limited by instability and traditional representations. QuanTaxo surpasses these baselines by leveraging quantum embeddings to capture semantic entanglements without explicit structural inputs. Its strong performance, even on larger datasets, highlights the representational power and robustness of quantum semantics in modeling taxonomic hierarchy and coherence.

**Figure 5.** Comparison of parent-child joint representation and concatenation for scoring on ‘Env’ and ‘Sci’. ‘Sup’ → superposition module, while ‘Mix’ →mixture module. R → real embedding while C →complex embedding.

## 5.2 Ablation Studies

QuanTaxo comprises three key modules: a complex embedding projector, a quantum module, and a joint representation module. We investigate the effect of different configurations on the performance of taxonomy expansion.

Impact of Real and Complex Representations on Quantum Modeling. We assess the effectiveness of complexvalued embeddings in QuanTaxo by comparing them to real-valued embeddings that use only amplitude and omit phase information. As shown in Figure 3, complex embeddings consistently outperform real-valued ones across all metrics. By incorporating both amplitude and phase, they enable richer, context-aware representations via quantum interference, leading to improved accuracy, higher MRR through better parent ranking, and superior Wu & Palmer similarity by preserving hierarchical structure. These results highlight the importance of amplitude-phase interactions in capturing nuanced relational semantics, making complex embeddings integral to the success of QuanTaxo.

Impact of Direct Sum vs. Weighted Sum in Mixture Models. We compare direct and weighted summation in real- and complex-valued mixture models across three benchmarks (Section 3.2, Figure 4). While both methods perform similarly in the real space, weighted summation significantly underperforms in the complex space. This is due to its disruption of the balance between amplitude and phase, which are crucial for capturing semantics in complex embeddings (M¨onning and Manandhar 2018). Misaligned phases can cause destructive interference, distorting the representation and leading to information loss.

Comparison of Parent-Child Joint Representation and Concatenation for Scoring. We compare joint representation against concatenation for parent-child scoring on the SemEval16-Env and SemEval16-Sci benchmarks (Fig. 5). Across all settings, joint representation consistently outperforms concatenation. Notably, complex-valued embeddings with joint representation yield the best results, effectively capturing hierarchical and semantic relationships. While real-valued embeddings also benefit from the joint

32506

![Figure extracted from page 6](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

**Figure 6.** Effect of density matrix dimensionality on model performance across ‘Env’, ‘Sci’ and ‘CS’.

**Figure 7.** Heatmaps of diagonals of joint representation of positive ⟨”environmental impact”,”environmental policy” ⟩and negative ⟨”environmental impact”,”environmental research” ⟩pairs, from SemEval16-Env.

setup, they remain slightly behind their complex counterparts. These findings highlight the superiority of joint representation—especially with complex embeddings—over simple concatenation for modeling relational structure.

Effect of Dimensionality of Density Matrix on Performance. We analyze the impact of density matrix dimensionality on model performance (Fig. 6) by projecting BERT embeddings into varying dimensions and computing their outer products. Performance generally improves with higher dimensionality. However, for complex-valued embeddings, performance stabilizes early—for instance, results at dimension 64 closely match those at 768. In contrast, real-valued embeddings continue to benefit from increased dimensions. These findings underscore the efficiency and robustness of complex-valued embeddings in capturing hierarchical and relational semantics, even at lower dimensions.

## 5.3 Distribution of Density Matrices

We analyze the diagonal features⃗xdiag from the joint representation to assess parent-child relationship scoring. Using the SemEval16-Env dataset and the query term environmental impact (true parent: environmental policy), we compare its density matrix with that of the lowest-scoring negative parent, environmental research. As shown in Figure 7, positive pairs exhibit higher intensity and more uniform diagonal values (ranging 0–100), reflecting strong semantic and hierarchical alignment. In contrast, negative pairs show lower intensity, irregular patterns, and sparse high values, indicating weak or absent coherence. These patterns highlight the

Dataset Query Ground Truth Predicted Parent Score

Env dust atmospheric pollutant environment 0.809 non-polluting vehicle pollution control measures environment 0.825 groundwater water water 0.999 tropical zone climatic zone climatic zone 0.999

Sci radiobiology biology science 0.961 enzymology biochemistry genetics 0.978 microbiology biology biology 0.999 nuclear physics physics physics 1.000

**Table 3.** Examples of QuanTaxo’s predictions with confidence scores across benchmarks.

effectiveness of the joint representation in capturing and distinguishing meaningful parent-child relationships.

## 5.4 Case Study

In this section, we present an error analysis with case studies to evaluate the effectiveness of the QuanTaxo framework on SemEval-2016 datasets (Table 3). For each benchmark, we examine two correct and two incorrect predictions, leading to two key insights on the strengths of quantum embeddings in modeling semantic and hierarchical relationships. QuanTaxo performs well on clear and well-defined concepts such as groundwater, tropical zone and microbiology, accurately retrieving appropriate anchor nodes due to the clarity of their definitions. In contrast, it struggles with ambiguous or underspecified terms like enzymology, and nonpolluting vehicle, where insufficient definitions hinder precise semantic grounding. Notably, incorrect predictions generally yield low matching scores, indicating that quantum embeddings avoid forming spurious entanglements in uncertain cases. These lower scores can serve as a heuristic for identifying potentially unreliable predictions in the absence of ground truth.

## 6 Conclusion

We propose QuanTaxo, a taxonomy expansion framework that uses quantum embeddings to model hierarchical and semantic structure. It consists of three core components: a complex embedding projector, a quantum representation module, and a joint representation module. By projecting entities into a complex-valued Hilbert space, QuanTaxo captures rich relationships through superposition and entanglement, which are well-suited for modeling hierarchy and polysemy. The quantum module encodes nuanced semantic overlaps, while the joint module fuses parent and child density matrices for coherent representation. Experiments on benchmarks show that QuanTaxo outperforms classical embedding methods and structure-aware models. Ablation studies highlight the impact of quantum representations and complex embeddings in enhancing semantic modeling. Error analysis further reveals QuanTaxo’s robustness in handling ambiguous entities. Overall, QuanTaxo demonstrates the promise of quantum-inspired approaches for scalable and accurate taxonomy modeling.

32507

![Figure extracted from page 7](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-quantaxo-a-quantum-approach-to-self-supervised-taxonomy-expansion/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

We gratefully acknowledge support from the Prime Minister’s Research Fellowship (PMRF), which funded this research.

## References

Abboud, R.; Ceylan, ˙I. ˙I.; Lukasiewicz, T.; and Salvatori, T. 2020. BoxE: A Box Embedding Model for Knowledge Base Completion. In NeurIPS, volume 33, 9649–9661. Arous, I.; Dolamic, L.; and Cudr´e-Mauroux, P. 2023. Taxo- Complete: Self-Supervised Taxonomy Completion Leveraging Position-Enhanced Semantic Matching. In Proceedings of the ACM Web Conference 2023, WWW ’23, 2509–2518. New York, NY, USA: Association for Computing Machinery. ISBN 9781450394161. Balkır, E. 2014. Using density matrices in a compositional distributional model of meaning. Master’s thesis, University of Oxford. Bansal, M.; Burkett, D.; de Melo, G.; and Klein, D. 2014. Structured Learning for Taxonomy Induction with Belief Propagation. In Toutanova, K.; and Wu, H., eds., Proceedings of the 52nd ACL, 1041–1051. Baltimore, Maryland: Association for Computational Linguistics. Berant, J.; Alon, N.; Dagan, I.; and Goldberger, J. 2015. Efficient Global Learning of Entailment Graphs. Computational Linguistics, 41(2): 221–263. Blacoe, W.; Kashefi, E.; and Lapata, M. 2013. A quantumtheoretic approach to distributional semantics. In NAACL, 847–857. Bordea, G.; Lefever, E.; and Buitelaar, P. 2016. SemEval- 2016 Task 13: Taxonomy Extraction Evaluation (TExEval- 2). In SemEval, 1081–1091. San Diego, California: Association for Computational Linguistics. Born, M.; and Wolf, E. 2013. Principles of optics: electromagnetic theory of propagation, interference and diffraction of light. Elsevier. Ganea, O.; Becigneul, G.; and Hofmann, T. 2018. Hyperbolic Entailment Cones for Learning Hierarchical Embeddings. In Dy, J.; and Krause, A., eds., ICML, volume 80, 1646–1655. PMLR. Goddard, C. 1994. Semantic and lexical universals: Theory and empirical findings. John Benjamins. Gonc¸alves, R. S.; Horridge, M.; Li, R.; Liu, Y.; Musen, M. A.; Nyulas, C. I.; Obamos, E.; Shrouty, D.; and Temple, D. 2019. Use of OWL and Semantic Web Technologies at Pinterest. In The Semantic Web – 18th ISWC 2019, Auckland, New Zealand, October 26–30, 2019, Proceedings, Part II, 418–435. Berlin, Heidelberg: Springer-Verlag. ISBN 978-3-030-30795-0. Jiang, M.; Song, X.; Zhang, J.; and Han, J. 2022. TaxoEnrich: Self-Supervised Taxonomy Completion via Structure- Semantic Representations. In WWW, 925–934. New York, NY, USA: ACM. ISBN 9781450390965. Jiang, S.; Yao, Q.; Wang, Q.; and Sun, Y. 2023. A Single Vector Is Not Enough: Taxonomy Expansion via Box Embeddings. In WWW, 2467–2476. New York, NY, USA: Association for Computing Machinery. ISBN 9781450394161.

Jurgens, D.; and Pilehvar, M. T. 2015. Reserating the awesometastic: An automatic extension of the WordNet taxonomy for novel terms. In Mihalcea, R.; Chai, J.; and Sarkar, A., eds., NAACL, 1459–1465. Denver, Colorado: Association for Computational Linguistics. Karamanolakis, G.; Ma, J.; and Dong, X. L. 2020. TXtract: Taxonomy-Aware Knowledge Extraction for Thousands of Product Categories. 8489–8502. Kenton, J. D. M.-W. C.; and Toutanova, L. K. 2019. Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of naacL-HLT, volume 1, 2. Minneapolis, Minnesota. Liu, X.; Song, Y.; Liu, S.; and Wang, H. 2012. Automatic taxonomy construction from keywords. In SIGKDD, 1433–1441. New York, NY, USA: Association for Computing Machinery. ISBN 9781450314626. Liu, Z.; Xu, H.; Wen, Y.; Jiang, N.; Wu, H.; and Yuan, X. 2021. TEMP: Taxonomy Expansion with Dynamic Margin Loss through Taxonomy-Paths. In Moens, M.-F.; Huang, X.; Specia, L.; and Yih, S. W.-t., eds., EMNLP, 3854–3863. Online and Punta Cana, Dominican Republic: Association for Computational Linguistics. Manzoor, E.; Li, R.; Shrouty, D.; and Leskovec, J. 2020. Expanding Taxonomies with Implicit Edge Semantics. In WWW, 2044–2054. New York, NY, USA: Association for Computing Machinery. ISBN 9781450370233. Mao, Y.; Zhao, T.; Kan, A.; Zhang, C.; Dong, X. L.; Faloutsos, C.; and Han, J. 2020. Octet: Online Catalog Taxonomy Enrichment with Self-Supervision. In SIGKDD, 2247–2257. New York, NY, USA. ISBN 9781450379984. M¨onning, N.; and Manandhar, S. 2018. Evaluation of complex-valued neural networks on real-valued classification tasks. arXiv preprint arXiv:1811.12351. Nickel, M.; and Kiela, D. 2017. Poincar´e Embeddings for Learning Hierarchical Representations. In Guyon, I.; Luxburg, U. V.; Bengio, S.; Wallach, H.; Fergus, R.; Vishwanathan, S.; and Garnett, R., eds., Advances in Neural Information Processing Systems, volume 30. Curran Associates, Inc. Nielsen, M. A.; and Chuang, I. L. 2010. Quantum computation and quantum information. Cambridge university press. Panchenko, A.; Faralli, S.; Ruppert, E.; Remus, S.; Naets, H.; Fairon, C.; Ponzetto, S. P.; and Biemann, C. 2016. TAXI at SemEval-2016 Task 13: a Taxonomy Induction Method based on Lexico-Syntactic Patterns, Substrings and Focused Crawling. In SemEval, 1320–1327. San Diego, California: Association for Computational Linguistics. Shen, J.; Shen, Z.; Xiong, C.; Wang, C.; Wang, K.; and Han, J. 2020. TaxoExpan: Self-supervised Taxonomy Expansion with Position-Enhanced Graph Neural Network. In WWW, 486–497. New York, NY, USA: Association for Computing Machinery. ISBN 9781450370233. Sinha, A.; Shen, Z.; Song, Y.; Ma, H.; Eide, D.; Hsu, B.-J. P.; and Wang, K. 2015. An Overview of Microsoft Academic Service (MAS) and Applications. In Proceedings of the 24th International Conference on World Wide Web, WWW ’15

32508

<!-- Page 9 -->

Companion, 243–246. New York, NY, USA: Association for Computing Machinery. ISBN 9781450334730. Snow, R.; Jurafsky, D.; and Ng, A. 2004. Learning Syntactic Patterns for Automatic Hypernym Discovery. In Saul, L.; Weiss, Y.; and Bottou, L., eds., Advances in Neural Information Processing Systems, volume 17. MIT Press. Sordoni, A.; Bengio, Y.; and Nie, J.-Y. 2014. Learning concept embeddings for query expansion by quantum entropy minimization. In AAAI, volume 28. Takeoka, K.; Akimoto, K.; and Oyamada, M. 2021. Lowresource Taxonomy Enrichment with Pretrained Language Models. In Moens, M.-F.; Huang, X.; Specia, L.; and Yih, S. W.-t., eds., EMNLP, 2747–2758. Online and Punta Cana, Dominican Republic: Association for Computational Linguistics. Velardi, P.; Faralli, S.; and Navigli, R. 2013. OntoLearn Reloaded: A Graph-Based Algorithm for Taxonomy Induction. Computational Linguistics, 39(3): 665–707. Von Neumann, J. 2018. Mathematical foundations of quantum mechanics: New edition, volume 53. Princeton university press. Wang, C.; Danilevsky, M.; Desai, N.; Zhang, Y.; Nguyen, P.; Taula, T.; and Han, J. 2013. A phrase mining framework for recursive construction of a topical hierarchy. In SIGKDD, 437–445. New York, NY, USA: Association for Computing Machinery. ISBN 9781450321747. Wang, S.; Zhao, R.; Chen, X.; Zheng, Y.; and Liu, B. 2021. Enquire One’s Parent and Child Before Decision: Fully Exploit Hierarchical Structure for Self-Supervised Taxonomy Expansion. In WWW, 3291–3304. New York, NY, USA: Association for Computing Machinery. ISBN 9781450383127. Wang, S.; Zhao, R.; Zheng, Y.; and Liu, B. 2022. Qen: Applicable taxonomy completion via evaluating full taxonomic relations. In WWW, 1008–1017. Wu, Z.; and Palmer, M. 1994. Verb Semantics and Lexical Selection. In ACL, 133–138. Las Cruces, New Mexico, USA. Yu, Y.; Li, Y.; Shen, J.; Feng, H.; Sun, J.; and Zhang, C. 2020. STEAM: Self-Supervised Taxonomy Expansion with Mini-Paths. In SIGKDD, 1026–1035. New York, NY, USA: Association for Computing Machinery. ISBN 9781450379984. Zhang, C.; Tao, F.; Chen, X.; Shen, J.; Jiang, M.; Sadler, B.; Vanni, M.; and Han, J. 2018a. TaxoGen: Unsupervised Topic Taxonomy Construction by Adaptive Term Embedding and Clustering. In KDD, 2701–2709. New York, NY, USA: Association for Computing Machinery. ISBN 9781450355520. Zhang, J.; Song, X.; Zeng, Y.; Chen, J.; Shen, J.; Mao, Y.; and Li, L. 2021. Taxonomy completion via triplet matching network. In AAAI, volume 35, 4662–4670. Zhang, P.; Niu, J.; Su, Z.; Wang, B.; Ma, L.; and Song, D. 2018b. End-to-end quantum-like language models with application to question answering. In AAAI, volume 32.

32509
