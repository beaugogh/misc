---
title: "ParaDySe: A Parallel Strategy Switching Framework for Dynamic Sequences in Transformer-based Large Language Models"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39649
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39649/43610
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# ParaDySe: A Parallel Strategy Switching Framework for Dynamic Sequences in Transformer-based Large Language Models

<!-- Page 1 -->

ParaDySe: A Parallel-Strategy Switching Framework for Dynamic Sequences in

Transformer-based Large Language Models

Zhixin Ou*, Peng Liang*, Linbo Qiao†, Jianchen Han, Baihui Liu

National Key Laboratory of Parallel and Distributed Computing, College of Computer Science and Technology, National

University of Defense Technology {ouzhixin16, peng leung, qiao.linbo, hjc, lbh}@nudt.edu.cn

## Abstract

Dynamic sequences with varying lengths have been widely used in the training of Transformer-based large language models (LLMs). However, current training frameworks adopt a pre-defined static parallel strategy for these sequences, causing neither communication-parallelization cancellation on short sequences nor out-of-memory on long sequences. To mitigate these issues, we propose ParaDySe, a novel adaptive Parallel strategy switching framework for Dynamic Sequences. ParaDySe enables on-the-fly optimal strategy adoption according to the immediate input sequence. It first implements the modular function libraries for parallel strategies with unified tensor layout specifications, and then builds sequence-aware memory and time cost models with hybrid methods. Guided by cost models, ParaDySe selects optimal layer-wise strategies for dynamic sequences via an efficient heuristic algorithm. By integrating these techniques together, ParaDySe achieves seamless hot-switching of optimal strategies through its well-designed function libraries. We compare ParaDySe with baselines on representative LLMs under datasets with sequence lengths up to 624K. Experimental results indicate that ParaDySe addresses OOM and CPC bottlenecks in LLM training by systematically integrating longsequence optimizations with existing frameworks.

Code — https://github.com/Carrie-ou/ParaDySe Extended version — https://arxiv.org/abs/2511.13198

## Introduction

In recent years, Transformer-based large language models (LLMs) have demonstrated remarkable performance not only in text-related tasks but also in cross-domain applications like genomic tasks due to their exceptional parallel computing capability and scalability. Models like GPT (OpenAI 2024) leverage self-attention to capture longdistance semantic relationships, with context windows expanding from 512 to 128K tokens, thereby improving performance in long-context tasks, including document understanding and programming assistance. Growing sequence

*These authors contributed equally. †Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

lengths exponentially increase the computational and memory complexity O(n2), creating significant challenges for LLM training.

Parallelism strategies partition LLM states and intermediate results into distributed devices, providing additional computational and memory resources for scaled model training. Recent researches improve training efficiency by partitioning in the sequence dimension, such as Sequence Parallelism (Li et al. 2023) and Ulysses (Jacobs et al. 2024), which have shown great improvements in training throughput. However, when processing documents that exceed 128K tokens, the extremely long sequences often lead to out-ofmemory (OOM) failures during model training. To achieve better memory savings, researchers establish fine-grained optimized sequence parallelisms, such as METP (Liang et al. 2025). It can significantly decrease the memory consumption of devices, making it suitable for training extremely long sequences. However, METP raises communication overhead as a trade-off to training efficiency, thereby negating performance gained by distributed parallelism. The communication-parallelization cancellation (CPC) becomes more severe when memory-saving parallel strategies are applied to short sequences, which bring more frequent communications during LLM training. To conclude, efficient strategies perform optimally for short sequences, while memory-saving strategies are suited for long sequences.

Existing LLM training frameworks, such as Megatron- LM (Shoeybi et al. 2020; Narayanan et al. 2021; Korthikanti et al. 2023), typically offer multiple parallel strategies for options, including tensor parallelism (TP), sequence parallelism (SP), etc (Tang et al. 2025; Zheng et al. 2024; Liang et al. 2023). These frameworks significantly enhance the capabilities of large-model training. Strategic parallelism selection enables optimal efficiency-memory trade-off for given workloads. By selecting appropriate parallel strategies for the training dataset, they can achieve a balanced tradeoff between training efficiency and memory consumption. However, ideally assuming the training workloads are static across different samples, these frameworks mostly employ a fixed parallel strategy for all Transformer layers throughout the entire training process. Therefore, they fail to adapt to real-world input sequences that range from queries consisting of several tokens to those comprising millions of tokens, remaining unable to resolve OOM failures or CPC issues.

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

24648

<!-- Page 2 -->

As a promising alternative, HotSPa (Ge et al. 2024) pioneers hot-switching at the mini-batch level for different sequence lengths across parallel strategies, integrating unified graph compilation and communication-aware scheduling. However, its coarse-grained switching mechanism, while supporting sequences up to 32K tokens, exhibits incompatibility with modern memory-efficient parallel strategies. This calls for a training framework that incorporates both novel and conventional parallelism to support extremely long sequences exceeding 300K tokens, adaptively selects parallel strategies for dynamic sequences, and achieves fine-grained switching.

To address it, this paper presents ParaDySe, a Parallelstrategy switching approach for Dynamic Sequences in Transformer models. ParaDySe enables layer-wise adaptive parallel training based on real-time sequence lengths, achieving seamless strategy switching without tensor redistribution or communication synchronization. Specifically, our contributions can be summarized as follows:

