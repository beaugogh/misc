---
title: "Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers"
source_url: https://icml.cc/virtual/2026/oral/71069
paper_pdf_url: https://arxiv.org/pdf/2502.08834v4
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

<!-- Page 1 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Zander W. Blasingame 1 2 Chen Liu 2

## Abstract

Deep generative models based on neural differential equations have become state-of-the-art for many generation tasks. These models rely on ODE/SDE solvers that integrate from a prior distribution to the data distribution; in many applications it is also highly desirable to integrate in the inverse direction. Standard solvers, however, accumulate discretization errors that prohibit exact inversion, an inaccuracy that is unacceptable in precision-critical applications. Existing inversion methods suffer from poor stability and low order of convergence, and are strictly limited to the ODE setting. In this work, we propose Rex, a family of reversible exponential (stochastic) Runge- Kutta solvers obtained by applying Lawson methods to convert any explicit (stochastic) Runge- Kutta scheme into an algebraically reversible one for both diffusion ODEs and SDEs. Beyond a rigorous theoretical analysis—establishing arbitrary-order convergence and a non-zero region of linear stability—we empirically demonstrate that Rex achieves near-machine-precision reconstruction and improves Boltzmann sampling with flow models as well as image generation and editing with diffusion models. Our code is available at: https://github.com/ zblasingame/Rex-solver

## 1. Introduction

Deep generative models based on neural differential equations (Kidger, 2022) have quickly become the state-of-theart in generation tasks across many varied modalities from image generation (Rombach et al., 2022), protein generation (Skreta et al., 2025b), Boltzmann sampling (Rehman et al., 2026a), and biometrics (Blasingame & Liu, 2024d). These models use the language of a neural Itô stochastic differen-

1AITHYRA 2Clarkson University. Correspondence to: ZB <zblasingame@aithyra.at>.

Proceedings of the 43 rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s).

x t 0 T ε

(a) Non-reversible: error ε > 0 x t 0 T ε=0

(b) Reversible: error ε = 0

**Figure 1.** Conventional solvers (left) accumulate discretization

error ε > 0 when integrated forward (solid) and then backward (dashed), so the reconstructed trajectory drifts from the original. Rex (right) is algebraically reversible: the backward step (shaded) lands exactly on the forward iterates, yielding ε = 0 regardless of step size or precision.

tial equation (SDE) (Kidger et al., 2021) or neural ordinary differential equation (ODE) (Chen et al., 2018)—sometimes referred to as a continuous normalizing flow (CNF)—to describe the (stochastic) mapping from a prior source distribution to the target data distribution. This can be achieved through a variety of numerical schemes (Lu et al., 2022b; Zhang et al., 2023; Zhang & Chen, 2023; Gonzalez et al., 2024) which integrate from the source to the target distribution. The exact inversion of this numerical method, i.e., going from the target distribution back to the source distribution, is invaluable in several key applications where precision is concerned. E.g., gradient descent through these models (Ben-Hamu et al., 2024; Blasingame & Liu, 2024a; McCallum & Foster, 2024) for training, fine-tuning, and differentiable rewards; image editing (Wallace et al., 2023; Wang et al., 2024); and calculating accurate likelihoods of the generative models, enabling sampling from Boltzmann distributions (Rehman et al., 2026a).

Whilst useful, designing such inversion methods is very tricky, as such solvers are plagued by issues of low order of convergence, lack of stability, amongst other undesirable properties; moreover, it is even more difficult to construct such schemes for SDEs. Recent work has developed exact inversion methods specifically for diffusion models (Wallace et al., 2023; Zhang et al., 2024; Wang et al., 2024). Unfortunately, these schemes suffer from poor numerical stability which can hamper their real-world utility, particularly in contexts like editing of real samples. Moreover, the arXiv:2502.08834v4 [cs.LG] 2 Jun 2026

<!-- Page 2 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers previous approaches do not support the often useful SDE formulation of diffusion models. Prior work (Nie et al., 2024; Wu & la Torre, 2023) has attempted to tackle SDEs, but these methods resort to storing the entire process in memory, which is only a trivial notion of reversibility.

To address these challenges we propose Rex, a family of reversible exponential (stochastic) Runge-Kutta solvers for diffusion models. Our contributions are:

• We construct Rex, an algebraically reversible family of solvers for both diffusion ODEs and SDEs. The Rex ODE solver inherits arbitrary order of convergence and a nonzero region of linear stability from the McCallum-Foster method, and Rex supports adaptive step sizes.

• We show that Rex is the reversible version of many popular solvers for diffusion models, including DDIM, DPM- Solver, and SEEDS-1.

• We empirically show that Rex achieves near-machineprecision reconstruction under exact inversion, while remaining competitive with prior reversible methods on unconditional generation, text-conditioned generation, and image editing.

• We demonstrate that Rex enables accurate likelihoodbased Boltzmann sampling on tri-alanine.

## 2. Preliminaries

## 2.1. Reversible Solvers

Recently, researchers studying neural differential equations have begun to propose several algebraically reversible solvers. Consider some prototypical neural ODE of the form ˙xt = uθ(t, xt) with vector field uθ ∈Cr(R×Rd; Rd) which satisfies the usual regularity conditions. Then consider a single-step numerical scheme of the form xn+1 = xn + Φh(tn, xn, uθ). Every numerical scheme Φ is reversible in the sense that we can rewrite the forward step as an implicit scheme of the form xn = xn+1 − Φh(tn, xn, uθ); however, this requires fixed point iteration1 and is both approximate and computationally expensive. This type of reversibility is known as analytic reversibility within the neural differential equations community (Kidger, 2022, Section 5.3.2.1). What we would prefer, however, is a form of reversibility that can be expressed in closed-form.

There are only a few such algebraically reversible solvers which have been proposed within the last few years (Zhuang et al., 2021; Kidger et al., 2021; McCallum & Foster, 2024) and only one of these works for SDEs, namely, the work of Kidger et al. (2021). Whilst only for ODEs the recent work of McCallum & Foster (2024) is highly interesting as it is the only algebraically reversible scheme with a non-

1If the step size h is small enough.

zero region of stability. We refer to the method proposed in McCallum & Foster (2024) as the McCallum-Foster method and summarize it below in Definition 2.1. Definition 2.1. Initialize ˆx0 = x0 and let ζ ∈(0, 1]. Consider a step size of h, then a forward step of the McCallum- Foster method is defined as xn+1 = ζxn + (1 −ζ)ˆxn + Φh(tn, ˆxn), (1a) ˆxn+1 = ˆxn −Φ−h(tn+1, xn+1), (1b)

and the backward step is given as

ˆxn = ˆxn+1 + Φ−h(tn+1, xn+1), (2a)

xn = ζ−1xn+1 + (1 −ζ−1)ˆxn −ζ−1Φh(tn, ˆxn). (2b)

## 2.2. Diffusion Models

Diffusion models (Sohl-Dickstein et al., 2015; Ho et al., 2020; Song et al., 2021a;b) have become one of the most popular paradigms for constructing generative models. Consider the following Itô stochastic differential equation (SDE) defined on time interval [0, T]:

dXt = f(t)Xt dt + g(t) dWt, (3)

where f, g ∈C∞([0, T])2 form the drift and diffusion coefficients of the SDE and where {Wt}t∈[0,T ] is the standard Brownian motion on the time interval. The coefficients f, g are chosen such that the SDE maps clean samples from the data distribution X0 ∼q(X) at time 0 to an isotropic Gaussian at time T. More specifically, for a noise schedule αt, σt ∈C∞([0, T]; R≥0) consisting of a strictly monotonically decreasing function αt and strictly monotonically increasing function σt, the drift and diffusion coefficients are given by f(t) = ˙αt αt

, g2(t) = ˙σ2 t −2 ˙αt αt σ2 t, (4)

where, with abuse of notation, ˙σ2 t denotes the time derivative of the function σ2 t (Lu et al., 2022b; Kingma et al., 2021)—this ensures that Xt ∼N(αtX0, σ2 t I). However, we wish to map from noise back to data; as such, we employ the result of Anderson (1982) to construct the reverse-time diffusion SDE of Equation (3), which is given by dXt = [f(t)Xt −g2(t)∇x log pt(Xt)] dt + g(t) dW t,

(5) where dt is a negative timestep, {W t}t∈[0,T ] is the standard Brownian motion in reverse-time, and pt(x):= p(t, x) is the marginal density function. Then, if we can learn the score function (t, x) 7→∇x log pt(x) (Song et al., 2021b)— or some other equivalent reparameterization, e.g., noise

2We let Cr(X; Y) denote the class of r-th differentiable functions from X to Y. If Y is omitted then Y = R.

<!-- Page 3 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers xn + + xn+1

Ψh Ψ−h

ˆxn ˆxn+1 −

× ζ κn ×κn+1

× 1 κn ×κn+1

× 1−ζ κn

(a) Forward step xn − − xn+1

Ψh Ψ−h

ˆxn ˆxn+1 +

× κn ζ × 1 κn+1

×κn × 1 κn+1

×(1 −ζ)

(b) Backward step

**Figure 2.** An overview of the Rex solver. Here Ψh denotes the Princeps scheme (see Section 3.1), ζ ∈(0, 1) is a coupling parameter,

and {κn}N n=1 denotes the set of weighting variables derived from the exponential schemes. The particular values of κn are discussed in Proposition 3.2. The visualization of the computation graph is inspired by McCallum & Foster (2024, Figure 2).

prediction (Song et al., 2021a; Ho et al., 2020) or data prediction (Kingma et al., 2021)—we can then draw samples from our data distribution q(X) by first sampling some XT ∼p(X) from the Gaussian prior and then employing a numerical SDE solver, e.g., Euler-Maruyama, to solve Equation (5) in reverse-time. Notably, through careful massaging of the Fokker-Planck-Kolmogorov equation for the marginal density, one can construct an ODE which is equivalent in distribution to Equation (5) (Song et al., 2021b; Maoutsa et al., 2020), yielding the popular probability flow ODE dxt dt = f(t)xt −g2(t)

2 ∇x log pt(xt). (6)

## 3. Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

In this section we introduce the Rex family of reversible exponential Runge-Kutta solvers. This family of bespoke numerical schemes is specifically tailored to exploit the semi-linear structure of the diffusion ODE/SDE. The elegance of Rex is that it can be built rather generally from many popular pre-existing ODE/SDE solvers. Let Φ denote our explicit (S)RK scheme of choice, e.g., Euler or the Dormand-Prince method. Then we massage the probability flow ODE and reverse-time SDE into a sufficiently nice form and apply Φ—we refer to this construction as Princeps, Ψ. Lastly, we construct a reversible scheme from this nice form of Ψ. We summarize this three-step recipe below.

Rex recipe.

1. Φ: select an explicit (S)RK scheme.

2. Ψ: build Princeps from the RK scheme.

3. Υ: build Rex out of Princeps.

In Figure 2 we present an overview of the Rex computational graph. The graph is identical for both the ODE and SDE formulations; only the weighting terms {κn} and the underlying numerical scheme Ψh differ. The rest of this section is organized as follows: first we construct the Princeps scheme Ψ from some explicit (S)RK scheme Φ in Section 3.1, then we construct Rex, Υ, from Princeps in Section 3.2, and lastly in Section 3.3 we discuss the theoretical properties of Rex.

## 3.1. Princeps

In this section we discuss how to build the underlying scheme, Ψ, from which we construct the reversible Rex scheme. As this scheme is one that is first we hereafter refer to it as the Princeps scheme. For simplicity of presentation we derive Princeps from the reverse-time diffusion SDE in Equation (5); however, this framework generalizes the probability flow ODE formulation, see Equation (6), with the explicit derivations detailed in Appendix C.1.

As the data and noise prediction formulations differ we will derive Princeps from a rather general view of the problem and elide the particular details, reserving them for Appendix C.2. Recall that the Itô SDE in Equation (5) has a semi-linear drift term and additive noise, this nice structure allows us to greatly simplify our discussion. We will rewrite Equation (5) as dXt = [a(t)Xt + b(t)fθ(t, Xt)] dt + g(t) dW t, (7)

where a(t), b(t) are the appropriate generalizations for the data and noise parameterizations and fθ denotes either the noise or data prediction model (see Appendix C; for background see Section 2.2). This form can then be simplified via exponential integrators, i.e., exp −

R t

0 a(τ) dτ, and then a suitable change of variables, the result of which we show in Proposition 3.1 with the proof in Appendix C.2.1.

<!-- Page 4 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers dXt = [a(t)Xt + b(t)fθ(t, Xt)] dt + g(t) dWt dYς = fθ(ς, Ξ(ς)Yς) + dWς

Xn+1 = Ξ(tn) Ξ(tn+1)Xn + Ψh(tn, Xn, Wn(ω)) Yn+1 = Yn + Φh(ςn, Yn, Wn(ω))

Exponential integrators & change-of-variables

Lawson method

**Figure 3.** Construction of the Princeps Ψ for the diffusion SDE in Equation (7) from an underlying explicit stochastic Runge-Kutta

scheme Φ; the probability flow ODE case follows mutatis mutandis.

Proposition 3.1. Assume that g(t) = p a(t)b(t), b(t)/a(t) →∞as t →∞, and b(t) > 0. Let

Ξ(t):= exp

R t

0 a(τ) dτ be the reciprocal of the integrating factor of Equation (7). Then the SDE in Equation (7) can be rewritten as dYς = fθ(ς, Ξ(ς)Yς) dς + dWς, (8)

where Yt = Ξ−1(t)Xt and ςt =

R

Ξ−1(t)b(t) dt.

Remark 3.1. In Appendices C.2.2 and C.2.3 we provide the particular realizations of the time-changed SDE for the data and noise parametrizations.

Proposition 3.1 highlights the first half of constructing Princeps and is the upper pathway in Figure 3. The rest of the section is devoted to constructing the lower pathway, i.e., how we create the exponentially weighted Stochastic Runge-Kutta scheme. The next question is which stochastic Runge-Kutta formulation to use, as unlike in the ODE case there are many possible different formulations to choose from.

Stochastic Runge-Kutta. Constructing a numerical scheme for SDEs is greatly more complicated than ODEs due to the complexities of stochastic processes and in particular stochastic integrals. Unlike numerical schemes for ODEs which are usually built upon truncated Taylor expansions, SDEs require constructing truncated Itô or Stratonovich-Taylor expansions (Kloeden & Platen, 1991) which results in numerous iterated stochastic integrals. Approximating these iterated integrals, or equivalently Lévy areas, of Brownian motion is quite difficult (Clark & Cameron, 2005; Mrongowius & Rößler, 2022); however, SDEs with certain constraints on the diffusion term may use specialized solvers to further achieve a strong order of convergence with simple approximations of these iterated stochastic integrals. As such there are several ways to express SRK methods depending on the choice of approximating these iterated integrals. We choose to follow the work of Foster et al. (2024) which makes usage of the space-time Lévy area in constructing such methods. The space-time Lévy area (see Foster et al., 2020, Definition 3.5; cf. Rößler, 2010) is defined below in Definition 3.2.

Definition 3.2 (Space-time Lévy area). The rescaled spacetime Lévy area of a Brownian motion {Wt} on the interval [s, t] corresponds to the signed area of the associated bridge process

Hs,t:= 1 h

Z t s

Ws,u −u −s h Ws,t du, (9)

where h:= t −s and Ws,u = Wu −Ws for u ∈[s, t].

In particular, for additive-noise SDEs which our SDE in Equation (8) is, the Itô and Stratonovich integrals coincide and the numerical scheme is significantly simpler, for more details we refer to Appendix B.

For the Itô SDE in Equation (8) we follow the conventions of Foster et al. (2024) and write an s-stage SRK as below; this form is a direct generalization of Foster et al. (2024, Equation (6.1)) to an arbitrary extended Butcher tableau (see the diffrax documentation).

f i θ = fθ(ςn + cih, Ξ(ςn + cih)Zi), (10a)

Zi = Yn + h



 i−1 X j=1 aijf j θ





+ aW i Wn + aH i Hn,

(10b)

Yn+1 = Yn + h s X i=1 bif i θ

!

+ bW Wn + bHHn.

(10c)

where h = ςn+1 −ςn is the step size and Wn:= Wtn,tn+1 and Hn:= Htn,tn+1 are the Brownian and Lévy increments respectively; and where aij, aW i, aH i ∈Rs×s, bi, bW, bH ∈Rs, and ci ∈Rs are the coefficients of an extended Butcher tableau (cf. Rößler, 2025; Foster et al., 2024); cf. the deterministic ODE setting in Stewart (2022, Section 6.1.4). Then by straightforward substitution for the identity of Y we arrive at the Princeps scheme denoted Ψ in Equation (11) below (see Appendices C.2.2 and C.2.3 for

<!-- Page 5 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers the explicit data and noise prediction realizations).

f i θ = fθ(ςn + cih, Ξ(ςn + cih)Zi), (11a)

Zi = Ξ−1(ςn)Xn + h



 i−1 X j=1 aijf j θ





+ aW i Wn + aH i Hn,

(11b)

Xn+1 = Ξ(ςn+1)

Ξ(ςn) Xn

+ Ξ(ςn+1)

" h s X i=1 bif i θ

!

+ bW Wn + bHHn

#

| {z } =:Ψ

,

(11c)

from which we will build the Rex scheme.

## 3.2. Rex

Equipped with Equation (11) we are now ready to construct Rex. The key idea is to construct a reversible scheme from an explicit (S)RK scheme (we provide more detail in Appendix B) for the reparameterized differential equation using the McCallum-Foster method and then apply Lawson methods to bring the scheme back to the original state variable; see Figure 3. We provide a brief summary below; the full derivation is in Appendix C.3.

Proposition 3.2 (Rex). Without loss of generality let Φ denote an explicit SRK scheme for the SDE in Equation (8) with extended Butcher tableau aij, bi, ci, aW i, aH i, bW, bH. Fix an ω ∈Ωand let W be the Brownian motion over time variable ς. Then the reversible solver constructed from Φ in terms of the underlying state variable Xt is given by the forward step

Xn+1 = κn+1 κn ζXn + (1 −ζ) ˆ Xn

+ κn+1Ψh(ςn, ˆ Xn, Wn(ω)),

ˆ Xn+1 = κn+1 κn

ˆ Xn −κn+1Ψ−h(ςn+1, Xn+1, Wn(ω)),

(12) and backward step

ˆ Xn = κn κn+1

ˆ Xn+1 + κnΨ−h(ςn+1, Xn+1, Wn(ω)),

Xn = κn κn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn

−κnζ−1Ψh(ςn, ˆ Xn, Wn(ω)),

(13) with step size h:= ςn+1 −ςn and where Ψ follows Equation (11) with κn = Ξ(ςn).

Remark 3.3. We can recover all four cases with the appropriate choice of weighting coefficient and time variable. For data prediction SDEs we have, κn = σn γn and ςt = α2 n σ2n; the ODE case is recovered for an explicit RK scheme with κn = σn and ςt = αn σn. For noise prediction models we have fθ denoting the noise prediction model with κn = αn and ςt = σn αn. The Brownian motion has a slightly different time-change in the noise prediction formulation; we defer the nuances to Appendix C.2.3.

We now justify the design choices in Proposition 3.2, in particular our handling of stochasticity. The key idea is to use the same realization of the Brownian motion in both the forward pass and backward pass. This has been explored in prior works studying the continuous adjoint equations for neural SDEs (Li et al., 2020; Kidger et al., 2021) and essentially amounts to fixing the realization of the Brownian motion along with clever strategies for reconstructing the same realization of the Brownian motion.

Numerical Simulation of the Brownian Motion. The naïve approach to fixing the realization is to cache the entire trajectory, which is both expensive and prohibits adaptive step-size solvers. Instead, recent work by Li et al. (2020); Kidger et al. (2021); Jelinˇciˇc et al. (2024) enables one to recalculate any realization of the Brownian motion from a single seed given access to a splittable pseudo-random number generator (PRNG) (Salmon et al., 2011); we adopt this approach and discuss the technical details in Appendix F.3.

## 3.3. Properties of Rex

Convergence Order. A nice property of the McCallum- Foster method is that the convergence order of the underlying explicit RK scheme Φ is inherited by the resulting reversible scheme (McCallum & Foster, 2024, Theorem 2.1). However, does this property hold true for Rex? We show that Rex can achieve an arbitrarily high order of convergence in Theorem 3.3 with the proof provided in Appendix D.2.

Theorem 3.3 (Rex is a k-th order solver). Let Φ be a k-th order explicit Runge-Kutta scheme for the reparameterized probability flow ODE in Equation (87) with variance preserving noise schedule (αt, σt). Then Rex constructed from Φ is a k-th order solver, i.e., given the reversible solution {xn, ˆxn}N n=1 and true solution xtn we have

∥xn −xtn∥≤Chk, (14)

for constants C, hmax > 0 and for step sizes h ∈ [0, hmax].

This result is for the ODE case; we refer to the generalized formulation of the probability flow ODE in Equation (87). Therefore, Rex inherits the convergence order of the base

<!-- Page 6 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers scheme, Φ, used to construct Princeps. As a clear corollary we have

Corollary 3.3.1. Let Φ be a k-th order explicit Runge- Kutta scheme for the reparameterized probability flow ODE in Equation (87) with variance preserving noise schedule (αt, σt). Then Princeps constructed from Φ is a k-th order solver.

An analogous result can be shown for the Princeps scheme for diffusion SDEs, i.e., that it inherits the strong order of convergence from the underlying SRK scheme Φ. We show this below with the full proof provided in Appendix D.3.

Theorem 3.4 (Convergence order for Princeps). Let Φ be a SRK scheme with strong order of convergence ξ > 0 for the reparameterized reverse-time diffusion SDE in Equation (8) with variance preserving noise schedule (αt, σt) and αT > 0. Then Ψ constructed from Φ has strong order of convergence ξ.

Relation to Existing Solvers. Next we show that several variants of Rex are actually the reversible versions of several well-known solvers in the literature for diffusion models, e.g., the DPM-Solvers (Lu et al., 2022b). We first begin by showing that Princeps subsumes many popular previous solvers developed for diffusion models in Theorem 3.5 with the full derivations in Appendix E.

Theorem 3.5 (Princeps subsumes previous solvers). Princeps subsumes the following solvers for diffusion models 1. DDIM (Song et al., 2021a),

2. DPM-Solver-1, DPM-Solver-2, DPM-Solver-12 (Lu et al., 2022b),

3. DPM-Solver++1, DPM-Solver++(2S), SDE-DPM- Solver-1, SDE-DPM-Solver++1 (Lu et al., 2022a),

4. SEEDS-1 (Gonzalez et al., 2024), and

5. gDDIM (Zhang et al., 2023).

As a natural corollary we have that Rex is then the reversible version of these highly popular solvers for diffusion models, i.e., we have that Rex (Euler) is Reversible DDIM &c.

Corollary 3.5.1. Rex is the reversible version of the wellknown solvers for diffusion models in Theorem 3.5.

Stability. One drawback of reversible solvers is their rather unimpressive stability, in fact until the work of Mc- Callum & Foster (2024) there were no reversible methods which had a non-zero region of stability. We discuss this in more detail in Appendix A.2 along with illustrating the poor stability characteristics of BDIA and O-BELM (see Corollaries A.4.1 and A.3.2). However, since Rex is built upon the McCallum-Foster method, the ODE solver has

DDIM EDICT BDIA O-BELM Rex

10−10

10−8

10−6

10−4

10−2

100

Latent MSE

10 steps 20 steps 50 steps

**Figure 4.** Latent-space reconstruction MSE at FP32 precision (log

scale; lower is better) for Stable Diffusion v1.5 (512 × 512, CFG 1.0) over 100 real images. Rex (Euler) is orders of magnitude below all baselines. Full numbers in Table 4.

a non-zero region of stability.3 This property will prove valuable later in our empirical studies.

## 4. Empirical Results

In this section we conduct a number of empirical studies to illustrate the utility of Rex in two major contexts. We primarily explore this in two contexts: 1) image generation and editing with exact inversion, and 2) ensuring invertibility for accurate likelihood calculations for Boltzmann sampling. Unless stated otherwise ζ = 0.999 for all experiments (see Appendix A.2 for the rationale behind this choice).

## 4.1. Reconstruction Error Under Finite Precision

While Rex is algebraically reversible, finite-precision arithmetic on GPUs can in principle break strict reversibility. We measure the round-trip reconstruction error (forward solve followed by reverse solve) over 100 real images from the pix2pix dataset encoded with Stable Diffusion v1.5 at 512 × 512, reporting latent-space MSE to exclude VAE reconstruction error from the measurement. Figure 4 summarizes the FP32 results across 10, 20, and 50 steps with CFG scale 1.0; Rex (Euler) is the most accurate solver at every step count, by one to several orders of magnitude over most baselines. Notably, O-BELM’s error grows with steps—consistent with its lack of a non-trivial linear stability region (see Appendix A.2). Full results (FP16 and pixel-space MSE) and additional discussion are deferred to Appendix H.1.

## 4.2. Image Generation

## 4.2.1. UNCONDITIONAL IMAGE GENERATION

Following prior works (Wang et al., 2024; Wallace et al., 2023), we begin by evaluating Rex as a standard sampling solver for diffusion models. To evaluate this we drew 104

3I.e., in the sense of the linear test equation, see Appendix A.2 for more details.

<!-- Page 7 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

0.5

10 steps

FD

FD∞

Precision

Recall

Density

Coverage 0.5

20 steps

FD

FD∞

Precision

Recall

Density

Coverage 0.5

50 steps

FD

FD∞

Precision

Recall

Density

Coverage

EDICT DDIM BDIA O-BELM

Rex (Midpoint) Rex (RK4) Rex (Euler-Maruyama) [SDE]

**Figure 5.** Radar charts comparing reversible solvers for unconditional image generation on CelebA-HQ (256 × 256) with a pre-trained

DDPM at 10, 20, 50 steps. Six metrics (FD, FD∞, Precision, Recall, Density, Coverage); Rex (Euler-Maruyama, mauve) attains the largest polygon at 20 and 50 steps. Raw values in Table 5.

(a) DDIM (b) EDICT (c) BDIA (d) O-BELM (e) Rex (RK4)

**Figure 6.** Qualitative comparison of unconditional sampling on

