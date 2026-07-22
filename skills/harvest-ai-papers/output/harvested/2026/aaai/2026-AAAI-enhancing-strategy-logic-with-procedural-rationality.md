---
title: "Enhancing Strategy Logic with Procedural Rationality"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38991
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38991/42953
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Enhancing Strategy Logic with Procedural Rationality

<!-- Page 1 -->

Enhancing Strategy Logic with Procedural Rationality

Ruiqi Jin1, Shuyi Li2, Yongmei Liu1*

1Department of Computer Science, Sun Yat-sen University, Guangzhou 510006, China 2School of Mathematics (Zhuhai), Sun Yat-sen University, Zhuhai 519082, China {jinrq7, lishy277}@mail2.sysu.edu.cn, ymliu@mail.sysu.edu.cn

## Abstract

ATL and Strategy Logic (SL) are important languages for representation and reasoning about strategic abilities of coalitions in multi-agent systems. In analyzing strategies of agents in multi-agent systems, an important concept to consider is rationality. Strategy Logic can express rationality concepts such as Nash Equilibrium (NE). Recently, there has been work on logics for joint abilities incorporating rationality concepts based on iterated elimination of dominated strategies (IEDS). Each of NE and IEDS has its strengths and limitations. However, when the payoff is binary, e.g., whether a goal is satisfied, IEDS has more distinguishing power than NE. In this work, we propose Strategy Logic with IEDS (SLIEDS), an extension of Strategy Logic with an IEDS operator, where we can reason about rational strategies that survive IEDS. We prove that SLIEDS is strictly more expressive than SL. Finally, we prove that model checking memoryless SLIEDS is EXPTIME-complete.

## Introduction

Logics for strategic abilities in multi-agent systems is an active research field in knowledge representation and reasoning. One of the fundamental works proposed is Alternating-time Temporal Logic (ATL/ATL∗) (Alur, Henzinger, and Kupferman 2002), where formula ⟨⟨A⟩⟩ψ specifies that coalition A has a collective strategy to achieve temporal goal ψ, where ψ is a Linear Temporal Logic (LTL) formula. Strategy Logic (SL) (Chatterjee, Henzinger, and Piterman 2010; Mogavero et al. 2014) extends ATL∗ with explicit quantification on strategies, e.g., the formula ∃x.∀y.∃z.(1, x)(2, y)(3, z)ψ means that there exists a strategy of agent 1 s.t. for all strategies of agent 2 there exists a strategy of agent 3 that can achieve the goal ψ. This provides more expressive power than ATL∗, as in the latter the only allowed quantification alterations are ∃∀or ∀∃. This makes SL very expressive in representing strategic abilities.

In analyzing strategies of agents in multi-agent systems, an important concept to consider is rationality. A rational agent chooses the best action to achieve her goal given her knowledge or beliefs about the world and the other agents.

*Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

However, ATL ignores the issue of rationality. For example, two cars have a joint strategy to avoid collision by both staying still, but this joint strategy is not rational given their goals to reach the destinations. In game theory (Osborne and Rubinstein 1994), there are two common concepts of rationality: Nash Equilibrium (NE) and Iterative Elimination of Dominated Strategies (IEDS). NE represents outcome rationality, while IEDS represents procedural rationality. In general, each of NE and IEDS has its strengths and limitations. For example, NE doesn’t specify how to arrive at an equilibrium, while IEDS fails in games without dominated strategies. However, when it comes to the situation where the payoff is binary, e.g., whether a goal is satisfied, IEDS has more distinguishing power than NE. To give a simple example, consider two agents trying to cooperate and achieve a goal: Both agents 1 and 2 have two strategies a and b, and (a, a) is the only joint strategy that cannot achieve the goal. Then any joint strategy other than (a, a) is a NE, but only (b, b) is preferred by IEDS. The properties and algorithmic complexities of IEDS are thoroughly studied (Berwanger 2007; Pauly 2016). It is well known that SL can express NE; however, SL cannot express IEDS due to its procedural property. There is other literature on procedural or bounded rationality (Simon 1955; Russell and Wefald 1991; Gigerenzer, Todd, and the ABC Research Group 2000), which consider bounded or procedural rationality as how the agents choose strategies under informational or computational limits.

Nonetheless, rational strategic reasoning has received considerable attention. Works along this line can be put into two groups. The first group is strategy verification and synthesis. Wooldridge et al. (2016) introduces rational verification, concerning whether a given temporal logic formula is satisfied in some or all equilibrium computations of a multi-agent system, where each agent has a goal specified with a temporal logic formula. Kupferman, Perelli, and Vardi (2016) thoroughly investigates rational synthesis under different rationality concepts in cooperative and noncooperative settings. Aminof et al. (2021) explores besteffort synthesis, which synthesizes non-dominated strategies to achieve LTL goals. Gutierrez et al. (2021) investigates the problem of verification of strict ϵ Nash equilibria, where agents have both an LTL goal and an additional goal to minimize cost. Gutierrez et al. (2023) considers rational verification of mean-payoff games and provides improved

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

19169

<!-- Page 2 -->

complexity results. Recently, Hyland et al. (2024) studies rational verification problem in a setting where agents have quantitative probabilistic goals. The second group is strategic logics, mostly extending ATL. Bulling, Jamroga, and Dix (2008) extends ATL with multiple operators, which enable reasoning about agents that only play strategies satisfying certain rational properties, including Nash Equilibria and non-dominated strategies. Gutierrez, Harrenstein, and Wooldridge (2014; 2017) proposes a logic containing operator [NE]ψ, meaning ψ holds on all NE computations. Lorini (2016) proposes a modal logic for interactive epistemology to reason about game-theoretic solution concepts in normal form games. Huang and Ruan (2017) extends ATL with modalities CE▷◁w

G ψ, meaning group G has collective strategies in the form of correlated equilibria with utilitarian value ▷◁w. Liu et al. (2020) proposes a modal logic JAADL for joint abilities by extending ATL∗with an operator (A)∞ ψ φ, meaning φ holds after IEDS w.r.t. group A and goal ψ. Li, Lorini, and Mittelmann (2025) extends coalition logic and ATL with minimal rationality modalities ⟨⟨C⟩⟩ratψ for existence of non-dominated strategies to achieve ψ.