• We propose ParaDySe, a novel framework enabling adaptive parallel strategy switching for dynamic sequences, which achieves sequence length support up to 624K tokens while significantly improving training efficiency. • Through the design of modular function libraries based on tensor layout specifications, ParaDySe eliminates tensor redistribution overhead, thereby enabling seamless strategy switching. • Through sequence-aware cost models for time and memory, ParaDySe achieves on-the-fly optimal layer-wise strategy selection adapted to dynamic sequences, with a balanced trade-off between training efficiency and memory consumption.

## Related Work

LLM Training Frameworks Transformer-based LLMs have two core operations: the Multi-Head Attention (MHA) and the Feed-Forward Network (FFN) operation. As LLMs demand increasing computational resources, various automatic parallel training frameworks have been proposed to address challenges in efficiency and memory consumption (Li et al. 2024). Deep- Speed introduces the ZeRO family (Ren et al. 2021; Rajbhandari et al. 2021) for fine-grained partitioning of optimizer states, gradients, and parameters, significantly reducing memory usage. Megatron-LM focuses on scalable training via tensor parallelism (TP) (Narayanan et al. 2021), and extends it with sequence parallelism (SP) and context parallelism (CP) (Korthikanti et al. 2023) to support longer sequences.Colossal-AI incorporates Ring Self-Attention (RSA) (Li et al. 2023) to parallelize MHA computation. Recent work has also explored automated strategy generation. AutoPipe (Liu et al. 2022) introduces a heuristic-based planner that partitions transformer blocks into sub-layer granularity to balance pipeline stages. Merak (Lai et al. 2023) further generalizes this idea by automatically composing 3D parallelism through a proxy-graph abstraction. While these frameworks achieve impressive performance,

Notation Definition b ∈Z+ Batch size s ∈Z+ Sequence length h ∈Z+ Hidden dimension size n ∈Z+ Number of attention heads p ∈Z+ Parallelism degree l ∈[1, L] Layer index of L-layer Transformer π ∈P Parallel strategy within strategy set P q ∈Q Transformer operation, Q = {MHA, FFN} X ∈X Layer input (e.g., XMHA) W ∈W Layer parameter (e.g., Wqkv) Y ∈Y Layer output (e.g., O, Z) Mπ(X) Memory cost model under π Tπ(X) Time cost model under π f l π,q ∈F Transformer function under (π, q, l)

**Table 1.** Notations and definitions. most adopt static parallel strategies fixed at training initialization. HotSPa (Ge et al. 2024) addresses this limitation via mini-batch-level hot-switching by pre-defined checkpoints and strategy sets, but restricts support to conventional parallel paradigms. Extending this line of dynamically switching, our ParaDySe framework introduces a more fine-grained framework at the Transformer layer level, which achieves sequence-aware adaptive strategy hot-switching, along with a more flexible functional programming approach.

Parallel Methods on 1D Device Grids

The device grid describes the topological structure of a computing cluster. One-dimensional (1D) device grids represent the linear arrangement of devices, typical in singlenode multi-accelerator configurations. Several operatorlevel parallel methods have been developed for 1D device grids. Megatron-LM TP+SP employs AllGather and ReduceScatter communications along the sequence dimension in both MHA and FFN layers. Its CP extension further enhances parallelism through sequence-dimension partitioning. DeepSpeed Ulysses (Jacobs et al. 2024) distributes attention heads via All-to-All communication, enabling independent processing of head subsets across devices. Colossal-AI SP (Li et al. 2023) introduces ring-based communication patterns for MHA optimization, though its activation memory remains quadratic with sequence length. METP (Liang et al. 2025) advances memory optimization through fine-grained partitioning and asynchronous ring-based execution, featuring a two-level loop structure for MHA that enables computation-communication overlap. However, existing long-sequence training methods lack strategy composability and runtime adaptability. Our work extends these methods by enhancing modularity and enabling dynamic control within 1D device grid constraints.

## Problem Formulation

The symbolic notations used in this paper are defined in Table 1. Transformer architecture has two core operations (q ∈Q), the Multi-Head Attention (MHA) and the Feed- Forward Network (FFN) operation, whose computational process can be formally expressed as Equations (1-3) and

24649

<!-- Page 3 -->

Switchable Functional Parallelism Module Hybrid Cost Estimation Module Input 𝑋𝑋

Parallel Strategy Tensor Layout

MegatronTS MegatronCZ

UlyssesZ ColossalZ

METP

Adaptive Parallel Strategy Switching Module

Parallel Strategy Selection Algorithm

① 𝑋𝑋

④ParaDySeMHA, ParaDySeFFN ⑤{𝑓𝑓𝜋𝜋𝑙𝑙,𝑞𝑞 𝑙𝑙 }, 𝑙𝑙∈[1, 𝐿𝐿], 𝑞𝑞= {𝑀𝑀𝑀𝑀𝑀𝑀, 𝐹𝐹𝐹𝐹𝐹𝐹}

Megatron-LM TP+SP

Megatron-LM CP

DeepSpeed Ulysses

Colossal-AI SP

METP

DeepSpeed ZeRO3

Parallel Method

② {𝜋𝜋, 𝑀𝑀𝜋𝜋(𝑋𝑋), 𝑇𝑇𝜋𝜋(𝑋𝑋)}, 𝜋𝜋∈𝒫𝒫

③ Π∗(𝑋𝑋) = {𝜋𝜋𝑙𝑙}, 𝑙𝑙∈[1, 𝐿𝐿]

