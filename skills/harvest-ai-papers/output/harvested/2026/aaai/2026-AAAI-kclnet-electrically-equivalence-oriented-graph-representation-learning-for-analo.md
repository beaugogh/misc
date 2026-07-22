---
title: "KCLNet: Electrically Equivalence-Oriented Graph Representation Learning for Analog Circuits"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37109
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37109/41071
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# KCLNet: Electrically Equivalence-Oriented Graph Representation Learning for Analog Circuits

<!-- Page 1 -->

KCLNet: Electrically Equivalence-Oriented Graph Representation Learning for

Analog Circuits

Peng Xu*1, Yapeng Li*2, Tinghuan Chen2, Tsung-Yi Ho1, Bei Yu1

## 1 Department of Computer

Science & Engineering, The Chinese University of Hong Kong 2 School of Science and Engineering, The Chinese University of Hong Kong (Shenzhen)

## Abstract

Digital circuit representation learning has made remarkable progress in the electronic design automation domain, effectively supporting critical tasks such as testability analysis and logic reasoning. However, representation learning for analog circuits remains challenging due to their continuous electrical characteristics compared to the discrete states of digital circuits. This paper presents a direct current (DC) electrically equivalent-oriented analog representation learning framework, named KCLNet. It comprises an asynchronous graph neural network structure with electricallysimulated message passing and a representation learning method inspired by Kirchhoff’s Current Law (KCL). This method maintains the orderliness of the circuit embedding space by enforcing the equality of the sum of outgoing and incoming current embeddings at each depth, which significantly enhances the generalization ability of circuit embeddings. KCLNet offers a novel and effective solution for analog circuit representation learning with electrical constraints preserved. Experimental results demonstrate that our method achieves significant performance in a variety of downstream tasks, e.g., analog circuit classification, subcircuit detection, and circuit edit distance prediction.

## Introduction

Analog and mixed-signal electronic systems have become the backbone of modern technological advancement, driving innovations from medical instrumentation to autonomous vehicles. Their pervasive presence relies fundamentally on the seamless integration of analog and digital circuits. Within this electronic design paradigm, analog circuits emerge as the critical interface bridging the physical and digital worlds (Gray et al. 2009). As shown in Figure 1, analog circuit components such as operational amplifiers and data converters translate real-world signals—temperature variations, sound waves, or wireless transmissions—into digitally processable information while maintaining signal fidelity. Despite occupying less than 20% of modern systemon-chip (SoC) area, analog blocks determine over 40% of product reliability and power efficiency metrics (Sansen 2007). The design of analog circuits confronts challenges rooted in their sensitivity to physical characteristics. Unlike

*These authors contributed equally. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

< l a t e x i t s h a

_ b a s e

6

4

=

"

F h y

6 d

J

P

T

F n

H

F

W

D

4

3 m d

J

8

H u

X w k

O

Y

=

"

>

A

A

A

B

7

H i c b

V

B

N

S

8

N

A

E

J

3

U r q

/ q h

6

9

L

B b

B

U

0 l

E q s e i

F

4

8

V

T

F t o

Q

9 l s

N

+

3

S z

S b s

T o

Q

S

+ h u

8 e

F

D

E q z

/

I m

/

/

G b

Z u

D

V h

8

M

P

N

6 b

Y

W

Z e m

E p h

0

H

W

/ n

N

L a

+ s b m

V n m

7 s r

O

7 t

3

9

Q

P

T x q m y

T

T j

P s s k

Y n u h t

R w

K

R

T

3

U a

D k

3

V

R z

G o e

S d

8

L

J

7 d z v

P

H

J t

R

K

I e c

J r y

I

K

Y j

J

S

L

B

K

F r

J

7 w u h c

F

C t u

X

V

3

A f

K

X e

A

W p

Q

Y

H

W o

P r

Z

H y

Y s i

7 l

C

J q k x

P c

9

N

M c i p

R s

E k n

X

6 m e

E p

Z

R

M

6

4 j

L

F

Y

2

5

C f

L

F s

T

N y

Z p

U h i

R

J t

S y

F

Z q

D

8 n c h o b

M

4

D

2 x l

T

H

J t

V b y

7

+

5

/

U y j

K

6

D

X

K g

0

Q

6

7

Y c l

G

U

S

Y

I

J m

X

9

O h k

J z h n

J q

C

W

V a

2

F s

J

G

N

N

G d p

8

K j

Y

E b

/

X l v

6

R

9

U f c a

9 c b

9

Z a

5

U

8

R

R h h

M

4 h

X

P w

4

A q a c

A c t

8

I

G

B g

C d

4 g

V d

H

O c

/

O m

/

O

+ b

C

0

5 x c w x

/

I

L z

8

Q

3 r

3

4

7

H

<

/ l a t e x i t

>

ZZ

Difference

Amplifier Integrator

DAC

Comparator Analog

Input

1 0 10 1 0

Digital Output

**Figure 1.** ∆Σ analog-to-digital converter (ADC), a typical analog circuit type.

digital counterparts operating in well-defined Boolean domains, analog components are perpetually exposed to parasitic, process variation, and layout-dependent effects. Thus, analog circuit design, from schematic to layout, remains primarily a manual, time-consuming, and error-prone task (Xu et al. 2024b) at present. The inherent electrical complexities of analog circuits create heavy reliance on human expertise, forming a critical bottleneck in automation.

Emerging machine learning paradigms, particularly graph neural networks (GNNs) (Hamilton 2020; Wu et al. 2021), exhibit substantial potential in decoding the design complexity inherent to analog circuits. Naturally, the analog circuits can be viewed as graphs that consist of devices and nets, and their connections. By converting analog circuits into graphs, contemporary methodologies have demonstrated significant progress across critical analog design sub-tasks (Chen et al. 2021; Gao et al. 2021; Kunal et al. 2020; Settaluri et al. 2020; Wang et al. 2020; Dong et al. 2023; Hou et al. 2024; Tu et al. 2025; Xu et al. 2024a, 2025). For analog topology classification, graph-level embeddings are utilized to retrieve the targeted layout templates of analog circuits, such as amplifiers and filters in (Kunal et al. 2020). For subgraph identification, parallel advancements in layout synthesis leverage subgraph-aware GNN architectures to reduce symmetry violations compared to manual design as in (Chen et al. 2021; Gao et al. 2021). At the transistor level, sizing optimization frameworks employing node-centric GNNs reduce simulation iterations (Settaluri et al. 2020; Wang et al. 2020; Dong et al. 2023; Hou et al. 2024). Additionally, analog circuit embeddings are also employed in various stages of analog circuit design, including large-scale subgraph matching during testing and performance optimiza-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

<!-- Page 2 -->

tion during routing (Tu et al. 2025; Xu et al. 2024a, 2025).

Despite widespread use of task-specific circuit embeddings, general analog circuit representation learning remains deficient in physical prior integration and lacks dedicated research as a standalone field. Some efforts attempt to develop multi-modality analog pretraining frameworks, where namebased text embeddings and auxiliary layout data are incorporated to incorporate domain knowledge (Ren et al. 2020; Zhu et al. 2022). While these multi-modality frameworks have demonstrated capability in the analog layout aspect, they have not demonstrated general representation capability at the analog circuit level. As the counterpart of analog circuits, digital circuit representation has demonstrated significant potential in leveraging physical laws, with Boolean algebra operations (J´onsson 1988) becoming a cornerstone of digital circuit representation learning (Li et al. 2022; Shi et al. 2023, 2024; Zheng et al. 2025; Wang et al. 2024; Wu et al. 2025). The intrinsic physical characteristics of analog devices are still neglected. Incorporating physical laws into analog circuit representation learning is crucial to match the success achieved in digital representation learning.

