---
title: "SyncBrain: Exploring Brain Functional Dynamics Through Neural Oscillatory Synchronization"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37156
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/37156/41118
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# SyncBrain: Exploring Brain Functional Dynamics Through Neural Oscillatory Synchronization

<!-- Page 1 -->

SyncBrain: Exploring Brain Functional Dynamics Through Neural Oscillatory

Synchronization

Jiaqi Ding1, Tingting Dan2, Zhixuan Zhou1, Guorong Wu1,2*

1Department of Computer Science, The University of North Carolina at Chapel Hill 2Department of Psychiatry, The University of North Carolina at Chapel Hill {jiaqid, zzhixuan}@cs.unc.edu, {Tingting Dan, grwu}@med.unc.edu

## Abstract

Neural coupling is a fundamental mechanism in neuroscience that facilitates the emergence of cognitive functions through dynamic interactions and synchronization among distributed brain regions. Inspired by this principle, we pose the question: Might the biological mechanism of neural oscillatory synchronization inspire the feature representation learning for neuroscience? By addressing this question through the Kuramoto model, renowned for simulating oscillatory dynamics, we present a novel physics-informed deep model, SyncBrain, it models brain regions as interacting oscillatory units and simulates their temporal dynamics and synchronization patterns to distinguish cognitive states. Furthermore, inspired by the brain’s inherent ability to dynamically attend to critical temporal information, we incorporate an adaptive control module that introduces an attention-like mechanism to guide information flow. We evaluate our model on multiple functional neuroimaging datasets, it demonstrates promising performance and enhanced interpretability in both cognitive state decoding and early disease diagnosis, outperforming existing computational methods. These results demonstrate the effectiveness of neural oscillatory mechanisms in shaping robust and interpretable machine learning models for neuroscience applications.

## Introduction

Growing evidence suggests that neurons interact through lateral connections, giving rise to rhythmic fluctuations of excitability (often referred to as brain rhythms or neural oscillations) within neuronal ensembles (Hubel and Wiesel 1962; Buzsaki 2006). Synchronized neurons form clusters that compete to interpret incoming signals. This competition, often referred to as “competitive learning”, progressively compresses information as it propagates through neuronal layers, thereby improving feature representation (Amari and Arbib 1977; Mountcastle 1997). At higher levels, competition further drives neurons to specialize in different aspects of the input (Notbohm, Kurths, and Herrmann 2012). In this way, oscillations facilitate the exchange of information across different sensory pathways, thereby playing a pivotal role in cross-modal influence (Van Atteveldt et al. 2014).

*Corresponding author Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Neural Oscillatory

Synchronization

Full locking unlocking

Time Coupling

Brain structure

Brain function Cognition

Behavior

Disease diagnosis

& prognosis

Explain, predict, understand

**Figure 1.** Illustration of neural oscillatory synchronization in brain rhythms. In this study, we develop a computational model to capture the emergence of synchronization from chaotic (unlocking) to synchronized (locking) phases based on underlying brain dynamics that reflect cognitive and pathological states.

Building on these oscillatory mechanisms, the brain coordinates distributed information processes involving sensory integration, parallel processing, and multi-modal convergence (Ghazanfar and Lewkowicz 2009), thereby binding information from separate cortical regions into coherent percepts and actions, as illustrated in Fig. 1. As a result, the human brain integrates signals from multiple sensory pathways to support cognition and behavior. This neural synchronization also manifests in our everyday experience. In daily life, we continually process information across diverse channels, such as sight, sound, and touch, enabling cross-modal influences to reinforce each other and enhance perceptual coherence and highlighting the importance of synchronized neural activity in creating unified perceptual experiences.

Thus, oscillatory synchronization is a hallmark of brain function, encoding diverse cognitive states through distinct spatial and temporal synchronization patterns across brain regions. These oscillatory signatures have been shown to differentiate task conditions, cognitive loads, and even disease stages (Siegel, Donner, and Engel 2012). By modeling such mechanisms, machine learning models can naturally inherit the brain’s capacity to distinguish functional states, enabling more accurate decoding and biologically grounded interpretations. Although various data-driven models have achieved remarkable success in understanding the neural mechanisms of how brain function gives rise to cognition by characterizing functional fluctuations (Gallos et al. 2024), a modeling

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

