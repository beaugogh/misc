---
title: "Rational Transductors"
source_url: https://icml.cc/virtual/2026/oral/71133
paper_pdf_url: https://arxiv.org/pdf/2602.07599v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Rational Transductors

<!-- Page 1 -->

Rational Transductors

Mehryar Mohri mohri@google.com

Google Research

Contents

## Introduction

3

## 2 Rational Features

Framework 6 2.1 Weighted Automata........................................ 6 2.2 Rational Feature Layers...................................... 6 2.3 Parameterization of Transition Matrices............................ 6 2.4 Deep Integration of Rational Features............................. 9 2.5 Architectural Extensions..................................... 10

## 3 Motivation: Why Rational

Features? 12

## 4 Expressivity and

Complexity 13 4.1 Positional Encodings and Generalization........................... 14 4.2 Expressive Separations: Parity and Counting......................... 15 4.3 The Expressive Hierarchy..................................... 17 4.4 Structural Characterization.................................... 20 4.5 Circuit Complexity Characterization.............................. 23

## 5 Theoretical Analysis of

Learning 25 5.1 Universality and Efficiency of Random Features....................... 25 5.2 Optimization Dynamics...................................... 29 5.3 Generalization and Robustness................................. 31

## 6 Concrete Training

Recipe 33 6.1 Efficient Parallel Backpropagation............................... 34 6.2 Spectral Control: The Unified Scaled Cayley Parameterization.............. 34 6.3 Near-Identity Initialization.................................... 35

## 7 Empirical

Validation 35 7.1 The Regular Gap: Modulo Counting.............................. 36 7.2 Length Generalization and Time-Invariance......................... 37 7.3 Computational Efficiency and Extreme Scaling....................... 38 7.4 Algorithmic Generalization: Long-Integer Addition.................... 39 7.5 Quantitative Generalization and Precision.......................... 40

## 8 Conclusion 42

arXiv:2602.07599v1 [cs.LG] 7 Feb 2026

<!-- Page 2 -->

A Theoretical Background: Weighted Automata and Rational Power Series 46 A.1 Rational Power Series over a Field............................... 46 A.2 Linear Representations and WFAs............................... 46 A.3 Fundamental Results........................................ 46 A.4 Remarks on Terminology and Graph Interpretation.................... 47

B Experimental Details and Hyperparameters 48 B.1 Hyperparameter Specifications................................. 48 B.2 Statistical Significance and Stability.............................. 48

<!-- Page 3 -->

## Abstract

Standard Transformers excel at semantic modeling but struggle with rigid sequential logic and state tracking. Theoretical work establishes that self-attention is limited to AC0 (under hard attention) or TC0 (under soft attention), complexity classes that often fail to support robust length generalization on sequential problems without intermediate chain-of-thought. In this work, we introduce Rational Transductors, a dual-stream architecture that augments the Transformer with a matrix-valued recurrence derived from Weighted Finite Automata (WFA). By injecting rational state information into the attention mechanism via a Deep Rational Injection scheme, our framework strictly generalizes the expressive power of Transformers to capture all Regular Languages, NC1-complete problems (such as Boolean Formula Evaluation), and fundamental separations like Parity and Modular Counting, while preserving O(L + log T) parallel time complexity. We ground the architecture in a rigorous learning theory: we prove that Random Rational Features act as a universal basis for sequential dependencies, justifying our initialization strategy, while establishing that the Differentiable Rational Feature regime is necessary to close the representational compactness gap. Theoretical analysis and empirical results demonstrate that Rational Transductors solve the "Regular Gap," enabling robust length generalization on algorithmic tasks where standard Transformers fail, without the sequential computational bottlenecks of traditional RNNs.

## 1 Introduction

The Transformer architecture [Vaswani et al., 2017] has revolutionized sequence modeling, establishing itself as the de facto standard for natural language processing, code generation, and beyond. Its success is largely attributed to the self-attention mechanism [Schmidhuber, 1992, Graves, 2013, Bahdanau et al., 2014, Luong et al., 2015], which models long-range semantic dependencies by allowing every token to interact directly with every other token. However, this semantic power comes with a well-documented blind spot: standard Transformers struggle with rigid sequential logic and state tracking. Theoretical analyses have shown that self-attention—without intermediate recurrence or chain-of-thought—is limited to AC0 (under hard attention) [Hahn, 2020] or TC0

(under soft attention) [Merrill and Sabharwal, 2024b], complexity classes that struggle to represent unbounded sequential dependencies uniformly [Huang et al., 2025, Merrill et al., 2022]. While TC0 models can theoretically approximate tasks like parity, they lack the inductive bias to learn state-tracking solutions that generalize to unseen lengths. Specifically, standard Transformers often fail to learn robust solutions for tasks outside the C-RASP fragment [Yang et al., 2025a, Huang et al., 2025], such as modular counting. In practice, this manifests as brittleness: models trained on short contexts frequently fail to maintain consistent state (e.g., tracking variable values or nested brackets) when deployed on longer sequences.

To address these limitations, a resurgence of interest in Recurrent Neural Networks (RNNs) and State Space Models (SSMs) has emerged [Gu et al., 2021, Gu and Dao, 2023, Smith et al., 2022]. These architectures reintroduce a latent state that evolves over time, theoretically enabling infinite context tracking. However, they often face a structural trade-off: simple time-invariant recurrences (like S4) are efficient but lack expressivity. While recent selective state space models (like Mamba) introduce token-dependence to bridge this gap, they typically do so by interleaving recurrence into the deep backbone, which reintroduces layer-wise sequential dependencies during inference or training. In contrast, simple gated RNNs (like LSTM) remain fundamentally sequential. Unlike interleaved architectures that incur an O(L log T) training bottleneck due to sequential layer-wise recurrences, Rational Transductors decouple state-tracking from feature mixing. This allows the entire rational state history to be pre-computed via a single parallel scan, reducing the total parallel depth to O(L + log T).

<!-- Page 4 -->

In this work, we argue that the dichotomy between "Attention" (semantics) and "Recurrence" (syntax) is a false one. We introduce Rational Transductors, a dual-stream architecture that unifies the semantic flexibility of Transformers with the rigorous state-tracking capabilities of Weighted Finite Automata (WFA). Our approach is grounded in the formal theory of Rational Power Series [Schützenberger, 1961], which provides the mathematical foundation for regular languages and their quantitative generalizations.

We argue that the failure of Transformers to generalize on algorithmic tasks is not due to a lack of capacity, but a lack of syntactic inductive bias. To correct this, we augment the Transformer with a Rational Feature Head, a matrix-valued recurrence that acts as a dedicated co-processor for sequential logic. Crucially, unlike standard RNNs that use non-linear activations (tanh, sigmoid), our rational states evolve via linear matrix multiplication. This design choice yields two decisive advantages:

## 1 Parallel Scalability:

The linear recurrence ht = Mxtht−1 can be computed via parallel associative scans (prefix sums) in O(log T) time [Blelloch, 1990], bypassing the sequential bottleneck that plagues traditional RNNs.

## 2 Theoretical Transparency: The state dynamics correspond exactly to Weighted Finite

Automata [Mohri, 2009], allowing us to leverage decades of formal language theory, such as the Schützenberger representation theorem [Schützenberger, 1961] and Fliess’ Theorem [Fliess, 1974], to prove guarantees on expressivity and generalization that are impossible for black-box RNNs.

We ground this architecture in a rigorous learning theory (Section 5). First, analyzing the Random Rational Feature limit (Section 5.1), we prove that a sufficiently wide, randomly initialized rational head acts as a universal basis for sequential dependencies. This theoretical result justifies our use of near-identity initialization to capture long-term context from the start of training. However, we show that random features are exponentially inefficient for precise algorithmic tasks. Therefore, our primary contribution is the Differentiable Rational Feature regime, where the transition matrices are learned end-to-end. We prove that this learned regime strictly expands the expressivity of Transformers to capture all Regular Languages, NC1-complete problems (such as Boolean Formula Evaluation), and fundamental separations like Parity and Modular Counting, while maintaining numerical stability through novel spectral parameterizations (Section 5.2).

Related Work. Our work lies at the intersection of three active research streams:

• State Space Models (SSMs) and Linear RNNs: Recent advances in efficient sequence modeling, including S4 [Gu et al., 2021], Mamba [Gu and Dao, 2023], RWKV [Peng et al., 2023], DeltaNet [Schlag et al., 2021], and Kimi Linear [Zhang et al., 2025], rely on linearizing state updates to enable parallel training. While these architectures are often grounded in signal processing, our framework provides a complementary automata-theoretic characterization. Although existing literature has established complexity bounds and formal language mappings for certain linear recurrences [Merrill et al., 2022], the Rational Transductor framework formalizes this class by providing a rigorous algebraic completion via the Krohn-Rhodes decomposition. This allows us to prove that such linear recurrences are sufficient to solve the "Regular Gap" and capture NC1-complete reasoning while maintaining a decoupled sidecar design. Furthermore, unlike "Deep SSMs" (e.g., Mamba, H3) which interleave recurrence and mixing layers—thereby reintroducing layer-wise sequential dependencies during training—Rational Transductors adopt a "Sidecar" design. By keeping the recurrent state evolution strictly input-driven, we decouple state tracking (WFA) from feature mixing (Transformer),

<!-- Page 5 -->

ht−1,1 ht−1,2

State t −1 ht−1 ht,1 ht,2

State t ht

Mxt,11

Mxt,22

Mxt,12

Mxt,21

Linear Update: ht,i = ∑j Mxt,ijht−1,j

Input Token xt

**Figure 1.** Visualizing the Rational State Update. The hidden state vector ht (right) is computed as a linear transformation of the previous state ht−1 (left). Each component ht,i aggregates the weighted paths from the previous step, illustrating the "sum of paths" definition.

guaranteeing an optimal O(L + log T) parallel depth without the iterative approximations or serialization inherent to stacked SSMs.

• Expressivity of Transformers: Hahn [2020] and Merrill and Sabharwal [2024b] established the AC0 and TC0 upper bounds for Transformers (depending on attention hardness), highlighting their inability to robustly model sequential state. Our work provides a constructive proof that augmenting attention with linear recurrence is sufficient to break this barrier and capture NC1.

• Spectral Learning of Automata: We draw inspiration from spectral learning algorithms for WFAs [Balle and Mohri, 2015], effectively embedding a spectral extraction mechanism directly into the deep learning optimization loop.

By bridging the gap between deep learning and automata theory, Rational Transductors offer a principled path toward foundation models that are not only semantically fluent but also syntactically robust.

Paper Organization. The remainder of this paper is organized as follows. Section 2 formally defines the Rational Transductor architecture, detailing the WFA formalism, the structured parameterization of transitions, and the Deep Rational Injection method. Section 3 motivates the architecture by analyzing the complementary strengths of attention and rational recurrences. Section 4 provides a rigorous theoretical analysis of the model’s expressivity in the learnable regime, proving it solves the "Regular Gap." Section 5 analyzes the learning theory of the model, establishing results on the universality of random features, optimization stability, and generalization bounds. Section 6 outlines the concrete training recipe, including the parallel scan algorithm and stability-enforcing normalizations. Section 7 presents empirical validation, and Section A reviews foundational theory.

<!-- Page 6 -->

## 2 Rational Features Framework

## 2.1 Weighted Automata

We view state tracking through the lens of Weighted Finite Automata (WFA). Formally, a WFA over the field of real numbers R is defined as a tuple A = (Σ, d, α,{Mσ}σ∈Σ), where:

• Σ is the finite alphabet of tokens.

• d ∈N is the dimension of the state space (number of states).

• α ∈Rd is the initial state vector.

• Mσ ∈Rd×d is the transition matrix associated with token σ.

Given a sequence of input tokens x = (x1,..., xT), a standard WFA computes a scalar value. However, for the purpose of feature extraction, we are interested in the sequence of vectors ht ∈Rd

(hidden states) produced by the automaton, which is defined as follows:

ht = Mxtht−1, with h0 = α. (1)

The i-th component ht,i represents the sum of the weights of all paths labeled with the prefix x1∶t that end at state i, weighted by the initial values in α (see Figure 1). We extend the definition of the matrices Mσ to sequences using the shorthand Mx = MxT⋯Mx1, which allows us to write the state after processing the full sequence as hT = Mxα.

Omission of β. In classical automata theory, a WFA also includes a final weight vector β ∈Rd to map the final state to a scalar output. We omit β in our definition as we are only interested in the sequence of intermediate vectors in Rd (hidden states).

## 2.2 Rational Feature Layers

We define the rational feature vector ht at time step t as the forward state of the automaton after processing the prefix x1∶t, that is ht = Mx1∶tα. The state evolves according to the linear recurrence (1).

Unlike standard Recurrent Neural Networks (RNNs) which use non-linear activation functions (e.g., tanh or σ), the update in (1) is linear. This linearity is the defining characteristic of rational series and provides two distinct advantages:

## 1 Theoretical Clarity: It guarantees that the features capture Regular

Languages (and their weighted generalizations) exactly.

## 2 Parallel Scalability:

The recurrence ht = Mxt... Mx1α can be computed efficiently on modern hardware using parallel associative scans (prefix sums), avoiding the sequential bottleneck of standard RNNs. While the constant factor depends on matrix multiplication costs (potentially O(d3) or O(d2) depending on structure), we assume moderate d such that this overhead is negligible compared to the quadratic cost of attention.

## 2.3 Parameterization of Transition Matrices

The Rational Transductor framework is agnostic to the specific internal structure of the transition matrices Mσ. Examples include diagonal, permutation, orthogonal via Cayley parametrization, or diagonal-plus-low-rank matrices with fixed rank. While our experiments focus on two primary regimes (decay and conservation), the architecture supports any structured matrix family S ⊂Rd×d:

<!-- Page 7 -->

Input Token xt

+

Transformer Block 1

+

Transformer Block 2

⋮

+

Transformer Block L

Output yt

WFA Hidden

State ht

Proj

W(0) Proj

W(1) Proj

W(L−1)

z(0)

t z(1)

t

Parallel Scan O(log T)

Deep Rational

Injection

**Figure 2.** The Rational Transductor Architecture. The Rational Head extracts state variables ht. These states are injected into the Attention Stream via layer-specific projections W(l), augmenting the semantic hidden states z(l)

t.

Diagonal plus Low-Rank (DPLR). For general sequence modeling tasks requiring efficient mixing and fading memory, we adopt the structure:

Mσ = Dσ + UσV⊺ σ, (2)

where Dσ is diagonal and Uσ,Vσ ∈Rd×r are low-rank factors. While the DPLR structure reduces the cost of serial unrolling and inference to O(dr), parallel training via associative scans necessitates dense matrix-matrix multiplication. Consequently, the training recurrence scales as O(d3). This remains computationally efficient for the moderate state dimensions (d ∈[4,32]) used in this work, where the overhead is negligible compared to the O(T) costs of surrounding layers. Similar lowrank updates have been successfully deployed in other linear RNN architectures, such as DeltaNet, to approximate gradients efficiently.

Orthogonal Parameterization (Cayley). For algorithmic tasks requiring infinite memory conservation (e.g., modular counting), we parameterize Mσ to be strictly orthogonal (M⊺ σMσ = I). In practice, this is achieved via the Cayley transform. Let Wσ ∈Rd×d be a learnable parameter matrix. We construct a skew-symmetric matrix Aσ = Wσ −W⊺ σ and define the transition as:

Mσ = (I + Aσ)(I −Aσ)−1. (3)

Since the Cayley transform maps skew-symmetric matrices to the special orthogonal group SO(d), this guarantees that the state norm ∥ht∥2 is preserved exactly over infinite horizons, regardless of the

<!-- Page 8 -->

input sequence. We discuss a generalized version of this, the Unified Scaled Cayley Parameterization, in Section 6.2, which augments this form to support both exact conservation and learnable decay within a single differentiable framework.

Other Structured Families. We note that other structured parameterizations such as Butterfly matrices (for efficient FFT-like mixing), Toeplitz or Hankel matrices (for convolutional structures), or Block-Sparse matrices can be seamlessly substituted into the Rational Head to induce different inductive biases without altering the fundamental architecture or training recipe.

Shared Basis Parameterization. To further reduce parameters and improve generalization, we can express transitions as

Mσ =

