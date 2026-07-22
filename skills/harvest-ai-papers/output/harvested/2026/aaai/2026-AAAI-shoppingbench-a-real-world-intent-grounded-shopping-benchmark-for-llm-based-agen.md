---
title: "ShoppingBench: A Real-World Intent-Grounded Shopping Benchmark for LLM-based Agents"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40640
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40640/44601
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# ShoppingBench: A Real-World Intent-Grounded Shopping Benchmark for LLM-based Agents

<!-- Page 1 -->

ShoppingBench: A Real-World Intent-Grounded Shopping Benchmark for

LLM-based Agents

Jiangyuan Wang 1*, Kejun Xiao1*, Qi Sun1†, Huaipeng Zhao1, Tao Luo1, Jian Dong Zhang1, Xiaoyi Zeng1

1Alibaba International Digital Commercial Group {wangjiangyuan.wjy, xiaokejunkejun.xia, qiran.sq}@alibaba-inc.com

## Abstract

Existing benchmarks in e-commerce primarily focus on basic user intents, such as ﬁnding or purchasing products. However, real-world users often pursue more complex goals, such as applying vouchers, managing budgets, and ﬁnding multiproducts seller. To bridge this gap, we propose Shopping- Bench, a novel end-to-end shopping benchmark designed to encompass increasingly challenging levels of grounded intent. Speciﬁcally, we propose a scalable framework to simulate user instructions based on various intents derived from sampled real-world products. To facilitate consistent and reliable evaluations, we provide a large-scale shopping sandbox that serves as an interactive simulated environment, incorporating over 2.5 million real-world products. Experimental results demonstrate that even state-of-the-art language agents (such as GPT-4.1) achieve absolute success rates under 50% on our benchmark tasks, highlighting the signiﬁcant challenges posed by our ShoppingBench. In addition, we propose a trajectory distillation strategy and leverage supervised ﬁne-tuning, along with reinforcement learning on synthetic trajectories, to distill the capabilities of a large language agent into a smaller one. As a result, our trained agent achieves competitive performance compared to GPT-4.1.

Code — https://github.com/yjwjy/ShoppingBench

## Introduction

Large language models (LLMs) have empowered agents with impressive abilities in task automation and decision-making, leading to growing interest from both academia and industry (Yao et al. 2024). In recent years, a variety of agent benchmarks have been introduced to systematically assess language agent performance across different scenarios. These benchmarks typically focus on evaluating end-to-end capabilities such as task planning, tool using, and reasoning. As a highly practical ﬁeld with broad application prospects, e-commerce has naturally become a key focus for evaluating agent capabilities.

However, existing benchmarks for evaluating language agents in e-commerce primarily focus on straightforward user

*These authors contributed equally. †Corresponding author. Copyright © 2026, Association for the Advancement of Artiﬁcial Intelligence (www.aaai.org). All rights reserved.

intents such as locating and purchasing products (Zhou et al. 2023; Yao et al. 2022a). In practice, e-commerce users often pursue multifaceted goals that extend beyond mere product acquisition. For example, as shown in Figure 1, language agent is expected to optimize discounts, combine multiple orders to qualify for free shipping, or verify total expenditures against budget constraints. Such grounded user intents require language agents to perform multi-step reasoning, effectively utilize domain-speciﬁc knowledge, and leverage external tools to fulﬁll complex user instructions. Despite increasing interest in language agents as autonomous decisionmakers (Mialon et al. 2023), current agent benchmarks in e-commerce rarely incorporate these realistic and nuanced user intents.

Beyond above agent benchmarks, previous e-commerce datasets primarily address isolated or narrowly scoped downstream tasks (Jin et al. 2023; Reddy et al. 2022; Yangning et al. 2023; Liu et al. 2023; Jia et al. 2022). While largescale benchmarks such as Shopping MMLU (Jin et al. 2024) and ChineseEcomQA (Chen et al. 2025) have been proposed based on large e-commerce corpora, they mainly focus on question answering(Wang et al. 2025) and skill-based evaluation rather than end-to-end agent performance. This limits their effectiveness in assessing a language agent’s ability to fulﬁll complex user intents in real-world shopping scenarios.

To bridge the above gaps, we propose ShoppingBench, a large-scale end-to-end shopping benchmark comprising 3,310 user instructions, designed to encompass progressively challenging levels of grounded intent in shopping scenarios. Speciﬁcally, we propose a scalable framework to simulate user instructions based on various intents derived from sampled real-world products. To facilitate consistent and reliable evaluations, we provide a large-scale e-commerce shopping sandbox that serves as an interactive simulated environment, incorporating over 2.5 million real-world products. To automatically evaluate the quality of language agents, we propose a series of new metrics based on different intent constraints.

