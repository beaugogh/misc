---
title: "A Causal Target for Learning to Defer Under Hidden Confounding"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39493
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39493/43454
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# A Causal Target for Learning to Defer Under Hidden Confounding

<!-- Page 1 -->

A Causal Target for Learning to Defer Under Hidden Confounding

Yanmin Li1 *, Lihua Liu1 *, Xin Wang2, Zhilong Mao1, Jibing Wu1 †, Weidong Bao1,

1Laboratory for Big Data and Decision, National University of Defense Technology 2University of Science and Technology of China yanminli@nudt.edu.cn, lihualiu@nudt.edu.cn, wz520@mail.ustc.edu.cn, {mzl02, wujibing, wdbao}@nudt.edu.cn

## Abstract

Learning decision policies from confounded observational data is a challenging task in causal inference, as unobserved confounders can lead to biased or suboptimal actions when relying solely on machine learning models. A synergistic approach is learning to defer, which decides when to act itself and when to defer to a human expert with access to unobserved information. However, constructing the learning target, which deﬁnes the probability of choosing each action or deferral, remains a core challenge. To address this, we propose causal-target-based learning to defer (CTLD) framework, where the causal target is constructed from sharp bounds on potential outcomes. Speciﬁcally, the degree of overlap between these bounds determines the probability of deferral, while their relative positions and widths deﬁne the probabilities over actions. CTLD aligns model predictions with this causal target to make probabilistic decisions over actions and deferral. We present comprehensive theoretical guarantees for the learned policy and demonstrate the effectiveness of CTLD on synthetic and semi-synthetic datasets.

Code — https://github.com/JustinLiam/CTLD

## Introduction

Causal policy learning, which aims to optimize decisionmaking from observational data, is critical in high-stakes domains such as healthcare, ﬁnance, and social services (Kallus 2018; Athey and Wager 2021). However, a fundamental challenge in leveraging such data is hidden confounding, which induces structural bias in causal effect estimation, thereby compromising the validity of learned policies and leading to suboptimal or even detrimental decisionmaking (Imbens and Rubin 2015). For example, in healthcare, unrecorded lifestyle or psychological factors may in- ﬂuence both treatment choices and outcomes, thereby serving as unobserved confounders that distort the data-driven policy learning.

Recent studies on confounding-robust policy learning, such as those based on the minimax regret framework (Kallus and Zhou 2018, 2021), often adopt a worst-case

*These authors contributed equally. †Jibing Wu is the corresponding author. Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

!!

< l a t e x i t s h a

_ b a s e

6

4

=

" g g

6

2

D

+

S d

N v

W

Y

7

S

3 o

Y

Z w

3

/ h s

6

4 y o

=

"

>

A

A

A

C

E

3 i c b

V

D

L

S s

N

A

F

L

3 x

W e

O r

6 t

L

N

Y

C m

4

K o l

I d

V l w

4

7

I

F

0 x b a

U

C a

T

S

T t

0

M g k z

E

6

G

E f o

F b

+ z

X u x

K

0 f

4

M c

I

T t s s

+ v

D

A w

O

G c e

+

/ c e

4

K

U

M

6

U d

5

8 f a

2 d

3 b

P z g s

H d n

H

J

6 d n

5

+

W

L y

7

Z

K

M k m o

R x

K e y

G

6

A

F e

V

M

U

E

8 z z

W k

3 l

R

T

H

A a e d

Y

P w

0

9 z u v

V

C q

W i

B c

9

S a k f

4

6

F g

E

S

N

Y

G

6 n l

D c o

V p

+

Y s g

L a

J

W

5

A

K

F

G g

O y r

/

9

M

C

F

Z

T

I

U m

H

C v

V c

5

U

+ z m

W m h

F

O p

3

Y

/

U z

T

F

Z

I y

H t

G e o w

D

F

V f r

5

Y d

I q q

R g l

R l

E j z h

E

Y

L d b

U j x

7

F

S k z g w l

T

H

W

I

7

X p z c

X

/ v

F

6 m o

0 c

/

Z y

L

N

N

B

V k

+

V

G

U c a

Q

T

N

L

8 a h

U x

S o v l k b

W

D

K

5 l t

M

7 e q q

S

J g

0 d

4

R

G

D

R k m k p m z

E

B l h i

Y k

2

M d o m

L

3 c z n

W

3

S v q u

5

9

V q

9 d

V

9 p o

C

K

5

E l z

D

D d y

C

C w

/

Q g

G d o g g c

E

K

L z

B

O

8 y s m f

V h f

V p f y

9

I d q

+ i

5 g j

V

Y

3

3

9 x d

J

5

M

<

/ l a t e x i t

>

U

Unobserved confounders

< l a t e x i t s h a

_ b a s e

6

4

=

"

Q

4

M

0

L

G u v

+ y

2

T

B

C r

L x

W g

T

+

L e l

M

M

=

"

>

A

A

A

C

E

3 i c b

V

D

L

S s

N

A

F

L

3 x

W e

O r

6 t

L

N

Y

C m

4

K o l

I d

V l w

4

7

I

F

+

4

A

2 l

M l k

0 g

6 d

T

M

L

M

R

C i h

X

+

D

W f o

0

7 c e s

H

+

D

G

C k z a

L

P j w w c

D j n

3 j v

3

H j

/ h

T

G n

H

+ b

F

2 d v f

2

D w

5

L

R

/ b x y e n

Z e f n i s q

P i

V

B

L a

J j

G

P

Z c

/

H i n

I m a

F s z z

W k v k

R

R

H

P q d d f

/

K

U

+

9

X

K h

W

L x

Y u e

J t

S

L

8

E i w k

B

G s j d

T q

D c s

V p

+

Y s g

L a

J

W

5

A

K

F

G g

O y

7

+

D

I

C

Z p

R

I

U m

H

C v

V d

5

E e x m

W m h

F

O

Z

/

Y g

V

T

T

B

Z

I

J

H t

G

+ o w

B

F

V

X r

Z

Y d

I a q

R g l

Q

G

E v z h

E

Y

L d b

U j w

5

F

S

0

8 g

3 l

R

H

W

Y

7

X p

5 e

J

/

X j

/

V

4 a

O

X

M

Z

G k m g q y

/

C h

M

O d

I x y q

9

G

A

Z

O

U a

D

5 d

G

5 i w f

I u

Z

X

V

0

V

C

Z

P m j s

C o

A c

N

E

M n

M

W

I m

M s

M d

E m

R t v k

5

W

6 m s

0

0

6 d z

W

3

X q u

3

7 i s

N

V

C

R

X g m u

4 g

V t w

4

Q

E a

8

A x

N a

A

M

B

C m

/ w

D n

N r b n

Y n

9 b

X s n

T

H

K n q u

Y

A

3

W

9 x

9

2 g

Z

5

P

<

/ l a t e x i t

>

X

Y

!

Causal policy learning Without human deferral

!

"

"

"

L2D

" Human expert

Learning to defer

Confounders

Action Action

Confounders

!

!

!

!

Action

< l a t e x i t s h a

_ b a s e

6

4

=

"

Z

G

Y x

S

J

F

J

G a o

I

U w n

X c

X

W

4 l b f

B w s

=

"

>

A

A

A

C

E

3 i c b

V

D

L

S s

N

A

F

L

2 p r p f

V

Z d u h p a

C q

5

K

I

V

J c

F

N y

5 b s

A

9 o

Q

5 l

M

J u

3

Q y

S

T

M

T

I

Q

S

+ g

V u

7 d e

4

E

7 d

+ g

B

8 j

O

G m z

6

M

M

D

A

4 d z

7 r z

7

/

F i z p

S

2

7

R

+ r s

L d

/ c

H h

U

P

C

6 d n

J

6 d

X

5

Q v r

7 o q

S i

S h

H

R

L x

S

P

Y

9 r

C h n g n

Y

0

0

5 z

2

Y

0 l x

6

H

H a

8

6

Z

P m d

9

7 p

