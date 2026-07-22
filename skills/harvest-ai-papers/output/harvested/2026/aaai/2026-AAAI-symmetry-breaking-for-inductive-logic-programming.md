---
title: "Symmetry Breaking for Inductive Logic Programming"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38973
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38973/42935
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Symmetry Breaking for Inductive Logic Programming

<!-- Page 1 -->

Symmetry Breaking for Inductive Logic Programming

Andrew Cropper1,2*, David M. Cerna3,4*, Matti J¨arvisalo2

1ELLIS Institute Finland 2University of Helsinki 3Dynatrace Research 4Czech Academy of Sciences Institute of Computer Science andrew.cropper@helsinki.fi, {david.cerna, dcerna}@{dynatrace.com, cs.cas.cz}, matti.jarvisalo@helsinki.fi

## Abstract

The goal of inductive logic programming is to search for a hypothesis that generalises training data and background knowledge. The challenge is searching vast hypothesis spaces, which is exacerbated because many logically equivalent hypotheses exist. To address this challenge, we introduce a method to break symmetries in the hypothesis space. We implement our idea in answer set programming. Our experiments on multiple domains, including visual reasoning and game playing, show that our approach can reduce solving times from over an hour to 17 seconds.

Code — https://github.com/logicand-learning-lab/aaai26- symbreak Extended version — https://arxiv.org/pdf/2508.06263

## Introduction

Inductive logic programming (ILP) is a form of machine learning (Muggleton 1991; Cropper and Dumancic 2022). The goal is to search a hypothesis space for a hypothesis (a set of rules) that generalises given training examples and background knowledge (BK).

To illustrate ILP, consider the inductive reasoning game Zendo. In this game, one player, the teacher, creates a secret rule that describes structures. The other players, the students, try to discover the secret rule by building structures. The teacher marks whether structures follow or break the rule. The first student to correctly guess the rule wins. For instance, for the positive and negative examples shown in Figure 1, a possible rule is “there is a small blue piece”.

**Figure 1.** Positive (E+) and negative (E−) Zendo examples.

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Given these examples and BK about the structures, an ILP system can induce a rule such as:

zendo(A) ←piece(A,B), size(B,C), blue(B), small(C)

The fundamental challenge in ILP is searching large hypothesis spaces. Recent approaches tackle this challenge by delegating the search to an off-the-shelf solver, such as a Boolean satisfiability solver (Ahlgren and Yuen 2013; Hocquette et al. 2024) or an answer set programming (ASP) solver (Law, Russo, and Broda 2014; Kaminski, Eiter, and Inoue 2019; Cropper and Morel 2021; Evans et al. 2021).

One problem for recent approaches is symmetries in the hypothesis space where many logically equivalent hypotheses exist. For instance, consider these two Zendo rules:

r1 = zendo(A) ←piece(A,B), size(B,C), blue(B), small(C) r2 = zendo(A) ←piece(A,C), size(C,B), blue(C), small(B)

Both rules can be in the hypothesis space. However, the rules are syntactic variants when considering theta-substitution (Plotkin 1971; Lloyd 2012). For instance, r1 = r2θ where θ = {C 7→B, B 7→C}. However, determining whether two rules are symmetrical (syntactic variants) is hard. For instance, theta-substitution is in general NP-complete (Garey and Johnson 1979).

In this paper, we address this symmetry challenge. We first define the body-variant problem: determining whether two rules only differ by the naming of body-only variables, such as r1 and r2 above. We show that this problem is graphisomorphism hard (K¨obler, Sch¨oning, and Tor´an 1993).

Due to the hardness of the body-variant problem, we introduce a sound, albeit incomplete, symmetry-breaking approach. Our idea exploits an ordering of variables in a rule. If a body literal l does not contain a variable x, but contains variables both larger and smaller than x according to the variable ordering, then x must occur in a literal lexicographically smaller than l. In other words, any gaps in the occurrence of variables with respect to an ordering must be justified by lexicographically smaller literals. We only order literals with arity greater than one because we assume that rules do not contain singleton variables, so the argument of a unary literal must appear elsewhere in the rule.

To illustrate our approach, consider rules r1 and r2 above. Assuming that variables are ordered alphabetically, the literal piece(A,C) of r2 has a gap in its arguments because B is

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19012

