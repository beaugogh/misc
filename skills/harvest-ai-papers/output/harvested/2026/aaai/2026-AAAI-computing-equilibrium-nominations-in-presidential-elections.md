---
title: "Computing Equilibrium Nominations in Presidential Elections"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38732
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38732/42694
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Computing Equilibrium Nominations in Presidential Elections

<!-- Page 1 -->

Computing Equilibrium Nominations in Presidential Elections

Piotr Faliszewski1, Stanisław Ka´zmierowski1,2, Grzegorz Lisowski3,

Ildik´o Schlotter4,5, Paolo Turrini6

1AGH University of Krak´ow, Poland 2University of Warsaw, Poland 3University of Groningen, The Netherlands 4ELTE Centre for Economic and Regional Studies, Hungary 5Budapest University of Technology and Economics, Hungary 6University of Warwick, United Kingdom faliszew@agh.edu.pls, s.kazmierowski@uw.edu.pl, g.a.lisowski@rug.nl, schlotter.ildiko@krtk.elte.hu, p.turrini@warwick.ac.uk

## Abstract

We study strategic candidate nomination by parties in elections decided by Plurality voting. Each party selects a nominee before the election, and the winner is chosen from the nominated candidates based on the voters’ preferences. We introduce a new restriction on these preferences, which we call party-aligned single-peakedness: all voters agree on a common ordering of the parties along an ideological axis, but may differ in their perceptions of the positions of individual candidates within each party. The preferences of each voter are single-peaked with respect to their own axis over the candidates, which is consistent with the global ordering of the parties. We present a polynomial-time algorithm for recognizing whether a preference profile satisfies party-aligned single-peakedness. In this domain, we give polynomial-time algorithms for deciding whether a given party can become the winner under some (or all) nominations, and whether this can occur in some pure Nash equilibrium. We also prove a tight result about the guaranteed existence of pure strategy Nash equilibria for elections with up to three parties for singlepeaked and party-aligned single-peaked preference profiles.

## Introduction

Let us consider a certain computer science department that needs to select its new head. The department has three research groups, one focused on artificial intelligence, one working on theoretical computer science, and one devoted to distributed systems. In the past, each group had just one candidate, and the person who got the most votes was selected as the head, for a four-year term. However, this time more people expressed their interest in the position; the groups— worried by the possibility of splitting the vote—decided that each of them will nominate only a single one. Yet, how should they decide on whom to choose?

Faliszewski et al. (2016) studied this problem by looking for a necessary winner, i.e., a candidate who wins irrespective of the nominations by the other groups, or by looking for a possible winner, i.e., a candidate who wins, provided the other groups’ nominations are favourable (formally, they

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

referred to such candidates as necessary and possible president, as they followed a naming scheme from politics). Yet, asking for a necessary winner is too demanding—such a candidate may fail to exist—and choosing a possible winner is too optimistic—there is no reason for the other groups to cooperate. Hence, we are looking for a game-theoretic solution: we model the scenario as a game, where each group is a player, each possible nominee is a strategy, and we are looking for a pure strategy Nash equilibrium (a group’s utility is 1 if its nominee wins and it is 0 otherwise), focusing on the classic Plurality rule (whoever gets the most votes wins). We are interested in two types of results: we analyse when equilibria are guaranteed to exist and, if that is not the case, what is the complexity of deciding their existence. Henceforth, we follow the politics-based naming convention of Faliszewski et al. (2016): we speak of parties that nominate candidates, and we refer to the candidates who win under a given pure strategy Nash equilibrium as equilibrium presidents.

Our Contribution. We find that the guarantees for equilibria existence, as well as the complexity of recognising equilibria, are very fragile and strongly depend on the nature of the voters’ preferences. In particular, we distinguish three types of preference profiles that the voters may have. First, we analyse 1D-Euclidean preferences (Enelow and Hinich 1984, 1990), where each candidate and each voter is a point on the line, and the voters rank the candidates in the order of their distance from their points. Second, we consider the classic single-peaked setting (Black 1958), where there is a commonly agreed order (or axis) of the candidates—such as the political left-to-right spectrum—and every prefix of every vote forms an interval within this axis. Finally, we introduce the notion of party-aligned single-peakedness.

In party-aligned single-peaked preferences, parties are ordered along a given axis, but each voter has their perceived axis, obtained from the party axis by replacing each party with its members, in whatever order the voter prefers. In other words, all voters agree on the positioning of the parties along the party axis, but they may disagree on the precise positioning of the parties’ candidates. Such differences may stem, for example, from differing beliefs about some better known or local candidate, whom a voter perceives as more

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16871

<!-- Page 2 -->

(or less) aligned with their ideals than other candidates from the same party. For example, consider parties A = {a1,a2} and B = {b} and the next three votes:

v1 ∶a2 ≻b ≻a1; v2 ∶a1 ≻b ≻a2; v3 ∶a1 ≻a2 ≻b based on their following perceived axes:

v1,v3 ∶a1 ◁a2 ◁b; v2 ∶a2 ◁a1 ◁b.

These preferences are not single-peaked—as they rank three different candidates in the last position, which is impossible in single-peaked elections—but they are party-aligned single-peaked. The mismatch in voters’ perception can give rise to non-trivial strategic decisions from the parties’ side. While party B can only nominate b, party A has to make a choice between a1 and a2. If party A nominates a2, voter v2 perceives party B as preferable to party A. By contrast, this is not the case for v1, who prefers a2 to b. However, should party A nominate a1 instead, they would end up gaining the vote of v2 but losing that of v1 to party B. Essentially, under party-aligned single-peakedness, a move to steal voters from one party can lead to losing some other ones.