In this paper, we enhance Strategy Logic with procedural rationality, and propose Strategy Logic with IEDS (SLIEDS). We choose IEDS because it is a profoundly important and highly influential notion of procedural rationality. Following JAADL, we extend SL with operators for elimination of dominated strategies (EDS) [π]φ and IEDS [π]∞φ, which means φ holds after EDS and IEDS, respectively, w.r.t. goals specified with π. Different from JAADL and similar to rational verification (Wooldridge et al. 2016), different agents can have different goals, represented using formulas, which allows us to reason about non-cooperative settings. We prove that adding only the EDS operator to SL does not increase its expressiveness. We also prove that adding the IEDS operator to SL makes it strictly more expressive. To this end, we construct two classes of models such that there is a SLIEDS formula to distinguish between them, but no SL formula can do so. Note that our definition of SLIEDS and expressiveness results apply to both memoryless and memoryful cases. Finally, we prove that modelchecking memoryless SLIEDS is EXPTIME-complete. This complexity is higher than model-checking memoryless SL, which is PSPACE-complete (ˇCerm´ak et al. 2018). To prove the non-trivial EXPTIME-hardness result, we first show that IEDS on payoff matrices succinctly represented with circuits is EXPTIME-hard, and then reduce it to model-checking memoryless SLIEDS.

## Preliminaries

In this section, we introduce SL, and define the concept of strategy space, which is needed for defining our logic.

Let AP be a finite non-empty set of atomic propositions, Ac a finite non-empty set of actions, and Ag a finite nonempty set of agents. Definition 1. A concurrent game structure (CGS) is a tuple G = ⟨W, L, P, τ, w0⟩, where

• W is a finite non-empty set of states; w0 ∈W is the initial state; L: W →2AP is a labeling function; For w1 w2 w0 w4 w3 (pass, pass)

(stop, pass)

(pass, stop)

(, pass)

(pass,)

(stop,) (, stop)

(stop, stop)

(,)

(,)

**Figure 1.** The intersection formalized as a CGS.

each agent i, Pi: W →2Ac specifies a non-empty set of its available actions at each state; • A decision at state w is a function mapping each agent i to an action from Pi(w). The state transition function τ maps a state w and a decision d at w to a new state.

Example 1 (Crossing road (Li, Lorini, and Mittelmann 2025)). Two vehicles, vehicle 1 and vehicle 2, approch an intersection and both want to go straight. Vehicles can choose to pass or stop. If one of the vehicles chooses to pass, while the other one chooses to stop, then the moving vehicle can cross the road safely and win. However, if both of the vehicles deside to pass at the same time, then the two vehicles will crash. In the CGS, atomic proposition wini denotes that i reached its goal, crash denotes that the two vehicle crash. Aside from initial state w0 where both vehicles don’t cross the intersection, we have four states: w1, where 1 stops; w2, where 2 stops; w3, where both pass successfully; and w4, where both pass at the same time and crashed. We formalize the CGS shown in Figure 1, where:

• Ag = {1, 2}, Ac = {pass, stop}, and AP = {win1, win2, crash}; W = {w0, w1, w2, w3, w4}; • L(w0) = ∅, L(w1) = {win2}, L(w2) = {win1}, L(w3) = {win1, win2}, L(w4) = {crash}; • Pi(w) = Ac for i = 1, 2 and all w ∈W; • τ is defined as in Figure 1. Definition 2. A history h in a CGS G is a finite state sequence w0w1... wn. We let h[i] be the ith state wi on the history, and last(h) be wn. Definition 3. A computation λ in a CGS G is an infinite state sequence w0w1.... We let λ[i] be the ith state wi on the computation. Definition 4 (Strategies). A memoryless strategy on a CGS G is a function σ: W →Ac. A memoryful strategy on a CGS G is a function σ: W ∗→Ac. We denote the set of all memoryless strategies Strr, the set of all memoryful strategies StrR. We use Str to range over Strr and StrR. Example 2 (Strategies in the crossing road game). Consider the CGS in Example 1. There are in general two kinds of memoryless strategies that may lead to winning:

• Strategy σp, where σp(w0) = pass, i.e., to pass first. • Strategy σs, where σs(w0) = stop, σs(w1) = σs(w2) = pass, i.e., to stop before the intersection and wait after the other vehicle passes.

19170

<!-- Page 3 -->

If both agents adopt the same strategy σp, it will result in a crash. Both agents adopting σs will not lead in to a crash, but a traffic obstruction: no one can win as the CGS is stuck in w0. They will safely pass the intersection if one chooses σp, and the other σs.

In the case of memoryful strategies, both vehicles stopping at w0 does not inevitably lead to a traffic obstruction, as agents can pass after some amount of time. Still, a crash may happen if the two agents pass at the same time.

We define the notion of executable strategies, and introduce the concept of strategy spaces. Definition 5 (Executablility). A memoryless strategy σ is executable for an agent i, if for all w ∈W we have σ(w) ∈ Pi(w). A memoryful strategy is executable for an agent i, if for all h ∈W ∗we have σ(h) ∈Pi(last(h)). We denote the set of all memoryless (resp. memoryful) executable strategies of agent i as Strr i (resp. StrR i). Definition 6. A strategy space Σ on a CGS is a function that maps each agent i to a subset of Stri. The full strategy space Σf on a CGS maps each agent i to Stri.

We now define the notion of an agent strategy assignment, which assigns a set of agents their executable strategies. Definition 7. An agent strategy assignment α is a partial function from Ag to Str. An agent strategy assignment is defined on a set A ⊆Ag of agents, if i ∈A iff α(i)̸ = ⊥. An agent strategy assignment α is restricted to a strategy space Σ if for all i s.t. α(i)̸ = ⊥, we have α(i) ∈Σ(i). Given an agent strategy assignment α, an agent i, and σ ∈Str ∪{⊥}, α[i 7→σ] denotes the assignment that maps i to σ and is otherwise equal to α.

We denote the set Ag −{i} as −i, and Ag −A as −A. Definition 8 (Outcome). A state w and an agent strategy assignment α defined on Ag determine a unique computation. We call this computation the outcome of w and α, and denote it as out(w, α).

We introduce SL as in (Mogavero et al. 2014). The definition is slightly modified, in which we use two seperate assignments to assign agents and strategy variables. Let StV be a countable non-empty set of strategy variables. We give the syntax of SL. Definition 9 (SL syntax). We define the syntax of SL formula φ as follows:

φ::= p | ¬φ | φ1 ∧φ2 | Xφ | φ1Uφ2 | ∃s.φ | (i, s)φ, where p ∈AP, i ∈Ag, and s ∈StV.

