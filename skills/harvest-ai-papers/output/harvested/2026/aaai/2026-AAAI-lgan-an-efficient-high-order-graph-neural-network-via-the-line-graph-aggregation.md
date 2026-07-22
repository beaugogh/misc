---
title: "LGAN: An Efficient High-Order Graph Neural Network via the Line Graph Aggregation"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39232
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39232/43193
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# LGAN: An Efficient High-Order Graph Neural Network via the Line Graph Aggregation

<!-- Page 1 -->

LGAN: An Efficient High-Order Graph Neural Network via the Line Graph Aggregation

Lin Du1, Lu Bai1*, Jincheng Li1, Lixin Cui2, Hangyuan Du3, Lichi Zhang4, Yuting Chen5, Zhao Li6

1School of Artificial Intelligence, Beijing Normal University, Beijing, China 2School of Information, Central University of Finance and Economics, Beijing, China 3School of Computer and Information Technology, Shanxi University, Taiyuan, China 4School of Biomedical Engineering, Shanghai Jiaotong University, Shanghai, China 5Centre for Learning Sciences and Technologies, The Chinese University of Hong Kong, Hong Kong, China 6Zhejiang Lab, Zhejiang, China dulin@mail.bnu.edu.cn, bailu@bnu.edu.cn

## Abstract

Graph Neural Networks (GNNs) have emerged as a dominant paradigm for graph classification. Specifically, most existing GNNs mainly rely on the message passing strategy between neighbor nodes, where the expressivity is limited by the 1-dimensional Weisfeiler-Lehman (1-WL) test. Although a number of k-WL-based GNNs have been proposed to overcome this limitation, their computational cost increases rapidly with k, significantly restricting the practical applicability. Moreover, since the k-WL models mainly operate on node tuples, these k-WL-based GNNs cannot retain finegrained node- or edge-level semantics required by attribution methods (e.g., Integrated Gradients), leading to the less interpretable problem. To overcome the above shortcomings, in this paper, we propose a novel Line Graph Aggregation Network (LGAN), that constructs a line graph from the induced subgraph centered at each node to perform the higherorder aggregation. We theoretically prove that the LGAN not only possesses the greater expressive power than the 2- WL under injective aggregation assumptions, but also has lower time complexity. Empirical evaluations on benchmarks demonstrate that the LGAN outperforms state-of-the-art k- WL-based GNNs, while offering better interpretability.

## Introduction

Recently, Graph Neural Networks (GNNs) have proven to be powerful tools for graph-structured data analysis across various domains (Bai et al. 2023; Cui et al. 2024; Qin et al. 2025). Most GNNs follow the message-passing framework, where each node updates its representation by aggregating information from its neighbors, thereby incorporating both node features and graph topology.

A fundamental limitation of such Message Passing Neural Networks (MPNNs) lies in their inability to distinguish certain non-isomorphic graphs, which has been proven to be at most as powerful as the 1-dimensional Weisfeiler- Lehman (1-WL) test (Xu et al. 2019). This limitation is usually caused by ignoring interactions among neighbors,

*Corresponding author: Lu Bai Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

HASH (), {{, }}

subgraph line-graph- based line graph

2

,

3, 2 3,

2 3

2

3

2

3

HASH () {{ (,), (,) }} 2 3 HASH () {{ (,), (,) }} 2 3 line-graph- based

2

3

1-WL 2

3

1-WL

2

3

1-WL 2

3

1-WL HASH (), {{, }}

subgraph line graph

HASH () {{ (,), (,) }}, {{ (,) }} HASH () {{ (,), (,) }}, {{ (,) }}

2 3

2 3 2 3

G

H

2

3

2

3

2

,

3,

**Figure 1.** Motivating example: why 1-WL fails and linegraph-based aggregation succeeds.

so that the MPNNs cannot distinguish the subtle structural differences like triangles. For instance, Figure 1 exhibits a pair of graphs G and H, that are non-isomorphic but indistinguishable under the 1-WL test. The red target node 1 in both graphs aggregates messages from an identical multiset of neighbors (i.e., nodes 2 and 3), leading to identical hash updates despite distinct substructures.

To overcome the expressivity limitations of MPNNs, researchers have developed a number of alternative GNNs based on the higher-order k-WL test (Cai, F¨urer, and Immerman 1992; Shervashidze et al. 2011) or stronger variants such as the k-FWL (Folklore Weisfeiler-Lehman) test. Since the k-WL test provides a more powerful framework for capturing the structural similarity of graphs, these k-WL-based GNNs simulating the higher-order isomorphism tests can achieve better performance on challenging graph learning tasks (Morris et al. 2021; Maron et al. 2020; Morris, Rattan, and Mutzel 2020; Bodnar et al. 2022). However, they rely on operations over node tuples or sets. While increasing k enables capturing higher-order node interactions (Sato 2020; Huang and Villar 2021), this design also results in greater computational overhead and reduced interpretability.

On the other hand, the line graphs from the classical graph

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

20914

<!-- Page 2 -->