CelebA-HQ (256×256) with a pre-trained DDPM at 10 discretization steps; non-reversible DDIM included as a baseline.

samples using a DDPM model (Ho et al., 2020) pre-trained on the CelebA-HQ (Karras et al., 2018) dataset with the various solvers, each using the same fixed seed. Following Stein et al. (2023), we report the Fréchet distance (FD) using a DINOv2 (Oquab et al., 2023) feature extractor along with FD∞(Chong & Forsyth, 2020). We also report precision and recall (Kynkäänniemi et al., 2019) along with density and coverage (Naeem et al., 2020), which together proxy fidelity and sample diversity.

In Table 5 we compare pre-existing methods for exact inversion with diffusion models against Rex, and include the nonreversible DDIM (Song et al., 2021a) solver as a baseline. The Rex family performs strongly, outperforming EDICT (Wallace et al., 2023) and BDIA (Zhang et al., 2024) by a wide margin and frequently outperforming O-BELM (Wang et al., 2024); Rex even surpasses the non-reversible DDIM baseline. Our reversible SDE scheme performs well outside of the small step-size regime, a well-known limitation of SDE schemes. Unlike the other reversible solvers, Rex’s hyperparameters were not tuned for this benchmark. In Figure 6 we present a visual qualitative comparison of the different solvers using the same initial noise. We provide additional experimental details in Appendix G.1.

For a discussion of why higher-order Rex (RK4) underper-

(a) DDIM (b) EDICT (c) BDIA (d) BELM (e) Rex

**Figure 7.** Qualitative comparison of text-to-image sampling with

Stable Diffusion v1.5 (512 × 512) at 10 discretization steps. Prompts (top to bottom): “White plate with fried fish and lemons sitting on top of it.”, “A lady enjoying a meal of some sort.”, “A young boy riding skis with ski poles.”.

forms lower-order Rex (Euler) and the SDE variant on this benchmark, see Appendix H.2.

## 4.2.2. CONDITIONAL IMAGE GENERATION

To further evaluate Rex we drew text-conditioned samples using Stable Diffusion v1.5 (Rombach et al., 2022) from 1000 randomly selected COCO captions (Lin et al., 2014), with the various solvers each using the same fixed seed. We report performance in terms of the CLIP Score (Hessel et al., 2021), the state-of-the-art text-to-image scoring function PickScore (Kirstain et al., 2023), and the Image Reward metric (Xu et al., 2023), which assigns a score reflecting human preferences—namely, aesthetic quality and prompt adherence—and has recently become a popular evaluation metric for diffusion models (Skreta et al., 2025a). In Table 6

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-007-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

10

20

50

10

20 50

10

20

50

CLIP (↑)

Image Reward (↑)

PickScore (↑)

EDICT DDIM BDIA (γ=0.5)

O-BELM Rex (Midpoint) Rex (RK4)

Rex (E-M) [SDE] Rex (ShARK) [SDE]

**Figure 8.** Radar chart comparing reversible solvers for text-to-

image generation with Stable Diffusion v1.5 (512 × 512) on 1000 COCO captions. Three metrics (CLIP score, Image Reward, PickScore), each split across 10/20/50 sampling steps; axes normalised to CLIP ∈[27, 32], Image Reward ∈[−1.4, 0.4], PickScore ∈[19, 22]. Raw values in Table 6.

we compare pre-existing methods for exact inversion with diffusion models against Rex, and include the non-reversible DDIM solver as a baseline. We observe that every Rex variant outperforms the other reversible solvers across all three metrics; the stochastic variants (Euler-Maruyama and ShARK) lead on Image Reward and PickScore. In Figure 7 we present a visual qualitative comparison of the different solvers using the same initial noise. We provide additional experimental details in Appendix G.2.

## 4.3. Image Editing

A central application of exact-inversion solvers is round-trip image editing: given a real image x0 and a source caption csrc, the solver inverts x0 to a latent xT, after which the diffusion model is re-sampled from xT under a new edit caption cedit to produce an edited image x′

0. The quality of the edit depends critically on the fidelity of the inversion: any reconstruction error propagates into spurious changes to regions that the prompt does not target. We follow Brooks et al. (2023) and use the pix2pix dataset, in which each example pairs an image with both a source description (e.g., “a man riding a horse”) and an editing instruction (e.g., “have him ride a dragon”). For each pair we invert x0 to time t = 0.6 using csrc and then re-sample back to t = 0 using cedit. In addition to the CLIP Score, Image Reward, and PickScore metrics used previously, we evaluate LPIPS

Image Reward (↑)

CLIP (↑)

PickScore (↑)

LPIPS (↓)

DDIM BDIA O-BELM

Rex (Euler) Rex (Dopri5)

**Figure 9.** Radar chart comparing reversible solvers on round-

trip image editing with Stable Diffusion v1.5 on the pix2pix dataset (50 inversion + 50 generation steps); LPIPS is inverted to 1 −LPIPS. Raw values in Table 7.

(Zhang et al., 2018) between x0 and x′

0 to measure the perceptual preservation of non-edited content; further setup details are in Appendix G.3.

**Figure 9.** summarises the results, with raw numbers in Table 7. Both the fixed-step Rex (Euler) and adaptive-step Rex (Dopri5) match or exceed the non-reversible DDIM baseline on every metric. LPIPS, the most direct measure of edit faithfulness, drops from 0.214 (DDIM) and 0.140 (O-BELM) to 0.107 for Rex (Dopri5)—roughly a 2× improvement over the strongest reversible baseline—while Image Reward and PickScore likewise top the table. BDIA fails catastrophically (LPIPS 0.885, Image Reward −2.21), consistent with its lack of a non-zero region of stability (see Appendix A.2 and Corollary A.3.2). We omit EDICT from Figure 9 entirely because it collapsed to the (approximate) identity map on this benchmark, producing edited images visually indistinguishable from the source. We highlight that Rex (Dopri5) is, to our knowledge, the first adaptive step-size reversible solver applied to diffusion editing.

## 4.4. Boltzmann Sampling

We evaluate the usefulness of Rex on equilibrium conformation sampling of tri-alanine. In particular, we are interested in drawing samples from a target Boltzmann distribution ptarget defined on Rd as ptarget(x) ∝exp (−E(x)), (15)

where E: Rd →R is the energy of the system which can be efficiently computed for any x. The Boltzmann distribution is notoriously difficult to sample with classical simulation-based techniques such as molecular dynamics;

<!-- Page 9 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers instead, recent work has turned to deep generative models equipped with exact likelihoods, trained on a small biased dataset. This biased model can then be corrected using selfnormalized importance sampling (Liu & Liu, 2001). Chen et al. (2018) showed that the exact likelihood of a neural ODE with learnt vector field uθ t can be found as the solution to the following augmented ODE xt log pθ t(xt)

= x0 log pθ

0(x0)

+

Z t

0 uθ s(xs) −

∇x, uθ s(xs)

ds.

(16) In practice, however, one has to use a discretized numerical scheme Φ, yet its inverse Φ−1 may not exist. This means the change-of-variables used to compute probabilities may not be valid any longer, introducing errors; as discussed in Rehman et al. (2026a), this can pose a significant problem if not properly addressed. Rex, denoted Υ, is reversible by construction: Υ−1 exists, so the change-of-variables yields proper probabilities up to discretization error.

Baselines. We compare against a broad variety of standard baselines which includes equivariant CNFs (Klein et al., 2023). In particular, we compare against an improved version, dubbed ECNF++, proposed by Tan et al. (2025a), which introduces a modified flow matching loss, a deeper architecture, an improved optimizer and learning rate schedule, and exponential moving average. We additionally compare to discrete normalizing flows in RegFlow (Rehman et al., 2026b) and the state-of-the-art Sequential Boltzmann Generator (SBG) (Tan et al., 2025a). Following Rehman et al. (2026a), we train our own diffusion transformer (DiT) (Peebles & Xie, 2023) on tri-alanine, which represents our final baseline. All the CNFs used the Dormand-Prince method (Dormand & Prince, 1980), a 5th-order Runge-Kutta scheme with an embedded 4th-order method for adaptive step sizing; the Butcher tableau is from Shampine (1986), and we use atol = rtol = 10−5.

**Table 1.** Quantitative results on tri-alanine over 104 samples. Best

in bold, second best underlined.

## Model

Numerical scheme ESS (↑) E-W2(↓) T-W2(↓)

RegFlow - 0.029 1.051 1.612 SBG (IS) - 0.052 0.758 0.502 SBG (SMC) - - 0.598 0.503 ECNF++ Dopri5 0.003 2.206 0.962 DiT Dopri5 0.140 0.737 0.468 DiT Rex (Dopri5) 0.104 0.495 0.497

Results. In Table 1 we report the results of the sampling from the Boltzmann distribution in terms of the effective sample size (ESS) and the 2-Wasserstein distance between both the energy distributions (E-W2) and dihedral angles (T-W2)—further info on these metrics is provided in Appendix G.5.3. We see that applying the reversible Rex (Dopri5) to the DiT improves the E-W2 metric to the best in the table, with a modest drop in ESS and a small increase in T-W2; all three remain competitive with the state-of-the-art. We note that for this experiment we choose ζ = 0.001: we do not need to invert the solver exactly, only to guarantee that the scheme is invertible, leaving us free to optimize for stability (see Appendix A.2). A qualitative comparison of the resulting energy distributions is provided in Figure 11.

## 5. Related Work

As mentioned earlier in the preliminaries (see Section 2.1), there have been several works which have explored algebraically reversible schemes for (neural) differential equations, namely, the asynchronous leapfrog method (Mutze, 2013; Zhuang et al., 2021), reversible Heun method (Kidger et al., 2021), and McCallum-Foster method (McCallum & Foster, 2024). We discuss these methods in more detail in Appendix A.1. Contemporary work by Shmelev & Salvi (2025) explores approximately invertible stochastic Runge- Kutta schemes.

Within the literature on diffusion models, the work on solvers for these models (see Song et al., 2021a; Lu et al., 2022b;a; Zhang et al., 2023) is relevant to our discussion on Princeps (see Theorem 3.5), in particular, the work by Gonzalez et al. (2024) which we discuss in more detail in Appendix A.4. Additionally, a few works have explored the exact inversion of diffusion models which we discuss in great detail in Appendix A.3.

## 6. Conclusion

We propose Rex, a family of reversible exponential (stochastic) Runge-Kutta solvers for diffusion models which can obtain an arbitrarily high order of convergence (for the ODE case). The construction also naturally admits reversible adaptive step-size solvers, enabling key AI4Science applications. Moreover, to the best of our knowledge, we propose the first method for exact inversion of diffusion SDEs without storing the entire trajectory of the Brownian motion. We also showed that Princeps subsumes several previous popular solvers, recovering reversible versions of these schemes. Our empirical studies show that Rex is both theoretically well-motivated and a capable, robust numerical scheme across a range of diffusion-model tasks. While we have presented Rex primarily in the context of diffusion models, the construction is substantially more general: it applies to any additive-noise SDE that can be written in the semi-linear form. This covers a broad class of generative models, including all the standard affine probability path flow matching formulations. Rex can be incorporated into existing applications in which preserving the bijectivity of flow maps is important.

<!-- Page 10 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

## Acknowledgements

ZB thanks Sam McCallum for his feedback and insight on material related to the McCallum-Foster method, ShARK, and space-time Lévy area. ZB also wishes to acknowledge Alexander Tong and Danyal Rehman for their feedback on the Boltzmann generator experiments; and Danyal Rehman for generously providing a pre-trained DiT checkpoint for our Boltzmann sampling experiments.

Impact Statement

We recognize that improving generative AI efficiency carries broader societal risks, including: (1) misuse for synthetic media generation, where more efficient inversion lowers the barrier to creating deepfakes or deceptive content; (2) amplification of training-data biases in higher-fidelity outputs; and (3) increased accessibility of generative tools, which may facilitate disinformation at scale.

## References

Adamu, I. A. Numerical approximation of SDEs & the stochastic Swift-Hohenberg equation. Ph.d. thesis, Heriot-Watt University, 2011. URL https: //www.ros.hw.ac.uk/bitstream/handle/ 10399/2460/AdamuIA_0711_macs.pdf.

Anderson, B. D. Reverse-time diffusion equation models.

Stochastic Processes and their Applications, 12(3):313– 326, 1982.

Ben-Hamu, H., Puny, O., Gat, I., Karrer, B., Singer, U., and Lipman, Y. D-flow: Differentiating through flows for controlled generation. In Forty-first International Conference on Machine Learning, 2024. URL https: //openreview.net/forum?id=SE20BFqj6J.

Blasingame, Z. W. and Liu, C. AdjointDEIS: Efficient gra- dients for diffusion models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024a. URL https://openreview.net/forum? id=fAlcxvrOEX.

Blasingame, Z. W. and Liu, C. Fast-dim: Towards fast diffusion morphs. IEEE Security & Privacy, 2024b.

Blasingame, Z. W. and Liu, C. Greedy-dim: Greedy al- gorithms for unreasonably effective face morphs. In 2024 IEEE International Joint Conference on Biometrics (IJCB), pp. 1–11, 2024c. doi: 10.1109/IJCB62174. 2024.10744517.

Blasingame, Z. W. and Liu, C. Leveraging diffusion for strong and high quality face morphing attacks. IEEE Transactions on Biometrics, Behavior, and Identity Sci- ence, 6(1):118–131, 2024d.

Blasingame, Z. W. and Liu, C. Greed is good: A unifying perspective on guided generation. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/ forum?id=s14pdQgoLb.

Bourgade, P. Stochastic analysis, 2010. URL https://cims.nyu.edu/~bourgade/ SA2010/StochasticAnalysis.pdf.

Brooks, T., Holynski, A., and Efros, A. A. Instructpix2pix:

Learning to follow image editing instructions. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 18392–18402, 2023.

Burrage, K. and Burrage, P. M. Order conditions of stochas- tic runge–kutta methods by b-series. SIAM Journal on Numerical Analysis, 38(5):1626–1646, 2000.

Butcher, J. C. Numerical methods for ordinary differential equations. John Wiley & Sons, 2016. Third Edition.

Cardano, G. Artis Magnæ, Sive de Regulis Algebraicis, Lib.

unus. 1545.

Chen, R. T., Rubanova, Y., Bettencourt, J., and Duvenaud,

D. K. Neural ordinary differential equations. Advances in neural information processing systems, 31, 2018.

Chong, M. J. and Forsyth, D. Effectively unbiased fid and inception score and where to find them. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 6070–6079, 2020.

Claessen, K. and Pałka, M. H. Splittable pseudorandom number generators using cryptographic hashing. ACM SIGPLAN Notices, 48(12):47–58, 2013.

Clark, J. M. and Cameron, R. The maximum rate of conver- gence of discrete approximations for stochastic differential equations. In Stochastic Differential Systems Filtering and Control: Proceedings of the IFIP-WG 7/1 Working Conference Vilnius, Lithuania, USSR, Aug. 28–Sept. 2, 1978, pp. 162–171. Springer, 2005.

Crouzeix, M. and Lisbona, F. The convergence of variable- stepsize, variable-formula, multistep methods. SIAM journal on numerical analysis, 21(3):512–534, 1984.

Debrabant, K., Kværnø, A., and Mattsson, N. C. Runge– kutta lawson schemes for stochastic differential equations. BIT Numerical Mathematics, 61(2):381–409, 2021.

DeBruine, L. and Jones, B. Face Research Lab London Set, 5 2017. URL https: //figshare.com/articles/dataset/Face_

Research_Lab_London_Set/5047666.

<!-- Page 11 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Dinh, L., Krueger, D., and Bengio, Y. Nice: Non-linear independent components estimation, 2015. URL https: //arxiv.org/abs/1410.8516.

Domingo-Enrich, C., Drozdzal, M., Karrer, B., and Chen,

R. T. Q. Adjoint matching: Fine-tuning flow and diffusion generative models with memoryless stochastic optimal control. In The Thirteenth International Conference on Learning Representations, 2025. URL https: //openreview.net/forum?id=xQBRrtQM8u.

Dormand, J. R. and Prince, P. J. A family of embedded

Runge–Kutta formulae. J. Comp. Appl. Math, 6:19–26, 1980.

Dowson, D. and Landau, B. The fréchet distance between multivariate normal distributions. Journal of multivariate analysis, 12(3):450–455, 1982.

Dubins, L. E. and Schwarz, G. On continuous martingales.

Proceedings of the National Academy of Sciences, 53(5): 913–916, 1965.

Feng, K. On difference schemes and symplectic geometry.

In Proceedings of the 5th international symposium on differential geometry and differential equations, 1984.

Foster, J., Lyons, T., and Oberhauser, H. An optimal polyno- mial approximation of brownian motion. SIAM Journal on Numerical Analysis, 58(3):1393–1421, 2020.

Foster, J. M. Numerical approximations for stochastic differ- ential equations. Ph.d. thesis, University of Oxford, 2020. URL https://ora.ox.ac.uk/objects/uuid: 775fc3f5-501c-425f-8b43-fc5a7b2e4310.

Foster, J. M., Dos Reis, G., and Strange, C. High order splitting methods for sdes satisfying a commutativity condition. SIAM Journal on Numerical Analysis, 62(1):500– 532, 2024.

Friz, P. K. and Hairer, M. A course on rough paths. Springer,

2020.

Gaines, J. G. and Lyons, T. J. Variable step size control in the numerical solution of stochastic differential equations. SIAM Journal on Applied Mathematics, 57(5):1455–1484, 1997.

Gonzalez, M., Fernandez Pinto, N., Tran, T., Hajri, H., Mas- moudi, N., et al. Seeds: Exponential sde solvers for fast high-quality sampling from diffusion models. Advances in Neural Information Processing Systems, 36, 2024.

Greydanus, S., Dzamba, M., and Yosinski, J. Hamiltonian neural networks. In Wallach, H., Larochelle, H., Beygelzimer, A., d'Alché-Buc, F., Fox, E., and Garnett, R. (eds.), Advances in Neural Information

Processing Systems, volume 32. Curran Associates, Inc., 2019. URL https://proceedings.neurips. cc/paper_files/paper/2019/file/ 26cd8ecadce0d4efd6cc8a8725cbd1f8-Paper. pdf.

Hessel, J., Holtzman, A., Forbes, M., Bras, R. L., and Choi,

Y. Clipscore: A reference-free evaluation metric for im- age captioning. arXiv preprint arXiv:2104.08718, 2021.

Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B., and

Hochreiter, S. Gans trained by a two time-scale update rule converge to a local nash equilibrium. Advances in neural information processing systems, 30, 2017.

Ho, J., Jain, A., and Abbeel, P. Denoising diffusion proba- bilistic models. Advances in neural information processing systems, 33:6840–6851, 2020.

Jayasumana, S., Ramalingam, S., Veit, A., Glasner, D.,

Chakrabarti, A., and Kumar, S. Rethinking fid: Towards a better evaluation metric for image generation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 9307–9315, 2024.

Jelinˇciˇc, A., Foster, J., and Kidger, P. Single-seed gener- ation of brownian paths and integrals for adaptive and high order sde solvers. arXiv preprint arXiv:2405.06464, 2024.

Jolicoeur-Martineau, A., Li, K., Piché-Taillefer, R., Kach- man, T., and Mitliagkas, I. Gotta go fast with score-based generative models. In The Symbiosis of Deep Learning and Differential Equations, 2021. URL https: //openreview.net/forum?id=gEoVDSASC2h.

Karras, T., Aila, T., Laine, S., and Lehtinen, J. Progres- sive growing of GANs for improved quality, stability, and variation. In International Conference on Learning Representations, 2018. URL https://openreview. net/forum?id=Hk99zCeAb.

Kidger, P. On Neural Differential Equations. Ph.d. the- sis, Oxford University, 2022. Available at https: //arxiv.org/abs/2202.02435.

Kidger, P., Foster, J., Li, X. C., and Lyons, T. Efficient and accurate gradients for neural sdes. Advances in Neural Information Processing Systems, 34:18747–18761, 2021.

Kingma, D., Salimans, T., Poole, B., and Ho, J. Varia- tional diffusion models. Advances in neural information processing systems, 34:21696–21707, 2021.

Kirstain, Y., Polyak, A., Singer, U., Matiana, S., Penna, J., and Levy, O. Pick-a-pic: An open dataset of user preferences for text-to-image generation. In Thirty-seventh Conference on Neural Information Processing Systems,

<!-- Page 12 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

2023. URL https://openreview.net/forum? id=G5RwHpBUv0.

Kish, L. Confidence intervals for clustered samples. Ameri- can Sociological Review, 22(2):154–165, 1957.

Klein, L. and Noé, F. Transferable boltzmann generators, 2025. URL https://arxiv.org/abs/2406. 14426.

Klein, L., Krämer, A., and Noé, F. Equivariant flow match- ing. Advances in Neural Information Processing Systems, 36:59886–59910, 2023.

Kloeden, P. E. and Platen, E. Stratonovich and itô stochastic taylor expansions. Mathematische Nachrichten, 151(1): 33–50, 1991.

Kloeden, P. E. and Platen, E. Stochastic Differential Equations, pp. 103–160. Springer Berlin Heidelberg, Berlin, Heidelberg, 1992. ISBN 978-3-662-12616-5. doi: 10.1007/978-3-662-12616-5_4. URL https://doi. org/10.1007/978-3-662-12616-5_4.

Kobayashi, K. Stochastic calculus for a time-changed semi- martingale and the associated stochastic differential equations. Journal of Theoretical Probability, 24(3):789–820, 2011.

Komori, Y., Cohen, D., and Burrage, K. Weak second order explicit exponential runge–kutta methods for stochastic differential equations. SIAM Journal on Scientific Computing, 39(6):A2857–A2878, 2017.

Kynkäänniemi, T., Karras, T., Laine, S., Lehtinen, J., and

Aila, T. Improved precision and recall metric for assessing generative models. Advances in neural information processing systems, 32, 2019.

Kynkäänniemi, T., Karras, T., Aittala, M., Aila, T., and

Lehtinen, J. The role of imagenet classes in fréchet inception distance. In The Eleventh International Conference on Learning Representations, 2023. URL https: //openreview.net/forum?id=4oXTQ6m_ws8.

Li, J., Li, D., Xiong, C., and Hoi, S. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In International conference on machine learning, pp. 12888–12900. PMLR, 2022.

Li, X., Wong, T.-K. L., Chen, R. T. Q., and Duvenaud, D.

Scalable gradients for stochastic differential equations. In Chiappa, S. and Calandra, R. (eds.), Proceedings of the Twenty Third International Conference on Artificial Intelligence and Statistics, volume 108 of Proceedings of Machine Learning Research, pp. 3870–3882. PMLR, 26– 28 Aug 2020. URL https://proceedings.mlr. press/v108/li20i.html.

Lin, S., Liu, B., Li, J., and Yang, X. Common diffusion noise schedules and sample steps are flawed. In Proceedings of the IEEE/CVF winter conference on applications of computer vision, pp. 5404–5411, 2024.

Lin, T.-Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ra- manan, D., Dollár, P., and Zitnick, C. L. Microsoft coco: Common objects in context. In European conference on computer vision, pp. 740–755. Springer, 2014.

Lipman, Y., Havasi, M., Holderrieth, P., Shaul, N., Le, M.,

Karrer, B., Chen, R. T., Lopez-Paz, D., Ben-Hamu, H., and Gat, I. Flow matching guide and code. arXiv preprint arXiv:2412.06264, 2024.

Liu, J. S. and Liu, J. S. Monte Carlo strategies in scientific computing, volume 10. Springer, 2001.

Loshchilov, I. and Hutter, F. Decoupled weight decay regu- larization. arXiv preprint arXiv:1711.05101, 2017.

Lowther, G. Time-changed brownian motion, 2010. URL https://almostsuremath.com/2010/04/ 20/time-changed-brownian-motion/.

Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C., and Zhu, J. Dpm- solver++: Fast solver for guided sampling of diffusion probabilistic models. arXiv preprint arXiv:2211.01095, 2022a.

Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C., and Zhu, J.

DPM-solver: A fast ODE solver for diffusion probabilistic model sampling in around 10 steps. In Oh, A. H., Agarwal, A., Belgrave, D., and Cho, K. (eds.), Advances in Neural Information Processing Systems,

2022b. URL https://openreview.net/forum? id=2uAaGwlP_V.

Lyons, T. J. Differential equations driven by rough sig- nals. Revista Matemática Iberoamericana, 14(2):215– 310, 1998.

Maoutsa, D., Reich, S., and Opper, M. Interacting particle solutions of fokker–planck equations through gradient– log–density estimation. Entropy, 22(8):802, 2020.

Matsubara, T., Miyatake, Y., and Yaguchi, T. Symplectic adjoint method for exact gradient of neural ode with minimal memory. In Ranzato, M., Beygelzimer, A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.), Advances in Neural Information Processing Systems, volume 34, pp. 20772–20784. Curran Associates, Inc., 2021. URL https://proceedings.neurips. cc/paper_files/paper/2021/file/ adf8d7f8c53c8688e63a02bfb3055497-Paper. pdf.

<!-- Page 13 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

McCallum, S. and Foster, J. Efficient, accurate and stable gradients for neural odes. arXiv preprint arXiv:2410.11648, 2024.

Mrongowius, J. and Rößler, A. On the approximation and simulation of iterated stochastic integrals and the corresponding lévy areas in terms of a multidimensional brownian motion. Stochastic Analysis and Applications, 40(3):397–425, 2022.

Mutze, U. An asynchronous leapfrog method ii. arXiv preprint arXiv:1311.6602, 2013.

Naeem, M. F., Oh, S. J., Uh, Y., Choi, Y., and Yoo, J. Re- liable fidelity and diversity metrics for generative models. In International conference on machine learning, pp. 7176–7185. PMLR, 2020.

Nie, S., Guo, H. A., Lu, C., Zhou, Y., Zheng, C., and Li,

C. The blessing of randomness: SDE beats ODE in general diffusion-based image editing. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum? id=DesYwmUG00.

Øksendal, B. Stochastic Differential Equations: An In- troduction with Applications. Universitext. Springer Berlin Heidelberg, Berlin, Germany, jul 2003. ISBN 9783662036204. doi: 10.1007/978-3-642-14394-6.

Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec,

M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El- Nouby, A., et al. Dinov2: Learning robust visual features without supervision. arXiv preprint arXiv:2304.07193, 2023.

