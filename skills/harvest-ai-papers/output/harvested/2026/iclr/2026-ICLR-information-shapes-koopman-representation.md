---
title: "Information Shapes Koopman Representation"
source_url: https://iclr.cc/virtual/2026/oral/10009364
paper_pdf_url: https://arxiv.org/pdf/2510.13025v2
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Information Shapes Koopman Representation

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

INFORMATION SHAPES KOOPMAN REPRESENTATION

Xiaoyuan Cheng1∗ Wenxuan Yuan2∗ Yiming Yang1 Yuanzhao Zhang3

Sibo Cheng4 Yi He1 Zhuo Sun5,6†

1Dynamic Systems Lab, University College London 2Department of Earth Science and Engineering, Imperial College London 3Santa Fe Institute 4CEREA, ENPC and EDF R&D, Institut Polytechnique de Paris 5School of Statistics and Data Science, Shanghai University of Finance and Economics 6Institute of Big Data Research, Shanghai University of Finance and Economics ∗Xiaoyuan Cheng and Wenxuan Yuan contributed equally to this work.

## ABSTRACT

The Koopman operator provides a powerful framework for modeling dynamical systems and has attracted growing interest from the machine learning community. However, its infinite-dimensional nature makes identifying suitable finitedimensional subspaces challenging, especially for deep architectures. We argue that these difficulties come from suboptimal representation learning, where latent variables fail to balance expressivity and simplicity. This tension is closely related to the information bottleneck (IB) dilemma: constructing compressed representations that are both compact and predictive. Rethinking Koopman learning through this lens, we demonstrate that latent mutual information promotes simplicity, yet an overemphasis on simplicity may cause latent space to collapse onto a few dominant modes. In contrast, expressiveness is sustained by the von Neumann entropy, which prevents such collapse and encourages mode diversity. This insight leads us to propose an information-theoretic Lagrangian formulation that explicitly balances this tradeoff. Furthermore, we propose a new algorithm based on the Lagrangian formulation that encourages both simplicity and expressiveness, leading to a stable and interpretable Koopman representation. Beyond quantitative evaluations, we further visualize the learned manifolds under our representations, observing empirical results consistent with our theoretical predictions. Finally, we validate our approach across a diverse range of dynamical systems, demonstrating improved performance over existing Koopman learning methods. The implementation is publicly available at https://github.com/Wenxuan52/InformationKoopman.

## INTRODUCTION

Modeling and predicting the behavior of nonlinear dynamical systems are fundamental problems in science and engineering (Brunton et al., 2020; Kovachki et al., 2023; Mezic, 2020). Classical approaches typically rely on nonlinear differential equations or black-box learning methods. In contrast, the Koopman operator framework offers a compelling alternative: it represents nonlinear evolution as a linear transformation in an appropriate function space (Koopman, 1931; Fritz, 1995).

Motivation. This linearization principle has recently attracted significant attention in the deep learning community, as it enables complex nonlinear dynamics to be modeled and predicted using linear representations. However, integrating this framework into deep architectures poses a fundamental challenge: the Koopman operator is inherently infinite-dimensional, necessitating the identification or learning of a suitable finite-dimensional subspace for practical implementation. Deep learning models, most notably variational autoencoders (VAEs), have been employed to approximate such

∗Email Xiaoyuan Cheng and Wenxuan Yuan to ucesxc4@ucl.ac.uk and wenxuan.yuan@qq.com. †Corresponding Author. Corresponding to Zhuo Sun: sunzhuo@mail.shufe.edu.cn.

arXiv:2510.13025v2 [cs.LG] 4 Feb 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026 subspaces in a purely data-driven manner (Otto & Rowley, 2019; Pan & Duraisamy, 2020; Liu et al., 2023). Yet in practice, the resulting representations often suffer from instability, mode collapse or fail to produce reliable dynamics. To address these challenges, some studies incorporate domain-specific priors—such as symmetry, conservation laws, dissipation, or ergodicity (Vaidya & Mehta, 2008; Weissenbacher et al., 2022; Azencot et al., 2020; Cheng et al., 2025)—into the Koopman representation. While effective in restricted settings, such approaches lack general principles for guiding Koopman representation. This calls for a more general and principled approach to constructing finite-dimensional representations, one that balances simplicity, in the form of latent linearity, with sufficient expressiveness (more literature review in Appendix C).

Information Bottleneck View. A natural way to achieve the tradeoff between simplicity and expressiveness is through the lens of the Information Bottleneck (IB). The classic IB framework formalizes the idea that a good representation should compress the input as much as possible while preserving information relevant to a downstream task (Tishby et al., 2000; Tishby & Zaslavsky, 2015). In the context of representation learning (see Table 1), this typically means finding a latent variable z that minimizes Complexity(x, z)1 from input x, while retaining expressiveness by improving Relevance(z, y) (Vera et al., 2018). Instead of a static latent representation, the goal of Koopman representation is to predict the future state xn given the current state xn−1 via a latent variable zn−1. This gives rise to a dynamical information bottleneck formulation: we aim to learn a Koopman representation zn−1 with maximal linear predictability of future state xn, while remaining as compact as possible.

**Table 1.** Information-theoretic comparison between standard and Koopman representations. Here, β controls the trade-off between simplicity and future-state expressiveness.

Latent Representation Koopman Representation Goal Disentangled z Predictive zn−1 Info. Flow x→z →y xn−1 →zn−1

Koopman operator −−−−−−−−→zn →xn Lagrangian β Complexity(x, z) −Relevance(z, y) β Complexity(xn−1, zn−1) −Relevance(zn−1, xn)

Why Is Finding a Good Koopman Representation Challenging? Learning Koopman representation imposes stricter constraints than conventional latent representation models (see Table 1). In VAE or β−VAE (Kingma et al., 2013; Burgess et al., 2018), the focus is on reconstructing the input x or sampling from its distribution, which only requires the latent representation z to contain enough information about y. However, in Koopman learning, the latent space needs to support linear forward from zn to zn+1 in some finite-dimensional spaces. This constraint implies that the latent representation must not only capture information about the current state but also conform to a linear predictive structure (structural consistency) (Mardt et al., 2018; Kostic et al., 2023a;b; 2024), which imposes a stronger restriction. Prior work has shown that simply increasing the dimensions of the latent space does not necessarily improve performance (Li et al., 2020; Brunton et al., 2021), underscoring the importance of maintaining temporal coherence, i.e., ensuring that latent trajectories evolve consistently over time to prevent instability and error accumulation. Moreover, predictive sufficiency requires that the latent representation retains enough Koopman modes to faithfully reconstruct the system’s future trajectories, such that multi-step prediction accuracy is preserved (Wang et al., 2022; 2025). Unlike standard VAEs and their variants, which emphasize flexible latent representations to support reconstruction, Koopman models demand dynamically consistent latent representations: small deviations can propagate and amplify over time. In summary, while conventional representation learning emphasizes disentanglement and reconstruction, Koopman representation learning requires three key properties: temporal coherence, predictive sufficiency, and structural consistency. The IB framework provides a meta view to navigate these trade-offs. It enables us to ask the central question:

Is it possible to learn Koopman representations that are both structurally simple and expressive, under the guidance of information-theoretic principles?

Motivated by this question, we approach the problem from a fresh IB perspective, leading to core contributions: Theoretical Insight. We develop an information-theoretic framework for Koopman representation, proving that mutual information controls error bounds while von Neumann entropy

1By Complexity(x, z) we mean the mutual information I(x; z) in the IB framework, quantifying how much of the input information x is retained in z. Relevance(z, y) denotes I(z; y), the information z carries about y.

<!-- Page 3 -->

Published as a conference paper at ICLR 2026 determines the effective dimension. By disentangling the information content of Koopman representations, we reveal how temporal coherence, predictive sufficiency, and structural consistency are governed by latent information and how these components are intrinsically connected to the spectral properties of the Koopman operator. This yields a novel information-theoretic Lagrangian that extends the classical IB principle by explicitly incorporating dynamical constraints, thereby making the fundamental trade-off between simplicity and expressivity in Koopman representation mathematically explicit. Principled Framework. Building on our information-theoretic Lagrangian, we derive a tractable, architecture-agnostic loss function that translates our theory into a practical algorithm. Each term of the loss corresponds directly to one of the three desiderata—temporal coherence, predictive sufficiency, and structural consistency. This yields a general algorithm that is broadly applicable: it extends naturally from physical dynamical systems to high-dimensional visual inputs and graph-structured dynamics, and our empirical results validate the theoretical predictions.

## 2 PRELIMINARIES

Notation. Let M ⊂Rn be a finite-dimensional manifold equipped with a measure µ. Consider a discrete-time nonlinear map T: M →M, so that the state xt ∈M evolves according to xt = T(xt−1). We denote by H = L2(M, µ), the Hilbert space of real-valued observables ϕ: M →R.

Definition 2.1 (Koopman Operator (Koopman, 1931)) The Koopman operator K: H →H is a linear operator acting on observables as

(Kϕ)(x) = ϕ(T(x)), for ϕ ∈H, x ∈M. (1)

Despite the appeal of lifting nonlinear dynamics into a linear forward via Koopman representation, practical approximations require projecting the infinite-dimensional function space H onto a finitedimensional subspace. In the Koopman learning framework, this restriction manifests as learning a finite set of effective latent features {ϕ1, ϕ2,..., ϕd} that map the state x as a latent representation z:= ϕ(x) ∈Z ⊊H, where Z is the latent space spanned by the selected latent features. The center of this paper is on discussion how to find a good representation z. To ground the principles of information theory, we introduce some essential technical definitions.

Definition 2.2 (Mutual Information (MacKay, 2003)) Given two random variables x and y with joint probability distribution p(x, y) and marginal distributions p(x) and p(y), the mutual information I(x; y) quantifies the amount of information shared between x and y, and is defined as

I(x; y) = E[log p(x, y)

p(x)p(y)] = E[log p(y|x)

p(y) ].

Definition 2.3 (Von Neumann Entropy (Witten, 2020)) Let ρ ∈Rd×d be a symmetric, positive semidefinite matrix with trace 1. The von Neumann entropy of ρ is defined as

S(ρ) = −tr(ρ log ρ).

If {λi}d i=1 are the eigenvalues of ρ, then S(ρ) = −Pd i=1 λi log λi. This value reflects latent effective dimensions: it is close to 0 if ρ is concentrated on a single direction, and close to log d if ρ is spread uniformly. More connection with effective dimension is given in Appendix E.

Intuitively, mutual information and the von Neumann entropy provide a principled way to measure the predictability and the intrinsic effective dimension of Koopman representation. Building on these preliminaries, we can quantify the preserved information under Koopman representation.

## METHOD

Our approach proceeds as: (1) a probabilistic analysis in Koopman representation how information loss drives error accumulation; (2) an information-theoretic characterization linking lost information to Koopman spectral properties; (3) a general Lagrangian formulation to guide better representation.

<!-- Page 4 -->

Published as a conference paper at ICLR 2026

## 3.1 INFORMATION FLOW IN KOOPMAN REPRESENTATION

A probabilistic view of Koopman representation. Firstly, we denote x1:t and z1:t as the states and their corresponding autoregressively generated latent variables from time step 1 to t, respectively. According to the direct information flow in Table 1, the Koopman representation induces the following trajectory distribution given x0:

pKR(x1:t|x0) =

Z p(z0|x0)

tY n=1 p(zn|zn−1)p(xn|zn)dz0dz1 · · · dzt. (2)

Here, p(z0|x0) acts as the encoder, mapping the initial state into a latent variable. The latent forward is modeled by a linear Gaussian transition, where p(zn|zn−1) = N(zn|Kzn−1, Σ) is a probabilistic representation of equation 1 with variance Σ. This directly reflects Definition 2.1, as the latent evolution is constrained to be linear. Finally, each state xn is reconstructed from its corresponding latent variable zn via a decoder p(xn|zn), typically instantiated as a Gaussian. We now turn to the fundamental question of whether information is inevitably lost during latent propagation.

Proposition 1 (Information Loss in Latent Evolution) Let xn−1 →zn−1

K −→zn →xn represent the information propagation in Koopman representation as shown in equation 2. Then, by the property of mutual information, the following holds:

I(xn−1; xn) ≥I(zn−1; xn) ≥I(zn−1; zn). (3)

The detailed proof and its multi-step extension are provided in Appendix F.1. The first inequality reflects that the mapping xn−1 →zn−1 is a compressed representation, which may discard predictive information about xn. The second inequality indicates that the latent forward propagation zn−1 →zn is governed by Koopman operator, inherently limits the information that can be preserved in the latent space. As a result, I(zn−1; xn) is larger than I(zn−1; zn), since the future state xn generally carries more dependencies on zn−1 than the latent evolution alone. In this sense, I(zn−1; zn) sets the information limit of Koopman representation by the operator K.

While Proposition 1 shows the degradation of information along latent propagation, it remains an abstract statement that is not directly tractable under the complex trajectory distributions in equation 2. To obtain a tractable measure, we turn to the Kullback–Leibler (KL) divergence as a natural way to quantify the discrepancy between true and Koopman-induced trajectories:

DKL p(x1:t|x0) ∥qKR(x1:t|x0)

≤DKL p(x1:t|x0) ∥pKR(x1:t|x0)

+ Eenc + Etra + Erec (4)

Here, p is the true distribution and pKR is the ideal Koopman model distribution in equation 2 without any approximations. qKR is the variational approximation, Eenc, Etra and Erec are approximation errors induced by the latent representation, Koopman operator and reconstruction (see details in Appendix F.2). This motivates the following result, which formalizes how the information gap translates into an autoregressive error bound for Koopman representations.

Proposition 2 (Autoregressive Error Bound of Koopman Representation) The distribution discrepancy between the true and Koopman-induced trajectories is bounded by the information gap as

∥p(x1:t | x0) −qKR(x1:t | x0)∥T V ≤ q

1 2[DKL(p(x1:t | x0) ∥pKR(x1:t | x0)) + E]

≤ v u u t 1

2 t X n=1

I(xn−1; xn) −I(zn−1; zn)

+ E.

(5)

Here, ∥· ∥T V is the total variation distance. The upper error bound is obtained as

EqKR[x1:t | x0] −Ep[x1:t | x0]

2 ≤ ¯C v u u t2 t X n=1

I(xn−1; xn) −I(zn−1; zn)

+ E, (6)

where ¯C is a positive constant and E is related to the approximation error in equation 4.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

The proof is in Appendix F.3. The KL divergence between the true and Koopman-induced trajectory distributions reflects how much temporal coherence is lost during representation. Here, I(xn−1; xn) quantifies the intrinsic dynamical coupling T in the original system, while I(zn−1; zn) characterizes the information of that coupling that exists under Koopman representation. Since I(zn−1; zn) acts as the information limit (see Proposition 1), the gap I(xn−1; xn) −I(zn−1; zn) measures the information that is lost when nonlinear dynamics are approximated by Koopman representation. Also, we link the upper/lower error bounds and distribution discrepancy in equations 6 (lower bound see equation 25). It reflects the prediction error is bounded by the step-wise information limit.

## 3.2 INFORMATION COMPONENTS IN KOOPMAN REPRESENTATION

The latent mutual information quantifies the magnitude of error, but does not uncover how this loss relates to Koopman spectral properties. To sharpen the insight from Propositions 1 and 2, we consider the aggregated quantity I(zt; xt), which measures the total information available to the decoder p(xt|zt). Our focus is on how much of this information can be stably propagated from past latent variables zt−n.

Koopman

Operator

Encoder

Decoder

Latent space Input Output

(a):

(b):

(c):

MI VNE MI + VNE

Koopman

Operator

Encoding

Decoding

Spectral Water-Filling Effect

