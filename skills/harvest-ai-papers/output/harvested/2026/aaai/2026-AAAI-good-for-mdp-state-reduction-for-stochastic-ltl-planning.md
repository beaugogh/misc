---
title: "Good-for-MDP State Reduction for Stochastic LTL Planning"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40967
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40967/44928
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Good-for-MDP State Reduction for Stochastic LTL Planning

<!-- Page 1 -->

Good-for-MDP State Reduction for Stochastic LTL Planning

Christoph Weinhuber1, Giuseppe De Giacomo1, Yong Li2*, Sven Schewe3, Qiyi Tang3

1University of Oxford, Oxford, UK 2Key Laboratory of System Software (Chinese Academy of Sciences), Institute of Software Chinese Academy of Sciences, PRC

3University of Liverpool, UK {christoph.weinhuber, giuseppe.degiacomo}@cs.ox.ac.uk, liyong@ios.ac.cn, {sven.schewe, qiyi.tang}@liverpool.ac.uk

## Abstract

We study stochastic planning problems in Markov Decision Processes (MDPs) with goals specified in Linear Temporal Logic (LTL). The state-of-the-art approach transforms LTL formulas into good-for-MDP (GFM) automata, which feature a restricted form of nondeterminism. These automata are then composed with the MDP, allowing the agent to resolve the nondeterminism during policy synthesis. A major factor affecting the scalability of this approach is the size of the generated automata. In this paper, we propose a novel GFM state-space reduction technique that significantly reduces the number of automata states. Our method employs a sophisticated chain of transformations, leveraging recent advances in good-for-games minimisation developed for adversarial settings. In addition to our theoretical contributions, we present empirical results demonstrating the practical effectiveness of our state-reduction technique. Furthermore, we introduce a direct construction method for formulas of the form GFφ, where φ is a co-safety formula. This construction is provably single-exponential in the worst case, in contrast to the general doubly-exponential complexity. Our experiments confirm the scalability advantages of this specialised construction.

Code — https://zenodo.org/records/17582751 Extended version — https://arxiv.org/pdf/2511.09073

## Introduction

Planning with temporal objectives has a long tradition in artificial intelligence. Early pioneering work, such as (Bacchus, Boutilier, and Grove 1996, 1997; Littman 1997; Littman, Goldsmith, and Mundhenk 1998; Thi´ebaux et al. 2006), defined key formalisms like Markov decision processes (MDPs), analysed the computational complexity of planning problems and introduced methods for handling non-Markovian rewards.

These foundations paved the way for more expressive and structured approaches, most notably the use of Linear Temporal Logic (LTL) (Pnueli 1977), to formally specify complex goals (Lacerda, Parker, and Hawes 2014; Brafman and Giacomo 2024). This field is now even pushing into areas like reinforcement learning (Yang, Littman, and Carbin

*Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

2022), multi-agent systems (Schillinger, B¨urger, and Dimarogonas 2019), and handling uncertainty (Yu et al. 2025).

Traditionally, in order to solve an MDP with an LTL goal φ, we first build a nondeterministic B¨uchi automaton (NBA) for φ. Then we convert the NBA to an equivalent deterministic automaton, e.g., a deterministic Rabin automaton (DRA) (Safra 1988). Recent progresses in this direction include direct translations of LTL to DRAs (Esparza and Kret´ınsk´y 2014). Afterwards, we need to perform the Cartesian product of the MDP and the DRA, identify accepting end-components (ECs) and compute a (memoryless) strategy with maximal probability of reaching accepting ECs.

State-of-the-art approaches (Hahn et al. 2015; Sickert et al. 2016) proposed the usage of limit-deterministic B¨uchi automata (LDBAs) to avoid the notorious problem of obtaining DRAs. LDBAs give the burden of resolving the nondeterminism in automata to the agent, without changing the optimal satisfaction probability. Yet, only a certain type of LDBAs works for all finite MDPs. The precise criterion for NBAs is expressed by being “good-for-MDP” (GFM), where all nondeterministic choices are angelic in the sense that they can be resolved by the agent, while preserving the optimal satisfaction probability (Hahn et al. 2020). While the LTL to GFM construction does not change the complexity of the overall planning problem, in practice, the difference among using GFMs and DRAs is significant (Meyer, Sickert, and Luttenberger 2018).

A major factor affecting the scalability of solving MDPs with LTL goals is the size of the GFM automata corresponding to the LTL goals (Hahn et al. 2015; Sickert and Kret´ınsk´y 2016). In this paper, we propose a novel GFM state-space reduction technique that significantly reduces the number of automata states. Our method employs a sophisticated chain of transformations, which allows us to leverage recent advances in good-for-games minimisation developed for adversarial settings (Radi and Kupferman 2022) to our context. We provide experimental evidence that our statereduction technique effectively reduces the automata state space, by taking benchmark examples of LTL goals from eight sources, including influential papers in planning, verification and reinforcement learning.

Furthermore, we introduce a direct method for constructing the GFM automata of formulas of the form GFφ, where φ is a co-safety property. This kind of formulas is common

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

36457

<!-- Page 2 -->

in both verification (Holeˇcek et al. 2004) and reinforcement learning (Jackermeier and Abate 2025). We show that the GFM automaton obtained through our specialised construction incurs only a singly exponential blow-up, in contrast to the doubly exponential blow-up in the general case. Moreover, we provide experimental evidence that this theoretical advantage indeed translates into significantly fewer states.

Extended Version. We refer to the extended version for all missing proofs and the full benchmark set.

## Preliminaries

Markov Decision Processes. Following (Baier and Katoen 2008), a Markov decision process (MDP) M is a tuple (S, Act, Σ, P, s0, L) with a finite set of states S, a set of actions Act, a set of labels Σ, a transition probability function P: S × Act × S →[0, 1], an initial state s0 ∈S and a labelling function L: S × Act →Σ that labels state-action pairs to the set of propositions that hold in that state1. We abuse the notation by writing Act(s) to denote the set of available actions at state s. A path ξ of M is an (in)finite sequence of alternating states and actions ξ = s0a0s1a1 · · ·, ending with a state if finite, such that for all i ≥0, ai ∈Act(si) and P(si, ai, si+1) > 0. The sequence L(ξ) = L(s0, a0)L(s1, a1), · · · over Σ is called the trace induced by the path ξ over M. We denote by FPaths and IPaths the set of all finite and infinite paths of M.

