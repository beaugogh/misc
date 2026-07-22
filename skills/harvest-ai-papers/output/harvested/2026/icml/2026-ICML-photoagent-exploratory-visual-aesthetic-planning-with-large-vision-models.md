---
title: "PhotoAgent: Exploratory Visual Aesthetic Planning with Large Vision Models"
source_url: https://icml.cc/virtual/2026/oral/71050
paper_pdf_url: https://arxiv.org/pdf/2602.22809v3
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# PhotoAgent: Exploratory Visual Aesthetic Planning with Large Vision Models

<!-- Page 1 -->

PhotoAgent: Exploratory Visual Aesthetic Planning with Large Vision Models

Mingde Yao1,5, Zhiyuan You1, King-Man Tam4, Menglu Wang3, Tianfan Xue1,2,5

1MMLab, CUHK 2Shanghai AI Lab 3USTC 4Institute of Science Tokyo 5CPII under InnoHK mingdeyao@foxmail.com tfxue@ie.cuhk.edu.hk

## Abstract

With the recent fast development of generative models, instruction-based image editing has shown great potential in generating high-quality images. However, the quality of editing highly depends on carefully designed instructions, placing the burden of task decomposition and sequencing entirely on the user. To achieve autonomous image editing, we present PhotoAgent, a system that advances image editing through explicit aesthetic planning. Specifically, PhotoAgent formulates autonomous image editing as a long-horizon decision-making problem. It reasons over user aesthetic intent, plans multi-step editing actions via tree search, and iteratively refines results through closedloop execution with memory and visual feedback, without requiring step-by-step user prompts. To support reliable evaluation in real-world scenarios, we introduce UGC- Edit, an aesthetic evaluation benchmark consisting of 7,000 photos and a learned aesthetic reward model. We also construct a test set containing 1,017 photos to systematically assess autonomous photo editing performance. Extensive experiments demonstrate that PhotoAgent consistently improves both instruction adherence and visual quality compared with baseline methods. The project page is https://mdyao.github.io/PhotoAgent.

## 1. Introduction

Recent instruction-based image editing models (Instruct- Pix2Pix [5], SDXL [29], SD [32], GPT-4o [28], Flux.1 kontext [19], Bagel [12], etc.) enable amateur users to achieve professional photo edits through natural language commands (e.g., remove the passersby), rather than solely manipulating low-level sliders (e.g., brightness and color). This shift broadens the scope of computational photography, moving beyond fidelity to the captured scene toward fidelity to the user’s aesthetic intent, thereby democratizing powerful photographic expression [23, 39].

Despite these advances, a critical bottleneck remains: these powerful models fundamentally rely on continuous user involvement, as shown in Fig. 1. Their effectiveness largely depends on the user’s ability to design precise and sequential instructions, which is difficult for amateur users. This reliance introduces several fundamental limitations: (1) Expertise barrier: Effective interaction requires expert knowledge. Amateur users often struggle either with designing articulate and precise editing instructions (e.g., decomposing “make my photo better” into detailed steps) or with evaluating whether editing results meet professional quality standards. (2) Algorithm selection: Different editing tasks require different specialized models. A single model may not be sufficient for all tasks, so users need to switch between models to achieve the desired results. (3) Interaction complexity: These models often require users, even professional ones, to issue multiple iterative commands, which is inherently time-consuming and prevents full automation for batch processing.

We argue that the next frontier in computational photography is not merely a single powerful editor or processor [5] [17] [39] [23], but an autonomous editing agent that can enhance photos without requiring expert-level operation. Such an agent would emulate the decision-making process of a human photo editor, who strategically selects and sequences tools based on an assessment of the image’s needs, and edits with specific tools. Recently, large vision and multimodal models (LVMs) [12] [22] [5] [39] have demonstrated remarkable perception and instructionconditioned editing capabilities, making an autonomous editing agent feasible.

In this paper, we introduce PhotoAgent, a novel autonomous system that integrates large vision and multimodal models (LVMs) with a suite of editing tools into a coherent framework, enabling fully automated, high-quality photo editing. As illustrated in Fig. 1, PhotoAgent introduces exploratory visual aesthetic planning within a closed-loop framework. Unlike open-loop systems (e.g., GenArtist [41]) that execute linear action sequences without feedback, PhotoAgent continuously evaluates its edits and strategically explores the editing space. This helps to avoid both short-sighted decisions and irrecoverable arti- arXiv:2602.22809v3 [cs.CV] 16 Jul 2026

<!-- Page 2 -->

I don’t know how to make it beautiful.

I need some experts:

I don’t know how to select algorithm to edit it.

I am so tired. I have worked for four hours.

Expertise Barrier

## Algorithm

Selection

Interaction Complexity

People-loop paradigm

Edit

Evaluate

Agent-loop paradigm

P er ce iv er

、

（

Qw en3

-V

L）

(1) Remove the person on the right side of the image.

(2) Crop the image to focus only on the central object.

(k) Replace the plain sky with the dramatic sunset.

PhotoAgent

P l a n n e r

（

M

C

T

S

）

Ex ec ut or

(

I ns tr uct

Pix

2Pi x,

FL

U

X

)

E va lu at o r

