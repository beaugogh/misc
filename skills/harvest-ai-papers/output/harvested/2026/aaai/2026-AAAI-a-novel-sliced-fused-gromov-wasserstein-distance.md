---
title: "A Novel Sliced Fused Gromov-Wasserstein Distance"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39669
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39669/43630
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# A Novel Sliced Fused Gromov-Wasserstein Distance

<!-- Page 1 -->

A Novel Sliced Fused Gromov-Wasserstein Distance

Moritz Piening*, Robert Beinert*

Institut f¨ur Mathematik, Technische Universit¨at Berlin, Straße des 17. Juni 136, 10623 Berlin, Germany piening@math.tu-berlin.de, beinert@math.tu-berlin.de

## Abstract

The Gromov–Wasserstein (GW) distance and its fused extension (FGW) are powerful tools for comparing heterogeneous data. Their computation is, however, challenging since both distances are based on non-convex, quadratic optimal transport (OT) problems. Leveraging 1D OT, a sliced version of GW has been proposed to lower the computational burden. Unfortunately, this sliced version is restricted to Euclidean geometry and loses invariance to isometries, strongly limiting its application in practice. To overcome these issues, we propose a novel slicing technique for GW as well as for FGW that is based on an appropriate lower bound, hierarchical OT, and suitable quadrature rules for the underlying 1D OT problems. Our novel sliced FGW significantly reduces the numerical effort while remaining invariant to isometric transformations and allowing the comparison of arbitrary geometries. We show that our new distance actually defines a pseudometric for structured spaces that bounds FGW from below and study its interpolation properties between sliced Wasserstein and GW. Since we avoid the underlying quadratic program, our sliced distance is numerically more robust and reliable than the original GW and FGW distance; especially in the context of shape retrieval and graph isomorphism testing.

## Introduction

The Gromov–Wasserstein (GW) distance (M´emoli 2011) and the Fused Gromov–Wasserstein (FGW) distance (Vayer et al. 2020a) extend the classical optimal transport (OT) framework (Villani 2003) to the comparison of heterogenous data by modelling them as metric measure spaces (mmspaces). While the resulting distances are powerful tools, their computation is costly and does not admit an exact solution. To accelerate the underlying non-convex, quadratic program, several algorithms have been proposed using regularization techniques (Peyr´e, Cuturi, and Solomon 2016; Peyr´e and Cuturi 2019), employing linearized distances (Beier, Beinert, and Steidl 2022; Nguyen and Tsuda 2023), quantizating the problem (Chowdhury, Miller, and Needham 2021) or using constrained optimization (Scetbon, Peyr´e, and Cuturi 2022; Scetbon et al. 2023). As a consequence, established solvers mainly compute upper bounds and numerical approximations of the actual GW and FGW distance.

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

An alternative acceleration framework builds on 1D OT and random projections to define the so-called sliced GW distance (Vayer et al. 2019; Beinert, Heiss, and Steidl 2023). However, sliced GW is restricted to Euclidean geometry and lacks isometric invariance, limiting its practical use. As a remedy, we design a novel sliced GW distance fixing these issues and extend it to FGW. In particular, our new distance allows for an analytical computation outlined in Figure 1.

For our design, we turn towards the complementary literature on lower GW bounds (M´emoli 2011; Vayer et al. 2019, 2020b; Jin, Yu, and Zhang 2022). Since many of these rely on optimization heuristics, such as bi-convex relaxation (Vayer et al. 2020b) or sorting (Vayer et al. 2019; Beinert, Heiss, and Steidl 2023), and we are interested in exact computation, we turn our attention to the bounds in (M´emoli 2011). In particular, we are motivated by recent theoretical work proving their metricity on certain spaces (M´emoli and Needham 2022) and the practical effectiveness of such bounds in graph isomorphism testing (Weitkamp 2022; Weitkamp et al. 2024), where established GW solvers fail in practice. The aim behind graph isomorphism testing (Shervashidze et al. 2011; Grohe and Schweitzer 2020) is to verify or disprove whether two or more graphs are topologically equivalent or not.

In this paper, we focus on the strongest of M´emoli’s GW bounds—the third lower bound (TLB)—and start by extending TLB to the fused case. TLB itself is defined as a hierarchical OT problem, i.e., an OT problem whose costs are given by another OT problem. Indeed, formulations of such kinds recently have attracted attention from the OT community (Dukler et al. 2019; Alvarez-Melis and Fusi 2020). Despite interesting theoretical properties (Delon and Desolneux 2020; Bonet, Vauthier, and Korba 2025), these problems are usually computationally challenging. Therefore, recent work has focused on extending sliced Wasserstein (SW) techniques to the hierarchical case for acceleration (Piening and Beinert 2025b; Nguyen et al. 2025). Keeping this technique in mind, we tackle the computational burden of our new FGW lower bound by rewriting it as an Euclidean Wasserstein distance. To circumvent the limitation of slicing in high dimensions (Tanguy, Flamary, and Delon 2025), we propose to employ numerical quadrature schemes. All in all, we deduce an equivalent, but more efficient, lower bound. Apart from extending the literature on sliced hierarchical

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

24828

<!-- Page 2 -->

features structured space quantiles and features structures pairwise distances sorted rows sampled quantiles features structured space structures pairwise distances sorted rows sampled quantiles quantiles and features

SFTLB

FTLB

OT

Wasserstein sliced Wasserstein

**Figure 1.** Visualization of our novel sliced fused Grovov–Wasserstein distance called SFTLB: Starting from two structured spaces like labeled graphs equipped with a graph distance, we sort the corresponding distance matrices row-wise. Subsequently, we determine samples of the quantile functions of the local distance distribution for each node. Afterward, we concatenate the sampled quantiles with the original features and interpret the outcome as an empirical Euclidean measure. Finally, we compute the Wasserstein or sliced Wasserstein distance between these measures.

OT, this also overcomes previous limitations of sliced GW, where sorting-based solvers might fail (Vayer et al. 2019; Beinert, Heiss, and Steidl 2023). We summarize our contributions as follows:

1. Towards the goal of an exact solver, we generalize M´emoli’s GW bound to FGW and recall its connection to a classical Wasserstein problem.