Proofs of statements marked with the ⋆symbol are deferred to the full version of our paper (Faliszewski et al. 2025). Remark 1. Though neither 1D-Euclidean nor single-peaked preferences need to put members of a given party on consecutive positions on the common axis (or line), all voters have to follow the same one. By contrast, party-aligned singlepeaked preferences require members of each party to take consecutive positions on each axis, but voters can freely order specific party members along their individual axes. ⌟ We establish the following results: 1. Pure strategy Nash equilibria always exist, provided there are at most three parties and the preferences are both single-peaked and party-aligned single-peaked, but may fail to exist for four parties (even with at most two members in each); for 1D-Euclidean elections, equilibria may fail to exist even for two parties of size at most two. 2. Whether a pure strategy Nash equilibrium exists in a party-aligned single-peaked election can be decided in polynomial time, but the problem is NP-hard in 1D- Euclidean elections (and, hence, under single-peaked ones). Deciding if a given party can win in some pure strategy Nash equilibrium, or if it can win under some or all nominations from other parties, is also polynomialtime solvable in party-aligned single-peaked elections. Remark 2. We focus on pure strategy Nash equilibria, which we will refer to simply as Nash equilibria. While allowing for randomisation is an important aspect of strategic decisions, we believe “pure” candidate selections are natural and often occurring events in the decision-making process of parties, e.g., through the use of primaries (Borodin et al. 2024). Besides related models of strategic nominations (Harrenstein et al. 2021; Sabato et al. 2017), the focus on pure strategy Nash equilibria is also widely established in other areas of computer science, such as the logical analysis of strategic reasoning in games, including, e.g., Boolean games (˚Agotnes et al. 2013; Gutierrez et al. 2021). ⌟

Related Literature. The line of research on party-based election models, as introduced by Faliszewski et al. (2016), has been expanded by taking into account different voting rules and investigating the related problems also from the parameterised complexity viewpoint by Misra (2019), Cechl´arov´a et al. (2023), Schlotter, Cechl´arov´a, and Trellov´a (2024), and Schlotter and Cechl´arov´a (2025). In a related vein, Pierczynski and Szufa (2024) analysed a family of rules where nominations are not needed.

Finding a Nash equilibrium was also studied in a similar model describing strategic nominations over different territories by Harrenstein and Turrini (2022). Equilibrium existence and computation for nominee selection problems was further studied in the context of the Hotelling-Downs framework where both voters and candidates are located on a line, which induces a natural preference ordering of candidates (Harrenstein et al. 2021; Deligkas, Eiben, and Goldsmith 2022). In a related paper, Sabato et al. restricts candidates’ and voters’ positioning to intervals, which has strong implications on equilibrium existence. Decision-making models in which strategic nomination has been studied include tournaments played by coalitions of players (Lisowski, Ramanujan, and Turrini 2022; Lisowski 2022).

Another important related line of research is strategic candidacy; see (Brill and Conitzer 2015; Dutta, Jackson, and Le Breton 2001; Eraslan and McLennan 2004). There, candidates have preferences over their opponents and may decide not to participate in an election to achieve a more favoured outcome. Such strategic behaviour may arise, e.g., due to certain costs incurred by participation (Obraztsova et al. 2015; Elkind et al. 2015). Finally, we mention that our research is directly related to the study of nominee selection in primaries; see, e.g., the work of Borodin et al. (2019).

Structured domains are surveyed in depth by Elkind, Lackner, and Peters (2022). A variant of single-peakedness closely related to ours is the domain due to Cornaz, Galand, and Spanjaard (2012, 2013) where each voter has to rank members of each party consecutively; note that this is not required for party-aligned single-peakedness.

## Preliminaries

Strategic Nominee Selection

For an integer k ⩾0 let [k] = {1,...,k} with [0] = ∅.

Consider a set C of candidates and a set P = {P1,...,Pk} of parties where P is a partitioning of the candidate set C. Let V = {v1,...,vn} be a set of voters, where each voter v has a strict preference order ≻v over the candidate set C; we call the collection (≻v)v∈V preference profile of the voters.

Our framework consists of two phases: a nomination phase, where each party selects its candidate, and an election phase, where voters choose among the nominated candidates based on their preferences. Thus, a nomination scheme is a tuple (c1,...,ck) where ci ∈Pi for all i ∈[k]. Given a nomination scheme (c1,...,ck), the reduced election takes place over the set C′ = {c1,...,ck} of nominees. We use the Plurality voting rule where each voter votes for their favourite candidate among C′, and the candidates with the highest number of votes obtained—their score—are the win-

16872

<!-- Page 3 -->

ners; the party whose nominee is a winner is also called a winner. Some candidate or party is a winner in some nomination scheme (c1,...,ck) if it is a winner in the reduced election over {c1,...,ck}.

We say that a candidate c′ i ∈Pi is a Nash deviation by party Pi for some nomination scheme (c1,...,ck) if c′ i ∈ Pi ∖{ci}, and ci is not a winner in the election resulting from (c1,...,ck) but c′ i is a winner in the election resulting from (c1,...,c′ i,...,ck). A nomination scheme is a (pure) Nash equilibrium if it admits no Nash deviation.

Structured Preferences Let us now introduce two types of restrictions on voters’ preference profiles that may arise in elections where there is a single ideological line which strongly determines voters’ behaviour such as, e.g., the left-to-right axis in politics.

Single-Peaked Profiles. We say that a preference profile (≻v)v∈V is single-peaked if there exists a total order ◁over the set C of candidates called an axis such that the preferences of each voter v are single-peaked with respect to the axis ◁, meaning that for every three candidates a,b,c ∈C with a ◁b ◁c the relation a ≻v b implies b ≻v c. Roughly speaking, this means that candidates can be placed along a line such that each voter v’ preferences are derived from the candidates’ distances to v’s “ideal point” on the line.

1-D Euclidean Profiles. A special case of single-peaked profiles appears in 1-D Euclidean elections where voters and candidates are located on the real line, and voters’ preferences over candidates stem from their distances.

