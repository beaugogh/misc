---
title: "Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schrödinger Bridges"
source_url: https://icml.cc/virtual/2026/oral/71076
paper_pdf_url: https://arxiv.org/pdf/2605.10917v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schrödinger Bridges

<!-- Page 1 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Usman A. Khan 1 2 3 Joseph W. Durham 1

## Abstract

We consider anonymous multi-agent path finding (MAPF) where a set of robots is tasked to travel to a set of targets on a finite, connected graph. We show that MAPF can be cast as a special class of multi-marginal optimal transport (MMOT) problems with an underlying Markovian structure, under which the exponentially large MMOT collapses to a linear program (LP) polynomial in size. Focusing on the anonymous setting, we establish conditions under which the corresponding LP is feasible, totally unimodular, and consequently, yields min-cost, integral ({0, 1}) transports that do not overlap in both space and time. To adapt the approach to large-scale problems, we cast the MAPF-MMOT in a probabilistic framework via Schr¨odinger bridges. Under standard assumptions, we show that the Schr¨odinger bridge formulation reduces to an entropic regularization of the corresponding MMOT that admits an iterative Sinkhorn-type solution. The Schr¨odinger bridge, being a probabilistic framework, provides a shadow (fractional) transport that we use as a template to solve a reduced LP and demonstrate that it results in near-optimal, integral transports at a significant reduction in complexity. Extensive experiments highlight the optimality and scalability of the proposed approaches.

## 1. Introduction

Coordinating large teams of robots to reach target locations while avoiding collisions in space and time is a fundamental problem in robotics and automation. In multi-agent path finding (MAPF), robots are assigned to targets on a shared graph and must compute collision-free trajectories

1Amazon Robotics, Boston, MA, USA. 2Boston College, Chestnut Hill, MA, USA. 3UAK holds concurrent appointments as an Amazon Scholar with Amazon Robotics and as a Professor of Computer Science at Boston College. Correspondence to: Usman A. Khan <uakhan@amazon.com, usman.khan@bc.edu>.

Preprint. May 12, 2026.

that are jointly optimal in both space and time. This coupling of assignment, path planning, and scheduling renders MAPF combinatorial in nature. In this paper, we show that MAPF can be cast as multi-marginal optimal transport (MMOT) over path spaces with an underlying Markovian structure. Focusing on the anonymous setting, where any robot may reach any target, we show that the resulting Markovian MMOT admits a polynomial-size linear program (LP) with strong optimality and integrality guarantees (extensions to non-anonymous settings are possible via more general MMOT formulations). We then use ideas from the Schr¨odinger bridge framework and develop an entropic regularization of the corresponding MMOT to build scalable, probabilistic relaxations of the MAPF problem. The main contributions of this paper are as follows.

• We show that MAPF is a special class of Markovian MMOT, which admits a polynomial-size LP with a totally unimodular constraint matrix in the anonymous setting; subsequently, all extreme points of the feasible polyhedron are integral ({0, 1}). We further derive the conditions under which the proposed min-cost LP yields min-move and min-makespan transports.

• We connect the MAPF-MMOT to Schr¨odinger bridges, which enable transports with desirable structural properties through appropriate reference distributions. By choosing the reference as a Gibbs kernel, the Schr¨odinger bridge reduces to an entropic regularization of the MAPF-MMOT enabling Sinkhorn-type fast iterations. The resulting Sinkhorn-MAPF provides a shadow transport, a set of likely paths from robots to targets. As the Gibbs parameter ε →0, the Schr¨odinger bridge associated with a highly volatile reference Markov chain concentrates onto tight, mincost geodesic corridors of the underlying graph.

• We use the shadow transport to guide a principled pruning of the underlying graph, resulting in an LP defined on a substantially reduced graph while preserving the totally unimodular structure of the feasible polyhedron. Because the Schr¨odinger bridge leads to a shadow cast on highly likely paths, the resulting pruned formulation is both scalable and integral. Experiments show arXiv:2605.10917v1 [cs.LG] 11 May 2026

<!-- Page 2 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges that as problem size grows, the resulting LP incurs less than 10% cost degradation while eliminating approximately 60–80% of the edges of the original graph.

Related Work: A comprehensive survey on MAPF can be found in (Stern, 2019); see also (Ma & Koenig, 2016; Peng et al., 2023; Ali & Yakovlev, 2023; Fine et al., 2023) for some recent results on anonymous MAPF. Representative algorithmic baselines for optimal MAPF include Conflict- Based Search, see e.g., (Sharon et al., 2015; Felner et al., 2017), as well as SAT-based formulations (Surynek, 2015). Prior work via time-expanded flow networks and integer programs can be found in (Yu & LaValle, 2013; Ma, 2020); however, this line of work does not explicitly characterize the integrality of MAPF solutions as a polyhedral property of the associated LP. In contrast, our MAPF–MMOT formulation establishes integrality of the resulting LP from first principles via total unimodularity (Schrijver, 1986; Ahuja et al., 1993). The proposed MMOT viewpoint is novel and further enables extensions to probabilistic formulations. In particular, we generalize MAPF-MMOT to the Schr¨odinger bridge problem where the goal is to find a robot distribution P over path spaces that is close to a given reference G. Key references in this direction include: (L´eonard, 2014), which surveys the Schr¨odinger problem and its connections to OT; (Pavon & Ticozzi, 2010) on discrete-time Markovian bridges; and (Haasler et al., 2021) on tree-structured costs. MMOT and its computational aspects are discussed in (Pass, 2015; Lin et al., 2022; Haasler et al., 2023). Related work on multi-marginal Sinkhorn methods can be found in (Benamou et al., 2015; Di Marino & Gerolin, 2020; Carlier, 2022). Of relevance is also the body of work in (Chen et al., 2016; 2017; 2021) that casts Schr¨odinger bridges within a stochastic control framework.

## 2. Background and Problem Formulation

In this section, we provide some preliminaries and formally write the multi-agent path finding (MAPF) problem.

Multi-Marginal OT: Multi-marginal optimal transport (MMOT) extends the classical two-marginal OT problem to multiple marginals. The transport here is not therefore between two measures but a coupling across more than two measures. Formally, consider a joint probability tensor P ∈RK×...×K, with T + 1 modes, each with K supports, and a transport cost tensor C of the same dimensions. Given T +1 marginals q0, q1,..., qT, the MMOT problem is to find a min-cost transport plan (coupling), i.e., min P≥0⟨P, C⟩ subject to ϕt(P) = qt, ∀t ∈0,..., T, such that all elements of P sum to 1, where ⟨·, ·⟩denotes the inner product and ϕt is the (linear) projection of the joint distribution P on its t-th marginal, given to be qt. A generalization to compactly supported Borel measures on smooth manifolds can be found in (Pass, 2015). Clearly, the discrete MMOT problem is a linear program with KT +1 variables in the transport tensor P. It has been shown that for T ≥2, combinatorial algorithms like the simplex methods no longer remain suitable (Lin et al., 2022). Because of the exponential state-space, recent work has studied convex relaxations using e.g., Sinkhorn iterations (Lin et al., 2022; Haasler et al., 2023).

From MMOT to MAPF: We now establish a connection between multi-agent path finding (MAPF) and MMOT problems. Consider a finite, bounded region of interest Ω⊂R2 in which N robots operate. We discretize Ωinto cells, each no smaller than a robot, and define a graph G = (V, E) whose vertices V correspond to cells and whose edges E connect adjacent cells between which a robot can transition in one time step. The resulting graph is finite, and the cell size ensures that each vertex is occupied by at most one robot at any time. Let |V| = K and let N robots in the set N occupy some vertices in V and travel on the edges E, over a time horizon T. The goal for the robots is to reach a set M of M distinct targets, also in V, such that M = N, while minimizing the travel cost and/or the travel time to reach those targets1. This setup is standard in the discrete MAPF literature; see, e.g., (Stern, 2019; Yu & LaValle, 2013; Standley, 2010). We further let µ = {µi} and ν = {νj}, both in RK, denote the initial distributions of N robots and targets, respectively, on K vertices.

Let (Xt)T t=0 be a discrete-time stochastic process with statespace {1,..., K}, where each state corresponds to a vertex of the graph G. In other words, (Xt)T t=0 is a possible trajectory taken by a robot over the time horizon T. Let P ∈RK×···×K

≥0 be a (T + 1)-th order tensor representing a distribution on path space. In particular, each entry Pi0,...,iT denotes the probability or the amount of mass (normalized to sum to one) assigned to a complete trajectory X0 = i0, X1 = i1,..., XT = iT, that is, the path i0 →i1 →· · · →iT over the time horizon t = 0,..., T, with it ∈V. Thus, P assigns mass directly to entire spacetime trajectories rather than to individual vertices or edges. The collective motion of all N robots, over the horizon T, is encoded in this joint path-space distribution and its one-time marginals qt recover the robot locations at each time. We have P i0,...,iT Pi0,...,iT = 1 and

K X i0=1

· · ·

K X it−1=1

K X it+1=1

· · ·

K X iT =1

Pi0,...,iT = 1

N [qt]it, (1)

with fixed endpoint distributions q0 = µ and qT = ν.

1For simplicity, we assume that the number of robots and targets are equal. Extensions to the unequal cases can be easily considered using unbalanced/partial OT but is beyond the scope of this exposition.

<!-- Page 3 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

From the path-space tensor P, the transport between consecutive time layers is obtained as a two-marginal. Specifically, the transport matrix Πt from time t −1 to t is defined by

[Πt]it−1,it = N

K X i0=1

· · ·

K X it−2=1

K X it+1=1

· · ·

K X iT =1

Pi0,...,iT, which represents the total mass (or joint probability) at vertex it−1 at time t −1 and at vertex it at time t, aggregated over all past (before t −1) and future (after t) evolution. Clearly, since robot motion is causal in time, the process (Xt)T t=0 is Markovian, i.e., for all t > 0,

P(Xt = u | Xt−1 = v,..., X0 = w)

= P(Xt = u | Xt−1 = v), for all u, v, w ∈V, and therefore the joint path-space tensor P admits the standard factorization:

Pi0,...,iT = P(iT | iT −1) ·... · P(i1 | i0) · P(i0)

= 1

N [q0]i0

T Y t=1

1 N [Πt]it−1,it