Spectral Mode Allocated Information

Overall Architecture

Spectral Information Disentanglement

Latent Space Original Space

**Figure 1.** Information-theoretic Koopman framework. (a) Structure overview, (b) Information disentanglement with spectral interpretations, and (c) Water-filling effect of Mutual Information (MI) and von Neumann entropy (VNE) on spectral information allocation.

Proposition 3 (Information Disentanglement and Spectral Property) The mutual information I(zt; xt) can be disentangled into a summation of three distinct components, each with a spectral interpretation (see proof in Appendix F.4, see Figure 1(b)):

Component Temporal-coherent Fast-dissipating Residual

Spectral property λ≈1 λ <1 no counterpart Mutual info term I(zt−n; zt) ↑ I(zt; xt−1 | zt−n) ↓ I(zt; xt | xt−1) ↓

The decomposition shows that Koopman representations preserve temporal-coherent information associated with spectral modes of the Koopman operator whose eigenvalues lie near the unit circle, while information linked to dissipating modes (|λ| < 1) decays rapidly and noiselike components have no spectral support, hence compressible.

(1). Temporal-coherent information I(zt−n; zt) (see closed form equation 29). This term represents information that persists along the latent evolution zt−n →· · · →zt. It corresponds to conserved or slowly dissipating information that remains stable during latent evolution. From a spectral perspective, these are associated with Koopman modes whose eigenvalues are near to the complex unit circle (i.e., |λ| ≈1), implying that the corresponding information is propagated almost losslessly across time and hence remains mutually informative between past and present latent variables.

(2). Fast-dissipating information I(zt; xt−1|zt−n) (see closed form equation 35). This term reflects short-term dependencies that arise from the most recent state xt−1, beyond what is already encoded in the past latent state zt−n. Such information provides transient predictive power but quickly leaks out, since the autoregressive latent evolution zt−n →· · · →zt cannot continually access external inputs xt−1. In contrast, these contributions are associated with Koopman modes whose eigenvalues satisfy |λ| < 1, indicating exponential information dissipation with forward steps. Consequently,

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-26.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-29.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-ICLR-information-shapes-koopman-representation/page-005-figure-34.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

Published as a conference paper at ICLR 2026 the mutual information they contribute vanishes rapidly as the time step n increases, making those modes inherently cannot be captured by temporal-coherent information.

(3). Residual information I(zt; xt|xt−1) (see closed form equation 36). This term measures unpredictable information in the current state that cannot be explained from the past state. It corresponds to information injected at the present step—such as noise or anomalies—that interferes with constructing a coherent latent state. Unlike temporal-coherent or fast-dissipating modes, these residuals have no spectral counterpart in the Koopman operator: they are not tied to any eigenvalue structure. From the IB perspective, such non-predictive component is compressible. Having the disentangled information, the next question is how latent mutual information shapes Koopman representations.

Proposition 4 (The Role of Latent Mutual Information) Maximizing the latent mutual information I(zt−n; zt) allocates spectral weights to temporally coherent modes in the latent space, thereby enhancing the relevance of the Koopman representation. However, excessive emphasis on this objective can lead to mode collapse, where the representation concentrates on only a few dominant modes and loses effective dimension (see Figure 1(c)).

In Koopman representation, the latent mutual information admits a closed form

I(zt−n; zt) = 1

2 log det(I + M −1

2 n (Kn)C(Kn)⊤M

−1

2 n) (7)

where det denotes the determinant, I is the identity matrix, C:= Cov(zt−n) is the latent covariance matrix and Mn:= Pn−1 i=0 KiΣ(Ki)⊤is the n−step linear forward covariance (see detailed explanation and proof in Appendix F.5). We find that, from a Lagrangian perspective, maximizing I(zt−n; zt) of Koopman representation under the finite variance constraint tr(C) < ∞leads to a water-filling allocation: variance is distributed along the directions corresponding to the largest eigenvalues of M

−1

2 n KnC(Kn)⊤M

−1

2 n. These directions correspond to temporally coherent modes, which explains why higher latent mutual information enhances relevance. However, when the spectrum of this matrix is highly skewed, the water-filling solution degenerates into a low-rank allocation, squeezing information into only a few dominant directions. This effect reduces the effective dimension of the latent space Z, causing some spectral weights to vanish (cf. equation 43). To address the collapse induced by skewed spectral allocation, we next analyze how effective dimension can be preserved through entropy regularization.

Proposition 5 (Effective Dimension and Anti-Collapse) Low effective dimension (see Proposition 4) in Koopman representation indicates information collapse to few dominant modes and limits the model’s ability to represent rich modes. Penalizing the von Neumann entropy S(C tr(C)) encourages more expressive and spectrally diverse representations.

Connecting to Proposition 4, Appendix F.6 contains a detailed proof via a water-filling and Lagrangian view. The normalized operator C tr(C) can be regarded as a density matrix in Hilbert space, and the effective dimension can be measured as exp(S) (see Definition E.2). When penalized with large the von Neumann entropy, the water-filling solution attains a non-zero allocation across all modes, preventing variance from collapsing entirely onto a few dominant directions (cf. equation 46). This ensures a positive distribution of spectral weights across all modes, thereby avoiding degenerate spectra and increasing the effective dimension of the latent space Z (see Figure 1(c)).

## 3.3 INFORMATION-THEORETIC FORMULATION FOR PRACTICAL IMPLEMENTATION

The preceding analysis (Propositions 3, 4 and 5) reveals a fundamental trade-off in Koopman representation learning: maximizing latent mutual information enhances temporal coherence and predictive ability but risks mode collapse, whereas entropy regularization promotes spectral diversity for predictive sufficiency. Based on this principle, we formulate the following unified Lagrangian:

max z α log I(zt−n; zt) −βI(zt; xt|zt−n) + γS

C tr(C)

+ log p(xt|zt), (8)

where α, β and γ are Lagrangian multipliers. In equation 8, the first term in equation 7 preserves temporal-coherent information, the second term penalizes fast-dissipating or confounding components (I(zt; xt|zt−n) = I(zt; xt−1|zt−n) + I(zt; xt|xt−1), see proof in equation 31), the third term

<!-- Page 7 -->

Published as a conference paper at ICLR 2026 rewards larger von Neumann entropy of the normalized covariance to promote spectral diversity in the latent space Z. Lastly, log p(xt|zt) is the reconstruction terms from predicted latent variable zt.

While the Lagrangian in equation 8 captures the desired information-theoretic trade-offs, it is not directly computable. To make it practical, we derive a tractable loss function for satisfying temporal coherence, predictive sufficiency and structural consistency max

X n h αI(zn; Pn) | {z } Temporal coherence

+ βEpθ(zn|xn)[log qψ(zn|zn−1)]

| {z } Structural consistency

+ βHpθ(zn|xn)

| {z } Encoder entropy

+ log pω(xn|zn)

| {z } Reconstruction i

+ γS(C tr(C)) | {z } Predictive sufficiency

+ LELBO.

(9)

In VAE structure (shown in Figure 1(a)), each component of the loss plays a distinct role in balancing the information-theoretic objectives: (1) The mutual information I(zn; Pn) captures temporal coherence by linking zn to its temporal neighborhood Pn = {zn±i | 1 ≤i ≤k}, which includes immediate past and future latent states; in practice, this can be computed either via the closed form in equation 7 for low-dimensional latents, or approximated by InfoNCE (Wu et al., 2020) for high-dimensional settings. (2) The term −Epθ(zn|xn)[log qψ(zn|zn−1)] −Hpθ(zn|xn) serves as an equivalent representation of the conditional mutual information I(zt; xt|zt−1), with linear Gaussian transition qψ(zn|zn−1) = N(zn|Kψzn−1, Σψ) and entropy of encoder Hpθ(zn|xn) (see Appendix G.1). Minimizing this KL not only encourages the latent representation to capture information from the state xn, but also compresses fast-dissipating and residual components, ensuring that the representation remains expressive yet simple. Here, Epθ(zn|xn)[log qψ(zn|zn−1)] enforces structural consistency in latent space. (3) The term log pω(xn|zn) is the decoder loss from predicted latent variable zn. (4) von Neumann entropy term S

C tr(C)

is computed from the normalized co- variance matrix C = 1 B

PB i=1(zi −¯z)(zi −¯z)⊤of the latent codes within a minibatch of size B. This promotes spectral diversity and guards against mode collapse, ensuring that the learned Koopman representation retains predictive sufficiency. (5) LELBO is the Evidence Lower Bound (ELBO) for training stability and reconstruction (see more analysis and implementation details in Appendix G.1). For AE structure, Epθ(zn|xn)[log qψ(zn|zn−1)] degenerates into a L2 loss enforcing the structural consistency ∥zn+1 −Kψzn∥2, and ELBO becomes AE reconstruction term (see G.2).

## 4 EXPERIMENTS

Tasks. We evaluate our approach across three types of dynamical data: (1) Physical simulations, including Lorenz 63, K´arm´an vortex street, Dam flow, and weather forecasting task (ERA5), which test the ability to capture nonlinear, stochastic and high-dimensional physical dynamics; (2) Visualinput control, including image-based Planar, Pendulum, Cartpole, and 3-Link manipulator, which evaluate the ability to extract latent dynamics from high-dimensional visual inputs while controllable in latent spaces; and (3) Graph-structured dynamics prediction, including Rope and Soft Robotics, which tests generalized abilities of latent representation on dynamics with graph structures (see experimental details in Appendix G.3).

Metrics. We assess performance on both forecasting and control. For forecasting, we report (i) normalized root mean square error (NRMSE) for short- and long-term predictions (for physical simulation and graphs-structured dynamics), (ii) physical consistency metrics based on spectral distribution errors based on 1000−step sequences (SDEs), (iii) distributions of state measured by the Kullback–Leibler divergence (KLD), and (iv) structural similarity index (SSIM) for physical simulations. (v) the quality of low-dimensional manifold construction from high-dimensional visual inputs. For control, we measure the success rate of latent-space control of visual inputs following the setting in (Levine et al., 2020).

Baseline Algorithms. We compare against competitive baselines for each type of task. For physical simulations, we include VAE (Burgess et al., 2018), Koopman Autoencoder (KAE) (Pan et al., 2023), Koopman Kernel Regression (KKR) (Bevanda et al., 2023), and a SOTA Koopman variant for chaos - Poincar´e Flow Neural Network (PFNN) (Cheng et al., 2025). For visual-input control,

<!-- Page 8 -->

Published as a conference paper at ICLR 2026 we consider VAE-based representation learning methods, including Embed to Control (E2C) (Banijamali et al., 2019), as well as Prediction, Consistency and Curvature (PCC) (Levine et al., 2020), together with KAE. For graph-structured dynamics, we compare with Compositional Koopman Operator (CKO) (Li et al., 2020), the current SOTA method for graph-structured dynamics.

**Table 2.** Performance comparison of five algorithms on physical simulation tasks. PFNN is designed for chaotic dynamics and is thus not evaluated on Dam Flow. Here, N-NRMSE and N-SSIM denote errors at N prediction steps, values in parentheses indicate variance, and SDE is the spectral distribution error. Best results are highlighted in bold with green, second best are shaded in blue.

Task Metric VAE KAE KKR PFNN Ours

Lorenz 63

(n = 3)

5-NRMSE 0.005 (0.002) 0.006 (0.003) 0.004 (0.002) 0.005 (0.003) 0.003 (0.002) 20-NRMSE 0.011 (0.007) 0.014 (0.009) 0.009 (0.008) 0.011 (0.007) 0.007 (0.004) 50-NRMSE 0.019 (0.011) 0.023 (0.013) 0.017 (0.009) 0.017 (0.007) 0.013 (0.008) KLD 1.047 0.464 0.342 0.293 0.285

K´arm´an Vortex (n = 64 × 64 × 2)

5-NRMSE 0.127 (0.005) 0.149 (0.011) 0.114 (0.065) 0.075 (0.007) 0.068 (0.006) 20-NRMSE 0.134 (0.003) 0.195 (0.015) 0.157 (0.057) 0.125 (0.012) 0.114 (0.015) 50-NRMSE 0.211 (0.018) 0.233 (0.027) 0.209 (0.028) 0.137 (0.015) 0.138 (0.018) 5-SSIM 0.743 (0.100) 0.719 (0.030) 0.868 (0.087) 0.920 (0.030) 0.936 (0.025) 20-SSIM 0.720 (0.079) 0.586 (0.039) 0.732 (0.086) 0.800 (0.050) 0.823 (0.047) 50-SSIM 0.539 (0.045) 0.571 (0.037) 0.581 (0.061) 0.710 (0.030) 0.688 (0.020) SDE 0.538 0.620 0.799 0.278 0.256

Dam Flow (n = 64 × 64 × 2)

5-NRMSE 0.030 (0.001) 0.037 (0.000) 0.019 (0.003) – 0.018 (0.001) 20-NRMSE 0.033 (0.000) 0.042 (0.000) 0.028 (0.002) – 0.024 (0.001) 50-NRMSE 0.034 (0.000) 0.046 (0.001) 0.031 (0.002) – 0.026 (0.003) 5-SSIM 0.522 (0.021) 0.419 (0.031) 0.720 (0.034) – 0.760 (0.012) 20-SSIM 0.443 (0.007) 0.282 (0.024) 0.584 (0.025) – 0.627 (0.010) 50-SSIM 0.404 (0.005) 0.176 (0.008) 0.502 (0.010) – 0.577 (0.006) SDE 0.563 0.488 0.373 – 0.244

ERA5 Weather

(channel avg)

5-NRMSE – 0.055 0.058 0.049 0.028 10-NRMSE – 0.063 0.068 0.060 0.035 50-NRMSE – 0.118 0.074 0.079 0.068 5-SSIM – 0.666 0.664 0.697 0.867 10-SSIM – 0.619 0.606 0.635 0.808 50-SSIM – 0.481 0.707 0.695 0.781

Result Analysis. Our analysis is organized around the contributions established in propositions(Section 3), and we structure the discussion by addressing the following key questions. (1) Does the latent mutual information determine the predictive limit of the Koopman representation? (Proposition 2) – Yes. This is verified by the quantitative results of physical simulations in Table 2. Consistent with proposition, the prediction error under Koopman representation inevitably accumulates and is bounded by the latent mutual information. By regularizing with latent mutual information, both short- and long-term predictions are improved. Notably, PFNN (Cheng et al., 2025) is a SOTA model specifically designed with domain-specific knowledge, while our method, grounded in general information theory, achieves comparable performance on chaotic tasks (Lorenz 63 and K´arm´an vortex). Compared with other Koopman-based methods, our approach yields substantial improvements in both physical consistency and predictive accuracy.

(2) How is the preserved information—particularly that associated with Koopman eigenmodes near the unit circle—shaped by latent mutual information and von Neumann entropy in constructing a dynamics-relevant manifold? (Proposition 4 and 5) The preserved information manifests in Koopman modes with eigenvalues lying close to the unit circle, capturing the recurrent structure of the K´arm´an vortex limit cycle, as shown in Figure 2 (left). However, KAE suffers from some eigenvalues collapse toward zero, reducing the effective latent dimension. This collapse explains the drift observed in its autoregressive prediction. In contrast, our model captures the limit-cycle structure and produces stable autoregressive trajectories, consistently revolving around the true orbit (Figure 2, right). Baselines such as KKR and PFNN also capture limit-cycle structure (via one-step reconstruction) but gradually deviate from the correct trajectory over long horizons. By incorporating latent mutual information, we ensure that temporal-coherent information is retained, while von Neumann entropy prevents eigenvalue degeneration and preserves sufficient modes. Consequently, the information behind those modes can be preserved over long horizons, which directly translates into improved long-term prediction accuracy and statistical consistency, as also reported in Table 2.

