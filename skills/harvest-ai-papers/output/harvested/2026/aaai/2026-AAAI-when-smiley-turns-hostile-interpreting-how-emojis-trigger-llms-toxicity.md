---
title: "When Smiley Turns Hostile: Interpreting How Emojis Trigger LLMs’ Toxicity"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40296
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40296/44257
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# When Smiley Turns Hostile: Interpreting How Emojis Trigger LLMs’ Toxicity

<!-- Page 1 -->

When Smiley Turns Hostile: Interpreting How Emojis Trigger LLMs’ Toxicity

Shiyao Cui1, Xijia Feng3, Yingkang Wang1, Junxiao Yang1, Zhexin Zhang1

Biplab Sikdar3, Hongning Wang1, Han Qiu†2, Minlie Huang†1

1The Conversational AI (CoAI) group, DCST, Tsinghua University 2Tsinghua University 3Department of Electrical and Computer Engineering, National University of Singapore cuishiyao@foxmail.com, aihuang@tsinghua.edu.cn

## Abstract

Emojis are globally used non-verbal cues in digital communication, and extensive research has examined how large language models (LLMs) understand and utilize emojis across contexts. While usually associated with friendliness or playfulness, it is observed that emojis may trigger toxicity generation in LLMs. Motivated by such a observation, we aim to investigate: (1) whether emojis can clearly enhance the toxicity generation in LLMs and (2) how to interpret this phenomenon. We begin with a comprehensive exploration of emoji-triggered LLM toxicity generation by automating the construction of prompts with emojis to subtly express toxicity. Experiments across 5 mainstream languages on 7 famous LLMs along with jailbreak tasks demonstrate that prompts with emojis could easily induce toxicity. To understand this phenomenon, we conduct model-level interpretations spanning semantic cognition, sequence generation and tokenization, suggesting that emojis can act as a heterogeneous semantic channel to bypass the safety mechanisms. To pursue deeper insights, we further probe the pre-training corpus and uncover potential correlation between the emoji-related data polution with the toxicity generation behaviors.

## Introduction

Emojis are non-verbal cues commonly used in digital communication to convey emotions, ideas, and abstract concepts (Hu et al. 2017), with over 90% global users incorporating them into everyday dialogues (Unicod 2025; Emojipedia 2024). The widespread usage has enabled emojis an important role in communication and the way large language models (LLMs) respond to modern popular languages 1.

Exploring how LLMs process emojis has attracted increasing research attention in recent years. Existing studies can be broadly categorized into two lines. The first focuses on emoji comprehension, where researchers perform comparative study about how humans and LLM understand emojis towards semantic expression (Peng et al. 2023; Lyu et al. 2024), sentiment popularity (Zheng, Lyu, and Luo 2025) and social media analysis (Zhou et al. 2025; Lyu et al. 2025). The second centers on emoji usage, investigating how LLMs incorporate emojis in text generation (de Janeiro 2023; Lyu

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

1Warning: this paper contains potentially sensitive contents.

**Figure 1.** Examples of rejection towards harmful requests in plain texts and fulfillment toward the prompt with emojis.

et al. 2024; Jain et al. 2025), and how the usage patterns differ from humans (Michael and Kenneth 2024). Researches above highlight the growing importance of understanding emojis in the context of LLM development and evaluation.

While emojis are generally perceived as symbols of casual or friendly expression (Zhukova and Herring 2024), we observe that they can trigger toxicity generation in LLMs. As Figure 1 shows, the harmful request expressed with plaintext prompt is refused by GPT-4o, while replacing a few words with semantically similar emojis can elicit a response. To mitigate the possibility of randomness, we perform pilot experiments across multiple models using 50 widely used toxic queries (Yan et al. 2025) and consistently observed similar phenomenon. Notably, the toxicity generation ratio of prompts with emojis in GPT-4o was nearly 50% higher than that of their plain-text counterparts, suggesting that emojis can influence the harmful generation of LLMs.

Given the prevalence and low barrier to emoji usage, it deserves a deep investigation to uncover the potential risks associated with emojis. Hence, this paper aims to perform a systematic study of (1) whether emojis can significantly enhance the toxicity generation in LLMs and (2) how to interpret this phenomenon. To fulfill the above goal, our research contains three aspects as follows:

(1) Explore the emoji-triggered toxicity generation in

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

30431

![Figure extracted from page 1](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

LLMs. Considering the linguistic characteristics of emojis, we automate the prompt construction with emojis for harmfulness expression and produce an emoji-version of the widely used red-teaming benchmark AdvBench (Zou et al. 2023). Experiments are performed across 5 major languages and 7 polular LLMs along with jailbreak tasks, providing a comprehensive view of such generation phenomenon.

(2) Interpret the phenomenon via model-level mechanisms. To speculate how emojis progressively affect model generation, we perform a top-down interpretation from three perspectives of LLMs: semantic cognition, sequence generation, and tokenization. The multifaceted interpretation reveals how LLMs understand, internally process and respond to prompts with emojis for subtle harmfulness expression.

(3) Probe the pre-training corpus for potential causes. Motivated by prior findings that pre-training token contexts could impact the model behaviors (Lin et al. 2025), we systematically examine emoji-related entries within pretraining corpora, aiming to uncover potential correlations between the emoji usage in pre-training contexts and our observed LLM toxicity generation from prompts with emojis.

Our key findings include: 1) Emoijs, when used as sensitive word replacement and toxicity camouflage elements, can effectively trigger toxicity generation in LLMs across mainstream languages, obviously more effective than their textual counterparts. 2) The tokenization disparity provides emojis a heterogeneous semantic expression channel and causes an internal representation gap with the raw harmful prompts, making LLMs less sensitive to the harmfulness in prompts. 3) A notable data pollution exist with emoji-related data entries in the pre-training corpora of LLMs, which may facilitate the malicious intent understanding and tolerance of toxicity generation with emojis 2.

