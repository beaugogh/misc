---
title: "RENEW: Risk- and Energy-Aware Navigation in Dynamic Waterways"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/38897
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/38897/42859
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# RENEW: Risk- and Energy-Aware Navigation in Dynamic Waterways

<!-- Page 1 -->

RENEW: Risk- and Energy-Aware Navigation in Dynamic Waterways

Mingi Jeong1,2, Alberto Quattrini Li2

1Department of Aerospace and Ocean Engineering, Virginia Tech 2Department of Computer Science, Dartmouth College mingijeong@vt.edu, alberto.quattrini.li@dartmouth.edu

## Abstract

We present RENEW, a global path planner for Autonomous Surface Vehicle (ASV) in dynamic environments with external disturbances (e.g., water currents). RENEW introduces a unified risk- and energy-aware strategy that ensures safety by dynamically identifying non-navigable regions and enforcing adaptive safety constraints. Inspired by maritime contingency planning, it employs a best-effort strategy to maintain control under adverse conditions. The hierarchical architecture combines high-level constrained triangulation for topological diversity with low-level trajectory optimization within safe corridors. Validated with real-world ocean data, RENEW is the first framework to jointly address adaptive non-navigability and topological path diversity for robust maritime navigation.

Code — https://github.com/dartmouthrobotics/RENEW.git

## Introduction

This paper presents a novel global path planner for Autonomous Surface Vehicle (ASV), addressing external disturbances like water currents, which significantly impact navigational risk and energy cost. For instance, in the Malacca and Singapore Straits—among the world’s busiest waterways—dynamic surface currents reshape navigable areas and dictate optimal paths. To mitigate risk, vessels must avoid adverse currents while ensuring turning maneuverability allows for reliable contingency maneuvers.

Global path planning under dynamic disturbances remains a challenge, particularly in identifying navigable areas and performing safety analysis to prevent grounding. To ensure ASVs respect state constraints, we propose a risk- and energy-aware framework that guarantees a feasible contingency maneuver—defined as a best effort under the worst case—to avoid Inevitable Collision States (ICS) (Blackmore, Ono, and Williams 2011; Johnson and Yip 2021). Our approach keeps trajectories within navigable regions despite adverse conditions and bounded uncertainty.

Prior work has addressed path planning under disturbances like ocean currents (Pereira et al. 2013; Kularatne, Bhattacharya, and Hsieh 2016; Doering et al. 2023), yet optimizing across multiple distinct paths while considering dynamic, restricted navigable areas remains an open challenge.

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Unexpected obstacle Ours

State-of-the-art

Disturbances

Fuel Cost 96.08 Min distance to obstacle [m]

12.55

Path length [m] 146.50

Fuel Cost 103.99 Min distance to obstacle [m]

1.23

Path length [m] 113.56

Optimal path

**Figure 1.** Path planning under external disturbances. (top) Our method selects energy-efficient paths across multiple homotopy classes, using current-based adaptive padding (gray) around obstacles (brown), to ensure feasible contingency maneuvers. (bottom) The baseline prioritizes distance over energy/homotopy. Without adaptive padding, its paths lack safety margins for contingency maneuvers.

A gap exists in accounting for non-holonomic constraints and irregular maneuvering (e.g., current-dependent turning radii) within these changing environments.

Given an environment map and vector field (e.g., ocean currents), our planner incorporates: (1) risk-aware safety via adaptive padding to avoid non-navigable areas; (2) a best-effort strategy for worst-case disturbances; and (3) a hierarchical architecture where a high-level planner identifies topologically distinct (homotopic) paths via constrained triangulation, and a low-level planner optimizes for energy and kinematics (see Fig. 1).

In summary, our key contributions are: • A safety framework using best-effort turning under uncertainty, accounting for irregular ASV maneuverability and current-dependent no-go areas; • An efficient hierarchical planner that uses constrained triangulation to find topologically distinct paths, optimizing for energy efficiency and kinematic feasibility; • Extensive validation via ablation studies and simulations in both custom realistic and real-world current scenarios. This is the first risk-aware global planner to unify dynamic external forces with topological guarantees for improved safety and efficiency.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

18333

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-001-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

Related Works Plethora of methods for global path planning appeared in the robotics literature, including efficient representations of the environment through sampling-based approaches, such as PRM (Kavraki et al. 1996) and RRT (LaValle and Kuffner Jr 2001), and corresponding search-based methods that can find the optimal path, e.g., A* (Hart, Nilsson, and Raphael 1968). For a general overview on path planning and specifically for ASVs, please refer to (Kavraki and LaValle 2016) and (Vagale et al. 2021b,a), respectively. Here we specifically discuss the relatively more recent global path planners that consider to some extent uncertainty and external disturbances, as well as related work that inspires our work, particularly tube-based and homotopic approaches.

Uncertainty in path planning arises from two sources: (1) imperfect prior knowledge of the environment and (2) deviations during execution due to motion/sensing noise or controller limitations. Some approaches model this uncertainty through collision probability bounds on roadmaps (Guibas et al. 2010), enabling chance-constrained optimization that bounds collision risk (Blackmore, Ono, and Williams 2011; Johnson and Yip 2021). For non-holonomic vehicles, the notion of non-navigable area captures regions where the vehicle may reach an unsafe state (ICS) despite its best effort (Bouguerra, Fraichard, and Fezari 2019; Blaich et al. 2015). The boundary’s shape can depend on uncertain disturbances, making its identification an open challenge. We adaptively identify non-navigable areas based on the ASV’s encounter direction within the external disturbance field, taking into account the vehicle’s non-holonomic constraints and probabilistically reasoning about worst-case scenarios—mirroring the maritime concept of an abort position, where fallback options for the safety are ensured under adverse conditions.