Intuitively, strategy quantification ∃s means “there exists a strategy s”, while agent binding (i, s) means “bind agent i to strategy s”. We use ⊤for true and ⊥for false. Standard abbreviations including F and G are defined as usual. Definition 10. The set of free agents and variables of an SL formula φ, denoted free(φ), is defined inductively as follows (omitting cases of ¬ and ∧):

• free(p) = ∅; free(Xφ) = Ag ∪free(φ); • free(φ1Uφ2) = Ag ∪free(φ1) ∪free(φ2); • free(∃s.φ) = free(φ) −{s};

• free((i, s)φ) = (free(φ) ∪{s}) −{i} if i ∈free(φ); • free((i, s)φ) = free(φ) if i /∈free(φ);

A formula φ is a sentence if free(φ) = ∅.

Definition 11. A variable strategy assignment χ: StV → Str maps each strategy variable to a strategy. For a variable strategy assignment χ, a strategy variable s and a strategy σ, χ[s 7→σ] is the variable strategy assignment that maps s to σ and is otherwise equal to χ.

Definition 12 (SL Semantics). Given a CGS G, a state w, a variable strategy assignment χ, an agent strategy assignment α defined on Ag, we define the semantics of SL formulas inductively as follows (omitting cases of ¬ and ∧):

• G, w ⊨χ,α p if p ∈L(w). • G, w ⊨χ,α ∃s.φ if there exists a strategy σ ∈Str s.t. G, w ⊨χ[s7→σ],α φ. • G, w ⊨χ,α (i, s)φ if χ(s) ∈ Stri, and we have G, w ⊨χ,α[i7→χ(s)] φ. • G, w ⊨χ,α Xφ if G, out(w, α)[1] ⊨χ,α φ. • G, w ⊨χ,α φ1Uφ2 if there exists k ∈ N s.t. G, out(w, α)[k] ⊨χ,α φ2 and for all i < k, we have G, out(w, α)[i] ⊨χ,α φ1.

For a sentence φ we omit χ and α and write G, w ⊨φ.

Given agents i1,..., in and their respective goals φ1,..., φn, SL can express the existence of deterministic Nash equilibra (Mogavero et al. 2014), with the formula ∃s1... ∃sn.(i1, s1)... (in, sn)φnd, where φnd states that all agents have no intention to deviate from the joint strategy represented by (s1,..., sn): φnd is the conjunction of formulas (∃y.(ik, y)φk) →φk for k = 1,..., n. We denote this formula with ∃NE(φ1,..., φn).

Syntax and Semantics of SLIEDS In this section, we propose Strategy Logic with IEDS (SLIEDS). We introduce its syntax and semantics, compare it to related logics, and analyze valid formulas in the logic.

JAADL extends ATL∗with operators (A)ψφ and (A)∞ ψ φ, meaning φ holds after EDS and IEDS, respectively, w.r.t. group A and goal ψ. Inspired by JAADL, we extend SL with strategy elimination and iterated elimination operators, written as [π] and [π]∞respectively. Different from JAADL and similar to rational verification (Wooldridge et al. 2016), different agents can have different goals, specified with the goal expression π. This allows us to reason about noncooperative settings.

Definition 13 (SLIEDS Syntax). We define the syntax of SLIEDS formula φ and goal expression π as follows:

φ::= p | ¬φ | φ1 ∧φ2 | Xφ | φ1Uφ2 |

∃s.φ | (i, s)φ | [π]φ | [π]∞φ, π::= ε | π, (i: φ), where p ∈AP, i ∈Ag, and s ∈StV.

SLIEDS formulas φ have an SL-like syntax, with temporal modalities X and U, strategy quantifier ∃s and agent binding operator (i, s). The two new operators are the operator [π]

19171

<!-- Page 4 -->

for elimination of dominated strategies (EDS) and the operator [π]∞for IEDS. The goal expression π in these operators denotes the goal of each agent, which is used to define the strategy dominance relation for the agent. For example, the pair (i: φ) means agent i holds the goal φ.

We also define abbreviations for the elimination operators: [π]2φ:= [π][π]φ, and similarly for [π]kφ. We also write π in abbreviation: We omit pairs like (i: ⊤), and combine agents with the same goal into a coalition. For example, with Ag = {1, 2, 3, 4}, we write (1: φ1), (2: φ1), (3: φ2), (4: ⊤) as ({1, 2}: φ1), (3: φ2) or (1, 2: φ1), (3: φ2).

Similarly to SL, we can define the set of free agents and variables in a formula. Definition 14. The set of free agents and variables of SLIEDS formulas is defined as follows: free([π]φ) = free(φ); free([π]∞φ) = free(φ); and for other types of formulas, the definitions are the same as in SL. An SLIEDS formula φ is a sentence if free(φ) = ∅.

In order to define the semantics of SLIEDS, we need to interpret the goal expression π. We begin so by defining goal assignments. Definition 15. A goal assignment goal maps each agent i to an SLIEDS formula φ. The formula goal(i) is called agent i’s goal. For a goal assignment goal and an SLIEDS formula φ, goal[i 7→φ] is the goal assignment that maps agent i to φ and is otherwise equal to goal. The default goal assignment goal0 maps each agent to ⊤.

The goal assignment maps each agent to her goal. Intuitively, every goal expression π denotes a goal assignment. We interpret a goal expression π as a goal assignment in the following way: Definition 16. The goal expression π is evaluated inductively as follows: [[ε]] = goal0; [[π1, (i: φ)]] = [[π1]][i 7→φ].

Finally, we define semantics of SLIEDS. The interpretation of SLIEDS formulas is defined w.r.t. a strategy space. We define two strategy space reduction operators Rπ,w,χ(Σ) and R∞ π,w,χ(Σ), which mean the reduction of Σ via EDS and IEDS, respectively. The definitions of the interpretation of formulas and the reduction operators are mutually inductive. Thus the following definition is long, consisting of 3 parts. Definition 17 (SLIEDS Semantics). We define the interpretation of SLIEDS formulas and the strategy space reduction operators R and R∞mutually inductively as follows:

(1) Given a CGS G, a state w, a strategy space Σ, a variable strategy assignment χ, an agent strategy assignment α defined on Ag, the interpretation of SLIEDS formulas is inductively defined as follows (omitting cases of ¬ and ∧):