To address these limitations, we propose an electrical physics-inspired representation learning framework, named KCLNet, which incorporates fundamental electrical principles through Kirchhoff’s current law (KCL). Kirchhoff’s Current Law states that the algebraic sum of all currents flowing into a node (junction) is equal to the algebraic sum of all currents flowing out (Paul 2001; Rewie´nski 2011; Athavale 2018). It is a fundamental principle in electrical circuit theory that forms the cornerstone of classical circuit analysis. The KCL is integrated through an electrically simulated message passing and a novel contrastive learning scheme. Our contributions are summarized as follows:

• To honor the electrical current flow, we convert analog circuits to directed acyclic graphs (DAGs) and propose an asynchronous message passing scheme with layerwise propagation from voltage to ground nodes. • Based on that, a physics-informed contrastive objective is designed where depth-wise embeddings enforce Kirchhoff’s current conservation positives and node masking creates electrically inconsistent negatives. We theoretically justify that the proposed contrastive objective can preserve the electrical principle of KCL. • The experimental results show that the analog circuit embeddings learned by our proposed KCLNet can benefit a variety of downstream tasks, with 20.77% improvement in Acc@1 gain in analog circuit classification, 43.36% mAP gain in analog subcircuit detection, and 1.6% MAE gain in analog circuit graph-edit-distance prediction.

Our codes are available at Code — https://github.com/shipxu123/KCLNet.

## Related Work

and Preliminaries Graph Neural Networks (GNNs) GNNs consist of two major components, where the aggregation step aggregates node features of target nodes’

Device Number of Pins Pin types NMOS nd + ng + ns + nb nd, ng, ns, nb PMOS nd + ng + ns + nb pd, pg, ps, pb NPN nb + nc + ne nb, nc, ne PNP nb + nc + ne nb, nc, ne Diode n+, n- Resistor n+, n- Capacitor n+, n- Inductor n+, n-

**Table 1.** Typical Analog Device Types

neighbors, and the combination step passes the previous aggregated features to networks to generate node embeddings. Mathematically, we can update node v’s embedding at the l-th layer by:

el v = AGG hl−1 u |∀u ∈N(v)

, hl v = COMBINE hl−1 v, el v

,

(1)

where N(v) denotes the neighbours of v.

Analog Representation Learning (ARL) Analog circuits pose unique representation challenges due to their bipartite structure (devices and nets) and heterogeneous device types. Recent work explores GNNs to learn analog circuit representations directly from graph structure (Kunal et al. 2020; Settaluri et al. 2020; Wang et al. 2020; Dong et al. 2023; Hou et al. 2024). We give the formal definition of an analog circuit graph as follows:

Definition 1 (Device) Each device vd ∈Vd is associated with attributes such as type (NMOS, RES, CAP, etc.), parameters (e.g., W, L, resistance, capacitance, etc.), and connectivity information, as shown in Table 1.

Definition 2 (Net) Each net vn ∈Vn is a junction where multiple devices connect, with topological metrics decided by the connected pins of devices as shown in Table 1.

Definition 3 (Analog Circuit Graph) The analog circuit graph consists of two groups of nodes Vd, Vn, corresponding to devices and nets. Those two groups of nodes are connected by a set of edges E, where different edge types correspond to different pin types, presenting connection information. Hence, the analog circuit graph has a form of bipartite graph as G = {Vd, Vn, E}.

## Method

Electrically-Simulated Async Message Passing Directed Acyclic Circuit Graph Conversion. In traditional analog representation learning, existing methods frequently disregard the directions of the analog circuit graph (Chen et al. 2021; Kunal et al. 2020; Tu et al. 2025). This omission leads to neglecting current flow directionality during the learning process, resulting in a loss of crucial physical information. Although behavioral-level analog circuits are used to construct directed graphs in (Dong et al. 2023) and (Hou et al. 2024), this approach is specifically tailored for specific analog devices, e.g., operational transconductance amplifier

<!-- Page 3 -->

g

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

O x q

N

H

Y

M

5

G h

Z

A

N

X w

N h

B

Z

Q

E d

D

7

A f

M

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

4

8 t

2

A

9 o

Q

9 l s

J

+ a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

4

Y e

L w w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

4

E d h

O

F

N

A o

E d o

L

J d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

S

Q f l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V h z

H p

0

X

5

9

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B w r m

M

4 g

=

=

<

/ l a t e x i t

> a

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

O x q

N

H

Y

M

5

G h

Z

A

N

X w

N h

B

Z

Q

E d

D

7

A f

M

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

4

8 t

2

A

9 o

Q

9 l s

J

+ a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

4

Y e

L w w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

4

E d h

O

F

N

A o

E d o

L

J d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

S

Q f l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V h z

H p

0

X

5

9

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B w r m

M

4 g

=

=

<

/ l a t e x i t

> a

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

Q

/ z

L n

Z k

E

K r h q j

/

2

D

T

T p

0 n

S

R n

1 g

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

4

8 t

2

A

9 o

Q

9 l s

J

+ a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

4

Y e

L w w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

4

E d h

O

F

N

A o

E d o

L

J d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p y

Q b l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V h z

H p

0

X

5

9

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B x c

G

M

5

A

=

=

<

/ l a t e x i t

> c

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

Q

/ z

L n

Z k

E

K r h q j

/

2

D

T

T p

0 n

S

R n

1 g

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

4

8 t

2

A

9 o

Q

9 l s

J

+ a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

4

Y e

L w w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

4

E d h

O

F

N

A o

E d o

L

J d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p y

Q b l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V h z

H p

0

X

5

9

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B x c

G

M

5

A

=

=

<

/ l a t e x i t

> c b n2 n2 n3 n3

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

F d

0

Z w

8 k r p

O t

N s i u

Q

Z r h

Z v

2 a

/

M

1 k

=

"

>

A

A

A

B

6

H i c b

V

D

L

T g

J

B

E

O z

F

F

+

I

L

9 e h l

I j

H x

R

H

Y

N

Q

Y

8 k

X j x

C

I o

8

E

N m

R

2 a

G

B k d n

Y z

M

0 t

C

N n y

B

F w

8 a

4

9

V

P

8 u b f

O

M

A e

F

K y k k

0 p

V d

7 q

7 g l h w b

V z

2

8 l t b e

/ s

7 u

X

C w e

H

R

8 c n x d

O z l o

4

S x b

D

J

I h

G p

T k

A

1

C i

6 x a b g

R

2

I k

V

0 j

A

Q

2

A

4 m

9 w u

/

P

U

W l e

S

Q f z

S x

G

P

6

Q j y

Y e c

U

W

O l x r

R f

L

L l l d w m y

S b y

M l

C

B

D v

V

/

8

6 g

0 i l o

Q o

D

R

N

U

6

6

7 n x s

Z

P q

T

K c

C

Z w

X e o n

G m

L

I

J

H

W

H

X

U k l

D

1

H

6

6

P

H

R

O r q w y

I

M

N

I

2

Z

K

G

L

N

X f

E y k

N t

Z

6

F g e

0

M q

R n r d

W

8 h

/ u d

1

E z

O

8

8

1

M u

4

8

S g

Z

K t

F w

0

Q

Q

E

5

H

F

1

2

T

A

F

T

I j

Z p

Z

Q p r i

9 l b

A x

V

Z

Q

Z m

0

B h u

C t v

7 x

J

W j d l r

1 q u

N i q l

W i

W

L

I w

8

X c

A n

X

4

M

E t

1

O

A

B

6 t

A

E

B g j

P

8

A p v z p

P z

4 r w

7

H

6 v

W n

J

P

N n

M

M f

O

J

8

/

4 o

2

M

9 w

=

=

<

/ l a t e x i t

> v

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

F d

0

Z w

8 k r p

O t

N s i u

Q

Z r h

Z v

2 a

/

M

1 k

=

"

>

A

A

A

B

6

H i c b

V

D

L

T g

J

B

E

O z

F

F

+

I

L

9 e h l

I j

H x

R

H

Y

N

Q

Y

8 k

X j x

C

I o

8

E

N m

R

2 a

G

B k d n

Y z

M