![Figure extracted from page 1](2026-AAAI-symmetry-breaking-for-inductive-logic-programming/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-symmetry-breaking-for-inductive-logic-programming/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

missing. Furthermore, size(C,B) contains B but (A, C) <lex (B, C). By renaming C to B and B to C within r2 the rule r1 results. Observe that, r1 contains both piece(A, B) and size(B, C) and (A, B) <lex (B, C). Thus, we can remove r2 from the hypothesis space and keep r1.

We implement our symmetry-breaking idea in ASP and demonstrate it with the ASP-based ILP system POPPER, which can learn optimal and recursive hypotheses from noisy data (Cropper and Morel 2021; Hocquette et al. 2024). We show that adding symmetry-breaking constraints to POPPER can drastically reduce solving and learning time, sometimes from over an hour to only 17 seconds.

Contributions and Novelty. The main novelty of this paper is a method for breaking symmetries in ILP. As far as we are aware, there is no existing work on this topic. The impact, which we demonstrate on multiple domains, is vastly reduced solving and learning times. Moreover, this work connects multiple AI areas, notably machine learning and constraint programming. Overall, we contribute the following:

• We define the problem of determining whether two rules are body-variants (Definition 6). We show that this problem is graph isomorphism hard (Proposition 1). • We describe a symmetry-breaking approach to prune body-variant rules. We prove that this approach is sound and only prunes body-variant rules (Proposition 2). • We describe an ASP implementation of our encoding that works with the ILP system POPPER. • We show experimentally on multiple domains, including visual reasoning and game playing, that our approach can reduce solving and learning times by 99%.

## Related Work

Rule learning. ILP induces rules from data, similar to rule learning methods (F¨urnkranz and Kliegr 2015), such as AMIE+ (Gal´arraga et al. 2015) and RDFRules (Zeman, Kliegr, and Sv´atek 2021). Rule-mining methods are typically limited to unary and binary relations and require facts as input and operate under an open-world assumption. By contrast, ILP usually operates under a closed-world assumption, supports relations of any arity, and can learn from definite programs as background knowledge.

ILP. Most classical ILP approaches build a hypothesis using a set covering algorithm by adding rules one at a time (Quinlan 1990; Muggleton 1995; Blockeel and De Raedt 1998; Srinivasan 2001). These approaches build rules literalby-literal using refinement operators to generalise or specialise a rule (Shapiro 1983; Quinlan 1990; Muggleton 1995; De Raedt and Dehaspe 1997; Blockeel and De Raedt 1998; Srinivasan 2001; Tamaddoni-Nezhad and Muggleton 2009). We differ because we do not use refinement operators. Rather, we break symmetries in an ILP approach that frames the ILP problem as a constraint satisfaction problem.

Constraint-based ILP. Many ILP systems frame the ILP problem as a constraint satisfaction problem, such as SAT (Ahlgren and Yuen 2013; Hocquette et al. 2024) and ASP (Corapi, Russo, and Lupu 2011; Law, Russo, and Broda 2014; Sch¨uller and Benz 2018; Kaminski, Eiter, and Inoue

2019; Evans et al. 2021; Bembenek, Greenberg, and Chong 2023). Most of these approaches formulate the ILP problem as rule selection where they precompute every possible rule in the hypothesis space and use a solver to search for a subset that generalises the examples. Because they precompute all possible rules, they cannot learn rules with many literals. By contrast, we build constraints to restrict rule generation without precomputation.

Redundancy in ILP. Symmetry breaking is a form of redundancy elimination. There is much work on avoiding redundancy in ILP, such as when testing hypotheses on training data (Struyf and Blockeel 2003). Raedt and Ramon (2004) check whether a rule has a redundant atom before testing it on examples to avoid a coverage check. Zeng, Patel, and Page (2014) prune rules with syntactic redundancy. For the rule h(X) ←p(X,Y), p(X,Z), they detect that p(X,Z) duplicates p(X,Y) under the renaming Z 7→Y, where Z and Y are not in other literals. By contrast, we reduce redundancy through declarative symmetry-breaking constraints.

Symmetry Breaking. Highly symmetric problems, when represented declaratively, can lead solvers such as ASP and SAT to perform redundant search. Lex-leader (Crawford et al. 1996) uses tools for computing graph symmetries (McKay 1981; Junttila and Kaski 2007; Darga et al. 2004) to automatically identify instance-specific symmetries. Detected symmetries are eliminated by introducing lex-leader symmetrybreaking constraints during preprocessing. This approach has been employed in SAT (Aloul, Markov, and Sakallah 2003; Anders, Brenner, and Rattan 2024), ASP (Drescher, Tifrea, and Walsh 2011; Devriendt and Bogaerts 2016), and other declarative approaches. Tarzariol, Gebser, and Schekotihin (2021) use ILP to learn first-order ASP symmetry-breaking constraints from examples of instance-specific constraints. By contrast, we break symmetries in the ILP hypothesis space. Our notion of symmetry differs from conventional domainlevel symmetries (Devriendt et al. 2016). In our work, symmetry refers to syntactic variable interchangeability in rule bodies: two rules are symmetric if one can be obtained from the other by renaming variables.

## 3 Inductive Logic Programming

In this section, we define ILP and describe prerequisite notation. Let P be a countably infinite set of predicate symbols and V be a countably infinite set of variables totally wellordered by <V. A term is either a constant or a variable. Every p ∈P has an arity 0 ≤a denoted arity(p). An atom is of the form p(t1,..., ta) where p ∈P, t1,..., ta are terms. Given an atom l = p(t1,..., ta), sym(l) = p, arity(l) = a, args(l) = (t1,..., ta) where (...) is an ordered tuple. We refer to an atom as ground if all its arguments are constants and constant-free if all its arguments are variables. A literal is an atom or a negated atom. A rule r is of the form h ←p1,..., pn where h, p1,..., pn are literals, head(r) = h, body(r) = {p1,..., pn}, and body≥2(r) is the subset of body(r) containing all literals in r with arity ≥2. We will only consider rules that are head-connected, i.e. all variables occurring in the head of a rule appear in a literal of the body of the rule. We refer

19013

<!-- Page 3 -->

to a rule as constant-free if all of its literals are constantfree. By vars(l) we denote the set of variables in a literal l. The variables of a rule r, denoted vars(r), is defined as head vars(r) ∪body vars(r) where head vars(r) = vars(head(r)) and body vars(r) = vars(body(r)).

We formulate our approach in the ILP learning from entailment setting (De Raedt 2008). We define an ILP input: Definition 1 (ILP input). An ILP input is a tuple (E, B, H) where E = (E+, E−) is a pair of sets of ground atoms denoting positive (E+) and negative (E−) examples, B is background knowledge, and H is a hypothesis space, i.e a set of possible hypotheses. We restrict hypotheses and background knowledge to definite programs with the least Herbrand model semantics (Lloyd 2012). We define a cost function: Definition 2 (Cost function). Given an ILP input (E, B, H), a cost function costE,B: H 7→N assigns a numerical cost to each hypothesis in H. We define an optimal hypothesis: Definition 3 (Optimal hypothesis). Given an ILP input (E, B, H) and a cost function costE,B, a hypothesis h ∈H is optimal with respect to costE,B when ∀h′ ∈H, costE,B(h) ≤costE,B(h′).

## 4 Complexity of Symmetry Breaking in ILP

Our goal is to find a subset of a hypothesis space that contains at least one optimal hypothesis after symmetry breaking: Definition 4 (Hypothesis space reduction problem). Given an ILP input (E, B, H), the hypothesis space reduction problem is to find H′ ⊆H such that if H contains an optimal hypothesis then there exists an optimal hypothesis h ∈H′. We focus on breaking symmetries by removing hypotheses that differ only by renaming variables. We define a bodyvariant rule: Definition 5 (Body variant). A rule r′ is a body-variant of a rule r if there exists a bijective renaming σ from body vars(r) to body vars(r′) such that rσ = r′. Example 1. Consider the rules in the introduction: r1 = zendo(A) ←piece(A,B), size(B,C), blue(B), small(C) r2 = zendo(A) ←piece(A,C), size(C,B), blue(C), small(B) Observe that head(r1) = head(r2) and using σ1 = {C 7→ B, B 7→C} and σ2 = {B 7→C, C 7→B}, it follows that r1σ1 = r2 and r2σ2 = r1 The body-variant problem is to decide whether two rules differ only by the naming of body-only variables: Definition 6 (Body-variant problem). Given rules r1 and r2 such that head(r1) = head(r2), the body-variant problem is deciding whether r1 and r2 are body-variants of each other. Deciding whether two rules are body variants is intractable as there is a reduction from the graph isomorphism problem to the body-variant problem, for which existing decision procedures are computationally prohibitive (Babai and Luks 1983; Babai and Codenotti 2008). The following result illustrates the (GI)-hardness (K¨obler, Sch¨oning, and Tor´an 1993) of the body-variant problem:

Proposition 1 (Body-variant hardness). The body-variant problem is GI-hard1.

Proof (sketch). We encode a graph G = (N, E) as a rule using a binary relation edge/2 and |N| variables denoting nodes of G. The reduction follows from this encoding (See Appendix).

This result motivates us to develop an incomplete yet tractable approach to the body-variant problem. Before discussing our approach, we first generalise the body-variant problem to hypothesis variants:

Definition 7 (Hypothesis variant). A hypothesis h′ is a variant of a hypothesis h if there is a bijective mapping f from the rules of h′ to the rules of h such that for all r ∈h′, r is a body variant f(r).

Example 2. Consider the following hypotheses:

Hypothesis 1 (h1) r1 = zendo(A) ←piece(A,B), size(B,C), blue(B), small(C) r2 = zendo(A) ←piece(A,C), size(C,B), red(C), large(B)

Hypothesis 2 (h2) r3 = zendo(A) ←piece(A,C), size(C,B), blue(C), small(B) r4 = zendo(A) ←piece(A,B), size(B,C), red(B), large(C)

Using a mapping f such that f(r1) = r3 and f(r2) = r4, we can observe that h1 is a hypothesis-variant of h2.

We generalise the body-variant problem to hypotheses:

Definition 8 (Hypothesis-variant problem). Given hypotheses h1 and h2, the hypothesis-variant problem is deciding whether h1 and h2 are hypothesis-variants of each other.

The body-variant problem is a special case of the hypothesisvariant problem, where hypotheses contain a single rule. Thus, it follows that the hypothesis-variant problem is also GI-hard.

## 5 Tractable Symmetry Breaking for ILP

Due to the hardness of the hypothesis variant problem, we now describe a sound yet incomplete approach to remove hypothesis variants from an ILP hypothesis space. For simplicity, we describe the approach for a single-rule hypothesis before generalising to arbitrary hypotheses.

Informally, our approach exploits variable ordering in a rule and forces the following condition on all rules in the hypothesis space. If a body literal l does not contain a variable x, but contains variables both larger and smaller than x according to the variable ordering, then x must occur in a literal lexicographically smaller than l. In other words, any skipped occurrence of a variable, with respect to <V, must be justified by lexicographically smaller literals.

To illustrate the idea, reconsider this Zendo rule from the introduction:

r2 = zendo(A) ←piece(A,C), size(C,B), blue(C), small(B)

1Arvind et al. (2015) reduce graph isomorphism to hypergraph isomorphism. Using this reduction we can extend our reduction from binary to n-ary predicates.

19014

<!-- Page 4 -->

We order variables alphabetically, i.e. A <V B <V C. The variable B is not in piece(A,C) so we need to check if a lexicographically smaller variable tuple than (A, C) is in the rule. To compare tuples we first order the variables in the tuple and add a prefix containing occurrences of the smallest variable. We assume that rules do not contain singleton variables. Thus, the argument of a unary literal must appear elsewhere in the rule, i.e. how the literal is ordered is completely dependent on another literal. For instance, the tuple of size(C,B) is (B, C) and the tuple of piece(A,C) is (A, C). Observe that (A, C) <lex (B, C) and there are no tuples smaller than (A, C) derivable from the rule. Thus, r2 is pruned because it does not contain a tuple smaller than (A, C) containing the skipped variable B. Observe that a similar analysis shows that r1 from the introduction is not pruned.

To formalise our approach, we make several assumptions explicit:

(i) A rule contains only variables, no constants. For example, the rule zendo(A) ←piece(A,B) obeys this assumption, but zendo(A) ←piece(A,lbt) does not, where lbt is a constant. (ii) The variables in the head of a rule are always the smallest variables according to the variable ordering2. Formally, for any rule r, v1 ∈head vars(r), v2 ∈body vars(r), v1 <V v2. For example, the rule zendo(A) ←piece(A,B) obeys this assumption as A <V B while the rule zendo(B) ←piece(A,B) does not. (iii) A variable is in a rule if and only if every smaller variable is in the rule. Formally, for any rule r, v1, v2 ∈vars(r), if there exists v3 ∈V such that v1 <V v3 <V v2, then v3 ∈vars(r). For example, the rule zendo(A) ← piece(A,B) obeys this assumption, while the rule zendo(A) ←piece(A,C) does not as A <V B <V C.

Any rule that violates assumptions (ii) and/or (iii) can be transformed by a variable renaming into the appropriate form, either by shifting variables or swapping head and body variables. Furthermore, we consider the argument tuples of literals reordered with respect to <V:

Definition 9 (Ordered variables). Let l be a literal, args(l) = (x1,..., xn), 1 ≤i1, · · ·, in ≤n such that for all 1 ≤j < n, xij ≤V xij+1 and ij̸ = ij+1. Then ord vars(l) = (xi1,..., xin).

Example 3. Let A <V B <V D, and l = p(D, A, B) be a literal. Then ord vars(l) = (A, B, D).

Additionally, we add a prefix to the tuples resulting from Definition 9 to produce tuples of uniform length:

Definition 10 (Prefix padding). Let k ≥0 and l be a literal such that ord vars(l) = (x1,..., xn). Then pre padk(l) = (x⋆,..., x⋆, | {z }

max{0,k−n} times x1,..., xn)

where x⋆is the minimal element with respect to <V.

For the rest of this section we assume the following:

2The total order <V on variable symbols.

Assumption 1. Let p be a predicate symbol in the BK such that for all other predicate symbols q in the BK, arity(p) ≥ arity(q). Then k ≥arity(p). We define a lexicographical literal order to order literals by first rearranging their arguments with respect to <V and then adding a prefix to the resulting tuples to produce tuples of uniform size: Definition 11 (Lexicographical literal order). Let l1 and l2 be literals with arity ≥2. Then we say that l1 <k lex l2 if pre padk(l1) <lex pre padk(l2) where <lex is the lexicographical order on k-tuples. Example 4. Let l1 = p(D, A, B) and l2 = q(C, B) be literals where variables are alphabetically ordered and k = 3. Then l2 <3 lex l1 because ord vars(l1) = (A, B, D), ord vars(l2) = (B, C), pre pad3(l1) = (A, B, D), pre pad3(l1) = (x∗, B, C), and (x∗, B, C) <lex (A, B, D) where x∗= A. We use this order to identify literals with skipped variables: Definition 12 (Skipped). Let l be a literal such that pre padk(l) = (x1,..., xn). Then skippedk(l) = {y | x1 <V y <V xn ∧y̸ ∈vars(l)}. Example 5. Consider the rule h(A, B) ← p(A, E), p(B, C), p(C, D) where variables are ordered alphabetically. Observe that skipped2(p(A, E)) = {B, C, D} and skipped2(p(C, D)) = ∅. Rules can contain literals with skipped variables but the skipped variables must be witnessed by a literal lower in the lexicographical literal order: Definition 13 (Witnessed). Let r be a rule, v be a variable, l1 ∈body≥2(r) such that v ∈skippedk(l1), and l2 ∈body≥2(r) such that v ∈vars(l2) and l2 <k lex l1. Then we say that l1 is v-witnessed in r.

A variable is unsafe if it is skipped in a literal and there is no witnessing literal: Definition 14 (Safe variable). Let r be a rule and v ∈ body vars(r) such that for all l ∈body≥2(r), where v ∈ skippedk(l), l is v-witnessed in r. Then v is safe. Otherwise, v is unsafe. We illustrate the concept of safe variables: Example 6. Consider the rules:

r2 = h(A,B) ←p(A,C),p(B,E),p(C,D) r3 = h(A,B) ←p(A,C),p(B,D),p(C,E) Observe that p(B, E) skips D and none of the literals of r2 witness p(B, E). The only literal containing D is p(C, D) and p(B, E) <2 lex p(C, D). Thus, D is unsafe in r2. In rule r3, p(C, E) skips D and p(C, E) is witnessed by p(B, D) because p(B, D) <2 lex p(C, E). Thus, D is safe in r3. Observe that in r3 all variables are safe including C and E, i.e. p(A, C) <2 lex p(B, D). We now show that every rule has a body-variant containing only safe variables: Proposition 2 (Soundness). For every rule r there exists a rule r′ such that r′ is a body-variant of r and all variables in r′ are safe.

19015

<!-- Page 5 -->

Proof (sketch). To simplify our argument we assume that vars(r) = {x1, · · ·, xm} where for 1 ≤j < m, xj <V xj+1. We prove the proposition by induction,3 selecting the smallest unsafe variable x (according to <V) and then constructing a substitution that, when applied to r, results in a rule where the smallest unsafe variable is larger than x. After finitely many steps the smallest unsafe variable is larger than xm, i.e. every variable in the constructed rule is safe.

See the appendix for a full proof. Below we outline the transformation used by the induction step of the full proof. Example 7. Let r8 = h(A, B) ←p(A, E), p(B, C), p(C, D).

where the variables are ordered alphabetically. The argument outlined in the proof of Proposition 2 applies to rule r8 as follows. Observe that C is the smallest unsafe variable in r8. Applying σ1 = {E 7→C, C 7→F}{F 7→E} to r8 we get the rule:

r9 = h(A, B) ←p(A, C), p(B, E), p(E, D).

Now D is the smallest unsafe variable in r9. Applying σ2 = {E 7→D, D 7→F}{F 7→E} to r9 we get the rule:

r10 = h(A, B) ←p(A, C), p(B, D), p(D, E).

Observe that rule r10 does not have unsafe variables. Thus applying the substitution σ = σ1σ2 = {E 7→C, C 7→ D, D 7→E} to r results in a body-variant where all variables are safe. We now show our main result: Theorem 1. Let (E, B, H) be an ILP input, costE,B be a cost function, and h ∈H be an optimal hypothesis with respect to costE,B. Then there exists h′ ∈H such that h′ is a variant of h and all rules of h′ only contain safe variables. See the appendix for examples of rules that are body-variants of each other and only contain safe variables.

## 6 Implementation We demonstrate our idea in ASP with the ILP system POPPER (Cropper and Morel 2021; Cropper and

Hocquette 2023a).

