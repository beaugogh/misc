---
title: "Strategic Reasoning over Golog Programs in the Nondeterministic Situation Calculus"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38977
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38977/42939
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Strategic Reasoning over Golog Programs in the Nondeterministic Situation Calculus

<!-- Page 1 -->

Strategic Reasoning over Golog Programs in the Nondeterministic Situation Calculus

Giuseppe De Giacomo1,2, Yves Lesp´erance3, Matteo Mancanelli2

1University of Oxford, Oxford, UK 2University of Rome La Sapienza, Rome, Italy 3York University, Toronto, ON, Canada giuseppe.degiacomo@cs.ox.ac.uk, lesperan@eecs.yorku.ca, mancanelli@diag.uniroma1.it

## Abstract

We investigate the problem of synthesizing strategies that guarantee the successful execution of a high-level nondeterministic agent program in Golog within a nondeterministic first-order basic action theory, considering the environment as adversarial. Our approach constructs a symbolic program graph that captures the control flow independently of the domain, enabling strategy synthesis through the cross product of the program graph with the domain model. We formally relate graph-based transitions to standard Golog semantics and provide a synthesis procedure that is sound though incomplete (in general, the problem is undecidable, given that we have a first-order representation of the state). We also extend the framework to handle the case where the environment’s possible behaviors are specified by a Golog program.

## Introduction

(Levesque et al. 1997) introduced high-level program execution as a way of designing autonomous agents, which seeks a middle ground between planning and normal programming. Instead of looking for a plan/strategy to achieve a goal as in planning, the agent looks for a strategy to successfully execute a nondeterministic program that specifies its task. They proposed the Golog language for specifying such programs, which use constructs such as branches, loops, and nondeterministic choice, and are defined over atomic actions and fluent conditions that are specified by a Basic Action Theory (BAT) in the situation calculus (McCarthy and Hayes 1969; Reiter 2001). To find a strategy to execute the program, the agent needs to reason over the action theory. If the program is very deterministic, searching for a successful execution strategy is easy, but as more nondeterminism is introduced, the search becomes harder and begins to resemble planning.

The problem we address in this paper is a variant of the high-level program execution task, i.e., given a Golog program δ and an action theory D, find a strategy for executing δ that guarantees successful termination starting from the initial situation S0 in the domain specified by D. If the domain is deterministic and the program is situation determined, i.e., there is a unique remaining program after executing each step, such a strategy can simply specify a sequence of actions⃗a to execute such that D |= Do(δ, S0, do(⃗a, S0)), i.e.,

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

doing⃗a in the initial situation yields a complete execution of δ. If the domain is deterministic but the program is not situation determined, the strategy should also specify the remaining program after each action in the sequence.

In this paper, we instead consider the case where the domain is nondeterministic and specified by a nondeterministic basic action theory (De Giacomo and Lesp´erance 2021) (DL21). For a situation determined program δ, we want to synthesize a strategy f, i.e., a mapping from situations to actions, such that the agent can force the program to be executed to successful termination by following f, i.e., D |= AgtCanForce(δ, S0, f). If the program is not situation determined, we also need to generate a strategy to select the remaining program, i.e., a mapping g from situations to programs, such that D |= AgtCanForce(δ, S0, f, g). If, as is typical in FOND planning (Geffner and Bonet 2013; Ghallab, Nau, and Traverso 2016), we have complete information about the initial state, i.e., have a model M such that M |= D, then we need to generate a strategy f such that M |= AgtCanForce(δ, S0, f) in the situation determined program case; in the non-situation determined program case, we also need to generate a strategy g to chose the remaining program, such that M |= AgtCanForce(δ, S0, f, g).

Most prior work on Golog program execution (Baier, Fritz, and McIlraith 2007; Baier et al. 2008; Fritz, Baier, and McIlraith 2008) focuses on deterministic environments, compiling Golog into the domain so classical planners can be used. We instead target nondeterministic domains using a reactive synthesis approach. A recent advancement is (Hofmann and Claßen 2025) (HC25), which uses the C2 decidable fragment of FOL but suffers from scalability issues. Our framework is simpler and more intuitive, while offering formal guarantees that relate program executions with classical Golog semantics and synthesis techniques. Our framework is also very flexible, and it can easily be extended to accommodate different challenges. We will show how one can specify separate programs on the agent’s behavior and on the environment’s behavior; this contrasts with (HC25), which takes the Golog program as a constraint on the behavior of the whole system, i.e., both the agent and environment.

## Preliminaries

Nondeterministic situation calculus. The situation calculus is a predicate logic language designed for specifying

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19047

<!-- Page 2 -->

dynamically changing worlds. World changes result from performing actions, and world histories are modeled as situations, which are action sequences. The constant S0 denotes the initial situation, and the function do(a, s) denotes the successor situation after executing a in s. Fluents are predicates or functions varying with the situation, and take a situation term as their final argument. In this language, we define domains represented by a basic action theory (BAT), where successor state axioms (SSAs) represent the causal laws of the domain (Reiter 2001). A predicate Poss(a, s) is used to state that a is executable in s. We can rely on the mechanism of regression R (Pirri and Reiter 1999) to reduce reasoning about a given future situation to reasoning about S0.

(DL21) propose a simple extension of the situation calculus to handle nondeterministic actions. For any primitive action in a nondeterministic domain, there can be a number of different outcomes, depending on how the environment behaves. This is modeled by an additional environment reaction parameter e, ranging over a new sort Reaction. We call the reaction-suppressed version of the action a(⃗o) an agent action and the full version a(⃗o, e) a system action. A nondeterministic basic action theory (NDBAT) D is a special kind of BAT, and it is the union of the following disjoint sets: foundational, domain independent, axioms of the situation calculus (Σ), axioms describing the initial situation (DS0), unique name axioms for actions and domain closure for action types (Dca), successor state axioms describing how system actions change the fluents (Dssa), and system action precondition axioms, stating when the complete system action can occur (Dposs). One also specifies agent action preconditions using Possag. The theory must entail the reaction independence requirement (i.e., ∀e.Poss(a(⃗o, e), s) ⊃ Possag(a(⃗o), s)) and the reaction existence requirement (i.e., Possag(a(⃗o), s) ⊃∃e.Poss(a(⃗o, e), s)).

