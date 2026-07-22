---
title: "Improved Fully Dynamic Submodular Maximization Under Matroid Constraints"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/41020
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/41020/44981
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Improved Fully Dynamic Submodular Maximization Under Matroid Constraints

<!-- Page 1 -->

Improved Fully Dynamic Submodular Maximization Under Matroid Constraints

Yiwei Gao1,2, Jialin Zhang1, 2, Zhjie Zhang3*

1State Key Lab of Processors, Institute of Computing Technology, Chinese Academy of Sciences, Beijing 100190, China 2School of Computer Science and Technology, University of Chinese Academy of Sciences, Beijing 100049, China 3Center for Applied Mathematics of Fujian Province, School of Mathematics and Statistics, Fuzhou University gaoyiwei22@mails.ucas.ac.cn, zhangjialin@ict.ac.cn, zzhang@fzu.edu.cn

## Abstract

This paper studies submodular maximization over matroids in the fully dynamic setting, where elements of an underlying ground set undergo sequential insertions and deletions. The goal is to maintain an approximate optimal solution for the current element set with a low amortized update time. For monotone submodular functions. we propose a dynamic algorithm achieving a (0.3178 −ε)-approximation using ˜Oε(k3) expected amortized queries, where k is the rank of the matroid contraint. Furthermore, we extend our approach to the non-monotone submodular maximization setting, obtaining a (0.1921 −ε)-approximation with the same update complexity. Both algorithms improve upon the best known approximation guarantees, which are (0.25 −ε) for the monotone case and (0.0932 −ε) for the non-monotone case.

## Introduction

Submodularity is a fundamental property that is possessed by many objective functions of combinatorial optimization problems. It captures the real-world phenomenon of diminishing returns, making it applicable across a range of practical contexts, including data summarization (Bairi et al. 2015; Kumari and Bilmes 2021), influence maximization (Kempe, Kleinberg, and Tardos 2003), sparse reconstruction (Bach 2010; Das and Kempe 2011), feature selection (Khanna et al. 2017; Das and Kempe 2018), information gathering (Radanovic et al. 2018), video analysis (Zheng et al. 2014). Due to their elegant structures, matroids often arise as the constraints of these problems. As a result, submodular maximization subject to a matroid constraint has been one of the central topics in the past decades.

Many excellent results on approximating the optimal solution of the problem have emerged. For monotone submodular maximization, the groundbreaking work of Vondr´ak (2008) proposed the famous continuous greedy algorithm, which attains (1 −1/e) approximation under matroid constraints. This is the best ratio one can achieve with a polynomial number of queries (Nemhauser and Wolsey 1978). For non-monotone submodular maximization, the best-known algorithm achieves 0.401 approximation (Buchbinder and Feldman 2024), while any polynomial algorithm can not

*Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

achieve an approximation ratio better than 0.478 (Gharan and Vondr´ak 2011; Qi 2022).

Recently, submodular maximization under the (fully) dynamic model has aroused researchers’ interest (Lattanzi et al. 2020a; Monemizadeh 2020). The dynamic model assumes that there is a stream of insertions and deletions of elements in the ground set N. Let Nt ⊆N be the set of elements that have been inserted but not deleted subsequently until time t. The goal is to maintain a feasible solution St ∈Nt that (approximately) maximizes the submodular objective function with an amortized update time of O(poly(k), polylog(n)).

Significant progresses has been made on the dynamic monotone submodular maximization for the cardinality constraint, also known as the uniform matroid. A series of works (Lattanzi et al. 2020a; Monemizadeh 2020; Banihashem et al. 2023a, 2024) proposed a variety of dynamic algorithms that maintains (1/2 −ε)-approximation using low amortized queries. The ratio is optimal in the sense that any algorithm that achieves a (1/2 + ε)-approximation for the problem requires an amortized query complexity of n˜Ω(ε)/k3 (Chen and Peng 2022). For general matroids, however, the best-known dynamic algorithms (Duetting et al. 2023; Banihashem et al. 2024) achieves only (1/4 −ε)-approximation, leaving a substantial room for improvement. For non-monotone submodular maximization, the best-known dynamic algorithms maintain (1/8 −ε)approximation for the cardinality constraints (Banihashem et al. 2023b) and (0.0932 −ε)-approximation for general matroid constraints (Liu and Yang 2024).

Our Contributions. We propose improved dynamic algorithms for submodular maximization subject to a matroid constraint. Specifically,

1. We are the first to show that a streaming algorithm based on the multilinear extension can be successfully maintained within the dynamic framework of (Banihashem et al. 2024)

2. Building on this, we develop two dynamic algorithms for fully dynamic submodular maximization under a matroid constraint: a (0.3178 −ε)-approximation for the monotone setting and a (0.1921 −ε)-approximation for the non-monotone setting, both with amortized query complexity ˜Oε(k3).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

36928

<!-- Page 2 -->

Both of our algorithms achieve substantially better approximation ratios than all existing methods, while maintaining average query complexity that is completely independent of n.

