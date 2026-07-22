---
title: "SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients"
source_url: https://icml.cc/virtual/2026/oral/71182
paper_pdf_url: https://arxiv.org/pdf/2603.08824v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

<!-- Page 1 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Anselm Paulus * 1 A. Ren´e Geist * 1 V´ıt Musil 2 Sebastian Hoffmann 3 Onur Beker 1 Georg Martius 1 4

## Abstract

Automatic differentiation (AD) frameworks such as JAX and PyTorch have enabled gradient-based optimization for a wide range of scientific fields. Yet, many “hard” primitives in these libraries such as thresholding, Boolean logic, discrete indexing, and sorting operations yield zero or undefined gradients that are not useful for optimization. While numerous “soft” relaxations have been proposed that provide informative gradients, the respective implementations are fragmented across projects, making them difficult to combine and compare. This work introduces SoftJAX and SoftTorch, open-source, feature-complete libraries for soft differentiable programming. These libraries provide a variety of soft functions as drop-in replacements for their hard JAX and Py- Torch counterparts. This includes (i) elementwise operators such as clip or abs, (ii) utility methods for manipulating Booleans and indices via fuzzy logic, (iii) axiswise operators such as sort or rank – based on optimal transport or permutahedron projections, and (iv) offer full support for straight-through gradient estimation. Overall, SoftJAX and SoftTorch make the toolbox of soft relaxations easily accessible to differentiable programming, as demonstrated through benchmarking and a practical case study. Code is available at github.com/a-paulus/softjax and github.com/a-paulus/softtorch.

## 1. Introduction

Automatic differentiation (AD) frameworks have enabled rapid progress in machine learning. They make gradient computation efficient, user-friendly, and composable.

* Equal contribution. Libraries implemented by Anselm Paulus. 1University of T¨ubingen, Germany 2Masaryk University, Czechia 3Max Planck Institute for Biogeochemistry, Germany 4Max Planck Institute for Intelligent Systems, T¨ubingen, Germany. Correspondence to: Anselm Paulus <anselm.paulus@tuebingen.mpg.de>, A. Ren´e Geist <rene.geist@uni-tuebingen.de>.

Preprint. March 11, 2026.

10 4 10 2 10 0 <

< method="neuralsort" mode="smooth" method="softsort" mode="c0" import softjax as sj arr = jnp.array([x, -1.0, 0.5, 0.8, 2.0]) ranks = sj.rank(arr, method="neuralsort", mode="smooth")[0]

**Figure 1.** Top: SoftJAX and SoftTorch provide differentiable

surrogates for discrete operations i. e., rankτ instead of rank. Numerous soft approximations can be obtained by tuning the softness parameter τ, selecting the softening method (e. g., “neuralsort” or “softsort”), and choosing a smoothness mode (e. g., smooth for

C∞or c1 for C1). Bottom: The soft surrogates shown above are instantiated using just three lines of code.

Thereby, they become a ubiquitous tool widely adopted beyond machine learning. This includes (i) differentiable rendering (Wang et al., 2019) using Nerfs (Mildenhall et al., 2020) and Gaussian splatting (Kerbl et al., 2023); (ii) differentiable simulation, such as MuJoCo XLA (MJX) (Todorov et al., 2012; MuJoCo, 2024; Paulus et al., 2025) and WARP (Howell, 2025); (iii) structured prediction like ranking (Rol´ınek et al., 2020a) and matching (Rol´ınek et al., 2020b); (iv) combinatorial layers for CEM (Amos & Yarats, 2020), MPC (Amos et al., 2018), and discrete decisions (Pogancic et al., 2020; Berthet et al., 2020); (v) differentiable optimization (Amos & Kolter, 2017; Agrawal et al., 2019; Blondel et al., 2022); and (vi) physical simulations, e. g., for a gravitational wave detector (Ruiz-Gonzalez et al., 2025). However, the programs for these and many more applications contain classical operations using comparisons for branching code, ranking elements, and so forth.

Unfortunately, AD does not necessarily result in informative gradients. Here, informative means providing a stable local direction leading to improvements in the objective. Uninformative are cases with zero gradients (e. g., rounding, comparisons, indexing, sort/max/top-k/median)

arXiv:2603.08824v1 [cs.LG] 9 Mar 2026

