---
title: "Multi-District School Choice: Playing on Several Fields"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38745
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38745/42707
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Multi-District School Choice: Playing on Several Fields

<!-- Page 1 -->

Multi-District School Choice: Playing on Several Fields*

Yannai A. Gonczarowski1, Michael Yin2, Shirley Zhang3

1Department of Economics and Department of Computer Science, Harvard University 2Paris School of Economics 3Department of Computer Science, Harvard University yannai@gonch.name, michaelyin2018@gmail.com, szhang2@g.harvard.edu

## Abstract

We extend the seminal model of Pathak and S¨onmez (2008) to a setting with multiple school districts, each running its own separate centralized match, and focus on the case of two districts. In our setting, in addition to each student being either sincere or sophisticated, she is also either constrained—able to apply only to schools within her own district of residence— or unconstrained—able to choose any single district within which to apply. We show that several key results from Pathak and S¨onmez (2008) qualitatively ﬂip: A sophisticated student may prefer for a sincere student to become sophisticated, and a sophisticated student may prefer for her own district to use Deferred Acceptance over the Boston Mechanism, irrespective of the mechanism used by the other district. We furthermore show that an unconstrained student may prefer for a constrained student to become unconstrained, regardless of the mechanisms used. Many of these phenomena appear abundantly in large random markets.

## Introduction

The Boston Mechanism (henceforth, BM; also sometimes referred to as the “Immediate Acceptance” mechanism) is a widely used school-choice mechanism, especially in schoolchoice systems that were not (re)designed by economists or computer scientists. This mechanism ﬁrst maximizes the number of applicants who get their ﬁrst-choice school (breaking ties based on the priorities that students have at the different schools, i.e., based on the schools’ “preferences”); then, subject to that, maximizes the number of applicants who get their second-choice school; then, subject to that, maximizes the number of applicants who get their third-choice school; and so forth. Despite being a very natural mechanism, BM suffers from various unattractive qualities, such as not being strategyproof and resulting in unstable matchings. Due to these and other shortcomings, there has been a push since the turn of the millennium (e.g., Abdulkadiro˘glu, Pathak, and Roth 2005; Abdulkadiro˘glu et al. 2005; Pathak and S¨onmez 2008) to replace BM with the betterbehaved Deferred Acceptance mechanism (Gale and Shapley 1962; henceforth, DA) in school-choice systems.

*This work adapts and extends the undergraduate thesis of Yin (2022). Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

One of the most compelling arguments given in favor of replacing BM with DA is the equity argument that originates in the seminal paper of Pathak and S¨onmez (2008), which considers a setting with some students being sincere (i.e., uninformed and unstrategic, always reporting their true preferences) and some being sophisticated (i.e., informed and strategic, together playing a Nash equilibrium). That paper proves that sophisticated students weakly prefer BM over DA (the latter mechanism could be seen as a baseline that treats sincere and sophisticated students equally, due to its strategyproofness). This leads Pathak and S¨onmez (2008) to view BM as weakly (and many times strictly) conferring an advantage to sophisticated students over sincere ones. Pathak and S¨onmez (2008) furthermore prove that when BM is used, sophisticated students weakly prefer for sincere students to remain sincere, giving a plausible explanation as to why informed parent groups might not be likely to share their know-how with parents outside their social circles.

A school district running a centralized matching mechanism is not an isolated capsule. Many districts, each running an independent centralized match, might exist next to each other, and some students might be able to choose in which district’s match to participate. For example, a 2005 report for the Berkeley Uniﬁed School District in California (Fried 2005) estimated that between 7.8% and 12% of the district’s high schoolers were “attending [the district] unof- ﬁcially,” and actually lived out-of-district. Choosing one’s school district can thus be done without ofﬁcial permission (as in the case above) at personal risk,1 or legally by moving to that district, an option many times available only to populations with greater ﬁnancial resources.2

Neighboring school districts are often independent of one another and might use different mechanisms to match students to schools. Due to the ability of some students to choose their school districts, one district switching its mech-

1See, for instance, Martin (2011) for more context on this illegal phenomenon, known as “boundary hopping” or “residency fraud,” which has at times led to prison sentences for parents.

2Comparing the prices of houses located near school district boundaries, Black (1999) estimates that parents are willing to pay 2.1% more to enroll their child in a district with a 5% higher mean test score, and Bayer, Ferreira, and McMillan (2007) similarly estimate a 1.8% higher willingness to pay for homes in a district with an average test score that is higher by one standard deviation.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

16980

<!-- Page 2 -->

anism has the potential to change the multi-district equilibrium, changing students’ strategies not only in terms of how they rank schools within a district but also in terms of their choice of school district. In this paper, we examine the two predictions of Pathak and S¨onmez (2008) that we describe above in a multi-district setting in which district choice (by the students who, for instance, possess the resources to of- ﬁcially relocate or are willing to risk punishment) is endogenized as part of the equilibrium. That is, in our setting, in addition to each student being either sincere or sophisticated, she is also either constrained—able to apply only to schools within her own district of residence—or unconstrained— able to strategically choose any single district within which to apply.3

