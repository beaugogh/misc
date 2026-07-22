---
title: "Reconfiguring Proportional Committees"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38727
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38727/42689
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Reconfiguring Proportional Committees

<!-- Page 1 -->

Reconfiguring Proportional Committees

Chris Dong1, Fabian Frank2, Jannik Peters3, Warut Suksompong3

1Hasso Plattner Institute, University of Potsdam 2Technical University of Munich 3National University of Singapore

## Abstract

An important desideratum in approval-based multiwinner voting is proportionality. We study the problem of reconfiguring proportional committees: given two proportional committees, is there a transition path that consists only of proportional committees, where each transition involves replacing one candidate with another candidate? We show that the set of committees satisfying the proportionality axiom of justified representation (JR) is not always connected, and it is PSPACE-complete to decide whether two such committees are connected. On the other hand, we prove that any two JR committees can be connected by committees satisfying a 2approximation of JR. We also obtain similar results for the stronger axiom of extended justified representation (EJR). In addition, we demonstrate that the committees produced by several well-known voting rules are connected or at least not isolated, and investigate the reconfiguration problem in restricted preference domains.

## Introduction

Multiwinner voting is one of the core topics in computational social choice and collective decision-making (Faliszewski et al. 2017). A set of voters submits preferences over a set of candidates, from which a fixed number of candidates need to be selected. Applications of this simple decision-making model range from deliberation platforms (Revel et al. 2025) to civic participation systems (Fish et al. 2024; Boehmer, Fish, and Procaccia 2025) to participatory budgeting (Peters, Pierczy´nski, and Skowron 2021), blockchain governance (Cevallos and Stewart 2021; Boehmer et al. 2024), and clustering (Kellerhals and Peters 2024). In particular, a substantial body of work has focused on approval-based multiwinner voting, where voters submit ballots containing the set of candidates that they approve (Lackner and Skowron 2023). For example, consider the deliberation platform setting of Revel et al. (2025). In their setting, users of a deliberation platform can write comments on a specific topic and “like” comments by other users of the platform. An important goal of such a platform is to summarize the discussion by selecting a fixed-size representative subset of the comments. This is precisely an approval-based multiwinner voting problem, with the voters corresponding

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

to the users of the platform, the candidates to the comments of the users, and the approval ballots to the sets of comments liked by different users. In all of the works mentioned thus far, a common aim is to achieve outcomes that proportionally represent the voters (Aziz et al. 2017; Peters and Skowron 2020; Brill and Peters 2023).

Traditionally, multiwinner voting is a static setting: based on the ballots submitted by voters, a single committee is selected. However, this is insufficient for modeling several applications, especially when a temporal aspect is present.1 Consider, for instance, the scenario of blockchain governance. Here, several blockchain systems use a “Nominated Proof-of-Stake” protocol in which a subset (i.e., “committee”) of the stakeholders is selected to take part in the blockchain Proof-of-Stake consensus mechanism. In such governance protocols, it is crucial to prevent the formation of an oligarchy, i.e., no small subset of the blockchain stakeholders should be able to control the consensus mechanism on their own (Tennakoon and Gramoli 2023). Tennakoon and Gramoli proposed two mechanisms to prevent an oligarchy from forming: (i) they suggested using proportional representation2 to ensure that every sufficiently large subset of stakeholders is represented in the committee, and (ii) they recommended periodically and frequently reconfiguring the blockchain committee in order to hinder oligarchies in the committee itself. However, this reconfiguration cannot simply replace the entire committee in a single step, as it would lead to a large computation and communication overhead on the blockchain (see, e.g., the discussion in the seminal work of Zamani, Movahedi, and Raykova (2018)). Instead, the committee should be gradually reconfigured over time. Blockchain systems are far from the only application of multiwinner voting where temporal aspects are relevant. Motivated by tasks in recommender systems and streaming services, Chen, Hatschka, and Simola (2024) recently introduced the problem of reconfiguration to approval-based multiwinner voting: given an initial committee and a target committee, can we reach the target committee from the initial committee by replacing one candidate at a time? For example, as described by Chen, Hatschka,

1We survey related prior work in Section 1.2. 2A prominent blockchain using methods from approval-based multiwinner voting is Polkadot (Cevallos and Stewart 2021; Boehmer et al. 2024).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16829

<!-- Page 2 -->

and Simola, these committees could represent catalogs of products displayed by streaming service providers or online stores, where changing these catalogs too abruptly might result in a suboptimal customer experience.

If no restrictions are placed on the intermediate committees, the answer to this question is obviously positive, as one can simply replace an excess candidate with a missing candidate in each step. The question becomes interesting, however, when the intermediate committees are required to maintain a quality comparable to that of the two given committees. Chen, Hatschka, and Simola (2024) measured “quality” using scoring rules, which assign a score to each committee based on the number of approvals of the voters. While committees that optimize certain scores are known to offer desirable properties—for instance, those maximizing the Proportional Approval Voting (PAV) score satisfy a proportionality axiom called extended justified representation (EJR)—those that maximize other scores such as the Approval Voting (AV) or Satisfaction Approval Voting (SAV) scores do not offer proportionality guarantees (Aziz et al. 2017). Moreover, committees with approximately optimal PAV scores need not satisfy approximate proportionality notions,3 which means that the intermediate committees selected by Chen, Hatschka, and Simola do not necessarily retain the proportionality guarantees of the initial and target committees. Considering the well-established importance of proportional representation in (approval-based) multiwinner voting, this inspires us to study the following problem:

Given two committees W and W ′ satisfying a proportionality axiom, does there exist a transition from W to W ′ such that each step in the transition involves replacing a candidate by another candidate, and every intermediate committee also (approximately) satisfies this proportionality axiom?