2. To overcome the limitations of sliced GW, we employ this connection and numerical quadrature schemes to define an effective novel sliced FGW distance between arbitrary structured spaces beyond Euclidean geometry.

3. We prove that our new distance is a pseudo-metric interpolating between TLB and SW. Additionally, our proof illustrates the dimensional dependence of SW.

4. Lastly, we provide numerical experiments for our sliced FGW, showcasing its efficiency as well as its applicability for shape comparison and graph isomorphism testing.

Proofs and additional remarks/experiments can be found in the extended version on arXiv (Piening and Beinert 2025a).

Optimal Transport-Based Distances

At the heart of OT is the calculation of optimal transfers from one measure to another. For this, let P(X) denote the space of Borel probability measures on a compact Polish space X. A measure ξ ∈P(X) is translated to another compact Polish space Y via a mapping T: X →Y by the pushforward T♯ξ:= ξ ◦T −1. Based on the canonical projections π• onto a component, e.g., πX: X × Y →X, (x, y) 7→x, the set of transport plans between ξ ∈P(X), υ ∈P(Y) is defined as

Γ(ξ, υ):= γ ∈P(X × Y)

πX,♯γ = ξ, πY,♯γ = υ

.

In general, OT seeks to find an optimal transport plan minimizing a given loss function. For certain losses, this procedure yields a metric between probability measures.

Wasserstein Distance For compact Z ⊂Rd equipped with the Euclidean norm ∥·∥, ζ, ζ′ ∈P(Z), and p ∈[1, ∞), the p-Wasserstein distance is introduced as

Wp p(ζ, ζ′):= inf γ∈Γ(ζ,ζ′)

Z

Z×Z

∥z −z′∥p dγ(z, z′)

=:Tp(γ)

(1)

and defines a metric1 on P(Z). Its computation requires expensive optimization procedures since closed-form solutions are rarely available.

One exception is the special case Z ⊂R, where the optimal plan can be expressed using the quantile function:

qζ: (0, 1) →R, s 7→inf z ∈R ζ((−∞, z]) > s

.

Then, the p-Wasserstein distance admits the closed-form

Wp p(ζ, ζ′) =

Z 1

0 qζ(s) −qζ′(s)

p ds; (2)

see (Villani 2003). For discrete measures with with n and m support points, the integral in (2) reduces to a sum with n+m−1 summands; see (Peyr´e and Cuturi 2019, Prop. 3.5) and (Villani 2003, Thm. 2.18).

Sliced Wasserstein Distance To leverage the computational benefits of the 1D Wasserstein distance, we consider the slicing operator πθ: Rd →R, z 7→θ · z, θ ∈Sd−1, where Sd−1:= {θ ∈Rd | ∥θ∥= 1} denotes the sphere with surface area A(Sd−1) and · the Euclidean inner product. For compact Z ⊂Rd, ζ, ζ′ ∈P(Z), and p ∈[1, ∞), the sliced p-Wasserstein (SW) distance is introduced as

SWp p(ζ, ζ′):= 1 A(Sd−1)

Z

Sd−1 Wp p(πθ,♯ζ, πθ,♯ζ′) dθ

1Symmetric, positive definite function with triangle inequality.

24829

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-002-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

with respect to the surface measure on Sd−1. The interest in this sliced distance is justified by the close relation to the classical Wasserstein distances. Namely, for compact Z ⊂Rd, both distances display a form of metric equivalence, i.e., there exists CZ > 0 such that

SWp p(ζ, ζ′) ≤Wp p(ζ, ζ′) ≤CZ SW

1 (d+1) p (ζ, ζ′)

for any ζ, ζ′ ∈P(Z); see (Bonnotte 2013; Bonneel et al. 2015; Kolouri, Park, and Rohde 2016). Moreover, the spherical integral can be efficiently approximated via random projections using Monte Carlo or Quasi-Monte Carlo methods for low-dimensional data (Nguyen, Bariletto, and Ho 2024; Hertrich, Jahn, and Quellmalz 2025) as well as Gaussian approximations for high-dimensional data (Nadjahi, Vialard, and Peyr´e 2021). Note that there exist various extensions to non-Euclidean spaces (Kolouri et al. 2019; Quellmalz, Beinert, and Steidl 2023; Bonet, Drumetz, and Courty 2025), invariant data (Beckmann, Beinert, and Bresch 2025a,b), general probability divergences (Nadjahi et al. 2020; Hertrich et al. 2024) and kernels (Rux, Quellmalz, and Steidl 2025).

Gromov–Wasserstein Distance To compare measures on distinct metric spaces, the GW distance extends classical OT by matching pairwise distances. For this, let X:= (X, g, ξ) be a metric measure (mm) space consisting of a compact metric space (X, g) and ξ ∈P(X). For mm-spaces X:= (X, g, ξ) and Y = (Y, h, υ), the Gromov–Wasserstein (GW) distance is then defined as

GWp p(X, Y):= inf γ∈Γ(ξ,υ)

ZZ

(X×Y)2 g(x, x′) −h(y, y′)

p

× dγ(x′, y′) dγ(x, y)

=:Dp(γ)

.

(3) Here, each transport plan π induces an overall distortion Dp between g and h. This expression defines a metric on the equivalence classes of isomorphic mm-spaces; see (M´emoli 2011). Since (3) is a non-convex, quadratic program, its minimization typically relies on entropic regularization and costly block-coordinate descent (Peyr´e and Cuturi 2019). As a consequence, a set of hierarchical lower bounds has been proposed in (M´emoli 2011; M´emoli and Needham 2022).

First Lower Bound Define the pointwise p-eccentricity sX,p: X →R of an mm-space X:= (X, g, ξ) as sp

X,p(x):=

Z

X gp(x, x′) dξ(x′).

Then, the first lower GW bound between X and Y is

FLBp p(X, Y):= Wp p(sX,p,♯ξ, sY,p,♯υ), which compares only the first-order moments of pairwise distances. This is an efficiently solvable 1D OT problem.

Second Lower Bound By matching the entire distribution of distances, the second lower GW bound reads as

SLBp p(X, Y):= Wp p g♯(ξ ⊗ξ), h♯(υ ⊗υ)

, where ⊗denotes the product measure. This lifts FLB by considering all pairwise distances at once. Again, characterization as 1D transport problem enables fast computation.

