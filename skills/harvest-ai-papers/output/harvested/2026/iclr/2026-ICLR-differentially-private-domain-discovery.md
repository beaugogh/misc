---
title: "Differentially Private Domain Discovery"
source_url: https://iclr.cc/virtual/2026/oral/10006582
paper_pdf_url: https://arxiv.org/pdf/2603.14016v1
venue: ICLR
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Differentially Private Domain Discovery

<!-- Page 1 -->

Published as a conference paper at ICLR 2026

MISSING MASS FOR DIFFERENTIALLY PRIVATE DOMAIN DISCOVERY

Travis Dick Google Research

Matthew Joseph Google Research

Vinod Raman ∗ Department of Statistics University of Michigan, Ann Arbor

## ABSTRACT

We study several problems in differentially private domain discovery, where each user holds a subset of items from a shared but unknown domain, and the goal is to output an informative subset of items. For set union, we show that the simple baseline Weighted Gaussian Mechanism (WGM) has a near-optimal ℓ1 missing mass guarantee on Zipfian data as well as a distribution-free ℓ∞missing mass guarantee. We then apply the WGM as a domain-discovery precursor for existing known-domain algorithms for private top-k and k-hitting set and obtain new utility guarantees for their unknown domain variants. Finally, experiments demonstrate that all of our WGM-based methods are competitive with or outperform existing baselines for all three problems.

## INTRODUCTION

Modern data analysis often requires working in data domains like queries, reviews, and purchase histories that are a priori unknown or impractically large (e.g., the set of all strings up to a fixed length). For these datasets, domain discovery is a critical first step for efficient downstream applications. Differential privacy (Dwork et al., 2006) (DP) enables privacy-preserving analysis of sensitive data, but it complicates domain discovery.

In the basic problem of set union, for example, each user has a set of items, and the goal is simply to output as many of these items as possible. This is a necessary step before further analysis, so set union (also known as key selection or partition selection) is a core component of several industrial (Wilson et al., 2020; Rogers et al., 2021; Amin et al., 2023) and open source (OpenDP, 2025) DP frameworks. For similar reasons, there are by now many DP set union algorithms in the literature. However, there are almost no provable utility guarantees (see Section 1.1). This makes it difficult to understand how well existing algorithms work, or how much they can be improved.

Our Contributions. We prove utility guarantees for several problems in DP domain discovery. First, by reframing DP set union in terms of mass instead of cardinality (i.e., the fraction of all items recovered, rather than the number of unique items), we prove utility guarantees for the simple and scalable Weighted Gaussian Mechanism (Gopi et al., 2020) (WGM). We first show that the WGM has near-optimal ℓ1 missing mass on Zipfian data (Theorem 3.3). We then prove a similar but distribution-free ℓ∞missing mass guarantee (Theorem 3.6).

Next, we build on these results by considering unknown domain variants of top-k and k-hitting set and obtain further utility guarantees for simple algorithms that run WGM to compute a baseline domain and then run a standard known-domain algorithm afterward. Relying on Theorem 3.6 enables us to prove utility guarantees for both top-k (Theorem 4.3) and k-hitting set (Theorem 4.5).

Finally, we evaluate our algorithms against the existing state of the art on six real-world datasets from varied domains (Section 5). These experiments demonstrate that, in addition to their theoretical guarantees, our WGM-based methods obtain strong empirical utility.

∗Work done while interning at Google Research.

arXiv:2603.14016v1 [cs.CR] 14 Mar 2026

<!-- Page 2 -->

Published as a conference paper at ICLR 2026

## 1.1 RELATED WORK

DP Set Union. Early work by Korolova et al. (2009) introduced the core idea of collecting a bounded number of items per user, constructing a histogram of item counts, and releasing items whose noisy counts exceed a carefully chosen threshold. Desfontaines et al. (2022) developed an optimal algorithm for the restricted setting where each user contributes a single item. Gopi et al. (2020) adapted noisy thresholding in the Weighted Gaussian Mechanism (WGM) by scaling contributions to unit ℓ2 norm. Swanberg et al. (2023) investigated a repeated version of WGM, and Chen et al. (2025) further built on these ideas by incorporating adaptive weighting to determine user contributions, and proved that the resulting algorithm dominates the WGM (albeit by a small margin, empirically). A separate line of work has studied sequential algorithms that attempt to choose user contributions adaptively, obtaining better empirical utility at the cost of scalability (Gopi et al., 2020; Carvalho et al., 2022).

We note that, as the utility results of Desfontaines et al. (2022) and Chen et al. (2025) are stated relative to other algorithms, our work is, to the best of our knowledge, the first to prove absolute utility guarantees for DP set union.

DP Top-k. While several algorithms have been proposed for retrieving a dataset’s k most frequent items given a known domain (Bhaskar et al., 2010; McKenna & Sheldon, 2020; Qiao et al., 2021; Gillenwater et al., 2022), to the best of our knowledge only Durfee & Rogers (2019) provide an algorithm for the unknown domain setting (see discussion in Section 5.2). They also provide a utility guarantee in terms of what Gillenwater et al. (2022) call k-relative error, which bounds the gap between the smallest-count output item and the kth highest-count item. In contrast, we prove a utility result for the more stringent notion of missing mass (see discussion in Section 4.1).

DP k-Hitting Set. In k-hitting set, the objective is to output a set of k items that maximizes the number of users whose subset intersects with it. This problem can also be viewed as an instance of cardinality-constrained submodular maximization. Previous works on private submodular maximization by Mitrovic et al. (2017) and Chaturvedi et al. (2021) establish approximation guarantees in the known-domain setting. However, they are not directly applicable when the domain is unknown.

PRELIMINARIES

## 2.1 NOTATION

Let X denote a countable universe of items. A dataset W of size n is a collection of subsets {Wi}i∈[n] where Wi ⊂X and |Wi| < ∞. We will use N = P i |Wi| to denote the total number of items across all users in the dataset and M:= | S i Wi| to denote the number of unique items across W. For an element x ∈S i Wi, we let N(x):= P i 1{x ∈Wi} denote its frequency. For a number r ∈[M], we use N(r) to denote the r’th largest frequency after sorting {N(x)}x∈S i Wi in decreasing order. We will use N(0, σ2) to denote a mean-zero Gaussian distribution with standard deviation σ. Finally, we use the notation ˜Ok (·) to suppress poly-logarithmic factors in k and likewise for ˜Ωk and ˜Θk.

## 2.2 DIFFERENTIAL PRIVACY

We say that a pair of datasets W, W ′ are neighboring if W ′ is the result of adding or removing a single user from W. In this work, we consider randomized algorithms A: (2X)⋆→2X which map a dataset W to a random subset S ⊆X. We say that A is (ϵ, δ)-differentially private if its distribution over outputs for two neighboring datasets are “close.”

Definition 2.1 (Dwork et al. (2006)). A randomized algorithm A is (ϵ, δ)-differentially private if for all pairs of neighboring datasets W, W ′, and all events Y ⊆2X,

PS∼A(W) [S ∈Y ] ≤eϵPS′∼A(W ′) [S′ ∈Y ] + δ.

We only consider approximate differential privacy (δ > 0) since we will often require that A(W) ⊆ S i Wi, which precludes pure differential privacy (δ = 0).

<!-- Page 3 -->

Published as a conference paper at ICLR 2026

## 2.3 PRIVATE DOMAIN DISCOVERY AND MISSING MASS

In private domain discovery, we are given a dataset W of n users, each of which holds a subset of items Wi ⊆X such that |Wi| < ∞and X is unknown. Given W, our is goal is to extract an informative subset S ⊆S i Wi that captures the “domain” of W while preserving differential privacy. In this paper, we often measure quality in terms of the missing mass of S. Definition 2.2. Given dataset W and output set S, the missing mass of S with respect to W is

MM(W, S):=

X x∈S i Wi\S

N(x)

N.

Smaller values of MM(W, S) indicate the that S better captures the high-frequency items in S i Wi. A useful perspective to the MM is that it is the ℓ1 norm of the vector (N(x)/N)x∈S i Wi\S. This view yields a generalization of the MM objective by taking the p’th norm of the vector of missing frequencies. That is, for p ≥0, define

MMp(W, S):=

N(x)

N x∈S i Wi\S p

(1)

where || · ||p: R⋆→R denotes the ℓp norm. The usual missing mass objective corresponds to setting p = 1. However, it is also meaningful to set p̸ = 1. For example, when p = ∞, the objective corresponds to minimizing the maximum missing mass. When p = 0, we recover the cardinality-based objective studied by existing work (see Related Work).

PRIVATE SET UNION

In general, we consider algorithms that satisfy the following “soundness” property: an item only appears in the output if it also appears in the input dataset. Assumption 1. For every algorithm A: (2X)⋆→2X and dataset W, we require A(W) ⊆S i Wi.

Assumption 1 is standard across works in the unknown domain setting. However, even with this assumption, it is difficult to obtain a meaningful trade-off between privacy and missing mass without assumptions on W.

To see why, fix some n ∈N, and consider the singleton dataset W where each user has a single, unique item, such that Wi = {xi} and xi̸ = xj for i̸ = j. Fix j ∈[n] and consider the neighboring dataset W ′ obtained by removing Wj from W. Since we require that A(W ′) ⊆S i W ′ i, we have that P [xj ∈A(W ′)] = 0. Since A is (ϵ, δ)-differentially private, we know that P [xj ∈A(W)] ≤δ. Since j ∈[n] was picked arbitrarily, we know that this is true for all j ∈[n] and hence, ES∼A(W) [MM(A, S)] ≥1 −δ. As δ is usually picked to be o

1 n

, it is not possible to significantly minimize MM for these datasets.

Fortunately, in practice, these sorts of pathological datasets are rare. Instead, datasets often exhibit what is known as Zipf’s or Power law (Zipf, 1949; Gabaix, 1999; Adamic & Huberman, 2002; Piantadosi, 2014). This means that the frequency of items in a dataset exhibit a polynomial decay. Hence, one natural way of measuring the complexity of W is by how “Zipfian” it is.