Such problems are typical in the field of reconfiguration (Nishimura 2018),1 and we will examine them for different proportionality notions in approval-based multiwinner voting. Aside from their intrinsic interest, investigating these problems will also yield insights into the structure of proportional committees, for example, whether the space of such committees is always connected or whether a proportional committee can be isolated in this space.

## 1.1 Our Results In

Section 3, we begin by examining the set of committees satisfying the axiom of justified representation (JR). We provide an example of JR committees that are not connected by any transition path containing only JR committees. In fact, these disconnected JR committees can be heavily isolated: it is possible that for a JR committee, no other JR committee is within distance k −2 of it (and this bound is tight), where k denotes the size of the committees. We

3As a simple example, suppose that the voters are split into two halves, where each half unanimously approves k candidates but the two candidate sets are disjoint. Selecting a committee with all k candidates from the same half yields a 2-approximation of PAV. However, for any α ≥1, it is possible to choose k and the number of voters so that the committee violates α-EJR.

also prove that deciding whether two JR committees are connected is PSPACE-complete. On the other hand, by relaxing the proportionality requirement for the intermediate committees, we show that any two JR committees can be connected via a path containing only “2-approximate” JR committees, and the factor of 2 cannot be improved. Furthermore, we examine the stronger axiom of extended justified representation (EJR). While the existence of isolated JR committees and the PSPACE-completeness transfer to EJR, any two EJR committees are connected via a path containing only 4-approximate EJR committees.

Next, in Section 4, we turn to proportional voting rules and present a general positive result: we show that the committees selected by several popular rules—including PAV, the Method of Equal Shares, and sequential-Phragmén—are all reachable from one another via committees satisfying JR. To prove this result, we show that each committee selected by these rules is connected to some committee containing an “affordable” JR subcommittee, and that all such affordable subcommittees are connected among themselves. This result stands in stark contrast to our earlier finding that there exist committees which are heavily isolated despite satisfying JR.

Finally, in Section 5, we study restricted preference domains and show that for the well-studied voter interval (VI) and candidate interval (CI) domains, the set of JR committees is always connected, that is, any JR committee can reach any other JR committee through a path containing only JR committees. In fact, on the CI domain we can always transition between two JR committees without involving auxiliary candidates that do not belong to the initial or target committee. By contrast, on the VI domain, this is true only if the committees contain no “Pareto-dominated” candidates.

## 1.2 Related Work Besides the work of Chen, Hatschka, and

Simola (2024) that we discussed earlier, our work is related to recent papers considering dynamic and online aspects of multiwinner voting. Dong and Peters (2025) studied a model in which the candidate set changes dynamically over time, and each chosen committee should satisfy proportionality without differing too much from the previous committee. A major difference between our work and theirs is that the set of candidates is static in our model, and the initial and target committees are given. Do et al. (2022) investigated an online setting where candidates arrive over time and each candidate must be irrevocably chosen or rejected. Several authors examined models that involve selecting a series of committees (Bredereck, Kaczmarczyk, and Niedermeier 2020; Bredereck, Fluschnik, and Kaczmarczyk 2022; Deltl, Fluschnik, and Bredereck 2023; Zech et al. 2024), with some allowing for changes in voter preferences over time; however, these authors did not assume predetermined initial or target committees and also did not consider proportionality. For a broader overview of research on temporal multiwinner voting, we refer to the survey by Elkind, Obraztsova, and Teh (2024). At a higher level, our work forms a part of the well-established literature on approval-based multiwinner voting. Other recent works include that of Revel et al. (2025), which applied the axiom of justified representation

16830

<!-- Page 3 -->

to the context of deliberation platforms, Boehmer, Fish, and Procaccia (2025), which studied proportionality in the context of “generative social choice”, and Kellerhals and Peters (2024), which established connections between justified representation axioms and proportional clustering.

Reconfiguration has long been studied for various algorithmic problems such as minimum spanning tree (Ito et al. 2011) and graph coloring (Johnson et al. 2016), and recently gained increasing attention in social choice theory. Igarashi et al. (2024) and Chandramouleeswaran, Nimbhorkar, and Rathi (2025) explored it in the context of fair division, whereas Ito et al. (2023) addressed a similar problem on item assignment. Obraztsova et al. (2013) and Obraztsova, Elkind, and Faliszewski (2020) considered the connectivity and convexity of ranked elections that select the same winner under certain voting rules, where two elections are considered adjacent if they can be obtained from each other by swapping adjacent candidates in the ranking of a single voter. Reconfiguration is also related to the framework of “one profile, successive solutions” proposed by Boehmer and Niedermeier (2021) for computational social choice.

## 2 Preliminaries and Notation

In this section, we recap the standard setting of approvalbased multiwinner voting and introduce terminology for the connectedness of (sets of) committees. For any positive integer t, let [t] = {1, 2,..., t}.

Approval-Based Multiwinner Voting We assume that we are given a set of n voters N = {v1,..., vn} and a set of m candidates C = {c1,..., cm}. An approval profile A = (Av)v∈N is a collection of approval ballots Av ⊆C, where each voter v ∈N submits the set of candidates that she approves. When a voter vi is given with index, we write Ai instead of Avi for convenience. Further, Nc:= {v ∈N | c ∈Av} denotes the support of a candidate c ∈C, and NW:= {v ∈N | W ∩Av̸ = ∅} denotes the support of a subset of candidates W ⊆C. Given a target committee size k ≤m, we call a subset of candidates W ⊆C a committee if |W| = k and a subcommittee if |W| ≤k. An instance consists of an approval profile A and a committee size k. A voting rule f takes as input an instance (A, k) and outputs a non-empty set of committees f(A, k).