Popper Our symmetry-breaking approach directly works with all variants of POPPERhopper,maxsynth,propper. For simplicity, we describe the basic version of POPPER.

POPPER uses a generate, test, combine, and constrain loop to find an optimal hypothesis (Definition 3) (the full algorithm is in the appendix). POPPER starts with an answer set program P. This program can be viewed as a generator program because each model (answer set) represents a hypothesis. The program P uses head (hlit/3) and body (blit/3) literals to represent a hypothesis. The first argument of each literal is the rule ID, the second is the predicate symbol, and the third is the literal variables, where 0 represents A, 1 represents B, etc. For instance, POPPER represents the rule f(A,B) ← tail(A,C), head(C,B) as a set with three atoms:

3Induction is performed over a finite total ordering towards a maximum element.

{hlit(0,f,(0,1)), blit(0,tail,(0,2)), blit(0,head,(2,1))} The program P contains choice rules for head and body literals:

{hlit(Rule,Pred,Vars)}:- rule(Rule), vars(Vars,Arity), hpred(Pred,Arity). {blit(Rule,Pred,Vars)}:- rule(Rule), vars(Vars,Arity), bpred(Pred,Arity). The literal rule(Rule) denotes rule indices. The literals hpred(Pred,Arity) and bpred(Pred,Arity) denote predicate symbols and arities that may appear in the head or body of a rule, respectively. The literal vars(Vars,Arity) denotes all possible variable tuples.