In addition, we also propose a trajectory distillation strategy, where tool-use trajectories are generated by the GPT-4.1, and using rejection sampling to ﬁlter low-quality trajectories. Then, we use these synthetic trajectories to train Qwen3- 4B with Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL), which can signiﬁcantly improve the performance. As a result, our trained language agent achieves com-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

33521

<!-- Page 2 -->

I am looking for a sunscreen with invisible shield tech, SPF 60, and cream texture. Also, need a foundation stick with full coverage, oil control, and a built-in brush… My budget is only 103, but I have a voucher with the following rules: 1. It is valid only when the total price of the products exceeds 83…

？

Shopping Sandbox

User

Agent

Reasoning: From the search results, I need to identify products… Tool Call: view_product {product_ids}

Reasoning: Based on the products, voucher and budget … write Python code to judge … Tool Call: python_execute {code}

Reasoning: The task has been successfully completed… and fit within their budget. Tool Call: recommend_product {product_ids}

foundation stick sunscreen

Product Category

Invisible shield tech SPF 60 cream texture

Product

Budget Checking

Voucher

1. Valid for all products. 2. Minimum order value: 83. 3. Save 10%, limit 10.

… full coverage oil control built-in brush

Products

Voucher

Budget Order Total

Check

Reasoning: I need to search for two products: a brightening sunscreen with specific features and a foundation stick with detailed requirements… Tool Call: find_product {product attribute}, find_product {product attribute}

Action

Obs

…

**Figure 1.** An illustration to depict a real-world user instruction with complex intent. Unlike previous agent benchmarks that solely focus on basic product purchases, ours incorporates coupon usage and optimal product combination within a budget.

petitive performance compared to GPT-4.1 agent.

Our experiments illustrate that even the best-performing language agent (GPT-4.1-based) achieves a success rate below 50%, underscoring the challenge of our benchmark. Quantitative and qualitative analysis of failure cases reveals existing agents’ limitations in understanding user instruction with complex intent and choosing appropriate tools. These ﬁndings underscore the need for advances in agent architecture, tool usage, problem decomposition, and web information integration.

Our contribution can be summarized as follows:

• We propose a scalable framework to simulate diverse user instructions and provide a sandbox environment with over 2.5 million products for consistent and interactive evaluation.

• We propose new automatic evaluation metrics, grounded in intent constraints, to rigorously assess language agents in e-commerce shopping tasks.

• We propose a trajectory distillation strategy to synthesize training data, ﬁlter out low-quality trajectories using our proposed automatic evaluation metric, and then use SFT and RL to efﬁciently distill GPT-4.1’s abilities into a smaller model, which achieves comparable performance.

• We evaluate 17 existing language agents, along with our ﬁne-tuned Qwen3-4B agent. Even the best-performing model, GPT-4.1, achieves a success rate below 50%, highlighting the challenge of our benchmark.

## Related Work

Existing benchmarks related to e-commerce shopping can generally be categorized into two types: agent benchmarks and task-oriented dialogue benchmarks.

Agent Benchmarks Recent advances in language agents have generated signiﬁcant interest regarding their potential to drive unprecedented automation across diverse industries (Chen et al. 2021; Yao et al. 2022b). Evaluating the capabilities of language models as agents requires examining their ability to aggregate information for multi-step reasoning and autonomous decisionmaking, as well as their proﬁciency in effective tool utilization (Huang et al. 2023; Schick et al. 2023; Yao et al. 2024). Recent research focus on developing domain-speciﬁc agents (Mialon et al. 2023) to address these challenges. E-commerce represents an especially realistic and pressing application scenario for language agents. Thus, more recent studies adopted web shopping (Zhou et al. 2023; Yao et al. 2022a) as a key benchmark domain to evaluate the capabilities of language agents in fulﬁlling user purchase requests. Most existing benchmarks for agents in e-commerce scenarios primarily focus on evaluating the user’s basic intent, namely, the successful purchase of a product. These benchmarks typically adopt a web shopping setting and deﬁne task success based on whether an order can be successfully placed.

However, in real-world e-commerce scenarios, user intents often extend beyond the basic goal of ﬁnding products. More complex and realistic intents, such as combining orders for free shipping or optimizing for coupon discounts, require language models to reason with speciﬁc e-commerce knowledge that are not adequate in existing agent benchmarks. To bridge this gap, we propose ShoppingBench, an end-to-end shopping benchmark for language agent, which grounds a wide range of realistic user intents.

