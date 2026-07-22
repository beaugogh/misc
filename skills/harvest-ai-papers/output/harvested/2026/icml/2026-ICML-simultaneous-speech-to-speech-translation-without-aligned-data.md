---
title: "Simultaneous Speech-to-Speech Translation Without Aligned Data"
source_url: https://icml.cc/virtual/2026/oral/71089
paper_pdf_url: https://arxiv.org/pdf/2602.11072v1
venue: ICML
year: 2026
retrieved_date: 2026-07-21
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Simultaneous Speech-to-Speech Translation Without Aligned Data

<!-- Page 1 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

Tom Labiausse 1 Romain Fabre 1 Yannick Est`eve 2 Alexandre D´efossez 1 3 Neil Zeghidour 3

## Abstract

Simultaneous speech translation requires translating source speech into a target language in real-time while handling non-monotonic word dependencies. Traditional approaches rely on supervised training with word-level aligned data, which is difficult to collect at scale and thus depends on synthetic alignments using language-specific heuristics that are suboptimal. We propose Hibiki- Zero, which eliminates the need for word-level alignments entirely. This fundamentally simplifies the training pipeline and enables seamless scaling to diverse languages with varying grammatical structures, removing the bottleneck of designing language-specific alignment heuristics. We first train on sentence-level aligned data to learn speech translation at high latency, then apply a novel reinforcement learning strategy using GRPO to optimize latency while preserving translation quality. Hibiki-Zero achieves state-of-theart performance in translation accuracy, latency, voice transfer, and naturalness across five X-to- English tasks. Moreover, we demonstrate that our model can be adapted to support a new input language with less than 1000h of speech. We provide examples, model weights, inference code1 and we release a benchmark containing 45h of multilingual data for speech translation evaluation.2

## 1. Introduction

We introduce Hibiki-Zero, a system for simultaneous and expressive speech-to-speech (S2ST) and speech-to-text (S2TT) translation that does not require aligned data for training. Unlike offline speech translation systems that access the full source utterance before translating, simultaneous translation must produce output incrementally while maintaining both

1Kyutai, Paris, France 2LIA, University of Avignon, France 3Gradium, Paris, France. Correspondence to: Hibiki-Zero <hibiki@kyutai.org>.

Preprint. February 12, 2026.

1github.com/kyutai-labs/hibiki-zero 2huggingface.co/collections/kyutai/hibiki-zero translation accuracy and speech naturalness. This requires learning a fine-grained translation policy that determines when to listen and when to speak. The most straightforward approach to learning such a policy is through supervised training on aligned data. However, human interpretation data with word-level alignments is virtually non-existent, forcing state-of-the-art systems to rely on synthetic data with automatic alignments (Labiausse et al., 2025). These automatic alignments are inherently limited, as they depend on hand-crafted heuristics rather than being learned from data.

Hibiki-Zero is a decoder-only model that synchronously receives source speech and generates translated speech leveraging a multistream architecture originally introduced by D´efossez et al. (2024). Unlike Hibiki (Labiausse et al., 2025), Hibiki-Zero is not trained with supervised learning on synthetic interpretation data but rather casts joint optimization of translation quality and latency as a reinforcement learning (RL) problem. While we still require a base model before the RL phase, it is trained using sentence-level aligned data which can be more easily constructed independently of the language compared to word-level aligned data. During RL, we exploit the sentence-level aspect of our data to design a simple reward system based on BLEU score (Papineni et al., 2002) only. To achieve this, we compute rewards at multiple intermediate instants during the translation of an input speech utterance by leveraging the simultaneous text translation also produced by our model. Using these process rewards, we obtain fine-grained local advantages across multiple translations from the same input. We then adapt GRPO (Shao et al., 2024) to our multistream architecture, using these advantages to optimize the model.

In a multilingual-to-English translation task, Hibiki-Zero outperforms previous state-of-the-art work in translation quality, latency, speaker identity preservation, and speech naturalness. We also retain all the benefits of multistream modeling such as batching and real-time inference on GPU while removing the necessity to build interpretation-like training data thus considerably simplifying the development of such models. We even demonstrate that Hibiki-Zero can adapt to a new input language with less than 1000h of training data marking an important step to make high quality speech translation (ST) available in more languages. We will release our data preparation code, model weights as well as a 45h multilingual speech benchmark for ST evaluation.

arXiv:2602.11072v1 [cs.CL] 11 Feb 2026

<!-- Page 2 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

## 2. Related Work

## 2.1. Simultaneous end-to-end speech translation

While speech translation was initially performed using cascaded systems combining automatic speech recognition (ASR), machine translation (MT) and text-to-speech synthesis (TTS) (Wahlster, 2000; Nakamura et al., 2006), it recently evolved in fully end-to-end systems (Jia et al., 2019; Lee et al., 2022a; Jia et al., 2022; Rubenstein et al., 2023) reducing error propagation and enabling transfer of nonlinguistic information such as the speaker voice identity or prosody to the generated speech. At first trained with auxiliary text of phoneme translation tasks (Jia et al., 2022; Zhang et al., 2024a), most recent works (Barrault et al., 2023; Labiausse et al., 2025; Cheng et al., 2025; Misiunas & Ablavatski, 2025) train directly on simultaneous S2TT and S2ST tasks so they can use the predicted text translation as a scaffolding for speech generation at inference time. Among direct ST training methods, those who achieve better speech naturalness are duplex audio systems that require to build a simultaneous ST dataset. They either rely on a synthetic data generation pipeline which includes a fine word-level text-to-translation alignment method (Labiausse et al., 2025; Misiunas & Ablavatski, 2025) or use a text LLM to split text into semantic chunks (a few words) that are individually translated thus providing chunk-level translation alignment (Cheng et al., 2025) before collecting human-annotated interpretation data for finetuning purposes. Hibiki-Zero removes most of the complexity from synthetic data generation as it only requires sentence-level translation alignment easily obtained from punctuation. Thanks to an efficient RL process, it is then possible to reduce the translation latency of the model so it achieves state-of-the-art quality/latency trade-off in multiple input languages.

## 2.2. Self-improvement of real-time translation systems

RL methods to improve simultaneous translation systems were first explored in the context of text translation. Some works used preference-based approaches (Yu et al., 2025) with preferences established in the context of simultaneous ST by prompting a text LLM while others applied online reinforcement procedures (Yu et al., 2025; Xu et al., 2025) with sequence-level rewards as a combination of translation quality and latency metrics. Because they lack sub-sentence granularity in their preference or reward signals, it is difficult for these methods to find an appropriate balance between translation quality and latency during the RL process. More recently, Seed LiveInterpret 2.0 (Cheng et al., 2025) applied PPO (Schulman et al., 2017) with a combination of intermediate evaluations of the generated sequences (process rewards) and overall evaluation of the translation (outcome rewards). Starting from a base supervised ST model trained with chunk-level alignment and finetuned on high-quality human interpretation data, they managed to strictly improve the quality/latency trade-off through RL. However, due to complex interactions between the numerous rewards they introduced, they encountered stability issues, reward hacking and had to rely on two different stages of RL training, using only outcome rewards at first before adding process rewards. On the other hand, Hibiki-Zero uses a single and straightforward reward system based on BLEU score (Papineni et al., 2002) coupled with GRPO (Shao et al., 2024) without KL regularization as previously done by Rastogi et al. (2025) to reduce memory requirements during training. Most importantly, it does not rely on any human interpretation or annotated data to finetune the model before reinforcement. On multilingual simultaneous ST tasks, Hibiki-Zero achieves state-of-the-art translation quality, latency, naturalness and speaker identity preservation. Hibiki-Zero is even able to adapt to a new input language after a light finetuning.

## 3. Method

We consider an utterance in a source language represented as a monophonic waveform X ∈Rfs·d, sampled at a frame rate fs = 24 kHz, of duration d. Similarly, its translation is given in a target language, denoted Y ∈Rfs·d. We assume X is padded to ensure both have the same duration. Our objective is to model P [Y |X]. Contrary to Labiausse et al. (2025), we do not constrain the modeling of Y knowing X to be entirely causal in our training data. Thanks to the diversity of causality and latency arrangements in the dataset, it is still possible to learn a base translation model. Its behavior is then adjusted by an online reinforcement learning strategy that rewards correct and simultaneous translations.

## 3.1. Modeling

We build on the framework introduced by D´efossez et al. (2024) for the joint modeling of multiple sequences of tokens and used by Labiausse et al. (2025) to perform simultaneous S2TT and S2ST with high fidelity.

## 3.1.1. NEURAL AUDIO CODEC

We use the pre-trained causal and streaming Mimi codec (D´efossez et al., 2024) to encode X and Y into low framerate sequences of discrete tokens. Mimi consists of an encoder and decoder from and to the waveform domain, and of an information bottleneck using Residual Vector Quantization (RVQ) (Zeghidour et al., 2022).

For language modeling, we are interested in the discrete indices of codebook entries which Mimi latents are projected to. We denote those (At,q) ∈{1,..., Na}fr·d×Q where fr = 12.5 Hz is the codec framerate, Q is the number of audio residual quantization levels varying up to 32 and Na the codebooks size. Following Zhang et al. (2024b);

<!-- Page 3 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

**Figure 1.** Architecture of the RQ-Transformer. Figure adapted

from D´efossez et al. (2024).

0

...

0

........................... Acoustic tokens

Semantic tokens

Text tokens

Hibiki-Zero stream (speaks)

.........

Hibiki-Zero is so fast Hibiki-Zero est tellement rapide

🤖 👤

0

...

0

....................................

Source stream

(listens)

Acoustic tokens

Semantic tokens

PAD EPAD Hibiki Zero PAS EPAD is EPAD so PAD EPAD fast PAD

...

PAD

...

...

...

0

...

0

0

...

0

PAD

...

...

...

...

...

...

**Figure 2.** Joint sequence modeling. From the source stream,

Hibiki-Zero predicts its Inner Monologue text stream, semantic and acoustic tokens. Figure adapted from Labiausse et al. (2025).

D´efossez et al. (2024), the output of the first quantization level is trained to replicate semantic information obtained from a WavLM self-supervised audio model (Chen et al., 2022). We refer to At,1 as semantic tokens, and At,q≥2 as acoustic tokens with the latter arranged in a coarse to fine manner. We keep only Q = 16 acoustic levels which is sufficient to ensure high quality speech.

## 3.1.2. JOINT MODELING OF DISCRETE AUDIO TOKENS

Following Yang et al. (2023); Labiausse et al. (2025), we leverage a RQ-Transformer (Lee et al., 2022b) as shown in Figure 1 to model (At,q) both over the time t and quantizer q axes as audio streams cannot be reasonably merged into a single discrete sequence. It consists in a large Temporal Transformer (Vaswani et al., 2017) of latent dimension D, operating at the same framerate fr as the codec, and being fed all the tokens generated so far, e.g. for all t ≤fr · d,

Zt = Temp(A0,..., At−1) ∈RD. (1)

A0 is defined as a deterministic token indicating the start of the generation. Then, a smaller scale Depth Transformer models auto-regressively the tokens At,1,..., At,Q over the quantizer axis, e.g. for all t ≤fr · d and q ≤Q, lt,q = Dep(Zt, At,0,..., At,q−1) ∈RNa, (2)

with At,0 also a special token, and with the goal of having, softmax(lt,q) ≈P [At,q|A0,..., At−1, At,0,... At,q−1]

Following (Copet et al., 2023; D´efossez et al., 2024), we introduce an acoustic delay shifting acoustic tokens of 2 time steps in the future compared to the semantic stream. The streams are realigned before decoding the audio with the codec. As this delay is always applied, we don’t introduce new notations for readability and refer to (At,q) directly.

## 3.1.3. TRANSLATION AS MULTISTREAM MODELING

Using the RQ-Transformer given by Eq. (1) and (2) to jointly model multiple discrete streams of tokens, we can perform the task of joint simultaneous S2TT and S2ST as illustrated in Figure 2. Following (D´efossez et al., 2024), we use an Inner Monologue by introducing a stream of padded text tokens (Wt) ∈{1,..., NW }fr·d whose content is the aligned text transcription of the audio modeled in AY. This text stream is concatenated with the audio tokens AY from the source interpretation along the q-axis such that it comes before the semantic level. Then, we concatenate the target tokens AY and source tokens AX along the q-axis. At inference time, predictions of tokens AX are skipped and actual tokens of the input audio are used instead.

## 3.1.4. ARCHITECTURAL DETAILS

At time-step t, tokens from the previous step, e.g. AX t−1, AY t−1, and Wt−1, are fed into dedicated embedding tables and contributions are summed with a BOS token used for the first time step t = 1. The RQ-Transformer uses standard Transformer layers (Vaswani et al., 2017), with gated SiLU activation (Shazeer, 2020; Hendrycks & Gimpel, 2016). A linear layer maps output Zt of the Temporal Transformer to logits for the text token Wt. The Depth Transformer then operates for Q steps to estimate the logits for the output stream and for Q additional steps for the input stream. Each depth step q takes as input Zt summed with a learned embedding of the previous audio token At,q−1, or Wt for q = 1. We provide architectural hyper-parameters in Section 4.1.

## 3.2. Coarse alignment of speech translation data

We have assumed training pairs (X, Y) to not be entirely causal at the interpretation level. We now detail the specific method used to build such coarse translation alignments.

## 3.2.1. SENTENCE-LEVEL ALIGNMENT

We start from an unaligned speech translation pair (X, Y) which only verifies a sentence mapping constraint meaning that both X and Y contain the same number of sentences and such that the ith sentence in Y is a translation of the ith sentence in X. Inspired by Labiausse et al. (2025), we

![Figure extracted from page 3](2026-ICML-simultaneous-speech-to-speech-translation-without-aligned-data/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data rely on the insertion of artificial silence in Y to delay its content with respect to X. For each sentence of index i, we introduce silence in Y to shift its ith sentence by an amount δi after the start of the ith sentence in X where δi ∼ U(0, δ × di) is sampled independently for each sentence, di is the duration of the ith sentence in X and δ ∈[0, 1] is an hyperparameter. Then, using punctuation characters such as commas or colons in a precomputed transcript of Y, we insert silences whose durations follow U(0, µ) at the corresponding instants in Y with µ being a hyperparameter.

## 3.2.2. NATURAL PAUSES TTS

Using the method described in Section 3.2.1, we might break the natural flow of speech by inserting silence on punctuations which is also subject to imprecisions of the transcript timestamps. Following Zeghidour et al. (2025), we train a TTS with synced audio and text streams as output, providing a control on the emission timestamp of each word to synthesize. Moreover, we train the TTS to perform voice transfer from a short audio conditioning of maximum 10 seconds. We can then generate an audio Y + using the original transcript of Y and naturally insert the pauses described in 3.2.1 while conditioned on the speaker from X. This results in new training pairs (X, Y +) where targets contain smoother transitions between speech and silences than Y.

## 3.3. Translation policy reinforcement

Assuming that we dispose of a simultaneous translation model as presented in Section 3.1, we now introduce a reinforcement learning procedure using process rewards based on BLEU scores to improve the translation policy of the model as illustrated in Figure 3. We adapt GRPO from Shao et al. (2024) to be our RL algorithm. We denote by πθ the translation model to optimize and πθold an older version of it acting as a regularizer. Given an input speech utterance X with a known sentence-level text translation y, we use πθold to generate G different speech translations (Yi)1≤i≤G, each of duration T × fr seconds where fr is the model frame rate and T a fixed number of frames.

## 3.3.1. PROCESS REWARDS

Let n be the number of sentences in X and (ti)0≤i≤n the frame indexes such that the sentence of index i in X starts at frame ti and ends at frame ti+1. We introduce S(t) as the sentence index at frame t ≥t0 in X i.e. S(t) = i for ti ≤t ≤ti+1 and S(t) = n −1 for t > tn. For a frame index t ≤T, we denote yt as the text concatenation of translated input sentences until the one of index S(t) included. Given a generation i, we define ˆy(i)

t as the partial text transcript until frame t given by the model’s output text stream. We now introduce the hyperparameter α ∈[0, 1]

and define the process reward for generation i at frame t as:

r(i)

t = (1 −α)BLEU

ˆy(i)

t, yt

+ αBLEU

ˆy(i)

T, yT

(3)

## 3.3.2. OPTIMIZATION OBJECTIVE

Using the modeling of X and (Yi)1≤i≤G as tokens AX and AY1,..., AYG, we define the probability ratios between πθ and πθold for each output i, codebook index q ≤Q and frame index t ≤T as:

p(i)

q,t = πθ

AYi q,t|AX

≤t, AYi q,<t πθold

AYi q,t|AX

≤t, AYi q,<t

(4)

Given a set of frame indexes t′

1 < t′ 2 <... < t′ s, we compute process rewards as defined in Section 3.3.1 for each output, namely r(i)

t′ j for i ≤G and j ≤s. We then normalize rewards per frame index across group elements:

¯r(i)

t′ j = r(i)

t′ j −mean k≤G h r(k)

t′ j i std k≤G h r(k)

t′ j i (5)

In practice, early experiments showed that using a regular frame indexes pattern along the input speech content performed better. Thus we introduce nw ∈N∗and use the end timestamp of every nw words in the input to set (t′ j)j≤s.

Then, we introduce the advantage of an output at step t as the sum of normalized rewards from the following steps:

R(i)

t =

X t′ j>t

¯r(i)

t′ j (6)

We compute the per-codebook objectives L(i)

q using the standard clipping function between 1 −ϵ and 1 + ϵ as:

L(i)

q =

T X t=1 min p(i)

q,tR(i)

t, clipϵ p(i)

q,t

R(i)

t

(7)

In the end, we seek to maximize the following objective with fixed weights cq for each depth q ≤Q:

E X∼D Yi∼πθold(X)





1 G

X q≤Q i≤G cq L(i)

q



 (8)

where D denotes our input speech distribution and πθold is a fixed version of the translation model that is replaced by πθ every fixed number of updates τ.

<!-- Page 5 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

La traduction, c'est simple. Mais la latence  est essentielle!

But latency is key!

Translation is simple. But latency       is the key.

But latency is key! Translation is easy.

frame

Translation is simple. But latency is key! +

+

Input

Output 1

Output 2

Translation is simple. Reference translation

= Translation is easy. But latency is key! Translation is simple. But latency is key!

= Translation is simple. But latency is the key. Translation is simple. But latency is key!

Translation is easy.

Translation is simple. But latency is key! Translation is simple. But latency

**Figure 3.** Process rewards method based on BLEU score. We

introduce intermediate BLEU score computed on the text output of the model before a given frame t and using the ground-truth translation of the corresponding input sentences processed so far. We combine it with the total output BLEU score using α ∈[0, 1].

## 4. Experiments

## 4.1. Architectural hyper-parameters

The backbone Temporal Transformer of Hibiki-Zero has a latent dimension of 2048 (8192 for the SiLU gating), 28 layers, 16 heads and local attention over 3000 tokens, i.e., 2B parameters and a 4min context. The Depth Transformer has a latent dimension of 1024 (4096 for the gating), 6 layers per codebook and 16 heads. It models Q = 16 audio codebooks for the output stream and the same for the input stream but only at training. We reduce the size of the model before RL by distillation into a smaller one using weight sharing among the codebooks of the Depth Transformer. Our final model architecture contains 3B parameters.

## 4.2. Training protocol

We train a multilingual-to-English speech translation system through the following steps, each with a cosine learning rate schedule and AdamW (Loshchilov & Hutter, 2019), with weight decay of 0.1, and momentum parameters (0.9, 0.95).

## 4.2.1. TEXT BACKBONE INITIALIZATION

We initialize the Temporal Transformer with Helium-13

(Kyutai, 2025) weights, an open-source base text LLM with 2B parameters trained using filtered Common Crawl4 data.

3huggingface.co/kyutai/helium-1-2b 4commoncrawl.org

## 4.2.2. AUDIO PRETRAINING

Starting from the pretrained text backbone, weights of the Depth Transformer are added to the architecture as well as audio tokens projection layers. We perform an audio pretraining with single stream audio as done by Labiausse et al. (2025) but on multilingual speech. Our data mixture comprises approximately 12% of audio in each input language, 50% of English and less than 2% of Italian. We train for 1K steps with a batch size of 144 and a learning rate of 2 · 10−4. After this pretraining stage, we duplicate the weights of the Depth Transformer to allow for future multistream training.

## 4.2.3. COARSE SPEECH TRANSLATION TRAINING

We construct a large-scale multilingual-to-English speech translation dataset comprising 40, 000 hours for each source language (French, Spanish, Portuguese, and German). Starting from a massive collection of multilingual audio, we extract 4 million single-speaker utterances, whose durations are between 30 and 75 seconds, and transcribe them using Whisper large-v3 (Radford et al., 2023). Transcripts are partitioned into sentences via Spacy’s core news sm and individually translated using MADLAD-3B (Kudugunta et al., 2023), after which we synthesize the target speech using the TTS system described in Section 3.2.2 with 10second speaker conditioning. To ensure coarse translation alignments, we apply the silence insertion technique from Section 3.2.1 using δ = 0.5 and µ = 2. Scaling our training budget following Labiausse et al. (2025), we perform 500, 000 gradient steps with a batch size of 96 and a learning rate of 3·10−5, computing the loss on both source and target streams with source noise augmentation. Finally, sequence termination is explicitly modeled by inserting a special input EOS token immediately following the source utterance and a separate EOS token in the text stream to demarcate the end of generation. Appendix Table 4 compares the performance of multilingual and monolingual models.

## 4.2.4. SPEECH TRANSLATION FINE-TUNING

We use the synthetic data generation method with natural pauses introduced in Section 3.2.2 to build a synthetic multilingual speech translation dataset of less than 200h in total. We fine-tune for 1K steps with a batch size of 16, a learning rate of 1 · 10−6 and other configurations being similar to the previous phase described in 4.2.3. We then distill the model into a light copy of itself with codebooks weight sharing using the same dataset and 20K gradient updates.

## 4.2.5. REINFORCEMENT LEARNING

Starting from the light fine-tuned translation model, we use data from the speech translation training introduced in Section 4.2.3 and run our reinforcement learning process as described in Section 3.3. We train with a batch size of 32, a

<!-- Page 6 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

**Table 1.** Objective comparison of Hibiki-Zero with Seamless (Barrault et al., 2023) and Hibiki (Labiausse et al., 2025) on short-form (Europarl-ST) and long-form (Audio-NTREX-4L) test data introduced in Section 4.3.

SHORT-FORM LONG-FORM

ASR ASR SPEAKER END ASR ASR SPEAKER END BLEU (↑) BLEU (↑) COMET (↑) SIM. (↑) OFFSET (↓) LAAL (↓) BLEU (↑) BLEU (↑) COMET (↑) SIM. (↑) OFFSET (↓) LAAL (↓)

SEAMLESS FRENCH 33.8 32.8 76.6 19.1 2.4 2.8 27.8 23.9 33.7 44.4 3.2 6.2 SPANISH 34.4 33.6 79.1 21.9 2.6 2.7 29.9 25.2 36.1 42.6 2.8 6.5 PORTUGUESE 34.1 33.6 78.9 23.9 2.8 3.1 29.0 25.6 35.0 35.7 3.2 6.6 GERMAN 27.8 27.3 82.3 20.6 2.4 3.0 27.8 24.0 40.6 47.8 2.5 7.3

HIBIKI FRENCH 32.4 31.8 81.5 35.7 2.5 3.5 29.5 26.4 42.0 52.8 2.6 6.8

HIBIKI-ZERO FRENCH 35.0 34.6 80.3 49.5 2.1 2.8 30.6 28.7 43.7 61.3 2.3 6.1 SPANISH 33.8 33.9 80.3 57.0 2.3 3.1 32.3 31.5 42.3 64.6 2.6 5.6 PORTUGUESE 33.6 33.6 78.9 51.4 2.4 3.0 33.2 31.3 42.6 62.1 2.3 6.3 GERMAN 28.7 28.6 82.0 51.5 1.9 2.8 29.1 28.3 42.3 66.0 2.0 5.9 group size of 4, learning rate of 2 · 10−7 and perform 2000 updates with τ = 20. Sequences of length T = 1500 frames are generated using a temperature of 0.8 and top-k of 250 for both text and audio streams. Process rewards are computed every nw = 8 input words and we set α = 0.4 and ϵ = 0.2. We use c0 = 100 and cq = 1 for q ≥1 to balance loss between text and audio streams. The model is evaluated every 10·τ updates on a valid set and we define Hibiki-Zero as the checkpoint with the best quality/latency trade-off according to objective evaluation metrics. Appendix Table 5 compares our base and fine-tuned models to Hibiki-Zero.

## 4.3. Evaluation datasets

Long-form data. We build Audio-NTREX-4L, a multilingual long-form ST dataset using text translations from the NTREX (Aepli et al., 2023) corpus. We select 300 examples for each source language and synthesize them using the following high-quality TTS from the industry: ElevenLabs5, Cartesia6 and Gradium7. We condition generations using voices from the multilingual dataset CML-TTS (de Oliveira et al., 2023). Audio-NTREX-4L contains around 15h of speech per TTS with an average duration of 45 seconds per sample and is split in balanced valid and test sets.

Short-form data. We filter data from Europarl- ST (Iranzo-S´anchez et al., 2020) and retain samples with realistic transcripts and duration between 2 and 20 seconds. We build valid and test sets, each with 1024 samples per source language for a total of 10h hours per set.

## 4.4. Evaluation metrics

Translation quality. We evaluate translation quality by transcribing generated speech using Whisper medium (Radford et al., 2023) and computing BLEU (Post, 2018) and

5elevenlabs.io/text-to-speech (“eleven-multilingual-v2 TTS”) 6cartesia.ai/sonic (“sonic-v2 TTS”) 7gradium.ai/#models (“default TTS”)

COMET (Rei et al., 2020) scores with respect to a reference translation, referred to as ASR-BLEU and ASR-COMET. To reduce the impact of ASR errors, hypothesis and reference texts are normalized8 before computing BLEU scores. Since Seamless and Hibiki-Zero perform speech-to-text translation in parallel, we also compute BLEU and COMET scores using their text outputs. We use the XCOMET-XL model.9.

Translation Latency. We rely on two common latency metrics known as End Offset and LAAL (Length-Adaptive Average Lagging). End Offset is defined as the time difference (in seconds) between the end of the last generated word and the end of the last word from the source. We compute LAAL following the method described by Papi et al. (2022) which defines it as an approximation of the average time (in seconds) between a source word and its translation. We use word-level emission timestamps (di)1...ngen produced by Whisper for ngen words in the generated speech. We define γ = ∆source max(ngen,nref) where ∆source is the duration of the source speech and nref the number of words in the reference translation. The LAAL score is then computed as 1 nmax

Pnmax i=1 di −(i −1)γ where nmax = min{i|di ≥∆source}.

Cross-lingual speaker similarity. For objective voice transfer evaluation, we use a standard model for speaker verification10 based on WavLM (Chen et al., 2022) and report the cosine similarity between the embeddings of the source and the generated speech.

Audio quality and naturalness. We rely on human raters to evaluate audio quality, speech naturalness and additional cross-lingual speaker similarity of generated audios. We conduct evaluations per input language using 50 samples and 20 raters for each model with 5 comparisons per rater.

8github.com/openai/whisper/blob/main/whisper/normalizers 9github.com/Unbabel/COMET 10github.com/microsoft/UniSpeech (“WavLM Large”)

<!-- Page 7 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

**Table 2.** Human evaluation. Raters report Mean Opinion Scores (MOS) on a scale ranging from 0 to 100 for each audio sample.

INPUT MODEL AUDIO SPEAKER SPEECH LANGUAGE QUALITY SIMILARITY NATURALNESS

FRENCH

SEAMLESS 11.4 ± 3.1 21.1 ± 4.9 21.2 ± 3.8 HIBIKI 62.9 ± 4.8 44.7 ± 5.1 57.0 ± 4.2 HIBIKI-ZERO 64.5 ± 4.2 70.0 ± 5.1 67.2 ± 4.1

SPANISH SEAMLESS 10.7 ± 2.6 21.2 ± 4.5 26.5 ± 4.4 HIBIKI-ZERO 66.8 ± 3.9 69.0 ± 3.9 66.2 ± 4.9

PORTUGUESE SEAMLESS 11.8 ± 3.1 32.5 ± 6.0 22.8 ± 3.9 HIBIKI-ZERO 62.0 ± 4.1 60.7 ± 4.2 75.6 ± 3.4

GERMAN SEAMLESS 15.6 ± 2.7 25.2 ± 4.9 26.4 ± 4.8 HIBIKI-ZERO 73.5 ± 3.4 65.3 ± 4.3 69.9 ± 3.9

**Table 3.** Objective results of model adaptation to input Italian

speech with 850 hours of finetuning data on short-form evaluation.

BLEU ASR SPEAKER END LAAL (↑) BLEU (↑) SIM. (↑) OFFSET (↓) (↓)

SEAMLESS 32.5 32.0 22.2 3.0 3.5

OURS BASE 14.3 14.3 50.6 3.9 4.3 FINETUNED 31.4 31.0 55.2 3.7 4.5 FINETUNED + RL 32.1 31.9 54.2 3.0 3.5

## 4.5. Inference configuration

We encode audio with the streaming codec and feed the tokens to Hibiki-Zero while decoding the output tokens to obtain a streaming translation. At the end of the input, we force EOS tokens to our model input audio streams, and keep sampling until it produces its own text stream EOS. We use temperature of 0.8 and top-k of 250 for all tokens.

## 4.6. Results

Objective evaluations. Table 1 compares Hibiki-Zero against the best available baselines for simultaneous S2ST namely Seamless (Barrault et al., 2023) and Hibiki (Labiausse et al., 2025) with the latter only supporting French as input. Our model outperforms both baselines on longform speech translation with more than 5pts of ASR BLEU, 20pts of speaker similarity and lower latency compared to Seamless. In the short-form setting, our approach outperforms Hibiki by 3pts of ASR BLEU while being faster and is on par with Seamless on the quality/latency trade-off but surpasses it on speaker similarity by more than 30pts.

Audio fidelity and speech expressivity. Human evaluations reported in Table 2 confirm the clear advantage of Hibiki-Zero compared to Seamless on speaker identity transfer but also show that it produces higher quality audio with better speech naturalness. Compared to Hibiki on a Frenchto-English task, our model reaches equivalent audio quality while being more natural with a better speaker similarity.

0 250 500 750 updates

58

59

60

61

62

63

BLEU

0 250 500 750 updates

3.5

4.0

4.5

5.0

5.5

6.0 text LAAL

= 0.10 = 0.30 = 0.40 = 0.50 = 0.65

**Figure 4.** Influence of hyperparameter α during RL. We plot

the BLEU score and text LAAL over training for various α (see Eq. (3)), starting from the same supervised model using nw = 8.

New language adaptation. Following our method from Section 4.2.3, we build a small coarse-aligned Italian-to- English ST dataset containing less than 1000 hours in each language. Starting from the base translation model obtained after the training stage described in Section 4.2.3, we finetune and apply our RL method for the Italian-to-English translation task only. Results are presented in Table 3 and show that we attain the same translation quality/latency trade-off as Seamless with better speaker similarity on an extension to Italian of our short-form evaluation data. As shown in Appendix Table 6, our model adapted to Italian also retains most of its capabilities on the original languages.

## 4.7. Ablations

We present ablation results in figures 4, 6 and 7 using exponential moving average smoothing for readability. Performance during RL is represented using BLEU and text LAAL metrics. They are computed every τ updates on a validation set using the output text stream of the model which is synchronized with the output audio. As observed by Labiausse et al. (2025), we also notice very high BLEU scores (around 60) compared to evaluation scores (around 30). Indeed, our train and valid sets were obtained with the same data generation process described in Section 4.2.3 thus following the same translation style as MADLAD-3B (Kudugunta et al., 2023) that our ST models learn to replicate.

Ablation: Quality/Latency control during RL. We benchmark the effect of parameter α introduced in Section 3.3.1 which balances total and intermediate BLEU scores in the definition of process rewards. As illustrated in Figure 4, performing RL with high values of α leads to a higher translation latency but better overall translation quality as expected. On the contrary, lower values of α reduce latency further at the cost of a limited quality decrease.

Ablation: Process rewards computation frequency. Using α = 0.5, we study the effect of parameter nw introduced in Section 3.3.2 which controls how often process rewards are computed along a generated sequence. As shown in Figure 6, decreasing this parameter below 8 does not significantly impact the final quality/latency trade-off.

<!-- Page 8 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

Input speech Translation A

= 2

0:00 0:10 0:20 0:30 0:40 0:50 1:00 time (s)

Translation B

= 0

**Figure 5.** Illustration of coarse translation alignment patterns Waveform A is generated by a model trained on coarse alignments with random silences. Waveform B is generated by a model trained on coarse alignments with silences between sentences only.

0 250 500 750 updates

60.0

60.5

61.0

61.5

62.0

BLEU

0 250 500 750 updates

4.0

4.5

5.0

5.5

6.0 text LAAL nw = 1 nw = 4 nw = 8

**Figure 6.** Influence of hyperparameter nw during RL. We plot

the BLEU score and text LAAL over training for various nw (see Sec. 3.3.2) starting from the same supervised model using α = 0.5.

Ablation: Alternative configurations. In Figure 7, we compare alternative configurations that could be used for model development instead of our main setup referred to as Reference experiment. We keep α = 0.5 and nw = 8 fixed.

## Experiment

(A) performs RL using the full translation of the reference input text instead of sentencelevel prefixes to compute intermediate BLEU scores. This amounts to modify Equation 3 so it becomes r(i)

noprefix,t = (1 −α)BLEU(ˆy(i)

t, yT) + αBLEU(ˆy(i)

T, yT). We observe better quality performance but at the cost of latency. According to us, this comes from intermediate BLEU scores being much noisier as translated references are too optimistic, making it harder to discriminate between sequences to optimize latency during RL.

## Experiment

(B) performs RL starting from a base model trained with full sentence delays between input and output speech meaning that δi = di for each sentence index i using notations from Section 3.2.1. Therefore, latency is much higher when starting RL and is reduced to around 6 seconds which remains far worse than the reference experiment. We also observe this behavior in preliminary experiments where RL was unable to teach the base model to start translation of an input sentence before it ends as the base model was never trained in that manner during supervised training. This justifies the use of δi < di when building coarse alignments so RL can benefit from exploration.

0 250 500 750 updates

52

54

56

58

60

62

BLEU

0 250 500 750 updates

4

5

6

7

9

10

11 text LAAL

Reference experiment (A) no prefix ground-truth (B) i = di (C) = 0

**Figure 7.** Alternative configurations. We use α = 0.5 and nw =

8 for all experiments. Experiment (A) uses the full translation of the input speech as reference to compute process rewards instead of sentence-level prefixes as in Equation 3. Experiment (B) performs RL on a supervised model trained with full sentence-delay i.e. δi = di for each input sentence of index i. Experiment (C) performs RL on a supervised model trained with coarse alignments using silences between sentences only i.e. µ = 0.

## Experiment

(C) performs RL starting from a base model trained with coarse alignments using sentence-level silences only (µ = 0). We observe a degradation both in terms of quality and latency compared to the reference experiment. The loss of quality is expected when decreasing µ as we don’t delay as much the output with respect to the input. The cause of higher latency is illustrated in Figure 5 where waveform B (µ = 0) is a speech translation where silences are located between sentences only. This results in a higher average latency than waveform A (µ > 0) which presents a better distribution of speech along time.

## 4.8. Limitations

This work proposes an efficient method to perform multilingual speech translation and shows promising results on new input language adaptation. However, while our model exhibits state-of-the-art speaker identity preservation, there is no way to control the intensity of the accent from the input language in the generated speech. Such control could be added by providing accent-annotated samples during supervised training and using conditioning at inference.

## 5. Conclusion

We present Hibiki-Zero, a multilingual model for simultaneous and expressive speech and text translation without requiring word-level alignment of translation data for training. Our method leverages coarse sentence-level alignments to train a base model that is further refined through Reinforcement Learning using process rewards based on BLEU score only. Hibiki-Zero outperforms the state-ofthe-art across multiple languages with better quality/latency trade-offs, speaker identity transfer and speech naturalness. Moreover, we demonstrate new language adaptation with our method using less than 1000 hours of speech data. We release Hibiki-Zero weights as well as our multilingual longform evaluation dataset to benefit the research community.

![Figure extracted from page 8](2026-ICML-simultaneous-speech-to-speech-translation-without-aligned-data/page-008-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-simultaneous-speech-to-speech-translation-without-aligned-data/page-008-figure-02.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 8](2026-ICML-simultaneous-speech-to-speech-translation-without-aligned-data/page-008-figure-03.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 9 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

## References

Aepli, N., Amrhein, C., Schottmann, F., and Sennrich, R.

A benchmark for evaluating machine translation metrics on dialects without standard orthography. In Koehn, P., Haddon, B., Kocmi, T., and Monz, C. (eds.), Proceedings of the Eighth Conference on Machine Translation, WMT 2023, pp. 1045–1065. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.WMT-1.99.

Barrault, L., Chung, Y., Meglioli, M. C., Dale, D., Dong,

N., Duppenthaler, M., Duquenne, P., Ellis, B., Elsahar, H., Haaheim, J., Hoffman, J., Hwang, M., Inaguma, H., Klaiber, C., Kulikov, I., Li, P., Licht, D., Maillard, J., Mavlyutov, R., Rakotoarison, A., Sadagopan, K. R., Ramakrishnan, A., Tran, T., Wenzek, G., Yang, Y., Ye, E., Evtimov, I., Fernandez, P., Gao, C., Hansanti, P., Kalbassi, E., Kallet, A., Kozhevnikov, A., Gonzalez, G. M., Roman, R. S., Touret, C., Wong, C., Wood, C., Yu, B., Andrews, P., Balioglu, C., Chen, P., Costa-juss`a, M. R., Elbayad, M., Gong, H., Guzm´an, F., Heffernan, K., Jain, S., Kao, J., Lee, A., Ma, X., Mourachko, A., Peloquin, B. N., Pino, J., Popuri, S., Ropers, C., Saleem, S., Schwenk, H., Sun, A. Y., Tomasello, P., Wang, C., Wang, J., Wang, S., and Williamson, M. Seamless: Multilingual expressive and streaming speech translation. CoRR, abs/2312.05187, 2023. doi: 10.48550/ARXIV.2312.05187.