In the generate stage, POPPER uses an ASP system to find a model of P for a fixed hypothesis size, enforced via a cardinality constraint on the number of head and body literals. If no model is found, POPPER increments the hypothesis size and loops again. If a model exists, POPPER converts it to a hypothesis h (a definite program).

In the test stage, POPPER uses Prolog to test h on the training examples and background knowledge. If h entails at least one positive example and no negative examples, POPPER saves h as a promising program.

In the combine stage, POPPER searches for a combination (a union) of promising programs that entails all the positive examples and has minimal size. POPPER formulates the search as a combinatorial optimisation problem (Cropper and Hocquette 2023a), implemented in ASP as an optimisation problem. If a combination exists, POPPER saves it as the best hypothesis and updates the maximum hypothesis size.

In the constrain stage, POPPER uses h to build constraints, which it adds to P to prune models and thus prune the hypothesis space. For instance, if h does not entail any positive example, POPPER adds a constraint to prune its specialisations as they are guaranteed not to entail any positive example. For instance, the following constraint prunes all specialisations (supersets) of the rule f(A,B) ←tail(A,C), head(C,B):

:- hlit(R,f,(0,1)), blit(R,tail,(0,2)), blit(R,head,(2,1)).

POPPER repeats this loop using multi-shot solving (Gebser et al. 2019) and terminates when it exhausts the models of P or exceeds a user-defined timeout. It then returns the best hypothesis found.