Definition 1. We say that an election E = (C,V) is 1-D Euclidean if there is a mapping f ∶C ∪V →R, such that for every voter v in V and every pair ci,cj in C, ci ≻v cj if and only if ∣f(v) −f(ci)∣< ∣f(v) −f(cj)∣.

Although 1-D Euclidean elections allow for voters to be indifferent between candidates that are equally close to them, we will ensure that the 1-D Euclidean elections used in this paper induce strict preferences.

Party-Aligned Single-Peakedness We assume that parties can be ordered along a global axis recognised by all voters, with candidates belonging to the same party placed contiguously. However, candidates within a party may be perceived differently by voters, who therefore may disagree on where different candidates within a given party are located along the axis. Formally, we say that a preference profile is party-aligned single-peaked if there exists a party axis ◁P, i.e., a total order over the set P of parties such that, for every voter v ∈V, there exists a perceived axis ◁v over the candidate set C for which

• v’s preference order ≻v is single-peaked w.r.t. ◁v, and • ◁v is compatible with ◁P, meaning that for each two candidates ci and cj belonging to different parties Pi and Pj, respectively, ci ◁v cj implies Pi ◁P Pj.

Example 1. Consider a set P = {Pa,Pb,Pc,Pd} of parties with Pa = {a}, Pb = {b1,b2}, Pc = {c1,c2}, and Pd = {d}, and three voters whose preferences are:

v ∶c2 ≻b1 ≻c1 ≻d ≻b2 ≻a; w ∶b1 ≻c1 ≻b2 ≻c2 ≻a ≻d;

z ∶b2 ≻c2 ≻c1 ≻d ≻b1 ≻a. The voters’ preferences are party-aligned single-peaked with party axis Pa ◁P Pb ◁P Pc ◁P Pd and perceived axes:

a ◁v b2 ◁v b1 ◁v c2 ◁v c1 ◁v d; a ◁w b2 ◁w b1◁w c1 ◁w c2 ◁w d; a ◁z b1 ◁z b2 ◁z c2 ◁z c1 ◁z d. ⌟

Recognising Party-Aligned Single-Peaked Profiles. We present a polynomial-time algorithm for recognising preference profiles that are party-aligned single-peaked. Formally, we deal with the following computational problem.

RECOGNISING PARTY-ALIGNED SINGLE-PEAKEDNESS Input: A set C of candidates partitioned into a set P of parties, and a set V of voters with preference profile (≻v)v∈V over the candidate set C. Question: Is the preference profile (≻v)v∈V partyaligned single-peaked?

The rest of this section proves the following result. Theorem 1. RECOGNIZING PARTY-ALIGNED SINGLE- PEAKEDNESS can be solved, and a suitable party axis—if existent—can be computed, in O(∣C∣⋅∣V ∣⋅∣P∣) time.

Verification of Party-Aligned Single-Peakedness Under Fixed Party Ordering. First, we formulate the necessary and sufficient conditions for a single-vote profile to be partyaligned single-peaked under a fixed ordering of parties. Lemma 1 (⋆). Consider a vote ≻v over the candidate set of parties P1,...,Pm. For each party Pi, let hi and li denote v’s most- and least-preferred candidate within Pi. Let Pj be the party containing v’s top candidate. Then ≻v is partyaligned single-peaked with party axis P1 ◁P ⋅⋅⋅◁P Pm if and only if the following conditions are met. (a) If Pj ∉{P1,Pm}, then lj ≻v hj−1 or lj ≻v hj+1. (b) For each parties Pi,Pi+1 with i > j we have li ≻v hi+1.

(c) For each parties Pi−1,Pi with i < j we have li ≻v hi−1.

Notice that whenever there are at most two parties, then conditions (1)–(3) of Lemma 1 are automatically true for any fixed party axis. Thus, we have the following consequence. Corollary 1. Every preference profile with at most two parties is party-aligned single-peaked.

Placing the Bottom Candidates. Following an idea by Escoffier, Lang, and ¨Ozt¨urk (2008), we present a lemma about the placement of a party that contains the lowestranked candidate in some vote. Lemma 2 (⋆). Let c ∈Pi be the candidate ranked in the last position by a voter v. If ≻v is party-aligned single-peaked with party axis ◁P, then Pi is either in the leftmost or the rightmost position in ◁P.

As a consequence of Lemma 2, in any party-aligned single-peaked consistent profile, at most two parties may have candidates that are ranked last by at least one voter.

16873

<!-- Page 4 -->

Vote-Imposed Restrictions. We move on to present some conditions that allow us to extend a partially determined party axis based on the given preference profile.

Suppose that we already know the position of certain parties in the party axis ◁P to be constructed. In particular, assume that we have an extremal party placement (L,R) for ◁P which consists of two sets of parties L,R ⊆P such that L contains the ∣L∣leftmost parties and R contains the ∣R∣rightmost parties according to ◁P.

Lemma 3 (⋆). Let (L,R) be an extremal party placement for some party axis ◁P, and consider a vote ≻v that is partyaligned single-peaked with axis ◁P. Assume that candidates in ⋃(R ∪L) do not form the suffix of the vote ≻v. Let

• a be v’s least favourite candidate in ⋃(P ∖(L ∪R)), • b be v’s most favourite candidate in ⋃(L ∪R), and • Pa and Pb be the parties containing a and b, respectively.

If Pb ∈R, then Pa directly follows the last party in L according to ◁P, while if Pb ∈L, then Pa directly precedes the first party in R according to ◁P.

Reducing the Problem. When Lemma 3 can no longer be applied, we use recursion based on the following lemma.