• G, w, Σ ⊨χ,α p if p ∈L(w). • G, w, Σ ⊨χ,α ∃s.φ if there exists a strategy σ ∈Str s.t. G, w, Σ ⊨χ[s7→σ],α φ. • G, w, Σ ⊨χ,α (i, s)φ if χ(s) ∈Σ(i), and we have G, w, Σ ⊨χ,α[i7→χ(s)] φ. • G, w, Σ ⊨χ,α [π]φ if G, w, Rπ,w,χ(Σ) ⊨χ,α φ. • G, w, Σ ⊨χ,α [π]∞φ if G, w, R∞ π,w,χ(Σ) ⊨χ,α φ. • G, w, Σ ⊨χ,α Xφ if G, out(w, α)[1], Σ ⊨χ,α φ.

• G, w, Σ ⊨χ,α φ1Uφ2 if there exists k ∈ N s.t. G, out(w, α)[k], Σ ⊨χ,α φ2 and for all i < k, we have G, out(w, α)[i], Σ ⊨χ,α φ1.

For a sentence φ we omit χ and α and write G, w, Σ ⊨φ.

(2) We now define the domination relation between strategies. We begin with the notion of the compatible set M of a strategy. Given a goal expression π, an agent i, a state w, a variable assignment χ, a strategy space Σ, and σ ∈Σ(i), the compatible set of σ w.r.t. π, i, w, χ, Σ, written Mπ,i,w,χ,Σ(σ), is the set of agent strategy assignments defined on −i and restricted to Σ that can work with σ to satisfy agent i’s goal [[π]](i) at w w.r.t. χ, i.e., for all agent strategy assignments α defined on −i and restricted to Σ, α ∈Mπ,i,w,χ,Σ(σ) iff G, w, Σ ⊨χ,α[i7→σ] [[π]](i).

For strategies σ, σ′ ∈Σ(i), we write σ ≥π,i,w,χ,Σ σ′ if Mπ,i,w,χ,Σ(σ) ⊇Mπ,i,w,χ,Σ(σ′). Additionally, we write σ >π,i,w,χ,Σ σ′ if Mπ,i,w,χ,Σ(σ) ⊃Mπ,i,w,χ,Σ(σ′), and we say σ dominates σ′ in Σ w.r.t. π, i, w, χ.

(3) The reduction of a strategy space Σ w.r.t. goal π, state w, and variable assignment χ, written Rπ,w,χ(Σ), is defined as follows: For all strategy σ ∈Σ(i), σ ∈Rπ,w,χ(Σ)(i) iff there is no σ′ ∈Σ(i) s.t. σ′ >π,i,w,χ,Σ σ. Note that if agent i has goal ⊤, then no strategy of i dominates another, thus Rπ,w,χ(Σ)(i) = Σ(i). For k ≥2, we define Rk π,w,χ(Σ) = Rπ,w,χ(Rk−1 π,w,χ(Σ)). Finally, we define the iterated reduction in the following way: For each agent i ∈Ag, R∞ π,w,χ(Σ)(i) = T∞ k=0 Rk π,w,χ(Σ)(i).

Definition 18 (Payoff matrix). Given a CGS G, a state w, a strategy space Σ, a goal formula φ, a variable strategy assignment χ, the payoff matrix, denoted PG,w,Σ,φ,χ, is a Boolean matrix with indices labeled by agent strategy assignments α defined on Ag and restricted to Σ such that for all such α, PG,w,Σ,φ,χ(α) = 1 iff G, w ⊨χ,α φ. We omit the subscripts of P if there is no ambiguity.

Finally, we use the Crossing road example to illustrate the EDS and IEDS operators of SLIEDS.

Example 3. We focus on the memoryless case, and consider three situations where agents have different goals. The payoff matrices of the three situations are given in Table 1.

First, both agents have the safety goal of never crash, denoted φs:= G¬crash. Then the formula [(1, 2: φs)]∀x.∀y.(1, x)(2, y)φs holds. It says that after a single EDS, any remaining joint strategies achieve the goal. This is because: as can be easily seen from Table 1a, for each agent, the strategy σs dominates σp, which is thus eliminated.

Second, besides the safety goal, each agent also has the liveness goal of reaching the destination, denoted φl i:= Fwini for i = 1, 2. Then the formula [(1: φs ∧φl

1), (2: φs ∧φl

2)]∀x.∀y.(1, x)(2, y)(φs ∧φl 1 ∧φl 2) does not hold. As can be seen from Table 1b, no strategy can be eliminated, and if both agents choose σs or both choose σp, the joint goal cannot be achieved.

Third, suppose that according to the law, vehicle 1 should yield the right of way, i.e., it should let vehicle 2 go first. We modify our language and the CGS to reflect it:

• Let illegal1, illegal2 ∈AP; • Let illegal1 ∈L(w2) and illegal1 ∈L(w4).

19172

<!-- Page 5 -->

(a)

σp σs σp 0, 0 1, 1 σs 1, 1 1, 1 (b)

σp σs σp 0, 0 1, 1 σs 1, 1 0, 0

(c)

σp σs σp 0, 0 0, 1 σs 1, 1 0, 0

**Table 1.** Payoff matrices of the situations in Example 3. Agent 1 (resp. 2) adopts row (resp. column) strategies.

Here, atom illegali represents i breaks the law. We assume the agents have goal πlegal:= (1: φs ∧φl

1 ∧ G¬illegal1), (2: φs ∧φl

2 ∧G¬illegal2). From Table 1c, for agent 1, σp will be dominated by σs and is eliminated; Yet, for agent 2, neither strategy dominates the other. Thus the formula [πlegal]∀x.∀y.(1, x)(2, y)(φs∧φl

1∧φl 2) does not hold. However, the formula [πlegal]∞∀x.∀y.(1, x)(2, y)(φs ∧φl

1 ∧φl 2) holds. This is because: in the second round of EDS, and agent 2’s σs is eliminated. With agent 1 does σs and agent 2 does σp, the joint goal is achieved.

We now compare SLIEDS to JAADL and ATL with minimal rationality of (Li, Lorini, and Mittelmann 2025). We show that a fragment of JAADL can be translated to SLIEDS. Aside from the EDS and IEDS operators, JAADL introduces action atoms and regular expressions, which are not expressible in SL. We name as JAATL the fragment of JAADL, which is the extension of ATL∗with the operators (A)ψφ and (A)∞ ψ φ. Then JAATL can be translated to SLIEDS as follows: In the base case, we use the translation from ATL∗ to SL. In the induction case, we have tr((A)ψφ) = [(A: tr(ψ))]tr(φ), and similarly for the IEDS operator.