A (finite-memory) strategy µ of M is a function µ: FPaths →Distr(Act) such that, for each ξ ∈FPaths, µ(ξ) ∈Distr(Act(lst(ξ))), where lst(ξ) is the last state of the finite path ξ and Distr(Act) denotes the set of all possible distributions over Act. Let ΩM µ (s0) denote the subset of infinite paths of M that correspond to strategy µ and initial state s0. A strategy µ is memoryless if µ: S →Distr(Act), meaning it selects actions independently of the past.

A strategy µ of M is able to resolve the nondeterminism of an MDP and induces a Markov chain (MC) Mµ = (FPaths, Σ, Pµ, L′) where, for ξ = s0a0 · · · sn−1an−1sn ∈ FPaths and an ∈ Act(sn), Pµ(ξ, ξ · an · sn+1) = P(sn, an, sn+1) · µ(ξ)(an) and L′(ξ) = L(sn−1, an−1).

A sub-MDP of M is an MDP M′ = (S′, Act′, Σ, P′, L′) where S′ ⊆S, Act′ ⊆Act is such that, for every s ∈ S′, Act′(s) ⊆Act(s), and P′ and L′ are analogous to P and L when restricted to S′ and Act′. In particular, M′ is closed under probabilistic transitions, i.e., for all s ∈ S′ and a ∈Act′ we have that P(s, a, s′) > 0 implies P′(s, a, s′) > 0. An end-component (EC) of an MDP M is a sub-MDP M′ of M such that its underlying graph is strongly connected. A maximal end-component (MEC) is an EC E = (E′, Act′, Σ, P′, L′) such that there is no other EC E′ = (E′′, Act′′, Σ, P′′, L′′) such that E′ ⊂E′′. An MEC E that cannot reach states outside E′ is a leaf component.

Theorem 1 ((de Alfaro 1997; Baier and Katoen 2008)). Once an EC E of an MDP is entered, there is a strategy that visits every state-action combination in E with probability 1 and stays in E forever. Moreover, for every strategy the union

1This generalises the usual labelling function L: S →Σ.

of the end-components is visited with probability 1. An infinite path of an MC M almost surely (with probability 1) will enter a leaf component.

Linear Temporal Logic. An LTL formula, over a finite set of atomic propositions AP is defined as φ::= a ∈AP | ¬φ | φ ∧φ | φ ∨φ | Xφ | Gφ | Fφ | φUφ. Here X (Next), G (Globally/Always), F (Finally/Eventually) and U (Until) are temporal operators.

An ω-trace w is an infinite sequence of letters w[0] w[1] w[2]... with w[i] ∈Σ = 2AP. We denote the infinite suffix w[i] w[i + 1]... by wi. The satisfaction relation |= between ω-traces w and formulas φ is defined as follows:

w |= a ⇐⇒a ∈w[0], w |= ¬φ ⇐⇒w̸ |= φ, w |= Xφ ⇐⇒w1 |= φ, w |= Gφ ⇐⇒∀k. wk |= φ, w |= Fφ ⇐⇒∃k. wk |= φ, w |= φUψ ⇐⇒∃k.

wk |= ψ ∧∀j < k, wj |= φ

Further, ∀w.w |= tt and ∀w.w̸ |= ff. We denote by [φ] the set of infinite traces satisfying the LTL formula φ.

Automata. A (nondeterministic) transition system (TS) is a tuple T = (Q, q0, δ), with a finite set of states Q, an initial state q0 ∈Q, and a transition function δ: Q × Σ →2Q. We extend δ to sets by δ(S, σ):= S q∈S δ(q, σ). A deterministic TS satisfies |δ(q, σ)| ≤1 for each q ∈Q and σ ∈Σ.

An automaton A is defined as a tuple (T, α), where T is a TS and α is an acceptance condition. We define ∆(δ) = {(q, σ, q′) | q, q′ ∈Q, σ ∈Σ, q′ ∈δ(q, σ)}. For an infinite trace w ∈Σω, a run of A on w is an infinite sequence of transitions ρ = (q0, w[0], q1)(q1, w[1], q2) · · · such that, for every i ≥0, qi+1 ∈δ(qi, w[i]). Let inf(ρ) be the set of transitions that occur infinitely often in a run ρ. The acceptance condition α ⊆∆(δ) is a set of accepting (rejecting, resp.) transitions for B¨uchi (co-B¨uchi, resp.). A run ρ satisfies the B¨uchi (co-B¨uchi, resp.) acceptance condition α if inf(ρ) ∩α̸ = ∅(inf(ρ) ∩α = ∅, resp.).

A run is accepting if it satisfies the condition α; a trace w ∈Σω is accepted by A if there is an accepting run ρ of A over w. We use three letter acronyms in {D, N}×{B, C}× {A} to denote automata types where the first letter stands for the TS mode, the second for the acceptance type and the third for automaton. For example, DBA means deterministic B¨uchi automaton. We assume that all automata are complete, i.e., for each state s ∈Q and letter σ ∈Σ, |δ(s, σ)| ≥1.

We denote by L(A) the ω-language recognised by an ωautomaton A, i.e., the set of ω-traces accepted by A.

## 3 Stochastic Planning Problem

Overview. In a stochastic planning problem, we model the interaction between the agent and the environment as an MDP M and its task specification as an LTL formula φ. The goal is to find an optimal strategy µ for M that maximises the chance that the infinite sequence of observed propositions satisfies φ. Formally, we want the probability of the ω-traces generated by Mµ and belonging to [φ], to be maximal among all possible choices of µ.

36458

<!-- Page 3 -->

MDPs and LTL Task Specification. Every LTL formula φ can be translated into a (nondeterministic) B¨uchi automaton A, accepting [φ], i.e., L(A) = [φ] (Vardi and Wolper 1986). Recall that, for a given strategy µ on an MDP M, we can induce an MC Mµ. We define the semantic satisfaction probability of the induced MC Mµ for L(A) as PMµ(L(A)) = P{ξ ∈ΩM µ (s0): L(ξ) ∈L(A)}, which is the probability of Mµ generating an ω-trace in [φ]. For an MDP M and an automaton A, we define the maximal semantic satisfaction probability as Psem(M, A) = supµ PMµ(L(A)). We look for an optimal strategy µ that achieves Psem(M, A) in the planning problem.