Lemma 4 (⋆). Let Π = (≻v)v∈V be a party-aligned singlepeaked preference profile over candidate set C with a party axis P1 ◁P ⋅⋅⋅◁P Pm. Assume further that the candidates in (P1 ∪⋅⋅⋅∪Pi) ∪(Pj ∪⋅⋅⋅∪Pm) form a suffix of each vote in Π, and let Q be the set of candidates not in this suffix. If the restriction of Π to Q is partyaligned single-peaked with a party axis Q1 ◁Q ⋅⋅⋅◁Q Qk, then Π is party-aligned single-peaked with the party axis P1,...,Pi,Q1,...,Qk,Pj,...,Pm.

Algorithm. Armed with the aforementioned results, we present the recognition algorithm proving Theorem 1.

Placing Bottom Parties. Given a preference profile Π, we begin by identifying the set B ⊆P of bottom parties, i.e., those containing a candidate appearing at the last position in some vote. Lemma 2 shows that all parties in B must appear at either the left- or the rightmost position of the hypothetical party axis ◁P. In particular, if ∣B∣> 2, then the profile is not party-aligned single-peaked, and we reject. If ∣B∣⩽2, then the exact placement of the parties in B is not important, because for every party axis witnessing the partyaligned single-peakedness of our profile, the reversed party axis does the same. Hence, we place the parties in B as the left- and (if ∣B∣= 2) rightmost parties in ◁P, creating an extremal party placement (L,R) for ◁P with L ∪R = B ≠∅.

Vote-Imposed Restrictions. Next, we iterate over the set of voters to check whether they impose some restriction on ◁P. More precisely, we apply Lemma 3 as long as possible, extending our extremal party placement (L,R)— together with the ordering of the parties in L ∪R according to ◁P—by fixing the placement of an additional party in the fashion determined by Lemma 3 in each step.

Reducing the Problem. If at some point there is no voter for which Lemma 3 can be applied, then the set of candidates contained in our current extremal party placement (L,R) forms a suffix in each vote. Hence, in line with Lemma 4, we delete all parties in L∪R together with all of their candidates from the profile Π, and find a suitable party axis for the resulting profile Π′ (containing at least one party less than Π) in a recursive manner. Note that if Π is party-aligned singlepeaked, then so is Π′, and a party axis witnessing the latter can be turned into a party axis for Π using Lemma 4 and the ordering of the parties contained in the extremal party placement (L,R) determined so far.

Checking the Resulting Profile. After obtaining a party axis ◁P, we check if profile Π is party-aligned singlepeaked under ◁P by checking the conditions in Lemma 1. If Π is not party-aligned single-peaked under ◁P, then Lemmas 2–4 guarantee that Π is not party-aligned single-peaked.

Running Time. The algorithm runs in O(∣C∣⋅∣V ∣⋅∣P∣) time; see the full version (Faliszewski et al. 2025).

## Equilibrium Existence

We move on to present the results concerning the existence of Nash equilibria in the considered model. Theorem 2. If voters’ preference profiles are single-peaked and also party-aligned single-peaked with at most three parties, then a Nash equilibrium always exists.

Proof. Let (≻v)v∈V be a preference profile that is both single-peaked and party-aligned single-peaked, i.e., each vote is single-peaked with respect to the same axis ◁that is compatible with some party axis. We call a nomination scheme⃗c centrist if the leftmost party PL nominates its rightmost candidate, and the rightmost party PR nominates its leftmost candidate in⃗c. If a voter v does not vote for PL in a centrist nomination scheme⃗c, then its favourite candidate is to the right of every candidate of PL, and hence there is no Nash deviation for⃗c by PL due to the single-peakedness of ≻v w.r.t. ◁. A symmetric argument shows that⃗c admits no Nash deviation by PR either.

We now distinguish between two cases. If there is a candidate c ∉PL∪PR that is a winner in some centrist nomination scheme⃗c, then neither the party containing c, nor any of the parties PL and PR has a Nash deviation for⃗c which is thus a Nash equilibrium. By contrast, if in all centrist nomination schemes, no party other than PL and PR wins, then any such nomination scheme is a Nash equilibrium, since no party has a Nash deviation.

Non-Existence of Nash Equilibria. Let us show an example proving the tightness of Theorem 2 in the sense that party-aligned single-peakedness alone does not guarantee a Nash equilibrium, even if the number of parties is only two. Theorem 3. There is an election E = (C,V) containing two size-two parties and three voters with a party-aligned singlepeaked preference profile that admits no Nash equilibria.

Proof. Consider the election E = (C,V) with two parties A = {a1,a2} and B = {b1,b2} and voters V = {v1,v2,v3} whose preferences are v1 ∶a1 ≻b1 ≻a2 ≻b2; v2 ∶b1 ≻a2 ≻b2 ≻a1; v3 ∶a2 ≻b2 ≻a1 ≻b1.

16874

<!-- Page 5 -->

a1 a2 b1 b2 v1,v3 v2 v3 v1,v2 v1 v2,v3 v1, v2,v3

– a1 a2 b1 b2

1 0

0 1

0 1

1 0

**Figure 1.** Illustration for Theorem 3. The left figure shows the voters supporting candidates of A and B in all nomination schemes. On the right, the corresponding winners and non-winners are indicated by “1” and “0”, respectively.

0 p3

• • 2 p1

5 voters

3

2 voters p′

1

•

6 voters

7 p2

• 8.9

2 voters

11 p′

2

•

7 voters

12 p4

•

**Figure 2.** Location of voters and candidates on the real line in the election constructed in Theorem 4. In all figures, voters are indicated by arrows, and candidates by black circles.

By Corollary 1, this profile is party-aligned single-peaked. To see that there is no Nash equilibrium, it suffices to consider each possible nomination scheme and the number of voters supporting the two parties in each of them, as depicted by Figure 1. It is easy to see that each of the four possible nomination schemes admits a Nash deviation.