ParaDySeMHA ParaDySeFFN

{𝑓𝑓𝜋𝜋1,𝑀𝑀𝑀𝑀𝑀𝑀

1, 𝑓𝑓𝜋𝜋1,𝐹𝐹𝐹𝐹𝐹𝐹

1 } {𝑓𝑓𝜋𝜋𝐿𝐿,𝑀𝑀𝑀𝑀𝑀𝑀

𝐿𝐿, 𝑓𝑓𝜋𝜋𝐿𝐿,𝐹𝐹𝐹𝐹𝐹𝐹

𝐿𝐿 }

𝑓𝑓MegatronTS,MHA 𝑓𝑓MegatronC𝑍𝑍,MHA 𝑓𝑓Ulysses𝑍𝑍,MHA 𝑓𝑓Colossal𝑍𝑍,MHA 𝑓𝑓METP,MHA 𝑓𝑓MegatronTS,FFN 𝑓𝑓MegatronC𝑍𝑍,FFN 𝑓𝑓Ulysses𝑍𝑍,FFN 𝑓𝑓Colossal𝑍𝑍,FFN 𝑓𝑓METP,FFN

Layer 𝑙𝑙

𝑇𝑇(𝑋𝑋) 𝑀𝑀(𝑋𝑋) = ቊRandom Forest Regressor

Polynomial Regression

Functional

Libraries

Π∗(𝑋𝑋) = argmin 𝜋𝜋𝑙𝑙

∑𝑙𝑙∈[1,𝐿𝐿] 𝑇𝑇𝜋𝜋𝑙𝑙(𝑋𝑋)

𝑋𝑋𝑀𝑀𝑀𝑀𝑀𝑀, 𝑋𝑋𝐹𝐹𝐹𝐹𝐹𝐹, 𝑂𝑂, 𝑍𝑍:

𝑏𝑏× ⁄ 𝑠𝑠𝑝𝑝× ℎ, 𝑊𝑊𝑞𝑞𝑞𝑞𝑞𝑞: ⁄ 3ℎ𝑝𝑝× ℎ, 𝑊𝑊𝑝𝑝𝑝𝑝𝑝𝑝𝑝𝑝: ⁄ ℎ𝑝𝑝× ℎ, 𝑊𝑊𝑖𝑖𝑖𝑖: ⁄ 4ℎ𝑝𝑝× ℎ, 𝑊𝑊𝑜𝑜𝑜𝑜𝑜𝑜: ⁄ 4ℎ𝑝𝑝× ℎ.

LLM 𝒞𝒞= (ℎ, 𝑛𝑛, 𝐿𝐿)

State {𝑊𝑊𝑀𝑀𝑀𝑀𝑀𝑀, 𝑊𝑊𝐹𝐹𝐹𝐹𝐹𝐹}

Function

{𝑓𝑓𝜋𝜋𝑙𝑙,𝑀𝑀𝑀𝑀𝑀𝑀 𝑙𝑙, 𝑓𝑓𝜋𝜋𝑙𝑙,𝐹𝐹𝐹𝐹𝐹𝐹 𝑙𝑙 }

··· ···

Layer 1

State

Function

Layer 𝐿𝐿

State

Function

{𝑓𝑓𝜋𝜋𝑙𝑙,𝑀𝑀𝑀𝑀𝑀𝑀 𝑙𝑙, 𝑓𝑓𝜋𝜋𝑙𝑙,𝐹𝐹𝐹𝐹𝐹𝐹 𝑙𝑙 }

⑥ 𝑠𝑠. 𝑡𝑡. ෍ 𝑙𝑙∈[1,𝐿𝐿]

𝑀𝑀𝜋𝜋𝑙𝑙(𝑋𝑋) < 𝑂𝑂𝑂𝑂𝑂𝑂

**Figure 1.** Overview of ParaDySe Framework for dynamic sequences with varying lengths. These three core Modules (namely Hybrid Cost Estimation Module, Switchable Functional Parallelism Module, and Adaptive Parallel Strategy Switching Module) are collaborative adaptively to achieve almost optimal parallel strategy according to the input sequence. The details of these modules are presented in the following subsection.

Equation (4) respectively.

Q, K, V = XMHAWqkv (1)

A = Softmax(QKT

√ d

)V (2)

O = AWproj (3) Z = GELU(XFFNWin)Wout (4) Let C = (h, n, L) be the configuration tuple that determines LLM type, as a simplification for Transformer-based LLM. Notably, we treat C as a fixed hyperparameter for methodology development, and only vary it in experimental evaluation. Given Transformer layer index l, parallel strategy π, and operation q, there exists f l π,q ∈F that implements the corresponding function, where F: X × W →Y. For each parallel strategy π under fixed configuration C, there exists layer-wise cost models Mπ(X) and Tπ(X), corresponding to the input X with sequence length s.

ParaDySe aims to determine the optimal parallel strategy lists Π∗= {π∗

1, · · ·, π∗ L}, where π∗ l denotes the parallel strategy at layer l that satisfies global optimization, for dynamically input sequence X by solving a constrained cost minimization problem:

Π∗(X) = argmin πl∈P Σ l∈[1,L] Tπl(X) (5)

s.t. Σ l∈[1,L] Mπl(X) < OOM (6)