We prove that even when considering only two school districts, both of the predictions of Pathak and S¨onmez (2008) that we describe above no longer hold. Speciﬁcally, a sophisticated student may strictly prefer for her district to use DA over BM, irrespective of whether she is constrained or unconstrained and of the mechanism used by the other district. Furthermore, a sophisticated student may strictly prefer for some sincere student to become sophisticated. The latter phenomenon also appears abundantly in large random markets; that is, for sufﬁciently large random markets, a constant fraction of sophisticated students strictly prefer that at least some sincere students become sophisticated. We round out our investigation by asking, for completeness, whether some students might prefer for others to change their constraint types, e.g., whether an unconstrained student might prefer for another student to become unconstrained, or whether a constrained student might prefer for another student who resides in a different district to become constrained. We prove a strong “anything goes” result showing that every such combination appears abundantly in large random markets.

Our results are not without limitations. For one, consider the phenomenon of sophisticated students strictly preferring DA over BM. While we show this phenomenon to be possible, it is our only result that might be rare in random markets,4 which could still lend credence to an argument in favor of DA over BM. Importantly, though, this argument becomes a quantitative issue of relative frequency rather than a qualitative issue of existence. More broadly, our paper is not intended to advocate for the use of BM. Rather, ﬁrst and foremost, it serves to introduce a formal model of multi-district school choice and provide a proof-of-concept highlighting that taking into account the broader landscape beyond only a single district may qualitatively change the analysis, including the validity of certain arguments for or against the use of various mechanisms. When designing the speciﬁcs of a mechanism or market (be it when choosing the overall mechanism as discussed in this paper, or possibly even when considering far more minute implementation details), one always weighs the speciﬁcs of the market in

3In either case, if a student is sophisticated, she strategically orders her submitted preference list over the schools in the district to which she applies.

4We do show that its frequency at least does not diminish as the market grows.

question. Our results highlight that in some cases, this market should be even more broadly deﬁned than is customary.

The remainder of this paper is structured as follows. After reviewing related work, in Section 2 we present the multidistrict school choice model. In Section 3 we prove our ﬁrst main result, regarding preference over sophistication types. In Section 4 we prove our second main result, regarding preference over mechanisms. In Section 5 we prove our results regarding preference over constraint types. In Section 6, we dive deeper into the mechanics that enable our ﬁrst main result—that sophisticated students might strictly prefer for some or all sincere students to become sophisticated. We uncover that there are two distinct mechanisms that can drive this result, identify the precise features of our model that enable each of these mechanisms, show their robustness, and derive necessary as well as sufﬁcient conditions over the market structure for each of these mechanisms to manifest. We conclude with a discussion in Section 7.

## 1.1 Related Work The application of mechanism design to school choice originated in

Abdulkadiro˘glu and S¨onmez (2003). Strategic opportunities in BM had been observed when this mechanism was ﬁrst described in the economic literature (Abdulkadiro˘glu et al. 2005), and were subsequently shown in the lab (Chen and S¨onmez 2006) and in the ﬁeld (Calsamiglia and G¨uell 2018). Welfare arguments in favor of DA over BM have appeared in Ergin and S¨onmez (2006) and Kojima (2008), culminating in the equity and fairness arguments of Pathak and S¨onmez (2008). Several papers examine some of the predictions of Pathak and S¨onmez (2008) in various extended models (still within a single district), such as with coarse priority structures (Abdulkadiro˘glu, Che, and Yasuda 2011; Babaioff, Gonczarowski, and Romm 2019) or with a ﬁner classiﬁcation of sophistication types (Zhang 2021). Our large-market analysis methods are technically most closely related to those of Babaioff, Gonczarowski, and Romm (2019).

To our knowledge, ours is the ﬁrst theoretical analysis of multi-district school choice where some students can choose their district. Hafalir, Kojima, and Yenmez (2022) also discuss a notion of interdistrict school choice, but in their model all students can freely rank schools regardless of district, and the focus is on a policy goal of diversity across districts. Grigoryan (2023) considers multiple neighborhoods with a school in each one, but families can again freely rank schools regardless of neighborhood, and the emphasis is on aggregate welfare and welfare for low-income families under different matching mechanisms. In contrast to these papers, because we utilize the lens of constrained and unconstrained students, our multi-district school choice problems are distinct from large single-district problems, allowing us to re-examine the equity arguments of Pathak and S¨onmez (2008) in this setting.

Within a single district, closest to our work are previous papers that analyze different types of schools (such as charter, magnet, and private schools) coexisting with public schools. We discuss these further in Appendix A. Finally, our investigation into the interplay between the choice of

16981

<!-- Page 3 -->

mechanism for one district and the multi-district equilibrium contributes to a recent line of work on “partial mechanism design” (e.g., Philippon and Skreta 2012; Tirole 2012; Kang 2023; see Kang and Muir 2023, for a review).

2 Model 2.1 Standard Concepts Employing much of the notation of Pathak and S¨onmez (2008), we use the following standard concepts from the school choice literature.

Single-District School Choice In a (single-district) school choice problem, there is a set of students I = {i1,..., in} and a set of schools S = {s1,..., sm}. Each student i has a strict preference ordering Pi over some subset of S, and i prefers remaining unassigned over being assigned to schools that are not in this subset. Each school s has a capacity of qs seats, which is the maximum number of students that s can accept, and a strict priority ordering ⇡s over all students. The schools’ priorities for students are responsive in the sense that 1) a school cannot reject students if it is not at capacity, and and 2) a school cannot accept a lower priority student over a higher priority student, regardless of which other students may or may not be accepted. School priority orderings and capacities are public (e.g., set by policy). So that school assignments can be determined, each student submits a rank-order list (henceforth, ROL) of any number of schools, which may or may not match her actual preference ordering.