![Figure extracted from page 1](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients and arbitrary subgradients (ReLU at zero, sort with duplicates). Many applications call for replacing such hard operations with soft ones that yield informative gradients. A successful example is addressing the “dying ReLU problem” (Lu et al., 2020), where ReLU’s zero gradients hinder gradient-based optimization of deep neural networks, by replacing the ReLU function with a smooth relaxation such as SiLU or Softplus.

While many relaxation techniques have been proposed, the existing toolbox is fragmented. Proposed techniques include analytic smooth surrogates (e. g., SiLU for ReLU (Hendrycks & Gimpel, 2016), sigmoid for steps (Petersen et al., 2021; 2022), and softmax for argmax (Beker et al., 2025; 2026)), optimization-based approaches (e. g., sorting via regularized optimal transport (Cuturi et al., 2019; Xie et al., 2020; Blondel et al., 2018) or projections onto the permutahedron (Blondel et al., 2020; Sander et al., 2023), proximal methods (Paulus et al., 2024)), stochastic relaxations (e. g., Gumbel-softmax (Maddison et al., 2017; Jang et al., 2017; Paulus et al., 2020), perturbed optimizers (Berthet et al., 2020; Niepert et al., 2021)), gradient “hacks” / estimators (straight-through (Bengio et al., 2013;

Sahoo et al., 2023), black-box differentiation (Pogancic et al., 2020)) and more.

To unify soft relaxations and ease their use, we present SoftJAX and SoftTorch. Our libraries provide soft dropin replacements for many commonly used hard operations in JAX (Bradbury et al., 2018) and Pytorch (Paszke et al., 2019). In turn, SoftJAX and SoftTorch form easy to use abstraction layers between user code and underlying primitive operations. Our treatment also draws unifying connections, generalizes various techniques, and provides comprehensible “softness” knobs and “mode” families across operations. As an example, see Figure 1 where we plot the soft rank operator for varying softness parameters τ > 0 and softening modes. As for all our relaxations, we recover the original hard operation as τ →0+. By combining the vast toolbox of soft relaxations, our libraries make soft differentiable programming accessible.

We next explain the operators implemented in SoftJAX and SoftTorch and how their hard versions are relaxed to soft counterparts. Section 2 reviews the basics of soft surrogates and straight-through estimation. Section 3 then describes the softening of elementwise operators in SoftJAX and SoftTorch, such as sign or round, via relaxations of the Heaviside step function. Section 4 shows how more involved axiswise operators, such as sort or quantile, can be softened via optimal transport or projections onto the unit simplex or the permutahedron. An overview of all currently implemented functions in SoftJAX is available in Figure 9. Finally, Section 5 presents runtime and memory comparisons to help end users select suitable methods that balance

1 0 1 x

0

1 sj.relu_st / jax.nn.relu sj.relu jax.grad(sj.relu_st)

**Figure 2.** The function relu st resorts to the straight-through

trick to use the hard function jax.nn.relu in the forward pass while using the soft function sj.relu for gradient computation.

the trade-offs required by their applications.

## 2. Softening and Straight-through estimation

Many functions used in modern ML frameworks are poorly suited for automatic differentiation as they are discontinuous or have large regions with zero derivative. To resolve this, our libraries have one main goal: to provide informative gradients for any program written in the supported frameworks. The underlying mechanism rests on two core concepts: soft surrogates and straight-through estimation.

Soft surrogate. Soft surrogates replace the original function with another function that has more informative gradients for optimization. Specifically, we call the function fτ with softening parameter τ > 0 a soft surrogate of f if (i) fτ is continuous and differentiable almost everywhere, (ii) fτ yields informative gradients over the relevant domain, i. e., avoids extended regions of zero derivative, and (iii) fτ recovers f in the limit τ →0+. The softening parameter τ controls the trade-off between faithfulness to f and gradient informativeness: larger τ benefits differentiability, while τ →0+ causes fτ to approach the original function. See Figure 2 for an example of a soft relu surrogate. Note that softening a function may involve significantly altering the output domain, e. g., a soft surrogate for boolean operations outputs a probability instead of a Boolean value, likewise a soft surrogate for an argmax operation outputs a probability distribution over indices instead of an index.

Straight-through estimation. Unfortunately, blindly replacing a function with a soft surrogate may introduce undesired effects in the forward pass, e. g., resulting in unphysical rollout trajectories of a simulator. Fortunately, these problems can be addressed effectively through straight-through estimation (STE).

Historically, STE dates back to early work on single-layer perceptrons (Rosenblatt, 1957), where the derivative of binary activations was replaced with the derivative of the identity map. Following Bengio et al. (2013), STE keeps the original function in the forward pass during automatic

<!-- Page 3 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

0

0

0

0 0

**Figure 3.** Arrows depict the normalized gradient of the product

of two functions f(x, y) = relu(x) and g(x, y) = relu(y). Applying straight-through estimation on each function individually causes the gradient ∇(fSTE · gSTE) to be zero if x < 0, whereas the gradient ∇(f · g)STE is non-zero.

differentiation, but uses the gradient of a soft surrogate in the backward pass. In our framework, STE is implemented via the straight-through trick, writing fSTE(x) = sg(f(x)) + fτ(x) −sg(fτ(x)), (1)

where sg denotes the stop-gradient operator of an automatic differentiation library. Therefore, we obtain fSTE = f on the forward pass, but ∇fSTE = ∇fτ on the backward pass. In practice, using a soft surrogate for differentiation amounts to wrapping a soft function like sj.relu in the sj.st function decorator, which implements the straight-through trick, i. e., y soft st = sj.st(sj.relu). Figure 2 illustrates straight-through wrapping a soft relu surrogate.

The straight-through pitfall. A subtle issue arises when STE-wrapped functions interact multiplicatively. Automatic differentiation computes the gradient between the product of functions fSTE(x) and gSTE(y) via the product rule as

∇(fSTE · gSTE) = ∇fτ · g + f · ∇gτ, (2)

where the original functions f and g appear as multiplicative gates in the backward pass. This defeats the purpose of softening, as the gradient can still vanish when scaled by f or g. As illustrated in Figure 3 for the case of f(x, y):= relu(x) and g(x, y) = relu(y), ∇(fSTE · gSTE) is zero when x, y < 0. To avoid gradient multiplication by zero, STE should be applied to the composite function such that

∇(f · g)STE = ∇(fτ · gτ) = ∇fτ · gτ + fτ · ∇gτ. (3)

In code, this reads: (notice the decorator)

@sj.st def relu_prod(x, y, **kwargs):

relu_x = sj.relu(x, **kwargs) relu_y = sj.relu(y, **kwargs) return relu_x * relu_y

To our knowledge, this “STE pitfall” and its remedy have not been explicitly discussed before.

1

-1 sign round abs clip less_equal isclose

'hard'

'smooth' mode=...

'c0' 1 1 y x ϵ greater heaviside x x

1 y 0

1 y x

1

-1 b a

**Figure 4.** Top: The heaviside function surrogates Hτ are used to

derive the sign, round, abs, and clip functions. Bottom: Comparison operations compare values x, y ∈R by interpreting Hτ as a CDF defining the probability that x > 0.

## 3. Elementwise Operators

Conceptually, all our elementwise soft operators, some of which are illustrated in Figure 4, are rooted in the relaxation of the Heaviside step function, defined as

H(x):=

  

 

0 if x < 0, 0.5 if x = 0, 1 else.

(4)

Its derivative is zero everywhere except at the origin, where it is not defined. Following many previous works (Funahashi, 1989; Han & Moraga, 1995; Rojas, 1996; Mhaskar, 1996; Duch & Jankowski, 1999; Huang et al., 2006b;a; Yuen et al., 2021; Li et al., 2021), we soften the Heaviside function with a sigmoidal function that traces a characteristic S-shape. Some examples include the standard exponentialbased sigmoid (referred to as smooth mode)

Hτ(x):= σ x τ

= 1 1 + exp(−x/τ), (5)

or the piece-wise polynomial-based sigmoidals1

Hτ(x):=

  

 

0 if x < −τ, g(x τ) if −τ ≤x ≤τ, 1 else,

(6)

with gc0(s):= 1 2 + s 2, gc1(s):= 1 2 + 3s 4 −s3 4, and gc2(s):= 1 2 + 15s 16 −5s3 8 + 3s5

16. The piecewise modes transition on [−τ, τ]; in the library, their input is rescaled by 1/5 so that all modes share an effective transition width of approximately 10τ, matching the smooth mode (σ(±5) ≈0.007/0.993). These piece-wise Heaviside relaxations are either continuous (linear, also referred to as c0 mode), differentiable (c1), or twice differentiable (c2).

## 3.1. Sign, abs, and round

A soft surrogate for the sign function is obtained by the Heaviside function and subtracting a constant. Moreover, a

1We overload the notation here.

<!-- Page 4 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients soft surrogate for the abs function is obtained by gating the soft sign function with x, reading signτ(x):= 2 · Hτ(x) −1, (7)

absτ(x):= signτ(x) · x. (8)

Following Semenov (2025), the round function is implemented as the difference between shifted sigmoidals roundτ(x):=

⌊x⌋+K X k=⌊x⌋−K k

Hτ x −k + 1

2

−Hτ x −k −1

2

, where K controls the number of neighbouring sigmoidals that are taken into account. Larger temperatures τ require a higher K, as each sigmoidal is softened over a larger region, thereby increasing its region of influence.

## 3.2. ReLU and clip

Due to its widespread use in ML, the rectified linear unit (ReLU) deserves extra attention. The function relu(x):= max{0, x} has zero gradient for x < 0, and at x = 0 it is only sub-differentiable. To get a soft surrogate, we can transform the sigmoidal via Integration reluτ(x):=

Z x

0 Hτ(t) dt, (9)

or via a gating mechanism reluτ(x):= x · Hτ(x). (10)

Therefore, for each of the Heaviside relaxations, we define two ReLU relaxations, some of which are well known. For instance, integrating the sigmoid yields the Softplus τ log(1 + ex/τ). On the other hand, gating the sigmoid recovers the SiLU activation (Hendrycks & Gimpel, 2016) x · σ(x/τ). From the soft ReLU, we can now derive a soft surrogate for the clip function as clipτ(x, a, b):= a + reluτ(x −a) −reluτ(x −b). (11)

## 3.3. Comparison operators and differentiable logic

Next, we turn to soft surrogates of comparison operators, such as greater or equal. The hard operators output a Boolean variable b ∈{True, False}, whereas our soft surrogates output a value in the interval [0, 1]. We directly get the soft comparison operators via the soft Heaviside function greaterτ(x, y) = Hτ(x −y −ϵ), gtr equalτ(x, y) = Hτ(x −y + ϵ), lessτ(x, y) = Hτ(y −x −ϵ), less equalτ(x, y) = Hτ(y −x + ϵ), equalτ(x, y) = 2 · less equalτ(absτ(x −y), 0), iscloseτ(x, y) = 2 · less equalτ(absτ(x −y), tol).

(12)

Here, ϵ denotes the machine precision to ensure that the surrogates converge to the correct hard function as τ →0+. In the definition of iscloseτ, we use a standard tolerance tol = atol + rtol · absτ(y) with atol > 0 and rtol > 0 denoting the relative and absolute tolerance.

The output of our soft surrogates can be interpreted as the probability of the hard comparison being True. For the sake of simplicity, we refer to such a probability as a soft Boolean or, in short, a “SoftBool”. This perspective has been studied extensively in the field of fuzzy logic (Belohlavek et al., 2017). Given multiple SoftBools p1,..., pn, differentiable logic operators reduce to the manipulation of probabilities. By default, our framework implements the logical all operator as all(p1,..., pn):= n Y j=1 pj, (13)

denoting the joint probability that independent Boolean events p1,..., pn equate to True. Alternatively, we allow using the geometric mean providing advantageous numerical scaling for gradient computation. Similarly, the not operator yields the probability that a Boolean event is False not(p):= ¬p = 1 −p. (14)

Other fuzzy logical operators are derived using the all and not operators any(p1,..., pn):= ¬ all(¬p1,..., ¬pn), and(p, q):= all(p, q), or(p, q):= any(p, q), xor(p, q):= or and(p, ¬q), and(¬p, q)

.

(15)

Similar to how normal Boolean variables can be used to select elements among two arrays, we can use a SoftBool variable pi to do a soft selection via the expectation zi = pi · xi + (1 −pi) · yi. (16)

In code, this is abstracted from the user via soft_cond = sj.greater(x, y) # [0.05 0.73 0.98] z = sj.where(soft_cond, x, y) # [0.39 0.27 0.69]

## 4. Axiswise Operators

After discussing elementwise operators in the previous section, this section discusses and derives soft surrogates for axis-wise operators such as argmax, sort or argtopk.

The simplest example of an axiswise operation is the (arg)max operator. The standard argmax operator returns an index j ∈{0,..., n −1}, and the max operator simply selects the corresponding element xj. Another way to write

<!-- Page 5 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients this is as an inner product xj = ej · x, where ej is one at index j and zero everywhere else. We can now relax the notion of an index as an indicator vector to a “SoftIndex” on the unit simplex

∆n:= p ∈[0, 1]n |

X

0≤j<n pj = 1

. (17)

In the case of the argmax operator, a simple relaxation that produces a SoftIndex is the softmax function (more accurately referred to as softargmax). The previous dot-product index-selection can now be interpreted as an expectation p · x =

X

0≤j<n pjxj = E j∼p[xj]. (18)

In code, our drop-in replacements read as:

x = jnp.array([0.1, 0.4, 0.8])

idx = jnp.argmax(x) # 2 y = jax.lax.dynamic_index_in_dim(x, idx) # [0.8]

soft_idx = sj.argmax(x) # [0.004 0.042 0.953] y = sj.dynamic_index_in_dim(x, soft_idx) # [0.78]

We can further generalize this technique of using SoftIndices to sorting and ranking. To see this, we first note that sorting an array x ∈Rn can be viewed as multiplying it with the sorting permutation matrix

P ⋆∈Σ = {P ∈{0, 1}n×n | P1n = 1n, P ⊤1n = 1}n

(19)

such that sort(x) = P ⋆x. (20)

Throughout, sort is in ascending order. The rows of P ⋆are indicator vectors, and the matrix multiplication can be interpreted as doing index selection in parallel. In this sense, the permutation matrix P ⋆can be interpreted as the generalized argsort operator, i. e., arg sort(x) = P ⋆. (21)

Similarly, the same matrix can be used for ranking, where rank 1 is assigned to the largest element, rank(x) = (P ⋆)⊤[n,..., 1]⊤. (22)

We can now relax the notion of a permutation matrix into a bistochastic matrix, the set of which is also called the Birkhoff polytope

Bn = {Pτ ∈Rn×n

+ | Pτ1n = 1n, P ⊤ τ 1n = 1n}. (23)

Note that in practice, for sorting or ranking, we only need Pτ to be a row- or column-stochastic matrix, respectively. The following two sections discuss how we can compute x y

2.0

0.3

-1.0

-3.1

4.0 1.0

0.5

0.0

0 1 a j b i

**Figure 5.** OT-based arg topk computes a (scaled) optimal transport

plan P ⋆ τ whose entries P ⋆ ij contain the probability mass transported from the j-th entry of x to the i-th entry of the anchor y.

soft permutation matrices Pτ from x, either resorting to regularized optimal transport (OT) or unit simplex projections. Finally, we will discuss an approach that directly relaxes the sort operator via projection onto the permutahedron without relaxing permutation matrices. In this version of the library, we deliberately choose to focus on deterministic approaches, and do not consider stochastic ones such as (Berthet et al., 2020; Jang et al., 2017; Maddison et al., 2017; Paulus et al., 2020). Table 2 provides an overview on the various available methods and regularizations.

## 4.1. Optimal Transport-based

The first family of algorithms is based on optimal transport. In general, optimal transport describes optimally moving probability mass from one distribution to another distribution while paying minimal cost. As described by Cuturi et al. (2019), regularized OT can be used to define soft (arg)sort operators. The general idea is to mimic a sortinglike behavior by defining two uniform distribution, one on the to-be-sorted input vector x ∈Rn and one on a set of increasing “anchor” points y ∈Rn. The optimal transport cost matrix is then defined as the squared distance between input and anchor points, which means that probability mass from large values of x will be moved to large anchor points. As the anchor points are sorted, this creates a sorting behavior, which is illustrated in Figure 5.

OT problem. The regularized optimal transport problem between two discrete probability measures Pn i=1 aiδxi, with source vector x = [x1, x2,..., xn]⊤and probability weight vector a = [a1, a2,..., an]⊤, and Pm j=1 bjδyj, with target vector y = [y1, y2,..., ym]⊤and probability weight vector b = [b1, b2,..., bm]⊤, is defined as

Γ⋆ τ:= arg min

Γ∈U(a,b)

⟨Γ, Cxy⟩+ τR(Γ). (24)

Here, the cost matrix (Cxy)ij = (xi −yj)2 is computed as the squared differences and U denotes the transport polytope of matrices summing to the marginals across rows and columns, i. e.,

U(a, b):= {Γ ∈Rn×m

+ | Γ1m = a, Γ⊤1n = b}. (25)

![Figure extracted from page 5](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-005-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Note that we omit the dependency of the optimal transport plan Γ⋆ τ on (a, x, b, y) for brevity.

We consider the case of an entropic regularizer R(Γ) = P i,j Γij(log Γij −1) (Cuturi, 2013), Euclidean regularizer R(Γ) = 1

2 P i,j Γ2 ij (Blondel et al., 2018) and p-norm regularizer R(Γ) = 1 p

P i,j |Γij|p (Paty & Cuturi, 2020). It is well known that the Euclidean regularizer has a sparsityinducing effect on the gradients; see, e. g., SparseMax (Martins & Astudillo, 2016). As discussed by Sander et al. (2023) in the context of projections onto the permutahedron, the p-norm regularizer shares this property, but additionally allows for everywhere differentiable relaxations (Theorem 1). Interestingly, for univariate inputs, the closed-form solutions of the entropic and Euclidean OT problem reduce to the corresponding sigmoidal functions used in our soft Heaviside relaxation, as shown in Section D.3.

OT based operators. We set the source marginal to a uniform distribution a = 1n/n, and specifically for sorting and ranking, we follow Cuturi et al. (2019) by setting uniform b = 1n/n and grid-like y = 1 n−1[0,..., n −1]⊤.

We define the scaled transposed transportation plan P ⋆ τ:= n(Γ⋆ τ)⊤. Since Γ⋆ τ1 = a and (Γ⋆ τ)⊤1 = b, each row and column of P ⋆ τ sums to 1. This allows us to interpret P ⋆ τ as a soft permutation matrix.

Moreover, we first standardize and then squash x with a sigmoid to the range [0, 1]. Although this is not strictly necessary, the use of x and y in the range [0, 1] improves numerical stability and makes the softening parameter independent of the scale of x. Then we have2 arg sortτ(x) = P ⋆ τ ∈Rn×n, (26)

sortτ(x) = P ⋆ τ x ∈Rn, (27)

rankτ(x) = (P ⋆ τ)⊤[n,..., 1]⊤∈Rn. (28)

To abstract the soft indices away from the user, we offer several replacements of utility functions for index selection that mirror the behavior of standard hard JAX and PyTorch index selection, e. g., x = jnp.array([0.3, 1.0, -0.5])

ind = jnp.argsort(x) # [2 0 1] val = jnp.take_along_axis(x, ind) # [-0.5 0.3 1.0]

soft_ind = sj.argsort(x)

## [[0.07 0. 0.93 ], [...], [...]] val = sj.take_along_axis(x, soft_ind)

## [-0.444 0.31 0.936]

In principle sorting is enough to define many other operators like max, median and top-k, via appropriate selection and

2Note, that the multiplication of the soft permutation matrix with x has close ties to the gating-style definition of the soft relu function in Equation (10), see Section D.5 for details.

combination of the soft-sorted values. However, the dimensionality of the cost matrix for an n-dimensional vector x is n × n, which can lead to large memory requirements.

Fortunately, it is possible to strongly reduce the dimensionality, by transporting multiple elements of x which we are not interested in (e. g., the bottom n −k elements in top-k) to a shared dummy anchor point, thereby reducing the number of anchors. For top-k, we follow Xie et al. (2020) by setting b = [ 1 n,..., 1 n, n−k n ]⊤∈R1×(k+1), y = 1 k[k,..., 1, 0]⊤∈R1×(k+1), then arg topkτ(x, k) = (P ⋆ τ)1:k ∈Rk×n, (29)

topkτ(x, k) = (P ⋆ τ)1:kx ∈Rk. (30)

Note that we can also trivially define an OT-based max as topkτ(x, k = 1); and min by flipping signs. For q-quantiles we slightly vary the approach of Cuturi et al. (2019) by setting k = ⌊q(n −1)⌋, b = [ k n, 1 n, 1 n, n−k−2 n ]⊤, y = 1 3[0, 1, 2, 3]⊤, then we can compute the lower ↓and upper ↑ q-quantiles via the second and third entry of P ⋆ τ, i. e., quantile↓ τ(x, q) = (P ⋆ τ)2x ∈R, (31)

quantile↑ τ(x, q) = (P ⋆ τ)3x ∈R. (32)

Various quantile definitions can be recovered by appropriately combining the upper and lower quantiles (e. g., interpolating or using midpoint). We also trivially get the median by evaluating the quantile function with q = 0.5.

## 4.2. Approximate OT: Unit simplex projection-based

The relaxations based on OT have many desirable properties such as smoothness in the case of an entropic regularizer. However, solving the OT problem can be memoryand compute-intensive in practice. We now describe different soft surrogates based on unit-simplex projections, which have a closed-form solution. The downside is that these relaxations typically still allow for some nondifferentiabilities, e. g., when ties occur. However, in practice they often perform well and are therefore selected as the default method of choice.

Unit simplex projection. The regularized linear program over the simplex, see Equation (17), is defined as

Πτ(x):= arg max p∈∆n

⟨x, p⟩−τR(p). (33)

We consider Euclidean regularization R(p) = 1 2∥p∥2 2, which leads to a Euclidean projection onto the unit simplex and entropic regularization R(p) = P j pj log pj, leading to a closed-form solution via the softmax exp(x/τ)/P j exp(xj/τ). Finally, we consider p-norm regularization R(p) = 1 p

P j |pj|p, which leads to a Bregman projection (Bregman, 1967) onto the unit simplex.

<!-- Page 7 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

## 1. Compute anchor

## 3. Axiswise unit simplex projection

4. Compute expectation 2. Pairwise distances

-9

-2.2

0.1

4

6 d(-9, 6)

. -9.0

-2.19

0.09

4.0

5.9

0 1 log scale 0 15 array array

0.1 4 -2.2 6 -9 0.1 4 -2.2 6 -9

**Figure 6.** Illustration of the Softsort algorithm.

SoftSort. Entropy-regularized OT can be solved efficiently via the Sinkhorn algorithm (Cuturi, 2013). In the case of OT for sorting in Equation (26), where both marginals a and b are uniform, the Sinkhorn algorithm boils down to alternating row and column softmax-normalization of the cost matrix. SoftSort (Prillo & Eisenschlos, 2020) can be seen as approximating this algorithm by reducing it to a single row-wise softmax normalization via a clever initialization of the anchors. This corresponds to the entropic regularizer in Equation (33), which we generalize to other regularizers, leading to new variants of SoftSort.

To define the anchors, instead of using a uniform grid over the interval [0, 1] as in Equation (26), the anchors are constructed by first applying the hard operator to x, e. g., y = sort(x). The cost matrix is the absolute difference between elements of x and y, which will intuitively assign a low transportation cost between elements of sort(x) that are close to x. For the sort operator, this leads to arg sortτ(x):= Πτ

−| sort(x)1⊤ n −1nx⊤|

. (34)

The projection is applied row-wise. The computation is illustrated in Figure 6. We showcase the output and partial derivatives of the soft sort operation for two different regularizers over a range of τ in Figure 7.

Note that the computation is independent over rows, we can therefore independently get soft operators for each of the sorted elements, which trivially gives us a soft (arg)topk/ quantile/max operator, by replacing the sort function in Equation (34) with the corresponding operator. Interestingly, the argmax operator reduces to Pτ(x), which for entropic regularization is simply softmax, thereby recovering the example used in the beginning of the chapter. For Euclidean regularization, it recovers the SparseMax (Martins & Astudillo, 2016) operator.

Finally, we can also define a novel SoftSort-style rank operator. For this we observe that Πτ is applied independently to each row of the cost matrix, so the resulting matrix is only row-stochastic and the corresponding argsort operator cannot be transposed to define a soft ranking as we did in the OT case. Instead, we transpose the cost matrix before applying the unit-simplex projection, which gives distributions over rank indices as arg rankτ(x):= Πτ

−|1n sort(x)⊤−x1⊤ n |

. (35)

Note, that all SoftSort-based surrogates are not fully smooth, as the computation involves the hard sort operator (nonsmooth at ties) and the absolute value function (non-smooth at zero). For this reason, the NeuralSort-based surrogates (which are fully smooth when combined with our soft abs) are selected as the default method for sort, rank, quantile, and median. However, for argmax, argmin, max, and min, the SoftSort-based method is the default, since it requires only a single simplex projection, giving O(n) complexity compared to NeuralSort’s O(n2), and in smooth mode it reduces to the standard softmax, the canonical soft argmax.

NeuralSort. NeuralSort (Grover et al., 2019) also utilizes unit-simplex projections but originates in a soft relaxation of the median operator. Defining the matrix of soft absolute differences Aτ x ∈Rn×n using our soft abs from Equation (8) as

(Aτ x)ij:= absτ(xi −xj), (36)

we have that Aτ x1n is the vector of sums of soft absolute differences between each element and all other elements.3

It is well-known that the median minimizes this sum for τ →0+, therefore we have arg median(x):= arg min p∈∆n

⟨A0 x1n, p⟩. (37)

By adding a regularizer similar to SoftSort Equation (33), we get a soft surrogate arg medianτ(x):= arg min p∈∆n

⟨Aτ x1n, p⟩+ τR(p) (38)

= Πτ(−Aτ x1n). (39)

NeuralSort generalizes this idea to the sorting operator, by setting arg sortτ(x)i:= Πτ

(2i −n −1)x −Aτ x1n

. (40)

For τ →0+ this recovers the true argsort operator. Intuitively, the vector that is projected is a linear combination of the original vector x and the vector of sums of soft absolute differences, which, when projected onto the unit simplex individually, give an argmax and an argmedian relaxation, respectively.

This also directly provides relaxations for the argmax, argmin, argquantile↑and argquantile↓operators by computing only the corresponding elements of the soft sorted

3The original NeuralSort paper (Grover et al., 2019) uses the hard |xi−xj|, which introduces gradient discontinuities at ties. By using our soft abs, we obtain fully smooth NeuralSort surrogates.

![Figure extracted from page 7](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

10−1 101 τ

0

1

2

Partial Derivative

10−1 101 τ

0

5

Output Value

Entropic Euclidean

**Figure 7.** Top: Output of the sort operator using “softsort” for

an array of n = 6 values as a function of softness τ. Elements converge to the mean value as τ →∞. Bottom: Partial derivatives ∂yj/∂xi. Here, j denotes the sorted position of input element xi. As τ →∞, the derivatives converge to 1/n.

array, i. e., with c↑= n −1 −2⌈q(n −1)⌉and c↓= n−1 −2⌊q(n−1)⌋, arg maxτ(x):= Πτ

(n −1)x −Aτ x1n

(41)

arg minτ(x):= Πτ

−(n −1)x −Aτ x1n

(42)

arg quantile↑ τ(x, q):= Πτ

−c↑x −Aτ x1n

(43)

arg quantile↓ τ(x, q):= Πτ

−c↓x −Aτ x1n

(44)

Note that the original paper (Grover et al., 2019) only treats the smooth (entropic) projection; we extend it to c0, c1, and c2 regularizers. As with SoftSort, the NeuralSort argsort matrix is only row-stochastic. To obtain soft ranks, we normalize each column to sum to one and compute rankτ(x) = eP ⊤[n,..., 1]⊤, mirroring Equation (26).

## 4.3. Permutahedron projection-based

For sorting and ranking, both OT-based and unit-simplexprojection-based approaches involve computations with the n × n cost matrix. In SoftJAX, we avoid materializing this matrix by processing rows in chunks via lax.scan, reducing memory from O(n2) to O(n) while also yielding O(1) XLA compilation time. Nevertheless, for large n, the O(n2) time complexity remains a bottleneck. Blondel et al. (2020); Sander et al. (2023) resolve this issue by directly softening the value-space operators, e. g., sort instead of argsort. This is achieved by interpreting these operators as projections onto the permutahedron, the convex hull of permutations of z, i. e.,

P(z):= conv({zσ | σ ∈Σ}). (45)

Here, Σ is the set of permutation matrices, see Equation (19). The Euclidean projection of a vector y ∈Rn onto the permutahedron of another vector z ∈Rn is given by

Projτ(y, z):= arg max p∈P(z)

⟨y, p⟩−τ

2

X j p2 j (46)

= arg min p∈P(z)

1 2∥p −y τ ∥2

2. (47)

Blondel et al. (2020) also propose a variant that uses an entropic regularizer by optimizing over exponentiated inputs and taking the log, i. e.,

Projτ(y, z):= log arg max p∈P(ez)

⟨y, p⟩−τ⟨p, log p −1⟩

.

FastSoftSort. Intuitively, FastSoftSort (Blondel et al., 2020) now projects the sorted ranks onto the permutahedron of the input x, which will select the permutation of x that is closest to being sorted. In the same way, projecting the (negative) x onto the permutahedron of the possible ranks selects the ranks that follow the ordering of x. This gives the surrogate operators sortτ(x) = Projτ([1,..., n], x), (48)

rankτ(x) = Projτ(−x, [1,..., n]). (49)

Other operators like top-k, quantile, median or max can be computed by first running soft sorting, and then selecting the appropriate values.

Crucially, Blondel et al. (2020) derive an algorithm based on isotonic optimization which solves the projection onto the permutahedron in O(n log n). This is much faster than the runtime of Sinkhorn which is O(Tn2), where T is the number of Sinkhorn iterations. However, note that this approach does not allow for an argsort or argrank operator.

SmoothSort. In OT and unit simplex projection-based approaches, entropic regularization typically leads to dense Jacobians, whereas Euclidean regularization promotes sparsity, see e. g., (Blondel et al., 2018). However, in FastSoft- Sort this is not the case: While Euclidean regularization behaves as usual by promoting sparsity, the entropic regularization behaves very similarly to the Euclidean case by promoting sparsity, as also discussed by Blondel et al. (2020).

Therefore, we propose a new variant of this surrogate family by adding entropic regularization to a dual formulation of the permutahedron projection; see Section D.6 for details. This leads to a surrogate that behaves more like the entropic regularizer in the OT setting, which yields dense Jacobians. Moreover, by replacing the hard order-statistic bounds in the permutahedron LP with smooth log-sum-exp relaxations (Section D.6), this variant is C∞differentiable, unlike the other FastSoftSort variants which are at most C2. Unfortunately, we cannot use the same fast PAV algorithm in this

<!-- Page 9 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

26 28 210 212

Array Size

101

103 Time (ms)

26 28 210 212

Array Size

102

105 Memory (KB)

Hard OT

SoftSort NeuralSort

FastSoftSort SmoothSort

SortingNet

**Figure 8.** Computation time (left) and peak memory consump-

tion (right) for a full forward-backward pass of sj.sort using smooth regularization. All six soft sorting methods are compared against the hard baseline. Extended results across all modes are in Figure 14.

case, because the smooth bounds require O(n2) preprocessing and the LP is solved via L-BFGS. However, compared to entropy-regularized OT, the O(n2) cost is paid only once (for the bounds), not per iteration, and we do not need to materialize an n × n matrix.

## 4.4. Sorting network-based

An alternative approach that avoids both the O(n2) pairwise cost matrix and iterative optimization is to use a differentiable sorting network. Following Petersen et al. (2021), who propose replacing the hard compare-and-swap operations in a bitonic sorting network with soft comparisons based on a logistic sigmoid, we implement a bitonic sorting network using our soft Heaviside function Hτ (Equations (5) and (6)) for soft swapping, i. e., σ = Hτ(a −b), (50)

soft min(a, b) = σ · b + (1 −σ) · a, (51)

soft max(a, b) = σ · a + (1 −σ) · b. (52)

In smooth mode, Hτ is the logistic sigmoid, directly recovering the method of Petersen et al. (2021), while c0, c1, and c2 modes yield new sorting network variants with the corresponding smoothness guarantees. Following Petersen et al. (2021), we obtain soft permutation matrices by tracking an n×n matrix P (initialized to the identity) through the network. At each compare-and-swap step, the rows of P corresponding to the two compared positions are mixed using the weights σ and 1 −σ, hence sort(x) = Px. Unlike Fast- SoftSort, sorting networks can therefore produce both sorted values and soft permutation matrices, enabling argsort and argmax in addition to sort, max, min, quantile, median, and top k.

5. Benchmarks & Case Study

In order to be useful for machine learning practitioners, softened functions and their gradients must be both fast to compute and memory efficient. SoftJAX allows us to easily compare these aspects across different methods within a unified framework. Figure 8 shows the computation time and peak memory of sj.sort for different input sizes and methods (smooth mode) on an Nvidia RTX 3060 GPU. The sorting network is the fastest soft method at 1.0 ms for n = 4096 (only ∼3.8× the hard baseline), followed by SoftSort (16 ms) and NeuralSort (37 ms). FastSoftSort is the most memory-efficient method, scaling roughly linearly (420 kB at n = 4096) since it avoids materializing a permutation matrix. Our novel method SmoothSort and the OT-based surrogate are the slowest out of the testsed methods. Extensive benchmarking results on all methods and modes for a variety of axis-wise functions are included in Appendix E.

Additionally, we include a case study which demonstrates the ease of using SoftJAX for softening a subroutine which is commonly used in collision detection, see Appendix B for details.

## 6. Conclusion

Standard tensor libraries with GPU acceleration and automatic differentiation have enabled differentiable optimization at scale in ML research. For many problems in ML and other fields, discrete primitives are needed, but result in uninformative gradients. Differentiable alternatives are scattered across papers, slowing progress and adoption. This work introduces SoftJAX and SoftTorch: feature-complete, unified and extensible libraries for soft relaxations of hard operators with principled straight-through estimation (STE).

We systematically derive differentiable surrogates for elementwise discrete operators from smooth relaxation of the Heaviside step function. Our framework also provides a broad set of axiswise differentiable discrete operators including argsort, argquantile, and argtop k – implemented via state-of-the-art algorithms based on optimal transport and simplex/permutahedron projections and derive indexselection primitives (e.g., take along axis, choose) for endto-end use. Through this standardization, this work derives a broad range of differentiable operators for which an implementation is currently not easily available (see Table 2).

Overall, the framework consolidates core components for soft differentiable programming into a single, well-tested, feature-complete library, improving reproducibility and lowering the barrier to widespread use of soft differentiable programming in practice.

## Acknowledgements

We thank the International Max Planck Research School for Intelligent Systems (IMPRS-IS) for supporting Anselm Paulus and Onur Beker.

<!-- Page 10 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

This work was supported by the ERC - 101045454 REAL- RL and the German Federal Ministry of Education and Research (BMBF) through the T¨ubingen AI Center (FKZ: 01IS18039A). Georg Martius is a member of the Machine Learning Cluster of Excellence, EXC number 2064/1 – Project number 390727645.

The work on this paper was supported by the Czech Science Foundation (GA ˇCR) grant no. 26-23981S.

Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here.

## References

Agrawal, A., Amos, B., Barratt, S. T., Boyd, S. P., Diamond,

S., and Kolter, J. Z. Differentiable convex optimization layers. In Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada, pp. 9558–9570, 2019.

Amos, B. and Kolter, J. Z. Optnet: Differentiable optimiza- tion as a layer in neural networks. In Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney, NSW, Australia, 6-11 August 2017, pp. 136–145, 2017.

Amos, B. and Yarats, D. The differentiable cross-entropy method. In Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event, pp. 291–302, 2020.

Amos, B., Rodriguez, I. D. J., Sacks, J., Boots, B., and

Kolter, J. Z. Differentiable MPC for end-to-end planning and control. In Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montr´eal, Canada, pp. 8299–8310, 2018.

Beker, O., G¨urtler, N., Shi, J., Geist, A. R., Razmjoo, A.,

Martius, G., and Calinon, S. A smooth analytical formulation of collision detection and rigid body dynamics with contact. In 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 18558–18565, 2025. doi: 10.1109/IROS60139.2025.11247449.

Beker, O., Geist, A. R., Paulus, A., G¨urtler, N., Shi, J.,

Calinon, S., and Martius, G. Smoothly differentiable and efficiently vectorizable contact manifold generation. arXiv:2602.20304, 2026.

Belohlavek, R., Dauben, J. W., and Klir, G. J. Fuzzy logic and mathematics: a historical perspective. Oxford University Press, 2017.

Bengio, Y., L´eonard, N., and Courville, A. C. Estimating or propagating gradients through stochastic neurons for conditional computation. CoRR, abs/1308.3432, 2013.

Berthet, Q., Blondel, M., Teboul, O., Cuturi, M., Vert, J., and Bach, F. R. Learning with differentiable perturbed optimizers. In Advances in Neural Information Processing Systems, volume 33, pp. 9508–9519, 2020.

Blondel, M., Seguy, V., and Rolet, A. Smooth and sparse optimal transport. In International Conference on Artificial Intelligence and Statistics, AISTATS 2018, 9-11 April 2018, Playa Blanca, Lanzarote, Canary Islands, Spain, pp. 880–889, 2018.

Blondel, M., Teboul, O., Berthet, Q., and Djolonga, J. Fast differentiable sorting and ranking. In Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event, pp. 950–959, 2020.

Blondel, M., Berthet, Q., Cuturi, M., Frostig, R., Hoyer,

S., Llinares-L´opez, F., Pedregosa, F., and Vert, J. Efficient and modular implicit differentiation. In Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022.

Bradbury, J., Frostig, R., Hawkins, P., Johnson, M. J., Leary,

C., Maclaurin, D., Necula, G., Paszke, A., VanderPlas, J., Wanderman-Milne, S., and Zhang, Q. JAX: composable transformations of Python+NumPy programs, 2018.

Bregman, L. The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming. USSR Computational Mathematics and Mathematical Physics, 7(3):200–217, 1967. ISSN 0041-5553. doi: https://doi.org/10.1016/ 0041-5553(67)90040-7.

Cuturi, M. Sinkhorn distances: Lightspeed computation of optimal transport. In Advances in Neural Information Processing Systems 26: 27th Annual Conference on Neural Information Processing Systems 2013. Proceedings of a meeting held December 5-8, 2013, Lake Tahoe, Nevada, United States, pp. 2292–2300, 2013.

Cuturi, M., Teboul, O., and Vert, J.-P. Differentiable rank- ing and sorting using optimal transport. In Wallach, H., Larochelle, H., Beygelzimer, A., d'Alch´e-Buc, F., Fox, E., and Garnett, R. (eds.), Advances in Neural Information Processing Systems, volume 32. Curran Associates, Inc., 2019.

<!-- Page 11 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Cuturi, M., Meng-Papaxanthos, L., Tian, Y., Bunne, C.,

Davis, G., and Teboul, O. Optimal transport tools (ott): A jax toolbox for all things wasserstein. arXiv preprint arXiv:2201.12324, 2022.

Duch, W. and Jankowski, N. Survey of neural transfer func- tions. Neural computing surveys, 2(1):163–212, 1999.

Flamary, R., Courty, N., Gramfort, A., Alaya, M. Z., Bois- bunon, A., Chambon, S., Chapel, L., Corenflos, A., Fatras, K., Fournier, N., Gautheron, L., Gayraud, N. T., Janati, H., Rakotomamonjy, A., Redko, I., Rolet, A., Schutz, A., Seguy, V., Sutherland, D. J., Tavenard, R., Tong, A., and Vayer, T. POT: Python optimal transport. Journal of Machine Learning Research, 22(78):1–8, 2021.

Flamary, R., Vincent-Cuaz, C., Courty, N., Gramfort, A.,

Kachaiev, O., Quang Tran, H., David, L., Bonet, C., Cassereau, N., Gnassounou, T., Tanguy, E., Delon, J., Collas, A., Mazelet, S., Chapel, L., Kerdoncuff, T., Yu, X., Feickert, M., Krzakala, P., Liu, T., and Fernandes Montesuma, E. Pot python optimal transport (version 0.9.5), 2024.

Funahashi, K.-I. On the approximate realization of continu- ous mappings by neural networks. Neural networks, 2(3): 183–192, 1989.

Grover, A., Wang, E., Zweig, A., and Ermon, S. Stochastic optimization of sorting networks via continuous relaxations. In 7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019, 2019.

Han, J. and Moraga, C. The influence of the sigmoid func- tion parameters on the speed of backpropagation learning. In International workshop on artificial neural networks, pp. 195–201. Springer, 1995.

Hendrycks, D. and Gimpel, K. Bridging nonlinearities and stochastic regularizers with gaussian error linear units. CoRR, abs/1606.08415, 2016.

Howell, T. Mujoco warp (mjwarp). https://github.

com/google-deepmind/mujoco_warp, March 2025. NVIDIA GPU Technology Conference (GTC).

Huang, G.-B., Chen, L., and Siew, C.-K. Universal ap- proximation using incremental constructive feedforward networks with random hidden nodes. IEEE Transactions on Neural Networks, 17(4):879–892, 2006a. doi: 10.1109/TNN.2006.875977.

Huang, G.-B., Zhu, Q.-Y., Mao, K., Siew, C.-K., Saratchan- dran, P., and Sundararajan, N. Can threshold networks be trained directly? IEEE Transactions on Circuits and Systems II: Express Briefs, 53(3):187–191, 2006b.

Jang, E., Gu, S., and Poole, B. Categorical reparameteriza- tion with gumbel-softmax. In 5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceed- ings, 2017.

Kerbl, B., Kopanas, G., Leimk¨uhler, T., and Drettakis, G. 3d gaussian splatting for real-time radiance field rendering. ACM Trans. Graph., 42(4):139:1–139:14, 2023. doi: 10. 1145/3592433.

Li, Y., Guo, Y., Zhang, S., Deng, S., Hai, Y., and Gu, S. Dif- ferentiable spike: Rethinking gradient-descent for training spiking neural networks. In Ranzato, M., Beygelzimer, A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.), Advances in Neural Information Processing Systems, volume 34, pp. 23426–23439. Curran Associates, Inc., 2021.

Lu, L., Shin, Y., Su, Y., and Em Karniadakis, G. Dying relu and initialization: Theory and numerical examples. Communications in Computational Physics, 28(5):1671–1706, June 2020. ISSN 1991-7120. doi: 10.4208/cicp.oa-2020-0165.

Maddison, C. J., Mnih, A., and Teh, Y. W. The concrete distribution: A continuous relaxation of discrete random variables. In 5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceedings, 2017.

Martins, A. F. T. and Astudillo, R. F. From softmax to sparsemax: A sparse model of attention and multi-label classification. In Proceedings of the 33nd International Conference on Machine Learning, ICML 2016, New York City, NY, USA, June 19-24, 2016, pp. 1614–1623, 2016.

Mhaskar, H. N. Neural networks for optimal approximation of smooth and analytic functions. Neural Computation, 8 (1):164–177, 1996. doi: 10.1162/neco.1996.8.1.164.

Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T.,

Ramamoorthi, R., and Ng, R. Nerf: Representing scenes as neural radiance fields for view synthesis. In Computer Vision - ECCV 2020 - 16th European Conference, Glas- gow, UK, August 23-28, 2020, Proceedings, Part I, pp. 405–421, 2020. doi: 10.1007/978-3-030-58452-8\ 24.

MuJoCo, T. MuJoCo XLA (MJX), 2024.

Niepert, M., Minervini, P., and Franceschi, L. Implicit MLE:

backpropagating through discrete exponential family distributions. In Advances in Neural Information Processing Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual, pp. 14567–14579, 2021.

<!-- Page 12 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J.,

Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., Kopf, A., Yang, E., DeVito, Z., Raison, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L., Bai, J., and Chintala, S. Pytorch: An imperative style, high-performance deep learning library. In Advances in Neural Information Processing Systems 32, pp. 8024– 8035. Curran Associates, Inc., 2019.

Paty, F. and Cuturi, M. Regularized optimal transport is ground cost adversarial. In Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event, pp. 7532–7542, 2020.

Paulus, A., Martius, G., and Musil, V. LPGD: A general framework for backpropagation through embedded optimization layers. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024, 2024.

Paulus, A., Geist, A. R., Schumacher, P., Musil, V., and

Martius, G. Hard contacts with soft gradients: Refining differentiable simulators for learning and control. CoRR, abs/2506.14186, 2025. doi: 10.48550/ARXIV. 2506.14186.

Paulus, M. B., Choi, D., Tarlow, D., Krause, A., and Mad- dison, C. J. Gradient estimation with stochastic softmax tricks. In Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020.

Petersen, F., Borgelt, C., Kuehne, H., and Deussen, O. Dif- ferentiable sorting networks for scalable sorting and ranking supervision. In Proceedings of the 38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event, pp. 8546–8555, 2021.

Petersen, F., Goldl¨uecke, B., Borgelt, C., and Deußen, O.

Gendr: A generalized differentiable renderer. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 3992–4001, 2022. doi: 10.1109/cvpr52688.2022.00397.

Pogancic, M. V., Paulus, A., Musil, V., Martius, G., and

Rol´ınek, M. Differentiation of blackbox combinatorial solvers. In 8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020, 2020.

Prillo, S. and Eisenschlos, J. M. Softsort: A continuous relaxation for the argsort operator. In Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event, pp. 7793– 7802, 2020.

Rader, J., Lyons, T., and Kidger, P. Optimistix: modular optimisation in jax and equinox. arXiv:2402.09983, 2024.

Rojas, R. The backpropagation algorithm. In Neural net- works: a systematic introduction, pp. 149–182. Springer, 1996.

Rol´ınek, M., Musil, V., Paulus, A., P., M. V., Michaelis,

C., and Martius, G. Optimizing rank-based metrics with blackbox differentiation. In 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2020, Seattle, WA, USA, June 13-19, 2020, pp. 7617–7627, 2020a. doi: 10.1109/CVPR42600.2020.00764.

Rol´ınek, M., Swoboda, P., Zietlow, D., Paulus, A., Musil,

V., and Martius, G. Deep graph matching via blackbox differentiation of combinatorial solvers. In Computer Vision - ECCV 2020 - 16th European Conference, Glasgow, UK, August 23-28, 2020, Proceedings, Part XXVIII, pp. 407–424, 2020b. doi: 10.1007/978-3-030-58604-1\ 25.

Rosenblatt, F. The perceptron, a perceiving and recognizing automaton:(Project Para). Cornell Aeronautical Laboratory, 1957.

Ruiz-Gonzalez, C., Arlt, S., Lehner, S., Berzins, A., Drori,

Y., Adhikari, R. X., Brandstetter, J., and Krenn, M. Neu- ral surrogates for designing gravitational wave detectors, 2025.

Sahoo, S. S., Paulus, A., Vlastelica, M., Musil, V., Kuleshov,

V., and Martius, G. Backpropagation through combinatorial algorithms: Identity with projection works. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023, 2023.

Sander, M. E., Puigcerver, J., Djolonga, J., Peyr´e, G., and

Blondel, M. Fast, differentiable and sparse top-k: a convex analysis perspective. In International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA, pp. 29919–29936, 2023.

Semenov, S. Smooth approximations of the rounding func- tion. CoRR, abs/2504.19026, 2025. doi: 10.48550/ ARXIV.2504.19026.

Stumm, P. and Walther, A. New algorithms for optimal on- line checkpointing. SIAM J. Sci. Comput., 32(2):836–854, March 2010. ISSN 1064-8275.

Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics engine for model-based control. In 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, pp. 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012. 6386109.

<!-- Page 13 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Wang, W. and Carreira-Perpi˜n´an, M. ´A. Projection onto the probability simplex: An efficient algorithm with a simple proof, and an application. CoRR, abs/1309.1541, 2013.

Wang, Y., Serena, F., Wu, S., ¨Oztireli, C., and Sorkine-

Hornung, O. Differentiable surface splatting for pointbased geometry processing. ACM Trans. Graph., 38(6): 230:1–230:14, 2019. doi: 10.1145/3355089.3356513.

Xie, Y., Dai, H., Chen, M., Dai, B., Zhao, T., Zha, H.,

Wei, W., and Pfister, T. Differentiable top-k with optimal transport. In Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M., and Lin, H. (eds.), Advances in Neural Information Processing Systems, volume 33, pp. 20520–20531. Curran Associates, Inc., 2020.

Yuen, B., Hoang, M. T., Dong, X., and Lu, T. Universal ac- tivation function for machine learning. Scientific reports, 11(1):18757, 2021.

<!-- Page 14 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

A. Library overview

Axiswise Elementwise Logical Selection Modes argmin heaviside logical and where ✓smooth min round logical or take along axis ✓c0 argsort sign logical xor take ✓c1 sort abs logical not choose ✓c2 argquantile relu any dynamic index in dim quantile clip all dynamic slice in dim Methods argmedian less dynamic slice ✓Optimal Transport median less equal ✓SoftSort top k equal ✓NeuralSort rank not equal ✓FastSoftSort isclose ✓SmoothSort ✓Sorting Network

**Figure 9.** Overview of all operators implemented in SoftJAX. Redundant operators such as max or greater have been omitted for brevity. Additionally, SoftJAX provides autograd-safe wrappers for common mathematical functions whose standard implementations produce NaN gradients at boundary points: sqrt, arcsin, arccos, div, log, and norm. These wrappers clamp gradients near singularities, making them safe for use in differentiable pipelines. SoftTorch provides the same operators using PyTorch naming conventions; see Table 1 for the mapping.

**Table 1.** Naming differences between SoftJAX and SoftTorch. SoftTorch follows PyTorch conventions. Functions listed as “—” are not

available in SoftTorch (no PyTorch equivalent).

SoftJAX SoftTorch clip clamp equal eq top k topk take along axis take along dim dynamic index in dim index select dynamic slice in dim narrow choose — dynamic slice —

<!-- Page 15 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

**Table 2.** Overview of algorithms used. While not all regularization methods are detailed in the literature for the various algorithm types, we derived the missing combinations by systematically combining the above-listed works.

Optimal transport smooth c0 (Blondel et al., 2018) c1/c2 (Paty & Cuturi, 2020) argmax (Cuturi et al., 2019) derived derived argsort (Cuturi et al., 2019) derived derived argquantile (Cuturi et al., 2019) derived derived argmedian (Cuturi et al., 2019) derived derived argtop k (Xie et al., 2020) derived derived rank (Cuturi et al., 2019) derived derived SoftSort smooth c0 c1/c2 argmax softmax (Martins & Astudillo, 2016) derived argsort (Prillo & Eisenschlos, 2020) derived derived argquantile (Prillo & Eisenschlos, 2020) derived derived argmedian (Prillo & Eisenschlos, 2020) derived derived argtop k (Prillo & Eisenschlos, 2020) derived derived rank derived derived derived NeuralSort smooth c0 c1/c2 argmax (Grover et al., 2019) derived derived argsort (Grover et al., 2019) derived derived argquantile (Grover et al., 2019) derived derived argmedian (Grover et al., 2019) derived derived argtop k (Grover et al., 2019) derived derived rank derived derived derived FastSoftSort smooth c0 c1/c2 sort (Blondel et al., 2020) (Blondel et al., 2020) (Sander et al., 2023) rank (Blondel et al., 2020) (Blondel et al., 2020) (Sander et al., 2023) SmoothSort smooth c0 c1/c2 sort novel — — rank novel — — Sorting network smooth c0 c1/c2 sort (Petersen et al., 2021) derived derived argsort (Petersen et al., 2021) derived derived

B. Case study: Collision detection in MuJoCo XLA

Mujoco (Todorov et al., 2012) is one of the most widely used simulators throughout robotics research. MuJoCo XLA (MJX) is a re-implementation of MuJoCo using JAX to enable GPU-parallelized automatic differentiation of robot simulations. Unfortunately, neither MuJoCo nor MJX are softly differentiable as emphasized by Paulus et al. (2025). To improve differentiability, Paulus et al. (2025) introduced soft relaxations of MuJoCo’s collision detection algorithms for simple primitives, i. e., sphere-plane and box-plane collisions. However, softening MuJoCo’s collision detection for mesh-mesh collisions is significantly more challenging as it involves numerous nested combinations of non-differentiable discrete operations. Alternatively, Beker et al. (2025; 2026) propose efficient soft collision detection via signed distance fields. To illustrate the utility of SoftJAX, we soften one of the key subroutines in MJX collision detection. The subroutine as shown in Figure 12 (left) chooses four vertices (A, B, C, D) from an ordered polygon that roughly maximize the contact patch area.

To render this algorithm smoothly differentiable, we convert it to SoftJax as shown in Figure 12 (right). For this, the following changes are made:

<!-- Page 16 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

**Figure 10.** Manifold points computed by the algorithm’s SoftJAX reimplementation over different softness values τ. While a small

softness causes the algorithm to choose points close to the vertices of the polygon, for large softness values, all four points collapse into a single point.

1. Replace discrete jnp.argmax with sj.argmax, which returns a “SoftIndex” distribution,

2. Replace indexing with sj.dynamic index in dim, which uses the “SoftIndex” as input,

3. Replace jnp.abs with sj.abs.

Note that the soft version returns “SoftIndex” distributions (shape: 4 x n) instead of the hard indices. The remaining code of the collision detection, therefore, needs to be adjusted accordingly.

Effect of smoothing on point selection and gradients. Figure 10 illustrates how the soft algorithm chooses four points from a seven-sided polygon as the softness parameter varies (computed as soft probs @ poly). For small softness values, the soft selection closely matches the hard algorithm. As softness increases, the selected points meet in a single point as the sj.argmax reduces to the computation of a mean, as also shown in Figure 11 (Left).

A key motivation for softening is to obtain informative gradients with respect to all function inputs. As shown in Figure 11 (Right), MJX’s hard version of manifold point selection always chooses four points out of the polygon’s five vertices such that for one polygon point, the gradient is null. In comparison, the algorithm’s soft re-implementation yields smooth, non-zero gradients at all vertices of the polygon (here deploying optimal transport with smooth regularization). Small softness values (e. g., τ = 0.01) cause the algorithm to select points similarly to its hard counterpart at the expense of increased gradient magnitudes (note the logarithmic y-axis). When small softness values are required in an application, we recommend to use gradient clipping to improve numerical stability.

Avoiding the STE pitfall. We could now directly use one of the relaxations as a differentiable proxy. However, oftentimes it is desirable not to alter the forward pass. For instance, in a physics simulation, we do not want to alter the forward physics. In these cases, we can resort to the straight-through trick, which means to replace only the gradient of a hard function on the forward pass with the gradient of the soft function on the backward pass. To avoid the STE pitfall, the straight-through trick is applied on the outer level of the downstream function, which calls the whole function twice instead of each of the primitives:

from softjax.straight_through import st manifold_points_softjax_st = st(manifold_points_softjax)

![Figure extracted from page 16](2026-ICML-softjax-softtorch-empowering-automatic-differentiation-libraries-with-informativ/page-016-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 17 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

0.17

0.00

0.10 point mean

MJX (hard) SoftJAX =0.01 SoftJAX =1.0

0.5 0.0 0.5 0.0

0.1 gradient

0.5 0.0 0.5 Applied x-perturbation xi

10 1

10 00 10 0

10 1

0.5 0.0 0.5

0.1

0.0

0.3 v0 v1 v2 v3 v4

**Figure 11.** Left: The manifold points mjx algorithm selects the four vertices of a polygon (here n = 5) that maximize the enclosed

area. In contrast, manifold points softjax selects the four points by computing an expectation using probability distributions over vertex indices. For small softness τ = 0.1, SoftJAX selects points similar to MJX. Right: Perturbing the x-position of an individual vertex vi by ∆xi changes the mean over all coordinates of the selected points. Notably, in the mode smooth with τ = 0.1 and τ = 1, the SoftJAX variant yields smooth gradients of the mean with respect to ∆xi. By contrast, MJX yields non-zero gradients solely for the vertices that have currently been selected by the algorithm.

def manifold_points_mjx(poly, poly_mask, poly_norm:

jnp.ndarray):

dist_mask = jnp.where(poly_mask, 0.0, -1e6) # Note: We add a small tie-breaker # A: select the most penetrating vertex a_logits = dist_mask - 0.1 * jnp.arange(poly.shape

[0]) a_idx = jnp.argmax(a_logits) a = poly[a_idx]

## B: farthest from A (largest squared distance) b_logits = ((a - poly) ** 2).sum(axis=1) + dist_mask b_idx = jnp.argmax(b_logits) b = poly[b_idx]

## C: farthest from the AB line within the plane ab = jnp.cross(poly_norm, a - b) ap = a - poly c_logits = jnp.abs(ap.dot(ab)) + dist_mask c_idx = jnp.argmax(c_logits) c = poly[c_idx]

## D: farthest from edges AC and BC ac = jnp.cross(poly_norm, a - c) bc = jnp.cross(poly_norm, b - c) bp = b - poly dist_bp = jnp.abs(bp.dot(bc)) + dist_mask dist_ap = jnp.abs(ap.dot(ac)) + dist_mask d_logits = dist_bp + dist_ap d_idx = jnp.argmax(d_logits) return jnp.array([a_idx, b_idx, c_idx, d_idx]) # Returns 4 vertex indices def manifold_points_softjax(poly, poly_mask, poly_norm

, softness: float = 0.1, mode: Literal["hard", " smooth"] = "smooth"): m, s = mode, softness dist_mask = jnp.where(poly_mask, 0.0, -1e6)

## A: soft argmax over masked distances a_logits = dist_mask - 0.1 * jnp.arange(poly.shape

[0]) a_idx = sj.argmax(a_logits, mode=m, softness=s) a = sj.dynamic_index_in_dim(poly, a_idx, axis=0, keepdims=False)