ParaDySe Framework Overview This paper proposes the ParaDySe framework, a Parallel- Strategy framework for Dynamic Sequences lengths in Transformer models. The ParaDySe framework consists of three core modules, the Switchable Functional Parallelism Module, the Hybrid Cost Estimation Module, and the Adaptive Parallel Strategy Switching Module, as shown in Figure 1.

Switchable Functional Parallelism Module

In distributed deep learning, the tensor layout describes the specific distribution pattern of tensors across the device grid. This module proposes a tensor layout specification for 1D device grids, typically in single-node multi-accelerator configurations, where each complete-information tensor can only be partitioned along a single dimension to prevent information loss. The complete-information tensors mainly consider the MHA and FFN operations within a Transformer layer, including layer inputs (XMHA, XFFN), layer parameters (Wqkv, Wproj, Win, Wout), and layer outputs (O, Z), while excluding intermediate results generated during computation by parallel methods.

According to the architecture of Transformer models, the layer inputs and outputs maintain consistent tensor layouts as b×s×h. The sharding layouts for each single dimension are as follows: b/p × s × h, b × s/p × h, and b × s × h/p. The layer parameters primarily focus on weight matrices, the core trainable state of Transformer models. In MHA operation, the h × h matrices of Q, K, V are concatenated to form parameter Wqkv with tensor layout h × 3h, expanding to h × 3nh when considering n attention heads. In FFN operation, the weight matrices Win and Wout are designed with dimensions h×4h and 4h× h, correspondingly. These two-dimensional tensors can be sharded either row-wise or column-wise.

We systematically analyze the tensor layouts of parallel methods in terms of sharding dimensions (e.g., b/s/h and row/column) and communication patterns (e.g., AllReduce/AllGather/ReduceScatter). For instance, Megatron- LM TP partitions the layer parameters Wproj, Wout row-wise and Wqkv, Win column-wise to decrease memory consumption. The SP method is integrated into Megatron-LM as the TP+SP paradigm, where an AllGather synchronizes activations along the s dimension before MHA and FFN operations, followed by a ReduceScatter communication. Table 2

24650

<!-- Page 4 -->

Parallel Method XMHA, O, XFFN, Z Wqkv Wproj Win Wout Megatron-LM TP b × s × h h × 3h/p h/p × h h × 4h/p 4h/p × h Megatron-LM TP+SP b × s/p × h h × 3h/p h/p × h h × 4h/p 4h/p × h Megatron-LM CP b × s/p × h h × 3h h × h h × 4h 4h × h DeepSpeed Ulysses b × s/p × h h × 3h h × h h × 4h 4h × h DeepSpeed ZeRO3 b/p × s × h (h/p × 3h)T h/p × h (h/p × 4h)T 4h/p × h Colossal-AI SP b × s/p × h h × 3h h × h h × 4h 4h × h METP b × s/p × h h × 3h/p h/p × h h × 4h/p 4h/p × h Specification b × s/p × h (3h/p × h)T h/p × h (4h/p × h)T 4h/p × h

**Table 2.** The tensor layout analysis on parallel methods, and tensor layout specification of parallel strategies.

## Algorithm

1: Parallel Strategy Selection Algorithm

Require: b: batch size; s: sequence length; C = (h, n, L):

LLM hyperparameters; D: Dictionary with keys as (b, s) and values as the optimal strategy lists Π(b,s) = {π1, · · ·, πL}; P: A list of parallel strategies sorted in ascending order by latency and memory usage. Ensure: Π∗= {π∗

1, · · ·, π∗ L}, where π∗ l denotes the optimal parallel strategy at layer l that satisfies global optimization. 1: pop useless(strategy sorted) 2: if (b, s) in D then 3: return D[(b, s)] 4: end if 5: strategy options ←[ ] 6: for i = 0 to len(P) −1 do 7: strategies ←[P[i]] × L 8: if i == 0 and not OOM(strategies) then 9: Π∗←strategies 10: break 11: end if 12: if not OOM(strategies) then 13: append strategies to strategy options 14: else 15: for k = i + 1 to len(P) −1 do 16: for l = 0 to L −1 do 17: pop the first element from strategies 18: append P[k] to the end of strategies 19: if not OOM(strategies) then 20: append strategies to strategy options 21: end if 22: end for 23: end for 24: end if 25: end for 26: if strategy options is not empty then 27: Π∗←least time cost strategies in strategy options 28: else 29: Π∗←least memory cost strategies × L 30: end if 31: D[(b, s)] ←Π∗

32: 33: return Π∗ concludes the tensor layouts analysis of the parallel methods introduced in the related work.

Since different parallel methods employ inconsistent tensor layouts, switching between parallel methods can lead to layout mismatches between the output tensor of the preceding operator and the input tensor of the subsequent operator. In such cases, a tensor redistribution operation is required, which introduces additional computational overhead and communication costs. Accordingly, this module establishes the tensor layout specification for the parallel strategy set to follow, which precisely defines standardized tensor sharding dimensions, as shown in the last row of table 2.

Following the tensor layout specification, we construct a compliant parallel strategy set by extending existing parallel methods. In tensor processing, most parallel methods adopt sequence-dimension (s) sharding for layer inputs/outputs. While ZeRO3 typically employs batch-dimension (b) partitioning, it can alternatively shard s through integration with sequence parallel methods. Regarding layer parameters, parallel methods including Megatron-LM CP, Deep- Speed Ulysses, and Colossal-AI SP maintain intact tensors, but can integrate with ZeRO3 to enable tensor sharding. Notably, ZeRO3 requires row-wise sharding of parameter weight matrices. To satisfy this constraint, we transpose both Wqkv and Win, ensuring memory-contiguous layouts across devices for proper AllGather execution. Adhering to tensor layout specifications, the parallel strategy set P comprises the following 5 elements (as shown in Figure 1).