1 N [qt−1]it−1

. (2)

Given a cost tensor C, with costs on each possible trajectory, the MAPF problem is to find N robot trajectories to targets that minimize travel cost or travel time. In this paper, our interest is to exploit the aforementioned probabilistic interpretation of P and deploy MMOT and its efficient relaxations for MAPF. To our advantage, the Markovian factorization of the joint tensor reduces the number of free variables from KT +1, exponential in T, to K2T, polynomial in T. Additionally, the general MMOT relaxes from fixing T + 1 marginals to only two boundary marginals: the starting distribution q0, which is where the robots are located, and the ending distribution qT, where the targets are located. The intermediate marginals q1,..., qT −1, consequently, define the positions the robots take when traveling from their starting locations to their destinations and are free under appropriate Markovianity/causality constraints as we will explicitly capture in the next section. This approach however comes at a price as MMOT, being a probabilistic object, does not necessarily result into integral 1

N {0, 1} transports. In other words, the transports may be fractional and the robots may split while traveling to the targets.

Building on this problem formulation, the remainder of the paper is organized as follows.

• Section 3 focuses on integral and optimal solutions of the proposed MAPF-MMOT. In particular, we show that the corresponding LP (P1) is totally unimodular under mild structural assumptions; consequently, all robots take non-conflicted, non-fractional paths to their targets. We further identify when these paths are minimum cost and/or minimum makespan.

• Section 4 builds towards scalability by casting MAPF as a probabilistic Schr¨odinger bridge and derives the corresponding entropic formulation and Sinkhorn- MAPF iterations (Appendix G). The main idea is to efficiently obtain a fractional (shadow) transport that concentrates mass on the most likely paths.

• Section 5 then recovers integrality from the shadow transports by solving a variation of the base P1 LP on a reduced graph obtained from the Schr¨odinger bridge, while Section 6 and 7, respectively, provide complexity analysis and a comprehensive set of experiments.

## 3. Integral and Optimal Solutions for MAPF

Recall the problem formulation in Section 2 where µ and ν (robot and target locations) are such that µi =