![Figure extracted from page 1](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-001-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-001-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 1](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-001-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

framework that explicitly decodes brain states from the perspective of neural oscillatory patterns has not been fully explored yet. Most existing approaches overlook the potential of oscillatory dynamics as a structured prior, leaving a gap in leveraging this fundamental principle for functional state representation.

Our work addresses this gap by introducing a physicsinformed framework grounded in neural oscillatory synchronization, coined SyncBrain, which integrates the principles of system dynamics governed by the Kuramoto model (Kuramoto 1975, 1984) to simulate the oscillatory synchronization patterns among distributed brain regions. Meanwhile, from a biological standpoint, the brain dynamically adjusts its oscillatory activity to process task-relevant information and suppress irrelevant fluctuations, which is an ability crucial for robust perception and cognition. Motivated by this domain knowledge, we introduce an adaptive control into the framework, enabling the model to dynamically regulate coupling strengths based on input features. This design allows the model to capture informative temporal dynamics while remaining resilient to context variability. Overall, our framework provides three main benefits: • By incorporating neuroscientific priors and mimicking brain rhythms under different cognitive or pathological states, the model achieves more accurate and robust state decoding performance. • The explicit integration of neural oscillation principles improves model transparency and interpretability, allowing us to analyze and understand the learning behavior of deep models from a neuroscientific perspective. • We validate our model across large-scale datasets involving both neurodegenerative diseases and cognitive tasks, where it demonstrates promising predictive performance. In addition, we show rich visualization and interpretability results to analyze how the model represents and aggregates oscillatory features, further reinforcing learning transparency and model explainability. This framework is designed to capture the governing dynamics underlying fluctuating neural oscillations, offering a biologically-grounded and interpretable approach for modeling brain function.

Related Works Brain State Decoding from fMRI. Brain state decoding aims to infer mental or cognitive states from brain activity, particularly functional magnetic resonance imaging (fMRI) signals. Early approaches relied heavily on linear/logistic classifiers, often applied to region-based or voxelwise statistical features (Pereira, Mitchell, and Botvinick 2009; Mitchell et al. 2004). With the growing availability of large-scale datasets like the Human Connectome Project (HCP) and ADNI, there has been a shift towards network-based representations, especially functional connectivity (FC) (Wee et al. 2012; Finn et al. 2015). Recently, deep learning models have achieved significant performance improvements by automatically extracting hierarchical representations from fMRI data, such as CNNs (Khosla et al. 2019), RNNs and LSTMs (Li and Fan 2018), as well as Transformer-based architectures (Hayat and Aramvith 2024). In addition, GNNs (Li et al. 2021) have emerged as a powerful tool for brain state decoding, as they can explicitly model interactions between brain regions (Ktena et al. 2018). Despite these advances, most models remain predominantly data-driven and may lack biological grounding, limiting their interpretability and robustness to noise. This gap has motivated recent efforts to incorporate domain knowledge into model design, such as modeling brain dynamics through differential equations (Cui et al. 2022).

Structural–Functional Coupling in the Brain. Understanding the relationship between structural connectivity (SC) and functional connectivity (FC) is central to uncovering how the brain’s physical architecture shapes its dynamic activity patterns. Honey et al. (2009) conducted one of the foundational studies in this area, showing that SC can partly predict resting-state FC patterns using computational models of neural dynamics (Honey et al. 2009). Subsequent studies have employed graph-theoretical (Abdelnour, Voss, and Raj 2014; Becker et al. 2018), machine learning (Zhang, Zhang, and Wu 2022), and dynamical systems approaches to explore SC-FC coupling. In the context of neurological disorders, Dan et al. (2023) proposed a cross-modality GNN model to uncover SC-FC coupling alterations in neurodegenerative diseases. Chow et al. (2024) extended this idea using a Koopman operator framework to model brain dynamics with explicit SC-FC coupling.

Oscillatory Networks in Machine Learning. The Kuramoto model is a classical nonlinear dynamical system describing synchronization in coupled oscillators (Kuramoto 1975). It has served as a foundation for modeling brain rhythms (Breakspear, Heitmann, and Daffertshofer 2010) and has recently been introduced into neural network architectures to model coordination and phase coupling among units. (Rusch et al. 2022) proposed Graph-Coupled Oscillator Networks (GraphCON), which propose a principled approach to deep graph learning via discretizations of secondorder ODEs representing damped, non-linear oscillators. (Nguyen et al. 2024) proposed a Kuramoto-based GNN variant that directly mitigates oversmoothing in deep GNNs by modulating node updates through oscillator dynamics. (Miyato et al. 2024) introduces Artificial Kuramoto Oscillatory Neurons (AKOrN) as a dynamical alternative to conventional threshold units, which uses generalized Kuramoto dynamics to induce synchronization among units. Despite their promise, oscillatory models in machine learning are still in their early stages. There remains significant opportunity to integrate these dynamics into task-relevant domains, such as brain decoding, where modeling neural synchronization can offer both performance and interpretability gains.

## Methodology

I. From Brain Networks to Brain Oscillations

Neural oscillations play a fundamental role in coordinating information processing across spatially distributed brain regions (Buzsaki 2006; Varela et al. 2001), wherein multiple brain regions temporally synchronize their activity to facilitate functional integration. To quantitatively study such

<!-- Page 3 -->

Oscillatory Synchronization

Y(L)

X(L)

identification

Graph Scattering Transform

Connectivity yi xi xj

𝑲𝒊𝒋

Y(0)

X(0)

BOLD signal

Disease Diagnosis

& Cognitive task

**Figure 2.** Illustration of SyncBrain. The geometric scattering transform (GST) is used to generate initial oscillators ˆX(0,0), while an adaptive control produces memory feedback ˆY (0). The oscillators evolve through synchronization, influenced by their intrinsic frequency, neighbors, and memory. The final state ˆY (L) is used for downstream tasks.

synchronization phenomena, the Kuramoto model has been widely used in computational neuroscience (Cabral et al. 2011; Deco et al. 2017). It captures how the intrinsic dynamics of brain regions and their interactions give rise to emergent synchronization patterns observed in neuroimaging data. Motivated by these findings, we aim to build a computational model that leverages Kuramoto oscillator dynamics to characterize brain rhythms, which can not only reflect biophysically plausible synchronization dynamics but also provide a new mechanism to decode cognitive or pathological brain states from neuroimaging signals.

Brain Networks. Current neuroimaging studies often represent the human brain as a graph G = (V, W), where V = {v1,..., vN} is the set of N brain regions (nodes), and W = [wij]N i,j=1 is the weighted adjacency matrix reflecting pairwise connectivity strengths. For a structural brain network derived from SC, we define the adjacency matrix entries wij as the normalized fiber counts between brain regions vi and vj. For a functional network, let X = {x | x(p) ∈RN, p = 1,..., P} represent the blood-oxygenlevel-dependent (BOLD) signals measured at region vi over P time points. The Pearson correlations among these signals determine the connectivity strengths wij.

The Kuramoto Framework. The Kuramoto model (Kuramoto 1975, 1984) is a canonical system for studying synchronization in networks of coupled oscillators. Each oscillator i has a phase θi(t) that evolves according to: dθi dt = ωi+K PN j=1 sin(θj−θi), where ωi is the intrinsic frequency and K is the global coupling strength. Depending on these parameters, the system exhibits transitions from incoherence to partial/global synchronization, making it a powerful tool to capture the collective dynamics of the brain network.

Linking Brain Networks to Oscillator Dynamics. Bridging the above views, we treat each brain region’s signal xi as arising from an intrinsic oscillator, by involving wij in the coupling coefficient between oscillators i and j. This enables us to construct an oscillator-based dynamical system over the brain network G that jointly reflects the structural topology (W) and temporal activity patterns (X). As shown in the following sections, this formulation not only models observed neural synchrony but also provides a theoretically grounded mechanism linking brain dynamics to the mechanisms behind cognitive and pathological states.

II. Brain Rhythm Identification via SyncBrain Traditional Kuramoto models represent each oscillator using a single scalar phase, which may oversimplify the complex and context-sensitive nature of neural dynamics. Such representations lack the flexibility to distinguish between different brain states or task conditions, limiting their effectiveness in cognitive decoding tasks.

To overcome this limitation, we introduce a vector-based Kuramoto model coupled with an adaptive control mechanism, as illustrated in Fig. 2. While the vector-based formulation retains rich multi-frequency features of neural oscillators, the adaptive control acts as a task-dependent feedback signal that modulates oscillator dynamics according to external demands. This design allows our SyncBrain to model brain synchronization not only as a passive emergent property, but also as an actively regulated process influenced by task- or disease-specific conditions. Together, these components enable the model to bridge high-dimensional brain rhythms with downstream cognitive or clinical outcomes.

Oscillator state representations. To construct the vectorbased oscillators, we draw inspiration from the geometric structure of brain networks and leverage the Geometric Scattering Transform (GST) (Gao, Wolf, and Hirn 2019). GST provides a principled way to extract multi-scale, multifrequency features from BOLD signals over time.

Concretely, GST builds harmonic wavelets using graph Laplacian, enabling the extraction of hierarchical representations {ˆxh(p)}H−1 h=0 across multiple diffusion scales. We begin by defining the lazy random walk matrix (Min, Wenkel, and Wolf 2020) as M = 1

2

IN + W D−1

, where IN is the identity matrix, W is the connectivity matrix, and D is the degree matrix with Dii = P j Wij. The wavelet operators at different scales are then recursively constructed as:

Ψ0:= IN −M, Ψh:= M 2h−1 −M 2h, 1 ≤h < H. (1) For each scale h, the transformed signal ˆxh(p) at time p is computed by: ˆxh(p) = Φ

Ψh x(p)

, where Φ:= M 2H acts as a low-pass filter. After applying GST, the neural signal at each region is represented as a matrix across scales and time points:

ˆX =

ˆx0, ˆx1,..., ˆxH−1

∈RN×P ×(H−1) (2) To define the oscillator state at brain region i, we flatten its multiscale time series into a vector ˆxi ∈RP (H−1), which

![Figure extracted from page 3](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-003-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

serves as the high-dimensional oscillator state. This formulation preserves rich temporal and spectral features, providing a unified feature representation.

Vector-Based Kuramoto Synchronization. To simulate the phase evolution of high-dimensional neural oscillators, we extend the classical Kuramoto model to a vector-based formulation. In this setting, the state of each oscillator ˆxi ∈ RP (H−1) evolves according to:

dˆxi dt = ωi +

N X j=1

Kij f(ˆxj, ˆxi), (3)

where ωi represents the intrinsic frequency vector of oscillator i, Kij is the learnable symmetric coupling strength between nodes i and j, and f(ˆxj, ˆxi) is a coupling function that encodes pairwise interactions.

To ground the dynamics in the structural or functional topology of the brain, we incorporate the connectivity matrix W = [wij] into the coupling function. Specifically, we define f

ˆxj, ˆxi

= wij ˆxj, such that each oscillator ˆxi is influenced by its neighbors proportionally to their connection strength. The aggregated effect of this interaction is captured by the matrix product (AW) ˆX, where A ∈RN×N is a learnable symmetric matrix that modulates the base connectivity W to form the effective coupling matrix K = AW.

Adaptive Memory Control Mechanism. While the vector-based Kuramoto model in Eq.(3) effectively captures synchronization dynamics, it lacks the capacity to incorporate transient memory mechanisms that are crucial for modeling functional fluctuations tied to cognitive processing. In the human brain, however, synchronization is not purely reactive, it is shaped by selective attention and memory systems that determine which neural patterns are retained and emphasized over time (Hutchinson and Turk-Browne 2012).

To incorporate this biological insight, we introduce an adaptive attending-memory control ˆyi into the vector-based Kuramoto framework. Derived from the initial embedding, this term allows each oscillator ˆxi to selectively modulate its future interactions based on relevant past neural activity. The resulting dynamics are governed by the following update:

dˆxi dt = ωi + β ˆyi +

N X j=1

Kij f

ˆxj, ˆxi

(4)

Here, the scalar coefficient β modulates the influence of the memory feedback ˆyi. A larger β increases the weight of historical information, while a smaller β promotes response to immediate dynamics. Thus, ˆyi is adaptively parameterized to enable dynamic control over the temporal extent of memory integration. By embedding such adaptive control into the oscillatory framework, our model inherits the nature of the attention-guided synchronization observed in biological neural systems (Liu, Slotine, and Barab´asi 2011).

Manifold-Constrained Projection. While the adaptive vector-based Kuramoto model enables each oscillator to evolve under both coupling and memory control, there remains a non-trivial challenge: without additional constraints, updates to each oscillator may be biased toward reinforcing its own current direction. This self-reinforcement can undermine synchronization, causing oscillators to resist aligning with others and thus compromising the emergence of coherent phase dynamics.

To address this, we introduce a geometric constraint (Chandra, Girvan, and Ott 2019) that forces each oscillator to update in a direction orthogonal to its current state. This ensures the update contributes to synchronization, rather than amplifying existing behavior. Specifically, let zi = βˆyi +

N X j=1

Kij f

ˆxj, ˆxi be the intermediate update direction for oscillator ˆxi, integrating both memory control and neighbor influences. We then compute the orthogonal component z⊥ i = zi − ⟨zi, ˆxi⟩ˆxi, where ⟨·, ·⟩denotes the standard inner product. This projected update ensures that the evolution of ˆxi aligns with relevant changes induced by neighboring oscillators and memory feedback, without collapsing onto itself.

By integrating all components discussed above, we now present an approach to predict the cognitive tasks/diseases based on neural oscillatory synchronization:

dˆxi dt = ωi + z⊥ i, (5)

which governs the evolution of each oscillator based on both intrinsic rhythm and extrinsic modulation.

To numerically implement this update, we adopt the following discretization with step size γ, followed by a normalization to constrain the updated oscillator to the unit sphere:

ˆx(l,t+1)

i = ˆx(l,t)

i + γ · dˆxi dt,

ˆx(l,t+1)

i ← ˆx(l,t+1)

i ∥ˆx(l,t+1)

i ∥

ˆyl i = ζ

˜x(l,T)

i

2 + b,

(6)

where t ∈[1, T] indicates the oscillation step, l ∈[1, L] denotes the model layer, and ˆyl i is the updated memory representation obtained after each full synchronization cycle via a transform function ζ (implemented as a 1-D convolution).

III. Integrating SyncBrain into Cognitive State Prediction and Disease Diagnosis SyncBrain takes the BOLD signals and structural/functional connectivity matrices as input. It first applies the Geometric Scattering Transform (GST), followed by an initial mapping (implemented as a fully connected layer) to generate the initial oscillator states ˆX and memory states ˆY, as illustrated in Fig. 2. These states then evolve according to the vector-based oscillatory synchronization dynamics defined in Eq. 4 and Eq. 5. At each synchronization step, the oscillator features are updated using Eq. 6, ultimately producing the final representations ˆX(L,T) and ˆY (L). These representations are used for downstream classification tasks, such as cognitive state decoding and neurological disease diagnosis, by minimizing the standard cross-entropy loss.

<!-- Page 5 -->

## Model

Metric(%) HCP-A HCP-YA HCP-WM ADNI OASIS PPMI NIFD

GCN

Acc 74.57±1.25 37.54±0.70 32.65±1.63 81.48±7.77 88.39±4.05 57.14±6.72 48.81±1.55 Pre 71.48±1.21 37.40±1.10 33.01±1.78 67.00±11.96 81.09±7.76 53.07±14.79 35.12±12.83 F1 71.78±1.81 36.09±0.78 32.25±1.53 73.38±10.56 83.40±5.66 49.51±5.19 32.52±1.33

GIN

Acc 72.28±0.85 35.17±1.55 33.16±2.67 79.26±6.46 88.12±4.24 62.39±5.71 49.90±1.97 Pre 69.74±0.80 36.34±1.88 33.40±3.01 74.76±7.32 79.99±7.04 62.53±4.57 42.33±6.13 F1 70.49±0.85 35.02±1.49 32.87±2.61 75.49±8.64 83.66±5.60 60.27±5.20 42.64±1.96

GAT

Acc 90.45±0.97 62.70±3.52 42.94±2.48 81.48±7.77 88.67±4.23 58.96±2.80 48.91±2.06 Pre 90.19±1.00 64.08±4.20 44.34±3.63 67.00±11.96 86.27±6.49 49.85±10.51 32.70±11.88 F1 90.12±1.03 62.36±3.56 42.54±2.26 73.38±10.56 84.06±5.91 50.56±4.78 32.57±2.67

GCNII

Acc 94.00±0.65 70.89±2.56 49.26±3.99 81.48±7.77 88.12±4.24 59.46±7.88 49.21±1.70 Pre 93.95±0.62 71.52±2.66 50.44±4.25 67.00±11.96 80.89±7.58 64.41±6.45 33.79±9.28 F1 93.92±0.65 70.84±2.70 48.79±4.10 73.38±10.56 82.84±5.93 55.55±7.84 33.71±2.54

GraphSAGE

Acc 94.20±0.84 74.16±2.43 53.46±3.26 82.22±6.37 88.12±4.24 61.83±3.50 49.21±1.49 Pre 94.15±0.89 74.87±2.30 54.22±3.42 74.00±4.84 80.89±7.58 42.50±11.29 44.63±3.87 F1 94.20±0.84 74.14±2.47 53.34±3.26 74.96±7.63 82.84±5.93 49.82±8.25 37.96±5.10

SAN

Acc 93.34±0.51 69.98±1.88 48.82±1.60 82.96±3.78 89.49±3.12 62.99±7.16 49.21±1.99 Pre 93.54±0.50 70.34±1.96 50.01±0.84 74.68±5.89 84.61±5.59 62.75±10.66 36.97±9.34 F1 93.34±0.51 69.85±1.99 48.41±1.33 77.10±3.78 85.95±3.99 61.47±8.92 34.05±3.01

GRAND

Acc 86.77±1.67 47.26±0.32 32.94±2.35 81.48±6.20 88.69±2.63 62.41±7.14 43.46±2.06 Pre 83.18±1.79 44.36±0.67 29.27±2.63 71.64±12.52 85.42±5.14 60.54±9.94 37.84±3.32 F1 86.96±1.06 46.98±0.71 34.43±1.09 74.49±8.83 84.75±3.31 59.99±9.42 38.38±2.62

GraphCON

Acc 93.32±0.45 70.45±1.48 55.33±0.54 82.96±5.54 88.41±2.49 60.12±2.04 48.31±1.35 Pre 91.34±0.52 67.04±1.97 52.29±0.83 77.35±9.67 80.33±4.60 44.98±9.41 30.49±7.78 F1 92.90±0.42 70.47±3.11 55.01±0.56 76.44±7.26 83.66±3.23 50.73±5.52 35.73±4.67

SyncBrain

Acc 95.55∗ ±0.77 85.20∗ ±1.60 89.22∗ ±1.72 83.05±8.28 89.30±4.27 63.12±4.59 82.27∗ ±6.42 Pre 95.57∗ ±0.77 85.53∗ ±1.73 89.66∗ ±1.49 71.06±15.14 81.62±8.11 63.10±15.61 82.76∗ ±5.78 F1 95.50∗ ±0.78 85.18∗ ±1.65 89.18∗ ±1.77 75.94±11.85 85.04±6.23 54.32±7.24 81.65∗ ±6.80

**Table 1.** Classification performance across 7 datasets using 9 baseline GNN models and SyncBrain. Bold indicates the best performance in each metric for a given dataset, while underline marks the second-best. (*) indicate that our model significantly outperforms all other baselines (paired t-test, p < 0.01).

## Experiments

In this section, we conduct extensive experiments to evaluate the performance of SyncBrain on two categories of fMRI datasets: (1) task-based fMRI data from the Human Connectome Project (HCP) and (2) resting-state fMRI data from disease-related cohorts. The implementation code and appendix are available at: https://github.com/jq-ding/AAAI26.

Datasets and Experimental Setup Datasets. For Task-based fMRI, we use three datasets from the Human Connectome Project (HCP): (i) HCP- Aging (HCP-A) (Bookheimer et al. 2019), which includes 4849 samples performing four cognitive tasks (VISMO- TOR, CARIT, FACENAME, and Resting State). (ii) HCP- Young Adults (HCP-YA) (Van Essen et al. 2013), which contains 1649 fMRI scans from seven cognitive tasks (Motor, Relational, Social, Working Memory, Language, Emotion, and Gambling). (iii) HCP-Working Memory (HCP- WM (Van Essen et al. 2013)), including 1360 samples alternating 2-back and 0-back conditions across four stimulus types (body, place, face, tool), thus includes eight classes in total. To evaluate the performance with respect to different brain parcellations, we use the Automated Anatomical Labeling (AAL) atlas (Tzourio-Mazoyer et al. 2002) to parcellate the fMRIs from HCP-A and HCP-YA into 116 regions and Brainnetome atlas (Fan et al. 2016) to parcellate the fM- RIs from HCP-WM into 246 regions.

Disease-related resting-state fMRI data includes the following public data cohorts: (i) Alzheimer’s Disease Neuroimaging Initiative (ADNI) (Petersen et al. 2010) includes 135 fMRI samples for individuals associated with Alzheimer’s disease (AD) or cognitively normal (CN). (ii) Open Access Series of Imaging Studies (OASIS) (LaMontagne et al. 2019) includes 362 samples from subjects diagnosed with AD or CN. (iii) Parkinson’s Progression Markers Initiative (PPMI)1 includes 173 samples with Parkinson’s disease, SWEDD(scans without evidence for dopaminergic deficit), Prodromal and healthy controls. (iv) Neuroimaging Initiative for Frontotemporal Lobar Degeneration (NIFD)2 focuses on frontotemporal dementia, including 1010 samples from individuals with cognitively normal (CON), lo-

1https://www.ppmi-info.org/ 2https://ida.loni.usc.edu/

<!-- Page 6 -->

Dataset # of samples # of class length # of ROIs

HCP-Aging 4,864 4 300 116 HCP-YA 1,649 7 175 116 HCP-WM 1,360 8 39 246 ADNI 135 2 140 116 OASIS 362 2 328 160 PPMI 173 4 239 116 NIFD 1,010 5 176 116

**Table 2.** The Summarization of Benchmarking Datasets.

gopenic variant of primary progressive aphasia (LPA), behavioral variant frontotemporal dementia (BV), progressive non-fluent aphasia (PNFA), and semantic variant (SV).

Experimental Setup. We compare SyncBrain with several widely used graph-based models in brain network analysis, including Graph Convolutional Networks (GCN) (Kipf and Welling 2016), Graph Isomorphism Networks (GIN) (Xu et al. 2018), Graph Attention Networks (GAT) (Veliˇckovi´c et al. 2017), GCNII (Chen et al. 2020), GraphSAGE (Hamilton, Ying, and Leskovec 2017), and the graph transformer with Spectral Attention Network (SAN) (Kreuzer et al. 2021). We also include PDE-based models such as GRAND (Chamberlain et al. 2021) and GraphCON (Rusch et al. 2022).

For SyncBrain, we set step size γ = 1, and the scalar coefficient β controlling the memory strength is a learnable parameter. To ensure fair comparison, all models are trained using five-fold cross-validation, and we report three evaluation metrics: accuracy (Acc), weighted precision (Pre), and weighted F1 score (F1). The training settings are as follows: hidden dimension is 256; the number of layers is 2 for GCN and GAT, and 4 for other models; each model is trained for 1500 epochs with a learning rate ranging from 5 × 10−4 to 1 × 10−3 and a weight decay of 5 × 10−4.

Performance and Discussion on Brain States Identification and Disease Diagnosis

All quantitative comparison results are summarized in Table 1. Across the seven fMRI datasets, SyncBrain almost consistently achieves the highest accuracy, precision, and F1-score among all evaluated GNN-based baselines, highlighting its strong generalization ability and robustness to diverse brain decoding tasks.

The performance gap is particularly pronounced on the more challenging datasets, such as HCP-WM and NIFD. For example, on HCP-WM, SyncBrain achieves an accuracy of 89.22%, substantially outperforming all other baselines. Similar trends are observed on NIFD, where SyncBrain reaches 82.27% accuracy compared to 49.9% for the second-best GIN. These results suggest that SyncBrain is especially effective in scenarios where traditional message passing struggles to model cognitive states with subtle and distributed neural patterns, such as working memory (HCP-WM) or neurodegeneration (NIFD). Specifically, shared structural connectivity across tasks limits GNNs relying on fixed message passing, whereas in NIFD, long-range disconnections challenge local information exchange. Moreover, statistical significance (p < 0.01) confirms that the improvements achieved by SyncBrain are statistically significant and robust across folds. These findings collectively emphasize that integrating oscillator dynamics and neurobiologically informed synchronization mechanisms enables more stable, accurate, and interpretable decoding of taskor disease-specific brain activity patterns, surpassing the limitations of conventional GNN architectures that operate solely on static graph topologies (Veliˇckovi´c et al. 2017).

Interpretable Oscillatory Representations: Phase Dynamics and Spatial Patterns

Phase-space trajectories reveal class-specific neural synchronization patterns. To gain deeper insights into how SyncBrain organizes brain representations, we visualize the evolution of feature embeddings across synchronization steps, as illustrated in Fig. 3. Specifically, we extract the initial representations ˆX(0,0) and ˆY (0), along with the intermediate transformed states ˆX(0,1), ˆX(0,2),..., ˆX(L,T), and project them onto a circular phase space, where each point is colored by its corresponding class label. The HCP-A dataset (top) and the NIFD dataset (bottom) are shown to illustrate both cognitive task-related and disease-related scenarios.

HCP-A VISMOTOR FACENAME CARIT REST

NIFD PNFA BV L_SD CON SV

𝑿

(0,0) 𝒀(0) 𝑿(0,1) 𝑿(0,2) 𝑿(0,3) 𝑿(L, T) …

**Figure 3.** Phase space visualization of the learned representations of SyncBrain from the initial input ˆX(0,0) to the final output ˆX(L,T). Points are colored by cognitive task labels for the HCP-A (top) and NIFD (bottom). SyncBrain is able to organize representations into well-separated manifolds aligned with task categories.

As the synchronization dynamics evolve, we observe that samples belonging to the same class progressively converge toward compact clusters along specific phase regions. This behavior is especially prominent in the final states ˆX(L,T), where the manifolds become well-separated and exhibit clear angular alignment. Such a trajectory from chaotic to synchronized states suggests that the coupling and adaptive memory mechanisms in SyncBrain effectively capture class-specific oscillatory patterns and differentiate them in the latent phase domain.

From a neuroscience perspective, this clustering can be

<!-- Page 7 -->

interpreted as a representation of neural synchronization: brain regions engaged in the same cognitive or pathological state tend to exhibit phase-locked oscillations, forming stable manifolds that encode task-specific or disease-specific dynamics (Buzsaki 2006). These visualizations highlight that SyncBrain organizes neural fluctuations into discriminative representations aligned with underlying brain states.

Disease-relevant brain region identification. To better interpret the spatial distribution of disease-relevant neural alterations, we visualize the top 10 most central brain regions for each neurodegenerative disease dataset (ADNI, PPMI, and NIFD) using degree centrality scores derived from the weights represented by K in Eq.4. We mapped the top 10 ROIs with the highest centrality scores (larger spheres) onto the cortical surface where colors represent their corresponding functional subnetworks using NeuroMArVL toolbox3.

ADNI PPMI NIFD

Frontoparietal Visual

Default Mode Ventral Attention

Sensorimotor Cerebellum

**Figure 4.** Top 10 most important brain regions (larger spheres) identified by our model for three neurodegenerative disease datasets: ADNI, PPMI, and NIFD. Regions are color-coded according to their associated functional networks. The selected regions align well with known neuropathological patterns reported in neuroscience.

The visualization highlights consistent and biologically meaningful patterns across datasets. In ADNI, which focuses on Alzheimer’s disease, our model identifies regions within the default mode network (DMN) and ventral attention network, which are known to be disrupted in early Alzheimer’s pathology (Greicius et al. 2004). In PPMI, targeting Parkinson’s disease, sensorimotor and cerebellum regions are frequently selected, aligning with known impairments in motor circuitry (Wu et al. 2009; Helmich et al. 2012). Finally, in NIFD, the selected regions primarily lie in the frontoparietal and ventral attention networks, both of which are associated with the executive and socioemotional deficits characteristic of frontotemporal dementia (FTD) (Seeley et al. 2009; Rosen et al. 2005). This alignment with established neuroanatomical findings provides strong evidence that our model not only performs accurate classification but also reveals interpretable biomarkers that map meaningfully to disease mechanisms.

Comparison of inference efficiency Table 3 reports the average per-subject inference time (in ms) for all baseline models and SyncBrain on three largescale datasets: HCP-A (4,864 samples), HCP-YA, and HCP-

3https://immersive.erc.monash.edu/neuromarvl/

WM (which has larger coupling matrices of size 264 × 264). This analysis is crucial for assessing the practical deployment potential of our method, especially given that SyncBrain introduces a more sophisticated oscillatorbased dynamic mechanism.

GCN GIN GAT GCNII SAGE SAN GRAND GraphCON Ours

HCP-A 0.66 0.58 0.86 0.82 0.57 1.02 11.39 0.91 1.02 HCP-YA 0.63 0.55 0.81 0.70 0.54 1.02 10.99 0.95 1.17 HCP-WM 1.41 1.09 2.24 1.74 1.05 2.81 74.21 1.47 1.56

Avg 0.9 0.74 1.31 1.09 0.72 1.62 32.2 1.11 1.25

**Table 3.** Inference time (ms/subject) on HCP-A, HCP- YA, and HCP-WM. SyncBrain achieves competitive efficiency compared to baseline models.

Despite the additional complexity from simulating synchronization dynamics, SyncBrain maintains competitive inference efficiency across all datasets. Specifically, the average inference time of SyncBrain is 1.25 ms, which is comparable to most traditional GNNs (e.g., GAT: 1.31 ms, GCNII: 1.09 ms), and significantly faster than PDE-based methods such as GRAND (32.2 ms). This highlights that our model’s biological plausibility does not come at the cost of computational burden.

On more challenging dataset HCP-WM with larger connectivity matrices, SyncBrain only incurs a moderate computational increase (1.56 ms), while GRAND suffer a drastic slowdown (74.21 ms). SyncBrain avoids the deep diffusion simulation overheads typically found in continuous-time or PDE-based approaches, making it wellsuited for large-scale neuroimaging applications.

## Conclusion

and Discussion

In this paper, we proposed SyncBrain, a physicsinformed deep model for modeling functional dynamics that is principled by the neural oscillatory synchronization widely studied in neuroscience. Across both task-based and disease-based fMRI datasets, our model outperforms GNN baselines, demonstrating robust classification. Visualization results further confirm that SyncBrain organizes features into meaningful phase-aligned clusters and a neuroscientifically meaningful spatial pattern. Our findings suggest that SyncBrain offers a promising new perspective for understanding cognitive and pathological brain states.

Despite the promising performance and biological interpretability of SyncBrain, several limitations merit further investigation. On one hand, SyncBrain integrates structural/functional connectivity as static graphs, incorporating dynamic graph structures might provide a more faithful characterization of transient neural interactions. On the other hand, while we demonstrate generalizability across multiple datasets, cross-site variability and scanner differences may still pose challenges for large-scale deployment, we would consider these factors in future work.

![Figure extracted from page 7](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-syncbrain-exploring-brain-functional-dynamics-through-neural-oscillatory-synchro/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

## Acknowledgements

This work was supported by the National Institutes of Health (AG091653, AG068399, AG084375) and the Foundation of Hope. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the NIH.

## References

Abdelnour, F.; Voss, H.; and Raj, A. 2014. Network diffusion accurately models the relationship between structural and functional brain connectivity networks. NeuroImage, 90: 335–347.

Amari, S.-I.; and Arbib, M. A. 1977. Competition and cooperation in neural nets. Systems neuroscience, 119–165.

Becker, C. O.; Pequito, S.; Bajaj, S.; Pappas, G. J.; Jayaram, V.; Sporns, O.; Vettel, J. M.; and Pasqualetti, F. 2018. Spectral mapping of brain functional connectivity from diffusion imaging. Scientific Reports, 8(1): 1411.

Bookheimer, S. Y.; Salat, D. H.; Terpstra, M.; Ances, B. M.; Barch, D. M.; Buckner, R. L.; Burgess, G. C.; Curtiss, S. W.; Diaz-Santos, M.; Elam, J. S.; et al. 2019. The lifespan human connectome project in aging: an overview. Neuroimage, 185: 335–348.

Breakspear, M.; Heitmann, S.; and Daffertshofer, A. 2010. Generative models of cortical oscillations: neurobiological implications of the Kuramoto model. Frontiers in Human Neuroscience, 4: 190.

Buzsaki, G. 2006. Rhythms of the Brain.

Cabral, J.; Hugues, E.; Sporns, O.; and Deco, G. 2011. Role of local network oscillations in resting-state functional connectivity. Neuroimage, 57(1): 130–139.

Chamberlain, B.; Rowbottom, J.; Gorinova, M. I.; Bronstein, M.; Webb, S.; and Rossi, E. 2021. Grand: Graph neural diffusion. In International Conference on Machine Learning, 1407–1418. PMLR.

Chandra, S.; Girvan, M.; and Ott, E. 2019. Continuous versus Discontinuous Transitions in the D-Dimensional Generalized Kuramoto Model: Odd D is Different. Physical Review. X, 9(1).

Chen, M.; Wei, Z.; Huang, Z.; Ding, B.; and Li, Y. 2020. Simple and deep graph convolutional networks. In International Conference on Machine Learning, 1725–1735. PMLR.

Chow, C.; Dan, T.; Styner, M.; and Wu, G. 2024. Understanding Brain Dynamics Through Neural Koopman Operator with Structure-Function Coupling. In International Conference on Medical Image Computing and Computer- Assisted Intervention, 509–518. Springer.

Cui, H.; Dai, W.; Zhu, Y.; Kan, X.; Gu, A. A. C.; Lukemire, J.; Zhan, L.; He, L.; Guo, Y.; and Yang, C. 2022. Braingb: a benchmark for brain network analysis with graph neural networks. IEEE transactions on medical imaging, 42(2): 493–506.

Dan, T.; Kim, M.; Kim, W. H.; and Wu, G. 2023. Uncovering Structural-Functional Coupling Alterations for Neurodegenerative Diseases. In International Conference on Medical Image Computing and Computer-Assisted Intervention, 87–96. Springer. Deco, G.; Kringelbach, M. L.; Jirsa, V. K.; and Ritter, P. 2017. The dynamics of resting fluctuations in the brain: metastability and its dynamical cortical core. Scientific Reports, 7(1): 3095. Fan, L.; Li, H.; Zhuo, J.; Zhang, Y.; Wang, J.; Chen, L.; Yang, Z.; Chu, C.; Xie, S.; Laird, A. R.; et al. 2016. The human brainnetome atlas: a new brain atlas based on connectional architecture. Cerebral Cortex, 26(8): 3508–3526. Finn, E. S.; Shen, X.; Scheinost, D.; Rosenberg, M. D.; Huang, J.; Chun, M. M.; Papademetris, X.; and Constable, R. T. 2015. Functional connectome fingerprinting: identifying individuals using patterns of brain connectivity. Nature Neuroscience, 18(11): 1664–1671. Gallos, I. K.; Lehmberg, D.; Dietrich, F.; and Siettos, C. 2024. Data-driven modelling of brain activity using neural networks, diffusion maps, and the Koopman operator. Chaos: An Interdisciplinary Journal of Nonlinear Science, 34(1). Gao, F.; Wolf, G.; and Hirn, M. 2019. Geometric scattering for graph data analysis. In International Conference on Machine Learning, 2122–2131. PMLR. Ghazanfar, A. A.; and Lewkowicz, D. J. 2009. The emergence of multisensory systems through perceptual narrowing. Trends in Cognitive Sciences, 13(11): 470–478. Greicius, M. D.; Srivastava, G.; Reiss, A. L.; and Menon, V. 2004. Default-mode network activity distinguishes Alzheimer’s disease from healthy aging: evidence from functional MRI. Proceedings of the National Academy of Sciences, 101(13): 4637–4642. Hamilton, W.; Ying, Z.; and Leskovec, J. 2017. Inductive representation learning on large graphs. Advances in neural information processing systems, 30. Hayat, M.; and Aramvith, S. 2024. Transformer’s role in brain MRI: a scoping review. IEEE Access. Helmich, R. C.; Hallett, M.; Deuschl, G.; Toni, I.; and Bloem, B. R. 2012. Cerebral causes and consequences of parkinsonian resting tremor: a tale of two circuits? Brain, 135(11): 3206–3226. Honey, C. J.; Sporns, O.; Cammoun, L.; Gigandet, X.; Thiran, J.-P.; Meuli, R.; and Hagmann, P. 2009. Predicting human resting-state functional connectivity from structural connectivity. Proceedings of the National Academy of Sciences, 106(6): 2035–2040. Hubel, D. H.; and Wiesel, T. N. 1962. Receptive fields, binocular interaction and functional architecture in the cat’s visual cortex. The Journal of physiology, 160(1): 106. Hutchinson, J. B.; and Turk-Browne, N. B. 2012. Memoryguided attention: control from multiple memory systems. Trends in Cognitive Sciences, 16(12): 576–579. Khosla, M.; Jamison, K.; Ngo, G. H.; Kuceyeski, A.; and Sabuncu, M. R. 2019. Machine learning in resting-state fMRI analysis. Magnetic resonance imaging, 64: 101–121.

<!-- Page 9 -->

Kipf, T. N.; and Welling, M. 2016. Semi-supervised classification with graph convolutional networks. arXiv preprint arXiv:1609.02907. Kreuzer, D.; Beaini, D.; Hamilton, W.; L´etourneau, V.; and Tossou, P. 2021. Rethinking graph transformers with spectral attention. Advances in Neural Information Processing Systems, 34: 21618–21629. Ktena, S. I.; Parisot, S.; Ferrante, E.; Rajchl, M.; Lee, M.; Glocker, B.; and Rueckert, D. 2018. Metric learning with spectral graph convolutions on brain connectivity networks. NeuroImage, 169: 431–442. Kuramoto, Y. 1975. Self-entrainment of a population of coupled non-linear oscillators. In International Symposium on Mathematical Problems in Theoretical Physics: January 23–29, 1975, Kyoto University, Kyoto/Japan, 420–422. Springer. Kuramoto, Y. 1984. Chemical Turbulence, 111–140. Berlin, Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-642- 69689-3. LaMontagne, P. J.; Benzinger, T. L.; Morris, J. C.; Keefe, S.; Hornbeck, R.; Xiong, C.; Grant, E.; Hassenstab, J.; Moulder, K.; Vlassenko, A. G.; et al. 2019. OASIS-3: longitudinal neuroimaging, clinical, and cognitive dataset for normal aging and Alzheimer disease. MedRxiv, 2019–12. Li, H.; and Fan, Y. 2018. Brain decoding from functional MRI using long short-term memory recurrent neural networks. In International conference on medical image computing and computer-assisted intervention, 320– 328. Springer. Li, X.; Zhou, Y.; Dvornek, N.; Zhang, M.; Gao, S.; Zhuang, J.; Scheinost, D.; Staib, L. H.; Ventola, P.; and Duncan, J. S. 2021. Braingnn: Interpretable brain graph neural network for fmri analysis. Medical Image Analysis, 74: 102233. Liu, Y.-Y.; Slotine, J.-J.; and Barab´asi, A.-L. 2011. Controllability of complex networks. nature, 473(7346): 167–173. Min, Y.; Wenkel, F.; and Wolf, G. 2020. Scattering gcn: Overcoming oversmoothness in graph convolutional networks. Advances in neural information processing systems, 33: 14498–14508. Mitchell, T. M.; Hutchinson, R.; Niculescu, R. S.; Pereira, F.; Wang, X.; Just, M. A.; and Newman, S. D. 2004. Learning to Decode Cognitive States from Brain Images. Machine Learning, 57(1–2): 145–175. Miyato, T.; L¨owe, S.; Geiger, A.; and Welling, M. 2024. Artificial Kuramoto Oscillatory Neurons. arXiv preprint arXiv:2410.13821. Mountcastle, V. B. 1997. The columnar organization of the neocortex. Brain: a journal of neurology, 120(4): 701–722. Nguyen, T.; Honda, H.; Sano, T.; Nguyen, V.; Nakamura, S.; and Nguyen, T. M. 2024. From coupled oscillators to graph neural networks: Reducing over-smoothing via a kuramoto model-based approach. In International Conference on Artificial Intelligence and Statistics, 2710–2718. PMLR. Notbohm, A.; Kurths, J.; and Herrmann, C. S. 2012. The firefly model of synchronization through cross-frequency coupling. PLOS ONE, 7(9): e45630.

Pereira, F.; Mitchell, T.; and Botvinick, M. 2009. Machine learning classifiers and fMRI: a tutorial overview. Neuroimage, 45(1): S199–S209. Petersen, R. C.; Aisen, P. S.; Beckett, L. A.; Donohue, M. C.; Gamst, A. C.; Harvey, D. J.; Jack Jr, C.; Jagust, W. J.; Shaw, L. M.; Toga, A. W.; et al. 2010. Alzheimer’s disease neuroimaging initiative (ADNI) clinical characterization. Neurology, 74(3): 201–209. Rosen, H. J.; Allison, S. C.; Schauer, G. F.; Gorno-Tempini, M. L.; Weiner, M. W.; and Miller, B. L. 2005. Neuroanatomical correlates of behavioural disorders in dementia. Brain, 128(11): 2612–2625. Rusch, T. K.; Chamberlain, B.; Rowbottom, J.; Mishra, S.; and Bronstein, M. 2022. Graph-coupled oscillator networks. In International Conference on Machine Learning, 18888– 18909. PMLR. Seeley, W. W.; Crawford, R. K.; Zhou, J.; Miller, B. L.; and Greicius, M. D. 2009. Neurodegenerative diseases target large-scale human brain networks. Neuron, 62(1): 42–52. Siegel, M.; Donner, T. H.; and Engel, A. K. 2012. Spectral fingerprints of large-scale neuronal interactions. Nature Reviews Neuroscience, 13(2): 121–134. Tzourio-Mazoyer, N.; Landeau, B.; Papathanassiou, D.; Crivello, F.; Etard, O.; Delcroix, N.; Mazoyer, B.; and Joliot, M. 2002. Automated anatomical labeling of activations in SPM using a macroscopic anatomical parcellation of the MNI MRI single-subject brain. Neuroimage, 15(1): 273– 289. Van Atteveldt, N.; Murray, M. M.; Thut, G.; and Schroeder, C. E. 2014. Multisensory integration: flexible use of general operations. Neuron, 81(6): 1240–1253. Van Essen, D. C.; Smith, S. M.; Barch, D. M.; Behrens, T. E.; Yacoub, E.; and Ugurbil, K. 2013. The WU-Minn Human Connectome Project: An overview. NeuroImage, 80: 62–79. Varela, F.; Lachaux, J.-P.; Rodriguez, E.; and Martinerie, J. 2001. The brainweb: phase synchronization and large-scale integration. Nature reviews neuroscience, 2(4): 229–239. Veliˇckovi´c, P.; Cucurull, G.; Casanova, A.; Romero, A.; Lio, P.; and Bengio, Y. 2017. Graph attention networks. arXiv preprint arXiv:1710.10903. Wee, C.-Y.; Yap, P.-T.; Zhang, D.; Denny, K.; Browndyke, J. N.; Potter, G. G.; Welsh-Bohmer, K. A.; Wang, L.; and Shen, D. 2012. Identification of MCI individuals using structural and functional connectivity networks. Neuroimage, 59(3): 2045–2056. Wu, T.; Wang, L.; Chen, Y.; Zhao, C.; Li, K.; and Chan, P. 2009. Changes of functional connectivity of the motor network in the resting state in Parkinson’s disease. Neuroscience letters, 460(1): 6–10. Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S. 2018. How powerful are graph neural networks? arXiv preprint arXiv:1810.00826. Zhang, H.; Zhang, H.; and Wu, G. 2022. Functional Connectivity Prediction from Structural Connectome using Deep Neural Network with Graph Representation. Medical Image Analysis, 75: 102289.