We proceed to show the tightness of Theorem 2 in terms of the number of parties.

Theorem 4. There exists a 1-D Euclidean election E with four parties and maximum party size 2 with both singlepeaked and party-aligned single-peaked preference profiles that does not admit any Nash equilibria.

Proof. Let us construct an instance with four parties that is both single-peaked and party-aligned single-peaked. We do this by constructing the following 1-D Euclidean election.

Let the distribution function φ of voters assign to each point x on the real line the number φ(x) of voters located at x. We set the distribution function φ of our instance such that φ(2) = 5, φ(3) = 2, φ(5) = 6, φ(8.9) = 2, φ(11) = 7, and φ(x) = 0 for all other points x on the real line. We define the set of parties P = {P1,P2,P3,P4}. Let P1 = {p1,p′

1}, P2 = {p2,p′

2}, P3 = {p3} and P4 = {p4}. The positions of the candidates are as shown in Figure 2.

It is straightforward to verify that all preference profiles in this election are party-aligned single-peaked (note that voters’ preferences can be formulated as strict total orders) and also single-peaked. Furthermore, we observe that parties P3 and P4 nominate the same candidate in each nomination scheme, and that their candidates cannot win in any nomination scheme. Figure 3 shows the number of votes obtained by parties P1 and P2, as well as the winner of the resulting election, depending on the nominated candidates. In each p1 p′

1 p2 p′

2

7 8

8 2

13 9

8 9 p1 p′

1 p2 p′

2

0 1

1 0

1 0

0 1

**Figure 3.** The left figure shows the numbers of voters supporting candidates of P1 and P2 in all possible nomination schemes. On the right, the corresponding winners and nonwinners are indicated by “1” and “0”, respectively.

nomination scheme, either party P1 or party P2 has a Nash deviation, so the instance admits no Nash equilibria.

Finding a Nash Equilibrium Let us now turn our attention to the problem of finding a Nash equilibrium whenever it exists. As we have already shown in Section 4, a Nash equilibrium may not exist even in very restricted domains involving just four parties. Formally, we define the corresponding problem as follows:

EQUILIBRIUM EXISTENCE Input: A set C of candidates partitioned into a set P of parties and a set V of voters with preference profile (≻v)v∈V over the set C. Question: Does (C,P,V,(≻v)v∈V) admit a Nash equi- librium?

It turns out that EQUILIBRIUM EXISTENCE is already NP-hard for single-peaked preference profiles, as we show in Theorem 5. In stark contrast with this, we give a polynomial-time algorithm that not only finds a Nash equilibrium, but also decides if a given party can win in some Nash equilibrium. We solve the following problem.

EQUILIBRIUM PRESIDENT Input: A set C of candidates partitioned into a set P of parties, a distinguished party P ∈P, and a set V of voters with preference profile (≻v)v∈V over the set C. Question: Is there a nomination scheme that is a Nash equilibrium for the instance and where P is a winner in the resulting election?

Theorem 5 (⋆). EQUILIBRIUM EXISTENCE and EQUI- LIBRIUM PRESIDENT are NP-hard for 1-D Euclidean, and hence, for single-peaked preference profiles.

We move on to present our main result: Theorem 6. EQUILIBRIUM EXISTENCE and EQUILIB- RIUM PRESIDENT are polynomial-time solvable if the preference profile is party-aligned single-peaked.

We present a polynomial-time algorithm for EQUILIB- RIUM PRESIDENT. Note that applying this algorithm for each party as the distinguished one results in a polynomialtime algorithm for EQUILIBRIUM EXISTENCE.

16875

<!-- Page 6 -->

Let (C,P,P,V,(≺v)v∈V) be our input instance for the EQUILIBRIUM PRESIDENT problem. Our algorithm uses dynamic programming and relies heavily on the structure of the preference domain.

We start by computing a party axis ◁P with respect to which the input profile (≺v)v∈V is party-aligned singlepeaked; let P1,...,Pk be the parties in P ordered according to ◁P, and let P = Pκ be the distinguished party among whose candidates we are searching for a candidate that can become a winner in some Nash equilibrium.

We first prove the following lemma.

Lemma 5 (⋆). Suppose that the profile (≻v)v∈V is partyaligned single-peaked. Then for each voter v ∈V, there exist at most two parties for which v might vote for in a reduced election. Moreover these two parties must be adjacent along the party axis, and can be found in O(∣C∣) time.

Partitioning the Voter Set. We now introduce the following sets of voters. First, for each i ∈[k], let V Pi denote the set of those voters in V who always vote for the nominee of party Pi irrespective of the nomination scheme. Note that v ∈V Pi if and only if the top ∣Pi∣candidates in v’s preference list are exactly the candidates belonging to Pi.

Second, for each i ∈[k −1], let V (Pi,Pi+1) denote the set of voters in V ∖(V Pi ∪V Pi+1) who always vote either for the nominee of Pi or for the nominee of Pi+1. By Lemma 5, the sets V Pi for i ∈[k] together with the sets V (Pi,Pi+1) for i ∈[k −1] form a partitioning of the voter set V, and this partitioning can be computed in O(∣V ∣⋅∣C∣) time.

Third, let us define the following sets of voters, crucial for our dynamic programming approach:

V⩽i = ( i ⋃ j=1

V Pj) ∪( i−1

⋃ j=1

V (Pj,Pj+1)), and (1)

V⩾i = ( k ⋃ j=i

V Pj) ∪( k−1

⋃ j=i

V (Pj,Pj+1)). (2)

Note that V⩽1 ⊆V⩽2 ⊆⋅⋅⋅⊆V⩽k = V, and observe also that voters in V⩽i may only vote for nominees in P1 ∪⋅⋅⋅∪Pi in any reduced election. Similarly, V = V⩾1 ⊇V⩾2 ⊇⋅⋅⋅⊇V⩾k, and voters in V⩾i may only vote for nominees in Pi ∪⋅⋅⋅∪Pk in any reduced election.