theory have recently offered another promising direction for improving the expressive power of GNNs. For a line graph, each node corresponds to an edge of the original graph structure, and each edge is formed if its connected nodes corresponding to the original edges sharing the same original node. This construction inherently captures the higher-order structural information that is not directly accessible in the original graph. As shown in Figure 1, the line graph of the induced subgraph centered at node 1 encodes not only the node-neighbor relations (1, 2) and (1, 3), but also the neighbor-neighbor interactions (2, 3), enabling more expressive and structure-aware aggregation. Thus, this enriched representation can naturally distinguish graphs G and H with just one iteration. Motivated by this observation, the line-graph-based neural networks have attracted growing attention, particularly in edge-centric tasks such as link prediction (Zhang et al. 2023; Liang et al. 2025) and community detection (Chen, Li, and Bruna 2020). However, their theoretical connection to the k-WL test is still not clear, influencing the employments for other graph-level tasks.

To address the above shortcomings, we propose a novel GNN framework, namely the Line Graph Aggregation Network (LGAN), for graph classification. Our key idea is to perform the information aggregation associated with the line graphs, that are constructed from the induced subgraph centered at each node. The proposed method can employ either the structural relationship between an original graph and its line graph or the favorable properties of the line graph. Overall, the main contributions are threefold.

1. We introduce the LGAN, a novel line-graph-based GNN for graph-level tasks. Unlike the previous linegraph-based methods focusing on edge-level tasks, the LGAN constructs line graphs over the node-centered subgraphs and further aggregates their messages to represent the whole graph. Moreover, the LGAN employs a dual aggregation design over the line graph to reinforce its isomorphic correspondence with the original graph. 2. We prove the expressive power of the LGAN and its relationship to the k-WL test. We prove that the LGAN surpasses the 2-WL test, under the assumption that aggregation-related functions are injective. Moreover, we show that the LGAN simulates the behavior of 2-FWL in a localized manner, while reducing the time complexity from cubic to nearly linear on sparse graphs. 3. We empirically validate the performance of the LGAN on graph classification tasks. The LGAN consistently outperforms or matches state-of-the-art baselines including the k-WL-based models. Moreover, the LGAN enables the visualization of important substructures in both synthetic and real-world graphs through edge-level attributions.

Preliminary Concepts 2.1 The Basic Notations

Let G(V, E, XV) be an undirected graph with node set V, edge set E, and node feature matrix XV = {xv ∈Rd | v ∈V }. The number of nodes and edges in G are denoted by n = |V | and m = |E|, respectively. The degree of a node v ∈V is denoted by dv. The neighborhood of a node v is defined as N(v) = {u ∈V | (v, u) ∈E}. A pair of isomorphic graphs G and H are denoted as G ∼= H. There exists a bijection φ: V (G) →V (H) such that (u, v) ∈ E(G) if and only if (φ(u), φ(v)) ∈E(H). {{·}} denotes a multiset, a set that allows repeated elements.

## 2.2 The Weisfeiler-Lehman Test We commence by introducing the 1-WL test (Weisfeiler and

Leman 1968), which is a well-known algorithm for graph isomorphism test. Given a labeled graph (G, ℓ), the algorithm proceeds by iteratively updating the node representations based on the local neighborhood information. Initially, each node is assigned a color by hashing its input features. At iteration l > 0, each node v ∈V updates its color by aggregating various colors of its multiset neighbors from the previous iteration and applying a hash function to this multiset with its previous color. The update rule is given by c(l)

v = HASH c(l−1)

v, {{c(l−1)

u | u ∈N(v)}}

. (1)

where c(l)

v denotes the color (i.e., the label) of node v at iteration l, and HASH(·) is an injective function to preserve distinctions between different inputs. This process is repeated until the color assignments converge, i.e., no further changes occur across iterations. It can be observed that the 1-WL algorithm cannot distinguish all non-isomorphic graphs, as illustrated in Figure 1.

We next introduce the k-WL test, a natural generalization of the 1-WL algorithm. Unlike the 1-WL that colors individual nodes, the k-WL test operates on the k-tuples of nodes and refines their labels by incorporating the structure of the induced k-dimensional neighborhoods. Given a labeled graph (G, ℓ), the algorithm first assigns initial colors to all k-tuples of nodes based on their isomorphism types and labels. At each iteration l > 0, the color of a k-tuple v = (v1,..., vk) ∈V k is updated by aggregating the colors of its neighboring tuples. Specifically, for each position i ∈{1,..., k}, we compute the multiset of colors of all tuples obtained by replacing the i-th element of v with every possible node w ∈V, and then update the color of v. This process is defined as c(l)

v,i ←{{c(l−1)

v(i→w) | w ∈V }}, (2a)

c(l)

v = HASH c(l−1)

v, c(l)

v,1, c(l)

v,2,..., c(l)

v,k

. (2b)

where v(i→w) denotes the k-tuple resulting from replacing the i-th entry of v with node w, c(l−1)

v(i→w) is the color assigned to the modified tuple at the previous iteration (l−1), c(l)

v,i denotes the multiset of colors obtained by varying the i-th element of v, and c(l)

v is the updated color of tuple v at iteration l. The process repeats until the coloring stabilizes.

We then describe the k-FWL test, a variant of the k-WL test that is often referred to the Folklore version. Given a labeled graph (G, ℓ), each k-tuple v = (v1,..., vk) ∈V k is initially colored according to its isomorphism type and node

20915

<!-- Page 3 -->

labels. At each iteration l > 0, the color of a k-tuple v is updated by first constructing a k-dimensional color vector for each node w ∈V, and then mapping these vectors together with the previous color into a new color. Specifically, c(l)

v,w ← c(l−1)

v(1→w),..., c(l−1)

v(k→w)

, (3a)

c(l)