Emoji Preliminary

Emojis, as a representative form of popular digital language, have played an increasingly important role in online communication. By September 2024, the Unicode Standard 16.0 (Unicode Consortium 2025) specified 3,790 emojis with 10 categories as Figure 2 shows. Comparing with other popular expression forms (e.g., abbreviations, acronyms and meme, etc.), emojis stand out for their broad accessibility and worldside popularity, particularly among younger users with steadily increasing usage across all age groups (Adobe 2022; Minich, Kerr, and Moreno 2025).

Linguistic Characteristics of Emojis

Considering previous studies, we induce three linguistic characteristics of emojis compared to the plain texts:

(1) Context-dependent means that emoji semantics vary with its surrounding contexts. For example, the official description of the emoji “Money with Wings” is transferring, or earning money, often with a flourish or sense of flair (EmojiPedia 2025). However, as shown in Figure 3, different surrounding contexts can shift its comprehension, giving rise to either benign or malicious inclinations.

2Code is available: https://github.com/thu-coai/EmojiAttack

**Figure 2.** The 10 categories of emojis and examples.

**Figure 3.** Illustration to the emoji characteristics.

(2) Tenor-shifting means that emojis can modulate emotional tonor, expressing nuances like playfulness or subtle sentiment beyond the literal meaning of the text. As shown in the 2nd example in Figure 3, the incorporation of transforms the task description into something resembling a simulated game mission, which may guide the model to interpret the prompt as less serious or more playful.

(3) Language-agnostic means that emojis are often interpretable across languages, universal regardless of the categories of the surrounding language contexts. Taking the last case in Figure 3 as an example, the emoji is used in diverse languages such as English, Chinese, and French, and universally expresses sentiments of heartbreak and sorrow, demonstrating its cross-linguistic usage salience.

The linguistic characteristics above make emojis a powerful complement to text, capable of significantly influencing how large language models interpret and understand the prompts embedded with emojis.

Emoji-triggered Toxicity Generation In this section, we first describe the insights to build prompts with emojis for toxicity generation, and then detail the prompt construction pipeline. Finally, we present the experimental results and necessary analysis.

Insight Considering the emoji characteristics of context-dependent and tenor-shifting, we leverage them to express toxicity subtly from the following two aspects:

(1) Sensitive words substitution. To evade the activation of safety mechanisms, semantically suggestive emojis could serve to replace the sensitive words (e.g., disable antivirus →, hatred →, phishing →). (2) Toxicity camouflage. To mislead the LLM into interpreting the request as benign, emojis could work to convey playfulness or task decoration, such as a riddle (),

30432

![Figure extracted from page 2](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-002-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 2](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-002-figure-10.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 3 -->

fictional scenario(), or harmless challenge (), thereby masking the underlying toxic intent.

Emoji Prompts Construction

We revise the raw harmful requests into the prompts with emojis to induce toxic generation, including three steps.

Step 1: Automatic craft. With the two insights above, we construct an instruction to guide a powerful LLM to automatically rewrite the raw request by incorporating emojis.

Step 2: Human revision. Given the automatic generation prompts, we conduct a human review to ensure that the prompts with emojis remain coherent and faithful to the original intent. If the semantics are deviated, manual revisions are performed. The top two rows in Figure 4 show a case of the raw and final rewritten prompt with emojis.

Step 3: Multilingual translation. Since emojis are language-agnostic, we translate the finalized prompts with emojis into several widely spoken languages, including Chinese, French, Spanish, and Russian. We employ the Google Translate API for this step instead of LLMs, as the latter may reject or alter harmful content due to safety mechanisms.

## Experimental Setup

Using the revised prompts with emojis, we conduct a range of experiments to investigate how they influence the toxicity generation behaviors of LLMs.

Setting. For a comprehensive investigation, two experiment settings are designed. 1) Emoji-induced generation: we experiment with harmful requests which are rewritten as prompts with emojis and evaluate them in multiple languages. 2) Emoji-enhanced generation: we apply our construction method to prompts generated by existing jailbreak techniques such as PAIR (Chao et al. 2025), TAP (Mehrotra et al. 2024), and DeepInception (Li et al. 2023), exploring whether emojis can enhance the existing jailbreak prompts. For a fair comparison in this setting, we maintain the original structure of raw jailbreak prompts but only replace the sensitive terms and add emojis for toxicity camouflage.

Dataset. Following previous studies (Chao et al. 2025), we adopt AdvBench (Zou et al. 2023), which spans 32 high-risk topics including hacking, bombing, murder, etc. In Setting-1, we rewrite all 520 instances in AdvBench in English as prompts with emojis for the main experiment. Then, we employ the the top-50 toxic and non-duplicate prompts (Mehrotra et al. 2024; Yan et al. 2025) for multilingual test in Setting-1 and all experiments in Setting-2.

Target Models. Experiments are performed on 7 representative models from different creators. The tested closed-source models include GPT-4o (2024-08-06) (OpenAI 2024), GPT-4-0613 (OpenAI 2023), Gemini-1.5pro (Google 2024a) and Gemini-2.0-flash (Google 2024b). For open-source models, we test Llama-3-8B-Instruct (Meta 2024), Qwen2.5-7B-Instruct (Team 2024b) and Qwen2.5- 72B-Instruct (Team 2024a). All experiments were repeated three times to account for randomness.