External disturbances have been mostly considered in the context of control and trajectory tracking, with methods based on feedback tracking controller and a reconfigurable disturbance compensation mechanism (Liu et al. 2018), Generalized Reduced Gradient (Rudd et al. 2017), and reinforcement learning (Faust, Malone, and Tapia 2015; Blekas and Vlachos 2018). In global path planning, some methods set an additional fixed safety distance that accounts for currents (Singh et al. 2018). Aine and Sujit (2016) integrates A* with a controller for feasibility checking (including disturbances) of connecting cells along the path. Trajectory generation using Hamilton-Jacobi reachability analysis to find error propagation due to disturbance can provide safety guarantees within a prediction horizon (e.g., for drones (Herbert et al. 2017; Seo et al. 2019)). External disturbances are also considered for optimizing the path energy efficiency. Jones and Hollinger (2017) proposed a stochastic trajectory optimization approach for underwater vehicles. An approach based on graphs with a flow model and cost function that includes energy finds paths for ASVs and AUVs so that they can leverage the dynamics of the surrounding flow (Kularatne, Bhattacharya, and Hsieh 2018). A two-stage planner composed of A* and a solver for an optimal continuous problem uses an energy cost function that considers wind to find energy-efficient paths (Bitar et al. 2020). We solve instead a global path planning problem, considering both feasibility, which is dynamically determined based on external disturbances, and energy efficiency.

Path boundaries were proposed for safe path planning for swarm of robots in cluttered environments within a single homotopic option based on the tube (Mao, Fu, and Quan 2024) or path set (Huang, Tang, and Au 2024). Similarly, robust motion planners leveraged the idea of funnels, which provides safety guarantees (Singh et al. 2017; Majumdar and Tedrake 2017). The concept of such boundaries inspires our method to account for the uncertainty and external disturbances described above, integrated in global path planning.

Previous approaches utilized homotopy classes (Bhattacharya, Likhachev, and Kumar 2012) to facilitate multirobot exploration (Kularatne, Bhattacharya, and Hsieh 2018; Huang, Tang, and Au 2024). We explicitly keep track of such homotopy classes during planning phase for maintaining alternatives the ASV can commit/replan, allowing for adaptive current padding per homotopy, thus increasing ASV safety.

## Problem Formulation

The problem is finding an optimal path Γ∗that is both safe and energy-efficient:

Γ∗= arg min

Γ

J(Γ) (1)

where Γ is a path in the spatial environment W ⊂R2 and J(·) is the objective function representing energy cost, influenced by fuel consumption under the disturbance field.

The disturbance field is denoted as C(t, x) which acts on the ASV at position x ∈R2 and time t. The navigable area at time t, denoted N(t), is the subset of W where the ASV can safely operate under the effect of C.

We consider a marine vehicle with a non-holonomic kinematic model and constant thrust, i.e., constant effort along the forward direction, while ω action for the directional change can be taken within [−ωmax, +ωmax]. This maneuvering behavior is typical for vessels operating at a fixed RPM. The resulting effective velocity in the world frame is:

Vworld(x, t) = Vc(x, t) + Vthrust(x, t) (2) where Vworld is the net velocity relative to the ground, Vthrust is the velocity relative to the water (i.e., propulsion), and Vc is the current-induced velocity at x.

Unlike prior works (e.g., (Kularatne, Bhattacharya, and Hsieh 2016; Doering et al. 2023)) that assume underactuated dynamics, we assume ||Vthrust(x, t)|| > ||Vc(x, t)||: this means the robot can overcome adverse currents, while still being constrained by the non-holonomic dynamics observed in practical scenarios. This formulation captures real-world navigational concerns—such as minimizing fuel consumption in the presence of misaligned currents—while ensuring the bounded safety, even in narrow or risk-prone passages.

We assume the map M and the 2D vector field C are available a priori (e.g., from forecasts) and remain unchanged during our short navigation time spans (Fossen 2021). We demonstrate that different currents in the same region at different times can result in varying optimal paths.

Main Approaches RENEW planner’s overall architecture is shown in Figure 2.

18334

<!-- Page 3 -->

No go zone

Disturbances

Info

Navigation

Mesh

Homotopy

Search

High-level

Planner Adaptive No

Go Zone

Low-level

Planner

H 1 H 2

H k

…

Energy cost

Sampling

Optimal path

**Figure 2.** System Architecture.

No Go Zone

We define an unsafe state L ⊂R2 as hard No Go Zone where the ego vehicle R must never enter, e.g., shorelines, buoys, and islands. Such L consists of collections of obstacles, represented by polygonal shapes. V(τ) (soft No Go Zone) denotes a set of positions where R may enter L despite its best effort τ (i.e., hard-over maneuver) due to, e.g., disturbances. V(τ)c is a set of positions where R can avoid L even if there exist disturbances, to prevent ICS.

We first construct a set of navigation meshes within the complement of the no go zone, denoted as Lc, using convex polygons. To ensure that obstacle boundaries are preserved during meshing, we employ Constrained Delaunay Triangulation (CDT) (Shewchuk 1996). This constraint-based triangulation partitions the environment into distinct subregions: L and Lc. We then identify V(τ) by adaptive padding proposed in the next sections. The resulting navigation meshes provide a structured representation of the robot’s N = V(τ)c, facilitating efficient planning. Our proposed method varies V(τ) depending on homotopic classes.

Homotopic Channel