E-commerce Datasets Previous e-commerce benchmarks mainly comprise isolated or narrowly related downstream tasks (Jin et al. 2023; Reddy et al. 2022; Yangning et al. 2023; Liu et al. 2023; Jia et al.

33522

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-07.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-11.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-002-figure-16.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

Stage1: Product Sampling

Stage3: User Instruction Simulation

Intents

Challenging level

Product Finder: Hey, I'm looking for a spicy 'BUTCHERON' snack in a big size, preferably in a brown pouch. It should be part of LazFlash deals and cost less than 188 pesos…

Products

Product Finder

Coupon & Budget

Sampling

Vouchers

Task: Write a brief and informal query to simulate a user searching for a product on the e-commerce platform based on... Product Fields: 1. The title is… 2. The flavor is spicy. 3...

Ta s k: Write a brief and informal query to simulate a user searching for a shop that sells multiple products on the… Product 1 Fields: 1. The title… 2. The color is yellow...

Multi-products Seller: Hey, can you help me find a shop that sells both of these items? First... Second… It should come with free shipping, cash on delivery, and cost more than 121 PHP.

User Instructions Prompt Templates

Stage 2: Field Sampling

Title

Service

Flavor

Price

Attributes

SKU Options

Product Fields plain spicy

Variation small big

Color red brown

… green middle sweat chosen w/o chosen

Task: Write… to simulate a user searching for one or more products within the budget on the e-commerce platform based... Product 1 Fields: 1. The title… Product 2 Fields: 1. The title …

Coupon & Budget: Looking for… My budget is only 103, but I have a voucher with the following rules: 1. It is valid only when total price of the products exceeds 83...

Task: Write… based on the given Problem, Answer, Title, and Product Title. It must contain the Problem and convey an intention to purchase the product corresponding to Title...

Knowledge: At which university did mechanical engineer Chen Gang serve as an assistant professor from 1993 to 1997? I would like to purchase a basketball jersey from that team…

Multi-products Seller

Knowledge

Shops

Simple QA

**Figure 2.** Construction of our ShoppingBench. Our benchmark encompasses four types of real-world user purchase intents: Products Finder, Knowledge, Multi-products seller, and Coupon & Budget, with complexity increasing progressively.

2022). Recently, multidimensional benchmarks such as Shopping MMLU (Jin et al. 2024) and ChineseEcomQA (Chen et al. 2025) have been constructed based on comprehensive e-commerce corpora. EcomScriptBench (Wang et al. 2025) is proposed to evaluate the ability of language models to generate plans with scripts and recommend products. However, these benchmarks primarily focus on conceptual and skillbased question answering in e-commerce, which poses challenges for the end-to-end evaluation of e-commerce agents.

## Problem Formulation

Each trajectory can be represented as a partially observable Markov decision process (POMDP) (U, S, A, T, O, R). It consists of the following components: a natural language instruction space U, a state space S, an action space A, an observation space O, a transition function T, and a reward function R. When a shopping agent performs an action, it interacts with the environment by invoking tools, which generates observations and updates the state. This process can be mathematically represented as:

(st+1, ot+1) = T (st, at)

where st represents the state at time step t, at denotes the action executed by the agent, T is the transition function, st+1 is the updated state, and ot+1 is the observation.

At the terminal state, we evaluate whether the predicted products in the terminal state, sT, satisfy all the requirements speciﬁed in the user’s instructions, U. The task is deemed successfully completed if:

success =

!1, if all conditions in U are met in sT, 0, otherwise.

ShoppingBench Construction

In this section, we introduce the construction of our Shopping- Bench, which consists of three key components: a simulated interactive environment, intent-grounded user instructions, and a predeﬁned tool set.

Grounded Shopping Intention

As shown in Figure 2, our ShoppingBench includes the following four real-world user purchase intents, with the challenges progressively increasing for each intent.

Products Finder. The language agent needs to ﬁnd the corresponding product based on the user’s description of the product attributes.

Knowledge. The language agent needs to infer the knowledge in the user’s question and identify the related product.

33523

<!-- Page 4 -->

Multi-products seller. The language model needs to ﬁnd the store that sells all the products described by the user.

Coupon & Budget. The language agent needs to understand the voucher rules and ﬁnd optimal product combinations within a budget.

Shopping Sandbox Implements

To ensure more consistent and reliable evaluations, we offer a large-scale shopping sandbox, serving as a simulated interactive environment that incorporates over 2.5 million real-world products sourced from Lazada.com. In this environment, an AI shopping agent is tasked with recommending suitable products tailored to the user’s real-world intents by leveraging a variety of tools. To support the API tool, we build two search engines: one for the product database and another for web-based knowledge.