**Figure 4.** Cases of prompts with emojis and the ablation, where the latter two cases are illustration for Sec..

Evaluation. Following previous studies (Qi et al. 2024; Jiang et al. 2024; Zou et al. 2025), we utilize GPT-Judge upon GPT-4o for evaluation with two metrics: 1) Harmful Score (HS) rates a response from 1 to 5 to indicate its harmfulness, where score 1 and 5 represent harmless and extremely harmful respectively. 2) Harmfulness Ratio (HR) is defined as # of responses with HS=5

## of responses × 100, which counts the ratio of responses which are extremely harmful. Note that in our implementation, we prepend a prompt explicitly instructing the LLM to answer directly with a brief response, as the models tend to generate lengthy emoji explanations.

## Results

We present the results in Table 1 and Table 2. To reveal the impact of emojis, Table 1 also shows emoji ablation which reversely translates emojis in prompts into the corresponding text words (Emoji→w ⃝) and entirely remove emojis (Emoji→) as Figure 4 shows. Observations are as follows. 1) Emojis can elicit toxic generation across a wide range of LLMs. As the left part in Table 1 shows, harmful prompts revised with emojis achieve significantly higher HS and HR than their ablated versions, demonstrating the effectiveness of emojis in eliciting toxic generation. Meanwhile, comparing with Table 2, they also outperform prior representative jailbreak methods, PAIR, TAP, and Deep Inception, which further validates the advantage of emojis.

2) Emoji-induced toxic generation is transferable across languages. When the textual words in emoji-prompts are translated into various languages, the prompts still yield toxic generation as the right part in Table 1 shows. This indicates the transferability of emoji-induced toxicity across languages. Notably, the tested Chinese (ZH), French (French), Spanish (ES) and Russian (RU) are all high-resourced languages, reflecting the widespread risk that emojis can facilitate harmful generation across user groups.

3) Emojis could consistently enhance toxicity generation for jailbreak methods. To examine whether emojis can augment existing jailbreak techniques, we revise existing jailbreak prompts by replacing sensitive words with emojis and adding the toxicity camouflage ones. Results in Table 2 show clear performance gains, demonstrating that emojis can effectively boost the success of jailbreak and highlighting their generalizability for toxicity generation.

30433

![Figure extracted from page 3](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-003-figure-06.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Advbench-EN Multilingual Models Metric Emoji P. Emoji→w ⃝ Emoji→ Raw P. EN ZH FR ES RU

HS 3.98 1.68 (-2.30) 2.10 (-1.88) 1.00 3.88 3.68 4.34 3.80 3.24 GPT-4o HR 65.76 14.00 (-51.76) 13.00 (-52.76) 0.00 64.00 48.00 76.00 50.00 36.00 HS 3.33 1.77 (-1.56) 2.73 (-0.60) 1.02 3.20 2.56 3.56 3.58 3.26 GPT-4 HR 47.50 16.32 (-31.18) 15.48 (-32.02) 0.60 44.00 30.00 54.00 46.00 36.00 HS 4.22 3.57 (-0.65) 2.33 (-1.89) 1.33 4.16 4.42 4.02 4.28 3.52 Gemini-Pro HR 65.19 55.19 (-10.00) 21.90 (-43.29) 7.69 64.00 72.00 52.00 62.00 42.00 HS 4.15 2.72 (-1.43) 2.73 (-1.42) 1.10 4.36 3.80 4.18 4.24 3.78 Gemini-flash HR 64.04 42.76 (-21.28) 24.62 (-39.42) 2.00 68.00 46.00 70.00 68.00 60.00 HS 2.67 1.22 (-1.45) 2.16 (-0.51) 1.00 2.92 2.42 3.10 3.24 2.36 Llama3-8B HR 28.46 2.34 (-26.12) 7.12 (-21.34) 0.00 28.00 24.00 24.00 36.00 20.00 HS 3.40 2.50 (-0.90) 2.76 (-0.64) 1.00 3.58 2.94 2.83 2.40 3.14 Qwen2.5-7B HR 40.19 16.33 (-23.86) 16.13 (-24.06) 0.00 46.00 38.00 20.00 16.00 30.00 HS 3.38 2.50 (-0.88) 3.26 (-0.12) 1.00 3.62 2.76 3.14 2.84 3.16 Qwen2.5-72B HR 39.81 30.25 (-9.56) 32.51 (-7.30) 0.00 44.00 44.0 40.00 32.00 28.00

**Table 1.** Results for emoji-induced generation (Setting-1) and emoji ablation. Model names are in short due to space limitation.

Models PAIR PAIR+Emoji ∆↑ TAP TAP+Emoji ∆↑ Deep. Deep.+Emoji ∆↑

GPT-4o 40.00 48.00 +8.00 50.00 60.00 +10.00 2.00 32.00 +30.00 GPT-4 44.00 54.00 +10.00 46.00 58.00 +12.00 8.00 12.00 +4.00 Gemini-Pro 44.00 64.00 +20.00 60.00 76.00 +16.00 36.00 60.00 +24.00 Gemini-flash 60.00 74.00 +14.00 58.00 64.00 +6.00 8.00 14.00 +6.00 Llama3-8B 14.00 38.00 +24.00 6.00 24.00 +18.00 6.00 12.00 +6.00 Qwen2.5-7B 54.00 66.00 +12.00 38.00 52.00 +14.00 24.00 26.00 +2.00 Qwen2.5-72B 44.00 54.00 +10.00 36.00 50.00 +14.00 6.00 30.00 +24.00

**Table 2.** Results of HR for emoji-enhanced generation with jailbreak prompts (Setting-2). Model names are in short.

Ablation to Emoji Functions

We further conduct an ablation to the two aspects of emoji usage: sensitive word substitution and toxicity camouflage. Given the positive correlation between overall AdvBench performance and top-50 toxic requests, we conduct ablation on the top-50 set, with results shown in Table 3.

1) w/o s.e. denotes the setting where emojis used to substitute sensitive words are replaced back with their textual sensitive words, while the toxicity camouflage emojis preceding the prompt are retained, as shown in Figure 4. A significant performance drop is observed across all models under this setting, highlighting the critical role of emoji sensitive word substitution in enabling successful toxic generation.