One of our key ideas is to construct a set of homotopic channels H consisting of multiple homotopy classes found over CDT in Lc (Figure 3). Intuitively, one homotopic channel in H represents a bound that R can follow. Multiple paths belong to a corresponding homotopy class if they meet the criteria, i.e., collision avoidance and kinematic feasibility.

0 50 100 X Coordinate [m]

0 50 100 Y Coordinate [m]

**Figure 3.** CDF-based navigation mesh and a single CDT homotopic channel. The color is lighter from the start (10,10) to the goal (90,90). Hard No Go Zone L is brown.

0 5 10 Y [m]

0 5 10 Y [m]

0 5 10 Y [m]

−5 0 5 X [m]

0 5 10 Y [m]

−5 0 5 X [m]

0 5 10 Y [m]

−5 0 5 X [m]

0 5 10 Y [m]

**Figure 4.** Irregular turning circle behaviors under the external disturbances with their noises: (top) northward current; (bottom) southward current; (left) turning circles from the robot in the example at (0,0) with heading samples [ϕ −∆ϕ, ϕ + ∆ϕ]. The closest turning circle (magenta) and its closest point (black dot) to the constrained edge are marked; (mid) turning circle behaviors under disturbance noises; (right) offset padding V(τ) for the constrained edge (gray), to ensure safety within the probabilistic bound.

To find such channels, we build roadmap by using dual property of CDT. Specifically, the CDT becomes a node and the edge shared by the neighboring triangles becomes a connection between nodes. Intuitively, from a start point to a goal point, we find a series of triangles, i.e., channel. We use the Depth First Search algorithm that can give one distinct channel, and continue to find topologically distinct channels H such that |H| = k, where k is the maximum homotopy classes to be found by user input. Note that k ≤2n where n is the number of total obstacles in the environment.

Definition 1 (Channel and Homotopic Channel) A series of triangles is defined as a channel that the robot can follow. For each homotopy option, there exists only one set of triangles, i.e., channel.

In this section, for simplicity, we present an example with obstacles represented as convex polygons. However, as validated in our experiments, the definitions and conditions also hold with concave obstacles by using a crossing-sequencebased method to identify homotopy classes (Tovar, Cohen, and LaValle 2009; Kim and Likhachev 2015).

Adaptive No Go Zone

Irregular turning: We consider a turning motion with constant forward speed and a non-zero turning rate ω. Based on Equation (2), the system dynamics are given by:

˙px = vthrust cos(θ) + cx, ˙py = vthrust sin(θ) + cy, ˙θ = ω with vthrust the thrust-induced speed in the body frame, and cx, cy the external disturbances in the global frame.

We define the best-effort control input τ as a hard-over turn with angular velocity either −ωmax or ωmax, to prevent entering the no go zone L. In alignment with naval

18335

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-003-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

0 2 6 Best effort [m]

north current south current 0 2 6 Best effort distance [m]

0.0 0.5 1.0 Cumulative Prob.

**Figure 5.** Probabilistic distribution and bounds of the besteffort maneuvers. (left) spatial extent of extreme points induced by best-effort actions; and (right) cumulative distribution of best-effort distances, along with bounded values based on the 95th percentile threshold (σ = 0.95 for 4.47 m: northward current, 1.96 m: southward current).

architecture concepts—specifically advance and tactical diameter—it is essential to identify the extreme points reached during such turns to ensure the robot remains outside of L.

Without disturbances, the robot traces a regular turning circle with radius r = vthrust/ω. In the presence of disturbances (i.e., |cx| > 0 or |cy| > 0), the turning shape becomes irregular (Figure 4). In other words, the disturbances affect the turning circle, thus the soft no go zone V(τ). Adaptive padding: To identify such varying V(τ), we propose a sampling-based approach to estimate the extreme points under worst-case conditions—when the robot comes closest to a constrained edge of a triangulated obstacle. Specifically, within a triangle, we sample hard-over turns τ ∈{−ω, +ω} based on: (1) the midline travel direction ϕ; (2) the cross-track offset ∆ϕ, (3) and the average direction and magnitude of disturbances. Among all sampled turns, we select the path that approaches the constrained edge most closely (i.e., the worst case)–see Figure 4 (left).

Furthermore, external disturbances are not constant within a triangle. To capture local variability, we resample based on the standard deviation of the current’s direction and magnitude (Figure 4 (mid)). Using these samples, we compute the percentile of distances to the closest edge and define a probabilistic collision bound σ, as shown in Figure 5. This distance is used as a padding offset from the original CDT boundaries. In other words, the robot avoids collision with the no go zone with probability σ, implying a risk level of 1−σ. For a given homotopic channel, we apply padding along the channel. Our method adapts to both the direction of the external force and the obstacle’s relative location, allowing for a more precise estimation of safety margins (Figure 4 (right)). Moreover, as shown in Figure 6, even the same constrained edge may experience different padding offsets depending on the homotopic options that change the relationship by the currents, vehicle, and constrained edge.

High-level Planner

Once we identify k topologically distinct homotopic channels and apply adaptive no go zone padding, the high-level planner evaluates fuel efficiency to select the optimal homotopy. To enable fair comparison across topologically distinct

0 50 100 X Coordinate [m]

0 50 100 Y Coordinate [m]

0 50 100 X Coordinate [m]

0 50 100 Y Coordinate [m]

**Figure 6.** Adaptive padding (gray) along a homotopy channel (blue triangles). (left) infeasible homotopy class due to the passage blocked by padding; and (right) feasible.