Symmetry Breaking Encoding We now describe our ASP encoding E to break symmetries. We add E to the answer set program P used by POPPER to generate programs to prune unsafe rules and thus unsafe hypotheses.

The fact var member(Vars,V) denotes that variable V is a member of variable tuple Vars, e.g. var member((0,4,3),3). For every variable tuple xs, we sort the tuple to ys and add the fact ordered vars(xs,ys) to E. For instance, for the variable tuple (4,1,3), we add the fact ordered vars((4,1,3),(1,3,4)). These facts match ordered variables (Definition 9). We add facts to encode the lexicographic order over variable tuples (Definition 11). For instance, we add the facts lower((0,0,1),(0,0,2)) and lower((4,7,1),(4,8,2)). We add all skipped facts

19016

<!-- Page 6 -->

of the form skipped(Vars,V) to denote that the variable V is strictly between two variables A and B in an ordered variable tuple Vars, where V is not in Vars (Definition 12); these include, for instance, the facts skipped((0,1,3),2), skipped((1,3,5),2), and skipped((1,3,5),4). We add a rule to identify the ordered variable tuple of a selected body literal:

appears(Rule,OrderedVars):- blit(Rule,_,Vars), padded_vars(Vars,PaddedVars), ordered_vars(PaddedVars,OrderedVars). The literal padded vars(Vars,PaddedVars) performs prefix padding on variable tuples (Definition 10). For instance, assuming that the maximum arity of any literal is 4, for the variable tuple (4,1) we added the fact padded vars((4,1),(0,0,4,1)). We add a rule to identify witnessed variables (Definition 13):

witnessed(Rule,V,Vars1):- appears(Rule,Vars1), skipped(Vars1,V), lower(Vars2,Vars1), var_member(V,Vars2), appears(Rule,Vars2). Finally, we add a constraint to prune rules with unsafe variables 14):

:- body_var(Rule,V), appears(Rule,Vars), skipped(Vars,V), not witnessed(Rule,V,Vars).

Our symmetry-breaking encoding adds at most O(m · n2 · k) ground rules to the ASP solver, where m is the number of candidate rules in a hypothesis, n is the number of possible variable tuples, and k is the number of possible variables.

## 7 Experiments

To test our claim that pruning variants can reduce solving time, our experiments aim to answer the question:

Q1 Can symmetry breaking reduce solving time?

To answer Q1, we compare the solving time of POPPER with and without symmetry breaking.

To test our claim that pruning variants allows us to scale to harder tasks, our experiments aim to answer the question:

Q2 Can symmetry breaking reduce solving time when pro- gressively increasing the complexity of tasks?