In this paper, we study rules and committees that proportionally represent the electorate. To define proportionality, we follow the justified representation approach initiated by Aziz et al. (2017). For ℓ≥0, we say that a group N ′ ⊆N of voters is ℓ-large if |N ′| ≥ℓ· n k. We say that N ′ is ℓ-cohesive if N ′ is ℓ-large and |T v∈N ′ Av| ≥ℓ, i.e., these voters approve at least ℓcandidates in common.

Proportionality Axioms A (sub)committee W satisfies justified representation (JR) if for every 1-cohesive group of voters N ′, there exists a voter v ∈N ′ with Av ∩W̸ = ∅. In other words, for every group of voters of size at least n k who approve at least one common candidate, at least one of these voters must approve some candidate in the (sub)committee. Similarly, a (sub)committee W satisfies extended justified representation (EJR) if for every ℓ∈N and every ℓcohesive group of voters N ′, there exists a voter v ∈N ′

{c1, c2}

{c1, c3}

{c2, c3}

{c3, c4}

{c2, c4}

{c1, c4}

**Figure 1.** Each node represents a committee of size two. An edge is drawn between two committees if the distance between them is one.

with |Av ∩W| ≥ℓ. We will also study approximate versions of these proportionality axioms. For α ≥1, we say that a (sub)committee satisfies α-JR (resp., α-EJR) if for every α-cohesive group of voters N ′ (resp., (αℓ)-cohesive group), there exists v ∈N ′ such that |Av ∩W| ≥1 (resp., |Av ∩W| ≥ℓfor each ℓ∈N). Observe that for α = 1, this is equivalent to JR and EJR, respectively. Throughout the paper, we let JR(A, k) (resp., EJR(A, k)) denote the set of all committees satisfying JR (resp., EJR) for a given instance. Similarly, we define α-JR(A, k) and α-EJR(A, k) for any α ≥1.

We say that a voting rule f satisfies a given axiom if for every instance (A, k) and every W ∈f(A, k), the committee W satisfies the axiom for this instance.

Distance, Connectedness, and Isolation To measure the distance between two committees W, W ′, we consider the size of their symmetric difference and define d(W, W ′):= |W \ W ′| = |W ′ \ W|.

Two committees W, W ′ are called connected in some set S of committees if there exists a sequence of committees W1,..., Wx ∈S with W1 = W and Wx = W ′ such that d(Wi, Wi+1) = 1 for all i ∈[x −1]. Two subcommittees are called connected in S if all pairs of committees containing them are connected in S. A set of subcommittees S is called connected in a set S if each pair of subcommittees W, W ′ ∈S is connected in S. Often, when S = S, we simply say that S is connected.

In contrast, for r ≥1, a committee W is called r-isolated in S if |S| ≥2, W ∈S, and for all committees W ′̸ = W with d(W, W ′) ≤r it holds that W ′ /∈S. If a committee is 1-isolated, we call it isolated for short. As an example, let C = {c1, c2, c3, c4} and k = 2. Figure 1 illustrates all committees as nodes of a graph, with an edge between two committees if the distance between them is 1. The committee {c1, c2} is (1-)isolated in S = {{c1, c2}, {c3, c4}}, while {{c1, c2}, {c3, c4}, {c1, c4}} is connected. Example 1. Consider the following instance with n = 9 and k = 3 (so n k = 3), and the approval profile

1 × {c1}, 2 × {c1, c2}, 4 × {c3, c4, c5}, 2 × {c3, c4, c6}. Two possible JR committees are {c1, c3, c4} and {c2, c5, c6}. The former committee additionally satisfies

16831

<!-- Page 4 -->

EJR, while the latter committee does not—the violation is caused by the last six voters, who would be underrepresented. The two committees are connected in the set of JR committees, e.g., via the following path:

{c1, c3, c4} →{c2, c3, c4} →{c2, c5, c4} →{c2, c5, c6}.

However, {c1, c3, c4} →{c5, c3, c4} →{c2, c5, c4} → {c2, c5, c6} is not a valid path, as {c5, c3, c4} does not satisfy JR due to the first three voters.

3 (Extended) Justified Representation Our definitions from Section 2 immediately lead us to our first question: is the set JR(A, k) of committees satisfying JR always connected? We provide a strong negative answer to this question. In particular, we show that there exists a JR committee with the property that no other committee of distance at most k −2 from it satisfies JR.

Theorem 3.1. For any k ≥3, there exists an approval profile A and a committee W ∈JR(A, k) that is (k −2)isolated in JR(A, k), that is, W is not the only committee in JR(A, k) and every other committee in JR(A, k) has distance at least k −1 to W.

Proof. Let the number of voters be n = k3. We shall construct a profile and specify a committee W satisfying JR, such that all other committees satisfying JR have a distance of at least k −1 to W and, moreover, W is not the only committee satisfying JR in this instance.

Let N = N1 ∪N2 be the set of voters partitioned into two groups, N1 = {v1,..., vk2} and N2 = {vk2+1,..., vn}. Furthermore, let C = C1 ∪C2 be the set of candidates, which we partition into a weak set (C1) and a strong set (C2). We choose C1 = {c1,..., ck} such that ci is approved by consecutive voters v1+(i−1)k, v2+(i−1)k,..., vk+(i−1)k. Note that this covers all the voters in N1 and that each candidate in C1 is approved by exactly k voters.

Additionally, for every i ∈[k2] and every subset N ′

2 ⊆ N2 with |N ′

2| = k2−1, we create a candidate di,N ′ 2 approved by the single voter vi and every voter in N ′

2. Formally, we set C2 = {di,N ′

2 | i ∈[k2], N ′ 2 ∈ N2 k2−1

}. Hence, every candidate in C2 is approved by exactly k2 = n k voters. We now claim that W = C1 satisfies JR. Let N ′ ⊆N be a 1-cohesive group with all voters in N ′ commonly approving a candidate c ∈C \ W. Note that each candidate in C1 is already in W, so c must be from C2. Since c is only approved by n k voters, the group N ′ has to be exactly the support of c. This means that N ′ contains at least one voter vi ∈N1. However, by construction there exists c′ ∈C1 = W with c′ ∈Ai, so W satisfies JR.