options, we first generate N paths per homotopy class. For each homotopy, we sample points along the passing edges— the shared boundaries between consecutive triangles within the homotopic sequence. The connection of these sampled points forms a complete path from the start to the goal. The convexity property of the CDT ensures that any straight-line connection between two points lying within or on a triangle is feasible—i.e., collision-free—thus guaranteeing that the full path from start to goal is geometrically valid.

However, geometric feasibility does not guarantee kinematic feasibility. To ensure that each path can be smoothed into a kinematically feasible trajectory, we incorporate a check during sampling. Instead of relying on a fixed turning radius r = vthrust/ω, we introduce an effective radius r′ = v′ world/ω, where v′ world represents the net effective speed based on average external disturbances within the local region a around each waypoint. This accounts for variations in turning capability due to environmental forces.

We then evaluate each path within every homotopy by computing a fuel cost defined as:

F =

Z

C α · vk thrust · ds vthrust +⃗c · ˆT(s)

(3)

where α is a system-dependent efficiency constant, vthrust is the constant thrust speed in still water, k is a model exponent (typically k = 2 for quadratic drag), ds is the differential path length,⃗w is the external current vector, and ˆT(s) is the unit tangent vector of the path at position s. The dot product⃗c· ˆT(s) captures the component of the current aiding or opposing the motion.

Finally, the best homotopy class h⋆minimizing the fuel cost is computed as the harmonic mean over sampled paths:

h⋆= arg min h∈H



 



1

|Ph|

|Ph| X i=1

## 1 Fh,i





−1

  (4)

where H is the set of all candidate homotopy classes considered by the planner; Ph is the set of all valid paths in homotopy class h; |Ph| denotes the number of paths within Ph; and Fh,i is the total fuel consumption of the i-th path in homotopy class h. The harmonic mean penalizes outliers with high fuel costs more than the arithmetic mean, promoting robustness in the selection process.

18336

<!-- Page 5 -->

Low-level Planner Once the optimal homotopy h⋆is found, we proceed to determine the optimal path within the set Ph⋆. Given the computations in the previous stage, each candidate path in Ph⋆ satisfies kinematic feasibility under disturbances. We select the optimal path p⋆that minimizes the fuel cost:

p⋆= arg min p∈Ph⋆F(p) (5)

Thus, the robot can follow the optimal trajectory while accounting for dynamic constraints and external disturbances, such as water currents, along the chosen homotopic channel.

## Experiments

and Results We validated our method in real-world and simulated environments against grid A⋆and sampling-based planners, including RRT, RRT⋆, PRM. The suffix “-D” (e.g., RRT-D) denotes the integration of Dubins constraints.

For sampling-based methods, we performed 10 runs in each environment using different random seeds. For PRM, PRM-D, and grid A⋆, we extracted multiple topologically distinct paths using the H-signature method proposed in (Bhattacharya, Likhachev, and Kumar 2012), and used A⋆as search algorithm. Therefore, PRM, PRM-D, and grid A⋆naturally find the shortest path belonging to each homotopy class. Additionally, we applied the path smoothing technique SIMPLIFYMAX from the OMPL library (S¸ucan, Moll, and Kavraki 2012) to enhance kinematic feasibility—especially for methods that produce piecewise-linear paths such as RRT, RRT⋆, and PRM. For grid A⋆, we implemented Dubins-style motion with a fixed turning radius r = vthrust/ω (Macenski, Booker, and Wallace 2024).

We used a vehicle model based on our custom-built ASV, which has a length of 2 m and maximum linear and angular speeds of 1.0 m/s and 35 °/s, respectively. These parameters were obtained from real-world experiments, as described in (Anonymous 2020). We tested the vehicle motion under Dubins constraints during the experiments.

We compared performance across several metrics. Fuel is defined by Equation 3. Safety is measured as the minimum distance to obstacles. The State metric is the number of states explored by the planner. For fair computation comparison, we report only the State metric. One example for insights on our method computational runtime: our method identifies homotopy classes within 10 s in an environment with 7 obstacles, and completes full path optimization using 500 samples per homotopy in approximately 300 s. While we report the Length of each path for reference, our primary objective is not to minimize it. Instead, F/D (fuel per unit distance) metric offers a more meaningful measure of path efficiency under external disturbances.

Next, we discuss results; full data for all environments and additional experiments are in our GitHub repository.

Comparative Studies We conducted a comparative analysis for two scenarios involving different start–goal combinations, using the environment from (Kularatne, Bhattacharya, and Hsieh 2016).

Our proposed method successfully identifies an optimal path by leveraging favorable current directions (Figure 7 (left)). Specifically, it identifies multiple topologically distinct options, selects the optimal homotopy class, and then chooses the best path within that class. As a result, the vehicle achieves reduced fuel consumption–even when the selected path is longer–by following routes where the currents provide assistance. See Table 1 for quantitative results.

We further evaluated our method under different values of k, the maximum number of homotopy classes considered—see Figure 7 (right). Notably, the case with k = 16 enabled the method to find the optimal path, with improvements compared to k = 1: fuel consumption (202.25 vs. 325.18), safety (16.40 vs. 7.70), path length (297.59 vs. 322.80), and fuel efficiency (F/D: 0.680 vs. 1.007).

0 100 200 X [m]

0 100 200 Y [m]

ours RRT RRT-D RRT* RRT*-D PRM PRM-D grid A* ours ours k=1

**Figure 7.** Qualitative comparison of paths in 4 gyres (start: green, goal: red). (left) ours and original paths by baseline methods; and (right) ours method with k = 16 vs. k = 1.