Third Lower Bound For each (x, y) ∈X × Y, the local distance distributions between X and Y is defined via

LDp p(x, y):= inf γ∈Γ(ξ,υ)

Z

X×Y g(x, x′) −h(y, y′)

p dγ(x′, y′)

= Wp p g(x, ·)♯ξ, h(y, ·)♯υ

. (4)

Decoupling the minimization of the inner and outer integral in (3), we arrive at the third lower GW bound:

TLBp p(X, Y):= inf γ∈Γ(ξ,υ)

Z

X×Y

LDp p(x, y) dγ(x, y)

=: ˜ Dp(γ)

. (5)

Note that the inner plans in (4) do not match the outer plan in (5). Similar to the other two cases, the estimation of LD benefits from accelerated 1D solutions. In contrast, TLB still requires a costly OT minimization.

Comparing all three lower bounds, we obtain the hierarchy (M´emoli 2011; Chowdhury and M´emoli 2019):

FLBp(X,Y) ≤SLBp(X,Y) ≤TLBp(X,Y) ≤GWp(X,Y).

Moreover, TLB is positive definite and thus defines a metric for certain classes of mm-spaces, whereas FLB and SLB fail to distinguish isomorphic mm-spaces (M´emoli and Needham 2022). To avoid the outer OT problem in (5), (Sato et al. 2020) rely on the maximum mean discrepancy (MMD) with respect to the 1D Wasserstein distance as kernel, which leads to an efficient computation scheme. In this paper, we follow a different approach by accelerating the computation of the outer OT problem using an efficient slicing, which actually leads to a metric equivalence with TLB.

Fused Gromov–Wasserstein Distance The GW distance allows for a geometrically meaningful comparison between unlabeled, undirected graphs. However, due to the importance of node features in practical applications, practitioners often resort to a combination of Wasserstein and GW distances. For this, the mm-spaces are extended by a common compact feature space Z ⊂Rd. More precisely, a structured space XS:= (X ×Z, g, ξ) consists of a compact metric space (X, g) and ξ ∈P(X × Z). Structured spaces are also known as labelled spaces or structured objects (Vayer et al. 2020a). The space of all structured spaces is denoted as S(Z). Having the generalization of TLB and its slicing in mind, we study the following distance on S(Z), which is a specific variant of (Vayer et al. 2020a, Def. 8): for XS:= (X × Z, g, ξ), and YS:= (Y × Z′, h, υ) with Z = Z′ as well as α ∈[0, 1] and p ∈[1, ∞), the fused GW (FGW) distance reads as

FGWp α,p(XS, YS):= inf γ∈Γ(ξ,υ)(1 −α) Dp(πX×Y,♯γ)

+ α Tp(πZ×Z′,♯γ), where Dp denotes the distortion in (3), Tp refers to the transport in (1), and α balances structure versus features. In the case α = 0, we recover the original GW distance of the structure part; for α = 1, we obtain the original Wasserstein distance of the label part. Notice that, for α ∈(0, 1) and

24830

<!-- Page 4 -->

p ∈[1, ∞), FGW only defines a semi-metric2 on the space of isomorphic structure spaces, fulfilling the relaxed triangle inequality

FGWp α,p(YS

1, YS 2)

≤2p−1

FGWp α,p(YS

1, XS) + FGWp α,p(XS, YS

2)

; see (Vayer et al. 2020a, Prop. 4).

## 3 Accelerating the Calculation of FGW A Lower Bound Using TLB

In principle, any of the lower bounds for the GW distance may be directly extended to the FGW distance. Due to the metric properties of TLB and its tight affinity to the original GW distance, we solely focus on this bound. The basic idea is to replace the GW distortion in FGW by TLB. In this manner, for XS:= (X ×Z, g, ξ), YS:= (Y ×Z′, h, υ) with compact Z = Z′ ⊂Rd, α ∈[0, 1], and p ∈[1, ∞), we introduce the Fused Third Lower Bound (FTLB) via

FTLBp α,p(XS, YS):= inf γ∈Γ(ξ,υ)(1 −α) ˜Dp(πX×Y,♯γ)

+ α Tp(πZ×Z′,♯γ), (6)

where ˜Dp relates to the mm-spaces X:= (X, g, πX,♯ξ) and Y:= (Y, h, πY,♯υ). Similar to GW and FGW, this includes TLB for α = 0. Consequently, all subsequent results apply to the classical GW distance as well. Indeed, FTLB provides a lower bound since we minimize over multiple, uncoupled inner plans as opposed to finding a single coupled plan. Due to the similarity to FGW, many properties of the original distance carry over to FTLB. Proposition 3.1. For XS:= (X × Z, g, ξ), YS:= (Y × Z, h, υ), Z ⊂Rd compact, let ξF:= πZ,♯ξ, υF:= πZ,♯υ and X:= (X, g, πX,♯ξ), Y:= (Y, h, πY,♯υ).

(i) There exists γ∗∈Γ(ξ, υ) minimizing (6). (ii) FTLBα,p(XS, YS) ≤FGWα,p(XS, YS). (iii) FTLBα,p(XS, YS) →Wp(ξF, υF) as α →1.

(iv) FTLBα,p(XS, YS) →TLBp(X, Y) as α →0.

(v) FTLBα,p defines a pseudo-semi-metric3 on S(Z) with

FTLBp α,p(YS

1, YS 2)

≤2p−1

FTLBp α,p(YS

1, XS) + FTLBp α,p(XS, YS

2)

for all XS, YS

1, YS 2 ∈S(Z).

A Novel Lower Bound via Slicing While lowering the computational burden, FTLB still requires solving an OT problem. For two discrete measures of cardinality n, this leads to a computational complexity of O(n3) for an exact OT solution and O(n2 log n) for a regularized one (Peyr´e and Cuturi 2019). To achieve further acceleration, we aim to combine ideas from SW and numerical integration. For this, let XS:= (X × Z, g, ξ) and YS:= (Y × Z′, h, υ) be equipped with discrete measures ξ:= n X i=1 ξi δ(xi,zi) and υ:= m X j=1 υj δ(yj,z′ j). (7)