v = HASH c(l−1)

v, {{c(l)

v,w | w ∈V }}

. (3b)

Here, c(l)

v,w denotes the k-dimensional color vector obtained by collecting the colors c(l−1)

v(i→w) of modified tuples v(i→w), and c(l)

v is the updated color of tuple v at iteration l, computed by hashing its previous color with the multiset of these vectors. The iteration continues until convergence.

Note that, for all k ≥2, the expressive power of the k- FWL test matches that of the (k + 1)-WL test (Grohe and Otto 2015; Grohe 2017, 2022).

## 2.3 The Line Graph

Given an undirected graph G(V, E), its line graph L(G) is a dual graph whose node set corresponds to the edge set of G, i.e., V (L(G)) = E(G). For L(G), a pair of nodes e1 = (u1, v1) and e2 = (u2, v2) are connected by an edge, if and only if the corresponding edges in G share at least one common endpoint. The line graph has some important properties that illustrate its relationship to the original graph. In particular, if the original graph G is connected, then its line graph L(G) is also connected. And if two graphs G and H are isomorphic, i.e., G ∼= H, then their line graphs are also isomorphic, i.e., L(G) ∼= L(H). Moreover, an important classical result from the graph theory (Whitney 1992) states the following isomorphism property of the line graph. Theorem 1 (Whitney’s Isomorphism Theorem). Let G1 and G2 be two connected graphs that are neither a triangle (K3) nor a claw graph (K1,3). If their line graphs are isomorphic, i.e., L(G1) ∼= L(G2), then the original graphs are also isomorphic, i.e., G1 ∼= G2.

The above theorem serves as an important theoretical foundation for the design of our work. Specifically, this theorem implies that, except for the special case K3 and K1,3, the structure of a graph can be uniquely reconstructed from its line graph. Our model will handle these exceptions via a tailored aggregation design, thus ensuring the theorem’s necessity and sufficiency within our framework.

Related Works 3.1 The k-WL-based GNNs In recent years, several higher-order methods have been proposed to overcome the expressivity limitations of MPNNs. Among them, the k-WL-based GNNs are most relevant to our work. Notably, Morris et al. (2021) introduced the kdimensional GNNs (k-GNNs), that improve the scalability by simulating the set-based k-WL, but lose fine-grained structural information. Maron et al. (2020) proposed Provably Powerful Graph Networks (PPGN), which bypass the combinatorial k-WL simulation by directly applying global matrix multiplications to encode pairwise interactions, but lack localized message passing to explicitly model substructures such as triangles. Morris, Rattan, and Mutzel (2020) proposed a localized variant of the k-WL (δ-k-LGNN) to reduce the computational overhead, yet it remains mainly effective on sparse graphs. Bodnar et al. (2022) introduced CW Networks, which transform the original graph into a cell complex—a topological abstraction that is less intuitive than structures like line graphs. Overall, these models show that k-order invariant or equivariant GNNs can achieve expressivity equivalent to the k-WL isomorphism test.

Although these k-WL-based models capture higherorder structural information, their computational cost grows rapidly with increasing k. Even for moderate values such as k=3, the memory and runtime costs become intractable on real-world graphs. Moreover, models defined on node tuples or sets tend to dilute node-level semantics, limiting interpretability in practice. To address these issues, we will propose a novel LGAN model, which performs line-graphbased local aggregation to emulate the k-WL while preserving effective node-level representations.

## 3.2 The Line-Graph-Based Neural Networks

Line-graph-based neural networks have gained increasing attention for leveraging line graphs to model edge relations (Cai et al. 2021; Zhang et al. 2023; Liang et al. 2025). These methods typically reformulate the edge prediction on the original graph as a node prediction task on its line graph. Beyond encoding the edge-centric relationships, the line graphs possess several well-established theoretical properties that make them particularly suitable for simulating higher-order isomorphism tests such as the k- WL. For example, the line graphs are tightly connected to the fundamental graph properties like connectivity and isomorphism (Whitney 1992), and they support the lineartime complexity algorithms for reconstructing the original graph (Roussopoulos 1973; Lehot 1974). In addition, several studies in hypergraph modeling have shown that the linegraph-based representations are advantageous for capturing complex relational structures (Bai, Ren, and Hancock 2014; Bai, Escolano, and Hancock 2016).

However, existing line-graph-based networks mainly focus on edge-level tasks, without fully leveraging the structural properties. In contrast, our LGAN targets graph-level classification with a tailored aggregation mechanism to capture the structural information. Furthermore, we will bridge the gap between line graphs and the k-WL tests by formally analyzing the expressivity of the proposed framework.

## 4 The Proposed LGAN Model

In this section, we give the detailed definition of the proposed LGAN model. As illustrated by Figure 2, for each target node, the proposed LGAN performs the localized message passing, by first extracting the 1-hop subgraph around each target node and constructing a line graph over this subgraph. Then the features through both target-neighbor and neighbor-neighbor interactions are aggregated to update the representation of the node. Finally, a multi-layer stacking scheme and global readout function are also employed for graph-level tasks. Below, we define these core components.

20916

<!-- Page 4 -->

target node triangle (K3) line graph

, target node claw (K1,3) line graph

,

, AGGRt

UPDATE

AGGRn

,

, neighbor-neighbor

,

UPDATE,

,

AGGRt

AGGRn neighbor-neighbor target-neighbor target-neighbor