Related Work. Lattanzi et al. (2020a) and Monemizadeh (2020) independently initiated the study of submodular maximization in the dynamic setting. For monotone submodular maximization under the cardinality constraint, Monemizadeh (2020) proposed a dynamic algorithm that attains (1/2 −ε)-approximation with amortized query complexity of O(ε−3k2 log5 n). Lattanzi et al. (2020a) presented an alternative dynamic algorithm that also achieves (1/2 − ε)-approximation, but has a polylogarithmic update time of O(ε−11 log6 k log2 n). Later, Banihashem et al. (2023a) pointed out that the analysis of Lattanzi et al. (2020a) has some correctness issues, and then presented another dynamic algorithm with polylogarithmic update time. Lattanzi et al. also remedied their algorithm in the latest arXiv version of their paper (Lattanzi et al. 2020b), achieving an improved update time of O(ε−4 log4 k log2 n). After that, Banihashem et al. (2024) proposed a novel dynamic algorithm whose amortized query complexity is O(ε−1k log2 k), which is the first fully dynamic algorithm with an update time independent of n. These results match the hardness result of Chen and Peng (2022), who showed that any dynamic algorithm that achieves a (1/2 + ε)-approximation for the problem requires amortized query complexity of n˜Ω(ε)/k3.

For monotone submodular maximization under the matroid constraint, Duetting et al. (2023) presented a dynamic algorithm whose approximation ratio is 1/4 −ε and amortized query complexity is O(ε−1k2 log2 n log3(ε−1k)). Indepenently, Banihashem et al. (2024) provided an improved algorithm with an O(k log k log3(ε−1k)) update time.

For non-monotone submodular maximization, Banihashem et al. (2023b) proposed a dynamic algorithm under the cardinality constraint, which achieves (1/8 −ε)approximation and requires O(ε−1k log2 k) oracle queries. Liu and Yang (2024) presented an improved algorithm that achieves (1/6 −ε)-approximation and requires O(ε−1k2 log2 k) amortized oracle queries. Liu and Yang (2024) also presented a dynamic algorithm for the matroid constraint, which attains (0.0932 −ε)-approximation and has an O(ε−1k2 log k log3(ε−1k)) update time.

## Preliminaries

Submodular Functions. Given a ground set N, a set function f: 2N →R maps every element of the power set of N to a real number. Submodularity captures the property of diminishing marginal returns in set functions. For clarity, we use the notation S + u to denote S ∪{u}, and S −u to denote S \ {u}. We define the marginal contribution of a set S with respect to another set T as f(S | T):= f(S ∪T) −f(T). In particular, the marginal contribution of a single element u with respect to a set T is given by f(u | T):= f(T ∪{u})−f(T). A set function f: 2N →R is called submodular if for any two sets S ⊆T ⊆N and an element u ∈N \ T we have f(u | S) ≥f(u | T).

In addition, f is called monotone if for any sets S ⊆T, we have f(S) ≤f(T). f is called non-negative if f ≥0.

Matroids. A matroid M = (N, I) is a set system where I ⊆2N is a family of subsets of the ground set N, which satisfies the following properties:

• ∅∈I; • If A ⊆B and B ∈I, then A ∈I; • If A, B ∈I with |A| < |B|, there exists u ∈B \ A such that A + u ∈I. The members of I are called independent sets. The maximal independent sets are called bases. It can be proven that all the bases share a common cardinality, called the rank of M. For a subset S ⊆N (not necessarily independent), its rank is defined as the size of its maximum independent subset, i.e. rank(S) = maxT ⊆S,T ∈I |T|. The span of a set S ⊆N in a matroid is the set of elements u ∈N such that rank(S ∪{u}) = rank(S).

Submodular Maximization under Matroid Constraints. The problem we are concerned with can be formulated as max{f(S): S ∈I}, where f is a non-negative submodular function and M = (N, I) forms a matroid defined over the ground set N. We use OPT to denote the optimal solution of the problem. We assume that f is accessed via a value oracle that returns f(S) when S is queried, and I is accessed by a membership oracle that returns whether S ∈I. We use the number of queries to the oracles an algorithm makes to measure the algorithm’s complexity. It is well-known that for maximizing a monotone submodular function with matroid constraint, any algorithm that achieves an approximation exceeding 1 −1/e requires exponentially many queries (Nemhauser and Wolsey 1978).

Multilinear Extension. A canonical way to solve submodular maximization is to transform it into a continuous problem. We now introduce the tools used in this approach. For a vector x ∈[0, 1]N, let R(x) be a random subset of N where each element u ∈N is included in R(x) independently with probability xu. For a set function f: 2N →R, its multilinear extension F: [0, 1]N →R is defined as the expected value of f over the random set R(x), that is,

F(x) = E[f(R(x))]

=

X

S⊆N

" f(S) ·

Y u∈S xu ·

Y u/∈S

(1 −xu)

#

.

Although computing the exact value of F(x) requires exponentially many queries to f, it can be efficiently approximated by Monte Carlo sampling. For any vector x ∈[0, 1]N, the partial derivative of F at coordinate u satisfies ∂uF(x) = F (x + (1 −xu) · 1u) −F (x −xu · 1u), where 1u is the indicator vector for element u.

The matroid polytope of M is defined as

PM:=

( x ∈RN

≥0:

X u∈S xu ≤rank(S), ∀S ⊆N

)

.

36929

<!-- Page 3 -->

functions constraints approximation ratio amortized query complexity reference monotone cardinality

0.5 −ε O(ε−3k2 log5 n) Monemizadeh (2020) 0.5 −ε O(ε−11 log6 k log2 n) Banihashem et al. (2023a) 0.5 −ε O(ε−4 log4 k log2 n) Lattanzi et al. (2020b) 0.5 −ε O(ε−1k log2 k), Banihashem et al. (2024)