<!-- Page 9 -->

Published as a conference paper at ICLR 2026

Ours KAE

𝑅𝑒(𝜆)

𝐼𝑚(𝜆)

𝑅𝑒(𝜆)

𝐼𝑚(𝜆)

**Figure 2.** Eigenvalue comparison and manifold visualization of the K´arm´an vortex street. Left: Eigenvalue distributions of Koopman operators. Right: t-SNE visualization of learned latent manifolds for five methods on the K´arm´an vortex. The underlying dynamics is abstracted as a limit cycle.

(3) How does explicit information-theoretic regularization sufficiently capture essential dynamics, compared with VAEs and Koopman autoencoders? (Proposition 4 and 5) As shown in the reconstructed manifolds of Figure 3, our method produces a latent manifold that aligns most closely with the ground truth. For E2C, which is directly built on a VAE architecture, the latent geometry is heavily distorted (the loss of coherence). The manifold learned by KAE collapses into a nearly onedimensional structure, reflecting the lack of effective dimensions in its latent space. PCC, a modified VAE-based method designed to improve manifold construction, demonstrates partial improvement but still exhibits a gap compared with our approach. By preserving both effective dimensionality and temporal coherence, our Koopman representation achieves the best average control performance in both noiseless and noisy environments (Table 8 and 9 in Appendix G.5.2).

Ground truth PCC manifold E2C manifold KAE manifold Our manifold

Y-axis position

**Figure 3.** Latent manifolds of Planar visualized using locally linear embedding. The first subfigure shows the ground truth, while the second to fifth depict manifolds learned by different algorithms.

2018-01-01 08:00

Ground Truth KAE KKR PFNN Ours

2018-01-08 08:00

0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840

Error

0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472

0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840 0.00000 0.00614 0.01227 0.01840

Error

0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472 0.00000 0.00491 0.00981 0.01472

**Figure 4.** Comparison of continuous predictions for the global humidity starting from 2018 −01 − 01 −00: 00 to 2018 −01 −08 −08: 00. Error maps in the lower panels demonstrate that, compared with other models, showing with more stable and accurate results of our model (see more demonstration in Appendix G.5.1).

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-information-shapes-koopman-representation/page-009-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 10 -->

Published as a conference paper at ICLR 2026

(4) How robust are the findings under noise, extended prediction horizons, and large-scale settings? (Proposition 1 and 2) Our method remains robust under both noisy observations and extended prediction horizons. As shown in Table 2 and Figure 4, it maintains stable performance in long-term rollouts and physical statistics in large scale weather forecasting. Moreover, our approach supports control under noisy environments, achieving competitive performance. These quantitative results are consistent with our probabilistic propositions.

(5) To what extent can our Lagrangian formulation be generalized to diverse architectures and adapted to support downstream tasks? (Proposition 1-5) Our formulation demonstrates broad applicability: it consistently improves performance across physical simulations (see Table 2), visual perception tasks for manifold construction and control (see Figure 3, Tables 8 and 9 in Appendix G.5.2), and graph-structured dynamics prediction (see Figure 5). These gains indicate that the proposed Lagrangian principle is architecture-agnostic and can be readily incorporated into different settings to enhance both predictive accuracy and task effectiveness (more results are referred to Appendix G.5).

**Figure 5.** Comparison of prediction over 100 rollout steps. The left two figures show results for the Rope environment (n ∈[40, 56]) with and without noise; the right two subfigures are the results for the Soft environment (n ∈[160, 224]).

𝛼= 0, 𝛽= 2, 𝛾= 0.5 𝛼= 1, 𝛽= 0, 𝛾= 0.5 𝛼= 1, 𝛽= 2, 𝛾= 0 𝛼= 4, 𝛽= 2, 𝛾= 0 𝛼= 2, 𝛽= 2, 𝛾= 0.5 𝛼= 3, 𝛽= 2, 𝛾= 0.5

Pendulum Angle π

−π

**Figure 6.** Ablation study on the pendulum task. Latent manifolds are learned from high-dimensional pendulum images, where the ground-truth phase space is isomorphic to S1 × R. Color represents the pendulum angle. Each subplot corresponds to removing or adjusting one regularization term: latent mutual information (α), KL divergence (β), and von Neumann entropy (γ).

Ablation Studies. We analyze the effect of varying each Lagrangian multiplier to understand its role in shaping Koopman representation. In the pendulum task, the ground-truth phase space is S1 × R, consisting of a periodic angle and an angular velocity. The ablation study in Figure 6 illustrates how each regularization term contributes to recovering this manifold from high-dimensional visual inputs. Without mutual information regularization (α = 0), temporal coherence is lost and the latent space degenerates into scattered points without geometric structure. Without structural consistency (β = 0), the latent manifold collapses, highlighting its role in enforcing the dynamics of Koopman representation. Removing the von Neumann entropy term (γ = 0) retains the circular S1 component but suppresses the R dimension, indicating the necessity of preserving effective dimensions. Increasing mutual information alone concentrates the representation on the S1 component (reflecting Proposition 4), while regularizing with von Neumann entropy yields a manifold that closely approximates the full S1 × R structure. These observations align with the theoretical roles of the three penalties: temporal coherence, structural consistency and predictive sufficiency.

## 5 CONCLUSION

We presented a new perspective on Koopman representation by formulating it through an information-theoretic lens, leading to a general Lagrangian formulation that balances simplicity and expressiveness. Our analysis reveals the relationship between Koopman spectral properties and information in deep architectures. The proposed algorithm based on the Lagrangian formulation consistently improves the performance in a wide range of dynamical system tasks.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-information-shapes-koopman-representation/page-010-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

## ACKNOWLEDGMENTS

Zhuo Sun is supported by Fundamental Research Funds for the Central Universities 2025110590 of Shanghai University of Finance and Economics.

ETHICS STATEMENT AND REPRODUCIBILITY STATEMENT

This work raises no specific ethical concerns beyond standard practices in machine learning research. All methods, datasets, and hyperparameters are described in detail, and core code is released in supplementary materials.

## REFERENCES

Daniel Alpay. Reproducing kernel spaces and applications, volume 143. Birkh¨auser, 2012.

Hassan Arbabi and Igor Mezic. Ergodic theory, dynamic mode decomposition, and computation of spectral properties of the koopman operator. SIAM Journal on Applied Dynamical Systems, 16 (4):2096–2126, 2017.

Omri Azencot, N Benjamin Erichson, Vanessa Lin, and Michael Mahoney. Forecasting sequential data using consistent koopman autoencoders. In International Conference on Machine Learning, pp. 475–485. PMLR, 2020.

Francis Bach. Information theory with kernel methods. IEEE Transactions on Information Theory,

69(2):752–775, 2022.

Mark R Baker and Rajendra B Patil. Universal approximation theorem for interval neural networks.

Reliable Computing, 4(3):235–239, 1998.

Ershad Banijamali, Rui Shu, Hung Bui, Ali Ghodsi, et al. Robust locally-linear controllable embed- ding. In International Conference on Artificial Intelligence and Statistics, pp. 1751–1759. PMLR, 2019.

Alain Berlinet and Christine Thomas-Agnan. Reproducing kernel Hilbert spaces in probability and statistics. Springer Science & Business Media, 2011.

Petar Bevanda, Max Beier, Armin Lederer, Stefan Sosnowski, Eyke H¨ullermeier, and Sandra Hirche.

Koopman kernel regression. Advances in Neural Information Processing Systems, 36:16207– 16221, 2023.

Petar Bevanda, Max Beier, Armin Lederer, Alexandre Capone, Stefan Sosnowski, and Sandra

Hirche. Koopman-equivariant gaussian processes. arXiv preprint arXiv:2502.06645, 2025.

Stephen P Boyd and Lieven Vandenberghe. Convex optimization. Cambridge university press, 2004.

Morten Breivik and Thor I Fossen. Guidance laws for planar motion control. In 2008 47th IEEE

Conference on Decision and Control, pp. 570–577. IEEE, 2008.

Steven L Brunton, Bernd R Noack, and Petros Koumoutsakos. Machine learning for fluid mechanics.

Annual review of fluid mechanics, 52(1):477–508, 2020.

Steven L Brunton, Marko Budiˇsi´c, Eurika Kaiser, and J Nathan Kutz. Modern koopman theory for dynamical systems. arXiv preprint arXiv:2102.12086, 2021.

Christopher P Burgess, Irina Higgins, Arka Pal, Loic Matthey, Nick Watters, Guillaume Des- jardins, and Alexander Lerchner. Understanding disentangling in beta-vae. arXiv preprint arXiv:1804.03599, 2018.

Xiaoyuan Cheng, Yi He, Yiming Yang, Xiao Xue, Sibo Cheng, Daniel Giles, Xiaohang Tang, and

Yukun Hu. Learning chaos in a linear way. arXiv preprint arXiv:2503.14702, 2025.

Thomas M Cover. Elements of information theory. John Wiley & Sons, 1999.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Imre Csisz´ar, Paul C Shields, et al. Information theory and statistics: A tutorial. Foundations and

Trends® in Communications and Information Theory, 1(4):417–528, 2004.

Suddhasattwa Das and Dimitrios Giannakis. Koopman spectra in reproducing kernel hilbert spaces.

Applied and Computational Harmonic Analysis, 49(2):573–607, 2020.

Suddhasattwa Das, Dimitrios Giannakis, and Joanna Slawinska. Reproducing kernel hilbert space compactification of unitary evolution groups. Applied and Computational Harmonic Analysis, 54:75–136, 2021.

Marco Federici, Patrick Forr´e, Ryota Tomioka, and Bastiaan S Veeling. Latent representation and simulation of markov processes via time-lagged information bottleneck. arXiv preprint arXiv:2309.07200, 2023.

J Fritz. John von neumann and ergodic theory. The Neumann Compendium (F. Br ody and T. V amos, eds.), World Scientific, Singapore, pp. 127–131, 1995.

Katsuhisa Furuta, Masaki Yamakita, and Seiichi Kobayashi. Swing up control of inverted pendulum.

In Proceedings of IECON’91: 1991 International Conference on Industrial Electronics, Control and Instrumentation, pp. 2193–2198, 1991.

Shlomo Geva and J. Sitte. A cartpole experiment benchmark for trainable controllers. Unpublished benchmark description (often cited in RL literature), 1993. often referenced as the visual cartpole, see e.g. in RL benchmarks.

Hans Hersbach, Bill Bell, Paul Berrisford, Shoji Hirahara, Andr´as Hor´anyi, Joaqu´ın Mu˜noz-Sabater,

Julien Nicolas, Carole Peubey, Raluca Radu, Dinand Schepers, Adrian Simmons, Cornel Soci, Saleh Abdalla, Xavier Abellan, Gianpaolo Balsamo, Peter Bechtold, Gionata Biavati, Jean Bidlot, Massimo Bonavita, Giovanna De Chiara, Per Dahlgren, Dick Dee, Michail Diamantakis, Rossana Dragani, Johannes Flemming, Richard Forbes, Manuel Fuentes, Alan Geer, Leo Haimberger, Sean Healy, Robin J. Hogan, El´ıas H´olm, Marta Janiskov´a, Sarah Keeley, Patrick Laloyaux, Philippe Lopez, Cristina Lupu, Gabor Radnoti, Patricia de Rosnay, Iryna Rozum, Freja Vamborg, Sebastien Villaume, and Jean-No¨el Th´epaut. The era5 global reanalysis. Quarterly Journal of the Royal Meteorological Society, 146(730):1999–2049, 2020.

Patrick Kidger and Terry Lyons. Universal approximation with deep narrow networks. In Conference on learning theory, pp. 2306–2327. PMLR, 2020.

Diederik P Kingma, Max Welling, et al. Auto-encoding variational bayes, 2013.

Bernard O Koopman. Hamiltonian systems and transformation in hilbert space. Proceedings of the

National Academy of Sciences, 17(5):315–318, 1931.

Bernard O Koopman and J v Neumann. Dynamical systems of continuous spectra. Proceedings of the National Academy of Sciences, 18(3):255–263, 1932.

Milan Korda and Igor Mezi´c. Optimal construction of koopman eigenfunctions for prediction and control. IEEE Transactions on Automatic Control, 65(12):5114–5129, 2020.

Vladimir Kostic, Pietro Novelli, Andreas Maurer, Carlo Ciliberto, Lorenzo Rosasco, and Massimil- iano Pontil. Learning dynamical systems via koopman operator regression in reproducing kernel hilbert spaces. Advances in Neural Information Processing Systems, 35:4017–4031, 2022.

Vladimir Kostic, Karim Lounici, Pietro Novelli, and Massimiliano Pontil. Sharp spectral rates for koopman operator learning. Advances in Neural Information Processing Systems, 36:32328– 32339, 2023a.

Vladimir R Kostic, Pietro Novelli, Riccardo Grazzi, Karim Lounici, and Massimiliano Pontil. Learn- ing invariant representations of time-homogeneous stochastic dynamical systems. arXiv preprint arXiv:2307.09912, 2023b.

Vladimir R Kostic, Karim Lounici, Prune Inzerilli, Pietro Novelli, and Massimiliano Pontil. Consis- tent long-term forecasting of ergodic dynamical systems. In Forty-first International Conference on Machine Learning, 2024.

<!-- Page 13 -->

Published as a conference paper at ICLR 2026

Nikola Kovachki, Zongyi Li, Burigede Liu, Kamyar Azizzadenesheli, Kaushik Bhattacharya, An- drew Stuart, and Anima Anandkumar. Neural operator: Learning maps between function spaces with applications to pdes. Journal of Machine Learning Research, 24(89):1–97, 2023.

Nir Levine, Yinlam Chow, Rui Shu, Ang Li, Mohammad Ghavamzadeh, and Hung Bui. Predic- tion, consistency, curvature: Representation learning for locally-linear control. arXiv preprint arXiv:1909.01506, 2020.

Yunzhu Li, Hao He, Jiajun Wu, Dina Katabi, and Antonio Torralba. Learning compositional koop- man operators for model-based control. arXiv preprint arXiv:1910.08264, 2020.

Yong Liu, Chenyu Li, Jianmin Wang, and Mingsheng Long. Koopa: Learning non-stationary time series dynamics with koopman predictors. Advances in neural information processing systems, 36:12271–12290, 2023.

Jan CA Lubbe. Information theory. Cambridge university press, 1997.

David JC MacKay. Information theory, inference and learning algorithms. Cambridge university press, 2003.

Andreas Mardt, Luca Pasquali, Hao Wu, and Frank No´e. Vampnets for deep learning of molecular kinetics. Nature communications, 9(1):5, 2018.

Alexandre Mauroy, Y Susuki, and Igor Mezic. Koopman operator in systems and control, volume 7.

Springer, 2020.

Igor Mezic. Koopman operator, geometry, and learning. arXiv preprint arXiv:2010.05377, 2020.

Samuel E Otto and Clarence W Rowley. Linearly recurrent autoencoder networks for learning dynamics. SIAM Journal on Applied Dynamical Systems, 18(1):558–593, 2019.

Shaowu Pan and Karthik Duraisamy. Physics-informed probabilistic learning of linear embeddings of nonlinear dynamics with guaranteed stability. SIAM Journal on Applied Dynamical Systems, 19(1):480–509, 2020.

Shaowu Pan, Eurika Kaiser, Brian M de Silva, J Nathan Kutz, and Steven L Brunton. Pykoop- man: A python package for data-driven approximation of the koopman operator. arXiv preprint arXiv:2306.12962, 2023.

Stephan Rasp, Stephan Hoyer, Alexander Merose, Ian Langmore, Peter Battaglia, Tyler Russell,