2Metric without triangle inequality. 3Semi-metric d without definiteness (d(x, x′) = 0̸ ⇒x = x′).

For the special case p = 2, we start with considering LD2 in (4), which is the key ingredient of the structure distortion

˜D2. The required 1D Wasserstein distance may here be analytically determined by exploiting (2), where the quantile functions can be explicitly computed using efficient sorting algorithms. To surmount the outer OT problem of FTLB, we instead propose to merely approximate (2) via some quadrature scheme, i.e.,

LD2

2(x, y) ≈ r X k=1 wk qg(x,·)♯ξ(sk) −qh(y,·)♯υ(sk)

2 with weights wk > 0, knots sk ∈(0, 1), and small r ∈ N. Note that we restrict ourselves to quadrature rules with positive weights. Using qξ,x:= (√wkqg(x,·)♯ξ(sk))r k=1 and qυ,y:= (√wkqh(y,·)♯υ(sk))r k=1, we may also write

LD2

2(x, y) ≈∥qξ,x −qυ,y∥2. In this manner, FTLB can be approximated by

FTLB2 α,2(XS, YS) ≈inf γ∈Γ(ξ,υ)

n,m X i,j=1 γij

√1−α (qξ,xi−qυ,yj)

√α (zi−z′ j)

2

= W2

2 n X i=1 ξi δ √1−αqξ,xi √αzi

=:ξQ α ∈P(Rr+d)

, m X j=1 υj δ √1−αqυ,yj √αz′ j

=:υQ α ∈P(Rr+d)

, (8)

where πij:= π((xi, zi), (yj, z′ j)). This approximation carries over to TLB. More precisely, for X:= (X, g, ξ) and Y:= (Y, h, υ) with ξ:= Pn i=1 ξi δxi and υ:= Pm j=1 υj δyj, we here obtain

TLB2

2(X, Y) ≈W2 2 n X i=1 ξi δqξ,xi

=:ξQ∈P(Rr)

, m X j=1 υj δqυ,yj

=:υQ∈P(Rr)

. (9)

Up to here, we have approximated TLB and FTLB using a quadrature rule for the inner 1D Wasserstein distances. To overcome the remaining outer OT minimization behind the Wasserstein distances in (8) and (9), we finally propose to replace these with the SW distance:

SFTLBα,2(XS, YS):= SW2(ξQ α, υQ α)

STLB2(X, Y):= SW2(ξQ, υQ). (10) In general, the sliced lower bounds hold only approximately, i.e., SFTLBα,2(XS, YS) ⪅FGW(XS, YS), where the quality depends on the employed quadrature rule. Since ξQ α, υQ α ∈P(Rr+d) and ξQ, υQ ∈P(Rr), the employed SW distances can be efficiently computed independently of the atom numbers n and m in (7). Moreover, many properties of the original FGW distance from Proposition 3.1 carry over to the sliced variant. Proposition 3.2. For XS:= (X × Z, g, ξ), YS:= (Y × Z, h, υ), Z ⊂Rd compact, let ξF:= πZ,♯ξ, υF:= πZ,♯υ and X:= (X, g, πX,♯ξ), Y:= (Y, h, πY,♯υ). For k, ℓ∈N with ℓ> 1, let ck,ℓ:= s

A(Sk+ℓ+1)

A(Sℓ+1)

A(Sℓ−1) A(Sk+ℓ−1).

For an arbitrary quadrature rule, it holds:

24831

<!-- Page 5 -->

(i) SFTLBα,2 defines a pseudo-metricS(Z), (ii) SFTLBα,2(XS, YS) →cr,d SW2(ξF, υF) as α →1, (iii) SFTLBα,2(XS, YS) →cd,r STLB2(X, Y) as α →0.

Given that ck,ℓ→0 for k →∞and ℓfixed (Gray 2004), the constants cr,d and cd,r illustrate the curse of dimensionality of the SW distance. In contrast to classical Wasserstein transport, the value of the SW distance for measures living on a subspace depends on the dimension of the underlying Euclidean space. Indeed, as we believe this to be of independent interest to the OT community, we state this dependence as a general result employed in the proof of Proposition 3.2. Proposition 3.3. For ζ, ζ′ ∈P(A × Z), A ⊂Rr and Z ⊂ Rd compact, with πA,♯ζ = πA,♯ζ′ = δ0, it holds

SW2(ζ, ζ′) = cr,d SW2(πZ,♯ζ, πZ,♯ζ′). Importantly, for empirical measures ξ and υ with n = m and ξi = υi = 1/n in (7), the rather simple, equispaced midpoint rule with r = n becomes exact, i.e.,

FTLBα,2(XS, YS) = W2(ξQ α, υQ α) instead of the approximation in (8). Consequently, SFTLB becomes an actual lower bound for the FGW distance. Moreover, SFTLB and FTLB are metrically equivalent. Proposition 3.4. For XS:= (X × Z, g, ξ) and YS:= (Y × Z, h, υ) with bounded X and Y, i.e. g(x, x′) ≤D and h(y, y′) ≤D for fixed D, and compact Z ⊂Rd, let ξ and υ in (7) be empirical measures with n = m and ξi = υi = 1/n. For the equispaced midpoint rule with r = n, it holds:

(i) SFTLBα,2(XS, YS) ≤FGWα,2(XS, YS), (ii) there exists CZ,D,r > 0 such that

SFTLBα,2(XS, YS) ≤FTLBα,2(XS, YS)

≤CZ,D,r SFTLB

1 r+d+1 α,2 (XS, YS). (11) Note that CZ,D,r can be chosen such that (11) holds true for all XS and YS of the stated form. Furthermore, Proposition 3.4 can be directly generalized to empirical measures ξ and υ with different atom numbers n and m by using a non-equispaced midpoint rule with r = n + m −1, see the technical appendix on arXiv (Piening and Beinert 2025a).

## 4 Numerical Experiments

In the following, we study the computational runtime of our distances, the underlying transport plans, as well as their behaviour in applications like free-support barycenters, shape classification, and graph isomorphism testing. All experiments were conducted with 13th Gen Intel Core i5-13600K CPU and an NVIDIA GeForce RTX 3060 GPU (12 GB).

