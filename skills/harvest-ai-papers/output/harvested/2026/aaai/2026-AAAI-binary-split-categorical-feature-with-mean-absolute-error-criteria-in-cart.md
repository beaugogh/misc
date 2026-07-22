---
title: "Binary Split Categorical Feature with Mean Absolute Error Criteria in CART"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40020
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40020/43981
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Binary Split Categorical Feature with Mean Absolute Error Criteria in CART

<!-- Page 1 -->

Binary Split Categorical Feature with Mean Absolute Error Criteria in CART

Peng Yu1,2,3, Yike Chen1, Chao Xu1*, Albert Bifet3,4, Jesse Read5

## 1 University of Electronic Science and Technology of China 2

Shopify 3 T´el´ecom Paris, Institut Polytechnique de Paris 4 The University of Waikato 5 ´Ecole Polytechnique, Institut Polytechnique de Paris peng.yu@shopify.com, cyike9982@gmail.com, cxu@uestc.edu.cn, albert.bifet@telecom-paris.fr, jesse.read@polytechnique.edu

## Abstract

In the context of the Classification and Regression Trees (CART) algorithm, the efficient splitting of categorical features using standard criteria like GINI and Entropy is wellestablished. However, using the Mean Absolute Error (MAE) criterion for categorical features has traditionally relied on various numerical encoding methods. This paper demonstrates that unsupervised numerical encoding methods are not viable for the MAE criteria. Furthermore, we present a novel and efficient splitting algorithm that addresses the challenges of handling categorical features with the MAE criterion. Our findings underscore the limitations of existing approaches and offer a promising solution to enhance the handling of categorical data in CART algorithms.

## Introduction

The CART family of algorithms (random forest, gradient boosting tree) is well-known for its top performance on tabular data. Real-world tabular data often contains not only numerical but also categorical features. The CART algorithm recursively partitions the input dataset with a binary split optimization step and terminates when reaching a minimum number of instances. While traditional machine learning models only work with numerical data, the CART family of algorithms can process categorical features directly. This flexibility is because the binary split optimization step in the CART algorithm only requires feature data types that allow for different subsets.

The binary split step is recognized as a major bottleneck regarding the computational efficiency of tree learning algorithms (Catlett 1991). Specifically, when processing categorical features, the associated discrete set topology can result in an exponential search space for binary splits. As a result, various numerical encoding methods have been developed to address this limitation. Consequently, many popular tree-based machine learning software packages (such as XGBoost (Chen and Guestrin 2016), LightGBM (Ke et al. 2017), and Catboost (Prokhorenkova et al. 2018)) only support numerical data or include automatic numerical encoding methods for categorical data. On the other hand, only

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

a subset of splitting criteria (such as mean squared error and Gini impurity) have optimally guaranteed numerical encodings for categorical data (Hastie, Tibshirani, and Friedman 2001). The splitting criterion MAE (Mean Absolute Error) lacks a proven optimal numerical encoding. MAE is more robust when dealing with outliers and skewed distributions and is widely adopted in various statistical domains. The most successful and practical numerical encoding method for this criterion is a median-based heuristic numerical encoding. This heuristic has been implemented in scikit-learn, and takes O(n2) time, where n is the dataset size (jiangfeng 2017). Unfortunately, O(n2) running time is too slow for practical purposes. The community suggests using subsampling to avoid the running time issue at the cost of finding a worse split, which is the standard in LightGBM.

Our Contributions We are motivated by two open problems: whether there is a numerical encoding that works for MAE, and if not, does there exist a fast exact algorithm for binary split through MAE?

1. We prove that no unsupervised numerical encoding method is optimal for MAE, and show a median heuristic could be twice the optimal. While the proof itself is relatively straightforward, the significance of this result is reflected in the substantial effort invested in seeking the optimal numerical encoding method. For instance, dozens of unsupervised numerical encoding methods are under development (McGinnis et al. 2018).

2. We develop an exact and completely new algorithm to solve the binary split of categorical features with the MAE criterion in O(n log n+k log k log n) time without using numerical encoding, where n is the number of data points and k is the number of categories. The new algorithm is faster than the current heuristics, and also gives the exact result. So it both handles real-world size data without subsampling and is completely optimal. The new algorithm may also hold independent interest, as it solves the unimodal cost 2-median problem, which generalizes various problems studied in computational geometry literature.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

27961

<!-- Page 2 -->

## Preliminaries

In regression tree learning, during a node split computation, the goal is to find a binary partition S, Sc of Y ∈Rn, based on some feature X. Here, Sc is the complement of S with respect to Y. When X is categorical, the goal can be further simplified as finding a binary partition of Y = {Y1, Y2,... Yk}, where Yi ⊆R is the subset of the target data points with category i in feature X. We assume the collection of data points in Y is a set, and they are all disjoint. This is only for the benefit of exposition. Everything would still hold with proper definition if repeated data points are allowed. One easy way is to assume that if there are copies of the same element, we just perturbed each one of them by an infinitesimal amount, so all data points are unique.

Depending on the splitting criteria, the partition must maximize or minimize an objective function. For a given set S ⊆Y, the MAE is defined as

