---
title: "Adjoint Schrödinger Bridge Sampler"
source_url: https://neurips.cc/virtual/2025/oral/115787
paper_pdf_url: https://arxiv.org/pdf/2506.22565v2
venue: NeurIPS
year: 2025
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Adjoint Schrödinger Bridge Sampler

<!-- Page 1 -->

Adjoint Schrödinger Bridge Sampler

Guan-Horng Liu1,∗, Jaemoo Choi2,∗, Yongxin Chen2, Benjamin Kurt Miller1, Ricky T. Q. Chen1,∗

1FAIR at Meta, 2Georgia Institute of Technology ∗Core contributors

Computational methods for learning to sample from the Boltzmann distribution—where the target distribution is known only up to an unnormalized energy function—have advanced significantly recently. Due to the lack of explicit target samples, however, prior diffusion-based methods, known as diffusion samplers, often require importance-weighted estimation or complicated learning processes. Both trade off scalability with extensive evaluations of the energy and model, thereby limiting their practical usage. In this work, we propose Adjoint Schrödinger Bridge Sampler (ASBS), a new diffusion sampler that employs simple and scalable matching-based objectives yet without the need to estimate target samples during training. ASBS is grounded on a mathematical model—the Schrödinger Bridge—which enhances sampling efficiency via kinetic-optimal transportation. Through a new lens of stochastic optimal control theory, we demonstrate how SB-based diffusion samplers can be learned at scale via Adjoint Matching and prove convergence to the global solution. Notably, ASBS generalizes the recent Adjoint Sampling (Havens et al., 2025) to arbitrary source distributions by relaxing the so-called memoryless condition that largely restricts the design space. Through extensive experiments, we demonstrate the effectiveness of ASBS on sampling from classical energy functions, amortized conformer generation, and molecular Boltzmann distributions.

Date: November 26, 2025

Correspondence: ghliu@meta.com

Code: https://github.com/facebookresearch/adjoint_samplers

## Introduction

Sampling from Boltzmann distributions is a fundamental problem in computational science, with widespread applications in Bayesian inference, statistical physics, and chemistry (Box and Tiao, 2011; Binder et al., 1992; Tuckerman, 2023). Mathematically, we aim to sample from a target distribution ν(x) known up to a unnormalized, often differentiable, energy function E(x): X ⊆Rd →R, ν(x):= e−E(x)

Z, where Z:=

Z

X e−E(x)dx (1)

is an intractable normalization constant. For instance, the energy function E(x) of a molecular system quantifies the stability of a chemical structure based on the 3D positions of particles. A lower energy indicates a more stable structure and hence a higher likelihood of its occurrence, i.e., ν(x) ∝e−E(x).

Classical methods that generate samples from ν(x) rely on Markov Chain Monte Carlo algorithms, which run a Markov chain whose stationary distribution is ν(x) (Metropolis et al., 1953; Neal, 2001; Del Moral et al., 2006). These methods, however, tend to suffer from slow mixing time and require extensive evaluations of energy function, limiting their practical usages due to prohibitive complexity.

To improve sampling efficiency, modern samplers focus on learning better proposal distributions (Noé et al., 2019; Midgley et al., 2023). Among those, recent advances in diffusion-based generative models (Song et al., 2021; Ho et al., 2020) have given rise to a family of Diffusion Samplers, which consider stochastic differential equations (SDEs) of the following form:

dXt =

 ft(Xt) + σtuθ t (Xt)

 dt + σtdWt, X0 ∼µ(X0), (2)

arXiv:2506.22565v2 [stat.ML] 24 Nov 2025


<!-- Page 2 -->

**Table 1.** Compared to prior diffusion samplers, Adjoint Schrödinger Bridge Sampler (ASBS) offers the most flexible design for diffusion samplers (2), while learning the drift uθ

t via scalable matching objectives that do not rely on computation of importance weights (IWs).

Design condition for (2) Learning method for uθ t

Method Non-memoryless Arbitrary prior Matching objective1 No reliance on IWs

PIS (Zhang and Chen, 2022) DDS (Vargas et al., 2023) ✗ ✗ ✗ ✓ LV-PIS & LV-DDS (Richter and Berner, 2024) ✗ ✗ ✗ ✗ PDDS (Phillips et al., 2024) iDEM (Akhound-Sadegh et al., 2024) ✗ ✗ ✓ ✗ AS (Havens et al., 2025) ✗ ✗ ✓ ✓ Sequential SB (Bernton et al., 2019) ✓ ✓ ✗ ✗

Adjoint Schrödinger Bridge Sampler (Ours) ✓ ✓ ✓ ✓ where ft(x): [0, 1] × X →X the base drift, σt: [0, 1] →R>0 the noise schedule, and µ(x) the initial source distribution. Given (ft, σt, µ), the diffusion sampler learns a parametrized drift uθ t (x) transporting samples to the target distribution ν(x) at the terminal time t = 1.

Computational methods for learning diffusion samplers have grown significantly recently (Zhang and Chen, 2022; Vargas et al., 2023; Berner et al., 2024; Chen et al., 2025). Due to the distinct problem setup in (1), the target distribution is defined exclusively by its energy E(x), rather than by explicit target samples.

This characteristic renders modern generative modeling techniques for scalability—particularly the score matching objectives1—less applicable. As such, prior matching-based diffusion samplers (Phillips et al., 2024; Akhound-Sadegh et al., 2024; De Bortoli et al., 2024) often require computationally intensive estimation of target samples via importance weights (IWs).

Recently, Havens et al. (2025) introduced Adjoint Sampling (AS), a new class of diffusion samplers whose matching objectives rely only on on-policy samples, thereby greatly enhancing scalability. By incorporating stochastic optimal control (SOC) theory (Kappen, 2005; Todorov, 2007), AS facilitates the use of Adjoint Matching (Domingo-Enrich et al., 2025), a novel matching objective that imposes self-consistency in generated samples, effectively eliminating the needs for target samples.

The efficiency of AS, however, is achieved through a specific instantiation of the SDE (2) to satisfy the so-called memoryless condition. This condition—formally discussed in Section 2—restricts its source distribution to be Dirac delta µ(x):= δ, precluding the use of common priors such as Gaussian or domain-specific priors such as the harmonic oscillators in molecular systems (Jing et al., 2023). Notably, the memoryless condition underlies all previous matching-based diffusion samplers, restricting the design space of (2) from other choices known to enhance transportation efficiency (Shaul et al., 2023). While the condition has been relaxed in non-matching-based methods at extensive computational complexity (Richter and Berner, 2024; Bernton et al., 2019), no existing diffusion sampler—to our best understanding—has successfully combined matching objectives with non-memoryless condition. Table 1 summarizes the comparison between prior diffusion samplers.

In this work, we propose Adjoint Schrödinger Bridge Sampler (ASBS), a new adjoint-matching-based diffusion sampler that eliminates the requirement for memoryless condition entirely. Formally, ASBS recasts learning diffusion sampler as a distributionally constrained optimization, known as the Schrödinger Bridge (SB) problem (Schrödinger, 1931, 1932; Léonard, 2013; Chen et al., 2016):

min u DKL(pu||pbase) = EX∼pu

Z 1

0

1 2∥uθ t (Xt)∥2dt



, (3a)

s.t. dXt =

 ft(Xt) + σtuθ t(Xt)

 dt + σtdWt, X0 ∼µ(X0), X1 ∼ν(X1). (3b)

Here, pu denotes the path distribution induced by the SDE in (3b), whereas pbase:= pu:=0 denotes the path distribution induced by the “base” SDE when ut:= 0. By minimizing their KL divergence, the SB problem (3) seeks the kinetic-optimal drift u⋆ t —an optimality structure well correlated with sampling efficiency in

1The matching objective is a simple regression loss, E∥uθ t (Xt) −vt(Xt, X1)∥2, w.r.t. some tractable vt.


<!-- Page 3 -->

generative modeling (Finlay et al., 2020; Liu et al., 2023). Since the SOC problem in AS corresponds to a specific case of the SB problem with (ft, µ):= (0, δ), ASBS extends AS to handle non-memoryless conditions by solving more general SB problems (see Theorem 3.1). Computationally, ASBS retains all scalability advantages from AS by utilizing an adjoint-matching objective that removes the need for estimating target samples. It also introduces a corrector-matching objective to correct nontrivial biases arising from non-memoryless conditions. We prove that alternating optimization between the two matching objectives is equivalent to executing the Iterative Proportional Fitting algorithm (Kullback, 1968), ensuring global convergence of ASBS to u⋆ t (see Theorem 3.2). Though extensive experiments, we show superior performance of ASBS over prior diffusion samplers across various benchmarks on sampling multi-particle energy functions.

In summary, we present the following contributions:

• We introduce ASBS, an SB-based diffusion sampler capable of sampling target distributions using only unnormalized energy functions, by solving general SB problems with arbitrary priors.

• We base ASBS on a new SOC framework that removes the restrictive memoryless condition, develop a scalable matching-based algorithm, and prove theoretical convergence to global solution.

• We show ASBS’s superior performance over prior methods on sampling Boltzmann distributions of classical energy functions, alanine dipeptide molecule and amortized conformer generation.

2 Preliminary

We revisit the memoryless condition introduced by Domingo-Enrich et al. (2025) and examine its impact on the constructions of SOC-based diffusion samplers (Zhang and Chen, 2022; Havens et al., 2025), which are closely related to our ASBS. Additional review can be found in Section A.

Stochastic Optimal Control (SOC) The SOC problem (4) studies an optimization problem:

min u EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + g(X1)  s.t. (2), (4)

which, unlike the SB problem (3), includes an additional terminal cost g(x): X →R at the terminal time t = 1 and considers the SDE without the terminal constraint X1 ∼ν. The primary reason for studying this specific optimization problem is that the optimal distribution is known analytically by2 p⋆(X0, X1) = pbase(X0, X1)e−g(X1)+V0(X0), where V0(x) = −log

Z pbase

1|0 (y|x)e−g(y)dy (5)

is the initial value function. That is, the optimal distribution p⋆is an exponentially tilted version of the base distribution, pbase:= pu:=0. Specifically, pbase is tilted by the terminal cost “−g(X1)” and the initial value function V0(X0), which is intractable. Consequently, to ensure its marginal p⋆(X1) follows the target distribution ν(X1), we must eliminate the initial value function bias from V0(X0).

Memoryless condition & SOC-based diffusion sampler A common approach to eliminate the aforementioned initial value function bias, adopted by most diffusion samplers, is to restrict the class of base processes to be memoryless. Formally, the memoryless condition assumes statistical independency between X0 and X1 in the base distribution:

pbase(X0, X1)

memoryless:= pbase(X0)pbase(X1). (6)

This memoryless condition (6) simplifies the optimal distribution at the terminal time t = 1 and, upon choosing a proper terminal cost g(x), recovers the target distribution ν, p⋆(X1)

memoryless =

Z pbase(X0)pbase(X1)e−g(X1)+V0(X0)dX0 ∝pbase(X1)e−g(X1) = ν(X1),

2Equation (5) can be obtained by rewriting (4) as DKL(pu||pbase) + Epu 1 [g(X1)] and then computing the analytic solution p⋆(X1|X0) ∝pbase(X1|X0)e−g(X1) and normalization

R pbase(X1|X0)e−g(X1)dX1 = e−V0(X0). See Section A.1 for details.


<!-- Page 4 -->

time t

**Figure 1.** Effect of the memoryless condition on learning SOC-based diffusion samplers. We consider Gaussian prior µ(x):= N(x; 0, 1) with (ft, σt) set to VP-SDE for the first plot and (0, 0.2) for the rest; see Section A.1 for details. The memoryless condition injects significant noise (left) to correct the otherwise biased optimization (middle), whereas ASBS can successfully debias any non-memoryless processes (right).

where the last equality is due to setting the terminal cost to g(x):= log pbase

1 (x) ν(x). Typically, the memoryless condition (6) is enforced by a careful design of the base distribution pbase or, equivalently, the parameters (ft, σt, µ) in (2). For instance, the variance-preserving process (VP; Song et al., 2021) considers a linear base drift ft, a noise schedule σt that grows significantly with time, and a Gaussian prior µ; see Figure 1. Alternatively, one could implement (6) with Dirac delta prior µ(x):= δ0(x) and ft:= 0, leading to the following SOC problem (Zhang and Chen, 2022):

min u EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + log pbase 1 (X1) ν(X1)

 s.t. dXt = σtut(Xt)dt + σtdWt, X0=0. (7)

Based on the aforementioned reasoning, solving (7) results in a diffusion sampler that transports samples to the target distribution at t=1, with Adjoint Sampling (Havens et al., 2025) as the only scalable method of this class. Despite encouraging, the SOC problem in (7) is nevertheless limited by its trivial source, precluding potentially more effective options for sampling Boltzmann distributions.

3 Adjoint Schrödinger Bridge Sampler

We introduce a new diffusion sampler by solving the SB problem (3), where the target distribution ν(x) is given by its energy function E(x) rather than explicit samples. All proofs are left in Section B.

3.1 SOC Characteristics of the SB Problem

The SB problem (3)—as an optimization problem with distribution constraints—is widely explored in optimal transport, stochastic control, and recently machine learning (Léonard, 2012; Chen et al., 2021; De Bortoli et al., 2021). Its kinetic-optimal drift u⋆satisfies the following optimality equations:

u⋆ t (x) = σt∇log φt(x), where

  

  φt(x) =

Z pbase

1|t (y|x)φ1(y)dy, φ0(x) ˆφ0(x) = µ(x)

ˆφt(x) =

Z pbase t|0 (x|y) ˆφ0(y)dy, φ1(x) ˆφ1(x) = ν(x)

(8a)

(8b)

and pbase t|s (y|x):= pbase(Xt=y|Xs=x) is the transition kernel of the base process for observing y at time t given x at time s. The SB potentials φt(x), ˆφt(x) ∈C1,2([0, 1], Rd) are then defined (up to some multiplicative constant) as solutions to forward and backward time integrations w.r.t. pbase t|s.

Equation (8) are computationally challenging to solve—even when pbase t|s has an analytical solution—due to the intractable integration and coupled boundaries at t = 0 and 1. Our key observation is that the first equation (8a) resembles the optimality condition of the SOC problem (4) (see Section A.1). This implies that the optimality conditions of SB hints an SOC reinterpretation, which, as we will demonstrate, is more tractable than solving (8) directly. We formalize our finding below.


<!-- Page 5 -->

Theorem 3.1 (SOC characteristics of SB). The kinetic-optimal drift u⋆ t in (8) solves an SOC problem min u EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + log ˆφ1(X1) ν(X1)

 s.t. (2). (9)

Theorem 3.1 suggests that every SB problem (3) can be solved like an SOC problem (4) with the terminal cost g(x):= log ˆ φ1(x)

ν(x). Comparing to the formulation in Adjoint Sampling (Havens et al., 2025), the two SOC problems, namely (7) and (9), differ in their terminal costs—where pbase

1 is replaced by ˆφ1—and the relaxation of the source distribution from Dirac delta X0 = 0 to general source µ(X0).

How ˆφ1(·) debiases non-memoryless SOC problems Taking a closer look at the effect of ˆφ1, notice that the optimal distribution of the SB problem—according to Theorem 3.1 and (5)—follows p⋆(X0, X1) = pbase(X0, X1) exp



−log ˆφ1(X1)

ν(X1) −log φ0(X0)



, (10)

where “−log φ0” is the equivalent initial value function. One can verify that the marginal at the terminal time t = 1 indeed satisfies the target distribution, p⋆(X1) =

Z p⋆(X0, X1)dX0

(10) = ν(X1) ˆφ1(X1)

Z pbase(X0, X1) 1 φ0(X0)dX0

(8a) = ν(X1) ˆφ1(X1)

Z pbase(X1|X0) ˆφ0(X0)dX0

(8b) = ν(X1).

(11)

That is, the optimality equations in (8), in their essence, construct a specific function ˆφ1(·) that eliminates the initial value function bias associated with any non-memoryless processes, thereby ensuring that the optimal distribution satisfies the target ν at t = 1.

3.2 Adjoint Sampling with General Source Distribution

We now specialize Theorem 3.1 to sampling Boltzmann distributions (1), where ν(x) ∝e−E(x), and hence the terminal cost of the new SOC problem in (9) becomes log ˆ φ1(x)

ν(x) = E(x) + log ˆφ1(x). To encourage minimal transportation cost (Chen and Georgiou, 2015; Peyré and Cuturi, 2019), we consider the Brownian-motion base process with a degenerate base drift ft:= 0. Applying Adjoint Matching (AM; Domingo-Enrich et al., 2025) to the resulting SOC problem leads to u⋆= arg min u Epbase t|0,1p¯u

0,1 

∥ut(Xt) + σt (∇E + ∇log ˆφ1) (X1)∥2

, ¯u = stopgrad(u). (12)

Note that the AM objective in (12) functions as a self-consistency loss—in that both the regression and its expectation depend on the optimization variable u. This makes (12) particularly suitable for learning SB-based diffusion samplers, unlike previous matching-based SB methods (Shi et al., 2023; Liu et al., 2024), which all require ground-truth target samples from X1 ∼ν.

Computing the AM objective in (12) requires knowing ∇log ˆφ1(x), which, as we discussed in (11), serves as a corrector that debiases the optimization toward the desired target. Notably, this corrector function ∇log ˆφ1(x) also admits a variational form (Peluchetti, 2022, 2023; Shi et al., 2023):3

∇log ˆφ1 = arg min h

Epu⋆

0,1 

∥h(X1) −∇x1 log pbase(X1|X0)∥2

. (13)

To summarize, Equations (12) and (13) characterize two distinct matching objectives that any kinetic-optimal drift u⋆ t of SBs must satisfy. When the source distribution degenerates to Dirac delta X0:= 0, (13) is minimized at ∇log pbase

1, and (12) simply recovers the objective used in Adjoint Sampling (Havens et al., 2025). In other words, (12) and (13) should be understood as a generalization of Adjoint Sampling to handle arbitrary—including non-memoryless—source distributions.

3Formally, ∇log ˆφt(x) is the kinetic-optimal drift along the reversed time coordinate s:= 1 −t, and (13) is its variational formulation, i.e., the Markovian projection at s = 0; see Section A.2 for details.


<!-- Page 6 -->

Algorithm 1 Adjoint Schrödinger Bridge Sampler (ASBS)

Require: Sample-able source X0 ∼µ, differentiable energy E(x), parametrized uθ(t, x) and hϕ(x)

1: Initialize h(0) ϕ:= 0 2: for stage k in 1, 2,... do

3: Update drift u(k)

θ by solving (14) ▷adjoint matching

4: Update corrector h(k)

ϕ by solving (15) ▷corrector matching 5: end for

CM

AM

**Figure 2.** Illustration of ASBS on a 2D example. By alternatively minimizing the Adjoint Matching (AM) objective (14) and the Corrector Matching (CM) objective (15), ASBS progressively learns a better corrector h(k)

ϕ that debiases the SOC problem for the control u(k)

θ. Note that since the corrector is initialized with h(0)

ϕ:= 0, the first AM stage simply regresses u(1)

θ to the energy gradient ∇E.

3.3 Alternating Optimization with Adjoint and Corrector Matching

Building upon the theoretical characterization in Section 3.2, we aim to design a learning algorithm that finds a diffusion sampler satisfying (12) and (13), which correspond to two simple matching-based objectives. However, these matching objectives cannot be naively implemented due to their interdependency: Solving (12) for the kinetic-optimal drift u⋆requires knowing ∇log ˆφ1. Likewise, solving (13) for the corrector function ∇log ˆφ1 requires samples from u⋆. We relax the interdependency with an alternating optimization scheme. Specifically, given an approximation of ∇log ˆφ1 ≈h(k−1) from the previous stage k −1, we first update the drift u(k) with the AM objective:

u(k):= arg min u Epbase t|0,1p¯u

0,1 h

∥ut(Xt) + σt(∇E + h(k−1))(X1)∥2i

, ¯u = stopgrad(u). (14)

Then, we use the resulting drift u(k) to update h(k) by minimizing the following matching objective, which—in light of the corrector role of ∇log ˆφ1—we refer to as the Corrector Matching objective:

h(k):= arg min h

Epu(k)

0,1 

∥h(X1) −∇x1 log pbase(X1|X0)∥2

. (15)

Equation (15) should be distinguish from the bridge-matching objectives in data-driven SB methods (Shi et al., 2023; Somnath et al., 2023), where X1 must be drawn from the target distribution ν. In contrast, the matching objectives in (14) and (15) depend only on model samples at the current stage X1 ∼pu(k)

θ (X1|X0), hence can be used to learn SB-based diffusion samplers at scale.

The alternating optimization between (14) and (15) creates a sequence of updates, (u(0), h(0)) →· · · (u(k), h(k)) → · · ·, that may be thought of as running coordinate descent between the control u and the corrector h. Intuitively, at each stage k, we first find the control u(k) that best aligns with the corrector from previous stage, h(k−1), then update the corrector h(k) accordingly to reflect the “memorylessness” of the current control u(k).


<!-- Page 7 -->

We summarize our method, Adjoint Schrödinger Bridge Sampler (ASBS), in Algorithm 1, while leaving the full details with additional components, such as replay buffers, in Section C. Finally, we prove that this alternating optimization indeed converges to the kinetic-optimal drift u⋆in (8).

Theorem 3.2 (Global convergence of ASBS). Algorithm 1 converges to the Schrödinger bridge solution of (3), provided all matching stages achieve their critical points, i.e., lim k→∞u(k) = u⋆.

4 Theoretical Analysis

We provide the proof of Theorem 3.2 and highlight theoretical insights throughout. While ASBS is specialized to a degenerate base drift ft:= 0, all theoretical results here apply to general ft. To simplify notation, we omit the parameters θ, ϕ and reparametrize the corrector by h(k) = ∇log ¯h(k). All proofs are left in Section B.

Our first result presents a variational characteristic to the solution of the AM objective in (14).

Theorem 4.1 (Adjoint Matching solves a forward half bridge). Let pu(k) be the path distribution induced by the drift u(k) in (14) at stage k. Then, pu(k) solves the following variational problem:

pu(k) = arg min p



DKL(p||q

¯h(k−1)): p0 = µ

, (16)

where q¯h(k−1) is the path distribution induced by a “backward” SDE on the reversed time coordinate s:= 1 −t, defined by the corrector from the previous stage ¯h(k−1):

dYs =



−fs(Ys) + σ2 s∇log ϕs(Ys)

 ds + σsdWs, ϕs(y) =

Z pbase

1−s|0(y|z)ϕ1(z)dz, (17)

with the boundary conditions Y0 ∼ν and ϕ0(y) = ¯h(k−1)(y).

Theorem 4.1 suggests that any SOC problems with the terminal cost g(x):= log

¯h(k)(x)

ν(x) can be reinterpreted as KL minimization w.r.t. a specific backward SDE (17) that is fully characterized by ν—which serves as its source distribution—and ¯h(k)—which defines its drift through the function ϕs(y). The objective in (16) differs from the one in the original SB problem (3) by disregarding the target boundary constraint, X1 ∼ν. Consequently, (16) only solves a forward half bridge.

Next, we show that the CM objective (15) admits a similar variational form, except backward in time.

Theorem 4.2 (Corrector Matching solves a backward half bridge). Let ¯h(k) be the corrector in (15) at stage k. Then, the path distribution q¯h(k) solves the following variational problem:

q

¯h(k) = arg min q



DKL(pu(k)||q): q1 = ν

(18)

Unlike (16), the objective in (18) disregards the source boundary constraint µ instead, thereby solving a backward half bridge. Theorems 4.1 and 4.2 imply that our ASBS in Algorithm 1 implicitly employs an optimization scheme that alternates between solving forward and backward half bridges, thereby instantiating the celebrated Iterative Proportional Fitting algorithm (IPF; Fortet, 1940; Kullback, 1968). Combining with the analysis by (De Bortoli et al., 2021) leads to our final result in Theorem 3.2.

5 Related Works

Data-driven Schrödinger Bridges The SB problem has attracted notable interests in machine learning due to its connection to diffusion-based generative models (Wang et al., 2021). Earlier methods implemented classical IPF algorithms (De Bortoli et al., 2021; Vargas et al., 2021; Chen et al., 2022), with scalability later enhanced by bridge matching-based methods (Shi et al., 2023; Liu et al., 2024). Unlike ASBS, all of them


<!-- Page 8 -->

focus on generative modeling and assume access to extensive target samples during training, making them unsuitable for sampling from Boltzmann distributions.

SB-inspired Diffusion Samplers Notably, in the context of diffusion samplers, the SB formulation has been constantly emphasized as a mathematically appealing framework for both theoretical analysis and method motivation (Zhang and Chen, 2022; Vargas et al., 2024; Richter and Berner, 2024; Havens et al., 2025). None of the prior methods, however, offers general solutions to learning SB-based diffusion samplers, instead specializing to either the memoryless condition or non-matching-based objectives, which largely complicate the learning process (see Table 1). Conceptually, our ASBS stands closest to SSB (Bernton et al., 2019) by learning general SB samplers. However, the two methods differ fundamentally in scalability: SSB is a Sequential Monte Carlo-based method (Chopin, 2002) augmented with learned transition kernels using Gaussian-approximated SB potentials. As with many MCMC-augmented samplers (Gabrié et al., 2022; Matthews et al., 2022), SSB requires extensive evaluations on the energy E(x), in contrast to ASBS, which is much more energy-efficient.

Learning-augmented MCMC This class of methods can be thought of as extension of classical sampling methods—such as MCMC (Metropolis et al., 1953; HASTINGS, 1970), Sequential Monte Carlo (SMC; Del Moral et al., 2006) and Annealed Importance Sampling (AIS; Neal, 2001)—where traditional proposal distributions are replaced with modern machine learning models. For instance, Arbel et al. (2021) and Gabrié et al. (2022) use normalizing flows (Chen et al., 2018) as learned proposal distributions, whereas Matthews et al. (2022) employ stochastic normalizing flow (Wu et al., 2020). More recently, Chen et al. (2025) have explored the use of diffusion models (Song et al., 2021; Ho et al., 2020). However, training these models typically requires computing importance weights, which necessitates a large number of energy evaluations.

MCMC-augmented Diffusion Samplers Alternatively, methods of this class adopt modern generative models to sampling Boltzmann distributions and incorporate MCMC techniques to mitigate the lack of explicit target samples. For example, Phillips et al. (2024), (De Bortoli et al., 2024) and (Akhound-Sadegh et al., 2024) employ score matching objective from score-based diffusion models (Song et al., 2021; Ho et al., 2020). In contrast, Albergo and Vanden-Eijnden (2025) base their method on action matching objectives (Neklyudov et al., 2023). However, estimating target samples requires computing importance weights, which makes these methods computationally expensive in terms of energy function evaluations.