Search engine. We use Pyserini(Lin et al. 2021) to build a product search engine, utilizing the BM25 sparse retrieval model to construct the index ofﬂine.

Web Search engine. We encapsulated a web search tool using Serper1, enabling access to online searches.

Intent-Grounded Instruction Generation

In this subsection, we present the framework for generating intent-grounded user instructions, which encompasses three key stages.

Stage I: Sampling Real-World Products We begin by sampling a diverse set of real-world products from our shopping sandbox, ensuring coverage across a wide range of constraints such as variations in categories, brands, attributes, and service. The sampling distribution of the product can be seen in Appendix A. Notably, for the Knowledge intent, SimpleQA (Wei et al. 2024) is used to link products, ensuring the veriﬁability of the responses. For the Coupon & Budget intent, we also synthesize multiple voucher rules and sample products that meet these rule requirements.

Stage II: Extracting Product Fields In the second stage, speciﬁc ﬁelds are extracted from the sampled products. These ﬁelds include detailed information such as product titles, attributes, associated services, and other relevant meta data. This structured information forms the basis for developing realistic user scenarios.

Stage III: Simulating User Queries Using the extracted product ﬁelds, we employ GPT-4.1 to simulate diverse and realistic user queries. These queries are carefully tailored to align with each purchase intent, which can be seen in Figure 2. Each simulated user instruction is intent-speciﬁc and grounded in real-world scenarios, aiming to evaluate the model’s capability to understand and navigate the constraints inherent in e-commerce tasks.

1https://serper.dev/

Interaction Tools

We provide a set of API tools to interact with our shopping sandbox. As shown in the Figure 3, we design six API tools: retrieving product lists, viewing product details, calculating discounts and budgets, retrieving web knowledge, recommending products, and terminating states. Each invocation of a tool is formalized as an action at, speciﬁcally represented as tool_name(para), where tool_name denotes the name of the tool being called, and para represents the parameters passed to the tool. Upon invocation, the tool returns an observation ot+1, which is the result or output of tool execution.

## Evaluation

Given a user instruction, the model outputs its reasoning process as well as an action in the form of a tool call in each step(Yao et al. 2022b). Based on the predicted tool calling, we parse the list of invoked tools and execute the corresponding functions, returning the observation. Then the agent generates the next round of reasoning and action predictions based on the current observation and the user instruction. This process is repeated until a terminal tool is called to end the current trajectory. In the terminal state, we compare the predicted products with the target products to automatically determine whether the task has been successfully completed.

Constrain Scores

We design the Absolute Success Rate (ASR) and Cumulative Average of the product Relevance (CAR) as metrics, which calculated from the following constrain scores.

Product Relevance Score. To measure the relevance between the predicted product and the target product, we consider three dimensions: title similarity, price similarity, and product feature similarity. The formulation can be seen as follows:

rpro = Isim→0.5 + Imin↑p↑max + |Ft →Fp|

2 + |Ft|, (1)

where Isim→0.5 indicates that when the title similarity between the predicted product and the target product exceeds the threshold (set to 0.5), the value is 1. Imin↑p↑maxindicates that when the price p is within the target product price range [min, max], the value is 1. |Ft →Fp| is the number of overlapping features, and |Ft| is the total number of features in the target product.

Knowledge Constrain Score. For the Knowledge intent, we evaluate whether the predicted products have the correct knowledge attribute, as follows:

rkw =

!1, if knowledge_attribute in title, 0, otherwise. (2)

Shop Constrain Score. For Multi-products seller intents, to assess whether the predicted products satisfy the user’s request that all products come from the same shop, we deﬁne the shop relevance score as follows:

33524

<!-- Page 5 -->