K ∑ k=1 aσ,kBk, where {Bk}K k=1 are shared basis matrices and aσ,k are token-dependent coefficients. This reduces parameters, improves generalization, and connects to tensor factorization. This parameterization induces a low-rank tensor factorization over (σ, i, j) and allows the model to learn token-conditioned dynamics in a shared latent basis. Empirically, this sharing acts as a strong inductive bias that stabilizes training when ∣Σ∣is large.

Parallel Combination (Sum). We can construct a Mixed Rational Head by running multiple independent automata in parallel. Mathematically, this corresponds to the Direct Sum of the transition matrices:

Mσ = M(1)

σ ⊕M(2)

σ = ⎛

⎝

M(1)

σ 0 0 M(2)

σ

⎞ ⎠. (4)

This formulation allows the model to instantiate parallel heads with distinct dynamical biases (e.g., mixing a DPLR head for fading context with an Orthogonal head for exact counting). The resulting state dimension is additive (d = d1 + d2), maintaining efficiency.

Mixture of Dynamics (Universal Transductor). To enable a general-purpose architecture that requires no manual tuning, we propose the Universal Rational Transductor (Figure 3). Inspired by Multi-Head Attention, we instantiate parallel rational heads (via the Direct Sum above) with distinct dynamical properties:

• Orthogonal Heads (Cayley): Learn strictly norm-preserving rotations, ideal for continuous group operations and infinite memory tasks (e.g., counting, parity).

• Stochastic Heads (Simplex): Parameterized as column-stochastic matrices, these heads function as differentiable finite state automata, ideal for discrete logic, state switching, and "hard resets" (e.g., addition, regular languages).

The outputs of these diverse kernels are concatenated and projected, allowing the network to autonomously route signals to the dynamical system best suited for the underlying algorithm. While recent works like PD-SSM [Terzi´c et al., 2025] have empirically adopted diagonal/permutation structures, our Universal Transductor derives this architecture from first principles via the Krohn-Rhodes decomposition (Theorem 10). This proves that the mixture of orthogonal (group) and stochastic (aperiodic) heads is not merely an efficient heuristic, but the algebraically necessary structure for capturing the full hierarchy of regular languages.

<!-- Page 9 -->

Input xt

Head 1: Orthogonal γ = 1

(Counting/Memory)

Head 2: Stochastic

(Switching/Logic)

Concat ht

Algebraic Interpretation: ht = h(1)

t ⊕h(2)

t (Direct Sum)

**Figure 3.** The Universal Rational Transductor. The architecture instantiates parallel heads with distinct dynamical biases: Orthogonal (top) for infinite memory and Stochastic (bottom) for discrete switching. These independent features are concatenated, corresponding to the direct sum (⊕) of the underlying automata.

Note on Cross-Products. While the parallel combination implements the sum of rational series, one can also implement the Cross-Product (or Tensor Product) Mσ = M(1)

σ ⊗M(2)

σ to compute the Hadamard product (intersection) of two series. However, as this scales quadratically (d1 × d2), we typically rely on the downstream attention layers to compute these multiplicative interactions via the "Virtual Tensorization" mechanism (Section 15).

Computational Efficiency and Associativity. To use the parallel prefix scan algorithm (Section 2.2), the family of matrices M must be closed under multiplication. We explicitly note that the scan operation requires the associative aggregation of the dense operators Mt. We do not apply low-rank projections during the scan, as this would violate associativity. Instead, we maintain computational efficiency by restricting the rational state dimension d to be small (typically d ∈[4,32]). Under this constraint, the O(d3) cost of matrix-matrix multiplication at each step is negligible compared to the O(T) costs of the surrounding layers.

## 2.4 Deep Integration of Rational Features

A naive approach to integration would be to simply concatenate the rational feature vector ht to the input token embedding (Input Injection). While standard residual connections theoretically allow information to propagate to depth L, relying on them forces the Transformer to preserve the exact state ht within the semantic backbone zt, competing with feature extraction and suffering from signal attenuation due to repeated layer normalizations. To address this, we propose Deep Rational Injection. Instead of augmenting only the input, we inject the rational features directly into the hidden state of every Transformer block via an independent pathway. This ensures that a fresh, uncorrupted view of the precise state tracking information is available at all levels of abstraction.

Let z(l)

t ∈Rdmodel denote the Transformer’s hidden representation at time step t immediately before layer l (where l = 0 represents the initial token embeddings). We modify the input to each

<!-- Page 10 -->

layer l by adding a projected view of the rational state:̃ z(l)

t = z(l)

t + W(l)

projht (5)

where W(l)

proj ∈Rdmodel×d is a learnable linear projection unique to layer l. By using a layer-specific projection W(l)

proj, the model can extract different aspects of the state history relevant to different depths of processing. For instance, early layers might use ht for local syntactic parsing (e.g., matching parentheses), while deeper layers might use the same ht to resolve long-term dependencies (e.g., tracking subject-verb agreement across long clauses). The modified stream̃ z(l)

t is processed by the standard Self-Attention and Feed-Forward sub-layers, and the result is added residually to the original backbone:

z(l+1)

t = TransformerLayerl(̃z(l)

t). (6)

We use the standard Pre-Norm configuration, where TransformerLayer(x) = x + Attn(LN(x)) +

FFN(LN(x)), ensuring that the injected rational state gradients propagate directly without identifying vanishing through normalization layers. Crucially, because ht is computed via a parallel scan, this deep injection adds no sequential dependency to the Transformer, preserving the O(L + log T) parallel time complexity. This defines our models, rational transductors (RTs). Figure 2 illustrates their architecture.

## 2.5 Architectural Extensions

Stacked Rational Transductors. While the canonical Rational Transductor architecture (Figure 2) uses a single rational head broadcast to all layers, the framework naturally admits a stacked generalization. A Stacked Rational Transductor of depth K consists of a sequence of K Rational Transductor blocks, where the output stream of the k-th block serves as the input to the (k + 1)-th block. Formally, let u(k−1)

t be the input vector to block k at time t. The block computes a local rational state h(k)

t and updates the residual stream:

h(k)

t = M(k)

xt h(k)

t−1 + V(k)u(k−1)

t (7)

u(k)

t = TransformerBlockk(u(k−1)

t + W(k)

projh(k)

t) (8)

where M(k) is the transition logic specific to layer k.

The Linear Collapse Property. A crucial theoretical observation guides our preference for the single-head design over the naive stack. In the regime where the inter-layer dependence is mediated by a linear map applied to the previous block’s output (and no non-linearity is applied to the recurrent state), the cascade of WFAs is reducible.

Proposition 1 (Reducibility of Cascaded WFAs). A cascade of K linear Weighted Finite Automata, where the state of automaton k depends linearly on the state of automaton k −1, is algebraically equivalent to a single WFA with a larger state space dimension dtotal = ∑K k=1 dk.

Proof. Consider two stacked states h(1) and h(2). The joint system update can be written as a block triangular matrix:

⎛ ⎝ h(1)

t h(2)

t

⎞ ⎠= (M(1) 0 Winter M(2))⎛

⎝ h(1)

t−1 h(2)

t−1

⎞ ⎠ (9)

<!-- Page 11 -->

(a) Rational Transductor (Wide)

Input x

WFA ht

Parallel Scan

TF Block 1

TF Block 2

TF Block 3

(b) Non-Linear Stack (Deep)

Input x

TF Block 1

WFA h(2)

TF Block 2

WFA h(3)

Input-Driven

State

State depends on Layer 1

**Figure 4.** Architectural Comparison. (a) Wide Recurrence: The Rational Transductor computes a single high-dimensional state ht directly from the input via a parallel scan, injecting it into all layers. (b) Deep Recurrence: Stacked architectures (e.g., H3, Mamba) interleave recurrence, where Layer k depends on the output of Layer k −1, reintroducing a sequential bottleneck during training.

This block matrix defines a valid transition matrix Mjoint for a single WFA. Thus, stacking linear recurrences does not strictly expand the class of representable functions beyond TRat; it merely structures the transition matrix.

Despite this algebraic reducibility, there is a representation-theoretic benefit to the stacked parameterization. By enforcing the block-triangular structure inherent in the cascade, the model uses significantly fewer parameters to represent the same total state dimension, acting as a strong inductive bias for decomposable processes.

Theorem 2 (Cascaded Parameter Efficiency). Let C be a cascade of K linear WFAs with state dimensions d1,..., dK. The number of parameters required to specify the transitions of the cascade is O(∣Σ∣∑K k=1 d2 k). In contrast, a generic (unconstrained) single WFA with the equivalent state dimension D = ∑K k=1 dk requires O(∣Σ∣(∑K k=1 dk)2) parameters. Thus, the stacked architecture enforces a sparsity constraint that reduces the sample complexity of learning by a factor of O(K) when dk ≈d.

Non-Linear Stacking and Deep Recurrence. A natural question arises regarding the interaction between the rational features and the non-linear components of the Transformer. While our proposed architecture (Figure 2) uses a "sidecar" design where the rational states are strictly inputdriven, one could alternatively construct a Non-Linear Stacked Transductor. In this variant, the input to the k-th rational head is not the original token embedding, but the non-linear output of the (k −1)-th Transformer block.

Unlike the linear case, non-linear stacking strictly increases the expressive capacity of the architecture per unit of state dimension. Because the transition dynamics of layer k depend on the non-linear transformation of layer k −1, the system can realize functions that are not realizable by any single linear WFA of the aggregate dimension.

Theorem 3 (Non-Linear Irreducibility). There exist cascades of rational transductors with inter-layer non-linearities such that any single linear WFA capable of realizing the same transduction requires a state dimension D ≫∑K k=1 dk.

Proof. Consider a cascade of two WFAs (K = 2) with state dimensions d1, d2 ≥3. Let the first WFA compute a state h(1)

t ∈Rd1 and the second compute h(2)

t ∈Rd2, where the input to the second

<!-- Page 12 -->

WFA is modulated by the state of the first via a multiplicative interaction (e.g., attention or gating u(2)

t = u(1)

t ⊗h(1)

t). To simulate this non-linear interaction with a single linear system, one must linearize the product state space, requiring a state vector isomorphic to the tensor product h(1)

t ⊗h(2)

t. The dimension of this linearized system is D = d1 × d2. For all d1, d2 ≥2 (and strictly for d > 2), the tensor product dimension exceeds the sum of dimensions (d1d2 > d1 + d2). Thus, the nonlinear cascade represents a function class that is more compact (linear vs quadratic in d) than any equivalent single linear WFA.

However, this expressivity comes at a steep computational cost. In our "Single Head" design, the states ht are rational functions of the input x. Consequently, the entire state history for all layers can be pre-computed in parallel using a single pass of associative scans (O(log T) depth). In contrast, in the Non-Linear Stack, the input to the k-th recurrence u(k−1)

t depends on the attention output of the previous layer. This introduces a layer-wise sequential dependency: the parallel scan for layer k cannot commence until layer k −1 is fully computed. For a model with L layers, the parallel complexity scales as O(L log T).1 For deep foundation models (L ≈96) [Brown et al., 2020], this serialization reintroduces a significant training bottleneck. Our architecture thus prioritizes parallel efficiency, opting to capture complex dependencies via a wider, input-driven rational state rather than a deep, serial one.

## 3 Motivation: Why Rational

Features?

To understand why augmenting transformers with weighted automata is effective, we must consider the complementary strengths of the two architectures. We argue that Rational Features provide the sequential rigidity that attention mechanisms lack, without sacrificing the semantic flexibility or computational parallelizability that makes transformers successful.

Complementarity of State Tracking and Recall. To avoid ambiguity, we clarify our terminology: we use ‘Syntax’ to refer to rigid, rule-based state tracking (e.g., maintaining variable values, counting modulo k, or balancing nested brackets), and ‘Semantics’ to refer to soft, associative recall (e.g., retrieving related concepts across long distances). Standard Transformers excel at modeling semantic dependencies via the attention mechanism, which allows tokens to interact directly regardless of distance. However, attention is inherently set-based; it treats the context as a “bag of tokens” enriched only by weak positional heuristics. This makes precise tasks—such as counting modulo k, tracking nested parenthesis depth, or maintaining the status of a variable in code generation—surprisingly difficult for standard Transformers. In contrast, Weighted Finite Automata are inherently designed for this type of syntactic state tracking. By computing a rational feature vector ht, the model maintains a compact summary of the past that is mathematically guaranteed to capture regular languages exactly. The Rational Transductor thus operates with a bicameral design: we use this term metaphorically to reflect a division of labor akin to biological cognitive systems, where the WFA head handles sequential logic and state tracking (maintaining context over time), while the Attention head handles long-range correlations and associative recall (retrieving content from history).

Inductive Bias for Length Generalization. The failure to generalize in Transformers is largely a failure of inductive bias. Positional encodings (whether absolute or relative) are often brittle: a Transformer trained on sequences of length N frequently fails on length 2N because the positional

1While theoretical circuit constructions can potentially parallelize deep non-linear networks to O(polylog T) depth (e.g., via divide-and-conquer on the composition of layers), standard layer-wise implementations in deep learning frameworks enforce a sequential dependency of depth L, making O(L log T) the practical latency lower bound.

<!-- Page 13 -->

**Table 1.** Theoretical comparison of capabilities between finite-depth Transformers and Rational Transductors. Transductors strictly expand expressivity to include all regular languages while sharing the fundamental limitation on context-free grammars.

Task / Property Transformer Transductor Theoretical Reason

Parity (Lparity) ✗† ✓ Limited to AC0/TC0

Modular Counting ✗ ✓ Lack of cyclic state vs. WFA exactness All Regular Languages ✗ ✓ Star-free limitation vs. Rational completeness Length Generalization ✗ ✓ Positional drift vs. Time-invariant recurrence All Context-Free Languages ✗ ✗ Lack of unbounded memory stack

† While soft-attention Transformers (TC0) can theoretically approximate Parity for fixed lengths via averaging, they cannot represent the solution uniformly for unbounded lengths without precision scaling or Chain-of-Thought, and empirically fail to generalize.

representations drift out of distribution. Rational features solve this by injecting a recurrent inductive bias. The state update ht = Mht−1 is time-invariant; the logic used to transition from step 10 to 11 is identical to the logic used for step 1000 to 1001. If the WFA learns to count or track state correctly on short sequences, it mathematically must continue to do so for sequences of arbitrary length. This provides the Transformer with a stable anchor of state information that does not degrade as sequence length increases.

Efficiency via Linear Recurrence. Historically, adding recurrence to Transformers (as in Transformer-XL or hybrids) introduced a sequential bottleneck, preventing parallel training. Rational features circumvent this trade-off. Because the transition function is linear (ht = Mtht−1), we avoid the need for sequential backpropagation through time. Instead, the sequence of states can be computed using parallel associative scans (or prefix sums) in O(log T) time on GPUs/TPUs. This ensures that adding rational features incurs negligible wall-clock overhead compared to the quadratic cost of attention, maintaining the scalability required for foundation models.

## 4 Expressivity and Complexity

In this section, we analyze the expressivity and generalization capabilities of Rational Transductors. We summarize our main findings in Table 1, which highlights that Transductors strictly generalize standard Transformers to capture all regular languages and NC1 complexity.

Theoretical Setup. Unless otherwise stated, all expressivity results assume exact or boundedprecision arithmetic with error tolerance independent of sequence length. For lower bounds, we define “Standard Transformers” as uniform families of fixed-depth architectures without auxiliary memory (no Chain-of-Thought). Under these constraints, Transformers are limited to AC0 (hard attention) [Hahn, 2020] or TC0 (soft attention) [Merrill and Sabharwal, 2024b], preventing them from solving sequential problems like Parity which require depth scaling with input length. Note that while this section focuses on representational capacity, we explicitly address numerical stability and optimization dynamics in Section 5.

Interpretation of Results. Table 1 illustrates that Transductors occupy just the right zone of expressivity. By integrating the WFA head, they overcome the fundamental inability of standard

<!-- Page 14 -->

Transformers (restricted to AC0 under hard attention, or TC0 under soft attention) to uniformly handle periodic and sequential logic (such as Parity and MODk), effectively solving the Regular Gap. Crucially, however, Transductors do not attempt to solve the Context-Free Gap; like standard Transformers, they lack the unbounded stack required for tasks like hierarchical bracket matching. This deliberate design choice preserves the O(L +log T) parallel time complexity that general RNNs or stack-augmented models sacrifice.

## 4.1 Positional Encodings and Generalization