**Figure 2.** Overview of the Line Graph Aggregation Network (LGAN). For each target node, the LGAN constructs the induced subgraph, transforms it into a line graph, and performs two relation-specific aggregations: AGGRt (red) for target–neighbor node pairs (i.e., edges sharing the same target node) and AGGRn (blue) for neighbor–neighbor node pairs, followed by an UPDATE fusion. The examples on K3 and K1,3 illustrate how LGAN resolves the exceptional cases in Whitney’s Theorem 1.

## 4.1 The Line Graph Construction

Given an input graph G(V, E), the LGAN updates the hidden representation of each target node t ∈V at layer l, denoted by h(l)

t ∈Rd. It first constructs an induced subgraph Gt = (Vt, Et) centered at t, where Vt = {t} ∪N(t) and Et = {(u, v) ∈E | u, v ∈Vt}. Then, the LGAN builds the line graph L(Gt) = (Et, Et), where each node represents an edge in Gt, and two nodes e1, e2 ∈Et are connected in Et if they share a common endpoint in Gt.

## 4.2 The Relation-Specific Aggregation

Let h(l−1)

{u,v} denote the representation of a node in the line graph L(Gt) at layer l−1, corresponding to the node pair {u, v} ∈E(Gt) in the original graph. It is computed as h(l−1)

{u,v} = COMBpair h(l−1)

u, h(l−1)

v

, (4)

where COMBpair denotes a symmetric combination function (e.g., element-wise summation) for mapping unordered node pairs to line graph node representation.

Then, the LGAN defines two relation-specific aggregations over the line graph L(Gt) as follows.

• Target–Neighbor Aggregation: Aggregates features of node pairs {t, p} incident to the target node t. • Neighbor–Neighbor Aggregation: Aggregates features of node pairs {p, q} among the neighbors of t. These aggregations correspond to the red and blue rectangles in Figure 2, labeled as AGGRt and AGGRn, respectively. To summarize the LGAN, we formally express the updated representation of the target node t at layer l as h(l)

t = ϕ

AGGRt

{{h(l−1)

{t,p} }}

, AGGRn

{{h(l−1)

{p,q}}}

, (5)

where ϕ is a learnable update function fusing the two relation-specific aggregated features. Its inputs are the outputs of AGGRt and AGGRn, which are aggregation functions (e.g., sum) operating over multisets of features incident to the target-neighbor pairs and neighbor-neighbor pairs, respectively. Specifically, we adopt concatenation to retain maximal information from both branches. Other fusion strategies (e.g., the element-wise sum, mean, or attentionbased gating) can also be applied within the framework.

To further enhance the information preservation and gradient flow, we also introduce a residual variant, termed as LGAN-res, which incorporates the previous node representation via a residual connection (He et al. 2015). Specifically, we add a linearly transformed residual from the previous layer to the fused aggregation result. For the LGAN-res, the updated representation of the target node t is given by z(l)

t = ψ

AGGRt

{{h(l−1)

{t,p} }}

, AGGRn

{{h(l−1)

{p,q}}}

,

(6)

h(l)

t = ϕ′

W (l) · h(l−1)

t + z(l)

t

, (7)

where ϕ′ is an additional multi-layer perceptron (MLP) applied after the residual summation. The residual path includes a linear projection to match dimensions if necessary. ψ, AGGRt, and AGGRn retain the same roles as in Eq. (5), maintaining permutation invariance and injectivity.

For the cases where the input graph G contains isolated nodes or nodes with no incident edges (i.e., E(Gt) = ∅), the corresponding line graph L(Gt) becomes empty, resulting in no available edge features for aggregation. In such scenarios, the fused message zt can be set to the zero vector. Consequently, the proposed LGAN-res naturally reduces to a variant of GIN (Xu et al. 2019), where the target node is

20917

<!-- Page 5 -->

updated solely based on a learnable projection of its previous representation, i.e., h(l)

t = ϕ′(W (l) · h(l−1)

t). This fallback behavior preserves stability and ensures that isolated nodes still receive meaningful updates.

## 4.3 The Multi-layer LGAN and Readout

While the above derivation focuses on a single LGAN layer, we stack L such layers to build a deep architecture as

H(0) = X, H(l) = LGANLayer

H(l−1)

, l = 1,..., L, where H(l) denotes the node representation matrix at layer l. Then we adopt a skip-cat (Xu et al. 2018) strategy, where the representations from all layers are concatenated before the final readout. The process is given by

Hskip = h

H(1) ∥· · · ∥H(L)i

, hG = READOUT(Hskip), where ∥denotes concatenation along the feature dimension, Hskip is the concatenated node representation matrix from all L layers, and hG is the final graph-level representation obtained by applying a READOUT function over all nodes.

Note that, the aggregation, update and readout functions of the LGAN follow the DeepSets framework (Zaheer et al. 2018), using the sum-based aggregation and MLPs to achieve the permutation invariance and injectivity. This ensures the maximal expressive power (Xu et al. 2019), while maintaining simplicity and efficiency.

Theoretical Properties of the LGAN

We analyze the expressive power and computational complexity of the proposed LGAN with general cases, where the line graph aggregation is feasible. We prove that it surpasses the 2-WL test under standard injectivity assumptions, while implicitly simulating the 2-FWL behavior through the localized aggregation. We also demonstrate that the LGAN achieves the linear time complexity on sparse graphs.

## 5.1 The Expressive Power of the LGAN