2) w/o d.e. refers to the removal of toxicity camouflage ahead of the emoji-prompt as the last case shown in Figure 4. This results in a moderate decline in harmfulness ratio and even some model performances remain unaffected. It reveals that decorative elements seem to contribute less than the sensitive substitution emojis. However, it does not mean their complete ineffectiveness. Comparing w/o s.e with the Emoji→w ⃝in Table 1, we observe that placing camouflage emojis before prompts with sensitive terms still leads to improved toxic generation, revealing its effectiveness.

Interpretation

In this section, we perform a top-down interpretations for how emojis trigger the LLM toxicity generation. The inter-

## Model

Emoji. w/o s.e. ∆ w/o d.e. ∆

GPT-4o 64.00 40.00 -24.00 58.00 -6.00 GPT-4 44.00 36.00 -8.00 42.00 -2.00 Gemini-Pro 64.00 56.00 -8.00 58.00 -6.00 Gemini-flash 68.00 54.00 -14.00 54.00 -14.00 Llama3-8B 28.00 0.00 -28.00 28.00 -0.00 Qwen2.5-7B 46.00 36.00 -10.00 44.00 -2.00 Qwen2.5-72B 44.00 10.00 -34.00 44.00 -0.00

**Table 3.** Ablation to emoji functions for Harmfulness Ratio.

pretation is perform towards LLMs spanning the semantic cognition, sequence generation, and tokenization, where we first examine whether LLMs recognize malicious intent conveyed by emojis, then investigate how emojis influence the generation process internally.

RQ1: Do LLMs perceive emoji toxicity. We investigate whether LLMs can recognize harmful intent of which the sensitive words are expressed with emojis. To this end, we sample 100 raw harmful requests and directly replace the sensitive terms with semantically related emojis. The emoji prompts are fed into LLMs, which are instructed to assess whether the emojis convey toxicity with explanations.

We experiment with representative models from different creators and present results in Table 4. We could see that most models successfully identify the malicious intent expressed by the emojis which substitute sensitive words, sug-

30434

<!-- Page 5 -->

## Model

GPT-4o Gemini-flash Llama3-8B Qwen2.5-7B

Ratio (%) 87.00 81.00 41.00 65.00

**Table 4.** Ratio of perceived toxicity from emoji prompts.

**Figure 5.** Response comparison: textual vs. emoji prompts

gesting that the emojis could serve as signals to sufficiently elicit harmful responses, leading to the observation:

Observation 1: Models can recognize the malicious intent expressed by emojis, yet how it bypasses safety mechanisms remain unclear.

RQ2: How do emojis influence generation. With the observation above, we intend to see how emojis influence the sequence-generation for harmful requests. Two analysis are performed with 100 pairs of raw harmful requests and its emoji-subsituted prompts. To specifically analyze the effects, we keep the original sentence structure and apply a straightforward replacement of sensitive words with related emojis (e.g., how to make a bomb →How to make a). 1) Prompt Attribution and Contribution Tracking (PACT) (Zhang et al. 2025) measures the emoji influence on the rejection response generation. With the first token in the rejection response as the target y, PACT is defined as the difference in the log probability (LP) of y between the raw harmful request x and its emoji-substituted counterpart x →{e}, which could be formulated as PACT(x, y) = LP(x →{e}, y) −LP(x, y), where a negative PACT value indicates the suppression of target token, namely the first token in rejection response. We experiment with Llama3-8B- Instruct and Qwen2.5-7B-Instruct. For close-sourced models, we experiment with GPT-4o where the OpenAI API provides the log probability of top 20 generation tokens.

As show in Figure 6, the first token for rejection responses are consistently suppressed across models. To further illustrate this effect, we conduct rejection keyword matching (Zou et al. 2023) on model responses. While all raw harmful requests are rejected, a certain proportion of emojisubstituted prompts have elicited non-rejected responses. We also present illustrative cases in Figure 5. When replacing sensitive words into emojis (marked in yellow), the rejection prefix (in orange) are also transformed into compliance response (in green). For the first case with Llama3-8B-

**Figure 6.** PACT distribution and rejection ratio.

**Figure 7.** Visualization of the raw and emoji prompts.

Instruct, though it does not provide detailed post content, it has begun its response with the prefix “Here ’s...”, a typical prefix which are usually optimized for adversarial optimization (Zou et al. 2023; Junxiao et al. 2025). In the second case with GPT-4o, the model directly produces fabricated content, including false information about a virus outbreak. These examples align with the PACT evaluation results, confirming that emojis can effectively suppress the model’s rejection behavior and facilitate toxic generation.