0 t

C

N n y

B

F w

8 a

4

9

V

P

8 u b f

O

M

A e

F

K y k k

0 p

V d

7 q

7 g l h w b

V z

2

8 l t b e

/ s

7 u

X

C w e

H

R

8 c n x d

O z l o

4

S x b

D

J

I h

G p

T k

A

1

C i

6 x a b g

R

2

I k

V

0 j

A

Q

2

A

4 m

9 w u

/

P

U

W l e

S

Q f z

S x

G

P

6

Q j y

Y e c

U

W

O l x r

R f

L

L l l d w m y

S b y

M l

C

B

D v

V

/

8

6 g

0 i l o

Q o

D

R

N

U

6

6

7 n x s

Z

P q

T

K c

C

Z w

X e o n

G m

L

I

J

H

W

H

X

U k l

D

1

H

6

6

P

H

R

O r q w y

I

M

N

I

2

Z

K

G

L

N

X f

E y k

N t

Z

6

F g e

0

M q

R n r d

W

8 h

/ u d

1

E z

O

8

8

1

M u

4

8

S g

Z

K t

F w

0

Q

Q

E

5

H

F

1

2

T

A

F

T

I j

Z p

Z

Q p r i

9 l b

A x

V

Z

Q

Z m

0

B h u

C t v

7 x

J

W j d l r

1 q u

N i q l

W i

W

L

I w

8

X c

A n

X

4

M

E t

1

O

A

B

6 t

A

E

B g j

P

8

A p v z p

P z

4 r w

7

H

6 v

W n

J

P

N n

M

M f

O

J

8

/

4 o

2

M

9 w

=

=

<

/ l a t e x i t

> v n1 n1 a c b n2 n2 n3 n3 n1 n1 n2 n2 g a c b v

∆= 0 ∆= 0 ∆= 1 ∆= 1 ∆= 2 ∆= 2 ∆= 3 ∆= 3 n1 n1

∆= 4 ∆= 4 n3 n3 n1 n1 n2 n2 n3 n3 v g

∆= 0 ∆= 0

∆= 1 ∆= 1

∆= 2 ∆= 2

∆= 3 ∆= 3

∆= 4 ∆= 4

**Figure 2.** Directed acyclic circuit graph representation: (1) analog circuit; (2) convert bipartite graph representation (left) to DAG via topology sorting (right); (3) electrically-simulated asynchronous message passing scheme.

(OTA), rather than being general-purpose. Notably, in analog circuits, current typically originates from the power supply and traverses along the signal path to the ground, as noticed in (Gao et al. 2021). Consequently, to incorporate the physical characteristics of current flow into representation learning, this paper introduces a novel approach by designating the voltage and ground nodes as special nodes. The original analog circuit graph, a bipartite graph, is thus transformed into a directed acyclic graph (DAG) next.

We first discuss the conversion from undirected to directed graphs via topology sorting (Kahn 1962). The voltage nodes and the ground nodes are added as the start nodes and the end nodes. Based on the current flow direction in the circuit, assign directions to each edge in E. Typically, current flows from voltage nodes to the ground nodes, so the edge directions should align with this current flow. Given that the analog circuit graph is a bipartite graph with edges only between devices and nets, we make the following theorem by topologically traversing from voltage nodes to ground nodes:

Theorem 1 (Alicyclic Guarantee after Conversion) The original graph is a bipartite graph where edges only exist between devices and nets. Assume voltage and ground nodes are special devices added to the graph: 1. Voltage nodes have only outgoing edges with connected nets; 2. Ground nodes have only incoming edges with connected nets. The converted directed graph will be acyclic by traversing the bipartite graph via topology sorting, with the voltage and ground nodes as the start and end points.

The proof of this theorem is provided in Appendix A.6. Following the theorem, the resulting graph becomes a DAG after conversion with voltage nodes as the start nodes and ground nodes as the terminal nodes, as shown in Figure 2. All paths in this DAG, pointing from voltage nodes to ground nodes, are consistent with the physical characteristics and signal flow of the circuit. This conversion process formalizes the structure of an analog circuit into a DAG, providing a foundation graph format for subsequent analog circuit representation learning. Depthwise Message Passing Scheme. Conventional graph neural networks (GNNs) operate synchronously as illustrated in (Bruna et al. 2014; Defferrard, Bresson, and Vandergheynst 2016; Hamilton, Ying, and Leskovec 2017; Velickovic et al. 2018; Xu et al. 2019). In synchronous message passing, all messages flow simultaneously along edges during each iteration.

For better capturing current flow direction as in (Dimo 1975; Wedepohl and Jackson 2002), we propose an asynchronous GNN (AGNN) architecture that simulates depthwise message passing from voltage nodes to ground nodes. We take voltage nodes as the root nodes of the first layer through topological ordering while fixing ground nodes as the terminal layer nodes. The electrically-simulated message passing process initiates from the voltage source node at depth 0, propagates sequentially from depth 1 to d, and ultimately reaches the ground nodes. At each depth level, only the vertices that have received messages from the previous depth propagate messages to their direct successors. The Figure 2 demonstrates an example of embedding nodes using this asynchronous GNN. Formally, for a target vertex v, the aggregation scheme of depth-asynchronous GNN at the ∆-th depth can be described as:

e(l)

{i:D(i,v)=∆−l} = AGG n h(k−1)

u: u ∈N(i)

o

, h(l)

{i:D(i,v)=∆−l} = COMBINE e(l)

i, h(0)

i

,

(2)

where D(i, v) denotes the distance between vertices i and v in the graph, and h(0)

i represents the initial feature vector of vertex i. We used the same AGG and COMBINE functions as GCN, with the sum of normalized neighbor embeddings in our implementation (Kipf and Welling 2017). Thus, our AGNN can be regarded as a GCN variant. Specifically, during the k-th iteration of a depth-∆, aggregation occurs exclusively at vertices located at a distance of ∆−k from the root node v, which selectively integrates messages from their topological predecessors. This aggregated output is then fused with the vertex’s original features to generate its updated representation vector.

Electrically Equivalent Contrastive Learning

Kirchhoff’s Current Law Analysis. KCL is one of the most fundamental theorems in analog circuit analysis (Paul 2001; Rewie´nski 2011; Athavale 2018). It describes a crucial principle: the total current entering a node always equals the total current exiting it, as shown in Figure 3. Formally, it can be defined as:

Iin1 + Iin2 + · · · ⇔Iout1 + Iout2 + · · ·. (3)

A key extension of the KCL is that the algebraic sum of input and output currents of multiple circuit components, i.e., a supernode, remains equal (Zeng and Zeng 2021; Zhu, Chen, and Yang 2024), which is frequently applied in the

<!-- Page 4 -->

I1 I1 I2 I2

I3 I3

I4 I4

I∆=4 I∆=4

I∆=3 I∆=3

I∆=2 I∆=2

||hb||2 ||hb||2 n2 n2 n3 n3 g a c b

||ha||2 ||ha||2

||hc||2 ||hc||2 ||hb||2 ||hb||2 ≥

≥

||ha||2 ||ha||2 ⊕

⊕ ⊕ n2 n2 g a c b v n1 n1 n3 n3

∆= 0 ∆= 0 ∆= 1 ∆= 1 ∆= 2 ∆= 2 ∆= 3 ∆= 3 ∆= 4 ∆= 4

Negatives

ˆI∆=3 ˆI∆=3

ˆI∆=2 ˆI∆=2 n1 n1 n2 n2

< l a t e x i t s h a

1

_ b a s e

6

=

"

O x q

N

H

Y

M

5

G h

Z

A

N

X w

N h

B

Z

Q

E d

D

7

A f

M

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

3

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

8 t

2

A

9 o

Q

9 l s

J

+

3 a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

Y e

L w

3 w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

E d h

O

F

N

A o

E d o

L

J

3 d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

S

Q f l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1

3 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V

3 h z

H p

0

X

5

9