MAE(S) = min a∈R

X x∈∪S

|x −a|. (1)

The a achieving the minimum is M(∪S), where M(·) is the median of the input. Define the error of a split S and Sc as λ(S), which is the sum of their MAE.

λ(S):= MAE(S) + MAE(Sc). (2) When using MAE as the splitting criterion, the objective value would be the minimum over all splits:

λ:= min S⊂Y,S̸=∅λ(S). (3)

The problem of computing the split S, Sc that achieves the minimum λ(S) is referred to as the MAE split problem.

To solve for the minimum, one can enumerate all subsets of Y, resulting in an undesirable O(2k) search space. On the other hand, the community has developed numerous heuristic numerical encoding methods.

Y1 Y1

Y2 Y2

Y3 Y3

Y4 Y4 e(Y4) e(Y4) e(Y3) e(Y3) e(Y2) e(Y2) e(Y1) e(Y1) R

**Figure 1.** A example where Y = {Y1, Y2, Y3, Y4}, and the encoding function e maps elements in Y to R. There are 5 downward closed sets, and 3 of them splits, so D(Y, e) = {{Y1}, {Y1, Y3}, {Y1, Y3, Y2}}.

Unsupervised Numerical Encoding Rather than enumerating all subsets, one can employ a numeric encoding/set function e: 2R →R to establish an ordering ⪯e and select sets based on this ordering.

A numerical encoding function is considered unsupervised if specified independently of the data, meaning it is determined without observing the input.

The numerical encoding provides a natural ordering over the elements of Y, where A ⪯e B if e(A) ≤e(B). We define the downward closed sets of Y as D′(Y, e), which consists of sets of the form {A | e(A) ≤x, A ∈Y} for some x.

Numerical encoding has been used as a heuristic to identify the optimal partition within the downward closed sets. Specifically, let D(Y, e) = D′(Y, e) \ {Y, ∅}, which are downward closed sets that splits Y into two non-empty sets. See Figure 1 for example. Our goal is to find S ∈D(Y, e) that minimizes the objective λ. This modified problem leads to a more favorable O(k) search space, although optimality is not guaranteed.

For instance, the median heuristic employs the encoding function e = M by arranging sets based on their medians. It then enumerates the downward closed sets and their complements as potential splits. Consequently, this approach yields only k −1 potential splits, which can be tested one by one and return the optimum.

Piecewise-linear functions We also introduce a few useful functions and their properties. A function f: R →R is unimodal, if there exists a c such that for any x ≤y ≤c, we have f(x) ≥f(y), and for c ≤x ≤y, f(x) ≤f(y).

A function h: R × R →R is totally monotone, if for any x1 ≤x2 ≤y1 ≤y2, h(x1, y1) ≥h(x1, y2) then h(x2, y1) ≥h(x2, y2). A positive linear combination of totally monotone functions is totally monotone. A matrix is totally monotone if the function h(i, j) = Mi,j is totally monotone. The main property of a totally monotone matrix is the index for row minimum is non-decreasing. That is, if Mi,ai is the minimum value of the ith row, then we have a1 ≤a2 ≤... ≤an (Park 1999).

We use B(f) to denote the set of breakpoints for a piecewise-linear function. Recall the median function M(S) is an element y ∈S, such that P x∈S |x −y| is minimized.

Splitting Criteria Numerical Encoding Optimal MSE Mean ✓ Gini impurity Single class percentage ✓ MAE One-hot × MAE Median ×

**Table 1.** Comparison of unsupervised encoding for different criteria.

Numerical Encoding and Median Heuristic Is there a numerical encoding that can be used to find the optimal binary split for MAE? Specifically, is there an encoding function e such that the following equality holds: λ is equal to minS∈D(Y,e) λ(S)?

**Table 1.** shows target mean-based numerical encoding for categorical features has been proven optimal in decision tree regression with mean squared error (MSE) in (Breiman et al. 1984), the same heuristic does not work with MAE. Still, this does not rule out the existence of other unsupervised numerical encodings that work for MAE. Unfortunately, we prove that such encoding cannot exist.

27962

<!-- Page 3 -->

Suppose a unique optimal partition of a dataset minimizes the MAE. In that case, any encoding that works for MAE must have the encoding of all elements in one partition strictly smaller than or greater than the encoding of the other partition. Formally, let {A, B} forms the unique optimum partition of dataset Y, and e is a encoding that works for MAE, then either e(A) < e(B) for all A ∈A and B ∈B, or e(A) > e(B) for all A ∈A and B ∈B. If the encoding e works for MAE, then the optimal partition is in D(Y, e). Theorem 1. No numerical encoding function works for binary split with MAE splitting criteria.

Proof. Assume such an encoding e exists and prove by contradiction via constructing a counter-example. Let ϵ > 0 be some small and fixed value, say 0.01.

Let a1 = 0, a2 = 2, a3 = 3, a4 = 5. We define Ai = {ai −ϵ, ai, ai + ϵ}, A′ i = {ai −ϵ, ai + ϵ, a1} if i ∈{3, 4}, otherwise A′ i = {ai −ϵ, ai + ϵ, a4}.