To answer Q2, we compare the solving time of POPPER with and without symmetry breaking when varying the complexity of an ILP task.

Finally, the goal of breaking symmetries is to reduce solving time and, in turn, reduce learning time. Therefore, our experiments aim to answer the question:

Q3 Can symmetry breaking reduce learning time?

To answer Q3, we compare the learning time of POPPER with and without symmetry breaking.

## Experimental Setup

To answer Q1, we compare the solving time (time spent generating hypotheses) of POPPER with and without symmetry breaking. We use a solving timeout of 20 minutes per task. To answer Q2, we compare the solving time of POPPER with and without symmetry breaking on progressively harder ILP tasks by increasing the number of variables allowed in a rule4. We use a solving timeout of 60 minutes per task. For Q1 and Q2, the independent variable is whether POPPER uses symmetry breaking and the dependent variable is the solving time, which depends entirely on the independent variable. To answer Q3, we compare the learning time of POPPER with and without symmetry breaking. We use a learning timeout of 60 minutes per task. However, learning times are a function of many things, not only solving time. For instance, symmetry breaking could reduce solving time by 50% allowing POPPER to generate twice as many hypotheses but it also needs to test them. Therefore, learning time does not directly measure the impact of symmetry breaking. In other words, the dependent variable (learning time) does not entirely depend on the independent variable.

In all experiments, the runtimes include the time spent generating the symmetry-breaking rules. We round times over one second to the nearest second. We repeat all experiments 10 times. We plot and report 95% confidence intervals (CI). We compute 95% CI via bootstrapping when data is non-normal. To determine statistical significance, we apply either a paired t-test or the Wilcoxon signed-rank test, depending on whether the differences are normally distributed. We use the Benjamini–Hochberg procedure to correct for multiple comparisons. We use POPPER 4.4.0. We use an AWS m6a.16xlarge instance to run experiments where each learning task uses a single core.

Domains We use 449 learning tasks from several domains: 1D-ARC. This dataset (Xu et al. 2024) contains visual reasoning tasks inspired by the abstract reasoning corpus (Chollet 2019).

IGGP. The task is to induce rules from game traces (Cropper, Evans, and Law 2020) from the general game playing competition (Genesereth and Bj¨ornsson 2013).

IMDB. A real-world dataset which contains relations about movies (Mihalkova, Huynh, and Mooney 2007).

List functions. The goal of each task in this data (Rule et al. 2024) is to identify a function that maps input lists to output lists, where list elements are natural numbers.

Trains. The goal is to find a hypothesis that distinguishes east and west trains (Larson and Michalski 1977).

Zendo. An inductive game where players discover secret rules by building structures (Cropper and Hocquette 2023b).

Experimental Results

Q1. Can Symmetry Breaking Reduce Solving Time? Figure 2 shows the solving times of POPPER with and without symmetry breaking5. Significance tests confirm (p < 0.05) that symmetry breaking reduces solving times on 97/449 (22%) tasks and increases solving times on 1/449 (0%) tasks. There is no significant difference in the other tasks. The mean decrease in solving time is 178 ± 56 seconds. The median decrease is 20 seconds with 95% CI between 8 and 51 seconds. The mean and median increase is 41 seconds. Some

4Cropper and Morel (2021) show that the hypothesis space grows exponentially in the number of variables allowed in a rule.

5Detailed per-task results and corresponding improvements are in the appendix.

19017

<!-- Page 7 -->

improvements are substantial. For instance, for the sokobanterminal task, symmetry breaking reduces the solving time from 1075 ± 112 seconds to 59 ± 6 seconds. These are minimum improvements because POPPER without symmetry breaking often times out after 20 minutes. With a longer timeout, we would likely see greater improvements. Overall, the results show that symmetry breaking can drastically reduce solving time.

+5

0

-5

-10

-15

-20

Task

Solving time difference (minutes)

**Figure 2.** Solving time difference (minutes) with symmetry breaking. The tasks are ordered by improvement.

Q2. Can Symmetry Breaking Reduce Solving Time When Progressively Increasing the Complexity of Tasks? Figure 3 shows the solving times of POPPER with and without symmetry breaking on progressively harder ILP tasks. The results show that POPPER without symmetry breaking struggles to scale to harder tasks. Without symmetry breaking, the mean solving times when allowed to use 7, 8, or 9 variables in a rule are 125 ± 44, 1411 ± 310, and 3600 ± 0 seconds respectively. By contrast, with symmetry breaking, the mean solving times when allowed to use 7, 8, or 9 variables in a rule are 4 ± 0, 7 ± 0, and 17 ± 2 seconds respectively. In other words, for the hardest task, symmetry breaking reduces solving time from over an hour to only 17 seconds, a 99.5% reduction. Overall, the results show that symmetry breaking can reduce solving time when progressively increasing the complexity of tasks.

Q3. Can Symmetry Breaking Reduce Learning Time? Figure 4 shows the learning times of POPPER with and without symmetry breaking. Significance tests confirm (p < 0.05) that symmetry breaking reduces learning times on 128/449 (29%) tasks and increases learning times on 12/449 (3%) tasks. There is no significant difference in the other tasks. The mean decrease in learning time is 385 ± 109 seconds and the median is 54 seconds with 95% CI between 21 and 134 seconds. The mean increase is 192 ± 121 seconds and the median is 120 seconds with 95% CI between 54 and 266 seconds. These are minimum improvements because POPPER without symmetry breaking often times out after 60 minutes. With a longer timeout, we would likely see greater improvements. Overall, the results show that symmetry breaking can

5 6 8 9 0

20

40

60

Number of variables

Solving time (minutes)

Baseline Symmetry breaking

