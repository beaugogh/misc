---
title: "Deviation Dynamics in Cardinal Hedonic Games"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38783
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38783/42745
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Deviation Dynamics in Cardinal Hedonic Games

<!-- Page 1 -->

Deviation Dynamics in Cardinal Hedonic Games

Valentin Zech1, Martin Bullinger2

1Department of Computer Science, University of Oxford, UK 2School of Engineering Mathematics and Technology, University of Bristol, UK zech@vzech.de, martin.bullinger@bristol.ac.uk

## Abstract

Computing stable partitions in hedonic games is a challenging task because there exist games in which stable outcomes do not exist. Even more, these No-instances can often be leveraged to prove computational hardness results. We make this impression rigorous in a dynamic model of cardinal hedonic games by providing meta theorems. These imply hardness of deciding about the possible or necessary convergence of deviation dynamics based on the mere existence of No-instances. Our results hold for additively separable, fractional, and modified fractional hedonic games (ASHGs, FHGs, and MFHGs). Moreover, they encompass essentially all reasonable stability notions based on single-agent deviations. In addition, we propose dynamics as a method to find individually rational and contractually individual stable (CIS) partitions in ASHGs. In particular, we find that CIS dynamics from the singleton partition possibly converge after a linear number of deviations but may require an exponential number of deviations in the worst case.

## Introduction

The field of Computational Social Choice (COMSOC) is concerned with aggregating potentially conflicting individual preferences of different agents into a compromise solution (Brandt et al. 2016). With various applications to, among others, politics, multi-agent systems, and economic processes, coalition formation is among the primary areas of interest within COMSOC (Ray and Vohra 2015). Here, a group of agents must be divided into distinct coalitions, with each agent having preferences for these divisions.

A common restriction on agents’ preferences is that their utility depends only on which agents are present in their own coalition. This restriction describes the model of socalled hedonic games (Dr`eze and Greenberg 1980). Since their introduction, they have been a constant area of interest in the literature on artificial intelligence and multi-agent systems (Aziz and Savani 2016; Bullinger, Elkind, and Rothe 2024). Hedonic games have been successfully utilized to model many interesting real-world settings, such as research team formation (Alcalde and Revilla 2004), allocation of indivisible goods (Peters 2016), task allocation for wireless

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

agents (Saad et al. 2011), and community detection in social networks (Aziz et al. 2019). Further, they have proven to be a powerful theoretical model in the context of clustering (Feldman, Lewin-Eytan, and Naor 2015; Ahmadi et al. 2022; Cohen-Addad et al. 2022), one of the central research topics in the realm of machine learning.

A prominent measure for the desirability of outcomes in hedonic games is stability, defined as the absence of beneficial deviations by agents to join other coalitions (Bogomolnaia and Jackson 2002). In certain scenarios, it is sensible to additionally require partial or unanimous consent of the otherwise affected agents, which give rise to a wide landscape of notions of stability (Aziz and Savani 2016). We will focus on those defined by deviations of single agents.

Some stability notions guarantee a stable outcome in any hedonic game, e.g., contractual individual stability where a deviation requires unanimous consent of all involved agents. For most stability notions, however, stable partitions are not guaranteed to exist, even in fairly restricted game classes. This gives rise to the problem of deciding whether a given hedonic game admits a stable partition. A common observation is that No-instances, i.e., games without a stable partition, can be used as gadgets to prove computational boundaries of the existence problem (see, e.g., Sung and Dimitrov 2010; Aziz, Brandt, and Seedig 2013; Peters and Elkind 2015; Brandt, Bullinger, and Tappe 2024).1 The work discussed so far is only concerned with whether an outcome is stable or not, while it matters less how this outcome is obtained. One natural way to model the process of obtaining stable outcomes are deviation dynamics, where the agents start in some initial state and then iteratively perform deviations as long as they have an incentive to do so, see, e.g., (Bil`o et al. 2018; Gairing and Savani 2019; Brandt, Bullinger, and Wilczynski 2023; Brandt, Bullinger, and Tappe 2024). Such dynamics have previously been utilized successfully, e.g., to show that partitions satisfying a specific stability notion always exist in a particular game class (Bogomolnaia and Jackson 2002; Boehmer and Elkind 2020; Brandt, Bullinger, and Tappe 2024; C¸ askurlu and Kizilkaya 2024), to study the complexity of computing

1Two notable exceptions are aversion-to-enemies games and the locally egalitarian variant of hedonic games. In both cases, the core is nonempty but an outcome in the core is NP-hard to compute (Dimitrov et al. 2006; Bullinger and Kober 2021).

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

17310

<!-- Page 2 -->