Chen, S., Wang, C., Chen, Z., Wu, Y., Liu, S., Chen, Z., Li,

J., Kanda, N., Yoshioka, T., Xiao, X., Wu, J., Zhou, L., Ren, S., Qian, Y., Qian, Y., Wu, J., Zeng, M., Yu, X., and Wei, F. Wavlm: Large-scale self-supervised pre-training for full stack speech processing. IEEE J. Sel. Top. Signal Process., 2022.

Cheng, S., Bao, Y., Huang, Z., Lu, Y., Peng, N., Xu, L.,

Yu, R., Cao, R., Du, Y., Han, T., Hu, Y., Li, Z., Liu,

S., Ma, S., Pan, S., Xiao, J., Xu, N., Yang, M., Ye, R., Yu, Y., Zhang, J., Zhang, R., Zhang, W., Zhu, W., Zou,

L., Lu, L., Wang, Y., and Wu, Y. Seed liveinterpret 2.0: End-to-end simultaneous speech-to-speech translation with your voice. CoRR, abs/2507.17527, 2025. doi: 10.48550/ARXIV.2507.17527. URL https://doi. org/10.48550/arXiv.2507.17527.

Copet, J., Kreuk, F., Gat, I., Remez, T., Kant, D., Synnaeve,

G., Adi, Y., and D´efossez, A. Simple and controllable music generation. In Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., and Levine, S. (eds.), Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, 2023.