We first show that our framework strictly generalizes modern positional encoding schemes.

Lemma 4 (Positional Encodings are Rational). Over the field of real numbers R, let P ∈RT×d be the matrix of Rotary Positional Embeddings (RoPE) or sinusoidal encodings. There exists a Weighted Finite Automaton A = (Σ, d, α,{Mσ}) such that for any position t, the rational feature vector ht is exactly the positional encoding at index t, independent of the input tokens.

Proof. Standard sinusoidal and rotary embeddings are defined by frequencies Θ = {θi}d/2 i=1. The encoding at position t is typically constructed by rotating pairs of dimensions. Consider the block-diagonal rotation matrix R:

R =

⎛ ⎜⎜⎜⎜ ⎝

Rθ1 0... 0 0 Rθ2... 0 ⋮ ⋮ ⋱ ⋮ 0 0... Rθd/2

⎞ ⎟⎟⎟⎟ ⎠

, where Rθi = (cos θi −sin θi sin θi cos θi) (10)

We define a WFA A as follows:

• Let the initial state α = (1,0,1,0,...,1,0)⊺∈Rd.

• Let the transition matrix Mσ = R for all σ ∈Σ. (The transition is input-independent).

The rational feature vector at time t evolves as ht = Mxt... Mx1α = Rtα. Since R is block-diagonal, we can analyze the evolution of the i-th pair of dimensions independently:

(ht,2i−1 ht,2i) = (cos θi −sin θi sin θi cos θi)

t

(1

0) = (cos(tθi) sin(tθi)). (11)

This matches exactly the definition of sinusoidal positional encodings. Thus, standard positional information is a special case of rational features where the transition matrices are unitary and inputindependent. While RoPE is typically applied as a modulation within the attention mechanism, this lemma demonstrates that the underlying state tracking mechanism is representable by a WFA.

This lemma implies that Transductors start with the full capability of standard Transformers (via PE) but extend it by allowing the transition matrices Mσ to be input-dependent, enabling the tracking of semantic states rather than just wall-clock time.

The construction in Lemma 4 formalizes the “RoPE Trick” used in recent linear attention and SSM architectures [Dao and Gu, 2025, Yang et al., 2025b]. However, while RoPE has traditionally been viewed as a positional modulation, this result provides the first rigorous proof that it constitutes a specific Rational Inductive Bias. This formalization explains precisely why RoPE fails to generalize length on algorithmic tasks: it constrains the recurrence to track input-independent relative position, rather than the input-dependent state required for semantic generalization.

<!-- Page 15 -->

Even h0 Odd

0

1

0

1

(a) Parity WFA

0 h0

1 2

0

0 0

1

1

1

(b) Modulo-3 Counter

**Figure 5.** State tracking mechanisms for exact regular languages. (a) The Parity WFA uses a 2-state flip mechanism to track Lparity. (b) The Modulo-3 WFA generalizes this to a cyclic group structure to solve Lk for k = 3. Input ‘0‘ acts as the Identity I (self-loop), while input ‘1‘ acts as a permutation.

## 4.2 Expressive Separations: Parity and Counting

Theorem 5 (The Parity Gap). Let Lparity be the language of binary strings x ∈{0,1}∗containing an odd number of 1s.

## 1 A standard Transformer with fixed depth, hard attention, and bounded-precision arithmetic cannot uniformly recognize

Lparity for input sequences of unbounded length.

## 2 There exists a Rational

Transductor with state dimension d = 2 that recognizes Lparity with 100% accuracy for any length T.

Proof. Part 1 (Transformer Limitation): Theoretical lower bounds establish that uniform AC0 circuits (Hard Attention) cannot compute Parity [Hahn, 2020]. While soft-attention Transformers are strictly more expressive, recent analysis proves they remain bounded within TC0 (Threshold Circuits) even with arbitrary precision, provided they operate in fixed depth [Merrill and Sabharwal, 2024b]. Turing completeness is only achievable when the model is permitted to generate intermediate Chain-of-Thought tokens, effectively using the context as a read-write tape [Pérez et al., 2021, Merrill and Sabharwal, 2024a]. Finite-depth models without such scratchpads remain bounded in computational power and, crucially, lack the inductive bias to learn robust algorithmic solutions [Merrill et al., 2022].

Part 2 (Rational Feature Solution): We construct a WFA A with d = 2 states that tracks the parity of the number of 1s (see Figure 5(a)). Let the state vector be ht ∈R2, where ht = (1,0)⊺represents an “Even” state and ht = (0,1)⊺represents an “Odd” state.

• Initial State: α = (1,0)⊺(0 is an even number).

• Transitions: For input token ‘0’, the count does not change. We set M0 = I = (1 0 0 1). For input token ‘1’, the parity flips. We set M1 = (0 1 1 0). (Note: While a standard Cayley parameterization in d = 2 is restricted to SO(2) and cannot represent the reflection matrix M1, this can be realized in the Rational Transductor by augmenting the state space to d ≥3. As detailed in Section 6.2, a rotation in three dimensions can embed the required reflection logic, ensuring algebraic completeness.)

<!-- Page 16 -->

The state update ht = Mxtht−1 performs exact modular arithmetic. If the number of ones is even, hT = (1,0)⊺; if odd, hT = (0,1)⊺. The Rational Transductor injects this hT into the final layer. A simple linear classifier (readout head) w = (0,1)⊺can then perfectly classify the sequence as y = sign(w⊺hT). This holds for any sequence length T, proving the claim.

Note that the construction in Part 2 explicitly relies on the learned parameterization (Regime II), where we can set Mσ to specific permutation matrices.

Theorem 6 (Exact Modular Counting). For any fixed integer k ≥2, there exists a Rational Transductor with state dimension d = k that exactly recognizes the language