matroid

0.25 −ε O(ε−1k2 log2 n log3(ε−1k)) Duetting et al. (2023) 0.25 −ε O(k log k log3(ε−1k)) Banihashem et al. (2024) 0.3178 −ε O ε−2k3 log5(k/ε) log2 k this paper non-montone cardinality 0.125 −ε O(ε−1k log2 k) Banihashem et al. (2023b) 0.1667 −ε O(ε−1k2 log2 k) Liu and Yang (2024)

matroid 0.0932 −ε O(ε−1k2 log k log3(ε−1k)) Liu and Yang (2024) 0.1921 −ε O ε−2k3 log5(k/ε) log2 k this paper

**Table 1.** The approximation ratio and update complexity of both previous and our dynamic algorithms

Given vector x ∈PM, Cualinescu et al. (2011) proposed the so-called PIPAGEROUNDING that returns a discrete solution S ∈I satisfying f(S) ≥F(x) without making any queries to f.

Streaming and Dynamic Model. In the streaming model for submodular maximization, elements from the ground set arrive one by one in fixed order. Upon arrival of each element, the algorithm must determine whether to retain or permanently discard it, while maintaining at most O(poly(k), polylog(n)) elements in memory at all times. The algorithm may evaluate the submodular function on the subset of elements currently held in memory. After the stream terminates, the algorithm outputs a feasible set over the ground set with a guaranteed approximation ratio.

In the fully dynamic model, the algorithm receives a stream of both insertions and deletions of elements. After each update, it must output a solution over the current element set. Formally, the algorithm proceeds for T rounds. In each round 1 ≤i ≤T, there is a current ground set Ni ⊆N, which evolves by either inserting or deleting a single element, i.e., Ni+1 = Ni + u or Ni+1 = Ni −u for some element u. A dynamic algorithm is said to achieve a γ-approximation if, in every round i, it outputs a solution Si such that f(Si) ≥γf(OPTi), where OPTi denotes the optimal solution with respect to the ground set Ni. we use π to denote a stream over the ground set N, and similarly, we use πd to denote a dynamic stream that includes both insertions and deletions. The algorithm also requires only an average of O(poly(k), polylog(n)) queries per update.

Dynamic Algorithm for Monotone

Submodular Maximization

In this section, we describe our dynamic algorithm for montone functions; The analysis of the approximation guarantee and query complexity will be presented in the following section. Throughout this and the next section, we use the fixed constants ε ∈(0, 1] and α ≈1.14, where α is the unique positive solution to the equation α + 2 = eα. We begin this section by assuming access to the exact value of f(OPT); we will later show how this assumption can be eliminated.

For convenience, we denote f(OPT) by τ whenever no ambiguity arises. We further define the following two functions: lb(x) = log1+ε εx k and ub(x) = log1+ε(x)

.

Dynamic Data Structure. Our algorithm reduces the amortized query complexity by maintaining a data structure. The data structure consists of T = O(k log(k/ε)) levels. At each level i, it maintains a vector ai ∈[0, 1]N, O(log(k/ε)) independent sets {Aj,i}ub(τ)

j=lb(τ)

1, a candidate set Ri, and a selected element ui.