Product of MDPs and B¨uchi automata. If A is a DBA, we can solve the problem of finding an optimal strategy µ by constructing the product MDP M × A and extract a memoryless strategy µ on M × A that reaches accepting components with maximal probability (Baier and Katoen 2008). If A is nondeterministic, this is in general not possible, because we have to resolve the nondeterminism, which corresponds to future forecasting capabilities that we can assign neither to the agent, nor to the (probabilistic) environment. However, it has been observed (Hahn et al. 2020; Sickert et al. 2016; Hahn et al. 2015) that there is a class of automata called good-for-MDPs (GFM) for which we can assign the nondeterminism to the agent without loss of optimality. Intuitively, a nondeterministic automaton is GFM, if the nondeterminism can be resolved by the agent (we postpone the formal definition of GFM to later in this section). If an automaton is GFM, then we can still adopt a variant of the product construction shown below:

Formally, let M = (S, Act, Σ, P, s0, L) be an MDP and A = (Q, q0, δ, α) be an NBA. We define the product MDP M × A = (S×, Act×, Σ, P×, ⟨s0, q0⟩, L×, α×) augmented with the acceptance condition α× where

• S× = S × Q is the state space. • Act× = Act×[k] is the action set where k is the maximal out-degree of A for any state in Q and letter in Σ. We denote [k] = {1, · · ·, k} for any integer k > 0. • P×: S× × Act× × S× →[0, 1] is the transition probability function such that P×(⟨s, q⟩, ⟨a, i⟩, ⟨s′, q′⟩) = P(s, a, s′) if P(s, a, s′) > 0 and q′ ∈δ(q, L(s, a)) where q′ is the i-th state in the ordered set δ(q, L(s, a)). • L×(⟨s, q⟩, ⟨a, i⟩) = L(s, a) for state ⟨s, q⟩∈S × Q and action ⟨a, i⟩∈Act×, and • For B¨uchi/co-B¨uchi, α× = {(⟨s, q⟩, ⟨a, i⟩, ⟨s′, q′⟩) | P×(⟨s, q⟩, ⟨a, i⟩, ⟨s′, q′⟩) > 0, (q, L(s, a), q′) ∈α}.

Instead of storing the selected successor state in the action name as in other literature, e.g. (Hahn et al. 2020), we index the choice by its position in a predefined order over successors. Formally, for each q ∈Q and σ ∈Σ, we define a function idxA,q,σ mapping each q′ ∈δ(q, σ) to its unique position i ∈[k]. This index i serves as the identifier for the agent’s choice in our product construction. This encoding is equivalent to (Hahn et al. 2020) but has a slight advantage of using fewer actions. For full details, see the extended version.

Conditions for GFMness. In order to see if an NBA is GFM, we have to characterise the probabilities that come from the syntactic construction above and show that they are the same of those intrinsic in the original problem. Recall that the probability of the original problem is the following:

Psem(M, A) = sup µ PMµ(L(A)).

The probability coming from the syntactic product construction above is characterised as: Psyn(M, A) = sup µ P{ξ ∈ΩM×A µ (⟨s0, q0⟩): ξ accepting}.

This can be simplified to Psyn(M, A) = supµ P(M×A)µ(FX), where X is the set of states of the accepting MECs in M × A that contain accepting transitions in α×.

Clearly, Psyn(M, A) ≤Psem(M, A), because accepting runs ξ only occur on accepting words. Thus, a strategy µ chooses an accepting run on accepting words in the best case, but it is also possible for µ to make wrong decisions.

Obviously, Psyn(M, A) = Psem(M, A) if A is deterministic. Following (Hahn et al. 2020), an NBA A is said to be GFM if, for all finite MDPs M, Psem(M, A) = Psyn(M, A). See extended version for a non-GFM case.

LTL to GFM automata. There are several algorithms to transform an LTL formula into an NBA that is GFM (Sickert et al. 2016; Hahn et al. 2020). The runtime to construct a GFM automaton from an LTL formula is doubly exponential in the size of the formula, which is the same cost as obtaining a deterministic automata. However, the practical advantage of going through GFM instead of deterministic automata is enormous and all state-of-the-art systems implement an LTL to GFM construction (Sickert et al. 2016; Hahn et al. 2020).

4 Probabilistic ω-Automata Our state reduction technique is based on obtaining a small probabilistic (B¨uchi) automaton (PA) out of a GFM automaton. The key characteristic of PAs (Baier, Gr¨oßer, and Bertrand 2012) is that, while being nondeterministic, their nondeterministic choices are resolved randomly. A PA P = (Σ, Q, δ, q0, α) is a nondeterministic automaton equipped with a B¨uchi acceptance condition α and a randomised transition function δ: Q × Σ 7→Distr(Q), where, from state q and letter σ, transition to q′ is taken with probability δ(q, σ)(q′). We often abuse notation by writing δ(q, σ) to denote its support. Each word w ∈Σω induces a probability measure Pw

P on Qω in the usual way. The probability that P accepts w, denoted by PP(w), is the probability measure of all accepting runs of w on P, that is:

PP(w) = Pw

P({π: π is an accepting run of w}). A PA P is a 0/1-PA if, for any word w ∈Σω, we have either PP(w) = 1 or PP(w) = 0. For a 0/1-PA P, with a slight abuse of notation, we say a word w is accepted by P (w is in L(P)) if PP(w) = 1. 0/1-PAs are known to be semantically deterministic (Li et al. 2025). That is, given a state p and a letter σ of a 0/1-PA P, for any two states q, r ∈δ(p, σ), we have that L(Pq) = L(Pr) where Ps is the automaton by setting the initial state to s. For a detailed introduction to PAs please refer to (Baier, Gr¨oßer, and Bertrand 2012).

36459

<!-- Page 4 -->

Product of MDPs and 0/1-PA. In the following, we show for the first time that 0/1-PAs can also be perceived as another type of GFM automata. To this end, we first define the product MDP of an MDP M and a 0/1-PA P 2.

Formally we define the product as follows. Let M = (S, Act, Σ, P, s0, L) be an MDP and P = (Q, q0, δ, α) be a 0/1-PA over Σ. We define the product MDP M ⊗P = (S⊗, Act⊗, Σ, P⊗, ⟨s0, q0⟩, L⊗, α⊗) where