To formalize the expressive advantage of the LGAN, we compare it with the set-based 2-WL test, a widely used and canonical variant operating on unordered node pairs with multiset aggregations. The following theorem shows that the LGAN is at least as powerful as the set-based 2-WL and can even distinguish some graphs that 2-WL cannot.

Theorem 2 (The LGAN is more expressive than the set-based 2-WL). Let A: G →Rd be an L-layer LGAN, the following components are injective at every layer, i.e., 1) the node-pair encoder COMBpair mapping unordered node pairs to the representation of the corresponding line graph node, 2) the multiset aggregators AGGRt and AGGRn (e.g., sum-based DeepSets), 3) the fusion and update functions ψ, ϕ and ϕ′, and 4) the graph-level readout function applied to the multiset of node representations. For any graphs G and H such that the induced subgraph Gt (resp. Ht) for every node t contains at least one edge (i.e., the corresponding line graphs are non-empty), the following holds.

• If the set-based 2-WL test distinguishes G and H, then the LGAN also maps them to different graph representations, i.e., A(G)̸ = A(H). • There exist graphs G and H such that the set-based 2- WL test fails to distinguish them, but the LGAN produces different representations, i.e., A(G)̸ = A(H).

Proof. We first prove by induction that any distinction made by the set-based 2-WL is reflected in the node representations of the LGAN, so that the final injective readout function further leads to different graph-level representations. We then demonstrate that the LGAN succeeds in distinguishing certain graphs where the 2-WL test fails through a counterexample. To commence, let c(l)

{a,b} denote the color assigned by the 2-WL algorithm to the unordered node pair {a, b} at layer l, and let h(l)

t denote the hidden representation of a target node t produced by the LGAN at the same layer. We assume the inductive hypothesis that for some layer l ≥0, if there exists a node pair {a, b} such that c(l)

{a,b}(G)̸ = c(l)

{a,b}(H), then there exists a node t ∈{a, b}

for which h(l+1)

t (G)̸ = h(l+1)

t (H). We first consider the base case l = 0. Suppose the initial 2-WL color c(0)

{a,b} encodes both the initial features of nodes a and b (i.e., xa and xb), and their connectivity. If c(0)

{a,b}(G)̸ = c(0)

{a,b}(H), two scenarios are detailed below. Scenario 1 represents the structural difference, such as when a and b are connected in G but not in H. Thus, the node-pair representation h(0)

{a,b} of G exists and is included in the multiset as given by h(0)

{a,b} ∈ nn h(0)

{a,w} | w ∈NG(a)

oo

= Ma(G), (8)

where Ma(G) is the multiset input to AGGRt for the target node a (cf. Eq. 5). Since h(0)

{a,b} /∈Ma(H) and AGGRt is injective, it follows that

AGGRt (Ma(G))̸ = AGGRt (Ma(H)). (9)

This difference propagates to the node representations updated by the LGAN at the next layer (layer 1), given by ϕ(AGGRt(Ma(G)), ·)̸ = ϕ(AGGRt(Ma(H)), ·), (10)

where ϕ denotes the update function using concatenationbased MLP, which is injective with respect to its first argument. Hence, h(1)

a (G)̸ = h(1)

a (H). Scenario 2 represents the feature difference, such as when (a, b) ∈E(G) ∩E(H), but xa(G)̸ = xa(H) or xb(G)̸ = xb(H). In this scenario, the initial node-pair representations are constructed via the injective function COMBpair (cf. Eq. 4) ensuring that

COMBpair(xa(G), xb(G))̸ = COMBpair(xa(H), xb(H)).

(11) i.e., h(0)

{a,b}(G)̸ = h(0)

{a,b}(H). This difference is captured by AGGRt for target nodes a or b, leading to h(1)

a (G)̸ = h(1)

a (H) or h(1)

b (G)̸ = h(1)

b (H). Thus the base case holds.

20918

<!-- Page 6 -->

Now suppose the inductive hypothesis holds for layer l−1 and consider the update at layer l. Suppose c(l)

{a,b}(G)̸ = c(l)

{a,b}(H), by the 2-WL update rule (cf. Eq. 2), this difference must arise from a mismatch in the below multisets

{{c(l−1)

{w,b} | w ∈V }} or {{c(l−1)

{a,w} | w ∈V }}.

Without loss of generality, assume the former differs between G and H. The difference in the multiset {{c(l−1)

{w,b} | w ∈V }} implies the existence of at least one node w∗such that c(l−1)

{w∗,b}(G)̸ = c(l−1)

{w∗,b}(H). By the inductive hypothesis, this implies h(l)

s (G)̸ = h(l)

s (H) for some s ∈{w∗, b}. By injectivity of COMBpair and AGGRt, this difference further propagates to a target node t where t ∈N(s), leading to h(l+1)

t (G)̸ = h(l+1)

t (H). Thus the induction holds. Having established the general result, we now use an example to show that the LGAN can distinguish graphs that the set-based 2-WL cannot. For graphs G and H in Figure 1 with identical initial node labels, any connected node pair (e.g., {1, 3}) has the same local statistics under the set-based 2-WL, that is, node 1 connects to node 3 and one other node, and is unconnected to the remaining nodes, while node 3 is symmetric. The multisets {{{w, 3}}} and {{{1, w}}} therefore contain the same number of connected and unconnected pairs in both graphs. As a result, the identical node labels and matching multiset statistics lead to the same node-pair representations. The same process applies to unconnected node pairs. Thus, the set-based 2-WL cannot distinguish G and H, but the LGAN can (Figure 1), proving more expressive.