We assume finitely many primitive action types A and fluent predicates F, no functions beyond constants, and all object terms drawn from a countably infinite set N of standard names (Levesque and Lakemeyer 2001), with the unique name assumption and domain closure. We also assume that Reaction is a sub-sort of Object. This means that in all models of the theory, object domains are isomorphic and countably infinite, where each element of the domain is denoted by a syntactic term, and we can use ground terms to denote any value of a domain. More generally, this allows us to confuse wlog substitutions of ground terms and assignments, and ends interpret quantification substitutionally.

Golog syntax. Golog is a high-level language for writing programs that are executed over a (possibly nondeterministic) Basic Action Theory. We consider programs written in a variant of Golog where the test construct yields no transitions and is final when the condition is satisfied (Claßen and Lakemeyer 2008; De Giacomo, Lesp´erance, and Pearce 2010). The key feature of our variant is that programs instruct agent actions, rather than system actions. The syntax of Golog programs is as follows:

δ::= a(⃗o) | φ? | δ1; δ2 | δ1|δ2 | πx.δ | δ∗ where a(⃗o) is an agent action term, φ? tests that φ holds, δ1; δ2 is the sequential execution of δ1 and δ2, δ1|δ2 is the nondeterministic choice of δ1 and δ2, πx.δ executes program δ for some nondeterministic choice of the object variable x, and δ∗performs δ zero or more times. Note that φ is a situation-suppressed formula, and we denote by φ[s] the formula obtained by restoring the situation argument s into all fluents in φ. We use nil as an abbreviation for True? to denote the empty program.

Golog Semantics and Variable Environments. To construct the program graph of a given program δ0, we need to talk about the subprograms of δ0. This is captured by the concept of syntactic closure. Following (De Giacomo et al. 2016), we separate the program terms themselves from the assignments to pick variables (i.e., variables bound by π). Let us assume wlog that all pick variables are renamed apart and there is a predefined ordering on such variables. It is possible to define a n-tuple of object terms⃗x = ⟨x1,..., xn⟩, called the environment term, where xi is the current value of i-th pick variable of δ0. We denote the cartesian product of n objects as On, and the object assigned to variable z as xz. We use a triple (δ,⃗x, s) to denote a complete configuration. At the beginning of an execution, the environment term is arbitrarily instantiated, and at each step of the computation it maintains only n values, where n is the number of pick variables. Tracking pick variables’ values separately avoids enumerating all the possible instantiations of πx.δ, keeping the number of resulting subprograms finite. We can define inductively the syntactic closure Γδ0 of a program δ0: (i) δ0, nil ∈Γδ0, (ii) if δ1; δ2 ∈Γδ0 and δ′

1 ∈Γδ1, then δ′ 1; δ2 ∈ Γδ0 and Γδ2 ⊆Γδ0, (iii) if δ1 | δ2 ∈Γδ0, then Γδ1, Γδ2 ⊆ Γδ0, (iv) if πz.δ ∈Γδ0, then Γδ ⊆Γδ0, (v) if δ∗∈Γδ0 then δ; δ∗∈Γδ0 Theorem 1. The syntactic closure Γδ0 of a Golog program δ0 is linear in the size of δ0.

The semantics of Golog is specified as usual in terms of single-steps, using two predicates: Final, specifying that the program may terminate in a given situation, and Trans, specifying that one step of the program δ in situation s may lead to situation s′ with δ′ remaining to be executed. Differently from previous works, we define Trans and Final considering both the triple-based configuration version and the environment reactions as follows:

Trans(a,⃗x, s, δ′,⃗x′, s′) ≡∃e.Poss(a[⃗x](e), s) ∧ δ′ = nil ∧⃗x′ =⃗x ∧s′ = do(a[⃗x](e), s) Trans(φ?,⃗x, s, δ′,⃗x′, s′) ≡False Trans(δ1; δ2,⃗x, s, δ′,⃗x′, s′) ≡Trans(δ1,⃗x, s, δ′

1,⃗x′, s′)∧ δ′ = δ′

1; δ2 ∨Final(δ1,⃗x, s) ∧Trans(δ2,⃗x, s, δ′,⃗x′, s′) Trans(δ1|δ2,⃗x, s, δ′,⃗x′, s′) ≡Trans(δ1,⃗x, s, δ′,⃗x′, s′) ∨

Trans(δ2,⃗x, s, δ′,⃗x′, s′) Trans(πz.δ,⃗x, s, δ′,⃗x′, s′) ≡∃d.Trans(δ,⃗xz d, s, δ′,⃗x′, s′) Trans(δ∗,⃗x, s, δ′,⃗x′, s′) ≡Trans(δ,⃗x, s, δ′′,⃗x′, s′) ∧ δ′ = δ′′; δ∗

Final(a,⃗x, s) ≡False Final(φ?,⃗x, s) ≡φ[⃗x][s] Final(δ1; δ2,⃗x, s) ≡Final(δ1,⃗x, s) ∧Final(δ2,⃗x, s) Final(δ1|δ2,⃗x, s) ≡Final(δ1,⃗x, s) ∨Final(δ2,⃗x, s) Final(πz.δ,⃗x, s) ≡∃d.Final(δ,⃗xz d, s) Final(δ∗,⃗x, s) ≡True

19048

<!-- Page 3 -->

where a[⃗x] and φ[⃗x] denotes the action term a and formula φ obtained by replacing all free pick variables with the object terms to which they are bound in⃗x, and⃗xz d denotes the environment term obtained by replacing the element corresponding to the pick variable z with d.