- MegatronTS: Megatron-LM TP+SP; - MegatronCZ: Megatron-LM CP+DeepSpeed ZeRO3; - UlyssesZ: DeepSpeed Ulysses+DeepSpeed ZeRO3; - ColossalZ: Colossal-AI SP+DeepSpeed ZeRO3; - METP: METP. These parallel strategies with identical tensor layouts theoretically enable seamless hot-switching without tensor redistribution. However, in practice, the parallel strategies in P are not switchable due to incompatibilities in implementation, such as programming interfaces and communication mechanisms. To address it, we construct modular parallel strategy function libraries based on functional programming, encapsulating the MHA and FFN computation processes of each parallel strategy into standardized functions, according to Equations (1-4). Specifically, we instantiate the parametric implementations under parallel strategy π for MHA and

24651

<!-- Page 5 -->

FFN operations through the mapping:

fπ,MHA: XMHA × WMHA →O (7) fπ,FFN: XFFN × WFFN →Z (8)

where WMHA = {Wqkv, Wproj}, WFFN = {Win, Wout}. For ∀π ∈P, the functions fπ,MHA and fπ,FFN are instantiated as the ParaDySeMHA and ParaDySeFFN modules respectively, collectively forming modular function libraries supporting multiple parallel strategies.

Hybrid Cost Estimation Module This module proposes sequence-aware hybrid cost models that adaptively select between Random Forest Regressor in ensemble learning framework (Breiman 2001) (RF) and Polynomial Regression (PR). The parallel strategy space P is converted into a multi-dimensional discrete feature via onehot encoding, and then concatenated with continuous LLM hyperparameters C = (h, n, L) to form configuration groups (C, π).

For each configuration group, we perform comprehensive profiling to measure the time cost T (X) and memory cost M(X) on training every X ∈X with length s in the dataset. The OOM threshold is set to the maximum memory consumption OOM(Mπ). Based on measurements under given configuration group (C, π), we independently construct hybrid models for estimating time and memory costs, taking s as the sole input variable.

T (X) M(X)

=

RF(X) s ≤max(sprofile) PR(X) s > max(sprofile) (9)

RF is employed for interpolation, when the input sequence is within the profiling lengths. It combines all tree outputs through mean aggregation to generate regression predictions. PR is employed for extrapolation, when the input sequence is beyond profiling lengths. Optional polynomial orders, from one to three, preserve the distinctive variation signature of each configuration while avoiding the bias of a global fit.

This sequence-aware hybrid cost module combines the interpolation advantages of RF with the extrapolation capabilities of PR. By setting OOM threshold OOM C π for each configuration group, it incorporates automatic OOM risk detection to inform subsequent heuristic strategy selection.

Adaptive Parallel Strategy Switching Module This module proposes a heuristic parallel strategy switching algorithm to select the optimal layer-wise parallel strategy, based on sequence-aware cost models under LLM configuration C and sequence inputs with length s, as detailed in Algorithm 1. Candidate strategies are filtered based on device memory constraints, with the time-optimal strategy selected from the feasible set. Complexity analysis. Lines 6-15 yield a worst-case computational complexity of O(P 2 × L2) = O(L2). Lines 12- 20 yield a worst-case memory complexity of O(P × L) + O(L) = O(L), accounting for both the storage of all possible strategy combinations and the final layer-wise strategy selections.

Optimizations. Despite the O(L2) theoretical complexity, significant constant factors arise from list operations and memory calculations during execution. To address this, we implement multiple optimizations in our heuristic algorithm.

Parameter Caching: A dictionary D stores mappings from (b, s) to strategy, reducing time complexity to O(1) for repeated configurations.

Pre-sorting Pruning (Line 1): Strategies inferior in both time and memory are eliminated before evaluation.

Early Termination (Line 8): If the fastest strategy by time ranking satisfies memory constraints, it’s immediately selected (O(L) best-case complexity).

OOM Short-circuiting (Lines 16/19): Memory checks terminate early when any strategy fails constraints, minimizing inner-loop iterations.

Smoothing (Line 33): If the time cost of previous strategy is estimated slightly higher than the current optimal strategy within ratio γ, ParaDySe retains the previous strategy to mitigate potential memory overhead from frequent strategy switching.

Implementation Functional programming libraries. The modular function library implements parallel strategies within the ParaDySeMHA class and the ParaDySeFFN class, exposing a strategy-agnostic callable fπ,q, such as fMETP,MHA. These functional libraries for parallel strategy set follow identical parameter lists (input: layer input, state: layer parameters) and return types (result: layer output). MHA and FFN functions of each parallel strategy take layer inputs and parameters as function arguments and return layer outputs after performing strategy-specific parallel computations. Internally, distributed computation is achieved through collective communication primitives (e.g., AllReduce, AllGather). This design enables parallel strategy hot-switching without reconfiguration. Cost model implementations. We measure the wall-clock time cost per sequence and real-time peak GPU memory allocation of PyTorch across combinations of parallel strategies π ∈P and model configurations C.