de Oliveira, F. S., Casanova, E., J´unior, A. C., da Silva Soares, A., and Filho, A. R. G. CML-TTS: A multilingual dataset for speech synthesis in low-resource languages. In Text, Speech, and Dialogue - 26th International Conference, TSD 2023, Pilsen, Czech Republic, September 4-6, 2023, Proceedings, pp. 188–199, 2023. doi: 10.1007/978-3-031-40498-6\ 17. URL https:// doi.org/10.1007/978-3-031-40498-6_17.

D´efossez, A., Mazar´e, L., Orsini, M., Royer, A., P´erez,

P., J´egou, H., Grave, E., and Zeghidour, N. Moshi: a speech-text foundation model for real-time dialogue. CoRR, abs/2410.00037, 2024. doi: 10.48550/ARXIV. 2410.00037.

Hendrycks, D. and Gimpel, K. Gaussian error linear units

(gelus). arXiv preprint arXiv:1606.08415, 2016.

Iranzo-S´anchez, J., Silvestre-Cerd`a, J. A., Jorge, J., Rosell´o,

N., Gim´enez, A., Sanch´ıs, A., Civera, J., and Juan, A. Europarl-st: A multilingual corpus for speech translation of parliamentary debates. In 2020 IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2020, Barcelona, Spain, May 4-8, 2020, pp. 8229–8233, 2020. doi: 10.1109/ ICASSP40776.2020.9054626. URL https://doi. org/10.1109/ICASSP40776.2020.9054626.

Jia, Y., Weiss, R. J., Biadsy, F., Macherey, W., Johnson,

M., Chen, Z., and Wu, Y. Direct Speech-to-Speech Translation with a Sequence-to-Sequence Model. In Proc. Interspeech 2019, pp. 1123–1127, 2019. doi: 10.21437/Interspeech.2019-1951.

Jia, Y., Ramanovich, M. T., Remez, T., and Pomerantz, R.

Translatotron 2: High-quality direct speech-to-speech translation with voice preservation. In Chaudhuri, K., Jegelka, S., Song, L., Szepesvari, C., Niu, G., and Sabato, S. (eds.), Proceedings of the 39th International Conference on Machine Learning, volume 162 of Proceedings of Machine Learning Research, pp. 10120–10134. PMLR, 17–23 Jul 2022.

Kudugunta, S., Caswell, I., Zhang, B., Garcia, X., Xin,

D., Kusupati, A., Stella, R., Bapna, A., and Firat, O. MADLAD-400: A multilingual and document-level large audited dataset. In Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., and Levine, S. (eds.), Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, 2023.

Kyutai. Helium 1: a modular and multilingual llm. Kyutai, 2025. URL https://kyutai.org/blog/ 2025-04-30-helium.

Labiausse, T., Mazar´e, L., Grave, E., D´efossez, A., and

Zeghidour, N. High-fidelity simultaneous speech-tospeech translation. In Forty-second International Conference on Machine Learning, ICML 2025, Vancouver,

<!-- Page 10 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

BC, Canada, July 13-19, 2025, 2025. URL https: //openreview.net/forum?id=fgjN8B6xVX.

Lee, A., Chen, P.-J., Wang, C., Gu, J., Popuri, S., Ma,

X., Polyak, A., Adi, Y., He, Q., Tang, Y., Pino, J., and Hsu, W.-N. Direct speech-to-speech translation with discrete units. In Muresan, S., Nakov, P., and Villavicencio, A. (eds.), Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 3327–3339, Dublin, Ireland, May 2022a. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.235.

Lee, D., Kim, C., Kim, S., Cho, M., and Han, W. Autore- gressive image generation using residual quantization. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2022, New Orleans, LA, USA, June 18-24, 2022, pp. 11513–11522. IEEE, 2022b. doi: 10.1109/CVPR52688.2022.01123.

Loshchilov, I. and Hutter, F. Decoupled weight decay regu- larization. In 7th International Conference on Learning Representations, ICLR 2019, 2019.

Misiunas, K. and Ablavatski, A. Real-time speech-to-speech translation. 2025. URL https://research.google/blog/ real-time-speech-to-speech-translation/. Google Research.

Nakamura, S., Markov, K., Nakaiwa, H., Kikui, G., Kawai,

H., Jitsuhiro, T., Zhang, J.-S., Yamamoto, H., Sumita, E., and Yamamoto, S. The ATR multilingual speech-tospeech translation system. IEEE Transactions on Audio, Speech, and Language Processing, 2006.

Papi, S., Gaido, M., Negri, M., and Turchi, M. Overgeneration cannot be rewarded: Length-adaptive average lagging for simultaneous speech translation. CoRR, abs/2206.05807, 2022. doi: 10.48550/ARXIV.2206. 05807.

Papineni, K., Roukos, S., Ward, T., and Zhu, W. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics, July 6-12, 2002, Philadelphia, PA, USA, pp. 311–318, 2002. doi: 10.3115/ 1073083.1073135. URL https://aclanthology. org/P02-1040/.

Post, M. A call for clarity in reporting BLEU scores. In

Proceedings of the Third Conference on Machine Translation: Research Papers, pp. 186–191, Brussels, Belgium, October 2018. Association for Computational Linguistics. doi: 10.18653/v1/W18-6319.

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey,

C., and Sutskever, I. Robust speech recognition via largescale weak supervision. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), International Conference on Machine Learning, ICML 2023, volume 202 of Proceedings of Machine Learning Research, pp. 28492–28518. PMLR, 2023.

Rastogi, A., Jiang, A. Q., Lo, A., Berrada, G., Lample,

G., Rute, J., Barmentlo, J., Yadav, K., Khandelwal, K., Chandu, K. R., Blier, L., Saulnier, L., Dinot, M., Darrin, M., Gupta, N., Soletskyi, R., Vaze, S., Scao, T. L., Wang, Y., Yang, A., Liu, A. H., Sablayrolles, A., H´eliou, A., Martin, A., Ehrenberg, A., Agarwal, A., Roux, A., Darcet, A., Mensch, A., Bout, B., Rozi`ere, B., Monicault, B. D., Bamford, C., Wallenwein, C., Renaudin, C., Lanfranchi, C., Dabert, D., Mizelle, D., de Las Casas, D., Chane-Sane, E., Fugier, E., Hanna, E. B., Delerce, G., Guinet, G., Novikov, G., Martin, G., Jaju, H., Ludziejewski, J., Chabran, J., Delignon, J., Studnia, J., Amar, J., Roberts, J. S., Denize, J., Saxena, K., Jain, K., Zhao, L., Martin, L., Gao, L., Lavaud, L. R., Pellat, M., Guillaumin, M., Felardos, M., Augustin, M., Seznec, M., Raghuraman, N., Duchenne, O., Wang, P., von Platen, P., Saffer, P., Jacob, P., Wambergue, P., Kurylowicz, P., Muddireddy, P. R., Chagniot, P., Stock, P., Agrawal, P., Sauvestre, R., Delacourt, R., Gandhi, S., Subramanian, S., Dalal, S., Gandhi, S., Ghosh, S., Mishra, S., Aithal, S., Antoniak, S., Schueller, T., Lavril, T., Robert, T., Wang, T., Lacroix, T., Nemychnikova, V., Paltz, V., Richard, V., Li, W., Marshall, W., Zhang, X., and Tang, Y. Magistral. CoRR, abs/2506.10910, 2025. doi: 10.48550/ARXIV.2506.10910. URL https: //doi.org/10.48550/arXiv.2506.10910.