**Figure 3.** Solving times (minutes) of POPPER with and without (baseline) symmetry breaking on one trains task. We vary the number of variables allowed in a rule and thus the size of the hypothesis space.

drastically reduce learning time.

+20

0

-20

-40

-60

Task

Learning time difference (minutes)

**Figure 4.** Learning time difference (minutes) with symmetry breaking. The tasks are ordered by improvement.

## 8 Conclusions and Limitations

We introduced a symmetry-breaking method for ILP. We showed that determining whether two rules are body-variants (Definition 6) is graph isomorphism hard (Proposition 1). We described a symmetry-breaking approach to prune bodyvariant rules and implemented it in ASP. We proved that this approach is sound and only prunes body-variant rules (Proposition 2). We have experimentally shown on multiple domains, including visual reasoning and game playing, that our approach can drastically reduce solving time and learning time, sometimes from over an hour to only 17 seconds.

## Limitations

Our symmetry-breaking approach is incomplete, as complete symmetry-breaking is graph isomorphism hard (Proposition 1). Finding other efficient symmetrybreaking techniques is future work.

19018

<!-- Page 8 -->

## Acknowledgments

We thank Andreas Niskanen for early discussions about this work. Andrew Cropper was supported by his EPSRC fellowship (EP/V040340/1). David M. Cerna was supported by the Czech Science Foundation Grant 22-06414L and Cost Action CA20111 EuroProofNet. Matti Jarvisalo was supported by Research Council of Finland (grant 356046).

## References

Ahlgren, J.; and Yuen, S. Y. 2013. Efficient program synthesis using constraint satisfaction in inductive logic programming. J. Machine Learning Res., 14(1): 3649–3682. Aloul, F. A.; Markov, I. L.; and Sakallah, K. A. 2003. Shatter: efficient symmetry-breaking for boolean satisfiability. In Proceedings of the 40th Design Automation Conference, DAC 2003, Anaheim, CA, USA, June 2-6, 2003, 836–839. ACM. Anders, M.; Brenner, S.; and Rattan, G. 2024. Satsuma: Structure-Based Symmetry Breaking in SAT. In Chakraborty, S.; and Jiang, J. R., eds., 27th International Conference on Theory and Applications of Satisfiability Testing, SAT 2024, August 21-24, 2024, Pune, India, volume 305 of LIPIcs, 4:1– 4:23. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Arvind, V.; Das, B.; K¨obler, J.; and Toda, S. 2015. Colored Hypergraph Isomorphism is Fixed Parameter Tractable. Algorithmica, 71(1): 120–138.

Babai, L.; and Codenotti, P. 2008. Isomorhism of Hypergraphs of Low Rank in Moderately Exponential Time. In 2008 49th Annual IEEE Symposium on Foundations of Computer Science, 667–676. Babai, L.; and Luks, E. M. 1983. Canonical labeling of graphs. In Proceedings of the Fifteenth Annual ACM Symposium on Theory of Computing, STOC ’83, 171–183. New York, NY, USA: Association for Computing Machinery.

ISBN 0897910990. Bembenek, A.; Greenberg, M.; and Chong, S. 2023. From SMT to ASP: Solver-Based Approaches to Solving Datalog Synthesis-as-Rule-Selection Problems. Proc. ACM Program. Lang., 7(POPL). Blockeel, H.; and De Raedt, L. 1998. Top-Down Induction of First-Order Logical Decision Trees. Artif. Intell., 101(1-2): 285–297. Chollet, F. 2019. On the Measure of Intelligence. CoRR. Corapi, D.; Russo, A.; and Lupu, E. 2011. Inductive Logic Programming in Answer Set Programming. In ILP 2011. Crawford, J. M.; Ginsberg, M. L.; Luks, E. M.; and Roy, A. 1996. Symmetry-Breaking Predicates for Search Problems. In Aiello, L. C.; Doyle, J.; and Shapiro, S. C., eds., Proceedings of the Fifth International Conference on Principles of Knowledge Representation and Reasoning (KR’96), Cambridge, Massachusetts, USA, November 5-8, 1996, 148–159. Morgan Kaufmann. Cropper, A.; and Dumancic, S. 2022. Inductive Logic Programming At 30: A New Introduction. J. Artif. Intell. Res., 74: 765–850. Cropper, A.; Evans, R.; and Law, M. 2020. Inductive general game playing. Mach. Learn., 109(7): 1393–1434.

Cropper, A.; and Hocquette, C. 2023a. Learning Logic Programs by Combining Programs. In ECAI 2023 - 26th European Conference on Artificial Intelligence, volume 372, 501–508. IOS Press. Cropper, A.; and Hocquette, C. 2023b. Learning Logic Programs by Discovering Where Not to Search. In Thirty- Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, 6289–6296. AAAI Press. Cropper, A.; and Morel, R. 2021. Learning programs by learning from failures. Mach. Learn., 110(4): 801–856. Darga, P. T.; Liffiton, M. H.; Sakallah, K. A.; and Markov, I. L. 2004. Exploiting structure in symmetry detection for CNF. In Malik, S.; Fix, L.; and Kahng, A. B., eds., Proceedings of the 41th Design Automation Conference, DAC 2004, San Diego, CA, USA, June 7-11, 2004, 530–534. ACM. De Raedt, L. 2008. Logical and relational learning. ISBN 978-3-540-20040-6. De Raedt, L.; and Dehaspe, L. 1997. Clausal Discovery. Mach. Learn., 26(2-3): 99–146. Devriendt, J.; and Bogaerts, B. 2016. BreakID: Static Symmetry Breaking for ASP (System Description). CoRR, abs/1608.08447. Devriendt, J.; Bogaerts, B.; Bruynooghe, M.; and Denecker, M. 2016. On local domain symmetry for model expansion. Theory Pract. Log. Program., 16(5-6): 636–652.