The cost model converts parallel strategies into 4dimensional one-hot encoded features, concatenated with normalized continuous parameters. We instantiate separate RF (n estimators=50, max depth=10) for each parallel strategy and prediction target (time/memory), implemented via scikit-learn with custom feature importance tracking.

The polynomial regression automatically fits and caches models per configuration using polyfit in numpy, with degree selection via AIC. The prediction engine implements runtime model switching based on sequence length boundaries stored in a configuration database. Adaptive parallel strategy switching implementations. The ParaDySe framework implementation enables instantaneous parallel strategy switching through a polymorphic function registry design. ParaDySe maintains a strategyto-function mapping dictionary, where each key corresponds to a specific operation implementation function (e.g., fMegatronTS,MHA). During execution, the forward method dynamically retrieves the function of target strategy π, and in-

24652

<!-- Page 6 -->

vokes the function with consistent inferences. This design guarantees hot-switching across parallel strategies by updating the strategy parameter, which dynamically switches parallel strategies π ∈P without reconstructing the computation graph.

## Experiment

Setting Platforms. Our experiments are conducted on a computing node equipped with 8 NVIDIA A100-SXM4-80GB GPUs interconnected via NVLink, supported by an AMD EPYC 7473X 24-Core Processor. The software stack comprised PyTorch 2.5.1, CUDA 12.4, NCCL 2.21.5, and FlashAttention-v2.7.4.post1. We set the random seed to 42 for RF. Datasets. Table 3 shows that datasets GitHubCode (Code- Parrot 2021) and GRCh38 (Consortium 2013) exhibit a pronounced long-tail distribution in length, with max 309K and 624K. GitHubCode adopts GPT-2 tokenization (Radford et al. 2019), and GRCh38 adopts 3-mer tokenization (Ji et al. 2021). Adopting Curriculum Learning principles (Wang, Chen, and Zhu 2022), we sort training sequences by length (short-to-long) to enhance training stability. Models. We conduct experiments on three representative LLMs, BERT (Devlin et al. 2019), LLaMA (Llama Team 2024), GPT (Brown et al. 2020) as shown in Table 4. Baselines. We consider individual parallel strategies π ∈P as baselines for comparison. Notably, ColossalZ strategy implements MHA operation by RSA, which inherently conflicts with FlashAttention optimization, resulting in suboptimal quadratic memory complexity. Meanwhile, the manually pre-defined switching mechanism of HotSPa inherently restricts support to conventional parallel paradigms and strategies, leaving extremely long genomic or code sequences exceeding 300K tokens beyond its scope. Consequently, this section excludes ColossalZ and HotSPa from experimental evaluation and analysis.

Overall Experiment Our experiments evaluate the performance and maximum supported sequence length of ParaDySe against baselines by training representative LLMs on datasets with extremely long sequences, as shown in Figure 2.

Experimental results on GitHubCode demonstrate that ParaDySe achieves the longest sequence support among all baselines (resolving OOM failures) while delivering substantial performance improvements (eliminating CPC issues). Taking BERT as an example, which is successfully trained by all baselines on the complete dataset, ParaDySe exhibits optimal training efficiency, reducing training time by up to 89.29% for the maximum sequences compared to baselines. As LLM scaling from BERT to GPT, ParaDySe consistently maintains long-sequence support of METP. Notably, with the largest GPT model, ParaDySe extends the trainable sequence length by up to 144.16% beyond baselines.

ParaDySe demonstrates consistent performance gains on GRCh38, with 58.01% faster training time for BERT and 181.22% longer sequences for GPT. ParaDySe effectively enhances training efficiency while substantially expanding sequence length support. We observe a single outlier case during LLaMA training, where the supported sequence length of ParaDySe slightly trails the top-performing baseline, directing future work toward communication analysis.

Ablation Study The ablation studies comprehensively validate the components of ParaDySe framework. In these studies, we train GPT on GRCh38, and refer to the original ParaDySe framework as ParaDySe (full). Parallel strategy set. The ablation study confirms that each option in the parallel strategy set contributes significantly to framework performance. Notably, the MegatronTS strategy demonstrates the most substantial impact on computational efficiency, while the METP optimization provides the greatest enhancement to maximum trainable sequence length. Hybrid cost model. The experimental results demonstrate that ParaDySe’s hybrid cost model, which integrates RF with PR, achieves superior performance compared to using PR alone. This improvement validates the effectiveness of our combined modeling approach. Algorithm optimization. We set the ratio γ = 5% to evaluate smoothing optimization. Experimental results confirm that the smoothing optimization for strategy switching yields modest but consistent improvements in both model performance and sequence length support. The smoothing optimization contributes to a dramatic enhancement of system stability, effectively eliminating the risks of performance fluctuations and communication overhead caused by abrupt strategy switching during training. During validation, we identified that frequent strategy switching incurs nonnegligible memory overhead and reduces maximum trainable sequence length.

Case Study Conventional parallel training frameworks suffer severe inefficiencies when handling OOM failures due to their inability to perform on-the-fly strategy switching, requiring complete environment re-initialization for strategy transitions. Our measurements on GPT training with GRCh38 reveal a total reset latency exceeding 31 seconds, comprising: 2- 3 seconds for dependency imports, 5 seconds for dataset reloading, 22 seconds for model reinitialization (accounting for 70.2% of total overhead), and 1 second for Adam optimizer setup. This rigid switching paradigm creates a critical performance bottleneck.