Let W ′̸ = W be another committee satisfying JR. Note that every combination of a subset of N2 of size k2 −1 together with one voter in N1 forms a 1-cohesive group. Since W ′ satisfies JR, at least one of the following two statements holds: (i) every voter in N1 approves at least one candidate from W ′, or (ii) at most k2 −2 voters in N2 approve no candidate from W ′. Since each candidate in C2 covers only one voter in N1, (i) would imply that W ′ = C1 = W, a contradiction. Thus, (ii) must hold. Since there are k3 −k2 voters in N2 and each candidate is approved by at most k2 −1 voters in N2, the number of candidates from C2 needed in W ′ so that at most k2 −2 voters in N2 are not covered is at least k3 −k2 −(k2 −2)

k2 −1 = k(k2 −1) −(2k2 −2) + k k2 −1

= k −2 + k k2 −1 > k −2.

Since this number must be an integer, W ′ contains at least k −1 candidates from C2; in particular, it has distance at least k −1 to W = C1. Finally, one can check that any subset of C2 that covers all voters in N2 indeed satisfies JR, and that such a subset of size k exists.

Since the instance constructed in the previous proof does not contain ℓ-cohesive groups for any ℓ> 1, the statement also applies to EJR. Corollary 3.2. For any k ≥3, there exists an approval profile A and a committee that is (k−2)-isolated in EJR(A, k).

Theorem 3.1 and Corollary 3.2 imply negative results for more relaxed models as well: even if in each step, x candidates are allowed to be swapped for some 1 ≤x < k −1, there still exist isolated committees.

Next, we prove that the bound of k −2 in Theorem 3.1 is tight, that is, any JR committee has another JR committee of distance at most k−1 to it (provided that the former committee is not the unique JR committee). Our proof is similar to the proof of Elkind et al. (2023, Theorem 3.5) on the number of committees satisfying JR. This proof, along with all other omitted proofs, can be found in the full version of our paper (Dong et al. 2025b). Proposition 3.3. Suppose that in an instance (A, k), a committee is r-isolated in JR(A, k). Then, r ≤k −2.

On the complexity front, we show that checking whether two committees satisfying JR are connected within the set of JR committees is PSPACE-complete. To this end, we reduce from the SAT-Reconfiguration problem, which is known to be PSPACE-hard (Gopalan et al. 2009). In fact, in our constructed instance, no candidate is approved by at least 2 · n k voters, so JR and EJR are equivalent. Therefore, we also obtain the same result for EJR. Theorem 3.4. Given an instance (A, k) and two JR committees, deciding whether the two committees are connected in JR(A, k) is PSPACE-complete. The same holds for EJR.

The results so far paint a rather negative picture: proportional committees may not be connected, and determining whether they are connected is computationally intractable. Nevertheless, we can obtain positive results if we only demand that the intermediate committees satisfy approximate instead of exact proportionality notions.

We first show that any two JR committees are connected in the space of 2-JR committees. For this, we will need two lemmas. The first lemma is an application of the pigeonhole principle—it implies that, given any committee W approved by |NW | voters and any s ≤k, we can always remove s candidates so that the resulting subcommittee is still approved by at least |NW | −s · n k voters.

16832

<!-- Page 5 -->

Lemma 3.5. Let W be any committee. There exists an order c1,..., ck of the candidates in W such that |NW \{c1,...,cs}| ≥|NW | −s · n k for all s ∈{0, 1,..., k}.

The second lemma observes that JR ensures better representation for groups of size at least 2 · n k.

Lemma 3.6. For any W ∈JR(A, k) and every 2-large and 1-cohesive group N ′ ⊆N, it holds that |N ′ ∩NW | > n k.

Using these two lemmas, we will show that any committee satisfying JR can reach any other committee satisfying JR via a path of 2-JR committees. The high-level idea of the proof is that, by applying Lemma 3.5, we obtain an order in which we remove candidates from both committees. With each removed candidate, we decrease the number of voters who approve at least one candidate by at most n k on average. On the other hand, Lemma 3.6 guarantees that any 2-large, 1-cohesive group has at least n k represented voters. Thus, intuitively, the added candidates due to 2-JR violations balance out against the candidates removed from the committees. Since the added candidates represent sufficiently many voters, we can connect the two resulting committees.

Theorem 3.7. For any instance (A, k), the set JR(A, k) is connected in 2-JR(A, k). Furthermore, any two JR committees can be connected via a sequence of at most 2k committees satisfying 2-JR.

Proof. We say that a subcommittee W ′ ⊆C is 2-JR greedy if it satisfies 2-JR and there is an enumeration W ′ = {d1,..., dℓ} such that |Ndr \ N{d1,...,dr−1}| ≥2 · n k for all dr ∈W ′. That is, W ′ can be obtained from the empty set by greedily adding new candidates, each covering at least 2 · n k previously uncovered voters. Note that a 2-JR greedy subcommittee can contain at most k

2 candidates. Proof outline: As the first step, we show that two committees each of which contains a 2-JR greedy subcommittee are always connected through a path of at most k committees satisfying 2-JR. In the more involved second step, we prove that every committee satisfying JR is connected via at most k

2 swaps to some superset of a 2-JR greedy subcommittee. Together, this implies that any two JR committees are connected via at most 2k committees satisfying 2-JR. Both steps leverage the fact that 2-JR greedy subcommittees always exist and contain at most k