We use Trans∗to denote the reflexive transitive closure of Trans, i.e., Trans∗(δ,⃗x, s, δ′,⃗x′, s′) means that there exists a sequence of one-step transitions taking the configuration (δ,⃗x, s) into the configuration (δ′,⃗x′, s′). We use also an adapted version of the notion of situation determined (SD) programs (De Giacomo, Lesp´erance, and Muise 2012):

SituationDetermined(δ,⃗x, s).=

∀s′, δ′, δ′′,⃗x′,⃗x′′.Trans∗(δ,⃗x, s, δ′,⃗x′, s′) ∧

Trans∗(δ,⃗x, s, δ′′,⃗x′′, s′) ⊃δ′ = δ′′ ∧⃗x′ =⃗x′′

Now, we have guarantees that all programs that δ0 can evolve into according to Trans and Final, must be in its syntactic closure Γδ0.

Lemma 2. Let D be an NDBAT over which δ0 is executed and M a model of D. If δ ∈Γδ0 and M |= Trans(δ,⃗x, s, δ′,⃗ x′, s′), then δ′ ∈Γδ0.

Proof. It follows directly from the recursive definition of Trans and the construction of Γδ0.

Lemma 3. Let D be an NDBAT over which δ0 is executed and M a model of D. If M |= Trans∗(δ0,⃗x0, s0, δ,⃗x, s), then δ ∈Γδ0.

Proof (sketch). By induction on the number of steps in the derivation of Trans∗(δ0,⃗x0, s0, δ,⃗x, s).

Example. A service robot must deliver a cup of coffee from the kitchen k to some offices officeA, officeB, and so on. The doors between the kitchen and the rooms are locked, and the robot must press a button to request that a door be opened. Which door opens is under the control of the environment. We assume the agent can execute the following actions: Pickup (grab a coffee), PutDown (place the currently held coffee), PressButton(e), (request to open some door, where the environment chooses the door via the environment reaction e = openOffice r), and MoveTo(r) (move to room r). Note that when it is not explicit, we assume an action has only one environment reaction Success. The fluents we need tell us where the agent is (At(r)), if the agent has grabbed a coffee (HasCoffee), if the coffee has been delivered (Delivered(r)), and if the door is open (DoorOpen(r)). The action preconditions and effects are as expected (e.g., the agent can move to a given office only if the corresponding door is open). For brevity, we use DeliverTo(r).= MoveTo(r); PutDown; MoveTo(k), and also φ(r).= DoorOpen(r) ∧¬Delivered(r). The agent program to deliver coffee is δ = (Pickup; (PressButton; ∃r.φ(r)?)∗; πr.φ(r)?; DeliverTo(r))∗; ∀r.Delivered(r)?, that is, the agent picks up coffee, repeatedly presses the button, and each time delivers coffee to an office with an open door that has not yet been served (if any). We assume the environment cannot act “unfairly”, i.e. eventually every door will be opened. A counter associated with the button prevents the environment from opening the same door infinitely often. The fluent CanOpen(r) indicates if the door can still be opened, i.e. the counter has not reached its bound.

First-Order Program Graphs We aim at performing transition system (TS)-based synthesis for generating a strategy compliant with a given Golog program. Synthesis can be viewed as a 2-player game among agent and environment (this is common also when dealing with temporal properties and reactive synthesis; see (Abadi, Lamport, and Wolper 1989; Pnueli and Rosner 1989)). Here we construct the game arena by considering both the FOND domain where the agent is acting and the program graph, whose paths represent executions of the specified Golog program. In this section, we show how the program graphs are constructed and what their properties are.

Constructing the Program Graph. Inspired by (Claßen 2013; Claßen and Lakemeyer 2008), we construct the program graph of a Golog program δ0, characterizing all possible executions of δ0 conditioned on the domain, which we do not fix until later. The program graph is thus a symbolic structure that captures the control flow semantics of Golog at the syntactic level, decoupled from domain dynamics, which are only integrated later via the cross product with the domain. Each node of the graph corresponds to a program in the syntactic closure of δ0 (i.e., a possible remaining program in the execution of δ0) and each edge is a guarded onestep transition from such a program to the remaining one.

We define properties of the nodes and relationships among them based on Trans and Final. Since we keep the pick operator, the program graph must capture all execution paths of the Golog program parametrized over the pick variables. In particular, pick variables are unbounded parameters of actions and tests, and no evaluation or binding can be performed before performing the cross product with the domain. Thus, we have to keep track of the pick variables for which we must assign a value of the domain. Specifically, we define two new relations T and F in a recursive way:

T(a, a) = {(Poss(a), ∅, nil)} T(a, b) = {} T(φ?, a) = {} T(δ1; δ2, a) =

{(¬F(δ1) ∧φ, P, δ′

1; δ2) | (φ, P, δ′ 1) ∈T(δ1, a)} ∪ {(F(δ1) ∧φ, P, δ′

2) | (φ, P, δ′ 2) ∈T(δ2, a)} T(δ1|δ2, a) = T(δ1, a) ∪T(δ2, a) T(πz.δ, a) = {(φ, P ∪z, δ′) | (φ, P, δ′) ∈T(δ, a)} T(δ∗, a) =

{(¬F(δ) ∧φ, P, δ′; δ∗) | (φ, P, δ′) ∈T(δ, a)}

F(a) = False F(φ?) = φ F(δ1; δ2) = F(δ1) ∧F(δ2) F(δ1|δ2) = F(δ1) ∨F(δ2) F(πz.δ) = ∃z.F(δ) F(δ∗) = True Given a Golog program δ and and action a, T(δ, a) returns a set of triples (φ, P, δ′), where φ is a guard condition representing the cases in which the transition can be performed,

19049

<!-- Page 4 -->

δ0 = (Pickup; (PressButton; ∃r.ϕ(r)?)∗; πr.∃r.ϕ(r)?; DeliverTo(r))∗; ∀r.Delivered(r)?