ParaDySe framework addresses this through an innovative hot-switching mechanism that combines: proactive OOM prediction using trained models to anticipate memory constraints, and switchable functional library with specified tensor layout enabling seamless strategy transitions. By continuously evaluating memory and computational costs during training, ParaDySe performs smooth hot-switching without interrupting training.

## Conclusion

We propose a novel layer-wise Parallel strategy switching framework for Dynamic Sequences (ParaDySe), which is

24653

<!-- Page 7 -->

Length (0, 4K) [4K, 8K) [8K, 16K) [16K, 32K) [32K, 64K) [64K, 128K) [128K, +∞) Max GitHubCode 65.7% 14.5% 9.8% 5.1% 2.7% 1.1% 1.1% 309K GRCh38 3.5% 26.4% 28.7% 21.2% 11.9% 5.5% 1.9% 624K

**Table 3.** Sequence length distributions and maximums of GRCh38 and GitHubCode.

0 50 100 150 200 250 300 Sequence Length (K tokens)

0 100 200 300 400 500

Cumulative Time (s)

(a) GitHubCode-BERT

0 50 100 150 200 250 300 Sequence Length (K tokens)

0 50 100 150 200 250

Cumulative Time (s)

(b) GitHubCode-LLaMA

0 50 100 150 200 250 Sequence Length (K tokens)

0

100

200

300

Cumulative Time (s)

(c) GitHubCode-GPT

0 100 200 300 400 500 600 Sequence Length (K tokens)

0

200

400

600

Cumulative Time (s)

(d) GRCh38-BERT

0 100 200 300 400 500 600 Sequence Length (K tokens)

0 200 400 600 800

Cumulative Time (s)

(e) GRCh38-LLaMA

0 50 100 150 200 250 300 Sequence Length (K tokens)

0 250 500 750

Cumulative Time (s)

(f) GRCh38-GPT

MegatronTS MegatronCZ UlyssesZ METP ParaDySe

**Figure 2.** Comparing ParaDySe with baselines across LLMs and long-sequence datasets on cumulative time (s) and sequence length (K tokens). Curve termination indicates OOM failure.

LLM h n L L/node BERT 16 24 24 LLaMA 64 80 8 GPT 12288 96 96 8

**Table 4.** LLM configurations.

Framework Seq len Time Time full Saving ParaDySe (full) 329728 3117.76 3117.76 w/o MegatronTS 300032 3173.80 2799.45 11.80% w/o MegatronCZ 300032 2795.91 2799.45 -0.13% w/o UlyssesZ 300032 2813.13 2799.45 0.49% w/o METP 112128 1741.99 1724.13 1.03% w/o RF 270336 2657.04 2622.89 1.29% w/o Smoothing 300032 2800.49 2799.45 0.04% *Seq len: maximum supported sequence length (token); *Time: cumulative training time (s) under framework; *Time full: cumulative training time (s) for ParaDySe (full) to reach the corresponding Seq len; *Saving: time-saving ratio (%) of ParaDySe (full) compared to the corresponding framework; *w/o means without, denoting the ablated component removed from the ParaDySe (full) framework.

**Table 5.** Ablation studies on parallel strategy set (L2-L5), hybrid cost model (L6), and algorithm optimization (L7).

architecturally composed of three integrated modules. Hot- Switching Functional Parallelism Module unifies tensor layouts across mainstream parallel methods, enabling layoutcompatible strategy switching at Transformer-layer granularity. Hybrid Cost Estimation Module constructs sequenceaware memory and time cost models to accurately predict resource consumption for each parallel strategy given input lengths. Adaptive Parallel Strategy Switching Module selects the optimal strategy set for each layer, which balances efficiency and memory utilization, achieving seamless redistribution-free switching.

ParaDySe resolves two critical bottlenecks in LLM training: CPC issues for short sequences and OOM failures for long sequences. Through systematic evaluations of typical LLMs with sequence lengths up to 624K tokens, our framework demonstrates significant improvements in end-to-end training efficiency. By integrating memory-efficient optimizations with general parallel strategies, ParaDySe establishes a new adaptive hot-switching paradigm for efficient and memory-saving LLM scaling.

The memory modeling during experiments was relatively coarse-grained, precluding precise calculations and resulting in suboptimal timing for strategy switching, which led to diminished effectiveness of layer-wise transitions.

## Acknowledgments

This work is sponsored in part by the National Natural Science Foundation of China under Grant No. 62025208 and 62421002.

24654

<!-- Page 8 -->

## References