3

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B w r m

M g

=

=

<

/ l a t e x i t

> a

< l a t e x i t s h a

1

_ b a s e

6

=

"

O x q

N

H

Y

M

5

G h

Z

A

N

X w

N h

B

Z

Q

E d

D

7

A f

M

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

3

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

8 t

2

A

9 o

Q

9 l s

J

+

3 a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

Y e

L w

3 w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

E d h

O

F

N

A o

E d o

L

J

3 d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

S

Q f l i l t

1

F y

D r x

M t

J

B

X

I

0

B u

W v

/ j

B m a

Y

T

S

M

E

G

1

7 n l u

Y v y

M

K s

O

Z w

F m p n

2 p

M

K

J v

Q

E f

Y s l

T

R

C

7

W e

L

Q

2 f k w i p

D

E s b

K l j

R k o f

6 e y

G i k

9

T

Q

K b

G d

E z

V i v e n

P x

P

6

+

X m v

D

W z

7 h

M

U o

O

S

L

R e

F q

S

A m

J v

O v y

Z

A r

Z

E

Z

M

L a

F

M c

X s r

Y

W

O q

K

D

M

2 m

5

I

N w

V t

9 e

Z

2

0 r

6 p e r

V p r

X l f q

1

3 k c

R

T i

D c

7 g

E

D

2

6 g

D v f

Q g

B

Y w

Q

H i

G

V

3 h z

H p

0

X

5

9

3

5

W

L

Y

W n

H z m

F

P

7

A

+ f w

B w r m

M g

=

=

<

/ l a t e x i t

> a c b Mask Matrix

Positives

< l a t e x i t s h a

1

_ b a s e

6

=

" h u

6

S v

V

/

P

V p u

0

K

N y

/

1 q

Z

R

2

M

0 m y

8

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

3

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

8 t

2

A

9 o

Q

9 l s

J

+

3 a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

Y e

L w

3 w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

E d h

O

F

N

A o

E d o

L

J

3 d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

O

R q

U

K

2

7

V

X

Y

C s

E y

8 n

F c j

R

G

J

S

/

+ s

O

Y p

R

F

K w w

T

V u u e

5 i f

E z q g x n

A m e l f q o x o

W x

C

R

9 i z

V

N

I

I t

Z

8 t

D p

2

R

C

6 s

M

S

R g r

W

9

K

Q h f p

7

I q

O

R

1 t

M o s

J

0

R

N

W

O

9

6 s

3

F

/

7 x e a s

J b

P

+

M y

S

Q

1

K t l w

U p o

K

Y m

M y

/

J k

O u k

B k x t

Y

Q y x e

2 t h

I

2 p o s z

Y b

E o

2

B

G

/

1

5

X

X

S v q p

6 t

W q t e

V

2 p

X

+ d x

F

O

E

M z u

E

S

P

L i

B

O t x

D

A

1 r

A

A

O

E

Z

X u

H

N e

X

R e n

H f n

Y

9 l a c

P

K

Z

U

/ g

D

5

/

M

H y

9

G

M

6

A

=

=

<

/ l a t e x i t

> g

< l a t e x i t s h a

1

_ b a s e

6

=

" h u

6

S v

V

/

P

V p u

0

K

N y

/

1 q

Z

R

2

M

0 m y

8

=

"

>

A

A

A

B

6

H i c b

V

B

N

S

8

N

A

E

J

3

U r

1 q

/ q h

6

9

L

B b

B

U

0 l

E q s e

C

F

8 t

2

A

9 o

Q

9 l s

J

+

3 a z

S b s b o

Q

S

+ g u

8 e

F

D

E q z

/

J m

/

/

G b

Z u

D t j

Y e

L w

3 w

8 y

8

I

B

F c

G

9 f

9 d g o b m

1 v b

O

8

X d

0 t

7

+ w e

F

R

+ f i k r e

N

U

M

W y x

W

M

S q

G

1

C

N g k t s

G

W

E d h

O

F

N

A o

E d o

L

J

3 d z v

P

K

H

S

P

J

Y

P

Z p q g

H

9

G

R

5

C

F n

1

F i p

O

R q

U

K

2

7

V

X

Y

C s

E y

8 n

F c j

R

G

J

S

/

+ s

O

Y p

R

F

K w w

T

V u u e

5 i f

E z q g x n

A m e l f q o x o

W x

C

R

9 i z

V

N

I

I t

Z

8 t

D p

2

R

C

6 s

M

S

R g r

W

9

K

Q h f p

7

I q

O

R

1 t

M o s

J

0

R

N

W

O

9

6 s

3

F

/

7 x e a s

J b

P

+

M y

S

Q

1

K t l w

U p o

K

Y m

M y

/

J k

O u k

B k x t

Y

Q y x e

2 t h

I

2 p o s z

Y b

E o

2

B

G

/

1

5

X

X

S v q p

6 t

W q t e

V

2 p

X

+ d x

F

O

E

M z u

E

S

P

L i

B

O t x

D

A

1 r

A

A

O

E

Z

X u

H

N e

X

R e n

H f n

Y

9 l a c

P

K

Z

U

/ g

D

5

/

M

H y

9

G

M

6

A

=

=

<

/ l a t e x i t

> g n1 n1 n2 n2 a c b

< l a t e x i t s h a

1

_ b a s e

6

=

" y l

D

G

T s t

9 p s

U g s s

3 p

/

B w v

K o

S

/

U

U

=

"

>

A

A

A

B

9

X i c b

V

D

L

S g

N

B

E

J z

1

G e

M r

6 t

H

L

Y

B

A

8 h d

0

Q o h c h o

A e

9

R

T

A

P

S

N

Y w

O

+ l

N h s w

+ m

O l

V w p

L

/

8

O

J

B

E a

/

+ i z f

/ x k m y

B

0

0 s a

C i q u u n u

8 m

I p

N

N r

2 t

7

W y u r a

+ s

Z n b y m

/ v

7

O

7 t

F w

O m z p

K

F

I c

G j

2

S k

2 h

7

T

I

E

U

I

D

R

Q o o

R

0 r

Y

I

E n o e

W

N r q

Z

+

6 x

G

U

F l

F j

+

M

Y

3

I

A

N

Q u

E

L z t

B

I

D

7 e

9 t

H s

N

E h m

9 p

O

V

J r

1

C

0

S

/

Y

M d

J k

G

S m

S

D

P

V e a v b j

3 g

S

Q

I h c

M q

0

7 j h

2 j m z

K

F g k u

Y

5

L u

J h p j x

E

R t

A x

9

C

Q

B a

D d d

H b

1 h

J a p

U

/

9

S

J k

K k c

7

U

3 x

M p

C

7

Q e

B

5

7 p

D

B g

O

9 a

I

3

F f

/ z

O g n

6

F

2 q w j h

B

C

P l

8 k

Z

9

I i h

G d

R k

D

7

Q g

F

H

O

T a

E c

S

X

M r

Z

Q

P m

W

I c

T

V

B

5

E

K z

+

P

I y a

Z

Z

L

T r

V

U v a s

U a

5

U s j h w

5

J i f k j

D j k n

N

T

I

D a m

T

B u

F

E k

W f y

S t

6 s

J

+ v

F e r c

+

5 q

0 r

V j

Z z

R

P

7

A

+ v w

B

I h

C

R m

A

=

=

<

/ l a t e x i t

>

I∆=2

< l a t e x i t s h a

1

_ b a s e

6

=

" y l

D

G

T s t

9 p s

U g s s

3 p

/

B w v

K o

S

/

U

U

=

"

>

A

A

A

B

9

X i c b

V

D

L

S g

N

B

E

J z

1

G e

M r

6 t

H

L

Y

B

A

8 h d

0

Q o h c h o

A e

9

R

T

A

P

S

N

Y w

O

+ l

N h s w

+ m

O l

V w p

L

/

8

O

J

B

E a

/

+ i z f

/ x k m y