1. The unique optimum partition of {A1, A′ 1, A4, A′ 4} is {A1, A′

1}, {A4, A′ 4}, without loss of generality, let e(A1) < e(A4). 2. The unique optimum partition of {A2, A′ 1, A3, A′ 4} is {A2, A′

1}, {A3, A′ 4}, hence e(A′ 1) < e(A′ 4). 3. The unique optimum partition of {A2, A′ 2, A3, A′ 3} is {A2, A′

2}, {A3, A′ 3}, hence e(A2) < e(A3). 4. The unique optimum partition of {A1, A′ 2, A′ 3, A4} is {A1, A′

3}, {A′ 2, A4}, hence e(A4) < e(A1), a contradiction.

Now we know that any encoding-based heuristic would not give the correct result, but maybe it can still give a good enough result. To answer this, we examine the limitations of the most widely used encoding-based heuristic, the median heuristic.

Empirically, it has been shown that the median numerical encoding works most of the time for MAE splitting criteria (Torgo 1999). The conclusion is made based on experiments on limited datasets. The median encoding result in sub-optimal splits was only observed through some rare, randomly generated datasets.

However, we design an input so that the median heuristic is almost twice as bad as the optimum. Let n be an even integer. Consider 4 collections of data points Y0, Y1, Y2, Y3. Y0, Y1 consists of n copies of 0 and 1, respectively. Let Y2 consist of n/2 copies of 0, n/2 + 1 copies of 0.5 + ϵ, and Y3 consists of n/2 copies of 1 and n/2 + 1 copies of 0.5 − ϵ. Using the median heuristic, the potential points to split are 0, 0.5 −ϵ, 0.5 + ϵ, 1. Observe that no matter which one is chosen, the output of the median heuristic would give a solution of value n + 2ϵ. The actual optimal would give a value around n/2 + 1.

## Methodology

Knowing that no unsupervised numerical encoding e works for MAE, there might still be efficient algorithms that give the exact solution and don’t use any encoding. In the following section, we propose such an algorithm. The algorithm is a fairly complicated divide-and-conquer that uses tools in computational geometry.

We first transform the MAE split problem into a more manageable version, where instead of optimization of subsets (which can be as large as 2k), it becomes optimizing over O(n2) points. Lemma 1. Let Y be a family of disjoint sets. Then λ = min ∅⊊S⊊Y

MAE(S) + MAE(Sc)

can be equivalently written as λ = min a,b ∈R

X

S ∈Y min

X i ∈S

|i −a|,

X j ∈S

|j −b|

.

Proof. By definition,

MAE(S) = min a ∈R

X i∈S S

|i −a|.

Hence, for any subset S ⊆Y with complement Sc, we have

MAE(S) + MAE(Sc) = min a∈R

X i∈∪S

|i −a|

+ min b∈R

X j∈∪Sc

|j −b|.

Note that S S and S Sc partition all elements in S Y. We may reorganize the sums set by set (i.e., over each S ∈Y), introducing two real parameters a and b. Gathering the terms for each S and observing that the choice min

X i∈S

|i −a|,

X j∈S

|j −b| corresponds to placing S into S or its complement Sc, respectively, yields min ∅⊊S⊊Y

MAE(S) + MAE(Sc)

= min a,b ∈R

X

S ∈Y min

X i∈S

|i −a|,

X j∈S

|j −b|

.

This confirms the claimed equivalence, completing the proof.

After the transformation, we consider the following optimization problem. Problem 1 (Median split problem). Given Y, a family of subsets of R, find a, b ∈R, such that P

S∈Y min(P i∈S |i − a|, P j∈S |j −b|) is minimized.

We define a few more substitutions to simplify (and at the same time, generalize) the problem even further.

Define fS(x) = P y∈S |y −x|. Observe that we try to optimize g(a, b) = P

S∈Y min{fS(a), fS(b)}. Note that each fS is piecewise-linear and unimodal. Indeed, let c = M(S), when x < c, fS is monotonically decreasing and when x > c, fS is monotonically increasing. Hence, fS is unimodal. We use this property to design a much faster algorithm. To this end, we introduce a much more general problem, the Unimodal Cost 2-Median problem (UC2M).

27963

<!-- Page 4 -->

## Algorithm

1: Binary MAE Split Function BINARYMAESPLIT:

Input: data C ←list of categories of the feature foreach c ∈C do

G ←∅ foreach (r, c) ∈data do add function x 7→|r −x| to G end fc ←P g∈G g end return UNIMODAL2MEDIAN({ fc | c ∈C })

Problem 2 (Unimodal Cost 2-Median (UC2M)). Let f1,..., fk: R →R be k piecewise-linear unimodal functions with a total of n breakpoints. Let g(a, b) = Pk i=1 min{fi(a), fi(b)}. Find a, b ∈R such that it minimizes g.

Theorem 2. Problem 1 reduces to Problem 2 in linear time.

Proof. Let fS = P i∈S |i−x|. Let the input to the Problem 1 be Y = {S1,..., Sk}. This reduces to Problem 2 with input functions fS1,..., fSk.