6 Experiments

Benchmarks We evaluate our ASBS on three classes of multi-particle energy functions E(x).

• Synthetic energy functions These are classical potentials based on pair-wise distances of an n-particle system, where E(x) is known analytically. Following (Akhound-Sadegh et al., 2024; Chen et al., 2025), we consider a 2D 4-particle Double-Well potential (DW-4), a 1D 5-particle Many-Well potential (MW-5), a 3D 13-particle Lennard-Jones potential (LJ-13) and a 3D 55-particle Lennard-Jones potential (LJ-55). For the ground-truth samples, we sample analytically from MW-5 and use the MCMC samples from (Klein et al., 2023) for the rest of three potentials.

• Alanine dipeptide This is a molecule consisting of 22 atoms in 3D. Specifically, we consider the alanine dipeptide in an implicit solvent and aim to sample from its Boltzmann distribution at a temperature 300K. Following prior methods (Zhang and Chen, 2022; Wu et al., 2020), we use the energy function E(x) from the OpenMM library (Eastman et al., 2017) and consider a more structural internal coordinate with the dimension d = 60. The ground-truth samples contain 107 configurations, simulated from Molecular Dynamics (Midgley et al., 2023).

• Amortized conformer generation Finally, we consider a new benchmark proposed in (Havens et al., 2025) for large-scale conformer generation. Conformers are locally stable configurations located at the local minima of the molecule’s potential energy surface (Hawkins, 2017). Sampling conformers is essentially a conditional generation task, targeting a Boltzmann distribution ν(x|g) ∝e−1 τ E(x|g) at a low temperature τ ≪1, conditioned on the molecular topology g ∈G. The training set Gtrain contains 24,477 molecular topologies from SPICE (Eastman et al., 2023), represented by the SMILES strings (Weininger, 1988), whereas the test set Gtest contains 80 topologies from SPICE and another 80 from GEOM-DRUGS (Axelrod and Gomez-Bombarelli, 2022). As with (Havens et al., 2025), we consider E(x|g) a foundation model


<!-- Page 9 -->

**Table 2.** Results on the synthetic energy functions for n-particle bodies with their corresponding dimensions d. Following (Chen et al., 2025; Havens et al., 2025), we report Sinkhorn for MW-5 and the Wasserstein-2 distances w.r.t samples,

W2, and energies, E(·)W2, for the rest. All values are averaged over three random trials. Best results are highlighted.

MW-5 (d=5) DW-4 (d = 8) LJ-13 (d = 39) LJ-55 (d = 165)

Method Sinkhorn ↓ W2 ↓ E(·) W2 ↓ W2 ↓ E(·) W2 ↓ W2 ↓ E(·) W2 ↓

PDDS (Phillips et al., 2024) — 0.92±0.08 0.58±0.25 4.66±0.87 56.01±10.80 — — SCLD (Chen et al., 2025) 0.44±0.06 1.30±0.64 0.40±0.19 2.93±0.19 27.98± 1.26 — — PIS (Zhang and Chen, 2022) 0.65±0.25 0.68±0.28 0.65±0.25 1.93±0.07 18.02± 1.12 4.79±0.45 228.70±131.27 DDS (Vargas et al., 2023) 0.63±0.24 0.92±0.11 0.90±0.37 1.99±0.13 24.61± 8.99 4.60±0.09 173.09± 18.01 LV-PIS (Richter and Berner, 2024) — 1.04±0.29 1.89±0.89 — — — — iDEM (Akhound-Sadegh et al., 2024) — 0.70±0.06 0.55±0.14 1.61±0.01 30.78±24.46 4.69±1.52 93.53± 16.31 AS (Havens et al., 2025) 0.32±0.06 0.62±0.06 0.55±0.12 1.67±0.01 2.40± 1.25 4.04±0.05 30.83± 8.19 ASBS (Ours) 0.15±0.02 0.43±0.05 0.20±0.11 1.59±0.03 1.99± 1.01 4.00±0.03 28.10± 8.15

-26 -22 -18 -14 Energy E(x)

.0

.1

.2

.3

Normalized Density

DW-4

ASBS (ours) Ground Truth

-60 -45 -30 -15 Energy E(x)

.00

.02

.04

.06

LJ-13

**Figure 3.** The energy histograms of DW-4 and LJ-13 from Table 2. ASBS generates samples whose energy profiles closely match those of the ground-truth samples.

10 3 10 2 10 1 100 101 102 103

Average NFE on Energy

100

101

102

103

Average NFE on Model

ASBS AS

PIS, DDS iDEM

Complexity per Grad. Update

**Figure 4.** Complexity w.r.t. the number of function evaluation (NFE) on LJ-13 potential.

eSEN from (Fu et al., 2025), which predicts energy with density-functional-theory accuracy at a much lower computational cost. We use CREST conformers (Pracht et al., 2024) as the ground-truth samples.

Baselinesandevaluation We compare ASBS with a wide range of diffusion samplers, including PIS (Zhang and Chen, 2022), DDS (Vargas et al., 2023), PDDS (Phillips et al., 2024), SCLD (Chen et al., 2025), LV (Richter and Berner, 2024), iDEM (Akhound-Sadegh et al., 2024) and finally Adjoint Sampling (AS; Havens et al., 2025). For the conformer generation task, we include additionally a domain-specific baseline, RDKit ETKDG (Riniker and Landrum, 2015), which relies on chemistry-based heuristics. The evaluation pipelines are consistent with prior methods, where we adopt the SCLD setup for MW-5, the PIS setup for alanine dipeptide, and the AS setup for all the rest; see Section D for details.

ASBS models For all tasks, we consider a degenerate base drift ft:= 0, as discussed in Section 3.2, and set σt a geometric noise schedule. For energy functions that directly take particle systems as inputs—such as DW, LJ, and eSEN—we parametrize the models uθ, hϕ with two Equivariant Graph Neural Networks (Satorras et al., 2021) and consider a domain-specific source distribution—the harmonic prior (Jing et al., 2023). Formally, for an n-particle system x = {xi}n i=0, the harmonic prior µharmonic(x) is a quadratic potential that can be sampled analytically from an anisotropic Gaussian:

µharmonic(x) ∝exp(−α

2 P i,j ∥xi −xj∥2). (19)

For other energy functions, we use standard fully-connected neural networks and consider Gaussian priors. All models are trained with Adam (Kingma and Ba, 2015) and, following standard practices (Havens et al., 2025; Akhound-Sadegh et al., 2024), utilize replay buffers; see Section C for details.

Results Table 2 presents the results on synthetic energy functions. Notably, ASBS consistently outperforms prior diffusion samplers across all energy functions. In Figure 3, we compare the energy histograms of DW-4 and LJ-13 potentials between the ground-truth MCMC samples and those from ASBS. It is evident that ASBS generates samples that closely resemble the target Boltzmann distribution ν(x) ∝e−E(x), resulting in energy profiles E(x) that are almost indistinguishable from the ground truth. Computationally, Figure 4


<!-- Page 10 -->

**Table 3.** Comparison between diffusion samplers on sampling the molecular Boltzmann distribution of the alanine dipeptide. We report the KL divergence DKL for the 1D marginal across five torsion angles and the Wasserstein-2 W2 on jointly (ϕ, ψ), known as Ramachandran plots (see Figure 5). Best results are highlighted.

DKL on each torsion’s marginal ↓ W2 on joint ↓

Method ϕ ψ γ1 γ2 γ3 (ϕ, ψ)

PIS (Zhang and Chen, 2022) 0.05±0.03 0.38±0.49 5.61±1.24 4.49±0.03 4.60±0.03 1.27±1.19 DDS (Vargas et al., 2023) 0.03±0.01 0.16±0.07 2.44±0.96 0.03±0.00 0.03±0.00 0.68±0.09 AS (Havens et al., 2025) 0.09±0.09 0.04±0.04 0.17±0.17 0.56±0.09 0.51±0.06 0.65±0.52

ASBS (Ours) 0.02±0.00 0.01±0.00 0.03±0.01 0.02±0.00 0.02±0.00 0.25±0.01

**Table 4.** Results on large-scale amortized conformer generation, evaluated on two test sets, SPICE and GEOM-DRUGS, both with and without post-processing relaxation. We report the coverage (%) and Absolute Mean RMSD (AMR) of the recall at the threshold 1.0Å. Note that “+RDKit warmup” refers to warm-starting the model uθ using RDKit conformers; see Section D for details. Best results without and with RDKit warm-up are highlighted separately.

without relaxation with relaxation

SPICE GEOM-DRUGS SPICE GEOM-DRUGS

Method Coverage ↑ AMR ↓ Coverage ↑ AMR ↓ Coverage ↑ AMR ↓ Coverage ↑ AMR ↓

RDKit ETKDG (Riniker and Landrum, 2015) 56.94±35.82 1.04±0.52 50.81±34.69 1.15±0.61 70.21±31.70 0.79±0.44 62.55±31.67 0.93±0.53

AS (Havens et al., 2025) 56.75±38.15 0.96±0.26 36.23±33.42 1.20±0.43 82.41±25.85 0.68±0.28 64.26±34.57 0.89±0.45

ASBS w/ Gaussian prior (Ours) 73.04±31.95 0.83±0.24 50.23±35.98 1.05±0.43 88.26±20.57 0.60±0.24 72.32±29.68 0.77±0.35

ASBS w/ harmonic prior (Ours) 74.05±31.61 0.82±0.23 53.14±35.69 1.03±0.42 88.71±18.63 0.59±0.24 72.77±29.94 0.78±0.35

AS +RDKit warmup (Havens et al., 2025) 72.21±30.22 0.84±0.24 52.19±35.20 1.02±0.34 87.84±19.20 0.60±0.23 73.88±28.63 0.76±0.34

ASBS +RDKit warmup (Ours) 77.84±28.37 0.79±0.23 57.19±35.14 0.98±0.40 88.08±18.84 0.58±0.24 73.18±30.09 0.76±0.37

**Figure 5.** Ramachandran plots for the alanine dipeptide between ground-truth and ASBS samples.

**Figure 6.** Example of ASBS generative process on amortized conformer generation. Given an unseen molecular topology g ∈Gtest from the test set—COCSc1sc2ccccc2[n+]1[O-] in this case—ASBS transports samples from the harmonic prior X0 ∼µharmonic to generate conformers X1.

shows the average number of evaluation required on the energy E(x) and the model uθ(t, x) for each gradient update. ASBS is much more efficient than most diffusion samplers, with a slight overhead compared to AS due to the additional network hϕ(x).

**Table 3.** summarizes the results for alanine dipeptide. Following standard pipeline (Zhang and Chen, 2022), we generate model samples X1 ∈R60 and extract five torsion angles—including the backbone angles ϕ, ψ and methyl rotation angles γ1, γ2, γ3—all of them exhibit multi-modal distributions. Notably, ASBS achieves lowest KL divergence to the ground-truth marginals across all five torsions. Figure 5 further compares the joint distributions of (ϕ, ψ), known as the Ramachandran plots (Spencer et al., 2019), between ground-truth and ASBS. While ASBS identifies all high-density modes in the region ϕ ∈[−π, 0], it misses few low-density modes. This mode-seeking behavior, inherit in all SOC-based diffusion samplers, could be improved with important weighting. We provide further discussions in Section D.4.

**Table 4.** presents the recall for amortized conformer generation compared to ground-truth samples. For prior diffusion samplers, we primarily compare to AS (Havens et al., 2025) due to the benchmark’s scale. Following AS, we ablate a warm-start stage using RDKit conformers, which are close but not identical to ground-truth