Real-world Environment We validated our proposed method in real-world scenarios, using nautical charts and sea surface current data from Copernicus (CMEMS 2025) and the National Ocean Satellite Center (NOSC 2025). The original nautical chart polylines were simplified using the Douglas–Peucker algorithm (Douglas and Peucker 1973). Each environment was scaled down to ASV-relevant dimensions for simulation purposes while preserving the geometric structure.

We selected three distinct environments: (1) Hansando (1:15 scale), located in the southern waters of Korea, features a complex current field and intricate topological structure within a coastal area (National Geospatial- Intelligence Agency 2022), with generally strong adverse current against the navigation direction; (2) Far East Asian waters (1:2000 scale), which are consistently affected by the strong northeastward-flowing Kuroshio current, influencing nearby maritime traffic (Chang et al. 2013); and (3) the Palawan Passage (1:5000 scale), where current directions change significantly between seasons, introducing dynamic navigational challenges (Hu et al. 2000).

First, although the path found by our method is not the shortest, the fuel efficiency and F/D are the best (Figure 8 and Table 1 (Hansando)). In some cases, the smoothed path is significantly worse than the original path, e.g., RRT. This occurs as the smoothing process does not explicitly account for external disturbances during optimization, leading to paths that are adversely affected by opposing currents.

18337

<!-- Page 6 -->

Ours RRT RRT-D RRT⋆ RRT⋆-D PRM PRM-D grid A⋆

Env. Metric S O S O S O S O S O S O S O S

4-Gyre (200×200) k=16

Fuel ↓ 202.25 310.57 236.27 377.45 293.34 288.07 235.09 354.94 269.92 295.35 219.17 657.11 224.84 225.68 215.15 – ±77.59 ±39.47 ±93.25 ±83.49 ±65.32 ±38.15 ±81.31 ±65.90 ±25.13 ±20.30 ±64.85 ±75.90 – –

Safety ↑ 16.40 1.77 1.18 3.38 4.00 1.77 1.05 3.23 3.01 2.64 0.99 3.98 4.20 1.42 0.97 – ±0.84 ±0.48 ±2.93 ±2.82 ±0.85 ±0.47 ±2.93 ±2.66 ±1.57 ±0.44 ±5.37 ±4.14 – –

F/D ↓ 0.680 0.99 0.92 1.19 1.13 1.01 0.93 1.14 1.15 0.83 0.86 1.04 0.86 0.857 0.841 – ±0.22 ±0.15 ±0.28 ±0.32 ±0.18 ±0.15 ±0.25 ±0.28 ±0.07 ±0.06 ±0.07 ±0.27 – – States ↓ 86 394.9±75.2 476.7±127.8 394.9±75.2 526.5±135.5 17662±5275 19174±7069 86521 (26) (2000) (2000) (10000)

Length* 297.59 311.28 256.12 317.14 259.72 305.71 255.84 309.09 257.59 291.88 255.99 358.17 266.98 263.25 255.92 (–) ±10.54 ±0.42 ±21.21 ±3.65 ±8.72 ±0.43 ±17.81 ±2.52 ±7.95 ±0.89 ±28.03 ±4.17 – –

Hansando (1533×1619) k=10

Fuel ↓ 2639.39 3566.74 3957.74 3634.23 3618.30 3564.63 3958.51 3428.69 3270.21 3148.71 2854.45 3470.89 2844.51 2863.82 2838.78 – ±159.10 ±618.34 ±355.33 ±421.82 ±159.10 ±618.35 ±170.68 ±388.83 ±183.73 ±204.84 ±96.70 ±36.09 – –

Safety ↑ 22.61 8.21 1.28 4.84 15.36 8.21 1.28 8.53 28.65 4.15 2.33 3.44 2.80 1.18 1.46 – ±13.41 ±0.32 ±5.76 ±12.79 ±13.41 ±0.32 ±10.38 ±13.76 ±4.90 ±2.01 ±2.27 ±2.68 – –

F/D ↓ 0.951 1.41 2.02 1.45 1.82 1.41 2.02 1.44 1.90 1.03 1.14 1.26 1.34 1.092 1.124 – ±0.14 ±0.43 ±0.16 ±0.25 ±0.14 ±0.43 ±0.15 ±0.25 ±0.06 ±0.08 ±0.13 ±0.13 – – States ↓ 161 2076.7±810.2 2120.9±601.8 2076.7±810.2 1831.6±539.3 21514.1±6425 21692.1±1937 42847 (34) (7000) (7000) (17408)

Length* 2775.04 2555.30 1997.28 2509.89 1992.01 2555.30 1997.28 2404.90 1935.47 3041.34 2560.38 2703.50 2095.76 2623.33 2526.09 – ±251.35 ±204.54 ±102.09 ±63.87 ±251.35 ±204.54 ±120.28 ±146.81 ±228.30 ±160.12 ±154.31 ±134.86 – –

Far East (1360×1270) k=10

Fuel ↓ 1247.83 1957.68 1512.88 1899.56 1472.81 1956.54 1513.44 1859.15 1447.35 1569.65 1386.34 1760.51 1387.14 1479.12 1288.27 – ±188.16 ±14.07 ±123.32 ±111.28 ±188.16 ±14.07 ±143.95 ±125.91 ±129.47 ±117.33 ±46.64 ±73.32 – –

Safety ↑ 37.69 2.11 1.13 1.95 3.63 2.11 1.24 2.51 4.56 4.39 1.25 3.12 2.93 1.05 1.80 – ±1.10 ±0.12 ±1.27 ±2.56 ±1.10 ±0.12 ±2.00 ±3.05 ±3.29 ±0.92 ±3.02 ±3.44 – –