## B: soft argmax of distance from A b_logits = (((a - poly) ** 2).sum(axis=1)) + dist_mask b_idx = sj.argmax(b_logits, mode=m, softness=s) b = sj.dynamic_index_in_dim(poly, b_idx, axis=0, keepdims=False)

## C: soft argmax farthest from AB line ab = jnp.cross(poly_norm, a - b) ap = a - poly c_logits = sj.abs(ap.dot(ab), mode=m, softness=s)

+ dist_mask c_idx = sj.argmax(c_logits, mode=m, softness=s) c = sj.dynamic_index_in_dim(poly, c_idx, axis=0, keepdims=False)

## D: softargmax farthest from AC and BC ac = jnp.cross(poly_norm, a - c) bc = jnp.cross(poly_norm, b - c) bp = b - poly dist_bp = sj.abs(bp.dot(bc), mode=m, softness=s) + dist_mask dist_ap = sj.abs(ap.dot(ac), mode=m, softness=s) + dist_mask d_logits = dist_bp + dist_ap d_idx = sj.argmax(d_logits, mode=m, softness=s) return jnp.stack([a_idx, b_idx, c_idx, d_idx])

**Figure 12.** Left: Non-differentiable algorithm used by MJX for collision detection between mesh-mesh collisions. The algorithm chooses

