---
title: "Efficient Hallucination Detection: Adaptive Bayesian Estimation of Semantic Entropy with Guided Semantic Exploration"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/40595
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/40595/44556
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Efficient Hallucination Detection: Adaptive Bayesian Estimation of Semantic Entropy with Guided Semantic Exploration

<!-- Page 1 -->

Efficient Hallucination Detection: Adaptive Bayesian Estimation of Semantic

Entropy with Guided Semantic Exploration

Qiyao Sun1, Xingming Li1, Xixiang He1, Ao Cheng1, Xuanyu Ji1,

Hailun Lu2, Runke Huang3, Qingyong Hu2*

1National University of Defense Technology, Changsha, China 2Intelligent Game and Decision Lab, Beijing, China 3The Chinese University of Hong Kong, Shenzhen, China {sunqiyao18, lixingming, hexixiang, chengao18, jixuanyu18}@nudt.edu.cn, Luhailun0728@outlook.com, runkehuang@cuhk.edu.cn, huqingyong15@outlook.com

## Abstract

Large language models (LLMs) have achieved remarkable success in various natural language processing tasks, yet they remain prone to generating factually incorrect outputs—known as “hallucinations”. While recent approaches have shown promise for hallucination detection by repeatedly sampling from LLMs and quantifying the semantic inconsistency among the generated responses, they rely on fixed sampling budgets that fail to adapt to query complexity, resulting in computational inefficiency. We propose an Adaptive Bayesian Estimation framework for Semantic Entropy with Guided Semantic Exploration, which dynamically adjusts sampling requirements based on observed uncertainty. Our approach employs a hierarchical Bayesian framework to model the semantic distribution, enabling dynamic control of sampling iterations through variance-based thresholds that terminate generation once sufficient certainty is achieved. We also develop a perturbation-based importance sampling strategy to systematically explore the semantic space. Extensive experiments on four QA datasets demonstrate that our method achieves superior hallucination detection performance with significant efficiency gains. In low-budget scenarios, our approach requires about 50% fewer samples to achieve comparable detection performance to existing methods, while delivers an average AUROC improvement of 12.6% under the same sampling budget.

## Introduction

Large language models (LLMs) (Zhao et al. 2025) have demonstrated remarkable capabilities in language understanding, generation, and reasoning, fundamentally transforming the landscape of natural language processing (Chen et al. 2023; Lai and Nissim 2024). However, these models exhibit a critical limitation: they are prone to generating hallucination contents that appear plausible and coherent but lack factual grounding or contradict verifiable information (Wang et al. 2023a). Unlike traditional natural language generation systems where hallucinations primarily involve inconsistencies with source content, LLM hallucinations encompass a broader spectrum of factual errors and faithfulness issues due to their open-ended nature (Huang et al.

*Corresponding author. Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

**Figure 1.** Comparison of fixed sampling (a) versus our adaptive Bayesian approach (b) for hallucination detection. Fixed sampling wastes computational resources on simple queries (LLM1) while failing to discover semantic diversity in complex cases (LLM2). Our method dynamically adjusts sampling based on variance thresholds, enabling efficient and accurate hallucination detection.

2025). The human-like fluency of LLM responses makes these hallucinations particularly difficult to detect, creating significant risks when deploying these models in real-world scenarios such as education, economics, science and so on (Lee et al. 2024; Wang et al. 2024; Luo et al. 2025). This fundamental challenge poses a substantial barrier to the reliable integration of LLMs into critical information systems where accuracy and trustworthiness are paramount.

Current hallucination detection methods can be broadly categorized into four paradigms based on their underlying mechanisms. (1) External knowledge-based methods leverage retrieval systems to validate LLM outputs against authoritative sources (Choi et al. 2023; Dhuliawala et al. 2024), but face limitations in domain coverage and require com-

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

33117