Pan, J., Yan, H., Liew, J. H., Feng, J., and Tan, V. Y. Towards accurate guided diffusion sampling through symplectic adjoint method. arXiv preprint arXiv:2312.12030, 2023.

Peebles, W. and Xie, S. Scalable diffusion models with transformers. In Proceedings of the IEEE/CVF international conference on computer vision, pp. 4195–4205, 2023.

Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh,

G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., and Sutskever, I. Learning transferable visual models from natural language supervision. In Meila, M. and Zhang, T. (eds.), Proceedings of the 38th International Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, pp. 8748–8763. PMLR, 18–24 Jul 2021. URL https://proceedings.mlr.press/ v139/radford21a.html.

Redmann, M. and Riedel, S. Runge-kutta methods for rough differential equations. arXiv preprint arXiv:2003.12626, 2020.

Rehman, D., Akhound-Sadegh, T., Gazizov, A., Bengio, Y., and Tong, A. FALCON: Few-step accurate likelihoods for continuous flows. In The Fourteenth International Conference on Learning Representations, 2026a. URL https: //openreview.net/forum?id=FbssShlI4N.

Rehman, D., Davis, O., Lu, J., Tang, J., Bronstein, M.,

Bengio, Y., Tong, A., and Bose, A. J. Efficient regressionbased training of normalizing flows for boltzmann generators. In The Fourteenth International Conference on Learning Representations, 2026b. URL https: //openreview.net/forum?id=ctdnzPxDI3.

Revuz, D. and Yor, M. Continuous martingales and Brow- nian motion, volume 293. Springer Science & Business Media, 2013.

Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and

Ommer, B. High-resolution image synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 10684–10695, 2022.

Rößler, A. Runge–kutta methods for the strong approxi- mation of solutions of stochastic differential equations. SIAM Journal on Numerical Analysis, 48(3):922–952, 2010.

Rößler, A. A class of stochastic runge-kutta methods for stochastic differential equations converging with order 1 in Lp-norm. arXiv preprint arXiv:2506.22657, 2025.

Rüemelin, W. Numerical treatment of stochastic differential equations. SIAM Journal on Numerical Analysis, 19(3): 604–613, 1982.

Ruth, R. D. A canonical integration technique. IEEE Trans.

Nucl. Sci., 30(CERN-LEP-TH-83-14):2669–2671, 1983.

Sajjadi, M. S., Bachem, O., Lucic, M., Bousquet, O., and

Gelly, S. Assessing generative models via precision and recall. Advances in neural information processing systems, 31, 2018.

Salmon, J. K., Moraes, M. A., Dror, R. O., and Shaw, D. E.

Parallel random numbers: as easy as 1, 2, 3. In Proceedings of 2011 international conference for high performance computing, networking, storage and analysis, pp. 1–12, 2011.

Shampine, L. F. Some practical Runge-Kutta formulas.

Mathematics of Computation, 46(173):135–150, 1986. doi: https://doi.org/10.2307/2008219.

Shampine, L. F. Stability of the leapfrog/midpoint method.

Applied Mathematics and Computation, 208(1):293–298,

2009.

<!-- Page 14 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Shmelev, D. and Salvi, C. Explicit and effectively symmetric schemes for neural sdes. arXiv preprint arXiv:2509.20599, 2025.

Shmelev, D., Ebrahimi-Fard, K., Tapia, N., and Salvi, C.

Explicit and effectively symmetric runge-kutta methods. arXiv preprint arXiv:2507.21006, 2025.

Skreta, M., Akhound-Sadegh, T., Ohanesian, V., Bonde- san, R., Aspuru-Guzik, A., Doucet, A., Brekelmans, R., Tong, A., and Neklyudov, K. Feynman-kac correctors in diffusion: Annealing, guidance, and product of experts. In Forty-second International Conference on Machine Learning, 2025a. URL https://openreview. net/forum?id=Vhc0KrcqWu.

Skreta, M., Atanackovic, L., Bose, J., Tong, A., and Nek- lyudov, K. The superposition of diffusion models using the itô density estimator. In The Thirteenth International Conference on Learning Representations, 2025b. URL https://openreview.net/forum? id=2o58Mbqkd2.

Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N., and

Ganguli, S. Deep unsupervised learning using nonequilibrium thermodynamics. In Proceedings of the 32nd International Conference on International Conference on Machine Learning - Volume 37, ICML’15, pp. 2256–2265. JMLR.org, 2015.

Song, J., Meng, C., and Ermon, S. Denoising diffusion implicit models. In International Conference on Learning Representations, 2021a. URL https:// openreview.net/forum?id=St1giarCHLP.

Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A.,

Ermon, S., and Poole, B. Score-based generative modeling through stochastic differential equations. In International Conference on Learning Representations, 2021b. URL https://openreview.net/forum? id=PxTIG12RRHS.

Song, Y., Dhariwal, P., Chen, M., and Sutskever, I. Con- sistency models. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), Proceedings of the 40th International Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research, pp. 32211–32252. PMLR, 23–29 Jul 2023. URL https://proceedings.mlr.press/ v202/song23a.html.

Stein, G., Cresswell, J., Hosseinzadeh, R., Sui, Y., Ross, B.,

Villecroze, V., Liu, Z., Caterini, A. L., Taylor, E., and Loaiza-Ganem, G. Exposing flaws of generative model evaluation metrics and their unfair treatment of diffusion models. In Advances in Neural Information Processing Systems, volume 36, 2023.

Stewart, D. E. Numerical analysis: A graduate course, volume 258. Springer, 2022.

Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., and Wojna,

Z. Rethinking the inception architecture for computer vision. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 2818–2826, 2016.

Tan, C. B., Bose, J., Lin, C., Klein, L., Bronstein, M. M., and Tong, A. Scalable equilibrium sampling with sequential boltzmann generators. In Forty-second International Conference on Machine Learning, 2025a. URL https: //openreview.net/forum?id=U7eMoRDIGi.

Tan, C. B., Hassan, M., Klein, L., Syed, S., Beaini, D.,

Bronstein, M. M., Tong, A., and Neklyudov, K. Amortized sampling with transferable normalizing flows. In The Thirty-ninth Annual Conference on Neural Infor- mation Processing Systems, 2025b. URL https:// openreview.net/forum?id=JenfC3ovzU.

Tong, A., FATRAS, K., Malkin, N., Huguet, G., Zhang, Y.,

Rector-Brooks, J., Wolf, G., and Bengio, Y. Improving and generalizing flow-based generative models with minibatch optimal transport. Transactions on Machine Learning Research, 2024. ISSN 2835-8856. URL https:// openreview.net/forum?id=CD9Snc73AW. Expert Certification.

Vogelaere, R. J. D. Methods of integration which preserve the contact transformation property of the hamilton equations. Report NO. 4, University of Notre Dame, 1956.

Wallace, B., Gokul, A., and Naik, N. Edict: Exact diffusion inversion via coupled transformations. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 22532–22541, 2023.

Wang, F., Yin, H., Dong, Y.-J., Zhu, H., Zhang, C., Zhao,

H., Qian, H., and Li, C. BELM: Bidirectional explicit linear multi-step sampler for exact inversion in diffusion models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. URL https: //openreview.net/forum?id=ccQ4fmwLDb.

Wu, C. H. and la Torre, F. D. A latent space of stochastic dif- fusion models for zero-shot image editing and guidance. In ICCV, 2023.

Xu, J., Liu, X., Wu, Y., Tong, Y., Li, Q., Ding, M., Tang,

J., and Dong, Y. Imagereward: learning and evaluating human preferences for text-to-image generation. In Proceedings of the 37th International Conference on Neural Information Processing Systems, pp. 15903–15935, 2023.

Zhang, G., Lewis, J. P., and Kleijn, W. B. Exact diffusion inversion via bidirectional integration approximation. In

<!-- Page 15 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Computer Vision – ECCV 2024: 18th European Conference, Milan, Italy, September 29–October 4, 2024, Proceedings, Part LVII, pp. 19–36, Berlin, Heidelberg, 2024. Springer-Verlag. ISBN 978-3-031-72997-3. doi: 10.1007/978-3-031-72998-0_2. URL https://doi. org/10.1007/978-3-031-72998-0_2.

Zhang, Q. and Chen, Y. Fast sampling of diffusion mod- els with exponential integrator. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum? id=Loek7hfb46P.

Zhang, Q., Tao, M., and Chen, Y. gDDIM: Generalized denoising diffusion implicit models. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum? id=1hKE9qjvz-.

Zhang, R., Isola, P., Efros, A. A., Shechtman, E., and Wang,

O. The unreasonable effectiveness of deep features as a perceptual metric. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 586–595, 2018.

Zhuang, J., Dvornek, N. C., sekhar tatikonda, and s Dun- can, J. MALI: A memory efficient and reverse accurate integrator for neural ODEs. In International Conference on Learning Representations, 2021. URL https: //openreview.net/forum?id=blfSjHeFM_e.

<!-- Page 16 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Appendices

A Detailed Discussion on Related Work........................ 17

A.1 Reversible Solvers............................ 17

Asynchronous Leapfrog Method • Reversible Heun Method • McCallum-Foster Method • Explicit and Effectively Symmetric Schemes

A.2 A Note on Stability............................ 20

A.3 Exact Inversion of Diffusion Models...................... 21

EDICT Sampler • BDIA Sampler • BELM Sampler • CycleDiffusion • Summary

A.4 SDE Solvers for Diffusion Models....................... 24

Comparison with SEEDS

B Stochastic Runge-Kutta Methods......................... 25

B.1 Foster-Reis-Strange SRK Scheme....................... 26

B.2 Independence of the Brownian and Lévy Increments.................. 27

B.3 ShARK............................... 27

B.4 A Brief Note on the Theory of Rough Paths.................... 27

B.5 Time-Changed Brownian Motion....................... 28

C Derivation of Rex.............................. 30

C.1 Rex (ODE).............................. 31

Proof of Proposition C.1 • Data Prediction • Noise Prediction

C.2 Rex (SDE).............................. 36

Proof of Reparametrized Semi-Linear SDE with Additive Noise • Proof of Reparametrized SDE for Data Prediction Models • Proof of Reparametrized SDE for Noise Prediction Models • Derivation of Rex (SDE)

C.3 Proof of Proposition 3.2.......................... 42

D Convergence Order Proofs........................... 43

D.1 Assumptions............................. 43

D.2 Proof of Theorem 3.3........................... 43

D.3 Proof of Theorem 3.4........................... 44

E Relation to Other Solvers for Diffusion Models..................... 45

E.1 Rex as Reversible ODE Solvers........................ 46

Euler • Second-Order Methods • Third-Order Methods

E.2 Rex as Reversible SDE Solvers........................ 50

Euler-Maruyama

E.3 Rex as Reversible SEEDS-1......................... 52

F Implementation Details............................ 53

F.1 Closed Form Expressions of the Noise Schedule................... 53

Variance Preserving SDEs • OT Flow Matching

F.2 Some Other Inverse Functions........................ 56

F.3 Numerical Simulation of Brownian Motion.................... 57

## Methods

• Implementation

<!-- Page 17 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

G Experimental Details............................. 58

G.1 Unconditional Image Generation....................... 59

Diffusion Model • Metrics • Hyperparameters

G.2 Conditional Image Generation........................ 60

Diffusion Model • Metrics • Hyperparameters

G.3 Image Editing............................. 61

G.4 Interpolation............................. 61

G.5 Boltzmann Sampling........................... 61

Datasets • Training Details • Metrics

G.6 Hardware.............................. 63

G.7 Repositories............................. 63

H Additional Results.............................. 63

H.1 Reconstruction Error........................... 64

H.2 Unconditional Image Generation....................... 65

H.3 Conditional Image Generation........................ 65

H.4 Image Editing............................. 65

H.5 Boltzmann Sampling........................... 66

H.6 Brownian Interval Overhead......................... 66

H.7 Ablation Study............................. 67

H.8 Visualization of Inversion and the Latent Space................... 67

H.9 Interpolation............................. 68

H.10 Uncurated Image Generation Samples...................... 68

A. Detailed Discussion on Related Work

In this section we provide a detailed comparison with relevant related works. We begin by discussing algebraically reversible solvers in Appendix A.1. Then in Appendix A.2 we introduce the stability of an ODE solver, a helpful tool in comparing reversible solvers. Using this tool along with examining the convergence order, we compare a variety of reversible solvers for diffusion models in Appendix A.3. Lastly, in Appendix A.4 we explore related work on constructing SDE solvers for diffusion models.

A.1. Reversible Solvers

The earliest work on reversible solvers can be traced back to the pioneering work on symplectic integrators by Vogelaere (1956); Ruth (1983); Feng (1984). Due to symplectic integrators being developed for solving Hamiltonian systems, they are intrinsically reversible by construction (Greydanus et al., 2019). More recently, Matsubara et al. (2021) explored the use of symplectic solvers for solving the continuous adjoint equations. Likewise, work by Pan et al. (2023) extended this idea, making use of symplectic solvers for solving the continuous adjoint equations for diffusion models. However, in this section we will focus on non-symplectic reversible solvers.

Throughout this section we consider solving the following d-dimensional IVP:

x(0) = x0, dx dt (t) = f(t, x(t)), (17)

over the time interval [0, T] with numerical solution {xn}N n=0.

<!-- Page 18 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

A.1.1. ASYNCHRONOUS LEAPFROG METHOD

To the best of our knowledge the asynchronous leapfrog definition was the first algebraically reversible non-symplectic solver, initially proposed by Mutze (2013) and popularized in a modern deep learning context by Zhuang et al. (2021). The asynchronous leapfrog method is a modification of the leapfrog method which converts it from a multi-step to single-step method. The method keeps track of a second state, {vn} which is supposed to be sufficiently close to the value of the vector field. We define the method below in Definition A.1.

Definition A.1 (Asynchronous leapfrog method). Initialize v0 = f(0, x0). Consider a step size of h and let ˆtn = tn + h/2, then a forward step of the asynchronous leapfrog method is defined as

ˆxn = xn + 1

2vnh, vn+1 = 2f(ˆtn, ˆxn) −vn, xn+1 = xn + f(ˆtn, ˆxn)h,

(18)

and the backward step is given as

ˆxn = xn+1 −1

2vn+1h, xn = xn+1 −f(ˆtn, ˆxn)h, vn = 2f(ˆtn, ˆxn) −vn+1.

(19)

Remark A.2. The method is a second-order solver (Zhuang et al., 2021, Theorem 3.1).

A.1.2. REVERSIBLE HEUN METHOD

Later work by Kidger et al. (2021) proposed the reversible Heun method, a general purpose reversible solver which is symmetric and is an algebraically reversible SDE solver in addition to being a reversible ODE solver. This solver keeps track of an auxiliary state variable ˆxn and an extra copy of previous evaluations of the drift and diffusion coefficients. We present this method below in Definition A.3. Definition A.3 (Reversible Heun method for ODEs). Initialize ˆx0 = x0. Consider a step size of h, then a forward step of the reversible Heun method is defined as

ˆxn+1 = 2xn −ˆxn + f(tn, ˆxn)h, xn+1 = xn + 1

2 (f(tn+1, ˆxn+1) + f(tn, ˆxn)) h. (20)

and the backward step is given as

ˆxn = 2xn+1 −ˆxn+1 −f(tn+1, ˆxn+1)h, xn = xn+1 −1

2 (f(tn+1, ˆxn+1) + f(tn, ˆxn)) h. (21)

Remark A.4. This method is a second-order solver (Kidger, 2022, Theorem 5.18).

Recall that simulating SDEs in reverse-time is much trickier than simulating ODEs in reverse-time. This observation is even more true of algebraically reversible methods for SDEs. To the best of our knowledge, the only general reversible solver for SDEs is the reversible Heun method. The main idea of the SDE formulation of the reversible Heun method is to extend the Euler-Heun method4 like how Heun’s method was extended to the reversible Heun solver for ODEs. We define the method in Kidger et al. (2021, Algorithm 1) below in Definition A.5. Definition A.5 (Reversible Heun method for SDEs). Initialize ˆx0 = x0. Consider a step size of h and let Wh:= Wtn+1 −Wtn, then a forward step of the reversible Heun method is defined as

ˆxn+1 = 2xn −ˆxn + µ(tn, ˆxn)h + σ(tn, ˆxn)Wh, xn+1 = xn + 1

2 (µ(tn+1, ˆxn+1) + µ(tn, ˆxn)) h

+ 1

2 (σ(tn+1, ˆxn+1) + σ(tn, ˆxn)) Wh.

(22)

4This converges with strong order 1 2 in the Stratonovich sense (Rüemelin, 1982).

<!-- Page 19 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers and the backward step is given as

ˆxn = 2xn+1 −ˆxn+1 −µ(tn+1, ˆxn+1)h −σ(tn, ˆxn)Wh, xn = xn+1 −1

2 (µ(tn+1, ˆxn+1) + µ(tn, ˆxn)) h

−1

2 (σ(tn+1, ˆxn+1) + σ(tn, ˆxn)) Wh.

(23)

Remark A.6. This method requires some tractable solution for recalculating the Brownian motion from a splittable PRNG.

A.1.3. MCCALLUM-FOSTER METHOD

Recent work by McCallum & Foster (2024) created a general method for constructing n-th order solvers from pre-existing explicit single-step solvers while also addressing the stability issues that earlier methods suffered from. As McCallum & Foster (2024) simply refer to their method as reversible X where X is the underlying single-step solver, we opt to refer to their method as the McCallum-Foster method. We restate the definition below.

Definition A.7 (McCallum-Foster method). Initialize ˆx0 = x0 and let ζ ∈(0, 1]. Consider a step size of h, then a forward step of the McCallum-Foster method is defined as xn+1 = ζxn + (1 −ζ)ˆxn + Φh(tn, ˆxn), (24a) ˆxn+1 = ˆxn −Φ−h(tn+1, xn+1), (24b)

and the backward step is given as

ˆxn = ˆxn+1 + Φ−h(tn+1, xn+1), (25a)

xn = ζ−1xn+1 + (1 −ζ−1)ˆxn −ζ−1Φh(tn, ˆxn). (25b)

Remark A.8. N.B., the ζ and ζ−1 terms in the forward and backward steps determine the stability of the system.

Interestingly, McCallum & Foster (2024, Theorem 2.1) showed that this reversible method inherits the convergence order of single-step solver Φh, enabling the construction of an arbitrarily high-order reversible solver. We restate this result below in Theorem A.1.

Theorem A.1 (Convergence order of the McCallum-Foster method). Consider the ODE in Equation (17) over [0, T] with fixed time horizon T > 0. Let T = Nh where N > 0 is the number of discretization steps and h > 0 is the step size. Let Φ be a k-th order ODE solver such that it satisfies the Lipschitz condition

∥Φη(·, a) −Φη(·, b)∥≤L|η|∥a −b∥, (26)

for all a, b ∈Rd and η ∈[−hmax, hmax] for some hmax > 0. Consider the reversible solution {xn, ˆxn}ninN admitted by Equation (1). Then there exists constants hmax > 0, C > 0, such that, for h ∈(0, hmax],

∥xn −x(tn)∥≤Chk. (27)

A.1.4. EXPLICIT AND EFFECTIVELY SYMMETRIC SCHEMES

Contemporary work by Shmelev & Salvi (2025) explores an explicit and effectively symmetric (EES) Runge-Kutta schemes (Shmelev et al., 2025) for neural SDEs. The key difference is that these schemes are only approximately invertible rather than exactly invertible. The other large difference is they construct the scheme for rough differential equations (RDEs) driven by a α-Hölder branched rough path, α ∈(0, 1]. More concretely, for some driving signal X: [0, T] →Rd, e.g., a semi-martingale, lifted to a rough path X (see Appendix B.4), we consider the rough differential equation dYt = f(Yt) dXt, (28)

where f is sufficiently smooth and bounded with bounded derivatives. Following Redmann & Riedel (2020), assume that there exists smooth paths {Xh}h>0 for step-sizes h > 0 whose natural lifts to branch rough paths {X h}h>0 converge almost surely to X under the metric of α-Hölder rough paths as h →0. Then we have the solution with drive X h given by dY h t = f(Y h t) dX h t. (29)

<!-- Page 20 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Shmelev & Salvi (2025) then uses the following Runge-Kutta scheme for the RDE given by yh n+1 = yh n + d X m=1 s X i=1 bifm(ki)X(m)

tn,tn+1, (30a)

ki = yh n + d X m=1 s X i=1 aijfm(ki)X(m)

tn,tn+1, (30b)

where Xtn,tn+1 denotes the increment of Xh over [tn, tn+1]. With an appropriate choice of coefficients aij and bi, the Runge-Kutta scheme for the RDE is approximately reversible (Shmelev & Salvi, 2025). Clearly, this scheme is quite different from the SRK schemes we study and construct exactly reversible schemes from (see Appendix B).

A.2. A Note on Stability

Historically, the stability properties of reversible solvers has been one of their weakest attributes (Kidger, 2022), limiting their use in practical applications. We formally introduce the notation of stability following Kidger (2022, Definition C.39), which we rewrite below in Definition A.9. Definition A.9 (Region of stability). Fix some numerical differential equation solver and let {xλ,h n }n∈N be the solution admitted by the numerical scheme solving the linear (or Dahlquist) test equation x(0) = x0, dx dt = λx(t), (31)

where λ ∈C, h > 0 is the step size, and x0 ∈Rd is a non-zero initial condition. The region of stability is defined as

{hλ ∈C: {xλ,h n }n∈N is uniformly bounded over tn}. (32)

I.e., there exists a constant C depending on λ and h but independent of tn such that ∥xλ,h n ∥< C.

With the linear test equation Equation (31), the ODE converges asymptotically when ℜ(λ) ≤0,5 and thus we are interested in numerical schemes which are bounded when the underlying analytical solution converges. Ideally, a numerical scheme would converge for all hλ with ℜ(λ) < 0.6 Thus, the larger the region of stability, the larger the step size we can take, wherein the numerical scheme still converges.

Remark A.10. Regrettably, the reversible Heun, leapfrog, and asynchronous leapfrog methods have poor stability properties. Specifically, the region of stability for all the methods is the complex interval [−i, i], see Kidger (2022, Theorem 5.20) for reversible Heun, Shampine (2009, Section 2) for leapfrog, and Zhuang et al. (2021, Appendix A.4) for asynchronous leapfrog.

In other words, all previous reversible solvers are nowhere linearly stable for any step size h.7 The instability in both asynchronous leapfrog and reversible Heun can be attributed to a step of general form 2A −B, i.e., we can write the source of instability as

2f(ˆtn, ˆxn) −vn, (asynchronous leapfrog)

2xn+1 −ˆxn+1. (reversible Heun)

Thus the instability in these reversible schemes is caused by a decoupling between vn and f(tn, xn) (asynchronous leapfrog); and xn and ˆxn (reversible Heun). The strategy of McCallum & Foster (2024) is to couple xn and ˆxn together with the coupling parameter ζ. Using this strategy, they showed that it was possible to construct a reversible solver with a non-trivial region of convergence. Let Φh(tn, xn) = R(hλ)xn and let R(hλ) denote the transfer function used in analysis of Runge-Kutta methods with step size h (see Stewart, 2022). We restate McCallum & Foster (2024, Theorem 2.3) below.

5The ODE converges to 0 when ℜ(λ) < 0. 6A region of stability which satisfies is known as a region of absolute stability. 7Linearly stability refers to stability for linear test equations with ℜ(λ) < 0.

<!-- Page 21 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Theorem A.2 (Region of stability for the McCallum-Foster method). Let Φ be given by an explicit Runge-Kutta solver. Then the reversible numerical solution {xn, ˆxn}n∈N given by Equation (1) is linearly stable iff

|Γ| < 1 + ζ, (33)

where

Γ = 1 + ζ −(1 −ζ)R(−hλ) −R(−hλ)R(hλ). (34)

Remark A.11. The McCallum-Foster method when constructed from explicit Runge-Kutta methods have a non-trivial region of stability. Note, however, that this region of stability is smaller than the original region of stability from the original Runge-Kutta method.

A.3. Exact Inversion of Diffusion Models

Independent of the work on reversible solvers for neural ODEs, several researchers have developed reversible methods for solving the probability flow ODE—often in the literature on diffusion models this is called the exact inversion of diffusion models. The discussion here covers prior reversible solvers; the (non-reversible) explicit (S)RK solvers that Princeps generalizes—DDIM, the DPM-Solver family, SEEDS-1, and gDDIM—are catalogued separately in Appendix E.

A.3.1. EDICT SAMPLER

The first work to explore this topic of exact inversion with diffusion models was that of Wallace et al. (2023), who inspired by coupling layers in normalizing flows (Dinh et al., 2015) proposed a reversible solver which they refer to as exact diffusion inversion via coupled transformations (EDICT). Like all reversible solvers, this method keeps track of an extra state, denoted by {yn}n∈N, with y0 = x0. Letting an = αn+1 αn and bn = σn+1 −αn+1 αn σn, this numerical scheme can be described as xinter n = anxn + bnxθ

T |tn(yn), yinter n = anyn + bnxθ

T |tn(xinter n), xn+1 = ξxinter n + (1 −ξ)yinter n yn+1 = ξxinter n + (1 −ξ)xn+1,

(35)

where ξ ∈(0, 1) is a mixing parameter.8 This method can be inverted to obtain a closed form expression for backward step:

yinter n = yn+1 −(1 −ξ)xn+1 ξ, xinter n = yn+1 −(1 −ξ)yinter n ξ, yn = yinter n −bnxθ

T |tn(xinter n)

an

, xn = xinter n −bnxθ

T |tn(yn)

an

.

(36)

Notably, the EDICT solver was developed in the context of discrete-time diffusion models and the connection to reversible solvers for ODEs was not considered in the original work. N.B., to the best of our knowledge, our work is the first to draw the connection between the work on reversible ODE solvers and exact inversion with diffusion models. Unfortunately, this method suffers from poor convergence issues (see Remark A.12) and generally has poor performance when used to perform sampling with diffusion models, thereby limiting its utility in practice (Zhang et al., 2024; Wang et al., 2024). Remark A.12. Later work by Wang et al. (2024, Proposition 6) showed that EDICT is actually a zero-order method, i.e., the local truncation error is O(h), making it generally unsuitable in practice.