2 candidates. Step 1: Let W and W ′ be two committees, and Wg ⊆W and W ′ g ⊆W ′ be 2-JR greedy subcommittees contained in them. By definition, |Wg|, |W ′ g| ≤ k 2, and every superset of Wg and W ′ g satisfies 2-JR. Hence, starting with W, we can remove candidates from W \ Wg and replace them with candidates from W ′ g (possibly along with candidates from W ′ \ W ′ g) without violating 2-JR. Call the resulting committee W ′′. Since W ′ g ⊆W ′′, we can remove all candidates from Wg and replace them with the remaining candidates from W ′ without violating 2-JR. This concludes the proof of Step 1.

Step 2: Let WJR be any committee satisfying JR. Our goal is to connect WJR to some superset of a 2-JR greedy subcommittee. We first determine a suitable 2-JR greedy subcommittee Wg = {d1,..., dℓ} through the following process. Enumerate the candidates in WJR = {c1,..., ck} according to Lemma 3.5. Initialize W ′ = WJR and r = s = 1. If s ≤k, remove cs from W ′. If a violation of 2-JR occurs as a result of the removal, add a witness candidate to W ′ and label it dr, increment r, and repeat until 2-JR is restored. Increment s and repeat starting from the removal. Once the process ends, set ℓ= r −1 and return W ′.

To analyze this process, for each r ∈[ℓ], denote by W ′ r = (WJR \ {c1,..., cs}) ∪{d1,..., dr−1} the set for which dr creates a 2-JR violation and is added next. We claim that (i) for all W ′ r created during the process, it holds that r ≤s; and (ii) when the process terminates, the final subcommittee W ′ is a 2-JR greedy subcommittee of the form {d1,..., dℓ}.

For (i), consider any set W ′ r = {cs+1,..., ck} ∪ {d1,..., dr−1}, and let W ′ = W ′ r ∪{dr}. To show that r ≤s, we perform a counting argument on |W ′ ∩NWJR|. In particular, we pretend that we obtain W ′ by first removing c1,..., cs from WJR at once and then iteratively adding d1,..., dr. Formally, let Wj = {cs+1,..., ck} ∪ {d1,..., dj−1} for each j ∈[r]. A telescoping sum argument yields

|NW ′ ∩NWJR|

= (|NW ′ ∩NWJR| −|NWr ∩NWJR|)

+ (|NWr ∩NWJR| −|NWr−1 ∩NWJR|)

+ · · · + (|NW2 ∩NWJR| −|N{cs+1,...,ck} ∩NWJR|)

+ |N{cs+1,...,ck} ∩NWJR|, where {cs+1,..., ck} = W1.

We claim that |(Ndj \ NWj) ∩NWJR| > n k for each j ∈ [r]. By the 2-JR violation of W ′ j, the set Ndj contains a 1cohesive subset N ∗of at least 2 · n k voters that are not in NW ′ j. Since Wj ⊆W ′ j, we have NWj ⊆NW ′ j, and therefore N ∗∩NWj = ∅too. By Lemma 3.6, it holds that |N ∗∩ NWJR| > n k, and so |(Ndj \NWj)∩NWJR| > n k, as claimed. Further, note that |N{cs+1,...,ck} ∩NWJR| ≥|NWJR| −s · n k due to Lemma 3.5. Hence, by the telescoping relation above, we obtain that |NW ′ ∩NWJR| > |NWJR| −s · n k + r · n k. As |NW ′ ∩NWJR| ≤|NWJR|, it follows that r < s, concluding the proof of (i).

To establish (ii), note that the final subcommittee is of the form W ′ = (WJR \ {c1,..., ck}) ∪{d1,..., dℓ} = {d1,..., dℓ}. Since each dr was added as a witness for a 2- JR violation of some superset of Wr, we have that the candidate dr satisfies |Ndr \N{d1,...,dr−1}| ≥|Ndr \NWr| ≥2· n k. Hence, the process ends with some 2-JR greedy subcommittee, concluding the proof of (ii).

Finally, we specify the desired sequence by letting W ′′ r = (WJR\{c1,..., cr})∪{d1,..., dr} for each r ∈[ℓ]. By (ii), W ′′ ℓis a committee containing a 2-JR greedy subcommittee. Further, by (i), each committee W ′′ r is a superset of some 2-JR subcommittee created during the process. Hence, W ′′ r satisfies 2-JR. Since d(WJR, W ′′

1) = d(W ′′ 1, W ′′ 2) = · · · = d(W ′′ ℓ−1, W ′′ ℓ) = 1 and ℓ≤ k 2 by (ii), this completes the proof of Step 2, and therefore the entire proof.

Theorems 3.1 and 3.7 show that two committees satisfying JR may not be connected in the set of JR committees,

16833

<!-- Page 6 -->

c1 c2 c3 c4 c5 c′

1 c′

2 c′

3 c′

4 c′

5

**Figure 2.** A visualization of Example 2. Voters are depicted as nodes, and row and column candidates as hyperedges around the nodes. The row committee {c′

i | 1 ≤i ≤5} is shown in yellow.

but are always connected in the set of 2-JR committees. This raises the question of whether the factor 2 is tight. The following proposition answers this question in the affirmative.

Proposition 3.8. For any α < 2, there exists an instance (A, k) such that JR(A, k) is not connected in α-JR(A, k).

Furthermore, we can employ a similar technique as in Theorem 3.7 to show that any two EJR committees are connected via 4-EJR committees. To achieve this, we switch from using the number of “represented” voters as our metric for deleting candidates to a variant of the PAV-score. The proof idea remains the same: we greedily delete the candidates that decrease this variant of the PAV score the least and replace them by candidates witnessing a 4-EJR violation. In the end, this will allow us to reach a common 4-EJR subcommittee from any EJR committee as a starting point.

Theorem 3.9. For any instance (A, k), the set EJR(A, k) is connected in 4-EJR(A, k).

Open Question 3.10. What is the smallest constant α such that for any instance (A, k), the set EJR(A, k) is connected in α-EJR(A, k)?