• S⊗= S × Q is the state space, • Act⊗= Act is the action set, • P⊗: S⊗× Act⊗× S⊗→[0, 1] is the transition probability function such that P⊗(⟨s, q⟩, a, ⟨s′, q′⟩) = P(s, a, s′) · δ(q, σ, q′) if P(s, a, s′) > 0 and q′ ∈δ(q, σ) where σ = L(s, a), • L⊗: S⊗×Act⊗→Σ where L⊗(⟨s, q⟩, a) = L(s, a) and • α⊗= {(⟨s, q⟩, a, ⟨s′, q′⟩) | (q, L(s, a), q′) ∈α, a ∈ Act⊗, P⊗(⟨s, q⟩, a, ⟨s′, q′⟩) > 0}. Intuitively, we still ask the agent to make decisions on which letter to choose for the 0/1-PA P, but leave the choice of a successor to a random strategy. That is, the agent resolves the nondeterminism by choosing actions, and once the action a is selected, according to the definition of MDP M ⊗P, we also know the chosen letter σ = L⊗(⟨s, q⟩, a) as well. This is different from the classical product M × A, where the agent not only decides the next letter, but also the next successor in A, by selecting the action ⟨a, i⟩∈Act×.

For the product M ⊗P, we can define a similar maximal syntactic satisfaction probability:

Psyn(M, P) = sup µ P{ξ ∈ΩM⊗P µ (⟨s0, q0⟩): ξ accepting}.

Crucially, we can see that 0/1-PAs are another type of GFM B¨uchi automata in the following sense: Theorem 2. Let D be a DBA and P be an equivalent 0/1- PA such that L(P) = L(D). For a finite MDP M, we have that Psyn(M, P) = Psyn(M, D) = Psem(M, D) = Psem(M, P).

An equivalent 0/1-PA P always exists for a DBA D because a DBA can be easily transformed to an equivalent 0/1- PA by transitioning to the only successor with probability one. Since 0/1-PAs are GFM based on our product MDP definition, we can then apply standard strategy synthesis approach once the product MDP M ⊗P is constructed.

## 5 Good-for-MDP State Reduction

In this section, we present our main contribution, a general state-space reduction for GFM automata. We assume to have a GFM automaton AGFM and through a polynomial Redux procedure, we return a 0/1-PA APA, whose state space can be significantly reduced. Redux works in several stages, see Figure 1, which we detail below.

2We note that a source of 0/1-PAs can be a special type of automata whose nondeterminism can be resolved by randomness discussed in (Henzinger, Prakash, and Thejaswini 2025). This type of automata is also said to be GFM in a discussion without formal proofs in (Henzinger, Prakash, and Thejaswini 2025).

**Figure 1.** Overview of our state reduction pipeline

• First step (Poly): we perform a GFM-to-DBA transformation by embedding in the transitions of the GFM AGFM the choices [k] used in the product construction of Section 3, making it a complete DBA ADBA. • Second step (Const): we treat the DBA ADBA as a DCA, ADCA, by simply changing the acceptance condition. • Third step (Poly): we apply a minimisation algorithm originally developed for good-for-games (GFG) NCAs (Radi and Kupferman 2022) to ADCA to obtain a minimal GFG-NCA AGFG-Min. • Fourth step (Poly): we transform the GFG-NCA AGFG-Min into a 0/1-PA APA with the same number of states as AGFG-Min.

Here “Poly” and “Const” indicate that their corresponding steps perform in polynomial and constant time, respectively.

Step 1: GFM to DBA

We consider the product M×AGFM of Section 3 and modify both the MDP M and automaton AGFM by embedding the transition choices [k]. The resulting MDP M′ has its action set expanded from Act to Act × [k]. Similarly, the resulting automaton ADBA will have the transitions re-labelled from Σ to Σ × [k]. As a result the automaton ADBA is deterministic.

Formally, we define the modified MDP M′ = (S′, s′

0, Act′, P′, L′) from M = (S, s0, Act, P, L) as

• S′ = S, s′ 0 = s0, Act′ = Act × [k], • L′: S′×Act′ →Σ′ where Σ′ = Σ×[k], and if L(s, a) = σ, then L′(s, ⟨a, i⟩) = ⟨σ, i⟩for all i ∈[k], and • P′(s, ⟨a, i⟩, s′) = P(s, a, s′) for all i ∈ [k] and P(s, a, s′) > 0.

We define the DBA ADBA = (QDBA, q0, δDBA, αDBA) from AGFM = (Q, q0, δ, α) as:

• QDBA = Q, αDBA = {(q, ⟨σ, i⟩, q′) | (q, σ, q′) ∈α, i = idxA,q,σ(q′)}, and • δDBA(q, ⟨σ, i⟩) = q′ if q′ ∈δ(q, σ) and idxA,q,σ(q′) = i.

ADBA will then be made complete. Intuitively, we assign the nondeterminism of AGFM to the agent by extending the action set Act to Act × [k] in M′, which then would allow us to obtain the DBA ADBA since the nondeterminism in AGFM will be taken care of by the agent. We observe that M×AGFM and M′ ×ADBA (obtained by applying the product construction in Section 3) have the same state space. Moreover, in M′ ×ADBA, the action set is Act×[k]×[1], as the maximal out-degree of the DBA ADBA is 1. We can drop [1], which is a constant in every transition and obtain:

36460