Alvaro Sanchez-Gonzalez, Vivian Yang, Rob Carver, Shreya Agrawal, Matthew Chantry, Zied Ben Bouallegue, Peter Dueben, Carla Bromberg, Jared Sisk, Luke Barrington, Aaron Bell, and Fei Sha. Weatherbench 2: A benchmark for the next generation of data-driven global weather models. Journal of Advances in Modeling Earth Systems, 16(6):e2023MS004019, 2024.

Olivier Roy and Martin Vetterli. The effective rank: A measure of effective dimensionality. In 2007

15th European signal processing conference, pp. 606–610. IEEE, 2007.

James V Stone. Information theory: A tutorial introduction to the principles and applications of information theory. 2024.

Naoya Takeishi, Yoshinobu Kawahara, and Takehisa Yairi. Learning koopman invariant subspaces for dynamic mode decomposition. Advances in neural information processing systems, 30, 2017.

Naftali Tishby and Noga Zaslavsky. Deep learning and the information bottleneck principle. In

2015 ieee information theory workshop (itw), pp. 1–5. Ieee, 2015.

Naftali Tishby, Fernando C Pereira, and William Bialek. The information bottleneck method. arXiv preprint physics/0004057, 2000.

Umesh Vaidya and Prashant G Mehta. Lyapunov measure for almost everywhere stability. IEEE

Transactions on Automatic Control, 53(1):307–323, 2008.

Darko Veberiˇc. Lambert w function for applications in physics. Computer Physics Communications,

183(12):2622–2628, 2012.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Matias Vera, Pablo Piantanida, and Leonardo Rey Vega. The role of the information bottleneck in representation learning. In 2018 IEEE international symposium on information theory (ISIT), pp. 1580–1584. IEEE, 2018.

Haoqing Wang, Xun Guo, Zhi-Hong Deng, and Yan Lu. Rethinking minimal sufficient representa- tion in contrastive learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 16041–16050, 2022.

Yiyi Wang, Jian’an Zhang, Hongyi Duan, Haoyang Liu, and Qingyang Li. Rethinking selectivity in state space models: A minimal predictive sufficiency approach. arXiv preprint arXiv:2508.03158, 2025.

Matthias Weissenbacher, Samarth Sinha, Animesh Garg, and Kawahara Yoshinobu. Koopman q- learning: Offline reinforcement learning via symmetries of dynamics. In International conference on machine learning, pp. 23645–23667. PMLR, 2022.

Matthew O Williams, Ioannis G Kevrekidis, and Clarence W Rowley. A data–driven approximation of the koopman operator: Extending dynamic mode decomposition. Journal of Nonlinear Science, 25(6):1307–1346, 2015.

Edward Witten. A mini-introduction to information theory. La Rivista del Nuovo Cimento, 43(4):

187–227, 2020.

Mike Wu, Chengxu Zhuang, Milan Mosse, Daniel Yamins, and Noah Goodman. On mutual in- formation in contrastive learning for visual representations. arXiv preprint arXiv:2005.13149, 2020.

Xingjian Wu, Xiangfei Qiu, Hongfan Gao, Jilin Hu, Bin Yang, and Chenjuan Guo. k2 vae: A koopman-kalman enhanced variational autoencoder for probabilistic time series forecasting. arXiv preprint arXiv:2505.23017, 2025.

Yuanchao Xu, Jing Liu, Zhongwei Shen, and Isao Ishikawa. Reinforced data-driven estimation for spectral properties of koopman semigroup in stochastic dynamical systems. arXiv preprint arXiv:2509.04265, 2025a.

Yuanchao Xu, Kaidi Shao, Isao Ishikawa, Yuka Hashimoto, Nikos Logothetis, and Zhongwei Shen.

A data-driven framework for koopman semigroup estimation in stochastic dynamical systems. arXiv preprint arXiv:2501.13301, 2025b.

Yuanchao Xu, Kaidi Shao, Nikos Logothetis, and Zhongwei Shen. Reskoopnet: Learning koopman representations for complex dynamics with spectral residuals. arXiv preprint arXiv:2501.00701, 2025c.

Yiming Yang, Xiaoyuan Cheng, Daniel Giles, Sibo Cheng, Yi He, Xiao Xue, Boli Chen, and Yukun

Hu. Tensor-var: Efficient four-dimensional variational data assimilation. In Forty-second International Conference on Machine Learning, 2025.

Raymond W Yeung. Information theory and network coding. Springer Science & Business Media,

2008.

Luo Yining, Chen Yingfa, and Zhang Zhen. Cfdbench: A large-scale benchmark for machine learn- ing methods in fluid dynamics. arXiv preprint arXiv:2310.05963, 2023.

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

THE USE OF LARGE LANGUAGE MODELS (LLMS)

During the preparation of this manuscript, the authors used ChatGPT to polish the writing (e.g., improving grammar, readability, and clarity). The content, technical contributions, and conclusions of the paper were developed entirely by the authors, who take full responsibility for all ideas and results presented.

A NOTATION

**Table 3.** Notations in the Main Text

Notations Meaning d latent dimension det determinant of matrix n state dimension p probability distribution pKR probability distribution of the Koopman-induced trajectory qKR variational approximation of the Koopman-induced trajectory t time step tr trace of matrix x state of dynamical systems z latent variable of dynamical systems C latent covariance matrix H Hilbert space I mutual information I identity matrix K Koopman operator DKL KL divergence L2(M, µ) Lebesgue space equipped with inner product Mn n−step linear forward covariance M finite-dimensional manifold N Gaussian distribution S von Neumann entropy T discrete-time nonlinear map of dynamics Z latent space spanned by {ϕ1,..., ϕd} α, β, γ Lagrangian multipliers λ eigenvalues ρ density matrix ϕ observable/feature ψ, θ, ω parameters for neural networks in Koopman representation

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

B A GENTLE INTRODUCTION TO APPENDIX

The appendix is organized to complement the main paper with precise definitions, detailed theoretical analysis, and additional experimental material. Given the information density of the appendix, we provide here a short roadmap to guide the reader:

• Appendix C More Literature review. We provide the classic to modern Koopman learning methods.

• Appendix D Limitations and Future Directions. We state the limitations of framework and propose some future directions for Koopman representation.

• Appendix E. Technical definitions. We collect the technical background, notations, and formal definitions used throughout the paper for ease of reference.

• Appendix F. Theoretical analysis. This section develops our theory step by step, where each proposition answers a natural “next question” in the following chain:

Q1. Will information be lost? (Proposition 1) Q2. If so, how much is lost? (Proposition 2) Q3. What kind of information is lost? (Proposition 3) Q4. How can we optimize information retention? (Proposition 4) Q5. How can we avoid negative side effects such as mode collapse? (Proposition 5)

In this way, the proofs form a coherent progression: each proposition is the answer to the next natural question raised by the previous one.

• Appendix G. Experimental setup and additional results. We provide implementation details, dataset descriptions, and supplementary results to support and validate the propositions made in the main text.

This structure ensures that readers can navigate the appendix according to their interests: consult Appendix A for notation, Appendix B for the full theoretical journey.

<!-- Page 17 -->

Published as a conference paper at ICLR 2026

C MORE LITERATURE REVIEW RELATED TO KOOPMAN REPRESENTATION

The Koopman operator was originally introduced by Koopman and von Neumann as a linear embedding of Hamiltonian dynamical systems (Koopman, 1931; Koopman & Neumann, 1932). However, its infinite-dimensional nature makes it difficult to identify suitable handcrafted basis functions using conventional methods (Brunton et al., 2021). To address this, kernel techniques from functional analysis have been employed as bases for learning the Koopman operator (Das & Giannakis, 2020; Das et al., 2021; Kostic et al., 2022; Bevanda et al., 2025). Owing to the well-posed properties of kernel functions in reproducing kernel Hilbert spaces (e.g., linearity, existence, and convergence guarantees), the Koopman operator can be directly approximated via (extended) dynamic mode decomposition (DMD or EDMD) (Williams et al., 2015; Takeishi et al., 2017; Arbabi & Mezic, 2017; Xu et al., 2025a). Despite these theoretical advantages, fixed kernel functions are often too restrictive to capture a general function space (Berlinet & Thomas-Agnan, 2011; Alpay, 2012).

In contrast, deep learning frameworks provide a more flexible alternative: leveraging the universal approximation property of neural networks (Baker & Patil, 1998; Kidger & Lyons, 2020), they allow learning a general Koopman representation without relying on predefined kernels. Following this principle, (variational) autoencoder (AE/VAE) architectures have been widely adopted to extract features spanning the Koopman subspace (Liu et al., 2023; Wu et al., 2025; Xu et al., 2025b;c). The resulting latent representations are flexible and support downstream tasks such as prediction and control (Li et al., 2020; Mauroy et al., 2020; Korda & Mezi´c, 2020; Weissenbacher et al., 2022). However, these representations are typically learned in a purely self-supervised manner, lacking explicit grounding in dynamical systems theory. To improve their reliability, recent studies incorporate domain-specific priors—such as symmetry, conservation laws, dissipation, or ergodicity—into the Koopman representation (Vaidya & Mehta, 2008; Weissenbacher et al., 2022; Azencot et al., 2020; Cheng et al., 2025). Within the VAE setting, recent studies (Federici et al., 2023) have started to link Markovian dynamics and information theory, demonstrating that time-lagged tricks can exploit mutual information to obtain better latent representations. While existing approaches are effective for specific dynamical systems, a formal theoretical foundation for guiding the learning of Koopman representations remains insufficient. In this work, we investigate how general information-theoretic principles can be employed to fill this gap.

D LIMITATIONS AND FUTURE DIRECTIONS

A current limitation of our framework is that it does not address the sample complexity or nonasymptotic convergence of the Koopman representation; future work could explore more rigorous theoretical analyses in this direction. In addition, recent studies have highlighted connections between kernel methods (Kostic et al., 2022; 2023a; 2024) and information theory (Bach, 2022), suggesting an interesting avenue for extending conventional kernel techniques in Koopman theory through an information-theoretic perspective.

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

E KEY TECHNICAL DEFINITIONS AND RELATED PROPERTIES

Definition E.1 (Density Matrix (Bach, 2022)) A density matrix ρ ∈Rd×d is a real symmetric matrix satisfying:

• ρ is positive semi-definite: ρ ⪰0

• The trace of ρ is 1: tr(ρ) = 1

Such a matrix can be interpreted as a probability-weighted combination of orthonormal directions in Rd. It admits a spectral decomposition:

ρ = d X i=1 piviv⊤ i, where pi ≥0, d X i=1 pi = 1, and vi ∈Rd with ∥vi∥= 1.

Definition E.2 (Effective Dimension (Roy & Vetterli, 2007)) Given a density matrix ρ on a Hilbert space, the effective dimension is defined as deff(ρ):= exp

S(ρ)

, where S(ρ) = −Tr(ρ log ρ) is the von Neumann entropy of ρ.

The effective dimension measures how many directions in a representation space are substantially used. Given a symmetric, positive semi-definite matrix ρ with unit trace, its von Neumann entropy

S(ρ) = −tr(ρ log ρ)

quantifies the spectral diversity of ρ. The effective dimension is then defined as deff(ρ) = exp

S(ρ)

, so that deff(ρ) can be interpreted as the number of dimensions effectively occupied by the latent variable. In particular, deff(ρ) = 1 when ρ is concentrated on a single direction (pure state in quantum mechanics), while deff(ρ) = d when ρ is maximally mixed and spreads uniformly over all d directions. A higher effective feature dimension is often required to ensure predictive sufficiency.

H(z) H(x)

I(z; x) H(z|x) H(x|z)

**Figure 7.** A Venn diagram illustrating entropy, conditional entropy, and mutual information between the true state x and latent variable z. H(x) and H(z) denote the Shannon entropy (total information) of x and z, respectively. Their symmetric overlap, I(z; x), represents the mutual information that quantifies how much information about the true dynamics is preserved in the Koopman representation. The non-overlapping regions, H(x|z) and H(z|x), correspond to the residual uncertainty not captured by I(z; x).

Definition E.3 (Entropy, Mutual Information and Conditional Mutual Information) Let x, y, z be random variables. Beyond the Definition 2.2 in the main text, we give a standard definition of (conditional) mutual information based on Shannon entropy (shown in Figure 7, (Csisz´ar et al., 2004)).

• D1 Entropy of a random variable x is defined as

H(x):= −

Z p(x) log p(x)dx.

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

• D2 Mutual Information is defined as

I(z; x):= H(z) + H(x) −H(z, x), equivalently,

I(z; x) = H(x) −H(x|z) = H(z) −H(z|x).

It can also be expressed in terms of the Kullback–Leibler (KL) divergence:

I(x; y) = DKL p(x, y)

p(x)p(y)

, where

DKL(p(x)∥q(x)):=

Z p(x) log p(x)

q(x)dx.

• D3. Conditional Mutual Information is defined as

I(x; y | z):= H(x | z) + H(y | z) −H(x, y | z), equivalently,

I(x; y | z) = H(x | z) −H(x | y, z).

In terms of KL divergence,

I(x; y | z) = Ez h

DKL p(x, y | z)

p(x | z) p(y | z)

i

= Ez h

DKL p(x | y, z)

p(x | z)

i

.

<!-- Page 20 -->

Published as a conference paper at ICLR 2026

F THEORETICAL FRAMEWORK

To ground our theoretical analysis, we first formalize the autoregressive structure of Koopman representations illustrated in Figure 8. The original dynamics evolve as a nonlinear transformation xt−n →xt−n+1 →· · · →xt.

In parallel, states are encoded into latent variables zt−n, which propagate linearly under the Koopman operator K and are subsequently decoded back to approximate the original states. This twolayer structure makes clear where information may dissipate: (i) during encoding from x to z, (ii) along the linear latent evolution governed by K, and (iii) during reconstruction from z to x. Analyzing this flow of information is therefore essential for understanding the fundamental limits of Koopman representations, and the proofs of the following propositions will be developed around this structure.

xt−n xt−n+1 · · · xt zt−n zt−n+1 · · · zt

T encoding

T T

K K decoding

K decoding

**Figure 8.** The autoregressive structure of Koopman representation. Top row (solid arrows): the original states xt−n evolve under the nonlinear map T. Bottom row (dashed arrows): the states are first encoded into latent variables zt−n, which then evolve linearly under the Koopman operator K. The latent variables are subsequently decoded back to approximate the original states. Thus, the latent evolution under Koopman representation captures essential structure but do not directly contain the full state information. Note: the dashed arrows represent the approximated Koopman representation in latent space, whereas the solid arrows denote the true underlying dynamics.

Fact F.1 As shown in Figure 8, we set that the latent variable zt is obtained via a probabilistic encoder that depends only on the current true state xt, i.e., p(zt | xt). Consequently, the information content of zt cannot exceed that of xt, so H(zt) ≤H(xt) (due to the data processing inequality (Stone, 2024)). Moreover, under this setting, zt is conditionally independent of any other variable in the dynamical system given xt, i.e.,

I(zt; □| xt) = 0, or equivalently □⊥⊥zt | xt, where □denotes any variable in the dynamical system.

F.1 PROOF OF PROPOSITION 1

Beyond establishing Proposition F.1, it is crucial to highlight the phenomenon of information dissipation in the autoregressive Koopman representation (see Figure 8) and to clarify how the Koopman operator K connects to the information limit. By a fundamental principle of information theory, a compressed representation can never increase the available information. While this observation yields a one-step inequality 3, our analysis extends it to the multi-step analysis, where the cumulative effect of encoding, autoregressive latent evolution via K, and decoding can be rigorously tracked. This extension makes explicit how information gradually dissipates at each stage of the Koopman representation, ultimately leading to the error accumulation.