2) Internal representations visualize the difference of raw and emoji-substituted prompts within the LLMs. As the last token representation is the key to induce the first generation token, we visualize its representation at the last layer via TSNE to see whether they are clustered. As shown in Figure 7, the representation of raw harmful requests and its emoji-substituted counterpart deviate with each other obviously. As previous study suggested (Xu et al. 2024; Gao et al. 2025), the representation shift may push input prompts beyond the learned safety boundary of LLMs, thereby weakening the model’s safety sensitiveness to harmful content. This observation may account for the suppressed rejective responses in PACT analysis. With the analysis above, we obtain the 2nd observation as follows:

Observation 2: Emojis-substituted prompts deviate from their raw counterparts in the representation space, yet the source of this gap remains unclear.

RQ3: How are emojis tokenized To explore the stem of representation gap with LLMs, we perform token-level interpretation to see whether tokenization brings perturbation to the input prompt. Tokenization converts input text into discrete sub-word units using algorithms such as bytepair encoding (BPE) (Sennrich, Haddow, and Birch 2016).

30435

![Figure extracted from page 5](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-005-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-005-figure-04.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 5](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-005-figure-05.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 6 -->

**Figure 8.** Emoji tokenization cases with GPT-4o, Llama3- 8B-Instruct and Qwen2.5-7B-Instruct model.

Toxicity Ratio Emojis

≥0.5 [0.3, 0.5) [0.1, 0.3)

**Table 5.** Context Toxicity Ratio which is higher than 0.1

To investigate how emojis are processed, we collected 1,393 single-character emojis and process them using the tokenizers of representative models.

Specifically, we first noticed that over 97% emojis are segmented into multiple sub-words for GPT-4o and Llama3- 8B-Instruct. Besides, with some tokenization cases presented in Figure 8, we have the following findings. 1) Rare Distribution. Most emojis are tokenized into multiple subtokens, suggesting that they are not treated as atomic tokens in the vocabulary by most tokenizers. As the vocabulary of the tokenizers reflect distributional information with the training corpus (Hayase et al. 2024; Xu, Lu, and Zhang 2024), the phenomenon suggest that emojis are rarely distributed in the LLM pre-training corpora. 2) Tokenization Mismatch. We observed that the sub-word tokens resulting from emoji tokenization are often unreadable or irregular. These sub-tokens share minimal overlap with the tokenized results of its corresponding textual words, as Figure 8 shows. This means that emoji can serve as a different channel to express the same semantics, thus presenting the disparity of internal representation of the prompt at sequence-level. Correspondingly, we derive the following observation:

Observation 3: Most emojis are tokenized into sub-word fragments, where the minimal overlap with textual words offers an alternative channel for conveying semantics.

Corpus Investigation of Emoji Exposure

With the model-level interpretation above, we also examine the pre-training corpus with emojis, as previous study suggested that the pre-training contexts can impact the corresponding generation behaviors (Lin et al. 2025). Hence, this section probes whether correlations exist between the emoji pre-training corpus and the toxicity generation phenomenon.

**Figure 9.** Emoji contexts in pre-training corpus.

Emojis Contexts in the Pre-training Corpus

We first check the contexts where emojis appear in the pretraining data, where two steps are involved.

Step 1: Extract the emoji-contained data entries. Using our revised 520 emoji-prompts from AdvBench, we identify 61 emojis that appear more than 20 times. Following prior work, we examine the C4 (Raffel et al. 2020; Lin et al. 2025) corpus by randomly selecting 4 data shards (approximately 100,000 samples in total) and filtering for entries containing the selected emojis. Finally, 398 data entries are obtained.

Step 2: Examine emoji contexts toxicity. In analyzing the filtered data entries containing frequently used emojis, we observed that they could be associated with toxic themes such as gambling, illegal downloads, fraud, and pornography. To quantify this, we instruct GPT-4o using a carefully designed instruction, prompting it to decide the toxicity of each emoji data entry. Results show that 32.8% of the highfrequency emoji appear in toxic contexts, and we present the emojis of which the context toxicity rate is more than 10% in Table 5. Correspondingly, these emojis are frequently appear in harmful requests regarding of hacking, phishing and illegally financial activities. The finding suggests a potential correlation between emoji-related toxic contexts in the corpus and the toxicity generation, where such co-occurence may increase the tolerance for toxicity generation.

30436