[

{

"price": 99.0, "product_id": "3064298409", "service”: ["freeShipping", "COD"], "shop_id": "2280917", "sold_count": 1, "title": "4PCS Car Wheel… "},... ]

def view_product_information( product_ids: str) [

{

"attributes": {

"color_family": ["red”, "black"], model: ["car tire valve stem caps"]}, "description": "", "product_id": "3064298409", "short_description": "⭐Features⭐" "●Protective Car Tyre Valve…", "sku_options":

{ "1": { "color": "black" },

"2": { "color": "blue" }} },... ]

def find_product( query: str, page: int, shop_id: str, price: str, sort: str, service: str)

{

"observation": {

"total_price": 112.0, "discount": 10.0, "final_price": 102.0 }, "success": true }

def python_execute( code: str)

{

"observation": [{

"time": "2025/07/14 13:56", "title": "ZEBRA SARASA Color Gel Pen JJZ58 3pcs

"content": “ZEBRA SARASA Color Gel Pen JJZ58 3pcs... ",

},...], "success": true}

def web_search( query: str, max_results: int) [

{

"product_id":

"3064298409", },... ]

{

" status": "success"}

def recommend_product( product_ids: str)

def terminate( status: str)

API Tool Pool

**Figure 3.** ShoppingBench provides six API tools designed to facilitate agent interaction with our shopping sandbox environment.

rshop =

!1, nt = np and |Srec| = 1 0, otherwise (3)

The score is 1 when the number of predicted products np is equal to the number of target products nt and all predicted products come from the same store (|Srec| = 1).

Budget Constrain Score. For Coupon & Budget intent, to evaluate whether the predicted products meet the user’s budget, we deﬁne the budget score as follows:

rbudget =

!1, if total_price ↑budget, 0, otherwise. (4)

Overall Metrics In this subsection, we detailed introduce our metrics: the Absolute Success Rate (ASR) and the Cumulative Average of the product Relevance (CAR).

Cumulative Average of the Product Relevance For each intention, we compute the Cumulative Average of the product Relevance (CAR) between the predicted and target products, deﬁned as:

Apro = 1 n n " i=1

1 ni ni " j=1 r(j)

pro, (5)

where n indicates the number of samples. 1 ni

#ni j=1 r(j)

pro represents the average product relevance within the i-th sample. ni indicates the number of products in i-th sample.

Absolute Success Rate We also further design the following metrics to measure the absolute success rate (ASR) for each intent.

Products Finder: For intents where the user wants to locate a particular product according to its attributes, we use the product relevance score rpro (Equation 1) to determine task success.

Spro = 1 n n " i=1 ω(r(i)

pro = 1), (6)

where, the indicator function ω(·) is deﬁned as:

ω(r(i)

pro = 1) =

$

1, if r(i)

pro = 1, 0, otherwise. (7)

Knowledge: For intents where user instructions require knowledge reasoning, we include the knowledge constraint score rkw (Equation 2).

Skw = 1 n n " i=1 ω(r(i)

pro = 1, r(i)

kw = 1). (8)

33525

<!-- Page 6 -->

Models Products Finder Knowledge Multi-products seller Coupon & Budget Avg. ASR(%) CAR(%) ASR(%) CAR(%) ASR(%) CAR(%) ASR(%) CAR(%)

Closed-Source Large Language Models

GPT-4.1 59.6 83.6 62.0 67.3 46.4 79.2 30.4 72.8 48.2 o3-mini 42.0 62.6 51.3 57.3 36.8 50.3 31.6 61.4 39.2 GPT-4o 52.4 71.5 50.0 58.7 24.0 52.4 25.2 65.6 36.6 GPT-4o-mini 33.2 46.9 28.0 31.3 10.4 52.7 11.6 54.6 20.0 Gemini-2.5-Flash 49.2 71.3 39.3 46.7 32.0 40.9 22.8 55.0 35.4 Claude-4-Sonnet 48.0 73.1 51.3 62.7 37.6 59.5 24.0 72.2 39.0 Qwen2.5-max 58.4 81.0 42.7 50.7 22.8 67.3 22.4 65.8 35.9

Open-Source Large Language Models

DeepSeek-R1 53.2 75.8 44.0 53.3 37.2 51.5 24.4 43.9 39.2 DeepSeek-V3 54.8 75.8 48.0 54.7 22.8 46.9 21.2 55.3 35.4 Qwen3-235B-A22B 49.2 77.2 40.0 46.7 28.8 56.3 14.4 55.3 32.3 Qwen3-32B 51.6 77.6 45.3 54.0 25.6 54.2 18.0 63.8 34.0 Qwen3-14B 46.0 70.4 30.0 37.3 19.2 53.1 12.4 58.1 26.6 Qwen3-8B 40.0 65.8 22.7 27.3 13.6 31.7 11.2 53.2 21.8 Qwen3-4B 36.4 66.4 18.7 26.0 8.8 29.8 8.4 45.5 18.0 Gemma-3-27B 32.0 48.5 46.7 57.3 18.0 65.4 17.2 62.5 26.5 Gemma-3-12B 27.2 42.5 32.0 36.7 9.6 51.7 13.6 55.7 19.3 Gemma-3-4B 24.4 40.1 16.7 20.7 0 31.1 4.8 30.7 10.9

Ours

SFT-Qwen3-4B 55.6 81.1 52.7 59.3 39.2 77.9 30.4 76.0 43.6 SFT+RL-Qwen3-4B 60.8 86.1 46.7 51.3 53.2 85.5 33.2 79.0 48.7

**Table 1.** Main results of different language agents on our ShoppingBench, including absolute success rate (ASR) and cumulative average of the product relevance (CAR). The average reported is domain-weighted ASR, rather than task-weighted.

Multi-products seller: For the intent where users want to ﬁnd multiple products sold by the same shop, we introduce the shop constraint score rshop (Equation 3).

Sshop = 1 n n " i=1 ω(1 ni ni " j=1 r(j)

pro = 1, r(i)

shop = 1). (9)

Coupon & Budget: For the intent with budget requirements, we introduce the budget constraint score rbudget (Equation 4). The formulation is deﬁned as follows:

Sbudget = 1 n n " i=1 ω(1 ni ni " j=1 r(j)

pro = 1, r(i)

budget = 1). (10)