8In practice, when used for image editing, the authors found that the parameter ξ controlled how closely the EDICT sampler aligned with the original sample, with lower values corresponding to higher agreement with the original sample.

<!-- Page 22 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

A.3.2. BDIA SAMPLER

Later work by Zhang et al. (2024) proposed a reversible solver for the probability flow ODE which they call bidirectional integration approximation (BDIA). The core idea is to use both single-step methods Φtn,tn−1 and Φtn,tn+1 to induce reversibility.9 Then using these two approximations—both of which are computed from a discretization centered around xn—the process is updated via a multistep process with a forward step of10 xn+1 = xn−1 −Φtn,tn−1(xn) + Φtn,tn+1(xn). (37)

The backwards step can easily be expressed as xn−1 = xn+1 + Φtn,tn−1(xn) + Φtn,tn+1(xn). (38)

In practice, BDIA uses the DDIM solver (i.e., Euler) for Φ, but in theory one could use a higher-order method—this was not explored in Zhang et al. (2024).

Proposition A.3 (BDIA is the leapfrog/midpoint method). The BDIA method described in Equation (37) is the leapfrog/midpoint method when Φh(t, x) = huθ t (x), i.e., the Euler step.

Proof. This can be shown rather straightforwardly by substitution, i.e., xn+1 = xn−1 + 2huθ tn(xn). (39)

Corollary A.3.1 (BDIA is a first-order method). BDIA is a first-order method, i.e., the local truncation error is O(h2).

Remark A.13. This result was also observed in Wang et al. (2024, Proposition 6).

Corollary A.3.2 (BDIA is nowhere linearly stable). BDIA is nowhere linearly stable, i.e., the region of stability is the complex interval [−i, i].

Proof. This follows straightforwardly from Proposition A.3 and Shampine (2009, Section 2).

Zhang et al. (2024) introduce a hyperparameter γ ∈[0, 1] which is used below

ˆΦtn,tn−1(xn) = (1 −γ)(xn−1 −xn) + γΦtn,tn−1(xn), (40)

to modify the BDIA update rule in Equation (37). Thus, γ can be viewed as a parameter which interpolates between the midpoint and Euler schemes. For image editing applications, the authors found this parameter to control how closely the BDIA sampler aligned with the original image, with lower values corresponding to higher agreement with the original image (making it similar to the ξ parameter from BDIA).

A.3.3. BELM SAMPLER

Recently, Wang et al. (2024) proposed a linear multi-step reversible solver for the probability flow ODE called the bidirectional explicit linear multi-step (BELM) sampler. First, they reparameterize the probability flow ODE as dx(t) = xθ

T |σt(x(t)) dσt, (41)

where x(t):= x(t)/αt, σ(t):= σt/αt, and xθ

T |σt(x(t)) = xθ

T |t(x(t)).11 The BELM sampler makes use of the variablestepsize-variable-formula (VSVF) linear multi-step methods (Crouzeix & Lisbona, 1984) to construct the numerical solver.

9N.B., in the original paper, Zhang et al. (2024) use quite different notation for explaining their idea; however, we find our presentation to be simpler for the reader as it more easily enables comparison to other methods.

10In some sense, this is reminiscent of the idea from the more general McCallum-Foster method; however, this approach results in a multi-step method unlike the single-step method of McCallum & Foster (2024).

11N.B., this is a popular parameterization of diffusion models and affine conditional flows. This can be done mutatis mutandis for target prediction models retrieving (Blasingame & Liu, 2025, Proposition D.2).

<!-- Page 23 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

The k-step VSVF linear multi-step method for solving the reparameterized probability flow ODE in Equation (41) is given by xn+1 = k X m=1 an,mxn+1−m (42)

+ k−1 X m=1 bn,mhn+1−mxθ

T |σn+1−m(xn+1−m). (43)

where an,m̸ = 0,12 and bn,m are coefficients chosen using dynamic multi-step formulæ to find the coefficients (Crouzeix & Lisbona, 1984); and hn are step sizes chosen beforehand. This scheme can be reversed via the backward step xn+1−k = 1 an,k xn+1 − k−1 X m=1 an,m an,k xn+1−m (44)

− k−1 X m=1 bn,m an,k hn+1−mxθ

T |σn+1−m(xn+1−m). (45)

Remark A.14. The BELM samplers require k −1 extra states to be stored in memory in order to be reversible. In contrast, McCallum & Foster (2024) only requires storing one extra states, irregardless of the desired convergence order. Additionally, poor stability is a concern with such linear multi-step methods (see Kidger, 2022, Remark 5.24).

Remark A.15. Interestingly, the earlier EDICT and BDIA methods can be viewed as instances of the BELM method (Wang et al., 2024, Appendicies A.7 and A.8).

By solving the multi-step formulæ to minimize the local truncation error, Wang et al. (2024) propose an instance of the BELM solver which they refer to as O-BELM defined as13 xn+1 = h2 n h2 n−1 xn−1 + h2 n−1 + h2 n h2 n−1 xn −hn(hn + hn+1)

hn+1 x0|σn(xn). (46)

Notably, the O-BELM sampler can also be viewed as instance of the leapfrog/midpoint method.

Theorem A.4 (O-BELM is the leapfrog/midpoint method). Fix a step size hn = h for all n, then O-BELM is the leapfrog/midpoint method.

Proof. This follows from substitution of hn = h.

Corollary A.4.1 (O-BELM is nowhere linearly stable). Fix a step size hn = h, then O-BELM is nowhere linearly stable, i.e., the region of stability is the complex interval [−i, i].

A.3.4. CYCLEDIFFUSION

To our knowledge, the only other work to propose exact inversion with the SDE formulation of the diffusion models is the work of Wu & la Torre (2023). However, there are several noticeable distinctions, the largest being that they store the entire solution trajectory in memory. Given a particular realization of the Wiener process that admits xt ∼N(αtx0 | σ2 t I), then given xs and noise ϵs ∼N(0, I) we can calculate xt = αt αs xs + 2σt(eh −1)ˆxT |s(xs) + σt p e2h −1ϵs. (47)

Wu & la Torre (2023) propose to invert this by first calculating, for two samples xt and xs, the noise ϵs. This can be calculated by rearranging the previous equation to find ϵs = xt −αt αs xs + 2σt(eh −1)ϵθ(xs, z, s)

σt

√ e2h −1

(48)

12This is to ensure that the method is reversible. 13N.B., the original equation in Wang et al. (2024, Equation (18)) had a sign difference for the coefficient of bi,1; however, this is due to differences in convention in handling integration in reverse-time.

<!-- Page 24 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 2.** Comparison of different (non-symplectic) reversible solvers. We note that some of the solvers were developed particularly for the

probability flow ODE (an affine conditional flow) whilst others work for general ODEs/SDEs. In the first column we denote the number of extra states the numerical scheme needs to keep in memory to ensure algebraic reversibility. For BELM k denotes the number of steps and for McCallum-Foster k denotes the convergence order of the underlying single-step solver. For the column labelled region of linear stability, we mean there exists some subset of C which is the region of stability and the set is not a null set. The proof of convergence for BELM is only provided for the special case (called O-BELM in Wang et al. (2024)) with k = 2.

Exponential Number of Local Region of Proof of Solver SDE integrators extra states truncation error linear stability convergence

Asynchronous leapfrog ✗ ✗ 1 O(h3) ✗ ✓ Reversible Heun ✓ ✗ 1 O(h3) ✗ ✓ McCallum-Foster ✗ ✗ 1 O(hk+1) ✓ ✓ EDICT ✗ ✗ 1 O(h) ✗ ✗ BDIA ✗ ✗ 1 O(h2) ✗ ✗ BELM ✗ ✓ k −1 O(hk+1) ✗ ∼ Rex ✓ ✓ 1 O(hk+1) ✓ ✓

With this the sequence {ϵti}N i=1 of added noises can be calculated which can be used to reconstruct the original input from the initial realization of the Wiener process. However, unlike our approach, this process requires storing the entire realization in memory.

A.3.5. SUMMARY

We present a summary of related works on either exact inversion or reversible solvers below in Table 2. N.B., we omit CycleDiffusion because it is more orthogonal to the general concept of a reversible solver and is only reversible in the trivial sense.

A.4. SDE Solvers for Diffusion Models

Next we discuss related works on SDE solvers for the reverse-time diffusion SDE in Equation (5). Now there are numerous stochastic Runge-Kutta (SRK) methods in the literature all tailor to specific types of SDEs, which we can distinguish by their strong order of convergence (see Definition D.1) and strong order conditions. For example, the classic Euler-Maruyama scheme (Kloeden & Platen, 1992) has strong order of convergence of 0.5 and was straightforwardlly applied to the reversetime diffusion SDE in Jolicoeur-Martineau et al. (2021) as a baseline. Song et al. (2021b) proposed an ancestral sampling scheme for a discretization of the forward-time diffusion SDE in Equation (3) with additional Langevin dynamics; likewise, the DDIM solver from Song et al. (2021a) can be viewed a sort of Euler-Maruyama scheme. Other classic SDE schemes like SRA1/SRA2/SRA3 schemes (Rößler, 2010) all have strong order of convergence 1.5 for additive noise SDEs and were tested for diffusion models in Jolicoeur-Martineau et al. (2021).

More recently, researchers have explored exponential solvers for SDEs, e.g., the exponential Euler-Maruyama method (Komori et al., 2017) and the stochastic Runge-Kutta Lawson (SRKL) schemes (Debrabant et al., 2021). From an initial inspection, the SRKL schemes of Debrabant et al. (2021, Algorithm 1) is somewhat similar to our method for constructing Ψ; however, upon closer inspection, there are some key fundamental differences.14 The largest of these is how the underlying SRK schemes are represented. In particular, the SRKL schemes choose to follow the conventions of Burrage & Burrage (2000) (for Stratonovich SDEs) in constructing the underlying SRK schemes; whereas we follow the SRK schemes outlined by Foster et al. (2024) (see Appendix B). These differences stem from how one chooses to handle the iterated stochastic integrals from the Stratonovich-Taylor (or Itô-Taylor) expansions.

A.4.1. COMPARISON WITH SEEDS

Mostly directly relevant to our work on constructing a stochastic Ψ is the SEEDS family of solvers proposed by Gonzalez et al. (2024). Similar to us, their approach also uses exponential methods to simplify the expression of diffusion models Gonzalez et al. (2024, Appendix B.1). There are two key distinctions, namely, 1) that they use the stochastic exponential

14N.B., in general Debrabant et al. (2021) consider full stochastic Lawson schemes where the integrating factor is a stochastic process given by the matrix exponential applied to linear terms in the drift and diffusion coefficients; conversely, the drift stochastic Lawson schemes are more similar to what we study.

<!-- Page 25 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers time differencing (SETD) method (Adamu, 2011), whereas we construct stochastic Lawson schemes;15 and 2) that they use a different technique for modelling the iterated stochastic integrals for high-order solvers. In particular, SEEDS introduces a decomposition for the iterated stochastic integrals produced by the Itô-Taylor expansions of Equation (5) such that the decomposition preserves the Markov property, i.e., the random variables used to construct model the Brownian increments from iterated integrals are independent on non-overlapping intervals and dependent on overlapping intervals (see Gonzalez et al., 2024, Proposition 4.3). By making use of the SRK schemes of Foster et al. (2024) developed from using the space-time Lévy area to construct high-order splitting methods, we have an alternative method for ensuring this property. This results in our solver based on ShARK (see Appendix B.3 and Theorem 3.4) having a strong order of convergence of 1.5; whereas, SEEDS-3 only achieves a weak order of convergence of 1.

This brings us to another large difference, the SEEDS solvers focus on the weak approximation to Equation (5); whereas we are concerned with the strong approximation to Equation (5). The difference between these two is that the weak convergence is considered with the precisions of the moments; whereas strong convergence is concerned with the precision of the path. Moreover, by definition a strong order of convergence implies a weak order of convergence, the converse is not true. In particular, for our application of developing reversible schemes, this strong order of convergence is particularly important as we care about the path. Thus, the technique SEEDS uses to replace iterated Itô integrals with other random variables with equivalent moment conditions is wholly unsuitable for our purposes as we desire a strong approximation.

B. Stochastic Runge-Kutta Methods

Recall that the general Butcher tableau for a s-stage explicit RK scheme (Stewart, 2022, Section 6.1.4) for a generic ODE is written as c1 c2 a21 c3 a31 a32............

cs as1 as2 · · · as(s−1) b1 b2 · · · bs−1 bs

= c a b. (49)

E.g., the famous 4-th order Runge-Kutta (RK4) method is given by

0

1 2 1 2

1 2 0 1 2 1 0 0 1

1 6 1 3 1 3 1 6

. (50)

However, for SDEs this is much trickier due to the presence of iterated stochastic integrals in the Itô-Taylor or Stratonovich- Taylor expansions (Kloeden & Platen, 1992). Consider a d-dimensional Stratonovich SDE driven by dw-dimensional Brownian motion {Wt}t∈[0,T ] defined as dXt = µθ(t, Xt) dt + σθ(t, Xt) ◦dWt, (51)

where µθ ∈C2(R × Rd; Rd) and σθ ∈C3(R × Rd; Rd×dw) satisfy the usual regularity conditions for Stratonovich SDEs (Øksendal, 2003, Theorem 5.2.1) and where ◦dWt denotes integration in the Stratonovich sense.

Rößler (2025) write one such class of an s-stage explicit SRK methods (cf. Burrage & Burrage, 2000; Rößler, 2010) for

15N.B., for certain scenarios these two different viewpoints converge, particularly, in the deterministic case. See our discussion on the family of DPM-Solvers which also use (S)ETD in Appendix E.

<!-- Page 26 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Equation (51) as

Z(0)

i = Xn + h i−1 X j=1 a(0)

ij µθ(tn + c(0)

j, Z(0)

j),

Z(k)

i = Xn + h i−1 X j=1 a(1)

ij µθ(tn + c(0)

j, Z(0)

j) + i−1 X j=1 dw X l=1 a(2)

ij I(l,k),nσθ(tn + c(1)

j, Z(l)

i),

Xn+1 = Xn + h s X i=1 b(0)

i µθ(tn + c(0)

i, Z(0)

j) + s X i=1 dw X k=1 b(1)

i I(k),n + b(2)

i σθ(tn + c(1)

j, Z(k)

i),

(52)

for k = 1,..., dw and where

I(k),n =

Z tn+1 tn

◦dW k u = W k tn+1 −W k tn, (53)

I(l,k),n =

Z tn+1 tn

Z u tn

◦dW l v ◦dW k u, (54)

let ˆI denote the iterated integrals for the Itô case mutatis mutandis. This scheme is described the by the extended Butcher tableau (Rößler, 2025)

c(0) a(0)

c(1) a(1) a(2)

b(0) b(1) b(2)

. (55)

These iterated integrals I(l,k),n are very tricky to work with and can raise up many practical concerns. As alluded to earlier (see Appendix A.4.1), it is common to use a weak approximation of such integrals via a random variables with corresponding moments. This results in two drawbacks: 1) the resulting SDE scheme only converges in the weak sense and 2) the solution yielded by the scheme is not a Markov chain in general. SEEDS overcomes the second issue by using a special decomposition to preserve the Markov property, see the ablations in Gonzalez et al. (2024) for more details on this topic in practice.

B.1. Foster-Reis-Strange SRK Scheme

Conversely, Foster et al. (2024) propose another SRK scheme based on higher-order splitting methods for Stratonovich SDEs. For the Stratonovich SDE in Equation (51) Foster et al. (2024) write an s-stage SRK as µi θ = µθ(tn + cih, Zi), σi θ = σθ(tn + cih, Zi),

Zi = Xn + h



 i−1 X j=1 aijµj θ



+ Wn



 i−1 X j=1 aW ij σj θ



+ Hn



 i−1 X j=1 aH ijσj θ



,

Xn+1 = Xn + h s X i=1 biµi θ

!

+ Wn s X i=1 bW i σi θ

!

+ Hn s X i=1 bH i σi θ

!

,

(56)

where h = tn+1 −tn is the step size and Wn:= Wtn,tn+1 and Hn:= Htn,tn+1 are the Brownian and space-time Lévy increments (see Definition 3.2) respectively; and where aij, aW ij, aH ij ∈Rs×s, bi, bW i, bH i ∈Rs, and ci ∈Rs for the coefficients for an extended Butcher tableau (Foster et al., 2024) which is given as c a aW aH b bW bH. (57)

E.g., we can write the famous Euler-Maruyama scheme as

0 0 0 0

1 1 0. (58)

<!-- Page 27 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

B.2. Independence of the Brownian and Lévy Increments

Remarkably, Foster et al. (2020, Theorem 2.2) present a polynomial Karhunen-Loève theorem for the Brownian bridge (see Definition F.1)—picture a stochastic analogue to the Fourier series of a function on a bounded interval—which leads to a most useful remark (Foster et al., 2020, Remark 3.6) which we restate below.

Remark B.1. We have that Hs,t ∼N(0, 1

12h) is independent of Ws,t when d = 1, likewise, since the coordinate processes of a Brownian motion are independent, one can write Ws,t ∼N(0, hI) and Hs,t ∼N(0, 1

12hI) are independent.

Thus, we have found another remedy to the problem of independent increments, whilst still being able to obtain a strong approximation of the SDE.

B.3. ShARK

Recently, Foster et al. (2024) developed shifted additive-noise Runge-Kutta (ShARK) for additive noise SDEs which is based on Foster et al. (2024, Equation (6.1)). This scheme converges strongly with order 1.5 for additive-noise SDEs and makes two evaluations of the drift and diffusion per step.

ShARK is described via the following extended Butcher tableau

0 0 1

5 6 5 6 5 6 1

0.4 0.6 1 0

−0.6 0.6

. (59)

The second row for the b variable describes the coefficients used for adaptive-step size solvers to approximate the error at each step. The Butcher tableau for this scheme can be found here: https://github.com/patrick-kidger/ diffrax/blob/main/diffrax/_solver/shark.py.

B.4. A Brief Note on the Theory of Rough Paths

To perform reversibility it is useful to consider the pathwise interpretation of SDEs (Lyons, 1998), as such we introduce a few notations from rough path theory. Let {Wt} be a dw-dimensional Brownian motion and let W be enhanced by

Ws,t =

Z t s

Ws,r ⊗◦dWr, (60)

where ⊗is the tensor product. Then, the pair W:= (W, W) is the Stratonovich enhanced Brownian rough path.16 Thus consider the dx-dimensional rough differential equation RDE of the form:

dXt = µ(t, Xt) dt + σ(t, Xt) dWt, X0 = x0. (61)

where µ: [0, T] × Rdx →Rdx is Lipschitz continuous in its second argument and σ ∈C1,3 b ([0, T] × Rdx; L(Rdw, Rdx)) (Friz & Hairer, 2020, Theorem 9.1).17 Fix an ω ∈Ω, then almost surely W(ω) admits a unique solution to the RDE (Xt(ω), σ(t, Xt(ω))) and Xt = Xt(ω) is a strong solution to the Stratonovich SDE18 started at X0 = x0. To elucidate, consider the commutative diagram below

W

Ψ 7−→(W, W) S 7−→X, (62)

where Ψ is a map which merely lifts Brownian motion into a rough path (could be Itô or Stratonovich), the second map, S, is known as the Itô-Lyons map (Lyons, 1998); this map is purely deterministic and is also a continuous map w.r.t. to initial

16See, Friz & Hairer (2020, Chapter 3) for more details. 17Here L(V, W) denotes the set of continuous maps from V to W, a Banach space. 18If Xt and ∂xXt are adapted and ⟨X, W ⟩t exists, then almost surely

Z T

0 XdWt =

Z T

0 X ◦dWt.

<!-- Page 28 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers condition and driving signal. Thus, for a fixed realization of the Brownian motion we have a pathwise interpretation of the Stratonovich SDE.

B.5. Time-Changed Brownian Motion

In this subsection we develop the time-changed Brownian motion machinery used throughout the SDE derivations in Appendix C.2. We review some necessary preliminary results about continuous local martingales and Brownian motion, and show that we can simplify the stochastic integrals in Equation (7) and the corresponding reparameterization with data/noise prediction models.

Dambis-Dubins-Schwarz Representation Theorem. We restate the Dambis-Dubins-Schwarz representation theorem (Dubins & Schwarz, 1965) which shows that continuous local martingales can be represented as time-changed Brownian motions.

Theorem B.1 (Dambis-Dubins-Schwarz representation theorem). Let M be a continuous local martingale adapted to a filtration {Ft}t≥0 beginning at 0 (i.e., M0 = 0) such that ⟨M⟩∞= ∞almost surely. Define the random variables {τt}t≥0 by τt = inf {s ≥0: ⟨M⟩s > t} = sup {s ≥0: ⟨M⟩s = t}. (63)

Then for any given t the random variable τt is an almost surely finite stopping time, and the processa Bt = Mτt is a Brownian motion w.r.t. the filtration {Gt}t≥0 = {Fτt}t≥0. Moreover,

Mt = B⟨M⟩t. (64)

aDefined up to a null set.

A Multi-Dimensional Version of the Dambis-Dubins-Schwarz Representation Theorem. In our work we are interested in a d-dimensional local martingale M:= (M 1,... M d). As such we discuss a multi-dimensional extension of Theorem B.1 which requires that the d-dimensional continuous local martingale if the quadratic (covariation) matrix ⟨M⟩ij t =

M i, M j t is proportional to the identity matrix. We adapt the following theorem from Lowther (2010, Theorem 2) and Bourgade (2010, Theorem 4.13) (cf. Revuz & Yor, 2013).

Theorem B.2 (Multi-dimensional Dambis-Dubins-Schwarz representation theorem). Let M = (M 1,..., M d) be a collection of continuous local martingales with M0 = 0 such that for any 1 ≤1 ≤d, ⟨M⟩ii

∞= ∞almost surely. Furthermore, suppose that ⟨M i, M j⟩t = δijAt, where δ denotes the Kronecker delta, for some process A and all 1 ≤i, j ≤d and t ≥0. Then there is a d-dimensional Brownian motion B w.r.t. a filtration {Gt}t≥0 such that for each t ≥0, ω 7→At(ω) is a G-stopping time and

Mt = BAt. (65)

Enlargement of the Probability Space. Recall that in Theorems B.1 and B.2 we stated that quadratic variation of the continuous local martingale needed to tend towards infinity as t →∞. So when does ⟨M⟩∞have a nonzero probability of being finite? It can be shown that Theorems B.1 and B.2 holds under an enlargement of the probability space (not the filtration). Consider both our original probability space (Ω, F, P) and another probability space (Ω′, F′, P ′) along with a measurable surjection f: Ω′ →Ωpreserving probabilities such that P(A) = P ′(f −1(A)) for all A ∈F, i.e., f∗P ′ is a pushforward measure. Thus any process on the original probability space can be lifted to (Ω′, F′, P ′) and likewise the filtration is also lifted to F′ t = {f −1(A): A ∈Ft}. Therefore, it is possible to enlarge the probability space so that Brownian motion is defined. E.g., if (Ω′′, F′′, P ′′) is probability space on which there is a Brownian motion defined, we can take Ω′ = Ω× Ω′′, F′ = F ⊗F′′, and P ′ = P ⊗P ′′ for the enlargement, and f:′ Ω→Ωis just the projection onto Ω.

Data Prediction. We now present a lemma for rewriting the stochastic differential in Equation (139) using the Dambis- Dubins-Schwarz representation theorem. Recall that in Equation (139) we denote the reverse-time d-dimensional Brownian motion as W t, i.e., by Lévy’s characterization we have W T = 0 and

W t −W s ∼−N(0, (t −s)I) = N(0, (t −s)I), (66)

for 0 ≤t < s ≤T. With this in mind we present Lemma B.3 below.

<!-- Page 29 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Lemma B.3. The stochastic differential q

−dϱt dt dW t can be rewritten as a time-changed Brownian motion of the form r

−dϱt dt dW t = dWϱ, (67)

where ϱt = γ2 t.

Proof. To simplify the stochastic integral term, we first define a continuous local martingale Mt via the stochastic integral

Mt:=

Z t

T r

−dϱ dt dW t. (68)

We choose time T as our starting point for the martingale rather than 0 and then integrate in reverse-time. However, due to the negative sign within the square root term, it is more convenient to work with Wt, i.e., the standard d-dimensional Brownian motion defined in forward time. Recall that the standard d-dimensional Brownian motion in reverse-time with starting point T is defined as

W t = WT −Wt (69)

which is distributed like Wt in time T −t. Define the function f(t, Wt) = W t. Then by Itô’s lemma we have df(t, Wt) = ∂tf(t, Wt) dt + d X i=1

∂xif(t, Wt) dW i t + 1

2 d X i,j=1

∂xi,xjf(t, Wt) d

W i, W j t, (70)

which simplifies to df(t, Wt) = dW t = −dWt. (71)

Thus we can rewrite Equation (68) as

Mt = −

Z t

T r

−dϱ dt dWt. (72)

Next we establish a few properties of this martingale. First, MT = 0 by construction. Second, since the integral consists of scalar noise, we have that ⟨M i, M j⟩t = 0 for all i̸ = j. Thus, the quadratic variation of ⟨Mt⟩ii for each i is found to be

⟨M⟩ii t = At = −

Z t

T r

−dϱτ dτ

2 dτ, (73)

=

Z t

T dϱτ dτ dτ, (74)

= ϱt −ϱT = α2 t σ2 t

−α2

T σ2

T

. (75)

Now we have a deterministic mapping from the original time to our new time via At. Now in general for any valid choice of (αt, σt) we do not necessarily have that ⟨M⟩ii

∞= ∞almost surely and as such we may need to enlarge the underlying probability space. Our constructed martingale can be expressed as time-changed Brownian motion, see Theorem B.2, such that Mt = WAt were Wϱ is the standard d-dimensional Brownian motion with time variable ϱ.

Now we can rewrite Equation (72) in differential form as dMt = dWAt. (76)

Because Brownian motion is time-shift invariant, we can then write dMt = dWϱt. (77)

Remark B.2. Lemma B.3 can similarly be found via Øksendal (2003, Theorem 8.5.7) and Kobayashi (2011, Lemma 2.3); however, due to the oddness of the reverse-time integration, we found it easier to tackle the problem via the Dambis-Dubins- Schwarz theorem.