Computational and Runtime Analysis For simplicity, we assume that the measures of the structured spaces XS:= (X × Z, g, ξ) and YS:= (Y × Z, h, υ) are empirical with the same number of atoms, i.e., n = m and ξi = υj = 1/n in (7). The first step of FTLB and SFTLB is to sample the quantiles of the local distance distributions, i.e., to compute qξ,xi and qυ,yj in (9), which essentially requires a row-wise sorting of the distance matrices regarding g and h with total complexity O(n2 log n).

n 100 10 000

FGW 0.03 ± 0.02 0.45 ± 0.07 178.29 ± 5.22 FTLB 0.06 ± 0.03 0.10 ± 0.02 15.69 ± 0.43 SFTLB 0.04 ± 0.04 0.03 ± 0.01 1.18 ± 0.00

**Table 1.** Average computation time in seconds for 5 instances with graph sizes 100, 1000, and 10 000. The remaining parameters have been chosen as r = 10 and L = 50.

FTLB In its second step, FTLB requires solving the outer OT problem in (9). Calculating the OT costs requires O((r+ d) n2) operations. The OT problem itself may be solved exactly in O(n3) or approximately in O(n2 log n) using entropic regularization; see (Peyr´e and Cuturi 2019). This leads to an all-in-all complexity of O((r+d+n) n2) (exact) or O((r+d+log n) n2) (approximated). In the experiments, we perform exact inner OT calculations with r = n.

SFTLB Here, we initially determine ξQ α and υQ α. Next, we employ a Monte Carlo scheme to calculate (10) by

SFTLB2 α,2(XS, YS) ≈1

L

L X ℓ=1

W2

2(πθℓ,♯ξQ α, πθℓ,♯υQ α)

with uniformly distributed directions θℓ∈Sr+d−1. The 1D Wasserstein distance can be computed by sorting, yielding an all-in-all complexity of O(Ln(r +d)+(Ln+n2) log n), where we aim for a small r. Here, the Monte Carlo scheme converges in O(

√

L) (Nadjahi et al. 2020).

The computational complexity of FTLB and SFTLB is dominated by the preliminary row-wise sorting and the employed OT solvers. To study the actual run-time speed-up, we generate 5 pairs of n × n distance matrices with n ∈ {100, 1000, 10 000} and 1D normal features. Using the POT toolbox (Flamary et al. 2021) for the OT computations, we then determine the corresponding FTLB, SFTLB, and FGW distance. The runtimes are recorded in Table 1, where the significant speed-up due to the slicing is clearly visible.

FTLB Transport Plans Although the GW distance is well fitted to detect similarities between two single structures, it usually fails to detect these in a set of independent structures. The FGW distance can overcome this issue by assigning appropriate labels. This observation carries over to the outer transport plans of TLB and FTLB, which is illustrated in Figure 2, where the left two spirals are transported to the right two. Source and target are here modelled as point clouds in R2 equipped with the Euclidean distance and binary feature labels.

To compare our FTLB transport with FGW and its entropic version, we adapt an example from (Flamary et al. 2021); see Figure 3. Each image displays the source graph on the left and the target graph on the right. The transports are visualized using the color of the community assignment in the source. In this example, the FTLB plan captures the main structures similarly to the original FGW plan, indicating that our FTLB transport may be an efficently-to-compute alternative in practice.

24832

<!-- Page 6 -->

(a) TLB

(b) FTLB (α = 0.9)

**Figure 2.** Comparison of TLB and FTLB transport plans. Crosses are colored based on the transported mass. FTLB achieves a more regular transport plan by integrating labels.

**Figure 3.** Comparison of FGW, entropic FGW (ϵ = 0.01), FTLP transport plan for α = 0.5. Target nodes are colored according to the transported mass. FGW and FTLB capture the same structural similarities.

Free-Support Euclidean Barycenters GW barycenters are generalized Fr´echet means that interpolate several mm-spaces Yk, k = 1,..., K by solving arg min n K X k=1

GW2

2(X, Yk) X mm-space o

. (12)

The solutions of the GW barycenter problem can be completely characterized using multi-marginal OT (Beier, Beinert, and Steidl 2023; Beier and Beinert 2025); its numerical computation, however, remains challenging. Established free-support methods (Peyr´e and Cuturi 2019) minimize over the distance of X producing non-Euclidean outputs; whereas fixed-support methods (Beier, Beinert, and Steidl 2023; Beier et al. 2025) limit the resolution of the barycenter. As an alternative, we replace GW in (12) by TLB, STLB (r = 500, L = 500) and the so-called Anchor Energy (AE) distance (Sato et al. 2020) for comparison. For each distance, we perform a gradient descent over the points xi ∈Rd in X = ({xi}n i=1, dE, ι}, where dE is the Euclidean metric

Bone Inputs TLB AE STLB

Goblet Inputs TLB AE STLB

Star Inputs TLB AE STLB

**Figure 4.** Euclidean 2D TLB, AE and STLB barycenters for five samples of different shape classes.

and ι the uniform measure. Figure 4 shows computed 2D barycenters for different upsampled shapes (n = 500) from (Beier, Beinert, and Steidl 2022), obtained via three identical random restart initializations, and 1000 steps (width: 0.1).

Classification of 2D and 3D Shapes A key application of the GW distance is the comparison of shapes, which can be represented as Euclidean point clouds or as meshes equipped with geodesic distances. Building on experiments from (M´emoli 2011; Beier, Beinert, and Steidl 2022), we rely on the k-nearest neighbor (KNN) classification (Cover and Hart 1967). More precisely, we first precompute pairwise distance matrices with respect to SLB, TLB, STLB (r = 10, L = 100), AE (Sato et al. 2020), qGW (Chowdhury and M´emoli 2019), LGW (Beier, Beinert, and Steidl 2022) and GW. Second, we evaluate the classification accuracy by assigning each test point to the majority class among its three nearest neighbors. We report the mean accuracy over 1000 random 25%/75% training/test splits on the following datasets: 2D Shapes: 80 shapes from 4 classes (bone, goblet, star, horseshoe) represented as Euclidean point clouds, each consisting of 50 points (Beier, Beinert, and Steidl 2022); Animals: 73 human/animal shapes from 7 classes (Sumner and Popovi´c 2004) downsampled to 3D meshes with 50 vertices, equipped with the geodesic distance (M´emoli 2011; Beier, Beinert, and Steidl 2022); FAUST-500 and FAUST-1000: 100 human meshes from