four vertices from a polygon that form a quadrilateral with approximately largest area. Right: Softened version of MJX’s manifold point algorithm yielding informative gradients and returning four “SoftIndex” distributions.

<!-- Page 18 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

C. Input standardization and squashing

All axiswise operators in SoftJAX and SoftTorch optionally preprocess the input x ∈Rn via a standardize-and-squash transform, following Cuturi et al. (2019). This serves two purposes: (i) it maps x into [0, 1], matching the range of the grid-like target marginal y = 1 n−1[0,..., n−1]⊤used in optimal transport, improving numerical stability; and (ii) it makes the softness parameter τ independent of the scale of x.

Forward transform. Given the input x, we first standardize and then squash with the logistic sigmoid σ, i. e., µ = mean(x), s = std(x), ex = σ x −µ s

, (53)

where µ and s are computed along the specified axis. The transformed input ex ∈(0, 1)n is then passed to the axiswise operator.

Inverse transform. For value-returning operators (e. g., sort), the output ey ∈(0, 1)n is then mapped back to the original scale. For this we apply the inverse, by first unsquashing via the logit function, and then destandardizing, i. e., y = logit(ey) · s + µ, where logit(p) = log p 1−p. (54)

The exception is SmoothSort (Section 4.3), which skips standardize-and-squash. This is because it is the only method which can return values larger than the largest input element (or smaller than the smalles input element) as the output is not a convex combination of inputs. Hence with standardize-and-squash, the output would not always be in the interval (0, 1), which can lead to undefined outputs of the unsquashing operation.