Remark B.3. Under the common scenario where σ0 = 0, then we have that ⟨M⟩ii

∞= ∞almost surely.

<!-- Page 30 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Noise Prediction. Next we discuss the stochastic integral used in the noise prediction formulation.

Lemma B.4. Let αT > 0. Then the stochastic differential q d dt (χ2 t) dW t can be rewritten as a time-changed Brownian motion of the form r d dt (χ2 t) dW t = dW χ2, (78)

where χt = σt αt.

Proof. To simplify the stochastic integral term, we first define a continuous local martingale Mt via the stochastic integral

Mt:=

Z t

T r d dt (χ2 t) dW t. (79)

We choose time T as our starting point for the martingale rather than 0 and then integrate in reverse-time, hence the negative sign. Next we establish a few properties of this martingale. First, MT = 0 by construction. Second, since the integral consists of scalar noise, we have that ⟨M i, M j⟩t = 0 for all i̸ = j. Thus, the quadratic variation of ⟨Mt⟩ii for each i is found to be

⟨M⟩ii t = At =

Z t

T r d dτ (χ2τ)

2 dτ, (80)

=

Z t

T d dτ χ2 t dτ, (81)

= χ2 t −χ2

T = σ2 t α2 t

−σ2

T α2

T

. (82)

Now we have a deterministic mapping from the original time to our new time via At. Now in general for any valid choice of (αt, σt) we do not necessarily have that ⟨M⟩ii

∞= ∞almost surely and as such we may need to enlarge the underlying probability space. Our constructed martingale can be expressed as time-changed Brownian motion, see Theorem B.2, such that Mt = W At were W χ2 is the standard d-dimensional Brownian motion with time variable χ2 in reverse-time.

Now we can rewrite Equation (68) in differential form as dMt = dW At. (83)

Because Brownian motion is time-shift invariant, we can then write dMt = dW χ2 t. (84)

Remark B.4. The constraint of αT > 0 is important to ensure that χT is finite which is necessary due to

W χ2 t = Wχ2

T −Wχ2 t. (85)

In practice this is satisfied with a number of noise schedules of diffusion models (see Appendix F.1).

C. Derivation of Rex

We derive the Rex scheme presented in Proposition 3.2 in the main paper.

Nomenclature. As alluded to earlier, there exist two popular reparameterizations of the score function which are used widely in practice, namely the noise prediction (Ho et al., 2020) and data prediction (Kingma et al., 2021) formulations. Following the conventions of Lipman et al. (2024), we write noise prediction model as xT |t(x) = E[XT |Xt = x] and write data prediction model as x0|t(x) = E[X0|Xt = x]. Throughout this paper we will assume the existence of sufficiently trained diffusion models denoted xθ

T |t(x) ≈xT |t(x) and xθ

0|t(x) ≈x0|t(x).

<!-- Page 31 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

C.1. Rex (ODE)

In this section we derive the Rex scheme for the probability flow ODE. We present derivations for both the data prediction and noise prediction formulations. It is well known (Blasingame & Liu, 2025, Equation (19); cf. Domingo-Enrich et al., 2025, Equation (8)) that the ODE in Equation (6) can be rewritten as dxt dt =

˙βt βt xt + σt ˙αt −˙σtαt βt fθ(t, xt), (86)

where βt = −αt for noise prediction and βt = σt for target prediction. This choice of β and fθ thus depends on the particulars of the noise or data reparameterization. Remark C.1. Without loss of generality any of the results for the probability flow ODE apply to any arbitrary flow model which models an affine probability path (Lipman et al., 2024) with the correct conversions to the flow matching conventions.19

It is well observed that the structure of the ODE in Equation (86) can be greatly simplified via exponential integrators (Lu et al., 2022b; Zhang & Chen, 2023; Blasingame & Liu, 2024a). We make use of this insight to rewrite the ODE in a form which eliminates the discretization error in the f(t)xt linear term along with a time reparameterization which will simplify the construction of the reversible solver. To accomplish this, we use exponential integrators in the form of a change-of-variables with yt = exp(−

R t

T

˙βu βu du)xt = βT βt xt. N.B., we integrate from time T to t because the ODE in Equation (86) is defined in reverse-time. To achieve the time reparametrization, we introduce a new variable ςt defined as the signal-to-noise ratio (SNR) αt/σt for the data prediction formulation and defined as the inverse SNR σt/αt for the noise prediction formulation. Using this time change we find Proposition C.1, in Appendix C.1.1 we provide the full derivation of this result.

C.1.1. PROOF OF PROPOSITION C.1

We state Proposition C.1 below.

Proposition C.1. The probability flow ODE in Equation (86) can be rewritten in ςt as dyς dς = |βT |fθ ς, βς βT yς

, (87)

where yt = βT βt xt and ςt = αtσt β2 t.

Proof. Recall that from Equation (86) we have that the ODE is given by dxt dt =

˙βt βt xt + σt ˙αt −˙σtαt βt fθ(t, xt). (88)

We can use the technique of exponential integrators to rewrite the ODE as d dt h e

R t

T −

˙βu βu duxt i

= e

R t

T −

˙βu βu du σt ˙αt −˙σtαt βt fθ(t, xt), (89)

recalling that we integrate from initial time T in reverse-time. Then the exponential terms simplify to e

R t

T −

˙βu βu du = βT βt

. (90)

We introduce a change-of-variables yt = βT βt xt to rewrite the ODE as dyt dt = βT βt σt ˙αt −˙σtαt βt | {z } =υt fθ t, βt βT yt

. (91)

19I.e., sampling in forward-time such that X1 ∼q(X) and X0 ∼p(X).

<!-- Page 32 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Next we define

˙ςt = sgn(βT)σt ˙αt −˙σtαt β2 t

, (92)

which we will now justify. Now recall that βt is either −αt or σt depending on whether fθ denotes the data or noise prediction model. Moreover we know that αt is a strictly monotonically decreasing in t and that σt is strictly monotonically increasing in t. We will now prove that there exists an inverse function for ςt such that tς(ςt) = t for both cases.

Case βt = −αt. We can write υt as υt = αT

˙σtαt −σt ˙αt α2 t

, (93)

(i) = αT d dt σt αt

, (94)

where (i) holds by the quotient rule. Clearly, we have that

˙ςt = d dt σt αt

, (95)

ςt = σt αt

, (96)

It follows from (αt, σt) that ςt is strictly monotonically increasing in t and thus we can construct its inverse.

Case βt = σt. We can write υt as υt = σT σt ˙αt −˙σtαt σ2 t

, (97)

(i) = σT d dt αt σt

, (98)

where (i) holds by the quotient rule. Clearly, we have that

˙ςt = d dt αt σt

, (99)

ςt = αt σt

, (100)

It follows from (αt, σt) that ςt is strictly monotonically decreasing in t and thus we can construct its inverse.

Thus, we can rewrite the ODE via a time-change to find dyς dς = |βT |fθ ς, βς βT yς

, (101)

with the usual abuse-of-notation yς:= ytς(ς), βς:= βtς(ς), &c.

Remark C.2. When in the noise prediction formulation with Proposition C.1 we recover the following reparameterization of Equation (86)

dzχ dχ = αT xθ

T |χ αχ αT zχ

, (102)

where αT > 0, zt = αT αt xt and χt = σt αt, which has been observed by numerous prior works (see Song et al., 2021a, Equation (14); Pan et al., 2023, Equation (11); Wang et al., 2024, Equation (6)).

Remark C.3. When in the data prediction formulation, Proposition C.1 recovers Blasingame & Liu (2025, Proposition D.2) which states that Equation (86) can be written as dyγ dγ = σT xθ

0|γ σγ σT yγ

, (103)

where yt = σT σt xt and γt = αt σt.

<!-- Page 33 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

C.1.2. DATA PREDICTION

We present this derivation in the form of Lemma C.2 below.

Lemma C.2 (Rex (ODE) for data prediction models). Let Φ be an explicit Runge-Kutta solver for the ODE in Equation (103) with Butcher tableau aij, bi, ci. The reversible solver for Φ in terms of the original state xt is given by the forward step xn+1 = σn+1 σn

(ζxn + (1 −ζ)ˆxn) + σn+1Ψh(γn, ˆxn),

ˆxn+1 = σn+1 σn

ˆxn −σn+1Ψ−h(γn+1, xn+1),

(104)

and backward step

ˆxn = σn σn+1

ˆxn+1 + σnΨ−h(γn+1, xn+1), xn = σn σn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −σnζ−1Ψh(γn, ˆxn),

(105)

with step size h:= γn+1 −γn and where Ψ denotes the following scheme

ˆzi = 1 σn xn + h i−1 X j=1 aijxθ

0|γn+cjh(σγn+cjh ˆzj),

Ψh(γn, xn) = h s X i=1 bixθ

0|γn+cih(σγn+cih ˆzi),

(106)

Proof. Recall that the forward step of the McCallum-Foster method for Equation (103) given Φ is given as yn+1 = ζyn + (1 −ζ)ˆyn + Φh(γn, ˆyn),

ˆyn+1 = ˆyn −Φ−h(γn+1, yn+1), (107)

with step size h = γn+1 −γn. We use the definition of yt = σT σt xt to rewrite the forward pass as xn+1 = σn+1 σn

(ζxn + (1 −ζ)ˆxn) + σn+1 σT

Φh γn, σT σn

ˆxn

,

ˆxn+1 = σn+1 σn

ˆxn −σn+1 σT

Φ−h γn+1, σT σn+1 xn+1

.

(108)

Mutatis mutandis we find the backward step in xt to be given as

ˆxn = σn σn+1

ˆxn+1 + σn σT

Φ−h γn+1, σT σn+1 xn+1

, xn = σn σn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −σn σT ζ−1Φh γn, σT σn

ˆxn

,

(109)

Next we simplify the explicit RK scheme Φ(γn, yn) for the time-changed probability flow ODE in Equation (103). Recall that the RK scheme can be written as zi = yn + h i−1 X j=1 aijσT x0|γn+cjh σγn+cjh σT zj

,

Φh(γn, yn) = h s X i=1 biσT x0|γn+cih σγn+cih σT zi

.

(110)

<!-- Page 34 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Next, we replace yt back with xt which yields zi = σT



1 σn xn + h i−1 X j=1 aijx0|γn+cjh σγn+cjh σT zj



,

Φh γn, σT σn xn

= σT h s X i=1 bix0|γn+cih σγn+cih σT zi

.

(111)

To further simplify, let σT ˆzi = zi and define Ψh(γn, xn):= σT Φ(γn, σT σn xn).

Thus we can write the following reversible scheme with forward step xn+1 = σn+1 σn

(ζxn + (1 −ζ)ˆxn) + σn+1Ψh(γn, ˆxn),

ˆxn+1 = σn+1 σn

ˆxn −σn+1Ψ−h(γn+1, xn+1),

(112)

and the backward step

ˆxn = σn σn+1

ˆxn+1 + σnΨ−h(γn+1, xn+1), xn = σn σn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −σnζ−1Ψh(γn, ˆxn),

(113)

with the numerical scheme

ˆzi = 1 σn xn + h i−1 X j=1 aijxθ

0|γn+cjh(σγn+cjh ˆzj),

Ψh(γn, xn) = h s X i=1 bixθ

0|γn+cih(σγn+cih ˆzi).

(114)

C.1.3. NOISE PREDICTION

We present this derivation in the form of Lemma C.3 below.

Lemma C.3 (Rex (ODE) for noise prediction models). Let Φ be an explicit Runge-Kutta solver for the ODE in Equation (102) with Butcher tableau aij, bi, ci. The reversible solver for Φ in terms of the original state xt is given by the forward step xn+1 = αn+1 αn

(ζxn + (1 −ζ)ˆxn) + αn+1Ψh(χn, ˆxn),

ˆxn+1 = αn+1 αn

ˆxn −αn+1Ψ−h(χn+1, xn+1),

(115)

and backward step

ˆxn = αn αn+1

ˆxn+1 + αnΨ−h(χn+1, xn+1), xn = αn αn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −αnζ−1Ψh(χn, ˆxn),

(116)

with step size h:= χn+1 −χn and where Ψ denotes the following scheme

ˆzi = 1 αn xn + h i−1 X j=1 aijxθ

T |χn+cjh(αχn+cjh ˆzj),

Ψh(χn, xn) = h s X i=1 bixθ

T |χn+cih(αχn+cih ˆzi),

(117)

<!-- Page 35 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Proof. Recall that the forward step of the McCallum-Foster method for Equation (102) given Φ is given as zn+1 = ζzn + (1 −ζ)ˆzn + Φh(χn, ˆzn),

ˆzn+1 = ˆzn −Φ−h(χn+1, zn+1), (118)

with step size h = χn+1 −χn. We use the definition of zt = αT αt xt to rewrite the forward pass as xn+1 = αn+1 αn

(ζxn + (1 −ζ)ˆxn) + αn+1 αT

Φh χn, αT αn

ˆxn

,

ˆxn+1 = αn+1 αn

ˆxn −αn+1 αT

Φ−h χn+1, αT αn+1 xn+1

.

(119)

Mutatis mutandis we find the backward step in xt to be given as

ˆxn = αn αn+1

ˆxn+1 + αn αT

Φ−h χn+1, αT αn+1 xn+1

, xn = αn αn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −αn αT ζ−1Φh χn, αT αn

ˆxn

,

(120)

Next we simplify the explicit RK scheme Φ(χn, zn) for the time-changed probability flow ODE in Equation (103). Recall that the RK scheme can be written as zi = zn + h i−1 X j=1 aijαT x0|χn+cjh αχn+cjh αT zj

,

Φh(χn, zn) = h s X i=1 biαT x0|χn+cih αχn+cih αT zi

.

(121)

Next, we replace zt back with xt which yields zi = αT



1 αn xn + h i−1 X j=1 aijx0|χn+cjh αχn+cjh αT zj



,

Φh χn, αT αn xn

= αT h s X i=1 bix0|χn+cih αχn+cih αT zi

.

(122)

To further simplify, let αT ˆzi = zi and define Ψh(χn, xn):= αT Φ(χn, αT αn xn).

Thus we can write the following reversible scheme with forward step xn+1 = αn+1 αn

(ζxn + (1 −ζ)ˆxn) + αn+1Ψh(χn, ˆxn),

ˆxn+1 = αn+1 αn

ˆxn −αn+1Ψ−h(χn+1, xn+1),

(123)

and the backward step

ˆxn = αn αn+1

ˆxn+1 + αnΨ−h(χn+1, xn+1), xn = αn αn+1 ζ−1xn+1 + (1 −ζ−1)ˆxn −αnζ−1Ψh(χn, ˆxn),

(124)

with the numerical scheme

ˆzi = 1 αn xn + h i−1 X j=1 aijxθ

T |χn+cjh(αχn+cjh ˆzj),

Ψh(χn, xn) = h s X i=1 bixθ

T |χn+cih(αχn+cih ˆzi).

(125)

<!-- Page 36 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

C.2. Rex (SDE)

In this section we derive the Rex scheme for the reverse-time diffusion SDE along with several helper derivations. We rely on the time-changed Brownian motion machinery developed in Appendix B.5, and proceed by reparameterizing Equation (7) (Appendix C.2.1), specializing to the data prediction scenario (Appendix C.2.2), and then performing an analogous derivation for the noise prediction scenario (Appendix C.2.3).

C.2.1. PROOF OF REPARAMETRIZED SEMI-LINEAR SDE WITH ADDITIVE NOISE

Recall our general semi-linear SDE with additive noise from Equation (7) which represents an abstraction (mutatis mutandis) of diffusion SDEs with the form, dXt = [a(t)Xt + b(t)fθ(t, Xt)] dt + g(t) dWt. (126)

We now restate Proposition 3.1 below.

Proposition 3.1. Assume that g(t) = p a(t)b(t), b(t)/a(t) →∞as t →∞, and b(t) > 0. Let Ξ(t):= exp

R t

0 a(τ) dτ be the reciprocal of the integrating factor of Equation (7). Then the SDE in Equation (7) can be rewritten as dYς = fθ(ς, Ξ(ς)Yς) dς + dWς, (8)

where Yt = Ξ−1(t)Xt and ςt =

R

Ξ−1(t)b(t) dt.

Proof. Let Ξ(t) be defined as the reciprocal of the integrating factor of Equation (7), i.e.,

Ξ(t) = exp

Z t

0 a(s) ds

. (127)

We can now write Equation (7) as d

Ξ−1(t)Xt

= b(t)

Ξ(t)fθ(t, Xt) dt + g(t)

Ξ(t) dWt, (128)

dYt

(i) = b(t)

Ξ(t)fθ(t, Ξ(t)Yt) dt + g(t)

Ξ(t) dWt, (129)

where (i) holds via Yt:= Ξ−1(t)Xt. Now we wish to introduce a time-changed variable ςt, to simplify the calculation into the form dYt = dςt dt fθ(t, Ξ(t)Yt) dt + r dςt dt dWt, (130)

thus we have the equalities dςt dt = b(t)

Ξ(t), (131) r dςt dt = g(t)

Ξ(t), (132)

which means that since Ξ, b, g are all positive functions, we have b(t) Ξ(t)

(i) = g2(t)

Ξ2(t), (133)

Ξ(t) = g2(t)

b(t), (134)

<!-- Page 37 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers where (i) holds by the squaring Equation (132) and setting equal to ˙ςt. Then,

Z dςt dt dt =

Z b(t) Ξ(t) dt, (135)

ςt =

Z b2(t)

g2(t) dt. (136)

Now we need to perform the time-change of the Brownian motion. For this we can just follow Lemma B.3 mutatis mutandis to find r dςt dt dWt = dWς, (137)

with σt →∞as t →∞since | g(t)

b(t) | = O(

√ t). Thus the SDE in Equation (7) becomes dYς = fθ(ς, Ξ(ς)Yς) dς + dWς, (138)

with abuse of notation for functions of ς−1(ςt) = t being denoted by ς. N.B., this inverse exists since b(t)̸ = 0 for all t ≥0.

C.2.2. PROOF OF REPARAMETRIZED SDE FOR DATA PREDICTION MODELS

It is well known (Lu et al., 2022a) that the reverse-time diffusion SDE in Equation (5) can be rewritten in terms of the data prediction model as dXt = f(t) + g2(t)

σ2 t

Xt −αtg2(t)

σ2 t xθ

0|t(Xt)

dt + g(t) dW t. (139)

Remarkably, following a similar derivation to the one above for the probability flow ODE yields a time-changed SDE with a very similar form to the one above, sans the Brownian motion term and different weighting terms.

Lemma C.4 (Time reparametrization of the reverse-time diffusion SDE). The reverse-time SDE in Equation (139) can be rewritten in terms of the data prediction model as dYϱ = σT γT xθ

0|ϱ γT σϱ σT γϱ

Yϱ dϱ + σT γT dWϱ, (140)

where Yt = σ2

T αt σ2 t αT Xt and ϱt:= α2 t σ2 t.

Proof. We rewrite Equation (5) in terms of the data prediction model, using the identity

∇x log pt(x) = −1 σ2 t x + αt σ2 t x0|t(x), (141)

to find dXt =



 f(t) + g2(t)

σ2 t

| {z } =a(t)

Xt +

−αtg2(t)

σ2 t

| {z } =b(t)

x0|t(Xt)



dt + g(t) dW t, (142)

where f(t) = ˙αt αt

, g2(t) = ˙σ2 t −2 ˙αt αt σ2 t = −2σ2 t d log γt dt. (143)

<!-- Page 38 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Next we find the integrating factor Ξt = exp

−

R t

T a(u) du

,

Ξt = exp

Z T t d log αu du + g2(u)

σ2u du

!

, (144)

= exp

Z T t d log αu du −2d log γu du du

!

, (145)

= exp

Z T t d log αu du −2 d log αu du −d log σu du du

!

, (146)

= exp

Z T t d log σ2 u du −d log αu du du

!

, (147)

= exp log σ2

T −log σ2 t −(log αT −log αt)

, (148)

= σ2

T αt σ2 t αT

. (149)

We can write the integrating factor in terms of γt as

Ξt = σT γt σtγT

. (150)

Moreover we can further simplify b(t) as b(t) = −αtg2(t)

σ2 t

, (151)

= 2αt d log γt dt. (152)

Thus we can rewrite the SDE in Equation (142) as d σT γT γt σt

Xt

= 2σT γT αt σt γt d log γt dt x0|t(Xt) dt + σT γT γt σt r

−2σ2 t d log γt dt dW t, (153)

dYt

(i) = 2σT γT αt σt γt d log γt dt x0|t γT σt σT γt

Yt dt + σT γT γt σt r

−2σ2 t d log γt dt dW t, (154)

dYt = σT γT dγ2 t dt x0|t γT σt σT γt

Yt dt + σT γT r

−γ2 t d log γ2 t dt dW t, (155)

dYt = σT γT dγ2 t dt x0|t γT σt σT γt

Yt dt + σT γT r

−dγ2 t dt dW t, (156)

dYϱ

(ii) = σT γT x0|ϱ γT σϱ σT γϱ

Yϱ dϱ + σT γT dWϱ, (157)

where (i) holds by the change-of-variables Yt = σT γt γT σt Xt and (ii) holds by Lemma B.3.

C.2.3. PROOF OF REPARAMETRIZED SDE FOR NOISE PREDICTION MODELS

Lemma C.5 (Time reparametrization of the reverse-time diffusion SDE for noise prediction models). The reverse-time SDE in Equation (5) can be rewritten in terms of the noise prediction model as dYχ = 2αT xθ

T |χ αχ αT

Yχ dχ + αT dW χ2, (158)

where Yt = αt αT Xt and χt:= σt αt.

<!-- Page 39 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Proof. We rewrite Equation (5) in terms of the noise prediction model to find dXt = f(t)Xt + g2(t)

σt xθ

T |t(Xt)

dt + g(t) dW t, (159)

where f(t) = ˙αt αt

, g2(t) = ˙σ2 t −2 ˙αt αt σ2 t = −2σ2 t d log γt dt. (160)

Next we find the integrating factor to be exp

−

R t

T f(u) du

= αT αt. Moreover, we can further simplify g2(t)

σt as g2(t)

σt

= −2σt d log γt dt, (161)

= −2σt

˙γt γt

, (162)

= −2σt γt

˙αtσt −αt ˙σt σ2 t

, (163)

= −2σ2 t αt

˙αtσt −αt ˙σt σ2 t

, (164)

= 2σ2 t αt αt ˙σt −˙αtσt σ2 t

, (165)

= 2αt ˙σt −˙αtσt αt

, (166)

(167)

Let χt:= σt αt = 1 γt. Thus we can rewrite the SDE in Equation (159) as d αT αt

Xt

= αT αt g2(t)

σ2 t xθ

T |t(Xt) dt + αT αt r

−2σ2 t d log γt dt dW t, (168)

dYt

(i) = αT αt g2(t)

σ2 t xθ

T |t αt αT

Yt dt + αT αt r

−2σ2 t d log γt dt dW t, (169)

dYt = 2αT αt ˙σt −˙αtσt α2 t xθ

T |t αt αT

Yt dt + αT αt r

−2σ2 t d log γt dt dW t, (170)

dYt

(ii) = 2αT ˙χtxθ

T |t αt αT

Yt dt + αT s

−2σ2 t α2 t d log γt dt dW t, (171)

dYt = 2αT ˙χtxθ

T |t αt αT

Yt dt + αT q

˙χ2 t dW t, (172)

dYχ

(iii) = 2αT xθ

T |χ αχ αT

Yχ dχ + αT dW χ2, (173)

(174)

where (i) holds by the change-of-variables Yt = αT αt Xt, (ii) holds by

−2σ2 t α2 t d log γt dt = σ2 t α2 t d(−2 log γt)

dt, (175)

= σ2 t α2 t d log χ2 t dt, (176)

= σ2 t α2 t

˙χ2 t χ2 t

, (177)

= ˙χ2 t, (178)

and (iii) holds by Lemma B.3 mutatis mutandis for χt.

<!-- Page 40 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

C.2.4. DERIVATION OF REX (SDE)

We present derivations for both the data prediction and noise prediction formulations.

Data Prediction. We present this derivation in the form of Lemma C.6 below.

Lemma C.6 (Rex (SDE) for data prediction models). Let Φ be an explicit stochastic Runge-Kutta solver for the additive noise SDE in Equation (140), we construct the following reversible scheme for diffusion models

Xn+1 = σn+1γn γn+1σn

(ζXn + (1 −ζ) ˆ Xn) + σn+1 γn+1

Ψh(ϱn, ˆ Xn, Wϱ(ω)),

ˆ Xn+1 = σn+1γn γn+1σn

ˆ Xn −σn+1 γn+1

Ψ−h(ϱn+1, Xn+1, Wϱ(ω)),

(179)

and the backward step is given as

ˆ Xn = σnγn+1 γnσn+1

ˆ Xn+1 + σn γn

Ψ−h(ϱn+1, Xn+1, Wϱ(ω)),

Xn = σnγn+1 γnσn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn −σn γn ζ−1Ψh(ϱn, ˆ Xn, Wϱ(ω)),

(180)

with step size h:= ϱn+1 −ϱn and where Ψ denotes the following scheme

ˆZi = γn σn

Xn + h i−1 X j=1 aijxθ

0|ϱn+cjh σϱn+cjh γϱn+cjh

ˆ Zj

+ aW i Wn + aH i Hn,

Ψh(ϱn, Xn, Wϱ(ω)) = h s X j=1 bixθ

0|ϱn+cih σϱn+cih γϱn+cih

ˆZi

+ bW Wn + bHHn.

(181)

Proof. We write the SRK scheme for the time-changed reverse-time SDE in Equation (140) to construct the following SRK scheme

Zi = Yn + h i−1 X j=1 aij σT γT x0|ϱn+cjh γT σϱn+cjh σT γϱn+cjh

Zj

+ σT γT

(aW i Wn + aH i Hn),

Yn+1 = Yn + h s X i=1 bi σT γT x0|ϱn+cih γT σϱn+cih σT γϱn+cih

Zi

+ σT γT

(bW Wn + bHHn),

(182)

with step size h = ϱn+1 −ϱn. Next, we replace Yt back with Xt which yields

Zi = σT γT



γn σn

Xn + h i−1 X j=1 aijx0|ϱn+cjh γT σϱn+cjh σT γϱn+cjh