B

0

0 s a

C i q u u n u

8 m

I p

N

N r

2 t

7

W y u r a

+ s

Z n b y m

/ v

7

O

7 t

F w

O m z p

K

F

I c

G j

2

S k

2 h

7

T

I

E

U

I

D

R

Q o o

R

0 r

Y

I

E n o e

W

N r q

Z

+

6 x

G

U

F l

F j

+

M

Y

3

I

A

N

Q u

E

L z t

B

I

D

7 e

9 t

H s

N

E h m

9 p

O

V

J r

1

C

0

S

/

Y

M d

J k

G

S m

S

D

P

V e a v b j

3 g

S

Q

I h c

M q

0

7 j h

2 j m z

K

F g k u

Y

5

L u

J h p j x

E

R t

A x

9

C

Q

B a

D d d

H b

1 h

J a p

U

/

9

S

J k

K k c

7

U

3 x

M p

C

7

Q e

B

5

7 p

D

B g

O

9 a

I

3

F f

/ z

O g n

6

F

2 q w j h

B

C

P l

8 k

Z

9

I i h

G d

R k

D

7

Q g

F

H

O

T a

E c

S

X

M r

Z

Q

P m

W

I c

T

V

B

5

E

K z

+

P

I y a

Z

Z

L

T r

V

U v a s

U a

5

U s j h w

5

J i f k j

D j k n

N

T

I

D a m

T

B u

F

E k

W f y

S t

6 s

J

+ v

F e r c

+

5 q

0 r

V j

Z z

R

P

7

A

+ v w

B

I h

C

R m

A

=

=

<

/ l a t e x i t

>

I∆=2

I∆=3 I∆=3

I∆=4 I∆=4

**Figure 3.** The framework of the physics-guided contrastive learning scheme, named the KCL Loss

analysis of the current values at different depths. Our key idea is to preserve this equivalence in the analog circuit embedding space at different depths:

I∆= I∆′, X h(l)

{i:D(i,v)=∆−l} =

X h(l)

{j:D(j,v)=∆′−l}, (4)

where ∆and ∆′ are different depths of current analog circuit graph. The electrical equivalence relation ”⇔” is an equivalence relation under the constraint of Equation (4). For all device sets within one equivalent depth, the sum of the embeddings of all devices they consist of should be equal. This equation finds a natural equivalence that exists in universal analog circuits with the same current inputs and outputs. Electrical Equivalence as Positives. For an analog circuit DAG graph Gi =

Vi d, Vi n, Ei

, we first use the GNN encoder to process all nodes from different depths in this graph and get their embeddings. As shown in Figure 3, the subcircuit embedding pairs (I∆, I∆′) from different depths are treated as positive pairs, whose embedding discrepancy will be minimized. According to Equation (4), a straightforward loss function is therefore:

L = d X

∆′̸=∆ sim(I∆, I∆′), where sim (v1, v2) is the cosine similarity function v⊤

1 v2 ∥v1∥·∥v2∥as in (He et al. 2020), and d is the maximum depth.

This simple constraint is critical for enhancing the quality of analog circuit embeddings. We show that by enforcing such constraints, the trained neural network can thus preserve the electrical characteristic of KCL with the following theorem: Theorem 2 (Kirchhoff’s Current Law preservation) Let {I∆1, I∆2,..., I∆n} and {I∆′

1, I∆′ 2,..., I∆′ n} be two sets of vectors in Rd, where n ≤d and 0 ≤∆i, ∆′ i < d, and d is the longest distance of the the analog circuit graph. Then, there exists a non-trivial linear map ϕ: Rd →R such that ϕ(I∆i) = ϕ(I∆′ i) for all i = 1, 2,..., n. The proof of this theorem is provided in Appendix A.7.

The theorem shows that for the current embeddings of different layers, there always exists a nonlinear mapping function that determines the input and output current values, with the algebraic sum satisfying KCL. Based on that, we also have the following corollary, with the proof also attached in Appendix A.7:

Corollary 1 Suppose that for each i, the distance between the corresponding vectors after normalization is sufficiently small, i.e., 1 −ˆI⊤

∆i ˆI∆′ i ≤ϵ. A smaller ϵ makes constructing the desired map ϕ(·) easier.

Directly minimizing the loss function is ineffective, as the model would become degenerate by producing all-zero vectors for every subcircuit embedding (Chen et al. 2020; Pang et al. 2022). Typical approaches to address this involve using negative sampling or contrastive learning techniques. In our work, we introduce a novel technique for generating negative samples by leveraging the electrical contradiction of KCL. Electrical Contradiction as Hard Negatives. We introduce a novel technique for generating negative samples ˆI∆by selectively applying dropout to node embeddings at each depth ∆. Because the sum of incoming currents at each layer is equal, artificially creating an imbalance by discarding node embeddings with higher current values naturally generates negative samples from the circuit’s perspective.