stable outcomes (Gairing and Savani 2019) or to place an upper bound on the price of stability in terms of achieving high social welfare (Bil`o et al. 2018; Monaco, Moscardelli, and Velaj 2020). While dynamics are, therefore, a powerful general tool, scenarios in which dynamics are guaranteed to converge offer a decentralized approach to reaching desirable partitions. Thus, they give rise to interesting questions in their own right. Specifically, Brandt, Bullinger, and Wilczynski (2023) ask whether, given a hedonic game and a starting partition, dynamics possibly or necessarily converge, i.e., reach a stable partition.

## 1.1 Contribution We will make the intuition that

No-instances lead to computational intractabilities explicit. In contrast to previous work that explicitly constructs No-instances and uses them to prove individual hardness results (see, e.g., Sung and Dimitrov 2010; Brandt, Bullinger, and Tappe 2024), we present meta-theorems that treat No-instances as a black box. This approach enables future hardness results to be derived by identifying a single suitable instance. The meta theorems concern the intractability of possible and necessary convergence of dynamics, and apply to three prominent classes of hedonic games: additively separable (Bogomolnaia and Jackson 2002), fractional (Aziz et al. 2019), and modified fractional (Olsen 2012) hedonic games. They hold for most reasonable stability notions based on deviations between Nash deviations (which simply need to make the deviator better off) and contractual individual deviations (which additionally require the consent of all other agents). We demonstrate the generality of our meta theorems by applying them for a general class of voting-based stability notions that encompass a wide range of known and new stability notions.

Finally, we zoom in on a special case of dynamics that necessarily converge, namely those based on contractual individual deviations for additively separable hedonic games. When starting from the singleton partition, the resulting partition additionally is individually rational, i.e., at least as good for each agent as being on her own. We show that fast convergence is always possible. It is, however, unclear how to efficiently identify the associated deviations. Simply running any sequence of deviations may take an exponential number of steps. Nonetheless, we identify the structural reason behind this result, leading to a fixed-parameter tractability result based on the number of certain valuation pairs.

## 1.2 Related Work Hedonic games were first introduced by

Dr`eze and Greenberg (1980), and later popularized by Bogomolnaia and Jackson (2002), Banerjee, Konishi, and S¨onmez (2001), and Cechl´arov´a and Romero-Medina (2001). An overview is provided in the book chapters by Aziz and Savani (2016) and Bullinger, Elkind, and Rothe (2024).

The axiomatic and computational properties of stability have been studied extensively in cardinal hedonic games (see, e.g., Dimitrov et al. 2006; Sung and Dimitrov 2010; Aziz, Brandt, and Seedig 2013; Woeginger 2013; Bil`o et al. 2018; Aziz et al. 2019; Boehmer and Elkind 2020; Brandt, Bullinger, and Tappe 2024). Sung and Dimitrov (2010), specifically, provide a detailed overview of stability based on single-agent deviations in additively separable hedonic games. Related to our efforts to study the computational complexity of finding a partition that is individually rational and contractually individually stable, Aziz, Brandt, and Seedig (2013) provide an algorithm for computing a (not necessarily individually rational) partition that is contractually individually stable in additively separable hedonic games. Further, Peters and Elkind (2015) utilize a meta approach to show hardness for several game classes and stability notions simultaneously, similar to our unified theory. In contrast to our investigation of deviation dynamics, their paper concerns the general existence of stable outcomes.

In this light, a recent trend has been to study the dynamic aspects of coalition formation based on beneficial deviations, which offer a decentralized approach to finding stable outcomes and can thus model specific real-world scenarios more realistically. Most related is the work by Brandt, Bullinger, and Wilczynski (2023) that studies the computational complexity of possible and necessary convergence of dynamics in a variety of game classes. The only overlap with our work is the consideration of fractional hedonic games. While Brandt, Bullinger, and Wilczynski (2023) only study individual stability, our meta theorems work for a much larger set of stability notions and additionally concerns other classes of cardinal hedonic games. Subsequently, Bullinger and Suksompong (2024) study possible and necessary convergence for the equivalent of Nash stability in a generalization of additively separable hedonic games.

Further, Bil`o et al. (2018) study Nash stability in fractional hedonic games and, for instance, utilize dynamics to design an algorithm that approximates the maximum social welfare of a Nash stable outcome in polynomial time. Gairing and Savani (2019) settle the complexity of deciding whether a stable partition exists in symmetric additively separable hedonic games by treating this question as local search problems. Brandt, Bullinger, and Tappe (2024) also study computational questions related to the existence of stable partitions, where all their positive results are obtained by proving convergence of dynamics. Boehmer, Bullinger, and Kerkmann (2023) propose a version of hedonic games specifically adapted to a dynamic setting, where utilities change after a deviation takes place. Their work also has implications for a fixed-utility setting: In particular, they consider the computational complexity of convergence in a given time limit and prove hardness results for additively separable hedonic games. In addition, Hoefer, Vaz, and Wagner (2018), Bullinger and Kober (2021), and Fanelli, Monaco, and Moscardelli (2021) study dynamics in hedonic games based on group deviations. Finally, we note that similar dynamic approaches to finding stable solutions have been studied in the context of stable matchings (Abeledo and Rothblum 1995; Hoefer, Vaz, and Wagner 2018; Brandt and Wilczynski 2024).

## Preliminaries

In this section, we introduce preliminaries. We use the convention that N is the set of nonnegative integers, including 0. For i ∈N, i ≥1, we denote [i]:= {1,..., i}.

17311

<!-- Page 3 -->

## 2.1 Hedonic Games

We consider a finite set N of n:= |N| agents. A nonempty subset of agents is called a coalition. We aim to partition the agents in N into disjoint coalitions. A coalition structure (or partition) of N is a subset π ⊆2N with S

C∈π C = N, where, for all C, D ∈π, it holds that C = D, or C ∩D = ∅. Given an agent a ∈N, we denote by π(a) the coalition in π that contains a. Let Na = {C ⊆N | a ∈C} denote the set of all coalitions that a can belong to. We refer to the partition π = {{a} | a ∈N} as the singleton partition, and to π = {N} as the grand coalition. Further, for each agent a ∈N, we call {a} the singleton coalition of a.

A hedonic game G = (N, ≿) consists of a set N of agents, and a preference profile ≿= (≿a)a∈N where ≿a⊆ Na × Na is a complete, reflexive, and transitive binary relation called agent a’s preference relation (Dr`eze and Greenberg 1980). Given two coalitions C, D ∈Na, we write C ≻a D if C ≿a D but not D ≿a C (i.e., a strictly prefers C over D). We say that a partition π is individually rational if π(a) ≿a {a} for each agent a ∈N, i.e., no agent would strictly prefer to be in her respective singleton coalition.

Agents have preferences over partitions based on preferences over coalitions. Given two partitions π, π′ of N, we say that π ≿a π′ if and only if π(a) ≿a π′(a). Further, we denote by G −a the game with agent set N \ {a} that is induced by G by removing agent a. We write π −a to mean the partition of N \ {a} that resulted from π by removing a from her coalition, formally, π −a:= {C \ {a} | C ∈ π, C̸ = {a}}.

We consider classes of hedonic games in which preference relations evolve from cardinal utility functions, i.e., agents have numeric value for each coalition and preferences are based on comparing these values. Formally, a cardinal hedonic game is given by the pair (N, u) where N is the agent set and u = (ua: Na →Q)a∈N a profile of utility functions. Then, (N, u) induces the hedonic game (N, ≿) where, for every agent a ∈N and coalitions C, D ∈Na, we define C ≿a D if and only if ua(C) ≥ua(D). We say that ua(C) is a’s utility for coalition C and extend this to utilities for partitions by setting ua(π):= ua(π(a)).

Cardinal hedonic games generally require to specify a utility for an exponentially large set of coalitions. To avoid listing these all explicitly, several classes of cardinal hedonic games have been proposed where utility functions are represented succinctly by merely specifying valuations for single agents. Let G = (N, u) be a cardinal hedonic game and let (va: N →Q)a∈N be a collection of valuation functions.

Following Bogomolnaia and Jackson (2002), G is called an additively separable hedonic game (ASHG) if for all a ∈N, C ∈Na it holds that ua(C) = P b∈C\{a} va(b). Following Aziz et al. (2019), G is called a fractional hedonic game (FHG) if for all a ∈N, C ∈Na it holds that ua(C) = P b∈C\{a}

va(b)

|C|. Following Olsen (2012), G is called a modified fractional hedonic game (MFHG) if for all a ∈N, it holds that ua({a}) = 0 and for all C ∈Na, C̸ = {a} it holds that ua(C) = P b∈C\{a}

va(b) |C|−1. In other words, the utility in an ASHG is the sum of val- uations for agents in the considered coalition, and the utility in an FHG and MFHG is the average valuation, where FHGs include the consideration of the agent herself. All three game classes are fully specified by the valuation functions and we therefore also represent an ASHG, FHG, or MFHG G by the pair (N, v), where v = (va: N →Q)a∈N is a profile of valuation functions.

## 2.2 Single-Agent Stability

We now formalize how to capture stability based on beneficial deviations by single agents. Given a hedonic game G = (N, ≿), a single-agent deviation of an agent a ∈N transforms a partition π of N into a partition π′ of N, where π(a)̸ = π′(a), and, for all agents b ∈N \ {a}, it holds that π(b) \ {a} = π′(b) \ {a}. We denote such a deviation by π a→π′. Intuitively, agent a deviates away from coalition π(a), to join coalition π′(a) (importantly, π′(a) can be a’s singleton coalition), while all other coalitions remain unchanged.

A minimum requirement for the desirability of a deviation is whether the deviator is better off by performing this deviation. A Nash deviation is a single-agent deviation π a→π′ of an agent a ∈N such that π′(a) ≻a π(a). A partition π which does not admit a Nash deviation is said to be Nash stable (NS), and π is called an NS partition.

While Nash stability offers a very strong and desirable solution concept, NS deviations completely disregard the opinion of members in the abandoned and welcoming coalition. In this light, several stability notions enforce additional requirements to be satisfied for a deviation to be valid. We introduce a general class of such stability notions based on voting among the involved agents.

Let C ⊆N be a coalition and a ∈N an agent. Following Brandt, Bullinger, and Tappe (2024), we define the favour-in set Fin(C, a) and favour-out set Fout(C, a) of C with respect to a as

Fin(C, a):= {b ∈C \ {a} | C ∪{a} ≻b C \ {a}} and

Fout(C, a):= {b ∈C \ {a} | C \ {a} ≻b C ∪{a}}.

These capture the agents in C that prefer a inside or outside the coalition C. Note that the definition is valid regardless of whether a is part of C.

Let qout, qin ∈[0, 1] be two real numbers interpreted as quotas. A Nash deviation π a→π′ of an agent a ∈N is called a (qout, qin)-vote deviation if 1. |Fout(π(a), a)| ≥qout(|Fin(π(a), a)| + |Fout(π(a), a)|) and 2. |Fin(π′(a), a)| ≥qin(|Fin(π′(a), a)| + |Fout(π′(a), a)|). Hence, such a deviation requires that at least a qout-fraction of the nonindifferent members of the abandoned coalition and a qin-fraction of the nonindifferent members of the welcoming coalition are strictly in favor of the deviation. Now, a partition is said to be (qout, qin)-voting-stable ((qout, qin)- VS) if it does not admit a (qout, qin)-vote deviation.

Our stability framework captures most single-deviation stability notions commonly considered in the literature. If qout, qin ∈{0, 1}, we obtain stability notions based on

17312

<!-- Page 4 -->

unanimous consent whenever consent is required. Specifically, (0, 0)-VS is NS, (0, 1)-VS is called individual stability (IS), (1, 0)-VS is called contractual Nash stability (CNS), and (1, 1)-VS is called contractual individual stability (CIS) (Bogomolnaia and Jackson 2002; Sung and Dimitrov 2007). In addition, (qout, qin)-VS generalizes previously studied voting-based stability concepts: Gairing and Savani (2019) consider (0, qin)-VS and (qout, 0)-VS under the names of vote-in and vote-out stability (VIS and VOS), and Brandt, Bullinger, and Tappe (2024) consider (0, 1

2)-VS, (1 2, 0)-VS, and (1

2, 1 2)-VS. Brandt, Bullinger, and Tappe (2024) call the latter separate-majorities stability (SMS). Among all of these, only CIS guarantees the existence of stable partitions.

Given a stability notion χ, we refer to the corresponding deviations and stable partitions as χ deviations and χ partitions, respectively.

Given two stability notions χ and χ′, we write χ ⇁ ⊂χ′ if every χ deviation is also a χ′ deviation. For instance, for every qout, qin ∈[0, 1], it holds that (qout, qin)-VS ⇁ ⊂NS and CIS ⇁ ⊂(qout, qin)-VS.

## 2.3 Standard Stability Notions

In the last section, we introduced a class of specific stability notions based on voting. To state our meta theorems, we propose a novel condition to capture an even more general class of stability notions between NS and CIS. These are defined for cardinal hedonic games and should satisfy two properties:

1. the feasibility of deviations only depends on the utility changes of the involved agents, not their identities, i.e., deviations are anonymously hedonic, 2. deviations that are stronger than feasible deviations are also feasible, i.e., deviations are monotonic.

We formalize this in the following.

Let G = (N, u) be a cardinal hedonic game, let a ∈N be an agent, and let π, π′ be two partitions of N. We refer to ucG(a, π, π′):= (ua(π), ua(π′)) as the utility-change tuple of a with respect to G, π and π′. Further, we refer to the multisets UC out

G (a, π, π′):= {ucG(b, π, π′) | b ∈π(a) \ {a}} and UC in

G(a, π, π′):= {ucG(b, π, π′) | b ∈π′(a) \ {a}} as the utility-change-out multiset and utility-change-in multiset of a with respect to G, π and π′, respectively. We denote by UC the set of all utility-change multisets (that is, both utility-change-out and utility-change-in multisets). For all functions ucG, UC out

G, and UC in

G, we will omit the game G whenever it is clear from the context.

We say that a stability notion χ is anonymously hedonic if there exists a polynomial-time computable function fχ: UC×UC×(Q×Q) →{0, 1}, such that, in case π a→π′, then fχ(UC out(a, π, π′), UC in(a, π, π′), uc(a, π, π′)) is 1 in case π a→π′ is a χ deviation, and 0 otherwise. Simply put, the validity of a deviation with respect to an anonymously hedonic stability notion solely depends on the changes in the utility of abandoned and welcoming coalitions and that of the deviator. In particular, this captures all stability notions that are implied by NS, and further only depend on the sizes of the favor-in and favor-out sets of the abandoned and welcoming coalitions. However, the class of anonymously hedonic stability notions allows for more nuanced requirements. For example, a deviation may be allowed if it is an NS deviation, and increases the utilitarian welfare, defined as P a∈N ua(π) for partition π. Next, given two multisets X, Y ∈UC, we say that X dominates Y, written Y ⊴X, if it holds that |Y | ≤|X| and:

∀(y, y′) ∈Y, (x, x′) ∈X: y′ −y ≤x′ −x. Now, an anonymously hedonic stability notion χ is monotone if, for all X, X′, Y, Y ′ ∈UC, and z, z′ ∈Q×Q, where X ⊴X′, Y ⊴Y ′, and {z} ⊴{z′}, it holds that:

fχ(X, Y, z) ≤fχ(X′, Y ′, z′), i.e., whenever a deviation is allowed with parameters X, Y, z, then it must also be allowed with parameters X′, Y ′, z′. We will refer to anonymously hedonic monotone stability notions as standard stability notions.

We note that our voting-based stability notions are standard stability notions, as the relevant favor-in and favor-out sets can be reconstructed with the information captured in the utility-change multisets. We defer the formal proof to the full version of this paper (Zech and Bullinger 2025). There, we also provide an example illustrating standard stability. Proposition 1. Let qout, qin ∈[0, 1]. Then, (qout, qin)-VS is a standard stability notion.

We remark that our notion of monotonicity does not capture all stability notions between NS and CIS, e.g., it fails to capture some notions that rely on the egalitarian welfare.

## 2.4 Deviation Dynamics

We are ready to introduce the central concept of this paper, which we will utilize to formulate our decision problems.

Stability notions naturally induce dynamics, where, given a hedonic game and a starting partition of the agents, we iteratively obtain successor partitions by letting agents perform deviations from the current partition in alignment with the stability notion.

Formally, let χ be a stability notion, let G = (N, ≿) be a hedonic game with a set N of agents, and let π0 be a partition of N. Then, an execution of the χ dynamics of (G, π0) is a finite or infinite sequence (πi)0≤i≤t of partitions, i.e., t ∈N ∪{+∞}, together with a corresponding sequence (ai)1≤i≤t of deviating agents, such that for every 1 ≤i ≤t, it holds that πi−1 ai→χ πi, i.e., πi evolves from πi−1 by a χ deviation of ai. We say that an execution of the χ dynamics of (G, π0) converges if πt is a χ partition.

We say that the χ dynamics of (G, π0) possibly converges if some execution of (G, π0) converges. Moreover, we say that the χ dynamics of (G, π0) necessarily converges if every execution of the χ dynamics of (G, π0) is finite. This means that we necessarily reach a χ partition if we continue applying χ deviations. By contrast, if the χ dynamics of (G, π0) does not converge necessarily, there have to be executions where the same partition is reached infinitely often. In this case, we say that the dynamics cycles.

As computational decision problems, possible and necessary convergence can be captured as follows.

17313

<!-- Page 5 -->

POSSIBLE CONVERGENCE OF DYNAMICS (χ-PCD) Input: A hedonic game G and a starting partition π0. Question: Is there a sequence of χ deviations on G that results in a χ partition when starting from π0?

NECESSARY CONVERGENCE OF DYNAMICS (χ-NCD) Input: A hedonic game G and a starting partition π0. Question: Is every sequence of χ deviations on G finite when starting from π0?

Typically, we consider χ-PCD and χ-NCD for a specific class of hedonic games, such as ASHGs.

We conclude with the simple observation that CIS dynamics necessarily converge. This follows immediately because we operate on a finite game and every CIS deviation increases the utilitarian welfare P a∈N ua(π) (Aziz, Brandt, and Seedig 2013). Observation 2. Every execution of the CIS dynamics converges necessarily.

## 3 Presentation of Meta Theorems

We now present our meta theorems. A proof sketch can be found in Section 4 and the full proof is provided in the full version of our paper. Our first theorem states that the existence of a cycling dynamics implies hardness of deciding about possible convergence of dynamics. Theorem 3. Let χ be a standard stability notion with χ ⇁ ⊂NS and CIS ⇁ ⊂χ. Assume that there exists an ASHG, FHG, or MFHG Gχ and partition πχ such that the χ dynamics of (Gχ, πχ) must cycle. Then χ-PCD is NP-hard for the game class of Gχ (e.g., for ASHGs if Gχ is an ASHG).

Moreover, if there exists an instance in which the dynamics can cycle but necessarily converge after the removal of a singleton coalition, we obtain hardness of deciding about necessary convergence of dynamics. Theorem 4. Let χ be a standard stability notion with χ ⇁ ⊂NS and CIS ⇁ ⊂χ. Assume that there exists an ASHG, FHG, or MFHG Gχ and partition πχ that contains a singleton coalition {a} ∈πχ, such that the χ dynamics can cycle on (Gχ, πχ), but necessarily converge on (Gχ −a, πχ −a). Then χ-NCD is coNP-hard for the game class of Gχ.

The precondition for the required game in Theorem 4 may seem intricate, but it is quite weak. For instance, it is satisfied whenever there exists a game in which the dynamics starting from the singleton partition can cycle. Indeed, in this case, one can obtain the desired game by iteratively removing agents until the dynamics from the singleton coalition necessarily converges. Then, the penultimate game in this procedure satisfies the prerequisites of Theorem 4. Moreover, both theorems hold whenever there exists an instance without a stable partition. In this case, the dynamics from any starting partition (e.g., the singleton partition) must cycle. We state the latter observation in the following corollary. Corollary 5. Let χ be a standard stability notion with χ ⇁ ⊂NS and CIS ⇁ ⊂χ. Assume that there exists an ASHG, FHG, or MFHG Gχ without a χ partition. Then, χ-PCD is NP-hard and χ-NCD is coNP-hard for the game class of Gχ.

We can directly apply our corollary for established stability notions of which it is known that instances without stable partitions exist. For instance, there exist ASHGs without an IS or CNS (and, therefore, no NS) partition (Bogomolnaia and Jackson 2002, Example 5; Sung and Dimitrov 2007, Example 2). Our meta theorems (Theorems 3 and 4) apply uniformly to all standard stability notions, including NS, IS, CNS, VIS, VOS, and SMS in ASHGs, FHGs, and MFHGs. All of these also follow from Theorem 6 below.

In fact, we now demonstrate the applicability of our meta theorems for any deviation concept between NS deviations and voting-based notions weaker than CIS deviations. More precisely, consider (qout, qin)-VS for any qout, qin ∈[0, 1]. In case that qout = qin = 1, this is CIS, for which dynamics necessarily converge (Observation 2). In all other cases, we show that Theorems 3 and 4 can be applied for all three game classes. We thus obtain a dichotomy that separates CIS from other voting-based stability notions.

Theorem 6. Let χ be a standard stability notion such that χ ⇁ ⊂NS and (qout, qin)-VS ⇁ ⊂χ for some qout, qin ∈[0, 1]. Then, χ-PCD is NP-hard and χ-NCD is coNP-hard for ASHGs, FHGs, and MFHGs if qout < 1 or qin < 1.

The proof is presented in the full version of our paper. It relies on constructing two games for which we apply Theorems 3 and 4 once each. We further distinguish whether for the relevant stability notion χ it holds that (qout, 1)-VS

⇁ ⊂χ or (1, qin)-VS ⇁ ⊂χ. All constructed games consist of a large set of deviating agents and a small set of gadget agents that never perform deviations (and, in fact, their valuation function is the 0-function, under which all coalitions yield an identical utility). Starting from a predetermined partition, there always exists precisely one deviating agent that can perform a permissible χ deviation, while no other deviation is possible that is even an NS deviation. Performing this deviation yields a partition that is identical up to a permutation of agents. Hence, we establish inevitable cycling, and, therefore, games suitable to apply Theorem 3. The starting partitions can then be turned into partitions satisfying the preconditions of Theorem 4 by removing the first deviator from her coalition and placing her in a singleton coalition.

## 4 Proof Sketch of Meta Theorems In this section, we outline the proofs of

Theorems 3 and 4. Both rely on a reduction from RESTRICTED EXACT COVER BY 3-SETS (RX3C). An instance of RX3C consists of a finite set of elements U = {e1,..., e3h} and a family M = {M1,..., M3h} subsets of U of size 3 such that every element of U belongs to exactly three sets in M. An instance is a Yes-instance if and only if there is a selection of exactly h sets from M whose union is U. RX3C is known to be NP-complete (Karp 1972; Gonzalez 1985).

Both proofs are performed in two steps: first, we encode the combinatorial structure of an RX3C instance as deviation dynamics, then we use the games assumed by the respective theorem as a gadget. The first step is the same for both theorems and is outlined in Figure 1. Given an instance (U, M) of RX3C, we introduce sets NU and NM of element agents and set agents representing U and M, respec-

17314

<!-- Page 6 -->

γ β α sX sY sZ xa xb xc xd xe xf g1 g2 Γ

NU

NM

Variable

Gadget

**Figure 1.** Illustration of the reduction. A covering instance (U, M) is represented by agents NU and NM. Here, we have U = {a,..., f} and M = {X, Y, Z} with X = {a, b, c}, Y = {b, c, d}, and Z = {d, e, f}. Black and red arrows indicate potential utility increases and decreases, respectively. Important coalitions of the starting partition are indicated in blue. In Yes-instances, dynamics can lead to agent γ ending up in a singleton coalition.

tively. Set agents receive a positive utility from the element agents corresponding to their contained elements. At the top, there is a set Γ of grouping agents, identical in size to the number of sets in an exact cover, e.g., 2 agents if |U| = 6. Further down, there are special agents α and β. The latter has a very high valuation for α but dislikes set agents. At the bottom, there is a variable gadget containing a dedicated agent γ who is the only agent that can interact with the other gadget agents through deviations.

In Figure 1, black arrows indicate deviation incentives, while red arrows represent deviation obstacles. The two important coalitions of the starting partition are indicated in blue. Generally, agents perform deviations “upwards.”

Element agents can freely join the coalitions of grouping agents, which can in principle lead to coalitions containing any grouping agent and any subset of element agents. However, set agents can only join the coalition of a grouping agent if it contains exactly the agents corresponding to its contained elements.2 Once this happens, a coalition is created from and towards which no more deviations happen.

Over time, the coalition of α contains less and less set agents. This allows β to join this coalition if and only if the deviated set agents correspond to an exact cover of U. This in turn allows the abandoned γ to engage in deviations within the gadget. In the deviation sequence up to this step, almost all performed deviations are CIS deviations and, therefore,

2Initially, coalitions of element agent contain an additional restricting agent that prevents set agents from joining. These are omitted from the figure for simplicity.

χ deviations. The only deviation that is possibly not a CIS deviation is when β joins α. When performing this deviation, it is the only time in the proof that we use that we need a standard stability notion.

By specifying the variable gadget, we can leverage this general reduction to prove Theorems 3 and 4. For possible convergence, we use the game in which cycling dynamics must happen. For each of the coalitions of the starting partition causing necessary cycling, we append a copy of the construction in Figure 1. If the source instance was a Noinstance, then agents of type γ (in the multiple copies) never end up in singleton coalitions. Hence, the gadget agents have to cycle inevitably. If, however, the source instance was a Yes-instance, then agents of type γ can join the coalitions from the gadget with CIS deviations, leading to a stable partition. Hence, dynamics possibly converge if and only if the source instance was a Yes-instance.

We now turn to necessary convergence. Note that coNPhardness for necessary convergence is identical to NPhardness of the question whether dynamics possibly cycle. We now use the possibly cycling game with its dedicated agent a as a variable gadget and identify γ with a. Hence, if the source instance was a No-instance, dynamics can never change the coalition of a, and, therefore, dynamics have to converge in the variable gadget. Otherwise, if the source instances was a Yes-instance, agent a can initiate cycling once she is in a singleton coalition.

## 5 Contractual Individual Stability

As CIS dynamics necessarily converge in any hedonic game (cf. Observation 2), CIS-PCD and CIS-NCD are trivially polynomial-time solvable. Moreover, Aziz, Brandt, and Seedig (2013) provide an algorithm to compute some CIS partition in polynomial time for ASHGs.3 Unfortunately, their algorithm fails to produce partitions that satisfy individual rationality, i.e., some agents might have a large negative utility. Notably, as CIS deviations preserve individual rationality, CIS dynamics from the singleton coalition guarantee the existence of individually rational CIS partitions. Observation 7. Let G be a hedonic game together with an individually rational partition π0. Then, any execution of the CIS dynamics of (G, π0) converges to an individually rational CIS partition.

By contrast, it is NP-hard to decide whether CIS dynamics lead to individually rational outcomes, when starting from a general partition. This result holds even for fairly restricted valuations, e.g., to {−1, 1}. We defer all missing proofs in this section to the full version of our paper. Theorem 8. Let f +: N →Q+ and f −: N →Q−be two functions with f +(n) ≥|f −(n)| for all n ∈N. It is NPhard to decide whether the CIS dynamics in an ASHG, FHG, or MFHG can converge to an individually rational partition from a given starting partition π, even when valuations are restricted to {f −(n), f +(n)} for games with n agents.

Hence, for each hedonic game, one can compute an individually rational CIS partition by running CIS dynamics

3Bullinger et al. (2025) correct an inaccuracy in this algorithm.

17315

<!-- Page 7 -->

from the singleton partition. However, it is not clear whether one can efficiently find a short converging sequence of CIS deviations, i.e., a sequence that consists of polynomially many steps. We, therefore, dedicate the remainder of this section to this question, and focus our attention on ASHGs.

First, we show that short converging sequences taking a linear number of CIS deviations always exist.

Theorem 9. Let G be an ASHG and let π be a CIS partition that was reached through an execution of the CIS dynamics on G when starting from the singleton partition. Then π can be reached from the singleton partition after exactly |N| − |π| CIS deviations.

Proof. Consider an execution of the CIS dynamics on G when starting from the singleton partition. Our proof relies on the following claim which is proved in the appendix.

Claim 10. Every coalition C in π contains exactly one agent that never deviated in the execution of the CIS dynamics.

We denote the agents that never deviate to reach π as per Claim 10 as the owners of their respective coalitions in π. Moreover, given an arbitrary agent a ∈N, we denote by oa the owner of the coalition π(a). Now, given the original (possibly exponential length) sequence of CIS deviations that resulted in π, consider the last deviation of each agent. We construct a new, shortened sequence of |N| −|π| deviations, where each agent a that is not the owner of a coalition performs exactly one deviation from her singleton coalition to join oa. We order this new deviation sequence by when the agents performed their last deviation in the original sequence. It is clear that this new deviation sequence results in the same partition π after exactly |N| −|π| steps.

It remains to show that the new sequence consists only of CIS deviations. As each agent deviates from her singleton coalition, no agent will ever be blocked from leaving. Now, given a nonowner agent a, let Cnew be the coalition that she joins in the new sequence and let Cori be the coalition that she joins in the original sequence. Observe that Cnew ⊆Cori must hold. Then, a not being blocked from joining Cnew directly follows from the fact that the original sequence consists only of CIS deviations. Further, in case there exists an agent b ∈Cori\Cnew with va(b) > 0, then b must have deviated from a coalition that contains a in the original sequence, which cannot have been a CIS deviation. Hence, va(b) ≤0, and thus ua(Cnew) ≥ua(Cori) > 0 must hold, where the strict inequality follows because Cori was reached in a CIS dynamics starting from the singleton partition by a deviation of a. Therefore, the deviation of a is a CIS deviation. Since a was chosen arbitrarily, this concludes the proof.

An additional observation from the last theorem is that in the constructed dynamics every agent deviates at most once. However, finding this sequence needed knowledge of a possibly much longer sequence. This raises the question whether all CIS dynamics starting from the singleton partition are short. We answer this question negatively by constructing a family of instance where CIS dynamics can have exponential length with respect to the game size.

Theorem 11. Let χ be a stability notion with CIS ⇁ ⊂χ. Then the χ dynamics starting from the singleton partition may take an exponential number of steps with respect to the game’s input size.

It remains an interesting open problem to determine the complexity of computing an individually rational CIS partition (even without using dynamics). We make first progress towards this question by identifying the structural reason behind Theorem 11. The games constructed in its proof heavily rely on valuations that are positive in one direction but 0 in the other. If we bound the number of agents with such valuations, we can efficiently compute individually rational CIS partitions. To this end, for an ASHG G = (N, u), define s(G):= |{a ∈N | ∃b ∈N: va(b) > 0 ∧vb(a) = 0}|.

The proof idea is as follows. We construct the desired CIS dynamics in three phases. Define X:= {a ∈N | ∃b ∈N: va(b) > 0 ∧vb(a) = 0}, i.e., |X| = s(G). In the first phase, the agents not in X deviate. After at most one deviation each, a partition is reached in which these agents cannot deviate again. In the second phase, agents in X deviate at most once, joining best coalitions containing agents not in X. The first two phases comprise at most n deviations. In the third phase, arbitrary CIS deviations are performed. It can be shown that, after the second phase, deviations can only be performed by agents in X, joining other agents in X. Hence, this can lead to at most s(G)s(G) unique partitions.

Theorem 12. An execution of the CIS dynamics starting from the singleton partition taking at most s(G)s(G) + n deviations can be computed in polynomial time with respect to the game’s input size.

## 6 Conclusion

We presented a meta approach to determine the computational complexity of deciding whether the deviation dynamics possibly or necessarily converge in a hedonic game based on the mere existence of simple No-instances. Our results encompass all standard stability notions based on deviations between NS and CIS deviations. Moreover, they hold for the prominent game classes of additively separable, fractional, and modified fractional hedonic games. We also investigated the computational complexity of finding an individually rational CIS partition in an ASHG. Here, dynamics may converge in a linear number of steps, but we can only efficiently extract the deviations for fast convergence when restricting the number of certain valuation pairs.

Natural directions for future work include reevaluating our hardness results for restricted domains of valuations, such as, utilities based on friend-and-enemy evaluations (Dimitrov et al. 2006), different classes of hedonic games, including ordinal models, or stability notions that rely on group deviations. Further, while Boehmer, Bullinger, and Kerkmann (2023) discuss the structure of outcomes and running time of simulations for NS dynamics, an interesting direction would be a comprehensive experimental evaluation for a broader set of stability notions. Finally, an intriguing open question is the computational complexity of computing an individually rational CIS partition, and the applicability of our established results to game classes other than ASHGs.

17316

<!-- Page 8 -->

## Acknowledgments

Most of this work was done when Martin Bullinger was at the University of Oxford. Martin Bullinger was supported by the AI Programme of The Alan Turing Institute.

## References

Abeledo, H.; and Rothblum, U. G. 1995. Paths to marriage stability. Discrete Applied Mathematics, 63(1): 1–12. Ahmadi, S.; Awasthi, P.; Khuller, S.; Kleindessner, M.; Morgenstern, J.; Sukprasert, P.; and Vakilian, A. 2022. Individual preference stability for clustering. In Proceedings of the 39th International Conference on Machine Learning (ICML), 197–246. Alcalde, J.; and Revilla, P. 2004. Researching with whom? Stability and manipulation. Journal of Mathematical Economics, 40(8): 869–887. Aziz, H.; Brandl, F.; Brandt, F.; Harrenstein, P.; Olsen, M.; and Peters, D. 2019. Fractional Hedonic Games. ACM Transactions on Economics and Computation, 7(2): 1–29. Aziz, H.; Brandt, F.; and Seedig, H. G. 2013. Computing Desirable Partitions in Additively Separable Hedonic Games. Artificial Intelligence, 195: 316–334. Aziz, H.; and Savani, R. 2016. Hedonic Games. In Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D., eds., Handbook of Computational Social Choice, chapter 15. Cambridge University Press. Banerjee, S.; Konishi, H.; and S¨onmez, T. 2001. Core in a simple coalition formation game. Social Choice and Welfare, 18: 135–153. Bil`o, V.; Fanelli, A.; Flammini, M.; Monaco, G.; and Moscardelli, L. 2018. Nash Stable Outcomes in Fractional Hedonic Games: Existence, Efficiency and Computation. Journal of Artificial Intelligence Research, 62: 315–371. Boehmer, N.; Bullinger, M.; and Kerkmann, A. M. 2023. Causes of Stability in Dynamic Coalition Formation. In Proceedings of the 37th AAAI Conference on Artificial Intelligence (AAAI), 5499–5506. Boehmer, N.; and Elkind, E. 2020. Individual-Based Stability in Hedonic Diversity Games. In Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI), 1822– 1829. Bogomolnaia, A.; and Jackson, M. O. 2002. The Stability of Hedonic Coalition Structures. Games and Economic Behavior, 38(2): 201–230. Brandt, F.; Bullinger, M.; and Tappe, L. 2024. Stability Based on Single-Agent Deviations in Additively Separable Hedonic Games. Artificial Intelligence, 334: 104160. Brandt, F.; Bullinger, M.; and Wilczynski, A. 2023. Reaching Individually Stable Coalition Structures. ACM Transactions on Economics and Computation, 11(1–2): 4:1–65. Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia, A. D., eds. 2016. Handbook of Computational Social Choice. Cambridge University Press. Brandt, F.; and Wilczynski, A. 2024. On the Convergence of Swap Dynamics to Pareto-Optimal Matchings. Journal of Artificial Intelligence Research, 80: 1063–1098.

Bullinger, M.; Dunajski, A.; Elkind, E.; and Gilboa, M. 2025. Single-Deviation Stability in Additively Separable Hedonic Games with Constrained Coalition Sizes. Technical report, https://arxiv.org/abs/2510.12641. Bullinger, M.; Elkind, E.; and Rothe, J. 2024. Cooperative Game Theory. In Rothe, J., ed., Economics and Computation: An Introduction to Algorithmic Game Theory, Computational Social Choice, and Fair Division, chapter 3, 139– 229. Springer. Bullinger, M.; and Kober, S. 2021. Loyalty in Cardinal Hedonic Games. In Proceedings of the 30th International Joint Conference on Artificial Intelligence (IJCAI), 66–72. Bullinger, M.; and Suksompong, W. 2024. Topological Distance Games. Theoretical Computer Science, 981: 114238. C¸ askurlu, B.; and Kizilkaya, F. E. 2024. On hedonic games with common ranking property. Annals of Mathematics and Artificial Intelligence, 92(3): 581–599. Cechl´arov´a, K.; and Romero-Medina, A. 2001. Stability in Coalition Formation games. International Journal of Game Theory, 29: 487–494. Cohen-Addad, V.; Lattanzi, S.; Maggiori, A.; and Parotsidis, N. 2022. Online and consistent correlation clustering. In Proceedings of the 39th International Conference on Machine Learning (ICML), 4157–4179. Dimitrov, D.; Borm, P.; Hendrickx, R.; and Sung, S. C. 2006. Simple Priorities and Core Stability in Hedonic Games. Social Choice and Welfare, 26(2): 421–433. Dr`eze, J. H.; and Greenberg, J. 1980. Hedonic Coalitions: Optimality and Stability. Econometrica, 48(4): 987–1003. Fanelli, A.; Monaco, G.; and Moscardelli, L. 2021. Relaxed core stability in fractional hedonic games. In Proceedings of the 30th International Joint Conference on Artificial Intelligence (IJCAI), 182–188. Feldman, M.; Lewin-Eytan, L.; and Naor, J. 2015. Hedonic clustering games. ACM Transactions on Parallel Computing (TOPC), 2(1): 1–48. Gairing, M.; and Savani, R. 2019. Computing Stable Outcomes in Symmetric Additively Separable Hedonic Games. Mathematics of Operations Research, 44(3): 1101–1121. Gonzalez, T. F. 1985. Clustering to minimize the maximum intercluster distance. Theoretical Computer Science, 38: 293–306. Hoefer, M.; Vaz, D.; and Wagner, L. 2018. Dynamics in matching and coalition formation games with structural constraints. Artificial Intelligence, 262: 222–247. Karp, R. M. 1972. Reducibility among Combinatorial Problems. In Miller, R. E.; and Thatcher, J. W., eds., Complexity of Computer Computations, 85–103. Plenum Press. Monaco, G.; Moscardelli, L.; and Velaj, Y. 2020. Stable outcomes in modified fractional hedonic games. Auton. Agents Multi Agent Syst., 34(1): 4. Olsen, M. 2012. On defining and computing communities. In Proceedings of the 18th Computing: The Australasian Theory Symposium (CATS), volume 128 of Conferences in Research and Practice in Information Technology (CRPIT), 97–102.

17317

<!-- Page 9 -->

Peters, D. 2016. Graphical Hedonic Games of Bounded Treewidth. In Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI). Peters, D.; and Elkind, E. 2015. Simple Causes of Complexity in Hedonic Games. In Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI), 617–623. Ray, D.; and Vohra, R. 2015. Coalition Formation. In Young, H. P.; and Zamir, S., eds., Handbook of Game Theory with Economic Applications, volume 4, chapter 5, 239–326. Elsevier. Saad, W.; Han, Z.; Basar, T.; Debbah, M.; and Hjorungnes, A. 2011. Hedonic Coalition Formation for Distributed Task Allocation among Wireless Agents. IEEE Transactions on Mobile Computing, 10(9): 1327–1344. Sung, S. C.; and Dimitrov, D. 2007. On Myopic Stability Concepts for Hedonic Games. Theory and Decision, 62(1): 31–45. Sung, S. C.; and Dimitrov, D. 2010. Computational Complexity in Additive Hedonic Games. European Journal of Operational Research, 203(3): 635–639. Woeginger, G. J. 2013. A hardness result for core stability in additive hedonic games. Mathematical Social Sciences, 65(2): 101–104. Zech, V.; and Bullinger, M. 2025. Deviation Dynamics in Cardinal Hedonic Games. Technical report, https://arxiv.org/abs/2511.11531

17318