![Figure extracted from page 10](2025-NEURIPS-adjoint-schr-dinger-bridge-sampler/page-010-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.


<!-- Page 11 -->

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100

Coverage Recall (%)

SPICE

RDKit AS ASBS gauss ASBS harmonic

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 SPICE + relax

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 GEOM-DRUG

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 GEOM-DRUG + relax

**Figure 7.** Recall coverage curves on amortized conformer generation on the SPICE and GEOM-DRUGS test sets without RDKit warm-start. Note that Table 4 reports the recall coverages at the threshold 1.0Å.

samples, and include results with relaxation for post-generation optimization. Since AS is a specific instance of ASBS with a Dirac delta prior—as discussed in Section 3.2—any performance improvements from AS to ASBS highlight the added capability to handle arbitrary priors and, consequently, non-memoryless processes. Remarkably, without any warm-start, ASBS with the harmonic prior (19) already matches and, in many cases, surpasses the RDKit-warm-up AS. With warm-start, ASBS achieves best performance across most metrics. This highlights the significance of domain-specific priors, aiding exploration as effectively as warm-start with additional data, which may not always be available. Finally, we visualize the generation process of ASBS with harmonic prior (19) in Figure 6 and report the recall curves in Figure 7. In practice, we observe that ASBS achieves slightly better results with a harmonic prior compared to a Gaussian prior, with both significantly outperforming AS (Havens et al., 2025). See Section D.4 for further ablation studies.

7 Conclusion and Limitation

We introduced Adjoint Schrödinger Bridge Sampler (ASBS), a new diffusion sampler for Boltzmann distributions that solves general SB problems given only target energy functions. ASBS is based on a scalable matching framework, converges theoretically to the global solution, and performs superiorly across various benchmarks. Despite these encouraging results, further enhancement with importance sampling techniques is worth investigating to mitigate the mode collapse inherent in SOC-inspired diffusion samplers. Exploring its effectiveness in sampling amortized Boltzmann distributions would also be valuable.

## Acknowledgements

The authors would like to thank Aaron Havens, Juno Nam, Xiang Fu, Bing Yan, Brandon Amos, and Brian Karrer for the helpful discussions and comments.

## References

Tara Akhound-Sadegh, Jarrid Rector-Brooks, Avishek Joey Bose, Sarthak Mittal, Pablo Lemos, Cheng-Hao Liu, Marcin

Sendera, Siamak Ravanbakhsh, Gauthier Gidel, Yoshua Bengio, Nikolay Malkin, and Alexander Tong. Iterated denoising energy matching for sampling from Boltzmann densities. In International Conference on Machine Learning (ICML), 2024.

Michael S Albergo and Eric Vanden-Eijnden. NETS: A non-equilibrium transport sampler. In International Conference on Machine Learning (ICML), 2025.

Michael Arbel, Alex Matthews, and Arnaud Doucet. Annealed flow transport monte carlo. In International Conference on Machine Learning (ICML), 2021.

Simon Axelrod and Rafael Gomez-Bombarelli. GEOM: energy-annotated molecular conformations for property prediction and molecular generation. Scientific Data, 9(1):185, 2022.

Richard Bellman. The theory of dynamic programming. Technical report, Rand corp santa monica ca, 1954.


<!-- Page 12 -->

Julius Berner, Lorenz Richter, and Karen Ullrich. An optimal control perspective on diffusion-based generative modeling. Transactions on Machine Learning Research (TMLR), 2024.

Espen Bernton, Jeremy Heng, Arnaud Doucet, and Pierre E Jacob. Schrödinger bridge samplers. arXiv preprint arXiv:1912.13170, 2019.

Kurt Binder, Dieter W Heermann, and K Binder. Monte Carlo simulation in statistical physics, volume 8. Springer,

1992.

Denis Blessing, Xiaogang Jia, Johannes Esslinger, Francisco Vargas, and Gerhard Neumann. Beyond ELBOs: a large-scale evaluation of variational methods for sampling. In International Conference on Machine Learning (ICML), 2024.

George EP Box and George C Tiao. Bayesian inference in statistical analysis. John Wiley & Sons, 2011.

James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula,

Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. JAX: composable transformations of Python+NumPy programs, 2018. http://github.com/google/jax.

Junhua Chen, Lorenz Richter, Julius Berner, Denis Blessing, Gerhard Neumann, and Anima Anandkumar. Sequential controlled langevin diffusions. In International Conference on Learning Representations (ICLR), 2025.

Ricky T. Q. Chen, Yulia Rubanova, Jesse Bettencourt, and David K Duvenaud. Neural ordinary differential equations.

In Advances in Neural Information Processing Systems (NeurIPS), 2018.

Tianrong Chen, Guan-Horng Liu, and Evangelos A Theodorou. Likelihood training of Schrödinger bridge using forward-backward SDEs theory. In International Conference on Learning Representations (ICLR), 2022.

Yongxin Chen and Tryphon Georgiou. Stochastic bridges of linear systems. IEEE Transactions on Automatic Control,

61(2):526–531, 2015.

Yongxin Chen, Tryphon T Georgiou, and Michele Pavon. On the relation between optimal transport and Schrödinger bridges: A stochastic control viewpoint. Journal of Optimization Theory and Applications, 169:671–691, 2016.

Yongxin Chen, Tryphon T Georgiou, and Michele Pavon. Stochastic control liaisons: Richard sinkhorn meets gaspard monge on a schrödinger bridge. SIAM Review, 63(2):249–313, 2021.

Nicolas Chopin. A sequential particle filter method for static models. Biometrika, 89(3):539–552, 2002.

Valentin De Bortoli, James Thornton, Jeremy Heng, and Arnaud Doucet. Diffusion Schrödinger bridge with applications to score-based generative modeling. In Advances in Neural Information Processing Systems (NeurIPS), 2021.

Valentin De Bortoli, Michael Hutchinson, Peter Wirnsberger, and Arnaud Doucet. Target score matching. arXiv preprint arXiv:2402.08667, 2024.

Pierre Del Moral, Arnaud Doucet, and Ajay Jasra. Sequential monte carlo samplers. Journal of the Royal Statistical

Society Series B: Statistical Methodology, 68(3):411–436, 2006.

Carles Domingo-Enrich, Michal Drozdzal, Brian Karrer, and Ricky T. Q. Chen. Adjoint Matching: Fine-tuning flow and diffusion generative models with memoryless stochastic optimal control. In International Conference on Learning Representations (ICLR), 2025.

Peter Eastman, Jason Swails, John D Chodera, Robert T McGibbon, Yutong Zhao, Kyle A Beauchamp, Lee-Ping

Wang, Andrew C Simmonett, Matthew P Harrigan, Chaya D Stern, Rafal P. Wiewiora, Bernard R. Brooks, and Vijay S. Pande. OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLoS computational biology, 13(7):e1005659, 2017.

Peter Eastman, Pavan Kumar Behara, David L Dotson, Raimondas Galvelis, John E Herr, Josh T Horton, Yuezhi Mao,

John D Chodera, Benjamin P Pritchard, Yuanqing Wang, Gianni De Fabritiis, and Thomas E. Markland. SPICE, a dataset of drug-like molecules and peptides for training machine learning potentials. Scientific Data, 10(1):11, 2023.

Chris Finlay, Jörn-Henrik Jacobsen, Levon Nurbekyan, and Adam Oberman. How to train your neural ODE: The world of jacobian and kinetic regularization. In International Conference on Machine Learning (ICML), 2020.

Robert Fortet. Résolution d’un système d’équations de M. Schrödinger. Journal de Mathématiques Pures et Appliquées,

19(1-4):83–105, 1940.


<!-- Page 13 -->

Xiang Fu, Brandon M Wood, Luis Barroso-Luque, Daniel S Levine, Meng Gao, Misko Dzamba, and C Lawrence

Zitnick. Learning smooth and expressive interatomic potentials for physical property prediction. In International Conference on Machine Learning (ICML), 2025.

Marylou Gabrié, Grant M Rotskoff, and Eric Vanden-Eijnden. Adaptive monte carlo augmented with normalizing flows. Proceedings of the National Academy of Sciences, 119(10):e2109420119, 2022.

WK HASTINGS. Monte carlo sampling methods using markov chains and their applications. Biometrika, 57(1):

97–109, 1970.

Aaron Havens, Benjamin Kurt Miller, Bing Yan, Carles Domingo-Enrich, Anuroop Sriram, Brandon Wood, Daniel

Levine, Bin Hu, Brandon Amos, Brian Karrer, Xiang Fu, Guan-Horng Liu, and Ricky T. Q. Chen. Adjoint Sampling: Highly scalable diffusion samplers via Adjoint Matching. In International Conference on Machine Learning (ICML), 2025.

Paul CD Hawkins. Conformation generation: The state of the art. Journal of chemical information and modeling, 57

(8):1747–1756, 2017.

Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In Advances in Neural Information

Processing Systems (NeurIPS), 2020.

Kiyosi Itô. On stochastic differential equations, volume 4. American Mathematical Soc., 1951.

Bowen Jing, Ezra Erives, Peter Pao-Huang, Gabriele Corso, Bonnie Berger, and Tommi S Jaakkola. EigenFold: Gener- ative protein structure prediction with diffusion models. In International Conference on Learning Representations (ICLR), Workshop Track, 2023.

Hilbert J Kappen. Path integrals and symmetry breaking for optimal control theory. Journal of Statistical Mechanics:

Theory and Experiment, 2005(11):P11011, 2005.

Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion-based generative models. In Advances in Neural Information Processing Systems (NeurIPS), 2022.

Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In International Conference on

Learning Representations (ICLR), 2015.

Leon Klein, Andrew Foong, Tor Fjelde, Bruno Mlodozeniec, Marc Brockschmidt, Sebastian Nowozin, Frank Noé, and

Ryota Tomioka. Timewarp: Transferable acceleration of molecular dynamics by learning time-coarsened dynamics. In Advances in Neural Information Processing Systems (NeurIPS), 2023.

Jonas Köhler, Leon Klein, and Frank Noé. Equivariant Flows: Exact likelihood generative learning for symmetric densities. In International Conference on Machine Learning (ICML), 2020.

Solomon Kullback. Probability densities with given marginals. The Annals of Mathematical Statistics, 39(4):1236–1243,

1968.

Greg Landrum. Rdkit: Open-source cheminformatics. https://www.rdkit.org, 2006.

Jean-François Le Gall. Brownian motion, martingales, and stochastic calculus. Springer, 2016.

Christian Léonard. From the Schrödinger problem to the Monge–Kantorovich problem. Journal of Functional Analysis,

262(4):1879–1920, 2012.

Christian Léonard. A survey of the Schrödinger problem and some of its connections with optimal transport. Discrete and Continuous Dynamical Systems, 2013.

Christian Léonard, Sylvie Rœlly, and Jean-Claude Zambrini. Reciprocal processes. A measure-theoretical point of view. Probability Surveys, 2014.

Daniel S Levine, Muhammed Shuaibi, Evan Walter Clark Spotte-Smith, Michael G Taylor, Muhammad R Hasyim, Kyle

Michel, Ilyes Batatia, Gábor Csányi, Misko Dzamba, Peter Eastman, Nathan C. Frey, Xiang Fu, Vahe Gharakhanyan, Aditi S. Krishnapriyan, Joshua A. Rackers, Sanjeev Raja, Ammar Rizvi, Andrew S. Rosen, Zachary Ulissi, Santiago Vargas, C. Lawrence Zitnick, Samuel M. Blau, and Brandon M. Wood. The Open Molecules 2025 (OMol25) dataset, evaluations, and models. arXiv preprint arXiv:2505.08762, 2025.

Guan-Horng Liu, Arash Vahdat, De-An Huang, Evangelos A Theodorou, Weili Nie, and Anima Anandkumar. I2SB:

Image-to-Image Schrödinger bridge. In International Conference on Machine Learning (ICML), 2023.


<!-- Page 14 -->

Guan-Horng Liu, Yaron Lipman, Maximilian Nickel, Brian Karrer, Evangelos A Theodorou, and Ricky T. Q. Chen.

Generalized Schrödinger bridge matching. In International Conference on Learning Representations (ICLR), 2024.

Alex Matthews, Michael Arbel, Danilo Jimenez Rezende, and Arnaud Doucet. Continual repeated annealed flow transport monte carlo. In International Conference on Machine Learning (ICML), 2022.

Nicholas Metropolis, Arianna W Rosenbluth, Marshall N Rosenbluth, Augusta H Teller, and Edward Teller. Equation of state calculations by fast computing machines. The journal of chemical physics, 21(6):1087–1092, 1953.

Laurence Illing Midgley, Vincent Stimper, Gregor NC Simm, Bernhard Schölkopf, and José Miguel Hernández-Lobato.

Flow annealed importance sampling bootstrap. In International Conference on Learning Representations (ICLR), 2023.

Radford M Neal. Annealed importance sampling. Statistics and computing, 11:125–139, 2001.

F. Neese. The orca program system. WIRES Comput. Molec. Sci., 2(1):73–78, 2012. doi: 10.1002/wcms.81.

Kirill Neklyudov, Daniel Severo, and Alireza Makhzani. Action matching: A variational method for learning stochastic dynamics from samples. In International Conference on Machine Learning (ICML), 2023.

Edward Nelson. Dynamical theories of Brownian motion, volume 106. Princeton university press, 2020.

Frank Noé, Simon Olsson, Jonas Köhler, and Hao Wu. Boltzmann generators: Sampling equilibrium states of many-body systems with deep learning. Science, 365(6457):eaaw1147, 2019.

Bernt Øksendal. Stochastic differential equations. In Stochastic Differential Equations, pages 65–84. Springer, 2003.

Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming

Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Kopf, Edward Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. Pytorch: An imperative style, high-performance deep learning library. In Advances in Neural Information Processing Systems (NeurIPS), 2019.

Stefano Peluchetti. Non-Denoising forward-time diffusions, 2022. https://openreview.net/forum?id=oVfIKuhqfC.

Stefano Peluchetti. Diffusion bridge mixture transports, Schrödinger bridge problems and generative modeling. arXiv preprint arXiv:2304.00917, 2023.

Gabriel Peyré and Marco Cuturi. Computational optimal transport: With applications to data science. Foundations and Trends® in Machine Learning, 11(5-6):355–607, 2019.

Angus Phillips, Hai-Dang Dau, Michael John Hutchinson, Valentin De Bortoli, George Deligiannidis, and Arnaud

Doucet. Particle denoising diffusion sampler. In International Conference on Machine Learning (ICML), 2024.

Philipp Pracht, Stefan Grimme, Christoph Bannwarth, Fabian Bohle, Sebastian Ehlert, Gereon Feldmann, Johannes

Gorges, Marcel Müller, Tim Neudecker, Christoph Plett, Sebastian Spicher, Pit Steinbach, Patryk A. Wesołowski, and Felix Zeller. CREST—A program for the exploration of low-energy molecular chemical space. The Journal of Chemical Physics, 160(11), 2024.

Lorenz Richter and Julius Berner. Improved sampling via learned diffusions. In International Conference on Learning

Representations (ICLR), 2024.

Sereina Riniker and Gregory A Landrum. Better informed distance geometry: using what we know to improve conformation generation. Journal of chemical information and modeling, 55(12):2562–2574, 2015.

Simo Särkkä and Arno Solin. Applied stochastic differential equations, volume 10. Cambridge University Press, 2019.

Vıctor Garcia Satorras, Emiel Hoogeboom, and Max Welling. E(n) equivariant graph neural networks. In International

Conference on Machine Learning (ICML), 2021.

Erwin Schrödinger. Über die Umkehrung der Naturgesetze, volume IX. Sitzungsberichte der Preuss Akad. Wissen.

Phys. Math. Klasse, Sonderausgabe, 1931.

Erwin Schrödinger. Sur la théorie relativiste de l’électron et l’interprétation de la mécanique quantique. In Annales de l’institut Henri Poincaré, 1932.

Neta Shaul, Ricky T. Q. Chen, Maximilian Nickel, Matthew Le, and Yaron Lipman. On kinetic optimal probability paths for generative models. In International Conference on Machine Learning (ICML), 2023.


<!-- Page 15 -->

Yuyang Shi, Valentin De Bortoli, Andrew Campbell, and Arnaud Doucet. Diffusion Schrödinger bridge matching. In

Advances in Neural Information Processing Systems (NeurIPS), 2023.

Vignesh Ram Somnath, Matteo Pariset, Ya-Ping Hsieh, Maria Rodriguez Martinez, Andreas Krause, and Charlotte

Bunne. Aligned diffusion Schrödinger bridges. In Conference on Uncertainty in Artificial Intelligence (UAI), 2023.

Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score- based generative modeling through stochastic differential equations. In International Conference on Learning Representations (ICLR), 2021.

Ryan K Spencer, Glenn L Butterfoss, John R Edison, James R Eastwood, Stephen Whitelam, Kent Kirshenbaum, and

Ronald N Zuckermann. Stereochemistry of polypeptoid chain configurations. Biopolymers, 110(6):e23266, 2019.

Vincent Stimper, Bernhard Schölkopf, and José Miguel Hernández-Lobato. Resampling base distributions of normalizing flows. In International Conference on Artificial Intelligence and Statistics (AISTATS), 2022.

Emanuel Todorov. Linearly-solvable Markov decision problems. In Advances in Neural Information Processing Systems

(NeurIPS), 2007.

Mark E Tuckerman. Statistical mechanics: theory and molecular simulation. Oxford university press, 2023.

Francisco Vargas, Pierre Thodoroff, Neil D Lawrence, and Austen Lamacraft. Solving Schrödinger bridges via maximum likelihood. Entropy, 2021.

Francisco Vargas, Will Grathwohl, and Arnaud Doucet. Denoising diffusion samplers. In International Conference on

Learning Representations (ICLR), 2023.

Francisco Vargas, Shreyas Padhy, Denis Blessing, and Nikolas Nüsken. Transport meets variational inference: Controlled monte carlo diffusions. In International Conference on Learning Representations (ICLR), 2024.

Gefei Wang, Yuling Jiao, Qian Xu, Yang Wang, and Can Yang. Deep generative learning via Schrödinger bridge. In

International Conference on Machine Learning (ICML), 2021.

David Weininger. Smiles, a chemical language and information system. 1. introduction to methodology and encoding rules. Journal of chemical information and computer sciences, 28(1):31–36, 1988.

Hao Wu, Jonas Köhler, and Frank Noé. Stochastic normalizing flows. In Advances in Neural Information Processing

Systems (NeurIPS), 2020.

Qinsheng Zhang and Yongxin Chen. Path integral sampler: A stochastic control approach for sampling. In International

Conference on Learning Representations (ICLR), 2022.


<!-- Page 16 -->

Contents

A Additional Preliminary A.1 Stochastic Optimal Control (SOC)................................. A.2 Schrödinger Bridge (SB)....................................... 18

B Proofs 19 B.1 Preliminary and Additional Theoretical Results.......................... 19 B.2 Missing Proofs in Main Paper.................................... 20

C Practical Implementation of ASBS 22

D Experiment Details 25 D.1 Synthetic Energy Functions..................................... 25 D.2 Alanine dipeptide........................................... 27 D.3 Amortized conformer generation.................................. 28 D.4 Additional Experiments and Discussions.............................. 29

A Additional Preliminary

A.1 Stochastic Optimal Control (SOC)

In this subsection, we expand Section 2 with details. Recall the SOC problem in (4):

min u EX∼pu

Z

1 2∥ut(Xt)∥2dt + g(X1) 

(20a)

s.t. dXt = [ft(Xt) + σtut(Xt)] dt + σtdWt, X0 ∼µ. (20b)

Similar to (8), the optimal control to (20) can be characterized through an optimality equation:

u⋆ t (x) = −σt∇Vt(x), where Vt(x) = −log

Z pbase

1|t (y|x)e−V1(y)dy, V1(x) = g(x) (21)

is the value function known to satisfy the Hamilton–Jacobi–Bellman (HJB) equation (Bellman, 1954). We provide further characterization below.

Optimal distribution The optimization problem in (20) is known analytically. Specifically, notice that the entropy-regularized objective in (20) can be reformulated as:

DKL(p(X)||pbase(X)) + Ep(X) [g(X1)]

= DKL

  p(X0)||pbase(X0)



+ Ep(X0)

h

DKL

  p(X|X0)||pbase(X|X0)



+ Ep(X|X0) [g(X1)]

i

= DKL

  p(X0)||pbase(X0)



+ Ep(X0)

h

DKL

  p(X|X0)||pbase(X|X0)e−g(X1)i

(22)

where we shorthand X ≡X[0,1] and denote pbase the base distribution induced by (20b) with u:= 0, i.e., the uncontrolled distribution. Minimizing (22) w.r.t. p yields p⋆(X|X0) = 1 Z(X0)pbase(X|X0)e−g(X1), p⋆(X0) = pbase(X0) (23)

where Z(X0) is the normalization term defined by

Z(X0):=

Z pbase(X|X0)e−g(X1)dX =

Z pbase(X1|X0)e−g(X1)dX1 (24)

which is exactly e−V (X0) due to (21). Combing (23) and (24) leads to the the optimal distribution in (5), which we restate below for completeness:

p⋆(X) = pbase(X)e−g(X1)+V0(X0) =⇒p⋆(X0, X1) = pbase(X0, X1)e−g(X1)+V0(X0) (25)


<!-- Page 17 -->

Adjoint Matching (AM) Scalable computational methods for solving (20) have been challenging, as naively back-propagating through (20) induces prohibitively high computational cost. Instead, Adjoint Matching (Domingo-Enrich et al., 2025) employs a matching-based objective, named Adjoint Matching (AM):

u⋆= arg min u EX∼p¯u 

∥ut(Xt) + σtat∥2

, ¯u = stopgrad(u), (26a)

where −dat = at · ∇ft(Xt)dt, a1 = ∇g(X1) (26b)

is the backward dynamics of the (lean) adjoint state at ≡a(t; X[t,1]). It has been proven that the unique critical point of (26) is the optimal control u⋆, implying a new characteristics of the optimal control u⋆using the adjoint state:

u⋆ t (x) = −σtEp⋆[at|Xt = x]. (27)

Adjoint Sampling (AS) Recently, Havens et al. (2025) introduced an adaptation of AM tailored to sampling Boltzmann distribution ν(x) ∝e−E(x) by considering ft:= 0, µ(x):= δ0(x), g(x):= log pbase

1 (x) ν(x). (28)

That is, AS considers the following SOC problem with a degenerate base drift, a Dirac delta prior, and a specific instantiation of the terminal cost g(x):= log pbase

1 (x) ν(x):

min u EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + log pbase 1 (X1) ν(X1)

 s.t. dXt = σtut(Xt)dt + σtdWt, X0=0. (29)

Notably, this SOC problem (29) admits a simplified adjoint state at and a degenerate initial value function V0(x):

at

(26b) = ∇g(X1)

(28) = ∇log pbase

1 (X1) + ∇E(X1) ∀t ∈[0, 1] (30)

V0(x)

(28) = −log

Z pbase

1 (y) ν(y) pbase

1 (y)dy = −log 1 = 0, (31)

which further implies that the optimal distribution p⋆is a reciprocal process (Léonard et al., 2014):

p⋆(X)

(31) = pbase(X)e−V1(X1) (28) = pbase(X) ν(X1) pbase

1 (X1) = pbase(X|X1)p⋆(X1). (32)

Combining the adjoint characteristics of the optimal control (27) with the simplified adjoint state at in (30) and optimal distribution p⋆(32) motivates the following Reciprocal Adjoint Matching (RAM) objective used in AS, where the unique critical point remains to be the optimal control u⋆in (21).

u⋆= arg min u Epbase t|1 p¯u

1 

∥ut(Xt) + σt

 

∇E + ∇log pbase

1 

(X1)∥2

, ¯u = stopgrad(u). (33)

Remark on reciprocal representation The reciprocal representation of the optimal-controlled distribution p⋆in (32) extends to general SOC problems (20) with non-trivial base drifts and source distributions. Specifically, any optimal-controlled distribution that solves (20) can be factorized by p⋆(X) = pbase(X|X0, X1)p⋆(X0, X1). (34)

We leave a formal statement in Theorem B.3 and Corollary B.4.

AS with linear base drift and Gaussian prior (Figure 1) Here, we discuss an alternative instantiation of AM for sampling with linear base drift and Gaussian prior, which reproduces the leftmost plot in Figure 1. Consider ft(x):= −1

2βtx, µ(x):= N(x; 0, I), σt:= p βt, g(x):= log pbase

1 (x) ν(x). (35)


<!-- Page 18 -->

where βt is chosen such that (ft, µ, σt) fulfill the memoryless condition. For instance, Figure 1 adopts the VPSDE (Song et al., 2021) setup:

βt = (1 −t)βmax + tβmin, βmax = 20, βmin = 0.1. (36)

Similar to (30), the resulting SOC problem admits a simplified adjoint state at:

at

(26b) = κt · ∇g(X1)

(35) = κt · (∇log pbase

1 (X1) + ∇E(X1)), κt:= e−1

2 R 1 t βτ dτ (36) = e−1

4 (1−t)(βt+β1) (37)

and the RAM objective becomes u⋆= arg min u Epbase t|0,1p¯u

0,1 

∥ut(Xt) + σtκt

 

∇E + ∇log pbase

1 

(X1)∥2

, ¯u = stopgrad(u). (38)

Note that pbase t|0,1 can be sampled analytically:

pbase t|0,1(Xt|X0, X1)

(35) = N(Xt; ¯κt(1 −κ2 t) 1 −¯κ2 1 X0 + κt(1 −¯κ2 t) 1 −¯κ2 1 X1, (1 −κ2 t)(1 −¯κ2 t) 1 −¯κ2 1 I), (39)

where κt is defined in (37) and ¯κt:= e−1

2 R t

0 βτ dτ (36) = e−1

4 t(βt+β0).

A.2 Schrödinger Bridge (SB)

In this subsection, we provide additional clarification on SB and specifically the derivation of (13). Recall the optimality equations of SB in (8):

u⋆ t (x) = σt∇log φt(x), where

  

  φt(x) =

Z pbase

1|t (y|x)φ1(y)dy, φ0(x) ˆφ0(x) = µ(x)

ˆφt(x) =

Z pbase t|0 (x|y) ˆφ0(y)dy, φ1(x) ˆφ1(x) = ν(x)

(40a)

(40b)

Just like how the value function of an SOC problem fully characterizes the optimal control and its corresponding optimal distribution, so does the SB potential φt(x):

p⋆(X) = pbase(X)φ1(X1)

φ0(X0) = pbase(X|X0)φ1(X1) ˆφ0(X0), (41)

where the last equality is due to pbase(X) = pbase(X|X0)µ(X0) and then invoking (40a). Note that (41) recovers (10) by marginalizing over t ∈(0, 1). Due to the construction of φt(x) and ˆφt(x) in (40), the marginal optimal distribution admits a strikingly simple factorization:

p⋆ t (x) =

Z pbase(X, Xt = x|X0)φ1(X1) ˆφ0(X0)dX

=

Z Z pbase(X1|Xt = x)pbase(Xt = x|X0)φ1(X1) ˆφ0(X0)dX0dX1

=

Z pbase(Xt = x|X0) ˆφ0(X0)dX0

 Z pbase(X1|Xt = x)φ1(X1)dX1



= ˆφt(x)φt(x), (42)

or, more generally, p⋆ s,t(y, x) = pbase t|s (x|y) ˆφs(y)φt(x), s ≤t. (43)

Derivation of (13) We now provide a simpler derivation of (13) compared to its original derivation based on path measure theory (Shi et al., 2023):

∇log ˆφt(x)

(40b) = 1 ˆφt(x)∇x

Z pbase t|0 (x|y) ˆφ0(y)dy

= 1 ˆφt(x)

Z

∇x log pbase t|0 (x|y)pbase t|0 (x|y) ˆφ0(y)dy

=

Z

∇x log pbase t|0 (x|y)p⋆

0|t(y|x)dy, (44)


<!-- Page 19 -->

where the last equality follows by p⋆

0|t(y|x) (42) = p⋆

0,t(y, x) ˆφt(x)φt(x)

(43) = pbase t|0 (x|y) ˆφ0(y)φt(x)

ˆφt(x)φt(x) = pbase t|0 (x|y) ˆφ0(y)

ˆφt(x).

Equation (44) implies a matching-based variational formulation of ∇log ˆφt(·)—also known as the bridge matching objective in data-driven SB (Shi et al., 2023; Liu et al., 2023).

∇log ˆφt = arg min h

Ep⋆

0,t 

∥ht(Xt) −∇xt log pbase(Xt|X0)∥2

. (45)

Equation (45) recovers (13) at t = 1.

B Proofs

B.1 Preliminary and Additional Theoretical Results

Lemma B.1 (Itô lemma (Itô, 1951)). Let Xt be the solution to the Itô SDE:

dXt = ft(Xt)dt + σtdWt.

Then, the stochastic process vt(Xt), where v ∈C1,2([0, 1], Rd), is also an Itô process:

dvt(Xt) =



∂tvt(Xt) + ∇vt(Xt) · f + 1

2σ2 t ∆vt(Xt)

 dt + σt∇vt(Xt) · dWt. (46)

Lemma B.2 (Laplacian trick). For any twice-differentiable function π such that π(x)̸ = 0, it holds that

1 π(x)∆π(x) = ∥∇log π(x)∥2 + ∆log π(x) (47)

Proof.

∆π(x) = ∇· ∇π(x)

= ∇· (π(x)∇log π(x))

= ∇π(x) · ∇log π(x) + π(x)∆log π(x)

= π(x)

 

∥∇log π(x)∥2 + ∆log π(x)



Theorem B.3 (SB characteristics of SOC). The optimal distribution p⋆of the SOC problem in (20) is also the solution to the following SB problem:

arg min p



DKL(p||pbase): p0 = µ, p1 = p⋆

1

. (48)

Proof. We aim to show that there exist a transform such that the SOC’s optimality equation (21) can be reinterpreted as the ones for SB (40). To this end, consider φt(x):= e−Vt(x), ˆφt(x):= eVt(x)p⋆ t (x). (49)

One can verify that the value function Vt(x) defined in (21) can be rewritten as φt(x) =

Z pbase

1|t (y|x)φ1(y)dy.


<!-- Page 20 -->

On the other hand, we can expand ˆφt(x) by

ˆφt(x) = eVt(x)

Z p⋆(X|Xt = x)dX

= eVt(x)

Z pbase(X1|Xt = x)pbase(Xt = x, X0)e−V1(X1)+V0(X0)dX1dX0 by (25)

= eVt(x)

Z pbase(Xt = x, X0)e−Vt(x)+V0(X0)dX0 by (21)

=

Z pbase(Xt = x|X0)µ(X0)eV0(X0)dX0

=

Z pbase t|0 (x|y) ˆφ0(y)dy. by (49)

Combined, the optimality equation (21) for the SOC problem can be rewritten equivalently as u⋆ t (x) = σt∇log φt(x), where

   

   φt(x) =

Z pbase

1|t (y|x)φ1(y)dy, φ0(x) ˆφ0(x) = µ(x),

ˆφt(x) =

Z pbase t|0 (x|y) ˆφ0(y)dy, φ1(x) ˆφ1(x) = p⋆

1(x).

We conclude that p⋆indeed solves (48).

Corollary B.4 (Reciprocal process of the SOC problem). The optimal distribution p⋆of the SOC problem in (20) is a reciprocal process, i.e., p⋆(X) = pbase(X|X0, X1)p⋆(X0, X1). (51)

B.2 Missing Proofs in Main Paper

Proof of Theorem 3.1 Comparing (8a) to (21), we can reinterpret φt(x) as an value function Vt(x) by reinterpreting

Vt(x):= −log φt(x), g(x):= −log φ1(x)

(8b) = log ˆφ1(x)

ν(x).

That is, the kinetic-optimal drift of SB solves an SOC problem (4) with a terminal cost g(x):= ˆφ1(x)

ν(x). □

Proof of Theorem 4.1 For notational simplicity, we will denote q ≡q¯h(k−1) throughout the proof. We first rewrite the backward SDE (17) in the forward direction (Nelson, 2020):

dXt =

 ft −σ2 t ∇log ϕt + σ2 t ∇log qt

 dt + σtdWt, X1 ∼ν, where we rewrite ϕt(x) w.r.t. the forward time coordiante:

ϕt(x) =

Z pbase t|0 (x|y)ϕ0(y)dy, ϕ1(x) = ¯h(k−1)(x). (52)

Note that (52) admits an equivalent PDE form by invoking Feynman-Kac formula (Le Gall, 2016):

∂tϕt(x) = −∇· (ftϕt) + σ2 t 2 ∆ϕt(x), ϕ1(x) = ¯h(k−1)(x). (53)

On the other hand, the dynamics of ∂tq follows the Fokker Plank equation (Øksendal, 2003):

∂tqt = −∇·

   ft −σ2 t ∇log ϕt + σ2 t ∇log qt

 qt



+ 1

2σ2 t ∆qt

= ∇·

   σ2 t ∇log ϕt −ft

 qt



−1

2σ2 t ∆qt,


<!-- Page 21 -->

and straightforward calculation yields

∂t log qt = σ2 t ∆log ϕt −∇· ft +

  σ2 t ∇log ϕt −ft



· ∇log qt −1 2σ2 t ∥∇log qt∥2 −1

2σ2 t ∆log qt, (54)

where we apply the Laplacian trick (47) to 1 q∆q = ∥∇log qt∥2 + ∆log qt.

Now, recall that p is the path distribution induced by the following SDE:

dXt = [ft(Xt) + σtut(Xt)] dt + σtdWt, X0 ∼µ. (55)

Invoke Ito Lemma (46) to log qt(Xt), where Xt follows (55):

d log qt =



∂tlog qt + ∇log qt · (ft + σtut) + 1

2σ2 t ∆log qt

 dt + σt∇log qt · dWt

(54) =

 σ2 t ∆log ϕt −∇· ft + σ2 t ∇log ϕt · ∇log qt −1

2σ2 t ∥∇log qt∥2 + ∇log qt · (σtut)

 dt

+ σt∇log qt · dWt (56)

Likewise, invoke Ito Lemma (46) to log ϕt(Xt), where Xt follows (55):

d log ϕt

=



∂tlog ϕt + ∇log ϕt · (ft + σtut) + 1

2σ2 t ∆log ϕt

 dt + σt∇log ϕt · dWt

(53) =



−∇· ft + σ2 t 2 ∆ϕt ϕt

+ ∇log ϕt · (σtut) + 1

2σ2 t ∆log ϕt

 dt + σt∇log ϕt · dWt

(47) =



−∇·ft + σ2 t 2  

∥∇log ϕt∥2 + ∆log ϕt



+ ∇log ϕt·(σtut) + 1

2σ2 t ∆log ϕt

 dt + σt∇log ϕt·dWt

=



−∇· ft + σ2 t 2 ∥∇log ϕt∥2 + ∇log ϕt · (σtut) + σ2 t ∆log ϕt

 dt + σt∇log ϕt · dWt (57)

Subtracting (57) from (56) leads to d log ϕt −d log qt =

 1

2∥ut + σt∇log ϕt −σt∇log qt∥2 −1 2∥ut∥2 dt + σt∇log ϕt qt

· dWt. (58)

Finally, we are ready to compute the variational objective in (16):

DKL(p||q

¯h(k−1)) = EX∼pu

Z 1

0

1 2∥ut(Xt) + σt∇log ϕt(Xt) −σt∇log qt(Xt)∥2dt 

(58) = EX∼pu

Z 1

0

  1

2∥ut(Xt)∥2 + d log ϕt(Xt) −d log qt(Xt)  dt



=EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + log ϕ1(X1) q1(X1) −log ϕ0(X0)

q0(X0)



(59)

∝EX∼pu

Z 1

0

1 2∥ut(Xt)∥2dt + log ¯h(k−1)(X1)

ν(X1)



. (60)

That is, we have shown that the variational objective DKL(p||q¯h(k−1)) is equivalent (up to an additive constant) to an SOC problem (60). Applying Reciprocal Adjoint Matching (Havens et al., 2025) with the reciprocal process from Corollary B.4 conclude that DKL(p||q¯h(k−1)) is minimized by pu(k). □

Proof of Theorem 4.2 For notational simplicity, we will denote p(k) ≡pu(k) throughout the proof. Let q be the path distribution induced by a backward SDE, propagating along the time coordinate s:= 1 −t:

dYs = [−fs(Ys) + σsvs(Ys)] ds + σsdWs, Y0 ∼ν.


<!-- Page 22 -->

Next, rewrite the forward SDE p(k) in the backward direction:

dYs = h

−fs −σsu(k)

s + σ2 s∇log p(k)

s i ds + σsdWs, Y0 ∼p(k)

t |t=1.

By Theorem B.3, we know that p(k) is the SB solution, thereby satisfying u(k)

t (x) = σt∇log φt(x), where

   

   φt(x) =

Z pbase

1|t (y|x)φ1(y)dy, φ0(x) ˆφ0(x) = µ(x)

ˆφt(x) =

Z pbase t|0 (x|y) ˆφ0(y)dy, φ1(x) ˆφ1(x) = p(k)

1 (x)

(61a)

(61b)

Since we are working with the backward time coordinate s, it is convenience to define ϕs:= ˆφ1−t and rewrite (61b) by ϕs(y) =

Z pbase

1−s|0(y|z)ϕ1(z)dz, ϕ0(y) = p(k)

1 (y) φ1(y). (62)

Now, expanding the variational objective with Girsanov Theorem yields (Särkkä and Solin, 2019)

DKL(p(k)||q) = EY ∼p(k)

Z 1

0

1 2∥−σs∇log φs(Ys) + σs∇log p(k) s (Ys) −vs(Ys)∥2ds



, (63)

which is minimized point-wise at v⋆ s(y) = σs∇log p(k)

s (y) φs(y)

(42) = σs∇log ˆφs(y).

In other words, the backward SDE that minimizes (63) must obey dYs =



−fs(Ys) + σ2 s∇log ϕs(Ys)

 ds + σsdWs, Y0 ∼ν, with ϕs defined in (62). That is, we have concluded so far that q p(k)

1 /φ1 = arg min q



DKL(p(k)||q): q1 = ν

. (64)

Hence, it remains to be shown that the minimizer ¯h(k)

1 of the CM objective at stage k equals p(k)

1 φ1. This is indeed the case since p(k) is the SB solution:

∇log ¯h(k) (15):= arg min h

Ep(k)

0,1 

∥h(X1) −∇x1 log pbase(X1|X0)∥2 (45) = ∇log ˆφ1

(42) = ∇log p(k)

1 φ1

.

□

C Practical Implementation of ASBS

Algorithm 2 summarizes the practical implementation of ASBS, where we expand the adjoint and corrector matching steps (i.e., lines 3 and 4 in Algorithm 1) to full details. Table 5 provides the hyper-parameters for each task. We break down each component as follows:

Harmonic prior µharmonic Recall the harmonic prior in (19):

µharmonic(x) ∝exp(−1

2 P i,j ∥xi −xj∥2). (65)

In practice, we set α = 1 and implement (65) as an anisotropic Gaussian. For instance, for a 2-particle system in 3D, i.e., x = [x1; x2] ∈R6, we can rewrite (65) as a quadratic potential, exp(−1

2∥x1 −x2∥2) = exp(x⊤Rx), where R =





1 0 0 −1

2 0 0 0 1 0 0 −1

2 0 0 0 1 0 0 −1

2 −1

2 0 0 1 0 0 0 −1

2 0 0 1 0 0 0 −1

2 0 0 1





, (66)


<!-- Page 23 -->

Algorithm 2 Adjoint Schrödinger Bridge Sampler (ASBS)

Require: Sample-able source X0 ∼µ, differentiable energy E(x), parametrized drift uθ(t, x) and corrector hϕ(x), replay buffers Badj and Bcrt, number of stages K, numbers of AM and CM epochs Madj and Mcrt, number of resamples N, number of gradient steps L, time scaling λt, maximum energy gradient norm αmax. 1: Initialize h(0) ϕ:= 0 ▷IPF initialization

2: for stage k in 1, 2,..., K do

3: for epoch in 1, 2,..., Madj do ▷adjoint matching

4: Sample from model {(X(i)

0, X(i) 1)}N i=1 ∼p¯u(k), where ¯u(k) = stopgrad(u(k)

θ)

5: Compute adjoint target a(i)

t:= stopgrad

 clip

 

∇E(X(i)

1), αmax 

+ h(k)

ϕ (X(i)

1) 

6: Update replay buffer Badj ←Badj ∪{(X(i)

0, X(i) 1, a(i) t)}N i=1

7: Take L gradient steps ∇θLAM w.r.t. the AM objective:

LAM(θ):= Et∼U[0,1],(X0,X1,at)∼Badj,Xt∼pbase(·|X0,X1)

h λt∥u(k)

θ (t, Xt) + σtat∥2i

8: end for

9: for epoch in 1, 2,..., Mcrt do ▷corrector matching

10: Sample from model {(X(i)

0, X(i) 1)}N i=1 ∼p¯u(k), where ¯u(k) = stopgrad(u(k)

θ)

11: Update replay buffer Bcrt ←Bcrt ∪{(X(i)

0, X(i) 1)}N i=1

12: Take L gradient steps ∇ϕLCM w.r.t. the CM objective:

LCM(ϕ):= E(X0,X1)∼Bcrt h

∥h(k)

ϕ (X1) −∇x1 log pbase(X1|X0)∥2i

13: end for 14: end for 15: return Kinetic-optimal drift u⋆≈uθ(t, x)

and then sample x from the Gaussian N(x; 0, (R + ϵI)−1), where we set ϵ = 10−4.

Noise schedule σt We consider two types of noise schedule.

• The geometric noise schedule (Song et al., 2021; Karras et al., 2022) monotonically decays from t = 0 to 1 according to some prescribed βmin and βmax:

σt geometric:= βmin

 βmax βmin

1−t q

2 log βmax βmin. (67)

It is convenience to further define κt|s:=

Z t s σ2 τdτ geometric = β2 max ·

 βmin βmax

2s

−

 βmin βmax

2t

, ¯β2:= β2 max −β2 min, γt:= κt|0

¯β2. (68)

With them, the conditional base distribution when f:= 0 can be represented compactly by pbase(Xt|X0) = N(Xt; X0, κt|0I) (69a)

pbase(Xt|X0, X1) = N(Xt; (1 −γt)X0 + γtX1, ¯β2γt(1 −γt)I) (69b)

• The constant noise schedule simply sets σt constant:= σ. (70)

When f:= 0, the base SDE is effectively a standard Brownian motion whose conditional distributions obey pbase(Xt|X0) = N(Xt; X0, σ2tI) (71a)

pbase(Xt|X0, X1) = N(Xt; (1 −t)X0 + tX1, σ2t(1 −t)I) (71b)


<!-- Page 24 -->

Replay buffers Badj and Bcrt Similar to many previous diffusion samplers (Havens et al., 2025; Akhound- Sadegh et al., 2024; Chen et al., 2025), we employ replay buffers B in computation of both adjoint (14) and corrector (15) matching objectives. Specifically, we rebase the expectation over model samples pu(k) onto a replay buffer B, which stores the most latest |B| samples. We update the buffer with N new samples every L gradient steps. Note that the use of replay buffers effectively render ASBS a hybrid method between on-policy and off-policy.

Parametrization of uθ and hϕ For each energy function, we parametrize the drift uθ(t, x) and the corrector hϕ(x) with two neural networks, vθ(t, x) and vϕ(t, x), of the same architecture.

Specifically, we parametrize the drift as uθ(t, x):= σtvθ(t, x), which effectively eliminates the noise schedule “σt” in matching target (see (14)), making it time-invariant for each sampled trajectory. The only exception is the conformer generation task, where we keep the original parametrization uθ(t, x):= vθ(t, x), which empirically yields better results. On the other hand, since hϕ(x) is independent of time, we simply set a fixed time input t = 1, i.e., hϕ(x):= vϕ(1, x).

The specific parametrization v(t, x) employed for each task are detailed below.

• MW-5: We consider v(t, x) a standard fully-connected network with 4 layers with 64 hidden features of the following form:

output = layer_n ◦· · · ◦layer_1 ◦(x_embed(x) + t_embed(t))

• DW-4, LJ-13, LJ-55: We consider v(t, x) a Equivariant Graph Neural Network (EGNN; Satorras et al., 2021) with 5 layers and 128 hidden features. The architecture of EGNN is aligned with prior methods (Akhound-Sadegh et al., 2024; Havens et al., 2025).

• Alanine dipeptide: We use the same architecture as in MW-5, except with 8 layers with 256 hidden features.

• Conformer generation: We consider v(t, x) a similar EGNN used in Adjoint Sampling (Havens et al., 2025), except with 20 layers. Ablation study on the same EGNN architecture can be found in Section D.4.

Clipping αmax We clip the energy gradient to prevent its maximum norm from exceeding αmax.

Time scaling λt Following standard practices for AM objective, we employ a time scaling λt to improve numerical stability. Note that this does not affect the minimizer of the AM objective. We set λt:= 1 σ2 t for all tasks.

Translation invariance For DW-4, LJ-13, LJ-55, and conformer generation tasks, we follow prior methods (Akhound-Sadegh et al., 2024; Havens et al., 2025) by restricting the state space to a zero center-of-mass (ZCOM) subspace and thereby enforcing translation invariance.

For a n-particle k-dimensional system, i.e., x = [x1; · · ·; xn] where xi ∈Rk, the ZCOM subspace is defined as X ZCOM = {x ∈Rnk: Pn i=1 xi = 0}. Practically, this is achieved by projecting the initial sample X0 ∼µ, the SDE’s noise dWt, and the energy gradient ∇E(·) onto X ZCOM. Note that the output of EGNN is by construction ZCOM.

Formally, the adaption is equivalent to augmenting the SDE with a projection matrix A ∈Rnk×nk:

dXt = σtAut(Xt)dt + σtAdWt, X0 = AY0, Y0 ∼µ, A =



In −1 n1n1⊤ n



⊗Ik, (72)

where ⊗is the Kronecker product, In ∈Rn×n is an identity matrix, and 1n ∈Rn is a vector of ones.

Initialization and alternate procedure As ASBS is an instantiation of the IPF algorithm (see Theorem 3.2), it must adhere to the IPF initialization protocol to ensure theoretical convergence to the global solution. Specifically, the IPF initialization can be implemented in two ways

• Initialize with h(0) ϕ:= 0 and run AM, CM,... until convergence. We adopt this setup for all tasks.


<!-- Page 25 -->

• Initialize with u(0) θ:= 0 and run CM, AM,... until convergence. Since pu(0) = pbase in this setup, the optimal corrector at the first CM stage is known analytically:

h(1)(x)

(15) =

Z pbase

0|1 (y|x)∇x log pbase 1|0 (x|y)dy

=

Z pbase

0|1 (y|x) pbase

1|0 (x|y)∇xpbase 1|0 (x|y)dy

= 1 pbase

1 (x)∇x

Z pbase

0 (y)pbase

1|0 (x|y)dy

=∇log pbase

1 (x) (73)

In practice, we find that the two setups yield similar performance.

RDKit warm-start This warm-starts the drift uθ using RDKit samples. The procedure is inspired by the fact that (Shi et al., 2023; Liu et al., 2023):

u⋆ t = σt∇log φt

= arg min ut

Ep⋆ t,1



∥ut(Xt) −σt∇xt log pbase(X1|Xt)∥2

= arg min ut

E(X0,X1)∼p⋆

0,1,Xt∼pbase(·|X0,X1) 

∥ut(Xt) −σt∇xt log pbase(X1|Xt)∥2

. (74)

where the last equality is due to p⋆

0,t,1(x, y, z) (41) = pbase t,1|0(y, z|x) ˆφ0(x)φ1(z)

=pbase t|0,1(y|x, z)pbase

1|t (z|y) ˆφ0(x)φ1(z) by Markov property

(43) = pbase t|0,1(y|x, z)p⋆

0,1(x, z). (75)

Equation (74) can be understood as an analogy of (45) for another SB potential φt. In practice, given RDKit samples X1 ∼qRDKit, we warm-start ASBS by minimizing w.r.t. the following objective:

Lwarmup(θ) =Et∼U[0,1],X0∼µ,X1∼qRDKit,Xt∼pbase(·|X0,X1)

h

˜λt∥ut(Xt) −σt∇xt log pbase(X1|Xt)∥2i

(69a) = Et∼U[0,1],X0∼µ,X1∼qRDKit,Xt∼pbase(·|X0,X1)



˜λt∥ut(Xt) −σt κ1|t

(X1 −Xt)∥2



, (76)

where κ1|t is defined in (68) for the geometric noise schedule. We set the time scaling ˜λt:= q σt κ1|t. Note that, unlike AS, the minimizer of (76) does not equal u⋆, since (X0, X1) ∼µ ⊗qRDKit̸ = p⋆

0,1 are sampled independently.

D Experiment Details

D.1 Synthetic Energy Functions

D.1.1 Energy functions

In this section, we provide the exact setup for our synthetic energy experiments in Table 2. We consider four synthetic energy functions that have been widely used in recent literature to benchmark sampling and generative algorithms: MW-5, DW-4, LJ-13, and LJ-55.

MW-5 The MW-5 (Many-Well in 5D) energy is a 5-particle 1D system adopted from Chen et al. (2025), where x = [x1; · · ·; x5] ∈R5 with xi ∈R,. The energy function is defined as follows:

E(x) =

5 X i=1

(x2 i −δ)2 (77)


<!-- Page 26 -->

**Table 5.** Hyperparameters of ASBS for the each task.

Synthetic energy functions Alanine dipeptide

Conformer generation MW-5 DW-4 LJ-13 LJ-55 µ N(0, 1) µharmonic in (19) with α=2, 2, 1 N(0, 0.25) µharmonic βmin — 0.001 0.001 0.001 0.001 0.001 βmax — 1 1 2 0.5 1 σ 0.2 — — — — — K 5 20 15 15 15 3 Madj 100 200 300 300 Mcrt 20 20 20 20 N 128 L 200 100 100 100 100 100 |B| 104 104 104 104 104 6.4 × 104 αmax — 100 100 100 100 150 λt 1 σ2 t

1 σ2 t

1 σ2 t

1 σ2 t

1 σ2 t

1 σ2 t where we set δ = 4. This creates distinct modes centered at combinations of ±

√ δ in each of the d dimensions.

DW-4 The DW-4 (Double-Well for 4 particles in 2D) energy is a physically motivated pairwise potential originally proposed in Köhler et al. (2020) and subsequently used in Akhound-Sadegh et al. (2024); Havens et al. (2025). It defines a system of four particles, each living in R2, leading to an 8D state vector x = [x1; x2; x3; x4] ∈R8 with xi ∈R2. The energy function reads

E(x) = exp



1

2τ

X i<j

  a(dij −d0) + b(dij −d0)2 + c(dij −d0)4



, (78)

where dij = ∥xi−xj∥2 is the Euclidean distance between particles i and j. We follow the standard configuration with a = 0, b = −4, c = 0.9, d0 = 1, and temperature τ = 1.

LJ-13 and LJ-55 The Lennard-Jones (LJ) potentials are classical intermolecular potentials commonly used in physics to model atomic interactions. These are defined for a system of n particles in 3D space, with x = [x1;...; xn] ∈R3n and xi ∈R3. The index following "LJ-" indicates the number of particles (e.g., 13 or 55). The unnormalized energy function takes the form:

E(x) = ϵ

2τ

X i<j

"rm dij

6

−

rm dij

12#

+ c

2

X i

∥xi −C(x)∥2, (79)

where dij = ∥xi −xj∥2 is the pairwise distance and C(x) denotes the center of mass of the particles. We use the parameter values rm = 1, ϵ = 1, c = 0.5, and τ = 1, following prior work. The LJ-13 and LJ-55 systems correspond to 39D and 165D, respectively.

D.1.2 Baselines

Here, we outline the procedure used to obtain the values reported in Table 2 for the baseline methods.

For PIS (Zhang and Chen, 2022), DDS (Vargas et al., 2023), and LV-PIS (Richter and Berner, 2024), iDEM (Akhound-Sadegh et al., 2024), and AS (Havens et al., 2025), we reuse the values reported in AS (Havens et al., 2025, Table 1) for DW-4, LJ-13, and LJ-55 energy functions. As for MW-5, which is not included in AS, we run iDEM using their official implementation and the rest of baseline methods using our own implementation in PyTorch (Paszke et al., 2019). We were unable to obtain reportable results for LV-PIS and iDEM on this energy function.


<!-- Page 27 -->

For PDDS (Phillips et al., 2024) and SCLD (Chen et al., 2025), we run their official implementations in JAX (Bradbury et al., 2018) using the default hyperparameter settings specified for the Log-Gaussian Cox Process experiment in their respective papers. To enhance stability and convergence on synthetic energy functions, we tune the gradient clipping parameters. For PDDS, we apply clipping to the gradient of the energy function. For SCLD, we clip both the energy gradient and the Langevin norm. In both cases, the clipping magnitude is selected from the set {1, 10, 100, 1000} based on the best validation performance. Training is performed for 100,000 iterations across all runs. For SCLD, we use subtrajectory splitting with the default value of 4, so that it does not degenerate to CMCD (Vargas et al., 2024). In practice, we find that using subtrajectories yields better results.

D.1.3 Evaluation Metrics

In this subsection, we outline the evaluation criteria used to quantitatively assess the quality of samples generated from synthetic energy functions. We employ three primary metrics: Sinkhorn distance, geometric W2, and energy W2, each designed to capture different aspects of distributional similarity between generated and ground truth samples.

Sinkhorn distance To evaluate the similarity between the empirical distributions of generated and reference samples, we compute the Sinkhorn distance using the entropy-regularized optimal transport formulation (Peyré and Cuturi, 2019), following the implementation of Blessing et al. (2024) and Chen et al. (2025). The

Sinkhorn regularization coefficient is set to 10−3 throughout. We use 2,000 samples from both the generated and ground truth distributions to compute the metric.

Geometric W2 For DW and LJ tasks, the potential energy functions—and consequently, the sample distributions—exhibit invariance to both particle permutations and rigid transformations such as rotations and reflections. To appropriately account for these symmetries, we employ the geometric W2 distance as defined by Akhound-Sadegh et al. (2024) and Havens et al. (2025). Formally, the 2-Wasserstein distance is computed as:

W2

2(ˆν, ν) = inf π∈Π(ˆν,ν)

Z

D(x, y)2 π(x, y) dxdy, (80)

where Π(ˆν, ν) denotes the set of joint couplings with prescribed marginals ˆν (generated) and ν (ground truth), and D(x, y) is a symmetry-aware distance between samples defined as:

D(x, y) = min R∈O(s), P ∈S(n) ∥x −(R ⊗P)y∥2. (81)

Here, O(s) denotes the group of orthogonal transformations in s spatial dimensions (rotations and reflections), and S(n) represents the symmetric group over n particles. As exact minimization over these symmetry groups is computationally infeasible, we adopt the approximation scheme of Köhler et al. (2020). We use 2000 samples from each generated and ground truth distribution to compute the metric.

EnergyW2 To evaluate fidelity with respect to the target energy landscape, we also compute the 2-Wasserstein distance between the energy values of generated samples and those of ground truth samples. For each target distribution, we generate 2,000 samples from both the model and the reference, and compare their respective energy histograms. This scalar-based Wasserstein metric serves as a proxy for how well the generative model captures the energy histogram of the target distribution.

D.2 Alanine dipeptide

Benchmark description We adopt the experiment setup primarily from (Midgley et al., 2023). Given a configuration of alanine dipeptide, which consists of 22 particles in 3D, i.e., x = [x1; · · ·; x22] ∈R66 where xi ∈R3, we apply the same coordinate transform T proposed by Midgley et al. (2023). This coordinate transform maps the Cartesian coordinates to internal coordinates, T (x) =: z ∈R60, which include bond lengths, bond angles, and dihedral angles (Stimper et al., 2022). This process effectively removes six degrees of freedom—three for translation and three for rotation—thereby enforcing structural invariance. Non-angular coordinates are further normalized using samples with minimal energies. We refer readers to (Midgley et al.,


<!-- Page 28 -->

2023, Appendix F.1) for further details. Note that the internal coordinate transformation is bijective. Hence, we can compute the energy via

E(x) = E(T −1(z)) (82)

Evaluation and baselines For each sample x = T −1(z) ∈R66, we extract five torsion angles, including the backbone angles ϕ, ψ and methyl rotation angles γ1, γ2, γ3. We report two divergence metrics with respect to the ground-truth distribution, which contains 107 samples simulated by Molecular Dynamics. We implement the baseline methods, including PIS (Zhang and Chen, 2022), DDS (Vargas et al., 2023), AS (Havens et al., 2025), using PyTorch (Paszke et al., 2019).

For the KL divergences, we adopt setup from (Wu et al., 2020) and compute the divergence of the ground-truth marginal to model marginal for each torsion angle:

DKL(p⋆(·)||puθ(·)) ≈

X

P ⋆(·) log P ⋆(·) + ϵ

P uθ(·) + ϵ, ϵ = 10−5, (83)

where P ⋆and P uθ are histograms of 107 samples, discretized between [−π, π] with 200 intervals.

For the Wasserstein-2 distance, we use the Geometric W2 in (80), where each sample is now in 2D, x = [ϕ, ψ] ∈R2. Due to the high computational cost, we compute the value using a subset of 104 samples from the test set ground-truth samples, which is fixed for all methods.

Finally, both Ramachandran plots in Figure 5 are generated using 107 samples.

D.3 Amortized conformer generation

In this subsection, we provide some context for the experimental results found in Table 4 regarding the generation of conformers.

Benchmark description Conformers are atomic representations of molecules in cartesian space with their constituent atoms arranged into local minima on the potential energy surface. Molecules are defined to be a graph of atoms (nodes) connected by bonds (edges); conformers are geometric realizations of that molecule. Torsion angles, or rotatable bonds, are particularly important degrees of freedom for defining conformations since bond lengths and bond angles are typically much more stable due to a high sensitivity to perturbations. It is common to consider bond lengths and bond angles fixed, while the torsional degrees of freedom define the conformer.

The task in this benchmark is to take a representation of the molecular graph, usually a SMILES string (Weininger, 1988), and comprehensively sample the conformational configuration space. In flexible molecules, there can be a large number of conformers with many separated modes in a 3n−6 dimensional space. (Where n represents the number of atoms and 6 comes from the irrelevance of rotation and translation of the conformer.) We quantify the notion of comprehensively sampling the space by comparing generated structures to a set of conformers sampled using expensive, standard search techniques (Pracht et al., 2024) that were further relaxed using extremely precise density function theory-based, quantum chemistry methods (Neese, 2012; Levine et al., 2025). A detailed description of this benchmark can be found in its source (Havens et al., 2025, Appendix F.).

Evaluation and baselines The method of comparison between proposed structure and reference conformer is to use RDKit’s (Landrum, 2006) implementation of Root Mean Squared Displacement (RMSD), a measure of distance between atomic structures that is invariant to translation and rotation. We set a threshold RMSD for two structures to match and computed the Recall Coverage and Recall Average Minimum RMSD (AMR). The experiment was performed with both generated structures and with generated structures after a so-called relaxation, i.e. geometry optimization of energy, using eSEN (Fu et al., 2025). The equations for computing these metrics are:

COV-R(δ):= 1

L |{l ∈{1,..., L}: ∃k ∈{1,..., K}, RMSD(Ck, C∗ l) < δ}| (84)

AMR-R:= 1

L

X l∈{1,...,L}

min k∈{1,...,K} RMSD(Ck, C∗ l) (85)


<!-- Page 29 -->

**Table 6.** Ablation study on amortized conformer generation using the same EGNN architecture as in AS (Havens et al., 2025). We report the recall at the thresholds 1.0Å and 1.25Å, where the latter was reported in AS.

without relaxation with relaxation

SPICE GEOM-DRUGS SPICE GEOM-DRUGS

Method Coverage ↑ AMR ↓ Coverage ↑ AMR ↓ Coverage ↑ AMR ↓ Coverage ↑ AMR ↓

Threshold 1.0Å

RDKit ETKDG (Riniker and Landrum, 2015) 56.94±35.82 1.04±0.52 50.81±34.69 1.15±0.61 70.21±31.70 0.79±0.44 62.55±31.67 0.93±0.53

AS (Havens et al., 2025) 56.75±38.15 0.96±0.26 36.23±33.42 1.20±0.43 82.41±25.85 0.68±0.28 64.26±34.57 0.89±0.45

ASBS w/ Gaussian prior (Ours) 68.61±33.48 0.88±0.25 46.03±35.99 1.08±0.36 84.77±22.65 0.64±0.25 68.83±31.53 0.80±0.37

ASBS w/ Harmonic prior (Ours) 70.70±33.21 0.86±0.24 52.19±35.93 1.05±0.41 86.79±22.86 0.61±0.24 70.08±31.60 0.80±0.37

AS +RDKit warmup (Havens et al., 2025) 72.21±30.22 0.84±0.24 52.19±35.20 1.02±0.34 87.84±19.20 0.60±0.23 73.88±28.63 0.76±0.34

ASBS +RDKit warmup (Ours) 74.29±31.25 0.82±0.24 55.88±36.51 0.98±0.34 87.25±20.77 0.60±0.24 74.11±30.16 0.75±0.34

Threshold 1.25Å

RDKit ETKDG (Riniker and Landrum, 2015) 72.74±33.18 1.04±0.52 63.51±34.74 1.15±0.61 81.61±27.58 0.79±0.44 71.72±29.73 0.93±0.53

AS (Havens et al., 2025) 82.22±25.72 0.96±0.26 60.93±35.15 1.20±0.43 94.10±15.67 0.68±0.28 79.08±29.44 0.89±0.45

ASBS w/ Gaussian prior (Ours) 87.20±21.88 0.88±0.25 70.86±31.98 1.08±0.36 95.19±10.29 0.64±0.25 84.66±25.03 0.80±0.37

ASBS w/ Harmonic prior (Ours) 89.66±19.42 0.86±0.24 74.50±32.32 1.05±0.41 96.64±10.15 0.61±0.24 83.76±24.77 0.80±0.37

AS +RDKit warmup (Havens et al., 2025) 89.42±17.48 0.84±0.24 72.98±30.82 1.02±0.34 96.65±7.51 0.60±0.23 87.01±22.79 0.76±0.34

ASBS +RDKit warmup (Ours) 90.85±17.74 0.82±0.24 77.86±30.37 0.98±0.34 97.28±6.55 0.60±0.24 87.81±22.75 0.75±0.34

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100

Coverage Recall (%)

SPICE

RDKit AS ASBS gauss ASBS harmonic

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 SPICE + relax

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 GEOM-DRUGS

0 0.5 1.0 1.5 2.0 Threshold (Ångström)

0

20

40

60

80

100 GEOM-DRUGS + relax

**Figure 8.** Ablation study on full recall coverage curves (without RDKit warm-start) using the same EGNN architecture as in AS (Havens et al., 2025). Note that Table 6 reports the values at the thresholds 1.0Å and 1.25Å.

where δ = 0.75 Å is the coverage threshold, L = max(L′, 128), where L′ is the number of reference conformers, K = 2L, and let {C∗ l }l∈[1,L] and {Ck}k∈[1,K] be the sets of ground truth and generated conformers respectively. We capped the reference conformers per molecule at 512 in COV-R.

The values for the baselines are adopted from AS (Havens et al., 2025).

D.4 Additional Experiments and Discussions

Ablation study between AS and ASBS using the same EGNN For the amortized conformer generation task in Table 4, we use an EGNN architecture with 20 layers, whereas AS employs the same architecture with 12 layers. In Table 6, we report the results of ASBS using the same 12-layer EGNN as AS. Notably, our ASBS consistently outperforms AS on all metrics across all setups, except the coverage for GEOM-DRUGS with relaxation and RDKit warm-start, where ASBS falls slightly behind AS by only 1.0%. Finally, Figure 8 reports the full recall coverage curves that reproduce Table 4.

Ability of ASBS in finding modes We conduct additional experiments on the 40-mode GMM in 2D. Specifically, we instantiate ASBS with a uni-variance Gaussian source distribution centered at zero, effectively assuming no prior knowledge of the target modes, as the initial distribution does not coincide with any target modes. We also run a vanilla Langevin baseline for 1 million steps, starting from the same source distribution.

**Figure 9.** represents the quantitative results. Notably, ASBS is able to identify almost all modes. In contrast, the vanilla Langevin baseline appears to suffer from a slow mixing rate, recovering less than half of the total


<!-- Page 30 -->

40 20 0 20 40

40

20

0

20

40 Target

40 20 0 20 40

Langevin Baseline

40 20 0 20 40

ASBS (ours)

**Figure 9.** Compared to vanilla Langevin baseline, our ASBS—instantiated with a standard uni-variance Gaussian—is able to identify almost all modes without any prior knowledge of where the target modes were located.

modes even after 1 million steps. We highlight this distinction as an advantage of constructing diffusion samplers from the stochastic control and Schrödinger Bridge frameworks, which allows theoretical convergence to target distribution within a finite horizon. Finally, we believe that with proper tuning of the ASBS noise schedule, its performance can be further enhanced.

Discussion on important weights Finally, we discuss the potential integration of ASBS with importance weights, emphasizing that our theoretical and algorithmic frameworks do not preclude the use of importance weights to further enhance performance or robustness.

Formally, the importance weights over model path X ∼pu admit the following representation:

w(X):= dp⋆(X)

dpu(X) = exp

Z 1

0 −1

2∥ut(Xt)∥2dt − Z 1

0 ut(Xt) · dWt −log ˆφ1(X1)

ν(X1) + log ˆφ0(X0)

µ(X0)



, (86)

which can be obtained from (59) by setting ¯h:= ˆφ1 so that q¯h = p⋆is the optimal distribution of SB.

Note that when the source distribution degenerates to the Dirac delta µ(X0) = δ0(X0), the last term log ˆφ0(X0)

µ(X0) becomes a constant and—as discussed in Section 3.2— ˆφ1 = pbase

1, thereby recovering the weights used in prior SOC-based methods (Zhang and Chen, 2022; Havens et al., 2025).

Equation (86) is also a more concise representation than the one derived in (Richter and Berner, 2024), by recognizing the following relation through the application of Ito Lemma (46) to log ˆφt(Xt):

log ˆφ1(X1) log ˆφ0(X0) =

Z 1

0

 1

2∥vt(Xt)∥2 + (ut · vt)(Xt) + ∇· (σtvt(Xt) −ft(Xt))  dt +

Z 1

0 vt(Xt) · dWt, (87)

where we shorthand vt(x):= σt∇log ˆφt(x).

Estimating the weight in (86) requires knowing the ratios ˆφ1(x)

ν(x) and ˆφ0(x)

µ(x), which are not immediately available with the current parametrization, uθ(t, x) ≈σt∇log φt(x) and hϕ(x) ≈∇log ˆφ1(x). One accommodation is to reparametrize the functions with potential network v(t, x): [0, 1] × X →R, uθ(t, x):= σt∇vθ(t, x), hϕ(x):= ∇vϕ(1, x) (88)

and then regress their gradients onto the adjoint and corrector targets. With that, the logarithmic ratios can be easily estimated:

log ˆφ1(x)

ν(x) = vϕ(1, x) + E(x), log ˆφ0(x)

µ(x)

(42) = −log φ0(x) = vθ(0, x). (89)

A more detailed investigation of this importance sampling scheme is left for future work.