See Algorithm 1 for the entire reduction assuming inputs are data points of pairs (r, c), where r is the value and c is the category of the feature. Note for simplicity of presentation, we only compute the value instead of the actual split, but it is easy to extend it to return the entire solution.

Therefore, we shift gears and try to solve Problem 2 in the remainder of the paper.

## Algorithm

for Unimodal Cost 2-Median

UC2M is related to various classical 2-median problems in 1D, where there is a cost that is a function of the distance to the center (Hassin and Tamir 1991; Chen and Wang 2011). Those problems can be seen as a symmetric unimodal cost 2-median problem. A function f: R →R is symmetric, if there exists some c ∈R, such that f(c−x) = f(c+x) for all x ∈R. Previous techniques do not help with our problem, as our functions are not always symmetric. Hence, we have to design the algorithm from the ground up. Note our algorithm would be a special case of the algorithm for unimodal cost facility location on a line problem (Zheng 2026), which we describe the design of the special case here.

For a piecewise-linear function f of n breakpoints, the representation consists of the sorted list of breakpoints x1,..., xn, and the corresponding values f(x1),..., f(xn). Additionally, the initial slope and the final slope are also stored. Given i, one can find xi, and evaluate f, the right slope of f, and the change of slope of f at xi, all in O(1) time. If we are interested in finding the value of f(x) by giving x instead of any index, it takes O(log n) time by doing a binary search over the list and then interpolating adjacent breakpoints.

Properties of the Problem Let f1,..., fk be the input of Problem 2, and g(x, y) = Pk i=1 min{fi(x), fi(y)}. Evaluate g for all x, y takes O(k) time each if we look at x, y in order. Hence, Problem 2 has an O(n2k) time algorithm.

This algorithm is extremely naive, looking through all possible input pairs. One might guess that if we fix a, then the function ga(b) = g(a, b) is a unimodal function, and then a binary search-like procedure can be applied to find the minimum b for ga. Unfortunately, this is false; ga can have many local minima. Fortunately, g is a totally monotone function.

Theorem 3. Let f: R →R be an unimodal function. The function g: R2 →R defined as g(x, y) = min(f(x), f(y)) if x ≤y, and g(x, y) = ∞if x > y, is a totally monotone function.

Proof. Consider for any x1 ≤x2 and y1 ≤y2.

In order to show h is totally monotone, we have to show that if min(f(x1), f(y1)) ≤min(f(x1), f(y2)), then min(f(x2), f(y1)) ≤min(f(x2), f(y2)).

If we do not have x1 ≤x2 ≤y1 ≤y2, we will obtain an infinity case, and one can see the inequalities hold.

Hence we assume x1 ≤x2 ≤y1 ≤y2. There are two cases. Case 1. If f(y1) ≤f(y2), then min{f(x2), f(y1)} ≤ min{f(x2), f(y2)}.

Case 2. Otherwise, assume f(y1) > f(y2). Because f(y1) > f(y2) but y1 ≤y2, so we must have y1 is in the decreasing part of the function f. Therefore, we must have f(x1) ≥f(x2) ≥f(y1) > f(y2). Hence, f(y1) = min{f(x1), f(y1)} ≤min{f(x1), f(y2)} = f(y2) < f(y1), a contradiction.

By Theorem 3, and the fact that the sum of totally monotone functions is totally monotone (Park 1999), the function we try to optimize in Problem 2 is a totally monotone function. Let x1,..., xn be all the breakpoints of all the functions ordered from smallest to largest. Consider the matrix M, such that Mi,j = g(xi, xj), where xi is the ith breakpoint of g, then M is a totally monotone matrix. It is useful for us to consider the index-based version of the breakpoint instead of the breakpoint itself for ease of implementation.

For a totally monotone matrix M, the SMAWK algorithm finds the row minima of each row of M in O(n) evaluations of entries in M (Aggarwal et al. 1987). Each evaluation takes O(k log k) time. Therefore, we obtain an O(nk log k) time algorithm. The SMAWK algorithm is known to use a minimum number of evaluations (up to a constant), so it seems there is no way to beat the current running time by much, as it is unlikely to do a single evaluation in less than O(k) time in the worst case.

However, observe that evaluations are not all independent. After evaluating Mi,j, evaluating Mi+1,j or Mi,j+1 would become easier, as the difference is only a single breakpoint, so the change in the function g is easy to describe. Hence, if one can arrange the order of evaluation and compute the ”difference” with a better data structure, a fast algorithm can be designed. In the next section, we show this is possible by

27964

<!-- Page 5 -->

massively speeding up the average time of each evaluation at the cost of slightly increasing the number of evaluations.

Slowing Down to Speed Up

Recall that we are interested in finding the x and y such that g(x, y) is minimized, where x, y are from a lattice grid and g(x, y) evaluated on the grid results in a totally monotone matrix. We can make the evaluation dependent on predecessors through an alternative divide-and-conquer algorithm other than the SMAWK. This new divide-and-conquer algorithm will take a total of O(n log n) evaluations of the matrix, so a slow down in the number of evaluations. However, a total speed up is obtained by speeding up each individual evaluation.