Assuming some hypothetical nomination scheme that is a Nash equilibrium and in which Pκ is a winner, we next guess the score s⋆obtained by the nominee of Pκ in such a Nash equilibrium; note that s⋆⩽∣V ∣, so there are at most ∣V ∣ possible values s⋆can take. Henceforth, we treat s⋆as fixed.

Feasible Partial Nomination Schemes. For some i ∈[k] at most κ, a left-feasible partial nomination scheme for i is a tuple (c1,...,ci) where cj ∈Pj for each j ∈[i], and

(α) for each j ∈[i−1], cj obtains at most s⋆votes in every nomination scheme (c1,...,ci,c′ i+1,...,c′ k),1and (β) for each j ∈[i −1], if cj obtains less than s⋆votes in some nomination scheme (c1,...,ci,c′ i+1,...,c′ k), then no candidate c′ j ∈Pj ∖{cj} obtains at least s⋆ votes in (c1,...,cj−1,c′ j,cj+1,...,ci,c′ i+1,...,c′ k).

Similarly, for each index i ∈[k] at least κ, a right-feasible partial nomination scheme for i is a tuple (c1,...,ci) where cj ∈Pj for each j ∈[i], and moreover,

(α′) for each j ∈[k]∖[i], cj obtains at most s⋆votes in ev- ery nomination scheme (c′

1,...,c′ i−1,ci,...,ck), and (β′) for each j ∈[k] ∖[i], if cj obtains less than s⋆votes in some nomination scheme (c′

1,...,c′ i−1,ci,...,ck), then no candidate c′ j ∈Pj ∖{cj} obtains at least s⋆ votes in (c′

1,...,c′ i−1,ci,...,cj−1,c′ j,cj+1,...,ck).

Viable Scores and Score Pairs. We are now ready to define the central notions necessary for our algorithm. For some i ∈[k] and candidate ci ∈Pi, an integer si is a left- (or right-) viable score for ci if there is a left- (or right-) feasible partial nomination scheme where ci obtains exactly si votes from V⩽i (from V⩾i, respectively).

Next, we define the concept of viability for pairs of integers. Given an index i ∈{2,...,k}, a pair (si−1,si) of integers is left-viable for a pair (ci−1,ci) ∈Pi−1 × Pi of candidates if there is a left-feasible partial nomination scheme where cj obtains exactly sj votes from V⩽i for both j ∈{i −1,i}. Notice that, consequently, some score si is left-viable for candidate ci ∈Pi if and only if there exists some si−1 ∈{0,1,...,s⋆} and candidate ci−1 ∈Pi−1 such that(si−1,si) is a left-viable pair for (ci−1,ci). The symmetric concept of right-viability is defined analogously.

Lemma 6 shows the importance of these notions.

Lemma 6 (⋆). Given a candidate cκ ∈Pκ, the following statements are equivalent:

(a) there exists a nomination scheme that is a Nash equi- librium and in which cκ is a winner with score s⋆; (b) there exist non-negative integers sl and sr satisfying sl + sr −∣V Pκ∣= s⋆such that sl is a left-viable score for cκ and sr is a right-viable score for cκ.

Computing Viable Score Pairs. Let us now provide a dynamic programming method for computing all left-viable score pairs for each candidate pair (ci,ci+1) ∈Pi × Pi+1 increasingly for each i ∈[κ−1]; computing right-viable scores can be done in a symmetric manner. From now on, we may write viability instead of left-viability.

Notice that for a given candidate pair (c1,c2) ∈P1 × P2, the only viable pair can be (s1,s2) where s1 = f(c1∣c2) ∶= ∣V P1∣+ ∣{v ∶v ∈V (P1,P2),c1 ≻v c2}∣, s2 = ∣V P2∣+ ∣{v ∶v ∈V (P1,P2),c2 ≻v c1}∣. (3)

However, such a pair (s1,s2) is not necessarily viable for (c1,c2), because it might not lead to a Nash equilibrium.

Lemma 7 (⋆). The pair (s1,s2) defined as in (3) is viable for a candidate pair (c1,c2) ∈P1 × P2 if and only if (†) s1 = s⋆, or (‡) s1 < s⋆and there is no c′

1 ∈P1 for which f(c′ 1∣c2) ⩾s⋆.

Now, we take the general case where 2 < i ⩽k and aim to compute the viable score pairs for the pairs in Pi−1 × Pi.

1Note that the nominees c′ i+1,..., c′ k are irrelevant here as they do not affect how voters in V⩽i vote.

16876

<!-- Page 7 -->

Lemma 8 (⋆). A pair (si−1,si) of non-negative integers with si−1 ⩽s⋆is viable for (ci−1,ci) ∈Pi−1×Pi if and only if there exist integers s′ i−1,si−2 ∈{0,1,...,s⋆} and candidate ci−2 ∈Pi−2 such that

(i) (si−2,s′ i−1) is a viable pair for (ci−2,ci−1), (ii) si−1 = s′ i−1 + ∣{v ∶v ∈V (Pi−1,Pi),ci−1 ≻v ci}∣, (iii) si = ∣{v ∶v ∈V (Pi−1,Pi),ci ≻v ci−1}∣+ ∣V Pi∣, and

(iv) either (†) si−1 = s⋆, or (‡) there is no c′ i−1 ∈Pi−1 for which f(c′ i−1∣ci,ci−2) ⩾s⋆where f(c′ i−1∣ci,ci−2) = ∣{v ∶v ∈V (Pi−1,Pi),c′ i−1 ≻v ci}∣

+ ∣V Pi−1∣+ {v ∶v ∈V (Pi−2,Pi−1),c′ i−1 ≻v ci−2}∣.