Drescher, C.; Tifrea, O.; and Walsh, T. 2011. Symmetrybreaking answer set solving. AI Commun., 24(2): 177–194. Evans, R.; Hern´andez-Orallo, J.; Welbl, J.; Kohli, P.; and Sergot, M. J. 2021. Making sense of sensory input. Artif. Intell., 293: 103438. F¨urnkranz, J.; and Kliegr, T. 2015. A Brief Overview of Rule Learning. In RuleML 2015, volume 9202 of Lecture Notes in Computer Science, 54–69. Springer. Gal´arraga, L.; Teflioudi, C.; Hose, K.; and Suchanek, F. M. 2015. Fast rule mining in ontological knowledge bases with AMIE+. VLDB J., 24(6): 707–730. Garey, M. R.; and Johnson, D. S. 1979. Computers and Intractability: A Guide to the Theory of NP-Completeness. Gebser, M.; Kaminski, R.; Kaufmann, B.; and Schaub, T. 2019. Multi-shot ASP solving with clingo. Theory Pract. Log. Program., 19(1): 27–82. Genesereth, M. R.; and Bj¨ornsson, Y. 2013. The International General Game Playing Competition. AI Magazine, 34(2): 107–111. Hocquette, C.; Niskanen, A.; J¨arvisalo, M.; and Cropper, A. 2024. Learning MDL Logic Programs from Noisy Data. In Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI, 10553–10561. AAAI Press.

Junttila, T. A.; and Kaski, P. 2007. Engineering an Efficient Canonical Labeling Tool for Large and Sparse Graphs. In Proceedings of the Nine Workshop on Algorithm Engineering and Experiments, ALENEX 2007, New Orleans, Louisiana, USA, January 6, 2007. SIAM. Kaminski, T.; Eiter, T.; and Inoue, K. 2019. Meta-Interpretive Learning Using HEX-Programs. In IJCAI 2019, 6186–6190.

19019

<!-- Page 9 -->

K¨obler, J.; Sch¨oning, U.; and Tor´an, J. 1993. The Graph Isomorphism Problem: Its Structural Complexity. Progress in Theoretical Computer Science. Birkh¨auser/Springer. ISBN 978-1-4612-6712-6. Larson, J.; and Michalski, R. S. 1977. Inductive inference of VL decision rules. SIGART Newsletter, 63: 38–44. Law, M.; Russo, A.; and Broda, K. 2014. Inductive Learning of Answer Set Programs. In JELIA 2014. Lloyd, J. W. 2012. Foundations of logic programming. Springer Science & Business Media. McKay, B. D. 1981. Practical Graph Isomorphism. Congressus Numerantium, 30: 45–87. Mihalkova, L.; Huynh, T. N.; and Mooney, R. J. 2007. Mapping and Revising Markov Logic Networks for Transfer Learning. In AAAI 2007, 608–614. Muggleton, S. 1991. Inductive Logic Programming. New Generation Computing, 8(4): 295–318. Muggleton, S. 1995. Inverse Entailment and Progol. New Generation Comput., 13(3&4): 245–286. Plotkin, G. 1971. Automatic Methods of Inductive Inference. Ph.D. thesis, Edinburgh University. Quinlan, J. R. 1990. Learning Logical Definitions from Relations. Mach. Learn., 5: 239–266. Raedt, L. D.; and Ramon, J. 2004. Condensed Representations for Inductive Logic Programming. In Dubois, D.; Welty, C. A.; and Williams, M., eds., Principles of Knowledge Representation and Reasoning: Proceedings of the Ninth International Conference (KR2004), Whistler, Canada, June 2-5, 2004, 438–446. AAAI Press. Rule, J. S.; Piantadosi, S. T.; Cropper, A.; Ellis, K.; Nye, M.; and Tenenbaum, J. B. 2024. Symbolic metaprogram search improves learning efficiency and explains rule learning in humans. Nature Communications, 15(1): 6847. Sch¨uller, P.; and Benz, M. 2018. Best-effort inductive logic programming via fine-grained cost-based hypothesis generation - The inspire system at the inductive logic programming competition. Mach. Learn., 107(7): 1141–1169. Shapiro, E. Y. 1983. Algorithmic Program DeBugging. Cambridge, MA, USA. ISBN 0262192187. Srinivasan, A. 2001. The ALEPH manual. Machine Learning at the Computing Laboratory, Oxford University. Struyf, J.; and Blockeel, H. 2003. Query Optimization in Inductive Logic Programming by Reordering Literals. In Horv´ath, T., ed., Inductive Logic Programming: 13th International Conference, ILP 2003, Szeged, Hungary, September 29-October 1, 2003, Proceedings, volume 2835 of Lecture Notes in Computer Science, 329–346. Springer. Tamaddoni-Nezhad, A.; and Muggleton, S. H. 2009. The lattice structure and refinement operators for the hypothesis space bounded by a bottom clause. Mach. Learn., 76(1): 37–72. Tarzariol, A.; Gebser, M.; and Schekotihin, K. 2021. Lifting Symmetry Breaking Constraints with Inductive Logic Programming. In Zhou, Z., ed., Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI 2021, 2062–2068. ijcai.org.

Xu, Y.; Li, W.; Vaezipoor, P.; Sanner, S.; and Khalil, E. B. 2024. LLMs and the Abstraction and Reasoning Corpus: Successes, Failures, and the Importance of Object-based Representations. Trans. Mach. Learn. Res., 2024. Zeman, V.; Kliegr, T.; and Sv´atek, V. 2021. RDFRules: Making RDF rule mining easier and even more efficient. Semantic Web, 12(4): 569–602.

Zeng, Q.; Patel, J. M.; and Page, D. 2014. QuickFOIL: Scalable Inductive Logic Programming. VLDB, 197–208.

19020