F/D ↓ 0.776 0.95 0.95 0.93 0.90 0.95 0.95 0.93 0.92 0.94 0.88 0.88 0.85 0.889 0.834 – ±0.05 ±0.00 ±0.05 ±0.06 ±0.05 ±0.00 ±0.07 ±0.06 ±0.08 ±0.07 ±0.03 ±0.06 – – States ↓ 183 2628.9±1318.1 2360.5±663.5 2628.9±1318.1 2451.6±710.9 57335.3±12757 56395.4±11991 32794 (73) (7000) (7000) (24948)

Length* 1607.33 2051.72 1587.42 2037.12 1638.50 2051.72 1587.42 1971.90 1613.50 1706.03 1544.24 1879.85 1547.43 1664.21 1545.30 – ±92.45 ±17.03 ±80.75 ±44.35 ±92.45 ±17.03 ±101.19 ±51.67 ±89.76 ±19.06 ±83.26 ±27.12 – –

**Table 1.** Performance comparison of paths across environments (size in meters). The best and second-best performances are highlighted in green and yellow. “O” and “S” denote original and smoothed paths. For sampling-based methods, values are mean in first row and ±std in second row over 10 runs. The number in parentheses in the States metric indicates the size of the discretized environment (Ours: triangulation vertices; PRM and PRM-D: sampled nodes; grid A⋆: grid cells with 2 m resolution for 4-gyre, and 10 m for Hansando and Far East). k denotes the maximum number of homotopy classes considered. *Note: our objective is not to minimize path length, but we report it for reference.

Ours Fuel Safety Length F/D Summer 160.563 9.153 164.586 0.976 Winter 131.787 13.133 167.053 0.789

**Table 2.** Performance comparison of paths across the summer and winter season.

Next, we show that our method can adaptively choose the optimal path under varying environmental conditions, even with the same start and goal points—see Figure 9 and Table 2. During the summer, our algorithm found the westside route to avoid strong northeast-directed currents along the east side of Palawan Island. During winter instead, our method found an efficient route along the east side thanks to the southwest-directed currents.

Ablation Studies We investigated how padding schemes, including our adaptive padding, and the path planning algorithms behave in controlled scenarios. We confined the homotopy class (i.e., the path must pass on the right side of the obstacle) and var-

0 500 X [m]

0 500 Y [m]

**Figure 8.** Qualitative comparison using real current data in Hansando area with the sea surface current in summer 2024.

ied the direction of a uniform water current field (Figure 10).

When the smoothed shortest path aligns with the optimal one, grid A⋆and our method yield comparable fuel efficiency, provided they share the same padding scheme (adaptive, no, or fixed padding). Notably, while 2 m resolution grid A⋆initially appears safer, smoothing results in tighter paths around obstacles, ultimately bringing its safety perfor-

18338

<!-- Page 7 -->

0 50 100 X [m]

0 50 100 150 Y [m]

0 50 100 X [m]

0 50 100 150 Y [m]

0.2

0.4

0.6

0.8

Current Speed [m/s]

**Figure 9.** Qualitative comparison of paths proposed by our method in the waters near Palawan Passage in the Philippines. (left) summer sea surface current in July 2024; and (right) winter sea surface current in December 2024.

Case Type Metric Ours grid A⋆-O grid A⋆-S a Adaptive

(45°)

Fuel ↓ 56.76 63.77 55.72 Safety ↑ 3.87 9.00 3.77 F/D ↓ 0.66 0.70 0.66 Length* 85.80 91.60 84.65 b No (45°)

Fuel ↓ 52.86 58.34 52.23 Safety ↑ 1.26 1.42 1.00 F/D ↓ 0.65 0.67 0.64 Length* 81.68 86.63 81.10 c Fixed

(45°)

Fuel ↓ 54.39 60.14 53.50 Safety ↑ 3.48 5.00 3.69 F/D ↓ 0.65 0.68 0.65 Length* 83.19 88.28 82.31 d Adaptive

(270°)

Fuel ↓ 311.29 357.97 360.37 Safety ↑ 6.46 7.00 5.43 F/D ↓ 3.34 3.98 4.32 Length* 93.16 89.94 83.45

**Table 3.** Ablation study results. *Note: our objective is not to minimize path length as noted in Table 1.

mance in line with our approach.

In contrast, there are cases where our method significantly outperforms grid A⋆. Our planner produced longer paths that are more fuel-efficient, especially when the smoothed shortest path encounters opposing currents that increase fuel consumption. Our method generates zig-zag paths with longer distances, but successfully avoids adverse currents and reduces overall fuel cost (Figures 10(right) and Table 3 (case d)). In these scenarios, grid A⋆selects shorter but less efficient paths under the same homotopy and padding scheme.

Lastly, Figures 10(left) and 10(right) demonstrate how our method ensures safety by satisfying a probabilistic collision bound through adaptive padding during passage, in contrast to the fixed padding shown in Figure 10(center-right).

Contingency Maneuver We validated how our proposed method ensures the avoidance of ICS, i.e., guaranteeing no collision even after executing a contingency maneuver: based on the paths found, we conducted forward simulations assuming the presence of an unexpected obstacle every 1 m along the path, and performed a contingency maneuver to test safety.

50 X [m]

0 50 100

50 X [m]

0 50 100

50 X [m]

0 50 100

50 X [m]

0 50 100

**Figure 10.** Qualitative comparison of paths by ablation tests with the current direction β. The padded area is colored in gray and the original obstacle area is in brown. (left) adaptive padding (β=45◦); (center-left) no padding (β=45◦); (center-right) fixed padding (β=45◦); (right) adaptive padding (β=−90◦).