Mechanisms A school choice mechanism uses students’ submitted ROLs and schools’ priority orderings and capacities to determine school assignments in a single district. Two such mechanisms are the Boston Mechanism (abbreviated as BM) and Deferred Acceptance (abbreviated as DA).

Deﬁnition 2.1. The Boston Mechanism (BM) (Abdulkadiro˘glu et al. 2005) operates in several rounds as follows:

• Round 1: Each student who submitted a non-empty ROL applies to the school she ranked 1st on her ROL. For each school, if there are at least as many seats available as applicants, the school (permanently) accepts every applicant. Otherwise, each school (permanently) allocates seats to applicants based on the school’s priority ordering up to its capacity, and rejects the remaining students. • Round k > 1: Consider only students who have not yet been accepted to a school. Each student who submitted an ROL of at least length k applies to the school she ranked kth. For each school, applicants are accepted or rejected in the same way as in Round 1, where the seats available are those that were not already ﬁlled in previous rounds. If a school has no seats available at the beginning of the round, it rejects all new applicants. • This process terminates when every student has been either assigned a seat at a school or rejected by every school on her ROL, in which case she stays unassigned.

Deﬁnition 2.2. The Deferred Acceptance mechanism (Gale and Shapley 1962) also operates in several rounds, but with only tentative acceptances until the very end, as follows:

• Round 1: Each student who submitted a non-empty ROL applies to the school she ranked 1st on her ROL. For each school, if there are at least as many seats available as applicants, the school tentatively accepts every applicant. Otherwise, each school tentatively allocates seats to applicants based on the school’s priority ordering up to its capacity, and (permanently) rejects the remaining students for whom no seats remain. • Round k > 1: Consider only students who are not currently tentatively accepted at a school (i.e., the students who were rejected by a school in round k−1). Each of these students applies to the school highest on her ROL that has not already rejected her. For each school, new applicants are considered alongside tentatively accepted students. All of these students are compared based on the school’s priority ordering and are tentatively accepted or permanently rejected in the same way as in Round 1.5 • This process terminates when every student has been either assigned a tentative seat or rejected by every school on her ROL, in which case she stays unassigned. All tentative acceptances then become permanent. We say that a mechanism is strategyproof if truthful reporting is a dominant strategy for every student. BM is not strategyproof: a student may beneﬁt from reporting an ROL that differs from her true preference ordering. DA is strategyproof (Dubins and Freedman 1981; Roth 1982): regardless of other students’ reported ROLs, it is a dominant strategy for every student to report her true preference ordering.

## 2.2 Multi-District School Choice