Rei, R., Stewart, C., Farinha, A. C., and Lavie, A. COMET:

A neural framework for MT evaluation. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, pp. 2685– 2702, 2020. doi: 10.18653/V1/2020.EMNLP-MAIN. 213. URL https://doi.org/10.18653/v1/ 2020.emnlp-main.213.

Rubenstein, P. K., Asawaroengchai, C., Nguyen, D. D.,

Bapna, A., Borsos, Z., de Chaumont Quitry, F., Chen, P., Badawy, D. E., Han, W., Kharitonov, E., Muckenhirn, H., Padfield, D., Qin, J., Rozenberg, D., Sainath, T. N., Schalkwyk, J., Sharifi, M., Ramanovich, M. T., Tagliasacchi, M., Tudor, A., Velimirovic, M., Vincent, D., Yu, J., Wang, Y., Zayats, V., Zeghidour, N., Zhang, Y., Zhang, Z., Zilka, L., and Frank, C. H. Audiopalm: A large language model that can speak and listen. CoRR, abs/2306.12925, 2023. doi: 10.48550/ARXIV.2306.12925.

Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and

Klimov, O. Proximal policy optimization algorithms.

<!-- Page 11 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

CoRR, abs/1707.06347, 2017. URL http://arxiv. org/abs/1707.06347.

Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M.,