## 5.2 The Theoretical Connection to 2-FWL

The standard k-FWL algorithm colors ordered k-tuples and replaces one coordinate of the tuple by all possible nodes (cf. Eq. (3)), which incurs prohibitive computational costs. To mitigate this, we follow the common practice of converting ordered tuples into unordered sets, obtaining the set-based k-FWL update as c(l)

v,w ←{{ c(l−1)

v(1→w),..., c(l−1)

v(k→w)}} (12a)

c(l)

v = HASH c(l−1)

v, c(l)

v,w w ∈V

(12b)

Fix the k = 2 case and choose an unordered node pair v = {p, q}. In Eq. (12a), the 2-FWL traverses every w ∈V to form the multiset c(l)

v,w = {{c(l−1)

{w,q}, c(l−1)

{p,w}}}. Observe that

• The collection {{c(l−1) {w,q}, c(l−1)

{p,w}}} exactly mirrors the set of node pairs incident to w and {p, q} in the LGAN.

• AGGRn

{{h(l−1)

{p,q}}}

plays the same role as the c(l−1)

{p,q} inside the 2-FWL hash. • When we regard the auxiliary node w as the target t in the LGAN, the multiset {{h(l−1)

{w,q}, h(l−1)

{p,w}}} becomes precisely the input to AGGRt.

Hence, each set-based 2-FWL update on the pair {p, q} can be locally simulated by a single LGAN update on the

1-hop induced subgraph around the target node t = w. Intuitively, the LGAN can be viewed as a sparse and local variant of the set-based 2-FWL, replacing global tuple updates with line graph aggregation over ego networks.

## 5.3 The Time Complexity Analysis

The LGAN attains the expressive benefits of 2-FWL without its cubic cost. Let dv be the degree of node v. A single LGAN layer aggregates dv target-neighbor edges and at most dv

2

= O(d2 v) neighbor-neighbor edges, giving a pernode cost of O(dv + d2 v). Summing over all nodes yields a total complexity of

O

X v dv +

X v d2 v

!

= O m +

X v d2 v

!

, (13)

ranging from O(n) on sparse graphs to O(n3) in the fully connected worst case-yet with a much smaller constant factor than the global 2-FWL due to the locality of the LGAN.

In contrast, higher-order GNNs such as the k- GNNs (Morris et al. 2021) and tensor-based models (Maron et al. 2019, 2020) incur O(nk) complexity. In practice, the LGAN achieves linear runtime on sparse graphs, compared to the O(n3) cost of the 2-WL with lower expressivity.

## Experiments

In this section, we evaluate the LGAN on six graph classification benchmarks from social networks, bioinformatics, and chemistry (Yanardag and Vishwanathan 2015). We also demonstrate its interpretability via edge attribution using Integrated Gradients (Sundararajan, Taly, and Yan 2017).

## 6.1 Experimental Setups

Setup. We adopt a 10-fold cross-validation strategy with stratified splits that preserve the label distribution across folds. We report our results following the evaluation protocol described in (Xu et al. 2019). Node degree one-hot encodings are used for social networks, and provided node labels or attributes for bioinformatics and chemical datasets. Hyper-parameters. We tune the number of layers, hidden dimension, dropout, and learning rate for each dataset. Baselines. We compare the proposed LGAN against three representative categories of models: graph kernels, standard GNNs, and k-WL-based methods. Specifically, the graph kernel baselines include the random walk kernel (RW) (Vishwanathan et al. 2008), shortest path kernel (SP) (Borgwardt and Kriegel 2005), propagation kernel (PK) (Neumann et al. 2016), and 2-WL kernel (Morris et al. 2021). The GNN baselines include the DCNN (Atwood and Towsley 2016), PATCHY-SAN (Niepert, Ahmed, and Kutzkov 2016), DGCNN (Zhang et al. 2018) and GIN (Xu et al. 2019). The k-WL-based methods include the 1-2-3 GNN (Morris et al. 2021), PPGN (Maron et al. 2020), δk-LWL (Morris, Rattan, and Mutzel 2020), and CW Networks (Bodnar et al. 2022).

20919

<!-- Page 7 -->

Datasets

MUTAG PTC(MR) PROTEINS IMDB-B IMDB-M COLLAB # graphs 188 344 # classes 2 2 2 2 3 3 Avg. # nodes 18 26 39 20 13 74

Kernels

RW 79.2±2.1 55.9±0.3 59.6±0.1 N/A N/A N/A SP 81.7± 58.9± 76.4± 59.2± 40.5± N/A PK 76.0±2.7 59.5±2.4 73.7±0.7 N/A N/A N/A 2-WL 77.0± 61.9± 75.2± 72.6± 50.6± N/A

GNNs

DCNN N/A N/A 61.3±1.6 49.1±1.4 33.5±1.4 52.1±0.7 PATCHYSAN 92.6±4.2 60.0±4.8 75.9±2.8 71.0±2.2 45.2±2.8 72.6±2.2 DGCNN 85.8±1.7 58.6±2.5 75.5±0.9 70.0±0.9 47.8±0.9 73.8±0.5 GIN 89.4±5.6 64.6±7.0 76.2±2.8 75.1±5.1 52.3±2.8 80.2±1.9 k-WL-based