D. Extended Axiswise Operators

D.1. Solving Optimization Problems

Optimal transport. In SoftJAX, for smooth-mode OT, we use Sinkhorn iterations implemented via ott-jax (Cuturi et al., 2022) by default. Alternatively, L-BFGS as suggested in (Blondel et al., 2018), implemented via the Optimistix library (Rader et al., 2024), can be used. For c0, c1, and c2 modes, we solve the dual OT problems (see Section D.2 for their formulations) using L-BFGS via Optimistix. Both libraries support implicit differentiation, which reduces memory usage and enables adaptive stopping criteria for optimization loops. In SoftTorch, we solve the optimal transport problems using POT (Flamary et al., 2021; 2024).

Projection onto the unit simplex. In smooth mode, this reduces to a simple call to a softmax function. In c0 mode, we use the well-known O(n log n) algorithm of (Wang & Carreira-Perpi˜n´an, 2013). For c1 and c2 modes, we derive closed-form solutions to the Bregman projection onto the unit simplex (Bregman, 1967), namely a quadratic formula for p = 3/2 (c1) and Cardano’s method for p = 4/3 (c2), both running in O(n log n).

Projection onto the permutahedron. We follow (Blondel et al., 2020), who reduce the Euclidean and log-KL projections onto the permutahedron to isotonic optimization, which is in turn solved in O(n log n) via the pool adjacent violators (PAV) algorithm.