![Figure extracted from page 4](2026-AAAI-good-for-mdp-state-reduction-for-stochastic-ltl-planning/page-004-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-good-for-mdp-state-reduction-for-stochastic-ltl-planning/page-004-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-AAAI-good-for-mdp-state-reduction-for-stochastic-ltl-planning/page-004-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

Lemma 1. The product M×AGFM and M′ ×ADBA are the same. Moreover, the optimal strategy µ for each state pair (s, q) ∈S × Q in either of the products will obtain optimal satisfaction probabilities in both products.

By Lemma 1, it is easy to observe that the syntactic probabilities of M × AGFM and M′ × ADBA are the same. Since ADBA is deterministic and thus GFM, we have Psyn(M′, ADBA) = Psem(M′, ADBA). It then follows: Theorem 3. Psem(M, AGFM) = Psyn(M, AGFM) = Psyn(M′, ADBA) = Psem(M′, ADBA).

The GFM to DBA conversion can be done in polynomial time. The construction of the modified MDP M′ and the DBA ADBA involves a direct translation of the original components. The number of states remains the same, while the size of the action set and the alphabet expands by a factor of k, which is a polynomial increase.

Step 2: DBA to DCA Next, we syntactically convert the DBA ADBA into a DCA ADCA. To do so, we only need to modify the acceptance condition. ADCA has the same set of states, initial state, and transition function as ADBA. The co-B¨uchi acceptance condition requires that a run is accepting if it intersects with the set of rejecting transitions only a finite number of times. The set αDCA of rejecting transitions for the DCA ADCA is the same as the set αDBA of accepting transitions in ADBA, but only interpreted differently. Observe that the languages of ADBA and ADCA complement each other. ADCA is just an intermediate automaton on which we apply GFG-minimisation next.

Since this conversion does not require any computational modification to the automaton’s transition structure, it can be done in constant runtime.

Step 3: GFG-Minimisation ADCA is deterministic and thus a GFG automaton that we can apply minimisation algorithms (Radi and Kupferman 2022) on in this step. To formally understand this step, we take a detour to introduce GFG automata.

GFG automata (Henzinger and Piterman 2006) are automata in which nondeterminism can be resolved deterministically by assigning the choice to the protagonist in an adversarial (vs. stochastic MDPs) games. Formally, an automaton A is said to be GFG if there exists a strategy f: Σ∗→Q such that for every accepting word w = σ0σ1 · · ·, the run f(ϵ)f(σ0) · · · f(σ0 · · · σi) · · · is accepting. Intuitively, this indicates that there is a deterministic strategy to produce an accepting run in a GFG automaton even if the accepting word is given letter by letter. Interestingly, (transition-based) GFG co-B¨uchi automata can be minimised in polynomial time (Radi and Kupferman 2022). Since GFG automata have more restricted nondeterminism than GFM automata, GFG automata are also GFM (Klein et al. 2014). GFG automata are not adopted in state-of-the-art stochastic planning tools, such as PRISM (Kwiatkowska, Norman, and Parker 2011). The reason is that GFG B¨uchi (resp. co-B¨uchi) automata cannot recognise all languages expressed by LTL as they are only as expressive as their deterministic counterparts. Moreover, current approaches to construct GFG automata are not as efficient as the ones for GFM. Notably, our work is able to use GFG minimisation on GFM automata that recognise all ω-regular properties. See extended version for more details.

In our construction we apply GFG co-B¨uchi minimisation (Radi and Kupferman 2022) on ADCA, yielding a minimal GFG-NCA AGFG-Min accepting L(ADCA).

Step 4: GFG-Min to 0/1-PA (Li et al. 2025) has proven that the minimal GFG-NCA produced by (Radi and Kupferman 2022) can be turned into a language equivalent 0/1-PA by resolving its nondeterminism with random choices.

The translation from the minimal GFG-NCA AGFG-Min to a 0/1-PA APA is quite simple: we only need to resolve the nondeterminism by random choices. Formally, we treat AGFG-Min as a B¨uchi automaton ANBA = (QNBA, q0, δNBA, αNBA) and build the PA APA = (QPA, q0, δPA, αPA) as:

• QPA = QNBA, αPA = αNBA, and • δPA(q, σ)(q′) = 1 |δNBA(q,σ)| for each q ∈QPA, σ ∈Σ′ and q′ ∈δNBA(q, σ). Following from (Li et al. 2025, Lemma 3), we get: Lemma 2. L(APA) = L(ADBA) and APA is a 0/1-PA.

It immediately follows that, according to Theorem 2, we can use APA to obtain an optimal strategy for M′ to achieve Psem(M′, APA) = Psem(M′, ADBA) since L(APA) = L(ADBA) holds. Together with Theorems 2 and 3, we then obtain our main result: Theorem 4. From an optimal strategy µ on M′ ⊗APA, one can obtain an optimal strategy µ′ for M that achieves the maximal probability Psem(M, AGFM).

Summary. Details on optimal strategy synthesis, along with further optimisations, are in the extended version. We summarise our stochastic planning algorithm below:

• Construct a GFM (B¨uchi) automaton AGFM from φ. • Create M′ from M and ADBA (and ADCA) from AGFM. • Apply GFG minimisation on ADCA and treat the minimised automaton AGFG-Min as a B¨uchi automaton ANBA. • Translate ANBA to a 0/1-PA APA. • Create M′ ⊗APA. • Identify the accepting MECs that have some accepting transitions. • Synthesise an optimal strategy µ that maximises the reachability probability of accepting MECs as usual.

## 6 Direct GFM

Construction for GFφ GFφ fragment. We now focus on the syntactic class of LTL formulas of the form GFφ where φ is a co-safety formula with the following syntax:

φ:= a | ¬a | φ ∧φ | φ ∨φ | Xφ | Fφ | φUφ.

They express that a finite trace pattern repeats infinitely often, which we refer to as repeated reachability properties. Formally, P ⊆Σω is a repeated reachability property if

36461

<!-- Page 6 -->

there exists a language of finite words R ⊆Σ∗such that, for every w ∈P, infinitely many prefixes of w belong to Σ∗· R. Then, we have that: Lemma 3. P is a repeated reachability property specifiable in LTL if, and only if, P is specifiable in GFφ, where φ is a co-safety formula.

The GFφ fragment is very common in verification (Holeˇcek et al. 2004) and also in reinforcement learning (Jackermeier and Abate 2025). More generally, repeated reachability properties are within a commonly used subclass of so-called recurrence properties (Manna and Pnueli 1990; Chang, Manna, and Pnueli 1992).

Direct GFM Construction for GFφ. Consider a formula of the form GFφ, the subformula φ expresses a finite trace property, which can be accepted by a nondeterministic finite automaton (NFA)3. To make our construction more general, we will start from an NFA instead of the formula φ in the following. An NFA N is a tuple (T, F) where T = (Q, q0, δ) is a nondeterministic TS and F ⊆Q is a set of final states. Unlike NBAs, NFAs only operate on finite traces rather than ω-traces. A finite trace u ∈Σ∗is accepted by an NFA N if one of its finite runs terminates at a final state.

We can construct for a co-safety property formula φ, an NFA Nφ = (Q, q0, δ, F) such that L∗(Nφ) · (tt)ω = [φ] where L∗(N) denotes the set of finite traces accepted by Nφ. Note that the alphabet here is Σ = 2AP.

Now we can construct from Nφ a GFM automaton A = (QA, qA, δA, αA) for GFφ where

• QA ⊆((Q \ F) ∪{q0}), qA = q0, • δA: QA × Σ →2QA is defined such that for each q ∈ QA and σ ∈Σ, we have (1) q′ ∈δA(q, σ) if q′ ∈δ(q, σ) with q′ /∈F, and (2) q0 ∈δA(q, σ), and • αA = {(q, σ, q0) ∈∆(δA) | ∃q′ ∈δ(q, σ) ∧q′ ∈F}. The intuition is that, for a repeated reachability property GFφ, we can forget the past finite trace at any point and start tracking whether the following finite trace satisfies φ. The B¨uchi acceptance condition will make sure that the reachability/co-safety formula φ will be satisfied infinitely often. Therefore, in the construction, we can always reset and go back to the initial state q0, which is why every state q has a successor q0 on every letter σ ∈Σ. Once the formula φ has been fulfilled, i.e., a final state q′ has been reached from q over letter σ in Nφ, we need to mark the transition (q, σ, q0) in A as accepting and start tracking finite traces satisfying φ again by moving back to the initial state q0.

It is also easy to show that a memoryless random strategy on A can generate an accepting run almost surely over an ωtrace from [GFφ]. This is because accepting transitions can be reached with positive probabilities from anywhere in A and it is not possible to skip accepting transitions forever in an infinite run with positive probabilities.

Let |φ| be the number of modalities and connectives in φ. It then follows that:

3Our construction applies to any NFA, not just those from cosafety LTL (see extended version), covering repeated reachability properties not expressible in LTL, i.e., monadic first-order and finite LTL (De Giacomo and Vardi 2013).

Pattern Owl Owl-Red Slim Slim-Red

TDR[6] 64 (0.46) 64 (0.03) 65 (0.09) 34 (0.01) TDR[7] 128 (0.46) 128 (0.15) 129 (0.12) 66 (0.02) TDR[8] 256 (0.48) 256 (0.69) 257 (0.14) 130 (0.05)

LIB[4] 17 (0.44) 10 (0.01) 33 (0.11) 18 (0.13) LIB[5] 21 (0.48) 12 (0.01) 65 (0.20) 34 (3.83) LIB[6] 25 (0.62) 14 (0.01) 129 (0.69) 66 (128.34)

BRP[6] 69 (0.55) 17 (0.02) 317 (0.14) 65 (0.17) BRP[7] 133 (0.65) 19 (0.04) 637 (0.21) 95 (0.71) BRP[8] 261 (0.86) 21 (0.14) 1277 (0.33) 146 (3.49)

EHP 13 (0.43) 9 (0.01) 127 (0.14) 54 (0.31)

NU[4] 44 (1.16) 23 (0.02) 51 (0.22) 39 (0.02) NU[5] 150 (1.41) 56 (0.17) 232 (0.82) 159 (0.76) NU[6] 433 (5.92) 249 (27.75) 1425 (12.24) 753 (163.32)

LFR[6] 39 (0.77) 40 (0.27) 40 (0.44) 21 (0.19) LFR[7] 72 (0.92) 73 (2.99) 73 (1.57) 34 (1.76) LFR[8] 137 (1.45) 138 (39.11) 138 (10.74) 59 (20.84)

**Table 1.** Comparison of automata state spaces of Owl and Slim against their reduced versions, Owl-Red and Slim-Red. We report number of states (smallest in bold) and runtime (in seconds). Within Owl-Red and Slim-Red we only measure the time it took to reduce the automaton.

Theorem 5. (1) L(A) = [GFφ], (2) A is GFM and (3) A has 2O(|φ|) states.

Note that as, for a co-safety/reachability property φ, the NFA Nφ of φ has 2O(|φ|) states (De Giacomo and Vardi 2013), so does our GFM automaton A for GFφ. Current GFM constructions such as (Sickert et al. 2016; Hahn et al. 2020) normally output a DBA for GFφ, which in general has 22O(|φ|) states. Therefore, our specialised GFM construction for repeated reachability property GFφ can be exponentially more efficient than current approaches.

## 7 Experiments for GFM state reduction

In this section, we validate the performance of our GFM state-space reduction on LTL specifications extracted from literature, which we define blow. The full benchmark set, with consistent state-space reductions on complex LTL specifications from over 8 sources, is in the extended version. Trigger with Delayed Response (TDR). This pattern requires a followed by b after n steps, to hold infinitely often. We define this fragment as TDR[n] = GF(a ∧Xnb) where Xn denotes n nested applications of the next operator. Liberouter (LIB). An example from the Liberouter verification project (Holeˇcek et al. 2004) checks liveness of binary signals, ensuring at least one signal does not become permanently stuck. Formally, LIB[n] = GF((a ∧X¬a) ∨(¬a ∧ Xa)∨(b∧X¬b)∨(¬b∧Xb)...), with n numbers of signals. Bounded Retransmission Protocol (BRP). Based on

36462

<!-- Page 7 -->

(Baier et al. 2023), BRP models that whenever a message is sent, a corresponding acknowledgement must occur within a bounded number of steps. BRP[n] = G("msg sent" → F("ack send" ∧φn)), where the subformula φn ensures that "ack rev" occurs within n steps after "ack send". We define φn = "ack rev" ∨X("ack rev" ∨X(· · · ∨ X("ack rev"))) with X applied n times. A smaller n enforces stricter guarantees, while a larger n relaxes them. Etessami–Holzmann Patterns (EHP). To evaluate the effectiveness of B¨uchi automata optimisations, (Etessami and Holzmann 2000) present deeply nested specifications. One formula is given by EHP = aU(b ∧X(c ∧F(d ∧XF(e ∧ XF(f ∧XFg))))). It expresses that condition a must hold continuously until a specific sequence of events is triggered. Nested Until Dependencies (NU). We define the nesteduntil pattern NU[n] = G(p1 →φn) where φk is recursively defined by φk = pkUφk+1 for k < n, and φn = pnUpn+1. This pattern was used in the runtime verification benchmarks for SystemC models (Tabakov, Rozier, and Vardi 2012). Layered Fairness and Reachability (LFR). As part of their evaluation, (M¨uller and Sickert 2017) introduced LFR[n] = F(b1) ∧(F(b2 ∧... F(bn)) ∧GF(a1 ∧X(a2 ∧... X(an))). The left-hand conjunct captures a nested reachability, while the right-hand side encodes a fairness condition, requiring a1,..., an to reoccur, with strict temporal progression.

## Experiment

Setup. In order to translate these LTL specifications to GFM automata, we use two state-of-the-art approaches. Owl (Kret´ınsk´y, Meggendorfer, and Sickert 2018), which we denote by Owl, and the “slim” GFM construction of (Hahn et al. 2020), which we implemented ourselves and denote by Slim. We refer to reduced Owl automata as Owl-Red and to reduced “slim” automata as Slim-Red. We use SPOT (Duret-Lutz 2013) for parts of patterns, for the GFG minimisation and we have used LTL datasets available in the Owl repository. All experiments were run on an 8-core ARM chip, with 16GB of RAM.

Results. Table 1 compares automata states before and after our reduction. We report the LTL to GFM construction time (in seconds) for Owl and Slim, and reduction time (excluding initial construction) for Owl-Red and Slim-Red.

Across all LTL patterns, the smallest automata (marked in bold) are consistently reduced ones. Owl features advanced formula simplification and post-processing optimisations and therefore constructs smaller automata than the “slim” GFM construction. Since our “slim” GFM construction is not as optimised as Owl, we can consistently reduce the state space of all “slim” GFMs and for cases like TDR and LFR, we obtain smaller Slim-Red than Owl-Red.

Note that for LFR, Owl returns incomplete automata, while our reduction returns complete ones with an explicit sink (see extended version). For the remaining cases NU, EHP, BRP and LIB, the smallest automata are our Owl-Red. More results, are in the extended version.

8 Experiments for GFφ

The first two LTL specification patterns above, namely TDR and LIB, refer to formulas that have the syntactic GFφ

Pattern Owl-Red Slim-Red GFM-GF

TDR[6] 64 (0.49) 34 (0.10) 7 (0.08) TDR[7] 128 (0.61) 66 (0.14) 8 (0.08) TDR[8] 256 (1.17) 130 (0.19) 9 (0.08) TDR[9] 512 (4.27) 258 (0.48) 10 (0.10) TDR[10] 1024 (23.67) 514 (0.91) 11 (0.09)

LIB[6] 14 (0.63) 66 (129.03) 13 (0.09) LIB[7] 16 (1.47) timeout 15 (0.12) LIB[8] 18 (5.95) timeout 17 (0.20) LIB[9] 20 (37.78) timeout 19 (0.23)

**Table 2.** State and runtime (in seconds) comparison of our direct construction GFM-GF against our reduced automata, Owl-Red and GFM-Red. The runtime for Owl-Red and GFM-Red includes construction and consecutive application of our reduction (in seconds). Timeout is 300 seconds.

structure and therefore, we can use them to evaluate our direct GFM automata construction. In particular, we show below that the direct construction gives us a large improvement with respect to the standard state-of-the-art GFM constructions (Kret´ınsk´y, Meggendorfer, and Sickert 2018; Hahn et al. 2020), even after applying our GFM reduction.

## Experiment

Setup. Table 2 compares our direct GFM construction (denoted by GFM-GF) to the automata obtained by our GFM state-space reduction. Again, we denote number of states of reduced Owl and “slim” GFM automata (Owl-Red, Slim-Red) but in contrast to Table 1, the runtime (in seconds), now contains both LTL to GFM construction and subsequent application of our reduction.

Results. For the LTL pattern TDR, Table 2 clearly shows that our direct construction GFM-GF, significantly outperforms both Owl-Red and Slim-Red, both in state size and runtime. Even when comparing the state size and construction time of GFM-GF to Owl and Slim, we can build exponentially more succinct automata, in a fraction of the time. For the LIB pattern, GFM-GF builds automata with a similar amount of states than Owl-Red, but again, we only require a fraction of the time. LIB[7] and LIB[8] timed out during reduction, while LIB[9] timed out during automata construction. More results, are in the extended version.

## 9 Conclusion

We conclude the paper by observing that our results immediately have an impact on a wide range of applications that use GFM automata, such as obtaining smaller strategies for planning problems, improving the efficiency of probabilistic verification (Hahn et al. 2015; Sickert and Kret´ınsk´y 2016), and reinforcement learning (Hahn et al. 2020; Jackermeier and Abate 2025). Furthermore, our results can be used to reduce the GFM automata obtained from variants of LTL, including LTLf+ and PPLTL+ recently proposed in (Aminof et al. 2025; De Giacomo et al. 2025).

36463

<!-- Page 8 -->

## Acknowledgements

We would like to thank the anonymous reviewers for their constructive feedback, that helped improve the paper. This work was supported in part by the CAS Project for Young Scientists in Basic Research (Grant No. YSBR- 040), ISCAS Basic Research (Grant Nos. ISCAS-JCZD- 202406, ISCAS-JCZD-202302), ISCAS New Cultivation Project ISCAS-PYFX-202201, the UKRI Erlangen AI Hub on Mathematical and Computational Foundations of AI (No. EP/Y028872/1) and by the EPSRC through grants EP/X03688X/1 and EP/X042596/1.

## References

Aminof, B.; De Giacomo, G.; Rubin, S.; and Vardi, M. Y. 2025. LTLf+ and PPLTL+: Extending LTLf and PPLTL to Infinite Traces. In IJCAI. Bacchus, F.; Boutilier, C.; and Grove, A. J. 1996. Rewarding Behaviors. In AAAI/IAAI, Vol. 2, 1160–1167. AAAI Press / The MIT Press. Bacchus, F.; Boutilier, C.; and Grove, A. J. 1997. Structured Solution Methods for Non-Markovian Decision Processes. In AAAI/IAAI, 112–117. AAAI Press / The MIT Press. Baier, C.; Gr¨oßer, M.; and Bertrand, N. 2012. Probabilistic ω-automata. J. ACM, 59(1): 1:1–1:52. Baier, C.; and Katoen, J. 2008. Principles of model checking. MIT Press. Baier, C.; Kiefer, S.; Klein, J.; M¨uller, D.; and Worrell, J. 2023. Markov chains and unambiguous automata. J. Comput. Syst. Sci., 136: 113–134. Brafman, R. I.; and Giacomo, G. D. 2024. Regular decision processes. Artif. Intell., 331: 104113. Chang, E. Y.; Manna, Z.; and Pnueli, A. 1992. Characterization of Temporal Property Classes. In ICALP, volume 623 of Lecture Notes in Computer Science, 474–486. Springer. de Alfaro, L. 1997. Formal verification of probabilistic systems. Ph.D. thesis, Stanford University, USA. De Giacomo, G.; Li, Y.; Schewe, S.; Weinhuber, C.; and Yu, P. 2025. Solving MDPs with LTLf+ and PPLTL+ Temporal Objectives. In IJCAI. De Giacomo, G.; and Vardi, M. Y. 2013. Linear Temporal Logic and Linear Dynamic Logic on Finite Traces. In IJCAI, 854–860. IJCAI/AAAI. Duret-Lutz, A. 2013. Manipulating LTL Formulas Using Spot 1.0. In ATVA, volume 8172 of Lecture Notes in Computer Science, 442–445. Springer. Esparza, J.; and Kret´ınsk´y, J. 2014. From LTL to Deterministic Automata: A Safraless Compositional Approach. In CAV, volume 8559 of Lecture Notes in Computer Science, 192–208. Springer. Etessami, K.; and Holzmann, G. J. 2000. Optimizing B¨uchi Automata. In CONCUR, volume 1877 of Lecture Notes in Computer Science, 153–167. Springer. Hahn, E. M.; Li, G.; Schewe, S.; Turrini, A.; and Zhang, L. 2015. Lazy Probabilistic Model Checking without Determinisation. In CONCUR, volume 42 of LIPIcs, 354–367. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik.

Hahn, E. M.; Perez, M.; Schewe, S.; Somenzi, F.; Trivedi, A.; and Wojtczak, D. 2020. Good-for-MDPs Automata for Probabilistic Analysis and Reinforcement Learning. In TACAS (1), volume 12078 of Lecture Notes in Computer Science, 306–323. Springer. Henzinger, T. A.; and Piterman, N. 2006. Solving Games Without Determinization. In CSL, volume 4207 of Lecture Notes in Computer Science, 395–410. Springer. Henzinger, T. A.; Prakash, A.; and Thejaswini, K. S. 2025. Resolving Nondeterminism with Randomness. In Gawrychowski, P.; Mazowiecki, F.; and Skrzypczak, M., eds., 50th International Symposium on Mathematical Foundations of Computer Science, MFCS 2025, August 25-29, 2025, Warsaw, Poland, volume 345 of LIPIcs, 57:1–57:18. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik. Holeˇcek, J.; Kratochv´ıla, T.; ˇReh´ak, V.; ˇSafr´anek, D.;

ˇSimeˇcek, P.; et al. 2004. Verification results in Liberouter project. Jackermeier, M.; and Abate, A. 2025. DeepLTL: Learning to Efficiently Satisfy Complex LTL Specifications for Multi- Task RL. In International Conference on Learning Representations (ICLR). Klein, J.; M¨uller, D.; Baier, C.; and Kl¨uppelholz, S. 2014. Are Good-for-Games Automata Good for Probabilistic Model Checking? In LATA, volume 8370 of Lecture Notes in Computer Science, 453–465. Springer. Kret´ınsk´y, J.; Meggendorfer, T.; and Sickert, S. 2018. Owl: A Library for ω-Words, Automata, and LTL. In ATVA, volume 11138 of Lecture Notes in Computer Science, 543–550. Springer. Kwiatkowska, M. Z.; Norman, G.; and Parker, D. 2011. PRISM 4.0: Verification of Probabilistic Real-Time Systems. In CAV, volume 6806 of Lecture Notes in Computer Science, 585–591. Springer. Lacerda, B.; Parker, D.; and Hawes, N. 2014. Optimal and dynamic planning for Markov decision processes with cosafe LTL specifications. In IROS, 1511–1516. IEEE. Li, Y.; Paul, S.; Schewe, S.; and Tang, Q. 2025. Accelerating Markov Chain Model Checking: Good-for-Games Meets Unambiguous Automata. In Piskac, R.; and Rakamari´c, Z., eds., CAV, volume 15932 of Lecture Notes in Computer Science, 276–298. Springer. Littman, M. L. 1997. Probabilistic Propositional Planning: Representations and Complexity. In AAAI/IAAI, 748–754. AAAI Press / The MIT Press. Littman, M. L.; Goldsmith, J.; and Mundhenk, M. 1998. The Computational Complexity of Probabilistic Planning. J. Artif. Intell. Res., 9: 1–36. Manna, Z.; and Pnueli, A. 1990. A Hierarchy of Temporal Properties. In PODC, 377–410. ACM. Meyer, P. J.; Sickert, S.; and Luttenberger, M. 2018. Strix: Explicit Reactive Synthesis Strikes Back! In CAV (1), volume 10981 of Lecture Notes in Computer Science, 578–586. Springer. M¨uller, D.; and Sickert, S. 2017. LTL to Deterministic Emerson-Lei Automata. In GandALF, volume 256 of EPTCS, 180–194.

36464

<!-- Page 9 -->

Pnueli, A. 1977. The Temporal Logic of Programs. In FOCS, 46–57. IEEE Computer Society. Radi, B. A.; and Kupferman, O. 2022. Minimization and Canonization of GFG Transition-Based Automata. Log. Methods Comput. Sci., 18(3). Safra, S. 1988. On the Complexity of omega-Automata. In FOCS, 319–327. IEEE Computer Society. Schillinger, P.; B¨urger, M.; and Dimarogonas, D. V. 2019. Hierarchical LTL-task mdps for multi-agent coordination through auctioning and learning. The international journal of robotics research. Sickert, S.; Esparza, J.; Jaax, S.; and Kret´ınsk´y, J. 2016. Limit-Deterministic B¨uchi Automata for Linear Temporal Logic. In CAV (2), volume 9780 of Lecture Notes in Computer Science, 312–332. Springer. Sickert, S.; and Kret´ınsk´y, J. 2016. MoChiBA: Probabilistic LTL Model Checking Using Limit-Deterministic B¨uchi Automata. In ATVA, volume 9938 of Lecture Notes in Computer Science, 130–137. Tabakov, D.; Rozier, K. Y.; and Vardi, M. Y. 2012. Optimized temporal monitors for SystemC. Formal Methods Syst. Des., 41(3): 236–268. Thi´ebaux, S.; Gretton, C.; Slaney, J. K.; Price, D.; and Kabanza, F. 2006. Decision-Theoretic Planning with non- Markovian Rewards. J. Artif. Intell. Res., 25: 17–74. Vardi, M. Y.; and Wolper, P. 1986. An Automata-Theoretic Approach to Automatic Program Verification (Preliminary Report). In LICS, 332–344. IEEE Computer Society. Yang, C.; Littman, M. L.; and Carbin, M. 2022. On the (In)Tractability of Reinforcement Learning for LTL Objectives. In IJCAI, 3650–3658. ijcai.org. Yu, P.; Li, Y.; Parker, D.; and Kwiatkowska, M. 2025. Planning with Linear Temporal Logic Specifications: Handling Quantifiable and Unquantifiable Uncertainty. CoRR, abs/2502.19603.

36465