Li, Y. K., Wu, Y., and Guo, D. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. CoRR, abs/2402.03300, 2024. doi: 10.48550/ ARXIV.2402.03300. URL https://doi.org/10. 48550/arXiv.2402.03300.

Shazeer, N. Glu variants improve transformer. arXiv preprint arXiv:2002.05202, 2020.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones,

L., Gomez, A. N., and and, L. K. Attention is all you need. In Advances in Neural Information Processing Systems (NeurIPS), pp. 5998–6008, 2017.

Wahlster, W. Verbmobil: Foundations of speech-to-speech translation. Springer, 2000.

Xu, T., Huang, Z., Sun, J., Cheng, S., and Lam, W.

Seqpo-simt: Sequential policy optimization for simultaneous machine translation. In Findings of the Association for Computational Linguistics, ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pp. 16107–16123, 2025. URL https://aclanthology.org/2025. findings-acl.828/.

Yang, D., Tian, J., Tan, X., Huang, R., Liu, S., Chang, X.,

Shi, J., Zhao, S., Bian, J., Wu, X., et al. Uniaudio: An audio foundation model toward universal audio generation. arXiv preprint arXiv:2310.00704, 2023.

Yu, D., Zhao, Y., Zhu, J., Xu, Y., Zhou, Y., and Zong,