Definition 3.1 ((C, s)-Zipfian). Let C ≥1 and s ≥0. A dataset W is (C, s)-Zipfian if

N(r)

N ≤C rs for all r ∈[M], where N(r) is the r’th largest frequency and N is the total number of items in W.

In light of the hardness above, we first restrict our attention to datasets that are (C, s)-Zipfian for s > 1. When s ≤1, the hard dataset previously outlined becomes a valid Zipfian dataset. We note that this restriction only impacts how we define the utility guarantee of the algorithm, and not its privacy guarantee; differential privacy is still measured with respect to the worst-case pair of neighboring datasets.

As s increases, the empirical mass gets concentrated more and more at the highest frequency item. Accordingly, any upper bound on missing mass should ideally decay as s increases. Another important property of (C, s)-Zipfian datasets W is that they restrict the size of any individual set Wi. Lemma 3.1, whose proof is in Appendix C.1, makes this precise.

<!-- Page 4 -->

Published as a conference paper at ICLR 2026

Lemma 3.1. Let W be any (C, s)-Zipfian dataset. Then, maxi |Wi| ≤(CN)1/s.

The rest of this section uses these two properties of Zipfian-datasets to obtain high-probability upper bounds on the missing mass. Our main focus will be on a simple mechanism used in practice known as the Weighted Gaussian Mechanism (WGM) (Gopi et al., 2020).

## 3.1 THE WEIGHTED GAUSSIAN MECHANISM

The WGM is parameterized by a noise-level σ > 0, threshold T ≥1, and user contribution bound ∆0 ≥1. Given a dataset W, the WGM operates in three stages. In the first stage, the WGM constructs a random dataset by subsampling without replacement from each user’s itemset to ensure that each user has at most ∆0 items. In the second, stage the WGM constructs a weighted histogram over the items in the random dataset. In the third stage, the WGM computes a noisy weighted histogram by adding mean-zero Gaussian noise with standard deviation σ to each weighted count. Finally, the WGM returns those items whose noisy weighted counts are above the threshold T. Pseudocode appears in Algorithm 1.

## Algorithm

## 1 Weighted Gaussian Mechanism Input:

Dataset W, noise level σ, threshold T, and user contribution bound ∆0.

1 Construct random dataset f W such that for every i ∈[n], f Wi ⊆Wi is a random sample (without replacement) of size min{∆0, |Wi|} from Wi.

## 2 Compute weighted histogram eH: S

i f Wi →R such that, for each x ∈S i f Wi, eH(x) = n X i=1

1

|f Wi|

!1/2

1{x ∈f Wi}.

3 For each x ∈S i f Wi, sample Zx ∼N(0, σ2) and compute noisy eH′(x):= eH(x) + Zx.

4 Keep items with large noisy weighted counts S = n x ∈S i f Wi: eH′(x) ≥T o

. Output: S

The following theorem from Gopi et al. (2020) verifies the approximate DP guarantee for the WGM. Theorem 3.2 (Theorem 5.1 (Gopi et al., 2020)). For every ∆0 ≥1, ϵ > 0 and δ ∈(0, 1), if σ, T > 0 are chosen such that

Φ

1

2σ −ϵσ

−eϵΦ

−1

2σ −ϵσ

≤δ

2 and T ≥ max 1≤t≤∆0

1 √ t + σΦ−1

1 −δ 2

1 t!!

then the WGM run with (σ, T) and input ∆0 is (ϵ, δ)-differentially private.

In Appendix C.2.1, we prove that the smallest choice of σ and T to satisfy the constraints in Theorem 3.2 gives that σ = Θ

1 ϵ p log(1/δ)

and T = Θ max n σ q log

∆0 δ

, 1 o

=

˜Θδ,∆0(max{σ, 1}). This result will be useful for deriving asymptotic utility guarantees involving the WGM.

## 3.2 UPPER BOUNDS ON MISSING MASS

Our main result in this section is Theorem 3.3, which provides a high-probability upper bound on the missing mass for the WGM in terms of the Zipfian parameters of the input dataset. Theorem 3.3. For every s > 1, C ≥1 and (C, s)-Zipfian dataset W, if the WGM is run with noise parameter σ > 0, threshold T ≥1, and user contribution bound ∆0 ≥1, then with probability at least 1 −β over S ∼WGM(W, ∆0), we have that

MM(W, S) = ˜Oβ,C,N

C

1 s s −1 maxi |Wi|

N√q⋆ s−1 s

(T + σ)

s−1 s

!

.

where q⋆:= min{maxi |Wi|, ∆0}.

<!-- Page 5 -->

Published as a conference paper at ICLR 2026

Note that in Theorem 3.3 the missing mass decays as the total number of items N grows. Moreover, as C decreases or s increases, the upper bound on missing mass decreases when N is sufficiently large compared to σ and T. This matches our intuition, as decreasing C and increasing s results in datasets that exhibit faster decays in item frequencies so relatively more of the mass is contained in high-mass items.

The proof of Theorem 3.3 relies on three helper lemmas. Lemma C.2 provides an upper bound on the missing mass due to the subsampling stage. Lemma C.3 guarantees that a high-frequency item in the original dataset will remain high-frequency in the subsampled dataset. Finally, Lemma C.4 provides a high-probability upper bound on the frequency of items that are missed by the WGM during the thresholding step. We provide the full proof in Appendix C.2.2.

Theorem 3.3 bounds the overall missing mass of the WGM mechanism. As corollary, note that if ∆0 ≥maxi |Wi| then the missing mass contributed by the subsampling step vanishes. By Theorem 3.2 and Lemma C.1, for every user contribution bound ∆0 ≥1, we need to pick σ = Θ

1 ϵ p log(1/δ)

and T = ˜Θ∆0,δ(max{σ, 1}) to to achieve (ϵ, δ)-differential privacy. Substituting these values into Theorem 3.3 gives the following corollary. Corollary 3.4. In the setting of Theorem 3.3, if we choose the minimum σ and T to ensure (ϵ, δ)-DP, then with probability at least 1 −β, we have that

MM(W, S) ≤˜Oβ,δ,∆0,C,N

C

1 s s −1 maxi |Wi| ϵ N√q⋆ s−1 s!

, where q⋆= min{∆0, maxi |Wi|}.

Corollary 3.4 shows that the error due to subsampling can dominate the missing mass. Accordingly, one should aim to set ∆0 as close as possible to maxi |Wi|. In fact, if one has apriori public knowledge of maxi |Wi|, then one should set ∆0 = maxi |Wi|. By Lemma 3.1, for any (C, s)-Zipfian dataset W, maxi |Wi| ≤(CN)1/s and hence the loss due to setting ∆0 will only be logarithmic in N. However, Corollary 3.4 omits logarithmic factors in ∆0, so one should avoid ∆0 ≫maxi |Wi|.

Theorem 3.5, whose proof is in Appendix D.1, shows that the dependence of ϵ and N in our upper bound from Corollary 3.4 can be tight. Theorem 3.5. Let A be any (ϵ, δ)-differentially private algorithm satisfying Assumption 1. For every s > 1, C ≥1, there exists a (C, s)-Zipfian dataset W ⋆such that

ES∼A(W ⋆) [MM(W ⋆, S)] = Ω

C1/s s −1

1 ϵN

(s−1)/s ln

1 + eϵ −1 2δ

(s−1)/s!

.

The proof of Theorem 3.5 exploits Assumption 1 by showing that any private algorithm that satisfies Assumption 1 cannot output low-frequency items with high-probability. We end this section by noting that our proof technique in Theorem 3.3 can also give us bounds on the ℓ∞missing mass (see Equation 1). Note that unlike Theorem 3.3, Theorem 3.6, whose proof is in Appendix C.2.3, does not require the dataset to be Zipfian. Theorem 3.6. Let W be any dataset. For every ϵ > 0, δ ∈(0, 1), and user contribution bound

∆0 ≥1, picking σ = Θ

1 ϵ p log(1/δ)

and T = ˜Θ∆0,δ(max{σ, 1}) gives that the WGM is

(ϵ, δ)-differentially private and with probability at least 1 −β over S ∼WGM(W, ∆0), we have

MM∞(W, S) ≤˜O∆0,δ,β maxi |Wi| ϵ N√q⋆

, where q⋆= min{∆0, maxi |Wi|}.

Upper bounds on the ℓ∞norm missing mass will be useful for deriving guarantees for the top-k selection (Section 4.1) and k-hitting set (Section 4.2) problems.

## 4 APPLYING THE WEIGHTED GAUSSIAN MECHANISM

This section applies WGM to construct unknown domain algorithms for top-k and k-hitting set. For both problems, we spend half of the overall privacy budget running WGM to obtain a domain D, and

<!-- Page 6 -->

Published as a conference paper at ICLR 2026 then spend the other half of the privacy budget running a known-domain private algorithm, using domain D, for the problem in question. By basic composition, the overall mechanism satisfies the desired privacy budget. Pseudocode for this approach is given in Algorithm 2.

## Algorithm

## 2 Meta Algorithm Input:

Dataset W, noise-level and threshold (σ, T), output size k, user contribution bound ∆0 ≥1, known-domain mechanism B

5 Let D ←WGM(W, ∆0) be the output of WGM with noise-level and threshold (σ, T) and input ∆0

6 Let S ←B(W, D, k) be the output of B on input W and domain D Output: S

In the next two subsections, we introduce the top-k selection and k-hitting set problems, summarize existing known-domain algorithms, and provide the specification of all algorithmic parameters. An important difference between the results in this section and that of Section 3, is that by using MM∞ bounds, we no longer require our dataset to be Zipfian in order to get meaningful guarantees.

## 4.1 PRIVATE TOP-k SELECTION

In the DP top-k selection problem, we are given some k ∈N and our goal is to output, in decreasing order, the k largest frequency items in a dataset W. Various loss objective have been considered for this problem, but we focus on missing mass.