Li, Lorini, and Mittelmann (2025) extends coalition logic and ATL with minimal rationality modalities ⟨⟨C⟩⟩ratψ for existence of non-dominated strategies to achieve ψ, where the domination relation between strategies is defined according to a total preorder on computations of the CGS. In comparison, our logic has a couple of advantages: First, they only consider EDS, while we consider both EDS and IEDS. Secondly, our definition of domination between strategies is defined via specifying goals for agents, which is in line with works of rational verification (Wooldridge et al. 2016), and we think this way is more natural and easier. Finally, ours allows to reason in the same formula about different domination relations specified via different goal expressions.

Finally, We discuss valid formulas in SLIEDS. Liu et al. (2020) analyzed valid formulas in JAADL (Propositions 1- 4). When these valid formulas are in JAATL, their translation to SLIEDS are valid, too. Additionally, we have:

Proposition 1. The following formulas are valid:

• [π]k(φ1 →φ2) →([π]kφ1 →[π]kφ2), k ∈N ∪{∞}. • ¬[π]kφ ↔[π]k¬φ, k ∈N ∪{∞}.

Moreover, some relations between NE and IEDS can be represented as valid formulas in SLIEDS. An example is the property that if after IEDS all remaining strategy profiles can w0 w1 w2 ∆ Dc\∆

(a1, a1)

(a1, a1)

**Figure 2.** CGSes in C1 and C2.





1 1 1 1 1 1 1 1 1 1 1









1 1 1 1 1 1 1 1 1 1 1





**Figure 3.** Payoff matrices of G1

3(left) and G2 3(right).

achieve both agents’ goals, then there exists a Nash Equilibrium in the original game, as shown below:

Proposition 2. Let Ag = {1, 2}, π be (1: φ1),(2: φ2), where φ1, φ2 are SLIEDS formulas. Then, [π]∞(φ∃∧φ∀) →∃NE(φ1, φ2) is valid, where φ∀is ∀x1∀x2 (1, x1)(2, x2) (φ1 ∧φ2), φ∃is ∃x1∃x2(1, x1)(2, x2)(φ1 ∧φ2), and ∃NE(φ1, φ2) is the formula expressing the existence of an NE w.r.t. goals φ1 and φ2.

Expressiveness Comparison In this section, we compare the expressive power of SLIEDS to its fragments. We prove that SL is as expressive as SLEDS, i.e., SL with only the EDS operator, while SLIEDS is strictly more expressive than SL. Our proofs apply to both memoryless and memoryful cases.

We first present the classic definition of expressive power.

Definition 19. Let L1 and L2 be two logics interpreted over the same classes of models M. We say that L2 is at least as expressive as L1, written L1 ⪯e L2, if for every formula φ1 ∈L1, there exists a formula φ2 ∈L2 s.t. for every model M ∈M, we have M ⊨φ1 iff M ⊨φ2.

Theorem 3. SL =e SLEDS.

Proof Sketch. To show that SLEDS can be translated to SL, it suffices to prove that the formula [π]φ with no EDS operator in its subformulas can be expressed in SL. For each agent binding subformula (i, x)φ1 of φ, we write a formula Eψ i (x) to denote that x is dominated by another strategies of i, according to i’s goal, and rewrite (i, x)φ1 as ¬Eψ i (x)∧(i, x)φ1. Finally, we remove the operator [π].

Theorem 4. SL ≺e SLIEDS.

Proof. The main idea of the proof is that we can construct two classes of CGSes C1 = {G1 m | m ≥3} and C2 = {G2 m | m ≥3} s.t. there is an SLIEDS formula to distinguish between C1 and C2, but no SL formula can do so.

The CGSes in the two classes all have the same structure as given in Figure 2. G1 m and G2 m both have 2m actions a1,..., a2m, where for both agents, a1 is the only possible action in w1 and w2, and they only differ in the set of decisions ∆that can achieve the goal of getting to the winning

19173

<!-- Page 6 -->

a1 a2 a3 a4 a5 a6 a1 a2 a3 a4 a5 a6

**Figure 4.** The graph of G(G1

3) (up) and G(G2 3) (down).

state w1 (which is the only state labeled with win in both models) from w0. We note that on such models, what distinguishes a strategy from another is the action to take in w0. Thus a strategy can be represented by the action taken in w0. So such a model can be uniquely represented with a payoff matrix. We give the payoff matrices of G1

3 and G2 3 in Figure 3. In general, the only difference between the payoff matrices of G1 m and G2 m is that the 1 at (m + 1, m + 1) is moved to (2m, m+1). It’s clear that in CGSes in C1, every remaining strategy profile can achieve the goal after IEDS (for both agents, only strategy am+1 is left), and it is not the case in C2 (for both agents, any strategy ai with i ≥m + 1 is left). Thus, the following SLIEDS formula can distinguish C1 and C2: φ = [(1, 2: Xwin)]∞∀x.∀y.(1, x)(2, y)Xwin.

To prove that no SL formula can distinguish C1 and C2, we translate SL formulas on C1 and C2 to FOL (first-order logic) formulas and models in C1 and C2 to first-order structures so that the satisfaction relation is maintained. The key information of the CGSes is what decisions make the transition from w0 to w1. Thus we introduce a binary predicate P(x, y) for this, and to translate a CGS G to a first-order structure G(G), we use the set of actions of G as the domain, and interpret P(x, y) according to G. Figure 4 shows the first-order structures obtained from G1

3 and G2 3, where actions in w0 are viewed as elements, and a directed edge from element a to b means P(a, b) is true. We now show how to translate formulas. Firstly, we note that on models from the two classes, every SL formula can be written without U, as φ1Uφ2 is equivalent to φ2 ∨(φ1 ∧Xφ2). Thus the key of the translation is how to translate Xφ. For this purpose, we can prove from a simple induction on φ that for any w ∈{w1, w2}, any SL formula φ is equivalent to either ⊤or ⊥; we write w |= φ in the former case and w̸ |= φ in the latter. Thus, let x and y be the variables of the strategies assigned to agents 1 and 2 respectively, Xφ can be translated as follows:

• ⊤, if w1 ⊨φ and w2 |= φ; • P(x, y), if w1 ⊨φ and w2 ⊭φ; • ¬P(x, y), if w1 ⊭φ and w2 ⊨φ; • ⊥, if w1 ⊭φ and w2 ⊭φ.