For SoftJAX, we reimplement the PAV algorithm in pure JAX, as the original NumPy code is incompatible with jax.vmap/jax.jit. In SoftTorch, we rely Numba-JIT for acceleration.

Moreover, we extend FastSoftSort to p-norm regularization following Sander et al. (2023). Note, that Sander et al. (2023) solve the PAV subproblem via bisection, we replace this with closed-form solutions to a quadratic formula for c1 and Cardano’s method for c2.

For SmoothSort (Section 4.3) we solve the dual of the entropically-regularized LP via L-BFGS (Rader et al., 2024). A custom VJP on the solver computes gradients via an adjoint saddle-point system. Note that SmoothSort is currently SoftJAX only.

<!-- Page 19 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

D.2. Dual OT Problems

For marginals a ∈∆n, b ∈∆m, cost matrix C ∈Rn×m, and dual potentials f ∈Rn, g ∈Rm, the dual of the entropy-regularized OT problem can be written as max f∈Rn,g∈Rm⟨f, a⟩+ ⟨g, b⟩−τ

X ij exp fi + gj −Cij τ

. (55)

and the corresponding optimal primal solution can be recovered via

(Γ⋆ τ)ij = exp f ⋆ i + g⋆ j −Cij τ

. (56)

The dual of the Euclidean regularized OT problem can be written as max f∈Rn,g∈Rm⟨f, a⟩+ ⟨g, b⟩−1

2τ

X ij fi + gj −Cij

2

+ (57)

and the corresponding optimal primal solution can be recovered via