δ1 = nil; (PressButton; ∃r.ϕ(r)?)∗;

πr.∃r.ϕ(r)?; DeliverTo(r); δ0 δ2 = nil; δ0

Pickup PressButton

{r}, DeliverTo Pickup

**Figure 1.** Program graph for the coffee-delivery robot.

P is the set of pick variables to be instantiated, and δ′ is the remaining program; F(δ) is the condition under which δ may terminate successfully. Note that φ is always a Boolean condition over the predicate Poss(a) and formulas in tests from δ and it is closed under conjunction and disjunction operators. Note also that neither φ nor F can be evaluated at this stage, because this would require knowing the domain.

Now, we can provide a definition for the program graph.

Definition 4. Let δ0 be a Golog program. The corresponding program graph is G = ⟨Φ × 2V × A, Q, q0, τ, L⟩, where

• Φ × 2V × A is the alphabet, with Φ a boolean formula over tests and Poss and V the set of pick variables • Q = Γδ0 is the syntactic closure of δ0 • q0 = δ0 is the initial program • τ(q, φ, P, a, q′) iff (φ, P, q′) ∈T(q, a) • L(q) = F(q) is a label assigned to q

Example Cont. The program graph corresponding to the coffee-delivery program previously introduced is represented in Figure 1 (guards are omitted for clarity). Note that the transition from the subprogram after PressButton depends on which door was opened by the environment, captured symbolically by a guarded transition of the form τ(q, DoorOpen(r) ∧ ¬Delivered(r), {r}, MoveTo(r), q′).

## Results

about Program Graphs. We now summarize key properties of the program graph used to symbolically encode the structure of Golog programs. Unless otherwise specified, we will write G for the program graph of a given Golog program δ0, D for the NDBAT over which δ0 is executed and M for a model of D. First, we can talk about the dimensions of the program graph:

Theorem 5. The number of nodes and the number of edges in G are linear in the size of δ0.

Proof. By Theorem 1, the number of subprograms in Γδ0 is linear in the size of δ0, which bounds the number of nodes in G. Each node generates only a constant number of transitions, so the number of edges is also linear.

We also relate program graphs with Golog’s operational semantics. In particular, symbolic transitions in the graph correspond to executable transitions in the model, and vice versa, provided guard conditions are satisfied, and F(δ) characterizes the same terminating configurations as Final.

Theorem 6. For all subprograms δ, δ′ ∈Γδ0, environment terms⃗x,⃗x′, agent action a, and situations s:

1. If τ(δ, φ, P, a, δ′) ∈G, ∀z̸ ∈P.x′ z = xz and M |= φ[⃗x′][s], then there exists a reaction e such that M |= Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)). 2. For every reaction e, if M |= Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)), then there exists φ s.t. τ(δ, φ, P, a, δ′) ∈ G, ∀z̸ ∈P.x′ z = xz, and M |= φ[⃗x′][s].

Proof (sketch). We proceed by structural induction on the syntax of δ. The base case is δ = a, where the graph contains τ(a, Poss(a), ∅, a, nil). By the semantics of Trans and the reaction existence/independence properties, M |= Poss(a)[⃗x][s] iff there exists e s.t. M |= Trans(a,⃗x, s, nil,⃗ x, do(a[⃗x](e), s)). All other constructs follow because the graph mimics the structure of the Trans rules.

Theorem 7. For all subprograms δ ∈Γδ0, environment terms⃗x and situations s, M |= Final(δ,⃗x, s) iff M |= F(δ)[⃗x][s].

Proof (sketch). We proceed by structural induction on δ. For δ = a, both Final(δ,⃗x, s) and F(δ) are False. For δ = φ? they are both φ, respectively. For compound constructs, F(δ) is built to match the structure of Final(δ,⃗x, s), and the result follows from the inductive hypothesis.

Now, we can prove that a full execution trace to a final configuration exists in the model if and only if there is a corresponding path in the program graph.

Theorem 8. Let (δ0,⃗x0, s0) be an initial configuration. Then, we have that M |= Trans∗(δ0,⃗x0, s0, δ,⃗x, s) ∧ Final(δ,⃗x, s) iff there is a sequence of transitions τ(q0, ϕ1, P1, a1, q1), τ(q1, ϕ2, P2, a2, q2)...τ(qn−1, ϕn, Pn, an, qn) in G, environment terms x0,..., xn and reactions e1,..., en such that q0 = δ0, qn = δ,⃗xn =⃗x and s = sn, and for each i = 1,..., n, (i) ∀z̸ ∈Pi, x′ i,z = xi,z, (ii) si = do(ai[xi](ei), si−1), (iii) M |= ϕi[xi][si−1], and (iv) M |= F(qn)[xn][sn].

Finally, if we have a SD program, then the symbolic transition relation becomes functional.

Theorem 9. Suppose that δ0 is SD in S0 wrt D. For any transitions τ(q, φ1, P, a, q′

1) and τ(q, φ2, P, a, q′ 2) in G, if there exists⃗x,⃗x′ and s such that ∀z̸ ∈P.x′ z = xz and M |= φ1[⃗x′][s] ∧φ2[⃗x′][s], then q′

1 = q′ 2.

Proof (sketch). Suppose two transitions from q in G for the same action a lead to q′

1 and q′ 2, and both guards are satisfied in M under the same⃗x and s. By Theorem 6, both transitions correspond to valid Trans steps. Since the program is situation-determined, executing a from (q,⃗x, s) must yield a unique successor configuration, so q′

1 = q′ 2.

Thus, if δ0 is situation determined in S0 wrt D, the characteristic graph becomes deterministic, and we can replace the relation τ(q, φ, P, a, q′) by the function τ(q, φ, P, a) = q′.

19050

<!-- Page 5 -->