C. Simulpl: Aligning human preferences in simultaneous machine translation. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025, 2025. URL https: //openreview.net/forum?id=XBF63bHDZw.

Zeghidour, N., Luebs, A., Omran, A., Skoglund, J., and

Tagliasacchi, M. Soundstream: An end-to-end neural audio codec. IEEE ACM Trans. Audio Speech Lang. Process., 30:495–507, 2022. doi: 10.1109/TASLP.2021. 3129994.

Zeghidour, N., Kharitonov, E., Orsini, M., Volhejn, V., de Marmiesse, G., Grave, E., P´erez, P., Mazar´e, L., and D´efossez, A. Streaming sequence-to-sequence learning with delayed streams modeling. CoRR, abs/2509.08753, 2025. doi: 10.48550/ARXIV.2509.08753. URL https: //doi.org/10.48550/arXiv.2509.08753.

Zhang, S., Fang, Q., Guo, S., Ma, Z., Zhang, M., and

Feng, Y. Streamspeech: Simultaneous speech-to-speech translation with multi-task learning. In Ku, L., Martins, A., and Srikumar, V. (eds.), Proceedings of the

62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pp. 8964–8986. Association for Computational Linguistics, 2024a. doi: 10.18653/V1/2024.ACL-LONG.485.

Zhang, X., Zhang, D., Li, S., Zhou, Y., and Qiu, X. Speech- tokenizer: Unified speech tokenizer for speech language models. In The Twelfth International Conference on Learning Representations, 2024b.