As shown in Figure 3, compute the squared L2 norm of its embedding h{i:D(i,v) as a measure of its magnitude and define a binary mask to identify top-k largest nodes:

r∆ i = h(l)

{i:D(i,v)=∆−l}

2,

M ∆[i] =

1 if r∆ i ∈top-k of {r∆

1,..., r∆ n } 0 otherwise.

(5)

Apply the dropout by element-wise multiplication of the original embeddings with the inverted mask:

ˆI∆=

X h{i:D(i,v)} ⊙

1 −M ∆, (6)

where ⊙denotes element-wise multiplication, and 1 is a matrix of ones. This zeros out embeddings for the top-k nodes, creating hard negatives.

<!-- Page 5 -->

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

S

S

G g

3

6

T

S

X

Q r

T k

D p

S

U z v a

Q b

D

+

2

M

0

=

"

>

A

A

A

C

B

3 i c b

V

D

L

S s

N

A

F

J

3

4 r

P

U

V d

S n

I

Y

B

F c l a

S

U

6 r

L g w i

4 r

2

A c

0

I

U w m k

3 b o

Z

B

J m

J k

I

J

2 b n x

V

9 y

4

U

M

S t v

+

D

O v

3

H

S

Z q

G t

F

4

Y n

H

M v

9

9 z j

J

4 x

K

Z

V n f x t r

6 x u b

W d m

W n u r u

3 f

3

B o

H h

3

3

Z

Z w

K

T

H o

4

Z r

E

Y

+ k g

S

R j n p

K a o

Y

G

S a

C o

M h n

Z

O

B

P b w p

9

8

E

C

E p

D

G

/

V

7

O

E u

B

E a c x p

S j

J

S m

P

P

P

M

8

W

M

W y

F m k v

6 y

T e k

T

I

T

X

B i

G

W

3 u d f

I

P b

N m

1 a

1 w

V

V g l

6

A

G y u p

6 p c

T x

D i

N

C

F e

Y

I

S l

H t p

U o

N

0

N

C

U c x

I

X n

V

S

S

R

K

E p

2 h

M

R h p y

F

B

H p

Z v

M

7 c n i h m

Q

C

G s d

C

P

K z h n f

0

9 k

K

J

K

F

V d

1

Z u

J

T

L

W k

H

+ p

4

1

S

F

V

6

7

G e

V

J q g j

H i

0

V h y q

C

K

Y

R

E

K

D

K g g

W

L

G

Z

B g g

L q r

1

C

P

E

E

C

Y a

W j q

+ o

Q

7

O

W

T

V

0

G

/

U b d b

9 d

Z d s

9

Z u l n

F

U w

C k

4

B f

A

B l e g

D

T q g

C

3 o

A g

0 f w

D

F

7

B m

/

F k v

B j v x s e i d c

0 o

Z

0

7

A n z

I

+ f w

A

H l

J o

E

<

/ l a t e x i t

>

HG2

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

S

S

G g

3

6

T

S

X

Q r

T k

D p

S

U z v a

Q b

D

+

2

M

0

=

"

>

A

A

A

C

B

3 i c b

V

D

L

S s

N

A

F

J

3

4 r

P

U

V d

S n

I

Y

B

F c l a

S

U

6 r

L g w i

4 r

2

A c

0

I

U w m k

3 b o

Z

B

J m

J k

I

J

2 b n x

V

9 y

4

U

M

S t v

+

D

O v

3

H

S

Z q

G t

F

4

Y n

H

M v

9

9 z j

J

4 x

K

Z

V n f x t r

6 x u b

W d m

W n u r u

3 f

3

B o

H h

3

3

Z

Z w

K

T

H o

4

Z r

E

Y

+ k g

S

R j n p

K a o

Y

G

S a

C o

M h n

Z

O

B

P b w p

9

8

E

C

E p

D

G

/

V

7

O

E u

B

E a c x p

S j

J

S m

P

P

P

M

8

W

M

W y

F m k v

6 y

T e k

T

I

T

X

B i

G

W

3 u d f

I

P b

N m

1 a

1 w

V

V g l

6

A

G y u p

6 p c

T x

D i

N

C

F e

Y

I

S l

H t p

U o

N

0

N

C

U c x

I

X n

V

S

S

R

K

E p

2 h

M

R h p y

F

B

H p

Z v

M

7 c n i h m

Q

C

G s d

C

P

K z h n f

0

9 k

K

J

K

F

V d

1

Z u

J

T

L

W k

H

+ p

4

1

S

F

V

6

7

G e

V

J q g j

H i

0

V h y q

C

K

Y

R

E

K

D

K g g

W

L

G

Z

B g g

L q r

1

C

P

E

E

C

Y a

W j q

+ o

Q

7

O

W

T

V

0

G

/

U b d b

9 d

Z d s

9

Z u l n

F

U w

C k

4

B f

A

B l e g

D

T q g

C

3 o

A g

0 f w

D

F

7

B m

/

F k v

B j v x s e i d c

0 o

Z

0

7

A n z

I

+ f w

A

H l

J o

E

<

/ l a t e x i t

>

HG2

HG1 HG1

GED(G1, G2) GED(G1, G2)

IoU = #inter(Npred, Ntrue)

#union(Npred, Ntrue) IoU = #inter(Npred, Ntrue)

#union(Npred, Ntrue)

HG1 HG1

## 2 Subcircuit

Detection 1. Circuit Classification 3. GED Prediction

**Figure 4.** The illustration of the downstream tasks: (1) Analog circuit classification; (2) Analog subcircuit detection; (3) Analog GED preidction.

KCL Loss. Combine the positives and negatives inspired by KCL, we follow the contrastive framework in (You et al. 2020; Zhu et al. 2020) to derive the KCL Loss, the training objective for (I∆, I∆′) with N = d × (d −1) pairs is:

L = −log esim(I∆,I∆′)/τ PN j=1 esim(I∆, ˆI∆′)/τ, where τ is a temperature hyperparameter.

## Experiments

We conduct experiments to address the following issues: (1) How does KCLNet compare to general GNNs and graph pretrained methods in terms of performance? (2) How effective is the proposed KCL Loss? (3) What is the impact of each KCLNet module on its overall performance?

## Experimental Setup

Dataset and Downstream Tasks. We employ the analog circuits dataset ANALOG in (Tu et al. 2025) generated using the analog circuit topology synthesis framework (Zhao and Zhang 2022). The generated circuits contain fundamental topologies ranging from basic building blocks to complex industrial-scale systems. The details of the used analog circuit topologies are in Appendix A.2.

In this paper, we introduce three downstream applications as shown in Figure 4 to verify our pre-trained circuit embedding. Three datasets for sub-tasks were developed for analog circuit-related tasks. For analog circuit classification, the ANALOG dataset was expanded by adjusting sizing parameters, resulting in ANALOG-CLS-428k; for analog subcircuit detection, following Kunal et al.’s (Kunal et al. 2020) framework, base circuit categories were classified via manual annotation, creating ANALOG-DET-242k with 242,320 samples; for analog graph edit distance (GED) prediction, ANALOG-GED-194k was generated via mutations on existing data. All datasets emphasize balanced splits and proportional representation of circuit characteristics to ensure robust model evaluation. The details of the definition of subtasks and the dataset partition scheme are provided in Appendix A.2. Evaluation Metrics. For the analog circuit classification task, we adopt standard classification metrics for evaluation: top-k accuracy (Acc@1, Acc@2, Acc@5), True Positive Rate (Recall), and F1 Score. For the analog subcircuit detection task, we use common evaluation metrics in detection tasks, including mAP (mean Average Precision), Recall, F1 Score, and IoU (Intersection over Union). We utilize common evaluation metrics in regression tasks for the graph edit distance prediction task, including MAE and MSE. The reported results are the average of the best results in 5 runs from different random seeds. Baseline Methods. The baseline methods we compare include two categories: (1) mainstream GNN encoders without pretraining; (2) mainstream GNN representation learning method combined with different GNN Encoders. For the mainstream GNN Encoders, we adopted the following commonly used GNN frameworks as our analog circuits encoder: GCN (Kipf and Welling 2017), GAT (Velickovic et al. 2018), GIN (Xu et al. 2019), Graphsage (Hamilton, Ying, and Leskovec 2017), GAT v2 (Brody, Alon, and Yahav 2022). For mainstream GNN pretraining methods, we utilized the general graph pre-training method named GraphCL (You et al. 2020), combined with different graph encoders as comparison methods. All methods are compared based on the same hyperparameter. The baseline methods’ implementation details are provided in Appendix A.4.

Experimental Results

Analog Circuits Classification. As shown in Table 2, we comprehensively compared the experimental results of various methods for the analog circuit classification task. Specifically, KCLNet achieves the highest accuracy among all baseline models, showcasing its superior representation ability for downstream classification. Compared to the pretrained graph model GraphCLGCN, our method brings about a 39.76% and 51.19% improvement in Acc@1 and F1 Score, respectively. When compared to the best performing methods, GraphCLGIN and GIN, it offers a 5.56% and 20.77% improvement in Acc@1 and F1 Score, respectively. These results confirm that KCLNet has better representation compared with existing approaches in the analog circuit classification task. Analog Subcircuits Detection. As shown in Table 3,

<!-- Page 6 -->

## Method

Acc@1↑ Acc@2↑ Acc@5↑ Recall↑ F1 Score↑

Base Models

GCN 0.561±0.061 0.784±0.040 0.913±0.014 0.405±0.087 0.404±0.121 GAT 0.479±0.105 0.681±0.148 0.794±0.118 0.327±0.060 0.275±0.069 GATv2 0.498±0.100 0.694±0.139 0.799±0.133 0.322±0.051 0.270±0.075 GIN 0.786±0.077 0.883±0.058 0.931±0.039 0.648±0.101 0.669±0.118 SAGE 0.774±0.019 0.927±0.023 0.938±0.004 0.626±0.028 0.638±0.055 GraphCL Variants

GraphCLGCN 0.679±0.131 0.795±0.120 0.910±0.063 0.558±0.150 0.564±0.186 GraphCLGAT 0.537±0.108 0.794±0.046 0.919±0.046 0.408±0.135 0.368±0.173 GraphCLGATv2 0.493±0.112 0.650±0.075 0.809±0.112 0.401±0.104 0.357±0.148 GraphCLGIN 0.875±0.083 0.943±0.009 0.950±0.006 0.741±0.083 0.759±0.102 GraphCLSAGE 0.899±0.013 0.958±0.001 0.962±0.001 0.726±0.024 0.744±0.036 Our Methods

KCLNet 0.949±0.004 0.958±0.005 0.964±0.004 0.829±0.015 0.853±0.011 w.o PosKCL 0.938±0.005 0.942±0.006 0.944±0.003 0.794±0.013 0.830±0.012 w.o NegKCL 0.939±0.004 0.946±0.010 0.949±0.010 0.801±0.015 0.682±0.335 w.o Pos+NegKCL 0.938±0.003 0.941±0.005 0.944±0.002 0.794±0.009 0.822±0.018

**Table 2.** Performance comparison on analog circuit classification. Top performers in each category are bold.

## Method

mAP↑ Recall↑ F1 Score↑ AUC↑ IoU↑

Base Models

GCN 0.368±0.002 0.260±0.004 0.225±0.003 0.796±0.002 0.144±0.002 GAT 0.383±0.013 0.290±0.033 0.262±0.038 0.808±0.012 0.170±0.032 GATv2 0.382±0.017 0.303±0.059 0.279±0.072 0.807±0.022 0.183±0.051 GIN 0.553±0.029 0.667±0.019 0.695±0.020 0.932±0.005 0.565±0.021 SAGE 0.355±0.004 0.255±0.002 0.211±0.002 0.785±0.001 0.133±0.001 GraphCL Variants

GraphCLGCN 0.363±0.014 0.222±0.005 0.181±0.008 0.762±0.008 0.115±0.005 GraphCLGAT 0.371±0.016 0.231±0.027 0.193±0.032 0.757±0.032 0.121±0.023 GraphCLGATv2 0.389±0.010 0.271±0.096 0.236±0.105 0.779±0.052 0.154±0.077 GraphCLGIN 0.434±0.033 0.539±0.076 0.539±0.090 0.898±0.017 0.420±0.070 GraphCLSAGE 0.361±0.016 0.253±0.015 0.213±0.013 0.776±0.014 0.134±0.009 Our Methods

KCLNet 0.622±0.002 0.721±0.002 0.753±0.002 0.949±0.000 0.634±0.003 w.o PosKCL 0.374±0.027 0.399±0.098 0.381±0.117 0.845±0.042 0.273±0.096 w.o NegKCL 0.602±0.039 0.706±0.040 0.736±0.046 0.944±0.010 0.615±0.053 w.o Pos+NegKCL 0.561±0.035 0.654±0.038 0.674±0.045 0.931±0.010 0.545±0.051

**Table 3.** Performance comparison on subcircuit detection task.

KCLNet also outperforms other methods in the subcircuit detection task. Compared to the best performing methods, GraphCLGIN and GIN, KCLNet achieves improvements of up to 43.36%, 33.80%, 39.61%, 5.67%, and 51.02% in the mAP, Recall, F1 Score, AUC, and IoU metrics, respectively. It can be observed that the general-purpose graph pretraining algorithm GraphCLGIN fails to enhance the model’s performance on downstream circuit-related tasks compared to GIN. The key issue is that these generic pre-training tasks often fail to capture equivalence in circuit diagrams. These improvements in metrics further indicate that KCLNet’s representation learning capabilities enhance the detection accuracy, recall, and robustness.

Graph-Edit-Distance Prediction. As shown in Figure 5, the proposed contrastive learning framework reduces up to 3.8% MAE compared to vanilla GNNs. Additionally, compared with methods that have experienced improvement through general pretraining, such as GraphCLGIN, KCLNet

<!-- Page 7 -->

0.96

0.97

0.98

0.99

Norm. MAE↓

Base Models GraphCL Ours 0.95

0.96

0.97

0.98

Norm. MSE↓

**Figure 5.** The averaged and normalized performance comparison on the analog circuit GED prediction task.

0.93 0.94 0.95 w.o KCL w.o KCLNEG w.o KCLPOS

KCLNet

ACC@1 ↑

(a)

0.36 0.50 0.64 w.o KCL w.o KCLNEG w.o KCLPOS

KCLNet mAP↑

(b)

**Figure 6.** Comparison between KCLNet with different variants of KCL Loss.

maintains a similar improvement with up to 1.6%. It can also be observed that general graph pretraining methods do not necessarily guarantee an improvement in the performance of GCN, which can be seen from the close MAE and MSE values.

Ablation Studies KCL-Inspired Loss at Work. A notable advantage of KCLNet lies in its ability to generate positive embeddings in the analog circuits from an electrical perspective. To verify this, Figure 6a and Figure 6b show performance comparisons of different KCL Loss variants. The w.o KCLPOS uses general graph-augmented positive samples to maximize alignment, w.o KCLNEG replaces KCL-based negatives with different graph samples in the same batch, and w.o KCL removes KCL Loss entirely, relying solely on asynchronous message passing. The results show that KCL Loss is crucial for final performance, with positive embeddings being the most important. Asynchronous Message Passing Scheme. In Table 4, we compare the performance differences between the proposed

20 65 110 155 200 0.400

0.600

0.800

Epochs

F1-Score(%)↑

GraphCLGIN GraphCLGCN

KCLNet

**Figure 7.** The pre-training epochs impact of KCLNet on classification, which outperforms general graph pretraining at earlier epochs.

Classification Detection Acc@1↑ F1-Score↑ mAP↑ IoU↑

GCN 0.561±0.061 0.404±0.121 0.368±0.002 0.144±0.002 GAT 0.496±0.127 0.306±0.101 0.383±0.013 0.170±0.032 GATv2 0.498±0.100 0.270±0.075 0.382±0.017 0.183±0.051 GIN 0.786±0.077 0.669±0.118 0.553±0.029 0.565±0.021 SAGE 0.774±0.019 0.638±0.055 0.355±0.004 0.133±0.001 AGNN 0.938±0.003 0.822±0.018 0.561±0.035 0.545±0.051

**Table 4.** Performance comparison between synchronous and asynchronous message passing (AGNN).

AGNN and synchronous GNN. AGNN outperforms the best synchronous model, GIN, by 19.6% and 22.9% in Acc@1 and F1-score in the cls task. It also improves the mAP by 1.4% in the det task, surpassing all other GNN models. These results confirm the effectiveness of electricallysimulated asynchronous message passing. The Effect of Training Epochs in KCLNet. As shown in Figure 7, KCLNet surpasses GraphCL pretrained methods for different epochs (GraphCLGIN and GraphCLGCN) starting from 20 epochs, showing strong early performance. Unlike other frameworks that rely on augmentation for positive samples with more pretraining epochs needed, KCLNet uses KCL’s physical prior knowledge to generate positive embeddings without augmentation, reducing the needed pretraining epochs.

## Conclusion

In this work, we use an electrically-simulated asynchronous graph neural network as the analog circuit encoder, leveraging Kirchhoff’s current law to aid representation learning by enforcing current embedding conservation across depths. Experiments show the model learns vital physical priors, significantly enhancing generalization across analog sub-tasks. We propose three future directions: 1) modeling Kirchhoff’s voltage law from a voltage perspective; 2) exploring better encoders like graph transformers; 3) incorporating additional inputs like SPICE codes to assist learning.