(

C

L

I

P

,

L

A

I

O

N,

Im ag e

R e w a r d

）

(1) Increase image saturation and brightness to make the colors more vivid.

(2)Add fluffy white clouds in the sky area.

(N) Change the color of the car in the foreground from red to blue.

Edited Image

…

…

…

Scoret: 4.7

Top-k Actions

Send edited image to next loop

Scoret > Scoret-1?

Yes!

N Candidate Actions

No! Rollback to t-th loop

1

3

4

Input Output

Fully autonomous editing without any manual intervention.

**Figure 1.** PhotoAgent autonomously performs high-level, semantically meaningful edits aligned with human aesthetic, moving beyond low-level color, contrast, or illumination tweaks. Upper-Left: People-loop, where users iteratively inspect the image, propose edits, and apply changes until satisfied. Upper-Right: PhotoAgent, where the process runs autonomously. Bottom: Edited photos. Note that PhotoAgent also supports user-guided editing (Fig. 6).

facts that commonly happen in greedy approaches, enabling coherent and high-quality results. In addition, PhotoAgent enables context editing, moving beyond the low-level adjustments (e.g., color, contrast, illumination) that existing photo-editing agents primarily perform [14, 21, 50]. This is achieved through programmatic control over a rich library of editing actions and flexible editing tools, enabling semantically meaningful manipulations such as adding a sun to a dim sky, making the scene feel more vibrant and lively, or modifying objects in the scene.

To achieve this, PhotoAgent consists of four core components: a perceiver, a planner, an executor, and an evaluator. The process begins with a VLM-based perceiver (e.g., Qwen3-VL [2]) that interprets the input image and produces a set of semantically meaningful editing actions. These candidate actions are then passed to a Monte Carlo Tree Search (MCTS)-based planner [8] [6], which explores possible editing trajectories in a tree structure and selects the top-K most promising actions. This exploratory mechanism ensures that our system embodies exploratory visual aesthetic planning, avoiding myopic decisions. The selected actions are subsequently executed using either advanced image generation tools (e.g., Flux.1 Kontext [19]) or traditional image processing libraries (e.g., OpenCV/PIL [4]). Finally, the evaluator integrates feedback from multiple scoring modules, allowing only those actions that positively contribute to the image’s aesthetic quality to pass. By iterating through this perceive–plan–execute–evaluate cycle, PhotoAgent forms a fully closed-loop process, enabling autonomous and reliable progress toward the final editing goal.

Additionally, one major challenge in this design is that existing image quality evaluation methods are insufficient for user-driven photo editing, also referred to as usergenerated content (UGC). The core issue lies in the composition of existing datasets, where existing datasets are overly generic, containing AI-generated images, screenshots, advertisements, and posters, rather than authentic user-captured photographs. To address this, we introduce UGC-Edit, a dataset of 7,000 real user photos annotated with human aesthetic scores. We also train a reward model on UGC-Edit, enabling reliable evaluation of aesthetic quality for multi-step image editing. Finally, to comprehensively evaluate the editing, we construct a test set of real

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-28.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-30.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-32.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-33.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-35.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-002-figure-36.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

photographs consisting of 1,017 images, on which our system achieves state-of-the-art results across quantitative metrics, qualitative assessment, and user studies.

In summary, this work makes the following contributions: • We propose PhotoAgent, an autonomous editing system that integrates a closed-loop architecture with a suite of editing and evaluation tools, enabling robust multi-step editing. • We introduce a visual aesthetic planner to explore sequences of editing actions over long horizons, enabling deliberate, goal-driven image editing. • We present the UGC-Edit dataset and introduce a reward model to support aesthetic research in autonomous image editing. We also introduce a test set of real photographs for evaluating autonomous photo editing. • Extensive experiments demonstrate that our complete system achieves significant improvements in editing quality.

## 2. Related Work

Image Editing Early pioneering works primarily leverage Generative Adversarial Networks (GANs) [15] or conditional encoder-decoder architectures for tasks like style transfer and attribute manipulation. For example, Cycle- GAN [49] proposes unpaired image-to-image (I2I) translation, and StarGAN [10] enables multi-attribute manipulation within a single model. However, these approaches are inherently limited since their editing capabilities are confined to the narrow distribution of their training data, which often struggle with open-vocabulary requests. They frequently produce low-resolution or artifact-ridden outputs.

A paradigm shift was ushered in by the advent of powerful diffusion models [27, 42] and their integration with natural language. Models like Stable Diffusion [1] treat image editing as conditional image generation, where the input image serves as a foundational condition. Recent methods (e.g., Prompt-to-Prompt [17], InstructPix2Pix [5]) manipulate the features in latent space to enable highly flexible editing following open-vocabulary instructions. This progress continues with next-generation architectures based on flow matching (e.g., Flux [19]) and the integration of powerful Multimodal Large Language Models (MLLMs) like GPT-4o [28], Show-o [43], Bagel [12], Nano Banana [16] and HunyuanImage-3.0 [7], which aim to tightly couple reasoning and generation. Despite these remarkable advances, a critical limitation exists. These models act primarily as single-step, static executors. Their performance is highly sensitive to meticulously engineered, low-level prompts, placing the burden of designing instructions and evaluations on the amateur user. These limitations prevent the method from handling complex, autonomous multi-step editing tasks, highlighting the need for a higher- level, planning-based framework.

Planning with Autonomous Agents To overcome the above limitations, a promising direction is to design an autonomous agent framework capable of multi-step planning and execution. Early works such as AlphaGo [37] employ planning algorithms like Monte Carlo Tree Search (MCTS) to navigate state spaces. Recently, LLM-based agents leverage LLM’s reasoning capability to decompose tasks into sequences of actions (e.g., HuggingGPT [35], ReAct [46], and Voyager [38]).

Within computer vision, works have explored integrating planning into image editing tasks. Some approaches, such as JarvisArt [23], MonetGPT [14], and PhotoArtAgent [9] leverage an LLM as a planner to parse a complex instruction into a sequence of calls to specialized image processing software. However, existing methods mainly focus on low-level editing tasks, such as color, tone, or exposure adjustments using procedural software tools like Lightroom or GIMP, which are limited to pure retouching.

More recent researches begin to explore directly applying MCTS and other search strategies to the text-to-image (T2I) generation process itself, building a search tree in the latent or textual space to find sequences of actions that better satisfy a high-level goal [36]. However, existing methods [14, 21, 50] have no planning capability for instructionbased image editing. Our approach addresses this through an MCTS planner that considers internal simulation with external execution. We also employ a learned reward model trained on user preferences to guide the search. This combination enables robust planning with a diverse toolset and is supported by a new editing-specific benchmark for evaluation.

Image Evaluation In an automated image editing pipeline, the evaluator is important, as it defines the reward function that guides the agent’s actions and determines the final output. Traditional full-reference image quality metrics, such as Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) [40], are not suited for this open-world setting. They require a ground-truth target image, which is obviously impossible for creative editing tasks.

The community then turns to no-reference metrics, including distribution-based measures like Fr´echet Inception Distance (FID) [18], aesthetic predictors [13], or CLIPbased image-text alignment scores [31]. While a step forward, these metrics are often too broad to provide reliable, fine-grained signals for specific editing tasks on usergenerated content (UGC). They cannot capture the subtle quality differences that are crucial in specific image editing tasks, such as aesthetic-oriented editing. To address this limitation, we introduce a specialized UGC evaluation dataset and train a reward model on the dataset. The reward model is adopted from a pretrained vision-language model

<!-- Page 4 -->

Output

1

2

N

… e.g. Depth=3

Score: 3.9

…

Score: 4.2

Score: 3.7

Lightweight Loop

Main Loop: 1, 2, …,t, …, T

Nano Banana

Crop Flip Rotate

Flux Diffusion GPT-4o

Show-o Bagel

{Action: i➙j➙k}

Light Executors

Light Evaluate

Edited image

P r o c e e d to th e ne x t l o o p

Perceiver

VLM models N Candidate Actions

Increase brightness to make colors more vivid. Add fluffy white clouds.

Change the color of the car.

Planner (search by MCTS)

Top-K Actions（K=3） Crop the image to focus on object.

Increase brightness to make colors more vivid.

Change the color of the car.

3

1

N

Executor

Basic Tools

AI Tools

Evaluator

CLIP

LAION

ImageReward UGC Evaluator

Image

LR image

Record Score[i][j][k]

Edited image

Rollback

Edited image

Score↑?

User-guided Editing

Enhance this image

PhotoAgent

(Optional)

k i j

… … …

… …

…

1

N

3 2

## 3 N 2

N

2 N-1 … … …

…

2

N

3 1

## 3 N 1

N

1 N-1 … … …

…

3

3

N

2 1

## 2 N 1

N

1 N-1 … … …

…

2

3

N

2 1

2 1 1 N-2 … … …

… N-1

N-1 N-1

**Figure 2.** Detailed loop of PhotoAgent. First, Perceiver extracts semantic cues from the current image and proposes N candidate editing actions. Second, Planner explores the candidate actions through iterative rollouts, scoring, and pruning to progressively refine edits and select the action that achieves the optimal result. Then, the executor applies these edits while the evaluator scores intermediate results, invoking re-planning when the score is unsatisfactory.