We denote this translation as trx,y(Xφ). Based on the given translation of Xφ, we give the translation from SL formulas to FOL. We first rename the variables s.t. no quantifiers share variables. We use an agent variable assignment β: Ag →StV in the translation to record the strategy variables assigned to agent 1 and 2. The formula tr(φ, β) is defined inductively as follows:

• tr(win, β) = ⊥, as win /∈L(s0); • tr(¬φ, β) = ¬tr(φ, β); • tr(φ1 ∧φ2, β) = tr(φ1, β) ∧tr(φ2, β); • tr(∃s.φ, β) = ∃s.tr(φ, β); • tr((i, s)φ, β) = tr(φ, β[i 7→s]); • tr(Xφ, β) = trβ(1),β(2)(Xφ)

For example, SL formula ∃x.∃y.∃z.(1, x)(2, y)Xp ∧ (1, x)(2, z)X¬p can be translated to ∃x.∃y.∃z.P(x, y) ∧ ¬P(x, z). The correctness of the translation can be proven by a simple induction on the formula if no quantifiers share variables.

Finally, we make use of a result from Libkin (2004) which states that no FOL sentences can distinguish two classes of graphs: one with linear orders of size 2m, and the other with the union of a linear order of size m and a directed cycle of size m, as exemplified by Figure 4. Therefore, no SL sentences can distinguish the classes C1 and C2.

## Model

Checking Memoryless SLIEDS In this section, we prove that model checking memoryless SLIEDS is EXPTIME-complete. This complexity is higher than that of model-checking memoryless SL, which is PSPACE-complete (ˇCerm´ak et al. 2018).

We first define the model checking problem for SLIEDS.

Definition 20. Given a CGS G, a state w on G, an SLIEDS sentence φ, the full memoryless or memoryful strategy space Σf, the problem is to check if G, w, Σf ⊨φ.

Upper Bound Our model checking algorithm MC for memoryless SLIEDS is derived directly from the semantics. Algorithm MC takes a CGS G = ⟨W, L, P, τ, w0⟩, a state w ∈W, a strategy space Σ, a formula φ and two assignments χ and α as parameters, and returns whether G, w, Σ ⊨χ,α φ by checking all the subformulas of φ recursively. All the cases except the case of U are straightforward. To process φ1Uφ2, we need to check if φ2 turns true before φ1 turns false on the computation out(w, α). As out(w, α) forms a loop in memoryless semantics, we only need to check at most |W| states on out(w, α). Since the definition of the strategy elimination operator is involved, we give the subprocess RS for processing it in Algorithm 1. The iterated elimination process RS∞ is done by calling RS on Σ repeatedly until reaching a fixed point.

Theorem 5. Model checking memoryless SLIEDS is in EXP- TIME, and can be done in time exponential to the model size m and the formula size l.

Proof Sketch. We prove that the algorithm takes O(2ml) time by induction on l. Processing φ1Uφ2 takes O(m(2m|φ1| + 2m|φ2|)) = O(2ml) time. Processing ∃s calls MC for every strategy. There are O(2m) strategies, thus it takes O(2m2m(l−1)) = O(2ml) time. As to [π]φ1 and [π]∞φ1, we have: since there are O(2m) agent strategy

19174

<!-- Page 7 -->

## Algorithm

1: Reducing strategy spaces RS(G, w, Σ, χ, π):

1: for each i ∈Ag do 2: for each σi ∈Σ(i) do 3: for each α of −i that is restricted to Σ do 4: if MC(G, w, Σ, [[π]](i), χ, α[i 7→σi]) then 5: add α to Mπ,w,χ,Σ(σi) 6: for each σi, σ′ i ∈Σ(i) do 7: if Mπ,w,χ,Σ(σi) ⊃Mπ,w,χ,Σ(σ′ i) then 8: Σ(i) ←Σ(i) −{σ′ i} 9: return Σ assignments, calling RS takes O(2m2m|π|) time; since RS∞performs RS at most O(2m) times, calling RS∞ takes O(2m2m2m|π|) time; thus processing both [π]φ1 and [π]∞φ1 takes O(2m|[π]| + 2m|φ1|) = O(2ml) time.

Lower Bound To prove the EXPTIME-hardness, we reduce a EXPTIMEhard problem to model checking memoryless SLIEDS. Pauly (2016) proved the 2-Simultaneous IEDS problem is P-hard. By a result of Papadimitriou and Yannakakis (1986), we obtain that 2-Simultaneous IEDS on succinct representation of payoff matrices is EXPTIME-hard. Then, we reduce this problem to model checking memoryless SLIEDS.

We first need to introduce succinct representation sof matrices proposed by Galperin and Wigderson (1983):

Definition 21 (Succinct representation). Let A be a Boolean matrix with N = |I| ≤2n rows and |J| ≤2n columns, where I and J are the sets of row numbers and column numbers. Let x be the binary representation of a number x. A circuit CA with size polynomial in n (polylograthmic in N) is a succinct representation of A if the following properties hold: CA is a combinational circuit with two inputs of n bits each, and for i ∈I, j ∈J, CA(i, j) = 1 iff Aij = 1.

We now introduce a generalization of the conclusion by Papadimitriou and Yannakakis (1986) about succinct representations. We begin with introducing the P-bounded halting problem and the notion of projections (Skyum and Valiant 1985). Given a Turing machine M, an input x and a number T, the bounded halting problem is the decision problem that decides whether M accepts x in T steps. This problem is P-complete by definition if T is polynomial to the size of M and x. A mapping π from a language L1 ⊆{0, 1}∗to another L2 is a projection iff the following conditions hold: (1) For any x ∈L1 (denoted as x1... xm) with length m, its image y = π(x) (denoted as y1... yl) has length l = mc, where c is a constant; (2) There exists a PTIME algorithm that computes the mapping δ: {1,..., l} →{0, 1, x1,..., xm, ¬x1,..., ¬xm} s.t. y1... yl = δ(1)... δ(l). That is, any output bit can be computed from some input bit. It follows that if L1 can be projected to L2, and L2 can be projected to L3, then L1 can be projected to L3.

Theorem (Papadimitriou and Yannakakis 1986). Given a decision problem Π on Boolean matrices, if there is a projec- s0 t0 f0 s1 t1 f1 s2... su−1 tu−1 fu−1

**Figure 5.** The CGS Gc. The initial state w0 = s0.