<!-- Page 12 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

## Appendix

**Table 4.** Objective evaluations of multilingual and monolingual base supervised models. As the multilingual base model is trained on

four times more data than each monolingual model, it has seen the same amount of each language after 400K updates as any monolingual model after 100K updates. For comparison, we provide evaluations after 100K and 400K updates for the multilingual model.

SHORT-FORM LONG-FORM

MODEL ASR SPEAKER END ASR SPEAKER END BLEU (↑) BLEU (↑) SIM. (↑) OFFSET (↓) LAAL (↓) BLEU (↑) BLEU (↑) SIM. (↑) OFFSET (↓) LAAL (↓)

FRENCH BASE@100K 31.8 31.3 52.1 3.1 3.6 28.7 27.7 67.6 3.4 6.0 BASE@400K 34.5 34.1 53.1 3.0 3.7 31.1 28.8 67.4 3.4 6.6 BASE-FR@100K 34.2 33.4 52.5 3.0 3.6 29.8 28.6 67.3 3.2 6.1 BASE-ES@100K 5.3 5.1 39.6 4.4 5.1 5.9 5.5 60.1 7.7 11.2 BASE-PT@100K 6.7 6.6 41.2 4.6 5.0 7.9 8.0 62.0 5.8 8.5 BASE-DE@100K 1.6 1.6 41.6 4.3 5.6 2.0 1.7 64.1 8.3 10.8