In this paper, we extend the traditional school choice problem (henceforth, the single-district school choice problem) by considering multiple districts. Speciﬁcally, in a multidistrict school choice problem, there is a set of ` districts. Each student i resides in some district d(i) and each school s is located in some district d(s). A student’s preference ordering may be over schools in multiple districts (including districts in which the student does not reside), and a school’s priority ordering is over all students across all districts. A student’s ROL may only contain schools from a single district, however; we call this the district in which she enrolls. Intuitively, this models the real-world setting where a student can only enroll in one school district per year.

Each district uses its own school choice mechanism to determine assignments of the students who enroll in the district to the schools that are located in the district. Different districts may use the same mechanism or different mechanisms; regardless, the school assignments for each district are combined to form the school assignments for the multi-district school choice problem as a whole.

## 2.3 Student Sophistication Types and Constraint Types As in

Pathak and S¨onmez (2008), a student is either sincere or sophisticated; this is known as her sophistication

5Students who were tentatively accepted by the school in round k−1 are not conferred any advantage, and may still be permanently rejected by that school in round k.

16982

<!-- Page 4 -->

type. Once a sincere student i determines that she will enroll in some district j, she submits her preference ordering restricted to schools in j (i.e., Pi with any schools not in j removed) as her ROL. In other words, a sincere student reports her true preferences over schools in the district she enrolls in. On the other hand, a sophisticated student strategizes when submitting her ROL over schools in the district she enrolls in. In addition to having a sophistication type, in the multi-district setting a student is also either constrained or unconstrained; we refer to this as her constraint type. A constrained student i can only enroll in the district in which she resides, d(i); while an unconstrained student can enroll in any (single) district.

Combining these two attributes, we have four categories of students. The behavior of each of these is largely intuitive, with a sincere-constrained student reporting her true preferences over schools in her district of residence; a sophisticated-constrained student strategically choosing an ROL over schools in her district of residence; and a sophisticated-unconstrained student strategically choosing both a district to enroll in and an ROL to submit over schools in that district. As in Pathak and S¨onmez (2008), sophisticated students who enroll in a DA district always use their dominant strategy within that district, i.e., truthfully rank the schools in that district. If an unconstrained student is indifferent between districts to enroll in (i.e. if this student remains unassigned regardless of where she enrolls), then we assume that this student enrolls in her district of residence.

For the majority of this paper, we consider a sincereunconstrained student to be one who reports her true preferences over schools in whichever district she enrolls in, and strategically chooses in which district to enroll accordingly. This is not the only reasonable deﬁnition of sincereunconstrained students, and in Appendix E.3 we ensure that our results also hold for a large class of other deﬁnitions.

## 2.4 Uniform(n; k) Model

Throughout this paper, we use examples of speciﬁc multidistrict school choice problems to demonstrate particular phenomena, some of which stand in contrast to the propositions in Pathak and S¨onmez (2008) that hold for the single-district setting. To analyze how frequently such phenomena occur, we consider large random two-district school choice problems inspired by the uniform models of Babaioff, Gonczarowski, and Romm (2019). In the uniform (n; k) model, there are 2 districts labeled L and R. Collectively, L and R contain n students I = {i1,..., in} and n schools S = {s1, s2,..., sn}, each with unit capacity (i.e., qs = 1 for all s 2 S).

Each student is either sincere or sophisticated; is either constrained or unconstrained; and resides in either district L or district R. There are thus eight categories of students: one for each possible sophistication type – constraint type – district of residence combination. A student’s category is drawn independently of all other students’ categories, and there is a positive probability of a student’s category being any of the eight possibilities. As such, there exists some categoryprobability lower bound p > 0, such that for each category, the probability of an arbitrary student being in this category is at least p. Each student’s preference ordering over schools (which may include schools in any district) is drawn uniformly at random from among all possible (strict) preference orderings of length k.6 Each student’s preference ordering is independent of all other students’ preference orderings, and of all students’ categories.

Each school independently has probability 1/2 of being located in district L and 1/2 of being located in district R.7 Finally, each school has a complete (strict) priority ordering over all students, drawn uniformly at random from the set of all such possible orderings, and independently of everything else. Thus, for any school and any two students ia and ib, the probability that ia has priority over ib at that school is 1/2.

## 3 Sophistication Types

In this section, we show that it is possible for a sophisticated student to prefer that (i.e., strictly beneﬁt if) some sincere student becomes sophisticated. In fact, we prove that such students are abundant in large random markets in which at least one district uses BM. This result stands in contrast to Proposition 3 of Pathak and S¨onmez (2008), which is that in the single-district setting when BM is used, all sophisticated students weakly suffer if any sincere student becomes sophisticated. Finally, we prove that this phenomenon cannot occur when all districts use DA.

We ﬁrst provide an illustrative example. Suppose that there are two districts, L and R, with schools `1 2 L and r1, r2, r3, r4 2 R respectively, where each school has unit capacity. District L uses an arbitrary mechanism, while district R uses BM. Further suppose that there are four students, i1, i2, i3, and i4.

The students’ sophistication types and preference orderings, as well as the schools’ priority orderings, are shown in the table below.8 Students whose preference orderings contain schools in only one district reside in that district and have arbitrary constraint types. Students whose preference orderings contains schools in both districts are unconstrained and reside in an arbitrary district.

Student preferences

(sincere) i1: r2 ≻r1 ≻`1 (sophisticated) i2: `1 ≻r3 (sincere) i3: r2 (sincere) i4: r1 ≻r4

School priority orderings

`1:i1 −i2 r1:i1 −i4 r2:i3 −i1 r3:i2 r4:i4 We show that i2 strictly prefers for i1 to become sophisticated. First, consider the original setting where i1 is sincere-

6This is a special case of the procedure used to draw preference lists in Immorlica and Mahdian (2005).

7These probabilities need only be constant and nonzero for our results to hold, but we set them equal to avoid clutter.

8The notation sa ≻sb indicates a student preference for school sa over school sb. The notation ia −ib indicates a school priority for student ia over student ib. Technically, a school’s priority ordering must include all students. Here, for each school, we list only the priority ordering over students who ﬁnd the school acceptable, as no other student would ever apply to the school.

16983

<!-- Page 5 -->

unconstrained, and recall that i1 strategizes over districts but always reports a truthful ROL. Observe that i1 enrolls in district L, as doing so matches her with school `1 while enrolling in district R results in her being unassigned. This is because if i1 were to enroll in R, she would not be matched in the ﬁrst round of BM, during which both r1 and r2 would be ﬁlled.

Since i1 enrolls in district L, sophisticated-unconstrained student i2 enrolls in district R (and ranks only r3) to avoid being unassigned. The matching process results in i1 assigned to `1, i2 assigned to r3, i3 assigned to r2, and i4 assigned to r1. This is the unique Nash equilibrium outcome. Note that in this outcome, i2 is assigned to her secondchoice school.

Suppose instead that i1 becomes sophisticated. Student i1 has no chance of being assigned to her ﬁrst-choice school, and is guaranteed admittance to r1 if and only if she enrolls in district R and ranks r1 ﬁrst, so she does so. Student i2 therefore chooses to enroll in district L (and ranks only `1), as this (and only this) guarantees her admittance at `1. The matching process results in i1 assigned to r1, i2 assigned to `1, i3 assigned to r2, and i4 is assigned to r4. This is the unique Nash equilibrium outcome. In this outcome, i2 is assigned to her ﬁrst-choice school, which is a strict improvement for her compared to when i1 is sincere.

## 3.1 Large-Market Analysis