Scenario Metric Ours RRT RRT-D RRT⋆RRT⋆-D PRM PRM-D grid A⋆

4-gyre Collision 0 79 21 81 30 69 23 79 Trials 1494 1280 1285 1280

Hansando Collision 0 34 8 61 15 14 19 61 Trials 2788 1906 2025 2561

Far East Collision 0 72 0 71 0 71 20 31 Trials 1608 1545 1582 1545

Total Collision 0 185 29 213 45 154 62 128 Trials 5890 4731 4892 5386

**Table 4.** Collision counts and total attempts during the contingency maneuvers over the found paths. green: the lowest collision count; red: the highest count.

Under dynamic disturbances, our proposed method consistently avoided collisions (Table 4). In contrast, state-ofthe-art approaches experienced collisions—an outcome that is critical in real-world scenarios where the uncertainty of environmental disturbances poses significant safety risks.

## Conclusion

and Future Steps

We presented a risk- and energy-aware global planner for ASVs navigating dynamic disturbances. By integrating adaptive padding and a worst-case best-effort strategy, our method ensures fuel efficiency while maintaining strict safety bounds. The hierarchical, triangulation-based approach identifies topologically distinct, kinematically feasible paths. Validated across controlled and real-world scenarios, the planner adapts to varying current profiles and obstacle configurations, with adaptive padding significantly increasing robustness in high-risk regions.

Future work includes extending this approach to scenarios where the vehicle can adjust its speed, rather than relying on the fixed-effort assumption used in this study. We expect that allowing speed modulation will result in more gliding behavior through the current field. Additional directions include integrating real-time current forecasts or onboard estimation of the vector field, as well as constructing local obstacle maps in partially or fully unknown environments.

18339