10 subjects (Bogo et al. 2014), downsampled and represented by 3D meshes with 500 and 1000 vertices equipped with the geodesic distance using PyVista (Sullivan and Kaszynski 2019) and NetworkX (Hagberg, Schult, and Swart 2008). Table 2 summarizes classification accuracy, runtime, and nullspace types (M´emoli and Needham 2022): SLB vanishes for globally matching distance distributions (‘global’), TLB/STLB/AE for locally matching distributions (‘local’), and GW for isomorphic shapes (‘iso’). Lastly, LGW and

24833

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-a-novel-sliced-fused-gromov-wasserstein-distance/page-006-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

distance type 2D shapes animals FAUST-500 FAUST-1000 acc. (%) time (ms) acc. (%) time (ms) acc. (%) time (ms) acc. (%) time (ms)

SLB global 97.9±2.2 0.6 100.0±0.1 0.7 31.2±5.4 48.3 35.2 ± 5.7 183.7 TLB local 100.0±0.3 0.7 100.0±0.0 0.8 36.8±5.4 24.8 40.0 ± 6.0 88.3 STLB local 99.3±1.2 1.3 99.2±1.1 1.5 35.8±5.5 11.6 40.1±5.7 23.1 AE local 99.7±0.9 0.6 97.8±1.8 0.7 37.8±5.6 8.1 41.6±5.7 35.8 GW iso 99.7±0.6 2.6 100.0±0.0 5.8 29.2±4.3 482.0 33.3±5.2 2398.3 LGW approx 91.2±2.7 288.9 89.8±3.9 481.0 29.4±4.7 7 · 104 30.2±5.1 105 qGW approx 61.6±4.4 16.4 48.8±6.3 14.7 13.7±3.6 18.2 12.4±3.2 35.3

**Table 2.** KNN Shape classification: Mean accuracy (acc.) with standard deviation and mean runtime (time).

graph model WS BA RR WS BA RR nodes 10 10 10 500 500 100 parameters k=4, pE=0.1 m=5, pB=0.5 R = 3, pB = 0.5 k=250, pE=0.1 m=250, pB=0.1 R = 3, pB = 0.5

SLB 90.40 ± 2.62 61.50 ± 3.44 96.30 ± 1.62 50.00 ± 0.00 50.00 ± 0.00 100.00 ± 0.00 TLB 96.80 ± 2.99 99.50 ± 1.02 99.40 ± 1.80 100.00 ± 0.00 100.00 ± 0.00 100.00 ± 0.00 STLB 99.00 ± 1.00 99.80 ± 0.40 99.80 ± 0.60 99.60 ± 0.80 99.40 ± 0.92 100.00 ± 0.00 GW 67.40 ± 3.83 73.30 ± 3.85 65.50 ± 4.03 65.00 ± 5.00 100.00 ± 0.00 100.00 ± 0.00 WL-D 100.00 ± 0.00 100.00 ± 0.00 50.00 ± 0.00 100.00 ± 0.00 100.00 ± 0.00 50.00 ± 0.00 FTLB 100.00 ± 0.00 96.00 ± 1.18 97.60 ± 1.50 100.00 ± 0.00 94.80 ± 1.60 98.60 ± 0.92 SFTLB 100.00 ± 0.00 98.20 ± 1.08 99.40 ± 0.92 100.00 ± 0.00 100.00 ± 0.00 99.80 ± 0.60 FGW 98.20 ± 1.66 90.30 ± 1.79 74.60 ± 2.69 100.00 ± 0.00 98.80 ± 1.33 69.80 ± 4.42 WL-F 100.00 ± 0.00 83.10 ± 3.21 81.30 ± 3.85 100.00 ± 0.00 99.20 ± 1.33 86.80 ± 3.92

**Table 3.** Mean accuracy (%) with standard deviation for graph isomorphism testing. The first five methods are label-agnostic, whereas the last four methods employ node features. Proposed methods are printed in bold.

qGW approximate GW (‘approx’)4. While most methods perform near-perfectly on ‘2D shapes’ and ‘animals’, accuracy drops on FAUST datasets. On these, ‘local’ methods (TLB, STLB, AE) consistently outperform other approaches. Although GW should yield perfect classifications in theory, the underlying non-convex quadratic minimization reduces the numerical accuracy. STLB shows a clear runtime advantage for large-scale datasets.

Detection of Graph Isomorphisms

An important theoretical property of the GW and FGW distance is that they vanish only for two isomorphic inputs (M´emoli 2011; Vayer et al. 2020a), which facilitates an application in graph isomorphism testing. In practice, the established GW and FGW solvers are however not accurate enough to give reliable results of this NP-hard problem (Grohe and Schweitzer 2020). Therefore, SLB has been proposed as a statistical test for graph isomorphisms (Weitkamp 2022; Weitkamp et al. 2024). However, SLB has less statistical power than TLB (M´emoli and Needham 2022); for this reason, we propose to use STLB and SFTLB instead. During the experiment, we rely on synthetic datasets of random graphs with fixed node numbers, where half of the graph pairs are isomorphic and half of the graph pairs are not. Here, we consider these graph generation models:

Watts–Strogatz (WS) Graph: The WS graph is governed by a neighborhood number k and an edge rewiring probability pE (Watts and Strogatz 1998). We add node features according to a 1D standard normal distribution.

4LGW/qGW depend heavily on hyperparameter choices balancing speed and performance, see our appendix for a discussion.

Barabasi–Albert (BA) Graph: The BA graph is governed by an edge generation number m (Barab´asi and Albert 1999). We assign node features in {0, 1} based on a Bernoulli distribution with probability pB. Random Regular (RR) Graph: The RR graph is based on a regularity R (Bollob´as 1998). We assign Bernoulli node features in {0, 1} according to the probability pB.