V

K x

S

L z o

W

U z d

E

I

8

F

C x j

B

2 k h t

P

C p

X

7 b q

9

B

N o l

T k

6 q k

K

M

K v

8

O

/

Y g k

I

R

W a c

K z

U w

L

F j

7 a

Z

Y a k

Y

4 n

Z e

G i a

I x

J l

M

8 p g

N

D

B

Q

6 p c t

P l o n

N

U

M

4 q

P g k i a

J z

R a q u s d

K

Q

6

V m o

W e q

Q y x n q h t

L x

P

/

8 w a

J

D h

7 d l

I k

4

0

V

S

Q

U d

B w p

G

O

U

H

Y

8 p m k

R

P

P

Z x s

C

Y

Z

V v

M

S

7

V k

T

B p

7 v

C

N

6 j

N

M

J

D

N n

I

T

L

B

E h

N t

Y i y

Z v

J z t d

H

Z

J

9

6

7 u

N

O q

N

9 n

2

W c m

T

K

8

I

N

V

O

A

W

H

H i

A

J j x

D

C z p

A g

M

I b v

M

P

C

W l g f q f t

S o t

W

H n

P

N

W z

A

+ v

4

D h k

K e

W g

=

=

<

/ l a t e x i t

> a

**Figure 1.** Overview of causal policy learning problem setup and two learning paradigms. Policies without deferral may yield suboptimal actions. The learning to defer (L2D) enables the model to defer to a human expert, thereby mitigating confounding effects and making better action decisions.

perspective, resulting in overly conservative treatments with limited utility. To address this limitation, we draw inspiration from the emerging paradigm of “Learning to Defer” (L2D) (Mozannar and Sontag 2020), where a model is trained not only to act autonomously but also to defer to a human expert when facing high causal uncertainty. This strategy may alleviate the pitfalls of overly conservative policies, thus potentially achieving a better balance between robustness and effectiveness, as illustrated in Figure 1.

The L2D paradigm can be viewed as learning a classiﬁer with the option of deferring to an expert. However, the observational data only reﬂects the covariates, action (e.g., treatment 0 or 1) and corresponding outcome, without explicit labels for when to defer. Thus, rather than learning to imitate deferrals, the model must infer when to defer by quantifying its uncertainty about the best course of action under hidden confounding. The core challenge, therefore, is to construct a learning target that serves as a principled proxy for the unknowable optimal decision, guiding the model on when to act versus when to defer.

Prior work addresses this by designing a cost-sensitive target which measures the penalty among actions and deferral (Ghoummaid and Shalit 2024). A key weakness of this approach is that its deferral cost directly incorporates the raw observed outcome for each sample, which makes the target sensitive to outcome stochasticity and may limit the learned policy’s reliability. Furthermore, this framework triggers deferral whenever the deferral penalty is lower than the penalties for taking actions. This trigger is based on a

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

23248

<!-- Page 2 -->

simple cost comparison, rather than a direct quantiﬁcation of the causal uncertainty between actions. These limitations highlight a clear research gap in designing a robust learning target based on a direct quantiﬁcation of causal uncertainty.

To address this gap, we propose the causal-target-based learning to defer (CTLD) framework to learn deferral policies. In the presence of hidden confounding, the true causal effects of actions are not identiﬁable, but they can be tightly bounded by sharp bounds1. By leveraging these bounds, CTLD constructs a probabilistic learning target designed to capture the uncertainty under hidden confounding. Speciﬁcally, the deferral probability is determined by the degree of overlap between the bounds, while the action probabilities are determined by the estimated treatment effect, which is in turn tempered by the overall uncertainty captured by the total width of the bounds. A model is then trained to match this target using a tailored loss function and an asymmetric softmax parameterization, which is suitable for the distinct nature of action versus deferral decisions, thereby learning a mapping from covariates to a probability distribution over actions and deferral.

Our main contributions are as follows: • We introduce a CTLD framework that leverages sharp causal bounds to construct the stable, probabilistic causal target, enabling robust action and deferral decisions under hidden confounding. • We establish theoretical guarantees for CTLD, including a regret-transfer bound that links the training loss to the performance gap between the learned policy and the optimal policy, while a generalization bound ensuring that the learned policy remains reliable on unseen data. • We conduct extensive experiments on both synthetic and semi-synthetic datasets, demonstrating that CTLD outperforms existing baselines in both policy values and deferral behavior.

## Related Work

Causal Policy Learning. Learning decision policies from observational data is fundamentally a causal inference challenge (Imbens and Rubin 2015). A core difﬁculty is that unobserved confounders, which are factors inﬂuencing both past actions and outcomes, can create spurious correlations, making it difﬁcult to discern which actions are genuinely effective. To directly confront this problem, the ﬁeld of causal policy learning seeks to ﬁnd not just optimal, but “robust” policies, whose performance is guaranteed to be safe even under worst-case assumptions about the confounding.

Broadly, two main approaches have emerged. Early “weight-centric” method sought robustness through data reweighting, exempliﬁed by minimax regret frameworks using the Inverse Propensity Weighting (IPW) estimator (Kallus and Zhou 2018, 2021). The statistical instability of this strategy, particularly its tendency to assign extremely large importance to a few rare observations, spurred the evolution

1Sharp bounds refer to the tightest possible upper and lower limits on potential outcomes that are consistent with the observed data and the assumed level of hidden confounding (Ho and Rosen 2015).

towards a more direct, “value-centric” perspective. This latter approach bypasses data re-weighting and instead asks, “Given the potential for confounding, what are the best-case and worst-case outcomes for any given action?”, leading to more stable methods that derive sharp bounds directly on potential outcomes (Dorn and Guo 2023; Hess et al. 2025).

Learning to Defer Paradigm. A promising avenue for mitigating risk under uncertainty is to design systems that can defer to a human expert (Bondi et al. 2022; Hemmer et al. 2023; Ruggieri and Pugnana 2025). This principle, known as “learning to defer” (L2D), has been systematically established in supervised learning, allowing a model to abstain on difﬁcult instances and pass them to an expert, thereby improving overall reliability (Mozannar et al. 2023; Tailor et al. 2024). The established approach for training such systems reduces the L2D problem to a well-understood, cost-sensitive classiﬁcation task using consistent surrogate losses (Mozannar and Sontag 2020). These developments provides a strong, principled foundation for building systems that can intelligently manage the trade-off between autonomous action and expert referral.

However, applying the L2D to causal policy learning introduces a fundamental challenge not present in supervised learning: the absence of ground-truth labels for counterfactual outcomes. To overcome this lack of direct supervision, all methods must rely on a set of assumptions to estimate causal effects from observational data. To make the problem tractable, pioneering works often operate under the assumption of unconfoundedness (e.g., Leit˜ao et al. (2022); Gao et al. (2021)). This has led to the development of simpliﬁed systems that learn to route decisions between an AI and an expert, optimizing the team’s overall performance by leveraging their complementary strengths. This unconfoundedness assumption, while powerful, is untenable in many realworld applications, as unobserved confounders can lead to biased estimates and, consequently, unsafe policies.

Learning to Defer under Hidden Confounding. Recently, a few pioneering works have begun to tackle the challenging problem of learning a deferral policy in the presence of hidden confounding. These efforts can be broadly categorized into three main methodologies. The ﬁrst is direct interval estimation of the conditioal average treatment effect (CATE), an approach taken by (Jesson et al. 2021), who ﬁrst estimate a range of possible CATE values and then apply a simple rule, such as deferring if the estimated interval contains zero. A second methodology is the “weightcentric” approach, pioneered by (Gao and Yin 2025), who propose a minimax framework that optimizes a worst-case policy risk over an uncertainty set of importance weights. However, this method can suffer from high variance due to the instability of these weights. A third strategy is costsensitive classiﬁcation, as developed by (Ghoummaid and Shalit 2024), whose training target is prone to instability from its reliance on noisy outcomes and provides only an indirect proxy for causal uncertainty. These limitations across different methodologies highlight a clear research gap in designing a robust learning target based on a direct quantiﬁcation of causal uncertainty. A structured comparison of these