We outline the idea as follows: for a fixed i, let j be the value that minimizes Mi,j. The optimum of the entire matrix must be either Mi,j, or of the form Mi′,j′ where i′ < i and j′ ≤j, or i′ > i and j′ ≥j (Park 1999). Hence, this gives us a natural divide-and-conquer algorithm: find the row minimum of the center row and recursively solve the new problem on the two smaller matrices. Observe the total number of evaluations of a n × m matrix would be T(n, m) = T(n/2, m1) + T(n/2, m2) + O(m) = O(m log n). Since, in our case, n = m, we get an algorithm taking O(n log n) evaluations.

Naively, this would give us an O(nk log n log k) time algorithm, which is even worse than the SMAWK algorithm. However, instead of the number of evaluations, we can show that the running time follows a similar recursion, and thus we obtain an O(n log n + k log k log n) time algorithm.

Naturally, we have to describe how to solve the two parts of the problem: Finding the row minimum and divide-andconquer.

Find the Minimum over a Single Row

Finding a minimum of a given row in the matrix M, is equivalent to answer the following question: Given functions f1,..., fk, and an fixed index a, how to find minb

Pk j=1 min(fj(xa), fj(xb)) quickly? For a fixed a, define the active set at index b to be the set of function indices j, such that fj(xa) > fj(xb). Let A1,..., An be the sequence of active sets at 1,..., n, respectively. Each function fj moves out of the active set only once. That is, for an index j ∈[k], there exists an index qj, such that for each i ≥qj, we have j ∈Ai, and j̸ ∈Ai otherwise.

Define fA = P i∈A fi. If we can quickly evaluate fA and update A, then we can quickly evaluate g. Indeed, in order to evaluate g(xa, xb), the idea is to break it down into evaluating f ¯ A(xa) + fA(xb) where A is the active set at index b.

It’s not hard to describe a data structure that maintains the value of fA(xa) under updates of A and a; this is precisely the evaluation data structure in Theorem 6. However, we must also decide which function has to be added or removed from A. This is done through a useful transformation. Let f be an unimodal function with the local minimum at c, define f †: R →R to be f †(x) = max{x′ | f(x′) ≤f(x)}

if x ∈(−∞, c] and −∞otherwise. Intuitively, this means for any x ≤c, if we have x ≤x′ ≤f †(x), then we know f(x′) ≤f(x). Namely, one can quickly observe if f(x) ≤f(x′) by checking if x′ ≤f †(x). See Figure 2.

If f is a piecewise-linear unimodal function of n breakpoints, then f † is a piecewise-linear decreasing function in (−∞, c] of n breakpoints and can be computed from f in O(n) time. We can find the value of f †(x) in O(log n) time. Since f † can be computed in linear time when f is created, we always assume that f † is computed when we use f.

Knowing f † i (xa) for each i, then we know precisely when i moves out of the active set: i moves out of the active set when xb > f † i (xa) for the first time. See Algorithm 2 for implementation of ROWMINIMA.

Theorem 4. If the input is k functions with a total of n breakpoints, row minima can be found in O(n + k log k) time.

Proof. We analyze the running time of ROWMINIMA. Ordering the functions by evaluation of f † j (xa) for each j, which takes Pk j=1 nj log nj = O(k log n k) time, where nj is the number of breakpoints of fj. Sorting the k functions by their † value takes O(k log k) time. The linear scan takes O(n) time. Hence, going through each breakpoint takes O(n) time. Note k = O(n), hence O(k log n k) = O(n). The total running time of RowMinima is O(n + k log k).

c x f f †(x) f †(x)

f(x) f(x)

x0 x0 f(x0) f(x0)

**Figure 2.** Intuition of the † transform.

Divide-and-Conquer In the divide-and-conquer step, we split the problem into evaluations over 2 smaller submatrices, which are almost disjoint.

Observe that once we are searching for the optimum in a submatrix where the row index ranges from amin to amax and the column index ranges from bmin to bmax. All the values of the functions outside this range are irrelevant. Hence, we can safely assume we process all the functions passed into the recursive call by removing the breakpoints outside the ranges. In practice, this is not explicit but is done through implicit bookkeeping. This allows us to bound the running time related to traversing the functions by O((bmax −bmin) + (amax −amin)) inside each recursive call. See the recursive algorithm OPTIMUM in Algorithm 2.

27965

<!-- Page 6 -->

Dataset Feature Data size Categories LightGBM relative Accuracy LightGBM Time (s) Our Time (s) Predict Droughts TS 19,300,680 7,588 0.9957 5.40698 0.948483 WS10M 19,300,680 1,740 0.9991 5.64445 0.737965 QV2M 19,300,680 2,210 0.9734 5.13713 0.843196 T2M RANGE 19,300,680 3,029 0.9729 5.40553 0.847019 delays zurich transport windspeed avg 5,465,575 66 0.9996 1.25839 0.283073 temp 5,465,575 143 0.9984 1.26260 0.289960 stop id 5,465,575 1,530 0.9766 1.29020 0.370960 time 5,465,575 3,526 0.9870 1.23520 0.402581 gpu kernel performance MWG 5,100,000 5 0.9234 2.25632 0.598805 MDIMC 5,100,000 7 0.9903 2.33057 0.271983 NWG 5,100,000 0.9583 2.36985 0.465714 diamonds carat 53,940 273 0.6193 0.021328 0.016229 table 53,940 127 0.9829 0.022840 0.008226 x 53,940 554 0.6213 0.028240 0.019635 house sales sqft living 21,613 1,038 0.8553 0.026370 0.009103 zipcode 21,613 70 0.8322 0.016795 0.005777 sqft above 21,613 946 0.8932 0.036526 0.008170 wine fixed acidity 1,143 91 0.8662 0.012946 0.000178 density 1,143 388 0.7094 0.010698 0.000281 volatile acidity 1,143 135 0.8067 0.005512 0.000193 citric acid 1,143 77 0.8611 0.004860 0.000177 boston ZN 506 26 0.8926 0.005560 0.000262 INDUS 506 76 0.7886 0.005856 0.000444 DIS 506 412 0.7320 0.018420 0.000626