![Figure extracted from page 1](2026-AAAI-efficient-hallucination-detection-adaptive-bayesian-estimation-of-semantic-entro/page-001-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 2 -->

plex verification pipelines. (2) Metacognition-based methods prompt LLMs to assess their own confidence (Kadavath et al. 2022), yet struggle with unreliability. (3) Singlesample methods analyze token-level patterns or hidden states within individual generations (Kossen et al. 2024; Zhang et al. 2023), offering computational efficiency but limited accuracy. (4) Multi-sample methods, particularly semantic entropy approaches (Farquhar et al. 2024), estimate uncertainty by clustering semantically equivalent outputs across multiple samples, demonstrating superior detection performance compared to other methods.

Despite their effectiveness, existing multi-sample methods suffer from a critical limitation: they employ fixed sampling budgets that fail to adapt to the inherent complexity of different queries. Simple factual questions may require only a few samples to reliably estimate semantic uncertainty, while complex or ambiguous queries necessitate extensive exploration of the semantic space. This one-size-fits-all approach results in computational waste for straightforward queries and insufficient sampling for challenging ones. Furthermore, current methods rely on multinomial sampling, which may repeatedly generate semantically similar outputs without efficiently exploring the full distribution of possible meanings. The lack of adaptive mechanisms and guided exploration strategies fundamentally limits the practical deployment of these methods in low-budget settings.

To address these limitations, we propose an Adaptive Bayesian Estimation framework for Semantic Entropy with Guided Semantic Exploration. Our approach introduces a hierarchical Bayesian framework that explicitly models the semantic distribution through a Dirichlet prior and decomposes the semantic entropy expectation via marginalization into two components: the posterior over the number of semantic categories and the conditional entropy given each possible category count. Building on this probabilistic foundation, we implement variance-based adaptive sampling that dynamically adjusts the number of queries based on posterior uncertainty, enabling efficient allocation of computational resources according to problem complexity. To accelerate variance convergence and enhance sampling efficiency, we develop a guided exploration strategy that identifies semantically critical tokens through importance weighting and systematically perturbs them to discover diverse interpretations, while employing importance sampling to maintain unbiased estimates.

Extensive experiments on four QA datasets demonstrate that our method achieves comparable or superior hallucination detection performance while significantly reducing the required number of model queries.

The main contributions can be summarized as follows:

• We introduce an adaptive Bayesian framework for semantic entropy estimation that dynamically adjusts sampling requirements based on observed uncertainty. • We develop a guided semantic exploration strategy with importance sampling that discovers diverse semantic interpretations by perturbing critical tokens, accelerating convergence compared to random sampling. • We demonstrate through comprehensive experiments that our method achieves state-of-the-art hallucination detection performance with significantly fewer samples, particularly excelling in resource-constrained scenarios.

## Related Work

## 2.1 Hallucination

Hallucination in large language models refers to the generation of content that appears coherent but lacks factual support or deviates from the intended output (Wang et al. 2023a). Current research categorizes LLM hallucinations into two main types: factuality hallucination and faithfulness hallucination (Huang et al. 2025). Factuality hallucination occurs when generated content contains errors that contradict verifiable facts, while faithfulness hallucination manifests as inconsistencies with provided context or internal logic within the generated text. The ability of LLMs to produce highly convincing and human-like responses makes detecting these hallucinations particularly challenging, necessitating the development of robust detection methods.

## 2.2 Hallucination Detection

The detection of hallucinations in LLMs has emerged as a critical research area, with various approaches developed to identify when models generate factually incorrect or inconsistent content. Current detection methods can be broadly categorized into three main paradigms based on their underlying mechanisms.

External knowledge based methods use external knowledge bases to guide LLM generation and validate outputs (Choi et al. 2023; Dhuliawala et al. 2024; Min et al. 2023; Wang et al. 2023b). However, these approaches face significant challenges as they heavily depend on the accuracy and completeness of external knowledge sources, and struggle with domain-specific or rapidly evolving information.

Metacognition based methods utilize the metacognitive capabilities of LLMs—their ability to reflect on and evaluate their own knowledge states. The fundamental assumption is that LLMs develop implicit metacognitive signals during training that enable them to distinguish between confident, factual generations and uncertain, potentially hallucinated content (Kadavath et al. 2022). These methods face challenges in calibrating self-awareness across diverse domains and struggle when the model’s metacognitive judgments are themselves unreliable.

Single-sample based methods require only a single forward pass through the model. FOCUS (Zhang et al. 2023) retrieve relevant tokens from the generation process and analyze token-level confidence patterns. While (Kossen et al. 2024) train specialized classifiers to predict uncertainty metrics directly from the model’s hidden states. These methods offer computational efficiency but often face challenges in interpretability and accuracy.

Multi-sample based methods detect hallucinations by analyzing inconsistencies across multiple LLM outputs. Early approaches using Lexical Similarity (Lin, Liu, and Shang 2022) and Predictive Entropy (Kadavath et al. 2022)

33118

<!-- Page 3 -->

often overestimated uncertainty due to diverse surface forms. Semantic Entropy (Kuhn, Gal, and Farquhar 2023; Farquhar et al. 2024) marked a breakthrough by clustering outputs into semantic equivalence classes and computing entropy over meaning distributions. While subsequent refinements (Duan et al. 2024; Bakman et al. 2024; Chen et al. 2024; Nikitin et al. 2024) and SDLG’s (Aichberger et al. 2025) diversified exploration strategies improved performance, all existing methods rely on fixed sampling budgets that ignore query complexity. Our adaptive framework addresses this limitation by dynamically adjusting sample sizes based on inherent uncertainty, achieving computational efficiency with detection accuracy improvement.

## Problem Formulation

Language Model Generation Let X denote the space of all possible prompts that can be presented to a language model. For a given prompt x ∈X, let Rx represent the set of all possible response sequences that the LLM can generate. We model the LLM’s generation process as a conditional probability distribution Pθ(r|x), where θ represents the model parameters and r ∈Rx is a response sequence.

Semantic Equivalence We define Mx as the set of distinct semantic meanings for prompt x. Let fx: Rx →Mx be a mapping function that assigns each response r ∈Rx to its corresponding meaning class m ∈Mx. This mapping induces a partition over the response space, where responses within the same partition are semantically equivalent.

Semantic Entropy Given a prompt x and the LLM’s response distribution Pθ(r|x), The probability of generating meaning m is:

p(m|x) =

X r∈Rx:fx(r)=m

Pθ(r|x) (1)

The semantic entropy for prompt x is then defined as the Shannon entropy over the meaning distribution:

Hsem = −

X m∈Mx p(m|x) log p(m|x) (2)

Estimation Problem In practice, we cannot enumerate all possible responses in Rx to compute the exact semantic entropy. Instead, treating Hsem as a random variable, we estimate it from a finite dataset obtained by sampling from the LLM. For a given prompt x, we generate N independent response sequences r1,..., rN ∼Pθ(·|x).

For each sampled sequence ri, we determine its semantic meaning mi = fx(ri), yielding a corresponding list of meanings m1,..., mN. Additionally, we obtain the generation probability Pθ(ri|x) for each sequence. Thus, the estimation dataset is defined as:

D = {(r1, m1, Pθ(r1|x)),..., (rN, mN, Pθ(rN|x))} (3)

We seek to develop an efficient semantic entropy estimator that dynamically increases N based on the observed sample variance, ensuring reliable yet minimal sampling cost.

## Algorithm

1: Bayesian Estimation of Semantic Entropy Input: Prompt x, LLM Pθ, variance threshold γ Parameter: Initial samples N0, top-k alternatives Output: Semantic entropy ˆHsem

1: // Initialize with weighted perplexity prior 2: Generate initial samples {r1,..., rN0} ∼Pθ(·|x) 3: Compute token importance weights wi,j ▷Eq. (15) 4: Calculate weighted perplexity ˆλ ▷Eq. (17) 5: Set prior p(K) ∼Poisson(ˆλ) 6: // Initialize dataset with initial samples 7: D ←{(ri, mi, Pθ(ri|x)): i = 1,..., N0} 8: Compute initial E[h|D] and Var[h|D] ▷Eq. (4-5) 9: // Adaptive sampling loop 10: while Var[h|D] > γ do 11: Generate new sample (r′, w′) via Guided Semantic Exploration from random r ∈D using top-k

▷Section 4.2 12: Add (r′, m′, Pθ(r′|x)) to D 13: // Bayesian update 14: Update effective counts nj and Dirichlet posterior parameters ˜αj with importance weight w′

▷Eq. (23-24) 15: Update truncated Dirichlet posterior constraints C

▷Eq. (6-7) 16: Compute posterior p(K|D) ▷Eq. (11) 17: Recalculate E[h|D] and Var[h|D] ▷Eq. (4-5) 18: end while 19: return ˆHsem = E[h|D]

## 4 Method

We propose a hierarchical Bayesian framework for efficient semantic entropy estimation that addresses two fundamental challenges: uncertainty in the number of distinct semantic meanings and the computational cost of exhaustive sampling. Our approach decomposes the estimation problem by marginalizing over the unknown cardinality of the semantic space, employing a truncated Dirichlet posterior that incorporates generation probability constraints to provide tighter uncertainty bounds. To adaptively calibrate prior beliefs, we introduce a weighted perplexity metric that captures prompt-specific semantic diversity. Furthermore, we develop a guided semantic exploration strategy using importance sampling, which systematically perturbs semantically critical tokens to discover diverse interpretations while maintaining unbiased estimates. The framework dynamically adjusts sampling based on observed variance, enabling reliable semantic entropy estimation with minimal cost. We detail the hierarchical Bayesian framework (Section 4.1) and the guided exploration mechanism (Section 4.2) below.

## 4.1 Hierarchical Bayesian Framework

We propose a hierarchical Bayesian framework that stratifies the semantic entropy estimation based on the number of distinct semantic categories |Mx|. Given the dataset D containing sampled responses and their semantic meanings, the key insight is that the semantic entropy Hsem fundamentally

33119

<!-- Page 4 -->

depends on both the cardinality of the meaning space and the probability distribution over these meanings.

Let K = |Mx| denote the number of distinct semantic meanings in Mx, and let h be a random variable that represents our belief about the value of Hsem. To compute its expected value given the observed dataset D, we apply the law of total expectation to marginalize over the unknown number of semantic categories:

E[h|D] =

∞ X

K=1

E[h|K, D] · p(K|D) (4)

Var[h|D] = EK[Var[h|K, D]] + VarK[E[h|K, D]] (5)

This hierarchical decomposition naturally separates the estimation problem into two components. E[h|K, D] represents the expected entropy conditioned on exactly K distinct semantic meanings being present in Mx. This expectation is taken with respect to the posterior distribution of p given both K and the observed data. p(K|D) captures our posterior belief about the cardinality of the meaning space after observing the sampled responses.

To enable adaptive sampling, we employ the total variance Var[h|D] from Equation (5) as our stopping criterion. The sampling process terminates when Var[h|D] < γ, where γ is a predefined threshold that controls the trade-off between estimation accuracy and computational cost.

Calculation of E[h|K, D] and Var[h|K, D] Given a fixed number of semantic categories K, we model the probability distribution over these categories using a Dirichlet prior. Let p = (p1,..., pK) denote the probability vector where pj represents the probability of generating semantic meaning j ∈{1,..., K}. We adopt a uninformative Dirichlet prior p ∼Dir(α0,..., α0).

After observing the dataset D, let nj = |{i: mi = j, i = 1,..., N}| denotes the number of sampled responses that map to semantic meaning j. Under standard Bayesian updating, the posterior would be Dir(α0 + n1,..., α0 + nK).

However, the LLM’s generation probabilities provide additional constraints on the feasible probability space. For each semantic category j, the true probability pj satisfy:

pj ≥

X ri∈D: fx(ri)=j

Pθ(ri|x) ≜bj (6)

This constraint arises because we have directly observed specific sequences belonging to category j with their generation probabilities. The constraint set is thus defined as:

C = {p ∈∆K−1: pj ≥bj for all j = 1,..., K} (7)

where ∆K−1 denotes the K −1 dimensional probability simplex.

The posterior distribution becomes a truncated Dirichlet distribution. Let π(p) denote the density of Dir(α) where α = (α0 + n1,..., α0 + nK). The truncated Dirichlet distribution over C has density:

πC(p) =

( π(p)

ZC if p ∈C 0 otherwise (8)

where ZC =

R

C π(p)dp is the normalization constant. The expected semantic entropy given K and D is:

E[h|K, D] =

Z

H(p) · πC(p)dp (9)

where H(p) = −PK j=1 pj log pj is the Shannon entropy. Similarly, the variance is:

Var[h|K, D] =

Z

H2(p) · πC(p)dp −E2[h|K, D] (10)

In practice, these integrals are computed via selfnormalized importance sampling (Swaminathan and Joachims 2015). The detailed implementation is discussed in Appendix A.

Posterior Inference of p(K|D) To compute the posterior distribution p(K|D), we apply Bayes’ theorem:

p(K|D) = p(D|K) · p(K) P∞

K′=1 p(D|K′) · p(K′) (11)

Calculation of marginal likelihood p(D|K) Now we compute the marginal likelihood p(D|K), which represents the probability of observing the dataset D given K semantic categories. This requires marginalizing over all possible probability distributions p consistent with K categories:

p(D|K) =

Z p(D|p, K) · πC(p)dp (12)

Given the observed category counts n = (n1,..., nK) from the sampled responses, the likelihood follows a multinomial distribution:

p(D|p, K) = N! QK j=1 nj!

K Y j=1 pnj j (13)

The integral in Equation (12) can be efficiently evaluated using importance sampling employed for Equation (9).

Calculation of prior p(K) via weighted perplexity We model the unknown number of semantic classes K using a Poisson prior with parameter λ:

p(K) = λKe−λ

K! (14)

This choice reflects the view that distinct semantic meanings emerge as rare events in the LLM’s vast semantic space. The parameter λ controls the expected number of coherent semantic interpretations for a given prompt.

we propose an adaptive elicitation method that calibrates λ based on the LLM’s inherent uncertainty for the specific prompt, which begins by generating a small initial sample of N0 responses {r1,..., rN0} from Pθ(·|x). For each response ri, we quantify the semantic importance of individual tokens to capture their contribution to the overall meaning. Let ri = (ti,1,..., ti,Li) denote the token sequence of

33120

<!-- Page 5 -->

length Li. We compute the importance weight for token ti,j as:

wi,j = 1 −sim(ri, ri \ {ti,j}) (15) where sim measures the similarity between two sentences on a scale of 0 to 1 and r(0)

i \ {ti,j} denotes the response with token ti,j removed.

Using these importance weights, we compute a weighted perplexity for each response that emphasizes semantically critical tokens:

WPLi = exp

−

PLi j=1 wi,j log Pθ(ti,j|ti,<j, x)

PLi j=1 wi,j

!

(16)

where Pθ(ti,j|ti,<j, x) is the conditional probability of token ti,j given the preceding tokens and prompt.

The empirical estimate of λ is then obtained as:

ˆλ = 1

N0

N0 X i=1

WPLi (17)

This weighted perplexity serves as a principled proxy for semantic diversity: higher values indicate greater uncertainty in the model’s semantic space, suggesting more potential semantic categories.

To handle the infinite summation in Equation (11), we employ a truncation strategy. Since p(K) decays exponentially for large K under the Poisson prior, we truncate the summation at Kmax = max(Kobs, 3λ), where Kobs denotes the number of distinct semantic meanings observed in D.

## 4.2 Guided Semantic Exploration

To improve the efficiency of semantic entropy estimation, we develop a guided exploration strategy that leverages importance sampling to systematically explore the LLM’s semantic space. By strategically perturbing tokens at semantically critical positions and continuing generation from these points, we can discover diverse semantic interpretations while maintaining computational efficiency.

Guided Language Generation We employ a perturbation-based approach to construct sequences that explore alternative semantic branches. For a given response r = (t1,..., tL) ∼Pθ(·|x), we first identify semantically critical positions using the token importance weights defined in Equation (15). Let I = {i1, i2,..., iL} denote the indices of all tokens ordered by their importance weights in descending order, where wi1 ≥wi2 ≥... ≥wiL.

At each critical position ij ∈I, we examine the conditional token distribution Pθ(·|t<ij, x) and identify the top-k alternative tokens excluding the original choice:

Aij = top-k{t ∈V \ {tij}: Pθ(t|t<ij, x)} (18) where V denotes the vocabulary. For each alternative token t′ ∈Aij, we generate a new response by replacing tij with t′ and continuing the generation:

r′ = (t1,..., tij−1, t′, t′ ij+1,..., t′

L′) (19)

where t′ ij+1,..., t′

L′ are sampled from Pθ(·|t1,..., tij−1, t′, x).

Importance Sampling The guided semantic exploration process described above forcibly modifies certain tokens in the generated sequences, deviating from the LLM’s original distribution Pθ(·|x). Since we are no longer sampling directly from Pθ(·|x), we must correct for this bias through importance sampling with a properly defined proposal distribution q(r|x) that accurately captures our modified sampling procedure.

The proposal distribution is defined as:

q(r|x) =

X r′∈Rx p(r|r′, x) · Pθ(r′|x) (20)

where p(r|r′, x) represents the probability of transforming an initial response r′ into r through our guided generation process. Under specific assumptions about token selection (Aichberger et al. 2025), the proposal distribution takes the form:

q(r|x) = Pθ(r|x) Pθ(tj|t<j, x) (21)

where j is the index of the perturbed token in sequence r = (t1,..., tL).

The importance weight for a sample r drawn from q(·|x) is:

w(r) = Pθ(r|x)

q(r|x) = Pθ(tj|t<j, x) (22)

This weight ensures unbiased estimation while promoting exploration of lower-probability but potentially semantically distinct sequences (See Appendix B for proof).

Bayesian Update with Weighted Samples When incorporating samples obtained through importance sampling into our hierarchical Bayesian framework, we must properly account for their importance weights. Let {(r(1), w(1)),..., (r(N−1), w(N−1))} denote the sequence of weighted samples, where r(t) is drawn from q(·|x) with importance weight w(t).

We modify the effective counts to reflect the importance weights. If sample r(N) is assigned to semantic category j, the effective count update becomes:

n(N)

j = n(N−1)

j + w(N) (23) The Dirichlet posterior parameters are then updated as:

α(N)

j = α0 + n(N)

j (24) To maintain proper normalization, we scale the posterior parameters:

˜α(N)

j = α(N)

j · PK k=1 α(0)

k + N PK k=1 α(t)

k

(25)

This scaling ensures that the effective sample size grows linearly with T while properly weighting each sample’s contribution according to its importance in exploring the semantic space.

The modified likelihood for computing p(D|p, K) in Equation (13) becomes:

p(D|p, K) = Γ(N) QK j=1 Γ(nj(T))

K Y j=1 pnj

(T)

j (26)

33121

<!-- Page 6 -->

LLM Dataset P(True)

N=2 N=5

SAR SE SESDLG OURS SAR SE SESDLG OURS

Llama-2-7B

CoQA.468.591.609.618.695.627.683.688.748 TriviaQA.488.708.710.724.835.741.795.827.897 TruthfulQA.509.598.621.635.732.632.713.724.795 SimpleQA.521.721.796.891.895.768.930.956.959

Llama-3.1-8B

CoQA.568.655.699.648.738.648.756.769.799 TriviaQA.714.728.759.741.855.563.866.850.913 TruthfulQA.633.661.642.655.753.603.741.750.818 SimpleQA.655.652.825.830.913.614.930.934.942

Mistral-Small-24B

CoQA.618.643.658.669.762.660.758.765.825 TriviaQA.624.641.689.703.872.778.790.817.928 TruthfulQA.597.622.661.673.773.663.765.772.839 SimpleQA.668.645.725.737.772.681.868.873.871

**Table 1.** AUROC for hallucination detection on open-form QA datasets across three representative LLMs. N denotes the sampling budget, representing the average number of response samples generated per query for uncertainty estimation. The best results are in bold and the second best is marked with underline.

## 5 Experimental Setup

Datasets and models We evaluate on four free-form QA datasets: CoQA (Reddy, Chen, and Manning 2019), TriviaQA (Joshi et al. 2017), TruthfulQA(Lin, Hilton, and Evans 2022), and SimpleQA (Wei et al. 2024), covering both openbook and closed-book scenarios. All experiments use zeroshot settings. We test three LLMs: Llama-2-7B (Touvron et al. 2023), Llama-3.1-8B (Dubey et al. 2024), and Mistral- Small-24B (Rastogi et al. 2025), ensuring generalization across different architectures and scales.

## Evaluation

We measure hallucination detection performance using AUROC (Bradley 1997), treating estimator outputs as binary classification scores. Following (Li et al. 2024), we use GPT-4.1 to judge response correctness with a Pass-All@3 method: sampling three responses per question and marking as hallucination if any response contradicts ground truth. For efficiency comparison, we evaluate AUROC at sampling budgets N=1 to 10. As our method uses adaptive sampling, we calibrate variance thresholds to match baseline sample counts.

Baselines We compare against four methods: P(True) (Kadavath et al. 2022) uses LLM self-assessment; SAR (Duan et al. 2024) aggregates token-level prediction entropy; SE (Farquhar et al. 2024) clusters semantic equivalents and computes entropy; SESDLG (Aichberger et al. 2025) enhances SE with targeted perturbations for diverse outputs.

Implementation. We conduct our experiments on a single A800 80GB GPU. Semantic clustering uses DeBERTa-v3large (He, Gao, and Chen 2023) for NLI-based equivalence detection. All generation uses temperature 1.0. N0 is set to 1 to reduce the initialization overhead, and top-k is set to 3. Adaptive sampling variance thresholds are calibrated to achieve average sample counts comparable to baselines.

## Results

and Analyses 6.1 Main Results

Since the computational overhead beyond LLM sampling costs is negligible for all methods (detailed analysis in Appendix C), we set equivalent sampling budgets across different approaches to ensure fair comparison. Table 1 presents the performance comparison across multiple models and datasets. First, our method achieves the highest AUROC in 23 out of 24 settings, with up to 16.9% improvement over the strongest baseline SESDLG (TriviaQA, Mistral-Small-24B, N=2). Second, the advantage is most pronounced in lowsample regimes: 12.6% average improvement at N=2 versus 6.3% at N=5, confirming that our adaptive sampling efficiently explores semantic space under computational constraints. Third, consistent improvements across different model architectures and QA domains demonstrate that our method captures fundamental semantic uncertainty properties rather than dataset-specific patterns, ensuring robust practical deployment.

## 6.2 Ablation Studies

We conduct ablation studies on TriviaQA using Llama-3.1- 8B to analyze each component’s contribution (Table 2).

Prior Estimation Replacing adaptive prior with fixed K = Kobs + 1 causes 4.3% (N=2) and 3.5% (N=5) performance drops, confirming that weighted perplexity effectively captures prompt-specific semantic diversity.

Adaptive Sampling Fixed sampling without Bayesian framework degrades performance by 9.6% (N=2) and 4.7% (N=5). Adding Bayesian framework to fixed sampling partially recovers performance but still underperforms by 5.7% and 2.8%. This shows: (1) Bayesian uncertainty quantification benefits all sampling strategies, and (2) variance-based

33122

<!-- Page 7 -->

## Method

N=2 N=5

Full Model.855.913

Prior Estimation w/o adaptive prior (K = Kobs + 1).812.878

Adaptive Sampling

Fixed sampling w/o Bayesian.759.866 Fixed sampling w/ Bayesian.798.885

Exploration Strategy w/o guided exploration.823.892

**Table 2.** Ablation study on TriviaQA using Llama-3.1-8B, showing AUROC performance when removing key components of our method.

## Model

CoQA TriviaQA TruthfulQA SimpleQA

Llama-2-7B 27.4% 37.5% 58.8% 98.5% Llama-3.1-8B 15.9% 34.7% 52.2% 76.2% Mistral-Small-24B 13.7% 21.2% 46.9% 71.5%

**Table 3.** Hallucination rates across different models and QA datasets using the Pass-All@3 evaluation method.

adaptive sampling is crucial for efficiency, especially in lowsample regimes.

Exploration Strategy Removing guided exploration decreases performance by 3.2% (N=2) and 2.1% (N=5), with larger impact at smaller budgets, confirming that importance sampling explores the semantic space and accelerates semantic discovery under constrained resources.

## 6.3 Further Analyses

Bayesian Framework as a Superior Estimator Our method maintains advantages even at higher sampling budgets (Figure 2) due to hierarchical uncertainty modeling: semantic space cardinality via p(K|D) and probability distributions via truncated Dirichlet posteriors. Unlike traditional methods assuming fixed semantic categories, we account for unobserved meanings through posterior inference. Generation probability constraints (Equation 6) further tighten the feasible space, improving accuracy even when extensive sampling would reveal most variations.

Adaptive Resource Allocation Figure 3 shows our adaptive strategy allocating resources by query complexity. Simple datasets (CoQA) exhibit high variance—many queries need only 1-2 samples due to rapid convergence. Complex datasets (SimpleQA) concentrate near the budget limit, indicating persistent uncertainty. This aligns with intuition: high-probability, consistent responses trigger early termination through decreased posterior variance, ensuring efficiency without sacrificing accuracy for real-world queries.

0 2 4 6 8 10 N

0.50

0.55

0.60

0.65

0.70

0.75

0.80

0.85

AUROC

OURS SESDLG SE SAR

(a) CoQA

0 2 4 6 8 10 N

0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95

AUROC

OURS SESDLG SE SAR

(b) TriviaQA

0 2 4 6 8 10 N

0.50

0.55

0.60

0.65

0.70

0.75

0.80

0.85

0.90

AUROC

OURS SESDLG SE SAR

(c) TruthfulQA

0 2 4 6 8 10 N

0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95

AUROC

OURS SESDLG SE SAR

(d) SimpleQA

**Figure 2.** AUROC performance comparison of hallucination detection methods on Llama-3.1-8B across varying sampling budgets N.

CoQA TriviaQA TruthfulQA SimpleQA 0

2

4

6

8

10

12

Actual Sampling Count N

Dataset complexity

Target avg. N=5

**Figure 3.** Distribution of actual sampling counts under a fixed average budget of N=5 across four QA datasets using Llama-3.1-8B.

Conclusions

In this paper, we propose an adaptive Bayesian estimation framework for semantic entropy that addresses the computational inefficiency of existing hallucination detection methods. Our hierarchical approach models semantic distributions through a Dirichlet prior, while guided exploration with importance sampling discovers diverse interpretations. Variance-based adaptive sampling dynamically allocates resources according to query complexity. Experiments demonstrate consistent superiority across multiple models and datasets, with significantly fewer samples required, particularly in low-budget scenarios. The framework’s efficient resource allocation makes it practical for real-world deployment. Future directions include extensions to multimodal settings and broader uncertainty quantification tasks.

33123

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Natural Science Foundation of China under Grant 62306331 and CAAI Youth Talent Lifting Project under Grant CAAI2023- 2025QNRC001.

## References

Aichberger, L.; Schweighofer, K.; Ielanskyi, M.; and Hochreiter, S. 2025. Improving Uncertainty Estimation through Semantically Diverse Language Generation. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net. Bakman, Y. F.; Yaldiz, D. N.; Buyukates, B.; Tao, C.; Dimitriadis, D.; and Avestimehr, S. 2024. MARS: Meaning- Aware Response Scoring for Uncertainty Estimation in Generative LLMs. In Ku, L.; Martins, A.; and Srikumar, V., eds., Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, 7752–7767. Association for Computational Linguistics. Bradley, A. P. 1997. The use of the area under the ROC curve in the evaluation of machine learning algorithms. Pattern Recognit., 30(7): 1145–1159. Chen, C.; Liu, K.; Chen, Z.; Gu, Y.; Wu, Y.; Tao, M.; Fu, Z.; and Ye, J. 2024. INSIDE: LLMs’ Internal States Retain the Power of Hallucination Detection. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net. Chen, L.; Deng, Y.; Bian, Y.; Qin, Z.; Wu, B.; Chua, T.; and Wong, K. 2023. Beyond Factuality: A Comprehensive Evaluation of Large Language Models as Knowledge Generators. In Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, 6325–6341. Association for Computational Linguistics. Choi, S.; Fang, T.; Wang, Z.; and Song, Y. 2023. KCTS: Knowledge-Constrained Tree Search Decoding with Token- Level Hallucination Detection. In Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, 14035–14053. Association for Computational Linguistics. Dhuliawala, S.; Komeili, M.; Xu, J.; Raileanu, R.; Li, X.; Celikyilmaz, A.; and Weston, J. 2024. Chain-of-Verification Reduces Hallucination in Large Language Models. In Ku, L.; Martins, A.; and Srikumar, V., eds., Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, 3563– 3578. Association for Computational Linguistics. Duan, J.; Cheng, H.; Wang, S.; Zavalny, A.; Wang, C.; Xu, R.; Kailkhura, B.; and Xu, K. 2024. Shifting Attention to Relevance: Towards the Predictive Uncertainty Quantification of Free-Form Large Language Models. In Ku, L.; Martins, A.; and Srikumar, V., eds., Proceedings of the 62nd Annual Meeting of the Association for Computational Linguis- tics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, 5050–5063. Association for Computational Linguistics. Dubey, A.; Jauhri, A.; Pandey, A.; Kadian, A.; Al-Dahle, A.; Letman, A.; Mathur, A.; Schelten, A.; Yang, A.; Fan, A.; Goyal, A.; Hartshorn, A.; et al. 2024. The Llama 3 Herd of Models. CoRR, abs/2407.21783. Farquhar, S.; Kossen, J.; Kuhn, L.; and Gal, Y. 2024. Detecting hallucinations in large language models using semantic entropy. Nat., 630(8017): 625–630. He, P.; Gao, J.; and Chen, W. 2023. DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. Open- Review.net. Huang, L.; Yu, W.; Ma, W.; Zhong, W.; Feng, Z.; Wang, H.; Chen, Q.; Peng, W.; Feng, X.; Qin, B.; and Liu, T. 2025. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. ACM Trans. Inf. Syst., 43(2): 42:1–42:55. Joshi, M.; Choi, E.; Weld, D. S.; and Zettlemoyer, L. 2017. TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension. In Barzilay, R.; and Kan, M., eds., Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics, ACL 2017, Vancouver, Canada, July 30 - August 4, Volume 1: Long Papers, 1601–1611. Association for Computational Linguistics. Kadavath, S.; Conerly, T.; Askell, A.; Henighan, T.; Drain, D.; Perez, E.; Schiefer, N.; Hatfield-Dodds, Z.; DasSarma, N.; Tran-Johnson, E.; Johnston, S.; Showk, S. E.; Jones, A.; Elhage, N.; Hume, T.; Chen, A.; Bai, Y.; Bowman, S.; Fort, S.; Ganguli, D.; Hernandez, D.; Jacobson, J.; Kernion, J.; Kravec, S.; Lovitt, L.; Ndousse, K.; Olsson, C.; Ringer, S.; Amodei, D.; Brown, T.; Clark, J.; Joseph, N.; Mann, B.; McCandlish, S.; Olah, C.; and Kaplan, J. 2022. Language Models (Mostly) Know What They Know. CoRR, abs/2207.05221. Kossen, J.; Han, J.; Razzak, M.; Schut, L.; Malik, S. A.; and Gal, Y. 2024. Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs. CoRR, abs/2406.15927. Kuhn, L.; Gal, Y.; and Farquhar, S. 2023. Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. OpenReview.net. Lai, H.; and Nissim, M. 2024. A Survey on Automatic Generation of Figurative Language: From Rule-based Systems to Large Language Models. ACM Comput. Surv., 56(10): 244. Lee, J.; Stevens, N.; Han, S. C.; and Song, M. 2024. A Survey of Large Language Models in Finance (FinLLMs). CoRR, abs/2402.02315. Li, D.; Jiang, B.; Huang, L.; Beigi, A.; Zhao, C.; Tan, Z.; Bhattacharjee, A.; Jiang, Y.; Chen, C.; Wu, T.; Shu, K.; Cheng, L.; and Liu, H. 2024. From Generation to Judgment:

33124

<!-- Page 9 -->

Opportunities and Challenges of LLM-as-a-judge. CoRR, abs/2411.16594. Lin, S.; Hilton, J.; and Evans, O. 2022. TruthfulQA: Measuring How Models Mimic Human Falsehoods. In Muresan, S.; Nakov, P.; and Villavicencio, A., eds., Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022, 3214–3252. Association for Computational Linguistics. Lin, Z.; Liu, J. Z.; and Shang, J. 2022. Towards Collaborative Neural-Symbolic Graph Semantic Parsing via Uncertainty. In Muresan, S.; Nakov, P.; and Villavicencio, A., eds., Findings of the Association for Computational Linguistics: ACL 2022, Dublin, Ireland, May 22-27, 2022, 4160–4173. Association for Computational Linguistics. Luo, Z.; Yang, Z.; Xu, Z.; Yang, W.; and Du, X. 2025. LLM4SR: A Survey on Large Language Models for Scientific Research. CoRR, abs/2501.04306. Min, S.; Krishna, K.; Lyu, X.; Lewis, M.; Yih, W.; Koh, P. W.; Iyyer, M.; Zettlemoyer, L.; and Hajishirzi, H. 2023. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, 12076–12100. Association for Computational Linguistics. Nikitin, A.; Kossen, J.; Gal, Y.; and Marttinen, P. 2024. Kernel Language Entropy: Fine-grained Uncertainty Quantification for LLMs from Semantic Similarities. In Globersons, A.; Mackey, L.; Belgrave, D.; Fan, A.; Paquet, U.; Tomczak, J. M.; and Zhang, C., eds., Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024. Rastogi, A.; Jiang, A. Q.; Lo, A.; Berrada, G.; Lample, G.; Rute, J.; Barmentlo, J.; Yadav, K.; Khandelwal, K.; Chandu, K. R.; Blier, L.; Saulnier, L.; et al. 2025. Magistral. CoRR, abs/2506.10910. Reddy, S.; Chen, D.; and Manning, C. D. 2019. CoQA: A Conversational Question Answering Challenge. Trans. Assoc. Comput. Linguistics, 7: 249–266. Swaminathan, A.; and Joachims, T. 2015. The Self- Normalized Estimator for Counterfactual Learning. In Cortes, C.; Lawrence, N. D.; Lee, D. D.; Sugiyama, M.; and Garnett, R., eds., Advances in Neural Information Processing Systems 28: Annual Conference on Neural Information Processing Systems 2015, December 7-12, 2015, Montreal, Quebec, Canada, 3231–3239. Touvron, H.; Martin, L.; Stone, K.; Albert, P.; Almahairi, A.; Babaei, Y.; Bashlykov, N.; Batra, S.; Bhargava, P.; Bhosale, S.; Bikel, D.; Blecher, L.; et al. 2023. Llama 2: Open Foundation and Fine-Tuned Chat Models. CoRR, abs/2307.09288. Wang, C.; Liu, X.; Yue, Y.; Tang, X.; Zhang, T.; Jiayang, C.; Yao, Y.; Gao, W.; Hu, X.; Qi, Z.; Wang, Y.; Yang, L.; Wang, J.; Xie, X.; Zhang, Z.; and Zhang, Y. 2023a. Sur- vey on Factuality in Large Language Models: Knowledge, Retrieval and Domain-Specificity. CoRR, abs/2310.07521. Wang, S.; Xu, T.; Li, H.; Zhang, C.; Liang, J.; Tang, J.; Yu, P. S.; and Wen, Q. 2024. Large Language Models for Education: A Survey and Outlook. CoRR, abs/2403.18105. Wang, X.; Yan, Y.; Huang, L.; Zheng, X.; and Huang, X. 2023b. Hallucination Detection for Generative Large Language Models by Bayesian Sequential Estimation. In Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, 15361–15371. Association for Computational Linguistics. Wei, J.; Karina, N.; Chung, H. W.; Jiao, Y. J.; Papay, S.; Glaese, A.; Schulman, J.; and Fedus, W. 2024. Measuring short-form factuality in large language models. CoRR, abs/2411.04368. Zhang, T.; Qiu, L.; Guo, Q.; Deng, C.; Zhang, Y.; Zhang, Z.; Zhou, C.; Wang, X.; and Fu, L. 2023. Enhancing Uncertainty-Based Hallucination Detection with Stronger Focus. In Bouamor, H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, 915–932. Association for Computational Linguistics. Zhao, W. X.; Zhou, K.; Li, J.; Tang, T.; Wang, X.; Hou, Y.; Min, Y.; Zhang, B.; Zhang, J.; Dong, Z.; Du, Y.; Yang, C.; Chen, Y.; Chen, Z.; Jiang, J.; Ren, R.; Li, Y.; Tang, X.; Liu, Z.; Liu, P.; Nie, J.-Y.; and Wen, J.-R. 2025. A Survey of Large Language Models. arXiv:2303.18223.

33125