23249

<!-- Page 3 -->

approaches is provided in Appendix A.

Our Method Problem Setup We consider a dataset D = {Xi, Ai, Yi}N i=1, where for each unit i, Xi ∈X represents pre-treatment covariates, Ai ∈A is the treatment received, and Yi ∈R is the observed outcome. In this work, we focus on the binary treatment setting, where the treatment action is Ai ∈{0, 1}. Under the potential outcomes framework, Yi(0) and Yi(1) denote the two potential outcomes for unit i. A summary of key terms and notation is included in Appendix B for reference.

The traditional goal of policy learning is to ﬁnd a policy π: X →{0, 1} that maximizes the expected outcome, V (π) = E[Y (π(X))]. Reliably evaluating this value from observational data, depends on three core assumptions: the stable unit treatment value assumption (SUTVA), positivity, and unconfoundedness (Imbens and Rubin 2015). However, the Unconfoundedness assumption (i.e., {Y (0), Y (1)} ⊥⊥ A|X) is often the most challenging to satisfy in practice (Gao and Yin 2025; Hess et al. 2025).

The violation of unconfoundedness can lead to suboptimal and unreliable policies. To mitigate this risk, we adapt the L2D framework, a form of human-AI collaboration. The goal is to learn a deferral policy π: X →{0, 1, ⊥}, which maps covariates either to a speciﬁc treatment action or to the deferral action (⊥). The value of such a policy π is the expected outcome of the joint system:

V (π) = E h

I(π(X)̸ =⊥)Y (π(X))

+ I(π(X) =⊥)Y (A)

i (1)

where the system follows the AI’s decision π(X) if it does not defer, and the expert’s decision otherwise. Following Ghoummaid and Shalit (2024), we assume the historical data was generated by this same expert, and model the expert’s action upon deferral as the historically observed action.

Our central problem is to learn an optimal policy π∗= arg maxπ V (π) in the presence of hidden confounding. To formalize this, we relax the unconfoundedness assumption by assuming the existence of an unobserved confounder U such that unconfoundedness holds conditioned on both X and U:

{Y (0), Y (1)} ⊥⊥A|X, U (2) To make this assumption operational, we quantify the strength of the confounding induced by U using the marginal sensitivity model (MSM) (Tan 2006), which bounds the degree to which U can inﬂuence treatment assignment given the estimable nominal propensity score e(x):= P(A = 1|X = x) versus the unidentiﬁable true propensity score e(x, u):= P(A = 1|X = x, U = u). Assumption 1 (MSM Assumption). The ratio between the true treatment odds, e(x, u)/(1 −e(x, u)), and the nominal treatment odds, e(x)/(1 −e(x)), is almost surely bounded by a factor Λ ≥1:

Λ−1 ≤ e(x, u) 1 −e(x, u)

e(x) 1 −e(x) ≤Λ.

Sharp bounds estimation

Causal target construction L2D policy Learning

0 1 AI action

! Defer to human x y

¯Q(x, 1)

¯Q(x, 0)

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

T x

Z

K b

5

O

8 a

W

L

W b

W u

2 o

1 n r b

6

O

W w

A

4

=

"

>

A

A

A

C

F

X i c b

V

D

L

S g

M x

F

L

1

T

X

V

8

V

V q

I l g

K r o

Z

U

S m f c

C

W

5

0 p

2 i r

U

E v

J

Z

N

I

2

N

P

M g y

Q h l

6

C e

4 t

V

/ j

T l w p r v

0

Y w

U w r

U q

0

H

A o d z k p t

7 j p

8

I r j

T

G

H

1

Z h

Y

X

F p e a

W

4 a q

+ t b

2 x u l b

Z m i p

O

J

W

U

N

G o t

Y v p

E

M c

E j

1 t

B c

C a b

S

E

Z

C

X

7

A b f

C a

+ z f

T

C o e

R

9 d

6 m

L

B

2

S

H o

R

7

J

K t

J

G u z j u

4

U y p j p

4 a x d

+ w i

7

L j

H r u e

5 q

O r g

C

X

5

I

G b

5 x

0

S l

9 g

U x

T

U

M

W a

S q

I

U q

0 q

T n

Q

7

I

1

J z

K t j

I v k s

V

S w g d k

B

5 r

G

R q

R k

K l

2

N l l

1 h

C p

G

C

V

A l u

Z

E

G k

U

2

R c

Z

C

Z

U a h r

6

5

G

R

L d

V

+

9

X

P z

P a

6

W

6

6

7

U z

H i

W p

Z h

G d f t

R

N

B d

I x y n

O j g

E t

G t

R j

+

G p j w f

I u

R

X

Z k

V

K

Z c m

R

2

D

U g

B

M q u

Y m

F a

J

9

I

Q r

U p

0 j

Z

9 z b

U z

T

5 p

H

T r

X u

1

C

9 r

5

Z

P

9

1 x x v

U

I

Q

9

O

I

B

D q

I

I

L

J

A

G

F

9

A

A

C j

1

4 g

E c

Y

W

2

P r y

X q

2

X q

Y l

F

6 z v t n f h

F

6 z

L

H

C o

/

M

=

<

/ l a t e x i t

>

I0

I1 softmax([s0

U, s1

U ])? Policy learning model g(x)