We compare the generated, unlabeled graph pairs using SLB, TLB, STLB, GW, and Weisfeiler-Lehman (WL) kernel test (Shervashidze et al. 2011). For the WL test, we use 5 iterations and set the labels to the node degree (WL-D). The labeled graph pairs are compared using α = 0.5 for FTLB, SFTLB (r = 5, L = 100), and entropic FGW (ε = 10−3), as well as with WL using 5 iterations and (binned) node features (WL-F). We classify two graphs as isomorphic if they are among the 50% most similar graph pairs in terms of the different distances or if the distance becomes exactly zero. In Table 3, we display the results of 10 experiment repetitions over 6 different random graph configurations.

## 5 Conclusion

We address the computational limits of GW and FGW by introducing new lower bounds. Extending TLB to the fused setting and linking it to a Wasserstein problem, we derive an efficient sliced FGW via numerical quadrature of 1D OTs. Our work bridges TLB and SW, clarifies SW’s dimensional behavior, and proves effective for shape and graph comparisons, thereby overcoming the limitations of sliced GW (Vayer et al. 2019). In future research, the calculation of local distance distribution required for AE, FTLB, and SFTLB may be further accelerated via sweep-line algorithms (Sato et al. 2020), which is not studied in this work.

24834

<!-- Page 8 -->

## Acknowledgments

M.P. acknowledges funding from the German Research Foundation (DFG) within the project BIOQIC (GRK2260/289347353).

## References

Alvarez-Melis, D.; and Fusi, N. 2020. Geometric dataset distances via optimal transport. In Advances in Neural Information Processing Systems, volume 33, 21428–21439. Curran Associates. Barab´asi, A.-L.; and Albert, R. 1999. Emergence of scaling in random networks. Science, 286(5439): 509–512. Beckmann, M.; Beinert, R.; and Bresch, J. 2025a. Maxnormalized Radon cumulative distribution transform for limited data classification. In International Conference on Scale Space and Variational Methods in Computer Vision, 241–254. Springer. Beckmann, M.; Beinert, R.; and Bresch, J. 2025b. Normalized Radon cumulative distribution transforms for invariance and robustness in optimal transport based image classification. arXiv:2506.08761. Beier, F.; and Beinert, R. 2025. Tangential fixpoint iterations for Gromov–Wasserstein barycenters. SIAM Journal on Imaging Sciences, 18(2): 1058–1100. Beier, F.; Beinert, R.; and Steidl, G. 2022. On a linear Gromov–Wasserstein distance. IEEE Transactions on Image Processing, 31: 7292–7305. Beier, F.; Beinert, R.; and Steidl, G. 2023. Multi-marginal Gromov–Wasserstein transport and barycentres. Information and Inference: A Journal of the IMA, 12(4): 2753–2781. Beier, F.; Piening, M.; Beinert, R.; and Steidl, G. 2025. Joint metric space embedding by unbalanced pptimal transport with Gromov–Wasserstein marginal penalization. In Proceedings of ICML’25. OpenReview.net. Beinert, R.; Heiss, C.; and Steidl, G. 2023. On assignment problems related to Gromov—Wasserstein distances on the real line. SIAM Journal on Imaging Sciences, 16(2): 1028– 1032. Bogo, F.; Romero, J.; Loper, M.; and Black, M. J. 2014. FAUST: Dataset and evaluation for 3D mesh registration. In Proceedings of CVPR’14. IEEE. Bollob´as, B. 1998. Random Graphs. Cambridge: Cambridge University Press. Bonet, C.; Drumetz, L.; and Courty, N. 2025. Sliced-Wasserstein distances and flows on Cartan-- Hadamard manifolds. Journal of Machine Learning Research, 26(32): 1–76. Bonet, C.; Vauthier, C.; and Korba, A. 2025. Flowing datasets with Wasserstein over Wasserstein gradient flows. In Proceedings of ICML’25. OpenReview.net. Bonneel, N.; Rabin, J.; Peyr´e, G.; and Pfister, H. 2015. Sliced and Radon Wasserstein barycenters of measures. Journal of Mathematical Imaging and Vision, 51: 22–45. Bonnotte, N. 2013. Unidimensional and Evolution Methods for Optimal Transportation. Ph.D. thesis, Universit´e Paris Sud–Paris XI, Orsay, France. PhD Thesis.

Chowdhury, S.; and M´emoli, F. 2019. The Gromov– Wasserstein distance between networks and stable network invariants. Information and Inference: A Journal of the IMA, 8(4): 757–787. Chowdhury, S.; Miller, D.; and Needham, T. 2021. Quantized Gromov–Wasserstein. In Proceedings of ECML PKDD’21, 811–827. Springer. Cover, T. M.; and Hart, P. E. 1967. Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1): 21–27. Delon, J.; and Desolneux, A. 2020. A Wasserstein-type distance in the space of Gaussian mixture models. SIAM Journal on Imaging Sciences, 13(2): 936–970. Dukler, Y.; Li, W.; Lin, A.; and Mont´ufar, G. 2019. Wasserstein of Wasserstein loss for learning generative models. In Proceedings of ICML’19, volume 97 of Proceedings of Machine Learning Research, 1716–1725. PMLR. Flamary, R.; Courty, N.; Gramfort, A.; Alaya, M. Z.; Boisbunon, A.; Chambon, S.; Chapel, L.; Corenflos, A.; Fatras, K.; Fournier, N.; Gautheron, L.; Gayraud, N. T. H.; Janati, H.; Rakotomamonjy, A.; Redko, I.; Rolet, A.; Schutz, A.; Seguy, V.; Sutherland, D. J.; Tavenard, R.; Tong, A.; and Vayer, T. 2021. POT: Python optimal transport. Journal of Machine Learning Research, 22(78): 1–8. Software available at https://pythonot.github.io/. Gray, A. 2004. Tubes. Basel: Birkh¨auser, 2nd edition. Grohe, M.; and Schweitzer, P. 2020. The graph isomorphism problem. Communications of the ACM, 63(11): 128–134. Hagberg, A. A.; Schult, D. A.; and Swart, P. J. 2008. Exploring network structure, dynamics, and function using NetworkX. In Varoquaux, G.; Vaught, T.; and Millman, J., eds., Proceedings of SciPy’08, 11–15. Curvenote. Hertrich, J.; Jahn, T.; and Quellmalz, M. 2025. Fast summation of radial kernels via QMC slicing. In Proceedings of the ICLR’25. OpenReview.net. Hertrich, J.; Wald, C.; Altekr¨uger, F.; and Hagemann, P. 2024. Generative sliced MMD flows with Riesz kernels. In Proceedings of the ICLR’24. OpenReview.net. Jin, H.; Yu, Z.; and Zhang, X. 2022. Orthogonal Gromov– Wasserstein Discrepancy with Efficient Lower Bound. In Procedings of UAI’22, volume 180 of Proceedings of Machine Learning Research, 917–927. PMLR. Kolouri, S.; Nadjahi, K.; Simsekli, U.; Badeau, R.; and Rohde, G. 2019. Generalized sliced Wasserstein distances. Advances in Neural Information Processing Systems, 32. Kolouri, S.; Park, S. R.; and Rohde, G. K. 2016. The Radon cumulative distribution transform and its application to image classification. IEEE Transactions on Image Processing, 25(2): 920–934. M´emoli, F. 2011. Gromov–Wasserstein distances and the metric approach to object matching. Foundations of Computational Mathematics, 11: 417–487. M´emoli, F.; and Needham, T. 2022. Distance distributions and inverse problems for metric measure spaces. Studies in Applied Mathematics, 149(4): 943–1001.