![Figure extracted from page 7](2026-AAAI-renew-risk-and-energy-aware-navigation-in-dynamic-waterways/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgments

This work is supported in part by the Burke Research Initiation Award, NSF CNS-1919647, 2144624, OIA1923004, and NOAA NH Sea Grant.

## References

Aine, S.; and Sujit, P. 2016. Integrating planning and control for efficient Path planning in the presence of environmental disturbances. In Proceedings of the International Conference on Automated Planning and Scheduling, volume 26, 441–449. Anonymous. 2020. Details omitted for double-blind review. 1805–1812. Bhattacharya, S.; Likhachev, M.; and Kumar, V. 2012. Topological constraints in search-based robot path planning. Autonomous Robots, 33: 273–290. Bitar, G.; Martinsen, A. B.; Lekkas, A. M.; and Breivik, M. 2020. Two-stage optimized trajectory planning for ASVs under polygonal obstacle constraints: Theory and experiments. IEEE Access, 8: 199953–199969. Blackmore, L.; Ono, M.; and Williams, B. C. 2011. Chanceconstrained optimal path planning with obstacles. IEEE Transactions on Robotics, 27(6): 1080–1094. Blaich, M.; Weber, S.; Reuter, J.; and Hahn, A. 2015. Motion safety for vessels: An approach based on Inevitable Collision States. In IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 1077–1082. Blekas, K.; and Vlachos, K. 2018. RL-based path planning for an over-actuated floating vehicle under disturbances. Robotics and Autonomous Systems, 101: 93–102. Bouguerra, M. A.; Fraichard, T.; and Fezari, M. 2019. Viability-Based Guaranteed Safe Robot Navigation. Journal of Intelligent & Robotic Systems, 95(2): 459–471. Chang, Y.-C.; Tseng, R.-S.; Chen, G.-Y.; Chu, P. C.; and Shen, Y.-T. 2013. Ship Routing Utilizing Strong Ocean Currents. Journal of Navigation, 66(6): 825–835. CMEMS. 2025. E.U. Copernicus Marine Service Information – Global Ocean Physics Analysis and Forecast. https: //doi.org/10.48670/moi-00016. Accessed: 2025-07-01. Doering, A.; Wiggert, M.; Krasowski, H.; Doshi, M.; Lermusiaux, P. F.; and Tomlin, C. J. 2023. Stranding Risk for Underactuated Vessels in Complex Ocean Currents: Analysis and Controllers. In 2023 62nd IEEE Conference on Decision and Control (CDC), 7055–7060. IEEE. Douglas, D. H.; and Peucker, T. K. 1973. Algorithms for the reduction of the number of points required to represent a digitized line or its caricature. Cartographica: the international journal for geographic information and geovisualization, 10(2): 112–122. Faust, A.; Malone, N.; and Tapia, L. 2015. Preferencebalancing motion planning under stochastic disturbances. In IEEE International Conference on Robotics and Automation (ICRA), 3555–3562. IEEE. Fossen, T. 2021. Handbook of Marine Craft Hydrodynamics and Motion Control. Wiley.

Guibas, L. J.; Hsu, D.; Kurniawati, H.; and Rehman, E. 2010. Bounded uncertainty roadmaps for path planning. In Algorithmic Foundation of Robotics VIII: Selected Contributions of the Eight International Workshop on the Algorithmic Foundations of Robotics, 199–215. Springer. Hart, P. E.; Nilsson, N. J.; and Raphael, B. 1968. A formal basis for the heuristic determination of minimum cost paths. IEEE transactions on Systems Science and Cybernetics, 4(2): 100–107. Herbert, S. L.; Chen, M.; Han, S.; Bansal, S.; Fisac, J. F.; and Tomlin, C. J. 2017. FaSTrack: A modular framework for fast and guaranteed safe motion planning. In IEEE Annual Conference on Decision and Control (CDC), 1517–1522. IEEE. Hu, J.; Kawamura, H.; Hong, H.; and Qi, Y. 2000. A Review on the Currents in the South China Sea: Seasonal Circulation, South China Sea Warm Current and Kuroshio Intrusion. Journal of Oceanography, 56(6): 607–624. Huang, J.; Tang, Y.; and Au, K. W. S. 2024. Homotopic Path Set Planning for Robot Manipulation and Navigation. Robotics: Science and Systems (RSS). Johnson, J. J.; and Yip, M. C. 2021. Chance-constrained motion planning using modeled distance-to-collision functions. In IEEE International Conference on Automation Science and Engineering (CASE), 1582–1589. IEEE. Jones, D.; and Hollinger, G. A. 2017. Planning energyefficient trajectories in strong disturbances. IEEE Robotics and Automation Letters, 2(4): 2080–2087. Kavraki, L.; Svestka, P.; Latombe, J.-C.; and Overmars, M. 1996. Probabilistic roadmaps for path planning in highdimensional configuration spaces. IEEE Transactions on Robotics and Automation, 12(4): 566–580. Kavraki, L. E.; and LaValle, S. M. 2016. Motion planning. In Springer handbook of robotics, 139–162. Springer. Kim, S.; and Likhachev, M. 2015. Path planning for a tethered robot using Multi-Heuristic A* with topology-based heuristics. In IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 4656–4663. IEEE. Kularatne, D.; Bhattacharya, S.; and Hsieh, M. A. 2016. Time and Energy Optimal Path Planning in General Flows. In Robotics: Science and Systems (RSS). Kularatne, D.; Bhattacharya, S.; and Hsieh, M. A. 2018. Going with the flow: a graph based approach to optimal path planning in general flows. Autonomous Robots, 42(7): 1369– 1387. LaValle, S. M.; and Kuffner Jr, J. J. 2001. Randomized kinodynamic planning. The international journal of robotics research, 20(5): 378–400. Liu, Z.; Zhang, Y.; Yuan, C.; and Luo, J. 2018. Adaptive path following control of unmanned surface vehicles considering environmental disturbances and system constraints. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 51(1): 339–353. Macenski, S.; Booker, M.; and Wallace, J. 2024. Open- Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics. arXiv preprint arXiv:2401.13078.

18340

<!-- Page 9 -->

Majumdar, A.; and Tedrake, R. 2017. Funnel libraries for real-time robust feedback motion planning. The International Journal of Robotics Research, 36(8): 947–982. Mao, P.; Fu, R.; and Quan, Q. 2024. Optimal virtual tube planning and control for swarm robotics. The International Journal of Robotics Research, 43(5): 602–627. National Geospatial-Intelligence Agency. 2022. Sailing Directions (Enroute): Coasts of Korea and China, Pub. 157. NOSC. 2025. National Ocean Satellite Center – GOCI-II. https://www.nosc.go.kr/eng/main.do. Accessed: 2025-07- 01. Pereira, A. A.; Binney, J.; Hollinger, G. A.; and Sukhatme, G. S. 2013. Risk-aware Path Planning for Autonomous Underwater Vehicles using Predictive Ocean Models. Journal of Field Robotics, 30(5): 741–762. Rudd, K.; Foderaro, G.; Zhu, P.; and Ferrari, S. 2017. A generalized reduced gradient method for the optimal control of very-large-scale robotic systems. IEEE transactions on robotics, 33(5): 1226–1232. Seo, H.; Lee, D.; Son, C. Y.; Tomlin, C. J.; and Kim, H. J. 2019. Robust trajectory planning for a multirotor against disturbance based on hamilton-jacobi reachability analysis. In IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 3150–3157. IEEE. Shewchuk, J. R. 1996. Triangle: Engineering a 2D quality mesh generator and Delaunay triangulator. In Lin, M. C.; and Manocha, D., eds., Applied Computational Geometry Towards Geometric Engineering, 203–222. Berlin, Heidelberg: Springer. Singh, S.; Majumdar, A.; Slotine, J.-J.; and Pavone, M. 2017. Robust online motion planning via contraction theory and convex optimization. In IEEE International Conference on Robotics and Automation (ICRA), 5883–5890. IEEE. Singh, Y.; Sharma, S.; Sutton, R.; Hatton, D.; and Khan, A. 2018. A constrained A* approach towards optimal path planning for an unmanned surface vehicle in a maritime environment containing dynamic obstacles and ocean currents. Ocean Engineering, 169: 187–201. S¸ucan, I. A.; Moll, M.; and Kavraki, L. E. 2012. The Open Motion Planning Library. IEEE Robotics & Automation Magazine, 19(4): 72–82. https://ompl.kavrakilab.org. Tovar, B.; Cohen, F.; and LaValle, S. M. 2009. Sensor Beams, Obstacles, and Possible Paths, volume 57 of Springer Tracts in Advanced Robotics, 317–332. Springer Berlin Heidelberg. Vagale, A.; Bye, R. T.; Oucheikh, R.; Osen, O. L.; and Fossen, T. I. 2021a. Path planning and collision avoidance for autonomous surface vehicles II: a comparative study of algorithms. Journal of Marine Science and Technology, 26(4): 1307–1323. Vagale, A.; Oucheikh, R.; Bye, R. T.; Osen, O. L.; and Fossen, T. I. 2021b. Path planning and collision avoidance for autonomous surface vehicles I: a review. Journal of Marine Science and Technology, 26(4): 1292–1306.

18341