![Figure extracted from page 6](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-006-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 6](2026-AAAI-when-smiley-turns-hostile-interpreting-how-emojis-trigger-llms-toxicity/page-006-figure-14.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 7 -->

Case Study We illustrate our findings above with cases in Figure 9. With the emoji functions of semantic emojis and camouflage emojis, we give cases respectively.

Case 1 for semantic emoji. The emoji is frequently used to replace sensitive terms in harmful requests related to “financial gain” or “money” obtained through illegal means. Consistently, its surrounding context often pertains to such topics. As shown in the first case of Figure 9, two representative examples include one discussing crypto trading via a coinbase wallet and another promoting money-making strategies on Instagram. Notably, are frequently associated with data entries about potentially illegal activities, which may embed malicious semantics into the emoji.

Case 2 for camouflage emoji. The emoji is commonly used at the beginning of revised emoji-prompts as a camouflage element, making the prompt appear playful or testlike. In our collected entries containing, we observed frequent co-occurrence with gaming-related content, as the Game Description illustrated in the second case of Figure 9. This suggests that may function as a disguise, leading the LLM to interpret a harmful request as an in-game task, thereby weakening the sensitive to harmful request.

Case 3 for Universal toxic emoji. In addition to emojis that serve as clear substitutes or camouflage, we noticed that some emojis, such as, appear across a wide range of harmful requests and in varying positions unexpectedly. Notably, analyzing its contextual usage in the corpus also shows substantial variation in co-occurring content. As illustrated in the final case of Figure 9, could appear in contexts related to pornography (buy viagra online), gambling (cash prizes!), and illegal downloads (Cheat Tool). We infer that such exposure to diverse toxic contexts during pre-training may embed multifaceted harmful semantics into the emoji, enabling it to trigger various forms of toxic generation.

Overall, the above analysis suggests a potential link between toxic emoji contexts in the corpus and the observed phenomenon of toxicity generation:

Observation 4: Emojis are exposed to polluted contexts during pre-training, which may increase the tolerance and tendency for similar toxicity generation.

## Related Work

Emojis Emojis (Hu et al. 2017) are increasingly used as non-verbal symbols to convey emotions and intentions in digital communications (Unicod 2025). Early researches mainly investigated the emoji pattern diversity across different platforms (Bai et al. 2019), communication scenarios (Chen, Ai, and He 2018), cultural contexts (Guntuku et al. 2019), and age groups (Koch, Romero, and Stachl 2022). Further, researchers have leveraged automatic techniques to analyze emojis within user-generated content, particularly for applications in sentiment (Hakami, Hendley, and Smith 2022; Lou et al. 2020) and behavior modeling (Ai, Chen, and He 2019; Li et al. 2018; Maraule, Duffett, and Edu 2025). With the rise large language models (LLMs), researchers further explored how these models understand and process emojis, particularly in comparison to humans (Peng et al. 2023; Lyu et al. 2024; Zhou et al. 2025; Lyu et al. 2025). Particularily, growing interest are paid to how LLMs incorporate emojis during response generation (de Janeiro 2023; Lyu et al. 2024; Jain et al. 2025). Despite the success above, few studies have investigated whether the presence of emojis could facilitate the toxicity generation of LLMs. Wei, Liu, and Erichson (2025) demonstrate that emojis can hinder harmful content detection of judge LLMs, but our work focuses on how emojis influence the toxicity generation process of the target LLM itself, which is under-explored previously.

Toxicity Generation with Low-resourced Languages or Specialized Coding

Several studies have demonstrated that low-resourced languages (e.g., Zulu) and specialized coding (e.g., Base64) could elicit harmful outputs from LLMs, which are closely related to our research. Specifically, harmful outputs could be elicited via low-resourced languages with both direct harmful requests (Deng et al. 2024; Wang et al. 2024; Shen et al. 2024) or jailbreak templates (Li et al. 2024; Huang et al. 2025). For specialized coding, early approaches employed simple encodings such as Morse Code and Base64 to obfuscate harmful requests (Yuan et al. 2023). Advanced strategies employ ASCII-based visual patterns (Jiang et al. 2024) and structured query languages such as Uniform Resource Locators (URLs) (Chen et al. 2025). This could be due to the failed generalization of safety alignment mechanisms developed for high-resourced natural languages.

While emojis may also trigger harmful generation due to similar deficiencies in safety training, they differ in the following ways. 1) Emojis ensemble characteristics of lowresourced languages and specialized coding. While emojis can serve as part of “language” for communication, they also rely on symbolic combinations and contextualization to express toxicity, similar to specialized coding methods. 2) Emojis are more universal and easily accessible. Unlike low-resourced languages, emojis are used globally across diverse groups, and they are far easier to use compared to specialized coding. Consequently, the risks associated with emojis could affect a larger user base, leading to broader potential harm. Therefore, it deserves a comprehensive investigation into how emojis trigger toxicity generation in LLMs.

## Conclusion

This paper starts with the phenomenon that harmful requests with emojis can trigger toxicity from LLMs. With extensive experiments across models, languages and jailbreak tasks, we first comprehensively explore the emoji-triggered toxicity generation. For further insights, we perform a series of interpretation from semantic cognition to tokenization, interpreting the generation at the model-level. Finally, an investigation to the pre-training corpus suggests potential correlation to the emoji-related data pollution to the toxicity generation. These findings emphasize the need for safety alignment that extends beyond literal languages as future works.

30437

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Science Foundation for Distinguished Young Scholars (with No. 62125604). This work was supported in part by the Postdoctoral Fellowship Program of CPSF (Grant No. GZC20240826) and the China Postdoctoral Science Foundation (Grant No. 2024M761679).

## References

Adobe. 2022. Future of Creativity: Global Emoji Trend Report Reveals Emoji Users are Happier than Ever. Technical report, Adobe Inc. Accessed: YYYY-06-24. Ai, B.; Chen, Y.; and He, X. 2019. Automatic detection of user sentiment and behavior in social media. Information Processing & Management, 56(3): 738–749. Bai, Q.; Dan, Q.; Mu, Z.; and Yang, M. 2019. A systematic review of emoji: Current research and future perspectives. Frontiers in psychology, 10: 2221. Chao, P.; Robey, A.; Dobriban, E.; Hassani, H.; Pappas, G. J.; and Wong, E. 2025. Jailbreaking Black Box Large Language Models in Twenty Queries. In IEEE Conference on Secure and Trustworthy Machine Learning, SaTML 2025, Copenhagen, Denmark, April 9-11, 2025, 23–42. Chen, S.; Yuan, Y.; Jiao, W.; and Tu, Z. 2025. Jailbreaking Aligned Large Language Models Using Structured Nonnatural Query Language. In The 63rd Annual Meeting of the Association for Computational Linguistics. Chen, Y.; Ai, B.; and He, X. 2018. Emoji as a new dimension of online communication: Exploring the impact of emoji use on social presence and satisfaction in instant messaging. Computers in Human Behavior, 86: 223–231. de Janeiro, E. d. R. 2023. Could large language models estimate valence of words? A small ablation study. Proceedings of CBIC. Deng, Y.; Zhang, W.; Pan, S. J.; and Bing, L. 2024. Multilingual Jailbreak Challenges in Large Language Models. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. Emojipedia. 2024. Emoji Statistics. https://emojipedia.org/ stats. Accessed: 2025-07-02. EmojiPedia. 2025. Money with Wings Emoji. https:// emojipedia.org/money-with-wings. Accessed: 2025-07-03. Gao, L.; Zhang, X.; Nakov, P.; and Chen, X. 2025. Understanding and Defending Against Jailbreaks in Large Language Models. In The 63rd Annual Meeting of the Association for Computational Linguistics. Google, G. T. 2024a. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. CoRR, abs/2403.05530. Google, G. T. 2024b. Introducing Gemini 2.0: our new AI model for the agentic era. https: //blog.google/technology/google-deepmind/google-geminiai-update-december-2024/#ceo-message. Accessed: 2025-12-02.