tion from the P-bounded halting problem to Π, then the problem on succinct representations of matrices is EXPTIMEhard.

This conclusion relates a P-hard problem on Boolean matrices to an EXPTIME-hard one on succinct representations. To apply it, we need the 2-Simultaneous IEDS given and proven to be P-hard by Pauly (2016). Given a finite twoplayer game with Boolean payoff, represented by two payoff matrices, the problem 2-Simutaneous IEDS is to decide whether a given strategy of player 1, represented by the row index, remains after IEDS. We consider this problem on succinct representations, where we use a circuit to represent payoff matrices of both players. Without loss of generality, we assume that a single input bit decides whether the circuit is calculating payoff of player 1 (if the bit is 0) or 2 (if the bit is 1).

Proposition 6. 2-Simultaneous IEDS on succinct representation of payoff matrices is EXPTIME-hard.

Proof Sketch. It is proven by Pauly (2016) that 2- Simultaneous is P-complete. Pauly’s proof is a projection from a variation of the monotone circuit value problem. By a similar proof as the one shown in (Greenlaw, Hoover, and Ruzzo 1995), we can show that the monotone circuit value problem variation can be projected from the P-bounded halting problem.

By a reduction from this problem, we have:

Theorem 7. Model checking memoryless SLIEDS is EXPTIME-hard.

Proof. Given a circuit C representing payoff matrices of both players and a strategy of player 1 represented with a binary number i, we construct in polynomial time a CGS Gc with 3 agents to simulate the game and a formula φc, s.t. φc holds on Gc in memoryless semantics iff the answer of 2-Simultaneous on C and i is true. The idea of constructing Gc and φc is as follows. We divide the gates of C into three types: input gates of player 1, input gates of player 2, and the other gates. Thus we introduce 3 agents corresponding to the 3 types of gates. We number the u gates of C, including the input gates, topologically. Gc has 3u states. Figure 5 shows the general structure of Gc. Each sj state has a controlling agent. For example, if sj is corresponding to an input gate of player 1, then the controlling agent of sj is agent 1. Agent 1 or 2 acts on the states controlled by her as follows: if the input bit of the corresponding gate is 1 (resp. 0), then agent

19175

<!-- Page 8 -->

1 on sj chooses an action which makes the transition to tj (resp. fj). Agent 3 also acts under the states controlled by her. The formula φc will encode the constraint that the acting of agent 3 must follow the circuit. For example, if gate j is an AND gate of the outputs of gate j1 and j2, then agent 3 chooses action leading to tj iff the controlling agents of sj1 and sj2 choose actions leading to tj1 and tj2. Formula φc states that agents 1 and 2 do IEDS according to the correct payoff calculated by agent 3, and after IEDS, there is a strategy of agent 1 left that performs the same as the strategy i of player 1. We now give the detailed construction of the CGS Gc and the formula φc.

The CGS Gc is constructed as follows:

• AP = {evalt, evala, win, in1, in2,..., inu}; • Ac = {yes, no, idle}, and Ag = {1, 2, 3}; • W = {sj, tj, fj | 0 ≤j < u}. • Every tj is labeled with evalt. The state fj corresponding to the input gate controlled by agent 3 is labeled with evala. The state tu−1 is labeled with win. We label the states sj controlled by 1 with the atoms ink, the first one is labeled in1, the second one in2, respectively. • For any agent i, if she controls state sj, then Pi(sj) = {yes, no}. Any other states w have Pi(w) = {idle}. • τ is defined as in Figure 5. In state sj controlled by i, the next state will be tj (resp. fj) if i does yes (resp. no).

Intuitively, evalt means that the gate is determined to have value 1, evala means that the circuit is evaluating the payoff of player 1, win means that the circuit outputs 1. Atoms ink labels the states corresponding to input gates of player 1. We assume there are u′ < u such states, and let their numbers be p1, p2,..., pu′. Therefore, the set of strategies on Gc for agent 1 and 2 would correspond to the set of strategies of player 1 and 2 in the matrix form of the finite two-player game. We denote the strategy that corresponds to the given strategy i as σ1.

To construct φc, we first give the LTL formula ψc that represents the correctness of the evaluation, namely, every gate’s value should be in line with their inputs. For an AND gate numbered j with input gates j1, j2,..., jk, the formula ψj is X2j+1evalt ↔V

1≤m≤k(X2jm+1evalt), which means that the value of this gate is true iff the values of all inputs to the gate are decided by the agents to be true. The formula stating the correctness for an OR gate or a NOT gate can be defined in a similar way. Our formula ψc that represents the correctness of the evaluation is written as the conjunction of all the ψj, while j ranges over all of the non-input gates.

Now it is possible to write the agents’ goals in the IEDS to let it correspond to the elimination in the original twoplayer game on matrices. Agent 1’s goal φ1 is written as ψc ∧Fevala →Fwin, which means if the evaluation is correct, and it is evaluating agent 1’s payoff, then the evaluation should be true, which means agent 1 got payoff 1. Similarly, agent 2’s goal φ2 is written as ψc ∧G¬evala →Fwin. The goal expression π is written as (1: φ1), (2: φ2), (3: ⊤).

The formula φc is given as follows. Let f(yes) = evalt, f(no) = ¬evalt. As the strategies of agent 1 have their behaviors only differ in the u′ states controlled by 1, and in any play these state will always be visited, we can write it as

[π]∞∃x.∀y.∀z.(1, x)(2, y)(3, z)

^

1≤k≤u′ F(ink ∧Xf(σ1(spk))).

This formula means that after the IEDS, there exists a strategy σ of 1 that in all states spk, which are labeled as ink and controlled by 1, will act in a way that the result corresponds to σ1’s actions, i.e., for k = 1,..., u′, if σ1(spk) = yes, then on the computation generated with σ, ink will be followed by evalt, and if σ1(spk) = no, then ink will be followed by evalf. σ is effectively σ1. Therefore, the original problem of 2-Simultaneous on succinct representations is reduced to model checking φc on Gc in the memoryless case.

The formula φc and the CGS Gc both have sizes polynomial to u, the number of gates in C. Since u is polynomial in n, both structures can be constructed in time polynomial in n, thus the reduction is polynomial.

Combining Theorem 5 and Theorem 7, we have

Corollary 8. Model checking memoryless SLIEDS is EXPTIME-complete.