Zj





+ σT γT

(aW i Wn + aH i Hn), σT γn+1 γT σn+1

Xn+1 = σT γn γT σn

Xn

+ σT γT h s X i=1 bi σT γT x0|ϱn+cih γT σϱn+cih σT γϱn+cih

Zi

+ σT γT

(bW Wn + bHHn)

| {z } =Ψh(ϱn,Xn,Wϱ)

.

(183)

To further simplify, let σT γT ˆZi = Zi, then we construct the reversible scheme with forward pass:

Xn+1 = σn+1γn γn+1σn

(ζXn + (1 −ζ) ˆ Xn) + σn+1 γn+1

Ψh(ϱn, ˆ Xn, Wϱ(ω)),

ˆ Xn+1 = σn+1γn γn+1σn

ˆ Xn −σn+1 γn+1

Ψ−h(ϱn+1, Xn+1, Wϱ(ω)),

(184)

<!-- Page 41 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers and backward pass

ˆ Xn = σnγn+1 γnσn+1

ˆ Xn+1 + σn γn

Ψ−h(ϱn+1, Xn+1, Wϱ(ω)),

Xn = σnγn+1 γnσn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn −σn γn ζ−1Ψh(ϱn, ˆ Xn, Wϱ(ω)),

(185)

with step size h:= ϱn+1 −ϱn and where

ˆZi = γn σn

Xn + h i−1 X j=1 aijxθ

0|ϱn+cjh σϱn+cjh γϱn+cjh

ˆ Zj

+ aW i Wn + aH i Hn,

Ψh(ϱn, Xn, Wϱ(ω)) = h s X j=1 bixθ

0|ϱn+cih σϱn+cih γϱn+cih

ˆZi

+ bW Wn + bHHn.

(186)

Noise Prediction. We present this derivation in the form of Lemma C.7 below.

Lemma C.7 (Rex (SDE) for noise prediction models). Let Φ be an explicit stochastic Runge-Kutta solver for the additive noise SDE in Equation (158), we construct the following reversible scheme for diffusion models

Xn+1 = αn+1 αn

(ζXn + (1 −ζ) ˆ Xn) + αn+1Ψh(χn, ˆ Xn, Wχ2(ω)),

ˆ Xn+1 = αn+1 αn

ˆ Xn −αn+1Ψ−h(χn+1, Xn+1, Wχ2(ω)),

(187)

and the backward step is given as

ˆ Xn = αn αn+1

ˆ Xn+1 + αnΨ−h(χn+1, Xn+1, Wχ2(ω)),

Xn = αn αn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn −αnζ−1Ψh(χn, ˆ Xn, Wχ2(ω)),

(188)

with step size h:= χn+1 −χn and where Ψ denotes the following scheme

ˆZi = 1 αn

Xn + h i−1 X j=1 h

2aijxθ T |χn+cjh αχn+cjh ˆ Zj i

+ aW i Wn + aH i Hn,

Ψh(χn, Xn, Wχ(ω)) = h s X i=1 h

2bixθ T |χn+cih αχn+cih ˆZi i

+ bW Wn + bHHn.

(189)

Proof. We write the SRK scheme for the time-changed reverse-time SDE in Equation (158) to construct the following SRK scheme

Zi = Yn + h i−1 X j=1

2aijαT xT |χn+cjh αχn+cjh αT

Zj

+ αT (aW i Wn + aH i Hn),

Yn+1 = Yn + h s X i=1

2biαT xT |χn+cih αχn+cih αT

Zi

+ αT (bW Wn + bHHn),

(190)

<!-- Page 42 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers with step size h = χn+1 −χn. Next, we replace Yt back with Xt which yields

Zi = αT



1 αn

Xn + h i−1 X j=1

2aijxT |χn+cjh αχn+cjh αT

Zj





+ αT (aW i Wn + aH i Hn), αn+1 αT

Xn+1 = αT αn

Xn

+ αT h s X i=1

2biαT xT |χn+cih αχn+cih αT

Zi

+ αT (bW Wn + bHHn)

| {z } =Ψh(χn,Xn,Wχ)

.

(191)

To further simplify, let αT ˆZi = Zi, then we construct the reversible scheme with forward pass:

Xn+1 = αn+1 αn

(ζXn + (1 −ζ) ˆ Xn) + αn+1Ψh(χn, ˆ Xn, Wχ(ω)),

ˆ Xn+1 = αn+1 αn

ˆ Xn −αn+1Ψ−h(χn+1, Xn+1, Wχ(ω)),

(192)

and backward pass

ˆ Xn = αn αn+1

ˆ Xn+1 + αnΨ−h(χn+1, Xn+1, Wχ(ω)),

Xn = αn αn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn −αnζ−1Ψh(χn, ˆ Xn, Wχ(ω)),

(193)

with step size h:= χn+1 −χn and where

ˆZi = 1 αn

Xn + h i−1 X j=1 h

2aijxθ T |χn+cjh αχn+cjh ˆ Zj i

+ aW i Wn + aH i Hn,

Ψh(χn, Xn, Wχ(ω)) = h s X i=1 h

2bixθ T |χn+cih αχn+cih ˆZi i

+ bW Wn + bHHn.

(194)

N.B., Wn = W χ2 n+1 −W χ2n.

C.3. Proof of Proposition 3.2

We now can construct Rex.

<!-- Page 43 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Proposition C.8 (Rex). Without loss of generality, let Φ denote an explicit SRK scheme for the SDE in Equation (140) with extended Butcher tableau aij, bi, ci, aW i, aH i, bW, bH. Fix an ω ∈Ωand let W be the Brownian motion over time variable ς. Then the reversible solver constructed from Φ in terms of the underlying state variable Xt is given by the forward step

Xn+1 = wn+1 wn ζXn + (1 −ζ) ˆ Xn

+ wn+1Ψh(ςn, ˆ Xn, Wn(ω)),

ˆ Xn+1 = wn+1 wn

ˆ Xn −wn+1Ψ−h(ςn+1, Xn+1, Wn(ω)),

(195)

and backward step

ˆ Xn = wn wn+1

ˆ Xn+1 + wnΨ−h(ςn+1, Xn+1, Wn(ω)),

Xn = wn wn+1 ζ−1Xn+1 + (1 −ζ−1) ˆ Xn −wnζ−1Ψh(ςn, ˆ Xn, Wn(ω)),

(196)

with step size h:= ςn+1 −ςn and where Ψ denotes the following scheme

ˆZi = 1 wn

Xn + h i−1 X j=1 h aijfθ ςn + cjh, wςn+cjh ˆZj i

+ aW i Wn(ω) + aH i Hn(ω),

Ψh(ςn, Xn, Wn(ω)) = h s X i=1 h bifθ ςn + cih, wςn+cih ˆZi i

+ bW Wn(ω) + bHHn(ω),

(197)

where fθ denotes the data prediction model, wn = σn γn and ςt = ϱt. The ODE case is recovered for an explicit RK scheme Φ for the ODE in Equation (103) with wn = σn and ςt = γt. For noise prediction models we have fθ denoting the noise prediction model with wn = αn and ςt = σn αn.

Proof. This follows by Lemmas C.2, C.3, C.6 and C.7 mutatis mutandis.

D. Convergence Order Proofs

D.1. Assumptions

Beyond the general regularity conditions imposed on the learned diffusion model itself (see Lu et al., 2022b; Blasingame & Liu, 2024a; 2025), we also assert that in the noise prediction setting that αT > 0. In practice most commonly used diffusion noise schedules like the linear or scaled linear schedule satisfy this, (see Appendix F.1; cf. Lin et al., 2024).

D.2. Proof of Theorem 3.3

Theorem 3.3 (Rex is a k-th order solver). Let Φ be a k-th order explicit Runge-Kutta scheme for the reparameterized probability flow ODE in Equation (87) with variance preserving noise schedule (αt, σt). Then Rex constructed from Φ is a k-th order solver, i.e., given the reversible solution {xn, ˆxn}N n=1 and true solution xtn we have

∥xn −xtn∥≤Chk, (14)

for constants C, hmax > 0 and for step sizes h ∈[0, hmax].

Proof. We will prove this for both the data prediction and noise prediction formulations.

Data prediction. By Theorem A.1 we have that reversible Φ is a k-th order solver, and thus

∥yn −ytn∥≤Chk. (198)

<!-- Page 44 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

We use the change of variables from Equation (103) to find σT σn xn −σT σn xtn

≤Chk, (199)

which simplifies to

∥xn −xtn∥≤σn σT

Chk. (200)

Now by definition for variance preserving type diffusion SDEs we have that σt ≤1 for all t. Thus we can write

∥xn −xtn∥≤C1hk, (201)

where C1 = C σT.

Noise prediction. By Theorem A.1 we have that reversible Φ is a k-th order solver, and thus

∥yn −ytn∥≤Chk. (202)

We use the change of variables from Equation (102) to find αT αn xn −αT αn xtn

≤Chk, (203)

which simplifies to

∥xn −xtn∥≤αn αT

Chk. (204)

Now by definition we have αt ≤1 for all t and we assume that αT > 0. Thus we can write

∥xn −xtn∥≤C1hk, (205)

where C1 = C σT.

D.3. Proof of Theorem 3.4

Definition D.1 (Strong order of convergence). Suppose an SDE solver admits a numerical solution Xn and we have a true solution Xtn. If sup 0≤n≤N E∥Xn −Xtn∥2 ≤Ch2α, (206)

where C > 0 is a constant and h is the step size, then the SDE solver strongly converges with order α.

Theorem 3.4 (Convergence order for Princeps). Let Φ be a SRK scheme with strong order of convergence ξ > 0 for the reparameterized reverse-time diffusion SDE in Equation (8) with variance preserving noise schedule (αt, σt) and αT > 0. Then Ψ constructed from Φ has strong order of convergence ξ.

Proof. We will prove this for both the data prediction and noise prediction formulations.

Data prediction. By definition we have Φ has strong order of convergence ξ and thus, sup 0≤n≤N E∥Yn −Ytn∥2 ≤Ch2ξ, (207)

where h = σ2 n+1 αn+1 −σ2 n αn. We use the change of variables from Equation (140) to find sup 0≤n≤N E σ2

T αn σ2nαT

Xn −σ2

T αn σ2nαT

Xtn

2 ≤Ch2ξ, (208)

which simplifies to sup 0≤n≤N E∥Xn −Xtn∥2 ≤σn√αT σT √αn

Ch2ξ. (209)

<!-- Page 45 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Since by definition αn is a monotonically decreasing function, σn is a monotonically increasing function, αT > 0, and σT ≤1 we can write sup 0≤n≤N E∥Xn −Xtn∥2 ≤Ch2ξ, (210)

as σn√αT σT √αn

≤1. (211)

Noise prediction. By definition we have Φ has strong order of convergence ξ and thus, sup 0≤n≤N E∥Yn −Ytn∥2 ≤Ch2ξ, (212)

where h = σn+1 αn+1 −σn αn. We use the change of variables from Equation (158) to find sup 0≤n≤N E αn αT

Xn −αn αT

Xtn

2 ≤Ch2ξ, (213)

which simplifies to sup 0≤n≤N E∥Xn −Xtn∥2 ≤

√αT √αn

Ch2ξ. (214)

Since by definition αn is a monotonically decreasing function strictly less than 1 and αT > 0, we can write sup 0≤n≤N E∥Xn −Xtn∥2 ≤Ch2ξ. (215)

E. Relation to Other Solvers for Diffusion Models

While this paper primarily focused on Rex and the family of reversible solvers created by it, we wish to discuss the relation between the underlying scheme Ψ constructed from our method and other existing solvers for diffusion models. The solvers considered here are all non-reversible; for a discussion of prior reversible solvers for diffusion models (EDICT, BDIA, O-BELM, CycleDiffusion) see Appendix A.3.

dXt = [a(t)Xt + b(t)fθ(t, Xt)] dt + g(t) dWt dYς = fθ(ς, Ξ(ς)Yς) + dWς

Xn+1 = Ξ(tn) Ξ(tn+1)Xn + Ψh(tn, Xn, Wn(ω)) Yn+1 = Yn + Φh(ςn, Yn, Wn(ω))

Exponential integrators & change-of-variables

Lawson method

**Figure 10.** Overview of the construction of Ψ for the probability flow ODE from an underlying RK scheme Φ for the reparameterized

ODE. This graph holds for the SDE case mutatis mutandis.

Surprisingly, we discover that using Lawson methods outlined in Figure 10 (cf. Figure 3 from the main paper) is a generalized methodology for construing numerical schemes for diffusion modes, and that it subsumes previous works. This means that several of the reversible schemes we presented here are reversible variants of well known schemes in the literature in diffusion models.

Theorem 3.5 (Princeps subsumes previous solvers). Princeps subsumes the following solvers for diffusion models 1. DDIM (Song et al., 2021a),

2. DPM-Solver-1, DPM-Solver-2, DPM-Solver-12 (Lu et al., 2022b),

3. DPM-Solver++1, DPM-Solver++(2S), SDE-DPM-Solver-1, SDE-DPM-Solver++1 (Lu et al., 2022a), 4. SEEDS-1 (Gonzalez et al., 2024), and

5. gDDIM (Zhang et al., 2023).

<!-- Page 46 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Proof. We prove the connection to each solver in the list within a set of separate propositions for easier readability. The statement holds true via Propositions E.1 to E.8 and Corollaries E.1.1 to E.6.1.

Corollary E.0.1. Rex is the reversible version of the well-known solvers for diffusion models in Theorem 3.5.

Remark E.1. The SDE solvers constructed from Foster-Reis-Strange SRK schemes are wholly unique (with the exception of the trivial Euler-Maruyama scheme) and have no existing counterpart in the literature in diffusion models. Thus Rex (ShARK) is not only a novel reversible solver, but a novel solver for diffusion models in general.

E.1. Rex as Reversible ODE Solvers

Here we discuss Rex as reversible versions for well-known numerical schemes for diffusion models. Recall that the general Butcher tableau for a s-stage explicit RK scheme (Stewart, 2022, Section 6.1.4) is written as c1 c2 a21 c3 a31 a32............

cs as1 as2 · · · a(s−1)s b1 b2 · · · bs−1 bs

= c a b. (216)

Embedded methods for adaptive step sizing are of the form c1 c2 a21 c3 a31 a32............

cs as1 as2 · · · a(s−1)s b1 b2 · · · bs−1 bs b∗

1 b∗

2 · · · b∗ s−1 b∗ s

, (217)

where the lower-order step is given by the coefficients b∗ i.

E.1.1. EULER

In this section we explore the numerical schemes produced by choosing the Euler scheme for Φ. The Butcher tableau for the Euler method is

0 0 1. (218)

Proposition E.1 (Rex (Euler) is reversible DPM-Solver++1). The underlying scheme of Rex (Euler) for the data prediction parameterization of diffusion models in Equation (103) is the DPM-Solver++1 from Lu et al. (2022a).

Proof. Apply in the Butcher tableau for the Euler scheme to Ψ constructed from Equation (102) to find xn+1 = σn+1 σn xn + σn+1hxθ

0|γn(xn), (219)

<!-- Page 47 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers with h = γn+1 −γn. We can rewrite the step size as σn+1h = σn+1 αn+1 σn+1

−αn σn

, (220)

= αn+1 −αn σn+1 σn

, (221)

= αn+1 αn+1 αn+1

− αn αn+1 σn+1 σn

, (222)

= −αn+1 αn αn+1 σn+1 σn

−1

, (223)

= −αn+1 γn γn+1

−1

, (224)

= −αn+1 e log γn γn+1 −1

, (225)

= −αn+1 elog γn−log γn+1 −1

, (226)

(i) = −αn+1 eλn−λn+1 −1

, (227)

(ii) = −αn+1 e−hλ −1

, (228)

where (i) holds by the letting λt = log γt following the notation of Lu et al. (2022b;a) and (ii) holds by letting hλ = λn+1 −λn. Plugging this back into Equation (219) yields xn+1 = σn+1 σn xn −αn+1 e−hλ −1 xθ

0|tn(xn), (229)

which is the DPM-Solver++1 from Lu et al. (2022a).

Corollary E.1.1 (Rex (Euler) is reversible deterministic DDIM for data prediction models). The underlying scheme of Rex (Euler) for the data prediction parameterization of diffusion models in Equation (103) is the deterministic DDIM solver from Song et al. (2021a).

Proof. This holds because DPM-Solver++1 is DDIM see Lu et al. (2022a, Equation (21)) with η = 0.

Proposition E.2 (Rex (Euler) is reversible DPM-Solver-1). The underlying scheme of Rex (Euler) for the data prediction parameterization of diffusion models in Equation (102) is the DPM-Solver-1 from Lu et al. (2022b, Equation (3.7)).

Proof. Apply in the Butcher tableau for the Euler scheme to Ψ from Rex (see Proposition 3.2) to find xn+1 = αn+1 αn xn + αn+1hxθ

T |χn(xn), (230)

<!-- Page 48 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers with h = χn+1 −χn. We can rewrite step size as αn+1h = αn+1 σn+1 αn+1

−σn αn

, (231)

= σn+1 −σn αn+1 αn

, (232)

= σn+1 σn+1 σn+1

− σn σn+1 αn+1 αn

, (233)

= −σn+1 σn σn+1 αn+1 αn

−1

, (234)

= −σn+1 χn χn+1

−1

, (235)

= −σn+1 e log χn χn+1 −1

, (236)

= −σn+1 elog χn−log χn+1 −1

, (237)

(i) = −σn+1 e−λn+λn+1 −1

, (238)

(ii) = −σn+1 ehλ −1

, (239)

where (i) holds by letting λt = log γt = −log χt following the notation of Lu et al. (2022b;a) and (ii) holds by letting hλ = λn+1 −λn. Plugging this back into Equation (219) yields xn+1 = αn+1 αn xn −σn+1 ehλ −1 xθ

T |tn(xn), (240)

which is the DPM-Solver-1 from Lu et al. (2022b).

Corollary E.2.1 (Rex (Euler) is reversible deterministic DDIM for noise prediction models). The underlying scheme of Rex (Euler) for the noise prediction parameterization of diffusion models in Equation (102) is the deterministic DDIM solver from Song et al. (2021a).

Proof. This holds because DPM-Solver-1 is DDIM see Lu et al. (2022b, Equation (4.1)).

E.1.2. SECOND-ORDER METHODS

In this section we explore the numerical schemes produced by choosing the explicit midpoint method for Φ. We can write a generic second-order method as

0 η η 1 − 1 2η 1 2η

, (241)

for η̸ = 0 (Butcher, 2016). The choice of η = 1

2 yields the explicit midpoint, η = 2 3 gives Ralston’s second-order method, and η = 1 gives Heun’s second-order method.

Proposition E.3 (Rex (generic second-order) is reversible DPM-Solver++(2S)). The underlying scheme of Rex (generic second-order) for the data prediction parameterization of diffusion models in Equation (103) is the DPM-Solver++(2S) from Lu et al. (2022a, Algorithm 1).

Proof. The DPM-Solver++(2S) (Lu et al., 2022a, Algorithm 1) is defined as u = σp σn xn −αp e−rλhλ −1 xθ

0|tn(xn),

D =

1 − 1 2rλ xθ

0|tn(xn) + 1 2rλ xθ

0|tp(u), xn+1 = σn+1 σn xn −αn+1 e−hλ −1

D,

(242)

<!-- Page 49 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers for some intermediate timestep tn > tp > tn+1 and with rλ = λp−λn λn+1−λn. Notice that rλ describes the location of the midpoint time in the λ-domain as a ratio, i.e., we could say λp = λn + rλhλ, (243)

where rλ ∈(0, 1) denotes the interpolation point between the initial timestep λn and terminal timestep λn+1. Thus we fix η = rλ as the step size ratio of the intermediate point.

Now we return to the underlying scheme of Rex applied to the generic second-order scheme, see Equation (241), Apply in the Butcher tableau for generic second-order scheme to Ψ constructed from Equation (102) to find z = 1 σn xn + ηhxθ

0|γn(xn), xn+1 = σn+1 σn xn + σn+1h

1 −1 2η xθ

0|γn(xn) + 1 2η xθ 0|γn+ηh(σpz)

,

(244)

with h = γn+1 −γn and σp = σγn+ηh with γp = γn + ηh. We can write σpz = σp σn xn + σpηhxθ

0|γn(xn). (245)

Plugging this back into Equation (244) yields σpz = σp σn xn + σpηhxθ

0|γn(xn), xn+1 = σn+1 σn xn + σn+1h

1 −1 2η xθ

0|γn(xn) + 1 2η xθ 0|γn+ηh(σpz)

| {z } = ˆ D

, (246)

which is the DPM-Solver++1 from Lu et al. (2022a). Now recall from Proposition E.1 that σn+1h = −αn+1 e−hλ −1)

, (247)

it follows that σpηh = −αp e−rλhλ −1

, (248)

due to λp −λn = rλhλ and ηh = λp −λn. Thus by letting σpz = u and ˆD = D we recover the DPM-Solver++(2S) solver.

Proposition E.4 (Rex (generic second-order) is reversible DPM-Solver-2)). The underlying scheme of Rex (generic second-order) for the noise prediction parameterization of diffusion models in Equation (102) is the DPM-Solver-2 from Lu et al. (2022b, Algorithm 4 cf. Algorithm 1).

Proof. This follows as straightforward derivation from Proposition E.2 and Proposition E.3.

Proposition E.5 (Rex (Euler-Midpoint) is DPM-Solver-12). The underlying scheme of Rex (Euler-Midpoint) for the noise prediction parameterization of diffusion models in Equation (102) is the DPM-Solver-12 from Lu et al. (2022b).

Proof. The explicit midpoint method with embedded Euler method for adaptive step sizing is given by the Butcher tableau

0 1 2 1 2 0 1 1 0

. (249)

From Proposition E.2 and Proposition E.4 we have shown that Rex (Euler) and Rex (Midpoint) correspond to DPM-Solver-1 and DPM-Solver-2 respectively. Thus the Butcher tableau above outlines DPM-Solver-12.

<!-- Page 50 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

E.1.3. THIRD-ORDER METHODS

For third-order solvers like DPM-Solver-3 (Lu et al., 2022b, Algorithm 5) our constructed scheme differs from solvers derived using ETD methods due to the presence of φ2 terms where φk+1(t) =

Z 1

0 e(1−δ)t δk k! dδ, (250)

This reasoning also extends to the DPM-Solver-4 from Gonzalez et al. (2024, Algorithm 7).

E.2. Rex as Reversible SDE Solvers

In this section we discuss the connections between Rex and pre-existing SDE solvers for diffusion models.

E.2.1. EULER-MARUYAMA

The extended Butcher tableau for the Euler-Maruyama scheme is given by

0 0 0 0

1 1 0. (251)

Proposition E.6 (Rex (Euler-Maruyama) is reversible SDE-DPM-Solver++1). The underlying scheme of Rex (Euler- Maruyama) for the data prediction parameterization of diffusion models in Equation (140) is the SDE-DPM-Solver++1 from Lu et al. (2022a, Equation (18)).

Proof. Apply in the Butcher tableau for the Euler-Maruyama scheme to Ψ constructed from Equation (158) to find xn+1 = σ2 n+1αn σ2nαn+1 xn + σ2 n+1 αn+1 hxθ

0|ϱn(xn) + σ2 n+1 αn+1

Wn, (252)

with h = ϱn+1 −ϱn. We can rewrite the step size as σ2 n+1 αn+1 h = σ2 n+1 αn+1 α2 n+1 σ2 n+1

−α2 n σ2n

, (253)

= αn+1 − α2 n αn+1 σ2 n+1 σ2n

, (254)

= αn+1

1 − α2 n α2 n+1 σ2 n+1 σ2n

, (255)

= αn+1

1 − ϱn ϱn+1

, (256)

= αn+1

1 −e 2 log γn γn+1

, (257)

= αn+1

1 −e2 log γn−2 log γn+1, (258)

(i) = αn+1

1 −e2λn−2λn+1, (259)

(ii) = αn+1

1 −e−2hλ, (260)

where (i) holds by letting λt = log γt following the notation of Lu et al. (2022b;a) and (ii) holds by letting hλ = λn+1 −λn. Now recall that σ2 n+1αn σ2nαn+1

= σn+1 σn e−hλ. (261)

Plugging these back into Equation (252) yields xn+1 = σn+1 σn e−hλxn + αn+1

1 −e−2hλ xθ

0|tn(xn) + σ2 n+1 αn

Wn. (262)

<!-- Page 51 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Now recall that the Brownian increment Wn:= Wϱn+1 −Wϱn has variance h. Thus via the Itô isometry we can write

Wn ∼

√ hϵ, (263)

with ϵ ∼N(0, I). Then we have σ2 n+1 αn+1

√ h = σ2 n+1 αn+1 s α2 n+1 σ2 n+1

−α2n σ2n

, (264)

= s σ2 n+1 − α2n α2 n+1 σ4 n+1 σ2n

, (265)

= σn+1 s

1 − α2n α2 n+1 σ2 n+1 σ2n

, (266)

= σn+1 r

1 − ϱn ϱn+1

, (267)

= σn+1 p

1 −e−2hλ. (268)

Thus we have re-derived the noise term of the SDE-DPM-Solver++1, and putting everything together we have obtained the SDE-DPM-Solver++1 from Lu et al. (2022a) which is xn+1 = σn+1 σn e−hλxn + αn+1

1 −e−2hλ xθ

0|tn(xn) + σn+1 p

1 −e−2hλϵ. (269)

Thus we have shown that the SDE-DPM-Solver++1 is the same as the underlying scheme of Rex (Euler-Maruyama).

Corollary E.6.1 (Rex (Euler-Maruyama) is reversible stochastic DDIM). The underlying scheme of Rex (Euler-Maruyama) for the data prediction parameterization of diffusion models in Equation (140) is the stochastic DDIM solver from Song et al. (2021a) with η = σt

√

1 −e−2hλ.

Proof. This holds because SDE-DPM-Solver-1 is DDIM see Lu et al. (2022a, Section 6.1).

Proposition E.7 (Rex (Euler-Maruyama) is reversible SDE-DPM-Solver-1). The underlying scheme of Rex (Euler- Maruyama) for the noise prediction parameterization of diffusion models in Equation (158) is the SDE-DPM-Solver-1 from Lu et al. (2022a, Equation (17)).