Guntuku, S. C.; Li, M.; Tay, L.; and Ungar, L. 2019. Studying Cultural Differences in Emoji Usage across the East and the West. Hakami, S. A. A.; Hendley, R.; and Smith, P. 2022. Emoji Sentiment Roles for Sentiment Analysis: A Case Study in Arabic Texts. In Proceedings of the Seventh Arabic Natural Language Processing Workshop (WANLP), 346–355. Hayase, J.; Liu, A.; Choi, Y.; Oh, S.; and Smith, N. A. 2024. Data Mixture Inference: What do BPE Tokenizers Reveal about their Training Data? arXiv:2407.16607. Hu, T.; Guo, H.; Sun, H.; Nguyen, T.-v.; and Luo, J. 2017. Spice up your chat: the intentions and sentiment effects of using emojis. In Proceedings of the International AAAI Conference on Web and Social Media, volume 11, 102–111. Huang, L.; Jin, H.; Bi, Z.; Yang, P.; Zhao, P.; Chen, T.; Wu, X.; Ma, L.; and Chen, H. 2025. The Tower of Babel Revisited: Multilingual Jailbreak Prompts on Closed-Source Large Language Models. CoRR, abs/2505.12287. Jain, N.; Wu, Z.; Villalobos, C. E. M.; Hilliard, A.; Guan, X.; Koshiyama, A.; Kazim, E.; and Treleaven, P. C. 2025. From Text to Emoji: How PEFT-Driven Personality Manipulation Unleashes the Emoji Potential in LLMs. In Findings of the Association for Computational Linguistics: NAACL 2025, 4687–4723. Jiang, F.; Xu, Z.; Niu, L.; Xiang, Z.; Ramasubramanian, B.; Li, B.; and Poovendran, R. 2024. ASCII Art-based Jailbreak Attacks against Aligned LLMs. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 15157–15173. Junxiao, Y.; Zhexin, Z.; Shiyao, C.; Hongning, W.; and Huang, M. 2025. Guiding not Forcing: Enhancing the Transferability of Jailbreaking Attacks on LLMs via Removing Superfluous Constraints. In The 63rd Annual Meeting of the Association for Computational Linguistics. Koch, T. K.; Romero, P.; and Stachl, C. 2022. Age and gender in language, emoji, and emoticon usage in instant messages. Computers in Human Behavior, 126: 106990. Li, J.; Liu, Y.; Liu, C.; Shi, L.; Ren, X.; Zheng, Y.; Liu, Y.; and Xue, Y. 2024. A Cross-Language Investigation into Jailbreak Attacks in Large Language Models. CoRR, abs/2401.16765. Li, W.; Chen, Y.; Hu, T.; and Luo, J. 2018. Mining the Relationship between Emoji Usage Patterns and Personality. Proceedings of the International AAAI Conference on Web and Social Media, 12. Li, X.; Zhou, Z.; Zhu, J.; Yao, J.; Liu, T.; and Han, B. 2023. DeepInception: Hypnotize Large Language Model to Be Jailbreaker. CoRR, abs/2311.03191. Lin, L.; Brown, H.; Kawaguchi, K.; and Shieh, M. 2025. Single Character Perturbations Break LLM Alignment. In AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA, 27473–27481. Lou, Y.; Zhang, Y.; Li, F.; Qian, T.; and Ji, D. 2020. Emoji- Based Sentiment Analysis Using Attention Networks. ACM Trans. Asian Low-Resour. Lang. Inf. Process., 19(5).

30438

<!-- Page 9 -->