(VLM) that contains inherent knowledge. The dataset and model enable learning of aesthetic evaluation, providing precise feedback to guide the agent toward high-quality results.

## 3. PhotoAgent

We propose PhotoAgent, an autonomous image editing system capable of executing multi-step editing tasks through a structured, closed-loop framework. As shown in Fig. 1, the system comprises four core components: a perceiver that interprets the input image and generates candidate editing actions, an MCTS-based planner that explores and selects potential editing actions, an executor that applies the edits, and an evaluator that assesses the editing results. In addition, PhotoAgent incorporates a tool-selection module to dynamically choose suitable editing tools and a memory module that records editing history, enabling informed planning, reflection, and consistent decision-making across multiple editing steps. The system operates iteratively through a perceive–plan–execute–evaluate cycle, where the closed-loop process continues until the editing objective is met or a termination condition is satisfied.

Perceiver: Instruction Generation The perceiver utilizes a VLM, e.g., LLaVA [22], Qwen3-VL [2, 3], to analyze the visual input It and generate a set of K diverse and atomic editing actions {ak t }K k=1. To this end, we introduce a structured, context-aware multimodal prompting scheme that conditions the VLM on both the current visual scene and aesthetic attributes, enabling the perceiver to act as an aesthetic-driven instruction generator. This structured, context-aware scheme has the following capabilities.

(a). The perceiver supports both fully autonomous editing, where no explicit user command is provided, and userguided editing, where users may express intent through mood, atmosphere, or feeling rather than concrete objects or operations. (b). We also let the perceiver infer the scene type and use it with the scene-aware prompt. This allows the agent to generate tailored strategies for different types of scenes. For example, for images with a human subject, we prioritize maintaining the character’s appearance while allowing more aggressive modifications to the background. (c). Moreover, we perform memory mechanisms that record the outcomes of each editing round to guide subsequent instruction generation. Over time, these records form a static strategy memory that helps the agent improve continuously and produce diverse, contextually appropriate edits. See Appendix H for detailed prompt and memory (history) design.

Planner: MCTS-Based Action Exploration The planner chooses the candidate actions through an MCTS-based planning process, as shown in Fig. 2. Specifically, unlike existing methods [14, 21, 50] that edit without planning, our planner enables the agent to simulate sequences of future edits, evaluating their long-term consequences before execution. This approach avoids short-sighted decisions and irreversible mistakes. To achieve this, MCTS consists of four phases: selection, expansion, simulation, and backpropagation.

In the selection phase, the planner starts from the root node representing the current image and chooses which candidate edits to explore next. These candidates come from

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-25.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 4](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-004-figure-27.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 5 -->

the perceiver’s output. The traversal balances exploration of new edits with exploitation of high-reward ones. When reaching a leaf node, the expansion phase adds new child nodes representing potential editing actions. For example, when evaluating an action like “adjust the color balance to enhance the blue of the sky and the green of the water”, it creates a new node to represent the resulting image state.

In the simulation phase, we evaluate candidate edits efficiently using a fast-approximation environment. To speed up simulations, we use reduced-resolution processing, which preserves essential visual and semantic information. We verify that this approximation does not introduce a significant sim-to-real gap, as demonstrated in Appendix A.

Finally, during backpropagation, we calculate the reward value and propagate it back through the tree. This updates the visit count and average reward of each visited node, helping the selection phase make better decisions. After a number of simulations, the algorithm selects the action with the highest average reward or the most visits from the root node for actual execution.

Executor: Action Execution Then, the executors actually run the selected actions on the image. In practice, we select the top-K actions rather than only the action with the highest score, which ensures robustness and avoids simulation inaccuracies in the previous step. For each action, our system selects between traditional operators, e.g., color adjustment or cropping via OpenCV/PIL [4]), and advanced generative models, e.g., FLUX.1 Kontext [19] or Step1X- Edit [23]. We then employ the evaluator to evaluate all results, retaining only the highest-scoring output as the next state It+1. This approach ensures that our final decisions are grounded in real outcomes rather than simulated estimates, significantly improving the reliability of our editing trajectory.

Evaluator: Outcome Evaluation The evaluator assesses the set of edited images {Ik t }K k=1 produced by executing the top-K actions, and outputs each an assessment score {rk t }K k=1. PhotoAgent employs an ensemble evaluation strategy that integrates traditional no-reference metrics (such as NIQE [25] and BRISQUE [24]), modern instruction-based assessment (such as CLIP-based aesthetic scoring [31, 33] and instruction-following evaluation [22]), and customizable perceptual models (see Section 4), to provide a comprehensive evaluation. We provide detailed settings in the Appendix C.

The highest candidate score is compared against the score of the input image It−1. If an improvement is observed, the corresponding image is selected as the next state. Otherwise, the system reverts to It−1. The process terminates when the maximum number of steps is reached or updates no longer change the result.

## 4. Evaluation for Editing Systems

Effective evaluation is critical for autonomous image editing, where systems must assess aesthetic quality in a way that aligns with human preferences and directly guides multi-step decision-making. Existing image quality metrics are largely designed for generic images and are illsuited for user-generated photos, especially in editing scenarios that require fine-grained and subjective judgments. To address this limitation, as shown in Fig. 3, we introduce a comprehensive evaluation framework that includes (i) a UGC-specific preference dataset for training aesthetic reward models, (ii) a learned reward model tailored to usergenerated photos. Furthermore, we construct a real-world photo editing benchmark for evaluating end-to-end editing performance.

UGC-Edit Dataset As shown in Fig. 3, we introduce UGC-Edit, a dataset of approximately 7,000 authentic usergenerated photos designed for training aesthetic evaluation models in photo editing systems. Images are sourced from the LAION Aesthetic dataset [33] and the RealQA benchmark [20]. As they contain diverse web images beyond real user photos, we apply a two-stage filtering process: a vision-language model first categorizes image types, followed by manual verification to retain only images with clear UGC characteristics. We merge the two sources and normalize all aesthetic scores to a unified 1–5 scale. This dataset serves exclusively as supervision for training a UGC-specific reward model aligned with human aesthetic preferences.

UGC Reward Model We train a UGC-specific reward model on UGC-Edit to predict fine-grained aesthetic scores reflecting human preferences, as shown in Fig. 3. The model is initialized from a pretrained vision-language model (Qwen2.5-VL [3]) and optimized using Group Relative Policy Optimization (GRPO) [34], which learns from relative rankings within image groups. This training strategy improves robustness to annotation noise and enables the model to capture subtle aesthetic cues for guiding multi-step photo editing. Importantly, the learned reward model constitutes one component of our evaluation framework. Final performance is assessed using a comprehensive evaluation protocol that combines multiple complementary metrics and human judgments. Detailed analyses are provided in Appendix B and C.

Editing Benchmark for Final Evaluation To evaluate the end-to-end performance of photo editing systems, we construct a separate benchmark consisting of 1,017 realworld photographs captured by different users and devices. It covers a diverse range of common photographic scenes, including portrait photography, natural landscapes, urban and architectural scenes, food photography, everyday objects, and low-light or night-time imagery. Each image is edited using multiple baseline methods for final evaluation.

<!-- Page 6 -->