Shopping Agent Training We utilize synthetic trajectories to train Qwen3-4B backbone using Supervised Fine-Tuning (SFT) and tool-calling based Reinforced Learning (RL).

Trajectory Distillation. We leverage GPT-4.1 to generate tool-calling trajectories from 2,410 user instructions. To ensure high data quality, we apply rejection sampling based on our evaluation metrics, retaining only trajectories that achieve absolute success. Speciﬁcally, any trajectory with a ﬁnal success score strictly less than 1 is ﬁltered out. While this stringent threshold discards approximately 50% of the generated data, it effectively preserves a high-quality subset of fully successful examples.

Cold Start with SFT. We sample multiple steps from each trajectory. The ﬁnal training dataset includes 5,552 steps. The model input includes the user instruction as well as the observation (e.g., a retrieved product list). The output consists of a reasoning trace (the process) and the next action (toolcalling). Then, we perform SFT on Qwen3-4B to enhance the model’s ability to understand complex instructions, process multi-round observations, and predict actions.

Reinforced Tool Calling. To further enhance the model’s tool-calling capabilities, we apply GRPO (Shao et al. 2024) with the tool reward(Qian et al. 2025) to continue training the SFT-Qwen3-4B model. The overall reward function combines a format reward and a tool-matching reward.

The tool-matching reward is deﬁned as:

Rmat = rn + rk + rv ↓[0, Smax], (11)

where rn denotes the tool name match rate, rk is the parameter name match rate, and rv is the parameter value match rate. Here, Smax represents the max score for Rmat. This raw score is then normalized to the interval [↔3, 3]:

Rtool = 6 · Rmat

Smax

↔3. (12)

33526

<!-- Page 7 -->