1-2-3 GNN 86.1± 60.9± 75.5± 74.2± 49.5± N/A PPGN 90.6±8.7 66.2±6.5 77.2±4.7 73.0±5.8 50.5±3.6 81.4±1.4 δ-2-LWL N/A N/A 75.1±0.3 73.3±0.5 50.2±0.6 N/A CW Networks 92.7±6.1 68.2±5.6 77.0±4.3 75.6±3.7 52.7±3.1 N/A

Ours LGAN 92.5±6.3 67.4±6.2 77.3±3.7 76.7±4.0 53.3±3.2 82.8±1.5 LGAN-res 92.0±5.8 66.6±7.0 76.8±3.6 76.6±3.1 53.5±2.7 82.7±1.7

**Table 1.** Test set classification accuracies (%). The mean accuracy and standard deviation are reported. Best performances are highlighted in bold, and second-best performances are underlined. N/A means Not Available.

## 6.2 Experimental Results and Analysis

**Table 1.** presents classification accuracies on six benchmark datasets. The proposed LGAN and LGAN-res achieve superior or comparable performance across most datasets. Compared to kernel-based methods and standard GNNs, our models offer consistently better accuracy. While several k- WL-based models attain strong results, they face scalability issues on large graphs (e.g., COLLAB). Overall, the LGAN strikes a favorable balance between accuracy and efficiency.

## 6.3 Interpretability via Edge Attribution

We assess the interpretability of the LGAN using edge attribution (Integrated Gradients) to determine whether it can identify critical substructures contributing to classification.

Figures 3(a) and (b) present two synthetic graphs G′ and H′, both of which are indistinguishable by the 2-WL due to having identical initial node features and neighborhood distributions. Similar to the pair in Figure 1, they differ only in the presence or absence of a triangle, which defines their class label. The LGAN successfully assigns high importance to the triangle edges, highlighting its ability to capture essential neighborhood interactions.

Figures 3(c) and (d) show two structurally similar molecules from the Mutagenicity dataset: 2-nitroanisole (mutagen) and 2-nitrobenzyl alcohol (non-mutagen). Both contain a nitro group (NO2), which is often associated with mutagenic activity. However, substituent difference (–OCH3 vs. –CH2OH) determines mutagenicity. The LGAN correctly emphasizes edges near critical functional groups, revealing chemically meaningful patterns. In summary, the LGAN offers fine-grained interpretability beyond the k-WL-based models that lack localized attribution.

5

4

3

2

1

0

(a) G’: No triangle

5

4

3

2

1

0

(b) H’: With triangle

O O

N H

C C

C H

C

C C

H H O

C H

H H

1.0

0.8

0.6

0.4

0.2

0.0

(c) Mutagen molecule

O O

N

C H H O C H C C H

C C C H

H

H

1.0

0.8

0.6

0.4

0.2

0.0

(d) Non-mutagen molecule

**Figure 3.** Edge visualizations with Integrated Gradients (redder and thicker edges represent higher importance).

## Conclusion

In this paper, we introduced the LGAN, a novel GNN that surpasses 2-WL expressivity through localized line graph aggregation. The LGAN is both efficient and interpretable, and performs competitively on graph classification tasks against state-of-the-art methods, including the k-WL-based models. Moreover, the LGAN can be naturally applied to node- and edge-level tasks, as its target-aware aggregation mechanism is general. In future works, we plan to extend the LGAN to more diverse applications, such as complex structural alignment and relational modeling (Bai et al. 2025).

20920

<!-- Page 8 -->

## Acknowledgments

This work is supported by the National Natural Science Foundation of China (No. 62576371, T2122020, 62576198, and 62471288).

## References