We begin by introducing our PICK algorithm, which is primarily used to compute ai and {Aj,i} at level i from ai−1 and {Aj,i−1} at level i −1 using the selected element ui. The algorithm takes as input a value a, a collection {Aj}, and an element u. It first queries the value of f(u). If f(u) does not lie in the interval [ετ/k, τ], the algorithm immediately returns False. Otherwise, it attempts to insert u into each Aj such that (1 + ε)i lies within the interval (−∞, ⌊logc(∂uF(a)⌋] ∩[lb(τ), ub(τ)], as long as the insertion preserves the matroid independence. If u is successfully inserted into some Aj, we increment the coordinate of a cor- responding to u by ε·(1+ε)i α·∂uF (a). If the above process results in any change to the sets Ai, the algorithm returns the updated vector a and the collection Ai. Otherwise, it returns False.

This algorithm can be used not only to acquire the i-th level’s data from the (i −1)-th level, but also to filter which elements in the (i −1)-th level can be used for effective updates. We say that an element u can be picked at level i if

PICK(ai−1, {Aj,i−1}, u, τ)̸ = False.

For convenience, we let Level 0 be the initialization level, where a0 = 0 and Aj = ∅for all i. For each 1 ≤i ≤T, Ri records all elements in Ri−1 that can be picked at level i. Then, ui is selected from Ri. It can perform a valid PICK at level i, and the result PICK(ai, {Aj,i}, ui, τ) is stored as {ai+1, {Aj,i+1}}.

1Throughout the rest of the paper, we encounter collections of sets denoted by {Aj,i}ub(τ)

j=lb(τ) and {Aj}ub(τ)

j=lb(τ) multiple times, where the index j always ranges from lb(τ) to ub(τ). For notational elegance, we write them as {Aj,i} and {Ai}, where the first subscript indicates the enumeration over the sets.

36930

<!-- Page 4 -->

As this data structure extends level by level, note that there are log1+ε(k/ε) sets {Aj,i}, and each Aj,i is an independent set containing at most k elements. Moreover, each level update inserts at least one element into some Aj,i. Therefore, after at most k log1+ε(k/ε) levels, no further elements can be picked. In practice, the process may terminate earlier if Ri = ∅for some level i < k log1+ε(k/ε). We define this level as the final level T of the data structure.

Upon reaching the final level T, we obtain a vector aT ∈ [0, 1]N such that F(aT) ≥

1 1+α −O(ε)

τ. Direct rounding cannot be applied to aT since it is only guaranteed to lie in the hypercube [0, 1]N, and not necessarily in the matroid polytope P(M).

To overcome this issue, we apply a procedure called PACK to the collection {Aj,T }. Specifically, the sets in {Aj,T } are partitioned into m:= ⌈α/ε⌉groups, where each group consists of sets whose indices are congruent modulo m. For each group of sets of the form Aj,T, Aj+m,T, Aj+2m,T,..., the algorithm initializes an empty set Si and processes the sets in decreasing order of indices, starting from the highestindexed set Aj+tm,T down to Aj,T, inserting elements into Si and keeping Si to be an independent set. This ensures that the average of the indicator vectors s:= 1 m

Pm i=1 1Si achieves multilinear value at least (1 −e−α −O(ε))f(a), and lies within the matroid polytope as each Si is a feasible independent set. Finally, we apply PIPAGEROUNDING(s) to obtain a discrete, feasible solution. Combined with the above guarantees, this yields a solution with provable approximation ratio. We note that the PACK algorithm incurs only Oε(k2) oracle queries, and thus we do not need to maintain the sets Si within the data structure. It suffices to run PACK on {Aj,T } once at the end of update.

We remark that both the PICK and PACK procedures are adapted from the streaming algorithm in Feldman et al. (2022). We just modify them to be compatible with our data structure.

Back to the data structure, if an update operation removes some element ui, it appears that we must reconstruct all levels following i in order to maintain correctness. If we were to reconstruct from level one after every update, this would incur at least an O(n) overhead. To avoid this, we ensure that in each update, the element ui is selected uniformly at random from Ri. As a result, a deletion triggers reconstruction at level i with probability only 1/|Ri|. Consequently, the earlier the level, the lower the probability of reconstruction, since the candidate sets satisfy Ri ⊆Ri+1.

We now describe how to reconstruct the data structure starting from level i. The corresponding procedure is given in Algorithm 4. The algorithm begins by generating a random permutation of the elements in Ri, and process them one by one. Suppose we are currently at level ℓ. If the current element u can be picked at level ℓand meet the element u, we update aℓand Aj,ℓaccordingly using u, and proceed to level ℓ+ 1 to process the next element. At this point, we postpone the computation of Rℓ+1. If, on the other hand, u cannot be picked at level ℓ, we perform a binary search backwards to find the most recent level z ≤ℓwhere u can still be picked. Once such a level is found, we add u to all sets

Rj for i < j ≤z. The correctness of this reconstruction algorithm relies on a key structural property: for each element u, the sets Ri satisfy a binary-searchable structure. Specifically, if u can be picked at some level z, then it must also be pickable at every earlier level j < z. We will formally prove this property in our analysis.

The algorithm finally reconstructs all information for level ℓ≥i. Moreover, since the reconstruction is driven by a random permutation over Ri, the selected element ui still preserves the original randomness assumption of being uniformly drawn from Ri.

## Algorithm

1: INITIALIZE(τ)

1 ai ←0 ∈[0, 1]N, Ai,j ←∅, Ri ←∅.

## Algorithm

2: PICK(a, {Aj}, u, τ)

1 if f(u) < ετ/k or f(u) > τ then

2 return False.

3 j(u) ←⌊logc(∂uF(a)⌋.

4 for i from lb(τ) to min{j(u), ub(τ)} do

5 if Aj + u ∈I then

6 Aj ←Aj + u.

7 a ←a + ε·(1+ε)i α·∂uF (a)1u.

8 if the above for loop results in no changes to any Ai then

9 return False.

10 else

11 return {a, {Ai}}.

## Algorithm

3: PACK({Aj}, τ)

1 m ←⌈α/ε⌉.

2 Sj ←∅for j ∈{0,..., m}.

3 for i from ub(τ) to lb(τ) do while ∃u ∈Aj \ S(j mod m) with

S(j mod m) + u ∈I do

5 S(j mod m) ←S(j mod m) + u.

6 s ←1 m t X j=1

1Sj.

7 return PIPAGEROUNDING(s).

Insertion. When an element u is inserted, we traverse the data structure from level 1 to T. At level i, if u can’t be picked, then it can’t be picked anymore at any deeper level either, and can thus be safely ignored. Otherwise, we attempt to insert it into Ri to maintain a uniform distribution: we add u to Ri and select it as the new ui with probability 1 |Ri|. If u is selected as ui, and then reconstruct the data structure from level i. Else, we proceed to the next level.

36931

<!-- Page 5 -->

## Algorithm

4: MATROIDCONSTRUCTLEVEL(i, τ)

## 1 Let P be a random permutation of elements of

Ri.

2 ℓ←i.

3 for u in P do

4 if PICK(aℓ−1, {Aj,ℓ−1}, u, τ)̸ = False then

{aℓ, {Aj,ℓ}} ←PICK(aℓ−1, {Aj,ℓ−1}, u, τ).

6 Rℓ+1 ←∅, ℓ←ℓ+ 1, uℓ←u.

7 else

## 8 Run binary search to find the lowest

z ∈[i, ℓ−1] such that PICK(az, {Aj,z}, u, τ) = False.

9 for r from i + 1 to z do

10 Rr ←Rr + u.

11 return T ←ℓ−1 which is the final ℓthat the for-loop above returns subtracted by one.

## Algorithm

5: INSERT(u, τ)

1 R0 ←R0 + u.

2 for i from 1 to T + 1 do

3 if PICK(ai−1, {Aj,i−1}, u, τ) = False then

4 break.

Ri ←Ri + u.

6 Let pi with probability 1 |Ri|, and otherwise pi = 0.

7 if pi = 1 then

8 ui ←u.

9 {ai, {Aj,i}} ←PICK(ai−1, {Aj,i−1}, u, τ).

10 Ri+1 ←{v ∈Ri:

PICK(ai−1, {Aj,i}, v, τ)̸ = False}.

11 MATROIDCONSTRUCTLEVEL(i + 1).

12 return PACK({Aj,T }).

Deletion. The deletion operation is simpler: we iterate from level 1 to T and remove the element u from each Ri until either u /∈Ri or u = ui. In the former case, we terminate the process; in the latter, we trigger a reconstruction starting from level i. This procedure naturally preserves the uniformity of the selected representatives ui, since in levels where no reconstruction occurs, we are merely removing u from the candidate set, which does not affect the uniform distribution of the remaining elements.

After the insertion or deletion, we send the collection {Aj,T } into the PACK algorithm to obtain the final result.

Relaxing the assumption of known f(OPT). Finally, we discuss how to eliminate the assumption that τ = f(OPT). The technique we employ was first introduced by (Monemizadeh 2020) and has been widely adopted in the context of dynamic algorithms for submodular maximization.

First, it is easy to show that if we are given an estimate τ ′ ∈[f(OPT), (1 + ε)f(OPT)] instead of the exact value f(OPT), then the resulting loss in the approximation guarantee is only additive in ε.

## Algorithm

6: DELETE(u, τ)

1 R0 ←R0 −u.

2 for i from 1 to T + 1 do

3 if u /∈Ri then

4 return False.

Ri ←Ri −u.

6 if ui = u then

7 MATROIDCONSTRUCTLEVEL(i).

8 return PACK({Aj,T }).

We then assume that there exist infinitely many parallel instances of the dynamic algorithm, each indexed by an integer i, where the i-th instance assumes τ = (1 + ε)i as an estimate for f(OPT), and each process maintains its own data structure independently.

Whenever an element u is inserted or deleted, we only need to update those processes i for which f(u) ∈ ε(1 + ε)i/k, (1 + ε)i

, and the number of such processes is at most O(log1+ε(k/ε)). In all other processes, the element u will be filtered out during the first step of PICK. Therefore, it suffices to perform the insertion or deletion operation only for these relevant instances. Putting everything together, our final algorithm is presented as Algorithm 7.

## Algorithm

7: DYNAMICMATROID(M(N, I), πd)

1 Let i denote whether the process with the guess f(OPT) = (1 + ε)i.

2 for all command in πd do

3 if the command is insert the element u then

4 for i with f(u) ∈[ ε(1+ε)i k, (1 + ε)i] do

INSERT(u, (1 + ε)i).

6 if the command is delete the element u then

7 for i with f(u) ∈[ ε(1+ε)i k, (1 + ε)i] do

8 DELETE(u, (1 + ε)i).

The following theorem summarizes the guarantees of our algorithm. We defer its proof to the next section. Theorem 1. For a monotone submodular function f and a fully dynamic stream with insertion and deletion, DYNAMICMATROID guarantees a (0.3178 −O(ε))approximation and have amortized query complexity O(ε−2k3 log(k) log3(k/ε)).

## Analysis

In this section, we prove Theorem 1. We first prove the correctness of the binary search procedure in Algorithm 4. Then, we explain the properties maintained by the data structure after each dynamic update. Finally, we leverage these properties to derive the algorithm’s approximation guarantee and its average query complexity.

36932

<!-- Page 6 -->

Correctness of Binary Search. We first observe that during the execution of algorithm 4 at level i, the stored vectors and sets from level i to level T are monotonically increasing.

Observation 2. After the execution of MATROIDCONSTRUCTLEVEL(x, τ), for any x ≤y ≤ z ≤T and lb(τ) ≤j ≤ub(τ) we have ay < az and Aj,y ⊆Aj,z.

Based on this observation, we proceed to prove the following lemma.

Lemma 3. After the execution of MATROIDCONSTRUCTLEVEL(x, τ), for any x ≤y ≤z ≤ T and any element u ∈Rx, if PICK(ax, {Aj,x}, u, τ) = False, then PICK(ay, {Aj,y}, u, τ) = False.

Proof. PICK(ax, {Aj,x}, u, τ) = False means that at least one of the following three situations must occur:

1. f(u) ≤ετ/k or f(u) ≥τ; 2.

log1+ε(∂uF(ax))

≤lb(τ); 3. for all lb(τ) ≤j ≤min{ log1+ε(∂uF(ax))

, ub(τ)}, Aj,x + u /∈I.

The first case directly leads to the conclusion we aim to prove. By submodularity of F and ax < ay we have ∂uF(ay) ≤∂uF(ax). Hence, the second case implies that log1+ε(∂uF(ay)

≤lb(τ), and combining with Aj,x ⊆ Aj,y the third case impiles that Aj,y + u /∈I for all lb(τ) ≤j ≤min{ log1+ε(∂uF(ay))

, ub(τ)}.

Lemma 3 means that for any u ∈Rx, there exist index y > x such that, PICK(az, {Aj,z}, u, τ) = False if and only if z ≥x. Thus, we can perform a binary search to find this z in algorithm 4 to acquire Ri correctly.

Theorem 4. After the execution of MATROIDCONSTRUCTLEVEL(x, τ), we have

Ri = {u ∈Ri−1: PICK(ai−1, {Aj,i}, u, τ)̸ = False}

for any x < i ≤T.

Maintaining Invariants. Now we can proceed to establish the invariants maintained by this data structure.

Theorem 5. After each INSERT or DELETE operation, the data structure maintains the following properties for any 1 ≤i ≤T:

1. T = O(k log(k/ε)). 2. Ri = {u ∈Ri−1: PICK(ai−1, {Aj,i}, u, τ)̸ = False}. 3. {ai, {Aj,i}} = PICK(ai−1, {Aj,i−1}, ui, τ). 4. ui is picked uniformly at random from Ri. Formally, if we treat the contents of the data structure as random variables, with the randomness stemming from the algorithm’s internal random seed, and denote them in boldface then for u ∈Ri, we have Pr[u = ui | T ≥i, u1 = u1, u2 = u2,..., ui−1 = ui−1].

Proof. We observe that during each deletion or insertion operation, the algorithm performs at most one level construction. Suppose the level construction is triggered at level x. For Property 2 and Property 3, if they hold for all levels 1 ≤

## Algorithm

8: STREAMALG(M(N, I), π, τ)

1 a ←[0, 1]N.

2 Aj ←∅for j ∈{lb(τ), lb(τ) + 1,..., ub(τ)}.

3 for every arriving element u ∈π do

4 if PICK(a, {Aj}, u)̸ = False then

5 {a, {Aj}} ←PICK(a, {Aj}, u).

6 return PACK{Aj}.

i < x before the update, they continue to hold afterwards as those levels remain unchanged. For levels x ≤i ≤T, Property 2 is guaranteed by the lemma 3, and Property 3 holds because the execution of line 5−6 of MATROIDCON- STRUCTLEVEL.

We remark that the proof of Property 4 is essentially identical to that in (Banihashem et al. 2024), and we omit it for brevity. This concludes the proof.

Approximation Guarantee. We can use the properties of the above data structure to establish the approximation ratio of the algorithm.

We first state the approximation guarantee of the STREA- MALG algorithm. Here, we point out that this algorithm is a modified version of that in Feldman et al. (2022). We modify it by avoiding using the sliding window technique to ensure it can be more effectively maintained by our dynamic data structure. Our proof follows a similar approach to that of Feldman et al. (2022) so we defer it to the appendix; here we only present the main theorems.

Theorem 6. For a submodular function f: 2N →R and an arbitrary data stream π, if we are given in advance a value τ ∈[f(OPT), (1 + ε)f(OPT)], then Algorithm 8 returns a set S with f(S) ≥(1−e−α

1+α −O(ε)) · f(OPT) ≈0.3178 − O(ε) · f(OPT).

Next, we show that after each update, the solution maintained by our data structure preserves the same approximation guarantee. In fact, the data structure is designed to faithfully simulate the execution of STREAMALG on a specific input stream.

Theorem 7. After each INSERT or DELETE operation, our data structure simulates STREAMALG with data stream π = (R0 \ R1, u1, R1 \ R2, u2,,..., RT −1, uT), where where each set Rt \ Rt+1 appears as a contiguous block, and the elements within each block can be arranged in an arbitrary order. Hence, our algorithm returns a solution S with f(S) ≥(0.3178 −O(ε)) · f(OPT) after each update.

Proof. According to Properties 2 and 3 of Theorem 5, we consider the execution of STREAMALG on the stream π. The algorithm first picks u1 and updates accordingly. Then, Property 2 implies that after u1 is picked, the elements will no longer be picked for all elements in R0 \ R1. Hence we can just skip them without leading to any effective update. The algorithm then picks u2 and skips all elements in

36933

<!-- Page 7 -->

R1 \ R2, accepts u3, and so on, proceeding through the entire stream. After doing so, it produces the solution vector aT, {Ai,T }. Finally, the algorithm passes this information to PACK, which returns a set S, just as it does in the INSERT and DELETE procedures.

Query Complexity. We first note that our algorithm uses an estimated value of F via sampling. Nevertheless, we can show that compared to using the exact value of F, this only incurs an additional overhead of ˜Oε(k2) and results in at most an ε loss in the approximation ratio. This allows us to incur an additional ˜Oε(k2) factor in the query complexity when converting between queries to f and F.

Lemma 8. If we use Monte Carlo sampling to estimate the value of F instead of accessing its exact value in our dynamic algorithm, then using O ε−2k2 log2(k/ε) log k value oracle of f per evaluation suffices to return a solution S whose value f(S) is within an additive εf(OPT) error, with failure probability o(1).

We also state the queries required by PIPAGEROUNDING algorithm.

Theorem 9 (Cualinescu et al. (2011)). The PIPAGEROUND- ING algorithm takes as input a vector x ∈[0, 1]N. It uses supp2(x) membership oracle queries and does not require any value oracle queries, where supp(x) denotes the number of nonzero components in x.

Observe that in our algorithm, the support of any vector x used has size at most O(k log(k/ε)). Therefore, PIPAGER- OUNDING does not constitute the main part of the query complexity of our algorithm.

Then we analyze the algorithm MATROIDCON- STRUCTLEVEL, and further examine the amortized query complexity of INSERT and DELETE.

Lemma 10. MATROIDCONSTRUCTLEVEL(i, τ) requires O

|Ri|ε−2k2 log3(k/ε) log2 k orcale queries.

Proof. All oracle queries in the execution of MATROID- CONSTRUCTLEVEL are made within calls to PICK. We first count the number of calls to PICK. Each element in every set Ri is invoked in a single call to PICK at Line 4 of the algorithm. Additionally, for each element that returns False by PICK, the algorithm performs a binary search (line 8), which incurs at most O(log T) = O(log(k/ε)) further calls to PICK per element. Thus We totally need O(|Ri| log(k/ε)) calls of PICK.

Each PICK operation queries the value of the multilinear extension once, and queries the independence of at most O(log(k/ε)) sets, so each PICK requires at most O ε−2k2 log2(k/ε) log k oracle queries, where the value oracle dominates. Thus, the execution of MATROIDCON- STRUCTLEVEL uses

O

|Ri|ε−2k2 log3(k/ε) log2 k oracle queries in total.

Lemma 11. Both INSERT(u, τ) and DELETE(u, τ) require O ε−2k3 log4(k/ε) log2 k amoritzed oracle queries.

Proof. Due to Property 4 of Theorem 5, we know that each update calls MATROIDCONSTRUCTLEVEL(i, τ) with probablity 1 |Ri|. By linearity of expectation, the total expected number of oracle queries by MATROIDCONSTRUCTLEVEL is:

T X i=1

1 |Ri|O

|Ri|ε−2k2 log3(k/ε) log2 k

= O ε−2k3 log4(k/ε) log2 k

.

Each update also invokes the PACK algorithm, which does not make any value oracle queries. It only performs O(k log(k/ε)) + O(k2 log2(k/ε)) = O(k2 log2(k/ε)) membership oracle queries, which are negligible in terms of the overall query complexity, which complete the proof.

Finally, since the technique for removing the assumption on τ incurs only an additional log(k/ε) factor, the final theorem follows immediately.

Theorem 12. DYNAMICMATROID algorithm requires at most O ε−2k3 log5(k/ε) log2 k amortized oracle queries.

Dynamic Algorithm for Non-monotone

Submodular Functions The approach for the non-monotone case is largely similar; we essentially replace the original PICK and PACK procedures with their non-monotone counterparts, PICKNM and PACKNM, both adapted from Feldman et al. (2022). Notably, we identified a minor error in the proof of the original PACK algorithm and fixed it through a modification of the algorithm. Due to space limitations, we defer the algorithm DYNAMICMATROIDNM and its analysis to the appendix.

Theorem 13. For a submodular function f and a fully dynamic stream with insertion and deletion, DY- NAMICMATROIDNM guarantees a (0.1921 −O(ε))approximation and have amortized query complexity O(ε−2k3 log(k) log3(k/ε)).

## Conclusion

In recent years, the dynamic model has attracted considerable attention in submodular maximization, leading to a number of intriguing advances. In this work, we significantly improve the approximation ratios for both the monotone and non-monotone settings of fully dynamic submodular maximization under matroid constraints. Our algorithm is independent of the ground-set size n, though its dependence on the rank k remains relatively high. This, however, is unavoidable, since even approximating the multilinear extension requires ˜O(k2) time. A major open question also remains: whether one can design algorithms with poly(log n, log k) update complexity under matroid constraints, analogous to what is achievable under cardinality constraints.

36934

<!-- Page 8 -->

## Acknowledgments

This work was supported in part by the National Natural Science Foundation of China Grants No. 62272441, 62402110.

## References

Bach, F. R. 2010. Structured sparsity-inducing norms through submodular functions. In Advances in Neural Information Processing Systems 23: 24th Annual Conference on Neural Information Processing Systems 2010. Proceedings of a meeting held 6-9 December 2010, Vancouver, British Columbia, Canada, 118–126. Curran Associates, Inc. Bairi, R.; Iyer, R. K.; Ramakrishnan, G.; and Bilmes, J. A. 2015. Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures. In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing of the Asian Federation of Natural Language Processing, ACL 2015, July 26-31, 2015, Beijing, China, Volume 1: Long Papers, 553–563. The Association for Computer Linguistics. Banihashem, K.; Biabani, L.; Goudarzi, S.; Hajiaghayi, M.; Jabbarzade, P.; and Monemizadeh, M. 2023a. Dynamic Constrained Submodular Optimization with Polylogarithmic Update Time. In International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA, volume 202 of Proceedings of Machine Learning Research, 1660–1691. PMLR. Banihashem, K.; Biabani, L.; Goudarzi, S.; Hajiaghayi, M.; Jabbarzade, P.; and Monemizadeh, M. 2023b. Dynamic Non-monotone Submodular Maximization. In Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023. Banihashem, K.; Biabani, L.; Goudarzi, S.; Hajiaghayi, M.; Jabbarzade, P.; and Monemizadeh, M. 2024. Dynamic Algorithms for Matroid Submodular Maximization. In Proceedings of the 2024 ACM-SIAM Symposium on Discrete Algorithms, SODA 2024, Alexandria, VA, USA, January 7-10, 2024, 3485–3533. SIAM. Buchbinder, N.; and Feldman, M. 2024. Constrained Submodular Maximization via New Bounds for DR- Submodular Functions. In Proceedings of the 56th Annual ACM Symposium on Theory of Computing, STOC 2024, Vancouver, BC, Canada, June 24-28, 2024, 1820–1831. ACM. Chen, X.; and Peng, B. 2022. On the complexity of dynamic submodular maximization. In STOC ’22: 54th Annual ACM SIGACT Symposium on Theory of Computing, Rome, Italy, June 20 - 24, 2022, 1685–1698. ACM. Cualinescu, G.; Chekuri, C.; P´al, M.; and Vondr´ak, J. 2011. Maximizing a Monotone Submodular Function Subject to a Matroid Constraint. SIAM J. Comput., 40(6): 1740–1766. Das, A.; and Kempe, D. 2011. Submodular meets Spectral: Greedy Algorithms for Subset Selection, Sparse Approximation and Dictionary Selection. In Proceedings of the 28th International Conference on Machine Learning, ICML

2011, Bellevue, Washington, USA, June 28 - July 2, 2011, 1057–1064. Omnipress. Das, A.; and Kempe, D. 2018. Approximate Submodularity and its Applications: Subset Selection, Sparse Approximation and Dictionary Selection. J. Mach. Learn. Res., 19: 3:1–3:34. Duetting, P.; Fusco, F.; Lattanzi, S.; Norouzi-Fard, A.; and Zadimoghaddam, M. 2023. Fully Dynamic Submodular Maximization over Matroids. In International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA, volume 202 of Proceedings of Machine Learning Research, 8821–8835. PMLR. Feldman, M.; Liu, P.; Norouzi-Fard, A.; Svensson, O.; and Zenklusen, R. 2022. Streaming Submodular Maximization Under Matroid Constraints. In 49th International Colloquium on Automata, Languages, and Programming, ICALP 2022, July 4-8, 2022, Paris, France, volume 229 of LIPIcs, 59:1–59:20. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Gharan, S. O.; and Vondr´ak, J. 2011. Submodular Maximization by Simulated Annealing. In Proceedings of the Twenty-Second Annual ACM-SIAM Symposium on Discrete Algorithms, SODA 2011, San Francisco, California, USA, January 23-25, 2011, 1098–1116. SIAM.

Kempe, D.; Kleinberg, J. M.; and Tardos, ´E. 2003. Maximizing the spread of influence through a social network. In Proceedings of the Ninth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Washington, DC, USA, August 24 - 27, 2003, 137–146. ACM. Khanna, R.; Elenberg, E. R.; Dimakis, A. G.; Negahban, S. N.; and Ghosh, J. 2017. Scalable Greedy Feature Selection via Weak Submodularity. In Proceedings of the 20th International Conference on Artificial Intelligence and Statistics, AISTATS 2017, 20-22 April 2017, Fort Lauderdale, FL, USA, volume 54 of Proceedings of Machine Learning Research, 1560–1568. PMLR. Kumari, L.; and Bilmes, J. A. 2021. Submodular Span, with Applications to Conditional Data Summarization. In Thirty- Fifth AAAI Conference on Artificial Intelligence, AAAI 2021, Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021, The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI 2021, Virtual Event, February 2-9, 2021, 12344–12352. AAAI Press. Lattanzi, S.; Mitrovic, S.; Norouzi-Fard, A.; Tarnawski, J.; and Zadimoghaddam, M. 2020a. Fully Dynamic Algorithm for Constrained Submodular Optimization. In Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. Lattanzi, S.; Mitrovic, S.; Norouzi-Fard, A.; Tarnawski, J.; and Zadimoghaddam, M. 2020b. Fully Dynamic Algorithm for Constrained Submodular Optimization. CoRR, abs/2006.04704. Liu, Y.; and Yang, W. 2024. Dynamic Algorithms for Nonmonotone Submodular Maximization. In Combinatorial

36935

<!-- Page 9 -->

Optimization and Applications - 17th International Conference, COCOA 2024, Beijing, China, December 6-8, 2024, Proceedings, Part II, volume 15435 of Lecture Notes in Computer Science, 119–131. Springer. Monemizadeh, M. 2020. Dynamic Submodular Maximization. In Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual. Nemhauser, G. L.; and Wolsey, L. A. 1978. Best Algorithms for Approximating the Maximum of a Submodular Set Function. Math. Oper. Res., 3(3): 177–188. Qi, B. 2022. On Maximizing Sums of Non-Monotone Submodular and Linear Functions. In 33rd International Symposium on Algorithms and Computation, ISAAC 2022, December 19-21, 2022, Seoul, Korea, volume 248 of LIPIcs, 41:1–41:16. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Radanovic, G.; Singla, A.; Krause, A.; and Faltings, B. 2018. Information Gathering With Peers: Submodular Optimization With Peer-Prediction Constraints. In Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the 8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018, 1603–1610. AAAI Press. Vondr´ak, J. 2008. Optimal approximation for the submodular welfare problem in the value oracle model. In Proceedings of the 40th Annual ACM Symposium on Theory of Computing, Victoria, British Columbia, Canada, May 17- 20, 2008, 67–74. ACM. Zheng, J.; Jiang, Z.; Chellappa, R.; and Phillips, P. J. 2014. Submodular Attribute Selection for Action Recognition in Video. In Advances in Neural Information Processing Systems 27: Annual Conference on Neural Information Processing Systems 2014, December 8-13 2014, Montreal, Quebec, Canada, 1341–1349.

36936