(Γ⋆ τ)ij = 1 τ f ⋆ i + g⋆ j −Cij

+. (58)

The dual of the p-norm regularized OT problem can be written as max f∈Rn,g∈Rm⟨f, a⟩+ ⟨g, b⟩−τ 1−q q

X ij fi + gj −Cij q

+, (59)

where q = p p−1. The corresponding optimal primal solution can be recovered via

(Γ⋆ τ)ij = f ⋆ i + g⋆ j −Cij τ

1 p−1

+. (60)

D.3. Elementwise Operators as Special Case

While elementwise and axiswise soft operators are treated as distinct categories in the main text, they are closely related. Specifically, the elementwise soft surrogates described in Section 3 can be recovered as special cases of the axiswise operators when n = 2. Here, we demonstrate that applying axiswise operators to a two-element vector x = [0, x]⊤yields the soft Heaviside functions derived earlier. To distinguish the mode-specific sigmoidals in this section, we introduce superscripts for the smoothness class. The smooth mode is H∞ τ (x):= σ(x/τ) = ex/τ/(1 + ex/τ). All piecewise modes share the structure

Hk τ(x):=

  

 

0 if x < −τ, gk(x/τ) if |x| ≤τ, 1 if x > τ,

(61)

with interpolation functions gk: [−1, 1] →[0, 1]

g0(s) = 1

2 + s 2, (c0, piecewise linear, C0) (62)

g1(s) = 1

2 + 3s 4 −s3 4, (c1, Hermite cubic, C1) (63)

g2(s) = 1

2 + 15s 16 −5s3 8 + 3s5 16. (c2, Hermite quintic, C2) (64)

The p-norm simplex projections at n=2 yield distinct C1 and C2 sigmoidals, which we denote eH

1 τ, eH

2 τ (same piecewise structure with egk replacing gk)

eg1(s) = s +

√

2 −s2 2

4, (p=3/2 p-norm, C1) (65)

eg2(s) = (t + s/2)3, t = −|s| sinh

1

3 arcsinh −2 s2|s|

. (p=4/3 p-norm, C2) (66)

These smoothness classes are confirmed for general n in Theorem 1.

<!-- Page 20 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Reduction of Soft Argmax Consider the soft argmax operator applied to x = [0, x]⊤. The output is a probability distribution p ∈∆2 over the indices. Since p0 + p1 = 1, the distribution is fully characterized by p1, which is a sigmoidal function of x/τ for each regularizer, i. e., arg maxτ([0, x]⊤) =

1 −p1, p1 ⊤. (67)

For entropic regularization, arg max reduces to the standard softmax, and hence we recover the sigmoid p1 = σ(x/τ) = H∞ τ (x). (68)

For p-norm regularization, the projection of [0, x]⊤onto the unit simplex solves arg minp∈∆2 −⟨[0, x]⊤, p⟩+ τ p

P i pp i.

With p = 2 (c0 mode), the first-order condition gives p1 = 1

2 + x 2τ = H0 τ(x), (69)

directly recovering the elementwise c0 sigmoidal.

With p = 3/2 (c1 mode), we get the first-order condition √p1 −√1−p1 = x/τ, which can be solved via the quadratic formula by p1 = eH

1 τ(x). This is another sigmoidal function in C1 with p′

1 = 0 at x = ±τ.

With p = 4/3 (c2 mode), we get the first-order condition p1/3

1 −(1−p1)1/3 = x/τ, which reduces to a depressed cubic.

That can be solved by Cardano’s formula, giving p1 = eH

2 τ(x). This is yet another sigmoidal function in C2. Note that H1, H2 are not special cases of an axiswise operator, but provide the same smoothness guarantees with simpler expressions.

Theorem 1 confirms that the C1 and C2 smoothness classes of eH

1 τ and eH

2 τ extend to the general n-dimensional simplex and transport polytope projections.

Reduction of Soft Sort and OT Similarly, we can analyze the behavior of soft sorting and optimal transport for n = 2. Let the input be x = [0, x]⊤with sorted anchors y = [0, 1]⊤and balanced marginals a = b = [ 1

2, 1 2]⊤. The cost matrix is denoted as Cij = (xi −yj)2. The OT solution then takes the form

P ⋆ τ = p1 1 −p1 1 −p1 p1

, Γ = P/2, (70)

which only leaves one degree of freedom p1 ∈[0, 1]. The cost simplifies to ⟨C, Γ⟩= 1+x2

2 −xp1, hence the regularized OT problem reduces to a scalar optimization in p1.

For entropy-regularized OT, the first-order condition log p1/(1−p1)

= x/τ gives p1 = σ(x/τ) = H∞ τ (x), (71)

recovering the logistic sigmoid, identical to the simplex projection in the previous paragraph. For Euclidean regularization (p=2), the first-order condition yields p1 = 1

2 + x/τ = H0 τ/2(x), (72)

matching the simplex result H0 τ(x) up to a factor of 2 in softness. For p=3/2, the first-order condition gives

√p1 − p

1 −p1 = √

2 x/τ, (73)

and for p=4/3, p1/3

1 −(1 −p1)1/3 = 21/3 x/τ, (74)

recovering the results of the previous paragraph up to softness scaling as eH

1 τ/

√

2(x) and eH 2 τ/ 3√

2(x), respectively.

<!-- Page 21 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

Softness convention. In our sigmoidal definitions, the piecewise polynomial modes (Equation (6)) transition from zero to one on the interval [−τ, τ]. In contrast, the smooth mode reaches near-saturation only at ≈±5τ. Therefore, we introduce a scaling factor for the piecewise polynomial modes as g(x/(5τ)), which widens their transition to [−5τ, 5τ], matching that of the smooth mode.

For axiswise operators, we do not add any mode-dependent scaling constants. As a result, the same τ value produces different effective softness across modes and problem sizes n for axiswise operators. For users needing comparable behavior across modes or sizes, we recommend measuring the normalized entropy H(P)/ log n of the soft permutation matrix and calibrating τ accordingly.

D.4. Smoothness of p-norm Regularized Projections

The preceding section verifies the smoothness classes C1 and C2 of the p-norm sigmoidals eH

1 τ and eH

2 τ for n = 2. We now prove that these smoothness classes hold for the general n-dimensional simplex projection and for the p-norm regularized optimal transport plan.

Theorem 1 (Smoothness of p-norm regularized projections). Let n ≥2, 1 < p ≤2, τ > 0, and let q = p/(p−1) be the conjugate exponent with q a positive integer. Define k:= q −2.

(i) Unit simplex. The p-norm regularized projection Πτ: Rn →∆n,

Πτ(x):= arg max p∈∆n

⟨x, p⟩−τ p∥p∥p p, (75)

is a Ck map. For entropic regularization P j pj log pj, the projection Πτ is C∞.

(ii) Transport polytope. For m ≥2, marginals a ∈∆n, b ∈∆m and cost matrix C ∈Rn×m, the p-norm regularized optimal transport plan

Γ⋆ τ(C):= arg min

Γ∈U(a,b)

⟨Γ, C⟩+ τ p

X ij

|Γij|p (76)

is a Ck map of C at every cost matrix for which the support {(i, j): Γ⋆ ij > 0} forms a connected bipartite graph. For entropic regularization P ij Γij(log Γij −1), the transport plan Γ⋆ τ is a C∞map of C unconditionally, since the support is always the full bipartite graph.

Moreover, the bound Ck is sharp: Πτ is not Ck+1, and Γ⋆ τ is not Ck+1. In particular, c0 (p=2) gives C0, c1 (p=3/2) gives C1, c2 (p=4/3) gives C2, and smooth gives C∞.

Since the cost matrix in the sorting application is Cij = (xi −yj)2, which is C∞in x, the transport plan Γ⋆ τ inherits the same Ck regularity as a function of the input x by the chain rule. The connectivity condition is generically satisfied, i. e., it holds for all cost matrices outside a set of measure zero.

Proof. The proof is based on the implicit function theorem applied to the optimality conditions of the optimization problems. Both parts rely on the positive-part power function, defined as φ: R →[0, ∞) by φ(t):= (t/τ)k+1

+, of which all derivatives up to order k exist and are continuous, therefore φ ∈Ck(R).

Part (i): Unit simplex. The KKT conditions for the simplex-constrained problem are xi −τ(p⋆ i)p−1 −ν + µi = 0, 1 ≤i ≤n, (77)

n X i=1 p⋆ i = 1, (78)

p⋆ i ≥0, µi ≥0, µi p⋆ i = 0, (79)

where ν is the multiplier for the equality constraint 1⊤p = 1 and µi are the multipliers for the non-negativity constraints. When p⋆ i > 0, complementary slackness gives µi = 0, so the stationarity condition reduces to p⋆ i = ((xi −ν)/τ)1/(p−1) =

<!-- Page 22 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients φ(xi −ν). When p⋆ i = 0, the stationarity condition gives µi = ν −xi ≥0, i. e., xi ≤ν. In both cases p⋆ i = φ(xi −ν), and substituting into the equality constraint yields n X i=1 φ(xi −ν) = 1. (80)

Define h: R × Rn →R by h(ν, x):= Pn i=1 φ(xi −ν) −1. As a finite sum of translates of φ, the function h is Ck in (ν, x). The partial derivative with respect to ν is

∂h ∂ν = − n X i=1 φ′(xi −ν), (81)

which is strictly negative at any (ν, x) satisfying h = 0. Indeed, P i φ(xi −ν) = 1 > 0 implies that at least one index i has xi > ν, and for any such index φ′(xi −ν) > 0.

For k ≥1 (i. e., p < 2), the Implicit Function Theorem for Ck maps yields that ν is a Ck function of x. Furthermore, the implicit ν(x) is unique and globally defined, since h(·, x) is strictly decreasing (it satisfies ∂h/∂ν < 0 at every root). Each component p⋆ i (x) = φ(xi −ν(x)) is then Ck as a composition of Ck functions, establishing Πτ ∈Ck. For entropic regularization, Πτ(x) = exp(x/τ)/ P j exp(xj/τ), which is C∞.

Part (ii): Transport polytope. The argument follows the same structure as Part (i). From the dual formulation (Section D.2), the optimal transport plan satisfies Γ⋆ ij = φ(f ⋆ i + g⋆ j −Cij), where (f ⋆, g⋆) are the dual potentials. The marginal constraints P j φ(fi + gj −Cij) = ai and P i φ(fi + gj −Cij) = bj define, after fixing gm = 0 to break the shift symmetry, a Ck implicit system of n + m −1 equations in n + m −1 unknowns. The Jacobian is non-singular if and only if the bipartite support graph {(i, j): Γ⋆ ij > 0} is connected, which is the standard non-degeneracy condition for optimal transport. Under this condition, the implicit function theorem gives Γ⋆ τ(C) ∈Ck. For entropic regularization, Γ⋆ ij = exp((f ⋆ i +g⋆ j −Cij)/τ) > 0 for all (i, j), so the support is always connected and the same argument yields Γ⋆ τ ∈C∞.

Sharpness. For any n ≥2, restricting Πτ to inputs of the form x = (x1, x2, −M,..., −M) with M large enough that only the first two components are active reduces the projection to the n = 2 case. The preceding section shows that this two-dimensional projection is the sigmoidal p1 = eH k τ(x), whose (k+1)-th derivative is discontinuous at |x| = τ. Since this is a restriction of Πτ, the full map cannot be Ck+1. The same embedding applies to Γ⋆ τ via the n = m = 2 reduction shown in the preceding section.

D.5. Gating- vs Integration-like behavior of axiswise operators