## Acknowledgments

This work is supported by The National Key Research and Development Program of China (No. 2023YFB4402900), The National Natural Science Foundation of China (No. 92573108 and No. 62304197), and The Research Grants Council of Hong Kong SAR (No. CUHK14211824 and No. CUHK14201624).

<!-- Page 8 -->

## References

Athavale, P. 2018. Kirchoff’s current law and Kirchoff’s voltage law. Johns Hopkins University, Retrived, 6. Brody, S.; Alon, U.; and Yahav, E. 2022. How Attentive are Graph Attention Networks? In Proc. ICLR. Bruna, J.; Zaremba, W.; Szlam, A.; and LeCun, Y. 2014. Spectral Networks and Locally Connected Networks on Graphs. In Proc. ICLR. Chen, H.; Zhu, K.; Liu, M.; Tang, X.; Sun, N.; and Pan, D. Z. 2021. Universal symmetry constraint extraction for analog and mixed-signal circuits with graph neural networks. In Proc. DAC, 1243–1248. IEEE. Chen, T.; Kornblith, S.; Norouzi, M.; and Hinton, G. 2020. A simple framework for contrastive learning of visual representations. In Proc. ICML, 1597–1607. Defferrard, M.; Bresson, X.; and Vandergheynst, P. 2016. Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering. In Proc. NIPS. Dimo, P. 1975. Nodal analysis of power systems. International Scholarly Book Services, Inc., Forest Grove, OR. Dong, Z.; Cao, W.; Zhang, M.; Tao, D.; Chen, Y.; and Zhang, X. 2023. CktGNN: Circuit Graph Neural Network for Electronic Design Automation. In Proc. ICLR. Gao, X.; Deng, C.; Liu, M.; Zhang, Z.; Pan, D. Z.; and Lin, Y. 2021. Layout symmetry annotation for analog circuits with graph neural networks. In Proc. ASPDAC, 152–157. Gray, P. R.; Hurst, P. J.; Lewis, S. H.; and Meyer, R. G. 2009. Analysis and design of analog integrated circuits. John Wiley & Sons. Hamilton, W. L. 2020. Graph Representation Learning. Synthesis Lectures on Artificial Intelligence and Machine Learning, 14(3): 1–159. Hamilton, W. L.; Ying, Z.; and Leskovec, J. 2017. Inductive Representation Learning on Large Graphs. In Proc. NIPS. He, K.; Fan, H.; Wu, Y.; Xie, S.; and Girshick, R. 2020. Momentum contrast for unsupervised visual representation learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 9729–9738. Hou, Y.; Zhang, J.; Chen, H.; Zhou, M.; Yu, F.; Fan, H.; and Yang, Y. 2024. CktGen: Specification-Conditioned Analog Circuit Generation. arXiv preprint arXiv:2410.00995. J´onsson, B. 1988. Relation algebras and Schr¨oder categories. Discrete Mathematics, 70(1): 27–45. Kahn, A. B. 1962. Topological sorting of large networks. Communications of the ACM, 5(11): 558–562. Kipf, T. N.; and Welling, M. 2017. Semi-Supervised Classification with Graph Convolutional Networks. In Proc. ICLR. Kunal, K.; Dhar, T.; Madhusudan, M.; Poojary, J.; Sharma, A.; Xu, W.; Burns, S. M.; Hu, J.; Harjani, R.; and Sapatnekar, S. S. 2020. GANA: Graph convolutional network based automated netlist annotation for analog circuits. In Proc. DATE, 55–60. IEEE. Li, M.; Khan, S.; Shi, Z.; Wang, N.; Yu, H.; and Xu, Q. 2022. Deepgate: Learning neural representations of logic gates. In Proc. DAC, 667–672.