Breiman, L. 2001. Random Forests. Machine Learning, 45(1): 5–32. Brown, T. B.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J.; Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; Agarwal, S.; Herbert-Voss, A.; Krueger, G.; Henighan, T.; Child, R.; Ramesh, A.; Ziegler, D. M.; Wu, J.; Winter, C.; Hesse, C.; Chen, M.; Sigler, E.; Litwin, M.; Gray, S.; Chess, B.; Clark, J.; Berner, C.; McCandlish, S.; Radford, A.; Sutskever, I.; and Amodei, D. 2020. Language models are few-shot learners. In Proceedings of NeurIPS, 1877– 1901. CodeParrot. 2021. GitHub Code Dataset. https:// huggingface.co/datasets/codeparrot/github-code. A dataset of filtered Python files from GitHub, prepared by the Code- Parrot team. Consortium, G. R. 2013. GRCh38.p14 Genome Assembly. https://www.ncbi.nlm.nih.gov/assembly/GCF 000001405.26/. Genome Reference Consortium Human Build 38, patch 14 (GRCh38.p14). Devlin, J.; Chang, M.-W.; Lee, K.; and Toutanova, K. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In Proceedings of NAACL-HLT, 4171–4186. Ge, H.; Fu, F.; Li, H.; Wang, X.; Lin, S.; Wang, Y.; Nie, X.; Zhang, H.; Miao, X.; and Cui, B. 2024. Enabling Parallelism Hot Switching for Efficient Training of Large Language Models. In Proceedings of the ACM Symposium on Operating Systems Principles, 178–194. Jacobs, S. A.; Tanaka, M.; Zhang, C.; Zhang, M.; Aminadabi, R. Y.; Song, S. L.; Rajbhandari, S.; and He, Y. 2024. System Optimizations for Enabling Training of Extreme Long Sequence Transformer Models. In Proceedings of the ACM Symposium on Principles of Distributed Computing, 121–130. Ji, Y.; Zhou, Z.; Liu, H.; and Davuluri, R. V. 2021. DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome. Bioinformatics, 37(15): 2112–2120. Korthikanti, V. A.; Casper, J.; Lym, S.; McAfee, L.; Andersch, M.; Shoeybi, M.; and Catanzaro, B. 2023. Reducing Activation Recomputation in Large Transformer Models. In Proceedings of Machine Learning and Systems, 341–353. Lai, Z.; Li, S.; Tang, X.; Ge, K.; Liu, W.; Duan, Y.; Qiao, L.; and Li, D. 2023. Merak: An Efficient Distributed DNN Training Framework with Automated 3d Parallelism for Giant Foundation Models. IEEE Transactions on Parallel and Distributed Systems, 34(5): 1466–1478. Li, D.; Li, S.; Lai, Z.; Fu, Y.; Ye, X.; Cai, L.; and Qiao, L. 2024. A Memory-Efficient Hybrid Parallel Framework for Deep Neural Network Training. IEEE Transactions on Parallel and Distributed Systems, 35(4): 577–591. Li, S.; Xue, F.; Baranwal, C.; Li, Y.; and You, Y. 2023. Sequence Parallelism: Long Sequence Training from System Perspective. In Rogers, A.; Boyd-Graber, J.; and Okazaki, N., eds., Proceedings of ACL, 2391–2404.

Liang, P.; Qiao, L.; Shi, Y.; Zheng, H.; Tang, Y.; and Li, D. 2025. Memory-Efficient Tensor Parallelism for Longsequence Transformer Training. Frontiers of Information Technology & Electronic Engineering, 26(5): 770–787. Liang, P.; Tang, Y.; Zhang, X.; Bai, Y.; Su, T.; Lai, Z.; Qiao, L.; and Li, D. 2023. A Survey on Auto-Parallelism of Large- Scale Deep Learning Training. IEEE Transactions on Parallel and Distributed Systems, 34(8): 2377–2390. Liu, W.; Lai, Z.; Li, S.; Duan, Y.; Ge, K.; and Li, D. 2022. AutoPipe: A Fast Pipeline Parallelism Approach with Balanced Partitioning and Micro-batch Slicing. In Proceedings of CLUSTER, 301–312. Llama Team. 2024. The Llama 3 Herd of Models. arXiv:2407.21783. Narayanan, D.; Shoeybi, M.; Casper, J.; LeGresley, P.; Patwary, M.; Korthikanti, V.; Vainbrand, D.; Kashinkunti, P.; Bernauer, J.; Catanzaro, B.; Phanishayee, A.; and Zaharia, M. 2021. Efficient large-scale language model training on GPU clusters using megatron-LM. In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis, 1–14. OpenAI. 2024. GPT-4 Technical Report. arXiv:2303.08774. Radford, A.; Wu, J.; Child, R.; Luan, D.; Amodei, D.; and Sutskever, I. 2019. Language Models are Unsupervised Multitask Learners. Rajbhandari, S.; Ruwase, O.; Rasley, J.; Smith, S.; and He, Y. 2021. ZeRO-infinity: breaking the GPU memory wall for extreme scale deep learning. In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis, 1–14. Ren, J.; Rajbhandari, S.; Aminabadi, R. Y.; Ruwase, O.; Yang, S.; Zhang, M.; Li, D.; and He, Y. 2021. ZeRO- Offload: Democratizing Billion-Scale Model Training. In Proceedings USENIX ATC, 551–564. Shoeybi, M.; Patwary, M.; Puri, R.; LeGresley, P.; Casper, J.; and Catanzaro, B. 2020. Megatron-LM: Training Multi- Billion Parameter Language Models Using Model Parallelism. arXiv:1909.08053. Tang, Y.; Yin, L.; Li, Q.; Zhu, H.; Li, H.; Zhang, X.; Qiao, L.; Li, D.; and Li, J. 2025. Koala: Efficient Pipeline Training through Automated Schedule Searching on Domain- Specific Language. ACM Transactions on Architecture and Code Optimization, 22(2): 63:1–25. Wang, X.; Chen, Y.; and Zhu, W. 2022. A Survey on Curriculum Learning. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(9): 4555–4576. Zheng, H.; Liang, P.; Tang, Y.; Shi, Y.; Qiao, L.; and Li, D. 2024. 3D Parallelism for Transformers via Integer Programming. In Proceedings of ICASSP, 6440–6444.

24655