Definition 4.1. For a dataset W, k ∈N, q ≤k and ordered sequence of domain elements S = (x1,..., xq), we denote the top-k missing mass by

MMk(W, S) =

Pk i=1 N(i) −Pq i=1 N(xi) N.

We let the sequence S have length q ≤k because we will allow our mechanisms to output less than k items, which will be crucial for obtaining differential privacy when the domain X is unknown. Note that MM(W, S) = MMk(W, S) if one takes k = | S i Wi|. As before, our objective is to design an approximate DP mechanism B which outputs a sequence S ⊆S i Wi of size at most k that minimizes MMk(W, S) with high probability.

To adapt Algorithm 2 to top-k, we need to specify a known-domain private top-k algorithm. We use the peeling exponential mechanism (see Algorithm 3) for its simplicity, efficiency, and tight privacy composition. Its privacy and utility guarantees appear in Lemmas 4.1 and 4.2 respectively.

## Algorithm

## 3 Peeling Exponential Mechanism Input:

Dataset W, domain D, noise-level λ, output size k ≤|D|

1 Let N(x) = Pn i=1 1{x ∈Wi} for x ∈D.

2 Let ˜N(x) = N(x) + Zx for x ∈D where Zx ∼Gumbel(λ). Output: Ordered sequence (x1,..., xk) such that ˜N(xi) = ˜N(i) for all i ∈[k].

Lemma 4.1 (Corollary 4.1 (Durfee & Rogers, 2019)). For every ϵ > 0, δ ∈(0, 1) and k ≥1, if λ = ˜Oδ

√ k ϵ

, then Algorithm 3 is (ϵ, δ)-differentially private.

Lemma 4.2. For every dataset W, domain D, λ ≥1 and k ≤|D|, if Algorithm 3 is run with noise-level λ, then with probability 1 −β over its output S, we have that

1 N



 X x∈Tk(W,D)

N(x) −

X x∈S

N(x)



≤O kλ

N log |D| β

, where Tk(W, D) ⊆D is the true set of top-k most frequent items in D.

We provide the exact λ to achieve (ϵ, δ)-differential privacy for Lemma 4.1 in Lemma B.1. The proof of Lemma 4.2 is standard, relies on Gumbel concentration inequalities, and appears in Appendix

<!-- Page 7 -->

Published as a conference paper at ICLR 2026

C.3.Similar upper bounds for other performance metrics have also been derived (Bafna & Ullman, 2017). With Lemmas 4.2 and 4.1 in hand, using the same choice of (σ, T) as in Theorem 3.2 for WGM yields our main result. The proof of Theorem 4.3 can be found in Appendix C.3. Theorem 4.3. Fix ϵ > 0, δ ∈(0, 1), and user contribution bound ∆0 ≥1. For every dataset W and k ≥1, if one picks σ = Θ

1 ϵ p log(1/δ)

, T = ˜Θ∆0,δ/2(max{σ, 1}) from Theorem 3.2, and λ = ˜Θδ/2

√ k ϵ from Lemma 4.1, then Algorithm 2, run with Algorithm 3, is (ϵ, δ)-differentially private and with probability 1 −β, its output S satisfies

MMk(W, S) ≤˜Oβ,δ,∆0 k N maxi |Wi| ϵ√q⋆ +

√ k log(M)

ϵ

!!

, where q⋆:= min{∆0, maxi |Wi|}.

We end this section by proving that a linear dependence on k ϵ on the top-k missing mass is unavoidable for algorithms satisfying Assumption 1 when ϵ ≤1. Corollary 4.4. Let ϵ ≤1 and δ ∈(0, 1). Let A be any (ϵ, δ)-differentially private algorithm satisfying Assumption 1. Then, for every k ≥1, there exists a dataset W such that

ES∼A(W,k)

h

MMk(W, S)

i

≥˜Ωδ k ϵN

.

The proof of Corollary 4.4 is in Appendix D.2 and is largely a consequence of Lemma D.1, which was used to prove the lower bound for set union (Theorem 3.5).

## 4.2 PRIVATE k-HITTING SET

In the k-hitting set problem, our goal is to output a set S of items of size at most k which intersects as many user subsets as possible, which is useful for data summarization and feature selection (Mitrovic et al., 2017). More precisely, our objective is to design an approximate DP mechanism which maximizes the number of hits Hits(W, S):= Pn i=1 1{S ∩Wi̸ = ∅}. Since this problem is also NP-hard without privacy concerns (Karp, 1972), we will measure performance relative to the optimal solution, i.e., show that with high probability, our algorithm output S satisfies

Hits(W, S) ≥γ · Opt(W, k) −err(ϵ, δ, k)

where Opt(W, k):= arg maxS⊆X,|S|≤k Hits(W, S) is the optimal value, err(ϵ, δ, k) is an additive error term that depends on problem specific parameters, and γ ∈(0, 1) is the approximation factor.

Like our algorithm for top-k selection, our mechanism for the k-hitting problem will follow the general structure of Algorithm 2. We will take the known-domain algorithm B to be the privatized version of the greedy algorithm for submodular maximization, as in Algorithm 1 from Mitrovic et al. (2017). This mechanism repeatedly runs the exponential mechanism (equivalently the Gumbel mechanism) to pick an item that hits a large number of users. After each iteration, we remove all users who contain the item output in the previous round and continue until we either have output k items, run out of items, or run out of users, and return the overall set of items. We call this algorithm the User Peeling Mechanism and its pseudo-code is given in Algorithm 4 in Appendix C.4.

By combining this with the same WGM choice of (σ, T) as in Theorem 3.2 for the first step of Algorithm 2, we get the main result of this section. Theorem 4.5. Fix ϵ > 0 and δ ∈(0, 1). For every dataset W, k ≥1, and user contribution bound ∆0, if one picks σ = Θ

1 ϵ p log(1/δ)

, T = ˜Θ∆0,δ/2(max{σ, 1}) from Theorem 3.2, and λ = ˜Θδ/2

1 ϵ

√ k from Lemma 4.1, then Algorithm 2, run with Algorithm 4, is (ϵ, δ)-differentially private and with probability 1 −β, its output S satisfies

Hits(W, S) ≥

1 −1 e

Opt(W, k) −˜Oβ,δ,∆0 k · maxi |Wi| ϵ√q⋆ + k3/2 ϵ log (Mk)

, where q⋆:= min{∆0, maxi |Wi|} and M = | S i Wi|.

<!-- Page 8 -->

Published as a conference paper at ICLR 2026

Theorem 4.5, proved in Appendix C.4, gives that if k is not very large (i.e., ln(Mk)

ln(M) ≤maxi p

|Wi|), then with high probability, the additive sub-optimality gap is on the order of

˜O∆0,δ,β,k k3/2 · maxi |Wi| · log(M)

ϵ√q⋆

.

When |X| ≫M, this provides an improvement over Theorem 1 in Mitrovic et al. (2017) whose guarantee is in terms log(|X|) and not log(M).

As in the lower bound proof for top-k selection, we again rely on the work behind Theorem 3.5 to show that one must lose k ϵ from the optimal value by restricting the algorithm A to output a subset of S i Wi.

Corollary 4.6. Let ϵ ≤1, δ ∈(0, 1) and A be any (ϵ, δ)-differentially private algorithm satisfying Assumption 1. Then, for every k ≥1, there exists a dataset W such that

ES∼A(W,k) [Hits(W, S)] ≥Opt(W, k) −˜Ωδ k ϵ

.

## 5 EXPERIMENTS

We empirically evaluate our methods on six real-life datasets spanning diverse settings. Informally, Reddit (Gopi et al., 2020), Amazon Games (Ni et al., 2019), and Movie Reviews (Harper & Konstan, 2015) are “large”, while Steam Games (Steam, 2025), Amazon Magazine (Ni et al., 2019), and Amazon Pantry (Ni et al., 2019) are “small” (see Appendix E for details). All experiments use a total privacy budget of (1, 10−5)-DP; additional experiments using (0.1, 10−5)-DP appear in Appendix F, but are not significantly qualitatively different. Dataset processing and experiment code can be found in the Supplement.

## 5.1 SET UNION

Datasets. We evaluate the WGM and baselines on all six datasets, relegating experiments on the small datasets to the Appendix F.1.1 for space.

Baselines. The baselines are the Policy Gaussian mechanism from Gopi et al. (2020) and the Policy Greedy mechanism from Carvalho et al. (2022), as these have obtained the strongest (though least scalable) performance in past work. As suggested in those papers, we set the policy hyperparameter α = 3 throughout.

Results. Figure 1 plots the average MM across 5 trials, for all three mechanisms as a function of ℓ0 bound ∆0 ∈{1, 50, 100, 150, 200, 300}. Across datasets, we find that the WGM obtains MM within 5% of that of the policy mechanisms, in spite of their significantly more intensive computation. This contrasts with previous empirical results for cardinality, where sequential methods often output ≈ 2X more items (see, e.g., Table 2 in Swanberg et al. (2023)). Plots for the small datasets (Appendix F.1.1) show a similar trend.

(a) Reddit (b) Amazon Games (c) Movie Reviews

**Figure 1.** Set Union MM as a function of ∆0. Note that lower is better.