## 4 Specific Voting Rules

In Theorem 3.1, we showed that proportional committees can be “far away” from other proportional committees. However, the committee in that example appears to be rather suboptimal, and would not be selected by common voting rules such as PAV or the Method of Equal Shares. In this section, we examine how well the choice sets of well-known proportional voting rules—that is, the sets of committees returned by these rules—are connected, either to other proportional committees or within themselves. For a description of the voting rules mentioned here, we refer to the full version of our paper (Dong et al. 2025b). Our first observation is that connectedness within the choice set itself is not a reasonable demand for approval-based multiwinner voting rules, as the choice sets may be too sparse to allow for connections.

Example 2. Consider an instance with r2 voters corresponding to points in an r × r grid. There are 2r candidates, one for each row and one for each column. Each voter approves the two candidates representing her column and row. For the committee size k = r, most well-known proportional voting rules (such as PAV, MES, and sequential- Phragmén) select only the committee consisting of all row candidates and the committee consisting of all column candidates. However, these two committees are not connected in the respective choice sets. See Figure 2 for a visualization.

In light of this observation, we instead study the connectedness of choice sets in JR(A, k) or EJR(A, k).

As our first positive result, we show that a large and wellbehaved set of subcommittees satisfying JR is connected. To specify this set, we recap the following variant of priceability (Peters and Skowron 2020) called affordability, introduced by Brill and Peters (2024). We state a more succinct version of it here. Definition 4.1 (Brill and Peters 2024). A subcommittee W is affordable if there exists a family of payment functions (pi: Ai →[0, 1])vi∈N such that

• P c∈Ai pi(c) ≤k n for each vi ∈N, and • P vi∈Nc pi(c) = 1 for each c ∈W. Furthermore, we define p to be a payment system for an affordable committee W if it is a family of payment functions that uphold the conditions in Definition 4.1.

We can now express our goal more precisely: we want to show that the set of all affordable subcommittees satisfying JR is connected via JR committees. As it turns out, this will have a favorable impact on the connectedness of several voting rules. Before proceeding, we need two auxiliary lemmas. Recall that any subset of an affordable subcommittee is also an affordable subcommittee, and the empty subcommittee is affordable (Brill and Peters 2024). Lemma 4.2 (Brill and Peters 2024, Observation 1). Let Waff be an affordable subcommittee. Then, for all subcommittees X ⊆Waff, it holds that |NX| ≥|X| · n k. Secondly, we show that we can connect any subcommittee W that satisfies JR and is approved by at least n k · (|W| −1) voters to some affordable subcommittee satisfying JR and containing an affordable subcommittee of W. Lemma 4.3. Let W be a subcommittee that satisfies JR such that |NW | ≥n k · (|W| −1), and let W ′ aff be an affordable subcommittee. Further, let X ⊆W ∩W ′ aff. Then, there exists an affordable subcommittee W X aff satisfying JR such that X ⊆W X aff, and W and W X aff are connected in JR(A, k). With these lemmas, we can show that any two affordable subcommittees satisfying JR are reachable from each other. Proposition 4.4. For any instance (A, k), the set of affordable subcommittees satisfying JR is connected in JR(A, k).

Several well-known proportional rules only select supersets of affordable subcommittees satisfying JR. Hence, we immediately obtain from Proposition 4.4 that the choice sets of such rules are always connected via JR committees. Further, the choice sets of different rules are interconnected— for example, we can transition from any MES committee to any seqCCAV committee without violating JR. While PAV and CCAV do not necessarily select supersets of affordable committees satisfying JR, we can nevertheless show that

16834

<!-- Page 7 -->

their choice sets are connected to a superset of an affordable subcommittee satisfying JR. Theorem 4.5. Consider the set of rules

R = {MES, seqCCAV, CCAV, PAV,

GJCR, GreedyEJR, seqPhragmén}.

For any rules f, f ′ ∈R (possibly f = f ′) and any instance (A, k), any committee from f(A, k) is connected to any other committee from f ′(A, k) in JR(A, k).

Hence, while the set of JR committees can be rather disconnected (Theorem 3.1), the committees chosen by many popular rules all lie in the same connected component within the set of committees satisfying JR.

For the stronger axiom of EJR, we show that the outcomes of the three most popular rules satisfying EJR are never isolated within the set of EJR committees. Theorem 4.6. For any instance (A, k), any committee returned by PAV, MES, or GJCR is not isolated in EJR(A, k). Open Question 4.7. Are the committees returned by PAV, MES, and GJCR connected in EJR(A, k) for all (A, k)?

## 5 Restricted Preference Domains

Finally, we turn our attention to restricted domains, in which the approval profiles are assumed to satisfy some structural constraints. Specifically, we study two common preference domains, candidate interval (CI) and voter interval (VI) (Elkind and Lackner 2015). Both are frequently used in the approval-based multiwinner voting literature and often allow circumventing impossibilities (see, e.g., Pierczy´nski and Skowron 2022; Brill et al. 2025; Dong et al. 2025a).

We start with the CI domain. An instance (A, k) is in the CI domain if there exists an order c1,..., cm of the candidates such that for every voter v ∈N, the set {j ∈[m] | cj ∈Av} forms an interval of consecutive integers. If an instance belongs to this domain, we show that the set of JR committees is connected in a “shortest-path” manner. Theorem 5.1. On the CI domain, the set of JR committees is connected. Moreover, any two JR committees W, W ′ are connected by a path of JR committees of length d(W, W ′).