Using dynamic programming based on Lemmas 7 and 8, we can compute all left-viable score pairs for each candidate pair (ci−1,ci) ∈Pi−1 × Pi increasingly for each i = 2,...,κ; note that it suffices to compute score pairs (si−1,si) where si−1 and si are between 0 and s⋆. Hence, we need to compute a binary variable for each si−1,si ∈{0,...,s⋆} and each ci−1 ∈Pi−1 and ci ∈Pi, for i = 2,...,κ, describing whether (si−1,si) is viable for (ci−1,ci) or not; we can determine these values for i = 2 using Lemma 7, and we can compute them for increasing values of i using Lemma 8.

This allows us to compute all left–viable scores for each candidate in Pκ. Computing right-viable scores can be done in a symmetric manner. Finally, we Lemma 6 to either find a candidate cκ ∈Pκ that wins in some Nash equilibrium with score s⋆or conclude correctly that no such candidate exists.

Running Time. Computing the party axis can be done in polynomial time, according to Theorem 1. Guessing the winning score s⋆of the distinguished party Pκ adds a factor of ∣V ∣to the running time necessary for computing the viable scores. Checking the conditions of Lemmas 7 and 8 can clearly be done in polynomial; hence, the running time of our algorithm is polynomial in the input size. This finishes the proof of Theorem 6.

## 6 Finding a Possible or Necessary President

Next, we show that the following problems are polynomialtime solvable in the domain of party-aligned single-peaked profiles, by an adaptation of our algorithm for Theorem 6:

POSSIBLE (or NECESSARY) PRESIDENT Input: A set C of candidates partitioned into a set P of parties, a distinguished party P ∈P, and a set V of voters with preference profile (≻v)v∈V over the set C. Question: Is P a winner in the election resulting from some (or all, respectively) nomination scheme(s)?

Faliszewski et al. (2016) proved that POSSIBLE PRESI- DENT is NP-complete for single-peaked preferences, while NECESSARY PRESIDENT is coNP-complete in general but becomes polynomial-time solvable for single-peaked preferences. They also showed that POSSIBLE PRESIDENT is polynomial-time solvable if the preferences are singlepeaked with respect to an axis along which the candidates of each party are ordered consecutively, that is, if preferences are single-peaked and also party-aligned single-peaked.

EQUI PRES POS PRES NEC PRES

SP & PASP P [Thm. 6] P [Thm. 7] P [F’16]

PASP P [Thm. 6] P [Thm. 7] P [Thm. 7]

SP NP-c [Thm. 5] NP-c [F’16] P [F’16]

**Table 1.** Summary of our algorithmic results. SP (and PASP) stands for single-peaked (party-aligned single-peaked) preferences. [F’16] marks results by Faliszewski et al. (2016).

The following theorem extends the tractability results of Faliszewski et al. (2016) to the domain of party-aligned single-peaked preference profiles.

Theorem 7 (⋆). The POSSIBLE and NECESSARY PRESI- DENT problems are polynomial-time solvable if the preference profile is party-aligned single-peaked.

Proof sketch. The algorithm for EQUILIBRIUM PRESIDENT presented in Section 5 can be adapted in a straightforward way to solve the POSSIBLE PRESIDENT problem; in fact, this is a simplification, since we only need to ensure that the distinguished party is a winner in some nomination scheme⃗c, but we do not require⃗c to be a Nash equilibrium.

To solve the NECESSARY PRESIDENT problem, we apply a slightly modified variant of our algorithm for POSSI- BLE PRESIDENT that not only ensures that the distinguished party P + is a winner in some nomination scheme, but also guarantees that some other party P −is not a winner; running this algorithm for each party P + other than P −, we can decide if P −wins in all reduced elections.

## Discussion

We have explored computational questions about strategic candidate nomination by parties in a model where voters’ preferences are party-aligned single-peaked, with a focus on the concept of Nash equilibria; see Table 1 for an overview of our algorithmic results. Studying different restrictions on the preference domain or voting rules other than Plurality are a natural direction for further research in the same model. More generally, extensions of our model that deal with possible interactions between the parties also seem interesting. For example, one could consider what a group of parties can achieve if they were to coordinate their nominations, with a coalition C ⊆P being powerful if there exists a tuple TC = (ci)Pi∈C of candidates such that for every nomination scheme extending TC, the Plurality winner is in TC. This definition generalizes the notion of a necessary president (i.e., a powerful singleton coalition), and we would like to know under what conditions we can determine it. Similar generalisations can be attempted for possible president, as well as a possible or necessary president in an equilibrium.

Understanding strategic nominations in district-based elections is another interesting direction, where the preference structure could improve equilibrium computation results. Finally, extensive interaction is worth exploring, where parties hold primaries at different times, with more nuanced (e.g., subgame-perfect) equilibria.

16877

<!-- Page 8 -->

## Acknowledgments

This work is supported by the European Union (ERC, PRAGMA, 101002854). Views and opinions expressed are however those of the author only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them. Grzegorz Lisowski acknowledges support by the European Union under the Horizon Europe project Perycles (Participatory Democracy that Scales). Ildik´o Schlotter was supported by the Hungarian Academy of Sciences under its Momentum Programme (LP2021-2) and its J´anos Bolyai Research Scholarship. Paolo Turrini acknowledges the support of the Leverhulme Trust for the Research Project Grant RPG-2023-050.

## References