![Figure extracted from page 8](2026-ICLR-differentially-private-domain-discovery/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICLR-differentially-private-domain-discovery/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICLR-differentially-private-domain-discovery/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Published as a conference paper at ICLR 2026

## 5.2 TOP-k

Datasets. All methods achieve near 0 top-k missing mass across all values of number of selected items k ∈{5, 10, 20, 50, 100, 200} on the three large datasets, as most mass is concentrated in a small number of heavy items. We therefore focus on the three small datasets.

Baselines. We compare our WGM-then-top-k mechanism to the limited-domain top-k mechanism from Durfee & Rogers (2019). Unlike our algorithm, the limited-domain mechanism has a hyperparameter ¯k. As such, for each k ∈{5, 10, 20, 50, 100, 200}, we take as baselines the limited-domain algorithm with ¯k ∈{k, 5k, 10k, ∞}. When ¯k < ∞, we set ∆0 = ∞for the limited-domain algorithm. Otherwise, when ¯k = ∞, we set ∆0 = 100 for the limited-domain algorithm, as recommended in Section 3 of Durfee & Rogers (2019).

Results. Figure 2 compares our method against the limited-domain method across different choices for k. Note that each line for the limited-domain method uses a different ¯k. We find that across all datasets, our method consistently obtains smaller top-k MM than all limited-domain baselines, and its advantage grows with k. Plots in Appendix F.2 demonstrate similar trends for a more stringent ℓ1 loss.

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 2.** Top-k MM as a function of k, using ∆0 = 100.

5.3 k-HITTING SET

Datasets. We use the same datasets as in the top-k experiments, for the same reason: a small number of items covers nearly all users in the large datasets.

Baselines. To the best of our knowledge, there are no existing private algorithm for the k-hitting set problem for unknown domains. Hence, we consider the following baselines: the non-private greedy algorithm and the private non-domain algorithm from Mitrovic et al. (2017) after taking S i Wi to be a public known-domain. Note that the latter baseline is not a valid private algorithm in the unknown domain setting since, in reality, S i Wi is private.

Results. Figure 3 plots the average number of users hit, along with its standard error across 5 trials, as a function of k ∈{5, 10, 20, 50, 100, 200}, fixing ∆0 = 100. We find that our method performs comparably with both baseline methods, neither of which is fully private. In particular, for the Steam Games and Amazon Magazine datasets, our method outperforms the known-domain private greedy algorithm that assumes public knowledge of S i Wi. This is because our method’s application of WGM for domain discovery produces a domain that is smaller than S i Wi while still containing high-quality items. This makes an easier problem for the peeling mechanism in the second step.

## 6 FUTURE DIRECTIONS

We conclude with some possible future research directions. First, our upper and lower bounds for top-k and k-hitting set do not match, so closing these gaps is a natural problem. Second, all of our methods enforce ℓ0 bounds by uniform subsampling without replacement from each user’s item set. Recent work by Chen et al. (2025) employs more involved and data-dependent subsampling strategies to obtain higher cardinality answers. Extending similar techniques to missing mass may be useful.

![Figure extracted from page 9](2026-ICLR-differentially-private-domain-discovery/page-009-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-differentially-private-domain-discovery/page-009-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICLR-differentially-private-domain-discovery/page-009-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 10 -->

Published as a conference paper at ICLR 2026

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 3.** Number of missed users as a function of k, using ∆0 = 100.

## REFERENCES

Lada A Adamic and Bernardo A Huberman. Zipf’s law and the Internet. Glottometrics, 2002.

Kareem Amin, Jennifer Gillenwater, Matthew Joseph, Alex Kulesza, and Sergei Vassilvitskii.

Plume: differential privacy at scale. In Privacy Engineering Practice and Respect (PEPR), 2023.

Mitali Bafna and Jonathan Ullman. The price of selection in differential privacy. In Conference on

Learning Theory, pp. 151–168. PMLR, 2017.

Raghav Bhaskar, Srivatsan Laxman, Adam Smith, and Abhradeep Thakurta. Discovering frequent patterns in sensitive data. In Knowledge Discovery and Data Mining (KDD), 2010.

Ricardo Silva Carvalho, Ke Wang, and Lovedeep Singh Gondara. Incorporating item frequency for differentially private set union. In Conference on Artificial Intelligence (AAAI), 2022.

Anamay Chaturvedi, Huy Le Nguyen, and Lydia Zakynthinou. Differentially private decomposable submodular maximization. In Conference on Artificial Intelligence (AAAI), 2021.

Justin Y Chen, Vincent Cohen-Addad, Alessandro Epasto, and Morteza Zadimoghaddam. Scalable

Private Partition Selection via Adaptive Weighting. In International Conference on Machine Learning (ICML), 2025.

Damien Desfontaines, James Voss, Bryant Gipson, and Chinmoy Mandayam. Differentially private partition selection. Privacy Enhancing Technologies Symposium (PETS), 2022.

David Durfee and Ryan M Rogers. Practical differentially private top-k selection with pay-what- you-get composition. Neural Information Processing Systems (NeurIPS), 2019.

Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. Calibrating noise to sensitivity in private data analysis. In Theory of Cryptography Conference (TCC), 2006.

Xavier Gabaix. Zipf’s law for cities: an explanation. The Quarterly Journal of Economics, 1999.

Jennifer Gillenwater, Matthew Joseph, Andres Munoz, and Monica Ribero Diaz. A Joint Expo- nential Mechanism For Differentially Private Top-k. In International Conference on Machine Learning (ICML), 2022.

Sivakanth Gopi, Pankaj Gulhane, Janardhan Kulkarni, Judy Hanwen Shen, Milad Shokouhi, and

Sergey Yekhanin. Differentially private set union. In International Conference on Machine Learning (ICML), 2020.

F. Maxwell Harper and Joseph A. Konstan. The MovieLens Datasets: History and Context. 2015.

RM Karp. Reducibility among combinatorial problems. Complexity of Computer Computations,

1972.

Aleksandra Korolova, Krishnaram Kenthapadi, Nina Mishra, and Alexandros Ntoulas. Releasing search queries and clicks privately. In International Conference on World Wide Web, 2009.

![Figure extracted from page 10](2026-ICLR-differentially-private-domain-discovery/page-010-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-differentially-private-domain-discovery/page-010-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 10](2026-ICLR-differentially-private-domain-discovery/page-010-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 11 -->

Published as a conference paper at ICLR 2026

Ryan McKenna and Daniel R Sheldon. Permute-and-flip: A new mechanism for differentially pri- vate selection. Neural Information Processing Systems (NeurIPS), 2020.

Marko Mitrovic, Mark Bun, Andreas Krause, and Amin Karbasi. Differentially private submod- ular maximization: Data summarization in disguise. In International Conference on Machine Learning (ICML), 2017.

Jianmo Ni, Jiacheng Li, and Julian McAuley. Justifying recommendations using distantly-labeled re- views and fine-grained aspects. In Empirical Methods in Natural Language Processing (EMNLP), 2019.

OpenDP. Privatizing histograms. https://docs.opendp.org/en/stable/ getting-started/examples/histograms.html, 2025.

Steven T Piantadosi. Zipf’s word frequency law in natural language: A critical review and future directions. Psychonomic bulletin & review, 2014.

Gang Qiao, Weijie Su, and Li Zhang. Oneshot differentially private top-k selection. In International

Conference on Machine Learning, pp. 8672–8681. PMLR, 2021.

Ryan Rogers, Subbu Subramaniam, Sean Peng, David Durfee, Seunghyun Lee, Santosh Kumar

Kancha, Shraddha Sahay, and Parvez Ahammad. LinkedIn’s Audience Engagements API: A Privacy Preserving Data Analytics System at Scale. Journal of Privacy and Confidentiality, 2021.

Steam. Steam games dataset. https://www.kaggle.com/datasets/tamber/ steam-video-games/data, 2025. Accessed: 2025-09-22.

Marika Swanberg, Damien Desfontaines, and Samuel Haney. DP-SIPS: A simpler, more scalable mechanism for differentially private partition selection. 2023.

Roman Vershynin. High-dimensional probability: An introduction with applications in data science.

Cambridge University Press, 2018.

Royce J Wilson, Celia Yuxin Zhang, William Lam, Damien Desfontaines, Daniel Simmons-

Marengo, and Bryant Gipson. Differentially Private SQL with Bounded User Contribution. 2020.

George Kingsley Zipf. Human behavior and the principle of least effort: An introduction to human ecology. Addison-Wesley Press, 1949.

A USEFUL CONCENTRATION INEQUALITIES

In this section, we review some basic concentration inequalities that we use in the main text. The first is the following Gaussian concentration equality.

Lemma A.1 (Gaussian concentration (Vershynin, 2018)). Let X1,..., Xn be an iid sequence of mean-zero Gaussian random variables with variance σ2. Then, for every δ ∈(0, 1), with probability at least 1 −δ, we have that max i |Xi| ≤σ s

2 log 2n δ

.

The second is for the concentration of a sequence of Gumbel random variables. While this result is likely folklore, we provide a proof for completeness.

Lemma A.2. Let X1,..., Xn be an iid sequence of Gumbel random variables with parameter λ. Then, for every δ ∈(0, 1), with probability at least 1 −δ, we have that max i |Xi| ≤λ · ln

2n δ

.

<!-- Page 12 -->

Published as a conference paper at ICLR 2026

Proof. Consider a single Xi, and recall that the CDF of a Gumbel distribution with parameter λ is F(x) = exp(−exp(−x/λ)). Then

P [|Xi| > T] = P [Xi > T] + P [Xi < −T]

= 1 −exp(−exp(−T/λ)) + exp(−exp(T/λ)) ≤exp(−T/λ) + exp(−exp(T/λ))

where the inequality uses 1 −e−x ≤x. Substituting in T = λ log(2n/δ) yields

P [|Xi| > t] ≤δ

2n + exp(−2n/δ) ≤δ n since for n ≥1 and δ ∈(0, 1), 2n δ ≥ln

2n δ

. Union bounding over the n samples completes the result. ■

B PRIVACY ANALYSIS OF PEELING EXPONENTIAL MECHANISM

Lemma B.1 (Lemma 4.2 in Gillenwater et al. (2022)). For every ϵ > 0, δ ∈(0, 1) and k ≥1, if λ = 1 ϵ0, where ϵ0:= max

( ϵ k, s

8 log 1 δ

+ 8ϵ k − s

8 log 1 δ k

)

, then Algorithm 3 is (ϵ, δ)-differentially private.

C MISSING PROOFS

C.1 PROOF OF LEMMA 3.1

Proof. Let W be a (C, s)-Zipfian dataset. Let r⋆= maxi |Wi|. Then, it must be the case that N(r⋆) ≥1. Since W is (C, s)-Zipfian, we also know that N(r⋆) ≤ CN (r⋆)s. Hence, we have that

(r⋆)s ≤CN implying that r⋆≤(CN)1/s. ■

C.2 PROOFS FOR THE WGM

C.2.1 PROOF OF σ AND T

Lemma C.1. For every ϵ > 0, δ ∈(0, 1), and ∆0 ≥1, there exists σ = Θ q log(1 δ) ϵ

!

and

T = ˜Θδ,∆0(max{σ, 1}) which satisfy the conditions in Theorem 3.2.

Proof. Starting with σ, it suffices to find the smallest σ such that

Φ

1

2σ −ϵσ

≤δ

2.

By monotonicity of Φ−1(·), we have that

Φ

1

2σ −ϵσ

≤δ

2 ⇐⇒ 1 2σ −ϵσ ≤Φ−1 δ

2

.

Hence, it suffices to find the smallest σ that satisfies

2ϵσ2 + 2Φ−1 δ

2 σ −1 ≥0.

Using the quadratic formula we can deduce that we need to take σ ≥−Φ−1 δ

2 ϵ = Φ−1

1 −δ 2 ϵ = Ω



 q log

1 δ ϵ



,

<!-- Page 13 -->

Published as a conference paper at ICLR 2026 where the last inequality follows from the fact that Φ−1(p) ≤ r

2 log

1 1−p for p > 1

## 2. Now for

T, we have

1 + σΦ−1

1 −δ 2

1 ∆0

!

≥ max 1≤t≤∆0

1 √ t + σΦ−1

1 −δ 2

1 t!!

.

Hence, it suffices to upper bound

1 + σΦ−1

1 −δ 2

1 ∆0

!

.

By Bernoulli’s inequality and monotonicity of Φ−1(·), we have that

Φ−1

1 −δ 2

1 ∆0

!

≤Φ−1

1 − δ 2∆0

.

Since δ ≤1 and ∆0 ≥1, we have that

Φ−1

1 − δ 2∆0

≤ s

2 log 2∆0 δ

.

Hence, it suffices to take

T = 1 + σ s

2 log 2∆0 δ

= Θ max

( σ s log

∆0 δ

, 1

)!

,

This completes the proof. ■

C.2.2 PROOF OF THEOREM 3.3

Before we prove Theorem 3.3, we present three helper lemmas, Lemma C.2, C.3, and C.4, which correspond to three different “good” events. Lemma C.2 provides an upper bound on the missing mass due to the subsampling stage. Lemma C.3 guarantees that a high-frequency item in the original dataset will remain high-frequency in the subsampled dataset. Lemma C.4 provides a high-probability upper bound on the frequency of items that are missed by the WGM during the thresholding step. The proof of Theorem 3.3 will then follow by combining Lemmas C.2, C.3, and C.4.

Lemma C.2. Let W be a (C, s)-Zipfian dataset for C ≥1 and s > 1. Fix a user contribution bound ∆0 ≥1. Let f W be the random dataset such that f Wi ⊆Wi is a random sample without replacement of size min{∆0, Wi}. Then, for every β ∈(0, 1), with probability 1 −β, we have that

MM(W, ∪if Wi) ≤C1/s s −1

1 p⋆N log

(CN)1/s β s−1 s where p⋆:= min

1, ∆0 maxi |Wi|

.

Proof. Let pi:= min

1, ∆0 |Wi| and p⋆:= mini pi. Fix an item x ∈S i Wi. Then

P

" x /∈

[ i f Wi

#

=

Y i:x∈Wi

(1 −pi) ≤exp

−

X i:x∈Wi pi

!

≤e−p⋆N(x), where N(x) = P i 1{x ∈Wi}. Fix β ∈(0, 1) and consider the threshold

Q:= 1 p⋆log

(CN)1/s β

.

<!-- Page 14 -->

Published as a conference paper at ICLR 2026

Note that Q⋆≥1 by definition of p⋆. Since W is (C, s)-Zipfian, for any r ∈[M] with N(r) > Q, it must be the case that r ≤

CN

Q

1/s by rs ≤ CN N(r). Hence, there are at most

CN

Q

1/s

“heavy” items whose frequencies are above Q. By the union bound, we get that

P

"

∃x ∈

[ i

Wi \ f Wi and N(x) > Q

#

≤

CN

Q

1/s e−p⋆Q ≤β so with probability at least 1 −β, we have that N(x) > Q =⇒x ∈S i f Wi for all x ∈S i Wi.

Under this event, we have that

MM(W, ∪if Wi) ≤1

N

X x:N(x)≤Q

N(x) ≤1

N

X r≥r0

N(r)

where r0 = max n

CN

Q

1/s

, 1 o

. Using the fact that N(r) ≤CNr−s and s > 1 (by assumption), we get that

1 N

X r≥r0

N(r) ≤C

X r≥r0 r−s ≤C

Z ∞ r0−1 x−sdx = C s −1(r0 −1)1−s ≤ C s −1r1−s

0.

Since r0 ≥

CN

Q

1/s

, we get MM(W, ∪if Wi) ≤ C1/s s−1

Q N s−1 s. Using Q = 1 p⋆log

(CN)1/s β completes the proof. ■

Lemma C.3. In the same setting as Lemma C.2, for every β ∈(0, 1), we have that with probability 1 −β, for every x ∈S i Wi,

N(x) ≥τ2 =⇒ e N(x) ≥1

2p⋆N(x), where p⋆:= min

1, ∆0 maxi |Wi|

, τ2:= 8 p⋆log

(CN)1/s β

, and e N(x) = P i 1{x ∈f Wi}.

Proof. Fix some x ∈S i Wi such that N(x) ≥τ2. Then, e N(x) is the sum of independent Bernoulli random variables with success probability at least p⋆. Thus, we have that E h e N(x)

i

≥p⋆N(x) and multiplicative Chernoff’s inequality gives

P e N(x) ≤1

2p⋆N(x)

≤exp

−1

8p⋆N(x)

≤exp

−1

8p⋆τ2

.

Now, since W is (C, s)-Zipfian, we have that N(x) ≤CN rs for all x ∈S i Wi, so there can be at most

CN τ2

1/s elements x ∈S i Wi with N(x) ≥τ2. A union bound yields

P

"

∃x ∈

[ i

Wi: N(x) ≥τ2, e N(x) < 1

2p⋆N(x)

#

≤ β (CN)1/s ·

CN τ2

1/s

≤β, which completes the proof. ■

Lemma C.4. For every dataset W, if the WGM is run with noise parameter σ > 0, threshold T ≥1, and user contribution bound ∆0 ≥1, then for every β ∈(0, 1), with probability at least

1−β over S ∼WGM(W, ∆0), we have that eH(x) ≤T0, ∀x ∈f M, where T0:= T+σ r

2 log

2N β and f M:= S i f Wi \ S.

Proof. By Line 4 in Algorithm 1, we have that for all x ∈f M, its noisy weighted count is eH′(x) < T. Hence, by standard Gaussian concentration bounds (see Appendix A), with probability at least 1 −β over just the sampling of Gaussian noise in Line 3, we have eH(x) ≤T0 for all x ∈f M. ■

<!-- Page 15 -->

Published as a conference paper at ICLR 2026

We are now ready to prove Theorem 3.3.

Proof. (of Theorem 3.3) Let f W be the random dataset obtained by sampling a set f Wi of elements of size min{∆0, |Wi|} without replacement from each Wi, and let S be the overall output of the WGM. Let e N(x) = Pn i=1 1{x ∈f Wi} be the frequency of item x in the subsampled dataset and note that e N(x) ≤√q⋆eH(x) for all x ∈S i f Wi, where eH is the weighted histogram of item frequencies from f W. Let f M = S i f Wi \ S be the random variable denoting the set of items in S i f Wi but not in the algorithm’s output S. Finally, define τ1:= 2√q⋆T0 p⋆ and τ2:= 8 p⋆log

3(CN)1/s β

, where

T0 = T + σ r

2 log

2N β

.

Let E1, E2, and E3 be the events of Lemma C.2, C.3, and C.4 respectively, setting the failure probability for each event to be β

3. Then, by the union bound, E1 ∩E2 ∩E3 occurs with probability 1 −β. It suffices to show that E1 ∩E2 ∩E3 implies the stated upper bound on MM(W, S). We can decompose MM(W, S) into two parts, mass missed by subsampling and mass missed by noisy thresholding:

MM(W, S) = MM(W, ∪if Wi) + 1

N

X x∈f M

N(x). (2)

Under E1, we have that

MM(W, ∪if Wi) ≤C1/s s −1

1 p⋆N log

3(CN)1/s β s−1 s

, hence for the remainder of the proof, we will focus on bounding 1 N

P x∈f M N(x). First, we claim that under E2 and E3, we have that N(x) ≤max{τ1, τ2} =: τ for all x ∈f M. This is because, by event E3, we have that for every x ∈f M, e N(x) ≤√q⋆T0. Thus, if there exists an x ∈f M such that N(x) ≥τ2, then by event E2, it must be the case that p⋆

2 N(x) ≤e N(x) ≤√q⋆T0, which implies that N(x) ≤τ1.

Now, define r0:= max n CN τ

1/s, 1 o

. If r ≥r0, then CN rs ≤τ. Since N(x) ≤τ for every x ∈f M, every such item has rank greater than r0. Hence,

1 N

X x∈f M

N(x) ≤1

N

X r≥r0

N(r) ≤

X r≥r0

C rs ≤C

Z ∞ r0−1 t−sdt ≤Cr1−s

0 s −1.

Substituting in the definition of r0 and continuing yields

1 N

X x∈f M

N(x) ≤C1/s s −1 τ

N s−1 s ≤C1/s s −1



 max n

2√q⋆T0 p⋆, 8 p⋆log

3(CN)1/s β o

N



 s−1 s

.

Now, we are ready to complete the proof. Using the decomposition of MM(W, S) in Equation 2 along with E1 ∩E2 ∩E3 implies that

MM(W, S) ≤C1/s s −1

1 p⋆N log

3(CN)1/s β s−1 s

+ C1/s s −1



 max n

2√q⋆T0, 8 log

3(CN)1/s β o p⋆N



 s−1 s

≤C1/s s −1

1 p⋆N s−1 s

9 max n√q⋆T0, log

3(CN)1/s β o s−1 s

= C1/s s −1

9 p⋆N s−1 s max

(

√q⋆

T + σ s

2 log 6N β

!

, log

3(CN)1/s β

) s−1 s

.

The proof is complete after noting that

√q⋆ p⋆= maxi |Wi| √q⋆. ■

<!-- Page 16 -->

Published as a conference paper at ICLR 2026

C.2.3 PROOF OF THEOREM 3.6

As in the proof of Theorem 3.3, we start with the following lemma which bounds the maximum missing mass due to the subsampling step.

Lemma C.5. Let W be any dataset. Fix a user contribution bound ∆0 ≥1. Let f W be the random dataset such that f Wi ⊆Wi is a random sample without replacement of size min{∆0, Wi}. Then, for every β ∈(0, 1), with probability 1 −β, we have that

MM∞(W, ∪if Wi) ≤ log

N β p⋆N.

where p⋆:= min

1, ∆0 maxi |Wi|

.

Proof. Let W be any dataset, ∆0 ≥1 and β ∈(0, 1). We will follow the same proof strategy as in the proof of Lemma C.2. Let pi:= min

1, ∆0 |Wi| and p⋆:= mini pi. Fix an item x ∈S i Wi. Then,

P

" x /∈

[ i f Wi

#

=

Y i:x∈Wi

(1 −pi) ≤exp

−

X i:x∈Wi pi

!

≤e−p⋆N(x), where N(x) = P i 1{x ∈Wi}. Fix β ∈(0, 1) and consider the threshold

Q:= 1 p⋆log

N β

≥1.

Since P x∈S i Wi N(x) = N, we have that that there are at most N

Q items such that N(x) > Q. Hence, by the union bound, we get that

P

"

∃x ∈

[ i

Wi \ f Wi and N(x) > Q

#

≤N

Q e−p⋆Q ≤β.

Hence, with probability at least 1 −β, we have that if x /∈S i f Wi, then N(x) ≤Q, giving that

MM∞(W, ∪if Wi) ≤ log

N β p⋆N, which completes the proof. ■

Now, we use Lemma C.5 to complete the proof of Theorem 3.6. Since the proof follows almost identically, we only provide a sketch here.

Proof. (sketch of Theorem 3.6) As in the proof of Theorem 3.3, define q⋆= min{maxi |Wi|, ∆0}

and T0 = T + σ r

2 log

6N β

. Keep τ1:= 2√q⋆T0 p⋆ but take τ2:= 8 p⋆log

3N β

.

Let E2 be defined identically in terms of T0. That is, E2 is the event that eH(x) ≤T0 for all x ∈f M, where T0 = T +σ r

2 log

6N β and f M = S i f Wi \S. Likewise, define E3 in terms of τ2 analogous to that in the proof of Theorem 3.3. That is, E3 is the event that for all x ∈S i Wi, either N(x) < τ2 or e N(x) ≥p⋆

2 · N(x). The fact that E2 occurs with probability at least 1 −β 3 follows identitically from the proof of Theorem 3.3.. As for event E3, note that we have

P

"

∃x ∈

[ i

Wi: N(x) ≥τ2, e N(x) < 1

2p⋆N(x)

#

≤N τ2

· e−p⋆τ2 8 ≤β

3,

<!-- Page 17 -->

Published as a conference paper at ICLR 2026 which follows similarly by using multiplicative Chernoff’s, the union bound, and the fact that there can be at most N τ2 items with frequency at least τ2. Hence, E3 occurs with probability at least 1 −β

3.

Then, by the union bound we have that with probability 1 −2β

3, both E2 and E3 occur. When this happens, we have that N(x) ≤max{τ1, τ2} for all x ∈f M because either N(x) ≤τ2, or otherwise 1 2p⋆N(x) ≤e N(x) ≤√q⋆T0, implying that N(x) ≤τ1. Consequently, under E2 and E3, we have that max x∈∪if Wi\S

N(x)

N ≤max{τ1, τ2}

N

By Lemma C.5, the event

MM∞(W, ∪if Wi) ≤ log

3N β p⋆N.

occurs with probability 1 −β

3. Hence, under E1 ∩E2 ∩E3, we have that

MM∞(W, S) ≤max n

MM∞(W, ∪if Wi), max x∈f W \S

N(x)

N o

≤ 8 p⋆N max

( log

3N β

, √q⋆

T + σ s

2 log 6N β

!)

, which occurs with probability 1 −β. Finally, plugging in σ = Θ

√ ln(1/δ)

ϵ and T = ˜Θ∆0,δ(σ)

completes the claim. ■

C.3 PROOF OF THEOREM 4.3

Since the privacy guarantee follows by basic composition, we only focus on proving the utility guarantee in Theorem 4.3. First, we provide the proof of Lemma 4.2.

Proof. (of Lemma 4.2) Let I = Tk(W, D) \ S and O = S \ Tk(W, D). Then, |I| = |O| ≤k and

X x∈Tk(W,D)

N(x) −

X x∈S

N(x) =

X x∈I

N(x) −

X x∈O

N(x).

Since |I| = |O|, there exists a one-to-one mapping π: I →O that pairs each item in I with an item in O. Thus, we can write

X x∈I

N(x) −

X x∈O

N(x) =

X x∈I

(N(x) −N(π(x))).

By definition of I and O, we have that for every x ∈I and y ∈O, ˜N(y) ≥˜N(x). Hence, we have that N(x) −N(y) ≤Zy −Zx and

X x∈I

(N(x) −N(π(x))) ≤

X x∈I

(Zπ(x) −Zx).

Define R:= P x∈I(Zπ(x) −Zx). Our goal is to get a high-probability upper bound on R via concentration. By Gumbel concentration (Lemma A.2), with probability 1 −β, we have that maxx∈D |Zx| ≤λ · log(2|D|/β). Hence, under this event, we get that

R ≤2kλ · log(2|D|/β).

Altogether, with probability 1 −β, we have

X x∈Tk(W,D)

N(x) −

X x∈S

N(x) ≤R ≤2kλ · log(2|D|/β).

Dividing by N completes the proof. ■

<!-- Page 18 -->

Published as a conference paper at ICLR 2026

Combining Lemmas 4.2 and 4.1 then gives the following corollary. Corollary C.6. For every dataset W, domain D, k ≤|D|, ϵ > 0, and δ ∈(0, 1), if Algorithm 3 is run with λ = ˜Θδ

√ k ϵ from Lemma 4.1, then Algorithm 3 is (ϵ, δ)-differentially private and with probability at least 1 −β over its output S, we have that

1 N



 X x∈Tk(W,D)

N(x) −

X x∈S

N(x)



≤˜Oδ,β k3/2 log |D| ϵN

.

With Corollary C.6 in hand, we are now ready to prove Theorem 4.3 after picking the same choice of (σ, T) as in Theorem 3.2.

Proof. (of Theorem 4.3) Recall that by Theorem 3.6, if we set σ = Θ

√ ln(1/δ)

ϵ and T =

˜Θ∆0,δ/2(max{σ, 1}), then the WGM is (ϵ/2, δ/2)-differentially private and with probability at least 1 −β/2 over D ∼WGM(W, ∆0), we have that

MM∞(W, D) ≤˜O∆0,δ/2,β/2 maxi |Wi| ϵN√q⋆

. (3)

Let Tk(W) be the true set of top-k elements and Tk(W, D) be the set of top-k elements within the (random) domain D. Then, under this event, Equation 3 gives that

1 N



 X x∈Tk(W)

N(x) −

X x∈Tk(W,D)

N(x)



≤k · MM∞(W, D) ≤˜O∆0,δ/2,β/2 k · maxi |Wi| ϵN√q⋆

.

(4) By Corollary C.6, we know that running Algorithm 3 on input W, domain D and λ = ˜Oδ/2

√ k ϵ gives (ϵ/2, δ/2)-differentially privacy and that with probability at least 1−β/2, its output S satisfies

1 N



 X x∈Tk(W,D)

N(x) −

X x∈S

N(x)



≤˜Oδ/2,β/2 k3/2 log |D| ϵN

. (5)

Adding Inequalities 4 and 5 together and taking |D| ≤| S i Wi| =: M gives that with probability 1 −β, the output S of Algorithm 2 satisfies

MMk(W, S) ≤˜Oβ,δ,∆0 k N maxi |Wi| ϵ√q⋆ +

√ k log(M)

ϵ

!!

, which completes the proof. ■

C.4 PROOF OF THEOREM 4.5

Before we prove Theorem 4.5, we first present the pseudo-code (Algorithm 4) for the user peeling mechanism described in Section 4.2 along with its privacy and utility guarantees.

The following lemma gives the utility and privacy guarantee of Algorithm 4. Lemma C.7. For every dataset W, domain D, and k ≤|D|, if Algorithm 4 is run with noise parameter λ > 0, then with probability 1 −β over its output S, we have that

Hits(W, S) ≥

1 −1 e

Opt(W, D, k) −2kλ log

2|D|k β

.

where Opt(W, D, k):= arg maxS⊆D,|S|≤k Hits(W, S). If one picks λ = ˜Θδ

√ k ϵ from Lemma

4.1, then Algorithm 4 is (ϵ, δ) differentially private and with probability 1 −β over its output S, we have

Hits(W, S) ≥

1 −1 e

Opt(W, D, k) −˜Oδ,β k3/2 log (|D|k)

ϵ

.

<!-- Page 19 -->

Published as a conference paper at ICLR 2026

## Algorithm

## 4 User Peeling Mechanism Input:

Dataset W, domain D, number of elements k, noise-level λ

1 Initialize W 1 ←W, D1 ←D, and output set S0 ←∅

2 for j = 1,..., k do

## 3 Compute histogram

Hj(x) = P i 1{x ∈W j i } for all x ∈Dj.

4 Compute noisy histogram ˜Hj(x) = Hj(x) + Zj x for all x ∈Dj where Zj x ∼Gumbel(λ).

5 Let xj ∈arg maxx∈Dj ˜Hj(x)

## 6 Update

Sj ←Sj−1 ∪{xj}, Dj+1 ←Dj \ {xj}, and W j+1 ←{Wi ∈W j: xj /∈Wi}.

7 end Output: Sk

Since Algorithm 4 also uses the peeling exponential mechanism, the privacy guarantee in Lemma C.7 follows exactly from Lemma 4.1, and so we omit the proof here. As for the utility guarantee, the proof is similar to the proof of Theorem 7 in Mitrovic et al. (2017). For the sake of completeness, we provide a self-contained analysis below.

Proof. Note that there exists at most |D|k random variables Zj x. Let E be the event that |Zj x| ≤α for all x ∈D and j ∈[k], where α = λ ln

2|D|k β

. Then, by Gumbel concentration (Lemma A.2), we have that P(E) ≥1 −β. For the rest of this proof, we will operate under the assumption that event E happens.

Define the function f: 2D →N as f(S):= Pn i=1 1{Wi ∩S̸ = ∅} = Hits(W, S). Then, f is a monotonic, non-negative submodular function. For x ∈D and S ⊆D let ∆(x, S):= f(S ∪{x}) −f(S) ≥0. Let S⋆∈arg maxS⊆D,|S|≤k f(S) be the optimal subset of D and denote Opt:= f(S⋆). First, we claim that for every S ⊆D, max x∈S⋆\S ∆(x, S) ≥Opt −f(S)

k. (6)

This is because

Opt = f(S⋆) ≤f(S⋆∪S)

≤f(S) +

X x∈S⋆\S

∆(x, S)

≤f(S) + k max x∈S⋆\S ∆(x, S), where the first two inequalities follows from monotonicity and submodularity respectively. Now, let x1,..., xk be the (random) items selected by the algorithm, and Sj = {x1,..., xj} with S0 = ∅. At round j ∈[k], define the current domain Dj:= D \ Sj−1. Let x⋆ j ∈arg max x∈S⋆\Sj−1

∆(x, Sj−1).

Then, by Equation 6, we have ∆(x⋆ j, Sj−1) ≥Opt −f(Sj−1)

k. This implies that

∆(xj, Sj−1) ≥Opt −f(Sj−1)

k −(∆(x⋆ j, Sj−1) −∆(xj, Sj−1))

= Opt −f(Sj−1)

k −(Hj(x⋆ j) −Hj(xj))

where the last equality stems from the fact that for every x ∈Dj, ∆(x, Sj−1) = Hj(x).

Recall that ˜Hj(x):= Hj(x) + Zj x for all x ∈D. We can upper bound Hj(x⋆ j) −Hj(xj) as

Hj(x⋆ j) −Hj(xj) = (˜Hj(x⋆ j) −˜Hj(xj)) + (Zj xj −Zj x⋆ j) ≤Zj xj −Zj x⋆ j, where last inequality is because ˜Hj(x⋆ j) −˜Hj(xj) ≤0 by the choice of xj ∈arg maxx∈Dj ˜H j(x) and the fact that x⋆ j ∈S⋆\ Sj−1 ⊆Dj. Therefore,

∆(xj, Sj−1) ≥Opt −f(Sj−1)

k −

Zj xj −Zj x⋆ j

. (7)

<!-- Page 20 -->

Published as a conference paper at ICLR 2026

Let Gj:= Opt −f(Sj). Using f(Sj) = f(Sj−1) + ∆(xj, Sj−1), we rearrange Equation 7 to get

Gj ≤

1 −1 k

Gj−1 + (Zj xj −Zj x⋆ j).

On the event E, we have that Zj xj −Zj x⋆ j ≤|Zj xj| + |Zj x⋆ j | ≤2α, hence

Gj ≤

1 −1 k

Gj−1 + 2α.

Recursing for j = 1,..., k and using the fact that G0 = Opt and (1 −1 k)k ≤e−1, gives

Gk ≤1 e Opt +2αk.

Substituting in the definition of Gk and α = λ ln

2|D|k β gives f(Sk) ≥

1 −1 e

Opt −2kλ log

2|D|k β

.

■

The guarantee in Lemma C.7 is with respect to the optimal set of k elements within the domain D. Since D ⊆S i Wi, we have that

Opt(W, D, k) ≤Opt(W, k).

The following simple lemma shows that when the domain D contains high-frequency items from W, Opt(W, D, k) is not too far away from Opt(W, k). Lemma C.8. Fix a dataset W, τ ≥0, and let D = {x ∈S i Wi: N(x) ≥τ}. Then,

Opt(W, D, k) ≥Opt(W, k) −kτ.

Proof. Recall that f(S):= Hits(W, S) is a monotone, non-negative submodular function. Let S1 ⊆X be the subset of X that achieves f(S1) = Opt(W, k) and S2 be the subset of D that achieves f(S2) = Opt(W, D, k). By submodularity and the definition of X \ D we have that f(S1) ≤f(S1 ∩D) + f(S1 ∩X \ D) ≤f(S2) + kτ, which completes the proof. ■

Lemma C.8 allows us to use the MM∞upper bound obtained by the WGM in Theorem 3.6 to upgrade the guarantee provided by Lemma C.7 to be in terms of Opt(W, k) instead of Opt(W, D, k). By using the same choice of (σ, T) as in Theorem 3.2, we get the main result of this section. As before, since the privacy guarantee follows by basic composition, we only focus on proving the utility guarantee.

Proof. (of Theorem 4.5) Recall that by Theorem 3.6 that if we set σ = Θ

√ ln(1/δ)

ϵ and T =

˜Θ∆0,δ/2(max{σ, 1}), then the WGM is (ϵ/2, δ/2)-differentially private and with probability at least 1 −β/2 over D ∼WGM(W, ∆0), we have that

MM∞(W, D) ≤˜O∆0,δ/2,β/2 maxi |Wi| ϵN√q⋆

.

By Lemma C.8, under this event we have that

Opt(W, D, k) ≥Opt(W, k) −˜O∆0,δ/2,β/2 k · maxi |Wi| ϵ√q⋆

.

Now, by Lemma C.7, we know that running Algorithm 4 on input W, domain D and λ =

˜Oδ/2

√ k ϵ gives (ϵ/2, δ/2)-differentially privacy and that with probability at least 1 −β/2, its output S satisfies

Hits(W, S) ≥

1 −1 e

Opt(W, D, k) −˜Oδ/2,β/2 k3/2 ϵ log (|D|k)

<!-- Page 21 -->

Published as a conference paper at ICLR 2026

Hence, by the union bound, with probability at least 1 −β, both events occur and we have that

Hits(W, S) ≥

1 −1 e

Opt(W, D) −˜Oβ,δ,∆0 k · maxi |Wi| ϵ√q⋆ + k3/2 ϵ log (Mk)

, where we use the fact that |D| ≤M. ■

D LOWER BOUNDS

D.1 LOWER BOUNDS FOR MISSING MASS

In this section, we prove Theorem 3.5. The following lemma will be useful.

Lemma D.1. Let A be any (ϵ, δ)-differentially private algorithm satisfying Assumption 1. Then, for every dataset W and item x ∈S i Wi, if N(x) ≤1 ϵ ln

1 + eϵ−1 2δ

, then PS∼A(W) [x ∈S] ≤1

2.

Proof. Fix some dataset W. Let A be any randomized algorithm with privacy parameters ϵ ≤1 and δ ∈(0, 1) satisfying Assumption 1. This means that for any item x ∈S i Wi such that NW (x) = 1, we have that

PS∼A(W) [x ∈S] ≤δ, where for a dataset W, we define NW (x):= P i 1{x ∈Wi}. Now, suppose x ∈S i Wi is an item such that NW (x) = 2. We can always construct a neighboring dataset W ′ by removing a user such that NW ′(x) = 1. Thus, we have that

PS∼A(W) [x ∈S] ≤eϵPS∼A(W ′) [x ∈S] + δ ≤δeϵ + δ = δ(eϵ + 1).

More generally, by unraveling the recurrence, we have that for any x ∈S i Wi with NW (x) = b,

PS∼A(W) [x ∈S] ≤δ b−1 X i=0

(eϵ)i = δ eϵb −1 eϵ −1.

Since W was arbitrary, for any dataset W and any x ∈S i Wi with NW (x) = b, we have that

PS∼A(W) [x /∈S] ≥1 −δ eϵb −1 eϵ −1.

Now, consider the exclusion probability p = 1/2. Our goal is to compute the largest b⋆such that for any dataset W, any x ∈S i Wi with NW (x) ≤b⋆has PS∼A(W) [x /∈S] ≥1

2. It suffices to solve for b in the inequality 1 −δ eϵb−1 eϵ−1 ≥1/2, which yields b ≤1 ϵ ln

1 + eϵ−1 2δ

=: b⋆. ■

Lemma D.1 provides a uniform upper bound on the the probability that any private mechanism can output a low frequency item. We now use Lemma D.1 to complete the proof of Theorem 3.5.

Proof. (of Theorem 3.5) Let b⋆= 1 ϵ ln

1 + eϵ−1 2δ as in the proof of Lemma D.1. By Lemma D.1, for any dataset W and item x ∈S i Wi such that N(x) ≤b⋆, we have PS∼A(W) [x /∈S] ≥ 1 2.

Consider a dataset W ⋆of size n, taking n sufficiently large, where

N(r)

N = Θ

C rs for all ranks r ∈[M ⋆], where M ⋆= | S i W ⋆ i | (note that such a dataset is possible if, for example, one restricts each user to contribute exactly a single item). We can lower bound the missing mass of A on W ⋆as

ES∼A(W ⋆) [MM(W ⋆, S)] ≥1

N

X x∈S i W ⋆ i,N(x)≤b⋆

PS∼A(W ⋆) [x /∈S] N(x)

≥ 1 2N

X x∈S i W ⋆ i,N(x)≤b⋆

N(x).

<!-- Page 22 -->

Published as a conference paper at ICLR 2026

Our next goal will be to find the smallest rank r⋆such that N(r⋆) ≤b⋆. It suffices to solve the inequality CN rs ≤b⋆for r. Doing so gives that r ≥ l CN b⋆

1 s m

=: r⋆. Hence, for this W ⋆, we have that

ES∼A(W ⋆) [MM(W ⋆, S)] ≥ 1 2N

X x∈S i W ⋆ i,N(x)≤b⋆

N(x)

= 1 2N

M ⋆ X r=r⋆

N(r)

= Ω

1 N

M ⋆ X r=r⋆

CN rs

!

.

Since s > 1, we can take M ⋆(and hence n) to be large enough so that

Ω

1 N

M ⋆ X r=r⋆

CN rs

!

= Ω

1

N

Z ∞ r⋆

CN rs dr

.

Thus,

ES∼A(W ⋆) [MM(W ⋆, S)] = Ω

1

N

Z ∞ r⋆

CN rs dr

= Ω

C s −1(r⋆)1−s

= Ω

C1/sN (1−s)/s s −1 (b⋆)(s−1)/s

= Ω

C1/sN −(s−1)/s s −1

1 ϵ ln

1 + eϵ −1 2δ

(s−1)/s!

= Ω

C1/s s −1 ·

1 ϵN

(s−1)/s

· ln

1 + eϵ −1 2δ

(s−1)/s!

, which completes the proof. ■

D.2 LOWER BOUNDS FOR TOP-k SELECTION

Proof. (of Corollary 4.4) Define b⋆= 1 ϵ ln

1 + eϵ−1 2δ like in Lemma D.1. Recall from Lemma D.1, that for any dataset W and any item x ∈S i Wi such that N(x) ≤b⋆, we have that

PS∼A(W,k) [x /∈S] ≥1

2.

Consider any dataset W ⋆such that | S i W ⋆ i | = k and N(i) = b⋆for all i ∈[k]. Then Pk i=1 N(i) = kb⋆. But, we also have that ES∼A(W,k)

P x∈S N(x)

≤kb⋆

## 2. Hence,

ES∼A(W ⋆,k)

h

MMk(W ⋆, S)

i

≥kb⋆

2N = ˜Ωδ k ϵN

, completing the proof. ■

D.3 LOWER BOUNDS FOR k-HITTING SET.

Proof. (of Corollary 4.6) Define b⋆= 1 ϵ ln

1 + eϵ−1 2δ as in Lemma D.1. Recall from Lemma D.1, that for any dataset W and any item x ∈S i Wi such that N(x) ≤b⋆, we have that

PS∼A(W,k) [x /∈S] ≥1

2.

<!-- Page 23 -->

Published as a conference paper at ICLR 2026

This is due to our restriction that A(W, k) ⊆S i Wi. Consider any dataset W ⋆consisting of k unique items and n = kb⋆users such that each item hits a disjoint set of b⋆users. Since the frequency of each of the k items is at most b⋆, A can output each item with probability at most 1/2. Hence, in expectation, A outputs at most k/2 distinct items, hitting at most kb⋆

2 users, while the optimal set of items includes all k items and hits all users. ■

E EXPERIMENT DETAILS

In this section, we provide details about the datasets used in Section 5. Table 1 provides statistics for the 6 datasets we consider. Reddit (Gopi et al., 2020) is a text-data dataset of posts from r/askreddit. For this dataset, each user corresponds to a set of documents, and following prior methodology, we take a user’s item set to be the set of tokens used across all documents. Movie Reviews (Harper & Konstan, 2015) is a dataset containing movie reviews from the MovieLens website. Here, we group movie reviews by user-id, and take a user’s itemset to be the set of movies they reviewed. Amazon Games, Pantry, and Magazine (Ni et al., 2019) are review datasets for video games, prime pantry, and magazine subscriptions respectively. Like for Movie Reviews, we group rows by user-id and take a user’s item set to the set of items they reviewed. Finally, Steam Games (Steam, 2025) is a dataset of 200k user interactions (purchases/play) on the Steam PC Gaming Hub. As before, we group the rows by user-id and take a user’s itemset to the be the set of games they purchased/played.

Dataset No. Users No. Items No. Entries

Reddit 245103 631855 18272211 Movie Reviews 162541 59047 25000095 Amazon Games 1540618 71982 2489395 Steam Games 12393 128804 Amazon Magazine 72098 88318 Amazon Pantry 247659 10814 447399

**Table 1.** Number of users, items, and entries (user-item pairs) for each dataset

E.1 RANK VS. FREQUENCY PLOTS

In order to get meaningful upper bounds on MM, Theorem 3.3 requires that W be (C, s)-Zipfian for s > 1. Figures 4 and 5 present log-log plots of frequency vs. rank for the large and small datasets respectively. In all cases, we observe that the real-world datasets we consider are (C, s)-Zipfian for s > 1 and sufficiently large C. Note that our definition of a Zipfian dataset only requires the frequency vs. rank plot to be upper bounded by a decaying polynomial.

(a) Reddit (b) Amazon Games (c) Movie Reviews

**Figure 4.** Log-log plot of frequency vs. rank for large datasets

![Figure extracted from page 23](2026-ICLR-differentially-private-domain-discovery/page-023-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICLR-differentially-private-domain-discovery/page-023-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICLR-differentially-private-domain-discovery/page-023-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 24 -->

Published as a conference paper at ICLR 2026

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 5.** Log-log plot of frequency vs. rank for small datasets

E.2 USER ITEM SET SIZE DISTRIBUTIONS

Figures 6 and 7 plot the Empirical CDF (ECDF) of user item set sizes for the large and small datasets respectively.

(a) Reddit (b) Amazon Games (c) Movie Reviews

**Figure 6.** ECDFs of user item set sizes for large datasets.

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 7.** ECDFs of user item set sizes for small datasets.

F ADDITIONAL EXPERIMENTAL RESULTS

F.1 PRIVATE DOMAIN DISCOVERY

F.1.1 RESULTS FOR SMALL DATASETS

**Figure 8.** plots the MM as a function of ∆0 for the small datasets. Again, we find that the WGM achieves comparable performance to the policy mechanism while being significantly more computationally efficient.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICLR-differentially-private-domain-discovery/page-024-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 25 -->

Published as a conference paper at ICLR 2026

(a) Missing Mass (b) Missing Mass (c) Missing Mass

**Figure 8.** MM as a function of ∆0 ∈{1, 50, 100, 150, 200, 300} for the small datasets.

F.1.2 RESULTS FOR ϵ = 0.10

Figures 9 and 10 plot the MM for the large and small datasets respectively when ϵ = 0.1 and δ = 10−5.

(a) Missing Mass (b) Missing Mass (c) Missing Mass

**Figure 9.** MM as a function of ∆0 ∈{1, 50, 100, 150, 200, 300} for large datasets when ϵ = 0.1 and δ = 10−5.

(a) Missing Mass (b) Missing Mass (c) Missing Mass

**Figure 10.** MM as a function of ∆0 ∈{1, 50, 100, 150, 200, 300} for small datasets when ϵ = 0.1 and δ = 10−5.

F.2 TOP-k SELECTION

The top-k ℓ1 loss is defined as ℓk

1(W, S) = min{|S|,k} X i=1

|N(i) −N(Si)| + k X i=min{|S|,k}

N(i), where S is any ordered sequence of items. Unlike the top-k MM, the top-k ℓ1 loss cares about the order of items output, and hence is a more stringent measure of utility.

**Figure 11.** plots the top-k ℓ1 MM for ϵ = 1.0, δ = 10−5, and ∆0 = 100. Similar to Figure 2, we observe that our method (purple) achieves significantly less Top-k ℓ1 loss compared to all baselines.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 25](2026-ICLR-differentially-private-domain-discovery/page-025-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 26 -->

Published as a conference paper at ICLR 2026

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 11.** Top-k ℓ1 loss vs. k with ϵ = 1.0, δ = 10−5, and ∆0 = 100.

(a) Top-k MM (b) top-k ℓ1

(c) Top-k MM (d) top-k ℓ1

(e) Top-k MM (f) top-k ℓ1

**Figure 12.** Top-k MM and Top-k ℓ1 vs. k for k ∈{5, 10, 20, 50, 100, 200}, with ϵ = 0.1, δ = 10−5 and ∆0 = 100.

**Figure 12.** plots the top-k MM and top-k ℓ1 loss for the small datasets when ϵ = 0.1 and δ = 10−5. Like the case when ϵ = 1.0, our method (purple) continues to outperform the baselines across all k values.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 26](2026-ICLR-differentially-private-domain-discovery/page-026-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 27 -->

Published as a conference paper at ICLR 2026

F.3 k-HITTING SET

**Figure 13.** plots the Number of missed users for the small datasets when ϵ = 0.1, δ = 10−5, and ∆0 = 100. We observe that our method (blue) performs comparably and sometimes outperforms the case where the domain S

i Wi is public.

(a) Steam Games (b) Amazon Magazine (c) Amazon Pantry

**Figure 13.** Number of missed users vs. k for k ∈{5, 10, 20, 50, 100, 200} with ϵ = 0.1, δ = 10−5, and ∆0 = 100.

![Figure extracted from page 27](2026-ICLR-differentially-private-domain-discovery/page-027-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 27](2026-ICLR-differentially-private-domain-discovery/page-027-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 27](2026-ICLR-differentially-private-domain-discovery/page-027-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