We generalize the example above to the uniform (n; 3) model. (The same analysis also works in the uniform (n; k) model for any constant k ≥3.) We say that a sophisticated student ia strictly (weakly) prefers for a sincere student ib to become sophisticated if ia strictly (weakly) prefers her match in every Nash equilibrium of the multi-district school choice problem when ib is sophisticated to her match in every Nash equilibrium of the multi-district school choice problem when ib is sincere. We show that there can be many sophisticated students who strictly prefer for distinct sincere students to become sophisticated. The full proof of Theorem 3.1 is given in Appendix B.1.

Theorem 3.1. For every p 2 (0, 1), there exists ⌧> 0 such that for any large enough n, in the uniform (n; 3) model with category-probability lower bound p and with one district using BM and the other using an arbitrary mechanism, there exists a set of sophisticated students of expected size at least ⌧n wherein each sophisticated student strictly prefers for a distinct sincere student to become sophisticated, and weakly prefers for all other sincere students to become sophisticated.

The proof of Theorem 3.1 shows that in a large random market, for any given set of four students, the probability that this set exhibits the structure from the example above (with respect to some set of ﬁve schools) is sufﬁciently high so that there are many such (disjoint) sets of students in such a market. This proof structure, which is inspired by Babaioff, Gonczarowski, and Romm (2019), is common to the largemarket proofs in our paper.

We conclude this section by proving that the condition in Theorem 3.1 of at least one district using BM is necessary.

The proof of Proposition 3.1 can be found in Appendix B.2.

Proposition 3.1. For every multi-district school choice problem in which all districts use DA, there does not exist a sophisticated student and sincere student pair such that the sophisticated student strictly prefers for the sincere student to become sophisticated.

## 4 Mechanism Choice

In this section, we show that another key result of Pathak and S¨onmez (2008) no longer holds true in the multi-district setting. Speciﬁcally, we show that in the multi-district setting, a sophisticated student may strictly prefer for her district to use DA instead of BM. This is true regardless of whether the sophisticated student is constrained or unconstrained. In particular, we give an example where the sophisticated student only ﬁnds schools in one district acceptable and prefers for that district to use DA.

Our example is as follows. Suppose there are two districts, L and R, with schools `1, `2 2 L and school r1 2 R respectively, where each school has unit capacity. Further suppose that there are three students, i1, i2, and i3.

The students’ sophistication types and preference orderings, as well as the schools’ priority orderings, are shown in the table below. Students i1 and i2 reside in L and have arbitrary constraint types. Student i3 is unconstrained and resides in an arbitrary district.

Student preferences

(sincere) i1:`1 ≻`2 (sophisticated) i2:`2 ≻`1 (sophisticated) i3:`2 ≻r1

School priority orderings

`1:i2 −i1 `2:i1 −i3 −i2 r1:i3

Observe that because i3 is the only student who ﬁnds any school in district R acceptable, the mechanism used by district R is irrelevant.

We show that i2 prefers for district L to use DA rather than BM. First, assume that district L is using BM. As sincere student i1 does not apply to `2 in the ﬁrst round, sophisticated student i3 chooses to apply to `2 in the ﬁrst round, guaranteeing i3’s acceptance at `2. Sophisticated student i2 hence realizes that she has no chance at `2 and instead applies to `1. This process results in i1 unassigned, i2 assigned to `1, and i3 assigned to `2, which is the unique Nash equilibrium outcome. Note that in this Nash equilibrium outcome, i2 is assigned to her second-choice school.

Suppose instead that district L uses DA. Then, student i2 uses her dominant strategy of ranking `2 above `1. This induces student i3 to enroll in R instead of L, as enrolling in L would result in i3 being unassigned. Speciﬁcally, i3 could “knock out” i2 from `2, but in that case i2 would knock out i1 from `1 and i1 would in turn knock out i3 from `2. This process results in i1 assigned to `1, i2 assigned to `2, and i3 assigned to r1, which is the unique Nash equilibrium outcome. In this Nash equilibrium outcome, i2 is assigned to her ﬁrst-choice school, which is a strict improvement for her compared to if district L uses BM.

16984

<!-- Page 6 -->

A key feature of this example is that there exists a cycle within the preferences of i1 and i2. This causes i3 to get knocked out of `2 when i3 applies to district L and district L is using DA. We show in Appendix C.1 that this example can be generalized to include a cycle with additional sophisticated students, in which each sophisticated student within the cycle similarly strictly prefers for the district containing her entire preference list to use DA.

## 4.1 Large-Market Analysis

We generalize the example above to the uniform (n; 2) model. (The same analysis also works in the uniform (n; k) model for any constant k ≥2.) We say that a sophisticated student i strictly prefers for a district d to use DA if i strictly prefers her match in every Nash equilibrium of the multidistrict school choice problem when d uses DA to her match in every Nash equilibrium when d uses BM. We show that there can be a constant number of sophisticated students who each prefer for the district that contains her entire preference list to use DA. The proof of Theorem 4.1 uses similar ideas to that of Theorem 3.1 and can be found in Appendix C.2.

Theorem 4.1. For every p 2 (0, 1), there exists ⌧> 0 such that for any large enough n, in the uniform (n; 2) model with category-probability lower bound p, there exists a set of sophisticated students of expected size at least ⌧wherein each sophisticated student strictly prefers for the district that contains her entire preference list to use DA rather than BM, regardless of the mechanism used by the other district.

## 5 Constraint Types