Proof. Apply in the Butcher tableau for the Euler scheme to Ψ from Rex (see Proposition 3.2) to find xn+1 = αn+1 αn xn + 2αn+1hxθ

T |χn(xn) + αn+1Wn, (270)

with h = χn+1 −χn. Recall from Proposition E.2 that we can rewrite the step size αn+1h = −σn+1 ehλ −1

. (271)

Now recall that the Brownian increment Wn:= W χ2 n+1 −W χ2 n has variance χ2 n −χ2 n+1.20 Thus via the Itô isometry we can write

Wn ∼ q χ2n −χ2 n+1ϵ, (272)

20This is because W 2 χ is defined in reverse-time.

<!-- Page 52 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers with ϵ ∼N(0, I). Then we have αn+1 q χ2n −χ2 n+1 = αn+1 s σ2n α2n

−σ2 n+1 α2 n+1

, (273)

= s σ2nα2 n+1 α2n

−σ2 n+1, (274)

= σn+1 s σ2nα2 n+1 σ2 n+1α2n

−1, (275)

= σn+1 s χ2n χ2 n+1

−1, (276)

= σn+1 r e log χ2n χ2 n+1 −1, (277)

= σn+1 q elog χ2n−log χ2 n+1 −1, (278)

= σn+1 p e−2 log γn+2 log γn+1 −1, (279)

= σn+1 p e2 log λn+1−2 log λn −1, (280)

= σn+1 p e2hλ −1. (281)

Plugging Equations (271) and (281) back into Equation (270) yields xn+1 = αn+1 αn xn −2σn+1 ehλ −1 xθ

T |χn(xn) + σn+1 p e2hλ −1ϵ, (282)

which is the SDE-DPM-Solver-1 from Lu et al. (2022a).

Corollary E.7.1 (Rex (Euler-Maruyama) is reversible stochastic DDIM for noise prediction models). The underlying scheme of Rex (Euler-Maruyama) for the noise prediction parameterization of diffusion models in Equation (158) is the stochastic DDIM solver from Song et al. (2021a) with η = σt

√ e−2hλ −1.

Proof. This follows straightforwardly from Corollary E.6.1 and Lu et al. (2022b, Equation (4.1)).

E.3. Rex as Reversible SEEDS-1

Proposition E.8 (Rex is reversible SEEDS-1). The choice of Euler or Euler-Maruyama for the underlying scheme of Rex with either the noise prediction parameterization of diffusion models in Equations (102) and (158) or data prediction in Equations (102) and (140) yields the four variants of SEEDS-1 outlined in Gonzalez et al. (2024, Equations (28-31)).

Proof. This follows straightforwardly from Propositions E.1, E.2, E.6 and E.7 by definition of SEEDS-1.

Corollary E.8.1 (Rex (Euler-Maruyama) is reversible gDDIM). The underlying scheme of Rex (Euler-Maruyama) for the data prediction parameterization of diffusion models in Equation (140) is the gDDIM solver in Zhang et al. (2023, Theorem 1) for ℓ= 1.

Proof. This follows as an immediate consequence of Proposition E.8 since by Gonzalez et al. (2024, Proposition 4.5) gDDIM is SEEDS-1.

As mentioned earlier in Appendix A.4.1 high-order variants of SEEDS use a Markov-preserving noise decomposition to approximate the iterated stochastic integrals. However, we follow Foster et al. (2024) and use the space-time Lévy area resulting in numerical schemes that are quite different beyond the first-order case, albeit that Rex exhibits better convergence properties.

<!-- Page 53 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

F. Implementation Details

F.1. Closed Form Expressions of the Noise Schedule

F.1.1. VARIANCE PRESERVING SDES

In practice, popular libraries like the diffusers library define the noise schedule for diffusion models as a discrete schedule {βn}N n=1 following Ho et al. (2020); Song et al. (2021a) as an arithmetic sequence of the form βn = β0

N + n −1 N(N −1)(β1 −β0), (283)

with hyperparameters β0, β1 ∈R≥0. Song et al. (2021b) defines the continuous-time schedule as βt = β0 + t(β1 −β0), (284)

for all t ∈[0, 1] in the limit of N →∞. Thus one can write the forward-time diffusion (variance preserving) SDE as dXt = −1

2βtXt dt + p βt dWt. (285)

Thus we can express the noise schedule (αt, σt) as αt = exp

−1

2

Z βt dt

, (286a)

σt = q

1 −α2 t. (286b)

N.B., often the hyperparmeters in libraries like diffusers are expressed as ˆβ0 = β0

N and ˆβ1 = β1

N, often with N = 1000.

Linear Noise Schedule. For the linear noise schedule in Equation (284) used by DDPMs (Ho et al., 2020), the schedule (αt, σt) is written as αt = exp

−β1 −β0

4 t2 −β0

2 t

, σt = q

1 −α2 t,

(287)

for t ∈[0, 1] with hyperparameters β0 and β1.

Proposition F.1 (Inverse function of γt for linear noise schedule). For the linear noise schedule used by DDPMs (Ho et al., 2020) the inverse function of γt denoted tγ can be expressed in closed form as tγ(γ) = −β0 + p β2

0 + 2(β1 −β0) log(γ−2 + 1) β1 −β0

. (288)

Proof. Let αt be denoted by αt = eat where at = −β1 −β0

4 t2 −β0

2 t. (289)

Then by definition of γt we can write γt = eat √

1 −e2at, (290)

<!-- Page 54 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers and with a little more algebra we find p

1 −e2at = eat γt

, (291)

1 −e2at = e2at γ2 t

, (292)

e−2at −1 = γ−2 t, (293)

e−2at = γ−2 t + 1, (294)

−2at = log(γ−2 t + 1). (295)

Then by substituting in the definition of at and letting γ denote the variable produced by γt we have β1 −β0

2 t2 + β0t −log(γ−2 + 1) = 0. (296)

We then use the quadratic formula to find the roots of the polynomial of t to find t = −β0 ± p β2

0 + 2(β1 −β0) log(γ−2 + 1) β1 −β0

. (297)

Since t ∈[0, 1] we only take the positive root and thus t = −β0 + p β2

0 + 2(β1 −β0) log(γ−2 + 1) β1 −β0

. (298)

Corollary F.1.1 (Inverse function of χt for linear noise schedule). It follows by a straightforward substitution from Proposition F.1 that tχ can be written as tχ(χ) = −β0 + p β2

0 + 2(β1 −β0) log(χ2 + 1) β1 −β0

. (299)

Corollary F.1.2 (Inverse function of ϱt for linear noise schedule). It follows by a straightforward substitution from Proposition F.1 that tϱ can be written as tϱ(ϱ) = −β0 + p β2

0 + 2(β1 −β0) log(ϱ−1 + 1) β1 −β0

. (300)

Scaled Linear Schedule. The scaled linear schedule is used widely by latent diffusion models (LDMs) (Rombach et al., 2022) and takes the discrete form of βn = q

ˆβ0 + n −1

N −1 q

ˆβ1 − q

ˆβ0

2

. (301)

Thus following a similar approach to Song et al. (2021b) we write the scaled linear schedule as a function of t, βt = (β1 −2 p β1β0 + β0)t2 + 2t( p β1β0 −β0) + β0. (302)

Then using Equation (286) we find the noise schedule (αt, σt) to be defined as αt = exp

−β1 −2√β1β0 + β0

6 t3 −

√β1β0 −β0

2 t2 −β0

2 t

, σt = q

1 −α2 t.

(303)

Next we will derive the inverse function for γt

<!-- Page 55 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Proposition F.2 (Inverse function of γt for scaled linear noise schedule). For the scaled linear noise schedule commonly used by LDMs (Rombach et al., 2022), the inverse function of γt denoted tγ can be expressed in closed form as tγ(γ) = β0 −√β1β0 −

3p 2(√β1β0 −β0)3 −3β0∆(√β1β0 −β0) −3∆2 log(γ−2 + 1) ∆, (304)

where

∆= β1 −2 p β1β0 + β0. (305)

Proof. Let αt be denoted by αt = eat where at = −β1 −2√β1β0 + β0

6 t3 −

√β1β0 −β0

2 t2 −β0

2 t. (306)

Then by definition of γt we can write γt = eat √

1 −e2at, (307)

and with a little more algebra we find p

1 −e2at = eat γt

, (308)

1 −e2at = e2at γ2 t

, (309)

e−2at −1 = γ−2 t, (310)

e−2at = γ−2 t + 1, (311)

−2at = log(γ−2 t + 1). (312)

Then by substituting in the definition of at and letting γ denote the variable produced by γt we have β1 −2√β1β0 + β0

3 t3 + ( p β1β0 −β0)t2 + β0t −log(γ−2 + 1) = 0. (313)

We then use the cubic formula (Cardano, 1545) to find the roots of the polynomial of t. The only real root is given by tγ(γ) = β0 −√β1β0 −

3p 2(√β1β0 −β0)3 −3β0∆(√β1β0 −β0) −3∆2 log(γ−2 + 1) ∆, (314)

where

∆= β1 −2 p β1β0 + β0. (315)

Corollary F.2.1 (Inverse function of χt for scaled linear noise schedule). It follows by a straightforward substitution from Proposition F.2 that tχ can be written as tχ(χ) = β0 −√β1β0 −

3p 2(√β1β0 −β0)3 −3β0∆(√β1β0 −β0) −3∆2 log(χ2 + 1) ∆, (316)

where

∆= β1 −2 p β1β0 + β0. (317)

Corollary F.2.2 (Inverse function of ϱt for scaled linear noise schedule). It follows by a straightforward substitution from Proposition F.2 that tϱ can be written as tϱ(ϱ) = β0 −√β1β0 −

3p 2(√β1β0 −β0)3 −3β0∆(√β1β0 −β0) −3∆2 log(ϱ−1 + 1) ∆, (318)

where

∆= β1 −2 p β1β0 + β0. (319)

<!-- Page 56 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

F.1.2. OT FLOW MATCHING

Within OT flow matching (Tong et al., 2024) framework these expressions become much simpler.21 Within this framework we have αt = t, (320a)

σt = 1 −t. (320b)

Consequently, we have the following simple proposition.

Proposition F.3 (Inverse function of γt in OT flow matching). Within the OT flow matching context the inverse function of γt denoted tγ can be expressed in closed form as tγ(γ) = γ 1 + γ. (321)

Proof. By definition of γt we write γt = t 1 −t, (322)

(1 −t)γt = t, (323)

γt = (1 + γt)t, (324)

t = γt 1 + γt. (325)

Corollary F.3.1 (Inverse function of χt in OT flow matching). It follows by a straightforward substitution from Proposition F.3 that tχ can be written as tχ(χ) = 1 1 + χ. (326)

F.2. Some Other Inverse Functions γ 7→σ. Additionally, we need to be able to extract the weighting terms from the time integration variable. For the ODE case we need the function σγ(γ) which describes the map γ 7→σ. By the definition of γ we have γ = α σ, (327)

γ

(i) =

√

1 −σ2 σ, (328)

σγ = p

1 −σ2, (329)

σ2γ2 = 1 −σ2, (330)

σ2γ2 = 1 −σ2, (331)

γ2 = σ−2 −1, (332)

γ2 + 1 = σ−2, (333)

σ2 = 1 γ2 + 1 (334)

σγ(γ) = 1 p γ2 + 1

, (335)

where (i) hold by σ2 = 1 −α2 for VP type diffusion SDEs.

21We will use the flow matching conventions where X1 ∼pdata.

<!-- Page 57 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers ϱ 7→σ γ. Likewise, for the SDE case we need the function which maps ϱ 7→σ γ. Recall that (note we drop the subscript t for the derivation)

ϱ = α2 σ2, (336)

thus we have ϱ

(i) = α2

1 −α2, (337)

(1 −α2)ϱ = α2, (338)

α−2 −1 = ϱ−1, (339)

α−2 = ϱ−1 + 1, (340)

α = 1 p ϱ−1 + 1

, (341)

where (i) hold by σ2 = 1 −α2 for VP type diffusion SDEs. Then we can write σ γ = σ2 α, (342)

= σ2 α α α, (343)

= σ2 α2 α, (344)

= ϱ−1α, (345)

= 1 ρ p ρ−1 + 1

. (346)

χ 7→α. Lastly, for the noise prediction models we need the map χ 7→α denoted αχ(χ). By definition of χ we have χ = σ α, (347)

χ

(i) =

√

1 −α2 α, (348)

αχ(χ)

(ii) = 1 p χ2 + 1

, (349)

where (i) hold by σ2 = 1 −α2 for VP type diffusion SDEs and (ii) holds by the derivation for σγ(γ) mutatis mutandis.

F.3. Numerical Simulation of Brownian Motion

Earlier we mentioned that for reversible methods we need to be able to compute both the same realization of the Brownian motion. Now sampling Brownian motion is quite simple—recall Lévy’s characterization of Brownian motion (Øksendal, 2003, Theorem 8.6.1)—and can be sampled by drawing independent Gaussian increments during the numerical solve of an SDE. A common choice for an adaptive solver is to use Lévy’s Brownian bridge formula (Revuz & Yor, 2013).

Definition F.1 (Lévy’s Brownian bridge). Given the standard dw-dimensional Brownian motion {Wt: t ≥0} and for any 0 ≤s < t < u, the Brownian bridge is defined as

Wt|Ws, Wu ∼N

Ws + t −s u −s(Wu −Ws), (u −t)(t −s)

u −s I

, (350)

and this quantity is conditionally independent of Wv for v < s or v > u.

Sampling the Brownian motion in reverse-time, however, is more complicated as it is only adapted to the natural filtration defined in forward time. The naïve approach to sampling Brownian motion, called the Brownian path, is to simply store the entire realization of the Brownian motion from the forward pass in memory and use Equation (350) when necessary (for adaptive step size methods). This results in a query time of O(1), but with a memory cost of O(ndw), where n is the number of samples.

<!-- Page 58 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

F.3.1. METHODS

Virtual Brownian Tree. Seminal work on neural SDEs by Li et al. (2020) introduced the Virtual Brownian Tree which extends the concept of Brownian trees introduced by Gaines & Lyons (1997). The Brownian tree recursively applies Equation (350) to sample the Brownian motion at any midpoint, constructing a tree structure; however, storing such a tree would be memory intensive. By making use of splittable pseudo-random number generators PRNGs (Salmon et al., 2011; Claessen & Pałka, 2013) which can deterministically generate two random seeds given an existing seed. Then making use of a splittable PRNG, one can evaluate the Brownian motion at any point by recursively applying the Brownian tree constructing to rebuild the tree until the recursive midpoint time tr is suitable close to the desired timestep t, i.e., |t −tr| < ϵ for some fixed error threshold ϵ > 0. This requires constant O(1) memory but takes O(log(1/ϵ)) time and is only approximate.

Brownian Interval. Closely related work by Kidger et al. (2021) introduces the Brownian Interval which offers exact sampling with O(1) query time. The primary difference between this method and Virtual Brownian Trees is that this method focuses on intervals rather than particular sample points. To elucidate, let Ws,t = Wt −Ws denote an interval of Brownian motion. Then the formula for Lévy’s Brownian bridge (350) can be rewritten in terms of Brownian intervals as

Ws,t|Ws,u ∼N t −s u −sWs,u, (u −t)(s −u)

u −s I

. (351)

Then, the method constructs a tree with stump being the global interval [0, T] and a random seed for a splittable PRNG. New leaf nodes are constructed when queries over intervals are made; this provides the advantage of the tree being querydependent, unlike the Virtual Brownian Tree which has a fixed dyadic structure. Further computational improvements are made to improve implementation with the details being found in Kidger (2022, Section 5.5.3). Beyond the numerical efficiency in computing intervals over points is that we regularly need use intervals in numeric schemes and not single sample point. Often, solvers which approximate higher-order integrals (e.g., stochastic Runge-Kutta) require samples of the Lévy area22 which would require the Brownian interval to construct.23

Updated Virtual Brownian Tree. Recent work by Jelinˇciˇc et al. (2024) improves upon the Virtual Brownian Tree (Li et al., 2020) by using an interpolation strategy between query points.24 This enables the updated algorithm to exactly match the distribution of Brownian motion and Lévy areas at all query times as long as each query time is at least ϵ apart.

F.3.2. IMPLEMENTATION

We used the Brownian interval (Kidger et al., 2021) provided by the torchsde library. In general we would recommend the virtual Brownian tree from Jelinˇciˇc et al. (2024) over the Brownian interval, an implementation of this can be found in the diffrax library. However, as our code base made extensive used of prior projects developed in pytorch and diffrax is a jax library, it made more sense to use torchsde for this project.

G. Experimental Details

We provide additional details for the empirical studies conducted in Section 4. N.B., for all experiments we used fixed random seeds between the different software components to ensure a fair comparison. For all image experiments we built our experimental code from the zituitui/BELM repository which contains the implementation of BELM (Wang et al., 2024) and reimplementations of EDICT (Wallace et al., 2023) and BDIA (Zhang et al., 2024). The rest of this section is devoted to particular experimental details.

22I.e., for a dw-dimensional Brownian motion over [s, t] the Lévy area is

2Li,j s,t:=

Z t s

W i s,udW j u −

Z t s

W j s,udW i u.

23The interested reader can find more details in James Foster’s thesis (Foster, 2020). 24This algorithm is a part of the popular Diffrax library.

<!-- Page 59 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

G.1. Unconditional Image Generation

G.1.1. DIFFUSION MODEL

We make use of a pre-trained DDPM (Ho et al., 2020) model trained on the CelebA-HQ 256 × 256 dataset (Karras et al., 2018). The linear noise schedule from (Ho et al., 2020) is given as βi =

ˆβ0 T + i −1 T(T −1)(ˆβ1 −ˆβ0). (352)

We convert this into a continuous time representation via the details in Appendix F.1 following Song et al. (2021b). For this experiment we used ˆβ0 = 0.0001 and ˆβ1 = 0.2. To ensure numerical stability due to 1 σt terms we solve the probability flow ODE in reverse-time on the time interval [ϵ, 1] with ϵ = 0.0002. This is a common choice to make in practice see Song et al. (2023).

G.1.2. METRICS

We use several metrics to assess the performance in unconditional image generation following Stein et al. (2023) by using a DINOv2 feature extractor (Oquab et al., 2023), all of which are calculated using the 10k generated samples and 30k real samples from the CelebA-HQ dataset. Throughout this section we will let {xi}n i=1 denote an empirical distribution drawn from our generated distribution Pθ and let {ˆxi}m i=1 denote an empirical distribution drawn from the data distribution Pdata.

FD. The Fréchet distance (FD) (Dowson & Landau, 1982) is measured using the sample mean and covariance of the real Pdata and generated Pθ distributions denoted

FD(Pdata∥Pθ) = ∥µdata −µθ∥2

2 + Tr

Σdata + Σθ −2(ΣdataΣθ)

1 2

, (353)

where (µ·, Σ·) denote the sample mean and covariances. This metric corresponds to the 2-Wasserstein distance between two multivariate Gaussians and is thus a valid metric between the first two moments. Heusel et al. (2017) popularized the use of this metric within the feature layer of an Inception-V3 network (Szegedy et al., 2016) to assess the fidelity of unconditional image generation, this metric is referred to as the Fréchet inception distance or FID. Recent works have challenged the use of the Inception-V3 network as the feature extractor (Stein et al., 2023; Jayasumana et al., 2024; Kynkäänniemi et al., 2023) showing that the Inception-V3 network is poorly suited for capturing a semantic view of images which correlates well to human judgment. In particular, Stein et al. (2023) shows that using DINOv2 (Oquab et al., 2023) for the feature extractor results in a metric which is significantly more aligned with human judgment.

FD∞. FD∞proposed by Chong & Forsyth (2020) is a modification of FD which aims to remove the inherent bias induced by using a finite number of empirical samples. The sample is determined by evaluating FD over 15 regular intervals over the number of total samples and fitting a linear trend to the 15 data points to infer a trend for FD as the number of empirical samples, N →∞.

Precision, Recall, Density and Coverage. The density metric (Naeem et al., 2020) is used as a proxy to measure sample fidelity and improves upon the earlier precision metric (Kynkäänniemi et al., 2019; Sajjadi et al., 2018). The metric is based upon nearest neighbours distance computed in a representation space and counts how many real-sample neighbourhood balls contain the generated sample. Likewise, to quantify sample diversity we use the coverage metric (Naeem et al., 2020) which improves upon the earlier recall metric (Kynkäänniemi et al., 2019; Sajjadi et al., 2018). The density metric is given by density(Pdata, Pθ) = 1 kn n X i=1 m X j=1

1B(ˆxj,δk(ˆxj))(xi), (354)

where 1A(·) denotes the indicator function for set A, B(x, r) constructs a Euclidean ball centered at x with radius r, and δk(ˆxj) is the distance to the k-th nearest neighbour in {ˆxi}m i=1, excluding itself. The precision metric is given by precision(Pdata, Pθ) = 1 n n X i=1

1Sm j=1 B(ˆxj,δk(ˆxj))(xi). (355)

<!-- Page 60 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Similarly, coverage is given by coverage(Pdata, Pθ) = 1 m m X j=1 max i=1,...,n 1B(ˆxj,δk(ˆxj))(xi). (356)

Likewise, the recall metric is given by recall(Pdata, Pθ) = 1 m m X j=1

1Sn i=1 B(xi,δk(xi))(ˆxj). (357)

We used k = 5 and 10k samples throughout, as standard.

On Reporting. When reporting on these metrics like in Table 5 we use bold font to denote the best performance with a 1% error range. More formally, suppose we have a series of n data points {xi}n i=1 that is totally ordered by some relation R We will denote a query point xi with bold font if the range-normalized absolute percentage error is less than ϵ > 0, i.e.,

| maxj xj −xi| maxj xj −mink xk

< ϵ. (358)

In our experiments we report ϵ = 0.01.

G.1.3. HYPERPARAMETERS

We follow the suggestion of Wallace et al. (2023) and report results with EDICT using the hyperparameter p = 0.93. For BDIA, the original paper recommends γ = 1.0 for unconditional image generation (Zhang et al., 2024, Section 6.1). However, we found γ = 0.5 to yield better performance. This corroborates with the findings of Wang et al. (2024).

G.2. Conditional Image Generation

G.2.1. DIFFUSION MODEL

We make use of Stable Diffusion v1.5 (Rombach et al., 2022), a pre-trained latent diffusion model (LDM) model. We also use the scaled linear noise schedule given as βi =



 s

ˆβ0 T + i −1 √

T(T −1)

q

ˆβ1 − q

ˆβ0





2

. (359)

We convert this into a continuous time representation via the details in Appendix F.1 following Song et al. (2021b). For this experiment we used ˆβ0 = 0.00085 and ˆβ1 = 0.012. To ensure numerical stability due to 1 σt terms, we solve the probability flow ODE in reverse-time on the time interval [ϵ, 1] with ϵ = 0.0002. This is a common choice in practice, see Song et al. (2023).

Numerical Schemes. We set the last two steps of Rex schemes to be either Euler or Euler-Maruyama for better stability near time 0.

G.2.2. METRICS

As mentioned in the main paper, we use the CLIP Score (Hessel et al., 2021) PickScore (Kirstain et al., 2023), and Image Reward metrics (Xu et al., 2023) to asses the ability of the text-to-image conditional generation task. We calculate each by comparing the sampled image and the given text prompt used to produce the image. We then report the average over the 1000 samples.

CLIP Score. The CLIP score measures the cosine similarity between the text and visual embeddings with pretrained CLIP model (Radford et al., 2021) denoted as

CLIPScore(x, c) = max

⟨EI(x), EC(c)⟩

∥EI(x)∥∥EC(c)∥, 0

, (360)

<!-- Page 61 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers where EI: Rd →V is the image embedder and EC: Rd′ →V is the caption embedder; and where x is the query image and c is the query caption. Thus this metric aims to measure how well our generated images align with their prompt. In particular, we use the ViT-L/14 backbone trained by OpenAI.

PickScore. Similar to CLIP score, PickScore finetunes a CLIP-H model on their proposed Pick-a-Pic dataset which purportedly aligns better with human preference over CLIP score.

Image Reward. Image Reward (Xu et al., 2023) is the newest of the three metrics and uses BLIP (Li et al., 2022) over CLIP as the backbone and finetunes the model using reward model training. The resulting metrics achieves state-of-the-art alignment with human preferences.

On Reporting. When reporting on these metrics like in Table 6, we use bold font to denote the best performance with a 1% error range. In our experiments we report ϵ = 0.01.

G.2.3. HYPERPARAMETERS

We follow the suggestion of Wallace et al. (2023) and report results with EDICT using the hyperparameter p = 0.93. For BDIA, the original paper recommends γ = 0.5 for text-to-image generation (Zhang et al., 2024, Section 6.1). We also ran BDIA with γ = 0.96 as suggested by Wang et al. (2024).

G.3. Image Editing

For our experiments we drew 100 text-image-instruction triples from the InstructPix2Pix dataset (Brooks et al., 2023) and report the mean of each metric over these. We use Stable Diffusion v1.5 with the same scaled-linear noise schedule and continuous-time conversion as in Appendix G.2. All fixed-step solvers use 100 inversion steps and 100 generation steps with CFG scale 3.0; Rex (Dopri5) uses the adaptive step controller of Dormand & Prince (1980) with atol = rtol = 10−5. The inversion is performed under the source caption csrc to time t = 0.6, after which generation back to t = 0 is performed under the edit caption cedit. We use the same EDICT and BDIA hyperparameters as in Appendix G.2.

G.4. Interpolation

Diffusion Model. We make use of a pre-trained DDPM (Ho et al., 2020) model trained on the CelebA-HQ 256 × 256 dataset (Karras et al., 2018). We used linear noise schedule from (Ho et al., 2020). We convert this into a continuous time representation via the details in Appendix F.1 following Song et al. (2021b). For this experiment we used ˆβ0 = 0.0001 and

ˆβ1 = 0.2. For the face pairings we followed Blasingame & Liu (2024a;c) and used the FRLL (DeBruine & Jones, 2017) dataset.

Notably, we used the noise prediction parameterization rather than data prediction as we found that it performed better for editing. This is likely due to the singularity of the 1 σt terms as t →0. Within this parameterization we could use the time interval [0, 1] instead of [ϵ, 1] like in previous experiments with data prediction models.