Lk = {x ∈{0,1}∗∶#1(x) ≡0 (mod k)}

for sequences of arbitrary length, whereas finite-depth Transformers cannot uniformly recognize Lk.

Proof. The negative result for standard Transformers follows from the fact that MODk gates are not realizable in AC0 for any k ≥2 [Smolensky, 1987]. For the Rational Transductor construction, we generalize the parity mechanism to the cyclic group Zk. We define a WFA with dimension d = k where the basis vector ei represents the current count being i (mod k) (see Figure 5(b)).

• Initial State: α = e0 = (1,0,...,0)⊺.

• Transitions: Let M0 = Ik (identity). Let M1 be the cyclic permutation matrix where (M1)ij = 1 if i ≡(j + 1) (mod k) and 0 otherwise.

The state update ht = Mxtht−1 ensures that if the current count is j, reading a ‘1’ moves the probability mass to (j + 1) (mod k). Thus, hT = er where r = #1(x) (mod k). A linear readout w = e0 correctly identifies if x ∈Lk.

Note: As with Parity, this capability assumes the learned regime, where the model can discover and maintain orthogonal transition matrices.

Theorem 7 (Exact Arithmetic Evaluation). Let valb∶Σ∗→N be the function that interprets a string x ∈{0,..., b −1}∗as a number in base b (e.g., for binary b = 2, "101" ↦5). There exists a Rational Transductor with state dimension d = 2 that computes valb(x) exactly for sequences of arbitrary length (assuming computation over R).

Proof. This function corresponds to the Horner scheme for polynomial evaluation. We construct a WFA with state vector ht = [vt,1]⊺, where vt is the current accumulated value.

• Initial State: α = [0,1]⊺.

• Transitions: For a digit σ ∈{0,..., b −1}, the update rule is vt = b ⋅vt−1 + σ. This is an affine transformation representable by the matrix:

Mσ = (b σ 0 1). (12)

The recurrence yields ht = Mxtht−1. The first component of hT exactly holds ∑T t=1 xt ⋅bT−t. A linear readout w = [1,0]⊺retrieves the integer value. Standard Transformers with bounded activations or attention scores cannot represent this unbounded growth function exactly, nor can standard RNNs with saturating non-linearities (e.g., tanh).

<!-- Page 17 -->

Generalization. This result illustrates a capability distinct from the finite-state logic of Parity or Modulo-k. As shown in prior work on the expressivity of weighted automata [Cortes and Mohri, 2000], WFAs can represent broad families of functions mapping strings to numerical values, including polynomial evaluations and probabilistic distributions. The Rational Transductor inherits this capacity to model quantitative, unbounded dependencies that are inaccessible to architectures constrained by saturation or bounded precision.

Recognition of Context-Free Languages. While we emphasized the distinction between Regular and Context-Free capabilities in Table 1, the ability to perform exact arithmetic (Theorem 7) theoretically bridges this gap. As established in [Cortes and Mohri, 2000], the support of rational power series over infinite fields can characterize certain Context-Free Languages, including palindromes and Dyck paths, by leveraging arithmetic "counting" mechanisms to enforce structural constraints (e.g., mapping balanced nested structures to a zero-sum weight). Thus, Rational Transductors possess the latent capacity to "recognize" these languages through quantitative embedding, though robust learning of such unbounded arithmetic solutions in practice requires high precision and specific inductive biases.

## 4.3 The Expressive Hierarchy

We can situate Rational Transductors within the broader hierarchy of sequence modeling architec- tures. The Rational Transductor framework occupies a precise theoretical niche, strictly generalizing both Rational Power Series and standard Transformers.

Proposition 8 (Expressive Hierarchy). Let FRat, FTF, FRT, and FRNN denote the classes of functions computable by Rational Power Series (linear WFAs), finite-depth Transformers, Rational Transductors, and general Recurrent Neural Networks, respectively. The following strict inclusions hold:

(FRat ∪FTF) ⊊FRT ⊊FRNN. (13)

Proof. We establish each inclusion and its strictness separately.

## 1 Rational

Series (FRat ⊊FRT). Any rational series is computable by a WFA [Schützenberger, 1961]. A Rational Transductor recovers this exactly by learning the corresponding transitions {Mσ} and setting the Transformer layers to perform a fixed linear readout. The inclusion is strict because Transductors can apply non-linear operations (e.g., softmax attention, layer normalization) to the sequence of rational states, whereas FRat is limited to linear transductions.

2. Transformers (FTF ⊊FRT). A Rational Transductor recovers a standard Transformer if the rational projection weights are set to zero (Wproj = 0). The strictness is proven by Theorem 5 and Theorem 6: Transductors can uniformly recognize Parity and Modular Counting languages, whereas standard Transformers (limited to AC0) cannot.

## 3 Recurrent Neural

Networks (FRT ⊊FRNN). Rational Transductors are a specific instance of RNNs where the state transition is strictly linear (ht = Mxtht−1). General RNNs allow for non-linear state dynamics (e.g., tanh), which encompass linear updates in the small-signal regime (linear region of the activation). The inclusion is strict because the linear state dynamics of the Transductor admit a parallel-prefix decomposition, limiting them to PNC1. In contrast, general RNNs with nonlinear activations and unbounded precision are P-complete (sequentially strictly harder). While linear Transductors can represent specific bounded Context-Free Languages (such as Boolean Formula Evaluation) via their NC1 capacity [Huang et al., 2025], they lack the unbounded stack required to recognize all Context-Free Languages (e.g., Dyck-k of arbitrary depth) uniformly.

<!-- Page 18 -->

Algebraic Completeness via Krohn-Rhodes. From the perspective of algebraic automata theory, the Krohn-Rhodes theorem establishes that any finite state machine can be decomposed into a cascade of simple groups (counters) and aperiodic monoids (threshold logic). Standard self-attention is known to be limited to the aperiodic component (star-free languages) [Hahn, 2020]. By incorporating linear recurrence, which naturally implements cyclic group operations (as seen in Theorem 6), Transductors effectively recover the group-theoretic component. Thus, Transductors provide a structurally complete architecture capable of modeling both the periodic and aperiodic sub-structures of all regular languages.

Descriptive Complexity and MSO. In the framework of descriptive complexity, standard Transformers are often associated with First-Order Logic (FO[<]), which describes star-free regular languages but fails to capture modulo counting quantifiers. In contrast, Weighted Finite Automata are intimately linked to Monadic Second-Order Logic (MSO[<]) over fields. By bridging these architectures, Transductors effectively lift the expressivity of the model from the limitations of first-order predicates to the fuller expressive range of monadic second-order logic on sequences.

Proposition 9 (Effective Capacity Increase). For any fixed horizon L, the pseudo-dimension of Rational Transductors strictly exceeds that of finite-depth Transformers with the same hidden dimension, due to the ability to linearly separate histories that are indistinguishable under attention-only architectures.

Proof. Let HTF and HRT be the hypothesis classes of finite-depth Transformers and Transductors. Consider the set of all binary sequences of length L, SL = {0,1}L, and the subset of labelings defined by y(x) = Parity(x). A Rational Transductor with d = 2 can realizably separate SL according to parity labelings (Theorem 5). Conversely, for fixed model size, there exists a length L such that a standard Transformer (AC0) cannot compute Parity [Furst et al., 1984], failing to shatter SL. Since HTF ⊆HRT and Transductors can realize dichotomies (parity) that Transformers cannot, Pdim(HRT) > Pdim(HTF).

Theorem 10 (Representational Completeness via Krohn-Rhodes). Let A be any deterministic finite automaton with state set Q and input alphabet Σ. There exists a parameter setting θ for a Stacked Rational Transductor (see Section 2.5) of finite depth L and width d such that the model exactly simulates the state transitions of A. Specifically, the architecture admits a parameterization that realizes the Krohn-Rhodes decomposition (SL ≀⋅⋅⋅≀S1) ≀(RL ≀⋅⋅⋅≀R1), where the Rational Feature Heads implement the simple groups Si and the Transformer layers implement the cascading feedback functions required by the wreath product.

Proof. The Krohn-Rhodes theorem states that any finite automaton can be decomposed into a cascade (wreath product) of finite simple groups and aperiodic monoids (resets) [Krohn and Rhodes, 1965]. We construct a parameterization of the Rational Transductor that physically instantiates this cascade.

## 1 The Wreath Product

Structure. A wreath product M2 ≀M1 is driven by a feedback function ϕ ∶Q1 × Σ →End(Q2), where the update rule for the second machine depends on the state of the first:

q(2)

t = q(2)

t−1 ⋅ϕ(q(1)

t−1, xt). (14)

## 2 Structural

Mapping. We map the cascade layers 1... L to the Transductor layers.

• Group Components (Si): The Rational Feature Head at layer i is parameterized to implement the group operations. For a simple group G, we set the transition matrices Mσ to be the permutation matrices representing the group elements.

• Aperiodic/Feedback Components (ϕ): The Transformer block between layer i and i + 1 implements the feedback function ϕ. The input to layer i + 1’s head is ut = FFN(LayerNorm(z(i)

t)).

<!-- Page 19 -->

## 3 Exact Implementation of Feedback

Logic. The function ϕ is a map over a finite domain (discrete states Q1 and alphabet Σ). It is a standard result that a Feed-Forward Network (FFN) with ReLU activations and sufficient width can exactly represent any function over a finite boolean domain (e.g., implementing arbitrary logic gates or look-up tables). Thus, there exists a setting of the FFN weights such that:

M(i+1)

t = Proj(FFN(Embed(q(1)

t−1) + Embed(xt))) (15)

exactly recovers the transition operator required by the wreath product logic ϕ(q(1)

t−1, xt). Conclusion. Since the architecture contains components capable of representing both the algebraic primitives (via linear recurrence matrices) and the arbitrary Boolean glue logic (via FFNs), there exists a parameter configuration that exactly simulates the full Krohn-Rhodes cascade.

Algebraic Division of Labor. This structural alignment highlights a natural division of labor within the architecture. The Rational Feature Head is uniquely suited to implement the permutation components (finite simple groups) of the decomposition via orthogonal recurrence matrices—precisely the structures that standard self-attention fails to represent uniformly. Meanwhile, the Transformer backbone (via FFNs and attention heads) efficiently implements the aperiodic components (reset logic, thresholds) and the cascading dependencies required to glue the decomposition together.

Significance: A Constructive Algebraic Completion. This result offers a fundamental algebraic justification for the Rational Transductor architecture, moving beyond simple expressive capacity arguments. It is established that standard self-attention is limited to recognizing star-free languages, which algebraically correspond to aperiodic monoids (threshold logic and resets). By augmenting this aperiodic component with a linear recurrence capable of implementing finite simple groups (permutations and cycles), the Rational Transductor effectively physically instantiates the Krohn- Rhodes decomposition of finite automata. In this view, the "Deep Rational Injection" mechanism functions as the wreath product operator, cascading the cyclic state information (from the group component) into the aperiodic logic (of the attention component). Thus, the architecture is not merely a heuristic ensemble, but a structurally complete neural realization of the fundamental algebraic components required to recognize any regular language, explicitly repairing the specific group-theoretic deficiency of the Transformer.

Theorem 11 (Logical Characterization via Weighted MSO). Let W-MSO[<] be the Weighted Monadic Second-Order Logic over the commutative semiring K (in this work, the field K = (R,+,×)). Under the restriction of hard attention (which implements FO[<] selection) and the assumption that the Transformer layers are constrained to linear projections (effectively disabling non-linear FFNs), the class of functions representable by Rational Transductors FRT coincides exactly with the class of functions definable in W-MSO[<]. That is:

FRT[HardAttn, Linear] = JW-MSO[<]K. (16)

Proof. We establish the equality by mutual inclusion.

## 1 Lower

Bound (JW-MSOK ⊆FRT). A fundamental result by Droste and Gastin [2007] establishes that for any formula ϕ ∈W-MSO[<] over a field, there exists a Weighted Finite Automaton (WFA) Aϕ that computes the same series. Since the Rational Feature Head of a Transductor can implement any WFA (by learning the transition matrices Mσ), and the Transformer layers can implement the linear readout (by setting Wproj to inject the final state and attention to identity), every W-MSO formula is realizable by a Rational Transductor.

## 2 Upper

Bound (FRT ⊆JW-MSOK). We show that the computation of a Rational Transductor is definable in W-MSO.

<!-- Page 20 -->

• Recurrence: The linear update ht = Mxtht−1 is a regular recurrence, which is known to be definable in MSO (specifically, the relation "state at t is q" is MSO-definable).

• Hard Attention: Hard attention performs a selection yt = xk where k = argmaxj(qt ⋅kj). The argmax and indexing operations are First-Order (FO[<]) definable relations.

• Composition: Since FO[<] ⊂MSO[<], the composition of the recurrence (MSO) and the attention mechanism (FO) remains within W-MSO.

Thus, the entire input-output mapping of the hard-attention Rational Transductor can be described by a single Weighted MSO formula.

Soft Attention and Extended Expressivity. We note that standard Transformers use soft attention, which strictly exceeds the expressivity of FO[<] and can approximate specific Context-Free Languages like Dyck-1 (anbn) [Merrill and Sabharwal, 2024b]. Consequently, a Rational Transductor with soft attention theoretically exceeds the W-MSO upper bound. However, the hard-attention equivalence (Theorem 11) serves to formalize the specific contribution of the Rational Head: it provides the monadic quantifiers (state tracking) that are structurally absent in the attention mechanism, regardless of precision.

Remark on Logical Completeness (Weighted MSO). This algebraic perspective naturally extends to descriptive complexity. It is a classical result that Weighted Finite Automata are expressively equivalent to Weighted Monadic Second-Order Logic (W-MSO[<]) [Droste and Gastin, 2007]. Standard Transformers are known to correspond to First-Order Logic (FO[<]), which effectively captures the "aperiodic" component of language but fails to express the "group" component (modulo counting). By structurally integrating a WFA (which captures the full power of MSO on sequences) with Attention (FO), the Rational Transductor architecture effectively bridges the gap between First-Order and Second-Order logic. This implies the model is logically complete for quantitative regular properties, contrasting with standard Transformers which are strictly limited to first-order expressivity.

## 4.4 Structural Characterization

We can rigorously characterize the class of functions computable by Rational Transductors FRT as the exact composition of the Transformer class with the class of Vector-Valued Rational Functions.

Definition 12 (Vector-Valued Rational Functions). Let Σ be an input alphabet. A function Φ∶Σ∗→ (Rd)∗is a Vector-Valued Rational Function if it is realizable by a Weighted Finite Automaton (WFA). That is, there exists a linear representation (α,{Mσ}σ∈Σ) such that for any input x = (x1,..., xT), the output is the sequence of state vectors Φ(x) = (h1,..., hT) defined by the recurrence ht = Mxtht−1 (with h0 = α). We denote this class as TRat.

Theorem 13 (Decomposition Characterization). Let TRat be the class of vector-valued rational functions defined above. Let FTF be the class of functions computable by finite-depth Transformers. The class of Rational Transductor functions is exactly the composition of these two classes:

FRT = FTF ○TRat (17)

That is, a function F is a Rational Transductor if and only if F(x) = G(Φ(x)) for some G ∈FTF and

Φ ∈TRat.

<!-- Page 21 -->

Proof. Direction 1 (FRT ⊆FTF ○TRat): We show that the Deep Rational Injection mechanism can be simulated by a standard Transformer given access to the rational states. A Rational Transductor computes layers via z(l+1)

t = TFl(z(l)

t + W(l)

projht). Consider a standard Transformer G taking the concatenated input ut = [xt; ht]. A standard Transformer can simulate the Transductor’s deep injection by: (1) Dedicating a subspace of its residual stream to copy ht forward to all layers (using identity attention/FFN weights); and (2) At each layer l, applying the linear operation corresponding to W(l)

proj to this subspace and adding it to the processing stream. Thus, any function computed by a Transductor is computable by a standard Transformer acting on the sequence (x, Φ(x)), where Φ ∈TRat.

Direction 2 (FTF ○TRat ⊆FRT): Consider an arbitrary composition F(x) = G(Φ(x)), where G is a Transformer and Φ is a rational function. By definition, Φ(x) corresponds to the state sequence ht of some linear representation. A Rational Transductor can implement this composition by: (1) Configuring its WFA head to generate ht; (2) Setting the first projection W(0)

proj to inject ht directly into the input embedding (simulating the input to G); and (3) Setting subsequent projections W(l)

proj = 0 for l > 0. The remaining Transformer layers then implement G exactly.

Corollary 14 (Maximality Under Linear Recurrence). Any extension of finite-depth Transformers that augments the model with a fixed-dimensional, associative, linear state update computable via parallel prefix operations cannot be strictly more expressive than Rational Transductors. Any further expressivity gain requires either non-linear state dynamics or depth growing with input length.

Proof. An "associative, linear state update" is defined by a recurrence of the form ht = M(xt)ht−1. This is mathematically isomorphic to the state evolution of a Weighted Finite Automaton. Since Transductors are defined (Theorem 13) as the composition of Transformers with the entire class of such rational functions TRat, they necessarily subsume any specific instance of this recurrence pattern.

Minimal Expressive Extension. Transductors constitute a minimal extension of standard Transformers that suffices to escape the AC0 barrier while preserving parallelizability. Thus, Transductors represent the smallest algebraically closed class of extensions that enable exact regular-language computation and length generalization.

Proposition 15 (Virtual Tensorization via Attention). Let ht ∈Rd be the rational feature state at time t. The Deep Rational Injection mechanism, combined with a single Self-Attention head, allows the Transductor to compute decision boundaries that are linear in the Kronecker product space ht ⊗ht′. Consequently, a Rational Transductor with state dimension d can approximate the expressive power of a higher-order Weighted Finite Automaton with state dimension d2, without explicitly materializing the O(d6) transition tensor.

Proof. Consider the input to the attention mechanism at layer l, denoted bỹ zt. Due to Deep Rational Injection, this vector is the sum of the semantic embedding and the projected rational state:̃ zt = zt + Wprojht. (18)

The self-attention mechanism computes alignment scores At,t′ between positions t (query) and t′

(key) via the inner product of projected representations:

Score(t, t′) = (WQ̃zt)⊺(WK̃zt′) (19)

= (zt + Wprojht)⊺W⊺

QWK(zt′ + Wprojht′). (20)

<!-- Page 22 -->

Expanding this quadratic form yields four terms. We focus on the term governing the interaction between the rational states:

Srational(t, t′) = h⊺ t (W⊺ projW⊺

QWKWproj)ht′. (21)

Let M = W⊺ projW⊺

QWKWproj be the effective interaction matrix. Using the vectorization identity a⊺Mb = vec(M)⊺(b ⊗a), we can rewrite the score as:

Srational(t, t′) = vec(M)⊺(ht′ ⊗ht). (22)

This demonstrates that the attention mechanism implicitly computes a linear function over the tensor product of the states. Physically stacking two WFAs would produce a state space of dimension d1 + d2, but the attention mechanism allows the model to leverage the multiplicative interactions of the states, effectively simulating a state space of dimension d × d. Thus, the Transductor can capture second-order dependencies (e.g., correlating the state at the start of a clause with the state at the end) that would otherwise require a significantly larger linear automaton to represent.

Significance: Implicit State Expansion. The theoretical significance of this result is twofold. First, it provides a rigorous justification for the "Sidecar" design (wide, parallel recurrence) over the "Stacked" design (deep, serial recurrence) used in recent hybrid models. While stacking linear layers physically increases the state depth, it reintroduces sequential dependencies that hinder training [Gu et al., 2021]. In contrast, Virtual Tensorization reveals that the interaction between the Rational Head and the Attention mechanism naturally simulates a higher-order automaton. By injecting the linear state ht into the query/key projections of the attention layer, the dot-product Attention(Q, K) effectively computes a kernel over the tensor product space ht ⊗ht′. This implies that a Rational Transductor with state dimension d can approximate the decision boundaries of a much larger automaton of dimension d2 (or higher, with multiple layers), achieving the expressive benefits of deep recurrence without incurring the O(L log T) serialization penalty or the O(d6) cost of explicitly simulating higher-order tensor dynamics. Thus, the architecture achieves a "virtual depth" via the multiplicative interactions of attention, maintaining the optimal O(log T) parallel efficiency of the linear scan while capturing the complex, hierarchical dependencies usually associated with deep, non-linear stacks.

Remark: Neural Implementation of Automata Operations. The Rational Transductor architecture can be understood as a physical realization of the closure properties of Rational Power Series:

• Parallel Heads as Direct Sum (⊕): Instantiating multiple independent rational heads (e.g., in the Universal Transductor) corresponds to the Sum operation. If head A tracks parity and head B tracks modulo-3, the concatenated state h = [hA; hB] represents the direct sum automaton AA ⊕AB, capable of tracking both features in parallel.

• Attention as Tensor Product (⊗): The Intersection of two regular languages (e.g., "strings that have odd parity AND length 0 (mod 3)") requires a state space isomorphic to the tensor product of the constituent automata. While the rational layer computes the sum, the subsequent non-linear mixing (via Attention or MLP) approximates the Cross-Product or Hadamard Product, allowing the model to form complex decision boundaries based on the conjunction of independent rational features.

<!-- Page 23 -->

Semantic zt

Rational ht

+ ˜zt

WQ

WK

×

Q

KT

Attention Score

Implicit Term: h⊺ t (W⊺ projW⊺

QWKWproj) ´¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¸¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¶

Interaction Matrix M ht′

Linear

State

Quadratic Interaction (Tensor Product)

**Figure 6.** Virtual Tensorization. By injecting the linear rational state ht into the Attention mechanism, the dot product QKT implicitly computes quadratic terms of the form h⊺

t Mht′. This effectively simulates a kernel over the tensor product space ht ⊗ht′, enabling the model to capture higher-order dependencies without explicitly materializing the O(d2) state space.

• Depth as Composition (○): Finally, stacking blocks corresponds to the Composition of transductions (or the cascade product), allowing for hierarchical feature extraction where the rational state at layer l depends on the semantic features extracted at layer l −1.

Thus, the architecture provides a complete differentiable substrate for the algebra of rational series.

## 4.5 Circuit Complexity Characterization

We now characterize the computational power of Transductors from the perspective of circuit complexity. This framing provides a rigorous explanation for why Transductors solve the Parity Gap.

Transformers: AC0, TC0, and Robustness. Finite-depth Transformers with hard attention compute Boolean functions within uniform AC0 [Hahn, 2020]. We note that "standard" Transformers using soft attention are strictly more expressive, falling into the complexity class TC0 (Threshold Circuits) [Merrill et al., 2022]. While TC0 models can theoretically express Parity (e.g., via global averaging), they lack the inductive bias to learn these solutions robustly. Recent work identifying C-RASP as a formal model of Transformer length generalization suggests that while tasks like Modulo Counting are in TC0, they are not expressible in the C-RASP fragment, explaining why standard models fail to learn them in a way that generalizes to unseen lengths. In contrast, Rational Transductors structurally implement the exact PNC1 mechanism required.

Theorem 16 (Circuit Upper Bound for Transductors). For fixed model parameters, any function computed by a Rational Transductor lies in PNC1 (and strictly in NC1 under the assumption of finite precision/fields).

Proof. The complexity class PNC1 (Probabilistic NC1) characterizes problems solvable by uniform arithmetic circuits of product-depth O(log T) and polynomial size. The Transductor computation proceeds in two stages:

## 1 Rational State

Computation. The rational feature state ht = Mxt⋯Mx1α involves an iterated product of T matrices. While iterated multiplication of matrices over a finite field (or bounded width branching programs) is in NC1 [Barrington, 1989], the simulation of weighted automata

<!-- Page 24 -->

over rationals or integers is complete for PNC1 [Jung, 1985]. Since the state update is associative, it admits a parallel-prefix tree decomposition of depth O(log T), placing it within PNC1.

## 2 Transformer

Processing. Standard Transformer layers perform aggregation (attention) over T elements. Even under the stronger assumption of soft attention (which places Transformers in TC0), this class is contained within NC1 (using the standard inclusion TC0 ⊆NC1) and thus within PNC1 [Hahn, 2020].

Since PNC1 is closed under composition and contains the Transformer’s complexity class, the total Transductor computation lies in PNC1.

Remark on Tightness. This upper bound is essentially tight from a circuit complexity perspective. The problem of simulating a general WFA (or iterated integer matrix multiplication) is known to be PNC1-complete. Claiming a tighter bound of NC1 for the general case would imply NC1 = PNC1, solving a major open problem in complexity theory. However, if we restrict the model to bounded precision arithmetic or operations over a finite field (effectively treating the WFA as a DFA or NFA), the complexity collapses to NC1 via Barrington’s Theorem. Rational Transductors thus occupy the complexity class PNC1, which sits between NC1 and L (Log-Space), strictly separating them from the AC0 (or TC0) limitations of standard Transformers.

Proposition 17 (Equivalence to Linear Branching Programs). The rational feature head of a Transductor implements a linear branching program whose width equals the state dimension d. Consequently, Rational Transductors can simulate any bounded-width branching program with polynomial length.

Proof. A Linear Branching Program (LBP) of width d is defined by updates vt = A(xt)vt−1. This is structurally identical to the WFA recurrence ht = Mxtht−1. Standard (Boolean) Branching Programs are a subset of LBPs. Since bounded-width permutation branching programs (over a finite alphabet) characterize NC1 (Barrington’s Theorem), and Transductors can learn permutation matrices (as in Theorem 5), this confirms that Transductors possess the expressive power to capture NC1-complete problems.

Theorem 18 (Circuit Lower Bound for Transductors). There exist functions computable by Rational Transductors that are not in AC0.

Proof. By Theorem 5 and Theorem 6, Transductors can uniformly compute Parity and Modular Counting over unbounded input lengths. Since MODk is not computable in AC0 for any k ≥2 [Smolensky, 1987], this establishes that FRT /⊆AC0.

Corollary 19 (Circuit Complexity Sandwich). The class of functions computable by Rational Transductors satisfies the following inclusion hierarchy relative to standard (hard-attention) Transformers:

AC0 ⊊FRT ⊆PNC1.

The Parallelism Gap This hierarchy highlights the computational trade-off characterizing Rational Transductors. While strictly more expressive than standard hard-attention Transformers (AC0), Transductors remain within PNC1, ensuring O(log T) parallelizability. This strictly separates them from general non-linear RNNs (like LSTMs or GRUs with unbounded precision), which are P-complete under sequential updates and cannot be parallelized to logarithmic depth without approximation.

<!-- Page 25 -->

Uniformity Across Lengths. All expressivity results for Transductors are uniform: a single fixed set of parameters suffices to compute the target function for sequences of arbitrary length. No depth or parameter scaling is required. In particular, Transductors correspond to uniform circuit families rather than length-specific (non-uniform) constructions.

On Real-Valued Attention. All circuit complexity claims refer to the standard Boolean abstraction of arithmetic operations with bounded precision, following prior analyses of Transformers in AC0 and NC1.

Why PNC1 Is Essentially Tight. This upper bound is not an artifact of our proof technique but a reflection of the intrinsic hardness of the rational state update. The rational state component corresponds to integer matrix multiplication or weighted automata evaluation, problems known to be complete for PNC1 [Jung, 1985]. Since Transductors do not permit non-associative state updates, they cannot simulate NC2-hard problems such as iterated matrix powering with growing dimension, nor can they solve L-complete problems like graph connectivity (unless PNC1 = L). Thus, the architecture is precisely situated: strictly more expressive than AC0 but bounded by the parallel limits of associative recurrence.

## 5 Theoretical Analysis of Learning

While the architecture of Rational Transductors is linear and convex in parts, its training dynamics in the learnable regime require careful analysis. In this section, we analyze the theoretical properties of the hypothesis class, distinguishing between the universality of random features at initialization and the optimization stability of learned features.

## 5.1 Universality and Efficiency of Random Features

We first address whether a randomly initialized WFA can serve as a generic state encoder. We prove that a sufficiently large random WFA generates a state space rich enough to linearly reconstruct the state of any target WFA up to a finite horizon, justifying our use of near-identity initialization strategies.

Theorem 20 (Universality of Random Rational Features). Let A∗be a target WFA with state dimension d∗generating states h∗ t ∈Rd∗. Let XL be the set of all input sequences of length up to L. Let Arand be a random WFA with state dimension d ≥∣XL∣, initialized such that its transition matrices {Mσ} are drawn from a continuous distribution (e.g., Gaussian). With probability one (assuming generic initialization and no algebraic dependencies), there exists a linear projection matrix W ∈Rd∗×d such that for all sequences x ∈XL, the random feature state ht perfectly recovers the target state:

Wht = h∗ t (23)

Proof. The proof relies on showing that the random WFA maps distinct histories to linearly independent vectors, thereby forming a basis for the target dynamics.

## 1 Matrix Formulation of

Trajectories. Let N = ∣XL∣be the number of distinct prefixes of length ≤L. Let H∗∈Rd∗×N be the matrix collecting the target states h∗ t for all N prefixes as columns. Let H ∈Rd×N be the matrix collecting the random WFA states ht for the same prefixes. Our goal is to find W satisfying WH = H∗. This system of linear equations has an exact solution if and only if the row space of H∗is contained in the row space of H. A sufficient condition is that H has full column rank (rank N).

## 2 Linear Independence of Random

States. The state ht for a sequence x = (x1,..., xt) in the random WFA is given by the product ht = Mxt... Mx1α. This is a polynomial map in the entries of

<!-- Page 26 -->

the matrices {Mσ}. Consider the determinant of any N × N submatrix of H. This determinant is a polynomial function of the random weights. Since we can construct at least one specific instance of WFA parameters where distinct sequences map to linearly independent vectors (e.g., by mapping to distinct basis vectors), this polynomial is not identically zero. A fundamental result in algebra states that if a polynomial is not identically zero, its zero set has measure zero. Since the entries of {Mσ} are drawn from a continuous distribution, the vectors in H are linearly independent with probability 1, provided d ≥N.

## 3 Existence of

Projection. Since H has rank N (full column rank), its Moore-Penrose pseudoinverse H+ = (H⊺H)−1H⊺is a well-defined left inverse (satisfying H+H = I). We construct the projection as:

W = H∗H+. (24)

Verifying the reconstruction:

WH = H∗(H+H) = H∗I = H∗. (25)

Thus, the random features ht contain sufficient information to linearly reconstruct the target states h∗ t exactly.

Approximation Bounds. While Theorem 20 establishes that random rational features can represent any target state space given sufficient width, we must also quantify how the approximation error scales with the dimension d. This is critical for understanding the efficiency of the random initialization. We identify the infinite-width limit of the Rational Transductor as an implicit kernel, which we term the induced rational kernel.

Theorem 21 (Uniform Spectral Approximation Bound). Let M = {Mσ}σ∈Σ be the collection of transition matrices. Let D be a distribution over Rd×d used to initialize each Mσ independently. Consider the kernel K ∶Σ∗× Σ∗→R defined by the expectation over this random initialization:

K(x, x′) = E M∼D[⟨Mxα,Mx′α⟩], (26)

where Mx = Mxt... Mx1. Let f ∗be a target function (the true sequence labeling function we wish to learn) that lies in the Reproducing Kernel Hilbert Space (RKHS) HK with norm ∥f ∗∥K ≤C.

Let fd(x) be the function computed by a Rational Transductor with d random features, where the transition matrices are drawn from D and fixed, and only the linear readout w is trained:

fd(x) = w⊺(Mxα). (27)

Assume the input domain X is restricted to sequences of length at most Tmax equipped with a weighted Hamming (or edit) metric, and the initialization distribution D satisfies the spectral constraint supσ ∥Mσ∥2 ≤ 1 almost surely. For any δ > 0, with probability at least 1 −δ over the random draw of M, the uniform approximation error is bounded by:

sup x∈X

∣f ∗(x) −fd(x)∣≤C √ d

⎛ ⎝

√

2log 1 δ + 4

√ d d −1∆L⎞

⎠, (28)

where ∆is the diameter of the metric space X and L is the Lipschitz constant of the rational feature map x ↦Mxα induced by the spectral bounds.

<!-- Page 27 -->

Remark on the RKHS Assumption (Realizability). The condition ∥f ∗∥K ≤C is formally equivalent to an assumption of realizability. By definition, the RKHS HK consists of all functions that can be expressed as limits of linear combinations of the random rational features defined by the distribution D. Since Theorem 20 establishes that these random features form a universal basis for the state dynamics of any Weighted Finite Automaton (up to a given length), the RKHS effectively covers the entire class of Rational Power Series. Thus, assuming f ∗lies in this space is simply assuming that the ground truth is, in fact, a regular language (or rational series) that the Rational Transductor architecture is capable of representing.

Proof. The proof proceeds by establishing boundedness and continuity of the random features, then applying uniform concentration bounds.

1. Boundedness via contraction. By the stability-aware parameterization (Section 6.2), the transition matrices are spectrally normalized such that ∥Mσ∥2 ≤γ ≤1. Consequently, for any sequence x of length T, the feature vector h(x) = MxT... Mx1α satisfies:

∥h(x)∥2 ≤[

T ∏ t=1

∥Mxt∥2]∥α∥2 ≤γT∥α∥2 ≤∥α∥2. (29)

Thus, the random features ϕ(x) = h(x) are uniformly bounded in Euclidean norm by R = ∥α∥2 independent of sequence length. This ensures that the kernel K(x, x′) is bounded, satisfying the preconditions for Hoeffding-type concentration.

2. Lipschitz continuity. We equip Σ≤Tmax with a weighted Hamming metric under which x ↦Mxα is L-Lipschitz due to spectral contraction. Since the map x ↦Mxα is a composition of contractive linear maps, it is Lipschitz continuous with respect to the initialization parameters. Specifically, a perturbation in the input (interpreted as a perturbation in the effective operator sequence) results in a bounded deviation in the output state h(x), with Lipschitz constant L determined by the spectral bounds of M.

3. Uniform convergence. Let fd(x) = ⟨w, ϕ(x)⟩be the random feature approximation. The error Γ(x) = f ∗(x) −fd(x) is a sum of d independent, bounded random variables.

• Pointwise Bound: For a fixed x, Hoeffding’s inequality gives

P(∣Γ(x)∣> ϵ) ≤2exp(−dϵ2/2C2R2).

• Covering Argument: Let N(ϵ,X) be the ϵ-covering number of the domain. Since Γ(x) is Lipschitz with constant L′ ∝CL, we can approximate the supremum over X by the maximum over the cover centers. Applying the union bound over the cover and optimizing the scale ϵ (via chaining) yields the additional term proportional to

√

∆L.

Combining these yields the stated bound, which holds with high probability over the random initialization.

Interpretation. This result fundamentally reframes the challenge of learning sequential logic. The bound O(C/

√ d) indicates that the approximation error is governed solely by the scale of the random projection d and the complexity of the target function C (in the RKHS sense). This implies a direct resource trade-off: we can avoid the optimization instability of training deep recurrences (the "non-convex hard problem") by simply increasing the width d of the random state (the "linear scaling problem"). Crucially, as d →∞, the random rational features form a universal basis for the class of functions defined by the rational kernel, guaranteeing that a sufficiently wide Rational

<!-- Page 28 -->

Transductor can solve any task representable by stable linear dynamics without ever training the recurrent weights.

Connection to Rational Kernels. The kernel K defined above is a specific instance of a Rational Kernel as defined by Cortes et al. [2004]. Specifically, if the transition matrices are drawn such that E[Mσ ⊗Mσ] is stable, K(x, x′) corresponds to the rational series computed by a weighted automaton on the product monoid. Our Random Rational Features can thus be viewed as an efficient, randomized approximation explicitly designed to scale these classical kernels to deep learning contexts.

Geometry Preservation via Johnson-Lindenstrauss. The O(1/

√ d) scaling in Theorem 21 acts as a functional equivalent to the Johnson-Lindenstrauss (JL) Lemma for sequence histories. Conceptually, the true history of the sequence lives in an infinite-dimensional feature space HK induced by the rational kernel. The random recurrent head acts as a random projection operator P∶HK →Rd. By the JL lemma, pairwise distances (and thus the distinguishability of distinct histories) are preserved with distortion ϵ provided d = Ω(ϵ−2 log N). This explains the "inefficiency" highlighted in Proposition 22: random features rely on generic concentration of measure, whereas learned features exploit the specific algebraic structure of the task.

The Compactness Gap. While Theorem 20 shows representational completeness, it relies on an exponentially large state dimension d ≈∣Σ∣L. In contrast, learning the transitions allows for compact representations. We quantify this gap below.

Proposition 22 (Compactness Gap). Let the target language be the set of strings with an even number of 1s (Parity).

• Learned Regime: A Rational Transductor can solve this perfectly with state dimension d = 2 by learning the exact flip transition M1 = (0 1 1 0).

• Random Regime: To solve this with fixed random features and a linear readout with error ϵ < 1/2, the required dimension scales as d = Ω(1/ϵ2) (by Theorem 21). (This lower bound holds for any isotropic initialization distribution.)

Proof. Part 1: Learned Features (Exact Construction). We explicitly construct a WFA with d = 2 that computes parity. Let the state space basis correspond to states {Even,Odd}. Initialize h0 = (1,0)⊺. Define the transition matrices for input bits 0 and 1 as:

M0 = (1 0 0 1) = I, M1 = (0 1 1 0) = σx. (30)

For any sequence x, the state hT = MxT... Mx1h0 will be (1,0)⊺if the number of ones is even, and (0,1)⊺if odd. A linear readout y = w⊺hT with w = (−1,1)⊺yields y = −1 (Even) or y = 1 (Odd). The separation is perfect (margin = 2), so the error is zero with d = 2.

Part 2: Random Features (Statistical Lower Bound). In the Random Regime, the function approximation fd(x) is a sum of d i.i.d. random features. By the Central Limit Theorem, the variance of the estimator scales as Var(fd(x)) ∝1 d. To correctly classify parity for all inputs with high probability, the approximation error (noise) must be strictly less than the classification margin (signal). From Theorem 21 (see above), the worst-case error scales as O(1/

√ d). Specifically, to ensure ∣f ∗(x) −fd(x)∣< ϵ uniformly, we require the standard deviation σd ≈ 1 √ d to be suppressed below ϵ. Rearranging 1 √ d ≤ϵ yields d ≥1 ϵ2. Thus, achieving a fixed error tolerance ϵ requires the

<!-- Page 29 -->

dimension to scale quadratically with the inverse error, whereas the learned solution achieves zero error with constant dimension.

This gap motivates our focus on the Learned Regime for practical applications, using the random regime results primarily to justify near-identity initialization.

Corollary 23 (Convex Learnability of Rational Projections). Let L(⋅,⋅) be a convex loss function (e.g., squared error or cross-entropy). Consider a Rational Transductor where the WFA transitions M are fixed and the downstream Transformer parameters θ are fixed (or constitute a linear readout). The optimization problem for the projection matrix W min

W ∑ (x,y)∈D

L(y, Gθ(x) + WhT(x)). (31)

is a convex optimization problem.

Proof. Since the WFA transitions are fixed, the feature vector hT(x) is a constant vector for any given input x. The term WhT(x) is linear in the variable W. Consequently, the model output̂ y = Gθ(x) + WhT(x) is an affine function of W. A fundamental property of convex optimization is that the composition of a convex function with an affine mapping preserves convexity. Therefore, the objective function, being a sum of convex functions composed with affine maps, is convex with respect to W. This guarantees that gradient descent will converge to a global optimum.

## 5.2 Optimization Dynamics

In the learned regime, we must ensure that the optimization landscape is well-behaved. We provide three key theorems guaranteeing optimization stability and well-conditioned gradient flow.

Theorem 24 (Gradient Norm Preservation). Consider the gradient of the loss L with respect to the hidden state ht, denoted δt = ∇htL. In the backward pass, the error signal propagates as δt−1 = M⊺ xtδt + vt−1. (32)

## 1 Explosion Guarantee:

If the transitions satisfy the spectral constraint ∥Mσ∥2 ≤γ ≤1, then the propagated gradient norm is strictly bounded: ∥δt−k∥2 ≤γk∥δt∥2 + C, preventing exponential explosion.

## 2 Vanishing Guarantee:

If the transitions are parameterized to be orthogonal (M⊺ σMσ = I), then the gradient norm is exactly preserved in the absence of injection: ∥δt−k∥2 = ∥δt∥2.

Proof. This follows directly from the properties of the spectral norm under matrix multiplication. For (1), ∥δt−1∥≤∥M⊺ xt∥∥δt∥+ ∥v∥≤γ∥δt∥+ ∥v∥. By induction, the homogeneous component decays (or stays constant) while the additive injection terms accumulate linearly, preventing exponential growth. For (2), if Mxt is orthogonal, ∥M⊺ xtδt∥2 = ∥δt∥2, ensuring the error signal from time t reaches time 0 without attenuation. This effectively solves the "long-term dependency" problem for the linear component.

This result establishes a structural immunity to the gradient explosion problem. Unlike standard RNNs, which often undergo chaotic gradient growth and require heuristic fixes like clipping, Rational Transductors are mathematically guaranteed to remain stable. By strictly bounding the spectral radius γ ≤1, the architecture ensures that error signals never expand exponentially, regardless of sequence length.

<!-- Page 30 -->

Theorem 25 (Gradient Maintenance via Deep Injection). Consider the backward recurrence for the Rational Transductor error signal (Eq. 32): δt−1 = M⊺δt + vt−1. Let the transition matrix be contractive with ∥M∥2 ≤γ < 1. Let v(l)

t−1 = ∇ht−1L(l) denote the gradient contribution from the injection at layer l. The gradient norm at step t −k is bounded below by the immediate injection terms:

∥δt−k∥2 ≥

XXXXXXXXXXXX k−1 ∑ j=0

(M⊺)jvt−1−j

XXXXXXXXXXXX2

−γk∥δt∥2 (33)

Proof. Unrolling the recurrence δt−1 = M⊺δt + vt−1 for k steps yields:

δt−k = (M⊺)kδt + k−1 ∑ j=0

(M⊺)k−1−jvt−1−j, (34)

where (M⊺)k denotes the ordered product of transition matrices. Applying the reverse triangle inequality (∥a + b∥≥∥b∥−∥a∥) and the sub-multiplicative property of the spectral norm (∥(M⊺)kδt∥≤γk∥δt∥), we obtain the lower bound:

∥δt−k∥2 ≥

XXXXXXXXXXXX k−1 ∑ j=0

(M⊺)k−1−jvt−1−j

XXXXXXXXXXXX2

−γk∥δt∥2. (35)

The first term represents the accumulated gradient injections from the deep Transformer layers. Even if the temporal connection vanishes (i.e., the second term γk∥δt∥→0 as k →∞), the state ht−k retains the magnitude of the direct gradient signal v, preventing total gradient collapse.

Crucially, this theorem demonstrates how Deep Rational Injection mitigates the vanishing gradient problem. In traditional recurrences, gradients depend entirely on backpropagation through time and often decay to zero. Here, the injection mechanism creates gradient highways that provide direct supervision from the local Transformer layers to the recurrent state. This allows the model to learn representations for recent events even if long-term dependencies are temporarily weak.

Theorem 26 (Bounded Hessian and Smoothness). Let L(M) be the loss with respect to the transition matrix M, assuming a contractive spectral constraint ∥M∥2 ≤γ < 1 and a Lipschitz-smooth downstream Transformer (e.g., with LayerNorm and bounded activation derivatives). Then, the loss function is β-smooth with respect to M. That is, the spectral norm of the Hessian is uniformly bounded independent of sequence length:

∥∇2

ML∥2 ≤β(γ, C) < +∞. (36)

Proof. The hidden state ht is a polynomial in M of degree t. The second derivative ∂2ht

∂M2 involves terms of the form ∑i,j Mi(∂M)Mj(∂M)Mt−i−j−2. For a standard RNN without constraints, these terms sum to a magnitude scaling with t2∥M∥t−2, which explodes if ∥M∥> 1. However, under the strict contraction constraint ∥M∥≤γ < 1, the series of second derivative terms converges geometrically. Specifically, the sum is bounded by the second derivative of the geometric series (1 −γ)−1, which is 2(1 −γ)−3. Since the Hessian of the composition L(ht(M)) depends on ∇ht and ∇2ht (both bounded by geometric series) and the smooth Transformer readout, the total Hessian is uniformly bounded.

Practically, the boundedness of the Hessian ensures a well-conditioned optimization landscape. This implies that the loss surface is free of pathological curvature or sharp cliffs, allowing standard first-order optimizers (like AdamW) to navigate the parameter space efficiently without requiring complex second-order corrections.

<!-- Page 31 -->

## 5.3 Generalization and Robustness

We now examine the model’s ability to generalize to unseen lengths and withstand adversarial perturbations.

Theorem 27 (Time-Invariant Error Bounding). Let M∗be the true transition logic of the target task (e.g., a counter or automaton) and let̂ M be the learned transition matrix. Assume the learned dynamics are contractive with spectral norm ∥̂M∥2 ≤γ < 1. If the learned matrix approximates the true logic with error ∥̂M −M∗∥≤ϵ, then the deviation between the true state h∗ t and the Rational Transductor statẽ ht is uniformly bounded for all t > 0:

sup t≥1

∥h∗ t −̃ ht∥≤ ϵC 1 −γ, (37)

where C = supt ∥h∗ t−1∥is the bound on the true state magnitude.

Proof. Let et = h∗ t −̂ ht be the state error at time t. The evolution of the error is given by:

et = M∗h∗ t−1 −̂ M̃ht−1 (38)

= M∗h∗ t−1 −(M∗+ ∆)(h∗ t−1 −et−1) where ∆=̂ M −M∗ (39)

=̂ Met−1 −∆h∗ t−1. (40)

Taking norms and applying the triangle inequality:

∥et∥≤∥̂M∥∥et−1∥+ ∥∆∥∥h∗ t−1∥≤γ∥et−1∥+ ϵC. (41)

This is a linear recurrence inequality. Solving for the steady state (limit as t →∞) yields the geometric series sum:

∥et∥≤ϵC t−1 ∑ k=0 γk ≤ ϵC 1 −γ. (42)

This completes the proof.

Remark: The Unitary Regime (γ = 1). Theorem 27 establishes a constant error bound by leveraging a contraction coefficient γ < 1, which is characteristic of the "fading memory" regime required for stable approximate matching. However, for tasks like Parity or Modular Counting that require infinite memory (γ = 1), the right-hand side of Equation 37 diverges. In this unitary regime, the length-independent bound strictly applies only to the ideal algebraic case where precision error ϵ = 0. While finite-precision noise may theoretically lead to linear error accumulation over time (∑t−1 k=0 1k = t), generalization is instead guaranteed by the algebraic exactness of the orthogonal parameterization (Theorem 6). Since the transition matrices Mσ form a subgroup isomorphic to the target automaton, the state evolution remains exactly on the solution manifold regardless of sequence length T, provided the hardware precision is sufficient to distinguish the discrete states of the group.

Implication: Learned Positional Encodings. This result provides the theoretical justification for disabling explicit Positional Encodings (PEs) in algorithmic tasks. Standard PEs (RoPE, sinusoidal) are brittle because they introduce out-of-distribution drift when test sequences exceed training lengths (Ltest > Ltrain). By relying solely on the recurrent state update, Rational Transductor learn a time-invariant transition rule. Theorem 27 guarantees that the error of this rule does not compound over time but remains bounded by a constant, unlocking the perfect length generalization observed experiments (Section 7.2).

<!-- Page 32 -->

Theorem 28 (Length-Independent Generalization). Let FRT be the class of Rational Feature functions f(x) = w⊺(MxT... Mx1α) parametrized by transition matrices satisfying the spectral constraint ∥Mσ∥2 ≤ γ < 1 and bounded readout ∥w∥2 ≤W. For a dataset S of N sequences of length T, the Empirical Rademacher Complexity is bounded by:̂

RS(FRT) ≤W∥α∥2 √

N

(1 1 −γ). (43)

Proof. The output of the Transductor head at time T can be written recursively. Since the transition dynamics are linear and contractive, the sensitivity of the output hT to the input token at position t decays exponentially as γT−t. Following standard stability analysis for recurrent systems [Miller and Hardt, 2018], the Lipschitz constant of the map x →hT with respect to the sequence (in the ℓ2 sense) is bounded by the geometric series ∑T k=0 γk < 1 1−γ. By Talagrand’s contraction lemma [Ledoux and Talagrand, 1991], the complexity of the class is bounded by the product of this Lipschitz constant and the complexity of the input embedding layer (which is O(1/

√

N)). Crucially, because the geometric series converges, the bound is independent of T.

Interpretation: Infinite-Horizon Reliability. Standard generalization bounds for RNNs typically scale with the sequence length (e.g., O(T/

√

N) or O(

√

T/N)), implying that model performance degrades on longer tasks. Theorem 28 establishes that for contractive Rational Transductors, the complexity—and thus the generalization gap—is independent of sequence length T. This theoretically guarantees that the model can be deployed on streaming data of indefinite duration without the risk of overfitting to the specific length statistics of the training set.

Theorem 29 (Hankel-Rademacher Complexity [Balle and Mohri, 2017]). Let FHankel,r be the class of rational functions f ∶Σ∗→R with Hankel nuclear norm ∥Hf ∥S1 ≤r. Let S = (x1,..., xN) be a sample of sequences and let Lmax = maxx∈S ∣x∣be the maximum sequence length. Define the max-prefix collision term σ2

S = supu∈Σ∗∑N i=1 I[u ∈pref(xi)]. The Empirical Rademacher complexity is bounded by:̂

RS(FHankel,r) ≤r

N (

√

2σ2 S log(2DS) + 2

3 log(2DS)) =̃ O(r √

N

), (44)

where DS is the total number of distinct suffixes present in the sample S (the size of the suffix trie), which is bounded by NLmax.

Proof. This result is a direct application of Theorem 6 from Balle and Mohri [2017]. The proof relies on two key steps:

1. Fliess’ Theorem Duality: The condition ∥Hf ∥S1 ≤r on the Hankel matrix is dual to the spectral norm bound on the data matrix Y (defined over the prefix/suffix splits of the sample S).

## 2 Matrix Concentration: The expected spectral norm of the data matrix is bounded using the Matrix

Bernstein inequality (specifically, a non-commutative Khintchine inequality). The variance term in this inequality corresponds exactly to the maximum number of times any specific prefix u appears across the dataset sequences xi, denoted by σ2

S.

For a detailed derivation of the constants 2/3 and the logarithmic factor, we refer the reader to the original proof in Balle and Mohri [2017].

<!-- Page 33 -->

Significance: Low-Rank Regularization. This result is profound because the rank of the Hankel matrix corresponds exactly to the minimal state dimension dmin of the Weighted Finite Automaton (Fliess’ Theorem). Consequently, penalizing the nuclear norm of the Hankel matrix (which our "Diagonal + Low Rank" parameterization effectively does) is rigorously equivalent to regularizing the state dimension of the underlying latent automaton. This confirms that Rational Transductors generalize by learning low-rank algebraic structures, distinguishing them from standard Transformers which often overfit to high-rank, spurious correlations.

Theorem 30 (Lipschitz Input Stability). Let x = (x1,..., xT) be a sequence of continuous input embeddings where xt ∈Rdin. Let fRT(x) be the output of the rational head. Assume the transition dynamics are contractive (∥M(x)∥2 ≤γ < 1) and the encoding of inputs into matrices is Lipschitz continuous with constant KM (i.e., ∥M(x) −M(x′)∥≤KM∥x −x′∥). Then, the map from the input sequence x to the final state hT is Lipschitz continuous with constant:

Lseq ≤KM∥α∥

1 −γ (45)

This bound is independent of the sequence length T.

Proof. Let x = (x1,..., xT) and x′ = (x′

1,..., x′ T) be two input sequences differing at time step t. Let hk and h′ k be the respective state sequences. The state deviation ek = hk −h′ k evolves as:

ek = M(xk)ek−1 + (M(xk) −M(x′ k))h′ k−1 (46)

Taking norms:

∥ek∥≤γ∥ek−1∥+ KM∥xk −x′ k∥R, (47)

where R = sup∥h′ k∥is the bounded state norm. Iterating this recurrence, the total deviation at time T due to a perturbation at time t is bounded by KMRγT−t∥xt −x′ t∥. Summing over all possible perturbation times t (triangle inequality for the whole sequence norm):

∥hT −h′

T∥≤

T ∑ t=1

KMRγT−t∥xt −x′ t∥≤(KMR

∞ ∑ k=0 γk)sup t

∥xt −x′ t∥. (48)

The geometric series converges to (1 −γ)−1, yielding the length-independent bound.

Interpretation: Robustness to Embedding Noise. This theorem guarantees that Rational Transductors are robust to small perturbations in the input embeddings, such as those caused by quantization, noise, or minor distribution shifts. The state hT varies smoothly with the input sequence x, with a Lipschitz constant that does not explode with T. This contrasts with chaotic systems where a small change in initial conditions or inputs can lead to exponentially diverging states over time.

## 6 Concrete Training Recipe

While the theoretical properties guarantee expressivity and stability, practical success relies on an efficient implementation. We detail the three pillars of our training recipe: parallel gradient computation, spectral normalization, and near-identity initialization.

<!-- Page 34 -->

## 6.1 Efficient Parallel Backpropagation

Standard Backpropagation Through Time (BPTT) imposes a sequential dependency O(T). We avoid this sequential dependency by exploiting the strict linearity of the rational update ht = Mxtht−1.

Forward Pass. The sequence of hidden states h1∶T is computed via a parallel associative scan (prefix sum) over the matrix monoid, reducing the parallel depth of the computation from T to O(log T).

Backward Pass. Crucially, the gradient computation is also parallelizable. As derived in Section 5.2, the adjoint variables δt = ∇htL satisfy the affine recurrence δt−1 = M⊺ xtδt + vt−1. By lifting this to homogeneous coordinates, we compute the same gradients as sequential BPTT using a reverse parallel scan. We define the augmented adjoint vector̂ δt ∈Rd+1 and the backward transition matrix Bt ∈R(d+1)×(d+1) as:̂ δt = (δt

1), Bt = (M⊺ xt vt−1 0⊺ 1). (49)

The recurrence then becomes a homogeneous matrix product̂ δt−1 = Bt̂δt, which is computable in O(log T) depth.

Implementation Details. We leverage hardware-aware fused kernels (e.g., in CUDA or Triton) to ensure that the wall-clock time of the rational head is negligible. While the Unified Scaled Cayley Parameterization requires a matrix inversion (I −At)−1 at every token step, we mitigate the O(Td3) pre-processing overhead by leveraging high-performance linear solvers within the fused kernel. For the small state dimensions used in this work (d ≤32), these inversions are executed entirely in high-bandwidth SRAM, bypassing the need to materialize the full T × d × d transition tensor and keeping memory complexity linear in T. Furthermore, although structured updates like DPLR allow for O(dr) unrolling during inference, we explicitly note that the parallel associative scan requires dense matrix multiplication; however, this O(d3) training cost remains negligible compared to the quadratic complexity of the self-attention mechanism.

## 6.2 Spectral Control: The Unified Scaled Cayley Parameterization

While Section 2.3 defines the broad family of admissible transition matrices, successful training requires a specific parameterization that controls the spectral radius ρ(M) to prevent gradient explosion. Depending on the matrix family, we use either intrinsic or explicit control.

## 1 Intrinsic Stability (The Scaled Cayley

Recurrence). For the algorithmic experiments, we use a Unified Scaled Cayley Parameterization that structurally guarantees stability without auxiliary normalization. We define the transition matrix as:

Mt = gt ⋅C(At) = gt ⋅(I + At)(I −At)−1, (50)

where At is skew-symmetric and gt ∈R is a scalar gain. The parameters At and gt are obtained via a linear projection of the input embedding xt, allowing Mt to be cached. Since the Cayley transform C(At) maps to SO(d), it is orthogonal by construction (∥⋅∥2 = 1). Thus, the spectral radius is determined solely by gt:

<!-- Page 35 -->

• Conservation (gt = 1): We fix gt = 1 for tasks like Modulo Counting, enabling infinite horizon tracking.

• Decay (gt < 1): We learn gt = σ(θt) ∈(0,1) (where θt is a learnable scalar) for fading memory tasks. The model can emulate the gating mechanisms of LSTMs or SSMs, attenuating past information to focus on recent context.

## 2 Explicit Spectral Normalization (General

Case). For unstructured or linearly parameterized families (e.g., DPLR, Butterfly, or Random Features) where the norm is not structurally bounded, we must enforce contractivity explicitly during the forward pass. For any learnable matrix component W, we apply:

Weffective = W max(1,∥W∥2/γ), (51)

where γ ∈(0,1] is a hyperparameter bounding the spectral radius. This formulation ensures that weights are only projected when they exceed the contractive threshold γ, preventing unnecessary geometric suppression of stable parameters.