**Figure 4.** Breakdown of failed GPT-4.1 agent trajectories in ShoppingBench, categorized as attribute mismatch (#AM), metric issue (#MI), product missing (#PM), constraint not satisﬁed (#CNS), and knowledge error (#KE).

The format reward Rformat evaluates structural correctness. It equals 1 if the output strictly adheres to the required JSON schema (validated via regex), and 0 otherwise.

The ﬁnal reward combines both components:

Rﬁnal = Rtool + Rformat ↓[↔3, 4]. (13)

## Experiments

Baselines. We evaluate 17 language agents on our ShoppingBench, including leading closed-source models (e.g., GPT-4.1, Claude-4-Sonnet, Qwen2.5-max) and open-source models (e.g., DeepSeek-R1, Qwen3-32B, Gemma-3-27B). Additionally, we further train Qwen3-4B with synthetic trajectories using supervised ﬁne-tuning and reinforcement learning. The training details can be seen in Appendix B.

Dataset. The ShoppingBench dataset consists of 3,310 user instructions in total, with 2,410 used for training and 900 for testing. The test set includes 150 samples for the Knowledge intent and 250 samples for each of the other intents. Detailed data statistics can be seen in Appendix C.

Main Results As shown in Table 1, we evaluated various language agents. The experimental results lead to the following conclusions:

• Overall Performance: On untrained language agents, GPT-4.1 achieves the highest overall performance, with an Absolute Success Rate (ASR) of 48.2%. Among opensource models, DeepSeek-R1 achieves the strongest overall performance, surpassing GPT-4o in average benchmarks. For simple intents such as product ﬁnding, GPT-4.1

**Figure 5.** Correlation analysis between various factors and absolute success rates across different intents. Detailed can be seen in Appendix F.

reaches 59.6% ASR, with cumulative average of product relevance (CAR) up to 83.6%. However, the performance of GPT-4.1 drops signiﬁcantly on complex tasks such as the Coupon & Budget intent, falling to 30.4% ASR. These results highlight substantial room for improvement in handling complex, real-world e-commerce intents. • Effect of Synthetic Trajectories: Motivated by above observation, we synthesize trajectories using GPT-4.1, generating training data via rejection sampling, and employing ﬁne-tuning in conjunction with the GRPO algorithm to train the Qwen3-4B model, enabling it to learn tool-use capabilities. Experimental results indicate that our enhanced model achieved a remarkable improvement, with a 30.7% higher success rate compared to the original Qwen3-4B, even surpasses the performance of GPT-4.1 agent by 0.5% ASR. These ﬁndings highlight the effectiveness of our trajectory distillation and training strategy.

Further Analysis We further analyze the reasons behind the challenges presented by our benchmark, potential areas for improvement, and the rationale of the tool settings.

Failure Breakdown We sampled 60 failed trajectories from the GPT-4.1 agent and manually analyzed the causes of their failure. We identiﬁed ﬁve distinct types of errors, which are categorized and visualized in Figure 4. The largest proportion of failures is due to missing or mismatched product attributes. This is also evident in Table 1, where the cumulative product relevance is much higher than the absolute success rate, indicating that many failures are caused by partial mismatches in product attributes. Detailed case study can be seen in Appendix D.

33527

![Figure extracted from page 7](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-007-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 7](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-007-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 8 -->

**Figure 6.** Comparison between humans and Agents.

Models Knowledge Intent w/o web_search tool

ASR(%) CAR(%) kw Score(%)

GPT-4.1 50.0 (↗12) 56.0 (↗11.3) 52.7 (↗13.3) o3-mini 32.0 (↗19.3) 37.3 (↗20) 34.7 (↗19.3) GPT-4o 39.3 (↗10.7) 46.7 (↗12) 42.0 (↗8) Gemini 19.3 (↗20) 23.3 (↗23.4) 20.7 (↗22.6)

**Table 2.** Ablation of web_search Tool for Knowledge Intent.

Furthermore, we conducted a correlation analysis between different factors and success rates under various intents. We used the Pearson correlation coefﬁcient to quantify these relationships (Figure 5). The analysis revealed that viewing product details is strongly correlated with accuracy across all intents, while the frequency of web_search tool usage is highly correlated with success in the Knowledge intent.

Compared with human performance. We sampled 200 tasks and invite three professional and well-educated individuals to complete each task. As shown in Figure 6, we draw two conclusions: (1) Even human participants have space for improvement on the more challenging intents, highlighting the challenging of our benchmark. (2) Even for state-ofthe-art LLMs, there remains a noticeable performance gap compared to human performance.

Effect of Thinking. We explore the effectiveness of incorporating <think> process before action. As shown in Figure 7, we ﬁnd that for simple intents like searching for a single product, the agents without <think> outperforms the think-based agents. However, for complex intents involving coupons or budget constraints, reasoning enables the language agent to ﬁnd product combinations that better meet user needs.

Effect of Web Search Tool. As shown in the Table 2, after removing the web search tool, even the strong baselines exhibited varying degrees of performance degradation. This indicates two key points: (1) existing language agents have limitations regarding long-tail knowledge in the e-commerce

(a) Products Finder intent.

(b) Coupon & Budget intent.

**Figure 7.** Comparison of reasoning for Products Finder and Coupon & Budget.

domain; (2) the information gain provided by online access can effectively compensate for the agents’ deﬁciencies in long-tail knowledge.

## Conclusion

We introduce ShoppingBench, a large-scale end-to-end benchmark for grounded shopping scenarios, featuring 3,310 diverse user instructions and a realistic sandbox environment of over 2.5 million products. Our proposed simulation framework, automatic evaluation metrics, and trajectory distillation approach set a new standard for agent evaluation. Experiments on 17 language agents and our ﬁne-tuned Qwen3-4B agent, reveal a signiﬁcant performance gap, highlighting both the challenges and future opportunities in language agent research for e-commerce tasks.

33528

![Figure extracted from page 8](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-AAAI-shoppingbench-a-real-world-intent-grounded-shopping-benchmark-for-llm-based-agen/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

## References

Chen, H.; Lv, K.; Hu, C.; Li, Y.; Yuan, Y.; He, Y.; Zhang, X.; Liu, L.; Liu, S.; Su, W.; et al. 2025. Chineseecomqa: A scalable e-commerce concept evaluation benchmark for large language models. arXiv preprint arXiv:2502.20196. Chen, M.; Tworek, J.; Jun, H.; Yuan, Q.; Pinto, H. P. D. O.; Kaplan, J.; Edwards, H.; Burda, Y.; Joseph, N.; Brockman, G.; et al. 2021. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374. Huang, Y.; Shi, J.; Li, Y.; Fan, C.; Zhang, S.; Liu, Y.; Zhou, P.; Wan, Y.; Gong, N.; and Sun, L. 2023. MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use. Jia, M.; Liu, R.; Wang, P.; Song, Y.; Xi, Z.; Li, H.; Shen, X.; Chen, M.; Pang, J.; and He, X. 2022. E-ConvRec: a large-scale conversational recommendation dataset for Ecommerce customer service. In Proceedings of the Thirteenth Language Resources and Evaluation Conference, 5787–5796. Jin, W.; Mao, H.; Li, Z.; Jiang, H.; Luo, C.; Wen, H.; Han, H.; Lu, H.; Wang, Z.; Li, R.; Li, Z.; Cheng, M.; Goutam, R.; Zhang, H.; Subbian, K.; Wang, S.; Sun, Y.; Tang, J.; Yin, B.; and Tang, X. 2023. Amazon-M2: A Multilingual Multilocale Shopping Session Dataset for Recommendation and Text Generation. Jin, Y.; Li, Z.; Zhang, C.; Cao, T.; Gao, Y.; Jayarao, P. S.; Li, M.; Liu, X.; Sarkhel, R.; Tang, X.; et al. 2024. Shopping MMLU: A Massive Multi-Task Online Shopping Benchmark for Large Language Models. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track. Lin, J.; Ma, X.; Lin, S.-C.; Yang, J.-H.; Pradeep, R.; and Nogueira, R. 2021. Pyserini: A Python Toolkit for Reproducible Information Retrieval Research with Sparse and Dense Representations. In Proceedings of the 44th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2021), 2356–2362. Liu, Y.; Zhang, W.; Dong, B.; Fan, Y.; Wang, H.; Feng, F.; Chen, Y.; Zhuang, Z.; Cui, H.; Li, Y.; et al. 2023. U-need: A ﬁne-grained dataset for user needs-centric e-commerce conversational recommendation. In Proceedings of the 46th international ACM SIGIR conference on research and development in information retrieval, 2723–2732. Mialon, G.; Fourrier, C.; Wolf, T.; LeCun, Y.; and Scialom, T. 2023. Gaia: a benchmark for general ai assistants. In The Twelfth International Conference on Learning Representa- tions. Qian, C.; Acikgoz, E. C.; He, Q.; Wang, H.; Chen, X.; Hakkani-Tür, D.; Tur, G.; and Ji, H. 2025. Toolrl: Reward is all tool learning needs. arXiv preprint arXiv:2504.13958. Reddy, C.; Màrquez, L.; Valero, F.; Rao, N.; Zaragoza, H.; Bandyopadhyay, S.; Biswas, A.; Xing, A.; and Subbian, K. 2022. Shopping Queries Dataset: A Large-Scale ESCI Benchmark for Improving Product Search. Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli, M.; Hambro, E.; Zettlemoyer, L.; Cancedda, N.; and Scialom,

T. 2023. Toolformer: Language models can teach themselves to use tools. Advances in Neural Information Processing Systems, 36: 68539–68551. Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.; Zhang, H.; Zhang, M.; Li, Y.; et al. 2024. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. Wang, W.; Cui, L.; Liu, X.; Nag, S.; Xu, W.; Luo, C.; Sarwar, S. M.; Li, Y.; Gu, H.; Liu, H.; et al. 2025. EcomScriptBench: A multi-task benchmark for e-commerce script planning via step-wise intention-driven product association. arXiv preprint arXiv:2505.15196. Wei, J.; Karina, N.; Chung, H. W.; Jiao, Y. J.; Papay, S.; Glaese, A.; Schulman, J.; and Fedus, W. 2024. Measuring short-form factuality in large language models. arXiv preprint arXiv:2411.04368. Yangning, L.; Ma, S.; Wang, X.; Shen, H.; Jiang, C.; Zheng, H.; Xie, P.; Huang, F.; and Jiang, Y. 2023. EcomGPT: Instruction-tuning Large Language Model with Chain-of- Task Tasks for E-commerce. Yao, S.; Chen, H.; Yang, J.; and Narasimhan, K. 2022a. Webshop: Towards scalable real-world web interaction with grounded language agents. Advances in Neural Information Processing Systems, 35: 20744–20757. Yao, S.; Shinn, N.; Razavi, P.; and Narasimhan, K. 2024. ε-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. arXiv:2406.12045. Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan, K.; and Cao, Y. 2022b. ReAct: Synergizing Reasoning and Acting in Language Models. Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; Lo, R.; Sridhar, A.; Cheng, X.; Ou, T.; Bisk, Y.; Fried, D.; et al. 2023. WebArena: A Realistic Web Environment for Building Autonomous Agents. In The Twelfth International Conference on Learning Representations.

33529