Synthesis and Strategic Reasoning. We now turn to the problem of synthesizing strategies that allow an agent to successfully execute a Golog program in the presence of adversarial nondeterminism. Building on the symbolic program graphs introduced earlier, we integrate these with a model of the domain to define a game arena over which synthesis can be carried out.

TS-based Synthesis for First Order Domains We adopt a transition system–based synthesis approach, where the program graph and the domain model are combined into a game structure that encodes the agent-environment interaction. Consider a nondeterministic domain DM = ⟨2F, A, s0, ρ, α⟩where:

• 2F is the set of states, with s0 ∈2F the initial state • α(s) ⊆A represents action preconditions • ρ(s, a, s′) with a ∈α(s) is the transition relation

Note that for any NDBAT D and model M |= D, there is a corresponding nondeterministic domain DM. We can define a game arena constructed by the cross product of the program graph G and the nondeterministic domain. Definition 10. Let δ0 be a program and DM a ND domain. The cross product is a tuple:

⟨A × Q × On × 2F,Q × On × 2F,(δ0,⃗x0, s0),Tr,Fin⟩ where

• A × Q × On × 2F is the alphabet • Q × On × 2F is a set of states • (δ0,⃗x0, s0) is the initial state • Tr((δ,⃗x, s), (a, δ′,⃗xP, s′)) = (δ′,⃗x′, s′) is the transition function where (i) ∃φ.τ(δ, φ, P, a, δ′), (ii) ∀z̸ ∈ P.x′ z = xz and ∀z ∈P.x′ z = xP z, (iii) s |= φ[⃗x′], and (iv) ρ(s, a[⃗x′], s′) • Fin = {(δ,⃗x, s) | s |= F(δ)[⃗x]} is the set of final states This can be viewed as a game arena with alphabet Σ = A × Q × On × 2F, where the agent controls the action A, the remaining program Q, and the binding of the pick variables On, and where the environment controls the next state 2F. A game strategy is a function κ: G →A × Q × On mapping states of the game g ∈G to agent actions, remaining programs, and bindings for the pick variables. The set of plays induced by a game strategy κ in the game arena A, Play(κ, A), is the set of all plays g0, g1,... ∈Gω such that g0 is the initial state of A and there exists an environment state s′ such that Tr(gi, (κ(gi), s′)) = gi+1. A game strategy κ is winning in A if, for every play g0, g1,... in Play(κ, A), there exists some i such that Fin(gi).

Agent Control and Strategic Reasoning.1 In order to represent the ability of the agent to execute an agent program in a ND domain, (DL21) introduce AgtCanForceBy(δ, f, s) as an adversarial version of Do in presence of environment reactions. This predicate states that strategy f, a function from situations to agent actions (including the special action stop), executes SD Golog agent program δ in situation s considering its nondeterminism angelic, as in the standard Do,

1These results can be extended to non-SD programs.

but also considering the nondeterminism of environment devilish/adversarial. Here is a version of AgtCanForceBy that considers the presence of an environment term⃗x:

AgtCanForceBy(δ,⃗x, f, s).= ∀P.[... ⊃P(δ,⃗x, s)]

where... stands for [f(s) = stop ∧Final(δ,⃗x, s) ⊃P(δ,⃗x, s)] ∧ [∃a.(f(s) = a̸ = stop ∧ ∃e.∃δ′.∃⃗x′.Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)) ∧ ∀e.(∃δ′.∃⃗x′.Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s))) ⊃ ∃δ′.∃⃗x′.Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)) ∧ P(δ′,⃗x′, do(a[⃗x′](e), s)) ⊃P(δ,⃗x, s)]

We say that predicate AgtCanForce(δ,⃗x, s) holds iff there exists a strategy f s.t. AgtCanForceBy(δ,⃗x, f, s) holds. Theorem 11. For any SD program δ0, subprogram δ ∈Γδ0, environment term⃗x, situation s and strategy f, we have that:

M |= AgtCanForceBy(δ,⃗x, f, s) iff (δ,⃗x, s) is in the least set Pµ such that if f(s)=stop ∧M |= Final(δ,⃗x, s), then (δ,⃗x, s) ∈Pµ if f(s)=a, a̸ = stop and there exists e, δ′, and⃗x′ s.t.

M |= Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)) and for all e the existence of δ′ and⃗x′ s.t. M |= Trans(δ,⃗x, s, δ′,⃗x′, do(a[⃗x′](e), s)) implies (δ′,⃗x′, do(a[⃗x′](e), s)) ∈Pµ, then (δ,⃗x, s) ∈Pµ iff (δ,⃗x, s) is in the least set Pµ such that if f(s)=stop and M |= F(δ)[⃗x][s], then (δ,⃗x, s) ∈Pµ if f(s)=a, a̸ = stop and there exists φ, δ′, and⃗x′ s.t.

τ(δ, φ, P, a, δ′), for all z not in P, x′ z = xz and M |= φ[⃗x′][s], and for all e the existence of δ′ and⃗x′ s.t. τ(δ, φ, P, a, δ′) and M |= φ[⃗x′][s] implies that (δ′,⃗x′, do(a[⃗x′](e), s)) is in Pµ, then (δ,⃗x, s) ∈Pµ

Proof. This follows directly from Theorems 6 and 7.

Finally, the next result shows that the existence of a winning strategy in the game arena means that the agent is able to execute the program starting from the initial situation in the underlying situation calculus model. Theorem 12. Let δ0 be a SD Golog program, D an NDBAT, M a model of D, DM the nondeterministic domain corresponding to M, and A the game arena generated by δ0 and DM. Then M |= AgtCanForce(δ0,⃗x, S0) iff there exists a winning strategy in A.

Proof (sketch). The agent can force successful execution in the model iff there is a strategy s.t. all executions lead to a final configuration. The executions correspond to paths in the game arena that reach a final state. Hence, the strategy exists iff there is a winning strategy in the arena.