24835

<!-- Page 9 -->

Nadjahi, K.; Durmus, A.; Chizat, L.; Kolouri, S.; Shahrampour, S.; and Simsekli, U. 2020. Statistical and topological properties of sliced probability divergences. In Advances in Neural Information Processing Systems, volume 33, 15657– 15669. Curran Associates. Nadjahi, K.; Vialard, F.-X.; and Peyr´e, G. 2021. Fast Approximation of the Sliced-Wasserstein distance Using concentration of random projections. In International Conference on Machine Learning (ICML), volume 139 of Proceedings of Machine Learning Research, 7946–7956. PMLR. Nguyen, D. H.; and Tsuda, K. 2023. On a linear fused Gromov–Wasserstein distance for graph structured data. Pattern Recognition, 138: 109351. Nguyen, K.; Bariletto, N.; and Ho, N. 2024. Quasi-Monte Carlo for 3D Sliced Wasserstein. In Proceedings of the ICLR’24. OpenReview.net. Nguyen, K.; Nguyen, H.; Pham, T.; and Ho, N. 2025. Lightspeed geometric dataset distance via sliced optimal transport. In Proceedings of ICML’25. OpenReview.net. Peyr´e, G.; and Cuturi, M. 2019. Computational optimal transport: with applications to data science. Foundations and Trends® in Machine Learning, 11(5-6): 355–607. Peyr´e, G.; Cuturi, M.; and Solomon, J. 2016. Gromov– Wasserstein averaging of kernel and distance matrices. In Proceedings of ICML’16, volume 48 of Proceedings of Machine Learning Research, 2664–2672. PMLR. Piening, M.; and Beinert, R. 2025a. A novel sliced fused Gromov–Wasserstein distance. arXiv:2508.02364. Piening, M.; and Beinert, R. 2025b. Slicing the Gaussian mixture Wasserstein distance. arXiv:2504.08544. Quellmalz, M.; Beinert, R.; and Steidl, G. 2023. Sliced optimal transport on the sphere. Inverse Problems, 39(4): 044003. Rux, N.; Quellmalz, M.; and Steidl, G. 2025. Slicing of radial functions: a dimension walk in the Fourier space. Sampling Theory, Signal Processing, and Data Analysis, 23(1): 1–40. Sato, R.; Cuturi, M.; Yamada, M.; and Kashima, H. 2020. Fast and robust comparison of probability measures in heterogeneous spaces. arXiv:2002.01615. Scetbon, M.; Klein, M.; Palla, G.; and Cuturi, M. 2023. Unbalanced low-rank optimal transport solvers. In Advances in Neural Information Processing Systems, volume 36, 52312– 52325. Curran Associates. Scetbon, M.; Peyr´e, G.; and Cuturi, M. 2022. Linear-time Gromov-–Wasserstein distances using low-rank couplings and costs. In Proceedings of ICML’22, volume 162 of Proceedings of Machine Learning Research, 19347–19365. PMLR. Shervashidze, N.; Schweitzer, P.; van Leeuwen, E. J.; Mehlhorn, K.; and Borgwardt, K. 2011. Weisfeiler–Lehman graph kernels. Journal of Machine Learning Research, 12: 2539–2561. Sullivan, B.; and Kaszynski, A. 2019. PyVista: 3D plotting and mesh analysis through a streamlined interface for the

Visualization Toolkit (VTK). Journal of Open Source Software, 4(37): 1450. Sumner, R. W.; and Popovi´c, J. 2004. Mesh data from deformation transfer for triangle meshes. Available online at http://people.csail.mit.edu/sumner/research/ deftransfer/data.html. Accessed: 2025-06-03. Tanguy, E.; Flamary, R.; and Delon, J. 2025. Properties of discrete sliced Wasserstein losses. Mathematics of Computation, 94(353): 1411–1465. Vayer, T.; Chapel, L.; Flamary, R.; Tavenard, R.; and Courty, N. 2019. Sliced Gromov–Wasserstein. In Advances in Neural Information Processing Systems, volume 32, 10525– 10535. Curran Associates. Correction: arxiv:1905.10124. Vayer, T.; Chapel, L.; Flamary, R.; Tavenard, R.; and Courty, N. 2020a. Fused Gromov–Wasserstein distance for structured objects. Algorithms, 13(9): 212. Vayer, T.; Redko, I.; Flamary, R.; and Courty, N. 2020b. CO-optimal transport. In Advances in Neural Information Processing Systems, volume 33, 17559–17570. Curran Associates. Villani, C. 2003. Topics in Optimal Transportation. Providence, RI: American Mathematical Society. Watts, D. J.; and Strogatz, S. H. 1998. Collective dynamics of ’small-world’ networks. Nature, 393(6684): 440–442. Weitkamp, C. A. 2022. Gromov–Wasserstein Distances and their Lower Bounds. Doctoral thesis, Georg-August- Universit¨at G¨ottingen. Weitkamp, C. A.; Proksch, K.; Tameling, C.; and Munk, A. 2024. Distribution of distances based object matching: asymptotic inference. Journal of the American Statistical Association, 119(545): 538–551.

24836