SPANISH BASE@100K 31.5 31.4 59.2 3.4 4.1 31.1 30.9 69.5 3.9 6.6 BASE@400K 33.8 33.6 60.3 3.4 4.1 33.3 32.6 69.4 3.8 6.6 BASE-FR@100K 8.9 8.8 48.2 3.8 4.1 11.4 11.4 63.6 4.6 7.3 BASE-ES@100K 33.2 33.0 59.9 3.5 4.2 33.5 32.7 69.8 4.1 6.6 BASE-PT@100K 22.3 22.2 50.2 3.5 4.1 24.5 24.4 63.8 4.2 7.0 BASE-DE@100K 1.3 1.1 38.9 4.2 5.1 2.1 1.7 57.1 9.6 12.3

PORTUGUESE BASE@100K 31.7 31.4 53.5 3.7 4.2 31.7 30.7 66.9 3.3 6.6 BASE@400K 33.9 33.7 54.5 3.6 4.1 33.5 32.5 67.4 3.1 6.5 BASE-FR@100K 2.5 2.4 43.2 4.2 4.7 9.0 8.6 53.6 4.9 7.8 BASE-ES@100K 12.8 12.8 47.3 4.2 4.9 23.9 23.0 56.9 3.8 8.0 BASE-PT@100K 32.5 32.2 54.4 3.9 4.4 32.2 30.8 67.8 3.4 7.0 BASE-DE@100K 0.6 0.7 42.2 3.9 5.1 1.3 0.9 52.0 10.8 11.7

GERMAN BASE@100K 25.9 25.7 53.6 2.7 3.5 28.3 28.0 70.6 3.4 6.4 BASE@400K 28.3 28.0 54.6 2.7 3.6 31.1 30.5 70.5 3.3 5.8 BASE-FR@100K 0.7 0.7 35.6 4.4 4.6 1.4 1.2 54.5 12.1 10.0 BASE-ES@100K 0.9 0.8 35.4 4.6 5.2 1.8 1.1 50.9 14.5 16.0 BASE-PT@100K 0.7 0.7 33.3 4.1 4.6 1.6 1.4 50.2 8.1 9.6 BASE-DE@100K 28.6 28.3 55.6 2.9 3.8 30.8 29.9 71.4 3.4 6.2

<!-- Page 13 -->

Simultaneous Speech-to-Speech Translation Without Aligned Data

**Table 5.** Objective evaluations of our base and fine-tuned models compared to Hibiki-Zero.

SHORT-FORM LONG-FORM

MODEL ASR ASR SPEAKER END ASR ASR SPEAKER END BLEU (↑) BLEU (↑) COMET (↑) SIM. (↑) OFFSET (↓) LAAL (↓) BLEU (↑) BLEU (↑) COMET (↑) SIM. (↑) OFFSET (↓) LAAL (↓)

FRENCH BASE 34.4 34.0 79.2 53.1 3.0 3.6 31.1 29.7 43.1 67.5 3.5 6.2 FINETUNED 34.3 33.9 78.7 52.9 3.5 4.0 31.0 29.0 41.6 66.7 4.8 6.9 HIBIKI-ZERO 35.0 34.6 80.3 49.5 2.1 2.8 30.6 28.7 43.7 61.3 2.3 6.1

SPANISH BASE 34.0 33.7 80.1 60.2 3.3 4.1 33.8 32.8 45.3 69.8 3.8 6.3 FINETUNED 33.9 33.7 80.3 60.2 3.6 4.2 32.9 32.2 43.5 69.2 4.7 6.7 HIBIKI-ZERO 33.8 33.9 80.3 57.0 2.3 3.1 32.3 31.5 42.3 64.6 2.6 5.6

PORTUGUESE BASE 33.5 33.2 78.8 54.2 3.6 4.2 34.0 32.6 42.2 67.0 3.3 6.6 FINETUNED 34.0 33.9 78.8 55.5 3.9 4.3 33.7 31.7 42.2 67.5 4.6 7.3 HIBIKI-ZERO 33.6 33.6 78.9 51.4 2.4 3.0 33.2 31.3 42.6 62.1 2.3 6.3

GERMAN BASE 28.6 28.4 83.0 54.8 2.7 3.6 30.6 30.0 44.7 70.6 3.3 6.0 FINETUNED 28.1 27.9 82.4 54.6 2.9 3.7 30.6 29.4 44.8 70.3 4.5 7.0 HIBIKI-ZERO 28.7 28.6 82.0 51.5 1.9 2.8 29.1 28.3 42.3 66.0 2.0 5.9

**Table 6.** Comparison between Hibiki-Zero and our model adapted for Italian on original languages with long-form evaluation.

MODEL BLEU ASR BLEU SPEAKER SIM. END OFFSET LAAL (↑) (↑) (↑) (↓) (↓)

FRENCH HIBIKI-ZERO 30.6 28.7 61.3 2.3 6.1 ITALIAN FINETUNED + RL 30.6 29.1 59.8 3.0 6.2

SPANISH HIBIKI-ZERO 32.3 31.5 64.6 2.6 5.6 ITALIAN FINETUNED + RL 31.1 30.3 62.8 2.6 6.3

PORTUGUESE HIBIKI-ZERO 33.2 31.3 62.1 2.3 6.3 ITALIAN FINETUNED + RL 32.9 31.3 56.4 2.7 6.5

GERMAN HIBIKI-ZERO 29.1 28.3 66.0 2.0 5.9 ITALIAN FINETUNED + RL 30.5 28.7 64.2 2.7 6.4