Atwood, J.; and Towsley, D. 2016. Diffusion-Convolutional Neural Networks. arXiv:1511.02136. Bai, L.; Cui, L.; Li, M.; Ren, P.; Wang, Y.; Zhang, L.; Yu, P. S.; and Hancock, E. R. 2025. AEGK: Aligned Entropic Graph Kernels Through Continuous-Time Quantum Walks. IEEE Transactions on Knowledge and Data Engineering, 37(3): 1064–1078. Bai, L.; Escolano, F.; and Hancock, E. R. 2016. Depth- Based Hypergraph Complexity Traces from Directed Line Graphs. Pattern Recognition, 54: 229–240. Bai, L.; Jiao, Y.; Cui, L.; Rossi, L.; Wang, Y.; Yu, P. S.; and Hancock, E. R. 2023. Learning Graph Convolutional Networks Based on Quantum Vertex Information Propagation. IEEE Transactions on Knowledge and Data Engineering, 35(2): 1747–1760. Bai, L.; Ren, P.; and Hancock, E. R. 2014. A Hypergraph Kernel from Isomorphism Tests. In Proceedings of International Conference on Pattern Recognition, 3880–3885. Bodnar, C.; Frasca, F.; Otter, N.; Wang, Y. G.; Li`o, P.; Mont´ufar, G.; and Bronstein, M. 2022. Weisfeiler and Lehman Go Cellular: CW Networks. arXiv:2106.12575. Borgwardt, K. M.; and Kriegel, H.-P. 2005. Shortest-Path Kernels on Graphs. In Proceedings of the IEEE International Conference on Data Mining, 74–81. Cai, J.-Y.; F¨urer, M.; and Immerman, N. 1992. An Optimal Lower Bound on the Number of Variables for Graph Identification. Combinatorica, 12(4): 389–410. Cai, L.; Li, J.; Wang, J.; and Ji, S. 2021. Line Graph Neural Networks for Link Prediction. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(9): 5103–5113. Chen, Z.; Li, X.; and Bruna, J. 2020. Supervised Community Detection with Line Graph Neural Networks. arXiv:1705.08415. Cui, L.; Bai, L.; Bai, X.; Wang, Y.; and Hancock, E. R. 2024. Learning Aligned Vertex Convolutional Networks for Graph Classification. IEEE Transactions on Neural Networks and Learning Systems, 35(4): 4423–4437. Grohe, M. 2017. Descriptive Complexity, Canonisation, and Definable Graph Structure Theory. Cambridge University Press. Grohe, M. 2022. The Logic of Graph Neural Networks. arXiv:2104.14624. Grohe, M.; and Otto, M. 2015. Pebble Games and Linear Equations. arXiv:1204.1990. He, K.; Zhang, X.; Ren, S.; and Sun, J. 2015. Deep Residual Learning for Image Recognition. arXiv:1512.03385. Huang, N. T.; and Villar, S. 2021. A Short Tutorial on the Weisfeiler-Lehman Test and Its Variants. In Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing, 8533–8537.

Lehot, P. G. 1974. An Optimal Algorithm to Detect a Line Graph and Output Its Root Graph. Journal of the Association for Computing Machinery, 21(4): 569–575. Liang, J.; Pu, C.; Shu, X.; Xia, Y.; and Xia, C. 2025. Line Graph Neural Networks for Link Weight Prediction. Physica A: Statistical Mechanics and its Applications, 661: 130406. Maron, H.; Ben-Hamu, H.; Serviansky, H.; and Lipman, Y. 2020. Provably Powerful Graph Networks. arXiv:1905.11136. Maron, H.; Fetaya, E.; Segol, N.; and Lipman, Y. 2019. On the Universality of Invariant Networks. arXiv:1901.09342. Morris, C.; Rattan, G.; and Mutzel, P. 2020. Weisfeiler and Leman Go Sparse: Towards Scalable Higher-Order Graph Embeddings. arXiv:1904.01543. Morris, C.; Ritzert, M.; Fey, M.; Hamilton, W. L.; Lenssen, J. E.; Rattan, G.; and Grohe, M. 2021. Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks. arXiv:1810.02244. Neumann, M.; Garnett, R.; Bauckhage, C.; and Kersting, K. 2016. Propagation Kernels: Efficient Graph Kernels from Propagated Information. Machine Learning, 102(2): 209– 245. Niepert, M.; Ahmed, M.; and Kutzkov, K. 2016. Learning Convolutional Neural Networks for Graphs. arXiv:1605.05273. Qin, X.; Bai, L.; Cui, L.; Li, M.; Du, H.; Wang, Y.; and Hancock, E. R. 2025. HA-SCN: Learning Hierarchical Aligned Subtree Convolutional Networks for Graph Classification. In Proceedings of the International Joint Conference on Artificial Intelligence, 3245–3253. Roussopoulos, N. D. 1973. A Max {m, n} Algorithm for Determining the Graph H from Its Line Graph G. Information Processing Letters, 2(4): 108–112. Sato, R. 2020. A Survey on the Expressive Power of Graph Neural Networks. arXiv:2003.04078. Shervashidze, N.; Schweitzer, P.; van Leeuwen, E. J.; Mehlhorn, K.; and Borgwardt, K. M. 2011. Weisfeiler- Lehman Graph Kernels. Journal of Machine Learning Research, 12(9): 2539–2561. Sundararajan, M.; Taly, A.; and Yan, Q. 2017. Axiomatic Attribution for Deep Networks. In Proceedings of the International Conference on Machine Learning, 3319–3328. Vishwanathan, S. V. N.; Borgwardt, K. M.; Kondor, I. R.; and Schraudolph, N. N. 2008. Graph Kernels. arXiv:0807.0093. Weisfeiler, B.; and Leman, A. 1968. The Reduction of a Graph to Canonical Form and the Algebra Which Appears Therein. Nauchno-Technicheskaya Informatsia, 2(9): 12– 16. Whitney, H. 1992. Congruent Graphs and the Connectivity of Graphs. Hassler Whitney Collected Papers, 61–79. Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2019. How Powerful Are Graph Neural Networks? arXiv:1810.00826. Xu, K.; Li, C.; Tian, Y.; Sonobe, T.; ichi Kawarabayashi, K.; and Jegelka, S. 2018. Representation Learning on Graphs with Jumping Knowledge Networks. arXiv:1806.03536.

20921

<!-- Page 9 -->

Yanardag, P.; and Vishwanathan, S. 2015. Deep Graph Kernels. In Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 1365–1374. Zaheer, M.; Kottur, S.; Ravanbakhsh, S.; Poczos, B.; Salakhutdinov, R.; and Smola, A. 2018. Deep Sets. arXiv:1703.06114. Zhang, M.; Cui, Z.; Neumann, M.; and Chen, Y. 2018. An End-to-End Deep Learning Architecture for Graph Classification. In Proceedings of the AAAI Conference on Artificial Intelligence, 4438–4445. Zhang, Z.; Sun, S.; Ma, G.; and Zhong, C. 2023. Line Graph Contrastive Learning for Link Prediction. Pattern Recognition, 140: 109537.

20922