• Fading Memory (γ < 1): We typically set γ ≈0.99 for general structured heads to ensure stable gradient propagation while allowing forgetting. This bound is essential for the theoretical guarantees in Section 5.1.

Remark on Topology. We note that the Cayley transform generates matrices with determinant +1 (rotations), which excludes reflections (determinant −1). While Eq. 50 could be augmented with a sign flip (gt < 0), we find empirically that using a state dimension d ≥3 allows the model to embed reflections as rotations in a higher-dimensional space, resolving the topological obstruction without special casing.

## 6.3 Near-Identity Initialization

To stabilize training, we initialize the rational head to act as a near-perfect integrator. Regardless of the chosen structure, we initialize parameters such that Mσ ≈I. Specifically:

• The diagonal term Dσ is initialized to 1 (or sampled from U[1 −ϵ,1]).

• The low-rank perturbation terms Uσ,Vσ are initialized independently from N(0, ν2) such that their product has variance ν2 ≈0.

This ensures that at step 0, the model acts as a near-perfect integrator over long horizons. The optimizer then gradually learns to “forget” irrelevant information by deviating from the identity, rather than struggling to learn “remembering” from a chaotic initialization.

## 7 Empirical Validation

We validate our theoretical findings on synthetic tasks designed to probe the limitations of attention.

Specifically, we investigate two key claims: (1) whether Rational Transductors can solve NC1complete tasks that are theoretically impossible for standard Transformers (the "Regular Gap"), and (2) whether the learned solutions generalize to unseen lengths (Time-Invariance).

For complete experimental details, including hyperparameters, optimization settings, and statistical reproducibility reports, refer to Appendix B.

<!-- Page 36 -->

## 7.1 The Regular Gap: Modulo Counting

Task Setup. We evaluated models on the Modulo-5 Counting task, which requires tracking the cumulative number of 1s in a binary sequence modulo 5. As established in Theorem 5 and Theorem 6, this task generally requires PNC1 complexity for uniform solvability. While softattention Transformers (TC0) can theoretically approximate the solution for fixed lengths, they lack the inductive bias to learn the cyclic state transition robustly. We empirically test whether models can bridge this gap.

## Model

Configuration. We compared the Rational Transductor against a standard Transformer. To ensure a fair comparison, both models were matched in parameter count (≈25k parameters).