Camera-captured

Poster

Painting

AI-generated

Modeling

Mobile-captured

Camera-captured Mobile-captured

UGC Reward Model Training

VLM-based relevance scoring Human verification

7k+ images Authentic UGC characteristics Normal distribution

O1 O2 O3

Output Reward rates

Group Advantage Computation

Reference Model

Reward Model Policy Model

Policy Optimization

Original distribution Normal distribution

UGC-Edit Dataset

LAION & RealQA

{ } R1 R2 R3 A1 A2 A3

Advantages

**Figure 3.** Pipeline for constructing the UGC-Edit Dataset and training reward model. We start with a diverse pool of source images from LAION [33] and RealQA [20]. Each image is processed through a structured prompt with Qwen3-VL [42] for UGC classification. The images are then filtered by human annotators. Finally, a reward model is trained via GRPO [34] to predict fine-grained quality scores.

We report quantitative metrics, qualitative comparisons, and user study results on this benchmark to assess real-world editing effectiveness.

## 5. Experiments

## 5.1. Implementation Details

We choose two groups of baselines for comparison, including non-agent methods and agent methods. For nonagent methods, we compare with InstructPix2Pix [5], SDXL+Prompt [29], and Flux.1 Kontext [19], which performs editing in a single step without planning capabilities. We use the vague editing prompt (i.e., “make this image better”) to reflect realistic scenarios with ambiguous user intent. For agent methods, we compare with Hugging- GPT [35] (which generates all editing commands in a single call), ReAct [46] (Open-loop, iteratively plans and executes without evaluation), and ReAct [46] (Closed-loop, iteratively plans and incorporates an evaluator to decide action retention).

We calculate two types of metrics: semantic alignment and non-reference image quality. For semantic alignment, we use CLIP Similarity (↑) [31] to measure how well the edited image preserves the original content. For image quality, we report ImageReward1 (↑) [44] to approximate human preference alignment, BRISQUE (↓) [24] for non-reference image quality, and Laion-Reward (↑) [33] for general aesthetic preference. Additionally, we report UGC Score (↑), which is calculated from our reward model fine-tuned on user-generated content (Section 4) to better reflect users’ aesthetic preferences.

1We use the implementation of https://github.com/RE-N-Y/imscore.

## 5.2. Main Results

Quantitative Results We show the quantitative results in Table 1. It can be seen that PhotoAgent achieves the best BRISQUE score, which reveals the effectiveness of our framework. In contrast, GPT-4o exhibits an over-editing intent, often outputting overly vivid colors and exaggerated contrast. While such outputs may score well on perceptual metrics, they can introduce significant image distortions. In addition, our method attains competitive performance on other metrics such as ImageReward. As for agent-based baselines, their overall performance is limited. In open-loop settings, this is mainly because they lack visual feedback, which can cause errors to accumulate and the system to drift away from the correct trajectory. In closed-loop settings, their performance is also constrained, which may lead to suboptimal or short-sighted decisions. The results demonstrate the effectiveness of the PhotoAgent, especially in producing consistent improvements in both semantic alignment and aesthetic quality.

Qualitative Results We also show qualitative comparisons in Fig. 4 to clearly demonstrate PhotoAgent’s effectiveness. We observe that non-agent methods, such as GPT- 4o, often apply generic edits and fail to address specific issues when given vague instructions (e.g., “make this image better”). Meanwhile, we find that agent-based baselines [35, 46], often suffer from error accumulation and make short-sighted planning decisions, resulting in unsatisfactory visual output. In contrast, PhotoAgent effectively explores multiple editing paths through a closed-loop planning mechanism, and progressively selects and executes the most appropriate editing actions.

User Study To further validate the effectiveness and robustness of PhotoAgent, we conduct a user study involving 20 participants across 27 real-world editing scenarios, col-

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-006-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

GPT-4o SDXL InstructPix2Pix Input Ours ReAct (cls.)

**Figure 4.** Qualitative results. PhotoAgent generates visually pleasing edits by autonomously improving color harmony, composition, and aesthetic expressiveness, often introducing a stronger sense of visual dynamics and atmosphere. Baseline methods tend to produce incomplete or less coherent outputs.

**Table 1.** Quantitative comparison of different planning strategies. The best results are in bold, and the second best are underlined.

## Methods

CLIP ImageReward↑ BRISQUE↓ Laion- UGC Score↑ Similarity ↑ Reward ↑ GPT-4o [28] 0.6015 0.4115 0.7215 0.5131 4.210 InstructPix2Pix [5] 0.6123 0.3824 0.6976 0.4826 3.428 SDXL [29] 0.6079 0.3801 0.7189 0.4944 3.277 Flux.1 Kontext [19] 0.6037 0.3971 0.6831 0.4973 3.561 HuggingGPT [35] 0.6006 0.3993 0.6992 0.4921 3.420 ReAct (Open-loop) [46] 0.6059 0.3872 0.6485 0.4989 3.175 ReAct (Closed-loop) [46] 0.6027 0.3962 0.6422 0.5011 3.258 PhotoAgent (Ours) 0.6254 0.4079 0.6217 0.5134 4.176 lecting a total of 540 votes. Participants are asked to select their preferred result based on both visual quality and willingness to share. As shown in Table 2, PhotoAgent is consistently favored over several baseline methods, demonstrating its effectiveness in real-world settings.

## 5.3. Ablation Studies

We perform ablation studies to verify the key designs of PhotoAgent. We examine the effect of the UGC evaluator by removing it from the framework, which significantly decreases aesthetic metrics like Laion-Reward. This confirms

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-17.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-18.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-19.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-20.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-21.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-22.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-23.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-007-figure-24.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

**Table 2.** User study results: percentage of votes selecting each method as the best.

HuggingGPT ReAct (cls.) GPT-4o PhotoAgent (Ours) 12.6% 15.2% 30.2% 42.0%

Input Iteration-1 Iteration-2 Iteration-3

**Figure 5.** The editing process of our PhotoAgent over three iterations.

the reward model’s effectiveness in editing preferences. In addition, we investigate the importance of simulation times. Limiting the number of MCTS simulations to 10 results in suboptimal decisions, which demonstrates the necessity of strategic planning. Likewise, reducing the MCTS search depth to 1 can effectively implement greedy selection, leading to lower performance on multi-step edits. Overall, our results indicate that the evaluator, the depth of planning, and the number of simulations all play important roles in PhotoAgent’s performance. Additional details are provided in the Appendix.

## 5.4. Analysis

Comparison with existing editing agents. Compared with recent editing agent systems such as JarvisArt [21], 4KAgent [50], and Agent Banana [47], PhotoAgent is designed as a more general and flexible framework for agentic photo editing.

First, while many existing systems are developed around specific tasks (for example, JarvisArt focuses on image retouching, and 4KAgent targets super-resolution), PhotoAgent is explicitly formulated as a general photo-editing agent. It can handle a broad spectrum tasks ranging from basic retouching (exposure, color and tone adjustments) to high-level semantic operations such as object addition/removal, composition changes, and background replacement.

Second, rather than binding to a single editor, PhotoAgent integrates a pool of heterogeneous executors and dynamically routes each instruction type to the empirically best-performing tool on public multi-turn editing bench-