**Table 2.** Comparison between LightGBM and our algorithm.

The main observation is that the sequence of functions is also split into two subproblems. Let Ma,b be the optimum value on the row a. We consider the functions in two classes, L = {i|fi(xa) ≤ fi(xb)}, and R = {i|fi(xa) > fi(xb)}. The algorithm would be correct if we pass down all functions. However, when we pass the function to the left recursion, during the evaluating values Ma′,b′ where a′ ∈ [amin, a] and b′ ∈ [bmin, b], the contribution of the function fi where i ∈ R is apparent: min(fi(xa′), fi(xb′)) = fi(xb′). Namely, P i∈R min(fi(xa′), fi(xb′)) = P i∈R fi(xb′). A similar result holds for right recursion. Therefore, there is no need to pass down all the functions; instead, we sum the functions and pass them down. This ensures the sequence of functions passed down is partitioned into two, each with one more function appended.

Theorem 5. Finding the optimum of Problem 2 for the input of k function of a total n breakpoints takes O((n + k log k) log n) time.

Proof. See appendix.

Some additional optimization can be done that does not change the asymptotic worst-case running time but improves the running time in practice. For example, in the recursion, if at some point, the only function remaining is the function that came from a sum of original functions, then the recursion can stop earlier.

Data Structure for Piecewise-Linear Functions We describe a data structure over a set of piecewise-linear functions, and it can return the sum quickly. This data structure is required to implement ROWMINIMA, where two dynamic sums of piecewise-linear functions need to be main- amin amin amax amax

< l a t e x i t s h a

1

_ b a s e

4

=

"

7

S

0

Y z z

E

Z o

V

9

E k

Y

Q

O k k

W

+ y b

R

G

A

Q

=

"

>

A

A

A

B

7 n i c b

Z

D

J

S g

N

B

E

I

Z r j

E u

M

W

1

Q

8 e

R k

M g q c w

I

7 g c

A

1

4

8

R j

A

L

J

E

P o d

Q k

T b p

7 h u

4 e

I

Q x

5

C

C

8 e

F

P

H q a

/ g

K

H g

R

P

P o p

2 l o

M m

/ t

D w

8 f

9

V d

F

W

F

C

W f a e

N n s

5

R b

X l l d y

8

X

N j a

3 t n e

K u

3 t

1

H a e

K

Y o

3

G

P

F b

N k

G j k

T

G

L

N

M

M

O x m

S g k

I u

T

Y

C

A d

X

4

7 x x h

0 q z

W

N a

Y

Y

K

B

I

D

3

J

I k a

J s

V

Y j

7

G

S

C y

V

G n

W

P

L

K

3 k

T u

I v g z

K

F

V y

H

9

9 v

B

1

9

Y

7

R

T f

2

9

2

Y p g

K l o

Z x o

3 f

K

9 x

A

Q

Z

U

Y

Z

R j q

N

C

O

9

W

Y

E

D o g

P

W x

Z l

E

S g

D r

L

J u

C

P

3

2

D p d

N

4 q

V f d

K

4

E

/ d

3

R

0 a

E

1 k

M

R

2 k p

B

T

F

/

P

Z

2

P z v y

V m u g y y

J h

M

U o

O

S

T j

+

K

U u a

2

B

3 v

7 n a

Z

Q m r

4

0

A

K h i t l

Z

X d o n i l

B j

L

1

S w

R

/

D n

V

1

E

+ m n

Z

P y

+ f

3 f i l i g d

T

5 e

E

Q j u

A

E f

L i

A

C l x

D

F

W p

A

Y

Q

D

3

8

A h

P

T u

I

8

O

M

/

O y

7

R

0 y

Z n

1

7

M

M f

O a

8

/

P

0 q

T

5

A

=

=

<

/ l a t e x i t

> bmin

< l a t e x i t s h a

1

_ b a s e

4

=

"

7

S

0

Y z z

E

Z o

V

9

E k

Y

Q

O k k

W

+ y b

R

G

A

Q

=

"

>

A

A

A

B

7 n i c b

Z

D

J

S g

N

B

E

I

Z r j

E u

M

W

1

Q

8 e

R k

M g q c w

I

7 g c

A

1

4

8

R j

A

L

J

E

P o d

Q k

T b p

7 h u