(

1, i ∈N, 0, otw. νj =

(

1, j ∈M, 0, otw.

with ∥µ∥1 =∥ν∥1 =N. Note that the (t −1) →t transport plan Πt = {πij,t} ∈RK×K contains the robot distributions at time t −1 and t as marginals, i.e., qt−1 = Πt1, 1⊤Πt = q⊤ t, t = 1,... T, where πij,t is the amount of mass transported from vertex i, at time t −1, to vertex j, at time t. Our goal is to find the optimal transport plans {Πt}T t=1 that moves the robots (mass at source distribution µ) to the targets (mass at destination distribution ν) over the time horizon T. Recall that C is the cost tensor and let Ct = {cij,t} denote the cost matrix at time t such that the cost of traveling on an edge i →j, starting at t −1 and arriving at t, is cij,t. We impose the following structural assumptions throughout this paper; see, e.g., (Stern, 2019; Yu & LaValle, 2013; Standley, 2010) for similar setups.

Assumption 3.1. The graph G and cost matrices Ct satisfy the following:

(i) Self-loops i →i ∈E, for all i ∈V, are always present.

Consequently, waiting at any vertex is always feasible.

(ii) If two edges in G do not share a common endpoint, the corresponding physical motions can be executed simultaneously without conflict. In addition, an edge i→j is included in G only if its traversal is independent of the occupancy of all vertices other than i and j.2

(iii) For each i →j ∈E, the cost cij,t < ∞, ∀t, while cij,t = +∞, ∀(i, j) /∈E.

2This abstraction is a standard safeguard in cooperative path finding literature; see, e.g., (Standley, 2010). If needed, one may refine the graph so that collision-relevant interactions occur only at shared vertices; or on grid graphs, diagonal motion is disallowed.

<!-- Page 4 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

(iv) We assume that Ci0,...,iT = PT t=1 cit−1it,t, i.e., the path cost is additive across time.

(v) The cost matrix satisfies the following, ∀t = 1,..., T:

0 = cjj,t, j ∈M < cii,t, i /∈M < cij,t, i̸ = j.

The graph structure imposed in Assumption 3.1(i)-(ii) ensures that the discretization faithfully captures the physical constraints of robot motion: edges and vertices cannot be added arbitrarily if they result in conflicts. Violating (i) or (ii) would mean the graph does not correctly model the physical environment, and collisions invisible to the discretized formulation may arise. The cost Assumption 3.1(v) is natural: a move expends strictly more energy than a wait, and waiting at a target is free. We emphasize that Assumption 3.1 does not require a grid graph or point-mass robots. Any finite, connected graph G satisfying (i)-(ii) suffices, and the LP formulation and its guarantees developed in the sequel hold for any such G.

Under Assumption 3.1(iv), the tensor inner product ⟨P, C⟩ reduces to a sum over local transports and costs. Subsequently, because of the Markovian restriction on P, the multi-marginal optimal transport formulation of anonymous MAPF can be equivalently written as follows:

P1: {Π∗ t }T t=1 = argmin{Πt}T t=1

T X t=1

⟨Πt, Ct⟩ subject to F:=

    

   

Πt ≥0, Π⊤ t 1 = Πt+11, ∀t = 1,..., T, Π11 = µ, Π⊤

T 1 = ν, 0 ≤Π⊤ t 1 ≤1, ∀t = 1,..., T −1,

We explain this MMOT formulation next:

• P1 is a linear program with linear constraints, in which the transport plans Πt’s are real-valued nonnegative decision variables (not necessarily integral).

• Gluing constraints: The second set of equality constraints impose a Markovian restriction to the global MMOT problem. They ensure that the mass transported from t to t + 1, must be the mass that arrives at t from t −1, i.e., Πt+11 = qt and also Π⊤ t 1 = qt.

• Terminal constraints: The boundary marginals are fixed to enforce the robots initial and terminal positions.

• Vertex-capacity constraints: The last inequality constraints ensure that no location (vertex in G) receives more than one robot.

Clearly, if Πt’s are integral, i.e., πij,t ∈{0, 1}, ∀i, j, t, then we get executable robot paths to the targets. Assumption 3.1 and the constraint polyhedron F further ensure that all targets are reached, while the robot trajectories are nonconflicting and min-cost. We characterize these results next.

## 3.1. Main Results

We now characterize some basic properties of P1 in the following lemmas.

Lemma 3.2. Let G = (V, E) be a finite, connected graph with |V| = K. Consider N robots in N and M targets in M, on distinct vertices in G, such that N = M ≤K/2. For each time t ∈N, let Ct = {ci,j,t} satisfy Assump- tion 3.1. Then, there exist a finite ¯T ∈N and a transport {Πt} ¯T t=1 feasible for P1, i.e., satisfying all constraints in F, such that P ¯T t=1⟨Πt, Ct⟩< ∞.

The proof is provided in Appendix A. Lemma 3.2 establishes the feasibility of anonymous MAPF and the constraint set F and does so purely at a structural level, without invoking any properties of the corresponding linear program (LP) beyond Assumption 3.1. The following lemma now concretely establishes the properties of the LP in P1.

Lemma 3.3. Consider the settings of Lemma 3.2 and Assumption 3.1, and fix a horizon ¯T such that F is nonempty with P ¯T t=1⟨Πt, Ct⟩< ∞, for some feasible {Πt}t. Then, the MMOT formulation P1 over the horizon ¯T satisfies:

(i) P1 admits an optimal solution {Π∗ t } ¯T t=1 that is integral, i.e., Π∗ t ∈{0, 1}K×K, for all t = 1,..., ¯T.

(ii) P1 results in a transport {Π∗ t } ¯T t=1 that attains a minimum cost over the horizon ¯T.

(iii) The complexity of P1 is polynomial in K and ¯T.

The proof is provided in Appendix B, where we show that P1 admits an optimal integral basic solution, as a consequence of total unimodularity of the constraint matrix (Schrijver, 1986). The result can also be viewed through the lens of classical integrality arguments for network flows (Ford. & Fulkerson, 1962; Ahuja et al., 1993). Regarding (iii), see Section 6 for precise complexity arguments. The next theorem uses the results of the previous two lemmas and applies them to the anonymous MAPF problem.

Theorem 3.4. Consider the settings of Lemmas 3.2, 3.3, and Assumption 3.1. The optimal transport plan {Π∗} ¯T t=1, returned by P1, satisfies:

(i) No two robots collide at any time.

(ii) The robot trajectories do not overlap in both space and time.

(iii) All robots reach a distinct target.

<!-- Page 5 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Theorem 3.4, proved in Appendix C, is one of the central results of this paper. It establishes the conditions under which MMOT gives executable robot trajectories, i.e., {0, 1} transports, relying on the total unimodularity (TU) of P1. TU in general is delicate, and adding arbitrary constraints to enforce a desirable behavior on robot trajectories typically breaks TU. It is therefore preferable to impose desirable traits in the trajectories through the cost matrices {Ct}t. We next describe a few of such desirable properties enforced via costs, in addition to Assumption 3.1; it can be verified that they do not violate Lemma 3.3 and Theorem 3.4.

No oscillations: For all distinct vertices i̸ = j ∈V, and all t, let cii,t + cii,t+1 < cij,t + cji,t+1. In other words, leaving i and returning to it, now or later, costs more than staying at i. Temporal urgency: For all i →j ∈E, all t, and all feasible moves, let cij,t ≤cij,t+1. Thus, executing a move is never cheaper later. Combined with Assumption 3.1(v), this implies that whenever a robot can reach a target earlier, there exists an optimal transport in which it does so and subsequently waits at the target. Temporal subadditivity: For all i, j, k ∈V and all t, let cij,t ≤cik,t + ckj,t+1. Thus, whenever a direct move from i to j is available, routing through an intermediate vertex over consecutive time steps is never cheaper. This rules out avoidable detours: if a robot can move directly to a vertex and then wait, it is never optimal to reach the same vertex via an unnecessary intermediate location. The two temporal conditions described above should not be used in scenarios, e.g., where a toll road becomes cheaper later (within the horizon ¯T) and the goal is to exploit that. Shortest-path costs: Assume that G is endowed with an edge-length metric d: E →R+ such that for all i →j ∈E and all t, cij,t = d(i, j). Under this cost structure, any minimum-cost transport minimizes the total traveled distance among all feasible transports. A canonical example is robots and targets embedded in R2, with d(i, j) given by the Euclidean distance.

Minimum Moves: It can be shown that given a feasible horizon ¯T, under transition costs ci̸=j,t = 1, for all t, and for sufficiently small waiting costs cii,t > 0, for i /∈M, a min-cost solution of P1 is also a min-move solution.

Minimum makespan: For any feasible transport {Πt} ¯T t=1, its makespan is the largest time-index for which πij,t > 0, for some i̸ = j. The minimum makespan is the smallest such value over all feasible transports. We next describe obtaining a minimum makespan transport from P1 by tuning costs with the help of the following assumption and lemma.

Assumption 3.5. Let {˜cij}i→j∈E satisfy ˜cjj = 0, j ∈M, and 0 < ˜cii,i/∈M < ˜cij,i̸=j and define ˜cmin to be the minimum over all ˜cij, with i̸ = j. Choose Ct = {cij,t} to be such that cij,t:= B t ˜cij, ∀i →j ∈E, ∀t, where B is chosen to satisfy (B −1)˜cmin > P i→j∈E ˜cij.

Note that Assumption 3.5 imposes a much stronger growth condition on the costs. It can be further verified that it satisfies Assumption 3.1 and also implies the aforementioned no-oscillations and temporal cost conditions.

Lemma 3.6. Let G be finite and connected and consider Ct such that it satisfies Assumption 3.5. Suppose that ¯T is a feasible horizon for P1. Then, for any solution {Π∗ t } ¯T t=1 of P1, all robot motions terminate by T ∗, where T ∗is the minimum makespan over all feasible transports.

The proof is provided in Appendix D. Note that Lemma 3.6 provides a transport over the entire horizon ¯T and achieving minimum makespan is implicit. In other words, the robot motion ceases at T ∗because of rapidly growing timedependent costs. Such costs may cause numerical instability; to avoid that the following result explicitly searches for the minimum feasible horizon T ∗.

Lemma 3.7. For a feasible anonymous MAPF instance over a finite, connected graph G with |V| = K, the minimum makespan satisfies T ∗≤N + K −1. A minimum makespan transport can be found in O(log K) calls to P1.

The T ∗bound in this lemma can be found, e.g., in (Yu & LaValle, 2013; Ma, 2020). The rest of the lemma follows by performing a binary search over the horizon T ∈[0, N + K −1] and checking for the earliest feasibility of P1. We thus obtain two complementary approaches for computing minimum makespan transports in Lemmas 3.6 and 3.7. The exponential cost construction in Assumption 3.5 and consequently Lemma 3.6 implicitly encode the makespan optimality into the objective, at the expense of aggressive cost scaling. Alternatively, minimum makespan can be found explicitly by searching over the horizon, requiring O(log K) calls to P1 with simpler cost.

An alternate min-makespan formulation can be achieved by minimizing z, such that z ≥t πij,t, ∀i /∈M, j ∈V, t. However, the resulting LP is not totally unimodular in general. In other words, explicit makespan minimization requires integer programs, and therefore the implicit mechanism described here may be preferable.

The results in this section yield a polynomial-time LP for anonymous MAPF; see also Section 6. This complexity however may be impractical for very large-scale MAPF. In the subsequent sections, we develop scalable solutions for P1 by casting MAPF as a discrete Schr¨odinger bridge, which provides a principled probabilistic framework for formulating and analyzing MAPF (Section 4). This formulation, under appropriate conditions, leads to a convex Problem P2, which we show is an entropic relaxation of P1. The resulting P2 admits highly efficient Sinkhorn-type iterations (Appendix G) but yields fractional (shadow) transports. Integrality is then enforced with a subsequent projection step to recover executable robot motions (Section 5).

<!-- Page 6 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

## 4 MAPF and the

Schr¨odinger Bridge Problem

The classical Schr¨odinger bridge is described as follows. Given a reference diffusion process G on a topological state space X, with arbitrary marginals, find a probability measure P ∗on the space of continuous trajectories that minimizes the relative entropy with respect to G:

P ∗= argminP KL(P ∥G), such that the measure P ∗has fixed initial and terminal marginals (Schr¨odinger, 1931; L´eonard, 2014). Here, G is typically chosen as Brownian motion and P ∗is the most plausible stochastic evolution whose continuous-time trajectories interpolate between the given boundary marginals. Schr¨odinger bridge formulations are widely used in applied physics and are typically studied in continuous settings to model the evolution of particle systems, see e.g., the hot and lazy gas experiments in (Villani, 2009; L´eonard, 2017). Originally introduced by Erwin Schr¨odinger in the 1930s, the Schr¨odinger bridge problem characterizes the path-space trajectories of gas particles from empirical observations of their distributions at two time instants, and is closely connected to large deviation theory, where Schr¨odinger bridges arise as minimizers of associated rate functionals (F¨ollmer, 1988). We now cast MAPF as a Schr¨odinger bridge and characterize the conditions under which this formulation reduces to the MAPF–MMOT problem P1.

For the remainder of the paper, we assume that T < ∞is a feasible horizon for P1. Recall the factorization of P in (2) and let G denote a reference Markovian tensor on V with a similar factorization, where Gt are the transports of the reference distribution G with marginals Gt1 = gt−1 and G⊤ t 1 = gt. The S¨chrodinger bridge problem corresponding to P1 seeks a joint distribution P, and the corresponding sequence of transports {Πt}T t=1, that is closest to G in the relative entropy sense, i.e., min P∈C KL(P∥G), (3)

where C is the set of tensors satisfying the constraints of P1 and each element of G is such that the KL divergence is well-defined.

Lemma 4.1. The Schr¨odinger bridge in (3) reduces to

KL(P∥G) =

T X t=1

KL(1

N Πt∥Gt) + KL(1

N q0∥g0)

−1

N

T X t=1

KL(1

N qt−1∥gt−1). (4)

The proof is provided in Appendix E. Note that the full Schr¨odinger bridge formulation decomposes into transport and marginal KL terms (4); a related decomposition is derived in (Pavon & Ticozzi, 2010) for the initial-final marginal problem using conditional transition probabilities. Eq. (4) represents the general form of the Schr¨odinger bridge, through which one may impose a desirable structure on the robot trajectories by appropriately choosing the reference transports Gt and marginals gt. Consequently, (4) returns a MAPF transport P that is consistent with the initial and final robot locations while remaining close to G. Existence and uniqueness of Schr¨odinger bridges are studied in (Pavon & Ticozzi, 2010), where a solution is derived using space–time harmonic functions under suitable assumptions on the reference processes. In the following, we restrict the reference distributions to the Gibbs form, which leads to Sinkhorn-type iterations.

Lemma 4.2. Let Ct = {cij,t} be the cost matrix and let Gt = {¯gij,t} be the normalized Gibbs kernel, i.e., ¯gij,t:= gij,t zt, gij,t:=exp

−cij,t ε

, and zt:= P k,ℓgkℓ,t. Then, for each t,

KL(1

N Πt∥Gt) = 1

N

X i,j

Πij,t log Πij,t

+ 1

N

X i,j

Πij,t cij,t ε + log 1

N + log zt.

The proof is provided in Appendix F. The above lemma leads to the following Schr¨odinger bridge formulation of MAPF, when the reference distribution G is the Gibbs kernel (after removing the constants that do not depend on the transport variables) and minimizing εN KL(1

N Πt∥Gt):

P2: min {Πt∈F}T t=1

T X t=1



⟨Πt, Ct⟩+ ε

X i,j πij,t(log πij,t −1)



 under the constraints of P1. We let {eΠt}T t=1 denote the transport resulted by P2 and note that P2 is precisely the entropic regularization of P1.

To obtain efficient and scalable solutions, P2 imposes the non-negativity constraints on the transport variables and allows Πt ≥0. This relaxation yields a convex problem that can be solved efficiently using Sinkhorn-type iterations. Under this relaxation, the marginal distributions induced by Πt may become fractional, and the marginal KL terms in the full Schr¨odinger bridge objective (Eq. (4)) may not remain constant. Consequently, P2 may no longer remain exactly equivalent to the Schr¨odinger bridge but can be interpreted as a tractable relaxation thereof. Solving the convex relaxation P2 yields fractional (shadow) transports, over which integrality can be imposed, as we will develop in Section 5. We provide the corresponding multi-marginal Sinkhorn iterations to build the fractional shadow transports eΠ in Appendix G. A formal discussion and analysis of Sinkhorn-MAPF is beyond the scope of this paper.

<!-- Page 7 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

## 5. Integral Projection of Sinkhorn-MAPF

To obtain an integral solution from the entropy-regularized transports {eΠt}T t=1, obtained from P2, we project eΠt’s back on the totally unimodular polyhedron F. To this end, we minimize a modified objective ⟨Πt, Ct⟩+ λ KL(Πt∥eΠt) that penalizes the transport Πt when it’s far from eΠt. Adding the KL penalty however makes the objective nonlinear, which we address by linearizing around an operating point π0 ij,t, yielding

KL(Πt∥eΠt) ≈

X i,j πij,t log π0 ij,t −log eπij,t

+

X i,j πij,t −

X i,j π0 ij,t.

Dropping constants and choosing π0 ij,t to be a constant over all i, j, we obtain

P3: min {Πt}T t=1

T X t=1



X i,j πij,t (cij,t −λ log(eπij,t + δ))



 subject to Πt ∈F, Πt ⊆[eΠt]η, ∀t, where δ ≥0 ensures the logarithm is well-defined, and [eΠt]η is the regularized transport eΠt with zeros for all elements that are at most η. We let {bΠt}T t=1 denote the transport resulted by P3, which is effectively built from the shadow transport P2, i.e, the entropic regularization of P1. We provide a few important remarks regarding P3 next:

• The constants λ, δ must be chosen carefully to ensure that the modified cost cij,t −λ log(eπij,t + δ) lies in the purview of Assumption 3.1. Clearly, {bΠt}t is integral {0, 1}, because P3 is an LP under the same feasibility polyhedron F of P1. However, the pruned graph or T may no longer remain feasible and η may need to be adjusted accordingly.

• The interplay between the three constants ε, λ, η straddle the spectrum of transports from optimal to highly scalable. Note that λ = η = 0, disconnects P2 (regardless of ε) and recovers P1.

• Choosing ε, λ > 0, independent of η, biases P3 to place mass on edges with large eπi,j,t, since the modified objective in P3 arises from a linearized KL divergence between bπi,j,t and eπi,j,t. Consequently, bπi,j,t may inherit the smoothing effect induced by P2 as ε ↑.

• A scalable recipe is apparent: solve convex P2 fast, build a shadow, and subsequently solve the P3 LP over a pruned graph (with appropriate choices of ε, η, λ, δ). A detailed breakdown of these parameters, based on 260 experiments on a 1.5M-variable problem, is provided in Appendix H.3.

## 6. Computation Complexity

The LP in Problem P1 returns T transport matrices {Πt}T t=1, each supported on |E| edges, resulting in n:= |E|T decision variables and O(n) constraints. On physical graphs with bounded-degree connectivity (e.g., nearest-neighbor motion), |E| = O(K) and thus n = O(KT). Using classical interior-point methods for linear programming, Problem P1 admits worst-case bit-complexity bounds of order O(n3L), where L is the encoding length of the input data. The corresponding methods may not return a basic optimal solution (a vertex of the constraint polyhedron); in such cases, standard crossover techniques can be used to recover an extremepoint solution (Wright, 1997; Potra & Wright, 2000). While these methods provide polynomial-time guarantees, practical implementations often rely on simplex-based methods, which perform significantly faster on large-scale instances despite lacking polynomial worst-case guarantees.

To improve scalability, P2 solves an entropic relaxation via Sinkhorn iterations (Appendix G) that are specialized to the MAPF problem and its constraints. The convergence and complexity of multi-marginal Sinkhorn are studied, e.g., in (Di Marino & Gerolin, 2020; Carlier, 2022), where linear convergence is established when the iterations are viewed as block coordinate descent on a convex dual objective. In practice, only a small number of Sinkhorn iterations suffices to construct the pruned graph used later in P3, as demonstrated in Section 7 and in the detailed experiments (Appendix H). Finally, Problem P3 solves the original linear program over the pruned graph and therefore has the same worst-case complexity bound as the aforementioned interior-point methods. However, due to the effective graph pruning based on the shadow transport of P2, the number of variables is significantly reduced, with n ≈ζ|E|T, where in practice ζ typically lies in the range [0.2, 0.4] for large-scale instances, as demonstrated in the experiments.

The above complexity bounds are worst-case limits. In practice, modern LP solvers such as Gurobi are highly optimized and we observe empirical solve time scaling as O(K1.68) for P1 and as O(K1.15) for the P2+P3 pipeline; see Fig. 4 and Appendix H.2 for a detailed scaling study.

## 7. Experiments

We consider a grid of size K =W ×H with potential obstacles; while the framework applies to arbitrary graphs, grids are chosen for simplicity. Motion is allowed in the cardinal directions, while diagonal motion is prohibited. Waiting costs 0 at targets and 0.5 at non-targets; move cost is ci̸=j = 1 for all i →j ∈E. The experiments are conducted using the HiGHS solver from the SciPy’s linprog library. Fig. 1 shows the min-cost P1 transport for two arbitrary configurations over T = 3; we note that arbitrar-

<!-- Page 8 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 1.** A 10 × 10 grid with {50, 25} robots ▲and targets •, and {0, 50} obstacles.

ily placed obstacles alter the connectivity and diameter of the underlying graph, and it no longer remains a regular grid. We next demonstrate the Schr¨odinger shadow transport (P2) in Fig. 2 on a 40 × 40 grid with {20, 80} robots and targets; all trajectories are superimposed. The left figures show the optimal integral transports P1; the middle figures show the (fractional) Sinkhorn-MAPF with ε = 50; while the right figures show integral P3 transports obtained on pruned graphs with nominal cost degradation. Finally, Fig. 3 demonstrates the cost degradation versus edges kept from the shadow transport on a K = W 2 grid with 2W robots. We observe that shadow-based pruning is much more effective and feasibility is obtained with smaller number of edges as K ↑with a nominal cost degradation.

To evaluate the runtime scaling, we switch to the Gurobi LP solver and conduct 162 independent runs on square grids ranging from K = 2,500 to K = 22,500 vertices at 5% robot density (N = 0.05K) and T = 30. Fig. 4 shows that P1 solve time grows as O(K1.68) while the P2+P3 pipeline scales nearly linearly as O(K1.15), yielding speedups from 3.6× to 7.1× with cost gap consistently below 10%. Every solution across all runs is verified integral. See Appendix H.2 for the full scaling study.

**Table 1.** reports the average cost gap (%) of the P2+P3 pipeline over 260 runs at K = 10,000 for varying (ε, λ). The regularization parameter ε is the dominant factor: small ε produces a concentrated shadow close to the P1 optimum, while λ has a milder effect. A robust default is ε = 0.2, λ = 0: a 4.3% gap at 5× speedup. See Appendix H.3 for the full sensitivity analysis.

**Table 1.** Average cost gap (%) relative to P1 for each (ε, λ) pair,

over 13 instances at K = 10,000, T = 30.

ε \ λ 0 0.5 1.0 5.0

0.1 2.3 2.5 2.7 3.0 0.2 4.3 5.0 5.8 7.3 0.5 11.1 12.7 14.0 16.5 1.0 17.3 18.9 20.1 23.1 5.0 17.1 18.0 18.7 19.9

## Appendix

H.4 validates the proposed approaches under nonuniform costs, and Appendix H.5 compares against the CBM baseline of (Ma & Koenig, 2016).

## 8. Conclusions

In this paper, we develop a principled framework for multiagent path finding (MAPF) that bridges multi-marginal optimal transport, entropy-regularized relaxations, and linear programming. By showing total unimodularity of the feasibility polyhedron, we obtain integral transports in polynomial time without explicitly enforcing integrality. We extend the methodology to Schr¨odinger bridges and entropic formulations that provide a novel probabilistic viewpoint of MAPF, yielding scalable approximations and structural guidance for reducing problem size. Building on this structure, the proposed projection and pruning strategies enable efficient recovery of executable transports, offering a flexible trade-off between tractability, smoothness, and optimality.

![Figure extracted from page 8](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 2.** (Left) Optimal P1; (Middle) Schr¨odinger shadow P2; (Right) Integral projection P3. Top (N = 20, T = 15): P1 cost 181; P2

cost 1053; P3 with 23% edges retained at cost 181, i.e., 0% degradation. Bottom (N = 80, T = 10): P1 cost 402; P2 cost 3160; P3 with 22% edges retained at cost 436, i.e., 8.5% degradation.

**Figure 3.** Scalable MAPF: The vertical axis plots the cost degradation x, i.e., the cost of transport obtained from P3 is (1 + x)copt, where copt is the optimal min-cost from P1; the horizontal axis plots the % of edges retained from the full P1 transport.

**Figure 4.** Runtime scaling across 162 runs at 5% robot density, T = 30. (Left) Solve time of P1 (circles) and P2+P3 (squares) versus K;

curves show power-law fits aKp + b. (Right) Speedup versus K; the green line connects averages, the shaded band shows ±1 std. dev., and red annotations indicate the average cost gap.

![Figure extracted from page 9](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-009-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-009-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-009-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 9](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-009-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 10 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

## Acknowledgments

This paper has been accepted for publication at the 43rd International Conference on Machine Learning (ICML’26), July 2026, as a spotlight paper.

## References

Ahuja, R. K., Magnanti, T. L., and Orlin, J. B. Network

Flows: Theory, Algorithms, and Applications. Prentice

Hall, Englewood Cliffs, NJ, 1993.

Ali, Z. A. and Yakovlev, K. Improved anonymous multi- agent path finding algorithm. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 17291–17298, 2023.

Benamou, J.-D., Carlier, G., Cuturi, M., Nenna, L., and

Peyr´e, G. Iterative Bregman projections for regularized transportation problems. SIAM Journal on Scientific Computing, 37(2), 2015.

Carlier, G. On the linear convergence of the multimarginal

Sinkhorn algorithm. SIAM Journal on Optimization, 32 (2), 2022.

Chen, Y., Georgiou, T. T., and Pavon, M. On the relation between optimal transport and Schr¨odinger bridges: A stochastic control viewpoint. Journal of Optimization Theory and Applications, 169:671–691, 2016.

Chen, Y., Georgiou, T. T., Pavon, M., and Tannenbaum, A.

Robust transport over networks. IEEE Transactions on Automatic Control, 62(9):4675–4682, 2017.

Chen, Y., Georgiou, T. T., and Pavon, M. Stochastic control liaisons: Richard Sinkhorn meets Gaspard Monge on a Schr¨odinger bridge. SIAM Review, 63(2), 2021.

Cuturi, M. Sinkhorn distances: Lightspeed computation of optimal transport. In Advances in Neural Information Processing Systems, pp. 2292–2300, 2013.

Di Marino, S. and Gerolin, A. An optimal transport ap- proach for the Schr¨odinger bridge problem and convergence of Sinkhorn algorithm. Journal of Scientific Computing, 85(27), 2020.

Felner, A., Stern, R., Shimony, S. E., Boyarski, E., Golden- berg, M., Sharon, G., Sturtevant, N. R., Wagner, G., and Surynek, P. Search-based optimal solvers for the multiagent pathfinding problem: Summary and challenges. In Proceedings of the Tenth International Symposium on Combinatorial Search, volume 8, 2017.

Fine, G., Atzmon, D., and Agmon, N. Anonymous multi- agent path finding with individual deadlines. In Proceedings of the 22nd International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2023.

F¨ollmer, H. Random fields and diffusion processes. Lecture

Notes in Mathematics, 1362:101–203, 1988.

Ford., L. R. and Fulkerson, D. R. Flows in Networks. Prince- ton University Press, Princeton, NJ, 1962.

Haasler, I., Ringh, A., Chen, Y., and Karlsson, J. Multi- marginal optimal transport with a tree-structured cost and the Schr¨odinger bridge problem. SIAM Journal on Control and Optimization, 59(4):2426–2458, 2021.

Haasler, I., Ringh, A., Chen, Y., and Karlsson, J. Scal- able computation of dynamic flow problems via multimarginal graph-structured optimal transport. Mathematics of Operations Research, 49(2):986–1011, 2023.

Kornhauser, D., Miller, G. L., and Spirakis, P. G. Coordinat- ing pebble motion on graphs, the diameter of permutation groups, and the efficiency of parallel algorithms. In Proceedings of the 25th Annual Symposium on Foundations of Computer Science, pp. 241–250, 1984.

L´eonard, C. A survey of the Schr¨odinger problem and some of its connections with optimal transport. Discrete and Continuous Dynamical Systems, 34(4):1533–1574, 2014.

L´eonard, C. On the convexity of the entropy along entropic interpolations. In Gigli, N. (ed.), Measure Theory in Non- Smooth Spaces, pp. 195–242. De Gruyter Open, 2017.

Lin, T., Ho, N., Cuturi, M., and Jordan, M. I. On the com- plexity of approximating multimarginal optimal transport. Journal of Machine Learning Research, 23(65): 1–43, 2022.

Ma, H. Target Assignment and Path Planning for Navigation

Tasks with Teams of Agents. PhD thesis, University of

Southern California, August 2020.

Ma, H. and Koenig, S. Optimal target assignment and path finding for teams of agents. In Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2016.

Pass, B. Multi-marginal optimal transport: Theory and appli- cations. ESAIM: Mathematical Modelling and Numerical Analysis, 49(6):1771–1790, 2015.

Pavon, M. and Ticozzi, F. Discrete-time classical and quan- tum markovian evolutions: Maximum entropy problems on path space. Journal of Mathematical Physics, 51: 042104, 2010.

Peng, X., Simonin, O., and Solnon, C. Non-crossing anony- mous MAPF for tethered robots. Journal of Artificial Intelligence Research, pp. 357–384, 2023.

<!-- Page 11 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Potra, F. A. and Wright, S. J. Interior-point methods. Jour- nal of Computational and Applied Mathematics, 124(1– 2):281–302, 2000.

Schmitzer, B. Stabilized sparse scaling algorithms for en- tropy regularized transport problems. SIAM Journal on Scientific Computing, 41(3):A1443–A1481, 2019.

Schrijver, A. Theory of Linear and Integer Programming.

John Wiley & Sons, New Yourk, NY, 1986.

Schr¨odinger, E. ¨Uber die umkehrung der naturgesetze. Sitzungsberichte der Preussischen Akademie der Wissenschaften, Physikalisch-mathematische Klasse, pp. 144– 153, 1931.

Sharon, G., Stern, R., Felner, A., and Sturtevant, N. R.

Conflict-based search for optimal multi-agent pathfinding. Artificial Intelligence, 219:40–66, 2015.

Standley, T. Finding optimal solutions to cooperative pathfinding problems. In Proceedings of the Twenty- Fourth AAAI Conference on Artificial Intelligence (AAAI), pp. 173–178, 2010.

Stern, R. Multi-agent path finding – An overview. In Osipov,

G. S., Panov, A. I., and Yakovlev, K. S. (eds.), Artificial Intelligence, volume 11866 of Lecture Notes in Computer Science, pp. 96–115. Springer, 2019.

Surynek, P. Reduced time-expansion graphs and goal de- composition for solving cooperative path finding suboptimally. In Proceedings of the Twenty-Fourth International Joint Conference on Artificial Intelligence (IJCAI), pp. 1916–1922, 2015.

Villani, C. Optimal Transport: Old and New, volume 338 of Grundlehren der mathematischen Wissenschaften. Springer, 2009.

Wright, S. J. Primal-Dual Interior-Point Methods. SIAM,

1997.

Yu, J. and LaValle, S. M. Multi-agent path planning and network flow. In Algorithmic Foundations of Robotics X, volume 86 of Springer Tracts in Advanced Robotics, pp. 157–173. Springer, 2013.

<!-- Page 12 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

## Appendix

Overview

The appendix is organized as follows.

Section Content

## Appendix

A Proof of Lemma 3.2 (Feasibility) Appendix B Proof of Lemma 3.3 (Integrality and TU) Appendix C Proof of Theorem 3.4 (Collision-free transports) Appendix D Proof of Lemma 3.6 (Minimum makespan) Appendix E Proof of Lemma 4.1 (KL decomposition) Appendix F Proof of Lemma 4.2 (Gibbs kernel reduction) Appendix G Sinkhorn-MAPF algorithm Appendix H Detailed Experiments H.1 Illustrative Experiments (Figs. 9–18) H.2 Scaling Study (162 runs, Table 2, Figs. 5–6) H.3 Parameter Sensitivity (260 runs, Table 3, Fig. 7) H.4 Non-uniform Costs (24 runs, Fig. 8) H.5 Baseline Comparison (15 runs, Table 4)

A. Proof of Lemma 3.2

Proof. Consider a Markov chain M whose state-space consists of all K-dimensional {0, 1} vectors with exactly N ones, representing the configuration space of the robots on the graph G. A transition from state q ∈M to q′ ∈M is allowed (and given a non-zero probability), whenever q′ is obtained from q by moving a single robot along a traversable edge (i, j) ∈E to a neighboring location j that is unoccupied by a robot, or by keeping all robots at their current vertices. In other words, the state q has outgoing (positive probability) edges to every state that can be achieved with exactly one robot’s valid move and also to itself (no robot moves). Because G is connected, the robots are indistinguishable, a standard result from the pebble motion literature states that the configuration space of M is connected (Kornhauser et al., 1984). Additionally, since G is finite, under the imposed transition probabilities, M is irreducible and every state in M is recurrent, i.e., from any state q1 ∈M, one can reach any other state q2 ∈M, by a finite sequence of single-robot moves along the edges of G, with probability 1. Therefore, the terminal configuration ν is reachable from µ in a finite number of steps ¯T. Clearly, a transport sequence {Πt} ¯T t=1 that encodes these Markovian transitions satisfies all feasibility constraints in F, and the theorem follows, since Ct is finite on E.

B. Proof of Lemma 3.3

Proof. We first show (i): In order to establish the integral solution guarantee by the LP in P1, we show that all constraints in F can be written in the form of a node-arc incidence matrix of an augmented directed graph ¯G that we construct as follows. Consider the time-expanded graph G ¯T

0 over the horizon ¯T, i.e., with vertices (i, t), for each i ∈V and time t = 0,..., ¯T, and arcs (i, t −1) →(j, t), for t = 1,..., ¯T, whenever the move i →j is allowed by G. We further apply the classical node-splitting construction of Ford and Fulkerson (Ford. & Fulkerson, 1962; Ahuja et al., 1993) to augment G ¯T

0 as follows. For every intermediate vertex (i, t), t = 1,..., ¯T −1, split it into two vertices

(i, t)′′ (in-node), (i, t)′ (out-node), and add an internal arc

(i, t)′′ →(i, t)′.

All arcs that originally entered (i, t), now enter (i, t)′′, traverse the internal arc (i, t)′′ →(i, t)′; and all arcs that originally left (i, t) now emanate from (i, t)′. Thus, at each time t = 1,..., ¯T −1, a transport entering any vertex i is forced over (i, t)′′ →(i, t)′ before it can move on to the next time layer t + 1. Let ¯G denote the resulting augmented graph with (¯T + 1) layers of G, with a total of 2K ¯T(= K + 2K(¯T −1) + K) vertices due to node-splitting, and with K(¯T −1) internal arcs added to the arcs in G ¯T

0.

<!-- Page 13 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Let ¯π stack all arc transport variables on ¯G. It can be verified that all constraints in P1 can now be written as ¯A¯π ≤¯b, −¯A¯π ≤−¯b, I ¯π ≤1, and −I ¯π ≤0, where ¯b ∈{0, ±1}2K ¯T is such that it is −µi for each node (i, 0) in layer 0, νj for each node (j, ¯T) in the last layer ¯T, and 0 on every intermediate split node. Define

ˆA:=





¯A −¯A

I −I



, ˆb:=





¯b −¯b

1 0



.

Since incidence matrices of directed graphs are totally unimodular (TU), ¯A is TU; see Chapter 19 in (Schrijver, 1986). Consequently, the overall constraint matrix ˆA is TU, because TU is preserved under row sign changes and appending rows of ±I. Since ˆA is TU, the polyhedron {¯π: ˆA¯π ≤ˆb} has integral extreme points. By the TUM theorem (Theorem 19.1 and Corollary 19.1a in (Schrijver, 1986)), solving the LP corresponding to P1 on the augmented ¯G admits an optimal basic solution that is integral. From standard network flow arguments (Ford. & Fulkerson, 1962; Ahuja et al., 1993), any feasible flow in the augmented network yields an equivalent feasible flow in the original time-expanded network G ¯T

0 that respects the node-capacity constraints, and conversely. Thus, {Π∗ t } ¯T t=1 can be chosen as an optimal basic solution and is therefore integral, and (i) follows. The rest of the lemma follows from the standard arguments in linear programming; see also Section 6 on precise complexity arguments.

C. Proof of Theorem 3.4

Proof. We first show (i). Robots may collide in the following scenarios: (a) at two intersecting edges i →m and j →k, for distinct i, j, k, m; or, (b) a robot traversing i →j may collide with stationary robots at nearby vertices; or, (c) when two robots travel to the same destination; or, (d) at a bidirectional edge i ↔j; or, (e) in a flow cycle i1 →i2 →· · · →ik →i1, for k ≥3. Clearly, (a) and (b) are ruled out because of Assumption 3.1(ii), and (c) is ruled out by the vertex-capacity constraint. To show that (d) does not appear in the transport, we proceed as follows. Suppose, on the contrary, that there exists a min-cost transport {Πt} ¯T t=1, such that at time t and two distinct vertices i̸ = j, we have πij,t = 1 and πji,t = 1, i.e., two robots simultaneously traverse the edges i →j and j →i. Since self-loops i →i and j →j are feasible by Assumption 3.1(i), define an alternate plan {˜Πt} ¯T t=1 that is exactly the same as the optimal {Πt} ¯T t=1, except for these swaps, which are replaced by waiting moves, i.e.,

˜πii,t = 1, ˜πjj,t = 1, ˜πij,t = 0, ˜πji,t = 0.

This modification preserves feasibility, since the row and column sums of the t-th slice Πt remain unchanged and hence the distributions qt−1 and qt are identical for both {Πt} ¯T t=1 and {˜Πt} ¯T t=1. By Assumption 3.1(v), cii,t + cjj,t < cij,t + cji,t, and therefore

⟨˜Πt, Ct⟩< ⟨Πt, Ct⟩, contradicting the optimality of {Πt} ¯T t=1. With a similar argument, a k-cycle leaves the configuration unchanged (because the robots are anonymous) at the price of k moves and is therefore also suboptimal. Hence, no min-cost solution contains a collision and (i) follows; (ii) follows consequently, and (iii) is guaranteed by the terminal feasibility of P1.

D. Proof of Lemma 3.6

Proof. That P1 results into integral transports is already established in Lemma 3.3. Let Π′ t ∈{0, 1}K×K, t = 1,..., ¯T, be an optimal solution of P1 obtained with the cost structure Ct described in Assumption 3.5, i.e., {Π′ t} ¯T t=1 minimizes the transport cost P t⟨Π′ t, Ct, ⟩, over the horizon t = 0, 1,..., ¯T, and let T ′ ≤¯T be its makespan, i.e., there is no motion after T ′. Let T ∗denote the minimum makespan over all feasible transports, and fix any feasible integral transport {Π∗ t } ¯T t=1, whose makespan is T ∗(extended to the horizon ¯T by waits at targets). Clearly, we have that T ′ ≥T ∗and we need to show that T ′ = T ∗.

Suppose, on the contrary, that T ′ > T ∗. Since T ′ is the makespan of {Π′ t}t, there exists at least one non-wait transport at time T ′, i.e., π′ ij,T ′ = 1, for some i̸ = j, with cost cij,T ′ = BT ′˜cij ≥BT ′ ˜cmin,

<!-- Page 14 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges from Assumption 3.5, and therefore the min-cost transport Π′ t satisfies:

¯T X t=1

⟨Π′ t, Ct⟩≥⟨Π′

T ′, CT ′⟩≥cij,T ′ ≥BT ′ ˜cmin ≥BT ∗+1 ˜cmin, since T ′ ≥T ∗+ 1. Similarly, {Π∗ t }t has no non-wait motion after time T ∗, so its cost is supported only on times t ≤T ∗, and using π∗ ij,t ≤1, we have

¯T X t=1

⟨Π∗ t, Ct⟩=

T ∗ X t=1

⟨Π∗ t, Ct⟩≤

T ∗ X t=1

X i→j∈E cij,t =

T ∗ X t=1

Bt X i→j∈E

˜cij.

By Assumption 3.5, it follows that

BT ∗+1 ˜cmin > BT ∗+1

B −1

X i→j∈E

˜cij ≥

T ∗ X t=1

Bt X i→j∈E

˜cij.

Hence, P ¯T t=1⟨Π′ t, Ct⟩> P ¯T t=1⟨Π∗ t, Ct⟩, contradicting the optimality of {Π′ t}t and we conclude that T ′ = T ∗.

E. Proof of Lemma 4.1

Proof. Since G is Markovian, it admits the following factorization:

Gi0,...,iT = [g0]i0

T Y t=1

[Gt]it−1,it

[gt−1]it−1

,

Recalling the definition of KL divergence, write

KL(P∥G) =

X i0,...,iT

Pi0,...,iT log Pi0,...,iT

Gi0,...,iT

.

Substituting the Markov factorizations in (3) yields

KL(P∥G) =

X i0,...,iT

Pi0,...,iT

" log

1 N [q0]i0

[g0]i0

+

T X t=1 log

1 N [Πt]it−1,it

[Gt]it−1,it

−log

1 N [qt−1]it−1

[gt−1]it−1

#

.

Distributing the sums and marginalizing P yields (4) and the proof follows.

F. Proof of Lemma 4.2

Proof. Recall that qt, for any t = 0, 1,..., T, is a {0, 1} vector with exactly N ones. Therefore,

KL(1

N qt∥gt) =

K X i=1

1 N [qt]i log

1 N [qt]i

[gt]i

=

X i∈Vt

## 1 N log

1 N [gt]i

:= κt, for all t, since gt are given fixed references. From (4), we have

KL(P∥G) =

T X t=1

KL(1

N Πt∥Gt) + κ,

<!-- Page 15 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges where κ encodes all κt’s and is independent of the transport variables. Fixing t and expanding the KL term, we get:

KL(1

N Πt∥Gt) =

X i,j

1 N Πij,t log

1 N Πij,t

Gij,t

=

X i,j

1 N Πij,t log 1

N Πij,t −

X i,j

1 N Πij,t log gij,t zt

=

X i,j

1 N Πij,t log 1

N Πij,t +

X i,j

1 N Πij,t cij,t ε +

X i,j

1 N Πij,t log zt,

= 1

N

X i,j

Πij,t log Πij,t + log 1

N + 1

N

X i,j

Πij,t cij,t ε + log zt, which yields the desired result after noting that P i,j Πij,t = N.

G. Sinkhorn-MAPF

Recall that P2 is an entropic regularization of the LP in P1. This regularization enables the use of efficient Sinkhorn-type algorithms, which scale to problem sizes where the original LP may become computationally intractable. We leverage these ideas to design an algorithm for the time-expanded transport formulation. Recall Gt from Lemma 4.1. It is well known (see e.g., Lemma 2 in (Cuturi, 2013)) that the minimizer of P2 is obtained at eΠt = diag(ut) Gt diag(vt), t = 1,..., T, for some positive scaling vectors ut, vt ∈RK

+, where diag(ut) is the diagonal matrix formed by the vector ut. The Sinkhorn algorithm is an iterative scheme to find the scaling vectors ut, vt such that eΠt, as written above, satisfies the constraint set F. We describe this procedure next. Given the element-wise expansion of the above, i.e., eπi,j,t = ui,t Gij,t vj,t, t = 1,..., T, i, j = 1,..., K, we note that, for each i, t,

[eΠt1]i =

X j eπij,t = ui,t

X j

Gij,tvj,t = ui,t [Gtvt]i, and similarly, for each j, t,

[eΠ⊤ t 1]j =

X i eπij,t = vj,t

X i ui,t Gij,t = vj,t [G⊤ t ut]j.

We can now write all constraints in F in terms of the scaling vectors as follows:

qt−1 = eΠt1 = ut ⊙[Gtvt], qt = eΠ⊤ t 1 = vt ⊙[G⊤ t ut], where ⊙denotes the element-wise product. Since eΠ⊤ t 1 = qt = eΠt+11, we have the dynamic consistency equation:

vt ⊙[G⊤ t ut] = ut+1 ⊙[Gt+1vt+1], t = 1,..., T −1. (5)

The boundary conditions are given by q0 = eΠ11 = u1 ⊙[G1v1] = µ, (6)

qT = eΠ⊤

T 1 = vT ⊙[G⊤

T uT ] = ν. (7)

We now define the Sinkhorn-MAPF algorithm below3:

3It is not uncommon to implement the resulting equations in the log domain to account for the numerical instabilities when ε →0, see e.g., (Schmitzer, 2019).

<!-- Page 16 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Initialization: Set u(0)

t = v(0)

t = 1 for all t = 1,..., T and then normalize the boundary slices only on the prescribed supports, i.e.,

[u(0)

1 ]i ← [µ]i [G1v(0)

1 ]i, for all i ∈supp(µ), [v(0)

T ]j ← [ν]j [G⊤

T u(0)

T ]j

, for all j ∈supp(ν);

where we adopt the convention throughout that the ratio is set to 0 if the denominator is zero unless otherwise stated.

Sinkhorn sweeps: For τ = 0,..., ¯τ −1, repeat the following:

## 1 Starting marginal projection:

Given v(τ) 1, update u(τ+1) 1 to conform with the starting marginal µ, using

[u(τ+1)

1 ]i =

(

[µ]i/[G1v(τ)

1 ]i, if [µ]i = 1, [u(τ)

1 ]i, if [µ]i = 0, and u(τ+1)

t = u(τ)

t, for t > 1.

## 2 Forward consistency projection:

For each t = 1,..., T −1, enforce the dynamic consistency between t and t + 1. First compute the current scaling constants

[qout t ]i = [v(τ)

t ]i · [G⊤ t u(τ+1)

t ]i,

[qin t ]i = [u(τ+1)

t+1 ]i · [Gt+1 v(τ)

t+1]i, and define a correction factor

[γt]i =

  

  s

[qin t ]i [qout t ]i

, if [qout t ]i > 0,

1, otw.

to update

[v(τ+1)

t ]i = [v(τ)

t ]i [γt]η i,

[u(τ+1)

t+1 ]i = [u(τ+1)

t+1 ]i [γt]−η i.

The multiplicative factor [γt]η i moves [qout t ]i and [qin t ]i closer at each node i. If η = 1 (and no other constraints are active), then the update enforces [qout t ]i = [qin t ]i in one step; for η ∈(0, 1), it is a damped projection.

## 3 Terminal marginal projection:

Given u(τ+1) T, update v(τ+1)

T to conform with the terminal marginal ν, using

[v(τ+1)

T ]j =

(

[ν]j/[G⊤

T u(τ+1)

T ]j, if [ν]j = 1, [v(τ)

T ]j, if [ν]j = 0.

For t < T, we already have v(τ+1)

t from the consistency update above.

## 4 Backward consistency projection:

For each t = T −1,..., 1, enforce the dynamic consistency between t + 1 and t, i.e., in reverse time. Compute

[¯qout t ]i = [u(τ+1)

t+1 ]i · [Gt+1 v(τ+1)

t+1 ]i,

[¯qin t ]i = [v(τ+1)

t ]i · [G⊤ t u(τ+1)

t ]i, and

[¯γt]i =

  

  s

[¯qin t ]i [¯qout t ]i

, [¯qout t ]i > 0,

1, otw.

<!-- Page 17 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges with updates

[u(τ+1)

t+1 ]i = [u(τ+1)

t+1 ]i [¯γt]η i,

[v(τ+1)

t ]i = [v(τ+1)

t ]i [¯γt]−η i.

As in the forward sweep, the multiplicative factor [γt]η i reduces the discrepancy between [qout t ]i and [qin t ]i at each node i, but now propagates corrections backward in time.

Final regularized transports: The algorithm is terminated at τ = ¯τ −1, resulting in eΠt = diag(u(¯τ)

t) Gt diag(v(¯τ)

t), t = 1,..., T,

H. Detailed Experiments

In this section, we provide a detailed set of experiments. We consider square grids of size K = W 2 with N robots, M targets, and O obstacles, such that N = M. While the proposed framework applies to arbitrary graphs, grids are chosen for ease of visualization and reproducibility. The time horizons are chosen such that the corresponding LPs are feasible; smaller values of T are only chosen for convenience as it is easier to display the corresponding trajectories. Unless stated otherwise, the cost structure is such that waiting cost at targets is cii = 0, i ∈M, waiting at non-target is cjj = 0.5, j /∈M, while the move cost is ci̸=j = 1, for all i →j ∈E.

H.1. Illustrative Experiments

We first provide some basic experiments to demonstrate the main ideas. The experiment setup is described in the caption of each figure and the corresponding LPs are solved using the standard linear programming suite in the HiGHS solver from the SciPy’s linprog library; all variables are continuous by default. Figs. 9, 10, and 11 solve P1 over a given time horizon T; we note that arbitrarily placed obstacles alter the connectivity and diameter of the underlying graph, and it no longer remains a regular grid. Figs. 12-15 elaborate the min-cost versus minimum makespan nature of the transports returned by P1. Figs. 16, 17, and 18 solve P2 with the Sinkhorn iterations of Appendix G for the following (ε, ¯τ) pairs, where ¯τ are the total number of Sinkhorn iterations: {(0.2, 50), (0.5, 10), (50, 5)}; then prune the resulting graph and project on the integral P3 LP. As known for Sinkhorn iterations, P2 may require a larger ¯τ as ε decreases; however, a useful shadow transport is typically obtained within a small number of iterations.

In the following subsections (Sections H.2–H.5), we conduct a large-scale study of the proposed approaches. We ran over 460 experiments on graphs ranging from K = 2,500 to K = 22,500 vertices, i.e., from 369K to 3.4M LP variables, using the Gurobi LP solver with continuous variables; all P1 and P3 solutions are verified integral as guaranteed by the TU of the underlying LP.

H.2. Scaling Study

We evaluate the runtime scaling of P1 and the P2+P3 pipeline on a 2022 MacBook; all LPs use continuous variables. We consider square grids of size K = W 2 with no obstacles, at 5% robot density (N = 0.05K), over a horizon T = 30. The cost structure follows the convention adopted in Assumption 3.1. The Sinkhorn parameters are ε = 0.2 and ¯τ = 150 sweeps. For each grid size, we generate 14–25 random instances and report averaged results. On grid graphs, each vertex has at most 5 neighbors (4 cardinal directions plus a self-loop), so the number of variables in P1 is |E|T ≈5KT. For example, at K = 22,500 with T = 30: |E|T = 3,357,000.

**Table 2.** summarizes the results across 8 grid sizes, totaling 162 runs. For each grid, we report the number of P1 variables (= |E|T), the average P1 solve time, the average P2+P3 solve times (Sinkhorn + feasible P3), the resulting speedup, cost gap relative to P1, and the percentage of edges retained from the shadow transport (which also provides the average number of P3 variables, kept after pruning).

**Fig. 4.** (in Section 7, left panel) plots the P1 and P2+P3 solve times against the number of grid vertices K, with power-law fits of the form aKp + b over all 162 individual runs. The fitted models are

P1: solve time = 2.26×10−5 K1.68 + 10.2 (R2 = 0.96),

<!-- Page 18 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Table 2.** Scaling of P1 and P2+P3 across grid sizes at 5% robot density (N = 0.05K), T = 30, ε = 0.2. All times are averaged and are

reported in seconds (s). Every solution across all 162 runs is verified integral.

K N Runs P1 vars P1 (s) P2+P3 (s) Speedup Gap (%) Kept (%)

2,500 125 20 369K 15 4 3.6× 8.0 32 5,625 281 25 835K 55 11 5.0× 8.7 35 8,100 405 19 1.2M 103 5.7× 9.0 37 10,000 500 24 1.5M 132 26 5.1× 5.9 41 13,225 661 14 2.0M 193 33 5.8× 8.1 39 15,625 781 23 2.3M 257 48 5.3× 5.9 43 19,600 980 2.9M 364 62 5.8× 7.2 42 22,500 1,125 19 3.4M 478 67 7.1× 6.5 40

P2+P3: solve time = 7.40×10−4 K1.15 −2.97 (R2 = 0.74).

We note that P1 time grows sub-quadratically in K, while the P2+P3 oracle time scales almost linearly. The speedup, shown in Fig. 4 (right panel), grows with problem size from 3.6× at K = 2,500 to 7.1× at K = 22,500, while the cost gap remains consistently below 10% (median 6.4%). Since P1 already provides the exact optimum, the P2+P3 pipeline offers a practical speed-quality tradeoff: a 5–7× speedup at under 10% cost degradation.

**Fig. 5.** examines the cost-gap-versus-speedup tradeoff from two perspectives. The left panel plots the cost gap against the speedup for each of the 162 individual runs, colored by the number of vertices K. The cluster structure confirms that larger instances achieve higher speedups at comparable or lower cost gaps, i.e., the shadow-based pruning becomes more effective as K grows. The right panel plots the average cost gap and speedup jointly against K on a dual axis. The cost gap remains stable between 5–9% across all grid sizes, while the speedup increases steadily from 3.6× to 7.1×.

**Fig. 6.** provides a complementary view of the pipeline. The left panel decomposes the average solve time into P1 (gray), Sinkhorn (blue), and P3 LP (red) components. The connected dots trace the scaling shape: the P1 curve grows subquadratically while the P2+P3 curve remains nearly flat. The italic percentages above each stacked bar indicate the Sinkhorn share of the P2+P3 oracle time, which decreases from 63% at K = 2,500 to 34% at K = 22,500; at large scale, the LP solve dominates. The right panel shows the variable reduction achieved by shadow-based pruning: P3 consistently operates on 32–43% of the P1 variables.

**Figure 5.** Cost gap and speedup tradeoff across 162 scaling runs at 5% robot density, T = 30. (Left) Cost gap (%) versus speedup for

each individual run, colored by the number of vertices K; the dashed line marks the 10% gap threshold. (Right) Average cost gap (%, left axis, red) and speedup (right axis, blue) versus K, with ±1 standard deviation error bars; the dotted line marks the 10% gap threshold.

H.3. Sinkhorn and Pruning Parameter Sensitivity

In this section, we study the sensitivity of the scalable P2+P3 pipeline to the corresponding parameters ε and λ. We sweep ε ∈{0.1, 0.2, 0.5, 1.0, 5.0} and λ ∈{0, 0.5, 1.0, 5.0} over 13 independent random instances on K = 10,000 vertices (W = H = 100, N = 500, T = 30, 1.5M variables in P1), for a total of 260 runs (20 parameter combinations per instance). The P1 baseline solves on average in 130s. Of the 260 runs, 233 are feasible; the 27 infeasible cases arise at the extremes ε = 0.1 (19 runs across 5 instances) and ε = 5.0 (8 runs across 2 instances). These infeasibilities are artifacts of the fixed pruning threshold (≈40–45% of edges retained); relaxing the threshold to retain more edges recovers feasibility in

![Figure extracted from page 18](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-018-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 19 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 6.** Pipeline decomposition across 8 grid sizes at 5% robot density, T = 30; all values are averages over 14–25 independent

instances. (Left) Solve time of P1 (gray bars) versus the Sinkhorn (P2, blue) and LP solve (P3, red) components of the pipeline; connected dots trace the scaling shape of each; italic percentages show the Sinkhorn share of the P2+P3 time. (Right) Number of LP variables in P1 (blue) versus P3 after pruning (red); percentages indicate the fraction of P1 variables retained.

all cases. Every feasible solution is verified integral.

**Table 1.** (in Section 7) reports the average cost gap (%) relative to P1 for each (ε, λ) combination. The parameter ε is the dominant factor: small ε (≤0.2) produces a concentrated shadow close to the P1 optimum, enabling aggressive pruning with 2–5% gap, while large ε smooths the shadow and increases the gap to 17–20%. The parameter λ has a milder effect, adding roughly 1–6% to the gap depending on ε. A plausible time-quality tradeoff is at ε = 0.2, λ = 0: a 4.3% gap in 26s (5.0× speedup over P1).

**Table 3.** reports the Sinkhorn convergence and P2 + P3 timing per ε (at λ = 0), where Sinkhorn iterations are terminated at convergence. The Sinkhorn convergence scales inversely with ε, as expected from entropic regularization: 307 sweeps at ε = 0.1 versus 39 at ε = 5.0. However, the cost gap increases as ε increases (from ∼2% at ε = 0.1 to ∼17% at ε = 5.0), reflecting the smoothing effect that makes the shadow less discriminative and the pruned graph less targeted. The total P2+P3 time ranges from 48s at ε = 0.1 to 22–26s at ε ≥0.2, all well below the P1 baseline of 130s. At ε = 5.0, the runtime increase is because of the diffuse shadow that makes pruning ineffective, resulting in more variables retained in P3.

**Table 3.** Sinkhorn convergence and P2+P3 pipeline timing per ε at λ = 0, averaged over 13 instances at K = 10,000, T = 30.

ε Sweeps Sinkhorn (s) P2+P3 (s) Gap (%) Kept (%)

0.1 307 20 48 2.3 47 0.2 132 9 26 4.3 42 0.5 97 7 22 11.1 40 1.0 75 5 23 17.3 43 5.0 39 3 25 17.1 47

**Figure 7.** Parameter sensitivity across 260 runs (13 instances, 20 combinations each) at K = 10,000, T = 30. (Left) Dual-axis plot

at λ = 0: effective Sinkhorn sweeps (left axis, blue) and cost gap (%, right axis, red) versus ε; shaded bands show ±1 standard deviation across instances. (Middle) Cost gap versus edges kept (%) for all 233 feasible runs, colored by ε. (Right) Average cost gap versus ε for each λ.

![Figure extracted from page 19](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-019-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 19](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-019-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 20 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

Parameter roles. The parameter ε controls the sharpness of the shadow transport: as ε →0, the Schr¨odinger bridge concentrates onto minimum-cost geodesic corridors, producing a sharp shadow that enables aggressive pruning at low cost gap; as ε increases, the shadow becomes diffuse and the pruned graph retains more edges with less discriminative structure. The parameter λ controls the bias toward the shadow in the P3 cost: increasing λ penalizes edges with small shadow flow, effectively forcing P3 to follow the shadow transport more closely. When costs are uniform, λ and ε together provide a beneficial tiebreaker among edges that are otherwise equivalent in cost, favoring those with a darker shadow. The parameter δ is a small numerical safeguard for the logarithm in the modified P3 cost and has negligible effect on the solution. Across the experiments reported in this paper, the following is a robust default that works without much fine-tuning: δ = 10−6, ε = 0.2, stop Sinkhorn when the last 20 iterates stabilize, and λ = 0. For the pruning threshold η, retaining 40–48% of edges (depending on ε) consistently yields feasible P3 solutions.

**Fig. 7.** visualizes the sensitivity structure from three perspectives. The left panel is a dual-axis plot: the left axis shows the effective number of Sinkhorn sweeps (blue) and the right axis shows the cost gap (red), both versus ε at λ = 0, with ±1 standard deviation shaded across the 13 instances. The sweeps decrease inversely with ε, while the gap increases nearly monotonically. The middle panel plots the gap against the fraction of edges retained for all 233 feasible runs, colored by ε, where lower ε achieves lower gaps at comparable pruning levels. For a fixed ε, the cost variation is also due to varying λ. The right panel isolates the effect of λ by plotting the gap versus ε for each λ value; the curves confirm that λ shifts the gap upward by a roughly constant offset, with a mild effect relative to ε.

H.4. Non-uniform Costs

In this section, we validate the proposed P1 and the P2+P3 pipeline under non-uniform costs. We assign each cell a random arrival cost ∼Uniform[0.6, 1] and wait cost ∼Uniform[0.1, 0.5] (wait at target = 0), preserving Assumption 3.1. Choosing costs like this reflects e.g., uneven terrains; see Fig. 8 (left) for a candidate scenario. We run 24 instances at K = 10,000 (W = H = 100, N = 500 robots, T = 30) with ε = 0.2, λ = 0. The P1 baseline averages 138s; the P2+P3 pipeline averages 25s at 5.1% gap and 5.4× speedup. For reference, the uniform-cost baseline (from the sensitivity study) gives 4.3% gap and 5.0× speedup. The gap and speedup under non-uniform costs are comparable, confirming that the pipeline adapts to the cost landscape without degradation. Fig. 8 (middle) shows the per-instance gap and speedup, and Fig. 8 (right) compares the uniform and non-uniform averages. Every solution is verified integral.

**Figure 8.** Non-uniform cost experiments across 24 instances at K = 10,000, T = 30. (Left) Illustrative terrain on a 100 × 100 grid;

each cell has a random arrival cost ∼Uniform[0.6, 1]; higher elevation corresponds to higher move cost. (Middle) Cost gap (%, left axis, red) and speedup (right axis, blue) per instance; dashed lines show non-uniform averages (5.1% gap, 5.4× speedup), dotted lines show the uniform-cost reference (4.3% gap, 5.0× speedup). (Right) Uniform versus non-uniform cost comparison, averaged over all instances.

H.5. Baseline Comparison

In this section, we compare with a close prior anonymous MAPF formulation (Ma & Koenig, 2016), which studies TAPF (combined target-assignment and path-finding). In TAPF, a generalization of anonymous MAPF, agents are partitioned into teams, each team is given the same number of targets as agents, and the goal is to jointly assign agents to targets and plan collision-free paths that minimize makespan. TAPF with a single team (all agents exchangeable) is the anonymous MAPF problem that we solve. Their method CBM (Conflict-Based Min-Cost-Flow) uses a min-cost max-flow solver on a time-expanded network on the low level (for within-team assignment and routing) and conflict-based search on the high level (for inter-team collision resolution). We note that the network-flow formulation in (Ma & Koenig, 2016) (or in (Yu &

![Figure extracted from page 20](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-020-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 20](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-020-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 20](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-020-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 21 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

LaValle, 2013)) does not establish total unimodularity of the constraint matrix. Consequently, even for a single team, the LP relaxation is not formulated and is not guaranteed to produce integer solutions; one must therefore resort to integer linear programming (ILP) or the hierarchical CBM search for integrality.

In contrast, our P1 formulation guarantees integral solutions from the continuous LP via TU, without branch-and-bound or conflict resolution. The comparison next provides a useful reference point on the same grid setting. We adopt the same experimental setting as (Ma & Koenig, 2016), Table 1: a 30 × 30 grid with 10% randomly blocked cells and 4-neighbor connectivity. Table 4 compares the results. CBM solves up to 50 agents in 5.32s; the reported ILP-based solver handles 50 agents in 162s with only 4% success rate within a 5-minute timeout. We note that restricting the formulation in (Ma & Koenig, 2016) to a single team may improve the performance, as the multi-team structure introduces additional complexity. In contrast, the proposed P1 solves 300 agents (same grid, 6× more agents) in 0.54s on average, and the P2+P3 pipeline solves in 0.49s at 0.63% gap. Our framework further scales to K = 22,500 vertices (1,125 agents) where P2+P3 solve time is 67s on average.

**Table 4.** Comparison on 30 × 30 grids with 10% obstacles. CBM and ILP results are from (Ma & Koenig, 2016), Table 1. Our results are

averaged over 15 instances.

## Method

Agents Time (s) Success

CBM (Ma & Koenig, 2016) 50 5.32 100% ILP (Ma & Koenig, 2016) 50 162 4% ILP (Ma & Koenig, 2016) 40 153 14%

P1 (ours) 300 0.54 100% P2+P3 (ours) 300 0.49 100%

<!-- Page 22 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 9.** A 25 × 25 grid with {200} robots ▲, {200} targets •, and {225} obstacles. Every cell is either a robot, a target, or an obstacle. The robot trajectories come from the min-cost transport obtained by solving P1 over T = 12.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 22](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-022-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 23 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 10.** A larger 40 × 40 grid with 300 robots ▲, 300 targets •, and 100 obstacles. The robot trajectories come from the min-cost

transport obtained by solving P1 over T = 6.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 23](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-023-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 24 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 11.** A larger 40 × 40 grid with 800 robots ▲and 800 targets •; every cell is either occupied by a robot or a target. The robot

trajectories come from the min-cost transport obtained by solving P1 over T = 6.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 24](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-024-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 25 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 12.** Min-cost vs. Min-makespan: A 6 × 8 grid with 4 robots ▲, 4 targets •, and 16 obstacles. Edges in the gray shaded region

have cost 10; rest follow our move-wait cost convention. With T = 10, the min-cost transport avoids the high cost interior and takes the robots from the boundary of the grid, with all one-cost moves for a total of 40.

![Figure extracted from page 25](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-025-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 26 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 13.** Min-cost vs. Min-makespan: A 6 × 8 grid with 4 robots ▲, 4 targets •, and 16 obstacles. Edges in the gray shaded region

have cost 10; rest follow our move-wait cost convention. With T = 9, all robots cannot travel on the boundary as that requires 10 moves; the min-cost transport therefore takes two robots from the boundary in 9 steps each, and two from the higher cost interior edges for a total cost of 82.

![Figure extracted from page 26](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-026-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 27 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 14.** Min-cost vs. Min-makespan: A 6 × 8 grid with 4 robots ▲, 4 targets •, and 16 obstacles. Edges in the gray shaded region

have cost 10; rest follow our move-wait cost convention. With T = 8, boundary paths are no longer feasible within the given time horizon. All robots must travel through the interior edges to reach the targets for a total cost of 132.

![Figure extracted from page 27](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-027-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 28 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 15.** Min-cost vs. Min-makespan: A 6 × 8 grid with 4 robots ▲, 4 targets •, and 16 obstacles. Edges in the gray shaded region

have cost 10; rest follow our move-wait cost convention. We choose the cost structure described in Assumption 3.5. P1 consequently provides the minimum makespan solution that terminates the robot motion in 5 steps, i.e., achieves the minimum makespan, when solved over a longer T = 10 horizon. The total cost of this transport increases exponentially, of the order of 1013. For larger problems, the corresponding solvers may run into numerical instabilities and the search procedure described in Lemma 3.7 may be more tractable to compute the minimum makespan.

![Figure extracted from page 28](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-028-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 29 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 16.** A 40 × 40 grid with 80 robots ▲, 80 targets •, and T = 10. The robot paths are superimposed over the horizon T. The first figure is the Schr¨odinger shadow that shows the likely mass transport obtained by solving P2 after ¯τ Sinkhorn iterations in Appendix G; ε = 0.2, ¯τ = 50. The next figures show the integral projection P3 by keeping the highest-valued X% of edges from the shadow. Cost is compared with the optimal in the figure title, and the optimal min-cost transport can be achieved with 32.6% edges. It is interesting to note the difference in the robot trajectories over these solutions.

![Figure extracted from page 29](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-029-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 30 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 17.** A 40 × 40 grid with 80 robots ▲, 80 targets •, and T = 10. The robot paths are superimposed over the horizon T. The first figure is the Schr¨odinger shadow that shows the likely mass transport obtained by solving P2 after ¯τ Sinkhorn iterations in Appendix G; ε = 0.5, ¯τ = 10. The next figures show the integral projection P3 by keeping the highest-valued X% of edges from the shadow. Cost is compared with the optimal in the figure title, which can be achieved with 32.4% edges.

![Figure extracted from page 30](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-030-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 31 -->

Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schr¨odinger Bridges

**Figure 18.** A 40 × 40 grid with 80 robots ▲, 80 targets •, and T = 10. The robot paths are superimposed over the horizon T. The first figure is the Schr¨odinger shadow that shows the likely mass transport obtained by solving P2 after ¯τ Sinkhorn iterations in Appendix G; ε = 50, ¯τ = 5. The next figures show the integral projection P3 by keeping the highest-valued X% of edges from the shadow. Cost is compared with the optimal in the figure title, which can be achieved with 42.7% edges.

![Figure extracted from page 31](2026-ICML-optimal-and-scalable-mapf-via-multi-marginal-optimal-transport-and-schr-dinger-b/page-031-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
