---
title: "Multi-Modal Style Transfer-based Prompt Tuning for Efficient Federated Domain Generalization"
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/39177
paper_pdf_url: https://ojs.aaai.org/index.php/AAAI/article/view/39177/43138
venue: AAAI
year: 2026
retrieved_date: 2026-07-22
content_scope: whole paper PDF text with extracted SVG figure assets
---
# Multi-Modal Style Transfer-based Prompt Tuning for Efficient Federated Domain Generalization

<!-- Page 1 -->

Multi-Modal Style Transfer-based Prompt Tuning for Efficient Federated

Domain Generalization

Yuliang Chen1,2*, Xi Lin1,2*, Jun Wu1,2, Xiangrui Cai3†, Qiaolun Zhang4,

Xichun Fan5, Jiapeng Xu1,2, Xiu Su6†

1School of Computer Science, Shanghai Jiao Tong University 2Shanghai Key Laboratory of Integrated Administration Technologies for Information Security 3College of Computer Science, Nankai University 4Department of Electronics, Information and Bioengineering, Polytechnic Institute of Milan 5New York University Shanghai 6Big Data Institute, Central South University {chenyuliang, linxi234, junwuhn, xjp20021018}@sjtu.edu.cn, caixr@nankai.edu.cn, qiaolun.zhang@mail.polimi.it, xf731@nyu.edu, xiusu1994@csu.edu.cn

## Abstract

Federated Domain Generalization (FDG) aims to collaboratively train a global model across distributed clients that can generalize well on unseen domains. However, existing FDG methods typically struggle with cross-client data heterogeneity and incur significant communication and computation overhead. To address these challenges, this paper presents a new FDG framework, dubbed FaST-PT, which facilitates local feature augmentation and efficient unseen domain adaptation in a distributed manner. First, we propose a lightweight Multi-Modal Style Transfer (MST) method to transform image embedding under text supervision, which could expand the training data distribution and mitigate domain shift. We then design a dual-prompt module that decomposes the prompt into global and domain prompts. Specifically, global prompts capture general knowledge from augmented embedding across clients, while domain prompts capture domain-specific knowledge from local data. Besides, Domain-aware Prompt Generation (DPG) is introduced to adaptively generate suitable prompts for each sample, which facilitates unseen domain adaptation through knowledge fusion. Extensive experiments on four cross-domain benchmark datasets, e.g., PACS and DomainNet, demonstrate the superior performance of FaST-PT over SOTA FDG methods such as FedDG-GA and DiPrompt. Ablation studies further validate the effectiveness and efficiency of FaST-PT.

## Introduction

Federated Learning (FL) (McMahan et al. 2017) is a widely adopted distributed machine learning paradigm, which facilitates collaborative model training while protecting privacy. Instead of relying on a single centralized server, FL distributes the training process across multiple clients (e.g., mobile devices or institutions) to collaboratively train a global model without sharing their private data. It is specifically

*These authors contributed equally. †Corresponding authors Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

well-suited for real-world applications where sensitive data is distributed across multiple sources (Guan et al. 2024).

Although FL has shown promising performance in various tasks, existing studies predominantly focus on enhancing model performance for the participating clients. However, they often overlook the generalization capability to unseen domains beyond the participating clients. Data encountered in these unseen environments can exhibit substantial distributional differences from training clients, due to variations in data sources, collection methods, or domainspecific characteristics. Effectively adapting FL to such domain shifts (Muandet, Balduzzi, and Sch¨olkopf 2013; Li et al. 2018) remains a technically challenging problem.

Federated Domain Generalization is defined as training a global model on multiple distributed source domains, aiming to achieve robust generalization to completely unseen target domains. Early attempts have been made to address the FDG problem. For example, ELCFS (Liu et al. 2021) allows clients to share the amplitude spectrum in frequency space for federated medical image segmentation. Similarly, CCST (Chen et al. 2023) extracts and exchanges style information to perform style transfer. Besides, FPL (Huang et al. 2023) facilitates the exchange of prototypes among clients. A common limitation of these methods is their reliance on sharing domain-related information among clients, which compromises the data privacy and communication constraints inherent in FL. Additionally, extracting domainspecific information often requires auxiliary modules, leading to increased computational overhead.

To address the above challenges, we propose a new framework dubbed Federated Multi-Modal Style Transfer with Prompt Tuning (FaST-PT). In FaST-PT, we introduce CLIP into FL and utilize its text-image alignment and generalization ability for handling FDG problems. On the one hand, we leverage CLIP’s powerful image-text alignment capabilities and propose Multi-Modal Style Transfer (MST), which enables client-side external domain style transfer to expand the training data distribution. Specifically, MST introduces a

The Fortieth AAAI Conference on Artificial Intelligence (AAAI-26)

20427

<!-- Page 2 -->

transform network that transforms image embeddings using the text representation of the external domain, facilitating the style transfer while retaining the class-specific information of the original image. On the other hand, we employ the prompt tuning paradigm of CLIP to facilitate efficient unseen domain adaptation. We first design a dual-prompt module that incorporates both global and domain prompts. In detail, global prompts are trained on augmented embeddings and aggregated across clients to capture general knowledge, while local prompts are trained solely on local data to preserve domain-specific knowledge. Additionally, we propose a domain-aware prompt generation mechanism to further incorporate domain knowledge based on domain similarity, thereby enhancing the adaptability of prompts to unseen domains. Our contribution can be summarized as follows:

• We present FaST-PT, a new FL framework that tackles the FDG problem through both client-side distribution alignment and efficient unseen domain adaptation by leveraging the text-image alignment and generalization capabilities of the pre-trained CLIP model. • We propose a multi-modal style transfer method that allows clients to transform the image embedding to the style of the external domains while retaining the class information under the supervision of text description to mitigate the distribution discrepancy among clients. • We design a dual-prompt module that leverages prompt partition to simplify feature disentanglement in traditional domain generalization, and employs domainaware prompt generation to integrate domain knowledge for efficient unseen domain adaptation. • Extensive experiments are conducted with FaST-PT on four benchmark datasets, consistently demonstrating its superior performance over baseline methods. Comprehensive ablation studies further validate the effectiveness and efficiency of FaST-PT.

## Related Work

Federated Learning

Federated learning (FL) distributes the training progress across multiple devices or compute nodes instead of a single central server to facilitate global training of the model while protecting data privacy. The most typical FL framework is FedAvg (McMahan et al. 2017; Koneˇcn`y et al. 2016), which decomposes the distributed learning process from the perspectives of local training and global averaging. However, traditional FL performs poorly under domain shift. Existing methods mainly focus on regularizing the local training on the client side to attain a well-performed global model. Fed- Prox (Li et al. 2020) added an extra term in the loss function to control the L2 distance of model weights. FedBN (Li et al. 2021) retains the parameters of the batch normalization layers locally and excludes them from the aggregation process.

Federated Domain Generalization

Federated domain generalization is a variant of DG tailored to the FL setting, aiming to mitigate domain shifts across clients and improve the model’s generalization to unseen domains (Liu et al. 2021; Nguyen, Torr, and Lim 2022; Wu and Gong 2021; Chen et al. 2023; Zhang et al. 2021a; Huang et al. 2023; Le et al. 2024). ELCFS (Liu et al. 2021) is the first to solve the FDG problem, which exchanges the amplitude spectrum in the frequency domain and employs episodic learning to further enhance generalization performance. CCST (Chen et al. 2023) allows clients to share their style information and achieve local style transfer, leading to more uniform distributions of source clients. Apart from domain information sharing methods, the remaining approaches focus on extracting domain-invariant features. For example, FedSR (Nguyen, Torr, and Lim 2022) leverages L2-norm and conditional mutual information regularizations to learn simple yet generalizable data representations. COPA (Wu and Gong 2021) simultaneously incorporates a domain-invariant representation extractor along with an ensemble of domain-specific classifiers.

Prompt Tuning Prompt tuning (Lester, Al-Rfou, and Constant 2021) is a parameter-efficient fine-tuning technique that introduces a small set of learnable prompt tokens as additional inputs, while keeping the parameters of foundation models frozen. As a pioneering work, CoOp (Zhou et al. 2022b) adapts CLIP (Radford et al. 2021) to downstream image recognition tasks by converting the input context tokens in the text encoder into learnable prompts. CoCoOp (Zhou et al. 2022a) extends CoOp by generating input-dependent prompts through a lightweight network. MaPLe (Khattak et al. 2023) further enhances the alignment between textual and visual representations in CLIP by introducing visual prompts alongside textual ones. In recent years, prompt tuning has been introduced into federated learning due to its inherent suitability for efficient communication. For instance, PromptFL (Guo et al. 2023) and FedPrompt (Zhao et al. 2023) independently learn text prompts on each local client and aggregate the optimized prompts on the server.

## Methods

We assume K clients, where each client i possesses a dataset from domain Di. The primary objective is to jointly train a global prompt module that generalizes effectively to the unseen target domain Du. A key assumption in our framework is that each client has access to simple text descriptions of external training domains ti (e.g., “a clipart of a”), which are considered non-sensitive and do not compromise client privacy. The framework of FaST-PT is shown in Figure 1.

Multi-Modal Style Transfer Existing FDG approaches improve the generalization capability of local models by incorporating knowledge from diverse domains, which necessitates sharing part of the domain knowledge among clients. While sharing such sensitive information between clients may bring the risk of data leakage, we propose a lightweight and secure local style transfer scheme, MST, which leverages CLIP’s extensive domain knowledge and strong text-image alignment capabili-

20428

<!-- Page 3 -->

𝑡! = “𝑡𝑒𝑎𝑝𝑜𝑡”

𝐼

𝑇

CLIP 𝒅𝒐𝒎𝒂𝒊𝒏𝒔 𝑡! = “𝑎 𝑐𝑙𝑖𝑝𝑎𝑟𝑡 𝑜𝑓 𝑎 𝑑𝑎𝑖𝑙𝑦 𝑠𝑡𝑎𝑝𝑙𝑒” 𝑡" = “𝑎 𝑠𝑘𝑒𝑡𝑐ℎ 𝑜𝑓 𝑎 𝑑𝑎𝑖𝑙𝑦 𝑠𝑡𝑎𝑝𝑙𝑒” 𝒍𝒂𝒃𝒆𝒍𝒔 𝑡# = [“𝑡𝑒𝑎𝑝𝑜𝑡”, ”ℎ𝑒𝑎𝑑𝑝ℎ𝑜𝑛𝑒”, ⋯]

𝒬!→# 𝑥

𝑇(𝑡!)

𝑇(𝑡")

𝑇(“𝑡𝑒𝑎𝑝𝑜𝑡”)

𝑇(”ℎ𝑒𝑎𝑑𝑝ℎ𝑜𝑛𝑒”)

Language supervision Joint embedding space

ℒ!

ℒ"

Loss function

ℒ

Embedding of internal domain 𝒟"

Embedding of external domain 𝒟#

Dataset 𝒮" Domain 𝒟"

Augmented data

(a) Stage I: Multi-Modal Style Transfer

(b) Stage II: Federated Prompt Tuning 𝑣$

%

𝑇 𝑣&

% 𝑣'

%

Client 𝟏 𝑡!

class class 𝑣$

(𝑣&

(𝑣'

(class

ℐ" = {ℐ"→#}

⋯

⋯

𝒟#

𝒟)

𝒟$ ℐ!→#

Global Prompt

Domain

Prompt

Client 𝑲

Client 𝒊

⋯

⋯

Handcrafted

Prompt 𝑇(𝑡")

𝑇(𝑃%)

𝑇(𝑃&)

𝐼(𝑥)

ℒ%

!

ℒ(

!

Domain classifier 𝑓(1, 𝜑)

ℒ*

!

ℐ!

𝐼(𝒮!)

𝜑!

𝜑)

𝜑$ 𝑣'

% 𝑣&

% 𝑣$

% 𝑃$

% 𝑣'

% 𝑣&

% 𝑣$

% 𝑃!

% 𝑣'

% 𝑣&

% 𝑣$

% 𝑃)

%

Server 𝜑 𝑣'

% 𝑣&

% 𝑣$

% 𝑃%

Inference with DPG

Global aggregation

Unseen domain

𝐼 𝑔' ⋯ 𝑔(𝑔) ⨂𝑃(

𝑃% 𝑃+ class

𝑇

Contrastive similarity

**Figure 1.** Framework of our proposed FaST-PT. The left side illustrates the local training process, while the right side depicts the communication between client and server. The client-side training is divided into two phases: (a) MST and (b) FPT. (a) In the MST phase, the client employs a frozen CLIP model along with text descriptions from various domains to train a transform network, enabling style transfer at the embedding level. (b) In the FPT phase, the client trains global prompts, domain prompts, and domain classifiers using the augmented data. The inference process is also depicted on the server side.

ties to facilitate latent feature augmentation at the embedding level. It allows client k with domain Dk to generate image embeddings for external domains D{1,2...K}\k.

MST mainly learns a transform network Qi→j that transforms the image embedding of the input image from Di to Dj, with the goal formulated as the following two aspects:

• The alignment between Di and Dj • The preservation of class-consistent features

Let x denote the input image and I(x) denote the image embedding of x. Besides, let tk denote the domain-related description of domain Dk and ty denote the class label. We compose these two parts to obtain the text input as t = [tk, ty], which is further encoded to get the text embedding T(t). For instance, if ti = “a clipart of a {}”, tj = “a sketch of a {}”, and ty could be “tiger”, then the composed text t =“a clipart of a tiger”.

To achieve the embedding transform from Di to Dj while preserving class-consistent features, we design two loss functions to train Qi→j for each domain Dj distinct from the local domain Di: alignment loss and consistency loss.

Alignment Loss The alignment loss LA(Qi→j) aims to ensure that the embeddings of augmented images more faithfully reflect the distinctive properties of their respective domains. LA(Qi→j) is supervised by textual descriptions associated with different source domains. While CLIP effectively captures relationships between text and image embeddings, directly obtaining their precise correspondence remains challenging. To address this, we align the change direction in the image and text embedding spaces as the optimization target. Specifically, this change direction is defined as the normalized difference between embeddings from Di and Dj. The alignment loss is thus formulated as:

LA(Qi→j) =

X

(x,y)∈Si

1 − Qi→j(I(x)) −I(x) ∥Qi→j(I(x)) −I(x)∥

· T(tj, ty) −T(ti, ty) ∥T(tj, ty) −T(ti, ty)∥

.

(1)

Consistency Loss The consistency loss LC is designed to preserve the class knowledge in transformed embeddings. The intuition behind designing LC is that using only the alignment loss may ensure style transfer of the embedding, but it can also erase some class information. We leverage CLIP’s zero-shot inference capabilities to assess the class information contained in the enhanced image embeddings. Specifically, we perform classification by comparing these enhanced embeddings with the text embeddings of class names. To this end, we adopt CLIP’s standard contrastive loss, formulated as follows:

LC(Qi→j) = E(x,y)∈Siℓce([Qi→j(I(x)) · T(ty)], y), (2)

where [I · T] denote the Softmax-based contrastive similarity computation and Top-1 prediction process.

The general objective LMST(Qi→j) of training the transform network Qi→j is the composition of the above two loss functions. To balance the effectiveness of alignment and consistency, we additionally introduce a hyperparameter λ to achieve the linear composition:

LMST(Qi→j) = λLA(Qi→j) + (1 −λ)LC(Qi→j). (3)

Client i with domain Di locally learn (K −1) transform networks for the other (K−1) clients and generate the corresponding augmentation embeddings Ii→j = Qi→j(x), x ∈ Si. Thus, each client maintains a set of augmentation embeddings as Ii = {Ii→j}, j ∈{1, 2... K}\i.

20429

![Figure extracted from page 3](2026-AAAI-multi-modal-style-transfer-based-prompt-tuning-for-efficient-federated-domain-ge/page-003-figure-01.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-multi-modal-style-transfer-based-prompt-tuning-for-efficient-federated-domain-ge/page-003-figure-08.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-multi-modal-style-transfer-based-prompt-tuning-for-efficient-federated-domain-ge/page-003-figure-09.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

![Figure extracted from page 3](2026-AAAI-multi-modal-style-transfer-based-prompt-tuning-for-efficient-federated-domain-ge/page-003-figure-12.svg)

AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. Use the surrounding page text and caption for interpretation.

<!-- Page 4 -->

Federated Prompt Tuning Yet, conventional DG methods often involve complex feature extraction techniques. How to leverage augmented embeddings to achieve domain generalization with minimal resource consumption remains an open challenge. Building on the powerful feature extraction capabilities of CLIP, we introduce prompt tuning of CLIP for efficient domain generalization. Motivated by the idea of feature disentanglement (Bui et al. 2021; Zhang et al. 2022) in traditional DG, we propose a dual-prompt module that divides the prompts into global and domain prompts.

Global Prompt P G is designed to capture the general knowledge of the downstream task, which should be shared across clients. P G is a set of L learnable vectors P G = {vG

1, vG 2,..., vG L }, with the same dimension as text embedding d. We denote the class label as ty. For the j-th class, we define the input of the text encoder with global prompt as t = [P G, tj y]. We denote the feature map of image x as I(x) and the text feature map as T([P G, tj y]). Thus, the prediction probability of the j-th class computed with contrastive similarity can be formulated as:

pG(y = j|x) = exp(H(T([P G, tj y]), I(x))/τ) PC i=1 exp(H(T([P G, tiy]), I(x))/τ)

, (4)

where H is the cosine similarity, C is the number of class and τ is the temperature of Softmax function. We optimize the global prompts by minimizing the cross-entropy loss computed over both the augmented embeddings and the original dataset. Specifically, the training loss on client i is defined as follows:

Li

G = E(x,y)∈Si∪Ii[ℓce(y, pG(y|x))]. (5)

Domain Prompt P D i is designed to capture the domainspecific knowledge of client i. Similarly, P D i is a set of vectors P D i = {vD

1, vD 2,..., vD L } with length L and dimension d. We concatenate P G with the domain prompt to form a new composite prompt P C = [P G, P D i ]. Specifically, the predicted probability is updated accordingly after introducing the domain prompt, by replacing P G with P C. The core idea of the domain-specific prompt is to enhance the performance of P D i on local data Si. We similarly optimize it using the cross-entropy loss Li

Cla = E(x,y)∈Si[ℓce(y, pC(y|x))]. Besides, the training of P D i should also enforce orthogonality with P G to guarantee the uniqueness of the extracted knowledge. To this end, we additionally introduce a contrastive loss term as follows:

Li

D = Li

Cla + Li

Con = E(x,y)∈Si[ℓce(y, pC(y|x))]

−log exp(sim(P D i, ti)) exp(sim(P D i, ti)) + exp(sim(P D i, P G)),

(6)

where ti is the handcrafted prompt for Domain Di and pC(y|x) is the probability predicted with prompt P C.

Notably, clients share global prompts for aggregation during training, while domain-specific prompts are retained locally and only shared after training. The final domain prompt list is formed as P D = [P D

1, P D 2,..., P D K ].

## Algorithm

1: FaST-PT

1: Input: Datasets Si, client number K, training round R, epoch number EG and EL 2: Output: Global Prompt P G, Domain prompt list P D, domain classifier f(·, φ) 3: Stage 1: Multi-Modal Style Transfer 4: for client i = 1, 2,..., K do 5: for Domain Dj ∈{D1, D2,..., DK}\Di do 6: Train Qi→j with LMST(Qi→j) (Eq. 3) 7: end for 8: end for 9: Clients locally augments image embedding Ii→j

10: Stage 2: Federated Prompt Tuning 11: for round r = 1, 2,..., R do 12: for client i = 1, 2,..., K do 13: for epoch e = 1, 2,..., EG do 14: Training P G i and φi with Li

G and Li

F 15: end for 16: end for 17: Upload P G i and φi 18: Server aggregates P G and φ and broadcasts 19: for client i = 1, 2,..., K do 20: for epoch e = 1, 2,..., ED do 21: Training P D i with Li

D 22: end for 23: end for 24: end for 25: Server collects P D and broadcasts

Domain-aware Prompt Generation Considering the latent similarity between training and unseen domains, we further design a domain-aware prompt generation scheme to integrate knowledge from diverse domains to enhance generalization performance, which enables better adaptation of the target domain Du. We utilize a domain classifier f(·, φ) to facilitate the domain similarity analysis. f(·, φ) takes image feature as the input and outputs the one-hot format result with K dimension as: G = [g1, g2... gK].

We weight ⊗the domain prompt list P D with the pseudodomain label G element-wise to generate the dynamic prompt P N for arbitrary image x as follows:

P N = f(I(x), φ) ⊗P D. (7)

P N integrates knowledge from multiple source domains to generate knowledge that approximates the target domain. During the inference stage, P N is concatenated with P G and fed into the text encoder. For the optimization of f(·, φ), we leverage the augmented dataset Si ∪Ii for training and denote the domain index as the label. We utilize the crossentropy loss and formulate the objective as follows:

Li

F = E(x,y,j)∈Si∪Ii[ℓce(j, f(x, φi))], (8)

where j is the domain index.

During the training of the prompt module, we adopt a two-stage alternating update strategy. First, clients update the global parameters P G and φ, and upload the gradient

20430

<!-- Page 5 -->

PACS (%) VLCS (%) Methods A C P S Avg C L S V Avg FedAvg 81.27 76.78 92.33 63.54 78.48 92.78 62.39 73.02 74.98 75.79 FedProx 80.22 77.17 96.08 64.28 79.44 93.22 62.80 74.64 74.96 76.41 ELCFS 85.89 74.02 92.14 69.16 80.30 93.28 61.64 73.42 76.06 76.10 FedSR 84.97 85.13 91.37 67.13 82.15 95.55 63.29 71.93 75.43 76.55 FedADG 80.16 81.92 91.28 68.43 80.45 95.96 65.63 70.29 76.70 77.15 FedDG-GA 94.03 83.19 76.85 82.93 84.25 95.14 62.82 74.41 77.49 77.47 PromptFL 93.19 94.72 99.10 83.76 92.70 99.26 66.08 79.38 78.56 80.82 FedAPT 93.78 95.52 99.63 85.31 93.56 99.01 67.91 78.66 81.53 81.78 DiPrompt 95.72 96.39 99.24 88.07 94.86 99.70 68.97 84.72 82.93 84.08 FaST-PT 97.32 99.31 99.93 96.09 98.16 99.17 70.59 86.05 86.26 85.52

**Table 1.** Performance comparison of different methods on the PACS dataset and the VLCS dataset.

updates, which are then aggregated by the server and broadcast back to all clients. Second, clients update the local parameters P D i and upload them after the final round. Since the training of P G and f(·, φ) does not interfere with each other, it is reasonable to train them simultaneously. The complete training process is illustrated in Alg.1.

## Discussion

FaST-PT achieves efficient local feature enhancement and robust domain generalization. Specifically, although FaST- PT leverages MST to mitigate domain shift and adopts prompt tuning for domain generalization, both components are built upon the CLIP model. This unified backbone design obviates the need for deploying additional models on local clients, thereby reducing memory consumption and computational overhead. Moreover, unlike traditional federated learning methods that require sharing full model parameters, FaST-PT only exchanges prompts and their associated lightweight generation modules across clients, substantially lowering communication costs (as further evidenced in our experimental results). Finally, in contrast to approaches that transmit domain-specific features, MST merely requires clients to share text descriptions of their respective domains—information that is inherently less sensitive, thus providing stronger privacy protection.

## Experiments

## Experimental Setup

Datasets We perform extensive experiments on four crossdomain datasets: PACS (Li et al. 2017) has four domains, photo (P), art-painting (A), cartoon (C) and sketch (S). VLCS (Fang, Xu, and Rockmore 2013) is a widely used benchmark for domain generalization, consisting of four domains, VOC2007 (V), LabelMe (L), Caltech101 (C), and SUN09 (S). DomainNet (Peng et al. 2019) is a large-scale dataset across six domains, clipart (C), infograph (I), painting (P), quickdraw (Q), real (R), and sketch (S). Office- Home (Venkateswara et al. 2017) is a medium-scale benchmark dataset containing four domains: Art (A), Clipart (C), Product (P), and Real-World (R). Following (Li et al. 2021; Yang, Wang, and Wang 2023), we select the top 10 classes for our experiment on DomainNet and OfficeHome. We adopt the leave-one-domain-out protocol, treating one domain as the target while using the others as source domains.

Baselines We compare our method with three types of state-of-the-art methods: 1) Traditional federated learning framework including FedAvg (McMahan et al. 2017) and FedProx (Li et al. 2020) that enables clients to collaboratively train a global model from scratch. 2) Conventional FedDG methods that integrate DG with FL to collaboratively train a generalized model that perform well on unseen domains, including ELCFS (Liu et al. 2021), FedSR (Nguyen, Torr, and Lim 2022), FedADG (Zhang et al. 2021b) and FedDG-GA (Zhang et al. 2021a). 3) Prompt tuning-based methods that introduce prompt tuning into FL to enhance the generalization ability of CLIP, including PromptFL (Guo et al. 2023), FedAPT (Su et al. 2024), and DiPrompt (Bai et al. 2024).

Implement Details We conduct our experiment with Python 3.11 on NVIDIA RTX A40 GPU. We use the OpenAI CLIP model with a ViT-L/14 backbone, which encodes both images and text into 768-dimensional feature vectors. For the MST stage, we utilize a 2-layer MLP as the transform network Qi→j with a hidden dimension of 384. we utilize the Adam optimizer with a learning rate of 1e−3 and a weight decay of 0.05. The loss weight λ is set as 0.5. For the prompt training stage, we utilize a fully-connection layer as the domain classifier f(·, φ). We use the SGD optimizer with a learning rate of 0.005 and 0.01 for training of the prompt and domain classifier, respectively. We set the communication round R as 20 and local training epoch EG = EL = 5. We set the batch size as 16 and prompt length as 4. We use the same hyperparameters and backbones across all experiments to ensure a fair comparison.

## Evaluation

We demonstrate the experimental results of FaST-PT and other methods in Table 1 and Table 2, which consists of totally 18 domain generalization tasks on PACS, VLCS, OfficeHome and DomainNet. All experimental results are reported as the average over three runs with different random seeds. Generally, we observe that although conventional FDG methods have demonstrated significantly better generalization performance than traditional FL approaches,

20431

<!-- Page 6 -->

OfficeHome (%) DomainNet (%) Methods A C P R Avg C I P Q R S Avg FedAvg 82.56 79.20 88.28 91.15 85.30 78.04 62.69 80.13 45.78 82.49 84.17 72.22 FedProx 83.19 77.91 90.28 91.60 85.74 79.11 64.77 82.82 51.65 84.65 83.94 74.49 ELCFS 88.72 82.64 89.37 91.75 88.12 83.28 67.18 85.78 58.65 88.31 86.37 78.26 FedSR 88.17 84.47 88.89 90.65 88.04 85.17 66.57 86.01 60.95 87.26 90.10 79.34 FedADG 86.51 87.25 91.52 92.30 89.40 83.95 69.68 84.05 61.51 90.78 86.79 79.46 FedDG-GA 87.86 86.90 92.42 93.25 90.11 86.69 70.93 85.69 60.72 89.82 87.18 80.17 PromptFL 92.35 88.73 95.20 98.80 93.77 89.92 72.75 87.46 60.85 93.54 90.47 82.50 FedAPT 94.28 90.76 97.08 98.95 95.27 91.44 72.04 90.62 63.88 95.27 94.23 84.58 DiPrompt 95.48 91.26 97.90 99.10 95.94 93.89 75.34 93.72 64.16 96.31 97.62 86.84 FaST-PT 98.57 92.72 99.24 99.40 97.48 97.48 78.14 97.17 66.88 97.90 98.46 89.17

**Table 2.** Performance comparison of different methods on the OfficeHome dataset and the DomainNet dataset.

there remains a notable performance gap compared to recent prompt-based FL methods. This substantial improvement in generalization can be largely attributed to the strong cross-modal and generalization capabilities of CLIP. Even when all methods are built upon the same pretrained visual backbone (ViT-L/14), prompt tuning enables more efficient adaptation to the distributional characteristics of each domain. Specifically, FaST-PT achieves state-of-the-art performance with an average accuracy of 98.16% on PACS, 85.52% on VLCS, 97.48% on OfficeHome, and 89.17% on DomainNet, surpassing the SOTA method DiPrompt by up to +3.30% on PACS and +2.33% on DomainNet. Among the total of 18 generalization tasks across all benchmarks, FaST- PT achieves the best performance on 17 tasks, demonstrating remarkable consistency. Compared to existing promptbased FL methods, FaST-PT still demonstrates a substantial performance advantage, highlighting the effectiveness of the proposed MST and DAP strategy, both of which play a critical role in enhancing cross-domain adaptability and mitigating the adverse effects of distributional shifts in FL.

Ablation Study

Effectiveness of Components To investigate the effectiveness of different components in FaST-PT, we evaluated various variants of FaST-PT on the PACS dataset, as shown in Table 3. In variants 1 and 2, we only employ global prompts or domain prompts combined with the DPG mechanism. Compared to variant 4, the performance decreased noticeably, which demonstrates the effectiveness of integrating global and domain knowledge for generalization tasks. In addition, through two comparative analyzes (1 vs. 3 and 4 vs. FaST-PT), we observed that the introduction of the MST strategy can mitigate the domain shift problem in FDG and effectively improve model performance, thus improving the generalization capability of the global model. Variant 5 exhibits a performance decline compared to FaST-PT, which also reflects that the contrastive loss we employed can strengthen the separation between global and domain knowledge, thereby indirectly enhancing adaptation to the target domain. In Variant 6, we conducted experiments by supplementing the textual descriptions of the target domain, allowing clients to generate image features for the target domain to assist the training of the global model.

Image from Internal Domain

NN Image from External Domain

DomainNet

PACS

Image from Internal Domain

NN Image from External Domain

**Figure 2.** Nearest Neighbors on PACS and DomainNet.

Its performance only surpasses FaST-PT by 0.24%.

Visualization of MST We evaluate the style transfer effect of the MST strategy, with the results presented in Figure 2. Since existing methods do not support converting image features back into images, we adopt a Nearest Neighbors (NN) approach to assess the generated augmented features. Specifically, we use all data from the extended domain as the reference set. For each enhanced embedding, we compute its cosine similarity with embeddings in the reference set and select the one with the highest similarity as its NN. In Figure 2, the top row displays the original images used for style transfer, while the bottom row shows the NNs corresponding to their enhanced features. We observe that although there is a clear difference in style between the top and bottom images, they consistently belong to the same semantic category. This observation aligns with the objectives of the two-part loss function employed during training and demonstrates the effectiveness of the MST strategy.

Effect of prompt length We analyze the effect of prompt length and demonstrate the result in Figure 3. Here, we set the lengths of the global and domain prompts to be equal. On PACS and DomainNet datasets, we observed that in most tasks, model performance exhibited a trend of initially increasing and then decreasing as the prompt length grows. Short prompt constrains the performance due to the limited information conveyed in the prompt. Conversely, long

20432

<!-- Page 7 -->

Variant P G P D LCon DPG MST ttarget A C P S Average 1 ✓ 91.21 90.94 94.54 93.61 92.58 2 ✓ ✓ 85.48 83.16 90.79 91.25 87.67 3 ✓ ✓ 92.43 94.14 95.81 95.13 94.38 4 ✓ ✓ ✓ ✓ 96.03 97.44 98.98 95.77 97.06 5 ✓ ✓ ✓ ✓ 97.74 99.09 99.48 95.48 97.95 6 ✓ ✓ ✓ ✓ ✓ ✓ 97.93 99.68 99.85 96.27 98.42 FaST-PT ✓ ✓ ✓ ✓ ✓ 97.32 99.31 99.93 96.09 98.16

**Table 3.** Effect of different components of Fast-PT on PACS.

1 2 4 8 16 32 Prompt Length

88

90

92

94

96

98

100

Accuracy(%)

PACS

A C P S Average

1 2 4 8 16 32 Prompt Length

40

50

60

70

80

90

100

Accuracy(%)

DomainNet

C I P Q

R S Average

**Figure 3.** Effect of prompt length on PACS and DomainNet datasets over three runs with different random seeds.

prompts may introduce noise or task-irrelevant information, which can negatively impact the alignment between image and text. Moreover, when using long prompts, the prompt weighting strategy employed in FaST-PT may lead to issues such as semantic dilution and reduced interpretability. We observe that when the prompt length is set to 4, most tasks, as well as the average accuracy, achieve their optimal performance. Therefore, we adopt a prompt length of 4 as the default setting in our experiments.

Result under Few-shot scenario To investigate the effectiveness of our framework in a few-shot setting, we compare the generalization ability of FaST-PT with existing promptbased methods under varying conditions of extremely limited data (shots = 1, 2, 4, 8, 16, 32). As illustrated in Figure 4, we observe that the performance of all methods improves with the increase in training samples. FaST-PT consistently demonstrates significant advantages across all settings on both the PACS and DomainNet datasets. These experimental results indicate that FaST-PT is capable of capturing both global and domain-specific information under few-shot settings, achieving robust generalization to unseen domains.

Cost Analysis We analysis the efficiency of FaST-PT in terms of communication and computation cost. We selected one representative method from each of the three categories of baseline approaches for analysis. For fairness, all methods employ ViT-L/14 as the visual encoder, with a consistent batch size of 16 and prompt length set to 4. Regarding communication efficiency, we measure params each client uploads per training round. Compared to traditional FL that requires uploading the entire model, prompt-based FL methods incur significantly lower communication costs.

1 2 4 8 16 32 Shots

88

90

92

94

96

98

Accuracy(%)

PACS

PromptFL FedAPT DiPrompt FaST-PT(ours)

1 2 4 8 16 32 Shots

78

80

82

84

86

88

Accuracy(%)

DomainNet

PromptFL FedAPT DiPrompt FaST-PT(ours)

**Figure 4.** Few-shot performance on PACS and DomainNet datasets over three runs with different random seeds.

## Method

FedAvg FedADG DiPrompt Ours Parameters 305M 318M 0.012M 0.005M FLOPs 1.296T 2.593T 1.739T 1.431T

**Table 4.** Communication and computation cost compared with baseline FDG methods. (Batchsize = 16)

Moreover, relative to DiPrompt, our method utilizes more lightweight and efficient modules, resulting in fewer than half the number of transmitted parameters. In terms of computational cost, we evaluated the FLOPs for processing a batch during inference. The additional modules introduced by FedADG substantially increase inference cost, whereas our approach only adds a domain classifier. Consequently, its FLOPs are only slightly higher than FedAvg and remain lower than those of DiPrompt.

## Conclusion

In this work, we propose a new framework named FaST-PT, which integrates CLIP into FL to tackle the FDG problem in terms of local feature augmentation and efficient unseen domain adaptation. Specifically, FaST-PT utilizes the MST strategy that allows clients to generate image embedding of external domains for mitigating the domain shift among clients. Besides, we design a prompt tuning module that partitions the prompt for capturing general and domain-specific knowledge, along with a domain-aware prompt generation mechanism to achieve the similarity-based domain knowledge mixing for efficient adaptation to unseen domains. Extensive experiments demonstrate that FaST-PT outperforms existing FDG methods across all the generalization tasks on four benchmark cross-domain datasets.

20433

<!-- Page 8 -->

## Acknowledgments

This work was supported by the National Natural Science Foundation of China under Grant 62572311, 62202302, U21B2019, 62406347, and 62572260.

## References

Bai, S.; Zhang, J.; Guo, S.; Li, S.; Guo, J.; Hou, J.; Han, T.; and Lu, X. 2024. Diprompt: Disentangled prompt tuning for multiple latent domain generalization in federated learning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 27284–27293.

Bui, M.-H.; Tran, T.; Tran, A.; and Phung, D. 2021. Exploiting domain-specific features to enhance domain generalization. Advances in Neural Information Processing Systems, 34: 21189–21201.

Chen, J.; Jiang, M.; Dou, Q.; and Chen, Q. 2023. Federated domain generalization for image recognition via cross-client style transfer. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 361–370.

Fang, C.; Xu, Y.; and Rockmore, D. N. 2013. Unbiased metric learning: On the utilization of multiple datasets and web images for softening bias. In Proceedings of the IEEE international conference on computer vision, 1657–1664.

Guan, H.; Yap, P.-T.; Bozoki, A.; and Liu, M. 2024. Federated learning for medical image analysis: A survey. Pattern Recognition, 110424.

Guo, T.; Guo, S.; Wang, J.; Tang, X.; and Xu, W. 2023. Promptfl: Let federated participants cooperatively learn prompts instead of models-federated learning in age of foundation model. IEEE Transactions on Mobile Computing.

Huang, W.; Ye, M.; Shi, Z.; Li, H.; and Du, B. 2023. Rethinking federated learning with domain shift: A prototype view. In 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 16312–16322. IEEE.

Khattak, M. U.; Rasheed, H.; Maaz, M.; Khan, S.; and Khan, F. S. 2023. Maple: Multi-modal prompt learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 19113–19122.

Koneˇcn`y, J.; McMahan, H. B.; Yu, F. X.; Richt´arik, P.; Suresh, A. T.; and Bacon, D. 2016. Federated learning: Strategies for improving communication efficiency. arXiv preprint arXiv:1610.05492.

Le, K.; Ho, L.; Do, C.; Le-Phuoc, D.; and Wong, K.-S. 2024. Efficiently assemble normalization layers and regularization for federated domain generalization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 6027–6036.

Lester, B.; Al-Rfou, R.; and Constant, N. 2021. The power of scale for parameter-efficient prompt tuning. arXiv preprint arXiv:2104.08691.

Li, D.; Yang, Y.; Song, Y.-Z.; and Hospedales, T. M. 2017. Deeper, broader and artier domain generalization. In Proceedings of the IEEE international conference on computer vision, 5542–5550.

Li, T.; Sahu, A. K.; Zaheer, M.; Sanjabi, M.; Talwalkar, A.; and Smith, V. 2020. Federated optimization in heterogeneous networks. Proceedings of Machine learning and systems, 2: 429–450. Li, X.; Jiang, M.; Zhang, X.; Kamp, M.; and Dou, Q. 2021. Fedbn: Federated learning on non-iid features via local batch normalization. arXiv preprint arXiv:2102.07623. Li, Y.; Gong, M.; Tian, X.; Liu, T.; and Tao, D. 2018. Domain generalization via conditional invariant representations. In Proceedings of the AAAI conference on artificial intelligence, volume 32. Liu, Q.; Chen, C.; Qin, J.; Dou, Q.; and Heng, P.-A. 2021. Feddg: Federated domain generalization on medical image segmentation via episodic learning in continuous frequency space. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 1013–1023. McMahan, B.; Moore, E.; Ramage, D.; Hampson, S.; and y Arcas, B. A. 2017. Communication-efficient learning of deep networks from decentralized data. In Artificial intelligence and statistics, 1273–1282. PMLR. Muandet, K.; Balduzzi, D.; and Sch¨olkopf, B. 2013. Domain generalization via invariant feature representation. In International conference on machine learning, 10–18. PMLR. Nguyen, A. T.; Torr, P.; and Lim, S. N. 2022. Fedsr: A simple and effective domain generalization method for federated learning. Advances in Neural Information Processing Systems, 35: 38831–38843. Peng, X.; Bai, Q.; Xia, X.; Huang, Z.; Saenko, K.; and Wang, B. 2019. Moment matching for multi-source domain adaptation. In Proceedings of the IEEE/CVF international conference on computer vision, 1406–1415. Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. Learning transferable visual models from natural language supervision. In International conference on machine learning, 8748–8763. PMLR. Su, S.; Yang, M.; Li, B.; and Xue, X. 2024. Federated adaptive prompt tuning for multi-domain collaborative learning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, 15117–15125. Venkateswara, H.; Eusebio, J.; Chakraborty, S.; and Panchanathan, S. 2017. Deep hashing network for unsupervised domain adaptation. In Proceedings of the IEEE conference on computer vision and pattern recognition, 5018–5027. Wu, G.; and Gong, S. 2021. Collaborative optimization and aggregation for decentralized domain generalization and adaptation. In Proceedings of the IEEE/CVF international conference on computer vision, 6484–6493. Yang, F.-E.; Wang, C.-Y.; and Wang, Y.-C. F. 2023. Efficient model personalization in federated learning via client-specific prompt generation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, 19159–19168. Zhang, H.; Zhang, Y.-F.; Liu, W.; Weller, A.; Sch¨olkopf, B.; and Xing, E. P. 2022. Towards principled disentanglement for domain generalization. In Proceedings of the IEEE/CVF

20434

<!-- Page 9 -->

conference on computer vision and pattern recognition, 8024–8034. Zhang, L.; Lei, X.; Shi, Y.; Huang, H.; and Chen, C. 2021a. Federated learning with domain generalization. arXiv preprint arXiv:2111.10487. Zhang, L.; Lei, X.; Shi, Y.; Huang, H.; and Chen, C. 2021b. Federated learning with domain generalization. arXiv preprint arXiv:2111.10487. Zhao, H.; Du, W.; Li, F.; Li, P.; and Liu, G. 2023. Fed- Prompt: Communication-Efficient and Privacy-Preserving Prompt Tuning in Federated Learning. In ICASSP 2023- 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 1–5. IEEE. Zhou, K.; Yang, J.; Loy, C. C.; and Liu, Z. 2022a. Conditional prompt learning for vision-language models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 16816–16825. Zhou, K.; Yang, J.; Loy, C. C.; and Liu, Z. 2022b. Learning to prompt for vision-language models. International Journal of Computer Vision, 130(9): 2337–2348.

20435