Liu et al. (2020) proved that model checking memoryless JAADL is in EXPTIME, but the lower bound was left open. Note that our technique for proving the complexity lower bound of model checking memoryless SLIEDS can be used in JAADL as well, with the modification that the decision problem used should be 2-Simultaneous in the fully cooperative setting. Such problem can also be proved as P-complete by a projection from the monotone circuit value problem variation. Therefore, we can conclude that model checking memoryless JAADL is EXPTIME-complete as well.

Mogavero et al. (2014) defined a number of SL fragments such as SL[NG], SL[BG], and SL[1G], where SL[1G] is the most restrictive and its model-checking problem is 2EXPTIME-complete while model-checking SL is nonelementary. We can define the corresponding SLIEDS fragments by extending SL fragments with EDS and IEDS operators. However, note that the SLIEDS formula φc in our proof of Theorem 7 is in SLIEDS[1G]. Thus, model-checking memoryless SLIEDS[1G] is already EXPTIME-complete.

## Conclusion

In this work, we propose SLIEDS – an extension of strategy logic SL with EDS and IEDS operators. Different from JAADL (Liu et al. 2020) and similar to rational verification (Wooldridge et al. 2016), when defining dominance of strategies, different agents can have different goals. With this extension, we can reason about rational strategic abilities in multi-agent systems based on the concepts of Nash Equilibrium, IEDS, and bounded rationality. We can also use SLIEDS to reason about joint abilities. We prove that the EDS operator can be expressed in SL, but SLIEDS is strictly more expressive than SL. Finally, we prove that model checking memoryless SLIEDS is EXPTIME-complete. Our future work will focus on exploring the model checking problem in the memoryful case.

19176

<!-- Page 9 -->

## Acknowledgments

We thank the anonymous reviewers for helpful comments. We acknowledge support from the Natural Science Foundation of China under Grant No. 62076261.

## References

Alur, R.; Henzinger, T. A.; and Kupferman, O. 2002. Alternating-time temporal logic. Journal of the ACM (JACM), 49(5): 672–713. Aminof, B.; De Giacomo, G.; Rubin, S.; et al. 2021. Besteffort synthesis: Doing your best is not harder than giving up. In Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence (IJCAI-21). Berwanger, D. 2007. Admissibility in infinite games. In 24th Annual Symposium on Theoretical Aspects of Computer Science (STACS-07). Bulling, N.; Jamroga, W.; and Dix, J. 2008. Reasoning about temporal properties of rational play. Annals of Mathematics and Artificial Intelligence, 53(1): 51–114.

ˇCerm´ak, P.; Lomuscio, A.; Mogavero, F.; and Murano, A. 2018. Practical verification of multi-agent systems against SLK specifications. Information and Computation, 261: 588–614. Chatterjee, K.; Henzinger, T. A.; and Piterman, N. 2010. Strategy logic. Information and Computation, 208(6): 677– 693. Galperin, H.; and Wigderson, A. 1983. Succinct representations of graphs. Information and Control, 56(3): 183–198. Gigerenzer, G.; Todd, P. M.; and the ABC Research Group. 2000. Simple heuristics that make us smart. Oxford University Press. Greenlaw, R.; Hoover, H. J.; and Ruzzo, W. L. 1995. Limits to parallel computation: P-completeness theory. Oxford University Press. Gutierrez, J.; Harrenstein, P.; and Wooldridge, M. 2014. Reasoning about equilibria in game-like concurrent systems. In Principles of Knowledge Representation and Reasoning: Proceedings of the Fourteenth International Conference (KR-14). Gutierrez, J.; Harrenstein, P.; and Wooldridge, M. J. 2017. Reasoning about equilibria in game-like concurrent systems. Annals of Pure and Applied Logic, 168(2): 373–403. Gutierrez, J.; Murano, A.; Perelli, G.; Rubin, S.; Steeples, T.; and Wooldridge, M. J. 2021. Equilibria for games with combined qualitative and quantitative objectives. Acta Informatica, 58(6): 585–610. Gutierrez, J.; Najib, M.; Perelli, G.; and Wooldridge, M. J. 2023. On the complexity of rational verification. Annals of Mathematics and Artificial Intelligence, 91(4): 409–430. Huang, X.; and Ruan, J. 2017. ATL Strategic Reasoning Meets Correlated Equilibrium. In Proceedings of the Twenty-Sixth International Joint Conference on Artificial Intelligence (IJCAI-17). Hyland, D.; Gutierrez, J.; Krishna, S.; and Wooldridge, M. J. 2024. Rational Verification with Quantitative Probabilistic

Goals. In Proceedings of the 23rd International Conference on Autonomous Agents and Multiagent Systems (AAMAS- 24). Kupferman, O.; Perelli, G.; and Vardi, M. Y. 2016. Synthesis with rational environments. Annals of Mathematics and Artificial Intelligence, 78(1): 3–20. Li, Y.; Lorini, E.; and Mittelmann, M. 2025. Rational Capability in Concurrent Games. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS-25). Libkin, L. 2004. Elements of Finite Model Theory. Springer. Liu, Z.; Xiong, L.; Liu, Y.; Lesp´erance, Y.; Xu, R.; and Shi, H. 2020. A Modal Logic for Joint Abilities under Strategy Commitments. In Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence (IJCAI-20). Lorini, E. 2016. A minimal logic for interactive epistemology. Synthese, 193(3): 725–755. Mogavero, F.; Murano, A.; Perelli, G.; and Vardi, M. Y. 2014. Reasoning about strategies: On the model-checking problem. ACM Transactions on Computational Logic (TOCL), 15(4): 1–47. Osborne, M. J.; and Rubinstein, A. 1994. A course in game theory. MIT press. Papadimitriou, C. H.; and Yannakakis, M. 1986. A note on succinct representations of graphs. Information and control, 71(3): 181–185. Pauly, A. 2016. The computational complexity of iterated elimination of dominated strategies. Theory of Computing Systems, 59: 52–75. Russell, S. J.; and Wefald, E. 1991. Do the right thing studies in limited rationality. MIT Press. Simon, H. A. 1955. A behavioral model of rational choice. The quarterly journal of economics, 99–118. Skyum, S.; and Valiant, L. G. 1985. A complexity theory based on Boolean algebra. Journal of the ACM (JACM), 32(2): 484–502. Wooldridge, M.; Gutierrez, J.; Harrenstein, P.; Marchioni, E.; Perelli, G.; and Toumi, A. 2016. Rational verification: From model checking to equilibrium checking. In Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI-16).

19177