Lemma F.2 (Chain Rule of Information) For variables x, y, z, the mutual information with their joint variable satisfies

I(x; y) = I(x; (y, z)) −I(x; z | y), where (y, z) is treated as the joint random variable with distribution p(y, z). According to the non-negativity of conditional mutual information, it is obvious that

I(x; (y, z)) ≥I(x; y).

<!-- Page 21 -->

Published as a conference paper at ICLR 2026

Proof 1 We prove this proposition as two steps.

Step 1. According to the autoregressive structure of the Koopman representation, the first inequality 3 follows directly from the data processing inequality (Stone, 2024). Since the latent variable zt−1 is a compressed representation of xt−1, the mutual information between successive states cannot exceed that induced by the original dynamics T. Formally,

I(xt−1; xt) ≥ I(zt−1; xt). (10)

This can be derived based on the Fact F.1, it can be factorized as

I(xt−1; xt) = I((xt−1, zt−1); xt) −I(zt−1; xt|xt−1) (Lemma F.2)

= I((xt−1, zt−1); xt) −(((((((I(zt−1; xt|xt−1) (Fact F.1) = I(zt−1; xt) + I(xt−1; xt|zt−1) (Lemma F.2) ≥I(zt−1; xt). (non-negativity of mutual information)

(11) Thus, the first inequality is derived.

Step 2. In terms of seconding inequality, we derive it as follow

I(zt−1; xt) = I(zt−1; (xt, zt)) −I(zt−1; zt|xt) (Lemma F.2) = I(zt−1; (xt, zt)) −((((((I(zt−1; zt|xt) (Fact F.1) = I(zt−1; zt) + I(zt−1; xt|zt) (Lemma F.2) ≥I(zt−1; zt). (non-negativity of mutual information)

(12) Here, the proof for the proposition ends.

Beyond the proposition, we would like to disentangle the what information is lost during the Koopman representation. Combining equations 11 and 12, we obtain

I(xt−1; xt) = I(zt−1; xt) + I(xt−1; xt|zt−1)

= I(zt−1; zt) + I(zt−1; xt|zt) + I(xt−1; xt|zt−1), (13)

then,

I(xt−1; xt) −I(zt−1; zt) = I(zt−1; xt|zt) + I(xt−1; xt|zt−1) | {z } step-wise information gap in Koopman representation

. (14)

Furthermore, we extend from one-step mutual information to multi-step ones (with n ≥1), such that

I(xt−n; xt) = I((xt−n, zt−n); xt) −I(zt−n; xt|xt−n) (Lemma F.2) = I((xt−n, zt−n); xt) (Fact F.1) = I(zt−n; xt) + I(xt−n; xt|zt−n) (Lemma F.2) = I(zt−n; zt) + I(zt−n; xt|zt) + I(xt−n; xt|zt−n). (repeating previous procedure)

(15) Also, I(xt−n; xt|zt−n) can be disentangled as follows:

Step 1 — Introduce zt−n+1 Apply Lemma F.2:

I(xt−n; xt | zt−n) = I(xt−n; zt−n+1 | zt−n) + I(xt−n; xt | zt−n, zt−n+1).

Here, the graphical structure ensures that:

I(xt−n; zt−n+1 | xt, zt−n) = 0, so there is no correction term.

Step 2 — Introduce zt−n+2. Expand the second term via Lemma F.2:

I(xt−n; xt | zt−n, zt−n+1) = I(xt−n; zt−n+2 | zt−n, zt−n+1)

+ I(xt−n; xt | zt−n, zt−n+1, zt−n+2).

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

Again, the graphical structure implies:

I(xt−n; zt−n+2 | xt, zt−n, zt−n+1) = 0.

Step 3 — Repeat recursively. For each i = t −n + 1, t −n + 2,..., t:

I(xt−n; xt | zt−n:i−1) = I(xt−n; zi | zt−n:i−1) + I(xt−n; xt | zt−n:i), where zt−n:i:= (zt−n, zt−n+1,..., zi).

Equivalently, in compact notation:

I(xt−n; xt|zt−n) = t X i=t−n+1

I(xt−n; zi|zt−n:i−1) + I(xt−n; xt|zt−n:t). (16)

Thus, by combining equations 15 and 16, the multi-step lost information becomes

I(xt−n; xt) −I(zt−n; zt)

= t X i=t−n+1

I(xt−n; zi|zt−n:i−1) + I(xt−n; xt|zt−n:t) + I(zt−n; xt|zt). (17)

Here, we interpret the physical meaning of the three parts in Koopman representation. Each term I(xt−n; zi|zt−n:i−1) measures how much new information about past state xt−n revealed by the latent variable the latent variable zi, given all previous latent states. Physically, this corresponds to the fast-dissipating modes that decay quickly; as more latent steps are added, this residual information diminishes rapidly to zero.

The second term I(xt−n; xt|zt−n:t) measures the residual dependency between the past and the current state that cannot be fully represented the latent sequence {zt−n:t} due to the compressed representation.

The quantity I(zt−n; xt|zt) measures the information about the state xt that remains in the past latent variable zt−n but is not preserved in the current latent zt. A positive value therefore indicates information loss during latent evolution. This phenomenon arises from Koopman modes with eigenvalues |λ| < 1, whose contributions decay over time and thus dissipate predictive information in the Koopman representation.

<!-- Page 23 -->

Published as a conference paper at ICLR 2026

F.2 DERIVATION OF VARIATIONAL DISTRIBUTION

The derivation of discrepancy between true and Koopman-induced trajectories is listed as follow:

DKL p(x1:t|x0) ∥qKR(x1:t|x0)

=E log p(x1:t|x0)pKR(x1:t|x0) pKR(x1:t|x0)qKR(x1:t|x0)

=E log p(x1:t|x0) pKR(x1:t|x0)

+ E log pKR(x1:t|x0)

qKR(x1:t|x0)

≤E log p(x1:t|x0) pKR(x1:t|x0)

+ E log pKR(z0:t, x1:t|x0)

qKR(z0:t, x1:t|x0)

=E log p(x1:t|x0) pKR(x1:t|x0)

+ E log p(z0|x0) Qt n=1 p(zn|zn−1)p(xn|zn)

qKR(z0|x0) Qt n=1 qKR(zn|zn−1)qKR(xn|zn)

=E log p(x1:t|x0) pKR(x1:t|x0)

+ E log p(z0|x0) qKR(z0|x0)

+ t X n=1

E log p(zn|zn−1) qKR(zn|zn−1)

+ E log p(xn|zn) qKR(xn|zn)

= DKL p(x1:t|x0) ∥pKR(x1:t|x0)

| {z } discrepancy between true and Koopman-induced distributions

+ DKL p(z0|x0) ∥qKR(z0|x0)

| {z } latent representation error, Eenc

+ t X n=1

DKL p(zn|zn−1) ∥qKR(zn|zn−1)

| {z } Koopman operator error, Etra

+ DKL p(xn|zn) ∥qKR(xn|zn)

| {z } reconstruction error, Erec

.

(18)

Here, qKR denotes the variational approximation. For notational convenience, we denote the last three terms in equation 18 by Eenc, Etra, and Erec, respectively. Also, the logic from third line to fourth line holds since the inequality follows from the fact that marginalization cannot increase KL divergence.

F.3 PROOF OF PROPOSITION 2

Before proving Proposition 2, we first introduce a technical lemma.

Lemma F.3 (Pinsker’s Inequality (Yeung, 2008)) For any two probability distributions p and q over the same space X, the total variation distance

∥p −q∥T V:= sup

X

|p(X) −q(X)| is equal to one half of their L1 distance:

∥p −q∥T V = 1

2

Z

|p(x) −q(x)| dx.

Moreover, it is bounded by the Kullback–Leibler divergence:

∥p −q∥T V = 1

2

Z

|p(x) −q(x)| dx ≤ q

1 2DKL(p ∥q).

Proof 2 The proof proceeds in four steps: (1) establish the connection between KL divergence and total variation distance, (2) relate KL divergence to latent mutual information, (3) derive the upper error bound via information-theoretic limits, and (4) show that the lower bound decays exponentially with increasing latent mutual information.

<!-- Page 24 -->

Published as a conference paper at ICLR 2026

Step 1. By applying Pinsker’s inequality (Lemma F.3) and equation 18, we can directly bound the distributional discrepancy as

∥p(x1:t|x0)−qKR(x1:t|x0)∥T V ≤ r

1 2

DKL (p(x1:t|x0) ∥pKR(x1:t|x0)) + Eenc + Etra + Erec

.

(19)

Step 2. The connection between mutual information and KL divergence is given as follows:

I(xt−1; xt) −I(zt−1; xt)

=E[log p(xt|xt−1)

p(xt) ] −E[log p(zt|zt−1)

p(zt) ] (Definition 2.2)

=E[log p(xt|xt−1)

p(xt) ] + E[log p(zt) p(zt|zt−1)]

=E[log p(xt|xt−1)p(zt)

p(xt)p(zt|zt−1) ]

=E[log p(xt|xt−1)

p(zt|zt−1) · p(xt,zt) p(xt|zt) p(xt,zt) p(zt|xt)

] (Bayes’ rule)

=E[log p(xt|xt−1)

p(zt|zt−1) · p(zt|xt)

p(xt|zt)].

(20)

By recursively using the result in equation 20, we can summation the results as t X n=1

I(xn−1; xn) −I(zn−1; zn)

= t X n=1

E[log p(xn|xn−1)

p(zn|zn−1) · p(zn|xn)

p(xn|zn)]

=E[log p(z0|x0)

p(z0|x0)

Qt n=1 p(xn|xn−1) Qt n=1 p(zn|zn−1)

· Qt n=1 p(zn|xn) Qt n=1 p(xn|zn)

].

(21)

Here, p(xn|xn−1) and p(zn|zn−1) are governed by the original nonlinear dynamics T and Koopman operator N(zt|Kzt−1, Σ), respectively. Based on this fact, we can further to develop equation 21 as

E[log p(z0|x0)

p(z0|x0)

Qt n=1 p(xn|xn−1) Qt n=1 p(zn|zn−1)

· Qt n=1 p(zn|xn) Qt n=1 p(xn|zn)

]

=E[log p(z0:t, x1:t) pKR(z0:t, x1:t)]

≥E[log p(x1:t) pKR(x1:t)]

=DKL p(x1:t|x0) ∥pKR(x1:t|x0)

.

(22)

Plugging equation 22 into equation 19 in Step 1, we have p(x1:t|x0) −qKR(x1:t|x0)

T V

≤ r

1 2

DKL (p(x1:t|x0) ∥pKR(x1:t|x0)) + Eenc + Etra + Erec

≤ v u u t1

2 t X n=1

(I(xn−1; xn) −I(zn−1; zn)) + Eenc + Etra + Erec.

(23)

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

Step 3. Based on the distributional discrepancy in equation 23, we have the following inequality

EqKR[x1:t | x0] −Ep[x1:t | x0]

2

=

Z x1:t dqKR(x1:t | x0) −

Z x1:t dp(x1:t | x0)

2 (Lebesgue measure)

≤ x1:t

∞

Z qKR(x1:t | x0) −p(x1:t | x0)

dx1:t | {z } L1 distance

(triangle inequality)

≤2 ¯C p(x1:t | x0) −qKR(x1:t | x0)

T V (Lemma F.3)

≤¯C q

2DKL(p(x1:t | x0) ∥qKR(x1:t | x0)) (Pinsker’s inequality)

≤¯C v u u t2 t X n=1

I(xn−1; xn) −I(zn−1; zn)

+ Eenc + Etra + Erec, (via equation 19).

where the state x lies in a compact space M with a complete metric, ensuring ∥x1:t∥∞≤¯C < ∞. The proof ends.

Step 4. The classical rate-distortion theorem (Cover, 1999) states that x1:t ∈Rn×t, under L2 error distortion via the ideal Koopman model pKR, the minimal achievable distortion D is bounded by

D ≥nt

2πe exp(2 ntH(x1:t)) · exp(−2 nt t X n=1

I(zn−1; zn)). (24)

Since the entropy H(x1:t) can be totally measured by the mutual information Pt n=1 I(xn−1; xn) of original dynamics T. Then the accumulative mean-squared error after t steps given x0 is bounded below as

Ep

∥x1:t −EqKR[x1:t|x0]∥|x0

≥C exp(−2 nt( t X n=1

I(zn−1; zn) + Eenc + Etra + Erec)), (25)

where the constant C = nt 2πe exp(2 nt

Pt n=1 I(xn−1; xn)) absorbs the marginal entropy of the trajectory.

Remark F.4 A special case of Proposition 2 is ergodic system, conditioning on x0 and then taking the long-time average lim t→∞

1 t DKL p(x1:t | x0) ∥qKR(x1:t | x0)

≤lim t→∞

1 t t X n=1

I(xn−1, xn) −I(zn−1, zn)

, which follows from Proposition 2. The left-hand side is the relative entropy rate, and the inequality shows that the dynamic discrepancy between p and qKR can be controlled by the per-step information difference.

F.4 PROOF OF PROPOSITION 3

Beyond establishing Proposition 3, it is even more important to clarify the connection between spectral theory and the information components of the Koopman representation. Before proceeding to the detailed proof, we first derive the closed-form expression of latent mutual information under the Koopman representation. This will allow us to interpret the spectral properties of the Koopman operator from an information-theoretic perspective.

For one-step forward under Koopman representation, we have zt = Kzt−1 + ϵt−1, ϵt−1 ∼N(0, Σ).

For multi-step forward, it can be recursively derived as zt = K(Kzt−2 + ϵt−2) + ϵt−1,

<!-- Page 26 -->

Published as a conference paper at ICLR 2026

**Figure 9.** Spectral behavior of the Koopman operator under different regimes. Left: Eigenvalues of K (orange dots) lie on the complex unit circle (|λ| = 1), and those of Kn with n = 7 (blue crosses) remain on the unit circle, indicating temporal coherence and preservation of information. Right: Eigenvalues of K lie strictly inside the complex unit circle (|λ| < 1), and the spectrum of Kn contracts toward the origin as n increases, reflecting fast mixing and information dissipation.

then, zt = Knzt−n + n−1 X i=0

Kiϵt−i.

Here, ϵt−i ∼N(0, Σ) is a time-independent Gaussian distribution for all i. Therefore, zt follows the distribution as N(Knzt−n, Pn−1 i=0 KiΣ(Ki)⊤). For convenience, we denote the covariance matrix as

Mn:= n−1 X i=0

KiΣ(Ki)⊤, with zt ∼N(Knzt−n, Mn) (26)

Without loss of generality, we can set zt−n ∼N(0, C) and the covariance matrix is denoted as C:= Cov(zt−n). Given the latent variable zt−n, the conditional entropy H(zt|zt−n) is calculated as

H(zt|zt−n) = 1

2 log[(2πe)d det Mn]. (27)

On the other hand, the entropy H(zt) is calculated as

H(zt) = 1

2 log[(2πe)d det

KnC(Kn)⊤+ Mn

]. (28)

Proof 3 The proof of this proposition proceeds in three steps: (1) we first interpret latent mutual information in relation to the spectral properties of the Koopman representation; (2) we disentangle the mutual information I(zt; xt) to clarify the role of each component and its associated spectral behavior; and (3) we derive the closed-form expression of mutual information under the Koopman representation, which highlights how the Koopman operator governs the information flow.

Step 1. Spectral Properties in Latent Mutual Information. Based on the Definition E.3, mutual information I(zt−n, zt) is calculated via equations 26, 27 and 28 as

I(zt−n, zt) = H(zt) −H(zt|zt−n)

= 1

2 log[(2πe)d det

KnC(Kn)⊤+ Mn

] −1

2 log[(2πe)d det Mn]

= 1

2 log (2πe)d det

KnC(Kn)⊤+ Mn

(2πe)d det Mn

= 1

2 log det(I + M −1

2 n (Kn)C(Kn)⊤M

−1

2 n).

(29)

We now examine how the behavior of the Koopman representation depends on its spectral properties, by analyzing the cases where the eigenvalues of K satisfy |λ| > 1, |λ| ≈1, and |λ| < 1.

![Figure extracted from page 26](2026-ICLR-information-shapes-koopman-representation/page-026-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-information-shapes-koopman-representation/page-026-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

|λ| > 1: The Koopman representation is explosive: ∥Kn∥grows exponentially, so the term

KnC(Kn)⊤dominates. As a result, the mutual information I(zt−n; zt) diverges with n, reflecting amplification of initial uncertainty.

|λ| ≈1: The Koopman representation is temporally coherent: KnC(Kn)⊤remains bounded, and when noise is small the mutual information is approximately conserved at a constant level. This corresponds to the temporal-coherent information component.

|λ| < 1: The Koopman represent is fast mixing: Kn →0 as n →∞, so the additional term vanishes relative to Mn. Thus the mutual information I(zt−n; zt) →0, indicating that information from the remote past information is asymptotically lost due to contraction and noise accumulation.

An illustration is given in Figure 9, where the left panel shows the |λ| = 1 case with eigenvalues lying on the unit circle, and the right panel shows the |λ| < 1 case with eigenvalues contracting toward the origin as n increases.

Step 2. Disentanglement of mutual information I(zt; xt).

According to the chain rule of mutual information, we have

H(x) = H(x | z) + I(z; x), (30)

where H(x | z) measures the irreducible uncertainty of x given the latent variable (i.e., the information lost in the latent space), and I(z; x) quantifies the total amount of information about x preserved in the latent representation.

In this sense, I(z; x) can be regarded as the maximum information that the decoder can retain about the data through the latent variables. To better understand the role of structural consistency, we next decompose I(z; x) into components, in order to examine how much of this retained information is attributable to the latent forward via Koopman representation.

I(zt; xt) =I(zt, (zt−n, xt)) −((((((I(zt−n; zt|xt) (Fact F.1) =I(zt−n; zt) + I(zt; xt|zt−n)

=I(zt−n; zt) + I(zt; (xt−1, xt)|zt−n) −(((((((((I(zt; xt−1|zt−n, xt) (Fact F.1) =I(zt−n; zt) + I(zt; xt−1|zt−n) + I(zt; xt|zt−n, xt−1)

=I(zt−n; zt) + I(zt; xt−1|zt−n) + I(zt; (zt−n, xt)|xt−1) −(((((((((I(zt−n; zt|xt−1, xt)

=I(zt−n; zt) + I(zt; xt−1|zt−n) + I(zt; xt|xt−1) −(((((((((I(zt; zt−n|xt−1, xt) =I(zt−n; zt) + I(zt; xt−1|zt−n) + I(zt; xt|xt−1).

(31)

Step 3. According to Step 1, the latent mutual information has been thoroughly explained; we now turn to the second and third terms in equation 31.

For linear conditional Gaussian (Lubbe, 1997), the mutual information for

I(a, b|c) = 1

2 log det Σa|c det Σb|c det Σa,b|c

(32)

where Σa|c and Σb|c denote the conditional covariance matrices of a and b given c, respectively, and Σa,b|c denotes the joint conditional covariance matrix of (a, b) given c, i.e.,

Σa,b|c =

Σa|c Σab|c Σba|c Σb|c

, with Σab|c and Σba|c being the conditional cross-covariances.

<!-- Page 28 -->

Published as a conference paper at ICLR 2026

The closed-form expression for the mutual information I(zt; xt−1 | zt−n) is derived as follows. Conditioned on zt−n, we have the linear–Gaussian relations zt−1 | zt−n ∼N

K n−1zt−n, Mn−1

, zt | zt−n ∼N

K nzt−n, Mn

,

(33)

where Mk = Pk−1 i=0 K i Σ (K i)⊤. Assume xt−1 = Dzt−1 + ϵt−1 with ϵt−1 ∼N(0, R), independent of the process noise. Then

Σzt,xt−1|zt−n =

Mn KMn−1D⊤

DMn−1K⊤ DMn−1D⊤+ R

. (34)

Plugging equation 33–equation 34 into the Gaussian closed-form identity yields

I(zt; xt−1 | zt−n) = 1

2 log det(Mn) det(DMn−1D⊤+ R)

det

Mn KMn−1D⊤

DMn−1K⊤ DMn−1D⊤+ R

. (35)

To analyze how I(zt; xt−1 | zt−n) scales with n, it suffices to study the growth of Mn = Pn−1 i=0 K iΣ(K i)⊤. If the spectral radius ρ(K) < 1, then Mn converges to the unique solution M∞of the discrete Lyapunov equation M∞= Σ + KM∞K⊤., hence I(zt; xt−1 | zt−n) remains bounded (“compressible”). Conversely, if ρ(K) > 1, then Mn diverges and the information grows unbounded along the unstable directions. When ρ(K) ≈1, the growth is slow and reflects long-term temporal coherence (then it contradicts with equation 29, and can be captured by the latent mutual information). Therefore, this compressible information corresponds to the spectral radius ρ(K) < 1.

As for the residual term I(zt; xt | xt−1), it can be expanded as

I(zt; xt | xt−1) = H(xt | xt−1) −H(xt | zt, xt−1)

= H(xt | xt−1) −1

2 log det((2πe)dR), (36)

where the second equality follows from the observation model xt = Dzt+ϵt with ϵt ∼N(0, R), which implies H(xt | zt, xt−1) = 1

2 log det((2πe)dR). Therefore, this residual mutual information depends only on the noise covariance R and original dynamics T, but it has no spectral counterpart in the Koopman operator.

Summary. The mutual information I(zt; xt) naturally decomposes into three parts: (i) temporal-coherent information I(zt−n; zt), which captures temporal coherence when eigenvalues of Koopman operator λ ≈1; (ii) fast-dissipating information I(zt; xt−1 | zt−n), which remains bounded only in the stable regime ρ(K) < 1; and (iii) residual information I(zt; xt|xt−1), which reflects observation noise and has no spectral counterpart. These three components and their spectral interpretations are summarized in Table 4.

**Table 4.** Spectral interpretation of information components in Koopman representation

Information Spectral property Temporal behavior Information meaning

Temporal-coherent λ ≈1 Long-lived, persistent

Predictable, low entropy Fast-dissipating λ < 1 Rapidly decaying, short-lived

Transient, compressible under IB Residual / Confounding – (no spectral counterpart)

Unpredictable, injected at present step

Noise, anomalies, non-predictive leftovers

<!-- Page 29 -->

Published as a conference paper at ICLR 2026

F.5 PROOF OF PROPOSITION 4

To establish this proposition, we analyze the problem from a Lagrangian perspective. Specifically, we investigate how the Koopman representation behaves when the latent mutual information I(zt−n; zt) is maximized under a finite variance constraint. This perspective reveals a water-filling allocation principle that governs how variance is distributed across spectral modes, thereby clarifying the connection between latent mutual information and the latent variable z.

Proof 4 Consider latent variable under Koopman representation showing equation 26 zt = Knzt−n + ε, ε ∼N(0, Mn), C:= E[zt−nz⊤ t−n], (37)

where denotes the covariance matrix of zt−n. The matrix C characterizes the spectral distribution of the latent variable, and our goal is to investigate how maximizing latent mutual information influences Koopman representation.

According to the previous proof in equation 29, we have

I(zt−n; zt) = 1

2 log det(I + M −1

2 n (Kn)C(Kn)⊤M

−1

2 n).

Denote the singular value decomposition M

−1

2 n (K)n = Udiag(√gi)V ⊤with gi ≥0. Then

I(zt−n; zt) = 1

2 log det

I + Udiag(√gi)V T CV diag(√gi)U ⊤

. (38)

As tr(C) measures the total second moment, we impose tr(C) ≤C for some finite constant C. This assumption ensures that the Koopman representation has a bounded total variance, preventing degenerate solutions where the variance grows without bound.

Under the constraint tr(C) ≤C, maximizing the latent mutual information under Koopman representation becomes an optimization problem as max

C

1 2 log det

I + Udiag(√gi)V T CV diag(√gi)U ⊤ s.t. tr(C) ≤C.

(39)

In equation 38, the matrices U and V are orthogonal, and C is a symmetric positive semidefinite matrix with eigenvalues {p1,..., pd} with pi ≥0 for all i. We interpret these eigenvalues as spectral weights of the Koopman observables/features, indicating how variance is allocated across the observable/feature directions {ϕ1,..., ϕd} defined in equation 1. Then, optimization problem in equation 39 becomes a water-filling problem as max pi, Pd i=1 pi≤C

1 2 d X i=1 log(1 + gipi). (40)

The Lagrangian formulation becomes

L = 1

2 d X i=1 log(1 + gipi) −µ( d X i=1 pi −C) − d X i=1 ηipi. (41)

According to Karush–Kuhn–Tucker (KKT) condition (Boyd & Vandenberghe, 2004), we obtain

∂L ∂pi

= gi 2(1 + gipi) −µ −ηi = 0, ηi = 0 ⇒ pi = 1

2µ −1 gi

. (42)

Based on the non-negativity of the eigenvalues pi ≥0 for all i, the optimal allocation is pi = max n

0, 1 2µ −1 gi o

, (43)

<!-- Page 30 -->

Published as a conference paper at ICLR 2026 where µ is the Lagrange multiplier determined by the variance budget constraint. This solution characterizes the spectral weights of the Koopman representation along each observable/feature direction, and reveals two key phenomena:

• Concentration on temporally coherent modes. Since gi depends on the Koopman eigenvalues through Kn, larger pi in equation 43 are assigned to eigen-directions with |λ| ≈1, corresponding to temporal-coherent modes.

• Mode collapse. Because Pd i=1 pi ≤C, variance is preferentially allocated to directions with larger gain gi, while less informative directions receive zero weight. This leads to a low-rank allocation (low effective dimension) where only a subset of modes are retained.

In summary, this proof demonstrates that maximizing latent mutual information is equivalent to a water-filling allocation of spectral weights, which naturally explains why emphasizing this objective can lead to mode collapse in the Koopman representation.

F.6 PROOF OF PROPOSITION 5

Connecting to Proposition 4, we continue to prove Proposition 5 via Lagrangian formulation. Without entropy regularization, the solution degenerates to low-rank (mode collapse); with entropy regularization, the solution assigns non-zero weights to all directions, improving effective dimension.

Proof 5 According to Definition 2.3, we can normalize C into a density matrix C tr(C), then

S(C tr(C)) = − d X i=1 pi tr(C) log pi tr(C)

with pi is the eigenvalue of C.

Under a given regularization coefficient γ, this normalization allows us to improve the effecitve dimension. Based on equation 41, the modified Lagrangian formulation under the regularized Von Neumann entropy becomes

L = 1

2 d X i=1 log(1 + gipi) + γ(− d X i=1 pi tr(C) log pi tr(C)) −µ( d X i=1 pi −C) − d X i=1 ηipi. (44)

Based on the KKT condition, we have

∂L ∂pi

= gi 2(1 + gipi) −µ −ηi − γ tr(C)(log pi tr(C) + 1) = 0, (45)

where ηi = 0 under the KKT condition. The solution of equation 45 is gi 2(1 + gipi) −µ = γ tr(C)(log pi tr(C) + 1).

Since a closed-form solution is not directly available, we proceed with further algebraic transformation.

By reorganization, log pi tr(C) = tr(C)

γ gi 2(1 + gipi) −µ

−1.

Exponential both sides:

pi tr(C) = exp tr(C)

γ gi 2(1 + gipi) −µ

−1

<!-- Page 31 -->

Published as a conference paper at ICLR 2026

Then, pi = tr(C) exp tr(C)

γ gi 2(1 + gipi) −µ

−1

We can transform the above form as, pi exp

−tr(C)

γ gi 2(1 + gipi)

| {z } >0

= tr(C) exp

−1 −tr(C)

γ µ

| {z } =C1>0

. (46)

Here C1 = tr(C) exp

−1 −tr(C)

γ µ is a positive constant Introducing y = 1 + gipi, we can write equation 46 via algebraic transform:

(y −1) exp

−tr(C)gi

2γy

= giC1. (47)

The above equation is related to the form x exp(x) + rx = constant, we can solve it via the generalized Lambert W function (also known as r-Lambert W a, see (Veberiˇc, 2012))

y = tr(C)gi

2γ

W1/(giC1)

tr(C)gi

2γ giC1

. (48)

Here, W1/(giC1)(·) is the r-Lambert W function. Since pi = y−1 gi, the closed form of pi becomes pi = tr(C)

2γ

W1/(giC1)

tr(C)gi

2γ giC1

−1 gi

> 0. (49)

Then, the solution of equation 44 under the regularized von Neumann entropy assigns non-zero spectral weight to all observable/feature directions {ϕ1,..., ϕd}, since pi > 0 holds according to equation 46. Consequently, the effective dimension is provably improved.

aWr denotes the generalized Lambert W function, defined as the solution of x exp(x) + rx = constant.

<!-- Page 32 -->

Published as a conference paper at ICLR 2026

G PRACTICAL DETAILS, IMPLEMENTATION AND EXPERIMENTAL DETAILS

G.1 IMPLEMENTATION DETAILS FOR VAE

## Algorithm

## 1 Information-Theoretic Koopman

Representation (VAE, probabilistic)

Require: Dataset D = {xn}T n=0; network parameters (α, β, γ); learning rate η; number of epochs K; batch size B; neighbor window k; temperature τ. 1: Initialize encoder pθ(z|x), decoder pω(x|z), and latent dynamics network qψ(zn|zn−1). 2: for epoch = 1 to K do 3: for each minibatch {x1,..., xB} from D do 4: Sample latents zi ∼pθ(z|xi). 5: Temporal coherence (InfoNCE): For each zn, treat its temporal neighbors Pn = {zn±i | 1 ≤i ≤k} as positive samples, compute

I(zn; Pn) ≈ 1 |Pn|

X p∈Pn log exp(z⊤ n zp/τ) PB j=1 exp(z⊤ n zj/τ)

.

6: Structural consistency: compute latent likelihood

Epθ(zn|xn)[log qψ(zn|zn−1)]

7: Predictive sufficiency: compute covariance C = 1 B

P i(zi −¯z)(zi −¯z)⊤, where ¯z = 1 B

P i zi; normalize P = C/tr(C), then compute

S(P) = −

X j λj log λj, where λj denotes j th eigenvalue of P.

8: Standard Evidence Lower Bound (ELBO) term (for training stability and reconstruction):

LELBO = log pω(xn−1|zn−1) −DKL(pθ(zn−1|xn−1) ∥N(0, I)).

9: Total Loss:

L = − h αI(zn; Pn) + Epθ(zn|xn)[log qψ(zn|zn−1)] + Hpθ(zn|xn)

+ log pω(xn|zn) + γS(P) + LELBO i

.

10: Update θ, ω, ψ using Adam step η 11: end for 12: end for

Connection to Structural Consistency. By Definition E.3, when given zn−1 the conditional mutual information is

I(zn; xn | zn−1) = H(zn | zn−1) −H(zn | xn, zn−1).

Since the encoder is independent of zn−1 in our setting (according to Figure 8), this simplifies to

I(zn; xn | zn−1) = H(zn | zn−1) −H(zn | xn). (50)

Consider the encoder distribution pθ(zn | xn), which maps observations to latent variables, and the Koopman prior qψ(zn | zn−1) = N zn | Kψzn−1, Σψ

, which models latent evolution as a linear Gaussian transition governed by the Koopman operator Kψ.

<!-- Page 33 -->

Published as a conference paper at ICLR 2026

Then the conditional mutual information can be equivalently written as the following form according to Definition E.3 or equation 50:

I(zn; xn | zn−1) = Epθ(zn|xn)

log pθ(zn | xn) qψ(zn | zn−1)

. (51)

Expanding the term in equation 51, we

I(zn; xn | zn−1) = Epθ(zn|xn)[−log qψ(zn | zn−1)] −Hpθ(zn | xn).

has two effects:

## 1 Alignment with

Koopman dynamics. The expectation term Epθ(zn|xn)[−log qψ(zn|zn−1)] requires samples drawn from the encoder to lie in regions of high likelihood under the Koopman prior. Since the prior is parameterized as a linear Gaussian transition, minimizing the KL forces the encoder outputs to be predictable under a linear structure.

2. Entropy regularization. The entropy term Hpθ(zn|xn) encourages that the encoder not to be deterministic.

Together, these effects ensure that the latent variables produced by the encoder not only encode information about the current state but also evolve consistently with the linear Gaussian dynamics imposed by the Koopman operator. Formally, pθ(zn | xn) ≈qψ(zn | zn−1) =⇒ zn evolves approximately linearly under Kψ, which enforces structural consistency in the latent space.

<!-- Page 34 -->

Published as a conference paper at ICLR 2026

G.2 IMPLEMENTATION DETAILS FOR AE

## Algorithm

## 2 Information-Theoretic Koopman

Representation (AE, deterministic)

Require: Dataset D = {xn}T n=0; hyperparameters (α, β, γ); learning rate η; number of epochs K; batch size B; neighbor window k; temperature τ. 1: Initialize deterministic encoder zn = fθ(xn), decoder ˆxn = gω(zn), and Koopman operator Kψ. 2: for epoch = 1 to K do 3: for each minibatch {x1,..., xB} from D do 4: Encode latents zi = fθ(xi) for i = 1,..., B. 5: Temporal coherence (InfoNCE):

I(zn; Pn) ≈ 1 |Pn|

X p∈Pn log exp(z⊤ n zp/τ) PB j=1 exp(z⊤ n zj/τ)

.

6: Structural consistency (deterministic):

LKoop = ∥zn+1 −Kψzn∥2.

7: Predictive sufficiency: compute S(P) from normalized covariance P = C tr(C), C =

1 B

P(zi −¯z)(zi −¯z)⊤. 8: Reconstruction:

Lrec = ∥xn −gω(zn)∥2.

9: Total Loss:

L = Lrec −αI(zn; Pn) + βLKoop −γS(P).

10: Update θ, ω, ψ with Adam step η. 11: end for 12: end for

<!-- Page 35 -->

Published as a conference paper at ICLR 2026

G.3 EXPERIMENT SETTINGS AND ADDITIONAL RESULTS

G.3.1 PHYSICAL SIMULATION

Lorenz. The Lorenz dataset is generated from the classical Lorenz system of ordinary differential equations (ODEs), which model simplified atmospheric convection. The governing equations are:

˙x = σ(y −x),

˙y = x(ρ −z) −y, ˙z = xy −βz,

(52)

where σ = 10, ρ = 28, and β = 8/3 are the standard chaotic parameters. The system is integrated using a fixed time step ∆t = 0.1 s with a fourth-order Runge–Kutta method. The resulting trajectories exhibit chaotic behavior and are commonly used as benchmarks for nonlinear dynamical system identification.

K´arm´an Vortex. The K´arm´an vortex street dataset is generated from the two-dimensional incompressible Navier–Stokes equations, which describe the velocity field (u, v) and pressure p of a viscous fluid:

∂u

∂t + u∂u

∂x + v ∂u

∂y = −∂p

∂x + 1

Re

∂2u

∂x2 + ∂2u

∂y2

,

∂v

∂t + u∂v

∂x + v ∂v

∂y = −∂p

∂y + 1

Re

∂2v

∂x2 + ∂2v

∂y2

,

∂u ∂x + ∂v

∂y = 0,

(53)

where Re = UL/ν is the Reynolds number, defined with characteristic velocity U, length L, and kinematic viscosity ν. The training dataset covers flows with Re ∈[40, 1000], while the test dataset focuses on Re = 1000. The flow is simulated around a cylinder, producing the characteristic alternating vortex shedding pattern. The domain is discretized on a 64 × 64 grid, with time step ∆t = 0.001 s, and both u and v velocity components are recorded at each grid point (data from (Yining et al., 2023)).

Dam Flow. The dam flow dataset is also generated from the two-dimensional incompressible Navier–Stokes equations, using the same formulation as in the K´arm´an vortex case. The training dataset spans Re ∈[40, 1000] and the test dataset uses Re = 1000. The flow is initialized in a rectangular channel with a fixed dam obstacle, where an imposed inlet velocity drives the fluid past the dam-like structure, generating a simple wake pattern downstream. The domain is discretized on a 64 × 64 spatial grid, with temporal resolution ∆t = 0.1 s (data from (Yining et al., 2023)).

The ERA5 dataset is a global atmospheric reanalysis produced by the European Centre for Medium- Range Weather Forecasts (ECMWF), providing a physically consistent estimate of the large-scale circulation from 1940 to the present (Hersbach et al., 2020). The physic state consists of five channels: 500,hPa geopotential, 850,hPa temperature, 700,hPa specific humidity, and 850,hPa wind components in the zonal and meridional directions. We train all baselines from 1979-01-01 to 2016-01- 01 and test after 2018-01-01 (data from (Rasp et al., 2024)). Illustrations are provided in Figure 10.

G.3.2 VISUAL INPUTS

Planar System In this task the main goal is to navigate an agent in a surrounded area on a 2D plane (Breivik & Fossen, 2008), whose goal is to navigate from a corner to the opposite one, while avoiding the six obstacles in this area. The system is observed through a set of 40 × 40 pixel images taken from the top view, which specifies the agent’s location in the area. Actions are twodimensional and specify the x −y direction of the agent’s movement, and given these actions the next positional state of the agent is generated by a deterministic underlying (unobservable) state evolution function. Start State: one of three corners (excluding bottom-right). Goal State: bottomright corner. Agent’s Objective: agent is within Euclidean distance of 2 from the goal state.

<!-- Page 36 -->

Published as a conference paper at ICLR 2026

Lorenz 63 Kármán Vortex Dam Flow (a). (b). (c).

(d).

Lorenz63 Kármán Vortex Dam Flow

**Figure 10.** Examples of physical simulation: (a).Lorenz 63, (b).K´arm´an Vortex, (c).Dam Flow, (d).ERA5

Inverted Pendulum — SwingUp & Balance This is the classic problem of controlling an inverted pendulum (Furuta et al., 1991) from 48 × 48 pixel images. The goal of this task is to swing up an under-actuated pendulum from the downward resting position (pendulum hanging down) to the top position and to balance it. The underlying state st of the system has two dimensions: angle and angular velocity, which is unobservable. The control (action) is 1-dimensional, which is the torque applied to the joint of the pendulum. To keep the Markovian property in the observation (image) space, similar to the setting in E2C, each observation xt contains two images generated from consecutive time-frames (from current time and previous time). This is because each image only shows the position of the pendulum and does not contain any information about the velocity. Start State: Pole is resting down (SwingUp), or randomly sampled in ±π/6 (Balance). Agent’s Objective: pole’s angle is within ±π/6 from an upright position.

CartPole This is the visual version of the classic task of controlling a cart-pole system (Geva & Sitte, 1993). The goal in this task is to balance a pole on a moving cart, while the cart avoids hitting the left and right boundaries. The control (action) is 1-dimensional, which is the force applied to the cart. The underlying state of the system st is 4-dimensional, which indicates the angle and angular velocity of the pole, as well as the position and velocity of the cart. Similar to the inverted pendulum, in order to maintain the Markovian property the observation xt is a stack of two 80×80 pixel images generated from consecutive time-frames. Start State: Pole is randomly sampled in ±π/6. Agent’s Objective: pole’s angle is within ±π/10 from an upright position.

3-link Manipulator — SwingUp & Balance The goal in this task is to move a 3-link manipulator from the initial position (which is the downward resting position) to a final position (which is the top position) and balance it. In the 1-link case, this experiment is reduced to inverted pendulum. In the 2-link case the setup is similar to that of acrobot, except that we have torques applied to all intermediate joints, and in the 3-link case the setup is similar to that of the 3-link planar robot arm domain that was used in the E2C paper, except that the robotic arms are modeled by simple rectangular rods (instead of real images of robot arms), and our task success criterion requires both the swing-up (manipulate to final position) and balance. The underlying (unobservable) state st of the system is 6-dimensional, which indicates the relative angular velocities and relative angles of the 3 links. Start State: Pole is resting down. Agent’s Objective: pole’s angle is within ±π/6 from an upright position.

The control algorithm is linear quadratic control in the latent space and the corresponding control horizon follows the setting in (Levine et al., 2020).

G.3.3 GRAPH-STRUCTURED DYNAMICS FOR SIMULATION

In the numerical experiments, we adopt the graph environments introduced in (Li et al., 2020), where interactions among objects are modeled differently according to their connection types and physical

![Figure extracted from page 36](2026-ICLR-information-shapes-koopman-representation/page-036-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 36](2026-ICLR-information-shapes-koopman-representation/page-036-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 36](2026-ICLR-information-shapes-koopman-representation/page-036-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 36](2026-ICLR-information-shapes-koopman-representation/page-036-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 37 -->

Published as a conference paper at ICLR 2026

**Figure 11.** The examples of visual inputs: Planar (left), Pendulum (middle), Cartpole (right).

properties. These environments are designed to capture diverse interaction dynamics through a Koopman representation (see illustrative examples in Figure 12), as detailed below:

In the Rope environment, the top mass is fixed in height and is treated differently from the other masses, resulting in two distinct types of self-interactions: one for the top mass and one for non-top masses. Additionally, there are eight types of interactions between different objects. Each mass is represented by four dimensions, encoding its state and velocity. Objects in a relation can be either the top mass or a non-top mass, yielding four possible combinations. Interactions may occur between adjacent masses or between masses that are two hops apart. In total, this gives 4 × 2 = 8 types of interactions between different objects. Training is performed on environments with 5–9 objects, while testing uses 10–14 objects. The overall dimensionality ranges from 40 to 56.

In the Soft environments, quadrilaterals are categorized into four types: rigid, soft, actuated, and fixed, each with its own form of self-interaction. For interactions between objects, an edge is defined between two quadrilaterals only if they are connected at a point or along an edge. Connections from different directions are treated as distinct relations, with eight possible directions: up, down, left, right, up-left, down-left, up-right, and down-right. Relation types also encode the category of the receiving object, resulting in a total of (8 + 1) × 4 = 36 possible relation types between objects. Training is conducted on environments with 5–9 quadrilaterals, while testing uses 10–14 quadrilaterals. Each quadrilateral is represented by a 16-dimensional vector, giving a total dimensionality ranging from 160 to 224.

In noisy environment, the additive noise is zero-mean Gaussian with standard deviation equal to 10% of the standard deviation of the observation data.

Rope 1 Rope 2 Soft 1 Soft 2 Graph of Soft 2

**Figure 12.** Examples of ropes and soft robots. Left: Blue nodes denote the initial states of Rope 1 and Rope 2, while orange nodes show their states after 40 time steps. Right: Interconnected quadrilaterals indicate the initial states, and the boxes represent the states of the soft robots after 40 time steps. The second soft robot (Soft 2) can be abstracted as a graph structure shown on the right.

G.4 IMPLEMENTATION ALGORITHM OF THREE TASKS

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 37](2026-ICLR-information-shapes-koopman-representation/page-037-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 38 -->

Published as a conference paper at ICLR 2026

**Table 5.** Model structures across experimental environments. Here, Kzt + Bat denotes a controlled latent transition with linear control input at (Visual Inputs case). K(A) denotes an adjacencyconditioned Koopman operator, corresponding to a shared Koopman composition modulated by the adjacency matrix A (i.e., K(A):= A ⊗K in graph environments; see Li et al. (2020, Page 4) for details).

Environment Structure Key Features

Physical Simulation AE (G.2) zt+1 = Kzt; reconstruction; Koopman linear forward; InfoNCE; von Neumann entropy

Visual Inputs (Control Tasks)

VAE (G.1) zt+1 = Kzt + Bat + ϵ (Linear Gaussian); VAE ELBO; reconstruction; InfoNCE; von Neumann entropy

Graph-structured Dynamics

AE (G.2) zt+1 = K(A)zt (adjacency-conditioned); reconstruction; InfoNCE; von Neumann entropy

<!-- Page 39 -->

Published as a conference paper at ICLR 2026

G.5 MORE EXPERIMENTAL RESULTS

G.5.1 PHYSICAL SIMULATIONS

**Figure 13.** Comparison of sampled spatial distributions based on 100000−step data for Lorenz 63. Green denotes the ground-truth distribution from the physical solver, and purple denotes samples generated by our method. Across both marginal and joint projections, the two distributions exhibit close agreement, demonstrating that our empirical results capture the underlying dynamics.

t = 0.71s

Ground Truth VAE KAE KKR PFNN Ours

Error

0

2

4

6

8

10

0.0

0.2

0.4

0.6

0.8

1.0

Kármán vortex street: Continuous Prediction from t=0.7s t = 0.8s Error

0

2

4

6

8

10

2

4

6

**Figure 14.** Comparison of continuous predictions for the K´arm´an vortex street starting from t = 0.7s. Ground truth are contrasted with predictions from VAE, KAE, KKR, PFNN, and our method. Error maps in the lower panels demonstrate that, compared with other models, our method achieves the closest agreement and effectively prevents collapse in the predicted fields.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-26.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-29.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-41.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-42.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-44.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-45.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-46.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-47.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-48.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-49.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-50.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-51.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-52.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 39](2026-ICLR-information-shapes-koopman-representation/page-039-figure-53.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 40 -->

Published as a conference paper at ICLR 2026 t = 5.5s

Ground Truth VAE KAE KKR Ours

Error

0.0

0.5

1.0

1.5

2.0

2.5

0.2

0.4

0.6

0.8

1.0

CFDBench Dam Flow: Continuous Prediction from t=5.0s t = 7.5s Error

0.0

0.5

1.0

1.5

2.0

0.5

1.0

1.5

**Figure 15.** Comparison of continuous predictions for the dam flow starting from t = 5.0s. Ground truth are contrasted with predictions from VAE, KAE, KKR, and our method. Error maps in the lower panels demonstrate that, compared with other models, our method more effectively prevents collapse in the predicted fields for dam flow.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-31.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-34.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-36.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-37.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-38.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-39.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-40.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-41.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-42.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-43.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 40](2026-ICLR-information-shapes-koopman-representation/page-040-figure-44.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 41 -->

Published as a conference paper at ICLR 2026

**Table 6.** Per-channel performance comparison on ERA5 weather forecasting. N-NRMSE and N- SSIM denote errors at N prediction steps; values in parentheses indicate the standard deviation across test samples. Even under the highly stochastic and high-dimensional ERA5 weather dynamics, our approach outperforms all baselines across both short-term and long-term prediction horizons.

Channel Metric KAE KKR PFNN Ours

Geopotential

5-NRMSE 0.058 (0.020) 0.061 (0.027) 0.046 (0.012) 0.023 (0.005) 10-NRMSE 0.068 (0.018) 0.074 (0.026) 0.062 (0.018) 0.032 (0.010) 50-NRMSE 0.157 (0.071) 0.082 (0.025) 0.082 (0.016) 0.075 (0.017) 5-SSIM 0.860 (0.054) 0.852 (0.064) 0.882 (0.036) 0.964 (0.011) 10-SSIM 0.836 (0.051) 0.820 (0.065) 0.848 (0.052) 0.943 (0.028) 50-SSIM 0.665 (0.195) 0.790 (0.049) 0.765 (0.055) 0.806 (0.039)

Temperature

5-NRMSE 0.049 (0.019) 0.052 (0.032) 0.040 (0.009) 0.022 (0.003) 10-NRMSE 0.056 (0.017) 0.064 (0.028) 0.051 (0.015) 0.026 (0.006) 50-NRMSE 0.114 (0.054) 0.074 (0.030) 0.067 (0.018) 0.063 (0.019) 5-SSIM 0.866 (0.046) 0.862 (0.058) 0.888 (0.026) 0.956 (0.008) 10-SSIM 0.844 (0.044) 0.829 (0.063) 0.859 (0.042) 0.942 (0.019) 50-SSIM 0.671 (0.216) 0.802 (0.059) 0.803 (0.051) 0.825 (0.042)

Humidity

5-NRMSE 0.064 (0.029) 0.069 (0.043) 0.055 (0.011) 0.031 (0.003) 10-NRMSE 0.077 (0.027) 0.085 (0.041) 0.070 (0.020) 0.038 (0.006) 50-NRMSE 0.165 (0.086) 0.093 (0.040) 0.088 (0.021) 0.084 (0.028) 5-SSIM 0.859 (0.056) 0.856 (0.076) 0.880 (0.026) 0.954 (0.008) 10-SSIM 0.818 (0.064) 0.805 (0.095) 0.835 (0.053) 0.933 (0.021) 50-SSIM 0.663 (0.220) 0.781 (0.087) 0.776 (0.058) 0.799 (0.057)

Wind u direction

5-NRMSE 0.055 (0.009) 0.056 (0.011) 0.053 (0.006) 0.032 (0.006) 10-NRMSE 0.059 (0.008) 0.061 (0.009) 0.060 (0.008) 0.041 (0.010) 50-NRMSE 0.096 (0.030) 0.063 (0.006) 0.070 (0.007) 0.062 (0.005) 5-SSIM 0.505 (0.122) 0.502 (0.141) 0.537 (0.084) 0.814 (0.051) 10-SSIM 0.433 (0.115) 0.415 (0.134) 0.424 (0.120) 0.721 (0.107) 50-SSIM 0.300 (0.251) 0.361 (0.085) 0.267 (0.100) 0.382 (0.068)

Wind v direction

5-NRMSE 0.051 (0.008) 0.051 (0.009) 0.050 (0.006) 0.031 (0.005) 10-NRMSE 0.054 (0.007) 0.054 (0.008) 0.055 (0.007) 0.040 (0.010) 50-NRMSE 0.060 (0.006) 0.057 (0.005) 0.087 (0.025) 0.057 (0.005) 5-SSIM 0.240 (0.159) 0.247 (0.183) 0.300 (0.091) 0.649 (0.098) 10-SSIM 0.163 (0.133) 0.163 (0.150) 0.208 (0.101) 0.499 (0.163) 50-SSIM 0.105 (0.077) 0.093 (0.082) 0.165 (0.193) 0.094 (0.074)

**Table 7.** Training time statistics for different models and tasks. Epoch times are reported as mean ± std (in seconds). For Ours, InfoNCE and entropy (von Neumann entropy) rows correspond to the total per-epoch computation. Notably, the overhead introduced by InfoNCE and von Neumann entropy is marginal, accounting for only a small percentage of the total training time.

. Task Metric VAE KAE KKR PFNN Ours

K´arm´an vortex

Epoch time (s) 172.94 ± 4.11 195.26 ± 3.47 186.47 ± 1.86 182.52 ± 2.53 201.23 ± 1.07 InfoNCE time (s) – – – – 13.78 ± 0.93 Entropy time (s) – – – – 0.97 ± 0.13

Dam Flow

Epoch time (s) 16.21 ± 0.29 16.95 ± 0.33 17.48 ± 0.29 – 18.92 ± 0.36 InfoNCE time (s) – – – – 0.76 ± 0.04 Entropy time (s) – – – – 0.56 ± 0.08

ERA5

Epoch time (s) – 240.20 ± 0.52 224.95 ± 0.54 242.33 ± 0.71 253.24 ± 2.05 InfoNCE time (s) – – – – 15.09 ± 0.80 Entropy time (s) – – – – 7.43 ± 0.64

<!-- Page 42 -->

Published as a conference paper at ICLR 2026

2018-01-01 08:00

Ground Truth KAE KKR PFNN Ours

2018-01-08 08:00

43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504

Error

0 12366 0 12366 0 12366 0 12366

43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504 43802 48703 53603 58504

Error

0 12366 0 12366 0 12366 0 12366

**Figure 16.** Comparison of continuous predictions for the global geopotential starting from 2018 − 01 −01 −00: 00 to 2018 −01 −08 −08: 00. Ground truth are contrasted with predictions from KAE, KKR, PFNN, and our method. Error maps in the lower panels demonstrate that, compared with other models, showing with more stable and accurate results of our model.

<!-- Page 43 -->

Published as a conference paper at ICLR 2026

2018-01-01 08:00

Ground Truth KAE KKR PFNN Ours

2018-01-08 08:00

223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06

Error

0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18

223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06 223.89 250.95 278.00 305.06

Error

0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18 0.00 20.73 41.45 62.18

**Figure 17.** Comparison of continuous predictions for the global temperature starting from 2018 − 01 −01 −00: 00 to 2018 −01 −08 −08: 00. Ground truth are contrasted with predictions from KAE, KKR, PFNN, and our method. Error maps in the lower panels demonstrate that, compared with other models, showing with more stable and accurate results of our model.

<!-- Page 44 -->

Published as a conference paper at ICLR 2026

2018-01-01 08:00

Ground Truth KAE KKR PFNN Ours

2018-01-08 08:00

32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64

Error

0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58

32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64 32.29 8.98 14.33 37.64

Error

0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58 0.00 17.53 35.06 52.58

**Figure 18.** Comparison of continuous predictions for the global u−direction wind starting from 2018−01−01−00: 00 to 2018−01−08−08: 00. Ground truth are contrasted with predictions from KAE, KKR, PFNN, and our method. Error maps in the lower panels demonstrate that, compared with other models, showing with more stable and accurate results of our model.

<!-- Page 45 -->

Published as a conference paper at ICLR 2026

2018-01-01 08:00

Ground Truth KAE KKR PFNN Ours

2018-01-08 08:00

34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60

Error

0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48

34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60 34.89 12.73 9.43 31.60

Error

0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48 0.00 15.83 31.65 47.48

**Figure 19.** Comparison of continuous predictions for the global v−direction wind starting from 2018−01−01−00: 00 to 2018−01−08−08: 00. Ground truth are contrasted with predictions from KAE, KKR, PFNN, and our method. Error maps in the lower panels demonstrate that, compared with other models, showing with more stable and accurate results of our model.

<!-- Page 46 -->

Published as a conference paper at ICLR 2026

(a)

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 1

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 10

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 20

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 30

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 40

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 50

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 60

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 70

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 80

Eigen Values 0.0

0.2

0.4

0.6

0.8

## 1.0 Epoch 90

With Without

(b)

Epoch 1 Epoch 10 Epoch 20 Epoch 30 Epoch 40

Epoch 50 Epoch 60 Epoch 70 Epoch 80 Epoch 90

0

1

2

3

4

5

6

(c)

Epoch 1 Epoch 10 Epoch 20 Epoch 30 Epoch 40

Epoch 50 Epoch 60 Epoch 70 Epoch 80 Epoch 90

0

1

2

3

4

5

6

**Figure 20.** Comparison between γ = 0.0 and γ = 0.5 on the physical simulation task with latent dimension 32. (a) Evolution of the eigenvalue spectrum over training epochs. (b) Heatmap of the latent covariance matrix for γ = 0.0 across epochs. (c) Heatmap of the latent covariance matrix for γ = 0.5 across epochs. With the addition of the von Neumann entropy regularizer, two clear effects emerge during training. First, the latent covariance matrix no longer collapses to a few dominant modes: the eigenvalue distribution becomes more uniform and remains close to full rank throughout optimization (see (a)), indicating that the model learns a richer set of modes rather than compressing them into a low-dimensional subspace. Second, the covariance structure transitions from highly sparse (when γ = 0) to dense and full-rank under entropy regularization (from (b) to (c)), verifying our theoretical prediction in Proposition 5.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 46](2026-ICLR-information-shapes-koopman-representation/page-046-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 47 -->

Published as a conference paper at ICLR 2026

(a)

Epoch

0.0

0.5

1.0

1.5

2.0

2.5

3.0

Total Loss

Total Loss Entropy Loss

0.0

0.1

0.2

0.3

0.4

0.5

Entropy Loss

Kármán Vortex

(b)

Epoch

0

1

2

3

4

5

6

Total Loss

Total Loss Entropy Loss

0.6

0.8

1.0

1.2

1.4

1.6

Entropy Loss

Dam Flow

(c)

Epoch

100

150

200

250

300

350

Total Loss

Total Loss Entropy Loss

0.5

1.0

1.5

2.0

2.5

3.0

3.5

4.0

Entropy Loss

ERA5

**Figure 21.** Visualization of the von Neumann entropy regularization loss and the total training loss over epochs for the physical simulation tasks. The stable behavior of both the total loss and the von Neumann entropy loss indicates that our training procedure is numerically stable and robust across different systems.

<!-- Page 48 -->

Published as a conference paper at ICLR 2026

G.5.2 VISUAL PERCEPTION

**Table 8.** Percentage to Goal (%) for different algorithms under noisy rollout. A higher value indicates that the system reaches closer to the goal within a fixed number of control steps.

Domain E2C PCC KAE Ours

Planar (n = 40 × 40) 6.2 (1.5) 34.8 (3.6) 5.1 (1.2) 39.6 (2.8) Pendulum (n = 48 × 40 × 2) 45.5 (3.9) 59.8 (3.2) 26.3 (2.8) 62.7 (2.9) Cartpole (n = 80 × 80 × 2) 8.1 (1.6) 53.1 (3.5) 57.2 (3.8) 61.9 (3.0) 3-link (n = 80 × 80 × 2) 5.0 (1.0) 21.3 (1.9) 2.1 (0.6) 19.5 (2.0)

**Table 9.** Percentage to Goal (%) for different algorithms under noiseless rollouts.

Domain E2C PCC KAE Ours

Planar (n = 40 × 40) 37.8 (3.5) 71.4 (0.6) 12.2 (1.4) 73.8 (0.5) Pendulum (n = 48 × 40 × 2) 88.5 (0.6) 90.1 (0.5) 68.2 (1.9) 91.5 (0.4) Cartpole (n = 80 × 80 × 2) 39.5 (3.3) 94.1 (1.6) 98.5 (0.3) 97.6 (1.2) 3-link (n = 80 × 80 × 2) 21.5 (0.9) 48.5 (1.6) 11.8 (0.8) 47.9 (1.4)

G.5.3 GRAPH-STRUCTURED DYNAMICS

Time Direction

Rope

Soft

**Figure 22.** Comparison of ground truth and our predictions over time for rope and soft-body dynamics. Top row (Rope): red dots indicate ground truth positions, while blue dots show our predicted trajectories. Middle and bottom rows (Soft): translucent shapes represent ground truth deformations, and solid colored blocks denote our predictions. The time axis progresses from left to right.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 48](2026-ICLR-information-shapes-koopman-representation/page-048-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 49 -->

Published as a conference paper at ICLR 2026

G.5.4 MODEL ARCHITECTURE

**Table 10.** Model architecture for K´arm´an Vortex and Dam Flow task with input dimension (C, H, W), where C denotes the number of velocity components and H × W is the spatial resolution.

Components Layer Layer number C, (H, W) Activation

Encoder

Convolution Block 1 C →8C, (H

2, W 2) ReLU Convolution Block 3 8C →64C, (H 16, W 16) ReLU Convolution2d 1 64C →128C, (H 16, W 16) ReLU Flatten – 128C, (H 16, W 16) →CHW 2 – Fully Connected 1 CHW

2 →ds – Koopman Operator Linear 1 ds →ds –

Decoder

Fully Connected 1 ds →CHW

## 2 ReLU

Transpose – CHW

2 →(128C, H

16, W 16) – ConvTranspose Block 3 128C →8C, (H, W) ReLU ConvTranspose2d 1 8C →C, (H, W) – Conv2d Refinement 3 C →C, (H, W) ReLU

**Table 11.** Model architecture for ERA5 task with input dimension (C, H, W), where C denotes the number of channels and H × W is the spatial resolution, using a factorized-attention encoder.

Components Layer Layer number C, (H, W) Activation

Encoder

Conv2d 1 C →64C

5, (H, W) – Conv2d 1 64C 5 →64C

5, (H 4, W 4) – FactorizedBlock 1 64C 5, (H 4, W 4) GELU Flatten – 64C 5, (H 4, W 4) →4CHW 5 – Fully Connected 1 4CHW 5 →ds – Koopman Operator Linear 1 ds →ds –

Decoder

Fully Connected 1 ds →4CHW

## 5 ReLU

Transpose – 4CHW 5 →(64C

5, H 4, W 4) – ConvTranspose2d 2 64C 5 →64C

5, (H, W) ReLU Conv2d 1 64C 5 →C, (H, W) – Conv2d Refinement 3 C →C, (H, W) ReLU

For fair comparison, the architectures for visual input and graph-structured dynamics follow the settings in Levine et al. (2020) and Li et al. (2020).

**Table 12.** Hyperparameter settings across physical simulations, visual inputs, and graph-structured dynamics

Parameter Symbol Physical Sim. Visual Inputs Graph Dyn.

Temporal coherence α 2.00 3.00 2.00 Structural consistency β – 2.00 – von Neumann entropy γ 0.10 0.50 0.10 InfoNCE neighborhood k 3 5 5

<!-- Page 50 -->

Published as a conference paper at ICLR 2026

G.6 BASELINE ALGORITHMS

Physical Simulation Tasks.

• VAE (Kingma et al., 2013): Baseline implemented using a standard variational autoencoder with a nonlinear forward map in latent space. Code available at https://github. com/bvezilic/Variational-autoencoder.

• KAE (Pan et al., 2023): Koopman learning with an autoencoder architecture. Code available at https://github.com/dynamicslab/pykoopman.

• KKR (Bevanda et al., 2023): For the low-dimensional Lorenz–63 system, we adopt fixed kernel functions as basis following the implementation in https://github. com/TUM-ITR/koopcore. For high-dimensional systems, we use deep kernel features following Yang et al. (2025), with code available at https://github.com/ yyimingucl/TensorVar/blob/main/model/KS_model.py.

• PFNN (Cheng et al., 2025): A state-of-the-art Koopman variant for learning and predicting chaotic dynamics. Code available at https://github.com/Hy23333/PFNN.

Visual Inputs.

• E2C (Banijamali et al., 2019): A latent embedding approach based on the VAE framework. Code available at https://github.com/ericjang/e2c.

• KAE (Pan et al., 2023): Koopman learning with an autoencoder architecture. Code available at https://github.com/dynamicslab/pykoopman.

• PCC (Banijamali et al., 2019): A state-of-the-art latent embedding algorithm also based on the VAE framework. Code available at https://github.com/VinAIResearch/ PCC-pytorch/tree/master/sample_results.

Graph-Structured Dynamics.

• CKO (Li et al., 2020): A Koopman-based framework for learning and predicting general graph-structured dynamics. Code available at https://github.com/YunzhuLi/ CompositionalKoopmanOperators.