In the main text, we have seen that there are two principled ways to get a soft relu surrogate from a soft sigmoidal, either by integration reluτ(x):=

Z x

0 Hτ(t) dt, (82)

which, in the case of the smooth regularizer, is simply a Softplus function, or via a gating mechanism reluτ(x):= Hτ(x) · x, (83)

which, in the case of an entropic regularizer, is simply a SiLU function,

We now observe that a similar mechanism is at play for axiswise operators: To get a soft surrogate for the sort operator, we “gate” the argsort operator with the input, i.e.

sortτ(x):= arg sortτ(x)x = P ⋆ τ (x) x. (84)

Intuitively, this means that the sort operator defined in this way behaves qualitatively similar to the SiLU function, which has a characteristic minimum, in contrast to the monotonically increasing Softplus function.

<!-- Page 23 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

A natural question is whether a version of the sort operator exists that behaves similarly to the Softplus function. Unfortunately, this would require integrating the multivariate argsort function. However, we are often anyway mainly interested in the gradient of the soft sort surrogate, while leaving the forward pass hard via straight-through estimation. The gradient (or, more precisely, the Jacobian) is extremely simple to compute. It is the function we would integrate, i. e., the argsort operator matrix.

In code, similar to the straight-through trick, we can manipulate our sort implementation to return the Jacobian of the integration-style version by using a stop-gradient operation on the argsort operator, i. e., soft_idx = jax.lax.stop_gradient(sj.argsort(x)) sorted_values = sj.take_along_axis(x, soft_idx)

This option is available via a simple flag, and it can be easily combined with straight-through estimation to get the hard forward pass and integration-style backward pass, e. g., sorted_values_st = sj.sort_st(x, gated_grad=False)

D.6. Entropy-regularized dual of permutahedron projection

Primal LP. The optimization problem over the permutahedron as stated in the main text is given by max p∈P(z)⟨y, p⟩. (85)

We can equivalently characterize the permutahedron constraint p ∈P(z) through a set of majorization inequalities k X i=1 p↓ i ≤ k X i=1 z↓ i ∀k: 1 ≤k < n (86)

and the sum equality n X i=1 pi = n X i=1 zi, (87)

where p↓and z↓are sorted in descending order.

Reduction to ordered cone. W.l.o.g., we can restrict the search space to ordered p by enforcing pi ≥pi+1 ∀i: 1 ≤i < n (88)

and then reorder the optimal solution back via the inverse permutation that sorts z. Crucially, on the ordered cone, the majorization inequalities become linear in p k X i=1 pi ≤ k X i=1 z↓ i ∀k: 1 ≤k < n. (89)

We can therefore rewrite the permutahedron LP as max p∈Rn⟨y↓, p⟩ subject to Ap ≤b

1⊤p = c

Dp ≥0,

(90)

<!-- Page 24 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients where we used A ∈R(n−1)×n, b ∈R(n−1), c ∈R, D ∈R(n−1)×n, defined as

(Ap)k:= k X i=1 pi ∀1 ≤k < n (91)

bk:= k X i=1 z↓ i ∀1 ≤k < n (92)

c:= n X i=1 zi (93)

(Dp)i:= pi −pi+1 ∀1 ≤i < n. (94)

Smoothing. The LP above is non-smooth in two ways. First, computing the majorization bounds bk = Pk i=1 z↓ i requires sorting z, which is not a smooth operation. Second, the LP itself is a linear program whose solution jumps between vertices. We address both by (i) replacing b with a smooth relaxation eb, and (ii) adding entropic regularization on the inequality slack variables.

For the bounds, we can rewrite bk as an optimization problem over subsets of indices, i. e., bk = k X i=1 z↓ i = max

S⊆[n] |S|=k

X i∈S zi. (95)

We can then replace the hard maximum with a log-sum-exp, which leads to a smooth relaxation, i. e., ebk:= τ log

X

S⊆[n] |S|=k exp

1 τ

X i∈S zi

= τ log ek ez/τ

, (96)

where ek(x) = P

|S|=k

Q i∈S xi sums all products of k distinct elements from x. In the limit τ →0+, we have ebk →bk.

Since en(x) = Q i xi, we directly get ebn = P i zi = c thereby preserving the equality constraint. Note also that the relaxed bounds satisfy ebk ≥bk, so the feasible set is a slight superset of the true permutahedron.

We next explain how the smoothed bounds can be computed in practice. For this we use the recurrence

E(j)

0 = 1, E(0)

k = 0 for k ≥1, (97)

E(j)

k = E(j−1)

k + ezj/τ · E(j−1)

k−1, (98)

where E(j)

k = ek(ez1/τ,..., ezj/τ). This requires O(n2) time runtime. Note that we work in log-space (logaddexp) for numerical stability and use optimal online checkpointing (Stumm & Walther, 2010) to reduce memory from O(n2) to O(n√n).

In order to smoothen the LP, we introduce slack variables and add entropic regularization onto them using ϕ(t) = t log(t)−t, i. e., max p∈Rn,s∈Rn−1,d∈Rn−1⟨y↓, p⟩−τ n−1 X k=1 ϕ(sk) −τ n−1 X i=1 ϕ(di)

subject to Ap + s = eb

1⊤p = c

Dp = d.

(99)

Dual problem and solution recovery. The smoothed primal problem has the dual problem min α∈Rn−1,β∈Rn−1,ν∈R⟨α, eb⟩+ νc + τ n−1 X k=1 e−αk/τ + τ n−1 X i=1 e−βi/τ subject to y↓−A⊤α + D⊤β −ν1 = 0.

(100)

<!-- Page 25 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

We now proceed by first eliminating ν via the equality constraint

0 = (y↓+ D⊤β −ν1)n ⇒ν(β) = y↓ n + (D⊤β)n. (101)

Now we define u(β) = y↓+ D⊤β −ν(β)1, (102)

which satisfies un(β) = 0. Note that have u(β) = A⊤α, which means αk(β) = uk(β) −uk+1(β) ∀k: 1 ≤k < n. (103)

Finally, substituting (αk(β), ν(β)) into the dual gives an unconstrained optimization problem over β, which we can solve via L-BFGS.

In tha last step we recover the primal solution from the dual solution (α⋆, β⋆, ν⋆). This is done via s⋆= exp(−α⋆/τ) (104)

d⋆= exp(−β⋆/τ) (105)

and p⋆is recovered by first defining prefix sums rk:= ebk −s⋆ k = k X i=1 p⋆ i ∀k: 1 ≤k < n, (106)

and then computing p⋆by differencing p⋆

1 = r1 (107)

p⋆ k = rk −rk−1 ∀k: 2 ≤k < n (108)

p⋆ n = c −rn−1. (109)

Backward pass. The solver uses a custom VJP that solves an adjoint system via conjugate gradients, with O(n) cost per iteration due to the banded structure of the LP constraints. Gradients through the smooth bounds use standard reverse-mode autodiff through Equation (96).

E. Additional Benchmark Experiments

We include additional benchmarking experiments for elementwise operators (Figure 13) and axiswise operators (Figures 14 to 20). Each figure shows runtime, JIT compilation time, and peak memory consumption as a function of input array size, broken down by regularization mode (smooth, c0, c1, c2).

<!-- Page 26 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

2×10−1

3×10−1

4×10−1 sign

Time (ms)

102

## 103 JIT

Time (ms)

10−1

100

101

102

Memory (KB)

2×10−1

3×10−1

4×10−1 abs

102

103

10−1

100

101

102

2×10−1

3×10−1

4×10−1 relu

102

103

10−1

100

101

102

2×10−1

3×10−1

4×10−1 round

102

103

10−1

100

101

102

2×10−1

3×10−1

4×10−1 clip

102

103

10−1

100

101

102

2×10−1

3×10−1

4×10−1 greater

102

103

10−1

100

101

102

22 24 28 210 212

Array Size

2×10−1

3×10−1

4×10−1 equal

22 24 28 210 212

Array Size

102

103

22 24 28 210 212

Array Size

10−1

100

101

102 hard Smooth C0 C1 C2

**Figure 13.** Benchmark results for elementwise operators.

<!-- Page 27 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

101

104

Smooth

Time (ms)

103

## 104 JIT

Time (ms)

102

105

108 Memory (KB)

101

104

C0

103

104

102

105

108

101

104

C1

103

104

102

105

108

26 28 210 212

Array Size

101

104

C2

26 28 210 212

Array Size

103

104

26 28 210 212

Array Size

102

105

108

Hard OT SoftSort NeuralSort FastSoftSort SmoothSort SortingNet

**Figure 14.** Benchmark results for sj.sort.

101

104

Smooth

Time (ms)

103

104

JIT Time (ms)

102

105

108 Memory (KB)

101

104

C0

103

104

102

105

108

101

104

C1

103

104

102

105

108

26 28 210 212

Array Size

101

104

C2

26 28 210 212

Array Size

103

104

26 28 210 212

Array Size

102

105

108

Hard OT SoftSort NeuralSort SortingNet

**Figure 15.** Benchmark results for sj.argsort.

<!-- Page 28 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

101

103

Smooth

Time (ms)

103

104

JIT Time (ms)

101

103

105

Memory (KB)

101

103

C0

103

104

101

103

105

101

103

C1

103

104

101

103

105

26 210 212

Array Size

101

103

C2

26 210 212

Array Size

103

104

26 210 212

Array Size

101

103

105

Hard OT SoftSort NeuralSort FastSoftSort SmoothSort SortingNet

**Figure 16.** Benchmark results for sj.max.

100

102

104

Smooth

Time (ms)

103

## 104 JIT

Time (ms)

101

103

105

Memory (KB)

100

102

104

C0

103

104

101

103

105

100

102

104

C1

103

104

101

103

105

26 210 212

Array Size

100

102

104

C2

26 210 212

Array Size

103

104

26 210 212

Array Size

101

103

105

Hard OT SoftSort NeuralSort FastSoftSort SmoothSort SortingNet

**Figure 17.** Benchmark results for sj.top k.

<!-- Page 29 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

101

103

Smooth

Time (ms)

103

## 104 JIT

Time (ms)

102

104

Memory (KB)

101

103

C0

103

104

102

104

101

103

C1

103

104

102

104

26 28 210 212

Array Size

101

103

C2

26 28 210 212

Array Size

103

104

26 28 210 212

Array Size

102

104

Hard OT SoftSort NeuralSort FastSoftSort SmoothSort SortingNet

**Figure 18.** Benchmark results for sj.median.

101

103

105

Smooth

Time (ms)

103

104

JIT Time (ms)

102

105

108 Memory (KB)

101

103

105

C0

103

104

102

105

108

101

103

105

C1

103

104

102

105

108

26 28 210 212

Array Size

101

103

105

C2

26 28 210 212

Array Size

103

104

26 28 210 212

Array Size

102

105

108

Hard OT SoftSort NeuralSort FastSoftSort SmoothSort SortingNet

**Figure 19.** Benchmark results for sj.rank.

<!-- Page 30 -->

SoftJAX & SoftTorch: Empowering Automatic Differentiation Libraries with Informative Gradients

101

103

Smooth

Time (ms)

103

104

JIT Time (ms)

102

105

Memory (KB)

101

103

C0

103

104

102

105

101

103

C1

103

104

102

105

26 28 210 212

Array Size

101

103

C2

26 28 210 212

Array Size

103

104

26 28 210 212

Array Size

102

105

Hard OT SoftSort NeuralSort SortingNet

**Figure 20.** Benchmark results for sj.argmax.