Input

…sky’s fading glow hold her gaze longer than time allows…

Input …frayed edges of dusk press close to the frame.…

… solitude unfolds here, unhurried and true…

…a chilled stillness where time slows down…

…gently shift attention to what peeking out from behind winter veil...

…warmth brought vitality, just like music playing..…

**Figure 6.** PhotoAgent with user-guided prompts.

marks, so as to fully exploit different tools’ strengths.

Third, PhotoAgent includes a UGC-oriented evaluator trained on real user photos and aesthetic ratings, so that the resulting images better reflect real users’ preferences and values instead of optimizing only generic aesthetic scores.

Finally, PhotoAgent incorporates a long-horizon planning mechanism that supports exploratory aesthetic optimization, which is beneficial for the multi-round editing. Collectively, these distinctions position our method as a more general, adaptive, and user-aligned alternative to prior specialized solutions.

Editing Process As shown in Fig. 5, PhotoAgent first adjusts the overall tone to significantly enhance the image’s aesthetic quality. Based on it, PhotoAgent can further edit specific objects, such as flying birds, which makes scene appear more lively and dynamic. This iterative strategy allows PhotoAgent to simultaneously preserve the original content and improve aesthetics, highlighting its effectiveness and robustness in producing visually compelling results.

User-guided Editing PhotoAgent supports not only fully autonomous editing, but also user-guided editing, which is common in real-world usage. In the user-guided setting, users are not required to specify concrete objects or explicit editing operations. Instead, they may express highlevel intent through abstract descriptions such as mood, atmosphere, or emotional tone. As illustrated in Fig. 6, PhotoAgent is able to interpret such guidance and produce visually appealing results with distinct styles under different prompts. This flexibility enables PhotoAgent to effectively align with the real-world application scenarios.

Terminate Condition PhotoAgent employs two complementary early stopping strategies to prevent unnecessary edits on high-quality images: (1) a maximum iteration limit,

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-13.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-15.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-008-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

which forces termination after a predefined number of steps, and (2) a no-improvement criterion, which stops editing if the evaluator detects no significant score improvement over N consecutive iterations. These mechanisms ensure that high-quality images are not over-edited.

## 6. Conclusion

We present PhotoAgent, an autonomous image editing system that reframes photo editing as a sequential decisionmaking process, reducing the reliance on precise human instructions. The novelty arises from the coordinated interaction of multiple modules rather than innovating on the underlying editing models themselves. Specifically, the system integrates four key components: an LLM-based perceiver, an MCTS-driven exploration strategy, a toolbased executor, and a VLM-based evaluator, forming a closed-loop framework supported by the proposed UGC- Edit dataset. Experimental results demonstrate that PhotoAgent outperforms existing methods in producing semantically coherent and aesthetically consistent enhancements. The framework provides a foundation for more photo editing in future work.

## References