G.5. Boltzmann Sampling

Our codebase is built upon the transferable-samplers/transferable-samplers repository (Tan et al., 2025b) wherein we add the Rex code.

G.5.1. DATASETS

We follow the same training, validation, and test split used by Tan et al. (2025a) to evaluate Rex on equilibrium conformation sampling tasks, with a focus on tri-alanine. These datasets are obtained from implicit solvent molecular dynamics (MD) simulations. In particular, a single MCMC chain is decomposed into 105, 2 × 104, and 104 samples for training, validation, and testing. The training and validation data are each taken from contiguous regions of the chain to simulate the realistic scenario wherein a pre-existing MCMC trajectory exists and one would like to use a Boltzmann generator to continue generating samples. Earlier parts of the trajectory under-sampled specific modes enabling a biased training set which we aim to debias through access to the energy function and SNIS. All MD simulations were run for 1 µs with a time step of 1 fs at temperatures of 300K and 310K for alanine dipeptide and tri-alanine mirroring those done by Klein & Noé (2025).

<!-- Page 62 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

Tri-alanine. For the tri-alanine dataset, we follow the splitting procedure of Tan et al. (2025a). The first 100,000 datapoints after burn-in are used as the training set, the next 10,000 points in the (subsampled) chain are used for validation, and a random selection of the rest of the chain is used as test samples. This creates a biased training set relative to the test set, and is realistic in the setting where we would like to draw samples more efficiently from an existing MD chain.

G.5.2. TRAINING DETAILS

Architecture. We adopt a DiT backbone (Peebles & Xie, 2023) with the details shown below in Table 3.

**Table 3.** Overview of architecture configurations.

Parameter DiT

Hidden size 192 Blocks 6 Heads 6 Conditional dimension 64 # of Parameters (M) 3.1 M

Training Configuration. All models were trained use an exponential moving average on the weights with a decay rate of 0.999. For evaluation we generated 104 proposal samples and we used the same number of re-sampling and computing all metrics.

Hyperparameters. We used AdamW algorithm (Loshchilov & Hutter, 2017) to perform gradient descent with a learning rate of 5 × 10−4, β = (0.9, 0.999), ϵ = 10−8, and weight decay 10−4. A cosine annealing schedule was applied to the learning rate with a warm-up phase covering 5% of the training iterations. We trained for 3000 epochs.

G.5.3. METRICS

We evaluate model performance using both sample-based metrics and metrics that assess energy distributions. We enumerate these in greater detail below.

Effective Sample Size. We compute the effective sample size (ESS) using Kish’s formula (Kish, 1957), i.e., given N ∈N generated particles with unnormalized importance weights {wi}N i=1 ⊊R≥0 we have

ESS({wi}i = 1N):= 1

N

1 PN i=1 w2 i

N X i=1 wi

!2

. (361)

The ESS is a measure of how many independent and equally-weighted samples would provide equivalent statistical power to the weighted sample.

2-Wasserstein Energy Distance (E-W2). To compare energy distributions we measure the 2-Wasserstein distance between them which for two probability measures µ, ν on R over energy values is given as

E-W2(µ, ν)2 = inf γ∈Π(µ,ν)

Z

R×R

|x −y|2 dγ(x, y), (362)

where Π(µ, ν) is the set of all couplings whose marginals are µ and ν. The 2-Wasserstein distance is an integral probability metric which captures both the difference in location and shape of two distributions.

Torus 2-Wasserstein Distance (T-W2). To measure structural similarity in torsional space, we compute the 2-Wasserstein distance over dihedral angles. For a molecule with L ∈N residues, we define the dihedral vector as

Dihedrals(x) = (ϕ1, ψ1,..., ϕL−1, ψL−1) ∈[0, 2π)2(L−1). (363)

Thus given the torus geometry, a natural cost function arises as the minimal signed angle difference, i.e., cT (x, y)2 =

2 X i=1

[(Dihedrals(x)i −Dihedrals(y)i + π) mod 2π −π]2. (364)

<!-- Page 63 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 4.** Reconstruction error in pixel space and latent space (MSE) for Stable Diffusion v1.5 (512 × 512) averaged over 100 real images,

at varying number of steps and floating-point precision. A CFG scale of 1.0 was used. † denotes runs with non-deterministic GPU operations enabled. Best results in bold, second best underlined.

Precision Solver Steps = 10 Steps = 20 Steps = 50

Pixel MSE Latent MSE Pixel MSE Latent MSE Pixel MSE Latent MSE fp32

DDIM 2.81 × 10−2 3.57 × 10−1 1.05 × 10−2 9.89 × 10−2 3.36 × 10−3 1.66 × 10−2

EDICT 1.86 × 10−3 1.59 × 10−6 1.86 × 10−3 1.98 × 10−7 1.86 × 10−3 2.23 × 10−9

BDIA 1.86 × 10−3 3.26 × 10−7 1.86 × 10−3 1.29 × 10−7 1.86 × 10−3 2.34 × 10−8

O-BELM 1.86 × 10−3 1.05 × 10−7 1.86 × 10−3 2.24 × 10−7 1.86 × 10−3 3.35 × 10−7

Rex (Euler) 1.86 × 10−3 3.77 × 10−9 1.86 × 10−3 1.98 × 10−9 1.86 × 10−3 8.85 × 10−10

Rex † (Euler) 1.86 × 10−3 3.77 × 10−9 1.86 × 10−3 1.98 × 10−9 1.86 × 10−3 8.85 × 10−10 fp16

DDIM 2.82 × 10−2 3.57 × 10−1 1.05 × 10−2 9.90 × 10−2 3.36 × 10−3 1.66 × 10−2

EDICT 1.96 × 10−3 9.84 × 10−4 1.90 × 10−3 3.94 × 10−4 1.86 × 10−3 7.87 × 10−6

BDIA 1.87 × 10−3 6.62 × 10−5 1.87 × 10−3 6.80 × 10−5 1.87 × 10−3 6.80 × 10−5

O-BELM 1.86 × 10−3 9.03 × 10−6 1.87 × 10−3 8.16 × 10−5 1.93 × 10−3 9.17 × 10−4

Rex (Euler) 1.86 × 10−3 1.63 × 10−6 1.87 × 10−3 2.44 × 10−6 1.87 × 10−3 1.25 × 10−5

Thus the torus 2-Wasserstein between two distributions µ, ν on [0, 2π)2(L−1) is then

T-W2(µ, ν)2 = inf γ∈Π(µ,ν)

Z

Rd×Rd cT (x, y)2 dγ(x, y). (365)

G.6. Hardware

All experiments were run using a single NVIDIA H100 80 GB GPU.

G.7. Repositories

In our empirical studies we made use of the following resources and repositories:

1. google/ddpm-celebahq-256 (DDPM Model)

2. stable-diffusion-v1-5/stable-diffusion-v1-5 (Stable Diffusion v1.5)

3. zituitui/BELM (Implementation of BELM, EDICT, and BDIA)

4. google-research/torchsde (Brownian Interval)

5. layer6ai-labs/dgm-eval (FD, FD∞, KD, Density, and Coverage metrics)

6. torchmetrics (CLIP score)

7. zai-org/ImageReward (Image Reward)

8. yuvalkirstain/pickscore (PickScore)

9. timbrooks/instructpix2pix-clip-filtered (InstructPix2Pix dataset)

10. transferable-samplers/transferable-samplers (Boltzman sampling)

11. transferable-samplers/many-peptides-md (Tri-alanine data)

H. Additional Results

This appendix collects results that could not fit into the main paper, including full quantitative tables for the radar charts and additional qualitative samples. We first report the full reconstruction-error study referenced in Section 4.1 (Appendix H.1), followed by the complete tables for unconditional generation (Appendix H.2), conditional generation (Appendix H.3), image editing (Appendix H.4), and Boltzmann sampling (Appendix H.5). We then turn to two further analyses of Rex: a profiling of

<!-- Page 64 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 5.** Quantitative comparison of different reversible solvers for unconditional image generation with a pre-trained DDPM model on

CelebA-HQ (256 × 256) with the non-reversible DDIM as a baseline. Our reversible ODE solvers are in pink and reversible SDE solvers in mauve.

Steps Solver FD (↓) FD∞(↓) Precision (↑) Recall (↑) Density (↑) Coverage (↑)

10

EDICT 1042.89 1034.82 0.49 0.10 0.19 0.11 BDIA 900.95 894.23 0.61 0.10 0.28 0.14 O-BELM 605.52 596.47 0.78 0.18 0.56 0.34 Rex (Midpoint) 607.20 597.04 0.78 0.21 0.60 0.37 Rex (RK4) 633.90 617.11 0.81 0.22 0.64 0.36 Rex (Euler-Maruyama) 610.16 598.56 0.79 0.10 0.61 0.37

DDIM 727.75 716.41 0.75 0.14 0.49 0.27

20

EDICT 752.68 743.89 0.68 0.15 0.36 0.21 BDIA 611.47 601.37 0.76 0.19 0.50 0.30 O-BELM 489.94 477.82 0.82 0.23 0.71 0.43 Rex (Midpoint) 539.96 527.85 0.81 0.26 0.66 0.41 Rex (RK4) 547.24 533.30 0.82 0.27 0.71 0.43 Rex (Euler-Maruyama) 460.42 447.01 0.86 0.21 0.91 0.51

DDIM 570.11 555.26 0.79 0.20 0.62 0.38

50

EDICT 551.13 534.73 0.78 0.24 0.60 0.37 BDIA 500.79 489.24 0.82 0.27 0.70 0.44 O-BELM 476.29 463.07 0.84 0.29 0.77 0.45 Rex (Midpoint) 505.67 494.94 0.81 0.29 0.70 0.44 Rex (RK4) 511.17 498.94 0.80 0.27 0.69 0.44 Rex (Euler-Maruyama) 391.93 381.01 0.87 0.28 0.98 0.56

DDIM 490.88 479.87 0.80 0.26 0.67 0.45 the Brownian Interval overhead incurred by our SDE schemes (Appendix H.6) and an ablation of the three core ingredients of Rex—the reversible coupling, exponential transformation, and time reparameterization (Appendix H.7). Finally, we present qualitative material: a visualization of the inversion trajectory and the diffusion latent space (Appendix H.8), an interpolation study between real-image pairs (Appendix H.9), and a gallery of uncurated conditional generation samples (Appendix H.10).

H.1. Reconstruction Error

This section reports the full reconstruction-error results referenced from Section 4.1 in the main paper. We measure the round-trip reconstruction error (forward solve followed by reverse solve) over 100 real images encoded with Stable Diffusion v1.5 at 512 × 512 resolution, evaluating at 10, 20, 50 steps in both FP32 and FP16 with a CFG scale of 1.0. We report the mean-squared error (MSE) in both pixel space and latent space; the latter isolates errors attributable to the numerical scheme by removing the VAE reconstruction error. For fair comparison we disabled non-deterministic GPU operations across all seed-matched runs; enabling them does not meaningfully change the inversion error of Rex (cf. the Rex † row in Table 4).

**Table 4.** reports the full results. The FP32 latent-space MSEs are visualized in Figure 4 of the main paper. Rex (Euler) outperforms every baseline w.r.t. inversion error in nearly every tested setting, and often by a wide margin. In FP32, Rex achieves a latent-space MSE that is on average roughly three orders of magnitude smaller than O-BELM and eight orders of magnitude smaller than DDIM. The advantage is particularly pronounced in the few-step regime where EDICT fails (note EDICT is competitive with Rex at 50 FP32 steps, but degrades sharply at fewer steps). DDIM is not algebraically reversible, so its error simply reflects the truncation error of the underlying solver. EDICT and BDIA both improve with the number of steps but plateau in the 10−7–10−9 range due to numerical instability of the coupling. O-BELM exhibits a more striking failure mode: the error grows with the number of steps, since the iteration is nowhere linearly stable and round-off error accumulates (see Appendix A.2). Rex sits closest to the floating-point round-off floor and improves monotonically with step count.

In FP16, Rex remains the best or close-second across all step budgets, with the advantage particularly pronounced in the few-step regime where EDICT fails. Pixel-space MSEs are dominated by the VAE reconstruction error and are essentially identical across reversible solvers; we report them for completeness.

<!-- Page 65 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 6.** Quantitative comparison of different reversible solvers in terms of average CLIP score, Image Reward, and PickScore for

conditional text-to-image generation with Stable Diffusion v1.5 (512 × 512) with the non-reversible DDIM as a baseline. Our reversible ODE solvers are in pink and reversible SDE solvers in mauve.

CLIP score (↑) Image Reward (↑) PickScore (↑)

Solver / Steps 10 20 50 10 20 50 10 20 50

DDIM 31.78 31.76 31.24 0.033 0.136 0.247 21.06 21.29 21.04 EDICT 27.97 31.04 31.17 -1.219 -0.134 -0.055 19.52 20.84 21.05 BDIA γ = 0.96 31.11 31.52 31.54 -0.111 0.067 0.087 20.52 21.01 21.19 BDIA γ = 0.5 31.57 31.48 31.48 -0.006 0.055 0.066 20.98 21.16 21.21 O-BELM 31.47 31.43 31.51 0.051 0.105 0.160 20.88 21.00 21.16 Rex (Midpoint) 31.62 31.64 31.60 0.119 0.179 0.198 21.28 21.38 21.41 Rex (RK4) 31.69 31.60 31.57 0.156 0.187 0.195 21.35 21.40 21.41 Rex (Euler-Maruyama) 31.68 31.56 31.33 0.222 0.239 0.264 21.50 21.66 21.70 Rex (ShARK) 31.55 31.56 31.39 0.239 0.249 0.263 21.51 21.66 21.72

H.2. Unconditional Image Generation

In Table 5 we report the raw metric values corresponding to the radar visualization in Figure 5. Across all three step budgets we observe that Rex variants consistently match or exceed the non-reversible DDIM baseline as well as the reversible baselines (EDICT, BDIA, O-BELM). The stochastic Rex (Euler-Maruyama) scheme is particularly strong at the 20 and 50 step budgets, attaining the best FD, FD∞, Precision, Density, and Coverage at 50 steps.

A Note on Higher-Order Schemes. Comparing the entries of Table 5 one might at first be surprised to find that the higher-order Rex (RK4) performs worse than the lower-order Rex (Euler) and that the SDE variant Rex (Euler–Maruyama) outperforms both. This is consistent with prior observations within the diffusion model community: for unconditional sampling with diffusion models, higher-order ODE schemes have often been observed to be no better—and sometimes worse—than first-order schemes in low-step regimes (Lu et al., 2022b;a). In contrast, in flow matching and AI4Science settings, adaptive higher-order schemes such as Dormand–Prince do consistently outperform Euler (Tong et al., 2024; Rehman et al., 2026a; Tan et al., 2025a); we see this same effect for the Boltzmann sampling experiment in Table 1. The comparison between Rex (RK4) and Rex (Euler–Maruyama) is also less surprising than it may at first appear: the latter is an SDE scheme and benefits from a stochastic regularization effect which pulls trajectories back toward the data manifold; this can dominate any gains from higher-order discretization. We therefore emphasize that our central claim is not that higher-order schemes are universally superior, but that Rex affords arbitrary order of convergence, giving practitioners the freedom to select the order appropriate for their setting.

H.3. Conditional Image Generation

In Table 6 we report the raw CLIP, Image Reward, and PickScore values corresponding to the nine-axis radar in Figure 8. The stochastic Rex variants (Euler-Maruyama and ShARK) consistently lead the Image Reward and PickScore axes at all three step budgets, while every Rex variant stays within a tenth of a point on CLIP of the non-reversible DDIM baseline.

**Table 7.** Quantitative comparison of different reversible solvers for image editing with the non-reversible DDIM as a baseline. Our

reversible ODE solvers are in pink and adaptive ODE solvers are in teal. Best results in bold, second best under-lined.

Solver Image Reward (↑) CLIP score (↑) PickScore (↑) LPIPS (↓)

DDIM -0.564 19.17 18.367 0.214 BDIA -2.205 18.57 16.956 0.885 O-BELM -0.639 19.16 18.416 0.140 Rex (Euler) -0.551 19.17 18.721 0.109 Rex (Dopri5) -0.547 19.16 18.698 0.107

H.4. Image Editing

In Table 7 we report the raw Image Reward, CLIP score, PickScore, and LPIPS values for the round-trip image-editing experiments visualised in Figure 9. Both fixed-step Rex (Euler) and adaptive-step Rex (Dopri5) match or beat the non-

<!-- Page 66 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 8.** Profiler report of a Rex (ShARK) sampling run with 50 steps.

Section Calls Wall (s) CPU (s) Avg Wall Peak CPU MB VRAM In VRAM Out ∆VRAM model_loading 1 2.754 2.470 2.754 27.53 0.0 4096.8 +4096.8 data_loading 1 0.002 0.002 0.002 1.13 4096.8 4096.8 +0.0 rex/encode_prompt 10 0.367 0.362 0.037 0.08 4125.6 4238.7 +113.1 rex/init_noise 10 0.050 0.050 0.005 0.06 4238.7 4238.9 +0.1 rex/brownian_interval 10 0.007 0.007 0.001 0.06 4238.9 4238.9 +0.0 rex/inference 10 104.914 104.697 10.491 0.35 4238.9 4239.0 +0.1 sampling/rex 10 105.405 105.170 10.540 0.37 4125.6 4128.8 +3.2 decode_and_save 10 1.438 1.365 0.144 3.79 4128.8 4128.8 +0.0

__TOTAL__ 1 109.665 109.071 109.665 3.77 0.0 4128.8 +4128.8 reversible DDIM baseline on every metric, with LPIPS roughly halved relative to DDIM. We omit EDICT from this table because the model failed entirely on this benchmark, collapsing to the identity map.

H.5. Boltzmann Sampling

In Figure 11 we provide a qualitative comparison of the energy distributions corresponding to the quantitative results reported in Table 1. We plot the true MD energy distribution alongside the unweighted and reweighted proposal distributions obtained from the DiT model when integrated with the non-reversible Dopri5 scheme and with the reversible Rex (Dopri5) scheme. The reweighted proposals from Rex (Dopri5) more closely match the true MD energy distribution, consistent with the substantial improvement in E-W2 reported in Table 1.

(a) Dopri5 (b) Rex (Dopri5)

**Figure 11.** True MD energy distribution with unweighted and reweighted proposals created using Rex (Dopri5).

H.6. Brownian Interval Overhead

Our stochastic Rex schemes rely on Kidger’s Brownian Interval (Kidger et al., 2021) to reconstruct the realizations of the Brownian motion and the associated space-time Lévy increments without storing the entire trajectory (see Appendix F.3). Since the Foster-Reis-Strange schemes only require the space-time Lévy area—which admits an exact closed-form joint distribution with the Brownian increment (Foster et al., 2020, Remark 3.6)—we avoid the notoriously difficult space-space Lévy area entirely; for further details see Jelinˇciˇc et al. (2024, Section 3). The Brownian Interval has O(log N) query times and O(N) memory in the number of queries. For longer horizons and higher-order schemes, the queries remain exact and the convergence behavior is governed by the underlying numerical scheme rather than the Brownian sampler. We emphasize that our work is agnostic to the choice of underlying mechanism for sampling the Brownian and space-time Lévy increments; we adopt the Brownian Interval because it is lightweight and well suited to our needs.

In Table 8 we profile Rex (ShARK) with 50 solver steps. The Brownian Interval contributes essentially no meaningful overhead, accounting for a negligible fraction of the total wall-clock time and adding no measurable VRAM usage compared with the cost of the network evaluations themselves.

![Figure extracted from page 66](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-066-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 66](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-066-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 67 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Table 9.** Ablations on image editing with Stable Diffusion v1.5 (512 × 512) at varying number of steps; CFG scale of 3.0. Inversion error

is reported as MSE in the latent space. Best results in bold, second best underlined.

Steps Variant Inv. error (↓) LPIPS (↓) CLIP score (↑) ImageReward (↑) PickScore (↑)

10

Rex (Euler) baseline 1.08 × 10−6 0.0505 19.1511 −0.4351 19.0827

No rev. coupling (DDIM) 4.54 × 10−2 0.1552 19.1126 −0.6081 18.9360 No exp. transform 2.52 × 10−6 0.0309 19.1479 −0.4582 19.1999 No time reparam 1.13 × 10−8 0.0275 19.1477 −0.4746 19.2000

20

Rex (Euler) baseline 8.66 × 10−7 0.0532 19.1552 −0.4142 19.1135

No rev. coupling (DDIM) 1.68 × 10−2 0.0950 19.1289 −0.4555 19.1270 No exp. transform 2.17 × 10−6 0.0309 19.1469 −0.4600 19.1813 No time reparam 6.38 × 10−9 0.0275 19.1481 −0.4755 19.2010

50

Rex (Euler) baseline 8.65 × 10−7 0.0577 19.1487 −0.3838 19.1596

No rev. coupling (DDIM) 4.21 × 10−3 0.0664 19.1461 −0.3906 19.1761 No exp. transform 1.36 × 10−6 0.0311 19.1476 −0.4571 19.1831 No time reparam 2.69 × 10−9 0.0275 19.1482 −0.4755 19.2015

H.7. Ablation Study

We provide ablations of the three core ingredients of Rex: the reversible coupling, the exponential transformation, and the time reparameterization. We run Rex (Euler) on the image editing task with Stable Diffusion v1.5 at 512 × 512 resolution and CFG scale of 3.0, and report inversion error (latent MSE), LPIPS, CLIP score, ImageReward, and PickScore. Results are reported in Table 9.

Reversible Coupling. Removing the reversible coupling reduces Rex (Euler) to (the non-reversible) DDIM (cf. Corollary E.2.1). The inversion error increases by at least four orders of magnitude and the downstream editing quality (LPIPS, ImageReward) degrades noticeably.

Exponential Transformation. Removing the exponential transform leads to a different (non-exponential) reversible scheme. Interestingly, this variant produces slightly higher LPIPS-preservation at a small cost to edit quality (ImageReward). This is consistent with the role of the exponential treatment of the linear drift, which biases the solver towards higher-fidelity edits.

Time Reparameterization. Removing the time reparameterization yields evenly spaced steps in t rather than uniform steps in ς. This is known to influence diffusion sampling behaviour and we observe improved inversion error at slightly worse editing performance.

H.8. Visualization of Inversion and the Latent Space

We conduct a further qualitative study of the latent space produced by inversion and the impact various design parameters play. First in Figure 12 we show the process of inverting and then reconstructing a real sample. Notice that while the data prediction formulation worked great in sampling and still possesses the correct reconstruction, i.e., it is still reversible, the latent space is all messed up. The variance of (xn, ˆxn) tends to about 107, many orders of magnitude too large! We did observe that raising ζ = 1 −10−9 did help reduce this, but it was still relatively unstable. N.B., these trends hold in a large number of discretization steps (we tested up to 250); however, for visualization purposes we chose fewer steps.

Conversely, the noise prediction formulation is much more stable, see Figure 13. The variance of (xn, ˆxn) is on the right order of magnitude this time, however, there are strange artefacting and it is clear the latent variables are not normally distributed.

Moving to the SDE case with ShARK in Figure 14, we see that the data prediction formulation is so unstable in forward-time that we ran into overflow errors and can no longer achieve algebraic reversibility. However, the noise parameterization with ShARK, see Figure 15, works very well with the latent variables, appearing to be close to normally distributed.

<!-- Page 68 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 12.** Inversion followed by sampling with Rex (Euler) 5 steps, ζ = 0.999. Data prediction. Top row tracks xn, bottom row ˆxn.

**Figure 13.** Inversion followed by sampling with Rex (Euler) 5 steps, ζ = 0.999. Noise prediction. Top row tracks xn, bottom row ˆxn.

H.9. Interpolation

We explore interpolating between the inversions of two images, a difficult problem as the inverted space is often non- Gaussian (Blasingame & Liu, 2024b). We illustrate an example of this in Figure 16 exploring interpolation with an unconditional DDPM model. We observe that stochastic Rex has much better interpolation properties than both ODE inversions, corroborating with Nie et al. (2024). Both ODE variants seem to fail quite noticeably, unable to smoothly interpolate between the two samples. N.B., we noticed that the inverted samples with ShARK had variance much closer to one, whereas the other inverted samples had much larger variance, likely contributing to the distortions.

H.10. Uncurated Image Generation Samples

We present uncurated text-to-image samples produced by Rex with Stable Diffusion v1.5 (512 × 512) across several underlying solvers and discretization-step budgets. Figures 17 and 18 show samples generated by Rex (RK4) at 10 and 50 steps, respectively, and Figures 19 and 20 show samples generated by Rex (ShARK) at the same step counts.

![Figure extracted from page 68](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-068-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 68](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-068-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 69 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 14.** FAILURE CASE! Inversion followed by sampling with Rex (ShARK) 5 steps, ζ = 0.999. Data prediction. Top row tracks xn,

bottom row ˆxn.

**Figure 15.** Inversion followed by sampling with Rex (ShARK) 5 steps, ζ = 0.999. Noise prediction. Top row tracks xn, bottom row ˆxn.

**Figure 16.** Unconditional interpolation between two real images from FRLL (DeBruine & Jones, 2017) with a DDPM model trained on

CelebA-HQ. Top row is BELM, middle is Rex (Euler), and bottom is Rex (ShARK). 50 steps used for each method.

![Figure extracted from page 69](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-069-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 69](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-069-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 69](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-069-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 69](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-069-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 69](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-069-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 70 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 17.** Uncurated samples created using Rex (RK4) and Stable Diffusion v1.5 (512 × 512) and 10 discretization steps.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 70](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-070-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 71 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 18.** Uncurated samples created using Rex (RK4) and Stable Diffusion v1.5 (512 × 512) and 50 discretization steps.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 71](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-071-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 72 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 19.** Uncurated samples created using Rex (ShARK) and Stable Diffusion v1.5 (512 × 512) and 10 discretization steps.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 72](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-072-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 73 -->

Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers

**Figure 20.** Uncurated samples created using Rex (ShARK) and Stable Diffusion v1.5 (512 × 512) and 50 discretization steps.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 73](2026-ICML-rex-a-family-of-reversible-exponential-stochastic-runge-kutta-solvers/page-073-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