In this section, we ask, for completeness, whether some students might prefer for some other students to change their constraint type. We ﬁnd a strong “anything goes” result here: For any combination of constraint types for two students, it might be the case that the ﬁrst student strictly prefers for the constraint type of the second student to change, and this is furthermore abundant in large random markets. This holds regardless of the sophistication types of the two students, regardless of whether or not they reside in the same district, and regardless of the mechanisms used by the two districts. We say that a student ia strictly prefers for a student ib to change her constraint type if ia is strictly worse off in every Nash equilibrium of the multi-district school choice problem when ib has her given constraint type compared to every Nash equilibrium of the multi-district school choice problem when ib has the opposite constraint type.

Theorem 5.1. For every p 2 (0, 1), there exists ⌧> 0 such that for every pair of (not necessarily distinct) sophistication types s1 and s2, every pair of (not necessarily distinct) constraint types c1 and c2, and for any large enough n, in the uniform (n; 2) model with category-probability lower bound p and with the districts using any combination of matching mechanisms, there exists a set of expected size at least ⌧n of students of sophistication type s1 and constraint type c1 wherein each student strictly prefers for a distinct student of sophistication type s2 and constraint type c2 from the same district to change her constraint type. Furthermore, this also holds if “from the same district” is replaced with “from the other district.”

The same result also holds in the uniform (n; k) model for any constant k ≥2. As it turns out, two types of constructions sufﬁce to cover all of the various combinations of constraint types, sophistication types, districts of residence, and mechanisms in Theorem 5.1. Let i1 and i2 be two students, where i1 is the student who prefers for i2 to change her constraint type. Both constructions involve i2 vacating her seat at a school s—either because she becomes constrained and s is not in her district of residence, or because she becomes unconstrained and would rather enroll in another district.

The simpler of the two constructions has i1 ﬁlling the vacancy left by i2 at s. This construction can be used in cases where i1 is unconstrained, as well as in cases where i1 is constrained and the school s is in i1’s district of residence. The second, slightly more elaborate construction covers the remaining cases, in which i1 is constrained and the school s is outside i1’s district of residence. These cases, in which our results are arguably more surprising at ﬁrst glance, include situations where i2 resides in the same district as (the constrained) i1 and vacates a spot in another district when i2 becomes constrained, as well as situations where i2 resides in a different district than i1 and vacates a spot in that district when i2 becomes unconstrained. In such cases, we introduce a third, unconstrained student, i3, who takes the seat vacated by i2 and therefore vacates a seat in the district of i1, which i1 in turn gets to ﬁll.

In Appendix D, we prove two cases of Theorem 5.1—one using each of the two constructions. The proof of each of the other cases of Theorem 5.1 is completely analogous to the proof of one of these two cases.

Sincere-Unconstrained Students In this section, we dive deeper into the machinery behind the results of Section 3, and ask which features of the school choice problems used in the analysis of that section are necessary for the results in that section to hold.

The deﬁnitions of three of the student types in our taxonomy follow closely from ideas in Pathak and S¨onmez (2008). Our fourth type—sincere-unconstrained students— while still heavily inspired by Pathak and S¨onmez (2008) and completely in line with our taxonomy, is conceptually (and formally, as we discuss below) further from the types deﬁned by that paper. Therefore, we ﬁrst ask whether and to what extent this student type plays a key role in our analysis, and then ask whether and to what extent our results are robust to changes in the precise deﬁnition of such students.

The construction in Section 3 hinges on a trait that only a sincere-unconstrained student can possess: She can block a sophisticated student from getting a seat at some school, and yet, she may vacate that seat for another school if she becomes sophisticated.9 The ﬁrst question we ask is whether there exists a school choice problem in which a sophisticated

9While a sincere-constrained student can also block a sophisticated student in the same way, a sincere-constrained student will not vacate that seat if she becomes sophisticated, as it is the best outcome she can achieve.

16985

<!-- Page 7 -->

student prefers for a sincere student to become sophisticated even in the absence of sincere-unconstrained students, to which we give an afﬁrmative answer. The proof of Proposition 6.1 is given in Appendix E.1.

Proposition 6.1. There exists a two-district school choice problem where (1) all sincere students are constrained, and (2) there exists a sophisticated student who strictly prefers for a speciﬁc sincere student to become sophisticated.

We observe that replacing the gadget in our current proof of Theorem 3.1 by the school choice problem from Proposition 6.1 results in a weaker guarantee. Speciﬁcally, the resulting guarantee is of an expected number of sophisticated students who prefer for some sincere student to become sophisticated that is only constant, rather than a constant fraction of the total number of students. In Appendix E.2, we argue that in fact no school choice problem that lacks sincereunconstrained students can result in a constant-fraction guarantee when used as the gadget in our proof of Theorem 3.1.

Given this, we next ask how robust Theorem 3.1 is to the precise deﬁnition of sincere-unconstrained students. Beyond fully strategizing over district choice and always enrolling in the district of her ﬁrst-choice school, there are many other reasonable ways a sincere-unconstrained student can choose where to enroll. For example, a sincereunconstrained student might simply count the number of schools on her preference ordering from each district, and enroll in the district with the most such schools. We show that our results extend to when sincere-unconstrained students use such positional heuristics as well. Taking inspiration from social choice theory (e.g., Young 1975; Boutilier et al. 2012), we deﬁne the class of scoring functions below.