• Transformer: 2 layers, dmodel = 32, 4 heads, using learned positional encodings.

• Rational Transductor: 2 layers, dmodel = 32. Following the recipe in Section 6.2, we used a single rational head (drat = 8) initialized in the Strictly Orthogonal Regime (Cayley parameterization). This enforces exact state conservation (γ = 1) and restricts the eigenvalues to the unit circle. Crucially, we disabled standard positional encodings, forcing the model to rely solely on the rational state for sequence tracking.

Remark on State Space Models (SSMs). We deliberately compare against Standard Transformers and LSTMs to highlight the specific contribution of linear recurrence vs. attention or non-linear gating. We note that recent State Space Models like Mamba [Gu and Dao, 2023] also rely on time-varying linear recurrences. Theoretically, our expressivity results (Theorem 16) imply that architectures like Mamba should also be capable of solving these PNC1 tasks, provided they are initialized to support unitary dynamics. Our Rational Transductor acts as a minimal theoretical proxy for this broader class of Linear RNNs, allowing us to isolate the specific automata-theoretic mechanisms (e.g., the necessity of orthogonal vs. stochastic transitions) without the confounding variables of Mamba’s complex gating and block design.

50 100 300 500 Sequence Length

0.0

0.2

0.4

0.6

0.8

1.0

Accuracy

Random Chance (20%) Standard Transformer Rational Transductor (Ours)

**Figure 7.** The Regular Gap (Modulo-5 Counting). The models are trained on short sequences (L = 50) and evaluated on longer lengths up to L = 500. The Standard Transformer (red) achieves high accuracy on the training distribution but fails to generalize, collapsing to near-random chance (20%) as length increases. The Rational Transductor (blue), leveraging the strictly orthogonal parameterization, learns the exact underlying automaton and maintains 100% accuracy across all tested lengths. Results are averaged over 5 random seeds; standard deviations are negligible (< 0.01%) and omitted for clarity (see Appendix B).

<!-- Page 37 -->

Results. Figure 7 illustrates the performance. The Standard Transformer fails to learn a robust counting mechanism, achieving only partial success on training lengths (L = 50) and collapsing to random chance (20%) on longer sequences. In contrast, the Rational Transductor converges to 100% accuracy almost immediately. This confirms that the Rational Head successfully learns the underlying group-theoretic operation (cyclic permutation), validating the expressivity claims of Theorem 6.

## 7.2 Length Generalization and Time-Invariance

Task Setup. Beyond expressivity, we tested for Length Generalization. Models are trained solely on short sequences (Ltrain = 40) but evaluated on sequences up to Ltest = 1000 (25× the training horizon). We use the Modulo-5 Counting task from the previous section as the testbed.

## Model

Configuration. We used the same architecture depths as in the previous experiment (2 layers, dmodel = 32):

• Transformer: 2 layers, 4 heads. We deliberately use standard Learned Absolute Positional Encodings to establish a baseline for the fundamental limits of the canonical Transformer architecture [Vaswani et al., 2017]. While relative encoding schemes like RoPE can technically extrapolate, they remain constrained to tracking input-independent relative positions. Our results demonstrate that Rational Transductors solve length generalization by learning input-dependent semantic state transitions, a capability that absolute and standard relative positional heuristics lack. Thus, a Transformer + RoPE is theoretically subsumed by the Rational Transductor framework.

• Rational Transductor: 2 layers, 4 heads, initialized in the Strictly Orthogonal Regime (Cayley). We disabled positional encodings entirely, resulting in a much smaller model (≈26k parame- ters) that must rely entirely on its recurrent state ht = Mht−1 to track the sequence, enforcing a shift-invariant solution by design.

40 100 500 1K Sequence Length

0.00

0.25

0.50

0.75

1.00

Accuracy

Train Horizon (L = 40)

Random Chance (20%) Standard Transformer Rational Transductor

**Figure 8.** Length Generalization. Models were trained only on sequences of length L = 40 (vertical dashed line) and evaluated on lengths up to L = 1000. The Standard Transformer (red) overfits to the training positions; its accuracy collapses to random chance (≈20%) on longer sequences. The Rational Transductor (blue) generalizes almost perfectly, maintaining 99% accuracy even at 25× the training length. This validates the algebraic exactness guarantee (Theorem 6). Shaded regions (invisible at this scale) denote standard deviation across 5 runs.

Results. As shown in Figure 8, the Standard Transformer suffers from catastrophic positional drift. Once the sequence length exceeds the training horizon (L = 40), the learned positional encodings are

<!-- Page 38 -->

no longer valid, and performance drops to random guessing. The Rational Transductor, however, maintains perfect accuracy (> 99%) up to L = 1000. This confirms that the model has learned an algebraically exact solution (as in Theorem 6) rather than an approximate one, consistent with the unitary parameterization (γ = 1). By disabling explicit positional encodings and relying on the recurrent state dynamics, the model is forced to learn a transition rule that is valid for any time step t. This demonstrates that Rational Transductors can serve as robust, algorithmic co-processors that do not suffer from the length-generalization brittleness of standard attention.

## 7.3 Computational Efficiency and Extreme Scaling

A core theoretical advantage of the Rational Transductor is its parallelizability. Unlike standard RNNs, which require sequential processing (O(T) latency2), and Transformers, which scale quadratically in memory or compute (O(T2)), Rational Transductors can be parallelized via an associative scan, achieving logarithmic time complexity (O(log T)) on parallel hardware.

Experimental Setup. To validate this scaling behavior, we benchmarked the inference latency (forward pass) of the sequence mixing layers in isolation (Rational Head vs. Self-Attention). This strictly isolates the algorithmic complexity of the recurrence (O(log T)) versus the attention mechanism (O(T2)), independent of the shared feed-forward blocks. We benchmarked the inference latency (forward pass) of the models on sequences of increasing length, ranging from T = 128 to T = 32,768. We used a batch size of B = 1 to strictly isolate the sequential throughput limitations of the architectures. All measurements were conducted on a single NVIDIA GPU (A100), averaged over 20–100 trials after a warm-up period.

## Model

Configuration. We implemented minimal, optimized kernels for each architecture to ensure a fair algorithmic comparison:

• Sequential RNN: A standard linear recurrence (ht = Mtht−1) implemented via a sequential loop. Matrix dimension d = 16.

• Transformer: Standard Self-Attention, using scaled_dot_product_attention (FlashAttention), PyTorch’s optimized implementation to represent the state-of-the-art baseline. Heads=4, dhead = 16.

• Rational Transductor: Our model, implemented using a Parallel Associative Scan algorithm (specifically a log-depth Kogge-Stone style scan). This allows the model to compute the cumulative matrix products for all time steps simultaneously. Matrix dimension d = 16.

2We note that recent methods like ParaRNN [Danieli et al., 2025] enable quasi-parallel training of non-linear RNNs via iterative linearization (Newton’s method), achieving theoretical O(k log T) depth. However, this approach requires multiple forward scans per update step. We benchmark against the standard exact sequential implementation used in most production baselines.

<!-- Page 39 -->

128 512 2K 8K 32K Sequence Length (T)

10 1

100

101

102

Latency (ms)

Sequential RNN Rational Transductor Standard Attention

**Figure 9.** Latency vs. Sequence Length. Wall-clock inference latency (ms) on a log-log scale. The Sequential RNN (red) scales linearly (O(T)), becoming prohibitively slow for long sequences. The Transformer (green) exhibits quadratic scaling (O(T2)), eventually running out of memory. The Rational Transductor (blue) leverages parallel associative scans to achieve sub-linear scaling, outperforming the RNN on sequences longer than T = 512 and maintaining high throughput even at T = 32k.

Results. Figure 9 plots the latency on a log-log scale. The Sequential RNN exhibits strict linear scaling O(T); while efficient for short sequences, it becomes the bottleneck at extreme lengths. The Transformer scales efficiently for short lengths due to FlashAttention but hits a quadratic wall, exploding in latency at extreme lengths. The Rational Transductor combines the best of both worlds: for short sequences, it is competitive with the Transformer; for long sequences (T > 512), the parallel scan allows it to overtake the Sequential RNN. We note that while wall-clock scaling on fixed-density GPUs eventually reflects hardware occupancy limits at very large T, the sublinear crossover points remain distinct. This empirically confirms the theoretical O(log T) parallel complexity established in Section 2.

## 7.4 Algorithmic Generalization: Long-Integer Addition

Task Setup. To test the model’s ability to learn discrete, discontinuous logic (in contrast to the smooth group operations of counting), we evaluated it on Long-Integer Addition. The task is to add two L-digit numbers digit-by-digit. This requires implementing a “Full Adder” state machine, where the carry bit must be:

• Generated (State →1) if the sum > 9.

• Propagated (State →State) if the sum = 9.

• Killed (State →0) if the sum < 9.

Models are trained on short numbers (L ∈[10,40]) and evaluated on lengths up to L = 1000.

## Model

Configuration. We compare the Rational Transductor against a standard Transformer. Both models share a backbone size of 2 layers with dmodel = 32 and 4 heads:

• Transformer: Used standard learned positional encodings with a capacity of 5000 positions.

<!-- Page 40 -->

• Rational Transductor: Following the recipe for discrete logic, we used the Universal Rational Transductor configuration, effectively routing to the Stochastic component (drat = 4). The transition matrices are parameterized as column-stochastic matrices (via softmax) to strictly preserve the l1-norm of the state, enforcing a probabilistic automaton structure ideal for switching logic. Crucially, we disable positional encodings, forcing the model to rely solely on the rational state to track the carry bit.

20 100 500 Number Length (Digits)

0.0

0.2

0.4

0.6

0.8

1.0

Sequence Accuracy

Standard Transformer Universal Rational Transductor

**Figure 10.** Experiment D: Long-Integer Addition. Sequence-level accuracy (exact match of the entire sum). The Standard Transformer (red) fits the training distribution (L = 20) but fails completely on longer sequences (0% at L = 100), unable to propagate carry bits over long distances. The Universal Rational Transductor (blue), leveraging a Stochastic head, learns the exact finite state automaton for addition. It generalizes perfectly to L = 1000 digits, demonstrating that the architecture can autonomously learn the correct switching logic for the task.

Results. Figure 10 shows the sequence-level accuracy. The Standard Transformer fails to generalize, dropping to 0% accuracy immediately outside the training window. Attention mechanisms struggle to maintain the hard sequential dependency of a carry bit over hundreds of steps when trained only on short sequences. In contrast, the Universal Rational Transductor achieves 100% accuracy across all lengths up to L = 1000. This confirms that by providing a diverse set of dynamic kernels (here, a Stochastic head), the model can autonomously learn and execute complex algorithmic rules that require both infinite memory conservation and discrete state switching.

## 7.5 Quantitative Generalization and Precision

While the previous examples (Parity, Addition) demonstrated the ability to track discrete states, they did not test the capacity for quantitative accumulation over unbounded domains. As established in [Cortes and Mohri, 2000], weighted automata can represent functions mapping sequences to numerical values (e.g., polynomial evaluation).

We consider the task of Base-2 Integer Evaluation. The model must map a binary string x ∈{0,1}L to its integer value f(x) = ∑L t=1 xt ⋅2L−t. This requires the hidden state to grow exponentially with sequence length (vt = 2vt−1 + xt), serving as a stress test for the “Linearity vs. Saturation” hypothesis.

Experimental Setup. We trained models on sequences of length L = 64. To strictly isolate architectural limitations from hardware precision limits, all operations were performed in Double

<!-- Page 41 -->

Precision (Float64). To fit within the dynamic range of double precision floating point arithmetic, target integer values were normalized to the unit interval [0,1] via scaling by 2−L. We note that for sequence lengths L > 53, the integer values 2L exceed the 53-bit significand precision of IEEE 754 Double Precision (Float64). The reported "machine precision" MSE in Figure 11 reflects the achieved numerical precision of the model under double-precision arithmetic. We compared the Rational Transductor against a Transformer and an LSTM:

• Rational Transductor: We used a general Affine WFA parameterization (1 layer, d = 12). Unlike the structured heads in Section 7.4, here the model learns unconstrained transition matrices A0, A1 ∈Rd×d and bias vectors b0, b1 ∈Rd from scratch, implementing the update ht = Axtht−1 + bxt. Initialization is set near identity to facilitate gradient flow. While a specialized scaling head could also solve this task, we used general matrices to demonstrate that the architecture can discover expansive dynamics (∣λ∣> 1) without explicit engineering.

• Transformer: 3 layers, dmodel = 32, 4 heads, relative positional encoding.

• LSTM: 1 layer, hidden dimension d = 32.

Despite the Transductor being significantly smaller in parameters (< 1k vs ≈12k), it is the only model theoretically capable of unbounded linear growth.

LSTM Transformer Rational Transductor

10 10

10 8

10 6

10 4

10 2

100

Mean Squared Error (Log Scale)

8.4e-02 8.4e-02

5.9e-09

Quantitative Precision (Seq Length 64)

Random Guessing

**Figure 11.** Quantitative Precision (Base-2 Evaluation). We trained models to compute the integer value of binary strings of length L = 64 using double precision. Standard architectures (LSTM, Transformer) fail completely (MSE ≈8.4 × 10−2), collapsing to the random-guessing baseline. The Rational Transductor learns the exact affine recurrence, achieving near-perfect precision (MSE ≈ 5.9 × 10−9).

Results. As shown in Figure 11, this task reveals a sharp expressivity gap. Both the LSTM and Transformer fail completely, converging to the variance of the dataset (MSE ≈8.4 × 10−2). For the LSTM, the gradient signal vanishes through 64 layers of saturating non-linearities (tanh); for the Transformer, the attention mechanism cannot resolve positional weights spanning 19 orders of magnitude (264 ≈1.8 × 1019) amidst softmax noise.

In contrast, the Rational Transductor exploits its linear recurrence to propagate gradients without attenuation, learning the exact Horner scheme to high numerical precision (MSE ≈5.9 × 10−9). We attribute this error floor primarily to optimization convergence limits and accumulated algorithmic round-off noise rather than the theoretical mantissa limits of the IEEE 754 Float64 standard.

<!-- Page 42 -->

## 8 Conclusion

We introduced the Rational Transductor, a hybrid architecture that bridges the gap between the semantic flexibility of Transformers and the rigid, state-dependent logic of formal languages. By augmenting self-attention with a linear, matrix-valued recurrence, we have showed that it is possible to break the expressivity and learnability barriers that constrain standard Transformers.

Our theoretical analysis aligns this approach with the Krohn-Rhodes decomposition, demonstrating that Transductors can structurally represent the full hierarchy of regular languages—from aperiodic counters to cyclic groups—mechanisms that standard models in AC0 (hard attention) cannot express, and models in TC0 (soft attention) fail to learn robustly.

Empirically, this theoretical advantage translates into solved length generalization: Rational Transductors achieve 100% accuracy on tasks like parity and modular addition where standard Transformers fail catastrophically. As a theoretically tractable instantiation of the emerging class of Linear RNNs, the Transductor framework offers a rigorous path toward neuro-symbolic models that combine the best of connectionist learning and algebraic reasoning.

Furthermore, we introduced the Universal Transductor, which leverages a mixture of orthogonal and stochastic kernels to autonomously select the optimal dynamical bias for the task. Our theoretical analysis shows that this architecture constitutes a neural instantiation of the fundamental trinities of formal language theory:

• Algebraic Completeness: Via the Krohn-Rhodes decomposition, the Rational Head implements the missing group-theoretic components (cyclic counters), while the Transformer implements the aperiodic components (thresholds and resets), fulfilling the division of labor required for universal regular processing.

• Logical Completeness: The model bridges the gap between the limitations of First-Order Logic (FO[<]) (characteristic of hard-attention Transformers) and the full expressivity of Weighted MSO, enabling precise symbolic reasoning without sacrificing learnability.

• Statistical Generalization: We proved that the model’s reliability is guaranteed by a dual mechanism: contractive stability for fading-memory tasks, and algebraic exactness (via orthogonal parameterization) for infinite-memory tasks like Parity, ensuring robust performance independent of sequence length.