min L(¯ (g(x), ˜p(x))

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

5

4 z r m h w

M

E

X

K

Y y v f

Q

2

T k d j

4

Z

N

H

Y

=

"

>

A

A

A

C

N

X i c b

V

D

L

T g

I x

F

L

2

D

L

8

Q

X

6 l

I

X

V

U

I

C i

Z

I

Z

Y

9

C

N

C

Y k b l

5

D

I

I w

F

C

O p

0

C

D

Z

1

H

2 o

6

R

T

F j

7

N

W

7 l

J

/

Q

D

X

L g z b v

0

C

E z v

A

A t

C

T

N

D k

9 p

7 f t

O

X b

A m

V

S m

+

W

4 k

V l b

X

1 j e

S m

6 m t

7

Z d v f

T

+

Q

U

6 o

S

C

0

S n z u i

4 a

N

J e

X

M o

1

X

F

F

K e

N

Q

F

D s

2 p z

W

7 c

F t

7

N c f q

J

D

M

9

+

7

V

M

K

B t

F

/ c

8

1 m

U

E

K y

1

1

0 i e y

Y

6

I b

1

L

K x i

C q j

O

O

Z m

U f n c

1 s r

0 l n z

I

I

5

A f p

L r

B n

J w

A z l

T v q n

5 f g k d

K m n

C

M d

S

N i

0 z

U

O

0

I

C

8

U

I p

6

N

U

K

5

Q

0 w

G

S

A e

7

S p q

Y d d

K t v

R

J

M o

I

Z b

X i o

K

4 v

9

P

I

U m q j z

E x

F

2 p

R y

6 t j

7 p

Y t

W

X y

1

4 s

/ u c

1

Q

9

W

9 b k f

M

C

0

J

F

P

T

J

9 q

B t y p

H w

U

9

4

I c

J i h

R f

L h w

Y c

D i

X

4 x

S

2

X m

R

M

K

F z

O

F p

1

G

C a

C

6

V i

I

9

L

H

A

R

O m i

U

7 o v a

7 m d v

6

R

2

U b

C

K h

W

L l

M l

M

6 f o x

B k k

4 g l

P

I g

Q

V

X

U

I

I

7

K

E

M

V

C

D z

B

M

7 z

A

2

B g b

H

8 a n

8

T

U t

O

W

H

M

2 j

6

E

B

R j f v

7 p g r h g

=

<

/ l a t e x i t

> s0 = ¯Q(x, 0) −¯Q(x, 1)

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

Z j n c b t

U y e a

N

4

6

/

9

P

V o

5

7

6

C

K

W

M

Y

=

"

>

A

A

A

C

N

X i c b

V

D

L

T g

I x

F

L

2

D

L

8

Q

X

6 l

I

X

V

U

I

C i

Z

I

Z

Y

9

C

N

C

Y k b l

5

D

I

I w

F

C

O p

0

C

D

Z

1

H

2 o

6

R

T

F j

7

N

W

7 l

J

/

Q

D

X

L g z b v

0

C

E z v

A

A t

C

T

N

D k

9 p

7 f t

O

X b

A m

V

S m

+

W

4 k

V l b

X

1 j e

S m

6 m t

7

Z d v f

T

+

Q

U

6 o

S

C

0

S n z u i

4 a

N

J e

X

M o

1

X

F

F

K e

N

Q

F

D s

2 p z

W

7 c

F t

7

N c f q

J

D

M

9

+

7

V

M

K

B t

F

/ c

8

1 m

U

E

K y

1

1

0 i e y

Y

6

E b

1

L

K x i

C q j

O

O

Z l

U f n c

1 s z

0 l n z

I

I

5

A f p

L r

B n

J w

A z l

T v q n

5 f g k d

K m n

C

M d

S

N i

0 z

U

O

0

I

C

8

U

I p

6

N

U

K

5

Q

0 w

G

S

A e

7

S p q

Y d d

K t v

R

J

M o

I

Z b

X i o

K

4 v

9

P

I

U m q j z

E x

F

2 p

R y

6 t j

7 p

Y t

W

X y

1

4 s

/ u c

1

Q

9

W

9 b k f

M

C

0

J

F

P

T

J

9 q

B t y p

H w

U

9

4

I c

J i h

R f

L h w

Y c

D i

X

4 x

S

2

X m

R

M

K

F z

O

F p

1

G

C a

C

6

V i

I

9

L

H

A

R

O m i

U

7 o v a

7 m d v

6

R

2

U b

C

K h

W

L l

M l

M

6 f o x

B k k

4 g l

P

I g

Q

V

X

U

I

I

7

K

E

M

V

C

D z

B

M

7 z

A

2

B g b

H

8 a n

8

T

U t

O

W

H

M

2 j

6

E

B

R j f v

7 w

8 r h k

=

<

/ l a t e x i t

> s1 = ¯Q(x, 1) −¯Q(x, 0)

U = |I0 [ I1|

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

C

A d i d

V

9

L u u j

J x l

Q

E

K

U

T w

N

Y q

U f

I

=

"

>

A

A

A

C

M

X i c b

V

C

7

S g

Q x

F

L j

2

/

W

1 a q l

C c

B

G s l h m

L

1

U

Y

U b

C w

V

X

B

V

2 l z

W

T u a v

B z

I

P k j r g

M

U

/ k

1 t v o b

C r

Z i

I

4

K

V v

W

A h m

F k t f

B

0

I

O

Z y

T m

+

Q c

P

1

H

S k

O v e

O

9

A

4

N

D w y

O j p b

H x i c m p

8 v

T

M v o l

T

L b

A u

Y h

X r

Q

5

8 b

V

D

L

C

O k l

S e

J h o

5

K

G v

8

M

A

/

S r

8 g z

P

U

R s b

R

H n

U

T b

I

X

8

O

J

I d

K

T h

Z q

V

1 e a

J

J

U

A

W

Z

J s

6 a h

O e

U c

V

E

4 e c

7

W

W a l d r r h

V t w f

2 l h f p

L

L x

+ v a w e

P d

8 t

N

M u v z e

D

W

K

Q h

R i

Q

U

N

6 b h u

Q m

1

M q

5

J

C o

V

5 q

Z k a

T

L g

4

5 c f

Y s

D

T i

I

Z p

W

1 o u

R s y

W r

B

K w

T a

7 s i

Y j

1

+

0

T

G

Q

2

O

6 o

W

9

P h p x

O z

G

+ v

E

P

/ z

G i l

1

1 l q

Z j

J

K

U

M

B

K f

D

V

S x

S h m

R

S c s k

B o

F q e

6

P

C x

N

Z

/

C

I v

L

X

0

X h d

Q

2

R

2

D

V

Q

H

K h p

Y

F x

A n

X t j

R b c t

G

X

9

7 u d v

2

R

/ p e r

V q r

V d t

7

I

5 f

1

P g

F k

Z g

D h

Z h

G

T x

Y h

U

Y h h

2 o g

4

A

L u

I

Q r u

H a u n

X v n

0

X m

C

H v q c z x

1 m

4

Q e c l w

9 x v

7

S

M

<

/ l a t e x i t

>

˜paction =

˜pdefer = |I0 \ I1|

U a = 1 a = 0

**Figure 2.** Overview of the CTLD framework.

A larger Λ accommodates greater degrees of unobserved confounding. When Λ = 1, the assumption reduces to standard unconfoundedness.

Causal-Target-based Learning to Defer To learn a deferral policy under hidden confounding, our CTLD method proceeds in three key steps, as shown in Figure 2: ﬁrst, we estimate sharp bounds on potential outcomes to quantify causal uncertainty; second, we leverage these bounds to construct a novel causal target; and ﬁnally, we train a policy to match this target using a tailored optimization procedure.

Sharp Bounds Estimation The ﬁrst step of our CTLD framework is to quantify the causal uncertainty arising from hidden confounders. We achieve this by estimating the sharp upper and lower bounds, denoted Q±(x, a), for the conditional average potential outcome (CAPO), where Q(x, a) = E[Y (a)|X = x].

These bounds are derived under Assumption 1 and are formally presented in Deﬁnition 1, which builds upon the quantile balancing method of Dorn and Guo (2023). The full derivation is provided in Appendix C.

Deﬁnition 1 (Sharp Bounds for CAPO). Under Assumption 1, the sharp upper and lower bounds on the CAPO Q(x, a), denoted Q±(x, a), are given by:

Q±(x, a) = w±(x, a)¯µ±(x, a) + w∓(x, a)µ±(x, a) (3)

where the components are deﬁned as follows. The weighting coefﬁcients w±(x, a) are:

w±(x, 1) = e(x) + (1 −e(x))Λ±1, w±(x, 0) = (1 −e(x)) + e(x)Λ±1.

The partial expectations are:

µ±(x, a) = E[Y · I±(Y, x, a)|X = x, A = a],

¯µ±(x, a) = E[Y · ¯I±(Y, x, a)|X = x, A = a].

The indicator functions I± and ¯I± are given by:

I+(y, x, a) = I{y ≤qτ(x, a)}, ¯I+(y, x, a) = I{y > qτ(x, a)},

I−(y, x, a) = I{y ≤q1−τ(x, a)}, ¯I−(y, x, a) = I{y > q1−τ(x, a)}, where the quantile level is τ = Λ/(1 + Λ).

23250

<!-- Page 4 -->

In practice, we compute these bounds by ﬁrst using neural networks to estimate the required nuisance functions: the nominal propensity score e(x) and the conditional quantile function qτ(x, a). The ﬁnal estimated bounds, denoted

ˆQ±(x, a), are obtained by plugging these nuisance estimates into Equation (3).

Causal Target Construction With the uncertainty bounds ˆQ±(x, a) established, the subsequent challenge is to convert this information into a robust learning target. Prior work, such as CARED (Ghoummaid and Shalit 2024), has approached this by constructing a surrogate cost that directly incorporates the single-sample observed outcome y. While innovative, this reliance makes the learning target sensitive to outcome stochasticity, which can impair the learned policy’s reliability. Our core idea, therefore, is to construct a causal target that derives its structure from the stable geometry of the uncertainty intervals, rather than from the noisy observed outcome. This target vector is thus designed with two key components: a deferral probability to represent the degree of causal uncertainty, and a calibrated action distribution to reﬂect the preferred treatment.

Deferral Probability. In our framework, the decision to defer is determined by the uncertainty about which action is optimal. We quantify this uncertainty by the degree of overlap between the estimated CAPO intervals for the two actions. Let Ia = [ ˆQ−(x, a), ˆQ+(x, a)]. The deferral probability is the ratio of the intersection length to the union length of these intervals:

˜pdefer(x) = |I0 ∩I1|

|I0 ∪I1|, (4)

This construction intuitively ensures that signiﬁcant overlap between the bounds leads to a high probability of deferral, while well-separated bounds result in a probability approaching zero.

Action Probability. For the action probabilities, we aim to capture the estimated treatment effect while being calibrated for uncertainty. To derive this probabilities, we begin with a provisional treatment effect based on the interval’s midpoint,

¯Q(x, a) = (ˆQ+(x, a) + ˆQ−(x, a))/2. This midpoint, serving as an initial uncalibrated measure, is then used to deﬁne a raw score for action 1 as score1(x) = ¯Q(x, 1) −¯Q(x, 0), with the score for action 0 being its negative.

However, using these raw scores directly can lead to overconﬁdent probabilities, particularly when the uncertainty bounds are wide. To address this, we introduce an uncertainty-scaling mechanism. We scale the scores by the total uncertainty, U(x) = |I0 ∪I1|, before applying the softmax function:

˜paction(x) = softmax score0(x)

U(x), score1(x)

U(x)

. (5)

This scaling tempers the model’s conﬁdence when causal estimates are imprecise.

Finally, this action distribution ˜paction(x) and the deferral probability ˜pdefer(x) are combined to form the complete causal target ˜p(x):

˜p(x) =

˜p0(x), ˜p1(x); ˜pdefer(x)

. (6) The resulting vector serves as a rich learning target that encodes both a calibrated action distribution and the degree of causal uncertainty.

L2D Policy Learning The ﬁnal step is to learn a scoring function g(x): X →R3 that maps input features to scores for each choice {0, 1, ⊥}. Because the deferral option is conceptually separate from the mutually exclusive actions {0, 1}, a standard softmax over all three outputs is ﬂawed. It would create an undesirable coupling, forcing the deferral probability to decrease as action probability increases, thereby ignoring the overall decision uncertainty.

To handle this structure correctly, we adopt the Asymmetric Softmax parameterization (¯ψ) from Cao et al. (2023). This function maps the raw scores g(x) to a valid probability vector suitable for our problem. Deﬁnition 2 (Asymmetric Softmax Parameterization). For a score vector u = [u0, u1, u⊥], the transformation ¯ψ(u) = [ ¯ψaction(u); ¯ψdefer(u)] is deﬁned as:

¯ψaction(u) = softmax([u0, u1]),

¯ψdefer(u) = exp(u⊥) P j∈{0,1,⊥} exp(uj) −maxj∈{0,1} exp(uj).

This parameterization ensures that the action probabilities ¯ψaction(u) = (¯ψ0(u), ¯ψ1(u)) form a valid distribution (i.e., ¯ψ0(u)+ ¯ψ1(u) = 1), while the deferral probability ¯ψdefer(u) is a separate, calibrated value between 0 and 1. Our learning objective is to minimize the discrepancy between the model’s output probabilities ¯ψ(g(X)) and our constructed causal target ˜p(X). We achieve this by minimizing a surrogate risk ˆR(g), which is a weighted sum of two crossentropy losses:

ˆR(g) = EX∼ˆ Pn h

Laction(g(X), ˜paction(X))

+ λ · Ldefer(g(X), ˜pdefer(X))

i (7)

where λ is a balancing hyperparameter. The action loss Laction is the standard cross-entropy between the predicted and target action distributions. The deferral loss Ldefer is the binary cross-entropy for the deferral decision:

Ldefer = − h

˜pdefer(X) log ¯ψdefer(g(X))

+ (1 −˜pdefer(X)) log(1 −¯ψdefer(g(X)))

i (8)

The optimal scoring function g∗is found by minimizing this empirical risk over a given model class G:

g∗= arg min g∈G

ˆR(g). (9)

The ﬁnal policy π∗(x) is then derived from these optimal scores. Speciﬁcally, after applying the Asymmetric Softmax transformation, we select the choice with the highest resulting probability. This ensures the decision rule is consistent with the calibrated probabilities used during training:

π∗(x) = arg max j∈{0,1,⊥}

¯ψj(g∗(x)). (10)

23251

<!-- Page 5 -->

Overlap

Outcome

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

2 q

6

/

+

A

G

C v

R f

2 z

G z q

I

B

0 s u

W f y o

=

"

>

A

A

A

C

P n i c b

Z

D

L

S g

M x

F

I b

P

1

H u

9

V

V

0

K

E i y

F q r

X

M u

F

A

3 g u

B

G d

6

3

Y

C

7

R j y

W

T

S

N j

R z

I c m

I

Z

Z i l e

9

G

3

O l r

+

A

J u

R

N y

6

E

U x b k

X o

E

P j z j l

J

/ t

8

J

O

Z

P

K

N

J

+

M

1

M

T k

1

P

T

M

7

F x

6 f m

F x a

T m z s l q

V

Q

S

Q

I r

Z

C

A

B

6

L u

Y

E k

8

2 l

F

M c

V p

P

R

Q

U e w

6 n

N a d

3

M u j

X r q i

Q

L

P

A v

V

D

+ k t o c

7

P m s z g p

V

G r c z

2

W c t

E

R

6 j

R

7

G

I

V l

P

L e

D f

J

X x f

M r

Q

L

6

J j s j

Y r c y

W b

N o

D g v

9

F d a

X y

B

D

+ e

V m

4

/

6

8

1

M p

8

N

N

2

A

R

B

7

1

F e

F

Y y o

Z l h s q

O s

V

C

M c

J q k m

G k

I

S

Y

9

3

K

E

N

L

X

3 s

U

W n

H

Q

0

8

J y m n i o n

Y g

9

P

E

V

G t

L x j

R h

7

U v

Y

9

R

0

9

6

W

H

X l

7

9

4

A

/ t d r

R

K p

9 a

M f

M

D y

N

F f

T

J

6 q

B

1 x p

A

I

0

C

A i

T

F

C i e

P

/

H h

S

E b

/

C

J

J

8

Y h

Y

U

L

7 c

D

V

1

G

S a

C a

V u

I d

L

H

A

R

O n

E

0 z o v

6

3 c

6 f

0

V

1 r

2 j t

F

/ f

L

O j g

E o q

F d d i

E

P

F h w

A

M d w

C i

W o

A

I

F b u

I

M

H e

D

Q e j

W f j

1

X g b j a a

M r

0

1

+

F

H

G

+ y f

I

1 b

B

S

<

/ l a t e x i t

>

I0 = [ ˆQ−(x, 0), ˆQ+(x, 0)]

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

O

A

E

Z

H y t w

P

2

P v p

U

R b

R b j c

P u

D

V m

4

U

=

"

>

A

A

A

C

F

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

U

V

4

2 v q k t

B

B k v

B

V

U m

K

V

F

0

I

B

T c u

K i

2

0

I

Y y m

U z a o

Z

N

J m

J k

I

I f

Q b

3

N q v c

S d u

X f o x g p

M

2 i z

4

8

M

H

A

4

9

4

7

9 x

4 v

Z l

Q q y

/ o x

S l v b

O

7 t

7

X

3 z

4

P

D o

+

K

R y e t a

R

U

S

I w c

X

D

E

I t

H z k

C

S

M c u

I o q h j p x

Y

K g

0

G

O k

6

0

0 e c

7

/

7

S o

S k

E

X

9

R a

U z c

E

I

0

4

D

S h

G

S k t

O

O m w

8

3

A

8 r

V a t u z

Q

E

3 i

V

2

Q

K i j

Q

H l

Z

+

B

3

6

E k

B w h

R m

S s m

9 b s

X

I z

J

B

T

F j

E z

N

Q

S

J

J j

P

A

E j

U h f

U

4

C

I t

1 s v u w

U

1 r

T i w y

A

S

+ n

E

F

+ p y

R

4

Z

C

K d

P

Q

0

U h

U m

O

7 u

X i f

1

4

/

U c

G d m

1

E e

J

4 p w v

P g o

S

B h

U

E c w v h z

4

V

B

C u

W r g y

M a b

7

F

1

K w t i g

K f

Y e v

V

Z

8 i

L

K g

+

C

+

I x

E g g r

H a

W p

8

7

L

X

0

9 k k n

U b d b t a b z z f

V

1 m

W

R

X

B l c g

C t w

D

W x w

C

1 r g

C b

S

B

A z

C g

4

A

2

8 g k x

M z

6

M

T

+

N r

U

V o y i p z s

A

L j

+ w

8

A

V p

+ d

<

/ l a t e x i t

> y2 = 9 y1 = 17

< l a t e x i t s h a

1

_ b a s e

6

4

=

" s

K c

2 q y l y s

B t u b p t l k k

4

H

S k

9 u

B o

=

"

>

A

A

A

C

P n i c b

Z

D

L

S g

M x

F

I b

P

1

H u

9

V

V

0

K

E i y

F q r

X

M u

F

A

3 g u

B

G d

6

3

Y

C

7

R j y

W

T

S

N j

R z

I c m

I

Z

Z i l e

9

G

3

O l r

+

A

J u

R

N y

6

E

U x b k

X o

E

P j z j l

J

/ t

8

J

O

Z

P

K

N

J

+

M

1

M

T k

1

P

T

M

7

F x

6 f m

F x a

T m z s l q

V

Q

S

Q

I r

Z

C

A

B

6

L u

Y

E k

8

2 l

F

M c

V p

P

R

Q

U e w

6 n

N a d

3

M u j

X r q i

Q

L

P

A v

V

D

+ k t o c

7

P m s z g p

V

G r c z

2

W c t

C

R

6 j

R

7

G

I

V l

P

L e

D f

J

X x e s r

Q

L

6

J j s j

Y r c y

W b

N o

D g v

9

F d a

X y

B

D

+ e

V m

4

/

6

8

1

M p

8

N

N

2

A

R

B

7

1

F e

F

Y y o

Z l h s q

O s

V

C

M c

J q k m

G k

I

S

Y

9

3

K

E

N

L

X

3 s

U

W n

H

Q

0

8

J y m n i o n

Y g

9

P

E

V

G t

L x j

R h

7

U v

Y

9

R

0

9

6

W

H

X l

7

9

4

A

/ t d r

R

K p

9 a

M f

M

D y

N

F f

T

J

6 q

B

1 x p

A

I

0

C

A i

T

F

C i e

P

/

H h

S

E b

/

C

J

J

8

Y h

Y

U

L

7 c

D

V

1

G

S a

C a

V u

I d

L

H

A

R

O n

E

0 z o v

6

3 c

6 f

0

V

1 r

2 j t

F

/ f

L

O j g

E o q

F d d i

E

P

F h w

A

M d w

C i

W o

A

I

F b u

I

M

H e

D

Q e j

W f j

1

X g b j a a

M r

0

1

+

F

H

G

+ y f

O

H

7

B

V

<

/ l a t e x i t

>

I1 = [ ˆQ−(x, 1), ˆQ+(x, 1)]

8 11

< l a t e x i t s h a

1

_ b a s e

6

4

=

"

L

V

L

W u i o t b b

Y

9

V s

J

4

G b

C s e z

1 z

2 e g

=

"

>

A

A

A

C

F

H i c b

V

D

L

S g

M x

F

L

3 j s

4

6 v q k t d

B

E v

B

V

Z m

R

U l

0

W

3

L i s

Y h

/

Q

D i

W

T y b

S h m c y

Q

Z

I

R

S

+ g d u

7 d e

4

E

3 f q

3 o

8

R z

L

R d

9

O

G

B w

O

G c

O a e

4 y e c

K e

0

4

P

9 b

G t b

2 z m u z

9

4

/

O

D w

6 z p

+ c

N l

S c

S k

L r

J

O a x b

P l

Y

U c

4

E r

W u m

O

W

0 l k u

L

I

7

T p

D

+

4 y v

/ l

M p

W

K x e

N

L

D h

H o

R

7 g k

W

M o

K

1 k

R

7 d c j d f c

E r

O

F

G i d u

H

N

S g

D l q

3 f x v

J

4 h

J

G l

G h

C c d

K t

V

0 n

0 d

4

I

S

8

0

I p

2

O

7 k y q a

Y

D

L

A

P d o

2

V

O

C

I

K m

8

0

3

X

S

M i k

Y

J

U

B h

L c

4

R

G

U

3

X x x

Q h

H

S g

0 j

3

9 y

M s

O

6 r

V

S

8

T

/

/

P a q

Q v v

R

E

T

S a q p

I

L

O

P w p

Q j

H a

M s

N g q

Y p

E

T z

4 d

L

A h

G

V b j

O

3 i o k i

Y

N

D k

C o w

Y

M

E

8 l

M

L

E

T

6

W

G

K i

T

Y

+

2

6 c t d b

W e d

N

K

L b q

V

U e

S g

X q h e f

G b

4 g

B

+ d w

C

V f g w g

1

U

4

R q

U

A c

C

I b z

A

K

0 y s i f

V m v

V s f s

I

3 r

H n b

Z

7

A

E

6

/ s

P

E

E

G j

K w

=

=

<

/ l a t e x i t

>

14 17

**Figure 3.** An illustrative scenario under hidden confounding, where the CAPO intervals for two actions overlap signiﬁcantly.

An Illustrative Comparison To highlight the advantage of our probabilistic causal target, we compare our CTLD framework to cost-sensitive methods, such as CARED (Ghoummaid and Shalit 2024), in a hidden confounding scenario. Assume for a patient with covariates x, the estimated CAPO intervals are I0 = [5, 15] and I1 = [8, 18], as depicted in Figure 3. Suppose an expert chose action a = 1, but we observe two different outcomes due to unobserved confounders: a high outcome y1 = 17 and a modest one y2 = 9. Cost-Sensitive Approach (e.g., CARED). This approach’s deferral cost, C⊥, directly depends on the observed outcome y. For our two realizations, this cost changes drastically from C⊥(y1) = 5 −17 = −12 to C⊥(y2) = 5 −9 = −4. This demonstrates a key weakness: the learning signal is highly sensitive to outcome uncertainty, which can impair the learned policy’s robustness. Our CTLD Approach. In contrast, our method constructs a causal target directly from the interval geometry, making it independent of the noisy outcome.

• The deferral probability, determined by the intervals’ relative overlap, is ˜pdefer(x) = |I0 ∩I1|/|I0 ∪I1| ≈0.54. • The action probabilities, derived from uncertaintyscaled CATE scores, are calibrated to ˜paction(x) ≈ [0.39, 0.61].

The resulting causal target, ˜p(x) ≈[0.39, 0.61; 0.54], is identical for both y1 and y2. This principled decoupling from outcome uncertainty provides a stable learning target, which is a central advantage of our CTLD framework. Detailed calculations are provided in Appendix D.

To summarize our CTLD, Algorithm 1 presents the procedure in three high-level steps: estimating sharp bounds, constructing causal targets, and learning the L2D policy.

Theoretical Guarantees Our theoretical analysis is presented in three interconnected parts. First, we establish the consistency of our CTLD’s core components (Propositions 1 and 2), which conﬁrms that our novel causal target is not an arbitrary construct but a statistically reliable learning target that converges to a meaningful quantity. Second, we present our main theoretical contribution: a regret-transfer bound (Theorem 1). This is the crucial bridge that formally connects minimizing our surrogate learning objective to the ultimate goal of minimizing the true, unobservable causal regret. Finally, we provide a standard generalization bound (Theorem 2) to ensure that the policy learned on the training data will perform

## Algorithm

1: Causal-target-based learning to defer (CTLD)

1: Input: Dataset D = {Xi, Ai, Yi}N i=1, confounding level Λ, loss balance λ, model class G 2: Output: Learned policy ˆπ(x) 3: // Step 1: Estimate sharp bounds 4: Estimate sharp CAPO bounds ˆQ±(Xi, a) for all samples i = 1,..., N. 5: // Step 2: Construct causal targets 6: for each Xi do 7: Compute deferral probability ˜pdefer(Xi) 8: Compute action probabilities ˜paction(Xi) 9: Form the complete target ˜p(Xi) 10: end for 11: // Step 3: Learn L2D policy 12: Learn g∗∈G by minimizing total loss over all ˜p(Xi) 13: return ˆπ(x) by Equation (10)

reliably on unseen data. Collectively, these results provide a comprehensive theoretical validation, showing that CTLD is not only learnable and stable, but also a principled and effective approach to decision-making under uncertainty. Assumption 2 (Regularity, Flexibility, and Convergence). We assume the following: (a) Bounded Outcomes: |Y | ≤ CY. (b) Sieve Approximation: optimal scoring function g∗can be increasingly well-approximated by a sequence of function classes {Gm}m≥1, where m denotes the model complexity. Formally, infg∈Gm ∥g −g∗∥L2 = O(m−β) for some β > 0. (c) Complexity Control: For every m, Rn(Gm) = O q log m n

. (d) Data-Driven Se- lection: Choose m = m(n) so that q log m(n)

n ≍n−α with α < β/(1 + 2β). (e) Bound Estimation Rate: ∥bQ± n − Q±∥L2 = Op(n−α).

Assumption (a) guarantees bounded potential outcomes and hence bounded sharp bounds. For (b) and (c), we employ a regularised sieve of weight–decayed ReLU networks Gm(n) whose width grows as m(n) ∝n1/(1+2β). This construction (i) approximates any β–H¨older target at rate m(n)−β, and (ii) enjoys a Rademacher complexity Rn(Gm(n)) = O p log m(n)/n due to the spectral-norm constraint (Schmidt-Hieber 2020). We determine m(n) via cross–validated early stopping, a practical method intended to approximate the balanced rate required by (d). Assumption (e) is justiﬁed by the established n−α rate for the deep neural network nuisance estimators used in their construction (Farrell, Liang, and Misra 2021, Theorem 1). This architecture and training protocol are consistent with state–of–the–art implementations (Ghoummaid and Shalit 2024; Hess et al. 2025). Proposition 1 (Consistency of Bound Estimators). Assumption 2(e) implies that the CAPO bound estimators ˆQ± n (x, a) are consistent for the true sharp bounds Q±(x, a). See Appendix C for the full proof. This proposition ensures that the inputs to our causal target construction are asymp-

23252

<!-- Page 6 -->

totically correct.

Proposition 2 (Consistency of the Causal Target). Under the consistency of the causal bound estimators, as the sample size n →∞, the causal target ˜pn(X) converges in probability to a deterministic limiting vector ˜p∗(X) that correctly reﬂects the underlying causal uncertainty.

See Appendix C for the full proof.

With these consistency propositions, our main theoretical contribution is a regret-transfer bound. Our ultimate goal is to ﬁnd a policy that minimizes the true causal regret, which measures the performance gap to the unknown optimal policy. However, this objective cannot be optimized directly. Instead, during training, we minimize a tractable true surrogate risk, denoted R(g), which is the expected cross-entropy loss against our causal targets. Let R∗be the minimum possible value of this risk. The quantity R(g)−R∗ is then the excess surrogate risk—a measure of how suboptimal our learned model is on the training objective. The following theorem provides the crucial bridge connecting causal regret to the surrogate risk.

Theorem 1 (Regret-Transfer Bound). For every score function g, let πg be the policy derived from it and π∗be the oracle policy deﬁned by the causal target. Then the excess causal regret is bounded by the excess surrogate risk:

EX

RegX(πg)

−EX

RegX(π∗)

≤Umax √

2 p

R(g) −R∗.

The full proof is provided in Appendix C. The signiﬁcance of this theorem is that it justiﬁes our entire learning procedure. It provides a formal guarantee that by ﬁnding a model with a low training error (i.e., minimizing the surrogate risk R(g)), we are indeed making progress towards the true goal of ﬁnding a policy with low real-world regret.

Finally, we provide a ﬁnite-sample generalization bound for our CTLD. This result is crucial as it connects the empirical risk ˆR(g) (what we minimize on our training data) to the true risk R(g) (the performance on the real-world data distribution), guaranteeing that the policy learned on the training data will perform reliably on unseen data.

Theorem 2 (Generalization Bound). Recall that R(g) is the true surrogate risk and let ˆR(g) be the empirical surrogate risk. Under Assumption 2, for the empirical risk minimizer ˆgn, with probability at least 1 −δ, the following holds:

R(ˆgn) −ˆR(ˆgn) ≤C1Rn(G) + C2n−α + C3 r log(1/δ)

n,

(11) where Rn(G) is the Rademacher complexity of the function class G, and C1, C2, C3 are constants.

The full proof is provided in Appendix C. This bound provides insight into the sources of generalization error, which consists of three key components: a term for the complexity of the model class (Rn(G)), an approximation error term from using an estimated target (n−α), and a standard statistical learning term.

0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 log(Λ) uncertainty parameter

−1.25

−1.00

−0.75

−0.50

−0.25

0.00

0.25

0.50

Policy Regret

CTLD ConfHAI CARED B-Learner CRLogit

Pessimistic Human Oracle True log(Λ)

**Figure 4.** Policy regret on synthetic data. The x-axis shows the assumed level of hidden confounding (log(Λ)), and lower policy regret indicates better performance. The vertical dashed line marks the true confounding level (log(Λ0) = 2.5). Our method, CTLD, consistently outperforms key baselines across nearly all levels of confounding.

## Experiments

We conduct experiments to evaluate the effectiveness of our proposed method, CTLD, in learning deferral policies under hidden confounding. We use two experimental settings: (1) a synthetic environment adapted from (Gao and Yin 2025) to allow for controlled analysis, and (2) a semi-synthetic setup based on the IHDP dataset (Hill 2011) to assess performance on more realistic data distributions. In both settings, we vary the marginal sensitivity parameter Λ to simulate different degrees of unobserved confounding.

Baselines and Setup We compare our CTLD against a comprehensive range of recent and standard baselines:

• ConfHAI (Gao and Yin 2025): A minimax IPW approach for deferral policy learning. • CARED (Ghoummaid and Shalit 2024): A cost-sensitive classiﬁcation method for deferral policy learning. • B-Learner (Oprescu et al. 2023; Jesson et al. 2021): A policy that defers when CATE interval bounds cross zero, otherwise assigns treatment. • CRLogit (Kallus and Zhou 2021): A minimax policy learning model without any deferral mechanism. • Pessimistic Policy: A conservative policy that avoids deferral by choosing the action with the better worst-case. • Random Deferral Policy: Randomly defers with ﬁxed probability, serving as a naive baseline. • Human/Expert Policy: A human-derived policy, simulating human decision-makers recommendations. • Oracle: A clairvoyant policy with access to true potential outcomes, used as an upper bound.

Comprehensive details regarding the experimental setup, data generation, and hyperparameter settings for all models, are provided in Appendix E.

23253

<!-- Page 7 -->

10−1 100 log(Λ) uncertainty parameter

13.5

14.0

14.5

15.0

15.5

16.0

16.5

17.0

Policy Value

CTLD ConfHAI CARED B-Learner CRLogit

Pessimistic Random Expert Oracle True log(Λ)

(a) Policy value for different values of log(Λ).

0.1 0.2 0.5 0.7 1.0 1.2 1.5 2.0 2.5 3.0 3.5 4.0 log(Λ) uncertainty parameter

0.0

0.2

0.4

0.6

0.8

Deferral Rate

CARED B-Learner

ConfHAI CTLD

(b) Deferral rate for different values of log(Λ).

**Figure 5.** Performance on the semi-synthetic IHDP dataset. (a) Policy value (higher is better) versus the assumed confounding level log(Λ), with the true value marked by a vertical dashed line. (b) Corresponding deferral rates for the deferral-enabled policies. CTLD achieves the highest policy value among learned policies while employing a highly efﬁcient deferral strategy, with a deferral rate consistently less than a third of that of the CARED baseline.

Synthetic Dataset

We replicate the synthetic data experiment from (Gao and Yin 2025) and run 10 trials. For each trial, we vary the uncertain parameter log(Λ) from 0.1 to 4, corresponding to various levels of assumed hidden confounding. We compare the policy regret for the returned policy for each method relative to the Baseline Policy, which assigns action a = 0 for all individuals. Additionally, we report the policy regret of Human Policy. Figure 4 shows the results. CTLD achieves the lowest regret among nearly all learned policies, closely approaching the Oracle performance. Notably, the performance of methods like ConfHAI and CARED deteriorates signiﬁcantly when the assumed confounding level log(Λ) is misspeciﬁed (i.e., far from the true value of 2.5). In contrast, CTLD remains stable across the entire range, demonstrating robustness to the misspeciﬁcation of the confounding level.

IHDP Dataset

To evaluate performance in a more realistic setting, we test our method on the semi-synthetic IHDP dataset, following the setup from (Jesson et al. 2021). The results, averaged over 200 dataset realizations, are presented in Figure 5.

The ﬁndings highlight the effectiveness and efﬁciency of our CTLD framework. As shown in Figure 5(a), CTLD consistently achieves the highest policy value among nearly all learned policies, robustly outperforming other methods across the entire range of confounding levels. Simultaneously, Figure 5(b) demonstrates that this superior performance is achieved with remarkable efﬁciency, as CTLD’s deferral rate is consistently less than a third of that required by the CARED. This result empirically validates that our core proposal of constructing the probabilistic learning target leads to a more effective and efﬁcient deferral policy.

0.2 0.4 0.6 0.8 1.0 2.0 3.0 4.0 5.0 Hyperparameter λ

14.5

15.0

15.5

16.0

16.5

17.0

17.5

Policy Value

0.0

0.1

0.2

0.3

0.4

0.5

0.6

Deferral Rate

Policy Value Deferral Rate

**Figure 6.** Ablation study on the hyperparameter λ in Equation (7). Larger λ increases the deferral rate while keeping the policy value stable.

Ablation Study

To assess the effect of λ, we conduct an ablation at log(Λ) = 0.5 and report results averaged over 200 trials. As shown in Figure 6, increasing λ monotonically raises the deferral rate. Crucially, this is achieved while the policy value remains high, indicating that CTLD learns to defer on genuinely uncertain cases without sacriﬁcing performance.

## Conclusion

In this paper, we study learning to defer under hidden confounding using only observational data. We introduce CTLD framework, which constructs a stable probabilistic target from sharp bounds on potential outcomes. CTLD is supported by regret-transfer and generalization guarantees. Experiments show that CTLD achieves strong policy value with an efﬁcient deferral rate, remaining robust even under misspeciﬁed confounding.

23254

<!-- Page 8 -->

## Acknowledgments

We thank all the anonymous reviewers and meta reviewers for their valuable comments, as well as all of our team members for their support and assistance.

## References

Athey, S.; and Wager, S. 2021. Policy learning with observational data. Econometrica, 89(1): 133–161. Bondi, E.; Koster, R.; Sheahan, H.; Chadwick, M.; Bachrach, Y.; Cemgil, T.; Paquet, U.; and Dvijotham, K. 2022. Role of human-AI interaction in selective prediction. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 36, 5286–5294. Cao, Y.; Mozannar, H.; Feng, L.; Wei, H.; and An, B. 2023. In defense of softmax parametrization for calibrated and consistent learning to defer. Advances in Neural Information Processing Systems, 36: 38485–38503. Dorn, J.; and Guo, K. 2023. Sharp sensitivity analysis for inverse propensity weighting via quantile balancing. Journal of the American Statistical Association, 118(544): 2645– 2657. Farrell, M. H.; Liang, T.; and Misra, S. 2021. Deep neural networks for estimation and inference. Econometrica, 89(1): 181–213. Gao, R.; Saar-Tsechansky, M.; De-Arteaga, M.; Han, L.; Lee, M. K.; and Lease, M. 2021. Human-AI Collaboration with Bandit Feedback. In Zhou, Z.-H., ed., Proceedings of the Thirtieth International Joint Conference on Artiﬁcial Intelligence, IJCAI-21, 1722–1728. Gao, R.; and Yin, M. 2025. Confounding-robust deferral policy learning. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 39, 14238–14246. Ghoummaid, M.; and Shalit, U. 2024. When to act and when to ask: policy learning with deferral under hidden confounding. Advances in Neural Information Processing Systems, 37: 56108–56135. Hemmer, P.; Thede, L.; V¨ossing, M.; Jakubik, J.; and K¨uhl, N. 2023. Learning to defer with limited expert predictions. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 37, 6002–6011. Hess, K.; Frauen, D.; Melnychuk, V.; and Feuerriegel, S. 2025. Efﬁcient and sharp off-Policy learning under unobserved confounding. arXiv:2502.13022. Hill, J. L. 2011. Bayesian nonparametric modeling for causal inference. Journal of Computational and Graphical Statistics, 20(1): 217–240. Ho, K.; and Rosen, A. M. 2015. Partial identiﬁcation in applied research: beneﬁts and challenges. Technical report, National Bureau of Economic Research. Imbens, G. W.; and Rubin, D. B. 2015. Causal inference in statistics, social, and biomedical sciences. Cambridge university press. Jesson, A.; Mindermann, S.; Gal, Y.; and Shalit, U. 2021. Quantifying ignorance in individual-level causal-effect estimates under hidden confounding. In International Conference on Machine Learning, 4829–4838. PMLR.

Kallus, N. 2018. Balanced Policy Evaluation and Learning. In Bengio, S.; Wallach, H.; Larochelle, H.; Grauman, K.; Cesa-Bianchi, N.; and Garnett, R., eds., Advances in Neural Information Processing Systems, volume 31. Curran Associates, Inc. Kallus, N.; and Zhou, A. 2018. Confounding-robust policy improvement. Advances in neural information processing systems, 31. Kallus, N.; and Zhou, A. 2021. Minimax-optimal policy learning under unobserved confounding. Management Science, 67(5): 2870–2890. Leit˜ao, D.; Saleiro, P.; Figueiredo, M. A. T.; and Bizarro, P. 2022. Human-AI Collaboration in Decision-Making: Beyond Learning to Defer. arXiv:2206.13202. Mozannar, H.; Lang, H.; Wei, D.; Sattigeri, P.; Das, S.; and Sontag, D. 2023. Who should predict? exact algorithms for learning to defer to humans. In International conference on artiﬁcial intelligence and statistics, 10520–10545. PMLR. Mozannar, H.; and Sontag, D. 2020. Consistent estimators for learning to defer to an expert. In International conference on machine learning, 7076–7087. PMLR. Oprescu, M.; Dorn, J.; Ghoummaid, M.; Jesson, A.; Kallus, N.; and Shalit, U. 2023. B-learner: Quasi-oracle bounds on heterogeneous causal effects under hidden confounding. In International Conference on Machine Learning, 26599– 26618. PMLR. Ruggieri, S.; and Pugnana, A. 2025. Things machine learning models know that they don’t know. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 39, 28684–28693. Schmidt-Hieber, J. 2020. Nonparametric regression using deep neural networks with ReLU activation function. The Annals of Statistics, 48(4): 1875–1897. Tailor, D.; Patra, A.; Verma, R.; Manggala, P.; and Nalisnick, E. 2024. Learning to defer to a population: A meta-learning approach. In International Conference on Artiﬁcial Intelligence and Statistics, 3475–3483. PMLR. Tan, Z. 2006. A distributional approach for causal inference using propensity scores. Journal of the American Statistical Association, 101(476): 1619–1637.

23255