Deﬁnition 6.2.

• For v 2 Rn, deﬁne the scoring function f v as follows. For any preference ordering Pi, deﬁne Pi(s) as the ranking of school s in Pi. Further let v

!

Pi(s)

"

= vPi(s) if s 2 Pi and v

!

Pi(s)

"

= 0 otherwise. Then we deﬁne the scoring function as f v(Pi) = arg max d

X s:d(s)=d v

!

Pi(s)

"

.

• A scoring function is monotone if both v!

Pi(s)

"

≥ v

!

Pi(s0)

" whenever s is ranked higher than s0 in Pi and v

!

Pi(s)

"

≥0 whenever s 2 Pi. • A sincere-unconstrained student uses a positional heuristic if she chooses in which district to enroll based on a monotone scoring function. In the case of a tie between districts, we assume that a student using a positional heuristic enrolls in the district of the school that she ranks ﬁrst among all schools in the tied districts.

If a sincere-unconstrained student enrolls in the district with the most schools they ﬁnd acceptable, this is equivalent to using a positional heuristic that assigns a score of 1 to every school in her preference ordering. Other examples of positional heuristics can be found in Appendix E.3. We adapt our large-market analysis to show that a version of Theorem

3.1 still holds when sincere-unconstrained students use positional heuristics. The proof of Theorem 6.1 can be found in Appendix E.3, along with its associated instance.

Theorem 6.1. Suppose that sincere-unconstrained students use a positional heuristic to decide which district to enroll in. Then for every p 2 (0, 1), there exists ⌧> 0 such that for any large enough n, in the uniform (n; 5) model with category-probability lower bound p and with one district using BM and the other using DA, there exists a set of sophisticated students of expected size at least ⌧n where each sophisticated student strictly prefers for a distinct sincere student to become sophisticated, and weakly prefers for all other sincere students to become sophisticated.

## Discussion

We show that several key results regarding sincere and sophisticated students from the seminal paper of Pathak and S¨onmez (2008) no longer hold in a multi-district setting. This highlights that when designing centralized mechanisms, it might be useful to deﬁne the market in question more broadly than is customary.

Several aspects of our model and results would potentially beneﬁt from further research. First, although the idea of district choice is motivated by students and their families boundary hopping or paying a premium to move, we do not explicitly model the associated (ﬁnancial or risk-taking) costs. Future research could impose a price on choosing a district other than one’s own district of residence, which would then factor into students’ strategic considerations. For this to be effective, it would also be necessary to think about student satisfaction with different school assignments using cardinal utilities rather than ordinal preferences. 10

While Theorem 4.1 establishes an at least constant frequency of sophisticated students who strictly prefer DA over BM even in a large random market, it is our only theorem that does not prove the abundance of such students. Even if we extend the proof of Theorem 4.1 to also take into account all cycles of the form discussed in Appendix C.1, the same proof technique would yield only constant frequency. To achieve a linear, or even super-constant frequency, one would have to, for example, ﬁnd a way for the existence of some cycle to be sufﬁcient for a super-constant number of sophisticated students outside the cycle to strictly prefer BM over DA. While we conjecture that this is not possible, ruling this out seems to be related to the question of whether Deferred Acceptance “circuits” can efﬁciently encode computational circuits in which various wires split, a question that was resolved negatively by Cook, Filmus, and Le (2014). It is plausible that computational-complexity-theoretic tools such as those used in that paper might be leveraged to prove the asymptotic tightness of the bound in Theorem 4.1. We conjecture this bound to be tight (perhaps up to logarithmic factors if preference list lengths are not held constant), but leave the veriﬁcation of this conjecture for future work.

10A recent paper by Artemov and Tomoeda (2025) studies a single district in which students can have “walking distance” priority for a school based on where they reside. Future research might draw inspiration from how their model incorporates a moving cost.

16986

<!-- Page 8 -->

## Acknowledgments

We thank Scott Kominers and Assaf Romm for insightful comments and discussions. Gonczarowski gratefully acknowledges research support by the National Science Foundation (NSF-BSF grant No. 2343922), Harvard FAS Inequality in America Initiative, and Harvard FAS Dean’s Competitive Fund for Promising Scholarship. Zhang was supported by an NSF Graduate Research Fellowship.

## References