Lyu, H.; Huang, J.; Zhang, D.; Yu, Y.; Mou, X.; Pan, J.; Yang, Z.; Wei, Z.; and Luo, J. 2025. Gpt-4v (ision) as a social media analysis engine. ACM Transactions on Intelligent Systems and Technology, 16(3): 1–54. Lyu, H.; Qi, W.; Wei, Z.; and Luo, J. 2024. Human vs. lmms: Exploring the discrepancy in emoji interpretation and usage in digital communication. In Proceedings of the International AAAI Conference on Web and Social Media, volume 18, 2104–2110. Maraule, M.; Duffett, R.; and Edu, T. 2025. Modeling emoji online marketing on websites among young consumers: the moderation effect of age. Future Business Journal, 11: 91. Mehrotra, A.; Zampetakis, M.; Kassianik, P.; Nelson, B.; Anderson, H. S.; Singer, Y.; and Karbasi, A. 2024. Tree of Attacks: Jailbreaking Black-Box LLMs Automatically. In Annual Conference on Neural Information Processing Systems 2024. Meta. 2024. Introducing Meta Llama 3: The most capable openly available LLM to date. https://ai.meta.com/blog/ meta-llama-3/. Accessed: 2025-12-02. Michael, D.; and Kenneth, H. 2024. How Good Is GPT’s Emojinal Intelligence? Investigating Emoji Patterns in LLM-Generated Social Media Text. In Proceedings of the International Conference on AI Research. Minich, M.; Kerr, B.; and Moreno, M. 2025. Adolescent Emoji Use in Text-Based Messaging: Focus Group Study. JMIR Formative Research, 9: e59640. OpenAI. 2023. GPT-4 system card. https://cdn.openai.com/ papers/gpt-4-system-card.pdf. Accessed: 2025-12-02. OpenAI. 2024. GPT-4o system card. https://openai.com/ index/gpt-4o-system-card/. Accessed: 2025-12-02. Peng, L.; Wang, Z.; Liu, H.; Wang, Z.; and Shang, J. 2023. Emojilm: Modeling the new emoji language. arXiv:2311.01751. Qi, X.; Zeng, Y.; Xie, T.; Chen, P.-Y.; Jia, R.; Mittal, P.; and Henderson, P. 2024. Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To! In The Twelfth International Conference on Learning Representations, ICLR 2024. Raffel, C.; Shazeer, N.; Roberts, A.; Lee, K.; Narang, S.; Matena, M.; Zhou, Y.; Li, W.; and Liu, P. J. 2020. Exploring the limits of transfer learning with a unified text-to-text transformer. J. Mach. Learn. Res., 21(1). Sennrich, R.; Haddow, B.; and Birch, A. 2016. Neural Machine Translation of Rare Words with Subword Units. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 1715–1725. Shen, L.; Tan, W.; Chen, S.; Chen, Y.; Zhang, J.; Xu, H.; Zheng, B.; Koehn, P.; and Khashabi, D. 2024. The Language Barrier: Dissecting Safety Challenges of LLMs in Multilingual Contexts. In Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, 2668–2680. Team, Q. 2024a. Qwen2.5-72B-Instruct. https:// huggingface.co/Qwen/Qwen2.5-72B-Instruct. Accessed: 2025-12-02.

Team, Q. 2024b. Qwen2.5-LLM: Extending the boundary of LLMs. https://qwenlm.github.io/blog/qwen2.5-llm/. Accessed: 2025-12-02. Unicod. 2025. About Emoji. https://home.unicode.org/ emoji/about-emoji/. Accessed: 2025-07-02. Unicode Consortium. 2025. Emoji Counts. https://unicode. org/emoji/charts/emoji-counts.html. Accessed: 2025-07-02. Wang, W.; Tu, Z.; Chen, C.; Yuan, Y.; Huang, J.; Jiao, W.; and Lyu, M. R. 2024. All Languages Matter: On the Multilingual Safety of LLMs. In Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, 5865–5877. Wei, Z.; Liu, Y.; and Erichson, N. B. 2025. Emoji Attack: Enhancing Jailbreak Attacks Against Judge LLM Detection. In Forty-second International Conference on Machine Learning. Xu, Y.; Lu, J.; and Zhang, J. 2024. Bridging the Gap between Different Vocabularies for LLM Ensemble. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), 7133–7145. Xu, Z.; Huang, R.; Chen, C.; and Wang, X. 2024. Uncovering safety risks of large language models through concept activation vector. Advances in Neural Information Processing Systems, 37: 116743–116782. Yan, Y.; Sun, S.; Duan, Z.; Liu, T.; Liu, M.; Yin, Z.; Li, Q.; and Lei, J. 2025. from Benign import Toxic: Jailbreaking the Language Model via Adversarial Metaphors. CoRR, abs/2503.00038. Yuan, Y.; Jiao, W.; Wang, W.; Huang, J.; He, P.; Shi, S.; and Tu, Z. 2023. GPT-4 is Too Smart to be Safe: Stealthy Chat with LLMs via Cipher. arXiv:2308.06463. Zhang, Q.; Qiu, H.; Wang, D.; Qian, H.; Li, Y.; Zhang, T.; and Huang, M. 2025. Understanding the Dark Side of LLMs’ Intrinsic Self-Correction. In The 63rd Annual Meeting of the Association for Computational Linguistics. Zheng, Y.; Lyu, H.; and Luo, J. 2025. Irony in Emojis: A Comparative Study of Human and LLM Interpretation. arXiv:2501.11241. Zhou, Y.; Xu, P.; Wang, X.; Lu, X.; Gao, G.; and Ai, W. 2025. Emojis decoded: Leveraging chatgpt for enhanced understanding in social media communications. In Proceedings of the International AAAI Conference on Web and Social Media, volume 19, 2302–2316. Zhukova, M.; and Herring, S. C. 2024. Benign or Toxic? Differences in Emoji Interpretation by Gender, Generation, and Emoji Type. Language@ Internet, 22(Special Issue): 74–108. Zou, A.; Wang, Z.; Kolter, J. Z.; and Fredrikson, M. 2023. Universal and Transferable Adversarial Attacks on Aligned Language Models. CoRR, abs/2307.15043. Zou, Q.; Xiao, J.; Li, Q.; Yan, Z.; Wang, Y.; Xu, L.; Wang, W.; Gao, K.; Li, R.; and Jiang, Y. 2025. QueryAttack: Jailbreaking Aligned Large Language Models Using Structured Non-natural Query Language. In Findings of Proceedings of the 63nd Annual Meeting of the Association for Computational Linguistics (Finding of ACL 2025).

30439