Example Cont. In the coffee delivery domain, the agent aims to ensure that every office eventually receives a cup of coffee, despite not controlling which door opens after each button press. The synthesis problem consists of coming up with a strategy f such that the agent can force the successful termination of the program δ from an initial situation S0 where no coffee has been delivered yet. A valid strategy repeatedly executes the PressButton action until some room r satisfies both DoorOpen(r) and ¬Delivered(r), at which

19051

<!-- Page 6 -->

point it moves to r and delivers the coffee. The nondeterminism due to the environment’s control is handled by the agent’s loop structure, which scans for a suitable target once the environment has revealed an open room.

Fixpoint Verification Procedure. To implement the predicate AgtCanForceBy in practice, one can adopt a sound symbolic fixpoint procedure that explores the executions of the agent program under all possible environment reactions. (De Giacomo, Lesp´erance, and Pearce 2010, 2016) present such a procedure for verifying first-order (FO) µ-ATL properties (Alur, Henzinger, and Kupferman 2002; Bradfield and Stirling 2007) over game structures. In particular, they develop a procedure [[Ψ]] for verifying a property Ψ by labeling nodes in a program graph, leveraging regression and fixpoint approximates (Tarski 1955).

Here, we want to verify AgtCanForce, which can be defined as a least fixpoint formula in their logic. The labeling of a program graph G is denoted by Z and produces a set {⟨δ, ϕ⟩| δ ∈G} where each node δ is associated with a FO formula ϕ that characterizes the situations s and environment terms⃗x in which AgtCanForce(δ,⃗x, s) is satisfied, i.e., the situations starting from which the agent can execute δ by following a certain strategy. We call a configuration (δ,⃗x, s) winning if we have a formula ϕ that guarantees AgtCanForce for that configuration, i.e. D |= ϕ(s), and if we fix δ and⃗x, a strategy is winning if the configuration (δ,⃗x, s) is winning.

For each program, we need to compute the formula ϕ that captures all the configurations that are winning for AgtCanForce, and we can proceed iteratively knowing that if in configuration (δ,⃗x, s) the agent can execute an action such that all possible resulting configurations (δ′,⃗x′, s′) are winning, then (δ,⃗x, s) is also winning. We can attempt to verify AgtCanForce by a least fixpoint procedure that iteratively generates better approximations of the labeling.

The least fixpoint approximation procedure is given by:

Z ←[[False]] Znew ←Final(Z) ∨PreAdv(Z) while(Z̸ = Znew) {

Z ←Znew Znew ←Final(Z) ∨PreAdv(Z)}

where we use Z̸ = Znew as an abbreviation for Dca̸ |= V

⟨δ,ϕ⟩∈Z,⟨δ,ϕnew⟩∈Znew ϕ ≡ϕnew. Now we just need to define the adversarial preimage of Z:

PreAdv(Z) = {⟨δ, ϕ⟩| δ ∈G and ϕ = W τ(δ,φ,P,a,q′)∈G,⟨q′,ϕ′⟩∈Z ∃⃗xP.[∀z̸ ∈P.x′ z = xz ∧∀z ∈P.x′ z = xP z ] ∧ φ[⃗x′] ⊃∀e ∈React.R(ϕ′[do(a[⃗x′](e), s)])} where R is one-step regression applied to the labels. Intuitively, PreAdv computes the set of configurations from which the agent can take an action s.t. all environment reactions lead to winning configurations. Note that, in general, the procedure is incomplete due to undecidability and the infiniteness of FO domains. Termination can be ensured by restricting to the propositional setting, to a decidable fragment of FOL or to the bounded situation calculus (De Giacomo, Lesp´erance, and Patrizi 2016; De Giacomo et al. 2021).

Theorem 13. Let (δ0, x0, S0) be an initial configuration. If the labeling procedure terminates and ⟨δ0, ϕ⟩is in the returned set, then D |= AgtCanForce(δ0, x0, S0) if and only if DS0 ∪Dca |= ϕ[S0].

Proof (sketch). By induction on the fixpoint construction. The labeling procedure mirrors the characterization of AgtCanForce (Thm 11), using Final for base cases and PreAdv to propagate winning configurations. Soundness follows from the correctness of these constructions.

Using Programs to Constrain the Environment Handling Environment Programs. Our framework naturally extends to scenarios where the environment’s behavior is constrained by its own program. We assume that the environment program contains only one action, namely DoReaction, taking the reaction e selected by the environment as a parameter, and that it can refer to the current action selected by the agent, which is denoted by the special symbol ac. Here, we need to adapt the semantics of the programs and define Trans and Final for both the agent program, denoted δa, and the environment program, denoted δe. Below is a sketch of Transa and Transe:

Transa(a,⃗x, s, δ′ a,⃗x′, a) ≡ Possag(a[⃗x], s) ∧δ′ = nil ∧⃗x′ =⃗x Transa(φ?,⃗x, s, δ′ a,⃗x′, a) ≡False...

Transe(DoReaction(e),⃗x, a, s, δ′ e,⃗x′, e) ≡ Poss(a(e), s) ∧δ′ e = nil ∧⃗x′ =⃗x Transe(φ?,⃗x, a, s, δ′ e,⃗x′, e) ≡False...

Transa is the same as in the original definition, but it has the action selected by the agent a as its last parameter instead of the next situation s′; Transe is similar, but it takes as input the agent action a and selects the environment reaction e (because the reaction depends on the action chosen by the agent), and again drops s′. Finala and Finale are equal to the original definition, except that Finale has a among its parameters, and in the final condition for tests we substitute the symbol ac with the actual action a:

Finale(DoReaction(e),⃗x, a, s) ≡False Finale(φ?,⃗x, a, s) ≡φ[⃗x, ac/a][s]...

Finally, system transitions result from the interleaved execution of the agent program and the environment program:

Trans(δa,⃗x, δe,⃗y, s, δ′ a,⃗x′, δ′ e,⃗y′, s′) ≡ Transa(δa,⃗x, s, δ′ a,⃗x′, a) ∧ Transe(δe,⃗y, a[⃗x′], s, δ′ e,⃗y′, e) ∧ s′ = do(a[⃗x′](e), s)

A final configuration is reached when both programs have terminated:

Final(δa,⃗x, δe,⃗y, s) ≡

Final(δa,⃗x, s) ∧Final(δe,⃗y, a, s)

Note that we could easily construct a program graph for the environment programs, and if we compute the cross

19052

<!-- Page 7 -->

product between the program graph of δa and the program graph of δe, we still obtain a program graph. It means that everything we have shown carries over even in this setting. This leads to a joint fixpoint definition of agent-environment interaction. We extend the predicate AgtCanForceByIf to capture whether an agent strategy f can enforce the successful execution of δa in the presence of an adversarial but constrained environment running δe.

AgtCanForceByIf (δa,⃗x, δe,⃗y, f, s).=

∀P.[... ⊃P(δa,⃗x, δe,⃗y, s)], where... stands for [(f(s) = stop ∧Final(δa,⃗x, s)) ⊃P(δa,⃗x, δe,⃗y, s)] ∧ [∃a.(f(s) = a̸ = stop ∧∃e.∃⃗x′,⃗y′.∃δ′ a, δ′ e. Trans(δa,⃗x, δe,⃗y, s, δ′ a,⃗x′, δ′ e,⃗y′, do(a[⃗x′](e), s)) ∧ ∀e.∀⃗y′.(∃δ′ a, δ′ e.∃⃗x. Trans(δa,⃗x, δe,⃗y, s, δ′ a,⃗x′, δ′ e,⃗y′, do(a[⃗x′](e), s)) ⊃ P(δ′ a,⃗x′, δ′ e,⃗y′, do(a[⃗x′](e), s)) ⊃P(δa,⃗x, δe,⃗y, s)]

We can use an analogous fixpoint procedure as before to do synthesis for this.

Example Cont. In our running example, the environment program can specify how the environment selects which door to open in response to the robot’s PressButton action. In general, the environment reaction will be Success if the action is not PressButton, and it will be door to be opened (openOfficeA, openOfficeB,...) otherwise:

δe = (((πx.ac̸ = PressButton ∧x = Success?;

DoReaction(x))∗); (πy.ac = PressButton ∧CanOpen(y)?;

DoReaction(y)))∗

As explained before, we ensure the environment not to be “unfair” using the fluent CanOpen, which prevents the environment from maintaining a door closed indefinitely.

## Discussion

We have presented a general approach for strategic reasoning over high-level agent programs in the situation calculus, focusing on the first-order nondeterministic setting, where programs constrain the behaviors of both the agent and the environment. This is related to the broader problem of planning with domain control knowledge (DCK), where traditional goal specifications are replaced by procedural, action-centric descriptions that express preferences over the manner in which goals are achieved. (Baier, Fritz, and McIlraith 2007; Baier et al. 2008) addressed this challenge by compiling DCK and temporally extended user preferences into planning problem instances, thereby ensuring that only action sequences adhering to the procedural constraints are generated. They proved how Golog-like programs can be translated into PDDL, enabling the use of domain-independent heuristic planners. (Fritz, Baier, and McIlraith 2008) extended this compilation approach to Con- Golog, a variant of Golog that supports explicit concurrency between programs.

In the case of Golog, the progression of procedural control knowledge is modeled using a nondeterministic finite automaton with ϵ-transitions (ϵ-NFA), where ϵ denotes a transition that does not consume any action. However, the environment remains entirely unconstrained, which significantly limits the ability to model realistic scenarios involving adversarial or unpredictable behavior. Moreover, only angelic nondeterminism originating from favorable program choices is considered, while devilish nondeterminism, stemming from hostile environmental influences, is not captured. Consequently, their frameworks are not suitable for modeling or reasoning about adversarial environments.

Our framework is also related to the work of (HC25), which investigates a game-theoretic approach to synthesizing strategies for agents whose behavior is guided by a Golog program and constrained by an LTLf temporal specification. In their approach, a finite game arena is constructed that encodes all possible executions of the Golog program under environment nondeterminism, while concurrently tracking the satisfaction of the LTLf temporal goal. To guarantee decidability, they restrict the underlying basic action theories to C2 (Gradel, Otto, and Rosen 1997; Zarrieß and Claßen 2016), a decidable two-variable fragment of FOL, and similarly constrain the temporal formulas by substituting propositions with quantifier-free C2 first-order formulas. While these restrictions ensure computational tractability, they significantly limit the expressive power of the framework.

Although their work provides an important contribution toward bridging agent programming with temporal logic synthesis, its applicability is limited to very simple scenarios. The experimental evaluation offers a proof-of-concept but reveals substantial scalability challenges. In contrast, our framework is capable of addressing substantially more complex domains while being simpler and more natural. We provide formal results on the relation between the execution paths in the program graph and Golog transition semantics (that can be translated also to characteristic graphs), and between TS-based synthesis and agent’s ability to execute a program in a first-order domain, as well as a fixpoint evaluation procedure for performing synthesis. Furthermore, they use Golog programs as constraints for the entire system, while our approach is more flexible and richer since it includes distinct programs constraining the agent and the environment, opening to possible extension to multi-agent system settings.

Golog provides procedural task specifications to contrast with declarative ones such as LTLf/LDLf (De Giacomo and Vardi 2013, 2015). When the object domain is finite and the initial state is known, our method is sound and complete. Its cost is polynomial in the game arena, which in turn is polynomial in the initial program, whereas LTLf/LDLf synthesis is 2EXPTIME in general. A natural direction for future work is therefore to investigate finite-state settings and apply concrete synthesis algorithms, enabling a direct comparison between procedural programs and temporally extended specifications like LDLf.

Another possible direction is to explore alternative ways of constraining the environment, for instance by using LTL trace constraints as in (De Giacomo, Lesp´erance, and Mancanelli 2025), where an LTL formula Cstr is imposed on environment behaviours and AgtCanForceByIf is defined to express that an agent can force δ along all paths satisfying Cstr when following f from s.

19053

<!-- Page 8 -->

## Acknowledgments

This work has been supported by the ERC Advanced Grant WhiteMech (No. 834228), the PRIN project RIPER (No. 20203FFYLK), the PNRR MUR project FAIR (No. PE0000013), the UKRI Erlangen AI Hub on Mathematical and Computational Foundations of AI (No. EP/Y028872/1), the Italian National Ph.D. on Artificial Intelligence at Sapienza University of Rome, the National Science and Engineering Research Council of Canada, and York University.

## References

Abadi, M.; Lamport, L.; and Wolper, P. 1989. Realizable and Unrealizable Specifications of Reactive Systems. In ICALP, volume 372 of Lecture Notes in Computer Science, 1–17. Springer. Alur, R.; Henzinger, T. A.; and Kupferman, O. 2002. Alternating-time temporal logic. Journal of the ACM (JACM), 49(5): 672–713. Baier, J. A.; Fritz, C.; Bienvenu, M.; and McIlraith, S. A. 2008. Beyond Classical Planning: Procedural Control Knowledge and Preferences in State-of-the-Art Planners. In AAAI, 1509–1512. Baier, J. A.; Fritz, C.; and McIlraith, S. A. 2007. Exploiting Procedural Domain Control Knowledge in State-of-the-Art Planners. In ICAPS, 26–33. Bradfield, J.; and Stirling, C. 2007. 12 Modal mu-calculi. Studies in logic and practical reasoning, 3: 721–756. Claßen, J. 2013. Planning and Verification in the agent language Golog. Ph.D. thesis, RWTH Aachen University. Claßen, J.; and Lakemeyer, G. 2008. A Logic for Non- Terminating Golog Programs. In KR, 589–599. De Giacomo, G.; Felli, P.; Logan, B.; Patrizi, F.; and Sardina, S. 2021. Situation Calculus for Controller Synthesis in Manufacturing Systems with First-Order State Representation. Artif. Intell. De Giacomo, G.; and Lesp´erance, Y. 2021. The Nondeterministic Situation Calculus. In KR, 216–226. De Giacomo, G.; Lesp´erance, Y.; and Mancanelli, M. 2025. Situation Calculus Temporally Lifted Abstractions for Generalized Planning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 14848–14857. De Giacomo, G.; Lesp´erance, Y.; and Muise, C. J. 2012. On supervising agents in situation-determined ConGolog. In AAMAS, 1031–1038. IFAAMAS. De Giacomo, G.; Lesp´erance, Y.; and Patrizi, F. 2016. Bounded situation calculus action theories. Artif. Intell., 237: 172–203. De Giacomo, G.; Lesp´erance, Y.; Patrizi, F.; and Sardina, S. 2016. Verifying ConGolog programs on bounded situation calculus theories. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 30. De Giacomo, G.; Lesp´erance, Y.; and Pearce, A. R. 2010. Situation Calculus-Based Programs for Representing and Reasoning about Game Structures. Proc. of KR, 445–455.

De Giacomo, G.; Lesp´erance, Y.; and Pearce, A. R. 2016. Situation Calculus Game Structures and GDL. In ECAI, volume 285 of Frontiers in Artificial Intelligence and Applications, 408–416. IOS Press. De Giacomo, G.; and Vardi, M. Y. 2013. Linear Temporal Logic and Linear Dynamic Logic on Finite Traces. In Ijcai, volume 13, 854–860. De Giacomo, G.; and Vardi, M. Y. 2015. Synthesis for LTL and LDL on Finite Traces. In IJCAI, 1558–1564. AAAI Press. Fritz, C.; Baier, J. A.; and McIlraith, S. A. 2008. Congolog, sin trans: Compiling congolog into basic action theories for planning and beyond. In Proceedings of the Eleventh International Conference on Principles of Knowledge Representation and Reasoning, 600–610. Geffner, H.; and Bonet, B. 2013. A Concise Introduction to Models and Methods for Automated Planning. Morgan & Claypool. Ghallab, M.; Nau, D.; and Traverso, P. 2016. Automated planning and acting. Cambridge University Press. Gradel, E.; Otto, M.; and Rosen, E. 1997. Two-variable logic with counting is decidable. In Proceedings of Twelfth Annual IEEE Symposium on Logic in Computer Science, 306– 317. IEEE. Hofmann, T.; and Claßen, J. 2025. LTLf Synthesis on First- Order Agent Programs in Nondeterministic Environments. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 14976–14986. Levesque, H. J.; and Lakemeyer, G. 2001. The logic of knowledge bases. Mit Press. Levesque, H. J.; Reiter, R.; Lesp´erance, Y.; Lin, F.; and Scherl, R. B. 1997. GOLOG: A Logic Programming Language for Dynamic Domains. Journal of Logic Programming, 31: 59–84. McCarthy, J.; and Hayes, P. J. 1969. Some Philosophical Problems From the Standpoint of Artificial Intelligence. Machine Intelligence, 4: 463–502. Pirri, F.; and Reiter, R. 1999. Some contributions to the metatheory of the situation calculus. Journal of the ACM (JACM), 46(3): 325–361. Pnueli, A.; and Rosner, R. 1989. On the synthesis of a reactive module. In Proceedings of the 16th ACM SIGPLAN- SIGACT symposium on Principles of programming languages, 179–190. Reiter, R. 2001. Knowledge in Action. Logical Foundations for Specifying and Implementing Dynamical Systems. The MIT Press. Tarski, A. 1955. A lattice-theoretical fixpoint theorem and its applications. Pacific Journal of Mathematics. Zarrieß, B.; and Claßen, J. 2016. Decidable verification of Golog programs over non-local effect actions. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 30.

19054