Ultimately, Rational Transductors represent a step towards bicameral foundation models, architectures that are as capable of precise, infinite-horizon sequential reasoning as they are of fluent semantic generation. By bridging the "Regular Gap" and capturing NC1-complete reasoning, this framework offers a mathematically grounded solution to the sequential logic failures inherent in standard Transformers. Furthermore, because the architecture maintains a strictly input-driven recurrence with O(L + log T) parallel depth, it is uniquely optimized for ultra-long-context modeling where quadratic bottlenecks remain prohibitive. Having established their theoretical completeness and empirical stability, the natural next step is evaluating transductors via large-scale pre-training on massive datasets.

<!-- Page 43 -->

## Acknowledgments

I thank Corinna Cortes and Will Merrill for very helpful comments on earlier drafts of this paper.

## References

C. Allauzen, M. Riley, J. Schalkwyk, W. Skut, and M. Mohri. OpenFst: A general and efficient weighted finite-state transducer library. In J. Holub and J. Zdárek, editors, Implementation and Application of Automata, 12th International Conference, CIAA 2007, Prague, Czech Republic, July 16-18, 2007, Revised Selected Papers, volume 4783 of Lecture Notes in Computer Science, pages 11–23. Springer, 2007.

D. Bahdanau, K. Cho, and Y. Bengio. Neural machine translation by jointly learning to align and translate. arXiv preprint arXiv:1409.0473, 2014.

B. Balle and M. Mohri. Spectral learning of general weighted automata via constrained matrix completion. In Advances in Neural Information Processing Systems, volume 25, pages 2159–2167, 2012.

B. Balle and M. Mohri. Learning weighted automata. In Proceedings of the 6th International Conference on Algebraic Informatics (CAI 2015), volume 9270 of Lecture Notes in Computer Science, pages 1–21, Stuttgart, Germany, September 2015. Springer.

B. Balle and M. Mohri. Generalization bounds for learning weighted automata. Theoretical Computer

Science, 716:89–106, 2017.

D. A. M. Barrington. Bounded-width polynomial-size branching programs recognize exactly those languages in NC1. Journal of Computer and System Sciences, 38(1):150–164, 1989.

J. Berstel and C. Reutenauer. Rational Series and Their Languages, volume 12 of EATCS Monographs on Theoretical Computer Science. Springer-Verlag, Berlin, Heidelberg, 1988.

G. E. Blelloch. Prefix sums and their applications. Technical Report CMU-CS-90-190, School of

Computer Science, Carnegie Mellon University, November 1990.

T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam,

G. Sastry, A. Askell, et al. Language models are few-shot learners. In Advances in Neural Information Processing Systems, volume 33, pages 1877–1901, 2020.

C. Cortes and M. Mohri. Context-free recognition with weighted automata. Grammars, 3(2-3):

133–150, 2000.

C. Cortes, P. Haffner, and M. Mohri. Rational kernels: Theory and algorithms. Journal of Machine

Learning Research, 5(Aug):1035–1062, 2004.

F. Danieli, P. Rodriguez, M. Sarabia, X. Suau, and L. Zappella. ParaRNN: Unlocking parallel training of nonlinear rnns for large language models. arXiv preprint arXiv:2510.21450, 2025.

T. Dao and A. Gu. Mamba-3: Improved sequence modeling using state space principles. OpenReview

Preprint, 2025. HwCvaJOiCj.

<!-- Page 44 -->

M. Droste and P. Gastin. Weighted automata and weighted logics. Theoretical Computer Science, 380

(1-2):69–86, 2007.

M. Fliess. Matrices de Hankel. Journal de Mathématiques Pures et Appliquées, 53(2):197–222, 1974.

M. Furst, J. B. Saxe, and M. Sipser. Parity, circuits, and the polynomial-time hierarchy. Mathematical systems theory, 17(1):13–27, 1984.

A. Graves. Generating sequences with recurrent neural networks. arXiv preprint arXiv:1308.0850,

2013.

A. Gu and T. Dao. Mamba: Linear-time sequence modeling with selective state spaces. arXiv preprint arXiv:2312.00752, 2023.

A. Gu, K. Goel, and C. Ré. Efficiently modeling long sequences with structured state spaces. arXiv preprint arXiv:2111.00396, 2021.

M. Hahn. Theoretical limitations of self-attention in neural sequence models. Transactions of the

Association for Computational Linguistics, 8:156–171, 2020.

X. Huang, A. Yang, S. Bhattamishra, Y. Sarrof, A. Krebs, H. Zhou, P. Nakkiran, and M. Hahn. A formal framework for understanding length generalization in transformers. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/ forum?id=U49N5V51rU.

H. Jung. On probabilistic tape complexity and fast circuits for matrix inversion problems. In Inter- national Colloquium on Automata, Languages, and Programming (ICALP), pages 281–291. Springer, 1985.

D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. In 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings, 2015. URL http://arxiv.org/abs/1412.6980.

K. Krohn and J. Rhodes. Algebraic theory of machines. i. prime decomposition theorem for finite semigroups and machines. Transactions of the American Mathematical Society, 116:450–464, 1965.

W. Kuich and A. Salomaa. Semirings, Automata, Languages, volume 5 of EATCS Monographs on

Theoretical Computer Science. Springer-Verlag, Berlin, Heidelberg, 1986. ISBN 978-3-540-16310-7.

M. Ledoux and M. Talagrand. Probability in Banach Spaces: Isoperimetry and Processes, volume 23 of

Ergebnisse der Mathematik und ihrer Grenzgebiete. Springer-Verlag, Berlin, Heidelberg, 1991.

I. Loshchilov and F. Hutter. Decoupled weight decay regularization. In International Conference on

Learning Representations, 2019. URL https://openreview.net/forum?id=Bkg6RiCqY7.

M.-T. Luong, H. Pham, and C. D. Manning. Effective approaches to attention-based neural machine translation. arXiv preprint arXiv:1508.04025, 2015.

W. Merrill and A. Sabharwal. The expressive power of transformers with chain of thought. In

International Conference on Learning Representations, 2024a.

W. Merrill and A. Sabharwal. Transformers in uniform TC0. arXiv preprint arXiv:2409.13629, 2024b.

<!-- Page 45 -->

W. Merrill, A. Sabharwal, and N. A. Smith. Saturated transformers are constant-depth threshold circuits. Transactions of the Association for Computational Linguistics, 10:843–856, 2022.

J. Miller and M. Hardt. Stable recurrent models. In International Conference on Learning Representa- tions, 2018.

M. Mohri. Weighted automata algorithms. In Handbook of Weighted Automata, pages 213–254.

Springer, Berlin, Heidelberg, 2009.

M. Mohri, F. Pereira, and M. Riley. Weighted finite-state transducers in speech recognition. Comput.

Speech Lang., 16(1):69–88, 2002.

B. Peng, E. Alcaide, Q. Anthony, A. Albalak, S. Arcadinho, H. Cao, X. Cheng, M. Chung, M. Grella,

K. Lin, et al. Rwkv: Reinventing rnns for the transformer era. In Findings of the Association for Computational Linguistics: EMNLP 2023, pages 14048–14077, 2023.

J. Pérez, P. Barceló, and J. Marinkovic. Attention is Turing-complete. Journal of Machine Learning

Research, 22(302):1–35, 2021.

A. Salomaa and M. Soittola. Automata-Theoretic Aspects of Formal Power Series. Texts and Monographs in Computer Science. Springer-Verlag, New York, 1978.

I. Schlag, K. Irie, and J. Schmidhuber. Linear transformers are secretly fast weight programmers. In

International Conference on Machine Learning, pages 9355–9366, 2021.

J. Schmidhuber. Learning to control fast-weight memories: An alternative to dynamic recurrent networks. Neural Computation, 4(1):131–139, 1992.

M.-P. Schützenberger. On the definition of a family of automata. Information and Control, 4(2-3):

245–270, 1961.

J. T. Smith, A. Warrington, and S. W. Linderman. Simplified state space layers for sequence modeling. arXiv preprint arXiv:2208.04933, 2022.

R. Smolensky. Algebraic methods in the theory of lower bounds for boolean circuit complexity. In

Proceedings of the nineteenth annual ACM symposium on Theory of computing, pages 77–82. ACM, 1987.

A. Terzi´c, N. Menet, M. Hersche, T. Hofmann, and A. Rahimi. Structured sparse transition matrices to enable state tracking in state-space models, 2025. URL https://arxiv.org/abs/2509. 22284.

A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin.

Attention is all you need. In Advances in neural information processing systems, volume 30, 2017.

A. Yang, M. Cadilhac, and D. Chiang. Knee-deep in C-RASP: A transformer depth hierarchy. arXiv preprint arXiv:2506.16055, 2025a. URL https://arxiv.org/abs/2506.16055.

S. Yang, Y. Shen, K. Wen, S. Tan, M. Mishra, L. Ren, R. Panda, and Y. Kim. Path attention: Position encoding via accumulating householder transformations. arXiv preprint arXiv:2505.16381, 2025b.

Y. Zhang, Z. Lin, Y. Du, et al. Kimi linear: An expressive, efficient attention architecture. arXiv preprint arXiv:2510.26692, 2025.

<!-- Page 46 -->

A Theoretical Background: Weighted Automata and Rational Power Series

In this appendix, we place the architecture of Rational Transductors within the broader theoretical framework of Weighted Finite Automata (WFAs) [Mohri, 2009] and Rational Power Series [Salomaa and Soittola, 1978, Berstel and Reutenauer, 1988, Kuich and Salomaa, 1986]. We define the specific class of series computed by our model and outline the fundamental theorems that guarantee their expressivity and learnability.

A.1 Rational Power Series over a Field

Let Σ be a finite alphabet and Σ∗be the free monoid generated by Σ. A formal power series S with coefficients in the field of real numbers R is a mapping S∶Σ∗→R. The value of S on a sequence x ∈Σ∗is denoted by (S, x). The set of all such formal power series is denoted by R⟪Σ∗⟫. The subset of Rational Power Series, denoted Rrat⟪Σ∗⟫, is the smallest subalgebra of R⟪Σ∗⟫containing all polynomials (series with finite support) that is closed under the following rational operations:

• Sum: (S + T, x) = (S, x) + (T, x);

• Cauchy Product: (S ⋅T, x) = ∑uv=x(S, u)(T, v)

• Kleene Star (Closure): S∗= ∑∞ n=0 Sn, provided (S, ϵ) = 0 to ensure convergence.

A.2 Linear Representations and WFAs

A fundamental result in the theory of weighted automata is the Schützenberger representation theorem [Schützenberger, 1961], which establishes that rational series are exactly those recognizable by finite weighted automata.

Definition 31 (Linear Representation). A linear representation of dimension d over R is a triple (α,{Mσ}σ∈Σ, β), where:

• α ∈Rd is the initial weight vector (column).

• Mσ ∈Rd×d are the transition matrices for each σ ∈Σ.

• β ∈Rd is the final weight vector (column).

This representation computes a series S defined by:

(S, x) = β⊺MxT... Mx1α. (52)

A.3 Fundamental Results

The Hankel Matrix and Fliess’ Theorem. A central tool in the analysis of rational series is the Hankel matrix HS, an infinite matrix indexed by pairs of strings (u, v) ∈Σ∗× Σ∗, where the entry at (u, v) is (S, uv).

Theorem 32 ([Fliess, 1974]). A series S is rational if and only if its Hankel matrix HS has finite rank. Furthermore, the rank of HS is equal to the dimension dmin of the minimal linear representation of S.

<!-- Page 47 -->

Minimization and Learning. For any rational series, the minimal linear representation is unique up to a similarity transformation (see [Balle and Mohri, 2015] for a short proof and illustration). Furthermore, spectral learning frameworks [Balle and Mohri, 2012] demonstrate that rational series can be learned efficiently under specific rank conditions via the singular value decomposition of the Hankel matrix.

A.4 Remarks on Terminology and Graph Interpretation

To clarify the relationship between our linear algebraic definition and standard automata theory, we provide the following remarks.

Equivalence of Dimension and State Count. The definition of a WFA via a linear representation of dimension d is mathematically isomorphic to a Weighted Finite Automaton with exactly d states.

• The dimension d corresponds to the set of discrete states Q = {q1,..., qd}.

• The entry (Mσ)ij corresponds to the weight of the edge transitioning from state qj to state qi upon reading symbol σ.

• Consequently, Fliess’ theorem can be equivalently stated as: the rank of the Hankel matrix equals the number of states in the minimal WFA recognizing the series.

The State Vector as a Weight Distribution. In the context of deep learning, the vector ht ∈Rd is often referred to as the “hidden state.” In the automata theoretic view, this vector represents the distribution of accumulated weights over the d states of the automaton at time t. Specifically, the i-th component ht,i is the sum of weights of all paths in the automaton ending at state qi given the input prefix x1∶t.

Deterministic Computation in Vector Space. While Weighted Finite Automata are not generally determinizable in the graph sense (i.e., transforming into an equivalent WFA with only one non-zero path per string) [Mohri, 2009], the linear recurrence ht = Mxtht−1 constitutes a deterministic update in the vector space Rd. This ensures that the Rational Transductor architecture remains deterministic and efficient to compute, despite the underlying WFA potentially representing non-deterministic weighted paths.

Finally, WFAs have been successfully used in a variety of applications, including speech recognition [Mohri, Pereira, and Riley, 2002]. The OpenFST software library [Allauzen, Riley, Schalkwyk, Skut, and Mohri, 2007] provides a very general and efficient implementation of the representation and algorithms related to WFAs.

<!-- Page 48 -->

B Experimental Details and Hyperparameters

B.1 Hyperparameter Specifications

To ensure reproducibility, we detail the exact hyperparameters used for the experiments in Section 7. All models were implemented in PyTorch and trained on a single NVIDIA T4 or A100 GPU. Optimization was performed using AdamW [Loshchilov and Hutter, 2019] or Adam [Kingma and Ba, 2015].

**Table 2.** summarizes the configurations for all four synthetic tasks. Note that for the Long-Integer Addition task, we used a curriculum learning strategy where the training sequence length was sampled uniformly from U[10,40] at each step to encourage robust generalization.

**Table 2.** Hyperparameters for Rational Transductor Experiments. (RT: Rational Transductor, TF: Transformer.)

Config / Task Modulo Counting Length Gen. Long Addition Base-2 Eval (Sec. 7.1) (Sec. 7.2) (Sec. 7.4) (Sec. 7.5)

## Model

Architecture Hidden Dim (dmodel) 32 32 32 12 (Rational Transductor) / 32 (Transformer) Rational State Dim (drat) 8 8 4 12 Layers 2 2 2 1 (Rational Transductor) / 3 (Transformer) Heads 4 4 4 4 Parameterization Orthogonal (Cayley) Orthogonal (Cayley) Stochastic (Softmax) Affine (General)

Optimization Seq Length (Ltrain) 50 40 U[10,40] 64 Batch Size 64 64 64 32 Optimizer AdamW AdamW AdamW Adam Learning Rate 5 × 10−3 5 × 10−3 5 × 10−3 1 × 10−2

Scheduler None Cosine Annealing None Cosine Annealing Gradient Clip 1.0 1.0 1.0 1.0 Training Steps 3,000 Steps 3,000 Steps 4,000 Steps 3,600 Steps (60 Epochs) Loss Function Cross Entropy Cross Entropy Cross Entropy MSE Precision Float32 Float32 Float32 Float64

B.2 Statistical Significance and Stability

Stability of Initialization: The Near-Identity Initialization described in Section 6.3 provides a highly stable starting point for learning algebraic structures. In our experiments (specifically Subsection 7.1 and Subsection 7.2), the Rational Transductor converged to 100% training accuracy within the first 500-1000 steps in every trial. The loss curves exhibit a deterministic drop characteristic of solving a convex-like problem in the lifted state space, rather than the high-variance grokking often seen in standard Transformers on these tasks.

Variance: We repeated all synthetic experiments across N = 5 random seeds to ensure statistical significance.

• Rational Transductor: Achieved 100% accuracy on the training distribution in 5/5 runs for Modulo Counting, Length Generalization, and Long-Integer Addition. For the Long- Integer Addition task, sequence-level standard deviation was negligible (< 0.05%). The Base-2 Evaluation task exhibited high stability across trials with an MSE standard deviation of < 1.0 × 10−10.

• Baseline Transformer: Consistently failed to generalize beyond Ltrain, with accuracy collapsing to the random baseline (20%) in all seeds, exhibiting negligible variance in its failure mode.

<!-- Page 49 -->

We conclude that the reported performance gap is due to the fundamental difference in inductive bias (Recurrent vs. Attention), not initialization luck.