4 e

I

Q x

5

C

C

8 e

F

P

H q a

/ g

K

H g

R

P

P o p

2 l o

M m

/ t

D w

8 f

9

V d

F

W

F

C

W f a e

N n s

5

R b

X l l d y

8

X

N j a

3 t n e

K u

3 t

1

H a e

K

Y o

3

G

P

F b

N k

G j k

T

G

L

N

M

M

O x m

S g k

I u

T

Y

C

A d

X

4

7 x x h

0 q z

W

N a

Y

Y

K

B

I

D

3

J

I k a

J s

V

Y j

7

G

S

C y

V

G n

W

P

L

K

3 k

T u

I v g z

K

F

V y

H

9

9 v

B

1

9

Y

7

R

T f

2

9

2

Y p g

K l o

Z x o

3 f

K

9 x

A

Q

Z

U

Y

Z

R j q

N

C

O

9

W

Y

E

D o g

P

W x

Z l

E

S g

D r

L

J u

C

P

3

2

D p d

N

4 q

V f d

K

4

E

/ d

3

R

0 a

E

1 k

M

R

2 k p

B

T

F

/

P

Z

2

P z v y

V m u g y y

J h

M

U o

O

S

T j

+

K

U u a

2

B

3 v

7 n a

Z

Q m r

4

0

A

K h i t l

Z

X d o n i l

B j

L

1

S w

R

/

D n

V

1

E

+ m n

Z

P y

+ f

3 f i l i g d

T

5 e

E

Q j u

A

E f

L i

A

C l x

D

F

W p

A

Y

Q

D

3

8

A h

P

T u

I

8

O

M

/

O y

7

R

0 y

Z n

1

7

M

M f

O a

8

/

P

0 q

T

5

A

=

=

<

/ l a t e x i t

> bmin bmax bmax a b

Row Minima Computation Row Minima Computation

Left recursion Left recursion Right recursion Right recursion

**Figure 3.** A demonstration of one step of the recursion algorithm.

tained, and also OPTIMUM, where the sum of piecewiselinear functions has to be computed and passed down.

Let f1,..., fk be piecewise-linear functions with a total of n distinct breakpoints. Although our algorithms can handle the case when breakpoints are not distinct, describing them does not provide additional insights.

Let fA = P i∈A fi. Let a global set of points x1,..., xn contain all the breakpoints of each fi. We aim to maintain a data structure that includes a set A and an index a, enabling the fast evaluation of fA(xa).

Formally, the data structure should have the following op-

27966