Next, we consider the VI domain. An instance is in the VI domain if there exists an ordering v1,..., vn of the voters such that for each candidate c, the support set Nc forms an interval with respect to the ordering—more formally, {i ∈ [n] | c ∈Ai} = {i ∈[n] | i∗≤i ≤j∗} for some i∗, j∗. We say that a candidate c is Pareto-dominated by a candidate c′ if Nc is a strict subset of Nc′. A candidate is Pareto-optimal if it is not Pareto-dominated by any other candidate. Theorem 5.2. On the VI domain, the set of JR committees is connected. Moreover, if two JR committees W, W ′ contain no Pareto-dominated candidates, then they can be connected by a path of JR committees of length d(W, W ′).

By contrast, shortest-path connections may not be possible if the committees contain Pareto-dominated candidates. Proposition 5.3. On the VI domain, there exist JR committees W, W ′ that cannot be connected by a path of JR committees of length d(W, W ′).

For EJR, we show that the set of committees satisfying the notion may not be connected through shortest paths, even for instances that simultaneously satisfy VI and CI.

Proposition 5.4. On the CI and VI domains, there exist EJR committees W, W ′ that cannot be connected by a path of EJR committees of length d(W, W ′).

Proof sketch. Consider the instance with voters N = {v1,..., v6}, candidates C = {c1,..., c7}, k = 3 (so n k = 2), and the following approval ballots: A1 = A2 = A3 = {c1, c2, c3, c4, c5} and A4 = A5 = A6 = {c3, c4, c5, c6, c7}. One can check that this instance is in both CI and VI, and that the committees {c1, c2, c3} and {c3, c6, c7} satisfy EJR. Now, EJR in this instance requires some voter to approve all three candidates in the committee, since all voters together form a 3-cohesive group. As no voter approves three candidates in the committee after replacing c1 or c2 in {c1, c2, c3} with c6 or c7, EJR is violated after a single replacement.

Open Question 5.5. Is the set of EJR committees connected on the CI or VI domain?

## 6 Conclusion and Future Directions

In this paper, we have studied the problem of reconfiguring proportional committees. We ask whether, for any two given proportional committees, there is a reconfiguration path consisting only of proportional committees such that each transition corresponds to swapping a pair of candidates. We demonstrate that committees satisfying justified representation (JR) or extended justified representation (EJR) do not always exhibit this type of connectivity. Nevertheless, we obtain positive results in three directions. Firstly, any two JR committees can be connected via a transition path consisting only of 2-JR committees, while any two EJR committees can be connected via 4-EJR committees. Secondly, the negative result for JR does not apply to several popular voting rules: the committees output by these rules belong to the same connected component within the set of JR committees. Thirdly, for two important restricted domains, the set of JR committees is always connected.

Our work leaves several intriguing directions for future research. For example, the connectedness of EJR committees is still not as well-understood as that of JR committees. In particular, it remains open whether it is always possible to connect two EJR committees via a path consisting only of 2-EJR committees, or whether the set of EJR committees is guaranteed to be connected in restricted domains. Moreover, our result that several well-known voting rules produce committees that can be connected by JR committees raises the following high-level question: All of these voting rules appear to select stronger committees than necessitated by the proportionality axioms. Indeed, the committee in the proof of Theorem 3.1 intuitively contains weak candidates and is not selected by common voting rules. Despite the perceived lack of quality, this committee satisfies all known proportionality axioms. Is there a principled way to explain this phenomenon, and what are good methods for distinguishing between “strong” and “weak” proportional committees?

16835

<!-- Page 8 -->

## Acknowledgments

This work was partially supported by the Singapore Ministry of Education under grant number MOE-T2EP20221- 0001, by the Deutsche Forschungsgemeinschaft under grant BR 2312/11-2, and by an NUS Start-up Grant. Most of this research was done when Chris Dong was a PhD student at the Technical University of Munich. We thank the anonymous reviewers of COMSOC 2025 and AAAI 2026 for their valuable feedback.

## References