Pang, B.; Zhang, Y.; Li, Y.; Cai, J.; and Lu, C. 2022. Unsupervised visual representation learning by synchronous momentum grouping. In Proc. ECCV, 265–282. Springer. Paul, C. R. 2001. Fundamentals of electric circuit analysis. John Wiley & Sons. Ren, H.; Kokai, G. F.; Turner, W. J.; and Ku, T.-S. 2020. ParaGraph: Layout parasitics and device parameter prediction using graph neural networks. In Proc. DAC, 1–6. IEEE. Rewie´nski, M. 2011. A perspective on fast-SPICE simulation technology. In Simulation and Verification of Electronic and Biological Systems, 23–42. Springer. Sansen, W. M. 2007. Analog design essentials, volume 859. Springer Science & Business Media. Settaluri, K.; Haj-Ali, A.; Huang, Q.; Hakhamaneshi, K.; and Nikolic, B. 2020. Autockt: Deep reinforcement learning of analog circuit designs. In Proc. DATE, 490–495. IEEE. Shi, Z.; Pan, H.; Khan, S.; Li, M.; Liu, Y.; Huang, J.; Zhen, H.-L.; Yuan, M.; Chu, Z.; and Xu, Q. 2023. Deepgate2: Functionality-aware circuit representation learning. In Proc. ICCAD, 1–9. IEEE. Shi, Z.; Zheng, Z.; Khan, S.; Zhong, J.; Li, M.; and Xu, Q. 2024. Deepgate3: Towards scalable circuit representation learning. arXiv preprint arXiv:2407.11095. Tu, J.; Li, Y.; Li, P.; Xu, P.; Zhang, Q.; Wan, S.; Sun, Y.; Yu, B.; and Chen, T. 2025. SMART: Graph Learning-Boosted Subcircuit Matching for Large-Scale Analog Circuits. IEEE TCAD. Velickovic, P.; Cucurull, G.; Casanova, A.; Romero, A.; Li`o, P.; and Bengio, Y. 2018. Graph Attention Networks. In Proc. ICLR. Wang, H.; Wang, K.; Yang, J.; Shen, L.; Sun, N.; Lee, H.-S.; and Han, S. 2020. GCN-RL circuit designer: Transferable transistor sizing with graph neural networks and reinforcement learning. In Proc. DAC, 1–6. IEEE. Wang, Z.; Bai, C.; He, Z.; Zhang, G.; Xu, Q.; Ho, T.-Y.; Huang, Y.; and Yu, B. 2024. Fgnn2: A powerful pre-training framework for learning the logic functionality of circuits. IEEE TCAD. Wedepohl, L.; and Jackson, L. 2002. Modified nodal analysis: an essential addition to electrical circuit theory and analysis. Engineering science and education journal, 11(3): 84– 92. Wu, H.; Zheng, H.; Pu, Y.; and Yu, B. 2025. Circuit Representation Learning with Masked Gate Modeling and Verilog-AIG Alignment. Proc. ICLR. Wu, Z.; Pan, S.; Chen, F.; Long, G.; Zhang, C.; and Yu, P. S. 2021. A Comprehensive Survey on Graph Neural Networks. IEEE Transactions on Neural Networks and Learning Systems, 32(1): 4–24. Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2019. How Powerful are Graph Neural Networks? In Proc. ICML. Xu, P.; Chen, G.; Zhu, K.; Chen, T.; Ho, T.-Y.; and Yu, B. 2024a. Performance-driven analog routing via heterogeneous 3dgnn and potential relaxation. In Proc. DAC, 1–6.

<!-- Page 9 -->

Xu, P.; Li, J.; Ho, T.-Y.; Yu, B.; and Zhu, K. 2024b. Performance-driven analog layout automation: Current status and future directions. In Proc. ASPDAC, 679–685. Xu, P.; Tu, J.; Chen, G.; Zhu, K.; Chen, T.; Ho, T.-Y.; and Yu, B. 2025. PARoute2: Enhanced Analog Routing via Performance-Drive Guidance Generation. IEEE TCAD. You, Y.; Chen, T.; Sui, Y.; Chen, T.; Wang, Z.; and Shen, Y. 2020. Graph contrastive learning with augmentations. Proc. NIPS, 33: 5812–5823. Zeng, G. L.; and Zeng, M. 2021. Kirchhoff’s Current Law (KCL). Electric Circuits: A Concise, Conceptual Tutorial, 31–35. Zhao, Z.; and Zhang, L. 2022. Analog integrated circuit topology synthesis with deep reinforcement learning. IEEE TCAD, 41(12): 5138–5151. Zheng, Z.; Huang, S.; Zhong, J.; Shi, Z.; Dai, G.; Xu, N.; and Xu, Q. 2025. DeepGate4: Efficient and Effective Representation Learning for Circuit Design at Scale. In Proc. ICLR. Zhu, K.; Chen, H.; Turner, W. J.; Kokai, G. F.; Wei, P.-H.; Pan, D. Z.; and Ren, H. 2022. Tag: Learning circuit spatial embedding from layouts. In Proc. ICCAD, 1–9. Zhu, Y.; Xu, Y.; Yu, F.; Liu, Q.; Wu, S.; and Wang, L. 2020. Deep Graph Contrastive Representation Learning. In ICML Workshop on Graph Representation Learning and Beyond. Zhu, Z.; Chen, Z.; and Yang, S. 2024. A Fast SIE Solver With Cut Set Analysis and Terminals as Supernodes for Interconnects. IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 43(9): 2730–2740.