[1] Stability AI. Stable diffusion 3.5. https: / / huggingface. co / stabilityai / stable diffusion-3.5-large, 2024. Accessed: 2025-09-23. 3 [2] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui

Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. Qwen3-vl technical report. arXiv preprint arXiv:2511.21631, 2025. 2, 4 [3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin

Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923, 2025. 4, 5 [4] Gary Bradski. The opencv library. Dr. Dobb’s Journal: Soft- ware Tools for the Professional Programmer, 25(11):120– 123, 2000. 2, 5 [5] Tim Brooks, Aleksander Holynski, and Alexei A Efros. In- structpix2pix: Learning to follow image editing instructions. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 18392–18402, 2023. 1, 3, 6, 7 [6] Cameron B Browne, Edward Powley, Daniel Whitehouse,

Simon M Lucas, Peter I Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez, Spyridon Samothrakis, and Simon Colton. A survey of monte carlo tree search methods. IEEE Transactions on Computational Intelligence and AI in games, 4(1):1–43, 2012. 2 [7] Siyu Cao, Hangting Chen, Peng Chen, Yiji Cheng, Yutao

Cui, Xinchi Deng, Ying Dong, Kipper Gong, Tianpeng Gu, Xiusen Gu, et al. Hunyuanimage 3.0 technical report. arXiv preprint arXiv:2509.23951, 2025. 3 [8] Guillaume Chaslot, Sander Bakkes, Istvan Szita, and Pieter

Spronck. Monte-carlo tree search: A new framework for game ai. In Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment, volume 4, pages 216–217, 2008. 2 [9] Haoyu Chen, Keda Tao, Yizao Wang, Xinlei Wang, Lei Zhu, and Jinjin Gu. Photoartagent: Intelligent photo retouching with language model-based artist agents. arXiv preprint arXiv:2505.23130, 2025. 3 [10] Yunjey Choi, Minje Choi, Munyoung Kim, Jung-Woo Ha,

Sunghun Kim, and Jaegul Choo. Stargan: Unified generative adversarial networks for multi-domain image-to-image translation. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2018. 3 [11] Marcos V Conde, Gregor Geigle, and Radu Timofte. Instruc- tir: High-quality image restoration following human instructions. In European Conference on Computer Vision, pages 1–21. Springer, 2024. 21 [12] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou,

Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, Guang Shi, and Haoqi Fan. Emerging properties in unified multimodal pretraining. arXiv preprint arXiv:2505.14683, 2025. 1, 3 [13] discus0434. Aesthetic predictor v2.5: Siglip-based aesthetic score predictor. https: / / github. com / discus0434/aesthetic-predictor-v2-5, 2024. GitHub repository. 3 [14] Niladri Shekhar Dutt, Duygu Ceylan, and Niloy J Mitra.

Monetgpt: Solving puzzles enhances mllms’ image retouching skills. ACM Transactions on Graphics (TOG), 44(4):1– 12, 2025. 2, 3, 4 [15] Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing

Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. In Z. Ghahramani, M. Welling, C. Cortes, N. Lawrence, and K.Q. Weinberger, editors, Advances in Neural Information Processing Systems, volume 27. Curran Associates, Inc., 2014. 3 [16] Google. Nano banana: Gemini 2.5 flash image editing model. https://aistudio.google.com/models/ gemini-2-5-flash-image, 2025. Accessed: 2025- 09-23. 3 [17] Amir Hertz, Ron Mokady, Jay Tenenbaum, Kfir Aberman,

Yael Pritch, and Daniel Cohen-Or. Prompt-to-prompt image editing with cross attention control. arXiv preprint arXiv:2208.01626, 2022. 1, 3 [18] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner,

Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. In Advances in Neural Information Processing Systems (NeurIPS), 2017. 3 [19] Black Forest Labs, Stephen Batifol, Andreas Blattmann,

Frederic Boesel, Saksham Consul, Cyril Diagne, Tim Dockhorn, Jack English, Zion English, Patrick Esser, Sumith Kulal, Kyle Lacey, Yam Levi, Cheng Li, Dominik Lorenz, Jonas M¨uller, Dustin Podell, Robin Rombach, Harry Saini, Axel Sauer, and Luke Smith. Flux.1 kontext: Flow matching for in-context image generation and editing in latent space, 2025. 1, 2, 3, 5, 6, 7 [20] Mingxing Li, Rui Wang, Lei Sun, Yancheng Bai, and Xi- angxiang Chu. Next token is enough: Realistic image quality

<!-- Page 10 -->

and aesthetic scoring with multimodal large language model. arXiv preprint arXiv:2503.06141, 2025. 5, 6 [21] Yunlong Lin, Zixu Lin, Kunjie Lin, Jinbin Bai, Panwang Pan,

Chenxin Li, Haoyu Chen, Zhongdao Wang, Xinghao Ding, Wenbo Li, et al. Jarvisart: Liberating human artistic creativity via an intelligent photo retouching agent. arXiv preprint arXiv:2506.17612, 2025. 2, 3, 4, 8 [22] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.

Visual instruction tuning. Advances in neural information processing systems, 36:34892–34916, 2023. 1, 4, 5 [23] Shiyu Liu, Yucheng Han, Peng Xing, Fukun Yin, Rui Wang,

Wei Cheng, Jiaqi Liao, Yingming Wang, Honghao Fu, Chunrui Han, Guopeng Li, Yuang Peng, Quan Sun, Jingwei Wu, Yan Cai, Zheng Ge, Ranchen Ming, Lei Xia, Xianfang Zeng, Yibo Zhu, Binxing Jiao, Xiangyu Zhang, Gang Yu, and Daxin Jiang. Step1x-edit: A practical framework for general image editing. arXiv preprint arXiv:2504.17761, 2025. 1, 3, 5 [24] Anish Mittal, Anush Krishna Moorthy, and Alan Con- rad Bovik. No-reference image quality assessment in the spatial domain. IEEE Transactions on image processing, 21(12):4695–4708, 2012. 5, 6 [25] Anish Mittal, Rajiv Soundararajan, and Alan C Bovik. Mak- ing a “completely blind” image quality analyzer. IEEE Signal processing letters, 20(3):209–212, 2012. 5 [26] NVIDIA Corporation. Nvidia developer blog. https:// developer.nvidia.com/blog. Accessed: 2025-11- 25. 21 [27] OpenAI. Dall·e 3, 2024. Accessed: 2025-09-23. 3 [28] OpenAI. Gpt-4o. https://openai.com/index/ hello-gpt-4o, 2024. Accessed: 2025-09-23. 1, 3, 7 [29] Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas M¨uller, Joe Penna, and Robin Rombach. Sdxl: Improving latent diffusion models for high-resolution image synthesis. arXiv preprint arXiv:2307.01952, 2023. 1, 6, 7 [30] Vaishnav Potlapalli, Syed Waqas Zamir, Salman H Khan, and Fahad Shahbaz Khan. Promptir: Prompting for all-inone image restoration. Advances in Neural Information Processing Systems, 36:71275–71293, 2023. 21 [31] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya

Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. arXiv preprint arXiv:2103.00020, 2021. 3, 5, 6 [32] Robin Rombach, Andreas Blattmann, Dominik Lorenz,

Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 10684–10695, 2022. 1 [33] Christoph Schuhmann, Romain Beaumont, Richard Vencu,

Cade Gordon, Ross Wightman, Mehdi Cherti, Theo Coombes, Aarush Katta, Clayton Mullis, Mitchell Wortsman, et al. Laion-5b: An open large-scale dataset for training next generation image-text models. Advances in neural information processing systems, 35:25278–25294, 2022. 5, 6 [34] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao

Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of math- ematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024. 5, 6 [35] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li,

Weiming Lu, and Yueting Zhuang. Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face. Advances in Neural Information Processing Systems, 36:38154–38180, 2023. 3, 6, 7 [36] Haoyuan Shi, Yunxin Li, Xinyu Chen, Longyue Wang, Bao- tian Hu, and Min Zhang. Animaker: Automated multi-agent animated storytelling with mcts-driven clip generation, 2025. 3 [37] David Silver, Aja Huang, Chris J Maddison, Arthur Guez,

Laurent Sifre, George Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. Mastering the game of go with deep neural networks and tree search. Nature, 529(7587):484–489, 2016. 3 [38] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar,

Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv: Arxiv-2305.16291, 2023. 3 [39] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan,

Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint arXiv:2409.12191, 2024. 1 [40] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Si- moncelli. Image quality assessment: From error visibility to structural similarity. IEEE transactions on image processing, 13(4):600–612, 2004. 3 [41] Zhenyu Wang, Aoxue Li, Zhenguo Li, and Xihui Liu.

Genartist: Multimodal llm as an agent for unified image generation and editing. Advances in Neural Information Processing Systems, 37:128374–128395, 2024. 1 [42] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan

Gao, Kun Yan, Sheng ming Yin, Shuai Bai, Xiao Xu, Yilei Chen, Yuxiang Chen, Zecheng Tang, Zekai Zhang, Zhengyi Wang, An Yang, Bowen Yu, Chen Cheng, Dayiheng Liu, Deqing Li, Hang Zhang, Hao Meng, Hu Wei, Jingyuan Ni, Kai Chen, Kuan Cao, Liang Peng, Lin Qu, Minggang Wu, Peng Wang, Shuting Yu, Tingkun Wen, Wensen Feng, Xiaoxiao Xu, Yi Wang, Yichang Zhang, Yongqiang Zhu, Yujia Wu, Yuxuan Cai, and Zenan Liu. Qwen-image technical report, 2025. 3, 6 [43] Jinheng Xie, Weijia Mao, Zechen Bai, David Junhao Zhang,

Weihao Wang, Kevin Qinghong Lin, Yuchao Gu, Zhijie Chen, Zhenheng Yang, and Mike Zheng Shou. Show-o: One single transformer to unify multimodal understanding and generation. arXiv preprint arXiv:2408.12528, 2024. 3 [44] Jiazheng Xu, Xiao Liu, Yuchen Wu, Yuxuan Tong, Qinkai

Li, Ming Ding, Jie Tang, and Yuxiao Dong. Imagereward: Learning and evaluating human preferences for textto-image generation. Advances in Neural Information Processing Systems, 36:15903–15935, 2023. 6 [45] Yuzhe Yang, Liwu Xu, Leida Li, Nan Qie, Yaqian Li,

Peng Zhang, and Yandong Guo. Personalized image aesthetics assessment with rich attributes. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern

<!-- Page 11 -->

Recognition, pages 19861–19869, 2022. 12 [46] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran,

Karthik Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In International Conference on Learning Representations (ICLR), 2023. 3, 6, 7 [47] Ruijie Ye, Jiayi Zhang, Zhuoxin Liu, Zihao Zhu, Siyuan

Yang, Li Li, Tianfu Fu, Franck Dernoncourt, Yue Zhao, Jiacheng Zhu, et al. Agent banana: High-fidelity image editing with agentic thinking and tooling. arXiv preprint arXiv:2602.09084, 2026. 8 [48] Hancheng Zhu, Zhiwen Shao, Yong Zhou, Guangcheng

Wang, Pengfei Chen, and Leida Li. Personalized image aesthetics assessment with attribute-guided fine-grained feature representation. In Proceedings of the 31st ACM International Conference on Multimedia, pages 6794–6802, 2023. 12 [49] Jun-Yan Zhu, Taesung Park, Phillip Isola, and Alexei A

Efros. Unpaired image-to-image translation using cycleconsistent adversarial networks. In Computer Vision (ICCV), 2017 IEEE International Conference on, 2017. 3 [50] Yushen Zuo, Qi Zheng, Mingyang Wu, Xinrui Jiang, Renjie

Li, Jian Wang, Yide Zhang, Gengchen Mai, Lihong V Wang, James Zou, et al. 4kagent: agentic any image to 4k superresolution. arXiv preprint arXiv:2507.07105, 2025. 2, 3, 4, 8

<!-- Page 12 -->

A. Sim-to-Real Gap in Low-Resolution Planner Simulation

PhotoAgent uses reduced-resolution rollouts to make MCTS planning computationally feasible. This raises the question of whether an action sequence that scores well in low-resolution simulation remains optimal when executed at full resolution. To address this, the system incorporates several design choices that effectively control the sim-to-real gap.

Evaluator Consistency across Resolutions. The Evaluator exhibits stable scoring behavior between simulated and real environments. Table 3 reports the alignment between reward rankings computed at reduced resolutions and those obtained at full resolution. Even at one-quarter resolution, the top-ranked decisions are largely preserved, and rank correlations remain high.

**Table 3.** Consistency between simulated (low-resolution) rewards and full-resolution rewards.

Metric 1/2 resolution 1/4 resolution Top-1 retention (same best) 85% 75% Top-3 retention 100% 90% Spearman correlation 0.94 0.79 Kendall τ 0.90 0.73

Full-Resolution Re-Scoring of Top-K Candidates. To further reduce sensitivity to coarse simulation, MCTS retains only the top-K candidate actions and forwards them for full-resolution evaluation. The final action is selected using these highfidelity scores. This step ensures that occasional deviations in low-resolution reward estimation do not influence the actual decision executed by the system.

Closed-Loop Replanning after Each Executed Edit. The system applies only one action at a time. After executing the chosen edit at full resolution, MCTS restarts from the updated image. This closed-loop design prevents any discrepancies between simulation and execution from accumulating across steps, ensuring that each decision remains grounded in the real environment.

B. Generalization of UGC Reward Model

To test how well our reward model generalizes beyond the UGC-Edit dataset, we evaluate it on the external PARA dataset [45], which includes a wide variety of content, styles, and lighting conditions. PARA provides aesthetic scores annotated by humans. Table 4 shows the correlation between the model’s predictions and human aesthetic judgments. The model achieves SRCC scores around 0.75, surpassing prior state-of-the-art PIAA models [48], which attain roughly 0.70– 0.72. These results demonstrate that the reward model consistently aligns with human preferences across other scenarios. This proves the effectiveness and generalization ability of our UGC reward model.

**Table 4.** Correlation of the reward model with human judgments on the PARA dataset.

Metric Aesthetic Content PLCC 0.7390 0.7577 SRCC 0.7560 0.7702

C. Experimental details

Details of MCTS Algorithm 1 shows the pseudo-code for the Monte Carlo Tree Search (MCTS) planner at the core of PhotoAgent. The search starts from the current image state st and runs for a set number of simulations. Each simulation follows four main phases: Selection, Expansion, Simulation (including Evaluation), and Backpropagation. Selection: The algorithm moves from the root node through the tree, choosing actions that balance exploration and exploitation using the UCT policy. This process continues until it reaches a leaf node that has not been fully expanded. Expansion: At a nonterminal leaf node sL, the perceiver generates candidate editing actions. Each action corresponds to a new child node, which is added to the search tree to represent the resulting image state. Simulation: From the expanded node, the algorithm performs a lightweight rollout up to a maximum depth d. During this rollout, the evaluator assesses the resulting state sT and assigns

<!-- Page 13 -->

**Figure 7.** More visual results of PhotoAgent.

a reward G, which reflects the predicted aesthetic and semantic quality of the edits. Backpropagation: The reward G is propagated backward along the path that was traversed. This updates the visit counts N(s, a) and average rewards Q(s, a) for all visited nodes, helping the selection phase make better decisions in future simulations. After completing all simulations, the action from the root node with the highest visit count is chosen for execution. This action represents the most thoroughly explored and promising option.

This MCTS process enables exploratory visual aesthetic planning. By simulating multiple possible future trajectories in a fast-approximation environment, the agent can obtain the outcomes of different editing strategies without performing costly real edits. Integrating the reward model ensures that the search favors edits aligned with human preferences. As a result, the

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 13](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-013-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 14 -->

**Figure 8.** More visual results of PhotoAgent.

system can find high-quality actions and handle multi-step editing.

VLM Planner Hyperparameters The vision-language model (VLM) planner generates candidate editing actions by analyzing the input image and user requirements. We configure the VLM with a maximum token length of 1024 for generating planning steps, a temperature of 0.7 to balance determinism and diversity, and a top-p (nucleus sampling) value of 0.8 to control the probability mass of candidate tokens.

Evaluator Hyperparameters Our multi-modal quality evaluator combines four complementary assessment models with carefully tuned weights. The

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 14](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-014-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 15 -->

Input Nano-Banana2

Grok-imagine Ours

Input Nano-Banana2

Grok-imagine Ours

**Figure 9.** Comparison with closed-source advanced image editing models nano-banana2 and Grok-Imagine. While both can further enhance input images, Grok-Imagine tends to over-enhance, producing exaggerated or dreamlike effects (e.g., a background resembling lens flare), whereas nano-banana2 is more restrained but lacks clear aesthetic guidance (e.g., unnecessary sky edits). Our method preserves the original content when the image is already visually appealing.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 15](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-015-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 16 -->

Input Nano-Banana2

Grok-imagine Ours

Input Nano-Banana2

Grok-imagine Ours

**Figure 10.** Nano-banana2 tends to add excessive details and may alter the main subject, such as the llama in the figure. Grok-Imagine often over-enhances and introduces unnecessary flares. Our method avoids unnecessary changes when the input image is already visually appealing (e.g., the cat) and produces more aesthetically pleasing results.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 16](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-016-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 17 -->

Grok-imagine Ours

Input Nano-Banana2

**Figure 11.** Our method generates images that preserve the original content and creative intent while enhancing the overall artistic mood and sense of atmosphere.

CLIP model, which measures image-text semantic alignment, is assigned a weight of 1.0. The aesthetic assessment model and ImageReward model, both emphasizing visual quality, are given higher weights of 2.0 each. The UGC evaluation model,

![Figure extracted from page 17](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-017-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 17](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-017-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 17](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-017-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 17](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-017-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 18 -->

Input Nano-Banana2

Grok-imagine Ours

**Figure 12.** Our method generates images with richer texture and material quality, while also enhancing the overall atmosphere and artistic mood, surpassing other compared methods.

serving as a quality indicator, is assigned a weight of 0.8. The final overall score is computed as a weighted sum of these individual metrics, with a total weight normalization of 5.8.

For the UGC evaluator’s text generation component, we employ a temperature of 0.7 and a top-p value of 0.9, with a

![Figure extracted from page 18](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-018-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 18](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-018-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 18](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-018-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 18](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-018-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 19 -->

maximum token length of 32 tokens to ensure concise and focused quality assessments.

D. More Visual Results

We show more visual results in Figs. 7–12.

## Algorithm

## 1 MCTS Planning for

PhotoAgent

Require: Current state st, Perceiver, Executor, Evaluator, Rollout depth d Ensure: Best action abest

1: while within computational budget do 2: s ←st ▷Start from root state 3:

4: // 1. Selection 5: while s is in the tree and not terminal do 6: a ←select action using UCT policy from s 7: s ←next state after taking action a 8: end while 9: sL ←s ▷Reached leaf node sL 10: 11: // 2. Expansion 12: if sL is non-terminal then 13: Actions ←Perceiver(sL) 14: Add child nodes for each action to the tree 15: end if

16: 17: // 3. Simulation 18: sT ←sL 19: for i = 1 to d do 20: a ←select random action from sT 21: sT ←next state after action a 22: if sT is terminal then 23: break 24: end if 25: end for 26: G ←Evaluator(sT) ▷Assess aesthetic and semantic quality

27: 28: // 4. Backpropagation 29: Backpropagate G along the path from st to sL 30: Update Q(s, a) and N(s, a) for all visited nodes 31: end while 32:

33: return abest = arg maxa N(st, a) ▷Choose the most visited action

E. Dataset Diversity and Fairness

The UGC-Edit dataset is constructed from two primary sources: LAION, which is predominantly English-dominant and collected from websites, and RealQA, a Chinese-dominant dataset collected from AutoNavi. Together, these sources provide a broad coverage of real-world scenarios, including tourist attractions, restaurants, hotels, leisure venues, and other useractive locations. This diversity enables the reward model to be trained and evaluated across a variety of cultural and content contexts. Preliminary checks on model outputs across these diverse contexts indicate no systematic bias against non-Western or unconventional aesthetic styles.

To evaluate the end-to-end performance of our photo editing system, we construct a diverse test set consisting of 1,017 real user-captured images. These images are sourced from multiple channels, including Lofter and Flickr photo streams,

<!-- Page 20 -->

self-captured photos using consumer cameras and smartphones, curated content from public websites, and a small subset from the LAION dataset filtered for authentic user-generated photographs. The resulting test set covers a wide range of photographic scenarios, including portraiture, landscape and nature scenes, urban and architectural photography, still-life and food images, night scenes, and casual snapshots. Each image was taken under varying lighting conditions, camera settings, and compositions, providing a realistic and challenging benchmark for assessing aesthetic improvements across different editing methods.

F. Computational Cost

We provide a detailed analysis of PhotoAgent’s computational profile and the practical points that influence latency. Our goal is to make clear where most of the cost arises and provide a potential way to optimize in practice.

Profiling the System. Multiple factors, including the number of simulations, the choice of executors, and GPU utilization, influence the running time of our system. We conduct a full profiling pass under the default configuration (search depth of 3, maximum of 20 simulations per iteration, and 3 editing iterations). As summarized in Table 5, the majority of the latency comes from the MCTS-based planner, where simulation and in-loop execution dominate the cost. Evaluator calls contribute a smaller but still noticeable fraction, whereas the perceiver stage contributes only a minor overhead. For comparison, agentbased methods such as ReAct (cls.) have an inference time of approximately 120s, which is on the same order of magnitude.

In practice, we find that extremely simple images require fewer MCTS simulations and sometimes do not need a simulation at all. This motivates a lightweight PhotoAgent. For example, using 10 simulations per iteration results in a total processing time of about 100s. The breakdown is perceiver 10s, executor 60s, planner 20s, and evaluator 30s.

**Table 5.** Runtime breakdown of PhotoAgent under the default configuration.

Component Time (s) Percentage (total/parent) Perceiver ∼10 2.1% Planner (MCTS) ∼250 53.2% / 100% →Executor (MCTS) ∼170 36.2% / 68.0% →Evaluator (MCTS) ∼80 17.0% / 32.0% Executor ∼180 38.3% Evaluator ∼30 6.4% Total† ∼470 100%

†Excludes initialization and duplicated evaluator time.

Here we provide three directions that may accelerate the system.

MCTS Search Budget. The first factor is the search budget of MCTS. Table 6 shows how varying the number of simulations directly trades off runtime and performance. Reducing the simulation count from 20 to 5 decreases the runtime from roughly 250s to 60s, while maintaining comparable BRISQUE, LAION-Reward, and UGC human scores. These results indicate that the default setting emphasizes quality, not speed, and that significantly faster operating points are readily attainable without architectural change.

**Table 6.** Impact of simulation budget on accuracy and runtime.

Simulations Time (s) BRISQUE↓ Laion-Reward↑ UGC Score↑ 5 ∼60 0.6292 0.5083 3.982 10 ∼120 0.6270 0.5099 4.005 15 ∼185 0.6246 0.5103 4.121 ∼250 0.6217 0.5134 4.176

Changing Editing Model. Second, an equally important factor is the choice of editing tool. Because PhotoAgent is toolagnostic, its execution time can immediately benefit from faster generative models without structural modification. For

<!-- Page 21 -->

example, at the same resolution (1080p), Step1x-Edit requires only about half the runtime of Flux.1 Kontext-Dev (reducing the time from ∼20s to ∼10s). Replacing the editing backend is a one-line API change, underscoring that the latency is not intrinsic to the framework.

## Model

Acceleration. Finally, the system naturally benefits from standard model-optimization techniques used in production environments. Quantizing the transformer blocks of FLUX.1 Kontext to FP8 or FP4 yields over 2× memory reduction and provides noticeably faster inference on NVIDIA Blackwell GPUs [26]. Comparable improvements can be obtained through TensorRT compilation or by adopting lower-precision evaluator models. These optimizations do not require any modifications to the PhotoAgent algorithm.

G. Future Work

While our system performs well overall, it still exhibits several failure cases, as shown in Fig. 13. For example, dark or low-quality images can lead to unsatisfactory edits because the model struggles both to interpret the content and to apply effective adjustments. Moreover, when the input image is already of high quality, the system may introduce changes that add little value or, in some cases, refuse to make edits altogether. We also observe situations where the system makes technically reasonable modifications, but the codification cannot match user expectations, which is a general problem in image editing tasks.

Input Output Output Output Input Input

**Figure 13.** Some failed results where the editor may have made excessive changes.

In this section, we focus on discussing how to extend the current system to other application domains. First, different application domains may require specialized editing tools. For example, medical or scientific images often rely on stable reconstruction models rather than generative editors, so integrating more deterministic editors, such as fidelity-oriented restoration models [11, 30], could improve stability. Second, practical deployment frequently involves combining heterogeneous tools, including local enhancement models or commercial APIs. Creating a unified, plugin-style interface would simplify management and reduce system overhead. Third, different domains require evaluators aligned with their specific attributes, such as diagnostic or structural metrics for scientific imagery. Domain-specific reward models can help maintain consistent performance across diverse tasks. Finally, new domains often require specialized evaluation metrics. For instance, non-photorealistic or artistic images, such as illustrations, anime, or heavily stylized renderings, may need training or finetuning on domain-specific data. Incorporating these components would allow PhotoAgent to guide edits more effectively and make it applicable to specialized tasks.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 21](2026-ICML-photoagent-exploratory-visual-aesthetic-planning-with-large-vision-models/page-021-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.