Abdulkadiro˘glu, A.; Che, Y.-K.; and Yasuda, Y. 2011. Resolving Conﬂicting Preferences in School Choice: The “Boston Mechanism” Reconsidered. American Economic Review, 101(1): 399–410. Abdulkadiro˘glu, A.; Pathak, P. A.; and Roth, A. E. 2005. The New York City High School Match. American Economic Review, 95(2): 364–367. Abdulkadiro˘glu, A.; Pathak, P. A.; Roth, A. E.; and S¨onmez, T. 2005. The Boston Public School Match. American Economic Review, 95(2): 368–371. Abdulkadiro˘glu, A.; and S¨onmez, T. 2003. School choice: A mechanism design approach. American Economic Review, 93(3): 729–747. Afacan, M. O.; Evdokimov, P.; Hakimov, R.; and Turhan, B. 2022. Parallel Markets in School Choice. Games and Economic Behavior, 133: 181–201. Akbarpour, M.; Kapor, A.; Neilson, C.; Van Dijk, W.; and Zimmerman, S. 2022. Centralized School Choice With Unequal Outside Options. Journal of Public Economics, 210: 104644. Artemov, G.; and Tomoeda, K. 2025. Zoned Out: The Long- Term Consequences of School Choice for Wealth Segregation. Mimeo. Babaioff, M.; Gonczarowski, Y. A.; and Romm, A. 2019. Playing on a Level Field: Sincere and Sophisticated Players in the Boston Mechanism with a Coarse Priority Structure. In Proceedings of the 20th ACM Conference on Economics and Computation (EC), 345. Bayer, P.; Ferreira, F.; and McMillan, R. 2007. A Uni- ﬁed Framework for Measuring Preferences for Schools and Neighborhoods. Journal of Political Economy, 115(4): 588– 638. Black, D. 1958. The Theory of Committees and Elections. Cambridge: Cambridge University Press. Black, S. E. 1999. Do Better Schools Matter? Parental Valuation of Elementary Education. The Quarterly Journal of Economics, 114(2): 577–599. Boutilier, C.; Caragiannis, I.; Haber, S.; Lu, T.; Procaccia, A. D.; and Sheffet, O. 2012. Optimal Social Choice Functions: A Utilitarian View. In Proceedings of the 13th ACM Conference on Electronic Commerce (EC), 197–214. Calsamiglia, C.; and G¨uell, M. 2018. Priorities in School Choice: The Case of the Boston Mechanism in Barcelona. Journal of Public Economics, 163: 20–36.

Chen, Y.; and S¨onmez, T. 2006. School Choice: An Experimental Study. Journal of Economic Theory, 127(1): 202– 231. Cook, S. A.; Filmus, Y.; and Le, D. T. M. 2014. The Complexity of the Comparator Circuit Value Problem. ACM Transactions on Computation Theory (TOCT), 6(4): 1–44. Do˘gan, B.; and Yenmez, M. B. 2019. Uniﬁed versus divided enrollment in school choice: Improving student welfare in Chicago. Games and Economic Behavior, 118. Dubins, L. E.; and Freedman, D. A. 1981. Machiavelli and the Gale-Shapley Algorithm. The American Mathematical Monthly, 88(7): 485–494. Ekmekci, M.; and Yenmez, M. B. 2019. Common Enrollment in School Choice. Theoretical Economics, 14(4): 1237–1270. Ergin, H.; and S¨onmez, T. 2006. Games of School Choice Under the Boston Mechanism. Journal of Public Economics, 90(1-2): 215–237. Fried, R. 2005. Attending to the Bottom Line: Boosting District Revenue and Enhancing Educational Mission Through Interdistrict Enrollment & Attendance Policy. An advanced policy analysis prepared for the Berkeley uniﬁed school district, Berkeley, California. Gale, D.; and Shapley, L. 1962. College admissions and the stability of marriage. American Mathematical Monthly, 69(1): 9–15. Grigoryan, A. 2023. School Choice and the Housing Market. Mimeo. Hafalir, I. E.; Kojima, F.; and Yenmez, M. B. 2022. Interdistrict school choice: A theory of student assignment. Journal of Economic Theory, 201. Immorlica, N.; and Mahdian, M. 2005. Marriage, honesty, and stability. In Proceedings of the Sixteenth Annual ACM-SIAM Symposium on Discrete Algorithms, SODA ’05, 53–62. Society for Industrial and Applied Mathematics. Kang, Z.; and Muir, E. 2023. Partial Mechanism Design and Incomplete-Information Industrial Organization. Tutorial, The 24th ACM Conference on Economics and Computation (EC). Kang, Z. Y. 2023. The Public Option and Optimal Redistribution. Mimeo. Kojima, F. 2008. Games of School Choice Under the Boston Mechanism With General Priority Structures. Social Choice and Welfare, 31: 357–365. Manjunath, V.; and Turhan, B. 2016. Two School Systems, One District: What to Do When a Uniﬁed Admissions Process is Impossible. Games and Economic Behavior, 95: 25– 40. Martin, M. 2011. Mother Jailed for School Fraud, Flares Controversy. Tell Me More, NPR. Pathak, P. A.; and S¨onmez, T. 2008. Leveling the playing ﬁeld: Sincere and sophisticated players in the Boston mechanism. American Economic Review, 98(4): 1636–1652. Philippon, T.; and Skreta, V. 2012. Optimal Interventions in Markets with Adverse Selection. American Economic Review, 102(1): 1–28.

16987

<!-- Page 9 -->

Roth, A. E. 1982. The Economics of Matching: Stability and Incentives. Mathematics of operations research, 7(4): 617–628. Tirole, J. 2012. Overcoming Adverse Selection: How Public Intervention Can Restore Market Functioning. American Economic Review, 102(1): 29–59. Turhan, B. 2019. Welfare and Incentives in Partitioned School Choice Markets. Games and Economic Behavior, 113: 199–208. Yin, M. 2022. Multi-District School Choice: When Sincere Students Stay and Sophisticated Students Stray. Underaduate thesis, Harvard University. Young, H. P. 1975. Social Choice Scoring Functions. SIAM Journal of Applied Mathematics, 28(4): 824–838. Zhang, J. 2021. Level-k reasoning in school choice. Games and Economic Behavior, 128: 1–17.

16988