![Figure extracted from page 6](2026-AAAI-binary-split-categorical-feature-with-mean-absolute-error-criteria-in-cart/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

## Algorithm

2: Finding Unimodal 2 Medians Function UNIMODAL2MEDIAN:

Input: f compute global list of breakpoints x1,..., xn compute the † transform for each function return OPTIMUM(1, n, 1, n, f)

Function OPTIMUM:

Input: amin, amax, bmin, bmax, f a ←(amin + amax)/2 (v, b) ←ROWMINIMA(a, bmin, bmax, f) if amin = amax then return v end L ←{ i | fi(xa) ≤fi(xb) } R ←{ i | fi(xa) > fi(xb) } f L ←{fi | i ∈L} ∪

P i∈R fi f R ←{fi | i ∈R} ∪

P i∈L fi vL ←OPTIMUM(amin, a, bmin, b, f L) vR ←OPTIMUM(a, amax, b, bmax, f R) return min(vL, vR, v)

Function ROWMINIMA:

Input: a, bmin, bmax, f renumber f1,..., fk so that f † j (xa) ≤f † j+1(xa) p ←1 A ←{1,..., k} for i = bmin to bmax do while f † p(xa) < xi do A ←A \ {p} p ←p + 1 end v ←f ¯ A(xa) + fA(xi) if v is the smallest seen value then b ←i end end return b erations. 1. INITIALIZE(f1,..., fk): Process the functions f1,..., fk, and return a data structure for f∅and a = −1. 2. ADD(i): Update A into A ∪{i}. 3. REMOVE(i): Update A into A \ {i}. 4. EVALUATE(): Return fA(xa). 5. NEXT(): Update a to a + 1. Such a data structure is standard, but we sketch it here for completeness. Theorem 6. Assuming all the breakpoints have been sorted, the data structure takes O(n) time to construct, and any sequence of O(n) queries takes O(n) time.

Proof. See appendix.

Theorem 7. Problem 2 can be solved in O((n + k log k) log n) time. Theorem 8. The median split problem on k categories and n data points can be solved in O((n + k log k) log n) time.

**Figure 4.** Running time in seconds vs. number of data points.

In particular, if the number of categories is small with respect to the number of datapoints, then our running time is simply O(n log n).

## Experiments

We implemented the algorithm in C++ and ran it on an 8core AMD Ryzen 7 5800H processor with 16GB of RAM.1 We selected several regression datasets from OpenML: two large datasets (more than 500k data points) (OpenML 2017, 2023), two medium-sized datasets (around 50k data points) (OpenML 2019, 2020), and two small datasets (about 1000 data points) (Kaggle 2022; OpenML 2014). For each dataset, we attempted a binary split on each of its features. We used LightGBM, as it can handle large-scale data inputs, whereas scikit-learn often fails to complete in a reasonable amount of time.

We recorded the running time and MAE values of our algorithm and LightGBM, and calculated the relative accuracy (our result / LightGBM result) for each dataset, as shown in the table above (OpenML dataset IDs in parentheses).

To further evaluate performance under imbalanced data, we selected two datasets from Kaggle: Predict Droughts(Minixhofer 2021) and Wine. Their results are also included in the table.

Our algorithm achieves exact MAE-optimal splits in all cases. Interestingly, LightGBM is sufficiently accurate in most instances. However, since our algorithm is consistently faster, there is no need to use subsampled data to reduce computation. For the imbalanced datasets, our method maintains higher accuracy than LightGBM and also demonstrates superior time efficiency. Furthermore, since our evaluation focuses only on single-level binary splits, we have reason to believe that, in multi-level decision trees, the cumulative error from heuristic methods like LightGBM may grow significantly as the depth increases.

1Code is available at https://anonymous.4open.science/r/ binary-split-F12B.

27967

![Figure extracted from page 7](2026-AAAI-binary-split-categorical-feature-with-mean-absolute-error-criteria-in-cart/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

We also examined running time asymptotics by creating subsets of the gpu performance dataset with feature MDIMC via sampling without replacement from 0.01 to 1.0 in 0.01 increments. We ran both our algorithm and Light- GBM on each subset and compared the runtime. The result in Figure 4 confirms that our method scales nearly linearly with input size.

## References

Aggarwal, A.; Klawe, M. M.; Moran, S.; Shor, P.; and Wilber, R. 1987. Geometric applications of a matrixsearching algorithm. Algorithmica, 2(1): 195–208. Breiman, L.; Friedman, J.; Stone, C.; and Olshen, R. 1984. Classification and Regression Trees. Catlett, J. 1991. Mega induction: a Test Flight. In Birnbaum, L. A.; and Collins, G. C., eds., Machine Learning Proceedings 1991, 596–599. San Francisco (CA): Morgan Kaufmann. ISBN 978-1-55860-200-7. Chen, D. Z.; and Wang, H. 2011. New Algorithms for 1- D Facility Location and Path Equipartition Problems. In Dehne, F.; Iacono, J.; and Sack, J.-R., eds., Algorithms and Data Structures, 207–218. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-642-22300-6. Chen, T.; and Guestrin, C. 2016. Xgboost: A scalable tree boosting system. In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining, 785–794. ACM. Hassin, R.; and Tamir, A. 1991. Improved complexity bounds for location problems on the real line. Operations Research Letters, 10(7): 395–402. Hastie, T.; Tibshirani, R.; and Friedman, J. 2001. The Elements of Statistical Learning. Springer Series in Statistics. New York, NY, USA: Springer New York Inc. jiangfeng. 2017. Trees with MAE criterion are slow to train. https://github.com/scikit-learn/scikit-learn/issues/9626. Accessed: 2024-12-30. Kaggle. 2022. Wine Quality Dataset. https://www. kaggle.com/datasets/yasserh/wine-quality-dataset. Accessed: 2025-07-26. Ke, G.; Meng, Q.; Finley, T.; Wang, T.; Chen, W.; Ma, W.; Ye, Q.; and Liu, T.-Y. 2017. LightGBM: A Highly Efficient Gradient Boosting Decision Tree. Advances in Neural Information Processing Systems 30, 3146–3154. McGinnis, W.; hbghhy; Tao, W.; andrethrill; Siu, C.; Davison, C.; and Bollweg, N. 2018. scikit-learncontrib/categorical-encoding: Release for zenodo. Minixhofer, C. 2021. Predict Droughts using Weather & Soil Data. https://www.kaggle.com/datasets/cdminix/usdrought-meteorological-data. Accessed: 2025-07-26. OpenML. 2014. boston dataset (v.1). https://www.openml. org/d/531. Accessed: 2025-1-7. OpenML. 2017. delays zurich transport dataset (v.1). https: //www.openml.org/d/40753. Accessed: 2025-1-9. OpenML. 2019. diamonds dataset (v.1). https://www. openml.org/d/42225. Accessed: 2025-1-8.

OpenML. 2020. house sales dataset (v.3). https://www. openml.org/d/42731. Accessed: 2025-1-9. OpenML. 2023. simulated sgemm gpu kernel performance dataset (v.2). https://www.openml.org/d/45662. Accessed: 2025-1-9. Park, J. K. 1999. The Monge Array: An Abstraction and Its Applications. Ph.D. thesis, Massachusetts Institute of Technology. Prokhorenkova, L.; Gusev, G.; Vorobev, A.; Dorogush, A. V.; and Gulin, A. 2018. CatBoost: unbiased boosting with categorical features. In Advances in Neural Information Processing Systems, 6638–6648. Torgo, L. F. R. A. 1999. Inductive learning of tree-based regression models. Ph.D. thesis, Universidade do Porto. Reitoria. Zheng, D. W. 2026. Unimodal Cost Facility Location on a Line. Unpublished manuscript.

27968