Aziz, H.; Brill, M.; Conitzer, V.; Elkind, E.; Freeman, R.; and Walsh, T. 2017. Justified Representation in Approval- Based Committee Voting. Social Choice and Welfare, 48(2): 461–485. Boehmer, N.; Brill, M.; Cevallos, A.; Gehrlein, J.; Sánchez- Fernández, L.; and Schmidt-Kraepelin, U. 2024. Approval- Based Committee Voting in Practice: A Case Study of (Over-)Representation in the Polkadot Blockchain. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), 9519–9527. Boehmer, N.; Fish, S.; and Procaccia, A. D. 2025. Generative Social Choice: The Next Generation. In Proceedings of the 42nd International Conference on Machine Learning (ICML). Boehmer, N.; and Niedermeier, R. 2021. Broadening the Research Agenda for Computational Social Choice: Multiple Preference Profiles and Multiple Solutions. In Proceedings of the 20th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 1–5. Bredereck, R.; Fluschnik, T.; and Kaczmarczyk, A. 2022. When Votes Change and Committees Should (Not). In Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI), 144–150. Bredereck, R.; Kaczmarczyk, A.; and Niedermeier, R. 2020. Electing Successive Committees: Complexity and Algorithms. In Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI), 1846–1853. Brill, M.; Israel, J.; Micha, E.; and Peters, J. 2025. Individual Representation in Approval-Based Committee Voting. Social Choice and Welfare, 64(1–2): 69–96. Brill, M.; and Peters, J. 2023. Robust and Verifiable Proportionality Axioms for Multiwinner Voting. In Proceedings of the 24th ACM Conference on Economics and Computation (ACM-EC), 301. Brill, M.; and Peters, J. 2024. Completing Priceable Committees: Utilitarian and Representation Guarantees for Proportional Multiwinner Voting. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), 9528– 9536. Cevallos, A.; and Stewart, A. 2021. A Verifiably Secure and Proportional Committee Election Rule. In Proceedings of the 3rd ACM Conference on Advances in Financial Technologies (AFT), 29–42. Chandramouleeswaran, H.; Nimbhorkar, P.; and Rathi, N. 2025. Fair Division in a Variable Setting. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 472–480. Chen, J.; Hatschka, C.; and Simola, S. 2024. Multi-Winner Reconfiguration. In Proceedings of the 38th Annual Conference on Neural Information Processing Systems (NeurIPS). Deltl, E. M.; Fluschnik, T.; and Bredereck, R. 2023. Algorithmics of Egalitarian versus Equitable Sequences of Committees. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence (IJCAI), 2651–2658. Do, V.; Hervouin, M.; Lang, J.; and Skowron, P. 2022. Online Approval Committee Elections. In Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI), 251–257. Dong, C.; Bullinger, M.; W˛as, T.; Birnbaum, L.; and Elkind, E. 2025a. Selecting Interlacing Committees. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 630–638. Dong, C.; Frank, F.; Peters, J.; and Suksompong, W. 2025b. Reconfiguring Proportional Committees. CoRR, abs/2504.15157. Dong, C.; and Peters, J. 2025. Proportional Multiwinner Voting with Dynamic Candidate Sets. In Proceedings of the 42nd International Conference on Machine Learning (ICML). Elkind, E.; Faliszewski, P.; Igarashi, A.; Manurangsi, P.; Schmidt-Kraepelin, U.; and Suksompong, W. 2023. Justifying Groups in Multiwinner Approval Voting. Theoretical Computer Science, 969: 114039. Elkind, E.; and Lackner, M. 2015. Structure in Dichotomous Preferences. In Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI), 2019–2025. Elkind, E.; Obraztsova, S.; and Teh, N. 2024. Temporal Fairness in Multiwinner Voting. In Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI), 22633–22640. Faliszewski, P.; Skowron, P.; Slinko, A.; and Talmon, N. 2017. Multiwinner Voting: A New Challenge for Social Choice Theory. In Endriss, U., ed., Trends in Computational Social Choice, chapter 2, 27–47. AI Access. Fish, S.; Gölz, P.; Parkes, D. C.; Procaccia, A. D.; Rusak, G.; Shapira, I.; and Wüthrich, M. 2024. Generative Social Choice. In Proceedings of the 25th ACM Conference on Economics and Computation (ACM-EC), 985. Gopalan, P.; Kolaitis, P. G.; Maneva, E.; and Papadimitriou, C. H. 2009. The Connectivity of Boolean Satisfiability: Computational and Structural Dichotomies. SIAM Journal on Computing, 38(6): 332–343. Igarashi, A.; Kamiyama, N.; Suksompong, W.; and Yuen, S. M. 2024. Reachability of Fair Allocations via Sequential Exchanges. Algorithmica, 86(12): 3653–3683. Ito, T.; Demaine, E. D.; Harvey, N. J. A.; Papadimitriou, C. H.; Sideri, M.; Uehara, R.; and Uno, Y. 2011. On the Complexity of Reconfiguration Problems. Theoretical Computer Science, 412(12–14): 1054–1065. Ito, T.; Kakimura, N.; Kamiyama, N.; Kobayashi, Y.; Nozaki, Y.; Okamoto, Y.; and Ozeki, K. 2023. On Reachable

16836

<!-- Page 9 -->

Assignments under Dichotomous Preferences. Theoretical Computer Science, 979: 114196. Johnson, M.; Kratsch, D.; Kratsch, S.; Patel, V.; and Paulusma, D. 2016. Finding Shortest Paths between Graph Colourings. Algorithmica, 75(2): 295–321. Kellerhals, L.; and Peters, J. 2024. Proportional Fairness in Clustering: A Social Choice Perspective. In Proceedings of the 38th Annual Conference on Neural Information Processing Systems (NeurIPS). Lackner, M.; and Skowron, P. 2023. Multi-Winner Voting with Approval Preferences. Springer Nature. Nishimura, N. 2018. Introduction to Reconfiguration. Algorithms, 11(4): 52:1–52:25. Obraztsova, S.; Elkind, E.; and Faliszewski, P. 2020. On Swap Convexity of Voting Rules. In Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI), 1910– 1917. Obraztsova, S.; Elkind, E.; Faliszewski, P.; and Slinko, A. 2013. On Swap-Distance Geometry of Voting Rules. In Proceedings of the 12th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 383– 390. Peters, D.; Pierczy´nski, G.; and Skowron, P. 2021. Proportional Participatory Budgeting with Additive Utilities. In Proceedings of the 35th Annual Conference on Neural Information Processing Systems (NeurIPS), 12726–12737. Peters, D.; and Skowron, P. 2020. Proportionality and the Limits of Welfarism. In Proceedings of the 21st ACM Conference on Economics and Computation (ACM-EC), 793– 794. Pierczy´nski, G.; and Skowron, P. 2022. Core-Stable Committees under Restricted Domains. In Proceedings of the 18th International Conference on Web and Internet Economics (WINE), 311–329. Revel, M.; Milli, S.; Lu, T.; Watson-Daniels, J.; and Nickel, M. 2025. Representative Ranking for Deliberation in the Public Sphere. In Proceedings of the 42nd International Conference on Machine Learning (ICML). Tennakoon, D.; and Gramoli, V. 2023. Blockchain Proportional Governance Reconfiguration: Mitigating a Governance Oligarchy. In Proceedings of the 23rd IEEE/ACM International Symposium on Cluster, Cloud and Internet Computing (CCGRID), 545–556. Zamani, M.; Movahedi, M.; and Raykova, M. 2018. Rapidchain: Scaling Blockchain via Full Sharding. In Proceedings of the 25th ACM SIGSAC Conference on Computer and Communications Security (CCS), 931–948. Zech, V.; Boehmer, N.; Elkind, E.; and Teh, N. 2024. Multiwinner Temporal Voting with Aversion to Change. In Proceedings of the 27th European Conference on Artificial Intelligence (ECAI), 3236–3243.

16837