˚Agotnes, T.; Harrenstein, P.; van der Hoek, W.; and Wooldridge, M. J. 2013. Verifiable Equilibria in Boolean Games. In Rossi, F., ed., IJCAI 2013, Proceedings of the 23rd International Joint Conference on Artificial Intelligence, Beijing, China, August 3-9, 2013, 689–695. IJ- CAI/AAAI. Black, D. 1958. The Theory of Committees and Elections. Cambridge University Press. Borodin, A.; Lev, O.; Shah, N.; and Strangway, T. 2019. Primarily about Primaries. In Proceedings of the 33rd AAAI Conference on Artificial Intelligence (AAAI), 1804–1811. Borodin, A.; Lev, O.; Shah, N.; and Strangway, T. 2024. Primarily about primaries. Artificial Intelligence, 104095. Brill, M.; and Conitzer, V. 2015. Strategic voting and strategic candidacy. In Proceedings of the 29th AAAI Conference on Artificial Intelligence (AAAI 2015), 819–826. Cechl´arov´a, K.; Lesca, J.; Trellov´a, D.; Hanˇcov´a, M.; and Hanˇc, J. 2023. Hardness of candidate nomination. Autonomous Agents and Multi-Agent Systems, 37: 37. Cornaz, D.; Galand, L.; and Spanjaard, O. 2012. Bounded Single-Peaked Width and Proportional Representation. In Proceedings of the 20th European Conference on Artificial Intelligence, 270–275. Cornaz, D.; Galand, L.; and Spanjaard, O. 2013. Kemeny Elections with Bounded Single-Peaked or Single-Crossing Width. In Proceedings of the 23rd International Joint Conference on Artificial Intelligence (IJCAI 2013), 76–82.

Deligkas, A.; Eiben, E.; and Goldsmith, T.-L. 2022. Parameterized Complexity of Hotelling-Downs with Party Nominees. In Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI 2022), 244–250. Dutta, B.; Jackson, M. O.; and Le Breton, M. 2001. Strategic candidacy and voting procedures. Econometrica, 69(4): 1013–1037. Elkind, E.; Lackner, M.; and Peters, D. 2022. Preference Restrictions in Computational Social Choice: A Survey. Technical Report arXiv.2205.09092 [cs.GT], arXiv.org. Elkind, E.; Markakis, E.; Obraztsova, S.; and Skowron, P. 2015. Equilibria of plurality voting: Lazy and truth-biased voters. In Proceedings of the 8th International Symposium on Algorithmic Game Theory (SAGT 2015), LNCS 9347, 110–122. Springer. Enelow, J.; and Hinich, M. 1984. The Spatial Theory of Voting: An Introduction. Cambridge University Press. Enelow, J.; and Hinich, M. 1990. Advances in the Spatial Theory of Voting. Cambridge University Press. Eraslan, H.; and McLennan, A. 2004. Strategic candidacy for multivalued voting procedures. Journal of Economic Theory, 117(1): 29–54. Escoffier, B.; Lang, J.; and ¨Ozt¨urk, M. 2008. Single-peaked consistency and its complexity. In Proceedings of the 18th European Conference on Artificial Intelligence (ECAI 2008), 366–370. IOS Press. Faliszewski, P.; Gourv`es, L.; Lang, J.; Lesca, J.; and Monnot, J. 2016. How hard is it for a party to nominate an election winner? In Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI 2016), 257–263. AAAI Press. Faliszewski, P.; Ka´zmierowski, S.; Lisowski, G.; Schlotter, I.; and Turrini, P. 2025. Computing Equilibrium Nominations in Presidential Elections. Technical Report arXiv.2511.11365 [cs.GT], arXiv.org. Gutierrez, J.; Harrenstein, P.; Perelli, G.; and Wooldridge, M. J. 2021. Expressiveness and Nash Equilibrium in Iterated Boolean Games. ACM Trans. Comput. Log., 22(2): 8:1–8:38. Harrenstein, P.; Lisowski, G.; Sridharan, R.; and Turrini, P. 2021. A Hotelling-Downs Framework for Party Nominees. In Proceedings of the 20th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2021), 593–601. IFAAMAS. Harrenstein, P.; and Turrini, P. 2022. Computing Nash Equilibria for District-based Nominations. In Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems, (AAMAS 2022), 588–596. IFAAMAS. Lisowski, G. 2022. Strategic nominee selection in tournament solutions. In Proceedings of the 19th European Conference on Multi-Agent Systems (EUMAS 2022), LNCS 13442, 239–256. Springer. Lisowski, G.; Ramanujan, M. S.; and Turrini, P. 2022. Equilibrium Computation For Knockout Tournaments Played By Groups. In Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems (AA- MAS 2022), 807–815. IFAAMAS.

16878

![Figure extracted from page 8](2026-AAAI-computing-equilibrium-nominations-in-presidential-elections/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-AAAI-computing-equilibrium-nominations-in-presidential-elections/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Misra, N. 2019. On the parameterized complexity of party nominations. In Proceedings of the 6th International Conference on Algorithmic Decision Theory (ADT 2019), 112– 125. Springer. Obraztsova, S.; Elkind, E.; Polukarov, M.; and Rabinovich, Z. 2015. Strategic candidacy games with lazy candidates. In Proceedings of the 24th International Joint Conference on Artificial Intelligence, (IJCAI 2015), 610–616. Pierczynski, G.; and Szufa, S. 2024. Single-Winner Voting with Alliances: Avoiding the Spoiler Effect. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2024), 1567–1575. Sabato, I.; Obraztsova, S.; Rabinovich, Z.; and Rosenschein, J. S. 2017. Real candidacy games: A new model for strategic candidacy. In Proceedings of the 16th Conference on Autonomous Agents and MultiAgent Systems, (AAMAS 2017), 867–875. IFAAMAS. Schlotter, I.; and Cechl´arov´a, K. 2025. Candidate nomination for Condorcet-consistent voting rules. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2025), 1858–1866. IFAA- MAS. Schlotter, I.; Cechl´arov´a, K.; and Trellov´a, D. 2024. Parameterized complexity of candidate nomination for elections based on positional scoring rules. Autonomous Agents and Multi-Agent Systems, 38: 28.

16879
